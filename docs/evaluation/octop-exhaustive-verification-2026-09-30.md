# Octop exhaustive verification — 2026-09-30

## Contract

This record captures the maximum exact-pin verification available for Octop in the frozen NAIA candidate universe.

It does **not** select Octop, create a shortlist, establish NAIA/Anna isolation, or promote a runtime.

Rules preserved:

```text
UPSTREAM_EXECUTION != ATENTO_ISOLATION_PROOF
MULTI_AGENT != STRICT_ROLE_ISOLATION
ALLOWLISTED_BRIDGE != BROKER_ONLY_HANDOFF
AVAILABLE_HITL != FAIL_CLOSED_DEFAULT
PERSISTED_CRON != BACKGROUND_AUTHORITY_PARITY
IMPLEMENTED != QUALIFIED
QUALIFIED != SELECTED
```

Candidate:

- repository: `TencentCloud/Octop`
- frozen pin: `e473dd3c4a4741618ffde1a42a3492341a189e8e`
- release workflow run: `36551442172`
- desktop package workflow run: `36551449063`
- CodeQL run: `36551421013`
- prior transfer audit: `docs/evaluation/naia-transfer-audit-octop-agentzero-rome-opengrokbot-2026-09-30.md`

No candidate checkout was modified by this verification.

---

## 1. Exact-pin hosted execution

The frozen SHA has more hosted evidence than the earlier first-page PR-only audit exposed.

### Release test suite

The release workflow checked out the exact frozen SHA and executed:

```text
uv run pytest -n auto -m "not live"
```

Observed result:

```text
3951 passed
17 skipped
5 warnings
duration = 663.04s
```

The test step completed successfully and the workflow then built and published the package.

Classification:

```text
EXACT_PIN_NON_LIVE_TEST_SUITE = PASS
PYTHON_TESTS = 3951_PASS_17_SKIPPED
UPSTREAM_GENERAL_HEALTH = PASS_WITH_SCOPE
```

The skipped/live boundary remains explicit. This is not a live-provider/browser/cloud qualification.

### Packaging / distribution

The same exact pin also completed:

- release distribution build and publication;
- Docker image build and push;
- desktop dashboard build;
- portable runtime assembly;
- native smoke import;
- desktop packaging for:
  - macOS arm64;
  - macOS amd64;
  - Linux amd64;
  - Linux arm64;
  - Windows amd64;
  - Windows arm64;
- FnOS FPK packaging;
- CodeQL analysis.

These establish packaging/runtime import health across several target platforms. They do not establish Atento role isolation.

---

## 2. Run-backed security/default contracts

The exact-pin full non-live suite includes the source tests under `tests/unit` and `tests/integration`.

### 2.1 Security defaults

`tests/unit/test_security_settings.py` asserts:

```text
hitl.enabled = false
tool_guard.enabled = true
tool_guard.mode = warn
```

The full suite passed at the frozen pin.

Therefore:

```text
HITL_MECHANISM = PRESENT
TOOL_GUARD_MECHANISM = PRESENT
DEFAULT_HITL = DISABLED
DEFAULT_TOOL_GUARD = WARN
DEFAULT_MATCHES_HARDENED_NAIA = NO
```

The earlier static classification is now run-backed at this pin.

### 2.2 Cross-user workspace denial

`tests/integration/test_workspace_api.py::test_non_owner_cannot_access_workspace` creates another user and asserts that access to the first user's agent workspace returns HTTP 403.

Because the full non-live suite passed:

```text
CROSS_USER_WORKSPACE_DENIAL = RUN_BACKED
USER_WORKSPACE_OWNERSHIP = RUN_BACKED
STRICT_SAME_OWNER_NAIA_ANNA_ISOLATION = NOT_ESTABLISHED
```

This is meaningful isolation evidence, but Atento's NAIA and Anna can belong to the same owner, so ordinary cross-user denial is insufficient.

---

## 3. Pending HITL restart remains unresolved by design

The exact-pin HITL store describes itself as:

```text
Session-scoped pending HITL records (process-local, TTL-gc).
```

Pending approval records are kept in an in-memory dictionary.

Therefore:

```text
PENDING_HITL_PROCESS_LOCAL = YES
PENDING_HITL_RESTART_CONTINUITY = NOT_ESTABLISHED
```

This is not contradicted by the broader control-plane/database restart behavior.

For Atento, a restart must not silently broaden authority. If Octop reaches a later composition phase, the useful lifecycle probe is narrow:

```text
pending approval before restart
→ restart
→ no action is silently authorized or replayed with broader authority
```

A broad restart suite is not required.

---

## 4. Cron connector authority remains composition-sensitive

The exact-pin connector contract states that `default_open=true` injects connector tools for the owner on IM and on Cron jobs when no explicit connector picks exist.

Explicit Cron picks override those defaults.

Therefore:

```text
CRON_WITH_EXPLICIT_PICKS = BOUNDED_BY_SELECTION
CRON_WITHOUT_EXPLICIT_PICKS = MAY_INHERIT_DEFAULT_OPEN_CONNECTORS
BACKGROUND_AUTHORITY_PARITY = CONFIG_DEPENDENT
```

For NAIA, the hardened composition must either:

1. use explicit connector picks for every consequential cron path; or
2. guarantee that every `default_open` connector is itself within the NAIA background authority set.

Do not infer background least privilege from interactive configuration alone.

---

## 5. New material Bridge authority surface

The frozen pin includes the Octop↔Octop Bridge / cloud-collaboration surface.

Its tunnel policy is not merely read-only.

