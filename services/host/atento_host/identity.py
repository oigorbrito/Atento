"""Host-issued, short-lived execution identities for runtime adapters.

The issuer must only be called after the host has authenticated the principal
and resolved the role from trusted channel/session policy. The token is
presented to the host control plane for validation; agents and runtime
containers must never receive the signing key or provide their own grants.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import re
import time
from dataclasses import dataclass
from typing import Callable, Collection, Mapping


_ROLES = frozenset({"NAIA", "ANNA", "APOLLO"})
_TOKEN_PART_RE = re.compile(r"^[A-Za-z0-9_-]+$")
_MAX_TOKEN_BYTES = 8192
_MAX_TTL_SECONDS = 300
_CLOCK_SKEW_SECONDS = 15
_CLAIM_KEYS = frozenset(
    {
        "v",
        "iss",
        "aud",
        "sub",
        "role_id",
        "session_id",
        "run_id",
        "generation",
        "granted_capability_set",
        "iat",
        "exp",
    }
)


class IdentityRejected(ValueError):
    """Identity could not be issued or failed verification."""


@dataclass(frozen=True)
class AuthenticatedExecutionIdentity:
    principal_id: str
    role_id: str
    session_id: str
    run_id: str
    generation: int
    granted_capability_set: tuple[str, ...]
    issued_at: int
    expires_at: int
    issuer: str
    audience: str


def _b64url_encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def _b64url_decode(value: str) -> bytes:
    if not value or not _TOKEN_PART_RE.fullmatch(value):
        raise IdentityRejected("malformed identity token")
    padding = "=" * (-len(value) % 4)
    try:
        return base64.urlsafe_b64decode(value + padding)
    except (ValueError, base64.binascii.Error) as exc:
        raise IdentityRejected("malformed identity token") from exc


class IdentityIssuer:
    """Issues HMAC-authenticated, role-scoped execution identities.

    ``role_grants`` is trusted host configuration keyed by authenticated
    principal and role. It is the only source of roles and grants; callers
    cannot request additional grants. The signing key must be injected by a
    host secret/key service and remain inside the control plane.
    """

    def __init__(
        self,
        *,
        signing_key: bytes,
        role_grants: Mapping[str, Mapping[str, Collection[str]]],
        issuer: str = "atento-host-control-plane",
        audience: str = "atento-runtime-adapter",
        max_ttl_seconds: int = 300,
        clock: Callable[[], float] = time.time,
    ) -> None:
        if not isinstance(signing_key, bytes) or len(signing_key) < 32:
            raise ValueError("signing_key must contain at least 32 bytes")
        if not 1 <= max_ttl_seconds <= _MAX_TTL_SECONDS:
            raise ValueError(f"max_ttl_seconds must be between 1 and {_MAX_TTL_SECONDS}")
        if not issuer or not audience:
            raise ValueError("issuer and audience are required")

        normalized: dict[str, dict[str, tuple[str, ...]]] = {}
        for principal_id, roles in role_grants.items():
            self._require_text(principal_id, "principal_id")
            normalized_roles: dict[str, tuple[str, ...]] = {}
            for role_id, grants in roles.items():
                if not isinstance(role_id, str) or role_id not in _ROLES:
                    raise ValueError(f"unsupported configured role: {role_id}")
                grant_values = tuple(grants)
                if any(not isinstance(grant, str) or not grant for grant in grant_values):
                    raise ValueError("configured grants must be non-empty strings")
                grant_set = tuple(sorted(set(grant_values)))
                normalized_roles[role_id] = grant_set
            normalized[principal_id] = normalized_roles

        self._signing_key = signing_key
        self._role_grants = normalized
        self._issuer = issuer
        self._audience = audience
        self._max_ttl_seconds = max_ttl_seconds
        self._clock = clock

    @staticmethod
    def _require_text(value: object, field: str) -> str:
        if not isinstance(value, str) or not value or value.strip() != value:
            raise IdentityRejected(f"{field} must be a non-empty canonical string")
        if len(value) > 256:
            raise IdentityRejected(f"{field} exceeds the host limit")
        return value

    def issue(
        self,
        *,
        authenticated_principal_id: str,
        role_id: str,
        session_id: str,
        run_id: str,
        generation: int,
        ttl_seconds: int | None = None,
    ) -> str:
        """Issue identity after upstream host authentication and role mapping."""
        principal = self._require_text(authenticated_principal_id, "principal_id")
        session = self._require_text(session_id, "session_id")
        run = self._require_text(run_id, "run_id")
        if not isinstance(role_id, str) or role_id not in _ROLES:
            raise IdentityRejected("unsupported role")
        if isinstance(generation, bool) or not isinstance(generation, int) or generation < 1:
            raise IdentityRejected("generation must be a positive integer")

        allowed = self._role_grants.get(principal, {}).get(role_id)
        if allowed is None:
            raise IdentityRejected("principal is not authorized for role")

        ttl = self._max_ttl_seconds if ttl_seconds is None else ttl_seconds
        if isinstance(ttl, bool) or not isinstance(ttl, int) or not 1 <= ttl <= self._max_ttl_seconds:
            raise IdentityRejected("requested identity lifetime is outside host policy")

        issued_at = int(self._clock())
        claims = {
            "v": 1,
            "iss": self._issuer,
            "aud": self._audience,
            "sub": principal,
            "role_id": role_id,
            "session_id": session,
            "run_id": run,
            "generation": generation,
            "granted_capability_set": list(allowed),
            "iat": issued_at,
            "exp": issued_at + ttl,
        }
        payload = json.dumps(claims, sort_keys=True, separators=(",", ":")).encode("utf-8")
        encoded = _b64url_encode(payload)
        signature = hmac.new(self._signing_key, encoded.encode("ascii"), hashlib.sha256).digest()
        return encoded + "." + _b64url_encode(signature)

    def verify(
        self,
        token: str,
        *,
        expected_role_id: str | None = None,
        expected_session_id: str | None = None,
        expected_run_id: str | None = None,
        expected_generation: int | None = None,
    ) -> AuthenticatedExecutionIdentity:
        if not isinstance(token, str) or len(token) > _MAX_TOKEN_BYTES:
            raise IdentityRejected("malformed identity token")
        parts = token.split(".")
        if len(parts) != 2:
            raise IdentityRejected("malformed identity token")
        encoded, signature_text = parts
        supplied_signature = _b64url_decode(signature_text)
        expected_signature = hmac.new(
            self._signing_key, encoded.encode("ascii"), hashlib.sha256
        ).digest()
        if not hmac.compare_digest(supplied_signature, expected_signature):
            raise IdentityRejected("identity signature is invalid")

        try:
            raw = json.loads(_b64url_decode(encoded))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise IdentityRejected("identity claims are malformed") from exc
        if not isinstance(raw, dict) or set(raw) != _CLAIM_KEYS:
            raise IdentityRejected("identity claims do not match schema")
        if raw["v"] != 1 or raw["iss"] != self._issuer or raw["aud"] != self._audience:
            raise IdentityRejected("identity issuer, audience, or version mismatch")

        principal = self._require_text(raw["sub"], "principal_id")
        role_id = raw["role_id"]
        session_id = self._require_text(raw["session_id"], "session_id")
        run_id = self._require_text(raw["run_id"], "run_id")
        generation = raw["generation"]
        issued_at = raw["iat"]
        expires_at = raw["exp"]
        grants = raw["granted_capability_set"]
        if not isinstance(role_id, str) or role_id not in _ROLES:
            raise IdentityRejected("unsupported role")
        if any(isinstance(v, bool) or not isinstance(v, int) for v in (generation, issued_at, expires_at)):
            raise IdentityRejected("identity time or generation claims are malformed")
        if generation < 1 or expires_at <= issued_at or expires_at - issued_at > self._max_ttl_seconds:
            raise IdentityRejected("identity lifetime or generation is invalid")
        if not isinstance(grants, list) or any(not isinstance(g, str) or not g for g in grants):
            raise IdentityRejected("identity grants are malformed")
        if len(set(grants)) != len(grants) or grants != sorted(grants):
            raise IdentityRejected("identity grants are not canonical")

        now = int(self._clock())
        if issued_at > now + _CLOCK_SKEW_SECONDS or expires_at <= now:
            raise IdentityRejected("identity is not currently valid")

        configured = self._role_grants.get(principal, {}).get(role_id)
        if configured is None or tuple(grants) != configured:
            raise IdentityRejected("identity role or grants are no longer authorized")

        bindings = (
            (expected_role_id, role_id, "role"),
            (expected_session_id, session_id, "session"),
            (expected_run_id, run_id, "run"),
            (expected_generation, generation, "generation"),
        )
        for expected, actual, label in bindings:
            if expected is not None and expected != actual:
                raise IdentityRejected(f"identity {label} binding mismatch")

        return AuthenticatedExecutionIdentity(
            principal_id=principal,
            role_id=role_id,
            session_id=session_id,
            run_id=run_id,
            generation=generation,
            granted_capability_set=tuple(grants),
            issued_at=issued_at,
            expires_at=expires_at,
            issuer=self._issuer,
            audience=self._audience,
        )
