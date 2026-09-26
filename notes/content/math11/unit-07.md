---
subject: Mathematics
grade: 11
unit: 7
title: Quadratic Equation
hours: 4
area: Algebra
---

A **quadratic equation** is any equation that can be written
$ax^{2} + bx + c = 0$ with $a \ne 0$. You have solved these since Grade 9. What is
new here is that you will answer questions about the roots *without finding them*:
how many real roots there are, what they add up to, what they multiply to, and how
to build an equation backwards from its roots. One expression — the discriminant —
controls almost all of it.

::: key The two facts this whole unit runs on
For $ax^{2}+bx+c = 0$ with roots $\alpha$ and $\beta$,
$$ \alpha + \beta = -\frac{b}{a}, \qquad \alpha\beta = \frac{c}{a},
\qquad D = b^{2}-4ac $$
Almost every question is solved by writing down the sum, the product and the
discriminant before doing anything else.
:::

## 7.1 Nature of roots

Completing the square on $ax^{2}+bx+c = 0$ gives the quadratic formula.

::: derivation The quadratic formula
Divide by $a$ (allowed, since $a \ne 0$) and move the constant across:

$$ x^{2} + \frac{b}{a}x = -\frac{c}{a} $$

Add $\left(\dfrac{b}{2a}\right)^{2}$ to both sides to complete the square:

$$ x^{2} + \frac{b}{a}x + \frac{b^{2}}{4a^{2}} = \frac{b^{2}}{4a^{2}} - \frac{c}{a}
= \frac{b^{2}-4ac}{4a^{2}} $$

$$ \left(x + \frac{b}{2a}\right)^{2} = \frac{b^{2}-4ac}{4a^{2}} $$

Taking square roots and rearranging,

$$ x = \frac{-b \pm \sqrt{b^{2}-4ac}}{2a} $$
:::

Everything about the *kind* of roots sits under the square-root sign.

::: definition Discriminant
$$ D = b^{2} - 4ac $$
is the **discriminant** of $ax^{2}+bx+c = 0$. It discriminates — it decides —
between the possible kinds of roots.
:::

Assume $a$, $b$, $c$ are **real**.

| Discriminant | Nature of the roots | The graph $y = ax^{2}+bx+c$ |
|---|---|---|
| $D > 0$, a perfect square | real, distinct, **rational** | cuts the $x$-axis at two rational points |
| $D > 0$, not a perfect square | real, distinct, **irrational** (a conjugate surd pair) | cuts the $x$-axis at two points |
| $D = 0$ | real and **equal**, both $= -b/2a$ | *touches* the $x$-axis at one point |
| $D < 0$ | no real roots; a **conjugate complex** pair | does not meet the $x$-axis |

The last two rows of the table assume $a$, $b$, $c$ are rational; irrational and
complex roots of a rational quadratic always come in conjugate pairs, so you can
never have exactly one irrational root.

```figure caption="The three cases. $D>0$ gives two crossings, $D=0$ gives one touch at the vertex, $D<0$ gives no crossing at all."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 3, figsize=(5.2,2.6), sharey=True)
x = np.linspace(-0.6, 4.6, 400)
data = [(3.0, '$x^{2}-4x+3$', '$D = 4 > 0$', '#1d6fb8', [1.0, 3.0], 'two real roots'),
        (4.0, '$x^{2}-4x+4$', '$D = 0$',     '#2e8b57', [2.0],      'one repeated root'),
        (6.0, '$x^{2}-4x+6$', '$D = -8 < 0$','#d9534f', [],         'no real root')]
for ax, (c, expr, dlab, col, roots, tag) in zip(axes, data):
    ax.plot(x, x**2 - 4*x + c, color=col, lw=1.9)
    ax.axhline(0, color=INK, lw=1.0)
    for r in roots:
        ax.plot([r], [0], 'o', color=col, ms=6.5, zorder=5)
        ax.annotate('$%g$' % r, (r, 0), textcoords='offset points',
                    xytext=(0,-15), ha='center', fontsize=8.8, color=col)
    ax.set_title(expr, fontsize=9.4, pad=4)
    ax.annotate(dlab, (2.0, 7.0), ha='center', fontsize=9.2, color=col)
    ax.annotate(tag, (2.0, -3.3), ha='center', fontsize=8.8, color=MUTED)
    ax.set_xlim(-0.8, 4.8); ax.set_ylim(-4.0, 8.4)
    ax.set_xticks([]); ax.set_yticks([])
    ax.spines[['top','right','left','bottom']].set_visible(False)
fig.subplots_adjust(wspace=0.10)
```

