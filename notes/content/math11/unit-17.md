---
subject: Mathematics
grade: 11
unit: 17
title: Limits and Continuity
hours: 10
area: Calculus
---

Calculus begins with one question: what happens to $f(x)$ when $x$ gets very close
to a number $a$, without ever being equal to it? The answer is the **limit**. From
it come the derivative (Unit 18) and the integral (Unit 19), so nothing later in
the course works until this idea is secure. This chapter builds the limit from an
intuitive table of values up to the formal $\varepsilon$–$\delta$ statement, lists
the standard limits you must know by heart, shows how to break every indeterminate
form, and ends with continuity — the property that a graph can be drawn without
lifting the pen.

::: key What the examiner asks from this unit
Group A almost always carries one or two limit evaluations and one continuity
question. Group B favours (i) evaluating a $0/0$ limit by factorisation or
rationalisation, (ii) a trigonometric or exponential limit built on a standard
result, and (iii) "find the value of $k$ so that $f$ is continuous at $x = a$".
Memorise the standard limits in §17.1 — half the marks in this unit come straight
off that list.
:::

## 17.1 Concept of limit; limits of algebraic and transcendental functions

### The idea of approaching

Consider

$$ f(x) = \frac{x^{2}-4}{x-2} $$

At $x = 2$ the formula gives $0/0$, which is meaningless, so $f(2)$ does not
exist. But that is not the question. The question is: what does $f(x)$ do as $x$
*approaches* 2?

| $x$ | 1.9 | 1.99 | 1.999 | 2 | 2.001 | 2.01 | 2.1 |
|---|---|---|---|---|---|---|---|
| $f(x)$ | 3.9 | 3.99 | 3.999 | undefined | 4.001 | 4.01 | 4.1 |

From both sides the values crowd in on 4. We write

$$ \lim_{x \to 2}\frac{x^{2}-4}{x-2} = 4 $$

and read it "the limit of $f(x)$ as $x$ tends to 2 is 4". Nothing here depends on
$f(2)$. Indeed for every $x \ne 2$ we may cancel:

$$ \frac{x^{2}-4}{x-2} = \frac{(x-2)(x+2)}{x-2} = x+2 $$

and $x+2 \to 4$. The cancellation is legal **precisely because** $x \ne 2$ in a
limit.

```figure caption="The graph of $f(x)=(x^2-4)/(x-2)$ is the line $y=x+2$ with the single point $x=2$ punched out. The limit at $x=2$ is 4 even though $f(2)$ does not exist."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,2.9))
xl = np.linspace(-0.4, 1.985, 300); xr = np.linspace(2.015, 4.4, 300)
ax.plot(xl, xl+2, color=ACCENT, lw=2)
ax.plot(xr, xr+2, color=ACCENT, lw=2)
ax.plot([2],[4], marker='o', ms=7, mfc='white', mec=ACCENT, mew=1.8, zorder=5)
ax.hlines(4, -0.4, 2, color=MUTED, lw=.9, ls=':')
ax.vlines(2, 0, 4, color=MUTED, lw=.9, ls=':')
for x0, dx in [(1.35, 0.35), (2.75, -0.35)]:
    ax.annotate('', xy=(x0+dx, x0+dx+2), xytext=(x0, x0+2),
                arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.5, mutation_scale=12))
ax.annotate('limit $=4$', (2,4), textcoords='offset points', xytext=(10,-6),
            color=INK, fontsize=9.5)
ax.annotate('$f(2)$ undefined', (2,4), textcoords='offset points', xytext=(-104,18),
            color=MUTED, fontsize=9,
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=.9, mutation_scale=9))
ax.set_xlabel('$x$'); ax.set_ylabel('$f(x)$')
ax.set_xlim(-0.4,4.4); ax.set_ylim(0,7)
ax.set_xticks([0,1,2,3,4]); ax.set_yticks([0,2,4,6])
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.45)
```

::: definition Limit (working definition)
A number $L$ is the limit of $f(x)$ as $x$ tends to $a$, written
$\lim_{x \to a} f(x) = L$, if $f(x)$ can be made as close to $L$ as we please by
taking $x$ sufficiently close to $a$ but **not equal to** $a$.
:::

### Left-hand and right-hand limits

On the real line $x$ can approach $a$ from two directions. Approaching through
values **less than** $a$ gives the **left-hand limit** (LHL), approaching through
values **greater than** $a$ gives the **right-hand limit** (RHL):

$$ \text{LHL} = \lim_{x \to a^{-}} f(x) = \lim_{h \to 0}f(a-h), \qquad
\text{RHL} = \lim_{x \to a^{+}} f(x) = \lim_{h \to 0}f(a+h) \qquad (h>0) $$

Rewriting one-sided limits with a positive $h$ in this way is the standard NEB
technique: it turns a one-sided limit into an ordinary limit.

::: key Existence of a limit
$\lim_{x \to a} f(x)$ exists **if and only if** the left-hand and right-hand
limits both exist, are finite, and are equal:

$$ \lim_{x \to a^{-}} f(x) = \lim_{x \to a^{+}} f(x) = L
\;\Longleftrightarrow\; \lim_{x \to a} f(x) = L $$

If they differ, the limit simply does not exist. It is *not* "two limits".
:::

```figure caption="A jump: the left-hand limit at $x=2$ is 1 and the right-hand limit is 4. Because $1 \ne 4$, $\lim_{x\to2}f(x)$ does not exist."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,3.0))
xl = np.linspace(-0.3, 2, 300); xr = np.linspace(2, 4.3, 300)
ax.plot(xl, 0.5*xl, color=ACCENT, lw=2, label='$f(x)=x/2,\\ x<2$')
ax.plot(xr, xr+2, color='#2e8b57', lw=2, label='$f(x)=x+2,\\ x>2$')
ax.plot([2],[1], marker='o', ms=7, mfc='white', mec=ACCENT, mew=1.8, zorder=5)
ax.plot([2],[4], marker='o', ms=7, mfc='white', mec='#2e8b57', mew=1.8, zorder=5)
ax.plot([2],[2.6], marker='o', ms=6, color='#d9534f', zorder=6)
ax.annotate('$f(2)=2.6$', (2,2.6), textcoords='offset points', xytext=(9,-4),
            color='#d9534f', fontsize=9)
ax.hlines(1, -0.3, 2, color=MUTED, lw=.9, ls=':')
ax.hlines(4, 2, 4.3, color=MUTED, lw=.9, ls=':')
ax.annotate('LHL = 1', (0.2,1), textcoords='offset points', xytext=(2,7), color=INK, fontsize=9.3)
ax.annotate('RHL = 4', (3.4,4), textcoords='offset points', xytext=(-6,-16), color=INK, fontsize=9.3)
ax.annotate('', xy=(1.92,0.96), xytext=(1.3,0.65),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.3, mutation_scale=11))
ax.annotate('', xy=(2.08,4.08), xytext=(2.75,4.75),
            arrowprops=dict(arrowstyle='-|>', color='#2e8b57', lw=1.3, mutation_scale=11))
ax.vlines(2, 0, 4.3, color=GRID, lw=1.0)
ax.set_xlabel('$x$'); ax.set_ylabel('$f(x)$')
ax.set_xlim(-0.3,4.4); ax.set_ylim(0,7)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.4)
ax.legend(loc='upper left', fontsize=8.4)
```

