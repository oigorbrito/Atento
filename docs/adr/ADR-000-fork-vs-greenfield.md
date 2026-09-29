# ADR-000 — Fork vs Greenfield

## Document contract

Esta ADR possui **uma única responsabilidade**: decidir a estratégia de adoção de upstream para a base executiva do Atento.

Ela deve conter contexto, alternativas, evidência do spike, decisão e consequências. Não é roadmap, não é registry de licenças e não é benchmark spec.

A fonte canônica de progresso continua sendo `roadmap.md`; a fonte canônica de licenças/provenance é `docs/third-party.md`.

- **Status:** Proposed
- **Date:** TBD
- **Decision owners:** TBD

## Context

O Atento pode ser implementado como arquitetura própria, selective port, **full donor**, fork de um projeto existente, model adapter ou combinação dessas estratégias. O projeto autoriza adoção integral de donors quando a evidência mostrar vantagem. Esta ADR deve ser concluída antes da migração dos blocos para a base executiva definitiva.

## Candidates

### PsyChat
- Repo: https://github.com/wink-wink-wink555/PsyChat
- Commit avaliado: `5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4`
- Terms: MIT
- Current status: candidate for full donor / fork / selective port

### PsychAgent
- Repo: https://github.com/ECNU-ICALK/PsychAgent
- Commit avaliado: `469f45ef468b968b3fccd1936d7e6a0a574e4c5c`
- Terms: nenhuma licença de repo verificada na revisão
- Current status: external research clone / architecture donor candidate

### TherapyMind
- Repo: https://github.com/zx070326-hash/TherapyMind
- Commit avaliado: `bfed3f5be61bab262bb00a0f3cc9718c4a965243`
- Terms: MIT + contextual notice
- Current status: full donor / lab spike candidate

### TheraMind (Emo-gml) — supplemental candidate/donor
- Repo: https://github.com/Emo-gml/TheraMind
- Commit avaliado: `416d0a00ecc8c76229512197765dc95be6513de5`
- Terms: README limits use to research and education
- Current status: architecture/mechanism donor; not a cleared product-base candidate
- Important: **distinct project from TherapyMind above**

### SoulChat2.0 / EmoLLM / MindChat
Tratar primariamente como trilha de modelos/checkpoints, não como base do Executive Runtime.

## Block-migration rule

A decisão desta ADR deve mapear a estratégia escolhida para **blocos A–S completos**. Não definir migração por semanas, prompts ou frações artificiais.

Exemplo:

```text
BLOCO I — RAG
  adoption_mode: FULL_DONOR
  donor: PsyChat
  integration: Atento chassis

BLOCO E — Memory
  adoption_mode: SELECTIVE_PORT
  donor: PsychAgent
```

Project Points são usados para medir a evidência produzida durante a migração do bloco, não para fracionar a migração.

## Full donor rule

Adoção integral não é penalizada por princípio. O donor pode ser copiado/forkeado na íntegra para o estudo quando isso melhorar a solução de forma mensurável. A ADR deve comparar o donor integral com alternativas razoáveis usando o mesmo AtentoEval.

A autorização interna do projeto não substitui os termos externos de redistribuição; isso é registrado separadamente em `docs/third-party.md`.

## Evaluation matrix

Preencher de 0–5:

| Criterion | PsyChat | TherapyMind | Greenfield Atento |
|---|---:|---:|---:|
| External terms / redistribution note | | | n/a |
| Architecture fit | | | 5 |
| Benchmark evidence | | | |
| Code maturity | | | |
| Modularity | | | |
| Safety separation | | | |
| Data provenance | | | |
| Provider independence | | | 5 |
| Upstream value | | | n/a |
| Migration cost | | | |
| Chassis fitness | | | |

## Test log

### Test batch 1 — static chassis baseline
- **Status:** PARTIAL — source audit complete; CI runner unavailable.
- **Candidate:** PsyChat upstream
- **Pinned commit:** `5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4`
- **Static Chassis Fitness:** **10/100**.
- **Evidence:** `evals/spikes/psychat/static-baseline.md`.
- **CI condition:** workflow jobs repeatedly ended with `runner_id=0` and no steps; this is infrastructure evidence, not donor failure.

