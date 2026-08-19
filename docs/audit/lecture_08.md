# Mathematics audit — `lectures/bodies/lecture_08.tex`

**Chapter:** Условно математическо очакване. Непрекъснати случайни величини (167-min double lecture)
**Witnesses used:** `run/lecture_08/audio/transcript.json` (3846 deduped segments, 0–167 min);
`run/lecture_08/ocr/board_0NN.json` (68 frames) + two board PNGs read directly;
`docs/REMEDIATION.md` §0–2, §8; L09 `bodies/lecture_09.tex` for downstream use of the change-of-variables rule.
**Break windows checked:** 46–60 min and 108–122 min. Across the first, boards 020–026
(t = 45.7 → 57.0 min) carry identical content — the г) tower-law line and nothing else; across the
second, boards 047–052 (t = 106.5 → 121.2 min) carry the identical insurance example. In both cases
the only diffs between consecutive frames are OCR noise (`г)` vs `Г)`, `10.000` vs `10,000`,
`0.59` vs `0,59`). So the board did not change and nothing was said. **No finding below rests on an
absence inside a break** — every one is anchored either to a spoken quote outside the break windows
or to a board frame.

Verification environment: `/Users/g8row/Documents/lec2tex/.venv/bin/python3` (sympy 1.x, numpy, scipy).

---

## F-01 — The identity every proof in the chapter uses is never stated

- **Severity:** LOST (and it makes the three proofs non-sequiturs)
- **Location:** `lectures/bodies/lecture_08.tex:99–118` (proof of Твърдение `prop:cond-exp-props`),
  gap sits between `:63` (the `keydefn`) and `:68`.

**What it says now.** The `keydefn` at `:57–63` defines

```
\E[X \given Y=y_j] = \sum_i x_i \mathbb{P}(B_i \given A_j)
```

and `:67` defines `\E[X \given Y] = \sum_j \E[X \given Y=y_j] \ind_{A_j}`. Then the proof opens at `:100`
with *«а) Използвайки дефиницията за индикаторно представяне:»* and writes

```
\E[aX + bZ \given Y] = \sum_j \frac{\E[(aX+bZ)\ind_{A_j}]}{\mathbb{P}(A_j)}\ind_{A_j}
```

The same representation is the sole engine of б) (`:109`, *«в дефиниционната сума»*) and г) (`:114`).

**Why that is wrong.** `\E[X\ind_{A_j}]/\mathbb{P}(A_j)` is *not* the book's definition and the book
never shows it equals `\E[X\given Y=y_j]`. Every proof in the section therefore begins from an
identity the reader has not been given, and `:100`/`:109` misdescribe it as "the definition".

The lecturer derived it explicitly, on the board, immediately before stating the definition:

> [23:53] «тогава ето този факт … ви дава много лесен начин за пресмятането на това очакване, и
> очакването на X·1_{A_j} не е нищо друго от очакването на сумата … x_i 1_{B_i} 1_{A_j} … от
> линейност тази сума излиза отвънка … x_i по вероятността на A_j ∩ B_i»
> [24:38] «или в този случай имаме, че очакването на X при положение Y … записвам го с червено,
> защото е важно, е сумата по j …»

`run/lecture_08/ocr/board_012.json` (t = 22.5 min) carries the general formula on its own line:

```
\mathbb{E}[X|Y] = \sum_j \frac{\mathbb{E} X 1_{A_j}}{\mathbb{P}(A_j)} 1_{A_j}
```

and `board_013.json` (t = 28.1 min) carries the bridge to the definition:

```
X = \sum_i x_i 1_{B_i} \implies \mathbb{E}[X\mid Y] = \sum_j \sum_i x_i \frac{\mathbb{P}(A_j \cap B_i)}{\mathbb{P}(A_j)} 1_{A_j}
                                                   = \sum_j \sum_i x_i \mathbb{P}(B_i \mid A_j) 1_{A_j}
```

Both boards were dropped from the chapter.

**Verification.** Re-derived the identity symbolically on the chapter's own two-dice model
(Y = number of sixes, X = number of ones, `Example ex:08-2`) by enumerating all 36 outcomes:
`E[X·1_{Y=0}] / P(Y=0) = (10/36)/(25/36) = 2/5`, and `Σ_i x_i P(X=x_i|Y=0) = 0·16/25 + 1·8/25 + 2·1/25 = 2/5`.
Equal, as required. (Same script as F-07.)

**Suggested fix.** Insert, between `:63` and `:65`, the лема the lecturer proved — as a
`lem`, since it is used three times afterwards:

> **Лема.** Нека $X=\sum_i x_i\ind_{B_i}$ и $Y$ са дискретни, а $A_j=\{Y=y_j\}$ е събитие с
> $\mathbb{P}(A_j)>0$. Тогава
> \[ \E[X\ind_{A_j}] = \sum_i x_i\,\mathbb{P}(A_j\cap B_i) = \mathbb{P}(A_j)\,\E[X\given Y=y_j], \]
> откъдето условното математическо очакване като случайна величина се записва в
> \emph{индикаторен вид}
> \[ \E[X\given Y] = \sum_j \frac{\E[X\ind_{A_j}]}{\mathbb{P}(A_j)}\,\ind_{A_j}. \]
> *Доказателство.* Произведението на два индикатора е индикатор на сечението, а очакването на
> индикатор е вероятност: $\E[\ind_{B_i}\ind_{A_j}] = \mathbb{P}(A_j\cap B_i)$. Разделяйки на
> $\mathbb{P}(A_j)$, получаваме $\sum_i x_i\mathbb{P}(B_i\given A_j)$, което е точно
> $\E[X\given Y=y_j]$. $\square$

and change `:100` from «Използвайки дефиницията за индикаторно представяне» to «Използвайки
индикаторния вид от лемата».

---

## F-02 — The minimisation property is the lecturer's definition; the book proves it only for binary $Y$ and never states it in general

- **Severity:** LOST / NARROWED
- **Location:** `lectures/bodies/lecture_08.tex:43` (`=: \E(X\given Y)`), `:55`, `:57–68`, `:70–80`

**What it says now.** `:43` christens the binary-case minimiser `\E(X\given Y)`; `:55` then says

> «Въз основа на изложената геометрична мотивация (като проекция в средноквадратичен смисъл),
> можем да дефинираме понятието формално за произволни дискретни случайни величини.»

and the formal definition that follows (`:57–68`) is the conditional-probability sum. Nowhere in the
chapter is it claimed — let alone proved — that for general $Y$ the random variable
$\E[X\given Y]=\sum_j \E[X\given Y=y_j]\ind_{A_j}$ solves $\min_G \E(X-G(Y))^2$.

