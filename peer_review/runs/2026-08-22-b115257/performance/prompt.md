# Agent-performance audit

Audit the observable behavior of the mathematical-review and fidelity-review
agents in run `2026-08-22-b115257`, plus the coordinator interventions recorded
in `RUN_LOG.md`. Do not infer or inspect private reasoning. Use only durable
prompts, states, events, ledgers, handoffs, invalidation markers, the manifest,
and misplaced artifacts. Do not edit lecture materials. Do not read
`docs/REMEDIATION.md` until the primary filesystem-derived metrics are fixed.

Required outputs are `state.json`, `events.jsonl`, `metrics.json`,
`findings.jsonl`, and `PERFORMANCE_REPORT.md`. Counts must be derived from
parsed JSONL records rather than newline counts where those differ.
