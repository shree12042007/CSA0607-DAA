# Task 4 – Best, Average and Worst-Case Behaviour (4 Marks)

## 4.1 Linear search
| Case | Input condition | Operations | Why |
|------|-----------------|-----------|-----|
| **Best** | The requested registration number is the **first** record in the file | 1 comparison | The loop exits at the first iteration. |
| **Average** | Key present and equally likely at any position (or present with probability p) | (n+1)/2 for success; p(n+1)/2 + (1−p)n in general | On average half of the list is scanned before the key is hit. |
| **Worst** | Key is the **last** record, or **not in the database** | n comparisons | No early exit is possible; every record must be examined to prove absence. |

*Observation:* the worst case is not rare – every failed lookup (e.g. a typo in a registration number) is a worst case. Measured at n = 10⁶: successful ≈ 4.8×10⁵ comparisons, unsuccessful = 10⁶.

## 4.2 Binary search
| Case | Input condition | Operations | Why |
|------|-----------------|-----------|-----|
| **Best** | Key is exactly the **middle** element of the sorted array | 1 comparison | Found in the first call. |
| **Average** | Key present, each position equally likely | ≈ log₂(n+1) − 1 | About half of the keys lie in the bottom level of the decision tree, which has the largest depth, so the average is only ≈1 below the worst. |
| **Worst** | Key absent, or located at the deepest level of the decision tree | ⌊log₂ n⌋ + 1 | The range must be halved until it is empty/one element. |

*Observation:* binary search has little spread – best 1, average ≈ 19, worst 20 for n = 10⁶. Important precondition: the array must remain sorted; otherwise results are wrong.

## 4.3 Hash table (chaining)
| Case | Input condition | Operations | Why |
|------|-----------------|-----------|-----|
| **Best** | Bucket is empty (unsuccessful search, 0 comparisons) or the key is first in its chain (1 comparison) | 0–1 | The hash directly points to the answer. |
| **Average** | Keys spread uniformly, load factor α | successful 1 + α/2 ≈ 1.375; unsuccessful α = 0.75 | Chain length is Poisson-like with mean α; independent of n. |
| **Worst** | All keys collide into one bucket (poor hash function, e.g. m sharing factors with a pattern in the registration numbers, or an adversarial key set) | n comparisons | The table degenerates into a linked list = linear search. |

*Observation:* the largest chain observed in the experiments was 4, 6, 6 and 7 for n = 10³…10⁶ – the worst case is theoretical for a well-chosen prime modulus (and can be avoided with a universal hash function).
