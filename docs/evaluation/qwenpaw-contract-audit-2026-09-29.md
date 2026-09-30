# QwenPaw contract audit — 2026-09-29

## Contract

This audit establishes only the **static operational contracts and hardening gaps** of the pinned QwenPaw candidate.

It does not rank candidates, create a shortlist, or claim runtime qualification.

Source:

`agentscope-ai/QwenPaw@777441721aa72db8e380d90e4d0481b05cbfd4cc`

```text
SOURCE_CONTRACT != RUNTIME_PASS
STRONG_PRIMITIVES != SAFE_DEFAULTS
COMPARABLE_PRODUCT != QUALIFIED
```

Current decision state remains:

```yaml
NAIA_BASE: NOT_SELECTED
NAIA_SHORTLIST: NOT_SELECTED
candidate_universe_complete: false
```

## 1. Product completeness

At the pin, QwenPaw exposes an end-to-end personal-assistant product surface:

- persistent per-Agent workspaces and memory;
- scheduled/cron work;
- messaging channels and web/desktop/TUI/CLI entry points;
- browser automation;
- optional desktop Computer Use on Windows/macOS;
- local and hosted model/provider paths;
- multi-agent/sub-agent support;
- tool governance, file protection and sandboxing.

Therefore:

```text
PRODUCT_COMPARABLE = YES
PERSISTENT_ASSISTANT_SURFACE = ESTABLISHED_SOURCE/DOCS
```

## 2. Memory and agent isolation

Upstream architecture documents the workspace as the per-Agent boundary and describes:

- separate workspace/config/chat history per Agent;
- per-role/per-Agent memory isolation;
- memory backend plugins with explicit isolation configuration;
- default per-Agent memory isolation for supported remote memory plugins;
- explicit shared modes rather than implicit cross-Agent fallback.

The plugin documentation also states that an unavailable memory backend fails explicitly rather than silently redirecting to another store.

Classification:

```text
PER_AGENT_MEMORY_MODEL = STRONG_STATIC_EVIDENCE
IMPLICIT_BACKEND_FALLBACK = NOT_OBSERVED
EXPLICIT_SHARED_MEMORY_MODE = SUPPORTED
STRICT_NAIA_ANNA_BOUNDARY = STILL_REQUIRES_SEPARATE_AUTHORITY CONTRACT
```

The existence of explicit shared modes means Atento must keep them disabled across NAIA/Anna unless a handoff-specific design authorizes otherwise.

## 3. Governance policy

`src/qwenpaw/governance/policy.py` implements:

- builtin system rules + user rules;
- actions `ALLOW`, `DENY`, `ASK`, `SANDBOX_FALLBACK`;
- per-Agent grantee matching;
- session-scoped approvals bound to `session_id`;
- sensitive-path protection;
- hard deny patterns for destructive shell operations;
- explicit policy rule persistence after approval.

A session-scoped rule fails closed when the request cannot prove the same session.

Classification:

```text
POLICY_PRIMITIVES = STRONG_STATIC_EVIDENCE
SESSION_SCOPED_AUTHORITY = FAIL_CLOSED_STATIC
SENSITIVE_PATH_GUARDS = STRONG_STATIC_EVIDENCE
```

## 4. Material NAIA mismatch — sandbox fallback

The current `ResourceGovernor` contains a deliberate fallback:

When the policy result is `SANDBOX_FALLBACK` but the sandbox is disabled or unavailable, it rewrites the decision to:

```text
ALLOW
reason = "... running unsandboxed"
```

Upstream unit tests explicitly document this behavior.

Separately, the global setting `security.sandbox_enabled` defaults to `false`.

Therefore the candidate's default/fallback posture is not equivalent to NAIA's required:

```text
isolation unavailable
→ do not broaden authority
→ fail closed
```

Classification:

```text
SANDBOX_PRIMITIVES = PRESENT
SANDBOX_DEFAULT = DISABLED
SANDBOX_UNAVAILABLE_FALLBACK = FAIL_OPEN_FOR_SANDBOX_FALLBACK_PATH
NAIA_DEFAULT_POLICY_FIT = NEEDS_HARDENING
```

This is a **configuration/runtime policy gap**, not proof that QwenPaw is unusable. A NAIA profile must prove that no relevant tool path converts missing isolation into broader unsandboxed authority.

## 5. Scheduled/background tool safety

QwenPaw has Cron/scheduled work, but the Console's current contract states that job `toolSafety`:

- can require risky tool approval;
- may block unattended cron jobs when enabled;
- is **disabled by default**;
- leaves File Guard active when disabled.

