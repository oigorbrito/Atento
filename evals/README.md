# AtentoEval

> **DECISION RESET:** o harness preserva evidência e infraestrutura de avaliação, mas nenhum adapter, system entry ou candidate registry entry constitui shortlist ou prioridade de NAIA/Anna/Apollo.

## Document contract

Este README é **operacional**: como executar o harness, formatos de entrada/saída e status dos adapters.

A metodologia pertence a `docs/evaluation/harness.md`. O progresso global pertence a `roadmap.md`. Não duplicar aqui thresholds, decisões arquiteturais ou regras de licença.

Scaffold do evaluation harness do Atento.

A especificação completa está em [docs/evaluation/harness.md](../docs/evaluation/harness.md).

## Objetivos

- comparar baselines, ablations, forks e modelos;
- medir resposta **e** trace interno;
- manter benchmarks externos separados por protocolo;
- bloquear regressões críticas de safety/privacy;
- produzir resultados reproduzíveis com manifest versionado.

## Quick start — scoring offline

Atualmente o scaffold implementa scoring offline de resultados já gerados.

```bash
python -m evals.atentoeval.runner \
  --cases evals/cases/core_v0.jsonl \
  --agent-scope ANNA \
  --agent-scope SHARED \
  --results /path/to/results.jsonl \
  --gates evals/config/release_gates.json
```

Formato esperado para cada linha de `results.jsonl`:

```json
{
  "case_id": "core.validation.001",
  "step_index": 0,
  "response": "texto da resposta",
  "trace": {
    "plan": {"strategy": "validation"},
    "memory": {"retrieved_ids": []},
    "tools": [],
    "safety": {"route": "normal"}
  },
  "latency_ms": 420.1,
  "usage": {
    "input_tokens": 100,
    "output_tokens": 80,
    "cost_usd": 0.001
  },
  "judge": {
    "weighted_behavior_score": 0.0,
    "critical_failure": false
  }
}
```

## Backlog histórico de adapters — sem prioridade decisória

A lista abaixo preserva integrações já consideradas, mas **não é ordem de execução**:

- runtime Atento;
- PsyChat upstream/adapted;
- ESConv;
- PsychEval;
- ENPMR-Bench;
- TEA-Bench;
- MentalHealthBench;
- CounselBench.

Novos adapters orientados a seleção só devem ser priorizados depois da reenumeração de chassis comparáveis da NAIA ou da Anna. Apollo permanece adiado.

Não coloque datasets externos aqui sem revisar licença e provenance.


## Candidate registry

Candidatos de donor/fork/native ficam em `evals/config/candidates.json`.

A identidade reproduzível de candidato inclui:

```text
candidate_id
block                           # eixo histórico de evidência; não arquitetura final
SOURCE_ID
variant
agent_scope
candidate_class
selection_status
repository + full upstream SHA (quando externo)
adapter_id
```

Validar o registry:

```bash
python -m evals.atentoeval.candidates validate-registry \
  --registry evals/config/candidates.json
```

Gerar a matrix usada pela CI:

```bash
python -m evals.atentoeval.candidates github-matrix \
  --registry evals/config/candidates.json
```

O workflow genérico é `.github/workflows/candidate-eval.yml`. Durante o `DECISION_RESET`, validação do registry pode rodar em CI, mas a execução de donor específico fica manual. Adicionar um donor ao registry, habilitar CI ou produzir `PASS_STATIC` **não** significa shortlist, promoção ou adoção.

Cada job gera um candidate-result tipado. O status de evidência distingue explicitamente:

- `PASS_EMPIRICAL`;
- `PASS_STATIC`;
- `PENDING_EXECUTION`;
- `INFRA_BLOCKED`;
- `QUALITY_RISK`;
- `ARCH_RISK`;
- `NOT_DECIDED`.

`PASS_STATIC` nunca deve ser convertido em runtime PASS por interpretação.

A metodologia multi-candidato está registrada em
`docs/evaluation/donor-candidate-comparison-research-2026-09-29.md`.

## Agent scope

O `core_v0.jsonl` contém casos explicitamente marcados como `ANNA`, `NAIA` ou `SHARED`.

Para decisão de seleção, não usar uma média comportamental que misture agentes. O relatório expõe `by_agent_scope` e marca quando uma execução contém múltiplos scopes. Casos `SHARED` podem ser executados junto ao agente relevante quando representam invariantes comuns de privacy/safety.
