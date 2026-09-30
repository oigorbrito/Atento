# Open Assistant exhaustive verification — 2026-09-30

## Scope

Candidate: `open-assistant-org/open-assistant`

Frozen evaluation pin:

```
32c55d2643f9fe38777f9212588b2eee45392514
```

Frozen release: `v1.4.9`

This record upgrades the prior static-only audit with run-backed evidence while preserving the distinction between source/runtime evidence, Atento composition, and the separate BSL adoption boundary.

Rules preserved:

- `UPSTREAM_TEST_PASS != ATENTO_ISOLATION_PROOF`
- `IMPLEMENTED != QUALIFIED`
- `VERIFIED != ACCEPTED`
- `ACCEPTED != PROMOTED`
- `BUILD_PASS != BROWSER_RUNTIME_PASS`
- `TECHNICAL_EVIDENCE != LEGAL_ADOPTION_CLEARANCE`

No Open Assistant source was modified.

## Exact-content functional CI

The frozen commit was produced by merged PR #107.

PR head:

```
97788d87da5ccf6afb13bb1e0c1ab2e960a6cf42
```

Frozen merge commit:

```
32c55d2643f9fe38777f9212588b2eee45392514
```

GitHub commit metadata shows both commits point to the identical tree:

```
01581596cd6032e09b8f226786e24333f0afbbd3
```

Therefore the repository contents exercised by PR CI are byte-for-byte the same Git tree as the frozen pin. This avoids transferring behavior across a source delta.

PR CI run:

- run: `35429209962`
- workflow: `CI`
- job: `lint-and-test`
- conclusion: `success`
- Python: 3.11
- install: `uv sync --all-extras --dev`
- formatter: `black --check .`
- test command: `pytest --cov=src --cov-report=xml`

Observed result:

```
596 passed, 26 skipped, 8 warnings in 28.46s
Coverage: 32% (6057/19132 lines)
```

Classification:

```ini
FROZEN_TREE_FUNCTIONAL_CI = PASS
PYTEST = PASS
BLACK = PASS
TESTS_PASSED = 596
TESTS_SKIPPED = 26
LINE_COVERAGE = 32_PERCENT
```

The 32% coverage figure is descriptive. It is not an overall quality or isolation score.

## Exact-pin build and static analysis

The exact frozen commit itself also has:

- successful release workflow `35429220473`;
- successful Docker image build/push workflow `35429240899`;
- successful exact-pin CodeQL analysis, including Python and JavaScript/TypeScript, e.g. scheduled run `35970623355`.

Thus:

```ini
EXACT_PIN_DOCKER_BUILD = PASS
EXACT_PIN_RELEASE_AUTOMATION = PASS
EXACT_PIN_CODEQL = PASS
```

## Run-backed scheduler evidence

The exact-content CI executed 43 tests from `tests/test_cron_jobs.py`; all 43 passed.

Observed exercised areas include:

- create/get/list/update/delete/toggle persisted jobs;
- enabled-only listing;
- prompt and direct-tool jobs;
- cron expression validation;
- execution creation/completion/failure/history;
- `run_now`;
- recipe skip guards;
- seeded nightly-job guard expectations.

The same CI also exercised future-task persistence and direct tool execution. One prompt-task execution test was skipped.

Separate run-backed evidence includes:

```
TestSystemTokenRefreshJob::test_system_job_not_duplicated_on_restart = PASS
test_052_rebuild_is_safe_when_lock_columns_already_exist = PASS
```

This strengthens the prior source-level persistence/restart evidence.

However, no independent narrower background capability set is proven. Scheduled direct-tool jobs still execute through the ordinary tool execution surface.

Classification:

```ini
CRON_TEST_SURFACE = PASS
PERSISTED_JOB_CRUD = PASS
DIRECT_SCHEDULED_TOOL_EXECUTION_TEST = PASS
RESTART_DUPLICATE_SYSTEM_JOB_GUARD = PASS_WITH_SCOPE
BACKGROUND_TECHNICAL_CAPABILITY_SUBSET = NOT_ESTABLISHED
```