**Why that is wrong.** The whole §"Мотивация" exists to establish that minimisation property, and the
lecturer made it *the definition*, explicitly for arbitrary $X$ and $Y$:

> [14:17] «Това ще бъде дефиницията на условно математическо очакване …»
> [14:41] «условното очакване на X при положение Y, което се означава … с $G^*(Y)$ … е тази функция,
> е тази случайна величина, която минимизира … по всички възможни функции»
> [15:42] «т.е. този вид условното математическо очакване ни дава минимума или най-доброто
> средноквадратично приближение на X, и в този смисъл е оправдано неговото въвеждане по същия
> начин, както е оправдано въвеждането на очакването на X»

and he twice said the definition does **not** depend on discreteness — the narrowing to "дискретни"
is the book's, not his:

> [14:01] «само искам да ви кажа, не съм го направил за дискретни само … аз казвам, ще работя с
> дискретни … но почти всички тия сметки вървят и за непрекъснатите»
> [16:16] «аз специално за Y ще ползвам все дискретни … но самата дефиниция не зависи от това дали
> Y е дискретна или не»
> [31:54] «вие имате едно много важно понятие … неговият смисъл е, че минимизира — това са числата,
> които трябва да избираме, които да характеризират X при положение, че наблюдаваме Y»

As the chapter now stands, the reader is given a motivation for binary $Y$, then a definition for
general $Y$, and no statement that the two agree. The payoff of §1 is dropped.

**Verification.** Confirmed the general claim numerically on the chapter's own two-dice example by
free minimisation over all three values of $G$ (sympy, solving $\partial_{g_y}\E(X-G(Y))^2=0$):

```
argmin G(y):  {g0: 2/5, g1: 1/5, g2: 0}
E[X|Y=0] = 2/5,  E[X|Y=1] = 1/5,  E[X|Y=2] = 0        <- identical
min value E(X-E[X|Y])^2 = 4/15  ≈ 0.2667
Var X (the best constant, i.e. best G with no info) = 5/18 ≈ 0.2778
```

so the conditional expectation is the minimiser and is *strictly* better than the best constant.

**Suggested fix.** Add a `prop` right after `:68` recovering what was said, with the second-moment
condition that makes it true:

> **Твърдение (характеризация чрез минимизация).** Нека $\E X^2<\infty$ и $Y$ е дискретна.
> Тогава за всяка функция $G$ с $\E[G(Y)^2]<\infty$ е изпълнено
> \[ \E\big(X - \E[X\given Y]\big)^2 \le \E\big(X-G(Y)\big)^2, \]
> т.е. минимумът $\min_G \E(X-G(Y))^2$ се достига при $G^*(Y)=\E[X\given Y]$. Точно това е
> смисълът, в който условното очакване е \emph{най-доброто средноквадратично приближение} на $X$
> чрез наблюдението $Y$ — обобщение на $\Var X = \min_{a}\E(X-a)^2$ от началото на лекцията.

and soften `:55`, e.g. «Ще дефинираме понятието формално за дискретни случайни величини; самата
характеризация чрез минимизация не зависи от това дали $Y$ е дискретна, но за непрекъснат случай
се налагат допълнителни технически тънкости.» (transcript [16:12]–[16:18]).

---

## F-03 — Change-of-variables theorem: strict monotonicity is not enough

- **Severity:** UNSOUND
- **Location:** `lectures/bodies/lecture_08.tex:306–311` (Теорема), proof `:321–350`

**What it says now.**

> «Нека $X$ е непрекъсната случайна величина, а $g:\mathbb{R}\to\mathbb{R}$ е строго монотонно
> растяща или строго монотонно намаляваща функция (поне в областта, където $X$ приема стойности с
> положителна плътност). Тогава $Y=g(X)$ е също непрекъсната случайна величина, чиято плътност се
> задава от формулата $f_Y(y) = f_X(g^{-1}(y))\left|(g^{-1}(y))'\right|$.»

**Why that is wrong.** Strict monotonicity alone does not give $Y$ a density, so the conclusion
«$Y$ е също непрекъсната случайна величина» is false. The formula also silently presumes $g^{-1}$
is differentiable — it appears inside the formula — which strict monotonicity does not deliver.
The failing case: let $C$ be the Cantor function, put

$$\psi(y)=\tfrac{1}{2}\big(y+C(y)\big)\quad\text{on }[0,1],$$

a continuous, strictly increasing bijection of $[0,1]$ onto itself, and let $g:=\psi^{-1}$ (extended
by the identity outside), which is continuous and strictly increasing. Take $X\sim U(0,1)$ and
$Y=g(X)$. Then $F_Y(y)=\mathbb{P}(X\le\psi(y))=\psi(y)$, which is **not** absolutely continuous:
$Y$ has no density at all, and half of its mass sits on the (Lebesgue-null) Cantor set. Meanwhile
$g^{-1}=\psi$ *is* differentiable almost everywhere with $\psi'=\tfrac12$ a.e. (because $C'=0$ a.e.),
so the theorem's right-hand side is defined a.e. and equals $1\cdot\tfrac12=\tfrac12$ — a function
whose integral over $(0,1)$ is $\tfrac12\neq1$. The formula returns a non-density.

**Verification.** Computed $C$ by base-3 expansion (depth 40) and $\psi=(y+C(y))/2$; then
central-differenced $\psi$ at 200 000 uniform random points with $h=10^{-7}$:

```
psi(0), psi(1) = 0.0, 1.0                       (so F_Y is a genuine CDF on [0,1])
empirical psi' : median = 0.500000,  99.32% of sample points within 1e-3 of 0.5
naive formula f_Y = f_X(psi(y))*|psi'(y)| = 1 * 1/2 = 1/2  on (0,1)
=> total mass returned by the theorem's formula = 0.5, must be 1  (deficit 0.5)
```

The missing half is the singular part carried by $C$.

**Two further gaps in the same statement.** (i) The formula is valid only for $y$ in the range of
$g$; for $y\notin g(\mathbb{R})$ the symbol $g^{-1}(y)$ is undefined and $f_Y(y)=0$. (ii) `:307`'s
parenthesis «(поне в областта, където $X$ приема стойности с положителна плътност)» is a correct
recovery of [141:00]–[141:52] — keep it — but it does not repair (i) or the differentiability gap.

Under **R1** the lecturer must not be silently corrected: he also said only «строго монотонно
растяща или намаляваща» ([138:50]). So the fix is a hypothesis plus a footnote, not a rewrite.

**Suggested fix.**

