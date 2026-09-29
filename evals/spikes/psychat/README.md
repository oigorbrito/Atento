# PsyChat Fork Spike

Branch: `spike/psychat-fork-eval`

Pinned donor:
- repo: https://github.com/wink-wink-wink555/PsyChat
- commit: `5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4`

## Scope

This spike evaluates PsyChat as a donor for **BLOCO I — Knowledge / RAG**. It does not migrate production code and does not award Project Points by itself.

## Test batches

### Upstream baseline
- static Chassis Fitness audit;
- provider/change-surface audit;
- session-isolation audit;
- compile/runtime workflow when CI runner is available.

### Adapted-donor boundary
A thin Atento chassis is placed around a donor port without rewriting donor internals.

Current evidence: `adapted-baseline.md`.

A real-source session probe is available at
`real_isolation_probe.py`; it loads the pinned donor's actual
`core/rag_system.py` with deterministic external-dependency stubs.

```text
Route contract
→ CapabilityRegistry
→ PsyChatExecutorAdapter
→ donor port
→ ResultValidator
→ trace
```

Cross-cutting boundaries in the spike:
- ModelGateway protocol;
- external SessionStore;
- SafetyPolicy;
- timeout/retry wrapper;
- structured trace events.

The adapted boundary is tested independently of external API keys.

Two levels are deliberately separated:

- deterministic fake-port tests for chassis contracts and replaceability;
- real-source probe for donor response shape and session ownership.

The fake-port suite exposed a real integration defect: upstream
`RAGSystem.generate_response()` returns a mapping, not the string originally
assumed by the bridge. The bridge now normalizes the pinned donor response shape.

Static CFS is also separated into:

- **adapter-only CFS** — measures the Atento boundary itself;
- **composed CFS** — audits donor + adapter together so direct donor provider
  bypasses cannot be hidden by a clean wrapper.

## Decision evidence

The fork decision must compare:
- upstream CFS;
- adapted CFS;
- donor code retained;
- files touched to swap executor/provider;
- session isolation;
- safety enforcement;
- conversational/RAG quality when live donor execution is available.

Do not interpret this spike as a production migration.

## Current execution status

- branch is aligned with current `main` ancestry;
- deterministic local suite: **11/11 passed** on Python 3.13.5;
- adapter-only static CFS: **90/100**;
- executor replacement: PASS;
- rollback-by-route: PASS;
- capability extension without Registry/Runtime modification: PASS;
- real-source session isolation probe: **BLOCKED_BY_INFRA**;
- composed donor+adapter CFS: **BLOCKED_BY_INFRA**;
- GitHub Actions jobs continue to terminate with no executed steps.

BLOCO I remains `IN_PROGRESS`.
Project Progress remains unchanged.
ADR-000 remains undecided.
