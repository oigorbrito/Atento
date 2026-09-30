# NAIA Gate-2 exact-pin hosted-execution reconciliation — 2026-09-30

## Purpose

Reconcile exact-pin GitHub Actions evidence for Gate-2 survivors that were previously marked `HOSTED_EXECUTION = NOT_OBSERVED` because the earlier connector path did not enumerate Actions runs by `head_sha`.

This record corrects evidence visibility only. A green CI run is transferred to Gate 2 only when directly relevant authority/isolation tests are observed in the executed job.

## Reconciled exact-pin statuses

```text
Suna           = CI/Tests/CodeQL SUCCESS
Letta Code     = CI SUCCESS with unit/API/headless/package matrix
RustFox        = CI SUCCESS with authority/isolation tests
Holt           = CI SUCCESS, build-only evidence observed
HubOS          = Pre-commit SUCCESS only

Rakazo         = CI FAILURE
Gobii          = CI FAILURE
PersonalJarvis = CI FAILURE
OpenGrokBot    = CI FAILURE

OpenAgentd     = NO ACTIONS RUN OBSERVED
AutoMate       = NO ACTIONS RUN OBSERVED
Agent Zero     = build/publish evidence only; no relevant test CI observed
```

## Transfer consequence

### Admitted to transferable-evidence frontier

```text
Suna
Letta Code
RustFox
```

Reason: exact-pin successful execution includes tests materially relevant to Gate-2 authority/isolation clauses.

Canonical records:

- `docs/evaluation/suna-gate2-transferable-authority-closure-2026-09-30.md`
- `docs/evaluation/letta-code-gate2-transferable-authority-closure-2026-09-30.md`
- `docs/evaluation/rustfox-gate2-transferable-authority-closure-2026-09-30.md`

### Not admitted from CI alone

```text
Holt:
  exact-pin CI green
  observed job = builds on Node 20/22
  no authority/isolation test evidence established from the job

HubOS:
  exact-pin Pre-commit green
  formatting/lint/static checks only
  no authority/isolation runtime clause closed

Agent Zero:
  build/publish workflows exist
  relevant Gate-2 test execution not established
```

### Exact-pin CI failures

The following exact pins have failed CI runs:

```text
Rakazo
Gobii
PersonalJarvis
OpenGrokBot
```

This record does **not** convert those failures into candidate elimination.

```text
CI_FAILURE != CANDIDATE_AUTHORITY_FAIL
```

A failure matters to Gate 2 only after attributing it to a decision-relevant authority/isolation contract. Until then the candidate remains technically alive under the previously frozen residual.

## Gate result

```text
EXACT_PIN_HOSTED_EXECUTION_RECONCILIATION = COMPLETE_V1

NEW_FRONTIER_ADMISSIONS = [Suna, Letta Code, RustFox]
CI_GREEN_BUT_NOT_AUTHORITY_ADMITTED = [Holt, HubOS]
CI_FAILURE_REQUIRES_ATTRIBUTION = [Rakazo, Gobii, PersonalJarvis, OpenGrokBot]
NO_RELEVANT_HOSTED_TEST_EXECUTION = [OpenAgentd, AutoMate, Agent Zero]

NEW_TECHNICAL_ELIMINATIONS = 0
```

This gate reduces redundant local work but does not qualify or rank candidates.