### Test batch 2 — forkability / extension seams
- **Status:** COMPLETE as static pinned-source audit.
- **Explicit extension seams passed:** **0/5**.
- **Thin-wrapper feasibility without donor edits:** **LOW**.
- **Evidence:** `evals/spikes/psychat/forkability-baseline.md`.
- **Interpretation:** PsyChat does not expose clean constructor/session/schema seams upstream. A maintainable adoption requires a fork patch or selective/block-level port rather than relying only on monkeypatching.

### Test batch 3 — Atento chassis adapter contract probe
- **Status:** IN_PROGRESS — contract surface expanded; current HEAD still lacks runner execution.
- **Current deterministic inventory:** **34 tests** across adapter/chassis/AtentoEval modules at the time of the latest inventory.
- **Historical results are not current evidence:** the earlier **11/11** local result and adapter-only **90/100 CFS** predate the current suite / ownership heuristic and must not be promoted to the current HEAD.
- **Git-measured minimal fork surface:** exactly **3 donor RAG files** in preserved Git evidence.
- **Static patched-source evidence:** provider calls are removed from those three files and model/embedding gateway seams plus external `force_retrieval` are present.
- **Integration defects found/fixed:** real donor mapping response shape; Router `force_retrieval` propagation; attempted-empty retrieval trace semantics; route/result identity enforcement; complete external trace-sink propagation.
- **Evidence:** `evals/spikes/psychat/adapted-baseline.md`.
- **Interpretation:** Atento boundaries materially improve replaceability, but current dynamic PASS/CFS numbers require execution on the present HEAD.

### Test batch 4 — real-source isolation + composed chassis
- **Status:** BLOCKED_BY_INFRA.
- **Probe:** `evals/spikes/psychat/real_isolation_probe.py`.
- **Composed audit:** donor source + Atento adapter are audited together so donor provider bypasses cannot be hidden by adapter-only scoring.
- **CI condition:** jobs are created but no workflow steps start; therefore no functional result is recorded yet.

### Test batch 5 — supplemental therapeutic-base audit (2026-09-29)

This batch did **not** compare every ADR candidate under one common AtentoEval run. It must not be interpreted as the final base ranking.

#### PsychAgent
- **Pinned commit:** `469f45ef468b968b3fccd1936d7e6a0a574e4c5c`.
- **Observed strengths:** multi-session state, longitudinal profile/session summaries, planning, skill retrieval, multiple therapy schools, reward-guided rollout, runnable research Web surface.
- **Evidence signal:** PsychEval/model-card evidence and human multi-session evaluation support the therapeutic mechanisms.
- **Observed resistance/evasion support:** skill library includes resistance, avoidance, silence, defense and gradual exploration patterns.
- **Product gaps:** demo-grade auth/privacy surface; no qualified crisis/suicide/escalation runtime found in inspected source.
- **Release gap:** public repo does not contain the complete paper-scale post-session evolution/training pipeline.
- **Terms blocker:** repository license was not detected; checkpoint terms were not cleared for product adoption in this audit.
- **Disposition:** strong therapeutic-engine reference/candidate, **adoption HOLD** pending terms, safety boundary and local transfer tests.

#### TheraMind (Emo-gml)
- **Pinned commit:** `416d0a00ecc8c76229512197765dc95be6513de5`.
- **Observed strengths:** dual-loop turn/session planning, reaction/resistance evaluation, emotion/strategy selection and adaptive therapy switching.
- **Observed chassis concerns:** JSON/file-backed state, hard-coded provider paths and concrete state-access inconsistencies in the public research implementation.
- **Safety:** no independent crisis/safety subsystem was established in the inspected source.
- **Terms blocker:** research/educational use only.
- **Disposition:** mechanism/architecture donor; not preferred as a direct product base.

#### Scope limitation
The result above means only:

```text
within the subset directly inspected in this batch:
PsychAgent showed stronger complete therapeutic-engine evidence than TheraMind
```

