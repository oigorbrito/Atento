# Engram scheduled toolset binding source audit — 2026-09-30

## Exact candidate source

Candidate repository: radotsvetkov/engram
Frozen pin: 3a43667deec4a680b42f3e880d7d6bac3baf0746

This is a static source audit of the daemon's run-construction path. It is not an executed scheduler experiment.

## Observed source flow

At the frozen pin:

1. Both scheduler entrypoints create a task and call run_task_core with attended=false:
   - one-shot --run-due: crates/engramd/src/main.rs:1116-1124;
   - resident scheduler tick: crates/engramd/src/main.rs:4957-4978.
2. run_task_core resolves the task's assigned durable agent at main.rs:4405-4407 and passes that same agent_def into run_agent_task_cb at main.rs:4461-4470.
3. run_agent_task_cb reads allowed_tools from that AgentDef at main.rs:3157-3161, appends the process's MCP tools, then filters the effective registry by the static list at main.rs:3222-3239.
4. Interactive and unattended invocations of the same task/agent both use this AgentDef.allowed_tools. The attended argument controls run policy, but the tool-registry construction shown above does not branch on it.
5. Engram's McpTool::run forwards model-authored arguments to MCP at crates/engram-agent/src/mcp.rs:705-713; it does not attach trusted run-origin metadata.

## Decision-relevant consequence

The passing harness used different effective registries for its interactive and scheduled-context Agent::run invocations. This source path does not show the daemon making that distinction for one shared durable-agent identity.

If the same agent allowlist contains both adapter identities, the unattended run can also see the interactive identity. If it contains only one, the interactive and scheduled calls share that same identity. The model-authored origin argument cannot close the gap because MCP receives it as ordinary tool arguments.

This is a source-derived inference from the call path, not a runtime FAIL for Engram. Separate agent identities or a trusted run-context-aware binding may be possible, but neither is selected or proven here.

## Current classification

~~~ini
ENGRAM_SOURCE_PATH_MAPPING = COMPLETE_FOR_TOOLSET_BINDING
SCHEDULER_ENTRYPOINTS_SET_UNATTENDED = CONFIRMED_STATIC
AGENT_ALLOWED_TOOLS = STATIC_PER_AGENT
MCP_RUN_ORIGIN_PROPAGATION = NOT_PRESENT_IN_INSPECTED_CALL
PRODUCTION_SCHEDULED_TOOLSET_BINDING = NOT_PROVEN
SAME_AGENT_INTERACTIVE_SCHEDULED_SEPARATION = NOT_ESTABLISHED
ENGRAM_BROWSER_EFFECT_AUTHORITY = STILL_OPEN
ENGRAM_CANDIDATE_FAIL = NOT_CLAIMED
CURRENT_PIN_QUALIFIED = 0
~~~

## Next decisive work

Before another execution, freeze a composition that binds trusted run context to the effective adapter authority while preserving the intended NAIA identity and memory boundary. Compare the narrow options on evidence and total adaptation/maintenance cost. Then test the real daemon entrypoints (interactive and scheduled) with a deterministic provider and the Atento MCP adapter. A new generic adapter suite or repeated Agent::run harness would not address this gap.
