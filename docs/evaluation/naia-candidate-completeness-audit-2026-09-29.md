# NAIA candidate completeness audit — 2026-09-29

## Contract

This record audits **product comparability and missing evidence**, not quality ranking.

It does not create a shortlist, winner, execution priority or runtime promotion.

```text
COMPARABLE_PRODUCT != QUALIFIED
STATIC_SOURCE_PRESENT != RUNTIME_PASS
HISTORICAL_EVIDENCE != CURRENT_PIN_PROOF
TECHNICAL_FIT != LEGAL_ADOPTION_CLEARED
```

Current authority remains:

```yaml
NAIA_BASE: NOT_SELECTED
NAIA_SHORTLIST: NOT_SELECTED
candidate_universe_complete: false
```

## Evidence vocabulary

- `ESTABLISHED_DOCS` — explicitly documented by the pinned upstream.
- `ESTABLISHED_SOURCE` — implementation/test surface is present at the pinned source tree; runtime behavior is not inferred.
- `PARTIAL` — the capability exists with a material limitation or incomplete status.
- `NOT_ESTABLISHED` — no transferable proof is claimed.
- `REQUIRES_DELTA_AUDIT` — historical Atento evidence exists, but the current pin contains material changes.
- `REQUIRES_RUNTIME_AUDIT` — source/docs establish the intended mechanism but runtime behavior remains unobserved by Atento.
- `LEGAL_ADOPTION_REVIEW` — technical research may continue, but product adoption is not cleared by this record.

---

## 1. Same-protocol completeness gate

A comparable NAIA chassis must plausibly provide an end-to-end personal-assistant runtime with:

1. persistent state or memory;
2. scheduled/background work;
3. practical user interaction surface;
4. external tools/actions;
5. model/provider path;
6. operational security/authority boundary;
7. maintainable deployment/adaptation surface.

Browser/computer use is measured separately because the NAIA target includes it, but lack of full computer-use does not silently become a failed runtime claim; it is recorded as a product delta.

## 2. Candidate evidence matrix

| Candidate | Assistant runtime | Persistence / memory | Scheduled/background | Interaction/channels | Browser/computer / external actions | Model/provider | Authority/security | Current audit disposition |
|---|---|---|---|---|---|---|---|---|
| **OpenClaw** `ca8f24d...` | historical Atento evidence | historical evidence + stronger memory sanitization | historical Atento evidence | historical channel evidence + stronger interaction boundaries | historical CUA/browser surface + stronger ownership ambiguity handling | historical Atento evidence | historical approval evidence + stronger gateway/channel boundary tests | `DELTA_STATIC_AUDIT_COMPLETE`; current-pin hardening/runtime probe remains pending only if decision-relevant |
| **OpenMausBot** `6005b1b...` | historical Atento evidence | historical evidence + current lending-memory hardening | historical evidence | historical evidence | historical evidence + stronger lending-memory gate | historical evidence + ChatGPT-plan additions | current request-auth/lending contracts audited statically | `DELTA_STATIC_AUDIT_COMPLETE`; targeted current-pin runtime tests remain pending |
| **QwenPaw** `7774417...` | complete assistant product surface | strong per-Agent memory/workspace model | cron/scheduled tasks present | multiple IM channels + console/TUI/desktop | browser + beta Windows/macOS Computer Use present | local + cloud providers | strong policy primitives, but sandbox default/fallback and cron safety defaults require hardening | `STATIC_CONTRACT_AUDIT_COMPLETE`; hardened runtime profile required before qualification |
| **AI Butler** `c35d3af...` | complete self-hosted assistant surface | strong per-profile memory banks | persistent scheduler + mission engine | webchat/terminal ready; 10 additional channels beta | browser + OS scripting present; Windows Tier 3/4 real desktop validation pending | Claude/Ollama ready upstream; other providers mixed | fail-closed shell allowlist, capability gates, default-deny credential broker | `STATIC_CONTRACT_AUDIT_COMPLETE`; targeted runtime validation still required |
| **NanoClaw** `4c1eabd...` | complete containerized assistant surface | per-agent/group workspace + memory | scheduled tasks | channels installed through skills | container/browser/tool surface; no generic desktop CUA claim | provider paths installed/composed through skills | strong container + credential-gateway model | `CHANGE_SURFACE_AUDIT_COMPLETE`; total migration cost is profile-dependent; current Ollama skill requires rederivation at pin |
| **TrustClaw** `c07410b...` | complete web/Telegram assistant surface | instance-scoped pgvector memory | persistent cron + fencing/auth | web + Telegram | Composio-managed external action surface; no local generic CUA | cloud/provider-routed models + external embeddings | user-scoped Composio session, but local per-action approval not established | `STATIC_CONTRACT_AUDIT_COMPLETE`; composed Composio/Vercel authority/cost runtime audit required |
| **Open Assistant** `32c55d2...` | `ESTABLISHED_DOCS`; single-container assistant | `ESTABLISHED_SOURCE`; memory repo/service/model | `ESTABLISHED_SOURCE`; cron repo/service/API/tests | web + WhatsApp + Slack documented | Playwright browser and email/calendar integrations have implementation/tests | OpenRouter/Anthropic/Groq/Ollama/vLLM documented | tool registry/executor and auth surfaces present; sandbox equivalence not established | comparable technical product; `LEGAL_ADOPTION_REVIEW` (BSL 1.1) + `REQUIRES_RUNTIME_AUDIT` |

