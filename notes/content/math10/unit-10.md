---
subject: Mathematics
grade: 10
unit: 10
title: Indices
hours: 0
area: Compulsory Mathematics
---

When we write $2\times2\times2\times2\times2$ we can shorten it to $2^5$. The small raised number is the **index** (or exponent or power), and it tells us how many times the **base** is multiplied by itself. Indices make very large and very small numbers easy to write: the distance to the Sun, the mass of a dust grain, the growth of bacteria. In Grade 9 you met the laws of indices for whole-number powers. This chapter extends them to **zero, negative and fractional indices**, uses them to simplify expressions, prove identities and, above all, to **solve exponential equations** such as $2^{x+1}=32$, which appear every year in the SEE.

::: key What the SEE asks from this chapter
Expect a 2- to 4-mark question such as: (i) simplify an expression using the laws of indices; (ii) evaluate a number with a fractional or negative index, e.g. $(64)^{2/3}$; (iii) **solve an exponential equation** by making the bases equal; (iv) **prove** that an expression such as $\left(\frac{x^a}{x^b}\right)^{a+b}\cdots=1$; (v) a "show that" with $2^x=3^y=6^{-z}$. Master the laws and the step "same base, so equate the powers".
:::

## 10.1 Indices: concepts, formulas and worked problems

### Index notation

In $a^n$, $a$ is the **base** and $n$ is the **index**. For a positive whole number $n$,

$$ a^n = a\times a\times\cdots\times a \quad (n\ \text{factors}) $$

Examples: $3^4=3\times3\times3\times3=81$, $(-2)^3=-8$, $(-2)^4=+16$. A negative base raised to an **odd** power is negative; to an **even** power it is positive.

### The laws of indices

::: key The laws of indices
For $a\neq0$, $b\ne 0$ and rational $m,n$:

| Law | Statement |
|---|---|
| Product | $a^m\times a^n=a^{m+n}$ |
| Quotient | $a^m\div a^n=a^{m-n}$ |
| Power of a power | $(a^m)^n=a^{mn}$ |
| Power of a product | $(ab)^n=a^nb^n$ |
| Power of a quotient | $\left(\frac{a}{b}\right)^n=\frac{a^n}{b^n}$ |
| Zero index | $a^0=1$ |
| Negative index | $a^{-n}=\frac{1}{a^n}$ |
| Fractional index | $a^{1/n}$ = $n$th root of $a$, $\quad a^{m/n}=\left(a^{1/n}\right)^m$ |
:::

These laws hold only when the **bases are the same** (product, quotient) — you cannot combine $2^3\times3^2$ using the product law.

::: derivation Why $a^0=1$ and $a^{-n}=\frac{1}{a^n}$
We use the quotient law, which we already know is true for whole numbers with $m>n$, and ask that it keep working for all numbers.

**Step 1 — zero index.** Take any $a\ne0$ and divide $a^n$ by itself. Any number divided by itself is 1, so

$$ \frac{a^n}{a^n}=1 $$

**Step 2 — apply the quotient law.** The same division gives

$$ \frac{a^n}{a^n}=a^{n-n}=a^0 $$

**Result.** Comparing the two answers, $a^0=1$.

**Step 3 — negative index.** Divide $a^0$ by $a^n$:

$$ \frac{a^0}{a^n}=\frac{1}{a^n} \quad\text{and also}\quad \frac{a^0}{a^n}=a^{0-n}=a^{-n} $$

**Result.** $a^{-n}=\frac{1}{a^n}$.

**What it means.** A negative index does not make a number negative; it turns it upside down. $2^{-3}=\frac{1}{8}$, not $-8$.
:::

::: derivation Why $a^{1/n}$ is the $n$th root
**Setting up.** We want a meaning for $a^{1/2}$ that obeys the product law.

**Step 1.** Multiply $a^{1/2}$ by itself:

$$ a^{1/2}\times a^{1/2}=a^{\frac{1}{2}+\frac{1}{2}}=a^1=a $$

**Step 2.** A number that multiplies itself to give $a$ is $\sqrt{a}$. Hence $a^{1/2}=\sqrt{a}$.

