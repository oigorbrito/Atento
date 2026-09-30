# Letta Code Gate-2 transferable authority closure — 2026-09-30

## Candidate

`letta-ai/letta-code@21daa38a8cdd74f2d03b634c8312253080bacfc1`

## Exact-pin hosted execution

Direct Actions lookup establishes exact-pin CI success across:

- lint/typecheck;
- update-chain smoke;
- local and hosted headless runs;
- Windows/Linux/macOS packaging;
- API and unit shards;
- Ollama/local-provider smoke.

A representative exact-pin unit shard recorded:

```text
running all 914 tests outside a pull request
shard result = 2193 tests across 217 files
```

The same executed shard includes permission and authority tests under:

- `src/permissions/format-denial.test.ts`
- `src/permissions/shell-command-normalization.test.ts`
- `src/permissions/permissions-checker.test.ts`
- `src/permissions/read-only-shell-security.test.ts`
- `src/permissions/permissions-mode.test.ts`

and integration hook tests directly show:

- pre-tool hooks can block execution;
- permission-request hooks can auto-allow or auto-deny;
- permission request context includes type, scope and `agent_id`;
- failed activation does not publish capabilities.

The exact repository also carries direct tests for:

- cross-agent permission guards;
- headless approval recovery;
- cron;
- memory confinement;
- sandbox transfer;
- workspace sandbox;
- recovery ownership.

## Gate-2 clauses transferable from executed evidence

```text
TECHNICAL_PERMISSION_DENIAL = EXECUTED
PRE_TOOL_BLOCKING_HOOK = EXECUTED
PERMISSION_REQUEST_AGENT_CONTEXT = EXECUTED
FAILED_ACTIVATION_CAPABILITY_PUBLISH = DENIED
HEADLESS/AUTHORITY_TEST_SURFACE = EXACT_PIN_CI_BACKED
```

The upstream default remains `unrestricted`; executed permission machinery does not convert that default into a hardened profile.

## Remaining Atento-specific residual

```text
permission mode = strict / explicit hardened rules
LETTA_FS_SANDBOX = enabled where the role requires shell
no shared-memory attachment across NAIA/Anna
no cross-agent search/conversation route across NAIA/Anna
prefer separate runtime/storage authority if any shared discovery seam remains
background/headless authority <= interactive hardened role authority
explicit broker = only cross-role path
```

## Gate-2 disposition

```text
LETTA_EXACT_PIN_CI = PASS
LETTA_PERMISSION_ENGINE_EXECUTED = YES
LETTA_HEADLESS/AUTHORITY_SURFACE_EXECUTED = YES
LETTA_ATENTO_RESIDUAL = HARDENED_PERMISSION_PROFILE + ROLE-SEPARATED_RUNTIME/MEMORY

LETTA_CURRENT_PIN_QUALIFIED = NO
```

No broad Letta Code suite should be rerun locally.
