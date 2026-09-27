---
subject: Mathematics
grade: 12
unit: 14
title: Differential Equations
hours: 12
area: Calculus
---

A **differential equation** is an equation that contains a derivative. It does
not tell you what $y$ is — it tells you how $y$ changes, and you have to
integrate to recover $y$ itself. Almost every law of nature is written this way:
Newton's second law, radioactive decay, the cooling of a cup of tea, the growth
of a population. This unit takes the integration machinery of Unit 13 and points
it at those laws.

::: key What the exam asks
**(1)** Write down the order and degree of a given equation, and form a
differential equation from a family of curves — short, and almost free marks.
**(2)** Solve a first-order first-degree equation. Everything turns on
*identifying the type*: separable, homogeneous, linear or exact. **(3)** A Group
C question combining a solution with an initial condition, or an application to
growth, decay or cooling. The four-line identification checklist in §14.2 is the
single most valuable thing in this chapter.
:::

## 14.1 Order and degree of a differential equation

::: definition Differential equation, order and degree
A **differential equation** is an equation involving an independent variable
$x$, a dependent variable $y$, and one or more derivatives of $y$ with respect
to $x$.

The **order** is the order of the *highest* derivative that appears.

The **degree** is the power of that highest derivative, after the equation has
been made free of radicals and fractional powers of the derivatives, and is
written as a polynomial in the derivatives.
:::

An equation in one independent variable is called **ordinary**. If it contains
partial derivatives such as $\frac{\partial z}{\partial x}$ it is a **partial**
differential equation, which is beyond this syllabus. Every equation in this
chapter is ordinary.

::: caution Clear the radicals *before* reading off the degree
The degree is defined only for an equation that is polynomial in the
derivatives. So
$$ \frac{dy}{dx} = \sqrt{1+\frac{d^{2}y}{dx^{2}}} $$
does not have degree $\frac12$. Square both sides first:
$\left(\frac{dy}{dx}\right)^{2} = 1 + \frac{d^{2}y}{dx^{2}}$, which is order $2$
and degree $1$. If no amount of algebra removes the radical — for instance
$\sin\frac{dy}{dx} = x$ — the degree is **not defined**.
:::

::: example Worked example 14.1
**Problem.** State the order and degree of each equation.

(a) $\dfrac{dy}{dx} + 3y = e^{x}$
(b) $\dfrac{d^{2}y}{dx^{2}} + 5\left(\dfrac{dy}{dx}\right)^{3} - 4y = 0$
(c) $\left(\dfrac{d^{3}y}{dx^{3}}\right)^{2} + \dfrac{dy}{dx} = \sin x$
(d) $\dfrac{d^{2}y}{dx^{2}} = \sqrt{1+\left(\dfrac{dy}{dx}\right)^{2}}$

**Solution.**

**(a)** The highest derivative is $\frac{dy}{dx}$, appearing to the first power.
**Order 1, degree 1.**

**(b)** The highest derivative is $\frac{d^{2}y}{dx^{2}}$, to the first power.
The cube belongs to a *lower* derivative and does not affect the degree.
**Order 2, degree 1.**

**(c)** Highest derivative $\frac{d^{3}y}{dx^{3}}$, squared. **Order 3, degree 2.**

**(d)** Squaring gives
$\left(\frac{d^{2}y}{dx^{2}}\right)^{2} = 1+\left(\frac{dy}{dx}\right)^{2}$, so
the highest derivative is of order $2$ and now appears squared.
**Order 2, degree 2.**
:::

::: example Worked example 14.2
**Problem.** State the order and degree of
(a) $x\left(\dfrac{d^{2}y}{dx^{2}}\right)^{3} + y\left(\dfrac{dy}{dx}\right)^{4} + y^{5} = 0$,
(b) $\dfrac{d^{2}y}{dx^{2}} + \sin\left(\dfrac{dy}{dx}\right) = 0$,
(c) $\left(\dfrac{dy}{dx}\right)^{3} - 4\dfrac{dy}{dx} + y = 0$.

**Solution.**

**(a)** Highest derivative: order $2$, and it is cubed. **Order 2, degree 3.**
The powers $4$ and $5$ are irrelevant to both answers.

**(b)** The highest derivative is of order $2$ and appears to the first power, so
the **order is 2**. But the equation is not polynomial in $\frac{dy}{dx}$ —
$\sin$ of a derivative cannot be cleared — so the **degree is not defined**.

**(c)** Order $1$, and the first derivative is cubed. **Order 1, degree 3.**
Notice that order and degree are quite independent of each other.
:::

::: definition Solution of a differential equation
A **solution** (or primitive) is any relation between $x$ and $y$, free of
derivatives, that satisfies the equation.

The **general solution** of an $n$-th order equation contains $n$ arbitrary
constants. A **particular solution** is obtained by using extra information —
initial or boundary conditions — to fix those constants.
:::

## 14.2 Differential equations of first order and first degree

The whole of the rest of this chapter is about the single type

$$ \frac{dy}{dx} = f(x,y), \qquad \text{equivalently} \qquad
M(x,y)\,dx + N(x,y)\,dy = 0 $$

Its general solution contains exactly **one** arbitrary constant, so it is a
one-parameter family of curves. That family is the right mental picture, and the
**slope field** draws it: at each point of the plane, draw a short segment whose
gradient is $f(x,y)$. Any curve that stays tangent to those segments is a
solution.

```figure caption="The slope field of $\frac{dy}{dx} = x - y$. Every short segment has gradient $x-y$ at that point, and the four coloured curves $y = x-1+Ce^{-x}$ thread through them — one curve for each value of $C$. The general solution is the whole family, not a single curve."
import numpy as np
fig, ax = plt.subplots(figsize=(5.0,3.2))
X, Y = np.meshgrid(np.linspace(-2, 4, 19), np.linspace(-3, 5, 17))
S = X - Y
L = 0.26
den = np.sqrt(1 + S**2)
U, V = L/den, L*S/den
ax.quiver(X, Y, U, V, angles='xy', scale_units='xy', scale=1, color=MUTED,
          width=0.0032, headwidth=0, headlength=0, headaxislength=0, pivot='mid')
xs = np.linspace(-2, 4, 400)
for C, c in zip([-3, -1, 1, 3], SERIES):
    ax.plot(xs, xs - 1 + C*np.exp(-xs), color=c, lw=1.6)
ax.plot(xs, xs - 1, color=INK, lw=1.3, ls='--')
ax.annotate('$C=0$:  $y = x-1$', (3.1, 2.1), (-1.95, 3.15), fontsize=8.8, color=INK,
            arrowprops=dict(arrowstyle='->', color=INK, lw=0.8))
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.set_xlim(-2.15, 4.15); ax.set_ylim(-3.2, 5.2)
ax.set_title('$\\frac{dy}{dx} = x - y$   and   $y = x - 1 + Ce^{-x}$', fontsize=9.4)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.32)
```

One extra condition picks out one member of the family. Geometrically, you
nominate a single point and follow the field through it.

```figure caption="The same field with the condition $y(0)=2$. Only one curve of the family passes through $(0,2)$: putting $x=0$, $y=2$ into $y = x-1+Ce^{-x}$ gives $2 = -1 + C$, so $C = 3$ and the particular solution is $y = x-1+3e^{-x}$."
import numpy as np
fig, ax = plt.subplots(figsize=(5.0,3.0))
X, Y = np.meshgrid(np.linspace(-2, 4, 19), np.linspace(-3, 5, 17))
S = X - Y
L = 0.26
den = np.sqrt(1 + S**2)
ax.quiver(X, Y, L/den, L*S/den, angles='xy', scale_units='xy', scale=1,
          color='#c3c9d3', width=0.0032, headwidth=0, headlength=0,
          headaxislength=0, pivot='mid')
xs = np.linspace(-2, 4, 400)
for C in [-3, -1, 0, 1, 2, 4, 5]:
    ax.plot(xs, xs - 1 + C*np.exp(-xs), color='#c3c9d3', lw=1.1)
ax.plot(xs, xs - 1 + 3*np.exp(-xs), color='#d9534f', lw=2.2)
ax.plot([0], [2], 'o', color=INK, ms=5.5, zorder=5)
ax.annotate('$(0, 2)$', (0, 2), textcoords='offset points', xytext=(8, 4),
            fontsize=9.4, color=INK)
ax.annotate('$y = x-1+3e^{-x}$', (1.35, 1.14), (1.65, -2.35), fontsize=9.2,
            color='#9c3531', arrowprops=dict(arrowstyle='->', color='#9c3531', lw=0.9))
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.set_xlim(-2.15, 4.15); ax.set_ylim(-3.2, 5.2)
ax.set_title('One initial condition $y(0)=2$ selects one curve', fontsize=9.4)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.32)
```

