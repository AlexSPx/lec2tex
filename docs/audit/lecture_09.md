# Mathematics audit — `lectures/bodies/lecture_09.tex`
*«Непрекъснати разпределения. Гама и хи-квадрат разпределение»*

Sources used: `run/lecture_09/audio/transcript.json` (primary), `run/lecture_09/ocr/board_0NN.json`
(boards 009, 013–016, 022–032), `lectures/bodies/formulas.tex`, `lectures/bodies/lecture_08.tex`,
`docs/REMEDIATION.md` §0–2 and §8. All numeric/symbolic claims were re-derived with
`.venv/bin/python3` (sympy 1.x, scipy, numpy); the exact commands and outputs are quoted
under each finding.

Statement numbers below are the shared-counter numbers (`thm` counter, verified from
`preamble.tex:122–159` — `defn/thm/prop/lem/cor/supp/keythm/example` all share it), i.e.
9.1 … 9.17 in source order. Твърдение 9.7 is the already-fixed one and is **not** re-reported.

Transcript caveat honoured: the break windows are ≈47:30–61:00 and ≈105:30–120:00; nothing
below rests on an absence inside those windows.

---

## 1. UNSOUND — the variance-additivity hypothesis the lecturer stated was dropped

**Location:** `lectures/bodies/lecture_09.tex:292–297` (the run-on continuation of Твърдение 9.8,
*Линейност на очакването*).

**What it says now:**

> Ако допълнително $X_1$ и $X_2$ са независими, то (отново **при съществуващи очаквания**):
> \[ \E[X_1 X_2] = \E[X_1] \E[X_2] \]
> \[ \Var(X_1 + X_2) = \Var(X_1) + \Var(X_2) \]

**Why that is wrong.** Two different results are placed under one hypothesis, and the hypothesis
is the weaker of the two. Existence of $\E X_1, \E X_2$ *is* enough for the product identity
(independence gives $\E|X_1X_2| = \E|X_1|\,\E|X_2| < \infty$, so Fubini applies), but it is
**not** enough for the variance identity.

Concrete failing case: let $X_1, X_2$ be i.i.d. with density $f(x) = \tfrac32 x^{-5/2}$, $x>1$
(Pareto, $\alpha = 3/2$). Then both expectations exist, but neither variance does, so the second
display equates three quantities none of which is defined.

The lecturer stated the two hypotheses **separately**, and stated the second one explicitly:

> **[88:32]** «при допускане, **че очакването на х1 и очакването на х2 съществуват** … очакването
> на х1 по х2 е очакването на х1 по очакването на х2 … **[89:00] и ако дисперсиите съществуват,
> то дисперсията на х1 плюс х2 е сумата на двете дисперсии**»

This is the same failure mode as the already-fixed 9.7: the pipeline merged two statements and
kept only the first one's hypothesis. Note also that the board records these as a *numbered
statement* of their own (`run/lecture_09/ocr/board_014.json` → `"Твър:"` at t = 5073 s ≈ 84:33),
whereas the book has demoted them to two unlabelled displays in running prose; the lecturer even
sketched the proof and assigned the rest («[89:17] аз няма да го доказвам това твърдение тук,
ще трябва да използвате функцията г от х е равен на х1 по х2»).

**Verification.**
```
$ .venv/bin/python3 -c "import sympy as sp; x=sp.symbols('x',positive=True); \
  f=sp.Rational(3,2)*x**sp.Rational(-5,2); \
  print(sp.integrate(f,(x,1,sp.oo)), sp.integrate(x*f,(x,1,sp.oo)), sp.integrate(x**2*f,(x,1,sp.oo)))"
1 3 oo
```
i.e. the density normalises, $\E X = 3 < \infty$, $\E X^2 = \infty$ ⇒ $\Var X$ does not exist.

**Suggested fix** — split them, restoring the lecturer's own hypotheses (and preferably as a
numbered `prop`, since that is what he wrote on the board):

> \begin{prop}
> Нека $X = (X_1, X_2)$ е непрекъснат вектор и $X_1 \perp\!\!\!\perp X_2$.
> \begin{enumerate}
>   \item Ако очакванията $\E X_1$ и $\E X_2$ съществуват, то съществува и $\E[X_1X_2]$ и
>         $\E[X_1X_2] = \E X_1 \cdot \E X_2$.
>   \item Ако освен това съществуват и дисперсиите $\Var X_1$ и $\Var X_2$, то
>         $\Var(X_1+X_2) = \Var X_1 + \Var X_2$.
> \end{enumerate}
> \end{prop}
>
> Доказателството на а) се получава от твърдение~\ref{prop:exp-vector} с $g(x_1,x_2)=x_1x_2$ и
> разпадането $f_X = f_{X_1}f_{X_2}$; б) — с $g(x_1,x_2)=(x_1+x_2)^2$. Лекторът оставя и двете
> сметки на читателя (вж.\ задача 3).

---

## 2. WRONG as stated — the exponential CDF and tail are given with no restriction on $x$

**Location:** `lectures/bodies/lecture_09.tex:145–152` (§ Експоненциално разпределение).

**What it says now:**

> Функцията на разпределение е:
> \[ F_X(x) = \int_{0}^{x} \lambda e^{-\lambda y} dy = 1 - e^{-\lambda x} \]
> … \[ \bar{F}_X(x) = \mathbb{P}(X \ge x) = 1 - F_X(x) = e^{-\lambda x} \]

**Why that is wrong.** Both formulas are asserted for all $x$. For $x<0$ they are outside
$[0,1]$: with $\lambda = 2$, $x = -1$ the first gives $F_X(-1) = -6.389$ and the second gives
$\bar F_X(-1) = 7.389$. This is not a pedantic point in this chapter, because $\bar F_X$ is then
fed straight into the memorylessness functional equation, and it is the *only* place in the
chapter where a distribution function is written without its case split — the uniform section
twelve lines earlier (`:37–44`) does give the full three-branch $F_X$.

