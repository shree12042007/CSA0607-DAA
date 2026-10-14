# Task 12 – Day-4 Design Challenge: Re-evaluate and Adapt the Design (8 Marks)

**New requirement:** 50,000 searches per hour on 1,000,000 records; new records only once per day.
Load: 50,000 / 3,600 ≈ **13.9 searches per second**, i.e. **1.2 million searches per day**.
Measured figures used below come from `Task_9_Experimental_Performance/results.json` (n = 10⁶, 50 % successful / 50 % unsuccessful queries; single core).

---
## A. Impact Analysis (2 marks)

**What changed.** In the original problem we did not know how often searches happen, so preprocessing and searching were judged together on a "few lookups" basis. Now (i) the search volume is known and very large (k = 1.2 × 10⁶ per day), and (ii) the data are essentially **static**: they change once per day.

**Assumptions affected.**
* *"Preprocessing must be cheap relative to the search work"* – no longer true; the preprocessing cost is paid **once per day** and shared by 1.2 million searches. Sorting (0.6 s) or building a hash table (3.6 s) costs 0.5 µs / 3 µs per search when amortised – negligible.
* *"Updates may interleave with searches"* – no longer true; the index can be built offline in an update window and then used read-only, which also means no locking.
* *"Per-search cost is not critical"* – now it is: total search work = k × cost per search.

**Why search frequency matters.** Total cost = P(n) + k·C(n). For linear search this is k·n/2 = 1.2 × 10⁶ × 5 × 10⁵ ≈ **6 × 10¹¹ comparisons/day**; for binary ≈ 2.4 × 10⁷; for hashing ≈ 1.7 × 10⁶ (+ build 10⁶).

**Why the low update frequency helps.** Structures that are expensive to build but fast to query (sorted array, hash table) become attractive, because their build cost is amortised over a full day of queries and does not have to be repeated after every insertion (the weak point of sorted arrays, where each insertion would cost Θ(n)).

---
## B. Evaluation of the Original Design (2 marks)

Original recommendation: sort once + binary search.

* **Expected behaviour at 50,000 searches/hour.** 20 comparisons and ≈ 9.5 µs per search ⇒ 13.9 searches/s use **0.013 %** of one core; ≈ 11.4 s of CPU per day for all searches. The requirement is met with an enormous margin.
* **Is the preprocessing cost acceptable?** Yes: 0.61 s sort (once per day) and 0.2 – 0.5 s to incorporate a day's new records (1,000 records, measured) – both trivial against a 24-hour period.
* **Could another approach give better overall performance?**
  * *Linear search (for reference):* 59.7 ms per search ⇒ **82.9 % of one core is busy just on searching** (≈ 19.9 CPU-hours per day) – no headroom for peaks (queue build-up), slower hardware or concurrency, and the cost grows linearly with database size. **Rejected.**
  * *Hash table:* ≈ 1.6 µs per search (≈ 5.8× faster than binary) and incremental insertion of 1,000 new records in 1.4 ms (vs 200–500 ms to maintain the sorted array). Total daily cost 5.6 s vs 12.0 s. Costs: 3.6 s build, more memory, no ordering, theoretical Θ(n) worst case.

| Daily cost, n = 10⁶, k = 1.2 M (measured, Python) | Avg search | CPU use of one core | Prep/day | Search/day | Total/day |
|---|---|---|---|---|---|
| Linear | 59.7 ms | 82.9 % | 0 | 71,606 s | 71,606 s |
| Binary + sort | 9.46 µs | 0.013 % | 0.61 s | 11.35 s | 11.97 s |
| Hash | 1.63 µs | 0.002 % | 3.63 s | 1.96 s | 5.59 s |

*Honest note:* the original design still *works*; the question is whether a better design exists. It does, but by an absolute margin of seconds per day, not orders of magnitude.

---
## C. Adaptation or Redesign (2 marks)

**Decision: MODIFY.** The original strategy family (preprocess once, then search fast) is kept, but the data structure is changed from a *sorted array + binary search* to a **hash index (chaining, prime m, load factor ≈ 0.75) as the primary exact-match lookup**, rebuilt/updated in the daily update window.

**What changes**
1. Search: `BinarySearch` → `HashSearch` (one hash computation + scan of one short chain).
2. Daily maintenance: instead of re-sorting/merging (Θ(n log n) or Θ(n + k)), the new k records are **inserted in O(k)** (1.4 ms for 1,000); only if α would exceed ≈ 0.75 is the table rebuilt with a larger prime m (Θ(n), once, amortised).
3. Index is read-only during the day ⇒ it can be shared by many search threads without locks; the update runs on a copy and is swapped in atomically.
4. If the administration still needs **ordered/range queries**, keep the sorted array as a secondary index (cost: 0.6 s/day) – hashing cannot answer them.
5. Use a universal/prime-modulus hash (not `K mod 2^j`) so patterns in registration numbers (e.g. year + department prefix) cannot create long chains.

**Effect on complexity**
| | Original | Modified |
|---|---|---|
| Search (average) | Θ(log n) ≈ 19–20 comparisons | **Θ(1)** ≈ 1.375 comparisons |
| Search (worst) | Θ(log n) | Θ(n) theoretical (observed chain ≤ 7) |
| Daily build | Θ(n log n) | Θ(n) (or Θ(k) incremental) |
| Daily update of k new records | Θ(n + k) | **Θ(k)** |
| Space | Θ(n) | Θ(n) with larger constant (m ≈ 1.33 n buckets + chains) |
| k searches per day | Θ((n+k) log n) | **Θ(n + k)** |

---
## D. Evidence-Based Defence (2 marks)

* **Complexity:** total daily cost goes from (n + k) log₂ n ≈ (10⁶ + 1.2×10⁶) × 20 ≈ 4.4 × 10⁷ basic operations to n + 1.375 k ≈ 10⁶ + 1.65 × 10⁶ = 2.7 × 10⁶ – about 16× fewer.
* **Experiment:** measured daily CPU 5.6 s (hash) vs 12.0 s (binary) vs 71,606 s (linear); search latency 1.6 µs vs 9.5 µs vs 59.7 ms; daily update 1.4 ms vs 200–500 ms.
* **Search frequency:** 13.9 searches/s – linear search consumes 83 % of a core (unacceptable, no peak headroom); binary and hash use ≤ 0.013 %.
* **Preprocessing cost:** hash build 3.6 s is paid once per day and is only ≈ 3 µs per search when amortised over 1.2 M searches; break-even against linear search is just ≈ 61 searches.
* **Dataset size:** the advantage of an O(1) structure over O(log n) grows slowly with n (20 → 30 comparisons at 10⁹ records), while linear search keeps growing linearly.
* **Trade-offs:** (a) extra memory (≈ 1.3 M buckets + 1 M entries); (b) no ordering ⇒ keep the sorted index if range queries are needed; (c) theoretical Θ(n) worst case ⇒ prime modulus / universal hashing and load-factor monitoring; (d) the performance gain over binary search is real (≈ 6× per search, ≈ 200× cheaper updates) but small in absolute terms – **if the administration needs ordered queries and does not need the extra speed, retaining the original binary-search design is also technically defensible**; what is *not* defensible is falling back to linear search.
* **Caveat on measurements:** all timings are from one Python run on one machine; the hash build (3.6 s) is slower than the C-implemented `sorted` (0.6 s) partly because of implementation language (see Task 10), so a compiled implementation would shift the build-time comparison in favour of hashing. This was not tested.

**Final decision:** *Modify* – hash index for exact registration-number lookups, built/updated once per day, with the sorted index kept only if ordered queries are required.
