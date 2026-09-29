# AtentoEval

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

## Próximos adapters

- Atento runtime;
- PsyChat upstream/adapted;
- ESConv;
- PsychEval;
- ENPMR-Bench;
- TEA-Bench;
- MentalHealthBench;
- CounselBench.

Não coloque datasets externos aqui sem revisar licença e provenance.


## Candidate registry

Candidatos de donor/fork/native ficam em `evals/config/candidates.json`.

A identidade reproduzível de candidato inclui:

```text
candidate_id
block
SOURCE_ID
variant
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

O workflow genérico é `.github/workflows/candidate-eval.yml`. Ele executa somente entradas com `ci_enabled=true` e perfil suportado. Adicionar um donor ao registry **não** significa promovê-lo nem adotá-lo.

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
