## 2026-10-03 - String Encoding & Type Failures in Cryptographic Helper Input Validation
**Vulnerability:** Passing unvalidated non-ASCII strings into `hmac.compare_digest` or calling `.encode("ascii")` on untrusted input tokens caused unhandled `TypeError` or `UnicodeEncodeError` crashes instead of failing closed with domain rejection exceptions.
**Learning:** Python's `hmac.compare_digest` raises `TypeError` when comparing strings containing non-ASCII characters, and `.encode("ascii")` raises `UnicodeEncodeError` when non-ASCII chars are present before regex format validation.
**Prevention:** Always validate character set and format (e.g. using ASCII regex matchers) on untrusted header strings and token parts before performing cryptographic operations or ASCII encoding.