The lecturer did give the negative branch:

> **[38:58]** «Първа, функцията на распределение е … **[39:10] отрицателно. [39:12] Това е
> интеграл от 0 до х, ламда, e^{-λy} …, [39:18] че е 1 − e^{−λx}»

**Verification.**
```
$ .venv/bin/python3 -c "import numpy as np; print(1-np.exp(2), np.exp(2))"
-6.38905609893065 7.38905609893065
```

**Suggested fix.**

> Функцията на разпределение е $F_X(x) = 0$ за $x \le 0$, а за $x > 0$
> \[ F_X(x) = \int_{0}^{x} \lambda e^{-\lambda y}\,dy = 1 - e^{-\lambda x} . \]
> … опашката е $\bar F_X(x) = \mathbb{P}(X \ge x) = 1$ за $x \le 0$ и $e^{-\lambda x}$ за $x>0$.

---

## 3. LOST — the χ²(1) proof drops the reason it may *not* use Теорема 9.10

**Location:** `lectures/bodies/lecture_09.tex:702–706` (proof of Твърдение 9.17).

**What it says now:**

> Ще покажем, че квадратът на една стандартно нормална величина $T_1 = Z_1^2$ има
> разпределение $\chi^2(1) \equiv \Gamma(1/2, 1/2)$.
> Започваме с функцията на разпределение за $t > 0$: …

**Why that is a loss.** The chapter spends its central boxed theorem (9.10) on a change of
variables whose *only* substantive hypothesis is bijectivity, and this proof is the one place in
the chapter where that hypothesis actually bites — which is exactly why the lecturer switched
methods, and he said so at length:

> **[159:25]** «само че вижте, тук T₁ като функция на Z₁ … **[159:37] тя не е монотонно
> растяща**, защото Z₁ приема стойности от минус безкрайност до безкрайност, параболата,
> **[159:45] не е взаимно еднозначна. [159:47] тя има проблем в нулата. [159:50] g′ е 2 пъти z
> … и тя има нула** … [159:58] на едно z не съответства едно t … **[160:09] Така че не можем да
> използваме директно теоремата за смяната на променливите, [160:13] сега ще ви покажа другия
> начин, който често пъти работи и е директен.**»

As the book stands, a reader has no idea why the CDF route appears here rather than an
application of 9.10, and the boxed theorem loses its one worked demonstration that its
hypotheses are not decoration.

**Verification.** $g(z)=z^2$ on $\mathbb R$: $g(-1)=g(1)=1$, $g'(0)=0$; not injective, so 9.10 is
inapplicable. The direct CDF route in the book is correct — see §*Checked and found sound*.

**Suggested fix** — restore the sentence before the CDF computation:

> Тук теорема~\ref{...} (смяна на променливите) **не е приложима**: изображението
> $g(z) = z^2$ не е взаимно еднозначно върху $\mathbb{R}$ — на $z$ и $-z$ съответства едно и
> също $t$, а производната $g'(z) = 2z$ се нулира в нулата. Затова минаваме по директния път
> през функцията на разпределение, който работи и без взаимна еднозначност.
> Започваме с функцията на разпределение за $t > 0$: …

---

## 4. LOST / UNCLEAR — χ²(n) is never defined; the definition is smuggled into Твърдение 9.17 as «≡»

**Location:** `lectures/bodies/lecture_09.tex:673–680` (§9.3.2 and Твърдение 9.17), and
`:724–728`.

**What it says now:**

> \begin{prop}
> Нека $Z_1, \dots, Z_n$ са независими в съвкупност стандартно нормални … Тогава сумата от
> техните квадрати има $\chi^2$ разпределение с $n$ степени на свобода, което е еквивалентно
> на Гама разпределение:
> \[ Y = \sum_{j=1}^n Z_j^2 \sim \chi^2(n) \equiv \Gamma\left(\frac{n}{2}, \frac{1}{2}\right) \]
> \end{prop}

**Why that is a defect.** `\chi^2` is nowhere defined in the chapter (grep over
`lectures/bodies/*.tex`: the only definitional statement in the whole book is a table row at
`formulas.tex:123`). So the `≡` inside 9.17 is doing definitional work inside a proposition, and
the proposition's mathematical content becomes ambiguous: read one way it asserts
$\sum Z_j^2 \sim \Gamma(n/2,1/2)$ (true, and what the proof proves); read the other way it
asserts an identity between two independently-defined families, which the proof does not
establish. Reading `≡` as a definition is the only consistent reading, but then 9.17 is a
definition and a theorem in one box.

The lecturer gave a **separate definition first**, then the theorem, and derived the moments:

> **[153:19]** «И последното нещо, което ще дефинирам за днес … то е частен случай на гама
> разпределение, но е много важно … **[153:45] X² е χ² с n степени на свобода, където n е цяло
> число. [153:52] Тогава и само тогава, когато X² е гама разпределено с параметри n върху 2 и
> 1 върху 2** … [154:22] Значи ще имаме една втора на степен n върху 2 … гама от n върху 2 …
> x^{n/2−1} … e^{−x/2} … [154:42] за x по-голямо от 0 и 0 иначе»
> **[155:01]** «от свойствата на гама функцията, очакването на X е алфа върху бета, което е
> n върху 2, върху една втора, е равно n. [155:09] И дисперсията е алфа върху бета на квадрат,
> което в случая е n върху 2 върху една четвърт, е равна на 2n.»

Confirmed on the board: `board_029`–`032` carry the theorem as `Y = Σ(Z_j)² ~ χ²(n)` with
`χ²(1) = Γ(½,½)` and `χ²(n) = Γ(n/2,½)` written *separately* (with `=`, not folded into the
theorem line).

In the book, all of that survives only as (a) an `≡` inside the proposition, (b) the explicit
density in appendix А, and (c) «очакването е $n$, а дисперсията $2n$» buried in the caption of
`fig:chi-square` (`:682–685`) with no derivation. The lecturer's restriction of $n$ to an
integer and his motivation (χ² arises as the sum of squared standardised regression errors,
[156:48]–[158:08], the reason L14 needs it) are gone entirely.

