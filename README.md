# Atento

Atento é o repositório canônico de um produto com três agentes especializados: **NAIA** (assistente pessoal persistente), **Anna** (assistente emocional/terapêutica) e **Apollo** (nutrição/fitness, atualmente adiado).

> **Estado atual (2026-10-02):** NanoClaw é a direção provisória da base geral da NAIA. PsychAgent é a direção escolhida pelo usuário para a base da Anna. MindRoom é candidato para validar como runtime comum dos três, sem vencedor qualificado. Apollo segue adiado. Veja [ADR-SYS-001](docs/adr/ADR-SYS-001-common-chassis-mindroom.md) para estados, evidências e contato mínimo entre agentes.

## Alinhamento conceitual em reconstrução

O projeto está reconciliando sua definição em três agentes: **NAIA** (assistente pessoal persistente), **Anna** (assistente emocional/terapêutica) e **Apollo** (nutrição/personal, adiado). O alinhamento atual está em [docs/product-concept-reset.md](docs/product-concept-reset.md). Até a reconciliação terminar, não interpretar a decomposição histórica do repositório como definição final.

## Onde começar

- **Handoff do reset/reconciliação:** [docs/handoff-2026-09-29-product-reset.md](docs/handoff-2026-09-29-product-reset.md)
- **Handoff do chassi sistêmico:** [docs/handoff-2026-09-30-atento-system-chassis.md](docs/handoff-2026-09-30-atento-system-chassis.md)
- **Re-screen de arquitetura/chassi do Atento completo:** [docs/evaluation/atento-system-architecture-chassis-rescreen-2026-09-30.md](docs/evaluation/atento-system-architecture-chassis-rescreen-2026-09-30.md)
- **Auditoria da reconciliação do remoto:** [docs/reconciliation-2026-09-29.md](docs/reconciliation-2026-09-29.md)
- **Regras para agentes/contribuidores:** [AGENTS.md](AGENTS.md)
- **Arquitetura, blocos e progresso global:** [roadmap.md](roadmap.md)
- **Decisão fork vs greenfield:** [docs/adr/ADR-000-fork-vs-greenfield.md](docs/adr/ADR-000-fork-vs-greenfield.md)
- **Composição dos agentes / isolamento e decisão atual do chassi:** [docs/adr/ADR-001-naya-product-composition.md](docs/adr/ADR-001-naya-product-composition.md)
- **Chassi comum — MindRoom (direção de implementação, não qualificada):** [docs/adr/ADR-SYS-001-common-chassis-mindroom.md](docs/adr/ADR-SYS-001-common-chassis-mindroom.md)
- **Seleção da base da NAIA (decision reset):** [docs/adr/ADR-002-assistant-base-selection.md](docs/adr/ADR-002-assistant-base-selection.md)
- **Seleção da base da Anna (decision reset):** [docs/adr/ADR-ANNA-001-therapeutic-base-selection.md](docs/adr/ADR-ANNA-001-therapeutic-base-selection.md)
- **Seleção da base do Apollo (deferred):** [docs/adr/ADR-APOLLO-001-fitness-nutrition-base-selection.md](docs/adr/ADR-APOLLO-001-fitness-nutrition-base-selection.md)
- **Evaluation harness:** [docs/evaluation/harness.md](docs/evaluation/harness.md)
- **Autoridade dos documentos:** [docs/documentation-map.md](docs/documentation-map.md)
- **Provenance e licenças externas:** [docs/third-party.md](docs/third-party.md)
- **Mapa de autoridade da documentação:** [docs/documentation-map.md](docs/documentation-map.md)
- **AtentoEval operacional:** [evals/README.md](evals/README.md)

## Progresso

O progresso oficial existe **somente** no `roadmap.md` e é medido em **100 Project Points para o projeto inteiro**.

Não duplicamos o número neste README para evitar status divergente.

## Princípio de engenharia

```text
problema
→ fonte/evidência
→ contrato
→ implementação
→ teste
→ benchmark
→ safety
→ release
```

Mudanças que não conseguem percorrer essa cadeia ainda não são consideradas defensáveis.

## Próximo marco

Próximo gate: quando existir adapter executável do Atento, validar a identidade confiável, isolamento entre papéis e restart/retry conforme ADR-SYS-001. Hoje o gate integrado permanece BLOCKED_ADAPTER.

## Aviso de escopo

A **Anna** não deve ser apresentada como substituta de profissional de saúde mental, diagnóstico médico, tratamento ou serviço de emergência. O **Apollo** também não deve assumir escopo médico sem requisitos e validação específicos. Safety conversacional, segurança de aplicação e boundaries entre agentes são requisitos separados.
