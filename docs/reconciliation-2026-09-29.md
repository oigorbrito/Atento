# Remote reconciliation report — 2026-09-29

## Scope

Repository:

```text
oigorbrito/Atento
```

Reconciliation base:

```text
main@a741fee5d57232083f0baee4aac26573673b7d07
```

Working PR:

```text
#19 — docs/concept-reset-part1-persistent-assistant
```

This report records a repository-wide reconciliation after a product-framing drift was identified.

The reconciliation rule was:

```text
PRESERVE EMPIRICAL EVIDENCE
RESET CONFUSED DECISION AUTHORITY
RESTORE PRODUCT IDENTITY
SEPARATE AGENT SCOPES
DO NOT SELECT A WINNER
```

## Restored product identity

```text
NAIA
  Nova Assistente Inteligente Artificial
  persistent personal assistant / secretary

Anna
  emotional / therapeutic assistant

Apollo
  nutrition / fitness / personal trainer assistant
  status: DEFERRED
```

The three agents are separate bounded domains.

Default cross-agent state:

```text
chat access       = isolated
memory authority  = isolated
tool authority    = isolated
silent role drift = forbidden
handoff topology  = NOT_SELECTED
```

## Decision state after reconciliation

```text
NAIA_BASE_WINNER = NOT_SELECTED
NAIA_SHORTLIST = NOT_SELECTED

ANNA_BASE_WINNER = NOT_SELECTED
ANNA_SHORTLIST = NOT_SELECTED

APOLLO_STATUS = DEFERRED
APOLLO_RESEARCH = NOT_STARTED

FORK_FULL_DONOR_NATIVE_STRATEGY = NOT_SELECTED
CROSS_AGENT_TOPOLOGY = NOT_SELECTED
```

Existing measurements do not grant shortlist status.

## Evidence explicitly preserved

The reconciliation did not delete:

- upstream repository pins and SHAs;
- benchmark references/results;
- static audit results;
- runtime observations;
- durability/security findings;
- gaps and blockers;
- change-surface measurements;
- provenance/terms notes;
- Project Points already earned;
- historical experiment IDs such as `OC-NAYA-*` when needed for traceability.

Historical labels such as `STRONG_CANDIDATE`, `FULL_DONOR_CANDIDATE`, `adoption HOLD`, preferred/non-preferred or finalist are retained only where they describe past audit state and are explicitly non-authoritative.

## Major reconciliation changes

### Product and governance

- added `docs/product-concept-reset.md` as provisional product-identity authority;
- added a self-contained handoff;
- updated `AGENTS.md` so the historical A–S architecture is not mandatory for all three agents;
- separated the historical `oigorbrito/NaIa` repository from **NAIA**, the current product agent;
- removed the stale Phase-8 completion dependency;
- preserved the 100-point ledger as historical/current evidence rather than pretending it is already the final three-agent architecture.

### ADRs

- ADR-000 reopened as historical strategy research / `DECISION_RESET`;
- ADR-001 preserves isolation requirements but concrete topology is not selected;
- ADR-002 resets the NAIA shortlist and preserves OpenMausBot/OpenClaw/historical-NaIa evidence;
- added ADR-ANNA-001 with `winner = NOT_SELECTED`, `shortlist = NOT_SELECTED`;
- added ADR-APOLLO-001 with `status = DEFERRED`.

### Evaluation harness

The previous seed corpus mixed personal-assistant and therapeutic cases without identifying the agent.

Reconciliation added explicit `agent_scope`:

- emotional-support / therapy cases → `ANNA`;
- business-hours external lookup → `NAIA`;
- cross-user privacy invariant → `SHARED`.

AtentoEval now:

- carries `agent_scope` into scored rows;
- reports metrics under `by_agent_scope`;
- supports `--agent-scope`;
- rejects release/selection gates that mix multiple primary agents;
- allows `SHARED` cases alongside one primary agent;
- marks static chassis scores as non-decisional evidence.

### Candidate registry

The candidate registry now explicitly records:

- `agent_scope`;
- `candidate_class`;
- `selection_status`;
- `decision_authority = false`;
- `registry_is_not_shortlist = true`;
- `candidate_universe_complete = false`.

Current Anna-related registry entries are evidence entries, not a shortlist.

### System matrix

Historical `atento_full` and its old ablations are preserved but disabled during the reset.

PsyChat/PsychAgent entries are marked evidence-only and not selected.

Simple baselines remain available as controls.

### Benchmarks

The existing benchmark registry is explicitly scoped primarily to **Anna**.

It is not treated as benchmark coverage for NAIA.

Apollo benchmark research is `NOT_STARTED`.

### CI/workflows

- generic candidate registry/schema validation can continue on PRs;
- donor-specific static execution is manual during the reset;
- the PsyChat fork-spike workflow is preserved for reproducibility but is manual-only;
- running a historical donor probe does not imply shortlist or priority.

### Dated research

Dated OpenClaw and donor-comparison records remain intact as evidence.

Their old next-step/finalist language is marked inactive or rewritten as historical methodology.

