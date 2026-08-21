# Lecture 07 mathematical peer review

Status: complete. All objects in `lectures/bodies/lecture_07.tex` (lines 1--646), required preamble notation, every theorem/proof/display/example/figure numerical claim, and all six exercises are covered in `coverage.jsonl`.

Findings: 7 total — P0: 0, P1: 3, P2: 4, P3: 0.

- P1 `L07-M-001`: the claimed universal Poisson-approximation recipe fails inside its advertised region.
- P1 `L07-M-002`: hypergeometric variance formula is undefined at the admitted boundary `N=M=n=1`.
- P1 `L07-M-004`: both landmark correlation theorems omit the positive-variance domain required to define correlation.
- P2 `L07-M-003`: joint CDF is evaluated at infinity outside its declared domain.
- P2 `L07-M-005`: supplemental correlation and fixed-value conditioning claims omit nondegeneracy/integrability/a.s. qualifications.
- P2 `L07-M-006`: the Poisson proof's all-n special case can assign an invalid binomial probability.
- P2 `L07-M-007`: boundary cases contradict the `rho=-1` and finite-population-factor `<1` wording.

No unresolved mathematical uncertainty. One `apply_patch` context mismatch occurred while finalizing the ledger; it changed nothing and the retry succeeded. No prohibited sources were inspected and no book file was edited. `lectures/lecture_07.pdf` was not needed for the mathematical pass; source-level displays and visual numerical claims were checked.
