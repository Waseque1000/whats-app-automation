"""Message templates management view with variable substitution and live preview."""
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from typing import Dict, Any, List, Optional

from app.ui import theme
from app.database.repository import TemplatesRepository, StudentsRepository
from app.services.template_service import TemplateService, SUPPORTED_VARIABLES
from app.utils.logger import logger

class TemplatesPage(ctk.CTkFrame):
    """Template manager view with syntax validation and live personalized preview."""

    def __init__(
        self,
        master,
        templates_repo: TemplatesRepository,
        students_repo: StudentsRepository,
        **kwargs,
    ):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.templates_repo = templates_repo
        self.students_repo = students_repo
        self._current_template_id: Optional[int] = None
        self._templates: List[Dict[str, Any]] = []

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._setup_ui()
        self.refresh()

    def _setup_ui(self):
        # Header banner
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, padx=24, pady=(20, 12), sticky="ew")

        title = ctk.CTkLabel(
            header,
            text="Message Templates",
            font=theme.FONT_HEADLINE_XL,
            text_color=theme.COLOR_TEXT,
            anchor="w",
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            header,
            text="Compose reusable broadcast templates with dynamic placeholders and live validation",
            font=theme.FONT_BODY_MD,
            text_color=theme.COLOR_TEXT_MUTED,
            anchor="w",
        )
        subtitle.pack(anchor="w")

        # Left Column: Saved Templates List
        left_panel = ctk.CTkFrame(
            self,
            fg_color=theme.COLOR_CARD,
            border_width=1,
            border_color=theme.COLOR_BORDER,
            corner_radius=8,
            width=280,
        )
        left_panel.grid(row=1, column=0, padx=(24, 12), pady=(0, 20), sticky="nsew")
        left_panel.grid_rowconfigure(2, weight=1)
        left_panel.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            left_panel,
            text="SAVED TEMPLATES",
            font=theme.FONT_HEADLINE_SM,
            text_color=theme.COLOR_TEXT_MUTED,
        ).grid(row=0, column=0, padx=16, pady=(16, 8), sticky="w")

        btn_new = ctk.CTkButton(
            left_panel,
            text="+ New Template",
            font=theme.FONT_HEADLINE_SM,
            fg_color=theme.COLOR_PRIMARY,
            hover_color=theme.COLOR_PRIMARY_HOVER,
            text_color="#0F1115",
            height=32,
            corner_radius=6,
            command=self._new_template,
        )
        btn_new.grid(row=1, column=0, padx=16, pady=(0, 10), sticky="ew")

        self.template_listbox = tk.Listbox(
            left_panel,
            background=theme.COLOR_SIDEBAR,
            foreground=theme.COLOR_TEXT,
            selectbackground=theme.COLOR_CARD_HOVER,
            selectforeground=theme.COLOR_PRIMARY,
            borderwidth=0,
            highlightthickness=0,
            font=theme.FONT_BODY_MD,
        )
        self.template_listbox.grid(row=2, column=0, padx=16, pady=(0, 16), sticky="nsew")
        self.template_listbox.bind("<<ListboxSelect>>", self._on_template_selected)

        # Right Column: Editor and Live Preview
        right_panel = ctk.CTkFrame(
            self,
            fg_color=theme.COLOR_CARD,
            border_width=1,
            border_color=theme.COLOR_BORDER,
            corner_radius=8,
        )
        right_panel.grid(row=1, column=1, padx=(0, 24), pady=(0, 20), sticky="nsew")
        right_panel.grid_rowconfigure(3, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)

        # Name entry
        name_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        name_frame.grid(row=0, column=0, padx=20, pady=(16, 8), sticky="ew")
        name_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(name_frame, text="Template Name:", font=theme.FONT_HEADLINE_SM, text_color=theme.COLOR_TEXT).grid(row=0, column=0, padx=(0, 10), sticky="w")
        self.name_entry = ctk.CTkEntry(
            name_frame,
            placeholder_text="e.g., Exam Schedule Announcement",
            height=34,
            corner_radius=6,
            fg_color=theme.COLOR_SIDEBAR,
            border_color=theme.COLOR_BORDER,
            text_color=theme.COLOR_TEXT,
        )
        self.name_entry.grid(row=0, column=1, sticky="ew")

        # Variables Chip Toolbar
        chips_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        chips_frame.grid(row=1, column=0, padx=20, pady=(0, 8), sticky="ew")

        ctk.CTkLabel(chips_frame, text="Insert Variable:", font=theme.FONT_BODY_SM, text_color=theme.COLOR_TEXT_MUTED).pack(side="left", padx=(0, 8))
        for var in sorted(list(SUPPORTED_VARIABLES)):
            tag = f"{{{{{var}}}}}"
            btn_var = ctk.CTkButton(
                chips_frame,
                text=tag,
                font=theme.FONT_CODE_SM,
                fg_color=theme.COLOR_SIDEBAR,
                hover_color=theme.COLOR_CARD_HOVER,
                text_color=theme.COLOR_PRIMARY,
                border_width=1,
                border_color=theme.COLOR_BORDER,
                height=26,
                corner_radius=4,
                command=lambda v=tag: self._insert_variable(v),
            )
            btn_var.pack(side="left", padx=4)

        # Editor Area + Live Preview in two split panes
        split_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        split_frame.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="nsew")
        split_frame.grid_columnconfigure(0, weight=1)
        split_frame.grid_columnconfigure(1, weight=1)
        split_frame.grid_rowconfigure(1, weight=1)

        # Left side: Editor text box
        ctk.CTkLabel(split_frame, text="CONTENT EDITOR", font=theme.FONT_HEADLINE_SM, text_color=theme.COLOR_TEXT_MUTED).grid(row=0, column=0, sticky="w", pady=(0, 4))
        self.editor_text = ctk.CTkTextbox(
            split_frame,
            fg_color=theme.COLOR_SIDEBAR,
            border_width=1,
            border_color=theme.COLOR_BORDER,
            corner_radius=6,
            text_color=theme.COLOR_TEXT,
            font=theme.FONT_BODY_MD,
            wrap="word",
        )
        self.editor_text.grid(row=1, column=0, padx=(0, 8), sticky="nsew")
        self.editor_text.bind("<KeyRelease>", lambda e: self._on_text_changed())

        # Right side: Live Preview box
        ctk.CTkLabel(split_frame, text="PERSONALIZED LIVE PREVIEW", font=theme.FONT_HEADLINE_SM, text_color=theme.COLOR_TEXT_MUTED).grid(row=0, column=1, sticky="w", pady=(0, 4))
        self.preview_box = ctk.CTkTextbox(
            split_frame,
            fg_color="#10141D",
            border_width=1,
            border_color=theme.COLOR_BORDER,
            corner_radius=6,
            text_color="#E2E8F0",
            font=theme.FONT_BODY_MD,
            wrap="word",
        )
        self.preview_box.grid(row=1, column=1, padx=(8, 0), sticky="nsew")
        self.preview_box.configure(state="disabled")

        # Validation status message bar
        self.val_label = ctk.CTkLabel(
            right_panel,
            text="✓ All placeholders recognized.",
            font=theme.FONT_BODY_SM,
            text_color=theme.COLOR_SUCCESS,
            anchor="w",
        )
        self.val_label.grid(row=3, column=0, padx=20, pady=(0, 8), sticky="w")

        # Bottom actions
        action_bar = ctk.CTkFrame(right_panel, fg_color="transparent")
        action_bar.grid(row=4, column=0, padx=20, pady=(0, 16), sticky="ew")

        self.btn_save = ctk.CTkButton(
            action_bar,
            text="Save Template",
            font=theme.FONT_HEADLINE_SM,
            fg_color=theme.COLOR_PRIMARY,
            hover_color=theme.COLOR_PRIMARY_HOVER,
            text_color="#0F1115",
            height=36,
            corner_radius=6,
            command=self._save_template,
        )
        self.btn_save.pack(side="left", padx=(0, 8))

        self.btn_delete = ctk.CTkButton(
            action_bar,
            text="Delete",
            font=theme.FONT_HEADLINE_SM,
            fg_color=theme.COLOR_DANGER,
            hover_color="#DC2626",
            text_color="#FFFFFF",
            height=36,
            corner_radius=6,
            command=self._delete_template,
        )
        self.btn_delete.pack(side="left", padx=8)

    def _insert_variable(self, tag: str):
        self.editor_text.insert(tk.INSERT, tag)
        self._on_text_changed()

    def _on_text_changed(self):
        content = self.editor_text.get("1.0", tk.END).strip()
        is_valid, found, unknown = TemplateService.validate_template(content)

        if unknown:
            self.val_label.configure(
                text=f"⚠️ Warning: Unknown placeholder(s) detected: {', '.join(unknown)}",
                text_color=theme.COLOR_WARNING,
            )
        elif not content:
            self.val_label.configure(text="Template content is empty.", text_color=theme.COLOR_TEXT_MUTED)
        else:
            self.val_label.configure(
                text=f"✓ Valid: {len(found)} placeholder(s) active ({', '.join(found) if found else 'none'})",
                text_color=theme.COLOR_SUCCESS,
            )

        # Update preview with a real or sample student
        sample = None
        all_students = self.students_repo.get_all(limit=1)
        if all_students:
            sample = all_students[0]

        preview_msg = TemplateService.preview(content, sample)
        self.preview_box.configure(state="normal")
        self.preview_box.delete("1.0", tk.END)
        self.preview_box.insert(tk.END, preview_msg)
        self.preview_box.configure(state="disabled")

    def refresh(self):
        """Reloads template list from SQLite."""
        self._templates = self.templates_repo.get_all()
        self.template_listbox.delete(0, tk.END)
        for t in self._templates:
            self.template_listbox.insert(tk.END, f"  {t['template_name']}")

    def _new_template(self):
        self._current_template_id = None
        self.name_entry.delete(0, tk.END)
        self.editor_text.delete("1.0", tk.END)
        self.editor_text.insert("1.0", "Hello {{name}},\n\nYour class batch is {{batch}}. Please note our upcoming session.\n\nThank you!")
        self._on_text_changed()

    def _on_template_selected(self, event):
        sel = self.template_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        if 0 <= idx < len(self._templates):
            t = self._templates[idx]
            self._current_template_id = t["id"]
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, t["template_name"])
            self.editor_text.delete("1.0", tk.END)
            self.editor_text.insert("1.0", t["content"])
            self._on_text_changed()

    def _save_template(self):
        name = self.name_entry.get().strip()
        content = self.editor_text.get("1.0", tk.END).strip()

        if not name:
            messagebox.showerror("Validation Error", "Please provide a template name.")
            return

        if not content:
            messagebox.showerror("Validation Error", "Template content cannot be empty.")
            return

        is_valid, found, unknown = TemplateService.validate_template(content)
        if unknown:
            res = messagebox.askyesno(
                "Unknown Placeholders",
                f"Unknown placeholders detected: {', '.join(unknown)}.\nDo you still want to save this template?",
            )
            if not res:
                return

        vars_str = ",".join(found)

        try:
            if self._current_template_id:
                self.templates_repo.update(self._current_template_id, name, content, vars_str)
                messagebox.showinfo("Saved", f"Template '{name}' updated successfully.")
            else:
                new_id = self.templates_repo.create(name, content, vars_str)
                self._current_template_id = new_id
                messagebox.showinfo("Created", f"Template '{name}' created successfully.")

            self.refresh()
        except Exception as exc:
            logger.error(f"Failed to save template: {exc}", exc_info=True)
            messagebox.showerror("Database Error", f"Unable to save template:\n{exc}")

    def _delete_template(self):
        if not self._current_template_id:
            messagebox.showwarning("Selection Required", "Please select a template to delete.")
            return

        name = self.name_entry.get().strip()
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete template '{name}'?")
        if confirm:
            try:
                self.templates_repo.delete(self._current_template_id)
                self._new_template()
                self.refresh()
                messagebox.showinfo("Deleted", "Template deleted successfully.")
            except Exception as exc:
                logger.error(f"Failed deleting template: {exc}", exc_info=True)
                messagebox.showerror("Error", str(exc))
