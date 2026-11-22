"""Q3: Brute-Force String Matching across contrasting text-pattern structures."""
import pandas as pd

def brute_force_search(text, pattern):
    n, m = len(text), len(pattern)
    comps = 0
    matches = []
    if m == 0 or m > n:
        return matches, comps
    for i in range(n - m + 1):
        j = 0
        while j < m:
            comps += 1
            if text[i + j] != pattern[j]:
                break
            j += 1
        if j == m:
            matches.append(i)
    return matches, comps

def main():
    cases = [
        ("1_Low_Work_Distinct", "AUTH_OK_SESSION_9941_PORT_443_TLS13_VERIFIED_NODE_ALPHA", "DROP_ROOT"),
        ("2_High_Work_WorstCase", "A" * 80 + "B", "A" * 20 + "B"),
        ("3_Repeated_Prefix_PartialHit", ("SCAN_ERR_001_" * 6) + "SCAN_ERR_002_ALERT", "SCAN_ERR_002"),
    ]
    rows = []
    for name, t, p in cases:
        m_idx, comps = brute_force_search(t, p)
        rows.append({"case": name, "n": len(t), "m": len(p), "hits": len(m_idx), "char_comparisons": comps})
    print(pd.DataFrame(rows).to_string(index=False))

if __name__ == "__main__":
    main()
