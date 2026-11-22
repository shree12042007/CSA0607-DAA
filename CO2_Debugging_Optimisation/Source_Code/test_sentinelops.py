"""Comprehensive test harness for SentinelOps SOC Alert-Triage Module (standard + boundary tests)."""
import math
from sentinelops_optimised import (
    sort_alerts,
    build_blocklist_index,
    is_blocked,
    find_signature,
    closest_logins,
)


def run_tests():
    # Standard prompt test data
    alerts = [("A1", 3), ("A2", 9), ("A3", 5), ("A4", 9), ("A5", 1)]
    sorted_a, _ = sort_alerts(alerts)
    assert sorted_a == [("A2", 9), ("A4", 9), ("A3", 5), ("A1", 3), ("A5", 1)]

    blocklist = ["10.0.0.5", "10.0.0.9", "172.16.4.2"]
    b_set = build_blocklist_index(blocklist)
    assert is_blocked(b_set, "10.0.0.9")[0] is True
    assert is_blocked(b_set, "10.0.0.5")[0] is True
    assert is_blocked(b_set, "8.8.8.8")[0] is False

    hits, _ = find_signature("FAILFAIXFAIL", "FAIL")
    assert hits == [0, 8]

    events = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
    pair, dist, _ = closest_logins(events)
    assert set(pair) == {0, 5}
    assert abs(dist - math.sqrt(2.0)) < 1e-9

    # Boundary tests required in Part (b) and Part (e)
    # 1. Empty blocklist
    assert is_blocked(build_blocklist_index([]), "10.0.0.1")[0] is False
    # 2. Equal severities (arrival order preserved)
    eq_alerts = [("X1", 7), ("X2", 7), ("X3", 7)]
    assert [x[0] for x in sort_alerts(eq_alerts)[0]] == ["X1", "X2", "X3"]
    # 3. Signature at the very end of the log
    assert find_signature("ALERT_01_SQLI", "SQLI")[0] == [9]
    # 4. Pattern longer than the log
    assert find_signature("OK", "TIMEOUT_ERR")[0] == []
    # 5. Fewer than two login events (0 and 1 events)
    assert closest_logins([]) == (None, math.inf, 0)
    assert closest_logins([(10.0, 20.0)]) == (None, math.inf, 0)

    print("ALL STANDARD AND BOUNDARY TEST CASES PASSED.")


if __name__ == "__main__":
    run_tests()