## Repository inventory review

Every blob in the PR head was reviewed for product/decision coupling.

| Path | Reconciliation disposition |
|---|---|
| `.github/workflows/candidate-eval.yml` | changed — donor execution manual during reset |
| `.github/workflows/psychat-fork-spike.yml` | changed — historical/manual only |
| `AGENTS.md` | changed — current governance/reset hierarchy |
| `README.md` | changed — three-agent identity |
| `docs/adr/ADR-000-fork-vs-greenfield.md` | changed — decision reset |
| `docs/adr/ADR-001-naya-product-composition.md` | changed — isolation preserved, topology reset; historical filename retained for link stability |
| `docs/adr/ADR-002-assistant-base-selection.md` | changed — NAIA selection reset |
| `docs/adr/ADR-ANNA-001-therapeutic-base-selection.md` | added |
| `docs/adr/ADR-APOLLO-001-fitness-nutrition-base-selection.md` | added |
| `docs/documentation-map.md` | changed — authority map reconciled |
| `docs/evaluation/donor-candidate-comparison-research-2026-09-29.md` | changed — historical evidence/methodology scope |
| `docs/evaluation/harness.md` | changed — agent-scoped evaluation |
| `docs/evaluation/openclaw-qualification-2026-09-29.md` | changed — evidence preserved, selection priority removed |
| `docs/handoff-2026-09-29-product-reset.md` | added |
| `docs/product-concept-reset.md` | added |
| `docs/third-party.md` | changed — provenance separated from selection |
| `evals/README.md` | changed — agent-scoped usage / no adapter priority |
| `evals/atentoeval/__init__.py` | reviewed — generic exports, no reconciliation change needed |
| `evals/atentoeval/candidates.py` | changed — candidate class/scope/selection metadata |
| `evals/atentoeval/gates.py` | reviewed — generic gate evaluator, no product-decision coupling |
| `evals/atentoeval/metrics.py` | changed — by-agent reporting |
| `evals/atentoeval/runner.py` | changed — filtering + mixed-agent gate protection |
| `evals/atentoeval/schema.py` | changed — explicit agent scope |
| `evals/cases/core_v0.jsonl` | changed — cases assigned to NAIA/Anna/SHARED |
| `evals/chassis/__init__.py` | reviewed — no change needed |
| `evals/chassis/donor_static_audit.py` | changed — static score explicitly non-decisional |
| `evals/config/benchmark_registry.json` | changed — benchmark agent scopes |
| `evals/config/candidates.json` | changed — evidence-only selection metadata |
| `evals/config/release_gates.json` | changed — agent-scoped selection policy |
| `evals/config/system_matrix.json` | changed — old architecture variants disabled |
| `evals/results/.gitkeep` | reviewed — no content |
| `evals/tests/test_candidates.py` | changed — selection metadata tests |
| `evals/tests/test_chassis.py` | changed — non-decisional CFS test |
| `evals/tests/test_gates.py` | reviewed — generic gates, no change needed |
| `evals/tests/test_metrics.py` | changed — agent-scope aggregation test |
| `evals/tests/test_runner.py` | added — mixed-agent gated run rejection |
| `roadmap.md` | changed — ledger preserved, architecture/selection authority reset |

## Known historical artifacts intentionally retained

The following are not current product decisions but remain for traceability:

- filename `ADR-001-naya-product-composition.md`;
- `SRC-NAIA` as the source ID for the historical `oigorbrito/NaIa` repository;
- `OC-NAYA-*` experiment IDs;
- historical `FULL_DONOR_CANDIDATE` provenance/status labels;
- historical A–S block names and existing Project Point ledger;
- PsyChat spike data and OpenClaw qualification evidence.

Renaming these identifiers would reduce provenance and is not required to restore decision correctness.

## What is now safe to infer

Safe:

```text
Atento has three agent domains.
NAIA and Anna need fresh comparable-candidate enumeration.
Apollo is deferred.
Existing evidence should be reused.
No base winner is selected.
```

Not safe:

```text
OpenClaw is a finalist because it was audited.
OpenMausBot is selected because it motivated the strategy.
PsychAgent is Anna's winner because it beat one inspected subset.
PsyChat is the Anna chassis because a spike exists.
A–S is already the final architecture of all three agents.
A registry/CI entry means adoption.
```

## Next engineering action

Do not begin another candidate-specific spike by inertia.

Next:

1. enumerate mature persistent-assistant chassis for NAIA;
2. enumerate mature complete therapeutic-agent chassis for Anna;
3. classify candidates before comparison;
4. map existing evidence to each comparable candidate;
5. identify only the missing material deltas;
6. then run the smallest decision-relevant probes.

Apollo remains deferred.

## Reconciliation outcome

```text
REMOTE_RECONCILED = YES
EVIDENCE_PRESERVED = YES
CONFUSED_DECISION_AUTHORITY = RESET
NAIA_WINNER = NOT_SELECTED
ANNA_WINNER = NOT_SELECTED
APOLLO = DEFERRED
```
