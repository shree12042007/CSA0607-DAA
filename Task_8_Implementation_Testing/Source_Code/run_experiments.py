"""
run_experiments.py - reproducible benchmark for Tasks 8, 9, 10, 12.
Run:  python run_experiments.py        (takes about 1-2 minutes)

Outputs (relative to the repository root):
  Task_9_Experimental_Performance/results.json, results.csv
  Report/Tables_and_Graphs/*.png
"""
import csv
import heapq
import json
import math
import os
import random
import statistics
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from search_algorithms import (linear_search, sort_records,
                               binary_search_recursive, build_hash_table)

SEED = 2024
SIZES = [1_000, 10_000, 100_000, 1_000_000]
Q = 100                      # queries per query-set (successful / unsuccessful)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT9 = os.path.join(ROOT, "Task_9_Experimental_Performance")
GRAPHS = os.path.join(ROOT, "Report", "Tables_and_Graphs")


def timed(fn, *a):
    t = time.perf_counter()
    r = fn(*a)
    return r, time.perf_counter() - t


def batch(fn, queries):
    """Average comparisons and average time (microseconds) over queries."""
    comps = 0
    t0 = time.perf_counter()
    for q in queries:
        comps += fn(q)[1]
    dt = time.perf_counter() - t0
    return comps / len(queries), dt / len(queries) * 1e6


def median_time_us(fn, key, reps=5):
    ts = []
    c = 0
    for _ in range(reps):
        t = time.perf_counter()
        c = fn(key)[1]
        ts.append((time.perf_counter() - t) * 1e6)
    return c, statistics.median(ts)


