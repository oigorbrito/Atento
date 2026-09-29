from __future__ import annotations

from .contracts import ExecutionResult


class ResultValidator:
    def validate(self, result: ExecutionResult) -> ExecutionResult:
        if not isinstance(result, ExecutionResult):
            raise TypeError("executor must return ExecutionResult")
        if not result.response.strip():
            raise ValueError("executor returned an empty response")
        if not result.executor:
            raise ValueError("executor id missing")
        if not result.capability:
            raise ValueError("capability missing")
        return result
