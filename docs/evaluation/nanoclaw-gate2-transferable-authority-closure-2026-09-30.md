# NanoClaw Gate-2 transferable authority closure — 2026-09-30

Candidate: `nanocoai/nanoclaw@4c1eabd3ddd74cc3d71b1871da857391a9411c8d`

## Exact-pin execution

Exact-pin CI is green.

Observed primary test jobs:

```text
Vitest files = 266 PASS / 1 skipped
Vitest tests = 3033 PASS / 1 skipped
secondary suite = 516 tests across 58 files, 3 skipped
Iron-front = SUCCESS
CI gate = SUCCESS
```

Run-backed Gate-2 tests include:

```text
gateway-approval-coordinator.test.ts = 46 PASS
permissions/channel-approval.test.ts = 18 PASS
permissions/permissions.test.ts = 15 PASS
permissions/sender-approval.test.ts = 6 PASS
permissions/sender-decline-notify.test.ts = 7 PASS
permissions/channel-card-interceptor.test.ts = 5 PASS
approvals/restart-honesty.test.ts = 8 PASS
approvals/approval-resolved.test.ts = 3 PASS
mount-security/index.test.ts = 5 PASS
container-restart.test.ts = 9 PASS
cli/resources/tasks.test.ts = 31 PASS
mailbox/sqlite/tasks.test.ts = 13 PASS
```

The container-runner suite also executes delivery deduplication, task wake semantics, provider isolation, timeout child termination and fail-closed memory-hook behavior.

## Transferable clauses

```text
GATEWAY_APPROVAL_AUTHORITY = PASS_UPSTREAM_EXACT_PIN
CHANNEL/SENDER_PERMISSION = PASS_UPSTREAM_EXACT_PIN
APPROVAL_RESTART_HONESTY = PASS_UPSTREAM_EXACT_PIN
MOUNT_SECURITY = PASS_UPSTREAM_EXACT_PIN
CONTAINER_RESTART_CONTRACT = PASS_UPSTREAM_EXACT_PIN
TASK_PERSISTENCE/WAKE_SURFACE = PASS_UPSTREAM_EXACT_PIN
PROVIDER_CONTINUATION_ISOLATION = PASS_UPSTREAM_EXACT_PIN_WITH_SCOPE
```

## Remaining Atento-specific residual

NanoClaw's actual authority is shaped by installed skills/gateway recipes. Therefore Atento must freeze the recipe as part of the candidate.

Residual:

```text
NAIA recipe = frozen least-privilege capability set
Anna recipe/runtime = independent
gateway approval ownership = role-specific
credential/mount grants = separate
cross-role channel wiring = denied
explicit broker = only cross-role path
background/task effects <= hardened interactive authority
```

## Disposition

```text
NANOCLAW_EXACT_PIN_CI = PASS
NANOCLAW_GATE2_TRANSFER = PASS_WITH_SCOPE
NANOCLAW_ATENTO_RESIDUAL = FROZEN_RECIPE + TWO_ROLE_COMPOSITION
NANOCLAW_FRONTIER_ELIGIBLE = YES
CURRENT_PIN_QUALIFIED = NO
```
