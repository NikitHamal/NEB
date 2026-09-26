---
subject: Mathematics
grade: 11
unit: 5
title: Sequence and Series
hours: 6
area: Algebra
---

A **sequence** is a list of numbers written in a definite order; a **series** is
what you get when you add the terms of a sequence. Three patterns cover almost
all of school mathematics: adding a fixed number each time (arithmetic),
multiplying by a fixed number each time (geometric), and taking reciprocals of an
arithmetic pattern (harmonic). This unit gives you the $n^{\text{th}}$ term and
the sum for each, the three means that sit between two numbers, and the
surprising fact that an endless sum of numbers can still be finite.

::: key What the exam asks
Almost every question is one of four shapes: *find a term*, *find a sum*, *insert
means*, or *given two facts about a sequence find the sequence*. The last shape —
two equations in $a$ and $d$ (or $a$ and $r$) — is the commonest Group B item.
Learn to set up and divide the two equations.
:::

## 5.1 Arithmetic, geometric and harmonic sequences and series

### Arithmetic progression (AP)

A sequence is an **arithmetic progression** if each term after the first is got by
adding a fixed number $d$, the **common difference**, to the one before it. With
first term $a$,

$$ a,\ a+d,\ a+2d,\ a+3d,\ \ldots $$

so the $n^{\text{th}}$ term (also written $t_n$ or $a_n$) is

$$ t_n = a + (n-1)d $$

The test for an AP is that $t_{n} - t_{n-1}$ is the *same* for every $n$.

::: derivation Sum of the first $n$ terms of an AP
Write the sum forwards and then backwards, where $l = a+(n-1)d$ is the last term:

$$ S_n = a + (a+d) + \cdots + (l-d) + l $$
$$ S_n = l + (l-d) + \cdots + (a+d) + a $$

Add the two lines term by term. Every one of the $n$ pairs adds up to $a+l$:

$$ 2S_n = n(a+l) \quad\Longrightarrow\quad S_n = \frac{n}{2}(a+l) $$

Putting $l = a+(n-1)d$ gives the working form

$$ S_n = \frac{n}{2}\left[2a + (n-1)d\right] $$
:::

Two small results follow and are worth knowing: $t_n = S_n - S_{n-1}$, and if
$a$, $b$, $c$ are in AP then $2b = a+c$.

### Geometric progression (GP)

A sequence is a **geometric progression** if each term after the first is got by
multiplying the one before it by a fixed non-zero number $r$, the **common
ratio**:

$$ a,\ ar,\ ar^{2},\ ar^{3},\ \ldots \qquad t_n = ar^{\,n-1} $$

The test for a GP is that $t_n / t_{n-1}$ is the same for every $n$.

::: derivation Sum of the first $n$ terms of a GP
$$ S_n = a + ar + ar^{2} + \cdots + ar^{\,n-1} $$

Multiply throughout by $r$:

$$ rS_n = ar + ar^{2} + \cdots + ar^{\,n-1} + ar^{\,n} $$

Subtract the second line from the first. Everything in the middle cancels:

$$ S_n - rS_n = a - ar^{\,n} \quad\Longrightarrow\quad S_n(1-r) = a(1-r^{n}) $$

$$ S_n = \frac{a(1-r^{n})}{1-r} \quad (r \ne 1), \qquad
S_n = \frac{a(r^{n}-1)}{r-1} $$

The two forms are identical; use the first when $r < 1$ and the second when
$r > 1$ so that you never handle negative numerators. If $r = 1$ the sequence is
$a, a, a, \ldots$ and $S_n = na$.
:::

If $a$, $b$, $c$ are in GP then $b^{2} = ac$.

```figure caption="An AP grows by equal steps, a GP by equal factors. Both start at $2$; the AP adds $3$, the GP multiplies by $1.6$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.8))
n = np.arange(1, 10)
ap = 2 + 3*(n-1)
gp = 2 * 1.6**(n-1)
ax.plot(n, ap, 'o-', color=ACCENT, ms=4.5, label='AP  $t_n = 2+3(n-1)$')
ax.plot(n, gp, 's-', color='#d9534f', ms=4.5, label='GP  $t_n = 2(1.6)^{n-1}$')
ax.annotate('add 3 each step', (3.2, 8.2), (1.05, 15.5), color=ACCENT, fontsize=8.8,
            arrowprops=dict(arrowstyle='-', color=ACCENT, lw=0.8))
ax.annotate('multiply by 1.6\neach step', (4.35, 34.5), color='#d9534f', fontsize=8.6)
ax.set_xlabel('term number  $n$'); ax.set_ylabel('$t_n$')
ax.set_xlim(0.5, 9.6); ax.set_ylim(0, 45)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.5); ax.legend(loc='lower right')
```

