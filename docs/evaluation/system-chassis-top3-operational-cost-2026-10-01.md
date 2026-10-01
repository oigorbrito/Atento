# Operational cost block — mobile chassis shortlist — 2026-10-01

## Scope and method

This is the operational-cost block after latency in the bounded sequential comparison. It reuses existing internal records and external benchmark publications. No benchmark, candidate test, or cost simulation was run or repeated.

Keep two distinct cost families:

1. **Operating cost:** inference/API and tool charges, hosting/compute/storage/network, and service/deployment overhead for a stated task volume and observation window.
2. **Engineering and lifecycle cost:** discovery, qualification, adaptation, upgrade, rework, maintenance, security review, and operations effort.

A benchmark's cost-per-task replaces a repeat only for its exact task/model/provider/runtime configuration. It is not a chassis cost or a three-role Atento bill. Do not estimate totals where usage volume, model/provider, service topology, or resource measurements are absent.

## Active shortlist: comparable operating-cost evidence

| Candidate | External benchmark result already reused | Operating-cost evidence usable for candidate ranking | Atento/internal cost evidence | Disposition |
|---|---|---|---|---|
| NanoClaw | Auto-ClawEval full 63.7 / Mini 67.8 with Claude Haiku 4.5, scores only in the reconciled record. | No candidate-specific dollar/task, provider usage, hosting bill, or common workload cost for the Atento pin in the checked records. | 7/7 hosted profile assertions used inert local fixtures and no live provider calls; therefore not an operational-cost run. Existing recipe counts measure source touchpoints, not runtime expense. | **NOT_MEASURED_COMPARABLY** |
| QwenPaw | PawBench v1.0 mean 73.7 for harness v1.1.3 over 150 tasks and 9 models; Atento pin differs. | PawBench provides a Model × Harness evaluation and identifies cost/trace quality as diagnostic dimensions, but the public leaderboard and inspected per-submission JSON expose scores/task counts rather than candidate cost or token totals. No usable QwenPaw cost value for this ranking. | No common Atento workload, provider usage, deployment bill, or three-role cost result recorded. | **NOT_MEASURED_COMPARABLY** |
| AI Butler | No independent external numeric benchmark score in the checked candidate record; own 4/7 live eval remains first-party and distinct. | No candidate-specific external operational-cost result found in the checked records. | Current pin's CI/scheduler/isolation results do not record a common production-like bill or per-successful-task cost. Its pin is separately security-blocked. | **NOT_MEASURED_COMPARABLY** |

External performance results remain separate: Auto-ClawEval and PawBench scores do not reveal comparable system operating costs. The Atento test evidence also cannot serve as a cost denominator because harness tests use synthetic data and do not exercise a common live model/provider workflow.

## External cost research already recorded

| External study | Existing published number | What it can tell us | Transfer limit |
|---|---|---|---|
| Efficient Agents v1 / GAIA | Authors report retaining 96.7% of OWL performance while operational cost changed from $0.398 to $0.228; the paper reports a 28.4% cost-of-pass improvement. | Cost-per-success is a useful metric alongside task quality. | Different framework, models, GAIA tasks, and deployment. No number transfers to NanoClaw, QwenPaw, AI Butler, or Atento. |
| AgentBalance | Up to 10% performance gain under matched token-cost budgets and up to 22% under matched latency budgets, in its own benchmark experiments. | Agent topology/model choice can change quality under a fixed cost or latency budget. | These are performance gains under controlled budgets, not operating-cost measurements for the active candidates or Atento. |
| PawBench v1.0 | The project defines model × harness comparison and indicates cost/trace inspection for model selection. The public 2026-05-29 leaderboard and inspected QwenPaw submission JSON do not provide per-candidate dollar/task or token totals. | It can replace repeated quality evaluation for the same published configuration; its cost dimension cannot be used from the exposed rows checked here. | QwenPaw's 73.7 score is not a cost score; NanoClaw and AI Butler are not in its evaluated harness set. |
| Claw-SWE-Bench | Reports cost alongside quality and duration for coding harnesses; the paper's tested cross-harness set does not contain the active three candidates. | Method reference for publishing quality and cost together under a shared budget. | No candidate result transfers to this shortlist or to the Atento personal-assistant workload. |

