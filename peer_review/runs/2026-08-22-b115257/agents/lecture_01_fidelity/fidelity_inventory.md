# Stage A — independent body-to-transcript map

Completed and persisted at 2026-08-21T22:20:00Z, before any blind finding was
opened. Primary transcript examined in its entirety: 3,621 chronological
segments, 00:00:00–00:30:30.15. Source locations below are timestamps in
`run/lecture_01/audio/transcript.json`; body locations are numbered lines in
`lectures/bodies/lecture_01.tex`.

## Coverage and recording integrity

The mathematical lecture is continuously represented from 00:05:25 through
00:30:30.15, aside from intelligibility/ASR defects. Observed defects are not
evidence that the original recording is partial: the primary and 1x ASR both
replace the spoken content at 23:28–23:38 and 30:11–30:21 with repeated `Σ`.
At 1x these correspond to 70.28 s and 27.82 s spans respectively. The file
still has material immediately before and after both spans, and board-state
captures continue through 00:30:27.33 (`board_081`). There is no audio/video
file in `run/lecture_01/audio/`, so whether the underlying recording (rather
than its transcript) is corrupt cannot be determined.

The first 05:25 is course administration/encouragement and is deliberately not
reconstructed. It is a source omission only for administrative material, not a
missing mathematical claim. The body is an edited notes artifact rather than a
verbatim transcript; its added worked supplement is identified below.

## Full material map

