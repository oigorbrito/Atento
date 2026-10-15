# Sentinel Journal - Critical Security Learnings

## 2026-10-03 - Python Boolean-Integer Subtyping in JSON Token Claims
**Vulnerability:** In Python, `isinstance(True, int)` is `True` and `True == 1` is `True`. When validating numeric schema fields in JSON claims (such as `"v": 1`), passing `"v": true` in JSON bypasses `raw["v"] != 1` check unless explicitly checked with `isinstance(val, bool)`.
**Learning:** `json.loads` deserializes JSON booleans to Python `bool` objects. Checks comparing `val != 1` or `val < 1` will fail to catch `True` unless `isinstance(val, bool)` is guarded first.
**Prevention:** Always check `if isinstance(val, bool) or val != 1:` when validating numeric claims from untrusted JSON payloads.
