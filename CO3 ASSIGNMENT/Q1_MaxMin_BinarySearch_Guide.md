# Q1 – Decomposition and Elimination in Ordered Data (6 Marks)

> This file contains the **concept explanation and pseudocode skeleton** to help you and your partner build the complete solution yourselves. It is intentionally incomplete — the derivations, experimental data, and final write-up must be your own work, since both of you will be individually questioned on this in the viva.

---

## Part A — Finding Maximum and Minimum (Tournament / Divide & Conquer Method)

### Naive approach (for comparison)
Scan once for max, once for min → **2(n−1)** comparisons.

### Divide and Conquer idea
Split the array in half, solve each half recursively, then combine.

**Base cases:**
- 1 element → it is both the max and min.
- 2 elements → **one comparison** determines which is max and which is min.

**Why the 2-element base case matters:** if you only had a 1-element base case, every combine step would need 2 comparisons with no savings. Handling pairs directly is what produces the final savings — this is something Student A should be able to explain and justify, not just state.

**Combine step:**
Given `(max1, min1)` from the left half and `(max2, min2)` from the right half:
- overall max = larger of `max1, max2` → 1 comparison
- overall min = smaller of `min1, min2` → 1 comparison
- Total combine cost = 2 comparisons, independent of subproblem size.

### Pseudocode skeleton (complete the details yourselves)

```
MaxMin(A, low, high):
    if high - low == 0:              # 1 element
        return (A[low], A[low])

    if high - low == 1:              # 2 elements
        if A[low] > A[high]:
            return (A[low], A[high])
        else:
            return (A[high], A[low])

    mid = (low + high) / 2
    (max1, min1) = MaxMin(A, low, mid)
    (max2, min2) = MaxMin(A, mid+1, high)

    max = larger of (max1, max2)     # 1 comparison
    min = smaller of (min1, min2)    # 1 comparison
    return (max, min)
```

### Recurrence to derive and solve (Student A's task)
- T(2) = 1
- T(n) = 2·T(n/2) + 2

Solve this (recursion tree or substitution) and compare the result against the naive 2n−2. You should be able to defend *why* the D&C approach does better and by how much.

### What Student A still needs to produce
- A diagram of the decomposition (tree showing how the array splits)
- Written explanation of how subproblems are formed and combined
- The solved recurrence and resulting comparison count
- A mathematical comparison against the naive method

### What Student B still needs to produce
- An actual implementation with a comparison counter instrumented in the code
- Test datasets of increasing size (e.g., powers of 2, and non-powers of 2 to test edge handling)
- A table comparing **predicted** comparisons (from Student A's formula) vs **observed** comparisons from running the code
- An explanation for any discrepancy (e.g., off-by-one effects, odd-length arrays)

---

## Part B — Binary Search

### Decision rule
Compare the target `x` to the middle element `A[mid]`.
- `x == A[mid]` → found, return index.
- `x < A[mid]` → recurse on the **left half** only.
- `x > A[mid]` → recurse on the **right half** only.

### Why elimination is valid (Student B must be able to justify this, not just state it)
The array is sorted, so:
- If `x < A[mid]`, every element to the right of `mid` is `≥ A[mid] > x`, so none of them can equal `x`. The right half is safely eliminated.
- The mirror argument holds for `x > A[mid]`.

This is the core justification question in the assignment — elimination is a *proof*, not a guess.

### Termination condition
`low > high` → search space is empty → target not found.

### Pseudocode skeleton

```
BinarySearch(A, low, high, x):
    if low > high:
        return NOT_FOUND

    mid = (low + high) / 2

    if A[mid] == x:
        return mid
    else if x < A[mid]:
        return BinarySearch(A, low, mid - 1, x)
    else:
        return BinarySearch(A, mid + 1, high, x)
```

### What Student A still needs to produce
- Designed test cases: successful search (various positions — first, last, middle) and unsuccessful search (value not present, value below min, value above max)
- Comparison counts recorded for each case
- Investigation of how comparison count grows as dataset size increases (should trend toward log₂n)
- Presented experimental evidence (table/graph)

### What Student B still needs to produce
- A written explanation of the decision rule
- The elimination justification above, in your own words
- Explanation of the termination condition
- A short discussion relating repeated elimination (halving the space each time) to the O(log n) efficiency

---

## Reminder for the Viva
Both of you must be able to explain **both parts**, not just your "primary" half. Faculty may ask Student A to explain Binary Search elimination, or Student B to explain the Max/Min recurrence. Practice explaining the other person's section out loud to each other before submission.
