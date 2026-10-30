"""Tests for messaging providers interface and WhatsApp Web configuration."""
import pytest
import tempfile
from pathlib import Path

from app.messaging.base import BaseMessagingProvider, RecipientStatus, ProviderMessageResult
from app.messaging.mock_provider import MockProvider
from app.messaging.whatsapp_web import WhatsAppWebProvider

def test_mock_provider_conformance():
    prov = MockProvider(simulate_latency_ms=0)
    assert isinstance(prov, BaseMessagingProvider)
    assert prov.is_connected() is True

    res = prov.send_message("+8801700000001", "Hello Test")
    assert res.status == RecipientStatus.SENT
    assert res.external_message_id is not None

def test_mock_provider_simulated_failure():
    prov = MockProvider(simulate_latency_ms=0)
    res = prov.send_message("+8801700000000", "Hello Fail")
    assert res.status == RecipientStatus.FAILED
    assert "unreachable" in res.error_message.lower()

def test_whatsapp_web_provider_conformance():
    with tempfile.TemporaryDirectory() as tmp_dir:
        prov = WhatsAppWebProvider(session_dir=tmp_dir)
        assert isinstance(prov, BaseMessagingProvider)
        assert "WhatsApp Web" in prov.provider_name
        assert prov.is_connected() is False
