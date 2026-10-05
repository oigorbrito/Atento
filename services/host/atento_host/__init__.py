"""Atento host-owned identity and Telegram enrollment primitives.

This package is an implementation slice, not a deployable production host.
"""

from .identity import AuthenticatedExecutionIdentity, IdentityIssuer, IdentityRejected
from .telegram_enrollment import (
    AuthenticatedTelegramEvent,
    EnrollmentChallenge,
    EnrollmentRejected,
    TelegramEnrollmentStore,
    TelegramPrincipalBinding,
    canonical_telegram_subject,
    issue_execution_identity_for_telegram,
)

__all__ = [
    "AuthenticatedExecutionIdentity",
    "IdentityIssuer",
    "IdentityRejected",
    "AuthenticatedTelegramEvent",
    "EnrollmentChallenge",
    "EnrollmentRejected",
    "TelegramEnrollmentStore",
    "TelegramPrincipalBinding",
    "canonical_telegram_subject",
    "issue_execution_identity_for_telegram",
    "AuthenticatedTelegramUpdate",
    "TelegramWebhookAuthenticator",
    "TelegramWebhookRejected",
]

from .telegram_webhook import (
    AuthenticatedTelegramUpdate,
    TelegramWebhookAuthenticator,
    TelegramWebhookRejected,
)
