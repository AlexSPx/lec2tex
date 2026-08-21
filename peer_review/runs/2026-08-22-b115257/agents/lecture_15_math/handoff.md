# Lecture 15 blind mathematical review

Status: complete. The book was not edited.

Coverage: 27 ledger objects account for all source sections, numbered
statements, proofs, displays, example, and exercises (including every stated
subpart). Preamble semantics relevant to environments and math macros were
checked. The PDF was not needed for mathematical disambiguation.

Findings: 4 total, all P2.

- F015-001: elementary-counting formulas omit natural domains.
- F015-002: binomial-identity proposition omits index conditions or a
  zero-extension convention.
- F015-003: Catalan and strict-excursion derivation fails to delimit n>=1 and
  mishandles n=0 at the displayed-factorial level.
- F015-004: the random-walk definition does not state iid symmetric steps.

Independent finite checks passed for distinct tuple/subset counts, surjection
inclusion-exclusion, Catalan bridges, and strict excursions. No tool failures
or retries occurred. The only recorded uncertainty is whether F015-004 is a
substantive missing hypothesis or terminology that the intended audience is
expected to supply; no later probability calculation depends on it.
