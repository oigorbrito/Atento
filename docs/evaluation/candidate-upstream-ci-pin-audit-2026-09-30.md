# Candidate upstream CI pin audit — 2026-09-30

## Purpose and boundary

This is one additional evidence pass for the frozen candidate pins recorded in the candidate freeze documents. It captures upstream GitHub Actions workflow health at those pins so that later Atento-specific probes can account for current source health.

This audit does **not** qualify any pin, rank candidates, award an isolation score, or establish Atento behavior. A green upstream workflow is not evidence of role isolation, authority parity, or safe external-effect recovery. The chassis probe `RP-EFFECT-01` remains **PENDING** and was not run.

## Method

- Queried GitHub Actions `push` workflow runs at the exact candidate SHA (first page, up to 100) for the 28 rows below.
- For rows with no observed push run, queried the connector's commit-associated workflow-runs endpoint, which is limited to pull-request-triggered runs. Those queries returned no runs.
- Inspected job summaries and available logs for the failing runs and the QwenPaw waiting run.
- Legacy commit statuses were inspected separately. OpenMausBot and Rakazo showed Vercel deployment success; this is deployment status, not a test result.
- A push query for OpenMausBot was initially made against an incorrect SHA. That row is explicitly marked unverified; the wrong-SHA result is excluded. Its corrected-SHA PR query returned no run, but a corrected-SHA push query was not confirmed in this pass.
- These are observed workflow records, not a locally reproduced test suite. The audit is time-bounded to the queried events and does not cover scheduled, manual, release, or other workflow triggers unless listed.

## Results