It does **not** mean:

```text
PsychAgent = final Atento therapist base
```

because PsyChat, TherapyMind and other ADR candidates still require the same decision protocol.

### Evidence references added by this batch

- **SRC-UKA** remains the primary Atento reference for belief state, uncertainty and active clarification.
- **SRC-AGENTMENTAL** adds a concrete information-gap / targeted-follow-up mechanism.
- **SRC-PATIENTPSI** adds patient-style robustness slices, especially reserved/evasive interaction.
- **SRC-MHSAFE** adds role-aware adversarial multi-turn safety evaluation.

### Retained local deltas for therapeutic candidates

Do not rerun complete external benchmarks merely to obtain another aggregate score.

Local tests remain justified for:

- Portuguese transfer;
- reserved/evasive subgroup degradation;
- information-gap behavior and premature-conclusion avoidance;
- therapist role-boundary adversarial prompts;
- independent crisis/safety integration;
- therapy-memory isolation;
- product-specific privacy/auth/runtime changes.

## Mandatory spike results

### Upstream execution
- [ ] PsyChat runs unchanged
- [ ] Dependencies documented
- [ ] Knowledge/data dependencies identified
- [ ] Baseline latency/cost captured

### Adapter experiment
- [x] Contract-level Model Gateway interception for known LLM paths
- [ ] Remove direct provider paths structurally in real donor fork
- [ ] Replace internal string route protocol in real donor with structured contract
- [x] Isolate vector/embedding call behind adapter contract in probe
- [x] Remove TTS from adapted core path in probe
- [x] Persist/restore session state outside donor runtime in probe
- [x] Add independent Safety Gate in probe
- [x] Add Capability Registry + Executor boundary
- [x] Add output Validator/Normalizer
- [x] Add tracing + retry/timeout boundary
- [ ] Execute all above against real pinned donor runtime

### AtentoEval comparison
- [ ] 20–50 seed cases
- [ ] upstream PsyChat
- [ ] adapted PsyChat
- [ ] clean-room Atento vertical slice
- [ ] cost
- [ ] p50/p95 latency
- [ ] quality
- [ ] strategy
- [ ] safety
- [ ] RAG/tool grounding as applicable

## Reuse accounting

Estimate after the adapter spike:

```yaml
upstream_core_loc:
loc_unchanged:
loc_modified:
loc_replaced:
percent_core_recognizably_retained:
estimated_fork_effort:
estimated_greenfield_effort:
```

A porcentagem de código retido é informativa, não decisiva. Full donor continua válido se o ganho sistêmico em tempo, qualidade, safety, custo e manutenção for melhor.

## Acceptance criteria

Para qualquer bloco usado como evidência de adoção, o respectivo readiness gate
deve primeiro indicar que o pacote de evidências está completo. Para o
**BLOCO I — RAG / PsyChat**, a fonte executável é:

`evals/spikes/psychat/block_i_readiness_gate.py`

A ADR não pode usar ausência de artefato como resultado implícito, nem promover
um PASS histórico de um HEAD anterior. Para o BLOCO I, a decisão exige
`ready_for_adr=true`.

Esta ADR só pode mudar de `Proposed` para `Accepted` quando:

- o upstream selecionado tiver sido executado sem alteração ou a impossibilidade estiver documentada;
- termos externos e estratégia de armazenamento/redistribuição tiverem sido registrados;
- houver report AtentoEval comparando as alternativas executáveis;
- os readiness gates dos blocos usados na decisão estiverem `ready_for_adr=true`;
- custo de adaptação vs clean-room tiver sido estimado;
- módulos mantidos/substituídos estiverem listados;
- riscos de safety/privacidade/provider coupling estiverem documentados;
- a decisão indicar estratégia de sync/rollback.

## Decision

```yaml
decision: TBD # full-donor | fork | selective-port | native | hybrid | model-adapter
primary_reason:
upstream_sync_strategy:
modules_reused:
modules_reimplemented:
model_strategy:
external_terms_note:
data_provenance:
```

## Consequences

TBD.
