#!/usr/bin/env python3
"""Static Chassis Fitness audit for an external donor.

This is a screening metric, not a quality or safety benchmark.
It intentionally uses only the Python standard library so it can run
before installing the donor's runtime dependencies.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path
from typing import Any


PY_SUFFIX = ".py"


def iter_python_files(root: Path):
    for path in root.rglob(f"*{PY_SUFFIX}"):
        if "__pycache__" in path.parts:
            continue
        yield path


def read_sources(root: Path):
    out = {}
    for path in iter_python_files(root):
        try:
            out[str(path.relative_to(root))] = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            out[str(path.relative_to(root))] = path.read_text(encoding="utf-8", errors="ignore")
    return out


def parse_sources(sources):
    trees = {}
    syntax_errors = {}
    for path, text in sources.items():
        try:
            trees[path] = ast.parse(text, filename=path)
        except SyntaxError as exc:
            syntax_errors[path] = f"{exc.msg}:{exc.lineno}"
    return trees, syntax_errors


def names_and_strings(trees):
    names = set()
    strings = []
    classes = []
    functions = []
    calls = []
    attrs = []
    imports = []
    for path, tree in trees.items():
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                names.add(node.id.lower())
            elif isinstance(node, ast.Attribute):
                attrs.append((path, node.attr.lower()))
            elif isinstance(node, ast.Constant) and isinstance(node.value, str):
                strings.append((path, node.value.lower()))
            elif isinstance(node, ast.ClassDef):
                classes.append((path, node.name.lower()))
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append((path, node.name.lower()))
            elif isinstance(node, ast.Call):
                calls.append((path, node))
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                imports.append((path, node))
    return names, strings, classes, functions, calls, attrs, imports


def dotted_call_name(node: ast.AST) -> str:
    parts = []
    cur = node
    while isinstance(cur, ast.Attribute):
        parts.append(cur.attr)
        cur = cur.value
    if isinstance(cur, ast.Name):
        parts.append(cur.id)
    return ".".join(reversed(parts)).lower()


def audit(root: Path, source_id: str, upstream_commit: str | None = None) -> dict[str, Any]:
    sources = read_sources(root)
    trees, syntax_errors = parse_sources(sources)
    names, strings, classes, functions, calls, attrs, imports = names_and_strings(trees)

    combined = "\n".join(sources.values()).lower()
    class_names = {n for _, n in classes}
    function_names = {n for _, n in functions}

    direct_provider_calls = []
    timeout_calls = []
    for path, call in calls:
        name = dotted_call_name(call.func)
        if name in {"requests.post", "requests.get", "requests.request"}:
            direct_provider_calls.append({"path": path, "call": name})
            if any(k.arg == "timeout" for k in call.keywords):
                timeout_calls.append({"path": path, "call": name})

    wildcard_config_imports = []
    for path, node in imports:
        if isinstance(node, ast.ImportFrom) and node.module == "config":
            if any(alias.name == "*" for alias in node.names):
                wildcard_config_imports.append(path)

    mutable_state_markers = {"conversation_history", "no_rag_counter", "last_retrieval_docs"}
    mutable_session_state = sorted(
        {(path, attr) for path, attr in attrs if attr in mutable_state_markers}
    )

    routing_files = {
        path
        for path, name in functions
        if name in {"analyze_user_input", "judge_rag_and_classify", "route", "dispatch"}
        or "route" in name
    }
    # A typed route decision is also valid evidence when execution lives in
    # another module. This captures contract-first runtimes without requiring
    # a monolithic route() function.
    routing_files.update(
        path for path, name in classes if name in {"routedecision", "router", "routerprotocol"}
    )
    execution_files = {
        path
        for path, name in functions
        if name in {"generate_response", "execute", "run", "invoke"}
    }

    routing_boundary = bool(routing_files and execution_files and (routing_files - execution_files))

    abstraction_tokens = ("executor", "adapter", "protocol", "interface")
    executor_abstraction = any(any(t in name for t in abstraction_tokens) for name in class_names)

    capability_registry = (
        any("registry" in name for name in class_names)
        or "capability_registry" in combined
        or "executor_registry" in combined
    )

    structured_contracts = (
        "pydantic" in combined
        or "basemodel" in combined
        or "typeddict" in combined
        or "@dataclass" in combined
        or "dataclasses" in combined
    )

    output_validation = (
        "model_validate" in combined
        or "parse_obj" in combined
        or "jsonschema" in combined
        or any("validator" in name or "validate" in name for name in function_names | class_names)
    )

    model_gateway = (
        "modelgateway" in combined
        or "model_gateway" in combined
        or any("gateway" in name and "model" in name for name in class_names)
    )
    provider_boundary = model_gateway and not direct_provider_calls

    state_externalization = not bool(mutable_session_state)

    observability_hooks = (
        "opentelemetry" in combined
        or "structlog" in combined
        or "trace_id" in combined
        or "span_id" in combined
        or "tracesink" in combined
        or '"event":' in combined
        or "logging." in combined
        or "logger." in combined
    )

    retry_evidence = bool(re.search(r"\bretry\b|\bretries\b|backoff", combined))
    timeout_evidence = bool(timeout_calls) or bool(re.search(r"\btimeout\b", combined))
    resilience_boundary = retry_evidence and timeout_evidence

    safety_tokens = ("safety", "acuity", "crisis", "self_harm", "suicid", "risk_router")
    safety_files = {
        path for path, text in sources.items() if any(token in text.lower() for token in safety_tokens)
    }
    generation_files = {
        path for path, name in functions if "generate" in name or "response" in name
    }
    independent_safety_boundary = bool(safety_files and (safety_files - generation_files))

    checks = {
        "routing_boundary": {
            "pass": routing_boundary,
            "evidence": {
                "routing_files": sorted(routing_files),
                "execution_files": sorted(execution_files),
            },
        },
        "executor_abstraction": {
            "pass": executor_abstraction,
            "evidence": sorted([{"path": p, "class": n} for p, n in classes if any(t in n for t in abstraction_tokens)], key=lambda x: (x["path"], x["class"])),
        },
        "capability_registry": {
            "pass": capability_registry,
            "evidence": "registry naming/static evidence",
        },
        "structured_contracts": {
            "pass": structured_contracts,
            "evidence": "pydantic/dataclass/TypedDict static evidence",
        },
        "output_validation": {
            "pass": output_validation,
            "evidence": "validator/schema static evidence",
        },
        "provider_boundary": {
            "pass": provider_boundary,
            "evidence": {
                "model_gateway": model_gateway,
                "direct_provider_calls": direct_provider_calls,
                "wildcard_config_imports": wildcard_config_imports,
            },
        },
        "state_externalization": {
            "pass": state_externalization,
            "evidence": [{"path": p, "attribute": a} for p, a in mutable_session_state],
        },
        "observability_hooks": {
            "pass": observability_hooks,
            "evidence": "logging/tracing static evidence",
        },
        "resilience_boundary": {
            "pass": resilience_boundary,
            "evidence": {
                "timeout_evidence": timeout_evidence,
                "retry_evidence": retry_evidence,
                "requests_with_timeout": timeout_calls,
            },
        },
        "independent_safety_boundary": {
            "pass": independent_safety_boundary,
            "evidence": {
                "safety_files": sorted(safety_files),
                "generation_files": sorted(generation_files),
            },
        },
    }

    passed = sum(1 for item in checks.values() if item["pass"])
    score = passed * 10

    return {
        "metric_version": "chassis-static-v0.1",
        "source_id": source_id,
        "upstream_commit": upstream_commit,
        "root": str(root),
        "python_file_count": len(sources),
        "syntax_error_count": len(syntax_errors),
        "syntax_errors": syntax_errors,
        "chassis_fitness_score": score,
        "checks_passed": passed,
        "checks_total": 10,
        "checks": checks,
        "raw_metrics": {
            "direct_provider_bypass_count": len(direct_provider_calls),
            "wildcard_config_import_count": len(wildcard_config_imports),
            "mutable_session_state_count": len(mutable_session_state),
        },
        "limitations": [
            "Static screening only; does not measure conversational quality.",
            "False positives/negatives are possible; dynamic replacement tests are required for ADR-000.",
            "A low score measures adaptation gap to Atento chassis, not scientific quality of the donor.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--upstream-commit")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    report = audit(args.root, args.source_id, args.upstream_commit)
    text = json.dumps(report, ensure_ascii=False, indent=2)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if report["syntax_error_count"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
