# Mathematics audit — `lectures/bodies/lecture_11.tex`
## "Централна гранична теорема и функции на моментите"

Witnesses used: `run/lecture_11/audio/transcript.json` (primary, 3634 segments, 107 min);
`run/lecture_11/ocr/board_0NN.json` + the board PNGs; `run/pesho/ocr/page_032–036.json`
(the student notebook covers exactly this lecture); `refs/probability1BG-2.pdf` (course
summary — has both Berry–Esseen and de Moivre–Laplace).

All numeric/symbolic checks were run with `/Users/g8row/Documents/lec2tex/.venv/bin/python3`
(sympy + scipy + numpy). Scripts left in the scratchpad as `v1.py`–`v5.py`.

**Headline:** the σ/√n normalisation that was broken in an earlier pass is now correct and I
confirmed it by simulation. One new hard error was found (the binomial threshold `k_n`), plus
one dropped hypothesis the lecturer stated aloud, one whole worked numerical example that is
missing, and several missing domain conditions on the moment generating function.

---

## 1. WRONG — the binomial threshold `k_n = np + a` is missing its `√(np(1−p))`, and the conclusion of the example is gone

**Location:** `lectures/bodies/lecture_11.tex:236` (§ "ЦГТ за Биномно разпределение", the text
between the two displays at :235 and :237)

**What it says now:**
> Това ни позволява да оценяваме лесно вероятности от вида $\mathbb{P}(X_n \ge k_n)$, където $k_n = np + a$:
> \[ \mathbb{P}(X_n \ge k_n) = \mathbb{P}\left( \frac{X_n - np}{\sqrt{np(1-p)}} \ge \frac{k_n - np}{\sqrt{np(1-p)}} \right) \approx \mathbb{P}\left( Z \ge \frac{k_n - np}{\sqrt{np(1-p)}} \right). \]

**Why that is wrong.** With `k_n = np + a` the threshold in the final display is
`a/√(np(1−p)) → 0`, so the whole display degenerates to `P(X_n ≥ k_n) → 1/2` for every fixed
`a`. It carries no information, and it is not what was said. The lecturer explicitly warned
against a fixed offset and then gave the right scaling:

> [100:46] «Обикновено К зависи от Н, то не е фиксирано.»
> [101:05] «например, ако вземете КН да е Н п плюс, да кажем, А корен Н, п по 1-п, това нещо ще ви е по-голямо или равен на А.»

i.e. `k_n = np + a√(np(1−p))`, whereupon the standardised threshold is exactly `a` and the
approximation reads `P(X_n ≥ k_n) ≈ P(Z ≥ a) = 1 − Φ(a)`. The book states the parametrisation
and then omits that punchline entirely.

**Root cause (worth recording).** `run/lecture_11/ocr/board_016.json` does read
`k_n = np + a` — but the frame `run/lecture_11/board/board_016.png` is timestamped 6072 s
(101:12) and shows the lecturer's hand still on the board at exactly the point where the
radical goes; the audio for the radical («А корен Н, п по 1-п») runs 6070.5–6073.4 s. The
pipeline OCR'd a half-written formula and the book froze it.

**Verification** (`v2.py`, scipy exact binomial vs both parametrisations, p = 0.3, a = 2):

```
 n        P(X_n>=np+a) exact   book approx   lecturer's k_n=np+a*sd
      100      0.36689           0.33126          0.02099
     1000      0.45698           0.44512          0.02533
    10000      0.48636           0.48259          0.02316
  1000000      0.49864           0.49826          0.02278
 10000000      0.49957           0.49945          0.02275     (P(Z>=2)=0.02275)
```
The book's version converges to 1/2; the lecturer's converges to `1 − Φ(2) = 0.02275`.