## Tool authority and planning expansion

The CI executed skill-aware planning tests. Critically, this test passed:

```
TestExpandSkillsForPlan::test_expands_to_include_all_enabled_skills
```

Additional passing assertions verify selected skills are preserved first and the system prompt is rebuilt with all backstories.

This turns the prior static observation into run-backed evidence:

```ini
INITIAL_SKILL_FILTERING = PRESENT
PLAN_EXPANSION_TO_ALL_ENABLED_SKILLS = RUN_BACKED_PRESENT
```

For a general assistant this may be intentional product behavior. For Atento's fixed NAIA/Anna authority model, it means selected-skill scoping alone cannot be treated as a security boundary. A hardened profile would need a separate technical deny/allow mechanism that planning cannot widen.

No repository-owned per-action approval boundary was established by this pass.

## Duplicate-effect guard

All 11 `tests/test_dedup_tool_calls.py` assertions passed, including:

- second identical successful call blocked inside the window;
- different tool/args allowed;
- call allowed after window expiry;
- failed result not cached.

Classification:

```ini
IN_PROCESS_DUPLICATE_CALL_GUARD = PASS
DURABLE_EXTERNAL_EFFECT_IDEMPOTENCY = NOT_ESTABLISHED
```

The tested expiry behavior confirms this is a bounded cache, not durable exactly-once semantics across restart/process boundaries.

## MCP / credential-path evidence

The CI executed 27 MCP service tests successfully.

Observed assertions include:

- multiple headers stored/rebuilt;
- header values never written into config JSON;
- blank value does not overwrite an existing secret;
- disabled tool execution raises;
- credentials are rolled back if discovery fails;
- OAuth PKCE uses S256;
- bearer header creation;
- missing token is rejected;
- expired token refresh;
- callback rejects unknown state.

Plugin authentication tests also exercised API-key/JWT storage, refresh and retry paths.

This is positive credential-handling evidence, but it does not change the static storage authority model: the audited credential repository is keyed globally by service name rather than by NAIA/Anna role identity.

```ini
MCP_SECRET_CONFIG_NON_DISCLOSURE = PASS_WITH_SCOPE
MCP_DISABLED_EXECUTION_DENIAL = PASS
OAUTH_FLOW_TESTS = PASS
PER_AGENT_CREDENTIAL_ISOLATION = NOT_ESTABLISHED
```

## Agent and conversation boundaries

Run-backed agent tests establish:

- coordinator delegation exists;
- specialist agents do not delegate by default;
- agent tool lists can be read and updated.

Slack tests establish that separate threads receive separate conversation identities and passive thread ingestion does not itself trigger an LLM reply.

Cancellation tests establish that cancellation ignores other conversations and can clear suspended state.

These are useful conversation/runtime boundaries, but they do not map one-to-one to non-forgeable NAIA/Anna authority identities.

## Browser evidence

The exact tree contains a Playwright browser implementation, as established by the prior source audit.

In the functional CI:

- browser request/model/screenshot/cookie-consent tests passed;
- the actual BrowserDriver/BrowserService navigation/click/type/scroll/extract/close tests were **skipped**;
- browser tool-registration and browser-agent runtime assertions in that group were also skipped.

Therefore:

```ini
BROWSER_IMPLEMENTATION = ESTABLISHED_SOURCE
BROWSER_MODEL_HELPER_TESTS = PASS
REAL_BROWSER_DRIVER_TESTS = SKIPPED
BROWSER_RUNTIME_PASS_AT_FROZEN_TREE = NOT_ESTABLISHED
BROWSER_NETWORK_POLICY = NOT_ESTABLISHED
```

The source-level warning that browser access can reach internal networks remains material until an Atento URL/network policy is frozen and tested.

## Memory evidence

The CI executed tiered-memory indexing/search tests successfully. Persistent conversation-memory source contracts remain scoped by `conversation_id`.

This pass does not establish a non-forgeable role identity above that conversation key.

```ini
MEMORY_HELPER_TESTS = PASS
PERSISTENT_MEMORY = ESTABLISHED_SOURCE
MEMORY_SCOPE = CONVERSATION_ID
STRICT_NAIA_ANNA_MEMORY_ISOLATION = NOT_ESTABLISHED
```