**Result.** In the same way $\left(a^{1/n}\right)^n=a$, so $a^{1/n}$ is the $n$th root of $a$, and by the power-of-a-power law $a^{m/n}=\left(a^{1/n}\right)^m$.

**What it means.** $8^{1/3}=2$ because $2\times2\times2=8$, and $8^{2/3}=2^2=4$. Take the root first, then the power: the numbers stay small.
:::

```figure caption="Graphs of y = 2^x (growth) and y = (1/2)^x (decay). Both pass through (0, 1) because a⁰ = 1."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6, 3.2))
x = np.linspace(-3, 3, 200)
ax.plot(x, 2.0**x, color=ACCENT, lw=1.8, label='y = 2ˣ')
ax.plot(x, 0.5**x, color='#dc2626', lw=1.8, label='y = (1/2)ˣ')
ax.axhline(0, color=INK, lw=0.8); ax.axvline(0, color=INK, lw=0.8)
ax.plot([0], [1], 'o', color=INK, ms=4)
ax.text(0.12, 1.35, '(0, 1)', fontsize=8)
for px in (-2, 2):
    ax.plot([px], [2.0**px], 'o', color=ACCENT, ms=3.5)
ax.text(2.05, 3.6, '(2, 4)', fontsize=8, color=ACCENT)
ax.text(-2.9, 4.4, '(−2, 4)', fontsize=8, color='#dc2626')
ax.set_xlim(-3.2, 3.2); ax.set_ylim(-0.5, 8.5)
ax.set_xlabel('x', fontsize=8.5); ax.set_ylabel('y', fontsize=8.5)
ax.tick_params(labelsize=8); ax.grid(color=GRID, lw=0.5)
ax.legend(fontsize=8, frameon=False, loc='upper center')
fig.tight_layout(pad=0.4)
```

### Simplifying expressions

::: example Product and quotient laws
**Problem.** Simplify (a) $2^5\times2^3$, (b) $\frac{3^7}{3^4}$, (c) $\frac{5^6\times5^{-2}}{5^3}$.

**Solution.**
(a) $2^5\times2^3=2^{5+3}=2^8=256$.

(b) $\frac{3^7}{3^4}=3^{7-4}=3^3=27$.

(c) $\frac{5^6\times5^{-2}}{5^3}=\frac{5^{6-2}}{5^3}=5^{4-3}=5^1=5$.
:::

::: example Negative and zero indices
**Problem.** Find the value of (a) $4^{-2}$, (b) $\left(\frac{2}{3}\right)^{-3}$, (c) $7^0+3^{-1}$.

**Solution.**
(a) $4^{-2}=\frac{1}{4^2}=\frac{1}{16}$.

(b) A negative index flips the fraction: $\left(\frac{2}{3}\right)^{-3}=\left(\frac{3}{2}\right)^3=\frac{27}{8}$.

(c) $7^0+3^{-1}=1+\frac{1}{3}=\frac{4}{3}$.
:::

::: example Fractional indices
**Problem.** Evaluate (a) $64^{2/3}$, (b) $\left(\frac{27}{8}\right)^{-2/3}$, (c) $(0.0016)^{3/4}$.

**Solution.**
(a) $64^{1/3}=4$, so $64^{2/3}=4^2=16$.

(b) First flip because the index is negative: $\left(\frac{27}{8}\right)^{-2/3}=\left(\frac{8}{27}\right)^{2/3}$. Now $\left(\frac{8}{27}\right)^{1/3}=\frac{2}{3}$, so the answer is $\left(\frac{2}{3}\right)^2=\frac{4}{9}$.

(c) $0.0016=\frac{16}{10000}=\left(\frac{2}{10}\right)^4$, so $(0.0016)^{3/4}=\left(\frac{2}{10}\right)^3=0.008$.
:::

::: example Simplifying with letters
**Problem.** Simplify $\frac{(x^3)^2\times x^{-4}}{x^{5}}$ and write the answer with a positive index.

**Solution.** $(x^3)^2=x^6$. Then