::: caution "No roots" is wrong
When $D < 0$ the equation still has **two** roots — they are just not real. Write
"the roots are imaginary (complex conjugates)", never "there are no roots".
:::

::: example Worked example 7.1
**Problem.** Discuss the nature of the roots of $2x^{2} - 7x + 3 = 0$, then solve it.

**Solution.** Here $a = 2$, $b = -7$, $c = 3$.

$$ D = b^{2} - 4ac = (-7)^{2} - 4(2)(3) = 49 - 24 = 25 $$

$D > 0$ and $25 = 5^{2}$ is a perfect square, so the roots are **real, distinct and
rational**.

$$ x = \frac{7 \pm \sqrt{25}}{4} = \frac{7 \pm 5}{4} = 3 \ \text{ or } \ \frac{1}{2} $$
:::

::: example Worked example 7.2
**Problem.** Find the values of $k$ for which
$x^{2} + 2(k+1)x + 9k - 5 = 0$ has equal roots.

**Solution.** Equal roots means $D = 0$. With $a = 1$, $b = 2(k+1)$, $c = 9k-5$,

$$ D = 4(k+1)^{2} - 4(9k-5) = 0 \;\Longrightarrow\; (k+1)^{2} - (9k-5) = 0 $$

$$ k^{2} + 2k + 1 - 9k + 5 = 0 \;\Longrightarrow\; k^{2} - 7k + 6 = 0 $$

$$ (k-1)(k-6) = 0 \;\Longrightarrow\; k = 1 \ \text{ or } \ k = 6 $$

**Check $k = 1$:** the equation is $x^{2}+4x+4 = 0$, i.e. $(x+2)^{2} = 0$ — equal
roots. **Check $k = 6$:** $x^{2}+14x+49 = 0$, i.e. $(x+7)^{2} = 0$. Both work.
:::

::: example Worked example 7.3
**Problem.** For what value of $m$ does
$(m+1)x^{2} + 2(m+3)x + (m+8) = 0$ have equal roots?

**Solution.** Set $D = 0$:

$$ 4(m+3)^{2} - 4(m+1)(m+8) = 0 \;\Longrightarrow\; (m+3)^{2} = (m+1)(m+8) $$

$$ m^{2} + 6m + 9 = m^{2} + 9m + 8 \;\Longrightarrow\; -3m + 1 = 0
\;\Longrightarrow\; m = \frac{1}{3} $$

Note $m = \tfrac13$ keeps $m+1 \ne 0$, so the equation really is quadratic. (Had
the answer been $m = -1$ we would have had to reject it.)
:::

::: tip Always check that $a \ne 0$
In a question with a parameter in the $x^{2}$ coefficient, a value that makes that
coefficient zero must be rejected — the equation stops being quadratic.
:::

## 7.2 Relation between roots and coefficients

::: derivation Sum and product of the roots
If $\alpha$ and $\beta$ are the roots of $ax^{2}+bx+c = 0$, then $ax^{2}+bx+c$
factorises as $a(x-\alpha)(x-\beta)$. Expanding,

$$ a(x-\alpha)(x-\beta) = ax^{2} - a(\alpha+\beta)x + a\alpha\beta $$

Comparing coefficients with $ax^{2}+bx+c$:

$$ -a(\alpha+\beta) = b \;\Longrightarrow\; \alpha+\beta = -\frac{b}{a},
\qquad a\alpha\beta = c \;\Longrightarrow\; \alpha\beta = \frac{c}{a} $$
:::

From these two, every symmetric expression in $\alpha$ and $\beta$ can be found
without ever solving the equation. Write $s = \alpha+\beta$ and $p = \alpha\beta$.

::: key The standard identities
$$ \alpha^{2}+\beta^{2} = s^{2} - 2p, \qquad (\alpha-\beta)^{2} = s^{2} - 4p $$
$$ \alpha^{3}+\beta^{3} = s^{3} - 3ps, \qquad
\frac{1}{\alpha}+\frac{1}{\beta} = \frac{s}{p}, \qquad
\frac{\alpha}{\beta}+\frac{\beta}{\alpha} = \frac{s^{2}-2p}{p} $$
Note that $(\alpha-\beta)^{2} = s^{2}-4p = \dfrac{b^{2}-4ac}{a^{2}} = \dfrac{D}{a^{2}}$ —
the discriminant appears again, which is why $D = 0$ means the roots coincide.
:::

