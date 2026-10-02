# Handoff — Atento chassi comum — 2026-10-02

## Objetivo e estado da decisão

Avaliar por gates eliminatórios, com o mesmo denominador e evidência equivalente, o menor conjunto defensável para um chassi comum NAIA/Anna/Apollo. Reutilizar benchmarks e testes já executados; não transformar ausência de evidência ou bloqueio do harness em falha de candidato.

- **Chassi comum:** MindRoom é a direção provisória e reversível registrada na PR #59; permanece pausado enquanto os demais candidatos alcançam os gates comparáveis. Não está qualificado para produção.
- **NAIA:** NanoClaw continua direção provisória da base da NAIA apenas; não é escolha do chassi comum e segue sem qualificação integrada.
- **Anna:** PR #59 e a instrução explícita mais recente localizada mantêm a base como `NOT_SELECTED`. A frase “Psych escolhida como Anna” aparece em registro de continuidade, mas não foi possível verificar uma mensagem do usuário que a confirme; não tratar Psych como escolhida sem fonte confirmatória.
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

1. Anna reconciliada para este handoff: manter `NOT_SELECTED`; a alegação de escolha de Psych não tem confirmação user-sourced disponível.
2. Continuar os mesmos gates eliminatórios nos candidatos ainda elegíveis, um por vez; usar resultados de benchmark já publicados como pontuação do eixo correspondente.
3. Ao surgir host/adapter executável existente, executar uma única vez o teste de restart/retry acima para cada candidato que chegar a essa etapa.
4. Só comparar ou escolher chassi comum quando a matriz apresentar evidência comparável suficiente; até lá, MindRoom permanece direção provisória/pausada, NanoClaw permanece direção provisória da NAIA, e nenhum deles é qualificado para produção.

Classificações obrigatórias: `PASS_WITH_SCOPE` nunca significa qualificação geral; `BLOCKED_ENVIRONMENT`/`BLOCKED_HARNESS` não são falhas do candidato; benchmark não é prova local; teste de componente não é prova de integração.
