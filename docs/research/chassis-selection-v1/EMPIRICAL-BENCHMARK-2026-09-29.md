# Benchmark empírico de chassis — 2026-09-29

> **Classificação:** histórico / referência de consulta.  
> **Escopo:** documenta os testes empíricos e benchmarkados executados durante a rodada de seleção de chassis do Atento.  
> **Não é:** benchmark de features, benchmark de performance ou instrução de continuidade.

## 1. Pergunta experimental

A rodada tentou responder:

> Qual candidato oferece o chassi mais defensável para um fork de longo prazo do Atento, considerando locality of change, modularidade, substituibilidade, memória, canais, policy, falha controlada, reversibilidade e compatibilidade com upstream?

A pergunta foi deliberadamente separada de:

- quantidade de features prontas;
- número de integrações;
- stars/forks;
- UI/polimento;
- marketing do projeto;
- performance de inferência sem relação com arquitetura.

## 2. Regras metodológicas aplicadas

1. **SHA exato por candidato.** Nenhuma conclusão arquitetural foi baseada apenas em `main`.
2. **Observação antes de comparação.** Cada candidato recebeu seu próprio evidence pack.
3. **Paridade antes de score/decisão.** Resultado diferente era permitido; profundidade de investigação diferente, não.
4. **`NOT_FOUND` não significava automaticamente ausência.**
5. **Ambiguidade estática virava `REQUIRES_PROBE`.**
6. **Probe direcionado testava hipótese arquitetural**, não “adicionar feature por adicionar”.
7. **Mutações independentes** e **evolução cumulativa** eram tratadas separadamente.
8. **Feature coverage** e **project health** ficaram fora da métrica de architecture fitness.
9. **Nenhum score numérico global** foi usado quando pesos/medições não eram defensáveis.

Vocabulário de evidência:

- `CONFIRMED`
- `NOT_FOUND`
- `UNCERTAIN`
- `CONTRADICTORY`
- `REQUIRES_PROBE`
- `NOT_APPLICABLE`

## 3. Candidatos e baselines congelados

| Candidato | Repositório | SHA congelado | Observação |
|---|---|---|---|
| Dify | `langgenius/dify` | `7b0660b45b127a44b6467533ec6a8cd949586770` | pacote normalizado para protocolo v1.1 |
| Rasa OSS | `RasaHQ/rasa` | `60a3cff9c08183760355b07bd60f5223d8916d6b` | maintenance mode tratado como risco de adoção separado |
| LibreChat | `LibreChat-AI/LibreChat` | `63363a777612e0d37956cc5d233ac489f3a302c3` | controle executável |
| Open WebUI | `open-webui/open-webui` | `8bd8b4fac5e059578ac0c74b3c18d11139f88b7d` | — |
| Letta Code | `letta-ai/letta-code` | `a75111ea610eff9b4a37baba4fbc6ee24bb73c79` | selecionado |
| AnythingLLM | `Mintplex-Labs/anything-llm` | `a355703427c67c5be17bc57c4c5d5d034e275444` | — |
| Flowise | `FlowiseAI/Flowise` | — | rejeitado no intake: upstream arquivado/EOL |

O repositório antigo `letta-ai/letta` foi explicitamente descartado como implementação atual; a avaliação foi redirecionada para `letta-ai/letta-code`.

## 4. Cenários arquiteturais benchmarkados

O protocolo congelado separou capacidades que poderiam parecer “uma feature” em subproblemas arquiteturais distintos:

| ID | Cenário |
|---|---|
| S01 | extensão de tool/action |
| S02 | adição/substituição de model provider |
| S03A | canal primário inbound |
| S03B | canal outbound / HITL |
| S03C | trigger/evento |
| S04A | file/blob storage |
| S04B | persistência de domínio |
| S04C | memória conversacional |
| S04D | resume/lock/checkpoint state |
| S05 | isolamento de contexto/policy entre assistentes |
| S06A | vector backend |
| S06B | retrieval strategy |
| S06C | ingestion/data source |
| S06D | pipeline RAG completo |
| S07 | failure isolation |
| S08 | policy cross-cutting |
| S09 | upstream/fork maintenance |
| S10 | reversibilidade/removal |

## 5. Métricas usadas nos probes