> Нека $X$ е непрекъсната случайна величина, а $g$ е строго монотонна и \emph{диференцируема} с
> $g'\neq 0$ в областта, където $X$ приема стойности с положителна плътност. Тогава $Y=g(X)$ е
> непрекъсната случайна величина и за всяко $y$ от множеството от стойности на $g$
> \[ f_Y(y) = f_X\big(g^{-1}(y)\big)\left|\big(g^{-1}(y)\big)'\right|, \]
> а $f_Y(y)=0$ извън това множество.

with a footnote: «На лекцията беше поискана само строга монотонност. Тя не е достатъчна:
съществува строго растяща непрекъсната $g$, за която $Y=g(X)$ няма плътност (образът на
канторовата функция носи половината от масата върху множество с мярка нула). Формулата и без това
съдържа $(g^{-1})'$, така че диференцируемостта е неявно предположена.»

---

## F-04 — «$F_X' = f_X$» is asserted globally; the lecturer said "почти навсякъде", and the book's own uniform example refutes it

- **Severity:** BROADENED (contradicts the book's own §"Равномерно разпределение")
- **Location:** `lectures/bodies/lecture_08.tex:262–265`, and the restatement at `:300`

**What it says now.**

> «Ако плътността $f_X$ е непрекъсната функция в дадена точка $x_0$, то от основната теорема на
> интегралното смятане следва, че производната на функцията на разпределение е равна на плътността:
> \[ \left.\frac{dF_X}{dx}\right|_{x=x_0} = f_X(x_0) \implies F_X' = f_X \]»

**Why that is wrong.** The hypothesis is local ("в дадена точка $x_0$"); the conclusion after the
`\implies` is global and unqualified. The lecturer said the opposite in the same breath:

> [132:45] «плътността е производната на функцията на разпределение … в класически смисъл е хубаво
> да имате непрекъсната, с нея да си направите съответното доказателство, че производната е равна
> на плътността»
> [133:03] «**но тя, значи, е почти навсякъде равна** — няма смисъл да влизаме в такива детайли»

The counterexample is two pages later in this very chapter: the uniform density at `:438` is
$f_X=1/(b-a)$ on $[a,b]$, i.e. $f_X(a)=f_X(b)=1/(b-a)\ne 0$, while the uniform $F_X$ at `:448` has no
derivative at $a$ or at $b$. So $F_X'=f_X$ fails at both endpoints of the chapter's own first example.
The board (`board_056.json`, t = 133.3 min) does carry the bare line `F_X' = f_X`, but the spoken
qualifier that immediately followed it was dropped — exactly the failure mode R3 warns about.

**Verification (sympy, $a=0$, $b=1$, book's own piecewise $F$):**

```
x=0: right-derivative = 1   left-derivative = 0   -> F'(0) does not exist
x=1: right-derivative = 0   left-derivative = 1   -> F'(1) does not exist
f(0) = f(1) = 1
```

**Suggested fix.** Replace the display's trailing implication and add the caveat:

> \[ \left.\frac{dF_X}{dx}\right|_{x=x_0} = f_X(x_0) \]
> Следователно във всяка точка на непрекъснатост на $f_X$ плътността е производна на функцията на
> разпределение. В общия случай равенството $F_X'=f_X$ е вярно само \emph{почти навсякъде}: за
> равномерното разпределение по-долу $F_X$ не е диференцируема в краищата $a$ и $b$, макар
> плътността там да е $1/(b-a)$.

---

## F-05 — $\mathbb{P}(X=c)=0$ is "derived" outside the scope of the definition; the lecturer's proof is gone

- **Severity:** UNSOUND (the justification does not follow from the stated definition)
- **Location:** `lectures/bodies/lecture_08.tex:225–232`

**What it says now.**

> «От свойствата на интеграла веднага следва, че вероятността $X$ да приеме точно една конкретна
> стойност $c$ е нула: $\mathbb{P}(X = c) = \int_{c}^{c} f_X(x)\,dx = 0$»

**Why that is wrong.** Clause 3 of the definition at `:216` licenses $\mathbb{P}(X\in(a,b))=\int_a^b f_X$
only «За всеки две числа $a<b$». The set $\{X=c\}$ is not an interval $(a,b)$ with $a<b$, so the first
equality is not an instance of the definition — the step assumes what it is proving. Nothing in the
chapter connects a null interval to a null point event.

The lecturer stated this as a твърдение and proved it properly, by monotonicity plus a limit:

> [124:30] «Събитието $X$ … за които $X(\omega)=c$ се влага в събитието $X$ да е по-малко от
> $c+1/n$ и $X$ да е по-голямо от $c-1/n$ … и това е вярно за всяко $n$»
> [125:20] «Понеже вероятността е монотонна … $\mathbb{P}(X=c)\le \mathbb{P}(X\in(c-1/n,c+1/n))$,
> което е по дефиниция интеграл … лявата страна не зависи от $n$, а дясната зависи от $n$, можем да
> устремим $n$ към безкрайност»

`run/lecture_08/ocr/board_055.json` (t = 126.5 min) carries the whole thing, statement and proof:

```
Тв: Нека X е непр. с.в. и c ∈ R. Тогава P(X=c)=0 и следователно за a<b,
    P(X∈(a,b)) = P(a<X<b) = P(a<X≤b) = P(a≤X<b) = P(a≤X≤b) = P(X∈[a,b)) = P(X∈[a,b])
Д-во: {X=c} ⊆ {c-1/n < X < c+1/n}  ∀n≥1
      P(X=c) ≤ P(X ∈ (c-1/n, c+1/n)) =(деф) ∫_{c-1/n}^{c+1/n} f_X(x)dx
      P(X=c) ≤ lim_{n→∞} ∫_{c-1/n}^{c+1/n} f_X(x)dx = ∫_c^c f_X(x)dx = 0
```

He also proved the interval-endpoint chain at `:231` by decomposing
$\{a<X\le b\}=\{a<X<b\}\cup\{X=b\}$ ([127:00]). The book asserts the chain with no argument.

**Verification.** No numerical check needed; this is a scope error in a citation of the book's own
definition. Cross-checked that clause 3 at `:216` indeed says «За всеки две числа $a<b$» — it does.

**Suggested fix.** Promote to a `prop` with the lecturer's proof:

> **Твърдение.** Нека $X$ е непрекъсната случайна величина и $c\in\mathbb{R}$. Тогава
> $\mathbb{P}(X=c)=0$.
> *Доказателство.* За всяко $n\ge 1$ имаме влагането
> $\{X=c\}\subseteq\{c-\tfrac1n<X<c+\tfrac1n\}$, откъдето по монотонност на вероятността и по
> дефиниция
> \[ \mathbb{P}(X=c)\ \le\ \mathbb{P}\!\left(X\in\left(c-\tfrac1n,\,c+\tfrac1n\right)\right)
>    = \int_{c-1/n}^{c+1/n} f_X(x)\,dx . \]
> Лявата страна не зависи от $n$, затова можем да устремим $n\to\infty$:
> $\mathbb{P}(X=c)\le\int_c^c f_X = 0$. $\square$
>
> **Следствие.** За $a<b$ всички интервали дават една и съща вероятност, защото
> $\{a<X\le b\}=\{a<X<b\}\cup\{X=b\}$ е обединение на непресичащи се събития, второто от които е с
> вероятност нула.

---

## F-06 — Tower law with no integrability hypothesis, and an unjustified double interchange of $\E$ with an infinite sum

- **Severity:** UNSOUND
- **Location:** `lectures/bodies/lecture_08.tex:92–93` (Твърдение, точка г)), proof `:111–118`

**What it says now.**

> «г) **Повторно очакване (Закон за пълното математическо очакване):** $\E[\E[X \given Y]] = \E X$.»

with no condition on $X$ anywhere in `prop:cond-exp-props` (`:86–97`), and a proof that moves $\E$
inside an infinite sum at `:115` and back out at `:117` without comment.

**Why that is wrong.** The identity is an equality between two things, one of which may not exist.
Concrete failing case: let $\mathbb{P}(Y=j)=2^{-j}$ for $j=1,2,\dots$, and conditionally on $Y=j$ let
$X=\pm j2^{j}$ with probability $\tfrac12$ each. Then $\E[X\given Y=j]=0$ for every $j$, so
$\E[X\given Y]\equiv0$ and the left-hand side is $0$; but $\E|X|=\infty$, so $\E X$ does not exist and
the right-hand side is meaningless. The chapter's own definition of $\E X$ for the continuous case
at `:401` *does* carry the condition $\int|x|f_X<\infty$ — so the omission here is inconsistent even
internally.

**Verification (sympy).**

```
sum_j P(Y=j) = 1                       (it is a genuine distribution)
E[X|Y=j] = 0 for every j  ->  E[E[X|Y]] = 0
E|X| = sum_j (j*2^j)*2^-j = oo         partial sums: N=10 -> 55, N=100 -> 5050, N=1000 -> 500500
```

**Suggested fix.** Add the hypothesis to the head of `prop:cond-exp-props` (`:86`), which also covers
а):

> **Твърдение (свойства на условното математическо очакване).** Нека $\E|X|<\infty$ и $\E|Z|<\infty$,
> а $Y$ е дискретна случайна величина. Тогава …

and in the proof of г) add one clause at `:115`: «Разместването на очакването и сумата е допустимо,
защото $\sum_j \E\big|X\ind_{A_j}\big| = \E|X| < \infty$ (теорема на Фубини–Тонели за редове).»

