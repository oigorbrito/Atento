# Atento

Atento é o repositório canônico de um produto com três agentes especializados: **NAIA** (assistente pessoal persistente), **Anna** (assistente emocional/terapêutica) e **Apollo** (nutrição/fitness, atualmente adiado).

> **Maturidade atual:** a direção provisória da base da NAIA é NanoClaw (`4c1eabd`), com qualificação técnica pendente. A base da Anna segue não selecionada; Apollo está adiado. A topologia integrada do Atento ainda não está selecionada.

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
- **Composição dos agentes / isolamento (reaberta):** [docs/adr/ADR-001-naya-product-composition.md](docs/adr/ADR-001-naya-product-composition.md)
- **Seleção da base da NAIA (direção NanoClaw provisória; qualificação pendente):** [docs/adr/ADR-002-assistant-base-selection.md](docs/adr/ADR-002-assistant-base-selection.md)
- **Seleção da base da Anna (decision reset):** [docs/adr/ADR-ANNA-001-therapeutic-base-selection.md](docs/adr/ADR-ANNA-001-therapeutic-base-selection.md)
- **Seleção da base do Apollo (deferred):** [docs/adr/ADR-APOLLO-001-fitness-nutrition-base-selection.md](docs/adr/ADR-APOLLO-001-fitness-nutrition-base-selection.md)
- **Evaluation harness:** [docs/evaluation/harness.md](docs/evaluation/harness.md)
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

## Próxima decisão

Antes de novos spikes, o projeto está comparando o **chassi do Atento completo** (NAIA, Anna e a fronteira futura do Apollo), reaproveitando evidência por escopo. A antiga triagem e o Top 5 da NAIA são role-specific; nenhum chassi sistêmico ou Top 5 global está selecionado. Apollo permanece adiado como pesquisa funcional.

## Aviso de escopo

A **Anna** não deve ser apresentada como substituta de profissional de saúde mental, diagnóstico médico, tratamento ou serviço de emergência. O **Apollo** também não deve assumir escopo médico sem requisitos e validação específicos. Safety conversacional, segurança de aplicação e boundaries entre agentes são requisitos separados.
