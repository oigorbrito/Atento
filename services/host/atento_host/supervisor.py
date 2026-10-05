"""Durable host-owned run ledger and lifecycle supervisor.

This slice enforces the lifecycle invariants from the Atento host/runtime
contract with SQLite transactions and generation-bound identities. It does not
execute agent processes; it owns run authority, claims, stale-worker rejection,
recovery eligibility, cancellation and terminal acknowledgement.
"""

from __future__ import annotations

import sqlite3
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from .identity import AuthenticatedExecutionIdentity, IdentityIssuer, IdentityRejected


_NONTERMINAL = frozenset(
    {"ACCEPTED", "CLAIMED", "RUNNING", "EFFECT_PENDING", "RETRY_WAIT", "RECONCILE_REQUIRED"}
)
_TERMINAL = frozenset({"ACKED", "FAILED_TERMINAL", "CANCELLED"})


class RunRejected(ValueError):
    """A run lifecycle operation violated host authority or state."""


@dataclass(frozen=True)
class ClaimLease:
    run_id: str
    generation: int
    claim_id: str
    claim_owner: str
    lease_expires_at: int


@dataclass(frozen=True)
class RunRecord:
    run_id: str
    generation: int
    state: str
    principal_id: str
    role_id: str
    session_id: str
    attempts: int
    claim_id: str | None
    claim_owner: str | None
    lease_expires_at: int | None
    result_ref: str | None
    terminal_reason: str | None
    updated_at: int


