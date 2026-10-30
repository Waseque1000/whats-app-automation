"""Application settings view for phone region, messaging preferences, and system diagnostics."""
import tkinter as tk
from tkinter import messagebox
from typing import Optional, Callable
import customtkinter as ctk
import threading
from pathlib import Path

from app.ui import theme
from app.database.repository import SettingsRepository
from app.messaging.whatsapp_web import WhatsAppWebProvider
from app.utils.logger import LOG_FILE, logger

class SettingsPage(ctk.CTkFrame):
    """Settings page allowing configuration of default region, messaging providers, and diagnostics."""

    def __init__(
        self,
        master,
        settings_repo: SettingsRepository,
        whatsapp_web_provider: Optional[WhatsAppWebProvider] = None,
        on_settings_changed: Optional[Callable[[str], None]] = None,
        on_provider_changed: Optional[Callable[[str], None]] = None,
        **kwargs,
    ):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.settings_repo = settings_repo
        self.whatsapp_web_provider = whatsapp_web_provider
        self.on_settings_changed = on_settings_changed
        self.on_provider_changed = on_provider_changed

        self._is_connecting = False

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
            text="Application Settings",
            font=theme.FONT_HEADLINE_XL,
            text_color=theme.COLOR_TEXT,
            anchor="w",
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            header,
            text="Configure default region code, messaging provider mode, and system parameters",
            font=theme.FONT_BODY_MD,
            text_color=theme.COLOR_TEXT_MUTED,
            anchor="w",
        )
        subtitle.pack(anchor="w")

        # Scrollable container for settings sections
        container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        container.grid(row=1, column=0, padx=24, pady=(0, 20), sticky="nsew")
        container.grid_columnconfigure(0, weight=1)

        # Section 1: Phone Normalization Settings
        s1 = ctk.CTkFrame(container, fg_color=theme.COLOR_CARD, border_width=1, border_color=theme.COLOR_BORDER, corner_radius=8)
        s1.pack(fill="x", pady=(0, 16))
        s1.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(s1, text="PHONE NUMBER PARSING & REGION", font=theme.FONT_HEADLINE_SM, text_color=theme.COLOR_TEXT_MUTED).grid(row=0, column=0, columnspan=2, padx=16, pady=(16, 8), sticky="w")

        ctk.CTkLabel(s1, text="Default ISO Country Code:\n(Used when phone number lacks country prefix)", font=theme.FONT_BODY_MD, text_color=theme.COLOR_TEXT, justify="left").grid(row=1, column=0, padx=16, pady=8, sticky="w")

        self.region_var = tk.StringVar(value="BD")
        self.region_menu = ctk.CTkOptionMenu(
            s1,
            variable=self.region_var,
            values=["BD (Bangladesh, +880)", "US (United States, +1)", "GB (United Kingdom, +44)", "IN (India, +91)", "CA (Canada, +1)", "AU (Australia, +61)", "AE (UAE, +971)", "SA (Saudi Arabia, +966)"],
            width=260,
            height=34,
            fg_color=theme.COLOR_SIDEBAR,
            button_color=theme.COLOR_CARD_HOVER,
        )
        self.region_menu.grid(row=1, column=1, padx=16, pady=8, sticky="e")

        # Section 2: Messaging Provider Integration
        s2 = ctk.CTkFrame(container, fg_color=theme.COLOR_CARD, border_width=1, border_color=theme.COLOR_BORDER, corner_radius=8)
        s2.pack(fill="x", pady=(0, 16))
        s2.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(s2, text="MESSAGING INTEGRATION & WHATSAPP CONNECTION", font=theme.FONT_HEADLINE_SM, text_color=theme.COLOR_TEXT_MUTED).grid(row=0, column=0, columnspan=2, padx=16, pady=(16, 8), sticky="w")

        ctk.CTkLabel(s2, text="Active Messaging Provider:", font=theme.FONT_BODY_MD, text_color=theme.COLOR_TEXT).grid(row=1, column=0, padx=16, pady=8, sticky="w")

        self.provider_var = tk.StringVar(value="mock")
        provider_choice_frame = ctk.CTkFrame(s2, fg_color="transparent")
        provider_choice_frame.grid(row=1, column=1, padx=16, pady=8, sticky="e")

        self.radio_mock = ctk.CTkRadioButton(
            provider_choice_frame,
            text="Mock Simulator (Testing)",
            variable=self.provider_var,
            value="mock",
            command=self._on_provider_selected,
            fg_color=theme.COLOR_PRIMARY,
        )
        self.radio_mock.pack(side="left", padx=8)

        self.radio_wweb = ctk.CTkRadioButton(
            provider_choice_frame,
            text="WhatsApp Web (Real WhatsApp)",
            variable=self.provider_var,
            value="whatsapp_web",
            command=self._on_provider_selected,
            fg_color=theme.COLOR_PRIMARY,
        )
        self.radio_wweb.pack(side="left", padx=8)

        # WhatsApp Web Connect Panel
        self.wweb_frame = ctk.CTkFrame(s2, fg_color=theme.COLOR_SIDEBAR, border_width=1, border_color=theme.COLOR_BORDER, corner_radius=6)
        self.wweb_frame.grid(row=2, column=0, columnspan=2, padx=16, pady=(8, 16), sticky="ew")
        self.wweb_frame.grid_columnconfigure(0, weight=1)

        instructions_text = (
            "📱 How to Connect Your Real WhatsApp:\n"
            "1. Click '🔗 Open WhatsApp Web & Scan QR' below.\n"
            "2. A Chromium browser window will open to web.whatsapp.com.\n"
            "3. On your phone: Open WhatsApp → Settings / Three Dots → Linked Devices → Link a Device.\n"
            "4. Scan the QR code displayed on screen. Once scanned, your session is saved locally in data/whatsapp_session/."
        )
        self.inst_lbl = ctk.CTkLabel(
            self.wweb_frame,
            text=instructions_text,
            font=theme.FONT_BODY_SM,
            text_color=theme.COLOR_TEXT_MUTED,
            justify="left",
            anchor="w",
        )
        self.inst_lbl.grid(row=0, column=0, columnspan=2, padx=14, pady=(12, 10), sticky="w")

        # Connection status row
        status_row = ctk.CTkFrame(self.wweb_frame, fg_color="transparent")
        status_row.grid(row=1, column=0, columnspan=2, padx=14, pady=(0, 12), sticky="ew")

        self.wweb_status_lbl = ctk.CTkLabel(
            status_row,
            text="● WhatsApp Web Status: Disconnected / Not Logged In",
            font=theme.FONT_HEADLINE_SM,
            text_color=theme.COLOR_WARNING,
        )
        self.wweb_status_lbl.pack(side="left")

        self.btn_connect_wweb = ctk.CTkButton(
            status_row,
            text="🔗 Open WhatsApp Web & Scan QR",
            font=theme.FONT_HEADLINE_SM,
            fg_color=theme.COLOR_PRIMARY,
            hover_color=theme.COLOR_PRIMARY_HOVER,
            text_color="#0F1115",
            height=34,
            corner_radius=6,
            command=self._connect_whatsapp_web_thread,
        )
        self.btn_connect_wweb.pack(side="right", padx=6)

        self.btn_disconnect_wweb = ctk.CTkButton(
            status_row,
            text="Disconnect",
            font=theme.FONT_BODY_SM,
            fg_color=theme.COLOR_CARD,
            hover_color=theme.COLOR_CARD_HOVER,
            text_color=theme.COLOR_TEXT,
            border_width=1,
            border_color=theme.COLOR_BORDER,
            height=34,
            corner_radius=6,
            command=self._disconnect_whatsapp_web,
        )
        self.btn_disconnect_wweb.pack(side="right", padx=6)

        # Section 3: Diagnostic Logs
        s3 = ctk.CTkFrame(container, fg_color=theme.COLOR_CARD, border_width=1, border_color=theme.COLOR_BORDER, corner_radius=8)
        s3.pack(fill="x", pady=(0, 16))
        s3.grid_columnconfigure(0, weight=1)

        log_hdr = ctk.CTkFrame(s3, fg_color="transparent")
        log_hdr.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 6))

        ctk.CTkLabel(log_hdr, text="DIAGNOSTIC LOG (data/logs/app.log)", font=theme.FONT_HEADLINE_SM, text_color=theme.COLOR_TEXT_MUTED).pack(side="left")
        btn_refresh_log = ctk.CTkButton(
            log_hdr,
            text="Refresh Logs",
            font=theme.FONT_BODY_SM,
            width=90,
            height=26,
            fg_color=theme.COLOR_SIDEBAR,
            command=self._load_log_preview,
        )
        btn_refresh_log.pack(side="right")

        self.log_text = ctk.CTkTextbox(
            s3,
            height=140,
            fg_color=theme.COLOR_SIDEBAR,
            font=theme.FONT_CODE_SM,
            text_color="#94A3B8",
            wrap="word",
        )
        self.log_text.grid(row=1, column=0, padx=16, pady=(0, 16), sticky="ew")

        # Save Settings Button
        btn_save = ctk.CTkButton(
            container,
            text="Save Settings",
            font=theme.FONT_HEADLINE_SM,
            fg_color=theme.COLOR_PRIMARY,
            hover_color=theme.COLOR_PRIMARY_HOVER,
            text_color="#0F1115",
            height=38,
            corner_radius=6,
            command=self._save_settings,
        )
        btn_save.pack(anchor="w", pady=(0, 20))

    def _on_provider_selected(self):
        choice = self.provider_var.get()
        if self.on_provider_changed:
            self.on_provider_changed(choice)

    def _connect_whatsapp_web_thread(self):
        if not self.whatsapp_web_provider:
            messagebox.showerror("Error", "WhatsApp Web provider not initialized.")
            return

        if self._is_connecting:
            return

        self._is_connecting = True
        self.btn_connect_wweb.configure(state="disabled", text="Opening Browser...")
        self.wweb_status_lbl.configure(
            text="● Opening browser... please scan QR code on screen",
            text_color=theme.COLOR_INFO,
        )

        def worker():
            logger.info("Starting WhatsApp Web connect worker...")
            success = self.whatsapp_web_provider.connect(timeout_sec=120)

            def on_done():
                self._is_connecting = False
                self.btn_connect_wweb.configure(state="normal", text="🔗 Open WhatsApp Web & Scan QR")
                if success:
                    self.wweb_status_lbl.configure(
                        text="● WhatsApp Web Status: Connected & Ready (Logged in)",
                        text_color=theme.COLOR_SUCCESS,
                    )
                    self.provider_var.set("whatsapp_web")
                    if self.on_provider_changed:
                        self.on_provider_changed("whatsapp_web")
                    messagebox.showinfo(
                        "WhatsApp Web Connected",
                        "WhatsApp Web has been successfully linked and authenticated!\n\n"
                        "Your session is saved in data/whatsapp_session/.\n"
                        "Active messaging provider switched to WhatsApp Web for campaigns.",
                    )
                else:
                    self.wweb_status_lbl.configure(
                        text="● WhatsApp Web Status: Not Connected or Timed Out",
                        text_color=theme.COLOR_WARNING,
                    )
                    messagebox.showwarning(
                        "Connection Incomplete",
                        "Could not verify WhatsApp Web login within the time limit.\n"
                        "Make sure to scan the QR code with WhatsApp on your phone.",
                    )

            self.after(0, on_done)

        t = threading.Thread(target=worker, daemon=True)
        t.start()

    def _disconnect_whatsapp_web(self):
        if self.whatsapp_web_provider:
            self.whatsapp_web_provider.disconnect()
            self.wweb_status_lbl.configure(
                text="● WhatsApp Web Status: Disconnected",
                text_color=theme.COLOR_WARNING,
            )
            messagebox.showinfo("Disconnected", "WhatsApp Web browser session closed.")

    def refresh(self):
        """Loads active settings from SQLite database."""
        val = self.settings_repo.get("default_region", "BD")
        for choice in self.region_menu._values:
            if choice.startswith(val):
                self.region_var.set(choice)
                break

        # Provider setting
        cur_provider = self.settings_repo.get("provider", "mock")
        self.provider_var.set(cur_provider)

        # Check real-time connection status
        if self.whatsapp_web_provider and self.whatsapp_web_provider.is_connected():
            self.wweb_status_lbl.configure(
                text="● WhatsApp Web Status: Connected & Ready (Logged in)",
                text_color=theme.COLOR_SUCCESS,
            )
        else:
            self.wweb_status_lbl.configure(
                text="● WhatsApp Web Status: Disconnected / Not Logged In",
                text_color=theme.COLOR_WARNING,
            )

        self._load_log_preview()

    def _load_log_preview(self):
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", tk.END)
        if LOG_FILE.exists():
            try:
                lines = LOG_FILE.read_text(encoding="utf-8").splitlines()
                recent = "\n".join(lines[-30:])
                self.log_text.insert(tk.END, recent)
            except Exception as exc:
                self.log_text.insert(tk.END, f"Error reading log: {exc}")
        else:
            self.log_text.insert(tk.END, "Log file not yet initialized.")
        self.log_text.configure(state="disabled")

    def _save_settings(self):
        choice = self.region_var.get()
        code = choice.split()[0].strip().upper()
        self.settings_repo.set("default_region", code)

        provider_choice = self.provider_var.get()
        self.settings_repo.set("provider", provider_choice)
        if self.on_provider_changed:
            self.on_provider_changed(provider_choice)

        logger.info(f"Settings updated: region={code}, provider={provider_choice}")

        if self.on_settings_changed:
            self.on_settings_changed(code)

        messagebox.showinfo(
            "Settings Saved",
            f"Settings updated successfully.\n\n"
            f"• Default Region: {code}\n"
            f"• Active Messaging Provider: {provider_choice}",
        )
