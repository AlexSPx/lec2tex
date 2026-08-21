# Final adjudication report

## Outcome

The final ledger remains **84 deduplicated remediable findings**: **P0=1,
P1=25, P2=58**. The rejected/downgraded ledger has **28 decisions covering 31
source IDs**. All 162 substantive source IDs are mapped, and all 100 blind
findings have a one-to-one valid fidelity verdict.

No book source was edited.

## Final-check traceability corrections

- **FC-I-002:** Q0 now contains only the sole P0, ADJ-058. Q1 contains all
  25 P1 items, including ADJ-014 with its quotient-domain/null-set
  disposition, and expressly excludes ADJ-058. Q2 contains all 58 P2 items.
  Thus the three queue bands are an exact severity partition of the master
  ledger.
- **FC-I-003:** L12-F-001 through L12-F-003 occur in both an invalidated
  fidelity package and its accepted retry. `SOURCE_COLLISION_REGISTRY.jsonl`
  records both canonical paths and the exclusion rule. The `source_refs` on
  ADJ-065, ADJ-066, and ADJ-071 bind their evidence specifically to
  `agents/lecture_12_fidelity_retry/new_findings.jsonl`. This provenance repair
  changes no master severity, disposition, or count.

## Render and reference result

The completed render audit is clean: 177/177 book pages and 149/149 standalone
pages were rasterized and inspected (326 pages total), with zero actionable
visual, reference-target, or PDF-readability defects. Static reference checks
also found 171 source labels, 171 AUX labels, and zero unresolved targets.
This adds no master finding and does not weaken the mathematical ledger.

## Remediation-document comparison

`docs/REMEDIATION.md` was treated as historical comparison evidence, not ground
truth. Its own implementation record describes an earlier accepted 172-page
artifact, whereas the audited current book has 177 pages, so historical claims
were not assumed to describe this baseline.

| Remediation source | Final adjudication result |
|---|---|
| B-02 (Toto framing, hedges, and numerical discussion) | Partial match with ADJ-005/006/008: the book needs an explicit model and must not strengthen the source. Disagreement: the document's proposed 6/49/≈1-in-1400 recovery conflicts with the fidelity evidence that the historical event was 6/42 with 18 winners. |
| B-03 (leave an omitted derivation as an exercise) | Consistent with ADJ-R-011: intentional deferred proofs should be labeled, not silently completed or escalated into an error. |
| B-05/B-06 (L15 revision framing and transcript-backed exercises) | Matches ADJ-081/082: preserve/recover source material and label it; do not relocate the lecture or invent missing tasks. |
| C-10 (CDF convention) | Resolved by the ADJ-R-021 tie-break. The current L05 source explicitly announces the strict/left convention; retain it with a prominent convention note rather than globally replacing it. The cited historical L09 location no longer contains the reported CDF statement. |
| D-10/D-11 (L06/L09 recovery) | Directionally matches ADJ-022--025 and ADJ-037/044, but recovery must not add unsupported mathematics. Correctness conditions and source scope must be explicit. |
| D-12 (no regression worked example) | Remains a P3 curriculum suggestion (ADJ-R-026), not a mathematical defect. |
| A/C formatting and build claims | No current action from this adjudication: the independent render/reference audit is clean. These historical implementation claims do not refute or resolve current mathematical findings. |

## Prior remediation rejections that remain rejected

- **D-01:** Do not replace Lecture 02's lecturer-specific axiom presentation
  with a different textbook formulation. This review reports only construction
  and measurability gaps (ADJ-009/010), not a demand to rewrite the axioms.
- **D-02:** Do not move Lecture 15 to a different chapter. ADJ-081/082 calls
  for accurate revision-session framing and source/provenance labels instead.
- **D-03/B-06:** Exercise restoration is appropriate only when transcript or
  board evidence supports it. Unmarked exercises remain provenance items, not
  license to invent content.

## New findings not supplied by the remediation document

- **ADJ-058 (P0):** the Lecture 11 finite-variance CLT proof is narrower than
  stated and is reused downstream.
- Cross-book formula-reference failures: omitted LLN/CLT, correlation,
  transformation, parameter-domain, and t-inference prerequisites
  (ADJ-028, ADJ-037, ADJ-056, ADJ-075, ADJ-084).
- Mathematical falsehoods and boundary defects across probability models,
  likelihoods, distributions, and regression (see the P1 queue below).

## Remaining adjudication disagreements / guardrails

1. Fidelity to a lecturer is not permission to state an undefined formula as a
   self-contained theorem. ADJ-077/078 remain accepted although the source made
   the same omissions; changes should make the qualification visible rather
   than erase the source's presentation.
2. The remediation document states that L15 tasks 6--9 and 11 were unavailable.
   The current fidelity evidence supports deferred/external tasks but not that
   exact enumeration from transcript alone; ADJ-R-028 remains rejected for
   insufficient evidence.
3. The strict-CDF convention is a resolved P3 convention issue, not a P2
   request to standardize all CDFs. Any future edit must preserve the stated
   course convention consistently.
