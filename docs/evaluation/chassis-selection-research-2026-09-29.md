# Chassis selection research — reconciliação da rodada 2026-09-29

## Document contract

Este é o **registro canônico de evidência datada** para a rodada de chassis/evolvability de 2026-09-29.

Autoridade conforme `docs/documentation-map.md`:

- contém pins, fatos observados, probes, resultados, limitações e reconciliação;
- não redefine o AtentoEval;
- não altera progresso do projeto;
- não substitui ADR;
- não escolhe silenciosamente o sistema-base da Assistente.

Arquivo bruto da rodada:

`docs/research/chassis-selection-v1/archive/`

## 1. Reconciliação com as decisões canônicas

A rodada histórica terminou usando o rótulo:

`letta-ai/letta-code = EXECUTABLE_CHASSIS_SELECTED`

Esse rótulo é preservado **como resultado interno daquela rodada de benchmark**. No repositório canônico do Atento ele deve ser interpretado como:

`BENCHMARK_SELECTED_FOR_ARCHITECTURE_SCAFFOLD_ONLY`

Ele não equivale a:

`NAYA_ASSISTANT_BASE_SELECTED`

Estado canônico após reconciliação:

| Questão | Documento autoridade | Estado |
|---|---|---|
| Fork vs greenfield / modo de adoção | `ADR-000` | Proposed / aberta |
| Assistente × Terapeuta como bounded contexts | `ADR-001` | Proposed |
| Sistema-base da Assistente | `ADR-002` | `winner: NOT_SELECTED` |
| Evidência de chassis Letta/Dify/Rasa/LibreChat/Open WebUI/AnythingLLM | este registro | concluída para a rodada/pins abaixo |
| Progresso global | `roadmap.md` | não alterado por esta reconciliação |

Portanto, a evidência Letta pode informar ADR-000/ADR-002 e fornecer contratos/scaffold reutilizáveis, mas **não fecha essas decisões sozinha**.

## 2. Pergunta experimental

A rodada respondeu:

> Qual candidato, dentro do conjunto avaliado, apresenta o chassi mais defensável para evolução de longo prazo considerando locality of change, modularidade, substituibilidade, canais, memória, policy, failure isolation, reversibilidade e compatibilidade com upstream?

Ela **não** respondeu diretamente:

> Qual sistema completo deve ser a base final da Nayá Assistente?

A ADR-002 avalia essa segunda pergunta com critérios de produto persistente, restart/recovery, authority model, effect durability e local deltas. As duas avaliações são complementares, não intercambiáveis.

## 3. Baselines congelados

| Candidato | Source ID | SHA |
|---|---|---|
| Dify | `SRC-DIFY` | `7b0660b45b127a44b6467533ec6a8cd949586770` |
| Rasa OSS | `SRC-RASA` | `60a3cff9c08183760355b07bd60f5223d8916d6b` |
| LibreChat | `SRC-LIBRECHAT` | `63363a777612e0d37956cc5d233ac489f3a302c3` |
| Open WebUI | `SRC-OPENWEBUI` | `8bd8b4fac5e059578ac0c74b3c18d11139f88b7d` |
| Letta Code | `SRC-LETTA` | `a75111ea610eff9b4a37baba4fbc6ee24bb73c79` |
| AnythingLLM | `SRC-ANYTHINGLLM` | `a355703427c67c5be17bc57c4c5d5d034e275444` |

Flowise foi rejeitado no intake por upstream arquivado/EOL e não recebeu score arquitetural comparável.

## 4. Metodologia aplicada

Princípios:

1. SHA exato por candidato.
2. Observação independente antes de comparação.
3. Parity pass antes de decisão.
4. `NOT_FOUND` não convertido automaticamente em ausência.
5. Ambiguidade estática convertida em `REQUIRES_PROBE`.
6. Probes direcionados por hipótese arquitetural.
7. Mutações independentes separadas da evolução cumulativa.
8. Feature coverage e project health separados de architecture fitness.
9. Sem score global inventado quando pesos/medições não estavam defensáveis.

