"""Mock messaging provider for local development and testing."""
import time
import uuid
from typing import Optional
from app.messaging.base import BaseMessagingProvider, RecipientStatus, ProviderMessageResult
from app.utils.logger import logger

class MockProvider(BaseMessagingProvider):
    """
    Simulates message dispatch for testing and development.
    Adheres strictly to the requirement: emits only statuses a real provider could verify.
    Never infers delivered or read receipts.
    """

    def __init__(self, simulate_latency_ms: int = 50):
        self._connected: bool = True
        self.simulate_latency_ms = simulate_latency_ms

    @property
    def provider_name(self) -> str:
        return "MockProvider (Test Simulator)"

    def connect(self) -> bool:
        self._connected = True
        logger.info("MockProvider connected successfully.")
        return True

    def is_connected(self) -> bool:
        return self._connected

    def send_message(self, phone: str, message: str) -> ProviderMessageResult:
        if not self._connected:
            return ProviderMessageResult(
                status=RecipientStatus.FAILED,
                error_message="Provider is not connected."
            )

        if self.simulate_latency_ms > 0:
            time.sleep(self.simulate_latency_ms / 1000.0)

        # Allow test simulation of failures via special test numbers
        if phone.endswith("0000") or "fail" in phone.lower():
            logger.warning(f"MockProvider: Simulating delivery failure for phone {phone}")
            return ProviderMessageResult(
                status=RecipientStatus.FAILED,
                error_message="Simulated provider failure: recipient unreachable.",
            )

        external_id = f"mock_msg_{uuid.uuid4().hex[:12]}"
        logger.info(f"MockProvider: Message sent to {phone} [id: {external_id}]")

        # Emits 'sent' (or 'submitted') as verified by dispatch; never infers delivered/read
        return ProviderMessageResult(
            status=RecipientStatus.SENT,
            external_message_id=external_id,
            error_message=None,
            raw_response={"simulated": True, "provider": "mock", "timestamp": time.time()}
        )

    def disconnect(self) -> None:
        self._connected = False
        logger.info("MockProvider disconnected.")
