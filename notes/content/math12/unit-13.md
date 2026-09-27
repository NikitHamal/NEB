---
subject: Mathematics
grade: 12
unit: 13
title: Anti-derivatives
hours: 18
area: Calculus
---

Differentiation asks: *given a function, how fast is it changing?* This unit asks
the opposite question: *given the rate of change, what was the function?* The
answer is called an **anti-derivative**, and the process of finding it is
**integration**. Eighteen teaching hours make this the largest single unit in
Grade 12 Mathematics, and it is also the one that pays best in the examination:
Group B always carries integration items and Group C almost always carries one.
The same machinery then measures areas, and in the next unit it solves
differential equations.

::: key What the exam asks
Three things, in this order of frequency. **(1)** Evaluate an indefinite
integral — you must recognise which of about a dozen methods applies. **(2)**
Evaluate a definite integral, often using a symmetry property to avoid work.
**(3)** Find an area, or evaluate an integral as the limit of a sum. Students
lose marks by choosing the *wrong method*, not by mis-executing the right one,
so learn the decision table in §13.2 before you learn any single technique.
:::

## 13.1 Standard integrals

### The anti-derivative and the indefinite integral

::: definition Anti-derivative
A function $F$ is an **anti-derivative** of $f$ on an interval if
$F'(x) = f(x)$ for every $x$ in that interval.

If $F$ is one anti-derivative of $f$, then so is $F(x) + C$ for every constant
$C$, because the derivative of a constant is zero. Conversely, any two
anti-derivatives of the same function differ by a constant. The whole family is
written

$$ \int f(x)\,dx = F(x) + C $$

and is called the **indefinite integral** of $f$. Here $f(x)$ is the
**integrand**, $x$ is the **variable of integration**, and $C$ is the
**constant of integration**.
:::

Why must two anti-derivatives differ only by a constant? If $F' = G' = f$, then
$(F-G)' = 0$ everywhere, and a function with zero derivative on an interval is
constant. So the picture of an indefinite integral is a *vertical stack* of
identical curves: at any fixed $x$ every member of the stack has exactly the
same slope.

```figure caption="The family $y = \frac{x^3}{3} + C$. All five curves are the same shape shifted vertically, and at $x=1$ every one of them has slope $x^2 = 1$ (dashed). This is why $\int x^2\,dx$ must carry $+C$."
import numpy as np
fig, ax = plt.subplots(figsize=(4.8,2.9))
x = np.linspace(-2.1, 2.1, 400)
for C, c in zip([-2,-1,0,1,2], SERIES):
    ax.plot(x, x**3/3 + C, color=c, lw=1.5)
    ax.plot([1], [1/3 + C], 'o', color=c, ms=3.4)
    xs = np.array([0.55, 1.45])
    ax.plot(xs, (1/3 + C) + 1.0*(xs - 1), color=INK, lw=1.0, ls='--', alpha=0.65)
ax.annotate('slope $=1$ on every curve at $x=1$', (1.45, 1.5), (-1.95, 3.15), fontsize=8.8, color=INK,
            arrowprops=dict(arrowstyle='->', color=INK, lw=0.8))
for C, c in zip([-2,-1,0,1,2], SERIES):
    ax.annotate('$C=%d$' % C, (-2.1, -3.087 + C), textcoords='offset points',
                xytext=(-3, -3), ha='right', color=c, fontsize=8.2)
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.set_xlim(-3.1, 2.4); ax.set_ylim(-5.4, 5.0)
ax.axhline(0, color=MUTED, lw=0.7); ax.axvline(0, color=MUTED, lw=0.7)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.45)
```

### The table you must know by heart

Every integration problem in the syllabus ends by matching something to a line
of this table. Learn it by reading each line **backwards** as a derivative.

::: key The complete table of standard integrals
| $f(x)$ | $\int f(x)\,dx$ |
|---|---|
| $x^{n}$, $n \ne -1$ | $\frac{x^{n+1}}{n+1} + C$ |
| $\frac{1}{x}$ | $\ln|x| + C$ |
| $e^{x}$ | $e^{x} + C$ |
| $a^{x}$, $a>0$, $a \ne 1$ | $\frac{a^{x}}{\ln a} + C$ |
| $\sin x$ | $-\cos x + C$ |
| $\cos x$ | $\sin x + C$ |
| $\sec^{2} x$ | $\tan x + C$ |
| $\csc^{2} x$ | $-\cot x + C$ |
| $\sec x \tan x$ | $\sec x + C$ |
| $\csc x \cot x$ | $-\csc x + C$ |
| $\tan x$ | $\ln|\sec x| + C$ |
| $\cot x$ | $\ln|\sin x| + C$ |
| $\sec x$ | $\ln|\sec x + \tan x| + C$ |
| $\csc x$ | $\ln|\csc x - \cot x| + C$ |
| $\frac{1}{\sqrt{1-x^{2}}}$ | $\sin^{-1} x + C$ |
| $\frac{1}{1+x^{2}}$ | $\tan^{-1} x + C$ |
| $\frac{1}{x^{2}+a^{2}}$ | $\frac{1}{a}\tan^{-1}\frac{x}{a} + C$ |
| $\frac{1}{x^{2}-a^{2}}$ | $\frac{1}{2a}\ln\left|\frac{x-a}{x+a}\right| + C$ |
| $\frac{1}{a^{2}-x^{2}}$ | $\frac{1}{2a}\ln\left|\frac{a+x}{a-x}\right| + C$ |
| $\frac{1}{\sqrt{a^{2}-x^{2}}}$ | $\sin^{-1}\frac{x}{a} + C$ |
| $\frac{1}{\sqrt{x^{2}+a^{2}}}$ | $\ln\left|x+\sqrt{x^{2}+a^{2}}\right| + C$ |
| $\frac{1}{\sqrt{x^{2}-a^{2}}}$ | $\ln\left|x+\sqrt{x^{2}-a^{2}}\right| + C$ |
| $\sqrt{a^{2}-x^{2}}$ | $\frac{x}{2}\sqrt{a^{2}-x^{2}} + \frac{a^{2}}{2}\sin^{-1}\frac{x}{a} + C$ |
| $\sqrt{x^{2}+a^{2}}$ | $\frac{x}{2}\sqrt{x^{2}+a^{2}} + \frac{a^{2}}{2}\ln\left|x+\sqrt{x^{2}+a^{2}}\right| + C$ |
| $\sqrt{x^{2}-a^{2}}$ | $\frac{x}{2}\sqrt{x^{2}-a^{2}} - \frac{a^{2}}{2}\ln\left|x+\sqrt{x^{2}-a^{2}}\right| + C$ |

The last nine lines are the **quadratic standard forms**. Roughly half of all
Group B integration questions reduce to one of them.
:::

Two rules let you use the table on a whole expression at once. For constants
$k$ and integrable $f$, $g$:

$$ \int k\,f(x)\,dx = k\int f(x)\,dx, \qquad
\int \left[f(x) \pm g(x)\right]dx = \int f(x)\,dx \pm \int g(x)\,dx $$

There is **no** product rule and **no** quotient rule for integrals. That
missing pair of rules is the reason this unit needs so many separate methods.

Because of that, integration is a *recognition* skill rather than a procedure.
Differentiation can be done mechanically by anyone who knows three rules, but
integration asks you to look at an expression and decide what it is disguised as.
That is why practice matters more here than anywhere else in the syllabus, and
why the first thing to do with any integral is not to start writing but to spend
ten seconds classifying it.

A third rule follows from the chain rule and costs nothing to learn. If
$\int f(x)\,dx = F(x) + C$ then, for constants $a \ne 0$ and $b$,

$$ \int f(ax+b)\,dx = \frac{1}{a}F(ax+b) + C $$

because differentiating the right side brings a factor $a$ down, which cancels
the $\frac{1}{a}$.

::: example Worked example 13.1
**Problem.** Evaluate $\int \left(3x^{2} - \frac{4}{x} + 5\sqrt{x} + e^{x}\right)dx$.

**Solution.** Split the integral term by term and apply the table to each.

$$ \int 3x^{2}\,dx = 3\cdot\frac{x^{3}}{3} = x^{3} $$

$$ \int \frac{4}{x}\,dx = 4\ln|x| $$

For $5\sqrt{x} = 5x^{1/2}$ the power rule gives exponent $\frac12 + 1 = \frac32$:

$$ \int 5x^{1/2}\,dx = 5\cdot\frac{x^{3/2}}{3/2} = \frac{10}{3}x^{3/2} $$

and $\int e^{x}dx = e^{x}$. Collecting, and writing one constant for all four,

$$ \int \left(3x^{2} - \frac{4}{x} + 5\sqrt{x} + e^{x}\right)dx
= x^{3} - 4\ln|x| + \frac{10}{3}x^{3/2} + e^{x} + C $$

**Check.** Differentiate: $3x^{2} - \frac4x + \frac{10}{3}\cdot\frac32 x^{1/2} + e^{x}
= 3x^{2} - \frac4x + 5\sqrt{x} + e^{x}$. Correct.
:::

::: example Worked example 13.2
**Problem.** Evaluate $\int \left(\sqrt{x} + \frac{1}{\sqrt{x}}\right)^{2}dx$ and
$\int \frac{(x^{2}+1)^{2}}{x^{2}}\,dx$.

**Solution.** Neither integrand is in the table, but both become table entries
after ordinary algebra. **Always expand or divide out first.**

$$ \left(\sqrt{x} + \frac{1}{\sqrt{x}}\right)^{2} = x + 2 + \frac{1}{x} $$

$$ \int \left(x + 2 + \frac1x\right)dx = \frac{x^{2}}{2} + 2x + \ln|x| + C $$

For the second, expand the numerator and divide each term by $x^{2}$:

$$ \frac{x^{4} + 2x^{2} + 1}{x^{2}} = x^{2} + 2 + x^{-2} $$

$$ \int \left(x^{2} + 2 + x^{-2}\right)dx = \frac{x^{3}}{3} + 2x - \frac{1}{x} + C $$
:::

::: example Worked example 13.3
**Problem.** Evaluate (a) $\int \tan^{2}x\,dx$, (b) $\int \sin^{2}x\,dx$,
(c) $\int \frac{dx}{1+\cos x}$.

**Solution.** Every one of these is solved by a trigonometric identity, not by a
new integration rule.

**(a)** Use $\sec^{2}x - \tan^{2}x = 1$, so $\tan^{2}x = \sec^{2}x - 1$:

$$ \int \tan^{2}x\,dx = \int \left(\sec^{2}x - 1\right)dx = \tan x - x + C $$

**(b)** Use the power-reduction identity $\cos 2x = 1 - 2\sin^{2}x$, so
$\sin^{2}x = \frac{1 - \cos 2x}{2}$:

$$ \int \sin^{2}x\,dx = \frac12\int (1 - \cos 2x)\,dx
= \frac{x}{2} - \frac{\sin 2x}{4} + C $$

**(c)** Use $1 + \cos x = 2\cos^{2}\frac{x}{2}$:

$$ \int \frac{dx}{2\cos^{2}\frac{x}{2}} = \frac12\int \sec^{2}\frac{x}{2}\,dx
= \frac12 \cdot \frac{\tan\frac{x}{2}}{1/2} + C = \tan\frac{x}{2} + C $$
:::

::: example Worked example 13.4
**Problem.** Evaluate (a) $\int (2x+3)^{5}dx$, (b) $\int \frac{dx}{3x+2}$,
(c) $\int \sin(5x-2)\,dx$, (d) $\int \frac{dx}{\sqrt{2x+1}}$.

**Solution.** All four are of the form $f(ax+b)$, so integrate as if the bracket
were $x$ and divide by $a$.

**(a)** $a = 2$: $\quad \int (2x+3)^{5}dx = \frac{1}{2}\cdot\frac{(2x+3)^{6}}{6} + C
= \frac{(2x+3)^{6}}{12} + C$

**(b)** $a = 3$: $\quad \int \frac{dx}{3x+2} = \frac{1}{3}\ln|3x+2| + C$

**(c)** $a = 5$: $\quad \int \sin(5x-2)\,dx = -\frac{1}{5}\cos(5x-2) + C$

**(d)** $a = 2$ and $\int x^{-1/2}dx = 2\sqrt{x}$:
$\quad \int \frac{dx}{\sqrt{2x+1}} = \frac{1}{2}\cdot 2\sqrt{2x+1} + C = \sqrt{2x+1} + C$
:::

::: caution The rule $\int f(ax+b) = \frac{1}{a}F(ax+b)$ needs $ax+b$ **linear**
It works for $(2x+3)^{5}$ but **not** for $(2x^{2}+3)^{5}$, because
differentiating $(2x^{2}+3)^{6}$ produces $4x$, not a constant. A non-linear
inside function always needs a substitution, and the substitution only closes if
the derivative of the inside function is already present as a factor.
:::

::: caution Never drop the $+C$
An indefinite integral without $+C$ is one function instead of a whole family,
and NEB markers deduct for it every single time. Also remember $\ln|x|$, not
$\ln x$: the modulus is what makes the formula valid for negative $x$ too.
:::

## 13.2 Integrals reducible to standard forms

Most integrands are not in the table. The art is to change them into something
that is. Read this decision table first; then learn the individual techniques.

Read the table from the top down and stop at the first row that fits. The rows
are deliberately in that order: the cheap checks — is it already standard, can it
be expanded, is it linear inside — come before the expensive ones. A great many
marks are thrown away each year by students who reach for integration by parts on
an integral that a single substitution would have finished in two lines, or who
attempt partial fractions on a fraction that is not yet proper.

