---
subject: Mathematics
grade: 11
unit: 18
title: Derivatives
hours: 22
area: Calculus
---

This is the longest unit in Grade 11 Mathematics, and the one that pays back most.
A derivative measures **how fast a quantity changes** — the slope of a curve, the
velocity of a body, the marginal cost of a shirt. Once you can differentiate, you
can find tangents and normals, decide where a graph rises or falls, locate its
highest and lowest points, and describe how it bends. Everything in this chapter
grows from a single limit, the one in §18.1, so learn that definition before
anything else.

::: key What the examiner asks from this unit
Derivatives carry more marks than any other single unit. Expect: two or three
Group A items (a quick derivative, a tangent slope, a maximum); a Group B question
asking for a derivative **by first principle** — this appears almost every year;
a Group B question on implicit, parametric or logarithmic differentiation; and a
full Group C question on maxima and minima or on tangent, normal and monotonicity.
The standard-derivative table in §18.2 must be in your memory, not in your notes.
:::

## 18.1 Derivative by first principle (definition)

### From average rate to instantaneous rate

Take a curve $y = f(x)$ and two points on it, $P(x,\,f(x))$ and
$Q(x+h,\,f(x+h))$. The straight line $PQ$ is a **secant** (a chord). Its slope is
the *average* rate of change of $f$ over the interval of width $h$:

$$ \text{slope of } PQ = \frac{f(x+h)-f(x)}{(x+h)-x} = \frac{f(x+h)-f(x)}{h} $$

Now slide $Q$ down the curve towards $P$ by letting $h \to 0$. The secant pivots
about $P$ and settles onto the **tangent** at $P$. The limiting slope is the
derivative.

```figure caption="Secants $PQ_1, PQ_2, PQ_3$ with shrinking $h$ rotate onto the tangent at $P$. The slope of the secant is $[f(x+h)-f(x)]/h$; its limit as $h\to0$ is $f'(x)$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,3.2))
f  = lambda z: 0.32*z**2 + 0.5
fp = lambda z: 0.64*z
x0 = 1.2; y0 = f(x0)
xs = np.linspace(0.0, 4.4, 400)
ax.plot(xs, f(xs), color=ACCENT, lw=2.2, zorder=4, label='$y=f(x)$')
cols = ['#b8860b', '#2e8b57', '#6a5acd']
for (hh, c, n, off) in zip([2.6, 1.5, 0.75], cols, [1, 2, 3],
                           [(6,-3), (6,-4), (4,-15)]):
    x1 = x0 + hh; y1 = f(x1)
    m = (y1-y0)/hh
    tt = np.array([x0-0.55, x1+0.30])
    ax.plot(tt, y0 + m*(tt-x0), color=c, lw=1.15, ls='--', zorder=3)
    ax.plot([x1],[y1], 'o', color=c, ms=4.6, zorder=6)
    ax.annotate(f'$Q_{n}$', (x1,y1), textcoords='offset points', xytext=off,
                color=c, fontsize=9)
m = fp(x0)
tt = np.array([x0-1.1, x0+2.4])
ax.plot(tt, y0 + m*(tt-x0), color='#d9534f', lw=1.9, zorder=5, label='tangent at $P$')
ax.plot([x0],[y0], 'o', color=INK, ms=5.6, zorder=7)
ax.annotate('$P$', (x0,y0), textcoords='offset points', xytext=(-13,-4),
            color=INK, fontsize=10)
ax.annotate('$h$ shrinks', (x0+1.5, f(x0+1.5)), textcoords='offset points',
            xytext=(-2,-34), color=MUTED, fontsize=9,
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.0, mutation_scale=10))
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.set_xlim(0,4.6); ax.set_ylim(0,7)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.4)
ax.legend(loc='upper left', fontsize=8.6)
```

::: definition Derivative — first principle
The derivative of $f$ at $x$ is

$$ f'(x) = \lim_{h \to 0}\frac{f(x+h)-f(x)}{h} $$

provided this limit exists and is finite. Finding a derivative straight from this
limit is called differentiation **from first principles** (or *ab initio*, or *by
the delta method*). An equivalent form used at a particular point $x=a$ is

$$ f'(a) = \lim_{x \to a}\frac{f(x)-f(a)}{x-a} $$

Notations for the same thing: $f'(x)$, $\dfrac{dy}{dx}$, $y'$, $y_1$,
$\dfrac{d}{dx}f(x)$, $Df(x)$.
:::

### The four-step procedure

Every first-principle question is answered by the same four steps. Write them out
every time — examiners give a mark for each.

::: memory The four steps
1. Write down $f(x+h)$, replacing every $x$ in the formula by $x+h$.
2. Form the difference $f(x+h)-f(x)$ and simplify it as far as possible.
3. Divide by $h$ — the simplification in step 2 must make one factor of $h$ cancel.
4. Take the limit as $h \to 0$.
:::

The only real skill is step 2: you must find the trick that exposes a factor of
$h$. For polynomials it is expansion; for surds it is the conjugate; for fractions
it is a common denominator; for trigonometric functions it is the
sum-to-product formula; for exponentials and logarithms it is a standard limit
from Unit 17.

::: derivation First principles: $y = x^{n}$
$$ \frac{dy}{dx} = \lim_{h\to0}\frac{(x+h)^{n}-x^{n}}{h} $$

Put $z = x+h$. As $h \to 0$ we have $z \to x$, and $h = z-x$, so

$$ \frac{dy}{dx} = \lim_{z\to x}\frac{z^{n}-x^{n}}{z-x} $$

This is exactly the standard algebraic limit of Unit 17, whose value is
$n\,x^{n-1}$. Hence

$$ \frac{d}{dx}\left(x^{n}\right) = n\,x^{n-1} $$

valid for every real index $n$. In particular $\dfrac{d}{dx}(x) = 1$ and
$\dfrac{d}{dx}(c) = 0$ for a constant $c$, since $c = cx^{0}$.
:::

::: derivation First principles: $y = \sqrt{x}$
$$ \frac{dy}{dx} = \lim_{h\to0}\frac{\sqrt{x+h}-\sqrt{x}}{h} $$

Step 2 gives $0$ over $0$, so multiply above and below by the conjugate
$\sqrt{x+h}+\sqrt{x}$:

$$ = \lim_{h\to0}\frac{(x+h)-x}{h\left(\sqrt{x+h}+\sqrt{x}\right)}
 = \lim_{h\to0}\frac{h}{h\left(\sqrt{x+h}+\sqrt{x}\right)} $$

Cancel $h$ — legal because $h \ne 0$ in a limit — and then let $h \to 0$:

$$ = \lim_{h\to0}\frac{1}{\sqrt{x+h}+\sqrt{x}} = \frac{1}{2\sqrt{x}} $$

This agrees with the power rule: $\sqrt{x} = x^{1/2}$ gives
$\tfrac12 x^{-1/2} = 1/(2\sqrt{x})$.
:::

::: derivation First principles: $y = \sin x$
$$ \frac{dy}{dx} = \lim_{h\to0}\frac{\sin(x+h)-\sin x}{h} $$

Use the sum-to-product identity
$\sin C - \sin D = 2\cos\dfrac{C+D}{2}\sin\dfrac{C-D}{2}$ with $C = x+h$,
$D = x$:

$$ \sin(x+h)-\sin x = 2\cos\left(x+\frac{h}{2}\right)\sin\frac{h}{2} $$

So

$$ \frac{dy}{dx}
= \lim_{h\to0}\frac{2\cos\left(x+\frac h2\right)\sin\frac h2}{h}
= \lim_{h\to0}\cos\left(x+\frac h2\right)\cdot\frac{\sin\frac h2}{\frac h2} $$

As $h \to 0$ the first factor tends to $\cos x$ and the second to 1 by the
standard limit $\lim_{u\to0}\frac{\sin u}{u} = 1$. Hence

$$ \frac{d}{dx}(\sin x) = \cos x $$

The same argument with $\cos C - \cos D = -2\sin\dfrac{C+D}{2}\sin\dfrac{C-D}{2}$
gives $\dfrac{d}{dx}(\cos x) = -\sin x$.
:::

::: derivation First principles: $y = e^{x}$ and $y = a^{x}$
$$ \frac{dy}{dx} = \lim_{h\to0}\frac{a^{x+h}-a^{x}}{h}
= \lim_{h\to0}\frac{a^{x}\left(a^{h}-1\right)}{h}
= a^{x}\lim_{h\to0}\frac{a^{h}-1}{h} $$

The factor $a^{x}$ does not involve $h$, so it comes outside the limit. The
remaining limit is the standard exponential limit of Unit 17, equal to $\ln a$.
Hence

$$ \frac{d}{dx}\left(a^{x}\right) = a^{x}\ln a, \qquad\text{and with } a = e,
\qquad \frac{d}{dx}\left(e^{x}\right) = e^{x} $$

since $\ln e = 1$. The exponential function $e^{x}$ is the only function equal to
its own derivative.
:::

::: derivation First principles: $y = \ln x$
$$ \frac{dy}{dx} = \lim_{h\to0}\frac{\ln(x+h)-\ln x}{h}
= \lim_{h\to0}\frac{1}{h}\ln\!\left(\frac{x+h}{x}\right)
= \lim_{h\to0}\frac{1}{h}\ln\!\left(1+\frac{h}{x}\right) $$

Put $u = h/x$, so $h = ux$ and $u \to 0$ as $h \to 0$:

$$ = \lim_{u\to0}\frac{1}{ux}\ln(1+u)
= \frac{1}{x}\lim_{u\to0}\frac{\ln(1+u)}{u} = \frac{1}{x}\cdot 1 $$

using the standard limit $\lim_{u\to0}\frac{\ln(1+u)}{u} = 1$. Hence

$$ \frac{d}{dx}(\ln x) = \frac{1}{x} \qquad (x>0) $$
:::

::: derivation First principles: $y = \tan x$
$$ \frac{dy}{dx} = \lim_{h\to0}\frac{\tan(x+h)-\tan x}{h} $$

Combine the two tangents over a common denominator:

$$ \tan(x+h)-\tan x = \frac{\sin(x+h)}{\cos(x+h)}-\frac{\sin x}{\cos x}
= \frac{\sin(x+h)\cos x-\cos(x+h)\sin x}{\cos(x+h)\cos x} $$

The numerator is $\sin\left[(x+h)-x\right] = \sin h$. Therefore

$$ \frac{dy}{dx} = \lim_{h\to0}\frac{\sin h}{h\cos(x+h)\cos x}
= \lim_{h\to0}\frac{\sin h}{h}\cdot\frac{1}{\cos(x+h)\cos x}
= \frac{1}{\cos^{2}x} = \sec^{2}x $$
:::

::: example Worked example 18.1 — a polynomial from first principles
**Problem.** Differentiate $f(x) = x^{3}+2x$ from first principles.

**Solution.**

*Step 1.* $f(x+h) = (x+h)^{3}+2(x+h) = x^{3}+3x^{2}h+3xh^{2}+h^{3}+2x+2h$.

*Step 2.* Subtract $f(x) = x^{3}+2x$; the terms without $h$ cancel:

$$ f(x+h)-f(x) = 3x^{2}h+3xh^{2}+h^{3}+2h = h\left(3x^{2}+3xh+h^{2}+2\right) $$

*Step 3.* Divide by $h$ (allowed, $h \ne 0$):

$$ \frac{f(x+h)-f(x)}{h} = 3x^{2}+3xh+h^{2}+2 $$

*Step 4.* Let $h \to 0$: every term containing $h$ vanishes, leaving

$$ f'(x) = 3x^{2}+2 $$
:::

::: example Worked example 18.2 — a surd from first principles
**Problem.** Find $\dfrac{dy}{dx}$ from first principles if $y = \sqrt{2x+3}$.

**Solution.**

*Step 1.* $y+\delta y = \sqrt{2(x+h)+3} = \sqrt{2x+2h+3}$.

*Step 2 and 3.* Form the difference quotient and rationalise the numerator:

$$ \frac{\sqrt{2x+2h+3}-\sqrt{2x+3}}{h}
\cdot\frac{\sqrt{2x+2h+3}+\sqrt{2x+3}}{\sqrt{2x+2h+3}+\sqrt{2x+3}}
= \frac{(2x+2h+3)-(2x+3)}{h\left(\sqrt{2x+2h+3}+\sqrt{2x+3}\right)} $$

The numerator is $2h$, so after cancelling $h$,

$$ = \frac{2}{\sqrt{2x+2h+3}+\sqrt{2x+3}} $$

*Step 4.* Let $h \to 0$:

$$ \frac{dy}{dx} = \frac{2}{2\sqrt{2x+3}} = \frac{1}{\sqrt{2x+3}} $$
:::

::: example Worked example 18.3 — a rational function from first principles
**Problem.** Differentiate $f(x) = \dfrac{1}{x+1}$ from first principles.

**Solution.**

$$ \frac{f(x+h)-f(x)}{h}
= \frac{1}{h}\left(\frac{1}{x+h+1}-\frac{1}{x+1}\right) $$

