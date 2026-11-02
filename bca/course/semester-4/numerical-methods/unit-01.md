---
subject: Numerical Methods
grade: BCA Semester 4
unit: 1
title: Solution of Nonlinear Equations
hours: 10
area: BCA 253 · Numerical Methods · Unit 1
---

Most equations that arise in engineering have no formula for their solution. There is no closed form for the root of x³ − x − 2 = 0 that you would want to use, and none at all for cos x = x. **Numerical methods** find an approximate answer to any wanted accuracy by repeating a simple calculation. This unit covers the errors that creep in and the classical root-finding methods.

::: key What this unit gives you
- Types of equations and errors in computing (round-off, truncation, absolute, relative).
- Bisection, false position, Newton–Raphson and secant methods with complete iteration tables.
- Fixed-point iteration and its convergence condition; Newton's method for a system of two nonlinear equations.
- Order of convergence and how to choose a method.
:::

All iteration tables in this book were produced by running the programs in `bca/tools/check_numerical.py`; nothing is typed by hand. Arithmetic is done in double precision and shown to six decimals.

## 1.1 Types of equations and locating roots

An **algebraic** equation is a polynomial equation (x³ − x − 2 = 0). A **transcendental** equation involves trigonometric, exponential or logarithmic functions (eˣ = 3x, cos x = x). A **root** (zero) of f is a number α with f(α) = 0.

**Intermediate value theorem.** If f is continuous on [a, b] and f(a)·f(b) < 0, then f has at least one root in (a, b). This sign change is how we **bracket** a root: tabulate f at convenient points and look for a sign change. For f(x) = x³ − x − 2 we have f(1) = −2 and f(2) = +4, so a root lies in (1, 2). The exact root, correct to ten decimals, is α = 1.5213797068.

## 1.2 Errors in computing

If the true value is *x* and the approximation is *x̂*:

- **Absolute error** E = |x − x̂|.
- **Relative error** Eᵣ = |x − x̂| / |x|; **percentage error** = Eᵣ × 100.
- A number is correct to *n* **significant digits** if its relative error is below 5 × 10⁻ⁿ.

::: example Errors in approximating √2
√2 = 1.4142136. Using x̂ = 1.414: E = 0.0002136, Eᵣ = 0.0001510, percentage error = 0.0151 %. The approximation is correct to four significant digits since Eᵣ < 5 × 10⁻⁴.
:::

### Sources of error

1. **Inherent (input) error**: measurement or data error before the computation starts.
2. **Round-off error**: a computer stores numbers with finite digits. Adding 0.3333 three times gives 0.9999, not 1. Double precision carries about 16 significant digits; single precision about 7.
3. **Truncation error**: an infinite process (series, limit) is cut short. Approximating eˣ at x = 0.5 by the first three Taylor terms gives 1.625000, and by four terms gives 1.645833, whereas the true value is 1.648721. The truncation errors are 0.023721 and 0.002888; each extra term cuts the error by roughly a factor of ten here.
4. **Propagation of error**: errors in the inputs grow or shrink through the operations. Subtracting nearly equal numbers (**cancellation**) is the worst case.

::: example Cancellation destroys digits
Compute √10001 − √10000 with five-significant-digit arithmetic. √10001 rounds to 100.00 and √10000 = 100.00, so the difference is 0.00000, all accuracy lost; the true value is 0.0049999. Rewriting algebraically as 1 / (√10001 + √10000) avoids the subtraction and gives 0.0049999 with the same five-digit arithmetic. Good numerical practice is to rearrange formulas to avoid subtracting nearly equal numbers.
:::

For a sum or difference the absolute errors add; for a product or quotient the *relative* errors add. For a function, the error is about |f′(x)|·Δx.

## 1.3 The bisection method

**Idea.** Keep an interval [a, b] with f(a)·f(b) < 0. Take the midpoint c = (a + b)/2. Replace b by c if f(a)·f(c) < 0, otherwise replace a by c. The interval halves each time.

**Algorithm.** (1) Choose a, b with f(a)f(b) < 0 and a tolerance ε. (2) c = (a + b)/2. (3) If f(c) = 0 or (b − a)/2 < ε, stop: c is the root. (4) If f(a)f(c) < 0, set b = c; else set a = c. (5) Go to 2.

