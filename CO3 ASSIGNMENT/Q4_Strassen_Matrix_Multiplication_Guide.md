# Q4 – The Reality of Strassen's Matrix Multiplication (7 Marks)

> Concepts and skeletons only — the experiments, measurements, and written analysis must be your own. Note: responsibilities are deliberately reversed here (Student B does the theory, Student A does the experiments) so the same student doesn't always do the same type of work.

---

## Shared Group Work (do together first)

- Study conventional block-matrix multiplication.
- Reconstruct Strassen's transformation (work through the algebra together, don't just copy it — you both need to understand it since Student A will be tested on parts of it too).
- Implement conventional and Strassen multiplication.
- Verify correctness (multiply the same matrices both ways, check results match).

---

## Core idea: conventional block multiplication

Split each n×n matrix into four (n/2)×(n/2) blocks:

```
A = [A11 A12]      B = [B11 B12]
    [A21 A22]          [B21 B22]
```

The conventional method computes C = A×B using **8** block multiplications:
```
C11 = A11*B11 + A12*B21
C12 = A11*B12 + A12*B22
C21 = A21*B11 + A22*B21
C22 = A21*B12 + A22*B22
```
That's 8 multiplications and 4 additions of blocks.

## Strassen's trick: 8 → 7 multiplications

Strassen defines 7 products (combinations of sums/differences of blocks):
```
M1 = (A11+A22) * (B11+B22)
M2 = (A21+A22) * B11
M3 = A11 * (B12-B22)
M4 = A22 * (B21-B11)
M5 = (A11+A12) * B22
M6 = (A21-A11) * (B11+B12)
M7 = (A12-A22) * (B21+B22)
```
Then combine:
```
C11 = M1 + M4 - M5 + M7
C12 = M3 + M5
C21 = M2 + M4
C22 = M1 - M2 + M3 + M6
```

This trades **1 multiplication** for **extra additions/subtractions** — multiplications are the expensive operation asymptotically, so this trade is a net win for large matrices.

## Pseudocode skeleton

```
Strassen(A, B, n):
    if n == 1:
        return A[0][0] * B[0][0]          # base case

    split A, B into four (n/2)x(n/2) blocks each

    M1..M7 = recursive Strassen calls as above

    combine M1..M7 into C11, C12, C21, C22
    return C (assembled from the four blocks)
```

---

## Student B — Algebraic Design & Correctness (your tasks)

1. Represent the conventional block decomposition (show the 8-multiplication formulas above, in your own notation/diagram).
2. Identify the eight standard block multiplications explicitly.
3. Explain the algebraic transformation reducing 8 multiplications to 7 — work through *why* M1–M7 combine correctly to reproduce C11–C22 (expand the algebra by hand for at least C11 and C22 to prove it to yourself).
4. Explain why the reconstructed expressions produce the correct result — this is really asking you to verify the algebra, not just trust the formula.
5. Explain how padding is handled when matrix size isn't a power of 2 (pad with zero rows/columns up to the next power of 2, then discard the extra rows/columns from the result).

---

## Student A — Experimental & Engineering Analysis (your tasks)

1. Select matrix sizes to test — include small (e.g., 2×2, 4×4), medium, and larger sizes, ideally powers of 2 for simplicity plus at least one non-power-of-2 to test padding.
2. Design the experiment: same matrices run through both conventional and Strassen multiplication.
3. Record multiplication counts for each method at each size.
4. Measure repeated execution times (average over multiple runs).
5. Identify the approximate practical crossover range — where does Strassen actually start winning in real time, not just in multiplication count?
6. Analyze overhead sources: the extra additions/subtractions Strassen requires, recursion overhead, and padding overhead (padding wastes computation on zero-regions).
7. Discuss memory/cache effects if you observe any (e.g., Strassen's extra temporary matrices can hurt cache locality for large n, which conventional iterative multiplication may not suffer as much).

**Suggested table:**

| Matrix size (n×n) | Conventional mult. count | Strassen mult. count | Conventional time | Strassen time |
|---|---|---|---|---|

---

## Joint Engineering Decision (answer together, both must defend it)

> Under what conditions would you use conventional matrix multiplication even though Strassen has superior asymptotic complexity?

Think about: small matrix sizes (overhead dominates), numerical stability concerns (Strassen can have more floating-point error due to extra additions/subtractions), implementation complexity, memory overhead from recursion and temporary matrices, and whether matrices are already near powers of 2 (padding cost).

---

## Reminder for the Viva
Possible transfer question: *"If the matrix size is not a power of two, what does your Strassen implementation need to do, and what cost does this introduce?"* Make sure Student A especially can answer this from the padding/overhead analysis above.
