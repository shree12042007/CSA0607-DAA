"""
Task 2: Job Sequencing with Deadlines
Course: CSA06 Design and Analysis of Algorithms (CO4 - Assignment 4A)
Strategy: Greedy Algorithm (Sort by Profit Descending, Schedule in Latest Free Slot <= Deadline)
"""

def job_sequencing(jobs):
    if not jobs:
        return [], 0

    sorted_jobs = sorted(jobs, key=lambda j: j["profit"], reverse=True)
    max_deadline = max(j["deadline"] for j in sorted_jobs)
    slots = [None] * (max_deadline + 1)

    total_profit = 0
    trace_log = []

    for job in sorted_jobs:
        jid = job["id"]
        d = job["deadline"]
        p = job["profit"]
        placed = False

        for t in range(min(d, max_deadline), 0, -1):
            if slots[t] is None:
                slots[t] = jid
                total_profit += p
                placed = True
                trace_log.append(f"Job {jid} (d={d}, p={p}) -> Assigned to Slot {t} | Cumulative Profit = {total_profit}")
                break

        if not placed:
            trace_log.append(f"Job {jid} (d={d}, p={p}) -> REJECTED (No free slot <= {d})")

    schedule = [(t, slots[t]) for t in range(1, max_deadline + 1) if slots[t] is not None]
    return schedule, total_profit, trace_log

if __name__ == "__main__":
    print("=== TASK 2: JOB SEQUENCING WITH DEADLINES ===")
    jobs_original = [
        {"id": "A", "deadline": 2, "profit": 80},
        {"id": "B", "deadline": 1, "profit": 35},
        {"id": "C", "deadline": 2, "profit": 60},
        {"id": "D", "deadline": 3, "profit": 40},
        {"id": "E", "deadline": 1, "profit": 25},
    ]
    sched1, prof1, logs1 = job_sequencing(jobs_original)
    print("\n[Test Case 1: Original Dataset]")
    for log in logs1:
        print(" ", log)
    print(f"Final Schedule (Slot, Job): {sched1} | Total Profit: {prof1}")

    jobs_modified = [
        {"id": "A", "deadline": 2, "profit": 80},
        {"id": "B", "deadline": 1, "profit": 70},
        {"id": "C", "deadline": 2, "profit": 60},
        {"id": "D", "deadline": 3, "profit": 40},
        {"id": "E", "deadline": 1, "profit": 25},
    ]
    sched2, prof2, logs2 = job_sequencing(jobs_modified)
    print("\n[Test Case 2: Modified Dataset (Job B Profit = 70)]")
    for log in logs2:
        print(" ", log)
    print(f"Final Schedule (Slot, Job): {sched2} | Total Profit: {prof2}")
