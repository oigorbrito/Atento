# Atento — alinhamento conceitual do produto

> Status: alinhamento provisório, 2026-09-29.
>
> Este documento registra o norte conceitual enquanto o Atento é reconciliado com a intenção original do usuário. Ele não apaga evidência técnica existente, não seleciona uma implementação-base e não substitui ainda roadmap/ADRs.

## 1. Repositório e produto

O repositório canônico deste trabalho é:

```text
oigorbrito/Atento
```

Dentro dele, o produto/ecossistema é organizado em três agentes com responsabilidades diferentes.

A **NAIA** — sigla para **Nova Assistente Inteligente Artificial** — é a assistente pessoal principal e a experiência central do produto.

A implementação histórica da NAIA deve ser tratada como **referência de ideia e de produto**, não como referência obrigatória de código, arquitetura ou chassis.

## 2. Origem da NAIA

A NAIA nasceu como uma assistente pessoal inspirada em experiências como Zapia.

Depois surgiu a categoria de **agente/assistente persistente**. O Grok Bot foi citado como referência conceitual dessa categoria.

Durante a pesquisa apareceu o **OpenMausBot** como uma implementação pública conceitualmente próxima e com uma superfície de produto mais madura que a implementação inicial da NAIA.

Isso levou à inversão estratégica:

```text
não:
OpenMausBot dentro da implementação histórica da NAIA

avaliar:
chassis persistente maduro
        +
diferenciais/ideias da NAIA
        +
features úteis de outros donors
```

O objetivo é evitar reconstruir do zero capacidades que uma base madura já tenha resolvido melhor.

## 3. Parte 1 — NAIA: assistente pessoal persistente

A NAIA deve cobrir, na medida técnica e financeiramente possível, o conjunto relevante de capacidades das referências de produto citadas pelo usuário — incluindo Grok Bot, Zapia e projetos comparáveis descobertos durante a pesquisa.

"100% das funcionalidades" deve ser interpretado como **meta de cobertura funcional/paridade de capacidade a ser inventariada e medida**, não como afirmação de que essa paridade já existe.

O OpenMausBot é o **primeiro anchor candidate conhecido** para essa parte.

Ele não está automaticamente selecionado.

A comparação de chassis da NAIA deve considerar pelo menos:

- persistência real de estado, contexto, tarefas e rotinas;
- continuidade após restart/interrupção;
- automações e execução em background;
- mensagens e canais;
- uso de computador, browser e aplicativos;
- integrações e ferramentas;
- memória pessoal;
- troca/roteamento de modelos e providers;
- arquitetura e ownership boundaries;
- modularidade e acoplamento;
- extensibilidade e facilidade de incorporar novas features;
- superfície de adaptação/fork;
- observabilidade, testes e evidência de execução;
- segurança e autoridade sobre efeitos externos;
- custo operacional;
- capacidade de evolução no curto, médio e longo prazo.

A próxima pesquisa da NAIA não deve assumir que a lista atual de candidatos está completa.

Projetos já presentes no repositório, incluindo OpenClaw, só permanecem como finalistas se sua inclusão puder ser justificada pelo mesmo protocolo aplicado aos demais.

## 4. Parte 2 — Anna: assistente emocional/terapêutica

A **Anna** é um segundo agente distinto da NAIA.

Seu domínio é apoio emocional/terapêutico.

A Anna não deve ser tratada como "modo terapêutico" da NAIA nem como uma persona compartilhando a mesma autoridade.

Sua implementação-base ainda não foi selecionada.

A estratégia é enumerar projetos terapêuticos maduros, privilegiando candidatos com:

- execução funcional observável;
- benchmarks ou avaliações publicadas;
- arquitetura suficientemente completa para operar como agente;
- memória/continuidade quando relevante;
- safety e role-boundary verificáveis;
- possibilidade de adaptação com change-surface pequeno;
- evidência de evolução/manutenção;
- capacidade de transferência para pt-BR e para o produto Atento.

A pesquisa deve separar:

