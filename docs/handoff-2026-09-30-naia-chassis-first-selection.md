# Handoff — Atento NAIA chassis-first selection — 2026-09-30

## Current state

Canonical repository:

`oigorbrito/Atento`

Branch:

`main`

Current decision state:

```ini
NAIA_BASE = NOT_SELECTED
NAIA_SHORTLIST = NOT_SELECTED
SELECTION_METHOD = ARCHITECTURE_FIRST
CHASSIS_GATE = PRIMARY
AUTHORITY_ISOLATION_GATE = SECONDARY
BENCHMARK_GATE = LATER
```

Latest architecture-selection policy:

`docs/evaluation/naia-architecture-first-chassis-selection-2026-09-30.md`

Latest policy clarification commit:

`d3f3eaff6b6971ef6213764b0598870ccad2c79e`

## Governing rule

Architecture and chassis are evaluated together as one object. The selection objective is the lowest defensible total adaptation and ongoing-maintenance cost; architectural repair, chassis integration, dependency/upstream friction, deployment, and upkeep contribute to the same envelope.

The **first selection parameter** is the candidate chassis with the **lowest defensible total adaptation and ongoing maintenance cost** for Atento's required properties. The goal is not a perfect chassis. Compare observed evidence and label estimates/unknowns; do not infer low cost from code size or architectural neatness alone.

Structural screening is prioritized because cross-cutting structural changes can create the largest maintenance and reconstruction burden. This is a cost criterion, not architecture for its own sake.

The policy's previous architecture-heavy weighted scoring table has been superseded. Compare the defensible total adaptation/maintenance burden first; preserve hard authority, isolation, persistence, and safety gates. Do not manufacture a precise total from unmeasured inputs.

Selection is based first on **high-replacement-cost structural properties**, not feature count or benchmark score.

```text
ARCHITECTURE_FIRST != ARCHITECTURAL_AESTHETICS
ARCHITECTURE_FIRST != FRAMEWORK_PREFERENCE
ARCHITECTURE_FIRST = HIGH_REPLACEMENT_COST_PROPERTY_SCREEN

BENCHMARK_SIGNAL != LOCAL_PROOF
BENCHMARK_SIGNAL != AUTHORITY_PROOF
BENCHMARK_SIGNAL != ISOLATION_PROOF
```

Classify every material gap as:

```text
LOCALIZED_REPAIR
COMPONENT_REPLACEMENT
CROSS_CUTTING_STRUCTURAL_REWRITE
```

Do not spend an expensive empirical battery on a candidate that already fails a high-cost structural gate.

## Candidate-test budget until first base choice

The universe contains **26 candidates**.

Three already have substantive exact-pin verification:

- OpenMausBot
- Gobii
- Octop

Therefore the remaining architecture-screen workload is **23 candidates**, not 26 new full batteries.

Planned funnel to the first NAIA base choice:

### Gate 1 — chassis/architecture
- **26/26 architecture screens complete**
- **25 candidates advance to Gate 2**
- **SelfAgent stops as a complete base candidate at its frozen pin**
- canonical result: `docs/evaluation/naia-architecture-gate1-screen-2026-09-30.md`

### Gate 2 — authority/isolation
- only survivors from Gate 1
- one targeted authority/isolation screen per survivor
- no predetermined full-battery count; candidates failing structural authority are stopped immediately

### Gate 3 — persistent runtime/recovery
- only survivors of Gates 1–2
- targeted tests for persistence, restart/recovery, scheduler/background authority and relevant state ownership
- reuse existing upstream evidence where the exact property and pin transfer

### Gate 4 — empirical comparison
Current planning target: **up to 10 deep candidates**, not 26.

For each deep candidate, execute only the smallest Atento-specific battery needed to resolve the remaining material deltas.

### First-choice gate

The first `NAIA_BASE` choice is made only after:

1. all candidates entering the deep-comparison set have their material architectural gaps classified;
2. authority/isolation residuals are tested or explicitly blocked;
3. relevant benchmark/evaluation evidence is normalized;
4. adaptation cost is recorded;
5. no unresolved hard failure remains for the selected candidate.

Therefore the planned workload is:

```text
26 architecture screens total
+ targeted authority/runtime tests only for survivors
+ up to 10 deep empirical candidate evaluations
= first-choice gate

NOT:
26 full batteries
```

The exact number of runtime assertions is intentionally not fixed in advance because the protocol stops early on structural failure and reuses sufficient existing evidence.

