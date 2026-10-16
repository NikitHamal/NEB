---
subject: Mathematics
grade: 8
unit: 3
title: Rational and Irrational Numbers
hours: 0
area: Compulsory Mathematics
---

Every fraction you can write as $\frac{p}{q}$, with $p$ and $q$ whole numbers
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
| $e=2.71828182\dots$ | the base of natural logarithms |

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

| Statement | True or false | Reason |
|---|---|---|
| Every integer is rational | true | $5=\frac51$ |
| Every rational number is an integer | false | $\frac12$ is not an integer |
| $\sqrt{9}$ is irrational | false | $\sqrt{9}=3$, an integer |
| $\pi$ is rational | false | its decimal never repeats |
| 0 is rational | true | $0=\frac01$ |

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
- Scientific notation is $a\times10^n$ with $1\le a<10$; multiply by multiplying
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
