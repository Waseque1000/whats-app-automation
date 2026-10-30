"""Dashboard view showcasing metrics, recent campaigns, and recent imports."""
import customtkinter as ctk
from typing import Callable, Optional
from app.ui import theme
from app.ui.components.stat_card import StatCard
from app.ui.components.table_view import TableView
from app.database.repository import StudentsRepository, CampaignsRepository, ImportsRepository

class DashboardPage(ctk.CTkFrame):
    """System overview dashboard matching Stitch and architecture specifications."""

    def __init__(
        self,
        master,
        students_repo: StudentsRepository,
        campaigns_repo: CampaignsRepository,
        imports_repo: ImportsRepository,
        on_navigate: Callable[[str], None],
        **kwargs,
    ):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.students_repo = students_repo
        self.campaigns_repo = campaigns_repo
        self.imports_repo = imports_repo
        self.on_navigate = on_navigate

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
            text="System Overview",
            font=theme.FONT_HEADLINE_XL,
            text_color=theme.COLOR_TEXT,
            anchor="w",
        )
        title.grid(row=0, column=0, sticky="w")

        subtitle = ctk.CTkLabel(
            header,
            text="Real-time campaign logistics, student registries, and verified dispatch audit",
            font=theme.FONT_BODY_MD,
            text_color=theme.COLOR_TEXT_MUTED,
            anchor="w",
        )
        subtitle.grid(row=1, column=0, sticky="w")

        # Quick Actions
        actions_frame = ctk.CTkFrame(header, fg_color="transparent")
        actions_frame.grid(row=0, column=1, rowspan=2, sticky="e")

        btn_new_campaign = ctk.CTkButton(
            actions_frame,
            text="+ New Campaign",
            font=theme.FONT_HEADLINE_SM,
            fg_color=theme.COLOR_PRIMARY,
            hover_color=theme.COLOR_PRIMARY_HOVER,
            text_color="#0F1115",
            height=36,
            corner_radius=6,
            command=lambda: self.on_navigate("campaigns"),
        )
        btn_new_campaign.pack(side="left", padx=6)

        btn_import = ctk.CTkButton(
            actions_frame,
            text="📥 Import Students",
            font=theme.FONT_HEADLINE_SM,
            fg_color=theme.COLOR_CARD,
            hover_color=theme.COLOR_CARD_HOVER,
            text_color=theme.COLOR_TEXT,
            border_width=1,
            border_color=theme.COLOR_BORDER,
            height=36,
            corner_radius=6,
            command=lambda: self.on_navigate("students"),
        )
        btn_import.pack(side="left", padx=6)

        # 4 Stat Cards
        cards_container = ctk.CTkFrame(self, fg_color="transparent")
        cards_container.grid(row=1, column=0, padx=24, pady=(0, 16), sticky="ew")
        for i in range(4):
            cards_container.grid_columnconfigure(i, weight=1)

        self.card_students = StatCard(
            cards_container,
            title="Total Students",
            value="0",
            subtext="0 valid format records",
            accent_color=theme.COLOR_PRIMARY,
        )
        self.card_students.grid(row=0, column=0, padx=(0, 8), sticky="ew")

        self.card_validity = StatCard(
            cards_container,
            title="Valid Phone Formats",
            value="0%",
            subtext="E.164 verified records",
            accent_color=theme.COLOR_INFO,
        )
        self.card_validity.grid(row=0, column=1, padx=4, sticky="ew")

        self.card_campaigns = StatCard(
            cards_container,
            title="Campaigns Created",
            value="0",
            subtext="Local broadcast drafts",
            accent_color=theme.COLOR_SECONDARY,
        )
        self.card_campaigns.grid(row=0, column=2, padx=4, sticky="ew")

        self.card_messages = StatCard(
            cards_container,
            title="Messages Sent",
            value="0",
            subtext="Verified provider submissions",
            accent_color=theme.COLOR_PRIMARY,
        )
        self.card_messages.grid(row=0, column=3, padx=(8, 0), sticky="ew")

        # Two-panel split: Recent Campaigns and Recent Imports
        tables_frame = ctk.CTkFrame(self, fg_color="transparent")
        tables_frame.grid(row=2, column=0, padx=24, pady=(0, 20), sticky="nsew")
        tables_frame.grid_columnconfigure(0, weight=3)
        tables_frame.grid_columnconfigure(1, weight=2)
        tables_frame.grid_rowconfigure(1, weight=1)

        # Left Column: Recent Campaigns
        camp_header = ctk.CTkLabel(
            tables_frame,
            text="RECENT CAMPAIGNS",
            font=theme.FONT_HEADLINE_SM,
            text_color=theme.COLOR_TEXT_MUTED,
            anchor="w",
        )
        camp_header.grid(row=0, column=0, pady=(0, 8), sticky="w")

        camp_cols = [
            ("id", "ID", 40),
            ("campaign_name", "Campaign Name", 160),
            ("status", "Status", 90),
            ("total_recipients", "Recipients", 80),
            ("created_at", "Date", 130),
        ]
        self.campaigns_table = TableView(tables_frame, columns=camp_cols)
        self.campaigns_table.grid(row=1, column=0, padx=(0, 8), sticky="nsew")

        # Right Column: Recent Imports
        imp_header = ctk.CTkLabel(
            tables_frame,
            text="RECENT IMPORTS",
            font=theme.FONT_HEADLINE_SM,
            text_color=theme.COLOR_TEXT_MUTED,
            anchor="w",
        )
        imp_header.grid(row=0, column=1, pady=(0, 8), sticky="w")

        imp_cols = [
            ("filename", "File", 120),
            ("total_rows", "Total", 50),
            ("valid_rows", "Valid", 50),
            ("duplicate_rows", "Dups", 50),
            ("imported_at", "Imported At", 110),
        ]
        self.imports_table = TableView(tables_frame, columns=imp_cols)
        self.imports_table.grid(row=1, column=1, padx=(8, 0), sticky="nsew")

    def refresh(self):
        """Refreshes dashboard metrics and tables from the database."""
        # Refresh student stats
        stu_stats = self.students_repo.get_stats()
        total_students = stu_stats["total_students"]
        valid_students = stu_stats["valid_formats"]

        pct = f"{(valid_students / total_students * 100):.1f}%" if total_students > 0 else "0%"
        self.card_students.update_values(
            str(total_students), f"{valid_students} valid E.164 formats"
        )
        self.card_validity.update_values(pct, f"{stu_stats['invalid_formats']} malformed flagged")

        # Refresh campaign stats
        camp_stats = self.campaigns_repo.get_stats()
        self.card_campaigns.update_values(
            str(camp_stats["total_campaigns"]), "Total local campaigns"
        )
        self.card_messages.update_values(
            str(camp_stats["messages_sent"]), f"{camp_stats['messages_submitted']} submitted, {camp_stats['messages_failed']} failed"
        )

        # Refresh tables
        recent_campaigns = self.campaigns_repo.get_campaigns(limit=10)
        self.campaigns_table.set_data(recent_campaigns)

        recent_imports = self.imports_repo.get_recent(limit=10)
        # Format timestamps nicely for display
        for r in recent_imports:
            ts = r.get("imported_at", "")
            if ts and len(ts) >= 19:
                r["imported_at"] = ts[:19].replace("T", " ")
        self.imports_table.set_data(recent_imports)
