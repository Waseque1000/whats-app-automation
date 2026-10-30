"""Phone validation and E.164 normalization using the phonenumbers library."""
from dataclasses import dataclass
from typing import Optional
import phonenumbers
from phonenumbers import NumberParseException, PhoneNumberFormat

@dataclass
class PhoneValidationResult:
    """Result of phone number parsing and validation."""
    is_valid: bool
    e164: Optional[str]
    raw: str
    country_code: Optional[int]
    national_number: Optional[str]
    error: Optional[str]

def normalize_phone(phone_input: any, default_region: str = "BD") -> PhoneValidationResult:
    """
    Parses and normalizes a phone number to E.164 format.
    Unparseable numbers are returned with is_valid=False and an error message.
    Leading zeros and text formatting are preserved in raw.
    """
    if phone_input is None:
        return PhoneValidationResult(
            is_valid=False,
            e164=None,
            raw="",
            country_code=None,
            national_number=None,
            error="Phone number is empty"
        )

    # Convert to string, preserving leading zeros (e.g. from Excel/CSV)
    raw_str = str(phone_input).strip()
    if not raw_str:
        return PhoneValidationResult(
            is_valid=False,
            e164=None,
            raw="",
            country_code=None,
            national_number=None,
            error="Phone number is empty"
        )

    # Clean float representations like 8801700000000.0 if imported from Excel numeric
    if raw_str.endswith(".0"):
        raw_str = raw_str[:-2]

    try:
        parsed = phonenumbers.parse(raw_str, default_region.upper() if default_region else None)
        is_possible = phonenumbers.is_possible_number(parsed)
        is_valid_format = phonenumbers.is_valid_number(parsed)

        if not is_possible:
            return PhoneValidationResult(
                is_valid=False,
                e164=None,
                raw=raw_str,
                country_code=parsed.country_code,
                national_number=str(parsed.national_number),
                error="Number length or prefix is impossible for specified region"
            )

        if not is_valid_format:
            # Still valid format for E.164 representation, but flag as unconfirmed format
            e164_str = phonenumbers.format_number(parsed, PhoneNumberFormat.E164)
            return PhoneValidationResult(
                is_valid=False,
                e164=e164_str,
                raw=raw_str,
                country_code=parsed.country_code,
                national_number=str(parsed.national_number),
                error="Invalid phone number format for region"
            )

        e164_str = phonenumbers.format_number(parsed, PhoneNumberFormat.E164)
        return PhoneValidationResult(
            is_valid=True,
            e164=e164_str,
            raw=raw_str,
            country_code=parsed.country_code,
            national_number=str(parsed.national_number),
            error=None
        )

    except NumberParseException as exc:
        return PhoneValidationResult(
            is_valid=False,
            e164=None,
            raw=raw_str,
            country_code=None,
            national_number=None,
            error=f"Unparseable phone format: {exc._msg}"
        )
    except Exception as exc:
        return PhoneValidationResult(
            is_valid=False,
            e164=None,
            raw=raw_str,
            country_code=None,
            national_number=None,
            error=f"Unexpected parsing error: {str(exc)}"
        )
