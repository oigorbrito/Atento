"""Host-owned Telegram enrollment and principal-to-role mapping.

This module begins at the boundary where the Telegram adapter has already
authenticated the provider transport. NanoClaw pairing state and NanoClaw's
owner role are deliberately not inputs to this authority path.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Collection, Mapping

from .identity import IdentityIssuer


_ROLES = frozenset({"NAIA", "ANNA", "APOLLO"})
_MAX_ENROLLMENT_TTL_SECONDS = 900
_MAX_ATTEMPTS = 10


class EnrollmentRejected(ValueError):
    """Telegram enrollment or resolution failed closed."""


@dataclass(frozen=True)
class AuthenticatedTelegramEvent:
    """Event identity after provider transport authentication by the adapter."""

    bot_account_id: int
    user_id: int


@dataclass(frozen=True)
class TelegramPrincipalBinding:
    principal_id: str
    provider_subject: str
    role_id: str


@dataclass(frozen=True)
class EnrollmentChallenge:
    challenge_id: str
    code: str
    expires_at: int
    attempts_left: int


def canonical_telegram_subject(event: AuthenticatedTelegramEvent) -> str:
    for value, field in (
        (event.bot_account_id, "bot_account_id"),
        (event.user_id, "user_id"),
    ):
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise EnrollmentRejected(f"telegram {field} must be a positive integer")
    return f"telegram:bot:{event.bot_account_id}:user:{event.user_id}"


class TelegramEnrollmentStore:
    """Durable Atento-owned Telegram enrollment state backed by SQLite."""

    def __init__(
        self,
        *,
        database_path: str | Path,
        enrollment_secret: bytes,
        enrollment_grants: Mapping[str, Collection[str]] | None = None,
        allow_bootstrap: bool = False,
        max_ttl_seconds: int = 300,
        max_attempts: int = 3,
        clock: Callable[[], float] = time.time,
    ) -> None:
        if not isinstance(enrollment_secret, bytes) or len(enrollment_secret) < 32:
            raise ValueError("enrollment_secret must contain at least 32 bytes")
        if not 1 <= max_ttl_seconds <= _MAX_ENROLLMENT_TTL_SECONDS:
            raise ValueError("max_ttl_seconds is outside host policy")
        if not 1 <= max_attempts <= _MAX_ATTEMPTS:
            raise ValueError("max_attempts is outside host policy")
        normalized: dict[str, frozenset[str]] = {}
        for principal_id, roles in (enrollment_grants or {}).items():
            if not principal_id or principal_id.strip() != principal_id:
                raise ValueError("enrollment grant principal must be canonical")
            values = frozenset(roles)
            if not values or not values.issubset(_ROLES):
                raise ValueError("enrollment grants contain unsupported roles")
            normalized[principal_id] = values

        self._database_path = str(database_path)
        self._secret = enrollment_secret
        self._enrollment_grants = normalized
        self._allow_bootstrap = allow_bootstrap
        self._max_ttl_seconds = max_ttl_seconds
        self._max_attempts = max_attempts
        self._clock = clock
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._database_path, timeout=5.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _initialize(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS telegram_principals (
                    principal_id TEXT PRIMARY KEY,
                    provider_subject TEXT NOT NULL UNIQUE,
                    role_id TEXT NOT NULL,
                    created_at INTEGER NOT NULL,
                    revoked_at INTEGER
                );
                CREATE TABLE IF NOT EXISTS telegram_enrollment_challenges (
                    challenge_id TEXT PRIMARY KEY,
                    provider_subject TEXT NOT NULL,
                    role_id TEXT NOT NULL,
                    code_digest BLOB NOT NULL,
                    expires_at INTEGER NOT NULL,
                    attempts_left INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    created_at INTEGER NOT NULL,
                    authorized_by TEXT,
                    bootstrap INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS telegram_enrollment_audit (
                    audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    occurred_at INTEGER NOT NULL,
                    event_type TEXT NOT NULL,
                    provider_subject TEXT,
                    principal_id TEXT,
                    role_id TEXT,
                    actor_principal_id TEXT,
                    detail TEXT NOT NULL
                );
                """
            )

    def _audit(
        self,
        conn: sqlite3.Connection,
        *,
        event_type: str,
        detail: str,
        provider_subject: str | None = None,
        principal_id: str | None = None,
        role_id: str | None = None,
        actor_principal_id: str | None = None,
    ) -> None:
        conn.execute(
            """
            INSERT INTO telegram_enrollment_audit
            (occurred_at, event_type, provider_subject, principal_id, role_id, actor_principal_id, detail)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                int(self._clock()),
                event_type,
                provider_subject,
                principal_id,
                role_id,
                actor_principal_id,
                detail,
            ),
        )

    def _digest(self, challenge_id: str, provider_subject: str, code: str) -> bytes:
        body = f"{challenge_id}|{provider_subject}|{code}".encode("utf-8")
        return hmac.new(self._secret, body, hashlib.sha256).digest()

    def start_enrollment(
        self,
        *,
        event: AuthenticatedTelegramEvent,
        role_id: str,
        authorized_by_principal_id: str | None = None,
        bootstrap: bool = False,
        ttl_seconds: int | None = None,
    ) -> EnrollmentChallenge:
        subject = canonical_telegram_subject(event)
        if role_id not in _ROLES:
            raise EnrollmentRejected("unsupported role")
        ttl = self._max_ttl_seconds if ttl_seconds is None else ttl_seconds
        if isinstance(ttl, bool) or not isinstance(ttl, int) or not 1 <= ttl <= self._max_ttl_seconds:
            raise EnrollmentRejected("requested enrollment lifetime is outside host policy")

        now = int(self._clock())
        challenge_id = secrets.token_urlsafe(18)
        code = f"{secrets.randbelow(1_000_000):06d}"

        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            active_count = conn.execute(
                "SELECT COUNT(*) AS n FROM telegram_principals WHERE revoked_at IS NULL"
            ).fetchone()["n"]

            if bootstrap:
                if not self._allow_bootstrap or active_count != 0 or authorized_by_principal_id is not None:
                    raise EnrollmentRejected("bootstrap enrollment is not authorized")
            else:
                if authorized_by_principal_id is None:
                    raise EnrollmentRejected("enrollment requires host-authorized principal")
                allowed = self._enrollment_grants.get(authorized_by_principal_id, frozenset())
                if role_id not in allowed:
                    raise EnrollmentRejected("authorizing principal cannot enroll requested role")
                actor = conn.execute(
                    """
                    SELECT 1 FROM telegram_principals
                    WHERE principal_id = ? AND revoked_at IS NULL
                    """,
                    (authorized_by_principal_id,),
                ).fetchone()
                if actor is None:
                    raise EnrollmentRejected("authorizing principal is not active")

            existing = conn.execute(
                "SELECT role_id, revoked_at FROM telegram_principals WHERE provider_subject = ?",
                (subject,),
            ).fetchone()
            if existing is not None:
                raise EnrollmentRejected("telegram subject already has a principal binding")

            conn.execute(
                """
                INSERT INTO telegram_enrollment_challenges
                (challenge_id, provider_subject, role_id, code_digest, expires_at, attempts_left,
                 status, created_at, authorized_by, bootstrap)
                VALUES (?, ?, ?, ?, ?, ?, 'PENDING', ?, ?, ?)
                """,
                (
                    challenge_id,
                    subject,
                    role_id,
                    self._digest(challenge_id, subject, code),
                    now + ttl,
                    self._max_attempts,
                    now,
                    authorized_by_principal_id,
                    int(bootstrap),
                ),
            )
            self._audit(
                conn,
                event_type="ENROLLMENT_STARTED",
                detail="challenge created under Atento host authority",
                provider_subject=subject,
                role_id=role_id,
                actor_principal_id=authorized_by_principal_id,
            )

        return EnrollmentChallenge(
            challenge_id=challenge_id,
            code=code,
            expires_at=now + ttl,
            attempts_left=self._max_attempts,
        )

    def complete_enrollment(
        self,
        *,
        event: AuthenticatedTelegramEvent,
        challenge_id: str,
        code: str,
    ) -> TelegramPrincipalBinding:
        subject = canonical_telegram_subject(event)
        if not challenge_id or not isinstance(code, str) or len(code) != 6 or not code.isdigit():
            raise EnrollmentRejected("malformed enrollment response")
        now = int(self._clock())

        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute(
                "SELECT * FROM telegram_enrollment_challenges WHERE challenge_id = ?",
                (challenge_id,),
            ).fetchone()
            if row is None or row["provider_subject"] != subject:
                raise EnrollmentRejected("enrollment challenge not found for subject")
            if row["status"] != "PENDING":
                raise EnrollmentRejected("enrollment challenge is not pending")
            if row["expires_at"] <= now:
                conn.execute(
                    "UPDATE telegram_enrollment_challenges SET status = 'EXPIRED' WHERE challenge_id = ?",
                    (challenge_id,),
                )
                self._audit(
                    conn,
                    event_type="ENROLLMENT_EXPIRED",
                    detail="challenge expired before successful completion",
                    provider_subject=subject,
                    role_id=row["role_id"],
                    actor_principal_id=row["authorized_by"],
                )
                conn.commit()
                raise EnrollmentRejected("enrollment challenge expired")

            supplied = self._digest(challenge_id, subject, code)
            if not hmac.compare_digest(supplied, row["code_digest"]):
                remaining = row["attempts_left"] - 1
                status = "LOCKED" if remaining <= 0 else "PENDING"
                conn.execute(
                    """
                    UPDATE telegram_enrollment_challenges
                    SET attempts_left = ?, status = ?
                    WHERE challenge_id = ?
                    """,
                    (max(0, remaining), status, challenge_id),
                )
                self._audit(
                    conn,
                    event_type="ENROLLMENT_ATTEMPT_REJECTED",
                    detail=f"wrong code; attempts_left={max(0, remaining)}",
                    provider_subject=subject,
                    role_id=row["role_id"],
                    actor_principal_id=row["authorized_by"],
                )
                conn.commit()
                raise EnrollmentRejected("enrollment code rejected")

            principal_id = f"atento:telegram:{event.bot_account_id}:{event.user_id}"
            conn.execute(
                """
                INSERT INTO telegram_principals
                (principal_id, provider_subject, role_id, created_at, revoked_at)
                VALUES (?, ?, ?, ?, NULL)
                """,
                (principal_id, subject, row["role_id"], now),
            )
            conn.execute(
                """
                UPDATE telegram_enrollment_challenges
                SET status = 'CONSUMED'
                WHERE challenge_id = ?
                """,
                (challenge_id,),
            )
            self._audit(
                conn,
                event_type="PRINCIPAL_ENROLLED",
                detail="provider subject mapped to Atento principal and role",
                provider_subject=subject,
                principal_id=principal_id,
                role_id=row["role_id"],
                actor_principal_id=row["authorized_by"],
            )

        return TelegramPrincipalBinding(
            principal_id=principal_id,
            provider_subject=subject,
            role_id=row["role_id"],
        )

    def resolve(self, event: AuthenticatedTelegramEvent) -> TelegramPrincipalBinding:
        subject = canonical_telegram_subject(event)
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT principal_id, provider_subject, role_id
                FROM telegram_principals
                WHERE provider_subject = ? AND revoked_at IS NULL
                """,
                (subject,),
            ).fetchone()
        if row is None:
            raise EnrollmentRejected("telegram subject is not enrolled or has been revoked")
        return TelegramPrincipalBinding(
            principal_id=row["principal_id"],
            provider_subject=row["provider_subject"],
            role_id=row["role_id"],
        )

    def revoke(self, *, principal_id: str, actor_principal_id: str) -> None:
        if not principal_id or not actor_principal_id:
            raise EnrollmentRejected("revocation requires principal and actor")
        now = int(self._clock())
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute(
                """
                SELECT provider_subject, role_id, revoked_at
                FROM telegram_principals WHERE principal_id = ?
                """,
                (principal_id,),
            ).fetchone()
            if row is None or row["revoked_at"] is not None:
                raise EnrollmentRejected("principal is not active")
            conn.execute(
                "UPDATE telegram_principals SET revoked_at = ? WHERE principal_id = ?",
                (now, principal_id),
            )
            self._audit(
                conn,
                event_type="PRINCIPAL_REVOKED",
                detail="principal binding revoked by host-authorized actor",
                provider_subject=row["provider_subject"],
                principal_id=principal_id,
                role_id=row["role_id"],
                actor_principal_id=actor_principal_id,
            )

    def audit_events(self) -> list[dict[str, object]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT occurred_at, event_type, provider_subject, principal_id,
                       role_id, actor_principal_id, detail
                FROM telegram_enrollment_audit
                ORDER BY audit_id
                """
            ).fetchall()
        return [dict(row) for row in rows]


def issue_execution_identity_for_telegram(
    *,
    event: AuthenticatedTelegramEvent,
    enrollment_store: TelegramEnrollmentStore,
    issuer: IdentityIssuer,
    session_id: str,
    run_id: str,
    generation: int,
    ttl_seconds: int | None = None,
) -> str:
    """Resolve host-owned role mapping and issue without caller-supplied role."""

    binding = enrollment_store.resolve(event)
    return issuer.issue(
        authenticated_principal_id=binding.principal_id,
        role_id=binding.role_id,
        session_id=session_id,
        run_id=run_id,
        generation=generation,
        ttl_seconds=ttl_seconds,
    )
