"""
EMAIL_MCP_ACTION_SKILL — Email Adapter
Phase 1: EmailAdapter ABC, MockEmailAdapter (no SMTP), RealEmailAdapter (Phase 2 stub).

Constitution compliance:
  - Principle I: Local-First — MockEmailAdapter requires no network
  - Section 8: Credential Storage — RealEmailAdapter never logs credentials
  - Principle VI: Fail Safe — health_check() never raises; send() never raises
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone

from .models import EmailActionStatus, EmailRequest, EmailResult


# ---------------------------------------------------------------------------
# Abstract interface
# ---------------------------------------------------------------------------

class EmailAdapter(ABC):
    """
    Abstract contract for email sending.

    Phase 1 uses MockEmailAdapter.
    Phase 2 will provide RealEmailAdapter backed by smtplib or an email API.
    """

    @abstractmethod
    def send(self, request: EmailRequest) -> EmailResult:
        """
        Send an email. Returns EmailResult. Never raises.
        On failure, return EmailResult with status=FAILED and error message.
        """

    @abstractmethod
    def health_check(self) -> bool:
        """Return True if the adapter is ready to send. Never raises."""


# ---------------------------------------------------------------------------
# MockEmailAdapter — in-memory, no network, deterministic
# ---------------------------------------------------------------------------

class MockEmailAdapter(EmailAdapter):
    """
    In-memory email adapter for unit tests and local development.
    No SMTP connection is made; emails are captured in self._sent.

    Usage::

        adapter = MockEmailAdapter()
        result  = adapter.send(make_email_request(["alice@example.com"], "Hi", "Body"))
        assert result.status == EmailActionStatus.SENT
        assert adapter.send_count == 1
    """

    def __init__(self, healthy: bool = True, fail_send: bool = False) -> None:
        self._sent:       list[EmailResult] = []
        self._healthy:    bool              = healthy
        self._fail_send:  bool              = fail_send
        self._send_count: int               = 0

    # ------------------------------------------------------------------
    # Test helpers
    # ------------------------------------------------------------------

    def set_healthy(self, healthy: bool) -> None:
        self._healthy = healthy

    def set_fail_send(self, fail: bool) -> None:
        """Simulate send failures when True."""
        self._fail_send = fail

    def clear_sent(self) -> None:
        self._sent.clear()
        self._send_count = 0

    @property
    def sent(self) -> list[EmailResult]:
        """All results produced by this adapter (defensive copy)."""
        return list(self._sent)

    @property
    def send_count(self) -> int:
        return self._send_count

    # ------------------------------------------------------------------
    # EmailAdapter interface
    # ------------------------------------------------------------------

    def send(self, request: EmailRequest) -> EmailResult:
        self._send_count += 1
        if self._fail_send:
            result = EmailResult(
                request_id=request.request_id,
                status=EmailActionStatus.FAILED,
                error="MockEmailAdapter: simulated send failure",
                adapter="mock",
            )
            self._sent.append(result)
            return result

        result = EmailResult(
            request_id=request.request_id,
            status=EmailActionStatus.SENT,
            sent_at=datetime.now(tz=timezone.utc),
            adapter="mock",
        )
        self._sent.append(result)
        return result

    def health_check(self) -> bool:
        return self._healthy


# ---------------------------------------------------------------------------
# RealEmailAdapter — Phase 2 stub (raises NotImplementedError)
# ---------------------------------------------------------------------------

class RealEmailAdapter(EmailAdapter):
    """
    Phase 2 stub.  Will wrap smtplib or an SMTP API.

    Accepts credential_token so callers can pass the secret from
    SecuritySkill without this class ever storing or logging it.
    """

    def __init__(self, config: "EmailConfig", credential_token: str = "") -> None:  # noqa: F821
        # credential_token is intentionally not stored as a persistent attribute
        self._has_token = bool(credential_token)

    def send(self, request: EmailRequest) -> EmailResult:
        raise NotImplementedError(
            "RealEmailAdapter is a Phase 2 stub. Use MockEmailAdapter for now."
        )

    def health_check(self) -> bool:
        # Returns False so callers don't treat stub as healthy
        return False
