#!/usr/bin/env python3
"""PsyChat-specific forkability probe.

Measures whether Atento chassis boundaries can be added around the pinned donor
without rewriting donor internals. This is architecture evidence for ADR-000,
not a conversational-quality benchmark.
"""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path


def read(root: Path, rel: str) -> str:
    return (root / rel).read_text(encoding="utf-8", errors="ignore")


def class_init_params(source: str, class_name: str) -> list[str]:
    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name == "__init__":
                    return [a.arg for a in item.args.args if a.arg != "self"]
    return []


def count_direct_posts(source: str) -> int:
    tree = ast.parse(source)
    count = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name) and node.func.value.id == "requests" and node.func.attr == "post":
                count += 1
    return count


def probe(root: Path) -> dict:
    agent = read(root, "agent/psychology_agent.py")
    rag = read(root, "core/rag_system.py")
    vector = read(root, "core/vector_store.py")
    web = read(root, "web/interface.py")

    rag_params = class_init_params(rag, "RAGSystem")
    agent_params = class_init_params(agent, "PsychologyAgent")
    vector_params = class_init_params(vector, "VectorStore")

    findings = {
        "rag_constructor_injection": bool(rag_params),
        "agent_constructor_injection": bool(agent_params),
        "vector_constructor_injection": bool(vector_params),
        "rag_constructs_agent_internally": "PsychologyAgent()" in rag,
        "rag_constructs_vector_store_internally": "VectorStore()" in rag,
        "global_rag_singleton_in_web": "rag_system = RAGSystem()" in web,
        "session_identity_evidence": any(token in web.lower() for token in ("session", "cookie", "user_id")),
        "string_route_protocol": "YES,主题1,主题2" in agent and ".split(',')" in agent,
        "forced_rag_policy_in_runtime": "MAX_NO_RAG_ROUNDS" in rag and "force_retrieval=True" in rag,
        "mutable_conversation_history": "self.conversation_history" in rag,
        "direct_llm_posts": count_direct_posts(agent) + count_direct_posts(rag),
        "direct_embedding_posts": count_direct_posts(vector),
    }

    seams = {
        "inject_llm_without_donor_edit": findings["agent_constructor_injection"],
        "inject_vector_store_without_donor_edit": findings["rag_constructor_injection"] and not findings["rag_constructs_vector_store_internally"],
        "inject_agent_without_donor_edit": findings["rag_constructor_injection"] and not findings["rag_constructs_agent_internally"],
        "isolate_web_session_without_runtime_edit": not findings["global_rag_singleton_in_web"] or findings["session_identity_evidence"],
        "replace_string_route_with_schema_without_agent_edit": not findings["string_route_protocol"],
    }
    passed = sum(seams.values())

    return {
        "metric_version": "psychat-forkability-v0.1",
        "findings": findings,
        "integration_seams": seams,
        "seams_passed": passed,
        "seams_total": len(seams),
        "thin_wrapper_feasibility": "LOW" if passed <= 1 else ("MEDIUM" if passed <= 3 else "HIGH"),
        "interpretation": (
            "LOW means key Atento boundaries cannot be injected around upstream "
            "through explicit extension seams; donor edits or selective porting are required."
        ),
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", required=True, type=Path)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    result = probe(args.root)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
