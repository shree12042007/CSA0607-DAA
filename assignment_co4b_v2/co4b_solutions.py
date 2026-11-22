"""
co4b_solutions.py
CSA06 Design and Analysis of Algorithms - Assignment 4B (CO4)
Department of Computer Science and Bioscience
SIMATS Engineering

Implements, instruments, tests, and benchmarks Tasks 1 through 6:
  Task 1: Word Wrap via Dynamic Programming
  Task 2: Fractional Knapsack (Greedy) vs. 0/1 Knapsack (Dynamic Programming)
  Task 3: Routing Engine (Dijkstra, Bellman-Ford, Floyd-Warshall, Warshall)
  Task 4: Assembly Line Scheduling via Dynamic Programming (2-line & 3-line analysis)
  Task 5: Minimum Spanning Tree (Kruskal, Prim, Boruvka)
  Task 6: Travelling Salesperson Problem via Bitmask Dynamic Programming (Held-Karp)

Run with:
  python co4b_solutions.py --all
  python co4b_solutions.py --task1 ... --task6
"""

import argparse
import csv
import heapq
import itertools
import math
import os
import platform
import random
import time
import tracemalloc

SEED = 2026


def ensure_dirs():
    for folder in ("data", "figures", "screenshots"):
        os.makedirs(folder, exist_ok=True)


def write_csv(filename, rows):
    if not rows:
        return
    ensure_dirs()
    path = os.path.join("data", filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def clock(fn, *args, **kwargs):
    t0 = time.perf_counter()
    res = fn(*args, **kwargs)
    return res, time.perf_counter() - t0


# ==============================================================================
# TASK 1: WORD WRAP AS A DOCUMENT-LAYOUT ENGINE (DYNAMIC PROGRAMMING)
# ==============================================================================
def word_wrap_dp(words, max_width):
    n = len(words)
    if n == 0:
        return {
            "total_penalty": 0,
            "lines": [],
            "unused_spaces": [],
            "line_penalties": [],
            "states_evaluated": 0,
            "steps": [],
        }

    for w in words:
        if len(w) > max_width:
            raise ValueError(f"Word '{w}' (len={len(w)}) exceeds max line width W={max_width}")

    dp = [math.inf] * (n + 1)
    choice = [-1] * (n + 1)
    dp[n] = 0
    states = 0
    steps = []

    for i in range(n - 1, -1, -1):
        line_len = 0
        cands = []
        for j in range(i + 1, n + 1):
            w_len = len(words[j - 1])
            line_len = w_len if j == i + 1 else (line_len + 1 + w_len)
            if line_len > max_width:
                break
            unused = max_width - line_len
            pen = 0 if j == n else (unused * unused)
            total_sub = pen + dp[j]
            states += 1
            cands.append((j, unused, pen, dp[j], total_sub))
            if total_sub < dp[i]:
                dp[i] = total_sub
                choice[i] = j
        steps.append({"i": i, "word": words[i], "best": dp[i], "next": choice[i], "cands": cands})

    lines, unused_list, pen_list = [], [], []
    idx = 0
    while idx < n:
        end = choice[idx]
        text = " ".join(words[idx:end])
        unused = max_width - len(text)
        pen = 0 if end == n else (unused * unused)
        lines.append(text)
        unused_list.append(unused)
        pen_list.append(pen)
        idx = end

    return {
        "total_penalty": dp[0],
        "lines": lines,
        "unused_spaces": unused_list,
        "line_penalties": pen_list,
        "states_evaluated": states,
        "steps": steps,
    }


def run_task1(log):
    log("\n=== TASK 1: WORD WRAP DP ===")
    text = "bioscience algorithms optimize sequence alignment and metabolic layout cleanly"
    words = text.split()
    base = word_wrap_dp(words, 22)
    log(f"Base W=22 -> penalty={base['total_penalty']}, states={base['states_evaluated']}")
    for k, (ln, sp, pn) in enumerate(zip(base["lines"], base["unused_spaces"], base["line_penalties"]), 1):
        log(f"  Line {k}: '{ln}' | unused={sp} | pen={pn}")

    rows = []
    for w in (16, 22, 30):
        r = word_wrap_dp(words, w)
        rows.append({
            "width_W": w,
            "lines": len(r["lines"]),
            "total_penalty": r["total_penalty"],
            "line_penalties": str(r["line_penalties"]),
        })
        log(f"  Width W={w}: lines={len(r['lines'])}, penalty={r['total_penalty']}, pens={r['line_penalties']}")

    exact = word_wrap_dp(["genomics"], 8)
    log(f"  Boundary exact fit: penalty={exact['total_penalty']}")
    try:
        word_wrap_dp(["transcriptomics"], 10)
    except ValueError as err:
        log(f"  Boundary oversized caught: {err}")

    write_csv("task1_widths.csv", rows)


# ==============================================================================
# TASK 2: FRACTIONAL KNAPSACK (GREEDY) VS. 0/1 KNAPSACK (DP)
# ==============================================================================
def fractional_knapsack(items, capacity):
    ops = 0
    ordered = []
    for iid, w, v in items:
        ops += 1
        ordered.append((v / w, iid, w, v))
    ordered.sort(key=lambda x: x[0], reverse=True)

    rem = float(capacity)
    total = 0.0
    chosen = []
    for ratio, iid, w, v in ordered:
        ops += 1
        if rem <= 0:
            continue
        if w <= rem:
            rem -= w
            total += v
            chosen.append((iid, 1.0, w, float(v)))
        else:
            frac = rem / w
            total += v * frac
            chosen.append((iid, round(frac, 4), rem, round(v * frac, 2)))
            rem = 0.0
    return total, chosen, ops


def greedy_01(items, capacity):
    ops = 0
    rem = capacity
    val = 0
    chosen = []
    for iid, w, v in sorted(items, key=lambda x: x[2] / x[1], reverse=True):
        ops += 1
        if w <= rem:
            rem -= w
            val += v
            chosen.append((iid, w, v))
    return val, chosen, ops


def dp_01(items, capacity):
    n = len(items)
    cap = int(capacity)
    dp = [[0] * (cap + 1) for _ in range(n + 1)]
    states = 0
    for i in range(1, n + 1):
        _, w, v = items[i - 1]
        wi = int(w)
        for c in range(cap + 1):
            states += 1
            if wi <= c and v + dp[i - 1][c - wi] > dp[i - 1][c]:
                dp[i][c] = v + dp[i - 1][c - wi]
            else:
                dp[i][c] = dp[i - 1][c]

    picked = []
    c = cap
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i - 1][c]:
            iid, w, v = items[i - 1]
            picked.append((iid, w, v))
            c -= int(w)
    picked.reverse()
    return dp[n][cap], picked, states


