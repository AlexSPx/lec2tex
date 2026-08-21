# Provisional adjudication report

## Scope and validation

This provisional ledger used all 15 valid blind mathematical packages, their
15 valid fidelity packages, and all three completed cross-book audits. The
invalidated `lecture_06_fidelity` and `lecture_12_fidelity` directories were
excluded; their retry packages supplied the fidelity evidence. No book source
was changed, and `docs/REMEDIATION.md` and `cross_book/render` were not read
while this provisional decision set was built.

- Blind mathematical IDs: 100
- Valid fidelity verdict IDs: 100
- Missing/orphan fidelity verdict IDs: 0 / 0
- Additional substantive fidelity IDs: 36
- Cross-book source IDs: 26
- Source IDs reconciled into ledgers: 162 / 162

`MASTER_FINDINGS.jsonl` contains 84 deduplicated, remediable P0--P2 records:
P0=1, P1=25, P2=58. `REJECTED_OR_DOWNGRADED.jsonl` contains 28 decisions
covering 31 lower-priority, duplicate, insufficient-evidence, or rejected
source IDs. Every P0/P1 record has either two independent supports or a
reproducible proof/counterexample recorded in `evidence_gate`.

## Provisional priority findings

- **P0 — ADJ-058:** Lecture 11 states the finite-variance iid CLT as proved,
  but its proof adds an MGF assumption and is reused downstream. A rescaled
  Student-t(3) counterexample establishes the proof-scope failure; fidelity
  confirms the book strengthened the lecturer's explicitly simplified status.

- **P1 clusters:** unqualified measure/model constructions (ADJ-003,
  ADJ-006, ADJ-010); moment/parameter/boundary failures (ADJ-018, ADJ-020,
  ADJ-022--ADJ-028, ADJ-041, ADJ-043); unsafe conditional expectation and
  transformation claims (ADJ-034, ADJ-037); CLT/normal approximation and
  inference failures (ADJ-056--ADJ-061, ADJ-067, ADJ-076--ADJ-077); and the
  unmarked large Lecture 09 addition (ADJ-049).

## Correctness versus fidelity decisions

Source faithfulness does not erase a real mathematical defect. For example,
the Lecture 14 rank, residual-degrees-of-freedom, and positive-variance
conditions remain accepted (ADJ-077--ADJ-078) because direct counterexamples
make the printed formulas undefined, even though fidelity confirms the
lecturer omitted the same conditions.

Conversely, source-faithful informal teaching was not automatically elevated
to a book defect. The deferred general PGF proof, conventional CDF-at-infinity
shorthand, and routine differentiation-under-the-integral justification were
downgraded to optional P3 clarifications. The two fidelity-marked primary
reviewer errors, L06-M002 and L10-M004, remain rejected.

## Tie-breaks recorded

1. **Strict CDF convention (L12-M001):** fidelity treated `P(X<x)` as an
   error against the standard right-continuous CDF. The notation audit instead
   demonstrates an intentional, internally consistent book-wide strict/left
   convention. It is downgraded to P3; the recommended action is a prominent
   convention label, not a global rewrite.
2. **Lecture 14 prerequisites:** fidelity labels the missing conditions
   source-faithful. Reproducible constant-design and `n=2` examples, plus the
   formula/dependency audits, retain P1 severity.
3. **Faithful informal null-event formulas:** Bayes/odds and elementary CDF
   shorthand with conventional readings are P3 where the source supplies the
   intended restricted context; genuine zero-denominator formulas that remain
   unqualified are retained in ADJ-011/013/034.

## Pending final comparison

The provisional ledger is fixed. The next phase may incorporate the completed
render audit and compare this ledger to `docs/REMEDIATION.md` as regression
evidence only, recording matches, newly discovered issues, rejected issues
that stay rejected, and genuine disagreements.
