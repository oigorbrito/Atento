"""Deterministic Atento-owned browser-effect authority adapter for the frozen Engram probe."""
from __future__ import annotations
from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Callable, FrozenSet, Iterable, Literal, Mapping, Protocol
Origin = Literal["interactive", "scheduled"]
Action = Literal["click", "type"]
class AuthorityDenied(RuntimeError): pass
class AuthorityControlUnavailable(RuntimeError): pass
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
    interactive: FrozenSet[Grant]
    scheduled: FrozenSet[Grant]
    def __post_init__(self) -> None:
        if not self.scheduled.issubset(self.interactive):
            extra = sorted(self.scheduled.difference(self.interactive))
            raise ValueError(f"scheduled authority must be a subset of interactive authority; extra={extra!r}")
    @classmethod
    def from_iterables(cls, *, interactive: Iterable[Grant], scheduled: Iterable[Grant] = ()):
        return cls(frozenset(interactive), frozenset(scheduled))
    def grants_for(self, origin: Origin) -> FrozenSet[Grant]:
        if origin == "interactive": return self.interactive
        if origin == "scheduled": return self.scheduled
        raise ValueError(f"unsupported origin: {origin!r}")
    def delegated(self, requested: Iterable[Grant]):
        requested_set = frozenset(requested)
        return BrowserAuthorityPolicy(self.interactive.intersection(requested_set), self.scheduled.intersection(requested_set))
@dataclass(frozen=True)
class BrowserEffectRequest:
    principal: str
    origin: Origin
    destination: str
    action: Action
    selector: str
    text: str | None = None
    def grant(self) -> Grant: return Grant(self.destination, self.action, self.selector)
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
        return {"effect_id":self.effect_id,"principal":self.principal,"origin":self.origin,"destination":self.destination,"action":self.action,"selector_hash":self.selector_hash,"decision":self.decision,"reason":self.reason}
PolicyHook = Callable[[BrowserEffectRequest, BrowserAuthorityPolicy], bool]
@dataclass
class BrowserEffectAdapter:
    driver: BrowserDriver
    policy: BrowserAuthorityPolicy
    policy_hook: PolicyHook | None = None
    audit: list[AuditRecord] = field(default_factory=list)
    def _effect_id(self, req):
        payload_hash = sha256((req.text or "").encode()).hexdigest()
        canonical = json.dumps({"principal":req.principal,"origin":req.origin,"destination":req.destination,"action":req.action,"selector":req.selector,"payload_hash":payload_hash}, sort_keys=True, separators=(",",":"))
        return sha256(canonical.encode()).hexdigest()
    def _record(self, req, *, decision, reason):
        rec = AuditRecord(self._effect_id(req), req.principal, req.origin, req.destination, req.action, sha256(req.selector.encode()).hexdigest(), decision, reason)
        self.audit.append(rec); return rec
    def _policy_allows(self, req):
        if self.policy_hook is not None:
            try:
                if not self.policy_hook(req, self.policy): return False
            except Exception as exc:
                self._record(req, decision="control_error", reason=f"policy-control-error:{type(exc).__name__}")
                raise AuthorityControlUnavailable("browser effect authority control unavailable") from exc
        return req.grant() in self.policy.grants_for(req.origin)
    def execute(self, req):
        if req.action == "type" and req.text is None: raise ValueError("type action requires text")
        if not self._policy_allows(req):
            self._record(req, decision="denied", reason="grant-not-present")
            raise AuthorityDenied("browser effect denied by technical authority policy")
        self._record(req, decision="allowed", reason="explicit-grant")
        if req.action == "click": observation = self.driver.click(destination=req.destination, selector=req.selector)
        elif req.action == "type": observation = self.driver.type_text(destination=req.destination, selector=req.selector, text=req.text or "")
        else: raise ValueError(f"unsupported action: {req.action!r}")
        return {"effect_id":self.audit[-1].effect_id,"status":"executed","observation":observation}
