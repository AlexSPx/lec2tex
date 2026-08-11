# Лекции — Вероятности и Статистика (СИ, 21/22)

Fixed, consistently-styled LaTeX lecture notes generated from the course video
playlist. Separate from the raw pipeline outputs in `run/`.

## Layout

```
lectures/
  preamble.tex           shared preamble — fonts, language, boxes, theorem envs
  bodies/lecture_NN.tex  the actual content. THIS IS THE SOURCE OF TRUTH — edit here
  lecture_NN.tex         auto-generated standalone driver (do not edit)
  lectures_full.tex      auto-generated combined-book driver (do not edit)
```

## Building

```
python3 scripts/build_lectures.py          # drivers + the combined book
python3 scripts/build_lectures.py --all    # + all 15 standalone PDFs
python3 scripts/build_lectures.py --gen-only
```

`lectures_full.pdf` (118 pp.) is the combined book: one title page, **one**
master table of contents, continuous pagination, running heads, and numbering
that runs across the whole volume (`Дефиниция 7.3`, `Теорема 11.1`, …).
`lecture_NN.pdf` are the same bodies as standalone articles.

| # | Тема |
|---|------|
| 01 | Въведение. Случайни експерименти, събития и σ-алгебри |
| 02 | Аксиоми на вероятността. Дискретна и геометрична вероятност |
| 03 | Условна вероятност, независимост и формула на Бейс |
| 04 | Случайни величини. Индикатори и дискретни случайни величини |
| 05 | Функция на разпределение. Математическо очакване и дисперсия |
| 06 | Пораждащи функции и основни дискретни разпределения |
| 07 | Теорема на Поасон. Хипергеометрично разпределение, ковариация и корелация |
| 08 | Условно математическо очакване. Непрекъснати случайни величини |
| 09 | Непрекъснати разпределения. Гама и хи-квадрат разпределение |
| 10 | Видове сходимост. Неравенство на Чебишов и закони за големите числа |
| 11 | Централна гранична теорема и функции на моментите |
| 12 | Точкови оценки. Максимално правдоподобие и метод на моментите |
| 13 | Доверителни интервали и проверка на хипотези |
| 14 | Линейна регресия |
| 15 | Комбинаторика и просто случайно блуждаене |

## Editorial conventions

- **Statements are numbered environments**, not hand-typed bold labels:
  `defn` (blue box), `thm` / `prop` / `lem` / `cor` (green box). All five share
  one counter, so `Твърдение 4.7` is unambiguous and `\label`/`\ref` works.
- **Proofs are `\begin{proof}`**, always *outside* the box, always closed by an
  automatic flush-right □.
- **Three reading tiers**, so the text can be skimmed. Explained to the reader in
  the front-matter chapter *Как да четете тези записки*:

  | tier | environments | look | meaning |
  |---|---|---|---|
  | landmark | `keythm` `keydefn` `keylem` | gold, 2.2 mm left bar, ★ | memorise; start revision here |
  | standard | `defn` / `thm` `prop` `lem` `cor` | blue / green box | ordinary definition / result |
  | skippable | `example`, `proof` | no fill, hairline left rule (▷ on examples) | safe to skip on a first pass |

  Each tier differs in **rule weight and fill** as well as hue, so the hierarchy
  survives greyscale printing. `keythm` shares the counter with `thm` and prints
  the same name — the mathematical status is identical, only the study weight
  differs. Currently 24 of 107 statements are starred (22%); keep it near that.
  Starring more destroys the signal.
- Defined terms use `\emph{}`. Bulgarian quotation marks `„ “`. Decimal comma,
  braced in math (`$0{,}95$`) so TeX does not set it as punctuation.
- Course/exam logistics are kept out of the mathematical flow (see the note at
  the end of Lecture 14).

## What was fixed in the current pass

**Typesetting.** Added `polyglossia` with `\setmainlanguage{bulgarian}`. Without
Bulgarian hyphenation patterns TeX could not break a single Cyrillic word, which
was the cause of **243 overfull `\hbox`es** (worst 43 pt ≈ 0.6 in) and the loose,
gappy justification throughout. Now **4**, worst 10 pt. Also added
`\frenchspacing` (so `г.`, `т.е.` no longer get sentence spacing), `microtype`,
widow/orphan penalties, and `\emergencystretch`. The auto-generated headings are
now Bulgarian (`Съдържание`, not `Contents`).

**Boxing.** The previous pass boxed statements with a regex that fired only on a
literal `\textbf{Дефиниция…}` label, so five lectures (02, 03, 13, 14, 15) got no
boxes at all despite being full of definitions — including the probability
axioms, conditional probability, independence, Bayes, confidence intervals and
the Neyman–Pearson lemma. Those are now boxed, and two truncated boxes were
repaired: the **Central Limit Theorem** box ended at `Тогава е вярно следното:`
with its conclusion outside the box, and the **σ-algebra** definition ended
before its three conditions. Three proofs that had been sealed *inside* their
statement boxes (L04, L05 ×2) were moved out.

**Cross-references.** An earlier cleanup removed the `а) б) в)` subsection
letters in Lecture 2 but left the prose pointing at them (`от точка б)`,
`от монотонността (точка в)`). Those now resolve through `\ref` to numbered
propositions.

**Section balance.** Sections were re-cut so the master contents is uniformly
useful. Previously four sections carried 47–69% of their whole lecture
(L13 §1 was 1393 words, 69% of the lecture; L08 §4 was 1038; L05 §2 was 1000)
while six others were 39–88-word stubs. Now no section exceeds 800 words and
none is under 100 (median 304). Specifically: L13 and L15 gained a third
section, L08 was split three ways, L05's pool-testing example was promoted; L06's
five one-paragraph distribution sections were gathered under
*Основни дискретни разпределения*, and L11's 70-word MGF worked example became a
subsection of the section it belongs to. Also fixed: **L05 §2 was titled
"Математическо очакване и дисперсия" while §3 was "Дисперсия"** — the title
over-claimed and is now "Математическо очакване". The one prose cross-reference
affected (`както в Пример 1`) now goes through `\ref`.

**Combined document.** Was previously produced by stitching the 15 compiled PDFs
with PyMuPDF (`scripts/combine_lectures.py`, now superseded), which gave 15
separate contents pages, no master TOC, and page numbers restarting at 1 in
every lecture — 15 pages printed "1", 15 printed "2", and so on across 122
pages. It is now a real `report`-class document with lectures as chapters.

The mathematical content is unchanged apart from paraphrasing: lecturer-voice
narration (`Лекторът дава интуиция…`, `Днес ще продължим…`) was rewritten in the
register of the surrounding text, and the exam-logistics paragraph in Lecture 14
was separated from the mathematics. Two transcription typos (`параметьр` →
`параметър`) were corrected. Nothing was removed.

`all_lectures.pdf` is the stale output of the old merge script and can be
deleted; `lectures_full.pdf` replaces it.
