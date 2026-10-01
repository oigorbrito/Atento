# NAIA Gate-2 Octop hardened composition freeze — 2026-09-30

## Purpose

Freeze the smallest Octop composition that can test the remaining Atento authority/isolation delta without rerunning the exact-pin non-live suite.

This record does **not** qualify, shortlist, rank, promote or select Octop.

Candidate:

`TencentCloud/Octop@e473dd3c4a4741618ffde1a42a3492341a189e8e`

Frozen profile:

`evals/config/naia_gate2_octop_v1.json`

## 1. Reused exact-pin evidence

Already established:

```text
NON_LIVE_TEST_SUITE = 3951_PASS_17_SKIPPED
CROSS_USER_WORKSPACE_DENIAL = RUN_BACKED
SECURITY_DEFAULTS = RUN_BACKED
BRIDGE_PATH_POLICY = RUN_BACKED
MULTIPLATFORM_PACKAGE_SMOKE = PASS
CODEQL = PASS
```

No broad Octop suite should be rerun for Gate 2.

## 2. Default posture rejected

The exact pin proves these defaults:

```text
HITL = disabled
tool_guard = enabled
tool_guard.mode = warn
```

They do not match the hardened NAIA authority contract.

Freeze:

```text
hitl.enabled = true
tool_guard.enabled = true
tool_guard.mode = require_approval
```

The mode itself is not considered fail-closed proof. `AUTH-FAIL-CLOSED` must exercise the actual failure/unavailability path.

## 3. Frozen role topology

```text
NAIA:
  runtime = independent
  workspace = independent
  credentials = independent
  connectors = explicit

Anna:
  runtime = independent
  workspace = independent
  credentials = independent
  connectors = explicit

cross-role:
  direct Octop Bridge = disabled
  shared workspace = forbidden
  allowed crossing = explicit Atento handoff broker only
```

This intentionally selects the lower-authority topology rather than trying to repurpose the stock Bridge as the Atento broker.

## 4. Bridge authority disposition

The exact-pin Bridge policy is run-backed and can mutate agent/tool configuration and perform browser handoff.

Therefore:

```text
OCTOP_BRIDGE != ATENTO_BROKER
STOCK_BRIDGE_ROLE_MUTATION_AUTHORITY = TOO_BROAD_FOR_CROSS_ROLE_PATH
```

Gate 2 does not need to prove a constrained custom Bridge if direct Bridge is absent from the frozen role composition.

Acceptance requires that neither role can reach the other through Bridge discovery/tunnels while the explicit Atento broker remains functional.

## 5. Cron connector authority

The exact pin can inject `default_open` connectors into Cron when no explicit connector picks exist.

The frozen profile forbids reliance on that fallback.

```text
every qualification cron path:
  connector picks = explicit
  default_open inheritance = not relied upon
  selected connector authority <= interactive role authority
```

`CRON-CONNECTOR` must fail if a Cron job receives an unpicked consequential connector.

## 6. Pending-HITL restart scope

Pending HITL state is process-local at the frozen pin.

This does not by itself eliminate the candidate. Gate 2 only requires:

```text
restart while approval is pending ->
  no silent execution
  no authority broadening
```

Durable continuation of a pending approval is not claimed unless separately demonstrated.

## 7. Replacement-cost classification

Current evidence supports:

```text
HITL_HARDENING = CONFIGURATION_DELTA
TOOL_GUARD_HARDENING = CONFIGURATION_DELTA
EXPLICIT_CRON_CONNECTORS = SUPPORTED
DIRECT_BRIDGE_REMOVAL_FROM_ROLE_TOPOLOGY = COMPOSITION
REQUIRED_CORE_PATCH = NOT_ESTABLISHED
REPAIR_CLASS = LOCALIZED_REPAIR
```

A mandatory product path that requires stock Bridge mutation authority would reopen the classification.

## 8. Evidence identity

```text
composition_profile_hash =
d31edd8cc866502e3bff1c5371303c85e16553462a869e553e97bf065b69c49d

policy_hash =
54db0851876df4097a981a8de0833650c6696be97e8fbcdbbc74c2e5b8c66369
```

These identify pre-execution state only.

## 9. Required execution

Execute only:

```text
ISO-1
ISO-2
ISO-3
ISO-4
ISO-5
ISO-6
AUTH-FAIL-CLOSED
CRON-CONNECTOR
```

Acceptance additionally requires:

```text
DIRECT_BRIDGE_ROLE_MUTATION = DENIED/ABSENT
BACKGROUND_AUTHORITY <= INTERACTIVE_AUTHORITY
AUTHORITY_CONTROL_FAILURE = FAIL_CLOSED
BROKER = ONLY_CROSS_ROLE_PATH
```

## 10. Current disposition

```text
OCTOP_COMPOSITION = FROZEN_V1
OCTOP_STATIC_TOPOLOGY = READY_FOR_EXECUTION
OCTOP_AUTH_FAIL_CLOSED = NOT_RUN
OCTOP_CRON_CONNECTOR = NOT_RUN
OCTOP_COMMON_GATE2 = BLOCKED_ENVIRONMENT

OCTOP_CANDIDATE_FAIL = NOT_CLAIMED
OCTOP_GATE2_PASS = NOT_CLAIMED
CURRENT_PIN_QUALIFIED = 0
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```
