# Fixed-cohort common test spike — 2026-10-01

## Request and decision boundary

This spike applies the frozen system-composition protocol to every candidate in its 11-member system cohort that has not been technically eliminated. SelfAgent was already stopped at the earlier NAIA Gate 1 as a complete NAIA base at its frozen pin, so it is excluded from this remaining candidate test queue; that stop does not eliminate SelfAgent as a donor or component in a different composition. SelfAgent is not one of the fixed 11 system candidates. OpenClaw remains in the system cohort: its recorded exclusion is only from the mobile-focused view, as a product-fit scope choice. AI Butler's security block, QwenPaw's hold, and missing pins/evidence are gates or blockers, not technical eliminations.

The common profile is the same eight negative assertions for every concrete Atento composition: `SYS-CHAT-01`, `SYS-MEM-01`, `SYS-TOOL-01`, `SYS-CRED-01`, `SYS-HANDOFF-01`, `SYS-HANDOFF-02`, `SYS-BG-01`, and `SYS-STATE-01`, as defined in `atento-system-architecture-chassis-rescreen-2026-09-30.md`. The frozen sequence also measures total adaptation and ongoing maintenance cost first. Reuse applies only when exact pin, setup, property, outcome, and provenance match.

## Spike outcome

```text
FIXED_COHORT_SIZE = 11
PREVIOUS_NAIA_BASE_ELIMINATION_EXCLUDED = SelfAgent\nTECHNICALLY_ELIMINATED_FROM_FIXED_SYSTEM_COHORT = 0
NEW_COMMON_PROFILE_RUNS = 0
EQUIVALENT_UPSTREAM_TESTS_OR_BENCHMARKS_REPEATED = 0
LOCAL_ATENTO_PRODUCT_RUNTIME = ABSENT
CANDIDATE_NEUTRAL_COMPOSITION_RUNNER = NOT_IMPLEMENTED
COMMON_RESULT = BLOCKED_BEFORE_EXECUTION
COMPARABLE_SYSTEM_COST_MEASUREMENTS = 0
```

This is a harness/runtime blocker, not a candidate test failure. The workspace available for this spike is not an Atento checkout, and the frozen protocol records no candidate-neutral runner. Existing candidate probes do not launch a complete Atento host/provider composition. Therefore none of the eight common assertions can be truthfully reported as newly executed across this cohort. No candidate was silently dropped, and no previous pass was promoted to a whole-system pass.

## Prior elimination excluded from this run\n\n- **SelfAgent:** excluded because the earlier Gate-1 record stopped it as a complete NAIA base at its frozen pin. This is the prior elimination the current test request must honor. It remains possible to reuse it as donor/component evidence in another composition; no such composition was tested here.\n- **OpenClaw:** retained in the fixed full-system cohort. Its removal from the active mobile-focused view is not a technical elimination from the system comparison.\n\n## Eliminatory-gate continuation using existing evidence

The prior elimination record is scoped to a candidate role/pin; it must not be generalized across different compositions.

| Subject | Existing gate evidence | Disposition for this test queue |
|---|---|---|
| SelfAgent | NAIA Gate 1 stopped its frozen pin as a complete NAIA base due to cross-cutting authority, background-execution, and scheduler-lifecycle repairs. | Excluded from the remaining NAIA-base queue. Not part of the fixed 11 system cohort; may remain a donor/component in another composition. |
| AI Butler | The scheduled security scan for frozen pin `c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c` recorded seven reachable advisories. | Do not rerun this unchanged pin in the common runtime test. Current pin is security-blocked; the candidate family is not eliminated and may return on a remediated, frozen pin. |
| QwenPaw | Existing audit identifies a sandbox-unavailable path that may broaden authority and cron/background authority requiring hardening; passing system-level fail-closed evidence is absent. | Hold for a fail-closed profile. This is unresolved, not a demonstrated structural impossibility or candidate elimination. |
| Remaining system candidates | Existing source/CI/fixture evidence is partial or non-transferable to the full Atento profile; no system-level hard-gate failure is recorded for these candidates in the checked documents. | Retain as unresolved; do not assign PASS or FAIL from missing integration evidence. |

```text
PRIOR_NAIA_BASE_ELIMINATION = SelfAgent (scope: complete NAIA base at frozen pin)
CURRENT_PIN_SECURITY_BLOCK = AI_Butler@c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c
NEW_COMMON_ELIMINATORY_TESTS_EXECUTED = 0
NEW_SYSTEM_CANDIDATE_ELIMINATIONS = 0
```

The current common eliminatory test still cannot execute: the Atento host/runtime and candidate-neutral composition runner are absent. Reuse the gates above and proceed only when a runnable seam exists; no upstream suite or approved probe is repeated here.

## Fixed cohort and reusable evidence

The entries below preserve the frozen order. Evidence is reused as documentary or exact-pin evidence only; it does not imply that the common eight-assertion test ran.

| Order | Candidate / pin | Existing evidence to reuse | Common-spike disposition |
|---:|---|---|---|
| 1 | NanoClaw — `nanocoai/nanoclaw@4c1eabd3ddd74cc3d71b1871da857391a9411c8d` | Exact-pin upstream CI (513 passed, 0 failed, 3 skipped); Atento hosted 7/7 with scope; SSE replay after SIGKILL on the raw webhook server with synthetic tokens and same SQLite file. Existing upstream claim/orphan/restart/delivery-attempt tests cover their stated candidate lifecycle properties. | `BLOCKED_ADAPTER` for Atento composition. None of that evidence proves real provider custody or role-bound scheduled-task retry after Atento host restart. |
| 2 | AI Butler — `LumabyteCo/aibutler@c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c` | Exact-pin Atento Gate-2 6/6 with scope; exact-pin CI and scoped scheduler evidence; live eval 4/7 is its own suite. | `BLOCKED_ADAPTER`; separately `BLOCK_CURRENT_PIN_ON_SECURITY` (seven reachable advisories in the recorded scan). Do not rerun unchanged pin security or claim the scoped scheduler result is a system pass. |
| 3 | OpenClaw — `openclaw/openclaw@e9571d77e76bd6d35996273d9e8398ad539b26e1` | Exact-pin source/tests for per-agent core state; PawBench score 72.1 applies only to its published benchmark configuration. | Retained in fixed cohort; excluded only from the mobile-focused view. `BLOCKED_ADAPTER`; separate Gateway/runtime and Atento cross-role behavior remain untested. |
| 4 | QwenPaw — `agentscope-ai/QwenPaw@777441721aa72db8e380d90e4d0481b05cbfd4cc` | PawBench 73.7 for its published release; exact-pin source/CI audit and identified fail-closed/background-authority gaps. | `BLOCKED_ADAPTER` and `HOLD_FOR_FAIL_CLOSED_PROFILE`; no whole-system pass inferred from the external score or partial CI. |
| 5 | MindRoom — `mindroom-ai/mindroom@4f3bd2d108a6f9be28174e0f66d78eeecddca386` | Exact-pin source review: per-agent roots; shared-runner isolation incomplete; dedicated worker path is deployment-specific. | `BLOCKED_ADAPTER`; backend-specific runtime proof required. |
| 6 | Bob Labs — `boblabs-eu/boblabs@a91d6dad098c8ba6d24436a856556078151db45d` | Exact-pin test definitions inspected for lab scope, consent, sandbox HMAC/nonce, and secrets; execution was not established by the reviewed record. | `BLOCKED_ADAPTER`; inspected test definitions are not passing results. |
| 7 | Ontheia — `Ontheia/ontheia@70802db61eb16533f55efce3d8785d810223d03b` | Exact-pin namespace/RLS source and CI evidence already recorded. | `BLOCKED_ADAPTER`; agent/domain authority and full handoff still need Atento composition evidence. |
| 8 | OpenAkita — `openakita/openakita@5f5b38da728274f0fd06461a481851be7c0bca6a` | Exact-pin build pass and source/state-test review; Python/unit/integration/smoke/E2E jobs were skipped in the recorded evidence. | `BLOCKED_ADAPTER`; no role-private isolation result inferred. |
| 9 | Clawix — `ClawixAI/clawix@5aee015e0bd793102fba69af486dd6e75df6d802` | Exact-pin lint/typecheck/test CI; reviewed multi-user tests use mocks. | `BLOCKED_ADAPTER`; no end-to-end role authorization/container-boundary result inferred. |
| 10 | Memoh — `felinics/Memoh@3d60a08aa42fdcddb218401699822741b51b52ad` (main head observed 2026-10-01) | Exact-pin license declaration now verified as AGPL-3.0; other prior discovery evidence remains scoped. | Common system run remains `BLOCKED_ADAPTER`; pin requirement is resolved, but no Atento runtime test was run. |
| 11 | Letta Code — `letta-ai/letta-code@21daa38a8cdd74f2d03b634c8312253080bacfc1` | Historical overlay fixture at a different SHA passed bounded policy/RAG/removal checks; historical Terminal-Bench scores remain benchmark-specific. | `BLOCKED_ADAPTER`; historical fixture and external score do not transfer to the current three-role composition. |

## Smallest falsifiable test once the seam exists

Prerequisites for the common cohort run:

1. An executable Atento host/runtime boundary that can compose a frozen candidate pin without adding a production integration solely for this test.
2. One candidate-neutral runner with a narrow adapter per candidate; the runner must accept the same synthetic NAIA, Anna, and Apollo identities, state sentinels, tool/credential grants, handoff payload, restart point, and assertions.
3. Memoh is now frozen at `3d60a08aa42fdcddb218401699822741b51b52ad` (main head observed 2026-10-01); keep its ordered slot and run only after a candidate adapter is executable.
4. Observable claim, terminal acknowledgement, and delivery identifiers so the test can distinguish a retry from duplicate terminal delivery.

When those prerequisites exist, run candidates serially in the frozen order. For each candidate, first record the comparable cost dimensions available, then run the same eight `SYS-*` assertions once. Include one inert NAIA scheduled task with a synthetic identity and no provider: persist it as due, terminate the host after claim and before terminal acknowledgement, restart, permit exactly one retry, and assert that the task remains NAIA-owned and terminal delivery is observed exactly once. Record each assertion independently as `PASS`, reproduced hard-gate `FAIL`, `BLOCKED`, or `BLOCKED_ADAPTER`; missing evidence is never a failure. Stop after one primary run per candidate, with only one targeted confirmation for a demonstrably invalid harness or possible hard-gate failure.

Do not repeat NanoClaw's approved SSE replay, the Atento 7/7 probe, upstream tests already cited above, or published benchmarks. This spike executed none of those again.

## Source records

- Frozen sequence/cohort and eight assertions: `docs/evaluation/atento-system-architecture-chassis-rescreen-2026-09-30.md`
- Existing candidate evidence and mobile-cohort scope: `docs/evaluation/system-chassis-isolation-adaptation-cost-2026-10-01.md`
- Execution status and existing-evidence map: `docs/evaluation/system-chassis-first-sieve-execution-status-2026-10-01.md`
- NanoClaw seam absence and exact residual: `docs/evaluation/nanoclaw-next-step-runtime-seam-audit-2026-10-01.md`
- Reliability evidence reuse and candidate-specific gates: `docs/evaluation/system-chassis-top3-reliability-recovery-2026-10-01.md`

This record is on the disposable branch only. PR #58 was not changed.


## User goal clarified — complete comparative eliminatory gates before selection — 2026-10-02

The user has clarified the governing goal: test eliminatory gates across every candidate that has not been technically eliminated, then choose one candidate only after the comparable gate evidence is complete. NanoClaw's prior designation remains a provisional direction and is not a final selection for this comparative decision. PR #58 remains outside this update.

Apply the same frozen eight SYS assertions and any other frozen hard gates to each eligible candidate in the fixed cohort. Reuse existing results only when pin, setup, property, outcome, and provenance match; run each missing test once and in frozen order. Candidate-specific component tests may add scoped evidence, but do not substitute them for an Atento composition assertion. Record hard-gate failure only when reproduced at the pinned setup; an unavailable seam, missing evidence, security block on one pin, or non-equivalent fixture remains blocked/unresolved rather than silently converted to elimination. Do not select a winner until the gate matrix contains enough comparable evidence to rule out each other eligible candidate or record an explicit remaining blocker.

Current progress includes Letta Code's scoped cron tests (99 tests / 238 assertions) and cross-agent memory-guard suite (63 tests / 102 assertions), all on its frozen pin. These do not close the common Atento assertions. Continue through candidates and gate rows serially, reusing prior NanoClaw/AI Butler results within their recorded scopes and preserving all open gates.


## Continuation — QwenPaw fail-closed eliminatory component gate — 2026-10-02

The QwenPaw frozen pin `agentscope-ai/QwenPaw@777441721aa72db8e380d90e4d0481b05cbfd4cc` was materialized and verified at the exact commit. One uncovered narrow gate was run serially: if the Hub provisioner preflight reports that its sandbox is unavailable, runtime admission must fail closed without persisting a runtime.

Existing upstream test body: `tests/unit/hub/test_service.py::test_unavailable_provisioner_rejects_runtime_registration`. Result: **PASS_WITH_SCOPE**. The test asserted that availability is false, creation raises `RuntimeProvisionerUnavailableError` with the preflight reason, and the registry remains empty. It used a synthetic unavailable provisioner and did not invoke the OS sandbox, a provider, or Atento identity/task execution.

The first ordinary pytest invocation stopped before collection because this environment lacked project dependencies and the repository-wide conftest imports the optional provider stack. To keep this one test bounded, the exact test function was invoked directly with its existing source, the exact pin's production Hub modules, and a minimal Python package loader; only pytest, Pydantic, PyYAML, and httpx were supplied. No candidate files or lockfiles changed. This is a harness adaptation disclosed for provenance, not an upstream full-suite pass.

```text
QWENPAW_SANDBOX_UNAVAILABLE_ADMISSION = PASS_WITH_SCOPE (SYNTHETIC_PROVISIONER)
QWENPAW_OS_SANDBOX_FAIL_CLOSED = NOT_TESTED_BY_THIS_CASE
QWENPAW_CRON_AUTHORITY_AND_ATENTO_NAIA_OWNERSHIP = OPEN
COMMON_ATENTO_PROFILE = BLOCKED_ADAPTER
CANDIDATE_ELIMINATION = NONE
```

This narrows the fail-closed uncertainty but does not by itself clear QwenPaw's hold: the recorded background/cron-authority gap and real sandbox enforcement remain unresolved. Keep it in the eligible comparison set, and do not infer a full-system pass.

A separate existing OpenClaw gate attempt on its frozen pin was also checked during this continuation: dependency installation from the frozen lock completed without changing tracked source, but the official test preparation refused to proceed because isolation from managed Gateway artifacts could not be verified. Its documented isolated runner requires non-root execution plus rootless Podman; this environment is UID 0 and has neither Podman nor Docker. No OpenClaw test body ran. Classify as `BLOCKED_ENVIRONMENT/HARNESS`, not a candidate result; retain OpenClaw in the fixed cohort. Do not bypass its guard.

Continue serially in frozen order with MindRoom next. The complete comparative gate matrix remains open; NanoClaw remains provisional only, and no winner is selected.


## Continuation — MindRoom workspace visibility gate — 2026-10-02

Frozen pin verified: `mindroom-ai/mindroom@4f3bd2d108a6f9be28174e0f66d78eeecddca386`. Ran only the existing scoped test:

```text
uv run --frozen --group dev -- python -m pytest -n 0 -q \
  tests/api/test_sandbox_runner_api.py::test_resolve_worker_base_dir_rejects_paths_outside_visible_workspaces
8 passed
```

The eight parameter cases check worker-visible workspace and private-scope paths and reject paths outside the worker root or its authorized visible workspaces. This exercises the source resolver used by sandbox-worker preparation; it did not start an OS/container worker, a provider, or an Atento runtime. The checkout remained at the exact frozen pin; dependency materialization followed its committed `uv.lock`.

```text
MINDROOM_WORKER_BASE_DIR_VISIBLE_WORKSPACE_GUARD = PASS_WITH_SCOPE (8 PARAMETER CASES)
MINDROOM_REAL_WORKER_BOUNDARY = NOT_TESTED_BY_THIS_CASE
MINDROOM_ATENTO_NAIA_OWNERSHIP_AND_RESTART_RETRY = OPEN
COMMON_ATENTO_PROFILE = BLOCKED_ADAPTER
CANDIDATE_ELIMINATION = NONE
```

This is reusable component evidence for workspace isolation, not a complete cross-agent production boundary result. The previously identified shared-runner/deployment-specific isolation issue remains open. Continue to Bob Labs in frozen order; the comparative selection remains pending.


## Continuation — Bob Labs sandbox replay-boundary gate — 2026-10-02

Frozen pin verified: `boblabs-eu/boblabs@a91d6dad098c8ba6d24436a856556078151db45d`. Ran one existing focused source guard:

```text
pytest control-plane/tests/regression/test_cso_2026_06_sandbox_hmac.py::test_sandbox_rejects_replayed_nonce
1 passed
```

