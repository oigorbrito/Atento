# Handoff — Atento chassi comum — 2026-10-02

## Objetivo e estado da decisão

Avaliar por gates eliminatórios, com o mesmo denominador e evidência equivalente, o menor conjunto defensável para um chassi comum NAIA/Anna/Apollo. Reutilizar benchmarks e testes já executados; não transformar ausência de evidência ou bloqueio do harness em falha de candidato.

- **Chassi comum:** MindRoom é a direção provisória e reversível registrada na PR #59; permanece pausado enquanto os demais candidatos alcançam os gates comparáveis. Não está qualificado para produção.
- **NAIA:** NanoClaw continua direção provisória da base da NAIA apenas; não é escolha do chassi comum e segue sem qualificação integrada.
- **Anna:** Psych foi escolhida pelo usuário como base de Anna. A PR #59 ainda diz `NOT_SELECTED`; esse texto está em conflito com a decisão e deve ser reconciliado numa edição autorizada própria. Não alterar a PR neste bloco.
- **Apollo:** pesquisa funcional adiada.
- **Topologia de produção:** nenhum resultado de teste de componente/fixture prova a composição completa do Atento. Seleção sistêmica final permanece pendente.

## GitHub e limites de escrita

- Repositório: `oigorbrito/Atento`.
- PR #58: aberta em draft; head observado `e948f344b91e20e655399b11300c439228d144ec`. **Não alterar sem instrução específica.**
- PR #59: aberta em draft, documental; direção provisória MindRoom e próximo gate `BLOCKED_ADAPTER`. Nenhum runtime de produto foi adicionado.
- Branch de trabalho autorizada: `codex/disposable-nanoclaw-mobile-replay-20261001`.
- Head após as atualizações de evidência: `8a5be37d95df854063ce67279a5fa3b2e2be1dc2`. Este handoff é registrado na mesma branch descartável.
- Registro principal de execução: [spike comparativo por coorte](../evaluation/system-chassis-fixed-cohort-common-test-spike-2026-10-01.md).

## Progresso comparativo recente

### Gates de autoridade/background com falha reproduzida e escopo limitado

- **QwenPaw** `agentscope-ai/QwenPaw@777441721aa72db8e380d90e4d0481b05cbfd4cc`: cron sem configuração explícita produziu `approval_level=off`. `QWENPAW_DEFAULT_CRON_TOOL_AUTHORITY = FAIL_WITH_SCOPE`; o perfil padrão está eliminado neste pin. Caminho explícito restritivo, autorização Atento e família do repositório não foram eliminados.
- **OpenAkita** `openakita/openakita@5f5b38da728274f0fd06461a481851be7c0bca6a`: ID de perfil sintético ausente fez o scheduler instanciar o agente padrão. `FAIL_WITH_SCOPE` para role drift/fallback do scheduler; caminho padrão de tarefa role-bound eliminado neste pin. Composição com validação fail-closed pelo host continua possível, mas não existe nem foi testada.
- **Clawix** `ClawixAI/clawix@5aee015e0bd793102fba69af486dd6e75df6d802`: aprovação allow associada à sessão pai foi aceita no sub-agent com o mesmo session ID. `FAIL_WITH_SCOPE` para composição multi-role em sessão compartilhada; arquitetura com sessões separadas ainda não foi testada.

Esses resultados eliminam caminhos ou configurações reproduzidos, não as famílias inteiras quando uma composição distinta pode corrigir a fronteira. Não generalizar além do escopo observado.

### Gate de marcador privado para o horizonte suplementar

