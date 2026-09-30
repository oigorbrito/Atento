# NAIA / Anna candidate re-enumeration — 2026-09-29

## Contract

This is the first candidate-universe rebuild after the product/decision reset.

It does **not** select a winner, create a shortlist, authorize execution priority, or promote a runtime.

Rules:

```text
ENUMERATED != QUALIFIED
QUALIFIED != SHORTLISTED
SHORTLISTED != SELECTED
EXTERNAL_SIGNAL != LOCAL_PROOF
TECHNICAL_CANDIDATE != LEGAL_ADOPTION_CLEARED
```

The purpose of this block is only to:

1. identify systems that are plausibly comparable to the current NAIA or Anna product roles;
2. pin each newly admitted source;
3. classify obvious non-equivalent sources before benchmark work;
4. map existing Atento evidence so it is reused rather than rerun;
5. identify the smallest missing material audit for the next block.

```yaml
NAIA_BASE: NOT_SELECTED
NAIA_SHORTLIST: NOT_SELECTED
ANNA_BASE: NOT_SELECTED
ANNA_SHORTLIST: NOT_SELECTED
APOLLO: DEFERRED
candidate_universe_complete: false
```

---

## 1. NAIA — persistent personal assistant universe

Admission target:

A NAIA base candidate should already operate as a persistent personal assistant rather than only an agent framework or isolated component. Material surfaces include persistent state/memory, user-facing runtime, tools/actions, model/provider routing, background/scheduled work, and at least one practical interaction surface beyond a toy CLI.

### Initial comparable set

| Source | Current pin | Class | Why it enters enumeration | Current evidence state |
|---|---|---|---|---|
| OpenClaw — `openclaw/openclaw` | `ca8f24d05fc49a224adab0c9426077fd8d93801d` | `PERSISTENT_ASSISTANT_BASE_CANDIDATE` | mature personal-assistant product; channels, persistent state, restart/recovery, tools/plugins, provider/model seams | substantial historical Atento qualification exists at older pin; **repin delta required, not full rerun** |
| OpenMausBot — `milind-soni/OpenMausBot` | `6005b1bf5883a7ffa639c07e729321f89b9532e1` | `PERSISTENT_ASSISTANT_BASE_CANDIDATE` | persistent assistant surface with routines, computer/browser/apps, model/provider switching and memory | substantial historical Atento evidence exists at older pin; **repin delta required** |
| QwenPaw — `agentscope-ai/QwenPaw` | `777441721aa72db8e380d90e4d0481b05cbfd4cc` | `PERSISTENT_ASSISTANT_BASE_CANDIDATE` | personal assistant with multi-channel chat, independent-agent memory/skills, scheduled execution, local models and tool/file protections | **new candidate; audit required** |
| AI Butler — `LumabyteCo/aibutler` | `c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c` | `PERSISTENT_ASSISTANT_BASE_CANDIDATE` | self-hosted assistant with memory, scheduler, agent loop, MCP, OS actions and persistent mission engine | **new candidate; public-beta maturity caveat; audit required** |
| NanoClaw — `nanocoai/nanoclaw` | `4c1eabd3ddd74cc3d71b1871da857391a9411c8d` | `PERSISTENT_ASSISTANT_BASE_CANDIDATE` | assistant with container isolation, messaging surfaces, memory and scheduled jobs | **new candidate; provider/runtime breadth and total product completeness require audit** |
| TrustClaw — `ComposioHQ/trustclaw` | `c07410bccb916236b45b563e8c4ff76ad83d3855` | `PERSISTENT_ASSISTANT_BASE_CANDIDATE` | 24/7 personal assistant, vector memory, web/Telegram, recurring work and broad external tool surface | **new candidate; Composio/Vercel dependency and self-hosting boundaries require audit** |
| Open Assistant — `open-assistant-org/open-assistant` | `32c55d2643f9fe38777f9212588b2eee45392514` | `PERSISTENT_ASSISTANT_BASE_CANDIDATE` | assistant surface covering personal tools, connectors, persistent artifacts, recurring work and messaging | **new technical candidate; BSL 1.1 terms materially constrain adoption** |

