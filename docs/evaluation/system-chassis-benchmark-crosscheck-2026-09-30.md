# Benchmark cross-check — Atento system chassis — 2026-09-30

## Question and decision scope

Question: does existing Atento or external benchmark evidence verify that proactive GitHub discovery is likely to lower the **total adaptation and ongoing-maintenance cost** of the complete Atento architecture for NAIA, Anna, and Apollo?

The benchmark evidence can guide the comparison design and show that cost/quality trade-offs are measurable. It does **not** currently establish which repository, topology, or discovery strategy is cheapest for Atento's three-agent composition.

```text
SYSTEM_COST_WINNER = NONE
COMPARABLE_THREE_ROLE_TOTAL_COST_RUNS = 0
GITHUB_DISCOVERY_COST_SAVING = HYPOTHESIS_NOT_MEASURED
SYSTEM_CHASSIS_HARD_GATES = DEFINED_NOT_EXECUTED
```

## Existing benchmark results mapped to Atento metrics

This is a documentary reuse of results already present in Atento. No score was recalculated and no test or benchmark was run for this report. Historical results stay in their original protocol and candidate scope.

| Existing result and note | Atento metric it informs | Scope and interpretation |
|---|---|---|
| PsyChat upstream static CFS: **10/100**; only routing_boundary passed. Explicit forkability seams: **0/5**. | CFS / architecture fitness; structural adaptation surface. | Anna/PsyChat upstream at its frozen pin. Indicates substantial structural adaptation for that RAG profile. It is not a three-agent isolation score or a total-cost grade. |
| PsyChat provider/lifecycle adaptation: **3 donor files**; full current BLOCO I correction: **4 donor files**. Snapshot: **1,410/1,600 lines retained = 88.125%**. Patched surface has **0 direct requests.post calls**. | Change surface, adapter/provider seam, retained upstream surface. | Existing partial structural cost evidence. The retention ratio is descriptive, not an acceptance threshold. Full patched runtime execution remains pending, so do not mark runtime quality or lifecycle cost PASS. |
| Letta experimental overlay: **0 core imports**, **0 host-core files changed**; general/therapeutic policy isolation PASS; bounded RAG outage PASS; disposer/removal PASS; **7 sequential mutations**, final regression PASS. | Change locality; scoped policy isolation; resilience; reversibility; regression after change. | Historical isolated prototype, not a complete Atento three-agent product. Supports a low-touch extension path within this fixture. Does not establish separate chats, credential isolation, Apollo, hours, or ongoing maintenance. |
| LibreChat control prototype: **0 core imports**; WhatsApp adapter PASS; memory isolation PASS; therapeutic policy isolation PASS; bounded RAG and Agents API outages PASS; **8 cumulative mutations**, final regression PASS; host harness unchanged. | Change locality; memory/policy isolation; resilience; reversibility/regression evidence. | Historical prototype/control. Its isolation assertions are bounded to this adapter fixture; they do not cover Atento's complete role, tool, credential, background, and consent contract. |
| NanoClaw representative recipes: WhatsApp **4 files / 1 import-index touchpoint / 4 dependencies**; OneCLI gateway **8 / 1 / 1 SDK**; OpenCode provider **40 / 5 / 1 SDK plus manifest/build touchpoints**; published Ollama recipe uncounted because it implies multiple manual core edits. | Change-surface and dependency burden. | NAIA-only partial static measurements. They show profile sensitivity: a repository cannot be assigned one “cheap” score without fixing the capability profile. They are not elapsed engineering hours or lifetime maintenance. |
| NAIA frozen candidate audit: **26/26** statically screened; **25 advanced**, SelfAgent stopped as a complete NAIA base at its pin; full comparable total-cost measurements **0/26**. | Hard-gate screening status and evidence coverage. | NAIA only. ADVANCED is not a system pass, and the SelfAgent stop does not eliminate it as a component in a different composition without testing that composition. |
| OrchBench (arXiv:2607.25656v1; study-reported): deterministic DAG simulation measures task quality, makespan, token use, and cross-agent information-transfer decisions. The authors report Pearson r = 0.816 against Claude Code execution quality; simulation used 1.3% of tokens and 10.3% of wall-clock time. | Workflow orchestration quality; handoff information retention; evaluation cost/efficiency. | Measures plans, not whole platforms/chassis. No role authorization, data/credential isolation, persistent runtime ownership, Atento adaptation, or maintenance cost. The reported correlation supports simulation signal in the paper's setup; it does not make simulated results equivalent to local Atento proof. |
| BenchLM agent-benchmark catalog (page data marked verified 2026-09-30): its displayed “Agentic Score” weights Terminal-Bench 2.0 (40%), OSWorld-Verified (35%), and BrowseComp (25%), normalized over available weights. Its displayed model leaders are Atria Dawn Preview 92.5, GPT-5.6 Sol 92.2, and GPT-6 Astra 91.5. | Later model/agent capability stage: multi-step computer/terminal work and web research, after the Atento model/provider/profile is frozen. | The composite is a model score, not a chassis score, and candidates may have different available benchmark subsets. Do not reuse its rank or recompute its composite as an Atento score. |
| BenchLM tool-use rows (page data marked verified 2026-09-30): MCP Atlas leader Muse Spark 1.1 88.1%; Toolathlon Muse Spark 1.1 75.6%; BFCL v4 BTL-3 88.5%. | Later model/tool capability stage: MCP/tool integration, tool selection/sequencing, schema and argument correctness. | Raw results stay in their own protocols. The catalog reports 0/42 owner/independent MCP Atlas rows, 0/26 Toolathlon rows, and 0/22 BFCL v4 rows; provider-reported results dominate. These do not establish Atento authorization, isolation, or handoff policy. |
| External AgentBalance result: reported performance gains up to **10% under matched token-cost budgets** and **22% under matched latency budgets** across its own benchmark setup. | Operational task quality, token cost, latency. | External inference/topology result only. It says nothing directly about adapting/maintaining Atento source code or role isolation. |
| External Efficient Agents v1: authors report **96.7%** of OWL performance and cost-of-pass improvement from **$0.398 to $0.228**; the arXiv record marks it work in progress. | Operational cost per successful task versus quality. | External GAIA result, different models/task/deployment. Not comparable with Atento engineering or lifecycle cost; its figures are not Atento estimates. |

