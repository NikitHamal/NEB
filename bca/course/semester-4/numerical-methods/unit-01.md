---
subject: Numerical Methods
grade: BCA Semester 4
unit: 1
title: Solution of Nonlinear Equations
hours: 10
area: BCA 253 · Numerical Methods · Unit 1
---

Most equations that arise in engineering have no formula for their solution. There is no closed form for the root of $x^{3} - x - 2 = 0$ that you would want to use, and none at all for $\cos x = x$. **Numerical methods** find an approximate answer to any wanted accuracy by repeating a simple calculation. This unit covers the errors that creep in and the classical root-finding methods.

::: key What this unit gives you
- Types of equations and errors in computing (round-off, truncation, absolute, relative).
- Bisection, false position, Newton–Raphson and secant methods with complete iteration tables.
- Fixed-point iteration and its convergence condition; Newton's method for a system of two nonlinear equations.
- Order of convergence and how to choose a method.
:::

Arithmetic is done in double precision and shown to six decimals.

## 1.1 Types of equations and locating roots

An **algebraic** equation is a polynomial equation $(x^{3} - x - 2 = 0)$. A **transcendental** equation involves trigonometric, exponential or logarithmic functions $(e^{x} = 3 x ,\  \cos x = x)$. A **root** (zero) of *f* is a number *α* with $f (\alpha) = 0$.

**Intermediate value theorem.** If *f* is continuous on $[a ,\  b]$ and $f (a) \cdot f (b) < 0$, then *f* has at least one root in $(a ,\  b)$. This sign change is how we **bracket** a root: tabulate *f* at convenient points and look for a sign change. For $f (x) = x^{3} - x - 2$ we have $f (1) = - 2$ and $f (2) = + 4$, so a root lies in (1, 2). The exact root, correct to ten decimals, is $\alpha = 1.5213797068$.

## 1.2 Errors in computing

If the true value is $\ast x \ast$ and the approximation is *x̂*:

- **Absolute error** E = |x − x̂|.
- **Relative error** Eᵣ = |x − x̂| / $|x|$; **percentage error** = Eᵣ × 100.
- A number is correct to $\ast n \ast$ **significant digits** if its relative error is below $5 \times 10^{-n}$.

::: example Errors in approximating √2
$\sqrt{2} = 1.4142136$. Using x̂ = 1.414: $E = 0.0002136$, Eᵣ = 0.0001510, percentage error = 0.0151 %. The approximation is correct to four significant digits since Eᵣ < $5 \times 10^{-4}$.
:::

### Sources of error

1. **Inherent (input) error**: measurement or data error before the computation starts.
2. **Round-off error**: a computer stores numbers with finite digits. Adding 0.3333 three times gives 0.9999, not 1. Double precision carries about 16 significant digits; single precision about 7.
3. **Truncation error**: an infinite process (series, limit) is cut short. Approximating $e^{x}$ at $x = 0.5$ by the first three Taylor terms gives 1.625000, and by four terms gives 1.645833, whereas the true value is 1.648721. The truncation errors are 0.023721 and 0.002888; each extra term cuts the error by roughly a factor of ten here.
4. **Propagation of error**: errors in the inputs grow or shrink through the operations. Subtracting nearly equal numbers (**cancellation**) is the worst case.

::: example Cancellation destroys digits
Compute $\sqrt{10001} - \sqrt{10000}$ with five-significant-digit arithmetic. $\sqrt{10001}$ rounds to 100.00 and $\sqrt{10000} = 100.00$, so the difference is 0.00000, all accuracy lost; the true value is 0.0049999. Rewriting algebraically as $\frac{1}{\sqrt{10001} + \sqrt{10000}}$ avoids the subtraction and gives 0.0049999 with the same five-digit arithmetic. Good numerical practice is to rearrange formulas to avoid subtracting nearly equal numbers.
:::

For a sum or difference the absolute errors add; for a product or quotient the *relative* errors add. For a function, the error is about $|f' (x)| \cdot \Delta x$.

## 1.3 The bisection method

**Idea.** Keep an interval $[a ,\  b]$ with $f (a) \cdot f (b) < 0$. Take the midpoint $c = \frac{a + b}{2}$. Replace *b* by *c* if $f (a) \cdot f (c) < 0$, otherwise replace a by *c*. The interval halves each time.

**Algorithm.** (1) Choose $a ,\  b$ with $f (a) f (b) < 0$ and a tolerance *ε*. (2) $c = \frac{a + b}{2}$. (3) If $f (c) = 0$ or $\frac{b - a}{2} < \epsilon$, stop: *c* is the root. (4) If $f (a) f (c) < 0$, set $b = c$; else set $a = c$. (5) Go to 2.

**Error bound.** After $\ast n \ast$ steps the root lies in an interval of length $\frac{b - a}{2^{n}}$, so the number of steps needed for accuracy *ε* is **$n \geq \log_{2} \left( \frac{b - a}{\epsilon} \right)$**. For [1, 2] this is $n \geq 10$ for $\epsilon = 10^{-3}$ and $n \geq 20$ for $\epsilon = 10^{-6}$.

::: example Bisection on x³ − x − 2 = 0, [1, 2]
| *n* | a | *b* | $c = \frac{a + b}{2}$ | $f (c)$ |

|---|---|---|---|---|

| 1 | 1.000000 | 2.000000 | 1.500000 | -0.125000 |

| 2 | 1.500000 | 2.000000 | 1.750000 | +1.609375 |

| 3 | 1.500000 | 1.750000 | 1.625000 | +0.666016 |

| 4 | 1.500000 | 1.625000 | 1.562500 | +0.252197 |

| 5 | 1.500000 | 1.562500 | 1.531250 | +0.059113 |

| 6 | 1.500000 | 1.531250 | 1.515625 | -0.034054 |

| 7 | 1.515625 | 1.531250 | 1.523438 | +0.012250 |

| 8 | 1.515625 | 1.523438 | 1.519531 | -0.010971 |

| 9 | 1.519531 | 1.523438 | 1.521484 | +0.000622 |

| 10 | 1.519531 | 1.521484 | 1.520508 | -0.005179 |

After ten steps $c = 1.520508$. The true error is 0.000872, within the guaranteed bound $1 / 2^{10} = 0.000977$. Note that $f (c)$ does not shrink steadily, but the bracketing interval always halves; that is what makes the method foolproof.
:::

::: example Square root of 10 by bisection: x² − 10 = 0 on [3, 4]
| *n* | a | *b* | *c* | $f (c)$ |

|---|---|---|---|---|

| 1 | 3.000000 | 4.000000 | 3.500000 | +2.250000 |

| 2 | 3.000000 | 3.500000 | 3.250000 | +0.562500 |

| 3 | 3.000000 | 3.250000 | 3.125000 | -0.234375 |

| 4 | 3.125000 | 3.250000 | 3.187500 | +0.160156 |

| 5 | 3.125000 | 3.187500 | 3.156250 | -0.038086 |

| 6 | 3.156250 | 3.187500 | 3.171875 | +0.060791 |

After six steps the last midpoint is 3.171875 and, since $f (c) > 0$ there, the root lies in [3.156250, 3.171875] (width $1 / 2^{6} = 0.015625$); the true value is 3.162278.
:::

**Properties.** Always converges if *f* is continuous and the bracket is valid; simple; **linear** convergence (one binary digit per step); slow; cannot find roots of even multiplicity (no sign change, such as $x^{2} = 0$).

## 1.4 The method of false position (regula falsi)

Instead of the midpoint, use the point where the **chord** joining $(a ,\  f (a))$ and $(b ,\  f (b))$ crosses the x-axis:

$$c = \frac{a \cdot f (b) - b \cdot f (a)}{f (b) - f (a)}$$

and keep the sub-interval whose ends still have opposite signs.

::: example False position on x³ − x − 2 = 0, [1, 2]
| *n* | a | *b* | *c* | $f (c)$ |

|---|---|---|---|---|

| 1 | 1.000000 | 2.000000 | 1.333333 | -0.962963 |

| 2 | 1.333333 | 2.000000 | 1.462687 | -0.333339 |

| 3 | 1.462687 | 2.000000 | 1.504019 | -0.101818 |

| 4 | 1.504019 | 2.000000 | 1.516331 | -0.029895 |

| 5 | 1.516331 | 2.000000 | 1.519919 | -0.008675 |

| 6 | 1.519919 | 2.000000 | 1.520957 | -0.002509 |

| 7 | 1.520957 | 2.000000 | 1.521258 | -0.000725 |

