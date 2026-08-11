# Remediation plan — *Вероятности и Статистика* lecture notes

**Status:** open. **Branch containing all sources:** `lecture-notes-sources`.
**Audience:** an engineer/agent picking this up cold. Read §0–§2 before touching anything.

---

## 0. What this document is

Two independent reviews were run against the notes:

1. **An external academic review** (blind — the reviewer was denied access to the
   repo's changelog and scripts so as not to be anchored). It found 14 formatting
   issues, 8 flow issues, 8 pedagogical issues and a verbosity analysis.
2. **A transcript-fidelity audit**, comparing the notes against the raw ASR in
   `run/lecture_NN/audio/transcript.json`.

The second audit **overturned three of the first review's conclusions** and
**reclassified four findings from "authorial choice" to "pipeline bug"**. Both
results are merged below with the root cause identified for each. Do not act on
the academic review alone — several of its recommendations would damage fidelity.

Every claim below is marked with a verification status:

| Mark | Meaning |
|---|---|
| **[V]** | Verified directly against source/PDF during this audit. Counts are reproducible. |
| **[V-T]** | Verified against the raw ASR transcript. Timestamp given. |
| **[R]** | Reported by the external reviewer, plausible, **not independently verified**. |

---

## 1. Repository orientation

```
lectures/
  preamble.tex            shared style: fonts, polyglossia, tcolorbox, amsthm envs
  bodies/lecture_NN.tex   CONTENT — the source of truth. Edit here.
  lecture_NN.tex          AUTO-GENERATED standalone driver. Never edit.
  lectures_full.tex       AUTO-GENERATED book driver. Never edit.
  lectures_full.pdf       the 118-page book
run/lecture_NN/
  audio/transcript.json   raw ASR: [{start, end, text}, ...]  ← ground truth
  board/board_NNN.png     extracted board frames
  ocr/board_NNN.json      per-frame VLM OCR
  board_states.json       [{timestamp, image}] — maps frames to spoken time
  ir/lecture_ir.json      pipeline intermediate representation
scripts/
  build_lectures.py       regenerates drivers + compiles
  migrate_bodies.py       ONE-TIME migration, guarded. Do not run.
  combine_lectures.py     SUPERSEDED. Do not use.
```

**Build:**
```bash
python3 scripts/build_lectures.py           # drivers + book
python3 scripts/build_lectures.py --all     # + 15 standalone PDFs
```

**Two hazards.**
1. `lectures/lecture_NN.tex` and `lectures_full.tex` are overwritten on every
   build. Edits there are silently lost.
2. `scripts/migrate_bodies.py` reads `lectures/lecture_NN.tex` expecting the
   *old* self-contained format. It is guarded by an existence check on
   `lectures/bodies/`; do not defeat the guard.

**Transcript search helper** (write to scratch, not the repo):
```python
import json, re
segs = json.load(open('run/lecture_06/audio/transcript.json'))
rx = re.compile('дисперси', re.I)
for i, s in enumerate(segs):
    if rx.search(s['text']):
        print(f"[{int(s['start']//60)}:{int(s['start']%60):02d}]",
              ' '.join(x['text'] for x in segs[max(0,i-3):i+4]))
```

---

## 2. Ground rules — read before editing

The notes are a **record of a real lecture course**. The following is binding:

* **R1. Do not "correct" the lecturer.** If the transcript shows he presented
  something in a non-standard way, the notes must follow him. Add a footnote if
  it matters; never silently substitute the textbook version. (See D-01, rejected.)
* **R2. Do not remove content.** Paraphrasing for register is fine; deletion is not.
* **R3. Never strengthen a claim.** The dominant failure mode of the generation
  pipeline was converting the lecturer's hedges into flat assertions (§4). When
  in doubt, weaken.
* **R4. Expansion must be recovery, not invention.** Where a chapter is thin, the
  material is in the transcript. Recover it. Do not write new mathematics.
* **R5. Verify against transcript before acting on any content-level finding.**
  Roughly a third of the external review's content findings dissolved on contact
  with the source.

---

## 3. Group A — defects introduced by the last editing pass

These are regressions from the recent restructuring, not inherited problems.
Highest priority: they are cheap and they are the most visible.

| ID | Issue | Location | Status |
|---|---|---|---|
| **A-01** | **28 proof headings render as English "Proof."** `preamble.tex:75` sets `\renewcommand{\proofname}{Доказателство}`, but polyglossia installs its Bulgarian captions at `\begin{document}` and overwrites it. The identical bug was diagnosed and fixed for `\chaptername` (see the comment in `scripts/build_lectures.py`) but the same fix was not applied to `\proofname`. Verified: 28 × "Proof" vs 10 × "Доказателство" in `lectures_full.pdf` (the 10 are cases passing an explicit optional argument). | `lectures/preamble.tex:75` | **[V]** |
| **A-02** | `example` environment declared and used **0 times**; `remark` declared and used **once**. Dead code introduced with the preamble. | `lectures/preamble.tex:68–70` | **[V]** |
| **A-03** | 44 `\label{}` added, only 4 `\ref{}` wired. Cross-reference infrastructure exists but is unused. | `bodies/*.tex` | **[V]** |
| **A-04** | Book and standalone builds number statements differently. `Твърдение 2.2` in `lectures_full.pdf` is a different statement from `Твърдение 2.2` in `lecture_06.pdf`. Both are distributed. | `scripts/build_lectures.py` | **[V]** |
| **A-05** | The only two `\subsubsection`s in the book are in L06, created when the five distribution sections were demoted. With `secnumdepth=2` they render unnumbered and are visually indistinguishable from the `\textbf{}` run-ins used elsewhere. | `bodies/lecture_06.tex:75,139` | **[V]** |
| **A-06** | The book's only `remark` environment sits in the *linear regression* chapter and concerns independence of sums — unrelated to regression. It was created when the exam-logistics section was split. | `bodies/lecture_14.tex:223–227` | **[V]** |
| **A-07** | Exam administrivia retained in the body, set off by a horizontal rule: *"Изискванията за изпита… Консултация преди изпита ще бъде организирана."* This was a deliberate decision to preserve content under R2, but it does not belong in the running text. | `bodies/lecture_14.tex:232` | **[V]** |

### Fixes

* **A-01** — move the `\renewcommand{\proofname}{Доказателство}` out of
  `preamble.tex` and into the document body emitted by `build_lectures.py`,
  next to the existing `\renewcommand{\chaptername}{Лекция}`. Applies to both the
  book driver and the standalone driver. **~5 min.** Verify with:
  `python -c "import pymupdf; t=''.join(p.get_text() for p in pymupdf.open('lectures/lectures_full.pdf')); print(t.count('Proof'))"` → must be 0.
* **A-02 + A-03** — see C-05 and B-06.
* **A-04** — decide which artefact is canonical (§7, decision D-04). If the book
  is canonical, either stop shipping the 15 standalone PDFs, or make the
  standalone drivers offset their counters to match the book.
* **A-05** — either raise `secnumdepth` to 3, or promote the two headings to
  `\subsection` and demote their siblings, or convert them to `\textbf{}` run-ins
  to match the rest of the book. Prefer the last: least disruption.
* **A-06** — move to L07 §7.4 (independence) or delete. It is a stray student
  question, not regression content.
* **A-07** — move to a front-matter note or an appendix. Do not delete (R2).

---

## 4. Group B — pipeline fidelity regressions

**These are the most serious findings in this document.** The generation pipeline
preserved mathematical content but systematically stripped *pedagogical framing* —
hedges, exercise assignments, caveats, attributions and numeric punchlines. In one
case this manufactured a factual error.

All five are verified against the raw ASR.

| ID | What the lecturer said | What the notes say | Location |
|---|---|---|---|
| **B-01** | **L10 @ 65:20** — *"Дали ще го кръстите Марков или Чебишев, те са с един и същи тип на доказателство, няма нещо по същество различно."* An explicit refusal to commit to a name. | *"Едно полезно следствие (често наричано **неравенство на Марков**)"* — a flat, and incorrect, attribution. The stated inequality is a consequence of Markov applied to \|X−EX\|^m, not Markov's inequality. **The pipeline created this error.** | `bodies/lecture_10.tex:142` |
| **B-02** | **L01 @ 3:55** — gives the number (*"Тази вероятност може да е едно около 1000"*), the decisive argument (*"тотализатор има по цял свят… също има в съседните държави, има навсякъде"*), and credits the source (Imperial College colleagues' book). His conclusion is hedged: *"не толкова малка, че да предизвика някакво наистина сериозно съмнение."* | All three dropped. The hedge is **upgraded** to *"всъщност е нормално статистическо отклонение, **напълно очаквано**"* — a stronger claim than the source, and one the arithmetic does not support (≈1 in 1400). The thread is then never resolved numerically in L03. | `bodies/lecture_01.tex:271`; `bodies/lecture_03.tex` §3.2 |
| **B-03** | **L06 @ 46:15** — *"Е, дисперсията е втората производна, аз няма да я записвам. Това Вие ще си го сметнете."* Explicitly assigned as an exercise. | Proposition states parts а) б) в) г); the proof gives а) б) г). Part в) (𝔻X = npq) simply vanishes, reading as an unexplained gap. | `bodies/lecture_06.tex` (binomial prop/proof) |
| **B-04** | **L03 @ 64:12** — *"Не съм си играл да проверявам, че не зависи"* — he states plainly that he did **not** verify independence. | *"Може да се докаже, че ако събитията $A_i$ са независими в съвкупност…"* — unearned confidence. | `bodies/lecture_03.tex:152` |
| **B-05** | **L15 (whole)** — a 73-minute **problem/revision session**, not a lecture: *"припомнете принципа за включване и изключване"*, *"Може ли някой просто да напише нещо в чата"*, *"Помните ли тези неща?"*, and an explicit reference to the prerequisite course (*"това ми се беше паднало на изпита по дискретни с доцент Марков. Сигурно и вие сте при него"*). Works through 11 numbered задачи. | Presented as fresh expository material: *"В тази лекция ще разгледаме някои основни елементи на комбинаториката."* The recap character and all the problems are gone. | `bodies/lecture_15.tex:1–3` |
| **B-06** | **All lectures** — 127 mentions of задача / упражнение / домашно / "оставям на вас" across the 15 transcripts. | 13 survive in the notes. Per lecture (transcript → notes): L02 6→0, L03 8→0, L05 9→0, L06 7→0, L07 6→0, L10 12→1, L12 18→3, L15 24→1. | `bodies/*.tex` |