## Mapping against the current system assertions

| Atento system metric / assertion | Existing evidence that can be reused | Status for complete NAIA + Anna + Apollo |
|---|---|---|
| SYS-CHAT-01 — isolated role chats and session continuity | No matched three-role result found in the chassis benchmark records reviewed. | NOT_ESTABLISHED |
| SYS-MEM-01 — cross-role private-memory denial | The Letta/LibreChat fixtures include bounded memory-isolation observations. | PARTIAL_COMPONENT_EVIDENCE; NOT_SYSTEM_PASS |
| SYS-TOOL-01 — tool authority and handoff reauthorization | Historical therapeutic-policy/tool-adapter tests provide a bounded policy signal; no complete typed handoff/recipient-authorization result is recorded in this chassis benchmark. | NOT_ESTABLISHED |
| SYS-CRED-01 — credential isolation | NanoClaw's OneCLI gateway surface is counted; that is an adaptation measure, not a cross-agent credential-denial outcome. | NOT_ESTABLISHED |
| SYS-HANDOFF-01/02 — minimal typed handoff, denial of implicit transfer | OrchBench measures DAG-level information-transfer decisions and retention effects in simulation; no permission/recipient reauthorization or implicit-transfer denial assertion. | PARTIAL_ORCHESTRATION_SIGNAL; AUTHORITY_NOT_ESTABLISHED |
| SYS-BG-01 — scheduler/retry/recovery retains role authority | Historical benchmark includes bounded interruption/recovery upstream tests for some donors, but no equivalent three-role background-authority assertion. | NOT_ESTABLISHED |
| SYS-STATE-01 — role-owned runtime/store/process state | Zero core imports and isolated fixture stores are useful architecture signals, not a full process/store/credential ownership proof across all three roles. | PARTIAL_COMPONENT_EVIDENCE; NOT_SYSTEM_PASS |
| Later model/agent capability — Terminal-Bench 2.0, OSWorld-Verified, BrowseComp / BenchLM Agentic Score | BenchLM publishes these as model benchmark results, with source-confidence labels and a weighted score normalized over available weights. | DEFERRED; no Atento model/provider/profile frozen; not chassis or role-boundary evidence |
| Later tool-use/model capability — MCP Atlas, Toolathlon, BFCL v4 | BenchLM publishes raw tool-use benchmark rows, mostly provider-reported at the checked page snapshot. | DEFERRED; can inform model/tool capability after profile freeze; cannot prove Atento tool authority, credential scope, or handoff reauthorization |
| Adaptation/change-surface cost | PsyChat donor-file counts and NanoClaw recipe touchpoints; Letta/LibreChat mutation counts. | PARTIAL_STRUCTURAL_MEASUREMENTS; no comparable complete-system total cost |
| Functional quality/safety | Anna-oriented benchmark registry and prototype assertions exist, but the system chassis comparison does not align their evaluated populations across candidates. | NOT_COMPARABLE_FOR_SYSTEM_SELECTION |
| Operational cost/latency | External papers provide separate token/$ and latency examples. No matched Atento composition result. | EXTERNAL_SIGNAL_ONLY |
| Ongoing maintenance cost | Historical upstream drift/rebase and change-surface observations are available for specific paths/windows. No equivalent ongoing maintenance hours or expense across whole compositions. | NOT_MEASURED_COMPARABLY |