| Candidato/pin | Resultado do teste comparável de componente |
|---|---|
| Open Pincery `fc33211c7b04e1a958a340c369cb635f018c13f4` | Bloqueado antes do corpo: teste de API exige PostgreSQL de teste isolado; não havia DB nem Docker/Podman. |
| OpenLegion `24efd6e06b28768cbbcd9275f43c479b3df37b18` | Harness bloqueado: teste não chegou à coleta; pin não tem uv.lock e o runner alternativo não teve paridade de dependências comprovada. |
| Moltis `1f6d28ea750d6654d52d5899b8be67727ebf7a19` | Bloqueado antes do teste por ausência de cargo. Probe temporário foi removido sem execução. |
| HybridClaw `b9378588f9f9666355fc5431a7b1f5292aaa93c0` | `PASS_WITH_SCOPE`: SQLite real; valor sob chave Anna não foi retornado sob chave NAIA. Identidades/chaves sintéticas; nenhum HostExecutor/Atento. |
| Hivekeep `7d023c952e46861070683825ff545daf981910f0` | `PASS_WITH_SCOPE`: SQLite real e serviço de memória de produção; Anna listou/buscou só a própria linha privada. IDs sintéticos e inserção direta via Drizzle; nenhum runtime/API de autorização Atento. |
| OpenVole `c8b405f4933a5ee0a1cb7725cf4c8a31cd24d732` | Não testado para este gate: testes disponíveis delimitam projetos, não identidade de agente/papel. |

Bloqueios de ambiente/harness não contam como FAIL. Os dois PASS_WITH_SCOPE são evidência de armazenamento/serviço, não provam que o host Atento vincule papel a chave/caminho.

## Evidência reutilizada — não repetir

- NanoClaw: run Atento anterior 7/7 com escopo; upstream lifecycle já auditado; replay SSE após SIGKILL no servidor raw webhook, SQLite persistente e porta reaproveitada passou com token sintético. Não prova provider real, auth de produção, runtime Atento ou retry da tarefa após restart.
- QwenPaw: API de memória negou GET cross-agent (404) no pin; gate separado do cron permissivo.
- Ontheia: suíte de namespace/memory e helper explícito de namespace por agent ID já executados com escopos distintos.
- OpenAkita: isolamento same-user/two-workspace aprovado antes do novo achado de identidade do scheduler.
- MindRoom: gates existentes de memory e worker foram registrados; manter pausa e não repetir enquanto outros não alcançarem o mesmo nível.
- Reutilizar também as suítes citadas de claim órfão, recorrência/backoff e atomicidade/retry. Não repetir o probe 7/7, replay SSE aprovado, benchmark upstream ou suites equivalentes.
- Scores publicados ficam separados por benchmark/configuração. Não somar métricas entre benchmarks diferentes.

## Gate integrado ainda bloqueado

`NAIA_HOST_PROCESS_TASK_RETRY_AFTER_RESTART = BLOCKED_ADAPTER`.

Nos documentos e heads inspecionados, o Atento não fornece um host runtime/gateway/provider executável para este caminho. A PR #58 documenta essa lacuna; a PR #59 acrescenta reconciliação documental, não runtime. Não criar integração de produção só para abrir o teste.

### Menor teste falsificável quando houver seam

Pré-condições: host existente executável com adapter para pin congelado; identidade sintética NAIA; tarefa inerte sem provider; IDs observáveis de claim e entrega terminal; persistência real usada pelo runtime do candidato.

1. Persistir uma tarefa agendada vencida pertencente à NAIA.
2. Encerrar o host depois do claim e antes do ack terminal.
3. Reiniciar o mesmo host/store e permitir exatamente uma tentativa de retry.
4. Verificar que a tarefa continua NAIA-owned, mantém grants iguais ou mais restritos e gera exatamente uma entrega terminal.
5. Falhar o teste se houver drift de papel, conteúdo privado cross-role, grant ampliado, ausência de retry ou duplicação terminal.

Executar um candidato por vez. Sem seam, conservar `BLOCKED_ADAPTER`; não substituir por fixture isolada e não inferir aprovação sistêmica.

## Próximo trabalho

1. Anna: Psych está escolhida pelo usuário; a PR #59 ainda diz `NOT_SELECTED`. Preservar a PR e tratar essa reconciliação documental separadamente.
2. Continuar os mesmos gates eliminatórios nos candidatos ainda elegíveis, um por vez; usar resultados de benchmark já publicados como pontuação do eixo correspondente.
3. Ao surgir host/adapter executável existente, executar uma única vez o teste de restart/retry acima para cada candidato que chegar a essa etapa.
4. Só comparar ou escolher chassi comum quando a matriz apresentar evidência comparável suficiente; até lá, MindRoom permanece direção provisória/pausada, NanoClaw permanece direção provisória da NAIA, e nenhum deles é qualificado para produção.

