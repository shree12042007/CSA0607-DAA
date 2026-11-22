# Q2 – The Quality of Decomposition in Sorting (7 Marks)

> This file contains concept explanations and pseudocode skeletons to help you build the full solution yourselves. The experiments, recorded data, and written analysis must be your own — both of you will be individually questioned on this.

---

## Shared Group Work (do together first)

- Implement Merge Sort and Quick Sort.
- Pick and clearly state a pivot strategy for Quick Sort (e.g., first element, last element, median-of-three, random). Whatever you choose, you must be able to justify it.
- Design two kinds of inputs:
  - one that gives **balanced** partitions
  - one that gives **severely unbalanced** partitions
- Run both algorithms on these inputs and record behavior.

---

## Merge Sort — core idea

**Decomposition:** split the array into two halves at the midpoint, regardless of the data. This split is always balanced — it doesn't depend on element values at all.

**Combine:** merge two sorted halves into one sorted array — this is where the real work happens (O(n) per merge level).

```
MergeSort(A, low, high):
    if low >= high:
        return                      # base case: 0 or 1 element

    mid = (low + high) / 2
    MergeSort(A, low, mid)
    MergeSort(A, mid+1, high)
    Merge(A, low, mid, high)        # O(n) combine step
```

**Why its decomposition is predictable:** the split point is always the midpoint — it never depends on the input values. So the recursion tree is always balanced, always height log₂n, regardless of input order (sorted, reverse-sorted, random — doesn't matter for the *shape* of the tree).

Recurrence: **T(n) = 2T(n/2) + O(n) → O(n log n)**, always.

---

## Quick Sort — core idea

**Decomposition:** pick a pivot, partition the array so elements smaller than pivot go left, larger go right. Unlike Merge Sort, *where* the split happens depends entirely on the pivot's rank in the data.

```
QuickSort(A, low, high):
    if low >= high:
        return

    p = Partition(A, low, high, pivot_strategy)
    QuickSort(A, low, p - 1)
    QuickSort(A, p + 1, high)
```

**Why decomposition quality varies:**
- Balanced split (pivot near median) → recursion tree height ≈ log₂n → O(n log n) total.
- Severely unbalanced split (pivot near min/max every time, e.g., already-sorted input with first-element pivot) → recursion tree height ≈ n → **O(n²)** total.

This is the core contrast Student B needs to explain: Merge Sort's split is *structural* (always midpoint), Quick Sort's split is *data-dependent* (depends on pivot rank), which is why one is predictable and the other isn't.

---

## Student A — Quick Sort Investigation (your tasks)

1. Design an input that produces **balanced** partitions for your chosen pivot strategy (e.g., random data, or data arranged so the pivot lands near the median).
2. Design an input that produces **severely unbalanced** partitions (e.g., already-sorted or reverse-sorted array, if you're using first/last-element pivot).
3. Instrument your code to record:
   - partition sizes at each recursive call
   - maximum recursion depth reached
4. Explain, with your recorded data as evidence, how pivot selection directly influences decomposition quality — don't just state it, point to your numbers.

**Suggested table to build:**

| Input type | Array size | Max recursion depth | Observed pattern |
|---|---|---|---|
| Random | | | |
| Sorted (worst case for your pivot) | | | |
| Reverse sorted | | | |

---

## Student B — Comparative D&C Analysis (your tasks)

1. Analyze Merge Sort's decomposition structure (always balanced, as above).
2. Compare its recursion tree shape with Quick Sort's (fixed height vs data-dependent height).
3. Explain **why** Merge Sort's decomposition is more predictable — tie this to the fact that the split point doesn't depend on data values.
4. Relate partition quality directly to recursion-tree height: a partition that gives sizes `(1, n-1)` instead of `(n/2, n/2)` adds a level to the tree instead of halving it.
5. Explain how **repeated** imbalance (not just one bad split) compounds into O(n²): if every single partition is maximally unbalanced, you get n levels of O(n) work each = O(n²).

---

## Joint Design Question (answer together, both must defend it)

> If you were designing a sorting component for an application in which the characteristics of the input data are not known in advance, what information would you want before deciding between these two D&C strategies?

Think about: Is memory constrained? (Merge Sort needs O(n) extra space; Quick Sort can be done in-place.) Is stability required? Is the data likely to be adversarial, nearly-sorted, or random? Is worst-case guarantee more important than average-case speed? Both of you should be able to give this answer independently in the viva — don't just memorize one person's version, actually understand the trade-off.

---

## Reminder for the Viva
A classic transfer question for this topic: *"If Quick Sort repeatedly produces a 90:10 split rather than a 50:50 split, what happens to the recursion structure?"* Make sure both of you can answer this by reasoning from the recursion tree, not by recalling a memorized line.
