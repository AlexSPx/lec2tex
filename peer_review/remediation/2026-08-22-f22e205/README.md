# Mathematical remediation run

Baseline review commit: `f22e205`

Branch: `codex/math-peer-remediation`

This run implements the certified master ledger from
`peer_review/runs/2026-08-22-b115257/adjudication/MASTER_FINDINGS.jsonl`.
Lecture agents edit disjoint `lectures/bodies/lecture_NN.tex` files. A later
cross-book agent owns `formulas.tex`, `frontmatter.tex`, and shared notation.

Generated drivers and PDFs must never be edited directly. Builds and reference
checks are centralized in the coordinator after each wave.