The sum and product also read off the graph: the axis of symmetry of
$y = ax^{2}+bx+c$ sits at $x = -b/2a$, exactly halfway between the roots.

```figure caption="The roots of $x^{2}-5x+4$ are $1$ and $4$. Their mean $\\frac{5}{2}$ is the axis of symmetry $x = -b/2a$, and the vertex lies on it."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,3.0))
x = np.linspace(-0.3, 5.3, 400)
ax.plot(x, x**2 - 5*x + 4, color=ACCENT, lw=1.9)
ax.axhline(0, color=INK, lw=1.0)
ax.plot([2.5, 2.5], [-2.9, 5.6], color='#d9534f', lw=1.1, ls='--')
for r in (1.0, 4.0):
    ax.plot([r],[0],'o',color=ACCENT,ms=6.5,zorder=5)
ax.plot([2.5],[-2.25],'o',color='#d9534f',ms=5.5,zorder=5)
ax.annotate(r'$\alpha = 1$', (1,0), textcoords='offset points', xytext=(7,13),
            ha='left', fontsize=9.4, color=ACCENT)
ax.annotate(r'$\beta = 4$', (4,0), textcoords='offset points', xytext=(-7,13),
            ha='right', fontsize=9.4, color=ACCENT)
ax.annotate('axis of symmetry\n$x = -b/2a = 5/2$', (2.5, 6.3), ha='center',
            fontsize=9.0, color='#d9534f', linespacing=1.5)
ax.annotate('vertex', (2.5,-2.25), textcoords='offset points', xytext=(11,-4),
            ha='left', fontsize=9.0, color='#d9534f')
ax.annotate('', xy=(1,-2.95), xytext=(4,-2.95),
            arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=0.9, mutation_scale=8))
ax.annotate(r'$\alpha+\beta = 5$,    $\alpha\beta = 4$', (2.5,-3.75), ha='center',
            fontsize=9.4, color=MUTED)
ax.set_xlim(-0.6, 5.6); ax.set_ylim(-4.2, 7.6)
ax.set_xticks([]); ax.set_yticks([])
ax.spines[['top','right','left','bottom']].set_visible(False)
```

::: example Worked example 7.4
**Problem.** If $\alpha$ and $\beta$ are the roots of $2x^{2}-5x+3 = 0$, find
(a) $\alpha^{2}+\beta^{2}$, (b) $\alpha^{3}+\beta^{3}$,
(c) $\dfrac{1}{\alpha}+\dfrac{1}{\beta}$, (d) $\alpha-\beta$ — all without solving.

**Solution.** $s = \alpha+\beta = -\dfrac{-5}{2} = \dfrac52$ and
$p = \alpha\beta = \dfrac32$.

(a) $\;\alpha^{2}+\beta^{2} = s^{2}-2p = \dfrac{25}{4} - 3 = \dfrac{13}{4}$

(b) $\;\alpha^{3}+\beta^{3} = s^{3} - 3ps = \dfrac{125}{8} - 3\left(\dfrac32\right)\left(\dfrac52\right)
= \dfrac{125}{8} - \dfrac{45}{4} = \dfrac{125-90}{8} = \dfrac{35}{8}$

(c) $\;\dfrac{1}{\alpha}+\dfrac{1}{\beta} = \dfrac{s}{p} = \dfrac{5/2}{3/2} = \dfrac53$

(d) $\;(\alpha-\beta)^{2} = s^{2}-4p = \dfrac{25}{4} - 6 = \dfrac14$, so
$\alpha-\beta = \pm\dfrac12$

**Check.** The roots really are $\tfrac32$ and $1$; their sum is $\tfrac52$, their
difference $\tfrac12$, and $\left(\tfrac32\right)^{2}+1^{2} = \tfrac{13}{4}$.
:::

::: example Worked example 7.5
**Problem.** If one root of $x^{2}+px+q = 0$ is double the other, show that
$2p^{2} = 9q$.

**Solution.** Let the roots be $\alpha$ and $2\alpha$.

$$ \text{Sum: } \alpha + 2\alpha = 3\alpha = -p \;\Longrightarrow\; \alpha = -\frac{p}{3} $$
$$ \text{Product: } \alpha(2\alpha) = 2\alpha^{2} = q $$

