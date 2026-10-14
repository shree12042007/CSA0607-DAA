# Task 11 – Recommend and Defend the Final Design (4 Marks)

## Recommendation (original problem, before the Day-4 change)
**Sort the registration numbers once and use binary search (recursive/iterative) on the sorted index.**

## Why this and not the alternatives
| Criterion | Linear | **Binary + sort** | Hash |
|-----------|--------|-------------------|------|
| Search cost (n = 10⁶, measured) | 0.5 million comparisons, 39–80 ms | **≈ 19–20 comparisons, ≈ 9–10 µs** | ≈ 1.3 comparisons, ≈ 1.6–1.9 µs |
| Preprocessing (n = 10⁶, measured) | none | **0.61 s** | 3.63 s |
| Break-even vs linear | – | **≈ 10 searches** | ≈ 61 searches |
| Worst-case guarantee | Θ(n) | **Θ(log n), always** | Θ(n) (theoretical; observed longest chain 7) |
| Extra memory | none | **none (sorted copy/ index only)** | Θ(n) buckets + chains |
| Supports ordered/range queries ("all students 230100–230199", "next registration number") | no | **yes** | no |
| Supports updates | trivial | needs re-sort / merge | trivial |

* **Theoretical efficiency:** Θ(n log n) preprocessing + Θ(log n) per search, i.e. Θ((n + k) log n) for k searches.
* **Experimental performance:** for n = 10³ → 10⁶ the average search comparisons rose from 9 to 19 (theory 8.97 → 18.93) and the search time from 4.3 to 10.2 µs, whereas linear search rose from 43 µs to 39 ms.
* **Preprocessing cost:** 0.14 ms (10³) … 0.61 s (10⁶); recovered after ≈ 10 searches at n = 10⁶.
* **Why not simply "lowest Big-O"?** Hashing has the lowest search complexity, but in our measurements it had the largest preprocessing cost (3.6 s at 10⁶), needs extra memory, gives no ordered access and has a Θ(n) worst case. Without information about how many searches will be made, binary search is the most balanced choice: tiny preprocessing, a hard logarithmic worst-case bound, no extra memory, and the sorted order is useful for administration (listing, ranges). Linear search is only justified for a one-off lookup on unsorted data (fewer than ≈ 10 searches).
* **Trade-offs / limitations:** (i) the sorted order must be maintained when records are added (re-sort or merge, Θ(n) – 0.2–0.5 s for a day's update at n = 10⁶ in our test); (ii) it is slower than hashing per search by a constant ≈ 5×; (iii) the result applies to in-memory data – for disk-resident data a B-tree variant of the same idea would be used.
* **Practical as the database grows?** Yes: 10³ → 10⁶ (×1000) costs only 10 extra comparisons; 10⁹ records would need ≈ 30 comparisons.
