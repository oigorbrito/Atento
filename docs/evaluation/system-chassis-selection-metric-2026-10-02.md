# System chassis selection metric and minimum decision rule

- Status: proposed operational clarification for the system-level selection record
- Scope: complete Atento composition for NAIA, Anna, and future Apollo
- Authority: subordinate to ADR-003; operationalizes the metric already named by the system-level chassis re-screen

## Decision question

Select the eligible Atento composition with the lowest defensible total cost to adapt, deploy, operate, and maintain against the same product contract. The comparison object is the complete composition (platform/control plane, role runtimes, identity and state boundaries, tools/credentials, handoff, background execution, deployment and update model), not a repository or upstream benchmark in isolation.

This makes the repo's existing `TOTAL_ADAPTATION_AND_ONGOING_MAINTENANCE_COST` the primary selection metric. Architecture/change-surface signals help explain or estimate that cost; they are not a competing score. Task-quality, latency, token cost, and reliability benchmarks remain separate metric families and may only be compared after the relevant profile and workload are frozen.

## Minimum eligibility threshold (hard gates)

A candidate is eligible for cost ranking only when every mandatory system assertion in the frozen Atento profile has direct, in-scope evidence of passing for the complete composition. The minimum is:

- 100% of required hard-gate assertions pass in the defined test suite;
- zero unauthorized cross-role reads, writes, tool/credential use, or authority escalation in the tested cases;
- explicit handoff executes under receiver-side authority and consent rules;
- scheduled, retry, delegated, and recovery execution retain the same or narrower authority;
- persisted role state can be recovered within the product's predeclared RTO/RPO without stale or broader authority.

These are test-suite acceptance thresholds, not claims of mathematical proof beyond the tested cases. The suite must identify role pairs, positive and negative cases, fault points, exact candidate pins, composition, adapter, environment, and artifacts. A passing fixture or mock is component evidence unless it exercises the relevant boundary in the complete composition.

Classify results as `PASS`, `FAIL`, or `BLOCKED/UNRESOLVED`. Missing adapters, unavailable infrastructure, unexecuted tests, and evidence that does not cover the whole boundary are `BLOCKED/UNRESOLVED`, never implicit pass or candidate failure. Only demonstrated inability to enforce a required invariant, or a measured/architecturally evidenced unacceptable rewrite burden under a predeclared cost limit, can support elimination.

## Primary cost metric

Freeze the product profile, exact revisions, deployment assumptions, workload, observation horizon `T`, and cost-accounting rules before measuring candidates. Record these components separately:

1. discovery and qualification effort;
2. engineering effort and direct expense for adaptation/integration;
3. deployment and operating cost over `T`;
4. upgrades, incident/recovery work, security revalidation, and maintenance over `T`;
5. recurring services/infrastructure and other direct costs over `T`.

When a single numeric ranking is needed, calculate:

```text
C_total(T) = labor_cost(discovery + qualification + adaptation + deployment + maintenance + revalidation over T)
           + direct_cost(deployment + operation + upgrades + recovery over T)
```

Use a predeclared fully loaded labor rate and currency conversion date/method. Do not mix engineer-hours with dollars or infer labor cost from file/line counts. If the owner has not set labor rates, currency, horizon, or budget, report the cost vector (hours and direct spend by phase); do not invent one scalar or a budget pass/fail.

Among candidates that pass all hard gates and have comparable measurements, the primary choice is the lowest observed `C_total(T)`. Preserve candidate-level ranges/uncertainty. If cost difference is within measurement uncertainty, report a tie/inconclusive result rather than a fabricated rank. Any absolute budget ceiling is a separate business constraint and must be set before the run.

## Secondary metrics and benchmark rules

After eligibility, apply only predeclared metric families relevant to the frozen profile: functional quality/safety, reliability and recovery, latency, operational cost (for example cost per successful task), and capability coverage. Define workload, denominator, target, and minimum acceptable SLO for each before execution. No universal percentage from an external benchmark is an Atento threshold.

Do not average unlike measures (CFS, source-file counts, mutation counts, test pass rates, tokens, latency, dollars) into one chassis score. Do not let a good benchmark or low cost compensate for a hard-gate failure. External benchmark results can prioritize probes, but transfer only when population, protocol, pin, workload, and boundary match; otherwise label them external/contextual evidence.

## Comparison protocol

1. Freeze equivalent complete compositions, exact pins, role profile, deployment assumptions, and candidate-specific adapters.
2. Apply the same positive and negative system assertions and fault scenarios to each candidate; preserve artifacts and identify which test boundaries are direct versus mocked.
3. Measure cost components using the same work scope, role assumptions, observation horizon, labor rates, and accounting rules.
4. Mark each metric `PASS`, `FAIL`, `BLOCKED/UNRESOLVED`, or `NOT_APPLICABLE`, with scope and evidence links.
5. Rank only candidates that pass the hard gates and have comparable cost evidence. Report ties and unresolved candidates separately.

## Reconciliation with current Atento records

- `docs/evaluation/atento-system-architecture-chassis-rescreen-2026-09-30.md` defines the product-wide comparison object and first selection metric. This document makes its minimum decision rule executable.
- `docs/evaluation/system-chassis-benchmark-crosscheck-2026-09-30.md` records `COMPARABLE_THREE_ROLE_TOTAL_COST_RUNS = 0` and `SYSTEM_CHASSIS_HARD_GATES = DEFINED_NOT_EXECUTED`. Therefore the current outcome remains no winner and no eligible cost ranking.
- `docs/evaluation/naia-architecture-first-chassis-selection-2026-09-30.md` governs a NAIA role-base screen only. Its NAIA cohort, results, and test budget do not qualify or rank a complete NAIA/Anna/Apollo system.
- `docs/adr/ADR-003-evidence-first-engineering-decision-policy.md` controls evidence quality and requires uncertainty to remain explicit. This rule does not promote a candidate or relax that ADR.

## Current measured state

```text
PRIMARY_METRIC = TOTAL_ADAPTATION_AND_ONGOING_MAINTENANCE_COST
MINIMUM_ELIGIBILITY = 100_PERCENT_REQUIRED_HARD_GATE_ASSERTIONS_PASS; ZERO_OBSERVED_UNAUTHORIZED_CROSS_ROLE_ACTIONS
COMPARABLE_THREE_ROLE_TOTAL_COST_RUNS = 0
SYSTEM_CHASSIS_HARD_GATES = DEFINED_NOT_EXECUTED
SYSTEM_CHASSIS_WINNER = NONE
SYSTEM_CHASSIS_SHORTLIST = NOT_SELECTED
```

These values describe the records reviewed, not a newly executed test. `100_PERCENT` means all assertions in the declared finite suite, not universal assurance.

## Official methodological references

- AWS Well-Architected, [REL13-BP01: define recovery objectives for downtime and data loss](https://docs.aws.amazon.com/wellarchitected/2024-06-27/framework/rel_planning_for_recovery_objective_defined_recovery.html): RTO/RPO are workload/business objectives used to select and evaluate recovery strategy; AWS does not prescribe universal values.
- AWS Well-Architected, [REL12: test reliability](https://docs.aws.amazon.com/wellarchitected/2022-03-31/framework/rel-failmgmt.html): test failure and recovery behavior and track KPIs, RTO, and RPO. These references support defining local thresholds; they do not supply Atento-specific limits.

