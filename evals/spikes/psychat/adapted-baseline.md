# PsyChat + Atento Chassis — Adapted Baseline

## Scope

- Atento branch: `spike/psychat-fork-eval`
- PsyChat donor: `wink-wink-wink555/PsyChat`
- Pinned donor commit: `5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4`
- Block: **BLOCO I — Knowledge / RAG**
- Project Progress impact: **none**. This is spike evidence, not a completed production block.

## Branch coherence

The spike was reconciled with `main` before continuing the experiment.

At the reconciliation point:

- `main`: `70e54082b99bb055d2cac672a027432da1cdd02a`
- spike merge commit: `3215339dc227dd88c1cba7a29fbbb2fb531594df`
- merge-base after reconciliation: current `main`
- behind `main`: **0**

No PR merge was performed. PR #1 remains draft/open.

## Deterministic adapter tests

Local deterministic execution on Python 3.13.5:

> **11/11 passed**

Covered behavior:

- external session isolation for distinct session IDs;
- restoration and extraction of donor state;
- prevention of accidental stateful donor reuse;
- executor replacement through `CapabilityRegistry`;
- route-level rollback from alternate executor to PsyChat;
- addition of a new capability without modifying Registry/Runtime;
- fail-closed behavior for unknown executor;
- rejection of invalid structured `RouteDecision`;
- tracing of executor/capability choice;
- chassis audit sanity checks.

### Integration defect found during the block

The first bridge test used a fake donor whose `generate_response()` returned a string.

The real PsyChat `RAGSystem.generate_response()` returns a mapping containing a `response` field.

Therefore the original bridge was not compatible with the pinned donor API even though the fake-based test passed.

The bridge was corrected to normalize:

- upstream mapping result → `result["response"]`;
- string result → string, for compatibility with narrow test donors;
- malformed/empty mapping → fail closed;
- unsupported result type → fail closed.

This finding is important evidence against treating fake-port tests alone as sufficient donor-integration proof.

## Chassis Fitness

### PsyChat upstream

Static baseline:

> **10/100**

See `static-baseline.md`.

### Adapter-only surface

Static audit of `evals/spikes/psychat/adapter`:

> **90/100**

PASS:

1. routing boundary
2. executor abstraction
3. capability registry
4. structured contracts
5. output validation
6. provider boundary **within the adapter tree**
7. observability hooks
8. resilience boundary
9. independent safety boundary

FAIL:

- state externalization

The static state check is conservative because the bridge references donor fields such as
`donor.conversation_history`, `donor.no_rag_counter` and
`donor.last_retrieval_docs` while restoring/extracting externally owned state.

### Important interpretation: adapter-only CFS is not composed-system CFS

The adapter contains a `ModelGateway` protocol and no direct provider HTTP calls.

The pinned donor underneath it still contains direct provider calls.

Therefore:

> **The real provider boundary is NOT yet solved by the thin wrapper.**

A composed donor+adapter static audit was added to CI so the adapter cannot hide donor bypasses by being audited in isolation.

The composed audit is not yet recorded as passed because GitHub Actions has not allocated a runner.

## Change-surface / replaceability

### Executor replacement

The runtime can register PsyChat and an alternate RAG executor simultaneously.

Switching between them is controlled by `RouteDecision.executor`.

Observed result:

- Registry modifications required: **0**
- Runtime modifications required: **0**
- replacement contract test: **PASS**
- rollback-by-route test: **PASS**

The final production metric `files_touched_to_swap_executor` should be measured again once the composition root is fixed, because registration wiring is currently inside the spike/test setup.

### Add capability

A second capability (`knowledge.lookup`) was registered and executed through the same Registry/Runtime.

Observed result:

- Registry modifications required: **0**
- Runtime modifications required: **0**
- capability-extension contract test: **PASS**

The final `files_touched_to_add_capability` must include the eventual executor implementation and composition-registration file; this spike only proves the chassis core does not need modification.

### Provider replacement

Still unresolved in the composed donor.

Pinned upstream evidence remains:

- LLM provider minimum change-surface: **3 files**
  - `config.py`
  - `agent/psychology_agent.py`
  - `core/rag_system.py`
- cross-provider implementation/config surface: **at least 5 files**

Therefore `files_touched_to_swap_provider` has **not improved yet** merely by wrapping PsyChat.

A fork patch or block-level selective port is still required to make the provider boundary real.

## Dynamic session-isolation probe

A real-source probe now exists:

`evals/spikes/psychat/real_isolation_probe.py`

It loads the pinned donor's actual `core/rag_system.py` and stubs only external dependencies
(provider/vector/TTS/data) so that `RAGSystem.generate_response()` remains donor code.

The probe checks two conditions:

1. one shared upstream `RAGSystem` instance carries session-A conversation state into the next conceptual session;
2. `PsyChatRagSystemPort` creates/restores isolated donor state so session-B receives only session-B state.

The upstream web source independently shows a process-global:

```python
rag_system = RAGSystem()
```

However, the dynamic probe has **not yet executed in CI**, so the upstream finding remains a
**cross-session isolation risk**, not a recorded confirmed leak.

## CI condition

Latest workflow attempts continue to finish before runner allocation:

- jobs are created;
- conclusion is reported as `failure`;
- job steps are absent / empty;
- no checkout, Python command, donor clone or test executes.

Classification:

> **INFRA FAILURE**

Do not record these runs as functional failures of PsyChat or the adapter.

## Current status

**BLOCO I — RAG: IN_PROGRESS**

Evidence now supports:

- the Atento chassis can improve replaceability around the donor;
- a fake donor can mask real API incompatibilities, so real-source probes are mandatory;
- the thin wrapper alone does not solve the donor's provider coupling;
- real-source session isolation and composed-system CFS remain blocked by CI infrastructure;
- AtentoEval RAG quality/cost/latency comparison remains pending.

Do not conclude ADR-000 from this baseline alone.
Do not increase Project Progress from this spike evidence alone.