---

## F-07 — Example `ex:08-2` drops its punchline: the whole point was $\E[X\given Y=0]=2/5$

- **Severity:** LOST
- **Location:** `lectures/bodies/lecture_08.tex:162–181` (`Example ex:08-2`), which stops at `:179`

**What it says now.** The example computes the conditional distribution $16/25, 8/25, 1/25$ and then
goes straight to the "5-sided die" intuition. It never computes the conditional expectation.

**Why that is wrong.** The lecturer's reason for doing this example at all was to show that the
conditional distribution gives a *second route* to the conditional expectation of §1:

> [83:20] «И ако искате да пресметнете очакването на X при положение $Y$ равно на нула, веднъж може
> да го направите по начина, по който аз бях направил в предходната лекция. Другият начин е просто
> да използвате тази формула … Това е $16/25$ по $0$, $8/25$ по $1$ и $1/25$ по $2$ … ми се струва,
> че е $10/25$, или [две пети].»
> [84:00] «Т.е. това ни дава алтернативен начин да си пресметнете условното математическо очакване
> — просто да си намерите разпределението на $X$ при условие $Y$. Но тук става дума за условното
> математическо очакване при конкретна стойност на $Y$. А оттам нататък … да си изградите
> условното математическо очакване на $X$ при положение $Y$, с което стартирахме.»

That last sentence is precisely the $\E[X\given Y=y]$-versus-$\E[X\given Y]$ distinction the chapter
is built around, and it is the only place in the chapter where the two are connected by a worked
number. Both the number and the remark are gone.

**Verification.** Full enumeration of the 36 outcomes (sympy/Fraction) reproduces the book's table
exactly and gives

```
P(Y=0) = 25/36 ;  P(X=x|Y=0) = {0: 16/25, 1: 8/25, 2: 1/25}
E[X|Y=0] = 0*16/25 + 1*8/25 + 2*1/25 = 10/25 = 2/5 = 0.4
```

(and, from F-02, $\E[X\given Y=1]=1/5$, $\E[X\given Y=2]=0$.)

**Suggested fix.** Append to the example, after `:179`:

> Оттук получаваме и условното математическо очакване при тази конкретна стойност:
> \[ \E[X\given Y=0] = 0\cdot\frac{16}{25} + 1\cdot\frac{8}{25} + 2\cdot\frac{1}{25}
>   = \frac{10}{25} = \frac{2}{5}. \]
> Това е втори път до същото число: веднъж през дефиницията от §1, и веднъж — както тук — през
> условното разпределение. Аналогично $\E[X\given Y=1]=1/5$ и $\E[X\given Y=2]=0$, а от тези три
> числа се сглобява \emph{случайната величина}
> $\E[X\given Y] = \tfrac25\ind_{\{Y=0\}} + \tfrac15\ind_{\{Y=1\}}$.

---

## F-08 — The mixture example hides the fact that $X$ and $Y$ are *not* independent

- **Severity:** LOST
- **Location:** `lectures/bodies/lecture_08.tex:125–144` (`Example ex:08-1`, "Смес от разпределения")

**What it says now.** The example introduces $X\sim\Ber(Y)$ and computes
$\E[X\given Y=2/3]=2/3$, $\E[X\given Y=1/3]=1/3$ without a word about the dependence between $X$ and $Y$.

**Why that is wrong.** In the lecture this was the one point that cost real time. The lecturer first
assumed independence, then retracted it on air:

> [65:25] «Не е необходимо $X$, априори, да е независимо от $Y$, но ние ще допуснем, че $X$ и $Y$ са
> независими.»
> …
> [71:18] «Какъв е случаят? То $X$ не е взето независимо от $Y$, защото като зафиксирате $Y$, то
> [това ви казва нещо] върху $X$, така че това, което написах тук, **не беше коректно** … Така че
> това нещо беше абсолютно излишно, **даже бих казал напълно грешно**.»
> [71:42] «Това, което си имах предвид, е простото нещо, че ако $Y$ е равно на 2/3, то $X$ е
> Бернулиево с 2/3.»

The board records the corrected version: `run/lecture_08/ocr/board_031.json` (t = 69.9 min) has the
line `X \not\perp\!\!\!\perp Y` — explicitly *dependent*.

