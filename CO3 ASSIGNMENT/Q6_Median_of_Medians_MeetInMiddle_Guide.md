# Q6 – Advanced Divide-and-Conquer Mini-Investigations (7 Marks)

> Concepts and skeletons only. Each of you leads one investigation, but both must verify the other's — this question gives the clearest individual evidence, so lean into actually understanding your own part deeply.

---

## Student A — Median of Medians (primary responsibility)

### Core idea
Used to find the k-th smallest element in O(n) worst-case time (unlike QuickSelect, which is O(n) average but O(n²) worst case).

**Steps:**
1. Divide the array into groups of 5 elements each.
2. Find the median of each group (small, fixed-size sort — O(1) per group).
3. Recursively find the median of these group-medians — this is the "median of medians," call it `p`.
4. Use `p` as the pivot: partition the array around it, same as QuickSelect.
5. Recurse into whichever side contains the k-th element.

### Pseudocode skeleton

```
SelectMedianOfMedians(A, k):
    if |A| <= 5:
        sort A, return k-th smallest directly        # base case

    groups = split A into groups of 5
    medians = [median(g) for g in groups]
    p = SelectMedianOfMedians(medians, |medians|/2)    # recursively find median of medians

    partition A around p into (Less, Equal, Greater)

    if k <= |Less|:
        return SelectMedianOfMedians(Less, k)
    else if k <= |Less| + |Equal|:
        return p
    else:
        return SelectMedianOfMedians(Greater, k - |Less| - |Equal|)
```

### What you need to do
1. Implement this for finding the k-th smallest element.
2. Explain the grouping strategy — why groups of 5 specifically (this is the classic choice; research/think about why not groups of 3 or 7 — it relates to balancing the recursive work).
3. Explain how the pivot (median of medians) is determined.
4. Explain why consistently disastrous partitions are prevented — the key guarantee is that the median of medians is provably "good enough": at least ~30% of elements are guaranteed to be less than it and ~30% greater, no matter the input.
5. Compare against QuickSelect (which uses a random or fixed pivot) — QuickSelect is usually faster in practice but has no worst-case guarantee.
6. Demonstrate the effect of a deterministic poor-pivot strategy — e.g., show what happens to plain QuickSelect with first-element pivot on a sorted array (O(n²) behavior), and contrast with Median of Medians staying O(n).
7. Explain why randomization reduces but doesn't eliminate poor partitions — a random pivot makes worst-case input hard to construct *in advance*, but an unlucky sequence of random choices can still occur.
8. Explain the worst-case guarantee: T(n) = T(n/5) + T(7n/10) + O(n) → solves to O(n).

### Student B Verification
You (Student B) must be able to explain: **Why is pivot quality central to the performance of selection algorithms?** Think about how pivot choice determines partition balance, which directly determines whether the recursion tree is shallow (fast) or deep (slow).

---

## Student B — Meet-in-the-Middle (primary responsibility)

### Core idea
Used for Subset-Sum problems where brute force is O(2ⁿ). Meet-in-the-Middle brings this down to roughly O(2^(n/2)).

**Steps:**
1. Split the set of n elements into two halves of n/2 each.
2. Generate **all** possible subset sums for each half separately (2^(n/2) sums per half).
3. Sort one of the two lists of sums.
4. For each sum in the first half's list, binary-search the second half's sorted list for a complementary value that makes the target sum.

### Pseudocode skeleton

```
MeetInMiddle(elements, target):
    split elements into Half1, Half2 (each of size n/2)

    sums1 = all subset sums of Half1          # 2^(n/2) values
    sums2 = all subset sums of Half2          # 2^(n/2) values

    sort sums2

    for each s1 in sums1:
        needed = target - s1
        if needed found in sums2 (via binary search):
            return TRUE (subset exists)

    return FALSE
```

### What you need to do
1. Explain how the original problem is divided (split the set in half).
2. Generate subset results for both halves (this is the 2^(n/2) enumeration step).
3. Explain how the partial results are combined/searched (sort + binary search, or a two-pointer approach).
4. Determine the resulting search-space size: instead of 2ⁿ total subsets checked, you generate 2^(n/2) + 2^(n/2) and search — much smaller for large n.
5. Analyze additional memory requirements — you must *store* all 2^(n/2) sums from both halves, which is the trade-off: less time, more space.
6. Compare with straightforward 2ⁿ enumeration — show concretely (e.g., for n=40, 2⁴⁰ is infeasible but 2²⁰ + 2²⁰ is very manageable).
7. Explain the time-memory trade-off explicitly: you're spending memory to avoid exponential time.

### Student A Verification
You (Student A) must be able to explain: **Why can Meet-in-the-Middle reduce computational work even though it introduces additional storage?** Think about how splitting the exponent in half (2^(n/2) vs 2ⁿ) is a massive practical win even though you now need to store and search through those intermediate results.

---

## Reminder for the Viva
This question is explicitly designed to produce clear individual evidence — but cross-verification still matters. Each of you should be able to explain the *other's* algorithm at a basic level, not just answer your assigned verification question from memory.