### Historical NaIa implementation

`oigorbrito/NaIa` remains valuable evidence for:

- explicit policy/approval contracts;
- audit/evidence;
- sensitive-memory consent;
- provider-neutral ports;
- operation/idempotency research.

It is **not automatically admitted as a directly comparable mature product base** merely because it was historically called a base candidate.

Current treatment:

```text
HISTORICAL_NAIA_IMPLEMENTATION = MECHANISM/ARCHITECTURE_DONOR
DIRECT_PRODUCT_BASE_COMPARABILITY = REQUIRES_REAUDIT
```

### Persistent-agent discovery expansion

The initial seven-candidate set was not exhaustive.

Detailed discovery record:

`docs/evaluation/naia-persistent-agent-discovery-2026-09-29.md`

External-evidence preflight:

`docs/evaluation/naia-external-evidence-preflight-2026-09-29.md`

Current product-shape references include **Grok Bot** and **Meta Muse**: persistent named agents, long-lived computer/browser state, proactive/scheduled work and explicit human-control boundaries. They are references, not source candidates.

New high-relevance technical candidates requiring same-protocol admission/completeness audit:

| Source | Observed pin | Discovery class | Why it remains in the universe |
|---|---|---|---|
| Rakazo — `elie222/rakazo` | `f4583525d632fcd8643fd6e24c7f51e3e04cb990` | `PERSISTENT_ASSISTANT_BASE_CANDIDATE` | direct Grok-Bot-class product: persistent bots, routines, private/team computers, browser/terminal/desktop, delegation and approvals |
| Gobii — `gobii-ai/gobii-platform` | `c9929bf8ea59b4695b99dcab59aa6c97a09c5bdb` | `PERSISTENT_AGENT_BASE_CANDIDATE` | durable always-on employees, event queues, schedules, browser, channels, approvals and a first-class eval suite |
| Octop — `TencentCloud/Octop` | `e473dd3c4a4741618ffde1a42a3492341a189e8e` | `PERSISTENT_ASSISTANT_BASE_CANDIDATE` | self-hosted multi-user/multi-agent assistant with cron, browser, remote desktop, memory, channels and approvals |
| PersonalJarvis — `PersonalJarvis/PersonalJarvis` | `1be33c457739ca7e161ee6fbaf298ec10d4dad3b` | `PERSISTENT_ASSISTANT_BASE_CANDIDATE` | routines, persistent state, browser, native computer-use, recovery and explicit OS-contract evidence |
| Letta Code — `letta-ai/letta-code` | `21daa38a8cdd74f2d03b634c8312253080bacfc1` | `PERSISTENT_AGENT_RUNTIME_CANDIDATE` | long-lived identity/memory, proactive crons, channels, approvals, remote computers and cross-agent calls |
| Kortix/Suna — `kortix-ai/suna` | `270c4a57c8ae5ffb85eff6d5b9700c5713612f28` | `PERSISTENT_AGENT_PLATFORM_CANDIDATE` | agents + triggers + secrets + connectors + sandbox/session runtime with exact-SHA release gates |
| Rome — `rome-os/rome` | `ef523c4659149e2711744deb04ec42c3be339907` | `PERSISTENT_AGENT_BASE_CANDIDATE` | direct Grok Bot/Muse-class alternative with persistent agents, routines, memory, actions/apps and approvals |
| Agent Zero — `agent0ai/agent-zero` | `e3051fb584b1a36be2b0a0c90606f1c2c2d356ec` | `PRODUCT_RUNTIME_BOUNDARY_CANDIDATE` | full computer/browser, persistent memory, scheduler and project-scoped runtime; framework-vs-product boundary must be audited |
| OpenGrokBot — `wolfqing/OpenGrokBot` | `43ba51fc0487b7adbb23861a1062a113390833d9` | `PERSISTENT_ASSISTANT_BASE_CANDIDATE` | isolated computer per bot, persistent sessions, routines, approvals and allowlisted handoffs |
| SelfAgent — `oezercet/SelfAgent` | `c86b0b1fbc0e177e67b59b8d26cc2ce9c18406d1` | `PROVISIONAL_BASE_CANDIDATE` | persistent memory/tasks, browser, scheduler, email/system tools and product UI |
| GoClaw — `sausheong/goclaw` | `c24c50ba2d16daff6aa2809b6c1a6f592977ae54` | `PROVISIONAL_BASE_CANDIDATE` | persistent memory/session state, heartbeat, cron, channels, policy and multi-agent runtime |
| Nebo — `NeboLoop/nebo-go` | `d566d27ec7c5ab36f3b95fdfda371bb45994dfd7` | `PROVISIONAL_BASE_CANDIDATE` | desktop companion, persistent memory, browser/shell and scheduling |

