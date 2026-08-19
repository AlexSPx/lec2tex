# Mathematics audit — `lectures/bodies/lecture_10.tex`
*„Видове сходимост. Неравенство на Чебишов и закони за големите числа“*

Witnesses used: `run/lecture_10/audio/transcript.json` (primary), `run/lecture_10/ocr/board_002…023.json`,
`run/pesho/ocr/page_028,029,031,034.json`. All numeric claims below were checked with
`/Users/g8row/Documents/lec2tex/.venv/bin/python3` (numpy/scipy/sympy); the commands and outputs are quoted.

Nine findings. Two are substantive (F1, F2); the rest are dropped hypotheses/caveats and one locally false
sentence. The chapter's core mathematics — the three definitions, both implications, both proofs, Markov,
Chebyshev and its proof, the WLLN proof, and all six applications — is correct.

---

## F1 — The universality sentence of Example 10.1 is false as written
**Severity:** BROADENED (the display is right; the sentence stating what it means is mathematically false)
**Location:** `lectures/bodies/lecture_10.tex:297`, `\begin{example}[Отклонение от десет стандартни отклонения]` (`ex:10-1`)

**What it says now**
> „Това е изключително силен универсален резултат — за \emph{всяка} случайна величина вероятността да
> надвиши 10 пъти стандартното си отклонение никога не надхвърля $1\%$.“

**Why that is wrong.** Three hypotheses are dropped at once: (i) it is the deviation *from the mean*,
$|X-\E X|$, that is bounded, not $X$ itself; (ii) the example's own normalisation $\E X = 0$ (line 293) is
silently discarded by the word „всяка“; (iii) finite variance is not required. Read literally the sentence
claims $\mathbb{P}(X > 10\sqrt{\Var X}) \le 0{,}01$ for every random variable, which fails for any variable
with a large mean.

The lecturer stated all three hypotheses explicitly, twice, in the two sentences the book compressed into
this one:

> **[67:50]** „Т.е. това е абсолютно универсално неравенство, валидно за всички хикс, **които имат 0
> очакване, които имат крайна дисперсия**, и това е оценка за тяхната вероятност да надвишава 10 пъти
> стандартното отклонение и тя никога не може да надвишава една 100, **независимо какви случайни величини
> изберете с 0 среда**.“

So this is a pipeline compression, not the lecturer's imprecision. (Note also the internal tension with
`supp:cheb-vs-normal` at line 301, which correctly calls the bound crude, and with the figure caption at
line 240, which correctly says „за всяка случайна величина **с крайна дисперсия**“.)

**Verification.** `scipy.stats.norm`, $X\sim N(100,1)$, so $\sqrt{\Var X}=1$:
```
N(100,1): P(X > 10*sigma)      = 1.0
N(100,1): P(|X-EX| > 10*sigma) = 0.0
```
The literal reading gives probability $1$, i.e. 100× the claimed bound; the intended reading gives $0$.
I also confirmed the bound is sharp, so it cannot be weakened away: with mass $1/200$ at $\pm 10\sigma$ and
the rest at $0$, sympy gives $\Var X = \sigma^2$ and $\mathbb{P}(|X-\E X| \ge 10\sigma) = 1/100$ exactly.

**Suggested fix**
> Това е изключително силен универсален резултат — за \emph{всяка} случайна величина с крайна дисперсия
> вероятността отклонението от очакването да надвиши 10 пъти стандартното отклонение никога не надхвърля
> $1\%$, независимо от разпределението.

---

## F2 — Both definitions „за редицата е в сила (У)ЗГЧ“ are missing; the LLN is narrowed to the i.i.d. case
**Severity:** LOST (with a NARROWING consequence)
**Location:** `lectures/bodies/lecture_10.tex:316–324` (before `keythm[Слаб ЗГЧ]`) and `:355–360`
(before `keythm[Усилен закон за големите числа]`, `thm:slln`)

**What it says now.** The chapter goes straight from the section heading to the i.i.d. theorem in both cases.
The notion „за редицата е в сила законът за големите числа“ — which is what the two theorems are theorems
*about* — never appears, and neither does the centred form $\frac1n\sum_{i=1}^n (X_i - \E X_i)$.

**Why that is wrong.** The lecturer gave the general definition first, for an arbitrary sequence with finite
expectations (no independence, no identical distribution), and only then specialised:

> **[70:35]** „Тази дефиниция е за слаб закон за големите числа или закон за големите числа. […] Значи, нека
> $X_i$ е редица от случайни величини с очаквания, то ест имат крайни очаквания за всяка една от тези
> случайни величини. Тогава за редицата е в сила законът за големите числа, ако [$\frac1n\sum(X_i-\E X_i)$]
> се схожда **по вероятност към 0**.“
> **[72:09]** „Имате редица от случайни величини с съществуващи очаквания, тогава за тази редица е в сила
> [ЗГЧ], ако от всяка една случайна величина извадите нейното средно, сумирате $n$ на брой от тях и
> разделите на $n$, и това клони по вероятност към 0. **В частния случай, който е важен**, е когато $X_i$
> са независими и еднакво разпределени…“