**Verification** (the identification itself is sound):
```
$ .venv/bin/python3   # scipy: gamma(a=n/2, scale=1/beta=2) vs chi2(df=n)
n=1: chi2 mean/var = 1.0,2.0    Gamma(0.5,scale2) = 1.0,2.0
n=2: 2.0,4.0                    2.0,4.0
n=4: 4.0,8.0                    4.0,8.0
n=8: 8.0,16.0                   8.0,16.0
n=13: 13.0,26.0                 13.0,26.0
# pointwise densities, t = 0.1/0.5/1.0/2.5/7.0
book 1/sqrt(2pi) t^-1/2 e^-t/2 == gamma.pdf(t,a=.5,scale=2) == chi2.pdf(t,df=1)  (8 d.p.)
```

**Suggested fix** — give χ² its own definition before the theorem, and restore the moments as
text rather than caption:

> \begin{defn}[хи-квадрат разпределение]\label{def:chi2}
> Нека $n$ е естествено число. Казваме, че $X$ има \emph{хи-квадрат разпределение с $n$ степени
> на свобода}, и пишем $X \sim \chi^2(n)$, ако $X \sim \Gamma\!\left(\frac n2, \frac12\right)$,
> тоест ако плътността ѝ е
> \[ f_X(x) = \frac{(1/2)^{n/2}}{\Gamma(n/2)}\, x^{n/2-1} e^{-x/2}, \quad x>0, \qquad
>    f_X(x) = 0 \text{ иначе.} \]
> \end{defn}
> От моментите на Гама разпределението (твърдение~\ref{...}) веднага следва
> $\E X = \frac{n/2}{1/2} = n$ и $\Var X = \frac{n/2}{1/4} = 2n$.

and then state 9.17 as `$Y = \sum_{j=1}^n Z_j^2 \sim \chi^2(n)$` with the `≡` removed.

---

## 5. WRONG terminology, contradicting the book's own convention — «мащабен параметър $\beta$»

**Location:** `lectures/bodies/lecture_09.tex:615` (Твърдение 9.14) and `:724` (proof of 9.17).

**What it says now:**

> `:615` Нека $X_1, \dots, X_n$ са независими в съвкупност …, като $X_i \sim \Gamma(\alpha_i, \beta)$
> **(имат общ мащабен параметър $\beta$)**.
> `:724` … е сума на $n$ независими Гама величини **с еднакъв мащабен параметър $\beta = 1/2$**
> и формов параметър $\alpha_j = 1/2$ …

**Why that is wrong.** The book's Гама is rate-parameterised (`:594–600`, density
$\propto x^{\alpha-1}e^{-\beta x}$, and `formulas.tex:122` the same). Under that convention
$\beta$ is the **rate**; the scale is $1/\beta$. Indeed if $X \sim \Gamma(\alpha,\beta)$ then
$cX \sim \Gamma(\alpha, \beta/c)$ — the parameter that transforms as a scale is $1/\beta$, not
$\beta$. Calling $\beta$ «мащабен параметър» is the one place in the book that mislabels it:
`formulas.tex:138` says only «сума от независими $\Gamma$ с **общо $\beta$**», and nothing else
in `bodies/` calls $\beta$ a scale (grep for `мащаб` returns L07/L11 uses about scaling of
random variables, plus these two lines and `:164`). Since the whole point of the parenthesis at
`:615` is to flag the shared-parameter condition, mislabelling it is exactly the sentence a
reader will use to decide which parameter must match — and «мащабен» invites the reader to
match $1/\beta$ under a `scale` convention imported from software (scipy's `scale`, R's `rate`
vs `scale`).

The lecturer said only «фиксирано» / «същия параметър»:

> **[137:10]** «бета трябва да е фиксирано, а алфа да се смени» … **[137:53]** «и същия
> параметър [бета] … [137:57] имате един и същи параметър [бета] и различни първи параметри»

**Verification** — the shared-rate condition is genuinely necessary (simulation, $n = 4\cdot10^5$):
```
$ .venv/bin/python3   # numpy gamma takes scale = 1/rate
shared rate  X1~G(1.3,rate2), X2~G(2.7,rate2):  KS vs G(4.0,rate2)  D=0.00133, p=0.48   -> fits
mixed  rates X1~G(1.3,rate2), X2~G(2.7,rate5):  KS vs G(4.0,rate2)  D=0.389,   p=0      -> rejected
                                                KS vs G(4.0,rate5)  D=0.277,   p=0      -> rejected
```
So Твърдение 9.14 **does** carry the shared-parameter condition (good), it is merely named wrong.

**Suggested fix.** At `:615`: «(имат общ втори параметър $\beta$ — интензитетът; сумирането е
възможно само при съвпадащ $\beta$)». At `:724`: «с еднакъв втори параметър $\beta = 1/2$ и
формов параметър $\alpha_j = 1/2$».

---

## 6. UNSOUND — the Гама (and експоненциалната) плътност is given «за $x \ge 0$», which is
undefined at $0$ for $\alpha<1$ — the very case used two subsections later

**Location:** `lectures/bodies/lecture_09.tex:596–600` (Гама), and the same pattern at `:138–142`
(експоненциално).

**What it says now:**

> \[ f_X(x) = \begin{cases} \frac{\beta^\alpha}{\Gamma(\alpha)} x^{\alpha-1} e^{-\beta x},
>   & \text{за } x \ge 0 \\ 0, & \text{иначе} \end{cases} \]

**Why that is wrong.** For $\alpha < 1$, $x^{\alpha-1} \to \infty$ as $x \downarrow 0$, so the
first branch does not define a value at $x = 0$. The chapter then uses precisely $\alpha = 1/2$
at `:703` and `:719` for $\chi^2(1)$, where the stated formula evaluates to $+\infty$ at the
included endpoint. The formula sheet gets this right (`formulas.tex:121–122`: both densities are
given with **$x > 0$**), so the chapter contradicts the appendix.

