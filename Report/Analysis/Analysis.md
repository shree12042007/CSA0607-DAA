# Combined Analysis (Tasks 2–7 and 10)

# Task 2 – Identify the Basic Operation (2 Marks)

In all three algorithms the **basic operation is the comparison of the search key K with a stored registration number** (`A[i] = K`, `A[mid] = K`, `key = K`). It is the operation that appears in the innermost loop / recursive step; everything else (index increments, `mid` computation, returning) is executed at most as many times as the comparison.

| Algorithm | Where it occurs | How its count changes with n |
|-----------|-----------------|------------------------------|
| Linear search | the `if A[i] = K` test inside the `for` loop | Executed once for every record examined. If the key is at position p it runs p times; if absent it runs n times. So the count grows **proportionally to n** – a 10× larger database costs about 10× more comparisons. |
| Binary search | the `if A[mid] = K` test at the top of each recursive call | Each call halves the range, so the number of calls (= comparisons) is about log₂ n. A 1000× larger database (10³→10⁶) adds only ~10 more comparisons. |
| Hash search | the `if key = K` test while scanning the single chain `T[K mod m]` | Only the chain length matters. With load factor α = n/m ≈ 0.75 the expected chain length is constant, **independent of n**. |

**Why this operation is appropriate.**
1. It is executed in the innermost repeated part, so it dominates running time as n grows (loop bookkeeping is proportional to it).
2. Each comparison of two 9-digit integers takes a roughly constant time, so *count of comparisons* is directly proportional to running time. This makes the count machine-independent, which is why the experiments (Task 9) record comparisons as well as seconds.
3. It is the only operation shared by all three algorithms, so it allows a fair comparison.

**Cost outside the search – preprocessing.** For algorithms 2 and 3 the preprocessing has its own basic operations: the *key comparison inside the sort* (Θ(n log n) comparisons) for binary search, and the *insertion/hash computation* (n of them) for hashing. These are included in Task 3 so the total cost is not understated.


---

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


---

# Task 4 – Best, Average and Worst-Case Behaviour (4 Marks)

## 4.1 Linear search
| Case | Input condition | Operations | Why |
|------|-----------------|-----------|-----|
| **Best** | The requested registration number is the **first** record in the file | 1 comparison | The loop exits at the first iteration. |
| **Average** | Key present and equally likely at any position (or present with probability p) | (n+1)/2 for success; p(n+1)/2 + (1−p)n in general | On average half of the list is scanned before the key is hit. |
| **Worst** | Key is the **last** record, or **not in the database** | n comparisons | No early exit is possible; every record must be examined to prove absence. |

*Observation:* the worst case is not rare – every failed lookup (e.g. a typo in a registration number) is a worst case. Measured at n = 10⁶: successful ≈ 4.8×10⁵ comparisons, unsuccessful = 10⁶.

## 4.2 Binary search
| Case | Input condition | Operations | Why |
|------|-----------------|-----------|-----|
| **Best** | Key is exactly the **middle** element of the sorted array | 1 comparison | Found in the first call. |
| **Average** | Key present, each position equally likely | ≈ log₂(n+1) − 1 | About half of the keys lie in the bottom level of the decision tree, which has the largest depth, so the average is only ≈1 below the worst. |
| **Worst** | Key absent, or located at the deepest level of the decision tree | ⌊log₂ n⌋ + 1 | The range must be halved until it is empty/one element. |

*Observation:* binary search has little spread – best 1, average ≈ 19, worst 20 for n = 10⁶. Important precondition: the array must remain sorted; otherwise results are wrong.

## 4.3 Hash table (chaining)
| Case | Input condition | Operations | Why |
|------|-----------------|-----------|-----|
| **Best** | Bucket is empty (unsuccessful search, 0 comparisons) or the key is first in its chain (1 comparison) | 0–1 | The hash directly points to the answer. |
| **Average** | Keys spread uniformly, load factor α | successful 1 + α/2 ≈ 1.375; unsuccessful α = 0.75 | Chain length is Poisson-like with mean α; independent of n. |
| **Worst** | All keys collide into one bucket (poor hash function, e.g. m sharing factors with a pattern in the registration numbers, or an adversarial key set) | n comparisons | The table degenerates into a linked list = linear search. |

*Observation:* the largest chain observed in the experiments was 4, 6, 6 and 7 for n = 10³…10⁶ – the worst case is theoretical for a well-chosen prime modulus (and can be avoided with a universal hash function).


---

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


---

# Task 6 – Formulate the Recurrence Relation (3 Marks)

The recursive algorithm is the **recursive binary search** (Algorithm 2):

```
BinarySearch(A, K, low, high)
  if low > high then return -1                  // (1) base case
  mid ← ⌊(low + high)/2⌋                        // (2) O(1) work
  if A[mid] = K then return mid                 // (3) 1 comparison
  else if K < A[mid] then return BinarySearch(A, K, low, mid-1)   // (4a) left call
  else return BinarySearch(A, K, mid+1, high)                    // (4b) right call
```

Let T(n) = number of key comparisons when the current range `A[low..high]` contains n = high − low + 1 records.