## Already completed

Do not repeat the exhaustive OpenMausBot battery.

Do not repeat the Gobii or Octop upstream suites merely because they are candidates.

Use their existing reports as evidence and test only their remaining Atento-specific deltas if they survive the architecture gate.

## Current priority set

The previous benchmark triage produced a provisional group for deeper investigation:

- OpenClaw
- QwenPaw
- Letta Code
- Rakazo
- Engram
- Gobii
- Octop
- NanoClaw
- AI Butler
- Kortix/Suna

This list is **not a final shortlist**. Revalidate it against the architecture-first gate before spending deep-test budget.

Engram may be treated as a component/memory donor rather than forced into the complete-chassis category.

## Operating instructions for next chat

Continue autonomously.

Do not provide micro-step updates.

Do not repeat completed batteries.

Gate 1 is complete. Continue with authority/isolation only for Gate-1 survivors, using the frozen residual ledger and existing exact-pin evidence before any local execution.

For each candidate, record:

```text
CHASSIS_STATUS
AUTHORITY_STATUS
ISOLATION_STATUS
PERSISTENCE_STATUS
REPLACEMENT_COST
EVIDENCE_SCOPE
NEXT_GATE
```

Eliminate structurally unsuitable candidates before runtime testing.

Keep `NAIA_BASE = NOT_SELECTED` until the first-choice gate is actually closed.

Do not convert benchmark signal into local qualification.

## Source hierarchy

- ADR-003: evidence-first engineering decision policy
- ADR-002: NAIA base-selection decision record
- architecture-first chassis policy: operational screening procedure
- candidate-specific verification reports: execution evidence
- historical comparison documents: non-authoritative unless explicitly reused



## Gate 1 closure update

```text
ARCHITECTURE_GATE_1 = COMPLETE_V1
ARCHITECTURE_SCREENED = 26_OF_26
ARCHITECTURE_SURVIVORS = 25
COMPLETE_BASE_STOPS = [SelfAgent]
NEXT_GATE = AUTHORITY_ISOLATION
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

Do not restart the 26-candidate architecture sweep. Gate 2 should stop early whenever an authority/isolation hard failure becomes structural, and should not execute vendor-default profiles merely to reconfirm already-known permissive behavior.


## Gate 2 static screen update

Canonical result:

`docs/evaluation/naia-authority-isolation-gate2-screen-2026-09-30.md`

```text
AUTHORITY_ISOLATION_STATIC_SCREEN = COMPLETE_V1
AUTHORITY_ISOLATION_SCREENED = 25_OF_25
VENDOR_DEFAULT_AUTHORITY_PASS = 0
AUTHORITY_ISOLATION_EMPIRICAL_PASS = 0
ADDITIONAL_GATE_2_STOPS = 0
```

Do not rerun vendor/default authority behavior. None of the 25 survivors can defensibly pass authority/isolation without an exact hardened composition, dependency freeze, or the one candidate-specific upstream-first prerequisite already recorded.

Next work is candidate-specific and evidence-minimizing: freeze only decision-relevant compositions, reuse exact-pin clauses already proved, run only missing negative authority/isolation checks, and stop on any cross-cutting structural authority repair.


## Gate-2 empirical frontier

Canonical record:

`docs/evaluation/naia-gate2-empirical-execution-frontier-2026-09-30.md`

```text
AI_BUTLER_EXACT_PIN_CI = PASS
AI_BUTLER_AUTHORITY_CLAUSES_TRANSFERRED = PASS_WITH_SCOPE
AI_BUTLER_GATE2 = ONE_RESIDUAL_COMPOSITION_TEST_REMAINING