::: key Which method for which integral
| The integrand looks like | Method | Typical example |
|---|---|---|
| a table entry, or a constant times one | read it off the table | $\int \sec^{2}x\,dx$ |
| a sum, product or quotient of powers | expand or divide out, then the table | $\int \frac{(x^{2}+1)^{2}}{x^{2}}dx$ |
| $f(ax+b)$ with $\int f$ known | integrate, divide by $a$ | $\int (2x+3)^{5}dx$ |
| contains $g(x)$ **and** its derivative $g'(x)$ | substitute $u = g(x)$ | $\int x\sqrt{x^{2}+1}\,dx$ |
| exactly $\frac{g'(x)}{g(x)}$ | answer is $\ln|g(x)|$ | $\int \tan x\,dx$ |
| product of two *unlike* functions | by parts, order by ILATE | $\int x e^{x}dx$ |
| a lone $\ln$ or inverse-trig function | by parts against $1$ | $\int \tan^{-1}x\,dx$ |
| $e^{ax}\sin bx$ or $e^{ax}\cos bx$ | by parts twice, then solve for $I$ | $\int e^{x}\sin x\,dx$ |
| quadratic in the denominator, no $x$ on top | complete the square, then table | $\int \frac{dx}{x^{2}+6x+13}$ |
| $\frac{px+q}{ax^{2}+bx+c}$ or $\frac{px+q}{\sqrt{ax^{2}+bx+c}}$ | split $px+q = \lambda\,(\text{denom})' + \mu$ | $\int \frac{2x+3}{x^{2}+4x+5}dx$ |
| $\sqrt{a^{2}-x^{2}}$, $\sqrt{a^{2}+x^{2}}$, $\sqrt{x^{2}-a^{2}}$ | $x=a\sin\theta$, $a\tan\theta$, $a\sec\theta$ | $\int \sqrt{9-x^{2}}\,dx$ |
| a rational function of $\sin x$ and $\cos x$ | $t = \tan\frac{x}{2}$ | $\int \frac{dx}{5+4\cos x}$ |
| a ratio of two polynomials | divide if improper, then partial fractions | $\int \frac{x^{2}+1}{(x+1)(x+2)}dx$ |
| a single $x$ outside a heavy radical | inverse substitution $x = \frac1t$ | $\int \frac{dx}{x\sqrt{1+x^{2}}}$ |
:::

### Integration by substitution

If we put $u = g(x)$ then $du = g'(x)\,dx$, and

$$ \int f\left(g(x)\right)g'(x)\,dx = \int f(u)\,du $$

The substitution **closes** only when every remaining $x$ disappears. That is
the test: after substituting, if any $x$ is left, the choice of $u$ was wrong.

::: example Worked example 13.5
**Problem.** Evaluate $\int x\sqrt{x^{2}+1}\,dx$.

**Solution.** The derivative of $x^{2}+1$ is $2x$, and an $x$ is already present.

Put $u = x^{2}+1$, so $du = 2x\,dx$, i.e. $x\,dx = \frac{du}{2}$.

$$ \int x\sqrt{x^{2}+1}\,dx = \int \sqrt{u}\,\frac{du}{2}
= \frac12 \cdot \frac{u^{3/2}}{3/2} = \frac{u^{3/2}}{3} $$

Put $u$ back: $\quad = \frac{1}{3}\left(x^{2}+1\right)^{3/2} + C$.

**Check.** $\frac{d}{dx}\frac{(x^{2}+1)^{3/2}}{3} = \frac{1}{3}\cdot\frac32(x^{2}+1)^{1/2}\cdot 2x
= x\sqrt{x^{2}+1}$. Correct.
:::

::: key The single most useful substitution
$$ \int \frac{g'(x)}{g(x)}\,dx = \ln|g(x)| + C $$
Whenever the numerator is exactly the derivative of the denominator (or a
constant times it), write down the logarithm immediately. This one pattern
produces $\int\tan x\,dx$, $\int\cot x\,dx$, $\int\frac{x^{3}}{x^{4}+5}dx$ and
half of every partial-fraction answer.
:::

::: example Worked example 13.6
**Problem.** Prove that $\int \tan x\,dx = \ln|\sec x| + C$ and
$\int \cot x\,dx = \ln|\sin x| + C$.

**Solution.** Write $\tan x = \dfrac{\sin x}{\cos x}$ and put $u = \cos x$, so
$du = -\sin x\,dx$:

$$ \int \frac{\sin x}{\cos x}\,dx = -\int \frac{du}{u} = -\ln|u| + C
= -\ln|\cos x| + C = \ln\left|\frac{1}{\cos x}\right| + C = \ln|\sec x| + C $$

For the cotangent, $u = \sin x$ gives $du = \cos x\,dx$ and the numerator is
already $\cos x$:

$$ \int \frac{\cos x}{\sin x}\,dx = \int \frac{du}{u} = \ln|\sin x| + C $$
:::

::: example Worked example 13.7
**Problem.** Evaluate (a) $\int \frac{e^{\tan^{-1}x}}{1+x^{2}}\,dx$,
(b) $\int \frac{x^{3}}{x^{4}+5}\,dx$, (c) $\int \frac{dx}{x\ln x}$,
(d) $\int \sin^{3}x\cos x\,dx$.

**Solution.** In each case spot the inside function and its derivative.

**(a)** $u = \tan^{-1}x$, $du = \frac{dx}{1+x^{2}}$:
$\quad \int e^{u}du = e^{u} + C = e^{\tan^{-1}x} + C$

**(b)** $u = x^{4}+5$, $du = 4x^{3}dx$:
$\quad \frac14\int\frac{du}{u} = \frac14\ln\left|x^{4}+5\right| + C$

**(c)** $u = \ln x$, $du = \frac{dx}{x}$:
$\quad \int\frac{du}{u} = \ln\left|\ln x\right| + C$

**(d)** $u = \sin x$, $du = \cos x\,dx$:
$\quad \int u^{3}du = \frac{u^{4}}{4} + C = \frac{\sin^{4}x}{4} + C$
:::

::: example Worked example 13.8
**Problem.** Prove the standard result $\int \sec x\,dx = \ln|\sec x + \tan x| + C$.

**Solution.** The trick is to multiply and divide by $\sec x + \tan x$, which
manufactures a "derivative over function" pattern.

$$ \int \sec x\,dx = \int \sec x \cdot \frac{\sec x + \tan x}{\sec x + \tan x}\,dx
= \int \frac{\sec^{2}x + \sec x\tan x}{\sec x + \tan x}\,dx $$

Now put $u = \sec x + \tan x$. Then
$du = \left(\sec x\tan x + \sec^{2}x\right)dx$, which is exactly the numerator:

$$ \int \frac{du}{u} = \ln|u| + C = \ln\left|\sec x + \tan x\right| + C $$

The same trick with $\csc x - \cot x$ gives
$\int \csc x\,dx = \ln|\csc x - \cot x| + C$.
:::

### Integration by parts

::: derivation The formula for integration by parts
Start from the product rule for two differentiable functions $u$ and $v$:

$$ \frac{d}{dx}(uv) = u\frac{dv}{dx} + v\frac{du}{dx} $$

Integrate both sides with respect to $x$. The left side integrates back to $uv$:

$$ uv = \int u\frac{dv}{dx}\,dx + \int v\frac{du}{dx}\,dx $$

Rearranging gives the working formula

$$ \int u\,dv = uv - \int v\,du $$

or, with $u = u(x)$ and $dv = v'(x)\,dx$ written out in full,

$$ \int u(x)\,v'(x)\,dx = u(x)v(x) - \int v(x)\,u'(x)\,dx $$

The method is useful exactly when $\int v\,du$ is **easier** than $\int u\,dv$.
:::

::: memory ILATE — which factor to call $u$
Choose $u$ as the function that comes **first** in this list:

**I** — Inverse trigonometric ($\sin^{-1}x$, $\tan^{-1}x$, …)
**L** — Logarithmic ($\ln x$)
**A** — Algebraic ($x$, $x^{2}$, polynomials)
**T** — Trigonometric ($\sin x$, $\cos x$)
**E** — Exponential ($e^{x}$, $a^{x}$)

The rest of the integrand is $dv$. The logic is that I and L get *simpler* when
differentiated, while T and E are just as easy to integrate as to differentiate.
:::

::: example Worked example 13.9
**Problem.** Evaluate $\int x e^{x}\,dx$.

**Solution.** Algebraic before Exponential, so $u = x$ and $dv = e^{x}dx$.

Then $du = dx$ and $v = e^{x}$.

$$ \int x e^{x}dx = x e^{x} - \int e^{x}\,dx = x e^{x} - e^{x} + C = (x-1)e^{x} + C $$

**Check.** $\frac{d}{dx}\left[(x-1)e^{x}\right] = e^{x} + (x-1)e^{x} = x e^{x}$. Correct.

Had we chosen $u = e^{x}$ instead, we would have got
$\frac{x^{2}}{2}e^{x} - \int \frac{x^{2}}{2}e^{x}dx$ — a *harder* integral. That
is what ILATE protects you from.
:::

::: example Worked example 13.10
**Problem.** Evaluate $\int x^{2}\sin x\,dx$ (the **repeated** case).

**Solution.** Algebraic before Trigonometric: $u = x^{2}$, $dv = \sin x\,dx$, so
$du = 2x\,dx$ and $v = -\cos x$.

$$ \int x^{2}\sin x\,dx = -x^{2}\cos x + 2\int x\cos x\,dx $$

The new integral is still a product, but the power of $x$ has dropped by one.
Apply parts again with $u = x$, $dv = \cos x\,dx$, $v = \sin x$:

$$ \int x\cos x\,dx = x\sin x - \int \sin x\,dx = x\sin x + \cos x $$

Substituting back,

$$ \int x^{2}\sin x\,dx = -x^{2}\cos x + 2x\sin x + 2\cos x + C $$

**Check.** Differentiating gives
$-2x\cos x + x^{2}\sin x + 2\sin x + 2x\cos x - 2\sin x = x^{2}\sin x$. Correct.
An integrand $x^{n}\sin x$ needs exactly $n$ applications of parts.
:::

::: example Worked example 13.11
**Problem.** Evaluate $\int \ln x\,dx$, $\int x^{2}\ln x\,dx$ and
$\int \tan^{-1}x\,dx$.

**Solution.** A lone logarithm or inverse-trig function is integrated *against
the invisible factor $1$*.

**(a)** $u = \ln x$, $dv = 1\,dx$, so $du = \frac{dx}{x}$ and $v = x$:

$$ \int \ln x\,dx = x\ln x - \int x\cdot\frac{1}{x}\,dx = x\ln x - x + C $$

**(b)** L before A: $u = \ln x$, $dv = x^{2}dx$, so $v = \frac{x^{3}}{3}$:

$$ \int x^{2}\ln x\,dx = \frac{x^{3}}{3}\ln x - \int \frac{x^{3}}{3}\cdot\frac1x\,dx
= \frac{x^{3}}{3}\ln x - \frac{x^{3}}{9} + C $$

**(c)** $u = \tan^{-1}x$, $dv = 1\,dx$, so $du = \frac{dx}{1+x^{2}}$ and $v = x$:

$$ \int \tan^{-1}x\,dx = x\tan^{-1}x - \int \frac{x}{1+x^{2}}\,dx
= x\tan^{-1}x - \frac12\ln\left(1+x^{2}\right) + C $$

using $\int\frac{g'}{g} = \ln|g|$ with $g = 1+x^{2}$ (always positive, so no
modulus is needed).
:::

::: example Worked example 13.12
**Problem.** Evaluate $I = \int e^{x}\sin x\,dx$ (the **cyclic** case).

**Solution.** Neither factor simplifies on differentiation, so parts will never
terminate. Instead, apply it twice and recover the original integral.

Take $u = \sin x$, $dv = e^{x}dx$, so $v = e^{x}$:

$$ I = e^{x}\sin x - \int e^{x}\cos x\,dx $$

Apply parts to the new integral with $u = \cos x$, $dv = e^{x}dx$:

$$ \int e^{x}\cos x\,dx = e^{x}\cos x + \int e^{x}\sin x\,dx = e^{x}\cos x + I $$

Substituting back,

$$ I = e^{x}\sin x - e^{x}\cos x - I \quad\Longrightarrow\quad 2I = e^{x}(\sin x - \cos x) $$

$$ I = \frac{e^{x}}{2}\left(\sin x - \cos x\right) + C $$

The general result, obtained the same way, is

$$ \int e^{ax}\cos bx\,dx = \frac{e^{ax}}{a^{2}+b^{2}}\left(a\cos bx + b\sin bx\right) + C $$

For example $\int e^{2x}\cos 3x\,dx
= \frac{e^{2x}}{13}\left(2\cos 3x + 3\sin 3x\right) + C$.
:::

::: tip The $\int e^{x}\left[f(x)+f'(x)\right]dx$ shortcut
$$ \int e^{x}\left[f(x) + f'(x)\right]dx = e^{x}f(x) + C $$
Proof: differentiate the right side. So
$\int e^{x}(\sin x + \cos x)\,dx = e^{x}\sin x + C$ in one line. Look for this
pattern before doing parts twice — it saves several minutes in the examination.
:::

### Reducing to the quadratic standard forms

::: derivation $\int \frac{dx}{x^{2}-a^{2}}$ and $\int \frac{dx}{\sqrt{x^{2}+a^{2}}}$
**First form.** Split by partial fractions, using
$\frac{1}{x^{2}-a^{2}} = \frac{1}{(x-a)(x+a)}$ and the identity
$\frac{1}{(x-a)(x+a)} = \frac{1}{2a}\left[\frac{1}{x-a} - \frac{1}{x+a}\right]$:

$$ \int \frac{dx}{x^{2}-a^{2}} = \frac{1}{2a}\left[\ln|x-a| - \ln|x+a|\right] + C
= \frac{1}{2a}\ln\left|\frac{x-a}{x+a}\right| + C $$

**Second form.** Put $x = a\tan\theta$, so $dx = a\sec^{2}\theta\,d\theta$ and
$\sqrt{x^{2}+a^{2}} = a\sec\theta$:

$$ \int \frac{dx}{\sqrt{x^{2}+a^{2}}} = \int \frac{a\sec^{2}\theta}{a\sec\theta}\,d\theta
= \int \sec\theta\,d\theta = \ln\left|\sec\theta + \tan\theta\right| + C_1 $$

From the reference triangle, $\tan\theta = \frac{x}{a}$ and
$\sec\theta = \frac{\sqrt{x^{2}+a^{2}}}{a}$, so

$$ = \ln\left|\frac{x + \sqrt{x^{2}+a^{2}}}{a}\right| + C_1
= \ln\left|x + \sqrt{x^{2}+a^{2}}\right| + C $$

because $-\ln a$ is itself a constant and is absorbed into $C$.
:::

Any quadratic can be pushed into one of these forms by **completing the
square**: $ax^{2}+bx+c = a\left[\left(x+\frac{b}{2a}\right)^{2}
+ \frac{4ac-b^{2}}{4a^{2}}\right]$. Then substitute $t = x + \frac{b}{2a}$.

::: example Worked example 13.13
**Problem.** Evaluate (a) $\int \frac{dx}{4x^{2}+9}$, (b) $\int \frac{dx}{x^{2}-16}$,
(c) $\int \frac{dx}{\sqrt{9-4x^{2}}}$.

**Solution.** Force each into the shape $x^{2} \pm a^{2}$ by taking the leading
coefficient outside.

**(a)** $4x^{2}+9 = 4\left(x^{2} + \frac94\right)$, so $a = \frac32$:

$$ \int \frac{dx}{4\left(x^{2}+\left(\frac32\right)^{2}\right)}
= \frac14 \cdot \frac{1}{3/2}\tan^{-1}\frac{x}{3/2} + C
= \frac{1}{6}\tan^{-1}\frac{2x}{3} + C $$

**(b)** Here $a = 4$ directly:

$$ \int \frac{dx}{x^{2}-4^{2}} = \frac{1}{2(4)}\ln\left|\frac{x-4}{x+4}\right| + C
= \frac{1}{8}\ln\left|\frac{x-4}{x+4}\right| + C $$

**(c)** $9-4x^{2} = 4\left(\frac94 - x^{2}\right)$, so
$\sqrt{9-4x^{2}} = 2\sqrt{\left(\frac32\right)^{2}-x^{2}}$:

$$ \frac12\int \frac{dx}{\sqrt{\left(\frac32\right)^{2}-x^{2}}}
= \frac12 \sin^{-1}\frac{x}{3/2} + C = \frac12\sin^{-1}\frac{2x}{3} + C $$
:::

::: example Worked example 13.14
**Problem.** Evaluate (a) $\int \frac{dx}{x^{2}+6x+13}$,
(b) $\int \frac{dx}{\sqrt{x^{2}+4x+13}}$, (c) $\int \frac{dx}{\sqrt{5-4x-x^{2}}}$.

**Solution.** Complete the square in every case.

**(a)** $x^{2}+6x+13 = (x+3)^{2} + 4 = (x+3)^{2} + 2^{2}$. Put $t = x+3$, $dt = dx$:

$$ \int \frac{dt}{t^{2}+2^{2}} = \frac12\tan^{-1}\frac{t}{2} + C
= \frac12\tan^{-1}\left(\frac{x+3}{2}\right) + C $$

**(b)** $x^{2}+4x+13 = (x+2)^{2} + 9 = (x+2)^{2} + 3^{2}$. With $t = x+2$:

$$ \int \frac{dt}{\sqrt{t^{2}+3^{2}}} = \ln\left|t + \sqrt{t^{2}+9}\right| + C
= \ln\left|x+2+\sqrt{x^{2}+4x+13}\right| + C $$

**(c)** Take out the minus sign first:
$5-4x-x^{2} = 5 - \left(x^{2}+4x\right) = 5 + 4 - (x+2)^{2} = 3^{2} - (x+2)^{2}$.
With $t = x+2$:

$$ \int \frac{dt}{\sqrt{3^{2}-t^{2}}} = \sin^{-1}\frac{t}{3} + C
= \sin^{-1}\left(\frac{x+2}{3}\right) + C $$
:::

::: caution Look at the sign of the $x^{2}$ term *before* completing the square
$\sqrt{x^{2}+4x+13}$ leads to a logarithm; $\sqrt{5-4x-x^{2}}$ leads to an
inverse sine. The difference is only the sign of $x^{2}$, and it changes the
whole answer. Write the bracket out fully rather than doing it in your head.
:::

### The forms $\frac{px+q}{ax^{2}+bx+c}$ and $\frac{px+q}{\sqrt{ax^{2}+bx+c}}$

With an $x$ in the numerator, **split the numerator** into a multiple of the
derivative of the quadratic plus a constant:

$$ px + q = \lambda\left(2ax + b\right) + \mu $$

Comparing coefficients, $\lambda = \frac{p}{2a}$ and $\mu = q - \frac{pb}{2a}$.
The $\lambda$ piece is a $\frac{g'}{g}$ pattern (a logarithm, or a square root);
the $\mu$ piece is one of the quadratic standard forms just done.

::: example Worked example 13.15
**Problem.** Evaluate $\int \frac{2x+3}{x^{2}+4x+5}\,dx$.

**Solution.** The derivative of $x^{2}+4x+5$ is $2x+4$. Write

$$ 2x+3 = (2x+4) - 1 $$

so the integral splits into two:

$$ \int \frac{2x+4}{x^{2}+4x+5}\,dx - \int \frac{dx}{x^{2}+4x+5} $$

The first is $\frac{g'}{g}$, giving $\ln\left|x^{2}+4x+5\right|$; and since
$x^{2}+4x+5 = (x+2)^{2}+1 > 0$ we may drop the modulus. For the second,
$t = x+2$ gives $\int \frac{dt}{t^{2}+1} = \tan^{-1}(x+2)$. Hence

$$ \int \frac{2x+3}{x^{2}+4x+5}\,dx = \ln\left(x^{2}+4x+5\right) - \tan^{-1}(x+2) + C $$
:::

::: example Worked example 13.16
**Problem.** Evaluate $\int \frac{x+2}{\sqrt{x^{2}+2x+3}}\,dx$.

**Solution.** The derivative of $x^{2}+2x+3$ is $2x+2$, so

$$ x+2 = \frac12(2x+2) + 1 $$

$$ \int \frac{x+2}{\sqrt{x^{2}+2x+3}}\,dx
= \frac12\int \frac{2x+2}{\sqrt{x^{2}+2x+3}}\,dx + \int \frac{dx}{\sqrt{x^{2}+2x+3}} $$

In the first integral put $u = x^{2}+2x+3$, $du = (2x+2)dx$:

$$ \frac12\int \frac{du}{\sqrt{u}} = \frac12 \cdot 2\sqrt{u} = \sqrt{x^{2}+2x+3} $$

For the second, $x^{2}+2x+3 = (x+1)^{2}+2$, so with $t = x+1$,
$\int\frac{dt}{\sqrt{t^{2}+2}} = \ln\left|t+\sqrt{t^{2}+2}\right|$. Altogether

$$ = \sqrt{x^{2}+2x+3} + \ln\left|x+1+\sqrt{x^{2}+2x+3}\right| + C $$
:::

::: tip Always check by differentiating
Integration has a free self-check that differentiation does not: differentiate
your answer and see whether you get the integrand back. It takes fifteen seconds
and it catches sign slips, missing factors of $\frac12$, and wrong partial
fraction constants. In the examination, if a question is worth five marks, spend
one of your minutes on this check — a wrong answer with perfect method still
loses most of the marks.
:::

### Trigonometric substitutions

When a radical cannot be removed by completing the square alone, replace $x$ by
a trigonometric function chosen to make the radical collapse by a Pythagorean
identity. Draw the **reference triangle** so that you can change back at the end.

| Radical | Substitute | Radical becomes | Because |
|---|---|---|---|
| $\sqrt{a^{2}-x^{2}}$ | $x = a\sin\theta$ | $a\cos\theta$ | $1-\sin^{2}\theta = \cos^{2}\theta$ |
| $\sqrt{a^{2}+x^{2}}$ | $x = a\tan\theta$ | $a\sec\theta$ | $1+\tan^{2}\theta = \sec^{2}\theta$ |
| $\sqrt{x^{2}-a^{2}}$ | $x = a\sec\theta$ | $a\tan\theta$ | $\sec^{2}\theta-1 = \tan^{2}\theta$ |

```figure caption="The three reference triangles. Draw the one you need, label the angle $\theta$, and every trigonometric function of $\theta$ can be read straight off it when you change back to $x$."
import numpy as np
fig, axs = plt.subplots(1, 3, figsize=(5.2,2.25))
data = [("$x = a\\sin\\theta$", "$a$", "$x$", "$\\sqrt{a^2-x^2}$"),
        ("$x = a\\tan\\theta$", "$\\sqrt{x^2+a^2}$", "$x$", "$a$"),
        ("$x = a\\sec\\theta$", "$x$", "$\\sqrt{x^2-a^2}$", "$a$")]
for ax, (title, hyp, opp, adj) in zip(axs, data):
    A = np.array([0.0, 0.0]); B = np.array([1.55, 0.0]); Cc = np.array([1.55, 1.05])
    ax.plot([A[0], B[0], Cc[0], A[0]], [A[1], B[1], Cc[1], A[1]], color=INK, lw=1.5)
    ax.plot([1.55-0.14, 1.55-0.14, 1.55], [0, 0.14, 0.14], color=MUTED, lw=0.9)
    th = np.linspace(0, np.arctan2(1.05, 1.55), 40)
    ax.plot(0.42*np.cos(th), 0.42*np.sin(th), color=ACCENT, lw=1.1)
    ax.text(0.50, 0.11, '$\\theta$', color=ACCENT, fontsize=10)
    ax.text(0.63, 0.74, hyp, fontsize=8.4, color=INK, rotation=34, ha='center')
    ax.text(1.63, 0.50, opp, fontsize=9.0, color=INK, va='center')
    ax.text(0.78, -0.27, adj, fontsize=8.6, color=INK, ha='center')
    ax.set_title(title, fontsize=9.2)
    ax.set_xlim(-0.30, 2.62); ax.set_ylim(-0.52, 1.42)
    ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: example Worked example 13.17
**Problem.** Derive $\int \sqrt{a^{2}-x^{2}}\,dx
= \frac{x}{2}\sqrt{a^{2}-x^{2}} + \frac{a^{2}}{2}\sin^{-1}\frac{x}{a} + C$.

**Solution.** Put $x = a\sin\theta$, so $dx = a\cos\theta\,d\theta$ and
$\sqrt{a^{2}-x^{2}} = a\cos\theta$.

$$ \int \sqrt{a^{2}-x^{2}}\,dx = \int a\cos\theta \cdot a\cos\theta\,d\theta
= a^{2}\int \cos^{2}\theta\,d\theta $$

Use $\cos^{2}\theta = \frac{1+\cos 2\theta}{2}$:

$$ = \frac{a^{2}}{2}\int (1 + \cos 2\theta)\,d\theta
= \frac{a^{2}}{2}\left(\theta + \frac{\sin 2\theta}{2}\right) + C
= \frac{a^{2}}{2}\theta + \frac{a^{2}}{2}\sin\theta\cos\theta + C $$

From the first reference triangle, $\theta = \sin^{-1}\frac{x}{a}$,
$\sin\theta = \frac{x}{a}$ and $\cos\theta = \frac{\sqrt{a^{2}-x^{2}}}{a}$, so

$$ = \frac{a^{2}}{2}\sin^{-1}\frac{x}{a}
+ \frac{a^{2}}{2}\cdot\frac{x}{a}\cdot\frac{\sqrt{a^{2}-x^{2}}}{a} + C
= \frac{x}{2}\sqrt{a^{2}-x^{2}} + \frac{a^{2}}{2}\sin^{-1}\frac{x}{a} + C $$
:::

::: example Worked example 13.18
**Problem.** Evaluate $\int \frac{dx}{x^{2}\sqrt{x^{2}-9}}$.

**Solution.** The radical is $\sqrt{x^{2}-a^{2}}$ with $a = 3$, so put
$x = 3\sec\theta$, $dx = 3\sec\theta\tan\theta\,d\theta$ and
$\sqrt{x^{2}-9} = 3\tan\theta$.

$$ \int \frac{3\sec\theta\tan\theta\,d\theta}{9\sec^{2}\theta \cdot 3\tan\theta}
= \frac{1}{9}\int \frac{d\theta}{\sec\theta} = \frac19\int \cos\theta\,d\theta
= \frac{\sin\theta}{9} + C $$

From the third reference triangle, the hypotenuse is $x$, the adjacent side is
$3$, and the opposite side is $\sqrt{x^{2}-9}$, so
$\sin\theta = \frac{\sqrt{x^{2}-9}}{x}$. Hence

$$ \int \frac{dx}{x^{2}\sqrt{x^{2}-9}} = \frac{\sqrt{x^{2}-9}}{9x} + C $$

**Check.** Differentiating $\frac{1}{9}\left(1 - \frac{9}{x^{2}}\right)^{1/2}$,
written this way to make the algebra short, returns
$\frac{1}{x^{2}\sqrt{x^{2}-9}}$. Correct.
:::

::: example Worked example 13.19
**Problem.** Evaluate $\int \frac{dx}{x\sqrt{1+x^{2}}}$ by the **inverse
substitution** $x = \frac{1}{t}$.

**Solution.** When a single power of $x$ sits outside a heavy radical, the
substitution $x = \frac1t$ turns the radical inside out. Here
$dx = -\frac{dt}{t^{2}}$ and

$$ \sqrt{1+x^{2}} = \sqrt{1 + \frac{1}{t^{2}}} = \frac{\sqrt{t^{2}+1}}{|t|} $$

Taking $t>0$ (i.e. $x>0$),

$$ \int \frac{-dt/t^{2}}{\frac1t \cdot \frac{\sqrt{t^{2}+1}}{t}}
= -\int \frac{dt}{\sqrt{t^{2}+1}} = -\ln\left|t + \sqrt{t^{2}+1}\right| + C $$

Putting $t = \frac1x$ back,

$$ = -\ln\left|\frac{1}{x} + \frac{\sqrt{1+x^{2}}}{x}\right| + C
= -\ln\left|\frac{1+\sqrt{1+x^{2}}}{x}\right| + C $$
:::

### The forms $\frac{1}{a+b\cos x}$ and $\frac{1}{a\sin x + b\cos x}$

::: key The half-angle (Weierstrass) substitution
Put $t = \tan\dfrac{x}{2}$. Then

$$ \sin x = \frac{2t}{1+t^{2}}, \qquad \cos x = \frac{1-t^{2}}{1+t^{2}},
\qquad \tan x = \frac{2t}{1-t^{2}}, \qquad dx = \frac{2\,dt}{1+t^{2}} $$

Every rational function of $\sin x$ and $\cos x$ becomes a rational function of
$t$, which §13.3 can always finish. To see where $dx$ comes from: $t=\tan\frac x2$
gives $\frac{dt}{dx} = \frac12\sec^{2}\frac{x}{2} = \frac{1+t^{2}}{2}$.
:::

::: example Worked example 13.20
**Problem.** Evaluate $\int \frac{dx}{5+4\cos x}$.

**Solution.** Put $t = \tan\frac{x}{2}$. Then

$$ 5 + 4\cos x = 5 + \frac{4\left(1-t^{2}\right)}{1+t^{2}}
= \frac{5+5t^{2}+4-4t^{2}}{1+t^{2}} = \frac{9+t^{2}}{1+t^{2}} $$

and $dx = \frac{2\,dt}{1+t^{2}}$, so the factor $1+t^{2}$ cancels completely:

$$ \int \frac{dx}{5+4\cos x} = \int \frac{2\,dt}{1+t^{2}}\cdot\frac{1+t^{2}}{9+t^{2}}
= 2\int \frac{dt}{t^{2}+3^{2}} $$

$$ = 2 \cdot \frac13\tan^{-1}\frac{t}{3} + C
= \frac{2}{3}\tan^{-1}\left(\frac{1}{3}\tan\frac{x}{2}\right) + C $$
:::

::: example Worked example 13.21
**Problem.** Evaluate $\int \frac{dx}{3\sin x + 4\cos x}$.

**Solution.** Again put $t = \tan\frac{x}{2}$:

$$ 3\sin x + 4\cos x = \frac{6t}{1+t^{2}} + \frac{4\left(1-t^{2}\right)}{1+t^{2}}
= \frac{-4t^{2}+6t+4}{1+t^{2}} $$

$$ \int \frac{dx}{3\sin x+4\cos x} = \int \frac{2\,dt}{-4t^{2}+6t+4}
= -\int \frac{dt}{2t^{2}-3t-2} = -\int \frac{dt}{(2t+1)(t-2)} $$

Split by partial fractions. Writing
$\frac{1}{(2t+1)(t-2)} = \frac{A}{2t+1} + \frac{B}{t-2}$ gives
$1 = A(t-2) + B(2t+1)$. Put $t=2$: $1 = 5B$, so $B = \frac15$. Put
$t = -\frac12$: $1 = -\frac52 A$, so $A = -\frac25$. Hence

$$ -\int \left[\frac{-2/5}{2t+1} + \frac{1/5}{t-2}\right]dt
= \frac{1}{5}\ln|2t+1| - \frac{1}{5}\ln|t-2| + C $$

$$ = \frac{1}{5}\ln\left|\frac{2\tan\frac{x}{2}+1}{\tan\frac{x}{2}-2}\right| + C $$

Notice the coefficient $\frac15 = \frac{1}{\sqrt{3^{2}+4^{2}}}$. That is no
accident: $a\sin x + b\cos x = \sqrt{a^{2}+b^{2}}\,\sin(x+\alpha)$, so the
integral always carries a factor $\frac{1}{\sqrt{a^{2}+b^{2}}}$ — a fast way to
check your answer.
:::

## 13.3 Integrals of rational functions

A **rational function** is a quotient $\frac{P(x)}{Q(x)}$ of two polynomials. If
$\deg P \ge \deg Q$ the fraction is *improper*: divide first, so that

$$ \frac{P(x)}{Q(x)} = \text{polynomial} + \frac{\text{remainder}}{Q(x)} $$

Once the fraction is proper, factorise $Q(x)$ and split it into **partial
fractions**. There are exactly four cases, decided entirely by the factors of
the denominator.

::: key The four partial-fraction cases
| Factor of $Q(x)$ | Contributes |
|---|---|
| distinct linear $(x-a)$ | $\dfrac{A}{x-a}$ |
| repeated linear $(x-a)^{2}$ | $\dfrac{A}{x-a} + \dfrac{B}{(x-a)^{2}}$ |
| distinct irreducible quadratic $(x^{2}+px+q)$ | $\dfrac{Ax+B}{x^{2}+px+q}$ |
| repeated quadratic $(x^{2}+px+q)^{2}$ | $\dfrac{Ax+B}{x^{2}+px+q} + \dfrac{Cx+D}{(x^{2}+px+q)^{2}}$ |

The number of unknown constants always equals $\deg Q$. Find them either by
substituting convenient values of $x$ (fastest for linear factors) or by
comparing coefficients (necessary for quadratic factors).
:::

::: example Worked example 13.22
**Problem.** Evaluate $\int \frac{dx}{(x-1)(x+2)}$ — **distinct linear factors**.

**Solution.** Write

$$ \frac{1}{(x-1)(x+2)} = \frac{A}{x-1} + \frac{B}{x+2} $$

Multiply through by $(x-1)(x+2)$: $\quad 1 = A(x+2) + B(x-1)$.

Put $x = 1$: $\;1 = 3A$, so $A = \frac13$. Put $x = -2$: $\;1 = -3B$, so
$B = -\frac13$. Therefore

$$ \int \frac{dx}{(x-1)(x+2)} = \frac13\int\frac{dx}{x-1} - \frac13\int\frac{dx}{x+2} $$

$$ = \frac13\ln|x-1| - \frac13\ln|x+2| + C = \frac{1}{3}\ln\left|\frac{x-1}{x+2}\right| + C $$
:::

::: example Worked example 13.23
**Problem.** Evaluate $\int \frac{dx}{(x-1)(x-2)(x-3)}$ and
$\int \frac{x\,dx}{(x-1)(x-2)}$.

**Solution.** **(a)** With
$\frac{1}{(x-1)(x-2)(x-3)} = \frac{A}{x-1}+\frac{B}{x-2}+\frac{C}{x-3}$ we get
$1 = A(x-2)(x-3) + B(x-1)(x-3) + C(x-1)(x-2)$.

Put $x=1$: $1 = A(-1)(-2) = 2A$, so $A = \frac12$.
Put $x=2$: $1 = B(1)(-1) = -B$, so $B = -1$.
Put $x=3$: $1 = C(2)(1) = 2C$, so $C = \frac12$.

$$ \int \frac{dx}{(x-1)(x-2)(x-3)}
= \frac12\ln|x-1| - \ln|x-2| + \frac12\ln|x-3| + C $$

**(b)** $\frac{x}{(x-1)(x-2)} = \frac{A}{x-1} + \frac{B}{x-2}$ gives
$x = A(x-2)+B(x-1)$. Put $x=1$: $A = -1$. Put $x=2$: $B = 2$. So

$$ \int \frac{x\,dx}{(x-1)(x-2)} = -\ln|x-1| + 2\ln|x-2| + C $$
:::

::: example Worked example 13.24
**Problem.** Evaluate $\int \frac{3x+5}{(x-1)^{2}(x+1)}\,dx$ — a **repeated
linear factor**.

**Solution.** The repeated factor needs *two* terms:

$$ \frac{3x+5}{(x-1)^{2}(x+1)} = \frac{A}{x-1} + \frac{B}{(x-1)^{2}} + \frac{D}{x+1} $$

Multiplying by $(x-1)^{2}(x+1)$:

$$ 3x+5 = A(x-1)(x+1) + B(x+1) + D(x-1)^{2} $$

Put $x=1$: $\;8 = 2B$, so $B = 4$.
Put $x=-1$: $\;2 = 4D$, so $D = \frac12$.
Compare the coefficients of $x^{2}$: $\;0 = A + D$, so $A = -\frac12$.

$$ \int \frac{3x+5}{(x-1)^{2}(x+1)}dx
= -\frac12\int\frac{dx}{x-1} + 4\int\frac{dx}{(x-1)^{2}} + \frac12\int\frac{dx}{x+1} $$

$$ = -\frac12\ln|x-1| - \frac{4}{x-1} + \frac12\ln|x+1| + C $$

using $\int (x-1)^{-2}dx = -\frac{1}{x-1}$. Note that only the *first-power*
terms give logarithms.
:::

::: caution The repeated factor needs both powers
Writing only $\frac{A}{(x-1)^{2}} + \frac{D}{x+1}$ gives two equations for a
problem that needs three constants, and the identity then fails for general $x$.
A factor $(x-a)^{n}$ always contributes $n$ terms, with denominators
$(x-a), (x-a)^{2}, \dots, (x-a)^{n}$.
:::

::: example Worked example 13.25
**Problem.** Evaluate $\int \frac{dx}{(x-1)\left(x^{2}+1\right)}$ — an
**irreducible quadratic factor**.

**Solution.** Since $x^{2}+1$ has no real factors, it takes a linear numerator:

$$ \frac{1}{(x-1)(x^{2}+1)} = \frac{A}{x-1} + \frac{Bx+D}{x^{2}+1} $$

$$ 1 = A\left(x^{2}+1\right) + (Bx+D)(x-1) $$

Put $x=1$: $\;1 = 2A$, so $A = \frac12$.
Coefficient of $x^{2}$: $\;0 = A + B$, so $B = -\frac12$.
Constant term: $\;1 = A - D$, so $D = -\frac12$.

$$ \int \frac{dx}{(x-1)(x^{2}+1)}
= \frac12\int \frac{dx}{x-1} - \frac12\int \frac{x+1}{x^{2}+1}\,dx $$

Split the second integral: $\frac{x}{x^{2}+1}$ is a $\frac{g'}{2g}$ pattern and
$\frac{1}{x^{2}+1}$ is a standard form.

$$ = \frac12\ln|x-1| - \frac14\ln\left(x^{2}+1\right) - \frac12\tan^{-1}x + C $$
:::

::: example Worked example 13.26
**Problem.** Evaluate $\int \frac{x^{3}+2x+1}{\left(x^{2}+1\right)^{2}}\,dx$ — a
**repeated quadratic factor**.

**Solution.** The decomposition is

$$ \frac{x^{3}+2x+1}{(x^{2}+1)^{2}} = \frac{Ax+B}{x^{2}+1} + \frac{Dx+E}{(x^{2}+1)^{2}} $$

Multiplying up, $\;x^{3}+2x+1 = (Ax+B)\left(x^{2}+1\right) + Dx + E$, i.e.

$$ x^{3}+2x+1 = Ax^{3} + Bx^{2} + (A+D)x + (B+E) $$

Comparing coefficients: $A = 1$, $B = 0$, $A + D = 2$ so $D = 1$, and
$B + E = 1$ so $E = 1$. Hence

$$ I = \int \frac{x\,dx}{x^{2}+1} + \int \frac{x\,dx}{(x^{2}+1)^{2}}
+ \int \frac{dx}{(x^{2}+1)^{2}} $$

The first two use $u = x^{2}+1$, $du = 2x\,dx$:

$$ \int \frac{x\,dx}{x^{2}+1} = \frac12\ln\left(x^{2}+1\right), \qquad
\int \frac{x\,dx}{(x^{2}+1)^{2}} = \frac12\int u^{-2}du = -\frac{1}{2(x^{2}+1)} $$

The third needs $x = \tan\theta$, $dx = \sec^{2}\theta\,d\theta$:

$$ \int \frac{\sec^{2}\theta\,d\theta}{\sec^{4}\theta} = \int \cos^{2}\theta\,d\theta
= \frac{\theta}{2} + \frac{\sin 2\theta}{4} = \frac{\theta}{2} + \frac{\sin\theta\cos\theta}{2} $$

With $\theta = \tan^{-1}x$, $\sin\theta = \frac{x}{\sqrt{1+x^{2}}}$ and
$\cos\theta = \frac{1}{\sqrt{1+x^{2}}}$, this is
$\frac12\tan^{-1}x + \frac{x}{2\left(1+x^{2}\right)}$. Collecting everything,

$$ I = \frac12\ln\left(x^{2}+1\right) + \frac{x-1}{2\left(x^{2}+1\right)}
+ \frac12\tan^{-1}x + C $$
:::

::: example Worked example 13.27
**Problem.** Evaluate $\int \frac{x^{2}+1}{(x+1)(x+2)}\,dx$ and
$\int \frac{x^{2}}{x^{2}+1}\,dx$ — **improper** fractions.

**Solution.** In both, the numerator degree is not less than the denominator
degree, so divide first.

**(a)** $\frac{x^{2}+1}{x^{2}+3x+2} = 1 + \frac{-3x-1}{(x+1)(x+2)}$. Now
$\frac{-3x-1}{(x+1)(x+2)} = \frac{A}{x+1} + \frac{B}{x+2}$ gives
$-3x-1 = A(x+2)+B(x+1)$. Put $x=-1$: $2 = A$. Put $x=-2$: $5 = -B$, so $B=-5$.

$$ \int \frac{x^{2}+1}{(x+1)(x+2)}dx = x + 2\ln|x+1| - 5\ln|x+2| + C $$

**(b)** $\frac{x^{2}}{x^{2}+1} = 1 - \frac{1}{x^{2}+1}$, so the integral is
$x - \tan^{-1}x + C$ at once. Dividing out first turns a hard-looking problem
into a one-line one.
:::

::: example Worked example 13.28
**Problem.** Evaluate $\int \frac{dx}{x^{3}+1}$.

**Solution.** Factorise the denominator using
$a^{3}+b^{3} = (a+b)\left(a^{2}-ab+b^{2}\right)$:
$\;x^{3}+1 = (x+1)\left(x^{2}-x+1\right)$, and $x^{2}-x+1$ is irreducible
(discriminant $1-4 = -3 < 0$). So

$$ \frac{1}{(x+1)(x^{2}-x+1)} = \frac{A}{x+1} + \frac{Bx+D}{x^{2}-x+1} $$

$$ 1 = A\left(x^{2}-x+1\right) + (Bx+D)(x+1) $$

Put $x=-1$: $\;1 = 3A$, so $A = \frac13$. Coefficient of $x^{2}$:
$0 = A + B$, so $B = -\frac13$. Constant: $1 = A + D$, so $D = \frac23$. Then

$$ I = \frac13\int\frac{dx}{x+1} - \frac13\int \frac{x-2}{x^{2}-x+1}\,dx $$

For the second integral, split the numerator using
$(x^{2}-x+1)' = 2x-1$: $\;x-2 = \frac12(2x-1) - \frac32$. Also
$x^{2}-x+1 = \left(x-\frac12\right)^{2} + \frac34$, so

$$ \int \frac{x-2}{x^{2}-x+1}dx = \frac12\ln\left(x^{2}-x+1\right)
- \frac32 \cdot \frac{2}{\sqrt{3}}\tan^{-1}\frac{2x-1}{\sqrt{3}} $$

Therefore

$$ \int \frac{dx}{x^{3}+1} = \frac13\ln|x+1| - \frac16\ln\left(x^{2}-x+1\right)
+ \frac{1}{\sqrt{3}}\tan^{-1}\left(\frac{2x-1}{\sqrt{3}}\right) + C $$
:::

## 13.4 The definite integral and its properties

Everything so far produced a *family of functions*. A definite integral produces
a single **number**, and that number measures an accumulation: area, distance,
total charge, total cost.

The shift is worth dwelling on. If $v(t)$ is the velocity of a bus on the
Prithvi Highway, then $\int v(t)\,dt$ is a family of position functions — useless
until you know where the bus started. But $\int_{9}^{12} v(t)\,dt$ is the
distance covered between nine and twelve o'clock, and that is a definite number
you can quote in kilometres. Definite integration is how a rate becomes a total.

::: definition Definite integral
If $f$ is continuous on $[a,b]$ and $F$ is any anti-derivative of $f$, then

$$ \int_{a}^{b} f(x)\,dx = \left[F(x)\right]_{a}^{b} = F(b) - F(a) $$

Here $a$ is the lower limit and $b$ the upper limit. The constant of integration
cancels, since $\left(F(b)+C\right) - \left(F(a)+C\right) = F(b)-F(a)$, which is
why a definite integral never carries $+C$.
:::

The link between the two halves of calculus is the **fundamental theorem**: if
$A(x) = \int_{a}^{x} f(t)\,dt$ is the accumulated area up to $x$, then
$A'(x) = f(x)$. Differentiating an area function gives back the curve. The
picture below is worth memorising, because it is the whole of calculus in two
panels.

```figure caption="Left: $A(x)$ is the shaded area under $f$ from $0$ to $x$. Right: the graph of $A$ itself. The slope of $A$ at $x=3$ equals the height $f(3)$ of the original curve — that is the fundamental theorem of calculus."
import numpy as np
fig, axs = plt.subplots(1, 2, figsize=(5.2,2.6))
x = np.linspace(0, 5, 600)
f = 1.2 + np.sin(x)
ax = axs[0]
ax.plot(x, f, color=INK, lw=1.7)
xf = np.linspace(0, 3, 400)
ax.fill_between(xf, 0, 1.2 + np.sin(xf), color=ACCENT, alpha=0.28)
ax.axvline(3, color='#d9534f', lw=1.1, ls='--')
ax.text(1.25, 0.42, '$A(x)$', fontsize=10.5, color='#14509a')
ax.annotate('$x$', (3.0, -0.30), fontsize=9.5, color='#9c3531', ha='center')
ax.set_title('$f(t) = 1.2 + \\sin t$', fontsize=9.2)
ax.set_xlabel('$t$'); ax.set_ylim(0, 2.6); ax.set_xlim(0, 5)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.4)
ax = axs[1]
A = np.concatenate([[0], np.cumsum((f[1:]+f[:-1])/2*np.diff(x))])
ax.plot(x, A, color=ACCENT, lw=1.8)
i = np.argmin(abs(x-3))
ax.plot([3],[A[i]],'o',color='#d9534f',ms=4.5)
xs = np.array([2.3, 3.7])
ax.plot(xs, A[i] + f[i]*(xs-3), color=INK, lw=1.1, ls='--')
ax.annotate('slope here $= f(3)$', (3.7, A[i]+f[i]*0.7), (0.35, 5.6),
            fontsize=8.6, color=INK, arrowprops=dict(arrowstyle='->', color=INK, lw=0.8))
ax.set_title('$A(x) = \\int_0^x f(t)\\,dt$', fontsize=9.2)
ax.set_xlabel('$x$'); ax.set_xlim(0, 5); ax.set_ylim(0, 7.2)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.4)
fig.tight_layout(pad=0.4)
```

A definite integral counts area **below** the axis as negative. So
$\int_{a}^{b} f\,dx$ is a *signed* area, and it can be zero even when the region
is large.

```figure caption="The definite integral as signed area. On $[0,\pi]$ the sine curve is above the axis and contributes $+2$; on $[\pi, 3\pi/2]$ it is below and contributes $-1$. Hence $\int_0^{3\pi/2}\sin x\,dx = 1$, although the total geometric area is $3$."
import numpy as np
fig, ax = plt.subplots(figsize=(5.0,2.8))
x = np.linspace(0, 3*np.pi/2, 500)
y = np.sin(x)
ax.plot(x, y, color=INK, lw=1.8)
xp = np.linspace(0, np.pi, 300)
xn = np.linspace(np.pi, 3*np.pi/2, 200)
ax.fill_between(xp, 0, np.sin(xp), color=ACCENT, alpha=0.30)
ax.fill_between(xn, 0, np.sin(xn), color='#d9534f', alpha=0.30)
ax.text(np.pi/2, 0.36, 'area $+2$', ha='center', fontsize=9.4, color='#14509a')
ax.text(np.pi*1.25, -0.48, 'area $-1$', ha='center', fontsize=9.4, color='#9c3531')
ax.axhline(0, color=MUTED, lw=0.9)
ax.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2])
ax.set_xticklabels(['$0$', '$\\pi/2$', '$\\pi$', '$3\\pi/2$'])
ax.set_xlabel('$x$'); ax.set_ylabel('$y = \\sin x$')
ax.set_xlim(-0.15, 3*np.pi/2 + 0.6); ax.set_ylim(-1.25, 1.35)
ax.annotate('net value $= 2 - 1 = 1$', (4.95, 1.02), fontsize=9.2, color=INK)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.4)
```

::: example Worked example 13.29
**Problem.** Evaluate (a) $\int_{1}^{2}\left(x^{2}+1\right)dx$,
(b) $\int_{0}^{\pi}\sin x\,dx$, (c) $\int_{0}^{3\pi/2}\sin x\,dx$,
(d) $\int_{0}^{2\pi}\sin x\,dx$.

**Solution.** Find an anti-derivative, then subtract.

**(a)** $\left[\frac{x^{3}}{3}+x\right]_{1}^{2}
= \left(\frac83+2\right) - \left(\frac13+1\right) = \frac{14}{3} - \frac43 = \frac{10}{3}$

**(b)** $\left[-\cos x\right]_{0}^{\pi} = -\cos\pi + \cos 0 = 1+1 = 2$

**(c)** $\left[-\cos x\right]_{0}^{3\pi/2} = -\cos\frac{3\pi}{2} + \cos 0 = 0 + 1 = 1$

**(d)** $\left[-\cos x\right]_{0}^{2\pi} = -1+1 = 0$

Parts (b), (c) and (d) are the three cases drawn in the figure: all area above,
part below, and exact cancellation.
:::

::: caution Change the limits when you change the variable
In a definite integral you may either (i) convert the limits to the new
variable, or (ii) integrate back to $x$ first and then substitute. What you must
**never** do is use the old limits with the new variable. In
$\int_{0}^{4}\frac{x\,dx}{\sqrt{x^{2}+9}}$ with $u = x^{2}+9$, the limits become
$u = 9$ and $u = 25$, not $0$ and $4$.
:::

::: example Worked example 13.30
**Problem.** Evaluate $\int_{0}^{4}\frac{x}{\sqrt{x^{2}+9}}\,dx$ and
$\int_{0}^{1} x e^{x}\,dx$.

**Solution.** **(a)** Put $u = x^{2}+9$, so $du = 2x\,dx$. When $x=0$, $u=9$;
when $x=4$, $u=25$.

$$ \int_{0}^{4}\frac{x\,dx}{\sqrt{x^{2}+9}} = \frac12\int_{9}^{25}\frac{du}{\sqrt{u}}
= \frac12\left[2\sqrt{u}\right]_{9}^{25} = \left[\sqrt{u}\right]_{9}^{25} = 5-3 = 2 $$

**(b)** By parts, using Worked example 13.9:

$$ \int_{0}^{1}x e^{x}dx = \left[(x-1)e^{x}\right]_{0}^{1}
= (0)e^{1} - (-1)e^{0} = 0 + 1 = 1 $$
:::

### The eight properties

::: key Properties of the definite integral
**P1** $\displaystyle\int_{a}^{b} f(x)\,dx = -\int_{b}^{a} f(x)\,dx$, and
$\displaystyle\int_{a}^{a} f(x)\,dx = 0$

**P2** $\displaystyle\int_{a}^{b} f(x)\,dx = \int_{a}^{c} f(x)\,dx + \int_{c}^{b} f(x)\,dx$
for any $c$

**P3** $\displaystyle\int_{a}^{b} f(x)\,dx = \int_{a}^{b} f(t)\,dt$ — the
variable of integration is a dummy

**P4** $\displaystyle\int_{0}^{a} f(x)\,dx = \int_{0}^{a} f(a-x)\,dx$

**P5** $\displaystyle\int_{a}^{b} f(x)\,dx = \int_{a}^{b} f(a+b-x)\,dx$

**P6** $\displaystyle\int_{-a}^{a} f(x)\,dx = 2\int_{0}^{a} f(x)\,dx$ if $f$ is
even, and $= 0$ if $f$ is odd

**P7** $\displaystyle\int_{0}^{2a} f(x)\,dx = 2\int_{0}^{a} f(x)\,dx$ if
$f(2a-x) = f(x)$, and $= 0$ if $f(2a-x) = -f(x)$

**P8** $\displaystyle\int_{0}^{a} f(x)\,dx \ge 0$ if $f(x)\ge 0$ on $[a,b]$, and
$\left|\int_{a}^{b}f\right| \le \int_{a}^{b}|f|$
:::

::: derivation Why P4 is true
In $\int_{0}^{a} f(x)\,dx$ put $x = a - t$, so $dx = -dt$. When $x=0$, $t=a$, and
when $x=a$, $t=0$:

$$ \int_{0}^{a} f(x)\,dx = \int_{a}^{0} f(a-t)\,(-dt) = \int_{0}^{a} f(a-t)\,dt $$

using P1 to swap the limits and absorb the minus sign. By P3 the dummy $t$ may
be renamed $x$, which is P4. The same substitution $x = a+b-t$ proves P5.

P4 and P5 are the two properties that make "impossible" integrals collapse: add
the original to the reflected copy and the integrand often becomes a constant.
:::

::: example Worked example 13.31
**Problem.** Evaluate $I = \displaystyle\int_{0}^{\pi/2}
\frac{\sqrt{\sin x}}{\sqrt{\sin x}+\sqrt{\cos x}}\,dx$.

**Solution.** No anti-derivative of this integrand exists in elementary terms,
so use P4 with $a = \frac{\pi}{2}$. Since
$\sin\left(\frac{\pi}{2}-x\right) = \cos x$ and
$\cos\left(\frac{\pi}{2}-x\right) = \sin x$,

$$ I = \int_{0}^{\pi/2}\frac{\sqrt{\cos x}}{\sqrt{\cos x}+\sqrt{\sin x}}\,dx $$

Add the two expressions for $I$. The denominators are now identical:

$$ 2I = \int_{0}^{\pi/2}\frac{\sqrt{\sin x}+\sqrt{\cos x}}{\sqrt{\sin x}+\sqrt{\cos x}}\,dx
= \int_{0}^{\pi/2} 1\,dx = \frac{\pi}{2} $$

$$ I = \frac{\pi}{4} $$

The same argument gives $\int_{0}^{\pi/2}\frac{dx}{1+\tan x} = \frac{\pi}{4}$ and
$\int_{0}^{\pi/2}\sin^{2}x\,dx = \int_{0}^{\pi/2}\cos^{2}x\,dx = \frac{\pi}{4}$,
because in each case the two copies add to $1$.
:::

::: example Worked example 13.32
**Problem.** Use P6 to evaluate $\int_{-1}^{1}\left(x^{3}+x\right)dx$ and
$\int_{-2}^{2}x^{2}\,dx$.

**Solution.** Test the parity first.

**(a)** $f(-x) = -x^{3}-x = -f(x)$, so $f$ is **odd** and the integral over a
symmetric interval is $0$. (Check directly:
$\left[\frac{x^{4}}{4}+\frac{x^{2}}{2}\right]_{-1}^{1} = \frac34 - \frac34 = 0$.)

**(b)** $f(-x) = x^{2} = f(x)$, so $f$ is **even**:

$$ \int_{-2}^{2}x^{2}dx = 2\int_{0}^{2}x^{2}dx = 2\left[\frac{x^{3}}{3}\right]_{0}^{2}
= 2 \cdot \frac83 = \frac{16}{3} $$

For a mixed integrand, split it: $\int_{-2}^{2}\left(x^{3}+3x^{2}\right)dx
= 0 + 3 \cdot \frac{16}{3} = 16$, because the cube is odd and the square is even.
Recognising parity turns a two-substitution problem into one line.
:::

::: example Worked example 13.33
**Problem.** Evaluate $\int_{0}^{\pi} x\sin x\,dx$ two ways.

**Solution.** **By parts.** With $u = x$ and $dv = \sin x\,dx$,

$$ \int_{0}^{\pi}x\sin x\,dx = \left[-x\cos x\right]_{0}^{\pi}
+ \int_{0}^{\pi}\cos x\,dx = \pi + \left[\sin x\right]_{0}^{\pi} = \pi + 0 = \pi $$

**By P4.** Replacing $x$ by $\pi - x$ and using $\sin(\pi-x) = \sin x$,

$$ I = \int_{0}^{\pi}(\pi-x)\sin x\,dx = \pi\int_{0}^{\pi}\sin x\,dx - I $$

so $2I = \pi \cdot 2 = 2\pi$ and $I = \pi$. The second method needs only
$\int_{0}^{\pi}\sin x\,dx = 2$, and it generalises: for any $f$,
$\int_{0}^{\pi}x f(\sin x)\,dx = \frac{\pi}{2}\int_{0}^{\pi}f(\sin x)\,dx$.
:::

::: example Worked example 13.34
**Problem.** Evaluate (a) $\int_{1}^{2}\frac{dx}{x(x+1)}$,
(b) $\int_{3}^{5}\frac{dx}{\sqrt{x^{2}-9}}$, (c) $\int_{0}^{\pi/2}\cos^{3}x\,dx$.

**Solution.** **(a)** Partial fractions:
$\frac{1}{x(x+1)} = \frac1x - \frac{1}{x+1}$, so

$$ \left[\ln|x| - \ln|x+1|\right]_{1}^{2} = \left[\ln\frac{x}{x+1}\right]_{1}^{2}
= \ln\frac23 - \ln\frac12 = \ln\frac43 $$

**(b)** A standard form with $a=3$:

$$ \left[\ln\left|x+\sqrt{x^{2}-9}\right|\right]_{3}^{5} = \ln(5+4) - \ln 3
= \ln 9 - \ln 3 = \ln 3 $$

**(c)** Write $\cos^{3}x = \cos x\left(1-\sin^{2}x\right)$ and put
$u = \sin x$, with limits $u=0$ to $u=1$:

$$ \int_{0}^{1}\left(1-u^{2}\right)du = \left[u - \frac{u^{3}}{3}\right]_{0}^{1}
= 1 - \frac13 = \frac{2}{3} $$
:::

## 13.5 The definite integral as the limit of a sum

The definite integral was *defined* long before anti-derivatives, as the limiting
total of thin rectangles. NEB asks for this derivation, so learn the four steps.

The idea is older than calculus: Greek mathematicians found areas by filling
shapes with polygons and letting the number of sides grow. What Newton and
Leibniz added was the discovery that this limit can be computed without any
limits at all, by anti-differentiating. When a question says "evaluate as the
limit of a sum", however, it is asking for the *long* method, and no marks are
available for quoting $F(b)-F(a)$.

::: derivation The definite integral as a limit
Divide $[a,b]$ into $n$ equal sub-intervals, each of width $h = \frac{b-a}{n}$.
The division points are $a,\;a+h,\;a+2h,\;\dots,\;a+nh = b$.

**Step 1.** On the $r$-th sub-interval take the rectangle of height
$f(a+rh)$ (the right-hand endpoint). Its area is $h\,f(a+rh)$.

**Step 2.** Add the $n$ rectangles:

$$ S_{n} = h\sum_{r=1}^{n} f(a+rh) = \frac{b-a}{n}\sum_{r=1}^{n}
f\left(a + \frac{r(b-a)}{n}\right) $$

**Step 3.** As $n\to\infty$ the rectangles get thinner and $S_{n}$ closes in on
the exact area. Define

$$ \int_{a}^{b} f(x)\,dx = \lim_{n\to\infty} \frac{b-a}{n}\sum_{r=1}^{n}
f\left(a + \frac{r(b-a)}{n}\right) $$

**Step 4.** Evaluate the sum in closed form using
$\sum r = \frac{n(n+1)}{2}$, $\sum r^{2} = \frac{n(n+1)(2n+1)}{6}$,
$\sum r^{3} = \frac{n^{2}(n+1)^{2}}{4}$, or the geometric series for $e^{x}$, and
then take the limit.
:::

```figure caption="Right-endpoint Riemann sums for $y=x^2$ on $[0,1]$. The overshoot above the curve shrinks as the rectangles thin: $S_4 = 0.4688$, $S_{10} = 0.3850$, $S_{40} = 0.3459$, converging on the exact value $\frac13$."
import numpy as np
fig, axs = plt.subplots(1, 3, figsize=(5.2,2.35), sharey=True)
xs = np.linspace(0, 1, 300)
for ax, n in zip(axs, [4, 10, 40]):
    h = 1.0/n
    xr = np.arange(1, n+1)*h
    ax.bar(xr - h, xr**2, width=h, align='edge', color=ACCENT, alpha=0.30,
           edgecolor=INK, linewidth=0.55 if n < 20 else 0.18)
    ax.plot(xs, xs**2, color='#d9534f', lw=1.6)
    S = h*np.sum(xr**2)
    ax.set_title('$n=%d$:  $S_n = %.4f$' % (n, S), fontsize=8.8)
    ax.set_xlim(0, 1.02); ax.set_xticks([0, 0.5, 1])
    ax.spines[['top','right']].set_visible(False)
    ax.set_xlabel('$x$')
axs[0].set_ylim(0, 1.08); axs[0].set_ylabel('$y = x^2$')
axs[2].annotate('exact $\\frac{1}{3}$', (0.06, 0.74), fontsize=9.0, color=INK)
fig.tight_layout(pad=0.4)
```

::: example Worked example 13.35
**Problem.** Evaluate $\int_{0}^{1}x^{2}\,dx$ as the limit of a sum.

**Solution.** Here $a=0$, $b=1$, $f(x)=x^{2}$ and $h = \frac1n$, so
$f(a+rh) = \left(\frac{r}{n}\right)^{2}$.

$$ S_{n} = \frac{1}{n}\sum_{r=1}^{n}\frac{r^{2}}{n^{2}}
= \frac{1}{n^{3}}\sum_{r=1}^{n} r^{2}
= \frac{1}{n^{3}} \cdot \frac{n(n+1)(2n+1)}{6} $$

Expand the numerator and divide through by $n^{3}$:

$$ S_{n} = \frac{2n^{2}+3n+1}{6n^{2}}
= \frac{1}{6}\left(2 + \frac{3}{n} + \frac{1}{n^{2}}\right) $$

Let $n\to\infty$, so that $\frac3n\to 0$ and $\frac{1}{n^{2}}\to 0$:

$$ \int_{0}^{1}x^{2}dx = \lim_{n\to\infty} S_{n} = \frac{2}{6} = \frac{1}{3} $$

This agrees with $\left[\frac{x^{3}}{3}\right]_{0}^{1} = \frac13$, and the
numbers in the figure — $0.4688$, $0.3850$, $0.3459$ — are $S_4$, $S_{10}$ and
$S_{40}$ from this very formula.
:::

::: example Worked example 13.36
**Problem.** Evaluate $\int_{0}^{1}e^{x}\,dx$ and $\int_{0}^{2}\left(x^{2}+1\right)dx$
as limits of sums.

**Solution.** **(a)** With $h = \frac1n$, $f(a+rh) = e^{r/n}$, so the sum is
geometric with first term $e^{1/n}$ and ratio $e^{1/n}$:

$$ S_{n} = \frac{1}{n}\sum_{r=1}^{n}e^{r/n}
= \frac{1}{n} \cdot \frac{e^{1/n}\left(e^{n \cdot \frac1n}-1\right)}{e^{1/n}-1}
= \frac{e^{1/n}(e-1)}{n\left(e^{1/n}-1\right)} $$

Write $t = \frac1n$, so $t\to 0$ as $n\to\infty$:

$$ \lim_{n\to\infty}S_{n} = (e-1)\lim_{t\to 0}\frac{e^{t} \cdot t}{e^{t}-1}
= (e-1) \cdot 1 = e-1 $$

using the standard limit $\lim_{t\to 0}\frac{e^{t}-1}{t} = 1$. And indeed
$\left[e^{x}\right]_{0}^{1} = e-1$.

**(b)** Now $a=0$, $b=2$, $h = \frac2n$ and
$f(a+rh) = \frac{4r^{2}}{n^{2}}+1$:

$$ S_{n} = \frac{2}{n}\sum_{r=1}^{n}\left(\frac{4r^{2}}{n^{2}}+1\right)
= \frac{8}{n^{3}} \cdot \frac{n(n+1)(2n+1)}{6} + \frac{2}{n} \cdot n $$

$$ = \frac{4}{3}\left(2+\frac3n+\frac{1}{n^{2}}\right)\cdot\frac12 \cdot 2 + 2
\;\longrightarrow\; \frac{8}{3} + 2 = \frac{14}{3} $$

which matches $\left[\frac{x^{3}}{3}+x\right]_{0}^{2} = \frac83+2 = \frac{14}{3}$.
:::

## 13.6 Area under a curve and area between two curves

::: key The four area formulas
**Under a curve, above the $x$-axis:**
$$ A = \int_{a}^{b} y\,dx = \int_{a}^{b} f(x)\,dx $$

**Between a curve and the $y$-axis** (horizontal strips):
$$ A = \int_{c}^{d} x\,dy $$

**Between two curves**, with $f$ the upper one on $[a,b]$:
$$ A = \int_{a}^{b}\left[f(x) - g(x)\right]dx $$

**When the curve dips below the axis**, integrate each piece separately and add
the absolute values, because area is never negative.
:::

The strip is the thing to picture. A vertical strip at $x$ has height $y$ and
thickness $dx$, so its area is $y\,dx$, and the integral sweeps it from $a$ to
$b$. A horizontal strip at height $y$ has length $x$ and thickness $dy$, giving
$x\,dy$.

Every area question is then the same four steps.

1. **Sketch** the curves, roughly but with the intersections and axis crossings
   in the right places.
2. **Find the limits** by solving the two equations simultaneously, or by setting
   $y=0$ if one boundary is the axis.
3. **Decide the strip direction**, and which boundary is the upper or outer one.
4. **Integrate** the strip area and evaluate.

Skipping the sketch is what causes the two classic errors: subtracting the curves
the wrong way round, and missing a region where the curve crosses the axis.

::: example Worked example 13.37
**Problem.** Find the area bounded by $y = x^{2}$, the $x$-axis and the lines
$x=0$ and $x=3$.

**Solution.** The curve is above the axis throughout $[0,3]$, so

$$ A = \int_{0}^{3} x^{2}\,dx = \left[\frac{x^{3}}{3}\right]_{0}^{3}
= \frac{27}{3} - 0 = 9 \text{ square units} $$

Similarly $\int_{0}^{2}x^{3}dx = \left[\frac{x^{4}}{4}\right]_{0}^{2} = 4$ and
$\int_{1}^{e}\frac{dx}{x} = \left[\ln x\right]_{1}^{e} = 1$ — the area under the
rectangular hyperbola from $1$ to $e$ is exactly one square unit, which is what
makes $e$ the natural base.
:::

::: example Worked example 13.38
**Problem.** Find the area enclosed between the line $y = 2x$ and the parabola
$y = x^{2}$.

**Solution.** **Step 1 — find the intersections.** Solve
$x^{2} = 2x$, i.e. $x(x-2) = 0$, so $x = 0$ and $x = 2$.

**Step 2 — decide which curve is on top.** At $x=1$, the line gives $2$ and the
parabola gives $1$, so the line is above throughout $(0,2)$.

**Step 3 — integrate the difference.**

$$ A = \int_{0}^{2}\left(2x - x^{2}\right)dx
= \left[x^{2} - \frac{x^{3}}{3}\right]_{0}^{2} = 4 - \frac83 = \frac{4}{3} $$

**Step 4 — state the answer.** The enclosed area is $\frac43$ square units.
:::

```figure caption="Area between $y=2x$ and $y=x^2$. Each vertical strip has height $(2x)-x^2$ and thickness $dx$, and the strips run between the intersections $x=0$ and $x=2$, giving $\int_0^2 (2x-x^2)dx = \frac43$."
import numpy as np
fig, ax = plt.subplots(figsize=(4.7,2.9))
x = np.linspace(-0.4, 2.5, 400)
ax.plot(x, 2*x, color=ACCENT, lw=1.8, label='$y = 2x$')
ax.plot(x, x**2, color='#d9534f', lw=1.8, label='$y = x^2$')
xf = np.linspace(0, 2, 300)
ax.fill_between(xf, xf**2, 2*xf, color=ACCENT, alpha=0.20)
xs = 1.6
ax.plot([xs, xs], [xs**2, 2*xs], color=INK, lw=2.6, alpha=0.8)
ax.annotate('strip of height $(2x) - x^2$', (xs, (xs**2+2*xs)/2), (-0.40, 4.75),
            fontsize=8.6, color=INK,
            arrowprops=dict(arrowstyle='->', color=INK, lw=0.8))
for px, py, lab in [(0,0,'$(0,0)$'), (2,4,'$(2,4)$')]:
    ax.plot([px],[py],'o',color=INK,ms=4)
    ax.annotate(lab, (px,py), textcoords='offset points', xytext=(6,-2), fontsize=8.8)
ax.text(0.12, 2.62, 'area $= \\frac{4}{3}$', fontsize=10, color='#14509a')
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.set_xlim(-0.55, 2.85); ax.set_ylim(-0.9, 5.5)
ax.axhline(0, color=MUTED, lw=0.7); ax.axvline(0, color=MUTED, lw=0.7)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.4); ax.legend(loc='lower right', fontsize=8.4)
```

::: example Worked example 13.39
**Problem.** Find the area bounded by the parabola $x = y^{2}$, the $y$-axis and
the line $y = 2$.

**Solution.** The bounding line is horizontal and the region touches the
$y$-axis, so use **horizontal strips** and integrate with respect to $y$. A strip
at height $y$ has length $x = y^{2}$ and thickness $dy$, so

$$ A = \int_{0}^{2} x\,dy = \int_{0}^{2} y^{2}\,dy
= \left[\frac{y^{3}}{3}\right]_{0}^{2} = \frac{8}{3}\text{ square units} $$

Doing the same region with vertical strips would need
$\int_{0}^{4}\left(2-\sqrt{x}\right)dx$ — correct, but longer. **Choose the strip
direction that makes the limits constants.**
:::

```figure caption="The same area computed with horizontal strips. Each strip has length $x = y^2$ and thickness $dy$, so $A = \int_0^2 y^2\,dy = \frac83$. Use horizontal strips whenever the region is bounded by the $y$-axis and horizontal lines."
import numpy as np
fig, ax = plt.subplots(figsize=(4.4,3.2))
y = np.linspace(0, 2.15, 300)
ax.plot(y**2, y, color='#d9534f', lw=1.9)
yf = np.linspace(0, 2, 300)
ax.fill_betweenx(yf, 0, yf**2, color=ACCENT, alpha=0.20)
for yy in np.linspace(0.12, 1.94, 11):
    ax.plot([0, yy**2], [yy, yy], color=ACCENT, lw=1.1, alpha=0.75)
