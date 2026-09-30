# AI Butler contract audit — 2026-09-29

## Contract

This audit establishes only the static operational contracts and maturity gaps of the pinned AI Butler candidate.

It does not rank candidates, create a shortlist, or convert upstream `ready` labels into independent Atento runtime proof.

Source:

`LumabyteCo/aibutler@c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c`

```text
UPSTREAM_READY != ATENTO_RUNTIME_PASS
STATIC_SOURCE != CURRENT_PIN_QUALIFICATION
COMPARABLE_PRODUCT != SELECTED
```

Decision state remains:

```yaml
NAIA_BASE: NOT_SELECTED
NAIA_SHORTLIST: NOT_SELECTED
candidate_universe_complete: false
```

## 1. Product completeness

At the pin, AI Butler exposes an end-to-end self-hosted assistant surface:

- web chat + terminal REPL;
- persistent scheduler;
- persistent mission engine;
- local memory/knowledge graph/FTS/vector stack;
- provider abstraction with local/cloud model paths;
- MCP client/server;
- browser automation;
- OS-native scripting;
- credential vault;
- capability-gated tools and audit;
- multiple channel adapters.

The repository itself labels the release/public surface as beta and distinguishes `ready` from `beta` features.

Classification:

```text
PRODUCT_COMPARABLE = YES
ASSISTANT_RUNTIME = ESTABLISHED_SOURCE/DOCS
MATURITY_MODEL = EXPLICIT_READY_VS_BETA
```

## 2. Memory isolation

The memory bank package explicitly scopes memory by isolation namespace.

Observed contracts:

- primary profile and background workers use separate banks by default;
- cross-bank access requires an explicit capability grant;
- database migration adds a bank dimension to memory tables;
- FTS and transcript isolation tests exist;
- multi-run/swarm workspace isolation tests exist.

Classification:

```text
PER_PROFILE_MEMORY_ISOLATION = STRONG_STATIC_EVIDENCE
CROSS_BANK_ACCESS = EXPLICIT_CAPABILITY_ONLY
IMPLICIT_SHARED_MEMORY = NOT_OBSERVED
```

This is compatible with NAIA's requirement that memory authority not silently expand across bounded agents.

## 3. Shell / OS authority

The security model is comparatively conservative.

Observed contracts:

- shell security defaults to `allowlist`;
- an empty allowlist denies execution;
- destructive/unlisted commands do not get a silent workaround;
- PowerShell, AppleScript, D-Bus and Shortcuts executors use allowlists;
- OS scripting tools are capability-gated;
- subprocess bridges inherit the shell sandbox;
- file operations enforce workspace boundaries and block symlink traversal;
- WASM plugins start with no filesystem/network/syscall capability unless granted.

Classification:

```text
SHELL_DEFAULT_POSTURE = FAIL_CLOSED_STATIC
EMPTY_ALLOWLIST = DENY
OS_SCRIPT_AUTHORITY = CAPABILITY_GATED
PLUGIN_SANDBOX = STRONG_STATIC_EVIDENCE
```

## 4. Credential authority

The just-in-time credential broker is documented/implemented as default-deny.

Observed behavior:

- stored credentials are not granted merely because a key exists;
- explicit auto-approved key lists control automatic issuance;
- credential requests are audited with agent ID and key;
- unknown/default cases do not silently grant.

Classification:

```text
CREDENTIAL_BROKER = DEFAULT_DENY_STATIC
CREDENTIAL_ACCESS_AUDIT = PRESENT
NAIA_CREDENTIAL_MODEL_FIT = STRONG_STATIC
```

## 5. Scheduler / background authority

The scheduler is persistent across restart and can run through different dispatch paths.

Current code/documentation establishes:

- schedules persist;
- due work and downtime recovery use the same dispatch decision;
- schedules can carry explicit capability subsets;
- recovery preserves those capability profiles rather than bypassing them.

This is materially aligned with NAIA's rule that background work must not gain more authority than its declared profile.

However per-schedule capability profiles are labeled beta.

Classification:

```text
SCHEDULER_PERSISTENCE = ESTABLISHED_SOURCE/DOCS
DOWNTIME_RECOVERY = ESTABLISHED_SOURCE
SCHEDULE_CAPABILITY_PROFILE = PRESENT_BETA
BACKGROUND_AUTHORITY_BYPASS = NOT_OBSERVED_STATIC
```

