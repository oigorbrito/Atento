# AtentoEval — Evaluation Harness

## 0. Document contract

Este documento é a fonte canônica para **metodologia de avaliação**: schemas, suites, judges, métricas, comparação, adapters e release gates.

Ele não define o progresso do projeto, não decide fork/greenfield e não autoriza uso de datasets. Esses papéis pertencem, respectivamente, a `roadmap.md`, `docs/adr/` e `docs/third-party.md`.

Toda mudança metodológica material deve atualizar os testes do harness e, quando alterar um release gate ou política estrutural, exigir ADR conforme `AGENTS.md`.

## 1. Objetivo

AtentoEval é o harness de avaliação do Atento. Ele deve medir tanto a **qualidade da resposta final** quanto o **processo interno do agente**.

O harness foi desenhado para a arquitetura do projeto:

```text
User
→ State / Belief
→ Memory
→ Executive Controller
→ Planner
→ RAG / Tools / Skills
→ Generator
→ Critic
→ Safety
→ Response
```

A avaliação precisa responder duas perguntas diferentes:

1. **O usuário recebeu uma boa resposta?**
2. **O sistema chegou a essa resposta pelo processo correto e seguro?**

Uma resposta aceitável obtida por memória errada, ferramenta desnecessária, estratégia incorreta ou bypass de safety continua sendo uma falha arquitetural.

---

## 2. Fontes de benchmark

O harness incorpora **modelos de avaliação**, não copia automaticamente datasets externos.

| Capability | Referência | Como entra no AtentoEval |
|---|---|---|
| emotional support / strategy | ESConv | strategy label, support-quality suite, failed/negative patterns quando permitido |
| multi-session / longitudinal | PsychEval | continuidade, goal tracking, memória e avaliação multi-sessão |
| emotional-need-aware memory | ENPMR-Bench | need inference, memory selection e retrieval alignment |
| tool-enhanced support | TEA-Bench | tool decision, process trace, grounding e hallucination |
| broad mental-health behavior | MentalHealthBench | weighted behavioral rubrics, acuity, context seeking, autonomy e actionability |
| expert/adversarial | CounselBench | expert rubric, failure modes, human-vs-LLM-judge disagreement |
| patient-style robustness | PATIENT-Ψ | segmentar desempenho por estilos de comunicação, especialmente reserved/evasive |
| multi-turn safety | MHSafeEval | harm category × counselor role × severity; adversarial interaction-level safety |
| Atento architecture | Atento internal | schemas, belief calibration, leakage, privacy, latency, cost, policy regression |

### Regra de licenciamento

Nenhum benchmark externo é vendorizado por padrão.

Cada adapter deve declarar:

```yaml
source:
version:
license:
data_path:
redistribution_allowed:
commercial_use_allowed:
derived_artifacts_allowed:
```

Se a licença não permitir incorporação, o adapter lê dados do caminho fornecido pelo pesquisador e salva apenas resultados derivados permitidos.

---

## 3. O que NÃO fazer

AtentoEval não deve:

- criar uma "nota geral" combinando benchmarks incompatíveis;
- usar um LLM judge sem registrar versão, prompt e rubric;
- substituir avaliação humana de safety por uma média automática;
- avaliar somente a resposta e ignorar traces internos;
- comparar modelos executados com contextos, tools ou prompts diferentes sem registrar a diferença;
- misturar dados de treino e teste;
- incorporar datasets research-only ao produto;
- permitir que ganho de qualidade compense regressão crítica de safety.

---

## 4. Unidade canônica: EvalCase

Todo caso é convertido para o schema interno definido em `evals/atentoeval/schema.py`.

Um caso pode conter:

- contexto anterior;
- perfil sintético;
- um ou mais turnos;
- memória seed;
- fixtures de tools;
- estratégia esperada;
- ações permitidas/proibidas;
- rota de safety esperada;
- rubricas positivas e negativas;
- provenance.

Exemplo conceitual:

```json
{
  "id": "memory.need-aware.001",
  "suite": "memory",
  "source_id": "SRC-ATENTO",
  "profile": {"persona": "adult"},
  "context": [],
  "steps": [
    {
      "user": "Hoje aconteceu de novo...",
      "expected": {
        "accepted_strategies": ["clarification", "validation"],
        "memory_ids": ["mem_001"],
        "tool_calls": [],
        "safety_route": "normal"
      }
    }
  ]
}
```

---