## Engineering/lifecycle cost remains separate

The current Atento records do not provide a comparable total operating-cost vector or a comparable adaptation-and-maintenance vector for any active candidate.

- NanoClaw has profile-specific static recipe counts (WhatsApp 4 files / 1 import / 4 dependencies; OneCLI 8 / 1 / 1 SDK; OpenCode 40 / 5 / 1 SDK plus manifest/build). These are structural touchpoints, not hours, API expense, or upkeep.
- AI Butler and QwenPaw have no comparable adaptation or operating-cost measurement in the current records.
- The historical Letta and LibreChat fixture mutation counts, and PsyChat's Anna/RAG-specific donor-file counts, are not measurements for the active mobile shortlist or full three-role Atento system.

Do not combine code touchpoints, paper cost-per-pass, API token usage, and hosting expense into one score.

## Gate result

```text
NEW_COST_TESTS_OR_BENCHMARKS_RUN = 0
EQUIVALENT_COST_BENCHMARKS_REPEATED = 0
COMPARABLE_EXTERNAL_COST_PER_TASK_ROWS_FOR_ACTIVE_SHORTLIST = 0
COMPARABLE_ATENTO_OPERATIONAL_COST_RUNS = 0
COMPARABLE_ADAPTATION_AND_MAINTENANCE_TOTALS = 0
NANOCLAW_COST_RANK = NOT_ESTABLISHED
QWENPAW_COST_RANK = NOT_ESTABLISHED
AI_BUTLER_COST_RANK = NOT_ESTABLISHED
OVERALL_OPERATIONAL_COST_RANK = NOT_ESTABLISHED
SYSTEM_CHASSIS_WINNER = NONE
```

No cost-based elimination or overall ranking is supported. Missing evidence is unranked, not zero and not failure. AI Butler's security block and QwenPaw's fail-closed hold remain independent hard-gate dispositions; low or unknown operating expense could not override them.

## Bounded next step

The sequential metric blocks now have recorded evidence through operational cost. The shortlist has no common Atento operating-cost or lifecycle-cost denominator, and the full system hard gates remain incomplete. Any future cost run should occur only after a comparable composition passes required hard gates and should freeze: one workload and success definition, model/provider and tool prices, request volume, retry policy, runtime/deployment topology, resource monitoring, and observation window. Report cost per successful task and fixed-period infrastructure separately. Do not run an open-ended benchmark or repeat any published benchmark already represented.

## Sources

- Atento external benchmark and cost mapping: [system-chassis-benchmark-crosscheck-2026-09-30.md](system-chassis-benchmark-crosscheck-2026-09-30.md)
- Atento candidate cost/isolation record: [system-chassis-isolation-adaptation-cost-2026-10-01.md](system-chassis-isolation-adaptation-cost-2026-10-01.md)
- Atento external candidate score record: [system-chassis-external-benchmark-coverage-2026-10-01.md](system-chassis-external-benchmark-coverage-2026-10-01.md)
- Efficient Agents: https://arxiv.org/abs/2508.02694
- AgentBalance: https://arxiv.org/abs/2512.11426
- PawBench public benchmark repo/results: https://github.com/agentscope-ai/PawBench and https://agentscope-ai.github.io/PawBench/en/
- Inspected QwenPaw result row (Qwen 3.6 Plus, 150 tasks): https://github.com/agentscope-ai/PawBench/blob/main/submissions/pawbench-4models-opusjudge-20260529__qwen3.6-plus__qwenpaw.json
- Claw-SWE-Bench: https://arxiv.org/abs/2606.12344