### Harmonic progression (HP)

A sequence of non-zero numbers is a **harmonic progression** if the reciprocals of
its terms form an AP. So $\tfrac{1}{3}, \tfrac{1}{7}, \tfrac{1}{11}, \ldots$ is an
HP because $3, 7, 11, \ldots$ is an AP.

::: key How to handle every HP question
Turn the terms upside down, work with the resulting AP, and invert the answer at
the very end. There is no separate formula worth memorising; the $n^{\text{th}}$
term of an HP whose reciprocals have first term $a$ and common difference $d$ is

$$ t_n = \frac{1}{a + (n-1)d} $$

There is **no elementary formula** for the sum of an HP — NEB never asks for one.
:::

| | AP | GP | HP |
|---|---|---|---|
| Built by | adding $d$ | multiplying by $r$ | reciprocals form an AP |
| $n^{\text{th}}$ term | $a+(n-1)d$ | $ar^{\,n-1}$ | $1/[a+(n-1)d]$ |
| Test on three terms | $2b = a+c$ | $b^{2} = ac$ | $b = 2ac/(a+c)$ |
| Sum of $n$ terms | $\frac{n}{2}[2a+(n-1)d]$ | $\frac{a(r^{n}-1)}{r-1}$ | no simple formula |

::: example Worked example 5.1
**Problem.** Which term of the arithmetic progression $7, 11, 15, \ldots$ is $179$?

**Solution.** Here $a = 7$ and $d = 11 - 7 = 4$. Set $t_n = 179$:

$$ 7 + (n-1)4 = 179 $$

Subtract $7$: $\;4(n-1) = 172$, so $n - 1 = 43$ and $n = 44$.

The $44^{\text{th}}$ term is $179$.
:::

::: example Worked example 5.2
**Problem.** The sum of the first $10$ terms of an AP is $175$ and the sum of the
first $20$ terms is $650$. Find the progression.

**Solution.** Use $S_n = \frac{n}{2}[2a+(n-1)d]$ twice.

$$ S_{10} = 5(2a + 9d) = 175 \;\Longrightarrow\; 2a + 9d = 35 $$
$$ S_{20} = 10(2a + 19d) = 650 \;\Longrightarrow\; 2a + 19d = 65 $$

Subtracting the first from the second eliminates $a$: $\;10d = 30$, so $d = 3$.
Then $2a = 35 - 9(3) = 8$, giving $a = 4$.

The progression is $4,\ 7,\ 10,\ 13,\ \ldots$
:::

::: example Worked example 5.3
**Problem.** The third term of a GP is $12$ and the sixth term is $96$. Find the
first term, the common ratio and the sum of the first eight terms.

**Solution.** From $t_n = ar^{\,n-1}$,

$$ ar^{2} = 12 \qquad\text{and}\qquad ar^{5} = 96 $$

**Divide** the second equation by the first — this is the standard move, because
$a$ cancels:

$$ \frac{ar^{5}}{ar^{2}} = r^{3} = \frac{96}{12} = 8 \;\Longrightarrow\; r = 2 $$

Then $a(2)^{2} = 12$ gives $a = 3$. Since $r > 1$,

$$ S_8 = \frac{a(r^{8}-1)}{r-1} = \frac{3(256-1)}{1} = 3 \times 255 = 765 $$
:::

::: example Worked example 5.4
**Problem.** (a) Find the $8^{\text{th}}$ term of the HP
$\tfrac{1}{3}, \tfrac{1}{7}, \tfrac{1}{11}, \ldots$
(b) Which term of the HP $\tfrac{1}{2}, \tfrac{1}{5}, \tfrac{1}{8}, \ldots$
equals $\tfrac{1}{98}$?

**Solution.** (a) Invert: the reciprocals $3, 7, 11, \ldots$ form an AP with
$a = 3$, $d = 4$. Its eighth term is $3 + 7(4) = 31$. Inverting back, the
$8^{\text{th}}$ term of the HP is $\dfrac{1}{31}$.

(b) Invert: $2, 5, 8, \ldots$ is an AP with $a = 2$, $d = 3$, and we need the term
equal to $98$:

$$ 2 + (n-1)3 = 98 \;\Longrightarrow\; 3(n-1) = 96 \;\Longrightarrow\; n = 33 $$

So $\tfrac{1}{98}$ is the $33^{\text{rd}}$ term.
:::

::: example Worked example 5.5
**Problem.** A shopkeeper in Birgunj saves Rs 2000 in the first month of a savings
scheme and increases the amount by Rs 250 every month. How much has she saved at
the end of two years?

