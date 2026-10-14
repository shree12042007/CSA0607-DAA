import math
import random
import time


# ----------------------------------------------------------------- M1 -------
def m1_bruteforce(products):
    """Original nightly routine. Basic operation = one title/seller comparison."""
    n = len(products)
    comparisons = 0
    duplicates = set()
    for i in range(0, n - 1):                # i = 0 .. n-2
        for j in range(i + 1, n):            # j = i+1 .. n-1
            comparisons += 1                 # basic operation
            if products[i] == products[j]:   # (title, seller) tuple compare
                duplicates.add(j)            # MarkDuplicate(j)
    return comparisons, duplicates


def m1_formula(n):
    """C(n) = sum_{i=0}^{n-2} (n-1-i) = n(n-1)/2"""
    return n * (n - 1) // 2


def m1_hash(products):
    """Proposed redesign: one pass with a hash set -> expected Theta(n)."""
    seen, duplicates, ops = set(), set(), 0
    for j, p in enumerate(products):
        ops += 1                             # one hash lookup per product
        if p in seen:
            duplicates.add(j)
        else:
            seen.add(p)
    return ops, duplicates


# ----------------------------------------------------------------- M2 -------
def m2_count(n):
    """Returns (outer iterations, number of Audit operations)."""
    i, outer, audits = 1, 0, 0
    while i < n:
        outer += 1
        for j in range(0, i):                # j = 0 .. i-1
            audits += 1                      # Audit(Request[j])  <- basic op
        i = i * 2
    return outer, audits


def m2_formula(n):
    """outer = ceil(log2 n);  audits = 2^ceil(log2 n) - 1"""
    k = (n - 1).bit_length() if n > 1 else 0     # exact integer ceil(log2 n)
    return k, 2 ** k - 1


if __name__ == "__main__":
    print("=" * 70)
    print("M1  Duplicate-Listing Detector  (basic op: title+seller comparison)")
    print("=" * 70)
    random.seed(1)
    print(f"{'n':>8} {'counted':>14} {'n(n-1)/2':>14} {'match':>6} {'time(s)':>9}")
    for n in (10, 100, 500, 1000, 2000, 4000):
        data = [(f"T{random.randint(0, n // 2)}", f"S{random.randint(0, 5)}")
                for _ in range(n)]
        t0 = time.perf_counter()
        c, dup_a = m1_bruteforce(data)
        dt = time.perf_counter() - t0
        ops, dup_b = m1_hash(data)
        assert dup_a == dup_b, "hash version disagrees with brute force"
        print(f"{n:>8} {c:>14,} {m1_formula(n):>14,} {str(c == m1_formula(n)):>6} {dt:>9.4f}")
    print("Doubling n multiplies the time by ~4  ->  quadratic growth, Theta(n^2).")
    print("Hash-based redesign returns identical duplicate sets (asserted above).")

    print()
    print("=" * 70)
    print("M2  API Rate Limiter  (basic op: Audit(Request[j]))")
    print("=" * 70)
    print(f"{'n':>9} {'outer':>6} {'ceil(lg n)':>10} {'audits':>11} "
          f"{'2^k-1':>11} {'n lg n':>12} {'audits/n':>9}")
    for n in (2, 3, 5, 8, 100, 1000, 1024, 1025, 100_000, 1_000_000):
        outer, audits = m2_count(n)
        k, f = m2_formula(n)
        assert outer == k and audits == f
        print(f"{n:>9,} {outer:>6} {k:>10} {audits:>11,} {f:>11,} "
              f"{n * math.log2(n):>12,.0f} {audits / n:>9.3f}")
    outer, audits = m2_count(1024)
    print(f"\nVerification n = 1024: outer iterations = {outer}, "
          f"i takes 1,2,4,...,512, Audit count = {audits} = 2^10 - 1")
    print(f"Claimed n log2 n = {1024 * 10:,}  ->  claim overestimates by "
          f"{1024 * 10 / audits:.1f}x; true growth is linear, Theta(n).")
