## 2026-10-03 - Avoid `statistics.mean` in tight Python loop aggregations
**Learning:** Python's `statistics.mean` adds significant overhead (~45x slower than direct `sum/len` arithmetic) due to type conversions and iterator checks. Additionally, computing percentiles on the same list repeatedly sorts it O(N log N) times unless pre-sorted.
**Action:** Use `sum(values) / len(values)` for list-of-float averages and pass `is_sorted=True` when reusing sorted numeric lists.