**Error bound.** After *n* steps the root lies in an interval of length (b − a)/2ⁿ, so the number of steps needed for accuracy ε is **n ≥ log₂((b − a)/ε)**. For [1, 2] this is n ≥ 10 for ε = 10⁻³ and n ≥ 20 for ε = 10⁻⁶.

::: example Bisection on x³ − x − 2 = 0, [1, 2]
| n | a | b | c = (a+b)/2 | f(c) |
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

After ten steps c = 1.520508. The true error is 0.000872, within the guaranteed bound 1/2¹⁰ = 0.000977. Note that f(c) does not shrink steadily, but the bracketing interval always halves; that is what makes the method foolproof.
:::

::: example Square root of 10 by bisection: x² − 10 = 0 on [3, 4]
| n | a | b | c | f(c) |
|---|---|---|---|---|
| 1 | 3.000000 | 4.000000 | 3.500000 | +2.250000 |
| 2 | 3.000000 | 3.500000 | 3.250000 | +0.562500 |
| 3 | 3.000000 | 3.250000 | 3.125000 | -0.234375 |
| 4 | 3.125000 | 3.250000 | 3.187500 | +0.160156 |
| 5 | 3.125000 | 3.187500 | 3.156250 | -0.038086 |
| 6 | 3.156250 | 3.187500 | 3.171875 | +0.060791 |

After six steps the last midpoint is 3.171875 and, since f(c) > 0 there, the root lies in [3.156250, 3.171875] (width 1/2⁶ = 0.015625); the true value is 3.162278.
:::

**Properties.** Always converges if f is continuous and the bracket is valid; simple; **linear** convergence (one binary digit per step); slow; cannot find roots of even multiplicity (no sign change, such as x² = 0).

## 1.4 The method of false position (regula falsi)

Instead of the midpoint, use the point where the **chord** joining (a, f(a)) and (b, f(b)) crosses the x-axis:

**c = (a·f(b) − b·f(a)) / (f(b) − f(a))**

and keep the sub-interval whose ends still have opposite signs.

::: example False position on x³ − x − 2 = 0, [1, 2]
| n | a | b | c | f(c) |
|---|---|---|---|---|
| 1 | 1.000000 | 2.000000 | 1.333333 | -0.962963 |
| 2 | 1.333333 | 2.000000 | 1.462687 | -0.333339 |
| 3 | 1.462687 | 2.000000 | 1.504019 | -0.101818 |
| 4 | 1.504019 | 2.000000 | 1.516331 | -0.029895 |
| 5 | 1.516331 | 2.000000 | 1.519919 | -0.008675 |
| 6 | 1.519919 | 2.000000 | 1.520957 | -0.002509 |
| 7 | 1.520957 | 2.000000 | 1.521258 | -0.000725 |

After seven steps c = 1.521258; the error, about 1.2 × 10⁻⁴, is already smaller than bisection's after ten steps (8.7 × 10⁻⁴). But notice that the end b = 2 never moves: because f is convex on this interval, the chord always lands on the same side of the root, so the approximations creep up from one side and each step shrinks the error only by a constant factor (about 0.29 here). That one-sided, merely linear behaviour is the usual weakness of the method; modified versions halve the stuck end's function value to repair it.
:::

## 1.5 The Newton–Raphson method

**Idea.** Replace f by its tangent line at the current guess *xₙ* and take the tangent's zero as the next guess. From the tangent y = f(xₙ) + f′(xₙ)(x − xₙ) setting y = 0:

**xₙ₊₁ = xₙ − f(xₙ) / f′(xₙ)**

The same formula follows from the first-order Taylor expansion f(α) ≈ f(xₙ) + (α − xₙ)f′(xₙ) = 0.

::: example Newton on f(x) = x³ − x − 2, f′(x) = 3x² − 1, x₀ = 1.5
| n | xₙ | f(xₙ) | f′(xₙ) | xₙ₊₁ |
|---|---|---|---|---|
| 0 | 1.500000 | -0.125000 | 5.750000 | 1.521739 |
| 1 | 1.521739 | +0.002137 | 5.947070 | 1.521380 |
| 2 | 1.521380 | +0.000001 | 5.943790 | 1.521380 |
| 3 | 1.521380 | +0.000000 | 5.943789 | 1.521380 |

