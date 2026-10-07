"""Adapter from the Atento Host Supervisor to the frozen NanoClaw runtime.

The adapter uses only seams verified at the frozen NanoClaw pin:
- package script entry via pnpm/tsx;
- ncl CLI over the host-owned 0600 Unix socket;
- one-shot task creation and task status reads.

It never imports NanoClaw's owner/pairing authority. Dispatch is allowed only
from an explicitly approved runtime head descended from the frozen upstream pin.
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Mapping, Sequence

from .identity import IdentityIssuer, IdentityRejected
from .supervisor import ClaimLease, HostRunLedger


NANOCLAW_FROZEN_PIN = "d7175d0dee42a1130c17ced09220b983257696a4"


class NanoClawAdapterRejected(ValueError):
    """The frozen runtime adapter failed closed."""


@dataclass(frozen=True)
class NanoClawDispatch:
    run_id: str
    generation: int
    role_id: str
    agent_group_id: str
    series_id: str
    row_id: str
    status: str


CommandRunner = Callable[[Sequence[str], Path], subprocess.CompletedProcess[str]]


def _default_runner(argv: Sequence[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(argv),
        cwd=str(cwd),
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
        shell=False,
    )


class NanoClawRuntimeAdapter:
    """Dispatch host-authorized runs through the frozen NanoClaw CLI seam."""

    def __init__(
        self,
        *,
        nanoclaw_root: str | Path,
        role_to_group: Mapping[str, str],
        identity_issuer: IdentityIssuer,
        ledger: HostRunLedger,
        runner: CommandRunner = _default_runner,
        upstream_base_pin: str = NANOCLAW_FROZEN_PIN,
        approved_runtime_head: str = NANOCLAW_FROZEN_PIN,
    ) -> None:
        root = Path(nanoclaw_root)
        if not root:
            raise ValueError("nanoclaw_root is required")
        for value, field in (
            (upstream_base_pin, "upstream_base_pin"),
            (approved_runtime_head, "approved_runtime_head"),
        ):
            if not isinstance(value, str) or len(value) != 40:
                raise ValueError(f"{field} must be a full commit SHA")
        if not role_to_group:
            raise ValueError("role_to_group is required")
        normalized: dict[str, str] = {}
        for role, group in role_to_group.items():
            if role not in {"NAIA", "ANNA", "APOLLO"}:
                raise ValueError(f"unsupported role mapping: {role}")
            if not isinstance(group, str) or not group or group.strip() != group:
                raise ValueError("NanoClaw group ids must be canonical strings")
            normalized[role] = group

        self._root = root
        self._role_to_group = normalized
        self._issuer = identity_issuer
        self._ledger = ledger
        self._runner = runner
        self._upstream_base_pin = upstream_base_pin
        self._approved_runtime_head = approved_runtime_head

    def _run(self, *argv: str) -> subprocess.CompletedProcess[str]:
        try:
            result = self._runner(argv, self._root)
        except (OSError, subprocess.SubprocessError) as exc:
            raise NanoClawAdapterRejected("runtime command could not be executed") from exc
        return result

    def verify_frozen_pin(self) -> None:
        result = self._run("git", "rev-parse", "HEAD")
        if result.returncode != 0:
            raise NanoClawAdapterRejected("cannot resolve NanoClaw checkout HEAD")
        actual = result.stdout.strip()
        if actual != self._approved_runtime_head:
            raise NanoClawAdapterRejected(
                "NanoClaw runtime head mismatch: "
                f"expected {self._approved_runtime_head}, got {actual}"
            )
        ancestry = self._run(
            "git",
            "merge-base",
            "--is-ancestor",
            self._upstream_base_pin,
            self._approved_runtime_head,
        )
        if ancestry.returncode != 0:
            raise NanoClawAdapterRejected(
                "approved NanoClaw runtime head is not descended from frozen upstream pin"
            )

    def _verify_identity_for_lease(
        self,
        *,
        identity_token: str,
        lease: ClaimLease,
    ):
        try:
            identity = self._issuer.verify(
                identity_token,
                expected_run_id=lease.run_id,
                expected_generation=lease.generation,
            )
        except IdentityRejected as exc:
            raise NanoClawAdapterRejected("execution identity is invalid for NanoClaw dispatch") from exc

        current = self._ledger.get(lease.run_id)
        if (
            current.generation != identity.generation
            or current.principal_id != identity.principal_id
            or current.role_id != identity.role_id
            or current.session_id != identity.session_id
        ):
            raise NanoClawAdapterRejected("execution identity does not match current host run")
        group = self._role_to_group.get(identity.role_id)
        if group is None:
            raise NanoClawAdapterRejected("role has no NanoClaw group mapping")
        return identity, group

    def _ncl_json(self, *args: str) -> object:
        result = self._run(
            "pnpm",
            "exec",
            "tsx",
            "src/cli/client.ts",
            *args,
            "--json",
        )
        if result.returncode != 0:
            raise NanoClawAdapterRejected(
                "NanoClaw CLI command failed without an accepted host result"
            )
        try:
            frame = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise NanoClawAdapterRejected("NanoClaw CLI returned malformed JSON") from exc
        if not isinstance(frame, dict) or frame.get("ok") is not True:
            raise NanoClawAdapterRejected("NanoClaw CLI rejected the command")
        if "data" not in frame:
            raise NanoClawAdapterRejected("NanoClaw CLI response is missing data")
        return frame["data"]

    def dispatch(
        self,
        *,
        identity_token: str,
        lease: ClaimLease,
        task_prompt: str,
    ) -> NanoClawDispatch:
        if not isinstance(task_prompt, str) or not task_prompt.strip():
            raise NanoClawAdapterRejected("task_prompt is required")
        if len(task_prompt) > 100_000:
            raise NanoClawAdapterRejected("task_prompt exceeds adapter limit")

        self.verify_frozen_pin()
        identity, group = self._verify_identity_for_lease(
            identity_token=identity_token,
            lease=lease,
        )

        current = self._ledger.get(identity.run_id)
        if current.state == "CLAIMED":
            self._ledger.mark_running(identity_token=identity_token, lease=lease)
        elif current.state != "RUNNING":
            raise NanoClawAdapterRejected("host run is not dispatchable")

        intent_ref = (
            f"nanoclaw:{self._approved_runtime_head}:intent:"
            f"{identity.run_id}:generation:{identity.generation}"
        )
        self._ledger.mark_dispatching(
            identity_token=identity_token,
            lease=lease,
            intent_ref=intent_ref,
        )

        process_after = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        data = self._ncl_json(
            "tasks",
            "create",
            "--name",
            f"atento-{identity.run_id}",
            "--group",
            group,
            "--prompt",
            task_prompt,
            "--process-after",
            process_after,
        )
        if not isinstance(data, dict):
            raise NanoClawAdapterRejected("NanoClaw task creation returned invalid data")

        series_id = data.get("series_id")
        row_id = data.get("row_id")
        status = data.get("status")
        if not all(isinstance(v, str) and v for v in (series_id, row_id, status)):
            raise NanoClawAdapterRejected("NanoClaw task creation response is incomplete")

        dispatch_ref = f"nanoclaw:{self._approved_runtime_head}:task:{series_id}:row:{row_id}"
        self._ledger.mark_dispatched(
            identity_token=identity_token,
            lease=lease,
            dispatch_ref=dispatch_ref,
        )
        return NanoClawDispatch(
            run_id=identity.run_id,
            generation=identity.generation,
            role_id=identity.role_id,
            agent_group_id=group,
            series_id=series_id,
            row_id=row_id,
            status=status,
        )

    def observe(
        self,
        *,
        identity_token: str,
        lease: ClaimLease,
        dispatch: NanoClawDispatch,
    ) -> str:
        """Observe one task and translate terminal status into host state."""

        self.verify_frozen_pin()
        identity, group = self._verify_identity_for_lease(
            identity_token=identity_token,
            lease=lease,
        )
        if (
            dispatch.run_id != identity.run_id
            or dispatch.generation != identity.generation
            or dispatch.role_id != identity.role_id
            or dispatch.agent_group_id != group
        ):
            raise NanoClawAdapterRejected("dispatch reference does not match current host authority")

        data = self._ncl_json(
            "tasks",
            "get",
            dispatch.series_id,
            "--group",
            group,
        )
        if not isinstance(data, dict):
            raise NanoClawAdapterRejected("NanoClaw task status returned invalid data")

        status = data.get("status")
        if not isinstance(status, str) or not status:
            raise NanoClawAdapterRejected("NanoClaw task status is missing")

        if status in {"pending", "paused", "processing"}:
            return status

        if status == "completed":
            completed_runs = data.get("completed_runs")
            failed_runs = data.get("failed_runs")
            recent_log = data.get("recent_log")
            if (
                not isinstance(completed_runs, int)
                or completed_runs < 1
                or not isinstance(failed_runs, int)
                or failed_runs != 0
                or not isinstance(recent_log, list)
                or not any(isinstance(line, str) and line.strip() for line in recent_log)
            ):
                raise NanoClawAdapterRejected(
                    "NanoClaw completed task lacks successful run evidence"
                )
            result_ref = (
                f"nanoclaw:{self._approved_runtime_head}:task:{dispatch.series_id}:"
                f"row:{dispatch.row_id}:completed:runs:{completed_runs}"
            )
            self._ledger.record_effect(
                identity_token=identity_token,
                lease=lease,
                result_ref=result_ref,
            )
            self._ledger.ack(identity_token=identity_token, lease=lease)
            return status

        if status in {"failed", "cancelled"}:
            self._ledger.fail_terminal(
                identity_token=identity_token,
                reason=f"NanoClaw task reached terminal state: {status}",
            )
            return status

        raise NanoClawAdapterRejected(f"unsupported NanoClaw task status: {status}")
