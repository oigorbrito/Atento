from __future__ import annotations

import json
import unittest

from atento_host.telegram_webhook import (
    TelegramWebhookAuthenticator,
    TelegramWebhookRejected,
)


class TelegramWebhookAuthenticatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.secret = "Atento_Webhook-Secret_2026"
        self.auth = TelegramWebhookAuthenticator(secret_token=self.secret, bot_account_id=777000)

    def body(self, update: dict[str, object]) -> bytes:
        return json.dumps(update, separators=(",", ":")).encode("utf-8")

    def test_valid_message_authenticates_before_emitting_user_event(self) -> None:
        result = self.auth.authenticate(
            secret_token_header=self.secret,
            body=self.body(
                {
                    "update_id": 1001,
                    "message": {
                        "message_id": 10,
                        "from": {"id": 123456, "is_bot": False, "first_name": "Igor"},
                    },
                }
            ),
        )
        self.assertEqual(result.event.bot_account_id, 777000)
        self.assertEqual(result.event.user_id, 123456)
        self.assertEqual(result.update_id, 1001)
        self.assertEqual(result.update_kind, "message")

    def test_missing_or_wrong_secret_fails_before_body_identity_is_trusted(self) -> None:
        attacker_body = self.body(
            {
                "update_id": 1002,
                "message": {"from": {"id": 999999, "is_bot": False}},
            }
        )
        for supplied in (None, "", "wrong-secret"):
            with self.subTest(supplied=supplied), self.assertRaises(TelegramWebhookRejected):
                self.auth.authenticate(
                    secret_token_header=supplied,
                    body=attacker_body,
                )

    def test_callback_query_actor_is_supported(self) -> None:
        result = self.auth.authenticate(
            secret_token_header=self.secret,
            body=self.body(
                {
                    "update_id": 1003,
                    "callback_query": {
                        "id": "cb-1",
                        "from": {"id": 222222, "is_bot": False},
                    },
                }
            ),
        )
        self.assertEqual(result.event.user_id, 222222)
        self.assertEqual(result.update_kind, "callback_query")

    def test_edited_message_actor_is_supported(self) -> None:
        result = self.auth.authenticate(
            secret_token_header=self.secret,
            body=self.body(
                {
                    "update_id": 1004,
                    "edited_message": {
                        "message_id": 11,
                        "from": {"id": 333333, "is_bot": False},
                    },
                }
            ),
        )
        self.assertEqual(result.event.user_id, 333333)
        self.assertEqual(result.update_kind, "edited_message")

    def test_unsupported_or_ambiguous_update_fails_closed(self) -> None:
        unsupported = {
            "update_id": 1005,
            "channel_post": {
                "message_id": 12,
                "sender_chat": {"id": -100123},
            },
        }
        ambiguous = {
            "update_id": 1006,
            "message": {"from": {"id": 1, "is_bot": False}},
            "callback_query": {"from": {"id": 2, "is_bot": False}},
        }
        for update in (unsupported, ambiguous):
            with self.subTest(update=update), self.assertRaisesRegex(
                TelegramWebhookRejected,
                "exactly one supported actor source",
            ):
                self.auth.authenticate(
                    secret_token_header=self.secret,
                    body=self.body(update),
                )

    def test_missing_from_or_bot_actor_is_rejected(self) -> None:
        cases = (
            {"update_id": 1007, "message": {"message_id": 13}},
            {
                "update_id": 1008,
                "message": {"from": {"id": 123, "is_bot": True}},
            },
        )
        for update in cases:
            with self.subTest(update=update), self.assertRaises(TelegramWebhookRejected):
                self.auth.authenticate(
                    secret_token_header=self.secret,
                    body=self.body(update),
                )

    def test_invalid_json_update_id_and_oversized_body_fail_closed(self) -> None:
        bad_inputs = (
            b"{",
            self.body({"update_id": True, "message": {"from": {"id": 1, "is_bot": False}}}),
            b"x" * (1_048_576 + 1),
        )
        for body in bad_inputs:
            with self.subTest(size=len(body)), self.assertRaises(TelegramWebhookRejected):
                self.auth.authenticate(
                    secret_token_header=self.secret,
                    body=body,
                )

    def test_secret_configuration_matches_telegram_character_contract(self) -> None:
        TelegramWebhookAuthenticator(secret_token="A-z_0-9", bot_account_id=777000)
        for secret in ("", "has space", "bad!", "x" * 257):
            with self.subTest(secret=secret[:12]), self.assertRaises(ValueError):
                TelegramWebhookAuthenticator(secret_token=secret, bot_account_id=777000)


if __name__ == "__main__":
    unittest.main()
