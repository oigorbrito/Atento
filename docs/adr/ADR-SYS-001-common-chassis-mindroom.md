# ADR-SYS-001 — Chassi comum dos três agentes — 2026-10-02

## Status

**DECIDED_FOR_REVERSIBLE_IMPLEMENTATION; NOT_QUALIFIED**

- Chassi comum selecionado para avançar: **MindRoom**.
- Fonte fixada: `mindroom-ai/mindroom@4f3bd2d108a6f9be28174e0f66d78eeecddca386`.
- Alternativa de arquitetura: plataforma multiagente integrada, com isolamento por papel.
- Escopo: NAIA, Anna e Apollo como identidades separadas no chassi compartilhado.
- Esta decisão não altera as decisões de base funcional de cada agente.

## Decisão

Avançar com MindRoom como chassi/runtime comum para hospedar e coordenar NAIA, Anna e Apollo. Configurar identidades, sessões, estado, memória, ferramentas, credenciais e trabalho em segundo plano por agente. Para estado e execução, usar escopo `user_agent` e workers dedicados; o escopo compartilhado `user` não atende à fronteira requerida.

A topologia operacional exata entre o chassi e cada base funcional ainda precisa ser congelada no primeiro desenho de implementação. Em particular, esta decisão **não** presume que o código NanoClaw será incorporado ao MindRoom, nem que MindRoom substitua uma base funcional específica. Não copiar código do donor nesta etapa.

## Decisões independentes por agente

| Decisão | Estado em 2026-10-02 |
|---|---|
| Base funcional da NAIA | NanoClaw é a direção provisória já escolhida; ainda não qualificada para produção. |
| Base funcional da Anna | Não selecionada. |
| Base funcional do Apollo | Pesquisa de base adiada. |
| Chassi/runtime comum dos três | MindRoom selecionado para implementação reversível; qualificação pendente. |

## Por que MindRoom

MindRoom é a alternativa ainda elegível com o encaixe direto mais claro para um runtime multiagente persistente: identidades e sessões de agente, equipes/delegação, memória, ferramentas e escopos de worker. No pin congelado, testes focados de memória cross-agent (três casos mock-based) e propagação do solicitante em evento agendado (dois casos com runtime em memória) passaram com escopo. Um meta-probe adicional produziu chaves `user_agent` distintas para NAIA, Anna e Apollo no mesmo usuário/sala sintéticos.

A comparação também preserva os riscos materiais observados nos outros pins: o caminho `run_at` do Ontheia não recuperou uma tarefa após falha pós-claim; o scheduler padrão do OpenAkita substituiu perfil desconhecido pelo agente padrão; a sessão compartilhada do Clawix deixou aprovação do pai alcançar subagente; e o cron padrão do QwenPaw emitiu aprovação desligada. Esses achados têm escopo de caminho/configuração e não equivalem, isoladamente, à eliminação das famílias. Bloqueios de ambiente/harness nos demais candidatos não foram tratados como falha funcional.

## Evidência, limites e gates abertos

A decisão é uma escolha do candidato menos ruim para interromper a busca ampla e começar uma implementação pequena e reversível. Não é uma declaração de vencedor por custo: não há medição comparável de adaptação e manutenção para a composição completa.

Evidência atual:

- `MINDROOM_THREE_ROLE_WORKER_KEY_PARTITION = PASS_WITH_SCOPE`: chaves distintas no resolvedor; sem worker/processo persistente.
- `MINDROOM_CROSS_AGENT_MEMORY_READ_UPDATE_DELETE = PASS_WITH_SCOPE`: três casos mock-based.
- `MINDROOM_SCHEDULED_REQUESTER_PROPAGATION = PASS_WITH_SCOPE`: dois casos em memória.
- A extensão descartável do backend de arquivo ficou `BLOCKED_HARNESS` antes das asserções.
- O host/runtime e gateway de produto do Atento continuam ausentes; a composição completa de três agentes e o gate comum de reinício/retry seguem `BLOCKED_ADAPTER`.

Antes de qualquer qualificação ou release, a implementação deverá demonstrar, em sequência e com identidades/sentinelas sintéticas:

1. worker, sessão e armazenamento persistente separados para NAIA, Anna e Apollo;
2. negação cruzada de leitura/escrita de memória, ferramenta e credencial, inclusive sob identidade ausente ou worker compartilhado;
3. handoff tipado e mínimo com reautorização no destinatário;
4. tarefa agendada NAIA mantendo propriedade e autoridade após claim, reinício e retry, sem duplicar entrega terminal;
5. custo observado de adaptação, deploy, operação e atualização.

