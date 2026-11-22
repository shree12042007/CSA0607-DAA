# Q3 – Breaking the Quadratic Barrier: Karatsuba Multiplication (7 Marks)

> Concepts and skeletons only — the derivations, timing experiments, and written analysis must be your own, since both of you can be individually questioned on this.

---

## Shared Group Work (do together first)

- Understand how large integers are decomposed into halves.
- Implement **standard (schoolbook) multiplication** — O(n²).
- Implement **Karatsuba multiplication**.
- Run a crossover experiment: time both algorithms across a range of input sizes.

---

## Core idea: decomposing the integers

Given two n-digit numbers `x` and `y`, split each into two halves:

```
x = x1 * 10^(n/2) + x0
y = y1 * 10^(n/2) + y0
```

**Standard approach** would need 4 recursive multiplications:
`x1*y1`, `x1*y0`, `x0*y1`, `x0*y0`

**Karatsuba's trick** computes the same product using only **3** multiplications:
```
z2 = x1 * y1
z0 = x0 * y0
z1 = (x1 + x0) * (y1 + y0) - z2 - z0      # this replaces x1*y0 + x0*y1
```

Then combine:
```
result = z2 * 10^n + z1 * 10^(n/2) + z0
```

## Pseudocode skeleton

```
Karatsuba(x, y):
    if x < 10 or y < 10:                # base case: single digit
        return x * y

    n = max(num_digits(x), num_digits(y))
    m = n / 2

    x1, x0 = split x at position m       # x = x1 * 10^m + x0
    y1, y0 = split y at position m

    z2 = Karatsuba(x1, y1)
    z0 = Karatsuba(x0, y0)
    z1 = Karatsuba(x1 + x0, y1 + y0) - z2 - z0

    return z2 * 10^(2m) + z1 * 10^m + z0
```

---

## Student A — Algorithmic Derivation (your tasks)

1. Explain how the integers are decomposed (as above, in your own words — with an example, e.g., multiply two 4-digit numbers by hand following this method).
2. Show how the 3 subproblems are formed from the split.
3. Explain **why** reducing 4 multiplications to 3 matters asymptotically — this is the crux of the whole algorithm, make sure you can argue it from the recurrence, not just state "it's faster."
4. Formulate the recurrence:
   - T(n) = 3·T(n/2) + O(n)   (the O(n) is the additions/subtractions and shifting)
5. Solve the recurrence (Master Theorem or recursion tree) — you should get **O(n^log₂3) ≈ O(n^1.585)**, compared to O(n²) for standard multiplication.
6. State the resulting asymptotic complexity and explain what log₂3 represents in terms of the recursion tree's branching factor vs depth.

---

## Student B — Crossover Investigation (your tasks)

1. Design a range of experimental input sizes — include very small numbers (a few digits), medium (tens of digits), and large (hundreds/thousands of digits).
2. Run repeated timing experiments for both algorithms at each size (run multiple trials and average, to reduce noise).
3. Record the number of multiplications performed by each algorithm at each size (not just time — multiplication *count* is a cleaner theoretical metric).
4. Determine the approximate crossover point — the input size where Karatsuba starts outperforming standard multiplication.
5. Explain why Karatsuba can perform **worse** for small inputs — think about what extra work it does (addition, subtraction, recursive call overhead) that a single multiplication avoids.
6. Identify where exactly that overhead comes from: each recursive call has setup/teardown cost, and for small n this fixed cost outweighs the asymptotic savings.

**Suggested table:**

| Digits (n) | Standard mult. count | Karatsuba mult. count | Standard time | Karatsuba time |
|---|---|---|---|---|
| ... | | | | |

---

## Joint Conclusion (answer together, both must defend it)

> Why does better asymptotic complexity not automatically imply better performance for every input size?

Think about: asymptotic notation describes growth rate as n → ∞ and hides constant factors; for small n, the constants and overhead dominate; recursion itself has a cost (function calls, memory allocation) that a simple loop doesn't pay. Use your own crossover data as concrete evidence when explaining this.

---

## Reminder for the Viva
Possible transfer question: *"If you had to multiply very small numbers (e.g., under 10 digits) repeatedly inside a larger program, would you use Karatsuba? Why or why not?"* Be ready to answer this from your own crossover data, not from memory of the general rule.
