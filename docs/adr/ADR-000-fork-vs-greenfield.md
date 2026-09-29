# ADR-000 — Fork vs Greenfield

## Document contract

Esta ADR possui **uma única responsabilidade**: decidir a estratégia de adoção de upstream para a base executiva do Atento.

Ela deve conter contexto, alternativas, evidência do spike, decisão e consequências. Não é roadmap, não é registry de licenças e não é benchmark spec.

A fonte canônica de progresso continua sendo `roadmap.md`; a fonte canônica de licenças/provenance é `docs/third-party.md`.

- **Status:** Proposed
- **Date:** TBD
- **Decision owners:** TBD

## Context

O Atento pode ser implementado como arquitetura própria, selective port de módulos externos, fork de um projeto existente ou combinação dessas estratégias. Esta ADR deve ser concluída antes do bootstrap da base de produção.

## Candidates

### PsyChat
- Repo: https://github.com/wink-wink-wink555/PsyChat
- Commit avaliado: `5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4`
- License: MIT
- Current status: candidate for spike/selective port

### PsychAgent
- Repo: https://github.com/ECNU-ICALK/PsychAgent
- Commit avaliado: `469f45ef468b968b3fccd1936d7e6a0a574e4c5c`
- License: nenhuma licença de repo verificada
- Current status: architecture/reference only

### TherapyMind
- Repo: https://github.com/zx070326-hash/TherapyMind
- Commit avaliado: `bfed3f5be61bab262bb00a0f3cc9718c4a965243`
- License: MIT + contextual notice
- Current status: lab spike candidate

### SoulChat2.0 / EmoLLM / MindChat
Tratar primariamente como trilha de modelos/checkpoints, não como base do Executive Runtime.

## Evaluation matrix

Preencher de 0–5:

| Criterion | PsyChat | TherapyMind | Greenfield Atento |
|---|---:|---:|---:|
| License fit | | | 5 |
| Architecture fit | | | 5 |
| Benchmark evidence | | | |
| Code maturity | | | |
| Modularity | | | |
| Safety separation | | | |
| Data provenance | | | |
| Provider independence | | | 5 |
| Upstream value | | | n/a |
| Migration cost | | | |

## Mandatory spike results

### Upstream execution
- [ ] PsyChat runs unchanged
- [ ] Dependencies documented
- [ ] Knowledge/data dependencies identified
- [ ] Baseline latency/cost captured

### Adapter experiment
- [ ] Replace direct DeepSeek call with Atento Model Gateway adapter
- [ ] Replace string decision parsing with structured contract
- [ ] Isolate vector store behind interface
- [ ] Remove TTS from core path
- [ ] Persist session outside process memory
- [ ] Add minimal independent Safety Gate

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
estimated_fork_to_mvp_days:
estimated_greenfield_to_mvp_days:
```

If less than ~40% of the upstream core remains recognizably useful after provider abstraction, structured contracts, memory, safety and observability, prefer selective port or greenfield.

## Acceptance criteria

Esta ADR só pode mudar de `Proposed` para `Accepted` quando:

- o upstream selecionado tiver sido executado sem alteração ou a impossibilidade estiver documentada;
- licença do código e dos dados relevantes tiver sido verificada;
- houver report AtentoEval comparando as alternativas executáveis;
- custo de adaptação vs clean-room tiver sido estimado;
- módulos mantidos/substituídos estiverem listados;
- riscos de safety/privacidade/provider coupling estiverem documentados;
- a decisão indicar estratégia de sync/rollback.

## Decision

```yaml
decision: TBD # fork | selective-port | clean-room | hybrid
primary_reason:
upstream_sync_strategy:
modules_reused:
modules_reimplemented:
model_strategy:
license_review:
data_review:
```

## Consequences

TBD.
