# Rakazo exhaustive verification — 2026-09-30

## Scope

Candidate: `elie222/rakazo`

Frozen evaluation pin:

```
f4583525d632fcd8643fd6e24c7f51e3e04cb990
```

This record upgrades the prior transfer audit with exact-pin hosted execution.

Rules preserved:

- `LATER_PASS != RETROACTIVE_ERASURE_OF_EARLIER_FAIL`
- `FLAKY_SIGNAL != DETERMINISTIC_FUNCTIONAL_FAIL`
- `UPSTREAM_PASS != ATENTO_ISOLATION_PROOF`
- `CONFIGURABLE_APPROVAL != SAFE_DEFAULT`
- `TEAM_COMPUTER_PROFILE_SEPARATION != STRICT_AGENT_ISOLATION`
- `IMPLEMENTED != QUALIFIED`
- `VERIFIED != ACCEPTED`
- `ACCEPTED != PROMOTED`

No Rakazo source was modified.

## Exact-pin push CI

Run:

- workflow: `ci`
- run: `36619326151`
- exact head: `f4583525d632fcd8643fd6e24c7f51e3e04cb990`
- event: `push`
- overall conclusion: `failure`

Successful jobs:

- Typecheck
- Lint
- Production builds
- Postgres journeys
- Unit tests

Failing job:

- Web E2E

### Unit suite

Observed unit result:

```
Test Files 446 passed | 28 skipped (474)
Tests      5504 passed | 172 skipped (5676)
```

No unit failure was reported.

Run-backed security/authority-adjacent suites include, among many others:

- `approval-effect.test.ts` — 25 tests
- `executor-readonly-approval.test.ts` — 38
- `executor-approval-replay.test.ts` — 18
- `action-approval.test.ts` — 30
- `mcp-approval.test.ts` — 11
- `approval-effect-key.test.ts` — 7
- `secrets-model-visibility-conformance.test.ts` — 10
- `bot-secrets.test.ts` — 29 adapter tests + 54 contract tests
- `credential-secrets.test.ts` — 10
- `run-secret.test.ts` — 14
- `secrets-guard.test.ts` — 12
- `pi-oauth.test.ts` — 102
- `mcp-oauth.test.ts` — 19
- `executor-oauth-retire.test.ts` — 4
- `computer-lifecycle.test.ts` — 69
- `computer-spec.test.ts` — 72
- `executor-computer-safety.test.ts` — 33

Several integration-shaped files requiring extra infrastructure were skipped in the generic unit job, including PostgreSQL/computer-use cases. They must not be counted as executed merely because their source exists.

Classification:

```ini
UNIT_SUITE = PASS
TYPECHECK = PASS
LINT = PASS
PRODUCTION_BUILD = PASS
AUTHORITY_SECRET_MECHANISMS = RUN_BACKED_AT_UNIT_LEVEL
```

## Postgres journeys

The dedicated Postgres job passed all observed test groups, including the 41-test `journeys.test.ts` group and the separate authorization group.

The job ran multiple isolated PostgreSQL-backed suites rather than relying on the unit job's skipped database cases.

Classification:

```ini
POSTGRES_JOURNEYS = PASS
POSTGRES_BACKED_EXECUTION = OBSERVED
```

## Push Web E2E failure

The push Web E2E result was:

```
154 passed
1 failed
```

Failed case:

```
e2e/new-bot-ux.spec.ts
later bot waits before showing the focus card; sending cancels it
```

The run also reported five agent runs whose persisted error was:

```
Scripted run failure
```

The Web E2E job therefore failed with exit code 1.

This is a real exact-pin red result and is preserved as such.

## Same-pin nightly verification

Later on 2026-09-30, scheduled run:

- workflow: `nightly verification`
- run: `36661225457`
- exact same SHA: `f4583525d632fcd8643fd6e24c7f51e3e04cb990`
- conclusion: `success`

The browser suite reported:

```
155 passed
```

The exact test that failed in the push run passed in the nightly:

```
later bot waits before showing the focus card; sending cancels it = PASS
```

The two marketing E2Es also passed.

No corresponding `Failed agent runs` / `Scripted run failure` summary was observed in the successful nightly log.

Classification:

```ini
PUSH_E2E = FAIL_1_OF_155
LATER_SAME_PIN_NIGHTLY_E2E = PASS_155_OF_155
SAME_PIN_RESULT_STABILITY = FLAKY_OR_TIMING_SENSITIVE_SIGNAL
DETERMINISTIC_REPRODUCIBLE_FAILURE = NOT_ESTABLISHED
```

The later green run does not erase the earlier failure. Conversely, the earlier single failure cannot be treated as deterministic when the exact same code and test later pass.

A stability claim would require repeated equivalent executions, not one red and one green sample.

## Transfer evidence now run-backed

The previous Rakazo/Gobii transfer audit remains the mechanism-level interpretation. Several of its Rakazo claims now have direct exact-pin execution support because the broad unit suite ran successfully.

### Approval replay / effect handling

