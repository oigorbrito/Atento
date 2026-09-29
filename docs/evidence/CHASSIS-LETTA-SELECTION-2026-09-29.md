# Handoff retrospectivo — Atento

> **Escopo deste documento:** registrar somente o que já foi realizado, testado, decidido e documentado.
> Ele **não** contém instrução de continuidade, próximo passo, marcador de retomada ou ordem para outro chat iniciar execução.

## 1. Estado consolidado

O benchmark arquitetural foi concluído com **`letta-ai/letta-code`** como chassi selecionado no SHA congelado:

`a75111ea610eff9b4a37baba4fbc6ee24bb73c79`

Estado registrado:

`EXECUTABLE_CHASSIS_SELECTED`

O **LibreChat** permaneceu como candidato de controle/fallback. A seleção foi feita por qualidade/forkabilidade arquitetural, não por quantidade de features.

Também foi concluído um **scaffold de fork F0–F5**. Durante a execução do benchmark/scaffold ele permaneceu em sandbox/fixtures, sem aplicação ao fork de produto. Posteriormente, este material histórico foi publicado em uma branch de documentação/pesquisa do próprio repositório Atento para preservação remota.

---

## 2. Metodologia que ficou documentada

A avaliação foi reorganizada para não confundir **produto pronto** com **qualidade do chassi**.

A ordem metodológica documentada ficou:

```text
Purpose / use cases
        ↓
Quality attribute scenarios
        ↓
Architecture reconnaissance
        ↓
Risks / sensitivities / trade-offs
        ↓
Targeted architecture probes
        ↓
Cumulative evolution test
        ↓
Comparative decision
```

Referenciais utilizados e documentados:

- ISO/IEC/IEEE 42030:2019 — Architecture Evaluation Framework;
- ISO/IEC/IEEE 42010:2022 — Architecture Description;
- ISO/IEC 25010:2023;
- ISO/IEC 25023;
- ISO/IEC 5055:2021;
- SEI QAW;
- SEI ATAM;
- CISQ;
- CNCF Technical Due Diligence / Day-0;
- evidências GitHub/CI/dependency graph;
- OpenSSF Scorecard como dimensão de higiene separada da qualidade arquitetural.

O protocolo passou por **V1** e depois foi congelado como **V1.1**, com execução por blocos, candidato por candidato, usando SHA exato e mantendo paridade dos testes.

---

## 3. Resultado comparativo documentado

### Letta Code

Forças observadas para o Atento:

- channel/WhatsApp nativo;
- memória/estado nativos;
- mods/tools como boundary dedicada;
- providers/mods;
- permission overlays;
- política com fase de approval e fase de execution;
- isolamento de mods por agente;
- forte encaixe para separar assistente geral e terapêutica.

Dívida estrutural principal assumida pelo Atento:

- RAG externo/removível.

### LibreChat

Forças observadas:

- plugin/MCP boundary madura;
- RAG externo como fronteira natural;
- hooks utilizáveis para policy;
- protótipo cumulativo sem edição do host.

Dívidas principais para o Atento:

- WhatsApp externo;
- memória longa própria.

A comparação levou à manutenção do Letta como principal e LibreChat como controle.

---

## 4. Evidência executável do Letta no SHA congelado

O SHA exato foi observado em GitHub Actions oficial com:

- checkout do commit exato;
- `bun install --frozen-lockfile`;
- lint/typecheck;
- build;
- update-chain smoke;
- matriz de testes unitários e API integration;
- package/local-backend smoke.

O CI ficou globalmente vermelho por um job `Headless / gemini-3.6-flash`, mas o log mostrou repetidos **Google AI HTTP 503 / high demand**. Isso foi classificado como indisponibilidade externa do provedor, não como regressão do chassi.

Foram localizados no mesmo SHA testes executados e aprovados para pontos críticos do Atento, incluindo:

- rollback de assistant message parcial após interrupção e antes de reload;
- retry de stream no resume/recovery;
- descoberta de user channel plugin;
- extensão de schema do `MessageChannel`;
- tool registration por mod;
- provider registration por mod;
- permission overlays;
- isolamento de mods por agente;
- rechecagem de permission overlay depois de `tool_start` alterar argumentos;
- bloqueio de `ask` na fase de execution.

Essas evidências permitiram promover o status de:

`PROVISIONAL_SOURCE_ARCHITECTURE_SELECTION`

para:

`EXECUTABLE_CHASSIS_SELECTED`

---

## 5. Compatibilidade/upstream já analisada

Foi feita verificação de estabilidade de superfícies relevantes.

Na janela observada de aproximadamente um mês, ficaram byte-for-byte estáveis, entre outras:

- `src/channels/plugin-registry.ts`;
- `src/mods/types.ts`;
- `src/mods/capabilities.ts`;
- `src/mods/README.md`;
- `src/skills/builtin/creating-mods/SKILL.md`;
- `src/skills/builtin/creating-mods/references/permissions.md`.

Foram observadas mudanças aditivas em superfícies de channel types/documentação, sem invalidar o boundary.

Também foi documentado o risco residual: o sistema de Mods do Letta prioriza **repairability** sobre promessa permanente de backwards compatibility. Por isso o scaffold passou a exigir pinning de upstream e contract tests para upgrades.

