"""
GMAIL_WATCHER_SKILL — Gmail Client
Phase 1: GmailClient ABC, MockGmailClient (test/dev), RealGmailClient (Phase 2 stub).

Constitution compliance:
  - Principle I: Local-First — MockGmailClient requires no network
  - Section 8: Credential Storage — RealGmailClient stub accepts credential_token, never logs it
  - Principle VI: Fail Safe — health_check() never raises; fetch errors are surfaced, not hidden
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections import deque
from typing import Optional

from .models import GmailConfig, GmailMessage, make_gmail_message


# ---------------------------------------------------------------------------
# Abstract interface
# ---------------------------------------------------------------------------

class GmailClient(ABC):
    """
    Abstract contract for Gmail access.

    Phase 1 uses MockGmailClient.
    Phase 2 will provide RealGmailClient backed by the Gmail API.
    """

    @abstractmethod
    def fetch_unread(
        self,
        max_results: int = 10,
        filter_labels: Optional[list[str]] = None,
    ) -> list[GmailMessage]:
        """
        Return up to *max_results* unread messages.

        If *filter_labels* is non-empty, only messages with at least one
        of those labels are returned. Never raises.
        """

    @abstractmethod
    def mark_read(self, message_id: str) -> bool:
        """Mark a message as read. Returns True on success."""

    @abstractmethod
    def health_check(self) -> bool:
        """Return True if the Gmail API / mock is reachable. Never raises."""


# ---------------------------------------------------------------------------
# MockGmailClient — deterministic, in-memory, no network
# ---------------------------------------------------------------------------

class MockGmailClient(GmailClient):
    """
    In-memory Gmail client for unit tests and local development.

    Usage::

        client = MockGmailClient()
        client.inject_message(make_gmail_message("Hello", "alice@example.com"))
        messages = client.fetch_unread(max_results=5)
    """

    def __init__(self, healthy: bool = True) -> None:
        self._inbox:   deque[GmailMessage] = deque()
        self._read:    set[str]            = set()
        self._healthy: bool                = healthy
        self._fetch_count: int             = 0

    # ------------------------------------------------------------------
    # Test helpers
    # ------------------------------------------------------------------

    def inject_message(self, message: GmailMessage) -> None:
        """Add a message to the mock inbox."""
        self._inbox.append(message)

    def set_healthy(self, healthy: bool) -> None:
        """Flip the health state."""
        self._healthy = healthy

    def clear_inbox(self) -> None:
        """Remove all messages from the mock inbox."""
        self._inbox.clear()
        self._read.clear()

    @property
    def fetch_count(self) -> int:
        """Total number of fetch_unread calls made."""
        return self._fetch_count

    @property
    def inbox_size(self) -> int:
        """Number of messages currently in the mock inbox."""
        return len(self._inbox)

    # ------------------------------------------------------------------
    # GmailClient interface
    # ------------------------------------------------------------------

    def fetch_unread(
        self,
        max_results: int = 10,
        filter_labels: Optional[list[str]] = None,
    ) -> list[GmailMessage]:
        self._fetch_count += 1
        results = []
        for msg in self._inbox:
            if msg.message_id in self._read:
                continue
            if filter_labels:
                if not any(lbl in msg.labels for lbl in filter_labels):
                    continue
            results.append(msg)
            if len(results) >= max_results:
                break
        return results

    def mark_read(self, message_id: str) -> bool:
        self._read.add(message_id)
        return True

    def health_check(self) -> bool:
        return self._healthy


# ---------------------------------------------------------------------------
# RealGmailClient — Phase 2 stub (raises NotImplementedError)
# ---------------------------------------------------------------------------

class RealGmailClient(GmailClient):
    """
    Phase 2 stub.  Will wrap the Google Gmail API.

    Accepts a credential_token so callers can pass the secret from
    SecuritySkill without this class ever storing or logging it.
    """

    def __init__(self, config: GmailConfig, credential_token: str = "") -> None:
        # credential_token is intentionally not stored as a persistent attribute
        # — Phase 2 will pass it through to the API client on each call.
        self._config = config
        self._has_token = bool(credential_token)

    def fetch_unread(
        self,
        max_results: int = 10,
        filter_labels: Optional[list[str]] = None,
    ) -> list[GmailMessage]:
        raise NotImplementedError(
            "RealGmailClient is a Phase 2 stub. Use MockGmailClient for now."
        )

    def mark_read(self, message_id: str) -> bool:
        raise NotImplementedError(
            "RealGmailClient is a Phase 2 stub. Use MockGmailClient for now."
        )

    def health_check(self) -> bool:
        # Returns False (not True) so watchers don't treat stub as healthy
        return False
