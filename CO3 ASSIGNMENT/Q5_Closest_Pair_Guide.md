# Q5 – Upgrading Closest Pair Using Divide and Conquer (6 Marks)

> Concepts and skeletons only — the experiments, data, and written analysis must be your own, since both of you face cross-understanding questions on this one specifically.

---

## Shared Group Work (do together first)

- Review the Brute-Force Closest-Pair approach from CO2 (check all pairs, O(n²)).
- Design the D&C Closest-Pair solution.
- Implement it.
- Compare both approaches using equivalent datasets.

---

## Core idea

**Setup:** Points are pre-sorted by x-coordinate (and a copy by y-coordinate is often kept too).

**Decomposition:**
1. Split the points into a left half and right half by a vertical line through the median x-coordinate.
2. Recursively find the closest pair in each half, getting distances `d_left` and `d_right`.
3. Let `d = min(d_left, d_right)`.

**The tricky part — the "strip":** the true closest pair might straddle the dividing line (one point in the left half, one in the right half). So you must check a **strip** of width `2d` centered on the dividing line.

**Why the strip doesn't need comparison with every other point:** within the strip, points are sorted by y-coordinate. A key geometric fact: for any point in the strip, you only need to compare it against the next **few** points above it in y-order (at most 7, by a packing argument — within a `d × 2d` box you can't fit more than a handful of points that are all pairwise ≥ d apart). This is what keeps the strip-check step to O(n) instead of O(n²).

**Combine step:** return the minimum of `d_left`, `d_right`, and the smallest cross-strip distance found.

## Pseudocode skeleton

```
ClosestPair(P_sorted_by_x):
    if |P| <= 3:
        return BruteForce(P)              # base case

    mid = median x-coordinate
    PL = points with x <= mid
    PR = points with x > mid

    dL = ClosestPair(PL)
    dR = ClosestPair(PR)
    d = min(dL, dR)

    strip = points within distance d of the dividing line, sorted by y
    dStrip = check only nearby points (limited window) in strip for closer pairs

    return min(d, dStrip)
```

---

## Student A — Decomposition Design (your tasks)

1. Explain how the points are organized (sorted by x, and why that ordering matters for splitting).
2. Explain how the problem is divided (vertical line through median x).
3. Identify what each recursive call returns (the closest distance found within that half — and typically also the sorted-by-y subset, depending on your implementation).
4. Explain the combine step (comparing dL, dR, and the strip).
5. Explain why the dividing boundary requires special treatment — this is exactly the "pairs can straddle the line" issue above. Make sure you can explain *why* brute-force-per-half alone would miss valid closest pairs.

**Cross-Understanding requirement for Student A:** you must also be able to explain *what experimental evidence demonstrates that the D&C strategy has actually reduced computational work* — this means you need to look at Student B's data and be ready to discuss it, not just your own part.

---

## Student B — Comparative Evidence (your tasks)

1. Design equivalent datasets for brute-force and D&C comparison (same points, both algorithms run on them).
2. Record distance calculations performed by each method (count actual distance computations, not just wall-clock time).
3. Record execution behavior (timing) across increasing dataset sizes.
4. Compare growth between the two approaches — does brute-force grow quadratically while D&C grows closer to n log n, as your data?
5. Determine approximately when D&C becomes practically advantageous (crossover point).

**Cross-Understanding requirement for Student B:** you must also be able to explain *why the strip/boundary stage does not require comparison with every other point* — this means understanding Student A's geometric argument above, not just running the experiments.

---

## Reminder for the Viva
This question is explicitly designed to test whether you each understand the *other* person's section — don't just memorize your own part. Practice explaining both the geometric argument (why the strip check is efficient) and the experimental evidence (why D&C actually wins) to each other before submission.
