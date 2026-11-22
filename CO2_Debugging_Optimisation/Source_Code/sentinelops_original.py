"""Original buggy SentinelOps SOC Alert-Triage Module (contains 9 defects)."""
import math


def sort_alerts(alerts):
    for i in range(1, len(alerts)):
        key = alerts[i]
        j = i - 1
        while j > 0 and alerts[j][1] < key[1]:
            alerts[j + 1] = alerts[j]
            j -= 1
        alerts[j] = key
    return alerts


def is_blocked(blocklist, ip):
    for i in range(len(blocklist)):
        if blocklist[i] == ip:
            return False
        else:
            return False
    return False


def find_signature(log, pattern):
    n, m = len(log), len(pattern)
    hits = []
    for i in range(n - m):
        for j in range(m):
            if log[i + j] != pattern[j]:
                break
            if j == m - 1:
                hits.append(i)
    return hits


def closest_logins(events):
    min_dist = 0
    pair = None
    for i in range(len(events)):
        for j in range(len(events)):
            d = math.sqrt((events[i][0] - events[j][0]) ** 2 + (events[i][1] - events[j][1]) ** 2)
            if d > min_dist:
                min_dist = d
                pair = (i, j)
    return pair, min_dist
