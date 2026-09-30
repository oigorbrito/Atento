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

## 1.1 Contrato funcional dos agentes

A separação do produto deve distinguir **autoridade de domínio** de **autoridade operacional**.

A NAIA é a experiência principal e pode funcionar como porta de entrada do produto, mas isso **não** a torna superusuária dos demais agentes. Anna e Apollo mantêm autoridade própria sobre seus domínios e memória própria.

| Agente | Papel principal | Autoridade de domínio | Autoridade operacional padrão |
|---|---|---|---|
| **NAIA** | assistente pessoal executiva / secretária persistente | organização da vida pessoal, tarefas, comunicação, pesquisa e coordenação operacional | calendário, e-mail, mensagens, pesquisa geral, compras, browser/computer use, apps conectados, rotinas, automações e outros efeitos externos pessoais autorizados |
| **Anna** | assistente emocional / terapêutica | conversa terapêutica, continuidade longitudinal, estratégia/intervenções, memória terapêutica, safety e acompanhamento emocional | apenas ferramentas necessárias ao próprio domínio; ações pessoais externas gerais não são herdadas da NAIA |
| **Apollo** | assistente de nutrição / fitness / personal trainer | treino, nutrição dentro do escopo definido, metas físicas, progresso, adaptação de plano e acompanhamento longitudinal do próprio domínio | ferramentas e integrações do domínio, como métricas/sensores quando autorizados; ações pessoais externas gerais não são herdadas da NAIA |

### NAIA — responsabilidade executiva

A NAIA é responsável por transformar intenção do usuário em execução operacional pessoal.

Inclui, quando autorizado:

- agenda, calendário, lembretes, tarefas e rotinas;
- e-mail, mensagens e comunicação;
- pesquisa geral, comparação de opções e apoio a compras;
- browser/computer use e aplicativos conectados;
- automações e trabalho persistente/background;
- coordenação logística e efeitos externos pessoais;
- memória pessoal geral necessária para continuidade operacional.

A NAIA **não** assume por padrão:

- formulação terapêutica;
- interpretação clínica/emocional longitudinal da Anna;
- acesso à memória privada da Anna;
- planejamento especializado de treino/nutrição do Apollo;
- acesso à memória privada do Apollo.

### Anna — responsabilidade terapêutica/emocional

A Anna é a autoridade do domínio emocional/terapêutico.

Inclui:

- conversa de apoio emocional/terapêutico;
- memória longitudinal do próprio domínio;
- perfil e continuidade entre sessões;
- planejamento/estratégia de acompanhamento;
- seleção de intervenções/skills do domínio;
- incerteza, clarificação e resistência/evasão;
- safety, limites de papel e regras de escalonamento;
- acompanhamento multi-sessão.

A Anna não deve virar assistente pessoal para executar pesquisa de preço, compras, e-mail, calendário, browser ou outras ações gerais. Quando uma necessidade terapêutica gerar uma tarefa operacional, ela pode produzir um **handoff mínimo e explícito** para a NAIA.

Exemplo:

```text
Anna identifica que o usuário quer ajuda para marcar uma consulta
        ↓
Anna decide apenas o que pertence ao contexto terapêutico
        ↓
handoff explícito com o mínimo necessário
        ↓
NAIA executa agenda/pesquisa/contato sob sua própria policy
```

### Apollo — responsabilidade fitness/nutrição

O Apollo é a autoridade do domínio de treino, nutrição e acompanhamento físico.

Quando reativado, inclui:

- definição e acompanhamento de metas físicas;
- planejamento de treino e rotina de exercícios;
- nutrição/meal planning dentro do escopo de produto aprovado;
- progresso, aderência e adaptação longitudinal;
- uso de métricas, sensores e wearables quando autorizado;
- memória própria necessária para evolução do plano.

Apollo não assume:

- terapia ou acompanhamento emocional da Anna;
- pesquisa/compras/comunicação geral da NAIA;
- autoridade médica além do que um contrato futuro de produto permitir.

Quando o plano do Apollo exigir logística geral — por exemplo colocar treinos no calendário, criar lembretes, pesquisar preço de equipamento ou organizar uma compra — a execução deve ser entregue explicitamente à NAIA.

### Infraestrutura compartilhada não significa memória compartilhada

Algumas capacidades podem ser comuns em nível de plataforma:

- identidade/autenticação;
- consentimento;
- auditoria e tracing;
- contratos de handoff;
- observabilidade e avaliação;
- abstrações de model/provider;
- infraestrutura técnica comum quando isso não quebra isolamento.

Isso não autoriza um agente a consultar memória, chat, ferramentas ou credenciais privadas de outro.

A regra é:

```text
SHARED_PLATFORM
!=
SHARED_AGENT_AUTHORITY

NAIA_IS_PRIMARY_EXPERIENCE
!=
NAIA_CAN_READ_EVERYTHING
```

### Regra de handoff

O agente atual deve tentar resolver apenas o que pertence ao próprio domínio.

Quando a intenção exigir outro domínio:

1. identificar a fronteira;
2. explicar ou sinalizar a transição quando necessário;
3. solicitar/usar consentimento conforme a sensibilidade;
4. transmitir somente o mínimo necessário;
5. o agente de destino toma sua própria decisão sob sua própria policy;
6. registrar o handoff para auditoria.

Nenhum handoff transfere automaticamente histórico completo, memória privada ou tool authority.

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