Nos probes de mudança eram registrados, quando observáveis:

- arquivos alterados;
- arquivos de core alterados;
- módulos não relacionados tocados;
- necessidade de editar registry/switch central;
- novas dependências;
- imports atravessando fronteiras;
- testes quebrados;
- possibilidade de disposer/removal;
- duplicação;
- ciclos/import-boundary violations;
- conflitos de rebase;
- resíduo após remoção;
- necessidade de novo subsistema;
- falha confinada vs falha compartilhada.

Interpretação usada:

- **zero-touch extension**: extensão pelo mecanismo pretendido sem editar registro/core do host;
- **config compatibility**: capacidade obtida por configuração/endpoint compatível;
- **central edit**: extensão exige alteração em selector/registry central;
- **external composition**: capacidade fica fora do host e usa API/service/tool boundary;
- **new subsystem**: o chassi não oferece aquela seam nativamente.

## 6. Probes direcionados M7 — resultados observados

### Dify

- **Tool plugin:** `PASS_CHANGE_LOCALITY`; 0 arquivos de registro do host observados.
- **Model provider:** `PASS_CHANGE_LOCALITY`; resolução via plugin runtime/factory.
- **Vector backend:** `PARTIAL_CORE_WIRING`; pelo menos 2 arquivos centrais no caminho documentado:
  - `api/core/rag/datasource/vdb/vector_type.py`
  - `api/pyproject.toml`
- **Canal primário WhatsApp-like:** nenhum port inbound nativo foi estabelecido; composição externa via API.
- **Fault injection:** não executado no host local por bloqueio de materialização do repo.
- **Upstream proxy:** janela curta; sem conclusão de longo prazo.

### Rasa OSS

- **Custom channel:** 0 edições centrais observadas quando carregado por module/class path.
- **Tracker/lock/event/policy:** seams por base class/configuração.
- **LLM/RAG moderno:** `NO_NATIVE_SEAM` no baseline clássico avaliado.
- **Fault injection:** não materializado localmente.
- **Upstream:** ausência de churn não foi tratada como vantagem porque a linha avaliada estava em maintenance mode.

### LibreChat

- **Deployment plugin:** 0 edições de registro do host observadas.
- **MCP:** extensão via configuração/runtime registry.
- **Model endpoint:** OpenAI-compatible/custom endpoint por configuração.
- **RAG:** boundary explícita de serviço externo via `RAG_API_URL`.
- **Canal primário:** sem port nativo WhatsApp; adapter externo necessário.
- **Fault injection:** posteriormente executado no protótipo de controle.

### Open WebUI

- **Tool/Filter plugin:** 0 edições de registro do host observadas.
- **OpenAI-compatible endpoint:** extensão por configuração.
- **Vector backend:** pelo menos 2 pontos centrais:
  - `backend/open_webui/retrieval/vector/type.py`
  - `backend/open_webui/retrieval/vector/factory.py`
- **File storage backend:** abstração existe, mas seleção central permanece em `backend/open_webui/storage/provider.py`.
- **Canal primário externo:** adapter externo necessário.

### Letta Code

- **Mod tool:** 0 edições de registro do host observadas.
- **Mod provider:** 0 edições de registro do host no backend local; scope limitation documentada para agentes API-managed.
- **User channel:** descoberta por manifest/user channel, sem edição de registry central.
- **WhatsApp:** first-party `ChannelPlugin`.
- **Backend:** contrato comum `Backend` + `BackendCapabilities`.
- **Policy:** permission overlays em approval e execution.
- **RAG clássico:** `NO_NATIVE_RAG_SEAM`; decisão foi compor como serviço/tool/MCP removível.

### AnythingLLM

- **Imported skill:** 0 edições de registro do core observadas.
- **MCP:** extensão dinâmica/configurada.
- **Generic OpenAI provider:** caminho compatível por configuração.
- **Novo provider nativo:** pelo menos 1 selector central em `server/utils/helpers/index.js`.
- **Novo vector backend:** pelo menos 1 selector central no mesmo helper.
- **Mensageria:** Telegram nativo; nenhuma interface genérica de channel nem WhatsApp nativo foi estabelecida.
- **Unattended execution:** comportamento de aprovação exigiu ressalva específica para jobs sem canal HITL.

