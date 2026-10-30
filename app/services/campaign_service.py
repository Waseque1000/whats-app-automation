"""Campaign creation, recipient staging, opt-out enforcement, and queue execution worker."""
import threading
import time
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable, Tuple

from app.messaging.base import BaseMessagingProvider, RecipientStatus, ProviderMessageResult
from app.services.template_service import TemplateService
from app.database.repository import CampaignsRepository, StudentsRepository
from app.utils.logger import logger

class CampaignService:
    """Manages campaign staging, opt-out rules enforcement, confirmation audit, and async execution."""

    def __init__(
        self,
        campaigns_repo: CampaignsRepository,
        students_repo: StudentsRepository,
        provider: BaseMessagingProvider,
    ):
        self.campaigns_repo = campaigns_repo
        self.students_repo = students_repo
        self.provider = provider

        self._active_thread: Optional[threading.Thread] = None
        self._pause_event = threading.Event()
        self._pause_event.set()  # Unpaused by default
        self._cancel_flag = False

    def stage_campaign_recipients(
        self,
        student_ids: List[int],
        template_text: str,
    ) -> Dict[str, Any]:
        """
        Filters candidates, strictly excludes opted-out students in the service layer,
        identifies unknown-consent students for UI warning, and generates personalized messages.

        Returns:
            {
                "eligible_recipients": List[Dict[str, Any]],
                "excluded_opted_out": List[Dict[str, Any]],
                "unknown_consent_count": int,
                "total_selected": int,
            }
        """
        students = self.students_repo.get_by_ids(student_ids)

        eligible: List[Dict[str, Any]] = []
        opted_out: List[Dict[str, Any]] = []
        unknown_consent_count = 0

        for s in students:
            consent = str(s.get("consent_status", "unknown")).lower()
            if consent == "opted_out":
                logger.warning(
                    f"Service layer rejected student id={s['id']} ({s['name']}) from campaign: status is opted_out."
                )
                opted_out.append(s)
                continue

            if consent == "unknown":
                unknown_consent_count += 1

            # Render message
            msg = TemplateService.render(template_text, s)
            eligible.append({
                "student_id": s["id"],
                "phone": s["phone"],
                "name": s["name"],
                "consent_status": s["consent_status"],
                "personalized_message": msg,
                "status": RecipientStatus.PENDING.value,
            })

        return {
            "eligible_recipients": eligible,
            "excluded_opted_out": opted_out,
            "unknown_consent_count": unknown_consent_count,
            "total_selected": len(students),
        }

    def create_campaign(
        self,
        campaign_name: str,
        template_text: str,
        template_id: Optional[int],
        student_ids: List[int],
    ) -> Tuple[int, Dict[str, Any]]:
        """
        Creates a draft campaign with verified eligible recipients.
        Throws ValueError if no eligible recipients or name is empty.
        """
        if not campaign_name.strip():
            raise ValueError("Campaign name cannot be empty.")

        staging = self.stage_campaign_recipients(student_ids, template_text)
        eligible = staging["eligible_recipients"]

        if not eligible:
            raise ValueError("Cannot create campaign: no eligible recipients (students may be opted-out or empty).")

        campaign_id = self.campaigns_repo.create(
            name=campaign_name,
            message_template=template_text,
            template_id=template_id,
            total_recipients=len(eligible),
        )

        self.campaigns_repo.add_recipients(campaign_id, eligible)
        logger.info(f"Created campaign #{campaign_id} '{campaign_name}' with {len(eligible)} recipients.")
        return campaign_id, staging

    def confirm_and_queue_campaign(
        self,
        campaign_id: int,
    ) -> str:
        """
        Explicit confirmation step required by business rules.
        Logs timestamp and updates status to 'queued'.
        """
        campaign = self.campaigns_repo.get_campaign(campaign_id)
        if not campaign:
            raise ValueError(f"Campaign #{campaign_id} not found.")

        confirmed_at = datetime.now().isoformat()
        self.campaigns_repo.record_confirmation(campaign_id, confirmed_at)
        logger.info(
            f"Campaign #{campaign_id} explicit confirmation logged at {confirmed_at}. Status transitioned to queued."
        )
        return confirmed_at

    def start_campaign_execution(
        self,
        campaign_id: int,
        on_progress: Optional[Callable[[int, int, Dict[str, Any]], None]] = None,
        on_completed: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> None:
        """Launches the campaign processing worker in a background thread."""
        if self._active_thread and self._active_thread.is_alive():
            raise RuntimeError("Another campaign is already actively executing.")

        self._cancel_flag = False
        self._pause_event.set()

        self._active_thread = threading.Thread(
            target=self._run_campaign_queue,
            args=(campaign_id, on_progress, on_completed),
            daemon=True,
            name=f"CampaignWorker-{campaign_id}",
        )
        self._active_thread.start()

    def pause_execution(self) -> None:
        """Pauses the active campaign execution queue."""
        logger.info("Campaign pause requested.")
        self._pause_event.clear()

    def resume_execution(self) -> None:
        """Resumes a paused campaign execution queue."""
        logger.info("Campaign resume requested.")
        self._pause_event.set()

    def cancel_execution(self, campaign_id: Optional[int] = None) -> None:
        """Cancels active campaign execution."""
        logger.warning(f"Campaign cancellation requested for campaign #{campaign_id}.")
        self._cancel_flag = True
        self._pause_event.set()  # Unblock if paused so thread can exit
        if campaign_id:
            self.campaigns_repo.update_campaign_status(campaign_id, "cancelled")

    def _run_campaign_queue(
        self,
        campaign_id: int,
        on_progress: Optional[Callable[[int, int, Dict[str, Any]], None]],
        on_completed: Optional[Callable[[Dict[str, Any]], None]],
    ) -> None:
        """Internal queue processor executing in background thread."""
        logger.info(f"Background worker started for campaign #{campaign_id}")
        self.campaigns_repo.update_campaign_status(campaign_id, "active")

        if not self.provider.is_connected():
            self.provider.connect()

        recipients = self.campaigns_repo.get_recipients(campaign_id)
        total = len(recipients)
        successful = 0
        failed = 0
        skipped = 0

        for idx, r in enumerate(recipients):
            # Check for cancellation
            if self._cancel_flag:
                logger.info(f"Campaign #{campaign_id} worker halted due to cancellation.")
                self.campaigns_repo.update_campaign_status(campaign_id, "cancelled")
                break

            # Check for pause
            self._pause_event.wait()
            if self._cancel_flag:
                break

            rec_id = r["id"]
            phone = r["phone"]
            msg = r["personalized_message"]

            # Double-check opt-out in case status changed in DB
            if r.get("consent_status") == "opted_out":
                self.campaigns_repo.update_recipient_status(
                    recipient_id=rec_id,
                    status=RecipientStatus.SKIPPED.value,
                    error_message="Recipient opted out before dispatch.",
                )
                skipped += 1
                continue

            # Update status to processing
            self.campaigns_repo.update_recipient_status(
                recipient_id=rec_id,
                status=RecipientStatus.PROCESSING.value,
            )

            try:
                # Dispatch through provider
                result: ProviderMessageResult = self.provider.send_message(phone, msg)
                sent_at = datetime.now().isoformat() if result.status in (RecipientStatus.SENT, RecipientStatus.SUBMITTED) else None

                self.campaigns_repo.update_recipient_status(
                    recipient_id=rec_id,
                    status=result.status.value,
                    error_message=result.error_message,
                    sent_at=sent_at,
                )

                if result.status in (RecipientStatus.SENT, RecipientStatus.SUBMITTED):
                    successful += 1
                elif result.status == RecipientStatus.SKIPPED:
                    skipped += 1
                else:
                    failed += 1

            except Exception as exc:
                logger.error(f"Error dispatching to {phone}: {exc}", exc_info=True)
                self.campaigns_repo.update_recipient_status(
                    recipient_id=rec_id,
                    status=RecipientStatus.FAILED.value,
                    error_message=str(exc),
                )
                failed += 1

            # Update counts in campaigns table
            self.campaigns_repo.update_campaign_counts(campaign_id, successful, failed, skipped)

            if on_progress:
                on_progress(idx + 1, total, {
                    "recipient_id": rec_id,
                    "phone": phone,
                    "status": result.status.value if 'result' in locals() else "failed",
                    "successful": successful,
                    "failed": failed,
                    "skipped": skipped,
                })

        final_status = "cancelled" if self._cancel_flag else "completed"
        completed_at = datetime.now().isoformat()
        self.campaigns_repo.update_campaign_status(campaign_id, final_status, completed_at)
        logger.info(
            f"Campaign #{campaign_id} finished with status '{final_status}': "
            f"success={successful}, failed={failed}, skipped={skipped}"
        )

        if on_completed:
            on_completed({
                "campaign_id": campaign_id,
                "status": final_status,
                "total": total,
                "successful": successful,
                "failed": failed,
                "skipped": skipped,
                "completed_at": completed_at,
            })
