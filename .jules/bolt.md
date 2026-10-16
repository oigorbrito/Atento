## 2026-09-30 - Dict Keys Comparison vs Intermediate Set Allocation

**Learning:** Comparing `dict.keys() == frozenset_object` in Python compares dictionary keys directly against a `frozenset` without allocating a temporary `set` object, avoiding unnecessary heap allocations in hot verification/schema-validation loops.

**Action:** Prefer `dict_obj.keys() == canonical_frozenset` over `set(dict_obj) == canonical_frozenset` in hot path schema/claims validation.
