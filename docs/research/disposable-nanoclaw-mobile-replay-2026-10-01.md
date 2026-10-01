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

The original graceful-restart case is being strengthened with one abrupt-crash condition; no prior candidate suite or 7/7 Atento assertions are rerun. The hosted result for this revision is pending.

One role-scoped SSE replay case:

1. Seed one reply for each NAIA, Anna, and Apollo fixture in a temporary SQLite outbox.
2. Read each role's first event with a synthetic bearer token.
3. Add one subsequent reply per role.
4. Terminate the worker with `SIGKILL` (no shutdown handler or SQLite close), then start a new process over the same SQLite file.
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

The SIGKILL revision is not yet verified until its GitHub Actions run completes. The previous graceful restart PASS does not transfer to this stronger condition.

```text
NANOCLAW_WEBHOOK_SERVER_SEAM = EXERCISED
SSE_LAST_EVENT_ID_REPLAY_AFTER_TEST_WORKER_RESTART = PASS_WITH_SCOPE
SYNTHETIC_ROLE_SCOPED_OUTBOX = PASS_WITH_SCOPE
PRODUCTION_ATENTO_GATEWAY_OR_AUTH = NOT_TESTED
REAL_MODEL_OR_PROVIDER_CALL = NOT_TESTED
NANOCLAW_NATIVE_MOBILE_API = NOT_ESTABLISHED
SCHEDULED_TASK_RESTART_AND_RETRY = STILL_PENDING
FULL_ATENTO_THREE_ROLE_QUALIFICATION = NOT_PASSED
```

The worker, tokens, role map, and SQLite outbox are a disposable Atento-side feasibility fixture. The test proves that NanoClaw's existing raw webhook server can host this fixture's SSE replay route and that the fixture resumes role-filtered events after a process restart. It does not prove the production Atento identity provider, memory/credential/tool isolation, a real model/provider integration, or scheduled-task recovery.

No prior 7/7 NanoClaw assertions or upstream candidate suite was rerun. This branch is not merged and is not an implementation recommendation.
