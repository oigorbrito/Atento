# Engram browser adapter integration boundary — 2026-09-30

## Scope

This is a bounded execution follow-up to [the first residual probe](../naia-engram-browser-authority-probe-2026-09-30.md). It exercises the exact Engram pin through its `engram-agent::Agent::run` path with a deterministic provider and the Atento-owned adapter wrapped as two MCP tool identities.

It does not execute the Engram daemon's real scheduler dispatch and does not qualify, select, accept, or promote Engram.

## Frozen identities and artifacts

```text
Atento base = cc5bacb648d98f0a055afcfba5c7424c39ba8e2a
Engram repository = radotsvetkov/engram
Engram pin = 3a43667deec4a680b42f3e880d7d6bac3baf0746
Atento adapter.py Git blob = a5162276bc8c4a48cfd53179bd100b16cb305c64
```

The temporary candidate patch adds only a `#[cfg(test)]` test module to Engram's `crates/engram-agent/src/lib.rs`. It is applied to the disposable checkout by the runner and is not an Engram product change. The adapter implementation is the existing Atento probe artifact; `mcp_server.py` exposes that adapter through Engram's stdio MCP client.

## Executed probe

Command:

```sh
evals/probes/engram_browser_authority/run_engram_probe.sh <output-dir>
```

The runner clones Engram, checks out and verifies the exact pin, applies the test-only patch, copies the pinned Atento adapter and MCP wrapper into the run directory, and runs one exact Rust test. Raw output: `evidence/engram-agent-runtime-probe-2026-09-30.log`.

Observed environment and result:

```text
Linux 6.18.44 x86_64
rustc 1.98.1
cargo 1.98.1
Python 3.12.14
ACTUAL_ENGRAM_PIN = 3a43667deec4a680b42f3e880d7d6bac3baf0746
1 test passed; 0 failed
test runtime = 0.24s
```

The deterministic provider made no external model call. The probe added no runtime dependencies and used only a fake reversible browser driver.

## Observed assertions

```ini
NATIVE_BROWSER_CLICK_TYPE_REMOVED = PASS
MEDIATED_MCP_TOOL_PRESENT = PASS
INTERACTIVE_AGENT_RUN_REACHES_ADAPTER = PASS_IN_HARNESS
UNATTENDED_CONTEXT_AGENT_RUN_REACHES_ADAPTER = PASS_IN_HARNESS
MODEL_SUPPLIED_ORIGIN_IGNORED = PASS
SCHEDULED_CLICK_GRANT = PASS
SCHEDULED_UNGRANTED_TYPE = DENIED_TECHNICALLY
AUTHORITY_CONTROL_ERROR = FAIL_CLOSED
CANDIDATE_VISIBLE_CREDENTIAL_SENTINEL = NOT_OBSERVED
```

The scheduled server obtains its origin from its subprocess configuration; the scripted model sends `origin=interactive` even on the scheduled call, and the adapter reports `scheduled`. The test constructs separate interactive and scheduled MCP tool identities and supplies the corresponding one-tool registry to each Agent run. The frozen adapter policy allows a click in both contexts and allows typing only interactively.

## Decision boundary and remaining block

This closes a bounded `Agent::run` + MCP + adapter composition path. It shows a no-core-patch integration route is executable in the harness:

```text
disable native browser click/type
+ separate interactive/scheduled MCP tool identities
+ caller-selected effective tool registry
+ adapter origin fixed outside model-authored arguments
```

The harness itself selects the corresponding tool registry. It does **not** establish that Engram's actual daemon/scheduler constructs and enforces those distinct toolsets for interactive and scheduled NAIA runs.

```ini
ENGRAM_AGENT_MCP_ADAPTER_BOUNDARY = PASS_WITH_SCOPE
REAL_DAEMON_SCHEDULER_DISPATCH = NOT_RUN
PRODUCTION_SCHEDULED_TOOLSET_BINDING = NOT_PROVEN
ENGRAM_BROWSER_EFFECT_AUTHORITY = STILL_OPEN
CORE_PATCH_REQUIRED = NOT_PROVEN
CURRENT_PIN_QUALIFIED = 0
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

The next decisive probe is to locate the real scheduler's run construction and show that an unattended NAIA run receives only the scheduled adapter identity while the interactive run receives the interactive identity, then execute those real entrypoints through the adapter. Do not rerun this harness or the eight standalone adapter checks without a material delta.