$$ \frac{x^6\times x^{-4}}{x^5}=\frac{x^{2}}{x^{5}}=x^{2-5}=x^{-3}=\frac{1}{x^3} $$
:::

::: example Powers of different bases
**Problem.** Simplify $\frac{2^{n+2}-2^{n}}{2^{n+1}}$.

**Solution.** Take $2^n$ common in the numerator: $2^{n+2}=2^n\times2^2=4\cdot2^n$. So

$$ \frac{4\cdot 2^n-2^n}{2\cdot 2^n}=\frac{2^n(4-1)}{2\cdot2^n}=\frac{3}{2} $$
:::

::: example A tidy ratio
**Problem.** Simplify $\frac{3^{n+1}+3^{n}}{3^{n+2}-3^{n}}$.

**Solution.** Write every term with $3^n$: numerator $=3^n(3+1)=4\cdot3^n$; denominator $=3^n(9-1)=8\cdot3^n$. The ratio is

$$ \frac{4\cdot3^n}{8\cdot3^n}=\frac{1}{2} $$
:::

::: caution Common mistakes
- $2^3\times2^4=2^7$, **not** $4^7$ — the base does not change when you multiply.
- $(a+b)^2\ne a^2+b^2$; the power-of-a-product law works only for products, never for sums.
- $-3^2=-9$ but $(-3)^2=+9$. The bracket decides the base.
- $a^{-n}$ is a reciprocal, not a negative number.
- $2^3+2^3=2\times2^3=2^4$, not $2^6$: only multiplication adds the indices.
:::

### Exponential equations

An equation in which the unknown is in the index, such as $3^{x}=81$, is called an **exponential equation**. The rule that solves almost all of them is:

::: key Equal bases, equal indices
If $a^x=a^y$ with $a>0$ and $a\neq1$, then $x=y$.

Procedure: (1) write every number as a power of the **same base**; (2) simplify each side with the laws; (3) equate the indices; (4) solve the resulting ordinary equation; (5) check in the original equation.
:::

::: example The simplest type
**Problem.** Solve $2^{x+1}=32$.

**Solution.** $32=2^5$, so $2^{x+1}=2^5$. Equating the indices: $x+1=5$, hence $x=4$.

**Check.** $2^{4+1}=2^5=32$. ✓
:::

::: example Base on both sides is a power of a smaller base
**Problem.** Solve $9^{x}=3^{x+2}$.

**Solution.** $9=3^2$, so $9^x=3^{2x}$. The equation becomes $3^{2x}=3^{x+2}$, so $2x=x+2$ and $x=2$.

**Check.** $9^2=81$ and $3^{4}=81$. ✓
:::

::: example Fractions as bases
**Problem.** Solve $\left(\frac{1}{2}\right)^{x}=8$.

**Solution.** $\frac{1}{2}=2^{-1}$, so $\left(\frac{1}{2}\right)^x=2^{-x}$, and $8=2^3$. Thus $-x=3$, $x=-3$.

**Check.** $\left(\frac{1}{2}\right)^{-3}=2^3=8$. ✓
:::

::: example Indices that are expressions
**Problem.** Solve $3^{2x-1}=27$.

**Solution.** $27=3^3$, so $2x-1=3$, $2x=4$, $x=2$.
:::

::: example Two powers added: take a common factor
**Problem.** Solve $5^{x+1}+5^x=150$.

**Solution.** $5^{x+1}=5\times5^x$. So $5\cdot5^x+5^x=150$. Taking $5^x$ common:

$$ 5^x(5+1)=150 \;\Rightarrow\; 5^x=25=5^2 \;\Rightarrow\; x=2 $$

**Check.** $5^3+5^2=125+25=150$. ✓
:::

::: example Two powers subtracted
**Problem.** Solve $2^{x+2}-2^{x}=24$.

**Solution.** $2^{x+2}=4\cdot2^x$, so $4\cdot2^x-2^x=24$, i.e. $3\cdot2^x=24$ and $2^x=8=2^3$. Hence $x=3$.
:::

::: example Products of powers
**Problem.** Solve $3^{x}\times3^{x+1}=81$.

