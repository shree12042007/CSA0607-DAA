# CSA06 – Design and Analysis of Algorithms · Assignment 1 (CO1)
**Design, Analyse and Validate an Efficient Search Strategy for a Large-Scale Student Record System**

**Student:** JAYASHREE S  **Course:** CSA06, Dept. of Computer Science and Engineering, SIMATS Engineering
**Repository:** https://github.com/shree12042007/CSA0607-DAA

## Project summary
A university must locate a student record by unique registration number in databases of 10³ → 10⁶+ records. Three *different* algorithmic strategies were designed, analysed mathematically, implemented, benchmarked and compared. The Day-4 challenge (50,000 searches/hour on 10⁶ records, updates once a day) was then used to re-evaluate the design.

| # | Algorithm | Strategy | Style | Preprocessing | Search (avg / worst) |
|---|-----------|----------|-------|---------------|----------------------|
| 1 | Linear search | Brute force | Iterative | none | Θ(n) / Θ(n) |
| 2 | Binary search | Decrease-and-conquer + presorting | **Recursive** | sort, Θ(n log n) | Θ(log n) / Θ(log n) |
| 3 | Hash table (chaining) | Space–time trade-off | Iterative | build, Θ(n) | Θ(1) / Θ(n) |

**Key results (n = 1,000,000):** average comparisons ≈ 480,745 (linear), 18.9 (binary), 1.3 (hash); average search time 39 ms / 10 µs / 1.9 µs; preprocessing 0 / 0.61 s / 3.6 s.
**Final recommendation:** original problem → sorted array + binary search (Task 11); Day-4 challenge → **modify** to a hash index rebuilt/updated daily (Task 12), keeping the sorted index only if range queries are needed.

## Repository structure
```
CO1_Assignment
├── Task_1_Algorithm_Design/            algorithms, pseudocode, preprocessing, justification
├── Task_2_Basic_Operation/             basic operation of every algorithm
├── Task_3_Mathematical_Complexity/     derivation of T(n) incl. preprocessing
├── Task_4_Case_Analysis/               best / average / worst case
├── Task_5_Asymptotic_Analysis/         O, Ω, Θ and interpretation
├── Task_6_Recurrence_Formulation/      T(n) = T(⌊n/2⌋) + 1
├── Task_7_Recurrence_Solution/         substitution, iteration, Master Theorem
├── Task_8_Implementation_Testing/
│   └── Source_Code/                    search_algorithms.py, test_algorithms.py, run_experiments.py, make_screenshots.py
├── Task_9_Experimental_Performance/    tables, graphs, results.csv / results.json
├── Task_10_Theory_vs_Experiment/       comparison and discussion
├── Task_11_Final_Recommendation/       recommended design and defence
├── Task_12_Design_Challenge/           Day-4 impact, evaluation, redesign, defence
├── Report/
│   ├── Source_Code_Screenshots/
│   ├── Output_Screenshots/
│   ├── Analysis/                       combined analysis (Tasks 2–7, 10)
│   ├── Tables_and_Graphs/              5 graphs + result tables
│   └── Documentation/                  Final_Report.md (complete report)
└── README.md
```

## How to run
Requirements: Python 3.9+, `pip install matplotlib pillow`.
```bash
cd Task_8_Implementation_Testing/Source_Code
python test_algorithms.py        # 15 tests – all should PASS
python run_experiments.py        # benchmark for n = 1k, 10k, 100k, 1M (≈ 1–2 min)
python make_screenshots.py       # optional: regenerate screenshots
```
`run_experiments.py` is seeded (`SEED = 2024`) so datasets and queries are identical on every run; timings vary slightly between machines.

## Notes on the experiments
* Each search returns `(index, comparisons)`, so the basic operation is counted exactly; timing includes this small counting overhead for all three algorithms equally.
* Preprocessing (sorting, hash-table build) is reported separately and included in total-cost analysis.
* Timings are from a single run in interpreted Python; see Task 10 for the discussion of where measurements deviate from theory.
