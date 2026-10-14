# Task 10 – Compare Theory with Experimental Behaviour (4 Marks)

![Theory vs experiment](../Report/Tables_and_Graphs/graph4_theory_vs_experiment.png)

## 10.1 Does the observed growth agree with the derived complexity? – comparison counts

| n | Linear theory (n+1)/2 | Linear measured | Binary theory log₂(n+1)−1 | Binary measured | Hash theory 1+α/2 | Hash measured |
|---|---|---|---|---|---|---|
| 1,000 | 500.5 | 440.1 | 8.97 | 9.08 | 1.375 | 1.34 |
| 10,000 | 5,000.5 | 5,094.6 | 12.29 | 12.34 | 1.375 | 1.45 |
| 100,000 | 50,000.5 | 49,256.0 | 15.61 | 15.75 | 1.375 | 1.40 |
| 1,000,000 | 500,000.5 | 480,744.5 | 18.93 | 18.91 | 1.375 | 1.28 |

* **Linear:** comparisons grow ×11.6 → ×9.7 → ×9.8 per decade of n, i.e. ≈ ×10 = linear growth. Deviations (−12 % … +2 %) come from using only 100 random queries (standard error ≈ 5.8 % of n/2 – larger at small samples); the unsuccessful search matches the theory exactly (n).
* **Binary:** matches log₂(n+1) − 1 to within 0.15 comparisons; every decade adds ≈ 3.3 comparisons (= log₂ 10), exactly as Θ(log n) predicts; the worst values 10, 14, 17, 20 equal ⌊log₂ n⌋ + 1 exactly – this validates the recurrence solution of Task 7.
* **Hash:** the number of comparisons is flat at ≈ 1.3–1.45 (successful) and ≈ 0.7–0.8 (unsuccessful), matching 1 + α/2 and α; the longest chains (4, 6, 6, 7) confirm that the worst-case Θ(n) does not occur with a prime modulus.

## 10.2 Execution time
| n | Linear (µs/search, succ.) | Binary | Hash | Sort prep (ms) | Hash build (ms) |
|---|---|---|---|---|---|
| 1,000 | 43.0 | 4.26 | 0.91 | 0.14 | 0.95 |
| 10,000 | 543.6 | 5.32 | 1.10 | 2.02 | 12.29 |
| 100,000 | 5,219.6 | 5.69 | 3.79 | 37.59 | 274.40 |
| 1,000,000 | 39,046 | 10.19 | 1.93 | 613.03 | 3,633.09 |

* Linear: time per comparison is ≈ 0.08–0.11 µs at every size, so time ∝ comparisons ∝ n: **theory and experiment agree closely** (×908 in time for ×1000 in n).
* Binary: time grows only ×2.4 for ×1000 in n – consistent with the doubling of comparisons (10 → 20).
* Hash: ≈ constant (0.9 – 3.8 µs, ×2.1 overall).

## 10.3 Where theory and experiment differ, and why
1. **Hash and binary times rise slightly although the theory says "constant"/"log".** At n = 10⁶ the data occupy tens of MB; accesses are random, so CPU-cache misses make each comparison slower than at n = 10³. The big-O model counts comparisons, not memory latency. The 100,000-record hash timing (3.79 µs) is also noisier than neighbouring sizes; timing at the µs scale is affected by garbage collection/OS scheduling – we did not repeat the full run multiple times, so small timing differences between sizes should not be over-interpreted.
2. **Preprocessing grows faster than theory.** Sorting grew ×4,300 for a ×1000 increase in n (n log n predicts ≈ ×2,000) and the hash build ×3,800 (Θ(n) predicts ×1000). The likely causes are cache/memory-allocation effects and Python's garbage collector while creating 1.3 million list objects and 1 million tuples (we did not profile to confirm).
3. **Hash build is *slower* than sorting here although Θ(n) < Θ(n log n).** `sorted()` is implemented in C, whereas our hash-table build is an interpreted Python loop; the constant factor of the implementation (≈ 6×) outweighs the log n factor (≈ 20) at n = 10⁶. This is a property of our implementation language, not of the algorithms; in a compiled implementation the hash build would be expected to be faster, but this was not tested.
4. **Counted vs measured:** the timing runs include the cost of the comparison counter itself (the same overhead for all three algorithms), so absolute times are somewhat inflated, but relative growth is unaffected.

## 10.4 Which algorithm scales best?
Search step: **Hash ≻ Binary ≻ Linear**. Between 10³ and 10⁶ records, linear search becomes ≈ 900× slower while binary becomes ≈ 2.4× slower and hash ≈ 2×. Including preprocessing, binary search pays off after only ≈ 10 searches and hashing after ≈ 61 searches at n = 10⁶ (Task 9/12), so both preprocessing investments are recovered very quickly in any system with repeated lookups.
