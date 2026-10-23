---
subject: Mathematics
grade: 8
unit: 3
title: Rational and Irrational Numbers
hours: 0
area: Compulsory Mathematics
---

Every fraction you can write as $\frac{p}{q}$, with $p$ and $q$ integers
and $q$ not zero, is a **rational number**, and as a decimal it either stops or
repeats. But some numbers cannot be written that way at all: $\sqrt{2}$ has a
decimal expansion that goes on for ever without repeating, and so does $\pi$.
This chapter sorts numbers into these two families, shows how to work with
square roots, and introduces the scientific notation used for very large and
very small quantities.

::: key What this chapter asks of you
You should be able to decide whether a number is rational or irrational, convert
a terminating or recurring decimal into a fraction, simplify surds and
rationalise a simple denominator, write a number in scientific notation and
multiply or divide numbers written that way.
:::

## 3.1 Rational numbers

A **rational number** is a number that can be written in the form
$\frac{p}{q}$, where $p$ and $q$ are integers and $q\ne0$. Every integer is
rational, because $5=\frac51$; every terminating decimal is rational, because
$0.25=\frac{25}{100}=\frac14$.

A rational number in its lowest terms, when written as a decimal, either

- **terminates**, such as $\frac{3}{8}=0.375$, or
- **recurs**, such as $\frac13=0.333\dots$ and
  $\frac{5}{11}=0.454545\dots$

| Decimal | Fraction | Type |
|---|---|---|
| 0.75 | $\frac34$ | terminating |
| 0.2 | $\frac15$ | terminating |
| $0.\overline{3}$ | $\frac13$ | recurring, one digit |
| $0.\overline{27}$ | $\frac{3}{11}$ | recurring, two digits |

The bar over the digits means those digits repeat for ever:
$0.\overline{27}=0.272727\dots$

### 3.1.1 Turning a recurring decimal into a fraction

::: example One repeating digit
**Problem.** Express $0.\overline{7}$ as a fraction in its lowest terms.

**Solution.** Let $x=0.\overline{7}=0.777\dots$ Then $10x=7.777\dots$

Subtract the first from the second:

$$10x-x=7.777\dots-0.777\dots\;\Longrightarrow\;9x=7
\;\Longrightarrow\;x=\frac79$$

**Check.** $7\div9=0.777\dots$ ✓. Dividing by 9 gives a single repeating digit,
which is why the answer has 9 in the denominator.
:::

::: example Two repeating digits
**Problem.** Express $0.\overline{45}$ as a fraction in its lowest terms.

**Solution.** Let $x=0.\overline{45}=0.454545\dots$ and multiply by 100,
because two digits repeat:

$$100x=45.4545\dots$$

Subtracting $x$:

$$99x=45\;\Longrightarrow\;x=\frac{45}{99}=\frac{5}{11}$$

**Check.** $5\div11=0.4545\dots$ ✓. The rule is: one repeating digit means
multiply by 10 and subtract, two digits by 100, and so on.
:::

::: caution Distinguish a recurring decimal from an irrational number
$0.333\dots$ repeats, so it is rational: $\frac13$. A number such as
$0.101001000100001\dots$, where the gap between the 1's grows, does **not**
repeat, and it is irrational. "Goes on for ever" alone does not make a number
irrational; "goes on for ever **without repeating**" does.
:::

## 3.2 Irrational numbers

An **irrational number** cannot be written as a fraction of two integers. Its
decimal expansion goes on for ever without repeating.

| Number | Why it is irrational |
|---|---|
| $\sqrt{2}=1.41421356\dots$ | no fraction squares to exactly 2 |
| $\sqrt{3}=1.73205080\dots$ | likewise |
| $\pi=3.14159265\dots$ | the ratio of a circle's circumference to its diameter |