### Fixes

* **B-01** — restore the lecturer's hedge. Something like: *"Аналогично неравенство
  за произволни моменти $m \ge 1$ (доказва се по същия начин; в литературата се
  среща и като неравенство на Марков, и като неравенство на Чебишов):"* Do **not**
  simply relabel it "Markov" or "Chebyshev" — he deliberately declined to choose.
* **B-02** — highest-value single fix in this section. In L01, replace *"напълно
  очаквано"* with his actual formulation. In L03, add the number (≈1/1400 for the
  consecutive-pairs event; he quoted ≈1/1000 from memory — quote **his** figure and
  footnote the exact value), and restore the multiple-lotteries argument, which is
  what actually resolves the paradox. Restore the Imperial College attribution.
* **B-03** — restore as an explicit exercise: *"Дисперсията се получава по същия
  начин чрез втората производна; оставяме сметката на читателя."* Do **not** write
  the derivation (R1/R4): he chose to assign it.
* **B-04** — replace with his caveat: note that mutual independence of the $A_i$
  is assumed here and not verified, and that the estimate is an approximation.
* **B-05** — **re-frame, do not relocate.** Rewrite the L15 opening to state that
  this is a revision session on material assumed known from discrete mathematics,
  and restore the problems (see B-06). This also dissolves the external reviewer's
  "combinatorics is in the wrong place" complaint — see §8, rejected finding D-02.
