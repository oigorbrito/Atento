# External test ranking — mobile chassis shortlist — 2026-10-01

## Scope

This note compares the three mobile-focus candidates recorded in Atento: NanoClaw, QwenPaw, and AI Butler. It reuses published third-party results; it does not rerun benchmarks. Only identical benchmark/task/model configurations support a direct rank. Scores from different benchmarks are not combined.

## Valid direct comparison: Auto-ClawEval

The Auto-ClawEval v4 paper reports the same model, Claude Haiku 4.5, for all tested harnesses. It lists NanoClaw and CoPaw (QwenPaw's former project name) in the same table, with scores for the full 1,040-environment suite and its 104-environment Mini subset.

| Rank in this benchmark comparison | Tested harness | Auto-ClawEval full mean | Mini mean | Difference |
|---:|---|---:|---:|---|
| 1 | NanoClaw | 63.7 | 67.8 | — |
| 2 | CoPaw / QwenPaw lineage | 60.8 | 59.3 | NanoClaw +2.9 full; +8.5 Mini |
| — | AI Butler | NOT_TESTED | NOT_TESTED | No result in this benchmark |

This is the only direct performance rank available between candidates in this shortlist. The benchmark evaluates harness capability on its generated tasks; it does not evaluate Atento role isolation, handoff authority, adaptation cost, or ongoing maintenance. The table's CoPaw result is a historical build under the former name, not the frozen Atento QwenPaw pin. The NanoClaw benchmark result is also not pinned to Atento's exact candidate SHA. Treat the order as a benchmark-specific lineage comparison, not exact-pin qualification.

## Other external results — separate ranks and tests

| Candidate | External result already published | Valid inference | Not established |
|---|---|---|---|
| QwenPaw | PawBench v1.0: mean 73.7 over the same 150 tasks and 9 models. In that benchmark, QwenPaw v1.1.3 ranked above the other two tested harnesses, Hermes (68.4) and OpenClaw (72.1). | QwenPaw ranked first among PawBench's three harnesses for that tested release/configuration. | PawBench did not include NanoClaw or AI Butler, so it cannot reorder the three-candidate shortlist. It is not an Atento pin score. |
| QwenPaw | A third-party security article reports 5 of 6 planted skill attacks blocked and 1 getting through, across 18 personal-assistant tasks, using QwenPaw v1.1.7. | Adversarial test found a concrete missed attack path; retain as a scoped warning. | The exercise is not the Atento isolation contract or a comparable NanoClaw/AI Butler security run. It is not a standardized cross-candidate leaderboard. |
| NanoClaw | WhisperBench preprint reports that its memory-injection attack transfers to NanoClaw and Hermes. Reported end-to-end success rates (87.5% OpenClaw, 71.4% Claude Code SDK) are not NanoClaw-specific. | Relevant external threat evidence for persistent-agent memory; it justifies retaining memory-injection as a security risk class. | No NanoClaw-specific numeric score is reported in the abstract; do not assign one or rank it against QwenPaw. |
| AI Butler | No independent candidate-specific numeric benchmark or external security result was found in the sources checked for this shortlist. The candidate's own eval is separate. | External numeric position is **NOT_RANKED**. | Absence is not zero or proof of poor capability. |

AI Butler's repository describes `aibutler eval` as an internal benchmark. The previously recorded 4/7 live result is first-party evidence, so it does not enter this external ranking.

## Ranking outcome

```text
AUTO_CLAWEVAL_HEAD_TO_HEAD = NanoClaw > CoPaw/QwenPaw-lineage > AI Butler NOT_TESTED
PAWBENCH = QwenPaw > OpenClaw > Hermes (separate benchmark; NanoClaw and AI Butler absent)
THREE_CANDIDATE_OVERALL_EXTERNAL_RANK = NOT_ESTABLISHED
THREE_CANDIDATE_SHARED_EXTERNAL_BENCHMARK_COVERAGE = 0
EXTERNAL_ISOLATION_OR_ADAPTATION_COST_RANK = NOT_ESTABLISHED
```

Therefore the defensible ranking is **partial**: NanoClaw beats the tested CoPaw/QwenPaw lineage in both Auto-ClawEval suites; QwenPaw leads PawBench but that benchmark has no NanoClaw or AI Butler row; AI Butler has no independent external score in the sources checked. No single score can reconcile these results without mixing benchmark scopes. This ranking does not change the separate Atento hard gates: AI Butler's frozen pin remains security-blocked in the existing Atento record, QwenPaw's sandbox fallback/background-authority gaps remain open, and NanoClaw's three-role test remains PASS_WITH_SCOPE.

## Primary sources

- Auto-ClawEval v4, Table 4 (model fixed at Claude Haiku 4.5; NanoClaw and CoPaw rows; full and Mini results): https://arxiv.org/html/2604.18543v4
- Official QwenPaw repository history, CoPaw rebrand to QwenPaw (2026-04-12): https://github.com/agentscope-ai/QwenPaw/commit/bcaeb90
- PawBench v1.0 live matrix and leaderboard (150 tasks, 9 models, 3 harnesses; data dated 2026-05-29): https://agentscope-ai.github.io/PawBench/en/
- PawBench evaluation README/methodology: https://github.com/agentscope-ai/PawBench/blob/main/README.md
- Third-party QwenPaw security exercise: https://pub.towardsai.net/i-planted-6-attacks-in-qwenpaws-18-tasks-its-guards-caught-5-and-the-6th-is-the-scary-one-0dce041b13d9
- WhisperBench / MemGhost preprint: https://arxiv.org/abs/2607.05189
- AI Butler repository's own eval-harness description: https://github.com/LumabyteCo/aibutler
- Existing Atento evidence and exact-pin caveats: `docs/evaluation/system-chassis-external-benchmark-coverage-2026-10-01.md`, `docs/evaluation/system-chassis-isolation-adaptation-cost-2026-10-01.md`, `docs/evaluation/system-chassis-gate2-continuation-2026-10-01.md`
