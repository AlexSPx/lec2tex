# Mathematics audit — `lectures/bodies/lecture_07.tex`
### "Теорема на Поасон. Хипергеометрично разпределение, ковариация и корелация"

Witnesses used: `run/lecture_07/audio/transcript.json` (1576 segs, 107.7 min),
`run/lecture_07/ocr/board_001…026.json`, `run/pesho/ocr/page_015…017.json`,
`lectures/bodies/frontmatter.tex` (notation table). All numeric checks run with
`/Users/g8row/Documents/lec2tex/.venv/bin/python3` (scipy/numpy).

---

## 1. WRONG — `\widetilde{X}` is given two incompatible meanings, making the book assert `Cov = ρ`

**Location:** `lectures/bodies/lecture_07.tex:360` and `:365` versus `:415–421`
(definition of ковариация and definition of коефициент на корелация).

**What it says now**

Line 360–365 (covariance section):
> "Ако дефинираме центрирани случайни величини $\widetilde{X} = X - \E X$ и
> $\widetilde{Y} = Y - \E Y$ …
> $\Cov(X, Y) = \E[(X - \E X)(Y - \E Y)] = \E[\widetilde{X}\widetilde{Y}]$"

Line 415–421 (correlation section):
> "Ако дефинираме центрираните и нормирани случайни величини като:
> $\widetilde{X} = \frac{X - \E X}{\sqrt{\Var X}}, \quad \widetilde{Y} = \frac{Y - \E Y}{\sqrt{\Var Y}}$ …
> $\rho(X, Y) = \E[\widetilde{X}\widetilde{Y}]$"

**Why that is wrong.** The same symbol is *defined twice, differently*, in the same
chapter, and both definitions are then used in displayed identities whose left-hand
sides differ. Read literally the book states
$\Cov(X,Y) = \E[\widetilde X\widetilde Y] = \rho(X,Y)$, which is false whenever
$\Var X\,\Var Y \neq 1$. The collision is not cosmetic: the proof of
`thm:corr-bounds` (`:485–491`) and both halves of the linear-dependence proof
(`:505–530`) all silently rely on the *normalised* reading ($\E\widetilde X^2 = 1$),
while `:365` relies on the *centred* reading, and `prop:var-sum`'s proof (`:389`)
introduces a third spelling `\tilde X = X - \E X` for the centred one — visually
identical to `\widetilde X`.

It also contradicts the book's own declared convention: `frontmatter.tex:83` states
> `$\widetilde{X}$ & центрирана и нормирана $X$`

so `:360` breaks the notation table.

The lecturer kept the two apart with two different accents, and so did the board and
the independent student notes:

* transcript **[69:03]** — «ако ви запишете **х вълна** да ви е х минус очакването на х
  и **у вълна** да ви е у минус очакването на у, то вашата ковариация на х и у е
  всъщност очакването на х вълна по у вълна» → tilde = *centred only*;
* transcript **[79:09]** — «Това се нарича **центрирана и нормирана** ХИКС», written
  on the board as $\overline{X}$: `run/lecture_07/ocr/board_019.json` has
  `\rho(X,Y) \overset{т.}{=} \mathbb{E}\overline{X}\,\overline{Y}` and
  `0 \le \mathbb{E}(\overline{X} \pm \overline{Y})^2`, while
  `board_017.json` has `\widetilde{X} = X - \mathbb{E}X` for the centred one;
* `run/pesho/ocr/page_017.json` likewise uses $\overline{X},\overline{Y}$ throughout
  the $|\rho|=1$ proof.

So the pipeline flattened a deliberate two-accent distinction onto one symbol.

**Verification.** `X = Y ~ Ber(1/2)`: computed $\Cov = 0.25$ but $\rho = 1.0$
(script: exact pmf sums, output `Cov = 0.25  rho = 1.0`). Both cannot equal
$\E[\widetilde X\widetilde Y]$ for the same $\widetilde X$.

**Suggested fix.** Restore the lecturer's two accents. Keep
$\widetilde X = X - \E X$, $\widetilde Y = Y - \E Y$ in §Ковариация (and in the proof
of `prop:var-sum`, replacing `\tilde X` by `\widetilde X`), and introduce the
normalised pair with an overline in §Коефициент на корелация:
> Ако означим центрираните и нормирани случайни величини
> \[ \overline{X} = \frac{X - \E X}{\sqrt{\Var X}}, \qquad \overline{Y} = \frac{Y - \E Y}{\sqrt{\Var Y}}, \]
> то $\E\overline{X} = 0$, $\Var\overline{X} = 1$ и $\rho(X,Y) = \E[\overline{X}\,\overline{Y}]$.

and rewrite `:485–530` and `frontmatter.tex:83` onto $\overline{X}$ accordingly.

---

## 2. WRONG — the covariance terms are said to be *missing* from the hypergeometric variance; they are precisely what is *present* there

**Location:** `lectures/bodies/lecture_07.tex:400–402` (paragraph after `prop:var-sum`).

**What it says now**
> "Ако величините са независими в съвкупност, всички ковариации се нулират и се
> връщаме към адитивността на дисперсията от лекция 5. Точно тези „ковариационни
> членове“ **липсват** при хипергеометричното разпределение, където изтеглянията не
> са независими."