Classificações obrigatórias: `PASS_WITH_SCOPE` nunca significa qualificação geral; `BLOCKED_ENVIRONMENT`/`BLOCKED_HARNESS` não são falhas do candidato; benchmark não é prova local; teste de componente não é prova de integração.


## SYS-MEM catch-up — 2026-10-02

- Bob Labs `a91d6dad…`: `BLOCKED_ENVIRONMENT`; its official `make test-only` requires Docker and the pinned API image. No test body ran.
- Ontheia `70802db6…`: reuse the already-recorded configured `agent_id` namespace probe as `PASS_WITH_SCOPE`. The extra 19/19 user-namespace unit-suite run was overlapping validation, not a new role-memory result.
- OpenAkita: reuse the existing private-marker pass; no rerun.
- Next unresolved fixed-cohort memory slice: Clawix `5aee015e0bd793102fba69af486dd6e75df6d802`; only continue if its real seam permits the frozen private-marker assertion.
- Common Atento `SYS-MEM-01` remains `BLOCKED_ADAPTER`. No candidate elimination follows from missing evidence.
- Detailed provenance and test scope: [fixed-cohort common test spike](../evaluation/system-chassis-fixed-cohort-common-test-spike-2026-10-01.md).


## Fixed-cohort memory slice closure — 2026-10-02

The latest candidate-specific catch-up adds Memoh's exact-pin PostgreSQL store denial and Letta Code's exact-pin 63/63 permission-guard suite. Bob Labs remains blocked before its test body by the official Docker runner/image; Clawix remains untested for the same private-marker read property; Ontheia's extra user-namespace test was redundant with the already-recorded role-key helper. OpenAkita evidence was reused. No candidate was eliminated from missing evidence.

The complete status and test provenance now appear in the [fixed-cohort spike record](../evaluation/system-chassis-fixed-cohort-common-test-spike-2026-10-01.md). Component passes remain scoped; the integrated common `SYS-MEM-01` is still `BLOCKED_ADAPTER` because the Atento host/runtime seam is absent.

Next block: continue the frozen cohort's tool-authority denial evidence using existing exact-pin tests/results first. Keep the common Atento `SYS-TOOL-01` blocked until an already-existing host adapter can exercise the same three-role profile; do not fabricate a production adapter.


## SYS-TOOL-01 catch-up — 2026-10-02

Reused candidate evidence shows scoped filters for QwenPaw, Ontheia, and OpenAkita; NanoClaw's no-grant native A2A denial and limited brokered-mailbox path; and a reproduced Clawix `FAIL_WITH_SCOPE` for shared-session approval reuse. The Clawix result applies to that path only. Other unmeasured candidates remain unmeasured, not failed.

The common Atento `SYS-TOOL-01` remains `BLOCKED_ADAPTER`. Exact pins, provenance, and the candidate-by-candidate boundaries are recorded in the [fixed-cohort spike](../evaluation/system-chassis-fixed-cohort-common-test-spike-2026-10-01.md). Next block: credential/provider isolation, reusing the frozen evidence and not rerunning equivalent probes.


## User-decision reconciliation — Anna / Psych — 2026-10-02

The prior handoff's wording that the user choice of Psych could not be verified is superseded by the user's continuity context, which confirms the explicit decision “Psych escolhida como Anna.” Treat Psych as the user's selected Anna base for project planning. The repository/PR #59 still says `NOT_SELECTED`; that documentation conflict remains to be reconciled in an authorized future edit. This handoff-only correction does not alter PR #59 or qualify Psych's integration.


## SYS-CRED-01 catch-up and Anna decision correction — 2026-10-02