Estados de evidência:

`CONFIRMED | NOT_FOUND | UNCERTAIN | CONTRADICTORY | REQUIRES_PROBE | NOT_APPLICABLE`

## 5. Cenários benchmarkados

- S01 — tool/action extension;
- S02 — model provider;
- S03A — inbound primary channel;
- S03B — outbound/HITL channel;
- S03C — event/trigger;
- S04A — blob/file storage;
- S04B — domain persistence;
- S04C — conversation memory;
- S04D — resume/lock/checkpoint state;
- S05 — assistant-context/policy isolation;
- S06A — vector backend;
- S06B — retrieval strategy;
- S06C — ingestion/data source;
- S06D — full RAG pipeline;
- S07 — failure isolation;
- S08 — cross-cutting policy;
- S09 — upstream/fork maintenance;
- S10 — reversibility/removal.

Métricas observadas quando aplicáveis:

- files changed;
- core files changed;
- unrelated modules touched;
- central selector/registry edits;
- dependency changes;
- cross-boundary imports;
- tests broken;
- cycles;
- removal residue;
- rebase conflicts;
- failure containment;
- reversibility.

## 6. Resultado dos probes direcionados

### Dify

- tool/model plugin: zero-touch host registration observado;
- vector backend: wiring central adicional observado;
- primary WhatsApp-like channel: composição externa;
- bom substrate RAG/workflow, mas esse resultado não prova fit como sistema-base Nayá.

### Rasa OSS

- channels/tracker/lock/event: seams explícitas e limpas;
- modern LLM/vector-RAG: não encontrado como substrate nativo equivalente;
- maintenance mode foi tratado como gate de adoção separado, não como score arquitetural.

### LibreChat

- deployment plugins/MCP/custom compatible endpoints: baixo core touch;
- RAG: boundary externa explícita;
- primary WhatsApp e long-term memory: composição externa/Atento-owned no protótipo.

### Open WebUI

- dynamic Tool/Filter layer: baixo core touch;
- vector/file storage: abstrações existem, porém novos backends ainda passam por wiring central;
- primary external messenger: composição externa.

### Letta Code

- mod tool: zero core registration edit observado;
- local provider mod: zero core registration edit no escopo local;
- user channels: discovery sem editar registry central;
- WhatsApp: first-party channel;
- memory/identity/recall: primitivas do chassi;
- permission overlays: approval + execution;
- classic vector RAG: não nativo; composição externa foi escolhida no scaffold experimental.

### AnythingLLM

- imported skills/MCP: baixo core touch;
- generic OpenAI-compatible path: configuração;
- native provider/vector additions: selector central;
- Telegram nativo; nenhuma channel seam genérica equivalente ao Letta foi estabelecida.

## 7. Experimentos executáveis

### Letta

Protótipo isolado:

- channel/tool/provider/policy/RAG adapter;
- 0 imports de core Letta;
- 0 host-core files alterados no harness;
- general/therapeutic policy isolation: PASS;
- RAG outage bounded: PASS;
- disposer/removal: PASS.

Evolução cumulativa:

- 7 mutações sequenciais;
- final regression: PASS;
- core imports: 0.

CI oficial no SHA congelado:

- exact SHA checkout;
- frozen-lock install;
- lint/typecheck;
- bundle build;
- update-chain smoke;
- unit/API integration matrices;
- package/local-backend smokes.

Um job `gemini-3.6-flash` falhou por Google AI HTTP 503/high demand. Foi registrado como provider availability failure, não como prova de regressão arquitetural.

Também foram observados no baseline testes upstream para:

- rollback de partial assistant message após interrupção;
- resume/recovery retry;
- user-channel discovery;
- MessageChannel extension;
- mod tool/provider/permission loading;
- per-agent mod isolation;
- permission recheck após transformação de argumentos;
- execution-phase ask bloqueado/fail-closed.