class HostRunLedger:
    """SQLite-backed run authority with generation and claim fencing."""

    def __init__(
        self,
        *,
        database_path: str | Path,
        identity_issuer: IdentityIssuer,
        clock: Callable[[], float] = time.time,
        max_lease_seconds: int = 300,
    ) -> None:
        if (
            isinstance(max_lease_seconds, bool)
            or not isinstance(max_lease_seconds, int)
            or not 1 <= max_lease_seconds <= 3600
        ):
            raise ValueError("max_lease_seconds is outside host policy")
        if not isinstance(identity_issuer, IdentityIssuer):
            raise ValueError("identity_issuer is required")
        self._database_path = str(database_path)
        self._identity_issuer = identity_issuer
        self._clock = clock
        self._max_lease_seconds = max_lease_seconds
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._database_path, timeout=5.0)
        conn.row_factory = sqlite3.Row
        return conn

    def _initialize(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS host_runs (
                    run_id TEXT PRIMARY KEY,
                    generation INTEGER NOT NULL,
                    state TEXT NOT NULL,
                    principal_id TEXT NOT NULL,
                    role_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    attempts INTEGER NOT NULL,
                    claim_id TEXT,
                    claim_owner TEXT,
                    lease_expires_at INTEGER,
                    result_ref TEXT,
                    terminal_reason TEXT,
                    created_at INTEGER NOT NULL,
                    updated_at INTEGER NOT NULL
                );

                CREATE TABLE IF NOT EXISTS host_run_events (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id TEXT NOT NULL,
                    generation INTEGER NOT NULL,
                    occurred_at INTEGER NOT NULL,
                    event_type TEXT NOT NULL,
                    state TEXT NOT NULL,
                    claim_id TEXT,
                    detail TEXT NOT NULL
                );
                """
            )

    @staticmethod
    def _require_text(value: object, field: str) -> str:
        if not isinstance(value, str) or not value or value.strip() != value:
            raise RunRejected(f"{field} must be a non-empty canonical string")
        if len(value) > 512:
            raise RunRejected(f"{field} exceeds the host limit")
        return value

    def _event(
        self,
        conn: sqlite3.Connection,
        *,
        run_id: str,
        generation: int,
        event_type: str,
        state: str,
        detail: str,
        claim_id: str | None = None,
    ) -> None:
        conn.execute(
            """
            INSERT INTO host_run_events
            (run_id, generation, occurred_at, event_type, state, claim_id, detail)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                run_id,
                generation,
                int(self._clock()),
                event_type,
                state,
                claim_id,
                detail,
            ),
        )

    @staticmethod
    def _identity_matches_row(
        identity: AuthenticatedExecutionIdentity,
        row: sqlite3.Row,
    ) -> bool:
        return (
            identity.run_id == row["run_id"]
            and identity.generation == row["generation"]
            and identity.principal_id == row["principal_id"]
            and identity.role_id == row["role_id"]
            and identity.session_id == row["session_id"]
        )

    def _verify_identity(self, token: str) -> AuthenticatedExecutionIdentity:
        try:
            return self._identity_issuer.verify(token)
        except IdentityRejected as exc:
            raise RunRejected("execution identity token is invalid") from exc

    def create_run(self, *, identity_token: str) -> RunRecord:
        identity = self._verify_identity(identity_token)
        if identity.generation != 1:
            raise RunRejected("new run must begin at generation 1")
        now = int(self._clock())
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            try:
                conn.execute(
                    """
                    INSERT INTO host_runs
                    (run_id, generation, state, principal_id, role_id, session_id,
                     attempts, claim_id, claim_owner, lease_expires_at, result_ref,
                     terminal_reason, created_at, updated_at)
                    VALUES (?, 1, 'ACCEPTED', ?, ?, ?, 0, NULL, NULL, NULL, NULL, NULL, ?, ?)
                    """,
                    (
                        identity.run_id,
                        identity.principal_id,
                        identity.role_id,
                        identity.session_id,
                        now,
                        now,
                    ),
                )
            except sqlite3.IntegrityError as exc:
                raise RunRejected("run_id already exists") from exc
            self._event(
                conn,
                run_id=identity.run_id,
                generation=1,
                event_type="RUN_ACCEPTED",
                state="ACCEPTED",
                detail="run created under verified host identity",
            )
        return self.get(identity.run_id)

    def claim(
        self,
        *,
        identity_token: str,
        claim_owner: str,
        lease_seconds: int,
    ) -> ClaimLease:
        identity = self._verify_identity(identity_token)
        owner = self._require_text(claim_owner, "claim_owner")
        if (
            isinstance(lease_seconds, bool)
            or not isinstance(lease_seconds, int)
            or not 1 <= lease_seconds <= self._max_lease_seconds
        ):
            raise RunRejected("lease_seconds is outside host policy")
        now = int(self._clock())
        claim_id = uuid.uuid4().hex
        lease_expires = now + lease_seconds

        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute(
                "SELECT * FROM host_runs WHERE run_id = ?",
                (identity.run_id,),
            ).fetchone()
            if row is None:
                raise RunRejected("run not found")
            if not self._identity_matches_row(identity, row):
                raise RunRejected("identity binding does not match current run generation")
            if row["state"] != "ACCEPTED":
                raise RunRejected("run is not claimable")
            changed = conn.execute(
                """
                UPDATE host_runs
                SET state = 'CLAIMED', attempts = attempts + 1,
                    claim_id = ?, claim_owner = ?, lease_expires_at = ?, updated_at = ?
                WHERE run_id = ? AND generation = ? AND state = 'ACCEPTED'
                """,
                (
                    claim_id,
                    owner,
                    lease_expires,
                    now,
                    identity.run_id,
                    identity.generation,
                ),
            )
            if changed.rowcount != 1:
                raise RunRejected("claim lost concurrent state transition")
            self._event(
                conn,
                run_id=identity.run_id,
                generation=identity.generation,
                event_type="RUN_CLAIMED",
                state="CLAIMED",
                claim_id=claim_id,
                detail=f"claim_owner={owner};lease_expires_at={lease_expires}",
            )

        return ClaimLease(
            run_id=identity.run_id,
            generation=identity.generation,
            claim_id=claim_id,
            claim_owner=owner,
            lease_expires_at=lease_expires,
        )

    def mark_running(
        self,
        *,
        identity_token: str,
        lease: ClaimLease,
    ) -> RunRecord:
        identity = self._verify_identity(identity_token)
        return self._claim_transition(
            identity=identity,
            lease=lease,
            expected_state="CLAIMED",
            next_state="RUNNING",
            event_type="RUN_STARTED",
            detail="worker began execution",
        )

    def record_effect(
        self,
        *,
        identity_token: str,
        lease: ClaimLease,
        result_ref: str,
    ) -> RunRecord:
        identity = self._verify_identity(identity_token)
        result = self._require_text(result_ref, "result_ref")
        now = int(self._clock())
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            row = self._require_live_claim(conn, identity=identity, lease=lease)
            if row["state"] != "RUNNING":
                raise RunRejected("run is not ready to record effect")
            changed = conn.execute(
                """
                UPDATE host_runs
                SET state = 'EFFECT_PENDING', result_ref = ?, updated_at = ?
                WHERE run_id = ? AND generation = ? AND state = 'RUNNING'
                  AND claim_id = ?
                """,
                (result, now, identity.run_id, identity.generation, lease.claim_id),
            )
            if changed.rowcount != 1:
                raise RunRejected("effect record lost concurrent state transition")
            self._event(
                conn,
                run_id=identity.run_id,
                generation=identity.generation,
                event_type="EFFECT_RECORDED",
                state="EFFECT_PENDING",
                claim_id=lease.claim_id,
                detail=f"result_ref={result}",
            )
        return self.get(identity.run_id)

    def ack(
        self,
        *,
        identity_token: str,
        lease: ClaimLease,
    ) -> RunRecord:
        identity = self._verify_identity(identity_token)
        now = int(self._clock())
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            row = self._require_live_claim(conn, identity=identity, lease=lease)
            if row["state"] != "EFFECT_PENDING" or not row["result_ref"]:
                raise RunRejected("run has no durable effect/result to acknowledge")
            changed = conn.execute(
                """
                UPDATE host_runs
                SET state = 'ACKED', claim_id = NULL, claim_owner = NULL,
                    lease_expires_at = NULL, updated_at = ?
                WHERE run_id = ? AND generation = ? AND state = 'EFFECT_PENDING'
                  AND claim_id = ?
                """,
                (now, identity.run_id, identity.generation, lease.claim_id),
            )
            if changed.rowcount != 1:
                raise RunRejected("ack lost concurrent state transition")
            self._event(
                conn,
                run_id=identity.run_id,
                generation=identity.generation,
                event_type="RUN_ACKED",
                state="ACKED",
                claim_id=lease.claim_id,
                detail="terminal success acknowledged after durable result",
            )
        return self.get(identity.run_id)

    def recover_expired(self, *, run_id: str) -> RunRecord:
        run = self._require_text(run_id, "run_id")
        now = int(self._clock())
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute(
                "SELECT * FROM host_runs WHERE run_id = ?",
                (run,),
            ).fetchone()
            if row is None:
                raise RunRejected("run not found")
            if row["state"] not in {"CLAIMED", "RUNNING", "EFFECT_PENDING"}:
                raise RunRejected("run is not recoverable from an active claim")
            if row["lease_expires_at"] is None or row["lease_expires_at"] > now:
                raise RunRejected("run claim lease has not expired")

            new_generation = row["generation"] + 1
            recovered_state = (
                "RECONCILE_REQUIRED"
                if row["state"] == "EFFECT_PENDING"
                else "RETRY_WAIT"
            )
            changed = conn.execute(
                """
                UPDATE host_runs
                SET generation = ?, state = ?,
                    claim_id = NULL, claim_owner = NULL, lease_expires_at = NULL,
                    updated_at = ?
                WHERE run_id = ? AND generation = ?
                  AND state IN ('CLAIMED', 'RUNNING', 'EFFECT_PENDING')
                """,
                (new_generation, recovered_state, now, run, row["generation"]),
            )
            if changed.rowcount != 1:
                raise RunRejected("recovery lost concurrent state transition")
            self._event(
                conn,
                run_id=run,
                generation=new_generation,
                event_type="RUN_RECOVERED",
                state=recovered_state,
                detail=f"expired_generation={row['generation']};from_state={row['state']}",
            )
        return self.get(run)

    def reconcile_effect(
        self,
        *,
        identity_token: str,
        effect_completed: bool,
        result_ref: str | None = None,
    ) -> RunRecord:
        """Resolve an ambiguous post-effect crash without blind replay."""

        identity = self._verify_identity(identity_token)
        if not isinstance(effect_completed, bool):
            raise RunRejected("effect_completed must be boolean")
        if effect_completed:
            result = self._require_text(result_ref, "result_ref")
        elif result_ref is not None:
            raise RunRejected("result_ref is only valid for a completed effect")
        else:
            result = None

        now = int(self._clock())
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute(
                "SELECT * FROM host_runs WHERE run_id = ?",
                (identity.run_id,),
            ).fetchone()
            if row is None or not self._identity_matches_row(identity, row):
                raise RunRejected("identity binding does not match recovered run")
            if row["state"] != "RECONCILE_REQUIRED":
                raise RunRejected("run does not require effect reconciliation")

            if effect_completed:
                changed = conn.execute(
                    """
                    UPDATE host_runs
                    SET state = 'ACKED', result_ref = ?, updated_at = ?
                    WHERE run_id = ? AND generation = ?
                      AND state = 'RECONCILE_REQUIRED'
                    """,
                    (result, now, identity.run_id, identity.generation),
                )
                event_type = "EFFECT_RECONCILED_COMPLETED"
                next_state = "ACKED"
                detail = f"result_ref={result}"
            else:
                changed = conn.execute(
                    """
                    UPDATE host_runs
                    SET state = 'RETRY_WAIT', result_ref = NULL, updated_at = ?
                    WHERE run_id = ? AND generation = ?
                      AND state = 'RECONCILE_REQUIRED'
                    """,
                    (now, identity.run_id, identity.generation),
                )
                event_type = "EFFECT_RECONCILED_NOT_COMPLETED"
                next_state = "RETRY_WAIT"
                detail = "adapter reconciliation authorized retry eligibility"

            if changed.rowcount != 1:
                raise RunRejected("effect reconciliation lost concurrent state transition")
            self._event(
                conn,
                run_id=identity.run_id,
                generation=identity.generation,
                event_type=event_type,
                state=next_state,
                detail=detail,
            )
        return self.get(identity.run_id)

    def release_retry(
        self,
        *,
        identity_token: str,
    ) -> RunRecord:
        identity = self._verify_identity(identity_token)
        now = int(self._clock())
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute(
                "SELECT * FROM host_runs WHERE run_id = ?",
                (identity.run_id,),
            ).fetchone()
            if row is None or not self._identity_matches_row(identity, row):
                raise RunRejected("identity binding does not match recovered run")
            if row["state"] != "RETRY_WAIT":
                raise RunRejected("run is not waiting for retry")
            changed = conn.execute(
                """
                UPDATE host_runs
                SET state = 'ACCEPTED', result_ref = NULL, updated_at = ?
                WHERE run_id = ? AND generation = ? AND state = 'RETRY_WAIT'
                """,
                (now, identity.run_id, identity.generation),
            )
            if changed.rowcount != 1:
                raise RunRejected("retry release lost concurrent state transition")
            self._event(
                conn,
                run_id=identity.run_id,
                generation=identity.generation,
                event_type="RETRY_AUTHORIZED",
                state="ACCEPTED",
                detail="fresh generation identity authorized retry",
            )
        return self.get(identity.run_id)

    def fail_terminal(
        self,
        *,
        identity_token: str,
        reason: str,
    ) -> RunRecord:
        identity = self._verify_identity(identity_token)
        return self._terminal_transition(
            identity=identity,
            state="FAILED_TERMINAL",
            event_type="RUN_FAILED_TERMINAL",
            reason=reason,
        )

    def cancel(
        self,
        *,
        identity_token: str,
        reason: str,
    ) -> RunRecord:
        identity = self._verify_identity(identity_token)
        return self._terminal_transition(
            identity=identity,
            state="CANCELLED",
            event_type="RUN_CANCELLED",
            reason=reason,
        )

    def _terminal_transition(
        self,
        *,
        identity: AuthenticatedExecutionIdentity,
        state: str,
        event_type: str,
        reason: str,
    ) -> RunRecord:
        reason_text = self._require_text(reason, "reason")
        now = int(self._clock())
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute(
                "SELECT * FROM host_runs WHERE run_id = ?",
                (identity.run_id,),
            ).fetchone()
            if row is None or not self._identity_matches_row(identity, row):
                raise RunRejected("identity binding does not match current run generation")
            if row["state"] in _TERMINAL:
                raise RunRejected("run is already terminal")
            changed = conn.execute(
                """
                UPDATE host_runs
                SET state = ?, terminal_reason = ?, claim_id = NULL,
                    claim_owner = NULL, lease_expires_at = NULL, updated_at = ?
                WHERE run_id = ? AND generation = ? AND state NOT IN
                    ('ACKED', 'FAILED_TERMINAL', 'CANCELLED')
                """,
                (state, reason_text, now, identity.run_id, identity.generation),
            )
            if changed.rowcount != 1:
                raise RunRejected("terminal transition lost concurrent state transition")
            self._event(
                conn,
                run_id=identity.run_id,
                generation=identity.generation,
                event_type=event_type,
                state=state,
                detail=reason_text,
            )
        return self.get(identity.run_id)

    def _claim_transition(
        self,
        *,
        identity: AuthenticatedExecutionIdentity,
        lease: ClaimLease,
        expected_state: str,
        next_state: str,
        event_type: str,
        detail: str,
    ) -> RunRecord:
        now = int(self._clock())
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            row = self._require_live_claim(conn, identity=identity, lease=lease)
            if row["state"] != expected_state:
                raise RunRejected(f"run is not in {expected_state}")
            changed = conn.execute(
                """
                UPDATE host_runs
                SET state = ?, updated_at = ?
                WHERE run_id = ? AND generation = ? AND state = ? AND claim_id = ?
                """,
                (
                    next_state,
                    now,
                    identity.run_id,
                    identity.generation,
                    expected_state,
                    lease.claim_id,
                ),
            )
            if changed.rowcount != 1:
                raise RunRejected("transition lost concurrent state transition")
            self._event(
                conn,
                run_id=identity.run_id,
                generation=identity.generation,
                event_type=event_type,
                state=next_state,
                claim_id=lease.claim_id,
                detail=detail,
            )
        return self.get(identity.run_id)

    def _require_live_claim(
        self,
        conn: sqlite3.Connection,
        *,
        identity: AuthenticatedExecutionIdentity,
        lease: ClaimLease,
    ) -> sqlite3.Row:
        row = conn.execute(
            "SELECT * FROM host_runs WHERE run_id = ?",
            (identity.run_id,),
        ).fetchone()
        if row is None:
            raise RunRejected("run not found")
        if not self._identity_matches_row(identity, row):
            raise RunRejected("identity binding does not match current run generation")
        if (
            lease.run_id != identity.run_id
            or lease.generation != identity.generation
            or row["claim_id"] != lease.claim_id
            or row["claim_owner"] != lease.claim_owner
        ):
            raise RunRejected("claim lease does not match current run claim")
        now = int(self._clock())
        if row["lease_expires_at"] is None or row["lease_expires_at"] <= now:
            raise RunRejected("claim lease is expired")
        return row

    def get(self, run_id: str) -> RunRecord:
        run = self._require_text(run_id, "run_id")
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM host_runs WHERE run_id = ?",
                (run,),
            ).fetchone()
        if row is None:
            raise RunRejected("run not found")
        return RunRecord(
            run_id=row["run_id"],
            generation=row["generation"],
            state=row["state"],
            principal_id=row["principal_id"],
            role_id=row["role_id"],
            session_id=row["session_id"],
            attempts=row["attempts"],
            claim_id=row["claim_id"],
            claim_owner=row["claim_owner"],
            lease_expires_at=row["lease_expires_at"],
            result_ref=row["result_ref"],
            terminal_reason=row["terminal_reason"],
            updated_at=row["updated_at"],
        )

    def events(self, run_id: str) -> list[dict[str, object]]:
        run = self._require_text(run_id, "run_id")
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT run_id, generation, occurred_at, event_type, state,
                       claim_id, detail
                FROM host_run_events
                WHERE run_id = ?
                ORDER BY event_id
                """,
                (run,),
            ).fetchall()
        return [dict(row) for row in rows]
