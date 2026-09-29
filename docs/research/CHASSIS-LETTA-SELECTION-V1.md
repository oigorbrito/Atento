# Chassis Selection V1 — Letta Code

## Document contract

Este documento é um **índice de pesquisa/evidência**. Ele não substitui `roadmap.md`, `docs/evaluation/harness.md` nem uma ADR aceita.

A rodada de benchmark arquitetural realizada em 2026-09-29 avaliou candidatos de chassis separando **arquitetura/forkabilidade** de **cobertura de features**. O pacote de evidência concluiu `letta-ai/letta-code` como `EXECUTABLE_CHASSIS_SELECTED` no SHA congelado `a75111ea610eff9b4a37baba4fbc6ee24bb73c79`, mantendo LibreChat como controle/fallback.

## O que está preservado nesta branch

- handoff retrospectivo do trabalho concluído;
- protocolo V1 e freeze V1.1;
- parity e decisão M8–M11;
- comparação executável Letta × LibreChat;
- relatório de full-checkout/CI do SHA congelado;
- scaffold F0–F5 e modelo de branch/change-control;
- benchmark empírico consolidado e matriz estruturada;
- archive técnico bruto para auditoria.

## Arquivos publicados

- `docs/evidence/CHASSIS-LETTA-SELECTION-2026-09-29.md` — handoff retrospectivo legível;
- `docs/evidence/CHASSIS-LETTA-SELECTION-2026-09-29.yaml` — handoff estruturado;
- `docs/research/chassis-selection-v1/EMPIRICAL-BENCHMARK-2026-09-29.md` — material empírico, testes, métricas, probes e resultados;
- `docs/research/chassis-selection-v1/EMPIRICAL-BENCHMARK-2026-09-29.yaml` — matriz estruturada para agentes;
- `docs/research/chassis-selection-v1/archive/` — evidência técnica bruta preservada;
- `docs/adr/ADR-001-executive-chassis-letta-code.md` — ADR proposta.

## Regra de leitura

O material desta branch registra evidência já produzida. Não deve ser interpretado como autorização automática para sobrescrever a arquitetura canônica de `main`. A promoção para arquitetura oficial do repositório deve acontecer pelo fluxo de ADR/revisão do Atento.
