# ADR-001 — Composição de agentes do produto

> **DECISION RESET — 2026-09-29:** preservar os requisitos de isolamento e a evidência já produzida, mas não tratar a topologia histórica abaixo como arquitetura selecionada. A nomenclatura corrente é **NAIA / Anna / Apollo**.

## Document contract

Esta ADR preserva a hipótese arquitetural histórica de separação entre domínios, mas sua topologia concreta está reaberta durante a reconciliação do produto.

Ela não escolhe o sistema-base da Assistente nem o sistema-base terapêutico. Essas seleções têm ADRs/evidências próprias.

- **Status:** Reopened — `DECISION_RESET`
- **Date:** 2026-09-29
- **Decision owners:** TBD

## Context

O produto agora possui três agentes conceitualmente distintos. Esta ADR histórica descrevia apenas dois deles e, por isso, não é mais suficiente como definição completa:

1. **NAIA — assistente pessoal/secretária**
   - calendário;
   - mensagens;
   - e-mail;
   - pesquisa;
   - compras;
   - rotinas;
   - computer/browser use;
   - ferramentas com side effects.

2. **Anna — assistente emocional/terapêutica**
   - conversa terapêutica;
   - memória longitudinal terapêutica;
   - planejamento;
   - skills/intervenções;
   - safety e escalation;
   - acompanhamento multi-sessão.

3. **Apollo — nutrição/personal trainer** — permanece adiado.

O requisito atual é que esses domínios não sejam fundidos em um agente onisciente com acesso irrestrito a tools, memória ou chats dos demais.

## Functional authority matrix

The product-level role contract is:

| Domain / capability | NAIA | Anna | Apollo |
|---|---|---|---|
| general personal assistant / secretary | **OWNER** | out of scope | out of scope |
| calendar, messages, email, shopping, general research | **OWNER / EXECUTOR** | handoff to NAIA | handoff to NAIA |
| browser/computer/apps and general personal side effects | **OWNER / EXECUTOR** | no inherited authority | no inherited authority |
| therapeutic/emotional conversation | out of scope except routing/handoff | **OWNER** | out of scope |
| therapeutic longitudinal memory / strategy / interventions | no default access | **OWNER** | no default access |
| therapeutic safety/escalation policy | no default ownership | **OWNER** | no default ownership |
| fitness/training/nutrition planning | out of scope except routing/handoff | out of scope | **OWNER** |
| fitness progress / adherence / wearable-domain state | no default access | no default access | **OWNER** |
| general logistics produced by another domain | **EXECUTOR after explicit handoff** | REQUESTER | REQUESTER |

Interpretation:

```text
DOMAIN_OWNER
!=
GENERAL_SIDE_EFFECT_EXECUTOR

NAIA = general personal operational executor
ANNA = therapeutic/emotional domain authority
APOLLO = fitness/nutrition domain authority
```

NAIA may be the primary user-facing entry point, but primary entry point does not grant cross-agent memory or tool authority.

Anna and Apollo may use tools that are intrinsic to their own domain under their own future policy. They do not inherit NAIA's general personal-action toolset.

## Historical candidate topology — not selected

```text
                         ATENTO PRODUCT
                              |
              +---------------+---------------+
              |                               |
             NAIA                         ANNA
      bounded context                   bounded context
              |                               |
              +--------- HANDOFF BROKER ------+
                    minimal / explicit
```

### Boundary invariants

O alvo arquitetural deve permitir provar:

```text
Therapist cannot query Assistant memory by default
Assistant cannot query Therapy memory by default

Therapist cannot invoke personal-side-effect tools by default
Assistant cannot invoke therapy internals by default

Cross-domain exchange uses explicit contracts
Cross-domain payload is minimum necessary
Sensitive handoff can require explicit user consent
Every handoff is auditable
```

A separação deve ser enforced pelo runtime/policy, não apenas por prompt ou fine-tuning.

## Example handoff

Durante uma sessão terapêutica:

> usuário relata dificuldade em marcar uma consulta médica.

A terapeuta pode propor:

```text
ACTION_REQUEST
type: appointment_help
minimum_payload:
  specialty: cardiology
  user_requested_help: true
```

O payload não deve carregar automaticamente:

- transcrição terapêutica;
- formulações clínicas;
- histórico emocional;
- notas privadas da sessão;
- memória terapêutica sem necessidade explícita.

A Assistente executa a tarefa operacional sob sua própria policy/approval boundary.

## Non-goals

Esta ADR não determina:

- monorepo vs múltiplos repositórios;
- mesma linguagem/runtime;
- mesmo banco;
- mesmo provedor de modelo;
- mesma engine de memória;
- que o usuário deva perceber duas marcas/produtos;
- que um sistema possa ler o armazenamento interno do outro.

Um único produto pode conter dois runtimes independentemente autorizados.

## Why this is proposed rather than accepted

A direção reduz blast radius e segue least privilege/data minimization, mas ainda precisa ser concretizada e testada no Atento.

Antes de aceitar:

- definir contratos de handoff;
- definir esquema de consentimento;
- provar isolamento de tools;
- provar isolamento de memória;
- provar que a experiência não força handoffs desnecessários;
- testar recuperação/restart sem cruzar autoridade;
- decidir topologia de deploy/repo.

## Fine-tuning rule

Fine-tuning pode melhorar comportamento, voz e resistência a role drift.

Não pode ser a boundary de segurança.

Ordem esperada:

```text
runtime capability isolation
→ policy/authorization
→ handoff contract
→ adversarial eval
→ behavior training/fine-tuning quando necessário
```

## Decision reset

```yaml
decision: NOT_SELECTED
status: DECISION_RESET
required_property: strong_cross_agent_isolation
naia_memory_authority: separate
anna_memory_authority: separate
apollo_memory_authority: separate_when_implemented
cross_agent_topology: TBD
handoff_mechanism: TBD
```

## Acceptance evidence required

- [ ] tool isolation test
- [ ] memory isolation test
- [ ] cross-domain leakage test
- [ ] minimal-disclosure handoff test
- [ ] explicit-consent test for sensitive handoff
- [ ] restart/recovery authority test
- [ ] role-drift adversarial suite


## System-level architecture/chassis re-screen — 2026-09-30

The product composition decision remains `NOT_SELECTED`, but the current evaluation scope is broader than the old NAIA base screen. The system-level re-screen compares the total Atento composition for NAIA, Anna, and future Apollo. Apollo's domain boundary must be supported now; Apollo-specific functional chassis research remains `DEFERRED`.

Canonical evidence/method record:

`docs/evaluation/atento-system-architecture-chassis-rescreen-2026-09-30.md`

The metric is the lowest defensible total adaptation and ongoing-maintenance cost for the complete product composition. The alternatives remain open: one multi-agent platform, separate specialist chassis behind explicit Atento control/handoff, or a hybrid. No topology is accepted by this note.

The former NAIA Gate-1 and Top 5 remain valid only as NAIA-role evidence. They do not qualify or rank the overall Atento system. The earlier two-agent diagram in this ADR is historical/incomplete because it omits Apollo; it is not the current target architecture.

System-level hard requirements include separate role chat/session, memory, credentials, tool authority and background authority; explicit minimal/auditable handoffs; and receiver-side authorization. Shared infrastructure does not imply shared private data.

```yaml
system_chassis_decision: NOT_SELECTED
system_chassis_shortlist: NOT_SELECTED
first_metric: total_adaptation_and_ongoing_maintenance_cost
architecture_alternatives: [integrated_multi_agent, composed_specialist_chassis, hybrid]
apollo_functional_chassis_research: DEFERRED
```

## Architecture selection update — 2026-10-03

Following the product owner's instruction to choose a chassis, select **NanoClaw as the reference runtime chassis for the Atento three-role composition**. Run NAIA, Anna, and Apollo as separate role groups with private state and grants; all cross-role work must pass through an Atento-owned, typed handoff boundary with receiver-side authorization. NanoClaw is selected as the implementation baseline because it is the only current system candidate with a direct Atento profile-derived three-role probe, and an earlier bounded probe at that exact pin passed eight assertions (`37096864526`), before the current overlay-install workflow; it does not qualify the overlay composition. MindRoom cannot yet bind to an Atento host adapter, and the other screened candidates lack comparable three-role Atento evidence or have a blocker at the inspected pin.

This is an architecture choice for the reference implementation and next qualification cycle, not a claim that NanoClaw has passed the complete system gate, won a comparable total-cost study, or is approved for production. The probe used an incomplete candidate overlay recipe and did not establish the real Atento host, full provider/channel wiring, host-process restart, real task fire/retry/terminal delivery, or approved recovery objectives. The drafted host contract remains unimplemented; RTO/RPO remain unset. No test result is upgraded by this decision.

```yaml
system_chassis_decision: SELECTED_FOR_REFERENCE_IMPLEMENTATION
system_chassis: NanoClaw
tested_candidate_pin: 6906434bcb13eaeca1a6d8b461a1f2c22e53359f
role_topology: three_isolated_role_groups
cross_role_boundary: atento_typed_handoff_with_receiver_authorization
system_gate: NOT_PASSED
production_eligibility: BLOCKED_UNRESOLVED
total_cost_comparison: NOT_MEASURED
RTO: TBD
RPO: TBD
```

The hard gates remain release conditions: install and verify all profile overlays at the frozen pin; bind the candidate to the real Atento host contract; test identity, cross-role memory/tool/credential denial, handoff reauthorization, whole-host restart, role-preserving scheduled/retry/recovery execution and terminal delivery; set and meet product RTO/RPO; then measure the comparable cost vector. If NanoClaw cannot satisfy those conditions within the predeclared adaptation boundary, reopen this choice and resume the unresolved cohort.

This update supersedes the earlier `system_chassis_decision: NOT_SELECTED` as the **reference-implementation choice only**. The production eligibility and comparative-cost decisions remain open.
