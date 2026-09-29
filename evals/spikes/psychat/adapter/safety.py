from __future__ import annotations

from .contracts import ExecutionRequest, ExecutionResult


class SpikeSafetyPolicy:
    """Deterministic enforcement seam for the spike.

    This is deliberately not a clinical classifier. It proves the donor cannot
    bypass pre/post policy enforcement. Production safety logic belongs to the
    Atento Safety block.
    """

    def precheck(self, request: ExecutionRequest) -> None:
        request.validate()

    def postcheck(self, result: ExecutionResult) -> None:
        if not result.response.strip():
            raise ValueError("safety boundary rejects empty output")
