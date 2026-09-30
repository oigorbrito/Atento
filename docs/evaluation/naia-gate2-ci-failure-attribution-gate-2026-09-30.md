# NAIA Gate-2 CI-failure attribution gate — 2026-09-30

## Purpose

Attribute exact-pin CI failures for candidates previously marked simply as “CI red,” so unrelated product/test failures are not confused with authority/isolation failure.

Candidates covered:

- Rakazo
- Gobii
- PersonalJarvis
- OpenGrokBot

## Result

```text
CI_FAILURE_ATTRIBUTION_GATE = COMPLETE_V1

Rakazo:
  overall CI red
  cause = one onboarding/focus-card E2E mismatch
  authority/isolation tests in same run = pass with scope
  frontier eligible = YES

Gobii:
  overall CI red
  causes include missing migration module + Bcc privacy regression
  frontier eligible = NO_AT_CURRENT_PIN
  eliminated = NO

PersonalJarvis:
  overall CI red
  directly relevant failure = Society/MCP routes without explicit policy classification
  repair class = localized policy coverage
  frontier eligible = NO_AT_CURRENT_PIN
  eliminated = NO

OpenGrokBot:
  overall CI red
  cause = one turn batching/concurrency mismatch
  approval/memory tests = pass with scope
  browser consequential-effect technical gate remains open
  frontier eligible = NO_AT_CURRENT_PIN
  eliminated = NO

NEW_TECHNICAL_ELIMINATIONS = 0
```

## Key rule confirmed

```text
CI_RED != AUTHORITY_FAIL
CI_GREEN != AUTHORITY_PASS
PER_TEST_EXECUTION + DECISION_RELEVANCE = TRANSFERABLE_EVIDENCE
```

Rakazo is the only candidate in this attribution group whose red workflow is caused by an unrelated test while the relevant authority/isolation cases executed successfully enough to reduce the remaining Gate-2 uncertainty to hardened composition.

Gobii remains blocked by a current-pin privacy-contract failure.

PersonalJarvis remains blocked by explicit policy-coverage incompleteness in its Society/MCP surface.

OpenGrokBot remains blocked by the already-known mandatory-browser-effect-gate gap, not by its red CI.