**Solution.** The monthly amounts form an AP with $a = 2000$, $d = 250$ and
$n = 24$ months.

$$ S_{24} = \frac{24}{2}\left[2(2000) + 23(250)\right] = 12\left[4000 + 5750\right] $$
$$ = 12 \times 9750 = 117\,000 $$

She has saved **Rs 1,17,000**.
:::

::: caution $n$ is a positive whole number
If solving for $n$ gives a fraction or a negative value, the number you were
given is simply not a term of that sequence — say so. Do not round $n$ to the
nearest integer.
:::

## 5.2 A.M., G.M., H.M. and their relations

### The three means of two numbers

For two numbers $a$ and $b$ (positive, unless stated otherwise):

::: definition The three means
- The **arithmetic mean** $A$ is the number that makes $a, A, b$ an AP:
  $2A = a+b$, so $A = \dfrac{a+b}{2}$.
- The **geometric mean** $G$ makes $a, G, b$ a GP: $G^{2} = ab$, so
  $G = \sqrt{ab}$.
- The **harmonic mean** $H$ makes $a, H, b$ an HP, i.e. $\dfrac1a, \dfrac1H, \dfrac1b$
  is an AP: $\dfrac{2}{H} = \dfrac1a + \dfrac1b$, so $H = \dfrac{2ab}{a+b}$.
:::

Each definition is just "the middle term of the corresponding progression".

### Inserting $n$ means between two numbers

To insert $n$ arithmetic means between $a$ and $b$ is to build an AP with $n+2$
terms in which $a$ is the first and $b$ is the last. So $b = a + (n+1)d$, giving

$$ d = \frac{b-a}{n+1} $$

For $n$ geometric means we need a GP of $n+2$ terms, so $b = ar^{\,n+1}$ and

$$ r = \left(\frac{b}{a}\right)^{1/(n+1)} $$

For $n$ harmonic means, insert $n$ arithmetic means between $1/a$ and $1/b$ and
invert every one of them at the end.

::: tip Count the terms, not the means
The commonest slip is writing $b = a+nd$. Inserting $n$ means makes
$n+2$ terms, so the last term is the $(n+2)^{\text{th}}$, which is $a+(n+1)d$.
:::

### The relation $A \ge G \ge H$ and $G^{2} = AH$

::: derivation $G^{2} = AH$ and $A \ge G \ge H$
**The product relation.** Multiply $A$ and $H$:

$$ AH = \frac{a+b}{2}\cdot\frac{2ab}{a+b} = ab = G^{2} $$

So $A$, $G$, $H$ are themselves in geometric progression. This is the single most
useful identity in the section: given any two of the three means you get the third
at once.

**The inequality.** For positive $a$, $b$,

$$ A - G = \frac{a+b}{2} - \sqrt{ab} = \frac{a - 2\sqrt{ab} + b}{2}
= \frac{\left(\sqrt{a}-\sqrt{b}\right)^{2}}{2} \ge 0 $$

because a square is never negative. Hence $A \ge G$, with equality only when
$\sqrt{a} = \sqrt{b}$, i.e. $a = b$. Now from $G^{2} = AH$ we get
$H = G^{2}/A$, so

$$ G - H = G - \frac{G^{2}}{A} = \frac{G(A-G)}{A} \ge 0 $$

since $G > 0$, $A > 0$ and $A - G \ge 0$. Therefore

$$ A \ge G \ge H $$

with all three equal exactly when $a = b$.
:::

The inequality has a clean picture. Draw a semicircle on a diameter of length
$a+b$; then the radius is $A$, the perpendicular half-chord is $G$, and a second
perpendicular inside the triangle is $H$.

