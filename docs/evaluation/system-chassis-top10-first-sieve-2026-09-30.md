# System chassis Top 10 — first sieve — 2026-09-30

## Result and ordering rule

This is a ranked measurement-priority queue for the first stage (architecture + chassis), updated from existing Atento reports. It is not a Top 10 of lowest-cost candidates and not a selection result.

Ordering uses transferability of existing architecture/chassis evidence, amount of observed evidence, direct relevance to the three-agent system, and pin readiness. It does not rank by price, safety, or overall quality. No benchmark was rerun and no value was recalculated.

ORDERING = FIRST_SIEVE_MEASUREMENT_PRIORITY
CFS_COMPARABLE_TOP10 = 0/10
COMPARABLE_THREE_ROLE_TOTAL_COST = 0/10
SYSTEM_DENOMINATOR = NOT_YET_FORMED
WINNER = NONE

## Ranked first-sieve table

| Priority | Candidate | Frozen source pin | Existing result / note | First-stage architecture + chassis interpretation | Later gate / missing comparable metric |
|---:|---|---|---|---|
| 1 | NanoClaw | nanocoai/nanoclaw@4c1eabd3ddd74cc3d71b1871da857391a9411c8d | Exact-pin core CI: 513 pass / 0 fail per Node matrix (3 skipped); Node 22/24 and Iron front race gate passed. Run-backed group control-plane and state-mount isolation, credential-config guards: PASS_WITH_SCOPE. Partial static recipes: WhatsApp 4 files / 1 import touchpoint / 4 deps; OneCLI 8 / 1 / 1 SDK; OpenCode 40 / 5 / 1 SDK plus manifest/build. | Strongest combined evidence here for a small-group/container architecture and profile-specific change surface. Change cost is demonstrably profile-dependent. CFS: ND. Full adaptation/maintenance cost: NOT_MEASURED. | These upstream tests do not prove a three-role Atento composition. Atento cross-role composition and real gateway non-disclosure remain NOT_RUN. |
| 2 | AI Butler | LumabyteCo/aibutler@c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c | Exact-pin functional/race/security-integration CI and run-backed bank-isolation/scheduler tests exist. Accepted Atento Gate-2 result: 6/6 common assertions PASS_WITH_SCOPE. Frozen pin later has a current scheduled security scan FAIL with seven reachable advisories; no repaired pin/regression run exists. | Best existing role-bank and capability-scoped scheduler evidence. This is a bounded runtime composition result, not total-cost evidence. CFS: ND. Adaptation/maintenance cost: NOT_MEASURED. | Security is a separate later gate and currently blocks this pin. Atento full NAIA/Anna/Apollo composition remains NOT_RUN; exact-pin identity-to-bank binding needs proof. |
| 3 | OpenClaw | openclaw/openclaw@e9571d77e76bd6d35996273d9e8398ad539b26e1 (NAIA qualification pin) | Exact-pin source/tests support strong per-agent core-state isolation and mature Gateway/runtime mechanisms. The audit says cross-agent session isolation is not default and strict Therapy separation requires a separate runtime/Gateway. Hosted CI at the inspected qualification pin was not observable. | Viable separate-runtime architecture signal; shared-Gateway agent count alone does not satisfy the strict role boundary. No comparable profile change-surface or total-cost value. | Compose separate role runtimes/stores and test credential, tool, scheduler/recovery, and handoff boundaries. |
| 4 | QwenPaw | agentscope-ai/QwenPaw@777441721aa72db8e380d90e4d0481b05cbfd4cc | Exact-pin static audit: per-agent memory/policy isolation is strong; session authority fails closed. Sandbox-unavailable fallback can fail open; cron authority needs hardening. At the pin, E2E smoke, frontend and pre-commit jobs succeeded; main Tests was waiting and Full Tests Nightly failed. | Strong state/policy primitives but hardening/configuration is part of the chassis adaptation. No comparable system change-surface or total-cost value. | Prove sandbox-unavailable denial and background authority; transfer only after exact frozen pin and test profile are reconciled. |
| 5 | MindRoom | mindroom-ai/mindroom@4f3bd2d108a6f9be28174e0f66d78eeecddca386 | Exact-pin source review confirms per-agent config and canonical state roots, but the pinned worker-runtime plan explicitly says agent-isolated filesystem visibility is incomplete for shared-runner/local paths; dedicated Kubernetes workers narrow mounts for selected scopes. No Atento execution or benchmark result. | Direct integrated-platform signal with a material isolation/integration seam already identified. CFS, Atento source tests, change surface and total cost: ND. | Validate exact-pin implementation, API path, delegated handoff, background authority and deployment burden. |
| 6 | Bob Labs | boblabs-eu/boblabs@a91d6dad098c8ba6d24436a856556078151db45d | Exact-pin source review found test definitions for user-visible lab scoping, explicit shared-memory confirmation, HMAC/nonce sandbox authentication, and encrypted provider/MCP secrets. These files were inspected but not run in this review. | Direct system-level architecture signal, but source/release notes are not independent enforcement tests. CFS, Atento tests, change surface and total cost: ND. | Probe bus payload boundaries, role isolation within/across Labs, and service/update burden. |
| 7 | Ontheia | Ontheia/ontheia@70802db61eb16533f55efce3d8785d810223d03b | Pinned docs describe per-agent tools/memory/skills, scheduling, delegation, RBAC and PostgreSQL RLS. | Direct system-level role topology signal; RLS/memory claims are not yet shown at Atento domain scope. CFS, Atento tests, change surface and total cost: ND. | Test agent/domain-level RLS, delegation minimization, background authority, and operational/update burden. |
| 8 | OpenAkita | openakita/openakita@5f5b38da728274f0fd06461a481851be7c0bca6a | Exact pin and license recorded. Upstream documents multi-agent use, scheduling, tools/computer and advertised sandbox layers. | Integrated-platform signal, with isolation still a source claim. CFS, Atento tests, change surface and total cost: ND. | Verify per-agent state/secrets/tools, handoff and actual sandbox boundary. |
| 9 | Clawix | ClawixAI/clawix@5aee015e0bd793102fba69af486dd6e75df6d802 | Exact pin recorded. README claims per-agent Docker containers, scoped memory, RBAC, approvals, persistent workspaces and audit; MIT badge was not independently confirmed by the LICENSE path at the pin. | Container isolation claim is relevant, but implementation and terms evidence remain incomplete. CFS, Atento tests, change surface and total cost: ND. | Verify code/tests, private versus group/org memory, and Docker/warm-pool/update burden. |
| 10 | Memoh | NOT_FROZEN (README blob df463bf149d14483ce388ae89cfcb3b5dde9be90) | README-level claims cover per-agent workspace/computer/filesystem/browser/network/memory and separate or all-in-one deployments. Exact commit is not frozen. | Potentially broad role runtime surface, currently discovery-only. CFS, Atento tests, change surface and total cost: ND. | Freeze exact commit before it can enter a pinned comparison; then inspect authority boundaries and deployment surface. |

