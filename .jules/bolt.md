# Bolt's Journal

## 2026-10-22 - Pre-sorting metric values in evaluation scoring
**Learning:** In evaluation harness runs, percentile metrics (p50, p95) are computed repeatedly for the same value lists across overall, suite, and agent scope aggregations. Passing unsorted lists to `_percentile` triggers redundant $O(N \log N)$ sorting passes.
**Action:** Always pre-sort value lists once per group before calculating multiple percentiles, and short-circuit empty collection operations in turn scoring.
