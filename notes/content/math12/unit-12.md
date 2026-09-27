---
subject: Mathematics
grade: 12
unit: 12
title: Derivatives
hours: 18
area: Calculus
---

At $18$ teaching hours this is the largest unit in the Grade 12 course, and it
carries the most marks. Grade 11 taught you what a derivative *is* — the limit of
a difference quotient, the slope of a tangent — and how to differentiate
polynomials, trigonometric functions and composites. Grade 12 finishes the
toolkit (hyperbolic and inverse hyperbolic functions, implicit and parametric
forms, logarithmic differentiation, higher derivatives) and then spends most of
its time on what the derivative is *for*: evaluating stubborn limits, estimating
small changes, writing down tangents and normals, measuring how fast one quantity
changes when another does, and finding the largest or smallest value a quantity
can take.

::: key What the exam asks
Expect one or two Group A items on a standard derivative or a limit, two or three
Group B questions (differentiate this; find the tangent and normal; a rate
problem; an L'Hospital limit), and very often a full Group C question on
**maxima and minima** — usually an applied optimisation problem worth $8$ marks.
Show the derivative, set it to zero, **and apply the second derivative test**;
markers award a mark for the test alone.
:::

## Revision: the differentiation toolkit

Everything in this unit rests on the table below. Learn it in the direction
"function $\to$ derivative" and also backwards, because Unit 13 will need it
reversed.

::: key Table of standard derivatives
Let $u$ be a differentiable function of $x$ and $c$, $n$, $a$ constants.

| $y$ | $\dfrac{dy}{dx}$ | $y$ | $\dfrac{dy}{dx}$ |
|---|---|---|---|
| $c$ | $0$ | $\sin^{-1}x$ | $\dfrac{1}{\sqrt{1-x^{2}}}$ |
| $x^{n}$ | $n x^{n-1}$ | $\cos^{-1}x$ | $-\dfrac{1}{\sqrt{1-x^{2}}}$ |
| $\sqrt{x}$ | $\dfrac{1}{2\sqrt{x}}$ | $\tan^{-1}x$ | $\dfrac{1}{1+x^{2}}$ |
| $e^{x}$ | $e^{x}$ | $\cot^{-1}x$ | $-\dfrac{1}{1+x^{2}}$ |
| $a^{x}$ | $a^{x}\ln a$ | $\sec^{-1}x$ | $\dfrac{1}{|x|\sqrt{x^{2}-1}}$ |
| $\ln x$ | $\dfrac{1}{x}$ | $\mathrm{cosec}^{-1}x$ | $-\dfrac{1}{|x|\sqrt{x^{2}-1}}$ |
| $\log_a x$ | $\dfrac{1}{x\ln a}$ | $\sinh x$ | $\cosh x$ |
| $\sin x$ | $\cos x$ | $\cosh x$ | $\sinh x$ |
| $\cos x$ | $-\sin x$ | $\tanh x$ | $\mathrm{sech}^{2}x$ |
| $\tan x$ | $\sec^{2}x$ | $\coth x$ | $-\mathrm{cosech}^{2}x$ |
| $\cot x$ | $-\mathrm{cosec}^{2}x$ | $\mathrm{sech}\,x$ | $-\mathrm{sech}\,x\tanh x$ |
| $\sec x$ | $\sec x\tan x$ | $\mathrm{cosech}\,x$ | $-\mathrm{cosech}\,x\coth x$ |
| $\mathrm{cosec}\,x$ | $-\mathrm{cosec}\,x\cot x$ | $\sinh^{-1}x$ | $\dfrac{1}{\sqrt{x^{2}+1}}$ |
| $\cosh^{-1}x$ | $\dfrac{1}{\sqrt{x^{2}-1}}$ | $\tanh^{-1}x$ | $\dfrac{1}{1-x^{2}}$ |
| $\coth^{-1}x$ | $\dfrac{1}{1-x^{2}}$ | $\mathrm{sech}^{-1}x$ | $-\dfrac{1}{x\sqrt{1-x^{2}}}$ |

**Rules.** $(u \pm v)' = u' \pm v'$; product $(uv)' = u'v + uv'$;
quotient $\left(\dfrac{u}{v}\right)' = \dfrac{u'v - uv'}{v^{2}}$;
chain $\dfrac{dy}{dx} = \dfrac{dy}{du}\cdot\dfrac{du}{dx}$.

Every entry generalises by the chain rule: for example
$\dfrac{d}{dx}\sin^{-1}u = \dfrac{1}{\sqrt{1-u^{2}}}\dfrac{du}{dx}$.
:::

Three notations appear in NEB papers and all mean the same thing:
$\dfrac{dy}{dx}$ (Leibniz), $f'(x)$ (Lagrange) and $y_{1}$ (used mainly for
higher derivatives, where $y_{2} = \frac{d^{2}y}{dx^{2}}$ and so on). Use
whichever the question uses.

::: tip Choosing the right technique
Read the *shape* of the function before you start.

| The function looks like | Use |
|---|---|
| $u \pm v$, $uv$, $u/v$ | sum, product, quotient rule |
| $f(g(x))$ | chain rule |
| an equation in $x$ **and** $y$ not solved for $y$ | implicit differentiation |
| $x$ and $y$ both given in terms of $t$ or $\theta$ | parametric: $\dfrac{dy/dt}{dx/dt}$ |
| $[u(x)]^{v(x)}$, or a long product of powers | logarithmic differentiation |
| an inverse trig function of a messy argument | substitute $x=\tan\theta$, $x=\sin\theta$ first |
:::

::: example Worked example 12.1 — inverse trigonometric functions
**Problem.** Differentiate (a) $y = \tan^{-1}\!\left(\dfrac{2x}{1-x^{2}}\right)$,
(b) $y = \tan^{-1}\sqrt{\dfrac{1-\cos x}{1+\cos x}}$.

**Solution.** Both look terrible and both collapse under a substitution — always
try that before the chain rule.

**(a)** Put $x = \tan\theta$, so $\theta = \tan^{-1}x$. Then
$\dfrac{2x}{1-x^{2}} = \dfrac{2\tan\theta}{1-\tan^{2}\theta} = \tan 2\theta$,
using the double-angle identity. Hence

$$ y = \tan^{-1}(\tan 2\theta) = 2\theta = 2\tan^{-1}x
\;\Longrightarrow\; \frac{dy}{dx} = \frac{2}{1+x^{2}} $$

**(b)** Use $1 - \cos x = 2\sin^{2}\frac{x}{2}$ and
$1 + \cos x = 2\cos^{2}\frac{x}{2}$:

$$ \sqrt{\frac{2\sin^{2}(x/2)}{2\cos^{2}(x/2)}} = \tan\frac{x}{2}
\;\Longrightarrow\; y = \tan^{-1}\left(\tan\frac{x}{2}\right) = \frac{x}{2} $$

$$ \frac{dy}{dx} = \frac12 $$
:::

::: example Worked example 12.2 — exponential and logarithmic functions
**Problem.** Differentiate (a) $y = e^{2x}\sin 3x$,
(b) $y = \ln\left[\tan\!\left(\dfrac{x}{2} + \dfrac{\pi}{4}\right)\right]$.

**Solution.**

**(a)** Product rule, with each factor needing the chain rule:

$$ \frac{dy}{dx} = \frac{d}{dx}(e^{2x})\cdot\sin 3x + e^{2x}\cdot\frac{d}{dx}(\sin 3x) $$
$$ = 2e^{2x}\sin 3x + 3e^{2x}\cos 3x = e^{2x}\left(2\sin 3x + 3\cos 3x\right) $$

**(b)** Let $u = \tan\left(\frac{x}{2}+\frac{\pi}{4}\right)$. Then
$\dfrac{dy}{dx} = \dfrac{1}{u}\dfrac{du}{dx}$ and
$\dfrac{du}{dx} = \frac12\sec^{2}\left(\frac{x}{2}+\frac{\pi}{4}\right)$:

$$ \frac{dy}{dx} = \frac{\frac12\sec^{2}\left(\frac{x}{2}+\frac{\pi}{4}\right)}
{\tan\left(\frac{x}{2}+\frac{\pi}{4}\right)}
= \frac{1}{2\sin\left(\frac{x}{2}+\frac{\pi}{4}\right)\cos\left(\frac{x}{2}+\frac{\pi}{4}\right)} $$

because $\dfrac{\sec^{2}A}{\tan A} = \dfrac{1}{\sin A\cos A}$. Now
$2\sin A\cos A = \sin 2A$ with $2A = x + \frac{\pi}{2}$:

$$ \frac{dy}{dx} = \frac{1}{\sin\left(x+\frac{\pi}{2}\right)} = \frac{1}{\cos x}
= \sec x $$
:::

::: example Worked example 12.3 — implicit differentiation
**Problem.** If $x^{3} + y^{3} = 3axy$ (the folium of Descartes), find
$\dfrac{dy}{dx}$.

**Solution.** Differentiate every term with respect to $x$, remembering that $y$
is a function of $x$ so each $y$ contributes a factor $\dfrac{dy}{dx}$:

$$ 3x^{2} + 3y^{2}\frac{dy}{dx} = 3a\left(1\cdot y + x\frac{dy}{dx}\right)
\qquad \text{(product rule on } 3axy) $$

Divide by $3$ and collect the $\dfrac{dy}{dx}$ terms on one side:

$$ y^{2}\frac{dy}{dx} - ax\frac{dy}{dx} = ay - x^{2}
\;\Longrightarrow\; \frac{dy}{dx} = \frac{ay - x^{2}}{y^{2} - ax} $$
:::

::: example Worked example 12.4 — parametric differentiation
**Problem.** If $x = a(\theta - \sin\theta)$ and $y = a(1 - \cos\theta)$, find
$\dfrac{dy}{dx}$.

**Solution.** Differentiate each coordinate with respect to the parameter and
divide:

$$ \frac{dx}{d\theta} = a(1 - \cos\theta), \qquad
\frac{dy}{d\theta} = a\sin\theta $$

$$ \frac{dy}{dx} = \frac{dy/d\theta}{dx/d\theta}
= \frac{a\sin\theta}{a(1-\cos\theta)} = \frac{\sin\theta}{1-\cos\theta} $$

Use $\sin\theta = 2\sin\frac{\theta}{2}\cos\frac{\theta}{2}$ and
$1-\cos\theta = 2\sin^{2}\frac{\theta}{2}$:

$$ \frac{dy}{dx} = \frac{2\sin\frac{\theta}{2}\cos\frac{\theta}{2}}
{2\sin^{2}\frac{\theta}{2}} = \cot\frac{\theta}{2} $$
:::

::: example Worked example 12.5 — logarithmic differentiation
**Problem.** Differentiate $y = x^{\sin x} + (\sin x)^{x}$.

**Solution.** A variable raised to a variable power cannot be handled by the
power rule or by the exponential rule. Split $y = u + v$ and take logarithms of
each part separately.

Let $u = x^{\sin x}$. Then $\ln u = \sin x \ln x$. Differentiating both sides:

$$ \frac{1}{u}\frac{du}{dx} = \cos x\,\ln x + \frac{\sin x}{x}
\;\Longrightarrow\;
\frac{du}{dx} = x^{\sin x}\left(\cos x\,\ln x + \frac{\sin x}{x}\right) $$

Let $v = (\sin x)^{x}$. Then $\ln v = x\ln(\sin x)$, so

$$ \frac{1}{v}\frac{dv}{dx} = \ln(\sin x) + x\cdot\frac{\cos x}{\sin x}
\;\Longrightarrow\;
\frac{dv}{dx} = (\sin x)^{x}\left[\ln(\sin x) + x\cot x\right] $$

$$ \frac{dy}{dx} = x^{\sin x}\left(\cos x\,\ln x + \frac{\sin x}{x}\right)
+ (\sin x)^{x}\left[\ln(\sin x) + x\cot x\right] $$
:::

::: example Worked example 12.6 — higher derivatives
**Problem.** If $y = e^{m\sin^{-1}x}$, prove that
$(1-x^{2})y_{2} - x y_{1} - m^{2}y = 0$, where $y_1 = \dfrac{dy}{dx}$ and
$y_2 = \dfrac{d^{2}y}{dx^{2}}$.

**Solution.** Differentiate once, by the chain rule:

$$ y_{1} = e^{m\sin^{-1}x}\cdot\frac{m}{\sqrt{1-x^{2}}} = \frac{my}{\sqrt{1-x^{2}}} $$

