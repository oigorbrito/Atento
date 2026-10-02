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

O snapshot de continuidade não contém um runtime/gateway do produto Atento que chame o chassi e mantenha o estado necessário para um evento de background. O PR #58 e o probe anterior delimitam essa lacuna. O workspace de avaliação disponível nesta sessão contém o MindRoom no pin acima, mas não o checkout Atento nem Docker; portanto não há como transformar os testes de componente existentes em uma prova de composição neste ambiente. A falta do adapter é bloqueio de infraestrutura de produto/harness, não falha do MindRoom.

Reutilizar, sem repetir, as evidências já registradas: particionamento das três chaves `user_agent` via resolver; casos de memória cross-agent com mocks; propagação de requester em teste em memória; testes upstream citados no registro de continuidade. Esses resultados permanecem `PASS_WITH_SCOPE`.

### Pré-condições para desbloquear

- Um seam executável do host Atento para iniciar/encaminhar trabalho à composição, com estado durável e um ponto observável de ack terminal.
- MindRoom no pin congelado, três identidades sintéticas mapeadas por papel e worker dedicado/`user_agent` para cada papel.
- Evento NAIA inerte e credenciais/provider ausentes; nenhum efeito externo ou chamada de modelo.
- Harness capaz de encerrar diretamente o processo host após claim e antes do ack terminal, reiniciar com o mesmo estado e observar retries/deliveries.

### Menor teste falsificável quando o seam existir

Persistir uma tarefa NAIA vencida; iniciar o host; observar o claim e encerrá-lo antes do ack terminal; reiniciar com o mesmo store e permitir exatamente um retry. Verificar que a tentativa recuperada continua NAIA-owned, conserva a mesma identidade/escopo `user_agent`, não lê estado das identidades sintéticas Anna/Apollo e produz no máximo uma entrega terminal para o ID da tarefa.

- **PASS_WITH_SCOPE:** identidade e propriedade NAIA sobrevivem ao restart e retry; estado alheio é inacessível; uma única entrega terminal observada.
- **FAIL do seam/configuração:** troca de papel, acesso cross-role ou entrega terminal duplicada com o harness válido.
- **INVALID / falha de harness:** SIGKILL atinge wrapper em vez do processo host, não se prova o estado pre-ack, o mesmo store não é reutilizado ou o controle de retry não é observável.
- **Permanece BLOCKED_ADAPTER:** não existe chamada executável do host Atento; não criar integração de produção só para destravar o teste.

Executar sequencialmente como um único probe descartável quando as pré-condições forem atendidas. Sem provider real, tarefas paralelas ou repetição dos testes equivalentes já citados.
