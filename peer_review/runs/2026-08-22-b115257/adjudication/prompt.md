# Provisional adjudication mandate

Run: `2026-08-22-b115257`

Construct a provisional, evidence-led master ledger from the valid blind
mathematical reviews, valid fidelity reviews, and the cross-book notation,
dependency, and formula audits.  Reconcile every blind mathematical finding
against its corresponding fidelity verdict.  A final P0/P1 needs two
independent supports or a reproducible proof/counterexample.  Distinguish a
mathematical error from a source-faithful lecturer presentation and from a
book/source fidelity strengthening or omission.

Do not edit book sources.  Do not read `docs/REMEDIATION.md` or
`cross_book/render` during this provisional stage.  Exclude every directory
containing `INVALIDATED.md`; use `lecture_06_fidelity_retry` and
`lecture_12_fidelity_retry` as their valid replacements.

Required final package: `state.json`, `events.jsonl`, `MASTER_FINDINGS.jsonl`,
`REJECTED_OR_DOWNGRADED.jsonl`, `PROVISIONAL_REPORT.md`, and `handoff.md`.
Set the final state to `waiting_for_render_and_remediation`, never `complete`.