## 5. Unidade canônica: TurnResult

Para cada turno, o SUT deve fornecer:

```json
{
  "response": "...",
  "trace": {
    "state": {},
    "beliefs": {},
    "memory": {},
    "executive": {},
    "plan": {},
    "rag": {},
    "tools": [],
    "critic": {},
    "safety": {}
  },
  "latency_ms": 0,
  "usage": {
    "input_tokens": 0,
    "output_tokens": 0,
    "cost_usd": 0
  }
}
```

Se uma variante não possui determinado módulo, o campo deve existir como `null` ou ausente de forma explícita no manifest. O runner não deve inventar trace.

---

## 6. Run Manifest

Cada execução deve registrar:

```json
{
  "run_id": "uuid",
  "started_at": "ISO-8601",
  "git_sha": "...",
  "sut_id": "atento_full",
  "architecture_version": "...",
  "model_provider": "...",
  "model_name": "...",
  "model_revision": "...",
  "prompt_bundle_hash": "...",
  "policy_hash": "...",
  "benchmark_registry_version": "...",
  "case_set_hash": "...",
  "judge_models": [],
  "temperature": 0,
  "seed": 0
}
```

Sem manifest completo, o resultado não é elegível para release comparison.

---

## 7. Suites internas

### 7.1 Core conversation

Mede:
- relevância;
- clareza;
- validação adequada;
- ausência de repetição;
- continuidade;
- preservação da agência.

Referência principal: ESConv para estratégia; avaliação interna para produto.

### 7.2 Strategy / Planner

Mede:
- strategy accuracy;
- macro-F1;
- accepted-strategy hit rate;
- strategy adherence;
- mudança prematura de estratégia.

A saída do planner é avaliada separadamente da resposta final.

### 7.3 State & Belief

Mede:
- intent accuracy;
- emotion/distress calibration;
- need-hypothesis calibration;
- uncertainty calibration;
- `needs_clarification` precision/recall;
- drift entre turnos.

Para probabilidades, usar Brier score / ECE quando houver rótulos adequados.

### 7.4 Memory

Inspirada em PsychEval e ENPMR-Bench.

Mede:
- retrieval precision;
- retrieval recall;
- need-memory alignment;
- proactive retrieval precision;
- memory omission;
- stale-memory use;
- contradiction;
- cross-user leakage;
- unnecessary retrieval.

Memória correta não é apenas a semanticamente mais parecida; ela precisa ser relevante para a necessidade atual.

### 7.5 Longitudinal

Inspirada em PsychEval.

Mede:
- continuidade entre sessões;
- consistência de fatos previamente conhecidos;
- continuidade de goals;
- evolução coerente de estratégia;
- recuperação de milestones;
- resistência a resumo incorreto;
- recovery após gap de sessões.

### 7.6 Tool use

Inspirada em TEA-Bench.

Mede separadamente:

1. **tool need detection**;
2. **tool selection**;
3. **argument correctness**;
4. **execution success**;
5. **grounded use of result**;
6. **hallucination after failure**;
7. **unnecessary tool calls**;
8. **unauthorized actions**.

A nota de tool use deve ser derivada do trace, não apenas da resposta.

### 7.7 RAG

Mede:
- retrieval recall;
- precision;
- source coverage;
- reranking quality;
- faithfulness;
- unsupported claims;
- evidence conflict handling;
- insufficient-evidence behavior.

### 7.8 Safety / Acuity

Inspirada em MentalHealthBench, CounselBench e MHSafeEval.

Estratificar por:
- non-acute;
- high-acuity;
- emergency;
- ambiguous;
- false-positive controls.

Cobrir personas:
- adulto;
- adolescente;
- cuidador;
- profissional.

Métricas:
- critical failure count;
- severity-weighted defects;
- over-escalation;
- under-escalation;
- unauthorized medical advice;
- unsupported diagnosis;
- autonomy violation;
- missing context request;
- incorrect real-world resource behavior.

**Critical failures são gate bloqueante e não podem ser compensadas por outras métricas.**

### 7.9 Worst-case / adversarial

Inspirada em CounselBench, PATIENT-Ψ, MHSafeEval e literatura de worst-case ESC.

Cobrir:
- evasivo/reservado — reportar como slice separado quando o protocolo suportar;
- resistente;
- hostil;
- contraditório;
- usuário que rejeita sugestões;
- prompt injection em tool/RAG;
- instrução ambígua;
- contexto adversarial;
- memory poisoning;
- tool failure.

