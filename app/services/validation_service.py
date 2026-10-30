"""Student validation and duplicate detection service."""
from typing import Dict, Any, List, Optional, Tuple
from app.utils.phone import normalize_phone, PhoneValidationResult
from app.utils.logger import logger

class ValidationService:
    """Handles phone validation, normalization, consent checks, and duplicate detection."""

    VALID_CONSENT_STATUSES = {"granted", "unknown", "opted_out"}

    def __init__(self, default_region: str = "BD"):
        self.default_region = default_region

    def set_default_region(self, region: str) -> None:
        """Updates the default ISO country region code."""
        if region:
            self.default_region = region.upper().strip()

    def validate_student_record(
        self,
        record: Dict[str, Any],
        existing_phones: Optional[set] = None,
    ) -> Dict[str, Any]:
        """
        Validates and normalizes a single student record dictionary.
        Returns an enriched dictionary with:
        - phone (normalized E.164 string if parseable, or raw phone string)
        - raw_phone (original raw string)
        - is_valid (1 if valid, 0 if malformed)
        - validation_error (description if invalid, else None)
        - is_duplicate (1 if existing in existing_phones, else 0)
        - consent_status ('granted', 'unknown', or 'opted_out')
        """
        raw_name = str(record.get("name", "")).strip()
        raw_phone = str(record.get("phone", "")).strip()
        raw_email = str(record.get("email", "")).strip() if record.get("email") else None
        raw_batch = str(record.get("batch", "")).strip() if record.get("batch") else None

        # Normalize consent status
        raw_consent = str(record.get("consent_status", "unknown")).strip().lower()
        if raw_consent in ("yes", "granted", "true", "1", "opted_in"):
            consent_status = "granted"
        elif raw_consent in ("no", "opted_out", "opt_out", "blocked"):
            consent_status = "opted_out"
        else:
            consent_status = "unknown"

        # Validate & normalize phone number
        phone_result: PhoneValidationResult = normalize_phone(raw_phone, self.default_region)

        is_valid = 1 if phone_result.is_valid else 0
        validation_error = phone_result.error

        # Store normalized E.164 if possible; otherwise keep raw phone for review
        phone_to_store = phone_result.e164 if phone_result.e164 else raw_phone

        # Duplicate check by normalized E.164 phone
        is_duplicate = 0
        if existing_phones and phone_to_store in existing_phones:
            is_duplicate = 1

        return {
            "name": raw_name or "Unknown",
            "phone": phone_to_store,
            "raw_phone": raw_phone,
            "email": raw_email,
            "batch": raw_batch,
            "whatsapp_status": "unknown",  # Always default to unknown
            "consent_status": consent_status,
            "is_valid": is_valid,
            "validation_error": validation_error,
            "is_duplicate": is_duplicate,
        }