Numbers of the form $\sqrt{n}$ where $n$ is a positive integer that is **not a
perfect square** are irrational. So $\sqrt{2}$, $\sqrt{3}$, $\sqrt{5}$, $\sqrt{7}$,
$\sqrt{8}$ and $\sqrt{10}$ are all irrational, while $\sqrt{1}$, $\sqrt{4}$, $\sqrt{9}$
and $\sqrt{16}$ are rational because they are 1, 2, 3 and 4.

A **surd** is an irrational root left in its exact form, such as $\sqrt{2}$ or
$3\sqrt{5}$. We keep them in that form rather than replacing them with a rounded
decimal, so that no accuracy is lost.

$$\sqrt{ab}=\sqrt{a}\times\sqrt{b},\qquad
\sqrt{\frac ab}=\frac{\sqrt{a}}{\sqrt{b}},\qquad
\sqrt{a^2b}=a\sqrt{b}$$

The last rule is the one used to simplify: take any perfect square you can find
out of the root.

::: example Simplifying a surd
**Problem.** Simplify $\sqrt{72}$ and $\sqrt{50}+\sqrt{18}$.

**Solution.** Look for the largest perfect-square factor.

$$\sqrt{72}=\sqrt{36\times2}=\sqrt{36}\times\sqrt{2}=6\sqrt{2}$$

For the sum, simplify each first:

$$\sqrt{50}=\sqrt{25\times2}=5\sqrt{2},\qquad
\sqrt{18}=\sqrt{9\times2}=3\sqrt{2}$$

Like surds may be added, just as like terms are:

$$5\sqrt{2}+3\sqrt{2}=8\sqrt{2}$$

**Answer.** $\sqrt{72}=6\sqrt{2}$ and $\sqrt{50}+\sqrt{18}=8\sqrt{2}$.

**Check.** $8\sqrt{2}=8\times1.414=11.31$, and
$\sqrt{50}+\sqrt{18}=7.071+4.243=11.314$ ✓.
:::

::: example Rationalising a denominator
**Problem.** Simplify $\frac{6}{\sqrt{3}}$.

**Solution.** A surd is not left in a denominator. Multiply the numerator and
the denominator by $\sqrt{3}$ — that is, by 1 in a useful form:

$$\frac{6}{\sqrt{3}}\times\frac{\sqrt{3}}{\sqrt{3}}
=\frac{6\sqrt{3}}{3}=2\sqrt{3}$$

**Answer.** $2\sqrt{3}$.

**Check.** $2\sqrt{3}=3.464$ and $6\div\sqrt{3}=6\div1.732=3.464$ ✓.
:::

### 3.2.1 Showing $\sqrt{2}$, $\sqrt{3}$, $\sqrt{5}$ on the number line

$\sqrt{2}=1.41421\dots$ never ends, so we cannot mark it by measuring a
decimal. Instead we use **Pythagoras' theorem** ($h^2=p^2+b^2$) to build a
length of exactly $\sqrt{2}$ units.

1. Draw a number line and mark 0 (point O) and 1 (point A).
2. At A draw $AB\perp OA$ with $AB=1$ unit.
3. Join OB. Then $OB=\sqrt{1^2+1^2}=\sqrt{2}$ units.
4. With O as centre and OB as radius, draw an arc to cut the number line at D.
   Then $OD=OB=\sqrt{2}$, so D is the point $\sqrt{2}$.

For $\sqrt{3}$, draw a perpendicular of 1 unit at the point $\sqrt{2}$ (at the
end of OB): the new hypotenuse is $\sqrt{(\sqrt{2})^2+1^2}=\sqrt{3}$. For
$\sqrt{5}$, use a triangle with base 2 and height 1:
$\sqrt{2^2+1^2}=\sqrt{5}$.

