# Remediation run log

## 2026-08-22 — initialization

- Created branch `codex/math-peer-remediation` from certified review commit
  `f22e205`.
- Selected `gpt-5.6-luna` with high reasoning for file-scoped fixes.
- Book sources were partitioned by lecture; generated outputs remain
  coordinator-owned.
- Started wave 1: Lectures 01, 07, and 11.

## 2026-08-22 — Lecture 11 checkpoint

- Luna/high completed all 10 assigned records: ADJ-046, ADJ-056--063,
  and ADJ-084.
- Coordinator validation passed: 10/10 unique resolution records, valid
  JSON/JSONL, balanced TeX environments, targeted anchor checks, and
  `git diff --check`.
- The P0 CLT proof-scope defect is resolved without weakening the stated
  finite-variance theorem.
- Reused the freed worker slot for Lecture 02.

## 2026-08-22 — Lecture 01 checkpoint

- Luna/high completed ADJ-001--008 with 8/8 unique resolved records.
- Coordinator checks confirmed accepted historical data (6/42, 18 winners),
  a stated i.i.d.-uniform model, the exact adjacent-repeat probability,
  almost-sure and measurability qualifications, valid JSON/JSONL, balanced
  TeX environments, and a clean scoped diff.
- Reused the freed worker slot for Lecture 08.

## 2026-08-22 — Lecture 02 checkpoint

- Luna/high completed ADJ-009 and ADJ-010 with 2/2 unique resolved records.
- Coordinator validation confirmed the probability construction on
  `2^Omega`, its countable-additivity argument, and the measurable finite
  positive-volume domain for geometric probability.
- JSON/JSONL and scoped diff checks passed; the slot moved to Lecture 12.

## 2026-08-22 — Lecture 07 checkpoint

- Luna/high completed all 10 assigned Lecture 07 body remediations.
- Six records are fully resolved and four are correctly marked partial only
  because their cross-book formulas/frontmatter sides remain coordinator-owned.
- Coordinator checks confirmed valid parameter boundaries, the Le Cam error
  qualification, regular-conditional/a.e. wording, positive-variance and
  almost-sure correlation statements, notation separation, valid audit data,
  balanced environments, and a clean scoped diff.
- Reused the worker slot for Lecture 03.

## 2026-08-22 — Lecture 08 checkpoint

- Luna/high completed all eight assigned body-side records; four remain
  partial solely for their shared `formulas.tex` side.
- Coordinator validation confirmed positive-atom and a.e./version semantics,
  integrability/L2 scope, the pushforward law, a.e. CDF differentiation,
  a valid one-to-one C1 change-of-variables theorem with zero density off the
  image, exponential support, supplement labels, and clean structural/data
  checks.
- Reused the worker slot for Lecture 04.

## 2026-08-22 — Lecture 03 checkpoint

- Luna/high completed all three Lecture 03 body assignments; ADJ-011 and
  ADJ-013 remain partial only for their other lecture/formula consumers.
- Coordinator review tightened the total-probability display to sum conditional
  terms only over positive-mass hypotheses, eliminating even conventional use
  of an undefined zero-mass conditional probability.
- Partition, regular-conditional/a.e., integrability, JSON/JSONL, TeX structure,
  and scoped diff checks passed; the slot moved to Lecture 09.

## 2026-08-22 — Lecture 12 checkpoint

- Luna/high completed nine body assignments using only the accepted retry
  provenance; the invalidated colliding fidelity package was explicitly ignored.
- Coordinator review confirmed likelihood, MLE boundary, moment-method,
  Cramer--Rao, Uniform consistency, sample-variance, and supplemental-label fixes.
- ADJ-083 was corrected from resolved to partial because its shared notation
  consumers remain for the central pass. Audit parsing and scoped checks passed.
- Reused the worker slot for Lecture 05.

## 2026-08-22 — Lecture 04 checkpoint

- Luna/high completed all five assigned records.
- Coordinator validation confirmed a total measurable null-set modification
  for the quotient, the correct countable-preimage measurability proof,
  nonnegative support masses, all-real equality-in-law quantification, and an
  in-order discrete independence criterion.
- Audit data, environment, and scoped diff checks passed; the slot moved to
  Lecture 10.

## 2026-08-22 — Lecture 09 checkpoint

- Luna/high completed 11 body-side assignments; shared formulas/table consumers
  remain explicitly partial.
- Coordinator review removed a false equivalence between Borel and
  Lebesgue-measurable sets and narrowed the zero-boundary CDF statement to the
  listed continuous nonnegative laws.
- Support, a.e. density, transformation, Jacobian, moment, Gamma, supplement,
  parameter-domain, JSON/JSONL, TeX structure, and scoped diff checks passed.
- Reused the worker slot for Lecture 13.

## 2026-08-22 — Lecture 10 checkpoint

- Luna/high completed all seven Lecture 10 body assignments; ADJ-056 remains
  partial only for its shared consumers.
- Coordinator validation confirmed a disjoint half-open typewriter partition
  with infinitely many zeros, higher-moment finiteness, a separate zero-variance
  Chebyshev branch, general and iid LLN scope, iid application assumptions,
  supplement labels, and clean audit/structure checks.
- Reused the worker slot for Lecture 14.

## 2026-08-22 — Lecture 05 checkpoint

- Luna/high completed four findings and the Lecture 05 side of shared ADJ-033.
- Coordinator validation confirmed the finite-second-moment squared-loss
  decomposition, finite/extended tail-sum conventions, mutually independent
  random-walk signs with parity-exact zero probability, covariance-scoped
  variance additivity, and clean audit/structure checks.
