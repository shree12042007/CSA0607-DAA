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