def run_task2(log):
    log("\n=== TASK 2: GREEDY VS. DP KNAPSACK ===")
    g_val, g_sel, g_ops = fractional_knapsack([("PKG-A", 10, 60), ("PKG-B", 20, 100), ("PKG-C", 30, 120)], 50)
    log(f"  Fractional normal case: val={g_val:.2f}, selected={g_sel}, ops={g_ops}")

    counter = [("CRATE-1", 10, 90), ("CRATE-2", 20, 100), ("CRATE-3", 30, 120)]
    g01_v, g01_s, _ = greedy_01(counter, 50)
    dp01_v, dp01_s, _ = dp_01(counter, 50)
    log(f"  0/1 Counterexample: greedy={g01_v} {g01_s} vs DP={dp01_v} {dp01_s}")

    rows = []
    for n_items in (5, 10, 15, 20, 25):
        rng = random.Random(SEED + n_items)
        arr = [(f"I{k+1:02d}", rng.randint(5, 35), rng.randint(20, 150)) for k in range(n_items)]
        cap = n_items * 15
        tracemalloc.start()
        (_, _, gc), tg = clock(fractional_knapsack, arr, cap)
        _, g_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        tracemalloc.start()
        (dv, _, dst), tdp = clock(dp_01, arr, cap)
        _, d_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        rows.append({
            "n_items": n_items,
            "capacity": cap,
            "greedy_ops": gc,
            "greedy_ms": round(tg * 1e3, 4),
            "greedy_kb": round(g_mem / 1024.0, 2),
            "dp_states": dst,
            "dp_ms": round(tdp * 1e3, 4),
            "dp_kb": round(d_mem / 1024.0, 2),
            "dp_val": dv,
        })
    write_csv("task2_comparison.csv", rows)


