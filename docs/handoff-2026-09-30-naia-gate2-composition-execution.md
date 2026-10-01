# HANDOFF — NAIA Gate 2 composition execution — 2026-09-30

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

License is out of scope for the current technical selection.

## Transferable-evidence frontier

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

This is not a shortlist or ranking. It only means broad upstream retesting is now redundant for these candidates.

Canonical frontier:

`docs/evaluation/naia-gate2-transferable-evidence-frontier-2026-09-30.md`

## Common Gate-2 harness

Frozen protocol:

`docs/evaluation/naia-gate2-common-composition-harness-v1-2026-09-30.md`

Machine-readable matrix:

`docs/evaluation/naia-gate2-common-composition-matrix-v1-2026-09-30.yaml`

Common assertions per candidate:

```text
ISO-1 cross-memory read
ISO-2 cross-memory mutation
ISO-3 cross-credential use
ISO-4 cross-tool/channel use
ISO-5 silent cross-role invocation
ISO-6 explicit broker positive control
```

Total common assertions:

```text
12 candidates × 6 = 72
```

Candidate-specific add-ons are frozen in the matrix. Do not invent new broad suites.

## Execution order

Evidence-minimizing only, not ranking:

```text
1. AI Butler
2. OpenMausBot
3. NanoClaw
4. AgentOS
5. Rome
6. Suna
7. Rakazo
8. Letta Code
9. Octop
10. QwenPaw
11. RustFox
12. Engram
```

## Local executor blocker

Canonical blocker:

`docs/evaluation/naia-gate2-composition-execution-block-2026-09-30.md`

Machine-readable resume queue:

`docs/evaluation/naia-gate2-composition-execution-queue-v1-2026-09-30.yaml`

Blocker identity:

```text
BLOCKER_ID = NAIA-G2-EXEC-INFRA-2026-09-30-01
TYPE = executor_network

github.com DNS = BLOCKED
local exact candidate checkout = ABSENT
```

Observed shell evidence:

```text
git ls-remote https://github.com/LumabyteCo/aibutler.git HEAD
-> Could not resolve host: github.com
```

Rule:

```text
EXECUTOR_INFRA_BLOCK != CANDIDATE_FAIL
```

Do not duplicate the same environment block as twelve candidate failures.

## Important new discovery: hosted AI Butler composition path exists

The repository already contains:

`.github/workflows/naia-gate2-aibutler-composition.yml`

and:

`tools/naia_gate2/aibutler/atento_gate2_test.go`

The workflow:

1. checks out Atento;
2. checks out exact AI Butler pin:
   `c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c`;
3. verifies the exact pin;
4. injects the Atento Gate-2 Go test;
5. runs:
   `go test ./internal/atento_gate2 -count=1 -v`.

This hosted path bypasses the local DNS limitation.

## Hosted AI Butler run already executed

GitHub Actions run:

```text
run_id = 36789543149
workflow = NAIA Gate2 AI Butler Composition
event = push
status = completed
conclusion = failure
head_sha = f5ea26ac9e9b3d9deb7382fffb49a9ce2fbec3f1
display_title = ci(naia): run AI Butler Gate 2 composition
```

Job:

```text
job_id = 110138936806
name = composition
conclusion = failure
```

The connector did not expose job logs successfully; `fetch_workflow_job_logs` returned a 404/blob-not-found response. Therefore the failure is **not yet attributed**.

Do not classify AI Butler as FAIL until the failing step is identified.

## AI Butler test audit

Current injected test implements the six common assertions using AI Butler internals:

- bank-scoped memory;
- separate file vaults;
- capability engine/channel scope;
- absence of `agent.delegate`;
- simple explicit broker payload.

Exact test file:

`tools/naia_gate2/aibutler/atento_gate2_test.go`

Important source compatibility already checked:

- `internal/memory.NewStore` exists;
- `memory.SaveThought` / `GetThoughts` are bank-scoped;
- `bank.With(ctx, bank)` exists;
- `ForgetThought` rejects cross-bank ids in upstream tests;
- `vault.New`, `Credential`, `ErrNotFound` exist;
- `capability.NewEngine`, `NewCapabilitySet`, `CheckRequest` exist.

