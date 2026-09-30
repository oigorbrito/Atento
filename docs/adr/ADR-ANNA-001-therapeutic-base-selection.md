# ADR-ANNA-001 — Seleção do sistema-base da Anna

> **DECISION RESET — 2026-09-29:** esta ADR reabre do zero a decisão de chassis da Anna sem apagar medições, pins, benchmarks, auditorias ou gaps já observados.

## Document contract

A **Anna** é o agente emocional/terapêutico do produto Atento.

Esta ADR possui uma única responsabilidade: decidir, quando houver evidência suficiente, qual sistema funcional deve servir como base da Anna e qual modo de adoção minimiza o custo total de adaptação.

Ela não decide:

- a base da NAIA;
- a arquitetura do Apollo;
- a topologia de comunicação entre agentes;
- qual benchmark é canônico;
- licenças/provenance, que continuam em `docs/third-party.md`.

- **Status:** Reopened — `DECISION_RESET`
- **Decision:** `NOT_SELECTED`
- **Shortlist:** `NOT_SELECTED`
- **Date:** 2026-09-29

## Current candidate-universe evidence

Post-reset re-enumeration is recorded in:

`docs/evaluation/candidate-reenumeration-2026-09-29.md`

This record expands/classifies the candidate universe but does not alter this ADR's `NOT_SELECTED` state or create a shortlist.



Current equivalence/completeness audit:

`docs/evaluation/anna-candidate-completeness-audit-2026-09-29.md`

This audit partitions complete chassis from mechanism donors; it does not create a shortlist.

## Decision question

> Entre agentes terapêuticos/emocionais realmente comparáveis, qual sistema funcionando chega à Anna alvo com a menor mudança total, preservando a maior quantidade de capacidade útil já provada?

A decisão deve comparar:

```text
repair/adapt a working therapeutic system
vs
fork with localized changes
vs
wrap
vs
selective port
vs
greenfield/native
vs
hybrid
```

Não privilegiar arquitetura mais limpa apenas por estética.

Um defeito localizado em um sistema funcional pode custar menos para corrigir que reconstruir todo o produto em outro chassis.

## Candidate-equivalence rule

Antes de comparar, cada fonte precisa ser classificada.

```text
THERAPEUTIC_BASE_CANDIDATE
MECHANISM_DONOR
MODEL_OR_CHECKPOINT
BENCHMARK_OR_EVAL_SOURCE
UNCLASSIFIED_PENDING_AUDIT
```

Somente `THERAPEUTIC_BASE_CANDIDATE` entra diretamente na decisão de chassis.

Um projeto de RAG, modelo, dataset, benchmark ou mecanismo isolado não deve ser promovido a base completa apenas porque aparece no mesmo registry.

## Evidence already preserved

### PsychAgent

Pinned evidence:

`ECNU-ICALK/PsychAgent@469f45ef468b968b3fccd1936d7e6a0a574e4c5c`

Evidence already recorded includes:

- multi-session state;
- longitudinal profile/session summaries;
- planning;
- skill retrieval;
- multiple therapy schools;
- reward-guided rollout;
- resistance/avoidance/silence/defense patterns;
- runnable research Web surface;
- PsychEval/model-card and human multi-session evidence referenced by the prior audit.

Gaps already recorded include:

- demo-grade auth/privacy surface;
- no qualified independent crisis/suicide/escalation runtime established in the inspected source;
- incomplete public release relative to the paper-scale post-session evolution/training pipeline;
- terms not fully cleared in the prior audit.

**Current equivalence class:** `THERAPEUTIC_BASE_CANDIDATE`.

The historical characterization as a strong therapeutic engine remains evidence, not selection authority.

### TherapyMind

Pinned evidence:

`zx070326-hash/TherapyMind@bfed3f5be61bab262bb00a0f3cc9718c4a965243`

Evidence already recorded includes:

- modular prompt compilation;
- multi-role review chain;
- safety prompt patterns;
- grey-zone tests;
- profile/session persistence;
- prior full-donor/fork/lab-spike consideration.

**Current equivalence class:** `MECHANISM_DONOR`.

The previous `FULL_DONOR_CANDIDATE` label is not a current shortlist decision.

### PsyChat

Pinned evidence:

`wink-wink-wink555/PsyChat@5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4`

Evidence already recorded includes:

- Agentic RAG;
- RAG decision;
- query rewrite;
- multi-query retrieval;
- context expansion;
- FastAPI prototype;
- static chassis/change-surface work;
- corpus provenance findings.

The current Atento evidence is heavily concentrated in RAG/chassis adaptation.

**Current equivalence class:** `MECHANISM_DONOR`.

The completeness audit found the current pin to be primarily an Agentic-RAG/retrieval/style mechanism rather than a complete longitudinal Anna chassis.

### TheraMind — Emo-gml

Pinned evidence:

`Emo-gml/TheraMind@416d0a00ecc8c76229512197765dc95be6513de5`

Evidence already recorded includes:

- dual-loop turn/session planning;
- reaction/resistance evaluation;
- emotion/strategy selection;
- adaptive therapy switching.

Gaps already recorded include:

- JSON/file-backed state;
- hard-coded provider paths;
- state-access inconsistencies;
- no independent crisis/safety subsystem established in the inspected source.

