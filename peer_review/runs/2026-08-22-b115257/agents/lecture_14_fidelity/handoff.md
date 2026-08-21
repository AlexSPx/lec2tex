# Lecture 14 fidelity handoff

Stage A is complete before the blind findings were opened. `fidelity_inventory.jsonl`
covers all 2,053 transcript segments from 00:00 through 96:45 in seven
timestamped checkpoints. The interval 45:00--60:00 has severe unrelated ASR
corruption; its intelligible portions are documented and it contains no body
material that cannot be corroborated at the clear resumption.

All four blind findings were independently verified:

- F14-001, F14-002, F14-003: mathematically valid missing conditions but
  faithful to the source's unqualified presentation.
- F14-004: the numerical concern is valid and the body mildly strengthens the
  source heuristic by saying normal quantiles are "safe" at n >= 32.

For the F14-004 check, direct numerical integration of the t(30) density gave
`P(|T| >= 1.95996398) = 0.05934672`.

No additional material fidelity defect was found. No book source was edited.
See `verdicts.jsonl` for exact body lines, timestamps, analysis, confidence,
and dispositions; `new_findings.jsonl` records the completed independent
search.
