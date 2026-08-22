# Remediation rubric v1

## Source policy

- Implement only certified master findings assigned to the owned source file.
- Preserve lecture fidelity: qualify or annotate source-faithful nonstandard
  statements rather than silently replacing the lecturer's presentation.
- Do not remove content. Recover transcript-backed caveats or context concisely.
- Label editor-created material as supplemental; do not invent new mathematics.
- Never edit generated lecture drivers, generated tables, or PDFs.

## Resolution record

Create one JSONL record per assigned master ID with:

`master_id`, `status`, `source_file`, `new_lines`, `change_summary`,
`mathematical_check`, `fidelity_check`, `tests`, and `remaining_risk`.

Allowed statuses are `resolved`, `partially_resolved`, and `deferred`. A
deferred or partial item requires a precise blocker. Do not claim resolution
merely because wording changed.

## Agent package

Each agent owns a remediation subdirectory containing `prompt.md`, `state.json`,
`events.jsonl`, `resolution.jsonl`, and `handoff.md`. Checkpoint after every
master finding. The coordinator alone builds the book and updates the master
manifest.