Se um hard gate falhar no adapter real, parar a promoção e revisar a topologia; não mascarar falha com prompt, nome de papel ou fixture.

## Reversibilidade e próxima ação

Manter MindRoom pinado e atrás de um limite de integração substituível. Implementar primeiro somente o seam mínimo de identidade/worker e registrar change surface. A decisão pode ser revertida se o primeiro probe real mostrar role drift, compartilhamento de autoridade, recuperação incorreta ou custo materialmente pior que a arquitetura composta.

Não alterar as PRs #57 e #58 como parte desta decisão. Esta ADR foi preparada em branch separada e não concede autorização de merge ou produção.


## Primeiro gate executável no Atento — 2026-10-02

```text
MINDROOM_ATENTO_HOST_RESTART_RETRY = BLOCKED_ADAPTER
```

Rechecagem de continuidade em 2026-10-02: `main` continua em `335c95f07b0c6a56c57d2a9cdf09f0a197200bf8`; a PR #58 segue aberta em draft no head `e948f344b91e20e655399b11300c439228d144ec`. Nenhum desses snapshots acrescenta um runtime/gateway de produto ao que o gate exige. A PR #58 não foi modificada.

O snapshot de continuidade não contém um runtime/gateway do produto Atento que chame o chassi e mantenha o estado necessário para um evento de background. O PR #58 e o probe anterior delimitam essa lacuna. O workspace de avaliação disponível nesta sessão contém o MindRoom no pin acima, mas não o checkout Atento nem Docker; portanto não há como transformar os testes de componente existentes em uma prova de composição neste ambiente. A falta do adapter é bloqueio de infraestrutura de produto/harness, não falha do MindRoom.

O `main` já contém a execução hospedada 36815873223, registrada em `docs/evaluation/system-chassis-gate2-continuation-2026-10-01.md`: 7/7 assertions limitadas passaram usando broker Atento de referência, APIs mailbox do NanoClaw, identidades sintéticas e tarefas de perfil. Essa evidência inclui autorização de handoff e dispatch sob identidade NAIA; não executa o runtime/gateway de produto, não mata/reinicia o processo host entre claim e ack terminal e não envolve workers `user_agent` do MindRoom. Ela fecha escopos anteriores sem fechar este gate.

Reutilizar, sem repetir, as evidências já registradas: particionamento das três chaves `user_agent` via resolver; casos de memória cross-agent com mocks; propagação de requester em teste em memória; testes upstream citados no registro de continuidade. Esses resultados permanecem `PASS_WITH_SCOPE`.

### Pré-condições para desbloquear

- Um seam executável do host Atento para iniciar/encaminhar trabalho à composição, com estado durável e um ponto observável de ack terminal.
- MindRoom no pin congelado, três identidades sintéticas mapeadas por papel e worker dedicado/`user_agent` para cada papel.
- Evento NAIA inerte e credenciais/provider ausentes; nenhum efeito externo ou chamada de modelo.
- Harness capaz de encerrar diretamente o processo host após claim e antes do ack terminal, reiniciar com o mesmo estado e observar retries/deliveries.

### Menor teste falsificável quando o seam existir

Persistir uma tarefa NAIA vencida; iniciar o host; observar o claim e encerrá-lo antes do ack terminal; reiniciar com o mesmo store e permitir exatamente um retry. Verificar que a tentativa recuperada continua NAIA-owned, conserva a mesma identidade/escopo `user_agent`, não lê estado das identidades sintéticas Anna/Apollo e produz exatamente uma entrega terminal para o ID da tarefa após o retry.

- **PASS_WITH_SCOPE:** identidade e propriedade NAIA sobrevivem ao restart e retry; estado alheio é inacessível; exatamente uma entrega terminal é observada após o retry.
- **FAIL do seam/configuração:** troca de papel, acesso cross-role, ausência de entrega terminal após o retry ou entrega terminal duplicada com o harness válido.
- **INVALID / falha de harness:** SIGKILL atinge wrapper em vez do processo host, não se prova o estado pre-ack, o mesmo store não é reutilizado ou o controle de retry não é observável.
- **Permanece BLOCKED_ADAPTER:** não existe chamada executável do host Atento; não criar integração de produção só para destravar o teste.

Executar sequencialmente como um único probe descartável quando as pré-condições forem atendidas. Sem provider real, tarefas paralelas ou repetição dos testes equivalentes já citados.


## Revalidação do seam e do gate — 2026-10-02

