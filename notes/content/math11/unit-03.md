---
subject: Mathematics
grade: 11
unit: 3
title: Functions
hours: 7
area: Algebra
---

A function is a rule that turns each input into exactly one output. That one sentence
carries the whole unit: limits, derivatives and integrals in the Calculus area are all
operations *on functions*, so everything later depends on being fluent here. The work
divides into four jobs — say which inputs are allowed (domain) and which outputs occur
(range), chain functions together (composition), undo them (inverse), and recognise the
standard families by their graphs.

::: key What the exam asks for
Group A takes a mark from domain, range or $f^{-1}$. Group B almost always asks either
"find $f \circ g$ and $g \circ f$ and show they are unequal" or "find the inverse of
$\frac{ax+b}{cx+d}$". Group C combines a domain/range question with sketches of the
standard curves. Always state domain and range as **sets or intervals**, never as a
sentence.
:::

## 3.1 Domain and range

::: definition Function
Let $A$ and $B$ be non-empty sets. A **function** $f : A \rightarrow B$ is a rule that
assigns to **each** element $x \in A$ **exactly one** element $f(x) \in B$.

- $A$ is the **domain**, $B$ is the **co-domain**.
- $f(x)$ is the **image** of $x$; $x$ is a **pre-image** of $f(x)$.
- The **range** is the set of images actually attained,
  $f(A) = \{f(x) : x \in A\} \subseteq B$.
:::

Two conditions must hold: every element of $A$ must be used, and none may have two
images. A relation failing either is not a function. On a graph this is the **vertical
line test**: a curve is the graph of a function only if no vertical line meets it more
than once.

::: definition One-one, onto, into
- $f$ is **one-one** (injective) if different inputs give different outputs:
  $f(x_1) = f(x_2) \Rightarrow x_1 = x_2$. Otherwise it is **many-one**.
- $f$ is **onto** (surjective) if the range equals the co-domain, $f(A) = B$. If
  $f(A) \subset B$ (some element of $B$ is left out), $f$ is **into**.
- $f$ is a **bijection** (one-one onto) if it is both. Only a bijection has an inverse.
:::

```figure caption="Mapping (arrow) diagrams. A rule is a function only when every left-hand dot has exactly one arrow leaving it."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
fig, axes = plt.subplots(2, 2, figsize=(5.0,3.4))
def panel(ax, L, R, pairs, title):
    sp = 0.42
    def pos(S, X):
        n = len(S)
        return {e: (X, ((n-1)/2.0 - i) * sp) for i, e in enumerate(S)}
    LP, RP = pos(L, 0.0), pos(R, 1.50)
    ax.add_patch(Ellipse((0.0,0), 0.60, sp*len(L)+0.42, fill=False, ec=MUTED, lw=1.0))
    ax.add_patch(Ellipse((1.50,0), 0.60, sp*len(R)+0.42, fill=False, ec=MUTED, lw=1.0))
    for P, ha, dx in ((LP,'right',-0.16), (RP,'left',0.16)):
        for e,(x,y) in P.items():
            ax.plot([x],[y],'o',color=INK,ms=3.0)
            ax.text(x+dx, y, str(e), fontsize=8.2, color=INK, ha=ha, va='center')
    for a, b in pairs:
        ax.annotate('', xy=RP[b], xytext=LP[a],
                    arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.0,
                                    mutation_scale=8, shrinkA=3, shrinkB=3))
    ax.set_title(title, fontsize=8.6, pad=2)
    ax.set_xlim(-0.62,2.12); ax.set_ylim(-1.18,1.18)
    ax.set_aspect('equal'); ax.axis('off')
panel(axes[0,0], ['1','2','3'], ['a','b','c'],
      [('1','a'),('1','b'),('2','c')], 'not a function\n(1 has two images, 3 has none)')
panel(axes[0,1], ['1','2','3'], ['a','b','c','d'],
      [('1','a'),('2','b'),('3','c')], 'one-one into\n($d$ is not an image)')
panel(axes[1,0], ['1','2','3'], ['a','b'],
      [('1','a'),('2','a'),('3','b')], 'many-one onto\n(1 and 2 share an image)')
panel(axes[1,1], ['1','2','3'], ['a','b','c'],
      [('1','a'),('2','b'),('3','c')], 'one-one onto (bijection)')
fig.tight_layout(h_pad=0.6)
```

### Finding the domain

When a function is given only by a formula, its domain is the largest set of real numbers
for which the formula makes sense. Three rules cover almost every exam question.

::: memory The three domain rules
1. **Never divide by zero.** For $\frac{p(x)}{q(x)}$, exclude the roots of $q(x) = 0$.
2. **Never take an even root of a negative.** For $\sqrt{g(x)}$, require $g(x) \ge 0$.
3. **Never take a logarithm of a non-positive number.** For $\log g(x)$, require
   $g(x) > 0$.

If two rules apply, take the **intersection** of the sets they allow.
:::

```figure caption="Reading domain and range off a graph of $y=\sqrt{9-x^2}$: project the curve onto the $x$-axis to get the domain $[-3,3]$, and onto the $y$-axis to get the range $[0,3]$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,2.9))
x = np.linspace(-3, 3, 500); y = np.sqrt(np.clip(9-x**2, 0, None))
ax.plot(x, y, color=ACCENT, lw=2.0)
ax.plot([-3,3],[0,0], color=SERIES[2], lw=4.0, solid_capstyle='butt', zorder=4)
ax.plot([0,0],[0,3], color=SERIES[1], lw=4.0, solid_capstyle='butt', zorder=4)
for px in (-3,3):
    ax.plot([px,px],[0,np.sqrt(max(9-px**2,0))], color=MUTED, lw=0.8, ls=':')
ax.plot([-3,0],[3,3], color=MUTED, lw=0.8, ls=':')
ax.text(0, -0.55, 'domain  $[-3,\\ 3]$', fontsize=8.8, color=SERIES[2], ha='center')
ax.text(0.18, 1.5, 'range\n$[0,\\ 3]$', fontsize=8.8, color=SERIES[1], va='center')
ax.axhline(0, color=MUTED, lw=0.8); ax.axvline(0, color=MUTED, lw=0.8)
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.set_xlim(-4.2,4.2); ax.set_ylim(-1.0,3.8)
ax.set_xticks([-3,-2,-1,0,1,2,3]); ax.set_yticks([0,1,2,3])
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.4)
```

