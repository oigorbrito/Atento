# QwenPaw Gate-2 transferable authority closure — 2026-09-30

Candidate: `agentscope-ai/QwenPaw@777441721aa72db8e380d90e4d0481b05cbfd4cc`

## Exact-pin hosted execution reconciliation

The exact pin has materially more executed evidence than the earlier audit observed.

Nightly exact-pin matrix:

```text
Unit py3.11 Windows = SUCCESS
Unit py3.11 Linux = SUCCESS
Unit py3.11 macOS = SUCCESS
Integrated py3.11 Linux/Windows/macOS = SUCCESS
Integrated py3.13 Linux = SUCCESS
Contract py3.11 Linux/Windows/macOS = SUCCESS
Contract py3.13 Linux = SUCCESS
Frontend = SUCCESS
Coverage = SUCCESS
Unit py3.13 Linux = FAILURE
```

The Python 3.13 unit failure is narrowly attributed to four PTY/terminal tests with `select()` file-descriptor-range/read-thread behavior:

```text
4 failed
17040 passed
24 skipped
```

This is not an authority-policy failure.

## Run-backed Gate-2 evidence

The successful exact-pin contract suite reports:

```text
412 passed / 1 skipped
```

and includes the security guardian contract surface.

The exact repository's executed matrix also contains:

- approval integration;
- cron integration/execution;
- sandbox module;
- security configuration/real security tests;
- unsandboxed gate tests;
- ACP permission tests;
- cron executor/manager tests;
- tool guard approval/engine tests;
- secret-store tests;
- sandbox implementations for Linux/Windows.

Observed contract tests include guardian unknown-tool/empty-param handling and memory-backend ownership/failure behavior.

## Transferable clauses

```text
SECURITY_GUARDIAN_CONTRACT = PASS_UPSTREAM_EXACT_PIN
CONTRACT_MATRIX_CROSS_PLATFORM = PASS_WITH_SCOPE
INTEGRATED_MATRIX_CROSS_PLATFORM = PASS_WITH_SCOPE
APPROVAL/CRON/SANDBOX_TEST_SURFACE = EXECUTED_AT_EXACT_PIN
PY3_13_TERMINAL_RUNTIME = FAIL_SPECIFIC
```

The known NAIA residual remains: sandbox-unavailable fallback and cron authority must be frozen so a missing confinement mechanism never broadens authority.

## Remaining Atento-specific residual

```text
sandbox unavailable => DENY / no unsandboxed fallback
cron/background authority <= interactive hardened authority
NAIA/Anna runtime/store/credentials = separated
cross-role channel/tool invocation = denied
broker = only cross-role path
target runtime excludes unresolved py3.13 PTY path unless repaired
```

## Disposition

```text
QWENPAW_GATE2_TRANSFER = PASS_WITH_SCOPE
QWENPAW_PY313_TERMINAL = FAIL_SPECIFIC
QWENPAW_FRONTIER_ELIGIBLE = YES_WITH_RUNTIME_SCOPE
CURRENT_PIN_QUALIFIED = NO
```

No broad QwenPaw rerun is justified for Gate 2.