### LibreChat — controle

Protótipo independente:

- external WhatsApp adapter → Agents API;
- memory sidecar por agent ID;
- therapeutic PreToolUse policy;
- external RAG boundary.

Resultado:

- core imports: 0;
- WhatsApp adapter: PASS;
- memory isolation: PASS;
- therapeutic policy isolation: PASS;
- RAG outage bounded: PASS;
- Agents API outage bounded no adapter: PASS.

Evolução cumulativa:

- 8 mutações;
- final regression: PASS;
- host harness file unchanged.

## 8. Upstream/forkability

### Letta

Em janela aproximada de um mês várias superfícies usadas pelo Atento ficaram byte-identical, incluindo:

- `src/channels/plugin-registry.ts`;
- `src/mods/types.ts`;
- `src/mods/capabilities.ts`;
- `src/mods/README.md`;
- `src/skills/builtin/creating-mods/SKILL.md`;
- `src/skills/builtin/creating-mods/references/permissions.md`.

Foi executada simulação de rebase por interseção de paths usando paths reais alterados no upstream observado: `PASS_NO_TEXTUAL_CONFLICT`.

Risco residual: Mods do Letta priorizam repairability e podem sofrer breaking changes. Mitigação experimental documentada: pin + contract tests + upgrade revalidation.

### LibreChat

Na janela observada de 578 commits:

- deployment plugin loader/runtime permaneceu byte-identical;
- hooks tiveram mudanças modestas;
- RAG context handling foi refatorado;
- `RAG_API_URL` permaneceu como boundary.

## 9. Scaffold F0–F5 produzido pela rodada

O scaffold é **evidência experimental reutilizável**, não implementação canônica já adotada no Atento:

- F0: upstream-core + Atento-overlay ownership; core-drift guard;
- F1: contratos C01–C08;
- F2: vertical probe general/therapeutic + removable RAG;
- F3: managed mod package `@atento/runtime-overlay`;
- F4: fork seed + bootstrap + CI contract runner em fixture;
- F5: change classifier para overlay/core exception/upstream migration.

Resultado experimental final: 0 core exceptions reais no scaffold.

## 10. Relação com ADR-002

A ADR-002 compara OpenMausBot, NaIA e OpenClaw como **sistemas-base completos da Assistente**.

Este benchmark comparou um conjunto diferente sob a ótica de **chassis/evolvability**.

Logo:

- Letta não deve ser inserido retroativamente como winner da ADR-002;
- OpenClaw/OpenMausBot/NaIA não devem ser descartados porque não participaram desta mesma rodada de chassis;
- um eventual uso de Letta como base definitiva exigiria aplicar os gates materiais da ADR-002/ADR-000 de forma comparável;
- os contratos/probes desta rodada podem ser reutilizados para isso.

## 11. O que pode ser reutilizado agora

Sem fechar ADR:

- protocolo de observação/paridade;
- cenários S01–S10;
- change-locality probes;
- add/remove reversibility;
- failure injection contracts;
- core-drift classifier;
- upstream contract lock;
- RAG-as-removable-sidecar pattern;
- permission recheck pattern;
- ownership `upstream core + overlay` como hipótese de fork.

## 12. O que não foi provado

Esta rodada não concluiu:

- qualidade conversacional/terapêutica;
- safety clínica;
- AtentoEval full comparison;
- throughput/tokens/s;
- custo;
- latência;
- production-load scalability;
- product completeness para Nayá;
- winner da ADR-002.

## 13. Archive

A íntegra dos artefatos técnicos produzidos na rodada está em:

`docs/research/chassis-selection-v1/archive/`

O archive é histórico. Se houver divergência, prevalecem as autoridades canônicas:

`AGENTS.md → roadmap.md → ADRs → docs/evaluation/harness.md → docs/third-party.md → documentation-map`.