The lecturer wrote $x>0$ **deliberately** and explained why on tape:

> **[133:37]** «e на минус бета х за х по-голямо … **[133:41] Айде ще напиша, не си мислите, че
> тук може да стане проблем, [133:44] тук ще напиша по-малко или равен [за нулевия клон].
> [133:46] Тук е по-голямо от 0. [133:48] Това няма никакво значение, в тази точка масата е 0.**»

**Verification.**
```
$ .venv/bin/python3 -c "from scipy import stats; print(stats.gamma.pdf(0.0,a=0.5,scale=2.0))"
inf
```

**Suggested fix** — match the lecturer and the appendix:

> \[ f_X(x) = \begin{cases} \frac{\beta^\alpha}{\Gamma(\alpha)} x^{\alpha-1} e^{-\beta x},
>   & \text{за } x > 0 \\ 0, & \text{за } x \le 0 \end{cases} \]
> (Стойността в самата нула е без значение — там масата е нула; за $\alpha < 1$ първият израз
> изобщо не е дефиниран в $0$.)

The same change applies to `:138–142` for consistency, although there $\lambda e^{-\lambda x}$
is finite at $0$ so nothing is undefined.

---

## 7. NARROWED / UNCLEAR — the convolution is boxed as a *definition*, and only in the
independent case, although the lecturer twice stressed independence is not needed

**Location:** `lectures/bodies/lecture_09.tex:390–398` (Дефиниция 9.11).

**What it says now:**

> За да намерим търсената маргинална плътност на сумата $Y_2$, интегрираме по $y_1$:
> \begin{defn}[конволюция]
> Плътността на сумата на **две независими** непрекъснати случайни величини се дава от
> \emph{конволюцията}
> \[ f_{Y_2}(y_2) = \int f_{X_1}(y_1) f_{X_2}(y_2 - y_1)\, dy_1 . \]
> \end{defn}

**Why that is a defect.** Two things.

(a) It is *not* a definition — it is the conclusion of the derivation in the six lines directly
above it (Jacobian $=1$, then marginalise). Boxed as a `defn` it reads as a stipulation, which
makes the preceding derivation look purposeless and leaves the actual theorem («плътността на
сумата **е** тази интеграл») unstated anywhere.

(b) It is stated only for independent $X_1, X_2$, whereas the general marginalisation
$f_{X_1+X_2}(y_2) = \int f_X(y_1, y_2-y_1)\,dy_1$ — valid for *any* continuous vector — is never
displayed. The chapter does note the distinction in prose at `:377–379` and `:389`, but only for
the *joint* density of $(Y_1,Y_2)$; the density of the sum, the thing actually wanted, is boxed
in the narrow case. The lecturer made this point twice, deliberately:

> **[103:40]** «Изискването за независимост по принцип е защото често пъти, ако те не са
> независими, не може да сметнете съвместната плътност. **[103:52] А ако имате съвместната
> плътност на х1 и х2, няма нужда да допускате, че са независими.**»
> **[122:21]** «но ако я знаем в явен вид, **няма нужда да изискваме тази независимост** …
> [122:36] Но ако я знаем, не е необходимо да допускаме независимост»

**Suggested fix** — state the general result, then the independent corollary:

> \begin{prop}[плътност на сума — конволюция]\label{def:convolution}
> Нека $X=(X_1,X_2)$ е непрекъснат вектор със съвместна плътност $f_X$. Тогава $Y_2 = X_1+X_2$
> е непрекъсната и
> \[ f_{Y_2}(y_2) = \int f_X(y_1,\; y_2-y_1)\, dy_1 . \]
> Ако освен това $X_1 \perp\!\!\!\perp X_2$, съвместната плътност се разпада и се получава
> \emph{конволюцията}
> \[ f_{Y_2}(y_2) = \int f_{X_1}(y_1)\, f_{X_2}(y_2-y_1)\, dy_1 . \]
> \end{prop}
> Независимостта не е част от схемата — тя е практическото условие, което ни позволява да
> построим $f_X$ от двете маргинални плътности.

(The label may stay `def:convolution` so the two `\ref`s at `:400` and `:404` keep working.)

---

## 8. UNSOUND (low) — «за всяко подмножество $D \subseteq \mathbb{R}^n$» in the joint-density
definition

**Location:** `lectures/bodies/lecture_09.tex:191–201` (Дефиниция 9.4), item 3.

**What it says now:**

> \item за всяко подмножество $D \subseteq \mathbb{R}^n$:
> \[ \mathbb{P}(X \in D) = \int \dots \int_D f_X(x)\, dx . \]

**Why that is wrong.** $\{X \in D\}$ need not be an event and $\int_D$ need not exist for an
arbitrary $D \subseteq \mathbb{R}^n$ (Vitali set). The book itself is stricter elsewhere: the
proof of Теорема 9.10 at `:352` opens with «Нека $A\subseteq g(\mathcal{D}(f_X))$ е произволно
**измеримо** множество», and the one-dimensional analogue in L08
(`lectures/bodies/lecture_08.tex:208–218`, item 3) is stated only «за всеки две числа $a<b$».
So this is an internal inconsistency as well as a false universal.

**Verification.** Not computational — standard: a non-measurable $D$ makes both sides undefined.
Cross-checked by reading `lecture_08.tex:206–220` and `lecture_09.tex:351–352`.

**Suggested fix.**

> \item за всяко (измеримо) подмножество $D \subseteq \mathbb{R}^n$: …

with, if desired, a footnote that measurability is a technical restriction which never fails for
the regions used in the course (правоъгълници, триъгълници, кръгове и обединения от такива).

---

## 9. LOST / R1 violation — the lecturer's $\Phi(1{,}96)$ was silently corrected

**Location:** `lectures/bodies/lecture_09.tex:132`.