ax.annotate('strip: length $x = y^2$,\nthickness $dy$', (1.2, 1.095), (1.75, 0.30),
            fontsize=8.6, color=INK,
            arrowprops=dict(arrowstyle='->', color=INK, lw=0.8))
ax.annotate('$y = 2$', (4.0, 2.0), (2.5, 2.08), fontsize=9.0, color=INK,
            arrowprops=dict(arrowstyle='->', color=INK, lw=0.8))
ax.plot([0, 4.0], [2, 2], color=MUTED, lw=0.9, ls=':')
ax.text(0.28, 1.55, 'area $= \\frac{8}{3}$', fontsize=10, color='#14509a')
ax.text(4.05, 1.62, '$x = y^2$', fontsize=10, color='#9c3531')
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.set_xlim(-0.35, 5.3); ax.set_ylim(-0.22, 2.35)
ax.axhline(0, color=MUTED, lw=0.7)
ax.axvline(0, color=INK, lw=1.4)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.4)
```

::: example Worked example 13.40
**Problem.** Find the area of the circle $x^{2}+y^{2} = a^{2}$, and hence the
area of the ellipse $\frac{x^{2}}{a^{2}} + \frac{y^{2}}{b^{2}} = 1$.

**Solution.** **Circle.** By symmetry the total area is four times the first
quadrant piece, where $y = \sqrt{a^{2}-x^{2}}$ and $x$ runs from $0$ to $a$:

$$ A = 4\int_{0}^{a}\sqrt{a^{2}-x^{2}}\,dx
= 4\left[\frac{x}{2}\sqrt{a^{2}-x^{2}} + \frac{a^{2}}{2}\sin^{-1}\frac{x}{a}\right]_{0}^{a} $$

using Worked example 13.17. At $x=a$ the first term vanishes and
$\sin^{-1}1 = \frac{\pi}{2}$, so

$$ A = 4\left(0 + \frac{a^{2}}{2}\cdot\frac{\pi}{2}\right) = \pi a^{2} $$

**Ellipse.** In the first quadrant
$y = \frac{b}{a}\sqrt{a^{2}-x^{2}}$, so the whole calculation is scaled by
$\frac ba$:

$$ A = 4\cdot\frac{b}{a}\int_{0}^{a}\sqrt{a^{2}-x^{2}}\,dx
= \frac{4b}{a}\cdot\frac{\pi a^{2}}{4} = \pi a b $$

With $a=4$ and $b=3$ this gives $12\pi$, and the shaded quarter in the figure is
$3\pi$.
:::

```figure caption="The ellipse $\frac{x^2}{16}+\frac{y^2}{9}=1$. Vertical strips in the first quadrant have height $y = \frac{b}{a}\sqrt{a^2-x^2}$, so the quarter area is $\frac{b}{a}\int_0^a \sqrt{a^2-x^2}\,dx = \frac{\pi a b}{4} = 3\pi$ and the whole ellipse has area $\pi a b = 12\pi$."
import numpy as np
fig, ax = plt.subplots(figsize=(4.9,2.9))
a, b = 4.0, 3.0
t = np.linspace(0, 2*np.pi, 600)
ax.plot(a*np.cos(t), b*np.sin(t), color=INK, lw=1.6)
xq = np.linspace(0, a, 300)
ax.fill_between(xq, 0, b*np.sqrt(np.clip(1-xq**2/a**2, 0, None)),
                color=ACCENT, alpha=0.26)