Clear the surd before differentiating again — this is the standard trick:

$$ \sqrt{1-x^{2}}\;y_{1} = my \;\Longrightarrow\; (1-x^{2})y_{1}^{2} = m^{2}y^{2}
\qquad \text{(squaring)} $$

Differentiate this with respect to $x$:

$$ -2x\,y_{1}^{2} + (1-x^{2})\cdot 2y_{1}y_{2} = m^{2}\cdot 2y y_{1} $$

Divide throughout by $2y_{1}$ (non-zero except at isolated points):

$$ (1-x^{2})y_{2} - x y_{1} - m^{2} y = 0 $$
:::

## 12.1 Derivatives of hyperbolic and inverse hyperbolic functions

::: definition Hyperbolic functions
$$ \sinh x = \frac{e^{x} - e^{-x}}{2}, \qquad \cosh x = \frac{e^{x}+e^{-x}}{2},
\qquad \tanh x = \frac{\sinh x}{\cosh x} = \frac{e^{x}-e^{-x}}{e^{x}+e^{-x}} $$

with $\mathrm{coth}\,x$, $\mathrm{sech}\,x$ and $\mathrm{cosech}\,x$ as the
reciprocals. The fundamental identity is

$$ \cosh^{2}x - \sinh^{2}x = 1 $$

(a **minus** sign, unlike $\sin^2 x + \cos^2 x = 1$), from which
$1 - \tanh^{2}x = \mathrm{sech}^{2}x$ and
$\coth^{2}x - 1 = \mathrm{cosech}^{2}x$.
:::

The name comes from the fact that $(\cosh t, \sinh t)$ traces the hyperbola
$x^{2}-y^{2}=1$ just as $(\cos t, \sin t)$ traces the circle $x^{2}+y^{2}=1$.
Physically, $\cosh$ is the shape of a hanging chain or a power line.

```figure caption="The three basic hyperbolic functions. $\\cosh x$ is even with minimum value $1$ at $x=0$; $\\sinh x$ is odd and increasing everywhere; $\\tanh x$ is odd, increasing, and squeezed between the asymptotes $y = \\pm 1$. Both $\\sinh x$ and $\\cosh x$ approach $\\frac12 e^{x}$ (dashed) for large $x$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8, 3.0))
x = np.linspace(-2.6, 2.6, 400)
ax.plot(x, np.cosh(x), color=SERIES[0], lw=1.8, label='cosh x')
ax.plot(x, np.sinh(x), color=SERIES[1], lw=1.8, label='sinh x')
ax.plot(x, np.tanh(x), color=SERIES[2], lw=1.8, label='tanh x')
ax.plot(x, 0.5*np.exp(x), color=MUTED, lw=1.0, ls='--', label='½e$^x$')
for yv in (1, -1):
    ax.axhline(yv, color=GRID, lw=0.9, ls=':')
ax.axhline(0, color=INK, lw=0.9); ax.axvline(0, color=INK, lw=0.9)
ax.text(-2.5, 1.15, 'y = 1', fontsize=8.0, color=MUTED)
ax.text(-2.5, -1.45, 'y = −1', fontsize=8.0, color=MUTED)
ax.set_ylim(-4.2, 5.4); ax.set_xlim(-2.7, 2.7)
ax.set_xlabel('x', fontsize=9.0); ax.set_ylabel('y', fontsize=9.0)
ax.legend(fontsize=8.4, loc='upper left', frameon=True, facecolor='white',
          edgecolor='none', framealpha=0.94)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.35)
fig.tight_layout(pad=0.4)
```

::: memory Osborn's rule for hyperbolic identities
Every trigonometric identity has a hyperbolic twin. Write the trigonometric
identity, replace $\sin \to \sinh$ and $\cos \to \cosh$, and then **change the
sign of every term that contains a product of two sines** (including
$\tan^{2}$ and $\cot^{2}$, which hide one).

| Trigonometric | Hyperbolic |
|---|---|
| $\cos^{2}x + \sin^{2}x = 1$ | $\cosh^{2}x - \sinh^{2}x = 1$ |
| $1 + \tan^{2}x = \sec^{2}x$ | $1 - \tanh^{2}x = \mathrm{sech}^{2}x$ |
| $\sin(A+B) = \sin A\cos B + \cos A\sin B$ | $\sinh(A+B) = \sinh A\cosh B + \cosh A\sinh B$ |
| $\cos(A+B) = \cos A\cos B - \sin A\sin B$ | $\cosh(A+B) = \cosh A\cosh B + \sinh A\sinh B$ |
| $\sin 2x = 2\sin x\cos x$ | $\sinh 2x = 2\sinh x\cosh x$ |
| $\cos 2x = 2\cos^{2}x - 1$ | $\cosh 2x = 2\cosh^{2}x - 1$ |

These are what let you simplify a hyperbolic derivative once you have found it.
:::

::: derivation Derivatives of $\sinh x$ and $\cosh x$
Differentiate the definitions directly, using
$\dfrac{d}{dx}e^{x} = e^{x}$ and $\dfrac{d}{dx}e^{-x} = -e^{-x}$:

$$ \frac{d}{dx}\sinh x = \frac{d}{dx}\left(\frac{e^{x}-e^{-x}}{2}\right)
= \frac{e^{x} + e^{-x}}{2} = \cosh x $$

$$ \frac{d}{dx}\cosh x = \frac{d}{dx}\left(\frac{e^{x}+e^{-x}}{2}\right)
= \frac{e^{x} - e^{-x}}{2} = \sinh x $$

Note there is **no minus sign** in the second one. For $\tanh x$ use the quotient
rule:

$$ \frac{d}{dx}\tanh x = \frac{\cosh x\cdot\cosh x - \sinh x\cdot\sinh x}{\cosh^{2}x}
= \frac{\cosh^{2}x - \sinh^{2}x}{\cosh^{2}x} = \frac{1}{\cosh^{2}x}
= \mathrm{sech}^{2}x $$
:::

::: definition Inverse hyperbolic functions in logarithmic form
$$ \sinh^{-1}x = \ln\left(x + \sqrt{x^{2}+1}\right), \quad x \in \mathbb{R} $$
$$ \cosh^{-1}x = \ln\left(x + \sqrt{x^{2}-1}\right), \quad x \ge 1 $$
$$ \tanh^{-1}x = \frac12\ln\left(\frac{1+x}{1-x}\right), \quad |x| < 1 $$
:::

::: derivation Derivative of $\sinh^{-1}x$, two ways
**From the logarithmic form.** With $y = \ln\left(x+\sqrt{x^{2}+1}\right)$,

$$ \frac{dy}{dx} = \frac{1}{x+\sqrt{x^{2}+1}}
\left(1 + \frac{x}{\sqrt{x^{2}+1}}\right)
= \frac{1}{x+\sqrt{x^{2}+1}}\cdot\frac{\sqrt{x^{2}+1}+x}{\sqrt{x^{2}+1}} $$

The bracket cancels the denominator, leaving

$$ \frac{dy}{dx} = \frac{1}{\sqrt{x^{2}+1}} $$

**By implicit differentiation.** Let $y = \sinh^{-1}x$, so $x = \sinh y$.
Differentiate with respect to $x$:

$$ 1 = \cosh y\,\frac{dy}{dx} \;\Longrightarrow\;
\frac{dy}{dx} = \frac{1}{\cosh y} = \frac{1}{\sqrt{1+\sinh^{2}y}}
= \frac{1}{\sqrt{1+x^{2}}} $$

using $\cosh^{2}y - \sinh^{2}y = 1$ and $\cosh y > 0$. The same method gives
$\dfrac{d}{dx}\cosh^{-1}x = \dfrac{1}{\sqrt{x^{2}-1}}$ and
$\dfrac{d}{dx}\tanh^{-1}x = \dfrac{1}{1-x^{2}}$.
:::

::: example Worked example 12.7 — hyperbolic derivatives
**Problem.** Differentiate (a) $y = \cosh(x^{2}+1)$, (b) $y = \ln(\cosh x)$,
(c) $y = \sinh^{3}2x$, (d) $y = \sinh x\cosh x$.

**Solution.**

**(a)** Chain rule with $u = x^{2}+1$:
$$ \frac{dy}{dx} = \sinh(x^{2}+1)\cdot 2x = 2x\sinh(x^{2}+1) $$

**(b)** $\dfrac{dy}{dx} = \dfrac{1}{\cosh x}\cdot\sinh x = \tanh x$.

**(c)** Write $y = (\sinh 2x)^{3}$ and apply the chain rule twice:
$$ \frac{dy}{dx} = 3(\sinh 2x)^{2}\cdot\cosh 2x\cdot 2 = 6\sinh^{2}2x\cosh 2x $$

**(d)** Product rule:
$$ \frac{dy}{dx} = \cosh x\cdot\cosh x + \sinh x\cdot\sinh x
= \cosh^{2}x + \sinh^{2}x = \cosh 2x $$
(the last step by the identity $\cosh 2x = \cosh^2 x + \sinh^2 x$; you could also
write $y = \frac12\sinh 2x$ first and differentiate in one line).
:::

::: example Worked example 12.8 — inverse hyperbolic derivatives
**Problem.** Differentiate (a) $y = \sinh^{-1}\dfrac{x}{3}$,
(b) $y = \cosh^{-1}(2x)$, (c) $y = \tanh^{-1}(x^{2})$.

**Solution.** Each is a standard derivative composed with an inner function.

**(a)** With $u = \dfrac{x}{3}$, $\dfrac{du}{dx} = \dfrac13$:
$$ \frac{dy}{dx} = \frac{1}{\sqrt{u^{2}+1}}\cdot\frac13
= \frac{1}{3\sqrt{\frac{x^{2}}{9}+1}} = \frac{1}{3\cdot\frac{\sqrt{x^{2}+9}}{3}}
= \frac{1}{\sqrt{x^{2}+9}} $$

**(b)** With $u = 2x$:
$$ \frac{dy}{dx} = \frac{1}{\sqrt{4x^{2}-1}}\cdot 2 = \frac{2}{\sqrt{4x^{2}-1}},
\qquad x > \tfrac12 $$

**(c)** With $u = x^{2}$:
$$ \frac{dy}{dx} = \frac{1}{1-x^{4}}\cdot 2x = \frac{2x}{1-x^{4}},
\qquad |x| < 1 $$
:::

::: caution Signs in the hyperbolic table
$\dfrac{d}{dx}\cosh x = +\sinh x$, but $\dfrac{d}{dx}\cos x = -\sin x$. Likewise
$\dfrac{d}{dx}\tanh^{-1}x = \dfrac{1}{1-x^{2}}$ while
$\dfrac{d}{dx}\tan^{-1}x = \dfrac{1}{1+x^{2}}$. Whenever you meet a hyperbolic
function, check the sign against the table before you write it down.
:::

## 12.2 L'Hospital's rule ($0/0$ and $\infty/\infty$ forms)

Some limits refuse to yield to factorising or to the standard limits
$\lim_{x\to0}\frac{\sin x}{x} = 1$. L'Hospital's rule turns them into a
derivative problem.

::: key L'Hospital's rule
If $f$ and $g$ are differentiable near $a$, $g'(x) \ne 0$, and

$$ \lim_{x\to a} \frac{f(x)}{g(x)} \quad \text{is of the form } \frac00
\text{ or } \frac{\infty}{\infty} $$

then

$$ \lim_{x\to a}\frac{f(x)}{g(x)} = \lim_{x\to a}\frac{f'(x)}{g'(x)} $$

provided the right-hand limit exists. The rule may be applied repeatedly. It
holds for $a$ finite or infinite.
:::

::: caution Check the form first, and differentiate separately
Two mistakes cost marks every year. First, **verify** that substituting $x = a$
really gives $\frac00$ or $\frac{\infty}{\infty}$ — applying the rule to
$\lim_{x\to0}\frac{\cos x}{x+1}$ gives the wrong answer because the form is
$\frac{1}{1}$, not indeterminate. Second, $\frac{f'}{g'}$ is **not** the quotient
rule: differentiate the numerator and the denominator *independently*.
:::

::: note Why the rule works (sketch)
Suppose $f(a) = g(a) = 0$. Divide numerator and denominator of the difference
quotients by $(x-a)$:

$$ \frac{f(x)}{g(x)} = \frac{f(x) - f(a)}{g(x) - g(a)}
= \frac{\dfrac{f(x)-f(a)}{x-a}}{\dfrac{g(x)-g(a)}{x-a}} $$

As $x \to a$ the top tends to $f'(a)$ and the bottom to $g'(a)$, so the quotient
tends to $\dfrac{f'(a)}{g'(a)}$ whenever $g'(a) \ne 0$. The full theorem, proved
from Cauchy's mean value theorem, removes that last restriction and extends the
result to $\frac{\infty}{\infty}$ and to $a = \pm\infty$.
:::

Other indeterminate forms — $0\cdot\infty$, $\infty - \infty$, $0^{0}$,
$1^{\infty}$, $\infty^{0}$ — must first be rewritten as a quotient (or have
logarithms taken) before the rule applies. The table below shows the standard
rearrangements.

| Form | Rewrite as | Becomes |
|---|---|---|
| $0\cdot\infty$ | $\dfrac{f}{1/g}$ | $\dfrac00$ |
| $\infty-\infty$ | put over a common denominator | $\dfrac00$ |
| $0^{0}$, $1^{\infty}$, $\infty^{0}$ | take $\ln$, then $\ln y = v\ln u$ | $0\cdot\infty$ |

::: example Worked example 12.9 — the $0/0$ form
**Problem.** Evaluate (a)
$\displaystyle\lim_{x\to0}\frac{e^{x} - e^{-x} - 2x}{x - \sin x}$,
(b) $\displaystyle\lim_{x\to0}\frac{\tan x - x}{x - \sin x}$.

**Solution.**

**(a)** At $x = 0$ the numerator is $1 - 1 - 0 = 0$ and the denominator is
$0 - 0 = 0$: the form is $\frac00$, so the rule applies.

$$ \lim_{x\to0}\frac{e^{x}-e^{-x}-2x}{x-\sin x}
= \lim_{x\to0}\frac{e^{x}+e^{-x}-2}{1-\cos x} \qquad \left(\text{still } \tfrac00\right) $$
$$ = \lim_{x\to0}\frac{e^{x}-e^{-x}}{\sin x} \qquad \left(\text{still } \tfrac00\right) $$
$$ = \lim_{x\to0}\frac{e^{x}+e^{-x}}{\cos x} = \frac{1+1}{1} = 2 $$

**(b)** Again $\frac00$ at every stage:

$$ \lim_{x\to0}\frac{\tan x - x}{x - \sin x}
= \lim_{x\to0}\frac{\sec^{2}x - 1}{1 - \cos x}
= \lim_{x\to0}\frac{2\sec^{2}x\tan x}{\sin x} $$

$$ = \lim_{x\to0}\frac{2\sec^{2}x}{\cos x}\cdot\frac{\sin x}{\sin x}
= \lim_{x\to0}\frac{2}{\cos^{3}x} = 2 $$

using $\tan x = \dfrac{\sin x}{\cos x}$ to cancel the $\sin x$ at the third step.
:::

::: example Worked example 12.10 — the $\infty/\infty$ form and its relatives
**Problem.** Evaluate (a) $\displaystyle\lim_{x\to\infty}\frac{x^{2}}{e^{x}}$,
(b) $\displaystyle\lim_{x\to 0^{+}} x\ln x$,
(c) $\displaystyle\lim_{x\to 0^{+}} x^{x}$.

**Solution.**

**(a)** The form is $\dfrac{\infty}{\infty}$. Apply the rule twice:

$$ \lim_{x\to\infty}\frac{x^{2}}{e^{x}} = \lim_{x\to\infty}\frac{2x}{e^{x}}
= \lim_{x\to\infty}\frac{2}{e^{x}} = 0 $$

The exponential beats every power — this is why $e^{x}$ dominates in growth
comparisons.

**(b)** The form is $0 \cdot (-\infty)$, which is indeterminate but not a
quotient. Rewrite it as one:

$$ \lim_{x\to0^{+}} x\ln x = \lim_{x\to0^{+}}\frac{\ln x}{1/x}
\qquad \left(\text{now } \tfrac{-\infty}{\infty}\right) $$
$$ = \lim_{x\to0^{+}}\frac{1/x}{-1/x^{2}} = \lim_{x\to0^{+}}(-x) = 0 $$

**(c)** The form is $0^{0}$. Take logarithms: let $y = x^{x}$, so
$\ln y = x\ln x$. By part (b), $\ln y \to 0$, hence

$$ \lim_{x\to0^{+}} x^{x} = e^{0} = 1 $$
:::

::: example Worked example 12.11 — standard limits recovered
**Problem.** Using L'Hospital's rule, evaluate
(a) $\displaystyle\lim_{x\to0}\frac{a^{x}-b^{x}}{x}$ $(a, b > 0)$,
(b) $\displaystyle\lim_{x\to0}\frac{\sinh x}{x}$,
(c) $\displaystyle\lim_{x\to0}\left(\frac1x - \frac{1}{\sin x}\right)$.

**Solution.**

**(a)** At $x=0$ the numerator is $1 - 1 = 0$: the form is $\frac00$. Using
$\dfrac{d}{dx}a^{x} = a^{x}\ln a$,

$$ \lim_{x\to0}\frac{a^{x}-b^{x}}{x} = \lim_{x\to0}\frac{a^{x}\ln a - b^{x}\ln b}{1}
= \ln a - \ln b = \ln\frac{a}{b} $$

**(b)** Again $\frac00$:

$$ \lim_{x\to0}\frac{\sinh x}{x} = \lim_{x\to0}\frac{\cosh x}{1} = \cosh 0 = 1 $$

the hyperbolic twin of $\lim_{x\to0}\frac{\sin x}{x} = 1$.

**(c)** The form is $\infty - \infty$, so combine into a single fraction first:

$$ \frac1x - \frac{1}{\sin x} = \frac{\sin x - x}{x\sin x}
\qquad\left(\text{now } \tfrac00\right) $$

$$ = \lim_{x\to0}\frac{\cos x - 1}{\sin x + x\cos x}
\qquad\left(\text{still } \tfrac00\right) $$
$$ = \lim_{x\to0}\frac{-\sin x}{2\cos x - x\sin x} = \frac{0}{2} = 0 $$
:::

## 12.3 Differentials

The derivative $\dfrac{dy}{dx}$ was introduced as a single symbol, not a
fraction. The language of **differentials** gives $dy$ and $dx$ separate meanings
so that the fraction becomes literal — and that makes the derivative a practical
tool for estimating small changes.

::: definition Differentials
For $y = f(x)$, let $dx = \Delta x$ be any increment in $x$. The **differential
of $y$** is defined as

$$ dy = f'(x)\,dx $$

$dy$ is the change in the *tangent line*; $\Delta y = f(x+\Delta x) - f(x)$ is
the change in the *curve*. For small $dx$ the two are nearly equal:

$$ \Delta y \approx dy = f'(x)\,dx, \qquad\text{so}\qquad
f(x + \Delta x) \approx f(x) + f'(x)\,\Delta x $$
:::

```figure caption="$dy$ against $\\Delta y$. Moving from $x$ to $x + \\Delta x$, the curve rises by $\\Delta y$ but the tangent rises by only $dy = f'(x)\\,dx$. The gap between them (the small bracket) shrinks faster than $\\Delta x$ does, which is why $dy$ is a usable estimate of $\\Delta y$ when $\\Delta x$ is small."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8, 3.1))
f = lambda t: 0.45*t**2 + 0.6
fp = lambda t: 0.9*t
x0, dx = 1.6, 1.15
xs = np.linspace(0.5, 3.35, 300)
ax.plot(xs, f(xs), color=ACCENT, lw=2.0, label='y = f(x)')
xt = np.linspace(1.15, 3.20, 50)
ax.plot(xt, f(x0) + fp(x0)*(xt - x0), color='#d9534f', lw=1.5, ls='--', label='tangent at x')
x1 = x0 + dx
ax.plot([x0, x1], [f(x0), f(x0)], color=INK, lw=1.1)
ax.plot([x1, x1], [f(x0), f(x0)+fp(x0)*dx], color='#d9534f', lw=1.6)
ax.plot([x1, x1], [f(x0)+fp(x0)*dx, f(x1)], color='#2e8b57', lw=1.6)
ax.plot([x0, x0], [0, f(x0)], color=GRID, lw=0.9, ls=':')
ax.plot([x1, x1], [0, f(x0)], color=GRID, lw=0.9, ls=':')
ax.plot([x0, x1], [f(x0), f(x1)], 'o', color=INK, ms=4.5)
ax.annotate('dx = Δx', xy=((x0+x1)/2, f(x0)), xytext=((x0+x1)/2, f(x0)-0.95),
            ha='center', fontsize=9.0, color=INK,
            arrowprops=dict(arrowstyle='-', color=INK, lw=0.8))
ax.text(x1+0.09, f(x0)+0.5*fp(x0)*dx, 'dy', fontsize=9.4, color='#d9534f', va='center')
ax.text(x1+0.09, f(x0)+fp(x0)*dx + 0.5*(f(x1)-f(x0)-fp(x0)*dx),
        'Δy − dy', fontsize=8.6, color='#2e8b57', va='center')
ax.annotate('', xy=(x1-0.14, f(x1)), xytext=(x1-0.14, f(x0)),
            arrowprops=dict(arrowstyle='<->', color=MUTED, lw=1.0))
ax.text(x1-0.24, f(x0)+0.52*(f(x1)-f(x0)), 'Δy', fontsize=9.4, color=MUTED,
        ha='right', va='center')
ax.set_xticks([x0, x1]); ax.set_xticklabels(['x', 'x + Δx'], fontsize=9.0)
ax.set_yticks([])
ax.set_xlim(0.5, 3.7); ax.set_ylim(0, 6.4)
ax.legend(fontsize=8.4, loc='upper left', frameon=False)
ax.spines[['top','right','left']].set_visible(False)
fig.tight_layout(pad=0.4)
```

::: example Worked example 12.12 — approximation by differentials
**Problem.** (a) Find the approximate value of $\sqrt{49.5}$.
(b) The radius of a sphere is measured as $7$ cm with a possible error of
$0.02$ cm. Find the approximate error in the calculated volume.

**Solution.**

**(a)** Take $y = \sqrt{x}$ with $x = 49$ (a perfect square nearby) and
$\Delta x = 0.5$. Then $f'(x) = \dfrac{1}{2\sqrt{x}}$, so

$$ dy = \frac{1}{2\sqrt{49}}\times 0.5 = \frac{0.5}{14} = 0.0357 $$

$$ \sqrt{49.5} \approx \sqrt{49} + dy = 7 + 0.0357 = 7.0357 $$

(The calculator value is $7.03562$, so the estimate is correct to four decimal
places.)

**(b)** $V = \dfrac43\pi r^{3}$, so $\dfrac{dV}{dr} = 4\pi r^{2}$ and

$$ dV = 4\pi r^{2}\,dr = 4\pi (7)^{2}(0.02) = 3.92\pi \approx 12.32\ \text{cm}^{3} $$

The relative error is worth noting:
$\dfrac{dV}{V} = \dfrac{4\pi r^{2}dr}{\frac43\pi r^{3}} = 3\dfrac{dr}{r}$, so a
$0.29\%$ error in the radius becomes a $0.86\%$ error in the volume — errors are
tripled by cubing.
:::

::: key Absolute, relative and percentage error
If $x$ is measured with error $\Delta x$ and $y = f(x)$ is computed from it:

| | Formula |
|---|---|
| absolute error in $y$ | $dy = f'(x)\,dx$ |
| relative error | $\dfrac{dy}{y}$ |
| percentage error | $\dfrac{dy}{y}\times 100\%$ |

For a power law $y = kx^{n}$ the relative errors are simply related:
$\dfrac{dy}{y} = n\dfrac{dx}{x}$. So squaring doubles the percentage error and
cubing triples it.
:::

::: example Worked example 12.13 — percentage error
**Problem.** The side of a cube is measured as $10$ cm with a possible error of
$0.01$ cm. Find the approximate error in the calculated surface area, and the
percentage error in the calculated volume.

**Solution.** Let $a$ be the side, $S = 6a^{2}$ the surface area and $V = a^{3}$
the volume, with $a = 10$ and $da = 0.01$.

$$ dS = \frac{dS}{da}\,da = 12a\,da = 12(10)(0.01) = 1.2\ \text{cm}^{2} $$

