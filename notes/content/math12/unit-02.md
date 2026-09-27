---
subject: Mathematics
grade: 12
unit: 2
title: Binomial Theorem
hours: 10
area: Algebra
---

Multiplying out $(a+b)^{2}$ is easy, $(a+b)^{5}$ is tedious, and $(a+b)^{20}$ by
hand is out of the question. The binomial theorem gives every term of
$(a+b)^{n}$ directly, without multiplying anything out, and the coefficients turn
out to be exactly the combination numbers $^{n}C_{r}$ of Unit 1 — which is no
coincidence. The theorem then stretches beyond whole-number powers to negative
and fractional ones, where it becomes an infinite series and a practical tool for
computing roots such as $\sqrt[3]{127}$ by hand. The same style of series
produces the number $e$, the most important constant in calculus.

::: key What the exam asks
Four things, again and again: **expand** a binomial; find a **particular term**
(general term, middle term, term independent of $x$, coefficient of $x^{k}$);
**expand for a negative or fractional index** and state the validity condition;
and **approximate** a root or a power to a stated number of decimal places. The
$e$ and $\log(1+x)$ series are usually a short sum-the-series item.
:::

## 2.1 Binomial theorem for a positive integral index

Multiply out the first few powers and watch the coefficients:

$$ (a+b)^{1} = a + b $$
$$ (a+b)^{2} = a^{2} + 2ab + b^{2} $$
$$ (a+b)^{3} = a^{3} + 3a^{2}b + 3ab^{2} + b^{3} $$
$$ (a+b)^{4} = a^{4} + 4a^{3}b + 6a^{2}b^{2} + 4ab^{3} + b^{4} $$

The powers of $a$ fall from $n$ to $0$, the powers of $b$ rise from $0$ to $n$,
their sum is always $n$, and the coefficients are $^{n}C_{0}, {}^{n}C_{1},
\ldots, {}^{n}C_{n}$.

::: key The binomial theorem, $n$ a positive integer
$$ (a+b)^{n} = \sum_{r=0}^{n} {}^{n}C_{r}\,a^{n-r}b^{r} $$
$$ = {}^{n}C_{0}a^{n} + {}^{n}C_{1}a^{n-1}b + {}^{n}C_{2}a^{n-2}b^{2}
+ \cdots + {}^{n}C_{n}b^{n} $$
There are exactly $n+1$ terms. Putting $a = 1$, $b = x$:
$$ (1+x)^{n} = 1 + {}^{n}C_{1}x + {}^{n}C_{2}x^{2} + \cdots + x^{n} $$
:::

Why combinations? Because $(a+b)^{n}$ is $n$ brackets multiplied together, and to
build the term $a^{n-r}b^{r}$ you must choose which $r$ of the $n$ brackets
contribute a $b$. That can be done in $^{n}C_{r}$ ways, so $a^{n-r}b^{r}$ appears
$^{n}C_{r}$ times. Here is the same fact proved formally.

::: derivation Binomial theorem by mathematical induction
Let $P(n)$ be the statement
$\;(a+b)^{n} = \sum_{r=0}^{n}{}^{n}C_{r}\,a^{n-r}b^{r}$.

**Base step.** For $n = 1$ the right side is
$^{1}C_{0}a + {}^{1}C_{1}b = a + b = (a+b)^{1}$. So $P(1)$ is true.

**Inductive step.** Assume $P(k)$ is true for some positive integer $k$:

$$ (a+b)^{k} = \sum_{r=0}^{k}{}^{k}C_{r}\,a^{k-r}b^{r} $$

Multiply both sides by $(a+b)$:

$$ (a+b)^{k+1} = a\sum_{r=0}^{k}{}^{k}C_{r}a^{k-r}b^{r}
+ b\sum_{r=0}^{k}{}^{k}C_{r}a^{k-r}b^{r} $$

$$ = \sum_{r=0}^{k}{}^{k}C_{r}a^{k+1-r}b^{r}
+ \sum_{r=0}^{k}{}^{k}C_{r}a^{k-r}b^{r+1} $$

In the second sum replace the dummy $r$ by $r-1$, so that it runs from $r=1$ to
$r=k+1$ and its general term becomes $^{k}C_{r-1}a^{k+1-r}b^{r}$ — the same shape
as the first sum. Separating the term $r=0$ from the first sum and $r=k+1$ from
the second:

$$ (a+b)^{k+1} = a^{k+1} + \sum_{r=1}^{k}
\left[{}^{k}C_{r} + {}^{k}C_{r-1}\right]a^{k+1-r}b^{r} + b^{k+1} $$

By **Pascal's rule** (Unit 1, property iv),
$^{k}C_{r} + {}^{k}C_{r-1} = {}^{k+1}C_{r}$. Also
$a^{k+1} = {}^{k+1}C_{0}a^{k+1}$ and $b^{k+1} = {}^{k+1}C_{k+1}b^{k+1}$, so the
two loose terms slot into the sum:

$$ (a+b)^{k+1} = \sum_{r=0}^{k+1}{}^{k+1}C_{r}\,a^{k+1-r}b^{r} $$

which is $P(k+1)$. Since $P(1)$ holds and $P(k) \Rightarrow P(k+1)$, by the
principle of mathematical induction $P(n)$ is true for every positive integer
$n$. $\blacksquare$
:::

::: caution Keep the minus sign inside the bracket
For $(a-b)^{n}$, write $b \to -b$: the signs alternate,
$(a-b)^{n} = a^{n} - {}^{n}C_{1}a^{n-1}b + {}^{n}C_{2}a^{n-2}b^{2} - \cdots$.
For something like $(2x - 3y)^{9}$ the whole of $-3y$ is the second quantity, so
the $r^{\text{th}}$ power is $(-3)^{r}y^{r}$ — cube the $3$ as well as the $y$.
:::

::: example Worked example 2.1
**Problem.** Expand $\left(2x + \dfrac{3}{x}\right)^{5}$.

**Solution.** Take $a = 2x$, $b = 3/x$, $n = 5$, with coefficients
$1, 5, 10, 10, 5, 1$:

$$ (2x)^{5} + 5(2x)^{4}\!\left(\frac{3}{x}\right) + 10(2x)^{3}\!\left(\frac{3}{x}\right)^{2}
+ 10(2x)^{2}\!\left(\frac{3}{x}\right)^{3} + 5(2x)\!\left(\frac{3}{x}\right)^{4}
+ \left(\frac{3}{x}\right)^{5} $$

Work out each piece:

$$ = 32x^{5} + 5(16x^{4})\frac{3}{x} + 10(8x^{3})\frac{9}{x^{2}}
+ 10(4x^{2})\frac{27}{x^{3}} + 5(2x)\frac{81}{x^{4}} + \frac{243}{x^{5}} $$

$$ = 32x^{5} + 240x^{3} + 720x + \frac{1080}{x} + \frac{810}{x^{3}}
+ \frac{243}{x^{5}} $$
:::

::: example Worked example 2.2
**Problem.** Evaluate $(\sqrt{3}+1)^{5} - (\sqrt{3}-1)^{5}$ without a
calculator.

