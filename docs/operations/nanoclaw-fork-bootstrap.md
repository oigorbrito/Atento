# NanoClaw fork bootstrap for Atento

Production blocker: #65.

Fixed boundary:

- upstream: `nanocoai/nanoclaw`
- Atento fork: `oigorbrito/nanoclaw`
- frozen upstream pin: `3f7e13b591a0c8980242b81ceff4b3f542ef839a`
- Windows deployment: WSL2/Linux + Docker
- Atento runtime head must be explicit and descend from the frozen upstream pin

## Execute inside WSL2

From the Atento checkout mounted in WSL2:

```bash
bash scripts/bootstrap-nanoclaw-wsl2.sh
```

The script fails closed unless GitHub CLI authentication and Docker are working. It creates the fork when absent, clones it, checks out the exact frozen pin, creates `atento/runtime-3f7e13b591a0`, and pushes that branch.

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

PASS requires retained evidence for the exact runtime head: `git rev-parse HEAD`, ancestry from the frozen pin, `docker info`, group IDs, role-to-group mapping, one real dispatch through completion/ACK, and one post-dispatch loss proving `RECONCILE_REQUIRED`. Mocks or documentation are not PASS.
