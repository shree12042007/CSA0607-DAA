"""Student Registration Number Search Implementations (CO1 Assignment)."""
import time
import numpy as np


def seq_search(records, target):
    """Iterative sequential search on unsorted registration numbers."""
    comps = 0
    for idx, reg in enumerate(records):
        comps += 1
        if reg == target:
            return idx, comps
    return -1, comps


def bin_search_rec(sorted_regs, target, low=0, high=None, comps=0):
    """Recursive binary search on sorted registration numbers."""
    if high is None:
        high = len(sorted_regs) - 1
    if low > high:
        return -1, comps
    mid = low + (high - low) // 2
    comps += 1
    if sorted_regs[mid] == target:
        return mid, comps
    if target < sorted_regs[mid]:
        return bin_search_rec(sorted_regs, target, low, mid - 1, comps)
    return bin_search_rec(sorted_regs, target, mid + 1, high, comps)


def build_hash_map(records):
    """Build hash index mapping registration number -> position in O(n) time."""
    hmap = {}
    for idx, reg in enumerate(records):
        if reg not in hmap:
            hmap[reg] = idx
    return hmap


def hash_search(hmap, target):
    """Lookup registration number in pre-built hash map in O(1) expected time."""
    return hmap.get(target, -1), 1


def main():
    sample = ["192410004", "192410001", "192410008", "192410002", "192410006"]
    s_sample = sorted(sample)
    h_sample = build_hash_map(sample)
    target = "192410006"

    i1, c1 = seq_search(sample, target)
    i2, c2 = bin_search_rec(s_sample, target)
    i3, c3 = hash_search(h_sample, target)

    assert sample[i1] == target
    assert s_sample[i2] == target
    assert sample[i3] == target
    assert seq_search(sample, "000000000")[0] == -1
    assert bin_search_rec(s_sample, "000000000")[0] == -1
    assert hash_search(h_sample, "000000000")[0] == -1
    print(f"Verified: seq_comps={c1}, bin_rec_comps={c2}, hash_comps={c3}")


if __name__ == "__main__":
    main()