For the volume, use the relative-error shortcut. The percentage error in the side
is

$$ \frac{da}{a}\times100 = \frac{0.01}{10}\times100 = 0.1\% $$

and since $V = a^{3}$,

$$ \frac{dV}{V} = 3\frac{da}{a} \;\Longrightarrow\;
\text{percentage error in } V = 3 \times 0.1\% = 0.3\% $$
:::

## 12.4 Tangent and normal to a curve

::: key Tangent and normal
Let $P(x_{1}, y_{1})$ lie on the curve $y = f(x)$ and let
$m = \left.\dfrac{dy}{dx}\right|_{(x_1,y_1)}$.

| | Slope | Equation |
|---|---|---|
| Tangent at $P$ | $m$ | $y - y_{1} = m(x - x_{1})$ |
| Normal at $P$ | $-\dfrac{1}{m}$ | $y - y_{1} = -\dfrac{1}{m}(x - x_{1})$ |

Special cases: if $m = 0$ the tangent is $y = y_{1}$ (horizontal) and the normal
is $x = x_{1}$; if $\dfrac{dy}{dx}$ is infinite the tangent is $x = x_{1}$ and
the normal is $y = y_{1}$.
:::

```figure caption="Tangent and normal to $y = x^{3} - 3x + 2$ at $P(2, 4)$. The tangent has slope $f'(2) = 9$, giving $y = 9x - 14$; the normal is perpendicular to it, slope $-1/9$, giving $x + 9y - 38 = 0$. The right angle at $P$ is the whole content of the word 'normal'."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8, 3.2))
x = np.linspace(-1.1, 2.7, 400)
ax.plot(x, x**3 - 3*x + 2, color=ACCENT, lw=2.0, label='y = x³ − 3x + 2')
xt = np.linspace(1.35, 2.55, 20)
ax.plot(xt, 9*xt - 14, color='#d9534f', lw=1.6, label='tangent  y = 9x − 14')
xn = np.linspace(-0.6, 2.9, 20)
ax.plot(xn, (38 - xn)/9, color='#2e8b57', lw=1.6, ls='--',
        label='normal  x + 9y − 38 = 0')
ax.plot([2], [4], 'o', color=INK, ms=6, zorder=5)
ax.annotate('P(2, 4)', xy=(2, 4), xytext=(-62, 30), textcoords='offset points',
            fontsize=9.4, color=INK,
            arrowprops=dict(arrowstyle='->', color=INK, lw=0.9))
# right-angle marker
import math
a1 = math.atan(9.0); a2 = math.atan(-1/9.0)
sx, sy = 0.16, 0.16*3.0
u = np.array([math.cos(a1), math.sin(a1)]); v = np.array([math.cos(a2), math.sin(a2)])
sc = np.array([0.20, 0.20*2.6])
P = np.array([2.0, 4.0])
A = P + u*sc; B = P + v*sc; C = P + (u+v)*sc
ax.plot([A[0], C[0], B[0]], [A[1], C[1], B[1]], color=MUTED, lw=1.0)
ax.axhline(0, color=INK, lw=0.8); ax.axvline(0, color=INK, lw=0.8)
ax.set_xlim(-1.2, 3.0); ax.set_ylim(-1.2, 8.0)
ax.set_xlabel('x', fontsize=9.0); ax.set_ylabel('y', fontsize=9.0)
ax.legend(fontsize=8.0, loc='upper left', frameon=False)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.35)
fig.tight_layout(pad=0.4)
```

::: example Worked example 12.14 — tangent and normal at a given point
**Problem.** Find the equations of the tangent and the normal to the curve
$y = x^{3} - 3x + 2$ at the point $(2, 4)$.

**Solution.** First check the point lies on the curve:
$2^{3} - 3(2) + 2 = 8 - 6 + 2 = 4$ ✓.

$$ \frac{dy}{dx} = 3x^{2} - 3 \;\Longrightarrow\;
m = \left.\frac{dy}{dx}\right|_{x=2} = 3(4) - 3 = 9 $$

**Tangent:** $y - 4 = 9(x - 2)$, that is

$$ y = 9x - 14 \qquad\text{or}\qquad 9x - y - 14 = 0 $$

**Normal:** slope $= -\dfrac19$, so $y - 4 = -\dfrac19(x-2)$. Multiply by $9$:

$$ 9y - 36 = -x + 2 \;\Longrightarrow\; x + 9y - 38 = 0 $$
:::

::: example Worked example 12.15 — tangent with a given slope, and an implicit curve
**Problem.** (a) Find the point on the curve $y = x^{3} - 11x + 5$ at which the
tangent is the line $y = x - 11$.
(b) Find the equation of the tangent to the circle $x^{2} + y^{2} = 25$ at
$(3, 4)$.

**Solution.**

**(a)** The given line has slope $1$, so we need
$\dfrac{dy}{dx} = 3x^{2} - 11 = 1$, giving $x^{2} = 4$, $x = \pm 2$.

- At $x = 2$: $y = 8 - 22 + 5 = -9$. The line at $x=2$ gives $y = 2 - 11 = -9$ ✓
  — the point $(2, -9)$ is on both.
- At $x = -2$: $y = -8 + 22 + 5 = 19$, but the line gives $y = -13$ ✗ — here the
  tangent is *parallel* to the line, not the line itself.

Hence the required point is $(2, -9)$.

**(b)** Differentiate implicitly:

$$ 2x + 2y\frac{dy}{dx} = 0 \;\Longrightarrow\; \frac{dy}{dx} = -\frac{x}{y}
\;\Longrightarrow\; m = -\frac34 \text{ at } (3,4) $$

$$ y - 4 = -\frac34(x - 3) \;\Longrightarrow\; 4y - 16 = -3x + 9
\;\Longrightarrow\; 3x + 4y = 25 $$

(Consistent with the Unit 8 result that the tangent to $x^2+y^2=a^2$ at
$(x_1,y_1)$ is $xx_{1} + yy_{1} = a^{2}$.)
:::

::: key Angle of intersection of two curves
The angle between two curves at a point of intersection is the angle between
their tangents there. If the slopes are $m_{1}$ and $m_{2}$,

$$ \tan\theta = \left|\frac{m_{1}-m_{2}}{1+m_{1}m_{2}}\right| $$

The curves are **orthogonal** (cut at right angles) if $m_{1}m_{2} = -1$, and
**touch** each other if $m_{1} = m_{2}$.
:::

::: example Worked example 12.16 — angle between two curves
**Problem.** Find the angle of intersection of the curves $y = x^{2}$ and
$y^{2} = x$ at the point other than the origin.

**Solution.** **Points of intersection.** Substitute $y = x^{2}$ into
$y^{2} = x$:

$$ x^{4} = x \;\Longrightarrow\; x(x^{3}-1) = 0 \;\Longrightarrow\; x = 0
\text{ or } x = 1 $$

So the required point is $(1, 1)$.

**Slopes there.** For $y = x^{2}$: $\dfrac{dy}{dx} = 2x$, so $m_{1} = 2$.

For $y^{2} = x$, differentiate implicitly: $2y\dfrac{dy}{dx} = 1$, so
$\dfrac{dy}{dx} = \dfrac{1}{2y}$ and $m_{2} = \dfrac12$.

**Angle.**

$$ \tan\theta = \left|\frac{2 - \frac12}{1 + 2\cdot\frac12}\right|
= \left|\frac{3/2}{2}\right| = \frac34 $$

$$ \theta = \tan^{-1}\frac34 \approx 36^{\circ}52' $$
:::

::: tip Always check the point is on the curve
Substitute the given coordinates into the equation of the curve before you
differentiate. If they do not satisfy it, the question is asking for a tangent
*from* an external point, which is a different (and longer) calculation.
:::

## 12.5 Derivative as a rate measure

If $y$ depends on $x$, then $\dfrac{dy}{dx}$ is the rate at which $y$ changes per
unit change in $x$. When both depend on time, the chain rule links their rates:

$$ \frac{dy}{dt} = \frac{dy}{dx}\cdot\frac{dx}{dt} $$

These are called **related rates** problems.

::: key Method for a related-rates problem
1. Draw a diagram and name the varying quantities with letters, not numbers.
2. Write the equation connecting them (geometry, usually).
3. Differentiate the whole equation **with respect to $t$**.
4. *Now* substitute the numerical values for the instant asked about.
5. State the answer with units, and say whether it is increasing or decreasing —
   a negative rate means decreasing.
:::

The same idea is used far beyond geometry. If $C(x)$ is the cost of producing
$x$ items, $\dfrac{dC}{dx}$ is the **marginal cost** — the extra cost of one more
item. If $Q$ is the charge flowing past a point in a wire,
$\dfrac{dQ}{dt}$ is the current. In every case the derivative answers the
question *"per unit of what, how much of this?"*

::: caution Substitute the numbers last
If you put $r = 15$ into $V = \frac43\pi r^{3}$ before differentiating, $V$
becomes a constant and $\dfrac{dV}{dt}$ comes out as zero. Differentiate first,
substitute second.
:::