# ==============================================================================
# TASK 3: ROUTING ENGINE (DIJKSTRA, BELLMAN-FORD, FLOYD-WARSHALL, WARSHALL)
# ==============================================================================
def sample_routing_graph():
    nodes = ["0:Hub", "1:North", "2:East", "3:South", "4:West", "5:Harbor", "6:Industrial", "7:Airport"]
    edges = [
        (0, 1, 4), (0, 2, 2), (0, 3, 9),
        (1, 2, 5), (1, 4, 10),
        (2, 3, 3), (2, 5, 8),
        (3, 4, 2), (3, 6, 7),
        (4, 6, 4), (4, 7, 12),
        (5, 7, 6),
        (6, 7, 3),
    ]
    return nodes, edges


def run_dijkstra(n, edges, src):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [math.inf] * n
    parent = [None] * n
    done = [False] * n
    dist[src] = 0.0
    pq = [(0.0, src)]
    order = []
    while pq:
        d, u = heapq.heappop(pq)
        if done[u]:
            continue
        done[u] = True
        order.append((u, d))
        for v, w in adj[u]:
            if not done[v] and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))
    return dist, parent, order


def run_bellman_ford(n, edges, src):
    dist = [math.inf] * n
    parent = [None] * n
    dist[src] = 0.0
    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if not math.isinf(dist[u]) and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                changed = True
        if not changed:
            break
    neg_cycle = any((not math.isinf(dist[u]) and dist[u] + w < dist[v]) for u, v, w in edges)
    return dist, parent, neg_cycle


def run_floyd_warshall_warshall(n, edges):
    fw = [[math.inf] * n for _ in range(n)]
    reach = [[False] * n for _ in range(n)]
    for i in range(n):
        fw[i][i] = 0.0
        reach[i][i] = True
    for u, v, w in edges:
        if float(w) < fw[u][v]:
            fw[u][v] = float(w)
        reach[u][v] = True
    for k in range(n):
        for i in range(n):
            if math.isinf(fw[i][k]) and not reach[i][k]:
                continue
            for j in range(n):
                if not math.isinf(fw[k][j]) and fw[i][k] + fw[k][j] < fw[i][j]:
                    fw[i][j] = fw[i][k] + fw[k][j]
                if reach[i][k] and reach[k][j]:
                    reach[i][j] = True
    return fw, reach


def run_task3(log):
    log("\n=== TASK 3: ROUTING ENGINE ===")
    nodes, edges = sample_routing_graph()
    n = len(nodes)
    d_dist, d_par, d_ord = run_dijkstra(n, edges, 0)
    log(f"  Stage A Dijkstra dists={d_dist}, finalized={d_ord}")

    edges_b = edges + [(3, 1, -8)]
    db_dist, _, _ = run_dijkstra(n, edges_b, 0)
    bfb_dist, _, bfb_neg = run_bellman_ford(n, edges_b, 0)
    log(f"  Stage B neg edge (3->1, -8): Dijkstra dist[1]={db_dist[1]} vs Bellman-Ford dist[1]={bfb_dist[1]}, neg_cycle={bfb_neg}")

    edges_c = edges_b + [(4, 3, -5)]
    _, _, bfc_neg = run_bellman_ford(n, edges_c, 0)
    log(f"  Stage C neg cycle detected={bfc_neg}")

    fw, reach = run_floyd_warshall_warshall(n, edges)
    log(f"  Stage D Floyd-Warshall row 0={[int(x) for x in fw[0]]}, reach row 0={[int(x) for x in reach[0]]}")


# ==============================================================================
# TASK 4: ASSEMBLY LINE SCHEDULING (DP)
# ==============================================================================
def assembly_schedule(p1, p2, t12, t21, e1, e2, x1, x2):
    n = len(p1)
    f1 = [0] * n
    f2 = [0] * n
    l1 = [1] * n
    l2 = [2] * n
    f1[0] = e1 + p1[0]
    f2[0] = e2 + p2[0]
    traces = []

    for j in range(1, n):
        s1, tr1 = f1[j - 1] + p1[j], f2[j - 1] + t21[j - 1] + p1[j]
        if s1 <= tr1:
            f1[j], l1[j], sel1 = s1, 1, "STAY"
        else:
            f1[j], l1[j], sel1 = tr1, 2, "TRANSFER"

        s2, tr2 = f2[j - 1] + p2[j], f1[j - 1] + t12[j - 1] + p2[j]
        if s2 <= tr2:
            f2[j], l2[j], sel2 = s2, 2, "STAY"
        else:
            f2[j], l2[j], sel2 = tr2, 1, "TRANSFER"

        traces.append((j + 1, s1, tr1, sel1, s2, tr2, sel2))

    if f1[n - 1] + x1 <= f2[n - 1] + x2:
        total, cur_line = f1[n - 1] + x1, 1
    else:
        total, cur_line = f2[n - 1] + x2, 2

    seq = [0] * n
    seq[n - 1] = cur_line
    for j in range(n - 1, 0, -1):
        seq[j - 1] = l1[j] if seq[j] == 1 else l2[j]

    return total, seq, traces


