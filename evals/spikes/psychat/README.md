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

Current evidence:

- `evidence-matrix.md` — canonical status ledger; separates PASS, pending execution, infra blockers and quality risks;
- `adapted-baseline.md` — detailed architectural baseline and interpretation;
- `index-migration-evidence.md` — QA provenance, vector metric/index migration and lifecycle experiment record;
- `docs/evaluation/donor-candidate-comparison-research-2026-09-29.md` — reconciled record of external benchmark research, Git methodology and empirical donor-comparison findings from this research cycle.

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

- branch remains aligned with current `main` ancestry;
- do not rely on a hard-coded test-count snapshot; the current suite evolves on
  the spike and evidence status is tracked in `evidence-matrix.md`;
- the historical **11/11** local result predates the current suite and must not
  be used as evidence for the present HEAD;
- the historical adapter-only **CFS 90/100** was produced under the older
  ownership heuristic and is not the current CFS result;
- Git change-surface is now split into two independently measured costs:
  **3 donor files** for the provider/lifecycle boundary and **4 donor files**
  for full BLOCO I RAG correctness/traceability after including
  `data/processor.py`;
- executor/capability/provider replacement and dynamic chassis assertions are
  encoded, but results that require Python execution remain pending on the
  current HEAD;
- real-source session isolation and composed CFS remain
  **BLOCKED_BY_INFRA**;
- GitHub Actions jobs continue to terminate before runner steps are created,
  and job logs are not materialized;
- an independent one-command Actions smoke workflow reproduces the same failure
  on both `ubuntu-latest` and `ubuntu-24.04`, isolating the problem from the
  BLOCO I workflow content;
- the pinned donor contains 12 knowledge text files but no committed
  `storage/` vector index; semantic retrieval therefore requires an index
  rebuild with a functioning embedding provider;
- paired `pt-BR` / `zh-CN` gold controls are now defined for PsyChat IDs
  328, 350, 1864 and 1882 so multilingual retrieval quality can be measured
  independently from chassis quality;
- the pinned upstream parser loses `qa_id` on all **4,760 / 4,760** dialogue
  sections because IDs precede the `##` dialogue delimiter; the BLOCO I
  processor patch carries the ID forward and source-level corpus validation
  preserves all 4,760 IDs;
- the patched vector collection explicitly uses cosine distance so the donor's
  existing `1 - distance` transform has cosine-similarity semantics;
- the current v0.20 experimental lifecycle variant adds explicit-only generation
  GC requiring quiescence confirmation; this is benchmark/forkability research,
  not a production architecture decision;
- the benchmark environment owns an exact Chroma constraint in
  `constraints.txt`, while the donor's original `chromadb>=0.4.0` remains
  recorded as upstream reproducibility evidence.

No stale historical PASS is promoted to the current HEAD.

BLOCO I remains `IN_PROGRESS`.
Project Progress remains unchanged.
ADR-000 remains undecided.


## Research-only boundary

Everything in this directory is part of empirical research, benchmark
instrumentation or forkability experiments for BLOCO I.

In particular:

- patched donor snapshots are experimental variants used to measure adaptation
  cost and behavior;
- dependency pins here belong to the benchmark environment;
- static Git evidence is not promoted to runtime PASS;
- external benchmark/provider documentation is contextual evidence and never
  substitutes for local Atento execution;
- no experiment in this spike is automatically adopted into production Atento
  architecture.

ADR-000 remains the decision boundary.
