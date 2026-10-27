"""Telegram webhook transport authentication for the Atento host boundary.

The Telegram Bot API can attach the configured webhook secret in
X-Telegram-Bot-Api-Secret-Token. This module verifies that secret before
parsing any update identity and only then emits an AuthenticatedTelegramEvent.
"""

from __future__ import annotations

import hmac
import json
import re
from dataclasses import dataclass
from typing import Any

from .telegram_enrollment import AuthenticatedTelegramEvent


_SECRET_RE = re.compile(r"^[A-Za-z0-9_-]{1,256}$")
_MAX_WEBHOOK_BODY_BYTES = 1_048_576


class TelegramWebhookRejected(ValueError):
    """Webhook input failed provider-authentication or schema validation."""


@dataclass(frozen=True)
class AuthenticatedTelegramUpdate:
    event: AuthenticatedTelegramEvent
    update_id: int
    update_kind: str


class TelegramWebhookAuthenticator:
    """Authenticate Telegram webhook requests before trusting update contents."""

    def __init__(
        self,
        *,
        secret_token: str,
        bot_account_id: int,
        max_body_bytes: int = _MAX_WEBHOOK_BODY_BYTES,
    ) -> None:
        if not isinstance(secret_token, str) or not _SECRET_RE.fullmatch(secret_token):
            raise ValueError(
                "secret_token must be 1-256 Telegram-compatible ASCII characters"
            )
        if (
            isinstance(bot_account_id, bool)
            or not isinstance(bot_account_id, int)
            or bot_account_id <= 0
        ):
            raise ValueError("bot_account_id must be a positive integer")
        if (
            isinstance(max_body_bytes, bool)
            or not isinstance(max_body_bytes, int)
            or not 1 <= max_body_bytes <= _MAX_WEBHOOK_BODY_BYTES
        ):
            raise ValueError("max_body_bytes is outside host policy")
        self._secret_token = secret_token
        self._bot_account_id = bot_account_id
        self._max_body_bytes = max_body_bytes

    def authenticate(
        self,
        *,
        secret_token_header: str | None,
        body: bytes,
    ) -> AuthenticatedTelegramUpdate:
        """Verify transport secret, then extract one unambiguous human actor."""

        if not isinstance(secret_token_header, str):
            raise TelegramWebhookRejected("telegram webhook secret is missing")
        if not hmac.compare_digest(
            secret_token_header.encode("utf-8"), self._secret_token.encode("utf-8")
        ):
            raise TelegramWebhookRejected("telegram webhook secret is invalid")

        if not isinstance(body, bytes) or not body or len(body) > self._max_body_bytes:
            raise TelegramWebhookRejected("telegram webhook body is invalid")

        try:
            raw = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise TelegramWebhookRejected("telegram webhook JSON is malformed") from exc

        if not isinstance(raw, dict):
            raise TelegramWebhookRejected("telegram webhook update must be an object")

        update_id = raw.get("update_id")
        if isinstance(update_id, bool) or not isinstance(update_id, int) or update_id < 0:
            raise TelegramWebhookRejected("telegram update_id is invalid")

        update_kind, actor = self._extract_actor(raw)
        user_id = actor.get("id")
        is_bot = actor.get("is_bot")
        if isinstance(user_id, bool) or not isinstance(user_id, int) or user_id <= 0:
            raise TelegramWebhookRejected("telegram actor id is invalid")
        if is_bot is not False:
            raise TelegramWebhookRejected("telegram actor must be a non-bot user")

        return AuthenticatedTelegramUpdate(
            event=AuthenticatedTelegramEvent(
                bot_account_id=self._bot_account_id,
                user_id=user_id,
            ),
            update_id=update_id,
            update_kind=update_kind,
        )

    @staticmethod
    def _extract_actor(raw: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        """Accept only update kinds with a direct Telegram User actor."""

        candidates: list[tuple[str, object]] = []

        for field in ("message", "edited_message"):
            value = raw.get(field)
            if value is not None:
                if not isinstance(value, dict):
                    raise TelegramWebhookRejected(f"telegram {field} is invalid")
                candidates.append((field, value.get("from")))

        callback = raw.get("callback_query")
        if callback is not None:
            if not isinstance(callback, dict):
                raise TelegramWebhookRejected("telegram callback_query is invalid")
            candidates.append(("callback_query", callback.get("from")))

        if len(candidates) != 1:
            raise TelegramWebhookRejected(
                "telegram update must contain exactly one supported actor source"
            )

        kind, actor = candidates[0]
        if not isinstance(actor, dict):
            raise TelegramWebhookRejected("telegram update has no authenticated user actor")
        return kind, actor
