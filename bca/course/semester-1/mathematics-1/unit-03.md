---
subject: Mathematics I
grade: BCA Semester 1
unit: 3
title: Differentiation
area: BCA 104 · Mathematics I · Unit 3
---

The **derivative** measures the instantaneous rate of change of a function: the slope of its tangent line, the speed of a moving object, the marginal cost of one more item. This unit defines it, builds the rules that make it mechanical, and extends them to implicit, logarithmic, parametric and higher-order cases.

::: key What this unit gives you
- The derivative as a limit; differentiability versus continuity.
- The full table of derivatives and the sum, product, quotient and chain rules.
- Implicit differentiation, logarithmic differentiation, parametric differentiation.
- Higher-order derivatives and the nth derivative of standard functions.
:::

## 3.1 The derivative from first principles

The **derivative** of f at x is

**f′(x) = lim (h→0) [f(x + h) − f(x)] / h**

if the limit exists. Geometrically it is the slope of the tangent to y = f(x) at x; it is also written dy/dx or Df(x).

::: example Worked example: first principles
**f(x) = x².** [f(x + h) − f(x)]/h = [(x + h)² − x²]/h = (2xh + h²)/h = 2x + h → **2x**.
**f(x) = √x.** [√(x + h) − √x]/h = h/(h(√(x + h) + √x)) = 1/(√(x + h) + √x) → **1/(2√x)**.
**f(x) = sin x.** [sin(x + h) − sin x]/h = sin x (cos h − 1)/h + cos x (sin h)/h → sin x · 0 + cos x · 1 = **cos x**.
:::

**Differentiability.** If f is differentiable at a, it is continuous at a. The converse is false: f(x) = |x| is continuous at 0 but has a corner there. The left slope is −1 and the right slope is +1, so f′(0) does not exist. A function also fails to be differentiable at a vertical tangent or a discontinuity.

## 3.2 Rules of differentiation

| Rule | Statement |
|---|---|
| Constant | (c)′ = 0 |
| Power | (xⁿ)′ = n xⁿ⁻¹ (any real n) |
| Constant multiple, sum | (c f)′ = c f′; (f ± g)′ = f′ ± g′ |
| Product | (fg)′ = f′g + fg′ |
| Quotient | (f/g)′ = (f′g − fg′)/g² |
| Chain | (f(g(x)))′ = f′(g(x)) · g′(x) |

**Table of standard derivatives**

| f(x) | f′(x) | f(x) | f′(x) |
|---|---|---|---|
| eˣ | eˣ | aˣ | aˣ ln a |
| ln x | 1/x | logₐ x | 1/(x ln a) |
| sin x | cos x | cos x | −sin x |
| tan x | sec²x | cot x | −cosec²x |
| sec x | sec x tan x | cosec x | −cosec x cot x |
| sin⁻¹x | 1/√(1 − x²) | cos⁻¹x | −1/√(1 − x²) |
| tan⁻¹x | 1/(1 + x²) | \|x\| | x/\|x\| (x ≠ 0) |

::: example Worked example: product, quotient, chain
**(a)** d/dx (x² sin x) = 2x sin x + x² cos x.
**(b)** d/dx [(x² + 1)/(x − 1)] = [2x(x − 1) − (x² + 1)]/(x − 1)² = **(x² − 2x − 1)/(x − 1)²**.
**(c)** d/dx sin(3x²) = cos(3x²) · 6x = **6x cos 3x²**.
**(d)** d/dx e^{x² + 1} = **2x e^{x² + 1}**.
**(e)** d/dx ln(x² + 4) = 2x/(x² + 4).
**(f)** d/dx √(1 + x³) = (1/2)(1 + x³)^{−1/2} · 3x² = **3x²/(2√(1 + x³))**.
**(g)** d/dx tan⁻¹(2x) = 2/(1 + 4x²).
:::

**Chain rule in layers.** For y = sin³(2x): outer cube, middle sine, inner 2x. y′ = 3 sin²(2x) · cos(2x) · 2 = 6 sin²(2x) cos(2x).

## 3.3 Implicit differentiation

When y is defined implicitly by an equation in x and y, differentiate both sides with respect to x, treating y as a function of x (so d/dx y² = 2y y′), then solve for y′.

::: example Worked example
**x² + y² = 25.** 2x + 2y y′ = 0, so y′ = −x/y. At (3, 4): slope −3/4, so the tangent is y − 4 = −(3/4)(x − 3), i.e. 3x + 4y = 25.

**x³ + y³ = 6xy.** 3x² + 3y² y′ = 6y + 6x y′, so y′(3y² − 6x) = 6y − 3x², giving **y′ = (2y − x²)/(y² − 2x)**.
:::

## 3.4 Logarithmic differentiation

For products and quotients with many factors, or for variable exponents f(x)^{g(x)}, take ln first: ln y = g ln f, then differentiate: y′/y = …

::: example Worked example
**y = xˣ.** ln y = x ln x, so y′/y = ln x + 1 and **y′ = xˣ (ln x + 1)**.
**y = x² (x + 1)³ / √(x − 2).** ln y = 2 ln x + 3 ln(x + 1) − ½ ln(x − 2), so y′/y = 2/x + 3/(x + 1) − 1/(2(x − 2)).
**y = (sin x)^{x}.** ln y = x ln sin x; y′ = (sin x)^x [ln sin x + x cot x].
:::

## 3.5 Parametric differentiation

If x = x(t), y = y(t), then **dy/dx = (dy/dt)/(dx/dt)** and **d²y/dx² = (d/dt (dy/dx)) / (dx/dt)**.

