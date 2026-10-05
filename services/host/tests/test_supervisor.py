from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from atento_host.identity import IdentityIssuer
from atento_host.supervisor import HostRunLedger, RunRejected


class HostRunLedgerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.now = 1_800_000_000
        self.principal = "atento:telegram:777000:123456"
        self.issuer = IdentityIssuer(
            signing_key=b"test-only-signing-key-which-is-32-bytes-minimum",
            role_grants={
                self.principal: {
                    "NAIA": {"calendar.read"},
                    "ANNA": {"anna.memory.read"},
                }
            },
            clock=lambda: self.now,
        )
        self.ledger = HostRunLedger(
            database_path=Path(self.tempdir.name) / "runs.sqlite3",
            identity_issuer=self.issuer,
            clock=lambda: self.now,
            max_lease_seconds=60,
        )
        self.token1 = self.token(generation=1)
        self.ledger.create_run(identity_token=self.token1)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def token(
        self,
        *,
        generation: int,
        role_id: str = "NAIA",
        session_id: str = "session-1",
        run_id: str = "run-1",
    ) -> str:
        return self.issuer.issue(
            authenticated_principal_id=self.principal,
            role_id=role_id,
            session_id=session_id,
            run_id=run_id,
            generation=generation,
        )

    def test_happy_path_requires_durable_result_before_ack(self) -> None:
        lease = self.ledger.claim(
            identity_token=self.token1,
            claim_owner="worker-1",
            lease_seconds=30,
        )
        self.ledger.mark_running(identity_token=self.token1, lease=lease)
        with self.assertRaisesRegex(RunRejected, "no durable effect"):
            self.ledger.ack(identity_token=self.token1, lease=lease)

        self.ledger.record_effect(
            identity_token=self.token1,
            lease=lease,
            result_ref="result:sha256:abc",
        )
        record = self.ledger.ack(identity_token=self.token1, lease=lease)
        self.assertEqual(record.state, "ACKED")
        self.assertEqual(record.result_ref, "result:sha256:abc")

    def test_stale_generation_cannot_reclaim_or_ack_after_recovery(self) -> None:
        old_lease = self.ledger.claim(
            identity_token=self.token1,
            claim_owner="worker-old",
            lease_seconds=1,
        )
        self.ledger.mark_running(identity_token=self.token1, lease=old_lease)
        self.now += 2

        recovered = self.ledger.recover_expired(run_id="run-1")
        self.assertEqual(recovered.state, "RETRY_WAIT")
        self.assertEqual(recovered.generation, 2)

        with self.assertRaisesRegex(RunRejected, "current run generation"):
            self.ledger.record_effect(
                identity_token=self.token1,
                lease=old_lease,
                result_ref="stale-result",
            )

        token2 = self.token(generation=2)
        self.ledger.release_retry(identity_token=token2)
        new_lease = self.ledger.claim(
            identity_token=token2,
            claim_owner="worker-new",
            lease_seconds=30,
        )
        self.assertNotEqual(old_lease.claim_id, new_lease.claim_id)

    def test_recovery_requires_expired_lease(self) -> None:
        self.ledger.claim(
            identity_token=self.token1,
            claim_owner="worker-1",
            lease_seconds=30,
        )
        with self.assertRaisesRegex(RunRejected, "has not expired"):
            self.ledger.recover_expired(run_id="run-1")

    def test_wrong_role_or_session_token_is_rejected(self) -> None:
        wrong_role = self.token(generation=1, role_id="ANNA")
        with self.assertRaisesRegex(RunRejected, "identity binding"):
            self.ledger.claim(
                identity_token=wrong_role,
                claim_owner="worker-1",
                lease_seconds=30,
            )

        wrong_session = self.token(generation=1, session_id="other-session")
        with self.assertRaisesRegex(RunRejected, "identity binding"):
            self.ledger.claim(
                identity_token=wrong_session,
                claim_owner="worker-1",
                lease_seconds=30,
            )

    def test_forged_or_tampered_token_is_rejected_before_state_access(self) -> None:
        payload, signature = self.token1.split(".")
        forged = payload + "." + ("A" if signature[-1] != "A" else "B") + signature[1:]
        with self.assertRaisesRegex(RunRejected, "identity token is invalid"):
            self.ledger.claim(
                identity_token=forged,
                claim_owner="worker-1",
                lease_seconds=30,
            )

    def test_duplicate_claim_is_rejected(self) -> None:
        self.ledger.claim(
            identity_token=self.token1,
            claim_owner="worker-1",
            lease_seconds=30,
        )
        with self.assertRaisesRegex(RunRejected, "not claimable"):
            self.ledger.claim(
                identity_token=self.token1,
                claim_owner="worker-2",
                lease_seconds=30,
            )

    def test_cancel_is_terminal_and_rejects_later_claim(self) -> None:
        record = self.ledger.cancel(
            identity_token=self.token1,
            reason="operator cancellation",
        )
        self.assertEqual(record.state, "CANCELLED")
        with self.assertRaisesRegex(RunRejected, "not claimable"):
            self.ledger.claim(
                identity_token=self.token1,
                claim_owner="worker-1",
                lease_seconds=30,
            )

    def test_terminal_failure_is_durable_and_audited(self) -> None:
        record = self.ledger.fail_terminal(
            identity_token=self.token1,
            reason="non-retryable adapter error",
        )
        self.assertEqual(record.state, "FAILED_TERMINAL")
        events = self.ledger.events("run-1")
        self.assertEqual(events[-1]["event_type"], "RUN_FAILED_TERMINAL")

    def test_restart_reopens_same_sqlite_state_and_fences_old_generation(self) -> None:
        lease = self.ledger.claim(
            identity_token=self.token1,
            claim_owner="worker-1",
            lease_seconds=1,
        )
        self.ledger.mark_running(identity_token=self.token1, lease=lease)
        self.now += 2

        reopened = HostRunLedger(
            database_path=Path(self.tempdir.name) / "runs.sqlite3",
            identity_issuer=self.issuer,
            clock=lambda: self.now,
            max_lease_seconds=60,
        )
        record = reopened.get("run-1")
        self.assertEqual(record.state, "RUNNING")
        recovered = reopened.recover_expired(run_id="run-1")
        self.assertEqual(recovered.generation, 2)
        self.assertEqual(recovered.state, "RETRY_WAIT")

        with self.assertRaisesRegex(RunRejected, "current run generation"):
            reopened.mark_running(identity_token=self.token1, lease=lease)


if __name__ == "__main__":
    unittest.main()
