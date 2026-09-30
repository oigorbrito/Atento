"""Deterministic Atento-owned browser-effect authority adapter for the frozen Engram probe.

This module is intentionally candidate-boundary focused. It does not claim to modify
Engram upstream or prove unrelated Engram tools. The adapter mediates consequential
browser click/type effects that the frozen composition removes from the unmediated
NAIA tool set.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Callable, FrozenSet, Iterable, Literal, Mapping, Protocol

Origin = Literal["interactive", "scheduled"]
Action = Literal["click", "type"]


class AuthorityDenied(RuntimeError):
    """The requested browser effect is outside the granted authority."""


class AuthorityControlUnavailable(RuntimeError):
    """Policy evaluation failed; the adapter must fail closed."""


class BrowserDriver(Protocol):
    def click(self, *, destination: str, selector: str) -> str: ...

    def type_text(self, *, destination: str, selector: str, text: str) -> str: ...


@dataclass(frozen=True, order=True)
class Grant:
    destination: str
    action: Action
    selector: str


@dataclass(frozen=True)
class BrowserAuthorityPolicy:
    """Frozen grants with an invariant that scheduled authority is never broader."""

    interactive: FrozenSet[Grant]
    scheduled: FrozenSet[Grant]

    def __post_init__(self) -> None:
        if not self.scheduled.issubset(self.interactive):
            extra = sorted(self.scheduled.difference(self.interactive))
            raise ValueError(
                "scheduled authority must be a subset of interactive authority; "
                f"extra={extra!r}"
            )

    @classmethod
    def from_iterables(
        cls,
        *,
        interactive: Iterable[Grant],
        scheduled: Iterable[Grant] = (),
    ) -> "BrowserAuthorityPolicy":
        return cls(frozenset(interactive), frozenset(scheduled))

    def grants_for(self, origin: Origin) -> FrozenSet[Grant]:
        if origin == "interactive":
            return self.interactive
        if origin == "scheduled":
            return self.scheduled
        raise ValueError(f"unsupported origin: {origin!r}")

    def delegated(self, requested: Iterable[Grant]) -> "BrowserAuthorityPolicy":
        """Delegates only the intersection of requested grants and caller authority."""
        requested_set = frozenset(requested)
        return BrowserAuthorityPolicy(
            interactive=self.interactive.intersection(requested_set),
            scheduled=self.scheduled.intersection(requested_set),
        )


@dataclass(frozen=True)
class BrowserEffectRequest:
    principal: str
    origin: Origin
    destination: str
    action: Action
    selector: str
    text: str | None = None

    def grant(self) -> Grant:
        return Grant(
            destination=self.destination,
            action=self.action,
            selector=self.selector,
        )


@dataclass(frozen=True)
class AuditRecord:
    effect_id: str
    principal: str
    origin: Origin
    destination: str
    action: Action
    selector_hash: str
    decision: Literal["allowed", "denied", "control_error"]
    reason: str

    def model_visible(self) -> Mapping[str, str]:
        # Deliberately excludes typed text and driver/provider credential material.
        return {
            "effect_id": self.effect_id,
            "principal": self.principal,
            "origin": self.origin,
            "destination": self.destination,
            "action": self.action,
            "selector_hash": self.selector_hash,
            "decision": self.decision,
            "reason": self.reason,
        }


PolicyHook = Callable[[BrowserEffectRequest, BrowserAuthorityPolicy], bool]


@dataclass
class BrowserEffectAdapter:
    driver: BrowserDriver
    policy: BrowserAuthorityPolicy
    policy_hook: PolicyHook | None = None
    audit: list[AuditRecord] = field(default_factory=list)

    def _effect_id(self, req: BrowserEffectRequest) -> str:
        # Identity uses non-secret, authority-relevant fields only. Text is represented by
        # a hash so the raw payload is not copied into the audit/model-visible surface.
        payload_hash = sha256((req.text or "").encode("utf-8")).hexdigest()
        canonical = json.dumps(
            {
                "principal": req.principal,
                "origin": req.origin,
                "destination": req.destination,
                "action": req.action,
                "selector": req.selector,
                "payload_hash": payload_hash,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        return sha256(canonical.encode("utf-8")).hexdigest()

    def _record(
        self,
        req: BrowserEffectRequest,
        *,
        decision: Literal["allowed", "denied", "control_error"],
        reason: str,
    ) -> AuditRecord:
        rec = AuditRecord(
            effect_id=self._effect_id(req),
            principal=req.principal,
            origin=req.origin,
            destination=req.destination,
            action=req.action,
            selector_hash=sha256(req.selector.encode("utf-8")).hexdigest(),
            decision=decision,
            reason=reason,
        )
        self.audit.append(rec)
        return rec

    def _policy_allows(self, req: BrowserEffectRequest) -> bool:
        if self.policy_hook is not None:
            try:
                if not self.policy_hook(req, self.policy):
                    return False
            except Exception as exc:
                self._record(
                    req,
                    decision="control_error",
                    reason=f"policy-control-error:{type(exc).__name__}",
                )
                raise AuthorityControlUnavailable(
                    "browser effect authority control unavailable"
                ) from exc
        return req.grant() in self.policy.grants_for(req.origin)

    def execute(self, req: BrowserEffectRequest) -> Mapping[str, str]:
        if req.action == "type" and req.text is None:
            raise ValueError("type action requires text")

        if not self._policy_allows(req):
            self._record(req, decision="denied", reason="grant-not-present")
            raise AuthorityDenied("browser effect denied by technical authority policy")

        self._record(req, decision="allowed", reason="explicit-grant")
        if req.action == "click":
            observation = self.driver.click(
                destination=req.destination,
                selector=req.selector,
            )
        elif req.action == "type":
            observation = self.driver.type_text(
                destination=req.destination,
                selector=req.selector,
                text=req.text or "",
            )
        else:
            raise ValueError(f"unsupported action: {req.action!r}")

        # Return a deliberately narrow model-visible surface.
        return {
            "effect_id": self.audit[-1].effect_id,
            "status": "executed",
            "observation": observation,
        }
