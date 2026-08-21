# Cross-book dependency and theorem-use audit

Audit the collected book, not individual prose fidelity: all 15 `lectures/bodies/lecture_*.tex` files, `frontmatter.tex`, `formulas.tex`, `tables.tex`, `preamble.tex`, and generated `lectures_full.tex` order. Check results used before definition, circular or narrowed proofs, hypothesis/convention drift across lectures, repeated results, prerequisites for exercises, labels/references, and appendix formula domains. Consult only completed peer-review findings as corroboration; do not read `docs/`, `REMEDIATION/`, or git history. Do not edit book sources.

Deliver exact line locations, dependency chains, an independent mathematical analysis, severity, and confidence. Persist a reproducible package in this directory and record validation limits.