::: example Worked example 3.1
**Problem.** Which of these are functions from $A = \{1,2,3\}$ to $B = \{4,5,6,7\}$?
(a) $\{(1,4),(2,5),(3,6)\}$ (b) $\{(1,4),(1,5),(2,6),(3,7)\}$ (c) $\{(1,4),(2,4)\}$

**Solution.**

(a) **Yes.** All three elements of $A$ appear once each, with one image apiece. It is
one-one and into (7 is not an image).

(b) **No.** The element $1$ has two images, $4$ and $5$, so the "exactly one" condition
fails.

(c) **No.** The element $3$ has no image, so the "each element" condition fails.
:::

::: example Worked example 3.2
**Problem.** Find the domain and range of (a) $f(x) = \dfrac{1}{x-3}$,
(b) $g(x) = \sqrt{x-2}$.

**Solution.**

**(a)** The denominator vanishes at $x = 3$, so

$$ \text{Domain} = \mathbb{R} - \{3\} = (-\infty,3) \cup (3,\infty) $$

For the range, set $y = \frac{1}{x-3}$ and solve for $x$: $x - 3 = \frac{1}{y}$, so
$x = 3 + \frac{1}{y}$. This is defined for every $y$ except $y = 0$. Hence

$$ \text{Range} = \mathbb{R} - \{0\} $$

(Indeed $\frac{1}{x-3}$ can never equal $0$, since a fraction with numerator $1$ is never
zero.)

**(b)** Need $x - 2 \ge 0$, i.e. $x \ge 2$, so the domain is $[2, \infty)$. As $x$ runs
over $[2,\infty)$, $x-2$ runs over $[0,\infty)$ and its square root runs over
$[0,\infty)$. Range $= [0, \infty)$.
:::

::: example Worked example 3.3
**Problem.** Find the domain and range of $h(x) = \sqrt{9 - x^{2}}$.

**Solution.** **Domain.** Require $9 - x^{2} \ge 0$, i.e. $x^{2} \le 9$, i.e.
$|x| \le 3$:

$$ \text{Domain} = [-3,\ 3] $$

**Range.** On this domain $x^{2}$ takes every value in $[0, 9]$, so $9 - x^2$ takes every
value in $[0, 9]$ and its non-negative square root takes every value in $[0, 3]$:

$$ \text{Range} = [0,\ 3] $$

The graph is the **upper half** of the circle $x^2 + y^2 = 9$ — the lower half is
excluded because $\sqrt{\ }$ is never negative.
:::

::: example Worked example 3.4
**Problem.** Find the range of $f(x) = x^{2} - 4x + 7$, $x \in \mathbb{R}$, and say
whether $f$ is one-one.

**Solution.** Complete the square:

$$ f(x) = (x^{2} - 4x + 4) + 3 = (x-2)^{2} + 3 $$

Since $(x-2)^{2} \ge 0$ for all real $x$, with equality only at $x = 2$,

$$ f(x) \ge 3 \qquad \text{so} \qquad \text{Range} = [3, \infty) $$

$f$ is **not** one-one: for example $f(1) = 1-4+7 = 4$ and $f(3) = 9-12+7 = 4$, so two
different inputs share an image. (The graph is a parabola, and a horizontal line cuts it
twice.)
:::

::: example Worked example 3.5
**Problem.** Find the domain and range of $f(x) = \dfrac{x+1}{x-2}$.

**Solution.** **Domain.** $x - 2 \ne 0$, so domain $= \mathbb{R} - \{2\}$.

**Range.** Put $y = \frac{x+1}{x-2}$ and make $x$ the subject:

$$ y(x-2) = x+1 \;\Rightarrow\; xy - 2y = x + 1 \;\Rightarrow\; x(y-1) = 2y+1 $$
$$ x = \frac{2y+1}{y-1} $$

This gives a valid $x$ for every $y$ except $y = 1$, so

$$ \text{Range} = \mathbb{R} - \{1\} $$

*Sense check:* $\frac{x+1}{x-2} = 1$ would force $x+1 = x-2$, i.e. $1 = -2$, impossible.
:::

::: caution Co-domain is not range
"$f : \mathbb{R} \rightarrow \mathbb{R}$, $f(x) = x^2$" has co-domain $\mathbb{R}$ but
range $[0,\infty)$, so it is **into**, not onto. Change the co-domain to $[0,\infty)$ and
the same rule becomes onto. Whether a function is onto depends on the co-domain you were
given — read the question.
:::

## 3.2 Inverse function; composite function

::: definition Composite function
If $f : A \rightarrow B$ and $g : B \rightarrow C$, the **composite** $g \circ f$ is the
function $A \rightarrow C$ defined by

$$ (g \circ f)(x) = g\!\left(f(x)\right) $$

Apply $f$ **first**, then $g$ — read the symbol from right to left. The domain of
$g \circ f$ is the set of $x$ in the domain of $f$ for which $f(x)$ lies in the domain
of $g$.
:::

```figure caption="Composition of $f(x)=2x$ with $g(x)=x+1$. Following the two arrows in turn gives $(g \circ f)(x) = 2x+1$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
fig, ax = plt.subplots(figsize=(5.0,2.8))
sp = 0.60
sets = [('A', 0.0, ['1','2','3']), ('B', 1.7, ['2','4','6']), ('C', 3.4, ['3','5','7'])]
P = {}
for name, X, els in sets:
    ax.add_patch(Ellipse((X,0), 0.62, sp*len(els)+0.42, fill=False, ec=MUTED, lw=1.0))
    ax.text(X, sp*len(els)/2+0.36, name, fontsize=9.5, color=INK, ha='center', style='italic')
    for i, e in enumerate(els):
        y = ((len(els)-1)/2.0 - i) * sp
        P[(name,e)] = (X, y)
        ax.plot([X],[y],'o',color=INK,ms=3.2)
        ax.text(X, y+0.16, e, fontsize=8.4, color=INK, ha='center')
for a, b in [('1','2'),('2','4'),('3','6')]:
    ax.annotate('', xy=P[('B',b)], xytext=P[('A',a)],
                arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.1,
                                mutation_scale=9, shrinkA=4, shrinkB=4))
for a, b in [('2','3'),('4','5'),('6','7')]:
    ax.annotate('', xy=P[('C',b)], xytext=P[('B',a)],
                arrowprops=dict(arrowstyle='-|>', color=SERIES[2], lw=1.1,
                                mutation_scale=9, shrinkA=4, shrinkB=4))
ax.text(0.85, 0.94, '$f: x \\mapsto 2x$', fontsize=9, color=ACCENT, ha='center')
ax.text(2.55, 0.94, '$g: x \\mapsto x+1$', fontsize=9, color=SERIES[2], ha='center')
ax.annotate('', xy=(3.15,-1.18), xytext=(0.25,-1.18),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.2,
                            mutation_scale=10, connectionstyle='arc3,rad=-0.16'))
ax.text(1.70, -1.62, '$g \\circ f: x \\mapsto 2x+1$', fontsize=9, color=SERIES[1], ha='center')
ax.set_xlim(-0.65,4.05); ax.set_ylim(-1.85,1.45); ax.axis('off')
```

