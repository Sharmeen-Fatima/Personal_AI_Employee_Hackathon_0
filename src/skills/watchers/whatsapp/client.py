"""
WHATSAPP_WATCHER_SKILL — WhatsApp Client
Phase 1: WhatsAppClient ABC, MockWhatsAppClient (test/dev), RealWhatsAppClient (Phase 2 stub).

Adapter pattern: the watcher depends only on the abstract WhatsAppClient interface.
Phase 2 will provide a concrete implementation backed by WhatsApp Business API / Twilio / etc.

Constitution compliance:
  - Principle I: Local-First — MockWhatsAppClient requires no network
  - Section 8: Credential Storage — RealWhatsAppClient accepts token parameter, never logs it
  - Principle VI: Fail Safe — health_check() never raises; fetch errors surfaced, not hidden
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections import deque
from typing import Optional

from .models import (
    WhatsAppChatType,
    WhatsAppConfig,
    WhatsAppMessage,
    make_whatsapp_message,
)


# ---------------------------------------------------------------------------
# Abstract interface
# ---------------------------------------------------------------------------

class WhatsAppClient(ABC):
    """
    Abstract contract for WhatsApp message access.

    Phase 1 uses MockWhatsAppClient.
    Phase 2 will provide RealWhatsAppClient backed by a real API adapter.
    """

    @abstractmethod
    def fetch_messages(
        self,
        max_results: int = 20,
        filter_chat_types: Optional[list[str]] = None,
        filter_senders: Optional[list[str]] = None,
    ) -> list[WhatsAppMessage]:
        """
        Return up to *max_results* unread/pending messages.

        Filters:
          filter_chat_types: only return messages from these chat types (PRIVATE/GROUP).
          filter_senders:    only return messages from these phone numbers.
        Never raises.
        """

    @abstractmethod
    def send_read_receipt(self, message_id: str) -> bool:
        """Mark a message as read. Returns True on success."""

    @abstractmethod
    def health_check(self) -> bool:
        """Return True if the WhatsApp API / mock is reachable. Never raises."""


# ---------------------------------------------------------------------------
# MockWhatsAppClient — deterministic, in-memory, no network
# ---------------------------------------------------------------------------

class MockWhatsAppClient(WhatsAppClient):
    """
    In-memory WhatsApp client for unit tests and local development.

    Usage::

        client = MockWhatsAppClient()
        client.inject_message(make_whatsapp_message("+14155550100", "Hello!"))
        messages = client.fetch_messages(max_results=10)
    """

    def __init__(self, healthy: bool = True) -> None:
        self._inbox:        deque[WhatsAppMessage] = deque()
        self._receipts_sent: set[str]              = set()
        self._healthy:       bool                  = healthy
        self._fetch_count:   int                   = 0

    # ------------------------------------------------------------------
    # Test helpers
    # ------------------------------------------------------------------

    def inject_message(self, message: WhatsAppMessage) -> None:
        """Add a message to the mock inbox."""
        self._inbox.append(message)

    def set_healthy(self, healthy: bool) -> None:
        """Flip the health state."""
        self._healthy = healthy

    def clear_inbox(self) -> None:
        """Remove all messages from the mock inbox and receipt log."""
        self._inbox.clear()
        self._receipts_sent.clear()

    @property
    def fetch_count(self) -> int:
        """Total number of fetch_messages calls made."""
        return self._fetch_count

    @property
    def inbox_size(self) -> int:
        """Number of messages currently in the mock inbox."""
        return len(self._inbox)

    @property
    def receipts_sent(self) -> set[str]:
        """Set of message IDs for which read receipts were sent."""
        return set(self._receipts_sent)

    # ------------------------------------------------------------------
    # WhatsAppClient interface
    # ------------------------------------------------------------------

    def fetch_messages(
        self,
        max_results: int = 20,
        filter_chat_types: Optional[list[str]] = None,
        filter_senders: Optional[list[str]] = None,
    ) -> list[WhatsAppMessage]:
        self._fetch_count += 1
        results: list[WhatsAppMessage] = []

        # Normalise filters to lowercase sets for comparison
        chat_filter   = {ct.lower() for ct in filter_chat_types} if filter_chat_types else None
        sender_filter = {sp.strip() for sp in filter_senders}     if filter_senders    else None

        for msg in self._inbox:
            if msg.message_id in self._receipts_sent:
                continue
            if chat_filter and msg.chat_type.lower() not in chat_filter:
                continue
            if sender_filter and msg.sender_phone not in sender_filter:
                continue
            results.append(msg)
            if len(results) >= max_results:
                break

        return results

    def send_read_receipt(self, message_id: str) -> bool:
        self._receipts_sent.add(message_id)
        return True

    def health_check(self) -> bool:
        return self._healthy


# ---------------------------------------------------------------------------
# RealWhatsAppClient — Phase 2 stub (raises NotImplementedError)
# ---------------------------------------------------------------------------

class RealWhatsAppClient(WhatsAppClient):
    """
    Phase 2 stub.  Will wrap a real WhatsApp Business API adapter
    (e.g. Twilio, Meta Cloud API, or whatsapp-web.js bridge).

    Accepts a credential_token so callers can pass the secret from
    SecuritySkill without this class ever storing or logging it.
    """

    def __init__(self, config: WhatsAppConfig, credential_token: str = "") -> None:
        self._config    = config
        self._has_token = bool(credential_token)

    def fetch_messages(
        self,
        max_results: int = 20,
        filter_chat_types: Optional[list[str]] = None,
        filter_senders: Optional[list[str]] = None,
    ) -> list[WhatsAppMessage]:
        raise NotImplementedError(
            "RealWhatsAppClient is a Phase 2 stub. Use MockWhatsAppClient for now."
        )

    def send_read_receipt(self, message_id: str) -> bool:
        raise NotImplementedError(
            "RealWhatsAppClient is a Phase 2 stub. Use MockWhatsAppClient for now."
        )

    def health_check(self) -> bool:
        # Returns False so watchers never treat stub as healthy
        return False