One earlier fetch path was wrong (`internal/memory/store.go` does not exist); actual implementation is in:

`internal/memory/memory.go`

This does not itself explain the workflow failure because imports target the package, not the file path.

## Immediate next action

Start from the failed hosted run, not from broad evidence research.

Required sequence:

1. inspect run `36789543149` through any available GitHub run/check/job endpoint that exposes the failing step or annotation;
2. determine whether failure is:
   - workflow/infrastructure;
   - compile/test harness defect;
   - AI Butler property failure;
3. if harness/workflow defect:
   - make the smallest repair;
   - preserve the diff;
   - rerun only AI Butler composition;
4. if candidate property failure:
   - classify the failed ISO clause;
   - determine `FAIL_LOCALIZED` vs `FAIL_STRUCTURAL`;
   - rerun only that clause if localized;
5. if AI Butler remains blocked by hosted infrastructure, move to OpenMausBot using the same common harness pattern.

Do not restart Gate 1, static Gate 2, frontier reconciliation or broad upstream CI audits.

## Early-stop rules

```text
localized config/profile defect
  -> repair once, rerun failed clause only

bounded middleware defect
  -> preserve diff, rerun failed clause only

cross-cutting structural rewrite
  -> eliminate current pin as complete base

environment/CI infrastructure failure
  -> BLOCKED_ENVIRONMENT, not candidate FAIL
```

## Non-frontier state

Still outside transferable frontier:

```text
OpenClaw
TrustClaw
Open Assistant
PersonalJarvis
Gobii
OpenGrokBot
GoClaw
Nebo
AutoMate
OpenAgentd
HubOS
Holt
Agent Zero
```

Canonical disposition:

`docs/evaluation/naia-gate2-non-frontier-hosted-evidence-disposition-2026-09-30.md`

Notable current-pin blocks:

```text
Gobii = Bcc privacy regression + migration inconsistency
PersonalJarvis = incomplete Society/MCP policy coverage
OpenGrokBot = consequential browser-effect gate still open
HubOS = fail-open/sessionless guard residual
Holt = external CLI authority seam not executed
```

None of those is currently a structural elimination.

## Global rules to preserve

```text
BENCHMARK_SIGNAL != LOCAL_PROOF
LOCAL_PASS != PERFORMANCE_PROOF
IMPLEMENTED != QUALIFIED
AVAILABLE != QUALIFIED
EXECUTED != VERIFIED
VERIFIED != ACCEPTED
ACCEPTED != PROMOTED
BENCHMARK_GAIN != TRANSFERABLE_GAIN

CI_RED != AUTHORITY_FAIL
CI_GREEN != AUTHORITY_PASS

EXECUTOR_INFRA_BLOCK != CANDIDATE_FAIL
FRONTIER_ENTRY != SHORTLIST
FRONTIER_ENTRY != QUALIFIED
```

Fixed Atento boundaries:

```text
chat access = isolated
memory authority = isolated
tool authority = isolated
silent role drift = forbidden
```

## User operating preference

Continue autonomously to substantive gates.

- Work in large batches.
- Do not return every microstep.
- Updates only for relevant discoveries or sufficiently long work.
- Do not use artificial “blocks” as progress units.
- Keep summaries compact to preserve context.
- Skip environment/human blockers and continue to the next candidate when possible.


## Update — hosted AI Butler failure attributed

Canonical:

`docs/evaluation/naia-gate2-hosted-runner-execution-block-2026-09-30.md`

Both workflow attempts failed before any step executed:

```text
attempt 1: runner_id=0, steps=[]
attempt 2: runner_id=0, steps=[]
```

Therefore:

```text
HOSTED_RUNNER_PROVISIONING = BLOCKED
AI_BUTLER_COMPOSITION = BLOCKED_ENVIRONMENT
AI_BUTLER_FAIL = NOT_CLAIMED
```

Do not debug the AI Butler Go assertions from these runs; they never executed.

Common Gate-2 result validation is now implemented in:

- `evals/atentoeval/gate2_composition.py`
- `evals/tests/test_gate2_composition.py`

Next real empirical step remains AI Butler once a runner is actually assigned. If hosted runners remain unavailable, continue only non-redundant harness/infrastructure work or move execution to another authorized environment with exact-pin access.