```figure caption="Locating $\sqrt{2}$ on the number line: OA = AB = 1 unit, so OB = $\sqrt{2}$; the arc with centre O and radius OB cuts the line at D = $\sqrt{2}$."
fig, ax = plt.subplots(figsize=(4.8, 2.6))
ax.plot([-0.6, 3.3], [0, 0], color=INK, lw=1.2)
for k in range(0, 4):
    ax.plot([k, k], [-0.06, 0.06], color=INK, lw=1)
    ax.text(k, -0.22, str(k), ha="center", fontsize=9, color=INK)
ax.plot([0, 1, 1, 0], [0, 0, 1, 0], color=ACCENT, lw=1.4)
ax.plot([0.9, 0.9, 1.0], [0, 0.1, 0.1], color=ACCENT, lw=0.8)
t = np.linspace(0, np.pi/4, 60)
r = np.sqrt(2)
ax.plot(r*np.cos(t), r*np.sin(t), color=SERIES[1], lw=1.2, ls="--")
ax.plot([r], [0], "o", color=SERIES[1], ms=5)
ax.text(-0.08, 0.1, "O", fontsize=9, ha="right", color=INK)
ax.text(1.05, -0.4, "A", fontsize=9, color=INK)
ax.text(1.06, 1.02, "B", fontsize=9, color=INK)
ax.text(1.45, 0.12, "D", fontsize=9, color=SERIES[1])
ax.text(1.42, -0.42, "$\\sqrt{2}$", fontsize=10, ha="center", color=SERIES[1])
ax.text(1.12, 0.5, "1", fontsize=9, color=ACCENT)
ax.text(0.5, -0.4, "1", fontsize=9, color=ACCENT, ha="center")
ax.text(0.3, 0.6, "$\\sqrt{2}$", fontsize=10, color=ACCENT)
ax.set_xlim(-0.7, 3.4); ax.set_ylim(-0.6, 1.3); ax.set_aspect("equal"); ax.axis("off")
```

::: tip Between which two integers?
To place a surd, find the perfect squares on either side of the number inside
it. For $\sqrt{20}$: $16<20<25$, so $4<\sqrt{20}<5$. For a closer answer,
$4.4^2=19.36$ and $4.5^2=20.25$, so $\sqrt{20}\approx4.47$. This costs ten
seconds and is the standard way to check a surd answer.
:::

## 3.3 Scientific notation

**Scientific notation** writes a number as a product of a number between 1 and
10 and a power of 10:

$$N=a\times10^n,\qquad 1\le a<10$$

| Number | In scientific notation |
|---|---|
| 45,000 | $4.5\times10^4$ |
| 320,000,000 | $3.2\times10^8$ |
| 0.0006 | $6\times10^{-4}$ |
| 0.00000072 | $7.2\times10^{-7}$ |

**Rules for the index.** Moving the decimal point $n$ places to the left
multiplies the number by $10^n$ and gives index $+n$; moving it $n$ places to the
right gives index $-n$.

### 3.3.1 Multiplying and dividing

Multiply the first parts and add the indices; divide the first parts and
subtract the indices.

$$(3\times10^5)\times(2\times10^3)=6\times10^8$$

$$\frac{8\times10^7}{2\times10^2}=4\times10^5$$

If the first part is not between 1 and 10 after the operation, adjust it:
$12\times10^3=1.2\times10^4$.

### 3.3.2 Adding and subtracting

Two numbers can be added or subtracted in scientific notation only when they
have the **same power of 10**. If the powers differ, rewrite one of them first.

::: example Addition and subtraction
**Problem.** Simplify (a) $3.4\times10^2+4.57\times10^3$
(b) $1.33\times10^5-4.9\times10^4$.

**Solution.**
(a) Make both powers $10^3$: $3.4\times10^2=0.34\times10^3$.

$0.34\times10^3+4.57\times10^3=(0.34+4.57)\times10^3=4.91\times10^3$

Check: $340+4570=4910=4.91\times10^3$ ✓.

(b) $4.9\times10^4=0.49\times10^5$, so

$1.33\times10^5-0.49\times10^5=(1.33-0.49)\times10^5=0.84\times10^5=8.4\times10^4$

Check: $133000-49000=84000$ ✓.
:::