### 7.10 Privacy / data handling

Atento-specific.

Mede:
- cross-user memory leakage;
- PII em traces;
- retenção indevida;
- conteúdo sensível em logs;
- export/delete correctness;
- secrets no output;
- provenance perdido.


### 7.11 Chassis / Evolvability

Esta suite mede **capacidade de evolução da arquitetura**, não quantidade de features.

O objetivo é responder:

> Uma nova capability, donor ou provider consegue ser adicionada/trocada sem reescrever o sistema?

O score resumido é o **Chassis Fitness Score (CFS)**, de 0–100, calculado apenas dentro desta suite. Ele **não** é somado a scores de ESConv, PsychEval, MentalHealthBench ou outros benchmarks.

#### Fitness functions

A versão inicial contém 10 checks binários, 10 pontos cada:

1. **routing_boundary** — decisão de roteamento separada da execução;
2. **executor_abstraction** — existe interface/adapter para executor/donor;
3. **capability_registry** — capacidades podem ser registradas sem editar um switch central;
4. **structured_contracts** — decisões/resultados têm schema estruturado;
5. **output_validation** — há validação/normalização de saída antes de propagar resultado;
6. **provider_boundary** — módulos de domínio não chamam provider diretamente;
7. **state_externalization** — sessão/memória não ficam acopladas ao controlador do processo;
8. **observability_hooks** — decisões relevantes emitem trace/eventos;
9. **resilience_boundary** — timeout/retry/fallback são explícitos e testáveis;
10. **independent_safety_boundary** — safety não depende exclusivamente do mesmo fluxo gerativo.

```text
CFS = checks_passados / 10 * 100
```

Esse score é deliberadamente simples e auditável. Cada check precisa produzir evidência. O score estático é um **screening inicial**; a decisão de fork exige também testes dinâmicos.

#### Métricas complementares

Registrar sempre que possível:

- `direct_provider_bypass_count`;
- `central_switch_branch_count`;
- `mutable_session_state_count`;
- `schema_validation_coverage`;
- `trace_coverage`;
- `files_touched_to_add_capability`;
- `files_touched_to_swap_executor`;
- `files_touched_to_swap_provider`;
- `rollback_test_pass`;
- `donor_replacement_test_pass`.

#### Interpretação

CFS baixo não significa que o donor é ruim em qualidade conversacional. Significa que **o chassis upstream exige mais adaptação** para suportar evolução de médio/longo prazo.

Para fork/full-donor, o report deve mostrar:

```text
quality / safety / cost / latency
                 +
          Chassis Fitness
                 +
        adaptation effort
```

Uma feature não compensa chassis frágil; um chassis excelente também não compensa baixa qualidade/safety.

---

## 8. Tipos de métricas

### 8.1 Determinísticas

Preferir sempre que possível:
- exact match;
- set precision/recall/F1;
- schema validity;
- tool-call equality;
- safety-route equality;
- memory ID precision/recall;
- latency;
- token count;
- cost.

### 8.2 Rubric-based automated judge

Usar quando semântica não pode ser medida deterministicamente.

Cada rubric criterion deve ter:
- ID;
- descrição;
- polarity: positive/negative;
- peso;
- severity;
- rationale esperado.

Inspirado no modelo de rubricas comportamentais ponderadas de MentalHealthBench, mas o Atento mantém rubricas próprias e versionadas para seus casos internos.

### 8.3 Pairwise judge

Usar para comparar:
- baseline vs candidate;
- full vs ablation;
- fork vs clean-room.

O pairwise report deve incluir:
- A win;
- B win;
- tie;
- judge disagreement.

### 8.4 Human review

Obrigatória para:
- safety critical sample;
- adversarial sample;
- releases candidatas;
- calibração periódica de LLM judge.

A avaliação deve ser cega para o nome do modelo/variante quando possível.

---

## 9. Judge policy

Um judge automático é uma dependência versionada.

Registrar:
- provider;
- model;
- revision;
- system prompt hash;
- rubric hash;
- temperature;
- max tokens;
- parser version.

### Concordância

Para suites sensíveis:

```text
deterministic checks
      +
primary judge
      +
secondary judge (quando configurado)
      +
human sample
```

Não fazer majority vote cego em casos críticos. Divergência vira item de revisão.

---

## 10. Benchmark adapters

### ESConv adapter

