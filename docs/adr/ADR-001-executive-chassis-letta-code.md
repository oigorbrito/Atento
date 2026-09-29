# ADR-001 — Executive Chassis: Letta Code

## Document contract

Esta ADR propõe a base executiva/chassi do Atento a partir da evidência preservada no benchmark de 2026-09-29. Ela não redefine o AtentoEval, o ledger do roadmap nem as regras de provenance de donors terapêuticos.

- **Status:** Proposed
- **Date:** 2026-09-29
- **Decision owner:** Atento project

## Context

O projeto precisava separar duas perguntas diferentes:

1. quais features/donors terapêuticos usar;
2. qual chassi de longo prazo suporta canais, memória, tools, policy, providers, RAG removível e evolução de fork com baixo core churn.

A avaliação comparou Dify, Rasa, LibreChat, Open WebUI, Letta Code e AnythingLLM sob protocolo congelado, com Flowise rejeitado no intake por upstream arquivado/EOL.

## Evidence

Evidência principal nesta branch:

- `docs/evidence/CHASSIS-LETTA-SELECTION-2026-09-29.md`.

Baseline selecionado:

```text
repository: letta-ai/letta-code
sha: a75111ea610eff9b4a37baba4fbc6ee24bb73c79
benchmark_state: EXECUTABLE_CHASSIS_SELECTED
control: LibreChat-AI/LibreChat
```

A seleção não foi baseada em feature count. Os principais critérios foram change locality, modularidade, substituibilidade, policy isolation, memória, channel boundary, reversibilidade, fault isolation e fork/upstream compatibility.

## Proposed decision

Usar **Letta Code** como chassi executivo do Atento, preservando a seguinte fronteira:

```text
Atento product layer
├── general assistant context
├── therapeutic assistant context
│   └── independent permission/policy overlay
├── Letta agent + memory core
├── Letta channel boundary
│   └── WhatsApp
├── Letta tool / MCP / mod boundary
├── model-provider boundary
└── Atento RAG adapter
    └── removable external retrieval service
```

RAG não deve se tornar um segundo orquestrador.

## Required invariants

- código de produto Atento permanece fora do core Letta quando existir boundary adequada;
- mudanças em core exigem exceção explícita, isolada e rastreável;
- general e therapeutic mantêm identidade, memória e policy separáveis;
- permission/policy terapêutica mantém rechecagem na fase de execução;
- upstream é pinado por SHA/versão;
- upgrades executam contract tests e revalidação de superfícies;
- feature count não é métrica de qualidade do chassi.

## Relationship to ADR-000

ADR-000 continua sendo a autoridade proposta para **modo de adoção de donors** (full donor/fork/selective port/native/hybrid). Esta ADR trata especificamente do **chassi executivo**. Donors terapêuticos continuam podendo ser avaliados e adotados por bloco atrás dos contratos do Atento.

## Consequences

### Positive

- WhatsApp/channel, memória e tool/policy boundaries já existem como conceitos do chassi;
- menor necessidade observada de espalhar código de produto pelo core;
- RAG pode permanecer substituível;
- há evidência executável/CI no SHA congelado para as superfícies críticas.

### Risks

- a API de Mods do Letta prioriza repairability sobre garantia permanente de backwards compatibility;
- upgrades precisam ser eventos explícitos de migração/revalidação;
- o RAG clássico não é uma primitiva nativa equivalente a Dify/Open WebUI e fica sob responsabilidade do Atento.

## Acceptance

Esta ADR pode mudar para `Accepted` somente após revisão do impacto no `roadmap.md`, `docs/third-party.md` e ADR-000, sem apagar a evidência histórica existente.
