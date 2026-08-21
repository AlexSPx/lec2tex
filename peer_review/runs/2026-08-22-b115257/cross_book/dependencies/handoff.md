# Cross-book dependency audit handoff

Completed audit package: 10 findings (P0: 1, P1: 5, P2: 4). No book source was changed.

The generated driver orders all 15 lectures correctly, followed by the formula and table appendices. Static label validation found 171 unique labels, 90 ref-like commands, no duplicates, and no unresolved target. A full LaTeX build could not be run because no TeX engine is installed; this is the sole validation failure.

Highest-priority remediation chains:

- `CBD-010`: Lecture 11 states the full finite-variance CLT but its proof silently requires an MGF; Lecture 13 and the appendix re-use the broader claim.
- `CBD-002`: the formula appendix removes iid and nonzero-variance requirements from LLN/CLT.
- `CBD-006`: the appendix conflates one-sample `t(n-1)` conditions with Lecture 14 regression `t(n-2)` conditions.
- `CBD-003`, `CBD-004`, `CBD-008`: formula appendices are not safe standalone references without their correlation, transformation, and distribution-boundary hypotheses.

`CBD-001` is a label/order issue rather than a mathematical falsehood: the Lecture 7 thinning proof references a criterion introduced later in that same lecture, though an earlier equivalent Lecture-4 definition exists.
