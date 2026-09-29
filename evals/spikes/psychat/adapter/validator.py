from __future__ import annotations

from .contracts import ExecutionResult


class ResultValidator:
    def validate(
        self,
        result: ExecutionResult,
        *,
        expected_capability: str | None = None,
        expected_executor: str | None = None,
    ) -> ExecutionResult:
        if not isinstance(result, ExecutionResult):
            raise TypeError("executor must return ExecutionResult")
        if not result.response.strip():
            raise ValueError("executor returned an empty response")
        if not result.executor:
            raise ValueError("executor id missing")
        if not result.capability:
            raise ValueError("capability missing")
        if (
            expected_capability is not None
            and result.capability != expected_capability
        ):
            raise ValueError(
                "executor result capability does not match selected route"
            )
        if (
            expected_executor is not None
            and result.executor != expected_executor
        ):
            raise ValueError(
                "executor result id does not match selected route"
            )
        return result
