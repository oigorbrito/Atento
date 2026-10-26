# Bolt's Journal - Critical Performance Learnings

## 2026-03-30 - Python statistics.mean Exact Fraction Bottleneck
**Learning:** Python's standard library `statistics.mean` converts float items into exact fractions using `float.as_integer_ratio()` to maintain arbitrary precision exact rational sums. When calculating mean scores over large benchmark evaluation datasets, this introduces an unexpected ~78x slowdown compared to standard floating point addition (`sum(vals) / len(vals)`).
**Action:** Prefer `sum(values) / len(values)` for float score/metric averaging in performance-sensitive evaluation and benchmark routines instead of `statistics.mean`.