**Current equivalence class:** `MECHANISM_DONOR`.

The current pin is an executable research therapist/patient simulation and remains valuable for dual-loop/adaptive-therapy mechanisms, but does not establish a product/runtime chassis comparable to Anna.

### OpenCouch

Pinned evidence:

`whanyu1212/OpenCouch@ac5af6ee4c9a06b4050c5a912439f343ade2c35c`

**Current equivalence class:** `THERAPEUTIC_BASE_CANDIDATE`.

The source audit establishes a durable emotional-support runtime with Postgres session/memory ownership, safety routing, crisis audit, guided exercises, web/TUI surfaces and observability. Upstream explicitly scopes itself as a supportive companion rather than a therapist, so Anna role/domain transfer remains a material audit before any shortlist decision.

### Inner Dialogue

Pinned evidence:

`ataglianetti/inner-dialogue@ffc9e8f78d0f15a8d720436f92fb6e0887fe7461`

**Current equivalence class:** `MECHANISM_DONOR`.

It provides persistent local profile/session conventions, therapy modalities, safety hooks/evals and update tooling, but relies on an external AI host rather than owning the inference/session runtime required by the current base-equivalence contract.

## Sources that are not automatically chassis candidates

The following sources remain valuable, but do not enter the chassis shortlist merely by existing in the therapeutic research set:

### Models / checkpoints / training systems

- SoulChat2.0 / PsyDT;
- EmoLLM;
- MindChat.

### Benchmarks / evaluation / mechanism references

- PsychEval;
- MentalHealthBench;
- CounselBench;
- PATIENT-Ψ;
- MHSafeEval;
- ENPMR-Bench;
- ESConv;
- AgentMental;
- User-Aware Active Knowledge Acquisition;
- CADSS / CPsDD;
- SAGE.

These can supply capabilities, tests, rubrics, datasets, architectural mechanisms or model components after the chassis decision.

## Anna target properties

A comparable therapeutic chassis should be audited for at least:

- coherent therapeutic/emotional interaction loop;
- longitudinal multi-session continuity;
- explicit state/profile/memory ownership;
- planning/strategy selection;
- support for uncertainty and clarification;
- resistance/evasion handling;
- safety and crisis boundary separable from generation;
- role-boundary robustness;
- privacy/auth/session isolation;
- provider/model replaceability;
- modularity and coupling;
- observability and testability;
- pt-BR transfer;
- adaptation/fork surface;
- upstream activity/maintenance;
- runtime completeness;
- cost and latency where measurable.

## Isolation requirement

Anna is a separate bounded agent.

By default she must not:

- read NAIA chat history;
- query NAIA private memory;
- invoke NAIA shopping/research/personal-side-effect tools;
- answer as a general personal assistant;
- inherit Apollo data or capabilities.

A request outside Anna's domain should not silently expand her authority.

The exact handoff topology remains undecided, but isolation is a required property of the final composition.

## Evidence reuse rule

Preserve and reuse:

- upstream benchmark results when the evaluated configuration is transferable;
- pinned source audits;
- static findings;
- runtime findings;
- known gaps;
- prior change-surface measurements;
- provenance findings.

Do not rerun them solely to create a new aggregate score.

Local testing is justified for:

- pt-BR transfer;
- Atento-specific adaptations;
- reserved/evasive subgroup behavior;
- independent safety integration;
- role-boundary adversarial behavior;
- memory/session isolation;
- privacy/auth/runtime changes;
- any material property not established upstream.

## Adaptation-cost rule

The base decision must measure total repair/adaptation cost, not merely architecture elegance.

Record at least:

```text
upstream capability preserved
files modified
donor internals modified
lines retained/replaced
new boundaries introduced
provider swap surface
storage swap surface
safety integration surface
session/memory isolation surface
runtime blockers
maintenance/upstream sync burden
estimated native rebuild effort
```

A candidate with localized defects can remain preferable if those defects are cheaper to repair than reconstructing equivalent mature capability elsewhere.

## Decision state

```yaml
agent: ANNA
role: EMOTIONAL_THERAPEUTIC_ASSISTANT
decision: NOT_SELECTED
shortlist: NOT_SELECTED
winner: NOT_SELECTED
adoption_mode: NOT_SELECTED
candidate_enumeration_complete: false
preserve_existing_measurements: true
reuse_existing_evidence: true
next_step: enumerate_and_reclassify_comparable_therapeutic_agent_chassis
```

## Acceptance criteria for a future decision

This ADR may leave `DECISION_RESET` only after:

- [ ] the candidate universe has been re-enumerated;
- [ ] complete chassis candidates are separated from donors/models/benchmarks;
- [ ] each finalist is pinned by repo + SHA/version;
- [ ] existing evidence has been reconciled without duplicate testing;
- [ ] runtime completeness is established for each finalist or absence is explicit;
- [ ] material Anna-specific deltas are tested;
- [ ] adaptation/change-surface is measured;
- [ ] safety/privacy/isolation blockers are characterized;
- [ ] pt-BR transfer risk is characterized;
- [ ] a fork/wrap/native/hybrid strategy is supported by evidence.

No previous ranking or “preferred” label satisfies these criteria by itself.