::: example From scientific notation to an ordinary number
**Problem.** Write (a) $4.579\times10^6$ and (b) $3.579\times10^{-4}$ as
ordinary decimal numbers.

**Solution.**
(a) Positive index: move the point 6 places to the **right**.
$4.579\times10^6=4.579\times1\,000\,000=4\,579\,000$.

(b) Negative index: $10^{-4}=\frac{1}{10^4}$, so move the point 4 places to the
**left**. $3.579\times10^{-4}=\frac{3.579}{10\,000}=0.0003579$.
:::

::: example Word problem — tanks of water
**Problem.** One tanker holds $1.5\times10^4$ litres and another holds
$7.0\times10^3$ litres. Find the total in scientific notation.

**Solution.** $7.0\times10^3=0.70\times10^4$.
Total $=(1.5+0.70)\times10^4=2.2\times10^4$ litres ($=22\,000$ litres).
:::

::: example A calculation in scientific notation
**Problem.** Simplify
$\frac{(4\times10^6)\times(3\times10^{-2})}{6\times10^2}$.

**Solution.** Multiply in the numerator first: the first parts give
$4\times3=12$, and the indices add: $6+(-2)=4$. So the numerator is
$12\times10^4$.

Now divide: $\frac{12}{6}=2$, and the indices subtract: $4-2=2$.

$$\frac{(4\times10^6)\times(3\times10^{-2})}{6\times10^2}=2\times10^2=200$$

**Check.** The numerator is $4\,000\,000\times0.03=120\,000$, and
$120\,000\div600=200$ ✓.
:::

::: example A very large quantity
**Problem.** Light travels at $3\times10^8$ m/s. How far does it travel in one
day?

**Solution.** Seconds in a day:
$24\times60\times60=86\,400=8.64\times10^4$ s.

$$\text{distance}=3\times10^8\times8.64\times10^4
=25.92\times10^{12}=2.592\times10^{13}\ \text{m}$$

**Answer.** About $2.59\times10^{13}$ m, which is 25.92 billion kilometres.

**Check.** One light year is about $9.46\times10^{12}$ km, that is
$9.46\times10^{15}$ m, and a day is $\frac{1}{365}$ of a year, so the daily
distance should be about $2.6\times10^{13}$ m ✓.
:::

## 3.4 Placing numbers on the number line

Rational and irrational numbers together fill the number line with no gaps. Any
point on the line is a real number, and every real number is either rational or
irrational.

The **real numbers** $R$ are the union of the rational numbers $Q$ and the
irrational numbers $Ir$: $R=Q\cup Ir$. $Q$ and $Ir$ are **disjoint**, since no
number is both. The sets sit inside one another:
$N\subset W\subset Z\subset Q\subset R$ and $Ir\subset R$.

| Statement | True or false | Reason |
|---|---|---|
| Every integer is rational | true | $5=\frac51$ |
| Every rational number is an integer | false | $\frac12$ is not an integer |
| $\sqrt{9}$ is irrational | false | $\sqrt{9}=3$, an integer |
| $\pi$ is rational | false | its decimal never repeats |
| 0 is rational | true | $0=\frac01$ |

## 3.5 The number line as a map of the number system

Every number you will meet in Grade 8 has a home on the number line, and the
line shows at a glance which sets sit inside which.

```figure caption="The number system as nested sets. Every natural number is a whole number, every whole number an integer, every integer a rational number — and the irrationals sit outside the rationals but still on the real line."
fig, ax = plt.subplots(figsize=(4.9, 3.3))
rings = [("Real numbers", 0.46, SERIES[2], 0.10),
         ("Rational", 0.36, SERIES[1], 0.14),
         ("Integers", 0.26, SERIES[0], 0.18),
         ("Whole", 0.17, SERIES[4], 0.22),
         ("Natural", 0.09, SERIES[3], 0.30)]
for lab, r, col, alpha in rings:
    ax.add_patch(matplotlib.patches.Circle((0.5, 0.48), r, facecolor=col,
                                           alpha=alpha, edgecolor=col,
                                           linewidth=1.2))
labels = [("Natural  1, 2, 3 ...", 0.50, 0.48, 7.2),
          ("Whole  0", 0.50, 0.60, 7.2),
          ("Integers  -3", 0.50, 0.68, 7.2),
          ("Rational  3/4, 0.25", 0.50, 0.78, 7.2),
          ("Real (outer ring = irrational: $\\sqrt{2}$, $\\pi$)", 0.50, 0.90, 7.0)]
for t, x, y, fs in labels:
    ax.text(x, y, t, ha="center", va="center", color=INK, fontsize=fs)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect("equal")
ax.axis("off")
```

