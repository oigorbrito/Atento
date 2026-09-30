# PR #19 pre-merge classification — 2026-09-29

## Contract

This file classifies the **51-file reconciliation surface observed before cleanup**.

States:

- `KEEP` — canonical product/governance material intended for main.
- `HISTORICAL_ONLY` — evidence retained for traceability; no current decision authority.
- `REMOVE_BEFORE_MERGE` — candidate-specific executable/spike material that must not become active main architecture.
- `NEEDS_LOCAL_VALIDATION` — active harness/config/test surface that remains merge-blocked until executable validation is observed.

## KEEP — 16

- `AGENTS.md`
- `README.md`
- `docs/adr/ADR-000-fork-vs-greenfield.md`
- `docs/adr/ADR-001-naya-product-composition.md`
- `docs/adr/ADR-002-assistant-base-selection.md`
- `docs/adr/ADR-ANNA-001-therapeutic-base-selection.md`
- `docs/adr/ADR-APOLLO-001-fitness-nutrition-base-selection.md`
- `docs/documentation-map.md`
- `docs/evaluation/harness.md`
- `docs/handoff-2026-09-29-product-reset.md`
- `docs/product-concept-reset.md`
- `docs/reconciliation-2026-09-29.md`
- `docs/reconciliation-open-pr-evidence-2026-09-29.md`
- `docs/third-party.md`
- `evals/README.md`
- `roadmap.md`

## HISTORICAL_ONLY — 9

- `docs/evaluation/chassis-selection-research-2026-09-29.md`
- `docs/evaluation/chassis-selection-research-2026-09-29.yaml`
- `docs/evaluation/donor-candidate-comparison-research-2026-09-29.md`
- `docs/evaluation/history/assistant-base-finalist-comparison-2026-09-29.md`
- `docs/evaluation/openclaw-qualification-2026-09-29.md`
- `docs/research/CHASSIS-LETTA-SELECTION-V1.md`
- `docs/research/chassis-selection-v1/archive/FILE_LIST.txt`
- `docs/research/chassis-selection-v1/archive/README.md`
- `evals/evidence/psychat_adapter_change_surface_git.json`

These files may remain in main because they are explicitly evidence/history surfaces rather than active candidate execution surfaces.

## REMOVE_BEFORE_MERGE — 11

- `.github/workflows/psychat-fork-spike.yml`
- `evals/cases/psychat_multilingual_gold_v0.jsonl`
- `evals/cases/rag_v0.jsonl`
- `evals/chassis/openclaw/README.md`
- `evals/chassis/openclaw/assistant-hardening.json`
- `evals/chassis/openclaw/naya-effect-plugin/effect-protocol.mjs`
- `evals/chassis/openclaw/naya-effect-plugin/effect-protocol.test.mjs`
- `evals/chassis/openclaw/naya-effect-plugin/index.mjs`
- `evals/chassis/openclaw/naya-effect-plugin/openclaw.plugin.json`
- `evals/chassis/openclaw/naya-effect-plugin/package.json`
- `evals/chassis/openclaw_naya_probe.py`

Disposition:

- the 10 newly-added candidate artifacts above have already been removed from the PR diff;
- the historical PsyChat workflow existed on main, so PR #19 now deletes it;
- exact historical executable evidence remains recoverable from closed PR heads #1 and #17.

## NEEDS_LOCAL_VALIDATION — 15

- `.github/workflows/candidate-eval.yml`
- `evals/atentoeval/candidates.py`
- `evals/atentoeval/metrics.py`
- `evals/atentoeval/runner.py`
- `evals/atentoeval/schema.py`
- `evals/cases/core_v0.jsonl`
- `evals/chassis/donor_static_audit.py`
- `evals/config/benchmark_registry.json`
- `evals/config/candidates.json`
- `evals/config/release_gates.json`
- `evals/config/system_matrix.json`
- `evals/tests/test_candidates.py`
- `evals/tests/test_chassis.py`
- `evals/tests/test_metrics.py`
- `evals/tests/test_runner.py`

## Static governance checks already established

The current registry/harness source establishes:

```text
decision_authority = false
registry_is_not_shortlist = true
selection_state = DECISION_RESET
candidate_universe_complete = false
mixed_agent_selection_comparison_forbidden = true
```

All currently registered external Anna candidates remain `NOT_SELECTED`.

The candidate loader now fails closed if a registry attempts `SELECTED` while:

- `decision_authority=false`;
- `selection_state=DECISION_RESET`; or
- `candidate_universe_complete=false`.

## Merge gate

```text
DOCUMENT_RECONCILIATION = READY_FOR_REVIEW
HISTORICAL_EXECUTABLE_CLEANUP = COMPLETE
HOSTED_VALIDATION = INFRA_BLOCKED
LOCAL_EXECUTABLE_VALIDATION = PASS_EMPIRICAL
MERGE_AUTHORIZATION = NO
RUNTIME_PROMOTION = NO
```

The Actions result with no executable steps is not a code failure and is not a pass. Merge remains blocked on the active `NEEDS_LOCAL_VALIDATION` surface until an executable local validation is observed.


## Local executable validation result

A local reconstruction of the active Python validation surface from the PR head was executed outside GitHub Actions.

Observed:

```text
test_candidates = PASS
test_chassis = PASS
test_metrics = PASS
test_runner = PASS
TOTAL = 12/12 PASS
```

Covered materially:

- registry pin and identity validation;
- CI matrix selection;
- fail-closed rejection of `SELECTED` during `DECISION_RESET`;
- external candidate pin requirement;
- typed `PASS_STATIC` preservation;
- rejection of invented evidence status;
- chassis audit semantics;
- provider-bypass/session-state detection;
- metric scoring;
- by-agent-scope aggregation;
- critical-failure counting;
- rejection of release/selection gates mixing NAIA and Anna.

Configuration/data parsing:

```text
benchmark_registry.json = VALID_JSON
candidates.json = VALID_JSON
release_gates.json = VALID_JSON
system_matrix.json = VALID_JSON
core_v0.jsonl = VALID_JSONL
core_v0 cases = 7
core_v0 scopes = [ANNA, NAIA, SHARED]
duplicate case ids = 0
```

The GitHub Actions workflow itself was accepted sufficiently for GitHub to create the exact-head run/jobs, but hosted execution still stopped before steps because of account infrastructure.

Updated gate:

```text
LOCAL_EXECUTABLE_VALIDATION = PASS_EMPIRICAL
HOSTED_VALIDATION = INFRA_BLOCKED
CODE_FAILURE = NOT_ESTABLISHED
DOCUMENT_RECONCILIATION = READY
HISTORICAL_EXECUTABLE_CLEANUP = COMPLETE
```