## 6. Mission / long-horizon state

The mission engine is a persistent state machine with:

- created/planned/running/waiting/completed/failed/cancelled states;
- persistent goals and plan state;
- supervisor/worker orchestration;
- audit trail;
- pause/resume/cancel semantics.

This is relevant to NAIA's persistent delegated-work target.

Classification:

```text
LONG_HORIZON_GOAL_STATE = STRONG_STATIC_EVIDENCE
MISSION_RUNTIME = UPSTREAM_READY_LABEL
ATENTO_RUNTIME_EXECUTION = NOT_OBSERVED
```

## 7. Channels

The repository explicitly distinguishes:

```text
ready channels = web chat + terminal
beta channels = Telegram, Slack, Discord, WhatsApp, Teams, Google Chat,
                LINE, IRC, webhook, Nostr
```

Upstream CONTRIBUTING states the beta adapters are code-complete/unit-tested but still awaiting broader real-world credential validation.

Therefore:

```text
PRACTICAL_USER_SURFACE = YES
MULTI_CHANNEL_CODE_SURFACE = PRESENT
MULTI_CHANNEL_REAL_WORLD_MATURITY = PARTIAL
```

A future Atento qualification must not count all 12 channels as equally proven.

## 8. Browser and computer-use

AI Butler contains real browser automation based on chromedp.

For broader computer-use tiers:

- Linux Tier 3 accessibility has automated live validation in upstream CI design;
- Linux Tier 4 capture/input has automated live validation in upstream CI design;
- Windows UIAutomation Tier 3 is unit-tested but explicitly awaits a real interactive Windows desktop;
- Windows Tier 4 capture/input is unit-tested but explicitly awaits a real interactive Windows desktop.

The source itself documents this gap.

Classification:

```text
BROWSER_AUTOMATION = ESTABLISHED_SOURCE
LINUX_COMPUTER_USE_DESIGN = STRONGER_UPSTREAM_EVIDENCE
WINDOWS_TIER3_RUNTIME = NOT_ESTABLISHED
WINDOWS_TIER4_RUNTIME = NOT_ESTABLISHED
```

This is a material NAIA gap if Windows computer-use is part of the selected deployment profile.

## 9. Provider maturity

The repository reports:

- Claude + Ollama as ready;
- several other providers as beta;
- an explicit provider factory abstraction.

Therefore:

```text
MULTI_PROVIDER_ARCHITECTURE = PRESENT
CLAUDE/OLLAMA = UPSTREAM_READY
OTHER_PROVIDER_MATURITY = MIXED
ATENTO_PROVIDER_RUNTIME_PROOF = NOT_OBSERVED
```

## 10. Hosted execution visibility

For exact pin:

`c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c`

the available GitHub connector reports:

```text
workflow_runs = []
combined_statuses = []
```

Therefore no current-pin CI pass/fail is claimed.

## 11. Current disposition

```text
AIBUTLER_PRODUCT_COMPARABLE = YES

STRONG_STATIC:
  - per-profile memory isolation
  - fail-closed shell allowlisting
  - capability-gated OS scripting
  - credential default-deny broker
  - scheduler persistence
  - recovery preserving schedule capability profiles
  - long-horizon mission state

MATERIAL_GAPS:
  - most messaging channels remain beta
  - Windows Tier 3/4 computer-use lacks real interactive validation
  - provider maturity is mixed
  - exact-pin hosted execution not observed

AIBUTLER_CURRENT_PIN_QUALIFIED = NO
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

## 12. Smallest next probe

If AI Butler remains decision-relevant, run a narrow Atento qualification using only surfaces upstream marks ready plus one target deployment delta:

1. restart persistence of scheduler + mission state;
2. one capability-scoped scheduled action;
3. one credential-gated action proving default-deny;
4. one browser action under the same capability policy;
5. on Windows target deployments, execute Tier 3/4 real desktop validation rather than relying on unit construction tests;
6. record adaptation touchpoints and provider selection.

Do not require all beta channels to pass before deciding chassis fit. Channel breadth should be added only when the product target actually needs it.

Until then:

```text
AIBUTLER_RUNTIME_TRANSFER = PENDING
```