The assertion checks that the frozen sandbox source tracks nonce use and rejects a replayed signature. It is explicitly source introspection; it does not send an HTTP request to the middleware or launch a Docker sandbox. The probe used minimal pytest/app-import dependencies and intentionally did not load the DB-backed control-plane conftest. Two warnings about unavailable asyncio pytest config options were emitted because pytest-asyncio was not installed; the selected test is synchronous and passed. No Bob Labs source or config was changed.

```text
BOBLABS_SANDBOX_REPLAY_GUARD_SOURCE_CHECK = PASS_WITH_SCOPE (STATIC SOURCE)
BOBLABS_LIVE_HMAC_MIDDLEWARE_AND_LAB_BINDING = NOT_TESTED_BY_THIS_CASE
ATENTO_ROLE_CREDENTIAL_BOUNDARY = OPEN
COMMON_ATENTO_PROFILE = BLOCKED_ADAPTER
CANDIDATE_ELIMINATION = NONE
```

This does not close Bob Labs' prior per-lab sandbox/HMAC integration uncertainty or qualify an Atento composition. Continue to Ontheia in frozen order; no candidate is selected.


## Continuation — Ontheia memory namespace authorization gate — 2026-10-02

Frozen pin verified: `Ontheia/ontheia@70802db61eb16533f55efce3d8785d810223d03b`. Reused the existing focused host memory-tool suite after the committed host lockfile install and TypeScript build:

```text
node --test dist/mcp/plugins/memory.spec.js
14 passed, 0 failed
```

The focused suite covers explicit/implicit namespace search allowlists, denial where access exists only in contextual `read_namespaces`, denial for unknown namespaces, and namespace-constrained writes. Test adapters/DB objects are mocks; no PostgreSQL RLS policy was exercised, no model/provider was called, and this is not an Atento runtime composition result. The frozen source tree stayed clean after install/build (generated dependency/build directories ignored).

```text
ONTHEIA_MEMORY_TOOL_NAMESPACE_AUTHORIZATION = PASS_WITH_SCOPE (14 MOCK-BASED TESTS)
ONTHEIA_LIVE_POSTGRES_RLS_AND_AGENT_RUNTIME = NOT_TESTED_BY_THIS_SUITE
ATENTO_CROSS_ROLE_MEMORY_ASSERTION = OPEN
COMMON_ATENTO_PROFILE = BLOCKED_ADAPTER
CANDIDATE_ELIMINATION = NONE
```

This adds scoped memory-authorization evidence only. Continue in fixed order with OpenAkita next; all candidate gates remain under comparison, with no winner selected.


## Continuation — OpenAkita memory workspace isolation gate — 2026-10-02

Frozen pin verified: `openakita/openakita@5f5b38da728274f0fd06461a481851be7c0bca6a`. Ran only the existing focused case using the project lock and dev extra:

```text
uv run --frozen --extra dev -- python -m pytest -q \
  tests/unit/test_memory_owner_isolation.py::test_same_user_different_bot_workspaces_do_not_share_memory
1 passed
```

The case writes memory for the same synthetic user in two bot workspaces and verifies that each workspace retrieves only its own entry. It is component-level store evidence: it does not exercise the three-role Atento host, a process boundary, or scheduled retry. One Starlette/httpx deprecation warning appeared during test startup; the test passed. The checkout remained on the exact frozen pin with no tracked edits.

```text
OPENAKITA_SAME_USER_BOT_WORKSPACE_MEMORY_ISOLATION = PASS_WITH_SCOPE (ONE UNIT TEST)
OPENAKITA_AGENT_PROCESS_BOUNDARY = NOT_TESTED_BY_THIS_CASE
ATENTO_ROLE_MEMORY_ASSERTION_AND_RESTART_RETRY = OPEN
COMMON_ATENTO_PROFILE = BLOCKED_ADAPTER
CANDIDATE_ELIMINATION = NONE
```

Continue to Clawix in frozen order. This narrows store-scope uncertainty but does not qualify private agent isolation in a deployed Atento composition; no winner is selected.


## Continuation — Clawix scheduled-task ownership gate — 2026-10-02

Frozen pin verified: `ClawixAI/clawix@5aee015e0bd793102fba69af486dd6e75df6d802`. After installing the frozen pnpm lock with the repository-pinned pnpm 10.32.1, one existing cron-service case was run:

```text
pnpm --filter @clawix/api exec vitest run \
  src/engine/__tests__/tools/cron.test.ts \
  -t 'rejects removing a task owned by another user'
1 passed; 33 sibling cases skipped by name filter
```

The case verifies that a user cannot remove a scheduled task owned by another user. It uses service-level test doubles and does not test a persistent production repository, process restart, Atento role identity, or terminal-delivery idempotency. No Clawix source, manifests, or lockfiles changed.

```text
CLAWIX_CROSS_USER_CRON_DELETE_GUARD = PASS_WITH_SCOPE (MOCKED SERVICE CASE)
CLAWIX_PERSISTED_ROLE_OWNERSHIP_AFTER_RESTART = NOT_TESTED_BY_THIS_CASE
ATENTO_NAIA_TASK_RETRY_AND_SINGLE_TERMINAL_DELIVERY = OPEN
COMMON_ATENTO_PROFILE = BLOCKED_ADAPTER
CANDIDATE_ELIMINATION = NONE
```

This is scoped ownership evidence only and does not close the NAIA restart/retry gate. Continue to Memoh in frozen order; no final chassis selection is made.


## Continuation — Memoh cross-bot memory mutation gate — 2026-10-02

Frozen pin verified: `felinics/Memoh@3d60a08aa42fdcddb218401699822741b51b52ad`. The previously cited builtin adapter scope tests were reused and not repeated. One distinct handler-authorization test was run:

```text
go test ./internal/handlers \
  -run '^TestChatDeleteOneRejectsForeignBotMemoryID$' -count=1
ok github.com/felinics/memoh/internal/handlers
```

It verifies that a memory ID carrying a different bot ID is rejected before the memory provider's delete method is called. This is a handler-level test with a fake provider; it does not prove database/RLS enforcement, host-process recovery, or Atento role-bound task retry. Go 1.25.7 was run from the local toolchain with build/module caches under `/tmp`; the frozen checkout remained unchanged.

```text
MEMOH_FOREIGN_BOT_MEMORY_DELETE = PASS_WITH_SCOPE (HANDLER + FAKE PROVIDER)
MEMOH_DATABASE_RLS_AND_PERSISTED_RESTART_AUTHORITY = NOT_TESTED_BY_THIS_CASE
ATENTO_NAIA_TASK_RETRY_AND_SINGLE_TERMINAL_DELIVERY = OPEN
COMMON_ATENTO_PROFILE = BLOCKED_ADAPTER
CANDIDATE_ELIMINATION = NONE
```

No builtin adapter memory suite was repeated. Continue to the final fixed-cohort slot, Letta Code; no winner is selected.


## Continuation — Letta Code Bubblewrap policy gate and cohort correction — 2026-10-02

Frozen pin verified: `letta-ai/letta-code@21daa38a8cdd74f2d03b634c8312253080bacfc1`. The already-run cron and cross-agent memory suites were not repeated. Ran one different focused sandbox-policy file:

```text
npx --yes bun@1.3.14 test src/sandbox/bwrap.test.ts
6 passed, 11 assertions
```

The tests verify argument construction for denied agent-tree masking, restoring only configured self/parent carveouts, readonly root in the write-scoped profile, and the `--die-with-parent` setting. They also explicitly verify that the profile does not unshare network. No Bubblewrap process or kernel boundary was executed; the Letta cross-agent memory suite continues to cover only its in-process guard and explicitly defers shell to the kernel sandbox.

```text
LETTA_BWRAP_POLICY_CONSTRUCTION = PASS_WITH_SCOPE (6 TESTS)
LETTA_KERNEL_ENFORCEMENT_AND_NETWORK_ISOLATION = NOT_TESTED_BY_THIS_CASE
LETTA_ATENTO_ROLE_BOUNDARY = OPEN
COMMON_ATENTO_PROFILE = BLOCKED_ADAPTER
CANDIDATE_ELIMINATION = NONE
```

**Correction to the older queue checkpoint:** the 2026-10-02 entry in the Letta continuation report that said the frozen queue was exhausted and instructed waiting was superseded by the user's clarified comparative goal. It is not the current disposition. The work is now continuing through the fixed 11-candidate cohort, applying each uncovered eliminatory component gate once and preserving candidate-specific scope. At this point Letta is the last ordered cohort slot tested in this continuation; the matrix has not established a winner because common Atento composition remains blocked for the candidates.



## Comparative gate snapshot after full-cohort component continuation — 2026-10-02

The fixed-order continuation has now visited all 11 cohort slots, excluding only the previously technically eliminated SelfAgent (outside this fixed cohort). This snapshot separates candidate-level eliminatory evidence from the still-unavailable common Atento composition:

| # | Candidate | Newly checked or reused eliminatory evidence | Current-pin disposition | Common Atento eight-assertion gate |
|---:|---|---|---|---|
| 1 | NanoClaw | Reuse exact-pin existing 7/7 Atento-scope probe, upstream lifecycle tests, and approved raw-webhook SSE restart/replay probe. None repeated here. | `PASS_WITH_SCOPE`; direction remains provisional for NAIA only. | `BLOCKED_ADAPTER` |
| 2 | AI Butler | Reuse exact-pin prior Gate-2 6/6 scoped evidence and existing scheduler evidence. | `BLOCK_CURRENT_PIN_ON_SECURITY` (seven reachable advisories); this does not eliminate the family. | `BLOCKED_ADAPTER` |
| 3 | OpenClaw | Existing secure runner attempt stopped before the test body: UID 0; official isolated runner requires non-root plus rootless Podman, neither runtime available. | `BLOCKED_ENVIRONMENT/HARNESS`; source-level cross-agent session caveat remains. | `BLOCKED_ADAPTER` |
| 4 | QwenPaw | Exact-pin sandbox-unavailable admission test passed with a synthetic unavailable provisioner. | `PASS_WITH_SCOPE`; real OS sandbox and cron/background authority remain open. | `BLOCKED_ADAPTER` |
| 5 | MindRoom | Exact-pin visible-workspace resolver test: 8 parameter cases passed. | `PASS_WITH_SCOPE`; real worker boundary and shared-runner deployment scope remain open. | `BLOCKED_ADAPTER` |
| 6 | Bob Labs | Exact-pin source guard for nonce replay rejection passed. | `PASS_WITH_SCOPE`; live sandbox middleware/HMAC/lab binding not exercised. | `BLOCKED_ADAPTER` |
| 7 | Ontheia | Exact-pin memory namespace authorization suite: 14 passed using mock adapters/DB. | `PASS_WITH_SCOPE`; live PostgreSQL RLS and agent runtime not exercised. | `BLOCKED_ADAPTER` |
| 8 | OpenAkita | Exact-pin same-user/two-bot-workspace memory isolation test passed. | `PASS_WITH_SCOPE`; no process boundary or Atento runtime result. | `BLOCKED_ADAPTER` |
| 9 | Clawix | Exact-pin cross-user scheduled-task removal denial test passed with service doubles. | `PASS_WITH_SCOPE`; persistent ownership through restart untested. | `BLOCKED_ADAPTER` |
| 10 | Memoh | Reuse existing builtin adapter bot-scope result; separate foreign-bot memory delete authorization test passed with fake provider. | `PASS_WITH_SCOPE`; DB/RLS and Atento restart/retry remain open. | `BLOCKED_ADAPTER` |
| 11 | Letta Code | Reuse exact-pin cron and cross-agent memory guard tests; separate Bubblewrap argument-policy file passed 6 tests / 11 assertions. | `PASS_WITH_SCOPE`; actual kernel enforcement and network isolation untested. | `BLOCKED_ADAPTER` |

```text
FIXED_COHORT_SLOTS_VISITED = 11_OF_11
TECHNICAL_CANDIDATE_ELIMINATIONS_IN_THIS_CONTINUATION = 0
OPEN_CURRENT_PIN_BLOCKS_OR_HOLDS = AI_BUTLER_SECURITY, QWENPAW_FAIL_CLOSED_PROFILE, OPENCLAW_HARNESS
COMMON_ATENTO_GATE_FOR_EACH_RETAINED_CANDIDATE = BLOCKED_ADAPTER
PR_58 = OPEN_DRAFT_AT_e948f344b91e20e655399b11300c439228d144ec; UNMODIFIED
PR_57 = OPEN_DRAFT_DOCUMENTATION_ONLY; NO_PRODUCT_RUNTIME
FINAL_CANDIDATE_SELECTION = NONE
NANOCLAW = PROVISIONAL_DIRECTION_ONLY
```

The PR #58 description still states that production gateway/provider wiring and role-bound scheduled-task retry/recovery are unqualified. PR #57 remains an evaluation-only, documentation-only host/runtime boundary contract and does not add an executable adapter. No executable Atento host runtime/provider gateway was found in these current open PR records. Therefore the smallest falsifiable common test remains blocked until that existing seam appears; do not build a production integration solely to unblock comparison.

### Preconditions and smallest falsifiable common test

Before running the test for each candidate, an executable Atento host/runtime seam must accept that frozen candidate pin, three synthetic role identities (NAIA/Anna/Apollo), isolated task/state/authority sentinels, a no-provider inert job, and observable claim/terminal-delivery IDs. Then, one candidate at a time: persist one due NAIA-owned inert scheduled task; stop the host after claim and before terminal acknowledgement; restart; allow one retry; assert ownership remains NAIA and terminal delivery count is exactly one. This tests the cross-cutting residual without a provider call. Any candidate adapter must be candidate-neutral in assertions and must not be a production integration created solely for this evaluation.

This component-gate continuation improves and makes explicit each pin's scoped evidence, but it does not supply comparable full-composition outcomes. No candidate can yet be selected from this matrix without treating missing adapter evidence as a pass or failure. The user-directed goal remains: finish comparable eliminatory gates for every eligible candidate, then decide.


## Normalized SYS-MEM component slice — QwenPaw — 2026-10-02

A second, more directly comparable memory gate was run on the frozen QwenPaw pin without repeating its sandbox-preflight case:

```text
uv run --extra test -- python -m pytest -n 0 -q \
  tests/integration/test_memory_context.py::test_memory_file_cross_agent_isolated
1 passed in 31.25s
```

The repository integration fixture launched the real QwenPaw app as a subprocess on an isolated temporary workspace. It created two agents, wrote a synthetic note through agent A's scoped HTTP route, verified agent B received 404 for that path, and verified agent A could read it. No provider/model was used. This is an exact-source-pin app integration result but its Python dependencies were resolved from the pin's version ranges because this repository has no root uv lockfile; warnings from uv concerned normalized legacy dependency specifiers. It still does not exercise Atento's host, role authorization, or scheduled-task recovery.

```text
QWENPAW_SCOPED_MEMORY_FILE_CROSS_AGENT = PASS_WITH_SCOPE (APP SUBPROCESS, 1 TEST)
ATENTO_SYS_MEM_01 = BLOCKED_ADAPTER
QWENPAW_CRON_AUTHORITY_AFTER_ATENTO_HOST_RESTART = OPEN
CANDIDATE_ELIMINATION = NONE
```


## Normalized SYS-MEM authorization slice — MindRoom — 2026-10-02

Frozen pin: `mindroom-ai/mindroom@4f3bd2d108a6f9be28174e0f66d78eeecddca386`. Ran the three existing negative-scope cases in sequence as one focused pytest selection:

```text
uv run --frozen --group dev -- python -m pytest -n 0 -q \
  tests/test_memory_facade.py -k 'rejects_other_agent_scope'
3 passed
```

The cases deny reading another agent's memory and reject updating or deleting it; the latter two assert that the backend mutation methods are not called. The backend is mocked. This does not test worker/process isolation, persistent authorization after restart, or Atento role authority. The frozen `uv.lock` was used; no candidate files changed.

```text
MINDROOM_CROSS_AGENT_MEMORY_READ_UPDATE_DELETE = PASS_WITH_SCOPE (3 MOCK-BASED CASES)
MINDROOM_PERSISTENT_OR_PROCESS_BOUNDARY = NOT_TESTED
ATENTO_SYS_MEM_01_AND_NAIA_RESTART_RETRY = BLOCKED_ADAPTER
CANDIDATE_ELIMINATION = NONE
```

## Bob Labs cross-lab memory authorization attempt — 2026-10-02

The exact-pin repository has a closer existing gate at `control-plane/tests/repositories/test_cross_tenant.py::test_get_all_memories_refuses_without_share_memory_confirmation`. It requires the repository's isolated PostgreSQL `bob_test` database, migrations, and environment variables provided by `make test-only`; its conftest explicitly refuses to run absent that setup or against a non-test database. This environment does not have the prepared test DB, so the test body was not started. No environment guard was bypassed and no Bob Labs candidate failure is inferred.