For NAIA, background execution must not silently gain a broader authority profile than interactive execution.

Classification:

```text
CRON_CAPABILITY = ESTABLISHED
CRON_TOOL_SAFETY_CONTROL = PRESENT
CRON_TOOL_SAFETY_DEFAULT = DISABLED
NAIA_BACKGROUND_AUTHORITY_FIT = NEEDS_HARDENING
```

## 6. Browser automation

QwenPaw exposes a unified browser tool and supports:

- managed isolated Chromium;
- connecting to the user's signed-in Chrome;
- navigation, interaction, download and screenshot paths;
- per-workspace browser state/persistence.

The browser surface is a real product capability, but connection to a signed-in user's browser has materially different authority from a managed isolated browser.

Atento must treat these as distinct runtime profiles.

```text
MANAGED_BROWSER = PRODUCT_CAPABILITY_PRESENT
SIGNED_IN_USER_BROWSER = HIGHER_AUTHORITY_PROFILE
BROWSER_EFFECT_DURABILITY = NOT_ESTABLISHED
```

## 7. Desktop Computer Use

Computer Use is an optional Desktop plugin for Windows/macOS.

Observed source/documentation contracts:

- global enable switch;
- per-Agent tool enable switch;
- separate application approval;
- deny / session-only allow / persistent allow;
- native helper rejects forbidden apps;
- approval binds to canonical app identity and displayed path evidence;
- desktop input is refused when desktop is locked or recent human input is detected;
- revoking saved access forces approval again.

The native approval code accepts only a matching approval request ID with explicit `decision=allow`.

However upstream documentation also states that:

- password/verification-code fields;
- CAPTCHAs;
- system/security prompts;
- some sensitive interfaces

cannot all be detected reliably and rely partly on agent operating guidance.

Computer Use is also explicitly marked **Beta**.

Classification:

```text
COMPUTER_USE_IMPLEMENTATION = ESTABLISHED_SOURCE
APP_ID_APPROVAL_BINDING = PASS_STATIC
SESSION/PERSISTENT_APP_ACCESS = EXPLICIT
RECENT_HUMAN_INPUT_GUARD = ESTABLISHED_DOCS
SENSITIVE_UI_TECHNICAL_BLOCK = PARTIAL
COMPUTER_USE_MATURITY = BETA
RUNTIME_PROOF_AT_PIN = NOT_OBSERVED
```

## 8. Hosted execution evidence

For the exact pin:

`777441721aa72db8e380d90e4d0481b05cbfd4cc`

the available GitHub connector reports:

```text
workflow_runs = []
combined_statuses = []
```

Therefore:

```text
HOSTED_RUNTIME/TEST_PASS = NOT_CLAIMED
HOSTED_RUNTIME/TEST_FAIL = NOT_CLAIMED
```

## 9. Current disposition

```text
QWENPAW_PRODUCT_COMPARABLE = YES
MEMORY_ISOLATION_STATIC = STRONG
POLICY_PRIMITIVES_STATIC = STRONG
BROWSER_CAPABILITY = PRESENT
COMPUTER_USE_STATIC = STRONG_WITH_BETA_LIMITS

MATERIAL_GAPS:
  - sandbox fallback can broaden to unsandboxed ALLOW
  - sandbox globally disabled by default
  - cron tool-safety disabled by default
  - signed-in browser profile has elevated authority
  - Computer Use sensitive-UI blocking is partial
  - exact-pin runtime execution not observed

QWENPAW_CURRENT_PIN_QUALIFIED = NO
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

## 10. Smallest next probe

If QwenPaw remains decision-relevant, do not run a broad benchmark.

Create one hardened NAIA profile and prove:

1. sandbox enabled;
2. sandbox-unavailable relevant tool paths **deny** rather than run unsandboxed;
3. cron jobs cannot bypass the interactive authority contract;
4. managed-browser and signed-in-browser profiles are separated;
5. Computer Use approvals remain bound to Agent/session/app identity;
6. restart does not broaden persistent approvals;
7. current-pin change surface is recorded.

Acceptance:

```text
HARDENED_PROFILE_VALID = YES
NO_UNSANDBOXED_FAIL_OPEN_ON_NAIA_PATH = YES
BACKGROUND_AUTHORITY <= INTERACTIVE_AUTHORITY
APPROVAL_RESTART_DOES_NOT_BROADEN = YES
RAW_RUNTIME_EVIDENCE_PRESERVED = YES
```

Until that probe executes:

```text
QWENPAW_RUNTIME_TRANSFER = PENDING
```