No row above is a rank or selection.

---

## 3. Historical-pin transfer audit

### OpenClaw

Detailed current-pin delta evidence:

`docs/evaluation/openclaw-current-delta-audit-2026-09-29.md`

Atento qualified:

`e9571d77e76bd6d35996273d9e8398ad539b26e1`

Current observed upstream:

`ca8f24d05fc49a224adab0c9426077fd8d93801d`

Git comparison:

```text
ahead = 67 commits
behind = 0
```

The delta is not merely UI/release noise. Visible changed surfaces include, among others:

- `extensions/memory-lancedb/*`;
- `extensions/cua-computer/*`;
- `extensions/device-pair/*`;
- Gateway/connection surfaces in native apps;
- channel interaction-boundary tests;
- cron/gateway ownership tests.

Therefore:

```text
OPENCLAW_HISTORICAL_EVIDENCE = REUSABLE
OPENCLAW_CURRENT_PIN_TRANSFER = NOT_YET_ESTABLISHED
NEXT = TARGETED_DELTA_AUDIT
```

Do not rerun unchanged historical restart/approval/channel evidence unless the delta touches the relevant contract.

### OpenMausBot

Detailed current-pin delta evidence:

`docs/evaluation/openmaus-current-delta-audit-2026-09-29.md`

Atento original qualification:

`947bef311bf5c3f55d3590849abf0eb329408519`

Current observed upstream:

`6005b1bf5883a7ffa639c07e729321f89b9532e1`

Git comparison:

```text
ahead = 11 commits
behind = 0
```

Material changed surfaces include:

- `server/lending-memory.ts` + tests;
- `server/memory-upkeep.ts` + tests;
- `server/sessions.ts` + tests;
- `server/request-auth.ts` + tests;
- managed-policy tests;
- cloud-home / workspace;
- ChatGPT-plan auth/driver/config paths.

Therefore:

```text
OPENMAUS_HISTORICAL_EVIDENCE = REUSABLE
OPENMAUS_CURRENT_PIN_TRANSFER = NOT_YET_ESTABLISHED
NEXT = TARGETED_DELTA_AUDIT
```

---

## 4. New-candidate static findings

### QwenPaw

Detailed operational-contract audit:

`docs/evaluation/qwenpaw-contract-audit-2026-09-29.md`

At pin `777441721aa72db8e380d90e4d0481b05cbfd4cc`:

Primary upstream documentation describes:

- three-layer memory;
- scheduled tasks / Cron;
- multi-channel operation;
- local model runtime plus Ollama/LM Studio and cloud providers;
- browser-use;
- sandbox/tool/file/access-policy controls.

The source tree also contains concrete computer-use runtime, Windows/macOS platform handlers and approval components.

However, the upstream feature table still labels computer-use as in progress.

Classification:

```text
PRODUCT_COMPARABLE = YES
COMPUTER_USE_SOURCE_PRESENT = YES
COMPUTER_USE_RUNTIME_PROOF = NOT_ESTABLISHED
EFFECTIVE_POLICY_RUNTIME = NOT_ESTABLISHED
```

### AI Butler

Detailed operational-contract audit:

`docs/evaluation/aibutler-contract-audit-2026-09-29.md`

At pin `c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c`:

Upstream explicitly labels the project public beta and distinguishes ready vs beta features.

Static source evidence includes:

- memory implementations, migrations and isolation tests;
- scheduling documentation;
- channel implementations/tests;
- browser implementation/tests;
- permissions/authentication;
- tool/MCP boundaries.

Classification:

```text
PRODUCT_COMPARABLE = YES
CORE_IMPLEMENTATION_SURFACE = ESTABLISHED_SOURCE
READY_BETA_BOUNDARY = MATERIAL
RUNTIME_TRANSFER_TO_NAIA = NOT_ESTABLISHED
```

Claims about upstream test counts remain upstream claims unless independently executed.

### NanoClaw

Detailed adaptation/change-surface audit:

`docs/evaluation/nanoclaw-change-surface-audit-2026-09-29.md`

At pin `4c1eabd3ddd74cc3d71b1871da857391a9411c8d`:

The product deliberately uses a core + installable-skill composition model. Channel/provider skills can copy modules into the user's fork.

Source evidence includes:

- scheduled-task machinery;
- provider contracts;
- Codex/OpenCode/Ollama skills;
- credential-gateway/credential-isolation tests;
- channel management skills.

Classification:

```text
PRODUCT_COMPARABLE = YES
SECURITY_MODEL = CONTAINER + CREDENTIAL_GATEWAY
EXTENSION_MODEL = SKILL_MATERIALIZES_CODE_IN_FORK
UPSTREAM_SYNC_COST = NOT_MEASURED
RUNTIME_TRANSFER_TO_NAIA = NOT_ESTABLISHED
```