Substituting the first into the second,

$$ 2\left(-\frac{p}{3}\right)^{2} = q \;\Longrightarrow\; \frac{2p^{2}}{9} = q
\;\Longrightarrow\; 2p^{2} = 9q $$
:::

## 7.3 Formation of quadratic equation

Reverse the relation. If a quadratic with leading coefficient $1$ has roots
$\alpha$ and $\beta$, then

$$ (x-\alpha)(x-\beta) = 0 \;\Longrightarrow\;
x^{2} - (\alpha+\beta)x + \alpha\beta = 0 $$

::: key Forming an equation
$$ x^{2} - (\text{sum of roots})\,x + (\text{product of roots}) = 0 $$
Find the sum and the product of the *required* roots, substitute, and clear
fractions at the end. Never find the actual roots unless you have to.
:::

::: example Worked example 7.6
**Problem.** Form the quadratic equation whose roots are $2+\sqrt{3}$ and
$2-\sqrt{3}$.

**Solution.**

$$ \text{Sum} = (2+\sqrt{3})+(2-\sqrt{3}) = 4 $$
$$ \text{Product} = (2+\sqrt{3})(2-\sqrt{3}) = 4 - 3 = 1 $$

$$ x^{2} - 4x + 1 = 0 $$

Notice the surds cancel — that is the point of conjugate pairs, and it is why an
equation with rational coefficients cannot have just one surd root.
:::

::: example Worked example 7.7
**Problem.** If $\alpha$, $\beta$ are the roots of $x^{2}-6x+8 = 0$, form the
equation whose roots are $\alpha^{2}$ and $\beta^{2}$.

**Solution.** $s = 6$, $p = 8$. For the *new* roots:

$$ \text{Sum} = \alpha^{2}+\beta^{2} = s^{2}-2p = 36-16 = 20 $$
$$ \text{Product} = \alpha^{2}\beta^{2} = (\alpha\beta)^{2} = 64 $$

$$ x^{2} - 20x + 64 = 0 $$

**Check.** The original roots are $2$ and $4$, so the new roots should be $4$ and
$16$: $4+16 = 20$ and $4 \times 16 = 64$. Correct.
:::

::: example Worked example 7.8
**Problem.** If $\alpha$, $\beta$ are the roots of $x^{2}+px+q = 0$, form the
equation whose roots are $\dfrac{\alpha}{\beta}$ and $\dfrac{\beta}{\alpha}$.

**Solution.** Here $s = -p$ and $\alpha\beta = q$.

$$ \text{Sum} = \frac{\alpha}{\beta}+\frac{\beta}{\alpha}
= \frac{\alpha^{2}+\beta^{2}}{\alpha\beta} = \frac{s^{2}-2q}{q} = \frac{p^{2}-2q}{q} $$
$$ \text{Product} = \frac{\alpha}{\beta}\cdot\frac{\beta}{\alpha} = 1 $$

$$ x^{2} - \frac{p^{2}-2q}{q}x + 1 = 0 \;\Longrightarrow\;
qx^{2} - \left(p^{2}-2q\right)x + q = 0 $$
:::

## 7.4 Symmetric roots; one or both roots common

### Symmetric functions of the roots

An expression in $\alpha$ and $\beta$ is **symmetric** if swapping $\alpha$ and
$\beta$ leaves it unchanged — for example $\alpha^{2}+\beta^{2}$,
$\alpha^{3}\beta^{3}$, or $\dfrac{1}{\alpha}+\dfrac{1}{\beta}$. Every symmetric expression
can be written in terms of $s$ and $p$ alone, so it can be evaluated straight from
the coefficients. That is exactly what §7.2 and §7.3 exploit.

$\alpha - \beta$ is **not** symmetric (swapping gives $\beta-\alpha$), which is why
we can only ever pin down $(\alpha-\beta)^{2}$ and are left with a $\pm$.

### One root common

Suppose $a_1x^{2}+b_1x+c_1 = 0$ and $a_2x^{2}+b_2x+c_2 = 0$ share exactly one root
$\alpha$. In an exam you usually have numbers, and the fastest route is direct:

::: tip The three-line method for a common root
1. Solve whichever equation factorises.
2. Substitute each of its roots into the other equation.
3. Whichever value of the unknown makes it true is the answer.
:::

There is also a general condition. Substituting $x = \alpha$ in both and
eliminating $\alpha$ between them (by cross-multiplication) gives

