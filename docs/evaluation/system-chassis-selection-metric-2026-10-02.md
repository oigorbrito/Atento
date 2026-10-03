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

## Application to existing results — 2026-10-03

This is a read-only adjudication of preserved repository evidence. No new candidate test or benchmark was executed for this update.

### Common-score availability

The current `evals/chassis/donor_static_audit.py` is a Python-only static scanner: it walks `.py` files and uses source-name/text/AST heuristics. Its own module contract says the score has no selection authority. It cannot be applied unchanged as a comparable score to the current mixed-language chassis cohort (for example, TypeScript and Go systems); absence of Python files would be a scanner applicability failure, not evidence that architectural checks fail.

Only one current-cohort-like numerical CFS result was located: PsyChat at 10/100. It is Anna/RAG-scoped and is not a matched score across system chassis. The historical 2026-09-29 six-donor screen selected Letta only as an architecture scaffold; it did not calculate a comparable global CFS and is not the current NAIA/Anna/Apollo selection.

### Existing evidence against the system eligibility gate

This matrix reuses the pinned first-sieve and Gate-2 records; it is not a fresh scan or a newly executed common suite.

| Current system candidate | Comparable CFS | Atento composition / blocking evidence | Cost | Current disposition |
|---|---|---|---|---|
| NanoClaw | `NOT_SCORED` | Three-role profile-derived probe: 7/7 harness tests pass; mapped SYS assertions are `PASS_WITH_SCOPE`; full system gate is `NOT_PASSED`. | Not measured comparably | Next residual probe; not eligible yet |
| AI Butler | `NOT_SCORED` | NAIA–Anna Gate 2: 6/6 common assertions `PASS_WITH_SCOPE`; exact tested pin has a separate scheduled security failure with seven reachable advisories. | Not measured comparably | Current pin blocked by security; requalify only on a repaired/refrozen pin |
| OpenClaw | `NOT_SCORED` | No matched three-role Atento run; strict role boundary requires separate runtime/Gateway composition, then isolation and recovery probes. | Not measured comparably | Unresolved / hold for composed proof |
| QwenPaw | `NOT_SCORED` | No matched three-role Atento run; audited sandbox-unavailable fallback can fail open and cron authority needs hardening. | Not measured comparably | Current profile blocked pending fail-closed proof |
| MindRoom | `NOT_SCORED` | No matched three-role Atento run; audited filesystem isolation is backend-dependent and incomplete on shared-runner/local paths. | Not measured comparably | Unresolved |
| Bob Labs | `NOT_SCORED` | Test definitions inspected but no hosted run found for the exact pin; Atento role-boundary mapping not demonstrated. | Not measured comparably | Unresolved |
| Ontheia | `NOT_SCORED` | Exact-pin host/WebUI CI passed; Atento agent/domain isolation and role mapping were not demonstrated. | Not measured comparably | Unresolved |
| OpenAkita | `NOT_SCORED` | Exact-pin build passed; Python/unit/integration/smoke/E2E jobs were skipped; Atento multi-role isolation not demonstrated. | Not measured comparably | Unresolved |
| Clawix | `NOT_SCORED` | Exact-pin lint/typecheck/test CI passed; reviewed tests use mocks and do not demonstrate Atento end-to-end role authorization. | Not measured comparably | Unresolved |
| Memoh | `NOT_SCORED` | No exact source commit frozen in the reviewed first-sieve record. | Not measured comparably | Pin required before qualification |

No current system candidate has a same-protocol CFS, and no candidate closes all mandatory Atento composition gates. Among the ten, zero are eligible for cost ranking. The prior PsyChat 10/100 CFS belongs to a different Anna/RAG donor scope and is excluded. The historical Letta result remains scaffold-only and outside this current cohort.

### Adjudication

```text
COMPARABLE_CFS_FOR_CURRENT_SYSTEM_COHORT = NONE
SYSTEM_PROFILE_DERIVED_NANOCLAW_PROBE = 7_OF_7_HARNESS_TESTS; PASS_WITH_SCOPE
SYSTEM_PROFILE_GATE = NOT_PASSED
AI_BUTLER_CURRENT_PIN = BLOCKED_BY_SECURITY_EVIDENCE
OTHER_SYSTEM_CANDIDATES = UNRESOLVED
COMPARABLE_COMPLETE_SYSTEM_COST_VECTORS = 0
ELIGIBLE_CANDIDATES_FOR_COST_RANKING = 0
SYSTEM_CHASSIS_WINNER = NONE
NEXT_PROBE_PRIORITY = NANOCLAW_RESIDUAL_COMPOSITION_GAPS
```

