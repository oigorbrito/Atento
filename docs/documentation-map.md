# Documentation Map — autoridade e conteúdo dos documentos

Este arquivo define **quem é a fonte de verdade para cada tipo de informação**. Seu objetivo é impedir documentação duplicada e decisões contraditórias.

## Regra de autoridade

Quando a mesma informação aparece em mais de um arquivo, prevalece o documento que possui autoridade canônica nesta tabela.

| Documento | Autoridade canônica | Deve conter | Não deve conter como fonte primária | Atualizar quando |
|---|---|---|---|---|
| `README.md` | entrada/navegação | propósito, maturidade, links e quick orientation | progresso duplicado, arquitetura detalhada, licenças completas | navegação ou posicionamento mudar |
| `AGENTS.md` | regras para agentes/contribuição automatizada | workflow, defensabilidade, gates, regras de progresso | arquitetura detalhada de módulo, decisões ADR específicas | regras de engenharia/governança mudarem |
| `docs/product-concept-reset.md` | identidade e escopo dos produtos | NAIA/Anna/Apollo e seus papéis | seleção de bases/chassi e evidência | papéis mudarem |
| `docs/handoff-*.md` | snapshot de continuidade | contexto suficiente para retomar uma sessão e apontar para fontes canônicas | substituir ADR/product concept/roadmap como autoridade | handoff material for atualizado |
| `docs/reconciliation-*.md` | auditoria de reconciliação | inventário revisado, mudanças de autoridade e resultado da varredura | substituir a fonte canônica de produto/decisão | nova reconciliação integral ocorrer |
| `roadmap.md` | ledger técnico + arquitetura histórica/em reconciliação + Project Points + progresso | blocos A–S, dependências, source map arquitetural, ledger 100 pontos, status global | protocolo detalhado de benchmark, licença legal detalhada, identidade de produto durante DECISION_RESET | escopo/progresso/dependências/arquitetura macro mudar |
| `docs/adr/ADR-SYS-001-common-chassis-mindroom.md` | decisão atual de arquitetura geral/composição | estado de cada base, runtime comum, limites entre agentes, evidência e gates | progresso e suites detalhadas | evidência/decisão de chassi mudar |
| `docs/adr/ADR-002-assistant-base-selection.md`, `ADR-ANNA-001-*`, `ADR-APOLLO-001-*` | decisão de base funcional por agente | direção/status e decisão específica de NAIA, Anna ou Apollo | decisão do runtime comum | base daquele agente mudar |
| `docs/adr/*.md` restantes | decisão arquitetural específica | contexto, alternativas, evidência, decisão, consequências | status geral do projeto | decisão estrutural for proposta/aceita/substituída |
| `docs/evaluation/harness.md` | metodologia AtentoEval | suites, schemas, judges, adapters, métricas, release comparison | progresso, escolha fork/greenfield, autorização de dataset | avaliação mudar |
| `docs/evaluation/*qualification*.md` / `*research*.md` | registro de evidência datada | pins, fatos observados, probes, blockers, síntese de pesquisa e gaps não provados | metodologia normativa, decisão ADR, progresso global | nova evidência material ou requalificação |
| `evals/README.md` | operação do harness | comandos, formatos, setup, troubleshooting | metodologia normativa ou thresholds duplicados | CLI/layout do harness mudar |
| `docs/third-party.md` | provenance/termos externos | repo, commit, termos conhecidos, dados, modo de adoção, attribution | decisão arquitetural final, progresso | fonte externa for considerada/atualizada/usada |
| documentação local de módulo | contrato técnico local | interface, invariants, failure modes, exemplos | regras globais duplicadas | módulo mudar |

## Avaliação atual dos Markdown existentes

### AGENTS.md — defensável
Papel correto: política de execução. Deve apontar para fontes canônicas em vez de copiar especificações inteiras. O progress tracking global foi tornado obrigatório.

### docs/product-concept-reset.md — autoridade provisória durante DECISION_RESET
Este documento define identidade e escopo dos agentes. As decisões correntes de base e chassi estão nas ADRs por papel e na ADR-SYS-001.

### roadmap.md — ledger técnico durante reconciliação
Permanece a fonte de verdade para Project Points e evidência de progresso, mas sua decomposição arquitetural histórica não substitui o product concept reset enquanto `DECISION_RESET` estiver ativo.

### ADR-000 / ADR-001 / ADR-002 — escopo
Preservam evidência histórica e decisões apenas dentro do escopo de cada arquivo. Para status corrente, ADR-SYS-001 governa o runtime comum; ADR-002 governa base NAIA. Textos `DECISION_RESET` datados não anulam decisões posteriores explícitas.

### ADR-ANNA-001 — seleção da base da Anna
Fonte de verdade para evidência e qualificação da base funcional da Anna. Direção escolhida pelo usuário: PsychAgent; qualificação pendente. PsyChat permanece donor de mecanismos/RAG.

### ADR-APOLLO-001 — seleção da base do Apollo
Fonte de verdade para o estado da decisão de chassis do Apollo. Enquanto `DEFERRED`, não existe shortlist, candidato preferido nem pesquisa de base iniciada.

### docs/evaluation/harness.md — defensável
Possui responsabilidade clara: metodologia de avaliação. Não deve carregar status geral do projeto.

### docs/evaluation/candidate-reenumeration-2026-09-29.md — universo comparável, não shortlist
Registra a reconstrução pós-reset dos universos de candidatos da NAIA e da Anna, com pins, classificação inicial, provenance e gaps para auditoria. Não possui autoridade para declarar shortlist, vencedor, prioridade de execução ou adoção.

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
Para decisões ainda abertas, usar ADR com status `Proposed`, `DECISION_RESET` ou `DEFERRED`, conforme o caso.  
Para implementação real, criar documentação local ligada ao código.


## Arquivos históricos e instruções CMD

O pacote `docs/research/chassis-selection-v1/archive/` preserva o ZIP histórico (integridade descrita no README do arquivo). `FILE_LIST.txt` inclui `AGENT_CMD.md`, mas não existe `AGENT_CMD.md` ativo na raiz do branch reconciliado. O material reconstruído/arquivado é referência histórica, não instrução atual nem autoridade de seleção. Para decisões atuais prevalecem ADR-SYS-001, as ADRs por agente, este mapa, o harness e o roadmap nos respectivos escopos.
