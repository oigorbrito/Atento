## 2026-10-03 - Prevent Unhandled String Encoding Exceptions at Security Boundaries
**Vulnerability:** External input containing non-ASCII characters in webhook secret headers or identity token payloads caused unhandled Python runtime exceptions (`TypeError` in `hmac.compare_digest` and `UnicodeEncodeError` in `.encode("ascii")`) instead of domain-level rejection exceptions.
**Learning:** `hmac.compare_digest` in Python 3 raises `TypeError` when comparing strings with non-ASCII characters, and `.encode("ascii")` raises `UnicodeEncodeError`.
**Prevention:** Always compare secrets as UTF-8 encoded `bytes` via `.encode("utf-8")` and validate token payload string character sets using regex (`_TOKEN_PART_RE.fullmatch`) before ASCII encoding.
