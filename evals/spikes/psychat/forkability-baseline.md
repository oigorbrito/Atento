# PsyChat — Forkability Baseline

## Scope

- Donor: `wink-wink-wink555/PsyChat`
- Pinned commit: `5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4`
- Probe: `evals/spikes/psychat/forkability_probe.py`
- Purpose: measure whether Atento chassis boundaries can be introduced through explicit upstream extension seams without editing donor internals.

## Result

> **Explicit extension seams: 0/5**
>
> **Thin-wrapper feasibility without donor edits: LOW**

The same checks used by the repository probe were evaluated against the pinned upstream source.

## Findings

| Finding | Result |
|---|---|
| `RAGSystem` constructor accepts injectable dependencies | NO |
| `PsychologyAgent` constructor accepts injectable LLM client | NO |
| `VectorStore` constructor accepts injectable embedding client | NO |
| `RAGSystem` constructs `PsychologyAgent()` internally | YES |
| `RAGSystem` constructs `VectorStore()` internally | YES |
| Web layer creates global `rag_system = RAGSystem()` | YES |
| Session/cookie/user identity handling found in web layer | NO |
| Route protocol uses `YES,topic...` string parsing | YES |
| Runtime contains forced-RAG policy | YES |
| Runtime owns mutable conversation history | YES |
| Direct LLM HTTP posts | 2 |
| Direct embedding HTTP posts | 1 |

## Integration seams

| Seam | Result |
|---|---|
| inject LLM without donor edit | FAIL |
| inject vector store without donor edit | FAIL |
| inject agent without donor edit | FAIL |
| isolate web session without runtime/web edit | FAIL |
| replace string route protocol without agent edit | FAIL |

## Interpretation

This result changes the fork hypothesis.

A **pure external wrapper with zero donor edits is not a strong long-term chassis strategy**. The adapter contract probe can intercept methods dynamically, but doing that through monkeypatch-style runtime replacement would be brittle against upstream changes.

The defensible alternatives are now:

1. **fork patch** — modify a small, explicit donor surface to introduce dependency injection and structured contracts; or
2. **block-level donor/selective port** — adopt PsyChat primarily for **BLOCO I — RAG**, excluding its web/session chassis.

## Minimum likely fork patch surface

For the RAG core, the current source indicates at least these donor files require structural edits:

- `agent/psychology_agent.py` — inject Model Gateway / structured route output;
- `core/vector_store.py` — inject embedding gateway;
- `core/rag_system.py` — inject agent/vector/generator, remove direct provider path, externalize policy/session boundary.

For a **full application fork**, `web/interface.py` also requires change to remove the process-global session runtime.

Therefore:

```text
block-level RAG donor: >= 3 donor core files structurally touched
full application fork: >= 4 donor files structurally touched
```

This is a change-surface estimate, not a final migration-cost conclusion.

## Next test

Prototype the minimal fork patch and rerun:

- forkability probe;
- Chassis Fitness;
- adapter contract tests;
- actual donor compile/import;
- AtentoEval seed cases when provider/runtime execution becomes available.
