# Letta Code eliminatory spike — 2026-10-02

## Candidate and scope

Frozen candidate: `letta-ai/letta-code@21daa38a8cdd74f2d03b634c8312253080bacfc1` (commit dated 2026-09-29). This is a bounded eliminatory preflight, not Atento composition or production qualification. No source files were changed; no provider credentials or model calls were used.

PR #58 was checked during this spike: it remains open and draft at head `e948f344b91e20e655399b11300c439228d144ec`. It was not modified.

## Exact-pin and local evidence

- Checkout: disposable clone `letta-code-pin`; `git rev-parse HEAD` returned `21daa38a8cdd74f2d03b634c8312253080bacfc1`.
- Repository `package.json` pins package manager `bun@1.3.14`, requires Bun >=1.3.2, and requires Node >=22.19.0.
- Available Node is v24.19.0. No Bun executable or installed `node_modules` is present.
- The local repo guide specifies Bun for source tests (`bun test`) and requires runtime-sensitive tests on the source path and built Node artifact.

One narrowly focused attempt against the existing schedule tests:

```text
bun test src/cron/cron-file.test.ts src/cron/scheduler.test.ts src/cron/runner.test.ts
/bin/bash: bun: command not found
exit code: 127
```

No test body started. This is `BLOCKED_ENVIRONMENT`, not a candidate failure. No suites were repeated through another runtime.

## Gate result

```text
PIN_IDENTITY = VERIFIED
REQUIRED_SOURCE_TEST_RUNTIME = BUN_1.3.14
AVAILABLE_SOURCE_TEST_RUNTIME = NODE_24.19.0; BUN_ABSENT
FOCUSED_CRON_TESTS = BLOCKED_ENVIRONMENT_BEFORE_START
ATENTO_HOST_RUNTIME_PROVIDER_SEAM = NOT_PRESENT_IN_AUDITED_ATENTO_STATE
NEW_CANDIDATE_ELIMINATION = NONE
END_TO_END_QUALIFICATION = NOT_ESTABLISHED
```

The repository is Letta Code, a CLI that connects to Letta agents; the inspected Atento records still say there is no product host/provider gateway adapter for the frozen cohort. A source test or overlay fixture would not demonstrate the requested Atento-owned scheduled-task recovery. Historical overlay evidence is at another SHA and remains non-transferable.

## Smallest falsifiable next test

Prerequisites:

1. An executable Atento host/runtime adapter for this exact pin, without building a production integration solely to unlock the evaluation.
2. Bun 1.3.14 plus dependencies from the frozen lockfile, for focused upstream source tests.
3. A synthetic Letta test backend or inert seam that creates no provider call, plus observable task claim, terminal acknowledgement, and delivery IDs.

Then run one disposable probe only: create one inert due NAIA task with a synthetic identity; persist it; terminate the host after claim but before terminal acknowledgement; restart; allow exactly one retry; assert the owner remains NAIA and exactly one terminal delivery is recorded. Do not run parallel jobs. Reuse the upstream tests already cited in the common-cohort record and do not repeat NanoClaw, Memoh, the 7/7 assertions, or the approved SSE replay.

## Disposition

`LETTA_CODE_CURRENT_PIN = UNRESOLVED / BLOCKED_ENVIRONMENT`. Missing runtime evidence is not a failure and does not technically eliminate Letta Code. Keep the scheduled-task recovery gate blocked until an executable adapter exists.

This record is on `codex/disposable-nanoclaw-mobile-replay-20261001` only. PR #58 remains unchanged.
