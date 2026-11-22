"""ShopSphere CO1 Scalability Audit Simulator & Verification Script."""
import math
import pandas as pd

OPS_PER_SEC = 1e8
WINDOW_SEC = 600.0


def m2_exact_audits(n):
    """Exact Audit calls for doubling window i = 1, 2, 4, ..., 2^(k-1) where n = 2^k."""
    if n <= 1:
        return 0
    k = int(math.floor(math.log2(n)))
    return (1 << k) - 1


def s1_expected_comparisons(n, p):
    """Expected comparisons for sequential search with hit probability p."""
    return p * (n + 1) / 2.0 + n * (1.0 - p)


def f_report_generator(n):
    """Profiling operation count f(n) = 3n^2 + 10n log2(n) + 50."""
    return 3.0 * (n ** 2) + 10.0 * n * math.log2(n) + 50.0


def main():
    print("M2 n=1024 exact audits:", m2_exact_audits(1024))
    print("S1 avg comparisons (n=1,000,000, p=0.5):", s1_expected_comparisons(1_000_000, 0.5))

    n = 1_000_000
    rows = [
        ("M1_Current", n * (n - 1) // 2),
        ("M2_RateLimiter", n - 1),
        ("S2_BinarySearch", math.ceil(math.log2(n)) + 1),
        ("M4_Current_Quad", n ** 2),
        ("M4_Redesign_NLogN", int(n * math.log2(n))),
        ("M5_Sales_NLog2N", int(n * (math.log2(n) ** 2))),
    ]
    df = pd.DataFrame([
        {
            "module": name,
            "ops_1M": ops,
            "est_sec_at_1e8_ops": round(ops / OPS_PER_SEC, 6),
            "exceeds_600s_window": (ops / OPS_PER_SEC) > WINDOW_SEC,
        }
        for name, ops in rows
    ])
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
