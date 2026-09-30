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
| **OpenClaw** `ca8f24d...` | historical Atento evidence | historical Atento evidence | historical Atento evidence | historical Atento evidence | historical Atento evidence | historical Atento evidence | historical Atento evidence | `REQUIRES_DELTA_AUDIT`: current head is 67 commits ahead of the qualified pin and touches memory, CUA/computer-use, device/gateway/channel-boundary surfaces |
| **OpenMausBot** `6005b1b...` | historical Atento evidence | historical evidence + current memory/session changes | historical evidence | historical evidence | historical evidence | historical evidence + ChatGPT-plan additions | historical evidence + current auth/policy changes | `REQUIRES_DELTA_AUDIT`: current head is 11 commits ahead of the original qualification and contains material memory/session/auth changes |
| **QwenPaw** `7774417...` | `ESTABLISHED_DOCS` | `ESTABLISHED_DOCS`; three-layer memory | `ESTABLISHED_DOCS`; cron/scheduled tasks | `ESTABLISHED_DOCS`; multiple IM channels + console/TUI/desktop | browser documented; computer-use source/approval/runtime files exist, while upstream feature table still marks computer-use in progress | `ESTABLISHED_DOCS`; local runtime/Ollama/LM Studio + cloud providers | `ESTABLISHED_SOURCE`; sandbox, tool/file guards, access policy and computer-use approval surfaces present | comparable product; `REQUIRES_RUNTIME_AUDIT`, especially computer-use and effective authority policy |
| **AI Butler** `c35d3af...` | `ESTABLISHED_DOCS`; upstream calls v0.1 public beta | `ESTABLISHED_SOURCE`; extensive memory code/tests/migrations | `ESTABLISHED_DOCS`; persistent scheduler marked ready | webchat/terminal ready; many additional channels explicitly beta | file/shell/git and OS scripting documented ready; browser implementation/tests exist | Claude/Ollama documented ready; several other providers beta | `ESTABLISHED_SOURCE`; permissions/auth/security surfaces and tests exist | comparable product; `REQUIRES_RUNTIME_AUDIT`; preserve ready-vs-beta distinctions |
| **NanoClaw** `4c1eabd...` | `ESTABLISHED_DOCS` | `ESTABLISHED_DOCS`; per-agent/group memory | `ESTABLISHED_DOCS`; scheduled tasks | multi-channel capability installed through skills | agent tool surface/container runtime established in source; general computer-use is not claimed here | Claude native path; Codex/OpenCode/Ollama provider modules installed through skills | container isolation + credential gateway documented; credential/provider isolation tests exist in skills | comparable product; `REQUIRES_RUNTIME_AUDIT` and adaptation-surface audit because capabilities are materialized into the fork via skills |
| **TrustClaw** `c07410b...` | `ESTABLISHED_DOCS`; web + Telegram | `ESTABLISHED_SOURCE`; memory save/search/flush surfaces | `ESTABLISHED_SOURCE`; cron routes/tools/settings | web + Telegram | 1000+ Composio-connected actions documented; no local browser/computer control established | model configuration exists, but provider replaceability is not established by this audit | cloud sandbox and OAuth-connected-account boundary documented | comparable personal-assistant product; `REQUIRES_RUNTIME_AUDIT`; external platform/deployment/cost boundaries are material |
| **Open Assistant** `32c55d2...` | `ESTABLISHED_DOCS`; single-container assistant | `ESTABLISHED_SOURCE`; memory repo/service/model | `ESTABLISHED_SOURCE`; cron repo/service/API/tests | web + WhatsApp + Slack documented | Playwright browser and email/calendar integrations have implementation/tests | OpenRouter/Anthropic/Groq/Ollama/vLLM documented | tool registry/executor and auth surfaces present; sandbox equivalence not established | comparable technical product; `LEGAL_ADOPTION_REVIEW` (BSL 1.1) + `REQUIRES_RUNTIME_AUDIT` |

No row above is a rank or selection.

---

## 3. Historical-pin transfer audit

### OpenClaw

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

At pin `32c55d2643f9fe38777f9212588b2eee45392514`:

Source tree establishes implementation surfaces for:

- memory;
- cron jobs with execution locks;
- tool registry/executor;
- browser;
- Outlook/calendar;
- credentials/auth.

Upstream documentation describes WhatsApp/Slack, email/calendar and local providers.

The repository `LICENSE` is Business Source License 1.1.

Classification:

```text
PRODUCT_COMPARABLE = YES
TECHNICAL_AUDIT_ALLOWED = YES
PRODUCT_ADOPTION_CLEARED = NO
LEGAL_ADOPTION_REVIEW = REQUIRED
RUNTIME_TRANSFER_TO_NAIA = NOT_ESTABLISHED
```

---

## 5. Smallest next evidence

The next block is **not** a seven-way benchmark.

Run only decision-relevant audits:

1. OpenClaw — targeted delta inspection of contracts touched since the old qualified pin.
2. OpenMausBot — targeted delta inspection of memory/session/auth/policy changes.
3. QwenPaw — minimal runtime proof for persistence + policy + browser/computer boundary.
4. AI Butler — minimal runtime proof restricted to features marked ready, plus restart/session ownership.
5. NanoClaw — measure actual files/touchpoints required to compose NAIA-relevant provider/channel/tool capabilities from skills.
6. TrustClaw — characterize dependency/cost/deployment boundary and prove one scheduled external action + memory continuity.
7. Open Assistant — legal terms first for adoption; technical runtime audit remains evidence-only until cleared.

Discovery pool (`SelfAgent`, `goclaw`, `nebo-go`) remains unaudited, so:

```text
CANDIDATE_UNIVERSE_COMPLETE = false
NAIA_SHORTLIST = NOT_SELECTED
```

## 6. Outcome

```text
NAIA_COMPARABLE_PRODUCTS_IDENTIFIED = 7
CURRENT_PIN_QUALIFIED = 0
HISTORICAL_EVIDENCE_REUSABLE = [OpenClaw, OpenMausBot]
NEW_STATIC_PRODUCT_AUDITS = [QwenPaw, AI Butler, NanoClaw, TrustClaw, Open Assistant]
SHORTLIST = NOT_SELECTED
WINNER = NOT_SELECTED
NEXT_BLOCK = TARGETED_MISSING_DELTA_AUDITS
```
