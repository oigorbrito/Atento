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

## Evidence cross-check

| Evidence | What it actually measures | Relevance to this question | Limit |
|---|---|---|---|
| Atento historical chassis/evolvability benchmark (`docs/evaluation/chassis-selection-research-2026-09-29.md`) | Frozen, task-specific extension/replacement probes across Letta, Dify, Rasa, LibreChat, Open WebUI, AnythingLLM; change locality, touched files, imports, dependencies, reversibility, test outcomes, and upstream drift. Two prototype paths reported zero Atento-to-core imports; cumulative evolution was 7 mutations for Letta and 8 for the LibreChat control, with final regressions passing. | Best existing Atento evidence for whether some chassis seams support adding/removing integrations. Reusable S01–S10 scenarios and adapter/reversibility probes can inform the new harness. | Different candidate population and historical protocol; not the complete NAIA/Anna/Apollo system contract. It did not produce comparable total adaptation + lifecycle hours/cost, and it explicitly must not be retroactively converted to current CFS. The two prototype outcomes do not select a system chassis. |
| Current Atento Chassis Fitness Score (CFS), `docs/evaluation/harness.md` §7.11 | A static 10-check, 0–100 screening profile for routing, executor abstraction, registry, contracts, validation, provider/state/observability/resilience/safety boundaries; complementary change-surface metrics include files touched to add/swap components. | Useful for a common structural pre-screen and evidence capture. It can identify adaptation seams to probe next. | A static score is not measured effort, operating cost, total maintenance, or a security gate pass. No current CFS execution in this rescreen qualifies a full three-role composition. |
| NAIA cost audit (`docs/evaluation/naia-architecture-chassis-maintenance-cost-audit-2026-09-30.md`) | Static screen of 26 NAIA-role sources; NanoClaw has partial touchpoint counts (4–40 copied files across representative profiles). | Gives candidate-specific NAIA clues and a reusable cost taxonomy. | `0/26` comparable total-cost measurements. Partial file counts are not elapsed adaptation effort or lifetime maintenance and do not transfer to the whole Atento composition. |
| Current benchmark registry (`evals/config/benchmark_registry.json`) | Functional/domain benchmarks, mostly Anna-scoped; adapters are largely `planned`. Internal synthetic cases cover contracts, belief, memory, tools, safety, privacy, latency, and cost; `SHARED` is an available scope. Apollo benchmark research is `NOT_STARTED`. | Supplies functional/safety case sources and scope discipline for the harness. `SHARED` is appropriate for cross-agent assertions. | It is not a chassis integration-cost benchmark. Registry entries are not executed results; mixed-agent aggregates have no selection authority. |
| AgentBalance (arXiv:2512.11426) | Multi-agent task performance under matched token-cost and latency budgets; 14 candidate LLM backbones, with reported gains up to 10%/22% at matched token/latency budgets. | Supports measuring end-to-end task quality, token cost, and latency together; the paper reports that backbone choice can shift the cost-performance frontier. | Optimizes agent/backbone/topology inference behavior, not GitHub discovery effort, Atento role isolation, software adaptation, or ongoing code/deployment maintenance. Its percentages are not transferable to Atento. |
| Efficient Agents (arXiv:2508.02694, v1; authors label it work in progress) | GAIA cost-of-pass / operational model costs and task performance. The abstract reports 96.7% of OWL performance while reducing a stated cost from $0.398 to $0.228 and improving cost-of-pass by 28.4%. | Shows a benchmark can compare operational cost per successful task against quality instead of feature count alone. | Work-in-progress result and different benchmark/task/system. Measures inference/operation economics, not software adaptation or long-term maintenance; do not import its dollar values or percentage as an Atento forecast. |

## Defensible conclusion

The benchmark evidence supports being proactive about **testing alternatives** and measuring a cost-quality frontier. It does not prove that a wider GitHub search itself reduces cost. Discovery may find a closer-fitting integrated platform, while the search, qualification, integration, deployment, and update burden may offset that gain.

The claim we can carry forward is:

> A bounded, capability-based GitHub horizon scan is a reasonable way to search for lower-cost Atento compositions, but any saving must be demonstrated by a comparable three-role composition and lifecycle-cost measurement.

Do not choose a winner, shortlist, or numeric estimate from upstream benchmark scores, popularity, feature counts, README claims, or CFS alone.

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

- Atento current composition contract and system discovery: `docs/evaluation/atento-system-architecture-chassis-rescreen-2026-09-30.md`.
- Historical chassis benchmark: `docs/evaluation/chassis-selection-research-2026-09-29.md`.
- Current cost audit: `docs/evaluation/naia-architecture-chassis-maintenance-cost-audit-2026-09-30.md`.
- Harness and CFS: `docs/evaluation/harness.md`.
- Current benchmark registry: `evals/config/benchmark_registry.json`.
- AgentBalance: https://arxiv.org/abs/2512.11426
- Efficient Agents: https://arxiv.org/abs/2508.02694

