## 2026-10-03 - Timing Side-Channel in Enrollment Challenge Verification
**Vulnerability:** In `TelegramEnrollmentStore.complete_enrollment`, challenge lookups and status checks failed before computing/comparing code digests, leaking timing signals on whether a challenge ID exists or is in PENDING state.
**Learning:** Returning early on database lookup misses avoids constant-time operations when validating authentication tokens or codes, exposing challenge existence or state via response timing.
**Prevention:** Always compute and compare against a constant dummy hash even when challenge or user record lookups fail before raising rejection exceptions.