::: caution Composition is not commutative
$f \circ g$ and $g \circ f$ are different functions in general. With $f(x) = 2x+3$ and
$g(x) = x^2$: $(f \circ g)(1) = f(1) = 5$ while $(g \circ f)(1) = g(5) = 25$. Writing
$f \circ g$ when you mean $g \circ f$ loses every mark in the question.
:::

::: example Worked example 3.6
**Problem.** If $f(x) = 2x + 3$ and $g(x) = x^{2}$, find $f \circ g$, $g \circ f$ and
$f \circ f$. Verify that $f \circ g \ne g \circ f$.

**Solution.**

$$ (f \circ g)(x) = f\!\left(g(x)\right) = f(x^{2}) = 2x^{2} + 3 $$
$$ (g \circ f)(x) = g\!\left(f(x)\right) = (2x+3)^{2} = 4x^{2} + 12x + 9 $$
$$ (f \circ f)(x) = f(2x+3) = 2(2x+3) + 3 = 4x + 9 $$

The two composites differ (they are not even the same shape of polynomial), so
$f \circ g \ne g \circ f$. A single value settles it: at $x=1$, $f \circ g$ gives $5$
while $g \circ f$ gives $25$.
:::

::: example Worked example 3.7
**Problem.** If $f(x) = \sqrt{x}$ and $g(x) = x - 4$, find $f \circ g$ and $g \circ f$
together with their domains.

**Solution.**

$(f \circ g)(x) = f(x-4) = \sqrt{x-4}$. This needs $x - 4 \ge 0$, so the domain is
$[4, \infty)$.

$(g \circ f)(x) = g(\sqrt{x}) = \sqrt{x} - 4$. Here $\sqrt{x}$ needs $x \ge 0$, and
subtracting $4$ adds no restriction, so the domain is $[0, \infty)$.

The two composites have different rules **and** different domains.
:::

::: definition Inverse function
If $f : A \rightarrow B$ is a **bijection**, its **inverse** $f^{-1} : B \rightarrow A$ is
the function satisfying

$$ f^{-1}(y) = x \quad \Leftrightarrow \quad f(x) = y $$

so that $f^{-1}\!\left(f(x)\right) = x$ for all $x \in A$ and
$f\!\left(f^{-1}(y)\right) = y$ for all $y \in B$. The domain of $f^{-1}$ is the range of
$f$, and the range of $f^{-1}$ is the domain of $f$.
:::

::: memory Finding an inverse — three steps
1. Write $y = f(x)$.
2. Make $x$ the subject.
3. Interchange the letters: replace $y$ by $x$ to get $f^{-1}(x)$.

Then **check** by computing $f\!\left(f^{-1}(x)\right)$; it must simplify to $x$.
:::

Because $y = f(x)$ and $x = f^{-1}(y)$ describe the same pairs with the coordinates
swapped, the graph of $f^{-1}$ is the **mirror image of the graph of $f$ in the line
$y = x$**.

```figure caption="$f(x) = x^3+1$ and $f^{-1}(x) = \sqrt[3]{x-1}$ are mirror images in the dashed line $y = x$. The point $(1,2)$ on $f$ becomes $(2,1)$ on $f^{-1}$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4,3.2))
def cbrt(t): return np.sign(t)*np.abs(t)**(1/3)
x = np.linspace(-2.2, 2.2, 500)
ax.plot(x, x**3+1, color=ACCENT, lw=1.9, label='$f(x)=x^3+1$')
t = np.linspace(-3.2, 3.2, 500)
ax.plot(t, cbrt(t-1), color=SERIES[1], lw=1.9, label='$f^{-1}(x)=\\sqrt[3]{x-1}$')
ax.plot([-3.2,3.2],[-3.2,3.2], color=MUTED, lw=1.0, ls=(0,(4,3)), label='$y=x$')
for (px,py),c in [((1,2),ACCENT), ((2,1),SERIES[1])]:
    ax.plot([px],[py],'o',color=c,ms=5, zorder=5)
    ax.annotate(f'$({px},{py})$', (px,py), textcoords='offset points',
                xytext=(-34,-4) if px == 1 else (8,-12), fontsize=8.4, color=c)
ax.axhline(0, color=MUTED, lw=0.8); ax.axvline(0, color=MUTED, lw=0.8)
ax.set_xlim(-3.2,3.2); ax.set_ylim(-3.2,3.2); ax.set_aspect('equal')
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.4)
ax.legend(loc='lower right', fontsize=7.8)
```

::: example Worked example 3.8
**Problem.** Find $f^{-1}$ for $f(x) = 3x - 5$ and verify your answer.

**Solution.** Step 1: $y = 3x - 5$. Step 2: $3x = y + 5$, so $x = \frac{y+5}{3}$.
Step 3: interchange letters,

$$ f^{-1}(x) = \frac{x+5}{3} $$

**Check.** $f\!\left(f^{-1}(x)\right) = 3 \cdot \frac{x+5}{3} - 5 = (x+5) - 5 = x$ ✓
and $f^{-1}\!\left(f(x)\right) = \frac{(3x-5)+5}{3} = x$ ✓
:::

::: example Worked example 3.9
**Problem.** If $f(x) = \dfrac{2x+3}{x-1}$, find $f^{-1}(x)$ and state the domain and
range of both $f$ and $f^{-1}$.

**Solution.** Put $y = \frac{2x+3}{x-1}$ and clear the fraction:

$$ y(x-1) = 2x+3 \;\Rightarrow\; xy - y = 2x + 3 $$

Collect the $x$ terms on one side:

$$ xy - 2x = y + 3 \;\Rightarrow\; x(y-2) = y+3 \;\Rightarrow\; x = \frac{y+3}{y-2} $$

Interchanging letters,

$$ f^{-1}(x) = \frac{x+3}{x-2} $$