* **B-06** — recover the exercises. They are in the transcripts. Add an `Задачи`
  section at the end of each lecture, or an exercises appendix. This is the single
  largest improvement available to the document's teaching value.

---

## 5. Group C — notation and formatting consistency

| ID | Issue | Evidence | Status |
|---|---|---|---|
| **C-01** | **Variance written three ways.** `DX` ×20 (L05, and once at L13), `\mathbb{D}X` ×82 (L06, 07, 08, 10, 11, 14), `\text{Var}(X)` ×18 (L09, L12). They collide across adjacent pages: `\mathbb{D}X` on p. 62, `Var(X)` on p. 66, same quantity. | counts reproducible by grep | **[V]** |
| **C-02** | **Indicator written four ways.** `1_A` ×41 (L04 — the lecture that *defines* it), `\mathbf{1}_A` ×53 (L05, L08), `I_{\{...\}}` ×10 (L10), `1_{(0,\theta)}` (L12). | " | **[V]** |
| **C-03** | **Conditional bar mixed.** 90 × `\mid`, 28 × bare `|`. Concentrated: L10 has 14 bare vs 1 `\mid`; L11 has 8 bare vs 0. Bare `|` produces wrong spacing. | " | **[V]** |
| **C-04** | **Distribution names inconsistent.** `\text{Bi}` ×2 vs `\text{Bin}` ×3; `\text{Poi}` ×2 vs `\text{Po}` ×1; `\text{Ber}` ×5 vs `\text{Bernoulli}` ×1. | " | **[V]** |
| **C-05** | **~40 examples have no environment.** 25 as `\textbf{Пример …}` run-ins, 15 as `\subsection{Пример …}`. None numbered, none citable; the 15 subsection ones clutter the TOC hierarchy while the other 25 are invisible to it. | " | **[V]** |
| **C-06** | **Run-on numbered list inside a definition box.** Literal `1.` `2.` `3.` instead of `enumerate`; renders as one justified block and causes 3 of the book's 12 underfull hboxes. The identical definition at `lecture_08.tex:208–218` correctly uses `enumerate`. | `bodies/lecture_09.tex:165–171` | **[V]** |
| **C-07** | **Hyphen list renders inline.** `- $X$: …` / `- $Y$: …` appear mid-paragraph in the justified text. | `bodies/lecture_07.tex:139–140` | **[V]** |
| **C-08** | **Interpretive prose trapped inside proofs** — forward-looking summary sentences placed before `\end{proof}`, so the flush-right □ terminates a sentence that is not part of the proof. | `bodies/lecture_07.tex:263, 308` | **[V]** |
| **C-09** | **`\ln k` becomes `\ln K`** mid-derivation, same constant. | `bodies/lecture_13.tex:274,278,282,286,290` (`k`) vs `:295` (`K`) | **[V]** |
| **C-10** | **CDF convention broken.** `lecture_05.tex:9` explicitly flags that this text uses $F(x)=\mathbb{P}(X<x)$, contra the English convention. `lecture_09.tex:191` then uses $\mathbb{P}(X_1 \le x_1, \dots)$. Reviewer also reports breaks at `lecture_11.tex:183` and `lecture_13.tex:15`. | `lecture_09.tex:191` **[V]**; L11/L13 **[R]** |
| **C-11** | **Dash style mixed.** 10 × ASCII `--`, 21 × en-dash `–`, 18 × em-dash `—`, for the same parenthetical function. The ASCII ones are concentrated in L12. | counts reproducible | **[V]** |
| **C-12** | **Tables ruled three ways.** `tabular{\|c\|c\|c\|c\|c\|}` (L04, full grid), `tabular{c\|c\|c}` (L06, partial), `array` inside display math ×3 (L08). | " | **[V]** |
| **C-13** | **Spelling / grammar.** `сига-алгебра` → сигма-алгебра (`lecture_10.tex:5`); `множестото` → множеството (`lecture_08.tex:160`); `наклона $\beta_1$ е нула` → наклонът, subject position (`lecture_14.tex:187`). | | **[V]** |
| **C-14** | **Two abbreviations coined for one concept**, only one used: *"най-мощна (н.м.о.), или оптимална (о.к.о.)"*. Drop о.к.о. | `bodies/lecture_13.tex:226,248` | **[V]** |
| **C-15** | **Roman/Cyrillic ordinal mix**: `грешка от I-ви род` / `II-ри род`. Standard Bulgarian is *от първи / втори род*. | `bodies/lecture_13.tex:210,212,216` | **[V]** |
| **C-16** | **Residual oral register.** `В тази глава` (wrong unit noun — everything else says "лекция") `lecture_06.tex:3`; `В началото на днешната лекция` `lecture_05.tex:3`; `Искам да обърна специално внимание` `lecture_05.tex:9`; `Миналия път видяхме` `lecture_05.tex:13`; `Днешната лекция е посветена на` `lecture_10.tex:3`; `За финал` `lecture_11.tex:188`. | | **[V]** |
| **C-17** | **Dangling pointer**: *"виж следващия пример"* — there is no following example; the next element is §9.4. | `bodies/lecture_09.tex:285` | **[V]** |

