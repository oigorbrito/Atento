#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROLES = ("NAIA", "ANNA", "APOLLO")
ROOTS = {
    "NAIA": Path("agents/naia"),
    "ANNA": Path("agents/anna"),
    "APOLLO": Path("agents/apollo"),
}
ALLOWED_SHARED = {"services/host"}
SCHEMA = "atento.logical-agent-project.v1"


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def load(role: str) -> dict:
    path = ROOTS[role] / "project.json"
    if not path.is_file():
        fail(f"{role}: missing {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{role}: invalid manifest: {exc}")
    if not isinstance(value, dict):
        fail(f"{role}: manifest must be object")
    return value


def main() -> int:
    seen_contexts: set[str] = set()

    for role in ROLES:
        m = load(role)
        if m.get("schema") != SCHEMA:
            fail(f"{role}: schema mismatch")
        if m.get("agent") != role:
            fail(f"{role}: agent mismatch")

        context = m.get("bounded_context")
        if not isinstance(context, str) or not context:
            fail(f"{role}: bounded_context required")
        if context in seen_contexts:
            fail(f"{role}: bounded_context must be unique")
        seen_contexts.add(context)

        runtime = m.get("runtime")
        if runtime != {"chassis": "nanoclaw", "group_isolation_required": True}:
            fail(f"{role}: runtime boundary must use isolated NanoClaw group")

        deps = m.get("dependencies")
        if not isinstance(deps, dict):
            fail(f"{role}: dependencies required")
        agent_deps = deps.get("agents")
        if agent_deps != []:
            fail(f"{role}: direct agent-to-agent dependency is forbidden")
        shared = deps.get("shared")
        if not isinstance(shared, list) or set(shared) - ALLOWED_SHARED:
            fail(f"{role}: unsupported shared dependency: {shared!r}")

        auth = m.get("authority")
        if not isinstance(auth, dict):
            fail(f"{role}: authority required")
        if auth.get("role_id") != role:
            fail(f"{role}: authority role mismatch")
        if auth.get("caller_selectable") is not False:
            fail(f"{role}: role authority must not be caller-selectable")

        # The experiment permits docs/tests/config below each role root, but no
        # cross-role filesystem imports/references are allowed in executable files.
        for path in ROOTS[role].rglob("*"):
            if not path.is_file() or path.name == "project.json":
                continue
            if path.suffix.lower() not in {".py", ".ts", ".tsx", ".js", ".jsx", ".sh"}:
                continue
            text = path.read_text(encoding="utf-8")
            for other in ROLES:
                if other == role:
                    continue
                needles = (
                    f"agents/{other.lower()}",
                    f"agents.{other.lower()}",
                    f"agents\\{other.lower()}",
                )
                if any(n in text.lower() for n in needles):
                    fail(f"{role}: executable cross-role reference in {path}: {other}")

    print("LOGICAL_AGENT_BOUNDARIES=PASS")
    print("DIRECT_AGENT_DEPENDENCIES=0")
    print("SHARED_DEPENDENCY=services/host")
    print("RUNTIME_CHASSIS=nanoclaw")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