**Solution.** In $(a+b)^{5} - (a-b)^{5}$ the even-power-of-$b$ terms are
identical and cancel, while the odd ones double:

$$ (a+b)^{5} - (a-b)^{5} = 2\left[{}^{5}C_{1}a^{4}b + {}^{5}C_{3}a^{2}b^{3}
+ {}^{5}C_{5}b^{5}\right] $$

With $a = \sqrt{3}$ (so $a^{2} = 3$, $a^{4} = 9$) and $b = 1$:

$$ = 2\left[5(9)(1) + 10(3)(1) + 1\right] = 2\left[45 + 30 + 1\right]
= 2(76) = 152 $$

The surds have vanished — which is the point of pairing the two expansions.
:::

## 2.2 General term; binomial coefficients

::: key General term, middle term
The $(r+1)^{\text{th}}$ term of $(a+b)^{n}$ is
$$ T_{r+1} = {}^{n}C_{r}\,a^{n-r}b^{r}, \qquad r = 0, 1, 2, \ldots, n $$
**Middle term.** There are $n+1$ terms.
- $n$ **even**: one middle term, $T_{\frac{n}{2}+1}$.
- $n$ **odd**: two middle terms, $T_{\frac{n+1}{2}}$ and $T_{\frac{n+3}{2}}$.
:::

::: derivation Where the general term comes from, and which term is the middle one
The theorem lists the terms as $r$ runs $0, 1, 2, \ldots, n$. The term with
subscript $r$ is therefore not the $r^{\text{th}}$ term but the
$(r+1)^{\text{th}}$, because $r = 0$ gives the *first* term. Hence
$T_{r+1} = {}^{n}C_{r}a^{n-r}b^{r}$ — always write the $r+1$ down before
substituting, or you will be one term out.

For the middle term, count the $n+1$ terms. If $n$ is even, $n+1$ is odd and a
single term stands in the middle, at position $\dfrac{(n+1)+1}{2} = \dfrac{n}{2}+1$.
If $n$ is odd, $n+1$ is even and no single term is central; the two middle ones
are at positions $\dfrac{n+1}{2}$ and $\dfrac{n+1}{2}+1 = \dfrac{n+3}{2}$.
:::

### Pascal's triangle and the binomial coefficients

The numbers $^{n}C_{r}$ are called the **binomial coefficients**. Written in
rows they form Pascal's triangle, in which each entry is the sum of the two
directly above it — which is exactly Pascal's rule
$^{n}C_{r-1} + {}^{n}C_{r} = {}^{n+1}C_{r}$.

```figure caption="Pascal's triangle. Row $n$ lists $^{n}C_{0}$ to $^{n}C_{n}$, the coefficients of $(a+b)^{n}$, and each entry is the sum of the two above it: $^{5}C_{1} + {}^{5}C_{2} = {}^{6}C_{2}$, i.e. $5 + 10 = 15$."
import numpy as np, matplotlib.pyplot as plt
from math import comb
fig, ax = plt.subplots(figsize=(5.0,3.0))
dx, dy = 0.52, 0.62
for n in range(7):
    for r in range(n+1):
        x = (r - n/2) * dx
        y = -n * dy
        hot = (n, r) in [(5,1), (5,2), (6,2)]
        ax.text(x, y, str(comb(n, r)), ha='center', va='center',
                fontsize=9.2, color='#d9534f' if hot else INK,
                fontweight='bold' if hot else 'normal')
    ax.text(-2.35, -n*dy, f'$n={n}$', ha='left', va='center',
            fontsize=8.0, color=MUTED)
for r0 in (1, 2):
    ax.annotate('', xy=((2 - 3) * dx, -6*dy + 0.20),
                xytext=((r0 - 2.5) * dx, -5*dy - 0.20),
                arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.0))
ax.text(1.95, -5.40*dy, '$5 + 10 = 15$', ha='left', fontsize=9.2, color='#d9534f')
ax.text(1.95, -6.25*dy, '$^{5}C_{1} + {}^{5}C_{2} = {}^{6}C_{2}$', ha='left',
        fontsize=9.2, color='#d9534f')
ax.text(0.0, 0.62, 'row $n$ = coefficients of $(a+b)^{n}$', ha='center',
        fontsize=9.2, color=ACCENT)
ax.set_xlim(-2.6, 4.4); ax.set_ylim(-4.45, 1.0)
ax.axis('off')
```

Three facts follow from putting numbers into $(1+x)^{n}$:

$$ x = 1: \quad {}^{n}C_{0} + {}^{n}C_{1} + {}^{n}C_{2} + \cdots + {}^{n}C_{n} = 2^{n} $$
$$ x = -1: \quad {}^{n}C_{0} - {}^{n}C_{1} + {}^{n}C_{2} - \cdots \pm {}^{n}C_{n} = 0 $$

Adding and subtracting these two gives the sum of the even-placed coefficients
and of the odd-placed ones, each equal to $2^{n-1}$.

::: example Worked example 2.3
**Problem.** Prove that
$^{n}C_{0} + {}^{n}C_{1} + \cdots + {}^{n}C_{n} = 2^{n}$, and hence find the sum
of the coefficients in the expansion of $(2x - 3y)^{12}$.

**Solution.** In the binomial theorem put $a = b = 1$:

$$ (1+1)^{n} = {}^{n}C_{0}1^{n} + {}^{n}C_{1}1^{n-1}1 + \cdots + {}^{n}C_{n}1^{n} $$

The left side is $2^{n}$ and the right side is the required sum, so the two are
equal. (In words: a set of $n$ elements has $2^{n}$ subsets, counted here by
size.)

For the second part, "the sum of the coefficients" means the value of the
expansion when every variable is set to $1$. Putting $x = y = 1$ in
$(2x-3y)^{12}$:

$$ (2 - 3)^{12} = (-1)^{12} = 1 $$
:::

```figure caption="Binomial coefficients of $(1+x)^{8}$ (even $n$: one middle term, $T_5$) and of $(1+x)^{9}$ (odd $n$: two equal middle terms, $T_5$ and $T_6$)."
import numpy as np, matplotlib.pyplot as plt
from math import comb
fig, axs = plt.subplots(1, 2, figsize=(5.1,2.6), sharey=True)
for ax, n, mids in [(axs[0], 8, [4]), (axs[1], 9, [4, 5])]:
    r = np.arange(n+1)
    v = [comb(n, int(k)) for k in r]
    cols = ['#d9534f' if k in mids else ACCENT for k in r]
    ax.bar(r, v, color=cols, alpha=0.88, width=0.68)
    for k, val in zip(r, v):
        shift = 0.0
        if len(mids) == 2 and k in mids:
            shift = -0.26 if k == mids[0] else 0.26
        ax.text(k + shift, val + 4, str(val), ha='center', fontsize=6.8, color=INK)
    ax.set_title(f'$(1+x)^{{{n}}}$  —  {n+1} terms', fontsize=9.0)
    ax.set_xlabel('$r$'); ax.set_xticks(r)
    ax.spines[['top','right']].set_visible(False)
    ax.grid(True, axis='y', alpha=.45)
axs[0].set_ylabel('$^{n}C_{r}$')
axs[0].set_ylim(0, 170)
axs[0].text(4, 105, '$T_{5}$', ha='center', fontsize=9.4, color='#d9534f')
axs[1].text(4.5, 148, '$T_{5}, T_{6}$', ha='center', fontsize=9.4, color='#d9534f')
```

