"""Q5: Brute-Force Convex Hull using cross-product half-plane test."""
import numpy as np
import pandas as pd

def cross_product(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def convex_hull_bf(points):
    n = len(points)
    hull_edges = []
    hull_verts = set()
    side_checks = 0
    eps = 1e-9
    for i in range(n):
        for j in range(i + 1, n):
            pos = neg = 0
            for k in range(n):
                if k == i or k == j:
                    continue
                side_checks += 1
                cp = cross_product(points[i], points[j], points[k])
                if cp > eps:
                    pos += 1
                elif cp < -eps:
                    neg += 1
            if pos == 0 or neg == 0:
                hull_edges.append((i, j))
                hull_verts.update([i, j])
    cx = sum(points[idx][0] for idx in hull_verts) / len(hull_verts)
    cy = sum(points[idx][1] for idx in hull_verts) / len(hull_verts)
    ordered = sorted(hull_verts, key=lambda idx: np.arctan2(points[idx][1] - cy, points[idx][0] - cx))
    return ordered, hull_edges, side_checks

def main():
    cfg1 = [(0, 0), (10, 0), (12, 6), (8, 12), (1, 11), (4, 4), (6, 5), (5, 8), (7, 3), (3, 7), (9, 6), (2, 3)]
    cfg2 = [(0, 0), (5, 0), (10, 0), (10, 5), (10, 10), (5, 10), (0, 10), (0, 5), (3, 3), (7, 7), (5, 5), (2, 8), (8, 2)]
    for name, pts in [("Config1", cfg1), ("Config2", cfg2)]:
        o, e, sc = convex_hull_bf(pts)
        print(name, "vertices=", o, "edges=", len(e), "side_checks=", sc)

if __name__ == "__main__":
    main()
