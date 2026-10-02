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