$$ \left(c_1a_2 - c_2a_1\right)^{2} = \left(a_1b_2 - a_2b_1\right)\left(b_1c_2 - b_2c_1\right) $$

and the common root itself is

$$ \alpha = \frac{c_1a_2-c_2a_1}{a_1b_2-a_2b_1} $$

### Both roots common

If both roots are common, the two quadratics are the same equation up to a
constant multiple, so their coefficients are proportional:

$$ \frac{a_1}{a_2} = \frac{b_1}{b_2} = \frac{c_1}{c_2} $$

```figure caption="$y = x^{2}-5x+6$ and $y = x^{2}-3x+2$ share the root $x = 2$ only: both curves cross the $x$-axis at the same point, but their other roots differ."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,3.0))
x = np.linspace(-0.2, 4.2, 400)
ax.plot(x, x**2-5*x+6, color=ACCENT, lw=1.9, label='$x^{2}-5x+6$')
ax.plot(x, x**2-3*x+2, color='#d9534f', lw=1.9, label='$x^{2}-3x+2$')
ax.axhline(0, color=INK, lw=1.0)
ax.plot([2],[0],'o',color='#2e8b57',ms=9,zorder=6)
ax.plot([3],[0],'o',color=ACCENT,ms=5.5,zorder=5)
ax.plot([1],[0],'o',color='#d9534f',ms=5.5,zorder=5)
ax.annotate('$x = 1$', (1,0), textcoords='offset points', xytext=(-9,-16),
            ha='right', fontsize=9.2, color='#d9534f')
ax.annotate('$x = 3$', (3,0), textcoords='offset points', xytext=(9,-16),
            ha='left', fontsize=9.2, color=ACCENT)
ax.annotate('common root  $x = 2$', (2,0), textcoords='offset points', xytext=(0,-40),
            ha='center', fontsize=9.4, color='#2e8b57')
ax.annotate('', xy=(2,-0.28), xytext=(2,-1.30),
            arrowprops=dict(arrowstyle='-', color='#2e8b57', lw=1.0))
ax.set_xlim(-0.4, 4.4); ax.set_ylim(-2.3, 6.6)
ax.set_xticks([]); ax.set_yticks([])
ax.spines[['top','right','left','bottom']].set_visible(False)
ax.legend(loc='upper center', ncol=2, fontsize=8.8, frameon=False)
```

::: example Worked example 7.9
**Problem.** Find the value of $k$ for which $x^{2}-5x+6 = 0$ and
$x^{2}-3x+k = 0$ have a common root.

**Solution.** The first equation factorises: $(x-2)(x-3) = 0$, so its roots are
$2$ and $3$. One of these must satisfy the second equation.

*If the common root is $2$:* $\;4 - 6 + k = 0 \Rightarrow k = 2$.

*If the common root is $3$:* $\;9 - 9 + k = 0 \Rightarrow k = 0$.

So $k = 2$ or $k = 0$.

**Check $k = 2$:** $x^{2}-3x+2 = (x-1)(x-2)$, roots $1$ and $2$ — shares $2$.
**Check $k = 0$:** $x^{2}-3x = x(x-3)$, roots $0$ and $3$ — shares $3$. Both valid.
:::

::: example Worked example 7.10
**Problem.** The equations $2x^{2}+3x+5 = 0$ and $ax^{2}+bx+c = 0$ have **both**
roots in common. If $a = 6$, find $b$ and $c$.

**Solution.** Both roots common means the coefficients are proportional:

$$ \frac{a}{2} = \frac{b}{3} = \frac{c}{5} $$

With $a = 6$ the common ratio is $\dfrac{6}{2} = 3$, so

$$ b = 3 \times 3 = 9, \qquad c = 3 \times 5 = 15 $$

The second equation is $6x^{2}+9x+15 = 0$, which is just $3$ times the first — so
of course the roots are identical.
:::

::: example Worked example 7.11
**Problem.** Find the value of $k$ for which the roots of
$kx^{2} - 2(1+2k)x + 3(2+k) = 0$ are equal.

**Solution.** Set $D = 0$ with $a = k$, $b = -2(1+2k)$, $c = 3(2+k)$:

$$ 4(1+2k)^{2} - 4k\cdot 3(2+k) = 0 \;\Longrightarrow\; (1+2k)^{2} - 3k(2+k) = 0 $$