def run_task4(log):
    log("\n=== TASK 4: ASSEMBLY LINE SCHEDULING ===")
    p1, p2 = [7, 9, 3, 4, 8, 4], [8, 5, 6, 4, 5, 7]
    t12, t21 = [2, 3, 1, 3, 4], [2, 1, 2, 2, 1]
    tot, seq, tr = assembly_schedule(p1, p2, t12, t21, 2, 4, 3, 2)
    log(f"  Base min_time={tot}, seq={seq}")
    for row in tr:
        log(f"    Station {row[0]}: L1(stay={row[1]}, xfer={row[2]}->{row[3]}) | L2(stay={row[4]}, xfer={row[5]}->{row[6]})")


# ==============================================================================
# TASK 5: KRUSKAL, PRIM & BORUVKA MST
# ==============================================================================
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


def mst_kruskal(n, edges):
    uf = UnionFind(n)
    mst, trace, cost = [], [], 0
    for u, v, w in sorted(edges, key=lambda e: (e[2], e[0], e[1])):
        if uf.union(u, v):
            mst.append((u, v, w))
            cost += w
            trace.append(f"+({u},{v},w={w})")
    return cost, mst, trace


def mst_prim(n, edges, start=0):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    seen = [False] * n
    seen[start] = True
    pq = [(w, start, v) for v, w in adj[start]]
    heapq.heapify(pq)
    mst, trace, cost = [], [], 0
    while pq and len(mst) < n - 1:
        w, u, v = heapq.heappop(pq)
        if seen[v]:
            continue
        seen[v] = True
        mst.append((u, v, w))
        cost += w
        trace.append(f"+({u},{v},w={w})")
        for nxt, nw in adj[v]:
            if not seen[nxt]:
                heapq.heappush(pq, (nw, v, nxt))
    return cost, mst, trace


def mst_boruvka(n, edges):
    uf = UnionFind(n)
    comps = n
    mst, trace, cost = [], [], 0
    while comps > 1:
        cheapest = {}
        for u, v, w in edges:
            ru, rv = uf.find(u), uf.find(v)
            if ru == rv:
                continue
            if ru not in cheapest or (w, u, v) < cheapest[ru]:
                cheapest[ru] = (w, u, v)
            if rv not in cheapest or (w, u, v) < cheapest[rv]:
                cheapest[rv] = (w, u, v)
        merged = 0
        for _, (w, u, v) in sorted(cheapest.items()):
            if uf.union(u, v):
                mst.append((u, v, w))
                cost += w
                comps -= 1
                merged += 1
                trace.append(f"+({u},{v},w={w})")
        if merged == 0:
            break
    return cost, mst, trace


def run_task5(log):
    log("\n=== TASK 5: KRUSKAL, PRIM & BORUVKA MST ===")
    n = 7
    edges = [
        (0, 1, 7), (0, 2, 5), (0, 3, 9), (1, 2, 8), (1, 4, 6), (1, 5, 11),
        (2, 3, 4), (2, 5, 10), (3, 4, 3), (3, 6, 12), (4, 5, 2), (4, 6, 8),
    ]
    kc, ke, kt = mst_kruskal(n, edges)
    pc, pe, pt = mst_prim(n, edges, 0)
    bc, be, bt = mst_boruvka(n, edges)
    log(f"  Kruskal={kc} {kt} | Prim={pc} {pt} | Boruvka={bc} {bt}")


