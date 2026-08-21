# Cross-book formulas audit

Audit all fifteen lecture bodies, `lectures/bodies/formulas.tex`, and generated
`lectures/bodies/tables.tex` as read-only. Check formula-sheet parameterizations
and hypotheses against lecture bodies, recompute worked numerical examples and
exercise claims where applicable, and check statistical-table applicability and
numerics. Report only evidence-backed findings with exact source lines; do not
read remediation material or git history and do not alter teaching sources.

Severity convention: P1 = produces an undefined/invalid method in ordinary
allowed inputs; P2 = incorrect statement or materially missing hypothesis;
P3 = clarification/coverage gap likely to cause misuse. Confidence is a
reviewer estimate in [0,1].