The exact-pin test `tests/unit/bridge/test_tunnel_policy.py` asserts that a peer tunnel may perform operations including:

- GET agent resources;
- POST agent uploads;
- PATCH agent tool settings;
- POST agent reload;
- PUT agent ACP tool configuration;
- PATCH agent plugin tools;
- POST MBTI application;
- POST browser session handoff;
- generic GET/POST/PUT/PATCH/DELETE/HEAD on many agent-resource paths matched by the agent-resource allowlist.

The policy also explicitly denies management/auth/control-plane routes such as:

- `/api/users`;
- `/api/auth/login`;
- `/api/bridge/connections`;
- `/api/admin/audit`;
- `/api/settings`;
- plugin installation.

The full suite passed, so these allow/deny contracts are run-backed.

Classification:

```text
BRIDGE_PATH_ALLOWLIST = RUN_BACKED
BRIDGE_MANAGEMENT_AUTH_PATHS = DENIED_BY_POLICY
BRIDGE_AGENT_MUTATION_AUTHORITY = PRESENT
BRIDGE_TOOL_CONFIGURATION_MUTATION = PRESENT
BRIDGE_PLUGIN_TOOL_MUTATION = PRESENT
BRIDGE_BROWSER_HANDOFF = PRESENT
```

This is a major Atento-relevant distinction.

An allowlisted Bridge is **not** automatically equivalent to Atento's broker-only role handoff. The Bridge can carry administrative/mutating authority over an agent's tool configuration and other agent-scoped surfaces.

Therefore:

```text
OCTOP_BRIDGE != ATENTO_BROKER_BY_DEFAULT
NAIA_TO_ANNA_BRIDGE_DIRECT_AUTHORITY = MUST_NOT_BE_INHERITED
ANNA_TO_NAIA_BRIDGE_DIRECT_AUTHORITY = MUST_NOT_BE_INHERITED
```

For strict NAIA/Anna isolation, the smallest defensible topology is one of:

```text
A. no direct Bridge relationship between role runtimes;
   explicit Atento broker is the only cross-role path

or

B. a separately constrained Bridge profile whose allowed methods/paths
   are reduced to the exact broker contract and exclude role/tool/config mutation
```

The stock Bridge policy at this pin does not establish B.

---

## 6. What this verification closes

The following no longer need generic reruns at the frozen pin:

```text
EXACT_PIN_NON_LIVE_PRODUCT_SUITE = EXECUTED
CROSS_USER_WORKSPACE_DENIAL = RUN_BACKED
SECURITY_DEFAULTS = RUN_BACKED
BRIDGE_PATH_POLICY = RUN_BACKED
MULTIPLATFORM_PACKAGE_SMOKE = RUN_BACKED
CODEQL = PASS
```

The useful future work is only the Atento composition delta.

---

## 7. Remaining Atento residuals

### R-AUTH

Freeze a NAIA profile with:

- HITL enabled where consequential;
- tool guard enforcing rather than warning;
- explicit connector authority;
- cron authority no broader than foreground authority;
- Bridge mutation authority absent from the role unless explicitly required.

### R-ISO

Instantiate the exact NAIA/Anna topology and prove:

```text
CROSS_MEMORY_READ = DENIED
CROSS_CREDENTIAL_USE = DENIED
CROSS_TOOL_OR_CHANNEL_USE = DENIED
SILENT_AGENT_INVOCATION = DENIED
DIRECT_BRIDGE_ROLE_MUTATION = DENIED
EXPLICIT_BROKER_HANDOFF = ONLY_ALLOWED_CROSS_ROLE_PATH
```

Cross-user workspace tests cannot substitute for this same-owner role test.

### R-LIFE

Only the pending-HITL restart seam remains decision-relevant if the chosen composition relies on persistent approval continuity.

### R-EFFECT

No generic exactly-once external-effect claim follows from cron persistence, HITL or Bridge.

### R-COST

Measure adaptation only during a real hardened composition.

---

## 8. Gate

The smallest defensible classification is:

```text
OCTOP_PIN = e473dd3c4a4741618ffde1a42a3492341a189e8e

UPSTREAM_EXACT_PIN_GENERAL_HEALTH = PASS_WITH_SCOPE
NON_LIVE_TEST_SUITE = 3951_PASS_17_SKIPPED
CODEQL = PASS
MULTIPLATFORM_PACKAGE_SMOKE = PASS

CROSS_USER_WORKSPACE_DENIAL = RUN_BACKED
SECURITY_DEFAULTS = RUN_BACKED

DEFAULT_HITL = DISABLED
DEFAULT_TOOL_GUARD = WARN
PENDING_HITL_RESTART_CONTINUITY = NOT_ESTABLISHED
CRON_BACKGROUND_AUTHORITY = CONFIG_DEPENDENT

BRIDGE_AGENT_MUTATION_AUTHORITY = PRESENT
BRIDGE_TOOL_CONFIG_MUTATION = PRESENT
BRIDGE_BROWSER_HANDOFF = PRESENT
ATENTO_BROKER_EQUIVALENCE = NOT_ESTABLISHED

ATENTO_ROLE_ISOLATION = NOT_ESTABLISHED
CURRENT_PIN_QUALIFIED = NO
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

This is not a candidate failure. It is a substantive composition gate.

The next useful Octop test is **not** another generic upstream suite. It is a hardened same-owner NAIA/Anna composition with Bridge authority removed or constrained, explicit cron connector picks, and RP-ISO-01/RP-AUTH-01 only for the residual boundaries.

No selection or promotion follows from this record.
