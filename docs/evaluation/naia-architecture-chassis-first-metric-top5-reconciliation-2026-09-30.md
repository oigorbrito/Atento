# NAIA first metric reconciliation and top-five measurement cohort — 2026-09-30

## Decision

The first candidate comparison metric is the **combined architecture/chassis adaptation and maintenance-cost envelope**:

```text
FIRST_METRIC = TOTAL_ARCHITECTURE_CHASSIS_ADAPTATION_AND_MAINTENANCE_COST
ARCHITECTURE_AND_CHASSIS = ONE_EVALUATION_OBJECT
COST_WINNER = NONE_ESTABLISHED
FINAL_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

Architecture and chassis are not separate competitors or score dimensions here. The comparison concerns the cost to adapt and keep the candidate's foundational system operating for Atento's required properties. It includes structural change, integration, dependency/upstream-update friction, deployment/topology, and operational upkeep.

No candidate currently has a complete, comparable, observed total-cost measurement. Consequently, the Top 5 below is a **priority cohort for the next comparable measurement**, not a claim that these are already the five cheapest, a final shortlist, or a runtime selection.

## Reconciled evidence state

The canonical maintenance-cost audit records:

- 26/26 candidates received static structural screening.
- SelfAgent is stopped as a complete-base candidate at its frozen pin because of cross-cutting structural gaps; this is not a timed maintenance-cost measurement.
- NanoClaw alone has partial static touchpoint counts (4–40 copied files in selected recipes, plus integration/dependency touchpoints). These are not elapsed maintenance cost or a complete Atento composition.
- Full comparable total-cost observations: 0/26.
- The Gate-2 composition attempt stopped before checkout and produced no candidate cost evidence.
- No cost winner can be named from current evidence.

Classification rule:

```text
OBSERVED_COST != STATIC_RISK_SIGNAL
PARTIAL_STATIC_TOUCHPOINT_COUNT != TOTAL_MAINTENANCE_COST
BLOCKED_ENVIRONMENT != CANDIDATE_FAILURE
TOP_5_MEASUREMENT_COHORT != FINAL_SHORTLIST
```

## Top 5 measurement-priority cohort

These five are selected for an initial common-profile comparison because the current record contains concrete, decision-relevant seams or prior exact-pin evidence that can support a bounded composition measurement. The order below is execution priority only; it does not imply lower cost.

| Priority | Candidate | Basis for inclusion | Cost evidence now | Missing evidence for the metric |
|---:|---|---|---|---|
| 1 | AI Butler | Exact-pin authority clauses transfer with scope; one residual two-role composition was identified as the next empirical target. | Static/transferable evidence only; composition unexecuted. | Same-profile NAIA/Anna composition diff, dependencies, touched paths, effort/rework, lifecycle and update friction. |
| 2 | NanoClaw | Only candidate with quantified static adaptation touchpoints across representative recipes; exact-pin suite and security contracts already exist. | Partial static measurement; not an Atento profile or maintenance observation. | Frozen Atento recipe, real composition, lifecycle operation, upstream update exercise and elapsed effort. |
| 3 | OpenMausBot | Exact-pin authority/approval/routine tests passed; remaining question is same-owner role composition. | Transferable exact-pin evidence; no adaptation-cost capture. | Same-profile role composition and measured change/dependency/maintenance surface. |
| 4 | QwenPaw | Exact-pin contract/integration matrix exists; its reported Python 3.13 PTY runtime failures are scoped and should not be conflated with cost. | Transferable exact-pin evidence; no profile-cost measurement. | Same-profile role composition and measured change/dependency/maintenance surface. |
| 5 | OpenClaw | Static screen describes a viable separate runtime/Gateway authority route and bounded hardening. | Static structural signal only. | Verify exact pin and freeze a comparable profile before measuring composition, operations, and update friction. |

The cohort is a practical first batch, not an exhaustive claim that other survivors are inferior. Reorder only if a newly verified exact-pin artifact or executable environment materially changes the cost-measurement readiness.

## Common measurement protocol for this cohort

Freeze the same Atento capability profile and capture, for each candidate:

1. Exact candidate pin, host/runtime, profile, and dependency lock.
2. Files added/copied and existing files changed, categorized as configuration, adapter/component, or core/cross-cutting.
3. Dependencies and transitive update surface.
4. Independent execution/control paths and role-specific runtime, state, memory, credential, tool, and scheduler identities.
5. Engineering wall time, failed attempts, and rework under the same scope.
6. One representative supported message/action path and restart/recovery operation.
7. An actual upstream update or a clearly marked NOT_EXERCISED result; do not infer update friction from static inspection.
8. Security/authority and isolation gates as hard pass/fail constraints, not cost tradeoffs.

Report raw observations and scope. Do not combine unmeasured inputs into a precise scalar. If one candidate cannot be materialized, record BLOCKED_ENVIRONMENT and continue; do not mark it eliminated.

## Reconciliation with canonical documents

This record clarifies, rather than changes, the existing decision:

- `docs/evaluation/naia-architecture-chassis-maintenance-cost-audit-2026-09-30.md` remains the evidence inventory and reports no measured total-cost winner.
- `docs/evaluation/naia-architecture-first-chassis-selection-2026-09-30.md` remains the selection policy; the first metric is combined architecture/chassis adaptation and maintenance cost.
- `docs/handoff-2026-09-30-naia-chassis-first-selection.md` remains the operational handoff, with Gate 2 and environment blocks intact.
- The Top 5 here means the first cost-measurement cohort only. It does not override the frozen Gate-2 frontier, convert transferable evidence into local proof, clear the executor block, select a shortlist, or promote a base.

## Next substantive gate

Resume measurement when an exact-pin executor can materialize candidate sources. Start at AI Butler as already queued; if that is still blocked, preserve the infrastructure block and proceed only with another cohort candidate that can be measured under the same frozen profile. Record the five candidates side by side before making a cost-based narrowing decision.

```text
NEXT = COMMON_PROFILE_COST_MEASUREMENT
CURRENT_EXECUTOR_BLOCK = PRESERVE_UNTIL_RESOLVED
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```