::: example Worked example 17.1 — a one-sided pair
**Problem.** Show that $\lim_{x \to 2}\dfrac{|x-2|}{x-2}$ does not exist.

**Solution.** Recall $|u| = u$ if $u \ge 0$ and $|u| = -u$ if $u < 0$.

*Left-hand limit.* Put $x = 2-h$ with $h > 0$. Then $x - 2 = -h < 0$, so
$|x-2| = h$ and

$$ \lim_{x\to2^{-}}\frac{|x-2|}{x-2} = \lim_{h\to0}\frac{h}{-h} = -1 $$

*Right-hand limit.* Put $x = 2+h$ with $h > 0$. Then $x-2 = h > 0$, so
$|x-2| = h$ and

$$ \lim_{x\to2^{+}}\frac{|x-2|}{x-2} = \lim_{h\to0}\frac{h}{h} = +1 $$

Since $-1 \ne 1$, the two one-sided limits disagree and the limit does not exist.
:::

### The precise ($\varepsilon$–$\delta$) definition

"As close as we please" is made exact by two Greek letters. $\varepsilon$
(epsilon) is the tolerance demanded on the output; $\delta$ (delta) is the
closeness we must impose on the input to meet it.

::: definition Formal definition of a limit
$\lim_{x \to a} f(x) = L$ means: for every $\varepsilon > 0$ there exists a
$\delta > 0$ such that

$$ 0 < |x-a| < \delta \;\Longrightarrow\; |f(x)-L| < \varepsilon $$

The condition $0 < |x-a|$ excludes $x = a$ itself — again, the value $f(a)$ is
irrelevant.
:::

Geometrically: draw a horizontal band of half-width $\varepsilon$ about $y = L$.
The definition says we can always find a vertical band of half-width $\delta$
about $x = a$ so narrow that the piece of curve inside it stays trapped in the
horizontal band.

```figure caption="The $\varepsilon$–$\delta$ picture. Given the $\varepsilon$-band about $L$, a $\delta$-band about $a$ exists whose graph lies entirely inside it."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,3.1))
f = lambda z: 0.35*z**2 + 0.6
a = 2.0; L = f(a)
x = np.linspace(0.2, 3.6, 500)
eps = 0.55
# delta must work on BOTH sides: take the smaller of the two half-widths
dr = np.sqrt((L+eps-0.6)/0.35) - a
dl = a - np.sqrt((L-eps-0.6)/0.35)
d = min(dl, dr)
ax.axhspan(L-eps, L+eps, color='#d9534f', alpha=0.10)
ax.axvspan(a-d, a+d, color=ACCENT, alpha=0.14)
ax.plot(x, f(x), color=MUTED, lw=1.4, zorder=3)
xin = np.linspace(a-d, a+d, 200)
ax.plot(xin, f(xin), color=ACCENT, lw=2.6, zorder=4)
ax.hlines([L-eps, L+eps], 0.2, 3.6, color='#d9534f', lw=1.0, ls='--')
ax.vlines([a-d, a+d], 0, 5.4, color=ACCENT, lw=1.0, ls='--')
ax.plot([a],[L], 'o', color=INK, ms=5, zorder=6)
ax.annotate('graph inside the $\\delta$-band\nstays inside the $\\epsilon$-band',
            (a+d, f(a+d)), textcoords='offset points', xytext=(12,28),
            fontsize=8.6, color=INK,
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=.9, mutation_scale=9))
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.set_xlim(0.2,3.6); ax.set_ylim(0,5.4)
ax.set_xticks([a-d, a, a+d])
ax.set_xticklabels(['$a-\\delta$', '$a$', '$a+\\delta$'])
ax.set_yticks([L-eps, L, L+eps])
ax.set_yticklabels(['$L-\\epsilon$', '$L$', '$L+\\epsilon$'])
ax.spines[['top','right']].set_visible(False)
```

::: example Worked example 17.2 — an $\varepsilon$–$\delta$ proof
**Problem.** Using the $\varepsilon$–$\delta$ definition, prove
$\lim_{x \to 3}(2x+1) = 7$.

**Solution.** Let $\varepsilon > 0$ be given. We need $|(2x+1)-7| < \varepsilon$.

$$ |(2x+1)-7| = |2x-6| = 2|x-3| $$

So $|(2x+1)-7| < \varepsilon$ is the same as $|x-3| < \varepsilon/2$.

Choose $\delta = \varepsilon/2$. Then whenever $0 < |x-3| < \delta$,

$$ |(2x+1)-7| = 2|x-3| < 2\delta = \varepsilon $$

Since a suitable $\delta$ exists for every $\varepsilon > 0$, the limit is 7.
:::

### Algebra of limits

If $\lim_{x\to a}f(x) = L$ and $\lim_{x\to a}g(x) = M$ (both finite), then:

| Rule | Statement |
|---|---|
| Sum / difference | $\lim (f \pm g) = L \pm M$ |
| Constant multiple | $\lim\, cf = cL$ |
| Product | $\lim (fg) = LM$ |
| Quotient | $\lim (f/g) = L/M$, provided $M \ne 0$ |
| Power | $\lim [f(x)]^{n} = L^{n}$ |
| Root | $\lim \sqrt[n]{f(x)} = \sqrt[n]{L}$, when the root is defined |
| Composite | $\lim g(f(x)) = g(L)$ if $g$ is continuous at $L$ |

For a **polynomial** $P$, direct substitution always works: $\lim_{x\to a}P(x) = P(a)$.
For a **rational** function $P/Q$, substitution works whenever $Q(a) \ne 0$. Only
when substitution produces a meaningless symbol do we need the machinery of §17.2.

### Limits of algebraic functions

The workhorse result is:

::: derivation The standard algebraic limit
For any rational index $n$ and $a > 0$,

$$ \lim_{x \to a}\frac{x^{n}-a^{n}}{x-a} = n\,a^{n-1} $$

