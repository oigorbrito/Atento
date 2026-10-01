# NAIA Gate-2 Rakazo hardened composition freeze — 2026-09-30

## Purpose

Freeze the smallest Rakazo composition that can test the remaining Atento authority/isolation delta without rerunning already-observed exact-pin suites.

This record does **not** qualify, shortlist, rank, promote or select Rakazo.

Candidate:

`elie222/rakazo@f4583525d632fcd8643fd6e24c7f51e3e04cb990`

Frozen profile:

`evals/config/naia_gate2_rakazo_v1.json`

## 1. Reused exact-pin evidence

Already preserved:

```text
APPROVAL_RESUME_PATH = PASS_UPSTREAM_EXACT_PIN
SCREEN_PROXY_ISOLATION = PASS_UPSTREAM_EXACT_PIN
SPACE_PRIVACY_BOUNDARY = PASS_UPSTREAM_EXACT_PIN_WITH_SCOPE
APPROVAL_UI/PERSISTENCE_SURFACE = EXECUTED
POSTGRES_JOURNEYS = PASS
UNIT_TESTS = PASS
```

The exact pin also has mixed Web E2E stability evidence: one onboarding timing failure on the push run and a later same-pin full-green rerun. That unrelated UI instability does not become an authority failure.

No broad Rakazo rerun is justified for Gate 2.

## 2. Frozen role topology

Rakazo's own architecture states that the computer container is the security boundary and that Team Computer is not an isolation boundary for mutually untrusted bots.

Therefore:

```text
NAIA:
  Space = atento-naia
  Computer = Private
  memory = Space-local
  data-bearing credentials = Space-local

Anna:
  Space = atento-anna
  Computer = Private
  memory = Space-local
  data-bearing credentials = Space-local

cross-role:
  shared Space = forbidden
  Team Computer as security boundary = forbidden
  cross-role path = explicit Atento handoff broker only
```

Distinct browser profiles inside one Team Computer do not satisfy the frozen topology.

## 3. Frozen consequential-action posture

The exact-pin evidence establishes a strong approval mechanism, but the product default allows actions to run while confirmations are optional advanced settings.

That default is not accepted for NAIA.

Freeze:

```text
selected consequential action ->
  explicit confirmation rule required

default consequential execution without the frozen rule ->
  forbidden for qualification
```

`CONSEQUENTIAL-RULES` must prove the effective rule, not merely the existence of approval UI.

## 4. Required rule behavior

For one benign representative external effect plus one denied effect, prove:

```text
explicit deny -> effect does not run
allow-once -> only the approved attempt runs
always-allow scope -> does not escape the exact intended tool/resource scope
changed resource/account binding -> stale approval does not authorize the new target
authority-control failure -> no effect
background/routine authority <= interactive authority
```

Already-transferred approval argument/resource binding should be reused rather than unit-tested again unless the frozen composition changes that boundary.

## 5. External-effect ambiguity

Rakazo already preserves an explicit `uncertain` effect state and avoids blind replay after ambiguous execution.

Therefore the Gate-2 composition preserves:

```text
UNCERTAIN_EFFECT = NO_BLIND_REPLAY
GENERIC_EXACTLY_ONCE = NOT_CLAIMED
```

Provider-specific reconciliation remains a later adapter concern only where the selected external effect requires it.

## 6. Replacement-cost classification

Current evidence supports:

```text
SEPARATE_SPACE_TOPOLOGY = UPSTREAM_SUPPORTED
PRIVATE_COMPUTER_ISOLATION_UNIT = AVAILABLE
APPROVAL_MECHANISM = STRONG
HARDENED_CONFIRMATION_PROFILE = CONFIGURATION_DELTA
REQUIRED_CORE_PATCH = NOT_ESTABLISHED
REPAIR_CLASS = LOCALIZED_REPAIR
```

If a selected consequential path is not governed by the frozen rule mechanism, reclassify only that path before any candidate-level conclusion.

## 7. Evidence identity

```text
composition_profile_hash =
fda374348c1c3d94ee6d69562c3fa126365b9f8505c332c9433e7af511d1eecd

policy_hash =
e906351046e89545b8dd49f36e609f499b3994a981ee9185221cda1ecaef87ec
```

These identify pre-execution composition/policy state only.

## 8. Required execution

Execute only:

```text
ISO-1
ISO-2
ISO-3
ISO-4
ISO-5
ISO-6
CONSEQUENTIAL-RULES
```

Acceptance additionally requires:

```text
TEAM_COMPUTER_SECURITY_BOUNDARY = NOT_USED
BACKGROUND_AUTHORITY <= INTERACTIVE_AUTHORITY
AUTHORITY_CONTROL_FAILURE = FAIL_CLOSED
BROKER = ONLY_CROSS_ROLE_PATH
```

## 9. Current disposition

```text
RAKAZO_COMPOSITION = FROZEN_V1
RAKAZO_STATIC_TOPOLOGY = READY_FOR_EXECUTION
RAKAZO_CONSEQUENTIAL_RULES = NOT_RUN
RAKAZO_COMMON_GATE2 = BLOCKED_ENVIRONMENT

RAKAZO_CANDIDATE_FAIL = NOT_CLAIMED
RAKAZO_GATE2_PASS = NOT_CLAIMED
CURRENT_PIN_QUALIFIED = 0
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```
