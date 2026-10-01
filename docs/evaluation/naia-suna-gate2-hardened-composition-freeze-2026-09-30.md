# NAIA Gate-2 Suna hardened composition freeze — 2026-09-30

## Purpose

Freeze the smallest Suna composition that can test the remaining Atento authority/isolation delta without rerunning exact-pin upstream suites.

This record does **not** qualify, shortlist, rank, promote or select Suna.

Candidate:

`kortix-ai/suna@270c4a57c8ae5ffb85eff6d5b9700c5713612f28`

Frozen profile:

`evals/config/naia_gate2_suna_v1.json`

## 1. Reused exact-pin evidence

Already established from exact-pin hosted execution:

```text
PER_AGENT_V2_GRANT_PATH = EXECUTED_WITH_SCOPE
PROJECT/IAM_DENIAL = RUN_BACKED
GATEWAY_AUTHN/AUTHZ_NEGATIVES = RUN_BACKED
SANDBOX/GATEWAY_ACCESS_SURFACE = EXECUTED
CORE_SCENARIOS = 502_PASS
```

No broad Suna suite should be rerun for Gate 2.

## 2. Frozen role topology

Suna's project is a shared knowledge/authority domain and therefore must not be shared by NAIA and Anna.

```text
NAIA:
  project = atento-naia
  repository = independent
  grants = independent
  memory/project brain = project-local
  credentials = project-local

Anna:
  project = atento-anna
  repository = independent
  grants = independent
  memory/project brain = project-local
  credentials = project-local

cross-role:
  shared project = forbidden
  shared repository = forbidden
  shared grants = forbidden
  shared project brain = forbidden
  allowed crossing = explicit Atento handoff broker only
```

This uses the upstream project/grant model rather than attempting to treat two agents inside one project as the strict Atento boundary.

## 3. Frozen connector policy

The exact-pin audit established:

```text
v2 omitted grants -> none
missing project policy -> allow_all
risk mode:
  read -> always_run
  write/destructive -> require_approval
```

The qualification profile therefore requires:

```yaml
policy:
  default_mode: risk
```

and retains the stronger rule:

```text
selected consequential tool needing stricter treatment ->
  explicit block OR explicit approval rule
```

A project that falls back to `allow_all` is invalid evidence for this frozen composition.

## 4. Connector-policy add-on

`CONNECTOR-POLICY` must prove:

```text
1. NAIA cannot acquire Anna connector grants.
2. Anna cannot acquire NAIA connector grants.
3. omitted v2 grants do not widen to all.
4. unmatched write/destructive connector actions require approval under risk mode.
5. an explicit block overrides permissive execution.
6. policy-control failure does not degrade to allow_all.
7. background trigger grants are a subset of the role's interactive grants.
```

The exact connector chosen for the benign qualification effect may be disposable/mock-backed; it must not broaden the candidate identity beyond the frozen project/policy mechanism.

## 5. External-effect scope

Suna documents scheduler fire dedup separately from business-effect idempotency.

Therefore:

```text
CRON_FIRE_DEDUP != EXTERNAL_EFFECT_EXACTLY_ONCE
```

Gate 2 does not require a generic exactly-once claim. Concrete high-risk adapters remain responsible for idempotency/readback/reconciliation later when selected.

## 6. Replacement-cost classification

Current evidence supports:

```text
TWO_PROJECT_TOPOLOGY = UPSTREAM_SUPPORTED
V2_DENY_BY_DEFAULT_GRANTS = AVAILABLE
HARDENED_PROJECT_POLICY = CONFIGURATION_DELTA
REQUIRED_CORE_PATCH = NOT_ESTABLISHED
REPAIR_CLASS = LOCALIZED_REPAIR
```

If a selected consequential connector bypasses the project policy path, that connector-specific seam must be reclassified separately.

## 7. Evidence identity

```text
composition_profile_hash =
a3eacedf6db39103805e5033ad1586fd54eacd176c5d75926d73e7bb79b536a4

policy_hash =
f927e119bcf47180461d590450fd72f1e22202435e833782fa7360ce9f1cfe1b
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
CONNECTOR-POLICY
```

Acceptance additionally requires:

```text
BACKGROUND_GRANTS <= INTERACTIVE_GRANTS
POLICY_CONTROL_FAILURE = FAIL_CLOSED
SHARED_PROJECT_BRAIN = NOT_USED_ACROSS_ROLE_BOUNDARY
```

## 9. Current disposition

```text
SUNA_COMPOSITION = FROZEN_V1
SUNA_STATIC_TOPOLOGY = READY_FOR_EXECUTION
SUNA_CONNECTOR_POLICY = NOT_RUN
SUNA_COMMON_GATE2 = BLOCKED_ENVIRONMENT

SUNA_CANDIDATE_FAIL = NOT_CLAIMED
SUNA_GATE2_PASS = NOT_CLAIMED
CURRENT_PIN_QUALIFIED = 0
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```
