# OpenMausBot exhaustive verification — 2026-09-30

## Scope

Candidate: `milind-soni/OpenMausBot`  
Frozen pin: `6005b1bf5883a7ffa639c07e729321f89b9532e1`  
Local checkout: exact frozen pin; no source changes. Dependencies installed with `pnpm install --frozen-lockfile`.

This pass inventories the candidate's available verification, runs the safe checks supported by this Linux executor, and checks the exact-pin upstream CI matrix. It does not qualify OpenMausBot for Atento, rank it, or establish the NAIA/Anna isolation contract.

## Exact-pin upstream CI

GitHub Actions run [36647214650](https://github.com/milind-soni/OpenMausBot/actions/runs/36647214650) completed successfully at the frozen pin. All 25 jobs reported success, including:

- static typecheck, lint, locale validation, Electron syntax check, and production UI build;
- all 12 Vitest shards across Ubuntu, macOS, and Windows;
- offline behavior-eval gate;
- control-plane check, tests, and dry run;
- Ubuntu renderer smoke through `control-omb ui`;
- packaged-server smokes on Ubuntu and Windows;
- Windows CUA host smoke;
- macOS packaged-server and Electron approval/permissions/phone-pairing smokes;
- Swift tests and iOS simulator build; Kotlin tests and Android build;
- Linux ARM64 cloudflared installer;
- Ubuntu 24.04 package and installed-app smoke;
- open-source build without the enterprise layer.

The run's aggregate `CI` job also succeeded. This is broad product-test evidence on the exact source pin, including platforms unavailable in this executor. It is not an Atento composition test and does not claim per-agent memory or authority isolation.

Previously recorded exact-pin results remain applicable: the focused lending-memory, cloud-lending-memory E2E, request-auth, and session tests passed in CI; the scheduled iOS thread UI run [36647665212](https://github.com/milind-soni/OpenMausBot/actions/runs/36647665212) passed 27/27.

## Local checks completed

| Check | Result |
|---|---|
| Frozen dependency install | Pass |
| CI selection/workflow/verification-doc tests | 59/59 pass |
| Root typecheck and eval-specific TypeScript check | Pass |
| Lint | Pass |
| Locale catalogs | Pass; 10 catalogs, 2,940 English strings |
| Electron module syntax check | Pass; 145 modules |
| Production renderer build | Pass |
| Composio broker test | 10/10 pass |
| Composio broker type check | Pass |
| Electron unit tests | 509 pass, 7 skipped, 0 failed |
| Packaged-server smoke | Pass: runs outside repository `node_modules`; all 12 proxy paths, MCP stdio, encrypted backup, and enterprise layer verified |
| Control-plane check and tests | Pass; 42 tests |
| Docs production build | Pass |
| Skin contrast check | Exit 0; see known exception below |
| Live-model eval gate | Correctly skipped in offline mode; no provider instance/config was supplied |

The renderer build and docs build emitted non-fatal warnings. The docs build reported an unknown `Boat` icon and that two GitHub release responses exceeded Next.js' 2 MB cache limit; static generation still completed. The contrast checker reported two already-labelled upstream gaps for the midnight skin (accent ink 3.65:1 and danger ink 3.10:1); its other listed themes passed their target pairs.

## Local integration-suite limitation

The full local `pnpm test` run did not complete. Its real-server fixtures hit a runner restriction: binding a Unix-domain permission-broker socket returns `EPERM` (for example, `permission broker unavailable ... listen EPERM: operation not permitted .../omb-perm-....sock`). Once this shared fixture dependency fails, server integration assertions and eval scenarios time out because no scripted turn is recorded. I stopped the long run after confirming the same error in fixture logs; do not interpret those cascading assertion failures as candidate regressions.

The eval Vitest gate reported 58 passing and 8 failing tests; Tier 1 and golden scenario runs also failed after the fixture could not start its broker socket/record turns. This executor-specific result conflicts with the exact-pin upstream behavior-evals job, which passed. Reproducing those suites locally requires a runner that permits the fixture's AF_UNIX socket operations.

The standalone broker, Electron, packaged-server, and control-plane checks were then run separately and passed as listed above.

## Not run locally

These are environment/configuration limits, not unresolved failures in the exact-pin CI:

- macOS/Windows host behavior, iOS/Android build environments, and Ubuntu-installed package lifecycle were covered by upstream exact-pin jobs, but cannot be recreated on this Linux executor.
- Human visual review and renderer-only surfaces not mapped by `control-omb ui` remain unverified here: Settings, sidebar drag-and-drop, VM modal, built-in browser panel, updater UI, and broader visual/layout judgment. The verification guide explicitly distinguishes these from the accessible-name-driven chat UI fixture.
- Live-model evals require an explicitly supplied test instance and credentials. The safe default is offline, and this pass confirmed that it skipped.
- Local real-server integration/eval reproduction is blocked by the executor's AF_UNIX restriction described above.

## Atento-specific open gate

The candidate's upstream tests and green CI do not establish the target Atento property: three distinct agents operating as isolated silos, with private memory/tools and only a narrow, sanitized message path. In particular, they do not prove NAIA-versus-Anna isolation for two bots belonging to one OpenMausBot owner, or broker-only handoff in the intended Atento composition. The real Engram → adapter/browser chassis integration remains **PENDING** as recorded in the prior Atento audit.

Before treating this candidate as passing the Atento chassis, the next substantive gate is to define and run those composition-level adversarial cases on an executor that supports the required fixtures. Until then, classify OpenMausBot as **upstream CI PASS; Atento isolation NOT ESTABLISHED**.
