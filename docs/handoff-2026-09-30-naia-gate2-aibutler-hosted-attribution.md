# HANDOFF — NAIA Gate 2 AI Butler hosted composition attribution — 2026-09-30

## Repository

`oigorbrito/Atento`

Branch:

`main`

## Current decision state

```text
FROZEN_CANDIDATE_UNIVERSE_V1 = 26
TECHNICAL_ELIMINATED = [SelfAgent]
TECHNICAL_SURVIVORS = 25

TRANSFERABLE_EVIDENCE_FRONTIER = COMPLETE_V5
FRONTIER_COUNT = 12

AUTHORITY_ISOLATION_EMPIRICAL_PASS = 0
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

License remains out of scope for technical selection.

## Frontier

```text
AI Butler
AgentOS
Octop
Rome
Engram
Suna
Letta Code
RustFox
Rakazo
OpenMausBot
NanoClaw
QwenPaw
```

Frontier entry is not shortlist, qualification, ranking or selection.

## Common Gate-2 composition harness

Canonical protocol:

`docs/evaluation/naia-gate2-common-composition-harness-v1-2026-09-30.md`

Machine-readable matrix:

`docs/evaluation/naia-gate2-common-composition-matrix-v1-2026-09-30.yaml`

Common assertions:

```text
ISO-1 cross-memory read
ISO-2 cross-memory mutation
ISO-3 cross-credential use
ISO-4 cross-tool/channel use
ISO-5 silent cross-role invocation
ISO-6 explicit broker positive control
```

Execution order begins with AI Butler.

## Local execution blocker

Canonical:

`docs/evaluation/naia-gate2-composition-execution-block-2026-09-30.md`

```text
BLOCKER_ID = NAIA-G2-EXEC-INFRA-2026-09-30-01
TYPE = executor_network
github.com DNS = BLOCKED
local candidate checkouts = ABSENT
```

Rule:

```text
EXECUTOR_INFRA_BLOCK != CANDIDATE_FAIL
```

This local blocker does not prevent hosted GitHub Actions execution.

## Hosted AI Butler composition path

Workflow:

`.github/workflows/naia-gate2-aibutler-composition.yml`

Injected test:

`tools/naia_gate2/aibutler/atento_gate2_test.go`

Exact AI Butler pin:

`LumabyteCo/aibutler@c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c`

Workflow behavior:

1. checkout Atento;
2. checkout exact AI Butler pin;
3. verify exact SHA;
4. setup Go 1.26.5;
5. inject `atento_gate2_test.go` under `candidate/internal/atento_gate2`;
6. execute:
   `go test ./internal/atento_gate2 -count=1 -v`.

## Hosted run already executed

```text
run_id = 36789543149
workflow = NAIA Gate2 AI Butler Composition
event = push
status = completed
conclusion = failure
head_sha = f5ea26ac9e9b3d9deb7382fffb49a9ce2fbec3f1
```

Observed check run:

```text
check_run_id = 110147437098
name = composition
status = completed
conclusion = failure
annotations_count = 2
annotations_url =
https://api.github.com/repos/oigorbrito/Atento/check-runs/110147437098/annotations
```

This is the newest material discovery.

Earlier job-log retrieval returned a 404/blob-not-found response, so the failure remains unattributed.

## Immediate next action

Read the 2 check-run annotations:

```text
GET /repos/oigorbrito/Atento/check-runs/110147437098/annotations
```

Then classify the failure as exactly one of:

```text
WORKFLOW/INFRASTRUCTURE
HARNESS_COMPILE_OR_API_DEFECT
ISO_PROPERTY_FAILURE
```

Do not mark AI Butler FAIL before this attribution.

## If annotations show harness/workflow defect

- make the smallest repair only;
- preserve the diff;
- rerun only the AI Butler hosted composition workflow;
- do not change candidate state.

## If annotations show ISO property failure

- map failure to ISO-1..ISO-6;
- classify:
  `FAIL_LOCALIZED` or `FAIL_STRUCTURAL`;
- rerun only the failed clause if localized;
- eliminate current pin only if repair requires cross-cutting structural rewrite.

## Current AI Butler test compatibility already checked

The injected test targets valid exact-pin APIs:

- `memory.NewStore`;
- `SaveThought`;
- `GetThoughts`;
- bank context scoping via `bank.With`;
- vault `New`, `Credential`, `ErrNotFound`;
- capability `NewEngine`, `NewCapabilitySet`, `CheckRequest`.

Actual memory implementation file is:

`internal/memory/memory.go`

not `internal/memory/store.go`.

Upstream exact-pin source also has direct bank-isolation tests, including cross-bank id-addressed mutation denial.

## Resume rules

Do not restart:

- Gate 1;
- static Gate 2;
- candidate reenumeration;
- frontier reconciliation;
- broad upstream CI/source audits.

Continue autonomously until a substantive gate.

If AI Butler hosted execution remains blocked by infrastructure after attribution, move to OpenMausBot using the same common harness pattern.

## Global rules

```text
BENCHMARK_SIGNAL != LOCAL_PROOF
LOCAL_PASS != PERFORMANCE_PROOF
IMPLEMENTED != QUALIFIED
AVAILABLE != QUALIFIED
EXECUTED != VERIFIED
VERIFIED != ACCEPTED
ACCEPTED != PROMOTED

CI_RED != AUTHORITY_FAIL
CI_GREEN != AUTHORITY_PASS
EXECUTOR_INFRA_BLOCK != CANDIDATE_FAIL
FRONTIER_ENTRY != SHORTLIST
FRONTIER_ENTRY != QUALIFIED
```

Fixed boundaries:

```text
chat access = isolated
memory authority = isolated
tool authority = isolated
silent role drift = forbidden
```

## User operating preference

- work in large batches;
- do not return every microstep;
- continue autonomously to substantive gates;
- skip environment/human blockers when possible;
- keep summaries compact.