and again for the strong law:

> **[81:14]** „Нека $X_i$ е редица от случайни величини с очаквания — разбира се, трябва да съществуват, за
> да ги пишем — тогава за редицата е в сила усиленият закон за големите числа, ако
> $\frac1n\sum_{i=1}^n (X_i - \E X_i)$ клони **почти сигурно** [към 0]. […] **[82:21]** Ако $\E X_i = \E X_1$
> за всяко $i$, то (\*) може да се напише като […] клони почти сигурно към очакването на първата, защото
> всичките са равни.“

Both witnesses confirm the board text verbatim:

* `run/lecture_10/ocr/board_020.json` (t = 4974 s ≈ 82:54):
  „**Деф:** (Усилен ЗГЧ) Нека $(X_i)_{i=1}^{\infty}$ е редица от сл. вел. с очаквания
  $(\mathbb{E}X_i)_{i=1}^{\infty}$. Тогава за редицата е в сила УЗГЧ. (\*)
  $\frac{\sum_{i=1}^n (X_i-\mathbb{E}X_i)}{n}\xrightarrow[n\to\infty]{\text{п.с.}}0$. Ако
  $\mathbb{E}X_i=\mathbb{E}X_1\ \forall i\ge 1$, то (\*) може да се напише като …“
* `run/pesho/ocr/page_034.json`: „**Деф1 (ЗГЧ)** Нека $(X_i)_{i=1}^{\infty}$ е редица от сл. вел с очаквания
  $(\mathbb{E}X_i)_{i=1}^{\infty}$. Тогава за редицата е в сила ЗГЧ, ако
  $\frac{\sum_{i=1}^n (X_i-\mathbb{E}X_i)}{n}\xrightarrow[n\to\infty]{\mathbb{P}}0$“

The board also carries the theorems separately (`board_019.json` „Теор1 (ЗГЧ)…“, `board_021.json`
„Теор. (УЗГЧ)…“), and *those* are what the book reproduces — faithfully. What was dropped is the definition
layer above them. The consequence is a genuine narrowing: in the book the LLN exists only as a property of
i.i.d. sequences, whereas the lecturer defined it for any sequence with finite means and the i.i.d. theorem
is one instance. This also removes the only place where the centred form $\sum(X_i-\E X_i)/n$ is explained —
yet the WLLN proof (lines 334–338) uses exactly that form without ever having introduced it, and the
statement's own note at line 323 is a fragment of the specialisation argument of [73:00]–[73:38].

**Verification.** Textual, against three independent witnesses (transcript, board OCR, student notes), quoted
above. No numeric claim is at issue.

**Suggested fix.** Insert before each theorem the definition the lecturer gave, e.g. for §Слаб ЗГЧ:

> \begin{defn}[Закон за големите числа за редица]
> Нека $(X_i)_{i=1}^\infty$ е редица от случайни величини с крайни очаквания $(\E X_i)_{i=1}^\infty$.
> Казваме, че за редицата е в сила \emph{законът за големите числа}, ако
> \[ \frac{\sum_{i=1}^n (X_i - \E X_i)}{n} \xrightarrow[n \to \infty]{\mathbb{P}} 0 . \]
> Ако освен това $\E X_i = \E X_1$ за всяко $i \ge 1$ (например когато величините са еднакво разпределени),
> то условието се записва в по-обичайния вид $\frac{1}{n}\sum_{i=1}^n X_i \xrightarrow{\mathbb{P}} \E X_1$.
> \end{defn}

and symmetrically for §Усилен ЗГЧ with $\xrightarrow{\text{п.с.}}$ and „усиленият закон“. Note that
independence is *not* part of the definition — it enters only in the theorem.

---

## F3 — „винаги можем да намерим естествено $r$, такова че $\frac{1}{r+1} < \varepsilon \le \frac{1}{r}$“ is false
**Severity:** WRONG (locally false; the conclusion of the remark survives, the justification does not)
**Location:** `lectures/bodies/lecture_10.tex:67` (Забележка after the definition of convergence in probability)

**What it says now**
> „Ако $\varepsilon$ е произволно реално число, винаги можем да намерим естествено $r$, такова че
> $\frac{1}{r+1} < \varepsilon \le \frac{1}{r}$.“

**Why that is wrong.** $\frac1r \le 1$ for every $r \in \mathbb{N}$, so no such $r$ exists for any
$\varepsilon > 1$. The reduction itself is still fine (for $\varepsilon > 1$ take $r = 1$ and use
$A_{n,\varepsilon} \subseteq A_{n,1}$), but the sentence asserts a false statement about all real
$\varepsilon$. The lecturer avoided this by stating the *general monotonicity*, which covers every
$\varepsilon$ at once — and that sentence is exactly what the pipeline dropped:

> **[8:57]** „Най-общо, имате, че ако епсилон е по-голямо от делта, то $A_{n,\delta}$ съдържа в себе си
> $A_{n,\varepsilon}$.“

