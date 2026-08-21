# New fidelity/mathematical findings not in the blind file

## L01-FID-001 — `confirmed_book_error` — wrong historical lottery and hence wrong numerical model (high confidence, P1)

- **Body:** lines 13, 59–66, and 256–284 call the 2009 scandal “6 of 49,” use
  `N=\binom{49}{6}=13,983,816`, and describe 14 second-draw winners.
- **Lecture source:** transcript 03:49–03:53 and 07:17–07:26 says 6/49;
  12:12–12:17 says 14 winners; 28:04–29:29 repeats the 6/49 model. OCR
  `board_008`, `board_068`, and `board_070`–`073` verify the source-visible
  6/49/13,983,816/10,000 model. The book is faithful to the lecturer, but the
  shared claim is factually wrong.
- **External factual check:** contemporary BNT reports identify the actual
  draws as *Toto 2, 6 of 42*, in draw numbers 72 and 73, with identical values
  on 6 and 10 September; its follow-up reports 18 winners, not 14. See
  [BNT’s investigation report](https://bntnews.bg/bg/a/14509-proverki-v-tototo-zaradi-tiraji-s-ednakvi-chisla-na-igrata-6-ot-42) and
  [BNT’s outcome report](https://bntnews.bg/bg/a/14564-njama-narushenija-v-tototo).
- **Independent calculation:** the relevant per-draw state count is
  `\binom{42}{6}=5,245,786`. Under iid uniform draws, any adjacent match among
  10,000 draws has probability
  `1-(1-1/5,245,786)^9999≈0.001904286` (about 1 in 525), not the 6/49 value
  about 1 in 1,399. Thus this is material to the lecture’s motivating
  probability conclusion, not cosmetic history.
- **Disposition:** either label the 6/49 example as a deliberately hypothetical
  model and remove its claimed identity with the 2009 incident, or correct the
  event/game, state count, and winner count everywhere.

## L01-FID-002 — `confirmed_book_error` — Brownian path properties lack the almost-sure qualifier (high confidence, P2)

- **Body:** line 10 says “the trajectory is continuous, nowhere differentiable,
  and has infinite length.”
- **Lecture source:** transcript 02:50–02:56 makes the same claim. No formula
  dispute requires OCR; it is a stochastic-path statement.
- **Analysis:** for Brownian motion those properties hold *almost surely*, not
  as pointwise properties of every path in a path-space realization. Removing
  the probability-one qualifier turns a standard theorem into an overstatement.
- **Disposition:** write “with probability one, sample paths are continuous,
  nowhere differentiable, and of infinite length (indeed infinite variation).”

## L01-FID-003 — `fidelity_omission_or_strengthening` — COVID base-rate example is strengthened (high confidence, P2)

- **Body:** line 16 says that an elementary analysis using vaccinated versus
  unvaccinated population proportions “would show” vaccine effectiveness.
- **Lecture source:** transcript 04:19–04:38 includes more caveats (the
  lecturer expressly says he is not speaking as a vaccine advocate, recognizes
  side effects, and says an analysis might indicate the claim is probably
  wrong), while 08:33–08:43 treats the data as an illustrative modeling
  question. The source does not present a derivation with specified dates,
  denominators, age/risk composition, or a causal estimand.
- **Analysis:** the book removes qualifications and upgrades an illustrative
  base-rate lesson into an asserted empirical conclusion. The stated 4–5%
  numerator alone cannot establish effectiveness; the relevant risk
  denominators and confounding/selection choices must be specified.
- **Disposition:** identify it as a historical hypothetical/base-rate example,
  retain the oral caveat, and do not claim a real-effect estimate without a
  defined dataset and model.
