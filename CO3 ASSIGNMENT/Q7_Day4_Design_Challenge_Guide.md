# Q7 – Design Divide and Conquer from First Principles (10 Marks)

> **Important note before anything else:** I don't see the actual Day-4 problem statement in the materials you uploaded — only this question's *process* (Stages 1–6) is described. The assignment references "the Day-4 problem" as something given separately (likely a handout from your Day-4 session). You'll need that problem statement to actually do this question — if you have it, share it and I can explain the *kind* of thinking it calls for.
>
> **Also important:** this question is structurally different from Q1–Q6. It explicitly requires **two independent, unaided proposals** before you're even allowed to discuss the problem with each other ("Neither student may work on this question independently and simply combine the answers later" / "No marks are deducted merely because an initial design is incorrect — the purpose is to provide evidence of independent algorithmic thinking"). That means Stage 1 is specifically testing *your own, unaided* first instinct on the problem. If I generate "Student A's proposal" and "Student B's proposal" for you, that defeats the entire point of the stage and the evidence you submit would be fabricated, not real evidence of independent thinking. I won't do that part regardless of the problem.

What I *can* do is walk you through what each stage is actually asking for, so you both approach it correctly.

---

## Stage 1 – Independent Design Proposal (must be done separately, without talking to each other)

Before you discuss anything with your partner, each of you — alone — should sketch:
- A possible decomposition: how would *you* split this problem into smaller versions of itself?
- A base case: what's the smallest/simplest version you'd stop recursing at?
- What information does each subproblem need to return for the combine step to work?
- A possible combine strategy: how do partial answers get merged into the final answer?

Write this down in your own words, even if you're not confident it's right. Keep both independent write-ups — you submit them as-is, mistakes and all.

## Stage 2 – Compare the Two Designs

Once you've both written your independent proposals, sit down together and compare:
- Where do your two designs agree?
- Where do they differ?
- What's a strength of each proposal? A weakness?
- Did either of you miss an edge case or piece of information the other considered?
- Which ideas from each proposal are worth keeping?

Write a short "design-comparison record" — this is evidence, so it should actually reflect your real discussion, not be reconstructed afterward to look tidy.

## Stage 3 – Joint Final Design

Now, together, build the actual final solution using the best ideas from both initial attempts. This final design must explicitly state:
- Decomposition
- Subproblems
- Base case
- Information returned by each subproblem
- Combine operation
- Full algorithm / pseudocode

## Stage 4 – Divide the Validation Responsibilities

- **Student A:** formulate the recurrence from your joint design, explain each term in it, solve it, and state the resulting asymptotic complexity.
- **Student B:** design correctness test cases, implement/instrument the final solution, compare it against a brute-force/straightforward baseline if feasible, and present the experimental evidence.

(This is the same kind of math-derivation / experimental-validation split you've already practiced in Q1–Q6 — once you have the actual joint design from Stage 3, I'm happy to help you work through the recurrence or the test-case design the same way I did for the earlier questions.)

## Stage 5 – Cross-Defence
- Student A must be able to explain what experimental evidence (from Student B's work) supports the design.
- Student B must be able to explain how the recurrence (from Student A's work) arises from the decomposition.

This is the same cross-understanding requirement as Q5 — don't just know your own half.

## Stage 6 – Joint Evaluation

Together, discuss and conclude:
- Why is this problem suitable for Divide and Conquer?
- What computational work does the decomposition actually reduce?
- What additional costs does recursion introduce (call overhead, combine-step cost, possible extra memory)?
- Under what conditions might D&C *not* be the right choice for this problem?

Final question to answer together: **what characteristics should an algorithm designer look for before choosing Divide and Conquer for a new problem?** General things to think about across all of Q1–Q6: does the problem break into independent, same-shaped subproblems; is the combine step cheap relative to the subproblem work; does the recursion actually reduce total work compared to brute force, etc. — ground your answer in what you observed across the earlier questions.

---

## What to do next
Send me the actual Day-4 problem statement (likely a separate handout) once you have it, and — **after you and your partner have each independently written your own Stage 1 proposal** — share those with me. I can then help you with Stage 2 onward: comparing the two designs, building the final pseudocode together, checking your recurrence, and helping design test cases, the same way I helped with Q1–Q6.