NEXT_EMPIRICAL_COMPOSITION_TARGET = AI_BUTLER
LOCAL_CLONE_NETWORK = BLOCKED_DNS
COMPOSITION_EXECUTION = NOT_RUN
```

Do not restart broad candidate tests. The next executable evidence is only the frozen AI Butler NAIA/Anna two-runtime negative composition. If the environment cannot obtain the exact pin, preserve the block as executor infrastructure and continue non-redundant evidence work; do not mark the candidate failed.


## Gate-2 transferable-evidence frontier

Canonical record:

`docs/evaluation/naia-gate2-transferable-evidence-frontier-2026-09-30.md`

```text
FRONTIER = [AI Butler, AgentOS]
NEXT = AI Butler two-role negative composition
SECOND_READY = AgentOS hardened two-role composition
SHORTLIST = NOT_SELECTED
BASE = NOT_SELECTED
```

Do not treat the frontier as a product ranking. It is only the set whose exact-pin executed evidence already closes enough authority clauses to make an Atento-specific composition the next non-redundant test.


## Transferable-evidence frontier V2

```text
FRONTIER = [AI Butler, AgentOS, Octop, Rome, Engram]
NEXT_EMPIRICAL_TARGET = AI Butler
BROAD_UPSTREAM_RETEST_FOR_FRONTIER = FORBIDDEN_AS_REDUNDANT
SHORTLIST = NOT_SELECTED
BASE = NOT_SELECTED
```

Rome and Engram now have exact-pin CI-backed Gate-2 authority clauses. Octop already had exhaustive exact-pin execution. Only Atento-specific hardened composition deltas remain useful for these five.


## Gate-2 frontier V3 / exact-pin execution reconciliation

Canonical records:

- `docs/evaluation/naia-gate2-exact-pin-hosted-execution-reconciliation-2026-09-30.md`
- `docs/evaluation/naia-gate2-transferable-evidence-frontier-2026-09-30.md`

```text
FRONTIER_V3 = [
  AI Butler,
  AgentOS,
  Octop,
  Rome,
  Engram,
  Suna,
  Letta Code,
  RustFox
]

FRONTIER_COUNT = 8
NEXT_EMPIRICAL_TARGET = AI Butler
NEW_TECHNICAL_ELIMINATIONS = 0
SHORTLIST = NOT_SELECTED
BASE = NOT_SELECTED
```

Do not rerun broad upstream suites for frontier candidates.

Exact-pin automation reconciliation also found:

```text
Holt = green build CI only; authority clauses not closed
HubOS = green pre-commit only; authority clauses not closed

Rakazo = exact-pin CI failure, attribution pending
Gobii = exact-pin CI failure, attribution pending
PersonalJarvis = exact-pin CI failure, attribution pending
OpenGrokBot = exact-pin CI failure, attribution pending
```

Do not convert un-attributed CI failures into candidate elimination.


## Gate-2 frontier V4 / CI attribution

```text
FRONTIER = [
  AI Butler,
  AgentOS,
  Octop,
  Rome,
  Engram,
  Suna,
  Letta Code,
  RustFox,
  Rakazo
]

FRONTIER_COUNT = 9
NEXT_EMPIRICAL_TARGET = AI Butler
NEW_TECHNICAL_ELIMINATIONS = 0
SHORTLIST = NOT_SELECTED
BASE = NOT_SELECTED
```

Attribution blocks outside the frontier:

```text
Gobii:
  Bcc privacy contract fails at frozen pin
  + migration-test inconsistency
  not eliminated, not frontier-ready

PersonalJarvis:
  Society/MCP authority policy table incomplete for newly exposed routes
  localized repair, not eliminated

OpenGrokBot:
  CI failure itself is unrelated turn batching
  but mandatory consequential browser-effect gate remains absent
  not frontier-ready
```

Do not convert any of these blocks into structural elimination without the corresponding bounded repair test.


## Gate-2 frontier V5

```text
FRONTIER_COUNT = 12
FRONTIER = [
  AI Butler,
  AgentOS,
  Octop,
  Rome,
  Engram,
  Suna,
  Letta Code,
  RustFox,
  Rakazo,
  OpenMausBot,
  NanoClaw,
  QwenPaw
]

REMAINING_NON_FRONTIER = 13
NEXT_EMPIRICAL_TARGET = AI Butler
SHORTLIST = NOT_SELECTED
BASE = NOT_SELECTED
```

Do not rerun broad upstream suites for frontier candidates.

New exact-pin evidence:
- OpenMausBot: cross-platform authority/approval/routine tests passed.
- NanoClaw: 3033 primary tests + approval/permission/restart/security contracts passed.
- QwenPaw: contract/integration matrix passed with one scoped Python 3.13 PTY runtime failure set.

Canonical residual disposition for the remaining non-frontier candidates:

`docs/evaluation/naia-gate2-non-frontier-hosted-evidence-disposition-2026-09-30.md`


## Common Gate-2 composition harness V1

Canonical:
- `docs/evaluation/naia-gate2-common-composition-harness-v1-2026-09-30.md`
- `docs/evaluation/naia-gate2-common-composition-matrix-v1-2026-09-30.yaml`

```text
FRONTIER = 12 candidates
COMMON_ASSERTIONS = 72
NEXT_EXECUTION_TARGET = AI Butler

