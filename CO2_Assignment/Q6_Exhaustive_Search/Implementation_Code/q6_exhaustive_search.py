"""Q6: Exhaustive Search for Humanitarian Airlift payload selection."""
import numpy as np
import pandas as pd

def exhaustive_knapsack(packages, max_weight):
    n = len(packages)
    total_subsets = 1 << n
    feasible = 0
    best_val = best_wt = best_mask = 0
    for mask in range(total_subsets):
        w_sum = v_sum = 0
        for i in range(n):
            if (mask >> i) & 1:
                w_sum += packages[i][1]
                v_sum += packages[i][2]
        if w_sum <= max_weight:
            feasible += 1
            if v_sum > best_val:
                best_val, best_wt, best_mask = v_sum, w_sum, mask
    chosen = [packages[i][0] for i in range(n) if (best_mask >> i) & 1]
    return chosen, best_wt, best_val, total_subsets, feasible

def main():
    rng = np.random.default_rng(2026)
    pkgs = [(f"PKG-{i+1:02d}", int(rng.integers(8, 30)), int(rng.integers(25, 140))) for i in range(18)]
    rows = []
    for n_p in (6, 12, 18):
        sub = pkgs[:n_p]
        cap = int(sum(x[1] for x in sub) * 0.45)
        _, bw, bv, tot_s, feas_s = exhaustive_knapsack(sub, cap)
        rows.append({"n": n_p, "cap": cap, "subsets_2n": tot_s, "feasible": feas_s, "best_wt": bw, "best_val": bv})
    print(pd.DataFrame(rows).to_string(index=False))

if __name__ == "__main__":
    main()