::: example Worked example 2.4
**Problem.** Find the term independent of $x$ in the expansion of
$\left(x^{2} - \dfrac{2}{x}\right)^{9}$.

**Solution.** The general term is

$$ T_{r+1} = {}^{9}C_{r}\,(x^{2})^{9-r}\left(-\frac{2}{x}\right)^{r}
= {}^{9}C_{r}\,(-2)^{r}\,x^{18-2r}\,x^{-r} = {}^{9}C_{r}(-2)^{r}x^{18-3r} $$

"Independent of $x$" means the power of $x$ is zero:

$$ 18 - 3r = 0 \;\Longrightarrow\; r = 6 $$

So the term is the seventh, and its value is

$$ ^{9}C_{6}(-2)^{6} = 84 \times 64 = 5376 $$
:::

::: example Worked example 2.5
**Problem.** Find the coefficient of $x^{32}$ in
$\left(x^{4} - \dfrac{1}{x^{3}}\right)^{15}$.

**Solution.**

$$ T_{r+1} = {}^{15}C_{r}(x^{4})^{15-r}\left(-\frac{1}{x^{3}}\right)^{r}
= (-1)^{r}\,{}^{15}C_{r}\,x^{60-4r-3r} = (-1)^{r}\,{}^{15}C_{r}\,x^{60-7r} $$

Set $60 - 7r = 32$, so $7r = 28$ and $r = 4$ — a whole number, so such a term
exists. Its coefficient is

$$ (-1)^{4}\,{}^{15}C_{4} = \frac{15 \times 14 \times 13 \times 12}{4 \times 3 \times 2 \times 1}
= 1365 $$
:::

::: example Worked example 2.6
**Problem.** Find the middle term(s) of (a)
$\left(\dfrac{x}{2} + \dfrac{2}{x}\right)^{8}$ and (b) $(2x - y)^{7}$.

**Solution.** (a) $n = 8$ is even, so there is one middle term,
$T_{\frac{8}{2}+1} = T_{5}$, i.e. $r = 4$:

$$ T_{5} = {}^{8}C_{4}\left(\frac{x}{2}\right)^{4}\left(\frac{2}{x}\right)^{4}
= 70 \cdot \frac{x^{4}}{16}\cdot\frac{16}{x^{4}} = 70 $$

(b) $n = 7$ is odd, so the middle terms are $T_{4}$ ($r=3$) and $T_{5}$ ($r=4$):

$$ T_{4} = {}^{7}C_{3}(2x)^{4}(-y)^{3} = 35 \times 16x^{4} \times (-y^{3})
= -560\,x^{4}y^{3} $$

$$ T_{5} = {}^{7}C_{4}(2x)^{3}(-y)^{4} = 35 \times 8x^{3} \times y^{4}
= 280\,x^{3}y^{4} $$
:::

::: example Worked example 2.7
**Problem.** Three consecutive coefficients in the expansion of $(1+x)^{n}$ are
$45$, $120$ and $210$. Find $n$ and the position of these terms.

**Solution.** Let them be $^{n}C_{r-1} = 45$, $^{n}C_{r} = 120$,
$^{n}C_{r+1} = 210$. Use the ratio of consecutive coefficients,
$\dfrac{^{n}C_{r}}{^{n}C_{r-1}} = \dfrac{n-r+1}{r}$:

$$ \frac{n-r+1}{r} = \frac{120}{45} = \frac{8}{3}
\;\Longrightarrow\; 3n - 3r + 3 = 8r \;\Longrightarrow\; 3n - 11r + 3 = 0 \quad (1) $$

$$ \frac{n-r}{r+1} = \frac{210}{120} = \frac{7}{4}
\;\Longrightarrow\; 4n - 4r = 7r + 7 \;\Longrightarrow\; 4n - 11r - 7 = 0 \quad (2) $$

Subtracting (1) from (2): $\;n - 10 = 0$, so $n = 10$; then (1) gives
$33 = 11r$, so $r = 3$.

**Check:** $^{10}C_{2} = 45$, $^{10}C_{3} = 120$, $^{10}C_{4} = 210$. ✓ The terms
are the $3^{\text{rd}}$, $4^{\text{th}}$ and $5^{\text{th}}$.
:::

## 2.3 Binomial theorem for any index (without proof)

If $n$ is *not* a positive integer, the list $^{n}C_{0}, {}^{n}C_{1}, \ldots$
never stops, because no factor $(n-r)$ is ever zero. The expansion then becomes
an infinite series, and an infinite series is only worth writing if it converges.

::: key Binomial series for any index
For any real number $n$ and $|x| < 1$,
$$ (1+x)^{n} = 1 + nx + \frac{n(n-1)}{2!}x^{2} + \frac{n(n-1)(n-2)}{3!}x^{3} + \cdots $$
with general term
$$ T_{r+1} = \frac{n(n-1)(n-2)\cdots(n-r+1)}{r!}\,x^{r} $$
**The condition $|x| < 1$ is part of the statement.** State it every time.
:::

Two remarks tie this to §2.1. First, if $n$ is a positive integer the factor
$(n-n)$ appears when $r = n+1$, every later term is zero, and the series stops by
itself at $n+1$ terms — the old theorem is the special case. Second, the
coefficients are no longer $^{n}C_{r}$ (that symbol needs a whole number), so
write them out as the product $n(n-1)\cdots(n-r+1)/r!$.

Four expansions are worth knowing by sight, all valid for $|x| < 1$:

| Expansion | Series |
|---|---|
| $(1-x)^{-1}$ | $1 + x + x^{2} + x^{3} + \cdots$ |
| $(1+x)^{-1}$ | $1 - x + x^{2} - x^{3} + \cdots$ |
| $(1-x)^{-2}$ | $1 + 2x + 3x^{2} + 4x^{3} + \cdots$ |
| $(1+x)^{1/2}$ | $1 + \dfrac{x}{2} - \dfrac{x^{2}}{8} + \dfrac{x^{3}}{16} - \cdots$ |