**Domains and ranges.** $f$ has domain $\mathbb{R} - \{1\}$ and, from the expression for
$x$, range $\mathbb{R} - \{2\}$. These swap for the inverse: $f^{-1}$ has domain
$\mathbb{R}-\{2\}$ and range $\mathbb{R}-\{1\}$.

**Check.** $f(3) = \frac{9}{2}$, and $f^{-1}\!\left(\frac{9}{2}\right) = \frac{9/2+3}{9/2-2} = \frac{15/2}{5/2} = 3$ ✓
:::

::: example Worked example 3.10
**Problem.** Let $f(x) = 2x$ and $g(x) = x+3$. Verify that
$(f \circ g)^{-1} = g^{-1} \circ f^{-1}$.

**Solution.** First the left side. $(f \circ g)(x) = f(x+3) = 2(x+3) = 2x + 6$. Setting
$y = 2x+6$ gives $x = \frac{y-6}{2}$, so

$$ (f \circ g)^{-1}(x) = \frac{x-6}{2} $$

Now the right side. From $y = 2x$, $f^{-1}(x) = \frac{x}{2}$; from $y = x+3$,
$g^{-1}(x) = x - 3$. Hence

$$ \left(g^{-1} \circ f^{-1}\right)(x) = g^{-1}\!\left(\frac{x}{2}\right) = \frac{x}{2} - 3 = \frac{x-6}{2} $$

The two agree, confirming the **reversal law** $(f \circ g)^{-1} = g^{-1} \circ f^{-1}$
(undo the last operation first — like taking off shoes before socks).
:::

## 3.3 Algebraic functions: linear, quadratic, cubic

A **polynomial function** has the form
$f(x) = a_nx^n + a_{n-1}x^{n-1} + \dots + a_1x + a_0$ with real coefficients and
$a_n \ne 0$; $n$ is its **degree**. Its domain is always $\mathbb{R}$. An **algebraic
function** is one built from polynomials by $+, -, \times, \div$ and roots — for example
$\frac{x+1}{x-2}$ and $\sqrt{9-x^2}$.

| Degree | Name | Standard form | Graph | Domain | Range |
|---|---|---|---|---|---|
| $0$ | constant | $y = c$ | horizontal line | $\mathbb{R}$ | $\{c\}$ |
| $1$ | linear | $y = mx + c$ | straight line, slope $m$ | $\mathbb{R}$ | $\mathbb{R}$ |
| $2$ | quadratic | $y = ax^2+bx+c$ | parabola | $\mathbb{R}$ | $[k,\infty)$ or $(-\infty,k]$ |
| $3$ | cubic | $y = ax^3+bx^2+cx+d$ | S-shaped curve | $\mathbb{R}$ | $\mathbb{R}$ |

```figure caption="Linear functions $y = mx+c$. The slope $m$ fixes the direction and $c$ the $y$-intercept; a horizontal line has $m=0$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,2.8))
x = np.linspace(-3, 3, 200)
for m, c, col, ls, lab in [(2,1,ACCENT,'-','$y = 2x+1$'), (-1,3,SERIES[1],'--','$y = -x+3$'),
                           (0,-2,SERIES[2],':','$y = -2$')]:
    ax.plot(x, m*x+c, color=col, lw=1.8, ls=ls, label=lab)
    ax.plot([0],[c],'o',color=col,ms=4.5, zorder=5)
ax.annotate('$y$-intercept $=1$', (0,1), textcoords='offset points', xytext=(10,-16),
            fontsize=8.2, color=ACCENT)
ax.annotate('slope $=2$', (1.6,4.2), textcoords='offset points', xytext=(6,4),
            fontsize=8.2, color=ACCENT)
ax.axhline(0, color=MUTED, lw=0.8); ax.axvline(0, color=MUTED, lw=0.8)
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.set_xlim(-3,3); ax.set_ylim(-5,7)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.4)
ax.legend(loc='upper left', fontsize=8.0)
```

::: key The quadratic $y = ax^{2}+bx+c$
Completing the square gives

$$ y = a\left(x + \frac{b}{2a}\right)^{2} + \left(c - \frac{b^{2}}{4a}\right) $$

- **Vertex** at $x = -\dfrac{b}{2a}$, with $y = c - \dfrac{b^{2}}{4a}$.
- **Axis of symmetry**: the vertical line $x = -\dfrac{b}{2a}$.
- Opens **upward** if $a > 0$ (vertex is a minimum), **downward** if $a < 0$ (maximum).
- $x$-intercepts are the roots of $ax^2+bx+c = 0$; there are two, one or none according as
  the discriminant $b^{2}-4ac$ is positive, zero or negative. The $y$-intercept is $c$.
:::

```figure caption="$y = x^2-4x+3$ (opens up, minimum at $(2,-1)$) and $y = -x^2+2x+3$ (opens down, maximum at $(1,4)$). Roots are the $x$-intercepts."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,3.0))
x = np.linspace(-2.2, 4.6, 500)
ax.plot(x, x**2-4*x+3, color=ACCENT, lw=1.9, label='$y = x^2-4x+3$')
ax.plot(x, -x**2+2*x+3, color=SERIES[1], lw=1.9, ls='--', label='$y = -x^2+2x+3$')
for (px,py),c,lab in [((2,-1),ACCENT,'min $(2,-1)$'), ((1,4),SERIES[1],'max $(1,4)$')]:
    ax.plot([px],[py],'o',color=c,ms=5.5, zorder=6)
    ax.annotate(lab, (px,py), textcoords='offset points',
                xytext=(12,-14 if py<0 else 6), fontsize=8.4, color=c)
for rx, c in [(1,ACCENT),(3,ACCENT),(-1,SERIES[1]),(3,SERIES[1])]:
    ax.plot([rx],[0],'o',color=c,ms=4, zorder=6)
ax.axvline(2, color=ACCENT, lw=0.9, ls=(0,(3,3)))
ax.text(2.08, -4.2, 'axis $x=2$', fontsize=8.0, color=ACCENT)
ax.axhline(0, color=MUTED, lw=0.8); ax.axvline(0, color=MUTED, lw=0.8)
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.set_xlim(-2.2,4.6); ax.set_ylim(-5,6.5)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.4)
ax.legend(loc='upper center', fontsize=8.0, ncol=2)
```

::: example Worked example 3.11
**Problem.** Sketch $y = x^{2} - 4x + 3$, giving the intercepts, vertex, axis of symmetry
and range.

