"""Campaign creation wizard, consent review, explicit confirmation, and execution monitor."""
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from datetime import datetime
from typing import Dict, Any, List, Optional

from app.ui import theme
from app.ui.components.table_view import TableView
from app.ui.components.modal_dialog import ModalDialog
from app.database.repository import CampaignsRepository, StudentsRepository, TemplatesRepository
from app.services.campaign_service import CampaignService
from app.utils.logger import logger

class CampaignsPage(ctk.CTkFrame):
    """Campaign builder and live dispatch orchestration."""

    def __init__(
        self,
        master,
        campaigns_repo: CampaignsRepository,
        students_repo: StudentsRepository,
        templates_repo: TemplatesRepository,
        campaign_service: CampaignService,
        **kwargs,
    ):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.campaigns_repo = campaigns_repo
        self.students_repo = students_repo
        self.templates_repo = templates_repo
        self.campaign_service = campaign_service

        self._selected_student_ids: List[int] = []
        self._current_campaign_id: Optional[int] = None
        self._is_paused = False

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._setup_ui()
        self.refresh()

    def _setup_ui(self):
        # Header banner
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, padx=24, pady=(20, 12), sticky="ew")

        title = ctk.CTkLabel(
            header,
            text="Campaigns & Dispatcher",
            font=theme.FONT_HEADLINE_XL,
            text_color=theme.COLOR_TEXT,
            anchor="w",
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            header,
            text="Configure outbound student campaigns, enforce consent compliance, and audit message delivery",
            font=theme.FONT_BODY_MD,
            text_color=theme.COLOR_TEXT_MUTED,
            anchor="w",
        )
        subtitle.pack(anchor="w")

        # Main content tabview or wizard steps
        self.tabview = ctk.CTkTabview(
            self,
            fg_color=theme.COLOR_CARD,
            segmented_button_selected_color=theme.COLOR_PRIMARY,
            segmented_button_selected_hover_color=theme.COLOR_PRIMARY_HOVER,
            text_color="#0F1115",
            segmented_button_unselected_color=theme.COLOR_SIDEBAR,
            segmented_button_unselected_hover_color=theme.COLOR_CARD_HOVER,
        )
        self.tabview.grid(row=1, column=0, padx=24, pady=(0, 20), sticky="nsew")

        self.tab_wizard = self.tabview.add("1. Create Campaign")
        self.tab_monitor = self.tabview.add("2. Dispatch Monitor")

        self._setup_wizard_tab()
        self._setup_monitor_tab()

    def _setup_wizard_tab(self):
        tab = self.tab_wizard
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=1)
        tab.grid_rowconfigure(1, weight=1)

        # Left Column: Campaign Details & Template Picker
        details_box = ctk.CTkFrame(tab, fg_color="transparent")
        details_box.grid(row=0, column=0, rowspan=2, padx=(12, 8), pady=12, sticky="nsew")
        details_box.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(details_box, text="CAMPAIGN SETUP", font=theme.FONT_HEADLINE_SM, text_color=theme.COLOR_TEXT_MUTED).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        # Campaign Name
        ctk.CTkLabel(details_box, text="Campaign Name:", font=theme.FONT_BODY_MD, text_color=theme.COLOR_TEXT).grid(row=1, column=0, sticky="w", pady=6)
        self.camp_name_entry = ctk.CTkEntry(
            details_box,
            placeholder_text="e.g. Midterm Results Notification",
            height=34,
            corner_radius=6,
            fg_color=theme.COLOR_SIDEBAR,
            border_color=theme.COLOR_BORDER,
        )
        self.camp_name_entry.grid(row=1, column=1, sticky="ew", padx=(8, 0), pady=6)

        # Template Selection Dropdown
        ctk.CTkLabel(details_box, text="Message Template:", font=theme.FONT_BODY_MD, text_color=theme.COLOR_TEXT).grid(row=2, column=0, sticky="w", pady=6)
        self.template_var = tk.StringVar(value="(Select Template)")
        self.template_menu = ctk.CTkOptionMenu(
            details_box,
            variable=self.template_var,
            values=["(Select Template)"],
            height=34,
            corner_radius=6,
            fg_color=theme.COLOR_SIDEBAR,
            button_color=theme.COLOR_CARD_HOVER,
            command=self._on_template_selected,
        )
        self.template_menu.grid(row=2, column=1, sticky="ew", padx=(8, 0), pady=6)

        # Template Body preview/editor
        ctk.CTkLabel(details_box, text="Message Body:", font=theme.FONT_BODY_MD, text_color=theme.COLOR_TEXT).grid(row=3, column=0, sticky="nw", pady=(10, 0))
        self.msg_body_text = ctk.CTkTextbox(
            details_box,
            height=200,
            fg_color=theme.COLOR_SIDEBAR,
            border_width=1,
            border_color=theme.COLOR_BORDER,
            corner_radius=6,
            font=theme.FONT_BODY_MD,
            wrap="word",
        )
        self.msg_body_text.grid(row=3, column=1, sticky="nsew", padx=(8, 0), pady=(10, 0))

        # Right Column: Recipient Selection
        recipient_box = ctk.CTkFrame(tab, fg_color="transparent")
        recipient_box.grid(row=0, column=1, rowspan=2, padx=(8, 12), pady=12, sticky="nsew")
        recipient_box.grid_rowconfigure(2, weight=1)
        recipient_box.grid_columnconfigure(0, weight=1)

        # Header with Select All / Deselect All
        rec_hdr = ctk.CTkFrame(recipient_box, fg_color="transparent")
        rec_hdr.grid(row=0, column=0, sticky="ew", pady=(0, 6))

        ctk.CTkLabel(rec_hdr, text="SELECT RECIPIENTS", font=theme.FONT_HEADLINE_SM, text_color=theme.COLOR_TEXT_MUTED).pack(side="left")

        btn_select_all = ctk.CTkButton(
            rec_hdr,
            text="Select All",
            font=theme.FONT_BODY_SM,
            width=70,
            height=26,
            fg_color=theme.COLOR_SIDEBAR,
            command=self._select_all_recipients,
        )
        btn_select_all.pack(side="right", padx=4)

        btn_clear = ctk.CTkButton(
            rec_hdr,
            text="Clear",
            font=theme.FONT_BODY_SM,
            width=50,
            height=26,
            fg_color=theme.COLOR_SIDEBAR,
            command=self._clear_recipients,
        )
        btn_clear.pack(side="right", padx=4)

        # Batch filter for recipient list
        batch_strip = ctk.CTkFrame(recipient_box, fg_color="transparent")
        batch_strip.grid(row=1, column=0, sticky="ew", pady=(0, 6))

        ctk.CTkLabel(batch_strip, text="Filter Batch:", font=theme.FONT_BODY_SM, text_color=theme.COLOR_TEXT_MUTED).pack(side="left", padx=(0, 6))
        self.rec_batch_var = tk.StringVar(value="All Batches")
        self.rec_batch_menu = ctk.CTkOptionMenu(
            batch_strip,
            variable=self.rec_batch_var,
            values=["All Batches"],
            height=28,
            width=140,
            fg_color=theme.COLOR_SIDEBAR,
            button_color=theme.COLOR_CARD_HOVER,
            command=lambda v: self._reload_recipient_picker(),
        )
        self.rec_batch_menu.pack(side="left")

        # Recipient Selection Table
        picker_cols = [
            ("id", "ID", 40),
            ("name", "Student Name", 140),
            ("phone", "Phone", 120),
            ("batch", "Batch", 80),
            ("consent_status", "Consent", 90),
        ]
        self.picker_table = TableView(recipient_box, columns=picker_cols, multi_select=True)
        self.picker_table.grid(row=2, column=0, sticky="nsew")

        # Action: Review & Confirmation
        self.btn_review = ctk.CTkButton(
            recipient_box,
            text="Review & Confirm Campaign →",
            font=theme.FONT_HEADLINE_SM,
            fg_color=theme.COLOR_PRIMARY,
            hover_color=theme.COLOR_PRIMARY_HOVER,
            text_color="#0F1115",
            height=38,
            corner_radius=6,
            command=self._open_review_modal,
        )
        self.btn_review.grid(row=3, column=0, pady=(12, 0), sticky="ew")

    def _setup_monitor_tab(self):
        tab = self.tab_monitor
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(2, weight=1)

        # Top status banner
        top_banner = ctk.CTkFrame(tab, fg_color=theme.COLOR_SIDEBAR, corner_radius=6)
        top_banner.grid(row=0, column=0, padx=16, pady=(12, 8), sticky="ew")
        top_banner.grid_columnconfigure(1, weight=1)

        self.monitor_camp_name = ctk.CTkLabel(
            top_banner,
            text="No active campaign selected.",
            font=theme.FONT_HEADLINE_SM,
            text_color=theme.COLOR_TEXT,
            anchor="w",
        )
        self.monitor_camp_name.grid(row=0, column=0, padx=16, pady=10, sticky="w")

        # Controls: Pause / Resume / Cancel
        controls_frame = ctk.CTkFrame(top_banner, fg_color="transparent")
        controls_frame.grid(row=0, column=1, sticky="e", padx=16)

        self.btn_pause = ctk.CTkButton(
            controls_frame,
            text="⏸ Pause",
            font=theme.FONT_BODY_SM,
            fg_color=theme.COLOR_CARD,
            hover_color=theme.COLOR_CARD_HOVER,
            text_color=theme.COLOR_TEXT,
            width=80,
            height=30,
            command=self._toggle_pause,
        )
        self.btn_pause.pack(side="left", padx=4)

        self.btn_cancel = ctk.CTkButton(
            controls_frame,
            text="🛑 Cancel Campaign",
            font=theme.FONT_BODY_SM,
            fg_color=theme.COLOR_DANGER,
            hover_color="#DC2626",
            text_color="#FFFFFF",
            width=120,
            height=30,
            command=self._cancel_active_campaign,
        )
        self.btn_cancel.pack(side="left", padx=4)

        # Progress bar
        self.monitor_progress = ctk.CTkProgressBar(tab, fg_color=theme.COLOR_SIDEBAR, progress_color=theme.COLOR_PRIMARY)
        self.monitor_progress.set(0)
        self.monitor_progress.grid(row=1, column=0, padx=16, pady=(0, 10), sticky="ew")

        # Recipient status table
        queue_cols = [
            ("id", "ID", 50),
            ("student_name", "Student Name", 140),
            ("phone", "Recipient Phone", 130),
            ("status", "Status", 100),
            ("error_message", "Result / Verification Detail", 240),
            ("sent_at", "Sent Timestamp", 140),
        ]
        self.queue_table = TableView(tab, columns=queue_cols)
        self.queue_table.grid(row=2, column=0, padx=16, pady=(0, 16), sticky="nsew")

    def refresh(self):
        """Loads available templates and reload recipient candidates."""
        templates = self.templates_repo.get_all()
        t_names = ["(Select Template)"] + [t["template_name"] for t in templates]
        self.template_menu.configure(values=t_names)

        # Batches
        batches = self.students_repo.get_batches()
        self.rec_batch_menu.configure(values=["All Batches"] + batches)

        self._reload_recipient_picker()

    def _reload_recipient_picker(self):
        batch_filter = "" if self.rec_batch_var.get() == "All Batches" else self.rec_batch_var.get()
        students = self.students_repo.get_all(batch=batch_filter, is_valid=1, limit=300)
        self.picker_table.set_data(students)

    def _select_all_recipients(self):
        for item in self.picker_table.tree.get_children():
            self.picker_table.tree.selection_add(item)

    def _clear_recipients(self):
        self.picker_table.tree.selection_remove(self.picker_table.tree.selection())

    def _on_template_selected(self, choice: str):
        if choice == "(Select Template)":
            return
        templates = self.templates_repo.get_all()
        for t in templates:
            if t["template_name"] == choice:
                self.msg_body_text.delete("1.0", tk.END)
                self.msg_body_text.insert(tk.END, t["content"])
                break

    def _open_review_modal(self):
        """Opens the review and explicit confirmation step."""
        camp_name = self.camp_name_entry.get().strip()
        template_text = self.msg_body_text.get("1.0", tk.END).strip()

        if not camp_name:
            messagebox.showerror("Campaign Name Required", "Please enter a campaign name.")
            return

        if not template_text:
            messagebox.showerror("Template Required", "Please provide a message body for this campaign.")
            return

        selected_records = self.picker_table.get_selected_records()
        if not selected_records:
            messagebox.showerror("Recipients Required", "Please select at least one recipient student.")
            return

        student_ids = [r["id"] for r in selected_records]

        # Stage recipients through the service layer (enforcing opt-out exclusion)
        staging = self.campaign_service.stage_campaign_recipients(student_ids, template_text)
        eligible = staging["eligible_recipients"]
        opted_out = staging["excluded_opted_out"]
        unknown_consent_count = staging["unknown_consent_count"]

        if not eligible:
            messagebox.showerror(
                "No Eligible Recipients",
                "All selected students are opted-out or ineligible. Cannot dispatch campaign.",
            )
            return

        # Modal Review & Confirmation Dialog
        modal = ModalDialog(self.winfo_toplevel(), title="🔒 Campaign Review & Explicit Confirmation", width=620, height=480)
        body = modal.body_frame

        # Review summary cards
        ctk.CTkLabel(
            body,
            text=f"Campaign: {camp_name}",
            font=theme.FONT_HEADLINE_MD,
            text_color=theme.COLOR_PRIMARY,
            anchor="w",
        ).pack(fill="x", pady=(0, 6))

        summary_box = ctk.CTkFrame(body, fg_color=theme.COLOR_CARD, border_width=1, border_color=theme.COLOR_BORDER, corner_radius=6)
        summary_box.pack(fill="x", pady=8, padx=2)

        ctk.CTkLabel(summary_box, text=f"Total Candidates Selected: {len(student_ids)}", font=theme.FONT_BODY_MD, text_color=theme.COLOR_TEXT).pack(anchor="w", padx=16, pady=(10, 2))
        ctk.CTkLabel(summary_box, text=f"✓ Eligible Recipients Queue: {len(eligible)}", font=theme.FONT_HEADLINE_SM, text_color=theme.COLOR_SUCCESS).pack(anchor="w", padx=16, pady=2)

        if opted_out:
            ctk.CTkLabel(
                summary_box,
                text=f"⛔ Excluded (Opted-Out): {len(opted_out)} student(s) automatically blocked by policy",
                font=theme.FONT_BODY_SM,
                text_color=theme.COLOR_DANGER,
            ).pack(anchor="w", padx=16, pady=2)

        if unknown_consent_count > 0:
            warn_frame = ctk.CTkFrame(body, fg_color="#2D1F08", border_width=1, border_color=theme.COLOR_WARNING, corner_radius=6)
            warn_frame.pack(fill="x", pady=6, padx=2)
            ctk.CTkLabel(
                warn_frame,
                text=f"⚠️ Consent Warning: {unknown_consent_count} recipient(s) have 'unknown' consent status.\nEnsure you have a legal or institutional basis to message them.",
                font=theme.FONT_BODY_SM,
                text_color=theme.COLOR_WARNING,
                justify="left",
            ).pack(anchor="w", padx=12, pady=8)

        # Message sample preview
        ctk.CTkLabel(body, text="Personalized Sample Preview:", font=theme.FONT_HEADLINE_SM, text_color=theme.COLOR_TEXT_MUTED).pack(anchor="w", pady=(8, 2))
        preview_box = ctk.CTkTextbox(body, height=80, fg_color=theme.COLOR_SIDEBAR, font=theme.FONT_BODY_SM)
        preview_box.insert(tk.END, eligible[0]["personalized_message"])
        preview_box.configure(state="disabled")
        preview_box.pack(fill="x", pady=(0, 10))

        # Checkbox for explicit confirmation
        confirm_var = tk.BooleanVar(value=False)
        chk = ctk.CTkCheckBox(
            body,
            text="I explicitly confirm that these recipients and message content comply with messaging policies.",
            variable=confirm_var,
            font=theme.FONT_BODY_SM,
            fg_color=theme.COLOR_PRIMARY,
            text_color=theme.COLOR_TEXT,
        )
        chk.pack(anchor="w", pady=(4, 10))

        def on_confirm_proceed():
            if not confirm_var.get():
                messagebox.showwarning("Confirmation Required", "You must check the explicit confirmation box before launching.")
                return

            try:
                # Create campaign and queue in database
                camp_id, _ = self.campaign_service.create_campaign(
                    campaign_name=camp_name,
                    template_text=template_text,
                    template_id=None,
                    student_ids=student_ids,
                )
                # Record confirmation timestamp
                confirmed_at = self.campaign_service.confirm_and_queue_campaign(camp_id)
                modal.destroy()

                # Switch to monitor tab and start background execution
                self._current_campaign_id = camp_id
                self.monitor_camp_name.configure(
                    text=f"Campaign #{camp_id}: {camp_name} (Confirmed: {confirmed_at[:19]})"
                )
                self.tabview.set("2. Dispatch Monitor")
                self._start_execution(camp_id)

            except Exception as exc:
                logger.error(f"Error creating campaign: {exc}", exc_info=True)
                messagebox.showerror("Campaign Error", str(exc))

        modal.add_button("Cancel", command=modal.destroy, side="right")
        modal.add_button("✓ Confirm & Launch", command=on_confirm_proceed, is_primary=True, side="right")

    def _start_execution(self, campaign_id: int):
        """Starts background worker and connects progress updates."""
        self._is_paused = False
        self.btn_pause.configure(text="⏸ Pause")

        # Load initial queue
        recipients = self.campaigns_repo.get_recipients(campaign_id)
        self.queue_table.set_data(recipients)

        def progress_callback(curr, total, data):
            def update_ui():
                self.monitor_progress.set(curr / max(total, 1))
                # Refresh queue table
                updated_recs = self.campaigns_repo.get_recipients(campaign_id)
                self.queue_table.set_data(updated_recs)
            self.after(0, update_ui)

        def completed_callback(summary):
            def on_complete():
                self.monitor_progress.set(1.0)
                updated_recs = self.campaigns_repo.get_recipients(campaign_id)
                self.queue_table.set_data(updated_recs)
                messagebox.showinfo(
                    "Campaign Completed",
                    f"Campaign #{summary['campaign_id']} finished with status: {summary['status']}\n\n"
                    f"Total: {summary['total']}\n"
                    f"Successful (Verified Sent): {summary['successful']}\n"
                    f"Failed: {summary['failed']}\n"
                    f"Skipped: {summary['skipped']}",
                )
            self.after(0, on_complete)

        self.campaign_service.start_campaign_execution(
            campaign_id,
            on_progress=progress_callback,
            on_completed=completed_callback,
        )

    def _toggle_pause(self):
        if not self._current_campaign_id:
            return
        if not self._is_paused:
            self.campaign_service.pause_execution()
            self._is_paused = True
            self.btn_pause.configure(text="▶ Resume")
        else:
            self.campaign_service.resume_execution()
            self._is_paused = False
            self.btn_pause.configure(text="⏸ Pause")

    def _cancel_active_campaign(self):
        if not self._current_campaign_id:
            return
        confirm = messagebox.askyesno("Cancel Campaign", "Are you sure you want to cancel this campaign? Dispatched messages cannot be undone.")
        if confirm:
            self.campaign_service.cancel_execution(self._current_campaign_id)
            self.btn_pause.configure(state="disabled")
            self.btn_cancel.configure(state="disabled")
