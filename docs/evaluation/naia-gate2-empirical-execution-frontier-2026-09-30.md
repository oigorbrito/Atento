# NAIA Gate-2 empirical execution frontier — 2026-09-30

## Purpose

Freeze the next empirical authority/isolation execution target without creating a shortlist or selecting a base.

The target is chosen by **residual evidence size**, not preference:

```text
NEXT_TEST_TARGET =
  candidate with the largest amount of exact-pin authority evidence already executed
  + smallest remaining Atento-specific composition delta
```

## Evidence comparison relevant to the next run

### AI Butler

`LumabyteCo/aibutler@c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c`

Exact-pin hosted evidence:

- CI success;
- Security success;
- race-detector test job success;
- exact executed packages covering memory bank isolation, capability monotonicity, shell/sandbox, credential broker and scoped scheduler authority.

Canonical closure:

`docs/evaluation/aibutler-gate2-transferable-authority-closure-2026-09-30.md`

Residual:

```text
ONE_ATENTO_SPECIFIC_RESIDUAL =
  two-role NAIA/Anna negative composition
```

### OpenClaw

`openclaw/openclaw@ca8f24d05fc49a224adab0c9426077fd8d93801d`

Exact-pin CI exists and is green, and the required hardening profile is statically expressible without a core patch.

However the exact push CI observed did not establish execution of the specific A2A negative scenario or the Atento two-runtime composition.

Residual remains broader than AI Butler's transferable executed set.

### QwenPaw

`agentscope-ai/QwenPaw@777441721aa72db8e380d90e4d0481b05cbfd4cc`

Direct Actions lookup corrects the earlier “no hosted execution observed” statement in part:

```text
E2E Smoke Tests = SUCCESS
Frontend Tests = SUCCESS
Pre-commit Checks = SUCCESS
CodeQL = SUCCESS
Tests = WAITING
Full Tests Nightly = FAILURE
```

The successful E2E smoke is UI coverage and does not close the sandbox-fallback / cron-authority residual.

Because the principal `Tests` workflow is not completed successfully at the observed exact pin, authority clauses are not transferred as runtime PASS.

## Frontier decision

```text
GATE2_EXECUTION_FRONTIER = FROZEN_V1
NEXT_EMPIRICAL_COMPOSITION_TARGET = AI_BUTLER

REASON =
  exact-pin executed authority evidence closes the most relevant clauses
  AND only one Atento-specific two-role negative composition remains

THIS_IS_NOT =
  shortlist
  winner
  base selection
  performance ranking
```

No candidate is promoted by being first in execution order.

## Frozen next test

Execute only the AI Butler two-role composition:

```text
NAIA runtime:
  independent runtime/config
  independent memory authority
  independent vault
  role-specific channel/tool capabilities

Anna runtime:
  independent runtime/config
  independent memory authority
  independent vault
  role-specific channel/tool capabilities

cross-role path:
  explicit Atento broker only
```

Negative assertions:

```text
CROSS_MEMORY_READ = DENIED
CROSS_MEMORY_MUTATION = DENIED
CROSS_CREDENTIAL_USE = DENIED
CROSS_TOOL_OR_CHANNEL_USE = DENIED
SILENT_AGENT_INVOCATION = DENIED
BACKGROUND_AUTHORITY <= INTERACTIVE_AUTHORITY
EXPLICIT_BROKER_HANDOFF = ONLY_ALLOWED_CROSS_ROLE_PATH
```

Outcome mapping:

```text
all relevant negatives pass:
  AI_BUTLER_GATE2 = PASS_WITH_SCOPE

bounded configuration defect:
  LOCALIZED_REPAIR
  rerun only failed clause

authority crosses independent domains or requires distributed core patches:
  CROSS_CUTTING_STRUCTURAL_REWRITE
  eliminate current pin as complete base
```

## Environment limitation

The current execution environment cannot resolve github.com for a local clone. This is recorded as an executor/network limitation, not candidate evidence.

Do not replace the missing composition run with a claim of PASS.

```text
LOCAL_CLONE_NETWORK = BLOCKED_DNS
AI_BUTLER_COMPOSITION_EXECUTION = READY_BUT_NOT_RUN
```