**Proof for positive integer $n$.** Use the identity

$$ x^{n}-a^{n} = (x-a)\left(x^{n-1}+x^{n-2}a+x^{n-3}a^{2}+\cdots+a^{n-1}\right) $$

There are exactly $n$ terms in the second bracket. Cancelling $(x-a)$, which is
allowed since $x \ne a$,

$$ \frac{x^{n}-a^{n}}{x-a} = x^{n-1}+x^{n-2}a+\cdots+a^{n-1} $$

Now let $x \to a$. Each of the $n$ terms tends to $a^{n-1}$, so the sum tends to
$n\,a^{n-1}$.
:::

::: example Worked example 17.3 — using the standard form
**Problem.** Evaluate $\displaystyle\lim_{x\to1}\frac{x^{5}-1}{x^{2}-1}$.

**Solution.** Direct substitution gives $0/0$. Divide numerator and denominator by
$(x-1)$ — that is, write each as a standard form with $a = 1$:

$$ \frac{x^{5}-1}{x^{2}-1} = \frac{\dfrac{x^{5}-1^{5}}{x-1}}{\dfrac{x^{2}-1^{2}}{x-1}} $$

Taking the limit of the top and bottom separately (the bottom limit is $2 \ne 0$):

$$ \lim_{x\to1}\frac{x^{5}-1}{x^{2}-1}
= \frac{5(1)^{4}}{2(1)^{1}} = \frac{5}{2} $$

**Check by factorisation.** $x^5-1=(x-1)(x^4+x^3+x^2+x+1)$ and
$x^2-1=(x-1)(x+1)$, so the ratio is $(x^4+x^3+x^2+x+1)/(x+1) \to 5/2$. ✓
:::

::: example Worked example 17.4 — rationalising a surd
**Problem.** Evaluate $\displaystyle\lim_{x\to0}\frac{\sqrt{1+x}-\sqrt{1-x}}{x}$.

**Solution.** Substitution gives $0/0$. Multiply top and bottom by the conjugate
$\sqrt{1+x}+\sqrt{1-x}$:

$$ \frac{\sqrt{1+x}-\sqrt{1-x}}{x}\cdot\frac{\sqrt{1+x}+\sqrt{1-x}}{\sqrt{1+x}+\sqrt{1-x}}
= \frac{(1+x)-(1-x)}{x\left(\sqrt{1+x}+\sqrt{1-x}\right)} $$

The numerator is $2x$, and $x \ne 0$ so it cancels:

$$ = \frac{2}{\sqrt{1+x}+\sqrt{1-x}}  \to  \frac{2}{1+1} = 1 $$
:::

### Limits at infinity

$\lim_{x\to\infty}f(x) = L$ means $f(x)$ can be brought arbitrarily close to $L$ by
taking $x$ large enough. The fundamental case is

$$ \lim_{x\to\infty}\frac{1}{x^{n}} = 0 \qquad (n > 0) $$

For a rational function, **divide every term by the highest power of $x$ in the
denominator**. Comparing degrees then gives a rule worth memorising.

::: memory Rational limits at infinity
For $f(x) = \dfrac{a_mx^{m}+\cdots}{b_nx^{n}+\cdots}$ as $x \to \infty$:

- $m < n$ (bottom heavier) $\Rightarrow$ limit is $0$
- $m = n$ (equal) $\Rightarrow$ limit is $a_m/b_n$, the ratio of leading coefficients
- $m > n$ (top heavier) $\Rightarrow$ limit is $\infty$ (does not exist finitely)

"Bottom heavy, zero; balanced, ratio; top heavy, blows up."
:::

When $\lim_{x\to\infty}f(x) = L$ is finite, the line $y = L$ is a **horizontal
asymptote** of the graph.

```figure caption="$f(x)=(3x^2+2x-1)/(5x^2-x+7)$ flattens onto its horizontal asymptote $y=3/5$, the ratio of the leading coefficients."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9,2.8))
x = np.linspace(1.0, 40, 900)
f = (3*x**2+2*x-1)/(5*x**2-x+7)
ax.plot(x, f, color=ACCENT, lw=2, label='$f(x)$')
ax.axhline(0.6, color='#d9534f', lw=1.4, ls='--', label='$y=3/5$')
for x0 in (2, 6, 16, 32):
    y0 = (3*x0**2+2*x0-1)/(5*x0**2-x0+7)
    ax.plot([x0],[y0], 'o', color=ACCENT, ms=4)
    ax.vlines(x0, 0.6, y0, color=MUTED, lw=.9)
ax.annotate('gap → 0', (32,(3*32**2+2*32-1)/(5*32**2-32+7)),
            textcoords='offset points', xytext=(-34,20), color=MUTED, fontsize=9,
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=.9, mutation_scale=9))
ax.set_xlabel('$x$'); ax.set_ylabel('$f(x)$')
ax.set_xlim(0,40); ax.set_ylim(0.5,0.72)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.45)
ax.legend(loc='lower right', fontsize=8.6)
```

::: example Worked example 17.5 — three degree cases
**Problem.** Evaluate as $x \to \infty$: (a) $\dfrac{3x^{2}+2x-1}{5x^{2}-x+7}$,
(b) $\dfrac{2x^{2}+3x+1}{x^{3}-2x+5}$, (c) $\dfrac{3x^{3}-2x}{4x^{2}+1}$.

**Solution.** (a) Divide top and bottom by $x^{2}$:

$$ \frac{3+\dfrac{2}{x}-\dfrac{1}{x^{2}}}{5-\dfrac{1}{x}+\dfrac{7}{x^{2}}}
\;\to\; \frac{3+0-0}{5-0+0} = \frac{3}{5} $$

(b) Divide by $x^{3}$: numerator $\to 0$, denominator $\to 1$, so the limit is $0$
(bottom heavier).

(c) Divide by $x^{2}$: $\dfrac{3x-\frac{2}{x}}{4+\frac{1}{x^{2}}}$. The numerator
grows without bound, so the limit is $\infty$; the limit does not exist finitely.
:::

### Limits of trigonometric functions

::: derivation The fundamental trigonometric limit
$$ \lim_{x \to 0}\frac{\sin x}{x} = 1 \qquad (x \text{ in radians}) $$

Take $0 < x < \pi/2$ and a unit circle with centre $O$. Let $A$ be on the circle,
$\angle AOB = x$, with $B$ on the horizontal radius. Comparing three areas —
triangle $OAB$, sector $OAB$, and the right triangle with the tangent at $B$ —

$$ \tfrac{1}{2}\sin x \;<\; \tfrac{1}{2}x \;<\; \tfrac{1}{2}\tan x $$

