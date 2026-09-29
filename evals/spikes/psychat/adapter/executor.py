from __future__ import annotations

from typing import Protocol

from .contracts import ExecutionRequest, ExecutionResult
from .resilience import retry_with_timeout_boundary


class PsyChatDonorPort(Protocol):
    """Narrow seam around the upstream RAG behavior."""

    def respond(self, *, message: str, session_state: dict) -> tuple[str, dict]: ...


class PsyChatExecutorAdapter:
    capability = "knowledge.rag"
    executor_id = "psychat"

    def __init__(self, donor: PsyChatDonorPort) -> None:
        self._donor = donor

    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        request.validate()

        def invoke() -> tuple[str, dict]:
            return self._donor.respond(
                message=request.message,
                session_state=dict(request.state),
            )

        response, next_state = retry_with_timeout_boundary(invoke)
        return ExecutionResult(
            response=response,
            executor=self.executor_id,
            capability=self.capability,
            metadata={"next_state": next_state},
        )
