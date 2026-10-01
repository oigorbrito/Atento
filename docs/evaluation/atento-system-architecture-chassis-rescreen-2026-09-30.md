# Atento system-level architecture/chassis re-screen — 2026-09-30

## Purpose and scope reset

This record corrects the scope of the previous architecture/chassis test. The Gate-1 result and cost Top 5 were explicitly **NAIA candidate-base** work; they did not test or select the product-wide chassis for NAIA, Anna, and Apollo.

The Atento selection object is now the **complete product composition**. NAIA remains the primary personal assistant and general operational executor; Anna owns the therapeutic/emotional domain; Apollo owns fitness/nutrition and is deferred. Apollo's product domain and future isolation boundary still constrain the system architecture even though Apollo-specific functional chassis research remains deferred.

```text
FIRST_SYSTEM_SELECTION_METRIC = TOTAL_ADAPTATION_AND_ONGOING_MAINTENANCE_COST
MEASUREMENT_OBJECT = ATENTO_SYSTEM_ARCHITECTURE_AND_CHASSIS
PRODUCT_DOMAINS = [NAIA, Anna, Apollo]
APOLLO_FUNCTIONAL_CHASSIS_RESEARCH = DEFERRED
NAIA_ROLE_TOP5 = ROLE_SPECIFIC_ONLY
SYSTEM_CHASSIS_WINNER = NONE
SYSTEM_CHASSIS_SHORTLIST = NOT_SELECTED
```

The old 26-candidate screen remains valid for its documented NAIA scope and as component-level evidence. Its 25 advances are **not** 25 system-level passes; its one SelfAgent stop remains a stop for the complete NAIA base at that frozen pin. No candidate is newly eliminated by this scope reset.

## Product-level architecture contract to screen

The comparison must cover a composition that can host the product's three independent domains. A platform need not use one agent runtime for all three; the architecture may use a shared platform, separate specialist chassis, or a hybrid.

Required invariants:

- Separate chat/session identity, memory authority, tool authority, credentials, and persistent state for NAIA, Anna, and future Apollo.
- NAIA's general operational tools do not become inherited authority for Anna or Apollo.
- Each specialist owns decisions and data in its domain.
- Cross-domain actions use an explicit, minimal, auditable handoff; the receiver executes under its own authority. Sensitive transfer follows an explicit consent policy.
- Scheduled, retry, recovery, and delegated execution preserve the same or narrower role authority as interactive execution.
- Shared infrastructure is allowed only where its data and authority boundaries are explicit. Shared platform does not imply shared private memory or credentials.
- Apollo can be added later without requiring a cross-cutting rebuild, but no Apollo-specific candidate or feature set is selected here.

## Architecture alternatives — all remain open

| Alternative | Description | Cost/risk to measure |
|---|---|---|
| Integrated multi-agent platform | One platform/control plane hosts the three agents with per-agent boundaries. | Cost to configure and prove per-agent state/tool/credential isolation; blast radius and upgrade coupling. |
| Composed specialist chassis | Separate role-appropriate systems integrated through a narrow Atento broker/control plane. | Duplicate operations, adapters, lifecycle and updates; explicit handoff and observability cost. |
| Hybrid | Shared identity/routing/audit/UI services with isolated role runtimes and state stores; specialist chassis may differ by role. | Boundary complexity, duplicated components, shared-service authority, and total upkeep. |

These are test alternatives, not a decision that one style is inherently cheaper or safer.

## Reused evidence versus new screening

- Reuse the NAIA Gate-1 exact-pin findings only for the properties and candidate pins they actually inspected.
- Reuse the Anna candidate audit for Anna-domain functional chassis only; it does not establish product-wide integration or cross-agent authority.
- Apollo remains deferred as a functional base search, but its future-domain boundary is included in the system-level architecture contract.
- Run no redundant broad upstream suites. For each exact pin, inspect only missing system-level seams: identity/state ownership, handoff mediation, credential/tool grants, background authority, recovery, and expected integration/update burden.
- Distinguish source claims, source tests, executed tests, and Atento composition evidence. Repository marketing text is discovery signal, not proof.

## GitHub discovery sweep — preliminary candidates

Search date: 2026-09-30 local time. This is a discovery and static pre-triage pass. Items below are not benchmarked, installed, or accepted. Pins are recorded where the GitHub commit search returned one; where only a branch README was retrieved, the exact commit remains to be frozen before testing.

