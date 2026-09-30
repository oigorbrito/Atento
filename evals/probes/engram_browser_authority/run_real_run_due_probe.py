#!/usr/bin/env python3
"""Exercise the exact-pin Engram CLI --run-due path against local deterministic fakes."""
from __future__ import annotations

import http.server
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
import socket
import urllib.request

PIN = "3a43667deec4a680b42f3e880d7d6bac3baf0746"
INTERACTIVE = "mcp_atento_browser_interactive_effect"
SCHEDULED = "mcp_atento_browser_scheduled_effect"
SECRET = "BROWSER_PROVIDER_SECRET_DO_NOT_LEAK"
HERE = Path(__file__).resolve().parent


class ProviderHandler(http.server.BaseHTTPRequestHandler):
    calls = 0
    seen_tool_names = set()
    def do_POST(self):
        size = int(self.headers.get("Content-Length", "0"))
        body = json.loads(self.rfile.read(size))
        ProviderHandler.calls += 1
        messages = body.get("messages", [])
        transcript = json.dumps(messages)
        interactive_case = "interactive browser authority probe" in transcript
        scheduled_case = not interactive_case and "Exercise one scheduled browser effect" in transcript
        tool_results = sum(message.get("role") == "tool" for message in messages)
        if (scheduled_case and tool_results >= 2) or (not scheduled_case and tool_results >= 1):
            message = {"role": "assistant", "content": "deterministic probe completed"}
            finish = "stop"
        else:
            available = [t["function"]["name"] for t in body.get("tools", [])]
            ProviderHandler.seen_tool_names.update(available)
            wanted = SCHEDULED if scheduled_case and tool_results == 0 else INTERACTIVE
            if wanted not in available:
                self.send_error(500, f"requested adapter missing from candidate tools: {wanted}; {available}")
                return
            message = {"role": "assistant", "content": "", "tool_calls": [{
                "id": "probe-call-1", "type": "function", "function": {
                    "name": wanted,
                    "arguments": json.dumps({"destination": "https://example.test/form",
                        "action": "type", "selector": "#note", "text": "scheduled probe",
                        "origin": "scheduled"}),
                },
            }]}
            finish = "tool_calls"
        payload = {"id": "probe", "object": "chat.completion", "created": int(time.time()),
            "model": body.get("model", "probe"), "choices": [{"index": 0, "message": message,
            "finish_reason": finish}], "usage": {"prompt_tokens": 1, "completion_tokens": 1,
            "total_tokens": 2}}
        raw = json.dumps(payload).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def log_message(self, *_args):
        pass


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} ENGRAM_CHECKOUT OUTPUT_DIR", file=sys.stderr)
        return 2
    candidate = Path(sys.argv[1]).resolve()
    output = Path(sys.argv[2]).resolve()
    output.mkdir(parents=True, exist_ok=True)
    actual_pin = subprocess.check_output(["git", "-C", str(candidate), "rev-parse", "HEAD"], text=True).strip()
    if actual_pin != PIN:
        raise SystemExit(f"pin mismatch: expected {PIN}, got {actual_pin}")
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), ProviderHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    port = server.server_address[1]
    start = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with tempfile.TemporaryDirectory(prefix="atento-run-due-") as temp:
        home = Path(temp) / "home"
        home.mkdir()
        now_ms = int(time.time() * 1000)
        agent_id = "agent-atento-probe"
        agent = {"id": agent_id, "name": "probe", "charter": "authority probe", "model": "",
            "provider": "", "base_url": "", "api_key": "", "effort": "",
            "allowed_tools": [INTERACTIVE, SCHEDULED], "home_project": None,
            "autonomy_policy": None, "color": "", "emoji": "", "created_ms": now_ms,
            "updated_ms": now_ms}
        (home / "agents.json").write_text(json.dumps([agent]))
        job = {"id": "atento-run-due-probe", "name": "browser authority probe",
            "payload": {"title": "Exercise one scheduled browser effect via the adapter",
                "detail": "Use the deterministic local adapter only."},
            "recurrence": {"kind": "once", "at_ms": now_ms - 5000},
            "next_fire_ms": now_ms - 1000, "created_ms": now_ms - 10000,
            "last_fire_ms": None, "last_task_id": None, "agent_id": agent_id}
        (home / "jobs.json").write_text(json.dumps([job]))
        adapter = HERE
        mcp = []
        for origin in ("interactive", "scheduled"):
            mcp.append({"name": f"atento_browser_{origin}", "command": sys.executable,
                "args": ["-u", str(adapter / "mcp_server.py")],
                "env": {"PYTHONPATH": str(adapter), "ATENTO_ORIGIN": origin,
                    "BROWSER_PROVIDER_SECRET": SECRET}, "cwd": str(adapter), "trusted": True})
        (home / "mcp.json").write_text(json.dumps(mcp))
        config = {"provider": {"kind": "openai", "base_url": f"http://127.0.0.1:{port}/v1",
                "model": "probe", "effort": ""},
            "embed": {"kind": "trigram", "model_dir": ""},
            "security": {"disabled_tools": ["browser_click", "browser_type"]}}
        (home / "config.json").write_text(json.dumps(config))
        env = os.environ.copy()
        env.update({"ENGRAM_HOME": str(home), "ENGRAM_LLM_API_KEY": "local-probe-only",
            "ENGRAM_EMBED_KIND": "trigram", "ENGRAM_IDLE_SECS": "1"})
        cmd = ["cargo", "run", "--offline", "--features", "http", "-p", "engramd", "--", "--run-due"]
        proc = subprocess.run(cmd, cwd=candidate, env=env, text=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, timeout=180)
        (output / "daemon.log").write_text(proc.stdout)
        tasks_file = home / "tasks.json"
        tasks = json.loads(tasks_file.read_text()) if tasks_file.exists() else []
        jobs = json.loads((home / "jobs.json").read_text())
        if proc.returncode != 0:
            raise SystemExit(f"engramd --run-due exit={proc.returncode}; see {output / 'daemon.log'}")
        if len(tasks) != 1:
            raise SystemExit(f"expected exactly one scheduler-created task, got {len(tasks)}")
        task = tasks[0]
        run = task.get("run") or {}
        steps = run.get("steps") or []
        step = next((s for s in steps if s.get("tool") == INTERACTIVE), None)
        if not step or "typed" not in step.get("observation", ""):
            raise SystemExit(f"interactive effect not observed in task receipt: {steps}")
        denial = next((s for s in steps if s.get("tool") == SCHEDULED), None)
        if not denial or "AuthorityDenied" not in denial.get("observation", ""):
            raise SystemExit(f"scheduled identity denial not observed in task receipt: {steps}")
        if task.get("status") != "done":
            raise SystemExit(f"scheduled task status was {task.get('status')!r}")
        if jobs:
            raise SystemExit(f"one-shot due job was not consumed: {jobs}")
        if SECRET in proc.stdout or SECRET in json.dumps(tasks):
            raise SystemExit("test credential appeared in model/provider-visible or task receipt output")

        # Run the comparison through the actual attended task HTTP entrypoint in a fresh daemon.
        with socket.socket() as probe_socket:
            probe_socket.bind(("127.0.0.1", 0))
            daemon_port = probe_socket.getsockname()[1]
        env["ENGRAM_ADDR"] = f"127.0.0.1:{daemon_port}"
        service = subprocess.Popen(cmd[:-1], cwd=candidate, env=env, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True)
        base = f"http://127.0.0.1:{daemon_port}"
        try:
            deadline = time.monotonic() + 30
            while True:
                try:
                    with urllib.request.urlopen(base + "/v1/tasks", timeout=1) as response:
                        if response.status == 200:
                            break
                except Exception:
                    if service.poll() is not None:
                        raise SystemExit("interactive daemon exited before API became ready")
                    if time.monotonic() >= deadline:
                        raise SystemExit("interactive daemon API did not become ready")
                    time.sleep(0.2)
            def post(path: str, value: dict | None = None):
                raw = json.dumps(value).encode() if value is not None else b""
                request = urllib.request.Request(base + path, data=raw, method="POST",
                    headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(request, timeout=60) as response:
                    return json.loads(response.read())
            interactive_task = post("/v1/tasks", {"title": "interactive browser authority probe",
                "detail": "Use the deterministic local adapter only.", "origin": "ui"})
            interactive_id = interactive_task["id"]
            post(f"/v1/tasks/{interactive_id}/agent", {"agent": agent_id})
            interactive_receipt = post(f"/v1/tasks/{interactive_id}/run")
            interactive_steps = (interactive_receipt.get("run") or {}).get("steps") or []
            interactive_step = next((s for s in interactive_steps if s.get("tool") == INTERACTIVE), None)
            if not interactive_step or "typed" not in interactive_step.get("observation", ""):
                raise SystemExit(f"interactive comparison did not execute the effect: {interactive_steps}")
            if interactive_receipt.get("status") != "done":
                raise SystemExit(f"interactive control task status was {interactive_receipt.get('status')!r}")
        finally:
            service.terminate()
            try:
                service_output, _ = service.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                service.kill()
                service_output, _ = service.communicate(timeout=5)
            (output / "interactive-daemon.log").write_text(service_output)
        server.shutdown()
        if SECRET in service_output or SECRET in json.dumps(interactive_receipt):
            raise SystemExit("test credential appeared in interactive logs or task receipt")
        (output / "receipts.json").write_text(json.dumps({
            "scheduled": task,
            "interactive_control": interactive_receipt,
        }, indent=2, sort_keys=True) + "\n")
        native_tools = {"browser_click", "browser_type"}.intersection(ProviderHandler.seen_tool_names)
        if native_tools:
            raise SystemExit(f"unmediated native browser tools were advertised: {sorted(native_tools)}")
        result = [
            "PROBE=Atento exact-pin Engram external --run-due browser authority boundary",
            f"EXPECTED_ENGRAM_PIN={PIN}", f"ACTUAL_ENGRAM_PIN={actual_pin}",
            f"START_UTC={start}", "TRIGGER=real engramd --run-due subprocess",
            "SCHEDULE_ENTRY=due persisted one-shot scheduler job; task created by task_from_schedule",
            "PROVIDER=local deterministic OpenAI-compatible HTTP server; no external model call",
            f"PROVIDER_CALLS={ProviderHandler.calls}",
            "NATIVE_BROWSER_TOOLS=browser_click/browser_type absent from effective provider toolsets",
            "ADAPTER_DRIVER=fake reversible driver; no real browser",
            "SCHEDULED_TOOL_IDENTITY=denied type effect by scheduled grant",
            "INTERACTIVE_TOOL_IDENTITY=executed type effect during unattended --run-due",
            f"TASK_STATUS={task.get('status')}", "JOB_CONSUMED=YES",
            "INTERACTIVE_CONTROL=real daemon POST /v1/tasks/{id}/run with attended=true; same effect executed",
            "CREDENTIAL_LEAK=NOT_OBSERVED", "RESULT=FAIL_EMPIRICAL_FOR_TESTED_COMPOSITION",
            "LIMIT=resident scheduler tick and real browser not exercised",
        ]
        (output / "summary.txt").write_text("\n".join(result) + "\n")
        print("\n".join(result))
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
