# Engram scheduled-only static binding probe — result (2026-09-30)

## Classification

`PASS_WITH_SCOPE` for the pre-registered property `BACKGROUND_AUTHORITY <= INTERACTIVE_AUTHORITY` under the tested composition. This is an empirical runtime result for the exact Engram pin and the deterministic local adapter. It does not qualify the Engram candidate or close `ENGRAM_BROWSER_EFFECT_AUTHORITY`, which remains `STILL_OPEN`.

## Frozen treatment and composition

- Engram pin: `3a43667deec4a680b42f3e880d7d6bac3baf0746` (checkout matched).
- One config treatment: `AgentDef.allowed_tools` exposes only `mcp_atento_browser_scheduled_effect`; same AgentDef and `ENGRAM_HOME` for unattended and attended runs.
- Adapter policy grants scheduled `click` on `https://example.test/form`, selector `#save`; scheduled `type` at `#note` is denied. The interactive MCP identity and native browser click/type are absent from the provider toolset.
- Deterministic OpenAI-compatible provider bound to loopback; no external inference. Fake reversible browser driver; no real browser.

## Observed outcomes

| Path | Scheduled click | Scheduled type | Trusted origin |
|---|---|---|---|
| Real `engramd --run-due` process creating a task from a due scheduler payload | executed | technically denied (`AuthorityDenied`) | `scheduled` |
| Real daemon `POST /v1/tasks/{id}/run` control | executed | technically denied (`AuthorityDenied`) | `scheduled` |

In both paths the model supplied `origin: interactive` in its tool arguments, but the server authority record remained `origin: scheduled`. There were 8 total deterministic local provider calls across both runs. No test credential was observed in logs or receipts.

## Scope and limitations

- The reduced static allowlist makes interactive-only browser `type` unavailable under this AgentDef. This is a composition tradeoff, not proof of full NAIA capability.
- Resident scheduler tick: `NOT_RUN`.
- Real browser: `NOT_RUN`.
- Policy-control failure case: `NOT_RUN`.
- Candidate qualification/promotion or shortlist/base changes: none.
- No other agent/runtime was exercised; NAIA/Anna isolation and cross-agent topology were not changed.

## Artifact integrity

- `receipts.json`: SHA-256 `89deb84f4ec0c74a3ab4b6336084a9fe88a19df15c2834f5d828e2e0d9bdd3d9`
- `summary.txt`: SHA-256 `077f56711e653f19c2561d367dfdc91f6bf7d3335bb73c969f58f54a3d21a93b`
- `run-due.log`: SHA-256 `872a465f0b45ccea714c2f1a73a062b6757760be4911fd3a6443ef387b895e35`
- `attended-daemon.log`: SHA-256 `8746d5dacba25f7aeaa62e89509fc533181e1039ec78f6dbbb73a8094fac0bd1`

The pre-registration is in `naia-engram-scheduled-only-binding-plan-2026-09-30.md`; it predates this execution. The runner and temporary test instrumentation are not part of this repository evidence commit; the pinned production Engram source was unchanged.
