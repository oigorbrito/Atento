# Engram scheduled-only tool binding probe plan — 2026-09-30

## Pre-registration state

This plan is frozen before the probe executes. It continues the RP-AUTH-01 residual after the dual-identity `--run-due` failure in Atento PR #51.

Atento base:

~~~text
main = 1e19915c7a666af5861027ea9477706bcb48d2e8
~~~

Candidate:

~~~text
repository = radotsvetkov/engram
pin = 3a43667deec4a680b42f3e880d7d6bac3baf0746
~~~

## One unresolved property

~~~text
BACKGROUND_AUTHORITY <= INTERACTIVE_AUTHORITY
~~~

The prior dual-identity composition failed because a static per-agent allowlist containing both MCP identities let an unattended task call the interactive adapter identity. No Engram source path in the frozen audit selects `allowed_tools` by `attended`.

## Frozen treatment

Keep the same NAIA durable-agent identity, memory home, candidate pin, adapter, grants, provider, task content, destination, action, and tool implementations. Change only the durable agent's static tool allowlist:

~~~ini
BEFORE = [mcp_atento_browser_scheduled_effect, mcp_atento_browser_interactive_effect]
AFTER  = [mcp_atento_browser_scheduled_effect]
~~~

The existing Atento adapter policy grants scheduled `click` on `https://example.test/form` at `#save`; scheduled `type` at `#note` is absent and must be denied. Interactive-only grants stay configured in the adapter policy but the interactive MCP identity is not exposed to this AgentDef. Both scheduler and attended runs use the same single allowed scheduled identity, so any pass establishes equal, restricted authority for this composition. It does not establish a richer interactive grant or the full NAIA browser profile.

Both tasks will attempt the same benign allowed `click` and denied `type`. Tool arguments will claim `origin="interactive"`; the MCP subprocess's trusted `ATENTO_ORIGIN=scheduled` must remain authoritative in both paths.

## Execution boundary

1. Run a due one-shot job through the actual `engramd --run-due` process. Engram must create the task from the job payload through `task_from_schedule`.
2. In a fresh daemon on the same ENGRAM_HOME and same AgentDef, create an attended task through `POST /v1/tasks/{id}/run`.
3. Use a local deterministic OpenAI-compatible HTTP provider and fake reversible browser driver. No external model or real browser.
4. Verify provider-visible tools include the scheduled adapter identity and exclude the interactive adapter identity plus native `browser_click` / `browser_type`.
5. Compare receipts: both paths execute only the scheduled-granted click and technically deny type; no path reaches the interactive identity.
6. Inspect daemon output, provider-visible results and receipts for the test credential.

## Decision outcomes

~~~ini
PASS_WITH_SCOPE = both real entrypoints expose only the scheduled identity; click is granted; type is denied; tool authority is equal and restricted; credential leak absent
FAIL = interactive identity or broader authority is reachable from unattended execution, a denied type executes, or authority control fails open
INVALID = exact pin / entrypoint / local provider / effective toolset / adapter identity is not verified
~~~

The relevant `FAIL` result would leave this static-toolset treatment insufficient. `PASS_WITH_SCOPE` would prove only the scheduled-only composition and preserve its cost: interactive browser type is unavailable through this AgentDef. Neither outcome qualifies or promotes Engram or changes NAIA/Anna candidate selection.

## Exclusions

~~~text
resident scheduler tick = NOT_IN_SCOPE
real browser = NOT_IN_SCOPE
policy-control exception path = NOT_IN_SCOPE
delegation = NOT_IN_SCOPE (already bounded at adapter boundary)
generic benchmarking / repeated adapter suite = FORBIDDEN
candidate source patch = NOT_AUTHORIZED_BY_THIS_PROBE
~~~

## Cost evidence to capture

Record the one changed allowlist entry, source modifications, dependencies, local wall time, provider call count, task receipts, and hashes. No LLM inference cost is expected because the provider is deterministic and local.

~~~ini
PRE_RUN_RESULT = NOT_RUN
ENGRAM_CANDIDATE_FAIL = NOT_CLAIMED
CURRENT_PIN_QUALIFIED = 0
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
~~~