**Solution.** The product law gives $3^{x+x+1}=3^{2x+1}$. Since $81=3^4$, we have $2x+1=4$, so $x=\frac{3}{2}$.
:::

::: example Powers with different bases that must be split
**Problem.** Solve $4^{x+1}=8^{x-1}$.

**Solution.** $4=2^2$ and $8=2^3$. Therefore $2^{2(x+1)}=2^{3(x-1)}$, so

$$ 2x+2=3x-3 \;\Rightarrow\; x=5 $$

**Check.** $4^6=4096$ and $8^4=4096$. ✓
:::

::: example Fractional index on the unknown
**Problem.** Solve $x^{3/2}=27$.

**Solution.** Raise both sides to the power $\frac{2}{3}$ (the reciprocal of the index):

$$ x=27^{2/3}=\left(27^{1/3}\right)^2=3^2=9 $$

**Check.** $9^{3/2}=(\sqrt{9})^3=27$. ✓
:::

::: example A quadratic hidden in an exponential
**Problem.** Solve $4^x-5\cdot2^x+4=0$.

**Solution.** Since $4^x=(2^x)^2$, let $y=2^x$. The equation becomes

$$ y^2-5y+4=0 \;\Rightarrow\; (y-1)(y-4)=0 \;\Rightarrow\; y=1 \text{ or } y=4 $$

If $2^x=1=2^0$ then $x=0$. If $2^x=4=2^2$ then $x=2$. So $x=0$ or $x=2$.

**Check.** $x=0$: $1-5+4=0$ ✓. $x=2$: $16-20+4=0$ ✓.
:::

```figure caption="Solving 2ˣ = 8 from the graph: draw the horizontal line y = 8, go down to the x-axis and read x = 3."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4, 2.8))
x = np.linspace(-0.5, 3.6, 200)
ax.plot(x, 2.0**x, color=ACCENT, lw=1.8)
ax.plot([0, 3, 3], [8, 8, 0], color='#dc2626', lw=1.2, ls='--')
ax.plot([3], [8], 'o', color='#dc2626', ms=4)
ax.text(3.05, 0.3, 'x = 3', fontsize=8.5, color='#dc2626')
ax.text(0.05, 8.4, 'y = 8', fontsize=8.5, color='#dc2626')
ax.text(0.1, 2.6, 'y = 2ˣ', fontsize=8.5, color=ACCENT)
ax.axhline(0, color=INK, lw=0.8); ax.axvline(0, color=INK, lw=0.8)
ax.set_xlim(-0.5, 3.8); ax.set_ylim(-0.5, 11)
ax.set_xlabel('x', fontsize=8.5); ax.set_ylabel('y', fontsize=8.5)
ax.tick_params(labelsize=8); ax.grid(color=GRID, lw=0.5)
fig.tight_layout(pad=0.4)
```

### Proving identities with indices

::: example Product of three ratios
**Problem.** Prove that $\left(\frac{x^a}{x^b}\right)^{a+b}\times\left(\frac{x^b}{x^c}\right)^{b+c}\times\left(\frac{x^c}{x^a}\right)^{c+a}=1$.

**Solution.** By the quotient law, $\frac{x^a}{x^b}=x^{a-b}$ and so on. Then by the power law,

$$ \text{LHS}=x^{(a-b)(a+b)}\times x^{(b-c)(b+c)}\times x^{(c-a)(c+a)} $$

Using $(p-q)(p+q)=p^2-q^2$, the total index is

$$ (a^2-b^2)+(b^2-c^2)+(c^2-a^2)=0 $$

So LHS $=x^0=1=$ RHS. Proved.
:::

::: example Two reciprocals add to 1
**Problem.** Show that $\frac{1}{1+x^{a-b}}+\frac{1}{1+x^{b-a}}=1$.

**Solution.** Let $p=x^{a-b}$. Then $x^{b-a}=\frac{1}{p}$, and

$$ \frac{1}{1+p}+\frac{1}{1+\frac{1}{p}}=\frac{1}{1+p}+\frac{p}{p+1}=\frac{1+p}{1+p}=1 $$

Proved.
:::