**What it says now:**

> Също така класическа стойност е $\Phi(1{,}96) \approx 0{,}975$, което означава, че $95\%$ от
> вероятностната маса е в интервала $[-1{,}96, 1{,}96]$.

**Why that is a defect.** The mathematics is correct; the fidelity is not. The lecturer said
$0{,}95$, twice, and it is his conflation of the one-sided table value with the two-sided
coverage:

> **[37:12]** «ще бъде фи от 1,96 — това е [приблизително] **0,95**. [37:20] ето това е 1,96,
> [37:23] тук се заключва вероятност **95 %**, [37:27] а в тука остава **5 %**»
> **[37:36]** «отивате в таблица, да гледате на 1,96 — **[по]мене от 0,95**»

Under R1 the book must not silently substitute the textbook value; a footnote is the sanctioned
route (§2, R1; cf. the two footnotes already added for L13 in §12 of `REMEDIATION.md`).

**Verification.**
```
$ .venv/bin/python3 -c "from scipy import stats; print(stats.norm.cdf(1.96), \
    stats.norm.cdf(1.96)-stats.norm.cdf(-1.96), stats.norm.ppf(0.95))"
0.9750021048517795 0.950004209703559 1.644853626951472
```
So $\Phi(1{,}96)=0{,}975$, the two-sided mass is $0{,}95$, and the one-sided $95\%$ quantile is
$1{,}645$ — the lecturer's number belongs to the interval, not to $\Phi$.

**Suggested fix.** Keep the corrected sentence and add a footnote:

> …в интервала $[-1{,}96, 1{,}96]$.\footnote{На лекцията беше казано
> «$\Phi(1{,}96)\approx 0{,}95$»; числото $0{,}95$ е вероятността на двустранния интервал
> $[-1{,}96,1{,}96]$, а самата стойност на функцията на разпределение е $0{,}975$. Едностранният
> квантил на ниво $0{,}95$ е $1{,}645$.}

---

## 10. LOST (low) — «Гама не е безпаметно» is dropped, right after $\Gamma(1,\beta)\equiv\Exp(\beta)$

**Location:** `lectures/bodies/lecture_09.tex:612` (the sentence identifying
$\Gamma(1,\beta) \equiv \Exponential(\beta)$).

**Why that is a loss.** The chapter establishes memorylessness for $\Exponential$ (`:158–162`),
then identifies $\Exponential(\beta)$ as the $\alpha=1$ member of the Гама family — the natural
misreading being that the family inherits the property. A student asked exactly this and the
lecturer answered emphatically:

> **[151:36]** «**Не, не е безпаметно. Само експоненциалното е безпаметно.** … [151:45] Всички
> безпаметни са само експоненциално. [151:47] Това е обратната теорема … [151:58] **Гамата не е
> [безпаметна]. [151:59] Първият параметър, алфата, е различен от 1 — не е безпаметна.**»

`formulas.tex:132` does record «само $\Exponential$ сред непрекъснатите», so the fact is in the
book; it is missing from the chapter that raises the question.

**Suggested fix** — one sentence after `:612`:

> Обратното не важи: безпаметността е характерна само за $\alpha = 1$. За $\alpha \ne 1$
> Гама разпределението \emph{не} е безпаметно — както видяхме, сред непрекъснатите
> разпределения единствено експоненциалното удовлетворява функционалното уравнение
> $\bar F(x+y)=\bar F(x)\bar F(y)$.

---

## 11. UNCLEAR (low) — in Допълнение 9.13, Стъпка 5, the map is not injective on
$\mathcal{D}(f_{X,Y})$

**Location:** `lectures/bodies/lecture_09.tex:481–492` («Стъпка 5: $Z = XY$»).

**What it says.** $W = X$, so $g(x,y) = (xy, x)$, and the step is presented as an application of
Теорема 9.10, whose one substantive hypothesis is that $g$ be взаимно еднозначно on
$\mathcal{D}(f_X)$.

**Why that is a gap.** $\mathcal{D}(f_{X,Y}) = \{f_{X,Y}>0\}$ contains the whole segment
$x = 0$, $0 < y \le \tfrac12$ (there $f_{X,Y}(0,y) = \tfrac{23}{2}\cdot 0 + y = y > 0$), and $g$
collapses all of it to the single point $(0,0)$; the inverse $y = z/w$ and the Jacobian $-1/w$
are both undefined at $w=0$. The conclusion is right — the offending set is Lebesgue-null, so it
contributes nothing — but the supplement's stated purpose is to show the theorem's machinery
being applied faithfully, and a reader who checks the hypothesis finds it violated with no
comment. Given that §3 above shows the chapter elsewhere *loses* the discussion of exactly this
hypothesis, it is worth one sentence.

**Verification.** The result itself is confirmed by simulation from the exact joint density
(rejection sampling on the triangle, then weighted resampling, $8\cdot10^5$ draws):
```
$ .venv/bin/python3
sim EX = 0.48925   exact 47/96  = 0.489583
sim EY = 0.13043   exact 25/192 = 0.130208
KS  Z=X+2Y vs F(z)=z^3            D=0.00106, p=0.33     -> f_Z = 3z^2 confirmed
KS  Z=XY   vs F(z)=1-(1-8z)^{3/2} D=0.00075, p=0.76     -> f_Z = 12*sqrt(1-8z) confirmed
max XY observed = 0.124984        claimed bound 1/8 = 0.125
sim Var(X-Y) = 0.089754           exact 367/4096 = 0.089600
```
Symbolically, all of Допълнение 9.13 checks out exactly (see §*Checked and found sound*).

**Suggested fix** — add after the Jacobian display:

> (Строго погледнато $g$ не е взаимно еднозначно върху цялата дефиниционна област: отсечката
> $x = 0$ се свива в точката $(0,0)$, а якобианата не е дефинирана при $w = 0$. Това е множество
> с нулева мярка и не влияе на плътността; достатъчно е теоремата да се приложи върху
> $\{x>0\}$.)

