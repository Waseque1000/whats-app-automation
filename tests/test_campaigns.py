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