Reused component evidence for QwenPaw (mock personal-provider selection), Bob Labs (HMAC/lab-binding unit tests), Ontheia (missing-secret exclusion and masking), and OpenAkita (diagnostic redaction). None proves provider-secret isolation across Atento roles. No real credentials or provider calls were used; common `SYS-CRED-01` remains `BLOCKED_ADAPTER`. The exact candidate scopes are in the [fixed-cohort spike](../evaluation/system-chassis-fixed-cohort-common-test-spike-2026-10-01.md).

Anna's base is Psych by the user's earlier explicit decision. PR #59 still carries `NOT_SELECTED`; preserve PR #59 and reconcile that text only under its own authorization.



## SYS-REL-01 catch-up — 2026-10-02

Reused the fixed-pin evidence for all 11 candidates and recorded each scope in the [fixed-cohort spike](../evaluation/system-chassis-fixed-cohort-common-test-spike-2026-10-01.md). No equivalent suite, benchmark, replay, or recovery test was rerun.

- NanoClaw has scoped candidate lifecycle and raw-webhook SSE replay passes; neither proves role-bound scheduled-task retry across Atento host restart.
- OpenClaw has one scoped SSE replay after SIGKILL/restart; no scheduled retry or real Atento auth/provider result.
- AI Butler's narrow scheduler test remains scoped, while its current pin remains blocked by seven reachable advisories.
- Reproduced path-specific failures remain limited to QwenPaw default cron authority, Ontheia one-shot `run_at` post-claim recovery, and OpenAkita unknown-profile scheduler fallback/role drift. Do not generalize to entire candidate families.
- MindRoom, Clawix, Memoh, and Letta Code have no comparable restart/recovery result recorded; Bob Labs remains blocked before test execution by the missing official Docker runner/image. Missing or blocked evidence is not a candidate failure.

```text
COMMON_ATENTO_SYS_REL_01 = BLOCKED_ADAPTER
NAIA_HOST_PROCESS_TASK_RETRY_AFTER_RESTART = BLOCKED_ADAPTER
EQUIVALENT_TESTS_OR_BENCHMARKS_RERUN = 0
CANDIDATES_ELIMINATED_FROM_MISSING_EVIDENCE = 0
```

The existing Atento host/runtime seam still cannot execute the real scheduled-task path. Preserve the minimal falsifiable restart/retry test already specified above; when an existing seam becomes available, run one candidate at a time and verify original role ownership, equal-or-narrower grants, and exactly one terminal delivery. Do not construct a production adapter solely to open this gate. The next block remains the next comparable frozen-cohort gate; MindRoom stays paused until the cohort catches up.


## SYS-COST-01 catch-up — 2026-10-02

A read-only GitHub metadata snapshot recorded current repository `size` for all 11 candidates as a coarse, time-sensitive proxy. These values describe the repositories now, not the frozen pins, source LOC, dependencies installed, deployment images, or runtime hardware needs. Exact-pin LOC and deployment footprint remain unavailable; OpenClaw's current repository size must not be treated as its minimum runtime footprint.

Adaptation cost is not ranked: existing notes locate three candidate-specific failure paths (QwenPaw default cron authority, Ontheia one-shot `run_at` post-claim recovery, OpenAkita unknown-profile scheduler fallback), but do not prove frozen-pin patch scope, dependency/build effects, or a minimal corrective test. The spike records the raw repository-size metadata and the next bounded evidence step.

```text
EXACT_PIN_SOURCE_SIZE = NOT_AVAILABLE
ADAPTATION_FIX_COST_RANK = NOT_ESTIMATED
CANDIDATE_RANKING_OR_SELECTION_CHANGED = NO
MINDROOM_REMAINS_PAUSED = YES
```

Next bounded action: inspect those three failing paths at their frozen pins only, define one repair-effort rubric, and retain the current statuses until the patch surface and falsifiable correction are evidenced. Do not edit candidate repos or protected Atento PRs for this audit. Anna's handoff status is Psych selected; PR #59's `NOT_SELECTED` remains a known documentary conflict and is still untouched.
