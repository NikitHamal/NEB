---
subject: Mathematics
grade: 8
unit: 9
title: Indices
hours: 0
area: Compulsory Mathematics
---

An index is shorthand for repeated multiplication: $2^5$ means
$2\times2\times2\times2\times2$. The shorthand is not just a saving of ink — it
turns multiplication into addition of indices, division into subtraction, and
powers of powers into multiplication, which is why indices appear in every later
chapter of algebra, in scientific notation, and in the arithmetic of growth.
This chapter sets out the laws, shows how to simplify expressions with them, and
shows how to solve the small exponential equations the syllabus asks for.

::: key What this chapter asks of you
You should be able to state and use the five laws of indices, evaluate negative
and zero indices, simplify an algebraic expression involving indices, and solve
a simple exponential equation.
:::

## 9.1 The laws of indices

| Law | Statement | Example |
|---|---|---|
| Product | $a^m\times a^n=a^{m+n}$ | $2^3\times2^4=2^7=128$ |
| Quotient | $a^m\div a^n=a^{m-n}$ | $5^6\div5^4=5^2=25$ |
| Power of a power | $(a^m)^n=a^{mn}$ | $(3^2)^3=3^6=729$ |
| Power of a product | $(ab)^n=a^nb^n$ | $(2x)^3=8x^3$ |
| Power of a quotient | $\left(\frac ab\right)^n=\frac{a^n}{b^n}$ | $\left(\frac23\right)^2=\frac49$ |

Two more results follow from the quotient law and are used constantly:

$$a^0=1\qquad(a\ne0),\qquad a^{-n}=\frac{1}{a^n}$$

The first comes from $a^m\div a^m=a^{m-m}=a^0$, and the quotient is 1. The
second comes from $a^0\div a^n=a^{0-n}=a^{-n}$, and dividing 1 by $a^n$ gives
$\frac{1}{a^n}$.

::: caution $a^0=1$ is not $0$
Any non-zero number raised to the power zero is 1. In particular $7^0=1$,
$x^0=1$ and $(3xy)^0=1$. But $0^0$ is not defined, and $0^5$ is 0 — the zero in
the index and the zero in the base are different things.
:::

::: example Using the product and quotient laws
**Problem.** Simplify $\frac{3^5\times3^2}{3^4}$.

**Solution.** Add the indices in the numerator first:

$$3^5\times3^2=3^{5+2}=3^7$$

Then subtract: $3^7\div3^4=3^{7-4}=3^3=27$.

**Answer.** 27.

**Check.** $3^5=243$ and $3^2=9$, so the numerator is $2187$; and
$2187\div81=27$ ✓.
:::

::: example An algebraic simplification
**Problem.** Simplify $\frac{12x^5y^3}{4x^2y}$.

**Solution.** Divide the numbers, then use the quotient law on each letter:

$$\frac{12}{4}=3,\qquad \frac{x^5}{x^2}=x^{5-2}=x^3,\qquad
\frac{y^3}{y}=y^{3-1}=y^2$$

$$\frac{12x^5y^3}{4x^2y}=3x^3y^2$$

**Answer.** $3x^3y^2$.

**Check.** Put $x=2$, $y=3$: the left side is
$\frac{12\times32\times27}{4\times4\times3}=\frac{10368}{48}=216$, and the right
side is $3\times8\times9=216$ ✓.
:::

::: example Zero and negative indices
**Problem.** Evaluate $5^0+2^{-3}$ and simplify $\left(\frac{2x}{y}\right)^{-2}$.

**Solution.** $5^0=1$ and $2^{-3}=\frac{1}{2^3}=\frac18$, so

$$5^0+2^{-3}=1+\frac18=1\frac18=\frac98$$

For the second, a negative index on a fraction turns it upside down:

$$\left(\frac{2x}{y}\right)^{-2}=\left(\frac{y}{2x}\right)^{2}
=\frac{y^2}{4x^2}$$

**Answer.** $1\frac18$ and $\frac{y^2}{4x^2}$.

**Check.** For the second, put $x=1$ and $y=2$. The left side is
$\left(\frac{2}{2}\right)^{-2}=1^{-2}=1$, and the right side is
$\frac{4}{4\times1}=1$. They agree ✓. Using $x=2$, $y=1$ instead: the left side
is $4^{-2}=\frac{1}{16}$, and the right side is $\frac{1}{4\times4}=\frac{1}{16}$ ✓.
:::