| Set | Symbol used in class | Members | Not members |
|---|---|---|---|
| Natural numbers | N | $1, 2, 3, \ldots$ | $0$, $-2$, $\frac{1}{2}$ |
| Whole numbers | W | $0, 1, 2, \ldots$ | $-2$, $\frac{1}{2}$ |
| Integers | Z | $\ldots, -2, -1, 0, 1, 2, \ldots$ | $\frac{1}{2}$, $\sqrt{3}$ |
| Rational numbers | Q | $\frac{p}{q}$, $q \neq 0$; terminating or recurring decimals | $\sqrt{2}$, $\pi$ |
| Irrational numbers | — | non-terminating, non-recurring decimals | $\frac{22}{7}$ (it is rational) |

::: caution Two traps that cost marks
$\frac{22}{7}$ is **rational**; it is only an approximation of $\pi$, which is
irrational. And $\sqrt{9} = 3$ is **rational** — a square root is irrational
only when the number under it is not a perfect square.
:::

::: example Deciding rational or irrational
**Question.** Classify each number as rational or irrational, giving a reason:
(i) $0.\overline{27}$ (ii) $\sqrt{45}$ (iii) $\sqrt{49}$ (iv) $3.141141114\ldots$

**Answer.**
(i) **Rational** — a recurring decimal; indeed $0.\overline{27} = \frac{27}{99} = \frac{3}{11}$.
(ii) **Irrational** — $45$ is not a perfect square, and $\sqrt{45} = 3\sqrt{5}$.
(iii) **Rational** — $\sqrt{49} = 7 = \frac{7}{1}$.
(iv) **Irrational** — the decimal neither terminates nor settles into a repeating block.
:::

::: note Activity — build a number line on the wall
Take a two-metre strip of chart paper. Mark $-5$ to $5$ at 10 cm intervals. Now
place these numbers as accurately as you can, writing each on a small card and
pinning it: $-\frac{7}{2}$, $-\sqrt{2}$, $0.75$, $\frac{5}{3}$, $\sqrt{5}$,
$\pi$, $\frac{22}{7}$.
**Discussion:** $\pi$ and $\frac{22}{7}$ land almost on the same spot. How far
apart are they really? (Work to four decimal places.)
:::

## Chapter summary

- A rational number is $\frac{p}{q}$ with $q\ne0$; as a decimal it terminates or
  recurs.
- A recurring decimal becomes a fraction by multiplying by 10, 100 or 1000 for
  one, two or three repeating digits, subtracting, and solving.
- An irrational number never repeats and cannot be written as a fraction;
  $\sqrt{n}$ is irrational unless $n$ is a perfect square.
- A surd is an exact irrational root; simplify by taking out the largest
  perfect-square factor, and add only like surds.
- Rationalise a denominator by multiplying the top and bottom by the surd.
- $\sqrt{2}$, $\sqrt{3}$, $\sqrt{5}$ are marked on a number line with right
  triangles (Pythagoras) and an arc from 0.
- $R=Q\cup Ir$, and $Q$ and $Ir$ are disjoint.
- Scientific notation is $a\times10^n$ with $1\le a<10$; to add or subtract,
  first make the powers of 10 equal; multiply by multiplying
  the first parts and adding the indices, divide by dividing and subtracting.

