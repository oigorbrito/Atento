# RustFox Gate-2 transferable authority closure — 2026-09-30

## Candidate

`chinkan/RustFox@6e24388d36d1c6fac399039d8cab07cd9cb8264b`

## Exact-pin hosted execution

Direct Actions lookup establishes exact-pin CI success:

```text
Clippy = SUCCESS
Test = SUCCESS
Check = SUCCESS
Format = SUCCESS
Web portal = SUCCESS
Build = SUCCESS
```

The Test job executed the Rust suite and includes directly relevant authority/isolation cases.

Observed run-backed tests include:

- `sandbox_defaults_to_home_workspace_and_excludes_secrets`;
- multi-bot allowlist isolation;
- conversation bot-id isolation;
- memory bot-id isolation;
- peer-depth rejection;
- Telegram allowlist isolation across bots;
- off-allowlist message rejection without bot calls;
- High-risk supervisor task requires approval;
- supervisor restores paused tasks on startup;
- production default thresholds auto-execute Medium risk;
- task creation rollback when scheduler arm fails;
- secret claims and masked settings;
- task enable path verifies real scheduler arm.

## Gate-2 clauses transferable from executed evidence

```text
MULTI_BOT_ALLOWLIST_ISOLATION = PASS_UPSTREAM_EXACT_PIN
BOT_CONVERSATION/MEMORY_ID_ISOLATION = PASS_UPSTREAM_EXACT_PIN_WITH_SCOPE
SUPERVISOR_HIGH_RISK_APPROVAL = PASS_UPSTREAM_EXACT_PIN
SUPERVISOR_RESTART_RESTORE = PASS_UPSTREAM_EXACT_PIN
HOME_SANDBOX_SECRET_EXCLUSION = PASS_UPSTREAM_EXACT_PIN
TELEGRAM_OFF_ALLOWLIST_REJECTION = PASS_UPSTREAM_EXACT_PIN
```

The suite also confirms the unsafe default rather than hiding it:

```text
MEDIUM_RISK_DEFAULT = AUTO_EXECUTE
```

Therefore the remaining problem is not whether RustFox has authority machinery; it is whether all consequential paths can be routed through a hardened owner.

## Remaining Atento-specific residual

```text
all consequential effect classes = technical approval/allowlist owner
Medium-risk auto-execution tightened for consequential effects
ordinary ToolRegistry and supervisor policy reconciled
NAIA/Anna durable USER/memory separated
peer invocation restricted to explicit broker
SecretStore role grants separated
scheduled authority <= hardened interactive authority
non-idempotent automatic replay disabled/reconciled
```

## Gate-2 disposition

```text
RUSTFOX_EXACT_PIN_CI = PASS
RUSTFOX_MULTI_BOT_ISOLATION_TESTS = PASS_WITH_SCOPE
RUSTFOX_SUPERVISOR_AUTHORITY_TESTS = PASS
RUSTFOX_ATENTO_RESIDUAL = UNIVERSAL_EFFECT_OWNER + ROLE_MEMORY/CREDENTIAL_COMPOSITION

RUSTFOX_CURRENT_PIN_QUALIFIED = NO
```

No broad RustFox suite should be rerun locally.