::: example $2^x=3^y=6^{-z}$
**Problem.** If $2^x=3^y=6^{-z}$, prove that $\frac{1}{x}+\frac{1}{y}+\frac{1}{z}=0$.

**Solution.** Let $2^x=3^y=6^{-z}=k$. Take the $x$th, $y$th and $(-z)$th roots:

$$ 2=k^{1/x},\qquad 3=k^{1/y},\qquad 6=k^{-1/z} $$

Since $6=2\times3$,

$$ k^{-1/z}=k^{1/x}\times k^{1/y}=k^{\frac{1}{x}+\frac{1}{y}} $$

The bases are equal, so the indices are equal: $-\frac{1}{z}=\frac{1}{x}+\frac{1}{y}$, that is $\frac{1}{x}+\frac{1}{y}+\frac{1}{z}=0$. Proved.
:::

::: example Value of a power expression
**Problem.** If $a^{x}=b$, $b^{y}=c$ and $c^{z}=a$, prove that $xyz=1$.

**Solution.** Substitute step by step: $a=c^z=(b^y)^z=b^{yz}=(a^x)^{yz}=a^{xyz}$. So $a^1=a^{xyz}$ and, equating indices, $xyz=1$. Proved.
:::

::: tip The one idea behind every question
Whatever the question, ask: "**Can I write every number with one common base?**" If yes, the laws collapse the question to an ordinary equation in the indices. If the bases are $4,8,16,32,64$, use base 2; for $9,27,81$ use base 3; for $25,125$ use base 5.
:::

## 10.2 Exercises of the SEE type

### Method for any question

1. Write every base as a power of one common prime (2, 3 or 5 usually). Remember $\frac{1}{2^n}=2^{-n}$.
2. Use the laws to reach a single power on each side.
3. **Equate the indices** and solve the linear (or quadratic) equation.
4. For sums of powers like $5^{x+1}+5^x$, take the smallest power as a common factor.
5. For a proof, work from the left side only, show every law you use, and end with "= RHS. Proved."
6. Check the answer by substituting back.

::: example SEE type: evaluate
**Problem.** Simplify $\frac{(25)^{3/2}\times(243)^{-1/5}}{5^{3}\times3^{-1}}$.

**Solution.** $25^{3/2}=(5^2)^{3/2}=5^3=125$. $243=3^5$, so $243^{-1/5}=3^{-1}=\frac{1}{3}$. The numerator is $125\times\frac{1}{3}$; the denominator is $125\times\frac{1}{3}$. The ratio is $1$.
:::

::: example SEE type: solve
**Problem.** Solve $2^{x}+2^{x+1}+2^{x+2}=56$.

**Solution.** $2^x(1+2+4)=56$, so $7\cdot2^x=56$, $2^x=8$, $x=3$.
:::

::: example SEE type: solve with an unknown base
**Problem.** Solve $\left(\frac{3}{5}\right)^{x-1}=\left(\frac{5}{3}\right)^{x+3}$.

**Solution.** Write the right side as $\left(\frac{3}{5}\right)^{-(x+3)}$. Equating the indices: $x-1=-(x+3)$, so $2x=-2$ and $x=-1$.

**Check.** LHS $=\left(\frac{3}{5}\right)^{-2}=\frac{25}{9}$; RHS $=\left(\frac{5}{3}\right)^{2}=\frac{25}{9}$. ✓
:::

::: example SEE type: find the value of an expression
**Problem.** Find the value of $\left(\frac{1}{27}\right)^{-2/3}\times 16^{-3/4}\div 2^{-1}$.

**Solution.** Take each factor separately.

- $\left(\frac{1}{27}\right)^{-2/3}=27^{2/3}=(27^{1/3})^2=3^2=9$.
- $16^{-3/4}=\frac{1}{16^{3/4}}=\frac{1}{(16^{1/4})^3}=\frac{1}{2^3}=\frac{1}{8}$.
- Dividing by $2^{-1}$ is the same as multiplying by $2$.

So the value is $9\times\frac{1}{8}\times2=\frac{9}{4}$.
:::

::: example SEE type: base 5 and base 25 mixed
**Problem.** Solve $25^{x-1}=\frac{1}{125}$.