**Why that is wrong.** It is exactly backwards. The covariance terms vanish in the
*independent* case; in the hypergeometric case they are present and negative, and
they are the whole reason the variance carries the factor $\frac{N-n}{N-1} < 1$.
The chapter's own proof of part в) says the right thing at `:231` ("Затова
дисперсията на сумата не е просто сума от дисперсиите, а **включва** и
ковариационните членове"), so `:401` also contradicts `:231`.

**Verification.** For $N=20$, $M=7$, $n=5$ with the indicator decomposition
$X=\sum_{j=1}^n X_j$:

```
sum of variances:        n·p(1−p)            = 1.1375
each pairwise covariance = M(M−1)/(N(N−1)) − p²  = −0.011974
total covariance contribution n(n−1)·Cov   = −0.239474
total                                       = 0.898026
closed formula n(M/N)((N−M)/N)((N−n)/(N−1)) = 0.898026
```

The covariance block is 21% of the sum of the variances, with a negative sign — not
absent. (Same script also verified $\E X$ and $\Var X$ against
`scipy.stats.hypergeom` for $(N,M,n) = (8,4,3), (20,7,5), (50,13,11), (100,40,7)$:
agreement to 10 decimals.)

**Suggested fix.**
> Ако величините са независими в съвкупност, всички ковариации се нулират и се
> връщаме към адитивността на дисперсията от лекция 5. Точно тези „ковариационни
> членове“ **се появяват** при хипергеометричното разпределение, където изтеглянията
> не са независими; те са отрицателни и именно те свиват дисперсията с множителя
> $\frac{N-n}{N-1}$.

---

## 3. BROADENED — the Poisson-approximation recipe is upgraded from the lecturer's "относително добре" to "изключително близки", and it is numerically false at the boundary of the stated range

**Location:** `lectures/bodies/lecture_07.tex:54`.

**What it says now**
> "\emph{Рецепта:} Приближението работи добре и може спокойно да се използва в
> случаите, когато $n \ge 100$ и $np \le 20$. Тогава, дори и да не знаем
> „границите“, твърдим, че биномните вероятности са **изключително близки** до
> Поасоновите с параметър $\lambda = np$."

**Why that is wrong.** The numbers $n \ge 100$, $np \le 20$ are the lecturer's
(**[8:51]** «И рецептата грубо казва … $np$ е по-малко или равен на 20. И $n$ е
по-голямо или равен на 100»), but his claim about the quality was hedged twice:

* **[9:44]** — «И така, че $n$ по $p$ не е голямо, е по-малко или равен, грубо казано
  на 20. … вероятностите на $Y$ може да ги приближават **относително добре** с
  вероятностите на Поасонова случайна величина.»
* **[10:55]** — «добре, **с някаква малка грешка** ще допусна, че вероятността не е
  тази, а е тази тук.»

"Изключително близки" is a strengthening (R3) and it is false at the corner of the
admissible region, $n=100$, $p=0.2$ ($np=20$), which the recipe explicitly permits.

**Verification.** Total-variation distance and pointwise error, `scipy.stats`:

```
n=100  p=0.20  λ=20 : TV=0.0542   P(X=20): bin 0.09930 vs poi 0.08884  (−10.5%)
n=100  p=0.15  λ=15 : TV=0.0395   P(X=15): bin 0.11109 vs poi 0.10244  (− 7.8%)
n=100  p=0.10  λ=10 : TV=0.0258   (− 5.1% at the mode)
n=100  p=0.01  λ= 1 : TV=0.0028   (− 0.5% at the mode)
n=1000 p=0.02  λ=20 : TV=0.0049   (− 1.0% at the mode)
max relative error over k with P(X=k)>1e−3, at n=100, p=0.2:  113%
```

So at the permitted boundary the approximation misses individual probabilities by a
factor of two in the tails and by 10% at the mode. What actually controls the error
is $p$ (the classical bound is $d_{TV} \le np^2 = \lambda p$, equal to 4 — vacuous —
at $n=100, p=0.2$), not $np$.

**Suggested fix.** Return to his formulation and drop the superlative:
> \emph{Рецепта:} Приближението може спокойно да се използва, когато $n \ge 100$ и
> $np \le 20$: тогава, дори без да минаваме към граница, биномните вероятности се
> приближават **относително добре** от Поасоновите с параметър $\lambda = np$, с
> малка допусната грешка.\footnote{Грешката се управлява от $p$, а не от $np$: за
> $n = 100$, $p = 0{,}2$ (крайният допустим случай) разстоянието по вариация е
> $0{,}054$, а отделни вероятности се различават с над 10\%. За $n = 1000$,
> $p = 0{,}02$ (същото $\lambda = 20$) разстоянието пада до $0{,}005$.}

Related loss: at **[9:19]** he set this as an explicit computational exercise —
«Може да си поиграете чисто компютърно да видите колко е добро това приближение, за
какви $k$. Ваши колеги миналата година го бяха правили … и бяха разсъждавали
по-дълбоко защо и тогава това приближение работи добре» — which is absent from
§Задачи (a B-06-class loss). Suggested extra task:
> Изследвайте числено колко добро е Поасоновото приближение: за $n = 100$ и
> $p = 0{,}01;\ 0{,}05;\ 0{,}1;\ 0{,}2$ сравнете $\mathbb{P}(Y = k)$ с
> $e^{-\lambda}\lambda^k/k!$ и определете за кои $k$ приближението е добро.