Put the bracket over the common denominator $(x+h+1)(x+1)$:

$$ = \frac{1}{h}\cdot\frac{(x+1)-(x+h+1)}{(x+h+1)(x+1)}
= \frac{1}{h}\cdot\frac{-h}{(x+h+1)(x+1)} = \frac{-1}{(x+h+1)(x+1)} $$

Letting $h \to 0$,

$$ f'(x) = \frac{-1}{(x+1)^{2}} $$
:::

::: example Worked example 18.4 — a trigonometric function from first principles
**Problem.** Find the derivative of $y = \sin 2x$ from first principles.

**Solution.**

$$ \frac{dy}{dx} = \lim_{h\to0}\frac{\sin 2(x+h)-\sin 2x}{h}
= \lim_{h\to0}\frac{\sin(2x+2h)-\sin 2x}{h} $$

Apply $\sin C-\sin D = 2\cos\frac{C+D}{2}\sin\frac{C-D}{2}$ with $C = 2x+2h$ and
$D = 2x$, so $\frac{C+D}{2} = 2x+h$ and $\frac{C-D}{2} = h$:

$$ = \lim_{h\to0}\frac{2\cos(2x+h)\sin h}{h}
= 2\lim_{h\to0}\cos(2x+h)\cdot\lim_{h\to0}\frac{\sin h}{h} $$

$$ = 2\cos 2x \times 1 = 2\cos 2x $$
:::

::: example Worked example 18.5 — an exponential from first principles
**Problem.** Differentiate $y = e^{2x}$ from first principles.

**Solution.**

$$ \frac{dy}{dx} = \lim_{h\to0}\frac{e^{2(x+h)}-e^{2x}}{h}
= \lim_{h\to0}\frac{e^{2x}\left(e^{2h}-1\right)}{h} $$

Take the constant factor $e^{2x}$ outside and adjust the fraction so the exponent
matches the denominator:

$$ = e^{2x}\lim_{h\to0}\frac{e^{2h}-1}{h}
= e^{2x}\cdot 2\lim_{h\to0}\frac{e^{2h}-1}{2h} = 2e^{2x} $$

using $\lim_{u\to0}\dfrac{e^{u}-1}{u} = 1$ with $u = 2h$.
:::

### Differentiability and continuity

::: key Differentiable $\Rightarrow$ continuous, but not conversely
If $f$ is differentiable at $a$ then $f$ is continuous at $a$. The converse is
false: $f(x) = |x|$ is continuous at $0$ but not differentiable there, because

$$ \lim_{h\to0^{-}}\frac{|0+h|-|0|}{h} = -1, \qquad
\lim_{h\to0^{+}}\frac{|0+h|-|0|}{h} = +1 $$

The left-hand derivative and right-hand derivative disagree, so $f'(0)$ does not
exist. The graph has a **corner** there.
:::

A derivative fails to exist at a point for exactly one of four reasons: a corner
(one-sided derivatives differ), a vertical tangent (the limit is $\pm\infty$, as
for $y = x^{1/3}$ at $0$), a discontinuity, or an endpoint of the domain.

::: example Worked example 18.5a — continuous but not differentiable
**Problem.** Show that $f(x) = |x-2|$ is continuous at $x = 2$ but not
differentiable there.

**Solution.** *Continuity.* For $x<2$, $f(x) = 2-x$, so
$\lim_{x\to2^{-}}f(x) = 0$. For $x>2$, $f(x) = x-2$, so
$\lim_{x\to2^{+}}f(x) = 0$. Also $f(2) = |2-2| = 0$. Since
LHL $=$ RHL $= f(2) = 0$, $f$ is continuous at $x = 2$.

*Differentiability.* Compute the two one-sided derivatives from the definition.

Left-hand derivative, with $h<0$ so that $2+h<2$ and $f(2+h) = -h$:

$$ Lf'(2) = \lim_{h\to0^{-}}\frac{f(2+h)-f(2)}{h}
= \lim_{h\to0^{-}}\frac{-h-0}{h} = -1 $$

Right-hand derivative, with $h>0$ so that $f(2+h) = h$:

$$ Rf'(2) = \lim_{h\to0^{+}}\frac{h-0}{h} = +1 $$

Since $Lf'(2) \ne Rf'(2)$, the limit defining $f'(2)$ does not exist, so $f$ is not
differentiable at $x = 2$ even though it is continuous there.
:::

```figure caption="$y=|x|$ is continuous everywhere but has no derivative at $x=0$: the slope is $-1$ on the left and $+1$ on the right, so no single tangent exists at the corner."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4,2.8))
x = np.linspace(-2.2, 2.2, 400)
ax.plot(x, np.abs(x), color=ACCENT, lw=2.4, zorder=4)
tt = np.array([-1.5, 0.55])
ax.plot(tt, -tt, color='#2e8b57', lw=1.2, ls='--', zorder=3)
ax.plot(-tt, -tt, color='#b8860b', lw=1.2, ls='--', zorder=3)
ax.plot([0],[0], 'o', color='#d9534f', ms=6.5, zorder=6)
ax.annotate('slope $-1$', (-1.4,1.4), textcoords='offset points', xytext=(-6,6),
            color='#2e8b57', fontsize=9, ha='left')
ax.annotate('slope $+1$', (1.4,1.4), textcoords='offset points', xytext=(-42,6),
            color='#b8860b', fontsize=9)
ax.annotate('corner: $f\'(0)$ does not exist', (0,0), textcoords='offset points',
            xytext=(-56,-42), color='#d9534f', fontsize=8.8,
            arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.0, mutation_scale=9))
ax.axhline(0, color=MUTED, lw=.8); ax.axvline(0, color=MUTED, lw=.8)
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.set_xlim(-2.2,2.2); ax.set_ylim(-1.35,2.3)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.35)
```

::: caution "Continuous" is not "smooth"
A question that asks you to show $f$ is continuous but not differentiable at a
point is asking for two separate calculations: LHL $=$ RHL $= f(a)$ for
continuity, and then the **left-hand and right-hand derivatives** from the
definition. Showing only continuity earns half the marks.
:::

## 18.2 Rules of differentiation

Differentiating everything from first principles would be unbearable. The rules
below do the work instead; each is proved once from the definition and then used
for ever.

### Sum, difference and constant multiple

If $u$ and $v$ are differentiable functions of $x$ and $c$ is a constant,

$$ \frac{d}{dx}(u \pm v) = \frac{du}{dx} \pm \frac{dv}{dx}, \qquad
\frac{d}{dx}(cu) = c\,\frac{du}{dx}, \qquad \frac{d}{dx}(c) = 0 $$

These follow directly from the corresponding limit laws. Differentiation is
therefore **linear**: differentiate a long sum term by term.

### The power rule

$$ \frac{d}{dx}\left(x^{n}\right) = n\,x^{n-1} \qquad \text{for every real } n $$

Before using it, rewrite roots and reciprocals as powers: $\sqrt{x} = x^{1/2}$,
$\dfrac{1}{x^{3}} = x^{-3}$, $\dfrac{1}{\sqrt[3]{x}} = x^{-1/3}$.

::: example Worked example 18.6 — power and sum rules together
**Problem.** Differentiate $y = 3x^{4}-\dfrac{5}{x^{2}}+2\sqrt{x}-7$.

**Solution.** First convert every term to a power of $x$:

$$ y = 3x^{4}-5x^{-2}+2x^{1/2}-7 $$

Differentiate term by term, using $\frac{d}{dx}x^{n} = nx^{n-1}$ on each:

$$ \frac{dy}{dx} = 3(4x^{3})-5(-2x^{-3})+2\left(\tfrac12 x^{-1/2}\right)-0 $$

$$ = 12x^{3}+10x^{-3}+x^{-1/2}
= 12x^{3}+\frac{10}{x^{3}}+\frac{1}{\sqrt{x}} $$

Note the double negative in the second term: $-5 \times (-2) = +10$. This sign is
the commonest slip in the whole unit.
:::

### The product rule

::: derivation Product rule from first principles
Let $y = uv$ where $u = u(x)$ and $v = v(x)$. Give $x$ an increment $h$, so $u$
becomes $u+\delta u$ and $v$ becomes $v+\delta v$. Then

$$ \delta y = (u+\delta u)(v+\delta v)-uv
= u\,\delta v+v\,\delta u+\delta u\,\delta v $$

Divide by $h$:

$$ \frac{\delta y}{h} = u\frac{\delta v}{h}+v\frac{\delta u}{h}
+\delta u\cdot\frac{\delta v}{h} $$

As $h \to 0$ we have $\delta u \to 0$ (because $u$ is continuous), while
$\delta u/h \to du/dx$ and $\delta v/h \to dv/dx$. The last term therefore tends
to $0 \times dv/dx = 0$, and

$$ \frac{d}{dx}(uv) = u\,\frac{dv}{dx}+v\,\frac{du}{dx} $$
:::

In words: **first times derivative of second, plus second times derivative of
first.** For three factors the pattern extends:
$(uvw)' = u'vw+uv'w+uvw'$.

::: example Worked example 18.7 — product rule
**Problem.** Differentiate $y = x^{3}\sin x$.

**Solution.** Take $u = x^{3}$ and $v = \sin x$, so $u' = 3x^{2}$ and
$v' = \cos x$. By the product rule,

$$ \frac{dy}{dx} = u\,v'+v\,u' = x^{3}\cos x+\sin x\cdot 3x^{2} $$

$$ = x^{3}\cos x+3x^{2}\sin x = x^{2}\left(x\cos x+3\sin x\right) $$
:::

### The quotient rule

::: derivation Quotient rule
Let $y = \dfrac{u}{v}$ with $v \ne 0$. With increments as before,

$$ \delta y = \frac{u+\delta u}{v+\delta v}-\frac{u}{v}
= \frac{v(u+\delta u)-u(v+\delta v)}{v(v+\delta v)}
= \frac{v\,\delta u-u\,\delta v}{v(v+\delta v)} $$

Divide by $h$ and let $h \to 0$; then $\delta v \to 0$, so $v+\delta v \to v$:

$$ \frac{dy}{dx} = \frac{v\dfrac{du}{dx}-u\dfrac{dv}{dx}}{v^{2}} $$
:::

The order matters here: it is **denominator times derivative of numerator, minus
numerator times derivative of denominator, all over the denominator squared.**
Reverse the subtraction and every sign in your answer is wrong.

::: example Worked example 18.8 — quotient rule
**Problem.** Differentiate $y = \dfrac{2x+3}{3x-2}$.

**Solution.** Take $u = 2x+3$ ($u' = 2$) and $v = 3x-2$ ($v' = 3$):

$$ \frac{dy}{dx} = \frac{(3x-2)(2)-(2x+3)(3)}{(3x-2)^{2}}
= \frac{6x-4-6x-9}{(3x-2)^{2}} = \frac{-13}{(3x-2)^{2}} $$

The derivative is negative for every $x \ne 2/3$, so this curve is decreasing on
each of its two branches.
:::

::: example Worked example 18.9 — quotient rule with an identity
**Problem.** Differentiate $y = \dfrac{\sin x}{1+\cos x}$.

**Solution.** With $u = \sin x$ and $v = 1+\cos x$,

$$ \frac{dy}{dx} = \frac{(1+\cos x)\cos x-\sin x(-\sin x)}{(1+\cos x)^{2}}
= \frac{\cos x+\cos^{2}x+\sin^{2}x}{(1+\cos x)^{2}} $$

Now use $\sin^{2}x+\cos^{2}x = 1$:

$$ = \frac{\cos x+1}{(1+\cos x)^{2}} = \frac{1}{1+\cos x} $$

Always look for a Pythagorean identity in the numerator before writing the final
line — the tidy form is what the marker wants.
:::

### The chain rule

If $y$ is a function of $u$ and $u$ is a function of $x$, then

$$ \frac{dy}{dx} = \frac{dy}{du}\times\frac{du}{dx} $$

This is the single most used rule in the chapter. For a composite
$y = f(g(x))$ it reads $y' = f'(g(x))\cdot g'(x)$: **differentiate the outside
function, keep the inside unchanged, then multiply by the derivative of the
inside.**

::: memory The chain of layers
Peel the function like an onion, outermost layer first, multiplying as you go.
For $y = \sin^{3}(2x+1)$ the layers are: cube $\to$ sine $\to$ linear, so
$y' = 3[\sin(2x+1)]^{2}\times\cos(2x+1)\times 2$.
:::

::: example Worked example 18.10 — one application of the chain rule
**Problem.** Differentiate $y = (3x^{2}+5)^{7}$.

**Solution.** Put $u = 3x^{2}+5$, so $y = u^{7}$. Then

$$ \frac{dy}{du} = 7u^{6}, \qquad \frac{du}{dx} = 6x $$

$$ \frac{dy}{dx} = \frac{dy}{du}\cdot\frac{du}{dx}
= 7\left(3x^{2}+5\right)^{6}\times 6x = 42x\left(3x^{2}+5\right)^{6} $$

