# Atento

Atento é o repositório canônico de um produto com três agentes especializados: **NAIA** (assistente pessoal persistente), **Anna** (assistente emocional/terapêutica) e **Apollo** (nutrição/fitness, atualmente adiado).

> **Maturidade atual:** reconciliação de produto + pesquisa/arquitetura + scaffold inicial de avaliação. Nenhum chassis está selecionado para NAIA ou Anna; Apollo está adiado.

## Alinhamento conceitual em reconstrução

O projeto está reconciliando sua definição em três agentes: **NAIA** (assistente pessoal persistente), **Anna** (assistente emocional/terapêutica) e **Apollo** (nutrição/personal, adiado). O alinhamento atual está em [docs/product-concept-reset.md](docs/product-concept-reset.md). Até a reconciliação terminar, não interpretar a decomposição histórica do repositório como definição final.

## Onde começar

- **Regras para agentes/contribuidores:** [AGENTS.md](AGENTS.md)
- **Arquitetura, blocos e progresso global:** [roadmap.md](roadmap.md)
- **Decisão fork vs greenfield:** [docs/adr/ADR-000-fork-vs-greenfield.md](docs/adr/ADR-000-fork-vs-greenfield.md)
- **Composição dos agentes / isolamento (reaberta):** [docs/adr/ADR-001-naya-product-composition.md](docs/adr/ADR-001-naya-product-composition.md)
- **Seleção da base da NAIA (decision reset):** [docs/adr/ADR-002-assistant-base-selection.md](docs/adr/ADR-002-assistant-base-selection.md)
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

Antes de novos spikes orientados por candidato, o projeto deve **reenumerar e reclassificar** os chassis comparáveis da NAIA e da Anna, reaproveitando a evidência já medida. Nenhum vencedor ou ordem de execução está selecionado.

## Aviso de escopo

A **Anna** não deve ser apresentada como substituta de profissional de saúde mental, diagnóstico médico, tratamento ou serviço de emergência. O **Apollo** também não deve assumir escopo médico sem requisitos e validação específicos. Safety conversacional, segurança de aplicação e boundaries entre agentes são requisitos separados.