After seven steps $c = 1.521258$; the error, about $1.2 \times 10^{-4}$, is already smaller than bisection's after ten steps $(8.7 \times 10^{-4})$. But notice that the end $b = 2$ never moves: because *f* is convex on this interval, the chord always lands on the same side of the root, so the approximations creep up from one side and each step shrinks the error only by a constant factor (about 0.29 here). That one-sided, merely linear behaviour is the usual weakness of the method; modified versions halve the stuck end's function value to repair it.
:::

## 1.5 The Newton–Raphson method

**Idea.** Replace *f* by its tangent line at the current guess $\ast x_{n} \ast$ and take the tangent's zero as the next guess. From the tangent $y = f (x_{n}) + f' (x_{n}) (x - x_{n})$ setting $y = 0$:

$$x_{n+1} = x_{n} - \frac{f (x_{n})}{f' (x_{n})}$$

The same formula follows from the first-order Taylor expansion $f (\alpha) \approx f (x_{n}) + (\alpha - x_{n}) f' (x_{n}) = 0$.

::: example Newton on f(x) = x³ − x − 2, f′(x) = 3x² − 1, x₀ = 1.5
| *n* | $x_{n}$ | $f (x_{n})$ | $f' (x_{n})$ | $x_{n+1}$ |

|---|---|---|---|---|

| 0 | 1.500000 | -0.125000 | 5.750000 | 1.521739 |

| 1 | 1.521739 | +0.002137 | 5.947070 | 1.521380 |

| 2 | 1.521380 | +0.000001 | 5.943790 | 1.521380 |

| 3 | 1.521380 | +0.000000 | 5.943789 | 1.521380 |

Two steps already give six correct decimals: the root is 1.521380. Compare ten bisection steps for three.
:::

::: example Square root of 10 by Newton (the "divide and average" rule)
For $f (x) = x^{2} - 10 ,\  x_{n+1} = x_{n} - \frac{x_{n}^{2} - 10}{(2 x_{n})} = \frac{1}{2} \left( x_{n} + \frac{10}{x_{n}} \right)$. Starting at $x_{0} = 3$:

| *n* | $x_{n}$ | $f (x_{n})$ | $f' (x_{n})$ | $x_{n+1}$ |

|---|---|---|---|---|

| 0 | 3.000000 | -1.000000 | 6.000000 | 3.166667 |

| 1 | 3.166667 | +0.027778 | 6.333333 | 3.162281 |

| 2 | 3.162281 | +0.000019 | 6.324561 | 3.162278 |

Three steps give 3.162278 to six decimals. This is the method calculators use for square roots.
:::

**Quadratic convergence.** Near a simple root the error satisfies $e_{n+1} \approx \left[ \frac{f'' (\alpha)}{2 f' (\alpha)} \right] \cdot e_{n}^{2}$, i.e. the number of correct digits roughly **doubles** each step. For our cubic the constant is $\frac{f''}{2 f'} = 0.768$. The actual errors of the iterates $x_{1} \ldots x_{4}$ were 2.14e-02, 3.59e-04, 9.92e-08, 7.55e-15 and the ratios $\frac{e_{n+1}}{e_{n}^{2}}$ were 0.786, 0.768, 0.768, settling at the predicted constant.

**Failure cases.** (1) $f' (x_{n}) = 0$ makes the step undefined; a tiny $f'$ throws the iterate far away. (2) A poor starting guess can diverge or wander to another root. (3) Cycling: for $f (x) = x^{3} - 2 x + 2$ starting at 0 the iterates alternate between 0 and 1. (4) For $f (x) = x^{\frac{1}{3}}$, the step is $x_{n+1} = x_{n} - 3 x_{n} = - 2 x_{n}$, so it diverges from every starting point. (5) At a multiple root convergence drops to linear. Always start near the root, found by a bracketing sweep or a few bisection steps.

## 1.6 The secant method

Newton needs the derivative. The **secant method** replaces $f' (x_{n})$ by the slope of the line through the last two points:

$$x_{n+1} = x_{n} - \frac{f (x_{n}) (x_{n} - x_{n-1})}{f (x_{n}) - f (x_{n-1})}$$

It needs two starting values but **no bracket** and only one new function evaluation per step.

::: example Secant on x³ − x − 2 = 0, x₀ = 1, x₁ = 2
| *n* | $x_{n-1}$ | $x_{n}$ | $f (x_{n-1})$ | $f (x_{n})$ | $x_{n+1}$ |

|---|---|---|---|---|---|

| 0 | 1.000000 | 2.000000 | -2.000000 | +4.000000 | 1.333333 |

| 1 | 2.000000 | 1.333333 | +4.000000 | -0.962963 | 1.462687 |

| 2 | 1.333333 | 1.462687 | -0.962963 | -0.333339 | 1.531169 |

| 3 | 1.462687 | 1.531169 | -0.333339 | +0.058626 | 1.520926 |

| 4 | 1.531169 | 1.520926 | +0.058626 | -0.002693 | 1.521376 |

| 5 | 1.520926 | 1.521376 | -0.002693 | -0.000020 | 1.521380 |

After six steps $x = 1.521380$. The first step $x_{2} = 1.333333$ equals the first false-position step, because both use the same chord; after that, the secant method always uses the two *latest* points and so is not held back by an old endpoint.
:::

The order of convergence is the golden ratio **$p \approx 1.618$**: between linear and quadratic. Per function evaluation it can beat Newton, because Newton needs *two* evaluations (*f* and $f'$) per step.

## 1.7 Fixed-point iteration and convergence

Rewrite $f (x) = 0$ as **$x = g (x)$** and iterate $x_{n+1} = g (x_{n})$. A root is a **fixed point** of *g*.

**Convergence theorem.** If *g* and $g'$ are continuous near the fixed point *α* and **$|g' (x)| < 1$** on an interval around *α* containing the starting value, the iteration converges to *α*, and the smaller $|g' (\alpha)|$, the faster. Convergence is linear with ratio $|g' (\alpha)|$. If $|g' (\alpha)| > 1$ it diverges.

::: example x³ − x − 2 = 0 rearranged as x = (x + 2)^(1/3), x₀ = 1.5
| *n* | $x_{n}$ | $x_{n+1} = (x_{n} + 2)^{\frac{1}{3}}$ |  | error |  |

|---|---|---|---|

| 0 | 1.500000 | 1.518294 | 3.09e-03 |

| 1 | 1.518294 | 1.520935 | 4.44e-04 |

| 2 | 1.520935 | 1.521316 | 6.40e-05 |

| 3 | 1.521316 | 1.521370 | 9.22e-06 |

| 4 | 1.521370 | 1.521378 | 1.33e-06 |

| 5 | 1.521378 | 1.521380 | 1.91e-07 |

| 6 | 1.521380 | 1.521380 | 2.75e-08 |

Here $g' (\alpha) = \frac{1}{3} (\alpha + 2)^{- \frac{2}{3}} = 0.1440$, so the error shrinks by about that factor each step (compare the error column: 3.09e-03, 4.44e-04, ... ratio ≈ 0.14). Another rearrangement, $x = x^{3} - 2$, has $|g' (\alpha)| = 3 \alpha^{2} = 6.944 > 1$ and from $x_{0} = 1.5$ the iterates are 1.375, 0.5996, -1.784, -7.682: it **diverges**, even though both rearrangements have the same root. The choice of *g* matters.
:::

## 1.8 Systems of nonlinear equations

For two unknowns, solve $f_{1} (x ,\  y) = 0 ,\  f_{2} (x ,\  y) = 0$ by **Newton's method**: at each step solve the linear system $J (x_{n} ,\  y_{n}) \cdot (\Delta x ,\  \Delta y)^{T} = - (f_{1} ,\  f_{2})^{T}$, where J is the **Jacobian** of partial derivatives, and update $x_{n+1} = x_{n} + \Delta x ,\  y_{n+1} = y_{n} + \Delta y$.

::: example x² + y² = 4 and xy = 1, starting from (2, 0.5)
$f_{1} = x^{2} + y^{2} - 4 ,\  f_{2} = x y - 1 ;\  J = \begin{bmatrix} 2 x & 2 y \\ y & x \end{bmatrix}$. At (2, 0.5): $J = \begin{bmatrix} 4 & 1 \\ 0.5 & 2 \end{bmatrix} ,\  (f_{1} ,\  f_{2}) = (0.25 ,\  0)$, and solving $J \cdot \Delta = - f$ gives $\Delta = (- 0.066667 ,\  0.016667)$, so the next point is (1.933333, 0.516667).

| *n* | $x_{n}$ | $y_{n}$ | $f_{1}$ | $f_{2}$ | $x_{n+1}$ | $y_{n+1}$ |

|---|---|---|---|---|---|---|

| 0 | 2.000000 | 0.500000 | +0.250000 | +0.000000 | 1.933333 | 0.516667 |

| 1 | 1.933333 | 0.516667 | +0.004722 | -0.001111 | 1.931853 | 0.517637 |

| 2 | 1.931853 | 0.517637 | +0.000003 | -0.000001 | 1.931852 | 0.517638 |

| 3 | 1.931852 | 0.517638 | +0.000000 | -0.000000 | 1.931852 | 0.517638 |

| 4 | 1.931852 | 0.517638 | -0.000000 | +0.000000 | 1.931852 | 0.517638 |

The solution is $(x ,\  y) = (1.931852 ,\  0.517638)$, which agrees with the exact answer $\left( \frac{\sqrt{6} + \sqrt{2}}{2} ,\  \frac{\sqrt{6} - \sqrt{2}}{2} \right)$. The number of correct digits doubles each step, as in the one-variable case.
:::

An alternative is **fixed-point iteration** on $x = g_{1} (x ,\  y) ,\  y = g_{2} (x ,\  y)$, converging when the Jacobian of *g* has norm below 1.

## 1.9 Choosing a method

| Method | Needs | Order | Evaluations per step | Guaranteed? |
|---|---|---|---|---|
| Bisection | bracket | 1 (linear, ratio $\frac{1}{2}$) | 1 *f* | yes |
| False position | bracket | 1 (often slow, one end stuck) | 1 *f* | yes |
| Secant | two starts | 1.618 | 1 *f* | no |
| Newton–Raphson | $f'$ and a start | 2 | 1 $f + 1 f'$ | no |
| Fixed point | *g* with | $g'$ | < 1 | 1 (ratio | $g'$ | ) | 1 *g* | only if | $g'$ | < 1 |

A practical strategy: bracket the root, take a few bisection steps, then finish with Newton or secant. A good program stops when $|x_{n+1} - x_{n}| < \epsilon$ or $|f (x_{n})| < \epsilon$, and also after a maximum number of iterations.

## 1.10 Seeing the ideas: Newton's tangent, bracketing and how fast each method converges

Most of the root-finding methods in this unit are geometric ideas before they are formulas. Plate 1.1 pairs the man behind the tangent method with a picture of his iteration, and the figures after it compare bracketing with fast iteration.

```photogrid label="1.1" cols="2" ratio="1.1" caption="Newton's method. (a) Isaac Newton, who described the tangent iteration in the 1670s (Joseph Raphson published the simplified form in 1690). (b) The iteration for $f (x) = x^{3} - x - 2$ from x0 = 2: each tangent line hits the x-axis at the next guess, 1.636364 and then 1.530397, closing in on the root 1.521380."
@ photo id="bca104/newton" cap="Isaac Newton"
fit 1.1
focus 0.5 0.7
@ svg cap="Tangent steps from x0 = 2"
f = Fig(300, 250)
ax = Axes(f, 36, 12, 250, 190, (1.3, 2.1), (-1, 4.5))
ax.grid(0.2, 1)
ax.axes("", "")
g = lambda x: x**3 - x - 2
gp = lambda x: 3 * x * x - 1
ax.curve(g, 1.3, 2.1, color=NAVY)
x = 2.0
for k in range(2):
    xn = x - g(x) / gp(x)
    f.line(ax.X(x), ax.Y(0), ax.X(x), ax.Y(g(x)), color=SLATE, dash=True)
    f.line(ax.X(x), ax.Y(g(x)), ax.X(xn), ax.Y(0), color=RED, sw=1.8)
    ax.pt(xn, 0, "x%d = %.4f" % (k + 1, xn), dx=(-4 if k == 0 else -30), dy=(-16 if k == 0 else 30), anchor="start", size=9.5)
    x = xn
ax.pt(2.0, 0, "x0 = 2", dx=0, dy=18, anchor="middle", size=9.5)
f.text(165, 232, "each tangent crosses the axis at the next guess", size=9.5, color=SLATE)
```

```svgfig label="1.1" caption="Bisection on $f (x) = x^{3} - x - 2$ in [1, 2]. The sign change guarantees a root inside; each midpoint c1 = 1.5, c2 = 1.75, c3 = 1.625, c4 = 1.5625 keeps the half that still has opposite signs at its ends, so the bracket halves every step."
f = Fig(580, 230)
ax = Axes(f, 50, 14, 510, 170, (0.9, 2.1), (-3, 5))
ax.grid(0.2, 1)
ax.axes("", "")
g = lambda x: x**3 - x - 2
ax.curve(g, 0.9, 2.1, color=NAVY)
ax.hline(0, color=SLATE, dash=False)
for k, c in enumerate([1.5, 1.75, 1.625, 1.5625]):
    ax.pt(c, g(c), "c%d" % (k + 1), dx=6, dy=-8 if g(c) > 0 else 16, size=10.5)
f.text(ax.X(1.62), ax.Y(-2.3), "bracket [1, 2]: f(1) = -2 < 0, f(2) = +4 > 0", size=10, color=TEAL, bold=True)
```

```svgfig label="1.2" caption="Speed of convergence for $x^{3} - x - 2 = 0$ (error on a log scale, 0 = error of 1, -6 = error of one millionth). Bisection gains a fixed amount per step (linear), false position and fixed-point iteration are also linear but faster, the secant method is superlinear (order 1.62) and Newton is quadratic, needing about 2 steps from x0 = 1.5 where bisection needs 19."
import math
f = Fig(580, 230)
ax = Axes(f, 50, 14, 510, 170, (0, 20), (-10, 0.5))
ax.grid(4, 2)
ax.axes("", "")
g = lambda x: x**3 - x - 2
gp = lambda x: 3 * x * x - 1
r = 1.5213797068045676
def lg(e): return max(-10, math.log10(max(e, 1e-12)))
a, b = 1.0, 2.0; pts = []
for n in range(1, 21):
    c = (a + b) / 2; pts.append((n, lg(abs(c - r))))
    if g(a) * g(c) < 0: b = c
    else: a = c
ax.curve(lambda n: lg(0.5 ** n), 0, 20, color=AMBER, label="bisection", lx=15, ly=-4.2)
x = 1.5; P = [(0, lg(abs(x - r)))]
for n in range(1, 5):
    x = x - g(x) / gp(x); P.append((n, lg(abs(x - r))))
for (n1, e1), (n2, e2) in zip(P, P[1:]):
    ax.curve(lambda t, n1=n1, e1=e1, n2=n2, e2=e2: e1 + (e2 - e1) * (t - n1) / (n2 - n1), n1, n2, color=RED, sw=2.4)
x = 1.5; P = [(0, lg(abs(x - r)))]
for n in range(1, 10):
    x = (x + 2) ** (1 / 3); P.append((n, lg(abs(x - r))))
for (n1, e1), (n2, e2) in zip(P, P[1:]):
    ax.curve(lambda t, n1=n1, e1=e1, n2=n2, e2=e2: e1 + (e2 - e1) * (t - n1) / (n2 - n1), n1, n2, color=TEAL, sw=2)
f.text(400, 72, "bisection: halves the error", size=10, color=AMBER, bold=True)
f.text(210, 110, "fixed point", size=10, color=TEAL, bold=True)
f.text(190, 176, "Newton (quadratic)", size=10, color=RED, bold=True)
f.text(306, 206, "iteration number", size=10.5, color=SLATE)
f.text(306, 222, "log10 of the error", size=10, color=SLATE)
```

### 1.10.1 Eight reasons engineers need numerical methods

1. **Most equations have no formula.** A polynomial of degree five or higher has no general solving formula, and equations such as $\cos x = x$ cannot be solved by algebra at all. Numerical methods still give the root to any accuracy we need. A calculator finds square roots in the same way.
2. **Real data is a table, not a formula.** Hydrologists in Nepal record the river flow at fixed hours, so they only have numbers. Interpolation, differentiation and integration work directly on such tables. No formula is needed.
3. **Exact integrals are often impossible.** The area under a curve such as *e* to the power minus *x* squared has no elementary answer. The trapezoidal and Simpson rules give it quickly and with a known error. Engineers use them to find the volume of water behind a $d a m$.
4. **Large systems of equations need computers.** A bridge model or an electrical network leads to hundreds of linear equations. Gauss elimination and iterative methods solve them in seconds. Solving them by hand would take days and would almost surely contain errors.
5. **Differential equations rarely have closed forms.** Cooling, population growth, vibration and circuit problems lead to equations that cannot be integrated exactly. Euler and Runge-Kutta methods step forward in time and give a usable answer. Weather forecasting is built on this idea.
6. **Errors can be measured and controlled.** Every method has an error bound or a stopping rule, such as the number of bisection steps *n* greater than or equal to log2((b - a) / tolerance). We know how accurate the answer is. This is better than a guess.
7. **Speed and cost.** Newton's method reaches six decimals in two or three steps, where bisection needs nineteen. Choosing a better method saves computer time in programs that run millions of times. This matters in games, simulations and mobile apps.
8. **Computers use them anyway.** Every scientific calculator, spreadsheet solver and programming library (NumPy, MATLAB) runs these algorithms inside. A student who knows them can choose the right tool and understand when the answer is unreliable. This is the base for data science and engineering software.

```photogrid label="1.2" cols="2" ratio="1.2" caption="A rounding error that grew with uptime. (a) A Patriot air-defence battery, one of the systems whose software counted time in tenths of a second. (b) The number 0.1 has no finite binary form, so a 24-bit register that keeps 23 binary places stores it as 0.0999999046, short by 9.54e-08 second on every tick. The error is invisible in one tick, but after 8 hours of continuous running the clock is 27 milliseconds wrong, which moves a target travelling at 1,676 metres a second by about 46 metres, and after 100 hours it is 0.34 second and 575 metres wrong. The sums were done with exact fractions. The lesson for numerical methods is that a tiny relative error multiplied by a large count is large, so count in integers where possible and know the bits you have."
@ photo id="bcanm/patriot" cap="A Patriot battery (Romanian Army): software clock matters"
fit 1.2
focus 0.5 0.5
@ svg cap="0.1 s stored in 23 bits: drift per hour"
from fractions import Fraction
tick = Fraction(1, 10)
stored = Fraction(int(tick * 2 ** 23), 2 ** 23)
err = float(tick - stored)
assert 9.0e-8 < err < 1.0e-7
hours = [1, 8, 20, 48, 100]
drift = {h: err * h * 3600 * 10 for h in hours}
SCUD = 1676
facts = dict(err="%.3g" % err, d100=round(drift[100], 2), d8=round(drift[8] * 1000), m100=round(drift[100] * SCUD), m8=round(drift[8] * SCUD), bits=23)
f = Fig(300, 236)
f.text(150, 12, "0.1 s chopped: %.2e s lost per tick" % err, size=10.5, color=NAVY, bold=True)
mx = drift[100]
for i, h in enumerate(hours):
    y = 30 + i * 30
    f.text(8, y + 11, "%d h" % h, size=10.5, color=NAVY, bold=True, anchor="start", vmid=True)
    w = max(drift[h] / mx * 120, 3)
    f.box(46, y, w, 22, "", fill="#fecaca" if h >= 20 else "#fde68a", stroke=SLATE, r=3, sw=1)
    f.text(52 + w, y + 11, "%.0f ms = %.0f m" % (drift[h] * 1000, drift[h] * SCUD), size=10.5, color=NAVY, bold=True, anchor="start", vmid=True)
f.text(150, 192, "clock error x target speed 1,676 m/s", size=10.5, color=SLATE)
f.text(150, 210, "tracking window is lost after long uptime", size=10.5, color=RED, bold=True)
f.text(150, 226, "fix: reboot, or exact arithmetic", size=10.5, color=TEAL, bold=True)
```

## 1.11 Floating-point numbers and machine epsilon

A computer stores a real number as a **floating-point** value: a sign, a fixed number of significant binary digits (the **mantissa**) and an exponent, $x = \pm\, m \times 2^{e}$. In IEEE 754 *double precision* the mantissa has 53 bits, which is about 15 to 16 significant decimal digits; in *single precision* it has 24 bits, about 7 digits. Only a finite set of numbers is representable, so every stored value is a rounded copy of the true one.

**Machine epsilon** $\varepsilon_{\text{mach}}$ is the gap between 1 and the next larger representable number. For doubles $\varepsilon_{\text{mach}} = 2^{-52} = 2.220446\times 10^{-16}$; for singles $2^{-23} = 1.192093\times 10^{-7}$. Rounding to nearest gives every stored number a relative error of at most $u = \varepsilon_{\text{mach}}/2$ (the **unit round-off**). Three consequences that matter in every method of this book:

- **Not every decimal is exact.** 0.1 has an endless binary expansion, so in double precision `0.1 + 0.2` evaluates to 0.30000000000000004, and a test `0.1 + 0.2 == 0.3` is false.
- **Small numbers vanish next to big ones.** `(1 + 1e-16) - 1` evaluates to 0 because $10^{-16}$ is below half of $\varepsilon_{\text{mach}}$: the addition returns exactly 1.
- **There is a range limit.** Doubles overflow near $1.8\times 10^{308}$ and underflow below $2.2\times 10^{-308}$.

::: key Consequence for the stopping rule
It is pointless to ask a double-precision iteration for a relative accuracy better than about $10^{-16}$; the table in Section 1.5 reaches the root to ten digits after three Newton steps and then the iterates simply stop changing. Asking for more only produces noise.
:::

## 1.12 Propagation of error and loss of significance

Suppose a quantity is computed from measured inputs, $z = f(x, y)$, and the inputs carry absolute errors $\Delta x$ and $\Delta y$. A first-order Taylor expansion gives the **error propagation formula**

$$\Delta z \;\lesssim\; \left|\frac{\partial f}{\partial x}\right| \Delta x \;+\; \left|\frac{\partial f}{\partial y}\right| \Delta y .$$

Special cases: for sums and differences the *absolute* errors add; for products and quotients the *relative* errors add; for a power $x^{k}$ the relative error is multiplied by $|k|$.

::: example Volume of a cylinder
A cylinder has radius $r = 2.50 \pm 0.02$ cm and height $h = 10.0 \pm 0.1$ cm. Its volume is $V = \pi r^{2} h = 196.35\ \text{cm}^3$. The relative error is $2\,(0.02/2.50) + 0.1/10.0 = 0.016 + 0.010 = 0.026$ (2.6 %), so $\Delta V \approx 0.026 \times 196.35 = 5.11\ \text{cm}^3$ and the volume lies between 191.24 and 201.45 cm³. The radius dominates because it is squared.
:::

**Loss of significance (cancellation).** Subtracting two nearly equal numbers cancels the leading digits that agree and leaves the doubtful trailing digits. The relative error of the difference can be huge even though each input was accurate.

::: example The small root of x² − 1000x + 1 = 0 in five-digit arithmetic
The exact roots are 999.999001 and 0.001000001. Work with five significant digits. The discriminant is $1000^{2} - 4 = 999996$, which rounds to $1.0000\times 10^{6}$, so $\sqrt{\ } = 1000.0$.

- **Direct formula.** The small root is $(1000 - 1000.0)/2 = 0$. Every digit is wrong: the subtraction of two nearly equal numbers destroyed the answer.
- **Rationalised formula.** Since the product of the roots is $c/a = 1$, the small root is $\dfrac{2c}{-b - \sqrt{b^{2}-4ac}}$ in magnitude, i.e. $\dfrac{2}{1000 + 1000.0} = 0.0010000$. Correct to five digits, and the subtraction has been replaced by an addition.
:::

The cure is algebra before arithmetic: rationalise, use a Taylor series, or use a trigonometric identity ($1 - \cos x = 2\sin^{2}(x/2)$ for small $x$) so that no two nearly equal numbers are subtracted.

**Condition and stability.** A *problem* is **ill-conditioned** if small changes in the data change the answer a lot (for instance, roots of a polynomial with clustered roots, Section 1.16, or the linear systems of Unit 4). An *algorithm* is **unstable** if rounding errors grow along the computation. Conditioning belongs to the problem; stability belongs to the method. A good algorithm cannot rescue an ill-conditioned problem, but a bad algorithm can ruin a well-conditioned one.

## 1.13 Accelerating convergence: Aitken's delta-squared and Steffensen's method

Fixed-point iterates $x_{n+1} = g(x_n)$ with $0 < |g'| < 1$ approach the root like a geometric progression, so the **error ratio is nearly constant**. If $x_{n+1} - \alpha \approx k\,(x_n - \alpha)$ for the same $k$ twice in a row, eliminating $k$ and solving for $\alpha$ gives **Aitken's $\Delta^{2}$ formula**:

$$\hat{x}_n = x_n - \frac{(x_{n+1} - x_n)^{2}}{x_{n+2} - 2x_{n+1} + x_n} .$$

**Steffensen's method** applies Aitken's formula immediately and restarts from the improved value: from $x_n$ compute $a = g(x_n)$, $b = g(a)$, then $x_{n+1} = x_n - \dfrac{(a - x_n)^{2}}{b - 2a + x_n}$. It needs no derivative yet converges quadratically.

::: example Accelerating $x = (x + 2)^{1/3}$ from $x_0 = 1.5$ (root 1.5213797068)
Plain iteration (Section 1.7) gives $x_1 = 1.5182945$, $x_2 = 1.5209353$, $x_3 = 1.5213157$, $x_4 = 1.5213705$: after four evaluations only four decimals are right. Aitken on the first three iterates gives $\hat{x}_0 = 1.5213808$ (error $1.1\times 10^{-6}$); on the next three it gives $1.5213797$.

| Steffensen step | $x_n$ | $a = g(x_n)$ | $b = g(a)$ | $x_{n+1}$ | error |
|---|---|---|---|---|---|
| 0 | 1.50000000 | 1.51829449 | 1.52093526 | 1.5213807618 | 1.05e-06 |
| 1 | 1.52138076 | 1.52137986 | 1.52137973 | 1.5213797068 | 2.4e-15 |

Two Steffensen steps (four evaluations of $g$ in all) reach double-precision accuracy, which plain iteration needs 15 steps for.
:::

::: caution When Aitken fails
If the denominator $x_{n+2} - 2x_{n+1} + x_n$ becomes 0 (the iterates have already converged, or $g' \approx 1$) the formula divides by zero. Stop as soon as $|x_{n+2} - x_{n+1}|$ is below the tolerance, before forming the quotient. A third Steffensen step on this example would divide $0/0$ for exactly that reason.
:::

## 1.14 Multiple roots and the modified Newton method

A root $\alpha$ has **multiplicity** $m$ if $f(x) = (x - \alpha)^{m} h(x)$ with $h(\alpha) \ne 0$; equivalently $f(\alpha) = f'(\alpha) = \dots = f^{(m-1)}(\alpha) = 0$. At a multiple root the graph touches the axis instead of crossing it, so bisection and false position (which need a sign change) cannot see an even-multiplicity root at all, and Newton's method **loses its quadratic speed**: near the root $f$ and $f'$ both tend to 0 and the error ratio tends to $(m - 1)/m$, i.e. the method is only linear (halving the error when $m = 2$).

Two repairs, both restoring quadratic convergence:

1. **Known multiplicity:** $x_{n+1} = x_n - m\,\dfrac{f(x_n)}{f'(x_n)}$.
2. **Unknown multiplicity:** apply Newton to $u(x) = f(x)/f'(x)$, which has the same roots but all of them *simple*:
$$x_{n+1} = x_n - \frac{f(x_n)\,f'(x_n)}{[f'(x_n)]^{2} - f(x_n)\,f''(x_n)} .$$

::: example $f(x) = x^3 - 3x + 2 = (x - 1)^{2}(x + 2)$, double root at 1, start $x_0 = 2$
Ordinary Newton: 1.555556, 1.297907, 1.155390, 1.079562, 1.040288, 1.020277, 1.010172, 1.005095. The error halves every step (0.556, 0.298, 0.155, 0.0796, 0.0403, ...), so eight steps give only two decimals.

Modified Newton with $m = 2$:

| $n$ | $x_n$ | $x_{n+1} = x_n - 2f/f'$ | error of $x_{n+1}$ |
|---|---|---|---|
| 0 | 2.00000000 | 1.1111111111 | 1.11e-01 |
| 1 | 1.11111111 | 1.0019493177 | 1.95e-03 |
| 2 | 1.00194932 | 1.0000006327 | 6.3e-07 |
| 3 | 1.00000063 | 1.0000000002 | 1.6e-10 |

Quadratic again: the error is roughly squared each step. The $f/f'$ method with the same start gives 0.909091, 0.998536, 0.9999996, 0.9999999996. Note the last modified-Newton iterate would fall back to $4.8\times 10^{-7}$ if one more step were taken: $f$ and $f'$ are both of size $10^{-10}$ or less there and their ratio is dominated by round-off, a warning that multiple roots are intrinsically ill-conditioned.
:::

```svgfig label="1.3" caption="Newton's method at the double root of $x^{3} - 3x + 2$ from $x_0 = 2$ (error on a log scale). Ordinary Newton gains only a factor of two per step (a straight line of slope about $-0.3$); with the multiplicity factor $m = 2$ the error falls quadratically and reaches $10^{-10}$ in four steps."
import math
f = Fig(560, 230)
ax = Axes(f, 56, 14, 520, 170, (0, 8), (-11, 0.5))
ax.grid(1, 2)
ax.axes("", "")
g = lambda x: x**3 - 3 * x + 2
gp = lambda x: 3 * x * x - 3
def lg(e): return max(-11, math.log10(max(e, 1e-12)))
def run(m, n):
    x = 2.0; P = [(0, lg(1.0))]
    for k in range(1, n + 1):
        x = x - m * g(x) / gp(x); P.append((k, lg(abs(x - 1))))
    return P
for P, col in ((run(1, 8), AMBER), (run(2, 4), RED)):
    for (n1, e1), (n2, e2) in zip(P, P[1:]):
        ax.curve(lambda t, n1=n1, e1=e1, n2=n2, e2=e2: e1 + (e2 - e1) * (t - n1) / (n2 - n1), n1, n2, color=col, sw=2.4)
    for n, e in P:
        f.circle(ax.X(n), ax.Y(e), 3.2, fill=col, stroke=col)
f.text(330, 56, "ordinary Newton: linear, ratio 1/2", size=10, color=AMBER, bold=True)
f.text(150, 160, "modified, m = 2: quadratic", size=10, color=RED, bold=True)
f.text(300, 206, "iteration number", size=10.5, color=SLATE)
f.text(300, 222, "log10 of the error", size=10, color=SLATE)
```

## 1.15 Polynomial roots: Horner's rule, deflation and Müller's method

**Horner's rule (synthetic division).** To evaluate $p(x) = a_0x^{n} + a_1x^{n-1} + \dots + a_n$ at $x = t$ use the nested form $p(t) = (\cdots((a_0 t + a_1)t + a_2)t + \cdots)t + a_n$. The running values are $b_0 = a_0$, $b_k = a_k + t\,b_{k-1}$, and the last one $b_n$ equals $p(t)$. It uses $n$ multiplications instead of about $n^{2}/2$ and is the way to evaluate polynomials in code. The earlier $b_k$ are exactly the coefficients of the **quotient** when $p(x)$ is divided by $(x - t)$, and $b_n$ is the remainder.

::: example Horner at t = 3 for p(x) = 2x³ − 6x² + 2x − 1
| | 2 | −6 | 2 | −1 |
|---|---|---|---|---|
| $t = 3$ | | 6 | 0 | 6 |
| $b_k$ | 2 | 0 | 2 | 5 |

So $p(3) = 5$ and $p(x) = (x - 3)(2x^{2} + 2) + 5$.
:::

Applying the same scheme again to the $b_k$ gives $p'(t)$, so one pass of "Horner twice" supplies both $p$ and $p'$ for a Newton step. Once a root $r$ is found, the quotient is a polynomial of one lower degree (**deflation**) and the search continues on it.

::: example Newton with Horner on p(x) = x³ − 6x² + 11x − 6 from x₀ = 0.5
| $n$ | $x_n$ | $p(x_n)$ | $p'(x_n)$ | $x_{n+1}$ |
|---|---|---|---|---|
| 0 | 0.50000000 | −1.875000 | 5.750000 | 0.82608696 |
| 1 | 0.82608696 | −0.443823 | 3.134216 | 0.96769287 |
| 2 | 0.96769287 | −0.067779 | 2.196974 | 0.99854405 |
| 3 | 0.99854405 | −0.002918 | 2.008742 | 0.99999683 |
| 4 | 0.99999683 | −0.000006 | 2.000019 | 1.00000000 |

The root is 1. Horner at $t = 1$ gives the quotient coefficients 1, −5, 6 and remainder 0, so the deflated quadratic is $x^{2} - 5x + 6 = (x - 2)(x - 3)$ with roots 2 and 3.
:::

::: caution Deflation order matters
Deflation passes the rounding error of each root into the quotient. Remove roots in **increasing order of magnitude** (smallest first) for stability, and polish every deflated root by a few Newton steps on the *original* polynomial.
:::

**Müller's method** generalises the secant method. The secant method fits a *line* through two points; Müller fits a *parabola* through three, $x_0, x_1, x_2$, and takes the nearer zero of the parabola as $x_3$. Put $h_1 = x_1 - x_0$, $h_2 = x_2 - x_1$, $\delta_1 = \dfrac{f(x_1) - f(x_0)}{h_1}$, $\delta_2 = \dfrac{f(x_2) - f(x_1)}{h_2}$. Then

$$A = \frac{\delta_2 - \delta_1}{h_2 + h_1},\quad B = A h_2 + \delta_2,\quad C = f(x_2),\quad x_3 = x_2 - \frac{2C}{B \pm \sqrt{B^{2} - 4AC}} ,$$

where the sign is chosen to make the denominator larger in magnitude. The order of convergence is about 1.84. The special value of Müller's method is that a negative discriminant produces a **complex** $x_3$, so it can find complex roots of a real function starting from real guesses, which Newton and secant cannot.

::: example Müller on x³ − x − 2 from x₀ = 1, x₁ = 1.5, x₂ = 2
| $n$ | $x_0$ | $x_1$ | $x_2$ | $A$ | $B$ | $C$ | $x_3$ | error |
|---|---|---|---|---|---|---|---|---|
| 0 | 1.000000 | 1.500000 | 2.000000 | 4.500000 | 10.500000 | 4.000000 | 1.52051760 | 8.6e-04 |
| 1 | 1.500000 | 2.000000 | 1.520518 | 5.020518 | 5.945759 | −0.005121 | 1.52137823 | 1.5e-06 |
| 2 | 2.000000 | 1.520518 | 1.521378 | 5.041896 | 5.944187 | −0.000009 | 1.52137971 | 1.0e-10 |

Three steps give ten correct digits: faster than the secant method (compare Section 1.6) at the price of a square root per step. The fitted coefficients approach the Taylor coefficients at the root: with $f''(\alpha) = 6\alpha = 9.13$ and $f'(\alpha) = 5.94$, the next row of the run has $A = 4.563 \approx f''/2$ and $B = 5.944 \approx f'$.
:::

```svgfig label="1.4" caption="One Müller step for $x^{3} - x - 2$. The cubic (navy) is replaced by the parabola (red) through the three starting points (1, -2), (1.5, -0.125) and (2, 4); the parabola's zero near 1.5205 is already within $10^{-3}$ of the true root 1.52138. The secant line through the last two points (dashed) crosses at 1.515."
f = Fig(380, 250)
ax = Axes(f, 40, 14, 340, 190, (0.9, 2.1), (-3, 5))
ax.grid(0.2, 1)
ax.axes("", "")
g = lambda x: x**3 - x - 2
ax.curve(g, 0.9, 2.1, color=NAVY, sw=2.2)
x0, x1, x2 = 1.0, 1.5, 2.0
y0, y1, y2 = g(x0), g(x1), g(x2)
def par(x):
    return y0 * (x - x1) * (x - x2) / ((x0 - x1) * (x0 - x2)) + y1 * (x - x0) * (x - x2) / ((x1 - x0) * (x1 - x2)) + y2 * (x - x0) * (x - x1) / ((x2 - x0) * (x2 - x1))
ax.curve(par, 0.9, 2.1, color=RED, sw=2)
ax.curve(lambda x: y1 + (y2 - y1) / (x2 - x1) * (x - x1), 1.2, 2.05, color=SLATE, sw=1.4)
for x, y in ((x0, y0), (x1, y1), (x2, y2)):
    f.circle(ax.X(x), ax.Y(y), 4, fill=AMBER, stroke=SLATE)
f.circle(ax.X(1.5205176), ax.Y(0), 4.5, fill=RED, stroke=RED)
f.text(110, 60, "cubic f", size=10.5, color=NAVY, bold=True)
f.text(230, 44, "parabola", size=10.5, color=RED, bold=True)
f.text(80, 150, "secant line", size=10, color=SLATE)
f.text(215, 232, "root near 1.5205", size=10, color=RED, bold=True)
```

## 1.16 Stopping criteria and the sensitivity of roots

**When to stop an iteration.** Three tests are in common use, and a reliable program checks more than one:

1. **Step size:** $|x_{n+1} - x_n| < \varepsilon$ (absolute), or $\dfrac{|x_{n+1} - x_n|}{|x_{n+1}|} < \varepsilon$ (relative, better when the root is large or tiny).
2. **Residual:** $|f(x_{n+1})| < \delta$. Small residual does *not* guarantee a small error when $f$ is flat near the root: for $f(x) = (x-1)^{5}$ the residual is only $10^{-10}$ at $x = 1.01$, a hundredth away from the root.
3. **Iteration cap:** $n \le N_{\max}$ (say 50) so that a divergent or cycling iteration terminates.

For bisection the error bound $(b - a)/2^{n}$ is known in advance, so no residual test is needed. For Newton and the secant method, the step size is a good estimate of the *previous* error because the convergence is superlinear.

**Roots can be extremely sensitive to the coefficients.** Take $p(x) = (x-1)(x-2)\cdots(x-6) = x^{6} - 21x^{5} + 175x^{4} - 735x^{3} + 1624x^{2} - 1764x + 720$. Change the coefficient $-21$ by only $10^{-4}$ (to $-21.0001$). The roots move to 0.999999, 2.000133, 2.997983, 4.008602, 4.986963 and 6.006420: the largest root shifts by 0.0064, about *sixty* times the change in the coefficient. The famous **Wilkinson polynomial**

$$W(x) = (x-1)(x-2)\cdots(x-20)$$

is far worse: changing the $x^{19}$ coefficient by $2^{-23} \approx 1.2\times 10^{-7}$ turns ten of the roots into complex pairs, with imaginary parts up to 2.8. The problem is ill-conditioned, so *no* algorithm in double precision (with relative data error $10^{-16}$) can be expected to find those roots reliably. The practical rule: be suspicious of high-degree polynomials with roots that lie close together or spread over a wide range, and prefer computing eigenvalues of the companion matrix (Unit 4, Section 4.6) to expanding the polynomial.

**Measuring the order of convergence.** If $e_n = |x_n - \alpha|$ is known, the order $p$ can be estimated from three successive errors by

$$p \approx \frac{\ln (e_{n+1}/e_n)}{\ln (e_n/e_{n-1})} .$$

For example, for Newton on $x^{3} - x - 2$ from $x_0 = 3$ the errors are 0.6325, 0.1805, 0.02087, 3.27e-04, 8.21e-08, 5.1e-15, and the estimates are 1.72, 1.93, 1.99, rising toward 2.

::: key Method summary after this section
Bisection: always works, linear. False position: bracketed, usually linear. Fixed point: linear with ratio $|g'|$; speed it up with Aitken/Steffensen. Newton: quadratic at a simple root, linear at a multiple root unless modified. Secant: order 1.618, no derivative. Müller: order 1.84, finds complex roots. Polynomials: use Horner for evaluation and deflate smallest first.
:::

## Formula and fact sheet

- Bisection: $c = \frac{a + b}{2}$; steps $n \geq \log_{2} \left( \frac{b - a}{\epsilon} \right)$.
- False position: $c = \frac{a f_{b} - b f_{a}}{f_{b} - f_{a}}$, with $f_{a}$ and $f_{b}$ the function values at the two ends.
- Newton: $x_{n+1} = x_{n} - \frac{f (x_{n})}{f' (x_{n})} ;\  e_{n+1} \approx \left[ \frac{f''}{2 f'} \right] e_{n}^{2}$.
- Secant: $x_{n+1} = x_{n} - \frac{f (x_{n}) (x_{n} - x_{n-1})}{f (x_{n}) - f (x_{n-1})}$; order 1.618.
- Fixed point: $x_{n+1} = g (x_{n})$, converges if $|g'| < 1$.
- Newton for systems: $J \cdot \Delta = - F$.
- Errors: absolute |x − x̂|; relative = absolute/|x|.
- Machine epsilon: double $2^{-52} = 2.22\times 10^{-16}$; unit round-off $u = \varepsilon_{\text{mach}}/2$.
- Error propagation: $\Delta z \lesssim |f_x|\,\Delta x + |f_y|\,\Delta y$; products add relative errors.
- Aitken: $\hat{x} = x_n - \dfrac{(x_{n+1} - x_n)^{2}}{x_{n+2} - 2x_{n+1} + x_n}$; Steffensen restarts after each Aitken step.
- Multiple root of multiplicity $m$: $x_{n+1} = x_n - m f/f'$ (quadratic again); unknown $m$: Newton on $f/f'$.
- Horner: $b_0 = a_0,\ b_k = a_k + t\,b_{k-1}$; $b_n = p(t)$. Müller: parabola through three points, order 1.84, complex roots possible.
- Order estimate: $p \approx \ln(e_{n+1}/e_n) / \ln(e_n/e_{n-1})$.

## Chapter summary

- Numerical root-finding replaces an impossible formula by a convergent repetition; errors (round-off, truncation, cancellation) set the achievable accuracy.
- Bisection and false position are safe but linear; Newton is quadratic but needs $f'$ and a good start; the secant method trades derivative for a 1.618 order; fixed-point iteration depends on $|g'| < 1$.
- Newton's method extends to systems through the Jacobian.
- Floating-point arithmetic has a unit round-off near $10^{-16}$; cancellation and error propagation explain why algebraic rearrangement matters before computing.
- Aitken and Steffensen accelerate fixed-point iteration; multiple roots slow Newton down to linear unless the multiplicity is used; Müller's method and Horner's rule handle polynomial roots, including complex ones.

## Practice

1. Define absolute, relative and percentage error. If $\sqrt{2}$ is approximated by 1.414, find all three.
2. How many bisection steps guarantee an error below $10^{-3}$ for a root in [1, 2]? Below $10^{-6}$?
3. Apply six steps of bisection to $x^{2} - 10 = 0$ on [3, 4]. What is the maximum possible error after six steps?
4. Apply Newton's method to $x^{2} - 10 = 0$ from $x_{0} = 3$. Why does it converge so fast?
5. Show that Newton's method applied to $f (x) = x^{\frac{1}{3}}$ diverges.
6. Show that the rearrangement $x = x^{3} - 2$ of $x^{3} - x - 2 = 0$ diverges while $x = (x + 2)^{\frac{1}{3}}$ converges.
7. Find the second iterate of the secant method for $x^{3} - x - 2 = 0$ from $x_{0} = 1 ,\  x_{1} = 2$.
8. Perform the first Newton step for $x^{2} + y^{2} = 4 ,\  x y = 1$ from (2, 0.5).
9. Explain why the false-position method may converge slowly.
10. Why is $\sqrt{10001} - \sqrt{10000}$ computed badly in short arithmetic, and how can the formula be rearranged?
11. What is machine epsilon? Why does `(1 + 1e-16) - 1` give 0 in double precision?
12. A cylinder has $r = 1.20 \pm 0.01$ and $h = 5.00 \pm 0.05$. Find the relative and absolute error in $V = \pi r^{2} h$.
13. Compute $\sqrt{1000^{2} + 1} - 1000$ in five-digit arithmetic directly and by rationalising. Compare with the true value.
14. Apply Aitken's formula to the iterates 1.5, 1.5182945, 1.5209353 of $x = (x + 2)^{1/3}$.
15. Newton's method is applied to $f(x) = (x - 2)^{3}$ from $x_0 = 3$. Find the first two iterates, the error ratio, and the result of the modified method with $m = 3$.
16. Use Horner's rule to find $p(2)$ and $p'(2)$ for $p(x) = x^{4} - 3x^{2} + 2x - 5$.
17. Take one Müller step for $f(x) = x^{2} + 1$ from $x_0 = 0,\ x_1 = 1,\ x_2 = 2$. What do you notice?
18. How many bisection steps are needed to locate a root in [1, 2] to within $10^{-5}$? Which stopping rule is this?
19. Three successive errors of an iteration are $10^{-2}$, $10^{-4}$ and $10^{-8}$. Estimate the order of convergence.
20. Why is the residual test $|f(x_n)| < \delta$ unreliable for $f(x) = (x - 1)^{5}$? Give a numerical example.

::: note Answers and worked solutions
**1.** Absolute error = |x − x̂|; relative = absolute/|x|; percentage = relative × 100. For $\sqrt{2} = 1.4142136$ and 1.414: absolute 0.0002136, relative 0.0001510, percentage 0.0151 %.

**2.** $n \geq \log_{2} \left( \frac{2 - 1}{\epsilon} \right)$: $\epsilon = 10^{-3}$ needs $n = 10 (2^{10} = 1024 > 1000) ;\  \epsilon = 10^{-6}$ needs $n = 20 (2^{20} \approx 10^{6})$.

**3.** The last midpoint is 3.171875. After six steps the root lies in an interval of width $1 / 2^{6} = 0.015625$, namely [3.156250, 3.171875], so the maximum possible error of the last midpoint is 0.015625 (the true $\sqrt{10} = 3.162278$, so the actual error is about 0.0096).

**4.** The iterates are 3.166667, 3.162281, 3.162278 (table in Section 1.5), so $\sqrt{10} \approx 3.162278$. Newton is quadratically convergent at a simple root: the correct digits double each step.

**5.** $f (x) = x^{\frac{1}{3}} ,\  f' (x) = \left( \frac{1}{3} \right) x^{- \frac{2}{3}}$, so $\frac{f}{f'} = 3 x$. Then $x_{n+1} = x_{n} - 3 x_{n} = - 2 x_{n}$: the magnitude doubles each step and the sign alternates; the iterates run away from the root 0 for every $x_{0} \neq 0$.

**6.** For $g (x) = x^{3} - 2 ,\  g' (\alpha) = 3 \alpha^{2} = 6.944 > 1$; starting at 1.5 the iterates are 1.375, 0.5996, -1.784, -7.682. For $g (x) = (x + 2)^{\frac{1}{3}} ,\  g' (\alpha) = 0.1440 < 1$, and the iterates converge as the table in Section 1.7 shows.

**7.** $x_{2} = 2 - \frac{f (2) (2 - 1)}{f (2) - f (1)} = 2 - \frac{4}{4 + 2} = 1.333333$. The next is $x_{3} = 1.462687$ (see Section 1.6 table).

**8.** $J (2 ,\  0.5) = \begin{bmatrix} 4 & 1 \\ 0.5 & 2 \end{bmatrix} ,\  f = (0.25 ,\  0) ,\  \Delta = (- 0.066667 ,\  0.016667)$, so $(x_{1} ,\  y_{1}) = (1.933333 ,\  0.516667)$.

**9.** For a convex or concave *f* on the bracket, the chord always crosses the axis on the same side of the root, so one end of the interval never moves and the other creeps up on the root linearly.

**10.** The two square roots are nearly equal, so their difference cancels the leading digits and leaves few significant ones. Multiply and divide by the conjugate: $\sqrt{10001} - \sqrt{10000} = \frac{1}{\sqrt{10001} + \sqrt{10000}} = 0.0049999$, which has no subtraction.

**11.** Machine epsilon is the gap between 1 and the next representable number: $2^{-52} = 2.22\times 10^{-16}$ in double precision. A number smaller than half of that is lost when added to 1, so $1 + 10^{-16}$ is stored as exactly 1 and the subtraction returns 0.

**12.** Relative error $= 2(0.01/1.20) + 0.05/5.00 = 0.016667 + 0.01 = 0.026667$ (2.67 %). $V = \pi(1.44)(5) = 22.620$, so $\Delta V \approx 0.026667 \times 22.620 = 0.603$.

**13.** Directly: $1000^{2} + 1 = 1\,000\,001 \to 1.0000\times 10^{6}$, so the root is 1000.0 and the difference is **0**. Rationalised: $\dfrac{1}{\sqrt{1000^{2}+1} + 1000} = \dfrac{1}{2000.0} = 0.00050000$. The true value is 0.00049999988.

**14.** $\Delta x_0 = 0.0182945$, $\Delta^{2}x_0 = 1.5209353 - 2(1.5182945) + 1.5 = -0.0156537$. So $\hat{x} = 1.5 - \dfrac{(0.0182945)^{2}}{-0.0156537} = 1.5 + 0.021381 = 1.521381$ (more precisely 1.5213808), against the true root 1.5213797: four evaluations of $g$ the plain way give only 1.52137.

**15.** $f/f' = (x - 2)/3$, so $x_{n+1} = x_n - (x_n - 2)/3$: $x_1 = 2.666667$, $x_2 = 2.444444$. The error ratio is $2/3 = (m-1)/m$ with $m = 3$: linear. The modified method $x_1 = 3 - 3(x_0 - 2)/3 = 2$ lands on the root in one step (the function is a pure cube).

**16.** Coefficients 1, 0, −3, 2, −5 with $t = 2$: $b = 1, 2, 1, 4, \mathbf{3}$, so $p(2) = 3$. Apply Horner again to 1, 2, 1, 4: $c = 1, 4, 9, \mathbf{22}$, so $p'(2) = 22$. Check: $4(8) - 6(2) + 2 = 22$.

**17.** $f$ is already a parabola, so the fitted parabola equals $f$: $h_1 = h_2 = 1$, $\delta_1 = 1$, $\delta_2 = 3$, $A = 1$, $B = 4$, $C = 5$. Then $B^{2} - 4AC = -4 < 0$ and $x_3 = 2 - \dfrac{2(5)}{4 + 2i} = 2 - (2 - i) = i$: **an exact complex root in one step**, from real starting points.

**18.** $n \ge \log_{2}(1/10^{-5}) = 16.61$, so 17 steps. This is the a-priori error bound of bisection; no residual test is needed.

**19.** $p \approx \dfrac{\ln(10^{-8}/10^{-4})}{\ln(10^{-4}/10^{-2})} = \dfrac{-9.21}{-4.61} = 2$: quadratic convergence.

**20.** $f$ is extremely flat near 1. At $x = 1.01$, which is 0.01 from the root, $f = (0.01)^{5} = 10^{-10}$, so a residual tolerance of $10^{-8}$ would accept an answer with a 1 % error. Use the step-size test as well, and prefer the modified method with $m = 5$.

:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Find the root of $x^{3} - 5 x + 1 = 0$ lying in [0, 1] by the bisection method (seven iterations). State how many iterations guarantee an error below $10^{- 3}$.**

*Check.* $f (0) = 1 > 0$ and $f (1) = - 3 < 0$, so a root lies in [0, 1] (Figure 1.1 shows the same idea for another function).

| *n* | a | *b* | $c = \frac{a + b}{2}$ | $f (c)$ |
|---|---|---|---|---|
| 1 | 0 | 1 | 0.500000 | -1.375000 |
| 2 | 0 | 0.5 | 0.250000 | -0.234375 |
| 3 | 0 | 0.25 | 0.125000 | +0.376953 |
| 4 | 0.125 | 0.25 | 0.187500 | +0.069092 |
| 5 | 0.1875 | 0.25 | 0.218750 | -0.083282 |
| 6 | 0.1875 | 0.21875 | 0.203125 | -0.007244 |
| 7 | 0.1875 | 0.203125 | 0.195312 | +0.030888 |

After seven steps the root lies in [0.195312, 0.203125]; the exact root is 0.201640. *Steps needed:* *n* >= log2((b - a)/epsilon) = $\log 2 (1 / 0.001) = 9.97$, so **10 iterations** guarantee an error below $10^{- 3}$. *Conclusion:* bisection is slow (linear) but always converges for a valid bracket.

**Q2 (5 marks). Use Newton-Raphson to solve $\cos x - x = 0$ starting with x0 = 1 (three iterations).**

*Formula.* $x (n + 1) = x (n) - \frac{f (x (n))}{f' (x (n))}$ with $f (x) = \cos x - x$ and $f' (x) = - \sin x - 1$.

| *n* | $x (n)$ | $f (x (n))$ | $f' (x (n))$ | $x (n + 1)$ |
|---|---|---|---|---|
| 0 | 1.000000 | -0.459698 | -1.841471 | 0.750364 |
| 1 | 0.750364 | -0.018923 | -1.681905 | 0.739113 |
| 2 | 0.739113 | -0.000046 | -1.673633 | 0.739085 |
| 3 | 0.739085 | -0.000000 | -1.673612 | 0.739085 |

The root is **0.739085** (the correct digits roughly double each step: 0, 1, 3, 6). *Why it is fast:* near a simple root the error satisfies $e (n + 1)$ is about $\left[ \frac{f''}{2 f'} \right] e (n)^{2}$ (quadratic convergence, Figure 1.2). *Cautions:* it fails when $f' (x) = 0$ and may diverge from a poor start. *Conclusion:* Newton is the preferred method when the derivative is available and the start is close.

**Q3 (10 marks). Compare the bisection, false-position, secant, Newton-Raphson and fixed-point methods for solving $f (x) = 0$. Illustrate with $x^{3} - x - 2 = 0$ and say how you would choose a method.**

*Introduction.* Root-finding methods fall into two families: **bracketing** methods (bisection, false position) that keep a root trapped inside an interval and always converge, and **open** methods (secant, Newton, fixed point) that start from one or two guesses, converge faster but can fail. Plate 1.1 shows Newton's tangent idea; Figure 1.1 shows bisection; Figure 1.2 compares their speeds.

*Methods.* (1) **Bisection:** midpoint of a sign-changing interval; error halves each step; *n* >= log2((b - a)/epsilon). (2) **False position:** the zero of the chord joining $(a ,\  f (a))$ and $(b ,\  f (b))$ replaces the midpoint; often faster but one end may stay fixed. (3) **Secant:** like false position without keeping the bracket, using the last two points; order about 1.62. (4) **Newton-Raphson:** $x - \frac{f}{f'}$; order 2; needs $f'$. (5) **Fixed point:** rewrite as $x = g (x)$ and iterate; converges when $|g' (x)| < 1$ near the root, with linear rate $|g'|$.

*Experiment.* Solving $x^{3} - x - 2 = 0$ (root 1.521380) to within $10^{- 6}$ (error, or residual for false position) needs: bisection on [1, 2] **19** iterations; false position **13**; fixed point $x = (x + 2)^{\frac{1}{3}}$ from 1.5 **6**; secant from 1 and 2 **6**; Newton from 1.5 only **2**.

| Method | Order | Needs bracket | Needs $f'$ | Iterations (this problem) | Main risk |
|---|---|---|---|---|---|
| Bisection | 1 (linear, 0.5) | Yes | No | 19 | Slow |
| False position | 1 | Yes | No | 13 | One end sticks |
| Fixed point | 1 (rate $a b s g'$) | No | No | 6 | May diverge |
| Secant | about 1.62 | No | No | 6 | May diverge |
| Newton-Raphson | 2 | No | Yes | 2 | $f' = 0$, bad start |

*Choice.* Use bisection (or false position) to obtain a safe bracket, then switch to Newton or secant to polish the answer; this hybrid is what library routines such as Brent's method do. Use the secant method when $f'$ is expensive or unavailable. *Conclusion:* there is no best method for every problem; safety and speed trade against each other, and good practice is to combine them.

**Q4 (10 marks). Explain why Newton's method slows down at a multiple root. Find the double root of $f(x) = x^{3} - 3x + 2$ from $x_0 = 2$ by (a) the ordinary Newton method and (b) the modified Newton method (four iterations each).**

*Introduction.* A root has multiplicity $m$ if $f = (x - \alpha)^{m}h(x)$ with $h(\alpha) \ne 0$. Newton's method derives from a tangent line; at a multiple root $f'(\alpha) = 0$ as well, so the tangent is nearly horizontal and the step $f/f'$ is only $\approx (x_n - \alpha)/m$. The error therefore shrinks by the factor $(m-1)/m$ per step (linear convergence, ratio 1/2 for $m = 2$), not squared.

*Ordinary Newton* ($f' = 3x^{2} - 3$): $x_1 = 2 - 4/9 = 1.555556$, $x_2 = 1.297907$, $x_3 = 1.155390$, $x_4 = 1.079562$. The errors 0.556, 0.298, 0.155, 0.080 halve each time, so after four steps only one decimal is right.

*Modified Newton* ($x_{n+1} = x_n - 2f/f'$):

| $n$ | $x_n$ | $x_{n+1}$ | error |
|---|---|---|---|
| 0 | 2.00000000 | 1.1111111111 | 1.11e-01 |
| 1 | 1.11111111 | 1.0019493177 | 1.95e-03 |
| 2 | 1.00194932 | 1.0000006327 | 6.3e-07 |
| 3 | 1.00000063 | 1.0000000002 | 1.6e-10 |

*Alternative.* If the multiplicity is unknown, apply Newton to $u = f/f'$: from $x_0 = 2$ it gives 0.909091, 0.998536, 0.9999996, 0.9999999996. *Conclusion:* the double root is $x = 1$; a multiplicity factor (or the $f/f'$ trick) restores quadratic convergence, and a multiple root is nevertheless ill-conditioned because $f$ and $f'$ both vanish there. Figure 1.3 shows the two error curves.
