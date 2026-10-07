# NanoClaw fork bootstrap for Atento

Production blocker: #65.

Fixed boundary:

- upstream: `nanocoai/nanoclaw`
- Atento fork: `oigorbrito/nanoclaw`
- approved upstream baseline: `d7175d0dee42a1130c17ced09220b983257696a4` (`v2026.10.0-rc.2`)
- Windows deployment: WSL2/Linux + Docker
- Atento runtime head must be explicit and descend from the approved upstream baseline

## Execute inside WSL2

From the Atento checkout mounted in WSL2:

```bash
bash scripts/bootstrap-nanoclaw-wsl2.sh
```

The script fails closed unless GitHub CLI authentication and Docker are working. It creates the fork when absent, clones it, checks out the exact approved baseline, creates `atento/runtime-d7175d0dee42`, and pushes that branch.

Then, inside the printed `ATENTO_NANOCLAW_ROOT`:

```bash
bash nanoclaw.sh
pnpm exec tsx src/cli/client.ts groups list --json
```

Retain concrete IDs for:

```text
NAIA   -> <group-id>
ANNA   -> <group-id>
APOLLO -> <group-id>
```

Do not use NanoClaw pairing or `owner` as Atento authority.

## #65 acceptance evidence

Current runtime qualification evidence (2026-10-06) is 3/3 for the common chassis using distinct NanoClaw agent groups and the same Codex runtime path:

- NAIA: task completed with persisted `ATENTO_RUNTIME_OK`;
- Anna: task completed with persisted `ATENTO_RUNTIME_OK`;
- Apollo: task produced persisted `groups/apollo/tasks/atento-apollo-smoke-01-7a9f.md` containing `ATENTO_RUNTIME_OK`.

This proves the common NanoClaw chassis can execute all three agent groups on the approved RC2 baseline. It does not prove Atento Host adapter dispatch, authority binding, crash reconciliation, Telegram delivery, or production eligibility.

#65 PASS still requires retained evidence for the exact runtime head: `git rev-parse HEAD`, ancestry from the approved baseline, `docker info`, group IDs, role-to-group mapping, one real dispatch through the Atento adapter to completion/ACK, and one ambiguous dispatch/post-dispatch loss proving `RECONCILE_REQUIRED`. Mocks or documentation are not PASS.