## Practice questions

**Group A — Objective (1 mark each)**

1. Which of these is irrational? <span class="marks">[1]</span>
   (a) $\frac34$ (b) $0.\overline{6}$ (c) $\sqrt{16}$ (d) $\sqrt{5}$
2. $0.00045$ in scientific notation is <span class="marks">[1]</span>
   (a) $45\times10^{-5}$ (b) $4.5\times10^{-4}$ (c) $4.5\times10^{4}$
   (d) $0.45\times10^{-3}$
3. $\sqrt{50}$ simplified is <span class="marks">[1]</span>
   (a) $5\sqrt{2}$ (b) $2\sqrt{5}$ (c) $25\sqrt{2}$ (d) $10\sqrt{5}$
4. $0.\overline{3}$ as a fraction is <span class="marks">[1]</span>
   (a) $\frac{3}{10}$ (b) $\frac13$ (c) $\frac{30}{100}$ (d) $\frac{3}{100}$
5. $(2\times10^3)\times(4\times10^2)$ equals <span class="marks">[1]</span>
   (a) $8\times10^5$ (b) $6\times10^5$ (c) $8\times10^6$ (d) $8\times10^1$
6. $\frac{9}{\sqrt{3}}$ simplified is <span class="marks">[1]</span>
   (a) $3\sqrt{3}$ (b) $\sqrt{27}$ (c) 3 (d) $9\sqrt{3}$

::: note Answers to Group A
**1.** (d) — 5 is not a perfect square.
**2.** (b) — the decimal point moves four places to the right.
**3.** (a) — $50=25\times2$.
**4.** (b) — $9x=3$ gives $x=\frac13$.
**5.** (a) — $2\times4=8$ and $3+2=5$.
**6.** (a) — $\frac{9\sqrt{3}}{3}=3\sqrt{3}$.
:::

**Group B — Short answer (2 marks each)**

1. Write $0.\overline{6}$ and $0.\overline{18}$ as fractions.
   <span class="marks">[2]</span>
2. Simplify $\sqrt{48}$ and $\sqrt{12}+\sqrt{27}$.
   <span class="marks">[2]</span>
3. Write 0.000000573 in scientific notation and write
   $6.4\times10^{-3}$ as a decimal. <span class="marks">[2]</span>
4. Show that $\sqrt{2}$ lies between 1.4 and 1.5.
   <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $x=0.\overline{6}$ gives $9x=6$, so $x=\frac69=\frac23$.
$x=0.\overline{18}$ gives $99x=18$, so $x=\frac{18}{99}=\frac{2}{11}$.
**2.** $\sqrt{48}=\sqrt{16\times3}=4\sqrt{3}$. And
$\sqrt{12}=2\sqrt{3}$, $\sqrt{27}=3\sqrt{3}$, so the sum is $5\sqrt{3}$.
**3.** $0.000000573=5.73\times10^{-7}$; and
$6.4\times10^{-3}=0.0064$.
**4.** $1.4^2=1.96$ and $1.5^2=2.25$. Since $1.96<2<2.25$, taking square roots
gives $1.4<\sqrt{2}<1.5$.
:::

**Group C — Long answer (4 marks each)**

1. Express $2.\overline{3}$ (the digit 3 repeating after a whole part of 2) as
   a fraction in its lowest terms. <span class="marks">[4]</span>
2. Simplify $\frac{(5\times10^{-3})\times(6\times10^7)}{3\times10^4}$ and give
   the answer both in scientific notation and as an ordinary number. Explain
   each step. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** Let $x=2.\overline{3}=2.333\dots$ Then $10x=23.333\dots$
