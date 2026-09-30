# QwenPaw exhaustive verification — 2026-09-30

## Scope

Candidate: `agentscope-ai/QwenPaw`

Frozen evaluation pin:

```
777441721aa72db8e380d90e4d0481b05cbfd4cc
```

This record continues the Atento candidate evaluation without moving the frozen pin. It consolidates exact-pin GitHub Actions execution, decoded failing logs, the exact source implementation implicated by those failures, and post-pin upstream fixes used only as causal corroboration.

Rules preserved:

- `UPSTREAM_SIGNAL != ATENTO_LOCAL_PROOF`
- `IMPLEMENTED != QUALIFIED`
- `VERIFIED != ACCEPTED`
- `ACCEPTED != PROMOTED`
- a later upstream fix does not retroactively make the frozen pin pass
- no candidate selection or promotion is authorized by this report

No QwenPaw source was modified.

## Exact-pin upstream execution

Scheduled workflow:

- workflow: `Full Tests Nightly`
- run: `36604935140`
- event: `schedule`
- exact head: `777441721aa72db8e380d90e4d0481b05cbfd4cc`
- conclusion: `failure`

The run exercised substantially more than the narrow push checks.

Observed successful jobs include:

- unit tests: Python 3.11 on Ubuntu, macOS, and Windows
- contract tests
- integrated tests: Python 3.11 on Ubuntu/macOS/Windows and Python 3.13 on Ubuntu
- frontend Vitest
- coverage aggregation

The exact-pin Python 3.13 / Ubuntu unit job failed.

### Unit failure

Observed summary:

```
4 failed, 17040 passed, 24 skipped, 3082 warnings
```

All four failures are in `tests/unit/services/test_terminal.py`:

1. `test_pty_does_not_inherit_service_socket`
2. `test_real_pty_cwd_unicode_resize_interrupt_and_cleanup`
3. `test_close_releases_write_blocked_by_pty_backpressure`
4. `test_exit_replay_and_detached_reclamation`

The reader thread traceback is the same failure class across the affected tests:

```
src/qwenpaw/services/terminal.py:_read
  -> self.process.read(4096)
src/qwenpaw/services/terminal_posix.py:read
  -> select.select([self.fd], [], [], IO_POLL_INTERVAL)

ValueError: filedescriptor out of range in select()
```

At this pin, `TerminalSession._read()` catches `EOFError` and `OSError`, but not this `ValueError`. The reader thread therefore terminates before the test can observe expected PTY output. This accounts directly for the empty-output assertions in three of the four failures and invalidates treating the red job as an external executor permission block.

Classification:

```ini
QWENPAW_EXACT_PIN_UNIT = FAIL
FAILURE_CLASS = UPSTREAM_IMPLEMENTATION_ROBUSTNESS
ENVIRONMENT_BLOCK = NO
```

The fact that the same broad unit suite passed on Python 3.11 and other platforms narrows the defect's observed trigger; it does not erase the exact-pin Python 3.13/Linux failure.

## E2E shards

The reusable E2E job at the frozen pin defines:

```yaml
timeout-minutes: 60
```

and the workflow documentation explicitly treats a shard reaching that ceiling as a cancelled/red result.

All three nightly Playwright shards were ultimately cancelled after approximately the job ceiling. They were not merely skipped because the unit job failed: each shard had started, executed tests, emitted its own failures, and continued/stalled until cancellation.

### p0

Before cancellation, the log records failing node IDs including:

- `TestACPPageDisplay::test_acp_page_load_and_card_list`
- `TestCreateACPDrawerForm::test_create_acp_drawer_form`
- `TestAgentList::test_agent_list_display_and_refresh`
- `TestCreateAgent::test_create_agent_success`
- `TestEditAgent::test_edit_agent_info`
- `TestToggleAgent::test_toggle_agent_status`
- `TestChannelListAndFilter::test_channel_list_filter_and_type`
- `TestConsoleEditConfig::test_console_edit_save_cancel`
- `TestDiscordEnableDisable::test_discord_enable_disable_ui`

The shard reached only roughly one quarter of its selected sequence before progress stopped and the job was cancelled.

### p1

Before cancellation:

- `TestCreateAndDeleteCustomACP::test_create_and_delete_custom_acp` failed after rerun.
- the next observed test was `TestForkProjectMultiAgent::test_fork_project_multi_agent_collaboration`, after which the shard did not report normal completion before cancellation.

### p2

Before cancellation, observed failures include:

- `TestACPCardDetails::test_acp_card_content_details`
- `TestDeleteAgent::test_delete_agent_success`
- `TestDeleteAgent::test_delete_agent_cancel`
- `TestMultipleChannelFormFields::test_four_channels_form_fields`
- `TestMQTTBotPrefix::test_mqtt_bot_prefix`

After `test_input_validation_and_special_chars` reported its main assertion as passed, cleanup repeatedly failed to open the session menu for an extended period until the 60-minute job ceiling was reached.

Classification:

```ini
QWENPAW_EXACT_PIN_E2E = FAIL_INCOMPLETE
E2E_SHARDS = 3
E2E_COMPLETED_SHARDS = 0
E2E_CANCELLED_SHARDS = 3
PRE_CANCEL_FUNCTIONAL_FAILURES = YES
STALL_BEFORE_CANCEL = YES
```

This supersedes the earlier shorthand that the shards were simply cancelled after the unit failure.

## Post-pin causal corroboration

The immediate child of the frozen pin is:

```
b6229ec30577fc92100def6865bac1d85384e7d4
fix(terminal): support high posix descriptors (#8032)
```

Its parent is exactly the evaluated pin. The patch replaces the POSIX terminal's `select.select()` reader/writer waits with registered `select.poll()` objects.

That is a direct upstream correction for the exact failure class observed in the frozen-pin traceback.

A later upstream commit is:

```
80e412da9b5505bcac5eec6add271d09fa144c60
fix(e2e): stop stalled session cleanup (#8041)
```

Its E2E patch changes stale UI selectors and makes session cleanup stop if the session count does not decrease, matching the prolonged cleanup symptoms observed in the frozen-pin E2E logs.

These commits are useful causal evidence, but they are not part of the frozen candidate pin.

Classification:

```ini
POST_PIN_TERMINAL_FIX = OBSERVED
POST_PIN_E2E_STALL_FIX = OBSERVED
POST_PIN_FIX_TRANSFER_TO_FROZEN_PIN = FORBIDDEN
```

## Atento-specific boundary evidence

Prior static work remains valid: QwenPaw has per-agent/workspace primitives, ownership tuples for terminal sessions, model configuration per agent, cron/scheduling, browser/computer-use surfaces, and policy/sandbox mechanisms.

This pass did not establish the composed Atento requirements:

- NAIA memory authority isolated from Anna
- Anna memory authority isolated from NAIA
- tool/credential/channel authority isolated by role
- scheduled authority equal to foreground authority
- browser authority frozen to an Atento-safe profile
- only explicit brokered handoff across roles
- integration of the selected Engram/adapter/browser chassis

No exact-pin result may be promoted by proxy from the upstream fixes.

## Gate

The smallest defensible exact-pin classification is:

```ini
CANDIDATE = QwenPaw
PIN = 777441721aa72db8e380d90e4d0481b05cbfd4cc

UPSTREAM_UNIT_MATRIX = FAIL
UPSTREAM_E2E = FAIL_INCOMPLETE
UPSTREAM_GENERAL_HEALTH_GATE = FAIL

ATENTO_ISOLATION = NOT_ESTABLISHED
ATENTO_COMPOSITION = NOT_RUN
NAIA_BASE = NOT_SELECTED
PROMOTION = NO
```

Because the frozen pin fails its own broad upstream health gate, downstream Atento composition is not required to decide whether this exact pin can be qualified now. Re-testing a repaired QwenPaw revision would require an explicit re-pin and a fresh evidence record; it must not overwrite this result.

## Evidence references

- exact-pin nightly: https://github.com/agentscope-ai/QwenPaw/actions/runs/36604935140
- exact-pin waiting push Tests workflow: https://github.com/agentscope-ai/QwenPaw/actions/runs/36559841525
- terminal fix immediately after pin: https://github.com/agentscope-ai/QwenPaw/commit/b6229ec30577fc92100def6865bac1d85384e7d4
- later E2E cleanup fix: https://github.com/agentscope-ai/QwenPaw/commit/80e412da9b5505bcac5eec6add271d09fa144c60

## Final disposition for comparison table

```ini
QWENPAW_FROZEN_PIN_STATUS = FAIL
FAIL_REASON_1 = POSIX_HIGH_FD_TERMINAL_DEFECT
FAIL_REASON_2 = E2E_FUNCTIONAL_FAILURES_AND_INCOMPLETE_SHARDS
REPAIR_EXISTS_UPSTREAM = YES_POST_PIN
REPIN_REQUIRED_FOR_REQUALIFICATION = YES
```