---

## 4. UNCLEAR / LOST — the linear-dependence criterion concludes $Y = aX+b$ pointwise, and the one step the lecturer flagged as delicate is asserted instead of justified

**Location:** `lectures/bodies/lecture_07.tex:500–502` (`keythm` "Критерий за линейна
зависимост") and `:521–531` (the $\Longleftarrow$ proof).

**What it says now**

Statement:
> "Тогава между тях има строго линейна зависимост от вида $Y = aX + b$ (за някакви
> константи $a \neq 0$ и $b$) тогава и само тогава, когато $|\rho(X, Y)| = 1$."

Proof:
> "Тъй като интегрираме (търсим математическо очакване) на **строго неотрицателна**
> случайна величина и получаваме 0, това означава, че самата случайна величина е
> тъждествено равна на нула (с вероятност 1):
> $(\widetilde{X} - \widetilde{Y})^2 = 0 \implies \widetilde{X} = \widetilde{Y}$"

**Why that is wrong.** Three points, in increasing order of importance.

1. The conclusion only holds **almost surely**, and the proof itself says so
   parenthetically before dropping it from the display and from the theorem
   statement. Concrete failing case: on $\Omega = [0,1]$ with Lebesgue measure take
   $X(\omega) = \omega$ and $Y(\omega) = \omega$ for $\omega \neq 1/2$,
   $Y(1/2) = 17$. Then $\rho(X,Y) = 1$ but there is no pair $(a,b)$ with
   $Y = aX+b$ *everywhere*. The theorem as printed is therefore false; with
   "с вероятност 1" it is exactly right. This also matters for the $\Longrightarrow$
   direction, where "$Y = aX+b$" should equally be read a.s.
2. "**строго** неотрицателна" is not a property $(\widetilde X - \widetilde Y)^2$ has —
   it is nonnegative, and the whole point is that it is *zero* somewhere. As written
   the sentence is self-contradictory.
3. The implication $\E Z^2 = 0 \Rightarrow Z = 0$ a.s. is the single step the lecturer
   singled out as the hard one, and he gave two things the book drops: the discrete
   argument, and a forward reference for the general case.

   * **[100:20]–[101:31]** — «ако имахме дискретни случайни величини, това ще бъде
     $\sum p_{ij}(\tilde x_i - \tilde y_j)^2$ … И ако това нещо, знаете, че е 0, вие
     трябва всички тези да са ви 0. Защото сумирате неотрицателно, неотрицателно и
     сумата ви е 0. Значи тези трябва да са 0 … защото вероятностите, които сме
     взели, са положителни. Те, ако са 0, нямаше 0 да ги вземаме.»
   * **[106:12]–[106:46]** — «Единственото нещо, което може би … е, че това очакване
     на нещо на квадрата е равно на 0, следва че това нещо вътре е 0. **А това ще
     видим с неравенството на Чебишов.** И аз ви дадох общите съображения чрез тази
     сума, която написах.»

   The book replaces both with a flat assertion, so the reader gets neither the
   discrete proof nor the notice that the general case is deferred.

**Verification.** No computation needed for the a.s. gap (an explicit
counterexample is given above); the discrete argument is arithmetic. Cross-checked
against `run/pesho/ocr/page_017.json`, which likewise records only the
$\Longrightarrow$ half in closed form.

**Suggested fix.** Statement:
> Тогава $|\rho(X, Y)| = 1$ тогава и само тогава, когато с вероятност 1 е изпълнено
> $Y = aX + b$ за някакви константи $a \neq 0$ и $b$.

Proof:
> Получихме $\E[(\widetilde{X} - \widetilde{Y})^2] = 0$. Очакване на неотрицателна
> случайна величина е 0 само ако самата величина е 0 с вероятност 1. За дискретни
> величини това се вижда направо: сумата
> $\sum_{i,j} p_{i,j}(\widetilde{x}_i - \widetilde{y}_j)^2$ е сума на неотрицателни
> събираеми, така че всяко събираемо с положителна вероятност $p_{i,j}$ е нула.\footnote{В
> общия случай твърдението следва от неравенството на Чебишов, което ще докажем в
> лекция 10; на лекцията беше отбелязано именно това.} Следователно
> $\widetilde{X} = \widetilde{Y}$ с вероятност 1.

---

## 5. LOST — the derivation of $p_j = M/N$ is replaced by a symmetry appeal; the lecturer computed it, on the board, from $\binom{N-1}{M-1}/\binom{N}{M}$

**Location:** `lectures/bodies/lecture_07.tex:226` (proof of `prop` part б).

**What it says now**
> "Поради пълната симетрия на модела (няма значение дали теглите първи или $j$-ти,
> преди да сте видели резултатите от останалите тегления, вероятността е една и
> съща), вероятността на коя да е позиция да се падне маркиран обект е точно
> пропорцията на маркираните обекти в началото, а именно $p_j = \frac{M}{N}$."