```figure caption="Partial sums of the series for $(1+x)^{1/2}$. At $x=0.6$ (inside $|x|<1$) they settle onto $\sqrt{1.6} = 1.2649$; at $x=1.8$ (outside) they swing further and further apart, so the series is useless there."
import numpy as np, matplotlib.pyplot as plt
fig, axs = plt.subplots(1, 2, figsize=(5.1,2.8))

def coeffs(a, m):
    c, v = [], 1.0
    for k in range(m):
        c.append(v); v *= (a - k)/(k + 1)
    return np.array(c)

c = coeffs(0.5, 15)
for ax, xv, col in [(axs[0], 0.6, ACCENT), (axs[1], 1.8, '#d9534f')]:
    S = np.cumsum(c * xv**np.arange(15))
    m = np.arange(1, 16)
    ax.plot(m, S, 'o-', color=col, ms=3.4)
    ax.set_xlabel('terms used')
    ax.set_title(f'$x = {xv}$', fontsize=9.4, color=col)
    ax.spines[['top','right']].set_visible(False)
    ax.grid(True, alpha=.45)
axs[0].axhline(np.sqrt(1.6), color=INK, ls='--', lw=0.9)
axs[0].text(7.5, 1.288, '$\\sqrt{1.6} = 1.2649$', fontsize=8.6, color=INK)
axs[0].set_ylim(0.98, 1.34); axs[0].set_ylabel('partial sum')
axs[1].axhline(np.sqrt(2.8), color=INK, ls='--', lw=0.9)
axs[1].text(1.0, 3.0, '$\\sqrt{2.8}$ is never reached:', fontsize=8.2, color=INK)
axs[1].text(1.0, -4.2, 'the swings grow\nwithout limit', fontsize=8.4,
            color='#d9534f')
axs[1].set_ylim(-13.5, 12.5)
```

::: example Worked example 2.8
**Problem.** Expand in ascending powers of $x$ as far as the term in $x^{3}$,
stating the range of validity: (a) $(1-2x)^{1/2}$, (b) $(4+x)^{-1/2}$.

**Solution.** (a) Use the series with $n = \tfrac12$ and the quantity $(-2x)$ in
place of $x$:

$$ (1-2x)^{1/2} = 1 + \frac12(-2x)
+ \frac{\frac12\left(-\frac12\right)}{2!}(-2x)^{2}
+ \frac{\frac12\left(-\frac12\right)\left(-\frac32\right)}{3!}(-2x)^{3} + \cdots $$

Take the terms one at a time. The second is $\tfrac12(-2x) = -x$. The third has
coefficient $\dfrac{\frac12\left(-\frac12\right)}{2} = -\dfrac18$ and
$(-2x)^{2} = 4x^{2}$, giving $-\tfrac18(4x^{2}) = -\tfrac12 x^{2}$. The fourth has
coefficient $\dfrac{\frac12\left(-\frac12\right)\left(-\frac32\right)}{6}
= \dfrac{3/8}{6} = \dfrac{1}{16}$ and $(-2x)^{3} = -8x^{3}$, giving
$\tfrac{1}{16}(-8x^{3}) = -\tfrac12 x^{3}$. So

$$ (1-2x)^{1/2} = 1 - x - \frac{x^{2}}{2} - \frac{x^{3}}{2} - \cdots,
\qquad |2x| < 1 \text{ i.e. } |x| < \tfrac12 $$

(b) The series needs a leading $1$, so take the $4$ outside first:

$$ (4+x)^{-1/2} = \left[4\left(1+\frac{x}{4}\right)\right]^{-1/2}
= 4^{-1/2}\left(1+\frac{x}{4}\right)^{-1/2}
= \frac12\left(1+\frac{x}{4}\right)^{-1/2} $$

With $n = -\tfrac12$:

$$ \left(1+\frac{x}{4}\right)^{-1/2} = 1 - \frac12\cdot\frac{x}{4}
+ \frac{\left(-\frac12\right)\left(-\frac32\right)}{2}\cdot\frac{x^{2}}{16}
+ \frac{\left(-\frac12\right)\left(-\frac32\right)\left(-\frac52\right)}{6}\cdot\frac{x^{3}}{64} $$

$$ = 1 - \frac{x}{8} + \frac{3x^{2}}{128} - \frac{5x^{3}}{1024} $$

Multiplying by $\tfrac12$:

$$ (4+x)^{-1/2} = \frac12 - \frac{x}{16} + \frac{3x^{2}}{256}
- \frac{5x^{3}}{2048} - \cdots, \qquad \left|\frac{x}{4}\right| < 1
\text{ i.e. } |x| < 4 $$
:::

::: caution Make the first term a $1$ before expanding
$(4+x)^{-1/2}$ is **not** $4^{-1/2} + \ldots$ term by term. Always factor out the
constant so the bracket reads $(1 + \text{something small})$, and remember that
the validity condition applies to that *something*, giving $|x| < 4$ here, not
$|x| < 1$.
:::

## 2.4 Approximation using binomial expansion

When $x$ is small, $x^{2}$ is very small and $x^{3}$ smaller still, so the first
two or three terms of the series already give an accurate value. This is how
roots were computed before calculators, and it is still the fastest way to see
*how* a quantity depends on a small change.

```figure caption="$y=\sqrt{1+x}$ against its $1$-, $2$- and $3$-term binomial approximations. Near $x=0$ all four curves coincide; the more terms, the wider the interval over which the approximation is usable."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.9))
x = np.linspace(-0.85, 1.8, 400)
ax.plot(x, np.sqrt(1+x), color=INK, lw=2.0, label='$\\sqrt{1+x}$ (exact)')
ax.plot(x, 1 + 0*x, color=SERIES[3], lw=1.3, ls=':', label='$1$')
ax.plot(x, 1 + x/2, color=ACCENT, lw=1.3, ls='--', label='$1+\\frac{x}{2}$')
ax.plot(x, 1 + x/2 - x**2/8, color='#2e8b57', lw=1.3,
        label='$1+\\frac{x}{2}-\\frac{x^{2}}{8}$')
ax.axvspan(-0.1, 0.1, color=ACCENT, alpha=0.10)
ax.text(0.0, 0.35, 'small $x$', ha='center', fontsize=8.4, color=ACCENT)
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.set_xlim(-0.9, 1.85); ax.set_ylim(0.2, 1.95)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.45); ax.legend(loc='lower right', fontsize=7.8)
```

::: example Worked example 2.9
**Problem.** Find the value of $(1.02)^{1/3}$ correct to five decimal places.

**Solution.** Write $1.02 = 1 + 0.02$ and expand with $n = \tfrac13$,
$x = 0.02$:

$$ (1+x)^{1/3} = 1 + \frac{1}{3}x + \frac{\frac13\left(-\frac23\right)}{2!}x^{2} + \cdots
= 1 + \frac{x}{3} - \frac{x^{2}}{9} + \cdots $$

$$ = 1 + \frac{0.02}{3} - \frac{0.0004}{9} + \cdots
= 1 + 0.0066667 - 0.0000444 = 1.0066223 $$

The next term is of order $x^{3} \approx 10^{-6}$ multiplied by a coefficient
less than $1$, so it cannot change the fifth decimal place. Hence

$$ (1.02)^{1/3} \approx 1.00662 $$

(A calculator gives $1.0066227$ — the two agree to seven places.)
:::

::: example Worked example 2.10
**Problem.** Using the binomial theorem, find $\sqrt[3]{127}$ correct to four
decimal places.

**Solution.** Choose the nearest perfect cube, $125 = 5^{3}$, and factor it out
so that the bracket is close to $1$:

$$ 127^{1/3} = (125 + 2)^{1/3} = \left[125\left(1 + \frac{2}{125}\right)\right]^{1/3}
= 5\left(1 + 0.016\right)^{1/3} $$

Now expand with $x = 0.016$:

$$ 5\left[1 + \frac{0.016}{3} - \frac{(0.016)^{2}}{9} + \cdots\right]
= 5\left[1 + 0.00533333 - 0.00002844\right] $$

$$ = 5 \times 1.00530489 = 5.02652 $$

So $\sqrt[3]{127} \approx 5.0265$ (the true value is $5.026526$).
:::

::: example Worked example 2.11
**Problem.** Find $\sqrt{102}$ correct to four decimal places, and evaluate
$(1.02)^{10}$ to four significant figures.

**Solution.** *First part.* $102 = 100(1 + 0.02)$, so

$$ \sqrt{102} = 10\left(1+0.02\right)^{1/2}
= 10\left[1 + \frac{0.02}{2} - \frac{(0.02)^{2}}{8} + \frac{(0.02)^{3}}{16}\right] $$

$$ = 10\left[1 + 0.01 - 0.00005 + 0.0000001\right] = 10(1.0099501) = 10.099501 $$

Hence $\sqrt{102} \approx 10.0995$.

*Second part.* Here $n = 10$ is a positive integer, so the expansion is exact and
finite; we simply stop when the terms become negligible:

$$ (1+0.02)^{10} = 1 + 10(0.02) + 45(0.02)^{2} + 120(0.02)^{3} + \cdots $$

$$ = 1 + 0.2 + 0.018 + 0.00096 + \cdots = 1.21896 \approx 1.219 $$
:::

::: tip Choosing the split
To approximate $\sqrt[k]{N}$, split $N$ as (nearest perfect $k^{\text{th}}$
power) $+$ (small remainder), then factor the power out. For $\sqrt{102}$ use
$100$, for $\sqrt[3]{127}$ use $125$, for $\sqrt[4]{17}$ use $16$. The smaller
the ratio remainder/power, the faster the series converges.
:::

## 2.5 Euler's number $e$

::: definition Euler's number
$$ e = \lim_{n\to\infty}\left(1 + \frac{1}{n}\right)^{n} $$
Its value is $e = 2.718281828\ldots$, an irrational number.
:::

::: derivation The series for $e$, and why $2 < e < 3$
Expand $\left(1+\dfrac1n\right)^{n}$ by the binomial theorem ($n$ a positive
integer):

$$ \left(1+\frac1n\right)^{n} = 1 + n\cdot\frac1n
+ \frac{n(n-1)}{2!}\cdot\frac{1}{n^{2}} + \frac{n(n-1)(n-2)}{3!}\cdot\frac{1}{n^{3}}
+ \cdots $$

Divide each $n$ in the numerators by one factor of $n$ from the denominator:

$$ = 1 + 1 + \frac{1}{2!}\left(1-\frac1n\right)
+ \frac{1}{3!}\left(1-\frac1n\right)\left(1-\frac2n\right) + \cdots $$

Let $n \to \infty$. Every bracket $\left(1 - \dfrac{k}{n}\right) \to 1$, so

$$ e = 1 + \frac{1}{1!} + \frac{1}{2!} + \frac{1}{3!} + \frac{1}{4!} + \cdots
= \sum_{r=0}^{\infty}\frac{1}{r!} $$

**Bounds.** Every term is positive, and the first two already give
$e > 1 + 1 = 2$. For an upper bound, note $r! \ge 2^{\,r-1}$ for $r \ge 1$, so

$$ e \le 1 + 1 + \frac{1}{2} + \frac{1}{2^{2}} + \frac{1}{2^{3}} + \cdots
= 1 + \frac{1}{1 - \frac12} = 1 + 2 = 3 $$

and the inequality is strict because $3! = 6 > 4 = 2^{2}$. Hence $2 < e < 3$.
:::

```figure caption="Two roads to $e = 2.71828$. The limit $\left(1+\frac{1}{n}\right)^{n}$ crawls towards it, while the series $\sum 1/r!$ is correct to $6$ decimal places after only $10$ terms."
import numpy as np, matplotlib.pyplot as plt
from math import factorial
fig, ax = plt.subplots(figsize=(5.0,2.8))
m = np.arange(1, 13)
lim = (1 + 1/m)**m
ser = np.cumsum([1/factorial(int(k)) for k in range(12)])
ax.plot(m, lim, 'o-', color=ACCENT, ms=3.8,
        label='$\\left(1+\\frac{1}{n}\\right)^{n}$,  $n = 1 \\ldots 12$')
ax.plot(m[1:], ser[1:], 's-', color='#2e8b57', ms=3.8,
        label='$1+\\frac{1}{1!}+\\cdots+\\frac{1}{r!}$')
ax.axhline(np.e, color=INK, ls='--', lw=1.0)
ax.text(8.6, 2.745, '$e = 2.71828$', fontsize=9.0, color=INK)
ax.axhline(3, color=MUTED, ls=':', lw=0.9)
ax.text(0.7, 3.03, 'upper bound 3', fontsize=8.2, color=MUTED)
ax.set_xlabel('number of terms / value of $n$'); ax.set_ylabel('value')
ax.set_xlim(0.5, 12.5); ax.set_ylim(1.85, 3.2)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.45); ax.legend(loc='lower right', fontsize=8.0)
```

## 2.6 Expansion of $e^{x}$, $a^{x}$ and $\log(1+x)$ (without proof)

::: key The three standard series
$$ e^{x} = 1 + \frac{x}{1!} + \frac{x^{2}}{2!} + \frac{x^{3}}{3!} + \cdots
\qquad \text{for all real } x $$
$$ a^{x} = e^{x\log_{e}a} = 1 + \frac{x\log a}{1!} + \frac{(x\log a)^{2}}{2!}
+ \frac{(x\log a)^{3}}{3!} + \cdots \qquad (a > 0) $$
$$ \log_{e}(1+x) = x - \frac{x^{2}}{2} + \frac{x^{3}}{3} - \frac{x^{4}}{4}
+ \cdots \qquad \text{for } -1 < x \le 1 $$
Putting $x \to -x$ in the last and subtracting,
$$ \log_{e}\frac{1+x}{1-x} = 2\left(x + \frac{x^{3}}{3} + \frac{x^{5}}{5} + \cdots\right),
\qquad |x| < 1 $$
:::

In NEB work $\log$ with no base written means the natural logarithm $\log_{e}$,
also written $\ln$. Note that the $e^{x}$ series converges for *every* $x$, while
the logarithmic series needs $-1 < x \le 1$: the graph below shows what happens
just outside that range.

