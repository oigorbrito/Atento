from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Iterable, List

from .gates import evaluate_gates
from .metrics import score_results, summarize_scores
from .schema import EvalCase, TurnResult


def load_jsonl(path: Path) -> Iterable[dict]:
    with path.open("r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc


def load_cases(path: Path) -> Dict[str, EvalCase]:
    cases: Dict[str, EvalCase] = {}
    for raw in load_jsonl(path):
        case = EvalCase.from_dict(raw)
        if case.id in cases:
            raise ValueError(f"duplicate case id: {case.id}")
        if not case.steps:
            raise ValueError(f"{case.id}: case has no steps")
        cases[case.id] = case
    return cases


def load_results(path: Path) -> List[TurnResult]:
    return [TurnResult.from_dict(x) for x in load_jsonl(path)]


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    parser = argparse.ArgumentParser(description="AtentoEval offline scorer")
    parser.add_argument("--cases", required=True, type=Path)
    parser.add_argument("--results", required=True, type=Path)
    parser.add_argument("--gates", type=Path)
    parser.add_argument(
        "--agent-scope",
        action="append",
        dest="agent_scopes",
        help="Restrict evaluation to one or more agent scopes, e.g. ANNA, NAIA or SHARED.",
    )
    parser.add_argument("--baseline-summary", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    cases = load_cases(args.cases)
    if args.agent_scopes:
        wanted_scopes = set(args.agent_scopes)
        cases = {
            case_id: case
            for case_id, case in cases.items()
            if case.agent_scope in wanted_scopes
        }
        if not cases:
            raise ValueError(f"no cases matched agent scopes: {sorted(wanted_scopes)}")

    results = load_results(args.results)

    unknown = sorted({r.case_id for r in results} - set(cases))
    if unknown:
        raise ValueError(f"results contain unknown case ids: {unknown}")

    rows = score_results(cases, results)
    summary = summarize_scores(rows)

    evaluated_scopes = sorted({case.agent_scope for case in cases.values()})
    primary_scopes = sorted(set(evaluated_scopes) - {"SHARED"})
    mixed_primary_agent_scopes = len(primary_scopes) > 1

    report = {
        "case_count": len(cases),
        "result_count": len(results),
        "agent_scopes": evaluated_scopes,
        "primary_agent_scopes": primary_scopes,
        "mixed_agent_scopes": len(evaluated_scopes) > 1,
        "mixed_primary_agent_scopes": mixed_primary_agent_scopes,
        "summary": summary,
        "rows": rows,
    }

    if args.gates and mixed_primary_agent_scopes:
        raise ValueError(
            "release/selection gates cannot mix multiple primary agent scopes: "
            f"{primary_scopes}; run each agent separately, optionally with SHARED cases"
        )

    if args.gates:
        gates = load_json(args.gates)
        baseline = load_json(args.baseline_summary) if args.baseline_summary else None
        if baseline and "summary" in baseline:
            baseline = baseline["summary"]
        report["gates"] = evaluate_gates(summary, gates, baseline)

    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)

    if report.get("gates", {}).get("passed") is False:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