# ==============================================================================
# TASK 6: TSP VIA BITMASK DP (HELD-KARP)
# ==============================================================================
def tsp_dp(cost_mat):
    n = len(cost_mat)
    full = (1 << n) - 1
    dp = [[math.inf] * n for _ in range(1 << n)]
    parent = [[-1] * n for _ in range(1 << n)]
    dp[1][0] = 0.0
    states = 1

    for mask in range(1, 1 << n, 2):
        for u in range(1, n):
            if not (mask & (1 << u)):
                continue
            prev_mask = mask ^ (1 << u)
            if prev_mask == 0:
                continue
            best_c = math.inf
            best_p = -1
            for p in range(n):
                if (prev_mask & (1 << p)) and not math.isinf(dp[prev_mask][p]):
                    states += 1
                    cand = dp[prev_mask][p] + cost_mat[p][u]
                    if cand < best_c:
                        best_c, best_p = cand, p
            dp[mask][u] = best_c
            parent[mask][u] = best_p

    ans = math.inf
    last = -1
    for u in range(1, n):
        if not math.isinf(dp[full][u]):
            total = dp[full][u] + cost_mat[u][0]
            if total < ans:
                ans, last = total, u

    route = []
    if last != -1:
        cur, m = last, full
        while cur != -1:
            route.append(cur)
            nxt = parent[m][cur]
            m ^= (1 << cur)
            cur = nxt
        route.extend([0])
        route.reverse()
        route.append(0)
    return ans, route, states


def tsp_exhaustive(cost_mat):
    n = len(cost_mat)
    best = math.inf
    best_r = None
    for perm in itertools.permutations(range(1, n)):
        c = cost_mat[0][perm[0]] + sum(cost_mat[perm[i]][perm[i + 1]] for i in range(len(perm) - 1)) + cost_mat[perm[-1]][0]
        if c < best:
            best, best_r = c, [0] + list(perm) + [0]
    return best, best_r


def synth_matrix(n, seed=SEED):
    rng = random.Random(seed + n)
    pts = [(rng.uniform(0, 50), rng.uniform(0, 50)) for _ in range(n)]
    mat = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                mat[i][j] = round(math.hypot(pts[i][0] - pts[j][0], pts[i][1] - pts[j][1]), 2)
    return mat


def run_task6(log):
    log("\n=== TASK 6: TSP BITMASK DP ===")
    labels7 = ["Hub", "A", "B", "C", "D", "E", "F"]
    c7, r7, s7 = tsp_dp(synth_matrix(7, SEED))
    log(f"  n=7 (Hub + 6 stops): cost={c7:.2f}, route={' -> '.join(labels7[i] for i in r7)}, states={s7}")

    m5 = synth_matrix(5, SEED + 10)
    c5_dp, r5_dp, _ = tsp_dp(m5)
    c5_ex, r5_ex = tsp_exhaustive(m5)
    log(f"  n=5 validation: DP={c5_dp:.2f} {r5_dp} vs Exhaustive={c5_ex:.2f} {r5_ex}")

    rows = []
    for n_loc in (4, 5, 6, 7, 8, 9, 10):
        mat = synth_matrix(n_loc, SEED + n_loc)
        tracemalloc.start()
        (val, _, st), dt = clock(tsp_dp, mat)
        _, mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        rows.append({
            "locations": n_loc,
            "states_evaluated": st,
            "time_ms": round(dt * 1e3, 3),
            "peak_kb": round(mem / 1024.0, 2),
            "min_cost": round(val, 2),
        })
        log(f"  n={n_loc}: states={st:>7,}, time={dt*1e3:7.2f} ms, mem={mem/1024:7.1f} KB")
    write_csv("task6_growth.csv", rows)


def main():
    parser = argparse.ArgumentParser()
    for t in ("task1", "task2", "task3", "task4", "task5", "task6", "all"):
        parser.add_argument(f"--{t}", action="store_true")
    args = parser.parse_args()
    ensure_dirs()
    log_out = []

    def log(msg):
        print(msg)
        log_out.append(msg)

    log(f"Python {platform.python_version()} | {platform.platform()} | Seed={SEED}")
    if args.task1 or args.all:
        run_task1(log)
    if args.task2 or args.all:
        run_task2(log)
    if args.task3 or args.all:
        run_task3(log)
    if args.task4 or args.all:
        run_task4(log)
    if args.task5 or args.all:
        run_task5(log)
    if args.task6 or args.all:
        run_task6(log)

    with open("execution_output.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(log_out) + "\n")


if __name__ == "__main__":
    main()
