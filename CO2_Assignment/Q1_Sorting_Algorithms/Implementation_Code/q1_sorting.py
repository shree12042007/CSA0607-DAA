"""Q1: Selection Sort, Bubble Sort, and Insertion Sort under contrasting orderings."""
import numpy as np
import pandas as pd

def selection_sort(arr):
    a = list(arr)
    n = len(a)
    comps = swaps = 0
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            comps += 1
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            swaps += 1
    return a, comps, swaps

def bubble_sort(arr):
    a = list(arr)
    n = len(a)
    comps = swaps = 0
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            comps += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                swapped = True
        if not swapped:
            break
    return a, comps, swaps

def insertion_sort(arr):
    a = list(arr)
    n = len(a)
    comps = shifts = 0
    for i in range(1, n):
        key = a[i]
        j = i - 1
        while j >= 0:
            comps += 1
            if a[j] > key:
                a[j + 1] = a[j]
                shifts += 1
                j -= 1
            else:
                break
        a[j + 1] = key
    return a, comps, shifts

def main():
    rng = np.random.default_rng(2026)
    n_orders = 60
    nearly = np.arange(1, n_orders + 1)
    idx = rng.choice(n_orders, size=3, replace=False)
    nearly[idx] = rng.permutation(nearly[idx])
    reverse_arr = np.arange(n_orders, 0, -1).tolist()
    edge_arr = [10, 10, 25, 25, 25, 40, 55, 70, 70, 85, 90, 90, 90, 90, 100]

    datasets = {
        "Nearly_Sorted_95pct": nearly.tolist(),
        "Reverse_Disordered": reverse_arr,
        "Duplicate_Scores_Edge": edge_arr,
    }
    rows = []
    for name, arr in datasets.items():
        for alg, fn in [("Selection", selection_sort), ("Bubble", bubble_sort), ("Insertion", insertion_sort)]:
            _, c, m = fn(arr)
            rows.append({"dataset": name, "algorithm": alg, "comparisons": c, "swaps_or_shifts": m})
    df = pd.DataFrame(rows)
    print(df.to_string(index=False))

if __name__ == "__main__":
    main()