**Why that is wrong.** The exchangeability appeal is true, but it is not what was
taught, and the lecturer said explicitly that the computation was the point of the
whole detour. He set up the arrangement model (all $N$ positions, the $M$ marked
objects distributed over them, then look at the first $n$):

* **[26:22]** — «ако искате да поставите маркираните някъде между тези $N$ на брой
  обекта, вие ще можете да го направите по $\binom{N}{M}$ начина»;
* **[27:10]** — «Ами вие вече имате $N$ без един обекта и $M$ без един маркиран,
  защото сте запазили един маркиран, който сте поставили тук» → $\binom{N-1}{M-1}$;
* **[28:01]** — «Е, това не е трудно да видите, че е $M$ върху $N$. Използвайки …
  формулите за тези биномни коефициенти»;
* **[28:36]** — «Загубих време да ви направя тази сметка само защото зад нея се крие
  тази … структура.»

The board carries the identity verbatim: `run/lecture_07/ocr/board_007.json` →
`\frac{\binom{N-1}{M-1}}{\binom{N}{M}} = \frac{M}{N}`, and the third witness
`run/pesho/ocr/page_015.json` has
`\frac{\binom{N-1}{M-1}}{\binom{N}{M}} = \frac{M}{N} = \mathbb{P}(X_j=1)`.

A second remark went with it and is also gone: **[27:36]** «Вижте, че това по никакъв
начин не зависи от малкото $n$» — i.e. $p_j$ is free of the sample size, which is
what makes the sum collapse to $n\,M/N$.

**Verification.** `sympy`: `simplify(binomial(N-1,M-1)/binomial(N,M))` → `M/N`;
checked as exact rationals for $(N,M) = (8,4), (20,7), (100,40), (13,5)$ — all equal
$M/N$.

**Suggested fix.** Recover the computation (R4) and keep the symmetry remark as
intuition:
> Пресмятаме $p_j$ в модела на разположенията: $M$-те маркирани обекта може да се
> разположат сред $N$-те места по $\binom{N}{M}$ равновъзможни начина, а тези от тях,
> при които на $j$-тото място стои маркиран обект, са $\binom{N-1}{M-1}$ (един
> маркиран е вече поставен, остават $M-1$ маркирани върху $N-1$ места). Значи
> \[ p_j = \mathbb{P}(X_j = 1) = \frac{\binom{N-1}{M-1}}{\binom{N}{M}} = \frac{M}{N}. \]
> Забележете, че този израз не зависи нито от $j$, нито от размера на извадката $n$ —
> точно това е симетрията на модела.

---

## 6. LOST — the explicit discrete formula for the covariance

**Location:** should sit in `lectures/bodies/lecture_07.tex` §Ковариация, after the
definition at `:362–371`.

**Why that is wrong.** The lecturer introduced covariance in full generality but
immediately wrote down what it means for a discrete pair, precisely because
expectation for non-discrete variables had not yet been defined, and he told the
students to fall back on it:

* **[66:49]–[67:21]** — «Ще ви дам пример, защото ние сме работили дотук само с
  дискретни: когато имаме две дискретни, ковариацията на $X$ и $Y$ не е нищо друго
  от сумата … $p_{ij}$ … по $(x_i - \E X)(y_j - \E Y)$»;
* **[68:02]** — «Сумирате по всички възможни стойности на двойката $X$ и $Y$»;
* **[71:59]** — «Ако се чувствате некомфортно с общи случайни величини, използвайте
  формулата за дискретните и отворете скобите в произведението, което имахте там.»

Nothing of this survives; the chapter defines $\Cov$ only abstractly, which leaves the
reader of a chapter that has not yet met continuous variables with no way to compute
anything. It is also the formula §Задачи task 5 tells the reader to use.

**Suggested fix.** Add after `:370`:
> За дискретни $X$ и $Y$ със съвместно разпределение $p_{i,j}$ това е обикновена
> двойна сума:
> \[ \Cov(X, Y) = \sum_{i}\sum_{j} p_{i,j}\,(x_i - \E X)(y_j - \E Y), \]
> и всички сметки по-долу може да се четат в тази форма — свойствата на очакването
> (линейност, положителност), доказани за дискретни величини, остават верни и в
> общия случай.

---

## 7. UNSOUND — independence $\Rightarrow$ $\Cov = 0$ is stated with no integrability hypothesis

**Location:** `lectures/bodies/lecture_07.tex:372–374` (`cor`).

**What it says now**
> "Ако $X$ и $Y$ са независими …, то математическото очакване на произведението им се
> разпада на произведение от очакванията им ($\E[XY] = \E X\E Y$). Следователно, при
> независими случайни величини ковариацията е точно 0."

**Why that is wrong.** Failing case: $X, Y$ independent standard Cauchy. They are
independent, but $\E|X| = \infty$, so $\E X$, $\E[XY]$ and hence $\Cov(X,Y)$ do not
exist — the covariance is not "точно 0", it is undefined. The definition one line
above does carry "(ако това очакване съществува)", but the corollary asserts a value
unconditionally. The lecturer's phrasing was the same (**[75:26]** «независимост на
$X$ и $Y$ влече нулева ковариация»), so under R1 the fix is a hypothesis plus a
footnote, not a rewrite.