Two steps already give six correct decimals: the root is 1.521380. Compare ten bisection steps for three.
:::

::: example Square root of 10 by Newton (the "divide and average" rule)
For f(x) = x² − 10, xₙ₊₁ = xₙ − (xₙ² − 10)/(2xₙ) = ½(xₙ + 10/xₙ). Starting at x₀ = 3:

| n | xₙ | f(xₙ) | f′(xₙ) | xₙ₊₁ |
|---|---|---|---|---|
| 0 | 3.000000 | -1.000000 | 6.000000 | 3.166667 |
| 1 | 3.166667 | +0.027778 | 6.333333 | 3.162281 |
| 2 | 3.162281 | +0.000019 | 6.324561 | 3.162278 |

Three steps give 3.162278 to six decimals. This is the method calculators use for square roots.
:::

**Quadratic convergence.** Near a simple root the error satisfies eₙ₊₁ ≈ [f″(α)/(2f′(α))]·eₙ², i.e. the number of correct digits roughly **doubles** each step. For our cubic the constant is f″/(2f′) = 0.768. The actual errors of the iterates x₁ … x₄ were 2.14e-02, 3.59e-04, 9.92e-08, 7.55e-15 and the ratios eₙ₊₁/eₙ² were 0.786, 0.768, 0.768, settling at the predicted constant.

**Failure cases.** (1) f′(xₙ) = 0 makes the step undefined; a tiny f′ throws the iterate far away. (2) A poor starting guess can diverge or wander to another root. (3) Cycling: for f(x) = x³ − 2x + 2 starting at 0 the iterates alternate between 0 and 1. (4) For f(x) = x^(1/3), the step is xₙ₊₁ = xₙ − 3xₙ = −2xₙ, so it diverges from every starting point. (5) At a multiple root convergence drops to linear. Always start near the root, found by a bracketing sweep or a few bisection steps.

## 1.6 The secant method

Newton needs the derivative. The **secant method** replaces f′(xₙ) by the slope of the line through the last two points:

**xₙ₊₁ = xₙ − f(xₙ)(xₙ − xₙ₋₁) / (f(xₙ) − f(xₙ₋₁))**

It needs two starting values but **no bracket** and only one new function evaluation per step.

::: example Secant on x³ − x − 2 = 0, x₀ = 1, x₁ = 2
| n | xₙ₋₁ | xₙ | f(xₙ₋₁) | f(xₙ) | xₙ₊₁ |
|---|---|---|---|---|---|
| 0 | 1.000000 | 2.000000 | -2.000000 | +4.000000 | 1.333333 |
| 1 | 2.000000 | 1.333333 | +4.000000 | -0.962963 | 1.462687 |
| 2 | 1.333333 | 1.462687 | -0.962963 | -0.333339 | 1.531169 |
| 3 | 1.462687 | 1.531169 | -0.333339 | +0.058626 | 1.520926 |
| 4 | 1.531169 | 1.520926 | +0.058626 | -0.002693 | 1.521376 |
| 5 | 1.520926 | 1.521376 | -0.002693 | -0.000020 | 1.521380 |

After six steps x = 1.521380. The first step x₂ = 1.333333 equals the first false-position step, because both use the same chord; after that, the secant method always uses the two *latest* points and so is not held back by an old endpoint.
:::

The order of convergence is the golden ratio **p ≈ 1.618**: between linear and quadratic. Per function evaluation it can beat Newton, because Newton needs *two* evaluations (f and f′) per step.

## 1.7 Fixed-point iteration and convergence

Rewrite f(x) = 0 as **x = g(x)** and iterate xₙ₊₁ = g(xₙ). A root is a **fixed point** of g.

**Convergence theorem.** If g and g′ are continuous near the fixed point α and **|g′(x)| < 1** on an interval around α containing the starting value, the iteration converges to α, and the smaller |g′(α)|, the faster. Convergence is linear with ratio |g′(α)|. If |g′(α)| > 1 it diverges.

