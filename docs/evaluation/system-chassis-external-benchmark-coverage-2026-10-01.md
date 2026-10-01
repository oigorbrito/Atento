# External benchmark coverage — system chassis cohort — 2026-10-01

## Purpose

This addendum checks published external benchmark results for every candidate in the fixed 11-item system chassis cohort. It reuses published scores and does not rerun any benchmark. It supplements the 2026-09-30 cross-check; where that earlier record said a score had not been reconciled for NanoClaw, this addendum records the Auto-ClawEval result found on 2026-10-01.

An external benchmark score can replace a repeat of that same benchmark only. Capability scores do not measure Atento adaptation cost, ongoing maintenance, or the three-role authority contract.

```text
FIXED_COHORT_CHECKED = 11
CANDIDATES_WITH_EXTERNAL_NUMERIC_RESULTS_FOUND = 4
CANDIDATES_WITH_NO_EXTERNAL_NUMERIC_RESULT_FOUND_IN_SOURCES_CHECKED = 7
COMPARABLE_EXTERNAL_THREE_ROLE_CHASSIS_COST_RESULTS = 0
OVERALL_CHASSIS_RANK = NOT_ESTABLISHED
```

“Not found” means not found in the bounded search and primary sources listed here; it is not a claim that no score exists anywhere.

## Candidate coverage

| Candidate | Published external result found | Comparison scope and transfer limit |
|---|---|---|
| NanoClaw | Auto-ClawEval, using Claude Haiku 4.5 for all harnesses: full suite mean score **63.7** (safety 94.6, completion 60.1, robustness 100.0); 104-task Auto-ClawEval-Mini mean **67.8** (99.0 / 60.8 / 100.0). | Same-run comparison with OpenClaw below. Paper does not pin this result to Atento's exact NanoClaw SHA. Capability/safety/robustness signal only; not Atento isolation acceptance or chassis cost. |
| AI Butler | No third-party candidate score found in the sources checked. Its own built-in live eval is **4/7** on its exact Atento pin. | The 4/7 is a first-party result on a distinct seven-task suite, not an external benchmark and not comparable with the other rows. Keep it in a separate evidence column. |
| OpenClaw | Auto-ClawEval with Claude Haiku 4.5: full suite **64.2** (93.8 / 61.3 / 100.0); Mini **64.2** (96.2 / 59.9 / 100.0). PawBench v1.0 mean **72.1**; ClawProBench: GLM-5.2 on OpenClaw v3.2.6 scored **80.05** on the 102-scenario open dataset and **56.1** on the 68-scenario closed dataset. | Auto-ClawEval is directly comparable to NanoClaw only within that benchmark. PawBench comparison is with QwenPaw only within PawBench. ClawProBench is a different model, runtime version, dataset, and scale; none is a three-role Atento chassis or lifecycle-cost score. |
| QwenPaw | PawBench v1.0 mean **73.7** across 9 models and 150 tasks. | Directly comparable with OpenClaw's 72.1 only within PawBench's published model × harness matrix. Benchmark harness release predates the Atento frozen pin; not a three-role system result. |
| MindRoom | No external candidate-specific numeric benchmark result found in the sources checked. | Source/test evidence remains as recorded in the system screen; no external benchmark rank. |
| Bob Labs | No external candidate-specific numeric benchmark result found in the sources checked. | Test definitions and source review are not benchmark outcomes; no external benchmark rank. |
| Ontheia | No external candidate-specific numeric benchmark result found in the sources checked. | Product documentation is not a benchmark outcome; no external benchmark rank. |
| OpenAkita | No external candidate-specific numeric benchmark result found in the sources checked. | Product documentation is not a benchmark outcome; no external benchmark rank. |
| Clawix | No external candidate-specific numeric benchmark result found in the sources checked. | README claims are not benchmark outcomes; no external benchmark rank. |
| Memoh | No external candidate-specific numeric benchmark result found for a frozen candidate pin. | The system screen still requires an exact commit pin; no score can be transferred to an unpinned source. |
| Letta Code | Terminal-Bench 2.0 historical results: **59.1% ± 2.4** with Claude Opus 4.5 (2025-11-24) and **53.5% ± 2.8** with GPT-5.1-Codex (2025-11-12). | These are separate model configurations on a different benchmark. They do not rank against PawBench or Auto-ClawEval and predate the current Atento pin. |