Divide throughout by $\tfrac{1}{2}\sin x$, which is positive:

$$ 1 < \frac{x}{\sin x} < \frac{1}{\cos x}
\qquad\Longrightarrow\qquad \cos x < \frac{\sin x}{x} < 1 $$

As $x \to 0^{+}$, $\cos x \to 1$, so by the sandwich (squeeze) theorem
$\sin x / x \to 1$. Since $\sin(-x)/(-x) = \sin x / x$, the function is even and
the left-hand limit is also 1. Hence the limit is 1.
:::

::: caution Radians only
$\lim_{x\to0}\frac{\sin x}{x} = 1$ is true **only in radians**. In degrees the
limit is $\pi/180 \approx 0.01745$, because $\sin x^{\circ} = \sin(\pi x/180)$. If
a question writes $\sin 30^{\circ}$ inside a limit, convert to radians first.
:::

```figure caption="$y=\sin x / x$ near the origin. The value at $x=0$ is undefined (hole), but the curve closes smoothly onto $y=1$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.9))
x = np.linspace(-9, 9, 1600); x = x[np.abs(x) > 1e-6]
ax.plot(x, np.sin(x)/x, color=ACCENT, lw=2)
ax.axhline(1, color='#d9534f', lw=1.1, ls='--')
ax.axhline(0, color=MUTED, lw=.8)
ax.plot([0],[1], marker='o', ms=7, mfc='white', mec=ACCENT, mew=1.8, zorder=6)
ax.annotate('hole at $(0,1)$', (0,1), textcoords='offset points', xytext=(12,10),
            color=INK, fontsize=9.3,
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=.9, mutation_scale=9))
ax.set_xlabel('$x$ (radians)'); ax.set_ylabel('$\\sin x / x$')
ax.set_xlim(-9,9); ax.set_ylim(-0.35,1.25)
ax.set_xticks([-9,-6,-3,0,3,6,9])
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.45)
```

Two companions follow immediately. Since $\tan x = \sin x/\cos x$,

$$ \lim_{x\to0}\frac{\tan x}{x} = \lim_{x\to0}\frac{\sin x}{x}\cdot\frac{1}{\cos x}
= 1 \times 1 = 1 $$

and using $1-\cos x = 2\sin^{2}(x/2)$,

$$ \lim_{x\to0}\frac{1-\cos x}{x^{2}}
= \lim_{x\to0}\frac{2\sin^{2}(x/2)}{x^{2}}
= \lim_{x\to0}\frac{1}{2}\left(\frac{\sin(x/2)}{x/2}\right)^{2} = \frac{1}{2} $$

::: example Worked example 17.6 — matching the angle to the denominator
**Problem.** Evaluate (a) $\displaystyle\lim_{x\to0}\frac{\sin 5x}{\tan 3x}$ and
(b) $\displaystyle\lim_{x\to0}\frac{1-\cos 4x}{x^{2}}$.

**Solution.** (a) Force each ratio to have matching angle on top and bottom:

$$ \frac{\sin 5x}{\tan 3x}
= \frac{\sin 5x}{5x}\cdot\frac{3x}{\tan 3x}\cdot\frac{5x}{3x} $$

As $x \to 0$ the first factor $\to 1$, the second $\to 1$, and the third is the
constant $5/3$. Hence the limit is $\dfrac{5}{3}$.

(b) Write $1-\cos4x = 2\sin^{2}2x$:

$$ \frac{2\sin^{2}2x}{x^{2}} = 2\left(\frac{\sin 2x}{2x}\right)^{2}\cdot\frac{(2x)^{2}}{x^{2}}
= 8\left(\frac{\sin 2x}{2x}\right)^{2} \;\to\; 8(1)^{2} = 8 $$
:::

### Limits of exponential and logarithmic functions

The number $e$ is *defined* by a limit:

$$ e = \lim_{x\to0}(1+x)^{1/x} = \lim_{x\to\infty}\left(1+\frac{1}{x}\right)^{x}
\approx 2.71828 $$

From it come the exponential and logarithmic standard limits:

$$ \lim_{x\to0}\frac{a^{x}-1}{x} = \ln a, \qquad
\lim_{x\to0}\frac{e^{x}-1}{x} = 1, \qquad
\lim_{x\to0}\frac{\ln(1+x)}{x} = 1 $$

```figure caption="$(1+1/x)^x$ climbs steadily towards $e \approx 2.718$ as $x$ increases — the limit that defines $e$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.8))
x = np.linspace(1, 120, 1200)
ax.plot(x, (1+1/x)**x, color=ACCENT, lw=2, label='$(1+1/x)^x$')
ax.axhline(np.e, color='#d9534f', lw=1.3, ls='--', label='$y=e$')
for xv in (1,2,5,10,50):
    ax.plot([xv],[(1+1/xv)**xv], 'o', color=ACCENT, ms=4.2)
ax.annotate('$x=1:\\ 2$', (1,2), textcoords='offset points', xytext=(6,-12),
            color=MUTED, fontsize=8.6)
ax.annotate('$x=50:\\ 2.691$', (50,(1+1/50)**50), textcoords='offset points',
            xytext=(-16,-20), color=MUTED, fontsize=8.6)
ax.set_xlabel('$x$'); ax.set_ylabel('$(1+1/x)^x$')
ax.set_xlim(0,120); ax.set_ylim(1.9,2.85)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.45)
ax.legend(loc='lower right', fontsize=8.6)
```

::: example Worked example 17.7 — exponential limits
**Problem.** Evaluate (a) $\displaystyle\lim_{x\to0}\frac{e^{3x}-1}{x}$,
(b) $\displaystyle\lim_{x\to0}\frac{5^{x}-3^{x}}{x}$, and
(c) $\displaystyle\lim_{x\to\infty}\left(1+\frac{3}{x}\right)^{2x}$.

**Solution.** (a) Multiply and divide by 3 so the exponent matches the denominator:

$$ \frac{e^{3x}-1}{x} = 3\cdot\frac{e^{3x}-1}{3x} \;\to\; 3 \times 1 = 3 $$

(b) Subtract and add 1 to split the fraction:

$$ \frac{5^{x}-3^{x}}{x} = \frac{(5^{x}-1)-(3^{x}-1)}{x}
= \frac{5^{x}-1}{x}-\frac{3^{x}-1}{x} \;\to\; \ln 5 - \ln 3 = \ln\frac{5}{3} $$

(c) Put $y = x/3$, so $x \to \infty$ gives $y \to \infty$ and $2x = 6y$:

$$ \left(1+\frac{1}{y}\right)^{6y} = \left[\left(1+\frac{1}{y}\right)^{y}\right]^{6}
\;\to\; e^{6} $$
:::

