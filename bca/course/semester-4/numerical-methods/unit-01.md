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

All iteration tables in this book were produced by running the programs in `bca/tools/check_numerical.py`; nothing is typed by hand. Arithmetic is done in double precision and shown to six decimals.

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

## Formula and fact sheet

- Bisection: $c = \frac{a + b}{2}$; steps $n \geq \log_{2} \left( \frac{b - a}{\epsilon} \right)$.
- False position: $c = \frac{a f (b) - b f (a)}{f (b) - f (a)}$.
- Newton: $x_{n+1} = x_{n} - \frac{f (x_{n})}{f' (x_{n})} ;\  e_{n+1} \approx \left[ \frac{f''}{2 f'} \right] e_{n}^{2}$.
- Secant: $x_{n+1} = x_{n} - \frac{f (x_{n}) (x_{n} - x_{n-1})}{f (x_{n}) - f (x_{n-1})}$; order 1.618.
- Fixed point: $x_{n+1} = g (x_{n})$, converges if $|g'| < 1$.
- Newton for systems: $J \cdot \Delta = - F$.
- Errors: absolute |x − x̂|; relative = absolute/|x|.

## Chapter summary

- Numerical root-finding replaces an impossible formula by a convergent repetition; errors (round-off, truncation, cancellation) set the achievable accuracy.
- Bisection and false position are safe but linear; Newton is quadratic but needs $f'$ and a good start; the secant method trades derivative for a 1.618 order; fixed-point iteration depends on $|g'| < 1$.
- Newton's method extends to systems through the Jacobian.

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