| Repository / inspected pin | System-level signal | Main unresolved architecture/cost question | Preliminary class |
|---|---|---|---|
| [MindRoom](https://github.com/mindroom-ai/mindroom/tree/4f3bd2d108a6f9be28174e0f66d78eeecddca386) `4f3bd2d108a6f9be28174e0f66d78eeecddca386` | Multi-agent Matrix runtime; agent accounts, teams, durable sessions, tools, memory and explicit delegation. Its docs define `user_agent` worker scope for per-agent filesystem isolation and describe dedicated Docker/Kubernetes workers. | The `user` worker scope intentionally shares a runtime/workspaces across that user's agents; select and test `user_agent`/dedicated workers. Matrix and worker deployment/operations may add cost. Delegation and credentials need Atento-specific tests. | SYSTEM_CHASSIS_CANDIDATE_FOR_PINNED_SCREEN |
| [Ontheia](https://github.com/Ontheia/ontheia/tree/70802db61eb16533f55efce3d8785d810223d03b) `70802db61eb16533f55efce3d8785d810223d03b` | Self-hosted platform with specialist agents, per-agent tools/memory/skills, workflows, scheduling, direct agent delegation, RBAC and PostgreSQL RLS. | RLS and memory namespaces must be checked at agent/domain scope, not inferred from user tenancy. Test direct delegation payload and credentials, update and deployment burden. | SYSTEM_CHASSIS_CANDIDATE_FOR_PINNED_SCREEN |
| [Bob Labs](https://github.com/boblabs-eu/boblabs/tree/a91d6dad098c8ba6d24436a856556078151db45d) `a91d6dad098c8ba6d24436a856556078151db45d` | Persistent multi-agent labs; each agent has model/memory/tool grants; typed event bus; per-Lab sandbox and self-hosted services. The inspected release notes include fixes to fail-closed sandbox HMAC and shell allow-list handling. | Determine whether role domains require separate Labs, how the bus shares data, what remains trusted inside a Lab, and whether its service/GPU stack raises total upkeep. Release-note fixes are not independent proof. | SYSTEM_CHASSIS_CANDIDATE_FOR_PINNED_SCREEN |
| [Clawix](https://github.com/ClawixAI/clawix/tree/5aee015e0bd793102fba69af486dd6e75df6d802) `5aee015e0bd793102fba69af486dd6e75df6d802` | Multi-agent orchestration claims per-agent Docker containers, scoped memory, RBAC, approvals, persistent workspaces, audit, and provider flexibility. | Verify isolation in code/tests; distinguish private per-agent memory from group/org sharing; measure Docker and warm-pool operations and Atento handoff adaptation. | SYSTEM_CHASSIS_CANDIDATE_FOR_PINNED_SCREEN |
| [Memoh](https://github.com/felinics/Memoh) — branch README inspected; exact commit not frozen | Self-hosted multi-agent platform; per-agent workspace/computer, filesystem, browser, network and long-term memory; supports separate server/channel deployment and also an all-in-one mode. | Freeze exact commit; prove credential, network, memory, and cross-agent boundaries; determine which components require Docker and the cost of always-on computers. | SYSTEM_CHASSIS_CANDIDATE_FOR_PINNED_SCREEN |
| [OpenAkita](https://github.com/openakita/openakita/tree/5f5b38da728274f0fd06461a481851be7c0bca6a) `5f5b38da728274f0fd06461a481851be7c0bca6a` | All-in-one assistant with multiple agents, scheduling, tools, browser/computer use, desktop/web/mobile interfaces, and advertised sandbox layers. | Verify per-agent state, secrets, tool authority, handoff semantics, and what the advertised sandbox actually isolates. | SYSTEM_CHASSIS_CANDIDATE_FOR_PINNED_SCREEN |
| [OpenClaw](https://github.com/openclaw/openclaw) — reuse the frozen Atento candidate pin | Existing NAIA candidate supports multiple agents in one Gateway with per-agent workspace, state and session stores. | Transfer is partial: test three role scopes, shared Gateway blast radius, credential fallback behavior, scheduler, and explicit handoff. Do not treat its NAIA evidence as system evidence. | CARRYOVER_SYSTEM_COMPOSITION_PROBE |
| [QwenPaw](https://github.com/agentscope-ai/QwenPaw/tree/80e412da9b5505bcac5eec6add271d09fa144c60) `80e412da9b5505bcac5eec6add271d09fa144c60` | Existing NAIA candidate with per-agent resources/governance/sandbox and MCP/A2A/ACP seams in current upstream descriptions. | Transfer exact pin to three role domains, verify sandbox fallback and cron authority, and measure composition/upkeep. | CARRYOVER_SYSTEM_COMPOSITION_PROBE |
| [Asterism](https://github.com/qmilab/asterism/tree/a8383b45f64a9a9c1923053b0f3894efb4672aba) `a8383b45f64a9a9c1923053b0f3894efb4672aba` | Explicit per-agent memory, secrets, workspace, autonomy and consented one-way agent connections. | Its own documentation says current separation is logical, not hardened containment. Keep as architecture/donor reference unless an external runtime boundary is proven. | ARCHITECTURE_REFERENCE_ONLY_AT_CURRENT_PIN |
| [AgentSpace](https://github.com/HKUDS/AgentSpace/tree/0f9da1b125def4d5a0d05b34bf7c5cec0686bbf2) `0f9da1b125def4d5a0d05b34bf7c5cec0686bbf2` | Multi-user collaborative workspace, access control, remote daemon and runtime support. | Its README lists multi-agent isolation and sandbox policy as planned, not implemented; do not count it as satisfying the current hard boundary. Keep on watch/reference. | NOT_ADMITTED_AS_CURRENT_SECURITY_CHASSIS |

This list expands the horizon; it is not an ordered Top 5. Other members of the prior 26-candidate NAIA universe remain uneliminated from system-level consideration until re-screened or stopped by exact evidence.

## Preliminary screen result

```text
OLD_NAIA_GATE1 = VALID_FOR_NAIA_SCOPE_ONLY
OLD_NAIA_GATE1_SYSTEM_LEVEL_PASSES = 0_CLAIMED
NEW_SYSTEM_PLATFORM_DISCOVERY_CANDIDATES = [MindRoom, Ontheia, Bob Labs, Clawix, Memoh, OpenAkita]
CARRYOVER_COMPOSITION_PROBES = [OpenClaw, QwenPaw]
ARCHITECTURE_REFERENCES = [Asterism, AgentSpace]
NEW_TECHNICAL_ELIMINATIONS = 0
FULL_ATENTO_SYSTEM_COMPOSITION_TESTS = 0
COMPARABLE_SYSTEM_TOTAL_COST_MEASUREMENTS = 0
SYSTEM_CHASSIS_WINNER = NONE
SYSTEM_CHASSIS_SHORTLIST = NOT_SELECTED
```

This is a discovery/static evidence pass, not an executed Atento architecture test. No repository claim or source test alone proves separation of Atento chats, memory, tools, credentials, or handoffs.

## Next execution sequence

1. Freeze one Atento system-level acceptance profile from ADR-001: three domain identities, private state/tool/credential stores, NAIA operational-executor boundary, explicit minimal handoff, audit/consent, scheduler/recovery parity; retain Apollo's domain now but defer its feature-base search.
2. Preserve the three topology alternatives above and map the candidate projects onto them. Reconcile the full previous 26-candidate universe against the new system contract; do not just rename the old NAIA Top 5.
3. Pin exact commits for every admitted candidate, starting with the six new platform candidates plus OpenClaw/QwenPaw carryovers. For each, run the smallest source/test probe that establishes multi-agent state ownership and background/tool authority. Stop only for demonstrated hard failures; record missing/blocked evidence separately.
4. Build one reproducible three-role negative composition harness. At minimum test cross-role chat/history, memory, secrets, tools, scheduler/recovery, explicit handoff payload limits, and recipient-side authorization.
5. Capture total adaptation and maintenance cost during equivalent compositions: file changes, dependency/update surface, independent runtime/control paths, deployment requirements, engineering time/rework, and ongoing operations. Do not form a numerical ranking before comparable observations exist.
6. Only after the system screen closes, define a system-level measurement cohort/Top 5. The prior OpenClaw/AI Butler/NanoClaw/QwenPaw/Letta Code cohort remains NAIA-role-specific.

## Evidence/source hierarchy

- Product role boundaries and open topology: `docs/adr/ADR-001-naya-product-composition.md`.
- NAIA role-specific screen and cost records: `docs/evaluation/naia-architecture-gate1-screen-2026-09-30.md`, `docs/evaluation/naia-architecture-chassis-maintenance-cost-audit-2026-09-30.md`, and the NAIA Top 5 record.
- Exact repository docs and code at listed commits; source claims are not runtime proof.
- Atento three-role composition artifacts and independent verification, once executed.

## Primary GitHub sources

- MindRoom: `https://github.com/mindroom-ai/mindroom/tree/4f3bd2d108a6f9be28174e0f66d78eeecddca386/docs/configuration/agents.md`; `.../docs/deployment/sandbox-proxy.md`; `.../docs/dev/persistent-worker-runtime-plan.md`.
- Ontheia: `https://github.com/Ontheia/ontheia/tree/70802db61eb16533f55efce3d8785d810223d03b`.
- Bob Labs: `https://github.com/boblabs-eu/boblabs/tree/a91d6dad098c8ba6d24436a856556078151db45d`.
- Clawix: `https://github.com/ClawixAI/clawix/tree/5aee015e0bd793102fba69af486dd6e75df6d802`.
- Memoh: `https://github.com/felinics/Memoh` (exact commit pending).
- OpenAkita: `https://github.com/openakita/openakita/tree/5f5b38da728274f0fd06461a481851be7c0bca6a`.
- Asterism: `https://github.com/qmilab/asterism/tree/a8383b45f64a9a9c1923053b0f3894efb4672aba`.
- AgentSpace: `https://github.com/HKUDS/AgentSpace/tree/0f9da1b125def4d5a0d05b34bf7c5cec0686bbf2`.
- OpenClaw and QwenPaw: exact candidate pins are in the existing Atento NAIA evidence records; retain those pins rather than current branch heads.