::: key Standard limits — the complete list
Every one of these is examinable and every one is used later. Learn them.

$$ \lim_{x\to a}\frac{x^{n}-a^{n}}{x-a} = n\,a^{n-1}, \qquad
\lim_{x\to\infty}\frac{1}{x^{n}} = 0\ \ (n>0) $$

$$ \lim_{x\to0}\frac{\sin x}{x} = 1, \qquad
\lim_{x\to0}\frac{\tan x}{x} = 1, \qquad
\lim_{x\to0}\frac{1-\cos x}{x^{2}} = \frac{1}{2} $$

$$ \lim_{x\to0}\frac{\sin^{-1}x}{x} = 1, \qquad
\lim_{x\to0}\frac{\tan^{-1}x}{x} = 1, \qquad
\lim_{x\to0}\cos x = 1 $$

$$ \lim_{\theta\to0}\frac{\sin\theta^{\circ}}{\theta} = \frac{\pi}{180} $$

$$ \lim_{x\to0}(1+x)^{1/x} = e, \qquad
\lim_{x\to\infty}\left(1+\frac{1}{x}\right)^{x} = e, \qquad
\lim_{x\to\infty}\left(1+\frac{a}{x}\right)^{x} = e^{a} $$

$$ \lim_{x\to0}\frac{a^{x}-1}{x} = \ln a, \qquad
\lim_{x\to0}\frac{e^{x}-1}{x} = 1, \qquad
\lim_{x\to0}\frac{\ln(1+x)}{x} = 1 $$

$$ \lim_{x\to0^{+}}\frac{1}{x} = +\infty, \qquad \lim_{x\to0^{-}}\frac{1}{x} = -\infty $$
:::

## 17.2 Indeterminate forms

Substituting $x = a$ sometimes produces a symbol that carries no information. Such
a symbol is called an **indeterminate form**: the limit may be any number, or may
not exist, and only further work decides which.

| Indeterminate | Typical source | Standard attack |
|---|---|---|
| $\dfrac{0}{0}$ | common factor, surd, trig at 0 | factorise, rationalise, or use a standard limit |
| $\dfrac{\infty}{\infty}$ | rational function as $x\to\infty$ | divide by the highest power of $x$ |
| $\infty-\infty$ | difference of surds or of fractions | rationalise, or combine over a common denominator |
| $0 \times \infty$ | product of a vanishing and a blowing-up factor | rewrite as $\frac{0}{0}$ or $\frac{\infty}{\infty}$ |
| $1^{\infty}$ | powers of $(1+\text{small})$ | force the form $(1+u)^{1/u}$ and use $e$ |
| $0^{0}$, $\infty^{0}$ | variable base and exponent | take logarithms first |

::: caution What is *not* indeterminate
$\dfrac{k}{0}$ with $k \ne 0$ is **not** indeterminate — it means the function is
unbounded, so the (two-sided) limit does not exist, though a one-sided limit may
be $+\infty$ or $-\infty$. Likewise $\dfrac{0}{k} = 0$ and $k^{\infty}$ for $k>1$
is $\infty$. Only the six forms in the table need extra work.
:::

::: example Worked example 17.8 — the $\infty-\infty$ form
**Problem.** Evaluate $\displaystyle\lim_{x\to\infty}\left(\sqrt{x^{2}+x}-x\right)$.

**Solution.** Both terms tend to $\infty$: the form is $\infty-\infty$. Rationalise
by multiplying by the conjugate:

$$ \sqrt{x^{2}+x}-x
= \frac{\left(\sqrt{x^{2}+x}-x\right)\left(\sqrt{x^{2}+x}+x\right)}{\sqrt{x^{2}+x}+x}
= \frac{x^{2}+x-x^{2}}{\sqrt{x^{2}+x}+x} = \frac{x}{\sqrt{x^{2}+x}+x} $$

Now divide top and bottom by $x$ (positive, so $\sqrt{x^{2}} = x$):

$$ = \frac{1}{\sqrt{1+\frac{1}{x}}+1} \;\to\; \frac{1}{\sqrt{1}+1} = \frac{1}{2} $$
:::

::: example Worked example 17.9 — $\infty-\infty$ from two fractions
**Problem.** Evaluate $\displaystyle\lim_{x\to1}\left(\frac{1}{x-1}-\frac{2}{x^{2}-1}\right)$.

**Solution.** Each fraction blows up, so combine them over the common denominator
$x^{2}-1 = (x-1)(x+1)$:

$$ \frac{1}{x-1}-\frac{2}{x^{2}-1}
= \frac{(x+1)-2}{(x-1)(x+1)} = \frac{x-1}{(x-1)(x+1)} $$

Cancel $(x-1)$, legal because $x \ne 1$:

$$ = \frac{1}{x+1} \;\to\; \frac{1}{2} $$
:::

::: example Worked example 17.10 — the $1^{\infty}$ form
**Problem.** Evaluate $\displaystyle\lim_{x\to0}(1+2x)^{1/3x}$.

**Solution.** The base $\to 1$ and the exponent $\to \infty$: the form is
$1^{\infty}$. Rewrite the exponent so that $(1+2x)^{1/2x}$ appears:

$$ (1+2x)^{1/3x} = \left[(1+2x)^{1/2x}\right]^{2/3} $$

As $x \to 0$, $2x \to 0$, so the inner bracket $\to e$. Therefore the limit is
$e^{2/3}$.
:::

::: tip Choosing the right move
Look at what caused the trouble. A **common factor** means factorise. A **surd**
means multiply by the conjugate. **Two fractions** means a common denominator.
**$x\to\infty$ in a rational function** means divide by the highest power.
**Powers of $(1 + \text{small})$** means force the $e$ form. Trigonometric or
exponential pieces mean insert the matching standard limit. Very few NEB questions
need anything else.
:::

## 17.3 Continuity and discontinuity of a function

### Continuity at a point

::: definition Continuity at a point
A function $f$ is **continuous at $x = a$** if all three conditions hold:

1. $f(a)$ is defined (i.e. $a$ is in the domain of $f$);
2. $\lim_{x\to a}f(x)$ exists, i.e. $\lim_{x\to a^{-}}f(x) = \lim_{x\to a^{+}}f(x)$;
3. $\lim_{x\to a}f(x) = f(a)$.

Compactly: $\lim_{x\to a^{-}}f(x) = \lim_{x\to a^{+}}f(x) = f(a)$. If any one
condition fails, $f$ is **discontinuous** at $a$.
:::

Informally, $f$ is continuous on an interval if its graph over that interval can
be drawn in one stroke without lifting the pen.