def main():
    rows = []
    extra = {}
    print("=" * 78)
    print("EXPERIMENTAL EVALUATION  (seed=%d, %d queries per query-set)" % (SEED, Q))
    print("=" * 78)
    for n in SIZES:
        rng = random.Random(SEED + n)
        records = rng.sample(range(10**8, 10**9), n)       # unique 9-digit reg. numbers, unsorted
        present = set(records)
        succ = [rng.choice(records) for _ in range(Q)]
        unsucc = []
        while len(unsucc) < Q:
            k = rng.randrange(10**8, 10**9)
            if k not in present:
                unsucc.append(k)

        # ---- preprocessing ----
        sorted_recs, t_sort = timed(sort_records, records)
        ht, t_hash = timed(build_hash_table, records)

        algos = {
            "Linear (iterative)": (lambda k: linear_search(records, k), 0.0, records[0], records[-1]),
            "Binary (recursive)": (lambda k: binary_search_recursive(sorted_recs, k), t_sort,
                                   sorted_recs[(n - 1) // 2], None),
            "Hash (chaining)":    (lambda k: ht.search(k), t_hash, None, None),
        }
        print(f"\n--- n = {n:,} ---   (hash: m={ht.m:,}, load factor={ht.load_factor():.3f})")
        print(f"{'Algorithm':20s}{'prep(ms)':>10s}{'avgC succ':>11s}{'avgC fail':>11s}"
              f"{'t succ(us)':>12s}{'t fail(us)':>12s}{'worstC':>9s}")
        for name, (fn, prep, best_key, worst_key) in algos.items():
            c_s, t_s = batch(fn, succ)
            c_u, t_u = batch(fn, unsucc)
            if name.startswith("Linear"):
                best_c, _ = median_time_us(fn, records[0], 3)
                worst_c, worst_t = median_time_us(fn, records[-1], 3)
            elif name.startswith("Binary"):
                best_c, _ = median_time_us(fn, sorted_recs[(n - 1) // 2], 3)
                worst_c = max(fn(k)[1] for k in unsucc)
                worst_t = t_u
            else:
                best_c, worst_c = 0, max(fn(k)[1] for k in succ + unsucc)
                worst_t = t_u
            row = dict(algorithm=name, n=n, prep_ms=prep * 1e3,
                       avg_comps_success=c_s, avg_comps_fail=c_u,
                       avg_time_success_us=t_s, avg_time_fail_us=t_u,
                       best_comps=best_c, worst_comps=worst_c)
            rows.append(row)
            print(f"{name:20s}{prep*1e3:10.2f}{c_s:11.2f}{c_u:11.2f}"
                  f"{t_s:12.2f}{t_u:12.2f}{worst_c:9d}")

        # ---- longest chain & verify correctness at this size ----
        longest = max(len(b) for b in ht.buckets)
        ok = all((linear_search(records, k)[0] != -1) == (binary_search_recursive(sorted_recs, k)[0] != -1)
                 == (ht.search(k)[0] != -1) for k in succ[:20] + unsucc[:20])
        print(f"   correctness check (40 queries, all 3 agree): {'OK' if ok else 'MISMATCH'};"
              f"  longest hash chain = {longest}")
        extra[n] = dict(longest_chain=longest, agree=ok, hash_m=ht.m)

        # ---- daily-update experiment (only at 1M) ----
        if n == 1_000_000:
            new_keys = []
            while len(new_keys) < 1000:
                k = rng.randrange(10**8, 10**9)
                if k not in present:
                    new_keys.append(k)
            t = time.perf_counter()
            for i, k in enumerate(new_keys):
                ht.insert(k, n + i)
            t_hins = time.perf_counter() - t
            t = time.perf_counter()
            merged = list(heapq.merge(sorted_recs, sorted(new_keys)))
            t_merge = time.perf_counter() - t
            t = time.perf_counter()
            _ = sorted(sorted_recs + new_keys)
            t_resort = time.perf_counter() - t
            extra["daily_update_1000_new_records_s"] = dict(
                hash_insert=t_hins, sorted_merge=t_merge, full_resort=t_resort)
            print(f"\n   Daily update of 1,000 new records at n=1,000,000:"
                  f" hash insert={t_hins*1e3:.2f} ms, sorted merge O(n+k)={t_merge*1e3:.1f} ms,"
                  f" full re-sort={t_resort*1e3:.1f} ms")

    # ------------------------------------------------------------------ save
    os.makedirs(OUT9, exist_ok=True)
    os.makedirs(GRAPHS, exist_ok=True)
    with open(os.path.join(OUT9, "results.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    # ---------------------------------------------- Task 12 projection
    big = {r["algorithm"]: r for r in rows if r["n"] == 1_000_000}
    per_hour, per_day = 50_000, 50_000 * 24
    per_sec = per_hour / 3600
    proj = {}
    for name, r in big.items():
        t_avg_us = (r["avg_time_success_us"] + r["avg_time_fail_us"]) / 2   # 50/50 mix
        daily_search_s = per_day * t_avg_us / 1e6
        proj[name] = dict(avg_search_us=t_avg_us,
                          cpu_utilisation_pct=per_sec * t_avg_us / 1e6 * 100,
                          prep_s_per_day=r["prep_ms"] / 1e3,
                          search_s_per_day=daily_search_s,
                          total_s_per_day=daily_search_s + r["prep_ms"] / 1e3)
    # break-even number of searches vs linear (at n = 1e6)
    lin_us = (big["Linear (iterative)"]["avg_time_success_us"] + big["Linear (iterative)"]["avg_time_fail_us"]) / 2
    breakeven = {}
    for name in ("Binary (recursive)", "Hash (chaining)"):
        t_avg = proj[name]["avg_search_us"]
        breakeven[name] = (big[name]["prep_ms"] * 1e3) / (lin_us - t_avg)
    extra["task12_projection"] = proj
    extra["breakeven_searches_vs_linear_n1e6"] = breakeven
    extra["requests_per_second"] = per_sec

    with open(os.path.join(OUT9, "results.json"), "w") as f:
        json.dump(dict(rows=rows, extra={str(k): v for k, v in extra.items()}), f, indent=2)

    print("\n" + "=" * 78)
    print("TASK 12 PROJECTION  (50,000 searches/hour = %.2f/s = %d/day, n = 1,000,000)" % (per_sec, per_day))
    print("=" * 78)
    print(f"{'Algorithm':20s}{'avg search(us)':>15s}{'CPU util %':>12s}{'prep s/day':>12s}"
          f"{'search s/day':>14s}{'total s/day':>13s}")
    for name, p in proj.items():
        print(f"{name:20s}{p['avg_search_us']:15.2f}{p['cpu_utilisation_pct']:12.3f}"
              f"{p['prep_s_per_day']:12.3f}{p['search_s_per_day']:14.2f}{p['total_s_per_day']:13.2f}")
    for k, v in breakeven.items():
        print(f"Break-even vs linear for {k}: {v:,.0f} searches")

    # ------------------------------------------------------------------ graphs
    names = ["Linear (iterative)", "Binary (recursive)", "Hash (chaining)"]
    colors = {"Linear (iterative)": "tab:red", "Binary (recursive)": "tab:blue", "Hash (chaining)": "tab:green"}

    def series(name, key):
        return [r[key] for r in rows if r["algorithm"] == name]

    # 1 comparisons
    plt.figure(figsize=(7, 5))
    for nm in names:
        plt.plot(SIZES, series(nm, "avg_comps_success"), "o-", label=nm, color=colors[nm])
    plt.xscale("log"); plt.yscale("log")
    plt.xlabel("n (records)"); plt.ylabel("avg comparisons (successful search)")
    plt.title("Average comparisons vs n"); plt.grid(True, which="both", alpha=.3); plt.legend()
    plt.tight_layout(); plt.savefig(os.path.join(GRAPHS, "graph1_comparisons.png"), dpi=150); plt.close()

    # 2 search time
    plt.figure(figsize=(7, 5))
    for nm in names:
        plt.plot(SIZES, series(nm, "avg_time_success_us"), "o-", label=nm, color=colors[nm])
    plt.xscale("log"); plt.yscale("log")
    plt.xlabel("n (records)"); plt.ylabel("avg search time (microseconds)")
    plt.title("Average search time vs n (successful)"); plt.grid(True, which="both", alpha=.3); plt.legend()
    plt.tight_layout(); plt.savefig(os.path.join(GRAPHS, "graph2_search_time.png"), dpi=150); plt.close()

    # 3 preprocessing
    plt.figure(figsize=(7, 5))
    for nm in names[1:]:
        plt.plot(SIZES, series(nm, "prep_ms"), "o-", label=nm + " preprocessing", color=colors[nm])
    plt.xscale("log"); plt.yscale("log")
    plt.xlabel("n (records)"); plt.ylabel("preprocessing time (ms)")
    plt.title("Preprocessing cost vs n (linear = 0)"); plt.grid(True, which="both", alpha=.3); plt.legend()
    plt.tight_layout(); plt.savefig(os.path.join(GRAPHS, "graph3_preprocessing.png"), dpi=150); plt.close()

    # 4 theory vs experiment (comparisons)
    plt.figure(figsize=(7, 5))
    xs = SIZES
    plt.plot(xs, series("Linear (iterative)", "avg_comps_success"), "o", color="tab:red", label="Linear measured")
    plt.plot(xs, [(n + 1) / 2 for n in xs], "--", color="tab:red", label="Linear theory (n+1)/2")
    plt.plot(xs, series("Binary (recursive)", "avg_comps_success"), "o", color="tab:blue", label="Binary measured")
    plt.plot(xs, [math.log2(n + 1) - 1 for n in xs], "--", color="tab:blue", label="Binary theory ~log2(n+1)-1")
    plt.plot(xs, series("Hash (chaining)", "avg_comps_success"), "o", color="tab:green", label="Hash measured")
    plt.plot(xs, [1 + 0.75 / 2] * len(xs), "--", color="tab:green", label="Hash theory 1+alpha/2")
    plt.xscale("log"); plt.yscale("log")
    plt.xlabel("n"); plt.ylabel("avg comparisons")
    plt.title("Theory vs experiment (successful search)"); plt.grid(True, which="both", alpha=.3)
    plt.legend(fontsize=8); plt.tight_layout()
    plt.savefig(os.path.join(GRAPHS, "graph4_theory_vs_experiment.png"), dpi=150); plt.close()

    # 5 total cost for k searches at n = 1e6
    plt.figure(figsize=(7, 5))
    ks = [10 ** e for e in range(0, 8)]
    for nm in names:
        prep = big[nm]["prep_ms"] / 1e3
        t = proj[nm]["avg_search_us"] / 1e6
        plt.plot(ks, [prep + k * t for k in ks], "o-", label=nm, color=colors[nm])
    plt.axvline(per_day, color="gray", ls=":", label="1.2 million searches/day")
    plt.xscale("log"); plt.yscale("log")
    plt.xlabel("number of searches k"); plt.ylabel("total time = preprocessing + k searches (s)")
    plt.title("Total cost vs number of searches (n = 1,000,000)")
    plt.grid(True, which="both", alpha=.3); plt.legend(fontsize=8); plt.tight_layout()
    plt.savefig(os.path.join(GRAPHS, "graph5_total_cost_vs_searches.png"), dpi=150); plt.close()
    print("\nResults and graphs saved.")


if __name__ == "__main__":
    main()
