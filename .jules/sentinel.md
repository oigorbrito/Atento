## 2026-10-03 - Active Principal Verification in Authority State Transitions
**Vulnerability:** In `TelegramEnrollmentStore.revoke`, `actor_principal_id` was accepted and written to audit logs without verifying that the revoking actor was an active, non-revoked principal in `telegram_principals`.
**Learning:** Functions accepting `actor_principal_id` for administrative actions must validate actor state against `telegram_principals` in addition to checking non-empty strings.
**Prevention:** Whenever adding host authority or revocation methods that take an `actor_principal_id`, ensure active status (`revoked_at IS NULL`) is checked in `telegram_principals` before applying changes.