**Solution.**

**Intercepts.** Put $y = 0$: $x^{2}-4x+3 = (x-1)(x-3) = 0$, so the curve crosses the
$x$-axis at $x = 1$ and $x = 3$. Put $x = 0$: $y = 3$.

**Vertex.** Complete the square:

$$ y = (x^{2}-4x+4) - 4 + 3 = (x-2)^{2} - 1 $$

So the vertex is $(2, -1)$ and the axis of symmetry is $x = 2$. (Check with
$x = -\frac{b}{2a} = \frac{4}{2} = 2$, then $y = 4 - 8 + 3 = -1$ ✓.)

**Shape and range.** $a = 1 > 0$, so the parabola opens upward and $(2,-1)$ is a minimum.
Range $= [-1, \infty)$.
:::

::: example Worked example 3.12
**Problem.** For $y = -x^{2} + 2x + 3$, find the roots, the vertex and the maximum value.

**Solution.** **Roots.** $-x^2+2x+3 = 0 \Rightarrow x^2 - 2x - 3 = 0 \Rightarrow (x-3)(x+1) = 0$,
so $x = -1$ and $x = 3$.

**Vertex.** $x = -\frac{b}{2a} = -\frac{2}{2(-1)} = 1$, and
$y = -(1)^2 + 2(1) + 3 = 4$. Vertex $(1, 4)$.

Since $a = -1 < 0$ the parabola opens downward, so $4$ is the **maximum** value and the
range is $(-\infty, 4]$.
:::

```figure caption="The cubic $y = x^3 - 3x$: roots at $0$ and $\pm\sqrt{3}$, a local maximum at $(-1,2)$ and a local minimum at $(1,-2)$. It is symmetric about the origin."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,2.9))
x = np.linspace(-2.3, 2.3, 600)
ax.plot(x, x**3-3*x, color=ACCENT, lw=2.0)
for (px,py),lab,off in [((-1,2),'max $(-1,2)$',(-6,8)), ((1,-2),'min $(1,-2)$',(6,-14))]:
    ax.plot([px],[py],'o',color=SERIES[1],ms=5.5, zorder=6)
    ax.annotate(lab, (px,py), textcoords='offset points', xytext=off,
                fontsize=8.4, color=SERIES[1])
for rx in (-np.sqrt(3), 0.0, np.sqrt(3)):
    ax.plot([rx],[0],'o',color=SERIES[2],ms=4.5, zorder=6)
ax.text(np.sqrt(3)-0.30, 0.50, '$\\sqrt{3}$', fontsize=8.4, color=SERIES[2], ha='center')
ax.text(-np.sqrt(3), -1.15, '$-\\sqrt{3}$', fontsize=8.4, color=SERIES[2], ha='center')
ax.axhline(0, color=MUTED, lw=0.8); ax.axvline(0, color=MUTED, lw=0.8)
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.set_xlim(-2.3,2.3); ax.set_ylim(-4.2,4.2)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.4)
```

::: example Worked example 3.13
**Problem.** Sketch $y = x^{3} - 3x$, stating its intercepts, symmetry and range.

**Solution.** **Intercepts.** $x^3 - 3x = x(x^2-3) = 0$ gives $x = 0, \pm\sqrt{3}$. The
$y$-intercept is $0$.

**Symmetry.** Replacing $x$ by $-x$: $(-x)^3 - 3(-x) = -x^3+3x = -y$. So $f(-x) = -f(x)$,
an **odd** function — the graph is symmetric about the origin.

**Behaviour.** For large positive $x$ the $x^3$ term dominates, so $y \rightarrow \infty$;
for large negative $x$, $y \rightarrow -\infty$. Between them the curve turns twice, at
$(-1, 2)$ and $(1, -2)$ (check: $(-1)^3-3(-1) = -1+3 = 2$, $1 - 3 = -2$).

**Range.** A cubic with non-zero leading coefficient takes every real value, so the range
is $\mathbb{R}$.
:::

## 3.4 Transcendental functions: trigonometric, exponential, logarithmic

A function that is **not** algebraic is called **transcendental**. The three families in
the syllabus are the trigonometric, exponential and logarithmic functions.

### Trigonometric functions

| Function | Domain | Range | Period |
|---|---|---|---|
| $\sin x$ | $\mathbb{R}$ | $[-1, 1]$ | $2\pi$ |
| $\cos x$ | $\mathbb{R}$ | $[-1, 1]$ | $2\pi$ |
| $\tan x$ | $\mathbb{R} - \{(2n+1)\frac{\pi}{2}\}$ | $\mathbb{R}$ | $\pi$ |
| $\csc x$ | $\mathbb{R} - \{n\pi\}$ | $(-\infty,-1] \cup [1,\infty)$ | $2\pi$ |
| $\sec x$ | $\mathbb{R} - \{(2n+1)\frac{\pi}{2}\}$ | $(-\infty,-1] \cup [1,\infty)$ | $2\pi$ |
| $\cot x$ | $\mathbb{R} - \{n\pi\}$ | $\mathbb{R}$ | $\pi$ |

Here $n$ is any integer. Note that $\sin$ and $\cos$ are bounded but $\tan$ is not, and
that $\tan$ repeats twice as fast as $\sin$.

```figure caption="Left: $\sin x$ and $\cos x$, both of period $2\pi$ and range $[-1,1]$. Right: $\tan x$, of period $\pi$, with vertical asymptotes (dashed) at $x = \pm\pi/2$ and $\pm 3\pi/2$."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(5.2,2.6))
ax = axes[0]
x = np.linspace(-2*np.pi, 2*np.pi, 800)
ax.plot(x, np.sin(x), color=ACCENT, lw=1.8, label='$\\sin x$')
ax.plot(x, np.cos(x), color=SERIES[1], lw=1.8, ls='--', label='$\\cos x$')
ax.axhline(1, color=MUTED, lw=0.7, ls=':'); ax.axhline(-1, color=MUTED, lw=0.7, ls=':')
ax.set_xticks([-2*np.pi,-np.pi,0,np.pi,2*np.pi])
ax.set_xticklabels(['$-2\\pi$','$-\\pi$','0','$\\pi$','$2\\pi$'])
ax.set_ylim(-1.7,1.7); ax.set_xlim(-2*np.pi,2*np.pi)
ax.legend(loc='upper center', ncol=2, fontsize=8.0)
ax = axes[1]
for k in (-2,-1,0,1):
    xs = np.linspace(k*np.pi+np.pi/2+0.04, (k+1)*np.pi+np.pi/2-0.04, 300)
    ax.plot(xs, np.tan(xs), color=SERIES[2], lw=1.8)
for a in (-1.5*np.pi, -0.5*np.pi, 0.5*np.pi, 1.5*np.pi):
    ax.axvline(a, color=SERIES[1], lw=1.0, ls=(0,(4,3)))
ax.set_xticks([-1.5*np.pi,-0.5*np.pi,0.5*np.pi,1.5*np.pi])
ax.set_xticklabels(['$-3\\pi/2$','$-\\pi/2$','$\\pi/2$','$3\\pi/2$'])
ax.set_ylim(-5,5); ax.set_xlim(-1.75*np.pi,1.75*np.pi)
ax.set_title('$\\tan x$', fontsize=9.2, pad=3)
for ax in axes:
    ax.axhline(0, color=MUTED, lw=0.8); ax.axvline(0, color=MUTED, lw=0.8)
    ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.35)
fig.tight_layout()
```