BROAD_RETEST = FORBIDDEN
SHORTLIST = NOT_SELECTED
BASE = NOT_SELECTED
```

All frontier candidates now use the same six black-box role-boundary assertions. Execute only listed candidate-specific add-ons. If an environment block prevents exact-pin composition, record `BLOCKED_ENVIRONMENT` and continue to the next candidate rather than changing the candidate result.


## Gate-2 execution attempt and current hard stop

First common-harness execution target: AI Butler.

Atento Actions run:

`36789543149`

```text
workflow accepted = YES
job created = YES
job failed before steps
checkout = NOT_RUN
composition assertions = NOT_RUN

LOCAL_GITHUB_DNS = BLOCKED
HOSTED_EXECUTOR = BLOCKED_BEFORE_STEPS
AI_BUTLER = BLOCKED_ENVIRONMENT
```

Do not repeat the same broken executor path for the remaining 11 frontier candidates.

Canonical block:
`docs/evaluation/naia-gate2-empirical-execution-infrastructure-block-2026-09-30.md`

Canonical phase gate:
`docs/evaluation/naia-gate2-evidence-exhaustion-gate-2026-09-30.md`

```text
STATIC_RESEARCH_LOOP = CLOSED_FOR_CURRENT_PINS
FRONTIER = 12
NON_FRONTIER = 13
GATE2_EMPIRICAL_PASS = 0
SHORTLIST = NOT_SELECTED
BASE = NOT_SELECTED
```

Resume only when an executor can materialize an exact pin or materially new exact-pin executed evidence appears.


## Composition execution currently blocked by executor infrastructure

Canonical:

`docs/evaluation/naia-gate2-composition-execution-block-2026-09-30.md`

```text
HARNESS = NAIA-GATE2-COMPOSITION-V1
EXECUTOR_GITHUB_DNS = BLOCKED
LOCAL_CANDIDATE_CHECKOUT = ABSENT
COMPOSITION_EXECUTION = BLOCKED_ENVIRONMENT

NEXT_EXECUTION_TARGET_WHEN_UNBLOCKED = AI Butler
```

Do not rerun upstream reconciliation. When an executable exact-pin environment exists, resume directly with the common six-assertion composition harness.


## Canonical Gate-2 execution blocker / resume queue

```text
BLOCKER_ID = NAIA-G2-EXEC-INFRA-2026-09-30-01
TYPE = executor_network
COMMON_HARNESS = NAIA-GATE2-COMPOSITION-V1
FRONTIER_BLOCKED = 12
CANDIDATE_STATE_CHANGE = NONE
```

Resume queue:

`docs/evaluation/naia-gate2-composition-execution-queue-v1-2026-09-30.yaml`

When executable exact-pin access returns, resume directly at AI Butler. Do not repeat upstream CI/source reconciliation and do not regenerate the frontier.


## Gate-2 common prerequisites now frozen

```text
COMMON_HARNESS = NAIA-GATE2-COMPOSITION-V1
BROKER_CONTRACT = FROZEN_V1

LOCAL_EXECUTION = BLOCKED_ENVIRONMENT
HOSTED_RUNNER_OBSERVED = UNASSIGNED (runner_id=0, steps=[])
BROKER_RUNTIME_INTEGRATION = NOT_RUN

GATE2_EMPIRICAL_PASS = 0
NEXT_CANDIDATE_WHEN_EXECUTABLE = AI Butler
```

Canonical assets:

- `evals/atentoeval/composition.py`
- `evals/config/naia_gate2_composition_v1.json`
- `evals/atentoeval/handoff_broker.py`
- `docs/evaluation/naia-gate2-handoff-broker-contract-v1-2026-09-30.md`
- `evals/results/naia_gate2_aibutler_blocked_2026-09-30.json`

Do not treat the existing synthetic `ISO6_explicit_broker_positive_control` helper under `tools/naia_gate2/aibutler` as Gate-2 evidence. The result validator intentionally rejects synthetic broker evidence.

## Maintenance-cost measurement audit

`docs/evaluation/naia-architecture-chassis-maintenance-cost-audit-2026-09-30.md`

Current audit status: 26/26 structurally screened; 0/26 full comparable total-cost measurements; NanoClaw has the only partial static touchpoint count. No total-cost winner is established.