```figure caption="Geometry of the three means for $a=8$, $b=2$: radius $OD = A = 5$, half-chord $CD = G = 4$, and $DF = H = 3.2$. Visibly $A \ge G \ge H$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9,2.9))
a, b = 8.0, 2.0
A_, B_ = np.array([0,0]), np.array([a+b,0])
O = np.array([(a+b)/2, 0]); C = np.array([a, 0])
G = np.sqrt(a*b); D = np.array([a, G])
th = np.linspace(0, np.pi, 300)
ax.plot(O[0] + (a+b)/2*np.cos(th), (a+b)/2*np.sin(th), color=MUTED, lw=1.2)
ax.plot([0, a+b], [0, 0], color=INK, lw=1.2)
u = (D - O)/np.linalg.norm(D - O)
F = O + np.dot(C - O, u)*u
ax.plot([O[0], D[0]], [O[1], D[1]], color=ACCENT, lw=1.8)
ax.plot([C[0], D[0]], [C[1], D[1]], color='#2e8b57', lw=2.2)
ax.plot([D[0], F[0]], [D[1], F[1]], color='#d9534f', lw=3.4, alpha=0.85)
ax.plot([C[0], F[0]], [C[1], F[1]], color=MUTED, lw=0.9, ls=':')
for P, lab, off in [(A_,'A',(-12,-5)), (C,'C',(-13,3)), (B_,'B',(5,-5)),
                    (O,'O',(-12,3)), (D,'D',(4,3)), (F,'F',(-13,1))]:
    ax.plot([P[0]],[P[1]],'o',color=INK,ms=3.4)
    ax.annotate(lab, P, textcoords='offset points', xytext=off, fontsize=9.2, color=INK)
ax.annotate('$OD = A = 5$', (5.65, 0.55), (0.9, 5.15), color=ACCENT, fontsize=9.3,
            arrowprops=dict(arrowstyle='-', color=ACCENT, lw=0.9))
ax.annotate('$CD = G = 4$', (8.0, 2.0), (9.15, 4.45), color='#2e8b57', fontsize=9.3,
            arrowprops=dict(arrowstyle='-', color='#2e8b57', lw=0.9))
ax.annotate('$DF = H = 3.2$', (7.05, 2.75), (4.55, 5.15), color='#d9534f', fontsize=9.3,
            arrowprops=dict(arrowstyle='-', color='#d9534f', lw=0.9))
ax.annotate('', xy=(0,-0.75), xytext=(8,-0.75),
            arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=0.9, mutation_scale=8))
ax.annotate('', xy=(8,-0.75), xytext=(10,-0.75),
            arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=0.9, mutation_scale=8))
ax.annotate('$a=8$', (4.0,-1.55), color=MUTED, fontsize=9.0, ha='center')
ax.annotate('$b=2$', (9.0,-1.55), color=MUTED, fontsize=9.0, ha='center')
ax.set_xlim(-1.0, 12.6); ax.set_ylim(-2.1, 6.2)
ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 5.6
**Problem.** Insert four arithmetic means between $3$ and $23$, and three
geometric means between $2$ and $32$.

**Solution.** *Arithmetic.* Four means give $4+2 = 6$ terms, so $23$ is the sixth
term:

$$ 23 = 3 + (6-1)d \;\Longrightarrow\; 5d = 20 \;\Longrightarrow\; d = 4 $$

The means are $7,\ 11,\ 15,\ 19$.

*Geometric.* Three means give $5$ terms, so $32$ is the fifth term:

$$ 32 = 2r^{4} \;\Longrightarrow\; r^{4} = 16 \;\Longrightarrow\; r = \pm 2 $$

With $r = 2$ the means are $4,\ 8,\ 16$; with $r = -2$ they are $-4,\ 8,\ -16$.
Both sets are valid geometric means.
:::

::: example Worked example 5.7
**Problem.** The arithmetic mean of two positive numbers is $10$ and their
geometric mean is $8$. Find the numbers and their harmonic mean.

**Solution.** From $A = 10$: $\;a + b = 20$. From $G = 8$: $\;ab = 64$.

Two numbers with known sum and product are the roots of
$x^{2} - (\text{sum})x + (\text{product}) = 0$:

$$ x^{2} - 20x + 64 = 0 \;\Longrightarrow\; (x-4)(x-16) = 0 $$

So the numbers are $4$ and $16$.

$$ H = \frac{2ab}{a+b} = \frac{2(64)}{20} = \frac{32}{5} = 6.4 $$

**Check with $G^{2} = AH$:** $\;AH = 10 \times 6.4 = 64 = 8^{2}$. Correct, and
$10 > 8 > 6.4$ as the inequality requires.
:::

::: example Worked example 5.8
**Problem.** Three numbers in geometric progression have sum $21$ and product
$216$. Find them.

**Solution.** When a *product* is given, choose the terms symmetrically as
$\dfrac{a}{r},\ a,\ ar$ — the $r$ then cancels in the product.

$$ \frac{a}{r}\cdot a \cdot ar = a^{3} = 216 \;\Longrightarrow\; a = 6 $$

Now use the sum:

$$ \frac{6}{r} + 6 + 6r = 21 \;\Longrightarrow\; \frac{1}{r} + r = \frac{21}{6} - 1 = \frac{5}{2} $$

Multiply by $2r$: $\;2 + 2r^{2} = 5r$, i.e. $2r^{2} - 5r + 2 = 0$, so
$(2r-1)(r-2) = 0$ and $r = 2$ or $r = \tfrac12$.

Either way the numbers are $3,\ 6,\ 12$ (in one order or the reverse).
:::

## 5.3 Sum of infinite geometric series

Add more and more terms of a GP and watch $S_n$. For $r = \tfrac12$ and $a = 1$
the partial sums are $1, 1.5, 1.75, 1.875, \ldots$ — climbing, but never reaching
$2$. For $r = 2$ they are $1, 3, 7, 15, \ldots$ — running away. The difference is
entirely the size of $r$.

::: derivation Sum to infinity
Start from the finite sum, written so the $r^{n}$ is isolated:

$$ S_n = \frac{a(1-r^{n})}{1-r} = \frac{a}{1-r} - \frac{a\,r^{n}}{1-r} $$

If $|r| < 1$, repeated multiplication by $r$ shrinks the number towards zero, so
$r^{n} \to 0$ as $n \to \infty$. The second term vanishes and

$$ S_{\infty} = \lim_{n\to\infty} S_n = \frac{a}{1-r}, \qquad |r| < 1 $$

If $|r| \ge 1$ then $r^{n}$ does not tend to zero — the partial sums grow without
limit (or oscillate, when $r \le -1$) and **the series has no sum**.
:::

::: key The convergence condition
$$ S_{\infty} = \frac{a}{1-r} \quad\text{exists if and only if}\quad -1 < r < 1 $$
Always state the condition. Examiners award a mark for it, and a "sum to infinity"
asked about $r = 3$ has the answer *the series does not converge*, not a number.
:::

Why does an endless sum stay finite? Because the terms shrink fast enough that
they can be packed inside a region of finite size. Take $a = \tfrac12$,
$r = \tfrac12$: the terms $\tfrac12, \tfrac14, \tfrac18, \ldots$ tile a unit
square exactly, leaving nothing over.

```figure caption="$\frac{1}{2}+\frac{1}{4}+\frac{1}{8}+\frac{1}{16}+\cdots = 1$. Each term halves the gap that is left, so the pieces fill the unit square without ever overflowing it."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(4.4,2.9))
x0, y0, w, h = 0.0, 0.0, 1.0, 1.0
cols = ['#1d6fb8', '#d9534f', '#2e8b57', '#b8860b', '#6a5acd', '#008b8b']
labels = ['$\\frac{1}{2}$', '$\\frac{1}{4}$', '$\\frac{1}{8}$', '$\\frac{1}{16}$']
vertical = True
for k in range(9):
    if vertical:
        pw, ph = w/2, h
        ax.add_patch(Rectangle((x0, y0), pw, ph, facecolor=cols[k % 6],
                               alpha=0.30, edgecolor=INK, lw=0.8))
        if k < 4:
            ax.text(x0 + pw/2, y0 + ph/2, labels[k], ha='center', va='center',
                    fontsize=10.5 if k < 2 else 8.4, color=INK)
        x0 += pw; w -= pw
    else:
        pw, ph = w, h/2
        ax.add_patch(Rectangle((x0, y0 + h - ph), pw, ph, facecolor=cols[k % 6],
                               alpha=0.30, edgecolor=INK, lw=0.8))
        if k < 4:
            ax.text(x0 + pw/2, y0 + h - ph/2, labels[k], ha='center', va='center',
                    fontsize=8.4, color=INK)
        h -= ph
    vertical = not vertical
