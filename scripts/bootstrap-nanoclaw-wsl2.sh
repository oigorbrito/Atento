#!/usr/bin/env bash
set -euo pipefail

FORK="${ATENTO_NANOCLAW_FORK:-oigorbrito/nanoclaw}"
UPSTREAM="${ATENTO_NANOCLAW_UPSTREAM:-nanocoai/nanoclaw}"
PIN="${ATENTO_NANOCLAW_UPSTREAM_PIN:-3f7e13b591a0c8980242b81ceff4b3f542ef839a}"
ROOT="${ATENTO_NANOCLAW_ROOT:-$HOME/atento-nanoclaw}"

for cmd in git gh docker; do
  command -v "$cmd" >/dev/null || { echo "missing required command: $cmd" >&2; exit 10; }
done

gh auth status >/dev/null
docker info >/dev/null

if ! gh repo view "$FORK" >/dev/null 2>&1; then
  gh repo fork "$UPSTREAM" --clone=false
fi

if [ ! -d "$ROOT/.git" ]; then
  gh repo clone "$FORK" "$ROOT"
fi

cd "$ROOT"
git remote get-url upstream >/dev/null 2>&1 || git remote add upstream "https://github.com/$UPSTREAM.git"
git fetch upstream --prune
git fetch origin --prune
git cat-file -e "$PIN^{commit}"

BRANCH="atento/runtime-${PIN:0:12}"
if git show-ref --verify --quiet "refs/heads/$BRANCH"; then
  git checkout "$BRANCH"
else
  git checkout -b "$BRANCH" "$PIN"
fi

HEAD="$(git rev-parse HEAD)"
if [ "$HEAD" != "$PIN" ]; then
  echo "FAIL: runtime head $HEAD differs from frozen upstream pin $PIN" >&2
  exit 20
fi

git push -u origin "$BRANCH"

echo "ATENTO_NANOCLAW_FORK=$FORK"
echo "ATENTO_NANOCLAW_UPSTREAM_PIN=$PIN"
echo "ATENTO_NANOCLAW_APPROVED_RUNTIME_HEAD=$HEAD"
echo "ATENTO_NANOCLAW_BRANCH=$BRANCH"
echo "ATENTO_NANOCLAW_ROOT=$ROOT"
echo
echo "Next: bash nanoclaw.sh"
echo "Then: pnpm exec tsx src/cli/client.ts groups list --json"
