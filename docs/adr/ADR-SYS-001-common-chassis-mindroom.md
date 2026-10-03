# ADR-SYS-001 — Chassi geral e composição dos três agentes

## Status (2026-10-02)

**Nenhum chassi comum está qualificado ou selecionado para produção.** MindRoom é o próximo candidato a validar como runtime comum, sujeito ao adapter de execução do Atento. NanoClaw é direção provisória apenas para a base funcional da NAIA. São decisões distintas.

| Decisão | Estado atual | Autoridade |
|---|---|---|
| Base funcional geral da NAIA | NanoClaw, direção provisória do usuário; não qualificado | [ADR-002](ADR-002-assistant-base-selection.md) |
| Base funcional da Anna | PsychAgent, direção escolhida pelo usuário; qualificação pendente | [ADR-ANNA-001](ADR-ANNA-001-therapeutic-base-selection.md) |
| Base funcional do Apollo | Adiada | [ADR-APOLLO-001](ADR-APOLLO-001-fitness-nutrition-base-selection.md) |
| Runtime/chassi comum dos três | Sem vencedor. MindRoom é o próximo candidato a validar, bloqueado pelo adapter | Esta ADR |

“Chassi geral” significa aqui a base funcional geral da NAIA; não significa que NanoClaw hospede os outros agentes. MindRoom, se passar os gates, seria o runtime compartilhado ao redor das bases funcionais por papel.

## Evidência do candidato MindRoom

Pin: `mindroom-ai/mindroom@4f3bd2d108a6f9be28174e0f66d78eeecddca386`.

- Chaves distintas `user_agent`: `PASS_WITH_SCOPE`; prova o resolvedor, não workers/processos persistentes.
- Memória cross-agent: três casos mock-based passaram; não provam isolamento real de filesystem/storage.
- Propagação de requester em scheduler: dois testes em memória passaram.
- Guarda de `base_dir`: quatro casos passaram; não prova isolamento contra caminhos absolutos ou mounts compartilhados.
- API OpenAI-compatible: 2/2 testes demonstraram que cabeçalho do solicitante não estabelece identidade e `/v1` rejeita `worker_scope=user_agent`. Resultado: `UNSUPPORTED_BY_PINNED_API`; essa API não é um seam de execução isolada.
- Host Atento + MindRoom, com tarefa agendada através de claim, queda, restart e retry: `BLOCKED_ADAPTER`. O runtime/gateway necessário não existe no snapshot auditado.

Esses resultados não elegem MindRoom nem eliminam a família. Fontes: [rescreen sistêmico e matriz de evidências](../evaluation/system-chassis-benchmark-crosscheck-2026-09-30.md), [continuidade do Gate 2](../evaluation/system-chassis-gate2-continuation-2026-10-01.md), [NCP-03 histórico](../evaluation/naia-common-probe-profile-2026-09-29.md) e [contrato do host, PR #57](../evaluation/atento-host-runtime-boundary-contract-2026-10-01.md).

## Teste eliminatório SYSTEM-ISO-01

Este é um hard gate de autorização/fluxo de dados, não um benchmark de qualidade de respostas. A exigência é defensável como contrato do produto: três papéis têm histórico, memória privada, credenciais, ferramentas e autoridade de background separados. A base normativa é negar acesso sem autorização e decidir acesso por identidade+recurso: [NIST SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final) e [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html). O benchmark [AgentDojo](https://proceedings.neurips.cc/paper_files/paper/2024/hash/97091a5177d8dc64b1da8bf3e1f6fb54-Abstract-Datasets_and_Benchmarks_Track.html) pode suplementar ataques por prompt injection contra ferramentas; ele não prova isolamento entre papéis e não substitui este gate.

### Preparação e protocolo

Fixar commit do candidato, adapter, configuração e topologia. Criar para NAIA, Anna e Apollo canários únicos não inferíveis (um por papel em histórico, memória, credencial e ferramenta sem efeito externo). Observar a decisão e o resultado no boundary técnico de autorização/storage/tool gateway; uma recusa textual do modelo não conta.

Executar deterministicamente:

1. Controle positivo: cada papel lê seu próprio canário e usa sua ferramenta permitida.
2. Para cada um dos seis pares direcionados entre papéis, tentar ler o histórico/memória e obter/usar a credencial/ferramenta privada do outro papel.
3. Repetir a tentativa com identidade ausente/desconhecida, identidade adulterada, contexto de sessão cruzado e via tarefa agendada/delegada.
4. Confirmar que todo acesso negado é bloqueado no boundary, sem valor do canário no retorno, trace, log ou efeito colateral.
5. Controle de exceção: somente após pedido explícito do usuário, permitir mensagem tipada de payload mínimo; reautorizar no destinatário; deduplicar replay. Consulta a histórico exige pedido explícito e devolve apenas resumo/trecho necessário, sem conceder acesso persistente.

### Critério

```text
OWN_ROLE_POSITIVE_CONTROLS = PASS
UNAUTHORIZED_CROSS_ROLE_READ_WRITE_DELETE_OR_ACTION = 0
UNKNOWN_OR_MISSING_IDENTITY = DENY
SCHEDULED_OR_DELEGATED_AUTHORITY > INTERACTIVE_AUTHORITY = NO
UNAUTHORIZED_CANARY_DISCLOSURE_OR_SIDE_EFFECT = 0
USER_REQUESTED_MINIMAL_HANDOFF = PASS
AUDIT_PROVENANCE_AND_REPLAY_DEDUP = PASS
```

**ELIMINAR a composição/pin** se uma tentativa não autorizada alcançar dado, credencial ou ação protegida, se identidade desconhecida falhar aberta, ou se trabalho agendado/delegado ganhar autoridade. Um falso negativo isolado reprova; não usar média nem pontuação agregada para compensar.

**Não eliminar** quando o adapter/harness não atingir o boundary ou não puder observar o resultado: classificar `BLOCKED_ADAPTER`/`INVALID`, corrigir a instrumentação e executar uma vez. Ausência de evidência não é falha do candidato. Registro com pin, fixtures, matriz de tentativas, resultado bruto e artefatos de auditoria é requisito para uma decisão defensável.

O gate elimina uma composição técnica, não declara segurança absoluta do produto.

## Regra de contato entre agentes

Padrão: nenhum agente lê o histórico ou memória privada dos demais; nenhuma delegação/notificação implícita; nenhum compartilhamento de credencial, ferramenta ou autoridade de background.

Sob comando explícito do usuário:

- Lembrete/informação: mensagem tipada com payload mínimo, origem, destinatário e ID deduplicável; destinatário reautoriza qualquer ação; registrar auditoria.
- Consulta de histórico: resumo/trecho mínimo ligado ao pedido, proveniência preservada e sem acesso contínuo. Se o pedido não determinar o contexto necessário, perguntar antes de ampliar.

A exceção vale só para a operação e o conteúdo autorizados; não cria memória compartilhada.

## Gates seguintes e estado de qualificação

Após SYSTEM-ISO-01 passar, validar separadamente continuidade após restart/retry e custo comparável. Já há um teste falsificável proposto para tarefa NAIA após claim/queda/restart; permanece `BLOCKED_ADAPTER`, sem repetir até existir host executável e observável.

Project Points e progresso continuam sob autoridade de `roadmap.md`. Esta ADR registra decisão e gate, não implementação nem qualificação de produção.
