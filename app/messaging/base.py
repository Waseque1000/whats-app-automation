"""Abstract messaging provider interface and recipient status enumeration."""
from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, Any

class RecipientStatus(str, Enum):
    """Unified recipient status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    SUBMITTED = "submitted"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class ProviderMessageResult:
    """Result returned by a messaging provider after dispatching an outbound message."""
    status: RecipientStatus
    external_message_id: Optional[str] = None
    error_message: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None

class BaseMessagingProvider(ABC):
    """
    Abstract interface for all WhatsApp messaging providers.
    Both MockProvider and future Cloud API/automation providers must inherit from this.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Name of the messaging provider."""
        pass

    @abstractmethod
    def connect(self) -> bool:
        """Initializes connection/session with the messaging service."""
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        """Returns True if the provider is currently connected and ready."""
        pass

    @abstractmethod
    def send_message(self, phone: str, message: str) -> ProviderMessageResult:
        """
        Dispatches a personalized message to a single phone number.
        Must return a ProviderMessageResult with an authorized status.
        Never infer 'delivered' or 'read' if the underlying network cannot confirm it.
        """
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Closes any active sessions or connections."""
        pass
