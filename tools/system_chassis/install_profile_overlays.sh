#!/usr/bin/env bash
set -euo pipefail

candidate=${1:?candidate checkout path required}
providers=${2:?providers checkout path required}
channels=${3:?channels checkout path required}
profile=${4:-evals/config/system_chassis_nanoclaw_v1.json}

mapfile -t pins < <(python3 - "$profile" <<'PY'
import json, sys
cfg = json.load(open(sys.argv[1], encoding="utf-8"))
recipe = cfg["topology"]["recipe"]
print(cfg["upstream_sha"])
print(recipe["providers_sha"])
print(recipe["channels_sha"])
PY
)
[[ $(git -C "$candidate" rev-parse HEAD) == "${pins[0]}" ]]
[[ $(git -C "$providers" rev-parse HEAD) == "${pins[1]}" ]]
[[ $(git -C "$channels" rev-parse HEAD) == "${pins[2]}" ]]

copy_from() {
  local source_root=$1 destination_root=$2 rel
  shift 2
  for rel in "$@"; do
    mkdir -p "$destination_root/$(dirname "$rel")"
    cp "$source_root/$rel" "$destination_root/$rel"
  done
}

copy_map() {
  local source_root=$1 destination_root=$2 mapping source_rel target_rel
  shift 2
  for mapping in "$@"; do
    source_rel=${mapping%% -> *}
    target_rel=${mapping#* -> }
    mkdir -p "$destination_root/$(dirname "$target_rel")"
    cp "$source_root/$source_rel" "$destination_root/$target_rel"
  done
}

copy_from "$providers" "$candidate" \
  src/providers/codex.ts \
  src/providers/codex-agents-md.ts \
  src/providers/codex-registration.test.ts \
  src/providers/codex-host-contribution.test.ts \
  src/providers/codex-agents-md.test.ts \
  container/agent-runner/src/providers/codex.ts \
  container/agent-runner/src/providers/codex-app-server.ts \
  container/agent-runner/src/providers/exchange-archive.ts \
  container/agent-runner/src/providers/exchange-archive.test.ts \
  container/agent-runner/src/providers/codex-registration.test.ts \
  container/agent-runner/src/providers/codex.factory.test.ts \
  container/agent-runner/src/providers/codex.turns.test.ts \
  container/agent-runner/src/providers/codex-app-server.test.ts \
  container/agent-runner/src/providers/codex-contract-parity.test.ts \
  container/agent-runner/src/providers/codex.conformance.test.ts \
  container/agent-runner/src/providers/codex-cli-tools.test.ts \
  container/agent-runner/src/provider-contracts/codex.ts \
  setup/providers/codex-registration.test.ts \
  container/AGENTS.md

copy_map "$candidate/.claude/skills/add-codex" "$candidate" \
  'payload/src/provider-contracts/codex.ts -> src/provider-contracts/codex.ts' \
  'payload/setup/providers/codex.ts -> setup/providers/codex.ts' \
  'payload/setup/providers/codex.test.ts -> setup/providers/codex.test.ts'

copy_map "$candidate/.claude/skills/add-onecli" "$candidate" \
  'payload/src/gateway-providers/onecli-files.ts -> src/gateway-providers/onecli-files.ts' \
  'payload/src/gateway-providers/onecli-files.test.ts -> src/gateway-providers/onecli-files.test.ts' \
  'payload/src/gateway-providers/onecli.ts -> src/gateway-providers/onecli.ts' \
  'payload/src/gateway-providers/onecli.test.ts -> src/gateway-providers/onecli.test.ts' \
  'payload/src/gateway-providers/onecli-install.test.ts -> src/gateway-providers/onecli-install.test.ts' \
  'payload/container/skills/onecli-gateway/SKILL.md -> container/skills/onecli-gateway/SKILL.md' \
  'payload/container/skills/onecli-gateway/instructions.md -> container/skills/onecli-gateway/instructions.md' \
  'payload/docs/onecli-upgrades.md -> docs/onecli-upgrades.md'

copy_from "$channels" "$candidate" \
  src/channels/telegram.ts \
  src/channels/telegram-pairing.ts \
  src/channels/telegram-pairing.test.ts \
  src/channels/telegram-markdown-sanitize.ts \
  src/channels/telegram-markdown-sanitize.test.ts \
  src/channels/telegram-registration.test.ts

append_import() {
  local file=$1 line=$2
  grep -Fqx "$line" "$file" || printf '\n%s\n' "$line" >> "$file"
}

append_import "$candidate/src/providers/index.ts" "import './codex.js';"
append_import "$candidate/src/provider-contracts/index.ts" "import './codex.js';"
append_import "$candidate/container/agent-runner/src/provider-contracts/index.ts" "import './codex.js';"
append_import "$candidate/container/agent-runner/src/providers/index.ts" "import './codex.js';"
append_import "$candidate/setup/providers/index.ts" "import './codex.js';"
append_import "$candidate/src/gateway-providers/installed.ts" "import './onecli.js';"
append_import "$candidate/src/channels/index.ts" "import './telegram.js';"

python3 - "$candidate/container/cli-tools.json" <<'PY'
import json, sys
path = sys.argv[1]
tools = json.load(open(path, encoding="utf-8"))
name, version = "@openai/codex", "0.155.1"
found = next((item for item in tools if item.get("name") == name), None)
if found and found.get("version") != version:
    raise SystemExit(f"unexpected {name} CLI pin: {found.get('version')}")
if not found:
    tools.append({"name": name, "version": version})
with open(path, "w", encoding="utf-8", newline="\n") as f:
    json.dump(tools, f, indent=2)
    f.write("\n")
PY

pnpm --dir "$candidate" add --save-exact \
  @chat-adapter/telegram@4.29.0 \
  @onecli-sh/sdk@2.2.1

echo "Installed the profile-pinned NanoClaw core, provider, gateway and channel overlays."