```figure caption="A ladder of fixed length $5$ m slides down a wall. Because $x^{2}+y^{2}=25$ always holds, differentiating with respect to $t$ gives $x\\frac{dx}{dt} + y\\frac{dy}{dt} = 0$. At the instant $x = 4$, $y = 3$, so a foot speed of $2$ m s⁻¹ outward forces the top down at $\\frac{8}{3}$ m s⁻¹ — faster than the foot moves."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4, 3.2))
ax.plot([0, 0], [0, 5.4], color=INK, lw=2.5)
ax.plot([-0.4, 5.6], [0, 0], color=INK, lw=2.5)
for xx in np.arange(-0.3, 5.6, 0.45):
    ax.plot([xx, xx-0.25], [0, -0.28], color=MUTED, lw=0.8)
for yy in np.arange(0.2, 5.3, 0.45):
    ax.plot([0, -0.28], [yy, yy-0.25], color=MUTED, lw=0.8)
ax.plot([0, 4], [3, 0], color='#d9534f', lw=2.6)
ax.plot([0, 3.1], [4, 0], color=MUTED, lw=1.3, ls='--')
ax.text(2.25, 1.95, '5 m', fontsize=9.6, color='#d9534f', rotation=-37)
ax.plot([0, 4], [0, 0], color=ACCENT, lw=0)
ax.annotate('', xy=(4.0, -0.62), xytext=(0, -0.62),
            arrowprops=dict(arrowstyle='<->', color=ACCENT, lw=1.1))
ax.text(2.0, -1.05, 'x = 4 m', ha='center', fontsize=9.0, color=ACCENT)
ax.annotate('', xy=(-0.75, 3.0), xytext=(-0.75, 0),
            arrowprops=dict(arrowstyle='<->', color='#2e8b57', lw=1.1))
ax.text(-0.95, 1.5, 'y = 3 m', ha='right', va='center', fontsize=9.0,
        color='#2e8b57', rotation=90)
ax.annotate('', xy=(5.25, 0.30), xytext=(4.05, 0.30),
            arrowprops=dict(arrowstyle='->', color=ACCENT, lw=1.6))
ax.text(5.35, 0.30, 'dx/dt = 2 m s⁻¹', fontsize=8.6, color=ACCENT,
        ha='left', va='center')
ax.annotate('', xy=(0.30, 1.75), xytext=(0.30, 2.95),
            arrowprops=dict(arrowstyle='->', color='#2e8b57', lw=1.6))
ax.annotate('dy/dt = −8/3 m s⁻¹', xy=(0.42, 2.30), xytext=(1.45, 4.85),
            fontsize=8.6, color='#2e8b57', ha='left', va='center',
            arrowprops=dict(arrowstyle='->', color='#2e8b57', lw=0.9))
ax.text(3.35, 1.05, 'earlier\nposition', fontsize=7.6, color=MUTED, ha='left')
ax.plot([0.42, 0.42, 0], [0, 0.42, 0.42], color=MUTED, lw=0.9)
ax.set_xlim(-2.0, 9.4); ax.set_ylim(-1.5, 5.6)
ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: example Worked example 12.17 — expanding balloon
**Problem.** Air is pumped into a spherical balloon at $100$ cm³ s⁻¹. Find the
rate at which the radius is increasing when the radius is $15$ cm. Find also the
rate of increase of the surface area at that instant.

**Solution.** Let $V$, $S$ and $r$ be the volume, surface area and radius at time
$t$. Then $V = \dfrac43\pi r^{3}$ and $S = 4\pi r^{2}$.

Differentiate $V$ with respect to $t$ (chain rule):

$$ \frac{dV}{dt} = 4\pi r^{2}\frac{dr}{dt} $$

Substitute $\dfrac{dV}{dt} = 100$ and $r = 15$:

$$ 100 = 4\pi(225)\frac{dr}{dt} \;\Longrightarrow\;
\frac{dr}{dt} = \frac{100}{900\pi} = \frac{1}{9\pi} \approx 0.0354\ \text{cm s}^{-1} $$

For the surface area,

$$ \frac{dS}{dt} = 8\pi r\frac{dr}{dt} = 8\pi(15)\cdot\frac{1}{9\pi}
= \frac{120}{9} = \frac{40}{3} \approx 13.33\ \text{cm}^{2}\,\text{s}^{-1} $$
:::

::: example Worked example 12.18 — the sliding ladder
**Problem.** A ladder $5$ m long rests against a vertical wall. The foot of the
ladder is pulled away from the wall at $2$ m s⁻¹. How fast is the top sliding
down the wall when the foot is $4$ m from the wall?

**Solution.** Let $x$ be the distance of the foot from the wall and $y$ the
height of the top, at time $t$. By Pythagoras the ladder length is constant:

$$ x^{2} + y^{2} = 25 $$

Differentiate with respect to $t$:

$$ 2x\frac{dx}{dt} + 2y\frac{dy}{dt} = 0 \;\Longrightarrow\;
\frac{dy}{dt} = -\frac{x}{y}\cdot\frac{dx}{dt} $$

When $x = 4$: $y = \sqrt{25 - 16} = 3$, and $\dfrac{dx}{dt} = 2$:

$$ \frac{dy}{dt} = -\frac43 \times 2 = -\frac83 \approx -2.67\ \text{m s}^{-1} $$

The negative sign means $y$ is **decreasing**: the top slides down at
$\dfrac83$ m s⁻¹.
:::

### Derivative as velocity and acceleration

The oldest use of the derivative is in mechanics. If a particle moves along a
straight line so that its displacement at time $t$ is $s = f(t)$, then

$$ \text{velocity } v = \frac{ds}{dt}, \qquad
\text{acceleration } a = \frac{dv}{dt} = \frac{d^{2}s}{dt^{2}} $$

The particle is **momentarily at rest** when $v = 0$, is moving forward when
$v > 0$ and backward when $v < 0$. Speed is $|v|$, which is why a particle can
have negative velocity and increasing speed at the same time.

::: example Worked example 12.19 — water filling a cone
**Problem.** Water is poured into an inverted right circular cone at the rate of
$3$ m³ min⁻¹. The cone is $10$ m deep and its base radius is $5$ m. Find the rate
at which the water level is rising when the water is $4$ m deep.

**Solution.** Let $h$ be the depth of water and $r$ the radius of the water
surface at time $t$. By similar triangles (the water cone is similar to the whole
cone),

$$ \frac{r}{h} = \frac{5}{10} = \frac12 \;\Longrightarrow\; r = \frac{h}{2} $$

This is the constraint that removes $r$. The volume of water is

$$ V = \frac13\pi r^{2}h = \frac13\pi\left(\frac{h}{2}\right)^{2}h
= \frac{\pi h^{3}}{12} $$

Differentiate with respect to $t$:

$$ \frac{dV}{dt} = \frac{\pi}{12}\cdot 3h^{2}\frac{dh}{dt}
= \frac{\pi h^{2}}{4}\frac{dh}{dt} $$

Now substitute $\dfrac{dV}{dt} = 3$ and $h = 4$:

$$ 3 = \frac{\pi(16)}{4}\frac{dh}{dt} = 4\pi\frac{dh}{dt}
\;\Longrightarrow\; \frac{dh}{dt} = \frac{3}{4\pi} \approx 0.239\ \text{m min}^{-1} $$

Note that $\dfrac{dh}{dt}$ is proportional to $\dfrac{1}{h^{2}}$: the deeper the
water, the more slowly the level rises.
:::

::: example Worked example 12.20 — motion of a particle
**Problem.** A particle moves along a straight line so that its displacement
after $t$ seconds is $s = t^{3} - 6t^{2} + 9t + 4$ metres. Find (a) its initial
velocity, (b) the times when it is momentarily at rest and its displacement then,
(c) its acceleration at those times.

**Solution.**

$$ v = \frac{ds}{dt} = 3t^{2} - 12t + 9 = 3(t-1)(t-3), \qquad
a = \frac{dv}{dt} = 6t - 12 $$

**(a)** Initial velocity is $v$ at $t = 0$: $v = 9$ m s⁻¹.

**(b)** At rest when $v = 0$, that is $t = 1$ s and $t = 3$ s.

$$ s(1) = 1 - 6 + 9 + 4 = 8\ \text{m}, \qquad
s(3) = 27 - 54 + 27 + 4 = 4\ \text{m} $$

**(c)** $a(1) = 6 - 12 = -6$ m s⁻² and $a(3) = 18 - 12 = 6$ m s⁻².

Between $t = 1$ and $t = 3$ the velocity is negative, so the particle moves
*backwards* by $8 - 4 = 4$ m before turning round again.
:::

## 12.6 Increasing and decreasing functions

::: definition Monotonic functions
A function $f$ is **increasing** on an interval $I$ if
$x_{1} < x_{2} \Rightarrow f(x_{1}) \le f(x_{2})$ for all $x_1, x_2 \in I$, and
**decreasing** if $x_{1} < x_{2} \Rightarrow f(x_{1}) \ge f(x_{2})$. Strict
inequalities give *strictly* increasing/decreasing.
:::

::: key The sign of $f'$ tells you everything
On an interval where $f$ is differentiable:

| Sign of $f'(x)$ | Behaviour of $f$ | Tangent |
|---|---|---|
| $f'(x) > 0$ | strictly increasing | slopes upward |
| $f'(x) < 0$ | strictly decreasing | slopes downward |
| $f'(x) = 0$ | stationary | horizontal |

So: differentiate, factorise $f'(x)$, find where it is zero, and test the sign of
$f'$ in each interval those roots create.
:::

```figure caption="$f(x) = 2x^{3} - 9x^{2} + 12x + 5$ above its derivative $f'(x) = 6(x-1)(x-2)$, drawn on the same $x$-axis. Where $f'$ is above the axis (green) $f$ rises; where $f'$ dips below (red) $f$ falls; the two zeros of $f'$ sit exactly under the turning points of $f$."
import numpy as np, matplotlib.pyplot as plt
fig, (a1, a2) = plt.subplots(2, 1, figsize=(4.8, 4.2), sharex=True,
                             gridspec_kw={'height_ratios': [1.25, 1]})
x = np.linspace(-0.2, 3.2, 500)
f = 2*x**3 - 9*x**2 + 12*x + 5
fp = 6*(x-1)*(x-2)
a1.plot(x, f, color=ACCENT, lw=2.0)
a1.plot([1, 2], [2-9+12+5, 16-36+24+5], 'o', color=INK, ms=5.5, zorder=5)
a1.text(1.0, 11.2, 'local max\n(1, 10)', ha='center', fontsize=8.2, color=INK)
a1.text(2.0, 6.6, 'local min\n(2, 9)', ha='center', fontsize=8.2, color=INK)
a1.set_ylabel('f(x)', fontsize=9.0)
a1.set_ylim(3.5, 14.5)
a2.plot(x, fp, color=INK, lw=1.8)
a2.fill_between(x, fp, 0, where=(fp > 0), color='#2e8b57', alpha=0.28)
a2.fill_between(x, fp, 0, where=(fp <= 0), color='#d9534f', alpha=0.28)
a2.axhline(0, color=INK, lw=1.0)
a2.set_ylabel("f '(x)", fontsize=9.0); a2.set_xlabel('x', fontsize=9.0)
a2.text(0.38, 1.5, "f ' > 0\nrising", ha='center', va='center',
        fontsize=8.2, color='#2e8b57')
a2.text(1.50, -3.6, "f ' < 0   falling", ha='center', va='center',
        fontsize=8.2, color='#d9534f')
a2.text(2.62, 1.5, "f ' > 0\nrising", ha='center', va='center',
        fontsize=8.2, color='#2e8b57')
a2.set_ylim(-5.5, 10.5)
for ax in (a1, a2):
    for xv in (1, 2):
        ax.axvline(xv, color=MUTED, lw=0.9, ls=':')
    ax.spines[['top','right']].set_visible(False)
    ax.grid(True, alpha=.30)
a2.set_xticks([0, 1, 2, 3])
fig.tight_layout(pad=0.4, h_pad=0.6)
```

::: example Worked example 12.21 — intervals of increase and decrease
**Problem.** Find the intervals in which
$f(x) = 2x^{3} - 9x^{2} + 12x + 5$ is increasing and decreasing.

**Solution.**

$$ f'(x) = 6x^{2} - 18x + 12 = 6(x^{2} - 3x + 2) = 6(x-1)(x-2) $$

$f'(x) = 0$ at $x = 1$ and $x = 2$. These split the real line into three
intervals; test the sign of each factor in each.

| Interval | $(x-1)$ | $(x-2)$ | $f'(x)$ | $f$ is |
|---|---|---|---|---|
| $x < 1$ | $-$ | $-$ | $+$ | increasing |
| $1 < x < 2$ | $+$ | $-$ | $-$ | decreasing |
| $x > 2$ | $+$ | $+$ | $+$ | increasing |

So $f$ is increasing on $(-\infty, 1)$ and $(2, \infty)$, and decreasing on
$(1, 2)$.
:::

## 12.7 Maxima and minima

::: definition Local extrema and stationary points
$f$ has a **local maximum** at $x = c$ if $f(c) \ge f(x)$ for all $x$ near $c$,
and a **local minimum** if $f(c) \le f(x)$ for all $x$ near $c$. A point where
$f'(c) = 0$ is called a **stationary** (or critical) point. Every local extremum
of a differentiable function is a stationary point — but not every stationary
point is an extremum.
:::

::: key First and second derivative tests
**Step 1.** Solve $f'(x) = 0$ to find the stationary points $x = c$.

**Step 2 — second derivative test.** Compute $f''(c)$:

| $f''(c)$ | Conclusion |
|---|---|
| $f''(c) < 0$ | local **maximum** at $c$ |
| $f''(c) > 0$ | local **minimum** at $c$ |
| $f''(c) = 0$ | test fails — use the first derivative test |

**First derivative test.** If $f'$ changes from $+$ to $-$ as $x$ increases
through $c$, it is a maximum; from $-$ to $+$, a minimum; no change of sign, it
is a point of inflection with a horizontal tangent.
:::

::: memory Which way round?
$f'' < 0$ means the slope is *falling*, so the curve bends downward like a
frown — that is a **maximum**. $f'' > 0$ bends upward like a smile — a
**minimum**. *Negative is a frown; positive is a smile.*
:::

```figure caption="$f(x) = x^{4} - 4x^{3} + 10$ carries all three features at once. At $x = 3$, $f'' = 36 > 0$: a local minimum. At $x = 0$ the tangent is horizontal but $f'' = 0$ and $f'$ does not change sign, so $(0, 10)$ is a point of inflection, not an extremum. At $x = 2$, $f''$ changes sign again, giving a second inflection at $(2, -6)$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0, 3.3))
x = np.linspace(-0.85, 3.75, 600)
f = lambda t: t**4 - 4*t**3 + 10
ax.plot(x, f(x), color=ACCENT, lw=2.1)
pts = [(0, 'inflection  (0, 10)\nf ′ = 0, f ″ = 0', (-4, -46), '#b8860b'),
       (2, 'inflection  (2, −6)\nf ″ changes sign', (46, 30), '#b8860b'),
       (3, 'minimum  (3, −17)\nf ′ = 0, f ″ = 36 > 0', (-16, -42), '#2e8b57')]
for xv, lab, off, col in pts:
    ax.plot([xv], [f(xv)], 'o', color=col, ms=6.5, zorder=6)
    ax.annotate(lab, xy=(xv, f(xv)), xytext=off, textcoords='offset points',
                fontsize=8.0, color=col, ha='center',
                arrowprops=dict(arrowstyle='->', color=col, lw=0.9))
for xv in (0, 3):
    ax.plot([xv-0.5, xv+0.5], [f(xv), f(xv)], color=MUTED, lw=1.2, ls='--')
