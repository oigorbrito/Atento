## 2026-09-30 - Invalidate Pending Enrollment Challenges on Supersede and Bound Subject Re-enrollment
**Vulnerability:** Pending enrollment challenges remained valid and completable even after a new enrollment challenge was issued for the same subject, or if the subject was already bound.
**Learning:** Enrollment state machines in SQLite must explicitly mark older pending challenge rows as `SUPERSEDED` when creating new challenges, and must re-verify that the subject is not already bound in `telegram_principals` within the `complete_enrollment` transaction before inserting.
**Prevention:** Always mark stale state as superseded when issuing new state tokens and perform double-checks on principal binding constraints within the completing database transaction.
