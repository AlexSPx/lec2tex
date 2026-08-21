# Performance audit — 2026-08-22-b115257

## Outcome

The run completed all 15 planned blind mathematical reviews and all 15 accepted
fidelity reviews. The analysis evidence is strong; artifact/process discipline
is materially weaker and required repeated coordinator recovery. This audit
uses only observable run artifacts. It neither inspected nor infers private
reasoning, and no book files were edited.

## Fixed filesystem metrics

| Measure | Result |
|---|---:|
| Math attempts / completed manifest units | 15 / 15 |
| Fidelity attempts / accepted packages | 17 / 15 |
| Invalidated attempts / successful fresh replacements | 2 / 2 |
| Parsed math coverage records | 291 |
| Parsed math candidate findings | 100 |
| Candidate severity | P0 1, P1 25, P2 66, P3 8 |
| Accepted Stage-A source-map records | 207 |
| Accepted ID-linked fidelity verdicts | 100 / 100 math IDs |
| Accepted raw verdict records | 101 (one L05 completion summary is not a verdict) |
| Material independent fidelity findings | 37 |
| Existing agent JSONL streams parsed | 118 / 118 |

The accepted verdict outcomes are 71 `confirmed_book_error`/`confirmed`, 12
`fidelity_omission_or_strengthening`, 15
`faithful_nonstandard_presentation`, and 2 `primary_reviewer_error`. Those are
different outcomes, not a single confirmation rate: a source-faithful
nonstandard presentation may still identify a legitimate mathematical concern,
while a fidelity omission identifies a book/source difference.

## Phase assessment

| Phase | Analysis quality | Artifact discipline |
|---|---|---|
| Blind math | 15/15 complete, 291 coverage records, 100 candidates, and 224 observable events. The model used exact calculations, proof checks, fallback numerical methods, and rendered checks where appropriate. | All 15 have the expected core package. Transient read/tool/validation incidents were recoverable, though logging terminology is not consistent. No explicit blind-scope violation marker was found. |
| Fidelity, accepted | All 15 packages show a persisted independent Stage A before blind finding access and reconcile every math ID exactly once. The 207 map records and 37 independent findings add meaningful source-fidelity coverage. | 7 accepted attempts required schema/path/name correction; 14/15 now contain all seven contract files. `lecture_12_fidelity_retry/handoff.md` remains absent. |
| Fidelity, invalidated | The original Lecture 06 and 12 attempts cannot count as independent analysis: both opened the blind finding set before persisting Stage A. | This is a real protocol failure, but it was visibly documented, invalidated, and retained rather than hidden. |
| Orchestration | The coordinator detected both blindness failures, forced fresh contexts, corrected canonicalization, and maintained a recoverable audit trail. | Intervention was effective but too frequent: natural-language constraints alone did not reliably produce contract-compliant artifacts. |

## Blindness, checkpoints, and recovery

The critical independence gate passed for all 15 accepted fidelity packages.
For Lectures 06 and 12, the original attempts are explicitly marked
`INVALIDATED`; their replacements are accepted only because their event trails
show Stage-A map persistence and validation before the first blind-file read.
Lecture 06 is especially auditable: retry event sequence 2 records a validated
22-record map and sequence 5 records the first successful finding-file open.

The rubric also asks for checkpoints after each transcript/source section. The
maps support broad coverage, but per-section checkpoint compliance cannot be
given one precise run-wide rate: event schemas differ from detailed section
events to aggregate checkpoints. The right conclusion is therefore **15/15
gate-compliant accepted packages**, not an unsupported claim of uniform
per-section event compliance.

## Failures and retries

There are 17 explicitly logged, recoverable tool/command/read/path incidents:
10 in math and 7 in fidelity. Examples include unavailable SymPy, SciPy, and
`pdftotext`; truncated reads; a patch-context mismatch; malformed jq filters;
and blind-artifact path probes. All recovered without an observed final
coverage blocker. This is a lower-bound count from events/states/handoffs and
`RUN_LOG.md`; passive transcript/OCR corruption is not counted as an agent tool
failure.

The important weakness is reporting consistency. For example, a final handoff
may say “no failures” while an event records a successfully repaired validation
failure. That is not a content failure, but it weakens automatic process
measurement.

## Schema and path discipline

Seven accepted fidelity attempts required correction: Lecture 01 (Markdown-only
initial persistence), 04 (ad hoc names), 06 retry (repository-level write), 08
(ad hoc new-findings name), 11 (repository-level Markdown package), 13 (ad hoc
Stage-A names), and 15 (ad hoc originals). All preserve the originals as
behavior evidence and have usable canonical data afterwards.

Two misplaced directories remain outside the run root, with 14 files total:

- `/Users/g8row/Documents/lec2tex/agents/lecture_06_fidelity_retry` — 7
  contract artifacts.
- `/Users/g8row/Documents/lec2tex/agents/lecture_11_fidelity` — 7 Markdown
  artifacts.

The accepted-package contract is otherwise close to complete: 104 of 105
expected files exist. The remaining exception is
`agents/lecture_12_fidelity_retry/handoff.md`. The invalidated Lecture 06
attempt lacks Stage-B artifacts as expected after interruption; that absence is
not charged against the accepted-package rate.

## Model and harness assessment

The manifest's `gpt-5.6-terra` with high reasoning is suitable for the
substantive task based on the available evidence: complete math coverage,
precise evidence ledgers, 100 independently reconciled candidates, and useful
fallback methods. Individual agent artifacts do not state a model, so this is
an assessment of the manifest-selected policy and output, not per-agent model
attribution.

The same evidence says prompts alone are insufficient for mechanical protocol
requirements. The model/harness division should be:

1. Keep the high-reasoning reviewer for math and source comparison.
2. Pre-create and absolute-path the artifact directory; prohibit success if an
   output resolves outside it.
3. Make Stage-B finding access capability-gated on a nonempty, schema-validated
   Stage-A map, rather than asking the agent to self-police blindness.
4. Provide one generated JSON schema for state/events/coverage/verdicts and a
   completion command that checks fields, IDs, counts, and required files.
5. Require structured incident fields (`kind`, `transient`, `recovered`,
   `blocker`) so successful retries are not later described as “no failures.”
6. Generate the handoff from validated state/ledger data, eliminating the one
   remaining missing handoff and reducing duplicated prose drift.

## Validation and uncertainties

All 118 existing agent JSONL streams parse as JSONL when loaded as streams.
Counts in this report use parsed records rather than `wc -l`; this matters for
blank valid streams and the L05 status-summary record. `manifest.json` still
lists cross-book as running, but that does not alter the completed math/fidelity
population audited here.

Observable logs are self-reported artifacts, not a complete execution trace.
Accordingly, “no math blindness violation observed” means no explicit marker
was found; it is not proof about unlogged activity. The performance audit did
not read `docs/REMEDIATION.md` before fixing the metrics above.
