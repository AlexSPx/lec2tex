# Stage A — independent transcript/body fidelity inventory

Scope: all 3,237 transcript segments (`00:00–107:07`) compared with the complete
lecture body. `lecture_06_math/findings.jsonl` was not opened during this stage.
Line citations below refer to `lectures/bodies/lecture_06.tex`.

| Transcript coverage / timestamp | Source claim or activity | Body location | Stage-A disposition |
|---|---|---|---|
| `00:00–02:01` | Repeated “subscribe”/recording setup, then a late-start/apology. | — | Omitted appropriately; non-lecture administration. |
| `02:01–04:00` | Introduces PGFs; quotes Pólya’s *bag* analogy, then gives the lecturer’s architecture/sketch analogy. | 1–3 | Architecture analogy retained and expanded. Pólya/bag attribution and analogy omitted (minor narrative omission). |
| `04:00–06:02` | Defines nonnegative integer-valued `X`; `g_X(s)=E[s^X]=Σs^nP(X=n)`, `s∈[-1,1]`; finite support is covered by zero terms. | 5–12 | Faithfully retained, with the finite-support explanation expanded. |
| `06:02–08:57` | States PGF uses: expectation, variance, and recovery of `P(X=k)` by derivatives. | 14–21 | Faithful; exact three identities retained. |
| `08:57–10:00` | Termwise derivative and `g'_X(1)=EX` when finite; equivalence of finite derivative and existence of expectation. | 24–42 | Faithful and strengthened with an explicit nonnegative-series/existence explanation. |
| `10:01–13:00` | Informal interchange of derivative and expectation; derives factorial second moment and variance identity. | 44–63 | Faithful. The source explicitly says rigor for interchanging derivative/expectation is omitted; body preserves that caveat in a footnote and adds a rigorous series route. |
| `13:00–15:54` | Demonstrates only `k=1` coefficient recovery; asks students to generalize. | 65–85 | Strengthened: body proves the complete `k≥0` result and distinguishes terms killed by differentiation from those killed at `s=0`; it accurately labels the source’s `k=1` limitation. |
| `16:00–19:09` | `X≡_dY` iff PGFs agree; both directions via coefficients/derivatives; English name “probability generating function.” | 87–99 | Faithful proof, concise; the English-language aside omitted. |
| `19:09–24:59` | Reviews joint independence for finite/infinite sequences and defines identically distributed variables. | 102–105 | Core definition of equal distribution retained. Infinite-sequence definition/finite-subfamily explanation is compressed to the parenthetical `(X_j)_{j=1}^∞`, so a mild pedagogical omission. |
| `25:02–31:59` | For independent nonnegative integer-valued `X_j`, PGF of the sum is product; IID case is a power; proof only for two terms and why independence matters. | 107–120 | Faithful. Body gives the two-variable proof and retains the fixed-`n` claim; it makes the “fixed number” condition explicit. |
| `32:00–36:40` | Defines Bernoulli scheme: independent binary trials with constant success probability; distinguishes independence from an unchanged probability structure; remarks such schemes can simulate/approximate general variables. | 190–204 | Definition and distinction retained (and clarified with a differing-coins example). The general simulation/Uniform(0,1) remark is omitted. |
| `36:40–41:00` | Bernoulli variable/table, `EX=p`, `VarX=pq`, `g=q+ps`; presenter briefly says “variance is 0” while pointing to `g''=0`, then immediately completes the variance formula to `pq`. | 205–215 | Final mathematical conclusion is faithfully `pq`; body cleanly gives the full calculation. The transient spoken slip is not retained and should not be propagated. |
| `41:00–49:00` | Defines binomial as successes in first `n` trials / sum of Bernoullis; derives PGF, mean, variance (calculation left), and PMF by derivative at zero. | 217–266 | Faithful and strengthened: complete derivative calculation is supplied for the PMF; variance calculation remains explicitly left to reader, as in source. |
| `49:00–60:04` | Transition, then recording break / repeated “subscribe”; at `59:25` answers an aside about simulating variables via Bernoulli schemes and Uniform(0,1). | — | Break/non-lecture content omitted. The simulation aside remains omitted (already noted at `32:00–36:40`). |
| `60:04–62:02` | COVID-returnees binomial illustration; explicitly calls equal `p` and independence a rough model/approximation. | 260–265 | Faithful and strengthened: labels it “rough approximation” and spells out the two modelling assumptions. |
| `62:02–65:01` | Defines geometric variable as failures before first success, including `X=min{n≥1:ΣX_j=1}-1`; notes competing count-trials convention; `0001→3`. | 281–285 | Faithful; formal definition and convention/example retained. |
| `66:01–75:00` | Derives `P(X=k)=q^kp`, `g=p/(1-qs)`, `EX=q/p`, `VarX=q/p²` using PGF; contrasts direct-series calculation. | 287–319 | Faithful and strengthened with all derivative algebra. Transcript ASR contains garbled/self-corrected intermediate phrasing around `71:02–73:58`; final result and board-facing derivation are consistent with body. |
| `75:00–79:59` | Examples: fair coin (mean tails before heads 1), `p=.05` infection model (19), basketball with a miss defined as the stopping success, road/vehicle-failure modelling; introduces memorylessness. | 321–327, 343–391 | Coin, infection, and basketball examples retained. The vehicle-failure example is omitted. Coupon-collector material is a new, clearly marked supplement, not source content. |
| `80:01–87:01` | Proves geometric memorylessness; processor and human-life contrast; gambling/roulette and 6/49 illustrations; says geometric is sole discrete and exponential the continuous memoryless law. | 329–341 | Core identity/proof and processor, human-life, gambling, 6/49 examples retained. The “exponential in continuous case” side remark is omitted; sole-discrete characterization is retained. |
| `87:03–91:56` | Defines negative binomial as failures before `r`-th success (`min{n:ΣX_j=r}-r`); `r=1` geometric; COVID capacity illustration; decomposes into IID geometric stages. | 398–403 | Faithful, with the formal minimum expression paraphrased and the stage rationale expanded. |
| `92:00–98:01` | Uses product PGF to derive neg-bin PGF, mean, variance and PMF; mean from linearity, variance requires independence; emphasises analytic derivation. | 405–440 | Faithful and strengthened by a fully legible `k`-derivative derivation. Source has audible/self-corrected formula wording in the transcript; final intended formula matches body. |
| `98:02–99:00` | Pedagogical/exam-level remarks, then moves beyond Bernoulli scheme. | — | Omitted appropriately as administrative/pedagogical guidance. |
| `99:01–102:57` | Defines Poisson by `P(X=k)=λ^ke^{-λ}/k!`; applications (accidents, goals, visible stars, arrivals); says stationary independent-increments rationale is beyond course; verifies probabilities sum to 1; says Poisson approximation to binomial is next lecture. | 442–453 | Faithful. Modelling examples/caveat, normalisation, and forward reference are retained; prose is clearer. |
| `103:01–105:00` | Derives `g=e^{λs-λ}`, `EX=VarX=λ` from first two derivatives. | 455–464 | Faithful, full derivation retained. |
| `105:00–107:07` | Announces next lecture’s Poisson approximation, then Google Meet/hybrid-teaching logistics. | 445, 466–477 | Approximation-forward-reference retained. Logistics omitted appropriately. The four end exercises are added pedagogical material. |

## Added material in the body (not presented in this lecture)

These are mathematically coherent additions, but are fidelity strengthenings rather
than source-transcript content:

1. `122–177`: random sums, PGF composition, Wald/total-variance moments, and Poisson thinning; explicitly marked as a supplement and cross-references lecture 7.
2. `178–188`: PGF/CDF identity and convention discussion; supplement.
3. Figure in `229–251` and `267–279`: binomial PMF graphic and mode calculation; the source did not cover them.
4. `343–391`: coupon collector derivation and asymptotics; supplement.
5. `466–477`: four exercises (including a Poisson exercise) created from/reinforcing source material.

## Stage-A conclusion before blind review

All substantive source topics are represented correctly. The body is a markedly
expanded set of notes: several additions are explicitly marked as supplements, while
the general `k` coefficient proof, detailed derivative calculations, model-assumption
explanations, figures, and exercises are unmarked enrichments. Source-specific minor
omissions are the Pólya/bag attribution, the Bernoulli-to-Uniform simulation aside,
the road/vehicle-failure example, the continuous exponential-memoryless aside, and
administrative/exam/logistics discussion. No unresolved formula dispute yet requires
board/OCR evidence; targeted board review will be used in Stage B if a blind finding
creates one.