This matters mathematically, not just historically. Point д) of `prop:cond-exp-props` (`:94–95`) is
the only tool in the property list that evaluates $\E[f(X,Y)\given Y=y_j]$, and it **requires**
$X\perp\!\!\!\perp Y$. A reader who reaches for it here gets the wrong answer. The step
$\E[X\given Y=2/3]=2/3$ holds by *construction of the mixture* (that is what "given $Y=2/3$, $X$ is
Bernoulli(2/3)" means), not by any property in the list.

**Verification (sympy).** $\E[\E[X\given Y]] = \tfrac23 p + \tfrac13(1-p) = \tfrac{p}{3}+\tfrac13$;
checks at the endpoints $p=1\Rightarrow 2/3$ and $p=0\Rightarrow 1/3$, as it must. Independence of
$X$ and $Y$ would force $\mathbb{P}(X=1\given Y=2/3)=\mathbb{P}(X=1)=\tfrac{p}{3}+\tfrac13$, which
equals $2/3$ only at $p=1$ — so $X\not\perp\!\!\!\perp Y$ for every $p\in(0,1)$, confirming the board.

**Suggested fix.** Insert after `:133`:

> Да отбележим веднага, че тук $X \not\perp\!\!\!\perp Y$ — точно това е смисълът на смесите:
> стойността на $Y$ променя разпределението на $X$. Затова свойство д) от
> Твърдение~\ref{prop:cond-exp-props} \emph{не} е приложимо; равенствата
> $\E[X\given Y=2/3]=2/3$ и $\E[X\given Y=1/3]=1/3$ следват направо от построението на модела —
> условното разпределение на $X$ при $Y=y$ е $\Ber(y)$.

---

## F-09 — `keydefn` omits $\mathbb{P}(Y=y_j)>0$, which the lecturer stated explicitly

- **Severity:** UNSOUND (division by zero) / LOST
- **Location:** `lectures/bodies/lecture_08.tex:57–63`

**What it says now.**

> «Нека $X$ и $Y$ са дискретни случайни величини. Условното математическо очакване на $X$ при
> условие, че $Y$ е приело конкретната стойност $y_j$ … $\E[X \given Y=y_j] = \sum_i x_i
> \mathbb{P}(B_i \given A_j)$»

**Why that is wrong.** $\mathbb{P}(B_i\given A_j)$ is undefined when $\mathbb{P}(A_j)=0$, and the
indicator representation used in every proof divides by $\mathbb{P}(A_j)$. The lecturer spelled the
condition out at the point of definition:

> [27:45] «Аз не казвам за кои $y_j$ … ясно е, че трябва да вземете възможна стойност на $Y$, а не
> някакво число, което $Y$ не може да приема … т.е. **има положителна вероятност** да приеме тази
> конкретна стойност.»

The book *does* state it two sections later, for the conditional distribution (`:151`: «за всяка
възможна стойност на $Y$ с $\mathbb{P}(Y=y_j)>0$»), which makes the omission in the keydefn look like
an oversight rather than a choice. The same clause is also missing from the sum over $j$ at `:67` and
from the distribution table at `:76`.

**Suggested fix.** `:58` → «Нека $X$ и $Y$ са дискретни случайни величини и нека $y_j$ е стойност на
$Y$ с $\mathbb{P}(Y=y_j)>0$. Условното математическо очакване … (сумата се предполага абсолютно
сходяща, което е изпълнено при $\E|X|<\infty$)». At `:67` add «където сумирането е по всички $j$ с
$\mathbb{P}(A_j)>0$».

---

## F-10 — $\E[g(X)]=\int g f_X$ carries no integrability condition, and the derivation the lecturer gave is replaced by "следва интуитивно"

- **Severity:** UNSOUND + LOST
- **Location:** `lectures/bodies/lecture_08.tex:415–418`

**What it says now.**

> «Ако искаме да пресметнем математическото очакване на функция от случайната величина $g(X)$, не е
> необходимо първо да намираме плътността на $Y=g(X)$. Използваме директната формула (която се
> доказва строго чрез теория на мярката, но следва интуитивно от току-що доказаната теорема за
> смяна на променливите): $\E[g(X)] = \int_{-\infty}^{\infty} g(x) f_X(x)\,dx$»

**Why that is wrong.** Two defects, and this is the same pattern as the Твърдение 9.7 example in the
brief.

(i) No condition on $g$ at all. The definition of $\E X$ eleven lines above (`:401`) correctly requires
$\int|x|f_X<\infty$; here the analogous $\int|g(x)|f_X(x)\,dx<\infty$ is dropped, so as written the
formula asserts the existence of $\E[g(X)]$ for any $g$ whatsoever. The lecturer stated the condition
for $\E X$ ([149:30] «и интеграл от минус безкрайност до безкрайност модул $x$ $f(x)\,dx$ е краен,
то очакването на $X$ е …») and then said only «по-общо … ако имате произволна функция $g$»
([152:00]) — so a footnote, not a silent correction, is the R1-compliant route for the wording; but
the finiteness condition itself is his, stated one minute earlier for the same construct.

(ii) The chapter says the formula «следва интуитивно» from the change-of-variables theorem and leaves
it there. The lecturer actually *carried out* that derivation on the board for increasing $g$:

> [153:00] «аз ще го направя в случая, когато $g$ е растяща … Тогава очакването на $Y$ е интеграл
> от минус безкрайност до безкрайност — това вече е дефиниция — $y$ по плътността на $Y$ … от
> предходната теорема ние знаем каква е плътността … и сега сменяме променливите, като поставим
> $y=g(v)$ … $g^{-1}(g(v))$ е просто $v$, и тук имате $(g^{-1})'(g(v))\cdot g'(v)\,dv$ … Е, сега
> това нещо е единица … Защото $v = g^{-1}(g(v))$, и вземете производни по $v$, използвайте
> производна за съставна функция.»

**Verification (sympy).** Reproduced the chain-rule step symbolically: for $g$ strictly increasing
and differentiable, $\frac{d}{dv}g^{-1}(g(v)) = (g^{-1})'(g(v))\,g'(v) = 1$, so the substitution
$y=g(v)$ turns $\int y f_Y(y)\,dy$ into $\int g(v) f_X(v)\,dv$. Checked numerically on
$X\sim U(0,1)$, $g(x)=e^{x}$: $\int_0^1 e^{x}\cdot 1\,dx = e-1 = 1.718282$, and
$\int_1^e y\cdot f_Y(y)\,dy$ with $f_Y(y)=1/y$ on $(1,e)$ gives $e-1 = 1.718282$. Equal.

**Suggested fix.**

