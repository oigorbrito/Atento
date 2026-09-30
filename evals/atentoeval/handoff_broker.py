from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping
import re


_ALLOWED_KINDS = {"handoff", "request", "response"}
_ROLE_RE = re.compile(r"^[A-Z][A-Za-z0-9_-]{0,31}$")
_MAX_BODY_CHARS = 4096


class BrokerContractError(ValueError):
    pass


@dataclass(frozen=True)
class BrokerEnvelope:
    from_role: str
    to_role: str
    kind: str
    body: str
    correlation_id: str

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)


_FORBIDDEN_KEYS = {
    "memory",
    "memory_id",
    "memory_ids",
    "credential",
    "credentials",
    "credential_key",
    "credential_value",
    "token",
    "api_key",
    "secret",
    "capability",
    "capabilities",
    "tool",
    "tool_handle",
    "channel_handle",
    "session_handle",
    "runtime_handle",
    "agent_handle",
}


def _require_string(data: Mapping[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value:
        raise BrokerContractError(f"{key} must be a non-empty string")
    return value


def validate_envelope(data: Mapping[str, Any]) -> BrokerEnvelope:
    allowed = {"from_role", "to_role", "kind", "body", "correlation_id"}
    extra = set(data) - allowed
    if extra:
        forbidden = sorted(extra & _FORBIDDEN_KEYS)
        if forbidden:
            raise BrokerContractError(
                "authority-bearing fields are forbidden: " + ", ".join(forbidden)
            )
        raise BrokerContractError("undeclared fields are forbidden: " + ", ".join(sorted(extra)))

    from_role = _require_string(data, "from_role")
    to_role = _require_string(data, "to_role")
    kind = _require_string(data, "kind")
    body = _require_string(data, "body")
    correlation_id = _require_string(data, "correlation_id")

    if not _ROLE_RE.fullmatch(from_role):
        raise BrokerContractError("invalid from_role")
    if not _ROLE_RE.fullmatch(to_role):
        raise BrokerContractError("invalid to_role")
    if from_role == to_role:
        raise BrokerContractError("cross-role broker requires distinct roles")
    if kind not in _ALLOWED_KINDS:
        raise BrokerContractError(f"unsupported kind: {kind}")
    if len(body) > _MAX_BODY_CHARS:
        raise BrokerContractError("body exceeds broker limit")
    if len(correlation_id) > 128:
        raise BrokerContractError("correlation_id exceeds broker limit")

    return BrokerEnvelope(
        from_role=from_role,
        to_role=to_role,
        kind=kind,
        body=body,
        correlation_id=correlation_id,
    )


class ExplicitHandoffBroker:
    """Minimal candidate-agnostic handoff boundary.

    This broker deliberately transports only a bounded message envelope.
    It has no APIs for memory, credentials, capabilities, tools, channels,
    sessions, runtimes, or agent handles.
    """

    def handoff(self, data: Mapping[str, Any]) -> Dict[str, str]:
        envelope = validate_envelope(data)
        return envelope.to_dict()
