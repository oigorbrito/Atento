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
