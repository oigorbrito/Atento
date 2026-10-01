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