`run/pesho/ocr/page_029.json` records the same as a displayed line: „$\varepsilon > \delta$ то
$A_{n,\varepsilon} \subseteq A_{n,\delta}$“.

**Verification.** Brute-force search over $r = 1 \dots 10^6$:
```
eps=0.3: r found -> [3]
eps=1.0: r found -> [1]
eps=1.5: r found -> NONE (claim fails)
eps=2.0: r found -> NONE (claim fails)
eps=7.0: r found -> NONE (claim fails)
```

**Suggested fix**
> \emph{Забележка:} В горната дефиниция е напълно достатъчно да се разглеждат само $\varepsilon$ от вида
> $\frac{1}{r}$ за естествено $r \ge 1$. Причината е монотонността на събитията: ако
> $\varepsilon > \delta > 0$, то $A_{n,\varepsilon} \subseteq A_{n,\delta}$, тъй като условието
> $|X_n - X| > \varepsilon$ влече $|X_n - X| > \delta$. Затова за произволно $\varepsilon > 0$ избираме
> естествено $r$ с $\frac{1}{r} \le \varepsilon$ и получаваме
> $\mathbb{P}(A_{n,\varepsilon}) \le \mathbb{P}(A_{n,1/r}) \to 0$. Работата с изброимо количество стойности
> на $\varepsilon$ е много полезна в теоретичните доказателства.

---

## F4 — The relation between the two laws is never stated: strong ⇒ weak, not conversely, and the weak law is superfluous here
**Severity:** LOST
**Location:** `lectures/bodies/lecture_10.tex:357` (the two-sentence bridge) and `:360–365` (`thm:slln`)

**What it says now**
> „Слабият закон гарантира сходимост само по вероятност. Усиленият закон утвърждава много по-силен
> резултат — сходимост почти сигурно.“

and inside `thm:slln`: „Това е най-полезният и често срещан вид на закона, тъй като в повечето практически
задачи […] работим с независими наблюдения от един и същи феномен.“

**Why that is wrong.** The book states *identical* hypotheses for both laws (i.i.d., $\E|X_1| < \infty$) and
then never draws the conclusion the lecturer drew twice from that coincidence. Two distinct pieces of content
are absent:

> **[82:08]** „Т.е. ако е вярно този закон [усиленият], той е верен и слабият закон, или просто законът за
> големите числа. Но ако е верен законът за големите числа, не е ясно дали е верен усиленият закон за
> големите числа.“
> **[85:39]** „Този закон за големите числа всъщност е по-използван, защото ако имате крайно очакване на
> модул $X_1$ […] този закон е винаги верен. Така че слабият закон в някакъв смисъл е **излишен или
> суперфлуус**, защото този винаги е верен в контекста, в който ние ще разглеждаме. А той е много по-силен,
> защото имате сходимост почти сигурно, а не сходимост по вероятност.“

The first is the *implication between the two laws as properties of a sequence* (which follows from Theorem
а) at line 90 applied to $\frac1n\sum(X_i-\E X_i)$) together with the non-implication. The second is the
observation that under the course's hypotheses the weak law adds nothing — a scope remark, exactly the class
of content the pipeline drops. Note the reason the book cannot state the first cleanly is F2: without the
definition „за редицата е в сила (У)ЗГЧ“ there is no object to which „strong ⇒ weak“ applies.

**Verification.** Textual; the deduction „strong ⇒ weak“ is Theorem а) of this same chapter, so nothing new is
asserted. No numeric claim.

**Suggested fix.** Replace the bridge at line 357 with:

> Слабият закон гарантира сходимост само по вероятност. Усиленият закон утвърждава много по-силен резултат —
> сходимост почти сигурно. По теорема~[а)] усиленият закон влече слабия: ако
> $\frac1n\sum_{i=1}^n (X_i - \E X_i) \to 0$ почти сигурно, то същото е вярно и по вероятност. Обратното не
> е вярно в общия случай — възможно е за една редица да е в сила законът за големите числа, без да е в сила
> усиленият. При условията, при които ще работим ($X_i$ независими и еднакво разпределени с
> $\E|X_1| < \infty$), усиленият закон е винаги верен, така че слабият закон в този контекст е излишен;
> той обаче се доказва елементарно и затова го разглеждаме първо.

---

## F5 — The Borel–Cantelli example uses independence in part б) without carrying the hypothesis
**Severity:** UNSOUND (the conclusion fails for a dependent sequence with the same marginals)
**Location:** `lectures/bodies/lecture_10.tex:43–47`, inside `\begin{supp}[Лема на Борел–Кантели]`
(`supp:borel-cantelli`)

**What it says now**
> „Ако вместо това вземем $X_n \sim \Ber(1/n)$, редът $\sum_n 1/n$ е разходящ и по част б) единиците се
> появяват безброй много пъти — тогава $X_n \to 0$ по вероятност, но \emph{не} почти сигурно. Двата примера
> се различават само по скоростта, с която вероятностите клонят към нула, и точно това разграничава двата
> вида сходимост.“