## 7. Modelo de evolução cumulativa M8

A evolução cumulativa não foi convertida em score arbitrário. O modelo carregou a **classe do mecanismo de mudança** para uma sequência Atento:

1. tool/MCP;
2. provider;
3. WhatsApp/canal primário;
4. memória longa;
5. policy/safety;
6. RAG/vector/retrieval;
7. segundo contexto de assistente;
8. regressão/rebase.

Resumo qualitativo observado:

| Mudança | Dify | Rasa | LibreChat | Open WebUI | Letta | AnythingLLM |
|---|---|---|---|---|---|---|
| Tool/MCP | zero-touch | zero-touch | zero-touch | zero-touch | zero-touch | zero-touch |
| Provider | zero-touch | new subsystem | config | config | scope-limited zero-touch | config |
| WhatsApp | external | zero-touch | external | external | zero-touch/native | new subsystem |
| Memória longa | coupled existing | new subsystem | new subsystem | coupled existing | first-class/native | coupled existing |
| Policy | coupled/conditional | new subsystem | plugin/hook | filter/plugin | permission overlay | conditional/new layer |
| RAG | native, some central wiring | new subsystem | external service | native, central wiring | external/new subsystem | native, central selector |
| Segundo contexto | config | config | config | config | native agent/context seam | config |

## 8. Experimento executável — Letta Code

### 8.1 Protótipo Atento isolado

Foi criado um protótipo executável com:

- user/channel boundary;
- mod tool;
- local provider;
- therapeutic permission overlay;
- RAG HTTP sidecar removível.

Resultado observado:

- **0 imports de core do Letta**;
- **0 arquivos do host alterados** no protótipo;
- policy general/therapeutic isolada;
- RAG outage confinada ao tool;
- disposer removeu registrations;
- namespace RAG posteriormente passou a ser derivado de `ctx.agent.id`, não escolhido pelo modelo.

### 8.2 Evolução cumulativa

Foram aplicadas **7 mutações sequenciais** no protótipo Letta:

1. channel;
2. tool;
3. provider;
4. therapeutic policy;
5. segundo contexto de assistente;
6. RAG adapter;
7. fault/regression test.

Resultado:

- regressão final: **PASS**;
- host harness alterado: **não**;
- core imports: **0**;
- registros removíveis: **PASS**.

### 8.3 CI oficial no SHA congelado

No SHA `a75111ea610eff9b4a37baba4fbc6ee24bb73c79` foram observados workflows oficiais com:

- checkout do SHA exato;
- `bun install --frozen-lockfile`;
- lint/typecheck;
- bundle build;
- update-chain smoke;
- unit tests em múltiplos shards/OS;
- API integration tests;
- package build/install;
- CLI smoke;
- local-backend headless smoke;
- provider/headless scenarios.

Um job global ficou vermelho em `Headless / gemini-3.6-flash` por respostas repetidas do Google AI `HTTP 503 UNAVAILABLE / high demand`. Isso foi classificado como indisponibilidade externa de provedor, não como regressão do chassi.

### 8.4 Testes upstream relevantes observados no host real

No baseline exato foram encontrados/executados testes cobrindo:

- `interrupt rolls back unpersisted partial assistant message before reload`;
- retry de stream após primeiro resume failure;
- retry de recovery drain;
- descoberta de user channels por `channel.json`;
- extensão do `MessageChannel` por user plugin;
- tool mods;
- provider mods;
- permission overlays;
- isolamento/reload de mods por agente;
- rechecagem de permission overlays depois de `tool_start` transformar argumentos;
- execution-phase `ask` tratado como bloqueio, não execução silenciosa.

## 9. Experimento executável — LibreChat controle

O controle recebeu um protótipo independente com:

- WhatsApp adapter externo → Agents API;
- memory sidecar separado por agent ID;
- therapeutic `PreToolUse` policy;
- RAG adapter/service boundary.

Resultados:

- `coreImports: 0`;
- WhatsApp external composition: **PASS**;
- memory isolation general/therapeutic: **PASS**;
- therapeutic hook isolation: **PASS**;
- RAG outage bounded: **PASS**;
- Agents API outage bounded no adapter WhatsApp: **PASS**.