```text
BOBLABS_CROSS_LAB_MEMORY_CONSENT = BLOCKED_ENVIRONMENT (ISOLATED POSTGRES TEST DB NOT PREPARED)
BOBLABS_SANDBOX_REPLAY_SOURCE_CHECK = PASS_WITH_SCOPE (PREVIOUSLY RECORDED; NOT REPEATED)
ATENTO_SYS_MEM_01 = BLOCKED_ADAPTER
CANDIDATE_ELIMINATION = NONE
```



## Continuação — OpenAkita evidência SYS-MEM reutilizada — 2026-10-02

A busca no pin `openakita/openakita@5f5b38da728274f0fd06461a481851be7c0bca6a` encontrou apenas o teste de isolamento entre dois bot-workspaces já executado nesta rodada:

```text
tests/unit/test_memory_owner_isolation.py::test_same_user_different_bot_workspaces_do_not_share_memory
1 passed (recorded previously; not repeated)
```

Não encontrei um teste distinto de memória cross-agent para acrescentar sem duplicar essa propriedade. O resultado já registrado permanece `PASS_WITH_SCOPE`; processo/host Atento e restart/retry continuam abertos.

## Continuação — Clawix sub-agent approval gate bloqueado no setup — 2026-10-02

No pin `ClawixAI/clawix@5aee015e0bd793102fba69af486dd6e75df6d802`, foi identificado um caso distinto do teste de remoção cross-user de cron já executado: `tool-approval-rendezvous.test.ts::sub-agent gate auto-denies without prompting and writes no memory`. Ele seria um teste unitário da negação fail-closed para sub-agent e da ausência de prompt/gravação de memória.

A tentativa direta pelo Vitest parou na importação do arquivo, antes da coleta/teste: o módulo `../generated/prisma/client.js` não existe no checkout materializado. O binário Prisma não estava disponível como shim; usei o CLI Prisma 7.4.2 já presente no store pnpm para tentar gerar o cliente. Essa tentativa parou antes de produzir o artefato ao buscar `schema-engine` em `binaries.prisma.sh`: a conexão foi negada pelo ambiente (`EPERM`). Não pedi escalada de rede nem alterei dependências travadas. O primeiro comando pelo wrapper pnpm ainda falhou no índice SQLite do store padrão; tentar redirecioná-lo não chegou ao Vitest. Nenhum guard foi ignorado, nenhum arquivo rastreado foi alterado e o corpo do teste não executou.

```text
CLAWIX_SUBAGENT_APPROVAL_FAIL_CLOSED = BLOCKED_ENVIRONMENT/GENERATED_PRISMA_CLIENT_MISSING
CLAWIX_CROSS_USER_CRON_DELETE_GUARD = PASS_WITH_SCOPE (PREVIOUSLY RECORDED; NOT REPEATED)
CANDIDATE_FAILURE = NOT_ESTABLISHED
COMMON_ATENTO_PROFILE = BLOCKED_ADAPTER
```

Pré-condição para reabrir apenas este teste: materializar dependências de geração travadas e gerar o cliente Prisma do pin, então executar o caso filtrado uma vez. Não equivale ao gate comum Atento de tarefa NAIA após restart.


## Memoh — tentativas adicionais de negação cross-bot bloqueadas por dependências — 2026-10-02

No pin `felinics/Memoh@3d60a08aa42fdcddb218401699822741b51b52ad`, foram identificados dois casos distintos do teste de exclusão unitária já executado: `TestChatUpdateRejectsForeignBotMemoryID` e `TestChatDeleteBatchRejectsWhenAnyIDBelongsToAnotherBot`. A execução focalizada não alcançou a coleta nem os corpos dos testes.

A primeira chamada parou porque o cache Go padrão tentava escrever em `/root/.cache/go-build`, somente leitura. Com `GOCACHE` e `GOMODCACHE` redirecionados para `/tmp`, a compilação tentou baixar módulos travados que não estavam em cache; a rede para `proxy.golang.org` foi negada pelo ambiente. Não houve alteração do checkout, fallback de dependências ou relaxamento do pin.

```text
MEMOH_FOREIGN_BOT_UPDATE_AND_BATCH_DELETE = BLOCKED_ENVIRONMENT (GO MODULES ABSENT; NETWORK UNAVAILABLE)
MEMOH_FOREIGN_BOT_SINGLE_DELETE = PASS_WITH_SCOPE (PREVIOUSLY RECORDED; NOT REPEATED)
CANDIDATE_FAILURE = NOT_ESTABLISHED
COMMON_ATENTO_PROFILE = BLOCKED_ADAPTER
```

Pré-condições para reabrir os dois casos: disponibilizar os módulos exatos do `go.mod/go.sum` no cache isolado e executar somente esses filtros no mesmo pin. Nenhum resultado destes bloqueios deve ser contado como falha funcional.


## Gate eliminatório encontrado — QwenPaw cron padrão desliga aprovação de ferramentas — 2026-10-02

No pin fixo `agentscope-ai/QwenPaw@777441721aa72db8e380d90e4d0481b05cbfd4cc`, foi executada uma sonda mínima e descartável no caminho de criação/executor de tarefa agendada, sem provider nem invocação de ferramenta:

```text
UV_CACHE_DIR=/tmp/qwenpaw-memory-uv-cache uv run --frozen --extra test -- python - <<'PY'
# create default agent CronJobSpec, execute through CronExecutor,
# capture the request at workspace.stream_query, then stop before a provider/tool
PY
# observed: default_tool_safety=False; emitted approval_level=off
```

A sonda usou o builder de job do pin e o `CronExecutor` de produção. No ponto de chamada de `stream_query`, capturou `request_context.approval_level == "off"` para o job sem configuração explícita, antes de qualquer provider ou ferramenta. A asserção foi satisfeita. A inicialização tentou tocar estado em `/root/.qwenpaw`, que é somente leitura; depois de capturar o resultado, o processo Python ficou preso no encerramento de uma thread importada e foi interrompido. Essa limitação afeta a limpeza do harness, não a observação capturada.

Corroboração no mesmo pin: `src/qwenpaw/app/crons/models.py::JobRuntimeSpec.tool_safety` tem default `False` e documenta que OFF executa todas as ferramentas sem checagens de aprovação; `src/qwenpaw/app/crons/executor.py` traduz `False` em `ToolExecutionLevel.OFF`. O teste `tests/integration/test_security_real.py::test_tool_guard_blocks_dangerous_shell_via_agent_run` liga explicitamente `tool_safety=True` e comenta que o default das tarefas cron é OFF.

Isso falha o gate eliminatório de autoridade de tarefa de fundo **na configuração padrão**: uma tarefa agendada recebe modo mais permissivo sem pedido explícito, contrariando o invariante de que execução agendada/retry/recovery deve manter autoridade igual ou mais restrita que a interativa. Classificação: `FAIL_WITH_SCOPE` para `QWENPAW_DEFAULT_CRON_TOOL_AUTHORITY`; não é prova de acesso cross-role nem de exfiltração de credencial.

O modelo permite `tool_safety=True`; portanto o resultado elimina o caminho/configuração padrão, não demonstra impossibilidade estrutural do repositório inteiro. QwenPaw só pode voltar a satisfazer esse gate se o adapter/configuração da composição fixar explicitamente aprovação restritiva e um único reteste demonstrar a política efetiva depois de persistência, execução e restart. Essa configuração e reteste ainda não existem no Atento, cujo host seam segue ausente.

```text
QWENPAW_DEFAULT_CRON_TOOL_AUTHORITY = FAIL_WITH_SCOPE
PROBE_PROVIDER_OR_TOOL_CALL = NONE (CAPTURED BEFORE stream_query BODY)
QWENPAW_EXPLICIT_TOOL_SAFETY_TRUE_PATH = NOT_TESTED_HERE
QWENPAW_REPOSITORY_FAMILY_ELIMINATED = NO (STRICT OVERRIDE EXISTS; UNVERIFIED IN COMPOSITION)
QWENPAW_DEFAULT_CRON_PROFILE_ELIMINATED = YES
COMMON_ATENTO_NAIA_RESTART_RETRY = BLOCKED_ADAPTER
FINAL_SYSTEM_CHASSIS_SELECTION = NONE
```

Este achado atualiza os snapshots anteriores que listavam apenas holds e bloqueios sem reprovação funcional nova. A elegibilidade de composição do pin QwenPaw permanece condicional ao fechamento verificável desse gate; a falha de ambiente do Bob Labs e os bloqueios de harness de OpenClaw/Clawix/Memoh continuam sem valor de FAIL.


## Gate eliminatório encontrado — OpenAkita scheduler troca perfil ausente pelo agente padrão — 2026-10-02

No pin `openakita/openakita@5f5b38da728274f0fd06461a481851be7c0bca6a`, executei uma sonda descartável no resolvedor de identidade do scheduler. A consulta de perfil foi controlada para retornar ausente para um ID sintético Anna; o agente padrão foi um objeto falso e nenhum provider, modelo ou ferramenta foi chamado.

```text
UV_CACHE_DIR=/tmp/openakita-uv-cache uv run --frozen --extra dev -- python - <<'PY'
# TaskExecutor._create_agent("synthetic-anna-profile-missing")
# _resolve_agent_profile -> None; observe and assert selected agent
PY
requested_profile=synthetic-anna-profile-missing
resolved_default_agent=True
initialized=call(start_scheduler=False)
exit=0
```

A sonda executou o caminho de produção `TaskExecutor._create_agent`. O próprio código em `src/openakita/scheduler/executor.py` registra aviso para perfil desconhecido e segue para `Agent()` sem perfil: uma tarefa persistida sob Anna/Apollo, se o ID não resolver após restart, pode continuar como o agente padrão. Isto viola o gate hard de identidade/background: tarefa agendada deve manter a mesma autoridade ou menos e não pode sofrer role drift silencioso. O esperado para identidade ausente é falhar fechado, sem instanciar executor substituto.

```text
OPENAKITA_SCHEDULER_UNKNOWN_PROFILE_ROLE_PRESERVATION = FAIL_WITH_SCOPE
OPENAKITA_DEFAULT_SCHEDULER_PATH_FOR_ROLE_BOUND_TASKS = ELIMINATED_AT_FROZEN_PIN
OPENAKITA_REPOSITORY_AS_DONOR_WITH_HOST_FAIL_CLOSED_VALIDATION = NOT_ELIMINATED
PROVIDER_OR_TOOL_CALL = NONE
OPENAKITA_SAME_USER_DIFFERENT_BOT_WORKSPACE_MEMORY_TEST = PASS_WITH_SCOPE (PRIOR; NOT REPEATED)
COMMON_ATENTO_HOST_PROCESS_RESTART_COMPOSITION = BLOCKED_ADAPTER
```

Este é um hard-gate failure reproduzido para o caminho interno do scheduler do pin, não uma falha de ambiente nem extrapolação do teste de memória anterior. O repositório ainda pode ser usado como componente somente se a composição impedir a execução quando o perfil persistido não resolver e provar esse fail-closed guard no restart; tal adapter/guard não existe no host Atento auditado. Não tratar um profile ID válido e um profile ID ausente como a mesma condição.

Este achado também atualiza o snapshot anterior de OpenAkita, que continha somente PASS_WITH_SCOPE de memória entre workspaces. Essa aprovação permanece válida para sua propriedade; a nova reprovação cobre uma propriedade independente de scheduler/role identity.


## Gate eliminatório com escopo — Clawix sub-agent herda aprovação da sessão pai — 2026-10-02

No pin `ClawixAI/clawix@5aee015e0bd793102fba69af486dd6e75df6d802`, foi executado um caso existente e ainda não coberto: `tool-approval-rendezvous.test.ts::sub-agent honors existing session allow (memory flows via shared sessionId)`.

```text
./node_modules/.bin/vitest run \
  --config /tmp/clawix-minimal-vitest.config.mts \
  packages/api/src/approvals/__tests__/tool-approval-rendezvous.test.ts \
  -t 'sub-agent honors existing session allow'
1 passed; 13 sibling cases skipped by name filter
```

O teste registra autorização de sessão `(session=s1, wiki_delete, page-a)=allow`, então chama o gate com `isSubAgent=true` e o mesmo `sessionId=s1`; o resultado esperado pelo teste é `{allowed: true}`. Não houve provider, ferramenta real ou persistência de sessão; esse é o comportamento exercitado do serviço de aprovação, com repositórios em memória. A identidade consultada pelo gate inclui user e session, mas não uma identidade/domínio de agente na chave da autorização. A worktree do pin ficou limpa; foi necessário compilar somente `@clawix/shared` para `dist/` ignorado e usar config mínima do Vitest para não carregar setup Prisma não necessário a este caso.

Para o contrato Atento, isto reprova **com escopo** a composição de papéis distintos em uma mesma sessão: uma aprovação dada no contexto pai atravessa ao sub-agent, sem novo handoff/autorização de destino. Classificação: `FAIL_WITH_SCOPE` para `CLAWIX_SHARED_SESSION_CROSS_ROLE_APPROVAL`; o fluxo multi-role em sessão compartilhada está eliminado neste pin. Separar sessões por papel pode evitar esta chave compartilhada, mas então handoff mínimo, destinatário e autorização própria ainda precisam de probe; não há composição Atento executável para provar isso.

```text
CLAWIX_PARENT_SESSION_ALLOW_INHERITED_BY_SUBAGENT = REPRODUCED (1 MOCK-BASED CASE)
CLAWIX_SHARED_SESSION_CROSS_ROLE_AUTHORITY = FAIL_WITH_SCOPE
CLAWIX_SHARED_SESSION_MULTI_ROLE_COMPOSITION = ELIMINATED_AT_FROZEN_PIN
CLAWIX_REPOSITORY_FAMILY_ELIMINATED = NO (SEPARATE-SESSION ARCHITECTURE NOT TESTED)
CLAWIX_PERSISTED_APPROVAL_OR_REAL_TOOL_EXECUTION = NOT_TESTED
COMMON_ATENTO_HOST_RESTART_COMPOSITION = BLOCKED_ADAPTER
FINAL_SYSTEM_CHASSIS_SELECTION = NONE
```

Este resultado é distinto do teste anteriormente bloqueado do sub-agent sem aprovação prévia e do teste já aprovado de remover tarefa de outro usuário. Os três comportamentos mantêm classificações próprias. A aprovação existente pelo mesmo session ID não foi interpretada como autorização válida entre domínios Atento.


## Letta Code — probe de rede real bloqueado pelo sandbox do harness — 2026-10-02

No pin `letta-ai/letta-code@21daa38a8cdd74f2d03b634c8312253080bacfc1`, reutilizei sem repetição a evidência anterior de `src/sandbox/bwrap.test.ts`: o teste do pin verifica que o perfil produzido não inclui `--unshare-net`. Para determinar se isso permitia contato com um serviço local, tentei um probe descartável com um listener sintético em `127.0.0.1` e o comando Bubblewrap com mount policy equivalente.

O probe parou antes de executar o Bubblewrap: o sandbox do ambiente negou a própria criação do socket do listener com `PermissionError: [Errno 1] Operation not permitted`. Portanto não houve conexão, tentativa de fuga, execução do subprocesso nem observação de acesso a endpoint. Classificação: `BLOCKED_ENVIRONMENT`, sem PASS/FAIL de rede para Letta. Nenhum arquivo do checkout foi alterado.

```text
LETTA_BWRAP_ARGUMENTS_OMIT_UNSHARE_NET = PASS_WITH_SCOPE (EXISTING TEST REUSED)
LETTA_LOCAL_SERVICE_REACHABILITY_FROM_BWRAP = BLOCKED_ENVIRONMENT (HOST LISTENER SOCKET DENIED BEFORE BWRAP)
LETTA_NETWORK_AUTHORITY_GATE = UNRESOLVED
CANDIDATE_ELIMINATION = NONE_FROM_THIS_PROBE
COMMON_ATENTO_RESTART_GATE = BLOCKED_ADAPTER
```

Para tornar falsificável esse gate, executar o mesmo listener local sintético e o Bubblewrap do pin num ambiente que permita socket local e namespace user/mount; comparar conexão do host com conexão do processo sandbox. Mesmo um resultado positivo provaria apenas acesso a loopback sintético; para demonstrar cross-role, um serviço/credencial Atento real e a política de autorização teriam de estar presentes no adapter executável.


## MindRoom — scheduled event preserves requester through dispatch prechecks — 2026-10-02

No pin `mindroom-ai/mindroom@4f3bd2d108a6f9be28174e0e66d78eeecddca386`, executei em série dois casos existentes ainda não registrados como executados:

```text
UV_CACHE_DIR=/tmp/mindroom-uv-cache uv run --frozen --group dev -- \
  python -m pytest -n 0 -q \
  tests/test_bot_scheduling.py::TestCommandHandling::test_scheduled_agent_event_with_router_requester_reaches_dispatch_policy \
  tests/test_bot_scheduling.py::TestCommandHandling::test_scheduled_agent_event_with_router_requester_survives_ingress_precheck \
2 passed
```