::: key Identify the type in this order
| Test | Type | Method |
|---|---|---|
| can you write it as $f(y)\,dy = g(x)\,dx$ | **separable** | integrate both sides |
| is every term of the same total degree in $x$ and $y$ | **homogeneous** | put $y = vx$ |
| does it look homogeneous apart from constants | **reducible** | shift the origin |
| is it $\dfrac{dy}{dx} + Py = Q$ with $P,Q$ functions of $x$ | **linear** | integrating factor $e^{\int P\,dx}$ |
| is $M\,dx + N\,dy = 0$ with $\dfrac{\partial M}{\partial y} = \dfrac{\partial N}{\partial x}$ | **exact** | integrate $M$ with respect to $x$ |

Work down the list and stop at the first match. Separable is cheapest, so always
test it first — many equations that look homogeneous or linear separate at once.
:::

### Formation of a differential equation

The reverse problem also appears in the examination: given a family of curves
with $n$ arbitrary constants, produce the differential equation it satisfies.
The recipe is to **differentiate $n$ times and eliminate the constants**.

::: example Worked example 14.3
**Problem.** Form the differential equation of (a) the family of straight lines
$y = mx$ through the origin, (b) the family of circles $x^{2}+y^{2} = a^{2}$
centred at the origin, (c) the family $y = Ae^{2x}$.

**Solution.** Each family has one constant, so differentiate once.

**(a)** $y = mx$ gives $\frac{dy}{dx} = m$. From the original equation
$m = \frac{y}{x}$, so eliminating $m$,

$$ \frac{dy}{dx} = \frac{y}{x} $$

**(b)** Differentiating $x^{2}+y^{2}=a^{2}$ with respect to $x$:
$2x + 2y\frac{dy}{dx} = 0$, and $a$ has already vanished, so

$$ \frac{dy}{dx} = -\frac{x}{y} $$

This is the equation whose slope field is drawn in §14.3 — the circles are
everywhere perpendicular to the radius, which is exactly what
$\frac{dy}{dx} = -\frac{x}{y}$ says.

**(c)** $\frac{dy}{dx} = 2Ae^{2x} = 2y$, so

$$ \frac{dy}{dx} - 2y = 0 $$
:::

::: example Worked example 14.4
**Problem.** Verify that $y = x - 1 + Ce^{-x}$ is the general solution of
$\dfrac{dy}{dx} + y = x$, and find the solution with $y(0) = 2$.

**Solution.** **Verification.** Differentiate:
$\frac{dy}{dx} = 1 - Ce^{-x}$. Add $y$:

$$ \frac{dy}{dx} + y = \left(1 - Ce^{-x}\right) + \left(x - 1 + Ce^{-x}\right) = x $$

The $Ce^{-x}$ terms cancel for *every* $C$, so the whole family satisfies the
equation, which is what "general solution" means.

**Particular solution.** Put $x=0$ and $y=2$ into $y = x-1+Ce^{-x}$:

$$ 2 = 0 - 1 + C \quad\Longrightarrow\quad C = 3 $$

$$ y = x - 1 + 3e^{-x} $$

That is the red curve in the second figure. Always substitute the condition into
the *general solution*, never into the differential equation.
:::

## 14.3 Separable variables

::: definition Variables separable
A first-order equation is **separable** if it can be written with all the $y$
terms (including $dy$) on one side and all the $x$ terms (including $dx$) on the
other:

$$ f(y)\,dy = g(x)\,dx $$

Integrating both sides gives the general solution

$$ \int f(y)\,dy = \int g(x)\,dx + C $$

One constant is enough: the two constants of integration combine into one.
:::

The test is whether $\frac{dy}{dx}$ **factorises** into a function of $x$ times a
function of $y$. If $\frac{dy}{dx} = h(x)\,k(y)$ then
$\frac{dy}{k(y)} = h(x)\,dx$ and you are done. Equations such as
$\frac{dy}{dx} = x+y$ do not factorise and are not separable.

```figure caption="The slope field of $\frac{dy}{dx} = -\frac{x}{y}$, which separates as $y\,dy = -x\,dx$ and integrates to $x^2+y^2 = c$. The solution family is the concentric circles, each cutting every radius at right angles."
import numpy as np
fig, ax = plt.subplots(figsize=(4.4,3.2))
X, Y = np.meshgrid(np.linspace(-3, 3, 17), np.linspace(-3, 3, 17))
with np.errstate(divide='ignore', invalid='ignore'):
    S = -X/Y
L = 0.30
den = np.sqrt(1 + S**2)
U, V = L/den, L*S/den
m = np.abs(Y) > 1e-9
ax.quiver(X[m], Y[m], U[m], V[m], angles='xy', scale_units='xy', scale=1,
          color=MUTED, width=0.004, headwidth=0, headlength=0,
          headaxislength=0, pivot='mid')
t = np.linspace(0, 2*np.pi, 400)
for r, c in zip([0.8, 1.5, 2.2, 2.9], SERIES):
    ax.plot(r*np.cos(t), r*np.sin(t), color=c, lw=1.6)
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.set_xlim(-3.3, 3.3); ax.set_ylim(-3.3, 3.3)
ax.set_aspect('equal')
ax.set_title('$\\frac{dy}{dx} = -\\frac{x}{y}$ :  $x^2+y^2 = c$', fontsize=9.4)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.30)
```

::: example Worked example 14.5
**Problem.** Solve $\left(1+x^{2}\right)\dfrac{dy}{dx} = 1+y^{2}$.

**Solution.** Separate, putting everything in $y$ on the left:

$$ \frac{dy}{1+y^{2}} = \frac{dx}{1+x^{2}} $$

Integrate both sides, using the standard form
$\int\frac{dt}{1+t^{2}} = \tan^{-1}t$:

$$ \tan^{-1}y = \tan^{-1}x + C $$

That is the general solution. It can also be written
$\tan^{-1}y - \tan^{-1}x = C$, or, taking the tangent of both sides and using
the subtraction formula, $\frac{y-x}{1+xy} = k$ — a family of circles.

**Check.** Differentiating $\tan^{-1}y - \tan^{-1}x = C$ gives
$\frac{1}{1+y^{2}}\frac{dy}{dx} - \frac{1}{1+x^{2}} = 0$, which rearranges to the
original equation.
:::

::: example Worked example 14.6
**Problem.** Solve $\dfrac{dy}{dx} = e^{x-y}$.

**Solution.** The exponential *factorises*, which is what makes this separable:

$$ \frac{dy}{dx} = e^{x}e^{-y} \quad\Longrightarrow\quad e^{y}\,dy = e^{x}\,dx $$

Integrating both sides,

$$ e^{y} = e^{x} + C $$

or $y = \ln\left(e^{x}+C\right)$. Note that $e^{x-y}$ had to be split before the
variables could be separated — always look for a hidden product.
:::

::: example Worked example 14.7
**Problem.** Solve $\sec^{2}x\tan y\,dx + \sec^{2}y\tan x\,dy = 0$.

**Solution.** Divide throughout by $\tan x\tan y$, which separates the variables:

$$ \frac{\sec^{2}x}{\tan x}\,dx + \frac{\sec^{2}y}{\tan y}\,dy = 0 $$