## Applied first-sieve status from existing Atento evidence

| Candidate group | First-sieve disposition | Why |
|---|---|---|
| NanoClaw, AI Butler, OpenClaw, QwenPaw | ADVANCE_WITH_SCOPE for their prior NAIA chassis screen; not a system-level pass. | Existing exact-pin structural and/or runtime evidence can be reused only for the inspected mechanisms. Three-role composition cost and all system assertions remain open. |
| MindRoom, Bob Labs, Ontheia, OpenAkita, Clawix | DISCOVERY_ONLY; eligible for exact-pin architecture/chassis screening. | The Atento record contains repository/pin claims and unresolved questions, but no Atento CFS, change-surface measurement, or composition test. |
| Memoh | PIN_REQUIRED before first-sieve qualification. | The inspected README is not tied to a frozen commit. |

Later-gate evidence must remain visible without changing the first-sieve label: AI Butler's six common Gate-2 assertions passed with scope, but its frozen pin has a current scheduled security failure; QwenPaw has an unresolved fail-open sandbox fallback path; OpenClaw requires separate runtime/Gateway boundaries for strict NAIA/Anna separation. NanoClaw's upstream gates and isolation mechanisms pass with scope, but the Atento cross-role composition is not run.

## Existing numeric notes outside the ranked ten

| Source result | Existing metric | Transfer limit |
|---|---|---|
| PsyChat upstream | CFS 10/100; routing boundary only; explicit extension seams 0/5; 3 donor files for provider/lifecycle and 4 for the full correction; 1,410/1,600 lines retained (88.125%). | Anna/RAG-specific structural adaptation evidence, not a system-platform score. |
| Letta prototype | 0 core imports/host-core changes; bounded general/therapeutic policy isolation, RAG outage and removal passed; 7 sequential mutations; final regression passed. | Historical isolated overlay fixture, not complete Atento role/credential/handoff qualification. |
| LibreChat control | 0 core imports; bounded WhatsApp/memory/policy/outage checks passed; 8 mutations; final regression passed. | Historical adapter control, not a whole-system result. |

## Current first-stage conclusion

The strongest existing architecture/chassis evidence among the ten is for specific mechanisms: NanoClaw's group/container and credential guard paths; AI Butler's bank isolation and scoped scheduler; and OpenClaw's per-agent runtime state plus separate-Gateway route. Their limits differ, so they do not yet share one complete-system denominator.

The numerical data are partial: NanoClaw touchpoints count files/dependencies for different recipes, while the Letta/LibreChat numbers count mutations in separate prototypes. PsyChat's CFS is Anna/RAG-scoped. None is a comparable total adaptation-and-maintenance cost for the complete Atento architecture. AI Butler's Gate-2 PASS_WITH_SCOPE is retained, alongside its separate current security failure; the pass does not override that later gate.

Thus this is the ranked queue for applying the first sieve, not ten comparable scores or a low-cost ranking. Missing evidence remains unresolved; no system candidate is eliminated by this table.

## Canonical evidence

- Whole-product contract and new system candidates: docs/evaluation/atento-system-architecture-chassis-rescreen-2026-09-30.md
- Existing benchmark-to-metric mapping: docs/evaluation/system-chassis-benchmark-crosscheck-2026-09-30.md
- NAIA Gate-1 source screen: docs/evaluation/naia-architecture-gate1-screen-2026-09-30.md
- AI Butler exact-pin evidence: docs/evaluation/aibutler-exhaustive-verification-2026-09-30.md and docs/evaluation/naia-gate2-chat-results-2026-10-01.md
- NanoClaw exact-pin evidence: docs/evaluation/nanoclaw-exhaustive-verification-2026-09-30.md and docs/evaluation/nanoclaw-change-surface-audit-2026-09-29.md
- OpenClaw evidence: docs/evaluation/openclaw-qualification-2026-09-29.md
- QwenPaw evidence: docs/evaluation/qwenpaw-contract-audit-2026-09-29.md
- Historical PsyChat/Letta/LibreChat measurements: docs/evaluation/donor-candidate-comparison-research-2026-09-29.md and docs/evaluation/chassis-selection-research-2026-09-29.md
