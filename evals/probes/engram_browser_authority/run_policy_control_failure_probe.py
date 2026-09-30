#!/usr/bin/env python3
"""Verify real Engram --run-due fails closed when adapter policy control errors."""
from __future__ import annotations
import http.server, json, os, socket, subprocess, sys, tempfile, threading, time
from pathlib import Path
PIN="3a43667deec4a680b42f3e880d7d6bac3baf0746"
SCHEDULED="mcp_atento_browser_scheduled_effect"; INTERACTIVE="mcp_atento_browser_interactive_effect"
SECRET="BROWSER_PROVIDER_SECRET_DO_NOT_LEAK"; HERE=Path(__file__).resolve().parent
class Provider(http.server.BaseHTTPRequestHandler):
 calls=0; tools_seen=[]; trace=[]
 def do_POST(self):
  body=json.loads(self.rfile.read(int(self.headers.get("Content-Length","0")))); Provider.calls+=1
  Provider.trace.append(body); messages=body.get("messages",[]); results=sum(m.get("role")=="tool" for m in messages)
  if results:
   message={"role":"assistant","content":"deterministic policy failure observed"}; finish="stop"
  else:
   names=[x["function"]["name"] for x in body.get("tools",[])]; Provider.tools_seen.append(names)
   if SCHEDULED not in names or INTERACTIVE in names: self.send_error(500,"effective toolset mismatch"); return
   args={"destination":"https://example.test/form","action":"click","selector":"#save","origin":"interactive"}
   message={"role":"assistant","content":"","tool_calls":[{"id":"policy-failure-call","type":"function","function":{"name":SCHEDULED,"arguments":json.dumps(args)}}]}; finish="tool_calls"
  data=json.dumps({"id":"probe","object":"chat.completion","created":int(time.time()),"model":body.get("model","probe"),"choices":[{"index":0,"message":message,"finish_reason":finish}],"usage":{"prompt_tokens":1,"completion_tokens":1,"total_tokens":2}}).encode()
  self.send_response(200); self.send_header("Content-Type","application/json"); self.send_header("Content-Length",str(len(data))); self.end_headers(); self.wfile.write(data)
 def log_message(self,*a): pass

