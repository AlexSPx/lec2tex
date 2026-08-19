# Mathematics audit of lectures 7–11 (2026-08-19)

Five independent audits, one per chapter, each run against the lecture
transcript as primary witness, the board OCR, and the handwritten notes as a
third witness. Every checkable claim was verified symbolically or by
simulation; the computations and their output are quoted in each finding.

Scope was mathematics only — no formatting, no typography. Statistics
(lectures 12–14) was deliberately deferred.

| Chapter | Findings | Worst |
|---|---|---|
| [07](lecture_07.md) Поасон, хипергеометрично, корелация | 12 | `\widetilde{X}` defined twice, so the book asserts Cov = ρ |
| [08](lecture_08.md) Условно очакване, непрекъснати | 15 | change of variables: strict monotonicity is not sufficient |
| [09](lecture_09.md) Непрекъснати, Гама, хи-квадрат | 12 | variance additivity under the wrong hypothesis |
| [10](lecture_10.md) Сходимост, Чебишов, ЗГЧ | 9 | the lecturer's definition of "в сила е ЗГЧ" is absent |
| [11](lecture_11.md) ЦГТ, функции на моментите | 9 | `k_n = np + a` is missing its √(np(1−p)) |

## The recurring failure mode

Nearly every substantive finding is one of three shapes, and all three are
pipeline artefacts rather than the lecturer's imprecision:

1. **Two statements merged, the weaker hypothesis kept.** This is the defect
   found in 9.7 before the audit, and it recurs in L09 (product rule vs
   variance additivity) and L08 (the property list).
2. **A caveat that exists only in the audio.** The lecturer says "стига
   очакванията да съществуват", "някакво положително число", "не е
   безпаметно" — the board does not record it, so the pipeline never saw it.
3. **A case split dropped**, leaving a formula asserted outside its domain:
   the exponential CDF for x < 0, the Gamma density at 0 for α < 1,
   `F' = f` at the endpoints of the uniform.

One new mode appeared in L11 and is worth remembering: the board OCR caught a
**half-written formula** (the frame is timestamped mid-radical) and the book
froze it. That is not a dropped caveat — it is a wrong reading of a correct
board.
