"""Student registry page with search, filters, import wizard modal, and exports."""
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import threading
from typing import Dict, Any, List, Optional
from pathlib import Path

from app.ui import theme
from app.ui.components.table_view import TableView
from app.ui.components.modal_dialog import ModalDialog
from app.database.repository import StudentsRepository, ImportsRepository
from app.services.import_service import ImportService
from app.services.report_service import ReportService
from app.utils.logger import logger

class StudentsPage(ctk.CTkFrame):
    """Students management view with search, filter, and import wizard."""

    def __init__(
        self,
        master,
        students_repo: StudentsRepository,
        imports_repo: ImportsRepository,
        default_region: str = "BD",
        **kwargs,
    ):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.students_repo = students_repo
        self.imports_repo = imports_repo
        self.default_region = default_region
        self.import_service = ImportService(students_repo, imports_repo, default_region)
        self.report_service = ReportService(students_repo, None)

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
            text="Student Registry",
            font=theme.FONT_HEADLINE_XL,
            text_color=theme.COLOR_TEXT,
            anchor="w",
        )
        title.grid(row=0, column=0, sticky="w")

        subtitle = ctk.CTkLabel(
            header,
            text="Central repository of student contacts, normalized E.164 formats, and consent status",
            font=theme.FONT_BODY_MD,
            text_color=theme.COLOR_TEXT_MUTED,
            anchor="w",
        )
        subtitle.grid(row=1, column=0, sticky="w")

        # Top Action Buttons
        btn_frame = ctk.CTkFrame(header, fg_color="transparent")
        btn_frame.grid(row=0, column=1, rowspan=2, sticky="e")

        btn_add = ctk.CTkButton(
            btn_frame,
            text="➕ Add Student",
            font=theme.FONT_HEADLINE_SM,
            fg_color=theme.COLOR_PRIMARY,
            hover_color=theme.COLOR_PRIMARY_HOVER,
            text_color="#0F1115",
            height=36,
            corner_radius=6,
            command=self._open_add_student_modal,
        )
        btn_add.pack(side="left", padx=6)

        btn_import = ctk.CTkButton(
            btn_frame,
            text="📥 Import File",
            font=theme.FONT_HEADLINE_SM,
            fg_color=theme.COLOR_CARD,
            hover_color=theme.COLOR_CARD_HOVER,
            text_color=theme.COLOR_TEXT,
            border_width=1,
            border_color=theme.COLOR_BORDER,
            height=36,
            corner_radius=6,
            command=self._open_import_wizard,
        )
        btn_import.pack(side="left", padx=6)

        btn_export = ctk.CTkButton(
            btn_frame,
            text="📤 Export CSV",
            font=theme.FONT_HEADLINE_SM,
            fg_color=theme.COLOR_CARD,
            hover_color=theme.COLOR_CARD_HOVER,
            text_color=theme.COLOR_TEXT,
            border_width=1,
            border_color=theme.COLOR_BORDER,
            height=36,
            corner_radius=6,
            command=self._export_students_csv,
        )
        btn_export.pack(side="left", padx=6)

        # Filters Bar
        filter_bar = ctk.CTkFrame(
            self,
            fg_color=theme.COLOR_CARD,
            border_width=1,
            border_color=theme.COLOR_BORDER,
            corner_radius=8,
            height=54,
        )
        filter_bar.grid(row=1, column=0, padx=24, pady=(0, 12), sticky="ew")

        # Search Input
        self.search_var = tk.StringVar()
        self.search_entry = ctk.CTkEntry(
            filter_bar,
            placeholder_text="🔍 Search by name, phone, email...",
            textvariable=self.search_var,
            width=280,
            height=34,
            corner_radius=6,
            fg_color=theme.COLOR_SIDEBAR,
            border_color=theme.COLOR_BORDER,
            text_color=theme.COLOR_TEXT,
        )
        self.search_entry.pack(side="left", padx=(12, 10), pady=10)
        self.search_entry.bind("<Return>", lambda e: self.refresh())

        # Batch Filter Dropdown
        self.batch_var = tk.StringVar(value="All Batches")
        self.batch_menu = ctk.CTkOptionMenu(
            filter_bar,
            variable=self.batch_var,
            values=["All Batches"],
            height=34,
            corner_radius=6,
            fg_color=theme.COLOR_SIDEBAR,
            button_color=theme.COLOR_CARD_HOVER,
            text_color=theme.COLOR_TEXT,
            command=lambda v: self.refresh(),
        )
        self.batch_menu.pack(side="left", padx=6, pady=10)

        # Consent Filter Dropdown
        self.consent_var = tk.StringVar(value="All Consent")
        self.consent_menu = ctk.CTkOptionMenu(
            filter_bar,
            variable=self.consent_var,
            values=["All Consent", "granted", "unknown", "opted_out"],
            height=34,
            corner_radius=6,
            fg_color=theme.COLOR_SIDEBAR,
            button_color=theme.COLOR_CARD_HOVER,
            text_color=theme.COLOR_TEXT,
            command=lambda v: self.refresh(),
        )
        self.consent_menu.pack(side="left", padx=6, pady=10)

        # Validity Filter Dropdown
        self.valid_var = tk.StringVar(value="All Validity")
        self.valid_menu = ctk.CTkOptionMenu(
            filter_bar,
            variable=self.valid_var,
            values=["All Validity", "Valid Only", "Invalid / Flagged Only"],
            height=34,
            corner_radius=6,
            fg_color=theme.COLOR_SIDEBAR,
            button_color=theme.COLOR_CARD_HOVER,
            text_color=theme.COLOR_TEXT,
            command=lambda v: self.refresh(),
        )
        self.valid_menu.pack(side="left", padx=6, pady=10)

        # Search / Reset buttons
        btn_filter = ctk.CTkButton(
            filter_bar,
            text="Filter",
            font=theme.FONT_HEADLINE_SM,
            fg_color=theme.COLOR_SIDEBAR,
            hover_color=theme.COLOR_CARD_HOVER,
            text_color=theme.COLOR_PRIMARY,
            border_width=1,
            border_color=theme.COLOR_PRIMARY,
            width=70,
            height=34,
            corner_radius=6,
            command=self.refresh,
        )
        btn_filter.pack(side="left", padx=6, pady=10)

        btn_reset = ctk.CTkButton(
            filter_bar,
            text="Reset",
            font=theme.FONT_BODY_SM,
            fg_color="transparent",
            hover_color=theme.COLOR_CARD_HOVER,
            text_color=theme.COLOR_TEXT_MUTED,
            width=60,
            height=34,
            corner_radius=6,
            command=self._reset_filters,
        )
        btn_reset.pack(side="left", padx=4, pady=10)

        # Records Table
        table_frame = ctk.CTkFrame(self, fg_color="transparent")
        table_frame.grid(row=2, column=0, padx=24, pady=(0, 20), sticky="nsew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        cols = [
            ("id", "ID", 50),
            ("name", "Student Name", 160),
            ("phone", "Normalized E.164", 140),
            ("raw_phone", "Raw Input", 120),
            ("batch", "Batch", 90),
            ("email", "Email", 160),
            ("consent_status", "Consent", 90),
            ("format_display", "Format Status", 110),
            ("whatsapp_status", "WhatsApp", 90),
        ]
        self.table = TableView(table_frame, columns=cols, multi_select=True)
        self.table.grid(row=0, column=0, sticky="nsew")

    def _reset_filters(self):
        self.search_var.set("")
        self.batch_var.set("All Batches")
        self.consent_var.set("All Consent")
        self.valid_var.set("All Validity")
        self.refresh()

    def refresh(self):
        """Fetches and displays students matching active filter criteria."""
        search = self.search_var.get().strip()
        batch = "" if self.batch_var.get() == "All Batches" else self.batch_var.get()
        consent = "" if self.consent_var.get() == "All Consent" else self.consent_var.get()

        valid_filter = self.valid_var.get()
        is_valid_param = None
        if valid_filter == "Valid Only":
            is_valid_param = 1
        elif valid_filter == "Invalid / Flagged Only":
            is_valid_param = 0

        students = self.students_repo.get_all(
            search=search,
            batch=batch,
            consent_status=consent,
            is_valid=is_valid_param,
            limit=500,
        )

        # Format display fields
        display_records = []
        for s in students:
            rec = dict(s)
            is_v = rec.get("is_valid", 1)
            is_dup = rec.get("is_duplicate", 0)
            if not is_v:
                rec["format_display"] = "⚠️ Malformed"
            elif is_dup:
                rec["format_display"] = "⚠️ Duplicate"
            else:
                rec["format_display"] = "✓ Valid"

            # Requirement: Never claim number is on WhatsApp; stays "Unknown" unless verified
            rec["whatsapp_status"] = rec.get("whatsapp_status", "unknown").capitalize()
            display_records.append(rec)

        self.table.set_data(display_records)

        # Refresh batch dropdown items
        batches = self.students_repo.get_batches()
        menu_items = ["All Batches"] + batches
        self.batch_menu.configure(values=menu_items)

    def _export_students_csv(self):
        """Exports currently filtered student view to CSV."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")],
            title="Export Students Registry",
        )
        if not file_path:
            return

        fmt = "xlsx" if file_path.lower().endswith(".xlsx") else "csv"
        try:
            saved_path = self.report_service.export_students(
                output_path=file_path,
                export_format=fmt,
                search=self.search_var.get().strip(),
                batch="" if self.batch_var.get() == "All Batches" else self.batch_var.get(),
                consent_status="" if self.consent_var.get() == "All Consent" else self.consent_var.get(),
            )
            messagebox.showinfo("Export Successful", f"Students exported successfully to:\n{saved_path}")
        except Exception as exc:
            logger.error(f"Failed exporting students: {exc}", exc_info=True)
            messagebox.showerror("Export Failed", str(exc))

    def _open_import_wizard(self):
        """Opens the modal import dialog with file selection, mapping, and duplicate options."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Spreadsheet files", "*.xlsx;*.xls;*.csv"), ("All Files", "*.*")],
            title="Select Student Spreadsheet",
        )
        if not file_path:
            return

        modal = ModalDialog(self.winfo_toplevel(), title="📥 Student Import & Normalization Wizard", width=680, height=580)
        body = modal.body_frame

        # File summary
        fname = Path(file_path).name
        file_info = ctk.CTkLabel(
            body,
            text=f"Selected File: {fname}",
            font=theme.FONT_HEADLINE_SM,
            text_color=theme.COLOR_PRIMARY,
            anchor="w",
        )
        file_info.pack(fill="x", pady=(0, 10))

        # Inspect headers
        try:
            columns = self.import_service.get_file_columns(file_path)
            auto_map = self.import_service.auto_detect_mapping(columns)
        except Exception as exc:
            messagebox.showerror("Read Error", f"Unable to read file: {exc}")
            modal.destroy()
            return

        mapping_box = ctk.CTkFrame(body, fg_color=theme.COLOR_CARD, border_width=1, border_color=theme.COLOR_BORDER, corner_radius=6)
        mapping_box.pack(fill="x", pady=6, padx=2)

        ctk.CTkLabel(mapping_box, text="COLUMN MAPPING", font=theme.FONT_HEADLINE_SM, text_color=theme.COLOR_TEXT_MUTED).grid(row=0, column=0, columnspan=2, padx=12, pady=(10, 6), sticky="w")

        fields = [
            ("name", "Student Name *", auto_map.get("name")),
            ("phone", "Phone Number *", auto_map.get("phone")),
            ("email", "Email Address", auto_map.get("email")),
            ("batch", "Batch / Class", auto_map.get("batch")),
            ("consent_status", "Consent Status", auto_map.get("consent_status")),
        ]

        dropdowns: Dict[str, ctk.CTkOptionMenu] = {}
        col_choices = ["(None)"] + columns

        for idx, (f_key, f_label, default_val) in enumerate(fields, start=1):
            lbl = ctk.CTkLabel(mapping_box, text=f_label, font=theme.FONT_BODY_MD, text_color=theme.COLOR_TEXT)
            lbl.grid(row=idx, column=0, padx=16, pady=4, sticky="w")

            initial = default_val if default_val in columns else "(None)"
            opt = ctk.CTkOptionMenu(
                mapping_box,
                values=col_choices,
                width=240,
                height=28,
                fg_color=theme.COLOR_SIDEBAR,
                button_color=theme.COLOR_CARD_HOVER,
            )
            opt.set(initial)
            opt.grid(row=idx, column=1, padx=16, pady=4, sticky="e")
            dropdowns[f_key] = opt

        # Duplicate Rule Selection
        dup_frame = ctk.CTkFrame(body, fg_color=theme.COLOR_CARD, border_width=1, border_color=theme.COLOR_BORDER, corner_radius=6)
        dup_frame.pack(fill="x", pady=10, padx=2)

        ctk.CTkLabel(
            dup_frame,
            text="DUPLICATE PHONE RESOLUTION",
            font=theme.FONT_HEADLINE_SM,
            text_color=theme.COLOR_TEXT_MUTED,
        ).pack(anchor="w", padx=12, pady=(10, 4))

        dup_choice_var = tk.StringVar(value="skip")
        ctk.CTkRadioButton(
            dup_frame,
            text="Skip incoming duplicate records",
            variable=dup_choice_var,
            value="skip",
            fg_color=theme.COLOR_PRIMARY,
            text_color=theme.COLOR_TEXT,
        ).pack(anchor="w", padx=16, pady=2)

        ctk.CTkRadioButton(
            dup_frame,
            text="Update existing record with new details",
            variable=dup_choice_var,
            value="update",
            fg_color=theme.COLOR_PRIMARY,
            text_color=theme.COLOR_TEXT,
        ).pack(anchor="w", padx=16, pady=2)

        ctk.CTkRadioButton(
            dup_frame,
            text="Keep both and flag as duplicate",
            variable=dup_choice_var,
            value="keep_both_flagged",
            fg_color=theme.COLOR_PRIMARY,
            text_color=theme.COLOR_TEXT,
        ).pack(anchor="w", padx=16, pady=(2, 10))

        # Progress / Status
        progress_bar = ctk.CTkProgressBar(body, fg_color=theme.COLOR_SIDEBAR, progress_color=theme.COLOR_PRIMARY)
        progress_bar.set(0)
        progress_bar.pack(fill="x", pady=(10, 4), padx=2)

        status_lbl = ctk.CTkLabel(body, text="Ready to import.", font=theme.FONT_BODY_SM, text_color=theme.COLOR_TEXT_MUTED)
        status_lbl.pack(anchor="w", padx=4)

        cancel_btn = modal.add_button("Cancel", command=lambda: self._cancel_import_wizard(modal), side="right")

        def run_import():
            # Build mapping
            mapping = {}
            for k, dd in dropdowns.items():
                val = dd.get()
                mapping[k] = val if val != "(None)" else None

            if not mapping.get("name") or not mapping.get("phone"):
                messagebox.showerror("Mapping Required", "Please map both Student Name and Phone Number.")
                return

            import_btn.configure(state="disabled")
            status_lbl.configure(text="Processing file in background...")

            def progress_hook(curr, total, msg):
                def update_ui():
                    progress_bar.set(curr / max(total, 1))
                    status_lbl.configure(text=f"{msg} ({curr}/{total})")
                self.after(0, update_ui)

            def worker():
                try:
                    res = self.import_service.execute_import(
                        file_path=file_path,
                        column_mapping=mapping,
                        duplicate_mode=dup_choice_var.get(),
                        on_progress=progress_hook,
                    )
                    def on_done():
                        self.refresh()
                        modal.destroy()
                        messagebox.showinfo(
                            "Import Finished",
                            f"Import completed successfully!\n\n"
                            f"Total Rows: {res['total_rows']}\n"
                            f"Valid Records: {res['valid_rows']}\n"
                            f"Flagged Malformed: {res['invalid_rows']}\n"
                            f"Duplicates Handled: {res['duplicate_rows']}\n"
                            f"Saved: {res['imported_count']}",
                        )
                    self.after(0, on_done)
                except Exception as exc:
                    logger.error(f"Import worker error: {exc}", exc_info=True)
                    def on_err():
                        status_lbl.configure(text=f"Error: {exc}")
                        import_btn.configure(state="normal")
                        messagebox.showerror("Import Error", str(exc))
                    self.after(0, on_err)

            t = threading.Thread(target=worker, daemon=True)
            t.start()

        import_btn = modal.add_button("Start Import", command=run_import, is_primary=True, side="right")

    def _cancel_import_wizard(self, modal):
        self.import_service.cancel()
        modal.destroy()

    def _open_add_student_modal(self):
        """Opens a modal dialog to manually add a new student record."""
        modal = ModalDialog(self.winfo_toplevel(), title="➕ Add New Student", width=580, height=520)
        body = modal.body_frame

        ctk.CTkLabel(
            body,
            text="MANUAL STUDENT ENTRY",
            font=theme.FONT_HEADLINE_SM,
            text_color=theme.COLOR_PRIMARY,
            anchor="w",
        ).pack(fill="x", pady=(0, 12))

        form_frame = ctk.CTkFrame(body, fg_color=theme.COLOR_CARD, border_width=1, border_color=theme.COLOR_BORDER, corner_radius=6)
        form_frame.pack(fill="x", padx=2, pady=(0, 10))
        form_frame.grid_columnconfigure(1, weight=1)

        # 1. Full Name
        ctk.CTkLabel(form_frame, text="Full Name *:", font=theme.FONT_BODY_MD, text_color=theme.COLOR_TEXT).grid(row=0, column=0, padx=16, pady=(14, 6), sticky="w")
        name_entry = ctk.CTkEntry(form_frame, placeholder_text="e.g. Tariq Ahmed", height=34, fg_color=theme.COLOR_SIDEBAR, border_color=theme.COLOR_BORDER)
        name_entry.grid(row=0, column=1, padx=16, pady=(14, 6), sticky="ew")

        # 2. Phone Number
        ctk.CTkLabel(form_frame, text="Phone Number *:", font=theme.FONT_BODY_MD, text_color=theme.COLOR_TEXT).grid(row=1, column=0, padx=16, pady=6, sticky="w")
        phone_entry = ctk.CTkEntry(form_frame, placeholder_text="e.g. 01712345678 or +8801712345678", height=34, fg_color=theme.COLOR_SIDEBAR, border_color=theme.COLOR_BORDER)
        phone_entry.grid(row=1, column=1, padx=16, pady=6, sticky="ew")

        # Live Phone Preview
        phone_preview_lbl = ctk.CTkLabel(
            form_frame,
            text=f"Default region: {self.default_region} (will normalize to E.164)",
            font=theme.FONT_BODY_SM,
            text_color=theme.COLOR_TEXT_MUTED,
            anchor="w",
        )
        phone_preview_lbl.grid(row=2, column=1, padx=16, pady=(0, 6), sticky="w")

        def on_phone_typed(event=None):
            val = phone_entry.get().strip()
            if not val:
                phone_preview_lbl.configure(
                    text=f"Default region: {self.default_region} (will normalize to E.164)",
                    text_color=theme.COLOR_TEXT_MUTED,
                )
                return

            validated = self.import_service.validation_service.validate_student_record(
                {"name": "test", "phone": val}
            )
            if validated["is_valid"]:
                phone_preview_lbl.configure(
                    text=f"✓ Normalized E.164: {validated['phone']}",
                    text_color=theme.COLOR_SUCCESS,
                )
            else:
                phone_preview_lbl.configure(
                    text=f"⚠️ {validated['validation_error'] or 'Invalid format for region'}",
                    text_color=theme.COLOR_WARNING,
                )

        phone_entry.bind("<KeyRelease>", on_phone_typed)

        # 3. Email Address
        ctk.CTkLabel(form_frame, text="Email Address:", font=theme.FONT_BODY_MD, text_color=theme.COLOR_TEXT).grid(row=3, column=0, padx=16, pady=6, sticky="w")
        email_entry = ctk.CTkEntry(form_frame, placeholder_text="e.g. tariq@example.com (optional)", height=34, fg_color=theme.COLOR_SIDEBAR, border_color=theme.COLOR_BORDER)
        email_entry.grid(row=3, column=1, padx=16, pady=6, sticky="ew")

        # 4. Batch / Class
        ctk.CTkLabel(form_frame, text="Batch / Class:", font=theme.FONT_BODY_MD, text_color=theme.COLOR_TEXT).grid(row=4, column=0, padx=16, pady=6, sticky="w")
        batch_entry = ctk.CTkEntry(form_frame, placeholder_text="e.g. Batch-2026 (optional)", height=34, fg_color=theme.COLOR_SIDEBAR, border_color=theme.COLOR_BORDER)
        batch_entry.grid(row=4, column=1, padx=16, pady=6, sticky="ew")

        # 5. Consent Status
        ctk.CTkLabel(form_frame, text="Consent Status:", font=theme.FONT_BODY_MD, text_color=theme.COLOR_TEXT).grid(row=5, column=0, padx=16, pady=(6, 14), sticky="w")
        consent_var = tk.StringVar(value="granted")
        consent_menu = ctk.CTkOptionMenu(
            form_frame,
            variable=consent_var,
            values=["granted (Opted-in)", "unknown (Unconfirmed)", "opted_out (Do Not Contact)"],
            height=34,
            fg_color=theme.COLOR_SIDEBAR,
            button_color=theme.COLOR_CARD_HOVER,
        )
        consent_menu.grid(row=5, column=1, padx=16, pady=(6, 14), sticky="ew")

        def save_manual_student():
            raw_name = name_entry.get().strip()
            raw_phone = phone_entry.get().strip()
            raw_email = email_entry.get().strip() or None
            raw_batch = batch_entry.get().strip() or None
            raw_consent = consent_var.get().split()[0].strip().lower()

            if not raw_name:
                messagebox.showerror("Validation Error", "Student Name is required.")
                name_entry.focus_set()
                return

            if not raw_phone:
                messagebox.showerror("Validation Error", "Phone Number is required.")
                phone_entry.focus_set()
                return

            # Normalize and validate through validation_service
            validated = self.import_service.validation_service.validate_student_record({
                "name": raw_name,
                "phone": raw_phone,
                "email": raw_email,
                "batch": raw_batch,
                "consent_status": raw_consent,
            })

            norm_phone = validated["phone"]

            # Check for existing duplicate phone in database
            existing = self.students_repo.find_by_phone(norm_phone)
            if existing:
                choice = messagebox.askyesnocancel(
                    "Duplicate Phone Detected",
                    f"A student with phone number '{norm_phone}' already exists:\n\n"
                    f"Name: {existing['name']}\n"
                    f"Batch: {existing.get('batch') or 'N/A'}\n\n"
                    f"• Click 'Yes' to UPDATE the existing student with new details.\n"
                    f"• Click 'No' to KEEP BOTH and flag this record as a duplicate.\n"
                    f"• Click 'Cancel' to abort.",
                )
                if choice is None:
                    return  # Cancel
                elif choice is True:
                    # Update existing record
                    self.students_repo.update_student(
                        student_id=existing["id"],
                        name=validated["name"],
                        email=validated["email"],
                        batch=validated["batch"],
                        consent_status=validated["consent_status"],
                        is_valid=validated["is_valid"],
                        validation_error=validated["validation_error"],
                    )
                    logger.info(f"Updated existing student id={existing['id']} with manual input.")
                    modal.destroy()
                    self.refresh()
                    messagebox.showinfo("Student Updated", f"Successfully updated record for '{validated['name']}'.")
                    return
                else:
                    # Keep both, flag as duplicate
                    validated["is_duplicate"] = 1

            # Insert new student record
            new_id = self.students_repo.add_student(
                name=validated["name"],
                phone=validated["phone"],
                raw_phone=validated["raw_phone"],
                email=validated["email"],
                batch=validated["batch"],
                whatsapp_status=validated["whatsapp_status"],
                consent_status=validated["consent_status"],
                is_valid=validated["is_valid"],
                validation_error=validated["validation_error"],
                is_duplicate=validated["is_duplicate"],
            )

            logger.info(f"Manually added student id={new_id} ({validated['name']}, {validated['phone']}).")
            modal.destroy()
            self.refresh()

            status_note = "Valid" if validated["is_valid"] else f"Flagged ({validated['validation_error']})"
            messagebox.showinfo(
                "Student Added",
                f"Student record saved successfully!\n\n"
                f"ID: #{new_id}\n"
                f"Name: {validated['name']}\n"
                f"Phone: {validated['phone']}\n"
                f"Status: {status_note}\n"
                f"Consent: {validated['consent_status']}",
            )

        modal.add_button("Cancel", command=modal.destroy, side="right")
        modal.add_button("Save Student", command=save_manual_student, is_primary=True, side="right")

