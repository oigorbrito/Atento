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

The comparison unit is an **Atento composition**: platform/control plane + role-specific runtimes + state/credential/tool boundaries + handoff mechanism + deployment/update model. A GitHub repository is a source/component candidate, not automatically a complete system candidate. A platform need not use one agent runtime for all three; the architecture may use a shared platform, separate specialist chassis, or a hybrid. This is an architecture trade-off evaluation against named product qualities, consistent with the SEI ATAM method; it does not assume a universal winner among shared and distributed styles.

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

## Ordered screening and common denominator

Selection is staged, with architecture and chassis assessed together first:

1. **Architecture + chassis:** screen structural fit against the Atento role boundaries, then measure the combined adaptation and ongoing-maintenance cost for a fixed capability profile. Keep structural signals (such as CFS, touchpoints, and change locality) distinct from observed engineering time and lifecycle expense.
2. **Other metric families:** apply declared metrics in sequence to the remaining comparable candidates: functional quality, safety, isolation, reliability/recovery, latency, and operational cost as applicable.
3. **Common denominator:** carry forward only candidates with an equivalent declared scope/profile and comparable evidence for each metric required at the current stage, while meeting hard gates. Track missing/blocked evidence as unresolved, not failed.
4. **Selection:** compare the surviving set on the predeclared objective. Do not combine unlike stage notes into a synthetic aggregate.

The benchmark cross-check maps existing results to this first sieve only where their original scope transfers. Those results do not yet form a comparable denominator for the complete NAIA–Anna–Apollo system.

## Reused evidence versus new screening

- Reuse the NAIA Gate-1 exact-pin findings only for the properties and candidate pins they actually inspected.
- Reuse the Anna candidate audit for Anna-domain functional chassis only; it does not establish product-wide integration or cross-agent authority.
- Apollo remains deferred as a functional base search, but its future-domain boundary is included in the system-level architecture contract.
- Run no redundant broad upstream suites. For each exact pin, inspect only missing system-level seams: identity/state ownership, handoff mediation, credential/tool grants, background authority, recovery, and expected integration/update burden.
- Distinguish source claims, source tests, executed tests, and Atento composition evidence. Repository marketing text is discovery signal, not proof.

## Proactive horizon discovery policy

The search should actively look beyond repositories already present in Atento's candidate registry. The user explicitly prioritizes proactive discovery beyond the currently known horizon because an overlooked integrated platform or reusable architecture may reduce total adaptation and maintenance work. This is a search hypothesis, not a claim that GitHub discovery is inherently cheaper or that a newly found project is preferable.

For each system-level screen, search by architecture capability and operational seam (multi-agent identity, isolated memory/state, tool and credential grants, explicit handoff/delegation, background execution, recovery, deployment/update model), not only by known project names. Record query/date, repositories considered, exact pins where available, provenance, and the reason each source is admitted, retained as reference, or set aside. Prefer primary repository docs/code and freeze an exact commit before qualification.

Use a bounded funnel: discover broadly; statically pre-triage against the Atento hard boundaries; probe only missing evidence at exact pins; then compare complete Atento compositions under the same negative assertions and cost envelope. Discovery can save effort by finding a closer-fitting platform before adapting components, but it can also add evaluation and operational burden. Therefore include search/triage effort in engineering adaptation cost, and count runtime, deployment, upgrade, and maintenance burden in the same total-cost comparison.

Do not treat repository popularity, README claims, feature count, or upstream tests as proof of Atento isolation. Do not eliminate a candidate for missing evidence alone; mark it unresolved until a bounded probe or explicit hard failure supports a decision. Re-run horizon discovery only when a material gap remains, a new architecture seam appears, or the current cohort fails/has excessive measured cost; avoid unbounded search that delays the comparable composition gate.

## GitHub discovery sweep — preliminary candidates

