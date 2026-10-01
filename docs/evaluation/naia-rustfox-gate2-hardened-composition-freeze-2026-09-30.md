# NAIA Gate-2 RustFox hardened composition freeze — 2026-09-30

## Purpose

Freeze the smallest RustFox composition that can test the remaining Atento authority/isolation delta without rerunning exact-pin upstream suites.

This record does **not** qualify, shortlist, rank, promote or select RustFox.

Candidate:

`chinkan/RustFox@6e24388d36d1c6fac399039d8cab07cd9cb8264b`

Frozen profile:

`evals/config/naia_gate2_rustfox_v1.json`

## 1. Reused exact-pin evidence

Already established:

```text
MULTI_BOT_ALLOWLIST_ISOLATION = PASS_UPSTREAM_EXACT_PIN
BOT_CONVERSATION/MEMORY_ID_ISOLATION = PASS_UPSTREAM_EXACT_PIN_WITH_SCOPE
SUPERVISOR_HIGH_RISK_APPROVAL = PASS_UPSTREAM_EXACT_PIN
SUPERVISOR_RESTART_RESTORE = PASS_UPSTREAM_EXACT_PIN
HOME_SANDBOX_SECRET_EXCLUSION = PASS_UPSTREAM_EXACT_PIN
TELEGRAM_OFF_ALLOWLIST_REJECTION = PASS_UPSTREAM_EXACT_PIN
```

No broad RustFox suite should be rerun for Gate 2.

## 2. Unsafe default tightened

The exact pin confirms that Medium-risk supervisor tasks auto-execute by default.

The frozen profile sets both supported tightening controls:

```toml
[risk]
require_approval_for_medium = true
auto_execute_only_low = true
```

The duplicated intent is deliberate for qualification: Medium must not silently become auto-executable through either policy branch.

## 3. Frozen role topology

```text
NAIA:
  runtime = independent
  durable USER/memory = independent
  SecretStore grants = independent
  peer grants = broker-only

Anna:
  runtime = independent
  durable USER/memory = independent
  SecretStore grants = independent
  peer grants = broker-only

cross-role:
  shared memory = forbidden
  shared secret grants = forbidden
  native peer invocation = forbidden
  allowed crossing = explicit Atento handoff broker only
```

## 4. Universal effect owner requirement

The residual is not whether supervisor approval exists. It is whether **every consequential effect path** is governed by the hardened authority owner.

`UNIVERSAL-EFFECT-OWNER` must inventory the selected NAIA effect surface and prove:

```text
supervisor consequential path -> hardened approval owner
ordinary ToolRegistry consequential path -> same-or-narrower authority
scheduled consequential path -> same-or-narrower authority
peer/delegated consequential path -> same-or-narrower authority
```

A consequential ToolRegistry path that bypasses the supervisor/equivalent hardened owner fails this add-on even if supervisor tests are green.

## 5. Replay and recovery

Supervisor startup restore is reusable evidence. The frozen composition additionally requires:

```text
non-idempotent effect with uncertain prior outcome ->
  no blind automatic replay
  OR adapter-specific reconciliation before retry
```

This does not claim generic exactly-once external effects.

## 6. Replacement-cost classification

Current evidence supports:

```text
MEDIUM_RISK_HARDENING = CONFIGURATION_DELTA
ROLE_MEMORY/SECRET_SEPARATION = COMPOSITION
SUPERVISOR_AUTHORITY = STRONG_UPSTREAM_MECHANISM
UNIVERSAL_EFFECT_OWNER = UNPROVEN_RUNTIME_COMPOSITION
REQUIRED_CORE_PATCH = NOT_ESTABLISHED
REPAIR_CLASS = LOCALIZED_REPAIR_PENDING_EFFECT_INVENTORY
```

If ordinary ToolRegistry effects cannot be routed through the hardened owner without cross-cutting changes, the classification changes to structural and the current pin must stop as a complete base candidate.

## 7. Evidence identity

```text
composition_profile_hash =
3750bae1f639f39d2f687edf3bba4190d16e05fb9c428ef36aef78fa971d389e

policy_hash =
b3a0ba038e3e7a57ea060badad9d7deb3ab59b4f245cfc806643bf8a2730a2ad
```

These identify pre-execution state only.

## 8. Required execution

Execute only:

```text
ISO-1
ISO-2
ISO-3
ISO-4
ISO-5
ISO-6
UNIVERSAL-EFFECT-OWNER
```

Acceptance additionally requires:

```text
MEDIUM_CONSEQUENTIAL_AUTO_EXECUTION = DISABLED
BACKGROUND_AUTHORITY <= INTERACTIVE_AUTHORITY
AUTHORITY_CONTROL_FAILURE = FAIL_CLOSED
NATIVE_PEER_CROSS_ROLE = DENIED
BROKER = ONLY_CROSS_ROLE_PATH
```

## 9. Current disposition

```text
RUSTFOX_COMPOSITION = FROZEN_V1
RUSTFOX_STATIC_TOPOLOGY = READY_FOR_EXECUTION
RUSTFOX_UNIVERSAL_EFFECT_OWNER = NOT_RUN
RUSTFOX_COMMON_GATE2 = BLOCKED_ENVIRONMENT

RUSTFOX_CANDIDATE_FAIL = NOT_CLAIMED
RUSTFOX_GATE2_PASS = NOT_CLAIMED
CURRENT_PIN_QUALIFIED = 0
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```
