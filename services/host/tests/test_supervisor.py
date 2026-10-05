from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from atento_host.identity import AuthenticatedExecutionIdentity
from atento_host.supervisor import HostRunLedger, RunRejected


def identity(*, generation: int = 1, role_id: str = "NAIA") -> AuthenticatedExecutionIdentity:
    return AuthenticatedExecutionIdentity(
        principal_id="atento:telegram:777000:123456",
        role_id=role_id,
        session_id="session-1",
        run_id="run-1",
        generation=generation,
        granted_capability_set=("calendar.read",),
        issued_at=1_800_000_000,
        expires_at=1_800_000_300,
        issuer="atento-host-control-plane",
        audience="atento-runtime-adapter",
    )


class HostRunLedgerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.now = 1_800_000_000
        self.ledger = HostRunLedger(
            database_path=Path(self.tempdir.name) / "runs.sqlite3",
            clock=lambda: self.now,
            max_lease_seconds=60,
        )
        self.id1 = identity()
        self.ledger.create_run(identity=self.id1)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_happy_path_requires_durable_result_before_ack(self) -> None:
        lease = self.ledger.claim(
            identity=self.id1,
            claim_owner="worker-1",
            lease_seconds=30,
        )
        self.ledger.mark_running(identity=self.id1, lease=lease)
        with self.assertRaisesRegex(RunRejected, "no durable effect"):
            self.ledger.ack(identity=self.id1, lease=lease)

        self.ledger.record_effect(
            identity=self.id1,
            lease=lease,
            result_ref="result:sha256:abc",
        )
        record = self.ledger.ack(identity=self.id1, lease=lease)
        self.assertEqual(record.state, "ACKED")
        self.assertEqual(record.result_ref, "result:sha256:abc")

    def test_stale_generation_cannot_reclaim_or_ack_after_recovery(self) -> None:
        old_lease = self.ledger.claim(
            identity=self.id1,
            claim_owner="worker-old",
            lease_seconds=1,
        )
        self.ledger.mark_running(identity=self.id1, lease=old_lease)
        self.now += 2

        recovered = self.ledger.recover_expired(run_id="run-1")
        self.assertEqual(recovered.state, "RETRY_WAIT")
        self.assertEqual(recovered.generation, 2)

        with self.assertRaisesRegex(RunRejected, "current run generation"):
            self.ledger.record_effect(
                identity=self.id1,
                lease=old_lease,
                result_ref="stale-result",
            )

        fresh = identity(generation=2)
        self.ledger.release_retry(identity=fresh)
        new_lease = self.ledger.claim(
            identity=fresh,
            claim_owner="worker-new",
            lease_seconds=30,
        )
        self.assertNotEqual(old_lease.claim_id, new_lease.claim_id)

    def test_recovery_requires_expired_lease(self) -> None:
        self.ledger.claim(
            identity=self.id1,
            claim_owner="worker-1",
            lease_seconds=30,
        )
        with self.assertRaisesRegex(RunRejected, "has not expired"):
            self.ledger.recover_expired(run_id="run-1")

    def test_wrong_role_or_session_identity_is_rejected(self) -> None:
        wrong_role = identity(role_id="ANNA")
        with self.assertRaisesRegex(RunRejected, "identity binding"):
            self.ledger.claim(
                identity=wrong_role,
                claim_owner="worker-1",
                lease_seconds=30,
            )

        wrong_session = AuthenticatedExecutionIdentity(
            principal_id=self.id1.principal_id,
            role_id=self.id1.role_id,
            session_id="other-session",
            run_id=self.id1.run_id,
            generation=1,
            granted_capability_set=self.id1.granted_capability_set,
            issued_at=self.id1.issued_at,
            expires_at=self.id1.expires_at,
            issuer=self.id1.issuer,
            audience=self.id1.audience,
        )
        with self.assertRaisesRegex(RunRejected, "identity binding"):
            self.ledger.claim(
                identity=wrong_session,
                claim_owner="worker-1",
                lease_seconds=30,
            )

    def test_duplicate_claim_is_rejected(self) -> None:
        self.ledger.claim(
            identity=self.id1,
            claim_owner="worker-1",
            lease_seconds=30,
        )
        with self.assertRaisesRegex(RunRejected, "not claimable"):
            self.ledger.claim(
                identity=self.id1,
                claim_owner="worker-2",
                lease_seconds=30,
            )

    def test_cancel_is_terminal_and_rejects_later_claim(self) -> None:
        record = self.ledger.cancel(identity=self.id1, reason="operator cancellation")
        self.assertEqual(record.state, "CANCELLED")
        with self.assertRaisesRegex(RunRejected, "not claimable"):
            self.ledger.claim(
                identity=self.id1,
                claim_owner="worker-1",
                lease_seconds=30,
            )

    def test_terminal_failure_is_durable_and_audited(self) -> None:
        record = self.ledger.fail_terminal(
            identity=self.id1,
            reason="non-retryable adapter error",
        )
        self.assertEqual(record.state, "FAILED_TERMINAL")
        events = self.ledger.events("run-1")
        self.assertEqual(events[-1]["event_type"], "RUN_FAILED_TERMINAL")

    def test_restart_reopens_same_sqlite_state(self) -> None:
        lease = self.ledger.claim(
            identity=self.id1,
            claim_owner="worker-1",
            lease_seconds=1,
        )
        self.ledger.mark_running(identity=self.id1, lease=lease)
        self.now += 2

        reopened = HostRunLedger(
            database_path=Path(self.tempdir.name) / "runs.sqlite3",
            clock=lambda: self.now,
            max_lease_seconds=60,
        )
        record = reopened.get("run-1")
        self.assertEqual(record.state, "RUNNING")
        recovered = reopened.recover_expired(run_id="run-1")
        self.assertEqual(recovered.generation, 2)
        self.assertEqual(recovered.state, "RETRY_WAIT")


if __name__ == "__main__":
    unittest.main()