| Component | Identified from the algorithm |
|-----------|-------------------------------|
| **Input size of original problem** | n = high − low + 1, the number of records still under consideration (initially all n records). |
| **Size of the sub-problem** | The left call receives `low..mid-1`: ⌊(n−1)/2⌋ = ⌈n/2⌉ − 1 records. The right call receives `mid+1..high`: ⌊n/2⌋ records. In the worst case it is ⌊n/2⌋ (the larger half). |
| **Number of recursive calls** | **One.** Lines (4a) and (4b) are mutually exclusive (if/else); only one half is searched, the other is discarded. (This is why it is a *decrease*-and-conquer, not a *divide*-and-conquer, algorithm: a = 1, not 2.) |
| **Work outside the recursive call** | Computing `mid`, one comparison `A[mid] = K` (and the `K < A[mid]` decision, counted as the same three-way comparison) ⇒ constant, f(n) = 1. |
| **Base case** | n = 0 (`low > high`): returns immediately with 0 comparisons ⇒ T(0) = 0. (And therefore T(1) = T(0) + 1 = 1: one record needs one comparison.) |

**Putting the pieces together.**  
T(n) = (work outside the call) + (number of calls) × T(size of the subproblem)

> **T(n) = T(⌊n/2⌋) + 1  for n ≥ 1,    T(0) = 0**

for the worst case (key absent or always going to the larger half).  
In asymptotic form, T(n) = T(n/2) + Θ(1), i.e. a = 1, b = 2, f(n) = Θ(1).

*Check with the code:* `binary_search_recursive` returns `idx, c + 1` after the recursive call, i.e. it adds exactly 1 comparison to the result of one smaller call – the same structure as the recurrence.

*Why the best case does not follow this recurrence:* if the key is at `mid`, the algorithm stops before recursing; T_best(n) = 1 – a non-recursive case already covered in Task 4.


---

# Task 7 – Solve the Recurrence Relation (4 Marks)

Recurrence from Task 6:  **T(n) = T(⌊n/2⌋) + 1, n ≥ 1; T(0) = 0** (so T(1) = 1).

## Method 1 – Backward substitution (iteration method)
**Why applicable:** the recurrence has a single recursive term with a simple shrinking argument, so repeated expansion shows a clear pattern. Take n = 2^k (the floors disappear) – the general case follows in Method 2.

T(n) = T(n/2) + 1
     = [T(n/4) + 1] + 1 = T(n/4) + 2
     = [T(n/8) + 1] + 2 = T(n/8) + 3
     …
     = T(n/2^i) + i

The expansion stops when n/2^i = 1, i.e. i = log₂ n. Then

T(n) = T(1) + log₂ n = 1 + log₂ n,

so **T(n) = log₂ n + 1 = Θ(log n)**.

## Method 2 – Substitution method (induction) – exact result for all n
**Claim:** T(n) = ⌊log₂ n⌋ + 1 for all n ≥ 1.
* *Base:* n = 1 ⇒ T(1) = 1 = ⌊log₂ 1⌋ + 1 ✓.
* *Inductive step:* assume the claim for all values < n, n ≥ 2. Then
  T(n) = T(⌊n/2⌋) + 1 = (⌊log₂ ⌊n/2⌋⌋ + 1) + 1.
  For n ≥ 2, ⌊log₂ ⌊n/2⌋⌋ = ⌊log₂ n⌋ − 1, so
  T(n) = (⌊log₂ n⌋ − 1 + 1) + 1 = ⌊log₂ n⌋ + 1 ✓. ∎

## Method 3 – Master Theorem
**Why applicable:** the recurrence has the form T(n) = a·T(n/b) + f(n) with a = 1 ≥ 1, b = 2 > 1 and f(n) = Θ(1) a polynomially bounded positive function.

* a = 1, b = 2 ⇒ n^(log_b a) = n^(log₂ 1) = n⁰ = 1.
* f(n) = Θ(1) = Θ(n^(log_b a)) ⇒ **Case 2** (f(n) = Θ(n^(log_b a) · log⁰ n)).
* Therefore T(n) = Θ(n^(log_b a) · log n) = **Θ(log n)**.

All three methods agree.

## Interpretation
* The recursion depth, and therefore the number of comparisons, grows **logarithmically**: doubling the database adds exactly **one** extra comparison.
* n = 1,000 → ≤ 10; n = 10⁶ → ≤ 20 (measured worst case: 10 and 20 – exact match with ⌊log₂ n⌋ + 1).
* The recursion depth equals the number of comparisons (≤ 20 for a million records), so the call stack is small (Θ(log n) space) and there is no risk of stack overflow.

## Supplementary – the preprocessing recurrence (merge sort)
Sorting for binary search by merge sort: S(n) = 2S(n/2) + Θ(n), S(1) = 0. Master Theorem: a = 2, b = 2 ⇒ n^(log₂ 2) = n and f(n) = Θ(n) ⇒ Case 2 ⇒ **S(n) = Θ(n log n)**. This confirms the preprocessing cost used in Task 3.


---

# Task 10 – Compare Theory with Experimental Behaviour (4 Marks)

![Theory vs experiment](../Tables_and_Graphs/graph4_theory_vs_experiment.png)

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
