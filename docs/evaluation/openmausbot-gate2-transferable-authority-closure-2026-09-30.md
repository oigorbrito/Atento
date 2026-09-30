# OpenMausBot Gate-2 transferable authority closure — 2026-09-30

Candidate: `milind-soni/OpenMausBot@6005b1bf5883a7ffa639c07e729321f89b9532e1`

## Exact-pin execution

Exact-pin CI is fully green across Linux, macOS, Windows, Android, iOS, packaged server, control-plane, behavior evals and vitest shards.

Run-backed Gate-2 evidence includes:

```text
server/request-auth.test.ts = 46 PASS
server/permission-proxy.test.ts = 11 PASS
electron/cua-windows-isolation.test.mjs = 8 PASS
server/approval-mode.test.ts = 22 PASS
server/peer-approval.test.ts = 18 PASS
server/peer-approval.e2e.test.ts = PASS
server/routine-delegation.e2e.test.ts = 8 PASS
server/routine-cron.e2e.test.ts = PASS
server/routine-continuity.e2e.test.ts = PASS
behavior evals = 66 PASS
control-plane tests = 42 PASS
```

Vitest shards execute the same 200-file suite across multiple operating systems, with platform-specific skips but no failures.

## Transferable clauses

```text
REQUEST_AUTHORITY = PASS_UPSTREAM_EXACT_PIN
PERMISSION_PROXY = PASS_UPSTREAM_EXACT_PIN
WINDOWS_CUA_ISOLATION = PASS_UPSTREAM_EXACT_PIN
APPROVAL_MODE = PASS_UPSTREAM_EXACT_PIN
PEER_APPROVAL_ALLOW/DENY = PASS_UPSTREAM_EXACT_PIN
PEER_APPROVAL_DURABILITY = PASS_UPSTREAM_EXACT_PIN
ROUTINE_DELEGATION_DENIAL/CANCELLATION = PASS_UPSTREAM_EXACT_PIN
CRON_CONFIRMATION_PATH = PASS_UPSTREAM_EXACT_PIN
ROUTINE_CONTINUITY = PASS_UPSTREAM_EXACT_PIN
```

## Remaining Atento-specific residual

The upstream evidence proves the mechanics but not the strict NAIA/Anna trust topology.

Residual:

```text
NAIA runtime/store/credentials = independent
Anna runtime/store/credentials = independent
same-owner cross-role access = denied
peer delegation across roles = broker-only
background/routine authority <= interactive role authority
provider/session auth cannot silently bridge role boundary
```

## Disposition

```text
OPENMAUSBOT_EXACT_PIN_CI = PASS
OPENMAUSBOT_GATE2_TRANSFER = PASS_WITH_SCOPE
OPENMAUSBOT_ATENTO_RESIDUAL = TWO_ROLE_COMPOSITION
OPENMAUSBOT_FRONTIER_ELIGIBLE = YES
CURRENT_PIN_QUALIFIED = NO
```