ax.axvspan(-0.85, 0, color='#2e8b57', alpha=0.07)
ax.axvspan(0, 2, color='#d9534f', alpha=0.08)
ax.axvspan(2, 3.75, color='#2e8b57', alpha=0.07)
ax.text(-0.45, 27.5, 'f ″ > 0', ha='center', va='center', fontsize=7.8, color='#2e8b57')
ax.text(1.0, 27.5, 'f ″ < 0   concave down', ha='center', va='center',
        fontsize=7.8, color='#d9534f')
ax.text(2.9, 27.5, 'f ″ > 0   concave up', ha='center', va='center',
        fontsize=7.8, color='#2e8b57')
ax.axhline(0, color=INK, lw=0.8)
ax.set_xlim(-0.9, 3.8); ax.set_ylim(-34, 32)
ax.set_xlabel('x', fontsize=9.0); ax.set_ylabel('f(x)', fontsize=9.0)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.30)
fig.tight_layout(pad=0.4)
```

::: example Worked example 12.22 — local maximum and minimum
**Problem.** Find the local maximum and minimum values of
$f(x) = x^{3} - 6x^{2} + 9x + 15$.

**Solution.**

$$ f'(x) = 3x^{2} - 12x + 9 = 3(x-1)(x-3) = 0 \;\Longrightarrow\; x = 1,\ 3 $$

$$ f''(x) = 6x - 12 $$

At $x = 1$: $f''(1) = 6 - 12 = -6 < 0$, so there is a local **maximum**, of value

$$ f(1) = 1 - 6 + 9 + 15 = 19 $$

At $x = 3$: $f''(3) = 18 - 12 = 6 > 0$, so there is a local **minimum**, of value

$$ f(3) = 27 - 54 + 27 + 15 = 15 $$

Note the "maximum" $19$ is larger than the "minimum" $15$ only locally — the
cubic itself is unbounded in both directions.
:::

```figure caption="Making an open box from a square sheet of side $18$ cm: cut a square of side $x$ from each corner and fold up the flaps. The base is $(18-2x)$ by $(18-2x)$ and the height is $x$, so $V = x(18-2x)^{2}$. The graph on the right shows $V$ peaking at $x = 3$ cm, where $V = 432$ cm³; $x = 9$ is the other root of $V' = 0$ but there the box has no base at all."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.2, 2.8),
                             gridspec_kw={'width_ratios': [1, 1.15]})
S, xc = 18.0, 3.0
a1.add_patch(Rectangle((0, 0), S, S, fc='none', ec=INK, lw=1.6))
for (cx, cy) in [(0, 0), (S-xc, 0), (0, S-xc), (S-xc, S-xc)]:
    a1.add_patch(Rectangle((cx, cy), xc, xc, fc='#d9534f', ec='#d9534f',
                           lw=1.0, alpha=0.30, hatch='//'))
a1.add_patch(Rectangle((xc, xc), S-2*xc, S-2*xc, fc=ACCENT, ec=ACCENT,
                       lw=1.2, alpha=0.16))
a1.plot([xc, xc], [0, S], color=MUTED, lw=0.9, ls='--')
a1.plot([S-xc, S-xc], [0, S], color=MUTED, lw=0.9, ls='--')
a1.plot([0, S], [xc, xc], color=MUTED, lw=0.9, ls='--')
a1.plot([0, S], [S-xc, S-xc], color=MUTED, lw=0.9, ls='--')
a1.text(S/2, S/2, 'base\n(18 − 2x)\n× (18 − 2x)', ha='center', va='center',
        fontsize=8.0, color=INK)
a1.annotate('', xy=(xc, -1.3), xytext=(0, -1.3),
            arrowprops=dict(arrowstyle='<->', color='#d9534f', lw=1.0))
a1.text(1.5, -3.3, 'x', ha='center', fontsize=9.0, color='#d9534f')
a1.annotate('', xy=(S, -1.3), xytext=(xc, -1.3),
            arrowprops=dict(arrowstyle='<->', color=MUTED, lw=1.0))
a1.text(10.5, -3.3, '18 cm', ha='center', fontsize=8.6, color=MUTED)
a1.text(S/2, S+1.2, 'cut the 4 corners, fold up', ha='center', fontsize=8.2,
        color=MUTED)
a1.set_xlim(-2.5, 20.5); a1.set_ylim(-5.0, 21.5)
a1.set_aspect('equal'); a1.axis('off')
xs = np.linspace(0, 9, 300)
a2.plot(xs, xs*(18-2*xs)**2, color=ACCENT, lw=2.0)
a2.plot([3], [432], 'o', color='#d9534f', ms=6.5, zorder=5)
a2.plot([0, 3], [432, 432], color=MUTED, lw=0.9, ls=':')
a2.plot([3, 3], [0, 432], color=MUTED, lw=0.9, ls=':')
a2.annotate('max V = 432 cm³\nat x = 3 cm', xy=(3, 432), xytext=(13, 6),
            textcoords='offset points', fontsize=8.2, color='#d9534f')
a2.set_xlabel('x (cm)', fontsize=8.8); a2.set_ylabel('V (cm³)', fontsize=8.8)
a2.set_xticks([0, 3, 6, 9]); a2.set_xlim(0, 9.4); a2.set_ylim(0, 560)
a2.spines[['top','right']].set_visible(False)
a2.grid(True, alpha=.35)
fig.tight_layout(pad=0.4)
```

::: example Worked example 12.23 — applied optimisation: the open box
**Problem.** A square sheet of tin of side $18$ cm has a small square cut from
each corner, and the flaps are folded up to make an open box. Find the side of
the square cut off so that the volume of the box is a maximum, and find that
maximum volume.

**Solution.** Let $x$ cm be the side of the square cut from each corner, where
$0 < x < 9$. The base is a square of side $18 - 2x$ and the height is $x$, so

$$ V = x(18 - 2x)^{2} $$

Differentiate by the product rule:

$$ \frac{dV}{dx} = (18-2x)^{2} + x\cdot 2(18-2x)(-2)
= (18-2x)\left[(18-2x) - 4x\right] $$
$$ = (18-2x)(18 - 6x) = 12(9-x)(3-x) $$

Set $\dfrac{dV}{dx} = 0$: $x = 9$ or $x = 3$. Reject $x = 9$ (then the base has
side $0$ and $V = 0$), leaving $x = 3$.

$$ \frac{d^{2}V}{dx^{2}} = 12\left[-(3-x) - (9-x)\right] = 12(2x - 12)
= 24x - 144 $$

At $x = 3$: $\dfrac{d^{2}V}{dx^{2}} = 72 - 144 = -72 < 0$, confirming a
**maximum**. Hence

$$ V_{\max} = 3(18-6)^{2} = 3 \times 144 = 432\ \text{cm}^{3} $$

The square cut from each corner should have side $3$ cm.
:::

::: example Worked example 12.24 — applied optimisation: cylinder in a sphere
**Problem.** Show that the cylinder of greatest volume that can be inscribed in a
sphere of radius $R$ has height $\dfrac{2R}{\sqrt{3}}$, and find that volume.

**Solution.** Let the cylinder have radius $r$ and height $h$. Its axis passes
through the centre of the sphere, so a radius of the sphere, half the height, and
the cylinder's radius form a right triangle:

$$ r^{2} + \frac{h^{2}}{4} = R^{2} \;\Longrightarrow\; r^{2} = R^{2} - \frac{h^{2}}{4} $$

This is the constraint that removes one variable. The volume is

$$ V = \pi r^{2} h = \pi\left(R^{2} - \frac{h^{2}}{4}\right)h
= \pi R^{2}h - \frac{\pi h^{3}}{4} $$

Now $R$ is a constant and $h$ is the only variable:

$$ \frac{dV}{dh} = \pi R^{2} - \frac{3\pi h^{2}}{4} = 0
\;\Longrightarrow\; h^{2} = \frac{4R^{2}}{3} \;\Longrightarrow\;
h = \frac{2R}{\sqrt{3}} $$

$$ \frac{d^{2}V}{dh^{2}} = -\frac{3\pi h}{2} < 0 \quad\text{for } h > 0 $$

so this is a maximum. The volume is

$$ V_{\max} = \pi\left(R^{2} - \frac{1}{4}\cdot\frac{4R^{2}}{3}\right)\frac{2R}{\sqrt{3}}
= \pi\cdot\frac{2R^{2}}{3}\cdot\frac{2R}{\sqrt{3}} = \frac{4\pi R^{3}}{3\sqrt{3}} $$

which is $\dfrac{4\sqrt{3}\,\pi R^{3}}{9} \approx 0.7698 R^{3}$, about $58\%$ of the
sphere's own volume $\frac43\pi R^{3}$.
:::

::: definition Absolute (global) extrema on a closed interval
On a closed interval $[a, b]$ a continuous function always attains a largest and
a smallest value. They occur either at a stationary point inside the interval or
at an endpoint. So: **evaluate $f$ at every stationary point in $[a,b]$ and at
both endpoints, and compare the list.** No second derivative test is needed.
:::

::: example Worked example 12.25 — absolute maximum and minimum
**Problem.** Find the absolute maximum and minimum values of
$f(x) = 2x^{3} - 24x + 107$ on the interval $[1, 3]$.

**Solution.**

$$ f'(x) = 6x^{2} - 24 = 6(x-2)(x+2) = 0 \;\Longrightarrow\; x = 2 \text{ or } x = -2 $$

Only $x = 2$ lies in $[1, 3]$; discard $x = -2$. Now evaluate $f$ at that point
and at both endpoints:

| $x$ | $1$ (endpoint) | $2$ (stationary) | $3$ (endpoint) |
|---|---|---|---|
| $f(x)$ | $2 - 24 + 107 = 85$ | $16 - 48 + 107 = 75$ | $54 - 72 + 107 = 89$ |

The **absolute maximum** is $89$, at $x = 3$, and the **absolute minimum** is
$75$, at $x = 2$. Notice that the maximum occurs at an endpoint, where
$f'(x) \ne 0$ — which is why endpoints must always be tested.
:::

::: caution Three marks lost every year in optimisation questions
1. **Not reducing to one variable.** You cannot differentiate $V = \pi r^{2}h$
   with respect to $h$ while $r$ still depends on $h$ — substitute the constraint
   first.
2. **Not rejecting impossible roots.** $x = 9$ in the open-box problem is a root
   of $\frac{dV}{dx} = 0$, but it is outside the domain $0 < x < 9$; say so.
3. **Not applying the test.** Writing "maximum" because the answer looks right
   earns nothing. State $f''(c) < 0$ (or the sign change of $f'$) explicitly.
:::

::: tip Structure of every optimisation answer
Write the quantity to be optimised; use the constraint to reduce it to **one**
variable; state the domain; differentiate; solve $=0$; reject impossible roots
with a reason; apply the second derivative test; compute the optimal value;
answer the question in words with units. Eight marks, eight steps.
:::

## 12.8 Concavity and points of inflection

The first derivative says whether a curve rises or falls. The **second**
derivative says which way it bends.

::: definition Concavity and points of inflection
A curve is **concave upward** on an interval if it lies above all its tangents
there, and **concave downward** if it lies below them. Then

$$ f''(x) > 0 \Rightarrow \text{concave upward}, \qquad
f''(x) < 0 \Rightarrow \text{concave downward} $$

A **point of inflection** is a point at which the concavity changes. At such a
point $f''(x) = 0$ (or fails to exist) **and** $f''$ changes sign there.
:::

```figure caption="Left: $f'' > 0$, the curve is concave upward and lies above every tangent, and the slopes of the tangents (dashed) increase from left to right. Right: $f'' < 0$, concave downward, lying below its tangents with slopes decreasing. The point of inflection is where the two behaviours meet."
import numpy as np, matplotlib.pyplot as plt
fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.2, 2.5), sharey=False)
for ax, sgn, ttl, col in ((a1, 1, "f ″ > 0 : concave up", '#2e8b57'),
                          (a2, -1, "f ″ < 0 : concave down", '#d9534f')):
    x = np.linspace(-1.6, 1.6, 300)
    y = sgn*0.75*x**2
    ax.plot(x, y, color=ACCENT, lw=2.1)
    for x0 in (-1.1, 0.0, 1.1):
        m = sgn*1.5*x0; y0 = sgn*0.75*x0**2
        xt = np.linspace(x0-0.62, x0+0.62, 10)
        ax.plot(xt, y0 + m*(xt-x0), color=col, lw=1.1, ls='--')
        ax.plot([x0], [y0], 'o', color=col, ms=3.6)
    seq = 'slopes increase:  −1.7  →  0  →  +1.7' if sgn > 0 \
          else 'slopes decrease:  +1.7  →  0  →  −1.7'
    ax.text(0, -1.95*sgn, seq, ha='center', va='center', fontsize=7.8, color=col)
    ax.text(0, -1.95*sgn + sgn*0.42, 'curve lies above its tangents' if sgn > 0
            else 'curve lies below its tangents',
            ha='center', va='center', fontsize=7.4, color=MUTED)
    ax.set_title(ttl, fontsize=8.6, pad=3, color=col)
    ax.set_ylim(-2.4, 2.4)
    ax.axhline(0, color=INK, lw=0.8)
    ax.set_xticks([]); ax.set_yticks([])
    ax.spines[['top','right','left','bottom']].set_visible(False)