Os casos constroem um evento agendado enviado pelo agente e com Router como solicitante original. Ambos verificam que o solicitante Router sobrevive ao precheck; o primeiro também verifica `source_kind=SCHEDULED_FIRE` e entrada na política de dispatch sem cair no filtro de agente não mencionado. O teste usa configuração/runtime em memória e não reinicia processo nem prova persistência da identidade em retry. Nenhum provider ou ferramenta foi chamado. O primeiro comando falhou apenas por tentativa de usar classe pytest incorreta; corrigido o seletor, os dois corpos passaram. O checkout permaneceu sem alterações.

```text
MINDROOM_SCHEDULED_REQUESTER_PROPAGATION = PASS_WITH_SCOPE (2 EXISTING TESTS)
MINDROOM_SCHEDULED_IDENTITY_AFTER_HOST_CRASH_AND_RETRY = NOT_TESTED
MINDROOM_COMMON_ATENTO_RESTART_RETRY = BLOCKED_ADAPTER
MINDROOM_CANDIDATE_ELIMINATION = NONE
```

A inspeção adjacente do broker de ferramentas confirma casos de runtime de owner indisponível como falha temporária retryable e mudança de autoridade como negação; esses testes existentes não foram repetidos. O próximo gate falsificável continua sendo o teste comum de tarefa NAIA após claim/crash/restart/retry, condicionado a um seam de host Atento executável já existente. Não criar integração produtiva para abrir esse seam.


## Gate eliminatório com escopo — Ontheia perde retry de tarefa one-shot após claim — 2026-10-02

No pin `Ontheia/ontheia@70802db61eb16533f55efce3d8785d810223d03b`, executei um probe descartável contra o `CronService` compilado do próprio checkout. Um job sintético `run_at` vencido, associado a user/agent UUIDs sintéticos e com prompt inerte, passou pelo claim SQL real do componente: `UPDATE app.cron_jobs SET active = false ... RETURNING *`. No limite imediatamente após o claim e antes do ack terminal, substituí apenas a execução downstream por uma exceção que simula queda do host. Em seguida criei um segundo `CronService` sobre o mesmo banco falso em memória (pool transacional) e executei `rescheduleAll()`, que usa o SELECT de produção para jobs ativos.

```text
claimCommitted=true
executionAttempts=1
activeAfterRestart=false
restoredJobs=0
```

O resultado é coerente com o fluxo fonte: `checkRunAtJobs()` desativa atomicamente o job antes de agendar `_executeJob` fire-and-forget; o restart carrega apenas jobs `active=true`. Nenhum caminho restaura/rearma esse one-shot em falha ou interrupção depois do claim. O teste não mata um processo OS real nem usa PostgreSQL; reproduz o ponto de crash por exceção no componente compilado, mantendo o estado de claim compartilhado. Não houve provider ou ferramenta.

Classificação: `FAIL_WITH_SCOPE` para `ONTHEIA_RUN_AT_CLAIM_RESTART_RETRY`. A implementação one-shot atual não satisfaz retry após queda no intervalo claim/ack, violando o gate mínimo de recuperação para uma tarefa scheduled role-bound. Isso elimina o caminho nativo `run_at` deste pin para a composição que exige essa garantia; não elimina o repositório como possível componente com outro executor/adapter fail-closed e retry durável, ainda não presente ou testado. A repetição/recorrência baseada em cron não foi testada e não recebe a mesma conclusão.

```text
ONTHEIA_RUN_AT_RESTART_RETRY = FAIL_WITH_SCOPE
ONTHEIA_ONE_SHOT_NATIVE_PATH = ELIMINATED_FOR_RETRY_REQUIRED_COMPOSITION
ONTHEIA_CRON_RECURRENCE_RETRY = NOT_TESTED
ONTHEIA_REPOSITORY_FAMILY = NOT_ELIMINATED
PROVIDER_OR_TOOL_CALL = NONE
COMMON_ATENTO_HOST_GATE = BLOCKED_ADAPTER
FINAL_CANDIDATE_SELECTION = NONE
```

O próximo menor teste falsificável para um futuro executor alternativo é repetir o mesmo estado inerte em PostgreSQL isolado: persistir tarefa vencida, claim, terminar processo após claim e antes do terminal ack, reiniciar e demonstrar um retry com identidade do agente preservada e exatamente uma entrega terminal. Não alterar PR #58 nem construir integração produtiva apenas para esse teste.


## Meta-probe de identidade do chassi comum — MindRoom com três papéis — 2026-10-02

No pin mindroom-ai/mindroom@4f3bd2d108a6f9be28174e0f66d78eeecddca386, testei no mesmo usuário/sala sintéticos os identificadores NAIA, Anna e Apollo usando o resolvedor de worker do próprio pin em user_agent:

```text
roles = [naia, anna, apollo]
worker_keys = [
v1:default:user_agent:~@synthetic:localhost:naia,
v1:default:user_agent:~@synthetic:localhost:anna,
v1:default:user_agent:~@synthetic:localhost:apollo
]
all_distinct = true
```

A asserção de três chaves distintas passou. Nenhum provider foi configurado/chamado. Classificação PASS_WITH_SCOPE: comprova somente a partição produzida pelo resolvedor de identidade, não armazenamento persistente, execução em workers separados, tool/credential grants, handoff ou retry após restart; portanto não fecha nenhum SYS-* do Atento.

Uma extensão descartável tentou escrever três marcadores privados através do backend de arquivos e então comparar leitura/update/delete cruzados. A execução parou no primeiro add antes de produzir resultado/asserções; o processo foi interrompido após timeout curto de diagnóstico. Classificação BLOCKED_HARNESS, sem inferência de falha funcional. Os testes anteriormente registrados de facade cross-agent e requester propagation não foram repetidos.

```text
MINDROOM_THREE_ROLE_WORKER_KEY_PARTITION = PASS_WITH_SCOPE
MINDROOM_THREE_ROLE_PERSISTENT_MEMORY_BOUNDARY = BLOCKED_HARNESS (FIXTURE WRITE STALLED BEFORE ASSERTIONS)
MINDROOM_SYSTEM_CHASSIS_QUALIFIED = NO
ATENTO_COMMON_CHASSIS_ADAPTER = BLOCKED_ADAPTER
```

O menor reteste da propriedade de memória deve usar o teste existente tests/test_memory_backend_contract.py::test_agent_scope_memories_invisible_to_other_agents com configuração de três nomes de agente e fixture de arquivo sem iniciar atualização semântica/background; não repetir a suíte geral. Para qualificar o chassi comum, ainda é necessária a fronteira de runtime Atento que execute as três identidades e exponha estado/auditoria reais.


## Revalidação do gate de retry do chassi — 2026-10-02

A PR #58 continua aberta/draft no head `e948f344b91e20e655399b11300c439228d144ec`. A documentação do probe/restart da NAIA nessa PR descreve evidência limitada do pin NanoClaw; não adiciona host runtime/gateway de produto Atento. A continuidade do MindRoom no snapshot da PR #59 também declara o host/runtime ausente e mantém o gate bloqueado. Na árvore atual desta branch descartável (`34e99e3347a43bc282bf2c5dd0ea79501d94448d`), os caminhos runtime/gateway encontrados são harnesses/adapters de probe; não existe caminho executável do host de produto para agendar, claimar e recuperar trabalho através de restart.

Não foi executado novo teste: sem esse seam, um fixture ou adapter inventado provaria apenas o harness. Classificação atual:

```text
NAIA_HOST_PROCESS_TASK_RETRY_AFTER_RESTART = BLOCKED_ADAPTER
MINDROOM_ATENTO_HOST_RESTART_RETRY = BLOCKED_ADAPTER
PRODUCTION_HOST_RUNTIME_OR_PROVIDER_CALL = NONE
PR_58_MODIFIED = NO
```

Pré-condições para um único probe descartável: host Atento executável com estado durável reutilizável e observabilidade de claim/ack terminal; identidade confiável da NAIA mapeada para worker isolado `user_agent`; identidades sintéticas Anna/Apollo como controles negativos; tarefa vencida inerte; provider ausente; capacidade de encerrar diretamente o processo host após claim e antes do ack; e observabilidade do retry e das entregas terminais.

Quando tudo existir, executar sequencialmente uma vez: persistir uma tarefa vencida da NAIA, iniciar e observar o claim, encerrar o host antes do ack terminal, reiniciar com o mesmo store e permitir exatamente um retry. PASS_WITH_SCOPE somente se a tarefa continuar NAIA-owned no mesmo escopo, não acessar estado de Anna/Apollo e produzir exatamente uma entrega terminal. Drift de identidade, leitura cruzada ou entrega duplicada com harness válido é FAIL do seam/configuração. Wrapper morto em vez do host, falta de prova pre-ack, store diferente ou retry não observável é INVALID/HARNESS. Enquanto faltar a chamada de produto, manter BLOCKED_ADAPTER; não implementar integração produtiva apenas para abrir este teste.

Reutilizar sem repetir: testes upstream de claims/orphans, delivery-attempt persistence, recurrence/backoff e mailbox re-armament já citados nos documentos anteriores; o replay REST+SSE aprovado e os probes 7/7 também permanecem fora desta execução. Não rodar tarefas paralelas.


## Gate comum: visibilidade de estado privado entre agentes — 2026-10-02

### Contrato comparável

A asserção comum deste bloco: no mesmo usuário/sala sintéticos, o agente A grava uma sentinela privada em seu escopo persistente; A consegue recuperá-la; o agente B não a lista nem recupera. Sem provider/modelo e sem efeitos externos. Evidência de arquivos/workspace, memória semântica e namespaces é mapeada para este contrato somente com limite explícito. Teste de configuração, mock ou path guard não equivale a execução do armazenamento de produção.

### Resultados congelados e probes deste bloco

| Candidato/pin | Evidência reutilizada ou probe focado | Resultado para o gate comum | Limite que permanece |
|---|---|---|---|
| NanoClaw 4c1eabd3ddd74cc3d71b1871da857391a9411c8d | Run Atento 36815873223, 7/7 assertions: mounts/group-state selecionados, propriedade DB/sessão e negação cross-group, entre outros. | PASS_WITH_SCOPE — role/group/state ownership | Não é o teste de sentinela NAIA-versus-Anna em memória persistente; não repetir o run 7/7. NanoClaw é base provisória da NAIA, não prova do chassi dos três. |
| OpenClaw e9571d77e76bd6d35996273d9e8398ad539b26e1 | Nenhum probe comparável de sentinela persistente registrado neste bloco; o teste de runner seguro em outro gate parou antes do corpo por `BLOCKED_ENVIRONMENT/HARNESS`. | NOT_TESTED / UNRESOLVED — permanece elegível no fixed system cohort de 11 | A exclusão por product fit vale só para a visão mobile; não remove OpenClaw da comparação do chassi completo. SYS-MEM Atento segue `BLOCKED_ADAPTER`. |
| AI Butler c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c | Reusar o bloqueio de segurança registrado para o pin atual. | BLOCK_CURRENT_PIN_SECURITY; gate de memória não avançado | Não executar mais testes neste pin sem correção e requalificação de segurança. Não contar como falha de memória. |
| QwenPaw 777441721aa72db8e380d90e4d0481b05cbfd4cc | Teste upstream test_workspace_files_isolated_across_agents passou 1/1. Probes descartáveis na API local: A escreveu/recuperou arquivo de memória sintético; listing de B não mostrou a sentinela e GET direto de B ao mesmo caminho retornou 404. | PASS_WITH_SCOPE — API de memória entre dois agentes, incluindo leitura direta | Não prova contenção contra acesso absoluto ao filesystem nem composição Atento. Probe de listing passou 1/1 em 16,50 s; probe de GET direto passou 1/1 em 16,60 s. Tentativa inicial bloqueada pelo sandbox ao abrir socket; com loopback autorizado passou. Falha de harness, não do pin. |
| MindRoom 4f3bd2d108a6f9be28174e0f66d78eeecddca386 | Reutilizar os três casos de facade cross-agent mock-based já aprovados; meta-probe de três chaves user_agent distintas já registrado. | PASS_WITH_SCOPE — facade mock/key partition; memória persistente de três papéis BLOCKED_HARNESS | Tentativa de fixture real parou no primeiro add antes de assertions. MindRoom fica pausado neste gate até a coorte alcançá-lo; não repetir aqui. |
| Bob Labs a91d6dad098c8ba6d24436a856556078151db45d | Reutilizar a tentativa focada registrada de sandbox HMAC, que parou antes da coleta por pytest indisponível. | BLOCKED_HARNESS | Nenhum resultado funcional de memória pode ser inferido. Não repetir sem mudança do runner. |
| Ontheia 70802db61eb16533f55efce3d8785d810223d03b | Reutilizar os dois testes de namespace anteriores; probe novo do helper agent_id produziu três namespaces distintos e negou as seis leituras cruzadas. | PASS_WITH_SCOPE — policy namespace configurável por papel | Helper de autorização apenas; namespace default segue user-keyed e não houve backend de memória, RLS ou execução de agente. |
| OpenAkita 5f5b38da728274f0fd06461a481851be7c0bca6a | Suíte focada existente: test_isolated_memory_rebinds_full_chain_and_cannot_read_global, test_create_agent_can_enable_isolated_memory, test_spawn_agent_inherits_isolated_memory: 3 passed. Probe descartável com dois perfis memory_mode=isolated: NAIA recuperou sua sentinela user-scoped e Anna não a recuperou; 1 passed em 0,76 s. | PASS_WITH_SCOPE — perfis de agente e stores privados isolados | Dois objetos/agentes no mesmo processo e bancos temporários; sem host real ou worker de produção. Primeira tentativa usou ranking de injeção como oráculo e não encontrou a sentinela; classificada inválida. O probe corrigido usou busca escopada determinística e passou. |
| Clawix 5aee015e0bd793102fba69af486dd6e75df6d802 | Reutilizar os 2 guards de traversal/outside-workspace já aprovados; não repetir. | PARTIAL — path guard | Harness de runner/path; não comprova sentinela privada isolada entre dois agentes nem autorização sobre memória persistente. |
| Memoh | Sem pin exato aceito no registro (PIN_REQUIRED). | NOT_TESTED / PIN_REQUIRED | Não executar contra branch flutuante nem tratar ausência de resultado como zero/falha. |
| Letta Code 21daa38a8cdd74f2d03b634c8312253080bacfc1 | Reusar o bloqueio de execução anterior: Bun indisponível no executor para seus testes de confinamento MemFS. | BLOCKED_HARNESS | Sem conclusão funcional neste gate; só retomar se Bun/runner exato ficar disponível. |

Correção de escopo: OpenClaw permanece na coorte sistêmica fixa de 11; sua exclusão por product fit vale apenas para a visão mobile. A linha acima registra SYS-MEM como `NOT_TESTED/UNRESOLVED`, sem inferir falha nem removê-lo da comparação. O perfil de segurança bloqueado do QwenPaw e o bloqueio de segurança do AI Butler continuam separados deste resultado de memória.

### Evidência bruta dos testes novos

QwenPaw:
- Comando: .venv/bin/pytest -q tests/integration/test_spike_cross_agent_memory_visibility.py
- Resultado: 1 passed in 16.50s.
- API local; dois agentes sintéticos; provider ausente; arquivo temporário removido após execução.

OpenAkita:
- Comando: .venv/bin/pytest --no-cov -q tests/unit/test_spike_cross_agent_memory_visibility.py
- Resultado: 1 passed in 0.76s.
- Busca direta em scope=user; dois perfis isolados; banco temporário; provider ausente; arquivo temporário removido.
- A execução inicial com get_injection_context foi INVALID_ORACLE (ranking/relevância), não FAIL do candidato.

Ontheia:
- Comando: node --test --test-name-pattern='isNamespaceAllowed resolves placeholders and wildcard suffixes' host/dist/memory/namespaces.spec.js
- Resultado: 1 passed; a negação é contra user_id externo, não contra outro papel no mesmo user.

O pytest -n 0 inicial do OpenAkita também foi erro de invocação (plugin xdist ausente); a chamada serial correta executou 3/3. Arquivos descartáveis de QwenPaw e OpenAkita foram removidos e ambos os checkouts voltaram limpos aos pins congelados. Não houve chamada de provider/modelo.

### Denominador comum deste bloco

SENTINEL_CROSS_ROLE_GATE = DEFINED
DIRECT_CANDIDATE_SCOPED_PASSES = [QwenPaw_API_SCOPE, OpenAkita_ISOLATED_PROFILE_SCOPE]
PARTIAL_OR_MOCK_ONLY = [NanoClaw_ROLE_GROUP_STATE, MindRoom_MOCK_FACADE, Ontheia_USER_NAMESPACE, Clawix_PATH_GUARD]
BLOCKED_OR_PIN_REQUIRED = [AI_Butler_SECURITY, BobLabs_HARNESS, LettaCode_HARNESS, Memoh_PIN]
FULL_ATENTO_COMPOSITION_PASSES = 0
CANDIDATES_ELIMINATED_BY_THIS_BLOCK = 0
MINDROOM_RESUMED = NO
BENCHMARKS_RERUN = 0

