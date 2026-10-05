from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from atento_host.identity import IdentityIssuer
from atento_host.telegram_enrollment import (
    TelegramEnrollmentStore,
    issue_execution_identity_for_telegram,
)
from atento_host.telegram_webhook import TelegramWebhookAuthenticator


class TelegramIdentityChainTests(unittest.TestCase):
    def test_authenticated_webhook_reaches_host_issued_role_identity(self) -> None:
        now = 1_800_000_000
        secret = "Atento_Webhook-Secret_2026"
        authenticator = TelegramWebhookAuthenticator(
            secret_token=secret,
            bot_account_id=777000,
        )
        body = json.dumps(
            {
                "update_id": 2001,
                "message": {
                    "message_id": 42,
                    "from": {"id": 123456, "is_bot": False},
                },
            },
            separators=(",", ":"),
        ).encode("utf-8")

        authenticated = authenticator.authenticate(
            secret_token_header=secret,
            body=body,
        )

        with tempfile.TemporaryDirectory() as tempdir:
            store = TelegramEnrollmentStore(
                database_path=Path(tempdir) / "host.sqlite3",
                enrollment_secret=b"test-only-enrollment-key-at-least-32-bytes",
                allow_bootstrap=True,
                clock=lambda: now,
            )
            challenge = store.start_enrollment(
                event=authenticated.event,
                role_id="NAIA",
                bootstrap=True,
            )
            binding = store.complete_enrollment(
                event=authenticated.event,
                challenge_id=challenge.challenge_id,
                code=challenge.code,
            )

            issuer = IdentityIssuer(
                signing_key=b"test-only-signing-key-which-is-32-bytes-minimum",
                role_grants={
                    binding.principal_id: {
                        "NAIA": {"calendar.read", "tasks.write"},
                    }
                },
                clock=lambda: now,
            )
            token = issue_execution_identity_for_telegram(
                event=authenticated.event,
                enrollment_store=store,
                issuer=issuer,
                session_id="telegram-session-2001",
                run_id="run-2001",
                generation=1,
            )
            identity = issuer.verify(
                token,
                expected_role_id="NAIA",
                expected_session_id="telegram-session-2001",
                expected_run_id="run-2001",
                expected_generation=1,
            )

        self.assertEqual(binding.provider_subject, "telegram:bot:777000:user:123456")
        self.assertEqual(identity.principal_id, "atento:telegram:777000:123456")
        self.assertEqual(identity.role_id, "NAIA")
        self.assertEqual(identity.granted_capability_set, ("calendar.read", "tasks.write"))


if __name__ == "__main__":
    unittest.main()