The extension model is a change-surface question, not an automatic rejection.

### TrustClaw

Detailed operational-contract audit:

`docs/evaluation/trustclaw-contract-audit-2026-09-29.md`

At pin `c07410bccb916236b45b563e8c4ff76ad83d3855`:

Source evidence includes:

- memory save/search/flush;
- cron scheduling;
- OAuth/auth integration routes;
- toolkits and tool invocation UI;
- Telegram configuration.

Upstream documents 1000+ Composio tool integrations and remote sandbox execution.

Classification:

```text
PRODUCT_COMPARABLE = YES
GENERAL_EXTERNAL_ACTION_SURFACE = ESTABLISHED_DOCS
LOCAL_BROWSER_COMPUTER_USE = NOT_ESTABLISHED
COMPOSIO_DEPENDENCY = MATERIAL
VERCEL_CRON_DEPLOYMENT_LIMITS = MATERIAL_FOR_SOME_DEPLOYMENTS
RUNTIME_TRANSFER_TO_NAIA = NOT_ESTABLISHED
```

### Open Assistant

Detailed exact-pin audit:

docs/evaluation/open-assistant-contract-audit-2026-09-29.md

At pin 32c55d2643f9fe38777f9212588b2eee45392514:

Established static contracts include:

- persistent conversation-scoped memory;
- persisted cron jobs reloaded at scheduler startup;
- execution history and instance locking;
- skill/service tool filtering;
- real Playwright browser automation;
- encrypted credential storage;
- OpenRouter/Anthropic/Groq/Ollama/vLLM provider paths.

Material boundaries include:

- no independent repository-owned per-action approval/deny policy established;
- multi-step planning can expand to all enabled skills;
- no separate technical capability subset for background jobs established;
- credentials are stored globally by service_name rather than agent/user identity;
- strict NAIA/Anna memory/tool/credential isolation is not established;
- browser network/URL authority needs hardening;
- desktop computer-use is not established;
- exact-pin hosted execution is not observed.

The repository LICENSE is Business Source License 1.1. Technical audit and product-adoption authority remain separate.

Classification:

~~~text
OPEN_ASSISTANT_STATIC_CONTRACT_AUDIT = COMPLETE
OPEN_ASSISTANT_STATIC_RESULT = PASS_WITH_SCOPE
OPEN_ASSISTANT_PRODUCT_COMPARABLE = YES
OPEN_ASSISTANT_CURRENT_PIN_QUALIFIED = NO
LEGAL_ADOPTION_CLEARED = NO
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
~~~

---

## 5. Smallest next evidence

The first seven-candidate static/completeness block is complete **only for that original audited subset**.

The candidate universe has since expanded materially. See:

- `docs/evaluation/naia-persistent-agent-discovery-2026-09-29.md`
- `docs/evaluation/naia-external-evidence-preflight-2026-09-29.md`

The common NCP profile remains canonical for later local-delta work:

`docs/evaluation/naia-common-probe-profile-2026-09-29.md`

But local NCP execution is not the next phase.

Required order:

~~~text
expanded candidate discovery
→ exact-pin admission/completeness audit
→ upstream tests/evals/run-artifact inventory
→ transfer/relevance classification
→ identify remaining material Atento delta
→ only then execute the smallest NCP sub-check
~~~

The previously audited seven retain their evidence. Do not redo OpenClaw/OpenMausBot/QwenPaw/AI Butler/NanoClaw/TrustClaw/Open Assistant merely because the universe expanded.

For technical discovery, license is not used as an exclusion or ordering criterion.

~~~text
ORIGINAL_AUDITED_SET_STATIC_BLOCK = COMPLETE
EXPANDED_CANDIDATE_UNIVERSE = OPEN
CANDIDATE_UNIVERSE_COMPLETE = false
LOCAL_COMMON_PROBE_PHASE = NOT_STARTED
NAIA_SHORTLIST = NOT_SELECTED
~~~

## 6. Outcome

~~~text
ORIGINAL_AUDITED_COMPARABLE_PRODUCTS = 7
EXPANDED_COMPARABLE_OR_PROVISIONAL_PRODUCTS > 7
CURRENT_PIN_QUALIFIED = 0
HISTORICAL_EVIDENCE_REUSABLE = [OpenClaw, OpenMausBot]
STATIC_PRODUCT_AUDITS_COMPLETE = [QwenPaw, AI Butler, NanoClaw, TrustClaw, Open Assistant]
OPEN_ASSISTANT_STATIC_RESULT = PASS_WITH_SCOPE
OPEN_ASSISTANT_CURRENT_PIN_QUALIFIED = NO
SHORTLIST = NOT_SELECTED
WINNER = NOT_SELECTED
NEXT_BLOCK = EXPANDED_CANDIDATE_ADMISSION_AND_EXTERNAL_EVIDENCE_PREFLIGHT
~~~
