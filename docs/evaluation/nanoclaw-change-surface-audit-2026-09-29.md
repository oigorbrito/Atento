# NanoClaw change-surface audit — 2026-09-29

## Contract

This audit measures the **adaptation and upstream-sync surface** of the pinned NanoClaw candidate.

It does not rank the candidate, create a shortlist, or treat a small core as proof of low total migration cost.

Source:

`nanocoai/nanoclaw@4c1eabd3ddd74cc3d71b1871da857391a9411c8d`

Relevant registry heads observed during the audit:

```text
channels  = 3f7e13b591a0c8980242b81ceff4b3f542ef839a
providers = 3959d1f055cba2320cf843b30834a278250346b8
```

Rules:

```text
SMALL_CORE != LOW_TOTAL_MIGRATION_COST
SKILL_RECIPE != ZERO_CHANGE_SURFACE
TESTED_INTEGRATION_POINT != FREE_UPSTREAM_SYNC
SOURCE_PRESENT != CURRENT_PIN_RUNTIME_PASS
```

Decision state remains:

```yaml
NAIA_BASE: NOT_SELECTED
NAIA_SHORTLIST: NOT_SELECTED
candidate_universe_complete: false
```

## 1. Product / isolation model

NanoClaw is a comparable persistent-assistant product.

Static source/documentation establishes:

- per-agent-group workspace;
- per-session/container isolation;
- separate memory/session state;
- scheduled tasks;
- channels installed through skills;
- provider abstraction;
- credential gateways;
- containerized browser/tool execution;
- agent-to-agent/wiring controls.

Credential design is particularly explicit:

- raw provider credentials are not intended to enter agent containers;
- a credential gateway injects credentials at the network boundary;
- container configuration rejects credential-looking URL/userinfo/query material;
- gateway/provider contributions are typed separately from composed container state.

Current container composition also defaults the runtime tier to `container`.

Classification:

```text
PRODUCT_COMPARABLE = YES
PER_AGENT_GROUP_BOUNDARY = STRONG_STATIC_EVIDENCE
CREDENTIAL_GATEWAY_MODEL = STRONG_STATIC_EVIDENCE
CURRENT_PIN_RUNTIME_EXECUTION = NOT_OBSERVED
```

## 2. NanoClaw's skill/update model

NanoClaw explicitly treats fork customization as a recipe problem.

`docs/skills-model.md` states that:

- skills are intended to keep custom changes small and attributable;
- apply/remove is journaled;
- deterministic `nc:` directives are idempotent where supported;
- channels/providers can live on registry branches and be **copied**, not merged, into the customized install;
- integration-point tests are expected to detect drift;
- `/update-nanoclaw` snapshots, updates, runs migrations/tests and refreshes installed payloads;
- installed integrations should fail closed during upgrades when refresh cannot be completed.

This is materially better than an undocumented fork with ad-hoc edits.

However, the same upstream design explicitly recognizes channels/providers as the exception where code spans multiple integration points.

Therefore:

```text
UPDATE_MODEL = EXPLICIT_AND_TESTABLE
FORK_DRIFT_RISK = MANAGED_NOT_ELIMINATED
CHANGE_SURFACE = CAPABILITY_DEPENDENT
```

## 3. Representative capability surfaces

The useful unit is not repository size. It is the number/type of touchpoints a required NAIA profile materializes into the fork.

### WhatsApp

`.claude/skills/add-whatsapp/SKILL.md` at the pin declares:

- 4 files copied from the `channels` registry branch:
  - `src/channels/whatsapp.ts`
  - `src/channels/whatsapp-registration.test.ts`
  - `container/skills/whatsapp-formatting/SKILL.md`
  - `container/skills/whatsapp-formatting/instructions.md`
- 1 import appended to `src/channels/index.ts`;
- 4 pinned package dependencies;
- build + targeted registration test;
- external/auth/wiring state and restart operations.

Classification:

```text
WHATSAPP_CODE_FILES_COPIED = 4
WHATSAPP_CORE_IMPORT_TOUCHPOINTS = 1
WHATSAPP_DEPENDENCIES = 4
WHATSAPP_CHANGE_SURFACE = LOW_TO_MODERATE
```

A material maintenance caveat is documented by upstream itself: updating trunk without refreshing the installed channel skill can leave a stale adapter copy with old behavior.

### OneCLI credential gateway

`.claude/skills/add-onecli/SKILL.md` declares:

- 8 copied files across gateway implementation/tests, container guidance and docs;
- 1 registry import append;
- 1 pinned SDK dependency;
- gateway setup, build and targeted tests.

Classification:

```text
ONECLI_FILES_COPIED = 8
ONECLI_CORE_IMPORT_TOUCHPOINTS = 1
ONECLI_SDK_DEPENDENCIES = 1
ONECLI_CHANGE_SURFACE = MODERATE
```

This surface is offset by strong value: credential material remains outside the agent container and the gateway seam is explicit.

### OpenCode provider

The current `add-opencode` payload is a materially larger integration.

Its deterministic copy contract installs **40 files** across:

- host provider contracts;
- host provider implementation;
- container agent-runner providers/contracts;
- auth/model/vault/gateway scripts;
- setup/provider code;
- corresponding tests.

It also appends imports to **5** existing registry/index files, installs a pinned SDK, updates the CLI tool manifest and performs several build/typecheck/test/image-build steps.

Classification:

```text
OPENCODE_FILES_COPIED = 40
OPENCODE_CORE_IMPORT_TOUCHPOINTS = 5
OPENCODE_SDK_DEPENDENCIES = 1
OPENCODE_MANIFEST_TOUCHPOINTS >= 1
OPENCODE_CHANGE_SURFACE = HIGH_MULTI_POINT
```

The integration is well-instrumented, but the breadth itself remains a real upstream-sync cost.

```text
GOOD_INTEGRATION_TESTS != SMALL_INTEGRATION
```

### Ollama provider

The pinned `add-ollama-provider` skill is qualitatively different.

It is a prose/manual skill rather than a fully deterministic `nc:` payload and assumes the core has:

- `ContainerConfig.env`;
- `ContainerConfig.blockedHosts`;
- corresponding runner wiring.

At the exact pinned core, the materialized `ContainerConfig` interface contains neither field. The current session composition instead takes provider/gateway contributions through the newer typed contribution seams.

Therefore the skill's prerequisite is **not met by the pinned core as written**.

The skill instructs manual core changes when fields are absent, including:

- changes to `src/container-config.ts`;
- changes to `src/container-runner.ts`;
- potentially a Dockerfile permission change;
- per-group environment/model edits.

The recommended `blockedHosts` control is specifically intended to stop accidental fallback to Anthropic billing, but that field is not present in the current core interface.

Classification:

```text
OLLAMA_SKILL_CORE_PREREQUISITE = NOT_MET_AT_PIN
OLLAMA_ZERO_TOUCH_CONFIG = NO
OLLAMA_CURRENT_SKILL = REQUIRES_REDERIVATION_AGAINST_CURRENT_PROVIDER_SEAM
OLLAMA_CHANGE_SURFACE = NOT_DEFENSIBLY_LOW_UNTIL_REDERIVED
```

This is not evidence that local models are impossible in NanoClaw. It is evidence that the **current published skill instructions and current pinned architecture are skewed** for this path.

## 4. Security / isolation findings relevant to adaptation

Static current-source evidence also includes:

- agent container hardening with dropped Linux capabilities / no-new-privileges in current architecture;
- typed runtime isolation tier;
- group-folder/session admission labels;
- credential-value refusal in contributed environment lanes;
- one-writer inbound/outbound session DB split;
- fail-closed scope handling on relevant control-plane paths;
- explicit admin approvals for self-modifying MCP installation paths.