- Reused the worker slot for Lecture 06 with accepted-retry-only provenance.

## 2026-08-22 — Lecture 13 checkpoint

- Luna/high completed all seven body-side assignments; shared consumers remain
  explicitly partial.
- Coordinator checks confirmed uniform-in-parameter coverage, invertible pivot
  requirements, generalized quantiles, separate known/unknown-mean chi-square
  intervals, exact normal-model t scope, distribution-sensitive asymptotics,
  and an explicit warning that Lecture 11's MGF sketch is not the general CLT
  proof.
- Audit and scoped structural checks passed; the slot moved to Lecture 15.

## 2026-08-22 — Lecture 14 checkpoint

- Luna/high completed all four body-side assignments; shared findings remain
  partial until the cross-book pass.
- Coordinator validation confirmed full-rank and degrees-of-freedom gates,
  positive-variance iid Normal errors, separate Z/t pivots and endpoints, and
  regression notation scope. A nearby universal `n>=32` safety claim was also
  narrowed to an accuracy-dependent heuristic.
- Started the disjoint formulas/frontmatter remediation pass.

## 2026-08-22 — Lecture 06 checkpoint

- Luna/high completed two local findings and the Lecture 06 sides of three
  shared findings, using only the accepted fidelity retry.
- Coordinator validation confirmed nonnegative-integer PGF scope, left-limit
  derivatives and moment hypotheses, random-sum moment gates, Binomial/Poisson
  tie and endpoint modes, Geo/NegBin endpoint conventions, and valid audit data.
- The shared formula-sheet sides remain assigned to the active cross-book pass.

## 2026-08-22 — Lecture 15 checkpoint

- Luna/high completed three findings and the lecture side of shared ADJ-079.
- Coordinator review caught and fixed the residual Pascal-domain boundary:
  the recurrence now requires `n>=1`, so no negative upper binomial index is
  invoked under the declared convention.
- Counting domains, Catalan `n=0`, positive stars-and-bars, source context,
  supplement/task provenance, audit data, and scoped checks passed.
- All 15 lecture-body edit packages are now complete.

## 2026-08-22 — cross-book checkpoint

- Luna/high completed all 21 assigned formulas/frontmatter records.
- Coordinator review additionally repaired repeated-choice and empty-codomain
  combinatorics domains, chain-rule positivity, regular-conditional a.e. scope,
  explicit endpoint modes, random-sum moment gates, a variance asymptotic,
  extended tail sums, a.e. CDF/density and independence statements, 2-D
  diffeomorphism conditions, PGF left derivatives, MLE scope, and uniform
  confidence coverage.
- The 21/21 shared resolution records, JSON/JSONL, TeX balance, labels, and
  scoped diff checks passed. All source editing phases are complete; central
  build and verification started.

## 2026-08-22 — final build and render checkpoint

- Rebuilt the combined 189-page book and all 15 standalone lecture PDFs with
  `scripts/build_lectures.py --all`; every target compiled successfully.
- `scripts/check_refs.py` passed with 173 registered labels, 61 references,
  and no dangling references; `git diff --check` also passed.
- Rasterized and visually inspected 347 pages in total: all 189 combined-book
  pages and all 158 standalone-lecture pages. A clipped notation-table cell on
  combined page 8 was shortened without dropping its explanatory condition,
  then rebuilt and re-inspected at 150 dpi; the corrected page is clean.
- Moved two theorem-style labels into their rendered bodies so they register in
  the AUX output. The mathematical content is unchanged; both targets now pass
  the reference audit.
- Source remediation is frozen for independent resolution and agent-performance
  audits. Generated PDFs remain build artifacts outside the source commits.

## 2026-08-22 — independent-audit correction checkpoint

- The first independent resolution audit correctly withheld certification at
  source freeze `b73e168` despite complete 84/84 ledger coverage. It identified
  three residual defects: Bayes conditioning on zero-mass partition members, a
  largest/smallest order-statistic wording mismatch, and Boolean operators in a
  numerical hypergeometric support bound.
- Corrected the Bayes statement by requiring a positive-mass selected
  hypothesis and summing only over positive-mass partition members; relabeled
  the displayed order-statistic density as the k-th smallest; and replaced the
  support notation by explicit `max`/`min` bounds.
- Rebuilt the combined book and all 15 standalones. All 16 PDF targets compile,
  the combined warning count remains 17, and reference validation again passes
  with 173 labels, 61 references, and zero dangling targets.
- Re-rendered and inspected the affected Bayes, hypergeometric, and formula
  pages; all three corrections are legible and remain inside the page bounds.
  A fresh independent audit is required against the new source freeze.

## 2026-08-22 — final certification checkpoint

- Froze corrected source at `f952a54` and reran the same independent resolution
  auditor without allowing source or PDF edits.
- Final audit certified all 84 master findings resolved (`P0=1`, `P1=25`,
  `P2=58`), with zero unresolved or uncertain verdicts. Its 84-row matrix and
  119-row package join validate; all 29 package-level partial records are
  closed by shared-scope corrections.
- The performance audit validated 16/16 worker packages, 80/80 required worker
  artifacts, 119/119 assignment-resolution rows, and zero JSON/JSONL parse
  failures. It preserves the first failed audit and all three recovery fixes.
- Final status: certified pass for source commit `f952a54`; no deferred
  mathematical findings and no book-source changes after the freeze.
