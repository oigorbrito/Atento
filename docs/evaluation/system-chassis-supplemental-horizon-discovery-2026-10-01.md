# Supplemental system-chassis horizon discovery — 2026-10-01

## Scope

This bounded addendum records one additional GitHub discovery sweep after the user asked to continue looking for missing chassis projects. The unit remains a complete Atento composition for NAIA, Anna, and Apollo, or a component that could materially reduce the composition cost. This is discovery/static pre-triage only.

Search focus: persistent multi-agent or personal-assistant runtimes; per-agent identity, memory and tool boundaries; API/provider integration; explicit delegation; scheduled work and recovery; self-hosting; mobile-client fit. Repositories already in the Atento cohort are not duplicated. Octop was found in prior Atento records and is not a new candidate.

No candidate in this addendum was installed, benchmarked locally, security-tested, or accepted. README and product claims are discovery signals, not Atento proof.

## Newly surfaced candidates

The first three below are prioritized for a pinned static screen because their documented architecture maps most directly to the Atento three-role boundary. This is a work queue, not a ranking or a qualification result.

| Priority | Project / exact pin observed | Fit signal from project source | Main unresolved Atento question | Discovery disposition |
|---:|---|---|---|---|
| 1 | [HybridClaw](https://github.com/HybridAIOne/hybridclaw) `b9378588f9f9666355fc5431a7b1f5292aaa93c0` | Self-hosted assistant runtime; project documents per-agent workspaces, models and budgets, explicit addressing, encrypted A2A trust, credential references, and a local API surface. MIT. | Does exact-pin storage, tool grants, provider credentials, sessions, background jobs, and retries enforce boundaries between three Atento roles when hosted behind the Android app? Product documentation is not proof. | ADMIT_TO_PINNED_STATIC_SCREEN |
| 2 | [OpenLegion](https://github.com/openlegion-ai/openlegion) `24efd6e06b28768cbbcd9275f43c479b3df37b18` | Project documents per-agent Docker/container or microVM isolation, separate memory/tools/schedules/budgets, a central credential vault, and default-deny cross-agent ACLs. | Verify exact-pin implementation and API/runtime seam. Requires Docker. Per-agent container isolation is structurally strong, but shared `TEAM.md`, trusted mesh host, and fallback from microVM to Docker require explicit Atento scoping and runtime verification. | ADVANCE_TO_RUNTIME_BOUNDARY_SPIKE |
| 3 | [Hivekeep](https://github.com/MarlBurroW/hivekeep) `7d023c952e46861070683825ff545daf981910f0` | Persistent personal-agent team, provider/API connectors, PWA, and agent-owned private memory by default with explicit sharing documented. MIT. | Confirm that role-specific tools, credentials, chat state, scheduled execution, and recovery are equally scoped; assess whether its single-container/storage model creates a cross-role boundary. The PWA is a client-fit signal, not Android integration proof. | ADMIT_TO_PINNED_STATIC_SCREEN |
| — | [OpenVole](https://github.com/openvole/openvole) `c8b405f4933a5ee0a1cb7725cf4c8a31cd24d732` | Self-hosted fleet; README describes per-agent identity, tools, memory, model selection, and server/dashboard; MIT. | Exact pin has per-agent process/config/data directories and project-level tool narrowing. Node network sandbox is effective only on Node 25+; VoleNet can share memory/tools/sessions, and orchestrator privilege crosses sibling administration. | STATIC_SCREEN_COMPLETE; BOUNDED_PROBE_PENDING |
| — | [Open Pincery](https://github.com/RCSnyder/open-pincery) `fc33211c7b04e1a958a340c369cb635f018c13f4` | Persistent event-driven agents with stable identity, append-only per-agent logs, lifecycle transitions, capability nonces, and a described security test suite. | REST API and rich Linux security suite exist. Credential vault is workspace-scoped, so same-workspace agents share a credential domain; role isolation likely needs one workspace per role and an Atento broker. Linux/Postgres deployment and required sandbox add adaptation weight. | STATIC_SCREEN_COMPLETE; BOUNDED_PROBE_PENDING |
| — | [OpenFang](https://github.com/RightNow-AI/openfang) `acf2587e46be174c10200489c9a2d23a39a98aeb` | Rust agent OS, multi-provider REST/streaming API, persistent agents and workflow features; Apache-2.0. A third-party Agent Reality Index lists 32.1/100 and rank 10/17 as of 2026-08-23. | Its own description says it is not a multi-agent orchestrator. Determine whether named agents provide separate durable memory, tool authority, and role-bound sessions before admitting it as a three-role system candidate. The third-party score is not an Atento or isolation result. | ROLE_RUNTIME_REFERENCE; NOT_ADMITTED_TO_SYSTEM_SHORTLIST |
| — | [OpenEnsemble](https://github.com/openensemble/openensemble) `1e9d9f8774b1243636623aea01293cdab866ba33` | Multi-agent assistant; source resolves per-agent episodic/rule memory and per-agent tool assignments. | Its per-user OS sandbox remains a design, not an implemented boundary; exact-pin tree contains no general test suite, though build/lint/typecheck CI passes. Additional full code review required before runtime probing. | REVIEWED; BELOW_BOUNDED_TOP3 |
| — | [MIRA](https://github.com/Vexillon-ai/MIRA) `d2732cf5a3d25eeea9cc1e26fdc38d1ffe95574e` | Self-hosted personal agent, user-scoped memory, tools and background sub-agents. | Source describes one persistent assistant, not three durable role-bound agents; multi-instance broker cost is unmeasured. | ROLE_RUNTIME_REFERENCE; NOT_IN_TOP3 |\n| — | [Moltis](https://github.com/moltis-org/moltis) `1f6d28ea750d6654d52d5899b8be67727ebf7a19` | Persistent agent personas with per-agent workspaces and tool policies; REST/WebSocket, PWA/mobile surface, sandboxed execution. Exact-pin CI includes tests, E2E, sandbox E2E and iOS app. | Verify per-agent vault authority, transcript ownership, and whether API/session authorization can enforce NAIA/Anna/Apollo boundaries. Rust/server migration cost remains unmeasured. | ADVANCE_TO_BOUNDED_TOP3 |
| — | [Kora](https://github.com/era3000/kora) | Self-hosted provider-connected assistant with per-user workspace and sub-agent features; MIT. | Inspected repository was a very small early-stage project with no release or frozen comparison pin; per-agent role boundaries are not established. | HOLD_FOR_MATURITY_AND_ROLE_BOUNDARY |

The exact pins above are the latest default-branch commit SHAs returned during this search where available; the repositories must be re-frozen before any later execution. A SHA records identity, not quality.

## Common pinned static screen — results

| Candidate | Session / memory boundary | Tools / credentials | Inter-agent and background surface | Static gate |
|---|---|---|---|---|
| HybridClaw | Canonical sessions are agent-addressed; default channel-peer scope; workspace defaults to agent ID. Cross-session memory is keyed by agent and user. Explicitly shared workspace or linked identities can widen scope. | Per-agent tools are supported, but an omitted allowlist is unrestricted. Credential references and delegated A2A tokens are present; these need explicit per-role configuration. | Explicit addressed A2A handoff; JWT delegation tokens are scoped and expiring. | Static candidate; below the cost-first top three. Preserve omitted/empty allowlist, shared-workspace denial, and handoff scope for a later probe if the top three fails. |
| OpenLegion | Separate agent containers and private workspaces/memory. Shared `TEAM.md` is readable by team members and must not carry private role context. | Default-deny permissions, explicit message ACLs, host-side credential vault. The mesh host is trusted and holds credentials; any-auth endpoints need deployment scoping. | Browser service is shared but per-agent; schedules exist. MicroVM init can fall back to Docker, so do not count microVM isolation without observing runtime mode. | **Top-three priority 2.** Test role-to-role message denial, shared-file leakage, credential proxy scope, and fallback mode. |
| Moltis | Persistent personas use per-agent workspaces; session state and memory tools operate with the selected agent. | Per-agent preset tool allow/deny is supported; vault/API authorization still needs role-bound tests. | REST/WebSocket API, PWA/mobile surface, per-agent sessions, background tools. | **Top-three priority 3.** Test vault authority, transcript ownership, API/session authorization, and restart. |
| Hivekeep | Per-agent persistent sessions and private profile/archive by default. Shared memories are searchable by all agents; contact records/notes are instance-wide. API supports agent-scoped clients and isolated conversations. | Toolboxes grant tools per agent; no configured toolbox resolves to core tools at the inspected pin. API keys can be scoped to an agent and allowed conversation modes. | Explicit inter-agent messaging and subagents; cron/webhooks feed agent queues. | Static candidate; below the cost-first top three. Preserve shared-memory, global contact-note, toolbox-default, API-key, and isolated-conversation probes for a later gate. |

These are source observations at the pins, not executed test results. The cost-first top three receives the same negative probes in sequence; stop on a reproduced hard-boundary failure and cap diagnosis before full integration. Alternates advance only if a top-three pin fails or cannot be reached. No cost/latency score or total adaptation estimate is inferred from repository size or feature count.

## Bounded remaining-horizon review

OpenEnsemble's pinned source does show per-agent prompt memory calls (own params/episodes with shared user facts separately scoped) and individual tool assignments. Its design document explicitly marks whole per-user sandboxing as not built. The current Atento deployment is a single user, so this is not by itself a role-boundary failure; however, lack of a committed test suite and incomplete OS boundary lower its priority. Exact-pin CI passes build, lint and typecheck only. The repository's `oe bench` is a local product benchmark, not an independent cross-project score.

OpenFang has self-reported measurements for startup, memory, binary size, security and channel/provider breadth; these remain project-run comparison claims. The third-party Agent Reality Index score already found is 32.1/100, rank 10/17 (2026-08-23). OpenFang describes itself as not a multi-agent orchestrator, so it remains a runtime/footprint reference. MIRA is likewise a persistent personal-agent runtime with spawnable workers, not three durable role personas at the inspected pin.

Moltis is different: pinned source has persisted agent personas, an individual workspace per agent, and per-agent tool presets that apply to each persona's sessions. Existing source tests cover per-agent workspaces, session behavior, tool policy, sandbox and agent-scoped memory tools. The external [Harness-Bench preprint](https://arxiv.org/abs/2605.27922) reports Moltis at **68.8 aggregate score, 78.4 completion, 100.0 security, 86.3 tool-use, 87.3 consistency, 84.1 robustness, 134.9K tokens and 8.0 turns**, averaged over 106 tasks and eight model backends. This is coding/workflow harness evidence, not role isolation; NanoClaw is not one of the compared harnesses. Reuse it as a separate benchmark signal; do not rerun or transfer it as an Atento score. Exact-pin CI has passing Rust test, E2E, sandbox E2E, coverage and iOS-app jobs; macOS app job failed in the observed run. An iOS app check is not Android qualification.

## Cost-first bounded top three for the next common probe

The order below is a **structural adaptation-effort hypothesis**, based on required runtime/services and boundary seams. It is not measured engineering time, a benchmark rank, or a winner declaration. The same role-boundary canary is applied serially, stopping on the first reproduced hard leak and capping diagnosis at one attempt.

| Order | Candidate | Why it enters this bounded probe | Highest-cost unknown |
|---:|---|---|---|
| 1 | Open Pincery | Strongest explicit sandbox/capability architecture and event-sourced lifecycle among newly screened pins. | Linux sandbox + PostgreSQL + workspace-scoped credential broker; split workspace/session authority across roles. |
| 2 | OpenLegion | Separate agent containers, explicit ACLs and host credential vault. | Docker/microVM deployment and trusted mesh host; shared team files and browser default permissions. |
| 3 | Moltis | Persistent per-agent personas/workspaces, API/PWA surface, extensive exact-pin CI and one externally published harness benchmark. | Verify role-bound vault/API authority and estimate Rust runtime adaptation. |

HybridClaw, Hivekeep, OpenVole and OpenEnsemble remain documented alternates, not additional simultaneous test targets. None is eliminated. OpenFang and MIRA remain references because the inspected architecture is not a three-persistent-role chassis. The Atento canary remains blocked until a pinned source checkout is available; GitHub proxy access failed in this workspace. This order does not change NanoClaw's provisional NAIA-only direction or select bases for Anna/Apollo.

## Existing benchmark coverage

A bounded search did not identify a common independent chassis benchmark for the screened projects. Moltis has the separate Harness-Bench result documented above; OpenFang has the Agent Reality Index result. Neither directly measures the Atento role-boundary requirement. HybridClaw documents local evaluation tooling; that is not an independent published comparative score. OpenFang has the separate Agent Reality Index result noted above, which cannot be combined with Atento candidate scores or used as evidence of isolation.

Do not repeat an external benchmark for a matching release/configuration if one is later found. Do not transfer a model score or a different runtime release to these pins. Any external capability score remains separate from adaptation cost, role isolation, credential custody, handoff, and recovery.

## Supplemental static screens — OpenVole and Open Pincery

| Candidate | What the exact pin supports | Atento-specific gap / adaptation pressure | Exact-pin CI and independent benchmark evidence |
|---|---|---|---|
| OpenVole `c8b405f4933a5ee0a1cb7725cf4c8a31cd24d732` | One child engine per agent; agent-specific config, Paws, identity and data directory. Tool access supports agent allowlists and task-level narrowing; orchestrator authority is explicitly granted and re-verified. Source tests cover non-widening tool profiles, project-scoped files, agent messaging, schedules and event logs. | Paws run as subprocesses under the same host user. Network restriction through Node's permission model is documented as effective only on Node 25+; Node 20–24 do not enforce that network grant. VoleNet's configured share options can expose tools/memory/session across peers. Disable sharing and orchestrator grants by default; verify per-agent credential env and Android-facing API/auth path. | Exact-pin checks: build, deploy and publish succeeded, but this pin's visible GitHub checks did not execute the source test suite. No independent candidate-specific numeric chassis benchmark found in the bounded search. [Build](https://github.com/openvole/openvole/actions/runs/35498206290/job/106045064072). |
| Open Pincery `fc33211c7b04e1a958a340c369cb635f018c13f4` | Per-agent event streams and wake lifecycle; typed permission modes and unknown tools default to destructive/denied; one-use, workspace-bound capability nonces; Linux bubblewrap/seccomp/Landlock sandbox. REST API can support an Android client. Exact-pin tests include workspace API denial, capability gate/nonces, credential vault, lifecycle and real bubblewrap smoke. | Credentials and capability nonce are workspace-scoped rather than agent-scoped. To preserve Atento role separation, use three workspaces or add a narrower credential broker; cross-role handoff then needs explicit broker rules. Runtime depends on PostgreSQL and Linux sandbox primitives. This is a heavier adaptation hypothesis, not measured effort. | Exact-pin `cargo test`, clippy, and real bubblewrap smoke succeeded; Linux x86_64 and macOS builds succeeded, Linux aarch64 and Windows builds failed. No independent candidate-specific numeric chassis benchmark found in the bounded search. [Cargo tests](https://github.com/RCSnyder/open-pincery/actions/runs/31919350786/job/95096541459), [real sandbox smoke](https://github.com/RCSnyder/open-pincery/actions/runs/31919350786/job/95096541497), [Linux aarch64 build](https://github.com/RCSnyder/open-pincery/actions/runs/31919540291/job/95097027303). |

These two candidates are now included in the same future canary cohort; source strength and general CI do not make them pass the Atento gate. No new test was executed, and no candidate is eliminated.

## Exact-pin upstream CI (reused, not rerun)

GitHub check-runs were queried by the three exact commit SHAs. These are upstream CI results, not Atento-specific qualification and not benchmark scores.

| Candidate pin | Exact-pin CI result found | Interpretation |
|---|---|---|
| HybridClaw `b9378588f9f9666355fc5431a7b1f5292aaa93c0` | Unit shards 1–3, `test`, `npm-e2e`, install E2E, coverage, lint, agent image build and CodeQL succeeded. Gateway Docker build was cancelled; Docker preflight skipped. | Broad upstream tests are green, but gateway container build is not demonstrated by this run. Relevant exact-pin jobs: [unit (1)](https://github.com/HybridAIOne/hybridclaw/actions/runs/36891088314/job/110466596211), [unit (2)](https://github.com/HybridAIOne/hybridclaw/actions/runs/36891088314/job/110466595982), [unit (3)](https://github.com/HybridAIOne/hybridclaw/actions/runs/36891088314/job/110466596022), [npm-e2e](https://github.com/HybridAIOne/hybridclaw/actions/runs/36891088314/job/110466596492), [gateway build](https://github.com/HybridAIOne/hybridclaw/actions/runs/36891087946/job/110467098800). |
| OpenLegion `24efd6e06b28768cbbcd9275f43c479b3df37b18` | Python test matrix for 3.11/3.12 across three shards and coverage all succeeded; lint succeeded (run 2026-08-23). | Upstream project test suite passes at this pin; it does not establish Atento three-role isolation. [CI run](https://github.com/openlegion-ai/openlegion/actions/runs/32638650769). |
| Hivekeep `7d023c952e46861070683825ff545daf981910f0` | Exact-pin `Typecheck, Test & Build` and typecheck/build gate succeeded (run 2026-09-17); newer checks on the same SHA include successful site builds. | Generic project health evidence. Dependabot failures are not application test failures. Does not prove Atento route-level boundaries. [test/build job](https://github.com/MarlBurroW/hivekeep/actions/runs/35212700435/job/105173759352). |

## Upstream test reuse audit (definitions inspected; not executed here)

| Candidate | Existing exact-pin test definitions that overlap | What they establish if run upstream | Remaining common Atento probe |
|---|---|---|---|
| HybridClaw | `tests/session-routing.test.ts`, `tests/session-instances.test.ts`, `tests/memory-service.test.ts`, `tests/container.memory-tool.test.ts`, `tests/delegation-jobs-store.test.ts`, `tests/gateway-service.agent-addressing.test.ts` | Unit/integration behavior for DM routing, session instances, memory operations, address resolution, and delegation lifecycle. The inspected tree has no dedicated `tool-policy` test file; policy source documents absent allowlist as unrestricted. | Use a hostile three-role fixture: distinct session and memory markers; absent/empty/explicit tool grants; attempted cross-role memory/tool access and A2A handoff. Verify the runtime result and audit record. |
| OpenLegion | `tests/test_permissions.py`, `tests/test_credentials.py`, `tests/test_handoff_integration.py`, `tests/test_shared_paths.py`, `tests/test_session_persistence.py` | Default-deny permission cases, credential-vault behavior, task handoff, path traversal protection, and browser session persistence under per-agent paths. Browser-action tests document that a legacy agent with `browser_actions=None` allows all known and future actions. | Three roles with explicit permission files; cross-role message, file, browser, and credential attempts; inspect actual runtime isolation backend/fallback; restart while work is pending. |
| Hivekeep | `src/server/services/external-api.test.ts`, `src/server/services/inter-agent.test.ts`, `src/server/services/memory.test.ts`, `src/server/services/agents.test.ts` | Service tests reject resolving a conversation under another agent/client and scope API requests by client. Inter-agent tests cover rate limiting. **Memory scope assertions in the inspected test are replicated helper logic**, not calls to the production memory service; do not count them as service-level isolation proof. | Three role-scoped API clients; route-level cross-agent reads/writes; real memory tool/service private-vs-shared query; toolbox omission/empty grants; ownership after restart. |

The test suites were not executed by this evaluation; the exact-pin upstream CI results above are reused as external evidence. No Atento runtime test was run. A test file's presence is not a pass. Existing upstream definitions are reusable only for the behavior they actually exercise; they do not replace the common Atento boundary probe.

## Next bounded execution gate

The single comparable probe for the three advancing candidates is a role-boundary canary: create NAIA, Anna, and Apollo with unique private sentinel values and disjoint tools/credentials; send one request per role; attempt direct access to each other role's sentinel, tool, credential, transcript, and isolated API conversation; then restart with one queued/delegated task and check that ownership and authorization remain unchanged. Use the same assertion set and fixture semantics for each candidate, sequentially. Record raw request/response or tool-call trace, resolved principal/agent/session IDs, effective tool grant, backing memory query result, restart state, and relevant logs. PASS requires all cross-role reads/actions to be denied, each role's own operation to succeed, and ownership to survive restart. Any cross-role disclosure or action is FAIL; missing instrumentation, backend ambiguity, or inability to execute is INVALID/HOLD, never a pass.

Stop a candidate on the first reproducible hard-boundary leak. Cap the first spike at this canary plus one diagnosis/reproduction attempt per failure; do not proceed to full adapter work unless the candidate passes. The pinned source checkout could not be obtained through this workspace's GitHub proxy. Exact-pin upstream CI provides a general test baseline, but the Atento boundary probe is still STATIC_SOURCE / NOT_EXECUTED until a pinned checkout and its declared dependencies are available. This does not change NanoClaw's provisional NAIA direction or qualify any new base.

## Bounded next gate

Completed the exact-pin source screens serially for HybridClaw, OpenLegion, Hivekeep, OpenVole, Open Pincery, OpenEnsemble, and Moltis. The cost-first common-probe order is Open Pincery, OpenLegion, Moltis. This is a source plausibility/priority decision, not execution proof or candidate qualification. The user directed that licenses be ignored as a screening criterion; no candidate is gated or removed on license grounds. Keep license facts out of ranking decisions.

Reuse all existing Atento candidate evidence. Do not repeat prior NanoClaw, QwenPaw, AI Butler, Octop, or benchmark tests. Do not install all candidates or start an open-ended benchmark loop. HybridClaw, Hivekeep, OpenVole and OpenEnsemble remain alternates outside this bounded top three unless a top-three candidate fails or a material gap specifically favors an alternate. OpenFang and MIRA stay as runtime references.

```text
NEW_REPOSITORIES_DISCOVERED = 8
PRIOR_ATENTO_CANDIDATES_DUPLICATED = [Octop]
NEW_TESTS_OR_BENCHMARKS_RUN = 0
NEW_COMMON_EXTERNAL_CHASSIS_SCORES = 0
NEW_CANDIDATE_QUALIFICATIONS = 0\nINDEPENDENT_NUMERIC_BENCHMARKS_REUSED = [Moltis_Harness_Bench_68.8, OpenFang_Agent_Reality_Index_32.1]\nSTATIC_PINS_SCREENED = 7\nCOST_FIRST_BOUNDED_PROBE_ORDER = [OpenPincery, OpenLegion, Moltis]\nDOCUMENTED_ALTERNATES = [HybridClaw, Hivekeep, OpenVole, OpenEnsemble]\nRUNTIME_REFERENCES = [OpenFang, MIRA]
FIRST_STATIC_SCREEN_PRIORITY = [HybridClaw, OpenLegion, Hivekeep]
OVERALL_THREE_ROLE_CHASSIS_WINNER = NOT_SELECTED
```

## Primary sources checked

- HybridClaw README: https://github.com/HybridAIOne/hybridclaw
- OpenLegion README, architecture, and license: https://github.com/openlegion-ai/openlegion
- Hivekeep README and agent memory docs: https://github.com/MarlBurroW/hivekeep and https://hivekeep.app/docs/agents/memory/
- OpenVole README: https://github.com/openvole/openvole
- Open Pincery README/security architecture: https://github.com/RCSnyder/open-pincery
- OpenFang README/API: https://github.com/RightNow-AI/openfang
- Agent Reality Index result: https://www.getreadyforagents.com/tools/openfang/
- OpenEnsemble README: https://github.com/openensemble/openensemble
- MIRA README: https://github.com/Vexillon-ai/MIRA
- Moltis README: https://github.com/moltis-org/moltis
- Kora README: https://github.com/era3000/kora
