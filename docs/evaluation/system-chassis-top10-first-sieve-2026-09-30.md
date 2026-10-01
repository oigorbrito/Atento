# System chassis Top 10 — first sieve — 2026-09-30

## Result type

This is a ranked measurement-priority queue for the first stage (architecture + chassis), using existing Atento notes and static source evidence. It is not a Top 10 of lowest-cost candidates and not a selection result.

ORDERING = FIRST_SIEVE_MEASUREMENT_PRIORITY
BASIS = SYSTEM_BOUNDARY_RELEVANCE + EXISTING_EVIDENCE_MATURITY + PIN_READINESS
CFS_COMPARABLE_TOP10 = 0/10
COMPARABLE_THREE_ROLE_TOTAL_COST = 0/10
SYSTEM_DENOMINATOR = NOT_YET_FORMED
WINNER = NONE

No benchmark was rerun and no values below were recalculated. “Not measured” is a real result state. Existing values retain their original candidate scope and protocol.

## Ranked measurement-priority table

| Priority | Candidate / composition source | Existing architecture/chassis result or note | Mapping to Atento first-stage metrics | Main unresolved item before it can enter a comparable denominator |
|---:|---|---|---|---|
| 1 | MindRoom, integrated multi-agent platform | Exact discovery pin recorded. Agent identities/teams, durable sessions, tools, memory, delegation, and worker scopes are documented. Its user worker scope shares workspaces; user_agent/dedicated workers are the relevant isolation option. | Strong direct system-architecture relevance; per-agent worker isolation seam identified. CFS: ND. Change surface: ND. Total cost: ND. | Verify identity/state/credential/tool boundaries at the pinned code/test level; test delegated handoff and background authority; measure deployment and adaptation surface. |
| 2 | Bob Labs, integrated multi-agent labs | Exact pin recorded. Per-agent model/memory/tool grants, typed event bus, per-Lab sandbox and self-hosted services are documented; release notes include security fixes. | Direct system-level grants/handoff signal. CFS: ND. Change surface: ND. Total cost: ND. | Test actual boundary enforcement, what crosses the event bus, role separation within/across Labs, and service/upgrade burden. |
| 3 | Ontheia, integrated multi-agent platform | Exact pin recorded. Per-agent tools/memory/skills, scheduling, direct delegation, RBAC and PostgreSQL RLS are documented. | Direct role topology and delegation signal. CFS: ND. Change surface: ND. Total cost: ND. | Prove RLS/memory separation at agent/domain scope and minimal handoff; measure deployment/update surface. |
| 4 | OpenClaw, multi-agent Gateway composition | Existing NAIA candidate evidence describes per-agent workspace, state and session stores in one Gateway. | Reusable role-runtime evidence; potential shared-control-plane composition. System CFS: ND. System change surface/cost: ND. | Reuse only the exact frozen Atento pin; test three-role isolation, shared Gateway blast radius, credential fallback, scheduler/recovery, and explicit handoff. |
| 5 | QwenPaw, multi-agent assistant composition | Existing NAIA evidence describes per-agent resources/governance/sandbox and MCP/A2A/ACP seams. | Reusable per-agent control signal. System CFS: ND. System change surface/cost: ND. | Resolve the canonical qualification pin; transfer the evidence to three role domains; test sandbox fallback, cron authority, and deployment burden. |
| 6 | AI Butler, persistent-agent composition | Existing audit records per-bank memory, fail-closed shell, credential broker and scheduler as usable seams. | Relevant authority and background-execution architecture signal. System CFS: ND. System change surface/cost: ND. | Compose role/bank boundaries and execute scheduler/recovery under the same grants; count adaptation and upkeep. |
| 7 | NanoClaw, group/container assistant composition | Existing static recipes: WhatsApp 4 files / 1 import-index touchpoint / 4 dependencies; OneCLI 8 / 1 / 1 SDK; OpenCode 40 / 5 / 1 SDK plus manifest/build touchpoints. | Only existing quantified partial change-surface data among these role-oriented carryovers. It is profile-dependent and NAIA-scoped. CFS: ND. Total cost: not measured. | Freeze one complete three-role profile; test cross-role isolation and credential gateway; do not treat file counts as hours or maintenance cost. |
| 8 | OpenAkita, integrated multi-agent assistant | Exact pin recorded. Multiple agents, scheduling, tools, computer use and advertised sandbox layers are documented. | System-level platform signal. CFS: ND. Change surface: ND. Total cost: ND. | Verify per-agent state, secrets, tool grants, handoff and sandbox behavior; measure operational/update footprint. |
| 9 | Clawix, containerized multi-agent orchestration | Exact pin recorded. Upstream claims per-agent Docker containers, scoped memory, RBAC, approvals, workspaces and audit. | System-level isolation claims with container boundary. CFS: ND. Change surface: ND. Total cost: ND. | Prove claims in code/tests; resolve private vs group/org memory scope; measure Docker/warm-pool and update burden. |
| 10 | Memoh, self-hosted multi-agent platform | README-level evidence describes per-agent workspace/computer/filesystem/browser/network/long-term memory and separate or all-in-one deployments; exact commit is not frozen. | Potentially broad per-agent runtime boundary. CFS: ND. Change surface: ND. Total cost: ND. | Freeze exact commit first; then test credential/network/memory boundaries and deployment cost. Until pinned, it is not executable comparison evidence. |