**Verification.** Simulation of iid standard Cauchy pairs, `numpy`:

```
n=10^4   sample cov =     1.77
n=10^5   sample cov =     3.94
n=10^6   sample cov =     7.85
n=10^7   sample cov =  -209.73
```

The sample covariance does not settle — there is nothing for it to converge to.
(`scipy.integrate.quad` of $|t|/(\pi(1+t^2))$ over $[-10^6,10^6]$ gives $8.795$ and
grows logarithmically, confirming $\E|X| = \infty$.)

**Suggested fix.**
> Ако $X$ и $Y$ са независими и имат крайни очаквания, то $\E[XY] = \E X\,\E Y$ и
> следователно $\Cov(X, Y) = 0$.\footnote{Условието за крайни очаквания е
> необходимо: за независими $X, Y$ със стандартно разпределение на Коши
> ковариацията не съществува, а не е нула. На лекцията то се подразбираше.}

Keep the rest of the corollary (the converse fails) unchanged — it is his and it is
correct.

---

## 8. UNSOUND — both correlation theorems are stated for "крайни дисперсии" only, contradicting the chapter's own definition of $\rho$

**Location:** `lectures/bodies/lecture_07.tex:470–475` (`thm:corr-bounds`) and
`:500–502` (Критерий за линейна зависимост), against the definition at `:410–413`.

**What it says now**
* `:411` — "Коефициент на корелация $\rho(X, Y)$ между две случайни величини с крайни
  и \emph{строго положителни} дисперсии …"
* `:471` — "За произволни случайни величини с **крайни дисперсии** е вярно, че
  $|\rho(X, Y)| \le 1$."
* `:501` — "Нека $X$ и $Y$ са случайни величини с **крайни дисперсии**."

**Why that is wrong.** Take $X \equiv 0$ and $Y \sim \Ber(1/2)$: both variances are
finite, so both theorems apply as written, but $\rho(X,Y) = 0/0$ is undefined by the
chapter's own definition, and each proof divides by $\sqrt{\Var X}$ at its first step
(`:485` needs $\Var\widetilde X = 1$, `:507–511` divides by $\sqrt{\Var X}$ and
$\sqrt{\Var Y}$). So the hypothesis printed in the two theorems is strictly weaker
than the one the definition and the proofs require. The lecturer wrote only
$\mathbb{D}X < \infty$, $\mathbb{D}Y < \infty$ on the board
(`run/lecture_07/ocr/board_019.json`, `board_020.json`; **[78:32]**, **[88:07]**), and
`run/pesho/ocr/page_016.json` records the same, so the omission is his — but the book
has already tightened the definition, and leaving the theorems loose makes the chapter
internally inconsistent.

Note that no *integrability* hypothesis is needed beyond finite variances: by
Cauchy–Schwarz $\E|\widetilde X \widetilde Y| \le \sqrt{\Var X \Var Y} < \infty$, so
$\Cov$ automatically exists here. Only positivity is missing.

**Verification.** By hand: $\Var X = 0 \Rightarrow$ denominator $0$; nothing to
compute. Cross-checked that the fix is not needed in the definition itself (`:411`
already has it).

**Suggested fix.** In both theorem statements replace "с крайни дисперсии" by
> Нека $X$ и $Y$ са случайни величини с крайни и строго положителни дисперсии
> ($0 < \Var X < \infty$, $0 < \Var Y < \infty$)

with one footnote, e.g. on `thm:corr-bounds`:
> \footnote{На лекцията беше записано само $\Var X < \infty$, $\Var Y < \infty$;
> строгата положителност е нужна, за да е дефиниран $\rho$.}

---

## 9. UNSOUND — the "only the Poisson has this property" characterisation omits the restriction $0 < p < 1$

**Location:** `lectures/bodies/lecture_07.tex:167–174` (last block of
`supp:poisson-thinning`).

**What it says now**
> "Ако $N$ е произволна целочислена неотрицателна величина, прореждането ѝ дава
> независими $M$ и $K$ само когато $N$ е Поасоново (или тъждествено 0)."

**Why that is wrong.** For $p = 1$ we get $M = N$ and $K \equiv 0$; a constant is
independent of everything, so *every* $N$ produces independent $M$ and $K$.
Symmetrically for $p = 0$. So the "only if" is false for $p \in \{0,1\}$ — take
$\mathbb{P}(N=1) = 0.5$, $\mathbb{P}(N=2) = 0.3$, $\mathbb{P}(N=5) = 0.2$, $p = 1$:
$M$ and $K$ are independent and $N$ is neither Poisson nor $\equiv 0$. The
functional-equation argument that follows also quietly needs $\mathbb{P}(N=0) > 0$
(it divides by $G_N(p)$ and $G_N(q)$ and normalises by $G_N(0)$) and needs $p,q > 0$
for the substitutions $a = ps$, $b = qt$ to sweep intervals of positive length.
Since `supp` blocks are audited for mathematics but not for lecture provenance, this
is a genuine (if minor) defect of the supplement.