> Ако $\int_{-\infty}^{\infty}|g(x)| f_X(x)\,dx<\infty$, то
> \[ \E[g(X)] = \int_{-\infty}^{\infty} g(x) f_X(x)\,dx . \]
> В пълна общност това е следствие от дефиницията на интеграла в смисъла на теория на мярката. За
> строго растяща и диференцируема $g$ обаче то следва направо от теоремата за смяна на
> променливите: по дефиниция $\E Y = \int y f_Y(y)\,dy$, а $f_Y(y)=f_X(g^{-1}(y))(g^{-1}(y))'$;
> субституцията $y=g(v)$ дава
> \[ \E Y = \int g(v)\, f_X(v)\, \underbrace{(g^{-1})'(g(v))\,g'(v)}_{=\,1}\,dv
>        = \int g(v) f_X(v)\,dv, \]
> където подчертаният множител е единица по правилото за производна на съставна функция, приложено
> към тъждеството $v = g^{-1}(g(v))$.

---

## F-11 — The deliberate abuse of the term "непрекъсната" is not recorded

- **Severity:** LOST
- **Location:** `lectures/bodies/lecture_08.tex:211–221` (`defn` "Абсолютно непрекъсната случайна величина")

**What it says now.** The environment is titled «Абсолютно непрекъсната случайна величина» and its
first sentence reads «Случайната величина $X$ се нарича **непрекъсната**, ако съществува неотрицателна
функция $f_X$ …». The mismatch between title and text is left unexplained.

**Why that is wrong.** The lecturer gave two different definitions and warned, at length, that they
are *not* equivalent and that he is knowingly conflating them:

> [99:15] «която аз ще дам [като] втора дефиниция. **Тя формално не е еквивалентна на първата**, но
> във вашия курс се третира като еквивалентна. Защото [не] знаем достатъчно анализ, за да може да
> говорим за **сингулярно непрекъснати** случайни величини.»
> [99:40] «така че аз тук за първи и последен път ще дефинирам $X$ като абсолютно непрекъсната, но
> винаги ще говоря за непрекъсната»
> [100:00] «но ще се разбира непрекъсната в този курс, така ще се казва, но това е … **abusive
> notation**, защото не е точно същото, но за да не се затрудняват студентите, се казва така»

The first definition was the "uncountably many values" one at [93:50]–[94:30], which the book keeps
only as motivation prose at `:203` without flagging that it is a *different* notion. Per the book's
own convention list, a footnote is the sanctioned way to record this; there is none.

**Suggested fix.** Add a footnote on the word «непрекъсната» at `:212`:

> \footnote{Строго погледнато дефинираме \emph{абсолютно} непрекъсната случайна величина. В курса
> ще казваме просто «непрекъсната», както направи и лекторът, отбелязвайки, че това е съзнателна
> неточност: съществуват случайни величини с неизброимо много стойности и без атоми, които
> въпреки това не притежават плътност (сингулярно непрекъснати). Те изискват анализ извън обхвата
> на курса.}

---

## F-12 — The converse characterisation of a density is used to close the change-of-variables proof but is never stated

- **Severity:** LOST
- **Location:** used at `lectures/bodies/lecture_08.tex:349`; belongs after `:232`

**What it says now.** The proof ends:

> «Тъй като вероятността $\mathbb{P}(Y \in (a, b))$ се пресмята чрез интеграл над интервала $(a,b)$
> от тази конкретна функция, то по дефиниция подинтегралната функция е именно търсената плътност на
> $Y$.»

The same reasoning is the premise at `:322`: «Търсим функция $f_Y$, която при интегриране над
произволен интервал $(a,b)$ да дава вероятността».

**Why that is wrong.** The definition at `:211–221` reads in one direction only: *if* a density exists
*then* probabilities are its integrals. The proof needs the converse — if a non-negative $h$ satisfies
$\mathbb{P}(X\in(a,b))=\int_a^b h$ for **all** $a<b$, then $X$ is continuous with density $h$. That
converse is true, and the lecturer deliberately stated it as a separate remark immediately before the
theorem, precisely so that the proof could invoke it:

> [133:38] «тук искам да направим няколко забележки …»
> [134:22] «вие знаете, че $X$ е непрекъсната, но не знаете плътността … и тогава вие имате в някакъв
> смисъл **обратната задача** — вие търсите функция, чрез която може да изчислявате вероятностите
> на $X$»
> [135:00] «И ако намерите такава функция, тя ви е вашата плътност. Ако това е вярно за всяко $a$
> по-малко от $b$ … ако може да изчислявате нейната вероятност за всеки $a$ и $b$ чрез конкретен
> интеграл от една единствена функция, **тази функция е нейната плътност**.»

He also made the framing point that the density then replaces the probability space entirely
([134:00] «вие в някакъв смисъл не се нуждаете от вероятностното пространство»). All of this is absent.

**Suggested fix.** Add a short remark after `:232` and cite it at `:349`:

> **Забележка (обратната задача).** Дефиницията се чете и в обратна посока. Ако $h\ge 0$ и за
> \emph{всеки} две числа $a<b$ е изпълнено $\mathbb{P}(X\in(a,b)) = \int_a^b h(x)\,dx$, то $X$ е
> непрекъсната с плътност $f_X = h$. Това е обичайният начин да се \emph{намери} плътност: не се
> тръгва от вероятностното пространство, а се търси една функция, чиито интеграли възпроизвеждат
> вероятностите. Точно по този начин ще завършим доказателството на теоремата за смяна на
> променливите по-долу.

---

## F-13 — The third motivation for continuous variables — the limit theorems — is dropped

- **Severity:** LOST
- **Location:** `lectures/bodies/lecture_08.tex:203–207` (§"Въведение и мотивация")

**What it says now.** Two reasons are given: storage efficiency (`:206`) and the fact that one usually
wants interval probabilities (`:207`).

**Why that is wrong.** The lecturer gave three, and called the third one the most pervasive:

> [98:00] «много често, а **практически винаги в нашия курс** — може би с изключение на теоремата на
> Поасон — граничните теореми са свързани с непрекъснати случайни величини. Т.е. вие в границата
> имате непрекъсната случайна величина и тя … тази неизброимост може и да не може да се реализира,
> но тя ви дава изключително добро приближение. Ние ще говорим за централната гранична теорема.»
> [98:30] «Централната гранична теорема има наистина забележителното свойство, че [за] огромен клас
> случайни величини … вие може да ги приближавате изключително точно просто с една табличка, дори
> не ви трябва суперкомпютър.»

This is the motivation that actually pays off later in the book (the normal approximation and the
$z$/$t$ tables in appendix Б), so its loss is not merely rhetorical.

**Suggested fix.** Add a third paragraph at `:207`:

