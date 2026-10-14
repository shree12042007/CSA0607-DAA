# Task 3 – Derive the Time-Complexity Function Mathematically (6 Marks)

**Input size:** n = number of student records. **Basic operation:** key comparison, C(n) = number of times it runs. Keys are distinct.

---
## 3.1 Linear search

*Worst case.* Key in last position or absent: the loop runs for i = 0…n−1, one comparison per iteration:

C_worst(n) = Σ_{i=0}^{n−1} 1 = **n**

*Best case.* Key at position 0: C_best(n) = **1**.

*Average case – successful search.* Assume the key is equally likely to be at any of the n positions (probability 1/n each). Finding the key at position i (1-indexed) costs i comparisons:

C_avg(n) = (1/n) Σ_{i=1}^{n} i = (1/n) · n(n+1)/2 = **(n+1)/2**

*Average with success probability p* (0 ≤ p ≤ 1; with probability 1−p the key is absent and costs n):

C_avg(n) = p·(n+1)/2 + (1−p)·n

*Preprocessing:* none, P(n) = 0.
*Total for k searches:* T_lin(n, k) = k · (n+1)/2 (successful) … k·n (unsuccessful) ⇒ **Θ(k·n)**.

*Check against data (n = 1,000,000):* theory (n+1)/2 = 500,000.5; measured 480,744 (100 random successful queries; the sampling standard deviation is ≈ n/√(12·100) ≈ 28,900, so the result is within one standard deviation). Unsuccessful: theory 1,000,000, measured 1,000,000.

---
## 3.2 Binary search (recursive) with sorting

### Search cost
Each call performs one comparison and recurses on at most ⌊n/2⌋ records (derivation in Task 6–7), giving C(n) = C(⌊n/2⌋) + 1, C(1) = 1 ⇒

C_worst(n) = **⌊log₂ n⌋ + 1**

*Average case (successful).* Take n = 2^k − 1 so that the comparison tree is a perfect binary tree of k levels. Level i (i = 1..k) holds 2^(i−1) records, each found after i comparisons:

C_avg(n) = (1/n) Σ_{i=1}^{k} i·2^(i−1) = ((k−1)·2^k + 1) / (2^k − 1) ≈ k − 1 + k/n

so **C_avg(n) ≈ log₂(n+1) − 1** (about one comparison less than the worst case).
For n = 10⁶: log₂(10⁶+1) − 1 = 18.93; measured 18.91.

### Preprocessing cost (sorting)
Any comparison sort needs at least log₂(n!) ≈ n log₂ n − 1.44 n comparisons, and merge sort achieves it: its recurrence S(n) = 2S(n/2) + (n−1) gives S(n) ≈ n log₂ n − n + 1.
Therefore **P(n) = Θ(n log n)**. (Our implementation uses Python's `sorted`, a Timsort, which is Θ(n log n) worst-case.)

### Total cost for k searches
T_bin(n, k) = P(n) + k · C(n) = **n log₂ n + k log₂ n = (n + k) log₂ n**, i.e. Θ((n + k) log n).

---
## 3.3 Hash table with separate chaining

Let m = number of buckets, load factor α = n/m (≈ 0.75 here). Assume simple uniform hashing: every key is equally likely to go to any of the m buckets.

### Preprocessing
Building: n insertions, each = one modulus + one append = O(1) ⇒ **P(n) = Θ(n)** (expected, and also worst case for appending at chain tail with a stored tail pointer / list append). Extra space Θ(n + m).

### Unsuccessful search
The whole chain is scanned. Expected chain length = n/m = α, so
**C_fail = α = 0.75** comparisons. (Measured: 0.66, 0.84, 0.80, 0.71.)

### Successful search
Consider the key that was the i-th to be inserted. The comparisons needed = 1 + (number of keys inserted *before* it that fall in the same chain). Each of the i−1 earlier keys lands in this chain with probability 1/m:

E[C | key i] = 1 + (i−1)/m

Averaging over i = 1..n:

C_avg = (1/n) Σ_{i=1}^{n} (1 + (i−1)/m) = 1 + (n−1)/(2m) = **1 + α/2 − α/(2n) ≈ 1 + α/2 = 1.375**

(measured: 1.34, 1.45, 1.40, 1.28). This does not depend on n ⇒ **O(1)** average.

### Worst case
If all n keys fall into the same chain (degenerate hash function): C_worst = n.

### Total cost for k searches
T_hash(n, k) = n + k·(1 + α/2) = **Θ(n + k)** expected.

---
## 3.4 Overall cost summary (preprocessing + searching)

| Algorithm | Preprocessing | One search (avg) | k searches in total |
|-----------|---------------|------------------|---------------------|
| Linear | 0 | (n+1)/2 | k(n+1)/2 → Θ(kn) |
| Binary | ≈ n log₂ n | ≈ log₂ n − 1 | n log₂ n + k log₂ n → Θ((n+k) log n) |
| Hash | ≈ n (insertions) | ≈ 1 + α/2 | n + 1.375k → Θ(n + k) |

**Break-even (in comparisons).** Binary search beats linear search when n log₂ n + k log₂ n < k n/2, i.e. k > n log₂ n / (n/2 − log₂ n) ≈ 2 log₂ n. For n = 10⁶ that is only k ≈ 40 searches in the comparison-count model (measured in time: 10 searches). Hashing beats linear when n + 1.375k < kn/2, i.e. k ≳ 2 – 3 searches in the count model (the measured time break-even is larger, 61 searches, because inserting into a hash table costs more *time* per element than a comparison – see Task 10).