**Metric note:** preserve each score and pass/fail exactly as its source records it. Do not convert CFS, mutation counts, source-file counts, behavioral benchmark scores, and model dollars into one aggregate “chassis note.” The Atento harness explicitly keeps these axes separate; any final decision must show the profile and its hard-boundary results.

## Sequential screening and common denominator

The decision proceeds in ordered stages rather than asking one score to represent every concern:

1. **Architecture + chassis stage:** assess whether each complete Atento composition can provide the required role boundaries and what it takes to adapt and maintain that structure. Keep CFS/change-surface observations separate from measured engineering and lifecycle cost.
2. **Subsequent metric stages:** apply one declared metric family at a time to the candidates that remain comparable, such as functional quality, safety, isolation assertions, reliability/recovery, latency, and operational cost.
3. **Common denominator:** retain the set of candidates that have the same declared scope/profile and comparable evidence for every metric required at that stage, while passing the non-negotiable gates. Report unresolved or blocked candidates separately; missing data is not a failure.
4. **Decision:** compare the survivors on the requested objective using the stage-specific evidence. Do not average unlike benchmark notes or use an overall score to hide a failed hard boundary.

Thus the current reused benchmark notes inform only the first architecture/chassis sieve where their scope transfers. They do not yet create a three-role denominator: the evidence is drawn from different candidate populations, profiles, and protocols.

## Defensible conclusion

The benchmark evidence supports being proactive about **testing alternatives** and measuring a cost-quality frontier. It does not prove that a wider GitHub search itself reduces cost. Discovery may find a closer-fitting integrated platform, while the search, qualification, integration, deployment, and update burden may offset that gain.

The claim we can carry forward is:

> A bounded, capability-based GitHub horizon scan is a reasonable way to search for lower-cost Atento compositions, but any saving must be demonstrated by a comparable three-role composition and lifecycle-cost measurement.

Do not choose a winner, shortlist, or numeric estimate from upstream benchmark scores, popularity, feature counts, README claims, or CFS alone.

### Minimum decision threshold