**Why that is wrong.** The independence assumption is stated only for the *first* example („Нека
$X_n \sim \Ber(1/n^2)$ са независими“, line 40) and is left to be inferred for the second by „вместо това“.
But independence is load-bearing exactly here: part а) needs no independence, part б) does, and without it
the conclusion is false. Concrete failing case: let $U \sim U(0,1)$ and $X_n = \ind_{\{U < 1/n\}}$. Then
$X_n \sim \Ber(1/n)$ for every $n$, the series $\sum 1/n$ still diverges, yet for every $\omega$ with
$U(\omega) > 0$ we have $X_n(\omega) = 0$ for all $n > 1/U(\omega)$ — so $X_n \to 0$ **почти сигурно**,
contradicting the sentence as an inference from the marginals.

The closing sentence („различават само по скоростта … и точно това разграничава“) is therefore also
overstated: the two examples differ in the rate *and* rely on independence for the divergent half.

Since this is a `supp`, absence from the transcript is not a defect (the lecturer did promise such an
example at **[5:12]** „Ако имаме време, ще ви дам пример, при който ще имаме множество с мярка 0, но все пак
не празното множество“, but never delivered it). The mathematics, however, must hold.

**Verification.** numpy, 20 000 indices, comparing the dependent construction with an independent one:
```
dependent X_n = 1{U < 1/n}:  fraction of paths with any 1 after n=1000: 0.00104
independent Ber(1/n):        mean #ones in n in (1000,20000] per path: 3.044
independent Ber(1/n):        fraction of paths with a 1 after n=1000:  0.9515
```
The dependent paths stop producing ones (the residual 0.1 % are the paths with $U < 1/1000$, which stop
later); the independent ones keep producing them, as Borel–Cantelli б) requires. Both have identical
marginals and both converge to $0$ in probability, since $\mathbb{P}(X_n = 1) = 1/n \to 0$ in either case.

**Suggested fix**
> Ако вместо това вземем независими $X_n \sim \Ber(1/n)$, редът $\sum_n 1/n$ е разходящ и по част б)
> единиците се появяват безброй много пъти — тогава $X_n \to 0$ по вероятност, но \emph{не} почти сигурно.
> Тук независимостта е съществена: за зависимата редица $X_n = \ind_{\{U < 1/n\}}$ с $U \sim U(0,1)$ имаме
> същите маргинални разпределения, но $X_n \to 0$ почти сигурно. Двата примера се различават по скоростта,
> с която вероятностите клонят към нула, и точно тя (при независимост) разграничава двата вида сходимост.

---

## F6 — The moment inequality drops the existence caveat the lecturer gave, and is applied outside its own cited hypothesis
**Severity:** LOST (with an internal inconsistency)
**Location:** `lectures/bodies/lecture_10.tex:285–289` (§Следствия и пример), against
`prop:markov` at `:213–216`

**What it says now**
> „Аналогично неравенство за произволни моменти $m \ge 1$ се получава, като приложим
> твърдение~\ref{prop:markov} към $Y = |X - \E X|^m$ и прага $a^m$ […]:
> $\mathbb{P}(|X - \E X| > a) \le \frac{\E[|X - \E X|^m]}{a^m}$.“

**Why that is wrong.** The book's own Markov proposition assumes „$Y \ge 0$ … **с крайно очакване**“, so the
substitution requires $\E|X-\E X|^m < \infty$, which is never mentioned. The lecturer stated precisely this
caveat, and also explained why it is harmless:

> **[65:02]** „И това е вярно за всяко $m$, по-голямо или равно на 1, **стига това очакване да съществува**.
> Дори да не съществува, това ще е безкрайност, но оценката ще е безсмислена.“

So the inequality is not *false* without the condition (the right-hand side is $+\infty$), but the book
neither states the condition nor gives the lecturer's reason for not needing it — while simultaneously citing
a proposition that demands it. `run/pesho/ocr/page_034.json` records the second form the lecturer wrote and
the book folded away: „$\mathbb{P}(|X|>a) \le \frac{\mathbb{E}|X|^n}{a^n}, \forall n \ge 1$“ under
$\mathbb{E}X = 0$.

The parenthetical „(названието Марков или Чебишов тук не се фиксира…)“ correctly recovers **[65:20]** „Дали
ще го кръстите Марков или Чебишов, те са с един и същи тип на доказателство“.

**Verification.** Logical, against the book's own line 215. No numeric claim.

**Suggested fix**
> Аналогично неравенство за произволни моменти $m \ge 1$ се получава, като приложим
> твърдение~\ref{prop:markov} към $Y = |X - \E X|^m \ge 0$ и към прага $a^m$ […]. Оценката е в сила при
> условие, че моментът $\E[|X - \E X|^m]$ съществува; ако той е безкраен, неравенството остава формално
> вярно, но е безсмислено.

---

## F7 — The worked Bernoulli computation of $C_{F_X}$ and the alternative notation for $\xrightarrow{d}$ are gone
**Severity:** LOST
**Location:** `lectures/bodies/lecture_10.tex:73` and `:75–82`

**What it says now.** One sentence: „Ако обаче $X$ има скокове (дискретна случайна величина, напр. на
Бернули), $C_{F_X}$ е цялата реална права без точките на скок.“

