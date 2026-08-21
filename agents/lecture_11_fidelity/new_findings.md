# New fidelity findings not dependent on the blind mathematical review

Audit timestamp: 2026-08-21T22:24:00Z.

| ID | Priority | Type | Evidence | Finding / disposition |
|---|---:|---|---|---|
| L11-F-001 | P2 | fidelity omission | Transcript 4510.00–5020.00 develops a concrete molecule/force threshold application (`n=10^6`, threshold 1000, then 5000, and normal-tail estimates). The body has no corresponding worked example; body 312 retains only a loosely related threshold-100 exercise. | The book omits a source application that demonstrates nonzero CLT thresholds and tail scaling. Restore a concise worked version if completeness relative to the lecture is required. |
| L11-F-002 | P2 | fidelity omission | Transcript 5714.84–5757.82 explicitly warns that 1000–2000-person polling does not by itself solve nonrandom selection/nonresponse. Body 255–268 concludes with the sample-size rationale but not this caveat. | The book strengthens the real-world reading of the ideal IID Bernoulli model by omission. Add a one-sentence caveat that sampling design and response bias are outside this calculation. |
| L11-F-003 | P1 | fidelity strengthening (overlaps L11-M-005) | Transcript 4115.12–4500.00 frames the CLT derivation as a simplified, technically incomplete idea; body 201–227 calls it a proof and says it is completed. | This materially changes epistemic status. Resolve as prescribed for L11-M-005. |

No additional formula discrepancy was found in the targeted checks of the normal-MGF derivation (OCR `board_010`, 3750.0), binomial normalization (OCR `board_016`, 6072.0), or Gamma-MGF computation (OCR `board_017`, 6273.0), conditional on the standard nondegenerate/positive-parameter domains noted in the verdicts.
