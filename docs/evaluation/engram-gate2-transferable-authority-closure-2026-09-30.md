# Engram Gate-2 transferable authority closure — 2026-09-30

## Candidate

`radotsvetkov/engram@3a43667deec4a680b42f3e880d7d6bac3baf0746`

## Exact-pin hosted execution

Direct Actions lookup establishes:

```text
CI run 29098438505 = SUCCESS
Release run 29098445723 = SUCCESS
```

The main job `fmt · clippy · test` completed successfully.

Observed executed test sets include:

```text
engram core/unit set = 116 passed / 1 ignored
engram-agent browser-cdp feature set = 102 passed / 6 ignored
agent scenario set = 4 passed / 0 failed
```

## Gate-2 clauses transferred from executed tests

The exact-pin run executed tests proving:

- opaque egress never auto-allows even under wildcard standing autonomy;
- autonomous egress budget is bounded;
- unattended non-allowlisted egress stages instead of auto-executing;
- explicit user approval permits the tested egress path;
- untrusted+sensitive combinations refuse egress;
- shell is refused when disabled;
- delegated/subagent execution uses inherited authority context;
- process skills are refused without the exec gate;
- filesystem parent and symlink escapes are blocked;
- sandbox command network is denied by default;
- tainted provenance cannot silently use the local process path.

Therefore:

```text
EGRESS_FAIL_CLOSED_FOR_TESTED_TAINT_CASES = PASS_UPSTREAM_EXACT_PIN
OPAQUE_DESTINATION_AUTO_ALLOW = DENIED
AUTONOMY_BUDGET = ENFORCED
SHELL_DISABLED = TECHNICALLY_REFUSED
FILESYSTEM_ESCAPE = DENIED
SUBAGENT_AUTHORITY_CONTEXT = EXECUTED_WITH_SCOPE
```

## Important non-transfer

The browser-CDP test job was compiled/executed with the feature, but real Chrome browser action tests were ignored:

```text
browser_cdp::navigates_types_clicks_and_extracts = IGNORED_NEEDS_CHROME
browser real-page tests = IGNORED_NEEDS_CHROME
```

Also, browser click/type remain outside Engram's egress classification by design.

Therefore:

```text
BROWSER_CONSEQUENTIAL_AUTHORITY = NOT_CLOSED
```

## Remaining Atento-specific residual

```text
NAIA separate ENGRAM_HOME/runtime
Anna separate ENGRAM_HOME/runtime
explicit broker only

trusted-run consequential effects = frozen technical authority
browser click/type consequential effects = technical gate
cross-home memory = denied
cross-home credentials = denied
cross-role tools/channels = denied
schedule wake behavior = frozen for deployment
```

## Gate-2 disposition

```text
ENGRAM_EXACT_PIN_CI = PASS
ENGRAM_EGRESS_AUTHORITY_TRANSFER = PASS_WITH_SCOPE
ENGRAM_FILESYSTEM_SHELL_TRANSFER = PASS_WITH_SCOPE
ENGRAM_BROWSER_AUTHORITY = OPEN
ENGRAM_ATENTO_RESIDUAL = TWO_HOME_COMPOSITION + UNIVERSAL_EFFECT_GATE + BROWSER_GATE

ENGRAM_CURRENT_PIN_QUALIFIED = NO
```

No broad Engram suite should be rerun locally.