```figure caption="Partial sums of $x - \frac{x^{2}}{2} + \frac{x^{3}}{3} - \cdots$ against $\log(1+x)$. Inside $-1 < x \le 1$ they close in on the curve; past $x=1$ they peel away, which is why the validity condition matters."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.9))
x = np.linspace(-0.85, 1.6, 500)
ax.plot(x, np.log(1+x), color=INK, lw=2.0, label='$\\log(1+x)$')
S = np.zeros_like(x)
for k, col in zip(range(1, 7), [SERIES[3], ACCENT, '#2e8b57', SERIES[4],
                                SERIES[5], '#d9534f']):
    S = S + ((-1)**(k+1)) * x**k / k
    if k in (1, 2, 4, 6):
        ax.plot(x, S, lw=1.1, ls='--', color=col,
                label=f'{k} term' + ('' if k == 1 else 's'))
ax.axvline(1.0, color=MUTED, lw=0.9, ls=':')
ax.text(1.04, -1.55, 'series valid only\nup to $x=1$', fontsize=8.2, color=MUTED)
ax.set_xlabel('$x$'); ax.set_ylabel('value')
ax.set_xlim(-0.9, 1.62); ax.set_ylim(-2.1, 1.6)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.45); ax.legend(loc='upper left', fontsize=7.6, ncol=2)
```

::: example Worked example 2.12
**Problem.** Find the sum of the series
$\;\dfrac{1}{1!} + \dfrac{2}{2!} + \dfrac{3}{3!} + \dfrac{4}{4!} + \cdots$

**Solution.** The general term is $\dfrac{n}{n!}$. Cancel one factor of $n$,
using $n! = n\,(n-1)!$:

$$ \frac{n}{n!} = \frac{n}{n\,(n-1)!} = \frac{1}{(n-1)!} $$

So the series becomes, as $n$ runs $1, 2, 3, \ldots$,

$$ \frac{1}{0!} + \frac{1}{1!} + \frac{1}{2!} + \frac{1}{3!} + \cdots = e $$

The sum is $e = 2.71828\ldots$
:::

::: example Worked example 2.13
**Problem.** Show that
$\;1 + \dfrac{1}{2!} + \dfrac{1}{4!} + \dfrac{1}{6!} + \cdots = \dfrac{e + e^{-1}}{2}$,
and evaluate it to four decimal places.

**Solution.** Write the two exponential series with $x = 1$ and $x = -1$:

$$ e = 1 + \frac{1}{1!} + \frac{1}{2!} + \frac{1}{3!} + \frac{1}{4!} + \cdots $$
$$ e^{-1} = 1 - \frac{1}{1!} + \frac{1}{2!} - \frac{1}{3!} + \frac{1}{4!} - \cdots $$

Adding, every odd-factorial term cancels and every even one doubles:

$$ e + e^{-1} = 2\left(1 + \frac{1}{2!} + \frac{1}{4!} + \frac{1}{6!} + \cdots\right) $$

Dividing by $2$ gives the required result. Numerically,

$$ \frac{e + e^{-1}}{2} = \frac{2.718282 + 0.367879}{2} = \frac{3.086161}{2}
= 1.5431 $$

(Subtracting instead gives the companion result
$\dfrac{1}{1!} + \dfrac{1}{3!} + \dfrac{1}{5!} + \cdots = \dfrac{e-e^{-1}}{2}$.)
:::

::: example Worked example 2.14
**Problem.** Use the logarithmic series to compute $\log_{e} 2$ correct to four
decimal places.

**Solution.** Putting $x = 1$ in $\log(1+x)$ gives
$1 - \tfrac12 + \tfrac13 - \cdots$, which is correct but crawls: you would need
thousands of terms. Use the faster series instead. Choose $x$ so that
$\dfrac{1+x}{1-x} = 2$, which gives $x = \dfrac13$:

$$ \log 2 = 2\left(\frac13 + \frac{1}{3}\cdot\frac{1}{3^{3}}
+ \frac{1}{5}\cdot\frac{1}{3^{5}} + \frac{1}{7}\cdot\frac{1}{3^{7}} + \cdots\right) $$

$$ = 2\left(0.333333 + 0.012346 + 0.000823 + 0.000065\right)
= 2(0.346567) = 0.693135 $$

So $\log_{e} 2 \approx 0.6931$ (true value $0.6931472$) — four terms were enough.
:::

::: example Worked example 2.15
**Problem.** Expand $3^{x}$ in ascending powers of $x$ as far as the term in
$x^{3}$, and hence evaluate $3^{0.1}$ to four decimal places. Also write down
the coefficient of $x^{4}$ in $e^{2x}$.

**Solution.** Any power $a^{x}$ is turned into an exponential by
$a = e^{\log_{e} a}$, so $a^{x} = e^{x\log_{e} a}$. With $a = 3$:

$$ 3^{x} = e^{x\log 3} = 1 + (x\log 3) + \frac{(x\log 3)^{2}}{2!}
+ \frac{(x\log 3)^{3}}{3!} + \cdots $$

Collect the powers of $x$:

$$ 3^{x} = 1 + x\log 3 + \frac{x^{2}(\log 3)^{2}}{2!}
+ \frac{x^{3}(\log 3)^{3}}{3!} + \cdots $$

Now put $\log_{e} 3 = 1.098612$, so $(\log 3)^{2}/2 = 0.603474$ and
$(\log 3)^{3}/6 = 0.220995$:

$$ 3^{x} \approx 1 + 1.098612\,x + 0.603474\,x^{2} + 0.220995\,x^{3} $$

At $x = 0.1$ each term is smaller than the last by a factor of about ten, so
three terms after the $1$ are ample:

$$ 3^{0.1} \approx 1 + 0.109861 + 0.006035 + 0.000221 = 1.116117 $$

Hence $3^{0.1} \approx 1.1161$ (calculator: $1.1161232$).

For $e^{2x}$, replace $x$ by $2x$ in $e^{x} = \sum x^{r}/r!$; the term in
$x^{4}$ is $(2x)^{4}/4!$, so the coefficient is

$$ \frac{2^{4}}{4!} = \frac{16}{24} = \frac{2}{3} $$
:::

## Chapter summary

- $(a+b)^{n} = \sum_{r=0}^{n}{}^{n}C_{r}a^{n-r}b^{r}$ for a positive integer $n$;
  it has $n+1$ terms and is proved by induction using Pascal's rule.
- General term: $T_{r+1} = {}^{n}C_{r}a^{n-r}b^{r}$. To find a particular term,
  simplify the power of $x$ in $T_{r+1}$ and equate it to the power wanted.
- Middle term: $T_{\frac{n}{2}+1}$ if $n$ is even; $T_{\frac{n+1}{2}}$ and
  $T_{\frac{n+3}{2}}$ if $n$ is odd.
- Binomial coefficients: $^{n}C_{r} = {}^{n}C_{n-r}$, they build Pascal's
  triangle, $\sum{}^{n}C_{r} = 2^{n}$, and the alternating sum is $0$.
- For any index and $|x| < 1$:
  $(1+x)^{n} = 1 + nx + \dfrac{n(n-1)}{2!}x^{2} + \cdots$ — always state
  $|x| < 1$, and factor out constants first so the bracket starts with $1$.
- Approximation: split $N$ into (nearest exact power) $+$ (small part), factor
  out, expand, and keep terms until they fall below the required place value.