## Valid partial comparisons

### Auto-ClawEval: NanoClaw vs OpenClaw

The paper's Table 4 says every harness used Claude Haiku 4.5. On the full 1,040-environment benchmark, OpenClaw's mean score is 64.2 and NanoClaw's is 63.7 (+0.5 for OpenClaw). On the 104-task Mini, NanoClaw is 67.8 and OpenClaw 64.2 (+3.6 for NanoClaw). The direction changes on the compact subset, so keep both results visible and do not combine them. Both harnesses report 100.0 robustness in these aggregate rows; this does not test Atento's role-preserving scheduler/recovery assertion.

### PawBench v1.0: QwenPaw vs OpenClaw

The live v1.0 matrix reports means of 73.7 for QwenPaw and 72.1 for OpenClaw across the same nine models and 150 tasks (+1.6 for QwenPaw). QwenPaw wins 7 of 9 per-model pairings, ties one, and loses one. This is a valid partial capability ranking for the published harness releases only.

The live matrix's mean row differs from a separate summary paragraph in the repository README (which reports 74.9 and 72.9). For this record, the live matrix is used because its nine model × harness rows and date (2026-05-29) are explicit. Preserve the discrepancy; do not silently substitute the README summary or recompute a hybrid number. No new score was calculated.

### Separate scales

- ClawProBench measures OpenClaw execution under model GLM-5.2 at runtime v3.2.6. Its 80.05 open and 56.1 closed scores are not comparable to PawBench or Auto-ClawEval.
- Terminal-Bench 2.0 reports Letta Code with two distinct model setups. Preserve the rows separately.
- AI Butler's 4/7 remains first-party evidence, not an external result.

No aggregate across benchmark suites is valid here.

## What the external results can and cannot replace

The published Auto-ClawEval, PawBench, ClawProBench, and Terminal-Bench rows replace repeating those same benchmark evaluations for the same measured releases/configurations. They do not provide scores for the six other repositories or establish current Atento-pin performance.

External research did not produce a common benchmark score for all 11 candidates. Therefore:

```text
EXTERNAL_SCORE_COVERAGE = PARTIAL
SAME_BENCHMARK_COMPARISONS = [NanoClaw vs OpenClaw on Auto-ClawEval,
                              QwenPaw vs OpenClaw on PawBench]
CHASSIS_ADAPTATION_COST = NOT_MEASURED_BY_THESE_BENCHMARKS
THREE_ROLE_ISOLATION_AUTHORITY_HANDOFF = NOT_ESTABLISHED_BY_THESE_SCORES
PROVISIONAL_TOP_3_CHASSIS = NOT_ESTABLISHED
```

Do not assign zero to candidates without a published score. Record them as `NOT_FOUND_IN_SOURCES_CHECKED`. To fill those rows with a common external benchmark, that benchmark would need to support the frozen candidate releases under one model, task set, budget, and scoring setup; no such published common run was found in this bounded search.

## Primary sources checked

- ClawEnvKit / Auto-ClawEval v4, including Table 4: https://arxiv.org/html/2604.18543v4
- Auto-ClawEval benchmark dataset: https://huggingface.co/datasets/AIcell/Auto-ClawEval
- PawBench v1.0 live leaderboard: https://agentscope-ai.github.io/PawBench/en/
- PawBench methodology and result notes: https://github.com/agentscope-ai/PawBench/blob/main/README.md
- ClawProBench leaderboard: https://suyoumo.github.io/bench/
- ClawProBench method and metric: https://github.com/suyoumo/ClawProBench
- Terminal-Bench 2.0 leaderboard: https://www.tbench.ai/?version=2.0
- Candidate source records and exact pins: `docs/evaluation/atento-system-architecture-chassis-rescreen-2026-09-30.md`
