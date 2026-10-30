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

def test_clean_variants_handles_various_formats():
    assert TemplateService.clean_variants(None) == []
    assert TemplateService.clean_variants("") == []
    assert TemplateService.clean_variants("  Hello  ") == ["Hello"]
    assert TemplateService.clean_variants(["SMS 1", "  ", "SMS 2"]) == ["SMS 1", "SMS 2"]
    assert TemplateService.clean_variants('["Design A", "Design B", "Design C"]') == ["Design A", "Design B", "Design C"]

def test_spintax_resolution():
    text = "{Hello|Hi|Greetings} {{name}}!"
    rendered = TemplateService.render(text, {"name": "Alex"})
    assert rendered in ["Hello Alex!", "Hi Alex!", "Greetings Alex!"]

def test_render_variant_round_robin():
    variants = [
        "Type 1: Hello {{name}}",
        "Type 2: Hi {{name}}",
        "Type 3: Dear {{name}}",
    ]
    student = {"name": "Zubair"}

    msg0, idx0 = TemplateService.render_variant(variants, student, 0)
    assert msg0 == "Type 1: Hello Zubair" and idx0 == 0

    msg1, idx1 = TemplateService.render_variant(variants, student, 1)
    assert msg1 == "Type 2: Hi Zubair" and idx1 == 1

    msg2, idx2 = TemplateService.render_variant(variants, student, 2)
    assert msg2 == "Type 3: Dear Zubair" and idx2 == 2

    # Cycles back to index 0 for recipient 3
    msg3, idx3 = TemplateService.render_variant(variants, student, 3)
    assert msg3 == "Type 1: Hello Zubair" and idx3 == 0

def test_validate_variants():
    valid_variants = [
        "Hello {{name}}",
        "Hi {{name}} in batch {{batch}}",
        "Dear student {{phone}}",
    ]
    is_valid, found, unknown = TemplateService.validate_variants(valid_variants)
    assert is_valid is True
    assert set(found) == {"name", "batch", "phone"}
    assert unknown == []

    invalid_variants = [
        "Hello {{name}}",
        "Your score is {{score}}",
    ]
    is_valid, found, unknown = TemplateService.validate_variants(invalid_variants)
    assert is_valid is False
    assert "score" in unknown

def test_template_repository_stores_and_retrieves_variants(templates_repo):
    variants = [
        "Type 1: Welcome {{name}}!",
        "Type 2: Hello {{name}}, welcome to our course!",
        "Type 3: Greetings {{name}}, excited to have you!",
    ]
    tid = templates_repo.create(
        name="Multi-variant Welcome",
        content=variants[0],
        variables="name",
        variants=variants,
    )
    tpl = templates_repo.get_by_id(tid)
    assert tpl["template_name"] == "Multi-variant Welcome"
    assert tpl["content"] == variants[0]
    assert tpl["variants_list"] == variants

    # Update template with 4 variants
    updated_variants = variants + ["Type 4: Hi {{name}}!"]
    templates_repo.update(
        tid,
        name="Multi-variant Welcome Updated",
        content=updated_variants[0],
        variables="name",
        variants=updated_variants,
    )
    tpl_updated = templates_repo.get_by_id(tid)
    assert tpl_updated["variants_list"] == updated_variants
    assert len(tpl_updated["variants_list"]) == 4
