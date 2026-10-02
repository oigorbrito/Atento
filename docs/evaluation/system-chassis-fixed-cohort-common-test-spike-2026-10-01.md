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