Os dois passes diretos têm configurações diferentes e continuam PASS_WITH_SCOPE; não formam ranking geral nem qualificação Atento. Resultados externos já publicados permanecem no registro benchmark-específico e não foram repetidos nem agregados a este gate. O próximo bloco comparável deve avançar a mesma sentinela para candidatos parcialmente cobertos que tenham pin/runner e escopo executável; MindRoom só retoma depois desse catch-up.


## Gate comum: autoridade de ferramentas por agente — 2026-10-02

### Contrato

Um toolset atribuído a A não deve vazar para B; uma política negada deve impedir registro/execução; grants seletivos devem manter só as ferramentas explicitamente autorizadas e as funções de controle independentes. Os probes aqui são de configuração/registro, sem chamada externa ou provider. Eles não substituem a assertion sistêmica de tentar executar uma ferramenta exclusiva do papel vizinho através do host Atento.

### Evidência executada ou reutilizada

| Candidato/pin | Evidência | Resultado | Limite |
|---|---|---|---|
| NanoClaw 4c1eabd3ddd74cc3d71b1871da857391a9411c8d | Reusar o 7/7 de 36815873223: A2A nativo sem grant negado, envelope broker/mailbox tipado e ação reautorizada no receptor. | PASS_WITH_SCOPE — mediação de handoff/autoridade | Adapter de teste, não host/provedor de produto; não repetir o 7/7. |
| AI Butler c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c | Bloqueio de segurança do pin atual. | BLOCK_CURRENT_PIN_SECURITY | Não avançar autoridade no pin sem correção/requalificação; não é falha deste gate. |
| QwenPaw 777441721aa72db8e380d90e4d0481b05cbfd4cc | test_tools_toggle_isolated_with_full_cycle: desabilitar ferramenta no agente A não altera B; reabilitação em A foi observada. | PASS_WITH_SCOPE — configuração API isolada (1 pass, 15,90 s) | Não invocou a ferramenta; nenhuma execução real/credential grant foi tentada. Requereu somente servidor loopback local. |
| MindRoom 4f3bd2d108a6f9be28174e0f66d78eeecddca386 | Reutilizar os dois testes focados já executados: header do requester não define identidade de execução e /v1 rejeita worker_scope=user_agent. | API OpenAI-compatible padrão não é seam de execução por papel neste pin. | Evidência já coberta; não repetir. A ADR mantém host adapter/recovery BLOCKED_ADAPTER. MindRoom segue pausado até catch-up da coorte. |
| OpenAkita 5f5b38da728274f0fd06461a481851be7c0bca6a | test_tool_inclusive_empty_keeps_only_independent_basics_when_extensions_empty e test_tool_inclusive_preserves_mcp_gateway_when_mcp_servers_are_selected: 2 passed. | PASS_WITH_SCOPE — filtro por profile e retenção condicional do gateway MCP | Unit tests de construção do toolset; não invocam tools nem provam contenção entre workers/processos. |
| Ontheia 70802db61eb16533f55efce3d8785d810223d03b | filterRunTools em host/dist/routes/mcp-utils.spec.js com padrões para “skills write tools stay out unless explicitly bound” e “scheduled runs never see create_schedule”: relatório Node, 1 pass para o módulo selecionado. | PASS_WITH_SCOPE — filtro de ferramenta por binding e restrição de schedule | Contrato de montagem do toolset; não é chamada real, credencial ou operação externa. |
| Clawix 5aee015e0bd793102fba69af486dd6e75df6d802 | Probe de autorização MCP no agent-runner.service.test.ts parou antes da coleta: import de ../generated/prisma/client.js ausente. | BLOCKED_HARNESS | Nenhum teste executou; não inferir falha do candidato. Geração Prisma não foi feita neste bloco. |
| Bob Labs a91d6dad098c8ba6d24436a856556078151db45d | Reutilizar bloqueio já registrado: pytest indisponível na tentativa de auditoria de sandbox HMAC. | BLOCKED_HARNESS | Sem resultado de autoridade por papel. |
| Letta Code 21daa38a8cdd74f2d03b634c8312253080bacfc1 | Runner Bun permanece indisponível para os testes de policy/MemFS. | BLOCKED_HARNESS | Sem inferência funcional. |
| Memoh | Pin exato segue PIN_REQUIRED. | NOT_TESTED / PIN_REQUIRED | Não executar branch móvel. |

OpenClaw continua fora da coorte ativa por decisão de product fit. Nenhum resultado deste bloco elimina candidato.

### Evidência bruta

QwenPaw:
- Comando: .venv/bin/pytest -q tests/integration/test_multi_agent_config_isolation.py::test_tools_toggle_isolated_with_full_cycle
- Resultado: 1 passed in 15.90s.
- Agentes e servidor locais sintéticos; nenhuma ferramenta foi invocada; provider ausente.

OpenAkita:
- Comando: .venv/bin/pytest --no-cov -q tests/unit/test_agent_factory_skill_filter.py::test_tool_inclusive_empty_keeps_only_independent_basics_when_extensions_empty tests/unit/test_agent_factory_skill_filter.py::test_tool_inclusive_preserves_mcp_gateway_when_mcp_servers_are_selected
- Resultado: 2 passed in 0.89s.

Ontheia:
- Comando: node --test --test-name-pattern='skills write tools stay out unless explicitly bound|scheduled runs never see create_schedule' host/dist/routes/mcp-utils.spec.js
- Resultado literal: tests 1, pass 1, fail 0; sem tool/provider externo.

Clawix:
- Comando: ./node_modules/.bin/vitest run packages/api/src/engine/__tests__/agent-runner.service.test.ts -t '<two MCP policy cases>'
- Resultado: falha de setup/coleta antes de testes por generated Prisma Client ausente; classificado BLOCKED_HARNESS.

### Resultado do subgate

TOOL_AUTHORITY_PER_AGENT = PARTIAL_PASS_WITH_SCOPE
DIRECT_POLICY_OR_TOOLSET_CHECKS = [QwenPaw_API_TOGGLE, OpenAkita_PROFILE_FILTER, Ontheia_BINDING_FILTER]
REUSED_ATENTO_BROKER_EVIDENCE = NanoClaw 7/7 (bounded adapter scope)
INTEGRATED_ATENTO_CROSS_ROLE_TOOL_EXECUTION = NOT_RUN
CANDIDATES_ELIMINATED = 0
BENCHMARKS_RERUN = 0
PROVIDER_OR_EXTERNAL_TOOL_CALLS = 0

Os três resultados novos têm test harnesses/semânticas diferentes e ficam lado a lado; não viram um rank numérico agregado. Scores externos já publicados permanecem reutilizados em suas próprias métricas. A próxima prova comum pendente é execução negativa cruzada de uma ferramenta exclusiva do papel B via o host Atento. Só executar quando o host/adapter de produto ou um seam já existente torná-la observável; não inventar integração de produção para abrir o gate.


## Gate comum: custódia e não exposição de credenciais — 2026-10-02

### Contrato

O contrato final exigido é por papel: credencial/provider grant atribuída a A não pode ser enumerada, injetada no contexto nem usada por B; credencial ausente ou não autorizada deve falhar fechado; logs/config exports não devem revelar o segredo. Os testes abaixo cobrem somente propriedades de componentes/configuração. Nenhum usou credencial real ou chamou provider.

### Evidência dos pins ativos

| Candidato/pin | Evidência deste bloco ou já registrada | Resultado com escopo | Lacuna que impede o denominador de papel |
|---|---|---|---|
| NanoClaw 4c1eabd3ddd74cc3d71b1871da857391a9411c8d | Os 7/7 checks hosted usam tokens/identidades sintéticas e provam boundaries selecionadas de group/session e broker. | PASS_WITH_SCOPE — limites do profile de teste | Nenhuma custódia de credenciais de provider/gateway do Atento foi exercitada; não repetir o 7/7. |
| AI Butler c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c | Reusar o bloqueio de segurança do pin atual. | BLOCK_CURRENT_PIN_SECURITY | Não avançar no pin sem correção e requalificação; não é falha deste gate. |
| QwenPaw 777441721aa72db8e380d90e4d0481b05cbfd4cc | Dois testes existentes em tests/unit/agents/test_model_provider_isolation.py: sem escolha explícita não escolhe modelo; seleção pessoal usa o provider pessoal, e não o fallback gerenciado. | PASS_WITH_SCOPE — seleção sintética de provider (2 passed, 0,49 s) | Usou mocks e token sintético; não comparou dois papéis com credenciais distintas nem inspecionou request/provider real. |
| MindRoom 4f3bd2d108a6f9be28174e0f66d78eeecddca386 | Testes de identidade API já registrados não configuram nem chamam provider. | NOT_TESTED | Sem host/gateway de produto e fonte confiável de credenciais por papel. Não repetir probes anteriores. |
| Bob Labs a91d6dad098c8ba6d24436a856556078151db45d | Teste existente test_cso_2026_06_sandbox_hmac.py executado sem o conftest de serviços externos: assinatura vinculada ao body, timestamp/nonce, verificador-fake e guards de source para SANDBOX_LAB_ID/HMAC: 21 passed. | PASS_WITH_SCOPE — isolamento de chamadas control-plane→sandbox por Lab | Não iniciou sandbox/container nem executou middleware real. Rodou com Python/pytest do venv local QwenPaw porque o executor base não tem pytest; deps não usadas na prova foram evitadas com --confcutdir. Não é credencial provider do Atento. |
| Ontheia 70802db61eb16533f55efce3d8785d810223d03b | Teste resolveEnvMap: secret: is resolved, masked and reported missing when unset passou 1/1; segredo ausente não entra em resolved e valor presente fica mascarado. | PASS_WITH_SCOPE — referência de segredo e masking | Não mostra separação de keys entre NAIA/Anna/Apollo nem policy de role no runtime. |
| OpenAkita 5f5b38da728274f0fd06461a481851be7c0bca6a | test_feedback_sanitized_config_redacts_runtime_state_bot_credentials passou 1/1. | PASS_WITH_SCOPE — redaction de app_secret em export diagnóstico | Não prova isolamento de provider ou secret store entre perfis/agentes. |
| Clawix 5aee015e0bd793102fba69af486dd6e75df6d802 | A tentativa anterior dos testes de binding MCP não coletou por Prisma Client gerado ausente. | BLOCKED_HARNESS | Sem execução de policy/bindings por agente; não inferir vazamento nem isolamento. |
| Letta Code 21daa38a8cdd74f2d03b634c8312253080bacfc1 | Bun ausente para execução dos testes de MemFS/policy. | BLOCKED_HARNESS | Sem resultado deste gate. |
| Memoh | Exact pin continua PIN_REQUIRED. | NOT_TESTED / PIN_REQUIRED | Não executar em branch móvel. |

OpenClaw continua excluído da coorte ativa por product fit. Bloqueios do AI Butler e do runner não contam como falha funcional de credenciais.

### Evidência bruta

QwenPaw:
- Comando: .venv/bin/pytest -q tests/unit/agents/test_model_provider_isolation.py::test_hub_does_not_choose_a_model_without_user_selection tests/unit/agents/test_model_provider_isolation.py::test_personal_model_uses_personal_provider_in_hub
- Resultado: 2 passed in 0.49s; modelos/provider foram mockados; sem chamada HTTP.

Bob Labs:
- Comando: PYTHONPATH=control-plane <qwenpaw-pin>/.venv/bin/pytest --confcutdir=control-plane/tests/regression -q control-plane/tests/regression/test_cso_2026_06_sandbox_hmac.py
- Resultado: 21 passed, 1 warning em 0.22s.
- Sem container ou socket; warning apenas de depreciação Pydantic. A primeira chamada carregou conftest Bob e parou antes da coleta por SQLAlchemy ausente; confcutdir retirou esse conftest e o arquivo não requer fixtures próprias além do monkeypatch padrão. Manter a diferença do ambiente registrada.

Ontheia:
- Comando: node --test --test-name-pattern='resolveEnvMap: secret: is resolved, masked and reported missing when unset' host/dist/secrets/resolver.spec.js
- Resultado: tests 1, pass 1, fail 0.

OpenAkita:
- Comando: .venv/bin/pytest --no-cov -q tests/unit/test_feedback_sanitized_config.py::test_sanitized_config_redacts_runtime_state_bot_credentials
- Resultado: 1 passed em 0,40 s.

### Resultado do gate

ROLE_LEVEL_PROVIDER_CREDENTIAL_CUSTODY = NOT_ESTABLISHED
COMPONENT_SECRET_HANDLING = PARTIAL_PASS_WITH_SCOPE
ATENTO_ROLE_TO_PROVIDER_CREDENTIAL_COMPOSITION = NOT_RUN
REAL_PROVIDER_CALLS = 0
REAL_SECRETS_USED = 0
CANDIDATES_ELIMINATED = 0
BENCHMARKS_RERUN = 0

O denominador comum ainda não foi alcançado para isolamento de credenciais por papel: não existe host Atento executável que aceite grants sintéticos separados para A/B e permita observar o conteúdo efetivamente entregue ao provider. Manter esse gate pendente; não adicionar gateway/integração produtiva só para fabricar um teste. Os números de benchmark externos permanecem como evidência separada, sem rerun nem média cruzada.


## Consolidação da coorte nos gates já percorridos — 2026-10-02

Esta tabela fecha o denominador de evidência para os três gates de isolamento que acabamos de avançar. Cada célula é classificada pelo escopo efetivamente observado; BLOCKED, PARTIAL e NOT_TESTED não são zero nem falha do candidato.

| Candidato ativo | Memória/estado privado | Autoridade de tools | Credenciais/provider | Recovery e retry Atento |
|---|---|---|---|---|
| NanoClaw | 7/7 Atento prova group/state e propriedade com escopo; sem marcador direto NAIA↔Anna | 7/7 nega A2A sem grant e demonstra caminho brokerado limitado | Só identidades/tokens sintéticos; custódia de provider não provada | BLOCKED_ADAPTER para tarefa host após restart |
| AI Butler | Gate não avançado | Gate não avançado | Gate não avançado | Pin atual bloqueado por security scan |
| QwenPaw | PASS_WITH_SCOPE: A grava/recupera; listing de B omite e GET direto de B ao mesmo path retorna 404 | PASS_WITH_SCOPE: toggle de tool em A não muda B | PASS_WITH_SCOPE: seleção personal provider mockada, sem chamada HTTP | HOLD por perfil fail-closed/cron; integração Atento não provada |
| MindRoom | Mock facade cross-agent e chaves user_agent passam; backend persistente três papéis BLOCKED_HARNESS | API /v1 padrão não executa com user_agent; não confiar requester header | Sem prova | BLOCKED_ADAPTER; MindRoom permanece pausado até catch-up |
| Bob Labs | BLOCKED_HARNESS anterior | Não avançado | PASS_WITH_SCOPE: 21 HMAC/lab-binding tests de componente, sem middleware/container real | Sem integração Atento executada |
| Ontheia | PASS_WITH_SCOPE: agent_id policy template cria 3 namespaces distintos e nega cruzamento no helper; default continua user-keyed, sem prova de storage | PASS_WITH_SCOPE para tool filtering via binding | PASS_WITH_SCOPE: segredo ausente excluído e valores mascarados | FAIL_WITH_SCOPE no run_at one-shot após post-claim failure; família não eliminada |
| OpenAkita | PASS_WITH_SCOPE: dois perfis isolados; A recupera, B não | PASS_WITH_SCOPE: filtros de ferramentas por profile | PASS_WITH_SCOPE: redaction no export diagnóstico | Risco já registrado no scheduler quando perfil é desconhecido; composição Atento ausente |
| Clawix | PARTIAL: path guards, sem sentinela entre papéis | BLOCKED_HARNESS: Prisma Client ausente antes da coleta | Não demonstrada | Sem restart/retry Atento |
| Memoh | PIN_REQUIRED | PIN_REQUIRED | PIN_REQUIRED | PIN_REQUIRED |
| Letta Code | Runner Bun ausente para provas MemFS | Runner Bun ausente | Runner Bun ausente | Sem composição Atento |

### Pontuações externas existentes reutilizadas

Esses números são mantidos como eixos de qualidade funcional por protocolo original; não foram rerodados nem convertidos em score de isolamento, credenciais ou recovery.

