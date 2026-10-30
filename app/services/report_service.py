"""Export service for exporting student registries and campaign reports to CSV and Excel."""
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd

from app.database.repository import StudentsRepository, CampaignsRepository
from app.utils.logger import logger

class ReportService:
    """Handles report generation and exact data exports to CSV and XLSX formats."""

    def __init__(self, students_repo: StudentsRepository, campaigns_repo: CampaignsRepository):
        self.students_repo = students_repo
        self.campaigns_repo = campaigns_repo

    def export_students(
        self,
        output_path: str,
        export_format: str = "csv",
        search: str = "",
        batch: str = "",
        consent_status: str = "",
    ) -> str:
        """
        Exports students matching filter criteria to CSV or XLSX.
        Exported fields exactly mirror the database columns.
        """
        students = self.students_repo.get_all(
            search=search, batch=batch, consent_status=consent_status
        )
        df = pd.DataFrame(students)

        # Standard column order
        cols = [
            "id", "name", "phone", "raw_phone", "email", "batch",
            "whatsapp_status", "consent_status", "is_valid",
            "validation_error", "is_duplicate", "created_at", "updated_at"
        ]
        if not df.empty:
            df = df[[c for c in cols if c in df.columns]]
        else:
            df = pd.DataFrame(columns=cols)

        return self._save_df(df, output_path, export_format)

    def export_campaign_report(
        self,
        campaign_id: int,
        output_path: str,
        export_format: str = "csv",
    ) -> str:
        """
        Exports all recipient logs and statuses for a specific campaign.
        Matches exact database values from campaign_recipients.
        """
        campaign = self.campaigns_repo.get_campaign(campaign_id)
        if not campaign:
            raise ValueError(f"Campaign #{campaign_id} not found.")

        recipients = self.campaigns_repo.get_recipients(campaign_id)
        df = pd.DataFrame(recipients)

        cols = [
            "id", "campaign_id", "student_id", "student_name", "phone",
            "consent_status", "sms_variant", "variant_index", "personalized_message", "status",
            "error_message", "sent_at", "updated_at"
        ]
        if not df.empty:
            df = df[[c for c in cols if c in df.columns]]
        else:
            df = pd.DataFrame(columns=cols)

        return self._save_df(df, output_path, export_format)

    def export_all_campaigns(
        self,
        output_path: str,
        export_format: str = "csv",
    ) -> str:
        """Exports high-level campaign summary history."""
        campaigns = self.campaigns_repo.get_campaigns(limit=500)
        df = pd.DataFrame(campaigns)

        cols = [
            "id", "campaign_name", "status", "total_recipients",
            "successful_recipients", "failed_recipients", "skipped_recipients",
            "confirmed_at", "created_at", "completed_at"
        ]
        if not df.empty:
            df = df[[c for c in cols if c in df.columns]]
        else:
            df = pd.DataFrame(columns=cols)

        return self._save_df(df, output_path, export_format)

    @staticmethod
    def _save_df(df: pd.DataFrame, output_path: str, export_format: str) -> str:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fmt = export_format.lower().strip()

        if fmt == "csv" or path.suffix.lower() == ".csv":
            if not str(path).lower().endswith(".csv"):
                path = path.with_suffix(".csv")
            df.to_csv(str(path), index=False, encoding="utf-8")
        elif fmt in ("xlsx", "excel") or path.suffix.lower() == ".xlsx":
            if not str(path).lower().endswith(".xlsx"):
                path = path.with_suffix(".xlsx")
            df.to_excel(str(path), index=False, engine="openpyxl")
        else:
            raise ValueError(f"Unsupported export format: {export_format}")

        logger.info(f"Exported {len(df)} records to {path}")
        return str(path)