> Третата и може би най-важната причина е, че непрекъснатите случайни величини се появяват като
> \emph{граници}. Почти всички гранични теореми в курса — с изключение на теоремата на Поасон —
> имат непрекъсната граница: дори когато изходният модел е дискретен, централната гранична теорема
> позволява той да бъде приближен с нормално разпределение изключително точно. Вместо огромен
> масив от вероятности е достатъчна една таблица.

---

## F-14 — The non-monotone case is illustrated only by the degenerate example

- **Severity:** UNCLEAR (minor)
- **Location:** `lectures/bodies/lecture_08.tex:313–319` (`supp:monotone-needed`)

**What it says now.**

> «Без нея твърдението пропада напълно: трансформация на непрекъсната величина може да бъде
> дискретна. Нека $X$ е произволна непрекъсната величина и $g(x) = \ind_{\{x \ge 0\}}$ …»

This faithfully recovers the lecturer's own example ([137:30]–[138:10]), so it is not a fidelity
defect. But «пропада напълно» overstates the situation in the case a reader will actually meet.

**Why it matters.** For a non-monotone but piecewise-monotone $g$, $Y$ normally *does* have a density;
what fails is only the single-branch formula, which must be replaced by a sum over the preimages
$g^{-1}$ restricted to each monotone branch. The canonical instance is $g(x)=x^2$, and the book needs
exactly that instance in `bodies/lecture_09.tex:703` ($Z_1^2\sim\chi^2(1)$) — where it is done from
scratch through the CDF rather than by a stated rule. No downstream error results, but the reader
leaves L08 believing non-monotone $g$ is hopeless.

**Verification (sympy + scipy + simulation).** With $X\sim N(0,1)$ and $Y=X^2$, applying the
theorem's formula to the single branch $g^{-1}(y)=\sqrt y$:

```
naive f_Y(y) = sqrt(2) e^{-y/2} / (4 sqrt(pi) sqrt(y))
  integral over (0, oo) = 1/2                 <- not a density
true chi2(1) density = 2 * naive,  integral = 1
scipy chi2.pdf(1.7, 1) = 0.13077818192388813  ==  2*naive at y=1.7 = 0.1307781819238881
simulation (2e6 draws of Z^2): P(Y<1.7) = 0.80838  vs  chi2.cdf(1.7,1) = 0.80771
```

so the single-branch formula gives exactly half the correct density — the two branches
$\pm\sqrt y$ each contribute one half.

**Suggested fix.** Extend the `supp` with a second paragraph:

> В по-мекия и много по-често срещан случай — $g$ е монотонна на всяко от няколко парчета — $Y$
> все пак има плътност, но формулата трябва да се сумира по всички клонове:
> \[ f_Y(y) = \sum_{k} f_X\big(g_k^{-1}(y)\big)\left|\big(g_k^{-1}(y)\big)'\right|, \]
> където $g_k$ са ограниченията на $g$ върху интервалите, на които е строго монотонна. За
> $g(x)=x^2$ клоновете са $\pm\sqrt{y}$ и всеки дава по половината от плътността; прилагането на
> формулата само с един клон дава точно два пъти по-малко от вярното. Оттам и
> $Z^2\sim\chi^2(1)$ за $Z\sim N(0,1)$ — извеждането е в лекция 9.

---

## F-15 — Minor, but real

Grouped because each is a one-line fix; all verified.

**(a) The motivation divides by $\mathbb{P}(A)$ and $\mathbb{P}(A^c)$ with no assumption $0<p<1$.**
`:36`, `:39`, `:41`. If $p\in\{0,1\}$ one of the two quotients is $0/0$, and the claim at `:41`
«квадратична форма с положителен хесиан» fails: the Hessian is
$\operatorname{diag}(2\mathbb{P}(A),\,2\mathbb{P}(A^c))$, which is positive definite iff
$0<p<1$ and merely semi-definite otherwise. Verified by hand from `:32`. Fix: at `:22` write «Нека
вероятностите са съответно $\mathbb{P}(Y=1)=\mathbb{P}(A)=p\in(0,1)$ и …», and at `:41` «положително
определен хесиан $\operatorname{diag}(2\mathbb{P}(A),2\mathbb{P}(A^c))$ (за $0<p<1$)».

**(b) The distribution table at `:70–80` is not a distribution table if two values of $Y$ share a
conditional expectation.** If $\E[X\given Y=y_1]=\E[X\given Y=y_2]$, the value's probability is
$p_1+p_2$, not $p_1$ and $p_2$ separately. The lecturer said the same thing ([30:43] «а вероятностите
са същите като на $Y$»), so under R1 this is footnote territory, not a correction: «Ако две различни
стойности на $Y$ дават една и съща условна очаквана стойност, съответните вероятности се сумират.»

**(c) `def:var-continuous` (`:408–413`) has no finiteness condition,** although the definition of
$\E X$ directly above it (`:401`) does. Fix: «Ако $\int x^2 f_X(x)\,dx<\infty$, то …».

**(d) `prop:exp-var-props` (`:420–430`) states linearity, $\Var(aX)=a^2\Var X$ and
$\E[XY]=\E X\,\E Y$ with no existence hypotheses** — same class as F-06, and the lecturer's own list
([156:00]–[157:30]) was equally informal. Fix: one lead-in clause «(предполагаме, че съответните
очаквания съществуват)». The lecturer also noted, in the same breath, that a continuous random
variable cannot be a constant, so «$\E c = c$» is inherited from the discrete case ([156:10] «ако $X$
… е непрекъсната случайна величина, тя не може да бъде константа, но все пак ще припомня, че
очакването на константа е константа. Това е за дискретна случайна величина по принцип») — worth the
same parenthesis.

**(e) `:185` says the multinomial has «$r \ge 1$ възможни изхода».** The lecturer explicitly ruled the
degenerate case out: [86:30] «Определено $r$ не е единица, защото това е само един възможен изход.
$r$ равен на 2 ще бъде биномно». Not false — with $r=1$ the formula returns 1 — but broader than what
was said. Fix: «$r \ge 2$ възможни изхода (при $r=1$ моделът е изроден, а при $r=2$ се връщаме към
биномното)».

---

## Checked and found sound

Everything below was checked against the transcript and/or computed, and is correct as it stands.

- **§Мотивация, the binary derivation (`:15–51`).** The expansion
  $f(a,b)=\E[X^2+a^2\ind_A+b^2\ind_{A^c}-2aX\ind_A-2bX\ind_{A^c}]$, both partial derivatives, and both
  solutions $a=\E[X\ind_A]/\mathbb{P}(A)=\E[XY]/\mathbb{P}(Y=1)$,
  $b=\E[X\ind_{A^c}]/\mathbb{P}(A^c)=\E[X(1-Y)]/\mathbb{P}(Y=0)$ match `board_006.json` line for line.
  The specialisation $X=\ind_B \Rightarrow G^*(Y)=\mathbb{P}(B\given A)\ind_A+\mathbb{P}(B\given A^c)\ind_{A^c}$
  matches `board_009/011.json`. $\Var X = \min_a \E(X-a)^2$ verified symbolically
  ($\E(X-a)^2 = \Var X + (\E X - a)^2$, minimised at $a=\E X$).
- **The $\E[X\given Y]$ / $\E[X\given Y=y_j]$ distinction is kept properly** throughout (`:60` vs `:65–68`,
  `:95`, `:151–158`). This is the chapter's main hazard and the book handles it correctly — including
  the `\ind_{A_j}` assembly at `:67`, which is exactly `board_015/016.json`.
- **Property д) has the expectation on the right-hand side.** `board_028.png` (read directly) shows the
  lecturer wrote «$\E[f(X,Y)\mid Y=y_0] = f(x;y_0)$» — *without* the outer $\E$ — and corrected himself
  aloud at [63:32]–[64:04] («тук трябва да имаме очакването … ако нямах очакването, това е случайна
  величина»). The book prints the corrected form $\E[f(X,y_j)]$. Correct.
