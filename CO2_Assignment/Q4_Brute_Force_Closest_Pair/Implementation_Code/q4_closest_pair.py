"""Q4: Brute-Force Closest Pair for drone positions in 2D."""
import math
import numpy as np
import pandas as pd

def closest_pair_bf(points):
    n = len(points)
    best_d = math.inf
    best_pair = None
    examined = calcs = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            examined += 1
            d = math.hypot(points[i][0] - points[j][0], points[i][1] - points[j][1])
            calcs += 1
            if d < best_d:
                best_d = d
                best_pair = (i, j)
    return best_pair, best_d, examined, calcs

def main():
    rows = []
    for n in (15, 40, 90):
        rng = np.random.default_rng(2026 + n)
        pts = rng.uniform(0, 1000, size=(n, 2)).tolist()
        pair, md, ex, cl = closest_pair_bf(pts)
        rows.append({"n": n, "formula_n_n1_2": n * (n - 1) // 2, "examined": ex, "calcs": cl, "min_dist": round(md, 4)})
    print(pd.DataFrame(rows).to_string(index=False))

if __name__ == "__main__":
    main()