### Exponential and logarithmic functions

::: definition Exponential and logarithmic functions
For a fixed base $a > 0$, $a \ne 1$:

- the **exponential function** is $f(x) = a^{x}$, with domain $\mathbb{R}$ and range
  $(0, \infty)$; its graph always passes through $(0, 1)$;
- the **logarithmic function** is $g(x) = \log_a x$, with domain $(0, \infty)$ and range
  $\mathbb{R}$; its graph always passes through $(1, 0)$.

They are inverses of each other: $\log_a(a^{x}) = x$ and $a^{\log_a x} = x$. The natural
base is $e = 2.71828\dots$, and $\log_e x$ is written $\ln x$.
:::

If $a > 1$ both functions are increasing; if $0 < a < 1$ both are decreasing. The
exponential curve has the $x$-axis ($y = 0$) as a horizontal asymptote, and the
logarithmic curve has the $y$-axis ($x = 0$) as a vertical asymptote — exactly what you
expect from reflecting one in $y = x$.

```figure caption="$y = e^x$ and $y = \ln x$ are reflections of each other in $y = x$. The horizontal asymptote $y=0$ of $e^x$ reflects into the vertical asymptote $x=0$ of $\ln x$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4,3.2))
x = np.linspace(-3.0, 1.6, 400)
ax.plot(x, np.exp(x), color=ACCENT, lw=1.9, label='$y = e^{x}$')
t = np.linspace(0.045, 4.6, 500)
ax.plot(t, np.log(t), color=SERIES[1], lw=1.9, label='$y = \\ln x$')
ax.plot([-3,4.6],[-3,4.6], color=MUTED, lw=1.0, ls=(0,(4,3)), label='$y = x$')
ax.axhline(0, color=ACCENT, lw=1.0, ls=(0,(2,2)))
ax.axvline(0, color=SERIES[1], lw=1.0, ls=(0,(2,2)))
for (px,py),c in [((0,1),ACCENT),((1,0),SERIES[1])]:
    ax.plot([px],[py],'o',color=c,ms=5, zorder=6)
    ax.annotate(f'$({px},{py})$', (px,py), textcoords='offset points',
                xytext=(7,-11), fontsize=8.2, color=c)
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.set_xlim(-3.0,4.6); ax.set_ylim(-3.0,4.6); ax.set_aspect('equal')
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.4)
ax.legend(loc='lower right', fontsize=8.0)
```

::: key Laws of indices and logarithms
For $a, b > 0$ with $a, b \ne 1$, and $m, n > 0$:

$$ a^{x} \cdot a^{y} = a^{x+y}, \qquad \frac{a^{x}}{a^{y}} = a^{x-y}, \qquad (a^{x})^{y} = a^{xy}, \qquad a^{0} = 1 $$
$$ \log_a(mn) = \log_a m + \log_a n, \qquad \log_a\!\left(\frac{m}{n}\right) = \log_a m - \log_a n $$
$$ \log_a(m^{k}) = k\log_a m, \qquad \log_a a = 1, \qquad \log_a 1 = 0 $$
$$ \text{change of base:} \quad \log_a m = \frac{\log_b m}{\log_b a} $$
:::

::: example Worked example 3.14
**Problem.** Find the domain of (a) $f(x) = \log(x^{2} - 5x + 6)$, and
(b) $g(x) = \ln(x-1) + \sqrt{4-x}$.

**Solution.**

**(a)** Require $x^{2} - 5x + 6 > 0$, i.e. $(x-2)(x-3) > 0$. A product of two factors is
positive when both are positive or both are negative:

- both positive: $x > 3$;
- both negative: $x < 2$.

Domain $= (-\infty, 2) \cup (3, \infty)$.

**(b)** Two conditions must hold **together**: $x - 1 > 0$ gives $x > 1$, and
$4 - x \ge 0$ gives $x \le 4$. Intersecting,

$$ \text{Domain} = (1,\ 4] $$
:::

::: example Worked example 3.15
**Problem.** Solve (a) $2^{x+1} = 8^{x-1}$, (b) $\log_2 x + \log_2(x-2) = 3$.

**Solution.**

**(a)** Write both sides to the same base: $8 = 2^{3}$, so
$8^{x-1} = 2^{3(x-1)}$. Equal powers of the same base force equal exponents:

$$ x + 1 = 3(x-1) = 3x - 3 \;\Rightarrow\; 4 = 2x \;\Rightarrow\; x = 2 $$

*Check:* $2^{3} = 8$ and $8^{1} = 8$ ✓

**(b)** Combine the logarithms with $\log m + \log n = \log(mn)$:

$$ \log_2\!\left(x(x-2)\right) = 3 \;\Rightarrow\; x(x-2) = 2^{3} = 8 $$
$$ x^{2} - 2x - 8 = 0 \;\Rightarrow\; (x-4)(x+2) = 0 \;\Rightarrow\; x = 4 \text{ or } x = -2 $$

**Reject $x = -2$**: the original expression needs $x > 0$ and $x - 2 > 0$, i.e. $x > 2$.
So $x = 4$. *Check:* $\log_2 4 + \log_2 2 = 2 + 1 = 3$ ✓
:::

::: caution Always check logarithmic solutions
Combining logarithms **widens** the domain, so an algebraically correct root can be
invalid for the original equation. After solving, substitute back and discard any root
that makes an argument zero or negative.
:::

