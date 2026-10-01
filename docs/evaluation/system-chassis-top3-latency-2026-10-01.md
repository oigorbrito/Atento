# Latency block — mobile chassis shortlist — 2026-10-01

## Scope and method

This is the latency block in the frozen metric sequence, after reliability/recovery. It reuses the existing Atento records and checked published benchmark evidence. No latency test or benchmark was executed or repeated for this note.

Latency must be tied to an observable boundary and workload. End-to-end assistant response time depends on model/provider, network, tool use, task difficulty, queueing, and runtime. Candidate-level numbers are comparable only when task set, model/provider, hardware/deployment, concurrency, timeout, and timing boundary align. This record does not combine latency with quality or operational cost.

## Existing shortlist evidence

| Candidate | Existing relevant external/internal score | Latency evidence usable for this ranking | Result |
|---|---|---|---|
| NanoClaw | Auto-ClawEval full mean 63.7 and Mini 67.8 with Claude Haiku 4.5; candidate/task score only. | No comparable candidate-specific latency figure recorded for the Atento pin or matching benchmark row. | **NOT_MEASURED_COMPARABLY** |
| QwenPaw | PawBench v1.0 mean 73.7 across 150 tasks and 9 models; published harness release differs from Atento pin. | No comparable candidate-specific latency distribution or common timing boundary recorded. | **NOT_MEASURED_COMPARABLY** |
| AI Butler | First-party exact-pin live eval 4/7; no independent external numeric score found in checked records. | No comparable candidate-specific latency result recorded. | **NOT_MEASURED_COMPARABLY** |

Auto-ClawEval's scores are not latency values. PawBench's recorded mean is task quality, not response duration. AI Butler's 4/7 is a first-party functional result, not a latency measurement.

## External evidence with limited transfer

| Source already checked | Published timing-related evidence | Why it does not rank this shortlist |
|---|---|---|
| AgentBalance (recorded in system-chassis-benchmark-crosscheck-2026-09-30.md) | Reports performance gains up to 22% under a matched latency budget in its own setup. | A quality-under-budget result, not per-candidate latency for NanoClaw, QwenPaw, or AI Butler. No Atento model/provider/runtime match. |
| OrchBench (same cross-check) | Reports a simulated evaluation using 10.3% of the wall-clock time of its comparison setup, plus correlation with execution quality. | Simulation/evaluation efficiency, not candidate response latency or three-role runtime timing. |
| Claw-SWE-Bench | Its paper/leaderboard defines mean wall-clock duration as a primary resource measure, with fixed prompts, task set, budget, and concurrency. Its evaluated claw sweep is OpenClaw, Hermes, ZeroClaw, Nanobot, and GenericAgent; it does not include NanoClaw, QwenPaw, or AI Butler. | Useful methodology for a future common coding-harness comparison, but its timing rows cannot be transferred to the three Atento candidates or the Atento mobile-assistant workload. OpenClaw is excluded from this active comparison by user direction. |

These findings do not produce a numeric order. Missing timing data is **NOT_FOUND / NOT_COMPARABLE**, not zero and not candidate failure.

## Gate result

```text
NEW_LATENCY_TESTS_OR_BENCHMARKS_RUN = 0
EQUIVALENT_LATENCY_TESTS_REPEATED = 0
COMPARABLE_EXTERNAL_LATENCY_RESULTS_FOR_ACTIVE_SHORTLIST = 0
NANOCLAW_LATENCY_RANK = NOT_ESTABLISHED
QWENPAW_LATENCY_RANK = NOT_ESTABLISHED
AI_BUTLER_LATENCY_RANK = NOT_ESTABLISHED
OVERALL_SHORTLIST_LATENCY_RANK = NOT_ESTABLISHED
```

No latency-based elimination or shortlist reorder is supported.

## Bounded next action

The next metric in the documented sequence is operational cost. Reuse external cost-per-task/cost-under-budget results only for their published task/model configurations; they do not replace Atento three-role operational cost. For latency itself, a local comparison would require a frozen Atento-relevant workload, fixed model/provider and deployment assumptions, and a stated timing boundary (for example, request accepted to first useful response, and request accepted to completed tool-backed response). Since the bounded external evidence contains no shared candidate-specific latency results, this block stops without launching a new benchmark.

## Sources

- Atento external benchmark cross-check: [system-chassis-benchmark-crosscheck-2026-09-30.md](system-chassis-benchmark-crosscheck-2026-09-30.md)
- Atento shortlist benchmark record: [system-chassis-top3-external-ranking-2026-10-01.md](system-chassis-top3-external-ranking-2026-10-01.md)
- Claw-SWE-Bench paper: https://arxiv.org/abs/2606.12344
- Claw-SWE-Bench leaderboard methodology and metrics: https://claw-swe-bench.github.io/