### Which functions are continuous

| Family | Continuous on |
|---|---|
| Polynomials | all of $\mathbb{R}$ |
| Rational $P(x)/Q(x)$ | all $x$ with $Q(x) \ne 0$ |
| $\sin x$, $\cos x$ | all of $\mathbb{R}$ |
| $\tan x$, $\sec x$ | all $x \ne (2n+1)\pi/2$ |
| $e^{x}$, $a^{x}$ | all of $\mathbb{R}$ |
| $\ln x$ | $x > 0$ |
| $\sqrt{x}$ | $x \ge 0$ |
| $|x|$ | all of $\mathbb{R}$ |

If $f$ and $g$ are continuous at $a$, so are $f \pm g$, $cf$, $fg$, and $f/g$
(provided $g(a) \ne 0$), and so is the composite $g \circ f$ when $g$ is
continuous at $f(a)$. Trouble therefore arises only at three kinds of place:
where a denominator vanishes, where a piecewise rule changes, and where the
formula itself is undefined.

### The three types of discontinuity

::: memory Removable, jump, infinite
- **Removable.** LHL $=$ RHL but $f(a)$ is missing or has the wrong value. A
  single point can be redefined to repair it — hence "removable".
- **Jump (finite / ordinary).** LHL and RHL both exist and are finite but are
  **unequal**. The size of the jump is $|\text{RHL}-\text{LHL}|$.
- **Infinite.** At least one one-sided limit is $\pm\infty$; the line $x = a$ is a
  vertical asymptote.
:::

```figure caption="The three discontinuities at $x=1$: removable (hole), jump (step), infinite (vertical asymptote)."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 3, figsize=(5.2,2.3), sharey=False)

ax = axes[0]
x = np.linspace(-0.6, 2.6, 400)
ax.plot(x[x < 0.99], (x[x < 0.99]+1), color=ACCENT, lw=1.9)
ax.plot(x[x > 1.01], (x[x > 1.01]+1), color=ACCENT, lw=1.9)
ax.plot([1],[2], marker='o', ms=6, mfc='white', mec=ACCENT, mew=1.6, zorder=5)
ax.set_title('removable', fontsize=9.5)
ax.set_ylim(0,4); ax.set_xlim(-0.6,2.6)

ax = axes[1]
xl = np.linspace(-0.6, 1, 200); xr = np.linspace(1, 2.6, 200)
ax.plot(xl, xl+1, color=ACCENT, lw=1.9)
ax.plot(xr, xr+0.2, color='#2e8b57', lw=1.9)
ax.plot([1],[2], marker='o', ms=6, mfc='white', mec=ACCENT, mew=1.6, zorder=5)
ax.plot([1],[1.2], marker='o', ms=5.2, color='#2e8b57', zorder=5)
ax.annotate('jump', (1,1.2), textcoords='offset points', xytext=(7,-17),
            color=MUTED, fontsize=8.4)
ax.set_title('jump', fontsize=9.5)
ax.set_ylim(0,4); ax.set_xlim(-0.6,2.6)

ax = axes[2]
xl = np.linspace(-0.6, 0.86, 300); xr = np.linspace(1.14, 2.6, 300)
ax.plot(xl, 1/(xl-1), color=ACCENT, lw=1.9)
ax.plot(xr, 1/(xr-1), color=ACCENT, lw=1.9)
ax.axhline(0, color=MUTED, lw=.8)
ax.axvline(1, color='#d9534f', lw=1.1, ls='--')
ax.set_title('infinite', fontsize=9.5)
ax.set_ylim(-8,8); ax.set_xlim(-0.6,2.6)

for ax in axes:
    ax.axvline(1, color=GRID, lw=0.8, zorder=0)
    ax.set_xticks([1]); ax.set_xticklabels(['$1$'])
    ax.set_yticks([])
    ax.spines[['top','right']].set_visible(False)
fig.tight_layout()
```

### Worked continuity problems

::: example Worked example 17.11 — classifying discontinuities
**Problem.** Classify the discontinuity of each function at the given point.

(a) $f(x) = \dfrac{x^{2}-9}{x-3}$ at $x = 3$; 
(b) $g(x) = \dfrac{|x-2|}{x-2}$ at $x = 2$; 
(c) $h(x) = \dfrac{1}{x-1}$ at $x = 1$.

**Solution.**

(a) $f(3)$ is $0/0$, undefined, so condition 1 fails. But for $x \ne 3$,
$f(x) = x+3$, so LHL $=$ RHL $= 6$. The limit exists while $f(3)$ does not:
this is a **removable** discontinuity. Defining $f(3) = 6$ repairs it.

(b) From Worked example 17.1, LHL $= -1$ and RHL $= +1$. Both are finite but
unequal, so this is a **jump** discontinuity of size $|1-(-1)| = 2$.

(c) As $x \to 1^{-}$, $x-1 \to 0^{-}$ so $h \to -\infty$; as $x\to1^{+}$,
$h \to +\infty$. This is an **infinite** discontinuity, and $x = 1$ is a vertical
asymptote.
:::

::: example Worked example 17.12 — finding $k$ for continuity
**Problem.** The function

$$ f(x) = \frac{x^{2}-1}{x-1}\ \ (x \ne 1), \qquad f(1) = k $$

is continuous at $x = 1$. Find $k$.

**Solution.** For $x \ne 1$, $\dfrac{x^{2}-1}{x-1} = \dfrac{(x-1)(x+1)}{x-1} = x+1$.
Hence

$$ \lim_{x\to1}f(x) = \lim_{x\to1}(x+1) = 2 $$

Continuity at $x=1$ requires $\lim_{x\to1}f(x) = f(1)$, i.e. $k = 2$.
:::

::: example Worked example 17.13 — a two-sided piecewise condition
**Problem.** A function is defined by $f(x) = 3x+a$ for $x<2$, $f(2)=7$, and
$f(x) = bx^{2}-1$ for $x>2$. Find $a$ and $b$ so that $f$ is continuous at $x=2$.

**Solution.** Apply the three conditions at $x = 2$.

*LHL:* $\lim_{x\to2^{-}}(3x+a) = 6+a$. 
*RHL:* $\lim_{x\to2^{+}}(bx^{2}-1) = 4b-1$. 
*Value:* $f(2) = 7$.

Continuity needs LHL $=$ RHL $= f(2)$:

$$ 6+a = 7 \;\Rightarrow\; a = 1, \qquad 4b-1 = 7 \;\Rightarrow\; b = 2 $$

So $a = 1$, $b = 2$.
:::