$$ 1 + 4k + 4k^{2} - 6k - 3k^{2} = 0 \;\Longrightarrow\; k^{2} - 2k + 1 = 0 $$

$$ (k-1)^{2} = 0 \;\Longrightarrow\; k = 1 $$

Since $k = 1 \ne 0$, the equation is genuinely quadratic. **Check:** at $k=1$ the
equation is $x^{2}-6x+9 = 0$, i.e. $(x-3)^{2} = 0$ — equal roots $x = 3$.
:::

::: example Worked example 7.12
**Problem.** If the equations $x^{2}+bx+c = 0$ and $x^{2}+cx+b = 0$ ($b \ne c$) have
a common root, find that root and the relation between $b$ and $c$.

**Solution.** Let $\alpha$ be the common root. Then

$$ \alpha^{2}+b\alpha+c = 0 \qquad \text{and} \qquad \alpha^{2}+c\alpha+b = 0 $$

Subtracting the second from the first removes $\alpha^{2}$:

$$ (b-c)\alpha + (c-b) = 0 \;\Longrightarrow\; (b-c)(\alpha - 1) = 0 $$

Since $b \ne c$ we may divide by $b-c$, giving $\alpha = 1$.

Putting $\alpha = 1$ back into the first equation:

$$ 1 + b + c = 0 \;\Longrightarrow\; b + c = -1 $$

So the common root is $1$ and $b+c+1 = 0$. (Subtracting the two equations is the
standard first move whenever both are monic — it turns a pair of quadratics into
one linear equation.)
:::

## Chapter summary

- $ax^{2}+bx+c = 0$ has roots $x = \dfrac{-b\pm\sqrt{b^{2}-4ac}}{2a}$.
- Discriminant $D = b^{2}-4ac$: $D > 0$ real distinct ($D$ a perfect square makes
  them rational), $D = 0$ real and equal, $D < 0$ a conjugate complex pair.
- $\alpha+\beta = -b/a$ and $\alpha\beta = c/a$; and
  $(\alpha-\beta)^{2} = D/a^{2}$.
- Useful identities: $\alpha^{2}+\beta^{2} = s^{2}-2p$,
  $\alpha^{3}+\beta^{3} = s^{3}-3ps$, $\dfrac{1}{\alpha}+\dfrac{1}{\beta} = \dfrac{s}{p}$.
- To form an equation: $x^{2} - (\text{sum})x + (\text{product}) = 0$.
- Symmetric expressions in the roots can always be written in $s$ and $p$;
  $\alpha-\beta$ cannot, so it carries a $\pm$.
- One root common: substitute the known roots of one equation into the other; in
  general $(c_1a_2-c_2a_1)^{2} = (a_1b_2-a_2b_1)(b_1c_2-b_2c_1)$.
- Both roots common: $\dfrac{a_1}{a_2} = \dfrac{b_1}{b_2} = \dfrac{c_1}{c_2}$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The roots of $x^{2}-5x+6 = 0$ are <span class="marks">[1]</span>
   (a) $-2, -3$ (b) $2, 3$ (c) $1, 6$ (d) $-1, -6$
2. The roots of $ax^{2}+bx+c = 0$ are real and equal if <span class="marks">[1]</span>
   (a) $b^{2}-4ac > 0$ (b) $b^{2}-4ac = 0$ (c) $b^{2}-4ac < 0$ (d) $b^{2} = 4a$
3. If $\alpha$, $\beta$ are the roots of $x^{2}-3x+2 = 0$, then
   $\alpha+\beta$ is <span class="marks">[1]</span>
   (a) $-3$ (b) $2$ (c) $3$ (d) $-2$
4. The quadratic equation whose roots are $3$ and $-2$ is <span class="marks">[1]</span>
   (a) $x^{2}-x-6 = 0$ (b) $x^{2}+x-6 = 0$ (c) $x^{2}-x+6 = 0$ (d) $x^{2}+5x+6 = 0$
5. If the roots of $ax^{2}+bx+c = 0$ are reciprocals of each other, then <span class="marks">[1]</span>
   (a) $a = b$ (b) $b = c$ (c) $a = c$ (d) $a+b+c = 0$
6. If $D < 0$ for a quadratic with real coefficients, the graph of
   $y = ax^{2}+bx+c$ <span class="marks">[1]</span>
   (a) cuts the $x$-axis twice (b) touches the $x$-axis (c) never meets the $x$-axis (d) is a straight line

