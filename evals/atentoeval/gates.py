from __future__ import annotations

from typing import Any, Dict, List


def _lookup(data: Dict[str, Any], dotted: str) -> Any:
    cur: Any = data
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def evaluate_gates(
    current_summary: Dict[str, Any],
    gate_config: Dict[str, Any],
    baseline_summary: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    failures: List[Dict[str, Any]] = []
    skipped: List[Dict[str, Any]] = []
    passed: List[Dict[str, Any]] = []

    for gate in gate_config.get("gates", []):
        if not gate.get("enabled", True):
            skipped.append({"id": gate["id"], "reason": "disabled"})
            continue

        metric = gate["metric"]
        value = _lookup(current_summary, metric)
        if value is None:
            failures.append({"id": gate["id"], "reason": "missing_metric", "metric": metric})
            continue

        ok = True
        detail: Dict[str, Any] = {"id": gate["id"], "metric": metric, "value": value}

        if "max" in gate:
            ok = ok and value <= gate["max"]
            detail["max"] = gate["max"]
        if "min" in gate:
            ok = ok and value >= gate["min"]
            detail["min"] = gate["min"]

        if "min_delta" in gate or "max_delta" in gate:
            if baseline_summary is None:
                skipped.append({"id": gate["id"], "reason": "baseline_required"})
                continue
            baseline = _lookup(baseline_summary, metric)
            if baseline is None:
                failures.append({"id": gate["id"], "reason": "missing_baseline_metric"})
                continue
            delta = value - baseline
            detail["baseline"] = baseline
            detail["delta"] = delta
            if "min_delta" in gate:
                ok = ok and delta >= gate["min_delta"]
                detail["min_delta"] = gate["min_delta"]
            if "max_delta" in gate:
                ok = ok and delta <= gate["max_delta"]
                detail["max_delta"] = gate["max_delta"]

        (passed if ok else failures).append(detail)

    return {
        "passed": len(failures) == 0,
        "failures": failures,
        "passed_gates": passed,
        "skipped_gates": skipped,
    }