::: example Worked example 3.16
**Problem.** State the domain, range and period of $y = 3\sin 2x$, and the value of $x$
in $[0, \pi]$ at which it first attains its maximum.

**Solution.** The domain is $\mathbb{R}$, since $\sin$ accepts any real input.

Since $-1 \le \sin 2x \le 1$, multiplying by $3$ gives $-3 \le 3\sin 2x \le 3$, so the
range is $[-3, 3]$; the **amplitude** is $3$.

The period of $\sin bx$ is $\frac{2\pi}{|b|}$, so here it is $\frac{2\pi}{2} = \pi$.

The maximum occurs when $\sin 2x = 1$, i.e. $2x = \frac{\pi}{2}$, so
$x = \frac{\pi}{4}$.
:::

## Chapter summary

- $f : A \rightarrow B$ assigns exactly one image to each element of $A$; the range
  $f(A)$ may be a proper subset of the co-domain $B$.
- One-one means distinct inputs have distinct images; onto means range $=$ co-domain;
  a bijection is both, and only a bijection is invertible.
- Domain rules: no division by zero, no even root of a negative, no log of a non-positive
  number; take the intersection when several apply.
- $(g \circ f)(x) = g(f(x))$ — apply $f$ first. In general $f \circ g \ne g \circ f$, and
  $(f \circ g)^{-1} = g^{-1} \circ f^{-1}$.
- To invert: write $y = f(x)$, make $x$ the subject, swap letters. Domain and range swap,
  and the graph of $f^{-1}$ is the reflection of that of $f$ in $y = x$.
- Quadratic $y = ax^2+bx+c$: vertex at $x = -\frac{b}{2a}$, opens up if $a>0$; the number
  of $x$-intercepts is decided by $b^2-4ac$.
- $\sin x, \cos x$: domain $\mathbb{R}$, range $[-1,1]$, period $2\pi$; $\tan x$: range
  $\mathbb{R}$, period $\pi$.
- $a^x$: domain $\mathbb{R}$, range $(0,\infty)$, through $(0,1)$. $\log_a x$: domain
  $(0,\infty)$, range $\mathbb{R}$, through $(1,0)$. They are mutual inverses.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The domain of $f(x) = \dfrac{1}{x^{2}-4}$ is <span class="marks">[1]</span>
   (a) $\mathbb{R}$ (b) $\mathbb{R} - \{2\}$ (c) $\mathbb{R} - \{-2, 2\}$ (d) $[-2,2]$
2. The range of $f(x) = x^{2} + 1$, $x \in \mathbb{R}$, is <span class="marks">[1]</span>
   (a) $\mathbb{R}$ (b) $[1, \infty)$ (c) $(1, \infty)$ (d) $[0, \infty)$
3. If $f(x) = 2x+1$ and $g(x) = x^{2}$, then $(g \circ f)(2)$ is <span class="marks">[1]</span>
   (a) $9$ (b) $25$ (c) $11$ (d) $5$
4. If $f(x) = 5x - 2$, then $f^{-1}(x)$ is <span class="marks">[1]</span>
   (a) $\frac{x-2}{5}$ (b) $\frac{x+2}{5}$ (c) $\frac{1}{5x-2}$ (d) $5x+2$
5. The period of $y = 2\cos 3x$ is <span class="marks">[1]</span>
   (a) $2\pi$ (b) $\frac{2\pi}{3}$ (c) $3\pi$ (d) $\pi$
6. The domain of $y = \ln(x - 4)$ is <span class="marks">[1]</span>
   (a) $[4, \infty)$ (b) $(4, \infty)$ (c) $(-\infty, 4)$ (d) $\mathbb{R} - \{4\}$
7. The graph of $f^{-1}$ is obtained from that of $f$ by reflecting in <span class="marks">[1]</span>
   (a) the $x$-axis (b) the $y$-axis (c) the line $y = x$ (d) the origin

::: note Answers to Group A
**1.** (c) — the denominator vanishes at $x = \pm 2$, and both must be excluded.

**2.** (b) — $x^2 \ge 0$, so $x^2+1 \ge 1$, and the value $1$ is attained at $x = 0$.

**3.** (b) — $f(2) = 5$, then $g(5) = 25$. (Applying $g$ first would give $9$, the wrong order.)

**4.** (b) — from $y = 5x-2$, $x = \frac{y+2}{5}$.

**5.** (b) — period of $\cos bx$ is $\frac{2\pi}{|b|} = \frac{2\pi}{3}$; the amplitude $2$ does not affect it.

**6.** (b) — need $x-4 > 0$; $\ln 0$ is undefined, so $4$ itself is excluded.

**7.** (c) — swapping $x$ and $y$ reflects a point in the line $y = x$.
:::

**Group B — Short answer (5 marks each)**

1. Define domain, co-domain and range of a function. Find the domain and range of
   $f(x) = \dfrac{1}{x-3}$ and of $g(x) = \sqrt{16 - x^{2}}$. <span class="marks">[5]</span>
2. If $f(x) = 3x - 2$ and $g(x) = x^{2}+1$, find $f \circ g$, $g \circ f$ and
   $(f \circ g)(2)$, and show that $f \circ g \ne g \circ f$. <span class="marks">[5]</span>
3. Find the inverse of $f(x) = \dfrac{3x+1}{x-2}$, stating its domain and range, and
   verify that $f\!\left(f^{-1}(x)\right) = x$. <span class="marks">[5]</span>
4. Sketch $y = x^{2} - 6x + 5$, showing the intercepts, the vertex, the axis of symmetry
   and the range. <span class="marks">[5]</span>
5. Find the domain of $f(x) = \sqrt{x+2} + \log(5 - x)$. <span class="marks">[5]</span>
6. State the amplitude, period and range of $y = 4\sin\frac{x}{2}$, and sketch one
   complete cycle. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** The **domain** is the set of allowed inputs; the **co-domain** is the set the
outputs are declared to lie in; the **range** is the set of outputs actually attained,
always a subset of the co-domain.

$f(x) = \frac{1}{x-3}$: denominator zero at $x=3$, so domain $= \mathbb{R}-\{3\}$. Setting
$y = \frac{1}{x-3}$ gives $x = 3 + \frac{1}{y}$, valid for all $y \ne 0$, so range
$= \mathbb{R}-\{0\}$.

$g(x) = \sqrt{16-x^2}$: need $16 - x^2 \ge 0$, i.e. $|x| \le 4$, so domain $= [-4,4]$. On
that interval $16-x^2$ ranges over $[0,16]$, so $g$ ranges over $[0,4]$.