- **All five properties in `prop:cond-exp-props` are the lecturer's five**, in his order: linearity
  [35:05], independence [38:23] (with the tool $\E[f(X)g(Y)]=\E f(X)\E g(Y)$, `board_019.json`),
  $X=f(Y)$ [41:51], tower [60:08]/`board_027.json`, substitution [62:43]/`board_028.json`. His board
  letters run а), б), в), г), е) — he skipped д) himself; nothing is missing, and no sixth property
  exists in either the transcript or the boards.
- **Proof of б)** — the collapse $\E X\sum_j\ind_{A_j}=\E X$ via "пълна група от събития" matches
  [41:04]–[41:22].
- **Example `ex:08-1` (mixture) arithmetic.** $\E[\E[X\given Y]] = \tfrac23 p + \tfrac13(1-p)$, verified
  symbolically; endpoints $p=1\to 2/3$, $p=0\to 1/3$. Matches `board_033.json`. (See F-08 for the
  missing dependence remark — the arithmetic itself is right.)
- **Example `ex:08-2` joint table.** All six entries verified by enumerating the 36 outcomes:
  $16,8,1/8,2,0/1,0,0$ over 36, summing to 1; $\mathbb{P}(Y=0)=25/36$; conditionals $16/25,8/25,1/25$;
  and the "5-sided die" intuition $(4/5)^2, 2\cdot\tfrac15\cdot\tfrac45, (1/5)^2$ is exactly right.
- **Multinomial section (`:183–198`).** The pmf $\frac{n!}{k_1!\cdots k_r!}p_1^{k_1}\cdots p_r^{k_r}$,
  the telescoping product of binomial coefficients, and the $r=2$ reduction all match
  [88:30]–[92:20] and are correct.
- **`Example ex:08-3` (insurance).** Verified with sympy:
  $\int_{1/10}^{1} 5(1-x)^4\,dx = 59049/100000 = (9/10)^5 = 0.59049$, so the book's «$\approx 0{,}59$»
  is right; the board (`board_048–052.json`) shows the same, and the lecturer's spoken «0,60» at
  [107:20] was self-corrected to «записано 0,59».
- **The interval-endpoint chain at `:231`** ($\mathbb{P}(a<X<b)=\dots=\mathbb{P}(a\le X\le b)$) is
  correct, and matches `board_055.json` exactly — only its justification is at issue (F-05).
- **$F_X(x)=\mathbb{P}(X<x)=\int_{-\infty}^{x}f_X(y)\,dy$ (`:257–260`)** — consistent with the book's
  strict-inequality convention and with `board_056.json`. The «$dy$ като мярка» remark at `:261`
  faithfully recovers a real digression ([130:10]–[131:40]).
- **The change-of-variables proof body (`:321–350`)** is correct in both branches, including the
  reversal of the integration limits in the decreasing case and the identification
  $-(g^{-1})' = |(g^{-1})'|$; it matches `board_060.json` (`g^↑` / `g^↓` branches) and
  [143:00]–[148:00]. The defects are in the hypotheses (F-03) and in the unstated converse (F-12),
  not in the algebra.
- **`supp:max-min`.** Verified symbolically and by simulation. Differentiating $F^n$ and
  $1-(1-F)^n$ in sympy returns exactly $nF^{n-1}f$ and $n(1-F)^{n-1}f$. For the exponential
  minimum with distinct rates $\lambda=(0.7,1.3,2.5)$, 400 000 draws give
  $\E m = 0.22234$ against $1/\sum\lambda_j = 0.22222$ and
  $\mathbb{P}(m>0.5)=0.10527$ against $e^{-0.5\sum\lambda_j}=0.10540$; the min's mean and standard
  deviation coincide (0.2223 / 0.2222), as they must for an exponential, while the max's do not
  (1.7469 / 1.3456) — so the parenthetical «(Максимумът не е.)» is right. The L12 cross-reference
  also checks out: 300 000 draws of $\max_j X_j$ for $X_j\sim U(0,3)$, $n=6$, give
  $\mathbb{P}(\max<2.1)=0.11714$ against $(2.1/3)^6=0.11765$. Note this is `supp` material, so its absence from the lecture is not a
  defect; the mathematics is sound. One small imprecision worth knowing about but not worth a finding
  under this book's strict-inequality convention: $\{m\ge x\}=\bigcap_j\{X_j\ge x\}$ is written with
  $\ge$ while $F$ is defined with $<$, and the step is legitimate only because
  $\mathbb{P}(X_j = x)=0$ for continuous $X_j$ — which is exactly the chapter's own
  $\mathbb{P}(X=c)=0$ result.
- **§Равномерно разпределение (`:432–455`).** Density, the check $\int_a^b \frac{dx}{b-a}=1$, and the
  three-branch CDF are all correct under the $F(x)=\mathbb{P}(X<x)$ convention ($F(a)=0$, $F(b)=1$
  both hold), and match [159:00]–[163:40]. (It is this $F$ that refutes `:264` — see F-04.)
- **§Задачи (`:459–466`).** Both exercises are genuine lecture assignments: task 1 ($Y=aX+b$ via the
  change-of-variables theorem) from [158:10], task 2 (verify $\frac{1}{b-a}\ind_{[a,b]}$ is a density)
  from [159:30].
- **No finding here duplicates a rejected item.** `docs/REMEDIATION.md` §8 rejects D-01 (L02 axioms),
  D-02 (relocating L15) and reclassifies D-03 (exercises); §7 D-06 (whether to split L08) is an
  editorial decision, not a mathematical defect, and is untouched above.
