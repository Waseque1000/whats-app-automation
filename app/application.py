"""Main desktop application window and lifecycle manager."""
import customtkinter as ctk
from typing import Dict, Any, Optional

from app.ui import theme
from app.ui.components.sidebar import Sidebar
from app.ui.dashboard import DashboardPage
from app.ui.students_page import StudentsPage
from app.ui.campaigns_page import CampaignsPage
from app.ui.templates_page import TemplatesPage
from app.ui.reports_page import ReportsPage
from app.ui.settings_page import SettingsPage

from app.database.connection import get_db_connection
from app.database.migrations import run_migrations
from app.database.repository import (
    StudentsRepository,
    CampaignsRepository,
    TemplatesRepository,
    ImportsRepository,
    SettingsRepository,
)
from app.services.campaign_service import CampaignService
from app.messaging.mock_provider import MockProvider
from app.messaging.whatsapp_web import WhatsAppWebProvider
from app.utils.logger import logger

class WhatsAppStudentMessengerApp(ctk.CTk):
    """Primary application window implementing CustomTkinter shell."""

    def __init__(self):
        super().__init__()

        # Window geometry and styling
        self.title("WhatsApp Student Messenger")
        self.geometry("1280x820")
        self.minsize(1080, 680)
        self.configure(fg_color=theme.COLOR_BACKGROUND)

        # Set CustomTkinter dark appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        # Initialize SQLite database and run migrations
        self.conn = get_db_connection()
        run_migrations(self.conn)

        # Initialize Repositories
        self.students_repo = StudentsRepository(self.conn)
        self.campaigns_repo = CampaignsRepository(self.conn)
        self.templates_repo = TemplatesRepository(self.conn)
        self.imports_repo = ImportsRepository(self.conn)
        self.settings_repo = SettingsRepository(self.conn)

        # Initialize Messaging Providers & Services
        default_region = self.settings_repo.get("default_region", "BD")
        self.mock_provider = MockProvider()
        self.whatsapp_web_provider = WhatsAppWebProvider()

        provider_type = self.settings_repo.get("provider", "mock")
        self.active_provider = self.whatsapp_web_provider if provider_type == "whatsapp_web" else self.mock_provider

        self.campaign_service = CampaignService(
            self.campaigns_repo, self.students_repo, self.active_provider
        )

        # Main window layout: 2 columns (Sidebar, Content Stage)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Instantiate Sidebar
        self.sidebar = Sidebar(self, on_navigate=self.navigate_to)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Container for pages
        self.stage_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stage_frame.grid(row=0, column=1, sticky="nsew")
        self.stage_frame.grid_rowconfigure(0, weight=1)
        self.stage_frame.grid_columnconfigure(0, weight=1)

        # Pages map
        self.pages: Dict[str, ctk.CTkFrame] = {}
        self._init_pages(default_region)

        # Start on dashboard
        self.navigate_to("dashboard")
        logger.info("Application initialized successfully.")

    def _init_pages(self, default_region: str):
        # 1. Dashboard
        self.pages["dashboard"] = DashboardPage(
            self.stage_frame,
            students_repo=self.students_repo,
            campaigns_repo=self.campaigns_repo,
            imports_repo=self.imports_repo,
            on_navigate=self.navigate_to,
        )

        # 2. Students
        self.pages["students"] = StudentsPage(
            self.stage_frame,
            students_repo=self.students_repo,
            imports_repo=self.imports_repo,
            default_region=default_region,
        )

        # 3. Campaigns
        self.pages["campaigns"] = CampaignsPage(
            self.stage_frame,
            campaigns_repo=self.campaigns_repo,
            students_repo=self.students_repo,
            templates_repo=self.templates_repo,
            campaign_service=self.campaign_service,
        )

        # 4. Templates
        self.pages["templates"] = TemplatesPage(
            self.stage_frame,
            templates_repo=self.templates_repo,
            students_repo=self.students_repo,
        )

        # 5. Reports
        self.pages["reports"] = ReportsPage(
            self.stage_frame,
            campaigns_repo=self.campaigns_repo,
            students_repo=self.students_repo,
        )

        # 6. Settings
        self.pages["settings"] = SettingsPage(
            self.stage_frame,
            settings_repo=self.settings_repo,
            whatsapp_web_provider=self.whatsapp_web_provider,
            on_settings_changed=self._on_settings_changed,
            on_provider_changed=self.set_active_provider,
        )

    def set_active_provider(self, provider_type: str):
        """Switches the active messaging provider between mock and whatsapp_web."""
        if provider_type == "whatsapp_web":
            self.active_provider = self.whatsapp_web_provider
        else:
            self.active_provider = self.mock_provider

        self.campaign_service.provider = self.active_provider
        self.settings_repo.set("provider", provider_type)
        logger.info(f"Active provider switched to: {self.active_provider.provider_name}")

        # Update sidebar footer
        if hasattr(self, "sidebar") and hasattr(self.sidebar, "update_provider_status"):
            is_conn = self.active_provider.is_connected()
            display_name = "WhatsApp Web Active" if provider_type == "whatsapp_web" else "Mock Gateway Active"
            self.sidebar.update_provider_status(display_name, is_connected=is_conn)

    def _on_settings_changed(self, new_region: str):
        logger.info(f"Applying new default region to students page: {new_region}")
        self.pages["students"].default_region = new_region
        self.pages["students"].import_service.validation_service.set_default_region(new_region)

    def navigate_to(self, page_key: str):
        """Switches the active viewport view."""
        if page_key not in self.pages:
            logger.warning(f"Navigating to unknown page: {page_key}")
            return

        for key, page in self.pages.items():
            if key == page_key:
                page.grid(row=0, column=0, sticky="nsew")
                if hasattr(page, "refresh"):
                    page.refresh()
            else:
                page.grid_forget()

        self.sidebar.set_active(page_key)

    def on_closing(self):
        """Cleanup upon window close."""
        logger.info("Application closing. Cleaning up resources...")
        try:
            self.mock_provider.disconnect()
            self.whatsapp_web_provider.disconnect()
            self.conn.close()
        except Exception:
            pass
        self.destroy()
