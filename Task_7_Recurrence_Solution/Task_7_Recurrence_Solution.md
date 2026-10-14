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