::: note Answers to Group A
**1.** (b) — $(x-2)(x-3) = 0$.

**2.** (b) — $D = 0$ makes the $\pm\sqrt{D}$ term vanish.

**3.** (c) — $\alpha+\beta = -b/a = 3$.

**4.** (a) — sum $= 1$, product $= -6$, so $x^{2}-x-6 = 0$.

**5.** (c) — if the roots are $\alpha$ and $1/\alpha$ then the product
$c/a = 1$, so $a = c$.

**6.** (c) — no real root means no real $x$ with $y = 0$.
:::

**Group B — Short answer (5 marks each)**

1. Discuss the nature of the roots of $3x^{2}-2x+1 = 0$ and of
   $4x^{2}-12x+9 = 0$. <span class="marks">[5]</span>
2. Find the values of $k$ for which $x^{2} - 2(1+3k)x + 7(3+2k) = 0$ has equal
   roots. <span class="marks">[5]</span>
3. If $\alpha$, $\beta$ are the roots of $2x^{2}+3x-4 = 0$, find
   $\alpha^{2}+\beta^{2}$ and $\dfrac{1}{\alpha^{2}}+\dfrac{1}{\beta^{2}}$. <span class="marks">[5]</span>
4. If $\alpha$, $\beta$ are the roots of $3x^{2}-5x+2 = 0$, form the equation whose
   roots are $\dfrac{1}{\alpha}$ and $\dfrac{1}{\beta}$. <span class="marks">[5]</span>
5. Find the value of $k$ if $x^{2}-7x+12 = 0$ and $x^{2}-8x+k = 0$ have a common
   root. <span class="marks">[5]</span>
6. If one root of $x^{2}+px+q = 0$ is three times the other, show that
   $3p^{2} = 16q$. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** For $3x^{2}-2x+1 = 0$: $D = (-2)^{2}-4(3)(1) = 4-12 = -8 < 0$, so the roots
are **imaginary**, a conjugate complex pair.

For $4x^{2}-12x+9 = 0$: $D = 144 - 4(4)(9) = 144-144 = 0$, so the roots are
**real and equal**, both $x = -b/2a = 12/8 = \tfrac32$. (Indeed
$4x^{2}-12x+9 = (2x-3)^{2}$.)

**2.** $D = 0$ gives $4(1+3k)^{2} - 28(3+2k) = 0$, i.e.
$(1+3k)^{2} - 7(3+2k) = 0$.

$$ 1 + 6k + 9k^{2} - 21 - 14k = 0 \;\Longrightarrow\; 9k^{2} - 8k - 20 = 0 $$

$$ k = \frac{8 \pm \sqrt{64 + 720}}{18} = \frac{8 \pm 28}{18}
= 2 \ \text{ or } \ -\frac{10}{9} $$

**3.** $s = -\tfrac32$, $p = -2$.

$$ \alpha^{2}+\beta^{2} = s^{2}-2p = \frac94 + 4 = \frac{25}{4} $$

$$ \frac{1}{\alpha^{2}}+\frac{1}{\beta^{2}} = \frac{\alpha^{2}+\beta^{2}}{(\alpha\beta)^{2}}
= \frac{25/4}{4} = \frac{25}{16} $$

**4.** For $3x^{2}-5x+2 = 0$, $s = \tfrac53$ and $p = \tfrac23$. The new roots have

$$ \text{sum} = \frac{1}{\alpha}+\frac{1}{\beta} = \frac{s}{p} = \frac{5/3}{2/3} = \frac52,
\qquad \text{product} = \frac{1}{\alpha\beta} = \frac{1}{2/3} = \frac32 $$

$$ x^{2} - \frac52 x + \frac32 = 0 \;\Longrightarrow\; 2x^{2}-5x+3 = 0 $$

(Sensible: reversing the coefficients of a quadratic inverts its roots. The
original roots are $\tfrac23$ and $1$; the new ones are $\tfrac32$ and $1$.)

**5.** $x^{2}-7x+12 = (x-3)(x-4)$, so its roots are $3$ and $4$.

If the common root is $3$: $9 - 24 + k = 0 \Rightarrow k = 15$.
If the common root is $4$: $16 - 32 + k = 0 \Rightarrow k = 16$.

So $k = 15$ or $k = 16$.

**6.** Let the roots be $\alpha$ and $3\alpha$. Then $4\alpha = -p$, so
$\alpha = -p/4$; and $3\alpha^{2} = q$. Substituting,

