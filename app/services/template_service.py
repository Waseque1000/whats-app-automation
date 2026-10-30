"""Message template parsing, placeholder validation, and personalized rendering."""
import re
import json
import random
from typing import Dict, Any, List, Set, Tuple, Optional, Union

# Supported standard placeholder variables
SUPPORTED_VARIABLES: Set[str] = {"name", "phone", "email", "batch"}

# Regular expression to match {{placeholder}} or {{ placeholder }}
PLACEHOLDER_REGEX = re.compile(r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}")

# Regular expression to match Spintax like {option1|option2|option3}
SPINTAX_REGEX = re.compile(r"\{([^{}]+?\|[^{}]+?)\}")

class TemplateService:
    """Handles template syntax validation, placeholder extraction, and variable substitution."""

    @staticmethod
    def apply_spintax(text: str) -> str:
        """
        Resolves Spintax formatted variations like '{Hello|Hi|Greetings}'
        by choosing one option randomly. Handles nested or sequential options.
        """
        if not text or "{" not in text or "|" not in text:
            return text

        result = text
        # Resolve innermost spintax patterns until none remain
        max_depth = 5
        depth = 0
        while depth < max_depth and SPINTAX_REGEX.search(result):
            result = SPINTAX_REGEX.sub(
                lambda m: random.choice(m.group(1).split("|")),
                result,
            )
            depth += 1
        return result

    @staticmethod
    def clean_variants(variants_input: Any) -> List[str]:
        """
        Normalizes and cleans a single string, list of strings, or JSON list of strings.
        Discards blank or empty variants.
        """
        if variants_input is None:
            return []

        if isinstance(variants_input, str):
            trimmed = variants_input.strip()
            if not trimmed:
                return []
            if trimmed.startswith("[") and trimmed.endswith("]"):
                try:
                    parsed = json.loads(trimmed)
                    if isinstance(parsed, list):
                        return [str(v).strip() for v in parsed if str(v).strip()]
                except Exception:
                    pass
            return [trimmed]

        if isinstance(variants_input, (list, tuple)):
            cleaned = []
            for v in variants_input:
                s = str(v).strip() if v is not None else ""
                if s:
                    cleaned.append(s)
            return cleaned

        return [str(variants_input).strip()] if str(variants_input).strip() else []

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
    def validate_variants(
        variants: List[str],
        allowed_variables: Optional[Set[str]] = None,
    ) -> Tuple[bool, List[str], List[str]]:
        """
        Validates all message variants in a list.
        Returns:
            (all_valid: bool, all_found: List[str], all_unknown: List[str])
        """
        cleaned = TemplateService.clean_variants(variants)
        if not cleaned:
            return False, [], ["At least one non-empty message variant is required."]

        all_found = []
        all_unknown = []
        seen_found = set()
        seen_unknown = set()

        for v in cleaned:
            valid, found, unknown = TemplateService.validate_template(v, allowed_variables)
            for f in found:
                if f not in seen_found:
                    seen_found.add(f)
                    all_found.append(f)
            for u in unknown:
                if u not in seen_unknown:
                    seen_unknown.add(u)
                    all_unknown.append(u)

        return len(all_unknown) == 0, all_found, all_unknown

    @staticmethod
    def render(template_text: str, student_data: Dict[str, Any]) -> str:
        """
        Renders a personalized message by substituting {{placeholder}} with student fields,
        and evaluating Spintax {a|b|c}. Missing fields default to empty string.
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

        subbed = PLACEHOLDER_REGEX.sub(replace_var, template_text)
        return TemplateService.apply_spintax(subbed)

    @staticmethod
    def render_variant(
        variants: List[str],
        student_data: Dict[str, Any],
        recipient_index: int,
    ) -> Tuple[str, int]:
        """
        Rotates through message variants in round-robin sequence:
        Recipient 0 -> Variant 0
        Recipient 1 -> Variant 1
        Recipient 2 -> Variant 2
        ...
        Returns:
            (personalized_message: str, variant_index: int)
        """
        cleaned = TemplateService.clean_variants(variants)
        if not cleaned:
            return "", 0
        variant_idx = recipient_index % len(cleaned)
        return TemplateService.render(cleaned[variant_idx], student_data), variant_idx

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

    @staticmethod
    def preview_variants(
        variants: List[str],
        sample_student: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Renders preview for each variant with variant index and text."""
        cleaned = TemplateService.clean_variants(variants)
        results = []
        for idx, v in enumerate(cleaned):
            rendered = TemplateService.preview(v, sample_student)
            results.append({
                "variant_index": idx,
                "variant_label": f"SMS #{idx + 1}",
                "template_text": v,
                "rendered_preview": rendered,
            })
        return results
