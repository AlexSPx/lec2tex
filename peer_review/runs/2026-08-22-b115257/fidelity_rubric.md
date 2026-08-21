# Fidelity verification rubric v1

Use a fresh context. Do not inspect `docs/REMEDIATION.md`, git history, other
lecture reports, or the README.

## Stage A: independent source map

Before opening the blind review's `findings.jsonl`, compare the lecture body to
its complete transcript. Record material claims, hedges, assumptions,
derivations, exercises, and caveats that are preserved, strengthened, weakened,
omitted, or added. Use timestamps. Consult board-state/OCR evidence on demand
for formula disputes rather than loading every OCR file. Relevant pages from
`refs/` may be used as secondary mathematical evidence.

Persist this independent map before beginning Stage B.

## Stage B: finding verification

Inspect every blind finding and classify it as one of:

- `confirmed_book_error`
- `faithful_nonstandard_presentation`
- `fidelity_omission_or_strengthening`
- `transcription_or_ocr_uncertainty`
- `primary_reviewer_error`
- `insufficient_evidence`

For each verdict, cite the blind finding ID, exact source lines, transcript
timestamps, relevant OCR/frame identifiers, reference evidence if used,
independent mathematical analysis, confidence, and recommended disposition.

Search for fidelity issues the blind mathematical reviewer could not see. Do
not edit the book. Checkpoint after each transcript/source section and save all
results before returning a final message.

