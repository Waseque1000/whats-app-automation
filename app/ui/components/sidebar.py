"""Sidebar navigation rail component for desktop application."""
import customtkinter as ctk
from typing import Callable, Dict
from app.ui import theme


class Sidebar(ctk.CTkFrame):
    """Persistent sidebar navigation rail — premium dark variant."""

    def __init__(
        self,
        master,
        on_navigate: Callable[[str], None],
        **kwargs,
    ):
        super().__init__(
            master,
            width=250,
            corner_radius=0,
            fg_color=theme.COLOR_SIDEBAR,
            border_width=0,
            **kwargs,
        )
        self.on_navigate = on_navigate
        self._buttons: Dict[str, ctk.CTkButton] = {}
        self._indicators: Dict[str, ctk.CTkFrame] = {}
        self._current_page: str = "dashboard"

        self.grid_rowconfigure(8, weight=1)
        self._setup_ui()

    def _setup_ui(self):
        # ── Brand Header ──────────────────────────────────────────────────────
        brand_frame = ctk.CTkFrame(
            self,
            fg_color="#0A1628",
            corner_radius=0,
            height=72,
        )
        brand_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 8))
        brand_frame.grid_propagate(False)
        brand_frame.grid_columnconfigure(0, weight=1)

        logo_label = ctk.CTkLabel(
            brand_frame,
            text="⚡ Student Messenger",
            font=(theme.FONT_FAMILY, 16, "bold"),
            text_color=theme.COLOR_PRIMARY,
            anchor="w",
        )
        logo_label.grid(row=0, column=0, padx=20, pady=(18, 2), sticky="w")

        sub_label = ctk.CTkLabel(
            brand_frame,
            text="WhatsApp Desktop Client",
            font=theme.FONT_BODY_SM,
            text_color=theme.COLOR_TEXT_MUTED,
            anchor="w",
        )
        sub_label.grid(row=1, column=0, padx=20, pady=(0, 14), sticky="w")

        # Thin green accent line under brand
        accent_line = ctk.CTkFrame(
            self,
            height=2,
            fg_color=theme.COLOR_PRIMARY,
            corner_radius=0,
        )
        accent_line.grid(row=1, column=0, sticky="ew", padx=0, pady=(0, 16))

        # ── Navigation Items ──────────────────────────────────────────────────
        nav_items = [
            ("dashboard",  "📊   Dashboard"),
            ("students",   "👥   Students Registry"),
            ("campaigns",  "🚀   Campaigns"),
            ("templates",  "📝   Templates"),
            ("reports",    "📑   Reports & History"),
            ("settings",   "⚙️   Settings"),
        ]

        for idx, (page_key, label_text) in enumerate(nav_items, start=2):
            # Row wrapper frame to hold indicator + button side-by-side
            row_frame = ctk.CTkFrame(self, fg_color="transparent", height=46)
            row_frame.grid(row=idx, column=0, padx=0, pady=2, sticky="ew")
            row_frame.grid_propagate(False)
            row_frame.grid_columnconfigure(1, weight=1)

            # Left active indicator bar
            indicator = ctk.CTkFrame(
                row_frame,
                width=4,
                height=46,
                fg_color="transparent",
                corner_radius=2,
            )
            indicator.grid(row=0, column=0, sticky="ns", padx=(6, 0))
            self._indicators[page_key] = indicator

            btn = ctk.CTkButton(
                row_frame,
                text=label_text,
                font=theme.FONT_BODY_MD,
                anchor="w",
                height=42,
                corner_radius=8,
                fg_color="transparent",
                text_color=theme.COLOR_TEXT_MUTED,
                hover_color=theme.COLOR_NAV_HOVER_BG,
                border_width=0,
                command=lambda pk=page_key: self._on_btn_click(pk),
            )
            btn.grid(row=0, column=1, padx=(4, 8), sticky="ew")
            self._buttons[page_key] = btn

        # ── Footer Status ─────────────────────────────────────────────────────
        footer = ctk.CTkFrame(
            self,
            fg_color="#0A1628",
            corner_radius=10,
            border_width=1,
            border_color=theme.COLOR_BORDER,
        )
        footer.grid(row=9, column=0, padx=14, pady=16, sticky="ew")

        dot = ctk.CTkLabel(
            footer, text="●", font=("Arial", 10),
            text_color=theme.COLOR_PRIMARY, width=16,
        )
        dot.pack(side="left", padx=(12, 6), pady=10)

        self.status_text = ctk.CTkLabel(
            footer,
            text="Mock Gateway Active",
            font=theme.FONT_CAPTION,
            text_color=theme.COLOR_TEXT_MUTED,
            anchor="w",
        )
        self.status_text.pack(side="left", fill="x", expand=True, padx=(0, 12), pady=10)
        self.status_dot = dot

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
                    fg_color=theme.COLOR_NAV_ACTIVE_BG,
                    text_color=theme.COLOR_NAV_ACTIVE_TEXT,
                    font=(theme.FONT_FAMILY, 13, "bold"),
                )
                self._indicators[key].configure(fg_color=theme.COLOR_PRIMARY)
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=theme.COLOR_TEXT_MUTED,
                    font=theme.FONT_BODY_MD,
                )
                self._indicators[key].configure(fg_color="transparent")