Exact-pin unit execution includes approval/effect/replay suites. Therefore the source-level mechanisms for approval argument/resource binding and replay/effect handling are no longer source-only evidence.

The previous bounded interpretation still applies:

```ini
APPROVAL_REPLAY_MECHANISM = RUN_BACKED_WITH_SCOPE
BLIND_REPLAY_PREVENTION = RUN_BACKED_MECHANISM_EVIDENCE
GENERIC_PROVIDER_EXACTLY_ONCE = NOT_CLAIMED
```

### Secret handling

Exact-pin secret visibility, bot-secret, credential-secret, run-secret and guard suites passed.

```ini
MODEL_VISIBLE_SECRET_GUARDS = RUN_BACKED_WITH_SCOPE
BOT_SECRET_CONTRACT = RUN_BACKED_WITH_SCOPE
```

This does not turn account-level model credentials into role-separated data-bearing authority; topology still matters.

### Computer boundary

A large exact-pin computer lifecycle/spec/safety surface passed, but the dedicated `computer-use.e2e.test.ts` and some Docker/Postgres computer cases were skipped in the generic unit job.

The architectural distinction remains:

```ini
TEAM_COMPUTER_BROWSER_PROFILE_SEPARATION = PRESENT
TEAM_COMPUTER_STRICT_AGENT_ISOLATION = NO
PRIVATE_COMPUTER_ISOLATION_UNIT = AVAILABLE
REAL_COMPUTER_E2E_IN_UNIT_JOB = SKIPPED
```

Strict NAIA/Anna composition must not rely on two browser profiles inside one Team Computer as the security boundary.

## Consequential-action default remains an Atento delta

The prior audit established that actions run by default while confirmation rules are optional/advanced configuration.

Nothing in the new CI evidence changes that product default.

```ini
APPROVAL_MECHANISM = STRONG
DEFAULT_CONSEQUENTIAL_POSTURE = NOT_ATENTO_HARDENED
ATENTO_REQUIRED_PROFILE = FAIL_CLOSED_RULESET
```

## Space boundary and strict role composition

Rakazo's Space model remains a strong application privacy boundary, and data-bearing secrets are Space-scoped.

But Atento still needs to freeze a role topology such as:

```
NAIA -> separate Space + Private Computer
Anna -> separate Space + Private Computer
cross-role path -> explicit broker only
```

The exact-pin upstream test runs do not instantiate that NAIA/Anna topology.

## Gate

Smallest defensible classification:

```ini
CANDIDATE = RAKAZO
PIN = f4583525d632fcd8643fd6e24c7f51e3e04cb990

UNIT_SUITE = PASS
POSTGRES_JOURNEYS = PASS
TYPECHECK = PASS
LINT = PASS
PRODUCTION_BUILD = PASS

PUSH_WEB_E2E = FAIL_1_OF_155
NIGHTLY_SAME_PIN_WEB_E2E = PASS_155_OF_155
E2E_STABILITY = MIXED_SAME_PIN

APPROVAL_EFFECT_MECHANISMS = RUN_BACKED_WITH_SCOPE
SECRET_VISIBILITY_MECHANISMS = RUN_BACKED_WITH_SCOPE

HARDENED_APPROVAL_PROFILE = NOT_FROZEN
STRICT_NAIA_ANNA_TOPOLOGY = NOT_RUN
BROKER_ONLY_HANDOFF = NOT_RUN
ATENTO_ISOLATION = NOT_ESTABLISHED
NAIA_BASE = NOT_SELECTED
PROMOTION = NO
```

The exact pin is not classified as a deterministic upstream functional failure because the only browser failure was not reproduced by the later same-pin full browser run. It is also not classified as a clean/stable E2E pass because the red execution remains valid evidence.

## Smallest remaining Rakazo probe

If Rakazo remains decision-relevant, do not repeat broad upstream suites. Compose only the Atento-specific delta:

1. separate NAIA/Anna Spaces;
2. separate Private Computers or stronger runtime boundary;
3. explicit fail-closed consequential approval rules;
4. data-bearing credentials confined per role;
5. broker-only handoff;
6. one scheduled consequential action under the same authority profile;
7. one provider-specific ambiguous-effect case only if that adapter lacks reconciliation;
8. optionally repeat the focus-card E2E enough times to characterize flake rate if UI stability becomes decision-critical.

## Evidence references

- push CI: https://github.com/elie222/rakazo/actions/runs/36619326151
- same-pin nightly verification: https://github.com/elie222/rakazo/actions/runs/36661225457
- frozen pin: https://github.com/elie222/rakazo/commit/f4583525d632fcd8643fd6e24c7f51e3e04cb990
- prior transfer audit: `docs/evaluation/naia-transfer-audit-rakazo-gobii-2026-09-29.md`

## Final disposition for comparison table

```ini
RAKAZO_FROZEN_PIN_STATUS = PASS_GENERAL_WITH_MIXED_E2E_STABILITY
FUNCTIONAL_BASELINE = STRONG
ATENTO_COMPOSITION = PENDING
FLAKE_SIGNAL = PRESENT
```
