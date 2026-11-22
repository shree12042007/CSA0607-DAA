"""Corrected SentinelOps SOC Alert-Triage Module (all 9 defects resolved)."""
import math


def sort_alerts(alerts):
    """Sort alert tuples (alert_id, severity) by highest severity first, preserving arrival order."""
    arr = list(alerts)
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j][1] < key[1]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def is_blocked(blocklist, ip):
    """Return True if ip appears anywhere in blocklist, else False."""
    for entry in blocklist:
        if entry == ip:
            return True
    return False


def find_signature(log, pattern):
    """Return all starting indices where pattern occurs in log (inclusive of end boundary)."""
    n, m = len(log), len(pattern)
    hits = []
    if m == 0 or m > n:
        return hits
    for i in range(n - m + 1):
        matched = True
        for j in range(m):
            if log[i + j] != pattern[j]:
                matched = False
                break
        if matched:
            hits.append(i)
    return hits


def closest_logins(events):
    """Return ((idx_a, idx_b), min_distance) for closest distinct login events, or (None, inf) if n < 2."""
    n = len(events)
    if n < 2:
        return None, math.inf
    min_dist = math.inf
    best_pair = None
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            d = math.hypot(events[i][0] - events[j][0], events[i][1] - events[j][1])
            if d < min_dist:
                min_dist = d
                best_pair = (i, j)
    return best_pair, min_dist
