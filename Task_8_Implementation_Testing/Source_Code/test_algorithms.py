"""
test_algorithms.py - correctness tests for all three algorithms.
Run:  python test_algorithms.py
"""
import math
import random
from search_algorithms import (linear_search, sort_records,
                               binary_search_recursive, build_hash_table)

passed = failed = 0


def check(name, cond):
    global passed, failed
    if cond:
        passed += 1
        print(f"  PASS  {name}")
    else:
        failed += 1
        print(f"  FAIL  {name}")


def run_all(records, key):
    """Return True/False presence found by each algorithm."""
    s = sort_records(records)
    ht = build_hash_table(records)
    l, _ = linear_search(records, key)
    b, _ = binary_search_recursive(s, key)
    h, _ = ht.search(key)
    return l, b, h, s


def test_case(title, records, key, expected_present):
    l, b, h, s = run_all(records, key)
    ok = ((l != -1) == expected_present and (b != -1) == expected_present
          and (h != -1) == expected_present)
    if expected_present:                      # returned positions must hold the key
        ok = ok and records[l] == key and s[b] == key and records[h] == key
    check(title, ok)


print("Functional test cases")
data = [230101, 230457, 230999, 231234, 231500, 232001, 232345]
random.Random(1).shuffle(data)
test_case("T1 key at first position of unsorted list", data, data[0], True)
test_case("T2 key at last position of unsorted list", data, data[-1], True)
test_case("T3 key in middle", data, data[3], True)
test_case("T4 absent key (inside range)", data, 230500, False)
test_case("T5 absent key smaller than min", data, 1, False)
test_case("T6 absent key larger than max", data, 999999, False)
test_case("T7 single-element list, present", [42], 42, True)
test_case("T8 single-element list, absent", [42], 43, False)
test_case("T9 empty list", [], 5, False)
test_case("T10 two elements, second present", [10, 20], 20, True)

print("Randomised cross-validation (all three algorithms must agree)")
rng = random.Random(7)
ok = True
for n in (1, 2, 3, 10, 100, 1000, 5000):
    recs = rng.sample(range(10**8, 10**9), n)
    s = sort_records(recs)
    ht = build_hash_table(recs)
    pool = set(recs)
    for _ in range(300):
        key = rng.choice(recs) if rng.random() < 0.5 else rng.randrange(10**8, 10**9)
        present = key in pool
        l, _ = linear_search(recs, key)
        b, _ = binary_search_recursive(s, key)
        h, _ = ht.search(key)
        if not ((l != -1) == (b != -1) == (h != -1) == present):
            ok = False
check("T11 random agreement on 7 sizes x 300 queries", ok)

print("Complexity-property tests")
n = 2**10 - 1
s = list(range(n))
worst = max(binary_search_recursive(s, k)[1] for k in range(-1, n + 1))
check(f"T12 binary worst case comparisons = floor(log2 n)+1 = {int(math.log2(n))+1} (got {worst})",
      worst == int(math.log2(n)) + 1)
check("T13 linear worst case = n comparisons", linear_search(list(range(500)), -1)[1] == 500)
check("T14 linear best case = 1 comparison", linear_search(list(range(500)), 0)[1] == 1)
ht = build_hash_table(list(range(1, 10001)))
check("T15 hash load factor approx 0.75", abs(ht.load_factor() - 0.75) < 0.01)

print(f"\nTests passed: {passed}   failed: {failed}")
raise SystemExit(0 if failed == 0 else 1)