### Fixes

The bulk of C-01–C-04 is one mechanical pass:

```latex
% add to preamble.tex
\newcommand{\E}{\mathbb{E}}
\newcommand{\Var}{\mathbb{D}}          % pick ONE and hold it
\newcommand{\ind}{\mathbf{1}}
\newcommand{\given}{\mid}
\DeclareMathOperator{\Bin}{Bi}
\DeclareMathOperator{\Poi}{Po}
\DeclareMathOperator{\Ber}{Ber}
```
then rewrite the bodies onto these. **Choose the target spellings from the most
common existing usage** (`\mathbb{D}`, `\mathbf{1}`, `\mid`) so the diff is
smallest. Re-verify counts afterwards; the check is that each concept has exactly
one spelling across `bodies/*.tex`.

C-05: convert all ~40 examples to the declared `example` environment (unboxed,
numbered on the shared counter — this also retires A-02), and remove the 15
`\subsection{Пример …}` headings from the hierarchy.

C-06–C-09, C-13–C-15, C-17: point fixes, ~30 min total.

C-16: rewrite in written register. Preserve meaning (R2) — *"Миналия път видяхме"*
becomes a `\ref` to the relevant chapter (see A-03), not a deletion.

---

## 6. Group D — content thinness and expansion

### 6.1 The measurement

