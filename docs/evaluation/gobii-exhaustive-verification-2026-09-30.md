# Gobii exhaustive verification — 2026-09-30

## Contract

This record captures the maximum exact-pin verification available for Gobii in the frozen NAIA candidate universe.

It does **not** select Gobii, create a shortlist, establish NAIA/Anna isolation, or promote a runtime.

Rules preserved:

```text
UPSTREAM_EXECUTION != ATENTO_ISOLATION_PROOF
MOST_TESTS_PASSING != GENERAL_HEALTH_PASS
AGENT_SCOPING_PRIMITIVE != SAME_OWNER_ROLE_ISOLATION
DIRECT_PEER_MESSAGING != BROKER_ONLY_HANDOFF
IMPLEMENTED != QUALIFIED
QUALIFIED != SELECTED
```

Candidate:

- repository: `gobii-ai/gobii-platform`
- frozen pin: `c9929bf8ea59b4695b99dcab59aa6c97a09c5bdb`
- exact-pin workflow run: `32515641268`
- prior transfer audit: `docs/evaluation/naia-transfer-audit-rakazo-gobii-2026-09-29.md`
- shared CI audit: `docs/evaluation/candidate-upstream-ci-pin-audit-2026-09-30.md`

No candidate checkout was modified by this verification.

---

## 1. Exact-pin hosted execution

The GitHub Actions run checked out the frozen SHA exactly.

### Python test matrix

Ten Python shards executed 6,917 tests in total.

| Shard | Tests executed | Result |
|---|---:|---|
| shard_01 | 616 | PASS |
| shard_02 | 868 | PASS |
| shard_03 | 567 | PASS |
| shard_04 | 840 | FAIL — 1 failure, 1 skipped |
| shard_05 | 620 | PASS |
| shard_06 | 628 | PASS |
| shard_07 | 963 | PASS |
| shard_08 | 579 | FAIL — 1 error |
| shard_09 | 667 | PASS |
| shard_10 | 569 | PASS |

Therefore:

```text
PYTHON_SHARDS = 8_PASS_2_FAIL
PYTHON_TESTS_EXECUTED = 6917
FULL_PYTHON_GATE = FAIL
```

### Other executed jobs

- frontend: 64 test files / 385 tests passed;
- sandbox server: 51 tests executed; job passed;
- Timeline PostgreSQL integration: 1 test executed; passed;
- Complexity Guardrails: passed;
- Tag Guard: passed;
- static asset build/publication: passed;
- staging dispatch: passed.

These are useful current-pin execution results. They do not override the failed Python gate.

---

## 2. Exact observed failures

### 2.1 SMTP BCC privacy/header boundary

Failing test:

```text
tests.unit.test_smtp_transport.TestSmtpTransport
  .test_send_keeps_bcc_out_of_visible_headers
```

Observed assertion:

```text
AssertionError: 'audit@example.com' is not None
```

The test contract expects the BCC recipient to be absent from visible message headers. At this exact pin, the assertion failed.

Classification:

```text
EMAIL_BCC_HEADER_PRIVACY_CONTRACT = FAIL
FAILURE_CLASS = PRODUCT_CONTRACT / PRIVACY_BOUNDARY
ENVIRONMENT_BLOCKER = NO
```

This is not safely dismissible as a generic flaky or infrastructure failure. It is a directly asserted email privacy boundary on a consequential outbound path.

It does **not** establish that every Gobii email path leaks BCC recipients in production, but the frozen pin fails its own regression contract and cannot receive a green general-health classification.

### 2.2 Native email migration consistency

Failing test:

```text
tests.unit.test_console_email_oauth.NativeAgentEmailIntegrationTests
  .test_migration_reverse_removes_only_accountless_oauth_sessions
```

Observed exception:

```text
ModuleNotFoundError:
  No module named 'api.migrations.0460_native_email_integrations'
```

Classification:

```text
NATIVE_EMAIL_REVERSE_MIGRATION_TEST = FAIL
FAILURE_CLASS = REPOSITORY / MIGRATION TEST CONSISTENCY
ENVIRONMENT_BLOCKER = NO
```

This is narrower than the BCC failure but still a real exact-pin repository consistency defect.

---

## 3. Reusable run-backed boundary evidence

The successful shards and logs provide materially stronger evidence than source inspection alone for several Gobii mechanisms.

Observed run-backed behavior includes:

- unauthorized agent settings/delete/search paths returning permission denial;
- contact permission-request creation and already-pending handling;
- secure credential requests bound to agent/key/domain records, including re-request behavior;
- linked-agent peer-message execution;
- peer-message quota enforcement;
- agent transfer-related suites;
- revoked chat/session access producing permission denial;
- allowlist-direction/API-key/console-allowlist tagged suites executing successfully;
- sandbox-server regression execution;
- responsibility-boundary/eval surfaces present at the frozen pin.

This supports reuse of mechanism evidence for:

```text
AGENT_ACCESS_CONTROL_PRIMITIVES = RUN_BACKED
CONTACT_PERMISSION_FLOW = RUN_BACKED
SECURE_CREDENTIAL_REQUEST_PRIMITIVES = RUN_BACKED
PEER_LINK_MESSAGE_PRIMITIVES = RUN_BACKED
REVOCATION_CHECKS = RUN_BACKED_IN_REVIEWED_PATHS
SANDBOX_SERVER_BASELINE = RUN_BACKED
```

Scope limit:

These results do not instantiate the Atento NAIA/Anna topology and do not prove that two same-owner roles have independent memory, credential, tool, or channel authority.

---

## 4. Peer messaging is not the Atento handoff contract by itself

Gobii has a native linked-agent direct-message primitive. The exact-pin tests/logs exercise real peer links and peer messages.

That is a useful product capability, but Atento requires a stricter invariant:

```text
SILENT_CROSS_ROLE_INVOCATION = DENIED
EXPLICIT_BROKER_HANDOFF = ONLY_ALLOWED_CROSS_ROLE_PATH
```

Therefore:

```text
GOBII_PEER_MESSAGING = PRESENT_AND_RUN_BACKED
BROKER_ONLY_HANDOFF = NOT_ESTABLISHED
DIRECT_PEER_PRIMITIVE_CAN_BE_REUSED_AS_BROKER = NOT_PROVEN
```

A future Gobii composition would have to freeze the exact role topology and either:

1. disable direct NAIA↔Anna peer authority except through an Atento broker contract; or
2. demonstrate that the Gobii peer-link mechanism itself can be constrained to the broker-only invariant.

The current hosted suite does not prove either condition.

---

## 5. Atento residuals after this execution pass

The prior transfer audit correctly classified Gobii as `COMPOSE_FIRST` for the remaining Atento-specific properties.

The hosted execution narrows what must **not** be rerun, but does not remove the composition residuals.

Still open:

### Authority

- exact contact/email review policy for NAIA;
- scheduled/background authority no broader than interactive authority;
- org/global grants excluded from cross-role authority;
- consequential email path requalified after the BCC regression is repaired.

### Isolation

- NAIA cannot read Anna memory;
- Anna cannot read NAIA memory;
- cross-role credential use denied;
- cross-role tools/channels denied;
- same-owner identity cannot silently collapse the role boundary.

### External effects

- one concrete consequential adapter may need adapter-specific uncertain-outcome/replay proof;
- the exact-pin BCC regression blocks treating the native email path as a healthy reference adapter.

### Cost

- adaptation touchpoints and operational cost must be measured only during a real hardened composition.

No broad local benchmark is justified before those composition facts are frozen.

---

## 6. Local execution boundary

The exact-pin hosted workflow is sufficient to establish the current upstream health failure.

A separate clean local checkout was not used to override or reinterpret the hosted result. Where local network/DNS access is unavailable to the evaluator, that remains an evaluator-environment limitation, not a Gobii failure.

No result in this record depends on classifying an evaluator network error as candidate behavior.

---

## 7. Gate

The smallest defensible classification at the frozen pin is:

```text
GOBII_PIN = c9929bf8ea59b4695b99dcab59aa6c97a09c5bdb

UPSTREAM_EXACT_PIN_GENERAL_HEALTH = FAIL
PYTHON_SHARDS = 8_PASS_2_FAIL
PYTHON_TESTS_EXECUTED = 6917

FRONTEND_TESTS = PASS_385
SANDBOX_SERVER_TESTS = PASS_51
TIMELINE_POSTGRES_TEST = PASS_1

EMAIL_BCC_HEADER_PRIVACY_CONTRACT = FAIL
NATIVE_EMAIL_REVERSE_MIGRATION_TEST = FAIL

AGENT_ACCESS_PRIMITIVES = RUN_BACKED
SECURE_CREDENTIAL_REQUEST_PRIMITIVES = RUN_BACKED
PEER_MESSAGING_PRIMITIVES = RUN_BACKED

ATENTO_ROLE_ISOLATION = NOT_ESTABLISHED
BROKER_ONLY_HANDOFF = NOT_ESTABLISHED
CURRENT_PIN_QUALIFIED = NO
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

This is a substantive stop gate for this frozen Gobii pin.

A repaired upstream commit may be explicitly re-pinned and requalified. Until then, spending Atento composition effort on this exact pin would mix a known-broken upstream baseline with Atento-specific adaptation evidence.

If re-pinned:

```text
1. rerun the exact repaired upstream regression suite;
2. verify the BCC privacy contract and migration consistency are green;
3. freeze one hardened Gobii NAIA/Anna composition;
4. run only residual RP-AUTH-01 / RP-ISO-01 boundaries that remain decision-relevant;
5. collect RP-COST-01 during that real composition;
6. keep NAIA_BASE = NOT_SELECTED until comparison is complete.
```

No selection or promotion follows from this record.