---

## 12. UNCLEAR (low) — «точно неговите крайни точки са границите за $y_1$»

**Location:** `lectures/bodies/lecture_09.tex:405`.

**What it says now:**

> При фиксирано $y_2$ ни трябва хоризонталното сечение на този образ: точно неговите крайни
> точки са границите за $y_1$.

**Why that is imprecise.** The horizontal section need not be an interval. If
$\mathcal{D}(f_X) = (0,1)^2 \cup (3,4)\times(0,1)$, then for fixed $y_2$ the section
$\{y_1 : (y_1, y_2-y_1) \in \mathcal{D}(f_X)\}$ is a union of two disjoint intervals and has no
single pair of «крайни точки» that describes it. In practice the error is harmless — the
integrand vanishes on the gap, so integrating between the outermost endpoints gives the right
answer — but the sentence asserts a general rule that does not hold, in the one paragraph whose
whole job is to teach the reader how to get the limits right.

The lecturer's own formulation was the safe one:

> **[124:12]** «И тук единствено е много важно да си определите границите на интегрирането.
> [124:17] **Те ще зависят от възможните стойности на $y_1$** … [124:49] Тогава трябва да
> интегрирате от тук до тук, **защото само тук са възможните стойности за $y_1$**»
> **[131:01]** «Тия неща, между другото, **няма рецепта**, ами те са точно такива с геометрични
> аргументи по принцип.»

**Suggested fix.**

> При фиксирано $y_2$ ни трябва хоризонталното сечение на този образ — тоест множеството от
> тези $y_1$, за които $(y_1, y_2-y_1) \in \mathcal{D}(f_X)$. Когато то е интервал (какъвто е
> случаят във всички примери по-долу), краищата му са границите на интегриране; общо правило
> няма — сечението се намира от геометрията на дефиниционната област.

---

## 13. Minor gaps worth a line each (no separate finding)

* `:724` — «сума на $n$ **независими** Гама величини»: the independence of the $Z_j^2$ is used
  but not justified. The lecturer said it («**[158:40]** понеже те са независими»); one clause
  («понеже $Z_j^2$ е функция само на $Z_j$, независимостта се запазва») closes it.
* `:407–421` — Твърдение 9.12 is stated for general $n$ but only $n=2$ is reduced to the scheme;
  the passage from $n=2$ to general $n$ (induction, plus the fact that $X_1+X_2$ is independent
  of $X_3$) is not mentioned. The lecturer likewise stated the general $n$ and did only $n=2$
  ([126:11]–[127:19]), so this is faithful; a half-sentence «останалото следва с индукция» would
  still help.
* `:314–318` (Допълнение 9.9) — $\E[Y \given X = x]$ is defined as a function of $x$, and then
  $\E\big[\E[g(X,Y) \given X]\big]$ is written without ever saying that
  $\E[g(X,Y)\given X] := \varphi(X)$ where $\varphi(x) = \E[g(X,Y)\given X=x]$. The identity is
  correct; the notation is used one step before it is introduced.
* Board `board_016` shows the lecturer wrote the image set out inside the theorem statement:
  `g(D_{f_X}) = {y ∈ R² : y = g(x) за някое x ∈ D(f_X)}`. Теорема 9.10 uses
  `g(\mathcal{D}(f_X))` without defining it in the box (only loosely in the preceding prose).
* Теорема 9.10 gives $f_Y$ only on $g(\mathcal{D}(f_X))$ and never says $f_Y = 0$ outside it, so
  strictly the density is left undefined on part of $\mathbb{R}^2$. Every worked application in
  the chapter then silently supplies the zero branch.

---

# Checked and found sound

Everything below was re-derived and matches the book exactly. This is the bulk of the chapter.

**Uniform.** Density, three-branch $F_X$ (consistent with the strict-inequality convention:
$F_X(b)=\mathbb{P}(X<b)=1$), $\E X = \frac{a+b}{2}$; the standardisation $Z=(X-a)/(b-a)$ and its
change-of-variables computation; $\E Z^2 = 1/3$, $\Var Z = 1/12$, $\Var X = (b-a)^2/12$.
Verified symbolically with sympy.

**Normal.** Density and normalisation; $\Phi$; the standardisation $Y=(X-\mu)/\sigma$ with the
algebra of the substitution; $\E Z = 0$ by oddness; the Feynman differentiation-under-the-integral
argument — I re-did the $\sigma$-derivative and it is right:
$\partial_\sigma e^{-y^2/2\sigma^2} = e^{-y^2/2\sigma^2}\cdot y^2/\sigma^3$, giving
$\sqrt{2\pi}\sigma^3 = \int y^2 e^{-y^2/2\sigma^2}dy$ and $\E Z^2 = 1$ at $\sigma=1$. This matches
`board_009` line for line («$\sqrt{2\pi} = \int -\frac{y^2}{2}\cdot\frac{-2}{\sigma^3}
e^{-y^2/2\sigma^2}dy$», «$\Rightarrow \sqrt{2\pi}\sigma^3 = \int y^2 e^{-y^2/2\sigma^2}dy
\big|_{\sigma=1}$»). $\mathbb{P}(X<x) = \Phi((x-\mu)/\sigma)$, $\Phi(0)=1/2$.

**Exponential.** Memorylessness derivation (the containment
$\{X\ge x+y\}\subseteq\{X\ge x\}$ step is right, and $\bar F = 1 - F$ is exact under the book's
$F(x)=\mathbb{P}(X<x)$ convention — no off-by-a-point error); the converse via
$\bar F(x+y)=\bar F(x)\bar F(y)$; $\lambda X \sim \Exponential(1)$ with the CDF check;
$\E X = 1/\lambda$, $\Var X = 1/\lambda^2$.