::: caution The commonest continuity slip
Students check only that LHL $=$ RHL and stop. Continuity needs the **third**
equality too: the common limit must equal $f(a)$. A function with LHL $=$ RHL but
a wrongly placed dot at $x=a$ is still discontinuous there (removable type).
:::

### Continuity on an interval, and one useful theorem

$f$ is continuous on the open interval $(a,b)$ if it is continuous at every point
inside. On the closed interval $[a,b]$ we additionally require continuity from the
right at $a$ ($\lim_{x\to a^{+}}f(x) = f(a)$) and from the left at $b$.

::: key Intermediate value theorem
If $f$ is continuous on $[a,b]$ and $N$ is any number between $f(a)$ and $f(b)$,
then there is at least one $c$ in $(a,b)$ with $f(c) = N$.

In particular, if $f(a)$ and $f(b)$ have **opposite signs**, then $f$ has a root
between $a$ and $b$. This is exactly the fact the bisection method of Unit 20
relies on.
:::

For example $f(x) = x^{3}-x-1$ is a polynomial, hence continuous. Since
$f(1) = -1 < 0$ and $f(2) = 5 > 0$, a root lies between 1 and 2.

## Chapter summary

- $\lim_{x\to a}f(x) = L$ describes the behaviour of $f$ **near** $a$, never at
  $a$; the value $f(a)$ is irrelevant to the limit.
- The limit exists iff LHL $=$ RHL $= L$, finite. Use $x = a \mp h$, $h>0$, to
  compute one-sided limits.
- Formally: for every $\varepsilon>0$ there is $\delta>0$ with
  $0<|x-a|<\delta \Rightarrow |f(x)-L|<\varepsilon$.
- Standard limits: $\frac{x^n-a^n}{x-a}\to na^{n-1}$; $\frac{\sin x}{x}\to1$;
  $\frac{\tan x}{x}\to1$; $\frac{1-\cos x}{x^{2}}\to\frac12$;
  $(1+x)^{1/x}\to e$; $\frac{a^{x}-1}{x}\to\ln a$; $\frac{\ln(1+x)}{x}\to1$;
  $\frac{1}{x^{n}}\to0$ as $x\to\infty$.
- The six indeterminate forms are $\frac00$, $\frac{\infty}{\infty}$,
  $\infty-\infty$, $0\times\infty$, $1^{\infty}$, $0^{0}$ (with $\infty^{0}$).
  Factorise, rationalise, divide by the highest power, or force the $e$ form.
- For a rational function as $x\to\infty$: bottom heavier $\Rightarrow 0$; equal
  degrees $\Rightarrow$ ratio of leading coefficients; top heavier $\Rightarrow\infty$.
- $f$ is continuous at $a$ iff $\lim_{x\to a^{-}}f = \lim_{x\to a^{+}}f = f(a)$.
- Discontinuities are **removable** (limit exists, value wrong or missing),
  **jump** (finite unequal one-sided limits) or **infinite** (a one-sided limit is
  $\pm\infty$, giving a vertical asymptote).

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. $\displaystyle\lim_{x\to2}\frac{x^{3}-8}{x^{2}-4}$ equals <span class="marks">[1]</span>
   (a) $2$ (b) $3$ (c) $4$ (d) $6$
2. $\displaystyle\lim_{x\to0}\frac{\sin 7x}{x}$ equals <span class="marks">[1]</span>
   (a) $0$ (b) $1$ (c) $7$ (d) $1/7$
3. $\displaystyle\lim_{x\to\infty}\frac{5x^{2}+3}{2x^{2}-x}$ equals <span class="marks">[1]</span>
   (a) $0$ (b) $5/2$ (c) $2/5$ (d) $\infty$
4. Which of the following is **not** an indeterminate form? <span class="marks">[1]</span>
   (a) $0/0$ (b) $\infty-\infty$ (c) $1^{\infty}$ (d) $0/5$
5. $f(x) = \dfrac{|x|}{x}$ has, at $x=0$, a discontinuity of type <span class="marks">[1]</span>
   (a) removable (b) jump (c) infinite (d) none — $f$ is continuous
6. $\displaystyle\lim_{x\to0}\frac{e^{x}-1}{x}$ equals <span class="marks">[1]</span>
   (a) $0$ (b) $1$ (c) $e$ (d) does not exist
7. If $f(x) = \dfrac{x^{2}-25}{x-5}$ for $x\ne5$, the value of $f(5)$ that makes $f$
   continuous is <span class="marks">[1]</span>
   (a) $0$ (b) $5$ (c) $10$ (d) $25$
8. $\displaystyle\lim_{x\to\infty}\left(1+\frac{4}{x}\right)^{x}$ equals <span class="marks">[1]</span>
   (a) $e$ (b) $4e$ (c) $e^{4}$ (d) $1$

::: note Answers to Group A
**1.** (b) — $\dfrac{(x-2)(x^2+2x+4)}{(x-2)(x+2)} \to \dfrac{12}{4} = 3$.

**2.** (c) — $\dfrac{\sin7x}{x} = 7\cdot\dfrac{\sin7x}{7x} \to 7$.

**3.** (b) — equal degrees, so the limit is the ratio of leading coefficients $5/2$.

**4.** (d) — $0/5 = 0$ exactly; nothing is indeterminate about it.

**5.** (b) — LHL $=-1$, RHL $=+1$: finite but unequal.

**6.** (b) — a standard limit, $\lim_{x\to0}(a^{x}-1)/x = \ln a$ with $a = e$.

**7.** (c) — $f(x) = x+5$ for $x\ne5$, whose limit at 5 is 10.

**8.** (c) — $\lim(1+a/x)^{x} = e^{a}$ with $a = 4$.
:::

**Group B — Short answer (5 marks each)**

1. Evaluate $\displaystyle\lim_{x\to1}\frac{x^{5}-1}{x^{2}-1}$ and state clearly
   which standard limit you have used. <span class="marks">[5]</span>
2. Evaluate $\displaystyle\lim_{x\to5}\frac{\sqrt{x+4}-3}{x-5}$. <span class="marks">[5]</span>
3. Prove that $\displaystyle\lim_{x\to0}\frac{\sin x}{x} = 1$ and hence evaluate
   $\displaystyle\lim_{x\to0}\frac{1-\cos x}{x^{2}}$. <span class="marks">[5]</span>
4. Evaluate $\displaystyle\lim_{x\to\infty}\left(\sqrt{x^{2}+3x}-x\right)$. <span class="marks">[5]</span>
5. A function is defined by $f(x) = 2x+3$ for $x \le 1$ and $f(x) = kx^{2}+1$ for
   $x > 1$. Find $k$ so that $f$ is continuous at $x=1$. <span class="marks">[5]</span>
