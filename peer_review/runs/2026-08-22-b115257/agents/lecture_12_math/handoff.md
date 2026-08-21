# Lecture 12 blind mathematical review — complete

The audit covers all source lines 1--406 through 29 ledger objects: each
section, numbered definition/proposition/supplement/remark, proof, displayed
derivation, example, figure-caption mathematical claim, and exercise.

Totals: 10 findings — P0: 0, P1: 1, P2: 9, P3: 0.

The central defect is `L12-M-005`: the unknown-variance normal MLE claimed in
Example 12-2 does not exist for n=1 (nor for an all-equal data set) because the
likelihood is unbounded as sigma^2 approaches zero. The other findings concern
the CDF convention, unjustified i.i.d. inference, formal likelihood conditions,
the omitted lower-support indicator in the uniform likelihood, MoM/SLLN
hypotheses, Cramer--Rao regularity, the epsilon domain in the uniform
consistency proof/exercise, and n=1 for corrected sample variance.

Artifacts:

- `findings.jsonl` has complete evidence, dependencies, confidence, and
  suggested disposition for every finding.
- `coverage.jsonl` contains 29 complete review entries.
- `events.jsonl` records observable inspections, independent checks, rejected
  counter-hypotheses, scope compliance, and JSON validation.

Residual uncertainty is limited to two convention/completeness findings: the
author may intentionally use P(X<x) as a left-continuous convention, and the
sample-moment proposition may be meant to inherit i.i.d./integer assumptions.
Both are recorded as P2 because the lecture also includes discrete laws and the
numbered statement is otherwise incomplete. No tool failures occurred. The
lecture source was not modified; the PDF was not needed for mathematical
verification.