A direção de implementação do chassi comum continua sendo **MindRoom**, em caráter reversível. Esta revalidação não promove o candidato a qualificado e não muda a base independente da NAIA (NanoClaw); Anna continua sem base e Apollo adiado.

Testes focados no pin 4f3bd2d108a6f9be28174e0f66d78eeecddca386 foram executados em sequência, sem provider nem rede externa:

- tests/test_openai_compat.py::TestChatCompletions::test_requester_header_is_not_used_for_execution_identity
- tests/test_openai_compat.py::TestChatCompletions::test_rejects_non_shared_worker_scope_agent

**2/2 passaram.** O resultado confirma uma restrição real do contrato atual do pin: cabeçalho do solicitante não estabelece identidade confiável e /v1 rejeita worker_scope=user_agent. Portanto, a API OpenAI-compatible padrão **não pode ser usada como seam de execução com isolamento por papel** na configuração exigida. Isso é evidência contra esse caminho específico, não prova de que todo o MindRoom seja inviável: os testes do backend Docker (258) e Kubernetes (201) também passaram, mas exercitam APIs simuladas; nenhum container ou cluster real foi iniciado.

As suítes amplas de recuperação não produziram resultado válido neste executor: houve bloqueio de bind de socket local em um teste e timeout/hang em tentativas mais amplas. A suíte completa também não coletou por dependências opcionais ausentes e caminhos de fixture sem permissão. Esses resultados são **BLOCKED_HARNESS/INCONCLUSIVE**, não falha funcional do MindRoom; não serão repetidos sem mudança concreta do ambiente.

O gate Atento permanece:

```text
MINDROOM_OPENAI_COMPAT_USER_AGENT_EXECUTION = UNSUPPORTED_BY_PINNED_API
MINDROOM_ATENTO_HOST_RESTART_RETRY = BLOCKED_ADAPTER
```

A checagem da PR #58 confirmou que ela segue aberta/draft no head e948f344b91e20e655399b11300c439228d144ec. Seu harness 7/7 é de escopo limitado e não acrescenta host runtime/gateway de produto. O registro do spike NanoClaw também continua descrevendo apenas um seam descartável, sem integração de produto. Não existe, nesses snapshots, caminho executável para claim/restart/retry no host Atento. A PR #58 permanece intocada.

### Menor teste falsificável após surgir o seam

Pré-condições: adapter interno executável que derive a identidade de NAIA de uma fonte confiável do Atento (sem confiar em cabeçalho arbitrário do solicitante), ligue-a a worker dedicado/escopo isolado do MindRoom, persista tarefa e estado, e exponha claim e ack terminal observáveis. Para o teste, usar store reutilizável, uma tarefa NAIA inerte vencida, identidades sintéticas distintas para Anna/Apollo, provider ausente e controle para matar diretamente o processo host.

Executar uma vez, sequencialmente: persistir a tarefa vencida; iniciar o host e observar o claim; encerrá-lo após claim e antes do ack terminal; reiniciar com o mesmo store; permitir exatamente um retry. Aprovar com escopo somente se a tentativa continuar NAIA-owned, manter o mesmo isolamento/identidade, não alcançar estado de Anna/Apollo e gerar exatamente uma entrega terminal para o ID da tarefa. Classificar quebra de identidade, leitura cruzada ou entrega duplicada como falha do seam; falta de ponto executável/observável continua BLOCKED_ADAPTER. Não construir integração de produção só para abrir este teste.


## Probe decisório de caminho de workspace — 2026-10-02

No checkout MindRoom pinado, foi executado:

```text
./.venv/bin/pytest tests/api/test_sandbox_runner_api.py::test_prepare_worker_request_rejects_sibling_private_agent_root_for_user_agent_workers -n 0 --no-cov -q
4 passed
```

Os quatro casos rejeitam base_dir na workspace de outro agente, na raiz privada do próprio agente, na subárvore de sessões e na raiz acima do workspace. Classificação: USER_AGENT_REQUEST_BASE_DIR_GUARD = PASS_WITH_SCOPE.

Limite decisório: isso valida a checagem do caminho declarado pelo pedido; não prova isolamento de filesystem contra acesso por caminho absoluto, processo local ou storage mais amplo montado. O próprio plano upstream ainda classifica a visibilidade em shared-runner/local como incompleta. Assim, não fecha a lacuna de isolamento do chassi nem muda o gate de composição; mantém-se MindRoom como escolha reversível para avançar, com qualificação bloqueada até um backend/seam executável demonstrar a fronteira real entre papéis.
