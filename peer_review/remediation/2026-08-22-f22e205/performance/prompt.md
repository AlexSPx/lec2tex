# Remediation performance audit prompt

Audit the remediation run `2026-08-22-f22e205` read-only against baseline
`f22e205`, final source freeze `f952a54`, and certified review run
`2026-08-22-b115257`. Inspect all 16 remediation packages, their manifests,
logs, git history/diffs, build/reference results, and the certified invalidated
and accepted fidelity artifacts. Incorporate the independent resolution audit
at `b73e168`, which caught three residual defects after the run was declared
source-frozen, and the coordinator's corrective commit/rebuild at `f952a54`.
Quantify assignments, resolution statuses, event and artifact completeness,
scope isolation, model policy, builds, coordinator corrections, malformed
artifacts, collisions, completion claims, and invalidated L06/L12 provenance.
Persist only this audit package. Do not edit source files, generated PDFs, or
existing review/remediation artifacts.
