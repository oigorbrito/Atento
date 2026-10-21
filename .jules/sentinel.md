# Sentinel Journal

## 2026-10-03 - Principal Revocation Actor Authorization Gap
**Vulnerability:** `TelegramEnrollmentStore.revoke` accepted `actor_principal_id` without verifying that the authorizing actor was an active, unrevoked principal in `telegram_principals`. This allowed revoked or non-existent actors to revoke other active principals.
**Learning:** Even when operations require an `actor_principal_id` parameter for audit trail logging, the actor's active status must be checked against host principal state in the database before granting administrative capabilities like revocation.
**Prevention:** In host identity stores, always validate `actor_principal_id` in database transactions with `WHERE principal_id = ? AND revoked_at IS NULL` prior to performing lifecycle changes.