**Verification.** The forward direction of the supplement was verified numerically:
for $\lambda = 6$, $p = 1/3$, summing
$\sum_N \mathbb{P}(N)\binom{N}{j}p^j q^{N-j}$ over $N \le 80$ and comparing the joint
$(M,K)$ table on $\{0..19\}^2$ against $\Poi(2) \otimes \Poi(4)$ gave
`max |joint − product| = 5.55e−17`. The $p=1$ counterexample needs no computation:
$K \equiv 0$.

The two figures in the supplement were also checked: in
`fig:thinning-independence` the plotted radii are proportional to
$\sqrt{\mathbb{P}(M=j,K=k)}$ (so the *areas* are proportional to the probabilities, as
the caption claims) with one common scale per panel — reproduced to 3 decimals for
both panels ($\Bin(6,1/3)$ on the anti-diagonal; $\Poi(2)\otimes\Poi(4)$ on the right).

**Suggested fix.**
> Ако $0 < p < 1$ и $N$ е произволна целочислена неотрицателна величина, прореждането
> ѝ дава независими $M$ и $K$ само когато $N$ е Поасоново (включително изродения
> случай $\lambda = 0$, тоест $N \equiv 0$). \emph{(За $p = 0$ или $p = 1$ един от
> двата броя е тъждествено 0 и независимостта е тривиална за всяко $N$.)}

---

## 10. LOST — the worked evaluation of the joint CDF on the two-dice example

**Location:** after `lectures/bodies/lecture_07.tex:318` (definition of
$F_{X,Y}$). The chapter gives the geometric description of the south-west rectangle
and then moves straight to `prop:marginal-from-joint`.

**Why that is wrong.** The lecturer spent **[43:41]–[45:22]** evaluating the new
definition on the example the chapter has just built, which is what makes the strict
inequality convention concrete:

* «Ако вземем конкретно пример за зарчетата … $F_{X,Y}(1/2, 1/2)$ … То ви хваща само
  ето тази точка. Значи това нещо е вероятността $X$ да е равна на 0 и $Y$ равна на
  0» — i.e. $F_{X,Y}(1/2,1/2) = \mathbb{P}(X=0,Y=0) = 16/36$;
* «Ако взема тази точка, да кажем 4, 4 — $F(4,4)$ е единица, защото всички са
  попаднали вътре»;
* and the intermediate case «ще да взема сумата на ето тези 4 вероятности».

Both endpoints are on the board: `run/lecture_07/ocr/board_010.json` and
`board_011.json` carry `F_{X,Y}(1/2,1/2)` `=` `\mathbb{P}(X=0;Y=0)` right under the
definition.

**Verification.** From the chapter's own table: $F_{X,Y}(1/2,1/2) = 16/36$;
$F_{X,Y}(3/2,3/2) = (16+8+8+2)/36 = 34/36$; $F_{X,Y}(4,4) = 1$. Arithmetic checked
against the table at `:284–293`, whose entries sum to $36/36$.

**Suggested fix.** Add after the geometric paragraph:
> \emph{Пример (продължение на примера с двата зара).} Понеже неравенствата са строги,
> $F_{X,Y}(1/2, 1/2) = \mathbb{P}(X = 0, Y = 0) = \frac{16}{36}$ — в правоъгълника
> попада само точката $(0,0)$. Аналогично
> $F_{X,Y}(3/2, 3/2) = \frac{16+8+8+2}{36} = \frac{34}{36}$, а
> $F_{X,Y}(4,4) = 1$, защото всички възможни стойности вече са уловени.

---

## 11. Fidelity note (not a mathematical error) — `prop:var-sum` is editorial content presented as lecture material

**Location:** `lectures/bodies/lecture_07.tex:376–398`.

The proposition ($\Var(aX+bY) = a^2\Var X + b^2 \Var Y + 2ab\Cov(X,Y)$ and the
$n$-term version) and its proof are **mathematically correct** — I verified the
$n$-term identity numerically as part of finding 2 (the indicator decomposition of the
hypergeometric variance reproduces the closed formula exactly). But it is not in the
lecture: nothing in the transcript states it. The only thing the lecturer said in this
direction is the negative remark at **[25:14]** — «Затова не може да докажете лесно и
дисперсията, защото ако имахте независимост, можеше да вземете … Дисперсия на сумата е
сума на дисперсия, но те не са независими» — and at **[21:11]** he explicitly refused
the hypergeometric variance as «чисто техническо упражнение». `git log -S` shows the
block entered in `7bf846b` "Strengthen the theory: proofs, missing statements, closed
hand-waves".

Since the book's convention is that non-lecture material lives in `supp` (Допълнение),
a `prop` on the shared counter reads as something the lecturer proved. Recommend
either moving it into a `supp` block or footnoting it as an editorial addition. No
change to the mathematics.

---

## 12. UNCLEAR — the middle panel of `fig:correlation` cannot support the claim its caption makes

**Location:** `lectures/bodies/lecture_07.tex:426–431` (caption) and `:454–459`
(the $\rho \approx 0$ point set).

**What it says now**
> "Средният панел предупреждава: $\rho \approx 0$ означава липса на \emph{линейна}
> връзка, а не независимост."

**Why that is wrong.** The plotted cloud is unstructured noise, so it illustrates
$\rho \approx 0$ but shows nothing about dependence — a reader looking for the warned
-about non-linear relation will not find one. The correct illustration is a visibly
dependent set with zero correlation (points on a circle, or on a parabola
$y \propto (x-\tfrac12)^2$).

