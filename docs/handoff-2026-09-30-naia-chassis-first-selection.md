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

`9e7f19e5edde1c315ca63bba34af3b66db0c0ecd`

## Governing rule

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
