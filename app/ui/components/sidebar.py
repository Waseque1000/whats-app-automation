"""Sidebar navigation rail component for desktop application."""
import customtkinter as ctk
from typing import Callable, Dict
from app.ui import theme

class Sidebar(ctk.CTkFrame):
    """Persistent sidebar navigation rail."""

    def __init__(
        self,
        master,
        on_navigate: Callable[[str], None],
        **kwargs,
    ):
        super().__init__(
            master,
            width=240,
            corner_radius=0,
            fg_color=theme.COLOR_SIDEBAR,
            border_width=1,
            border_color=theme.COLOR_BORDER,
            **kwargs,
        )
        self.on_navigate = on_navigate
        self._buttons: Dict[str, ctk.CTkButton] = {}
        self._current_page: str = "dashboard"

        self.grid_rowconfigure(8, weight=1)  # Spacer row
        self._setup_ui()

    def _setup_ui(self):
        # App brand / header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(24, 20), sticky="ew")

        title_label = ctk.CTkLabel(
            header_frame,
            text="⚡ Student Messenger",
            font=theme.FONT_HEADLINE_MD,
            text_color=theme.COLOR_PRIMARY,
            anchor="w",
        )
        title_label.pack(fill="x")

        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="WhatsApp Desktop Client",
            font=theme.FONT_BODY_SM,
            text_color=theme.COLOR_TEXT_MUTED,
            anchor="w",
        )
        subtitle_label.pack(fill="x")

        # Divider
        divider = ctk.CTkFrame(self, height=1, fg_color=theme.COLOR_BORDER)
        divider.grid(row=1, column=0, padx=16, pady=(0, 16), sticky="ew")

        # Navigation buttons
        nav_items = [
            ("dashboard", "📊  Dashboard"),
            ("students", "👥  Students Registry"),
            ("campaigns", "🚀  Campaigns"),
            ("templates", "📝  Templates"),
            ("reports", "📑  Reports & History"),
            ("settings", "⚙️  Settings"),
        ]

        for idx, (page_key, label_text) in enumerate(nav_items, start=2):
            btn = ctk.CTkButton(
                self,
                text=label_text,
                font=theme.FONT_BODY_MD,
                anchor="w",
                height=38,
                corner_radius=6,
                fg_color="transparent",
                text_color=theme.COLOR_TEXT,
                hover_color=theme.COLOR_CARD_HOVER,
                command=lambda pk=page_key: self._on_btn_click(pk),
            )
            btn.grid(row=idx, column=0, padx=12, pady=4, sticky="ew")
            self._buttons[page_key] = btn

        # Footer status indicator
        footer = ctk.CTkFrame(self, fg_color=theme.COLOR_CARD, corner_radius=6)
        footer.grid(row=9, column=0, padx=12, pady=16, sticky="ew")

        status_dot = ctk.CTkLabel(
            footer,
            text="●",
            font=("Arial", 14),
            text_color=theme.COLOR_PRIMARY,
            width=16,
        )
        status_text = ctk.CTkLabel(
            footer,
            text="Mock Gateway Active",
            font=theme.FONT_CAPTION,
            text_color=theme.COLOR_TEXT_MUTED,
            anchor="w",
        )
        self.status_dot = status_dot
        self.status_text = status_text
        self.status_dot.pack(side="left", padx=(10, 4), pady=8)
        self.status_text.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=8)

        self.set_active("dashboard")

    def update_provider_status(self, provider_name: str, is_connected: bool = True):
        """Updates the status text and indicator in the sidebar footer."""
        self.status_text.configure(text=provider_name)
        self.status_dot.configure(
            text_color=theme.COLOR_PRIMARY if is_connected else theme.COLOR_WARNING
        )

    def _on_btn_click(self, page_key: str):
        self.set_active(page_key)
        self.on_navigate(page_key)

    def set_active(self, page_key: str):
        self._current_page = page_key
        for key, btn in self._buttons.items():
            if key == page_key:
                btn.configure(
                    fg_color=theme.COLOR_CARD,
                    text_color=theme.COLOR_PRIMARY,
                    border_width=1,
                    border_color=theme.COLOR_PRIMARY,
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=theme.COLOR_TEXT,
                    border_width=0,
                )