**Verification.** Extracted the 24 plotted coordinates and computed, with
`numpy`/`scipy.stats`:

```
pearson  rho(x,y)      =  0.060      <- matches the "rho ~ 0" label
spearman rho(x,y)      =  0.100
rho(|x - mean x|, y)   = -0.108
rho(x^2, y)            =  0.031
rho(x, y^2)            =  0.102
```

No monotone or quadratic structure — the panel is consistent with independence.
(The other three panels were verified to match their labels: claimed
$+0{,}95 / +0{,}55 / -0{,}95$, actual $0.953 / 0.556 / -0.961$.)

**Suggested fix.** Either replace the middle point set with a zero-correlation but
dependent configuration (e.g. points along $y = 4(x-\tfrac12)^2$, or on a circle) and
keep the caption, or keep the cloud and weaken the caption to
> Средният панел показва липса на линейна връзка. Важно е обаче, че $\rho \approx 0$
> само по себе си не означава независимост — възможна е силна нелинейна зависимост
> при нулева корелация.

---

# Checked and found sound

Everything below was verified and needs no change.

**Poisson theorem and its proof (`:15–44`).**
* Hypotheses match the lecture exactly: $X_n \sim \Bin(n,p_n)$ for every $n \ge 1$,
  $\lim n p_n = \lambda > 0$, conclusion for every $k \ge 0$ (**[3:55]–[5:05]**; the ASR
  garbles "$k \ge 0$" into "$k$ по-голямо да равна на 1", but the board and
  `run/pesho/ocr/page_015.json` confirm $k \ge 0$).
* The pgf continuity statement at `:7–11` is correctly stated (convergence of
  $G_{X_n}$ on the domain to the pgf of an integer-valued $X$ implies pointwise
  convergence of the probabilities) and correctly attributed as unproved
  (**[1:11]** «твърдение, което няма да го доказвам»).
* The proof's restriction to the special case $np_n = \lambda$ exactly is the
  lecturer's own (**[11:02]–[11:38]**) and is labelled as such.
* `sympy`: $\sum_k \binom{5}{k}p^k(1-p)^{5-k}s^k - (1-p+ps)^5 = 0$;
  $\sum_k e^{-\lambda}\lambda^k s^k/k! = e^{\lambda(s-1)}$;
  $\lim_{n\to\infty}(1+\lambda(s-1)/n)^n = e^{\lambda(s-1)}$. The algebra
  $1 - \frac{\lambda}{n} + \frac{\lambda}{n}s = 1 + \frac{\lambda(s-1)}{n}$ is right.
* Numerically, $\Bin(n,3/n)$ pmf $\to \Poi(3)$ pmf: at $n=10^5$ the first six
  probabilities agree with $\Poi(3)$ to $2\cdot10^{-6}$.

**Hypergeometric proposition (`:189–233`).**
* pmf, $\E X = nM/N$ and $\Var X = n\frac{M}{N}\frac{N-M}{N}\frac{N-n}{N-1}$ all match
  the board (`board_003/004/005/006/007.json`) and `run/pesho/ocr/page_015.json`.
* `scipy.stats.hypergeom`: mean and variance agree with the closed formulas to 10
  decimals for $(N,M,n) = (8,4,3), (20,7,5), (50,13,11), (100,40,7)$.
* Support bounds $0 \vee (n-N+M) \le k \le M \wedge n$ are correct, including the
  non-trivial lower bound: for $(N,M,n) = (10,8,5)$ the true support is $\{3,4,5\}$
  and the formula gives $(3,5)$; for $(12,9,7)$ it is $\{4,\dots,7\}$ vs $(4,7)$.
* Parameter constraints $N \ge M$, $N \ge n$ match **[18:46]**.
* The linearity-of-expectation route (indicators, no independence needed) and the
  explicit warning that the $X_j$ are *not* independent are faithful to
  **[24:53]–[25:26]**; refusing the variance as a technical exercise is his
  (**[21:11]**) and it is preserved as §Задачи task 2.

**`supp:hg-to-bin` (`:240–249`).** $\Hyp(N,M,n) \to \Bin(n,p)$ under $M/N \to p$, $n$
fixed: for $p = 0.3$, $n = 4$ the pmf converges to $\Bin(4,0.3)$ —
at $N = 10^6$ agreement is to $10^{-4}$; the stated mechanism (drawing a few items
barely changes the proportion) is correct.

**`supp:poisson-thinning` forward direction (`:57–165`).** Joint pmf derivation, the
factorisation $e^{-\lambda} = e^{-\lambda p}e^{-\lambda q}$, both marginals, the
independence conclusion, the contrast with fixed $N$ (correlation $-1$ between $M$ and
$K = n - M$), and the worked example ($\Poi(20)$, $p=0.15$ → $\Poi(3)$ and $\Poi(17)$;
$\Var M = 3 \neq 2.55$; $\mathbb{P}(M=0) = e^{-3} = 0.0498$) are all correct.
Numerically the joint table for $\lambda=6$, $p=1/3$ matches
$\Poi(2)\otimes\Poi(4)$ to $5.6\times10^{-17}$. Both figures' data reproduce their
captions. (Only the "only Poisson" endnote needs the $0<p<1$ caveat — finding 9.)