```text
THERAPEUTIC_BASE_CANDIDATE
vs
MECHANISM_DONOR
vs
MODEL/CHECKPOINT
vs
BENCHMARK/EVALUATION_SOURCE
```

Não promover automaticamente um projeto de RAG, modelo ou mecanismo isolado a chassis terapêutico completo.

## 5. Parte 3 — Apollo: nutrição e personal trainer

O **Apollo** será um terceiro agente especializado em nutrição, treino e acompanhamento físico.

Sua decisão de base possui ADR própria:

- `docs/adr/ADR-APOLLO-001-fitness-nutrition-base-selection.md`

Ele permanece **em espera** neste momento.

A auditoria do remoto em 2026-09-29 não encontrou candidatos, benchmarks ou medições específicos do Apollo já registrados. Portanto:

```text
APOLLO_STATUS = DEFERRED
APOLLO_SHORTLIST = NOT_SELECTED
APOLLO_WINNER = NOT_SELECTED
APOLLO_RESEARCH = NOT_STARTED
```

Nenhuma seleção de chassis, donor ou arquitetura específica para Apollo deve bloquear a qualificação da NAIA ou da Anna.

## 6. Isolamento entre agentes

NAIA, Anna e Apollo são **bounded contexts distintos**.

Por padrão:

- um agente não lê o histórico de chat do outro;
- um agente não consulta a memória privada do outro;
- um agente não herda automaticamente as ferramentas do outro;
- um agente não executa ações pertencentes ao domínio do outro;
- um agente não usa outro agente como fallback silencioso;
- qualquer handoff deve ser explícito, mínimo e auditável;
- dados sensíveis só atravessam a fronteira quando o contrato permitir e, quando necessário, com consentimento do usuário.

Exemplo de boundary:

```text
usuário conversa com Anna
        ↓
pede preço de iPhone
        ↓
Anna NÃO consulta preço
Anna NÃO vira assistente pessoal
Anna permanece no domínio emocional/terapêutico
e pode, quando apropriado, orientar o usuário a levar
a demanda operacional para a NAIA
```

O mesmo princípio vale nas outras direções.

## 7. Estratégia de adoção: "carro andando" antes de greenfield

O projeto não possui preferência ideológica por greenfield.

A hipótese a testar é que, muitas vezes, é mais eficiente partir de um sistema funcional e corrigir seus defeitos do que reconstruir todas as capacidades sobre um chassis teoricamente mais elegante.

Analogia de engenharia:

```text
carro funcional com amortecedor defeituoso
pode exigir menos trabalho total
que desmontar o carro inteiro
para migrar tudo para outro chassis
```

Isso não significa aceitar dívida arquitetural sem medição.

A comparação deve medir empiricamente:

- quantidade de capacidade funcional já preservada;
- defeitos reais que precisam ser corrigidos;
- donor files/linhas realmente modificados;
- número e profundidade dos boundaries que precisam ser introduzidos;
- custo para trocar provider/executor/storage;
- regressões criadas pela adaptação;
- esforço de manutenção/sync com upstream;
- custo estimado de reproduzir as mesmas capacidades em greenfield.

Portanto:

```text
CLEANER_ARCHITECTURE
!=
LOWER_TOTAL_MIGRATION_COST

KNOWN_LOCAL_DEFECT
!=
BAD_BASE_AUTOMATICALLY
```

O alvo é encontrar o **menor conjunto de mudanças necessário para transformar uma base já funcional no agente alvo**.

Variantes válidas para comparação incluem:

```text
UPSTREAM
WRAPPED
FORKED
SELECTIVE_PORT
NATIVE
MODEL_ADAPTER
HYBRID
```

## 8. Protocolo de pesquisa e evidência

O processo correto para cada agente é:

```text
definir a categoria
→ enumerar projetos maduros comparáveis
→ localizar benchmarks/evidência existente
→ auditar arquitetura e implementação
→ executar somente o que a evidência externa não prova
→ comparar sob contratos equivalentes
→ medir change-surface real
→ selecionar ou rejeitar o chassis
```