ax.add_patch(Rectangle((0,0), 1, 1, facecolor='none', edgecolor=INK, lw=1.4))
ax.annotate('total area $=1$', (0.5, -0.12), ha='center', fontsize=9.2, color=INK)
ax.set_xlim(-0.05, 1.05); ax.set_ylim(-0.22, 1.06)
ax.set_aspect('equal'); ax.axis('off')
```

The same story told with numbers: plot $S_n$ against $n$ and the convergent cases
flatten onto a horizontal line while the divergent case escapes.

```figure caption="Partial sums of $a=1$ with three ratios. For $r=\frac12$, $S_n \to 2$; for $r=-\frac12$, $S_n \to \frac23$, oscillating inwards; for $r=1.5$ the sums diverge."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.9))
n = np.arange(1, 13)
for r, c, lab in [(0.5, ACCENT, '$r=\\frac{1}{2}$'),
                  (-0.5, '#2e8b57', '$r=-\\frac{1}{2}$'),
                  (1.5, '#d9534f', '$r=1.5$')]:
    S = (1 - r**n)/(1 - r)
    ax.plot(n, S, 'o-', color=c, ms=3.8, label=lab)
    if abs(r) < 1:
        ax.axhline(1/(1-r), color=c, lw=0.9, ls='--', alpha=0.75)