## 9.2 Simplifying expressions with several laws

The order to work in: deal with the brackets first, then the powers of powers,
then the products and quotients.

::: example A three-step simplification
**Problem.** Simplify $\left(\frac{2a^3b^{-2}}{4ab}\right)^2$.

**Solution.** **Step 1 — simplify inside the bracket.** Divide the numbers:
$\frac{2}{4}=\frac12$. For $a$: $a^{3-1}=a^2$. For $b$:
$b^{-2-1}=b^{-3}$. So inside we have $\frac{a^2b^{-3}}{2}$, that is
$\frac{a^2}{2b^3}$.

**Step 2 — square everything.**

$$\left(\frac{a^2}{2b^3}\right)^2=\frac{a^{4}}{4b^{6}}$$

**Answer.** $\frac{a^4}{4b^6}$.

**Check.** Put $a=1$, $b=1$: the original is
$\left(\frac{2}{4}\right)^2=\frac14$, and the answer is $\frac14$ ✓.
:::

::: example Powers of a product
**Problem.** Simplify $(2x^2y)^3\times(3xy^2)^2$.

**Solution.** Apply the power to each factor:

$$(2x^2y)^3=2^3x^6y^3=8x^6y^3,\qquad
(3xy^2)^2=9x^2y^4$$

Now multiply, adding indices of like bases:

$$8x^6y^3\times9x^2y^4=72x^{6+2}y^{3+4}=72x^8y^7$$

**Answer.** $72x^8y^7$.

**Check.** Put $x=y=1$: the original is $2^3\times3^2=8\times9=72$, and the
answer gives $72$ ✓.
:::

## 9.3 Exponential equations

An **exponential equation** has the unknown in the index, such as
$2^x=32$. The method is to write both sides as powers of the **same base** and
then equate the indices.

$$a^m=a^n\;\Longrightarrow\;m=n\qquad(a>0,\ a\ne1)$$

::: example Solving by making the bases equal
**Problem.** Solve $3^x=81$.

**Solution.** Write 81 as a power of 3: $81=3^4$. So

$$3^x=3^4\;\Longrightarrow\;x=4$$

**Answer.** $x=4$.

**Check.** $3^4=81$ ✓.
:::

::: example An equation with a second term
**Problem.** Solve $2^{x+1}=64$.

**Solution.** $64=2^6$, so $2^{x+1}=2^6$ and therefore $x+1=6$, giving $x=5$.

**Answer.** $x=5$.

**Check.** $2^{5+1}=2^6=64$ ✓.
:::

::: example An equation with a power on both sides
**Problem.** Solve $9^{x}=27^{2}$.

**Solution.** Write both numbers as powers of 3: $9=3^2$ and $27=3^3$. So

$$(3^2)^x=(3^3)^2\;\Longrightarrow\;3^{2x}=3^{6}$$

Equating indices: $2x=6$, so $x=3$.

**Answer.** $x=3$.

**Check.** $9^3=729$ and $27^2=729$ ✓.
:::

::: caution The base must be the same before you compare indices
From $2^x=8^2$ you may **not** write $x=2$. Change the right side to the base 2
first: $8^2=(2^3)^2=2^6$, so $x=6$. Comparing indices of different bases is not
allowed.
:::

## 9.4 The laws of indices in one place

```figure caption="How fast a power grows. Doubling just ten times multiplies a quantity by more than a thousand — this is why indices are used for very large and very small numbers."
n = np.arange(0, 11)
vals = 2.0 ** n
fig, ax = plt.subplots(figsize=(4.7, 2.9))
ax.plot(n, vals, color=SERIES[0], marker="o", markersize=4.5, linewidth=2)
for i in (0, 5, 10):
    ax.annotate(f"$2^{{{i}}}={int(vals[i])}$", xy=(i, vals[i]),
                xytext=(i - 0.2, vals[i] + 90), fontsize=8, color=INK)
ax.set_xlabel("index n", color=MUTED, fontsize=9)
ax.set_ylabel("value of $2^n$", color=MUTED, fontsize=9)
ax.set_ylim(0, 1200)
ax.grid(color=GRID, linewidth=0.7)
ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.tick_params(colors=MUTED, labelsize=8.4)
```