**Solution.** $25=5^2$ and $\frac{1}{125}=5^{-3}$. Then $5^{2(x-1)}=5^{-3}$, so $2x-2=-3$, $2x=-1$ and $x=-\frac{1}{2}$.

**Check.** $25^{-3/2}=\frac{1}{25^{3/2}}=\frac{1}{5^3}=\frac{1}{125}$. ✓
:::

::: example SEE type: the unknown is in two places
**Problem.** Solve $2^{x+1}\times 4^{x-1}=16$.

**Solution.** $4^{x-1}=2^{2x-2}$. By the product law the left side is $2^{(x+1)+(2x-2)}=2^{3x-1}$. Since $16=2^4$, we need $3x-1=4$, so $x=\frac{5}{3}$.

**Check.** $2^{8/3}\times4^{2/3}=2^{8/3}\times2^{4/3}=2^{4}=16$. ✓
:::

::: example SEE type: simplify to a single power
**Problem.** Simplify $\frac{(a^2b^{-1})^3\times(ab^2)^{-2}}{a^{2}b^{-3}}$.

**Solution.** Open the brackets with the power-of-a-product law:

$$ (a^2b^{-1})^3=a^6b^{-3},\qquad (ab^2)^{-2}=a^{-2}b^{-4} $$

Multiply: $a^{6-2}b^{-3-4}=a^4b^{-7}$. Divide by $a^2b^{-3}$: $a^{4-2}b^{-7+3}=a^2b^{-4}=\frac{a^2}{b^4}$.
:::

::: example SEE type: a word problem
**Problem.** A culture of bacteria doubles every hour. At 8 a.m. there are 5 bacteria. After how many hours will there be 640 bacteria?

**Solution.** After $t$ hours the number is $5\times2^t$. Put $5\times 2^t=640$, so $2^t=128=2^7$ and $t=7$ hours, i.e. at 3 p.m.
:::

::: example SEE type: square roots as indices
**Problem.** Simplify $\frac{\sqrt{x^{3}}\times x^{-1/2}}{x^{1/2}}$ for $x>0$.

**Solution.** $\sqrt{x^3}=x^{3/2}$. The expression is $\frac{x^{3/2}\times x^{-1/2}}{x^{1/2}}=\frac{x^{1}}{x^{1/2}}=x^{1/2}=\sqrt{x}$.
:::

::: tip How to write the proof in the exam
Write the given statement, then **LHS =** and one law per line (the markers love to see "by the law $a^m\times a^n=a^{m+n}$"). End with **= RHS. Proved.** A neat proof earns full marks even if one arithmetic slip happens in a side calculation.
:::

## Chapter summary

- $a^m\times a^n=a^{m+n}$, $\ a^m\div a^n=a^{m-n}$, $\ (a^m)^n=a^{mn}$, $\ (ab)^n=a^nb^n$.
- $a^0=1$ and $a^{-n}=\frac{1}{a^n}$; a negative index flips the base.
- $a^{1/n}$ is the $n$th root of $a$ and $a^{m/n}=\left(a^{1/n}\right)^m$: root first, then power.
- If $a^x=a^y$ ($a>0,\ a\ne1$) then $x=y$.
- To solve an exponential equation: common base, simplify, equate indices, check.
- For sums like $a^{x+k}\pm a^x$ take the smallest power as the common factor.
- Equations such as $4^x-5\cdot2^x+4=0$: put $y=2^x$ and solve the quadratic in $y$.
- To prove an identity: simplify one side with the laws until it equals the other.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The value of $a^0$ ($a\ne0$) is <span class="marks">[1]</span>
   (a) 0 (b) 1 (c) $a$ (d) undefined
2. $2^{-3}$ is equal to <span class="marks">[1]</span>
   (a) $-8$ (b) $-6$ (c) $\frac{1}{8}$ (d) $\frac{1}{6}$
3. $8^{2/3}$ is equal to <span class="marks">[1]</span>
   (a) 2 (b) 4 (c) 16 (d) 64
