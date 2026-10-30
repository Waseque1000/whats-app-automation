"""Reusable dark modal dialog wrapper."""
import customtkinter as ctk
from typing import Optional, Callable
from app.ui import theme

class ModalDialog(ctk.CTkToplevel):
    """Base modal window with dark theme styling and parent transient positioning."""

    def __init__(
        self,
        parent,
        title: str = "Dialog",
        width: int = 560,
        height: int = 420,
        **kwargs,
    ):
        super().__init__(parent, **kwargs)
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.configure(fg_color=theme.COLOR_BACKGROUND)
        self.resizable(False, False)

        # Center relative to parent
        self.transient(parent)
        self.grab_set()

        # Window layout
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Header
        self.header_frame = ctk.CTkFrame(
            self, fg_color=theme.COLOR_SIDEBAR, height=52, corner_radius=0
        )
        self.header_frame.grid(row=0, column=0, sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text=title,
            font=theme.FONT_HEADLINE_SM,
            text_color=theme.COLOR_TEXT,
            anchor="w",
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=12, sticky="w")

        # Body container
        self.body_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.body_frame.grid(row=1, column=0, padx=20, pady=16, sticky="nsew")

        # Footer for buttons
        self.footer_frame = ctk.CTkFrame(
            self, fg_color=theme.COLOR_SIDEBAR, height=56, corner_radius=0
        )
        self.footer_frame.grid(row=2, column=0, sticky="ew")

    def add_button(
        self,
        text: str,
        command: Callable[[], None],
        is_primary: bool = False,
        is_danger: bool = False,
        side: str = "right",
    ) -> ctk.CTkButton:
        """Adds an action button to the modal footer."""
        if is_danger:
            fg = theme.COLOR_DANGER
            hover = "#DC2626"
            txt_color = "#FFFFFF"
        elif is_primary:
            fg = theme.COLOR_PRIMARY
            hover = theme.COLOR_PRIMARY_HOVER
            txt_color = "#0F1115"
        else:
            fg = theme.COLOR_CARD
            hover = theme.COLOR_CARD_HOVER
            txt_color = theme.COLOR_TEXT

        btn = ctk.CTkButton(
            self.footer_frame,
            text=text,
            command=command,
            fg_color=fg,
            hover_color=hover,
            text_color=txt_color,
            font=theme.FONT_HEADLINE_SM,
            height=34,
            corner_radius=6,
        )
        btn.pack(side=side, padx=10, pady=10)
        return btn
