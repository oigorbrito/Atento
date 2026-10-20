## 2025-05-18 - Avoid duplicate set operations in metrics calculation
**Learning:** In precision/recall evaluation routines like `_set_prf`, performing set intersection `e & a` multiple times inside the same function creates redundant set allocations and traversals, causing unnecessary CPU and memory overhead during large benchmark runs.
**Action:** Store the length of set intersection `common = len(e & a)` once when calculating both precision and recall.