Evolução cumulativa de **8 mutações**:

1. WhatsApp adapter;
2. MCP/tool deployment extension;
3. compatible model endpoint;
4. therapeutic policy;
5. assistant contexts;
6. long-term memory sidecar;
7. RAG adapter;
8. regression/fault test.

Resultado: **PASS** com 0 alterações no arquivo host do harness.

## 10. Estabilidade/upstream

### Letta

Foi feita comparação temporal das superfícies usadas pelo Atento. Em janela aproximada de um mês, várias permaneceram byte-identical:

- `src/channels/plugin-registry.ts`;
- `src/mods/types.ts`;
- `src/mods/capabilities.ts`;
- `src/mods/README.md`;
- `src/skills/builtin/creating-mods/SKILL.md`;
- `src/skills/builtin/creating-mods/references/permissions.md`.

Mudanças em channel types/documentação foram observadas como aditivas.

Também foi executada uma **simulação de rebase por interseção de paths** usando paths realmente alterados no upstream observado. Resultado: `PASS_NO_TEXTUAL_CONFLICT`.

Risco residual documentado: a API de Mods do Letta prioriza **repairability** e admite breaking changes. Mitigação: pin de SHA/versão + contract tests antes de upgrade.

### LibreChat

Em amostra de aproximadamente um mês, com **578 commits** no intervalo observado:

- deployment plugin loader/runtime: byte-identical;
- hooks: mudanças modestas;
- RAG context handling: refatorado;
- boundary `RAG_API_URL`: preservada.

## 11. Scaffold empírico F0–F5

Os experimentos posteriores transformaram as conclusões em invariantes executáveis:

- **F0:** ownership `upstream core + Atento overlay`, guard de core drift;
- **F1:** contratos C01–C08, inclusive fixtures negativas;
- **F2:** vertical probe general/therapeutic + external RAG + reversibility;
- **F3:** pacote `@atento/runtime-overlay` construído e importado dinamicamente;
- **F4:** bootstrap de fork + CI runner em Git fixture; wrong-SHA refusal testado;
- **F5:** classifier de change control testado em Git:
  - `OVERLAY_ONLY` passa;
  - `INVALID_CORE_DRIFT` bloqueia;
  - `CORE_EXCEPTION_ONLY` passa;
  - `INVALID_MIXED_CHANGE` bloqueia.

No final de F5: **0 core exceptions reais**.

## 12. O que não foi benchmarkado

Para evitar extrapolação indevida, esta rodada **não** produziu conclusão sobre:

- throughput;
- tokens/s;
- latência de modelo;
- custo de inferência;
- qualidade clínica;
- taxa de sucesso terapêutico;
- escalabilidade de produção sob carga;
- segurança ofensiva completa;
- disponibilidade operacional de provedores externos.

Também não houve score numérico 1–100 final, porque pesos arbitrários teriam reduzido a defensabilidade do resultado.

## 13. Receita de reprodução recomendada

Para repetir o benchmark em novos candidatos:

```text
1. freeze exact SHA
2. inventory architecture boundaries
3. fill evidence pack independently
4. parity pass
5. create independent worktree per probe
6. run targeted mutation
7. collect changed-files/core-churn/tests/deps
8. run cumulative mutation branch
9. inject bounded failures
10. add/remove extension
11. compare/rebase against newer upstream
12. only then compare candidates
```

Git recomendado:

```bash
git clone <repo> candidate
cd candidate
git checkout <frozen-sha>

git worktree add ../probe-tool <frozen-sha>
git worktree add ../probe-provider <frozen-sha>
git worktree add ../probe-channel <frozen-sha>
git worktree add ../cumulative <frozen-sha>
```

Cada probe deve preservar:

- comando executado;
- SHA;
- diff;
- `git diff --stat`;
- arquivos de core tocados;
- testes antes/depois;
- logs de falha;
- resultado de removal;
- conflitos de rebase.

## 14. Relação com o archive bruto

A evidência bruta da rodada está preservada nesta mesma branch em:

`docs/research/chassis-selection-v1/archive/`

O archive contém protocols, evidence packs, parity, probes, M8–M11, executable gates, scaffold F0–F5, scripts e handoffs.

Este documento é a camada **empírica legível** sobre esse material bruto.