## Test-quality caveat

The green test run emitted eight warnings. Among them, several functions in `tests/test_conversation_history.py` return booleans rather than asserting, producing `PytestReturnNotNoneWarning`.

That does not invalidate the complete 596-test run, but those specific conversation-history checks are weaker evidence than ordinary assertion-based tests and are not used here to close an Atento gate.

## Legal/adoption boundary

The existing BSL 1.1 finding remains separate from technical behavior.

```ini
TECHNICAL_TESTING = COMPLETED_WITH_SCOPE
LEGAL_ADOPTION_CLEARED = NO
COMMERCIAL_ADOPTION = REQUIRES_SEPARATE_LEGAL_REVIEW_OR_PERMISSION
```

No technical result in this report overrides the license terms.

## Gate

Smallest defensible classification:

```ini
CANDIDATE = OPEN_ASSISTANT
PIN = 32c55d2643f9fe38777f9212588b2eee45392514

FROZEN_TREE_FUNCTIONAL_CI = PASS
EXACT_PIN_DOCKER_BUILD = PASS
EXACT_PIN_CODEQL = PASS
CRON_TEST_SURFACE = PASS
MCP_CREDENTIAL_HANDLING = PASS_WITH_SCOPE
IN_PROCESS_DEDUP = PASS
REAL_BROWSER_DRIVER_TESTS = SKIPPED

PLAN_EXPANSION_TO_ALL_ENABLED_SKILLS = PRESENT_RUN_BACKED
BACKGROUND_CAPABILITY_SUBSET = NOT_ESTABLISHED
PER_AGENT_CREDENTIAL_ISOLATION = NOT_ESTABLISHED
STRICT_ROLE_MEMORY_ISOLATION = NOT_ESTABLISHED
BROWSER_NETWORK_POLICY = NOT_ESTABLISHED

ATENTO_CROSS_ROLE_COMPOSITION = NOT_RUN
ATENTO_ISOLATION = NOT_ESTABLISHED
LEGAL_ADOPTION_CLEARED = NO
NAIA_BASE = NOT_SELECTED
PROMOTION = NO
```

The candidate has materially stronger runtime evidence than the prior static audit recorded, but the Atento-specific authority/isolation gap remains open.

## Smallest residual technical probe

If technical composition remains decision-relevant independently of the legal gate, freeze:

- separate NAIA and Anna stores/credentials or separate runtimes;
- a hard tool allow/deny layer that planning cannot widen;
- a background capability set no broader than interactive authority;
- an explicit browser URL/network policy.

Then execute only the unresolved cross-role and authority paths:

1. cross-role memory read/write attempts;
2. cross-role credential/tool attempts;
3. planned skill expansion against the hard deny boundary;
4. same action interactively and scheduled;
5. browser access to allowed and denied network targets;
6. restart with persisted jobs and credentials;
7. broker-only handoff.

A broad generic benchmark is not required before that composition exists.

## Evidence references

- PR CI: https://github.com/open-assistant-org/open-assistant/actions/runs/35429209962
- PR #107: https://github.com/open-assistant-org/open-assistant/pull/107
- exact-pin Docker build: https://github.com/open-assistant-org/open-assistant/actions/runs/35429240899
- exact-pin CodeQL: https://github.com/open-assistant-org/open-assistant/actions/runs/35970623355
- frozen pin: https://github.com/open-assistant-org/open-assistant/commit/32c55d2643f9fe38777f9212588b2eee45392514

## Final disposition for comparison table

```ini
OPEN_ASSISTANT_FROZEN_PIN_STATUS = PASS_UPSTREAM_WITH_ATENTO_COMPOSITION_PENDING
FUNCTIONAL_TEST_EVIDENCE = STRONG_GENERAL
BROWSER_RUNTIME_EVIDENCE = INCOMPLETE
AUTHORITY_HARDENING_REQUIRED = YES
LEGAL_GATE_SEPARATE = OPEN
```
