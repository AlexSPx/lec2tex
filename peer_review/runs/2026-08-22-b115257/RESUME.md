# Resume instructions

1. Read `manifest.json` and continue the first non-complete phase.
2. Inspect each running agent directory's `state.json` and `handoff.md`.
3. A missing agent with incomplete state is resumed by a fresh Terra agent using
   only its prompt, state, handoff, rubric, and unfinished source sections.
4. Do not expose blind reviewers to `docs/REMEDIATION.md`, transcripts, OCR,
   previous findings, or other reviews.
5. Never edit `lectures/bodies/*.tex` during this run.
6. Checkpoint and commit after each completed batch of three agents.