| Law | Statement | Example |
|---|---|---|
| Product | $a^m \times a^n = a^{m+n}$ | $2^3 \times 2^4 = 2^7$ |
| Quotient | $\frac{a^m}{a^n} = a^{m-n}$ | $\frac{5^6}{5^2} = 5^4$ |
| Power of a power | $(a^m)^n = a^{mn}$ | $(3^2)^3 = 3^6$ |
| Power of a product | $(ab)^m = a^m b^m$ | $(2x)^3 = 8x^3$ |
| Power of a quotient | $\left(\frac{a}{b}\right)^m = \frac{a^m}{b^m}$ | $\left(\frac{2}{3}\right)^2 = \frac{4}{9}$ |
| Zero index | $a^0 = 1$, $a \neq 0$ | $7^0 = 1$ |
| Negative index | $a^{-n} = \frac{1}{a^n}$ | $4^{-2} = \frac{1}{16}$ |
| Fractional index | $a^{1/n} = \sqrt[n]{a}$ | $27^{1/3} = 3$ |

::: caution The three commonest slips
$a^m + a^n$ is **not** $a^{m+n}$ — the product law applies to multiplication,
never to addition. $(-2)^2 = 4$ but $-2^2 = -4$, because the index binds
tighter than the minus sign. And $(a+b)^2 \neq a^2 + b^2$.
:::

::: example Working with mixed indices
**Question.** Simplify $\dfrac{(2^3)^2 \times 2^{-4}}{2^{-1}}$.

**Answer.** Numerator: $(2^3)^2 = 2^6$, so $2^6 \times 2^{-4} = 2^{2}$.
Dividing: $\frac{2^2}{2^{-1}} = 2^{2-(-1)} = 2^3 = \textbf{8}$.
:::

::: example Solving for an index
**Question.** Solve $3^{2x-1} = 81$.

**Answer.** Write both sides with the same base: $81 = 3^4$.
So $2x - 1 = 4 \Rightarrow 2x = 5 \Rightarrow x = \frac{5}{2} = \textbf{2.5}$.
:::

::: note Activity — the folding paper
Fold a sheet of paper in half as many times as you can, recording the number of
layers after each fold: $1, 2, 4, 8, \ldots$ Write the count as a power of 2.
**Discussion:** Most people stop at six or seven folds. If you could fold it
30 times, the stack would be $2^{30}$ sheets thick — work out roughly how many
kilometres that is, taking one sheet as 0.1 mm.
:::

## Chapter summary

- $a^m\times a^n=a^{m+n}$; $a^m\div a^n=a^{m-n}$; $(a^m)^n=a^{mn}$;
  $(ab)^n=a^nb^n$; $\left(\frac ab\right)^n=\frac{a^n}{b^n}$.
- $a^0=1$ for every non-zero $a$, and $a^{-n}=\frac{1}{a^n}$.
- Simplify inside brackets first, then apply powers, then multiply or divide
  like bases by adding or subtracting indices.
- An exponential equation is solved by writing both sides as powers of the same
  base and equating the indices.

## Practice questions

**Group A — Objective (1 mark each)**

1. $2^3\times2^4$ equals <span class="marks">[1]</span>
   (a) $2^7$ (b) $2^{12}$ (c) $4^7$ (d) $2^1$
2. $5^0$ equals <span class="marks">[1]</span>
   (a) 0 (b) 1 (c) 5 (d) not defined
3. $3^{-2}$ equals <span class="marks">[1]</span>
   (a) $-9$ (b) $-6$ (c) $\frac19$ (d) $\frac13$
4. $(x^2)^5$ equals <span class="marks">[1]</span>
   (a) $x^7$ (b) $x^{10}$ (c) $x^{25}$ (d) $2x^5$
5. If $2^x=32$, then $x$ is <span class="marks">[1]</span>
   (a) 4 (b) 5 (c) 6 (d) 16
6. $\frac{a^6}{a^2}$ equals <span class="marks">[1]</span>
   (a) $a^3$ (b) $a^4$ (c) $a^8$ (d) $a^{12}$

