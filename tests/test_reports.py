"""Tests for CSV and XLSX exports ensuring exported data exactly mirrors the database."""
import pytest
import tempfile
from pathlib import Path
import pandas as pd

from app.services.report_service import ReportService
from app.database.repository import StudentsRepository, CampaignsRepository

def test_export_students_matches_database_data(
    report_service: ReportService,
    students_repo: StudentsRepository,
):
    s1 = students_repo.add_student(
        name="Student Alpha",
        phone="+8801700000001",
        raw_phone="01700000001",
        email="alpha@test.com",
        batch="2026-CS",
        consent_status="granted",
    )
    s2 = students_repo.add_student(
        name="Student Beta",
        phone="+8801700000002",
        raw_phone="01700000002",
        email="beta@test.com",
        batch="2026-EE",
        consent_status="opted_out",
    )

    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
        temp_csv = f.name

    try:
        report_service.export_students(temp_csv, export_format="csv")
        df = pd.read_csv(temp_csv, dtype=str)

        assert len(df) == 2
        alpha = df[df["name"] == "Student Alpha"].iloc[0]
        assert alpha["phone"] == "+8801700000001"
        assert alpha["raw_phone"] == "01700000001"
        assert alpha["consent_status"] == "granted"
        assert alpha["batch"] == "2026-CS"
        assert alpha["email"] == "alpha@test.com"

        beta = df[df["name"] == "Student Beta"].iloc[0]
        assert beta["consent_status"] == "opted_out"
    finally:
        Path(temp_csv).unlink(missing_ok=True)

def test_export_campaign_report_matches_db(
    report_service: ReportService,
    campaigns_repo: CampaignsRepository,
    students_repo: StudentsRepository,
):
    sid = students_repo.add_student(name="Test Recipient", phone="+8801700000001")
    cid = campaigns_repo.create(
        name="Export Test Campaign",
        message_template="Hello {{name}}",
        template_id=None,
        total_recipients=1,
    )
    campaigns_repo.add_recipients(
        cid,
        [{
            "student_id": sid,
            "phone": "+8801700000001",
            "personalized_message": "Hello Test Recipient",
            "status": "sent",
        }],
    )

    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
        temp_xlsx = f.name

    try:
        report_service.export_campaign_report(cid, temp_xlsx, export_format="xlsx")
        df = pd.read_excel(temp_xlsx, dtype=str, engine="openpyxl")

        assert len(df) == 1
        row = df.iloc[0]
        assert int(row["campaign_id"]) == cid
        assert row["phone"] == "+8801700000001"
        assert row["status"] == "sent"
        assert row["personalized_message"] == "Hello Test Recipient"
    finally:
        Path(temp_xlsx).unlink(missing_ok=True)
