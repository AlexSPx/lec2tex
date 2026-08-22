# Remediation performance audit

## Executive result

The final source freeze is `f952a54`, and the fresh independent resolution audit
certified it (`84/84` resolved; no unresolved or uncertain verdicts). The
process history still contains an important escape: an independent resolution
audit against the earlier freeze `b73e168` caught three residual source defects
after workers and the coordinator had declared source editing frozen. The
coordinator fixed all three in one additional source commit and rebuilt
successfully; the fresh audit verified all three repairs and found no new defect.

The earlier process weaknesses remain: inconsistent event schemas, nine
completion claims without a validation event, run-level rather than worker-level
model attribution, and coordinator edits that are not separately attributable
from initial worker output.

This audit is read-only. No book source, PDF, or existing review artifact was
edited.

## Fixed metrics

| Measure | Result |
|---|---:|
| Final source freeze | f952a54 |
| Final independent audit | certified pass; 84/84 resolved |
| Worker packages | 16 (15 lectures + cross-book) |
| Assignment rows / resolution rows | 119 / 119 |
| Certified master IDs / represented | 84 / 84 |
| Resolution rows | 90 resolved; 29 partially resolved; 0 deferred |
| Parsed event records | 141 across 16 JSONL streams |
| Required worker files | 80 / 80 present |
| JSON/JSONL parse failures | 0 |
| Repeated master IDs | 22 IDs across 57 rows (shared scope) |
| Packages with machine validation event | 7 / 16 |
| Event records missing `event` key | 7 (all Lecture 10) |
| Explicit status corrections | 1 (Lecture 12 ADJ-083) |
| Residual defects caught after initial freeze | 3 (audit at b73e168) |
| Coordinator recovery commit / source delta | f952a54; 3 files, +11/-5 |
| Invalidated fidelity attempts / accepted retries | 2 / 2 |
| L12 collision records | 3 |
| Build targets / failures | 16 / 0 |
| Pages (combined + standalone) | 189 + 158 = 347 |
| Labels static / AUX | 173 / 173 |
| References / dangling | 61 / 0 |

## What Luna did well

The worker output covers every certified ID and reconciles every assignment to
a resolution row. Partial statuses are used for shared findings rather than
silently claiming that a lecture-only edit completed a formula/frontmatter
side; the cross-book package then supplies 21 resolved shared records. All
worker source ownership checks pass, and the committed diff contains only the
expected 17 TeX source files plus audit metadata.

The L06 and L12 remediation packages explicitly select accepted retry
provenance and exclude invalidated fidelity artifacts. The certified review
run retains invalidation markers, Stage-A-before-Stage-B evidence for both
retries, and a three-record L12 collision registry. There is no observed leak
of invalidated L06/L12 content into remediation evidence.

The final centralized build is strong: every target compiled, the combined
and standalone page counts are present, the existing 347-page raster audit is
clean, and the reference audit is clean with 173/173 labels and no dangling
targets. After recovery, the run log records 17 combined-build warnings and
clean inspection of the affected Bayes, hypergeometric, and formula pages, but
the final independent audit now certifies the corrected freeze.

## Independent-audit escape and recovery

The first independent resolution audit inspected freeze `b73e168` and correctly
withheld certification despite complete 84/84 resolution-matrix coverage. It
found exactly three residual defects:

- Bayes' formula in Lecture 03 used conditional probabilities for zero-mass
  partition members;
- the shared order-statistic entry called the k-th-smallest density the
  k-th-largest statistic;
- Lecture 07 used Boolean `OR`/`AND` rather than numeric `max`/`min` support
  bounds for the hypergeometric law.

The coordinator repaired these three defects in `f952a54` across three source
files (`lecture_03.tex`, `lecture_07.tex`, and `formulas.tex`), adding 11 and
removing 5 source lines, then rebuilt all 16 PDF targets and reran reference
checks. This is strong recovery and demonstrates that the independent audit was
valuable; it also means the earlier “source frozen” claim was premature as a
mathematical certification claim. The fresh `f952a54` audit then verified the
three repairs, found no new defect, and certified the final source.

## What Luna did poorly / process risk

The package contract was not enforced consistently. All streams parse, but
Lecture 10's seven event records have no `event` field, event names vary
(`start`, `started`, `validate`, `validated`, and others), and only 7 packages
emit a machine-readable validation event. Nine packages claim complete or
completed without that event. This is a provenance/measurement defect, not a
claim that those source edits failed.

The remediation manifest declares `gpt-5.6-luna/high`; the certified review
manifest separately declares `gpt-5.6-terra/high`, which is consistent with
separate phases but is not linked to worker-level attempt records. The
remediation manifest also reports all source work complete while
`resolution_audit` remains `running` even though the final audit now certifies
`f952a54`; this is a stale state-model field. Worker prompts and states do not
record a model or attempt ID, so `gpt-5.6-luna/high` is only run-level attribution.
Finally, the run log records substantial coordinator recovery: one explicit
status correction, four named lecture-side corrections, 14 cross-book repair
classes, and final layout/reference corrections. The package does not preserve
a clean initial-worker-versus-coordinator diff, so autonomous worker accuracy
cannot be estimated from the final source alone.

## Scope, collisions, and generated outputs

The baseline-to-final-freeze diff changes 17 expected TeX sources with 974
insertions and 423 deletions; no unexpected source file is present. There are
19 commits after the baseline, one after the initial freeze. Resolution
records have zero source-ownership violations. After the freeze, the worktree
contains 16 modified PDFs and an untracked `tmp/` directory, consistent with
generated build/raster artifacts; no source edit after `f952a54` was observed.

The 22 repeated master IDs are expected shared-scope collisions, not duplicate
resolution rows for the same source. The separate certified L12 fidelity
collision registry is the relevant provenance collision: three IDs occur in an
invalidated package and accepted retry, and the final adjudication binds them
to the retry records.

## Recommendations for the next large-book run

1. Context sizing: assign one source file or bounded section window per worker,
   require a section checkpoint before moving on, and reserve context for the
   evidence ledger and schema-valid handoff. Keep cross-book consumers in a
   separate wave after lecture-side work.
2. Retry policy: preserve the failed attempt, invalidate it explicitly, then
   allow one fresh-context retry with a new attempt ID and reason code. Do not
   merge outputs from attempts; escalate after the retry if the contract still
   fails.
3. Blindness/provenance: pre-create canonical absolute paths; capability-gate
   Stage B finding access on a nonempty, schema-validated Stage-A map; record
   accepted source refs and collision selectors in a registry.
4. Contract validation: use one JSON Schema for state, events, assignments,
   and resolutions. Require `event`, timestamp, attempt/model IDs, source
   scope, master ID, status, and validation result. Refuse `complete` until
   required files, IDs, parse, scope, and validation checks pass.
5. Independent checking: have a coordinator or second agent independently
   check each scoped diff, shared finding, source provenance, TeX structure,
   references, build, and raster output. Persist separate worker and
   coordinator commits or correction events so recovery cost is measurable.

## Evidence index

- `manifest.json`, `RUN_LOG.md`, and `agents/*` under this remediation run.
- `git log`/`git diff` from `f22e205` through `f952a54`.
- `peer_review/remediation/2026-08-22-f22e205/audit/FINAL_AUDIT.md` and its
  matrix/events, which record the three pre-freeze residuals.
- Certified review `FINAL_REPORT.md`, `SOURCE_COLLISION_REGISTRY.jsonl`, and
  the invalidated/accepted L06/L12 fidelity packages.
- `lectures/lectures_full.aux` and current generated PDF page counts.