**Joint distributions (`:251–308`).** The two-dice example is arithmetically exact:
$16+8+8+2+1+1 = 36$; marginals $25/36, 10/36, 1/36$ equal $\Bin(2,1/6)$ scaled by 36
(verified: `[25., 10., 1.]`). Matches **[38:08]–[40:33]** step for step.

**Joint CDF and marginals (`:310–335`).** $F_{X,Y}(x,y) := \mathbb{P}(X<x,Y<y)$ with
the strict inequality matches `board_010.json` and the book's global convention;
$F_{X,Y}(x,\infty) = F_X(x)$, $F_{X,Y}(\infty,y) = F_Y(y)$, $F_{X,Y}(\infty,\infty)=1$
and the justification via $\mathbb{P}(A \cap B) = \mathbb{P}(A)$ when
$\mathbb{P}(B)=1$ match `board_015.json` and **[60:29]–[62:26]** exactly.

**`thm:indep-criterion` (`:337–344`).** The CDF-factorisation criterion is a genuine
iff under the book's strict-inequality convention: the sets
$(-\infty,x)\times(-\infty,y)$ form a $\pi$-system generating $\mathcal{B}(\mathbb{R}^2)$,
so agreement of the two measures there extends to the whole $\sigma$-algebra. The
remark that the pointwise criterion is the usable one for discrete variables is his
(**[63:01]**).

**`rem:sum-dependence` (`:346–350`) and §Задачи Домашно 2.** The counterexample
$Y = Z$ is valid; $X + Y = X + Z$ is not independent of $Z$ (e.g.
$\Cov(X+Z, Z) = \Var Z = 1 \neq 0$). Per `docs/REMEDIATION.md` §11 this homework was
deliberately relocated here from L14, so its absence from the L07 transcript is
expected.

**Covariance definition and scaling (`:362–371`, `:404`).** The existence caveat
"(ако това очакване съществува)" matches **[66:34]** and
`run/pesho/ocr/page_016.json`; the alternative formula
$\Cov = \E[XY] - \E X\,\E Y$ matches the board (`board_017.json`) and is left as an
exercise exactly as he left it (**[71:54]**, §Задачи task 5);
$\Cov(10X,10Y) = 100\Cov(X,Y)$ and the scale-invariance of $\rho$ are correct and are
his motivation verbatim (**[73:06]–[73:57]**, **[77:06]–[77:40]**).

**`prop:var-sum`'s mathematics (`:376–398`).** Correct (see finding 11 for the
provenance point). The $n$-term identity was verified in the hypergeometric setting:
$n\,p(1-p) + n(n-1)\Cov(X_i,X_j) = 1.1375 - 0.2395 = 0.8980$, equal to the closed
hypergeometric variance to 15 decimals.

**`thm:corr-bounds` proof (`:482–496`).** The Cauchy–Bunyakovsky argument via
$0 \le \E[(\widetilde X \pm \widetilde Y)^2] = 2 \pm 2\rho$ is exactly the board
argument (`board_019.json`) and is correct; the Cauchy–Schwarz / inner-product remark
at `:477–481` recovers **[83:56]–[84:16]**, including his refusal to develop the
geometric viewpoint. (Hypothesis wording: finding 8.)

**Linear-dependence criterion, $\Longrightarrow$ direction (`:504–519`).** Correct,
including $\sqrt{\Var Y} = |a|\sqrt{\Var X}$ and $v = \operatorname{sgn}(a) = \pm1$.
The book's added hypothesis $a \neq 0$ is a necessary tightening of the board version
`Y = aX + b \iff |\rho|=1` (`board_020.json`) and is right to be there. Handling the
$\rho = -1$ case by "аналогично" is his (**[97:56]**).

**Exercise recovery.** §Задачи tasks 1–5 all trace to explicit assignments:
task 1 → **[13:43]** «Опитайте се да докажете, че ето това нещо се схожда към това
число»; task 2 → **[21:11]**; task 3 → **[30:00]–[30:21]** (the eight-marker demo,
$\Hyp(8,4,3)$, asking for $k = 0,1,2,3$); task 4 → **[61:13]**; task 5 → **[71:54]**.
Only the computational Poisson-approximation experiment (**[9:19]**) is missing — noted
under finding 3.

---

# Not reported (book conventions / already-rejected classes)

* $F_X(x) = \mathbb{P}(X<x)$ strict, `\Var` printing as $\mathbb{D}$, `\Poi`/`\Bin`
  spellings — deliberate conventions.
* The $\Poi$/$\Bin$/$\Hyp$ parameter order $\Hyp(N,M,n)$ differs from
  `run/pesho/ocr/page_015.json`'s $HG(M,N,n)$, but the board
  (`board_003–007.json`) uses $HG(N,M,n)$ as the book does.
* The special-case proof needs $n \ge \lambda$ for $p_n = \lambda/n \le 1$ — too
  pedantic to footnote; the limit is unaffected.
* Formatting matters (C-07 hyphen list, C-08 prose inside proofs) were out of scope
  and are already recorded in `docs/REMEDIATION.md`.