def main():
 if len(sys.argv)!=3: raise SystemExit(f"usage: {sys.argv[0]} ENGRAM_CHECKOUT OUTPUT_DIR")
 candidate=Path(sys.argv[1]).resolve(); out=Path(sys.argv[2]).resolve(); out.mkdir(parents=True,exist_ok=True)
 actual=subprocess.check_output(["git","-C",str(candidate),"rev-parse","HEAD"],text=True).strip()
 if actual!=PIN: raise SystemExit(f"pin mismatch {actual}")
 server=http.server.ThreadingHTTPServer(("127.0.0.1",0),Provider); threading.Thread(target=server.serve_forever,daemon=True).start()
 start=time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()); t0=time.monotonic()
 with tempfile.TemporaryDirectory(prefix="atento-policy-fail-") as td:
  home=Path(td)/"home"; home.mkdir(); driver_trace=out/"driver-effects.jsonl"; authority_trace=out/"authority-records.jsonl"; provider_trace=out/"provider-trace.json"
  driver_trace.write_text(""); authority_trace.write_text("")
  now=int(time.time()*1000); aid="agent-atento-probe"
  agent={"id":aid,"name":"probe","charter":"authority fail-closed probe","model":"","provider":"","base_url":"","api_key":"","effort":"","allowed_tools":[SCHEDULED],"home_project":None,"autonomy_policy":None,"color":"","emoji":"","created_ms":now,"updated_ms":now}
  (home/"agents.json").write_text(json.dumps([agent]))
  job={"id":"atento-policy-control-failure","name":"policy-control failure","payload":{"title":"Test authority-control fail-closed behavior","detail":"Use only the deterministic local Atento adapter."},"recurrence":{"kind":"once","at_ms":now-5000},"next_fire_ms":now-1000,"created_ms":now-10000,"last_fire_ms":None,"last_task_id":None,"agent_id":aid}
  (home/"jobs.json").write_text(json.dumps([job]))
  mcp=[]
  for origin in ("interactive","scheduled"):
   env={"PYTHONPATH":str(HERE),"ATENTO_ORIGIN":origin,"BROWSER_PROVIDER_SECRET":SECRET,"ATENTO_DRIVER_TRACE":str(driver_trace),"ATENTO_AUTHORITY_TRACE":str(authority_trace)}
   if origin=="scheduled": env["ATENTO_POLICY_FAIL"]="1"
   mcp.append({"name":f"atento_browser_{origin}","command":sys.executable,"args":["-u",str(HERE/"mcp_server_policy_probe.py")],"env":env,"cwd":str(HERE),"trusted":True})
  (home/"mcp.json").write_text(json.dumps(mcp))
  port=server.server_address[1]; config={"provider":{"kind":"openai","base_url":f"http://127.0.0.1:{port}/v1","model":"probe","effort":""},"embed":{"kind":"trigram","model_dir":""},"security":{"disabled_tools":["browser_click","browser_type"]}}
  (home/"config.json").write_text(json.dumps(config))
  env=os.environ.copy(); env.update({"ENGRAM_HOME":str(home),"ENGRAM_LLM_API_KEY":"local-probe-only","ENGRAM_IDLE_SECS":"1"})
  cmd=["cargo","run","--offline","--features","http","-p","engramd","--","--run-due"]
  p=subprocess.run(cmd,cwd=candidate,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180); (out/"run-due.log").write_text(p.stdout)
  tasks=json.loads((home/"tasks.json").read_text()) if (home/"tasks.json").exists() else []
  if p.returncode or len(tasks)!=1: raise SystemExit(f"run-due did not create exactly one task: exit={p.returncode}, tasks={len(tasks)}")
  receipt=tasks[0]; steps=(receipt.get("run") or {}).get("steps") or []
  if len(steps)!=1 or steps[0].get("tool")!=SCHEDULED: raise SystemExit(f"unexpected task tool evidence: {steps}")
  if "AuthorityControlUnavailable" not in steps[0].get("observation",""): raise SystemExit(f"policy error did not reach task receipt: {steps[0]}")
  audit=[json.loads(x) for x in authority_trace.read_text().splitlines() if x.strip()]
  effects=[json.loads(x) for x in driver_trace.read_text().splitlines() if x.strip()]
  if len(audit)!=1 or audit[0].get("decision")!="control_error" or audit[0].get("origin")!="scheduled": raise SystemExit(f"wrong authority audit trace: {audit}")
  if effects: raise SystemExit(f"driver executed despite control error: {effects}")
  if receipt.get("status")!="done": raise SystemExit(f"unexpected task status: {receipt.get('status')}")
  if SECRET in p.stdout or SECRET in json.dumps(receipt): raise SystemExit("test credential leaked to daemon output/receipt")
  provider_trace.write_text(json.dumps(Provider.trace,indent=2)+"\n")
  if SECRET in provider_trace.read_text(): raise SystemExit("test credential leaked to provider-visible context")
  server.shutdown()
  for n in ("run-due.log","provider-trace.json","driver-effects.jsonl","authority-records.jsonl","receipt.json"):
   if not (out/n).exists(): (out/n).write_text(json.dumps(receipt,indent=2)+"\n" if n=="receipt.json" else "")
  (out/"receipt.json").write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
  elapsed=time.monotonic()-t0
  summary=["PROBE=Engram RP-AUTH-01 policy-control failure integration","PIN_EXPECTED="+PIN,"PIN_ACTUAL="+actual,"START_UTC="+start,"ENTRYPOINT=real engramd --run-due with one due job","TREATMENT=scheduled adapter policy hook raises before authorization","EFFECTIVE_TOOLS=scheduled MCP identity only; native browser tools disabled","MODEL_ORIGIN_ARGUMENT=interactive; trusted authority origin=scheduled","POLICY_RESULT=AuthorityControlUnavailable returned into Engram task receipt","AUTHORITY_AUDIT=control_error on scheduled origin","DRIVER_EFFECTS=0","PROVIDER=deterministic loopback; external inference=NO","REAL_BROWSER=NO","TEST_CREDENTIAL_LEAK=NOT_OBSERVED",f"PROVIDER_CALLS={Provider.calls}",f"WALL_SECONDS={elapsed:.3f}","RESULT=PASS_WITH_SCOPE","RESIDENT_TICK=NOT_RUN","CANDIDATE_QUALIFIED=NO"]
  (out/"summary.txt").write_text("\n".join(summary)+"\n"); print("\n".join(summary)); return 0
if __name__=="__main__": raise SystemExit(main())