**2.** $(f \circ g)(x) = f(x^2+1) = 3(x^2+1) - 2 = 3x^2 + 1$.

$(g \circ f)(x) = g(3x-2) = (3x-2)^2 + 1 = 9x^2 - 12x + 5$.

$(f \circ g)(2) = 3(4) + 1 = 13$. (Check directly: $g(2) = 5$, $f(5) = 13$ ✓)

They are different — for instance $(g \circ f)(2) = 9(4)-24+5 = 17 \ne 13$. Hence
$f \circ g \ne g \circ f$.

**3.** Put $y = \frac{3x+1}{x-2}$. Then $y(x-2) = 3x+1$, so $xy - 2y = 3x + 1$ and
$x(y-3) = 2y+1$, giving $x = \frac{2y+1}{y-3}$. Hence

$$ f^{-1}(x) = \frac{2x+1}{x-3} $$

$f$ has domain $\mathbb{R}-\{2\}$ and range $\mathbb{R}-\{3\}$, so $f^{-1}$ has domain
$\mathbb{R}-\{3\}$ and range $\mathbb{R}-\{2\}$.

*Verification.*

$$ f\!\left(f^{-1}(x)\right) = \frac{3 \cdot \frac{2x+1}{x-3} + 1}{\frac{2x+1}{x-3} - 2} = \frac{\frac{6x+3+x-3}{x-3}}{\frac{2x+1-2x+6}{x-3}} = \frac{7x}{7} = x $$

**4.** $y = x^2-6x+5 = (x-1)(x-5)$, so the $x$-intercepts are $1$ and $5$; the
$y$-intercept is $5$.

Completing the square, $y = (x-3)^2 - 4$, so the vertex is $(3,-4)$ and the axis of
symmetry is $x = 3$. Since $a = 1 > 0$ the parabola opens upward, the minimum value is
$-4$, and the range is $[-4, \infty)$. The sketch is a U through $(1,0)$, $(5,0)$,
$(0,5)$ with its lowest point at $(3,-4)$.

**5.** Two conditions: $x + 2 \ge 0$ gives $x \ge -2$, and $5 - x > 0$ gives $x < 5$.
Intersecting,

$$ \text{Domain} = [-2,\ 5) $$

**6.** For $y = a\sin bx$ with $a = 4$ and $b = \frac{1}{2}$:

amplitude $= |a| = 4$; period $= \frac{2\pi}{|b|} = \frac{2\pi}{1/2} = 4\pi$;
range $= [-4, 4]$.

One complete cycle runs from $x = 0$ to $x = 4\pi$: it starts at $0$, rises to the maximum
$4$ at $x = \pi$, returns to $0$ at $x = 2\pi$, falls to the minimum $-4$ at $x = 3\pi$
and comes back to $0$ at $x = 4\pi$.
:::

**Group C — Long answer (8 marks each)**

1. (a) Define one-one, onto and bijective functions, illustrating each with an arrow
   diagram. <span class="marks">[3]</span>
   (b) If $f(x) = \dfrac{x+2}{x-1}$, find $f^{-1}(x)$, state the domain and range of $f$
   and $f^{-1}$, and verify $f^{-1}\!\left(f(x)\right) = x$. <span class="marks">[5]</span>
2. (a) Sketch, on the same axes, $y = e^{x}$ and $y = \ln x$, marking the asymptotes,
   the points $(0,1)$ and $(1,0)$, and the line of symmetry. State the domain and range
   of each. <span class="marks">[4]</span>
   (b) Solve $\log_3(x+6) + \log_3(x-2) = 2$. <span class="marks">[4]</span>

::: note Answers to Group C
**1. (a)** A function $f: A \rightarrow B$ is:

- **one-one (injective)** if $f(x_1) = f(x_2)$ forces $x_1 = x_2$ — in an arrow diagram,
  no two arrows land on the same dot;
- **onto (surjective)** if every element of $B$ is an image — no dot in $B$ is left
  without an arrow;
- **bijective** if both hold — the arrows pair up the two sets exactly, one to one.

For example $f(x) = 2x+1$ on $\mathbb{R}$ is bijective; $f(x) = x^2$ on $\mathbb{R}$ is
neither (many-one, and into since negatives are never attained).

**1. (b)** Put $y = \frac{x+2}{x-1}$. Then $y(x-1) = x+2$, so $xy - y = x + 2$ and
$x(y-1) = y+2$, giving $x = \frac{y+2}{y-1}$. Interchanging letters,

$$ f^{-1}(x) = \frac{x+2}{x-1} $$

so this $f$ is its own inverse (a *self-inverse* or involution). Its domain is
$\mathbb{R}-\{1\}$ and its range is $\mathbb{R}-\{1\}$; the same pair serves for
$f^{-1}$.

*Verification.*

$$ f^{-1}\!\left(f(x)\right) = \frac{\frac{x+2}{x-1} + 2}{\frac{x+2}{x-1} - 1} = \frac{\frac{x+2+2x-2}{x-1}}{\frac{x+2-x+1}{x-1}} = \frac{3x}{3} = x $$

**2. (a)** $y = e^{x}$ is increasing, passes through $(0,1)$, lies entirely above the
$x$-axis and approaches the horizontal asymptote $y = 0$ as $x \rightarrow -\infty$; its
domain is $\mathbb{R}$ and range $(0,\infty)$.

$y = \ln x$ is increasing, passes through $(1,0)$, exists only for $x > 0$ and approaches
the vertical asymptote $x = 0$ as $x \rightarrow 0^{+}$; its domain is $(0,\infty)$ and
range $\mathbb{R}$.

The two curves are reflections of each other in the line $y = x$, which is therefore the
line of symmetry of the pair. (See the figure in section 3.4.)

**2. (b)** Combine the logarithms:

$$ \log_3\!\left((x+6)(x-2)\right) = 2 \;\Rightarrow\; (x+6)(x-2) = 3^{2} = 9 $$
$$ x^{2} + 4x - 12 = 9 \;\Rightarrow\; x^{2} + 4x - 21 = 0 \;\Rightarrow\; (x+7)(x-3) = 0 $$

So $x = -7$ or $x = 3$. The original equation needs $x + 6 > 0$ and $x - 2 > 0$, i.e.
$x > 2$, so **reject $x = -7$**.

$x = 3$. *Check:* $\log_3 9 + \log_3 1 = 2 + 0 = 2$ ✓
:::