**Why that is wrong.** The lecturer deliberately moved the example *before* the definition and spent
**[11:03]–[13:41]** (about two and a half minutes of board work) computing it, because it is the only place in
the chapter where the reader sees why the definition must exclude the jump points:

> **[11:17]** „Айде директно да ви дам примера преди дефиницията, за да не се объркат […] да си вземем
> най-простия случай, в който $X$ е $\Ber(1/2)$. Каква е функцията на разпределение? Тя е 0 […] когато $x$ е
> по-малко или равно на 0. След това е $1/2$ […] и след това става единица. […] **[12:12]** Значи $C_{F_X}$
> е $\mathbb{R}$ без 2 точки, 0 и 1.“
> **[12:45]** „$x$ принадлежи на $C_{F_X}$ тогава и само тогава, когато вероятността да видите $X$ [равно на
> $x$] е по-голяма от 0.“ [Note: the ASR drops the negation; the criterion he wrote and the book records at
> line 73 is the correct one.]

Also absent is the alternative notation he gave right after the definition:

> **[16:22]** „И само ще кажа, че се записва алтернативно, често пъти, като [$\mathbb{P}(X_n < x) \to
> \mathbb{P}(X < x)$], като се игнорира, че вероятностните пространства може да са различни.“

`run/pesho/ocr/page_029.json` records both — the Bernoulli remark („за НСВ $C_{F_X} = \mathbb{R}$“) and, as a
parenthesis under the definition, „(Може да се запише $\mathbb{P}(X_n < x) \xrightarrow[n\to\infty]{}
\mathbb{P}(X < x)$)“. That parenthesis is also what makes the strict-inequality convention visible at the one
point in the book where it matters most.

**Verification.** With $X \sim \Ber(1/2)$ and the book's convention $F_X(x) = \mathbb{P}(X < x)$:
$F_X(x) = 0$ for $x \le 0$, $= 1/2$ for $0 < x \le 1$, $= 1$ for $x > 1$; jumps exactly at $\{0,1\}$, which
are exactly the atoms. Consistent with line 73 and with the convention in `docs/REMEDIATION.md`.

**Suggested fix.** Restore the example ahead of the definition, e.g.:

> Например нека $X \sim \Ber(1/2)$. При нашата конвенция $F_X(x) = 0$ за $x \le 0$, $F_X(x) = \frac12$ за
> $0 < x \le 1$ и $F_X(x) = 1$ за $x > 1$. Точките на скок са $0$ и $1$ — точно двете стойности с
> положителна вероятност — тоест $C_{F_X} = \mathbb{R} \setminus \{0, 1\}$.

and add after the definition: „Условието се записва още и като $\mathbb{P}(X_n < x) \to \mathbb{P}(X < x)$ за
$x \in C_{F_X}$, при което различните вероятностни пространства остават премълчани.“

---

## F8 — The sandwich example draws a conclusion the LLN alone cannot support
**Severity:** BROADENED (mild)
**Location:** `lectures/bodies/lecture_10.tex:378`, `\begin{example}[Проверка на грамаж]` (`ex:10-3`)

**What it says now**
> „Ако измерим средно 46 грама при достатъчно голямо $n$, по силата на ЗГЧ имаме сериозни основания да се
> усъмним, че истинското очакване е 50 грама.“

**Why that is wrong.** The LLN is a purely asymptotic statement: it says the average converges, not how far
$46$ is from $50$ for a given $n$. Deciding whether the observed gap is significant is precisely what the LLN
does *not* give, and the lecturer said so at length, ending the example on that caveat:

> **[92:22]** „Просто вие ще видите, че средният грамаж тук би било, да кажем, 46 […] а вече дали вие трябва
> да сте близко до истинското средно или не, вече това трябва да определите с някой допълнителен резултат,
> защото тук ви казва, че на безкрайност се приближавате към очакването. А кога? Колко бързо трябва да сте
> близо до тази истинска вероятност и очакването на $X_1$, това нещо ще ни даде отговор централната гранична
> теорема.“
> **[93:57]** „…имате предостатъчно на брой опити, основание да се усъмните, че обявеният грамаж е верен.
> Така се работи с вакцините, но там не става с трима пациенти, защото нямате достатъчно брой опити, за да
> сте сигурни, че сте близки до истинската вероятност.“

The book keeps the punchline („сериозни основания да се усъмним“) and drops the qualification that makes it
legitimate. The same CLT pointer *is* retained in `ex:10-6` (line 402) and in `ex:10-5`, so the loss is local
to this example.

**Verification.** Logical/structural; no numeric claim is made by the book here.

**Suggested fix.** Append to the example:
> Самият закон за големите числа обаче не казва \emph{колко} наблюдения са „достатъчно“ и колко голяма
> разлика е значима — той е граничен резултат. На този въпрос отговаря централната гранична теорема, която
> ще разгледаме по-нататък.

---

