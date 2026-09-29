# Atento

Atento é um projeto de engenharia para um sistema conversacional de apoio emocional com arquitetura explícita de estado, memória, decisão executiva, planejamento, grounding, ferramentas, safety e avaliação.

> **Maturidade atual:** pesquisa/arquitetura + scaffold inicial de avaliação. Não tratar o repositório atual como sistema clínico ou produto de produção.

## Onde começar

- **Regras para agentes/contribuidores:** [AGENTS.md](AGENTS.md)
- **Arquitetura, blocos e progresso global:** [roadmap.md](roadmap.md)
- **Decisão fork vs greenfield:** [docs/adr/ADR-000-fork-vs-greenfield.md](docs/adr/ADR-000-fork-vs-greenfield.md)
- **Composição Nayá — Assistente × Terapeuta (proposta):** [docs/adr/ADR-001-naya-product-composition.md](docs/adr/ADR-001-naya-product-composition.md)
- **Seleção da base da Assistente (em avaliação):** [docs/adr/ADR-002-assistant-base-selection.md](docs/adr/ADR-002-assistant-base-selection.md)
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

Antes do bootstrap da base de produção, o projeto deve fechar a **ADR-000 — Fork vs Greenfield** usando o spike e o AtentoEval.

## Aviso de escopo

O Atento não deve ser apresentado como substituto de profissional de saúde mental, diagnóstico médico, tratamento ou serviço de emergência. Safety conversacional e segurança de aplicação são requisitos separados e precisam de validação própria.
