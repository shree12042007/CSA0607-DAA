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