## F9 — „съществува точно едно $k$“ is false at the endpoints of the closed intervals
**Severity:** UNCLEAR (correct conclusion, literally false intermediate claim; smallest finding in the list)
**Location:** `lectures/bodies/lecture_10.tex:103` and `:112–114`,
`\begin{example}[По вероятност, но не почти сигурно]` (`ex:10-typewriter`)

**What it says now**
> $\xi_{n,k} = \ind_{\left[\frac{k-1}{n},\, \frac{k}{n}\right]}$ … „за всяко фиксирано $\omega \in [0,1]$ и за
> всяко $n$ съществува точно едно $k$, за което $\omega$ попада в съответния интервал“

**Why that is wrong.** The intervals are written closed, so they overlap at their endpoints: for $\omega = 1/2$
and $n = 2$ both $k = 1$ ($[0, 1/2]$) and $k = 2$ ($[1/2, 1]$) contain $\omega$. „Точно едно“ holds for
almost every $\omega$, not for every $\omega$. The conclusion („не се схожда за нито едно $\omega$“) is
unaffected — the sequence still takes the value $1$ infinitely often and $0$ infinitely often — so this is a
wording-level unsoundness, not a broken example. This example is editorial (not in the transcript), so only
its mathematics is at issue.

**Verification.** Direct enumeration over $n \le 60$ for several $\omega$, counting the last 200 terms of the
flattened sequence:
```
omega=0.0     ones=3 zeros=197
omega=0.13    ones=3 zeros=197
omega=0.5     ones=4 zeros=196
omega=1/3     ones=4 zeros=196
omega=1.0     ones=4 zeros=196
```
Both values recur for every $\omega$ tested (so the example's conclusion is confirmed), and the counts for
$\omega \in \{0.5, 1/3, 1.0\}$ exceed those for generic $\omega$ precisely because those points lie in two
intervals for infinitely many $n$ — which is the failure of „точно едно“.

**Suggested fix.** Either use half-open intervals,
$\xi_{n,k} = \ind_{\left[\frac{k-1}{n},\, \frac{k}{n}\right)}$ (with the last one closed), or write „поне
едно $k$“ / „точно едно $k$ за почти всяко $\omega$“.

---

# Checked and found sound

Everything below I checked against the transcript, the board OCR and (where applicable) numerically, and
found correct. This is the bulk of the chapter.

**The three definitions.**
* *Почти сигурно* (line 15) — defined before any use, via $L_X = \{\omega : \lim X_n(\omega) = X(\omega)\}$
  and $\mathbb{P}(L_X) = 1$; matches **[4:21]–[5:53]** and `page_028.json`. The gloss at line 22 (the
  exception set may be non-empty but has measure 0) is exactly **[5:12]**–**[5:34]**.
* *По вероятност* (line 58) — $\forall \varepsilon > 0: \mathbb{P}(|X_n - X| > \varepsilon) \to 0$, with the
  strict $>$ inside, matching **[6:15]**–**[7:42]** and `page_029.json`. The remark that the probability need
  not decrease monotonically (line 65) is **[8:12]**.
* *По разпределение* (line 75) — stated **at continuity points of the limit** $F_X$, and correctly on
  *different* spaces $(\Omega_n, \mathcal{A}_n, \mathbb{P}_n)$ for each $n$. Verbatim match with
  `board_002.json` and `page_029.json`; the „$C_{F_X}$“ machinery at line 73 and the atom criterion
  („точките на скок са точно тези $x$, за които $\mathbb{P}(X=x)>0$“) are correct under the book's
  $F_X(x) = \mathbb{P}(X < x)$ convention. The common-space requirement is correctly restricted to the first
  two modes (line 5, line 71), as at **[2:30]**–**[2:56]** and **[9:42]**–**[10:13]**.
* Line 5 correctly hedges that other modes exist („Съществуват и други видове“), matching **[2:06]** — so no
  mean-square claim is made and none is needed.

**Directions of the implications and the non-implications.**
* Theorem (line 88): а) п.с. $\Rightarrow$ по вероятност; б) по вероятност $\Rightarrow$ по разпределение.
  Both directions correct, matching `page_029.json` „Теор 1“ and **[19:37]**–**[20:29]**. The ordering claim
  at line 95 („най-силната … почти сигурно … най-слабата … по разпределение“) is correct.
* Line 97 correctly says the converses fail *in general* („по принцип“), matching **[19:52]** and
  **[20:48]**–**[21:15]**; nowhere does the chapter claim that $\xrightarrow{d}$ implies anything stronger.
* The only stated converse (`prop` at line 203) is correctly limited to a **constant** limit, with the
  common-space caveat the lecturer flagged at **[38:04]**–**[38:25]**. Its proof idea is correct: with
  $F_c(x) = 0$ for $x \le c$ and $1$ for $x > c$ under this convention, $c$ is the only discontinuity, and
  $\mathbb{P}(|X_n - c| > \varepsilon) = \mathbb{P}(X_n > c+\varepsilon) + \mathbb{P}(X_n < c-\varepsilon)$
  is a disjoint decomposition whose two terms are dominated by $1 - F_{X_n}(c+\varepsilon) \to 0$ and
  $F_{X_n}(c-\varepsilon) \to 0$. Matches **[38:58]**–**[41:27]** and `page_031.json`.
