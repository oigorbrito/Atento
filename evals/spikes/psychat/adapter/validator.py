from __future__ import annotations

from typing import Any, Dict

from .contracts import ContractError


def normalize_psychat_result(raw: Any) -> Dict[str, Any]:
    if not isinstance(raw, dict):
        raise ContractError("PsyChat result must be an object")
    if raw.get("success") is not True:
        raise ContractError(f"PsyChat execution failed: {raw.get('reason', 'unknown')}")

    response = raw.get("response")
    if not isinstance(response, str) or not response.strip():
        raise ContractError("PsyChat response must be a non-empty string")

    sources = raw.get("sources", [])
    if not isinstance(sources, list):
        raise ContractError("PsyChat sources must be a list")

    return {
        "response": response.strip(),
        "used_rag": bool(raw.get("used_rag", False)),
        "sources": sources,
        "topic": raw.get("topic"),
        "reason": raw.get("reason"),
    }
