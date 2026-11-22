# CO4_Assignment_4A — Design and Analysis of Algorithms (CSA06)

**Institution:** Saveetha Institute of Medical And Technical Sciences (SIMATS Engineering)  
**Department:** Computer Science and Engineering  
**Course:** CSA06 — Design and Analysis of Algorithms  
**Course Outcome:** CO4 (Solve optimization problems using Dynamic Programming and Greedy strategies)  

---

## Repository Structure

```text
CO4_Assignment_4A/
│
├── Source_Code/
│   ├── Task_1/
│   │   └── task1_fractional_knapsack.py
│   ├── Task_2/
│   │   └── task2_job_sequencing.py
│   ├── Task_3/
│   │   └── task3_knapsack_01.py
│   ├── Task_4/
│   │   └── task4_word_break.py
│   ├── Task_5/
│   │   └── task5_shortest_paths.py
│   └── Task_6/
│       └── task6_energy_scheduling.py
│
├── Report/
│   └── CO4_Assignment_4A_Report.pdf
│
└── README.md
```

---

## Summary of Tasks & Algorithmic Strategies

| Task | Problem Title | Strategy | Time Complexity | Space Complexity |
| :--- | :--- | :--- | :--- | :--- |
| **Task 1** | Logistics Vehicle Loading (Fractional Knapsack) | Greedy (Value-to-Weight Ratio) | $O(n \log n)$ | $O(n)$ |
| **Task 2** | Job Sequencing with Deadlines | Greedy (Descending Profit + Latest Slot) | $O(n^2)$ | $O(d_{\max})$ |
| **Task 3** | Cargo Planning System (0/1 Knapsack) | Dynamic Programming + Backtracking | $O(nW)$ | $O(nW)$ |
| **Task 4** | Word Break Forensics & Repair | Dynamic Programming (Prefix Reachability) | $O(n^2 \cdot L)$ | $O(n)$ |
| **Task 5** | Graph Shortest Paths (Dijkstra, Bellman-Ford, Floyd) | Greedy & Dynamic Programming | $O(V^2)$ / $O(VE)$ / $O(V^3)$ | $O(V)$ / $O(V^2)$ |
| **Task 6** | **Day-4 Design Challenge:** Energy-Aware Job Scheduling | Weighted Interval Scheduling (DP + Binary Search) | $O(n \log n)$ | $O(n)$ |

---

## How to Run the Programs

Ensure Python 3.8+ is installed on your machine. Execute any task script from the repository root:

```bash
python3 Source_Code/Task_1/task1_fractional_knapsack.py
python3 Source_Code/Task_2/task2_job_sequencing.py
python3 Source_Code/Task_3/task3_knapsack_01.py
python3 Source_Code/Task_4/task4_word_break.py
python3 Source_Code/Task_5/task5_shortest_paths.py
python3 Source_Code/Task_6/task6_energy_scheduling.py
```