- $e = \lim_{n\to\infty}\left(1+\dfrac1n\right)^{n}
  = \sum_{r=0}^{\infty}\dfrac{1}{r!} = 2.71828\ldots$, and $2 < e < 3$.
- $e^{x} = \sum \dfrac{x^{r}}{r!}$ (all $x$); $a^{x} = e^{x\log a}$;
  $\log(1+x) = x - \dfrac{x^{2}}{2} + \dfrac{x^{3}}{3} - \cdots$ for
  $-1 < x \le 1$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The number of terms in the expansion of $(2x + 3y)^{12}$ is <span class="marks">[1]</span>
   (a) $12$ (b) $13$ (c) $14$ (d) $24$
2. The middle term of $(1+x)^{10}$ is <span class="marks">[1]</span>
   (a) $T_{5}$ (b) $T_{6}$ (c) $T_{5}$ and $T_{6}$ (d) $T_{11}$
3. The value of $^{n}C_{0} + {}^{n}C_{1} + \cdots + {}^{n}C_{n}$ is <span class="marks">[1]</span>
   (a) $2^{n}$ (b) $2^{n-1}$ (c) $n^{2}$ (d) $0$
4. The expansion of $(1+x)^{-3}$ is valid for <span class="marks">[1]</span>
   (a) all $x$ (b) $x > 0$ (c) $|x| < 1$ (d) $|x| > 1$
5. The coefficient of $x^{2}$ in $(1-x)^{-2}$ is <span class="marks">[1]</span>
   (a) $1$ (b) $2$ (c) $3$ (d) $4$
6. The sum $1 + \dfrac{1}{1!} + \dfrac{1}{2!} + \dfrac{1}{3!} + \cdots$ equals <span class="marks">[1]</span>
   (a) $e - 1$ (b) $e$ (c) $e + 1$ (d) $\log e$

::: note Answers to Group A
**1.** (b) — a positive integral index $n$ gives $n+1 = 13$ terms.

**2.** (b) — $n = 10$ is even, so there is one middle term,
$T_{\frac{10}{2}+1} = T_{6}$.

**3.** (a) — put $x = 1$ in $(1+x)^{n}$.

**4.** (c) — the binomial series for a non-positive-integral index needs
$|x| < 1$.

**5.** (c) — $(1-x)^{-2} = 1 + 2x + 3x^{2} + \cdots$

**6.** (b) — this is exactly the series $\sum_{r\ge 0} 1/r! = e$.
:::

**Group B — Short answer (5 marks each)**

1. State and prove the binomial theorem for a positive integral index by
   mathematical induction. <span class="marks">[5]</span>
2. Find the term independent of $x$ in the expansion of
   $\left(2x^{2} - \dfrac{1}{x}\right)^{9}$. <span class="marks">[5]</span>
3. Find the middle term in the expansion of
   $\left(\dfrac{2x}{3} - \dfrac{3}{2x}\right)^{6}$. <span class="marks">[5]</span>
4. Expand $(1+3x)^{-2}$ in ascending powers of $x$ up to the term in $x^{3}$,
   stating the range of values of $x$ for which the expansion is valid. <span class="marks">[5]</span>
5. Using the binomial theorem, find the value of $\sqrt[5]{33}$ correct to four
   decimal places. <span class="marks">[5]</span>
6. Find the sum of the series
   $\dfrac{1}{2!} + \dfrac{1}{4!} + \dfrac{1}{6!} + \cdots$ in terms of $e$. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** *Statement:*
$(a+b)^{n} = \sum_{r=0}^{n}{}^{n}C_{r}a^{n-r}b^{r}$ for every positive integer
$n$.

*Proof.* For $n=1$ the right-hand side is $a+b$, so the statement holds. Assume
it holds for $n = k$. Multiplying by $(a+b)$,

$$ (a+b)^{k+1} = \sum_{r=0}^{k}{}^{k}C_{r}a^{k+1-r}b^{r}
+ \sum_{r=0}^{k}{}^{k}C_{r}a^{k-r}b^{r+1} $$

Shifting the index in the second sum ($r \to r-1$) makes both general terms
$a^{k+1-r}b^{r}$, and collecting them gives

$$ a^{k+1} + \sum_{r=1}^{k}\left[{}^{k}C_{r} + {}^{k}C_{r-1}\right]a^{k+1-r}b^{r}
+ b^{k+1} $$

By Pascal's rule the bracket is $^{k+1}C_{r}$, and the two loose terms are the
$r=0$ and $r=k+1$ members, so the whole is
$\sum_{r=0}^{k+1}{}^{k+1}C_{r}a^{k+1-r}b^{r}$. Hence the result holds for $k+1$,
and by induction for all positive integers $n$.

**2.** $T_{r+1} = {}^{9}C_{r}(2x^{2})^{9-r}\left(-\dfrac1x\right)^{r}
= {}^{9}C_{r}\,2^{9-r}(-1)^{r}x^{18-2r-r}$.

Set $18 - 3r = 0$, so $r = 6$:

$$ T_{7} = {}^{9}C_{6}\,2^{3}(-1)^{6} = 84 \times 8 = 672 $$

**3.** $n = 6$ is even, so the middle term is $T_{4}$, with $r = 3$:

$$ T_{4} = {}^{6}C_{3}\left(\frac{2x}{3}\right)^{3}\left(-\frac{3}{2x}\right)^{3}
= 20 \times \frac{8x^{3}}{27}\times\left(-\frac{27}{8x^{3}}\right) = -20 $$

**4.** With $n = -2$ and the quantity $3x$:

$$ (1+3x)^{-2} = 1 + (-2)(3x) + \frac{(-2)(-3)}{2!}(3x)^{2}
+ \frac{(-2)(-3)(-4)}{3!}(3x)^{3} + \cdots $$

$$ = 1 - 6x + 3(9x^{2}) - 4(27x^{3}) + \cdots = 1 - 6x + 27x^{2} - 108x^{3} + \cdots $$

Valid when $|3x| < 1$, that is $|x| < \dfrac13$.

**5.** The nearest fifth power is $32 = 2^{5}$:

$$ 33^{1/5} = (32+1)^{1/5} = 2\left(1 + \frac{1}{32}\right)^{1/5}
= 2\left(1 + 0.03125\right)^{1/5} $$

With $n = \tfrac15$ and $x = 0.03125$:

$$ 2\left[1 + \frac{x}{5} + \frac{\frac15\left(-\frac45\right)}{2}x^{2} + \cdots\right]
= 2\left[1 + 0.00625 - \frac{2}{25}(0.000977)\right] $$

$$ = 2\left[1 + 0.00625 - 0.0000781\right] = 2(1.0061719) = 2.0123438 $$

So $\sqrt[5]{33} \approx 2.0123$ (true value $2.0123466$).

**6.** From Worked example 2.13,
$1 + \dfrac{1}{2!} + \dfrac{1}{4!} + \cdots = \dfrac{e+e^{-1}}{2}$. Subtracting
the leading $1$,

