"""Metric card component for dashboard analytics."""
import customtkinter as ctk
from typing import Optional
from app.ui import theme


# Icon map for stat cards (title keyword → emoji icon)
_ICON_MAP = {
    "student": "👥",
    "valid": "✅",
    "phone": "✅",
    "campaign": "🚀",
    "message": "💬",
    "sent": "💬",
    "report": "📑",
    "template": "📝",
}


def _resolve_icon(title: str) -> str:
    lower = title.lower()
    for kw, icon in _ICON_MAP.items():
        if kw in lower:
            return icon
    return "📌"


class StatCard(ctk.CTkFrame):
    """Premium KPI metric card with colored accent top-bar and icon."""

    def __init__(
        self,
        master,
        title: str,
        value: str = "0",
        subtext: str = "",
        accent_color: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(
            master,
            fg_color=theme.COLOR_CARD,
            border_width=1,
            border_color=theme.COLOR_BORDER,
            corner_radius=12,
            **kwargs,
        )
        self.accent_color = accent_color or theme.COLOR_PRIMARY
        self._title_text = title
        self._value_text = value
        self._subtext_text = subtext
        self._icon = _resolve_icon(title)

        self._setup_ui()

    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=1)

        # Colored top accent bar
        accent_bar = ctk.CTkFrame(
            self,
            height=4,
            fg_color=self.accent_color,
            corner_radius=0,
        )
        accent_bar.grid(row=0, column=0, sticky="ew", padx=0, pady=0)

        # Icon + Title row
        top_row = ctk.CTkFrame(self, fg_color="transparent")
        top_row.grid(row=1, column=0, padx=16, pady=(14, 4), sticky="ew")
        top_row.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            top_row,
            text=self._title_text.upper(),
            font=theme.FONT_BODY_SM,
            text_color=theme.COLOR_TEXT_MUTED,
            anchor="w",
        )
        self.title_label.grid(row=0, column=0, sticky="w")

        icon_label = ctk.CTkLabel(
            top_row,
            text=self._icon,
            font=("Arial", 20),
            text_color=self.accent_color,
            width=30,
            anchor="e",
        )
        icon_label.grid(row=0, column=1, sticky="e")

        # Big Number Value
        self.value_label = ctk.CTkLabel(
            self,
            text=self._value_text,
            font=(theme.FONT_FAMILY, 32, "bold"),
            text_color=theme.COLOR_TEXT,
            anchor="w",
        )
        self.value_label.grid(row=2, column=0, padx=16, pady=(4, 4), sticky="w")

        # Subtext with accent color
        self.subtext_label = ctk.CTkLabel(
            self,
            text=self._subtext_text,
            font=theme.FONT_BODY_SM,
            text_color=self.accent_color,
            anchor="w",
        )
        self.subtext_label.grid(row=3, column=0, padx=16, pady=(0, 16), sticky="w")

    def update_values(self, value: str, subtext: Optional[str] = None):
        """Updates the metric value and optional subtext."""
        self._value_text = str(value)
        self.value_label.configure(text=self._value_text)
        if subtext is not None:
            self._subtext_text = subtext
            self.subtext_label.configure(text=self._subtext_text)