::: note Answers to Group A
**1.** (a) — the indices add.
**2.** (b) — any non-zero number to the power zero is 1.
**3.** (c) — $3^{-2}=\frac{1}{9}$.
**4.** (b) — multiply the indices: $2\times5=10$.
**5.** (b) — $32=2^5$.
**6.** (b) — subtract: $6-2=4$.
:::

**Group B — Short answer (2 marks each)**

1. Simplify $4^3\times4^2\div4^4$. <span class="marks">[2]</span>
2. Simplify $\frac{15a^4b^3}{5a^2b}$. <span class="marks">[2]</span>
3. Evaluate $\left(\frac{3}{4}\right)^{-2}$. <span class="marks">[2]</span>
4. Solve $5^x=125$. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $4^{3+2-4}=4^1=4$.
**2.** $3a^{2}b^{2}$.
**3.** $\left(\frac{4}{3}\right)^2=\frac{16}{9}=1\frac79$.
**4.** $125=5^3$, so $x=3$.
:::

**Group C — Long answer (4 marks each)**

1. Simplify $\left(\frac{3x^2y^{-1}}{6xy^2}\right)^{-2}$ and give the answer
   with positive indices only. <span class="marks">[4]</span>
2. Solve $4^{x+1}=32$. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** **Step 1 — simplify inside.** $\frac{3}{6}=\frac12$; for $x$:
$x^{2-1}=x$; for $y$: $y^{-1-2}=y^{-3}$. So inside the bracket we have
$\frac{x}{2y^3}$, that is $\frac{xy^{-3}}{2}$.
**Step 2 — apply the power $-2$.**
$\left(\frac{x}{2y^3}\right)^{-2}=\left(\frac{2y^3}{x}\right)^{2}
=\frac{4y^6}{x^2}$.
**Check.** Put $x=y=1$: the original is
$\left(\frac{3}{6}\right)^{-2}=\left(\frac12\right)^{-2}=4$, and the answer gives
$\frac41=4$ ✓.
**2.** Write both sides as powers of 2: $4=2^2$ and $32=2^5$, so
$(2^2)^{x+1}=2^5$, that is $2^{2(x+1)}=2^5$. Equating indices:
$2(x+1)=5$, so $2x+2=5$, $2x=3$, and $x=1.5$.
**Check.** $4^{2.5}=4^2\times4^{0.5}=16\times2=32$ ✓.
:::

**Extra practice**

**Group B (2 marks)**

**11.** Simplify: $\dfrac{x^5 \times x^{-2}}{x^{-3}}$.
**12.** Find the value of $16^{3/4}$.

**Group C (4 marks)**

**13.** Solve: (i) $2^{x+2} = 128$ (ii) $5^{2x} = \dfrac{1}{125}$.

::: note Extra practice — answers
**11.** $x^{5-2} = x^3$; then $\frac{x^3}{x^{-3}} = x^{3+3} = x^6$.
**12.** $16^{3/4} = (2^4)^{3/4} = 2^3 = 8$.
**13.** (i) $128 = 2^7$, so $x + 2 = 7$ and $x = 5$.
(ii) $\frac{1}{125} = 5^{-3}$, so $2x = -3$ and $x = -\frac{3}{2} = -1.5$.
:::

## Objective practice

**Choose the correct answer.** <span class="marks">[5×1=5]</span>

**1.** $3^4 \times 3^2$ equals
   (a) $3^6$ (b) $3^8$ (c) $9^6$ (d) $3^2$
**2.** $5^0 + 2^{-1}$ equals
   (a) 0 (b) 1 (c) 1.5 (d) 2
**3.** $16^{1/2}$ equals
   (a) 8 (b) 4 (c) 32 (d) 2
**4.** If $3^x = 81$, then $x$ is
   (a) 3 (b) 4 (c) 9 (d) 27
**5.** $(-3)^2$ equals
   (a) $-9$ (b) 9 (c) $-6$ (d) 6

::: note Objective practice — answers
**1.** (a) — add the indices. **2.** (c) — $1+0.5=1.5$. **3.** (b) — $\sqrt{16}=4$. **4.** (b) — $3^4=81$. **5.** (b) — the bracket squares the sign too.
:::
