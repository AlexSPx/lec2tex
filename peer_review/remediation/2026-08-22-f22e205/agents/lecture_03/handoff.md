# Lecture 03 handoff

Patched only `lectures/bodies/lecture_03.tex`.

- ADJ-011: local Lecture 03 conditioning ratios, null partition terms, and
  conditional-independence domain are qualified; lecture 08/formulas work is
  pending.
- ADJ-012: hospital diagnoses are explicitly a mutually exclusive exhaustive
  partition, with `H_other` when necessary.
- ADJ-013: continuous point conditioning now uses a specified regular
  conditional version almost everywhere; the iid identity
  `E[X_1|S_n]=S_n/n` is stated a.s. under integrability; lecture 07/formulas
  work is pending.

Validation passed: `git diff --check` and targeted path/line inspection. No
global build was run.
