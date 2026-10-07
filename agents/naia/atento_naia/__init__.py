from __future__ import annotations

import json
from pathlib import Path

ROLE = "NAIA"


def load_project(root: str | Path | None = None) -> dict:
    base = Path(root) if root is not None else Path(__file__).resolve().parents[1]
    data = json.loads((base / "project.json").read_text(encoding="utf-8"))
    if data.get("agent") != ROLE:
        raise ValueError(f"role mismatch: expected {ROLE}")
    return data