Retained written prose as a fraction of spoken words, per lecture. Prose words
only: LaTeX markup, inline and display maths stripped.

| lec | 01\* | 02 | 03 | 04 | 05 | **06** | 07 | 08 | **09** | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| lecture min | 31\* | 109 | 108 | 107 | 103 | 107 | 108 | **167** | **171** | 108 | 107 | 107 | 108 | 97 | 74 |
| spoken words | 10779\* | 11631 | 9618 | 10158 | 9218 | 11163 | 10303 | 15895 | 15302 | 10829 | 9720 | 9794 | 5181 | 8186 | 6539 |
| notes words | 1987 | 1266 | 2027 | 1668 | 2105 | **610** | 1967 | 2216 | **1276** | 1709 | 1671 | 1419 | 2009 | 1366 | 999 |
| **kept** | 18% | 11% | 21% | 16% | 23% | **5.5%** | 19% | 14% | **8.3%** | 16% | 17% | 15% | 39% | 17% | 15% |

Mean retention **17%**.

\* **L01's row is unreliable** — 10 779 words in 31 minutes is 348 wpm, which is
impossible. `run/lecture_01/` is 43 MB against ~1 GB for the others, so the
capture is probably partial. Do not use L01's ratio for anything.

**L06 (5.5%) and L09 (8.3%) are the outliers**, at roughly a third of the mean.
They are also exactly the two chapters the blind external reviewer independently
flagged as "too thin" from the rendered PDF alone, without access to this table.
Two independent methods agreeing makes this the most solid finding in the document.