for xx in np.linspace(0.22, 3.86, 12):
    yy = b*np.sqrt(max(1-xx**2/a**2, 0))
    ax.plot([xx, xx], [0, yy], color=ACCENT, lw=1.0, alpha=0.8)
ax.annotate('strip height $y = \\frac{b}{a}\\sqrt{a^2-x^2}$', (2.2, 1.25), (-4.95, -3.55),
            fontsize=8.8, color=INK, arrowprops=dict(arrowstyle='->', color=INK, lw=0.8))
ax.text(0.45, 1.85, 'quarter\narea', fontsize=9.0, color='#14509a')
ax.text(-4.75, 2.05, 'total area $= \\pi a b$', fontsize=9.6, color=INK)
ax.plot([a],[0],'o',color=INK,ms=3.6); ax.plot([0],[b],'o',color=INK,ms=3.6)
ax.annotate('$(a,0)$', (a,0), textcoords='offset points', xytext=(3,-11), fontsize=8.6)
ax.annotate('$(0,b)$', (0,b), textcoords='offset points', xytext=(4,2), fontsize=8.6)
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.axhline(0, color=MUTED, lw=0.7); ax.axvline(0, color=MUTED, lw=0.7)
ax.set_xlim(-5.2, 5.7); ax.set_ylim(-4.35, 3.7)
ax.set_aspect('equal')
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.35)
```

::: example Worked example 13.41
**Problem.** Find the area enclosed between the parabolas $y^{2} = 4x$ and
$x^{2} = 4y$.

**Solution.** **Intersections.** From the second, $y = \frac{x^{2}}{4}$.
Substituting into the first, $\frac{x^{4}}{16} = 4x$, so $x^{4} = 64x$, giving
$x\left(x^{3}-64\right) = 0$ and hence $x = 0$ or $x = 4$.

**Upper curve.** At $x=1$, $y^{2}=4x$ gives $y = 2$ while $x^{2}=4y$ gives
$y = \frac14$. So $y = 2\sqrt{x}$ is above $y = \frac{x^{2}}{4}$.

$$ A = \int_{0}^{4}\left(2\sqrt{x} - \frac{x^{2}}{4}\right)dx
= \left[\frac{4x^{3/2}}{3} - \frac{x^{3}}{12}\right]_{0}^{4} $$

$$ = \frac{4 \cdot 8}{3} - \frac{64}{12} = \frac{32}{3} - \frac{16}{3}
= \frac{16}{3}\text{ square units} $$
:::

::: example Worked example 13.42
**Problem.** Find the area bounded by $y = 4-x^{2}$ and the $x$-axis, and the
area enclosed between $y = x^{2}$ and $y = x^{3}$.

**Solution.** **(a)** The parabola cuts the axis where $4-x^{2}=0$, i.e.
$x = \pm 2$, and is above the axis between them. The function is even, so

$$ A = 2\int_{0}^{2}\left(4-x^{2}\right)dx
= 2\left[4x - \frac{x^{3}}{3}\right]_{0}^{2} = 2\left(8-\frac83\right)
= \frac{32}{3} $$

**(b)** $x^{2} = x^{3}$ gives $x^{2}(1-x) = 0$, so $x = 0$ and $x = 1$. On
$(0,1)$ we have $x^{2} > x^{3}$ (test $x = \frac12$: $\frac14 > \frac18$), so

$$ A = \int_{0}^{1}\left(x^{2}-x^{3}\right)dx
= \left[\frac{x^{3}}{3}-\frac{x^{4}}{4}\right]_{0}^{1} = \frac13-\frac14
= \frac{1}{12} $$
:::

::: caution Areas below the axis
$\int_{-1}^{1}x^{3}dx = 0$, but the region between the cubic and the axis from
$-1$ to $1$ has area $\frac12$. If the curve crosses the axis inside the
interval, **find the crossing points first**, integrate over each piece, and add
the magnitudes. Writing a single integral and reporting a negative "area" loses
the mark every time.
:::

## Chapter summary

- **Anti-differentiation** reverses differentiation:
  $\int f(x)\,dx = F(x)+C$ where $F' = f$. The $+C$ is compulsory, and it makes
  the answer a whole family of parallel curves.
- Learn the **table of standard integrals** to the point of recall, including
  $\int\frac{dx}{x} = \ln|x|$, the nine quadratic forms, and
  $\int\tan x\,dx = \ln|\sec x|$, $\int\sec x\,dx = \ln|\sec x+\tan x|$.
- **Substitution** works when the integrand contains $g(x)$ together with
  $g'(x)$. The master pattern is
  $\int\frac{g'(x)}{g(x)}dx = \ln|g(x)|+C$.
- **By parts**: $\int u\,dv = uv - \int v\,du$, with $u$ chosen by **ILATE**.
  Polynomial times sine or exponential needs repeated parts; $e^{ax}\sin bx$ is
  cyclic, so apply parts twice and solve for $I$; and
  $\int e^{x}\left[f+f'\right]dx = e^{x}f(x)+C$ in one step.
- A quadratic denominator is handled by **completing the square**; an $x$ in the
  numerator by splitting $px+q = \lambda(\text{denominator})' + \mu$.
- Radicals $\sqrt{a^{2}-x^{2}}$, $\sqrt{a^{2}+x^{2}}$, $\sqrt{x^{2}-a^{2}}$ call
  for $x = a\sin\theta$, $a\tan\theta$, $a\sec\theta$; draw the reference
  triangle to convert back.
- Any rational function of $\sin x$ and $\cos x$ yields to
  $t = \tan\frac{x}{2}$, using $\sin x = \frac{2t}{1+t^{2}}$,
  $\cos x = \frac{1-t^{2}}{1+t^{2}}$, $dx = \frac{2\,dt}{1+t^{2}}$.
- **Rational functions**: divide first if improper, then split into partial
  fractions according to the four denominator cases.
- $\int_{a}^{b}f = F(b)-F(a)$ is a **number** and a *signed* area. The
  properties P4, P5 (reflection) and P6, P7 (symmetry) evaluate integrals whose
  anti-derivatives do not exist in elementary form.
- As a **limit of a sum**,
  $\int_{a}^{b}f\,dx = \lim_{n\to\infty}\frac{b-a}{n}\sum_{r=1}^{n}
  f\left(a+\frac{r(b-a)}{n}\right)$.
- **Areas**: $\int_{a}^{b}y\,dx$ for vertical strips, $\int_{c}^{d}x\,dy$ for
  horizontal strips, $\int_{a}^{b}(\text{upper}-\text{lower})\,dx$ between two
  curves, and split the interval wherever the curve crosses the axis.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. $\int \dfrac{dx}{x}$ equals <span class="marks">[1]</span>
   (a) $-\dfrac{1}{x^{2}}+C$ (b) $\ln|x|+C$ (c) $x\ln x - x + C$ (d) $\dfrac{1}{2x^{2}}+C$
2. $\int \dfrac{dx}{x^{2}+9}$ equals <span class="marks">[1]</span>
   (a) $\dfrac13\tan^{-1}\dfrac{x}{3}+C$ (b) $\tan^{-1}\dfrac{x}{3}+C$ (c) $\dfrac19\tan^{-1}\dfrac{x}{3}+C$ (d) $\dfrac13\sin^{-1}\dfrac{x}{3}+C$
3. $\int_{0}^{1}e^{x}\,dx$ equals <span class="marks">[1]</span>
   (a) $e$ (b) $e-1$ (c) $1-e$ (d) $e+1$
4. $\int_{-2}^{2}x^{3}\,dx$ equals <span class="marks">[1]</span>
   (a) $8$ (b) $16$ (c) $0$ (d) $\dfrac{16}{3}$
5. $\int \tan x\,dx$ equals <span class="marks">[1]</span>
   (a) $\sec^{2}x+C$ (b) $\ln|\sin x|+C$ (c) $\ln|\sec x|+C$ (d) $\ln|\sec x+\tan x|+C$
6. To evaluate $\int\sqrt{x^{2}-a^{2}}\,dx$ the correct substitution is <span class="marks">[1]</span>
   (a) $x=a\sin\theta$ (b) $x=a\tan\theta$ (c) $x=a\sec\theta$ (d) $x=a\cos\theta$
7. The area bounded by $y=x^{2}$, the $x$-axis, $x=0$ and $x=3$ is <span class="marks">[1]</span>
   (a) $3$ (b) $9$ (c) $27$ (d) $\dfrac{27}{2}$

::: note Answers to Group A
**1.** (b) — the only case of $\int x^{n}dx$ that is not a power, and the modulus
keeps it valid for $x<0$.

**2.** (a) — standard form $\int\frac{dx}{x^{2}+a^{2}} = \frac1a\tan^{-1}\frac xa+C$
with $a=3$.

**3.** (b) — $\left[e^{x}\right]_{0}^{1} = e - 1$.

**4.** (c) — $x^{3}$ is odd and the interval is symmetric, so P6 gives $0$.

**5.** (c) — put $u=\cos x$: $\int\tan x\,dx = -\ln|\cos x| = \ln|\sec x|+C$.
Option (d) is $\int\sec x\,dx$.

**6.** (c) — then $x^{2}-a^{2} = a^{2}\left(\sec^{2}\theta-1\right) = a^{2}\tan^{2}\theta$
and the radical disappears.

**7.** (b) — $\int_{0}^{3}x^{2}dx = \left[\frac{x^{3}}{3}\right]_{0}^{3} = 9$.
:::

**Group B — Short answer (5 marks each)**

1. Evaluate $\int x^{2}\sin x\,dx$. <span class="marks">[5]</span>
2. Evaluate $\int \dfrac{dx}{x^{2}+6x+13}$. <span class="marks">[5]</span>
3. Evaluate $\int \dfrac{2x+1}{(x+1)(x-2)}\,dx$. <span class="marks">[5]</span>
4. Using the properties of definite integrals, evaluate
   $\int_{0}^{\pi/2}\dfrac{dx}{1+\tan x}$. <span class="marks">[5]</span>
5. Evaluate $\int \dfrac{dx}{1+\sin x}$ by the substitution
   $t=\tan\dfrac{x}{2}$. <span class="marks">[5]</span>
6. Find the area of the region enclosed between the line $y=x$ and the curve
   $y=x^{3}$ in the first quadrant. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** By ILATE take $u=x^{2}$, $dv=\sin x\,dx$, so $v=-\cos x$:

$$ \int x^{2}\sin x\,dx = -x^{2}\cos x + 2\int x\cos x\,dx $$

Apply parts again with $u=x$, $dv=\cos x\,dx$, $v=\sin x$:
$\int x\cos x\,dx = x\sin x + \cos x$. Hence

$$ \int x^{2}\sin x\,dx = -x^{2}\cos x + 2x\sin x + 2\cos x + C $$

**2.** Complete the square: $x^{2}+6x+13 = (x+3)^{2}+2^{2}$. Put $t = x+3$, so
$dt = dx$:

$$ \int\frac{dt}{t^{2}+2^{2}} = \frac12\tan^{-1}\frac t2 + C
= \frac{1}{2}\tan^{-1}\left(\frac{x+3}{2}\right) + C $$

**3.** Let $\frac{2x+1}{(x+1)(x-2)} = \frac{A}{x+1}+\frac{B}{x-2}$, so
$2x+1 = A(x-2)+B(x+1)$. Put $x=-1$: $-1 = -3A$, so $A = \frac13$. Put $x=2$:
$5 = 3B$, so $B = \frac53$. Therefore

$$ \int\frac{2x+1}{(x+1)(x-2)}dx = \frac13\ln|x+1| + \frac53\ln|x-2| + C $$

**4.** Write $I = \int_{0}^{\pi/2}\frac{dx}{1+\tan x}
= \int_{0}^{\pi/2}\frac{\cos x\,dx}{\cos x+\sin x}$. By P4, replacing $x$ by
$\frac{\pi}{2}-x$ swaps $\sin$ and $\cos$:

$$ I = \int_{0}^{\pi/2}\frac{\sin x\,dx}{\sin x+\cos x} $$

Adding the two forms, $2I = \int_{0}^{\pi/2}1\,dx = \frac{\pi}{2}$, so
$I = \frac{\pi}{4}$.

**5.** With $t=\tan\frac x2$ we have $\sin x = \frac{2t}{1+t^{2}}$ and
$dx = \frac{2\,dt}{1+t^{2}}$, so

$$ 1+\sin x = \frac{1+t^{2}+2t}{1+t^{2}} = \frac{(1+t)^{2}}{1+t^{2}} $$

$$ \int\frac{dx}{1+\sin x} = \int\frac{2\,dt}{1+t^{2}}\cdot\frac{1+t^{2}}{(1+t)^{2}}
= 2\int\frac{dt}{(1+t)^{2}} = -\frac{2}{1+t} + C $$

$$ = -\frac{2}{1+\tan\frac{x}{2}} + C $$

**6.** The curves meet where $x = x^{3}$, i.e. $x\left(x^{2}-1\right)=0$, so in
the first quadrant $x=0$ and $x=1$. On $(0,1)$, $x > x^{3}$ (at $x=\frac12$,
$\frac12 > \frac18$), so the line is above:

$$ A = \int_{0}^{1}\left(x-x^{3}\right)dx
= \left[\frac{x^{2}}{2}-\frac{x^{4}}{4}\right]_{0}^{1} = \frac12-\frac14
= \frac{1}{4}\text{ square units} $$
:::

**Group C — Long answer (8 marks each)**

1. Prove that $\int\dfrac{dx}{\sqrt{x^{2}-a^{2}}}
   = \ln\left|x+\sqrt{x^{2}-a^{2}}\right|+C$ by a suitable trigonometric
   substitution, and hence evaluate $\int_{3}^{5}\dfrac{dx}{\sqrt{x^{2}-9}}$. <span class="marks">[8]</span>
2. (a) Define the definite integral as the limit of a sum and use the definition
   to evaluate $\int_{0}^{1}\left(x^{2}+x\right)dx$. (b) State the property
   $\int_{0}^{a}f(x)\,dx = \int_{0}^{a}f(a-x)\,dx$ and use it to evaluate
   $\int_{0}^{\pi/2}\sin^{2}x\,dx$. <span class="marks">[8]</span>
3. (a) Find the area of the region bounded by the parabola $y^{2}=8x$ and its
   latus rectum $x=2$. (b) Find the area enclosed between the parabola
   $y=x^{2}$ and the line $y=x+2$. <span class="marks">[8]</span>

::: note Answers to Group C
**1.** Put $x = a\sec\theta$. Then $dx = a\sec\theta\tan\theta\,d\theta$ and

$$ \sqrt{x^{2}-a^{2}} = \sqrt{a^{2}\left(\sec^{2}\theta-1\right)}
= a\tan\theta $$

so

$$ \int\frac{dx}{\sqrt{x^{2}-a^{2}}}
= \int\frac{a\sec\theta\tan\theta\,d\theta}{a\tan\theta}
= \int\sec\theta\,d\theta = \ln\left|\sec\theta+\tan\theta\right| + C_{1} $$

From the reference triangle, $\sec\theta = \frac xa$ and
$\tan\theta = \frac{\sqrt{x^{2}-a^{2}}}{a}$, so

$$ = \ln\left|\frac{x+\sqrt{x^{2}-a^{2}}}{a}\right| + C_{1}
= \ln\left|x+\sqrt{x^{2}-a^{2}}\right| + C $$

since $-\ln a$ is absorbed into the constant. With $a=3$,

$$ \int_{3}^{5}\frac{dx}{\sqrt{x^{2}-9}}
= \left[\ln\left|x+\sqrt{x^{2}-9}\right|\right]_{3}^{5}
= \ln(5+4) - \ln 3 = \ln\frac93 = \ln 3 $$

**2. (a)** Divide $[a,b]$ into $n$ equal parts of width $h=\frac{b-a}{n}$ and
define

$$ \int_{a}^{b}f(x)\,dx
= \lim_{n\to\infty}\frac{b-a}{n}\sum_{r=1}^{n}f\left(a+\frac{r(b-a)}{n}\right) $$

Here $a=0$, $b=1$, $h=\frac1n$ and
$f\left(\frac rn\right) = \frac{r^{2}}{n^{2}}+\frac rn$, so

$$ S_{n} = \frac1n\sum_{r=1}^{n}\left(\frac{r^{2}}{n^{2}}+\frac{r}{n}\right)
= \frac{1}{n^{3}}\cdot\frac{n(n+1)(2n+1)}{6} + \frac{1}{n^{2}}\cdot\frac{n(n+1)}{2} $$

$$ = \frac{1}{6}\left(2+\frac3n+\frac{1}{n^{2}}\right)
+ \frac12\left(1+\frac1n\right) $$

Letting $n\to\infty$ gives $\frac{2}{6}+\frac12 = \frac13+\frac12 = \frac{5}{6}$,
which agrees with $\left[\frac{x^{3}}{3}+\frac{x^{2}}{2}\right]_{0}^{1}$.

**(b)** Substituting $x = a-t$ in $\int_{0}^{a}f(x)\,dx$ gives $dx = -dt$ with
limits reversed, so $\int_{0}^{a}f(x)\,dx = \int_{0}^{a}f(a-t)\,dt$, which is the
stated property. Taking $a=\frac{\pi}{2}$ and $f(x)=\sin^{2}x$, and using
$\sin\left(\frac{\pi}{2}-x\right)=\cos x$,

$$ I = \int_{0}^{\pi/2}\sin^{2}x\,dx = \int_{0}^{\pi/2}\cos^{2}x\,dx $$

Adding, $2I = \int_{0}^{\pi/2}\left(\sin^{2}x+\cos^{2}x\right)dx
= \int_{0}^{\pi/2}1\,dx = \frac{\pi}{2}$, so $I = \frac{\pi}{4}$.

**3. (a)** For $y^{2}=8x$ we have $4a = 8$, so $a = 2$ and the latus rectum is
$x = 2$. The curve is symmetric about the $x$-axis, so the area is twice the part
above it, where $y = \sqrt{8x} = 2\sqrt{2}\,\sqrt{x}$:

$$ A = 2\int_{0}^{2}2\sqrt{2}\,\sqrt{x}\,dx
= 4\sqrt{2}\left[\frac{2x^{3/2}}{3}\right]_{0}^{2}
= \frac{8\sqrt{2}}{3}\cdot 2\sqrt{2} = \frac{32}{3}\text{ square units} $$

**(b)** The curves meet where $x^{2} = x+2$, i.e. $x^{2}-x-2 = 0$, giving
$(x-2)(x+1)=0$, so $x=-1$ and $x=2$. Between them the line is above (at $x=0$ it
gives $2$ against $0$), so

$$ A = \int_{-1}^{2}\left(x+2-x^{2}\right)dx
= \left[\frac{x^{2}}{2}+2x-\frac{x^{3}}{3}\right]_{-1}^{2} $$

$$ = \left(2+4-\frac83\right) - \left(\frac12-2+\frac13\right)
= \frac{10}{3} + \frac76 = \frac{27}{6} = \frac{9}{2}\text{ square units} $$
:::