---

## 6. Scaffold de fork já produzido

### F0 — Baseline e ownership

**PASS**

Foi documentado:

- baseline congelado;
- modelo `upstream core + Atento overlay`;
- `CORE_EXCEPTIONS` inicialmente vazio;
- protocolo de upgrade;
- guard de core drift.

### F1 — Extension skeleton e contratos

**PASS**

Foi criado o esqueleto:

```text
atento/
  channels/
  mods/
  policy/
  rag/
  contracts/
  packaging/
  scripts/
```

Foram definidos contratos arquiteturais **C01–C08**, cobrindo core drift, imports internos, channel boundary, policy terapêutica, RAG removível, isolamento de memória/identidade, reversibilidade e contract lock de upstream.

Também foram executadas fixtures negativas para provar que as violações são detectadas.

### F2 — Vertical probe mínimo

**PASS**

Foi executado um probe vertical contendo:

- envelope de canal com forma de WhatsApp;
- seleção de contexto general/therapeutic;
- namespaces de memória separados;
- policy terapêutica;
- RAG HTTP externo;
- falha RAG limitada ao tool;
- registro e descarte de tools/policy;
- zero import interno do Letta.

### F3 — Packaging bridge

**PASS**

Foi produzido e testado um pacote managed-mod:

`@atento/runtime-overlay`

O pacote:

- registra policy terapêutica;
- registra RAG somente se configurado;
- exige ID explícito do agente terapêutico;
- deriva namespace RAG de `ctx.agent.id`;
- não permite o modelo escolher namespace de memória/RAG;
- usa apenas a shape pública injetada de `letta.*`;
- remove registrations por disposer.

### F4 — Fork seed e CI

**PASS**

Foi produzido:

- fork seed;
- bootstrap com verificação de Git checkout limpo;
- validação do SHA esperado;
- recusa de SHA incorreto;
- CI contract runner;
- exemplo de GitHub Actions mantido em `atento/ci/`.

O bootstrap foi testado em repositório Git sintético.

### F5 — Modelo de branches/commits e change-control

**PASS**

Foram definidos os tipos:

- `OVERLAY_ONLY`;
- `CORE_EXCEPTION_ONLY`;
- `INVALID_CORE_DRIFT`;
- `INVALID_MIXED_CHANGE`;
- `UPSTREAM_MIGRATION`.

Também foi criado classifier executável para path sets/PR diff e testado que:

- mudança só em overlay passa;
- mudança em core sem exceção falha;
- exceção de core isolada passa;
- exceção de core misturada com feature falha.

Ao final do F5:

- scaffold arquitetural: **completo**;
- exceções reais de core: **0**.

---

## 7. Invariantes que ficaram registrados

1. Feature do Atento não entra no core do Letta quando existir boundary adequada.
2. Código de produto Atento vive por padrão em `atento/**`.
3. Mudança em `src/**` exige exceção explícita, isolada e rastreável.
4. RAG permanece removível e não vira segundo orquestrador.
5. Policy terapêutica permanece independente da policy geral.
6. Identidade/memória general e therapeutic permanecem separáveis.
7. Upgrade upstream é evento explícito de migração/revalidação.
8. Quantidade de features não entra no score de qualidade do chassi.

---

## 8. Principais documentos/artefatos já produzidos

Documentação de protocolo e decisão:

- `PROTOCOL_V1.md`
- `PROTOCOL_V1_1_FREEZE.md`
- `EVIDENCE_TEMPLATE.yaml`
- `PARITY.md`
- `PARITY_TEMPLATE.md`
- `M8_CUMULATIVE_EVOLUTION.md`
- `M9_DECISION_GATES.md`
- `M10_FINAL_DECISION.md`
- `M11_EXECUTABLE_SELECTION.md`
- `EXECUTABLE_COMPARISON.md`
- `AGENT_CMD.md`
- `INDEX.md`

Evidência executável:

- `executable_gate/letta-code/RESULT.yaml`
- `executable_gate/letta-code/REPORT.md`
- `executable_gate/librechat/RESULT.yaml`
- `executable_gate/librechat/REPORT.md`

Scaffold/fork:

- `fork_baseline/F0_REPORT.md`
- `fork_baseline/F1_REPORT.md`
- `fork_baseline/F2_REPORT.md`
- `fork_baseline/F3_REPORT.md`
- `fork_baseline/F4_REPORT.md`
- `fork_baseline/F5_REPORT.md`
- `fork_baseline/BRANCH_MODEL.md`
- `fork_baseline/CHANGE_CONTROL.yaml`
- `fork_baseline/fork_seed/`

---

## 9. O que não foi aplicado ao produto

Para evitar confusão:

- o fork seed foi construído e testado em sandbox/fixtures, mas **não aplicado ao código de produto do repositório Atento**;
- esta publicação remota preserva documentação/evidência em branch de pesquisa;
- essa publicação documental não equivale a aplicar o fork seed, migrar blocos do produto ou alterar o runtime do Atento.

Este handoff encerra em registro histórico. Ele deliberadamente não contém instrução sobre o que fazer depois.
