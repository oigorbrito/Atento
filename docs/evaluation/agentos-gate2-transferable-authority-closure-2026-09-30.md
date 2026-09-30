# AgentOS Gate-2 transferable authority closure — 2026-09-30

## Candidate

`use-agent-os/agent-os@226c906291fc68f3c4517623446bdaec1b48a82d`

## Exact-pin hosted execution

Direct Actions lookup establishes exact-pin execution that the earlier transfer audit did not observe:

```text
CI run 36590011922 = SUCCESS
Web UI Browser Smoke = SUCCESS
frontend = SUCCESS
Windows Release Assets = SUCCESS
Desktop Release Assets = SUCCESS
```

The CI matrix completed on both Linux and Windows.

Observed backend test results:

```text
Linux:   16774 passed, 50 skipped
Windows: 16701 passed, 123 skipped
```

The exact-pin frontend suite also completed:

```text
109 files passed
2382 tests passed
```

## Gate-2 authority clauses transferred from executed tests

### Interactive authority / approval

`tests/test_tools/test_shell_approval_policy.py` is part of the exact successful suite.

The executed test source establishes, among other things:

- sandbox-off forces an approval prompt even when global auto-approve is configured;
- cached approval intent from another session does not skip the prompt;
- sensitive shell targets are detected;
- explicit elevated bypass remains a deliberate override rather than an accidental path.

Therefore:

```text
SESSION_SCOPED_APPROVAL_REUSE = PASS_UPSTREAM_EXACT_PIN
SENSITIVE_SHELL_APPROVAL_PATH = PASS_UPSTREAM_EXACT_PIN
CROSS_SESSION_CACHED_APPROVAL = DENIED_IN_TESTED_PATH
```

A hardened NAIA profile must still disable bypass/elevated convenience defaults.

### Background authority

The exact suite includes:

- `tests/test_scheduler/test_cron_default_elevation.py`
- `tests/test_scheduler/test_cron_elevation.py`
- `tests/test_scheduler/test_cron_tool_profile.py`

Executed tests prove:

- `cron_default_mode = off` leaves agent-run cron unelevated;
- interactive elevation does not leak into cron when cron default is off;
- explicit per-job `elevated: off` survives persistence;
- non-agent cron job types reject elevation;
- invalid cron tool profiles are rejected at the write boundary;
- known restricted profiles are persisted canonically.

Therefore the unsafe shipped cron default is configurable away without replacing the scheduler.

```text
HARDENED_CRON_UNELEVATED_MODE = PASS_UPSTREAM_EXACT_PIN
INTERACTIVE_ELEVATION_LEAK_TO_CRON = NO_IN_TESTED_OFF_PROFILE
INVALID_CRON_PROFILE = DENIED_AT_WRITE_BOUNDARY
SCHEDULER_REWRITE_REQUIRED = NO
```

### Sensitive-path / credential-file boundary

The exact suite includes sensitive-path tests that cover host credential material on Linux and Windows, including:

- GitHub CLI;
- cloud credentials;
- Docker registry credentials;
- shell free-form text scanning;
- workspace traversal;
- Windows AppData credential locations.

This is a filesystem/shell protection clause, not a complete per-role credential-vault proof.

```text
HOST_CREDENTIAL_PATH_GUARDS = PASS_UPSTREAM_EXACT_PIN_WITH_SCOPE
```

### Browser policy

The exact CI includes browser policy tests and the exact pin also has a successful Web UI Browser Smoke workflow.

However AgentOS explicitly places Chromium outside the ordinary process sandbox and relies on a distinct browser policy layer.

Therefore:

```text
BROWSER_POLICY_TEST_SURFACE = EXECUTED
BROWSER_PROCESS_SANDBOX_PARITY = NOT_APPLICABLE
BROWSER_AUTHORITY = SEPARATE_POLICY_DOMAIN
```

This remains a composition concern if browser actions are included in the NAIA Gate-2 target profile.

## Remaining Atento-specific residual

The current upstream evidence does not prove the strict NAIA/Anna role boundary.

The defensible target composition is:

```text
NAIA AgentOS runtime / state / credentials / channels
              |
        explicit Atento broker
              |
Anna independent AgentOS runtime / state / credentials / channels
```

The hardened profile must additionally freeze:

```text
permissions.default_mode != bypass
permissions.cron_default_mode = off
browser policy = explicit restricted profile
```

Residual negative assertions:

```text
CROSS_MEMORY_READ = DENIED
CROSS_CREDENTIAL_USE = DENIED
CROSS_TOOL_OR_CHANNEL_USE = DENIED
SILENT_AGENT_INVOCATION = DENIED
BACKGROUND_AUTHORITY <= INTERACTIVE_AUTHORITY
BROWSER_EFFECT_AUTHORITY <= FROZEN_ROLE_POLICY
EXPLICIT_BROKER_HANDOFF = ONLY_ALLOWED_CROSS_ROLE_PATH
```

## Gate-2 disposition

```text
AGENTOS_EXACT_PIN_CI = PASS
AGENTOS_LINUX_TESTS = 16774_PASS
AGENTOS_WINDOWS_TESTS = 16701_PASS

INTERACTIVE_AUTHORITY_TRANSFER = PASS_WITH_SCOPE
HARDENED_CRON_AUTHORITY_TRANSFER = PASS_WITH_SCOPE
SENSITIVE_PATH_GUARDS_TRANSFER = PASS_WITH_SCOPE
BROWSER_POLICY_SURFACE = EXECUTED_BUT_SEPARATE_DOMAIN

ATENTO_TWO_ROLE_COMPOSITION = NOT_RUN
AGENTOS_GATE2 = COMPOSITION_PLUS_BROWSER_POLICY_RESIDUAL
AGENTOS_CURRENT_PIN_QUALIFIED = NO
```

No broad AgentOS suite should be rerun locally. Only the Atento-specific two-role hardened composition remains decision-relevant.
