from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from atento_host.identity import IdentityIssuer
from atento_host.telegram_enrollment import (
    AuthenticatedTelegramEvent,
    EnrollmentRejected,
    TelegramEnrollmentStore,
    issue_execution_identity_for_telegram,
)


class TelegramEnrollmentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.db = Path(self.tempdir.name) / "host.sqlite3"
        self.now = 1_800_000_000
        self.event = AuthenticatedTelegramEvent(user_id=123456)
        self.store = TelegramEnrollmentStore(
            database_path=self.db,
            enrollment_secret=b"test-only-enrollment-key-at-least-32-bytes",
            allow_bootstrap=True,
            max_ttl_seconds=60,
            max_attempts=2,
            clock=lambda: self.now,
        )

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def enroll_bootstrap_naia(self):
        challenge = self.store.start_enrollment(
            event=self.event,
            role_id="NAIA",
            bootstrap=True,
        )
        return self.store.complete_enrollment(
            event=self.event,
            challenge_id=challenge.challenge_id,
            code=challenge.code,
        )

    def test_bootstrap_is_explicit_and_only_allowed_without_active_principal(self) -> None:
        with self.assertRaisesRegex(EnrollmentRejected, "requires host-authorized principal"):
            self.store.start_enrollment(event=self.event, role_id="NAIA")

        binding = self.enroll_bootstrap_naia()
        self.assertEqual(binding.principal_id, "atento:telegram:123456")

        other = AuthenticatedTelegramEvent(user_id=999)
        with self.assertRaisesRegex(EnrollmentRejected, "bootstrap enrollment is not authorized"):
            self.store.start_enrollment(event=other, role_id="ANNA", bootstrap=True)

    def test_challenge_is_six_digits_and_expires(self) -> None:
        challenge = self.store.start_enrollment(
            event=self.event,
            role_id="NAIA",
            bootstrap=True,
            ttl_seconds=1,
        )
        self.assertEqual(len(challenge.code), 6)
        self.assertTrue(challenge.code.isdigit())
        self.now += 1
        with self.assertRaisesRegex(EnrollmentRejected, "expired"):
            self.store.complete_enrollment(
                event=self.event,
                challenge_id=challenge.challenge_id,
                code=challenge.code,
            )

    def test_wrong_attempts_are_bounded(self) -> None:
        challenge = self.store.start_enrollment(
            event=self.event,
            role_id="NAIA",
            bootstrap=True,
        )
        for _ in range(2):
            with self.assertRaisesRegex(EnrollmentRejected, "code rejected"):
                self.store.complete_enrollment(
                    event=self.event,
                    challenge_id=challenge.challenge_id,
                    code="000000" if challenge.code != "000000" else "000001",
                )
        with self.assertRaisesRegex(EnrollmentRejected, "not pending"):
            self.store.complete_enrollment(
                event=self.event,
                challenge_id=challenge.challenge_id,
                code=challenge.code,
            )

    def test_challenge_cannot_be_consumed_by_another_telegram_subject(self) -> None:
        challenge = self.store.start_enrollment(
            event=self.event,
            role_id="NAIA",
            bootstrap=True,
        )
        with self.assertRaisesRegex(EnrollmentRejected, "not found for subject"):
            self.store.complete_enrollment(
                event=AuthenticatedTelegramEvent(user_id=654321),
                challenge_id=challenge.challenge_id,
                code=challenge.code,
            )

    def test_authenticated_event_maps_to_host_role_and_identity_issuer(self) -> None:
        binding = self.enroll_bootstrap_naia()
        issuer = IdentityIssuer(
            signing_key=b"test-only-signing-key-which-is-32-bytes-minimum",
            role_grants={
                binding.principal_id: {
                    "NAIA": {"calendar.read", "tasks.write"},
                }
            },
            clock=lambda: self.now,
        )

        token = issue_execution_identity_for_telegram(
            event=self.event,
            enrollment_store=self.store,
            issuer=issuer,
            session_id="telegram-session-1",
            run_id="run-1",
            generation=1,
        )
        identity = issuer.verify(
            token,
            expected_role_id="NAIA",
            expected_session_id="telegram-session-1",
            expected_run_id="run-1",
        )
        self.assertEqual(identity.principal_id, binding.principal_id)
        self.assertEqual(identity.role_id, "NAIA")
        self.assertEqual(identity.granted_capability_set, ("calendar.read", "tasks.write"))

    def test_revocation_blocks_future_resolution(self) -> None:
        binding = self.enroll_bootstrap_naia()
        self.store.revoke(
            principal_id=binding.principal_id,
            actor_principal_id=binding.principal_id,
        )
        with self.assertRaisesRegex(EnrollmentRejected, "not enrolled or has been revoked"):
            self.store.resolve(self.event)
        events = self.store.audit_events()
        self.assertEqual(events[-1]["event_type"], "PRINCIPAL_REVOKED")

    def test_non_bootstrap_enrollment_requires_explicit_host_grant(self) -> None:
        first = self.enroll_bootstrap_naia()
        second_db = Path(self.tempdir.name) / "host-with-grants.sqlite3"
        store = TelegramEnrollmentStore(
            database_path=second_db,
            enrollment_secret=b"test-only-enrollment-key-at-least-32-bytes",
            enrollment_grants={first.principal_id: {"ANNA"}},
            allow_bootstrap=True,
            clock=lambda: self.now,
        )
        seed = store.start_enrollment(
            event=self.event,
            role_id="NAIA",
            bootstrap=True,
        )
        store.complete_enrollment(
            event=self.event,
            challenge_id=seed.challenge_id,
            code=seed.code,
        )
        anna = AuthenticatedTelegramEvent(user_id=222222)
        challenge = store.start_enrollment(
            event=anna,
            role_id="ANNA",
            authorized_by_principal_id=first.principal_id,
        )
        binding = store.complete_enrollment(
            event=anna,
            challenge_id=challenge.challenge_id,
            code=challenge.code,
        )
        self.assertEqual(binding.role_id, "ANNA")


if __name__ == "__main__":
    unittest.main()