Subtracting: $10x-x=23.333\dots-2.333\dots$, so $9x=21$ and
$x=\frac{21}{9}=\frac{7}{3}$.
**Check.** $7\div3=2.333\dots$ ✓. The whole part is removed automatically by the
subtraction, because both numbers have the same fractional part.
**2.** **Step 1 — multiply in the numerator.** First parts:
$5\times6=30$. Indices: $-3+7=4$. So the numerator is $30\times10^4$.
**Step 2 — divide.** First parts: $\frac{30}{3}=10$. Indices: $4-4=0$. So the
result is $10\times10^0=10$. **Step 3 — put it in scientific notation.**
$10=1\times10^1$. **Answer.** $1\times10^1$, which is the ordinary number 10.
**Check.** The numerator is $0.005\times60\,000\,000=300\,000$, and
$300\,000\div30\,000=10$ ✓.
:::

**Extra practice — textbook-style questions**

**1.** Write true or false: (a) The sets of rational and irrational numbers are disjoint. (b) The set of whole numbers and the set of integers are the same. (c) $\sqrt{4}$ is irrational.
**2.** Reduce to fractions: (a) $0.\overline{24}$ (b) $4.\overline{78}$ (c) $0.\overline{132}$.
**3.** Write in scientific notation: (a) 101000 (b) 0.00671 (c) 74171.7.
**4.** Simplify and write in scientific notation: (a) $1.2\times10^5+5.35\times10^6$ (b) $\frac{8.4\times10^{-4}}{1.2\times10^{-3}}$.
**5.** How many tanks, each of capacity $1.5\times10^3$ litres, are needed to store $9.0\times10^6$ litres of petrol?
**6.** Show $\sqrt{5}$ on a number line.

::: note Extra practice — answers
**1.** (a) True (b) False — integers also contain $-1,-2,\dots$ (c) False — $\sqrt{4}=2$.
**2.** (a) $100x-x=24$, so $x=\frac{24}{99}=\frac{8}{33}$. (b) $x=4.7878\dots$, $100x=478.78\dots$, $99x=474$, $x=\frac{474}{99}=\frac{158}{33}$. (c) $1000x-x=132$, $x=\frac{132}{999}=\frac{44}{333}$.
**3.** (a) $1.01\times10^5$ (b) $6.71\times10^{-3}$ (c) $7.41717\times10^4$.
**4.** (a) $0.12\times10^6+5.35\times10^6=5.47\times10^6$. (b) $\frac{8.4}{1.2}\times10^{-4-(-3)}=7\times10^{-1}$.
**5.** $\frac{9.0\times10^6}{1.5\times10^3}=6\times10^3=6000$ tanks.
**6.** Mark O at 0 and A at 2. At A draw $AB\perp OA$, $AB=1$. Then $OB=\sqrt{2^2+1^2}=\sqrt{5}$. With centre O and radius OB, draw an arc to cut the number line at D; D represents $\sqrt{5}\approx2.24$.
:::

## Objective practice

**Choose the correct answer.** <span class="marks">[5×1=5]</span>

**1.** Which of these is irrational?
   (a) $0.25$ (b) $\frac{3}{7}$ (c) $\sqrt{9}$ (d) $\sqrt{11}$
**2.** $\frac{22}{7}$ is
   (a) irrational (b) rational (c) an integer (d) a whole number
**3.** $0.\overline{3}$ as a fraction is
   (a) $\frac{3}{10}$ (b) $\frac{1}{3}$ (c) $\frac{3}{11}$ (d) $\frac{33}{100}$
**4.** Every integer is
   (a) a natural number (b) a whole number (c) a rational number (d) irrational
**5.** $4.54\times10^{-3}-2.4\times10^{-3}$ equals
   (a) $2.14\times10^{-3}$ (b) $2.14\times10^{0}$ (c) $2.14\times10^{-6}$ (d) $6.94\times10^{-3}$

::: note Objective practice — answers
**1.** (d) — 11 is not a perfect square. **2.** (b) — it is a ratio of two integers. **3.** (b) — $\frac{3}{9}=\frac{1}{3}$. **4.** (c) — every integer can be written as $\frac{p}{1}$. **5.** (a) — same power of 10, so subtract the first parts: $4.54-2.4=2.14$.
:::
