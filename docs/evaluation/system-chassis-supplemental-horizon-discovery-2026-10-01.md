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
| 2 | [OpenLegion](https://github.com/openlegion-ai/openlegion) `24efd6e06b28768cbbcd9275f43c479b3df37b18` | Project documents per-agent Docker/container or microVM isolation, separate memory/tools/schedules/budgets, a central credential vault, and default-deny cross-agent ACLs. | Verify exact-pin implementation and API/runtime seam. Requires Docker. License is PolyForm Perimeter 1.0.1: the project states internal self-hosting is allowed but competing hosted/service redistribution is restricted. Obtain a product-specific license determination before adoption. | ADMIT_TO_PINNED_STATIC_SCREEN_WITH_LICENSE_GATE |
| 3 | [Hivekeep](https://github.com/MarlBurroW/hivekeep) `7d023c952e46861070683825ff545daf981910f0` | Persistent personal-agent team, provider/API connectors, PWA, and agent-owned private memory by default with explicit sharing documented. MIT. | Confirm that role-specific tools, credentials, chat state, scheduled execution, and recovery are equally scoped; assess whether its single-container/storage model creates a cross-role boundary. The PWA is a client-fit signal, not Android integration proof. | ADMIT_TO_PINNED_STATIC_SCREEN |
| — | [OpenVole](https://github.com/openvole/openvole) `c8b405f4933a5ee0a1cb7725cf4c8a31cd24d732` | Self-hosted fleet; README describes per-agent identity, tools, memory, model selection, and server/dashboard; MIT. | Verify actual server-side authorization and whether fleet delegation or VoleNet sharing can be disabled/bounded per Atento role. Exact role/session/credential isolation is unproven. | WATCHLIST; NOT_IN_FIRST_THREE |
| — | [Open Pincery](https://github.com/RCSnyder/open-pincery) `fc33211c7b04e1a958a340c369cb635f018c13f4` | Persistent event-driven agents with stable identity, append-only per-agent logs, lifecycle transitions, capability nonces, and a described security test suite. | No license was identified in the GitHub repository metadata checked; resolve adoption rights before implementation study. Verify usable HTTP/mobile integration and inspect, rather than infer from, the reported tests. | HOLD_LICENSE_AND_INTEGRATION_CHECK |
| — | [OpenFang](https://github.com/RightNow-AI/openfang) `acf2587e46be174c10200489c9a2d23a39a98aeb` | Rust agent OS, multi-provider REST/streaming API, persistent agents and workflow features; Apache-2.0. A third-party Agent Reality Index lists 32.1/100 and rank 10/17 as of 2026-08-23. | Its own description says it is not a multi-agent orchestrator. Determine whether named agents provide separate durable memory, tool authority, and role-bound sessions before admitting it as a three-role system candidate. The third-party score is not an Atento or isolation result. | ROLE_RUNTIME_REFERENCE; NOT_ADMITTED_TO_SYSTEM_SHORTLIST |
| — | [OpenEnsemble](https://github.com/openensemble/openensemble) `1e9d9f8774b1243636623aea01293cdab866ba33` | Self-hosted multi-user assistant with agents, memory, and scheduler; AGPL-3.0. | No inspected evidence establishes per-agent role authority or cross-agent memory/tool denial. Resolve AGPL implications for the intended distribution. | HOLD_FOR_ROLE_BOUNDARY_AND_LICENSE_CHECK |
| — | [MIRA](https://github.com/Vexillon-ai/MIRA) `d2732cf5a3d25eeea9cc1e26fdc38d1ffe95574e`; [Moltis](https://github.com/moltis-org/moltis) `1f6d28ea750d6654d52d5899b8be67727ebf7a19` | Persistent single-assistant runtimes with remote model-provider connectors, memory, tools, and sandbox features. MIRA is AGPL-3.0; Moltis is MIT. | Source descriptions establish a strong single-role surface, not an isolated three-role composition. Three separate instances plus a narrow Atento broker remain a possible architecture, with duplicated lifecycle/adaptation cost unmeasured. | ROLE-SPECIFIC_REFERENCES |
| — | [Kora](https://github.com/era3000/kora) | Self-hosted provider-connected assistant with per-user workspace and sub-agent features; MIT. | Inspected repository was a very small early-stage project with no release or frozen comparison pin; per-agent role boundaries are not established. | HOLD_FOR_MATURITY_AND_ROLE_BOUNDARY |

The exact pins above are the latest default-branch commit SHAs returned during this search where available; the repositories must be re-frozen before any later execution. A SHA records identity, not quality.

## Existing benchmark coverage

A bounded search for external numeric results did not identify a common independent chassis benchmark for HybridClaw, OpenLegion, Hivekeep, OpenVole, or Open Pincery. HybridClaw documents local evaluation tooling; that is not an independent published comparative score. OpenFang has the separate Agent Reality Index result noted above, which cannot be combined with Atento candidate scores or used as evidence of isolation.

Do not repeat an external benchmark for a matching release/configuration if one is later found. Do not transfer a model score or a different runtime release to these pins. Any external capability score remains separate from adaptation cost, role isolation, credential custody, handoff, and recovery.

## Bounded next gate

Proceed serially in this order: HybridClaw, OpenLegion (only after the license question is dispositioned), then Hivekeep. First inspect the exact pinned source and test definitions against the common Atento assertions. A project advances only if the pin contains a plausible path to three role-bound sessions, private memory, tool/credential authority, explicit handoff, and background/recovery controls. Missing proof stays unresolved; a hard structural incompatibility or licensing stop can remove it before implementation.

Reuse all existing Atento candidate evidence. Do not repeat prior NanoClaw, QwenPaw, AI Butler, Octop, or benchmark tests. Do not install all candidates or start an open-ended benchmark loop. OpenVole and Open Pincery remain outside this first three unless the first gate exposes a material gap they uniquely address.

```text
NEW_REPOSITORIES_DISCOVERED = 8
PRIOR_ATENTO_CANDIDATES_DUPLICATED = [Octop]
NEW_TESTS_OR_BENCHMARKS_RUN = 0
NEW_COMMON_EXTERNAL_CHASSIS_SCORES = 0
NEW_CANDIDATE_QUALIFICATIONS = 0
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
