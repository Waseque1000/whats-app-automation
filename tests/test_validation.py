"""Tests for phone normalization, validation, region fallback, and duplicate detection."""
import pytest
from app.utils.phone import normalize_phone
from app.services.validation_service import ValidationService

def test_normalize_valid_phone_with_country_code():
    res = normalize_phone("+8801712345678", default_region="BD")
    assert res.is_valid is True
    assert res.e164 == "+8801712345678"
    assert res.country_code == 880

def test_normalize_phone_using_default_region():
    # Number without country prefix in Bangladesh
    res = normalize_phone("01712345678", default_region="BD")
    assert res.is_valid is True
    assert res.e164 == "+8801712345678"
    assert res.raw == "01712345678"

def test_normalize_phone_us_region():
    res = normalize_phone("2025550143", default_region="US")
    assert res.is_valid is True
    assert res.e164 == "+12025550143"

def test_unparseable_phone_is_flagged_not_dropped():
    res = normalize_phone("abc12345#bad", default_region="BD")
    assert res.is_valid is False
    assert res.raw == "abc12345#bad"
    assert res.error is not None
    assert "Unparseable" in res.error or "error" in res.error.lower()

def test_preserve_leading_zeros_and_raw_phone():
    res = normalize_phone("01999999999", default_region="BD")
    assert res.raw == "01999999999"
    assert res.raw.startswith("0")

def test_validation_service_duplicate_detection(validation_service: ValidationService):
    existing = {"+8801712345678"}
    rec1 = {
        "name": "Rahim",
        "phone": "01712345678",
        "consent_status": "granted",
    }
    val1 = validation_service.validate_student_record(rec1, existing)
    assert val1["is_duplicate"] == 1
    assert val1["phone"] == "+8801712345678"

    rec2 = {
        "name": "Karim",
        "phone": "01812345678",
        "consent_status": "opted_out",
    }
    val2 = validation_service.validate_student_record(rec2, existing)
    assert val2["is_duplicate"] == 0
    assert val2["consent_status"] == "opted_out"