Each term is now $\frac{g'}{g}$, since $\frac{d}{dx}\tan x = \sec^{2}x$:

$$ \ln|\tan x| + \ln|\tan y| = \ln|c| $$

Combining the logarithms and removing them,

$$ \tan x\tan y = c $$

Writing the constant as $\ln|c|$ rather than $C$ at the start is a standard trick
whenever the answer is going to be a product.
:::

::: example Worked example 14.8
**Problem.** Solve $x\left(1+y^{2}\right)dx = y\left(1+x^{2}\right)dy$ and find
the particular solution through $(0,1)$.

**Solution.** Divide both sides by $\left(1+x^{2}\right)\left(1+y^{2}\right)$:

$$ \frac{x\,dx}{1+x^{2}} = \frac{y\,dy}{1+y^{2}} $$

Both sides are $\frac{g'}{2g}$ patterns, so integrating gives

$$ \frac12\ln\left(1+x^{2}\right) = \frac12\ln\left(1+y^{2}\right) + \frac12\ln c $$

Multiply by $2$ and remove the logarithms:

$$ 1+x^{2} = c\left(1+y^{2}\right) $$

**Particular solution.** Put $x=0$, $y=1$: $\;1 = c(2)$, so $c = \frac12$, giving
$2\left(1+x^{2}\right) = 1+y^{2}$, that is $y^{2} = 2x^{2}+1$.
:::

::: example Worked example 14.9
**Problem.** Solve $x\dfrac{dy}{dx} = y(x-1)$.

**Solution.** Separate:

$$ \frac{dy}{y} = \frac{x-1}{x}\,dx = \left(1 - \frac1x\right)dx $$

Integrate both sides:

$$ \ln|y| = x - \ln|x| + \ln|C| $$

Collect the logarithms: $\ln|y| + \ln|x| = x + \ln|C|$, so $\ln|xy| - \ln|C| = x$
and therefore

$$ xy = Ce^{x}, \qquad\text{that is}\qquad y = \frac{Ce^{x}}{x} $$

**Check.** $\frac{dy}{dx} = \frac{Ce^{x}(x-1)}{x^{2}} = \frac{y(x-1)}{x}$, as
required.
:::

::: caution Do not lose the constant, and do not lose solutions
Two habits to keep. First, add the constant **at the moment you integrate**, not
at the end — half of all lost marks in this chapter are a missing $C$. Second,
when you divide by something like $\tan y$ or $y$, you are assuming it is not
zero. The constant solution $y = 0$ often satisfies the equation as well, and a
careful answer mentions it.
:::

## 14.4 Homogeneous differential equations

::: definition Homogeneous function and homogeneous equation
A function $f(x,y)$ is **homogeneous of degree $n$** if
$f(tx,ty) = t^{n}f(x,y)$ for every $t$. In practice: every term has the same
total degree in $x$ and $y$. So $x^{2}+xy+y^{2}$ is homogeneous of degree $2$,
and $x^{2}+y$ is not homogeneous at all.

The equation $M(x,y)\,dx + N(x,y)\,dy = 0$ is **homogeneous** if $M$ and $N$ are
homogeneous of the *same* degree. Equivalently

$$ \frac{dy}{dx} = F\left(\frac{y}{x}\right) $$

the right side depending on $x$ and $y$ only through the ratio $\frac{y}{x}$.
:::

::: derivation Why the substitution $y = vx$ works
Suppose $\frac{dy}{dx} = F\left(\frac yx\right)$. Put $y = vx$, where $v$ is a new
function of $x$. By the product rule,

$$ \frac{dy}{dx} = v + x\frac{dv}{dx} $$

Substituting into the equation gives

$$ v + x\frac{dv}{dx} = F(v) \quad\Longrightarrow\quad
x\frac{dv}{dx} = F(v) - v $$

and this **always separates**:

$$ \frac{dv}{F(v)-v} = \frac{dx}{x} $$

Integrate, then replace $v$ by $\frac yx$. If the equation is easier the other way
round, the substitution $x = vy$ works identically.
:::

::: example Worked example 14.10
**Problem.** Solve $\dfrac{dy}{dx} = \dfrac{x^{2}+y^{2}}{2xy}$.

**Solution.** Numerator and denominator are both homogeneous of degree $2$, so
put $y = vx$, $\frac{dy}{dx} = v + x\frac{dv}{dx}$:

$$ v + x\frac{dv}{dx} = \frac{x^{2}+v^{2}x^{2}}{2x \cdot vx} = \frac{1+v^{2}}{2v} $$

$$ x\frac{dv}{dx} = \frac{1+v^{2}}{2v} - v = \frac{1+v^{2}-2v^{2}}{2v}
= \frac{1-v^{2}}{2v} $$

Separate the variables:

$$ \frac{2v\,dv}{1-v^{2}} = \frac{dx}{x} $$

The left side is $-\frac{g'}{g}$ with $g = 1-v^{2}$, so integrating gives

$$ -\ln\left|1-v^{2}\right| = \ln|x| - \ln|C| $$

$$ \ln\left|x\left(1-v^{2}\right)\right| = \ln|C|
\quad\Longrightarrow\quad x\left(1-v^{2}\right) = C $$

Finally put $v = \frac yx$:

$$ x\left(1 - \frac{y^{2}}{x^{2}}\right) = C \quad\Longrightarrow\quad
x^{2} - y^{2} = Cx $$

**Check.** Differentiating $x^{2}-y^{2}=Cx$ gives
$2x - 2y\frac{dy}{dx} = C = \frac{x^{2}-y^{2}}{x}$, and solving for
$\frac{dy}{dx}$ returns $\frac{x^{2}+y^{2}}{2xy}$.
:::

```figure caption="The solution family $x^2 - y^2 = Cx$ of $\frac{dy}{dx}=\frac{x^2+y^2}{2xy}$, drawn for $C = 0.6, 1.2, 2.0, 3.0, 4.2$. The dotted rays $y = vx$ are the lines along which $v$ is constant — that is the geometric reason the substitution $y = vx$ works for a homogeneous equation."
import numpy as np
fig, ax = plt.subplots(figsize=(4.7,3.0))
x = np.linspace(0.01, 6, 700)
for C, c in zip([0.6, 1.2, 2.0, 3.0, 4.2], SERIES):
    v = x**2 - C*x
    y = np.sqrt(np.clip(v, 0, None))
    y[v < 0] = np.nan
    ax.plot(x, y, color=c, lw=1.6)
    ax.plot(x, -y, color=c, lw=1.6)
for k in [0.55, 1.0, 1.9]:
    ax.plot(x, k*x, color=MUTED, lw=0.8, ls=':')
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.set_xlim(0, 6.1); ax.set_ylim(-3.6, 3.6)
ax.axhline(0, color=MUTED, lw=0.7)
ax.set_title('$x^2 - y^2 = Cx$, the solutions of $\\frac{dy}{dx}=\\frac{x^2+y^2}{2xy}$',
             fontsize=9.2)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.32)
```

::: example Worked example 14.11
**Problem.** Solve $\dfrac{dy}{dx} = \dfrac{x-y}{x+y}$.

**Solution.** Both parts are homogeneous of degree $1$. Put $y = vx$:

$$ v + x\frac{dv}{dx} = \frac{x - vx}{x + vx} = \frac{1-v}{1+v} $$

$$ x\frac{dv}{dx} = \frac{1-v}{1+v} - v = \frac{1-v-v-v^{2}}{1+v}
= \frac{1-2v-v^{2}}{1+v} $$

Separating,

$$ \frac{(1+v)\,dv}{1-2v-v^{2}} = \frac{dx}{x} $$

The derivative of $1-2v-v^{2}$ is $-2-2v = -2(1+v)$, so the left side is
$-\frac{1}{2}\cdot\frac{g'}{g}$:

$$ -\frac12\ln\left|1-2v-v^{2}\right| = \ln|x| - \frac12\ln|C| $$

Multiply by $-2$ and combine:

$$ \ln\left|1-2v-v^{2}\right| + \ln\left|x^{2}\right| = \ln|C|
\quad\Longrightarrow\quad x^{2}\left(1-2v-v^{2}\right) = C $$

With $v = \frac yx$ this is

$$ x^{2} - 2xy - y^{2} = C $$
:::

::: example Worked example 14.12
**Problem.** Solve $x\dfrac{dy}{dx} = y + x\tan\dfrac{y}{x}$.

**Solution.** Divide through by $x$ to expose the ratio:

$$ \frac{dy}{dx} = \frac yx + \tan\frac yx $$

Put $y = vx$:

$$ v + x\frac{dv}{dx} = v + \tan v \quad\Longrightarrow\quad
x\frac{dv}{dx} = \tan v $$

The $v$ terms cancel, which always happens when the equation has this shape:

$$ \cot v\,dv = \frac{dx}{x} \quad\Longrightarrow\quad
\ln|\sin v| = \ln|x| + \ln|C| $$

$$ \sin v = Cx \quad\Longrightarrow\quad \sin\frac{y}{x} = Cx $$
:::

### Equations reducible to homogeneous form

An equation

$$ \frac{dy}{dx} = \frac{a_{1}x + b_{1}y + c_{1}}{a_{2}x + b_{2}y + c_{2}} $$

fails to be homogeneous only because of the constants $c_{1}$ and $c_{2}$. Shift
the origin to the point where both numerator and denominator vanish: put
$x = X + h$ and $y = Y + k$, choose $h$ and $k$ to kill the constants, and note
that $\frac{dy}{dx} = \frac{dY}{dX}$ because the shift does not change the
gradient. The result is homogeneous in $X$ and $Y$.

::: example Worked example 14.13
**Problem.** Solve $\dfrac{dy}{dx} = \dfrac{x+2y-3}{2x+y-3}$.

**Solution.** **Step 1 — find the shift.** Solve
$x+2y-3 = 0$ and $2x+y-3 = 0$ simultaneously. Subtracting gives $y = x$, and
then $3x = 3$, so $x = 1$, $y = 1$. Put

$$ x = X+1, \qquad y = Y+1, \qquad \frac{dy}{dx} = \frac{dY}{dX} $$

**Step 2 — the equation is now homogeneous.**

$$ \frac{dY}{dX} = \frac{(X+1)+2(Y+1)-3}{2(X+1)+(Y+1)-3} = \frac{X+2Y}{2X+Y} $$

**Step 3 — put $Y = vX$.**

$$ v + X\frac{dv}{dX} = \frac{1+2v}{2+v} \quad\Longrightarrow\quad
X\frac{dv}{dX} = \frac{1+2v-2v-v^{2}}{2+v} = \frac{1-v^{2}}{2+v} $$

**Step 4 — separate and integrate.**

$$ \frac{(2+v)\,dv}{(1-v)(1+v)} = \frac{dX}{X} $$

Partial fractions: $\frac{2+v}{(1-v)(1+v)} = \frac{A}{1-v} + \frac{B}{1+v}$ gives
$2+v = A(1+v) + B(1-v)$. Put $v=1$: $3 = 2A$, so $A = \frac32$. Put $v=-1$:
$1 = 2B$, so $B = \frac12$. Hence

$$ -\frac32\ln|1-v| + \frac12\ln|1+v| = \ln|X| + \text{constant} $$

Multiply by $2$ and collect:

$$ \ln\frac{|1+v|}{|1-v|^{3}} = \ln\left|X^{2}\right| + \ln|C'| $$

$$ \frac{1+v}{(1-v)^{3}} = C'X^{2} $$

**Step 5 — go back.** With $v = \frac YX$, the left side is
$\frac{(X+Y)X^{2}}{(X-Y)^{3}}$, so the $X^{2}$ cancels and

$$ X+Y = C(X-Y)^{3} $$

Finally $X = x-1$ and $Y = y-1$, so $X+Y = x+y-2$ and $X-Y = x-y$:

$$ x+y-2 = C(x-y)^{3} $$
:::

## 14.5 Linear differential equations

::: definition Linear equation of the first order
An equation is **linear of the first order** if it can be written

$$ \frac{dy}{dx} + P(x)\,y = Q(x) $$

where $P$ and $Q$ are functions of $x$ alone. "Linear" means $y$ and
$\frac{dy}{dx}$ appear only to the first power, and never multiplied together.
:::

::: derivation The integrating factor
Multiply the equation by an unknown positive function $I(x)$:

$$ I\frac{dy}{dx} + IPy = IQ $$

We would like the left side to be the exact derivative of $Iy$. Since

$$ \frac{d}{dx}(Iy) = I\frac{dy}{dx} + \frac{dI}{dx}y $$

the two agree provided $\frac{dI}{dx} = IP$. That is a separable equation:

$$ \frac{dI}{I} = P\,dx \quad\Longrightarrow\quad \ln I = \int P\,dx
\quad\Longrightarrow\quad I = e^{\int P\,dx} $$

This $I$ is the **integrating factor**. With it, the equation becomes

$$ \frac{d}{dx}\left(Iy\right) = IQ $$

and integrating both sides gives the general solution

$$ y \cdot e^{\int P\,dx} = \int Q\,e^{\int P\,dx}\,dx + C $$
:::

::: memory Three steps, every time
1. Force the equation into the form $\frac{dy}{dx} + Py = Q$ — divide by whatever
   multiplies $\frac{dy}{dx}$.
2. Compute $I = e^{\int P\,dx}$. No constant is needed here, and if
   $\int P\,dx = \ln f(x)$ then $I = f(x)$ straight away.
3. Write $Iy = \int IQ\,dx + C$ and finish the integral.
:::

::: example Worked example 14.14
**Problem.** Solve $x\dfrac{dy}{dx} + 2y = x^{3}$.

**Solution.** **Step 1.** Divide by $x$ to reach standard form:

$$ \frac{dy}{dx} + \frac{2}{x}y = x^{2}, \qquad\text{so } P = \frac2x, \; Q = x^{2} $$

**Step 2.** $\int P\,dx = \int\frac{2}{x}dx = 2\ln x = \ln x^{2}$, so

$$ I = e^{\ln x^{2}} = x^{2} $$

**Step 3.**

$$ \frac{d}{dx}\left(x^{2}y\right) = x^{2} \cdot x^{2} = x^{4}
\quad\Longrightarrow\quad x^{2}y = \frac{x^{5}}{5} + C $$

$$ y = \frac{x^{3}}{5} + \frac{C}{x^{2}} $$

**Check.** $\frac{dy}{dx} = \frac{3x^{2}}{5} - \frac{2C}{x^{3}}$, so
$x\frac{dy}{dx} + 2y = \frac{3x^{3}}{5} - \frac{2C}{x^{2}} + \frac{2x^{3}}{5}
+ \frac{2C}{x^{2}} = x^{3}$. Correct for every $C$.
:::

::: example Worked example 14.15
**Problem.** Solve $\dfrac{dy}{dx} + y\cot x = 2\cos x$.

**Solution.** Already in standard form with $P = \cot x$ and $Q = 2\cos x$.

$$ \int \cot x\,dx = \ln|\sin x| \quad\Longrightarrow\quad I = \sin x $$

Multiplying through,

$$ \frac{d}{dx}\left(y\sin x\right) = 2\sin x\cos x $$

The right side is the derivative of $\sin^{2}x$, so

$$ y\sin x = \sin^{2}x + C \quad\Longrightarrow\quad
y = \sin x + C\csc x $$

where $\csc x$ is the cosecant. Equations with $\cot x$ or $\tan x$ as $P$ always
give a trigonometric integrating factor: $\sin x$ and $\sec x$ respectively.
:::

::: example Worked example 14.16
**Problem.** Solve $\left(1+x^{2}\right)\dfrac{dy}{dx} + 2xy = 4x^{2}$.

**Solution.** Divide by $1+x^{2}$:

$$ \frac{dy}{dx} + \frac{2x}{1+x^{2}}y = \frac{4x^{2}}{1+x^{2}} $$

$$ \int\frac{2x\,dx}{1+x^{2}} = \ln\left(1+x^{2}\right)
\quad\Longrightarrow\quad I = 1+x^{2} $$

Notice that $I$ is exactly the factor we divided by — that is common, and it is
worth spotting, because then the equation was *already* in the form
$\frac{d}{dx}(Iy) = \text{something}$:

$$ \frac{d}{dx}\left[\left(1+x^{2}\right)y\right] = 4x^{2}
\quad\Longrightarrow\quad \left(1+x^{2}\right)y = \frac{4x^{3}}{3} + C $$

$$ y = \frac{4x^{3}+3C}{3\left(1+x^{2}\right)} $$
:::

::: example Worked example 14.17
**Problem.** Solve (a) $\dfrac{dy}{dx} + y = e^{-x}$, (b)
$\dfrac{dy}{dx} - y\tan x = \sec x$, (c) $\dfrac{dy}{dx} + y = e^{x}$ with
$y(0)=1$.

**Solution.** **(a)** $P=1$, so $I = e^{x}$ and

$$ \frac{d}{dx}\left(ye^{x}\right) = e^{x}e^{-x} = 1
\quad\Longrightarrow\quad ye^{x} = x + C
\quad\Longrightarrow\quad y = (x+C)e^{-x} $$

**(b)** $P = -\tan x$, so $\int P\,dx = \ln|\cos x|$ and $I = \cos x$:

$$ \frac{d}{dx}\left(y\cos x\right) = \sec x\cos x = 1
\quad\Longrightarrow\quad y\cos x = x + C
\quad\Longrightarrow\quad y = (x+C)\sec x $$

**(c)** $I = e^{x}$ again, but now $Q = e^{x}$:

$$ \frac{d}{dx}\left(ye^{x}\right) = e^{2x} \quad\Longrightarrow\quad
ye^{x} = \frac{e^{2x}}{2} + C \quad\Longrightarrow\quad
y = \frac{e^{x}}{2} + Ce^{-x} $$

Now apply $y(0) = 1$: $\;1 = \frac12 + C$, so $C = \frac12$ and

$$ y = \frac{e^{x}+e^{-x}}{2} $$
:::

::: caution "Linear" is about $y$, not about $x$
$\frac{dy}{dx} + x^{3}y = \sin x$ is linear — the powers of $x$ do not matter.
But $\frac{dy}{dx} + y^{2} = x$ is **not** linear, and neither is
$y\frac{dy}{dx} = x$. Also, if the roles are reversed and you find $P$ and $Q$
turning out to be functions of $y$, treat $x$ as the dependent variable and use
$\frac{dx}{dy} + P(y)x = Q(y)$ with integrating factor $e^{\int P\,dy}$.
:::

## 14.6 Exact differential equations

::: definition Exact differential equation
The equation

$$ M(x,y)\,dx + N(x,y)\,dy = 0 $$

is **exact** if its left side is the total differential $du$ of some function
$u(x,y)$, that is if $M = \frac{\partial u}{\partial x}$ and
$N = \frac{\partial u}{\partial y}$. The general solution is then simply

$$ u(x,y) = C $$

**Test for exactness.** The equation is exact if and only if

$$ \frac{\partial M}{\partial y} = \frac{\partial N}{\partial x} $$

because both sides then equal the mixed second derivative
$\frac{\partial^{2}u}{\partial x\,\partial y}$.
:::

::: memory How to find $u$
1. Test: differentiate $M$ with respect to $y$ and $N$ with respect to $x$. If
   they disagree, the equation is not exact.
2. Integrate $M$ with respect to $x$, holding $y$ constant. The "constant" of
   integration is an unknown function $g(y)$.
3. Differentiate that result with respect to $y$, set it equal to $N$, and solve
   for $g'(y)$.
4. Integrate $g'(y)$ and write $u(x,y) = C$.

A shortcut that works for every equation in this syllabus: integrate $M\,dx$ and
$N\,dy$, then write down each distinct term **once**.
:::

::: example Worked example 14.18
**Problem.** Solve $\left(3x^{2}+2y\right)dx + \left(2x+3y^{2}\right)dy = 0$.

**Solution.** **Test.** $M = 3x^{2}+2y$ and $N = 2x+3y^{2}$, so

$$ \frac{\partial M}{\partial y} = 2, \qquad \frac{\partial N}{\partial x} = 2 $$

They agree, so the equation is exact.

**Find $u$.** Integrate $M$ with respect to $x$, treating $y$ as a constant:

$$ u = \int\left(3x^{2}+2y\right)dx = x^{3} + 2xy + g(y) $$

Differentiate with respect to $y$ and compare with $N$:

$$ \frac{\partial u}{\partial y} = 2x + g'(y) = 2x + 3y^{2}
\quad\Longrightarrow\quad g'(y) = 3y^{2} \quad\Longrightarrow\quad g(y) = y^{3} $$

**Solution.**

$$ x^{3} + 2xy + y^{3} = C $$

**Check.** The total differential is
$\left(3x^{2}+2y\right)dx + \left(2x+3y^{2}\right)dy = 0$, the original equation.
:::

::: example Worked example 14.19
**Problem.** Solve $\left(2xy+y^{2}\right)dx + \left(x^{2}+2xy\right)dy = 0$.

**Solution.** $\frac{\partial M}{\partial y} = 2x+2y$ and
$\frac{\partial N}{\partial x} = 2x+2y$, so the equation is exact.

$$ u = \int\left(2xy+y^{2}\right)dx = x^{2}y + xy^{2} + g(y) $$

$$ \frac{\partial u}{\partial y} = x^{2} + 2xy + g'(y) = x^{2}+2xy
\quad\Longrightarrow\quad g'(y) = 0 $$

So $g$ is a constant and the solution is

$$ x^{2}y + xy^{2} = C, \qquad\text{that is}\qquad xy(x+y) = C $$
:::

::: example Worked example 14.20
**Problem.** Solve (a) $\left(y\cos x + 1\right)dx + \sin x\,dy = 0$,
(b) $\left(x^{2}+y^{2}\right)dx + 2xy\,dy = 0$.

**Solution.** **(a)** $\frac{\partial M}{\partial y} = \cos x$ and
$\frac{\partial N}{\partial x} = \cos x$, so it is exact.

$$ u = \int\left(y\cos x+1\right)dx = y\sin x + x + g(y) $$

$$ \frac{\partial u}{\partial y} = \sin x + g'(y) = \sin x
\quad\Longrightarrow\quad g'(y) = 0 $$

$$ y\sin x + x = C $$

**(b)** $\frac{\partial M}{\partial y} = 2y$ and
$\frac{\partial N}{\partial x} = 2y$, so it is exact.

$$ u = \int\left(x^{2}+y^{2}\right)dx = \frac{x^{3}}{3} + xy^{2} + g(y) $$

$$ \frac{\partial u}{\partial y} = 2xy + g'(y) = 2xy
\quad\Longrightarrow\quad g'(y) = 0 $$

$$ \frac{x^{3}}{3} + xy^{2} = C, \qquad\text{or}\qquad x^{3} + 3xy^{2} = C' $$

This equation is also homogeneous of degree $2$, so $y = vx$ would solve it as
well — a reminder that the types overlap, and the cheapest applicable method is
the right one.
:::

## 14.7 Applications of differential equations

Every application in this section is the same equation. If a quantity changes at
a rate proportional to its own size, then

$$ \frac{dy}{dt} = ky \quad\Longrightarrow\quad \frac{dy}{y} = k\,dt
\quad\Longrightarrow\quad \ln y = kt + c \quad\Longrightarrow\quad y = y_{0}e^{kt} $$

where $y_{0}$ is the value at $t=0$. A positive $k$ gives **growth**, a negative
$k$ gives **decay**. Two data points are always enough: the first fixes $y_{0}$
and the second fixes $k$.

### Population growth

::: example Worked example 14.21
**Problem.** The population of a municipality grows at a rate proportional to the
population present. It was $40{,}000$ in 2068 BS and $50{,}000$ in 2078 BS. What
will it be in 2088 BS?

**Solution.** Let $P$ be the population $t$ years after 2068 BS. Then

$$ \frac{dP}{dt} = kP \quad\Longrightarrow\quad P = 40000\,e^{kt} $$

using $P = 40000$ when $t = 0$. At $t = 10$, $P = 50000$:

$$ 50000 = 40000\,e^{10k} \quad\Longrightarrow\quad e^{10k} = \frac54 = 1.25 $$

$$ k = \frac{\ln 1.25}{10} \approx 0.02231\text{ per year} $$

For 2088 BS, $t = 20$, and since $e^{20k} = \left(e^{10k}\right)^{2}$:

$$ P = 40000\left(\frac54\right)^{2} = 40000 \times \frac{25}{16} = 62{,}500 $$

Notice that the second step avoided evaluating $k$ at all. Whenever the times are
equally spaced, work with the *ratio* and the arithmetic stays exact.
:::

```figure caption="Exponential growth $P = 40000\,e^{kt}$ with $k = \frac{1}{10}\ln 1.25 \approx 0.0223$ per year. Equal ten-year intervals multiply the population by the same factor $1.25$, giving 40 000, 50 000 and 62 500."
import numpy as np
fig, ax = plt.subplots(figsize=(4.9,2.9))
k = np.log(1.25)/10
t = np.linspace(0, 22, 400)
P = 40000*np.exp(k*t)
ax.plot(t, P, color=ACCENT, lw=2.0)
for tt, lab in [(0, '2068 BS\n40 000'), (10, '2078 BS\n50 000'), (20, '2088 BS\n62 500')]:
    ax.plot([tt], [40000*np.exp(k*tt)], 'o', color='#d9534f', ms=5)
    ax.plot([tt, tt], [0, 40000*np.exp(k*tt)], color=MUTED, lw=0.7, ls=':')
ax.annotate('2068 BS\n40 000', (0, 40000), textcoords='offset points',
            xytext=(9, -19), fontsize=8.4, color=INK)
ax.annotate('2078 BS\n50 000', (10, 50000), textcoords='offset points',
            xytext=(-46, 4), fontsize=8.4, color=INK)
ax.annotate('2088 BS\n62 500', (20, 62500), textcoords='offset points',
            xytext=(-50, 6), fontsize=8.4, color=INK)
ax.set_xlabel('years after 2068 BS,  $t$'); ax.set_ylabel('population  $P$')
ax.set_xlim(0, 22.5); ax.set_ylim(35000, 70000)
ax.set_title('$\\frac{dP}{dt} = kP \\Rightarrow P = 40000\\,e^{kt}$', fontsize=9.4)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.4)
```

::: example Worked example 14.22
**Problem.** A bacterial culture doubles in $3$ hours. By what factor has it
grown after $12$ hours?

**Solution.** With $N = N_{0}e^{kt}$ and $N = 2N_{0}$ at $t=3$,

$$ e^{3k} = 2 \quad\Longrightarrow\quad k = \frac{\ln 2}{3} $$

After $12$ hours, $12 = 4\times 3$, so

$$ \frac{N}{N_{0}} = e^{12k} = \left(e^{3k}\right)^{4} = 2^{4} = 16 $$

The culture is $16$ times its original size. Exponential growth doubles in a
*fixed time*, no matter how large the population already is.
:::

### Newton's law of cooling

::: derivation Newton's law of cooling
A body at temperature $\theta$ in surroundings at temperature $\theta_{s}$ loses
heat at a rate proportional to the temperature *excess*:

$$ \frac{d\theta}{dt} = -k\left(\theta - \theta_{s}\right), \qquad k>0 $$

Separate the variables, writing $\theta - \theta_{s}$ as the single quantity that
matters:

$$ \frac{d\theta}{\theta-\theta_{s}} = -k\,dt \quad\Longrightarrow\quad
\ln\left|\theta-\theta_{s}\right| = -kt + c $$

$$ \theta - \theta_{s} = Ae^{-kt} \quad\Longrightarrow\quad
\theta = \theta_{s} + \left(\theta_{0}-\theta_{s}\right)e^{-kt} $$

where $\theta_{0}$ is the initial temperature. As $t\to\infty$ the exponential
dies and $\theta\to\theta_{s}$: the surrounding temperature is a **horizontal
asymptote**, and the body never quite reaches it.
:::

::: example Worked example 14.23
**Problem.** A glass of tea at $80\,^{\circ}$C is left in a room at
$20\,^{\circ}$C. After $10$ minutes it has cooled to $50\,^{\circ}$C. Find its
temperature after a further $10$ minutes, and the time at which it reaches
$30\,^{\circ}$C.

**Solution.** Here $\theta_{s} = 20$ and $\theta_{0} = 80$, so the excess starts
at $60$:

$$ \theta = 20 + 60e^{-kt} $$

At $t=10$, $\theta = 50$, so the excess is $30$:

$$ 30 = 60e^{-10k} \quad\Longrightarrow\quad e^{-10k} = \frac12
\quad\Longrightarrow\quad k = \frac{\ln 2}{10} \approx 0.0693\text{ per minute} $$

The excess halves every $10$ minutes. At $t = 20$ the excess is
$60\times\frac14 = 15$, so

$$ \theta = 20 + 15 = 35\,^{\circ}\text{C} $$

For $\theta = 30$ the excess is $10$:

$$ 10 = 60e^{-kt} \quad\Longrightarrow\quad e^{kt} = 6
\quad\Longrightarrow\quad t = \frac{\ln 6}{k} = \frac{10\ln 6}{\ln 2}
\approx 25.8\text{ minutes} $$
:::

```figure caption="Newton's law of cooling for tea at $80\,^\circ$C in a $20\,^\circ$C room: $\theta = 20 + 60e^{-kt}$ with $k = \frac{\ln 2}{10}$. The excess over room temperature halves every ten minutes, giving $50\,^\circ$C and $35\,^\circ$C, and the dashed line $\theta = 20$ is the asymptote the curve approaches but never reaches."
import numpy as np
fig, ax = plt.subplots(figsize=(5.0,2.9))
k = np.log(2)/10
t = np.linspace(0, 42, 500)
T = 20 + 60*np.exp(-k*t)
ax.plot(t, T, color=ACCENT, lw=2.0)
ax.axhline(20, color='#d9534f', lw=1.3, ls='--')
ax.annotate('asymptote  $\\theta_s = 20\\,^\\circ$C',
            (26.5, 21.6), fontsize=8.8, color='#9c3531')
for tt, TT in [(0, 80), (10, 50), (20, 35)]:
    ax.plot([tt], [TT], 'o', color=INK, ms=4.6)
    ax.plot([tt, tt], [20, TT], color=MUTED, lw=0.7, ls=':')
    ax.annotate('$%d\\,^\\circ$C' % TT, (tt, TT), textcoords='offset points',
                xytext=(5, 4), fontsize=8.6, color=INK)
ax.fill_between(t, 20, T, color=ACCENT, alpha=0.10)
ax.annotate('excess $\\theta-\\theta_s$ halves\nevery 10 minutes', (14, 30), (20.5, 52),
            fontsize=8.6, color=INK, arrowprops=dict(arrowstyle='->', color=INK, lw=0.8))
ax.set_xlabel('time  $t$  (minutes)'); ax.set_ylabel('temperature  $\\theta$  ($^\\circ$C)')
ax.set_xlim(0, 42); ax.set_ylim(14, 88)
ax.set_title("Newton's law of cooling:  $\\theta = 20 + 60e^{-kt}$", fontsize=9.4)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.4)
```

### Radioactive decay

For a radioactive sample the number of undecayed nuclei satisfies
$\frac{dN}{dt} = -\lambda N$, so $N = N_{0}e^{-\lambda t}$. The **half-life**
$T$ is the time for half the sample to decay, and putting
$N = \frac{N_{0}}{2}$ gives

$$ \frac12 = e^{-\lambda T} \quad\Longrightarrow\quad
T = \frac{\ln 2}{\lambda} $$

The half-life does not depend on how much you started with — that is the single
most useful fact about decay.

```figure caption="Radioactive decay $N = N_0e^{-\lambda t}$ with half-life $T = 30$ years. Each interval of $30$ years leaves half of what was there, so the fractions remaining at $30$, $60$ and $90$ years are $\frac12$, $\frac14$ and $\frac18$."
import numpy as np
fig, ax = plt.subplots(figsize=(5.0,2.9))
Th = 30.0
lam = np.log(2)/Th
t = np.linspace(0, 100, 500)
N = np.exp(-lam*t)
ax.plot(t, N, color=ACCENT, lw=2.0)
for n in (1, 2, 3):
    tt = n*Th
    ax.plot([0, tt], [0.5**n, 0.5**n], color=MUTED, lw=0.8, ls=':')
    ax.plot([tt, tt], [0, 0.5**n], color=MUTED, lw=0.8, ls=':')
    ax.plot([tt], [0.5**n], 'o', color='#d9534f', ms=4.6)
ax.annotate('', xy=(0, 1.06), xytext=(30, 1.06),
            arrowprops=dict(arrowstyle='<|-|>', color='#9c3531', lw=1.0, mutation_scale=8))
ax.annotate('half-life $T = \\frac{\\ln 2}{\\lambda} = 30$ yr', (22, 1.135),
            ha='center', fontsize=8.8, color='#9c3531')
for n, lab in [(1, '$\\frac{1}{2}$'), (2, '$\\frac{1}{4}$'), (3, '$\\frac{1}{8}$')]:
    ax.annotate(lab, (n*Th, 0.5**n), textcoords='offset points', xytext=(7, 3),
                fontsize=9.6, color=INK)
ax.set_xticks([0, 30, 60, 90])
ax.set_xlabel('time  $t$  (years)'); ax.set_ylabel('fraction left  $N/N_0$')
ax.set_xlim(0, 100); ax.set_ylim(0, 1.34)
ax.set_title('$\\frac{dN}{dt} = -\\lambda N \\Rightarrow N = N_0 e^{-\\lambda t}$', fontsize=9.4)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.4)
```

::: example Worked example 14.24
**Problem.** Radium has a half-life of $1600$ years. What fraction of a sample
remains after $3200$ years? And if a different substance loses $20\%$ of its mass
in $10$ days, find its half-life.

**Solution.** **(a)** $3200 = 2\times 1600$, so two half-lives have passed and

$$ \frac{N}{N_{0}} = \left(\frac12\right)^{2} = \frac14 = 25\% $$

**(b)** Losing $20\%$ leaves $80\%$, so $e^{-10\lambda} = 0.8$ and

$$ \lambda = -\frac{\ln 0.8}{10} = \frac{\ln 1.25}{10} \approx 0.02231
\text{ per day} $$

$$ T = \frac{\ln 2}{\lambda} = \frac{10\ln 2}{\ln 1.25}
\approx \frac{6.931}{0.2231} \approx 31.1\text{ days} $$
:::

## Chapter summary

- A **differential equation** relates $y$ to its derivatives. Its **order** is
  the highest derivative present; its **degree** is the power of that derivative
  once all radicals in the derivatives have been cleared. The degree may be
  undefined.
- The **general solution** of an $n$-th order equation contains $n$ arbitrary
  constants. Extra conditions turn it into a **particular solution**. To **form**
  the equation of a family with $n$ constants, differentiate $n$ times and
  eliminate the constants.
- A first-order first-degree equation has a one-parameter family of solutions, and
  the **slope field** is the picture of that family.
- **Separable**: write $f(y)\,dy = g(x)\,dx$ and integrate both sides. Test this
  first, because it is the cheapest method.
- **Homogeneous**: if $\frac{dy}{dx} = F\left(\frac yx\right)$, put $y = vx$ so
  that $\frac{dy}{dx} = v + x\frac{dv}{dx}$. The result always separates.
- **Reducible to homogeneous**: for
  $\frac{dy}{dx} = \frac{a_{1}x+b_{1}y+c_{1}}{a_{2}x+b_{2}y+c_{2}}$, shift the
  origin with $x = X+h$, $y = Y+k$ chosen to kill both constants.
- **Linear**: for $\frac{dy}{dx} + Py = Q$ the integrating factor is
  $I = e^{\int P\,dx}$, and then $Iy = \int IQ\,dx + C$.
- **Exact**: $M\,dx + N\,dy = 0$ is exact when
  $\frac{\partial M}{\partial y} = \frac{\partial N}{\partial x}$, and the
  solution is $u = C$ where $\frac{\partial u}{\partial x} = M$ and
  $\frac{\partial u}{\partial y} = N$.
- **Applications.** Proportional change gives $\frac{dy}{dt} = ky$ and
  $y = y_{0}e^{kt}$: growth for $k>0$, decay for $k<0$, with half-life
  $T = \frac{\ln 2}{\lambda}$. Newton's law of cooling gives
  $\theta = \theta_{s} + \left(\theta_{0}-\theta_{s}\right)e^{-kt}$, with
  $\theta_{s}$ as a horizontal asymptote.
- Whenever the given times are equally spaced, work with **ratios** rather than
  computing $k$ — the arithmetic stays exact and much shorter.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The order and degree of
   $\left(\dfrac{d^{2}y}{dx^{2}}\right)^{3} + \left(\dfrac{dy}{dx}\right)^{2} = 0$
   are <span class="marks">[1]</span>
   (a) $2$ and $2$ (b) $2$ and $3$ (c) $3$ and $2$ (d) $1$ and $2$
2. The general solution of a differential equation of order $3$ contains <span class="marks">[1]</span>
   (a) $1$ constant (b) $2$ constants (c) $3$ constants (d) no constant
3. The integrating factor of $\dfrac{dy}{dx} + \dfrac{y}{x} = x^{2}$ is <span class="marks">[1]</span>
   (a) $x$ (b) $\ln x$ (c) $\dfrac1x$ (d) $e^{x}$
4. The differential equation of the family of lines $y = mx$ is <span class="marks">[1]</span>
   (a) $\dfrac{dy}{dx} = x$ (b) $\dfrac{dy}{dx} = m$ (c) $\dfrac{dy}{dx} = \dfrac{y}{x}$ (d) $x\dfrac{dy}{dx} = 1$
5. The substitution that reduces a homogeneous equation to separable form is <span class="marks">[1]</span>
   (a) $y = vx$ (b) $x+y = v$ (c) $y = e^{v}$ (d) $v = \dfrac{dy}{dx}$
6. $M\,dx + N\,dy = 0$ is exact if <span class="marks">[1]</span>
   (a) $M = N$ (b) $\dfrac{\partial M}{\partial x} = \dfrac{\partial N}{\partial y}$ (c) $\dfrac{\partial M}{\partial y} = \dfrac{\partial N}{\partial x}$ (d) $MN = 1$
7. If a radioactive substance decays with constant $\lambda$, its half-life is <span class="marks">[1]</span>
   (a) $\dfrac{1}{\lambda}$ (b) $\dfrac{\ln 2}{\lambda}$ (c) $\lambda\ln 2$ (d) $\dfrac{2}{\lambda}$

::: note Answers to Group A
**1.** (b) — the highest derivative is of order $2$ and it is cubed.

**2.** (c) — one arbitrary constant for each integration.

**3.** (a) — $I = e^{\int dx/x} = e^{\ln x} = x$.

**4.** (c) — differentiating gives $\frac{dy}{dx}=m$, and $m = \frac yx$ from the
family itself.

**5.** (a) — then $\frac{dy}{dx} = v + x\frac{dv}{dx}$ and the variables separate.

**6.** (c) — both sides equal the mixed partial derivative of the same function
$u$.

**7.** (b) — $\frac12 = e^{-\lambda T}$ gives $T = \frac{\ln 2}{\lambda}$.
:::

**Group B — Short answer (5 marks each)**

1. Form the differential equation of the family of circles $x^{2}+y^{2} = a^{2}$
   and state its order and degree. <span class="marks">[5]</span>
2. Solve $\dfrac{dy}{dx} = e^{x-y}$. <span class="marks">[5]</span>
3. Solve $\dfrac{dy}{dx} = \dfrac{x-y}{x+y}$. <span class="marks">[5]</span>
4. Solve $x\dfrac{dy}{dx} + 2y = x^{3}$. <span class="marks">[5]</span>
5. Show that $\left(y\cos x + 1\right)dx + \sin x\,dy = 0$ is exact and solve
   it. <span class="marks">[5]</span>
6. A body cools from $100\,^{\circ}$C to $70\,^{\circ}$C in $5$ minutes in a room
   at $20\,^{\circ}$C. Find its temperature after $10$ minutes. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Differentiate $x^{2}+y^{2}=a^{2}$ with respect to $x$:
$2x + 2y\frac{dy}{dx} = 0$, so

$$ x + y\frac{dy}{dx} = 0, \qquad\text{that is}\qquad \frac{dy}{dx} = -\frac{x}{y} $$

The constant $a$ disappeared on its own because the family has one constant and we
differentiated once. The equation is of **order 1 and degree 1**.

**2.** Split the exponential and separate:
$e^{y}dy = e^{x}dx$. Integrating, $e^{y} = e^{x} + C$, that is
$y = \ln\left(e^{x}+C\right)$.

**3.** Both parts are homogeneous of degree $1$, so put $y = vx$:

$$ v + x\frac{dv}{dx} = \frac{1-v}{1+v} \quad\Longrightarrow\quad
x\frac{dv}{dx} = \frac{1-2v-v^{2}}{1+v} $$

Separating and noting that $\frac{d}{dv}\left(1-2v-v^{2}\right) = -2(1+v)$,

$$ -\frac12\ln\left|1-2v-v^{2}\right| = \ln|x| - \frac12\ln|C| $$

so $x^{2}\left(1-2v-v^{2}\right) = C$, and with $v = \frac yx$,

$$ x^{2}-2xy-y^{2} = C $$

**4.** Divide by $x$: $\frac{dy}{dx} + \frac2x y = x^{2}$, so $P = \frac2x$ and
$I = e^{2\ln x} = x^{2}$. Then

$$ \frac{d}{dx}\left(x^{2}y\right) = x^{4} \quad\Longrightarrow\quad
x^{2}y = \frac{x^{5}}{5} + C \quad\Longrightarrow\quad
y = \frac{x^{3}}{5} + \frac{C}{x^{2}} $$

**5.** $M = y\cos x + 1$ and $N = \sin x$, so
$\frac{\partial M}{\partial y} = \cos x = \frac{\partial N}{\partial x}$ and the
equation is exact. Integrating $M$ with respect to $x$,
$u = y\sin x + x + g(y)$. Then
$\frac{\partial u}{\partial y} = \sin x + g'(y) = N = \sin x$, so $g'(y)=0$.
The solution is

$$ y\sin x + x = C $$

**6.** With $\theta_{s}=20$ and $\theta_{0}=100$ the excess starts at $80$:
$\theta = 20 + 80e^{-kt}$. At $t=5$, $\theta = 70$, so the excess is $50$:

$$ e^{-5k} = \frac{50}{80} = \frac58 $$

At $t = 10$ the excess is $80\left(e^{-5k}\right)^{2} = 80\times\frac{25}{64}
= 31.25$, so

$$ \theta = 20 + 31.25 = 51.25\,^{\circ}\text{C} $$
:::

**Group C — Long answer (8 marks each)**

1. (a) Derive the integrating factor of the linear equation
   $\dfrac{dy}{dx} + P(x)y = Q(x)$. (b) Hence solve
   $\dfrac{dy}{dx} + y\cot x = 2\cos x$. <span class="marks">[8]</span>
2. (a) State Newton's law of cooling as a differential equation and solve it to
   show that $\theta = \theta_{s} + \left(\theta_{0}-\theta_{s}\right)e^{-kt}$.
   (b) A body at $100\,^{\circ}$C is left in a room at $25\,^{\circ}$C and cools
   to $70\,^{\circ}$C in $10$ minutes. Find its temperature after $20$ minutes and
   the time it takes to reach $40\,^{\circ}$C. <span class="marks">[8]</span>
3. (a) Solve $x\dfrac{dy}{dx} = y + \sqrt{x^{2}+y^{2}}$ for $x>0$.
   (b) Show that $(2x+3y)\,dx + (3x+4y)\,dy = 0$ is exact and solve it. <span class="marks">[8]</span>

::: note Answers to Group C
**1. (a)** Multiply the equation by an unknown function $I(x)$:
$I\frac{dy}{dx} + IPy = IQ$. We want the left side to be $\frac{d}{dx}(Iy)$,
which equals $I\frac{dy}{dx} + \frac{dI}{dx}y$. Comparing the two,
$\frac{dI}{dx} = IP$. This separates:

$$ \frac{dI}{I} = P\,dx \quad\Longrightarrow\quad \ln I = \int P\,dx
\quad\Longrightarrow\quad I = e^{\int P\,dx} $$

With this $I$ the equation reads $\frac{d}{dx}(Iy) = IQ$, and integrating gives
$Iy = \int IQ\,dx + C$.

**(b)** Here $P = \cot x$ and $Q = 2\cos x$, so
$\int P\,dx = \ln|\sin x|$ and $I = \sin x$. Then

$$ \frac{d}{dx}\left(y\sin x\right) = 2\sin x\cos x $$

The right side is the derivative of $\sin^{2}x$, so
$y\sin x = \sin^{2}x + C$ and

$$ y = \sin x + C\csc x $$

**2. (a)** The rate of cooling is proportional to the excess over the
surroundings:

$$ \frac{d\theta}{dt} = -k\left(\theta-\theta_{s}\right), \qquad k>0 $$

Separating the variables,
$\frac{d\theta}{\theta-\theta_{s}} = -k\,dt$, so
$\ln\left|\theta-\theta_{s}\right| = -kt + c$ and
$\theta - \theta_{s} = Ae^{-kt}$. At $t=0$, $\theta = \theta_{0}$, so
$A = \theta_{0}-\theta_{s}$ and

$$ \theta = \theta_{s} + \left(\theta_{0}-\theta_{s}\right)e^{-kt} $$

**(b)** Here $\theta_{s} = 25$ and $\theta_{0} = 100$, so the excess starts at
$75$ and $\theta = 25 + 75e^{-kt}$. At $t=10$, $\theta = 70$, so the excess is
$45$:

$$ e^{-10k} = \frac{45}{75} = \frac35 $$

At $t=20$ the excess is $75\left(\frac35\right)^{2} = 75\times\frac{9}{25} = 27$,
so

$$ \theta = 25+27 = 52\,^{\circ}\text{C} $$

For $\theta = 40$ the excess is $15$, so $e^{-kt} = \frac{15}{75} = \frac15$ and
$kt = \ln 5$. Since $k = \frac{1}{10}\ln\frac53$,

$$ t = \frac{10\ln 5}{\ln\frac53} \approx \frac{16.094}{0.5108}
\approx 31.5\text{ minutes} $$

**3. (a)** Divide by $x$ (positive) to get
$\frac{dy}{dx} = \frac{y}{x} + \sqrt{1+\frac{y^{2}}{x^{2}}}$, which depends only
on $\frac yx$, so the equation is homogeneous. Put $y = vx$:

$$ v + x\frac{dv}{dx} = v + \sqrt{1+v^{2}} \quad\Longrightarrow\quad
x\frac{dv}{dx} = \sqrt{1+v^{2}} $$

$$ \frac{dv}{\sqrt{1+v^{2}}} = \frac{dx}{x} \quad\Longrightarrow\quad
\ln\left|v+\sqrt{1+v^{2}}\right| = \ln|x| + \ln|C| $$

using the standard integral $\int\frac{dv}{\sqrt{v^{2}+1}}
= \ln\left|v+\sqrt{v^{2}+1}\right|$. Removing the logarithms,
$v+\sqrt{1+v^{2}} = Cx$, and putting $v = \frac yx$ and multiplying by $x$:

$$ y + \sqrt{x^{2}+y^{2}} = Cx^{2} $$

**(b)** $M = 2x+3y$ and $N = 3x+4y$, so
$\frac{\partial M}{\partial y} = 3 = \frac{\partial N}{\partial x}$ and the
equation is exact. Integrating $M$ with respect to $x$,

$$ u = \int(2x+3y)\,dx = x^{2} + 3xy + g(y) $$

Differentiating with respect to $y$ and comparing with $N$:

$$ 3x + g'(y) = 3x + 4y \quad\Longrightarrow\quad g'(y) = 4y
\quad\Longrightarrow\quad g(y) = 2y^{2} $$

The general solution is

$$ x^{2} + 3xy + 2y^{2} = C $$
:::