Secondary discovery remains open for systems including AutoMate, Agent OS, OpenAgent, Open Intern, HubOS, Engram, Holt and RustFox.

For this technical discovery phase:

```text
LICENSE_FILTER_FOR_TECHNICAL_DISCOVERY = DISABLED
CANDIDATE_UNIVERSE_COMPLETE = false
LOCAL_COMMON_PROBE_PHASE = NOT_STARTED
```

Do not start a local benchmark merely because the previous seven-candidate static block was complete. First reconcile upstream tests/evals and determine the material Atento delta for the expanded set.

---

## 2. Anna — emotional / therapeutic agent universe

Admission target:

A complete Anna base should provide an end-to-end emotional/therapeutic interaction runtime with longitudinal state or memory, strategy/intervention behavior, role/safety boundaries and a user-facing or executable counseling flow. Models, datasets, RAG-only projects and evaluation frameworks do not qualify merely because they are mental-health related.

### Initial set

> The Anna completeness audit supersedes the provisional class labels in the first enumeration where source/runtime inspection established non-equivalence. See `docs/evaluation/anna-candidate-completeness-audit-2026-09-29.md`.

| Source | Current pin | Class | Why it enters enumeration | Current evidence state |
|---|---|---|---|---|
| PsychAgent — `ECNU-ICALK/PsychAgent` | `469f45ef468b968b3fccd1936d7e6a0a574e4c5c` | `THERAPEUTIC_BASE_CANDIDATE` | runnable multi-session counseling generation + web workspace, longitudinal memory/planning, skill retrieval and multiple therapy schools | existing Atento evidence reusable; full post-session evolution assets absent; repository license still unresolved |
| TherapyMind — `zx070326-hash/TherapyMind` | `bfed3f5be61bab262bb00a0f3cc9718c4a965243` | `MECHANISM_DONOR` | modular counseling agent with session lifecycle, persistence/recovery, safety layers and internal review chain | existing evidence reusable; runtime completeness and external terms require audit |
| TheraMind — `Emo-gml/TheraMind` | `416d0a00ecc8c76229512197765dc95be6513de5` | `MECHANISM_DONOR` | executable therapist/patient longitudinal loop with adaptive therapy selection and multi-session planning | existing evidence reusable; research/educational terms block ordinary product adoption |
| OpenCouch — `whanyu1212/OpenCouch` | `ac5af6ee4c9a06b4050c5a912439f343ade2c35c` | `THERAPEUTIC_BASE_CANDIDATE` **pending domain-fit audit** | persistent emotional-support product with Postgres state/memory, safety routing, crisis audit, guided multi-turn exercises and observable runtime | **new candidate; pre-beta; must test whether wellness/support scope adequately maps to Anna target** |
| Inner Dialogue — `ataglianetti/inner-dialogue` | `ffc9e8f78d0f15a8d720436f92fb6e0887fe7461` | `MECHANISM_DONOR` | persistent local therapy toolkit with session files, multiple modalities, update/doctor tooling and safety framework | **new source; must determine whether it is a complete chassis or a Claude/tooling-dependent mechanism package** |
| PsyChat — `wink-wink-wink555/PsyChat` | `5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4` | `MECHANISM_DONOR` | existing therapeutic project with Agentic RAG and prototype runtime | historical Atento evidence is heavily RAG/adaptation-centric; complete Anna-base status remains unproven |
| `matteodante/therapist` | `dd9848fe9662ee6ea7f44f1795fe1d6b8114a47d` | `MECHANISM_DONOR / DOMAIN_ADJACENT` | strong local encrypted longitudinal memory, atomic state commit and explicit intervention records | project explicitly scopes itself to self-reflection / not therapy; do not compare as full Anna base without a role-contract change |