ax.annotate('$S_\\infty = 2$', (5.6, 2.30), color=ACCENT, fontsize=9.4)
ax.annotate('$S_\\infty = \\frac{2}{3}$', (5.6, 0.02), color='#2e8b57', fontsize=9.4)
ax.annotate('sums run away', (4.55, 6.4), color='#d9534f', fontsize=9.4)
ax.set_xlabel('number of terms  $n$'); ax.set_ylabel('partial sum  $S_n$')
ax.set_xlim(0.5, 12.5); ax.set_ylim(0, 9)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.5); ax.legend(loc='upper right', ncol=1, handlelength=1.6)
```

::: example Worked example 5.9
**Problem.** Find the sum to infinity of $\;9 - 6 + 4 - \dfrac{8}{3} + \cdots$

**Solution.** The ratio is $r = \dfrac{-6}{9} = -\dfrac{2}{3}$; check it with the
next pair, $\dfrac{4}{-6} = -\dfrac{2}{3}$. Since $|r| = \tfrac23 < 1$ the sum
exists. With $a = 9$,

$$ S_{\infty} = \frac{a}{1-r} = \frac{9}{1-\left(-\frac{2}{3}\right)}
= \frac{9}{\frac{5}{3}} = 9 \times \frac{3}{5} = \frac{27}{5} = 5.4 $$
:::

::: example Worked example 5.10
**Problem.** Express the recurring decimal $0.\overline{45} = 0.454545\ldots$ as a
fraction in lowest terms.

**Solution.** Split the decimal into blocks of two digits:

$$ 0.454545\ldots = \frac{45}{100} + \frac{45}{10\,000} + \frac{45}{1\,000\,000} + \cdots $$

This is a GP with $a = \dfrac{45}{100}$ and $r = \dfrac{1}{100}$, and $|r| < 1$, so

$$ S_{\infty} = \frac{45/100}{1 - 1/100} = \frac{45/100}{99/100} = \frac{45}{99} = \frac{5}{11} $$

Dividing confirms it: $5 \div 11 = 0.4545\ldots$
:::

::: example Worked example 5.11
**Problem.** The sum of an infinite geometric series is $15$ and the sum of the
squares of its terms is $45$. Find the series.

**Solution.** Squaring every term of a GP with ratio $r$ gives a GP with first
term $a^{2}$ and ratio $r^{2}$. So we have two equations:

$$ \frac{a}{1-r} = 15 \qquad (1) \qquad\qquad \frac{a^{2}}{1-r^{2}} = 45 \qquad (2) $$

From (1), $a = 15(1-r)$. Substitute into (2), using $1-r^{2} = (1-r)(1+r)$:

$$ \frac{225(1-r)^{2}}{(1-r)(1+r)} = 45 \;\Longrightarrow\; \frac{225(1-r)}{1+r} = 45 $$

$$ 5(1-r) = 1+r \;\Longrightarrow\; 5 - 5r = 1 + r \;\Longrightarrow\; 6r = 4
\;\Longrightarrow\; r = \frac{2}{3} $$

Then $a = 15\left(1-\tfrac23\right) = 5$. The series is

$$ 5 + \frac{10}{3} + \frac{20}{9} + \frac{40}{27} + \cdots $$

**Check.** Sum of squares $= \dfrac{25}{1-\frac49} = \dfrac{25}{\frac59} = 45$. Correct.
:::

::: caution Sum of squares needs $r^{2}$, not $r$
In the last example the second series has ratio $r^{2}$, so its denominator is
$1 - r^{2}$, not $1-r$. Writing $a^{2}/(1-r)$ is the standard error here.
:::

## Chapter summary

- AP: $t_n = a+(n-1)d$ and $S_n = \frac{n}{2}[2a+(n-1)d] = \frac{n}{2}(a+l)$.
  Three terms are in AP if $2b = a+c$.
- GP: $t_n = ar^{\,n-1}$ and $S_n = \dfrac{a(r^{n}-1)}{r-1} = \dfrac{a(1-r^{n})}{1-r}$
  for $r \ne 1$. Three terms are in GP if $b^{2} = ac$.
- HP: reciprocals form an AP, so $t_n = 1/[a+(n-1)d]$. Invert, solve as an AP,
  invert back. There is no elementary sum formula.
- Means of $a$ and $b$: $A = \dfrac{a+b}{2}$, $G = \sqrt{ab}$,
  $H = \dfrac{2ab}{a+b}$.
- $G^{2} = AH$ (so $A$, $G$, $H$ are in GP) and $A \ge G \ge H$, with equality
  only when $a = b$.
- Inserting $n$ means makes $n+2$ terms: $d = \dfrac{b-a}{n+1}$,
  $r = (b/a)^{1/(n+1)}$.
- Sum to infinity: $S_{\infty} = \dfrac{a}{1-r}$ **if and only if** $|r| < 1$.
- Two given facts about a sequence give two equations: **subtract** them for an AP,
  **divide** them for a GP.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The $10^{\text{th}}$ term of the AP $2, 5, 8, \ldots$ is <span class="marks">[1]</span>
   (a) $27$ (b) $29$ (c) $31$ (d) $32$
2. If the arithmetic mean of two numbers is $9$ and their geometric mean is $6$, their harmonic mean is <span class="marks">[1]</span>
   (a) $3$ (b) $4$ (c) $5$ (d) $7.5$
3. The sum of the infinite series $1 + \frac{1}{3} + \frac{1}{9} + \cdots$ is <span class="marks">[1]</span>
   (a) $\frac{2}{3}$ (b) $\frac{4}{3}$ (c) $\frac{3}{2}$ (d) $2$
4. An infinite geometric series has a finite sum if and only if <span class="marks">[1]</span>
   (a) $r > 1$ (b) $r < 0$ (c) $|r| < 1$ (d) $|r| \ge 1$
5. The harmonic mean between $3$ and $6$ is <span class="marks">[1]</span>
   (a) $4$ (b) $4.5$ (c) $\sqrt{18}$ (d) $9$
6. If $2, x, 8$ are in geometric progression, then $x$ equals <span class="marks">[1]</span>
   (a) $4$ only (b) $5$ (c) $\pm 4$ (d) $\pm 5$

::: note Answers to Group A
**1.** (b) — $t_{10} = 2 + 9(3) = 29$.

**2.** (b) — $G^{2} = AH$ gives $36 = 9H$, so $H = 4$.

**3.** (c) — $a = 1$, $r = \tfrac13$, so $S_{\infty} = 1/(1-\tfrac13) = \tfrac32$.

**4.** (c) — only then does $r^{n} \to 0$.

**5.** (a) — $H = 2(3)(6)/(3+6) = 36/9 = 4$.

**6.** (c) — $x^{2} = 2 \times 8 = 16$, so $x = \pm 4$; both make a valid GP
($2,4,8$ with $r=2$, and $2,-4,8$ with $r=-2$).
:::

**Group B — Short answer (5 marks each)**

1. Derive the formula for the sum of the first $n$ terms of an arithmetic series,
   and hence find the sum of the first $30$ odd natural numbers. <span class="marks">[5]</span>
2. The fourth term of a geometric progression is $24$ and the seventh term is
   $192$. Find the first term, the common ratio and the sum of the first $10$
   terms. <span class="marks">[5]</span>
3. If $a$, $b$, $c$ are in harmonic progression, show that
   $b = \dfrac{2ac}{a+c}$. Hence find the harmonic mean of $4$ and $12$. <span class="marks">[5]</span>
4. Insert four harmonic means between $\dfrac{1}{2}$ and $\dfrac{1}{12}$. <span class="marks">[5]</span>
5. The first term of an infinite geometric series is $3$ and its sum is $4$. Find
   the common ratio and the fourth term. <span class="marks">[5]</span>
6. Express $0.3\overline{7} = 0.3777\ldots$ as a fraction in lowest terms. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Write $S_n = a + (a+d) + \cdots + l$ and again in reverse order; adding the
two lines pairs every term to give $a+l$, and there are $n$ pairs, so
$2S_n = n(a+l)$ and $S_n = \frac{n}{2}(a+l) = \frac{n}{2}[2a+(n-1)d]$.

For the odd numbers $1, 3, 5, \ldots$: $a = 1$, $d = 2$, $n = 30$, so
$S_{30} = 15[2 + 29(2)] = 15(60) = 900$. (Indeed the sum of the first $n$ odd
numbers is always $n^{2} = 30^{2} = 900$.)

**2.** $ar^{3} = 24$ and $ar^{6} = 192$. Dividing, $r^{3} = 8$, so $r = 2$; then
$8a = 24$ gives $a = 3$.

$$ S_{10} = \frac{3(2^{10}-1)}{2-1} = 3(1024-1) = 3069 $$

**3.** $a, b, c$ in HP means $\frac1a, \frac1b, \frac1c$ are in AP, so
$\frac{2}{b} = \frac1a + \frac1c = \frac{a+c}{ac}$. Cross-multiplying gives
$b = \dfrac{2ac}{a+c}$.

For $4$ and $12$: $H = \dfrac{2(4)(12)}{16} = \dfrac{96}{16} = 6$.

**4.** Work with the reciprocals $2$ and $12$. Four means give six terms, so
$12 = 2 + 5d$, i.e. $d = 2$. The AP is $2, 4, 6, 8, 10, 12$, so the four harmonic
means are $\dfrac14,\ \dfrac16,\ \dfrac18,\ \dfrac{1}{10}$.

**5.** $\dfrac{3}{1-r} = 4$ gives $3 = 4 - 4r$, so $r = \dfrac14$ (and
$|r| < 1$, so the sum is legitimate). Fourth term
$= ar^{3} = 3\left(\tfrac14\right)^{3} = \dfrac{3}{64}$.

**6.** Only the $7$ recurs, so separate the non-recurring part:

$$ 0.3777\ldots = \frac{3}{10} + \left(\frac{7}{100} + \frac{7}{1000} + \cdots\right) $$

The bracket is a GP with $a = \frac{7}{100}$, $r = \frac{1}{10}$, summing to
$\dfrac{7/100}{9/10} = \dfrac{7}{90}$. So the value is
$\dfrac{3}{10} + \dfrac{7}{90} = \dfrac{27+7}{90} = \dfrac{34}{90} = \dfrac{17}{45}$.
Check: $17 \div 45 = 0.3777\ldots$
:::

**Group C — Long answer (8 marks each)**

1. (a) Define a geometric progression and derive the formula for the sum of its
   first $n$ terms. <span class="marks">[4]</span>
   (b) The sum of three numbers in geometric progression is $21$ and their product
   is $216$. Find the numbers. <span class="marks">[4]</span>
2. (a) For two positive numbers, prove that $G^{2} = AH$ and that
   $A \ge G \ge H$. <span class="marks">[4]</span>
   (b) The arithmetic mean of two numbers is $\dfrac{25}{4}$ and their harmonic
   mean is $4$. Find the numbers. <span class="marks">[4]</span>
3. (a) State the condition under which an infinite geometric series has a sum, and
   derive the formula for that sum. <span class="marks">[4]</span>
   (b) A ball is dropped from a height of $12\ \text{m}$ and on each bounce rises
   to $\dfrac{2}{3}$ of the previous height. Find the total vertical distance it
   travels before coming to rest. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** (a) See the derivation in §5.1: multiply $S_n$ by $r$, subtract, and the
middle terms cancel to leave $S_n(1-r) = a(1-r^{n})$, so
$S_n = \dfrac{a(1-r^{n})}{1-r}$ for $r \ne 1$.

(b) Take the numbers as $\dfrac{a}{r}, a, ar$. The product gives $a^{3} = 216$,
so $a = 6$. The sum gives $\dfrac6r + 6 + 6r = 21$, i.e.
$r + \dfrac1r = \dfrac52$, so $2r^{2} - 5r + 2 = 0$ and $r = 2$ or $\tfrac12$.
The numbers are $3, 6, 12$.

**2.** (a) $AH = \dfrac{a+b}{2}\cdot\dfrac{2ab}{a+b} = ab = G^{2}$. Next,
$A - G = \dfrac{(\sqrt{a} - \sqrt{b})^{2}}{2} \ge 0$, so $A \ge G$; and
$G - H = G - \dfrac{G^{2}}{A} = \dfrac{G(A-G)}{A} \ge 0$, so $G \ge H$. Equality
throughout only if $a = b$.

(b) $G^{2} = AH = \dfrac{25}{4}\times 4 = 25$, so $ab = 25$. Also
$a+b = 2A = \dfrac{25}{2}$. The numbers are the roots of

$$ x^{2} - \frac{25}{2}x + 25 = 0 \;\Longrightarrow\; 2x^{2} - 25x + 50 = 0 $$

$$ x = \frac{25 \pm \sqrt{625-400}}{4} = \frac{25 \pm 15}{4} = 10 \text{ or } \frac52 $$

So the numbers are $10$ and $2.5$. Check: $A = 12.5/2 = 6.25 = \tfrac{25}{4}$ and
$H = 2(25)/12.5 = 4$. Correct.

**3.** (a) $S_n = \dfrac{a}{1-r} - \dfrac{ar^{n}}{1-r}$. If $|r| < 1$ then
$r^{n} \to 0$ as $n \to \infty$, leaving $S_{\infty} = \dfrac{a}{1-r}$. If
$|r| \ge 1$, $r^{n}$ does not tend to zero and no sum exists.

(b) The ball falls $12\ \text{m}$, then rises and falls $12\left(\tfrac23\right)$,
then rises and falls $12\left(\tfrac23\right)^{2}$, and so on. Total distance

$$ = 12 + 2\left[12\left(\tfrac23\right) + 12\left(\tfrac23\right)^{2} + \cdots\right] $$

The bracket is a GP with $a = 8$, $r = \tfrac23$, so its sum is
$\dfrac{8}{1-\frac23} = 24$. Total distance $= 12 + 2(24) = 60\ \text{m}$.
:::
