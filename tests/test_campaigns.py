"""Tests for campaign creation, state transitions, opt-out exclusion, and confirmation logging."""
import pytest
import time
from app.services.campaign_service import CampaignService
from app.database.repository import CampaignsRepository, StudentsRepository
from app.messaging.mock_provider import MockProvider
from app.messaging.base import RecipientStatus

def test_opted_out_student_strictly_excluded_in_service_layer(
    campaign_service: CampaignService,
    students_repo: StudentsRepository,
):
    # Add granted student
    s1 = students_repo.add_student(
        name="Student Granted",
        phone="+8801700000001",
        consent_status="granted",
    )
    # Add opted-out student
    s2 = students_repo.add_student(
        name="Student Opted Out",
        phone="+8801700000002",
        consent_status="opted_out",
    )
    # Add unknown consent student
    s3 = students_repo.add_student(
        name="Student Unknown",
        phone="+8801700000003",
        consent_status="unknown",
    )

    staging = campaign_service.stage_campaign_recipients(
        student_ids=[s1, s2, s3],
        template_text="Hello {{name}}",
    )

    # Opted-out student MUST NOT be in eligible recipients
    eligible_ids = [r["student_id"] for r in staging["eligible_recipients"]]
    assert s1 in eligible_ids
    assert s3 in eligible_ids
    assert s2 not in eligible_ids

    # Opted out student must be in excluded list
    excluded_ids = [s["id"] for s in staging["excluded_opted_out"]]
    assert s2 in excluded_ids
    assert staging["unknown_consent_count"] == 1

def test_campaign_creation_and_confirmation_required(
    campaign_service: CampaignService,
    campaigns_repo: CampaignsRepository,
    students_repo: StudentsRepository,
):
    s1 = students_repo.add_student(
        name="Student One",
        phone="+8801700000001",
        consent_status="granted",
    )

    camp_id, staging = campaign_service.create_campaign(
        campaign_name="Test Broadcast",
        template_text="Hello {{name}}",
        template_id=None,
        student_ids=[s1],
    )

    camp = campaigns_repo.get_campaign(camp_id)
    assert camp["status"] == "draft"
    assert camp["confirmed_at"] is None

    # Explicit confirmation step
    confirmed_at = campaign_service.confirm_and_queue_campaign(camp_id)
    assert confirmed_at is not None

    camp_after = campaigns_repo.get_campaign(camp_id)
    assert camp_after["status"] == "queued"
    assert camp_after["confirmed_at"] == confirmed_at

def test_campaign_execution_queue_and_mock_statuses(
    campaign_service: CampaignService,
    campaigns_repo: CampaignsRepository,
    students_repo: StudentsRepository,
):
    s1 = students_repo.add_student(
        name="Good Student",
        phone="+8801700000001",
        consent_status="granted",
    )
    # Special simulated failing number in MockProvider
    s2 = students_repo.add_student(
        name="Failing Student",
        phone="+8801700000000",
        consent_status="granted",
    )

    camp_id, _ = campaign_service.create_campaign(
        campaign_name="Dispatch Test",
        template_text="Hello {{name}}",
        template_id=None,
        student_ids=[s1, s2],
    )
    campaign_service.confirm_and_queue_campaign(camp_id)

    # Synchronously run worker queue
    campaign_service._run_campaign_queue(camp_id, on_progress=None, on_completed=None)

    camp = campaigns_repo.get_campaign(camp_id)
    assert camp["status"] == "completed"
    assert camp["successful_recipients"] == 1
    assert camp["failed_recipients"] == 1

    recipients = campaigns_repo.get_recipients(camp_id)
    r_success = next(r for r in recipients if r["student_id"] == s1)
    r_fail = next(r for r in recipients if r["student_id"] == s2)

    # Mock provider must emit verified status 'sent' - NEVER fabricated delivered/read
    assert r_success["status"] == RecipientStatus.SENT.value
    assert r_fail["status"] == RecipientStatus.FAILED.value

def test_student_without_whatsapp_is_skipped_and_advances_to_next(
    campaign_service: CampaignService,
    campaigns_repo: CampaignsRepository,
    students_repo: StudentsRepository,
):
    """
    Verifies that when a student has no WhatsApp account:
    1. The number is marked as 'skipped' (not failed).
    2. Student registry updates whatsapp_status to 'inactive'.
    3. The campaign automatically and seamlessly proceeds to the next student.
    """
    s1 = students_repo.add_student(
        name="Student with WhatsApp 1",
        phone="+8801700000001",
        consent_status="granted",
    )
    s2_no_wa = students_repo.add_student(
        name="Student without WhatsApp",
        phone="+8801700009999",  # Trigger simulated 'no WhatsApp' skip
        consent_status="granted",
    )
    s3 = students_repo.add_student(
        name="Student with WhatsApp 2",
        phone="+8801700000003",
        consent_status="granted",
    )

    camp_id, _ = campaign_service.create_campaign(
        campaign_name="Skip Non-WhatsApp Test",
        template_text="Hello {{name}}",
        student_ids=[s1, s2_no_wa, s3],
    )
    campaign_service.confirm_and_queue_campaign(camp_id)

    # Execute worker queue
    campaign_service._run_campaign_queue(camp_id, on_progress=None, on_completed=None)

    camp = campaigns_repo.get_campaign(camp_id)
    assert camp["status"] == "completed"
    assert camp["successful_recipients"] == 2
    assert camp["skipped_recipients"] == 1
    assert camp["failed_recipients"] == 0

    recipients = campaigns_repo.get_recipients(camp_id)
    r1 = next(r for r in recipients if r["student_id"] == s1)
    r2 = next(r for r in recipients if r["student_id"] == s2_no_wa)
    r3 = next(r for r in recipients if r["student_id"] == s3)

    assert r1["status"] == RecipientStatus.SENT.value
    assert r2["status"] == RecipientStatus.SKIPPED.value
    assert "no WhatsApp" in r2["error_message"]
    assert r3["status"] == RecipientStatus.SENT.value

    # Check student registry status updates
    stu2 = students_repo.get_by_id(s2_no_wa)
    assert stu2["whatsapp_status"] == "inactive"