| Body scope | Transcript coverage | Fidelity status and notes |
|---|---|---|
| 1–7, course goal and motivation | 00:44–01:18; 01:51–05:08 | Preserved in condensed form. Transcript additionally describes course components/assessment (00:09–00:43), consultation/recording advice (01:26–01:50), and a general study exhortation (05:09–05:25); these are omitted, appropriately for lecture notes. |
| 9–10, Brownian motion | 02:00–03:46; 27:05–27:59 | Preserved: Brown 1827, uncertainty about molecular cause, Einstein 1905/kinetic account, nondifferentiable infinite-length idealization, uses in stochastic differential equations. Transcript adds Perrin/Avogadro/Nobel details (02:57–03:10), Parisi/Nobel and Monte Carlo remarks (03:17–03:46), and later a Black–Scholes example (27:29–27:40); omitted. No contradicting formula seen. |
| 13, repeated 6/49 draw and 14 winners | 03:49–04:19; 12:12–12:24; 28:04–29:47 | Preserved. The oral claim is hedged: around 10,000 draws; probability “not so small” as to itself produce serious suspicion. The 14-winner contextual argument appears at 12:12–12:17. Board OCR 069–078 (28:48–29:42) agrees with the event formulation. |
| 16, COVID example | 04:19–04:46; 08:33–08:43 | Preserved with a stronger prose conclusion: the transcript says a base-rate/statistical analysis could indicate the conjecture is probably false and remarks on vaccine effectiveness; the body says it “would show” real effectiveness. This is a fidelity strengthening, though framed as an illustrative historical claim rather than a derivation. |
| 19, Tao/Sendor | 04:59–05:08 | Preserved nearly verbatim: Tao’s work substantially proving Sendov’s conjecture and stochastic element. |
| 22–38, random experiment; elementary events; sample space | 05:25–06:20 | Preserved. Oral lecture calls the preliminary definitions informal/pseudo-definitions (05:27–05:34); body typesets them formally. The semantic content, notation `ω`/`Ω`, and coin rationale are retained. |
| 40–78, coin, die, 6/49, processor lifetime, Brownian sample spaces | 06:40–08:33 | Preserved. OCR `board_008` at 07:55 confirms all displayed coin/die/6/49/`R_+` formulae, including `N=13,983,816`. Transcript gives more board exposition and a remark that exact real-valued measurement is an approximation; body smoothly condenses it. |
| 81–90, events and examples | 10:15–12:01 | Preserved: events are subsets of `Ω`, person/shop and odd-die examples. Transcript also has processor-temperature interval examples (10:56–11:27) and an aside on betting popularity (11:43–12:27); omitted. |
| 92–128, inclusion, union, intersection, complement | 12:45–15:30 | Preserved. The body’s `ω∈A ⇒ ω∈B` agrees with the intended oral definition despite noisy ASR at 12:49–12:52. OCR/board evidence used later for formula disputes, not needed to resolve this one. |
| 130–181, laws/operations | 15:48–18:49 | Preserved: commutativity, associativity, distributivity, countable union/intersection, both De Morgan laws, and involution. Transcript teaches the two countable De Morgan laws explicitly at 17:07–17:42. It does not visibly enumerate the displayed finite distributive identity in the ASR, but does state it at 16:14–16:28; body gives the correct identity. |
| 183–220, sigma-algebra definition and countable-intersection proof | 18:57–22:40 | Preserved and substantially clarified. The oral definition has the same three axioms; the body supplies a complete proof of countable-intersection closure. OCR `board_055` (22:57.67) supports the De-Morgan proof chain and `board_056` shows the trivial-algebra setup. The body removes hesitations and a board-writing false start, not a mathematical claim. |
| 222–238, two finite sigma-algebra examples | 22:53–24:20 | Preserved. The transcript calls the full power set `2^Ω` natural and states its `2^n` cardinality. |
| 240–242, Borel example | 24:21–25:08 | Preserved. Oral lecture explicitly limits scope (will not develop Borel sigma-algebras); the body retains the key reason for them and standard interval examples. This is not a claimed construction of Lebesgue measure. |
| 244–254, target/dart reduction | 25:12–26:33 | Preserved. Transcript says arrow/point location is uncountable but score-sector outcome reduces to three outcomes. OCR `board_062` at 26:32 confirms the eight-element power-set list. |
| 256–284, 10,000-draw totalizer model | 08:48–09:34; 28:04–29:47 | Preserved. OCR `board_066`–`068` verifies `Ω=⊗_{i=1}^{10000}Ω_i`, `|Ω|=N^{10000}`, `A=2^Ω`, and `|A|=2^{N^{10000}}`; OCR `board_071`–`078` verifies `A=⋃_{i=1}^{9999}A_i` and `A_i={ω^(i)=ω^(i+1)}`. Oral speaker explicitly acknowledges the 10,000 versus 10,001 endpoint convenience issue at 28:52–29:00, then uses 9,999 adjacent pairs. The body preserves the final consistent 10,000-draw/9,999-pair formulation. |
| 286–293, De Morgan exercise | 17:11–17:18 | Preserved. Oral instruction is to check the two-set law and optionally the other; body matches. |
| 295–302, two-envelope exercise | 29:48–30:30 | Preserved. Oral source says two values such as 1/2 or 1/10,000; body explicitly allows reals/negatives and formalizes `a<b`, a benign strengthening consistent with an interval-independent strategy. The exact spoken question is obscured by the `Σ` ASR gap (30:11–30:21), but before/after it establish no prior information and ask for a success probability above 1/2. OCR `board_080`–`081` confirms `a<b`. |
| 304–327, envelope solution | No spoken solution; oral lecture ends after assigning the problem | Added editorial supplement, clearly labelled as a solution. It is an addition rather than a misattribution to the lecture. Its correctness needs Stage B mathematical review; as a fidelity matter, the label prevents a false claim that it was spoken. |

## Stage-A independent flags to carry into Stage B

1. **Fidelity strengthening, moderate importance:** line 16 changes the oral
   conditional/hedged COVID reasoning into a stronger claim that analysis
   “would show” effectiveness. It is a temporal medical/statistical example,
   not a theorem proved in the lecture.
2. **Fidelity strengthening, low importance:** lines 26–36 formalize material
   the speaker expressly called informal/pseudo-definitions.
3. **Potential source-model ambiguity, medium importance:** the oral speaker
   acknowledges at 28:52–29:00 that 10,001 draws would make a 10,000-pair
   count convenient, but ultimately writes/uses 10,000 draws and 9,999 pairs;
   the book follows that final formulation. No fidelity error, but it is a
   likely target for a mathematical finding.
4. **Recording evidence limitation:** two ASR spans are replaced by `Σ`; no
   available source audio exists to establish a recording failure. Treat claims
   unique to those spans as `transcription_or_ocr_uncertainty`, not as proof of
   an incomplete original lecture.