A evidência upstream deve ser reaproveitada quando realmente transferível.

Não repetir benchmarks ou testes apenas para produzir um segundo número sobre o mesmo invariante.

Testes locais devem priorizar:

- deltas introduzidos pelo Atento;
- transferências de idioma/domínio;
- boundaries de autoridade;
- integração real;
- gaps não provados;
- regressões causadas pela adaptação.

## 9. Licença durante descoberta

Licença **não é critério eliminatório da pesquisa técnica inicial**.

Um projeto pode ser estudado e comparado mesmo que seus termos inviabilizem posteriormente determinado modo de distribuição ou incorporação.

Ainda assim, provenance e termos legais continuam obrigatórios para qualquer adoção concreta.

Portanto:

```text
TECHNICAL_CANDIDATE
!=
LEGAL_ADOPTION_CLEARED
```

## 10. Reconciliação provisória da trilha terapêutica existente

A decisão de base da Anna possui agora uma ADR própria:

- `docs/adr/ADR-ANNA-001-therapeutic-base-selection.md`

O remoto atual contém vários projetos relacionados à Anna, mas **nenhum deles pertence à shortlist neste momento**.

Até nova auditoria homogênea:

- **PsychAgent** — `UNCLASSIFIED_PENDING_AUDIT`; evidência terapêutica já medida permanece válida.
- **TherapyMind** (`zx070326-hash/TherapyMind`) — `UNCLASSIFIED_PENDING_AUDIT`; evidência já coletada permanece válida.
- **PsyChat** — `UNCLASSIFIED_PENDING_AUDIT`; precisa ser classificado como chassis completo ou donor de componentes com base em auditoria, não no label histórico.
- **TheraMind** (`Emo-gml/TheraMind`) — `UNCLASSIFIED_PENDING_AUDIT`; a interpretação histórica como donor de mecanismo é preservada apenas como evidência anterior.

Nenhum label histórico como `FULL_DONOR_CANDIDATE`, `adoption HOLD`, “preferido” ou “não preferido” possui autoridade de seleção enquanto `DECISION_RESET` estiver ativo.

### Modelos/checkpoints, não chassis por padrão

- SoulChat2.0 / PsyDT;
- EmoLLM;
- MindChat.

### Benchmarks/referências de avaliação e mecanismos auxiliares

- PsychEval;
- MentalHealthBench;
- CounselBench;
- PATIENT-Ψ;
- MHSafeEval;
- ENPMR-Bench;
- ESConv;
- AgentMental;
- User-Aware Active Knowledge Acquisition.

Essa classificação é **provisória** e deve ser confirmada durante a reconciliação do remoto. Nenhum vencedor foi selecionado.

## 11. Relação com a documentação existente

Este registro não apaga ADRs, avaliações ou pesquisas anteriores.

Até a reconciliação terminar:

- documentação anterior é evidência/histórico, não necessariamente definição final;
- decomposições antigas não devem ser mantidas apenas por inércia;
- OpenClaw/OpenMausBot/outros candidatos da NAIA precisam de origem e critérios comparáveis;
- candidatos terapêuticos precisam ser separados de donors, modelos e benchmarks;
- nenhuma base está selecionada para NAIA ou Anna;
- Apollo permanece adiado.

```text
REPOSITORY = ATENTO

AGENT_1 = NAIA
ROLE_1 = PERSISTENT_PERSONAL_ASSISTANT
OPENMAUSBOT = INITIAL_ANCHOR_CANDIDATE
NAIA_BASE_WINNER = NOT_SELECTED

AGENT_2 = ANNA
ROLE_2 = EMOTIONAL_THERAPEUTIC_ASSISTANT
ANNA_BASE_WINNER = NOT_SELECTED

AGENT_3 = APOLLO
ROLE_3 = NUTRITION_FITNESS_ASSISTANT
APOLLO_STATUS = DEFERRED

CROSS_AGENT_DEFAULT = ISOLATED
```
