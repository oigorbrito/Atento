# Gobii Gate-2 CI attribution — 2026-09-30

Candidate: `gobii-ai/gobii-platform@c9929bf8ea59b4695b99dcab59aa6c97a09c5bdb`

## Exact-pin CI shape

The exact-pin CI is globally red, but most jobs succeed.

Observed:

```text
Complexity Guardrails = SUCCESS
Tag Guard = SUCCESS
Timeline PostgreSQL Integration = SUCCESS
Sandbox Server Tests = SUCCESS
Frontend Tests = SUCCESS
Publish Static Assets = SUCCESS

tests shards 01,02,03,05,06,07,09,10 = SUCCESS
tests shard 04 = FAILURE
tests shard 08 = FAILURE
Combined Test Results = SUCCESS
```

## Failure attribution

Two concrete failures were located.

### Shard 08

`tests.unit.test_console_email_oauth.NativeAgentEmailIntegrationTests.test_migration_reverse_removes_only_accountless_oauth_sessions`

fails because the expected migration module is missing:

```text
ModuleNotFoundError:
api.migrations.0460_native_email_integrations
```

This is a migration/test-version consistency failure.

### Shard 04

`tests.unit.test_smtp_transport.TestSmtpTransport.test_send_keeps_bcc_out_of_visible_headers`

fails because the Bcc header is still visible in the constructed message:

```text
expected Bcc header = absent
observed Bcc header = audit@example.com
```

This is a real email-privacy/output-contract regression at the frozen pin.

## Gate-2 interpretation

Neither failure proves that Gobii's secure credential delegation, peer-handoff ownership, or role-grant architecture requires a structural rewrite.

However the Bcc regression is security/privacy relevant enough that the exact pin should not be admitted to the transferable-evidence frontier merely because many other shards pass.

```text
GLOBAL_CI = RED
MIGRATION_TEST_CONSISTENCY = FAIL
SMTP_BCC_PRIVACY_CONTRACT = FAIL

CROSS_CUTTING_STRUCTURAL_REWRITE = NOT_ESTABLISHED
GOBII_ELIMINATED = NO
GOBII_FRONTIER_ELIGIBLE = NO_AT_CURRENT_PIN
```

Existing source/eval contracts remain reusable, but the current pin needs a changed-pin or exact rerun showing the privacy regression resolved before frontier admission.
