# AtentoEval

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