* Counterexample `ex:10-samedist` is correct: for i.i.d. $N(0,1)$, $\xi_n - \xi \sim N(0,2)$, so
  $\mathbb{P}(|\xi_n - \xi| > \varepsilon)$ is a constant $> 0$. Simulated with $2\times10^5$ draws at
  $\varepsilon = 1$: empirical $0.4783 / 0.4817 / 0.4779$ for $n = 1, 5, 50$ against the exact
  $2(1-\Phi(1/\sqrt2)) = 0.4795$ — constant in $n$, as claimed.
* Counterexample `ex:10-typewriter` is correct apart from F9: $\mathbb{P}(\xi_{n,k} > \varepsilon) = 1/n \to 0$
  and the sequence diverges at every $\omega$ (enumeration above).

**Proof of а) (lines 132–160).** The decomposition
$L_X = \bigcap_r \bigcup_n \bigcap_{k \ge n} A^c_{k,1/r}$ with
$A^c_{k,1/r} = \{|X_k - X| \le 1/r\}$, the De Morgan step to
$L_X^c = \bigcup_r B_r$, the deduction $\mathbb{P}(B_r) = 0\ \forall r$ from
$0 = \mathbb{P}(\bigcup_r B_r) \ge \mathbb{P}(B_\ell)$, the monotone decrease
$C_{n,r} \supseteq C_{n+1,r}$, continuity from above, and the final squeeze
$C_{n,r} \supseteq A_{n,1/r}$ are all correct and reproduce `board_004.json` and `page_029.json`
line-for-line, including the $\varepsilon = 1/r$ restriction justified by the (repaired) remark of F3.

**Proof of б) (lines 162–198).** Both inclusions are correct:
$\{X_n < x\} \subseteq \{X < x+\varepsilon\} \cup A_{n,\varepsilon}$ (on $A^c$, $X \le X_n + \varepsilon <
x + \varepsilon$) and $\{X < x-\varepsilon\} \cap A^c_{n,\varepsilon} \subseteq \{X_n < x\}$ (on $A^c$,
$X_n \le X + \varepsilon < x$). The sandwich
$F_X(x-\varepsilon) - \mathbb{P}(A_{n,\varepsilon}) \le F_{X_n}(x) \le F_X(x+\varepsilon) +
\mathbb{P}(A_{n,\varepsilon})$ follows correctly (the lower bound via
$\mathbb{P}(B \cap A^c) \ge \mathbb{P}(B) - \mathbb{P}(A)$), and the $\liminf/\limsup$ step plus
$\varepsilon \downarrow 0$ at a continuity point is exactly right — with the book's convention $F_X$ is
left-continuous, so the left end converges to $F_X(x)$ unconditionally and only the right end needs
continuity, which is where the hypothesis $x \in C_{F_X}$ is spent. Matches **[32:37]**–**[36:32]** and
`page_031.json`.

**Markov (`prop:markov`, lines 213–224).** Correctly requires $Y \ge 0$; conclusion
$\mathbb{P}(Y > a) \le \E Y/a$ for all $a > 0$ with strict $>$ on the left, consistent with the Chebyshev
convention of the chapter and with `formulas.tex:258`. The pointwise bound $Y \ge a\,\ind_{\{Y>a\}}$ and
monotonicity of $\E$ are correctly applied. The stated „с крайно очакване“ is a harmless strengthening of the
hypothesis (the inequality is vacuous otherwise); the derivation of Chebyshev from it at line 226 is correct,
since $\{(X-\E X)^2 > a^2\} = \{|X - \E X| > a\}$.

**Chebyshev (`keythm`, lines 230–235) and its proof (262–282).** Statement matches the board verbatim across
13 OCR'd frames (`board_006`…`board_018`): „Нека $X$ е сл. вел. с дисперсия $\mathbb{D}X$. Тогава
$\mathbb{P}(|X-\mathbb{E}X|>a) \le \frac{\mathbb{D}X}{a^2}\ \forall a>0$“, including the strict $>$ (the
`≥`-vs-`>` question is the already-rejected item in `docs/REMEDIATION.md` §8 and is not re-raised). The proof
— $Y = X - \E X$, $\Var X = \Var Y = \E Y^2$, splitting $1 = \ind_{\{|Y| \le a\}} + \ind_{\{|Y| > a\}}$,
discarding the non-negative first term, replacing $Y^2$ by $a^2$ on $\{|Y| > a\}$ — is correct and follows
**[61:04]**–**[63:27]** and `page_034.json` step for step. The display of `ex:10-1` (line 295) is correct;
only its prose gloss is F1.

**`supp:cheb-vs-normal` (lines 301–310).** Both numbers verified: Chebyshev at $a = 2\sqrt{\Var X}$ gives
$\mathbb{P}(|X - \E X| \le 2\sqrt{\Var X}) \ge 1 - 1/4 = 0{,}75$; and
`2*norm.cdf(2)-1 = 0.9544997361036416`, i.e. $\approx 0{,}9545$ as printed.