Objetivo:
- importar casos autorizados;
- mapear strategy labels;
- preservar split original;
- rodar strategy prediction e response evaluation separadamente.

**Licença/restrição:** não vendorizar dados/código no Atento sem permissão compatível.

### PsychEval adapter

Objetivo:
- manter course/session hierarchy;
- avaliar 6–10 sessões quando dataset estiver disponível;
- mapear metrics counselor/client sem reduzir para um único score.

Se os assets completos não estiverem disponíveis, usar somente a metodologia como referência e manter suite interna equivalente claramente rotulada como `ATENTO_LONGITUDINAL`.

### ENPMR adapter

Objetivo:
- carregar memory bank;
- latent emotional need;
- gold supportive memory mapping;
- avaliar need inference e retrieval de forma separada.

### TEA-Bench adapter

Objetivo:
- compatibilizar tool fixture/MCP sandbox;
- capturar tool process trace;
- executar com tools ON/OFF;
- medir ganho e regressões de grounding.

O Atento deve poder rodar:
- `tools_disabled`;
- `tools_enabled`;
- `tool_failure_injected`.

### MentalHealthBench adapter

Objetivo:
- executar benchmark aberto conforme protocolo oficial;
- preservar rubricas/weights;
- armazenar decomposição por acuity/persona/dimension;
- não misturar score oficial com suites internas.

### CounselBench adapter

Objetivo:
- executar Eval e Adv separadamente;
- manter dimensões originais;
- usar expert annotations quando disponíveis;
- medir divergência human-vs-LLM judge.

---

## 11. System matrix

A matriz está em `evals/config/system_matrix.json`.

Categorias obrigatórias:

```text
baseline_single_pass
baseline_strong_prompt
atento_no_memory
atento_no_planner
atento_no_critic
atento_full
psychat_upstream        # spike only
psychat_adapted         # spike only
specialized_generators  # via Model Gateway
```

Toda ablation deve mudar **uma variável arquitetural principal por vez**.

---

## 12. Release gates

Configuração em `evals/config/release_gates.json`.

### Gates imediatamente bloqueantes

- critical safety failures > 0;
- cross-user memory leak > 0;
- unauthorized external action > 0;
- secrets/credential disclosure > 0;
- schema-breaking error acima do limite definido.

### Gates que exigem calibração antes de ativar

- strategy accuracy;
- belief calibration;
- memory recall;
- tool F1;
- RAG faithfulness;
- pairwise win rate;
- p95 latency;
- cost/turn.

O harness não inventa thresholds de qualidade antes de existir baseline.

---

## 13. Release comparison

A comparação padrão deve produzir:

```text
candidate vs baseline
├── core
├── strategy
├── state/belief
├── memory
├── longitudinal
├── rag
├── tools
├── safety
├── adversarial
├── privacy
├── cost
└── latency
```

Não mostrar apenas média. Sempre mostrar distribuição e segmentos críticos.

---

## 14. Fork/clone evaluation

O gate pré-migração da ADR-000 e cada migração por bloco usam o mesmo harness.

Para PsyChat, comparar:

```text
PsyChat upstream
PsyChat + Atento adapters
Atento clean-room vertical slice
```

O report deve medir:
- quality;
- strategy;
- safety;
- RAG;
- latency;
- cost;
- chassis fitness;
- adaptation touchpoints;
- amount of upstream code retained.

Isso alimenta `ADR-000-fork-vs-greenfield.md`.

---

## 15. Directory layout

```text
evals/
├── README.md
├── atentoeval/
│   ├── __init__.py
│   ├── schema.py
│   ├── metrics.py
│   ├── gates.py
│   └── runner.py
├── cases/
│   └── core_v0.jsonl
├── config/
│   ├── benchmark_registry.json
│   ├── release_gates.json
│   └── system_matrix.json
├── results/
│   └── .gitkeep
└── tests/
    ├── test_metrics.py
    └── test_gates.py
```

External benchmark datasets should normally live outside the repository and be referenced by path/environment configuration.

---

## 16. Implementation order

1. canonical schemas;
2. offline scoring;
3. release gates;
4. internal synthetic core suite;
5. Atento SUT adapter;
6. PsyChat spike adapter;
7. deterministic trace metrics;
8. judge interface;
9. human-review export;
10. external benchmark adapters.

Isso permite começar a medir a arquitetura antes que todos os benchmarks externos estejam integrados.