::: example Worked example
x = t², y = t³. dx/dt = 2t, dy/dt = 3t², so dy/dx = 3t/2. Then d²y/dx² = (3/2)/(2t) = **3/(4t)**.
For x = a cos t, y = a sin t (a circle): dy/dx = −cot t.
:::

## 3.6 Higher-order derivatives

The second derivative f″ = d/dx(f′) measures how the slope itself changes (concavity, acceleration). In general f⁽ⁿ⁾ is the nth derivative.

| y | yⁿ-th derivative |
|---|---|
| eᵃˣ | aⁿ eᵃˣ |
| sin x | sin(x + nπ/2) |
| cos x | cos(x + nπ/2) |
| (ax + b)ᵐ | m(m − 1)…(m − n + 1) aⁿ (ax + b)^{m − n} |
| ln(ax + b) | (−1)ⁿ⁻¹ (n − 1)! aⁿ/(ax + b)ⁿ |
| 1/(x + a) | (−1)ⁿ n!/(x + a)ⁿ⁺¹ |

::: example Worked example
**y = x³ − 4x² + 5x:** y′ = 3x² − 8x + 5, y″ = 6x − 8, y‴ = 6, y⁽⁴⁾ = 0.
**y = e^{2x}:** y⁽ⁿ⁾ = 2ⁿ e^{2x}; the 5th derivative is 32 e^{2x}.
**y = sin x:** y″ = −sin x, y⁗ = sin x (period 4).
**If y = a cos(ln x) + b sin(ln x), show x² y″ + x y′ + y = 0.** y′ = (−a sin(ln x) + b cos(ln x))/x, so x y′ = −a sin + b cos. Differentiate: y′ + x y″ = (−a cos − b sin)/x, so x y′ + x² y″ = −y. Hence x² y″ + x y′ + y = 0. ∎
:::

**Leibniz's theorem** for the nth derivative of a product: (uv)⁽ⁿ⁾ = Σ C(n, k) u⁽ⁿ⁻ᵏ⁾ v⁽ᵏ⁾. For (x² e^{x})″: u = x², v = eˣ, giving x² eˣ + 2(2x) eˣ + 2 eˣ = (x² + 4x + 2) eˣ.

## Formula and fact sheet

- f′(x) = lim [f(x + h) − f(x)]/h.
- (xⁿ)′ = nxⁿ⁻¹; (eˣ)′ = eˣ; (ln x)′ = 1/x; (sin x)′ = cos x; (cos x)′ = −sin x; (tan x)′ = sec²x.
- (fg)′ = f′g + fg′; (f/g)′ = (f′g − fg′)/g²; chain: f′(g)·g′.
- Implicit: differentiate both sides, y′ appears with each y.
- Log differentiation for f^g: y′ = y (g′ ln f + g f′/f).
- Parametric: dy/dx = ẏ/ẋ.
- Differentiable ⇒ continuous (not conversely).

## Chapter summary

- The derivative is the limit of difference quotients, equal to the slope of the tangent.
- A small table plus four rules (sum, product, quotient, chain) handles nearly every function.
- Implicit, logarithmic and parametric methods cover curves not written as y = f(x).
- Higher derivatives and nth-derivative formulas appear in series and in applications.

## Practice

1. Differentiate from first principles f(x) = 1/x.
2. Differentiate: (a) x³ e^{x}, (b) (ln x)/x², (c) sin(x²) cos(3x), (d) tan⁻¹(x²).
3. Differentiate y = (1 + x²)^{5} and y = √(sin x + cos x).
4. Find dy/dx if x² y + y³ = 10 at (1, 2).
5. Differentiate y = x^{sin x}.
6. If x = 2 cos t, y = 3 sin t find dy/dx and d²y/dx².
7. Find the nth derivative of y = 1/(x + 2) and of y = sin 3x.
8. Prove that if y = e^{x} sin x then y″ − 2y′ + 2y = 0.
9. Find the point on y = x² − 4x + 5 where the tangent is parallel to the x-axis.
10. Is f(x) = |x − 1| differentiable at 1? Justify.

::: note Answers and worked solutions
**1.** [1/(x + h) − 1/x]/h = −h/(h x(x + h)) = −1/(x(x + h)) → **−1/x²**.
**2.** (a) **x²eˣ(3 + x)**. (b) (1/x · x² − ln x · 2x)/x⁴ = **(1 − 2 ln x)/x³**. (c) **2x cos(x²) cos 3x − 3 sin(x²) sin 3x**. (d) **2x/(1 + x⁴)**.
**3.** **10x(1 + x²)⁴**; **(cos x − sin x)/(2√(sin x + cos x))**.
**4.** 2xy + x² y′ + 3y² y′ = 0, so y′ = −2xy/(x² + 3y²). At (1, 2): −4/(1 + 12) = **−4/13**. (Check: 1·2 + 8 = 10 ✓.)
**5.** ln y = sin x · ln x, y′ = x^{sin x} [cos x ln x + sin x / x].
**6.** dy/dx = 3 cos t/(−2 sin t) = **−(3/2) cot t**. d²y/dx² = [(3/2) cosec²t]/(−2 sin t) = **−(3/4) cosec³t**.
**7.** (−1)ⁿ n!/(x + 2)ⁿ⁺¹; **3ⁿ sin(3x + nπ/2)**.
**8.** y′ = eˣ(sin x + cos x), y″ = eˣ(2 cos x). Then y″ − 2y′ + 2y = eˣ[2 cos x − 2 sin x − 2 cos x + 2 sin x] = 0. ∎
**9.** y′ = 2x − 4 = 0 ⇒ x = 2, y = 1: **(2, 1)**.
**10.** No. Left slope −1, right slope +1, so the two one-sided derivatives differ at the corner x = 1 although f is continuous there.
:::