$$ \frac{1}{2!} + \frac{1}{4!} + \frac{1}{6!} + \cdots = \frac{e+e^{-1}}{2} - 1
= \frac{e + e^{-1} - 2}{2} \approx 0.5431 $$
:::

**Group C — Long answer (8 marks each)**

1. (a) Write down the general term of $(a+b)^{n}$ and use it to find the
   coefficient of $x^{5}$ in $\left(2x^{2} + \dfrac{3}{x}\right)^{10}$. <span class="marks">[4]</span>
   (b) If the coefficients of the $5^{\text{th}}$, $6^{\text{th}}$ and
   $7^{\text{th}}$ terms in the expansion of $(1+x)^{n}$ are in arithmetic
   progression, find $n$. <span class="marks">[4]</span>
2. (a) State the binomial theorem for any index and the condition for its
   validity. Expand $(1-x)^{-3}$ up to the term in $x^{3}$. <span class="marks">[4]</span>
   (b) Find $\sqrt[4]{17}$ correct to five decimal places using the binomial
   expansion. <span class="marks">[4]</span>
3. (a) Show that $e = \displaystyle\sum_{r=0}^{\infty}\frac{1}{r!}$ by expanding
   $\left(1+\dfrac1n\right)^{n}$, and prove that $2 < e < 3$. <span class="marks">[4]</span>
   (b) Prove that
   $\log_{e}\dfrac{1+x}{1-x} = 2\left(x + \dfrac{x^{3}}{3} + \dfrac{x^{5}}{5} + \cdots\right)$
   and hence find $\log_{e} 1.5$ correct to four decimal places. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** (a) $T_{r+1} = {}^{n}C_{r}a^{n-r}b^{r}$. For
$\left(2x^{2} + \dfrac3x\right)^{10}$,

$$ T_{r+1} = {}^{10}C_{r}(2x^{2})^{10-r}\left(\frac{3}{x}\right)^{r}
= {}^{10}C_{r}\,2^{10-r}3^{r}\,x^{20-2r-r} $$

Set $20 - 3r = 5$, so $r = 5$. The coefficient is

$$ ^{10}C_{5}\,2^{5}\,3^{5} = 252 \times 32 \times 243 = 1\,959\,552 $$

(b) The coefficients are $^{n}C_{4}$, $^{n}C_{5}$, $^{n}C_{6}$, and in AP means

$$ 2\,{}^{n}C_{5} = {}^{n}C_{4} + {}^{n}C_{6} $$

Divide throughout by $^{n}C_{5}$ and use
$\dfrac{^{n}C_{4}}{^{n}C_{5}} = \dfrac{5}{n-4}$ and
$\dfrac{^{n}C_{6}}{^{n}C_{5}} = \dfrac{n-5}{6}$:

$$ 2 = \frac{5}{n-4} + \frac{n-5}{6} $$

Multiply by $6(n-4)$:

$$ 12(n-4) = 30 + (n-5)(n-4) \;\Longrightarrow\; 12n - 48 = 30 + n^{2} - 9n + 20 $$

$$ n^{2} - 21n + 98 = 0 \;\Longrightarrow\; (n-7)(n-14) = 0 $$

So $n = 7$ or $n = 14$. **Check $n = 14$:** $^{14}C_{4} = 1001$,
$^{14}C_{5} = 2002$, $^{14}C_{6} = 3003$, and $2(2002) = 1001 + 3003$. ✓
**Check $n = 7$:** $35, 21, 7$ and $2(21) = 35 + 7$. ✓

**2.** (a) For any real $n$ and $|x| < 1$,

$$ (1+x)^{n} = 1 + nx + \frac{n(n-1)}{2!}x^{2} + \frac{n(n-1)(n-2)}{3!}x^{3} + \cdots $$

Put $n = -3$ and replace $x$ by $-x$:

$$ (1-x)^{-3} = 1 + (-3)(-x) + \frac{(-3)(-4)}{2}x^{2}
+ \frac{(-3)(-4)(-5)}{6}(-x^{3}) $$

$$ = 1 + 3x + 6x^{2} + 10x^{3} + \cdots \qquad (|x| < 1) $$

(The coefficients are the triangular numbers — a useful check.)

(b) The nearest fourth power is $16 = 2^{4}$:

$$ 17^{1/4} = (16+1)^{1/4} = 2\left(1 + \frac{1}{16}\right)^{1/4}
= 2(1 + 0.0625)^{1/4} $$

With $n = \tfrac14$, $x = 0.0625$:

$$ 2\left[1 + \frac{x}{4} + \frac{\frac14\left(-\frac34\right)}{2}x^{2}
+ \frac{\frac14\left(-\frac34\right)\left(-\frac74\right)}{6}x^{3}\right] $$

$$ = 2\left[1 + 0.015625 - \frac{3}{32}(0.00390625)
+ \frac{7}{128}(0.000244141)\right] $$

$$ = 2\left[1 + 0.015625 - 0.000366211 + 0.0000133514\right]
= 2(1.01527214) = 2.03054 $$

So $\sqrt[4]{17} \approx 2.03054$ (true value $2.0305432$).

**3.** (a) By the binomial theorem,

$$ \left(1+\frac1n\right)^{n} = 1 + 1 + \frac{1}{2!}\left(1-\frac1n\right)
+ \frac{1}{3!}\left(1-\frac1n\right)\left(1-\frac2n\right) + \cdots $$

Letting $n \to \infty$, each bracket tends to $1$, giving
$e = 1 + \dfrac{1}{1!} + \dfrac{1}{2!} + \cdots$

All terms are positive, so $e > 1 + 1 = 2$. Since $r! \ge 2^{\,r-1}$ for
$r \ge 1$,

$$ e < 1 + \left(1 + \frac12 + \frac{1}{2^{2}} + \cdots\right)
= 1 + \frac{1}{1-\frac12} = 3 $$

Hence $2 < e < 3$.

(b) From the logarithmic series,

$$ \log(1+x) = x - \frac{x^{2}}{2} + \frac{x^{3}}{3} - \frac{x^{4}}{4} + \cdots $$
$$ \log(1-x) = -x - \frac{x^{2}}{2} - \frac{x^{3}}{3} - \frac{x^{4}}{4} - \cdots $$

Subtracting, the even powers cancel and the odd ones double:

$$ \log\frac{1+x}{1-x} = 2\left(x + \frac{x^{3}}{3} + \frac{x^{5}}{5} + \cdots\right),
\qquad |x| < 1 $$

For $\log 1.5$ we need $\dfrac{1+x}{1-x} = \dfrac32$, which gives
$2 + 2x = 3 - 3x$, so $x = \dfrac15 = 0.2$. Then

$$ \log 1.5 = 2\left(0.2 + \frac{0.008}{3} + \frac{0.00032}{5}
+ \frac{0.0000128}{7}\right) $$

$$ = 2\left(0.2 + 0.0026667 + 0.000064 + 0.0000018\right) = 2(0.2027325)
= 0.405465 $$

So $\log_{e}1.5 \approx 0.4055$ (true value $0.4054651$).
:::