| Candidate | Frozen pin | Observed upstream CI/workflow result at pin | Interpretation |
|---|---|---|---|
| OpenClaw | `ca8f24d05fc49a224adab0c9426077fd8d93801d` | Only `security-fast` ran successfully; preflight, core checks, and UI/E2E jobs were skipped at this push. [Run](https://github.com/openclaw/openclaw/actions/runs/36650380651) | Security/diff checks only; this pin has no functional-test execution evidence from the observed push run. |
| OpenMausBot | `6005b1bf5883a7ffa639c07e729321f89b9532e1` | Corrected-SHA CI and Docker image runs both succeeded. CI includes unit/eval and platform smoke jobs. [CI](https://github.com/milind-soni/OpenMausBot/actions/runs/36647214650) · [Docker](https://github.com/milind-soni/OpenMausBot/actions/runs/36647214680) | Corrected result supersedes the unverified row in the initial audit; details and boundary limits below. |
| QwenPaw | `777441721aa72db8e380d90e4d0481b05cbfd4cc` | Frontend, pre-commit, CodeQL, E2E smoke, formatting succeeded; Tests workflow remains waiting at Maintainer Approval. [Waiting run](https://github.com/agentscope-ai/QwenPaw/actions/runs/36559841525) | Partial green; core Tests run is pending approval, not a failure. |
| AI Butler | `c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c` | CI and Security succeeded. | Green observed workflows; no isolation proof. |
| NanoClaw | `4c1eabd3ddd74cc3d71b1871da857391a9411c8d` | CI and registry-skills workflows succeeded. | Green observed workflows; no isolation proof. |
| TrustClaw | `c07410bccb916236b45b563e8c4ff76ad83d3855` | No push or PR-triggered runs observed at the pin. | No run observed; functional test coverage unknown. |
| Open Assistant | `32c55d2643f9fe38777f9212588b2eee45392514` | Release workflow succeeded. | Release workflow only; not a functional test result. |
| Rakazo | `f4583525d632fcd8643fd6e24c7f51e3e04cb990` | CI failed in Playwright E2E; typecheck, lint, production build, Electron smoke, Postgres journeys, and unit tests succeeded. Playwright failed `later bot waits before showing the focus card; sending cancels it`: after sending and advancing the clock, the focus card remained visible (expected 0 matches, received 1); five scripted agent runs also failed. [Run](https://github.com/elie222/rakazo/actions/runs/36619326151) | Concrete E2E gap; not specifically an isolation test. |
| Gobii | `c9929bf8ea59b4695b99dcab59aa6c97a09c5bdb` | Two test shards failed: SMTP BCC header assertion and missing migration module `api.migrations.0460_native_email_integrations`. Other shards, timeline PostgreSQL integration, sandbox server, and frontend jobs succeeded. [Run](https://github.com/gobii-ai/gobii-platform/actions/runs/32515641268) | Concrete upstream test/build consistency gaps; no mapping to isolation established. |
| Octop | `e473dd3c4a4741618ffde1a42a3492341a189e8e` | CodeQL succeeded. | Security scan only; functional test result unknown. |
| PersonalJarvis | `1be33c457739ca7e161ee6fbaf298ec10d4dad3b` | CI failed. Linux shard reported 5,003 passed / 51 failed / 39 skipped, with 50 failures already baselined and 1 new. Several realtime-provider endpoint tests returned 404. Static gates failed: silent-exceptions, async-routes, public-docs. Merge train succeeded. [CI run](https://github.com/PersonalJarvis/PersonalJarvis/actions/runs/36601197262) | Mixed: one new test failure plus static-gate failures; not simply a baseline-only failure. |
| Letta Code | `21daa38a8cdd74f2d03b634c8312253080bacfc1` | No push or PR-triggered runs observed at the pin. | No run observed; functional test coverage unknown. |
| Kortix/Suna | `270c4a57c8ae5ffb85eff6d5b9700c5713612f28` | Tests, CI, DB migrations, security scans, catalogs, and development deploy workflows succeeded. | Green observed workflows; no isolation proof. |
| Rome | `ef523c4659149e2711744deb04ec42c3be339907` | CI, E2E Testing by Midscene, and Release succeeded. | Green observed workflows; no isolation proof. |
| Agent Zero | `e3051fb584b1a36be2b0a0c90606f1c2c2d356ec` | Docker image build/publish workflow succeeded (three associated runs). | Build evidence only; no functional test result established. |
| OpenGrokBot | `43ba51fc0487b7adbb23861a1062a113390833d9` | Typecheck succeeded; tests failed 1 of 320 (319 passed): a turn-queue test expected two bot messages but observed one. Bot computer image build succeeded. [Run](https://github.com/wolfqing/OpenGrokBot/actions/runs/36511497713) | Concrete concurrency/turn handling test gap relevant to lifecycle behavior, not a direct isolation verdict. |
| SelfAgent | `c86b0b1fbc0e177e67b59b8d26cc2ce9c18406d1` | No push or PR-triggered runs observed at the pin. | No run observed; functional test coverage unknown. |
| GoClaw | `c24c50ba2d16daff6aa2809b6c1a6f592977ae54` | No push or PR-triggered runs observed at the pin. | No run observed; functional test coverage unknown. |
| Nebo | `d566d27ec7c5ab36f3b95fdfda371bb45994dfd7` | Build-and-push workflow failed; deployment was skipped. Job summary did not expose test steps. | Build/deploy failure; functional test status unknown. |
| AutoMate | `7e197b49135590b0f78c8cd9cd570dfd6764afab` | No push or PR-triggered runs observed at the pin. | No run observed; functional test coverage unknown. |
| AgentOS | `226c906291fc68f3c4517623446bdaec1b48a82d` | CI, Web UI Browser Smoke, frontend, and release-asset workflows succeeded. | Green observed workflows; browser smoke is not an isolation proof. |
| OpenAgentd | `b2acf236f4e9e6b503281f2364e9915a60158376` | No push or PR-triggered runs observed at the pin. | No run observed; functional test coverage unknown. |
| Open Intern (deferred) | `e2d9dc312a1a07a304c55d88a92c1f0b86cd68c9` | No push or PR-triggered runs observed at the pin. | Deferred candidate; no run observed. |
| HubOS | `7c14b14ed1d26c3d1b597cc213cf97ddfbb7cdcb` | Pre-commit checks succeeded. | Pre-commit only; functional test result unknown. |
| Engram | `3a43667deec4a680b42f3e880d7d6bac3baf0746` | CI and Release succeeded. | Green observed workflows; does not change the separate Atento Engram runtime integration state. |
| Holt | `3a9cb8b0fd62e0b61e5e600a3fa341bd5b03e65e` | CI and Release succeeded. | Green observed workflows; no isolation proof. |
| RustFox | `6e24388d36d1c6fac399039d8cab07cd9cb8264b` | CI succeeded. | Green observed workflow; no isolation proof. |
| PsychAgent | `469f45ef468b968b3fccd1936d7e6a0a574e4c5c` | No push or PR-triggered runs observed at the pin. | No run observed; functional test coverage unknown. |
| OpenCouch | `ac5af6ee4c9a06b4050c5a912439f343ade2c35c` | CI succeeded. | Green observed workflow; no isolation proof. |

## Effect on the Atento evaluation

- This audit adds upstream workflow health and pinpointed failure evidence only.
- It does not close residual families A/I/L/B/E/D/C/G from the residual-only probe ledger.
- No candidate is promoted or removed based on this status pass.
- `RP-EFFECT-01 = PENDING`; no uncertain-outcome external effect was exercised.
- Rows with no observed runs remain **unknown coverage**, not test failures.


## Focused test-coverage pass

A second pass inspected completed job summaries and logs for tests relevant to authority, boundaries, memory ownership, browser/sandbox use, and recovery. This was a log-level evidence review of the same frozen pins, not a new local execution. Test names below indicate what those upstream suites assert; they do not prove Atento's three-role topology.

| Candidate | Test execution / directly relevant assertions observed | What remains unproved for Atento |
|---|---|---|
| OpenClaw | The push run executed `security-fast`; core checks, test shards, and UI/E2E jobs were skipped. | No functional tests from this observed pin run to transfer. |
| OpenMausBot | Pin-specific push result remains unverified after correcting the SHA; corrected PR query returned no run. | No test evidence attributed in this pass. |
| QwenPaw | UI smoke: 4 passed, 234 deselected. Exact-pin source uses mocked auth/agents/catch-all API routes and only checks login-page rendering. Frontend/pre-commit passed; main Tests workflow still waits for maintainer approval. | Smoke validates frontend harness only; no backend or cross-role isolation assertion ran. |
| AI Butler | Race-enabled Go tests passed, including `internal/permissions`, `internal/plugin/sandbox`, and `internal/shell/sandbox`; integration and security jobs passed. Package coverage reported 94.7% permissions, 90.9% plugin sandbox, and 35.3% shell sandbox. | Package coverage is not evidence that separate roles cannot cross-read memory, credentials, tools, or channels. No explicit three-role isolation assertion was identified in these logs. |
| NanoClaw | Host/container suites passed. Logs include per-provider continuation state selecting the correct slot, memory scaffolding that avoids importing legacy workspace memory, and failure-closed behavior for malformed memory-hook input. | These are narrow provider/workspace-memory boundaries, not cross-role credential/tool/channel isolation. |
| TrustClaw | No push or PR workflow run observed at the pin. | No run-backed test coverage to transfer. |
| Open Assistant | The observed workflow only created a release. | No test execution evidence from that run. |
| Rakazo | Unit tests (including integration and Postgres journeys) passed; 154 browser E2E cases passed and one failed: delayed focus card remained visible after sending should have cancelled it. | The observed suite does not close the selected profile's cross-role boundaries. |
| Gobii | Sandbox-server and most backend shards passed. Two shards failed on an SMTP BCC assertion and an absent migration module. | No evidence that per-agent memory/secret primitives compose into independent NAIA/Anna authority domains. |
| Octop | CodeQL analysis passed. | Static security analysis only; no functional boundary assertion in this run. |
| PersonalJarvis | Linux test shard reported 5,003 passed, 51 failed (50 baseline-known, one new); static gates for silent exceptions, async routes, and public docs failed. Several realtime-provider tests returned 404. | Functional suites remain mixed; target-profile authority and cross-role isolation are open. |
| Letta Code | No push or PR workflow run observed at the pin. | No run-backed test coverage to transfer. |
| Kortix/Suna | Core/browser/package suites passed (logs report 709/709 and 502/502 in separate test invocations). Logs cover session-cache ownership across sandboxes, collision handling for duplicate session IDs, and project-secret strategy/audit behavior. | Session ownership and secret lifecycle tests do not establish separate role memory/tool/channel authority. |
| Rome | Integration suite: 31 passed, 3 skipped. Tests explicitly cover approval exception → journal persistence → replay → action execution, and strict-mode behavior on replay divergence. | Useful approval/recovery evidence; it does not establish role separation or background authority parity. |
| Agent Zero | Image build/publish workflow succeeded; no functional test job ran in the inspected run. | No run-backed test coverage to transfer from that run. |
| OpenGrokBot | 319/320 tests passed. A bot turn-queue test failed; a separate test in the same suite passed that a bot may stop its own routine but not a teammate's. | Narrow ownership assertion is useful; one concurrency/lifecycle failure remains, and broad memory/credential/channel separation is not established. |
| SelfAgent | No push or PR workflow run observed at the pin. | No run-backed test coverage to transfer. |
| GoClaw | No push or PR workflow run observed at the pin. | No run-backed test coverage to transfer. |
| Nebo | Build/deploy job failed; job summary exposed no test steps. | Functional test coverage unknown. |
| AutoMate | No push or PR workflow run observed at the pin. | No run-backed test coverage to transfer. |
| AgentOS | Python and UI suites passed (logs report 16,774 Python tests and 2,382 UI tests). UI tests cover approval prompts/pages and memory views; a task-runtime cleanup-under-load test passed. | These runs demonstrate product/UI behavior and cleanup, not technical cross-role denial at runtime. |
| OpenAgentd | No push or PR workflow run observed at the pin. | No run-backed test coverage to transfer. |
| Open Intern (deferred) | No push or PR workflow run observed at the pin. | Deferred; no run-backed test coverage. |
| HubOS | Pre-commit checks passed; no functional test step appeared in the inspected run. | No run-backed functional coverage to transfer. |
| Engram | CI includes deterministic eval (4/4) and tests for deny-by-default sandbox network, explicit approval before tainted egress, refusal when untrusted and sensitive content are combined, approval requests that stop without granting, and memory facts tagged with the active actor. | Strong narrow authority/sandbox/taint evidence; does not prove separate NAIA/Anna stores, credentials, channels, or broker-only handoff. |
| Holt | Build and CLI smoke tests passed on Node 20 and 22. | Smoke checks do not exercise the frozen external-brain dependency authority seam. |
| RustFox | Tests passed for `allowlist_isolation_across_bots`, high-risk task approval, per-bot session-key isolation for the same user, cancellation isolation across bots, and secret masking/private secret storage. | This is the strongest directly relevant cross-bot test evidence in this pass, but it still does not prove separate cross-role memory/channel domains or composed scheduled authority. |
| PsychAgent | No push or PR workflow run observed at the pin. | No run-backed test coverage to transfer. |
| OpenCouch | Backend tests passed (1,633); logs include database rejection of invalid memory namespace kinds. | Schema validation is not cross-agent isolation evidence. |

### Coverage result

The observed upstream tests provide **transferable, narrow evidence** for particular mechanisms: sandbox/network default, approval and replay, per-bot allowlist/session/cancellation isolation, memory actor tagging, and memory/provider-slot separation. The log review found no test that demonstrates all Atento requirements together: isolated NAIA/Anna memory, credential, tool, and channel authority with only explicit brokered handoff.

This is a coverage gap map, not a failure score. Existing assertions should be reused at their proven boundary; the missing composed property remains for a later, separately gated probe.


## Exact-pin assertion review

For the narrow test names called out above, source files were fetched at the same candidate SHAs used by the workflows. This checks what the tests actually assert, rather than relying on names or CI green status.

| Candidate / exact-pin test | Assertion verified in source | Evidence scope |
|---|---|---|
| RustFox — `tests/telegram_update_injector.rs::allowlist_isolation_across_bots` | Main bot accepts a Telegram update; researcher bot with a different allowed-chat set returns `RejectedAllowlist`. | Positive, narrow per-bot Telegram allowlist routing. It does not test memory, credentials, tool registry, or channel/session isolation. |
| RustFox — `tests/supervisor_dod_smoke.rs::dod_high_risk_task_requires_approval` | With `require_approval_for_medium = true`, a medium-risk task returns `NeedsApproval`. | Authority-gate behavior for one configured risk threshold; not a scheduled/background parity test. |
| NanoClaw — `container/agent-runner/src/db/session-state.test.ts` | Claude and Codex continuation identifiers are stored/read from distinct provider slots; clearing Codex leaves Claude intact. | Provider-session state separation only, not agent-role memory separation. |
| Rome — `packages/core/src/actions/engine.integration.test.ts` | A child action requiring approval parks during recording; execution journal persists; replay after approval resumes the action. Separate assertions cover strict-mode replay divergence. | Approval/recovery lifecycle and action execution; no role-boundary assertion. |
| OpenGrokBot — `gateway/test/server-v021.test.ts` | A scout bot cannot stop the ticker bot's routine, while it can stop its own; database state and scheduler removal are asserted. | Direct per-bot routine ownership check. The same workflow's turn-queue test failed at this pin. |
| Engram — `crates/engram-agent/src/agent.rs` | After a read marked both untrusted and sensitive, the next egress step is refused; the egress tool did not execute; ledger sequence/hash evidence is asserted. | Strong narrow taint/egress control. It does not test the deferred real browser-adapter integration or distinct NAIA/Anna runtime homes. |

The code search index for some files pointed at later default-branch commits, so those results were not treated as pin evidence. The assertion review above uses direct file fetches at each frozen commit.

## Current execution gate

Only the Engram/Atento composition has a frozen hardened topology in the present evaluation record. Its adapter-only tests already passed 8/8. The remaining real browser-adapter/chassis integration is the explicitly pending test and remains untouched. Other candidates do not yet have frozen Atento-specific profiles/topologies satisfying the residual microprobe gate; their upstream test artifacts are reusable coverage, but cannot produce local Atento PASS/FAIL by themselves.


## OpenMausBot corrected-pin CI follow-up

The initial push query used the wrong SHA. A corrected query for `6005b1bf5883a7ffa639c07e729321f89b9532e1` found two push runs on 2026-09-29: CI (`36647214650`) and Docker image (`36647214680`), both successful. The earlier “unverified” disposition is superseded.

Observed test and smoke evidence:

- Control-plane check / workerd tests / dry run: 42 tests passed.
- Offline behavior-eval workflow: 66 tests passed across 13 files, including redaction tests. Tier 3 was intentionally kept offline in CI.
- macOS packaged-server smoke: approval mode transitions passed; HTTP elevation was rejected; private grant and resumed-mode transitions were verified. Reported app permissions were microphone allowed, camera denied, display intent-bound, and foreign origin denied.
- Paired-phone authorization smoke: real pairing succeeded; forged headers were ignored; unpaired/revoked pairing and failed bootstrap were denied; pairing survived restart.
- Packaged-server smoke passed on Ubuntu and Windows; four-shard Vitest passed on Ubuntu, macOS, and Windows.
- Docker-image boot smoke asserted the server did not bind a public interface, tested tenant-stack pairing, and checked non-root browser operation.

This is materially relevant upstream evidence for approval, origin, pairing, packaging, and bootstrap controls. It is not evidence that NAIA and Anna have independent memory, credential, tool, or channel authority, nor that cross-role handoff is broker-only.


## AI Butler exact-pin sandbox profile review

The CI log for pin `c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c` shows the race-enabled tests for `internal/permissions`, `internal/plugin/sandbox`, and `internal/shell/sandbox` passed. I also fetched those test files at the same pin and checked the actual assertions:

- `DefaultPolicy` is expected to allow network access.
- `StrictPolicy` is expected to deny network and filesystem access and cap execution at 30 seconds; the test rejects a network-capable plugin manifest under that policy.
- `ModeOff` wraps a shell command as `sh -lc`; the workspace-only and allowlist modes select OS-specific confinement wrappers.

This narrows the reusable evidence: sandbox mechanisms exist and their configuration contracts have tests, while the default plugin policy is network-permissive and `ModeOff` is not a confinement boundary. An Atento composition would need to choose and verify the strict profiles explicitly. None of these tests assert independent NAIA/Anna memory, credential, or channel authority.
