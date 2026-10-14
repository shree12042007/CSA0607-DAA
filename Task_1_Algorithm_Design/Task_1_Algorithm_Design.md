# Task 1 – Design the Algorithm (5 Marks)

**Problem.** Given a collection of *n* student records, each with a unique registration number, decide whether a key *K* exists and return its position.
**Input size:** *n* = number of records (10³ → 10⁶+).

Three algorithms with *different design strategies* were chosen. The iterative/recursive requirement is met by Algorithm 1 (iterative) and Algorithm 2 (recursive). Algorithm 2 is **not** an iterative/recursive twin of Algorithm 1 – it uses a different strategy and a different data organisation.

| # | Algorithm | Design strategy | Style | Preprocessing |
|---|-----------|-----------------|-------|---------------|
| 1 | Sequential (linear) search | Brute force | Iterative | None |
| 2 | Binary search | Decrease-and-conquer (decrease by half) + presorting (transform-and-conquer) | Recursive | Sort the records, Θ(n log n) |
| 3 | Hash table with chaining | Space–time trade-off (hashing / input enhancement) | Iterative (inside chain) | Build table, Θ(n) expected |

---
## Algorithm 1 – Linear Search (Brute Force, Iterative)

**Basic idea.** Examine records one by one from the start until the key is found or the list ends. It makes no assumption about the order of the data.

```
ALGORITHM LinearSearch(A[0..n-1], K)
  for i ← 0 to n-1 do
      if A[i] = K then return i        // key comparison
  return -1
```
**Preprocessing:** none – works directly on the unsorted database.
**Why investigated:** It is the natural baseline; it is the only option if a record is looked up once and the data are unordered, and it has zero setup cost and zero extra memory. All other algorithms must be compared against it.

---
## Algorithm 2 – Binary Search (Decrease-and-Conquer, Recursive)

**Basic idea.** If the records are sorted by registration number, compare K with the middle record. If equal, done; if K is smaller, the key can only be in the left half; otherwise only in the right half. Each comparison discards half of the remaining records.

```
ALGORITHM Preprocess(A[0..n-1])
  sort A in ascending order            // e.g. merge sort / Timsort, Θ(n log n)

ALGORITHM BinarySearch(A, K, low, high)
  if low > high then return -1         // base case: empty range
  mid ← ⌊(low + high) / 2⌋
  if A[mid] = K then return mid        // key comparison
  else if K < A[mid] then return BinarySearch(A, K, low, mid-1)
  else                    return BinarySearch(A, K, mid+1, high)
```
**Preprocessing:** the records (or an index of registration numbers + record pointers) must be sorted once.
**Why investigated:** it is the textbook example of decrease-and-conquer; it turns a Θ(n) problem into Θ(log n) at the cost of a one-time sort, so it tests whether presorting pays off. It is also naturally recursive, giving a recurrence relation to analyse (Tasks 6–7).

---
## Algorithm 3 – Hash Table with Separate Chaining (Space–Time Trade-off)

**Basic idea.** Use the registration number to compute the address of the record directly: h(K) = K mod m (m prime, m ≈ n/0.75). Records whose keys collide are kept in a short linked list (chain) at that bucket. A search computes h(K) and scans only that one chain.

```
ALGORITHM BuildHash(A[0..n-1])
  m ← smallest prime ≥ n / 0.75
  create m empty chains T[0..m-1]
  for i ← 0 to n-1 do
      append (A[i], i) to chain T[A[i] mod m]      // O(1)

ALGORITHM HashSearch(T, K)
  for each (key, row) in chain T[K mod m] do
      if key = K then return row                   // key comparison
  return -1
```
**Preprocessing:** build the table once, Θ(n) expected, extra memory Θ(n).
**Why investigated:** it trades memory for time and is the only strategy of the three that can reach Θ(1) average lookups; it represents the standard "database index" idea for exact-match queries and has cheap incremental insertion – relevant to the Day-4 challenge.

---
**Selection summary.** The three strategies sit at three points of the design space: *no preprocessing / slow search* (brute force), *Θ(n log n) preprocessing / logarithmic search* (presorting), and *Θ(n) preprocessing + extra memory / constant average search* (hashing). Source code: `Task_8_Implementation_Testing/Source_Code/search_algorithms.py`.
