# Task 5 – Asymptotic Analysis (3 Marks)

## 5.1 Notation for each algorithm

| Algorithm | Best case | Average case | Worst case | Preprocessing |
|-----------|-----------|--------------|-----------|---------------|
| Linear | Θ(1) | Θ(n) | Θ(n) | none |
| Binary (recursive) | Θ(1) | Θ(log n) | Θ(log n) | Θ(n log n) |
| Hash (chaining) | Θ(1) | Θ(1) expected | Θ(n) | Θ(n) |

**Justification with definitions.**
* Linear, average: (n+1)/2 ≥ n/2 for all n ≥ 1 and (n+1)/2 ≤ n for n ≥ 1, so with c₁ = 1/2, c₂ = 1 and n₀ = 1 we get c₁n ≤ (n+1)/2 ≤ c₂n ⇒ **Θ(n)**. The search function as a whole is **O(n)** and also **Ω(1)** (it always does ≥ 1 comparison), so no single Θ describes *all* inputs – hence the case split.
* Binary: ⌊log₂ n⌋ + 1 ≥ (1/1)·log₂ n for n ≥ 2 and ≤ 2 log₂ n for n ≥ 2 ⇒ **Θ(log n)**; the best case, key in the middle, is Θ(1), so search is O(log n) and Ω(1).
* Hash: 1 + α/2 is a constant (α is held at ≈ 0.75 by choosing m) ⇒ Θ(1) expected; worst case n ⇒ O(n).
* Sorting: Ω(n log n) by the decision-tree lower bound for comparison sorts and O(n log n) by merge sort ⇒ Θ(n log n).

**Order of growth:**  1 ≺ log n ≺ n  (hash ≺ binary ≺ linear for the search step); for the *preprocessing* step: n ≺ n log n.

## 5.2 Behaviour when n becomes very large and the meaning for the university

| n | Linear (avg. comparisons) | Binary (worst) | Hash (avg.) |
|---|---------------------------|----------------|-------------|
| 1,000 | ≈ 500 | 10 | ≈ 1.4 |
| 10,000 | ≈ 5,000 | 14 | ≈ 1.4 |
| 100,000 | ≈ 50,000 | 17 | ≈ 1.4 |
| 1,000,000 | ≈ 500,000 | 20 | ≈ 1.4 |

* Going from 10³ to 10⁶ records (×1000): linear search does **1000× more work**, binary search only **2× more** (10 → 20 comparisons), and hash search **the same** amount.
* A linear search over 10⁶ records performs half a million comparisons per request; a binary search does 20 – a reduction of ~25,000×. Hence linear search is acceptable for a 1,000-record department list but impractical as the university scales to millions of records.
* Because the growth rates are different *orders* (n vs log n vs 1), the constant factors (e.g. the per-comparison speed) cannot rescue the linear algorithm: a computer 100× faster merely postpones the problem by 100× in n.
* The preprocessing is also asymptotically meaningful: sorting grows as n log n, so it is **superlinear**, and a hash build is **linear**. Both are one-time costs which are amortised over the number of searches k. Total growth: linear Θ(kn), binary Θ((n+k) log n), hash Θ(n+k). When k is large (the Day-4 scenario: 1.2 million searches per day) the preprocessing terms become negligible compared with the Θ(kn) term of linear search.