Search date: 2026-09-30 local time. This is a discovery and static pre-triage pass. Items below are not benchmarked, installed, or accepted. Pins are recorded where the GitHub commit search returned one; where only a branch README was retrieved, the exact commit remains to be frozen before testing.

| Repository / inspected pin | System-level signal | Main unresolved architecture/cost question | Preliminary class |
|---|---|---|---|
| [MindRoom](https://github.com/mindroom-ai/mindroom/tree/4f3bd2d108a6f9be28174e0f66d78eeecddca386) `4f3bd2d108a6f9be28174e0f66d78eeecddca386` | Multi-agent Matrix runtime; agent accounts, teams, durable sessions, tools, memory and explicit delegation. Its docs define `user_agent` worker scope for per-agent filesystem isolation and describe dedicated Docker/Kubernetes workers. | The `user` worker scope intentionally shares a runtime/workspaces across that user's agents; select and test `user_agent`/dedicated workers. An inspected worker-runtime plan also says current OpenAI-compatible `/v1` requests do not yet support requester-scoped `user`/`user_agent` execution, which may constrain an Atento API integration. Matrix and worker deployment/operations may add cost. Delegation and credentials need Atento-specific tests. | SYSTEM_CHASSIS_CANDIDATE_FOR_PINNED_SCREEN |
| [Ontheia](https://github.com/Ontheia/ontheia/tree/70802db61eb16533f55efce3d8785d810223d03b) `70802db61eb16533f55efce3d8785d810223d03b` | Self-hosted platform with specialist agents, per-agent tools/memory/skills, workflows, scheduling, direct agent delegation, RBAC and PostgreSQL RLS. | RLS and memory namespaces must be checked at agent/domain scope, not inferred from user tenancy. Test direct delegation payload and credentials, update and deployment burden. | SYSTEM_CHASSIS_CANDIDATE_FOR_PINNED_SCREEN |
| [Bob Labs](https://github.com/boblabs-eu/boblabs/tree/a91d6dad098c8ba6d24436a856556078151db45d) `a91d6dad098c8ba6d24436a856556078151db45d` | Persistent multi-agent labs; each agent has model/memory/tool grants; typed event bus; per-Lab sandbox and self-hosted services. The inspected release notes include fixes to fail-closed sandbox HMAC and shell allow-list handling. | Determine whether role domains require separate Labs, how the bus shares data, what remains trusted inside a Lab, and whether its service/GPU stack raises total upkeep. Release-note fixes are not independent proof. | SYSTEM_CHASSIS_CANDIDATE_FOR_PINNED_SCREEN |
| [Clawix](https://github.com/ClawixAI/clawix/tree/5aee015e0bd793102fba69af486dd6e75df6d802) `5aee015e0bd793102fba69af486dd6e75df6d802` | Multi-agent orchestration claims per-agent Docker containers, scoped memory, RBAC, approvals, persistent workspaces, audit, and provider flexibility. | Verify isolation in code/tests; distinguish private per-agent memory from group/org sharing; measure Docker and warm-pool operations and Atento handoff adaptation. | SYSTEM_CHASSIS_CANDIDATE_FOR_PINNED_SCREEN |
| [Memoh](https://github.com/felinics/Memoh) — branch README inspected; exact commit not frozen | Self-hosted multi-agent platform; per-agent workspace/computer, filesystem, browser, network and long-term memory; supports separate server/channel deployment and also an all-in-one mode. | Freeze exact commit; prove credential, network, memory, and cross-agent boundaries; determine which components require Docker and the cost of always-on computers. | SYSTEM_CHASSIS_CANDIDATE_FOR_PINNED_SCREEN |
| [OpenAkita](https://github.com/openakita/openakita/tree/5f5b38da728274f0fd06461a481851be7c0bca6a) `5f5b38da728274f0fd06461a481851be7c0bca6a` | All-in-one assistant with multiple agents, scheduling, tools, browser/computer use, desktop/web/mobile interfaces, and advertised sandbox layers. | Verify per-agent state, secrets, tool authority, handoff semantics, and what the advertised sandbox actually isolates. | SYSTEM_CHASSIS_CANDIDATE_FOR_PINNED_SCREEN |
| [OpenClaw](https://github.com/openclaw/openclaw) — reuse the frozen Atento candidate pin | Existing NAIA candidate supports multiple agents in one Gateway with per-agent workspace, state and session stores. | Transfer is partial: test three role scopes, shared Gateway blast radius, credential fallback behavior, scheduler, and explicit handoff. Do not treat its NAIA evidence as system evidence. | CARRYOVER_SYSTEM_COMPOSITION_PROBE |
| [QwenPaw](https://github.com/agentscope-ai/QwenPaw/tree/777441721aa72db8e380d90e4d0481b05cbfd4cc) `777441721aa72db8e380d90e4d0481b05cbfd4cc` | Existing NAIA candidate with per-agent resources/governance/sandbox and MCP/A2A/ACP seams in current upstream descriptions. | Transfer exact pin to three role domains, verify sandbox fallback and cron authority, and measure composition/upkeep. | CARRYOVER_SYSTEM_COMPOSITION_PROBE |
| [Asterism](https://github.com/qmilab/asterism/tree/a8383b45f64a9a9c1923053b0f3894efb4672aba) `a8383b45f64a9a9c1923053b0f3894efb4672aba` | Explicit per-agent memory, secrets, workspace, autonomy and consented one-way agent connections. | Its own documentation says current separation is logical, not hardened containment. Keep as architecture/donor reference unless an external runtime boundary is proven. | ARCHITECTURE_REFERENCE_ONLY_AT_CURRENT_PIN |
| [AgentSpace](https://github.com/HKUDS/AgentSpace/tree/0f9da1b125def4d5a0d05b34bf7c5cec0686bbf2) `0f9da1b125def4d5a0d05b34bf7c5cec0686bbf2` | Multi-user collaborative workspace, access control, remote daemon and runtime support. | Its README lists multi-agent isolation and sandbox policy as planned, not implemented; do not count it as satisfying the current hard boundary. Keep on watch/reference. | NOT_ADMITTED_AS_CURRENT_SECURITY_CHASSIS |

This list expands the horizon; it is not an ordered Top 5. The discovery pass adds six possible integrated-system platforms to the prior 26 role-oriented sources. This is not a 32-item ranking: the selection unit is a concrete Atento composition, and one repository may be a whole platform, a role runtime, or only a donor. The former 26 remain available as role-runtime/composition sources with their original NAIA results preserved; none gains a system-level pass by carryover.

## Shared system-level architecture assertions

Use these same negative assertions for every concrete Atento composition; record cross-agent cases under AtentoEval `agent_scope=SHARED`, with source and destination roles explicit. This is the minimum structural comparison profile, not a full functional qualification suite.

| ID | Required assertion | Expected observation |
|---|---|---|
| SYS-CHAT-01 | Route a turn to NAIA, Anna, and Apollo separately, including a direct follow-up and a restart. | Correct domain identity/session resumes; no silent role drift or cross-chat history import. |
| SYS-MEM-01 | Attempt each cross-role private memory read (NAIA↔Anna, NAIA↔Apollo, Anna↔Apollo). | Denied by runtime/storage boundary; no content in output, traces, or retrieval artifacts. |
| SYS-TOOL-01 | Attempt to invoke another role's tools, including NAIA general personal side effects from Anna/Apollo. | Denied unless a typed handoff is authorized; prompts/persona alone do not grant access. |
| SYS-CRED-01 | Attempt to use or enumerate another role's credentials/provider connection. | Denied; secret material never enters another role's prompt, workspace, or trace. |
| SYS-HANDOFF-01 | Anna/Apollo request a bounded general task from NAIA. | Only the declared minimal payload crosses; NAIA re-authorizes the action under its own policy; handoff is auditable. Raw transcript/private memory is not inherited. |
| SYS-HANDOFF-02 | Attempt untyped, implicit, overbroad, or unauthorized transfer. | Denied or held for explicit decision; no silent full-context transfer. Sensitive-consent positive paths remain unqualified until the consent contract is decided. |
| SYS-BG-01 | Invoke scheduled/retry/recovery work under each role and restart the system before completion. | Background work has the same or narrower role grants as interactive work; no stale privilege or cross-role job adoption. |
| SYS-STATE-01 | Inspect process/runtime/store/config ownership for all role domains. | Every private store, state root and execution identity maps to the intended role; shared control-plane data has explicit schema/access policy. |

Capture the cost envelope during the same run: changed/copied files, dependency and pin changes, runtime/store/control paths, deployment services, handoff adapters, update friction, elapsed engineering time, rework, operations burden, and relevant model/tool cost. Do not use a qualitative feature matrix as numeric total cost.

```text
SYSTEM_ASSERTION_PROFILE = V1_DEFINED
SYSTEM_ASSERTION_EXECUTION = NOT_RUN
COST_MEASUREMENTS = NONE
```

## Benchmark cross-check

- Ranked first-sieve measurement queue (Top 10; priority order, not cost rank): `docs/evaluation/system-chassis-top10-first-sieve-2026-09-30.md`.


The detailed benchmark reconciliation is in `docs/evaluation/system-chassis-benchmark-crosscheck-2026-09-30.md`. It cross-checks Atento's historical chassis/evolvability probes, current CFS and benchmark registry, the NAIA cost audit, and two external cost-efficiency studies.

The historical Atento chassis run provides reusable extension/replacement probes and observed prototype results for Letta and a LibreChat control, but used a different candidate set and did not measure comparable lifecycle cost for NAIA + Anna + Apollo. Existing PsyChat upstream static CFS is 10/100 (routing boundary only); its 0/5 explicit seams, donor-file counts, and line-retention result are Anna/RAG-specific partial adaptation evidence. Current CFS is a static architecture screen, not effort or system qualification. The current benchmark registry is primarily Anna-oriented, largely planned, and does not benchmark system integration/maintenance cost. The NAIA audit records 0/26 comparable total-cost measurements; its NanoClaw touchpoint range is partial static evidence only.

External research supports measuring task performance together with inference token-cost/latency or cost per successful task. It does not validate GitHub discovery as cost-saving, Atento's hard isolation boundaries, or software lifecycle cost. Its quantitative results are not transferred into Atento.

```text
SYSTEM_BENCHMARK_CROSSCHECK = COMPLETED_DOCUMENTARY
SYSTEM_COMPARABLE_THREE_ROLE_COST_RUNS = 0
SYSTEM_CHASSIS_BENCHMARK_QUALIFICATION = NOT_ESTABLISHED
GITHUB_DISCOVERY_COST_SAVING = HYPOTHESIS_NOT_MEASURED
```

## Preliminary screen result

```text
OLD_NAIA_GATE1 = VALID_FOR_NAIA_SCOPE_ONLY
OLD_NAIA_UNIVERSE = 26_ROLE_ORIENTED_SOURCES
OLD_NAIA_GATE1_SYSTEM_LEVEL_PASSES = 0_CLAIMED
NEW_SYSTEM_PLATFORM_DISCOVERY_CANDIDATES = [MindRoom, Ontheia, Bob Labs, Clawix, Memoh, OpenAkita]
CARRYOVER_ROLE_COMPOSITION_SOURCES = [OpenClaw, QwenPaw, AI Butler, NanoClaw, Letta Code]
ARCHITECTURE_REFERENCES = [Asterism, AgentSpace]
NEW_TECHNICAL_ELIMINATIONS = 0
FULL_ATENTO_SYSTEM_COMPOSITION_TESTS = 0
COMPARABLE_SYSTEM_TOTAL_COST_MEASUREMENTS = 0
SYSTEM_CHASSIS_WINNER = NONE
SYSTEM_CHASSIS_SHORTLIST = NOT_SELECTED
```

This is a discovery/static evidence pass, not an executed Atento architecture test. No repository claim or source test alone proves separation of Atento chats, memory, tools, credentials, or handoffs.

## Bounded sequential test model — 2026-10-01

The normative method is `docs/evaluation/harness.md#111-system-chassis-first-sieve-bounded-sequential-comparison`. This dated record fixes the cohort/order and reports its execution state; it does not select a candidate.

### Fixed cohort and order

Run one candidate at a time, in this order. The first sieve for **each** candidate starts by measuring `TOTAL_ADAPTATION_AND_ONGOING_MAINTENANCE_COST`, then executes the same eight `SYS-*` assertions in the section above. This order preserves the existing Top 10 evidence-priority queue and carries Letta Code forward from the earlier system screen; it is not a cost ranking.

| Order | Candidate | Commit used for this screen |
|---:|---|---|
| 1 | NanoClaw | `nanocoai/nanoclaw@4c1eabd3ddd74cc3d71b1871da857391a9411c8d` |
| 2 | AI Butler | `LumabyteCo/aibutler@c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c` |
| 3 | OpenClaw | `openclaw/openclaw@e9571d77e76bd6d35996273d9e8398ad539b26e1` |
| 4 | QwenPaw | `agentscope-ai/QwenPaw@777441721aa72db8e380d90e4d0481b05cbfd4cc` |
| 5 | MindRoom | `mindroom-ai/mindroom@4f3bd2d108a6f9be28174e0f66d78eeecddca386` |
| 6 | Bob Labs | `boblabs-eu/boblabs@a91d6dad098c8ba6d24436a856556078151db45d` |
| 7 | Ontheia | `Ontheia/ontheia@70802db61eb16533f55efce3d8785d810223d03b` |
| 8 | OpenAkita | `openakita/openakita@5f5b38da728274f0fd06461a481851be7c0bca6a` |
| 9 | Clawix | `ClawixAI/clawix@5aee015e0bd793102fba69af486dd6e75df6d802` |
| 10 | Memoh | Exact commit must be frozen in `docs/third-party.md` before execution; currently `PIN_REQUIRED`. |
| 11 | Letta Code | `letta-ai/letta-code@21daa38a8cdd74f2d03b634c8312253080bacfc1` |

The cohort is fixed for this pass. Do not silently drop a candidate or expand the cohort mid-run. A pin that cannot be frozen blocks that candidate until resolved; continue with the next candidate, then return to it before closing the cohort.

### Comparison controls and bounded work

- Same candidate-neutral profile, three role identities, synthetic data/credentials, policies, handoff payload, restart/failure conditions, and expected observations for all candidates.
- Before execution, map existing test/CI/probe evidence to each candidate and each assertion. Reuse a result when its exact pin, setup, tested property, outcome, and provenance are applicable; capture evidence level and limitations. Do not rerun equivalent tests to normalize commands or names.
- Candidate adapters can translate only the mechanics needed to run and inspect assertions. If a usable adapter would require building product runtime or broad donor changes, record `BLOCKED_ADAPTER` and move on.
- Run only uncovered assertions or Atento-specific deltas. At most one new primary run per candidate and one targeted confirmation for suspected infrastructure invalidity or possible hard-gate failure; no duplicate runs or broad upstream suite reruns.
- Start cost assessment with existing measured adaptation/maintenance evidence; collect only missing marginal dimensions. Separate measured historical evidence from newly measured and non-comparable estimates. Record files/touchpoints, dependencies/pins, runtime/store/control/deployment paths, engineering time/rework, and ongoing operations. No synthetic total-cost score.
- Statuses: `PASS`, reproduced hard-gate `FAIL`, `BLOCKED` for absent/non-transferable evidence, or `BLOCKED_ADAPTER`. Missing evidence is not failure. Complete the cohort despite earlier pass/fail results; no infinite reruns.
- Maintain a provisional Top 3 only among completed hard-gate passes with comparable cost evidence. Preserve ties/unranked results where needed. The Top 3 is not a selection; no candidate is eliminated solely for missing evidence.

### GitHub recommendation and this protocol

GitHub Actions defaults independent jobs and matrix variations to parallel execution; matrix `fail-fast` is enabled by default. That default would violate the serial order and could prevent later candidates from running after an early failure. A future workflow should set `max-parallel: 1` and `fail-fast: false`, and enforce cohort order with an ordered runner or explicit `needs` chain (plus an appropriate `if` condition so failures do not skip later candidates). GitHub's documentation describes workflow execution mechanics; it does not define Atento's cost-first method, comparable assertions, or provisional Top 3. See [job variations](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations), [using jobs](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-jobs), and [workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax).

### Current execution state

```text
COHORT_SIZE = 11
COMMON_PROFILE = 8_ASSERTIONS_DEFINED; CANDIDATE_NEUTRAL_RUNNER_NOT_IMPLEMENTED
EXISTING_EVIDENCE_REUSE = REQUIRED_BEFORE_ANY_RERUN
SEQUENTIAL_CANDIDATE_RUNS = 0
COMPARABLE_COST_MEASUREMENTS = 0
PROVISIONAL_TOP_3 = NOT_STARTED
CANDIDATE_SELECTED = NONE
```

## Evidence/source hierarchy

- Product role boundaries and open topology: `docs/adr/ADR-001-naya-product-composition.md`.
- NAIA role-specific screen and cost records: `docs/evaluation/naia-architecture-gate1-screen-2026-09-30.md`, `docs/evaluation/naia-architecture-chassis-maintenance-cost-audit-2026-09-30.md`, and the NAIA Top 5 record.
- Exact repository docs and code at listed commits; source claims are not runtime proof.
- Atento three-role composition artifacts and independent verification, once executed.

## Primary GitHub sources

- MindRoom: `https://github.com/mindroom-ai/mindroom/blob/4f3bd2d108a6f9be28174e0f66d78eeecddca386/docs/configuration/agents.md`; `https://github.com/mindroom-ai/mindroom/blob/4f3bd2d108a6f9be28174e0f66d78eeecddca386/docs/deployment/sandbox-proxy.md`; `https://github.com/mindroom-ai/mindroom/blob/4f3bd2d108a6f9be28174e0f66d78eeecddca386/docs/dev/persistent-worker-runtime-plan.md`.
- Ontheia: `https://github.com/Ontheia/ontheia/tree/70802db61eb16533f55efce3d8785d810223d03b`.
- Bob Labs: `https://github.com/boblabs-eu/boblabs/tree/a91d6dad098c8ba6d24436a856556078151db45d`.
- Clawix: `https://github.com/ClawixAI/clawix/tree/5aee015e0bd793102fba69af486dd6e75df6d802`.
- Memoh: `https://github.com/felinics/Memoh` (exact commit pending).
- OpenAkita: `https://github.com/openakita/openakita/tree/5f5b38da728274f0fd06461a481851be7c0bca6a`.
- Asterism: `https://github.com/qmilab/asterism/tree/a8383b45f64a9a9c1923053b0f3894efb4672aba`.
- AgentSpace: `https://github.com/HKUDS/AgentSpace/tree/0f9da1b125def4d5a0d05b34bf7c5cec0686bbf2`.
- Architecture-analysis basis: [SEI ATAM](https://www.sei.cmu.edu/library/the-architecture-tradeoff-analysis-method/) evaluates architectural tradeoffs against quality-attribute goals; [NIST SP 800-207](https://doi.org/10.6028/NIST.SP.800-207) informs identity- and policy-based resource-access requirements. Neither source selects a chassis for Atento.
- OpenClaw and QwenPaw: exact candidate pins are in the existing Atento NAIA evidence records; retain those pins rather than current branch heads.