Expanding the bracket first would take a page and gain no marks.
:::

::: example Worked example 18.11 — three layers
**Problem.** Differentiate $y = \sin^{3}(2x+1)$.

**Solution.** Write $y = \left[\sin(2x+1)\right]^{3}$ and peel:

*Outer layer* (cube): $3\left[\sin(2x+1)\right]^{2}$.
*Middle layer* (sine): multiply by $\cos(2x+1)$.
*Inner layer* (linear): multiply by $2$.

$$ \frac{dy}{dx} = 3\sin^{2}(2x+1)\cdot\cos(2x+1)\cdot 2
= 6\sin^{2}(2x+1)\cos(2x+1) $$
:::

::: example Worked example 18.12 — chain rule with a surd inside
**Problem.** Differentiate $y = \tan\sqrt{x}$.

**Solution.** Put $u = \sqrt{x} = x^{1/2}$, so $y = \tan u$ and

$$ \frac{dy}{du} = \sec^{2}u, \qquad \frac{du}{dx} = \frac{1}{2\sqrt{x}} $$

$$ \frac{dy}{dx} = \sec^{2}\sqrt{x}\times\frac{1}{2\sqrt{x}}
= \frac{\sec^{2}\sqrt{x}}{2\sqrt{x}} $$
:::

::: example Worked example 18.12a — quotient and chain rules together
**Problem.** Differentiate $y = \dfrac{x}{\sqrt{1+x^{2}}}$.

**Solution.** It is quicker to write the surd as a power and use the product rule
than to use the quotient rule:

$$ y = x\left(1+x^{2}\right)^{-1/2} $$

Differentiate, applying the chain rule to the second factor:

$$ \frac{dy}{dx} = 1\cdot\left(1+x^{2}\right)^{-1/2}
+x\cdot\left(-\tfrac12\right)\left(1+x^{2}\right)^{-3/2}\cdot 2x $$

$$ = \left(1+x^{2}\right)^{-1/2}-x^{2}\left(1+x^{2}\right)^{-3/2} $$

Take out the lower power $\left(1+x^{2}\right)^{-3/2}$ as a common factor:

$$ = \left(1+x^{2}\right)^{-3/2}\left[\left(1+x^{2}\right)-x^{2}\right]
= \frac{1}{\left(1+x^{2}\right)^{3/2}} $$

Factorising out the **most negative** power is the standard way to tidy answers of
this kind; it is expected in the marking scheme.
:::

### Derivatives of trigonometric functions

$\sin x$ and $\cos x$ were differentiated from first principles above; the other
four follow by the quotient rule. For example, with $\sec x = 1/\cos x$,

$$ \frac{d}{dx}(\sec x) = \frac{\cos x\cdot 0-1\cdot(-\sin x)}{\cos^{2}x}
= \frac{\sin x}{\cos^{2}x} = \sec x\tan x $$

| $y$ | $\sin x$ | $\cos x$ | $\tan x$ | $\cot x$ | $\sec x$ | $\csc x$ |
|---|---|---|---|---|---|---|
| $dy/dx$ | $\cos x$ | $-\sin x$ | $\sec^{2}x$ | $-\csc^{2}x$ | $\sec x\tan x$ | $-\csc x\cot x$ |

::: memory The "co-" rule
Every function whose name begins with **co**- ($\cos$, $\cot$, $\csc$) has a
**minus sign** in its derivative. The other three do not.
:::

### Derivatives of inverse trigonometric functions

::: derivation Derivative of $\sin^{-1}x$
Let $y = \sin^{-1}x$, so $x = \sin y$ with $-\pi/2 \le y \le \pi/2$.
Differentiate $x = \sin y$ with respect to $y$:

$$ \frac{dx}{dy} = \cos y $$

Therefore $\dfrac{dy}{dx} = \dfrac{1}{\cos y}$. On the principal range
$\cos y \ge 0$, so

$$ \cos y = \sqrt{1-\sin^{2}y} = \sqrt{1-x^{2}} $$

$$ \frac{d}{dx}\left(\sin^{-1}x\right) = \frac{1}{\sqrt{1-x^{2}}}, \qquad |x|<1 $$

The same method gives all six. Note that
$\cos^{-1}x = \pi/2-\sin^{-1}x$, which explains at once why its derivative is the
negative of the one above.
:::

| $y$ | $\sin^{-1}x$ | $\cos^{-1}x$ | $\tan^{-1}x$ | $\cot^{-1}x$ | $\sec^{-1}x$ | $\csc^{-1}x$ |
|---|---|---|---|---|---|---|
| $dy/dx$ | $\dfrac{1}{\sqrt{1-x^{2}}}$ | $\dfrac{-1}{\sqrt{1-x^{2}}}$ | $\dfrac{1}{1+x^{2}}$ | $\dfrac{-1}{1+x^{2}}$ | $\dfrac{1}{|x|\sqrt{x^{2}-1}}$ | $\dfrac{-1}{|x|\sqrt{x^{2}-1}}$ |

::: tip Simplify before you differentiate
Inverse-trigonometric questions in NEB papers are usually designed to collapse
after a substitution such as $x = \tan\theta$ or $x = \sin\theta$. Look for the
patterns $\dfrac{2x}{1-x^{2}}$ ($= \tan2\theta$), $2x\sqrt{1-x^{2}}$
($= \sin2\theta$) and $\dfrac{1+x}{1-x}$ ($= \tan(\pi/4+\theta)$). One line of
trigonometry saves ten lines of algebra.
:::

::: example Worked example 18.13 — simplify first
**Problem.** Differentiate $y = \tan^{-1}\dfrac{1+x}{1-x}$.

**Solution.** Put $x = \tan\theta$, so $\theta = \tan^{-1}x$. Then

$$ \frac{1+x}{1-x} = \frac{1+\tan\theta}{1-\tan\theta}
= \frac{\tan\frac{\pi}{4}+\tan\theta}{1-\tan\frac{\pi}{4}\tan\theta}
= \tan\left(\frac{\pi}{4}+\theta\right) $$

Hence $y = \dfrac{\pi}{4}+\theta = \dfrac{\pi}{4}+\tan^{-1}x$, and differentiating,

$$ \frac{dy}{dx} = 0+\frac{1}{1+x^{2}} = \frac{1}{1+x^{2}} $$

The quotient-plus-chain route gives the same answer after half a page of algebra.
:::

::: example Worked example 18.14 — the $2x\sqrt{1-x^{2}}$ pattern
**Problem.** Differentiate $y = \sin^{-1}\left(2x\sqrt{1-x^{2}}\right)$ for
$|x| < \dfrac{1}{\sqrt{2}}$.

**Solution.** Put $x = \sin\theta$ with $-\pi/4 < \theta < \pi/4$. Then
$\sqrt{1-x^{2}} = \cos\theta$ and

$$ 2x\sqrt{1-x^{2}} = 2\sin\theta\cos\theta = \sin2\theta $$

Because $-\pi/2 < 2\theta < \pi/2$, we may write $y = \sin^{-1}(\sin2\theta) = 2\theta$,
that is $y = 2\sin^{-1}x$. Therefore

$$ \frac{dy}{dx} = \frac{2}{\sqrt{1-x^{2}}} $$

The restriction on $x$ matters: outside $|x|<1/\sqrt{2}$ the simplification
$\sin^{-1}(\sin2\theta) = 2\theta$ fails and the sign of the answer changes.
:::

### Derivatives of exponential and logarithmic functions

$$ \frac{d}{dx}e^{x} = e^{x}, \qquad \frac{d}{dx}a^{x} = a^{x}\ln a, \qquad
\frac{d}{dx}\ln x = \frac{1}{x}, \qquad
\frac{d}{dx}\log_{a}x = \frac{1}{x\ln a} $$

The last follows from the change of base $\log_a x = \dfrac{\ln x}{\ln a}$, in
which $\ln a$ is only a constant. Combined with the chain rule:

$$ \frac{d}{dx}e^{f(x)} = e^{f(x)}f'(x), \qquad
\frac{d}{dx}\ln f(x) = \frac{f'(x)}{f(x)} $$

::: example Worked example 18.15 — product of exponential and trigonometric
**Problem.** Differentiate $y = e^{x^{2}}\tan x$.

**Solution.** Product rule with $u = e^{x^{2}}$ and $v = \tan x$. By the chain
rule $u' = e^{x^{2}}\cdot 2x$, and $v' = \sec^{2}x$. So

$$ \frac{dy}{dx} = e^{x^{2}}\sec^{2}x+\tan x\cdot 2xe^{x^{2}}
= e^{x^{2}}\left(\sec^{2}x+2x\tan x\right) $$
:::

::: example Worked example 18.16 — a logarithm worth remembering
**Problem.** Show that $\dfrac{d}{dx}\ln(\sec x+\tan x) = \sec x$.

**Solution.** Using $\dfrac{d}{dx}\ln f = \dfrac{f'}{f}$ with
$f = \sec x+\tan x$,

$$ f'(x) = \sec x\tan x+\sec^{2}x = \sec x\left(\tan x+\sec x\right) $$

Therefore

$$ \frac{dy}{dx} = \frac{\sec x(\sec x+\tan x)}{\sec x+\tan x} = \sec x $$

The bracket cancels completely — which is why this particular logarithm appears
so often in integration (Unit 19).
:::

### Differentiating one function with respect to another

NEB papers often ask for $\dfrac{du}{dv}$ where both $u$ and $v$ are given
functions of $x$. Treat $x$ as a parameter, exactly as in §18.3:

$$ \frac{du}{dv} = \frac{du/dx}{dv/dx} $$

::: example Worked example 18.16a — one function with respect to another
**Problem.** (a) Differentiate $x^{2}$ with respect to $x^{3}$.
(b) Differentiate $\sin^{-1}\dfrac{2x}{1+x^{2}}$ with respect to $\tan^{-1}x$ for
$|x|<1$.

**Solution.** (a) Let $u = x^{2}$ and $v = x^{3}$. Then $\dfrac{du}{dx} = 2x$ and
$\dfrac{dv}{dx} = 3x^{2}$, so

$$ \frac{du}{dv} = \frac{2x}{3x^{2}} = \frac{2}{3x} \qquad (x \ne 0) $$

(b) Simplify first. Put $x = \tan\theta$ with $-\dfrac{\pi}{4}<\theta<\dfrac{\pi}{4}$;
then $\dfrac{2x}{1+x^{2}} = \dfrac{2\tan\theta}{1+\tan^{2}\theta} = \sin2\theta$, so

$$ u = \sin^{-1}(\sin2\theta) = 2\theta = 2\tan^{-1}x, \qquad v = \tan^{-1}x $$

Hence $\dfrac{du}{dx} = \dfrac{2}{1+x^{2}}$, $\dfrac{dv}{dx} = \dfrac{1}{1+x^{2}}$,
and

$$ \frac{du}{dv} = \frac{2/(1+x^{2})}{1/(1+x^{2})} = 2 $$
:::

### Logarithmic differentiation

When the **variable appears in the exponent**, or when a function is a long
product and quotient of powers, take natural logarithms of both sides first.

::: memory When to take logs
Use logarithmic differentiation if you see either
(i) $[f(x)]^{g(x)}$ — a variable base **and** a variable index, where neither the
power rule nor the exponential rule applies on its own; or
(ii) a product/quotient of four or more factors, where $\ln$ turns multiplication
into addition.
:::

::: example Worked example 18.17 — variable base and variable index
**Problem.** Differentiate $y = x^{\sin x}$, $x>0$.

**Solution.** Take natural logarithms of both sides:

$$ \ln y = \sin x\,\ln x $$

Differentiate both sides with respect to $x$. On the left, $\ln y$ is a function
of $y$ which is a function of $x$, so the chain rule gives
$\dfrac{1}{y}\dfrac{dy}{dx}$. On the right use the product rule:

$$ \frac{1}{y}\frac{dy}{dx} = \sin x\cdot\frac{1}{x}+\ln x\cdot\cos x $$

Multiply through by $y$ and substitute $y = x^{\sin x}$:

$$ \frac{dy}{dx} = x^{\sin x}\left(\frac{\sin x}{x}+\cos x\ln x\right) $$
:::

::: example Worked example 18.18 — a sum of two such terms
**Problem.** Differentiate $y = x^{x}+(\sin x)^{x}$.

**Solution.** A sum must be split: you cannot take the logarithm of a sum. Put
$u = x^{x}$ and $v = (\sin x)^{x}$, so $y = u+v$ and $y' = u'+v'$.

*For $u$:* $\ln u = x\ln x$, so
$\dfrac{1}{u}\dfrac{du}{dx} = x\cdot\dfrac1x+\ln x = 1+\ln x$, giving

$$ \frac{du}{dx} = x^{x}\left(1+\ln x\right) $$

*For $v$:* $\ln v = x\ln(\sin x)$, so

$$ \frac{1}{v}\frac{dv}{dx} = x\cdot\frac{\cos x}{\sin x}+\ln(\sin x)
= x\cot x+\ln(\sin x) $$

$$ \frac{dv}{dx} = (\sin x)^{x}\left[x\cot x+\ln(\sin x)\right] $$

Adding,

$$ \frac{dy}{dx} = x^{x}(1+\ln x)+(\sin x)^{x}\left[x\cot x+\ln(\sin x)\right] $$
:::

::: caution $x^{x}$ is neither a power nor an exponential
Writing $\dfrac{d}{dx}x^{x} = x\cdot x^{x-1}$ (power rule) or $x^{x}\ln x$
(exponential rule) are both wrong. The power rule needs a **constant index**; the
exponential rule needs a **constant base**. When both vary, only logarithmic
differentiation works.
:::

::: key Table of standard derivatives — learn all of it
| $y$ | $\dfrac{dy}{dx}$ | $y$ | $\dfrac{dy}{dx}$ |
|---|---|---|---|
| $c$ (constant) | $0$ | $\sin^{-1}x$ | $\dfrac{1}{\sqrt{1-x^{2}}}$ |
| $x^{n}$ | $nx^{n-1}$ | $\cos^{-1}x$ | $\dfrac{-1}{\sqrt{1-x^{2}}}$ |
| $\sqrt{x}$ | $\dfrac{1}{2\sqrt{x}}$ | $\tan^{-1}x$ | $\dfrac{1}{1+x^{2}}$ |
| $\dfrac{1}{x}$ | $-\dfrac{1}{x^{2}}$ | $\cot^{-1}x$ | $\dfrac{-1}{1+x^{2}}$ |
| $e^{x}$ | $e^{x}$ | $\sec^{-1}x$ | $\dfrac{1}{|x|\sqrt{x^{2}-1}}$ |
| $a^{x}$ | $a^{x}\ln a$ | $\csc^{-1}x$ | $\dfrac{-1}{|x|\sqrt{x^{2}-1}}$ |
| $\ln x$ | $\dfrac{1}{x}$ | $\sin x$ | $\cos x$ |
| $\log_{a}x$ | $\dfrac{1}{x\ln a}$ | $\cos x$ | $-\sin x$ |
| $\tan x$ | $\sec^{2}x$ | $\cot x$ | $-\csc^{2}x$ |
| $\sec x$ | $\sec x\tan x$ | $\csc x$ | $-\csc x\cot x$ |

And the four rules:

$$ (u\pm v)' = u'\pm v', \qquad (uv)' = uv'+vu', \qquad
\left(\frac{u}{v}\right)' = \frac{vu'-uv'}{v^{2}}, \qquad
\frac{dy}{dx} = \frac{dy}{du}\cdot\frac{du}{dx} $$
:::

## 18.3 Derivatives of parametric and implicit functions

So far $y$ has been given by an explicit formula $y = f(x)$. Two other
descriptions are just as common, and each has its own technique.

### Implicit differentiation

A relation such as $x^{2}+y^{2} = 25$ or $x^{3}+y^{3} = 3axy$ defines $y$ in terms
of $x$ without being solved for $y$. Such a relation is called **implicit**. We
can still find $dy/dx$ without solving, by differentiating every term of the
equation with respect to $x$ and treating $y$ as a function of $x$.

::: memory The one rule of implicit differentiation
Whenever you differentiate a term containing $y$, apply the chain rule and
multiply by $\dfrac{dy}{dx}$:

$$ \frac{d}{dx}\left(y^{2}\right) = 2y\frac{dy}{dx}, \qquad
\frac{d}{dx}\left(\sin y\right) = \cos y\frac{dy}{dx}, \qquad
\frac{d}{dx}(xy) = x\frac{dy}{dx}+y $$

Then collect all the $\dfrac{dy}{dx}$ terms on one side and factor.
:::

::: example Worked example 18.19 — the folium of Descartes
**Problem.** If $x^{3}+y^{3} = 3axy$, find $\dfrac{dy}{dx}$.

**Solution.** Differentiate each term with respect to $x$. The right-hand side
needs the product rule on $xy$:

$$ 3x^{2}+3y^{2}\frac{dy}{dx} = 3a\left(x\frac{dy}{dx}+y\right) $$

Divide by 3 and gather the $dy/dx$ terms on the left, the rest on the right:

$$ y^{2}\frac{dy}{dx}-ax\frac{dy}{dx} = ay-x^{2} $$

$$ \frac{dy}{dx}\left(y^{2}-ax\right) = ay-x^{2} $$

$$ \frac{dy}{dx} = \frac{ay-x^{2}}{y^{2}-ax} \qquad (y^{2} \ne ax) $$

The answer contains both $x$ and $y$; that is normal and expected for an implicit
curve.
:::

::: example Worked example 18.20 — implicit derivative at a point
**Problem.** Find the equations of the tangent and normal to the circle
$x^{2}+y^{2} = 25$ at the point $(3,4)$.

**Solution.** Differentiate implicitly:

$$ 2x+2y\frac{dy}{dx} = 0 \qquad\Longrightarrow\qquad \frac{dy}{dx} = -\frac{x}{y} $$

At $(3,4)$ the slope of the tangent is $m = -\dfrac{3}{4}$.

*Tangent:* $y-4 = -\dfrac34(x-3)$, i.e. $4y-16 = -3x+9$, so

$$ 3x+4y = 25 $$

*Normal:* its slope is $-1/m = \dfrac43$, so $y-4 = \dfrac43(x-3)$, giving
$3y-12 = 4x-12$, i.e.

$$ 4x-3y = 0 $$

As expected for a circle, the normal passes through the centre $(0,0)$.
:::

### Parametric differentiation

Sometimes both coordinates are given in terms of a third variable, the
**parameter**: $x = f(t)$, $y = g(t)$. Here the chain rule gives

$$ \frac{dy}{dx} = \frac{dy/dt}{dx/dt}
= \frac{\dot{y}}{\dot{x}}, \qquad \frac{dx}{dt} \ne 0 $$

Differentiate $y$ with respect to the parameter, differentiate $x$ with respect to
the parameter, then divide. Do **not** try to eliminate the parameter first unless
it is very easy; that is usually the longest route.

::: example Worked example 18.21 — the astroid
**Problem.** If $x = a\cos^{3}\theta$ and $y = a\sin^{3}\theta$, find
$\dfrac{dy}{dx}$.

**Solution.** Differentiate each coordinate with respect to $\theta$, using the
chain rule on the cubes:

$$ \frac{dx}{d\theta} = 3a\cos^{2}\theta\cdot(-\sin\theta)
= -3a\cos^{2}\theta\sin\theta $$

$$ \frac{dy}{d\theta} = 3a\sin^{2}\theta\cdot\cos\theta
= 3a\sin^{2}\theta\cos\theta $$

Divide:

$$ \frac{dy}{dx} = \frac{3a\sin^{2}\theta\cos\theta}{-3a\cos^{2}\theta\sin\theta}
= -\frac{\sin\theta}{\cos\theta} = -\tan\theta $$

Everything cancels except one ratio — a good sign that you have differentiated
correctly.
:::

### The second derivative of a parametric curve

::: caution $d^{2}y/dx^{2}$ is *not* $\ddot{y}/\ddot{x}$
The first derivative divides, but the second does not. You must differentiate
$dy/dx$ **with respect to $t$** and then divide by $dx/dt$ again:

$$ \frac{d^{2}y}{dx^{2}} = \frac{d}{dx}\left(\frac{dy}{dx}\right)
= \frac{\dfrac{d}{dt}\left(\dfrac{dy}{dx}\right)}{\dfrac{dx}{dt}} $$
:::

::: example Worked example 18.22 — first and second derivatives of a parabola
**Problem.** For $x = at^{2}$, $y = 2at$, find $\dfrac{dy}{dx}$ and
$\dfrac{d^{2}y}{dx^{2}}$.

**Solution.** First derivatives with respect to $t$:

$$ \frac{dx}{dt} = 2at, \qquad \frac{dy}{dt} = 2a $$

$$ \frac{dy}{dx} = \frac{2a}{2at} = \frac{1}{t} $$

For the second derivative, differentiate $1/t$ with respect to $t$ and then divide
by $dx/dt$:

$$ \frac{d}{dt}\left(\frac{1}{t}\right) = -\frac{1}{t^{2}} $$

$$ \frac{d^{2}y}{dx^{2}} = \frac{-1/t^{2}}{2at} = -\frac{1}{2at^{3}} $$

(The common wrong answer, $\ddot y/\ddot x = 0/2a = 0$, would say the parabola is a
straight line.)
:::

## 18.4 Higher order derivatives

Differentiating $f'$ gives the **second derivative** $f''$, differentiating again
gives the third, and so on. The standard notations are

$$ \frac{dy}{dx},\quad \frac{d^{2}y}{dx^{2}},\quad \frac{d^{3}y}{dx^{3}},\ \ldots,
\ \frac{d^{n}y}{dx^{n}} $$

or $y', y'', y''', y^{(4)}, \ldots, y^{(n)}$, or $y_1, y_2, y_3, \ldots, y_n$ —
the last is the form NEB papers most often use.

The physical meaning is familiar from Physics: if $s(t)$ is displacement, then
$s_1 = ds/dt$ is velocity and $s_2 = d^{2}s/dt^{2}$ is acceleration. In §18.8 the
second derivative will tell us how a curve bends.

### $n$-th derivatives of standard functions

Differentiate repeatedly and the pattern appears:

| $y$ | $y_n$ |
|---|---|
| $x^{m}$ | $m(m-1)(m-2)\cdots(m-n+1)\,x^{m-n}$ |
| $x^{n}$ | $n!$ |
| $e^{ax}$ | $a^{n}e^{ax}$ |
| $\ln x$ | $\dfrac{(-1)^{n-1}(n-1)!}{x^{n}}$ |
| $\dfrac{1}{x+a}$ | $\dfrac{(-1)^{n}\,n!}{(x+a)^{n+1}}$ |
| $\sin(ax+b)$ | $a^{n}\sin\left(ax+b+\dfrac{n\pi}{2}\right)$ |
| $\cos(ax+b)$ | $a^{n}\cos\left(ax+b+\dfrac{n\pi}{2}\right)$ |

The trigonometric entries work because each differentiation advances the angle by
a right angle: $\cos u = \sin\left(u+\frac{\pi}{2}\right)$.

::: example Worked example 18.23 — a third derivative
**Problem.** If $y = x^{3}\ln x$, find $y_3$.

**Solution.** Differentiate three times, using the product rule each time.

$$ y_1 = 3x^{2}\ln x+x^{3}\cdot\frac{1}{x} = 3x^{2}\ln x+x^{2} $$

$$ y_2 = 6x\ln x+3x^{2}\cdot\frac{1}{x}+2x = 6x\ln x+3x+2x = 6x\ln x+5x $$

$$ y_3 = 6\ln x+6x\cdot\frac{1}{x}+5 = 6\ln x+6+5 = 6\ln x+11 $$
:::

::: example Worked example 18.24 — proving a differential equation
**Problem.** If $y = e^{ax}\sin bx$, show that
$y_2-2ay_1+\left(a^{2}+b^{2}\right)y = 0$.

**Solution.** Differentiate once by the product rule:

$$ y_1 = ae^{ax}\sin bx+be^{ax}\cos bx = e^{ax}\left(a\sin bx+b\cos bx\right) $$

Differentiate again, product rule once more:

$$ y_2 = ae^{ax}(a\sin bx+b\cos bx)+e^{ax}(ab\cos bx-b^{2}\sin bx) $$

$$ = e^{ax}\left[\left(a^{2}-b^{2}\right)\sin bx+2ab\cos bx\right] $$

Now substitute into the left-hand side, writing $s = \sin bx$ and $c = \cos bx$:

$$ y_2-2ay_1+\left(a^{2}+b^{2}\right)y
= e^{ax}\left[\left(a^{2}-b^{2}\right)s+2abc-2a(as+bc)+\left(a^{2}+b^{2}\right)s\right] $$

The $c$ terms give $2abc-2abc = 0$; the $s$ terms give
$a^{2}-b^{2}-2a^{2}+a^{2}+b^{2} = 0$. Hence the whole expression is zero, as
required.
:::

::: example Worked example 18.25 — a standard NEB identity
**Problem.** If $y = A\sin mx+B\cos mx$, prove that $y_2+m^{2}y = 0$.

**Solution.**

$$ y_1 = Am\cos mx-Bm\sin mx $$

$$ y_2 = -Am^{2}\sin mx-Bm^{2}\cos mx = -m^{2}\left(A\sin mx+B\cos mx\right) = -m^{2}y $$

Therefore $y_2+m^{2}y = 0$. This is the equation of simple harmonic motion, which
is why $\sin$ and $\cos$ describe every oscillation in Physics.
:::

::: example Worked example 18.25a — an $n$-th derivative
**Problem.** If $y = \dfrac{1}{3x+2}$, find $y_n$.

**Solution.** Write $y = (3x+2)^{-1}$ and differentiate repeatedly, using the
chain rule each time (the inner derivative is always 3):

$$ y_1 = -1(3x+2)^{-2}\cdot3 = \frac{-3}{(3x+2)^{2}} $$

$$ y_2 = (-1)(-2)(3x+2)^{-3}\cdot3^{2} = \frac{2!\,3^{2}}{(3x+2)^{3}} $$

$$ y_3 = (-1)(-2)(-3)(3x+2)^{-4}\cdot3^{3} = \frac{-3!\,3^{3}}{(3x+2)^{4}} $$

Each step contributes one more factor of 3, one more factor from the falling index,
and one more sign change. The pattern is therefore

$$ y_n = \frac{(-1)^{n}\,n!\,3^{n}}{(3x+2)^{n+1}} $$

*Check with $n=4$:* the formula gives $4!\,3^{4}/(3x+2)^{5} = 1944/(3x+2)^{5}$,
which is what a fourth direct differentiation produces.
:::

## 18.5 Geometric interpretation of derivative

### Slope of the tangent

From §18.1, $f'(a)$ is the limit of the secant slopes at $x = a$, that is:

::: key The geometric meaning
$f'(a)$ is the **gradient (slope) of the tangent** to the curve $y = f(x)$ at the
point where $x = a$. Equivalently, $f'(a) = \tan\psi$, where $\psi$ is the angle
the tangent makes with the positive $x$-axis.
:::

The **normal** at a point is the line through that point perpendicular to the
tangent. Perpendicular lines have slopes whose product is $-1$, so

$$ m_{\text{tangent}} = f'(a), \qquad
m_{\text{normal}} = -\frac{1}{f'(a)} \qquad \left(f'(a) \ne 0\right) $$

### Equations of tangent and normal

At the point $\left(x_1, y_1\right)$ on the curve, with $m = f'(x_1)$:

$$ \text{Tangent: } y-y_1 = m\left(x-x_1\right), \qquad
\text{Normal: } y-y_1 = -\frac{1}{m}\left(x-x_1\right) $$

Special cases: if $f'(x_1) = 0$ the tangent is horizontal ($y = y_1$) and the
normal is vertical ($x = x_1$); if $f'(x_1)$ is infinite the tangent is vertical
and the normal horizontal.

```figure caption="Tangent and normal to $y=x^3-3x+2$ at $P(2,4)$. The tangent has slope $f'(2)=9$; the normal, being perpendicular, has slope $-1/9$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,3.2))
f  = lambda z: z**3 - 3*z + 2
fp = lambda z: 3*z**2 - 3
x = np.linspace(-1.2, 3.0, 500)
ax.plot(x, f(x), color=ACCENT, lw=2.2, zorder=4, label='$y=x^3-3x+2$')
x0, y0 = 2.0, f(2.0); m = fp(2.0)
tt = np.array([1.05, 2.55])
ax.plot(tt, y0 + m*(tt-x0), color='#d9534f', lw=1.7, zorder=5, label='tangent, $m=9$')
nn = np.array([-0.4, 3.0])
ax.plot(nn, y0 - (1/m)*(nn-x0), color='#2e8b57', lw=1.7, ls='--', zorder=5,
        label='normal, $m=-1/9$')
ax.plot([x0],[y0], 'o', color=INK, ms=6, zorder=7)
ax.annotate('$P(2,4)$', (x0,y0), textcoords='offset points', xytext=(-48,2),
            color=INK, fontsize=9.5)
ax.axhline(0, color=MUTED, lw=.8); ax.axvline(0, color=MUTED, lw=.8)
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.set_xlim(-1.2,3.0); ax.set_ylim(-3,10)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.35)
ax.legend(loc='upper left', fontsize=8.2)
```

::: example Worked example 18.26 — tangent and normal
**Problem.** Find the equations of the tangent and the normal to the curve
$y = x^{3}-3x+2$ at the point where $x = 2$.

**Solution.** *Point.* $y = 2^{3}-3(2)+2 = 8-6+2 = 4$, so $P$ is $(2,4)$.

*Slope.* $\dfrac{dy}{dx} = 3x^{2}-3$, so $m = 3(4)-3 = 9$.

*Tangent.* $y-4 = 9(x-2)$, i.e.

$$ 9x-y-14 = 0 $$

*Normal.* Slope $= -\dfrac19$, so $y-4 = -\dfrac19(x-2)$. Multiplying by 9,
$9y-36 = -x+2$, i.e.

$$ x+9y-38 = 0 $$
:::

### Angle between two curves

The angle between two curves at a common point is the angle between their tangents
there. If the slopes are $m_1$ and $m_2$,

$$ \tan\theta = \left|\frac{m_1-m_2}{1+m_1m_2}\right| $$

The curves are **orthogonal** (perpendicular) if $m_1m_2 = -1$, and **touch** each
other if $m_1 = m_2$.

::: example Worked example 18.27 — angle of intersection
**Problem.** Find the angle between the curves $y = x^{2}$ and $y^{2} = x$ at the
point $(1,1)$.

**Solution.** *First curve.* $y = x^{2}$ gives $\dfrac{dy}{dx} = 2x$, so
$m_1 = 2$ at $(1,1)$.

*Second curve.* $y^{2} = x$; differentiating implicitly,
$2y\dfrac{dy}{dx} = 1$, so $\dfrac{dy}{dx} = \dfrac{1}{2y}$ and
$m_2 = \dfrac12$ at $(1,1)$.

$$ \tan\theta = \left|\frac{2-\frac12}{1+2\cdot\frac12}\right|
= \left|\frac{3/2}{2}\right| = \frac{3}{4} $$

$$ \theta = \tan^{-1}\frac34 = 36^{\circ}52' \approx 36.87^{\circ} $$
:::

### The derivative as a rate of change

The tangent picture is geometric, but the same limit has a physical reading. If
$y$ depends on $x$, then $\dfrac{dy}{dx}$ is the **rate at which $y$ changes per
unit change in $x$**, measured at that instant. A positive value means $y$ grows
as $x$ grows; a large magnitude means it grows quickly.

This is why the derivative appears everywhere outside mathematics: with $s(t)$ a
displacement, $\dfrac{ds}{dt}$ is velocity and $\dfrac{d^{2}s}{dt^{2}}$ is
acceleration; with $C(x)$ a total cost, $\dfrac{dC}{dx}$ is the marginal cost of
one more unit; with $A(r)$ an area, $\dfrac{dA}{dr}$ tells how the area responds
to a change in radius. Chaining two such rates gives
$\dfrac{dA}{dt} = \dfrac{dA}{dr}\cdot\dfrac{dr}{dt}$.

::: example Worked example 18.27a — velocity and acceleration
**Problem.** A particle moves along a straight line so that its displacement after
$t$ seconds is $s = t^{3}-6t^{2}+9t+4$ metres. Find its velocity and acceleration
at time $t$, the times at which it is momentarily at rest, and its acceleration at
each of those times.

**Solution.** Velocity is the first derivative and acceleration the second:

$$ v = \frac{ds}{dt} = 3t^{2}-12t+9 = 3(t-1)(t-3) $$

$$ a = \frac{d^{2}s}{dt^{2}} = 6t-12 = 6(t-2) $$

The particle is at rest when $v = 0$, i.e. at $t = 1\ \text{s}$ and
$t = 3\ \text{s}$.

At $t = 1$: $a = 6(1-2) = -6\ \text{m s}^{-2}$ (it is about to move backwards).
At $t = 3$: $a = 6(3-2) = +6\ \text{m s}^{-2}$ (it is about to move forwards).

The displacements there are $s(1) = 8\ \text{m}$ and $s(3) = 4\ \text{m}$ — the
particle advances, reverses, then advances again.
:::

::: example Worked example 18.27b — a rate of change of area
**Problem.** Oil spilled on the Koshi river spreads in a circle whose radius grows
at $2\ \text{cm s}^{-1}$. How fast is the area of the slick increasing at the
moment when the radius is $10\ \text{cm}$?

**Solution.** The area of a circle is $A = \pi r^{2}$, and $r$ itself changes with
time, so by the chain rule

$$ \frac{dA}{dt} = \frac{dA}{dr}\cdot\frac{dr}{dt} = 2\pi r\cdot\frac{dr}{dt} $$

Substituting $r = 10\ \text{cm}$ and $\dfrac{dr}{dt} = 2\ \text{cm s}^{-1}$,

$$ \frac{dA}{dt} = 2\pi(10)(2) = 40\pi \approx 125.7\ \text{cm}^{2}\,\text{s}^{-1} $$
:::

### Reading $f'$ off the graph of $f$

Because $f'$ is the slope, the sign of $f'$ and the shape of $f$ are locked
together: where the curve climbs, $f'$ is above the axis; where it falls, $f'$ is
below; at a turning point the curve is momentarily flat and $f'$ crosses zero.

```figure caption="Top: $f(x)=x^3-3x$. Bottom: its derivative $f'(x)=3x^2-3$. $f$ rises exactly where $f'>0$, falls where $f'<0$, and turns where $f'=0$ (at $x=-1$ and $x=1$)."
import numpy as np, matplotlib.pyplot as plt
fig, (a1, a2) = plt.subplots(2, 1, figsize=(4.9,3.4), sharex=True,
                             gridspec_kw=dict(hspace=0.12))
x = np.linspace(-2.2, 2.2, 600)
f  = x**3 - 3*x
fp = 3*x**2 - 3
a1.plot(x, f, color=ACCENT, lw=2.1)
a1.axhline(0, color=MUTED, lw=.8)
for xc in (-1, 1):
    a1.axvline(xc, color=GRID, lw=1.0)
    a2.axvline(xc, color=GRID, lw=1.0)
    a1.plot([xc],[xc**3-3*xc], 'o', color='#d9534f', ms=5.5, zorder=5)
a1.annotate('rises', (-1.7, -1.7**3+3*1.7), textcoords='offset points',
            xytext=(-6,-16), color='#2e8b57', fontsize=8.6)
a1.annotate('falls', (0, 0), textcoords='offset points', xytext=(-12,8),
            color='#d9534f', fontsize=8.6)
a1.annotate('rises', (1.75, 1.75**3-3*1.75), textcoords='offset points',
            xytext=(-32,4), color='#2e8b57', fontsize=8.6)
a1.set_ylabel('$f(x)$'); a1.set_ylim(-4.5,4.5)
a2.plot(x, fp, color='#b8860b', lw=2.1)
a2.axhline(0, color=MUTED, lw=.8)
a2.fill_between(x, 0, fp, where=(fp > 0), color='#2e8b57', alpha=0.16)
a2.fill_between(x, 0, fp, where=(fp < 0), color='#d9534f', alpha=0.16)
a2.annotate("$f'>0$", (-1.75, 5.2), color='#2e8b57', fontsize=8.8, ha='center')
a2.annotate("$f'<0$", (0, -2.0), color='#d9534f', fontsize=8.8, ha='center')
a2.annotate("$f'>0$", (1.75, 5.2), color='#2e8b57', fontsize=8.8, ha='center')
a2.set_ylabel("$f'(x)$"); a2.set_xlabel('$x$'); a2.set_ylim(-4.5,9.5)
for a in (a1, a2):
    a.set_xlim(-2.2,2.2)
    a.spines[['top','right']].set_visible(False)
    a.grid(True, alpha=.3)
a2.set_xticks([-2,-1,0,1,2])
```

::: tip Sign of $f'$, shape of $f$
Reading a graph question backwards is a standard Group A trick: you are shown the
graph of $f'$ and asked about $f$. Remember only this: $f'$ **above** the axis
means $f$ is going **up**; $f'$ **crossing** the axis means $f$ has a turning
point; $f'$ itself increasing means $f$ bends upwards (§18.8).
:::

## 18.6 Monotonicity of a function; intervals of increase and decrease

A function is **monotonic** on an interval if it moves in only one direction
there — always up, or always down.

::: definition Increasing and decreasing
Let $f$ be defined on an interval $I$ and let $x_1 < x_2$ be any two points of $I$.

- $f$ is **increasing** on $I$ if $f(x_1) \le f(x_2)$, and **strictly increasing**
  if $f(x_1) < f(x_2)$.
- $f$ is **decreasing** on $I$ if $f(x_1) \ge f(x_2)$, and **strictly decreasing**
  if $f(x_1) > f(x_2)$.
:::

Since $f'$ is the slope of the tangent, the test is immediate.

::: key The monotonicity test
Let $f$ be differentiable on an interval $I$. Then on that interval:

$$ f'(x) > 0 \ \text{for all } x \in I \;\Longrightarrow\; f \text{ is strictly increasing on } I $$

$$ f'(x) < 0 \ \text{for all } x \in I \;\Longrightarrow\; f \text{ is strictly decreasing on } I $$

$$ f'(x) = 0 \ \text{for all } x \in I \;\Longrightarrow\; f \text{ is constant on } I $$
:::

### The procedure

::: memory Finding intervals of increase and decrease
1. Compute $f'(x)$ and **factorise** it completely.
2. Solve $f'(x) = 0$; add any point where $f'$ is undefined. These are the
   **critical points**; mark them on a number line.
3. The critical points cut the line into open intervals. Test the **sign** of
   $f'$ in each interval, using one convenient value or the sign of each factor.
4. Report: increasing where $f' > 0$, decreasing where $f' < 0$.
:::

::: example Worked example 18.28 — intervals of increase and decrease
**Problem.** Find the intervals in which $f(x) = x^{3}-3x^{2}-9x+5$ is increasing
and in which it is decreasing.

**Solution.** *Step 1.* Differentiate and factorise:

$$ f'(x) = 3x^{2}-6x-9 = 3\left(x^{2}-2x-3\right) = 3(x-3)(x+1) $$

*Step 2.* $f'(x) = 0$ at $x = -1$ and $x = 3$. These cut the real line into three
intervals.

*Step 3.* Test the sign of each factor:

| Interval | $(x+1)$ | $(x-3)$ | $f'(x)$ | Behaviour |
|---|---|---|---|---|
| $x < -1$ | $-$ | $-$ | $+$ | increasing |
| $-1 < x < 3$ | $+$ | $-$ | $-$ | decreasing |
| $x > 3$ | $+$ | $+$ | $+$ | increasing |

*Step 4.* $f$ is increasing on $(-\infty,-1)$ and on $(3,\infty)$, and decreasing
on $(-1,3)$.

A quick numerical check: $f'(0) = -9 < 0$, which confirms the middle row.
:::

```figure caption="$f(x)=x^3-3x^2-9x+5$. The curve rises on $(-\infty,-1)$, falls on $(-1,3)$ and rises again on $(3,\infty)$ — exactly where $f'(x)=3(x-3)(x+1)$ is positive, negative and positive."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,3.0))
f = lambda z: z**3 - 3*z**2 - 9*z + 5
x = np.linspace(-3.0, 5.2, 700)
ax.axvspan(-3.0, -1, color='#2e8b57', alpha=0.10)
ax.axvspan(-1, 3, color='#d9534f', alpha=0.10)
ax.axvspan(3, 5.2, color='#2e8b57', alpha=0.10)
ax.plot(x, f(x), color=ACCENT, lw=2.2, zorder=4)
for xc in (-1, 3):
    ax.plot([xc],[f(xc)], 'o', color=INK, ms=5.5, zorder=6)
    ax.axvline(xc, color=MUTED, lw=.9, ls=':')
ax.annotate('$(-1,\\ 10)$', (-1,f(-1)), textcoords='offset points', xytext=(-16,8),
            color=INK, fontsize=8.8)
ax.annotate('$(3,\\ -22)$', (3,f(3)), textcoords='offset points', xytext=(4,-14),
            color=INK, fontsize=8.8)
ax.annotate('increasing', (-2.1, -12), color='#2e8b57', fontsize=8.8, ha='center')
ax.annotate('decreasing', (1.0, -12), color='#d9534f', fontsize=8.8, ha='center')
ax.annotate('increasing', (4.3, -12), color='#2e8b57', fontsize=8.8, ha='center')
ax.axhline(0, color=MUTED, lw=.8)
ax.set_xlabel('$x$'); ax.set_ylabel('$f(x)$')
ax.set_xlim(-3.0,5.2); ax.set_ylim(-30,20)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.3)
```

::: example Worked example 18.29 — monotonicity of a trigonometric function
**Problem.** Show that $f(x) = \sin x$ is strictly increasing on
$\left(-\dfrac{\pi}{2},\dfrac{\pi}{2}\right)$ and strictly decreasing on
$\left(\dfrac{\pi}{2},\dfrac{3\pi}{2}\right)$.

**Solution.** $f'(x) = \cos x$.

On $\left(-\dfrac{\pi}{2},\dfrac{\pi}{2}\right)$ the cosine is positive, so
$f' > 0$ and $\sin x$ is strictly increasing there.

On $\left(\dfrac{\pi}{2},\dfrac{3\pi}{2}\right)$ the cosine is negative, so
$f' < 0$ and $\sin x$ is strictly decreasing there.

This is exactly why $\sin^{-1}$ is defined with the principal range
$\left[-\dfrac{\pi}{2},\dfrac{\pi}{2}\right]$: that is the largest interval on
which $\sin$ is one-to-one.
:::

::: caution A zero derivative at one isolated point is harmless
$f(x) = x^{3}$ has $f'(0) = 0$, yet $f$ is strictly increasing on all of
$\mathbb{R}$, because $f' = 3x^{2} > 0$ everywhere else. "Increasing" concerns an
**interval**, not a single point, so do not break an interval at a point where
$f'$ touches zero without changing sign.
:::

## 18.7 Extreme values (maxima and minima)

### Critical points

::: definition Local extremes
$f$ has a **local (relative) maximum** at $x = c$ if $f(c) \ge f(x)$ for all $x$
in some open interval around $c$; a **local minimum** if $f(c) \le f(x)$ there.
The value $f(c)$ is the extreme value; the point $\left(c, f(c)\right)$ is a
**turning point**.

A point $c$ where $f'(c) = 0$ or where $f'(c)$ does not exist is called a
**critical point** (or stationary point when $f'(c) = 0$).
:::

::: key Fermat's necessary condition
If $f$ has a local extreme at an interior point $c$ and $f'(c)$ exists, then
$f'(c) = 0$.

The converse is false. $f'(c) = 0$ only makes $c$ a **candidate**: for
$f(x) = x^{3}$ we have $f'(0) = 0$, but $0$ is neither a maximum nor a minimum —
it is a point of inflection. A test is always needed.
:::

### The first derivative test

Examine how the **sign** of $f'$ changes as $x$ passes through the critical point
$c$, moving from left to right:

| Sign change of $f'$ at $c$ | Conclusion |
|---|---|
| $+$ to $-$ | local **maximum** at $c$ |
| $-$ to $+$ | local **minimum** at $c$ |
| no change ($+,+$ or $-,-$) | neither — a point of inflection |

The picture is easy to remember: the curve goes up then down over a hill (maximum),
or down then up through a valley (minimum).

### The second derivative test

Often faster, when $f''$ is easy to compute.

::: key Second derivative test
Suppose $f'(c) = 0$. Then

$$ f''(c) < 0 \;\Longrightarrow\; \text{local maximum at } c $$

$$ f''(c) > 0 \;\Longrightarrow\; \text{local minimum at } c $$

$$ f''(c) = 0 \;\Longrightarrow\; \text{test fails — go back to the first derivative test} $$

Memory hook: $f'' < 0$ means the curve is bending **downwards** like a frown, so
the stationary point is a peak; $f'' > 0$ bends **upwards** like a smile, so it is
a valley.
:::

::: example Worked example 18.30 — maxima and minima of a cubic
**Problem.** Find the maximum and minimum values of
$f(x) = 2x^{3}-15x^{2}+36x+10$.

**Solution.** *Stationary points.*

$$ f'(x) = 6x^{2}-30x+36 = 6\left(x^{2}-5x+6\right) = 6(x-2)(x-3) $$

Setting $f'(x) = 0$ gives $x = 2$ and $x = 3$.

*Second derivative test.*

$$ f''(x) = 12x-30 $$

At $x = 2$: $f''(2) = 24-30 = -6 < 0$, so there is a local **maximum**.
At $x = 3$: $f''(3) = 36-30 = 6 > 0$, so there is a local **minimum**.

*Extreme values.*

$$ f(2) = 2(8)-15(4)+36(2)+10 = 16-60+72+10 = 38 $$

$$ f(3) = 2(27)-15(9)+36(3)+10 = 54-135+108+10 = 37 $$

So the maximum value is $38$ at $x = 2$ and the minimum value is $37$ at $x = 3$.

Note that the local maximum value $38$ exceeds the local minimum value $37$, as it
must for a cubic — but neither is a global extreme, since $f \to \pm\infty$ as
$x \to \pm\infty$.
:::

```figure caption="$f(x)=2x^3-15x^2+36x+10$ has a local maximum $38$ at $x=2$ and a local minimum $37$ at $x=3$. The tangent is horizontal at both turning points."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,3.0))
f = lambda z: 2*z**3 - 15*z**2 + 36*z + 10
x = np.linspace(0.6, 4.4, 600)
ax.plot(x, f(x), color=ACCENT, lw=2.2, zorder=4)
for xc, lab, col, off in [(2, 'local max $(2,\\ 38)$', '#d9534f', (-6,12)),
                          (3, 'local min $(3,\\ 37)$', '#2e8b57', (2,-22))]:
    ax.plot([xc],[f(xc)], 'o', color=col, ms=6, zorder=6)
    ax.plot([xc-0.55, xc+0.55], [f(xc)]*2, color=col, lw=1.4, ls='--', zorder=5)
    ax.annotate(lab, (xc,f(xc)), textcoords='offset points', xytext=off,
                color=col, fontsize=8.8)
ax.set_xlabel('$x$'); ax.set_ylabel('$f(x)$')
ax.set_xlim(0.6,4.4); ax.set_ylim(28,46)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.35)
```

### Absolute extremes on a closed interval

On a closed interval $[a,b]$ a continuous function always attains a greatest and a
least value. To find them, evaluate $f$ at **every critical point inside the
interval and at both endpoints**, then pick the largest and smallest of those
numbers. The endpoints are the step students forget.

::: example Worked example 18.31 — absolute extremes
**Problem.** Find the absolute maximum and minimum of $f(x) = x^{3}-3x$ on
$[-2,3]$.

**Solution.** $f'(x) = 3x^{2}-3 = 3(x-1)(x+1)$, zero at $x = \pm1$; both lie in
$[-2,3]$.

Evaluate at the two critical points and the two endpoints:

| $x$ | $-2$ | $-1$ | $1$ | $3$ |
|---|---|---|---|---|
| $f(x)$ | $-2$ | $2$ | $-2$ | $18$ |

The absolute maximum is $18$, at the endpoint $x = 3$; the absolute minimum is
$-2$, attained twice, at $x = -2$ and at $x = 1$.
:::

### Applied maxima and minima

::: memory Method for an optimisation word problem
1. Draw a figure and name the variables.
2. Write the quantity to be optimised as a formula.
3. Use the given constraint to reduce it to **one** variable, and state that
   variable's physical range.
4. Differentiate, set the derivative to zero, solve.
5. Confirm maximum or minimum with the second derivative test.
6. Answer the question actually asked, with units.
:::

```figure caption="An open box made by cutting a square of side $x$ from each corner of a $24 \times 9$ cm sheet and folding up the flaps. Base $ (24-2x) \times (9-2x)$, height $x$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(4.8,2.6))
W, H, c = 24.0, 9.0, 2.6
ax.add_patch(Rectangle((0,0), W, H, fill=False, ec=INK, lw=1.6))
ax.add_patch(Rectangle((c,c), W-2*c, H-2*c, fc=ACCENT, alpha=0.12, ec=ACCENT,
                       lw=1.4, ls='--'))
for (px,py) in [(0,0),(W-c,0),(0,H-c),(W-c,H-c)]:
    ax.add_patch(Rectangle((px,py), c, c, fc='#d9534f', alpha=0.28, ec='#d9534f', lw=1.2))
ax.annotate('$x$', (c/2, c/2), ha='center', va='center', fontsize=9, color='#a33')
ax.annotate('squares cut away', (c/2, H), textcoords='offset points',
            xytext=(6,16), ha='left', fontsize=8.2, color='#a33',
            arrowprops=dict(arrowstyle='-|>', color='#a33', lw=1.0, mutation_scale=9))
ax.annotate('base of the box', (W/2, H/2), ha='center', va='center',
            fontsize=9, color=ACCENT)
ax.annotate('', xy=(0,-1.1), xytext=(W,-1.1),
            arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=1.0, mutation_scale=9))
ax.annotate('24 cm', (W/2,-1.1), ha='center', va='top', fontsize=8.6, color=MUTED)
ax.annotate('', xy=(-1.1,0), xytext=(-1.1,H),
            arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=1.0, mutation_scale=9))
ax.annotate('9 cm', (-1.5,H/2), ha='right', va='center', fontsize=8.6, color=MUTED)
ax.set_xlim(-4.5, W+1); ax.set_ylim(-3.2, H+3.4)
ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 18.32 — the open box
**Problem.** From each corner of a rectangular sheet of tin $24\ \text{cm}$ by
$9\ \text{cm}$, a square of side $x$ is cut away and the flaps are folded up to
make an open box. Find $x$ so that the volume is greatest, and find that volume.

**Solution.** After cutting, the base measures $(24-2x)$ by $(9-2x)$ and the
height is $x$, so

$$ V = x(24-2x)(9-2x) = 4x^{3}-66x^{2}+216x $$

with $0 < x < 4.5$ (the shorter side must stay positive).

Differentiate:

$$ \frac{dV}{dx} = 12x^{2}-132x+216 = 12\left(x^{2}-11x+18\right) = 12(x-2)(x-9) $$

Setting $dV/dx = 0$ gives $x = 2$ or $x = 9$. Only $x = 2$ lies in the allowed
range.

*Check.* $\dfrac{d^{2}V}{dx^{2}} = 24x-132$, and at $x = 2$ this is
$48-132 = -84 < 0$, so the volume is a maximum.

*Answer.* $x = 2\ \text{cm}$, and

$$ V_{\max} = 2 \times 20 \times 5 = 200\ \text{cm}^{3} $$
:::

::: example Worked example 18.33 — a fencing problem
**Problem.** A farmer in Chitwan has $100\ \text{m}$ of fencing and wants to
enclose a rectangular plot against a long straight wall, which needs no fence.
What dimensions give the greatest area?

**Solution.** Let the two sides perpendicular to the wall be $x$ metres each; the
side parallel to the wall is then $100-2x$ metres. The area is

$$ A = x(100-2x) = 100x-2x^{2}, \qquad 0 < x < 50 $$

$$ \frac{dA}{dx} = 100-4x = 0 \;\Longrightarrow\; x = 25 $$

$$ \frac{d^{2}A}{dx^{2}} = -4 < 0 \quad\text{(maximum)} $$

So the plot is $25\ \text{m}$ by $50\ \text{m}$, with maximum area
$A = 25 \times 50 = 1250\ \text{m}^{2}$.
:::

::: caution Do not stop at $x$
Optimisation questions usually ask for the maximum **value**, or for the
dimensions, not for the value of $x$ that produces it. Finish the arithmetic and
attach the unit — cm³, m², rupees. Marks are lost here every year.
:::

## 18.8 Concavity and points of inflection

The first derivative says whether a curve is going up or down. The second
derivative says **which way it bends**.

::: definition Concavity
A curve is **concave upward** (convex) on an interval if it lies **above** all of
its tangents there — it holds water, like a smile. It is **concave downward** if
it lies **below** its tangents — like a frown.

$$ f''(x) > 0 \ \text{on } I \;\Longrightarrow\; f \text{ is concave upward on } I $$

$$ f''(x) < 0 \ \text{on } I \;\Longrightarrow\; f \text{ is concave downward on } I $$
:::

The reason is simple: $f'' > 0$ means $f'$ (the slope) is increasing, so the
tangent keeps turning anticlockwise and the curve bends upwards.

::: definition Point of inflection
A **point of inflection** is a point on the curve at which the concavity
**changes** — from upward to downward or the reverse.

At such a point $f''(x) = 0$ (or $f''$ fails to exist), **and** $f''$ must change
sign there. The condition $f''(c) = 0$ alone is not enough: for $f(x) = x^{4}$ we
have $f''(0) = 0$, yet $f'' = 12x^{2} \ge 0$ on both sides, so the curve is
concave upward throughout and $(0,0)$ is not an inflection point.
:::

```figure caption="$f(x)=x^4-4x^3$ is concave up for $x<0$ and $x>2$ and concave down between. The concavity changes at $(0,0)$ and $(2,-16)$, so both are points of inflection."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9,3.1))
f = lambda z: z**4 - 4*z**3
x = np.linspace(-1.2, 3.6, 700)
ax.axvspan(-1.2, 0, color='#2e8b57', alpha=0.10)
ax.axvspan(0, 2, color='#d9534f', alpha=0.10)
ax.axvspan(2, 3.6, color='#2e8b57', alpha=0.10)
ax.plot(x, f(x), color=ACCENT, lw=2.2, zorder=4)
for xc, lab, off in [(0, '$(0,0)$', (6,10)), (2, '$(2,-16)$', (6,4))]:
    ax.plot([xc],[f(xc)], 'o', color='#b8860b', ms=6.5, zorder=6)
    ax.annotate(lab, (xc,f(xc)), textcoords='offset points', xytext=off,
                color=INK, fontsize=8.8)
ax.annotate('concave up', (-0.75, -14), color='#2e8b57', fontsize=8.4, ha='center')
ax.annotate('concave down', (1.0, 6), color='#d9534f', fontsize=8.4, ha='center')
ax.annotate('concave up', (3.0, 6), color='#2e8b57', fontsize=8.4, ha='center')
ax.annotate('points of inflection', (2, -16), textcoords='offset points',
            xytext=(-42,-26), color='#b8860b', fontsize=8.4,
            arrowprops=dict(arrowstyle='-|>', color='#b8860b', lw=1.0, mutation_scale=9))
ax.axhline(0, color=MUTED, lw=.8)
ax.set_xlabel('$x$'); ax.set_ylabel('$f(x)$')
ax.set_xlim(-1.2,3.6); ax.set_ylim(-32,18)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.3)
```

::: example Worked example 18.34 — concavity and inflection
**Problem.** Find the intervals of concavity and the points of inflection of
$f(x) = x^{4}-4x^{3}$.

**Solution.**

$$ f'(x) = 4x^{3}-12x^{2}, \qquad f''(x) = 12x^{2}-24x = 12x(x-2) $$

$f''(x) = 0$ at $x = 0$ and $x = 2$. Test the sign of $f''$ in the three
intervals:

| Interval | $12x$ | $(x-2)$ | $f''$ | Concavity |
|---|---|---|---|---|
| $x < 0$ | $-$ | $-$ | $+$ | upward |
| $0 < x < 2$ | $+$ | $-$ | $-$ | downward |
| $x > 2$ | $+$ | $+$ | $+$ | upward |

The sign of $f''$ changes at both $x = 0$ and $x = 2$, so both give points of
inflection. Their coordinates:

$$ f(0) = 0, \qquad f(2) = 16-32 = -16 $$

Inflection points: $(0,0)$ and $(2,-16)$. The curve is concave upward on
$(-\infty,0)$ and $(2,\infty)$, concave downward on $(0,2)$.

Note that $x = 0$ is also a stationary point, since $f'(0) = 0$, yet it is **not**
a turning point: $f' = 4x^{2}(x-3)$ is negative on both sides of $0$. This is
precisely the case where the second derivative test fails and the first derivative
test rescues you.
:::

::: example Worked example 18.35 — a complete analysis
**Problem.** For $f(x) = x^{3}-6x^{2}+9x+1$, find the intervals of increase and
decrease, the local extreme values, and the point of inflection.

**Solution.** *Derivatives.*

$$ f'(x) = 3x^{2}-12x+9 = 3(x-1)(x-3), \qquad f''(x) = 6x-12 = 6(x-2) $$

*Monotonicity.* $f' > 0$ for $x < 1$ and for $x > 3$; $f' < 0$ for $1 < x < 3$.
So $f$ increases on $(-\infty,1)$ and $(3,\infty)$ and decreases on $(1,3)$.

*Extremes.* $f''(1) = -6 < 0$, so $x = 1$ gives a local maximum
$f(1) = 1-6+9+1 = 5$. And $f''(3) = 6 > 0$, so $x = 3$ gives a local minimum
$f(3) = 27-54+27+1 = 1$.

*Inflection.* $f''(x) = 0$ at $x = 2$, and $f''$ changes from negative to positive
there, so $(2, f(2)) = (2,3)$ is a point of inflection. Notice that it sits exactly
midway between the two turning points — true for every cubic.
:::

::: tip Curve sketching in six lines
Examiners often bundle §18.6–§18.8 into one Group C question. Answer in this
order and you cannot leave anything out: (1) intercepts, (2) $f'$ factorised,
(3) intervals of increase/decrease, (4) turning points with the second derivative
test, (5) $f''$ and intervals of concavity, (6) points of inflection. Then sketch.
:::

## Chapter summary

- **First principle:** $f'(x) = \lim_{h\to0}\dfrac{f(x+h)-f(x)}{h}$. Four steps —
  form $f(x+h)$, subtract, divide by $h$, take the limit. The trick in step 2 is
  expansion (polynomials), the conjugate (surds), a common denominator
  (fractions), sum-to-product (trigonometric) or a standard limit (exponential and
  logarithmic).
- Differentiable $\Rightarrow$ continuous, but not the reverse: $|x|$ has a corner
  at $0$ where the left and right derivatives are $-1$ and $+1$.
- **Rules:** $(u\pm v)' = u'\pm v'$; $(uv)' = uv'+vu'$;
  $\left(\frac uv\right)' = \frac{vu'-uv'}{v^{2}}$; chain rule
  $\frac{dy}{dx} = \frac{dy}{du}\cdot\frac{du}{dx}$.
- **Standard derivatives:** $x^{n} \to nx^{n-1}$; $e^{x} \to e^{x}$;
  $a^{x} \to a^{x}\ln a$; $\ln x \to 1/x$; $\sin x \to \cos x$;
  $\cos x \to -\sin x$; $\tan x \to \sec^{2}x$; $\sin^{-1}x \to 1/\sqrt{1-x^{2}}$;
  $\tan^{-1}x \to 1/(1+x^{2})$. Every "co-" function carries a minus sign.
- **Logarithmic differentiation** for $[f(x)]^{g(x)}$ and for long
  products/quotients: take $\ln$ of both sides, then differentiate, remembering
  $\frac{d}{dx}\ln y = \frac1y\frac{dy}{dx}$.
- **Implicit:** differentiate every term in $x$, attaching $\frac{dy}{dx}$ to each
  $y$-term, then collect and factor. **Parametric:**
  $\frac{dy}{dx} = \dfrac{dy/dt}{dx/dt}$, and
  $\frac{d^{2}y}{dx^{2}} = \dfrac{\frac{d}{dt}\left(\frac{dy}{dx}\right)}{dx/dt}$ —
  never $\ddot y/\ddot x$.
- **Geometry:** $f'(a)$ is the slope of the tangent at $x=a$; the normal has slope
  $-1/f'(a)$; the angle between curves is
  $\tan\theta = \left|\dfrac{m_1-m_2}{1+m_1m_2}\right|$.
- **Monotonicity:** $f' > 0$ increasing, $f' < 0$ decreasing. **Extremes:** solve
  $f' = 0$, then use the sign change of $f'$ or the sign of $f''$ ($f''<0$
  maximum, $f''>0$ minimum). On a closed interval, test the endpoints too.
- **Concavity:** $f'' > 0$ concave up, $f'' < 0$ concave down; an inflection point
  needs $f'' = 0$ **and** a change of sign.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. By first principle, $\dfrac{d}{dx}\sqrt{x}$ equals <span class="marks">[1]</span>
   (a) $\dfrac{1}{\sqrt{x}}$ (b) $\dfrac{1}{2\sqrt{x}}$ (c) $2\sqrt{x}$ (d) $\dfrac{\sqrt{x}}{2}$
2. $\dfrac{d}{dx}(\sin 3x)$ equals <span class="marks">[1]</span>
   (a) $\cos 3x$ (b) $-3\cos 3x$ (c) $3\cos 3x$ (d) $3\sin 3x$
3. If $y = x^{x}$ then $\dfrac{dy}{dx}$ equals <span class="marks">[1]</span>
   (a) $x\,x^{x-1}$ (b) $x^{x}\ln x$ (c) $x^{x}(1+\ln x)$ (d) $x^{x}$
4. The slope of the tangent to $y = x^{2}-4x+3$ at $x = 3$ is <span class="marks">[1]</span>
   (a) $0$ (b) $2$ (c) $-2$ (d) $6$
5. $\dfrac{d}{dx}\left(\tan^{-1}x\right)$ equals <span class="marks">[1]</span>
   (a) $\dfrac{1}{\sqrt{1-x^{2}}}$ (b) $\dfrac{-1}{1+x^{2}}$ (c) $\dfrac{1}{1+x^{2}}$ (d) $\sec^{2}x$
6. If $x = at^{2}$ and $y = 2at$, then $\dfrac{dy}{dx}$ equals <span class="marks">[1]</span>
   (a) $t$ (b) $\dfrac{1}{t}$ (c) $\dfrac{1}{2t}$ (d) $2at$
7. The function $f(x) = x^{3}-3x$ is decreasing on <span class="marks">[1]</span>
   (a) $(-\infty,-1)$ (b) $(-1,1)$ (c) $(1,\infty)$ (d) all of $\mathbb{R}$
8. If $f'(c) = 0$ and $f''(c) > 0$, then $f$ has at $x = c$ a <span class="marks">[1]</span>
   (a) local maximum (b) local minimum (c) point of inflection (d) corner
9. $\dfrac{d}{dx}\left(e^{2x}\right)$ equals <span class="marks">[1]</span>
   (a) $e^{2x}$ (b) $2e^{2x}$ (c) $2xe^{2x-1}$ (d) $e^{2}$
10. The $n$-th derivative of $e^{3x}$ is <span class="marks">[1]</span>
    (a) $3e^{3x}$ (b) $3^{n}e^{3x}$ (c) $n^{3}e^{3x}$ (d) $e^{3x}$
11. The point of inflection of $y = x^{3}-3x^{2}+2$ is <span class="marks">[1]</span>
    (a) $(0,2)$ (b) $(1,0)$ (c) $(2,-2)$ (d) $(3,2)$

::: note Answers to Group A
**1.** (b) — rationalising the numerator gives $1/\left(\sqrt{x+h}+\sqrt{x}\right) \to 1/(2\sqrt{x})$.

**2.** (c) — chain rule: outer derivative $\cos 3x$, inner derivative $3$.

**3.** (c) — logarithmic differentiation: $\ln y = x\ln x$, so $y'/y = 1+\ln x$.

**4.** (b) — $\dfrac{dy}{dx} = 2x-4$, which is $6-4 = 2$ at $x=3$.

**5.** (c) — a standard derivative.

**6.** (b) — $\dfrac{dy/dt}{dx/dt} = \dfrac{2a}{2at} = \dfrac1t$.

**7.** (b) — $f' = 3(x-1)(x+1)$ is negative exactly on $(-1,1)$.

**8.** (b) — $f''>0$ means the curve is concave up (a "smile"), so the stationary
point is a valley.

**9.** (b) — chain rule: $e^{2x}\times 2$.

**10.** (b) — each differentiation multiplies by 3, so $n$ of them give $3^{n}$.

**11.** (b) — $y'' = 6x-6 = 0$ gives $x=1$, and $y(1) = 1-3+2 = 0$; $y''$ changes
sign there.
:::

**Group B — Short answer (5 marks each)**

1. Find, from first principles, the derivative of $y = \sqrt{2x+3}$. <span class="marks">[5]</span>
2. Find the derivative of $\tan x$ from first principles. <span class="marks">[5]</span>
3. Differentiate $y = \left(x^{2}+1\right)^{3}(2x-1)^{4}$ using logarithmic
   differentiation. <span class="marks">[5]</span>
4. Differentiate $y = \ln\dfrac{1+x}{1-x}$ with respect to $x$. <span class="marks">[5]</span>
5. If $x = a(t-\sin t)$ and $y = a(1-\cos t)$, find $\dfrac{dy}{dx}$. <span class="marks">[5]</span>
6. If $y = \sin^{-1}x$, prove that $\left(1-x^{2}\right)y_2-x\,y_1 = 0$. <span class="marks">[5]</span>
7. Find the equations of the tangent and the normal to the curve
   $y = x^{2}-4x+3$ at the point where it meets the $x$-axis at $x = 3$. <span class="marks">[5]</span>
8. Find the intervals in which $f(x) = 2x^{3}-3x^{2}-12x+5$ is increasing and
   decreasing. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** $\dfrac{dy}{dx} = \lim_{h\to0}\dfrac{\sqrt{2x+2h+3}-\sqrt{2x+3}}{h}$.
Multiply above and below by the conjugate $\sqrt{2x+2h+3}+\sqrt{2x+3}$:

$$ = \lim_{h\to0}\frac{(2x+2h+3)-(2x+3)}{h\left(\sqrt{2x+2h+3}+\sqrt{2x+3}\right)}
= \lim_{h\to0}\frac{2h}{h\left(\sqrt{2x+2h+3}+\sqrt{2x+3}\right)} $$

Cancel $h$ and let $h \to 0$:
$\dfrac{dy}{dx} = \dfrac{2}{2\sqrt{2x+3}} = \dfrac{1}{\sqrt{2x+3}}$.

**2.** $\dfrac{d}{dx}\tan x = \lim_{h\to0}\dfrac{\tan(x+h)-\tan x}{h}$. Writing
each tangent as sine over cosine and using a common denominator,

$$ \tan(x+h)-\tan x = \frac{\sin(x+h)\cos x-\cos(x+h)\sin x}{\cos(x+h)\cos x}
= \frac{\sin h}{\cos(x+h)\cos x} $$

because the numerator is $\sin[(x+h)-x]$. Hence

$$ \frac{d}{dx}\tan x = \lim_{h\to0}\frac{\sin h}{h}\cdot
\frac{1}{\cos(x+h)\cos x} = 1\cdot\frac{1}{\cos^{2}x} = \sec^{2}x $$

**3.** Take logarithms: $\ln y = 3\ln\left(x^{2}+1\right)+4\ln(2x-1)$.
Differentiate both sides:

$$ \frac{1}{y}\frac{dy}{dx} = 3\cdot\frac{2x}{x^{2}+1}+4\cdot\frac{2}{2x-1}
= \frac{6x}{x^{2}+1}+\frac{8}{2x-1} $$

$$ \frac{dy}{dx} = \left(x^{2}+1\right)^{3}(2x-1)^{4}
\left[\frac{6x}{x^{2}+1}+\frac{8}{2x-1}\right] $$

Combining over a common denominator gives the tidy form
$\dfrac{dy}{dx} = 2\left(x^{2}+1\right)^{2}(2x-1)^{3}\left(10x^{2}-3x+4\right)$.

**4.** First use the log law to split the quotient:
$y = \ln(1+x)-\ln(1-x)$. Then

$$ \frac{dy}{dx} = \frac{1}{1+x}-\frac{-1}{1-x} = \frac{1}{1+x}+\frac{1}{1-x}
= \frac{(1-x)+(1+x)}{(1+x)(1-x)} = \frac{2}{1-x^{2}} $$

**5.** $\dfrac{dx}{dt} = a(1-\cos t)$ and $\dfrac{dy}{dt} = a\sin t$. Hence

$$ \frac{dy}{dx} = \frac{a\sin t}{a(1-\cos t)} = \frac{\sin t}{1-\cos t} $$

Using $\sin t = 2\sin\frac t2\cos\frac t2$ and $1-\cos t = 2\sin^{2}\frac t2$,

$$ \frac{dy}{dx} = \frac{2\sin\frac t2\cos\frac t2}{2\sin^{2}\frac t2}
= \cot\frac{t}{2} $$

**6.** $y = \sin^{-1}x$ gives $y_1 = \dfrac{1}{\sqrt{1-x^{2}}}$, so
$\left(1-x^{2}\right)y_1^{2} = 1$. Differentiate this equation with respect to
$x$, using the product rule on the left:

$$ \left(1-x^{2}\right)\cdot 2y_1y_2+y_1^{2}(-2x) = 0 $$

Divide throughout by $2y_1$, which is non-zero:

$$ \left(1-x^{2}\right)y_2-x\,y_1 = 0 $$

**7.** *Point.* At $x = 3$, $y = 9-12+3 = 0$, so the point is $(3,0)$.
*Slope.* $\dfrac{dy}{dx} = 2x-4 = 2$ at $x = 3$.
*Tangent.* $y-0 = 2(x-3)$, i.e. $2x-y-6 = 0$.
*Normal.* Slope $= -\dfrac12$, so $y = -\dfrac12(x-3)$, i.e. $x+2y-3 = 0$.

**8.** $f'(x) = 6x^{2}-6x-12 = 6\left(x^{2}-x-2\right) = 6(x-2)(x+1)$, which is
zero at $x = -1$ and $x = 2$.

| Interval | $(x+1)$ | $(x-2)$ | $f'$ | Behaviour |
|---|---|---|---|---|
| $x<-1$ | $-$ | $-$ | $+$ | increasing |
| $-1<x<2$ | $+$ | $-$ | $-$ | decreasing |
| $x>2$ | $+$ | $+$ | $+$ | increasing |

So $f$ increases on $(-\infty,-1)$ and $(2,\infty)$ and decreases on $(-1,2)$.
:::

**Group C — Long answer (8 marks each)**

1. (a) Define the derivative of a function from first principle, and hence find
   the derivative of $\cos x$ from first principle. <span class="marks">[4]</span>
   (b) If $y = \tan^{-1}\dfrac{2x}{1-x^{2}}$, show that
   $\dfrac{dy}{dx} = \dfrac{2}{1+x^{2}}$ for $|x| < 1$. <span class="marks">[4]</span>
2. For the function $f(x) = 2x^{3}-3x^{2}-12x+5$, find the intervals of increase
   and decrease, the local maximum and minimum values, the intervals of concavity
   and the point of inflection. Hence sketch the curve. <span class="marks">[8]</span>
3. (a) State the second derivative test for maxima and minima. <span class="marks">[2]</span>
   (b) An open box with a square base is to be made from $108\ \text{cm}^{2}$ of
   sheet metal. Find the dimensions that give the greatest volume, and state that
   volume. <span class="marks">[6]</span>

::: note Answers to Group C
**1. (a)** *Definition.* The derivative of $f$ at $x$ is
$f'(x) = \lim_{h\to0}\dfrac{f(x+h)-f(x)}{h}$, when this limit exists.

*Application to $\cos x$.*

$$ \frac{d}{dx}\cos x = \lim_{h\to0}\frac{\cos(x+h)-\cos x}{h} $$

Use $\cos C-\cos D = -2\sin\dfrac{C+D}{2}\sin\dfrac{C-D}{2}$ with $C = x+h$ and
$D = x$:

$$ \cos(x+h)-\cos x = -2\sin\left(x+\frac h2\right)\sin\frac h2 $$

$$ \frac{d}{dx}\cos x
= \lim_{h\to0}\left[-\sin\left(x+\frac h2\right)\right]\cdot
\lim_{h\to0}\frac{\sin\frac h2}{\frac h2} = -\sin x \times 1 = -\sin x $$

**(b)** Put $x = \tan\theta$, so $\theta = \tan^{-1}x$ and, since $|x|<1$,
$-\dfrac{\pi}{4} < \theta < \dfrac{\pi}{4}$. Then

$$ \frac{2x}{1-x^{2}} = \frac{2\tan\theta}{1-\tan^{2}\theta} = \tan2\theta $$

Because $-\dfrac{\pi}{2} < 2\theta < \dfrac{\pi}{2}$, we may write
$y = \tan^{-1}(\tan2\theta) = 2\theta = 2\tan^{-1}x$. Differentiating,

$$ \frac{dy}{dx} = 2\cdot\frac{1}{1+x^{2}} = \frac{2}{1+x^{2}} $$

**2.** *Derivatives.*

$$ f'(x) = 6x^{2}-6x-12 = 6(x-2)(x+1), \qquad f''(x) = 12x-6 = 6(2x-1) $$

*Increase and decrease.* $f' = 0$ at $x = -1, 2$. From the sign table (Group B,
question 8) $f$ increases on $(-\infty,-1)$ and $(2,\infty)$, and decreases on
$(-1,2)$.

*Local extremes.* $f''(-1) = -18 < 0$, so $x = -1$ gives a local **maximum**,

$$ f(-1) = -2-3+12+5 = 12 $$

$f''(2) = 18 > 0$, so $x = 2$ gives a local **minimum**,

$$ f(2) = 16-12-24+5 = -15 $$

*Concavity.* $f'' < 0$ for $x < \dfrac12$ (concave down) and $f'' > 0$ for
$x > \dfrac12$ (concave up).

*Inflection.* $f'' = 0$ at $x = \dfrac12$, where the sign changes, and

$$ f\!\left(\tfrac12\right) = \tfrac14-\tfrac34-6+5 = -\tfrac32 $$

so the point of inflection is $\left(\dfrac12,\,-\dfrac32\right)$ — midway between
the two turning points, as it must be for a cubic.

*Sketch.* Rising to the peak $(-1,12)$, falling through the inflection
$\left(\frac12,-\frac32\right)$ to the valley $(2,-15)$, then rising again;
$f(0) = 5$ is the $y$-intercept.

**3. (a)** If $f'(c) = 0$, then: $f''(c) < 0$ implies a local maximum at $c$;
$f''(c) > 0$ implies a local minimum at $c$; and if $f''(c) = 0$ the test gives no
information, so the first derivative test (sign change of $f'$) must be used.

**(b)** Let the square base have side $x$ cm and the height be $h$ cm. The box is
open, so the sheet covers the base and four sides:

$$ x^{2}+4xh = 108 \qquad\Longrightarrow\qquad h = \frac{108-x^{2}}{4x} $$

The volume is

$$ V = x^{2}h = x^{2}\cdot\frac{108-x^{2}}{4x} = \frac{108x-x^{3}}{4}
= 27x-\frac{x^{3}}{4}, \qquad 0 < x < \sqrt{108} $$

$$ \frac{dV}{dx} = 27-\frac{3x^{2}}{4} = 0 \;\Longrightarrow\; x^{2} = 36
\;\Longrightarrow\; x = 6 \ \ (x>0) $$

$$ \frac{d^{2}V}{dx^{2}} = -\frac{3x}{2}, \qquad
\left.\frac{d^{2}V}{dx^{2}}\right|_{x=6} = -9 < 0 $$

so $x = 6$ gives a maximum. Then

$$ h = \frac{108-36}{24} = 3 $$

The box is $6\ \text{cm}\times6\ \text{cm}\times3\ \text{cm}$, with greatest volume

$$ V_{\max} = 6 \times 6 \times 3 = 108\ \text{cm}^{3} $$
:::