**WLLN (`keythm[Слаб ЗГЧ]`, lines 318–324) and its proof (326–353).** Hypotheses match `board_019.json`
exactly: „редица от нез. и еднакво разпр. сл. вел. с $\mathbb{E}X_1$ и $\mathbb{E}|X_1|<\infty$“, conclusion
$\frac1n\sum X_i \xrightarrow{\mathbb{P}} \E X_1$. Correct as stated (Khinchin). The proof **declares** its
extra hypothesis in its own heading and first line („в случая, когато дисперсията съществува … при
допълнителното по-силно условие, че $\Var X_1 < \infty$“), which is exactly what the lecturer did at
**[75:30]** („Ние ще докажем […] случая, когато не само очакването съществува, но и дисперсията е крайна, за
да може да използваме неравенството на Чебишов“) and what the board records („Д-во: Ще докажем когато
$DX_1<\infty$“). So there is **no** hypothesis-laundering here: the proof does not silently use more than the
statement grants; it announces the restriction. Every step checks out — the centring, the multiplication by
$n$, Chebyshev with $a = \varepsilon n$ applied to $Y = \sum(X_i - \E X_i)$ (which has mean $0$), the
variance-of-a-sum step flagged as the place where independence is used (line 344, matching **[78:16]** „тук се
използва ключово независимост“), the equal-variances step from identical distribution, and the final
$\Var X_1/(n\varepsilon^2) \to 0$. Worth recording explicitly, since it was the main thing to look for: the
proof needs only *uncorrelatedness* and *equal variances*, i.e. strictly less than the i.i.d. hypothesis
assumed — it is weaker than the statement, never stronger.

**SLLN (`thm:slln`, lines 359–365).** Hypotheses match `board_021.json` („независими и еднакво разпределени
сл. вел., такива че $\mathbb{E}|X_1| < \infty$“); conclusion is a.s. convergence to $\E X_1$. Correct
(Kolmogorov), and correctly left unproved, as at **[85:30]**. The cross-reference from
`lectures/bodies/lecture_11.tex:9` to `thm:slln` is consistent, as is `formulas.tex:260–261`.

**All six applications.**
* `ex:10-2` (Bernoulli / voting / vaccines) — $\frac1n\sum X_i \to p = \E X_1$ a.s.; matches
  `board_022.json` and **[86:25]**–**[89:29]**. Attribution to the *strong* law is what the lecturer said.
* `ex:10-3` (ham) — see F8; the arithmetic and the setup are right.
* `ex:10-4` (roulette) — $\E X_1 = \frac{18}{37} - \frac{19}{37} = -\frac{1}{37}$, verified against
  `board_023.json`, which has the same value and the same a.s. limit.
* `ex:10-5` (tug-of-war) — the whole point of the example is correct and is the lecturer's own warning at
  **[98:42]**–**[99:54]**: $S_n/n \to 0$ but $\mathbb{P}(S_n > 0) \to 1/2$, **not** $0$. Verified exactly with
  `scipy.stats.binom.sf(n/2, n, 0.5)`: $0.376953\ (n{=}10)$, $0.460205\ (n{=}10^2)$, $0.487387\ (n{=}10^3)$,
  $0.496011\ (n{=}10^4)$, $0.500000\ (n{=}100001)$ — converging to $1/2$ while $\E[S_n/n] = 0$.
* `ex:10-6` (Monte Carlo) — $Y_i \sim \Ber(|A|)$ because the unit cube has volume 1 (with the lecturer's
  „ако беше с друг обем, щяхме да разделим на обема“ correctly kept as a parenthesis), a.s. convergence to
  $|A|$, and the correct forward pointer to the CLT for the rate. Matches **[100:41]**–**[103:41]**.

**Exercises (lines 407–415).** All four correspond to things the lecturer actually assigned:
$\varepsilon = 1/r$ at **[8:57]**, finishing б) at **[36:19]**, finishing the constant-limit converse at
**[41:37]**, and the $10\sigma$ bound at **[67:08]** („Ето ви задача, която ако се опитате, може бързо да
решите“). Exercise 4 correctly states the hypotheses ($\E X = 0$, $\Var X < \infty$) that F1's prose drops.

---

## Summary

The chapter is in good shape mathematically. One sentence is false as written (F1) and one is false for
$\varepsilon > 1$ (F3); one `supp` needs an independence hypothesis carried over (F5). The most consequential
finding is not an error but an omission: the lecturer's *definition* of what it means for a sequence to
satisfy the (strong) law of large numbers — written on the board as „Деф“, recorded by the student, and stated
for arbitrary sequences with finite means — is absent from the book, which therefore presents the LLN as an
i.i.d.-only phenomenon (F2) and cannot state how the two laws relate (F4). Notably, the one place where a
hypothesis-laundering defect would have been most damaging — the weak law's proof using more than the
statement grants — is clean: the extra hypothesis $\Var X_1 < \infty$ is declared in the proof heading, and
the proof in fact uses less than the i.i.d. hypothesis it is given.