**Допълнение 9.3 (Коши).** $\int |x| f(x)\,dx$ diverges for $f(x)=1/(\pi(1+x^2))$, so no mean and
hence no variance; the framing as the counterexample to «symmetric density ⇒ mean 0» and to
dropping the first-moment condition in the LLN is correct.

**Дефиниция 9.5 (маргинална плътност)**, the joint CDF ↔ density relation, and the caveat
«в точките, в които плътността е непрекъсната» — the last matches the lecturer verbatim
(«**[73:24]** разбира се, тук има едно скрито условие, че в точката $x$ тази плътност трябва да
е непрекъсната»).

**Теорема 9.6 (критерий за независимост).** Both the CDF form and the density form are correct;
with $F(x)=\mathbb{P}(X<x)$ (left-continuous) the product form still characterises independence,
since taking right limits recovers $\mathbb{P}(X\le x, Y\le y)=F_X(x^+)F_Y(y^+)$.

**Независимост в съвкупност** (`:245–250`) matches the lecturer's definition at [78:24]–[81:17],
including the «в частност $k=n$» remark he made at [81:05].

**Теорема 9.10 (смяна на променливите)** and its proof. The hypotheses as stated are sufficient:
requiring *both* $g$ and $h$ differentiable forces $J \ne 0$ (chain rule on $g\circ h = \mathrm{id}$
gives $Dg(h(y))Dh(y)=I$), so no separate non-vanishing-Jacobian assumption is needed. Statement
and hypotheses match `board_016` word for word, including «$g$ и $h$ са непрекъснати и
диференцируеми в $\mathcal{D}(f_X)$ и $g(\mathcal{D}_{f_X})$». The proof's logic
($\mathbb{P}(Y\in A)=\mathbb{P}(X\in h(A))=\iint_{h(A)}f_X=\iint_A f_X(h(y))|J(y)|dy$ for all
measurable $A$ ⇒ the integrand is the density) is valid and is the lecturer's proof
([100:04]–[102:05]).

**The sum scheme.** $Y=(X_1, X_1+X_2)$, $h(y)=(y_1, y_2-y_1)$,
$J = \det\begin{psmallmatrix}1&0\\-1&1\end{psmallmatrix} = 1$ — identical to `board_022`.
The remark that independence is only needed to *build* $f_X$ is the lecturer's own point.

**Твърдение 9.12 (сума на нормални).** True; and the justification that
$\mathcal{D}(f_X)=g(\mathcal{D}(f_X))=\mathbb{R}^2$, hence limits $\pm\infty$, matches
[130:05]–[131:37] («въобще образът отново е $\mathbb{R}^2$»).

**Допълнение 9.13 in full.** Every number is exact. sympy over the triangle
$\{0\le x\le 1,\ 0\le y\le (1-x)/2\}$ with $f = cx+y$:

| claim | book | sympy |
|---|---|---|
| normalisation | $c/12 + 1/24 = 1 \Rightarrow c = 23/2$ | `c/12 + 1/24`, `solve → [23/2]` |
| $f_X(x)$ | $(1+44x-45x^2)/8$ | `-45x**2/8 + 11x/2 + 1/8` (identical), `∫₀¹ = 1` |
| $\E X$ | $47/96$ | `47/96` |
| $\E Y$ | $25/192$ | `25/192` |
| $\E[Y\mid X=\tfrac12]$ | $\frac{71/384}{47/32} = \frac{71}{564} \approx 0{,}126$ | `71/564`, and $f_X(1/2)=47/32$ ✓ |
| $Z = X+2Y$ | $J=1$, $f_Z = 3z^2$ on $[0,1]$ | ✓ symbolically and by KS test ($p=0.33$) |
| $Z = XY$ | $J=-1/w$, $w^2-w+2z\le 0$, $w_{1,2}=\frac{1\mp\sqrt{1-8z}}2$, $f_Z = 12\sqrt{1-8z}$ on $[0,\tfrac18]$ | ✓; KS test $p=0.76$; simulated $\max XY = 0.124984$ vs the derived bound $1/8$ |
| the AM–GM remark | $x\cdot 2y \le ((x+2y)/2)^2 \le 1/4 \Rightarrow xy \le 1/8$, equality at $(\tfrac12,\tfrac14)$ | ✓ |
| Vieta step | $\frac{23}{2}d + z\frac{w_2-w_1}{w_1w_2} = \frac{23}{2}d + \frac d2 = 12d$ | ✓ ($w_1w_2=2z$, $w_2-w_1=d$) |
| $\Var U$, $U = X-Y$ | $\E[(X-Y)^2]-(\E U)^2 = 367/4096$ | `E(X-Y)^2 = 7/32`, `VarU = 367/4096`, sim `0.08975` |
| CLT constant | $\E U/\sigma_U = 23/\sqrt{367} \approx 1{,}20$ | `1.20059…` |
| CLT direction | $\mathbb{P}(\sum U_i>0)\approx\Phi(1{,}20\sqrt n)\to 1$ | correct: $\mathbb{P}(S>-a)=1-\Phi(-a)=\Phi(a)$ |
| the independence subtlety | $X_i \not\perp Y_i$ but the *pairs* are i.i.d., so $U_i$ are i.i.d. | correct, and it is the right thing to flag |
| the tikz picture | $w_{1,2}$ at $z=0{,}06$ plotted at $0{,}1394$ and $0{,}8606$ | $\frac{1\mp\sqrt{1-0{,}48}}{2} = 0{,}1394,\ 0{,}8606$ ✓ |

The figure caption's geometric account (hyperbola $xy=z$ cutting the hypotenuse in two points for
$z<\tfrac18$, tangent at $(\tfrac12,\tfrac14)$, outside for larger $z$) is correct.

**Допълнение 9.9 (условна плътност).** $f_{Y\mid X}=f_{X,Y}/f_X$ with $f_X(x)>0$; it is a density
in $y$ for each fixed $x$; the conditional probability and conditional expectation integrals; the
tower property $\E[g(X,Y)]=\E[\E[g(X,Y)\mid X]]$ for integrable $g$; and
$\E[g(X,Y)\mid X=x]=\E[g(x,Y)]$ under independence. All correct.