Thus NanoClaw remains the next probe priority based on existing evidence, not the selected winner. There is no defensible numeric cross-candidate score or winner in the available results.

To create a comparable chassis score, the ten CFS properties must be assessed with a language-neutral evidence rubric or equivalent verified analyzers for each candidate language and the same frozen profile. Keep unknown properties as `UNRESOLVED`, not zero. Treat CFS as a structural screening vector, then apply the full hard-gate suite; only surviving candidates may be compared on total cost. The CFS implementation itself states that static screening alone does not decide fork/selection.

## Official methodological references

- AWS Well-Architected, [REL13-BP01: define recovery objectives for downtime and data loss](https://docs.aws.amazon.com/wellarchitected/2024-06-27/framework/rel_planning_for_recovery_objective_defined_recovery.html): RTO/RPO are workload/business objectives used to select and evaluate recovery strategy; AWS does not prescribe universal values.
- AWS Well-Architected, [REL12: test reliability](https://docs.aws.amazon.com/wellarchitected/2022-03-31/framework/rel-failmgmt.html): test failure and recovery behavior and track KPIs, RTO, and RPO. These references support defining local thresholds; they do not supply Atento-specific limits.


## Additional exact-pin functional benchmark check — 2026-10-03

The frozen AI Butler pin publishes an internal live-mode baseline of 4/7 tasks (57%), suite hash `28438749c91bd565…`, using Ollama Cloud `glm-5.1` on 2026-07-08: [exact-pin baseline](https://github.com/LumabyteCo/aibutler/blob/c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c/docs/eval/BASELINE.md). The baseline itself describes two failures as output-phrasing checks and one as a scripted error-then-recovery trajectory expectation; its same-suite comparison is only meaningful for equal suite hashes.

This is useful evidence that the pinned candidate has a reproducible functional-eval mechanism, but it is not the Atento three-role composition suite, does not test the frozen system hard gates, and has no matching NanoClaw run under the same benchmark. Therefore `4/7` must not be compared with NanoClaw's `7/7 PASS_WITH_SCOPE`, treated as a system score, or used to resolve AI Butler's separate exact-pin security blocker.

```text
AIBUTLER_INTERNAL_LIVE_EVAL = 4_OF_7 (57%); EXACT_PIN; MODEL_AND_SUITE_SPECIFIC
AIBUTLER_EVAL_COMPARABLE_TO_NANOCLAW_SYSTEM_PROBE = NO
SYSTEM_CANDIDATE_PRIORITY = NANOCLAW (strongest direct three-role Atento evidence)
SYSTEM_CHASSIS_ELIGIBILITY = NONE
SYSTEM_CHASSIS_WINNER = NONE
```


## Candidate continuation — current upstream and alternative screen — 2026-10-03

The latest NanoClaw upstream head checked for this continuation is `6906434bcb13eaeca1a6d8b461a1f2c22e53359f`. Its exact-head [CI run 37071400042](https://github.com/nanocoai/nanoclaw/actions/runs/37071400042) completed successfully: the CI gate, host/container test shards, and `iron-front` job passed. The tested Atento profile pin remains `4c1eabd3ddd74cc3d71b1871da857391a9411c8d`; the latest head is 15 commits ahead and adds/churns gateway, approval, Iron Proxy, and provider-overlay surfaces. Upstream CI is currentness evidence only: it does not transfer the Atento three-role probe to the newer pin, nor does it close process-restart, provider, real channel, scheduled firing/retry, or complete-composition assertions.

The public Agno Demo OS is a screened alternative, not an eligible replacement: its frozen project dependency is `agno[os]==2.8.1` at [the inspected project revision](https://github.com/agno-agi/demo-os/blob/985b72e2064a77a0c4cfc204f945a844f3d4db31/pyproject.toml). Agno issue [#9041](https://github.com/agno-agi/agno/issues/9041) documents a scheduler authorization confused-deputy issue; the issue was closed with maintainer and reporter comments saying the fix is in Agno 3.0. This means the inspected 2.8.1 Demo OS pin cannot be advanced for Atento's schedule-authority gate without a fixed, exact dependency pin and fresh qualification. This is a version-specific block, not a conclusion that all Agno 3.x compositions fail.

Candidate decision from available evidence:

- **NanoClaw is the leading candidate to qualify next**, because it is the only current system candidate with a direct three-role Atento profile-derived probe (7/7 harness assertions, all explicitly scoped) and now has green upstream CI at current HEAD.
- **NanoClaw is not yet eligible or the winner.** Its Atento evidence is tied to the older exact pin and leaves complete host/composition assertions open.
- **No alternative found in this continuation supersedes it.** Agno Demo OS is blocked at the inspected dependency pin; AI Butler remains blocked at its inspected pin by the recorded security evidence; the remaining matrix entries lack matched full-composition gate evidence.

The only defensible answer to “which candidate?” is therefore **NanoClaw, as the provisional qualification lead**. The selection result remains no eligible candidate and no winner until its current exact pin (or an explicitly frozen tested pin) passes all required composition gates and comparable cost vectors are recorded. The immediate product-side dependency is resolving the still-`TBD` Atento host topology and handoff contract in ADR-001 so the complete system boundary is testable; this is not recorded as a NanoClaw failure.

```text
PROVISIONAL_QUALIFICATION_LEAD = NANOCLAW
NANOCLAW_CURRENT_HEAD_UPSTREAM_CI = PASS (head 6906434; run 37071400042)
NANOCLAW_ATENTO_THREE_ROLE_EVIDENCE_PIN = 4c1eabd (7/7 harness; scoped)
NANOCLAW_SYSTEM_ELIGIBILITY = BLOCKED/UNRESOLVED
AGNO_DEMO_OS_INSPECTED_PIN = BLOCKED_PENDING_FIXED_AGNO_PIN_AND_REQUALIFICATION
ELIGIBLE_CANDIDATES = 0
SYSTEM_CHASSIS_WINNER = NONE
```

## Current-pin Atento residual probe — 2026-10-03

The same bounded probe was rerun against NanoClaw exact HEAD `6906434bcb13eaeca1a6d8b461a1f2c22e53359f`, with the profile pin, canonical topology hash, test pin assertion, and workflow checkout changed together. Atento Actions run [37096028670](https://github.com/oigorbrito/Atento/actions/runs/37096028670) succeeded: exact-pin verification, locked dependency installation, native SQLite build, inert test image pull, probe injection, and Vitest all completed successfully. The JUnit artifact was uploaded. The unchanged probe source contains seven `it(...)` assertions, so the current-pin result is 7/7 for this same bounded probe. The duplicate run [37096026143](https://github.com/oigorbrito/Atento/actions/runs/37096026143) for the same commit also succeeded.

The frozen-profile validator also passed with 12/12 candidate configs and no failures after the pin/hash update. This is stronger than the prior-pin evidence for container mount/session and brokered mailbox behavior, but the test scope is still unchanged: it does not start NanoClaw's full host, real provider/gateway or channel adapters, or prove host-process restart and actual three-role scheduled fire/retry/recovery. Assertions mapped to system requirements remain `PASS_WITH_SCOPE`, not full hard-gate passes. No cost vector was produced.

```text
NANOCLAW_ATENTO_PROFILE_PIN = 6906434bcb13eaeca1a6d8b461a1f2c22e53359f
NANOCLAW_ATENTO_BOUNDED_PROBE = PASS (7/7, hosted, run 37096028670)
FROZEN_PROFILE_VALIDATION = PASS (12/12 configs, zero failures)
SYSTEM_PROFILE_GATE = NOT_PASSED
ELIGIBLE_CANDIDATES_FOR_COST_RANKING = 0
SYSTEM_CHASSIS_WINNER = NONE
NEXT = CLOSE_FULL_HOST_PROVIDER_CHANNEL_BACKGROUND_AND_RESTART_GAPS; MEASURE_COMPARABLE_COST
```
