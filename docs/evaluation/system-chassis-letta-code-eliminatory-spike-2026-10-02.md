# Letta Code eliminatory spike — 2026-10-02

## Candidate and scope

Frozen candidate: `letta-ai/letta-code@21daa38a8cdd74f2d03b634c8312253080bacfc1` (commit dated 2026-09-29). This is a bounded eliminatory preflight, not Atento composition or production qualification. No source files were changed; no provider credentials or model calls were used.

PR #58 was checked during this spike: it remains open and draft at head `e948f344b91e20e655399b11300c439228d144ec`. It was not modified.

## Exact-pin and local evidence

- Checkout: disposable clone `letta-code-pin`; `git rev-parse HEAD` returned `21daa38a8cdd74f2d03b634c8312253080bacfc1`.
- Repository `package.json` pins package manager `bun@1.3.14`, requires Bun >=1.3.2, and requires Node >=22.19.0.
- Available Node is v24.19.0. Bun was initially absent. The exact Bun 1.3.14 runner was obtained through `npx`; dependencies were installed from the frozen lockfile with install scripts disabled. The candidate checkout remained clean (no source, manifest, or lockfile diff).
- The local repo guide specifies Bun for source tests (`bun test`) and requires runtime-sensitive tests on the source path and built Node artifact. This spike only covers the selected source component tests.

The first direct invocation failed before test start because `bun` was not on PATH (exit 127). After supplying the exact runner, three existing focused schedule tests were run sequentially:

| Test file | Result | Scope |
|---|---:|---|
| `src/cron/cron-file.test.ts` | PASS, 52 tests / 122 assertions | Schedule persistence APIs, identity filtering, status transitions, scheduler lease/lock behavior, garbage collection and jitter. |
| `src/cron/scheduler.test.ts` | PASS, 31 tests / 87 assertions | Scheduler lease/tick behavior, schedule matching, dedupe, lifecycle and pre-fire revalidation. |
| `src/cron/runner.test.ts` | PASS, 16 tests / 29 assertions | Runner selection and Cloud schedule input/target mapping. |

These are scoped unit tests. They do not simulate a real task claim, host-process crash/restart, retry delivery, or Atento role ownership across an integrated runtime.

## Gate result

```text
PIN_IDENTITY = VERIFIED
BUN_1.3.14 = AVAILABLE_VIA_NPX
FOCUSED_CRON_TESTS = PASS_WITH_SCOPE (99 tests / 238 assertions)
ATENTO_HOST_RUNTIME_PROVIDER_SEAM = NOT_PRESENT_IN_AUDITED_ATENTO_STATE
NAIA_TASK_RETRY_AFTER_HOST_RESTART = BLOCKED_ADAPTER
NEW_CANDIDATE_ELIMINATION = NONE
END_TO_END_QUALIFICATION = NOT_ESTABLISHED
```

The repository is Letta Code, a CLI that connects to Letta agents; the inspected Atento records still say there is no product host/provider gateway adapter for the frozen cohort. Passing schedule component tests does not demonstrate the requested Atento-owned scheduled-task recovery. Historical overlay evidence is at another SHA and remains non-transferable.

## Smallest falsifiable next test

The remaining Atento-level test requires:

1. An executable Atento host/runtime adapter for this exact pin, without building a production integration solely to unlock the evaluation.
2. A synthetic Letta test backend or inert seam that creates no provider call.
3. Observable task identity/owner, claim, retry, terminal acknowledgement, and delivery IDs.

Then run one disposable probe only: create one inert due NAIA task with a synthetic identity; persist it; terminate the host after claim but before terminal acknowledgement; restart; allow exactly one retry; assert the owner remains NAIA and exactly one terminal delivery is recorded. Do not run parallel jobs. Reuse upstream tests already cited in the common-cohort record and do not repeat NanoClaw, Memoh, the 7/7 assertions, or the approved SSE replay.

## Disposition

`LETTA_CODE_CURRENT_PIN = PASS_WITH_SCOPE (FOCUSED_COMPONENTS); ATENTO_RECOVERY = BLOCKED_ADAPTER`. Missing integration evidence is not a failure and does not technically eliminate Letta Code. Keep the scheduled-task recovery gate blocked until an executable adapter exists.

This record is on `codex/disposable-nanoclaw-mobile-replay-20261001` only. PR #58 remains unchanged.


## Continuation check — 2026-10-02

The follow-up check found no executable Atento host/runtime/provider adapter for the scheduled-task probe in the reviewed current records:

- PR #58 remains open and draft at head `e948f344b91e20e655399b11300c439228d144ec`; its current description still lists product gateway/provider wiring and task retry/recovery as unqualified.
- PR #57 remains an open draft for the evaluation-only host/runtime boundary contract; its description says it is documentation-only and does not add product runtime.
- The checked current open-PR results also include PR #55 (GitAgent/OpenGAP control-plane assessment) and PR #35 (transfer audit). Neither is an implementation of the missing Atento runtime seam.
- No executable seam was identified in the checked current PR/document records. This does not make missing evidence a candidate failure.

```text
LETTA_CODE_FIXED_COHORT_ORDER = 11_OF_11
NEXT_CANDIDATE_IN_FROZEN_COHORT = NONE
NAIA_TASK_RETRY_AFTER_HOST_RESTART = BLOCKED_ADAPTER
NEW_RUNTIME_IMPLEMENTATION_FOUND = NO
NEXT_ACTION = WAIT_FOR_OR_PROVIDE_EXECUTABLE_HOST_RUNTIME_SEAM
```

The frozen candidate queue is exhausted at Letta Code. Do not add an out-of-cohort candidate to this run or repeat scoped tests while the Atento adapter is absent. The falsifiable probe and prerequisites above remain the next gate once an executable seam exists.


## Additional eliminatory gate — cross-agent memory access — 2026-10-02

At the user's direction, one different exact-pin gate was tested: whether in-process file and memory tools deny paths owned by a different agent.

Command, run on the frozen checkout with Bun 1.3.14:

```text
npx --yes bun@1.3.14 test src/permissions/cross-agent-guard.test.ts
63 pass
0 fail
102 expect() calls
```

The suite exercises self/parent/foreign agent scope; Read, Write, Glob, Grep, LS, NotebookEdit, and ApplyPatch path classification; ancestor-path and symlink escapes; local-backend MemFS; and permission-mode integration. The exact checkout remained at 21daa38a8cdd74f2d03b634c8312253080bacfc1; git status and the tracked-file diff were clean after execution.

Limits observed in the same passing suite:

- The guard is enabled by default, but a parent process can explicitly disable it with the CLI override. Tests confirm the override permits foreign memory in acceptEdits mode. Atento would need to own and pin this configuration; the suite does not prove an external authority boundary.
- Shell commands are intentionally left to the kernel sandbox. This test file verifies that the in-process guard defers shell access; it does not execute or qualify Letta Code's kernel sandbox.
- All cases are isolated unit/integration fixtures. They do not exercise Letta Code inside an Atento adapter, real OS identities, or the candidate's deployed runtime.

```text
CROSS_AGENT_IN_PROCESS_MEMORY_GUARD = PASS_WITH_SCOPE (DEFAULT_CONFIGURATION)
GUARD_OPERATOR_BYPASS = PRESENT_AND_TESTED
KERNEL_SANDBOX_BOUNDARY = NOT_TESTED_HERE
ATENTO_ROLE_MEMORY_ISOLATION = NOT_QUALIFIED
CANDIDATE_ELIMINATION = NONE
```

This adds scoped candidate evidence for the memory gate; it does not satisfy the common Atento SYS-MEM-01 composition assertion. No previously recorded NanoClaw, Memoh, 7/7, SSE replay, or Letta cron test was repeated.


## Superseding cohort continuation checkpoint — 2026-10-02

This section supersedes the earlier paragraph above that declared `NEXT_CANDIDATE_IN_FROZEN_COHORT = NONE` and said to wait. The user clarified that the governing goal is to run comparable eliminatory gates across every candidate not already technically eliminated, then choose only after the matrix is complete. We resumed the fixed cohort from the recorded checkpoint and have since run one scoped, exact-pin component gate each for QwenPaw, MindRoom, Bob Labs, Ontheia, OpenAkita, and Clawix, plus this distinct Letta Bubblewrap policy-construction gate. Outcomes and limits are recorded chronologically in `docs/evaluation/system-chassis-fixed-cohort-common-test-spike-2026-10-01.md`.

Letta result: `src/sandbox/bwrap.test.ts` passed 6 tests / 11 assertions on Bun 1.3.14. This verifies construction of Bubblewrap args (including denied-root masking, scoped carveouts, and die-with-parent) but does not launch Bubblewrap or prove kernel enforcement. Previously run Letta cron and cross-agent memory suites were not repeated.

```text
LETTA_BWRAP_POLICY_CONSTRUCTION = PASS_WITH_SCOPE
FIXED_COHORT_COMPONENT_GATES = CONTINUED_AFTER_LETTA
COMMON_ATENTO_NAIA_OWNERSHIP_AFTER_RESTART_RETRY = BLOCKED_ADAPTER
FINAL_CANDIDATE_SELECTION = NOT_MADE
PR_58 = UNMODIFIED
```

Continue the comparative gate matrix; do not treat the earlier queue-exhausted wording as current. No production runtime was added to unblock the test.