::: example x³ − x − 2 = 0 rearranged as x = (x + 2)^(1/3), x₀ = 1.5
| n | xₙ | xₙ₊₁ = (xₙ+2)^(1/3) | |error| |
|---|---|---|---|
| 0 | 1.500000 | 1.518294 | 3.09e-03 |
| 1 | 1.518294 | 1.520935 | 4.44e-04 |
| 2 | 1.520935 | 1.521316 | 6.40e-05 |
| 3 | 1.521316 | 1.521370 | 9.22e-06 |
| 4 | 1.521370 | 1.521378 | 1.33e-06 |
| 5 | 1.521378 | 1.521380 | 1.91e-07 |
| 6 | 1.521380 | 1.521380 | 2.75e-08 |

Here g′(α) = ⅓(α + 2)^(−2/3) = 0.1440, so the error shrinks by about that factor each step (compare the error column: 3.09e-03, 4.44e-04, ... ratio ≈ 0.14). Another rearrangement, x = x³ − 2, has |g′(α)| = 3α² = 6.944 > 1 and from x₀ = 1.5 the iterates are 1.375, 0.5996, -1.784, -7.682: it **diverges**, even though both rearrangements have the same root. The choice of g matters.
:::

## 1.8 Systems of nonlinear equations

For two unknowns, solve f₁(x, y) = 0, f₂(x, y) = 0 by **Newton's method**: at each step solve the linear system J(xₙ, yₙ)·(Δx, Δy)ᵀ = −(f₁, f₂)ᵀ, where J is the **Jacobian** of partial derivatives, and update xₙ₊₁ = xₙ + Δx, yₙ₊₁ = yₙ + Δy.

::: example x² + y² = 4 and xy = 1, starting from (2, 0.5)
f₁ = x² + y² − 4, f₂ = xy − 1; J = [[2x, 2y], [y, x]]. At (2, 0.5): J = [[4, 1], [0.5, 2]], (f₁, f₂) = (0.25, 0), and solving J·Δ = −f gives Δ = (-0.066667, 0.016667), so the next point is (1.933333, 0.516667).

| n | xₙ | yₙ | f₁ | f₂ | xₙ₊₁ | yₙ₊₁ |
|---|---|---|---|---|---|---|
| 0 | 2.000000 | 0.500000 | +0.250000 | +0.000000 | 1.933333 | 0.516667 |
| 1 | 1.933333 | 0.516667 | +0.004722 | -0.001111 | 1.931853 | 0.517637 |
| 2 | 1.931853 | 0.517637 | +0.000003 | -0.000001 | 1.931852 | 0.517638 |
| 3 | 1.931852 | 0.517638 | +0.000000 | -0.000000 | 1.931852 | 0.517638 |
| 4 | 1.931852 | 0.517638 | -0.000000 | +0.000000 | 1.931852 | 0.517638 |

The solution is (x, y) = (1.931852, 0.517638), which agrees with the exact answer ((√6 + √2)/2, (√6 − √2)/2). The number of correct digits doubles each step, as in the one-variable case.
:::

An alternative is **fixed-point iteration** on x = g₁(x, y), y = g₂(x, y), converging when the Jacobian of g has norm below 1.

## 1.9 Choosing a method

| Method | Needs | Order | Evaluations per step | Guaranteed? |
|---|---|---|---|---|
| Bisection | bracket | 1 (linear, ratio ½) | 1 f | yes |
| False position | bracket | 1 (often slow, one end stuck) | 1 f | yes |
| Secant | two starts | 1.618 | 1 f | no |
| Newton–Raphson | f′ and a start | 2 | 1 f + 1 f′ | no |
| Fixed point | g with |g′| < 1 | 1 (ratio |g′|) | 1 g | only if |g′| < 1 |

A practical strategy: bracket the root, take a few bisection steps, then finish with Newton or secant. A good program stops when |xₙ₊₁ − xₙ| < ε or |f(xₙ)| < ε, and also after a maximum number of iterations.

## Formula and fact sheet

