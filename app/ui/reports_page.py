"""Campaign history, recipient audit inspection, and CSV/XLSX export tools."""
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from typing import Dict, Any, List, Optional
from pathlib import Path

from app.ui import theme
from app.ui.components.table_view import TableView
from app.database.repository import CampaignsRepository, StudentsRepository
from app.services.report_service import ReportService
from app.utils.logger import logger

class ReportsPage(ctk.CTkFrame):
    """Historical audit logs and report export view."""

    def __init__(
        self,
        master,
        campaigns_repo: CampaignsRepository,
        students_repo: StudentsRepository,
        **kwargs,
    ):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.campaigns_repo = campaigns_repo
        self.students_repo = students_repo
        self.report_service = ReportService(students_repo, campaigns_repo)
        self._selected_campaign_id: Optional[int] = None

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._setup_ui()
        self.refresh()

    def _setup_ui(self):
        # Header banner
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, padx=24, pady=(20, 12), sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header,
            text="Campaign Reports & History",
            font=theme.FONT_HEADLINE_XL,
            text_color=theme.COLOR_TEXT,
            anchor="w",
        )
        title.grid(row=0, column=0, sticky="w")

        subtitle = ctk.CTkLabel(
            header,
            text="Examine historical campaign outcomes, export detailed delivery logs, and download audit sheets",
            font=theme.FONT_BODY_MD,
            text_color=theme.COLOR_TEXT_MUTED,
            anchor="w",
        )
        subtitle.grid(row=1, column=0, sticky="w")

        # Export Buttons
        btn_box = ctk.CTkFrame(header, fg_color="transparent")
        btn_box.grid(row=0, column=1, rowspan=2, sticky="e")

        btn_export_all = ctk.CTkButton(
            btn_box,
            text="Export All Summary (CSV)",
            font=theme.FONT_BODY_SM,
            fg_color=theme.COLOR_CARD,
            hover_color=theme.COLOR_CARD_HOVER,
            text_color=theme.COLOR_TEXT,
            border_width=1,
            border_color=theme.COLOR_BORDER,
            height=34,
            corner_radius=6,
            command=self._export_all_campaigns_csv,
        )
        btn_export_all.pack(side="left", padx=4)

        self.btn_export_selected_csv = ctk.CTkButton(
            btn_box,
            text="Export Selected (CSV)",
            font=theme.FONT_HEADLINE_SM,
            fg_color=theme.COLOR_PRIMARY,
            hover_color=theme.COLOR_PRIMARY_HOVER,
            text_color="#0F1115",
            height=34,
            corner_radius=6,
            command=lambda: self._export_selected_campaign("csv"),
        )
        self.btn_export_selected_csv.pack(side="left", padx=4)

        self.btn_export_selected_xlsx = ctk.CTkButton(
            btn_box,
            text="Export Selected (XLSX)",
            font=theme.FONT_HEADLINE_SM,
            fg_color=theme.COLOR_SECONDARY,
            hover_color=theme.COLOR_SECONDARY_HOVER,
            text_color="#0F1115",
            height=34,
            corner_radius=6,
            command=lambda: self._export_selected_campaign("xlsx"),
        )
        self.btn_export_selected_xlsx.pack(side="left", padx=4)

        # Campaigns History Table
        hist_frame = ctk.CTkFrame(self, fg_color="transparent")
        hist_frame.grid(row=1, column=0, padx=24, pady=(0, 10), sticky="ew")
        hist_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(hist_frame, text="PAST CAMPAIGNS (Click row to inspect recipients)", font=theme.FONT_HEADLINE_SM, text_color=theme.COLOR_TEXT_MUTED).grid(row=0, column=0, sticky="w", pady=(0, 4))

        camp_cols = [
            ("id", "ID", 40),
            ("campaign_name", "Campaign Name", 200),
            ("status", "Status", 90),
            ("total_recipients", "Total", 60),
            ("successful_recipients", "Sent", 60),
            ("failed_recipients", "Failed", 60),
            ("skipped_recipients", "Skipped", 60),
            ("confirmed_at", "Confirmed At", 140),
            ("completed_at", "Completed At", 140),
        ]
        self.camp_table = TableView(
            hist_frame,
            columns=camp_cols,
            on_select=self._on_campaign_row_selected,
            height=160,
        )
        self.camp_table.grid(row=1, column=0, sticky="nsew")

        # Recipient Details Table for Selected Campaign
        rec_frame = ctk.CTkFrame(self, fg_color="transparent")
        rec_frame.grid(row=2, column=0, padx=24, pady=(0, 20), sticky="nsew")
        rec_frame.grid_rowconfigure(1, weight=1)
        rec_frame.grid_columnconfigure(0, weight=1)

        self.rec_label = ctk.CTkLabel(
            rec_frame,
            text="RECIPIENT DISPATCH LOGS",
            font=theme.FONT_HEADLINE_SM,
            text_color=theme.COLOR_TEXT_MUTED,
        )
        self.rec_label.grid(row=0, column=0, sticky="w", pady=(4, 4))

        rec_cols = [
            ("id", "Log ID", 50),
            ("student_name", "Student Name", 140),
            ("phone", "Recipient Phone", 130),
            ("consent_status", "Consent", 80),
            ("status", "Status", 90),
            ("personalized_message", "Message Dispatched", 240),
            ("error_message", "Error / Result Detail", 180),
            ("sent_at", "Sent Timestamp", 140),
        ]
        self.rec_table = TableView(rec_frame, columns=rec_cols)
        self.rec_table.grid(row=1, column=0, sticky="nsew")

    def refresh(self):
        """Reloads campaigns list and updates detail view."""
        campaigns = self.campaigns_repo.get_campaigns(limit=100)
        self.camp_table.set_data(campaigns)

        if campaigns and not self._selected_campaign_id:
            self._select_campaign(campaigns[0]["id"], campaigns[0]["campaign_name"])

    def _on_campaign_row_selected(self, record: Dict[str, Any]):
        cid = record.get("id")
        cname = record.get("campaign_name", "Campaign")
        if cid:
            self._select_campaign(cid, cname)

    def _select_campaign(self, campaign_id: int, campaign_name: str):
        self._selected_campaign_id = campaign_id
        self.rec_label.configure(
            text=f"RECIPIENT DISPATCH LOGS — CAMPAIGN #{campaign_id} ({campaign_name})"
        )
        recipients = self.campaigns_repo.get_recipients(campaign_id)
        self.rec_table.set_data(recipients)

    def _export_selected_campaign(self, fmt: str):
        if not self._selected_campaign_id:
            messagebox.showwarning("Selection Required", "Please select a campaign from the list first.")
            return

        ext = f".{fmt}"
        file_path = filedialog.asksaveasfilename(
            defaultextension=ext,
            filetypes=[(f"{fmt.upper()} files", f"*{ext}")],
            title=f"Export Campaign #{self._selected_campaign_id} Report",
        )
        if not file_path:
            return

        try:
            saved = self.report_service.export_campaign_report(
                self._selected_campaign_id, output_path=file_path, export_format=fmt
            )
            messagebox.showinfo("Export Successful", f"Campaign report exported to:\n{saved}")
        except Exception as exc:
            logger.error(f"Failed exporting campaign: {exc}", exc_info=True)
            messagebox.showerror("Export Failed", str(exc))

    def _export_all_campaigns_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Export All Campaigns Summary",
        )
        if not file_path:
            return

        try:
            saved = self.report_service.export_all_campaigns(output_path=file_path, export_format="csv")
            messagebox.showinfo("Export Successful", f"All campaigns summary exported to:\n{saved}")
        except Exception as exc:
            logger.error(f"Failed exporting all campaigns: {exc}", exc_info=True)
            messagebox.showerror("Export Failed", str(exc))