fig.tight_layout(pad=0.4)
```

::: example Worked example 12.26 — concavity and inflection
**Problem.** For $f(x) = x^{4} - 4x^{3} + 10$, find the intervals of concavity,
the points of inflection, and the local extrema.

**Solution.**

$$ f'(x) = 4x^{3} - 12x^{2} = 4x^{2}(x - 3), \qquad
f''(x) = 12x^{2} - 24x = 12x(x-2) $$

**Stationary points.** $f'(x) = 0$ at $x = 0$ and $x = 3$.

- At $x = 3$: $f''(3) = 12(3)(1) = 36 > 0$, so a local **minimum**, value
  $f(3) = 81 - 108 + 10 = -17$.
- At $x = 0$: $f''(0) = 0$, so the second derivative test fails. Use the first
  derivative test: $f'(x) = 4x^{2}(x-3)$ is negative on both sides of $0$
  (because $4x^{2} > 0$ and $x - 3 < 0$), so $f'$ does **not** change sign.
  Hence $(0, 10)$ is not an extremum.

**Concavity.** $f''(x) = 12x(x-2) = 0$ at $x = 0$ and $x = 2$.

| Interval | $12x$ | $(x-2)$ | $f''$ | Concavity |
|---|---|---|---|---|
| $x < 0$ | $-$ | $-$ | $+$ | upward |
| $0 < x < 2$ | $+$ | $-$ | $-$ | downward |
| $x > 2$ | $+$ | $+$ | $+$ | upward |

$f''$ changes sign at both $x = 0$ and $x = 2$, so there are **two points of
inflection**: $(0, 10)$ and $(2, -6)$, since $f(2) = 16 - 32 + 10 = -6$.
:::

## Chapter summary

- The standard derivatives, the product, quotient and chain rules, and the
  techniques for implicit ($y$ gives a factor $\frac{dy}{dx}$), parametric
  ($\frac{dy}{dx} = \frac{dy/dt}{dx/dt}$) and logarithmic differentiation (take
  $\ln$ of both sides, for $u^{v}$ forms) are the working toolkit.
- Hyperbolic: $\sinh x = \frac{e^{x}-e^{-x}}{2}$, $\cosh x = \frac{e^{x}+e^{-x}}{2}$,
  $\cosh^{2}x-\sinh^{2}x=1$, and
  $(\sinh x)' = \cosh x$, $(\cosh x)' = \sinh x$, $(\tanh x)' = \mathrm{sech}^{2}x$.
  Inverses: $(\sinh^{-1}x)' = \frac{1}{\sqrt{x^{2}+1}}$,
  $(\cosh^{-1}x)' = \frac{1}{\sqrt{x^{2}-1}}$,
  $(\tanh^{-1}x)' = \frac{1}{1-x^{2}}$.
- **L'Hospital:** for $\frac00$ or $\frac{\infty}{\infty}$ only,
  $\lim\frac{f}{g} = \lim\frac{f'}{g'}$, repeated as needed. Convert
  $0\cdot\infty$, $\infty-\infty$, $0^{0}$, $1^{\infty}$ to a quotient first.
- **Differentials:** $dy = f'(x)dx$ and
  $f(x+\Delta x)\approx f(x) + f'(x)\Delta x$; relative error
  $\frac{dy}{y}$.
- **Tangent** at $(x_1,y_1)$: $y-y_1 = m(x-x_1)$ with
  $m = f'(x_1)$; **normal**: $y-y_1 = -\frac{1}{m}(x-x_1)$.
- **Angle between curves:**
  $\tan\theta = \left|\frac{m_1-m_2}{1+m_1m_2}\right|$; orthogonal if
  $m_1m_2=-1$.
- **Rates:** $\frac{dy}{dt} = \frac{dy}{dx}\cdot\frac{dx}{dt}$; differentiate the
  relation with respect to $t$, then substitute. In motion,
  $v = \frac{ds}{dt}$ and $a = \frac{d^{2}s}{dt^{2}}$.
- $f' > 0 \Rightarrow$ increasing; $f' < 0 \Rightarrow$ decreasing;
  $f' = 0 \Rightarrow$ stationary.
- **Second derivative test:** $f'(c)=0$ with $f''(c)<0$ gives a maximum,
  $f''(c)>0$ a minimum, $f''(c)=0$ is inconclusive.
- **Absolute extrema on $[a,b]$:** compare $f$ at every interior stationary
  point and at both endpoints.
- $f''>0$ concave up, $f''<0$ concave down; a **point of inflection** needs
  $f''=0$ *and* a change of sign.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. $\dfrac{d}{dx}(\cosh x)$ is <span class="marks">[1]</span>
   (a) $-\sinh x$ (b) $\sinh x$ (c) $\mathrm{sech}^{2}x$ (d) $\cosh x$
2. $\displaystyle\lim_{x\to0}\frac{1-\cos x}{x^{2}}$ equals <span class="marks">[1]</span>
   (a) $0$ (b) $\dfrac12$ (c) $1$ (d) $2$
3. $\dfrac{d}{dx}\sinh^{-1}(3x)$ is <span class="marks">[1]</span>
   (a) $\dfrac{3}{\sqrt{1-9x^{2}}}$ (b) $\dfrac{3}{\sqrt{9x^{2}+1}}$
   (c) $\dfrac{1}{\sqrt{9x^{2}+1}}$ (d) $\dfrac{3}{9x^{2}+1}$
4. The slope of the normal to $y = x^{2}$ at $(1, 1)$ is <span class="marks">[1]</span>
   (a) $2$ (b) $-2$ (c) $\dfrac12$ (d) $-\dfrac12$
5. If $f''(c) = 0$ and $f''$ changes sign at $c$, the point $x = c$ is a <span class="marks">[1]</span>
   (a) maximum (b) minimum (c) point of inflection (d) none of these
6. If $y = x^{3}$, the approximate change in $y$ when $x$ changes from $2$ to
   $2.01$ is <span class="marks">[1]</span>
   (a) $0.01$ (b) $0.12$ (c) $0.6$ (d) $1.2$
7. $f(x) = x^{3} + 3x$ is <span class="marks">[1]</span>
   (a) increasing for all $x$ (b) decreasing for all $x$
   (c) increasing only for $x>0$ (d) neither
8. $\displaystyle\lim_{x\to0}\frac{a^{x}-b^{x}}{x}$ equals <span class="marks">[1]</span>
   (a) $\ln(ab)$ (b) $\ln\dfrac{a}{b}$ (c) $a - b$ (d) $0$
9. The function $f(x) = x^{3} - 3x$ is decreasing on <span class="marks">[1]</span>
   (a) $(-\infty, -1)$ (b) $(-1, 1)$ (c) $(1, \infty)$ (d) $\mathbb{R}$
10. Two curves cut orthogonally at a point if the slopes $m_{1}$, $m_{2}$ of
    their tangents there satisfy <span class="marks">[1]</span>
    (a) $m_{1} = m_{2}$ (b) $m_{1}m_{2} = 1$ (c) $m_{1}m_{2} = -1$
    (d) $m_{1} + m_{2} = 0$
11. A particle moves with $s = t^{3} - 3t^{2}$. Its acceleration at $t = 2$ is <span class="marks">[1]</span>
    (a) $0$ (b) $6$ (c) $-6$ (d) $12$

::: note Answers to Group A
**1.** (b) — no minus sign, unlike $\dfrac{d}{dx}\cos x$.

**2.** (b) — L'Hospital twice: $\dfrac{\sin x}{2x} \to \dfrac{\cos x}{2} = \dfrac12$.

**3.** (b) — $\dfrac{1}{\sqrt{u^{2}+1}}\cdot 3$ with $u = 3x$.

**4.** (d) — tangent slope $2x = 2$, so normal slope $=-\dfrac12$.

**5.** (c) — that is the definition of a point of inflection.

**6.** (b) — $dy = 3x^{2}dx = 3(4)(0.01) = 0.12$.

**7.** (a) — $f'(x) = 3x^{2}+3 > 0$ for every real $x$.

**8.** (b) — L'Hospital: $\dfrac{a^{x}\ln a - b^{x}\ln b}{1} \to \ln a - \ln b$.

**9.** (b) — $f'(x) = 3(x^{2}-1) < 0$ exactly when $-1 < x < 1$.

**10.** (c) — perpendicular tangents.

**11.** (b) — $a = \dfrac{d^{2}s}{dt^{2}} = 6t - 6 = 6$ at $t = 2$.
:::

**Group B — Short answer (5 marks each)**

1. Differentiate with respect to $x$: (a) $y = \ln(\cosh 3x)$,
   (b) $y = \tanh^{-1}(x^{2})$. <span class="marks">[5]</span>
2. If $y = x^{\sin x}$, find $\dfrac{dy}{dx}$. <span class="marks">[5]</span>
3. Evaluate $\displaystyle\lim_{x\to0}\frac{x - \sin x}{x^{3}}$ using
   L'Hospital's rule. <span class="marks">[5]</span>
4. Find the approximate value of $\sqrt{36.6}$ using differentials. <span class="marks">[5]</span>
5. Find the equations of the tangent and the normal to the curve
   $y = x^{2} - 4x + 3$ at the point where it meets the $y$-axis. <span class="marks">[5]</span>
6. The radius of a circular plate is increasing at $0.02$ cm s⁻¹. Find the rate
   at which its area is increasing when the radius is $10$ cm. <span class="marks">[5]</span>
7. Find the intervals in which $f(x) = x^{3} - 3x^{2} - 9x + 5$ is increasing or
   decreasing, and find its local maximum and minimum values. <span class="marks">[5]</span>
8. Find two positive numbers whose sum is $24$ and whose product of one with the
   square of the other is a maximum. <span class="marks">[5]</span>
9. Water is poured into an inverted right circular cone of depth $10$ m and base
   radius $5$ m at $3$ m³ min⁻¹. Find the rate at which the water level rises
   when the water is $4$ m deep. <span class="marks">[5]</span>
10. Find the absolute maximum and minimum values of
    $f(x) = 2x^{3} - 24x + 107$ on the interval $[1, 3]$. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** (a) Chain rule, outer $\ln u$ with $u = \cosh 3x$:

$$ \frac{dy}{dx} = \frac{1}{\cosh 3x}\cdot\sinh 3x\cdot 3 = 3\tanh 3x $$

(b) Standard derivative $\dfrac{d}{dx}\tanh^{-1}u = \dfrac{1}{1-u^{2}}\dfrac{du}{dx}$
with $u = x^{2}$:

$$ \frac{dy}{dx} = \frac{1}{1-x^{4}}\cdot 2x = \frac{2x}{1-x^{4}},
\qquad |x| < 1 $$

**2.** Take logarithms: $\ln y = \sin x\,\ln x$. Differentiate both sides with
respect to $x$ (product rule on the right):

$$ \frac{1}{y}\frac{dy}{dx} = \cos x\,\ln x + \sin x\cdot\frac1x $$

$$ \frac{dy}{dx} = x^{\sin x}\left(\cos x\,\ln x + \frac{\sin x}{x}\right) $$

**3.** At $x=0$ the form is $\dfrac00$, so the rule applies (three times):

$$ \lim_{x\to0}\frac{x-\sin x}{x^{3}} = \lim_{x\to0}\frac{1-\cos x}{3x^{2}}
= \lim_{x\to0}\frac{\sin x}{6x} = \lim_{x\to0}\frac{\cos x}{6} = \frac16 $$

**4.** Let $y = \sqrt{x}$, $x = 36$, $\Delta x = 0.6$. Then
$\dfrac{dy}{dx} = \dfrac{1}{2\sqrt{x}} = \dfrac{1}{12}$ and

$$ dy = \frac{1}{12}\times 0.6 = 0.05 \;\Longrightarrow\;
\sqrt{36.6} \approx 6 + 0.05 = 6.05 $$

(Calculator: $6.0498$, so the error is under $0.0003$.)

**5.** The curve meets the $y$-axis where $x = 0$, giving $y = 3$; the point is
$(0, 3)$.

$$ \frac{dy}{dx} = 2x - 4 \;\Longrightarrow\; m = -4 \text{ at } x = 0 $$

Tangent: $y - 3 = -4(x-0)$, that is $4x + y - 3 = 0$.

Normal: slope $\dfrac14$, so $y - 3 = \dfrac14 x$, that is $x - 4y + 12 = 0$.

**6.** $A = \pi r^{2}$, so differentiating with respect to $t$,

$$ \frac{dA}{dt} = 2\pi r\frac{dr}{dt} = 2\pi(10)(0.02) = 0.4\pi
\approx 1.26\ \text{cm}^{2}\,\text{s}^{-1} $$

**7.** $f'(x) = 3x^{2} - 6x - 9 = 3(x-3)(x+1)$, zero at $x = -1$ and $x = 3$.

| Interval | $f'(x)$ | $f$ |
|---|---|---|
| $x<-1$ | $+$ | increasing |
| $-1<x<3$ | $-$ | decreasing |
| $x>3$ | $+$ | increasing |

$f''(x) = 6x - 6$. At $x = -1$, $f'' = -12 < 0$: local **maximum**
$f(-1) = -1 - 3 + 9 + 5 = 10$. At $x = 3$, $f'' = 12 > 0$: local **minimum**
$f(3) = 27 - 27 - 27 + 5 = -22$.

**8.** Let the numbers be $x$ and $y = 24 - x$, with $0 < x < 24$, and maximise
$P = x y^{2} = x(24-x)^{2}$.

$$ \frac{dP}{dx} = (24-x)^{2} + x\cdot 2(24-x)(-1) = (24-x)\left[(24-x) - 2x\right]
= (24-x)(24-3x) $$

$\dfrac{dP}{dx} = 0$ gives $x = 24$ (rejected, then $y = 0$ and $P = 0$) or
$x = 8$.

$$ \frac{d^{2}P}{dx^{2}} = -(24-3x) - 3(24-x) = 6x - 96 $$

At $x = 8$: $48 - 96 = -48 < 0$, a maximum. The numbers are $8$ and $16$, giving
$P = 8 \times 256 = 2048$.

**9.** Let $h$ be the depth and $r$ the surface radius of the water at time $t$.
By similar triangles $\dfrac{r}{h} = \dfrac{5}{10}$, so $r = \dfrac{h}{2}$ and

$$ V = \frac13\pi r^{2}h = \frac13\pi\frac{h^{2}}{4}h = \frac{\pi h^{3}}{12} $$

Differentiating with respect to $t$,

$$ \frac{dV}{dt} = \frac{\pi h^{2}}{4}\frac{dh}{dt} $$

Put $\dfrac{dV}{dt} = 3$ and $h = 4$:

$$ 3 = 4\pi\frac{dh}{dt} \;\Longrightarrow\;
\frac{dh}{dt} = \frac{3}{4\pi} \approx 0.239\ \text{m min}^{-1} $$

**10.** $f'(x) = 6x^{2} - 24 = 6(x-2)(x+2)$, so the stationary points are
$x = \pm2$; only $x = 2$ lies in $[1,3]$. Evaluate $f$ there and at the
endpoints:

| $x$ | $1$ | $2$ | $3$ |
|---|---|---|---|
| $f(x)$ | $85$ | $75$ | $89$ |

Absolute maximum $= 89$ at $x = 3$ (an endpoint); absolute minimum $= 75$ at
$x = 2$.
:::

**Group C — Long answer (8 marks each)**

1. (a) Define the hyperbolic functions $\sinh x$ and $\cosh x$ in terms of
   exponentials, and hence prove that
   $\dfrac{d}{dx}(\sinh x) = \cosh x$ and
   $\dfrac{d}{dx}(\tanh x) = \mathrm{sech}^{2}x$. <span class="marks">[4]</span>
   (b) Prove, by putting $y = \sinh^{-1}x$, that
   $\dfrac{d}{dx}\sinh^{-1}x = \dfrac{1}{\sqrt{1+x^{2}}}$, and hence
   differentiate $y = \sinh^{-1}\left(\dfrac{x}{2}\right) + \cosh^{-1}(3x)$. <span class="marks">[4]</span>
2. (a) State L'Hospital's rule and the conditions under which it may be used. <span class="marks">[2]</span>
   (b) Evaluate $\displaystyle\lim_{x\to0}\frac{e^{x}-e^{-x}-2x}{x-\sin x}$. <span class="marks">[3]</span>
   (c) Evaluate $\displaystyle\lim_{x\to\infty}\frac{x^{2}}{e^{x}}$ and explain
   why the rule had to be applied twice. <span class="marks">[3]</span>
3. A square sheet of tin of side $18$ cm has an equal square cut from each corner
   and the edges folded up to form an open box.
   (a) Express the volume $V$ as a function of the side $x$ of the square cut
   off, and state the domain of $x$. <span class="marks">[3]</span>
   (b) Find the value of $x$ that makes $V$ a maximum, applying the second
   derivative test, and find the maximum volume. <span class="marks">[5]</span>
4. (a) Find the equations of the tangent and the normal to the curve
   $y = x^{3} - 3x + 2$ at the point $(2, 4)$. <span class="marks">[4]</span>
   (b) Find the intervals in which $f(x) = 2x^{3} - 9x^{2} + 12x + 5$ is
   increasing and decreasing, and find its local maximum and minimum values
   using the second derivative test. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** (a) By definition

$$ \sinh x = \frac{e^{x}-e^{-x}}{2}, \qquad \cosh x = \frac{e^{x}+e^{-x}}{2} $$

Differentiating the first, and using
$\dfrac{d}{dx}e^{-x} = -e^{-x}$,

$$ \frac{d}{dx}\sinh x = \frac{e^{x}-(-e^{-x})}{2} = \frac{e^{x}+e^{-x}}{2}
= \cosh x $$

Similarly $\dfrac{d}{dx}\cosh x = \dfrac{e^{x}-e^{-x}}{2} = \sinh x$. Then by
the quotient rule, with $\tanh x = \dfrac{\sinh x}{\cosh x}$,

$$ \frac{d}{dx}\tanh x = \frac{\cosh x\cdot\cosh x - \sinh x\cdot \sinh x}{\cosh^{2}x}
= \frac{\cosh^{2}x-\sinh^{2}x}{\cosh^{2}x} = \frac{1}{\cosh^{2}x}
= \mathrm{sech}^{2}x $$

using the identity $\cosh^{2}x-\sinh^{2}x = 1$.

(b) Let $y = \sinh^{-1}x$, so that $x = \sinh y$. Differentiating both sides with
respect to $x$:

$$ 1 = \cosh y\,\frac{dy}{dx} \;\Longrightarrow\; \frac{dy}{dx} = \frac{1}{\cosh y} $$

Since $\cosh^{2}y = 1 + \sinh^{2}y = 1 + x^{2}$ and $\cosh y > 0$ always,

$$ \frac{dy}{dx} = \frac{1}{\sqrt{1+x^{2}}} $$

Applying this and the corresponding result for $\cosh^{-1}$ with the chain rule,

$$ \frac{d}{dx}\left[\sinh^{-1}\frac{x}{2} + \cosh^{-1}3x\right]
= \frac{1}{\sqrt{\frac{x^{2}}{4}+1}}\cdot\frac12
+ \frac{1}{\sqrt{9x^{2}-1}}\cdot 3 $$

$$ = \frac{1}{\sqrt{x^{2}+4}} + \frac{3}{\sqrt{9x^{2}-1}} $$

**2.** (a) If $f$ and $g$ are differentiable in a neighbourhood of $a$ (except
possibly at $a$) with $g'(x)\ne 0$ there, and if
$\lim_{x\to a}\dfrac{f(x)}{g(x)}$ takes the indeterminate form $\dfrac00$ or
$\dfrac{\infty}{\infty}$, then

$$ \lim_{x\to a}\frac{f(x)}{g(x)} = \lim_{x\to a}\frac{f'(x)}{g'(x)} $$

provided the right-hand limit exists (finitely or infinitely). The rule may be
repeated, and $a$ may be $\pm\infty$.

(b) Substituting $x = 0$ gives $\dfrac{1-1-0}{0-0} = \dfrac00$, so the rule
applies:

$$ \lim_{x\to0}\frac{e^{x}-e^{-x}-2x}{x-\sin x}
= \lim_{x\to0}\frac{e^{x}+e^{-x}-2}{1-\cos x} = \frac{0}{0} $$
$$ = \lim_{x\to0}\frac{e^{x}-e^{-x}}{\sin x} = \frac{0}{0}
= \lim_{x\to0}\frac{e^{x}+e^{-x}}{\cos x} = \frac{2}{1} = 2 $$

(c) As $x \to \infty$ both $x^{2}$ and $e^{x}$ tend to $\infty$, so the form is
$\dfrac{\infty}{\infty}$:

$$ \lim_{x\to\infty}\frac{x^{2}}{e^{x}} = \lim_{x\to\infty}\frac{2x}{e^{x}} $$

The new quotient is *still* $\dfrac{\infty}{\infty}$ — one differentiation only
reduces the degree of the numerator by one, while $e^{x}$ is unchanged — so the
rule must be applied again:

$$ = \lim_{x\to\infty}\frac{2}{e^{x}} = 0 $$

**3.** (a) Let $x$ cm be the side of each square cut off. The base of the box is
a square of side $18 - 2x$ and the height is $x$, so

$$ V = x(18-2x)^{2} = 4x^{3} - 72x^{2} + 324x $$

For a box to exist we need $x > 0$ and $18 - 2x > 0$, so the domain is
$0 < x < 9$.

(b) $$ \frac{dV}{dx} = 12x^{2} - 144x + 324 = 12(x^{2} - 12x + 27)
= 12(x-3)(x-9) $$

Setting $\dfrac{dV}{dx} = 0$ gives $x = 3$ or $x = 9$; $x = 9$ is outside the
domain (the base would vanish), so $x = 3$.

$$ \frac{d^{2}V}{dx^{2}} = 24x - 144 $$

At $x = 3$: $\dfrac{d^{2}V}{dx^{2}} = 72 - 144 = -72 < 0$, so $V$ is a
**maximum** at $x = 3$.

$$ V_{\max} = 3(18 - 6)^{2} = 3 \times 144 = 432\ \text{cm}^{3} $$

So a square of side $3$ cm should be cut from each corner, giving a maximum
volume of $432$ cm³.

**4.** (a) First verify the point lies on the curve:
$2^{3} - 3(2) + 2 = 4$ ✓. Then

$$ \frac{dy}{dx} = 3x^{2} - 3 \;\Longrightarrow\; m = 3(4) - 3 = 9 $$

Tangent: $y - 4 = 9(x-2)$, i.e. $9x - y - 14 = 0$.

Normal: slope $-\dfrac19$, so $y - 4 = -\dfrac19(x-2)$, i.e.
$x + 9y - 38 = 0$.

(b) $$ f'(x) = 6x^{2} - 18x + 12 = 6(x-1)(x-2) $$

so $f'(x) = 0$ at $x = 1$ and $x = 2$, and the sign of $f'$ is

| Interval | $f'(x)$ | $f$ |
|---|---|---|
| $x<1$ | $+$ | increasing |
| $1<x<2$ | $-$ | decreasing |
| $x>2$ | $+$ | increasing |

Hence $f$ increases on $(-\infty,1)$ and $(2,\infty)$ and decreases on $(1,2)$.

$f''(x) = 12x - 18$. At $x = 1$, $f''(1) = -6 < 0$, so a local **maximum** of

$$ f(1) = 2 - 9 + 12 + 5 = 10 $$

At $x = 2$, $f''(2) = 6 > 0$, so a local **minimum** of

$$ f(2) = 16 - 36 + 24 + 5 = 9 $$
:::