6. Using the $\varepsilon$–$\delta$ definition, prove that
   $\displaystyle\lim_{x\to4}(3x-5) = 7$. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Write both as standard forms about $a=1$:
$\dfrac{x^{5}-1}{x^{2}-1} = \dfrac{(x^{5}-1)/(x-1)}{(x^{2}-1)/(x-1)}$.
Using $\lim_{x\to a}\frac{x^{n}-a^{n}}{x-a} = na^{n-1}$ with $a=1$, the numerator
tends to $5(1)^{4} = 5$ and the denominator to $2(1)^{1} = 2$. Hence the limit is
$\boxed{5/2}$.

**2.** Form $0/0$. Multiply by the conjugate $\sqrt{x+4}+3$:

$$ \frac{\sqrt{x+4}-3}{x-5}\cdot\frac{\sqrt{x+4}+3}{\sqrt{x+4}+3}
= \frac{(x+4)-9}{(x-5)(\sqrt{x+4}+3)} = \frac{x-5}{(x-5)(\sqrt{x+4}+3)} $$

Cancel $(x-5)$ since $x \ne 5$, leaving $\dfrac{1}{\sqrt{x+4}+3} \to \dfrac{1}{3+3} = \dfrac{1}{6}$.

**3.** *Proof.* For $0 < x < \pi/2$, comparing the areas of triangle $OAB$, sector
$OAB$ and the tangent triangle in a unit circle gives
$\frac12\sin x < \frac12 x < \frac12\tan x$. Dividing by $\frac12\sin x > 0$ gives
$1 < x/\sin x < 1/\cos x$, i.e. $\cos x < \frac{\sin x}{x} < 1$. As $x\to0^{+}$,
$\cos x \to 1$, so by the squeeze theorem $\frac{\sin x}{x}\to1$. The function is
even, so the left-hand limit is 1 too.

*Hence.* $1-\cos x = 2\sin^{2}(x/2)$, so

$$ \frac{1-\cos x}{x^{2}} = \frac{2\sin^{2}(x/2)}{4(x/2)^{2}}
= \frac{1}{2}\left(\frac{\sin(x/2)}{x/2}\right)^{2} \to \frac{1}{2}(1)^{2} = \frac{1}{2} $$

**4.** Form $\infty-\infty$. Rationalise:

$$ \sqrt{x^{2}+3x}-x = \frac{x^{2}+3x-x^{2}}{\sqrt{x^{2}+3x}+x} = \frac{3x}{\sqrt{x^{2}+3x}+x} $$

Divide top and bottom by $x>0$:
$\dfrac{3}{\sqrt{1+3/x}+1} \to \dfrac{3}{1+1} = \dfrac{3}{2}$.

**5.** LHL $= \lim_{x\to1^{-}}(2x+3) = 5$, and $f(1) = 2(1)+3 = 5$.
RHL $= \lim_{x\to1^{+}}(kx^{2}+1) = k+1$.
Continuity requires $k+1 = 5$, so $k = 4$.

**6.** Let $\varepsilon>0$. Then $|(3x-5)-7| = |3x-12| = 3|x-4|$, which is less
than $\varepsilon$ exactly when $|x-4| < \varepsilon/3$. Choose $\delta = \varepsilon/3$;
then $0<|x-4|<\delta \Rightarrow |(3x-5)-7| = 3|x-4| < 3\delta = \varepsilon$.
Since $\delta$ exists for every $\varepsilon$, the limit is 7.
:::

**Group C — Long answer (8 marks each)**

1. (a) State the three conditions for a function to be continuous at $x = a$, and
   describe the three types of discontinuity with a sketch of each. <span class="marks">[4]</span>
   (b) Discuss the continuity of

   $$ f(x) = \frac{x^{2}-1}{x-1}\ (x<1), \qquad f(1) = 3, \qquad f(x) = 2x\ (x>1) $$

   at $x = 1$, classify the discontinuity, and state how (if at all) it can be
   removed. <span class="marks">[4]</span>
2. (a) Define an indeterminate form and list the six standard ones. <span class="marks">[2]</span>
   (b) Evaluate $\displaystyle\lim_{x\to0}\frac{5^{x}-3^{x}}{x}$,
   $\displaystyle\lim_{x\to0}\frac{\sin 5x}{\tan 3x}$ and
   $\displaystyle\lim_{x\to0}(1+2x)^{1/3x}$, naming the form in each case. <span class="marks">[6]</span>

::: note Answers to Group C
**1. (a)** $f$ is continuous at $a$ iff (i) $f(a)$ is defined, (ii)
$\lim_{x\to a}f(x)$ exists (LHL $=$ RHL), (iii) that limit equals $f(a)$.
*Removable:* LHL $=$ RHL but $f(a)$ missing or different — a hole in the graph.
*Jump:* LHL and RHL finite but unequal — a step. *Infinite:* a one-sided limit is
$\pm\infty$ — a vertical asymptote. (See the three-panel figure in §17.3.)

**(b)** LHL $= \lim_{x\to1^{-}}\dfrac{(x-1)(x+1)}{x-1} = \lim_{x\to1^{-}}(x+1) = 2$.
RHL $= \lim_{x\to1^{+}}2x = 2$. So the limit exists and equals 2. But
$f(1) = 3 \ne 2$, so condition (iii) fails and $f$ is discontinuous at $x=1$.
Because the limit exists and is finite, the discontinuity is **removable**;
redefining $f(1) = 2$ makes $f$ continuous at 1.

**2. (a)** An indeterminate form is an expression obtained by direct substitution
whose value is not determined by the limits of its parts — the limit may be any
number or may fail to exist. The six are $\frac00$, $\frac{\infty}{\infty}$,
$\infty-\infty$, $0\times\infty$, $1^{\infty}$ and $0^{0}$ (with $\infty^{0}$ a
seventh variant of the last).

**(b)** *First* ($\frac00$): split as
$\dfrac{(5^{x}-1)-(3^{x}-1)}{x} = \dfrac{5^{x}-1}{x}-\dfrac{3^{x}-1}{x}
\to \ln 5 - \ln 3 = \ln(5/3)$.

*Second* ($\frac00$): $\dfrac{\sin5x}{\tan3x}
= \dfrac{\sin5x}{5x}\cdot\dfrac{3x}{\tan3x}\cdot\dfrac{5}{3} \to 1\cdot1\cdot\dfrac53 = \dfrac53$.

*Third* ($1^{\infty}$): $(1+2x)^{1/3x} = \left[(1+2x)^{1/2x}\right]^{2/3} \to e^{2/3}$.
:::
