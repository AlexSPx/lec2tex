# Lecture 06 remediation handoff

Completed the assigned Lecture 06 fixes in
`lectures/bodies/lecture_06.tex`.

- ADJ-022: PGF mean is qualified as an extended left-derivative identity;
  the finite variance identity requires `E[X^2]<infinity`.
- ADJ-023: random-sum mean and variance formulas state separate finite-moment
  assumptions.
- ADJ-024: Binomial and Poisson mode ties are listed, along with Binomial
  endpoints and the optional Poisson `lambda=0` endpoint; the figure caption
  now says the rounded heights sum approximately to one.
- ADJ-025: geometric and negative-binomial sections use `0<p<1`, explain the
  `p=1` degenerate convention and `p=0` non-finite waiting case, and handle
  the coupon collector's deterministic first stage.
- ADJ-033: Lecture 06 moment statements carry finite-existence hypotheses.

ADJ-024, ADJ-025, and ADJ-033 are marked partially resolved because shared
formula-sheet/cross-book occurrences remain pending for their owning agents.
No global build was run. Validation passed with `git diff --check` and scoped
path/JSONL checks. Existing unrelated worktree changes were preserved.
