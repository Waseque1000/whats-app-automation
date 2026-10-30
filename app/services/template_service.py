"""Message template parsing, placeholder validation, and personalized rendering."""
import re
from typing import Dict, Any, List, Set, Tuple, Optional

# Supported standard placeholder variables
SUPPORTED_VARIABLES: Set[str] = {"name", "phone", "email", "batch"}

# Regular expression to match {{placeholder}} or {{ placeholder }}
PLACEHOLDER_REGEX = re.compile(r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}")

class TemplateService:
    """Handles template syntax validation, placeholder extraction, and variable substitution."""

    @staticmethod
    def extract_placeholders(template_text: str) -> List[str]:
        """Returns a list of unique placeholder names found in the template text."""
        if not template_text:
            return []
        matches = PLACEHOLDER_REGEX.findall(template_text)
        # Preserve order of appearance while deduplicating
        seen = set()
        result = []
        for match in matches:
            var_name = match.strip().lower()
            if var_name not in seen:
                seen.add(var_name)
                result.append(var_name)
        return result

    @staticmethod
    def validate_template(
        template_text: str,
        allowed_variables: Optional[Set[str]] = None,
    ) -> Tuple[bool, List[str], List[str]]:
        """
        Validates template syntax and identifies unknown placeholders.
        Returns:
            (is_valid: bool, found_variables: List[str], unknown_variables: List[str])
        """
        if not template_text or not template_text.strip():
            return False, [], ["Template content cannot be empty."]

        allowed = allowed_variables if allowed_variables is not None else SUPPORTED_VARIABLES
        found = TemplateService.extract_placeholders(template_text)
        unknown = [v for v in found if v not in allowed]

        is_valid = len(unknown) == 0
        return is_valid, found, unknown

    @staticmethod
    def render(template_text: str, student_data: Dict[str, Any]) -> str:
        """
        Renders a personalized message by substituting {{placeholder}} with student fields.
        Missing fields default to empty string.
        """
        if not template_text:
            return ""

        def replace_var(match: re.Match) -> str:
            var_name = match.group(1).strip().lower()
            val = student_data.get(var_name)
            if val is None:
                # Check for raw_phone fallback if var is phone
                if var_name == "phone":
                    val = student_data.get("raw_phone", "")
                else:
                    val = ""
            return str(val)

        return PLACEHOLDER_REGEX.sub(replace_var, template_text)

    @staticmethod
    def preview(template_text: str, sample_student: Optional[Dict[str, Any]] = None) -> str:
        """Convenience method to render a preview for UI."""
        default_sample = {
            "name": "Jane Doe",
            "phone": "+8801700000001",
            "email": "jane@example.com",
            "batch": "2026-Fall",
        }
        data = sample_student if sample_student else default_sample
        return TemplateService.render(template_text, data)
