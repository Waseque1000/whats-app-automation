"""Student spreadsheet import service with column mapping, duplicate resolution, and background threading."""
import threading
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable, Set
import pandas as pd

from app.utils.file_handler import read_spreadsheet, inspect_file_columns
from app.utils.logger import logger
from app.services.validation_service import ValidationService
from app.database.repository import StudentsRepository, ImportsRepository

class ImportService:
    """Orchestrates spreadsheet parsing, validation, duplicate handling, and database persistence."""

    def __init__(
        self,
        students_repo: StudentsRepository,
        imports_repo: ImportsRepository,
        default_region: str = "BD",
    ):
        self.students_repo = students_repo
        self.imports_repo = imports_repo
        self.validation_service = ValidationService(default_region)
        self._cancel_requested: bool = False

    def cancel(self) -> None:
        """Requests cancellation of an ongoing import."""
        self._cancel_requested = True

    @staticmethod
    def get_file_columns(file_path: str) -> List[str]:
        """Returns column headers of the target file."""
        return inspect_file_columns(file_path)

    @staticmethod
    def auto_detect_mapping(columns: List[str]) -> Dict[str, Optional[str]]:
        """
        Suggests mapping of required/optional fields to file columns.
        Fields: 'name', 'phone', 'email', 'batch', 'consent'
        """
        mapping: Dict[str, Optional[str]] = {
            "name": None,
            "phone": None,
            "email": None,
            "batch": None,
            "consent_status": None,
        }
        for col in columns:
            clean = col.lower().replace("_", " ").replace("-", " ").strip()
            if not mapping["name"] and any(k in clean for k in ("name", "student name", "full name", "first name")):
                mapping["name"] = col
            elif not mapping["phone"] and any(k in clean for k in ("phone", "mobile", "whatsapp", "contact", "cell", "number")):
                mapping["phone"] = col
            elif not mapping["email"] and "email" in clean:
                mapping["email"] = col
            elif not mapping["batch"] and any(k in clean for k in ("batch", "class", "grade", "section", "intake")):
                mapping["batch"] = col
            elif not mapping["consent_status"] and any(k in clean for k in ("consent", "opt", "permission", "status")):
                mapping["consent_status"] = col

        return mapping

    def preview_import(
        self,
        file_path: str,
        column_mapping: Dict[str, str],
        max_rows: int = 10,
    ) -> Dict[str, Any]:
        """
        Parses the first N rows for UI preview and error summary.
        """
        df = read_spreadsheet(file_path)
        existing_students = self.students_repo.get_all()
        existing_phones = {s["phone"] for s in existing_students if s.get("phone")}

        preview_records: List[Dict[str, Any]] = []
        errors: List[str] = []

        total_rows = len(df)
        limit = min(total_rows, max_rows)

        name_col = column_mapping.get("name")
        phone_col = column_mapping.get("phone")
        email_col = column_mapping.get("email")
        batch_col = column_mapping.get("batch")
        consent_col = column_mapping.get("consent_status")

        for idx in range(limit):
            row = df.iloc[idx]
            raw_rec = {
                "name": row[name_col] if name_col and name_col in df.columns else "",
                "phone": row[phone_col] if phone_col and phone_col in df.columns else "",
                "email": row[email_col] if email_col and email_col in df.columns else "",
                "batch": row[batch_col] if batch_col and batch_col in df.columns else "",
                "consent_status": row[consent_col] if consent_col and consent_col in df.columns else "unknown",
            }
            validated = self.validation_service.validate_student_record(raw_rec, existing_phones)
            if not validated["is_valid"]:
                errors.append(f"Row {idx+1}: {validated['validation_error']} (Phone: {validated['raw_phone']})")
            preview_records.append(validated)

        return {
            "total_rows": total_rows,
            "preview_records": preview_records,
            "sample_errors": errors,
        }

    def execute_import(
        self,
        file_path: str,
        column_mapping: Dict[str, str],
        duplicate_mode: str = "skip",  # 'skip', 'update', 'keep_both_flagged'
        on_progress: Optional[Callable[[int, int, str], None]] = None,
    ) -> Dict[str, Any]:
        """
        Executes full file import with duplicate handling and creates an audit record in 'imports'.
        Duplicate modes:
        - 'skip': ignore incoming duplicate row
        - 'update': update existing record with incoming data
        - 'keep_both_flagged': insert new record flagged as is_duplicate=1
        """
        self._cancel_requested = False
        filename = Path(file_path).name
        df = read_spreadsheet(file_path)
        total_rows = len(df)

        existing_students = self.students_repo.get_all()
        # Map normalized phone -> existing student dict
        existing_phone_map: Dict[str, Dict[str, Any]] = {
            s["phone"]: s for s in existing_students if s.get("phone")
        }

        name_col = column_mapping.get("name")
        phone_col = column_mapping.get("phone")
        email_col = column_mapping.get("email")
        batch_col = column_mapping.get("batch")
        consent_col = column_mapping.get("consent_status")

        valid_rows = 0
        invalid_rows = 0
        duplicate_rows = 0
        imported_students: List[int] = []

        logger.info(f"Starting import of {filename} ({total_rows} rows), duplicate mode: {duplicate_mode}")

        for idx in range(total_rows):
            if self._cancel_requested:
                logger.warning(f"Import of {filename} cancelled by user at row {idx+1}/{total_rows}")
                break

            row = df.iloc[idx]
            raw_rec = {
                "name": str(row[name_col]).strip() if name_col and name_col in df.columns else "",
                "phone": str(row[phone_col]).strip() if phone_col and phone_col in df.columns else "",
                "email": str(row[email_col]).strip() if email_col and email_col in df.columns else "",
                "batch": str(row[batch_col]).strip() if batch_col and batch_col in df.columns else "",
                "consent_status": str(row[consent_col]).strip() if consent_col and consent_col in df.columns else "unknown",
            }

            validated = self.validation_service.validate_student_record(
                raw_rec, set(existing_phone_map.keys())
            )

            is_valid = validated["is_valid"]
            if is_valid:
                valid_rows += 1
            else:
                invalid_rows += 1

            norm_phone = validated["phone"]
            is_dup = norm_phone in existing_phone_map

            if is_dup:
                duplicate_rows += 1
                if duplicate_mode == "skip":
                    logger.debug(f"Row {idx+1}: Skipping duplicate phone {norm_phone}")
                elif duplicate_mode == "update":
                    existing = existing_phone_map[norm_phone]
                    self.students_repo.update_student(
                        student_id=existing["id"],
                        name=validated["name"],
                        email=validated["email"],
                        batch=validated["batch"],
                        consent_status=validated["consent_status"],
                        is_valid=validated["is_valid"],
                        validation_error=validated["validation_error"],
                    )
                    imported_students.append(existing["id"])
                elif duplicate_mode == "keep_both_flagged":
                    new_id = self.students_repo.add_student(
                        name=validated["name"],
                        phone=validated["phone"],
                        raw_phone=validated["raw_phone"],
                        email=validated["email"],
                        batch=validated["batch"],
                        consent_status=validated["consent_status"],
                        is_valid=validated["is_valid"],
                        validation_error=validated["validation_error"],
                        is_duplicate=1,
                    )
                    imported_students.append(new_id)
            else:
                # Fresh record
                new_id = self.students_repo.add_student(
                    name=validated["name"],
                    phone=validated["phone"],
                    raw_phone=validated["raw_phone"],
                    email=validated["email"],
                    batch=validated["batch"],
                    consent_status=validated["consent_status"],
                    is_valid=validated["is_valid"],
                    validation_error=validated["validation_error"],
                    is_duplicate=0,
                )
                imported_students.append(new_id)
                existing_phone_map[norm_phone] = validated

            if on_progress and (idx % 10 == 0 or idx == total_rows - 1):
                on_progress(idx + 1, total_rows, f"Importing row {idx+1} of {total_rows}...")

        # Record into imports audit table
        import_id = self.imports_repo.add_import(
            filename=filename,
            total_rows=total_rows,
            valid_rows=valid_rows,
            invalid_rows=invalid_rows,
            duplicate_rows=duplicate_rows,
        )

        logger.info(
            f"Completed import {import_id} ({filename}): total={total_rows}, "
            f"valid={valid_rows}, invalid={invalid_rows}, duplicates={duplicate_rows}"
        )

        return {
            "import_id": import_id,
            "filename": filename,
            "total_rows": total_rows,
            "valid_rows": valid_rows,
            "invalid_rows": invalid_rows,
            "duplicate_rows": duplicate_rows,
            "imported_count": len(imported_students),
            "cancelled": self._cancel_requested,
        }