**Гама.** Density normalisation via $y=\beta x$ (`:604–610`) — correct and matches
[134:32]–[135:16]. $\Gamma(1,\beta)\equiv\Exponential(\beta)$. $\Gamma(1)=1$,
$\Gamma(n+1)=n!$ (for natural $n$; the lecturer stated it the same loose way at [134:09] and even
explained the mероморфic extension, so per R1 this is faithful).
$\Gamma(\alpha+1)=\alpha\Gamma(\alpha)$: `sympy.simplify(gamma(a+1)-a*gamma(a)) → 0`.
$\Gamma(1/2)=\sqrt\pi$: `sympy.gamma(1/2) → sqrt(pi)`.

**Твърдение 9.14 (сума на Гама) and its proof.** The limits $0\le y_1\le y_2$ are derived
correctly from $X_1,X_2\ge 0$ and match `board_026` (`∫₀^{y₂} …, y₂>0`). The Beta-function step is
right: $\int_0^{y_2} y_1^{\alpha_1-1}(y_2-y_1)^{\alpha_2-1}dy_1 = y_2^{\alpha_1+\alpha_2-1}
B(\alpha_1,\alpha_2)$ with $B = \Gamma(\alpha_1)\Gamma(\alpha_2)/\Gamma(\alpha_1+\alpha_2)$, and
the resulting density is exactly $\Gamma(\alpha_1+\alpha_2,\beta)$. The shared-parameter
condition **is** present (only mislabelled — finding 5); simulation confirms it is necessary.
The infinite-divisibility remark and the example «$\Gamma(3{,}5,\beta)$ като сума от 7 независими
$\Gamma(0{,}5,\beta)$» are correct ($7 \times 0{,}5 = 3{,}5$) and are recovered from the
lecturer's answer to a student at [167:09]–[168:45], including his own «безгранично делимо».

**Следствие 9.15.** $\sum_{i=1}^n \Exponential(\lambda) \sim \Gamma(n,\lambda)$ — correct, and it
is the lecturer's corollary at [145:18]–[147:09], including his «стига да са с един и същи
параметър».

**Твърдение 9.16 (моменти на Гама) and its proof.** $\E X = \alpha/\beta$,
$\Var X = \alpha/\beta^2$ — correct for the rate parameterisation. sympy:
`∫₀^∞ x·f = alpha/beta`, `∫₀^∞ x²·f = alpha*(alpha+1)/beta**2`, so
`Var = alpha/beta**2`. The proof's trick (recognise the $\Gamma(\alpha+1,\beta)$ density inside
the integral) is algebraically exact:
$\frac{\Gamma(\alpha+1)}{\beta\Gamma(\alpha)}\cdot\frac{\beta^{\alpha+1}}{\Gamma(\alpha+1)}
= \frac{\beta^{\alpha}}{\Gamma(\alpha)}$ ✓. Leaving the second moment as an exercise matches
[148:51]–[152:55] («това ще го пресметнете със същия интеграл»), and Задача 4 records it.

**Твърдение 9.17 (χ²) and its proof.** The identification $\chi^2(n)=\Gamma(n/2,1/2)$ and
$Z^2\sim\chi^2(1)$ are both true (scipy check above, to 8 decimal places pointwise and exactly in
mean/variance for $n=1,2,4,8,13$). The CDF route is correct:
$\mathbb{P}(Z^2<t)=\mathbb{P}(-\sqrt t<Z<\sqrt t)$, the $2\times$ symmetrisation, and
$\frac{d}{dt}$ with $\frac{d}{dt}\sqrt t = \frac1{2\sqrt t}$ giving
$f_{T_1}(t)=\frac1{\sqrt{2\pi}}t^{-1/2}e^{-t/2}$ — identical to `board_030`–`032`. The
constant-matching argument is **not** circular: $f_\Gamma$ integrates to 1 by the definition of
$\Gamma(\alpha)$ (shown at `:604`), $f_{T_1}$ integrates to 1 because it was derived as a density,
and two densities of the same functional form must share the constant — whence
$\Gamma(1/2)=\sqrt\pi$ as a by-product. This is exactly the lecturer's argument at
[165:41]–[166:27], including his «Но вие това не трябва да го знаете, за да заключите, че това е
равно на това».

**`fig:chi-square`.** The plotted curves are correct: e.g. the $n=2$ curve at $x=0{,}05$ is
plotted at $0{,}488$ against $\tfrac12 e^{-0{,}025}=0{,}4877$. The caption's «очакването е $n$, а
дисперсията $2n$» is right (though see finding 4 — it belongs in the text, not the caption), and
the forward reference to L13's two-quantile confidence interval for the variance is accurate.

**Задачи 1–4.** All four are well-posed and all four are transcript-backed
([15:04], [44:48], [89:17], [152:31]). Задача 4's phrasing («пресметнете втория момент … и
изведете $\E X = \alpha/\beta$, $\Var X = \alpha/\beta^2$») redundantly re-asks for the first
moment, which the proof already gives — cosmetic, not reported.

**Conventions.** No breach found. $F_X(x)=\mathbb{P}(X<x)$ is respected throughout (including at
`:191–226`, which `REMEDIATION.md` C-10 flagged — that one is fixed). `\Var`, `\E`, `\ind`,
`\perp\!\!\!\perp` and the rate-parameterised $\Gamma(\alpha,\beta)$ are used consistently;
$\chi^2(n)=\Gamma(n/2,1/2)$ agrees with `formulas.tex:123` and with L13/L14. The only
convention conflicts found are the two in findings 5 and 6.

**Not re-reported:** Твърдение 9.7 (already fixed); everything in `REMEDIATION.md` §8; C-06,
C-17 and D-11 (formatting/thinness, out of scope for this audit — and C-17's dangling
«виж следващия пример» pointer no longer appears in the file).
