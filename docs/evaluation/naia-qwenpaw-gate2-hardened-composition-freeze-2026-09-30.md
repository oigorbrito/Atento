# NAIA Gate-2 QwenPaw hardened composition freeze — 2026-09-30

## Purpose

Freeze the smallest QwenPaw composition that can test the remaining Atento authority/isolation delta without rerunning the exact-pin matrix.

This record does **not** qualify, shortlist, rank, promote or select QwenPaw.

Candidate:

`agentscope-ai/QwenPaw@777441721aa72db8e380d90e4d0481b05cbfd4cc`

Frozen profile:

`evals/config/naia_gate2_qwenpaw_v1.json`

## 1. Reused exact-pin evidence

Already established:

```text
SECURITY_GUARDIAN_CONTRACT = PASS_UPSTREAM_EXACT_PIN
CONTRACT_MATRIX_CROSS_PLATFORM = PASS_WITH_SCOPE
INTEGRATED_MATRIX_CROSS_PLATFORM = PASS_WITH_SCOPE
APPROVAL/CRON/SANDBOX_TEST_SURFACE = EXECUTED_AT_EXACT_PIN
```

The Python 3.13 Linux unit lane has four PTY/terminal failures after 17,040 passes. That runtime-specific failure is preserved and is not treated as an authority-policy failure.

No broad QwenPaw rerun is justified for Gate 2.

## 2. Frozen runtime scope

The qualification composition uses:

```text
target Python runtime = 3.11
Python 3.13 PTY path = excluded as unresolved at this frozen pin
```

This is a scope restriction, not a claim that the Python 3.13 defect is repaired.

## 3. Frozen role topology

```text
NAIA:
  runtime/store = independent
  credentials = independent
  sandbox domain = independent

Anna:
  runtime/store = independent
  credentials = independent
  sandbox domain = independent

cross-role:
  shared store = forbidden
  shared credentials = forbidden
  native cross-role invocation = forbidden
  allowed crossing = explicit Atento handoff broker only
```

## 4. Sandbox-unavailable invariant

The decisive rule is:

```text
sandbox unavailable/degraded -> DENY
unsandboxed fallback -> forbidden
```

`SANDBOX-UNAVAILABLE` must prove that a tool requiring confinement does not silently execute on the host or another less-restricted runtime when the sandbox mechanism is absent, unhealthy or rejected.

This is distinct from proving that the normal sandbox works.

## 5. Cron authority

`CRON-AUTHORITY` must prove:

```text
scheduled/background tool authority <= interactive hardened role authority
cross-role channel/tool grants are unavailable
sandbox failure on cron follows the same deny rule
authority-control failure does not broaden execution
```

No background path may treat unattended execution as an implicit approval.

## 6. Replacement-cost classification

Current evidence supports:

```text
PY311_TARGET_RUNTIME = SUPPORTED
SANDBOX/GUARDIAN_MECHANISM = EXECUTED_UPSTREAM
ROLE_SEPARATION = COMPOSITION
PY313_PTY_DEFECT = SCOPED_OUT_NOT_REPAIRED
REQUIRED_CORE_PATCH_FOR_PY311_PROFILE = NOT_ESTABLISHED
REPAIR_CLASS = LOCALIZED_REPAIR
```

If the target product later requires the unresolved Python 3.13 PTY path, this runtime-scope decision must be reopened.

## 7. Evidence identity

```text
composition_profile_hash =
640e8a2ebef817037e4392a74647fc9b67cabc5c9e0816700d3139dbc6da5f4a

policy_hash =
b671ded09fc82028b1cfba146acfac4c06e7d3e891e0a3bb7c2c9a34dcd1ab7a
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
SANDBOX-UNAVAILABLE
CRON-AUTHORITY
```

Acceptance additionally requires:

```text
UNSANDBOXED_FALLBACK = ABSENT
BACKGROUND_AUTHORITY <= INTERACTIVE_AUTHORITY
AUTHORITY_CONTROL_FAILURE = FAIL_CLOSED
BROKER = ONLY_CROSS_ROLE_PATH
```

## 9. Current disposition

```text
QWENPAW_COMPOSITION = FROZEN_V1
QWENPAW_RUNTIME_SCOPE = PYTHON_3_11
QWENPAW_STATIC_TOPOLOGY = READY_FOR_EXECUTION
QWENPAW_SANDBOX_UNAVAILABLE = NOT_RUN
QWENPAW_CRON_AUTHORITY = NOT_RUN
QWENPAW_COMMON_GATE2 = BLOCKED_ENVIRONMENT

QWENPAW_CANDIDATE_FAIL = NOT_CLAIMED
QWENPAW_GATE2_PASS = NOT_CLAIMED
CURRENT_PIN_QUALIFIED = 0
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```
