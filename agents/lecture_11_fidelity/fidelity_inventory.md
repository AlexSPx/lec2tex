# Stage A — independent source map (persisted before blind findings)

Audit timestamp: 2026-08-21T22:15:00Z. Primary transcript: `run/lecture_11/audio/transcript.json` (complete, 0.00–6438.00). Body: `lectures/bodies/lecture_11.tex`. “Added” means unsupported by the spoken transcript, not necessarily mathematically false.

| Transcript span | Source claim / action | Body location | Map / initial fidelity assessment |
|---|---|---|---|
| 101.70–258.50 | IID sequence, common cdf, `S_n`, SLLN and error `E_n=S_n/n-μ→0` a.s. | 3–13 | Preserved, including the reason partial sums are neither IID nor independent. |
| 262.14–316.36 | New question: rate of convergence; CLT announced. | 13–17 | Preserved. |
| 323.78–485.92 | IID finite-variance CLT; `Z_n=(S_n-nμ)/(σ√n)⇒N(0,1)`. | 19–25 | Preserved formula and hypotheses. Transcript treats `σ` as positive, while body only writes `σ²<∞`; this is an implicit nondegeneracy issue for later review. |
| 509.80–698.00 | Heuristic error scale `σZ/√n`, its random (not deterministic) nature, and universality. | 56–60 | Preserved and polished. “Entirely predetermined” at body 58 is stronger wording than source’s heuristic qualification. |
| 700.00–1190.00 | Distributional convergence means cdf convergence; interval probabilities and algebraic unstandardizing. | 62–70 | Preserved. |
| 1200.00–1550.00 | Tug-of-war `±1` example, win probability tends to `1/2`, tie probability tends to zero. | 74–85 | Preserved. |
| 1550.00–1650.00 | Continuous asymmetric density: `½e^{-y}` for positive values and `¼` on `(-2,0)`; lecturer says mean is 0 and *thinks* variance is 1. | 87–100 | Preserved density and CLT purpose; body replaces the tentative variance with the correct `5/3` (explicitly flags the source’s tentative “1”). This is a corrective strengthening, not a silent transcription. |
| — | Three-panel simulated/histogram CLT figure. | 27–50 | Added instructional visual; no spoken source analogue. |
| — | Lindeberg–Feller supplement. | 102–119 | Added advanced extension; absent from transcript. Its last sentence (“IID case … automatically”) requires qualifications and is a prospective mathematical/fidelity check. |
| 1680.00–2200.00 | Definition of MGF, finite domain near zero, discrete sum and continuous integral; uniform and exponential examples. | 121–148 | Preserved. Exact source examples are present; body has clearer domain language. |
| 2251.46–2348.46 | Ordinary/absolute/central/absolute-central moments and practical use through fourth order. | 150–158 | Preserved. |
| 2392.46–2690.46 | MGF at zero; moments via derivatives; independence product; convergence theorem; uniqueness; affine transformation. | 160–175 | Preserved, re-ordered (affine before uniqueness/convergence) and made more formal. Interchange of expectation and infinite Taylor sum is presented with less spoken caution. |
| 4018.66–4046.54 | Finite mean/variance need not imply MGF; characteristic functions handle the general CLT. | 177–183 | Preserved. |
| 3575.36–3868.16 | Derivation `M_Z(s)=e^{s²/2}` by completing the square, then `M_{N(μ,σ²)}(t)=e^{μt+σ²t²/2}`. | 185–197 | Preserved. |
| 3874.10–4500.00 | CLT proof *idea*: standardize `Y_j`; impose global MGF existence for simplicity; product MGF and Taylor expansion; lecturer repeatedly calls remaining details non-rigorous/technical. | 199–227 | Core derivation preserved, but body labels it a completed “proof” and ends “proof completed.” The source expressly hedges “idea” and “not quite rigorous”; this is a material strengthening to verify in Stage B. |
| 4510.00–5020.00 | Molecule/tug threshold application, e.g. `n=10^6`, threshold 1000 or 5000 and normal-tail approximation. | — (aside from exercise 312) | Omitted as worked application; body retains only a related exercise with threshold 100. |
| 5020.00–5778.80 | Bernoulli polling/Monte Carlo setup, worst-case `p(1-p)≤1/4`, normal-tail heuristic, error/sample-size discussion, and caveat that samples/responses need not be ideal. | 255–270 | Main derivation preserved. Body omits source’s extended real-world sampling caveat and explicitly turns a heuristic CLT approximation into a chain containing `≤`; needs Stage B mathematical scrutiny. |
| 5790.92–5908.34 | Berry–Esseen announced: cdf error uniformly bounded at order `1/√n`, involving third central/absolute moment and constant near 0.47. | 272–277 | Preserved in a cleaner formal theorem, but source OCR does not distinguish the absolute third moment reliably; body uses `E|X_1-μ|^3`, the standard form. |
| 5917.02–6094.82 | Binomial as sum of IID Bernoulli variables; standardized CLT and thresholds depending on `n`. | 231–240 | Preserved. Body adds the “fixed deviation → 1/2” explanation. |
| — | Local de Moivre–Laplace supplement. | 242–253 | Added; no spoken counterpart. |
| 6100.66–6378.44 | Gamma density/MGF computation with `t<β`, then first and second moments by differentiation. | 279–302 | Preserved. |
| — | Three exercises, including normal MGF, threshold 100, and Gamma moments. | 304–319 | Added instructional material; source only gestures toward examples/thresholds, not assigned exercises. |

## Stage-A inventory of potential fidelity deltas

1. **Proof-status strengthening:** transcript 3874.10–4500.00 describes an informal/non-rigorous proof idea; body 201–227 makes it an official completed proof.
2. **Omitted source application:** transcript 4510.00–5020.00’s molecule example and numerical thresholds are not retained as a worked example.
3. **Omitted source caveat:** transcript 5714.84–5757.82 emphasizes that real polling error includes nonrandom sampling/nonresponse; body’s polling paragraph does not retain this caveat.
4. **Added advanced content:** figure, Lindeberg–Feller, local de Moivre–Laplace, and exercises have no spoken equivalent. Their fidelity classification depends on whether the project permits explicit enrichment; mathematical accuracy will be checked.
5. **Potential formula/hypothesis risks requiring mathematical review:** CLT statement’s `σ=0` case; global-MGF assumption versus needed local behavior; MGF Taylor/interchange and remainder; the inference chain in body 258–266; Lindeberg–Feller’s IID assertion; and Berry–Esseen hypotheses.
