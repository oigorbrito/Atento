from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from atento_host.identity import IdentityIssuer
from atento_host.nanoclaw_adapter import (
    NANOCLAW_FROZEN_PIN,
    NanoClawAdapterRejected,
    NanoClawRuntimeAdapter,
)
from atento_host.supervisor import HostRunLedger


class FakeRunner:
    def __init__(self) -> None:
        self.calls: list[tuple[tuple[str, ...], Path]] = []
        self.task_status = "pending"
        self.pin = NANOCLAW_FROZEN_PIN

    def __call__(self, argv, cwd):
        args = tuple(argv)
        self.calls.append((args, cwd))
        if args == ("git", "rev-parse", "HEAD"):
            return subprocess.CompletedProcess(args, 0, self.pin + "\n", "")
        if "tasks" in args and "create" in args:
            frame = {
                "id": "req-1",
                "ok": True,
                "data": {
                    "series_id": "atento-run-1-a1b2",
                    "row_id": "t-a1b2",
                    "status": "pending",
                },
            }
            return subprocess.CompletedProcess(args, 0, json.dumps(frame), "")
        if "tasks" in args and "get" in args:
            frame = {
                "id": "req-2",
                "ok": True,
                "data": {
                    "series_id": "atento-run-1-a1b2",
                    "row_id": "t-a1b2",
                    "status": self.task_status,
                },
            }
            return subprocess.CompletedProcess(args, 0, json.dumps(frame), "")
        return subprocess.CompletedProcess(args, 1, "", "unexpected command")


class NanoClawRuntimeAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.now = 1_800_000_000
        self.principal = "atento:telegram:777000:123456"
        self.issuer = IdentityIssuer(
            signing_key=b"test-only-signing-key-which-is-32-bytes-minimum",
            role_grants={self.principal: {"NAIA": {"calendar.read"}}},
            clock=lambda: self.now,
        )
        self.token = self.issuer.issue(
            authenticated_principal_id=self.principal,
            role_id="NAIA",
            session_id="session-1",
            run_id="run-1",
            generation=1,
        )
        self.ledger = HostRunLedger(
            database_path=Path(self.tempdir.name) / "runs.sqlite3",
            identity_issuer=self.issuer,
            clock=lambda: self.now,
        )
        self.ledger.create_run(identity_token=self.token)
        self.lease = self.ledger.claim(
            identity_token=self.token,
            claim_owner="adapter-worker",
            lease_seconds=60,
        )
        self.runner = FakeRunner()
        self.adapter = NanoClawRuntimeAdapter(
            nanoclaw_root=Path(self.tempdir.name) / "nanoclaw",
            role_to_group={"NAIA": "group-naia"},
            identity_issuer=self.issuer,
            ledger=self.ledger,
            runner=self.runner,
        )

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_dispatch_requires_exact_frozen_pin_and_uses_cross_platform_cli(self) -> None:
        dispatch = self.adapter.dispatch(
            identity_token=self.token,
            lease=self.lease,
            task_prompt="Process the Atento run input.",
        )
        record = self.ledger.get("run-1")
        self.assertEqual(record.state, "DISPATCHED")
        self.assertEqual(dispatch.agent_group_id, "group-naia")
        cli_call = next(args for args, _ in self.runner.calls if "tasks" in args)
        self.assertEqual(cli_call[:4], ("pnpm", "exec", "tsx", "src/cli/client.ts"))
        self.assertNotIn("shell", cli_call)

    def test_pin_mismatch_blocks_before_runtime_dispatch(self) -> None:
        self.runner.pin = "0" * 40
        with self.assertRaisesRegex(NanoClawAdapterRejected, "pin mismatch"):
            self.adapter.dispatch(
                identity_token=self.token,
                lease=self.lease,
                task_prompt="blocked",
            )
        self.assertEqual(self.ledger.get("run-1").state, "CLAIMED")
        self.assertFalse(any("tasks" in args for args, _ in self.runner.calls))

    def test_role_mapping_is_host_owned(self) -> None:
        adapter = NanoClawRuntimeAdapter(
            nanoclaw_root=Path(self.tempdir.name) / "nanoclaw",
            role_to_group={"ANNA": "group-anna"},
            identity_issuer=self.issuer,
            ledger=self.ledger,
            runner=self.runner,
        )
        with self.assertRaisesRegex(NanoClawAdapterRejected, "no NanoClaw group mapping"):
            adapter.dispatch(
                identity_token=self.token,
                lease=self.lease,
                task_prompt="blocked",
            )

    def test_completed_task_records_effect_then_acks(self) -> None:
        dispatch = self.adapter.dispatch(
            identity_token=self.token,
            lease=self.lease,
            task_prompt="do work",
        )
        self.runner.task_status = "completed"
        status = self.adapter.observe(
            identity_token=self.token,
            lease=self.lease,
            dispatch=dispatch,
        )
        self.assertEqual(status, "completed")
        self.assertEqual(self.ledger.get("run-1").state, "ACKED")

    def test_failed_task_becomes_terminal_failure(self) -> None:
        dispatch = self.adapter.dispatch(
            identity_token=self.token,
            lease=self.lease,
            task_prompt="do work",
        )
        self.runner.task_status = "failed"
        status = self.adapter.observe(
            identity_token=self.token,
            lease=self.lease,
            dispatch=dispatch,
        )
        self.assertEqual(status, "failed")
        self.assertEqual(self.ledger.get("run-1").state, "FAILED_TERMINAL")

    def test_monitor_loss_after_dispatch_recovers_to_reconcile_required(self) -> None:
        self.adapter.dispatch(
            identity_token=self.token,
            lease=self.lease,
            task_prompt="do work",
        )
        self.now += 61
        record = self.ledger.recover_expired(run_id="run-1")
        self.assertEqual(record.state, "RECONCILE_REQUIRED")
        self.assertEqual(record.generation, 2)


if __name__ == "__main__":
    unittest.main()