NanoClaw also supports a stronger egress-lockdown architecture in source that routes agent traffic through a selected gateway and is documented as fail-fast when the network/gateway cannot be established.

These are useful primitives, but any Atento qualification must test the **actual selected capability recipe**, not an uncomposed trunk.

```text
TRUNK_SECURITY_PRIMITIVES != COMPOSED_PROFILE_PROOF
```

## 5. Hosted execution visibility

For exact pin:

`4c1eabd3ddd74cc3d71b1871da857391a9411c8d`

hosted execution is now observed and recorded in:

`docs/evaluation/nanoclaw-exhaustive-verification-2026-09-30.md`

Exact-pin core CI run `36624644303` passed, including Node 22/24 host+container matrices and the Iron front-proxy race gate. Exact-pin registry-skills run `36624644411` also passed its channel/provider matrix, combined-provider, legacy-refresh, promotion and registry gates.

This supersedes the original no-run observation without changing the earlier change-surface measurements.

## 6. Adaptation profiles

The same NanoClaw core can produce materially different maintenance surfaces.

### Profile A — trunk + one channel + OneCLI

Representative touchpoints:

```text
WhatsApp:
  copied files = 4
  existing-file imports = 1
  dependencies = 4

OneCLI:
  copied files = 8
  existing-file imports = 1
  SDK dependency = 1
```

This is a moderate and explicit composition surface.

### Profile B — OpenCode + channel + gateway

OpenCode alone adds:

```text
40 copied files
+ 5 existing registry/index touches
+ SDK/manifest/build integration
```

Total fork maintenance is therefore materially larger.

### Profile C — Ollama + channel

At this exact pin, the published Ollama skill cannot be counted as a low-touch profile because it assumes obsolete/missing core fields and requires rederivation against the newer provider contribution architecture.

## 7. Current disposition

```text
NANOCLAW_PRODUCT_COMPARABLE = YES
NANOCLAW_CORE_ARCHITECTURE = SMALL_AND_EXPLICIT
SKILL_UPDATE_MODEL = STRONG_STATIC
CREDENTIAL_ISOLATION_MODEL = STRONG_STATIC

CHANGE_SURFACE:
  WHATSAPP = LOW_TO_MODERATE
  ONECLI = MODERATE
  OPENCODE = HIGH_MULTI_POINT
  OLLAMA = REQUIRES_REDERIVATION_AT_PIN

UPSTREAM_SYNC_COST = PROFILE_DEPENDENT
CURRENT_PIN_RUNTIME_EXECUTION = NOT_OBSERVED
NANOCLAW_CURRENT_PIN_QUALIFIED = NO
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

NanoClaw should not be rejected because a provider is multi-point, and it should not be preferred merely because the core is small. The relevant comparison is **total adaptation + maintenance cost for the exact NAIA capability profile**.

## 8. Smallest next empirical probe

If NanoClaw remains decision-relevant, freeze one representative NAIA recipe before execution.

A defensible first recipe is:

```text
one messaging channel
+ one credential gateway
+ one provider path
+ scheduled task
+ persistent memory
```

For that frozen recipe:

1. start from the exact upstream pin;
2. apply skills using the supported update/apply path;
3. preserve pre/post Git diff;
4. count added/copied/modified existing files and dependency changes;
5. apply again to prove idempotency;
6. execute the integration tests declared by the skills;
7. restart and prove memory/schedule persistence;
8. prove raw credentials do not enter the agent container;
9. perform one controlled upstream-update refresh and record conflicts/repairs;
10. preserve raw output.

For local-model testing, first rederive Ollama integration using the **current provider contribution seam** rather than patching the obsolete skill instructions blindly.

Until then:

```text
NANOCLAW_TOTAL_MIGRATION_COST = NOT_MEASURED_EMPIRICALLY
NANOCLAW_RUNTIME_TRANSFER = PENDING
```
