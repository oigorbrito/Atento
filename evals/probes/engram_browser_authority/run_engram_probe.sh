#!/usr/bin/env bash
set -euo pipefail
if [[ $# -ne 1 ]]; then
  echo "usage: $0 OUTPUT_DIR" >&2
  exit 2
fi
out=$1
probe_root=$(git rev-parse --show-toplevel)
probe_root="$probe_root/evals/probes/engram_browser_authority"
mkdir -p "$out"
out=$(cd "$out" && pwd)
log="$out/run.log"
candidate="$out/engram"
adapter_dir="$out/adapter"

{
  echo "PROBE=Atento Engram browser authority integration boundary"
  echo "EXPECTED_ENGRAM_PIN=3a43667deec4a680b42f3e880d7d6bac3baf0746"
  echo "HOST=$(uname -srm)"
  echo "RUST=$(rustc --version)"
  echo "CARGO=$(cargo --version)"
  echo "PYTHON=$(python3 --version)"
  echo "START_UTC=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  git clone --filter=blob:none https://github.com/radotsvetkov/engram.git "$candidate"
  git -C "$candidate" checkout --detach 3a43667deec4a680b42f3e880d7d6bac3baf0746
  actual=$(git -C "$candidate" rev-parse HEAD)
  echo "ACTUAL_ENGRAM_PIN=$actual"
  test "$actual" = "3a43667deec4a680b42f3e880d7d6bac3baf0746"
  git -C "$candidate" apply "$probe_root/engram-agent-probe.patch"
  mkdir -p "$adapter_dir"
  cp "$probe_root/adapter.py" "$probe_root/mcp_server.py" "$adapter_dir/"
  echo "TEST=engram-agent::atento_mcp_runtime_probe::candidate_agent_routes_both_origins_through_adapter_and_fails_closed"
  (cd "$candidate" && ATENTO_PROBE_DIR="$adapter_dir" cargo test -p engram-agent atento_mcp_runtime_probe::candidate_agent_routes_both_origins_through_adapter_and_fails_closed -- --exact --nocapture)
  echo "END_UTC=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "RESULT=PASS_BOUNDED_AGENT_RUN_PATH"
  echo "LIMIT=REAL_DAEMON_SCHEDULER_DISPATCH_NOT_EXERCISED"
} 2>&1 | tee "$log"

