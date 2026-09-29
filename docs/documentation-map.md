# Documentation Map — autoridade e conteúdo dos documentos

Este arquivo define **quem é a fonte de verdade para cada tipo de informação**. Seu objetivo é impedir documentação duplicada e decisões contraditórias.

## Regra de autoridade

Quando a mesma informação aparece em mais de um arquivo, prevalece o documento que possui autoridade canônica nesta tabela.

| Documento | Autoridade canônica | Deve conter | Não deve conter como fonte primária | Atualizar quando |
|---|---|---|---|---|
| `README.md` | entrada/navegação | propósito, maturidade, links e quick orientation | progresso duplicado, arquitetura detalhada, licenças completas | navegação ou posicionamento mudar |
| `AGENTS.md` | regras para agentes/contribuição automatizada | workflow, defensabilidade, gates, regras de progresso | arquitetura detalhada de módulo, decisões ADR específicas | regras de engenharia/governança mudarem |
| `roadmap.md` | escopo + arquitetura macro + Project Points + progresso | blocos A–S, dependências, source map arquitetural, ledger 100 pontos, status global | protocolo detalhado de benchmark, licença legal detalhada | escopo/progresso/dependências/arquitetura macro mudar |
| `docs/adr/*.md` | decisão arquitetural específica | contexto, alternativas, evidência, decisão, consequências | status geral do projeto | decisão estrutural for proposta/aceita/substituída |
| `docs/evaluation/harness.md` | metodologia AtentoEval | suites, schemas, judges, adapters, métricas, release comparison | progresso, escolha fork/greenfield, autorização de dataset | avaliação mudar |
| `docs/evaluation/*qualification*.md` / `*research*.md` | registro de evidência datada | pins, fatos observados, probes, blockers, síntese de pesquisa e gaps não provados | metodologia normativa, decisão ADR, progresso global | nova evidência material ou requalificação |
| `evals/README.md` | operação do harness | comandos, formatos, setup, troubleshooting | metodologia normativa ou thresholds duplicados | CLI/layout do harness mudar |
| `docs/third-party.md` | provenance/termos externos | repo, commit, termos conhecidos, dados, modo de adoção, attribution | decisão arquitetural final, progresso | fonte externa for considerada/atualizada/usada |
| documentação local de módulo | contrato técnico local | interface, invariants, failure modes, exemplos | regras globais duplicadas | módulo mudar |

## Avaliação atual dos Markdown existentes

### AGENTS.md — defensável
Papel correto: política de execução. Deve apontar para fontes canônicas em vez de copiar especificações inteiras. O progress tracking global foi tornado obrigatório.

### roadmap.md — defensável com disciplina de ownership
É intencionalmente amplo. Deve permanecer a fonte de verdade para **o que falta e quanto do projeto inteiro está concluído**. Detalhes que evoluem rapidamente devem apontar para docs especializados.

### ADR-000 — defensável enquanto `Proposed`
Não deve ser tratada como decisão antes do spike. A mudança para `Accepted` exige evidência listada na própria ADR.

### docs/evaluation/harness.md — defensável
Possui responsabilidade clara: metodologia de avaliação. Não deve carregar status geral do projeto.

### docs/evaluation/*qualification*.md / *research*.md — evidência, não decisão
Registros datados podem consolidar inspeções, benchmarks usados como referência, provas Git, execução de probes e bloqueios. Devem declarar pins e limitações. Não substituem o harness, ADR, third-party registry ou roadmap.

### docs/third-party.md — defensável
Registra facts de provenance/termos e o modo de adoção. Fonte sem termos claros pode ser usada como clone externo de pesquisa, mas não deve ser redistribuída silenciosamente dentro do repo.

### evals/README.md — defensável
Deve continuar curto e operacional.

## Documentos que devem existir

### README.md — obrigatório
Entrada do repositório. Deve explicar propósito, maturidade, segurança, navegação e onde está o progresso. Não repetir o ledger.

### SECURITY.md — criar antes de usuários externos/piloto
Deve conter política de reporte de vulnerabilidade, escopo, contato e disclosure. Não confundir com o Safety Engine conversacional.

### CONTRIBUTING.md — criar quando houver colaboração externa
Deve resumir setup, branch/PR workflow e apontar para AGENTS.md. Não duplicar as regras extensas de defensabilidade.

### docs/architecture/*.md — criar quando a implementação existir
Um documento por subsistema somente quando houver código real suficiente para justificar documentação local. Não pré-criar arquitetura fictícia.

### docs/runbooks/*.md — criar antes de staging/produção
Incidentes, rollback, backup/restore e operações.

## Regra anti-documentação-fictícia

Não criar documento detalhando módulo que ainda não existe como se estivesse implementado.

Para componentes futuros, usar o `roadmap.md`.  
Para decisões ainda abertas, usar ADR com status `Proposed`.  
Para implementação real, criar documentação local ligada ao código.
