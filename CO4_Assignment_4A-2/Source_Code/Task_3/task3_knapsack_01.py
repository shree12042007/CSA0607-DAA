"""
Task 3: 0/1 Knapsack Problem (Cargo Planning System)
Course: CSA06 Design and Analysis of Algorithms (CO4 - Assignment 4A)
Strategy: Dynamic Programming with Optimal Item Reconstruction
"""

def knapsack_01(items, capacity):
    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w_i = items[i - 1]["weight"]
        v_i = items[i - 1]["value"]
        for w in range(1, capacity + 1):
            if w_i <= w:
                include_val = v_i + dp[i - 1][w - w_i]
                exclude_val = dp[i - 1][w]
                dp[i][w] = max(include_val, exclude_val)
            else:
                dp[i][w] = dp[i - 1][w]

    selected_items = []
    curr_w = capacity
    for i in range(n, 0, -1):
        if dp[i][curr_w] != dp[i - 1][curr_w]:
            item = items[i - 1]
            selected_items.append(item["id"])
            curr_w -= item["weight"]

    selected_items.reverse()
    return dp[n][capacity], selected_items, dp

if __name__ == "__main__":
    print("=== TASK 3: 0/1 KNAPSACK CARGO PLANNING ===")
    cargo_items = [
        {"id": "P", "weight": 2, "value": 12},
        {"id": "Q", "weight": 3, "value": 20},
        {"id": "R", "weight": 4, "value": 25},
        {"id": "S", "weight": 5, "value": 30},
    ]
    cap = 7
    max_val, selected, dp_table = knapsack_01(cargo_items, cap)

    print(f"\n[Test Case 1] Vehicle Capacity = {cap}")
    print("DP Table:")
    header = "Item\Cap | " + " ".join(f"{w:3d}" for w in range(cap + 1))
    print(header)
    print("-" * len(header))
    row_names = ["0 (None)"] + [f"{it['id']} (w={it['weight']},v={it['value']})" for it in cargo_items]
    for r_idx, row in enumerate(dp_table):
        print(f"{row_names[r_idx]:12s} | " + " ".join(f"{val:3d}" for val in row))

    print(f"\nMaximum Optimal Value: {max_val}")
    print(f"Selected Items: {selected}")

    val_small, sel_small, _ = knapsack_01(cargo_items, 1)
    print(f"\n[Test Case 2] Capacity = 1 -> Max Value: {val_small}, Selected: {sel_small}")
