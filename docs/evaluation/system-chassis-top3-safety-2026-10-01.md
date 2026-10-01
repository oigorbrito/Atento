# Safety evidence — mobile chassis shortlist — 2026-10-01

## Scope and method

This is the safety block for the mobile shortlist: NanoClaw, QwenPaw, and AI Butler. The declared metric sequence puts safety after functional quality. This record reuses existing published benchmarks, third-party security findings, and exact-pin Atento evidence. No test was repeated or executed for this note.

Scores are only ranked within the same benchmark and configuration. An external task-safety subscore is not a security certification and cannot satisfy Atento's role isolation, credential, handoff, or recovery gates.

## Comparable external benchmark result

Auto-ClawEval v4 uses Claude Haiku 4.5 across its evaluated harnesses. Its Table 4 includes NanoClaw and CoPaw, the former name of the QwenPaw project. It reports these safety subscores:

| Rank within this benchmark pair | Tested harness | Auto-ClawEval safety | Auto-ClawEval-Mini safety | Pairwise delta |
|---:|---|---:|---:|---|
| 1 | NanoClaw | 94.6 | 99.0 | — |
| 2 | CoPaw / QwenPaw lineage | 89.7 | 93.3 | NanoClaw +4.9 full; +5.7 Mini |
| — | AI Butler | NOT_TESTED | NOT_TESTED | No result |

This is a valid benchmark-specific rank for the historical harness builds evaluated in the paper, not an exact-pin result for the Atento candidates. The paper's CoPaw row predates/does not identify the frozen Atento QwenPaw commit. AI Butler is absent from this benchmark.

## Other external security evidence

| Candidate | External evidence | Scope and transfer limit |
|---|---|---|
| QwenPaw | A third-party article reports 5 of 6 planted skill attacks blocked and one bypass, across 18 personal-assistant tasks, on QwenPaw v1.1.7. | A scoped, individually conducted adversarial exercise, not a standardized comparison against NanoClaw or AI Butler. One bypass is actionable evidence; it is not a comparable rate against other candidates. |
| NanoClaw | A preprint's WhisperBench/MemGhost abstract reports transfer of its memory-injection attack to NanoClaw and Hermes. It reports 87.5% for OpenClaw/GPT-5.4 and 71.4% for Claude Code SDK/Sonnet 4.6, but no NanoClaw-specific rate. | Keep the attack-transfer claim as threat evidence. Do not attribute the other systems' rates to NanoClaw or rank it by a missing rate. |
| AI Butler | No independent candidate-specific safety/security benchmark result was found in the sources checked for this shortlist. | NOT_RANKED on the external security-test axis; absence is not zero. Its project-owned eval is first-party, not an external result. |

## Atento exact-pin evidence — separate from external ranking

| Candidate | Existing Atento evidence | Disposition for this safety block |
|---|---|---|
| NanoClaw | Hosted three-role profile run 36815873223 passed 7/7 with scope. It used synthetic role material and proved selected group/mount boundaries; provider/gateway credential custody and production runtime remain untested. | **PASS_WITH_SCOPE** for the tested boundaries; whole-system security gate remains open. |
| QwenPaw | Exact-pin source review identifies a sandbox-unavailable path that can broaden to unsandboxed ALLOW and cron authority needing hardening. Existing exact-pin full nightly failed; the main Tests status was incomplete. | **HOLD_FOR_FAIL_CLOSED_PROFILE**; the external benchmark and article do not close these Atento-specific gaps. |
| AI Butler | Exact-pin Atento ISO-1..ISO-6 run passed with scope at module/broker-adapter level. The same frozen pin's scheduled security workflow run 36426287353 failed with seven reachable advisories. | **BLOCK_CURRENT_PIN_ON_SECURITY**; a repaired, refrozen pin would need requalification. |

The Atento security dispositions come from existing records, not a new scan in this block: `docs/evaluation/system-chassis-gate2-continuation-2026-10-01.md` and `docs/evaluation/system-chassis-isolation-adaptation-cost-2026-10-01.md`.

## Safety block result

```text
EXTERNAL_AUTO_CLAWEVAL_PAIRWISE_ORDER = NanoClaw > CoPaw/QwenPaw-lineage
AI_BUTLER_EXTERNAL_SECURITY_RESULT = NOT_FOUND_IN_SOURCES_CHECKED
ATENTO_CURRENT_PIN_SECURITY_STATUS = {
  NanoClaw: PASS_WITH_SCOPE,
  QwenPaw: HOLD_FOR_FAIL_CLOSED_PROFILE,
  AI Butler: BLOCK_CURRENT_PIN_ON_SECURITY
}
NEW_TESTS_OR_SCANS_RUN = 0
FULL_ATENTO_SECURITY_PASS = 0
OVERALL_THREE_CANDIDATE_SAFETY_RANK = NOT_ESTABLISHED
```

No all-three safety ranking is defensible. The shared Auto-ClawEval subset ranks NanoClaw over the historical CoPaw/QwenPaw harness. The separate QwenPaw article identifies one attack bypass. AI Butler has no independent published score in the checked sources and its present Atento pin is separately blocked by a current security finding. Keep these as distinct evidence axes; do not average them.

## Primary sources

- Auto-ClawEval v4, Table 4 (same Claude Haiku 4.5; full and Mini safety rows): https://arxiv.org/html/2604.18543v4
- Official QwenPaw rebrand history from CoPaw (2026-04-12): https://github.com/agentscope-ai/QwenPaw/commit/bcaeb90
- Third-party QwenPaw security exercise (18 tasks, 6 planted attacks): https://pub.towardsai.net/i-planted-6-attacks-in-qwenpaws-18-tasks-its-guards-caught-5-and-the-6th-is-the-scary-one-0dce041b13d9
- WhisperBench/MemGhost preprint: https://arxiv.org/abs/2607.05189
- AI Butler project describes its eval as an internal harness: https://github.com/LumabyteCo/aibutler
