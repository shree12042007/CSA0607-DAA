"""
search_algorithms.py
CSA06 Design and Analysis of Algorithms - CO1 Assignment
Student Record Retrieval: three distinct search strategies.

Every search function returns a tuple (index, comparisons):
    index        -> position of the key (or -1 if absent)
    comparisons  -> number of key comparisons performed (the basic operation)

Algorithm 1 : Sequential (linear) search  - Brute force,        ITERATIVE
Algorithm 2 : Binary search               - Decrease & conquer, RECURSIVE
Algorithm 3 : Hash table (chaining)       - Space-time trade-off (hashing)
"""


# ---------------------------------------------------------------------------
# Algorithm 1: Linear search (brute force, iterative). No preprocessing.
# ---------------------------------------------------------------------------
def linear_search(records, key):
    comps = 0
    for i in range(len(records)):
        comps += 1                      # basic operation: records[i] == key
        if records[i] == key:
            return i, comps
    return -1, comps


# ---------------------------------------------------------------------------
# Algorithm 2: Binary search (decrease-and-conquer, recursive).
# Preprocessing: records must be sorted (done by sort_records()).
# ---------------------------------------------------------------------------
def sort_records(records):
    """Preprocessing for binary search: O(n log n) comparison sort (Timsort)."""
    return sorted(records)


def binary_search_recursive(arr, key, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    if low > high:                      # base case: empty subarray
        return -1, 0
    mid = (low + high) // 2
    if arr[mid] == key:                 # basic operation: one key comparison
        return mid, 1                   # (three-way compare counted once)
    if arr[mid] < key:
        idx, c = binary_search_recursive(arr, key, mid + 1, high)
    else:
        idx, c = binary_search_recursive(arr, key, low, mid - 1)
    return idx, c + 1


# ---------------------------------------------------------------------------
# Algorithm 3: Hash table with separate chaining (space-time trade-off).
# Preprocessing: build the table, O(n) expected.
# ---------------------------------------------------------------------------
def _is_prime(x):
    if x < 2:
        return False
    if x % 2 == 0:
        return x == 2
    i = 3
    while i * i <= x:
        if x % i == 0:
            return False
        i += 2
    return True


def _next_prime(x):
    while not _is_prime(x):
        x += 1
    return x


class ChainedHashTable:
    """Hash table, h(k) = k mod m, m prime, load factor ~ 0.75."""

    def __init__(self, n_expected, load_factor=0.75):
        self.m = _next_prime(int(n_expected / load_factor) + 1)
        self.buckets = [[] for _ in range(self.m)]
        self.size = 0

    def insert(self, key, row):
        self.buckets[key % self.m].append((key, row))
        self.size += 1

    def search(self, key):
        comps = 0
        for k, row in self.buckets[key % self.m]:
            comps += 1                  # basic operation: key comparison in chain
            if k == key:
                return row, comps
        return -1, comps

    def load_factor(self):
        return self.size / self.m


def build_hash_table(records):
    """Preprocessing for hashing: n insertions, O(n) expected."""
    ht = ChainedHashTable(len(records))
    for row, key in enumerate(records):
        ht.insert(key, row)
    return ht
