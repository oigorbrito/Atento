# OpenGrokBot Gate-2 CI attribution — 2026-09-30

Candidate: `wolfqing/OpenGrokBot@43ba51fc0487b7adbb23861a1062a113390833d9`

Exact-pin CI is red because one gateway batching/concurrency test fails:

```text
test/server-v021.test.ts
one turn at a time per bot
message batching expectation mismatch
```

Observed suite totals:

```text
gateway tests = 319 passed / 1 failed
test files = 32 passed / 1 failed
bot computer image = SUCCESS
```

Gate-2-relevant tests in the same exact-pin run pass, including:

- approval from inside a routine;
- pending approval counts per conversation;
- approval endpoint tests;
- memory tests.

Therefore:

```text
CI_FAILURE_CAUSE = TURN_BATCHING/CONCURRENCY
AUTHORITY_TESTS_IN_RUN = PASS_WITH_SCOPE
CI_RED != AUTHORITY_FAIL
```

The candidate still does not enter the transferable-evidence frontier because the known browser consequence gap remains open: a signed-in browser can execute outward effects without a mandatory technical hold gate.

```text
OUTWARD_BROWSER_EFFECT_GATE = NOT_TECHNICALLY_MANDATORY
ROUTINE_HOLD_MECHANISM = EXECUTED
APPROVAL_ENDPOINT = EXECUTED
UNIVERSAL_BROWSER_EFFECT_AUTHORITY = OPEN

OPENGROKBOT_FRONTIER_ELIGIBLE = NO_AT_CURRENT_PIN
OPENGROKBOT_ELIMINATED = NO
```

The next useful proof remains the localized `execToolCall` effect-policy hardening defined in the existing preflight.
