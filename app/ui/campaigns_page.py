"""Campaign creation wizard, consent review, explicit confirmation, and execution monitor."""
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from datetime import datetime
from typing import Dict, Any, List, Optional

from app.ui import theme
from app.ui.components.table_view import TableView
from app.ui.components.modal_dialog import ModalDialog
from app.database.repository import CampaignsRepository, StudentsRepository, TemplatesRepository
from app.services.campaign_service import CampaignService
from app.services.template_service import TemplateService, SUPPORTED_VARIABLES
from app.utils.logger import logger

class CampaignsPage(ctk.CTkFrame):
    """Campaign builder and live dispatch orchestration."""

    def __init__(
        self,
        master,
        campaigns_repo: CampaignsRepository,
        students_repo: StudentsRepository,
        templates_repo: TemplatesRepository,
        campaign_service: CampaignService,
        **kwargs,
    ):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.campaigns_repo = campaigns_repo
        self.students_repo = students_repo
        self.templates_repo = templates_repo
        self.campaign_service = campaign_service

        self._selected_student_ids: List[int] = []
        self._current_campaign_id: Optional[int] = None
        self._is_paused = False

        # Message variations state for anti-restriction rotation
        self._variants: List[str] = [
            "Hello {{name}},\n\nThis is a notification regarding your batch {{batch}}.\n\nThank you!"
        ]
        self._active_variant_index: int = 0

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
            text="Campaigns & Dispatcher",
            font=theme.FONT_HEADLINE_XL,
            text_color=theme.COLOR_TEXT,
            anchor="w",
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            header,
            text="Configure outbound student campaigns, enforce anti-restriction rotation, and audit live delivery",
            font=theme.FONT_BODY_MD,
            text_color=theme.COLOR_TEXT_MUTED,
            anchor="w",
        )
        subtitle.pack(anchor="w")

        # Main content tabview
        self.tabview = ctk.CTkTabview(
            self,
            fg_color=theme.COLOR_CARD,
            segmented_button_selected_color=theme.COLOR_PRIMARY,
            segmented_button_selected_hover_color=theme.COLOR_PRIMARY_HOVER,
            text_color="#0F1115",
            segmented_button_unselected_color=theme.COLOR_SIDEBAR,
            segmented_button_unselected_hover_color=theme.COLOR_CARD_HOVER,
        )
        self.tabview.grid(row=1, column=0, padx=24, pady=(0, 20), sticky="nsew")

        self.tab_wizard = self.tabview.add("1. Create Campaign")
        self.tab_monitor = self.tabview.add("2. Dispatch Monitor")

        self._setup_wizard_tab()
        self._setup_monitor_tab()

    def _setup_wizard_tab(self):
        tab = self.tab_wizard
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=1)
        tab.grid_rowconfigure(0, weight=1)

        # Left Column: Campaign Setup & Message Variations Studio
        details_box = ctk.CTkFrame(tab, fg_color="transparent")
        details_box.grid(row=0, column=0, padx=(12, 8), pady=12, sticky="nsew")
        details_box.grid_columnconfigure(1, weight=1)
        details_box.grid_rowconfigure(3, weight=1)

        ctk.CTkLabel(
            details_box,
            text="CAMPAIGN SETUP",
            font=theme.FONT_HEADLINE_SM,
            text_color=theme.COLOR_TEXT_MUTED,
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        # Campaign Name
        ctk.CTkLabel(
            details_box,
            text="Campaign Name:",
            font=theme.FONT_BODY_MD,
            text_color=theme.COLOR_TEXT,
        ).grid(row=1, column=0, sticky="w", pady=6)
        self.camp_name_entry = ctk.CTkEntry(
            details_box,
            placeholder_text="e.g. Midterm Results Announcement",
            height=34,
            corner_radius=6,
            fg_color=theme.COLOR_SIDEBAR,
            border_color=theme.COLOR_BORDER,
        )
        self.camp_name_entry.grid(row=1, column=1, sticky="ew", padx=(8, 0), pady=6)

        # Template Selection Dropdown
        ctk.CTkLabel(
            details_box,
            text="Load Saved Template:",
            font=theme.FONT_BODY_MD,
            text_color=theme.COLOR_TEXT,
        ).grid(row=2, column=0, sticky="w", pady=6)
        self.template_var = tk.StringVar(value="(Select Template)")
        self.template_menu = ctk.CTkOptionMenu(
            details_box,
            variable=self.template_var,
            values=["(Select Template)"],
            height=34,
            corner_radius=6,
            fg_color=theme.COLOR_SIDEBAR,
            button_color=theme.COLOR_CARD_HOVER,
            command=self._on_template_selected,
        )
        self.template_menu.grid(row=2, column=1, sticky="ew", padx=(8, 0), pady=6)

        # Message Variations Studio (Anti-Restriction Rotation)
        var_card = ctk.CTkFrame(
            details_box,
            fg_color=theme.COLOR_CARD,
            border_width=1,
            border_color=theme.COLOR_BORDER,
            corner_radius=8,
        )
        var_card.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(10, 0))
        var_card.grid_columnconfigure(0, weight=1)
        var_card.grid_rowconfigure(4, weight=1)

        # Card Header with shield badge
        card_hdr = ctk.CTkFrame(var_card, fg_color="transparent")
        card_hdr.grid(row=0, column=0, padx=12, pady=(10, 4), sticky="ew")
        card_hdr.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card_hdr,
            text="🛡️ MESSAGE VARIATIONS (Anti-Restriction)",
            font=theme.FONT_HEADLINE_SM,
            text_color=theme.COLOR_PRIMARY,
        ).grid(row=0, column=0, sticky="w")

        self.var_count_badge = ctk.CTkLabel(
            card_hdr,
            text="1 SMS Type Configured",
            font=theme.FONT_BODY_SM,
            text_color=theme.COLOR_TEXT_MUTED,
        )
        self.var_count_badge.grid(row=0, column=1, sticky="e")

        # Rotation policy explanation
        ctk.CTkLabel(
            var_card,
            text="Provide 3, 4, or 5 SMS types. Messages cycle sequentially across students (Student 1 → SMS 1, Student 2 → SMS 2...) to prevent WhatsApp spam bans.",
            font=theme.FONT_CAPTION,
            text_color=theme.COLOR_TEXT_MUTED,
            justify="left",
            wraplength=380,
        ).grid(row=1, column=0, padx=12, pady=(0, 6), sticky="w")

        # Variation Selector Tabs Bar
        self.tabs_bar = ctk.CTkFrame(var_card, fg_color=theme.COLOR_SIDEBAR, corner_radius=6)
        self.tabs_bar.grid(row=2, column=0, padx=12, pady=4, sticky="ew")

        # Variable insertion toolbar & active variant label
        toolbar = ctk.CTkFrame(var_card, fg_color="transparent")
        toolbar.grid(row=3, column=0, padx=12, pady=(6, 4), sticky="ew")

        self.active_var_label = ctk.CTkLabel(
            toolbar,
            text="Editing SMS #1 (Primary)",
            font=theme.FONT_HEADLINE_SM,
            text_color=theme.COLOR_TEXT,
        )
        self.active_var_label.pack(side="left", padx=(0, 10))

        # Variable tags
        for var in sorted(list(SUPPORTED_VARIABLES)):
            tag = f"{{{{{var}}}}}"
            btn_tag = ctk.CTkButton(
                toolbar,
                text=tag,
                font=theme.FONT_CODE_SM,
                fg_color=theme.COLOR_SIDEBAR,
                hover_color=theme.COLOR_CARD_HOVER,
                text_color=theme.COLOR_PRIMARY,
                border_width=1,
                border_color=theme.COLOR_BORDER,
                height=24,
                width=60,
                corner_radius=4,
                command=lambda v=tag: self._insert_variable_into_variant(v),
            )
            btn_tag.pack(side="left", padx=2)

        # Spintax quick chip
        btn_spin = ctk.CTkButton(
            toolbar,
            text="{Hi|Hello}",
            font=theme.FONT_CODE_SM,
            fg_color=theme.COLOR_SIDEBAR,
            hover_color=theme.COLOR_CARD_HOVER,
            text_color=theme.COLOR_INFO,
            border_width=1,
            border_color=theme.COLOR_BORDER,
            height=24,
            width=70,
            corner_radius=4,
            command=lambda: self._insert_variable_into_variant("{Hello|Hi|Greetings}"),
        )
        btn_spin.pack(side="left", padx=2)

        # Message editor textbox
        self.msg_body_text = ctk.CTkTextbox(
            var_card,
            height=150,
            fg_color=theme.COLOR_SIDEBAR,
            border_width=1,
            border_color=theme.COLOR_BORDER,
            corner_radius=6,
            font=theme.FONT_BODY_MD,
            wrap="word",
        )
        self.msg_body_text.grid(row=4, column=0, padx=12, pady=(4, 6), sticky="nsew")
        self.msg_body_text.bind("<KeyRelease>", lambda e: self._on_variant_text_changed())

        # Footer status bar (char count + validation)
        card_footer = ctk.CTkFrame(var_card, fg_color="transparent")
        card_footer.grid(row=5, column=0, padx=12, pady=(0, 10), sticky="ew")
        card_footer.grid_columnconfigure(0, weight=1)

        self.var_status_label = ctk.CTkLabel(
            card_footer,
            text="✓ All placeholders valid",
            font=theme.FONT_BODY_SM,
            text_color=theme.COLOR_SUCCESS,
            anchor="w",
        )
        self.var_status_label.grid(row=0, column=0, sticky="w")

        self.var_char_label = ctk.CTkLabel(
            card_footer,
            text="0 characters",
            font=theme.FONT_BODY_SM,
            text_color=theme.COLOR_TEXT_MUTED,
            anchor="e",
        )
        self.var_char_label.grid(row=0, column=1, sticky="e")

        # Initial render of tabs
        self._select_variant(0)

        # Right Column: Recipient Selection
        recipient_box = ctk.CTkFrame(tab, fg_color="transparent")
        recipient_box.grid(row=0, column=1, padx=(8, 12), pady=12, sticky="nsew")
        recipient_box.grid_rowconfigure(2, weight=1)
        recipient_box.grid_columnconfigure(0, weight=1)

        # Header with Select All / Deselect All
        rec_hdr = ctk.CTkFrame(recipient_box, fg_color="transparent")
        rec_hdr.grid(row=0, column=0, sticky="ew", pady=(0, 6))

        ctk.CTkLabel(
            rec_hdr,
            text="SELECT RECIPIENTS",
            font=theme.FONT_HEADLINE_SM,
            text_color=theme.COLOR_TEXT_MUTED,
        ).pack(side="left")

        btn_select_all = ctk.CTkButton(
            rec_hdr,
            text="Select All",
            font=theme.FONT_BODY_SM,
            width=70,
            height=26,
            fg_color=theme.COLOR_SIDEBAR,
            command=self._select_all_recipients,
        )
        btn_select_all.pack(side="right", padx=4)

        btn_clear = ctk.CTkButton(
            rec_hdr,
            text="Clear",
            font=theme.FONT_BODY_SM,
            width=50,
            height=26,
            fg_color=theme.COLOR_SIDEBAR,
            command=self._clear_recipients,
        )
        btn_clear.pack(side="right", padx=4)

        # Batch filter for recipient list
        batch_strip = ctk.CTkFrame(recipient_box, fg_color="transparent")
        batch_strip.grid(row=1, column=0, sticky="ew", pady=(0, 6))

        ctk.CTkLabel(
            batch_strip,
            text="Filter Batch:",
            font=theme.FONT_BODY_SM,
            text_color=theme.COLOR_TEXT_MUTED,
        ).pack(side="left", padx=(0, 6))
        self.rec_batch_var = tk.StringVar(value="All Batches")
        self.rec_batch_menu = ctk.CTkOptionMenu(
            batch_strip,
            variable=self.rec_batch_var,
            values=["All Batches"],
            height=28,
            width=140,
            fg_color=theme.COLOR_SIDEBAR,
            button_color=theme.COLOR_CARD_HOVER,
            command=lambda v: self._reload_recipient_picker(),
        )
        self.rec_batch_menu.pack(side="left")

        # Recipient Selection Table
        picker_cols = [
            ("id", "ID", 40),
            ("name", "Student Name", 140),
            ("phone", "Phone", 120),
            ("batch", "Batch", 80),
            ("consent_status", "Consent", 90),
        ]
        self.picker_table = TableView(recipient_box, columns=picker_cols, multi_select=True)
        self.picker_table.grid(row=2, column=0, sticky="nsew")

        # Action: Review & Confirmation
        self.btn_review = ctk.CTkButton(
            recipient_box,
            text="Review & Confirm Campaign →",
            font=theme.FONT_HEADLINE_SM,
            fg_color=theme.COLOR_PRIMARY,
            hover_color=theme.COLOR_PRIMARY_HOVER,
            text_color="#0F1115",
            height=38,
            corner_radius=6,
            command=self._open_review_modal,
        )
        self.btn_review.grid(row=3, column=0, pady=(12, 0), sticky="ew")

    def _setup_monitor_tab(self):
        tab = self.tab_monitor
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(2, weight=1)

        # Top status banner
        top_banner = ctk.CTkFrame(tab, fg_color=theme.COLOR_SIDEBAR, corner_radius=6)
        top_banner.grid(row=0, column=0, padx=16, pady=(12, 8), sticky="ew")
        top_banner.grid_columnconfigure(1, weight=1)

        self.monitor_camp_name = ctk.CTkLabel(
            top_banner,
            text="No active campaign selected.",
            font=theme.FONT_HEADLINE_SM,
            text_color=theme.COLOR_TEXT,
            anchor="w",
        )
        self.monitor_camp_name.grid(row=0, column=0, padx=16, pady=10, sticky="w")

        # Controls: Pause / Resume / Cancel
        controls_frame = ctk.CTkFrame(top_banner, fg_color="transparent")
        controls_frame.grid(row=0, column=1, sticky="e", padx=16)

        self.btn_pause = ctk.CTkButton(
            controls_frame,
            text="⏸ Pause",
            font=theme.FONT_BODY_SM,
            fg_color=theme.COLOR_CARD,
            hover_color=theme.COLOR_CARD_HOVER,
            text_color=theme.COLOR_TEXT,
            width=80,
            height=30,
            command=self._toggle_pause,
        )
        self.btn_pause.pack(side="left", padx=4)

        self.btn_cancel = ctk.CTkButton(
            controls_frame,
            text="🛑 Cancel Campaign",
            font=theme.FONT_BODY_SM,
            fg_color=theme.COLOR_DANGER,
            hover_color="#DC2626",
            text_color="#FFFFFF",
            width=120,
            height=30,
            command=self._cancel_active_campaign,
        )
        self.btn_cancel.pack(side="left", padx=4)

        # Progress bar
        self.monitor_progress = ctk.CTkProgressBar(tab, fg_color=theme.COLOR_SIDEBAR, progress_color=theme.COLOR_PRIMARY)
        self.monitor_progress.set(0)
        self.monitor_progress.grid(row=1, column=0, padx=16, pady=(0, 10), sticky="ew")

        # Recipient status table showing which SMS Design was assigned
        queue_cols = [
            ("id", "ID", 40),
            ("student_name", "Student Name", 130),
            ("phone", "Recipient Phone", 120),
            ("sms_variant", "SMS Design", 90),
            ("status", "Status", 90),
            ("error_message", "Result / Verification Detail", 240),
            ("sent_at", "Sent Timestamp", 130),
        ]
        self.queue_table = TableView(tab, columns=queue_cols)
        self.queue_table.grid(row=2, column=0, padx=16, pady=(0, 16), sticky="nsew")

    # -------------------------------------------------------------
    # Message Variations Management
    # -------------------------------------------------------------
    def _save_current_variant_text(self):
        """Persists the editor text into the active variation index."""
        if 0 <= self._active_variant_index < len(self._variants):
            text = self.msg_body_text.get("1.0", tk.END).strip()
            self._variants[self._active_variant_index] = text

    def _select_variant(self, index: int):
        """Switches the editor to a specific variation index."""
        self._save_current_variant_text()
        self._active_variant_index = max(0, min(index, len(self._variants) - 1))

        self.msg_body_text.delete("1.0", tk.END)
        self.msg_body_text.insert(tk.END, self._variants[self._active_variant_index])

        self._rebuild_variant_tabs()
        self._on_variant_text_changed()

    def _add_variant(self):
        """Adds a new SMS variation (up to 10)."""
        self._save_current_variant_text()
        if len(self._variants) >= 10:
            messagebox.showwarning("Limit Reached", "You can configure up to 10 message variations.")
            return

        starters = [
            "Hello {{name}},\n\nUpdate regarding your batch {{batch}}.\n\nBest regards!",
            "Hi {{name}},\n\nFriendly reminder for your {{batch}} session.\n\nThank you!",
            "Greetings {{name}},\n\nImportant announcement for batch {{batch}}.\n\nRegards!",
            "Dear {{name}},\n\nPlease check the schedule for {{batch}}.\n\nThanks!",
        ]
        next_num = len(self._variants) + 1
        new_text = starters[(next_num - 1) % len(starters)]
        self._variants.append(new_text)
        self._select_variant(len(self._variants) - 1)

    def _remove_variant(self):
        """Removes the currently active variation."""
        self._save_current_variant_text()
        if len(self._variants) <= 1:
            messagebox.showwarning("Cannot Remove", "You must keep at least one message variation.")
            return

        self._variants.pop(self._active_variant_index)
        self._active_variant_index = max(0, min(self._active_variant_index, len(self._variants) - 1))
        self._select_variant(self._active_variant_index)

    def _rebuild_variant_tabs(self):
        """Re-renders tab buttons for all variations."""
        for widget in self.tabs_bar.winfo_children():
            widget.destroy()

        for idx in range(len(self._variants)):
            is_active = (idx == self._active_variant_index)
            btn = ctk.CTkButton(
                self.tabs_bar,
                text=f"SMS #{idx + 1}",
                width=66,
                height=26,
                corner_radius=4,
                font=theme.FONT_HEADLINE_SM if is_active else theme.FONT_BODY_SM,
                fg_color=theme.COLOR_PRIMARY if is_active else theme.COLOR_SIDEBAR,
                hover_color=theme.COLOR_PRIMARY_HOVER if is_active else theme.COLOR_CARD_HOVER,
                text_color="#0F1115" if is_active else theme.COLOR_TEXT,
                command=lambda i=idx: self._select_variant(i),
            )
            btn.pack(side="left", padx=2, pady=3)

        btn_add = ctk.CTkButton(
            self.tabs_bar,
            text="+ Add SMS",
            width=76,
            height=26,
            corner_radius=4,
            font=theme.FONT_BODY_SM,
            fg_color=theme.COLOR_CARD_HOVER,
            hover_color=theme.COLOR_BORDER,
            text_color=theme.COLOR_PRIMARY,
            command=self._add_variant,
        )
        btn_add.pack(side="left", padx=4, pady=3)

        if len(self._variants) > 1:
            btn_rem = ctk.CTkButton(
                self.tabs_bar,
                text="🗑",
                width=30,
                height=26,
                corner_radius=4,
                font=theme.FONT_BODY_SM,
                fg_color=theme.COLOR_SIDEBAR,
                hover_color=theme.COLOR_DANGER,
                text_color=theme.COLOR_DANGER,
                command=self._remove_variant,
            )
            btn_rem.pack(side="left", padx=2, pady=3)

        count = len(self._variants)
        plural = "s" if count != 1 else ""
        self.var_count_badge.configure(
            text=f"{count} SMS Type{plural} (Rotation Active)" if count > 1 else "1 SMS Type (Single)"
        )
        self.active_var_label.configure(
            text=f"Editing SMS #{self._active_variant_index + 1} of {count}"
        )

    def _insert_variable_into_variant(self, tag: str):
        """Inserts a variable placeholder or spintax tag at current cursor."""
        self.msg_body_text.insert(tk.INSERT, tag)
        self._on_variant_text_changed()

    def _on_variant_text_changed(self):
        """Updates validation feedback and char counter for active variation."""
        text = self.msg_body_text.get("1.0", tk.END).strip()
        if 0 <= self._active_variant_index < len(self._variants):
            self._variants[self._active_variant_index] = text

        is_valid, found, unknown = TemplateService.validate_template(text)
        chars = len(text)
        self.var_char_label.configure(text=f"{chars} chars")

        if unknown:
            self.var_status_label.configure(
                text=f"⚠️ Unknown tag: {', '.join(unknown)}",
                text_color=theme.COLOR_WARNING,
            )
        elif not text:
            self.var_status_label.configure(
                text="Template content is empty.",
                text_color=theme.COLOR_TEXT_MUTED,
            )
        else:
            self.var_status_label.configure(
                text=f"✓ Active tags: {', '.join(found) if found else 'none'}",
                text_color=theme.COLOR_SUCCESS,
            )

    # -------------------------------------------------------------
    # Recipient Selection & Templates
    # -------------------------------------------------------------
    def refresh(self):
        """Loads available templates and reload recipient candidates."""
        templates = self.templates_repo.get_all()
        t_names = ["(Select Template)"] + [t["template_name"] for t in templates]
        self.template_menu.configure(values=t_names)

        # Batches
        batches = self.students_repo.get_batches()
        self.rec_batch_menu.configure(values=["All Batches"] + batches)

        self._reload_recipient_picker()

    def _reload_recipient_picker(self):
        batch_filter = "" if self.rec_batch_var.get() == "All Batches" else self.rec_batch_var.get()
        students = self.students_repo.get_all(batch=batch_filter, is_valid=1, limit=300)
        self.picker_table.set_data(students)

    def _select_all_recipients(self):
        for item in self.picker_table.tree.get_children():
            self.picker_table.tree.selection_add(item)

    def _clear_recipients(self):
        self.picker_table.tree.selection_remove(self.picker_table.tree.selection())

    def _on_template_selected(self, choice: str):
        if choice == "(Select Template)":
            return
        templates = self.templates_repo.get_all()
        for t in templates:
            if t["template_name"] == choice:
                variants_list = t.get("variants_list")
                if variants_list and len(variants_list) > 0:
                    self._variants = [v for v in variants_list if v.strip()]
                else:
                    self._variants = [t["content"]] if t.get("content") else [""]
                self._select_variant(0)
                break

    # -------------------------------------------------------------
    # Review & Confirmation Step
    # -------------------------------------------------------------
    def _open_review_modal(self):
        """Opens the review and explicit confirmation step with multi-variant preview."""
        camp_name = self.camp_name_entry.get().strip()
        self._save_current_variant_text()

        active_variants = [v.strip() for v in self._variants if v.strip()]

        if not camp_name:
            messagebox.showerror("Campaign Name Required", "Please enter a campaign name.")
            return

        if not active_variants:
            messagebox.showerror("Template Required", "Please provide at least one message variation.")
            return

        all_valid, all_found, all_unknown = TemplateService.validate_variants(active_variants)
        if all_unknown:
            proceed = messagebox.askyesno(
                "Unknown Placeholders",
                f"Unknown placeholder(s) detected: {', '.join(all_unknown)}.\nDo you still want to proceed?",
            )
            if not proceed:
                return

        selected_records = self.picker_table.get_selected_records()
        if not selected_records:
            messagebox.showerror("Recipients Required", "Please select at least one recipient student.")
            return

        student_ids = [r["id"] for r in selected_records]

        # Stage recipients with round-robin rotation across active variations
        staging = self.campaign_service.stage_campaign_recipients(student_ids, variants=active_variants)
        eligible = staging["eligible_recipients"]
        opted_out = staging["excluded_opted_out"]
        unknown_consent_count = staging["unknown_consent_count"]

        if not eligible:
            messagebox.showerror(
                "No Eligible Recipients",
                "All selected students are opted-out or ineligible. Cannot dispatch campaign.",
            )
            return

        # Modal Review & Confirmation Dialog
        modal = ModalDialog(
            self.winfo_toplevel(),
            title="🔒 Campaign Review & Anti-Restriction Confirmation",
            width=740,
            height=640,
        )
        body = modal.body_frame

        # Top campaign summary
        ctk.CTkLabel(
            body,
            text=f"Campaign: {camp_name}",
            font=theme.FONT_HEADLINE_MD,
            text_color=theme.COLOR_PRIMARY,
            anchor="w",
        ).pack(fill="x", pady=(0, 4))

        summary_box = ctk.CTkFrame(body, fg_color=theme.COLOR_CARD, border_width=1, border_color=theme.COLOR_BORDER, corner_radius=6)
        summary_box.pack(fill="x", pady=6, padx=2)

        ctk.CTkLabel(
            summary_box,
            text=f"Total Candidates Selected: {len(student_ids)}  •  ✓ Eligible Queue: {len(eligible)}",
            font=theme.FONT_BODY_MD,
            text_color=theme.COLOR_TEXT,
        ).pack(anchor="w", padx=14, pady=(8, 2))

        # Anti-restriction rotation summary
        v_count = len(active_variants)
        rot_sub = f"Student 1 → SMS #1, Student 2 → SMS #2" + (f", Student 3 → SMS #3..." if v_count >= 3 else "...")
        ctk.CTkLabel(
            summary_box,
            text=f"🛡️ Anti-Restriction Active: {v_count} SMS design{'s' if v_count != 1 else ''} configured",
            font=theme.FONT_HEADLINE_SM,
            text_color=theme.COLOR_SUCCESS,
        ).pack(anchor="w", padx=14, pady=2)
        ctk.CTkLabel(
            summary_box,
            text=f"Sequential Rotation Pattern: {rot_sub}",
            font=theme.FONT_CAPTION,
            text_color=theme.COLOR_TEXT_MUTED,
        ).pack(anchor="w", padx=14, pady=(0, 8))

        if opted_out:
            ctk.CTkLabel(
                summary_box,
                text=f"⛔ Excluded (Opted-Out): {len(opted_out)} student(s) automatically blocked by policy",
                font=theme.FONT_BODY_SM,
                text_color=theme.COLOR_DANGER,
            ).pack(anchor="w", padx=14, pady=(0, 6))

        if unknown_consent_count > 0:
            warn_frame = ctk.CTkFrame(body, fg_color="#2D1F08", border_width=1, border_color=theme.COLOR_WARNING, corner_radius=6)
            warn_frame.pack(fill="x", pady=4, padx=2)
            ctk.CTkLabel(
                warn_frame,
                text=f"⚠️ Consent Warning: {unknown_consent_count} recipient(s) have 'unknown' consent status.",
                font=theme.FONT_BODY_SM,
                text_color=theme.COLOR_WARNING,
            ).pack(anchor="w", padx=12, pady=6)

        # Multi-Student Live Rotation Preview
        ctk.CTkLabel(
            body,
            text="Multi-Student Rotation Preview (How Students Receive Different Designs):",
            font=theme.FONT_HEADLINE_SM,
            text_color=theme.COLOR_TEXT_MUTED,
        ).pack(anchor="w", pady=(6, 2))

        preview_scroll = ctk.CTkScrollableFrame(body, height=170, fg_color=theme.COLOR_SIDEBAR, corner_radius=6)
        preview_scroll.pack(fill="both", expand=True, pady=(0, 6))

        sample_count = min(len(eligible), 4)
        for i in range(sample_count):
            rec = eligible[i]
            card = ctk.CTkFrame(preview_scroll, fg_color=theme.COLOR_CARD, corner_radius=6, border_width=1, border_color=theme.COLOR_BORDER)
            card.pack(fill="x", padx=6, pady=4)

            hdr_line = ctk.CTkFrame(card, fg_color="transparent")
            hdr_line.pack(fill="x", padx=10, pady=(6, 2))

            ctk.CTkLabel(
                hdr_line,
                text=f"Student #{i + 1}: {rec['name']} ({rec['phone']})",
                font=theme.FONT_HEADLINE_SM,
                text_color=theme.COLOR_TEXT,
            ).pack(side="left")

            ctk.CTkLabel(
                hdr_line,
                text=f"➜  {rec['sms_variant']}",
                font=theme.FONT_HEADLINE_SM,
                text_color=theme.COLOR_PRIMARY,
            ).pack(side="right")

            txt_box = ctk.CTkTextbox(card, height=54, fg_color=theme.COLOR_SIDEBAR, font=theme.FONT_BODY_MD)
            txt_box.insert(tk.END, rec["personalized_message"])
            txt_box.configure(state="disabled")
            txt_box.pack(fill="x", padx=10, pady=(0, 8))

        # Checkbox for confirmation in the footer (guaranteed visible and pre-checked)
        confirm_var = tk.BooleanVar(value=True)
        chk = ctk.CTkCheckBox(
            modal.footer_frame,
            text="✓ I confirm recipient consent & compliance",
            variable=confirm_var,
            font=theme.FONT_BODY_SM,
            fg_color=theme.COLOR_PRIMARY,
            text_color=theme.COLOR_TEXT,
        )
        chk.pack(side="left", padx=16, pady=10)

        def on_confirm_proceed():
            # Clicking 'Confirm & Launch' represents explicit user confirmation
            confirm_var.set(True)

            try:
                # Create campaign and queue in database with all variants
                camp_id, _ = self.campaign_service.create_campaign(
                    campaign_name=camp_name,
                    template_text=active_variants[0],
                    variants=active_variants,
                    template_id=None,
                    student_ids=student_ids,
                )
                # Record confirmation timestamp
                confirmed_at = self.campaign_service.confirm_and_queue_campaign(camp_id)
                modal.destroy()

                # Switch to monitor tab and start background execution
                self._current_campaign_id = camp_id
                self.monitor_camp_name.configure(
                    text=f"Campaign #{camp_id}: {camp_name} ({v_count} SMS types rotating • Confirmed: {confirmed_at[:19]})"
                )
                self.tabview.set("2. Dispatch Monitor")
                self._start_execution(camp_id)

            except Exception as exc:
                logger.error(f"Error creating campaign: {exc}", exc_info=True)
                messagebox.showerror("Campaign Error", str(exc))

        modal.add_button("Cancel", command=modal.destroy, side="right")
        modal.add_button("✓ Confirm & Launch", command=on_confirm_proceed, is_primary=True, side="right")

    # -------------------------------------------------------------
    # Live Execution Monitor
    # -------------------------------------------------------------
    def _start_execution(self, campaign_id: int):
        """Starts background worker and connects progress updates."""
        self._is_paused = False
        self.btn_pause.configure(text="⏸ Pause")

        # Load initial queue
        recipients = self.campaigns_repo.get_recipients(campaign_id)
        self.queue_table.set_data(recipients)

        def progress_callback(curr, total, data):
            def update_ui():
                self.monitor_progress.set(curr / max(total, 1))
                # Refresh queue table
                updated_recs = self.campaigns_repo.get_recipients(campaign_id)
                self.queue_table.set_data(updated_recs)
            self.after(0, update_ui)

        def completed_callback(summary):
            def on_complete():
                self.monitor_progress.set(1.0)
                updated_recs = self.campaigns_repo.get_recipients(campaign_id)
                self.queue_table.set_data(updated_recs)
                messagebox.showinfo(
                    "Campaign Completed",
                    f"Campaign #{summary['campaign_id']} finished with status: {summary['status']}\n\n"
                    f"Total: {summary['total']}\n"
                    f"Successful (Verified Sent): {summary['successful']}\n"
                    f"Failed: {summary['failed']}\n"
                    f"Skipped: {summary['skipped']}",
                )
            self.after(0, on_complete)

        self.campaign_service.start_campaign_execution(
            campaign_id,
            on_progress=progress_callback,
            on_completed=completed_callback,
        )

    def _toggle_pause(self):
        if not self._current_campaign_id:
            return
        if not self._is_paused:
            self.campaign_service.pause_execution()
            self._is_paused = True
            self.btn_pause.configure(text="▶ Resume")
        else:
            self.campaign_service.resume_execution()
            self._is_paused = False
            self.btn_pause.configure(text="⏸ Pause")

    def _cancel_active_campaign(self):
        if not self._current_campaign_id:
            return
        confirm = messagebox.askyesno("Cancel Campaign", "Are you sure you want to cancel this campaign? Dispatched messages cannot be undone.")
        if confirm:
            self.campaign_service.cancel_execution(self._current_campaign_id)
            self.btn_pause.configure(state="disabled")
            self.btn_cancel.configure(state="disabled")
