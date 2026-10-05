# ADR-APOLLO-001 — Seleção do sistema-base do Apollo

> **DEFERRED / DECISION RESET — 2026-09-29:** Apollo está definido conceitualmente, mas sua pesquisa de chassis não começou. Nenhuma base, shortlist, donor ou arquitetura está selecionada.

## Document contract

O **Apollo** é o agente especializado em **nutrição, treino e acompanhamento físico** do produto Atento.

Esta ADR existe para impedir que decisões da NAIA ou da Anna sejam reutilizadas automaticamente no Apollo e para preservar um ponto de entrada claro quando a pesquisa desse agente começar.

Ela não decide:

- a base da NAIA;
- a base da Anna;
- a topologia de comunicação entre agentes;
- arquitetura clínica/médica;
- qualquer candidato externo neste momento.

- **Status:** `DEFERRED`
- **Decision:** `NOT_SELECTED`
- **Shortlist:** `NOT_SELECTED`
- **Candidate enumeration:** `NOT_STARTED`
- **Date:** 2026-09-29

## Shared runtime direction and deferred functional work

The product owner selected NanoClaw as the common operational runtime reference, including the substrate intended for Apollo if Apollo is reactivated. This does not reactivate Apollo's functional chassis research, select a nutrition/fitness base, or authorize migration work. `APOLLO_STATUS = DEFERRED` remains in force.

## Role

Apollo será responsável pelo domínio de:

- treino;
- atividade física;
- planejamento de rotina de exercícios;
- acompanhamento de metas físicas;
- alimentação/nutrição dentro do escopo que vier a ser definido;
- acompanhamento longitudinal relacionado ao seu próprio domínio.

Ele é um agente separado da NAIA e da Anna.

## Isolation requirement

Por padrão, Apollo não deve:

- ler o histórico privado da Anna;
- acessar memória terapêutica da Anna;
- ler memória pessoal da NAIA sem contrato explícito;
- executar ferramentas pessoais da NAIA por herança;
- assumir funções terapêuticas da Anna;
- usar dados sensíveis de saúde/estado emocional fora do mínimo necessário para seu domínio e da política futura do produto.

O mesmo isolamento vale na direção inversa.

A topologia concreta de handoff continua `TBD`.

## Domain-boundary examples

Exemplos conceituais:

```text
usuário conversa com Apollo
        ↓
pede para comprar um produto ou pesquisar preço
        ↓
Apollo não vira NAIA automaticamente
```

```text
usuário conversa com Apollo
        ↓
traz sofrimento emocional que pertence ao domínio da Anna
        ↓
Apollo não passa a operar como terapeuta
```

O mecanismo futuro de orientação/handoff deve respeitar os boundaries definidos para o produto.

## Candidate-equivalence rule

Quando a pesquisa começar, as fontes devem ser classificadas antes de qualquer comparação:

```text
FITNESS_NUTRITION_BASE_CANDIDATE
MECHANISM_DONOR
MODEL_OR_CHECKPOINT
DATA_SOURCE
BENCHMARK_OR_EVAL_SOURCE
DEVICE_OR_SENSOR_INTEGRATION
UNCLASSIFIED_PENDING_AUDIT
```

Somente candidatos realmente comparáveis entram na decisão de chassis.

Um app de dieta, modelo de recomendação, dataset, wearable integration ou biblioteca de exercícios não deve ser promovido automaticamente a agente-base completo.

## Future decision question

> Entre agentes de fitness/nutrição realmente comparáveis, qual sistema funcionando chega ao Apollo alvo com menor mudança total e maior capacidade útil já provada?

Quando essa etapa começar, comparar:

```text
UPSTREAM
WRAPPED
FORKED
SELECTIVE_PORT
NATIVE
HYBRID
```

com a mesma filosofia usada para NAIA e Anna:

```text
working system + localized repair
vs
rebuilding equivalent capability
```

## Future chassis criteria

A enumeração futura deve considerar pelo menos:

- funcionamento end-to-end;
- planejamento longitudinal;
- memória e progress tracking;
- treino/routine scheduling;
- nutrition/meal planning quando aplicável;
- integração com sensores/wearables quando aplicável;
- adaptação de plano com base em progresso;
- model/provider replaceability;
- modularidade e acoplamento;
- observabilidade e testabilidade;
- segurança do domínio;
- privacy/data ownership;
- pt-BR transfer;
- custo operacional;
- adaptation/fork surface;
- upstream maturity/maintenance;
- capacidade de evolução de curto, médio e longo prazo.

## Evidence state

Auditoria do repositório Atento em 2026-09-29 não encontrou candidatos Apollo previamente registrados sob termos como:

- Apollo / Apolo;
- nutrition;
- personal trainer;
- workout;
- health coach.

Portanto:

```text
EXISTING_APOLLO_MEASUREMENTS = NONE_FOUND
EXISTING_APOLLO_CANDIDATE_SET = NONE_FOUND
```

Isso não significa ausência de projetos externos adequados. Significa apenas que essa pesquisa ainda não está documentada no Atento.

## Execution rule

Apollo permanece adiado.

Não iniciar pesquisa extensa, spike, fork ou benchmark do Apollo enquanto a prioridade atual estiver na reconciliação e seleção das bases da NAIA e da Anna, salvo decisão explícita posterior.

## Decision state

```yaml
agent: APOLLO
role: NUTRITION_FITNESS_ASSISTANT
status: DEFERRED
decision: NOT_SELECTED
shortlist: NOT_SELECTED
winner: NOT_SELECTED
adoption_mode: NOT_SELECTED
candidate_enumeration_complete: false
research_started: false
next_step: WAIT_FOR_EXPLICIT_REACTIVATION
```

## Reactivation criteria

Quando Apollo for reativado:

- [ ] definir escopo funcional exato;
- [ ] definir limites entre wellness, fitness, nutrição e domínio médico;
- [ ] enumerar projetos comparáveis;
- [ ] classificar chassis vs donors/modelos/datasets/integrations;
- [ ] localizar benchmarks e evidência upstream;
- [ ] comparar adaptation cost vs greenfield;
- [ ] definir requisitos de isolamento com NAIA e Anna;
- [ ] só então criar shortlist.

Até lá, não existe candidato preferido.
