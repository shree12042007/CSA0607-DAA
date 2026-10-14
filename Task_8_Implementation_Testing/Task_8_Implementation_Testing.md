# Task 8 – Implement and Test the Algorithms (4 Marks)

## Implementation
Language: Python 3 (standard library + `matplotlib`, `Pillow` only for graphs/screenshots).

| File (in `Source_Code/`) | Purpose |
|--------------------------|---------|
| `search_algorithms.py` | The three algorithms: `linear_search` (iterative), `binary_search_recursive` + `sort_records`, `ChainedHashTable` + `build_hash_table`. Every search returns `(index, comparisons)` so that the basic operation can be counted exactly, exactly as analysed in Tasks 2–3. |
| `test_algorithms.py` | 15 correctness / property tests. |
| `run_experiments.py` | Benchmark for n = 1,000; 10,000; 100,000; 1,000,000. Writes `results.csv/json` and the graphs. |
| `make_screenshots.py` | Renders source code and console outputs to PNG for the report. |

The implementation matches the analysed pseudocode one-to-one (one comparison counted per loop iteration / per recursive call / per chain element).

## Reproducible testing procedure
1. **Dataset.** For each n a list of n *unique* 9-digit registration numbers (100,000,000–999,999,999) is drawn with `random.Random(2024 + n).sample`, in random (unsorted) order. All three algorithms receive exactly the same records (linear: the raw list; binary: the sorted copy; hash: the table built from the same list). Fixed seeds make the run repeatable.
2. **Query sets.** 100 random *existing* keys (successful search) and 100 random *non-existing* keys (unsuccessful search). Identical query sets for all three algorithms. In addition: best-case key (first element for linear, middle element for binary), and worst-case key (last element for linear).
3. **Measurements.** Average number of comparisons, average time per search (µs, `time.perf_counter`), preprocessing time (ms), worst comparisons seen, longest hash chain.
4. **Consistency.** Same machine, same process, same Python interpreter, no other deliberate load; sorting and hashing time are included in the preprocessing column rather than hidden.
5. **Correctness check at every size:** 40 queries (20 present, 20 absent) must give the same found/not-found result in all three algorithms – all sizes reported *OK*.

## Test cases (`test_algorithms.py`)
| ID | Case | Expected |
|----|------|----------|
| T1 | key = first element of unsorted list | found by all |
| T2 | key = last element | found |
| T3 | key in the middle | found |
| T4 | absent key inside the value range | not found |
| T5 | absent key smaller than minimum | not found |
| T6 | absent key larger than maximum | not found |
| T7/T8 | single-element list (present / absent) | found / not found |
| T9 | empty list | not found, no crash |
| T10 | two-element list, second present | found |
| T11 | 7 sizes × 300 random queries – all three must agree with Python `in` | agree |
| T12 | binary worst case on n = 1023 | = ⌊log₂ n⌋+1 = 10 |
| T13/T14 | linear worst / best case counts | n / 1 |
| T15 | hash load factor | ≈ 0.75 |

**Result: 15 passed, 0 failed** (`Report/Output_Screenshots/test_output.png`).

## How to run
```
cd Task_8_Implementation_Testing/Source_Code
pip install matplotlib pillow
python test_algorithms.py
python run_experiments.py        # ≈ 1–2 minutes; writes results + graphs
python make_screenshots.py
```
