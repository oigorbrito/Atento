# Rome Gate-2 transferable authority closure — 2026-09-30

## Candidate

`rome-os/rome@ef523c4659149e2711744deb04ec42c3be339907`

## Exact-pin hosted execution

Direct Actions lookup establishes exact-pin execution:

```text
CI run 36610578591 = SUCCESS
E2E Testing by Midscene = SUCCESS
Release = SUCCESS
```

CI jobs all completed successfully, including:

- unit-tests-web
- unit-tests-core
- unit-tests-rest
- integration-tests
- e2e-tests
- db-schema

The integration job executed `pnpm test:integration` and finished with:

```text
31 passed / 3 skipped
```

## Gate-2 clauses transferred from executed tests

The exact integration suite includes `src/actions/engine.integration.test.ts`, and the logs show the complete approval replay path:

```text
record
-> approval exception
-> journal persisted
-> replay
-> previously pending action executes
-> completion
```

It also executes strict-mode divergence handling for replay.

Therefore:

```text
DURABLE_ACTION_APPROVAL_STATE_MACHINE = PASS_UPSTREAM_EXACT_PIN
PENDING_ACTION_REPLAY = PASS_UPSTREAM_EXACT_PIN
APPROVED_PAYLOAD_REPLAY_BINDING = PASS_UPSTREAM_EXACT_PIN_WITH_SCOPE
STRICT_REPLAY_DIVERGENCE = PASS_UPSTREAM_EXACT_PIN
```

Combined with exact-pin approval API tests already inventoried in the transfer audit, Rome has strong reusable approval evidence.

## Remaining Atento-specific residual

The upstream run does not prove that every consequential action in the selected NAIA configuration carries `requiresApproval`, nor that provider-native execution cannot bypass Rome-owned policy.

The hardened Atento topology remains:

```text
NAIA Rome profile/process
       |
 explicit Atento broker
       |
Anna separate Rome profile/process
```

Residual:

```text
AUTO_APPROVE_SKILLS = false
AUTO_APPROVE_TOOLS = false
AUTO_APPROVE_WORKFLOWS = false

ALL_CONSEQUENTIAL_NAIA_ACTIONS = approval-aware
PROVIDER_NATIVE_BYPASS = denied/not reachable
CROSS_PROFILE_MEMORY = denied
CROSS_PROFILE_AUTH = denied
CROSS_PROFILE_TOOL/CHANNEL = denied
SILENT_CROSS_ROLE_INVOCATION = denied
BROKER = only cross-role path
```

## Gate-2 disposition

```text
ROME_EXACT_PIN_CI = PASS
ROME_DURABLE_APPROVAL_TRANSFER = PASS_WITH_SCOPE
ROME_PROFILE_ISOLATION = STRONG_SOURCE_CONTRACT
ROME_ATENTO_RESIDUAL = TWO_PROFILE_COMPOSITION + ACTION_COMPLETENESS + PROVIDER_BYPASS

ROME_CURRENT_PIN_QUALIFIED = NO
```

No broad Rome suite should be rerun locally.