## Existing numeric notes outside this Top 10

These are preserved as component/control evidence, not silently inserted into the system ranking:

| Existing source result | Original metric | Correct use in the first sieve |
|---|---|---|
| PsyChat upstream | CFS 10/100; routing boundary only; explicit extension seams 0/5; 3 donor files for provider/lifecycle, 4 for full current correction; 1,410/1,600 lines retained (88.125%). | Anna/RAG-specific structural adaptation evidence. Not a system platform CFS, not a three-agent isolation score, and not total cost. |
| Letta prototype | 0 core imports and host-core files changed; bounded general/therapeutic policy isolation, RAG outage, and removal passed; 7 sequential mutations; final regression passed. | Historical adapter/evolvability control. Useful method evidence, not a complete multi-agent system candidate measurement. |
| LibreChat control prototype | 0 core imports; bounded WhatsApp adapter, memory/policy isolation and outage tests passed; 8 mutations; final regression passed. | Historical control for extension and bounded isolation. Not a whole Atento role/credential/handoff result. |

## What the ordering means

- Ranks 1–3 are integrated platforms with explicit multi-agent and per-agent architecture signals.
- Ranks 4–7 reuse already-screened assistant candidates where Atento has role-specific evidence; that evidence still needs system transfer.
- Ranks 8–10 complete the new system-platform discovery set. Memoh is last in execution priority only because its exact pin is unresolved, not because a failure was found.
- The ordering is for efficient evidence acquisition and first-stage comparison. It does not imply that rank 1 is cheaper, safer, or selected.

## Current first-stage measurement outcome

The only defensible quantitative findings relevant to the first stage are partial and scoped to other tasks: PsyChat's Anna/RAG structural audit, NanoClaw's NAIA recipe touchpoints, and Letta/LibreChat prototype change/evolution notes. The six newly discovered system platforms have no Atento CFS, change-surface measurement, or total-cost measurement in the existing records. The other role-candidate signals are static source findings.

Therefore the current Top 10 is a ranked queue for applying the first sieve, not ten comparable scores. The complete-product common denominator remains empty until comparable architecture/chassis evidence is available. Candidates with missing evidence remain unresolved, not eliminated.

## Canonical evidence

- Whole-product contract and discovery pins: docs/evaluation/atento-system-architecture-chassis-rescreen-2026-09-30.md
- Existing numeric and qualitative result mapping: docs/evaluation/system-chassis-benchmark-crosscheck-2026-09-30.md
- NAIA static cost audit: docs/evaluation/naia-architecture-chassis-maintenance-cost-audit-2026-09-30.md
- NanoClaw change-surface results: docs/evaluation/nanoclaw-change-surface-audit-2026-09-29.md
- PsyChat/Letta/LibreChat historical evidence: docs/evaluation/donor-candidate-comparison-research-2026-09-29.md and docs/evaluation/chassis-selection-research-2026-09-29.md
