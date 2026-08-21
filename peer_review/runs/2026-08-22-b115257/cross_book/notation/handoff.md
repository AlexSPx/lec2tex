# Handoff — cross-book notation audit

Completed without modifying book sources. Coverage is complete: 15 lecture
bodies plus `formulas.tex`, `frontmatter.tex`, and `preamble.tex`.

Recorded 8 high-confidence findings: 2 P1 and 6 P2. The book is otherwise
consistent on its intentional strict-CDF convention, `\E`/`\Var`/`\ind`/`\given`
macros, Geo/NegBin failure-count support convention, and the Normal/
chi-square/Student parameter notation.

Priority repairs: `CBN-003` (invalid exponential CDF below zero) and `CBN-006`
(formula appendix permits a zero-variance CLT division and overstates MGF
conditions). `CBN-001` is the only direct rate-versus-scale terminology
contradiction.

Validation target: parse `state.json` and every nonblank line of the three
JSONL files. No validation failures were observed at completion.