L08 and L09 were ~170-minute **double lectures** compressed at or below the rate
applied to 107-minute ones.

### 6.2 Specific gaps

| ID | Issue | Location | Status |
|---|---|---|---|
| **D-10** | L06 at 131 words/page against a book norm of ~225. Three results asserted without derivation: the geometric variance (*"Аналогично, чрез втората производна се получава…"*), the negative-binomial pmf $\binom{r+k-1}{k}p^rq^k$ (stated with no argument, and it is the least obvious formula in the chapter), and binomial part в) (= B-03). | `bodies/lecture_06.tex` | **[V]** thinness; **[R]** the two non-B-03 gaps |
| **D-11** | L09 at 162 words/page across 56 display equations. The 2-D change-of-variables theorem, the Jacobian and the convolution formula are given in ~48 lines with the proof replaced by a single sentence. | `bodies/lecture_09.tex:237–285` | **[R]** |
| **D-12** | L14 contains **no worked numerical example** — the one topic a software-engineering cohort will implement. Galton's anecdote, seven pages of algebra, no data. | `bodies/lecture_14.tex` | **[V]** (no numerals in the chapter) |
| **D-13** | The two-envelope problem is posed at `lecture_01.tex:273–280` and never answered anywhere in the remaining 14 lectures. | | **[R]**, grep for "плик" supports it |
| **D-14** | L11 §11.1 re-derives the SLLN setup that L10 has just stated as a theorem (~250 words of restatement). | `bodies/lecture_11.tex:1–13` | **[R]** |
| **D-15** | Running examples repeat without cross-reference: tug-of-war ×3 (L05, L10, L11), roulette ×2, Monte Carlo ×3, Toto ×4. Each occurrence re-introduces its setup from scratch. | | **[R]** |
| **D-16** | Over-explained relative to content: L01 §1.1 (~480 words of four vignettes before the first definition; the COVID and Tao ones never recur) and §1.3.2 (~350 words restating set identities the text itself calls "интуитивни и добре познати"). L03 §3.1.1 (~300 words on the dice example before the definition it motivates, which then redoes the same computation). | | **[R]** |

### 6.3 How to expand

**This is a recovery job, not a writing job (R4).** There are 11 163 spoken words
behind L06's 610.

Recommended procedure per chapter:
1. Read the full transcript for the lecture end-to-end.
2. Cross-reference `board_states.json` → `board/board_NNN.png` → `ocr/board_NNN.json`
   to recover what was actually written on the board at each timestamp. The board
   is where the derivations live; the ASR alone will not give you them.
3. Restore derivations the lecturer actually performed. Mark as exercises the ones
   he explicitly assigned (B-03 is one; there will be others).
4. Target the 17% mean, not 100%. The goal is parity with the rest of the book.

**Order: L06 first** — worst compression, hardest material, and short enough
(107 min, 11k words) to validate the approach before committing to L09's 15 302.

---

## 7. Decisions requiring a human

These are not defects. Do not act unilaterally.

* **D-04 — canonical artefact.** Are the 15 standalone PDFs still shipped? This
  determines the fix for A-04 and whether statement numbers must agree across both.
