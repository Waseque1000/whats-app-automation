"""Tests for message template substitution, placeholder extraction, and validation."""
import pytest
from app.services.template_service import TemplateService

def test_template_substitution():
    tpl = "Dear {{name}}, your class {{batch}} starts at 10 AM. Phone: {{phone}}"
    student = {
        "name": "Sarah Connor",
        "batch": "Cybernetics-101",
        "phone": "+8801700000000",
    }
    rendered = TemplateService.render(tpl, student)
    assert rendered == "Dear Sarah Connor, your class Cybernetics-101 starts at 10 AM. Phone: +8801700000000"

def test_template_missing_placeholder_falls_back_to_empty():
    tpl = "Hello {{name}}, your email is {{email}}."
    student = {"name": "John"}  # No email provided
    rendered = TemplateService.render(tpl, student)
    assert rendered == "Hello John, your email is ."

def test_template_validation_identifies_unknown_placeholders():
    tpl = "Hello {{name}}, your role is {{role}} and department is {{department}}."
    is_valid, found, unknown = TemplateService.validate_template(tpl)
    assert is_valid is False
    assert set(found) == {"name", "role", "department"}
    assert set(unknown) == {"role", "department"}

def test_template_validation_valid():
    tpl = "Notice for {{name}} in batch {{batch}}."
    is_valid, found, unknown = TemplateService.validate_template(tpl)
    assert is_valid is True
    assert unknown == []
    assert set(found) == {"name", "batch"}

def test_empty_template_validation():
    is_valid, found, unknown = TemplateService.validate_template("   ")
    assert is_valid is False