**Suggested fix:**
> Това ни позволява да оценяваме лесно вероятности от вида $\mathbb{P}(X_n \ge k_n)$. Обикновено границата $k_n$ зависи от $n$ и не е фиксирана; ако например $k_n = np + a\sqrt{np(1-p)}$, то
> \[ \mathbb{P}(X_n \ge k_n) = \mathbb{P}\!\left( \frac{X_n - np}{\sqrt{np(1-p)}} \ge \frac{k_n - np}{\sqrt{np(1-p)}} \right) \approx \mathbb{P}(Z \ge a) = 1 - \Phi(a). \]

---

## 2. UNSOUND — ЦГТ (и Бери–Есеен, и Линдеберг–Фелер) assume σ² finite but not σ² > 0, although the lecturer said "положително число"

**Location:** `lectures/bodies/lecture_11.tex:20` (`\begin{keythm}[Централна гранична теорема]\label{thm:clt}`);
same defect propagates to `:271` (`thm:berry-esseen`), `:105` (`supp:lindeberg`) and `:232` (§ ЦГТ за биномно).

**What it says now:**
> Нека $(X_i)_{i=1}^\infty$ са независими и еднакво разпределени (н.е.р.) случайни величини със средно $\mu = \E[X_1]$ и дисперсия $\Var[X_1] = \sigma^2 < \infty$. Тогава за
> \[ Z_n := \frac{\sqrt{n}}{\sigma} E_n = \dots = \frac{S_n - n\mu}{\sigma\sqrt{n}} \]

**Why that is wrong.** If `σ² = 0` — i.e. `X_i ≡ μ` a.s., a perfectly legitimate i.i.d.
sequence with finite variance — then `S_n − nμ = 0` and `σ√n = 0`, so `Z_n = 0/0` is not
defined and the theorem as stated is meaningless rather than merely uninteresting. The
lecturer stated positivity explicitly, in the same breath as finiteness:

> [5:52] «а тук допускаме съществуването на дисперсия сигма квадрат, което моментално влече съществуването на това очакване…»
> [6:06] «но ето тази крайн[ост] на тази дисперсия, че [е] някакво положително число, влече следното.»

Neither the board (`board_002.json`: `DX_1 = \sigma^2 < \infty`) nor pesho (`page_035`) wrote
the positivity, so this is a case where the audio is the only witness that has it — exactly
the class of loss this audit is looking for.

