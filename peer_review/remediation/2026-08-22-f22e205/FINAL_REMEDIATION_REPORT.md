# Final mathematical remediation report

## Outcome

The book remediation is complete and independently certified at source commit
`f952a54` on branch `codex/math-peer-remediation`.

- Certified findings resolved: **84/84** (`P0=1`, `P1=25`, `P2=58`).
- Final audit verdicts: **84 resolved, 0 not resolved, 0 uncertain**.
- Deferred mathematical findings: **0**.
- Source scope: the expected 15 lecture bodies plus `formulas.tex` and
  `frontmatter.tex`; no unexpected book source was changed.

The first independent audit at `b73e168` withheld certification and found three
residual defects: a zero-prior Bayes term, a largest/smallest order-statistic
mismatch, and Boolean notation in a numerical hypergeometric support bound.
All three were fixed in `f952a54`, rebuilt, visually checked, and verified by a
fresh read-only audit. The failed checkpoint remains in the audit history.

## Build and artifact verification

- All 16 PDF targets compile: one combined book and 15 standalone lectures.
- Combined book: 189 A4 pages; standalones: 158 pages; total raster audit:
  **347 pages**.
- References: 173 registered labels, 61 references, zero dangling targets.
- `git diff --check` and all remediation JSON/JSONL parsing checks pass.
- A notation-table overflow found during rendering was corrected and its page
  re-inspected at 150 dpi. The three post-audit mathematical corrections were
  also rebuilt and inspected in their rendered locations.
- Remaining TeX messages are non-actionable over/underfull diagnostics; no
  visible clipping or mathematical rendering defect remains.

## Agent performance

The remediation used 16 Luna/high worker packages: one per lecture plus one
shared cross-book pass. The package set contains all 80 required worker files,
119 assignment-resolution rows, and all 84 certified IDs. Of the 119 package
rows, 90 are resolved and 29 are lecture-side partials; every partial is closed
by the shared pass. Invalidated Lecture 06 and Lecture 12 fidelity attempts did
not leak into the accepted remediation provenance.

The cheaper workers were effective for bounded, single-file correction work,
but the audit shows why coordination remained necessary. Only 7/16 packages
logged a machine-readable validation event; Lecture 10 has seven event rows
without the canonical `event` key; model identity is recorded at run level,
not per attempt; and the coordinator made material follow-up corrections. Most
importantly, the first independent audit caught three residual defects after
the initial source freeze. The final pass succeeded because completion was
gated on independent source inspection, rebuilds, references, and render QA
rather than worker status flags alone.

For a future large book, retain one file or bounded section per agent, keep the
shared-consumer pass separate, require schema-validated event/model/attempt
metadata, invalidate retries rather than merging them, and refuse completion
until a fresh independent auditor certifies the frozen source.

## Evidence

- Certified resolution audit: `audit/FINAL_AUDIT.md` and
  `audit/RESOLUTION_MATRIX.jsonl`.
- Agent/process audit: `performance/PERFORMANCE_REPORT.md` and
  `performance/metrics.json`.
- Worker checkpoints: `agents/lecture_01` through `agents/lecture_15` and
  `agents/cross_book`.
- Chronological recovery log: `RUN_LOG.md`.
