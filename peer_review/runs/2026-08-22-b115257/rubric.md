# Review rubric v1

## Blind mathematical pass

Review every section and account for every numbered statement, proof, displayed
derivation, example, and exercise. Check definitions, hypotheses, quantifiers,
domains, edge cases, proof steps, constants, indices, distribution
parameterizations, independence and measurability assumptions, convergence
modes, computations, and dependencies.

Do not inspect `docs/REMEDIATION.md`, git history, other agent reports, raw
transcripts, board OCR, or the README during this pass. Do not edit the book.

## Severity

- P0: false central result or invalid proof with downstream consequences.
- P1: substantive mathematical error, wrong result, or missing essential hypothesis.
- P2: genuine gap, ambiguity, inconsistent convention, or unjustified step.
- P3: pedagogical or presentation defect without mathematical invalidity.

## Evidence standard

Each finding must identify exact source lines, reproduce the disputed claim,
give an independent derivation or counterexample, list dependencies, state
confidence, and distinguish mathematical correctness from source fidelity.

An agent may not report completion until its coverage ledger accounts for every
in-scope object and `state.json` records no unfinished sections.

## Observable-behavior logging

Log files inspected, checks performed, tool failures, retries, changes of
confidence, rejected hypotheses, blockers, and scope deviations. Do not attempt
to record private chain-of-thought. Record concise, auditable reasons and
evidence instead.