$$ 3\left(\frac{p^{2}}{16}\right) = q \;\Longrightarrow\; 3p^{2} = 16q $$
:::

**Group C — Long answer (8 marks each)**

1. (a) Derive the quadratic formula by completing the square. <span class="marks">[4]</span>
   (b) Define the discriminant and describe the nature of the roots in each of its
   three cases, giving one numerical example of each. <span class="marks">[4]</span>
2. (a) If $\alpha$, $\beta$ are the roots of $ax^{2}+bx+c = 0$, prove that
   $\alpha+\beta = -\dfrac{b}{a}$ and $\alpha\beta = \dfrac{c}{a}$. <span class="marks">[3]</span>
   (b) If $\alpha$, $\beta$ are the roots of $x^{2}-6x+8 = 0$, form the equation
   whose roots are $\alpha+\dfrac{1}{\beta}$ and $\beta+\dfrac{1}{\alpha}$. <span class="marks">[5]</span>
3. (a) Show that if the two equations $a_1x^{2}+b_1x+c_1 = 0$ and
   $a_2x^{2}+b_2x+c_2 = 0$ have both roots common then
   $\dfrac{a_1}{a_2} = \dfrac{b_1}{b_2} = \dfrac{c_1}{c_2}$. <span class="marks">[4]</span>
   (b) Find $k$ so that $x^{2}-5x+6=0$ and $x^{2}-3x+k=0$ have a common root, and
   in each case state the common root. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** (a) See the derivation in §7.1: divide by $a$, complete the square by adding
$(b/2a)^{2}$, and take square roots to get
$x = \dfrac{-b\pm\sqrt{b^{2}-4ac}}{2a}$.

(b) $D = b^{2}-4ac$.
$D > 0$: real and distinct — e.g. $x^{2}-5x+6 = 0$ with $D = 1$, roots $2, 3$.
$D = 0$: real and equal — e.g. $x^{2}-4x+4 = 0$, double root $2$.
$D < 0$: a conjugate complex pair — e.g. $x^{2}+x+1 = 0$ with $D = -3$.

**2.** (a) Since $\alpha$, $\beta$ are the roots,
$ax^{2}+bx+c \equiv a(x-\alpha)(x-\beta) = ax^{2} - a(\alpha+\beta)x + a\alpha\beta$.
Comparing the coefficients of $x$ and the constants gives
$\alpha+\beta = -b/a$ and $\alpha\beta = c/a$.

(b) For $x^{2}-6x+8=0$: $s = 6$, $p = 8$ (the roots are $2$ and $4$).

$$ \text{Sum} = \alpha + \beta + \frac{1}{\alpha} + \frac{1}{\beta} = s + \frac{s}{p}
= 6 + \frac68 = \frac{27}{4} $$

$$ \text{Product} = \left(\alpha+\frac{1}{\beta}\right)\left(\beta+\frac{1}{\alpha}\right)
= \alpha\beta + 1 + 1 + \frac{1}{\alpha\beta} = 8 + 2 + \frac18 = \frac{81}{8} $$

$$ x^{2} - \frac{27}{4}x + \frac{81}{8} = 0 \;\Longrightarrow\;
8x^{2} - 54x + 81 = 0 $$

**Check.** The new roots are $2+\tfrac14 = \tfrac94$ and $4+\tfrac12 = \tfrac92$;
their sum is $\tfrac{27}{4}$ and product $\tfrac{81}{8}$. Correct.

**3.** (a) Let the common roots be $\alpha$ and $\beta$. Then
$a_1x^{2}+b_1x+c_1 = a_1(x-\alpha)(x-\beta)$ and
$a_2x^{2}+b_2x+c_2 = a_2(x-\alpha)(x-\beta)$. Dividing one identity by the other,

$$ \frac{a_1x^{2}+b_1x+c_1}{a_2x^{2}+b_2x+c_2} = \frac{a_1}{a_2} $$

for all $x$, so the two quadratics are proportional term by term:
$\dfrac{a_1}{a_2} = \dfrac{b_1}{b_2} = \dfrac{c_1}{c_2}$.

(b) Roots of the first are $2$ and $3$. Putting $x = 2$ in the second:
$4-6+k = 0$, so $k = 2$ (common root $2$). Putting $x = 3$: $9-9+k = 0$, so
$k = 0$ (common root $3$).
:::
