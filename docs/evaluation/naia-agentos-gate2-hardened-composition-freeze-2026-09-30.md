# NAIA Gate-2 AgentOS hardened composition freeze — 2026-09-30

## Purpose

Freeze the smallest AgentOS composition that can test the remaining Atento authority/isolation delta without rerunning the already-green exact-pin upstream suites.

This record does **not** qualify, shortlist, rank, promote or select AgentOS.

Candidate:

`use-agent-os/agent-os@226c906291fc68f3c4517623446bdaec1b48a82d`

Canonical common harness:

`NAIA-GATE2-COMPOSITION-V1`

Frozen profile:

`evals/config/naia_gate2_agentos_v1.json`

## 1. Exact-pin evidence reused

Already closed with exact-pin execution:

```text
INTERACTIVE_AUTHORITY_TRANSFER = PASS_WITH_SCOPE
HARDENED_CRON_AUTHORITY_TRANSFER = PASS_WITH_SCOPE
SENSITIVE_PATH_GUARDS_TRANSFER = PASS_WITH_SCOPE
BROWSER_POLICY_TEST_SURFACE = EXECUTED
```

Observed exact-pin suite:

```text
Linux backend = 16774 passed / 50 skipped
Windows backend = 16701 passed / 123 skipped
frontend = 2382 tests passed
Web UI Browser Smoke = success
```

Do not rerun the broad AgentOS suite for this Gate-2 composition.

## 2. Hardened role topology

```text
NAIA:
  runtime = independent process
  workspace_dir = independent
  state_dir = independent
  gateway token = independent
  provider/browser credentials = independent
  channels = independent

Anna:
  runtime = independent process
  workspace_dir = independent
  state_dir = independent
  gateway token = independent
  provider/browser credentials = independent
  channels = independent

cross-role:
  shared state_dir = forbidden
  shared workspace_dir = forbidden
  shared gateway token = forbidden
  shared credentials = forbidden
  native silent role invocation = forbidden
  allowed crossing = explicit Atento handoff broker only
```

This is a deployment composition and does not require an AgentOS core patch merely to represent the boundary.

## 3. Frozen permission/sandbox posture

The shipped convenience defaults are not accepted for unattended Atento execution.

Freeze:

```toml
[sandbox]
sandbox = true
security_grading = true

[permissions]
default_mode = "off"
cron_default_mode = "off"
```

Reason:

- AgentOS documents `bypass` as a permissive default/convenience mode;
- exact-pin tests already prove that `cron_default_mode = off` prevents interactive elevation from leaking into cron;
- the candidate therefore does not require a scheduler rewrite to represent the Atento background-authority invariant.

Target invariant:

```text
BACKGROUND_AUTHORITY <= INTERACTIVE_ROLE_AUTHORITY
```

## 4. Frozen browser policy domain

AgentOS intentionally treats browser authority as a separate policy domain because Chromium is not governed by the ordinary process sandbox.

Freeze the bounded qualification profile:

```toml
[browser]
enabled = true
headless = true
cdp_port = 0
attach_confirmed = false
allowed_domains = ["example.com"]
persist_profile = false
dialog_policy = "must_respond"
restrict_evaluate = true
```

The domain is intentionally harmless and narrow for qualification. It is not a production browsing allowlist.

The relevant residual is not whether the browser works. It is:

```text
BROWSER_EFFECT_AUTHORITY <= FROZEN_ROLE_POLICY
```

Attach mode is excluded from this composition because it can drive an operator browser and would broaden the authority surface under test.

## 5. Required execution only

Run the six common assertions:

```text
ISO-1 cross-memory read denied
ISO-2 cross-memory mutation denied
ISO-3 cross-credential use denied technically
ISO-4 cross-tool/channel use denied
ISO-5 silent cross-role invocation denied
ISO-6 explicit Atento broker positive control
```

Plus:

```text
BROWSER-1
  allowed-domain effect is available only to the intended role
  off-domain navigation/effect is denied
  Anna cannot use NAIA browser/session authority
  scheduled/background browser authority is no broader than foreground authority
  browser-policy/control failure denies
  raw role-only credentials are not exposed in model-visible browser surfaces
```

No broad benchmark or upstream regression battery is authorized by this freeze.

## 6. Replacement-cost classification

```text
REQUIRED_CORE_PATCH = NOT_ESTABLISHED
SCHEDULER_REWRITE_REQUIRED = NO
BROWSER_ENGINE_REPLACEMENT_REQUIRED = NO
REPAIR_CLASS = LOCALIZED_REPAIR
REPAIR_SURFACE = CONFIGURATION/COMPOSITION
```

This remains bounded to the frozen profile until runtime execution.

## 7. Evidence identity

```text
composition_profile_hash =
8b9a37d4f1178244b3a7c4768fb4c7f282d53a99e50ef9b195e852cea66a9f6b

policy_hash =
0cba6b4a4f30f620d13ffa2b67fb71d980303adc1d4ccc6ae9ff44105fc1cf55
```

These hashes identify pre-execution policy/composition state only.

## 8. Current disposition

The common Gate-2 execution infrastructure is still unavailable. The previous hosted path failed before steps because no runner was assigned; repeating that path would not add candidate evidence.

Therefore:

```text
AGENTOS_COMPOSITION = FROZEN_V1
AGENTOS_STATIC_TOPOLOGY = READY_FOR_EXECUTION
AGENTOS_COMMON_GATE2 = BLOCKED_ENVIRONMENT
AGENTOS_CANDIDATE_FAIL = NOT_CLAIMED
AGENTOS_GATE2_PASS = NOT_CLAIMED

CURRENT_PIN_QUALIFIED = 0
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

When an executable exact-pin environment exists, execute only ISO-1..ISO-6 plus BROWSER-1 against this frozen identity.
