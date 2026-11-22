"""Production-optimised SentinelOps SOC Alert-Triage Module (Part C & Part E)."""
import math


def sort_alerts(alerts):
    """
    Sort alerts by severity descending while preserving arrival order (stability).
    Effective for streaming/nearly-sorted batches with small local out-of-order shifts.
    """
    arr = list(alerts)
    comparisons = 0
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if arr[j][1] < key[1]:
                arr[j + 1] = arr[j]
                j -= 1
            else:
                break
        arr[j + 1] = key
    return arr, comparisons


def build_blocklist_index(blocklist):
    """Build a hash set from blocklist for O(1) average lookup across repeated SOC queries."""
    return set(blocklist)


def is_blocked(blocklist_or_set, ip):
    """Check if ip is blocked in O(1) average time when given a set/frozenset, or linear scan if list."""
    if isinstance(blocklist_or_set, (set, frozenset)):
        return ip in blocklist_or_set, 1
    comparisons = 0
    for entry in blocklist_or_set:
        comparisons += 1
        if entry == ip:
            return True, comparisons
    return False, comparisons


def find_signature(log, pattern):
    """
    Brute-force pattern search across log with safe mismatch skip when log[i + j] is absent from pattern.
    Preserves exact match positions while avoiding redundant re-scans past non-matching characters.
    """
    n, m = len(log), len(pattern)
    hits = []
    comparisons = 0
    if m == 0 or m > n:
        return hits, comparisons

    pattern_chars = set(pattern)
    last_start = n - m
    i = 0
    while i <= last_start:
        j = 0
        while j < m:
            comparisons += 1
            if log[i + j] != pattern[j]:
                break
            j += 1
        if j == m:
            hits.append(i)
            i += 1
        else:
            mismatch_ch = log[i + j]
            if mismatch_ch not in pattern_chars:
                i = i + j + 1
            else:
                i += 1
    return hits, comparisons


def closest_logins(events):
    """
    Find closest distinct login pair ((i, j), distance) using:
    1) Unordered distinct pairs (eliminating self and duplicate pairs)
    2) Squared distance comparisons inside inner loop (deferring math.sqrt to the end)
    3) Spatial grid bucketing (cell size = sqrt(best_sq)) and |dx|, |dy| bounding-box pruning
    """
    n = len(events)
    if n < 2:
        return None, math.inf, 0

    best_sq = math.inf
    best_pair = None
    dist_calcs = 0

    for i in range(n - 1):
        dx = events[i][0] - events[i + 1][0]
        dy = events[i][1] - events[i + 1][1]
        sq = dx * dx + dy * dy
        dist_calcs += 1
        if sq < best_sq:
            best_sq = sq
            best_pair = (i, i + 1)

    cell_size = math.sqrt(best_sq) if best_sq > 0.0 else 1e-9
    if cell_size == 0.0:
        cell_size = 1e-9

    grid = {}
    for idx, (x, y) in enumerate(events):
        cx = int(math.floor(x / cell_size))
        cy = int(math.floor(y / cell_size))
        grid.setdefault((cx, cy), []).append(idx)

    seen_pairs = set()
    for (cx, cy), bucket in grid.items():
        neighbors = []
        for dcx in (-1, 0, 1):
            for dcy in (-1, 0, 1):
                neighbors.extend(grid.get((cx + dcx, cy + dcy), []))
        for u in bucket:
            ux, uy = events[u]
            for v in neighbors:
                if u == v:
                    continue
                pair = (u, v) if u < v else (v, u)
                if pair in seen_pairs:
                    continue
                seen_pairs.add(pair)
                vx, vy = events[v]
                dx = ux - vx
                if abs(dx) >= cell_size:
                    continue
                dy = uy - vy
                if abs(dy) >= cell_size:
                    continue
                sq = dx * dx + dy * dy
                dist_calcs += 1
                if sq < best_sq:
                    best_sq = sq
                    best_pair = pair
                    if best_sq > 0.0:
                        cell_size = math.sqrt(best_sq)

    min_dist = math.sqrt(best_sq) if best_sq < math.inf else math.inf
    return best_pair, min_dist, dist_calcs