| Benchmark já publicado | Resultados que entram na comparação | Regra de uso |
|---|---|---|
| Auto-ClawEval v4 / Claude Haiku 4.5 | NanoClaw 63,7 full / 67,8 Mini; CoPaw→QwenPaw lineage 60,8 full / 59,3 Mini | Comparação direta só dentro desse benchmark/config histórico. |
| PawBench v1.0 / 150 tasks | OpenClaw 72,1; QwenPaw 73,7 (harness means over the same 9-model matrix; published harness versions OpenClaw v2026.4.24 and QwenPaw v1.1.3) | Same-benchmark signal: QwenPaw +1.6 points in this published release/configuration. Not the frozen Atento pins; do not combine with Auto-ClawEval. [Official leaderboard](https://agentscope-ai.github.io/PawBench/en/). |
| Terminal-Bench 2.0 | Letta Code 59,1% ±2,4 com Claude Opus 4.5; 53,5% ±2,8 com GPT-5.1-Codex | Duas configurações do próprio benchmark; não comparável diretamente com pontuações de agentes pessoais. |
| AI Butler internal live eval | 4/7 no registro do pin | Evidência first-party; eixo separado de resultados externos. |

Os detalhes e provenance permanecem nos registros de cobertura/ranking de benchmark de 2026-10-01. Ausência de linha para outros candidatos não equivale a nota zero.

### Ponto de convergência

ACTIVE_COHORT = 10
CANDIDATE_FULL_THREE_ROLE_PASSES = 0
DIRECT_MEMORY_MARKER_PASSES = [QwenPaw_API_SCOPE, OpenAkita_ISOLATED_PROFILE_SCOPE]
TOOL_CONFIG_OR_BINDING_PASSES = [QwenPaw, OpenAkita, Ontheia]
ROLE_LEVEL_PROVIDER_CREDENTIAL_CUSTODY = NOT_ESTABLISHED_FOR_ALL
NAIA_HOST_RESTART_RETRY = BLOCKED_ADAPTER
MINDROOM_REMAINS_PAUSED = YES
EXTERNAL_BENCHMARKS_RERUN = 0
CROSS_BENCHMARK_AGGREGATE_SCORE = NOT_CREATED
CANDIDATE_ELIMINATIONS_FROM_MISSING_EVIDENCE = 0

O denominador comparável já está definido como três negações (sentinela/memória privada, tool exclusiva e credential/provider de outro papel) mais preservação de propriedade sob restart/retry, sempre no mesmo perfil de papéis. A evidência direta ainda não cobre todos os candidatos nem uma composição Atento; por isso não há rank sistêmico ou qualificação. O próximo delta com maior poder decisório é a tool exclusiva de B negada quando requisitada por A através de um host/adapter executável. Se esse seam continuar ausente, manter os casos como bloqueados no nível Atento, usar os scores externos existentes apenas no eixo deles e não repetir suites/benchmarks.


## Addendum — namespace por papel configurado no Ontheia — 2026-10-02

Executado uma vez no helper compilado do pin 70802db61eb16533f55efce3d8785d810223d03b: usar a policy vector.agent.${agent_id}.private para NAIA, Anna e Apollo no mesmo user sintético produziu três namespaces distintos; cada papel foi aceito no próprio namespace e seis tentativas para os outros dois foram negadas. Resultado PASS_WITH_SCOPE para template explícito de role; o namespace padrão continua baseado em user_id e o probe não tocou backend vetorial, PostgreSQL/RLS nem runtime de agente.

Comando: node --input-type=module -e '<resolver/isNamespaceAllowed probe for three roles>'
Saída observada: configured_role_namespaces=[vector.agent.naia.private, vector.agent.anna.private, vector.agent.apollo.private], all_distinct=true, cross_role_denied=true, default_namespaces=[vector.agent.synthetic-user.memory, vector.user.synthetic-user.memory], default_is_role_specific=false.

Isso melhora a evidência configurável de Ontheia, mas não aumenta DIRECT_MEMORY_MARKER_PASSES: nenhum texto privado foi gravado/consultado no backend e a invisibilidade persistente não foi testada.


## Addendum — leitura direta de memória no QwenPaw — 2026-10-02

Para fechar a lacuna deixada pelo teste de listagem, executei um segundo probe descartável, sem repetir aquela assertion: após A gravar e recuperar um arquivo de memória sintético, B tentou GET do mesmo caminho relativo via API. Resultado: 404 para B; 1 pass em 16,60 s. Servidor local, dois agentes sintéticos, sem provider; arquivo de teste removido e checkout voltou limpo ao pin.

Comando: .venv/bin/pytest -q tests/integration/test_spike_cross_agent_memory_direct_read.py
Classificação: PASS_WITH_SCOPE para isolamento de API memory-file entre dois agentes. Não prova leitura por caminho absoluto/processo, store criptograficamente separado ou composição Atento.


## Supplemental top-three common memory gate — 2026-10-02

PR #58's supplemental horizon record names a separate cost-first probe order: Open Pincery, OpenLegion, then Moltis. These are additions to the evaluation horizon, not replacements for the 11-slot cohort above. Their published benchmark and CI evidence is reused; no benchmark or broad upstream suite was rerun here.

The shared eliminatory property for this block is the private-state negative: write one synthetic marker into role B's private memory/state, attempt to read it as role A through the candidate's normal scoped API/tool, require denial with no marker bytes, and confirm role B still reads it. No provider, model, or real tool is needed. A component's own workspace/agent identity is not automatically equivalent to an Atento role identity; record the mapping and scope.

| Order | Frozen candidate pin | Closest identified seam | Outcome |
|---:|---|---|---|
| 1 | Open Pincery — RCSnyder/open-pincery@fc33211c7b04e1a958a340c369cb635f018c13f4 | Existing tests/api_test.rs::test_agent_routes_are_scoped_to_workspace checks authenticated cross-workspace agent API denial. Its fixture calls common::test_pool(), which requires an isolated PostgreSQL test database and runs migrations/truncation. This workspace has no TEST_DATABASE_URL, PostgreSQL client/server, Docker, or Podman. Test body not started: BLOCKED_ENVIRONMENT. The property is workspace API isolation, not a direct role-private-memory read. | Not equivalent result |
| 2 | OpenLegion — openlegion-ai/openlegion@24efd6e06b28768cbbcd9275f43c479b3df37b18 | Closest existing denial is tests/test_agent_goals_endpoint.py::test_agent_cannot_read_peer_goals; it concerns peer standing-goal state, not private memory. The normal pytest invocation produced no collection/result; the focused invocation with plugin autoload disabled and the repository conftest cut off also remained silent and was interrupted after the bounded wait (exit 130). The pin has no uv.lock; dependencies are ranges in pyproject.toml, so the alternate runner's dependency parity was not established. BLOCKED_HARNESS, no test result. | Not equivalent result |
| 3 | Moltis — moltis-org/moltis@1f6d28ea750d6654d52d5899b8be67727ebf7a19 | Source exposes is_path_in_agent_memory_scope and agent-scoped memory tools. No existing test in crates/chat/src/memory_tools/tests.rs directly asserts cross-role private-path denial. A disposable five-assertion helper probe was drafted then removed before execution; cargo is absent. BLOCKED_ENVIRONMENT, no test result. | Not executed |

```text
SUPPLEMENTAL_TOP3_PINS_VERIFIED = 3_OF_3
COMMON_PRIVATE_STATE_ASSERTION_EXECUTED = 0_OF_3
OPEN_PINCERY = BLOCKED_ENVIRONMENT (ISOLATED_POSTGRES_ABSENT)
OPENLEGION = BLOCKED_HARNESS (NO_COLLECTED_TEST_RESULT; EXIT_130_AFTER_INTERRUPT)
MOLTIS = BLOCKED_ENVIRONMENT (CARGO_ABSENT; TEMP_PROBE_NOT_EXECUTED)
NEW_CANDIDATE_FAILURES = 0
COMMON_ATENTO_HOST_GATE = BLOCKED_ADAPTER
BENCHMARKS_RERUN = 0
```

The smallest falsifiable candidate-level probe is the same marker read-denial above, adapted only at the published test seam: run Pincery's scoped API test with a fresh isolated PostgreSQL database; run OpenLegion's existing authenticated peer-state denial test in a stable, exact recorded Python environment and separately add no test unless the private-memory surface can be reached; run Moltis's agent-scoped memory search/get path with two synthetic agent IDs and assert the other role's marker is filtered. These component probes can narrow candidate evidence but cannot substitute for the Atento composition test.

The smallest falsifiable common Atento test remains: after an executable Atento host seam exists, assign two synthetic role identities, write a private marker for B, request it as A through the actual role-bound API/tool, assert denial and no marker in response/traces, then verify B's positive read. Do not create a production adapter just to unlock this gate. Until candidate-specific harness prerequisites and the common host seam are available, all three remain unresolved on this property; no comparative score or elimination is supported.

No candidate checkout was left modified. PR #58 was inspected at e948f344b91e20e655399b11300c439228d144ec and not changed. This addendum is only on the disposable branch.

## Supplemental alternates — private memory marker gate — 2026-10-02

After the supplemental top-three candidates could not reach an equivalent test in this runner, two alternates were probed in the documented order. The same bounded property was used: store a synthetic private marker under role B's identifier; ensure role A cannot retrieve it and role B can; no provider or model call.

| Candidate / pin | Result | Scope and limits |
|---|---|---|
| HybridClaw — HybridAIOne/hybridclaw@b9378588f9f9666355fc5431a7b1f5292aaa93c0 | PASS_WITH_SCOPE — one disposable test, two assertions. After the exact pin's npm-shrinkwrap dependencies were installed with Node 22 / npm 11.10.0, production setMemoryValue/getMemoryValue used a real temporary SQLite database. The Anna-keyed marker was returned for Anna and null for NAIA. | The API parameter is a synthetic key stored in kv_store.agent_id; this did not run a HostExecutor turn or prove Atento role identity is bound to that key. The first test attempt failed before assertions because better-sqlite3 had Node 24 ABI; after rebuilding that native dependency under Node 22, the single probe passed. Temporary test removed. |
| Hivekeep — MarlBurroW/hivekeep@7d023c952e46861070683825ff545daf981910f0 | PASS_WITH_SCOPE — one disposable test, three assertions. With Bun 1.3.13 from the exact-pin CI and frozen bun.lock dependencies, real temporary SQLite migrations/schema and production memory service listMemories/getMemory were used. Anna listed only Anna's row, could not fetch NAIA's row, and could fetch her own. | Synthetic agent IDs; rows were inserted directly through Drizzle, no provider/model/runtime or external API authorization. This is a service/storage boundary, not Atento integration. Temporary test and DB removed. The existing memory.test.ts private-filter example reimplements a filter over arrays and was not counted or rerun. |
| OpenVole — openvole/openvole@c8b405f4933a5ee0a1cb7725cf4c8a31cd24d732 | NOT_RUN for this memory gate. | The closest existing scoped-file tests bind project IDs, not persistent agent/role identity. Counting their pass as cross-role memory evidence would change the assertion. No test was run. |

```text
HYBRIDCLAW_PRIVATE_KV_KEY_ISOLATION = PASS_WITH_SCOPE
HIVEKEEP_PRIVATE_MEMORY_SERVICE_ISOLATION = PASS_WITH_SCOPE
OPENVOLE_ROLE_PRIVATE_MEMORY_ASSERTION = OPEN
COMMON_ATENTO_SYS_MEM_01 = BLOCKED_ADAPTER
NEW_SYSTEM_CANDIDATE_ELIMINATIONS = 0
BENCHMARKS_RERUN = 0
```

These two passes establish scoped component behavior only. They do not close SYS-MEM-01 for a complete Atento composition: the host must bind NAIA/Anna/Apollo identity to each candidate's private key/path and prove denial through the actual role-bound runtime. MindRoom remains paused as directed until comparable component gates have been applied to the active alternatives; NanoClaw's previously approved tests and benchmarks were reused, not repeated.

## OpenClaw SYS-MEM catch-up attempt — 2026-10-02

O pin fixado para a coorte é `openclaw/openclaw@e9571d77e76bd6d35996273d9e8398ad539b26e1`. A inspeção somente leitura no SHA exato encontrou testes de resolução de workspace/agent directory (`src/agents/agent-scope.test.ts`) e identidade de índice de memória (`extensions/memory-core/src/memory/index-identity.test.ts`); nenhum deles estabelece o contrato de sentinela persistente cross-agent deste gate, portanto nenhum resultado foi reaproveitado como PASS.

A tentativa de disponibilizar o checkout focado parou antes de clonar: `git clone --filter=blob:none --no-checkout --depth=20 https://github.com/openclaw/openclaw.git /tmp/atento-openclaw-exactpin` falhou ao conectar ao proxy de rede do executor. Nenhuma dependência foi instalada e nenhum teste foi iniciado.

```text
OPENCLAW_SYS_MEM_SENTINEL = BLOCKED_ENVIRONMENT (EXACT-PIN CHECKOUT UNAVAILABLE)
OPENCLAW_CANDIDATE_FAILURE = NOT_ESTABLISHED
OPENCLAW_FIXED_SYSTEM_COHORT_MEMBERSHIP = RETAINED
FULL_ATENTO_SYS_MEM = BLOCKED_ADAPTER
```

Próximo passo falsificável: com o checkout do pin e dependências congeladas disponíveis num runner, executar uma vez o menor caso de gravação/leitura persistente sob agente A e negação de listagem/leitura sob agente B; coletar o transcript bruto e classificar apenas essa propriedade. Não confundir este teste de componente com `SYS-MEM-01` integrado do Atento, que continua bloqueado pelo adapter/runtime de produto ausente.

## OpenClaw — normalized SYS-MEM persistent sentinel — 2026-10-02

No pin exato `openclaw/openclaw@e9571d77e76bd6d35996273d9e8398ad539b26e1`, instalei somente a dependência congelada dos workspaces necessários e executei um teste temporário focalizado contra `getMemorySearchManager`, com duas identidades e workspaces separados. A sentinela sintética foi gravada em `NAIA/MEMORY.md`; cada manager sincronizou o índice de memória real do componente com SQLite temporário e sem provider/vector.

Comando final:

```text
COREPACK_HOME=/tmp/atento-openclaw-corepack corepack pnpm exec vitest run \
  --config test/vitest/vitest.extension-database-workers.config.ts \
  extensions/memory-core/src/memory/sys-mem-cross-agent-probe.tmp.test.ts \
  --maxWorkers=1 --reporter=verbose
1 passed; duration 12.05s; exit 0
```

Resultado bruto: o manager NAIA retornou a sentinela no índice; a busca do manager Anna não continha a sentinela. Anna retornou uma correspondência fraca ao próprio arquivo porque o probe usou `minScore=0`; isso não expôs conteúdo de NAIA. A assertion compara presença/ausência do marcador, não exige uma lista de busca vazia.

Duas invocações iniciais não são resultados de candidato: a primeira usou o campo inexistente `result.text` em vez de `snippet`; a segunda exigiu lista vazia e marcou como falha um resultado fraco do arquivo próprio de Anna. Corrigi o oráculo para buscar somente vazamento da sentinela e executei a seleção novamente; o teste final passou. Não houve provider/modelo/ferramenta, dados reais, edição de fonte ou mudança de lockfile. O arquivo de teste temporário foi removido e `git status --short` ficou limpo no pin exato.

```text
OPENCLAW_SYS_MEM_PERSISTENT_SENTINEL = PASS_WITH_SCOPE
OPENCLAW_DIRECT_CANDIDATE_SCOPED_PASS = YES (IN-PROCESS MEMORY INDEX; DISTINCT WORKSPACES)
OPENCLAW_PROCESS_OR_HOST_BOUNDARY = NOT_TESTED
OPENCLAW_ATENTO_SYS_MEM_01 = BLOCKED_ADAPTER
OPENCLAW_CANDIDATE_ELIMINATION = NONE
```

Este resultado avança OpenClaw no slice comparável da sentinela persistente; não demonstra isolamento contra acesso ao filesystem fora da API do manager, nem prova o host/runtime/autoridade do Atento. O bloqueio integrado continua separado.


## Bob Labs and Ontheia SYS-MEM catch-up — 2026-10-02

### Bob Labs — exact pin `boblabs-eu/boblabs@a91d6dad098c8ba6d24436a856556078151db45d`

The exact-pin `control-plane/tests/repositories/test_cross_tenant.py` defines the memory-sharing confirmation negative/positive cases. `control-plane/tests/conftest.py` requires a real database URL containing `bob_test`, and the root `make test-only` runs migrations and pytest inside the `bob-manager-bob-api:latest` Docker image on the test network. This executor had no Docker/Podman, so the official test body was not started. A temporary local PostgreSQL 16 install was removed after confirming it could not supply the required official runner/image. The result remains `BLOCKED_ENVIRONMENT`; neither a candidate failure nor a test pass is claimed.

### Ontheia — exact pin `Ontheia/ontheia@70802db61eb16533f55efce3d8785d810223d03b`

Existing evidence already recorded in this file is the more relevant role-configured helper probe: three explicit `agent_id` namespaces were distinct, own-role reads were allowed, and six cross-role helper attempts were denied. Retain `PASS_WITH_SCOPE` for that configured namespace helper only; storage, PostgreSQL/RLS enforcement, and Atento identity binding were not exercised.

A further check in this session installed the locked host dependencies, built the host, and ran `node --test dist/memory/namespaces.spec.js`: 19 passed, 0 failed. This suite's negative case uses a foreign `user_id` against a namespace template. It overlaps the already-recorded helper property and does not add a new role-private-memory result; do not count it as a second pass.

### Queue continuation

OpenAkita's existing marker result is reused without rerun. Clawix remains unresolved for this memory slice: existing evidence covers path guards, while no exact-pin direct private-marker cross-role test is recorded. Continue at Clawix's frozen pin only if its real workspace/memory seam can express the same private marker property; otherwise record the narrow blocker and advance serially. The full Atento `SYS-MEM-01` remains `BLOCKED_ADAPTER`.


## Memoh and Letta Code SYS-MEM catch-up — 2026-10-02

### Memoh — exact pin `felinics/Memoh@3d60a08aa42fdcddb218401699822741b51b52ad`

The exact-pin in-memory runtime scope test passed:

```text
GOTOOLCHAIN=auto go test ./internal/memory/adapters/builtin -run '^TestMemoryRuntimesRejectForeignAndMissingScopeBeforeMutation$' -count=1
PASS (graph and file runtimes; in-memory fake stores)
```

It rejects foreign/missing-bot update/delete and adversarial formation mutations and checks that each bot's original item remains intact. This is component evidence with fake stores, not persistent read isolation.

The stronger existing integration case, `TestPostgresUpsertNodeRejectsConflictingBotScope`, was run once with the pin's embedded production migrations and a dedicated local PostgreSQL 16 database:

```text
GOTOOLCHAIN=auto TEST_POSTGRES_DSN=<isolated local DSN> go test ./internal/memory/wikistore -run '^TestPostgresUpsertNodeRejectsConflictingBotScope$' -count=1 -v
PASS (0.033s)
```

It created synthetic bot A/B rows for one synthetic user, rejected B's attempt to overwrite A's ID, confirmed A's original was unchanged, denied B's GetNode for A's ID, and allowed A's own update. The repo's Compose currently targets PostgreSQL 18; this disposable executor used 16, so the result is scoped to the exact-pin SQL/store behavior on PostgreSQL 16, not a version-matched deployment check. No model/provider or Atento runtime was used.

```text
MEMOH_PRIVATE_MEMORY_STORE_SCOPE = PASS_WITH_SCOPE
MEMOH_ATENTO_ROLE_ID_BINDING = NOT_TESTED
MEMOH_SYSTEM_SYS_MEM_01 = BLOCKED_ADAPTER
```

### Letta Code — exact pin `letta-ai/letta-code@21daa38a8cdd74f2d03b634c8312253080bacfc1`

Using Bun 1.3.14 and the frozen `bun.lock`, the focused `src/permissions/cross-agent-guard.test.ts` run passed: 63 tests, 0 failures, 102 expectations. It covers default-deny reads across permission modes for foreign API/local agent-memory paths, own-memory positive controls, recursive/list operations, symlink escapes for in-process file tools, and explicit parent/subagent scope.

Scope: this is policy/permission-layer proof with synthetic filesystem roots; it does not run an LLM, connect a Letta API, test an actual OS sandbox boundary, or map Atento role identities to Letta agent IDs. Some explicit parent guard-disable behavior is tested as configurable; an Atento profile would need to keep the default guard enabled. Historical overlay evidence at a different SHA was not reused as exact-pin proof.

```text
LETTA_CODE_CROSS_AGENT_MEMORY_TOOL_GUARD = PASS_WITH_SCOPE
LETTA_CODE_OS_PROCESS_BOUNDARY = NOT_TESTED
LETTA_CODE_ATENTO_ROLE_BINDING = NOT_TESTED
LETTA_CODE_SYSTEM_SYS_MEM_01 = BLOCKED_ADAPTER
```

### Fixed-cohort SYS-MEM position after catch-up

| Candidate | Best current memory evidence for this slice | Disposition |
|---|---|---|
| NanoClaw | Exact-pin 7/7 role-state/group isolation and negative cross-group lookup; no direct private-marker read between role memories. | `PASS_WITH_SCOPE` for state/group boundary; marker slice open. |
| AI Butler | Existing current-pin security scan has seven reachable advisories. | `BLOCK_CURRENT_PIN_ON_SECURITY`; do not rerun unchanged pin. |
| OpenClaw | Persistent synthetic marker returned by NAIA manager and absent from Anna manager at exact pin. | `PASS_WITH_SCOPE`; in-process index only. |
| QwenPaw | Existing API probe denies B's direct GET of A's private memory file. | `PASS_WITH_SCOPE`; no host/process boundary. |
| MindRoom | Mock facade/keyed tests pass; persistent three-role backend test remains blocked in its harness. | `BLOCKED_HARNESS`; MindRoom remains paused. |
| Bob Labs | Official test requires Docker and `bob-manager-bob-api:latest`; the test body did not start. | `BLOCKED_ENVIRONMENT`; no candidate failure. |
| Ontheia | Reuse the already-recorded explicit three-`agent_id` namespace helper: own scopes accepted, six cross-role scopes denied. The 19/19 additional user-namespace suite run was overlapping validation, not a new marker result. | `PASS_WITH_SCOPE` for configured helper; storage/RLS open. |
| OpenAkita | Reuse the previously recorded two-profile private-marker result. | `PASS_WITH_SCOPE`; no rerun. |
| Clawix | Exact-pin docs and query code define private wiki visibility by `ownerId=userId`; private pages are readable by the owner and that user’s agents. | `FAIL_WITH_SCOPE` for distinct Atento roles sharing one Clawix user; static product contract, no direct runtime probe. A distinct-user-per-role mapping may alter this, but is untested. |
| Memoh | Exact-pin real PostgreSQL store denied foreign-bot read and overwrite; also fake-store graph/file mutation scope test passed. | `PASS_WITH_SCOPE`; PostgreSQL 16, no Atento ID binding. |
| Letta Code | Exact-pin 63/63 cross-agent guard suite; in-process file reads denied across permission modes and symlink cases. | `PASS_WITH_SCOPE`; no actual kernel-boundary or Atento role mapping. |

```text
FIXED_COHORT_SIZE = 11
CANDIDATE_MEMORY_SLICE = MIXED_SCOPES; NO_AGGREGATE_SCORE
COMMON_ATENTO_SYS_MEM_01 = BLOCKED_ADAPTER
CANDIDATES_ELIMINATED_FROM_MISSING_EVIDENCE = 0
MINDROOM_REMAINS_PAUSED = YES
```



## SYS-TOOL-01 candidate evidence catch-up — 2026-10-02

This block reuses exact-pin evidence already recorded. No candidate suite or benchmark was rerun. The common property is an unauthorized attempt by role A to invoke a tool reserved to role B, with denial unless an explicit, typed, recipient-authorized handoff is present. Candidate-level configuration filters and isolated permission tests are labeled separately from a composed Atento runtime.

| Candidate / exact pin | Reusable tool-authority evidence | Current scoped disposition |
|---|---|---|
| NanoClaw — `nanocoai/nanoclaw@4c1eabd3ddd74cc3d71b1871da857391a9411c8d` | Exact-pin Atento 7/7 probe denied native direct A2A without a destination grant; reference-broker typed requests reached the real mailbox API under a test adapter. | `PASS_WITH_SCOPE`; test adapter, no deployed Atento broker/runtime. |
| AI Butler — `LumabyteCo/aibutler@c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c` | This authority slice was not advanced; current pin is separately security-blocked by the recorded scan. | `BLOCK_CURRENT_PIN_ON_SECURITY`; do not rerun unchanged pin. |
| OpenClaw — `openclaw/openclaw@e9571d77e76bd6d35996273d9e8398ad539b26e1` | The SYS-MEM manager probe did not exercise exclusive tool grants or A2A authorization. | `NOT_TESTED` for this slice. |
| QwenPaw — `agentscope-ai/QwenPaw@777441721aa72db8e380d90e4d0481b05cbfd4cc` | Existing exact-pin test shows toggling a tool for agent A does not change agent B's tool configuration. It is a configuration-isolation result, not an unauthorized runtime invocation through Atento. | `PASS_WITH_SCOPE` for per-agent tool configuration only. |
| MindRoom — `mindroom-ai/mindroom@4f3bd2d108a6f9be28174e0f66d78eeecddca386` | The standard `/v1` path does not execute with `user_agent`; a requester header is not an authority substitute. | `BLOCKED_HARNESS`; MindRoom remains paused. |
| Bob Labs — `boblabs-eu/boblabs@a91d6dad098c8ba6d24436a856556078151db45d` | Tool-authority execution was not advanced; its required official Docker runner/image is unavailable in this executor. | `NOT_TESTED`; environment block is not failure. |
| Ontheia — `Ontheia/ontheia@70802db61eb16533f55efce3d8785d810223d03b` | Existing test applies tool filtering through a configured binding. It does not establish the Atento role-to-binding mapping or a complete handoff. | `PASS_WITH_SCOPE` for configured binding only. |
| OpenAkita — `openakita/openakita@5f5b38da728274f0fd06461a481851be7c0bca6a` | Existing exact-pin checks show tool filtering by profile. Scheduler fallback on an unknown profile remains a separate authority/role-drift issue. | `PASS_WITH_SCOPE` for profile filtering; no Atento dispatch proof. |
| Clawix — `ClawixAI/clawix@5aee015e0bd793102fba69af486dd6e75df6d802` | Existing exact-pin probe showed an allow approval associated with the parent session accepted by a sub-agent carrying that same session ID. Separate-session composition was not tested. | `FAIL_WITH_SCOPE` for the shared-session path; do not generalize to a separate-session architecture. |
| Memoh — `felinics/Memoh@3d60a08aa42fdcddb218401699822741b51b52ad` | The SYS-MEM runtime/store tests did not exercise exclusive tools or ACL grants. | `NOT_TESTED` for this slice. |
| Letta Code — `letta-ai/letta-code@21daa38a8cdd74f2d03b634c8312253080bacfc1` | The 63-test memory guard suite protects cross-agent file reads; it does not test B-exclusive action tools or recipient-authorized handoff. | `NOT_TESTED` for exclusive-tool authority. |

```text
CANDIDATE_EXACT_PIN_TOOL_SIGNALS = SCOPED_AND_NONCOMPARABLE
REPRODUCED_FAILURE_SCOPE = CLAWIX_SHARED_SESSION_APPROVAL
CANDIDATES_ELIMINATED_FROM_MISSING_EVIDENCE = 0
COMMON_ATENTO_SYS_TOOL_01 = BLOCKED_ADAPTER
```

The Clawix failure is a concrete negative for the tested shared-session composition. It does not establish that separate-session mode fails. Existing candidate-specific filters are useful signals but do not close a common three-role assertion. The Atento host/runtime adapter needed to make the same A→B denial observable is still absent; do not create it only to unlock this test.


## SYS-CRED-01 credential/provider evidence catch-up — 2026-10-02

Reuse the component evidence below; no real credentials, provider calls, or equivalent tests were used in this block. The common property is that a secret granted only to role B is absent from role A's environment, files, arguments, logs, model-visible context, and provider request while B retains its own authorized path.

| Candidate / exact pin | Reusable evidence | Scope and disposition |
|---|---|---|
| NanoClaw — `nanocoai/nanoclaw@4c1eabd3ddd74cc3d71b1871da857391a9411c8d` | Role-unique synthetic identities were mounted per auxiliary container in the prior 7/7 profile probe. | `PASS_WITH_SCOPE` for synthetic identity mount separation only; no provider/gateway credential custody proof. |
| AI Butler — `LumabyteCo/aibutler@c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c` | Credential/provider slice not advanced; current pin is blocked on its recorded security scan. | `BLOCK_CURRENT_PIN_ON_SECURITY`. |
| OpenClaw — `openclaw/openclaw@e9571d77e76bd6d35996273d9e8398ad539b26e1` | SYS-MEM manager probe used no provider/vector and did not exercise gateway credential custody. | `NOT_TESTED` for role-bound provider secrets. |
| QwenPaw — `agentscope-ai/QwenPaw@777441721aa72db8e380d90e4d0481b05cbfd4cc` | Existing exact-pin test selected each agent's personal provider using a mock; no HTTP request was sent. | `PASS_WITH_SCOPE` for configuration selection only; not secret invisibility at the provider boundary. |
| MindRoom — `mindroom-ai/mindroom@4f3bd2d108a6f9be28174e0f66d78eeecddca386` | No role-level provider credential boundary was demonstrated. | `NOT_TESTED`; MindRoom remains paused. |
| Bob Labs — `boblabs-eu/boblabs@a91d6dad098c8ba6d24436a856556078151db45d` | Existing 21 HMAC/lab-binding unit assertions cover secret-binding components. | `PASS_WITH_SCOPE` for component signing/binding; no middleware/container/provider delivery proof. |
| Ontheia — `Ontheia/ontheia@70802db61eb16533f55efce3d8785d810223d03b` | Existing tests check absent secrets are excluded and configured secret values are masked. | `PASS_WITH_SCOPE` for resolver/redaction paths; no cross-role provider request. |
| OpenAkita — `openakita/openakita@5f5b38da728274f0fd06461a481851be7c0bca6a` | Existing exact-pin test checks redaction from diagnostic export. | `PASS_WITH_SCOPE` for export redaction; no provider-bound role-isolation proof. |
| Clawix — `ClawixAI/clawix@5aee015e0bd793102fba69af486dd6e75df6d802` | No role-bound provider secret result recorded. | `NOT_TESTED`. |
| Memoh — `felinics/Memoh@3d60a08aa42fdcddb218401699822741b51b52ad` | The current memory tests did not examine provider credentials. | `NOT_TESTED`. |
| Letta Code — `letta-ai/letta-code@21daa38a8cdd74f2d03b634c8312253080bacfc1` | The current memory-guard suite did not inspect provider secret injection or custody. | `NOT_TESTED`. |

```text
ROLE_LEVEL_PROVIDER_CREDENTIAL_CUSTODY = NOT_ESTABLISHED_FOR_ALL
REAL_CREDENTIALS_USED = 0
REAL_PROVIDER_CALLS = 0
COMMON_ATENTO_SYS_CRED_01 = BLOCKED_ADAPTER
```

Component secret handling is not equivalent to secret isolation by Atento role. The same candidate-neutral host/runtime seam is still required to prove that a role-B-only secret never reaches role A's process or model while B can use it. No adapter was invented to open this assertion.



## SYS-REL-01 reliability/recovery catch-up — 2026-10-02

This block reuses the frozen-pin CI, component probes, and previously recorded Atento runs. No equivalent suite, benchmark, replay test, or recovery test was rerun. Candidate lifecycle evidence is kept separate from the common role-bound Atento assertion.

| Candidate / exact pin | Reusable reliability or background evidence | Scoped disposition for this block |
|---|---|---|
| NanoClaw — `nanocoai/nanoclaw@4c1eabd3ddd74cc3d71b1871da857391a9411c8d` | Exact-pin CI (513 passed, 0 failed, 3 skipped) includes claim/incarnation, failed stop/release, host replacement, bounded persisted delivery attempts across restart, container restart and orphan paths. Prior Atento hosted run 36815873223 passed 7/7 with scope. Prior raw-webhook SSE replay after SIGKILL/restart reused SQLite and the same port; synthetic unknown token returned 401. None ran an Atento role-owned scheduled task through host restart and terminal retry. | `PARTIAL_PASS_WITH_SCOPE` for candidate lifecycle and raw-webhook replay. `BLOCKED_ADAPTER` for task retry under integrated Atento host. Reuse; do not repeat. |
| AI Butler — `LumabyteCo/aibutler@c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c` | Exact-pin race CI run 28973914814 passed, including internal/schedule; `TestTickUsesScopedCapabilities` checks scoped schedule capability behavior. Later scheduled scan 36426287353 found seven reachable advisories. | `PASS_WITH_SCOPE` for the narrow scheduler assertion only; `BLOCK_CURRENT_PIN_ON_SECURITY` independently. No recovery requalification on the unchanged pin. |
| OpenClaw — `openclaw/openclaw@e9571d77e76bd6d35996273d9e8398ad539b26e1` | Previously recorded exact-pin replay probe: after SIGKILL, server rebound on the same port within 5s, reused SQLite state, and replayed the per-agent SSE event; unknown synthetic token received HTTP 401. One successful replay case. | `PASS_WITH_SCOPE` for raw-webhook SSE replay only. Scheduled task retry, real authentication, provider/gateway, and Atento host recovery remain `NOT_TESTED`. |
| QwenPaw — `agentscope-ai/QwenPaw@777441721aa72db8e380d90e4d0481b05cbfd4cc` | Existing exact-pin cron probe with no explicit configuration produced `approval_level=off`; static/runtime audit also identifies sandbox-unavailable fallback that can broaden authority, incomplete main-test evidence, and a failed full nightly. | `FAIL_WITH_SCOPE` for the permissive default-cron authority path; hold other restart/recovery claims until fail-closed behavior and passing frozen-pin runtime evidence exist. |
| MindRoom — `mindroom-ai/mindroom@4f3bd2d108a6f9be28174e0f66d78eeecddca386` | Existing worker/memory evidence is harness-scoped; no comparable role-bound host restart/retry result is recorded. MindRoom remains paused per the cohort order. | `NOT_TESTED` for restart/recovery; do not advance or repeat while the other active alternatives catch up. |
| Bob Labs — `boblabs-eu/boblabs@a91d6dad098c8ba6d24436a856556078151db45d` | Official test runner requires Docker and `bob-manager-bob-api:latest`; this executor lacks Docker/Podman and the image. The test body did not start. | `BLOCKED_ENVIRONMENT`; no candidate failure or recovery pass. |
| Ontheia — `Ontheia/ontheia@70802db61eb16533f55efce3d8785d810223d03b` | Existing exact-pin recovery probe recorded a one-shot `run_at` post-claim failure path. Other namespace/helper evidence belongs to the memory slice and is not recovery evidence. | `FAIL_WITH_SCOPE` for the tested one-shot post-claim recovery path; do not generalize to recurring jobs or the entire candidate. |
| OpenAkita — `openakita/openakita@5f5b38da728274f0fd06461a481851be7c0bca6a` | Existing exact-pin scheduler probe supplied an unknown synthetic profile ID; scheduler instantiated the default agent, producing role drift. Prior same-user/two-workspace evidence is a separate isolation assertion. | `FAIL_WITH_SCOPE` for scheduler fallback/role drift. A host-side fail-closed composition is possible but absent and untested. |
| Clawix — `ClawixAI/clawix@5aee015e0bd793102fba69af486dd6e75df6d802` | Recorded negative evidence is approval reuse in a shared parent/sub-agent session; it is a tool-authority result, not restart/recovery proof. No comparable recovery run is recorded. | `NOT_TESTED` for restart/recovery; retain the separate shared-session `FAIL_WITH_SCOPE` under SYS-TOOL-01 only. |
| Memoh — `felinics/Memoh@3d60a08aa42fdcddb218401699822741b51b52ad` | Existing exact-pin memory scope tests cover fake stores and a PostgreSQL 16 store boundary; they do not induce restart or task retry. | `NOT_TESTED` for restart/recovery. |
| Letta Code — `letta-ai/letta-code@21daa38a8cdd74f2d03b634c8312253080bacfc1` | Existing 63/63 permission-guard suite covers in-process memory access and symlink cases; it does not exercise process recovery or scheduled task retries. | `NOT_TESTED` for restart/recovery. |

```text
FIXED_COHORT_SIZE = 11
RELIABILITY_EVIDENCE = MIXED_SCOPES; NO_AGGREGATE_SCORE
CANDIDATE_PATH_FAILURES = QWENPAW_DEFAULT_CRON_AUTHORITY, ONTHEIA_RUN_AT_POST_CLAIM, OPENAKITA_UNKNOWN_PROFILE_FALLBACK
NANOCLAW_CANDIDATE_LIFECYCLE_AND_OPENCLAW_SSE_REPLAY = PASS_WITH_SCOPE
AI_BUTLER_CURRENT_PIN = BLOCK_CURRENT_PIN_ON_SECURITY
BLOCKED_ENVIRONMENT_OR_NOT_TESTED = NOT_CANDIDATE_FAILURE
COMMON_ATENTO_SYS_REL_01 = BLOCKED_ADAPTER
CANDIDATES_ELIMINATED_FROM_MISSING_EVIDENCE = 0
EQUIVALENT_TESTS_OR_BENCHMARKS_RERUN = 0
```

The three scoped failures eliminate only the reproduced paths/configurations, not whole candidate families where a distinct fail-closed composition could address the boundary. Component lifecycle and SSE replay do not prove the common Atento contract. The smallest integrated assertion remains the frozen-handoff task: persist one inert NAIA-owned scheduled task, interrupt the existing host after claim and before terminal ack, restart the same host/store, permit one bounded retry, then verify role ownership, equal-or-narrower grants, and exactly one terminal delivery. Current result: `NAIA_HOST_PROCESS_TASK_RETRY_AFTER_RESTART = BLOCKED_ADAPTER`. Do not build a product adapter just to open it; do not repeat the already-passing 7/7 hosted probe or raw-webhook replay.


## SYS-COST-01 footprint and adaptation-cost evidence audit — 2026-10-02

This is a read-only metadata snapshot from GitHub repository objects, collected 2026-10-02. The API `size` value is in KiB and describes each repository as it exists now on its default branch; it is not the frozen candidate commit, an install size, a deployment image, or a runtime memory measure. It excludes any claim about hardware requirements and may reflect repository history/storage conventions. Use it only as a coarse repository-footprint proxy, not as a ranking or exact-pin size.

| Fixed-cohort candidate | Repository | GitHub `size` now (KiB) | Approx. repository footprint |
|---|---|---:|---:|
| NanoClaw | `nanocoai/nanoclaw` | 32,771 | 32.0 MiB |
| AI Butler | `LumabyteCo/aibutler` | 1,790 | 1.7 MiB |
| OpenClaw | `openclaw/openclaw` | 7,485,543 | 7.14 GiB |
| QwenPaw | `agentscope-ai/QwenPaw` | 130,767 | 127.7 MiB |
| MindRoom | `mindroom-ai/mindroom` | 77,211 | 75.4 MiB |
| Bob Labs | `boblabs-eu/boblabs` | 9,300 | 9.1 MiB |
| Ontheia | `Ontheia/ontheia` | 3,263 | 3.2 MiB |
| OpenAkita | `openakita/openakita` | 295,541 | 288.6 MiB |
| Clawix | `ClawixAI/clawix` | 13,733 | 13.4 MiB |
| Memoh | `felinics/Memoh` | 116,605 | 113.9 MiB |
| Letta Code | `letta-ai/letta-code` | 100,315 | 98.0 MiB |

No exact-pin LOC, tracked-source bytes, installed dependency bytes, or deployment image sizes were returned by the available repository-metadata endpoint. Exact-pin checkout transfer previously failed for OpenClaw when the executor network proxy refused the clone. Do not infer that the large OpenClaw repository size equals the runtime needed by a minimal deployment.

### Adaptation-cost disposition

The existing gate records identify concrete repair surfaces for QwenPaw's default cron authority, Ontheia's one-shot `run_at` post-claim path, and OpenAkita's unknown-profile scheduler fallback. They do not yet contain a frozen-pin patch-size estimate, dependency/build impact, tests required for repair, or confirmation that each candidate can fix the issue without moving the boundary into a missing Atento host adapter. Assigning numeric effort or a relative repair-cost ranking now would be speculation.

```text
CURRENT_REPOSITORY_SIZE_PROXY = RECORDED_FOR_11_CANDIDATES
EXACT_FROZEN_PIN_LOC_AND_DEPLOYMENT_FOOTPRINT = NOT_AVAILABLE
ADAPTATION_FIX_COST_RANK = NOT_ESTIMATED (INSUFFICIENT PIN-SCOPED REPAIR EVIDENCE)
CANDIDATE_RANKING_OR_SELECTION_CHANGED = NO
MINDROOM_REMAINS_PAUSED = YES
```

Smallest next cost-evidence step: inspect only the three failing paths at their frozen pins and capture the source files, configuration defaults, dependency/build boundary, and smallest fail-closed correction/test sketch; then classify repair effort with one consistent rubric. Do not implement candidate fixes as part of this audit. For source size, obtain exact-pin source archives in a permitted runner and count tracked source files/LOC with one frozen extension/filter rule across the entire cohort; do not substitute current default-branch sizes for pinned measurements.


### Frozen-pin repair-scope triage — 2026-10-02

Read-only source inspection at each failing pin narrowed the candidate-local correction surface. This is a structural code/test estimate, not person-hours, a committed fix, or a comparative qualification result.

| Candidate / frozen source | Observed failure mechanism at the pin | Smallest defensible correction and regression evidence | Structural effort |
|---|---|---|---|
| QwenPaw — [cron models](https://github.com/agentscope-ai/QwenPaw/blob/777441721aa72db8e380d90e4d0481b05cbfd4cc/src/qwenpaw/app/crons/models.py) and [executor](https://github.com/agentscope-ai/QwenPaw/blob/777441721aa72db8e380d90e4d0481b05cbfd4cc/src/qwenpaw/app/crons/executor.py) | `CronJobRuntimeConfig.tool_safety` defaults to `False`; the frozen executor maps that value to `ToolExecutionLevel.OFF`. Existing negative result matches this exact default path. | Make unattended execution fail closed when the field is omitted; preserve explicit, reviewed configuration semantics. Add frozen-pin tests for omitted/default, explicit safe setting, and request-context approval value. Check all creation surfaces before implementation. | **M** — default propagation/config compatibility plus focused regression assertions; exact fix not selected. |
| Ontheia — [CronService](https://github.com/Ontheia/ontheia/blob/70802db61eb16533f55efce3d8785d810223d03b/host/src/runtime/CronService.ts) | The one-shot poll atomically commits `active=false` before launching `_executeJob`; an execution rejection is only logged by the fire-and-forget catch. The failed one-shot is therefore not eligible for another poll. | Add persistent claim/attempt/recovery semantics that prevent duplicate execution while making an unacknowledged failure retryable; add fault-injection coverage across claim, failure, restart, bounded retry, and terminal ack. | **L** — durable lifecycle/state-machine change and restart/duplicate controls. |
| OpenAkita — [scheduler executor](https://github.com/openakita/openakita/blob/5f5b38da728274f0fd06461a481851be7c0bca6a/src/openakita/scheduler/executor.py) | `_resolve_agent_profile` returning no profile for a non-default ID logs a warning and then constructs the default `Agent`, causing silent role drift. | Fail the scheduled task closed for an unknown profile, retain the explicit default-ID behavior, and add a regression that proves unknown IDs do not instantiate the default agent. | **S** — a local fallback branch plus focused test; host-side role validation remains separately required. |

Effort rubric: **S** = one candidate-local branch/default and focused regression; **M** = configuration/default propagation across creation surfaces plus regression coverage; **L** = persistent task-lifecycle/state-machine semantics with restart, bounded-retry, and duplicate-delivery assertions. These are relative implementation-surface categories only; no calendar or labor-hour estimate is defensible from this evidence.

```text
QWENPAW_REPAIR_SCOPE = M (STRUCTURAL; UNIMPLEMENTED)
ONTHEIA_REPAIR_SCOPE = L (STRUCTURAL; UNIMPLEMENTED)
OPENAKITA_REPAIR_SCOPE = S (STRUCTURAL; UNIMPLEMENTED)
COMMON_ATENTO_HOST_ADAPTER_COST = NOT_ESTIMABLE (NO EXECUTABLE DESIGN/SEAM)
REPAIR_TESTS_RUN = 0
CANDIDATE_REPOSITORIES_MODIFIED = 0
```

These candidate-local corrections would not supply the missing Atento host/runtime/gateway seam and do not change any integrated gate from `BLOCKED_ADAPTER`. No candidate ranking, elimination, or selection changes follow from this effort triage.


## SYS-BENCH-01 published-score comparison catch-up — 2026-10-02

This block reuses published results and adds no benchmark runs. The only direct fixed-cohort pair found on one current published harness benchmark is PawBench v1.0: the official 150-task page reports a 9-model average of OpenClaw 72.1 and QwenPaw 73.7, with harness versions OpenClaw v2026.4.24 and QwenPaw v1.1.3. This is a **+1.6 point PawBench signal for QwenPaw** under that published release matrix. It is not a pass on Atento's frozen pins and does not test role isolation, credentials, or recovery. PawBench describes scores as a model × harness matrix and says the axes should be read independently; the 150 tasks combine six sources and include text and multimodal tasks ([methodology](https://agentscope-ai.github.io/PawBench/en/blog/PAWBENCH_MODEL_HARNESS_BLOG_EN/)).

| Existing benchmark signal | Valid comparison | What it does not establish |
|---|---|---|
| PawBench v1.0: OpenClaw 72.1; QwenPaw 73.7 average | Same benchmark page and 9-model matrix; QwenPaw leads by 1.6 points for those published versions. | Frozen-pin behavior, cost on the user's API/model setup, or Atento security gates. |
| Auto-ClawEval: NanoClaw 63.7 full / 67.8 Mini; CoPaw 60.8 full / 59.3 Mini | Same paper, Claude Haiku 4.5; NanoClaw's reported means are +2.9 full and +8.5 Mini. The paper places them in different integration tiers (NanoClaw Tier 2 MCP; CoPaw Tier 3 SKILL.md + shell). | CoPaw is historical QwenPaw lineage, not the frozen QwenPaw pin; tier differs, so this is not a clean current-candidate head-to-head. [Paper](https://arxiv.org/abs/2604.18543). |
| Terminal-Bench 2.0: Letta Code 59.1% ±2.4 with Claude Opus 4.5; 53.5% ±2.8 with GPT-5.1-Codex | Two model configurations for the same agent/benchmark; keep each result as its own line. | Cross-agent ranking against PawBench/Auto-ClawEval or isolation/recovery qualification. [Leaderboard archive](https://hub.harborframework.com/datasets/terminal-bench/terminal-bench-2/latest?leaderboard=2-0&tab=leaderboard). |
| AI Butler internal live eval: 4/7 | Retain as a small first-party observation for that exact pin/eval. | Comparable score against external benchmarks or other candidate suites. |
| Other frozen-cohort candidates | No reusable score located in the current benchmark record. | Missing score is not zero and does not eliminate a candidate. |

```text
BENCHMARK_RUNS_THIS_BLOCK = 0
SAME_BENCHMARK_FIXED_COHORT_PAIR = OPENCLAW_VS_QWENPAW (PawBench release matrix only)
PAWBENCH_SIGNAL = QWENPAW +1.6 POINTS (PUBLISHED HARNESS VERSIONS)
CROSS_BENCHMARK_AGGREGATE_SCORE = NOT_CREATED
FROZEN_PIN_QUALIFICATION_FROM_BENCHMARK = NONE
CANDIDATE_SELECTION_CHANGED = NO
```

The prior table's PawBench row now includes both OpenClaw and QwenPaw, resolving the previously split recording. Keep published benchmark scores as the functional-quality axis only. Existing common Atento memory/tool/credential/recovery gates remain separate; no candidate is promoted or eliminated by this score catch-up.


## Clawix SYS-MEM private-role scope resolution — 2026-10-02

Read-only inspection at exact pin `ClawixAI/clawix@5aee015e0bd793102fba69af486dd6e75df6d802` resolved whether the existing seam can express role-private memory.

- The pinned [memory contract](https://github.com/ClawixAI/clawix/blob/5aee015e0bd793102fba69af486dd6e75df6d802/docs/MEMORY.md) says private wiki pages belong to a user and are readable by that owner and their agents.
- The pinned [WikiSearchRepository](https://github.com/ClawixAI/clawix/blob/5aee015e0bd793102fba69af486dd6e75df6d802/packages/api/src/db/wiki-search.repository.ts) takes `userId` as its identity input; `ownership='mine'` filters only `WikiPage.ownerId = userId`, while `visible` adds group/org shares. The query has no `agentDefinitionId` or role-scoped key.
- The pinned [SPEC](https://github.com/ClawixAI/clawix/blob/5aee015e0bd793102fba69af486dd6e75df6d802/docs/SPEC.md) separately keys sessions by `(userId, agentDefinitionId, channelId)`. Session separation therefore does not make private wiki pages role-private.
- Clawix's own memory guide describes the wiki as a shared continuity layer across agents for one user. This is intentional product behavior, not evidence of accidental database leakage.

For the frozen Atento profile—three roles under one user identity—the private-memory contract does not isolate one role's private marker from another. Record `FAIL_WITH_SCOPE` for this same-user role-private property based on the exact-pin authorization contract; do not generalize to the whole Clawix family. Separate Clawix user IDs per role could create a different composition, but Atento identity mapping, shared profile handling, and cross-user controls would then need explicit testing. No private-marker test was run, no Prisma setup/harness was fabricated, and no Clawix source was modified.

```text
CLAWIX_SAME_USER_ROLE_PRIVATE_MEMORY = FAIL_WITH_SCOPE (STATIC PINNED CONTRACT)
CLAWIX_DIRECT_PRIVATE_MARKER_RUNTIME_PROBE = NOT_RUN
CLAWIX_DISTINCT_USER_PER_ROLE_COMPOSITION = NOT_TESTED
CLAWIX_CANDIDATE_FAMILY_ELIMINATED = NO
COMMON_ATENTO_SYS_MEM_01 = BLOCKED_ADAPTER
```

This supersedes the earlier Clawix `NOT_TESTED` row for the narrow same-user role-private property. Existing filesystem path guards remain scoped to path traversal and do not repair the user-scoped wiki visibility model.
