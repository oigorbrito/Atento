# Disposable NanoClaw mobile replay probe — result

Date: 2026-10-01

## Scope

A one-scenario feasibility probe was added only on:

`codex/disposable-nanoclaw-mobile-replay-20261001`

Base: Atento PR #58 head `e948f344b91e20e655399b11300c439228d144ec`.

The workflow checked out and verified the exact NanoClaw pin:

`nanocoai/nanoclaw@4c1eabd3ddd74cc3d71b1871da857391a9411c8d`

It injected one test into that checkout and exercised NanoClaw's real `registerWebhookHandler` HTTP server with a disposable adapter fixture and SQLite outbox.

## Test

One role-scoped replay case now covers an abrupt worker crash. No prior candidate suite or 7/7 Atento assertions are rerun.

One role-scoped SSE replay case:

1. Seed one reply for each NAIA, Anna, and Apollo fixture in a temporary SQLite outbox.
2. Read each role's first event with a synthetic bearer token.
3. Add one subsequent reply per role.
4. Terminate the directly spawned Node worker with `SIGKILL` (no shutdown handler or SQLite close); poll for the fixed port to become bindable, with a 5-second limit, then restart over the same SQLite file.
5. Reconnect with each role's prior `Last-Event-ID`.
6. Assert that each role receives only its own next event and that an unknown token receives HTTP 401.

## Result

Previous graceful-restart baseline (separate evidence):

- GitHub Actions run `36934662391`, commit `b05f450c2d45f9265acd12c3a9967f39b9a0862a`
- exact candidate-pin check: PASS
- dependency install and SQLite native build: PASS
- replay probe: 1 test, 1 pass, 0 failures
- raw JUnit artifact: `disposable-nanoclaw-mobile-replay-36934662391`
- artifact SHA-256: `d7abfada63435d8f272ba4c7cd3b5d94b6a19dd9675ddfa3b6bdba809838fb26`

A second identical CI pass occurred at run `36934690875` after a workflow-trigger adjustment. It adds no new evidence. Two earlier runs failed because of escaping/framing defects in the new test fixture; the candidate-pin check passed in both. Those failures are classified as harness defects, not NanoClaw failures.

## Interpretation and limits

SIGKILL diagnostic and controlled rerun: run `36936155950` hit the default 5-second Vitest limit. Runs `36936315900` and `36936452447` reported `EADDRINUSE`; run `36936877058` did not observe the port becoming bindable within 5 seconds. Those runs used the `tsx` CLI and killed only its direct child, so they are retained as harness-diagnostic failures rather than candidate failures. The fixture was corrected to start the TypeScript worker in the directly signaled Node process (`node --import tsx`). On exact NanoClaw pin `4c1eabd3ddd74cc3d71b1871da857391a9411c8d`, run `36936998880` then passed 1/1 test (test duration 0.625 s): after `SIGKILL`, the fixed port became bindable within the 5-second bound; a new worker restarted against the same SQLite file; each role received only its next SSE event using its prior `Last-Event-ID`; unknown synthetic bearer token received HTTP 401. JUnit artifact `disposable-nanoclaw-mobile-replay-36936998880` has SHA-256 `8af735a73aa7d55e53ba9ee10e7cbd650b97ff41886fdb8298bf085593904bb3`. The exact port-release latency was not preserved as a separate metric. Classify abrupt same-port replay as `PASS_WITH_SCOPE` for this one crash/restart and synthetic fixture only. This does not prove production Atento authentication, provider custody, task retry/recovery, or complete three-role qualification.

```text
NANOCLAW_WEBHOOK_SERVER_SEAM = EXERCISED
SSE_LAST_EVENT_ID_REPLAY_AFTER_GRACEFUL_TEST_WORKER_RESTART = PASS_WITH_SCOPE
SSE_LAST_EVENT_ID_REPLAY_AFTER_SIGKILL_SAME_PORT_RESTART = PASS_WITH_SCOPE
SYNTHETIC_ROLE_SCOPED_OUTBOX = PASS_WITH_SCOPE
PRODUCTION_ATENTO_GATEWAY_OR_AUTH = NOT_TESTED
REAL_MODEL_OR_PROVIDER_CALL = NOT_TESTED
NANOCLAW_NATIVE_MOBILE_API = NOT_ESTABLISHED
SCHEDULED_TASK_RESTART_AND_RETRY = STILL_PENDING
FULL_ATENTO_THREE_ROLE_QUALIFICATION = NOT_PASSED
```

The worker, tokens, role map, and SQLite outbox are a disposable Atento-side feasibility fixture. The test proves that NanoClaw's existing raw webhook server can host this fixture's SSE replay route and that the fixture resumes role-filtered events after one abrupt worker-process exit and restart. It does not prove the production Atento identity provider, memory/credential/tool isolation, a real model/provider integration, or scheduled-task recovery.

No prior 7/7 NanoClaw assertions or upstream candidate suite was rerun. This branch is not merged and is not an implementation recommendation.

## Next residual — NAIA scheduled-task recovery

Existing exact-pin evidence was audited and reused; it was not rerun:

- NanoClaw `src/host-sweep.test.ts` tests orphan processing-claim cleanup after a killed container, rescheduling with backoff, and preserving retry state.
- NanoClaw `src/modules/scheduling/recurrence.test.ts` covers recurrence creation and script-failure backoff.
- NanoClaw `src/mailbox/sqlite/arm-next-task.test.ts` covers atomic next-occurrence creation and retry after an insertion failure.
- Atento `tools/system_chassis/nanoclaw.atento.test.ts` verifies role-scoped task creation/list/get and denies cross-group operations; those test tasks are intentionally scheduled in the future and do not fire.

The uncovered NAIA delta is one integrated **Atento host-process** restart after a due task is claimed but before its terminal acknowledgment, followed by one retry. The current Atento worktree has no product host runtime/provider gateway adapter to execute this path, as recorded by the PR #58 runtime-seam audit. Therefore:

```text
UPSTREAM_TASK_COMPONENT_EVIDENCE = REUSED
ATENTO_ROLE_SCOPED_TASK_API = PASS_WITH_SCOPE (EXISTING 7/7 PROBE)
NAIA_HOST_PROCESS_TASK_RETRY_AFTER_RESTART = BLOCKED_ADAPTER
NEW_TASK_RETRY_TEST = NOT_RUN
```

The smallest next executable probe, once that adapter exists, is one inert NAIA task with synthetic identity and no provider call: persist the due task, terminate the host after claim/before acknowledgment, restart the same runtime, allow one retry, and assert that the task remains NAIA-owned, no Anna/Apollo state or authority is reachable, and the task produces no duplicate terminal delivery after completion. This probe should reuse the upstream recovery checks above rather than copy their internals or rerun their suite.


## Follow-up recheck — NAIA task retry after host restart — 2026-10-01

### Recheck result

PR #58 remains open and in draft at head `e948f344b91e20e655399b11300c439228d144ec`. Its current description and the runtime-seam audit still identify no Atento product host runtime or production gateway/provider adapter. The current disposable-branch record also has no intervening implementation of that seam. NanoClaw's raw webhook server and channel adapter are not the Atento host task runtime; the SSE replay probe does not execute scheduled work.

```text
ATENTO_PRODUCT_HOST_RUNTIME = ABSENT
PRODUCTION_GATEWAY_PROVIDER_ADAPTER = ABSENT
NAIA_HOST_PROCESS_TASK_RETRY_AFTER_RESTART = BLOCKED_ADAPTER
NEW_TASK_RETRY_PROBE = NOT_RUN
PR_58_MODIFIED = NO
```

This is an Atento integration blocker, not a NanoClaw failure. The approved SSE replay remains `PASS_WITH_SCOPE`; it is not evidence for scheduled-task retry.

### Preconditions before one probe

Do not implement a product integration solely to unblock this test. Reopen this gate only when the real Atento host runtime seam exists and can be launched in test mode. The seam must:

- accept a persisted due task through the actual Atento-to-NanoClaw scheduling/dispatch path;
- bind the task to a server-side synthetic NAIA identity and NAIA-owned state, without trusting a client-supplied role;
- expose the host process lifecycle and a deterministic point after task claim but before terminal acknowledgment;
- persist claim/retry/terminal-delivery state across a host restart and expose enough evidence to count terminal deliveries;
- run without a provider call, external side effect, production credential, or parallel task.

The exact-pinned NanoClaw component tests already listed above remain reused evidence. Do not rerun them, the prior Atento 7/7 assertions, the benchmark, or the approved SSE replay.

### Smallest falsifiable probe once prerequisites exist

Run exactly one disposable NAIA task with an inert effect and synthetic identity:

1. Persist one due task through the real host adapter and verify its owner is NAIA before dispatch.
2. Let the host claim it, then terminate the host process before terminal acknowledgment.
3. Restart the same host runtime against the same durable task state and permit exactly one retry.
4. Observe the terminal record and delivery count; verify the task remains NAIA-owned throughout, reaches one terminal outcome, and produces no duplicate terminal delivery.

No Anna or Apollo task is added. The probe must not call a provider or produce an external effect.

### Acceptance and result classification

Accept this probe only if the recorded raw trace proves the same task ID and NAIA owner before claim, after restart, and at terminal completion; the host actually restarted; one retry occurred; and terminal delivery count is exactly one. Missing any of these observations is INVALID/INCONCLUSIVE, not PASS.

Classify a wrong owner, cross-role access, lost task, or duplicate terminal delivery under an otherwise valid harness as a behavior failure of the exercised integration path. Classify failure to start/kill/restart at the declared lifecycle seam, absent event instrumentation, or a broken fixture as HARNESS/INFRA INVALID; do not attribute it to NanoClaw. Any PASS is scoped to this single synthetic task and does not qualify production, provider custody, or the three-agent topology.

Until the prerequisites exist, retain `NAIA_HOST_PROCESS_TASK_RETRY_AFTER_RESTART = BLOCKED_ADAPTER` and do not run a substitute fixture test.


## Disposable task-restart seam spike — 2026-10-01

The user requested a spike. Added a separate one-case workflow and test on this disposable branch only:

- `tools/system_chassis/nanoclaw-task-restart-spike.atento.test.ts`
- `tools/system_chassis/nanoclaw-task-restart-spike-worker.ts`
- `.github/workflows/nanoclaw-task-restart-spike.yml`

The spike checks out the same exact NanoClaw pin, creates one due task in a disposable NAIA-named SQLite mailbox, starts a fixture worker, records a processing claim, SIGKILLs that worker before terminal acknowledgment, and restarts a fresh worker on the same mailbox files. The restarted worker calls NanoClaw's exported `_resetStuckProcessingRowsForTesting` helper, waits for its single scheduled backoff retry, applies a synthetic terminal acknowledgment, and records one inert terminal-ledger row. The test is serial and has no provider/channel call, real identity, external effect, Anna/Apollo task, benchmark, or repeated prior suite.

### Scope boundary

This is a **component seam spike**, not the previously blocked Atento host-runtime probe. It does not launch NanoClaw's production `main()`/host sweep, use the actual Atento scheduler/provider adapter, or test real role authorization. NAIA ownership is a synthetic fixture value stored beside the mailbox. The terminal ledger is also fixture code, so its one row does not prove production duplicate suppression. A passing result can only show that the pinned recovery helper can reschedule a persisted orphan claim across a fixture worker-process restart; it cannot change `NAIA_HOST_PROCESS_TASK_RETRY_AFTER_RESTART = BLOCKED_ADAPTER` or qualify NanoClaw.

The original product-level acceptance probe remains unchanged: it requires the actual Atento adapter, one real host-process lifecycle boundary, a real NAIA-bound scheduled task, one post-restart retry, and authoritative terminal-delivery counting.

### Execution state at commit preparation

```text
SPIKE_IMPLEMENTATION = ADDED_ON_DISPOSABLE_BRANCH
EXACT_NANOCLAW_PIN = 4c1eabd3ddd74cc3d71b1871da857391a9411c8d
SPIKE_CASES = 1
PROVIDER_OR_EXTERNAL_EFFECT = NONE
UPSTREAM_TESTS_RERUN = NO
PR_58_MODIFIED = NO
PRODUCT_HOST_ADAPTER = ABSENT
PRODUCT_GATE = BLOCKED_ADAPTER
HOSTED_SPIKE_RUN = NOT_YET_VERIFIED
```

If the disposable workflow run cannot be read from the connected GitHub interface, preserve that as an observability limitation; do not infer PASS from a commit or workflow dispatch.


The workflow trigger was narrowed to `workflow_dispatch` plus the one-shot sentinel path `tools/system_chassis/run-nanoclaw-task-restart-spike.once`; the sentinel has not been created. The connected GitHub interface available in this session can write branch files and inspect PR-triggered runs, but exposes neither workflow dispatch nor a list of push-triggered runs. The private Actions page is not readable in the current browser session. Therefore no hosted result is claimed, and no further trigger was sent. The spike is implemented but execution remains unverified.


## Follow-up observability check — 2026-10-01 20:11 America/Sao_Paulo

Read-only commit-status checks returned empty status contexts for the workflow-creation and spike commits `e151a3829fd28801c83fb39e0d5bf65856e29ecc`, `4aeba03cc1ef9bb63ed40e1f5d2d64711dbe495f`, `063cd55efa5924b1b42d66cc02e9f092cfa19c5c`, and current record commit `e3689ee24dc5fc9acb1afad447d684ce2995e0f5`. The only available workflow-run lookup is explicitly limited to pull-request-triggered runs and returned no runs for the workflow commit; this does not enumerate push-triggered runs. Empty commit statuses therefore do **not** establish that Actions did not run or that the test failed to start.

No run ID, job summary, JUnit artifact, or raw execution log is available through the connected GitHub interface. No manual dispatch or sentinel push was performed. Keep `HOSTED_SPIKE_RUN = NOT_VERIFIED`; do not infer a test result.


## One-shot trigger attempt — 2026-10-01 20:14 America/Sao_Paulo

Created the configured sentinel exactly once at commit `ddd45ed4a37a92522a8772a17ef25eb2a141bb1c`. Read-only status checks at approximately 12 seconds and 37 seconds after the commit both returned `statuses = []`. The workflow-run lookup also returned an empty collection, but that endpoint is limited to pull-request-triggered runs and cannot confirm this push-triggered attempt.

```text
SENTINEL_CREATED_ONCE = YES
SENTINEL_COMMIT = ddd45ed4a37a92522a8772a17ef25eb2a141bb1c
COMBINED_COMMIT_STATUSES = EMPTY_AT_12S_AND_37S
PUSH_WORKFLOW_RUN_LISTING = UNAVAILABLE
RUN_ID / JOB_LOG / JUNIT_ARTIFACT = NOT_OBTAINED
HOSTED_SPIKE_RESULT = NOT_VERIFIED
ADDITIONAL_TRIGGER = NOT_SENT
```

This retry proves only that the sentinel commit exists. It does not establish that GitHub Actions accepted, started, or completed the workflow. Keep the spike result unclassified until a run ID and raw JUnit evidence are obtained.