The same omission bites three more places:
* `:271` divides by `σ³`;
* `:105–111` (`supp:lindeberg`) divides by `s_n` and `s_n²`, so it needs `s_n > 0`;
* `:232–235` needs `p ∈ (0,1)`, otherwise `√(np(1−p)) = 0`. The course's own summary states
  this hypothesis explicitly ("Теорема 4.11 (Моавър-Лаплас). Нека $Z \sim N(0,1)$ и
  $X_n \sim Bin(n,p)$, за $p \in (0,1)$", `refs/probability1BG-2.pdf`).

**Verification.** Symbolic/definitional (`v4.py` §11): with `X_i ≡ μ`, `Z_n = 0/0`. No
simulation needed. Separately I confirmed the *non-degenerate* normalisation is right —
see "Checked and found sound", item 1.

**Suggested fix:** in `thm:clt`, replace the hypothesis with
> …със средно $\mu = \E[X_1]$ и дисперсия $\Var[X_1] = \sigma^2$, за която $0 < \sigma^2 < \infty$.

add `s_n > 0` (or `\sigma_j^2` not all zero) to `supp:lindeberg`, and open § "ЦГТ за Биномно
разпределение" with `Нека $p \in (0,1)$ и $X_n \sim \Bin(n,p)$`.

---

## 3. UNSOUND — the properties of $M_X$ are stated with no domain condition at all, so the "k-th derivative gives the k-th moment" property is false as written

**Location:** `lectures/bodies/lecture_11.tex:162–175` (the `enumerate` "Свойства на функциите
на моментите"), specifically item 2 at `:164–167`.

**What it says now:**
> \item \textbf{Връзка с моментите:} Използвайки развитието на експоненциалната функция в ред на Тейлър, $e^{tX} = \sum_{k=0}^\infty \frac{t^k X^k}{k!}$, и **разменяйки очакването и сумата**, получаваме:
> \[ M_X(t) = \E\left[\sum \frac{t^kX^k}{k!}\right] = \sum_{k=0}^\infty \frac{t^k}{k!}\E[X^k]. \]
> Това представяне кодира моментите на $X$. $k$-тата производна на $M_X(t)$ в точката $t=0$ ни дава точно $k$-тия момент:
> \[ \left.\frac{d^k}{dt^k}M_X(t)\right|_{t=0} = \E[X^k]. \]

**Why that is wrong.** The definition at `:128` says the MGF is taken "за всички $t$, за които
това очакване съществува…, **обикновено** в някакъв интервал $|t| < r_0$ ($r_0 > 0$)" —
"обикновено" is a hedge, not a hypothesis, and `rem:charfun` at `:177` then correctly says
there are random variables for which the MGF does not exist. So the properties list inherits
no condition, and item 2 is asserted for arbitrary `X`. Concrete failing case: let
`P(X = k) = 1/(ζ(3)k³)`, `k = 1,2,…`. Then `E[X] < ∞`, `E[X²] = +∞`, and
`M_X(t) = +∞` for **every** `t > 0`, so `M_X` is finite only on `(−∞,0]` — there is no
neighbourhood of 0 at all, the two-sided derivative at 0 does not exist, and no derivative
could produce the (infinite) second moment. The series identity likewise needs
`|t| < r_0` (it is a Tonelli interchange, which is why "разменяйки очакването и сумата"
needs a condition rather than just a comma).

Note also that item 5 (`:173`, uniqueness) *does* carry the correct condition ("за всички $t$
в някаква околност на нулата ($|t| < r_0$)"), and item 6 (`:174`) carries
`t \in (-\varepsilon,\varepsilon)`. So the chapter is internally inconsistent: the two
properties that need a neighbourhood of 0 have it, and the two that need it just as badly
(items 2 and 3) do not.

**Verification** (`v5.py`):
```
 P(X=k) = 1/(zeta(3) k^3)      c = 1/zeta(3) = 0.83190737
 E[X]   = c*zeta(2) = 1.3684328   (finite)
 E[X^2] = oo                       (sympy Sum(...).doit() -> oo)
 t=0.1: 200th term of sum c e^{tk}/k^3 = 4.634e+01  (grows without bound) -> M_X(t)=+oo
```

**Suggested fix.** Preface the list at `:162`:
> Навсякъде по-долу допускаме, че функцията на моментите е крайна в някаква околност на нулата, тоест че съществува $r_0 > 0$ с $M_X(t) < \infty$ за $|t| < r_0$; без това допускане свойства 2. и 3. не са в сила.

and add to item 2 a footnote in the sanctioned style:
> \footnote{Размяната на очакването и безкрайната сума, както и диференцирането под знака на очакването, се обосновават именно от крайността на $M_X$ в околност на нулата; в лекцията те бяха извършени без коментар.}

---

## 4. LOST — the whole worked numerical CLT computation (the ~10⁶-particle / Brownian model) is absent

**Location:** absent; belongs after `ex:11-1` (`lectures/bodies/lecture_11.tex:85`) or in
§ "Приложения" at `:229`. Transcript [76:12]–[81:24], roughly five minutes.

**What the lecturer gave.** He re-read the tug-of-war model as a physical one — a particle
struck by molecules from left and right, "прототип на движение, браво[новско] движение" —
took `n = 10⁶` particles, declared "movement" to occur when the resultant force exceeds
1000, and then did the arithmetic out loud:

> [80:08] «Ние знаем, че SN върху корен N, което в този случай е S 10 на 6 върху 1000 точно, е приблизително Z.»
> [80:34] «Това означава точно S 10 на 6 върху 10 на 3 да е по-голямо от единица, което от централна[та] гранична[та] теорема е приблизително Z да е по-голямо от единица, или ако ползвате таблиците, тази ще бъде единица минус Ф от 1.»
> [80:59] «Ако вместо 1000 тук имахте 5 пъти по 1000 или 5000 … тук ще имате 5 и Ф[от] 5 и тук трябва да знаете, че това е приблизително 0.»

**Why this matters.** As it stands the chapter contains **no** worked CLT calculation that
produces a number and no use of the normal tables, even though the lecturer stressed the
table lookup twice and the sample-size section later leans on exactly that skill. `ex:11-1`
stops at the symmetry answer 1/2; exercise 2 at `:309` asks the reader to "помислите как ЦГТ
се прилага" to the >100 variant but gives nothing. This is the B-06-shaped loss (a numeric
punchline dropped) applied to the chapter's central technique.

**Verification.** `√(10⁶) = 10³`, so the threshold `1000/10³ = 1` and
`P(S_n > 1000) ≈ 1 − Φ(1) = 0.1587`; for 5000 the threshold is 5 and
`1 − Φ(5) = 2.87×10⁻⁷ ≈ 0` (scipy `norm.sf(1)`, `norm.sf(5)`). Both match what he said.

**Suggested fix.** Add an `example` after `ex:11-1`, e.g.:
> \begin{example}[Частица, блъскана от молекули]
> Същият модел описва движението на частица, върху която отляво и отдясно се удрят молекули: $X_j = \pm 1$ е приносът на $j$-тия удар, а $S_n$ — резултантната сила. Нека $n = 10^6$ и нека приемем, че частицата се задвижва, когато резултантната сила надвиши $1000$. Тъй като $\sigma = 1$ и $\sqrt{n} = 10^3$,
> \[ \mathbb{P}(S_n > 1000) = \mathbb{P}\!\left(\frac{S_n}{\sqrt n} > 1\right) \approx \mathbb{P}(Z > 1) = 1 - \Phi(1) \approx 0{,}16, \]
> което се отчита от таблицата за стандартното нормално разпределение. Ако прагът е $5000$, то $\mathbb{P}(S_n > 5000) \approx 1 - \Phi(5) \approx 0$.
> \end{example}

---

## 5. UNSOUND — Бери–Есеен is stated without the hypothesis $\E|X_1-\mu|^3 < \infty$

**Location:** `lectures/bodies/lecture_11.tex:269–273` (`thm:berry-esseen`)

**What it says now:**
> \begin{thm}[Неравенство на Бери\,--\,Есен]
> За всяко $x \in \mathbb{R}$
> \[ \left| \mathbb{P}(Z_n < x) - \Phi(x) \right| \le \frac{C \cdot \E[|X_1 - \mu|^3]}{\sigma^3 \sqrt{n}}, \]
> където $C$ е абсолютна константа (около $0{,}47$).
> \end{thm}

**Why that is a defect.** Strictly the inequality is vacuously true when the third absolute
central moment is infinite, so this is statement hygiene rather than falsity — but it makes
the theorem unusable as stated (no finiteness, no `σ > 0`, and no statement that the
hypotheses of `thm:clt` are still in force), and the course's own summary states the
hypothesis explicitly:

> `refs/probability1BG-2.pdf`: «Неравенството на Бери-Есен гласи, че ако $X_1,X_2,\dots$ са i.i.d. сл.в. и $\mu := E[X_1]$, $\sigma := \sqrt{Var(X_1)}$, $\rho := E|X_1-\mu|^3 < \infty$, то, полагайки $Z_n := \dots$, имаме $\sup_x |P(Z_n \le x) - \Phi(x)| \le \rho/(2\sigma^3\sqrt n)$.»

**Verification** (`v3.py` §5) — the inequality as the book writes it is numerically sound for
`X = ±1` (`σ = 1`, `ρ = 1`):
```
 n=  1  sup|P(Z_n<x)-Phi(x)| = 0.3412   bound 0.47/sqrt(n) = 0.4700   ok
 n=  2                        0.2500                        0.3323   ok
 n= 10                        0.1230                        0.1486   ok
 n= 50                        0.0561                        0.0665   ok
```
Also worth recording: the transcript has the lecturer saying «тук участва третия момент.
**Третия централен** момент» [97:00], i.e. without the modulus. The book's `\E[|X_1-\mu|^3]`
is the correct form and the non-absolute version would be false — for the symmetric `X = ±1`
above `E[(X−μ)³] = 0`, so the non-absolute bound would assert `sup|·| ≤ 0`, which the table
refutes. So the book is right to use the modulus; per R1 that silent correction deserves a
footnote rather than nothing. (pesho `page_036` also writes `E|X_1-\mu|^3`, with
`0,4748` — consistent with the book's "около 0,47".)

**Suggested fix:**
> \begin{thm}[Неравенство на Бери\,--\,Есен]
> При условията на теорема~\ref{thm:clt} (в частност $0<\sigma^2<\infty$), ако освен това $\rho := \E|X_1-\mu|^3 < \infty$, то
> \[ \sup_{x \in \mathbb{R}} \left| \mathbb{P}(Z_n < x) - \Phi(x) \right| \le \frac{C\rho}{\sigma^3 \sqrt{n}}, \]
> където $C$ е абсолютна константа ($C \le 0{,}4748$).
> \end{thm}
> …с бележка под линия: в лекцията беше казано «третият централен момент»; неравенството изисква третия \emph{абсолютен} централен момент — за симетрични величини $\E[(X_1-\mu)^3]=0$ и неабсолютният вариант би бил невярен.

---

## 6. UNSOUND (в `supp`) — the local de Moivre–Laplace form is stated for every $k$, with no restriction to the central range

**Location:** `lectures/bodies/lecture_11.tex:239–250` (`supp:moivre-local`)

**What it says now:**
> \[ \mathbb{P}(X_n = k) \ \approx\ \frac{1}{\sqrt{np(1-p)}}\, f_Z\!\left( \frac{k-np}{\sqrt{np(1-p)}} \right), \qquad f_Z(x) = \frac{1}{\sqrt{2\pi}}e^{-x^2/2}. \]

**Why that is wrong.** With no condition on `k`, the approximation is asserted uniformly over
`k = 0,…,n`, and it fails catastrophically in relative terms once `(k−np)/√(np(1−p))` leaves a
bounded range. The classical statement holds uniformly only for `k` with
`x_k = (k−np)/√(np(1−p))` in a bounded set. (The `supp` also inherits finding 2's missing
`p ∈ (0,1)`.)

**Verification** (`v3.py` §4, `n = 100`, `p = 0.5`, `sd = 5`, scipy exact pmf):
```
   k    x=(k-np)/sd    exact P(X=k)      supp approx     ratio approx/exact
  50       0.00          7.959e-02        7.979e-02            1.003
  55       1.00          4.847e-02        4.839e-02            0.998
  60       2.00          1.084e-02        1.080e-02            0.996
  70       4.00          2.317e-05        2.677e-05            1.155
  80       6.00          4.228e-10        1.215e-09            2.874
  90       8.00          1.366e-17        1.010e-15           73.997
 100      10.00          7.889e-31        1.539e-23     19_508_125
```
Off by eight orders of magnitude at `k = n`.

Note for the parent: the course summary (`refs/probability1BG-2.pdf`, Теорема 4.11) writes the
same thing "за $k = 0,1,2,\dots$", so this is inherited, not invented. The fix is one clause,
not a rewrite.

**Suggested fix:** append to the display
> …равномерно по онези $k$, за които $x_k := \frac{k-np}{\sqrt{np(1-p)}}$ остава в ограничен интервал; далеч в опашките (например $k = n$) относителната грешка на това приближение расте неограничено.

---

## 7. BROADENED (invented attribution) — property 6 is named "Теорема на Леви-Крамер"; the lecturer named nothing, and the name belongs to a different theorem

**Location:** `lectures/bodies/lecture_11.tex:174`

**What it says now:**
> \item \textbf{Сходимост (Теорема на Леви-Крамер):} Ако редица от функции на моментите $M_{X_n}(t)$ се схожда поточково към функция на моментите $M_X(t)$ за всички $t \in (-\varepsilon, \varepsilon)$, то … $X_n \xrightarrow{d} X$.

**Why that is a defect.** The mathematical content is correct. The attribution is not, and it
is not sourced:
* the transcript contains **zero** occurrences of "Леви" or "Крамер" (grep over all 3634
  segments); at [42:28]–[43:20] he simply states the property and says «Това е много удобно,
  ще го видим в централната гранична теорема»;
* pesho's `page_033` lists it as unnamed property "д)";
* substantively, the Lévy(–Cramér) continuity theorem is the **characteristic-function**
  statement — which this chapter deliberately puts out of scope in `rem:charfun` at `:177`.
  The moment-generating-function version is due to Curtiss (1942).

This is the B-01 failure mode: the pipeline supplied a confident name the lecturer did not
give, and the name is wrong.

**Suggested fix:** drop the attribution, or footnote it:
> \item \textbf{Сходимост:} Ако редица от функции на моментите $M_{X_n}(t)$ се схожда поточково към функция на моментите $M_X(t)$ за всички $t \in (-\varepsilon,\varepsilon)$, то $X_n \xrightarrow{d} X$.\footnote{Аналогът за характеристични функции е теоремата за непрекъснатост на Леви; вариантът за функции на моментите се приписва на Къртис. В лекцията свойството беше дадено без име.}

---

## 8. LOST — the lecturer's own cross-reference from $M_X$ to the probability generating functions of лекция 6 is dropped

**Location:** `lectures/bodies/lecture_11.tex:168–170` (property 3, independence/product)

**What the lecturer said** at [42:03], immediately after stating the product rule:
> «Ако х е независимо y, то функцията на х плюс y на моментите е функцията на х умножено по функцията на y, нещо което ние добре знаем от … случая на така наречените пораждащи функции.»

**Why that matters.** `lectures/bodies/lecture_06.tex:100–120` proves exactly this property for
the PGF `g_X(s)` ("Важно свойство на пораждащите функции се проявява при суми от независими
случайни величини… Тук независимостта е съществена"), and `frontmatter.tex:76` already lists
`g_X, M_X` side by side in the notation table. The chapter never makes the connection, so the
reader is not told that `M_X(t) = g_X(e^t)` in spirit and that the two transforms share their
whole point. This is content the lecturer gave that is simply absent; it is also the natural
place to say that the MGF is *not* the PGF, which the audit brief asks about.

**Verification.** grep confirms `пораждащ` appears 0 times in `lecture_11.tex` and 14 times in
`lecture_06.tex`; the transcript hit is at segment start 2548 s.

**Suggested fix:** append to `:170`
> Свойството е точният аналог на познатото ни от \crosslecture{...}{пораждащите функции в лекция 6}: и там произведението заменя комбинаторната задача за разпределението на сума, и там независимостта е съществена.

---

## 9. UNCLEAR — "кумулативният ефект при събиране винаги асимптотично клони към нормално разпределение" is false without the standardisation

**Location:** `lectures/bodies/lecture_11.tex:60` (последното изречение на абзаца **Универсалност**)

**What it says now:**
> Веднъж фиксирани ли са те, кумулативният ефект при събиране винаги асимптотично клони към нормално разпределение.

**Why that is wrong as written.** `S_n` itself converges to nothing — it drifts to `±∞` a.s.
whenever `μ ≠ 0`, and even for `μ = 0` its variance `nσ² → ∞`. Only `(S_n − nμ)/(σ√n)`
converges. The sentence as phrased is the standard student misreading of the CLT and the
chapter has just spent a page building the correct normalisation, so it undercuts itself.
The lecturer's own formulation was careful:

> [12:53] «то поведението на SN асимптотично се определя само от μ и сигма и може да се опише с това нормално разпределение.»

He says *"can be described by"*, not *"tends to"*. R3 (never strengthen) applies.

**Suggested fix:**
> Веднъж фиксирани ли са те, асимптотичното поведение на сумата $S_n$ се определя само от $\mu$ и $\sigma$: след центриране с $n\mu$ и нормиране със $\sigma\sqrt n$ границата винаги е стандартното нормално разпределение.

---

# Checked and found sound

1. **The CLT normalisation — the historical bug is fixed and verified.** `:21` gives
   `Z_n = (√n/σ)E_n = (S_n − nμ)/(σ√n)`, matching board_002 and pesho page_035 verbatim.
   Monte Carlo (`v1.py`, 400 000 replicates of `n = 400` draws from the `ex:11-2` density):
   `Var(S_n/√n) = 1.6687` (against `σ² = 5/3 = 1.6667`) and
   `Var(S_n/(σ√n)) = 1.0012`, mean `−0.00012`. The σ in the denominator is genuinely
   required and genuinely present.
2. **`ex:11-2` and its footnote.** sympy: `∫f = 1`, `E[Y] = 0`, `E[Y²] = 5/3`,
   `Var = 5/3`. The footnote's numbers are exactly right, the parenthetical
   «(В лекцията дисперсията беше спомената предположително като единица.)» is the correct
   R1 treatment of [26:34] «мисля, че неговата дисперсия отново е единица», and the
   parenthetical «Без нормиране с σ границата е $N(0,\tfrac53)$» is confirmed by the
   simulation above.
3. **i.i.d. is stated** in `thm:clt` and in §11.1, and independence *is* stated in the
   product property (`:168`) and re-emphasised in the proof (`:213`) — matching the
   lecturer's «Вижте колко е важно, че Y_j са независими» [70:05].
4. **Convergence in distribution at continuity points is handled properly.** `:62–66`
   argues that Φ is continuous on all of ℝ, hence the convergence holds for every `b`
   and for open/half-open/closed intervals alike. This is a faithful and correct rendering
   of [13:40]–[16:10] and of pesho's `C_Z = C_Φ = ℝ`. The strict inequality
   `P(Z_n < b)` at `:63,65` is the book's own convention, not an error.
5. **The MGF may fail to exist — and the book says so.** `rem:charfun` (`:177`) states that
   there are variables with finite mean and variance and no MGF, and gives the
   characteristic function `φ_X(t) = E e^{itX}` with the right reason (`|e^{itX}| = 1`) and
   the right scope disclaimer. This is a faithful recovery of [67:01]–[67:26]. Nothing in
   the chapter conflates `M_X` with `φ_X` or with лекция 6's `g_X` (see finding 8 — the
   problem is the missing link, not a conflation).
6. **Uniqueness carries the neighbourhood-of-0 condition** (`:173`, «за всички $t$ в някаква
   околност на нулата ($|t| < r_0$)»). Correct, and it does *not* repeat the lecturer's
   slip at [43:46] where he stated the converse instead.
7. **`ex:11-3` (uniform):** `M_X(t) = (e^t − 1)/t`, `r_0 = ∞`, with the L'Hôpital/Taylor
   remark at `t = 0`. Correct. **`ex:11-4` (exponential):** `M_X(t) = 1/(1−t)` for `t < 1`,
   divergent for `t ≥ 1`, "съществува сигурно в интервала $(-1,1)$" — correct and matches
   pesho's `X ~ Exp(1) ⟹ a = 1`.
8. **Normal MGF.** sympy: `(1/√(2π))∫ e^{sy}e^{-y²/2} dy = e^{s²/2}`. The
   complete-the-square derivation at `:188–194` and `M_X(t) = e^{μt+σ²t²/2}` via
   `X = μ + σZ` are both correct, and match board_010 and pesho page_033.
9. **Gamma MGF and its moments** (rate parameterisation, per the book's conventions).
   sympy: `∫₀^∞ e^{tx} β^α/Γ(α) x^{α−1}e^{−βx} dx = β^α/(β−t)^α` for `β/t > 1`;
   `M'(0) = α/β`; `M''(0) = α(α+1)/β²`. All three displays at `:289,294,298` are right,
   as is the `t < β` restriction and the `Γ(α,1)`-density identification at `:284`.
10. **The CLT proof.** Every step checks: the rewriting `Z_n = n^{-1/2}ΣY_j`, `E Y_1 = 0`,
    `Var Y_1 = 1`, `M_{Z_n}(t) = (M_{Y_1}(t/√n))^n`, the second-order Taylor expansion,
    and `(1 + (t²/2)/n + o(1/n))^n → e^{t²/2}`. It matches board_011/012 and pesho
    page_036 step for step. The simplifying assumption at `:209` ("добре дефинирана за
    всички $t$") is faithful to [66:35]–[66:52] and to pesho page_033 («ще допуснем, че
    $M_{Y_1}$ е деф. $|t| < \infty$»); board_011 wrote the weaker `|t| < r_0`, and the
    weaker one is all the proof actually needs — worth a one-line footnote if the parent
    wants it, but not a defect.
11. **`supp:lindeberg`.** The Lindeberg condition and conclusion are stated correctly, and
    the closing claim that the i.i.d. case satisfies it automatically is right: with
    `s_n² = nσ²` the quotient becomes `σ^{-2}E[(X_1−μ)²1_{|X_1−μ|>εσ√n}] → 0` by dominated
    convergence. (Needs `σ² > 0` — folded into finding 2.)
12. **The sample-size / Monte-Carlo derivation at `:253–265`.** Every step verified:
    `P(|E_N|>ε) = P(|S_N−Np|/√(Np(1−p)) > ε√N/√(p(1−p)))` is an identity;
    `max p(1−p) = 0.25` at `p = 0.5` (numpy grid); `ε√N/√(p(1−p)) ≥ 2ε√N`; the inclusion
    giving `P(|E_N|>ε) ≤ P(|Z_N| > 2ε√N)`; and the Gaussian tail bound
    `∫_A^∞ e^{-y²/2}dy ≤ e^{-A²/2}/A` (checked at `A = 0.5,1,2,3,5` — holds in all cases).
    The factor 2 at `:263` **corrects** the board, which wrote the one-tail form
    (board_013/014/015: `≈ (1/√(2π))e^{-A²/2}/A`), and the footnote at `:264` says so
    explicitly — the sanctioned R1 mechanism, correctly applied.
    I also ran the recipe end to end (`v4.py`): with `ε = δ = 0.01` it gives `A = 2.615`,
    `N = 17 091`, and the exact binomial `P(|E_N| > 0.01)` is `0.0091` at `p = 0.5`,
    `0.0043` at `p = 0.3` — inside the target `δ = 0.01`. The Berry–Esseen additive slack
    at that `N` is `≈ 0.0036`, i.e. about a third of `δ`, so the `≈` in the derivation is
    quantitatively real but does not invalidate the conclusion, and the book's remark at
    `:267` that the sign "може да бъде строго оценен" is fair.
13. **The moment definitions at `:152–157`** (ordinary / absolute / central / absolute
    central, `k = 2` giving the variance) are all correct and match pesho page_032. In
    particular the book gets right what the lecturer garbled at [37:56], where he called
    `E[(X−μ)^k]` "абсолютен централен момент".
14. **`ex:11-1` (tug of war).** `E X_1 = 0`, `Var X_1 = 1`, `S_n/√n ≈ Z`,
    `P(S_n > 0) ≈ 1/2`, and the remark that `P(S_n = 0) → 0`. Correct, and matches
    board_004 exactly.
15. **No continuity correction** anywhere in the binomial material. The lecturer did not
    give one and neither does the course summary, so its absence is not a fidelity defect —
    though a `supp` on it would be a natural addition if the parent wants one.