- Bisection: c = (a + b)/2; steps n ≥ log₂((b − a)/ε).
- False position: c = (a f(b) − b f(a)) / (f(b) − f(a)).
- Newton: xₙ₊₁ = xₙ − f(xₙ)/f′(xₙ); eₙ₊₁ ≈ [f″/(2f′)]eₙ².
- Secant: xₙ₊₁ = xₙ − f(xₙ)(xₙ − xₙ₋₁)/(f(xₙ) − f(xₙ₋₁)); order 1.618.
- Fixed point: xₙ₊₁ = g(xₙ), converges if |g′| < 1.
- Newton for systems: J·Δ = −F.
- Errors: absolute |x − x̂|; relative = absolute/|x|.

## Chapter summary

- Numerical root-finding replaces an impossible formula by a convergent repetition; errors (round-off, truncation, cancellation) set the achievable accuracy.
- Bisection and false position are safe but linear; Newton is quadratic but needs f′ and a good start; the secant method trades derivative for a 1.618 order; fixed-point iteration depends on |g′| < 1.
- Newton's method extends to systems through the Jacobian.

## Practice

1. Define absolute, relative and percentage error. If √2 is approximated by 1.414, find all three.
2. How many bisection steps guarantee an error below 10⁻³ for a root in [1, 2]? Below 10⁻⁶?
3. Apply six steps of bisection to x² − 10 = 0 on [3, 4]. What is the maximum possible error after six steps?
4. Apply Newton's method to x² − 10 = 0 from x₀ = 3. Why does it converge so fast?
5. Show that Newton's method applied to f(x) = x^(1/3) diverges.
6. Show that the rearrangement x = x³ − 2 of x³ − x − 2 = 0 diverges while x = (x + 2)^(1/3) converges.
7. Find the second iterate of the secant method for x³ − x − 2 = 0 from x₀ = 1, x₁ = 2.
8. Perform the first Newton step for x² + y² = 4, xy = 1 from (2, 0.5).
9. Explain why the false-position method may converge slowly.
10. Why is √10001 − √10000 computed badly in short arithmetic, and how can the formula be rearranged?

::: note Answers and worked solutions
**1.** Absolute error = |x − x̂|; relative = absolute/|x|; percentage = relative × 100. For √2 = 1.4142136 and 1.414: absolute 0.0002136, relative 0.0001510, percentage 0.0151 %.
**2.** n ≥ log₂((2 − 1)/ε): ε = 10⁻³ needs n = 10 (2¹⁰ = 1024 > 1000); ε = 10⁻⁶ needs n = 20 (2²⁰ ≈ 10⁶).
**3.** The last midpoint is 3.171875. After six steps the root lies in an interval of width 1/2⁶ = 0.015625, namely [3.156250, 3.171875], so the maximum possible error of the last midpoint is 0.015625 (the true √10 = 3.162278, so the actual error is about 0.0096).
**4.** The iterates are 3.166667, 3.162281, 3.162278 (table in Section 1.5), so √10 ≈ 3.162278. Newton is quadratically convergent at a simple root: the correct digits double each step.
**5.** f(x) = x^(1/3), f′(x) = (1/3)x^(−2/3), so f/f′ = 3x. Then xₙ₊₁ = xₙ − 3xₙ = −2xₙ: the magnitude doubles each step and the sign alternates; the iterates run away from the root 0 for every x₀ ≠ 0.
**6.** For g(x) = x³ − 2, g′(α) = 3α² = 6.944 > 1; starting at 1.5 the iterates are 1.375, 0.5996, -1.784, -7.682. For g(x) = (x + 2)^(1/3), g′(α) = 0.1440 < 1, and the iterates converge as the table in Section 1.7 shows.
**7.** x₂ = 2 − f(2)(2 − 1)/(f(2) − f(1)) = 2 − 4/(4 + 2) = 1.333333. The next is x₃ = 1.462687 (see Section 1.6 table).
**8.** J(2, 0.5) = [[4, 1], [0.5, 2]], f = (0.25, 0), Δ = (-0.066667, 0.016667), so (x₁, y₁) = (1.933333, 0.516667).
**9.** For a convex or concave f on the bracket, the chord always crosses the axis on the same side of the root, so one end of the interval never moves and the other creeps up on the root linearly.
**10.** The two square roots are nearly equal, so their difference cancels the leading digits and leaves few significant ones. Multiply and divide by the conjugate: √10001 − √10000 = 1/(√10001 + √10000) = 0.0049999, which has no subtraction.
:::
