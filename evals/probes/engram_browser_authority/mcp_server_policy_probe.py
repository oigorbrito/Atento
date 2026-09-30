import json, os, sys
from adapter import AuthorityControlUnavailable, AuthorityDenied, BrowserAuthorityPolicy, BrowserEffectAdapter, BrowserEffectRequest, Grant
DEST="https://example.test/form"; BUTTON="#save"; INPUT="#note"; SECRET="BROWSER_PROVIDER_SECRET_DO_NOT_LEAK"
class Driver:
 def _record(self, event):
  with open(os.environ["ATENTO_DRIVER_TRACE"], "a", encoding="utf-8") as f: f.write(json.dumps(event)+"\n")
 def click(self, *, destination, selector):
  self._record({"action":"click","destination":destination,"selector":selector}); return "clicked"
 def type_text(self, *, destination, selector, text):
  self._record({"action":"type","destination":destination,"selector":selector,"text":text}); return "typed"
policy=BrowserAuthorityPolicy.from_iterables(interactive=[Grant(DEST,"click",BUTTON),Grant(DEST,"type",INPUT)],scheduled=[Grant(DEST,"click",BUTTON)])
def hook(req, policy):
 if os.environ.get("ATENTO_POLICY_FAIL")=="1": raise RuntimeError("policy unavailable")
 return True
adapter=BrowserEffectAdapter(Driver(),policy,policy_hook=hook); origin=os.environ["ATENTO_ORIGIN"]
def send(o): sys.stdout.write(json.dumps(o)+"\n"); sys.stdout.flush()
for line in sys.stdin:
 msg=json.loads(line); method=msg.get("method"); mid=msg.get("id")
 if method=="initialize": send({"jsonrpc":"2.0","id":mid,"result":{"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"serverInfo":{"name":"atento-policy-probe","version":"probe1"}}})
 elif method=="tools/list": send({"jsonrpc":"2.0","id":mid,"result":{"tools":[{"name":"effect","description":"Authority-bound browser action","inputSchema":{"type":"object","properties":{"destination":{"type":"string"},"action":{"type":"string"},"selector":{"type":"string"},"text":{"type":"string"},"origin":{"type":"string"}},"required":["destination","action","selector"]}}]}})
 elif method=="tools/call":
  a=msg["params"]["arguments"]; req=BrowserEffectRequest("naia",origin,a["destination"],a["action"],a["selector"],a.get("text"))
  try:
   result=adapter.execute(req); result["authority_record"]=dict(adapter.audit[-1].model_visible()); send({"jsonrpc":"2.0","id":mid,"result":{"content":[{"type":"text","text":json.dumps(result)}]}})
  except (AuthorityDenied,AuthorityControlUnavailable) as e:
   if adapter.audit:
    with open(os.environ["ATENTO_AUTHORITY_TRACE"],"a",encoding="utf-8") as f: f.write(json.dumps(dict(adapter.audit[-1].model_visible()))+"\n")
   send({"jsonrpc":"2.0","id":mid,"result":{"isError":True,"content":[{"type":"text","text":type(e).__name__+":"+str(e)}]}})
