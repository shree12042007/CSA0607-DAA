"""Q2: Sequential Search across list sizes and hit/miss positions."""
import pandas as pd

def sequential_search(records, target_id):
    comps = 0
    for idx, rec in enumerate(records):
        comps += 1
        if rec["tool_id"] == target_id:
            return idx, rec, comps
    return -1, None, comps

def main():
    rows = []
    for sz in (20, 100, 500):
        recs = [{"tool_id": f"T-{100+i}", "tech_id": f"TECH-{(i%12)+1:02d}", "issue_time": f"08:{i%60:02d}", "bay": f"B-{(i%6)+1}"} for i in range(sz)]
        for label, tid in [
            ("Success_First", recs[0]["tool_id"]),
            ("Success_Middle", recs[sz // 2]["tool_id"]),
            ("Success_Last", recs[-1]["tool_id"]),
            ("Unsuccessful_Miss", "T-9999"),
        ]:
            pos, _, comps = sequential_search(recs, tid)
            rows.append({"list_size": sz, "scenario": label, "position": pos, "comparisons": comps})
    print(pd.DataFrame(rows).to_string(index=False))

if __name__ == "__main__":
    main()
