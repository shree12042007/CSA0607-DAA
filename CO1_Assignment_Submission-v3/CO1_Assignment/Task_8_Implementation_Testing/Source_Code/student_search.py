"""Student Registration Number Search Strategies (CO1 Assignment)."""
import math
import time
import numpy as np


def sequential_search_iter(records, target):
    """Iterative sequential search on unsorted registration numbers. Returns (index, comparisons)."""
    comparisons = 0
    for idx, reg_no in enumerate(records):
        comparisons += 1
        if reg_no == target:
            return idx, comparisons
    return -1, comparisons


def binary_search_rec(sorted_records, target, low=0, high=None, comparisons=0):
    """Recursive binary search on sorted registration numbers. Returns (index, comparisons)."""
    if high is None:
        high = len(sorted_records) - 1
    if low > high:
        return -1, comparisons
    mid = low + (high - low) // 2
    comparisons += 1
    if sorted_records[mid] == target:
        return mid, comparisons
    if target < sorted_records[mid]:
        return binary_search_rec(sorted_records, target, low, mid - 1, comparisons)
    return binary_search_rec(sorted_records, target, mid + 1, high, comparisons)


def build_hash_table(records):
    """Build hash table mapping registration number -> record index in O(n) time."""
    table = {}
    for idx, reg_no in enumerate(records):
        if reg_no not in table:
            table[reg_no] = idx
    return table


def hash_table_search(table, target):
    """Lookup registration number in pre-built hash table. Returns (index, key_checks)."""
    return table.get(target, -1), 1


def run_verification():
    sample = ["192410005", "192410001", "192410009", "192410003", "192410007"]
    s_sample = sorted(sample)
    h_sample = build_hash_table(sample)

    target = "192410007"
    i_seq, _ = sequential_search_iter(sample, target)
    i_bin, _ = binary_search_rec(s_sample, target)
    i_hash, _ = hash_table_search(h_sample, target)

    assert sample[i_seq] == target
    assert s_sample[i_bin] == target
    assert sample[i_hash] == target

    # Missing key check
    assert sequential_search_iter(sample, "999999999")[0] == -1
    assert binary_search_rec(s_sample, "999999999")[0] == -1
    assert hash_table_search(h_sample, "999999999")[0] == -1
    print("Verification passed for hit and miss cases.")


if __name__ == "__main__":
    run_verification()
