"""Tests for spreadsheet file ingestion, column mapping, bad rows, and duplicate modes."""
import pytest
import tempfile
from pathlib import Path
import pandas as pd

from app.services.import_service import ImportService
from app.database.repository import StudentsRepository, ImportsRepository

def test_import_csv_with_leading_zeros_and_mapping(
    import_service: ImportService,
    students_repo: StudentsRepository,
    imports_repo: ImportsRepository,
):
    with tempfile.NamedTemporaryFile(suffix=".csv", mode="w", delete=False, encoding="utf-8") as f:
        f.write("Full Name,Contact Number,Class Batch,Consent\n")
        f.write("Alice Smith,01700000001,Batch-A,yes\n")
        f.write("Bob Jones,01800000002,Batch-B,no\n")
        f.write("Bad Number Student,1234,Batch-C,unknown\n")
        temp_path = f.name

    try:
        mapping = {
            "name": "Full Name",
            "phone": "Contact Number",
            "email": None,
            "batch": "Class Batch",
            "consent_status": "Consent",
        }
        res = import_service.execute_import(temp_path, mapping, duplicate_mode="skip")

        assert res["total_rows"] == 3
        assert res["valid_rows"] == 2
        assert res["invalid_rows"] == 1
        assert res["duplicate_rows"] == 0

        # Verify database contents
        students = students_repo.get_all()
        assert len(students) == 3

        alice = next(s for s in students if s["name"] == "Alice Smith")
        assert alice["phone"] == "+8801700000001"
        assert alice["raw_phone"] == "01700000001"
        assert alice["consent_status"] == "granted"
        assert alice["is_valid"] == 1

        bob = next(s for s in students if s["name"] == "Bob Jones")
        assert bob["consent_status"] == "opted_out"

        bad = next(s for s in students if s["name"] == "Bad Number Student")
        assert bad["is_valid"] == 0
        assert bad["validation_error"] is not None

        # Verify imports audit table
        recent_imports = imports_repo.get_recent(limit=1)
        assert len(recent_imports) == 1
        assert recent_imports[0]["total_rows"] == 3
        assert recent_imports[0]["valid_rows"] == 2
        assert recent_imports[0]["invalid_rows"] == 1

    finally:
        Path(temp_path).unlink(missing_ok=True)

def test_import_xlsx_and_duplicate_handling_skip(
    import_service: ImportService,
    students_repo: StudentsRepository,
):
    # Pre-populate one student
    students_repo.add_student(
        name="Existing Rahim",
        phone="+8801711111111",
        raw_phone="01711111111",
        batch="Old Batch",
    )

    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
        temp_path = f.name

    df = pd.DataFrame([
        {"Name": "Rahim Duplicate", "Phone": "01711111111", "Batch": "New Batch"},
        {"Name": "New Karim", "Phone": "01722222222", "Batch": "Batch 2026"},
    ])
    df.to_excel(temp_path, index=False, engine="openpyxl")

    try:
        mapping = {"name": "Name", "phone": "Phone", "batch": "Batch"}
        res = import_service.execute_import(temp_path, mapping, duplicate_mode="skip")

        assert res["total_rows"] == 2
        assert res["duplicate_rows"] == 1

        students = students_repo.get_all()
        assert len(students) == 2
        rahim = next(s for s in students if s["phone"] == "+8801711111111")
        assert rahim["name"] == "Existing Rahim"  # Kept original because duplicate_mode is 'skip'
    finally:
        Path(temp_path).unlink(missing_ok=True)

def test_import_duplicate_mode_update(
    import_service: ImportService,
    students_repo: StudentsRepository,
):
    students_repo.add_student(
        name="Existing Rahim",
        phone="+8801711111111",
        batch="Old Batch",
    )

    with tempfile.NamedTemporaryFile(suffix=".csv", mode="w", delete=False) as f:
        f.write("name,phone,batch\n")
        f.write("Rahim Updated,01711111111,Updated Batch\n")
        temp_path = f.name

    try:
        mapping = {"name": "name", "phone": "phone", "batch": "batch"}
        res = import_service.execute_import(temp_path, mapping, duplicate_mode="update")

        assert res["duplicate_rows"] == 1
        students = students_repo.get_all()
        assert len(students) == 1
        assert students[0]["name"] == "Rahim Updated"
        assert students[0]["batch"] == "Updated Batch"
    finally:
        Path(temp_path).unlink(missing_ok=True)
