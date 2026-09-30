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
| OpenClaw | `ca8f24d05fc49a224adab0c9426077fd8d93801d` | CI, CodeQL, workflow sanity, dispatch succeeded; cache-warm skipped. [Runs](https://github.com/openclaw/openclaw/actions) | Green observed workflows; no isolation proof. |
| OpenMausBot | `6005b1bf5883a7ffa639c07e729321f89b9532e1` | Corrected SHA: PR-trigger query returned none. Push result not verified due to initial wrong-SHA query. A Vercel status on the candidate had been observed separately. | **Unverified** in this battery; do not infer no tests or pass. |
| QwenPaw | `777441721aa72db8e380d90e4d0481b05cbfd4cc` | Frontend, pre-commit, CodeQL, E2E smoke, formatting succeeded; Tests workflow remains waiting at Maintainer Approval. [Waiting run](https://github.com/agentscope-ai/QwenPaw/actions/runs/36559841525) | Partial green; core Tests run is pending approval, not a failure. |
| AI Butler | `c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c` | CI and Security succeeded. | Green observed workflows; no isolation proof. |
| NanoClaw | `4c1eabd3ddd74cc3d71b1871da857391a9411c8d` | CI and registry-skills workflows succeeded. | Green observed workflows; no isolation proof. |
| TrustClaw | `c07410bccb916236b45b563e8c4ff76ad83d3855` | No push or PR-triggered runs observed at the pin. | No run observed; functional test coverage unknown. |
| Open Assistant | `32c55d2643f9fe38777f9212588b2eee45392514` | Release workflow succeeded. | Release workflow only; not a functional test result. |
| Rakazo | `f4583525d632fcd8643fd6e24c7f51e3e04cb990` | CI failed in Playwright E2E; typecheck, lint, production build, Electron smoke, Postgres journeys, and unit tests succeeded. Failed case produced a mismatched UI value and scripted agent-run failures. [Run](https://github.com/elie222/rakazo/actions/runs/36619326151) | Concrete E2E gap; not specifically an isolation test. |
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