### Sources that remain non-base by category

Still do **not** place these directly into the Anna base comparison:

- SoulChat / PsyDT — model/checkpoint/training source;
- EmoLLM — model/training/deployment donor;
- MindChat — model/checkpoint/deployment donor;
- PsychEval — benchmark/evaluation source;
- MentalHealthBench — benchmark/evaluation source;
- CounselBench — benchmark/evaluation source;
- PATIENT-Ψ — patient-style evaluation source;
- MHSafeEval — safety evaluation source;
- ENPMR-Bench — memory evaluation source;
- ESConv — strategy taxonomy/benchmark;
- AgentMental — mechanism/evaluation reference.

---

## 3. Evidence reuse / smallest next audit

Do not rerun broad tests already established at an unchanged pin.

### NAIA

For OpenClaw and OpenMausBot:

1. diff old qualified pin → current pin;
2. inspect only material changes touching persistence, memory, tools, authority, background work, channels, restart/recovery or product integration;
3. carry forward unaffected evidence explicitly;
4. run a local delta only when transfer is not defensible.

For the previously admitted candidates and the new persistent-agent expansion:

1. establish runtime/product completeness at an exact pin;
2. locate directly relevant upstream tests/evals and available run artifacts;
3. map NAIA target capabilities;
4. classify authority/security model;
5. identify memory ownership and restart behavior;
6. measure provider/tool/channel coupling;
7. estimate adaptation surface before any behavioral benchmark;
8. run a local test only for a material Atento delta or blocking unproven invariant.

License is not used as a technical discovery/admission filter in the current phase.

### Anna

For PsychAgent, TherapyMind, TheraMind and PsyChat:

- reuse current pinned Atento evidence first;
- only close the missing chassis-completeness / safety / privacy / pt-BR / legal deltas.

For OpenCouch and Inner Dialogue:

- first establish class equivalence before any head-to-head benchmark.

---

## 4. Explicit non-decisions

This enumeration does **not** imply:

- OpenClaw or OpenMausBot remain finalists;
- QwenPaw is preferred because of popularity;
- AI Butler is mature because it reports many tests;
- NanoClaw is preferable because it is small;
- TrustClaw is preferable because of tool count;
- Open Assistant is legally adoptable;
- PsychAgent is Anna's winner;
- OpenCouch is clinically equivalent to a therapeutic agent;
- Inner Dialogue is a complete chassis;
- PsyChat is excluded permanently.

Current state remains:

```text
NAIA_BASE = NOT_SELECTED
NAIA_SHORTLIST = NOT_SELECTED
ANNA_BASE = NOT_SELECTED
ANNA_SHORTLIST = NOT_SELECTED
APOLLO = DEFERRED
CANDIDATE_UNIVERSE_COMPLETE = false
NEXT_BLOCK = EXPANDED_CANDIDATE_ADMISSION_AND_EXTERNAL_EVIDENCE_PREFLIGHT
```
