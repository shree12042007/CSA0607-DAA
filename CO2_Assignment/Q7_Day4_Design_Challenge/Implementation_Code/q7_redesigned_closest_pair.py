"""Q7 Day-4 Design Challenge: Grid-Bucketed + Bounding-Box Pruned Closest Pair."""
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

def closest_pair_redesigned_grid(points):
    n = len(points)
    if n < 2:
        return None, math.inf, 0, 0
    best_d = math.inf
    best_pair = None
    calcs = 0
    for i in range(n - 1):
        d0 = math.hypot(points[i][0] - points[i + 1][0], points[i][1] - points[i + 1][1])
        calcs += 1
        if d0 < best_d:
            best_d = d0
            best_pair = (i, i + 1)

    cell = max(best_d, 1e-9)
    grid = {}
    for idx, (x, y) in enumerate(points):
        grid.setdefault((int(x // cell), int(y // cell)), []).append(idx)

    seen = set()
    for (cx, cy), bucket in grid.items():
        nbrs = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                nbrs.extend(grid.get((cx + dx, cy + dy), []))
        for u in bucket:
            ux, uy = points[u]
            for v in nbrs:
                if u == v:
                    continue
                pair = (u, v) if u < v else (v, u)
                if pair in seen:
                    continue
                seen.add(pair)
                vx, vy = points[v]
                if abs(ux - vx) >= best_d or abs(uy - vy) >= best_d:
                    continue
                d = math.hypot(ux - vx, uy - vy)
                calcs += 1
                if d < best_d:
                    best_d = d
                    best_pair = pair
    return best_pair, best_d, len(seen), calcs

def main():
    rows = []
    for n in (15, 40, 90):
        rng = np.random.default_rng(2026 + n)
        pts = rng.uniform(0, 1000, size=(n, 2)).tolist()
        _, md0, ex0, cl0 = closest_pair_bf(pts)
        _, md1, ex1, cl1 = closest_pair_redesigned_grid(pts)
        rows.append({"n": n, "orig_calcs": cl0, "new_pairs": ex1, "new_calcs": cl1, "min_dist": round(md1, 4)})
    print(pd.DataFrame(rows).to_string(index=False))

if __name__ == "__main__":
    main()