def test_multiple_message_variants_round_robin_rotation(
    campaign_service: CampaignService,
    students_repo: StudentsRepository,
    campaigns_repo: CampaignsRepository,
):
    """
    Verifies that providing 3, 4, or 5 SMS types rotates sequentially:
    Student 1 -> SMS #1
    Student 2 -> SMS #2
    Student 3 -> SMS #3
    Student 4 -> SMS #4
    Student 5 -> SMS #1 (cycles back)
    Student 6 -> SMS #2
    """
    # Create 6 students
    s_ids = []
    for i in range(1, 7):
        sid = students_repo.add_student(
            name=f"Student_{i}",
            phone=f"+880170000000{i}",
            consent_status="granted",
            batch=f"Batch-{i}",
        )
        s_ids.append(sid)

    # 4 distinct SMS designs / types
    sms_variants = [
        "Design 1: Hello {{name}}, batch {{batch}} notice.",
        "Design 2: Greetings {{name}}! Reminder for {{batch}}.",
        "Design 3: Dear {{name}}, please check {{batch}} updates.",
        "Design 4: Hi {{name}}, upcoming {{batch}} class details.",
    ]

    camp_id, staging = campaign_service.create_campaign(
        campaign_name="Anti-Ban Rotation Campaign",
        template_text=sms_variants[0],
        template_id=None,
        student_ids=s_ids,
        variants=sms_variants,
    )

    eligible = staging["eligible_recipients"]
    assert len(eligible) == 6

    # Verify rotation across 4 variants: 0, 1, 2, 3, 0, 1
    expected_indices = [0, 1, 2, 3, 0, 1]
    for idx, (rec, exp_idx) in enumerate(zip(eligible, expected_indices)):
        assert rec["variant_index"] == exp_idx
        assert rec["sms_variant"] == f"SMS #{exp_idx + 1}"
        assert f"Design {exp_idx + 1}" in rec["personalized_message"]
        assert f"Student_{idx + 1}" in rec["personalized_message"]

    # Verify database persistence
    camp_rec = campaigns_repo.get_campaign(camp_id)
    assert camp_rec["variants_list"] == sms_variants

    db_recipients = campaigns_repo.get_recipients(camp_id)
    assert len(db_recipients) == 6
    for idx, (db_rec, exp_idx) in enumerate(zip(db_recipients, expected_indices)):
        assert db_rec["variant_index"] == exp_idx
        assert db_rec["sms_variant"] == f"SMS #{exp_idx + 1}"
        assert f"Design {exp_idx + 1}" in db_rec["personalized_message"]

def test_five_sms_types_rotation_across_ten_students(
    campaign_service: CampaignService,
    students_repo: StudentsRepository,
    campaigns_repo: CampaignsRepository,
):
    """
    Tests 5 distinct SMS types rotating across 10 students,
    cycling through 1, 2, 3, 4, 5, 1, 2, 3, 4, 5.
    """
    s_ids = []
    for i in range(1, 11):
        sid = students_repo.add_student(
            name=f"Student_{i:02d}",
            phone=f"+88017000000{i:02d}",
            consent_status="granted",
            batch="Batch-2026",
        )
        s_ids.append(sid)

    five_sms_types = [
        "SMS Type 1: Dear {{name}}, please check your batch {{batch}} class.",
        "SMS Type 2: Hello {{name}}, exciting updates for {{batch}} today!",
        "SMS Type 3: Hi {{name}}, friendly class reminder for batch {{batch}}.",
        "SMS Type 4: Greetings {{name}}, don't miss your {{batch}} session.",
        "SMS Type 5: Hey {{name}}, class time for {{batch}} is approaching!",
    ]

    camp_id, staging = campaign_service.create_campaign(
        campaign_name="5 SMS Types Campaign",
        template_text=five_sms_types[0],
        template_id=None,
        student_ids=s_ids,
        variants=five_sms_types,
    )

    eligible = staging["eligible_recipients"]
    assert len(eligible) == 10

    # Expected variant indices: 0, 1, 2, 3, 4, 0, 1, 2, 3, 4
    expected = [0, 1, 2, 3, 4, 0, 1, 2, 3, 4]
    for idx, rec in enumerate(eligible):
        exp_v = expected[idx]
        assert rec["variant_index"] == exp_v
        assert rec["sms_variant"] == f"SMS #{exp_v + 1}"
        assert f"SMS Type {exp_v + 1}" in rec["personalized_message"]