* **D-05 — exercises destination.** Per-lecture `Задачи` sections, or a single
  appendix? Affects B-06's shape.
* **D-06 — L08 split.** L08 is a 167-minute double lecture covering conditional
  expectation *and* the whole introduction to continuous random variables; its own
  title admits it. The seam is at `bodies/lecture_08.tex:197`. Splitting it into
  two chapters would renumber lectures 9–15 and break the correspondence with the
  video playlist. Recommend: leave as is, or split and document the mapping.
* **D-07 — front matter.** The book has no preface, no prerequisites statement, no
  notation table. A notation table would prevent recurrence of C-01–C-04.

---

## 8. Rejected findings — do not action

The external review raised these. The transcript audit shows each would damage
fidelity. Recorded here so they are not re-raised.

* **D-01 — "Replace L02's axioms with the standard Kolmogorov three."**
  **Rejected.** L02 @ 3:16 — the lecturer states exactly three properties, the
  second being $\mathbb{P}(A^c) = 1 - \mathbb{P}(A)$; he then spends 45:11–46:11
  verifying it for his discrete construction and assigns the third to the students.
  The redundant complement axiom is genuinely his. The notes are faithful. Changing
  this would violate R1. A footnote noting the relationship to Kolmogorov's
  formulation is acceptable; substitution is not. **[V-T]**
* **D-02 — "Move combinatorics (L15) to a Lecture 0 / appendix, because
  $\binom{49}{6}$ is used on page 3."** **Rejected as stated.** L15 is a revision
  session on material students already had in discrete mathematics (B-05), so the
  earlier use is legitimate — students knew binomial coefficients. The real defect
  is that the notes misrepresent the session's character. Fix B-05 (re-framing);
  do not relocate the chapter.
* **D-03 — "Add exercises."** **Not rejected, but reclassified.** The
  recommendation is right; the framing ("write exercises") is wrong. 127 exercises
  exist in the transcripts and were dropped. This is B-06, a recovery task.

---

## 9. Suggested sequencing

| Phase | Contents | Effort | Risk |
|---|---|---|---|
| **1** | A-01, C-06, C-07, C-08, C-09, C-13, C-14, C-15, C-17 | ~1 h | none — mechanical |
| **2** | C-01–C-04 (macro pass), C-11, C-12, C-16, A-05 | ~3 h | low — verify counts after |
| **3** | **B-01 … B-04** (fidelity restorations) | ~2 h | **must re-read transcripts; do not do from this document alone** |
| **4** | A-02 + C-05 (example environment), A-03 (wire cross-references), A-06, A-07 | ~4 h | low |
| **5** | B-05 + B-06 (L15 re-frame, exercise recovery) | ~2 d | medium — editorial judgement |
| **6** | D-10 (L06 recovery), then D-11 (L09) | ~3 d | medium — the main content work |
| **7** | D-12, D-13, D-14, D-15, D-16 | ~2 d | medium |

Phase 3 is deliberately placed after the cosmetic work: it is the phase most
likely to need a second opinion, and it should not be blocked behind it.

---

## 10. Acceptance criteria

Run after each phase:

```bash
python3 scripts/build_lectures.py --all        # all 16 must compile
```

| Check | Command | Required |
|---|---|---|
| No English captions | count `Proof`/`Contents`/`Глава` in `lectures_full.pdf` | 0 |
| No unresolved refs | count `??` in extracted text | 0 |
| Overfull boxes | tectonic log, unique lines | ≤ 2 (current baseline) |
| Duplicate page numbers | folio frequency in the book | none |
| One spelling per concept | grep for the C-01–C-04 variants | 1 each |
| No content loss | prose word count vs pre-change | must not fall |

The last is the important one. Baseline at the time of writing: **24 295** Bulgarian
prose words across `bodies/*.tex`. Phases 5–7 should push this **up**, not down.
Any phase that reduces it needs justification against R2.
