# CSA06 – Design and Analysis of Algorithms
## CO1 – Assessment Tool 1: Scalability Audit of "ShopSphere"

**Student Name:** ____________  **Reg. No.:** ____________

### Repository layout
```
CO1_AT1/
├── Question_1/
│   ├── Source_Code/   (Python 3 – no external libraries)
│   └── Report/        (report + captured program output)
└── README.md
```

### How to run
```
cd Question_1/Source_Code
python3 m1_m2_iterative.py          # (b) M1 and M2 : counters vs closed forms
python3 m3_search.py                # (c),(e) S1/S2  : recurrence, best/avg/worst
python3 m4_m5_recurrences.py        # (d) M4/M5      : recurrences vs closed forms
python3 bounds_and_scalability.py   # (f),(g)        : Theta(n^2) proof check, scalability table
```

### Summary of results
| Module | Exact count | Complexity | n = 1,000,000 @ 10^8 ops/s |
|---|---|---|---|
| M1 | n(n−1)/2 | Θ(n²), space Θ(1) | 83.3 min – **FAIL** |
| M2 | 2^⌈log₂n⌉ − 1 | Θ(n) (claim Θ(n log n) is wrong) | 10.5 ms |
| S2 | ⌊log₂n⌋ + 1 | Θ(log n); space Θ(1) iter / Θ(log n) rec | 20 comparisons |
| M4 current | 2n² − n | Θ(n²) | 5.56 h – **FAIL** |
| M4 redesign | n log₂n + n | Θ(n log n) | 0.21 s |
| M5 | n + n·L(L+1)/2 | Θ(n log² n) | 2.10 s |

Report: `Question_1/Report/CSA06_CO1_AT1_Report.docx`
