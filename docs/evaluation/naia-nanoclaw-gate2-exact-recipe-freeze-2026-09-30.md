# NAIA Gate-2 NanoClaw exact recipe freeze — 2026-09-30

## Purpose

Freeze one decision-relevant NanoClaw recipe from exact-pin/exact-registry evidence so the Gate-2 SUT identity is no longer ambiguous.

This record does **not** qualify, shortlist, rank, promote or select NanoClaw.

Core candidate:

`nanocoai/nanoclaw@4c1eabd3ddd74cc3d71b1871da857391a9411c8d`

Frozen profile:

`evals/config/naia_gate2_nanoclaw_v1.json`

## 1. Why this recipe is not an arbitrary product preference

The exact-pin registry workflow run `36624644411` checked out the frozen core pin and resolved:

```text
channels_sha  = 3f7e13b591a0c8980242b81ceff4b3f542ef839a
providers_sha = 3959d1f055cba2320cf843b30834a278250346b8
```

The same run successfully applied/tested both:

```text
add-telegram
add-codex
```

The core pin itself carries the in-tree OneCLI gateway skill and pins:

```text
onecli gateway = 1.41.0
onecli CLI     = 2.2.5
onecli SDK     = 2.2.1
```

Therefore the qualification recipe reuses one exact combination already represented by the candidate's own composition machinery rather than inventing a new channel/provider stack.

## 2. Frozen recipe identity

```text
core:
  4c1eabd3ddd74cc3d71b1871da857391a9411c8d

channel:
  registry ref = 3f7e13b591a0c8980242b81ceff4b3f542ef839a
  skill = add-telegram
  package = @chat-adapter/telegram@4.29.0

provider:
  registry ref = 3959d1f055cba2320cf843b30834a278250346b8
  skill = add-codex
  package = @openai/codex@0.155.1

credential gateway:
  source = core-pin in-tree add-onecli payload
  gateway = 1.41.0
  CLI = 2.2.5
  SDK = 2.2.1
```

The registry run proves application/testing of Telegram and Codex against this core. It does **not** by itself prove the complete OneCLI-backed Atento runtime recipe.

## 3. Frozen role topology

```text
NAIA:
  agent group = atento-naia
  runtime container = independent
  group state = independent
  memory = group-local
  OneCLI agent identity = group-bound
  OneCLI secret grants = independent
  Telegram channel instance = independent
  provider = Codex

Anna:
  agent group = atento-anna
  runtime container = independent
  group state = independent
  memory = group-local
  OneCLI agent identity = group-bound
  OneCLI secret grants = independent
  Telegram channel instance = independent
  provider = Codex

cross-role:
  shared group state = forbidden
  cross-group CLI = forbidden
  cross-group mounts = forbidden
  shared gateway secret grants = forbidden
  shared channel instance = forbidden
  native cross-role handoff = forbidden
  allowed crossing = explicit Atento handoff broker only
```

## 4. Gateway authority assumptions converted to tests

The exact OneCLI payload source binds gateway agent identity to `agentGroupId`, scopes approval subscription by installation/group ownership, denies translation errors, and leaves foreign ownership requests undecided rather than claiming authority over them.

The setup path also rejects an incompatible/unreachable v1 gateway as not ready.

These are source contracts until exercised in the frozen complete recipe.

Required recipe checks:

```text
ownership unavailable -> no approval/effect
approval translation failure -> deny
gateway unavailable/incompatible -> fail closed
role secret grants -> group-local
real provider credential -> absent from container-readable env/files/args
background authority <= interactive role authority
```

## 5. RECIPE-FREEZE add-on

Execute the common six assertions plus the recipe-specific checks:

```text
ISO-1 cross-memory read denied
ISO-2 cross-memory mutation denied
ISO-3 cross-credential use denied
ISO-4 cross-tool/channel use denied
ISO-5 silent cross-role invocation denied
ISO-6 explicit Atento broker positive control

RECIPE-FREEZE:
  exact core/channels/providers refs match
  exact OneCLI versions match
  add-telegram remains installed/registered
  add-codex remains installed/registered
  apply/reapply/update preserves the frozen boundary
  restart preserves group/state/credential isolation
  scheduled task preserves same-or-narrower authority
```

## 6. Evidence identity

```text
composition_profile_hash =
1b1bfa822a4dc1154a4e78b059f01bdfc22c7bcabbfeea095d4bd8985dd2c875

policy_hash =
29d441dd951db8308af0ed7056e4ad585bee909678a8adcd26cf39f8e44d31b6
```

These are canonical SHA-256 hashes of the serialized `topology` and `policy` objects in the machine-readable freeze.

## 7. Replacement-cost classification

```text
CHANNEL_INSTALL = SUPPORTED_SKILL_COMPOSITION
PROVIDER_INSTALL = SUPPORTED_SKILL_COMPOSITION
GATEWAY_INSTALL = SUPPORTED_IN_TREE_SKILL_COMPOSITION
GROUP_ISOLATION = SUPPORTED_MECHANISM
CORE_PATCH_REQUIRED = NOT_ESTABLISHED
REPAIR_CLASS = LOCALIZED_REPAIR
```

The skill-application surface remains adaptation cost and must be measured during the real recipe run.

## 8. Current disposition

```text
NANOCLAW_RECIPE = FROZEN_V1
NANOCLAW_STATIC_TOPOLOGY = READY_FOR_EXECUTION
NANOCLAW_COMPLETE_RECIPE_RUNTIME = NOT_RUN
NANOCLAW_COMMON_GATE2 = BLOCKED_ENVIRONMENT

NANOCLAW_CANDIDATE_FAIL = NOT_CLAIMED
NANOCLAW_GATE2_PASS = NOT_CLAIMED
CURRENT_PIN_QUALIFIED = 0
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```
