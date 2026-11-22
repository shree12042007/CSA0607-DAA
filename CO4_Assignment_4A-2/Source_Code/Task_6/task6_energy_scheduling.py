"""
Task 6: Day-4 Design Challenge - Energy-Aware Job Scheduling (Weighted Interval Scheduling)
Course: CSA06 Design and Analysis of Algorithms (CO4 - Assignment 4A)
Strategy: Dynamic Programming with Binary Search for Predecessor Compatibility
"""

import bisect

def schedule_energy_jobs(jobs):
    if not jobs:
        return 0, [], [], []

    sorted_jobs = sorted(jobs, key=lambda j: j["finish"])
    n = len(sorted_jobs)
    finish_times = [j["finish"] for j in sorted_jobs]

    p = [0] * (n + 1)
    for i in range(1, n + 1):
        start_i = sorted_jobs[i - 1]["start"]
        idx = bisect.bisect_right(finish_times, start_i, 0, i - 1)
        p[i] = idx

    dp = [0] * (n + 1)
    decision = [False] * (n + 1)

    for i in range(1, n + 1):
        val_i = sorted_jobs[i - 1]["value"]
        include_val = val_i + dp[p[i]]
        exclude_val = dp[i - 1]
        if include_val > exclude_val:
            dp[i] = include_val
            decision[i] = True
        else:
            dp[i] = exclude_val
            decision[i] = False

    selected = []
    curr = n
    while curr > 0:
        if decision[curr]:
            selected.append(sorted_jobs[curr - 1]["id"])
            curr = p[curr]
        else:
            curr -= 1

    selected.reverse()
    return dp[n], selected, dp, p

if __name__ == "__main__":
    print("=== TASK 6: ENERGY-AWARE JOB SCHEDULING (WEIGHTED INTERVAL SCHEDULING) ===")
    jobs_stage5 = [
        {"id": "J1", "start": 1, "finish": 3, "value": 20},
        {"id": "J2", "start": 2, "finish": 5, "value": 50},
        {"id": "J3", "start": 4, "finish": 6, "value": 30},
        {"id": "J4", "start": 6, "finish": 8, "value": 40},
        {"id": "J5", "start": 5, "finish": 9, "value": 60},
        {"id": "J6", "start": 8, "finish": 10, "value": 30},
        {"id": "J7", "start": 9, "finish": 11, "value": 50},
        {"id": "J8", "start": 11, "finish": 13, "value": 40},
    ]
    max_energy, sel_jobs, dp_arr, p_arr = schedule_energy_jobs(jobs_stage5)
    print("\n[Stage 5: Assignment 8-Job Dataset]")
    print(f"  Predecessor Array p[1..8]: {p_arr[1:]}")
    print(f"  DP Array DP[0..8]        : {dp_arr}")
    print(f"  Optimal Selected Jobs    : {sel_jobs}")
    print(f"  Maximum Energy-Saving    : {max_energy}")

    jobs_adversarial = [
        {"id": "A1", "start": 1, "finish": 3, "value": 10},
        {"id": "A2", "start": 2, "finish": 10, "value": 100},
        {"id": "A3", "start": 3, "finish": 5, "value": 15},
        {"id": "A4", "start": 5, "finish": 7, "value": 15},
        {"id": "A5", "start": 7, "finish": 9, "value": 15},
    ]
    max_adv, sel_adv, dp_adv, p_adv = schedule_energy_jobs(jobs_adversarial)
    print("\n[Stage 6: Adversarial 5-Job Dataset]")
    print(f"  Predecessor Array p[1..5]: {p_adv[1:]}")
    print(f"  DP Array DP[0..5]        : {dp_adv}")
    print(f"  Optimal Selected Jobs    : {sel_adv}")
    print(f"  Maximum Energy-Saving    : {max_adv}")
