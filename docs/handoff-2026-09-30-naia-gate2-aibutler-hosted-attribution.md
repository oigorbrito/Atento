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


## Continuation update — composition preparation after executor attribution

The hosted AI Butler failure has already been attributed elsewhere to runner provisioning:

```text
runner_id = 0
steps = []
AI_BUTLER_COMPOSITION = BLOCKED_ENVIRONMENT
AI_BUTLER_FAIL = NOT_CLAIMED
```

Do not repeat that hosted path until a runner is actually assignable.

Because blocked candidates are skipped for non-redundant work, composition preparation continued.

### OpenMausBot

Canonical freeze:

- `evals/config/naia_gate2_openmausbot_v1.json`
- `docs/evaluation/naia-openmausbot-gate2-hardened-composition-freeze-2026-09-30.md`

```text
OPENMAUSBOT_COMPOSITION = FROZEN_V1
topology = two independent runtimes / HOME / OMB_DATA_DIR / session+credential domains
native cross-role peer/ask_bot/delegation = forbidden
cross-role path = explicit Atento broker only
REPAIR_CLASS = LOCALIZED_REPAIR
EXECUTION = BLOCKED_ENVIRONMENT
```

The shared single-runtime/same-authority-domain topology is rejected as the Atento test topology; this is not a candidate failure.

### NanoClaw

Do not fabricate a recipe merely to advance the queue.

Current exact-pin evidence says the SUT identity depends on the installed channel/gateway/provider recipe. Until one representative Atento qualification recipe is selected and frozen, its `RECIPE-FREEZE` add-on remains unresolved.

```text
NANOCLAW_RECIPE = NOT_FROZEN
NANOCLAW_FAIL = NOT_CLAIMED
```

### AgentOS

Canonical freeze:

- `evals/config/naia_gate2_agentos_v1.json`
- `docs/evaluation/naia-agentos-gate2-hardened-composition-freeze-2026-09-30.md`

```text
AGENTOS_COMPOSITION = FROZEN_V1
permissions.default_mode = off
permissions.cron_default_mode = off
sandbox = on
browser = managed/headless, attach disabled, restricted qualification domain
topology = independent runtime/workspace/state/auth/credential/channel domains
cross-role path = explicit Atento broker only
REPAIR_CLASS = LOCALIZED_REPAIR
EXECUTION = BLOCKED_ENVIRONMENT
```

### Current substantive gate

```text
COMMON_GATE2_EXECUTOR = BLOCKED_ENVIRONMENT
AI_BUTLER = execution blocked, not failed
OPENMAUSBOT = composition frozen, execution blocked
NANOCLAW = recipe identity not frozen, candidate not failed
AGENTOS = composition frozen, execution blocked

AUTHORITY_ISOLATION_EMPIRICAL_PASS = 0
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

Execution resume order remains the frozen common-harness order when infrastructure is available. Static preparation may continue past blocked entries, but it must not alter that execution order or convert preparation into qualification.


## Gate-2 static preparation closure update

Canonical closure:

`docs/evaluation/naia-gate2-composition-preparation-frontier-v1-2026-09-30.md`

```text
GATE2_STATIC_COMPOSITION_PREPARATION = COMPLETE_V1
FROZEN_COMPOSITION_IDENTITIES = 12_OF_12
FROZEN_CONFIG_INTEGRITY = PASS
EXECUTION_ORDER = UNCHANGED

GATE2_EMPIRICAL_PASS = 0
NEW_TECHNICAL_ELIMINATIONS = 0
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

A dependency-free integrity checker is now versioned at:

`tools/naia_gate2/validate_frozen_configs.py`

It locks exact candidate/repo/SHA/harness identities, canonical topology/policy hashes and the exact assertion/add-on surface for all 12 frontier candidates.

### AI Butler

The pre-existing synthetic ISO-6 helper was removed from the executable evidence path.

The hosted harness now invokes the real Atento `ExplicitHandoffBroker` through:

`tools/naia_gate2/broker_runtime_adapter.py`

and validates/uploads a canonical result after candidate assertions pass.

```text
AI_BUTLER_REAL_BROKER_PATH = WIRED
AI_BUTLER_RESULT_VALIDATOR = WIRED
AI_BUTLER_POST_REPAIR_EXECUTION = NOT_OBSERVED
```

Do not claim Gate-2 PASS until a runner actually executes the repaired workflow.

### NanoClaw

Recipe ambiguity is closed from exact candidate-owned registry evidence:

```text
core = 4c1eabd3ddd74cc3d71b1871da857391a9411c8d
channels = 3f7e13b591a0c8980242b81ceff4b3f542ef839a
providers = 3959d1f055cba2320cf843b30834a278250346b8
channel = add-telegram / @chat-adapter/telegram@4.29.0
provider = add-codex / @openai/codex@0.155.1
gateway = add-onecli / gateway 1.41.0 / CLI 2.2.5 / SDK 2.2.1
```

Canonical:
- `evals/config/naia_gate2_nanoclaw_v1.json`
- `docs/evaluation/naia-nanoclaw-gate2-exact-recipe-freeze-2026-09-30.md`

Complete recipe runtime remains `NOT_RUN`.

### Engram

The previous one-AgentDef/two-identity composition remains an empirical FAIL for that exact composition.

Exact-pin source confirms:

```text
Job.agent_id
 -> task.agent
 -> AgentDef
 -> AgentDef.allowed_tools
 -> run_task_core ToolRegistry filtering
```

The new frozen composition uses separate interactive and scheduled AgentDefs:

```text
atento-naia-interactive ->
  [mcp_atento_browser_interactive_effect]

atento-naia-scheduled ->
  [mcp_atento_browser_scheduled_effect]
```

Canonical:
- `evals/config/naia_gate2_engram_v1.json`
- `docs/evaluation/naia-engram-gate2-split-agentdef-composition-freeze-2026-09-30.md`

```text
DUAL_IDENTITY_ONE_AGENTDEF = FAIL_EMPIRICAL_FOR_TESTED_COMPOSITION
SPLIT_AGENTDEF_COMPOSITION = FROZEN_V1_NOT_RUN
REPAIR_CLASS = LOCALIZED_REPAIR_PENDING_EXECUTION
```

Do not reinterpret the prior FAIL as repaired until the split-AgentDef runtime executes.

### Resume rule

Static preparation for the current 12-candidate frontier is now exhausted.

Resume empirical execution in the existing frozen order when a usable executor exists:

```text
1 AI Butler
2 OpenMausBot
3 NanoClaw
4 AgentOS
5 Rome
6 Suna
7 Rakazo
8 Letta Code
9 Octop
10 QwenPaw
11 RustFox
12 Engram
```

Do not restart Gate 1, static Gate 2, frontier discovery, broad upstream suites or composition-definition work without a material source/policy delta.


## 2026-10-01 chat-results consolidation

Canonical consolidated record:

`docs/evaluation/naia-gate2-chat-results-2026-10-01.md`

The decisive state change from this chat is:

```text
GATE2_STATIC_COMPOSITION_PREPARATION = COMPLETE_V1
FROZEN_COMPOSITION_IDENTITIES = 12_OF_12
FROZEN_CONFIG_INTEGRITY = PASS

AI_BUTLER_GATE2_COMPOSITION = PASS_WITH_SCOPE
AI_BUTLER_COMMON_ASSERTIONS = 6_OF_6_PASS
AI_BUTLER_ISO6 = PASS_RUNTIME_BROKER
AI_BUTLER_EVIDENCE_VALIDATOR = PASS
AI_BUTLER_ARTIFACT_PRESERVED = YES

GATE2_EMPIRICAL_PASS = 1
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

Accepted AI Butler evidence:

- run `36801793397`
- job `110177534395`
- artifact `11136566058`
- artifact zip SHA-256 `a9d13826c34b0e51c847e3a81226a14b57a21943f4362c7d069ed13c1421dae1`
- preserved result `evals/results/naia_gate2_aibutler_runtime_2026-10-01.json`
- result record `docs/evaluation/naia-aibutler-gate2-empirical-result-2026-10-01.md`

The old synthetic ISO-6 run is not accepted evidence. The accepted run exercised the real Atento `ExplicitHandoffBroker` path and passed the canonical result validator.

PR #56 was an evidence-observability probe only and was closed without merge.

### Current resume point

The frozen queue now advances to:

```text
2 OpenMausBot
```

OpenMausBot runtime harness mapping has started:

- exact pin inspected;
- isolated HOME / `OMB_DATA_DIR` test infrastructure identified;
- real server e2e harness identified;
- peer visibility, delegation and routine authority surfaces identified.

No OpenMausBot common Gate-2 runtime result exists yet.

Resume by building/running the minimum exact-pin **two independent OpenMausBot authority-domain** composition for:

```text
ISO-1
ISO-2
ISO-3
ISO-4
ISO-5
ISO-6
SAME-OWNER-ROLE-BOUNDARY
```

Then preserve the canonical result before advancing to NanoClaw.

Do not repeat AI Butler common Gate-2 execution unless its frozen identity changes materially.
