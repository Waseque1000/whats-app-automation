"""Metric card component for dashboard analytics."""
import customtkinter as ctk
from typing import Optional
from app.ui import theme

class StatCard(ctk.CTkFrame):
    """Reusable card widget displaying a KPI metric."""

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
            corner_radius=8,
            **kwargs,
        )
        self.accent_color = accent_color or theme.COLOR_PRIMARY
        self._title_text = title
        self._value_text = value
        self._subtext_text = subtext

        self._setup_ui()

    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=1)

        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text=self._title_text.upper(),
            font=theme.FONT_BODY_SM,
            text_color=theme.COLOR_TEXT_MUTED,
            anchor="w",
        )
        self.title_label.grid(row=0, column=0, padx=16, pady=(14, 4), sticky="w")

        # Big Number Value
        self.value_label = ctk.CTkLabel(
            self,
            text=self._value_text,
            font=theme.FONT_HEADLINE_XL,
            text_color=theme.COLOR_TEXT,
            anchor="w",
        )
        self.value_label.grid(row=1, column=0, padx=16, pady=(0, 4), sticky="w")

        # Subtitle / Details
        self.subtext_label = ctk.CTkLabel(
            self,
            text=self._subtext_text,
            font=theme.FONT_BODY_SM,
            text_color=self.accent_color,
            anchor="w",
        )
        self.subtext_label.grid(row=2, column=0, padx=16, pady=(0, 14), sticky="w")

    def update_values(self, value: str, subtext: Optional[str] = None):
        """Updates the metric value and optional subtext."""
        self._value_text = str(value)
        self.value_label.configure(text=self._value_text)
        if subtext is not None:
            self._subtext_text = subtext
            self.subtext_label.configure(text=self._subtext_text)