4. If $3^{x}=81$ then $x$ is <span class="marks">[1]</span>
   (a) 3 (b) 4 (c) 27 (d) 5
5. $a^m\times a^n$ is equal to <span class="marks">[1]</span>
   (a) $a^{mn}$ (b) $a^{m-n}$ (c) $a^{m+n}$ (d) $(2a)^{m+n}$

::: note Answers to Group A
**1.** (b) — $a^0=1$.
**2.** (c) — $2^{-3}=\frac{1}{2^3}=\frac{1}{8}$.
**3.** (b) — $8^{1/3}=2$, then $2^2=4$.
**4.** (b) — $81=3^4$.
**5.** (c) — add the indices.
:::

**Group B — Short answer (2 marks each)**

1. Simplify $\frac{2^{5}\times 2^{-2}}{2^{1}}$. <span class="marks">[2]</span>
2. Evaluate $\left(\frac{16}{81}\right)^{3/4}$. <span class="marks">[2]</span>
3. Solve $5^{x-2}=125$. <span class="marks">[2]</span>
4. Solve $4^{x}=8^{x-1}$. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $2^{5-2-1}=2^2=4$.
**2.** $\frac{16}{81}=\left(\frac{2}{3}\right)^4$, so the answer is $\left(\frac{2}{3}\right)^3=\frac{8}{27}$.
**3.** $125=5^3$, so $x-2=3$ and $x=5$.
**4.** $2^{2x}=2^{3x-3}$, so $2x=3x-3$ and $x=3$.
:::

**Group C — Short answer (3 marks each)**

1. Solve $3^{x+1}+3^{x}=36$. <span class="marks">[3]</span>
2. Simplify $\frac{2^{n+3}-2^{n+1}}{2^{n+2}}$. <span class="marks">[3]</span>
3. Solve $x^{2/3}=16$ (take $x>0$). <span class="marks">[3]</span>
4. Prove that $\frac{1}{1+x^{p-q}}+\frac{1}{1+x^{q-p}}=1$. <span class="marks">[3]</span>

::: note Answers to Group C
**1.** $3\cdot3^x+3^x=4\cdot3^x=36$, so $3^x=9$ and $x=2$.
**2.** Numerator $=2^n(8-2)=6\cdot2^n$; denominator $=4\cdot2^n$; ratio $=\frac{3}{2}$.
**3.** Raise to $\frac{3}{2}$: $x=16^{3/2}=4^3=64$.
**4.** Put $t=x^{p-q}$; the sum is $\frac{1}{1+t}+\frac{t}{t+1}=1$.
:::

**Group D — Long answer (4 marks each)**

1. Solve $4^{x}-6\cdot2^{x}+8=0$. <span class="marks">[4]</span>
2. Prove that $\left(\frac{x^m}{x^n}\right)^{m+n}\times\left(\frac{x^n}{x^l}\right)^{n+l}\times\left(\frac{x^l}{x^m}\right)^{l+m}=1$. <span class="marks">[4]</span>
3. If $2^x=3^y=6^{-z}$, show that $xy+yz+zx=0$. <span class="marks">[4]</span>
4. Solve $2^{x+3}+2^{x+1}=40$ and verify your answer. <span class="marks">[4]</span>

::: note Answers to Group D
**1.** Let $y=2^x$: $y^2-6y+8=0$, $(y-2)(y-4)=0$, so $y=2$ or $4$, giving $x=1$ or $x=2$.
**2.** The index sum is $(m^2-n^2)+(n^2-l^2)+(l^2-m^2)=0$, so the product is $x^0=1$.
**3.** Let the common value be $k$: $2=k^{1/x}$, $3=k^{1/y}$, $6=k^{-1/z}$. From $6=2\times3$ we get $-\frac{1}{z}=\frac{1}{x}+\frac{1}{y}$, i.e. $\frac{1}{x}+\frac{1}{y}+\frac{1}{z}=0$. Multiplying by $xyz$ gives $yz+xz+xy=0$.
**4.** $8\cdot2^x+2\cdot2^x=10\cdot2^x=40$, $2^x=4$, $x=2$. Check: $2^5+2^3=32+8=40$ ✓.
:::