Use [`system-chassis-selection-metric-2026-10-02.md`](system-chassis-selection-metric-2026-10-02.md) as the operational rule for the **complete system chassis**. Eligibility requires 100% of the frozen suite's mandatory hard-gate assertions to pass, including zero observed unauthorized cross-role actions. This is a finite-suite acceptance criterion, not universal assurance. Blocked, missing, mocked-only, or non-comparable system evidence remains unresolved and cannot be used to rank or eliminate a candidate. Among eligible candidates with the same profile and cost-accounting horizon, compare total adaptation plus ongoing-maintenance cost; if required labor rates, horizon, or comparable measurements are missing, report the component vector and do not invent a scalar winner. The repository currently records zero comparable three-role cost runs and gates as defined but not executed.
## Minimum comparable Atento benchmark to close the question

For each candidate composition, freeze exact revisions and the same functional profile. Use the same task cases, model/provider or explicitly declared local model, token/tool budgets, deployment assumptions, and observation window. Run hard boundary assertions first: isolated chats/state/memory/tools/credentials, explicit minimal handoff with recipient-side reauthorization, and role-preserving scheduler/retry/recovery.

For candidates that pass the hard gates, record separately:

1. **Discovery and qualification effort:** query batches, repositories reviewed, exact pins frozen, engineering hours to decide fit, and evidence still missing.
2. **Adaptation effort:** elapsed active engineering time, files/lines and dependency changes, adapters/control-plane work, rework, and tests needed to produce the same Atento profile.
3. **Operational cost per successful task:** model/tool spend, token use, latency, failure/retry rate, and task quality under the fixed workload.
4. **Ongoing maintenance burden:** deployment/service count, upgrade effort/conflicts, security/policy revalidation, recovery/on-call work, and drift over an agreed observation window.
5. **Result:** hard-gate status plus distributions by candidate; no single composite score unless its weights and decision purpose are preregistered.

Count failed/blocked infrastructure as `INVALID/BLOCKED` rather than candidate failure. A bounded GitHub scan is itself included in the first cost category so discovery can be assessed instead of assumed to be free.

## Sources

- OrchBench v1 (arXiv:2607.25656): https://arxiv.org/abs/2607.25656 and https://arxiv.org/html/2607.25656v1

- Atento current composition contract and system discovery: `docs/evaluation/atento-system-architecture-chassis-rescreen-2026-09-30.md`.
- Historical multi-donor chassis benchmark: `docs/evaluation/chassis-selection-research-2026-09-29.md`.
- Existing PsyChat CFS/fork-surface results: `docs/evaluation/donor-candidate-comparison-research-2026-09-29.md`.
- NanoClaw partial surface results: `docs/evaluation/nanoclaw-change-surface-audit-2026-09-29.md`.
- Current cost audit: `docs/evaluation/naia-architecture-chassis-maintenance-cost-audit-2026-09-30.md`.
- Harness and CFS: `docs/evaluation/harness.md`.
- Current benchmark registry: `evals/config/benchmark_registry.json`.
- BenchLM LLM agent benchmarks (page data marked verified 2026-09-30): https://benchlm.ai/llm-agent-benchmarks
- BenchLM methodology: https://benchlm.ai/methodology
- BenchLM benchmark pages: https://benchlm.ai/benchmarks/terminal-bench-2, https://benchlm.ai/benchmarks/osworld-verified, https://benchlm.ai/benchmarks/browsecomp, https://benchlm.ai/benchmarks/mcpatlas, https://benchlm.ai/benchmarks/toolathlon, https://benchlm.ai/benchmarks/bfcl-v4
- Agentic Score weights and source-confidence counts are specific to the BenchLM page snapshot. The displayed model ranks are not independent evidence of chassis fitness; benchmark-specific provider/independent counts and raw scores must be read in their own pages.
- AgentBalance: https://arxiv.org/abs/2512.11426
- Efficient Agents: https://arxiv.org/abs/2508.02694

