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

```svgfig label="3.1" caption="From secant to tangent for f(x) = x² at P(1, 1). The slope of the secant PQ is (f(1 + h) − f(1))/h. As h shrinks, Q slides down the curve towards P and the secant turns into the tangent, whose slope 2 is the derivative f′(1)."
f = Fig(740, 290)
a = Axes(f, 30, 14, 350, 255, (-0.5, 3.2), (-0.5, 7.5)); a.grid(1, 1).axes()
a.curve(lambda x: x * x, color=NAVY, sw=2.6)
a.curve(lambda x: 1 + 3.5 * (x - 1), -0.2, 2.9, color=AMBER, sw=1.6, dash=True)
a.curve(lambda x: 1 + 2.75 * (x - 1), -0.2, 2.9, color=TEAL, sw=1.6, dash=True)
a.curve(lambda x: 2 * x - 1, -0.3, 2.9, color=RED, sw=2.4)
a.pt(1, 1, "P(1, 1)", dx=8, dy=18); a.pt(2.5, 6.25, "Q₁", color=AMBER, dx=-8, dy=-2, anchor="end"); a.pt(1.75, 3.0625, "Q₂", color=TEAL, dx=-10, dy=6, anchor="end")
f.text(a.X(1.9), a.Y(2.0), "tangent: slope 2", size=10.5, color=RED, bold=True, anchor="start")
f.text(430, 28, "Slope of the secant PQ", size=12, color=NAVY, bold=True, anchor="start")
rows = [("h = 1.5", "Q = (2.5, 6.25)", "3.5"), ("h = 0.75", "Q = (1.75, 3.0625)", "2.75"), ("h = 0.1", "Q = (1.1, 1.21)", "2.1"), ("h = 0.01", "Q = (1.01, 1.0201)", "2.01"), ("h → 0", "Q → P", "2  (derivative)")]
for i, (h, q, s) in enumerate(rows):
    y = 40 + i * 42
    f.box(430, y, 90, 32, h, fill=BLUE, stroke=NAVY, color=NAVY, size=11, bold=True); f.box(526, y, 120, 32, q, fill=SOFT, stroke="#94a3b8", color=SLATE, size=9.5)
    f.box(652, y, 82, 32, s, fill=MINT if i == 4 else SAND, stroke=TEAL if i == 4 else AMBER, size=10 if i == 4 else 11.5, bold=True)
f.text(430, 270, "slope = ((1 + h)² − 1)/h = 2 + h  →  2", size=11, color=SLATE, anchor="start")
```

```photogrid label="3.1" cols="3" ratio="1.0" caption="Derivative = rate of change. (a) The speedometer of a car shows the derivative of distance with respect to time. (b) Isaac Newton (1643-1727) and (c) Gottfried Wilhelm Leibniz (1646-1716) developed calculus independently; the notation dy/dx is Leibniz's, the dot notation is Newton's."
@ photo id="bca104/speedo" cap="Speedometer: v = ds/dt"
fit 1.0
focus 0.5 0.5
call 0.5 0.93 0.5 0.62 "Reads ds/dt in km/h"
@ photo id="bca104/newton" cap="Isaac Newton"
fit 1.0
focus 0.5 0.6
@ photo id="bca104/leibniz" cap="G. W. Leibniz"
fit 1.0
focus 0.5 0.62
```

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

```svgfig label="3.2" caption="A function and its derivative, read together. For f(x) = x³ − 3x (top) the derivative is f′(x) = 3x² − 3 (bottom). Where f′ is positive f rises, where f′ is negative f falls, and where f′ = 0 (x = ±1) the graph of f has a flat tangent: a local maximum at x = −1 and a local minimum at x = 1."
f = Fig(740, 330)
a = Axes(f, 40, 12, 660, 140, (-2.3, 2.3), (-3.2, 3.2)); a.grid(1, 1).axes()
a.curve(lambda x: x**3 - 3 * x, color=NAVY, sw=2.6); a.pt(-1, 2, "local max (−1, 2)", dx=8, dy=-6); a.pt(1, -2, "local min (1, −2)", dx=-8, dy=18, anchor="end")
f.text(a.X(1.5), a.Y(2.8), "f(x) = x³ − 3x", size=11.5, color=NAVY, bold=True, anchor="start")
b = Axes(f, 40, 178, 660, 140, (-2.3, 2.3), (-3.5, 6.5)); b.grid(1, 2).axes()
b.curve(lambda x: 3 * x * x - 3, color=TEAL, sw=2.6); b.pt(-1, 0, "f′ = 0", dx=-8, dy=-8, anchor="end"); b.pt(1, 0, "f′ = 0", dx=8, dy=-8)
f.text(b.X(1.2), b.Y(5.6), "f′(x) = 3x² − 3", size=11.5, color=TEAL, bold=True, anchor="start")
for x in (-1, 1): f.line(a.X(x), a.Y(3.2), a.X(x), b.Y(-3.5), color=AMBER, sw=1.2, dash=True)
f.text(a.X(-1.9), b.Y(-1.7), "f′ > 0: f rising", size=10, color=TEAL, bold=True); f.text(a.X(0), b.Y(-2.4), "f′ < 0: f falling", size=10, color=TEAL, bold=True); f.text(a.X(1.9), b.Y(-1.7), "f′ > 0: rising", size=10, color=TEAL, bold=True)
```

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

```svgfig label="3.3" caption="Implicit differentiation on the circle x² + y² = 25. Differentiating both sides gives 2x + 2y·dy/dx = 0, so dy/dx = −x/y. At P(3, 4) the slope is −3/4, and the tangent is perpendicular to the radius OP (whose slope is 4/3)."
f = Fig(740, 300)
a = Axes(f, 20, 10, 280, 280, (-7, 7), (-7, 7)); a.grid(1, 1, labels=False).axes()
a.curve(lambda x: math.sqrt(25 - x * x), -5, 5, color=NAVY, sw=2.6, n=300); a.curve(lambda x: -math.sqrt(25 - x * x), -5, 5, color=NAVY, sw=2.6, n=300)
a.curve(lambda x: 4 - 0.75 * (x - 3), -1.5, 7, color=RED, sw=2.2); a.curve(lambda x: 4 * x / 3, 0, 3, color=TEAL, sw=2, dash=True)
a.pt(3, 4, "P(3, 4)", dx=8, dy=-8); a.pt(0, 0, "O", r=3, color=SLATE, dx=-8, dy=14, anchor="end")
f.text(a.X(4.2), a.Y(1.2), "tangent", size=11, color=RED, bold=True, anchor="start")
steps = [("1. Differentiate both sides with respect to x", "d/dx (x²) + d/dx (y²) = d/dx (25)"), ("2. Treat y as a function of x (chain rule)", "2x + 2y · dy/dx = 0"), ("3. Solve for dy/dx", "dy/dx = −x / y"), ("4. Put in the point (3, 4)", "slope m = −3/4"), ("5. Tangent line: y − 4 = m(x − 3)", "3x + 4y = 25")]
for i, (s, e) in enumerate(steps):
    y = 24 + i * 54
    f.box(330, y, 395, 46, "", fill=BLUE if i % 2 == 0 else SOFT, stroke="#cbd5e1")
    f.text(342, y + 18, s, size=10.5, color=NAVY, bold=True, anchor="start"); f.text(342, y + 36, e, size=11.5, color=SLATE, anchor="start")
```

## 3.7 Eight uses of derivatives

1. **Speed and acceleration.** If s(t) is the position of a vehicle, then v = ds/dt is its speed and a = dv/dt = d²s/dt² is its acceleration. A Kathmandu microbus driver feels the second derivative when the bus brakes at Koteshwor. Traffic engineers use these to set safe speed limits.
2. **Finding maximum profit and minimum cost.** A business writes profit as a function P(x) of the number of items and solves P′(x) = 0. A bakery in Butwal can find the number of cakes that earns most. The second derivative then confirms that the point is a maximum and not a minimum.
3. **Tangent lines and linear approximation.** Near a point a curve looks like its tangent, so f(x) ≈ f(a) + f′(a)(x − a). Calculators use this to find √4.02 ≈ 2 + 0.02/4 = 2.005 quickly. Graphics software draws smooth curves in the same way.
4. **Machine learning and gradient descent.** To train a model, a computer finds the minimum of an error function by moving against the derivative. A positive slope means "go left", a negative slope means "go right". This is how recommendation and speech systems learn.
5. **Related rates.** When one quantity changes, others linked to it change too. If water is pumped into a tank at a known rate, the derivative tells how fast the level rises. Municipal water engineers use it for the tanks of the Melamchi supply.
6. **Growth and decay models.** The derivative of a population or an investment tells how fast it grows. For P = P₀eᵏᵗ we get dP/dt = kP, so growth is proportional to size. This links directly to the differential equations in Unit 6.
7. **Curve sketching and optimisation in design.** The first derivative shows where a graph rises and falls, and the second shows its curvature (Figure 3.2). Designers use these to shape road curves, bridge cables and the packaging of a drink can.
8. **Sensitivity and economics.** The derivative of cost with respect to quantity is the marginal cost, the extra cost of one more unit. A hydropower plant uses marginal cost to decide how many turbines to run. In any formula, a large derivative warns that a small error in input gives a large error in output.

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

## Model answers: medium (5 marks) and long (10 marks) questions

**Q (5 marks). Find the derivative of f(x) = √x from first principles. Find also the slope of the curve at x = 4.**

The **derivative** of f at x is defined by the limit f′(x) = lim (h→0) [f(x + h) − f(x)] / h, provided the limit exists. It is the slope of the tangent line (Figure 3.1).

1. Write the difference quotient: [√(x + h) − √x] / h. Putting h = 0 gives 0/0, so we rationalise.
2. Multiply top and bottom by the conjugate √(x + h) + √x. The numerator becomes (x + h) − x = h.
3. The quotient is h / [h(√(x + h) + √x)] = 1 / (√(x + h) + √x) for h ≠ 0.
4. Let h → 0: the denominator tends to √x + √x = 2√x.

So **f′(x) = 1/(2√x)** for x > 0. At x = 4 the slope is 1/(2 × 2) = **1/4**, and the tangent line is y − 2 = ¼(x − 4). *Check:* between x = 4 and x = 4.04, √4.04 − √4 = 2.00998 − 2 = 0.00998, and 0.00998/0.04 ≈ 0.2495, close to 1/4.

**Q (5 marks). If x³ + y³ = 6xy, find dy/dx by implicit differentiation and the slope of the tangent at (3, 3).**

When y cannot be easily written as a function of x we differentiate both sides with respect to x, remembering that y depends on x, so d(y³)/dx = 3y² · dy/dx (chain rule).

1. Differentiate: 3x² + 3y² · dy/dx = 6y + 6x · dy/dx (the product rule is used on 6xy).
2. Collect the dy/dx terms on one side: 3y² · dy/dx − 6x · dy/dx = 6y − 3x².
3. Factor: dy/dx (3y² − 6x) = 6y − 3x².
4. Divide: **dy/dx = (2y − x²) / (y² − 2x)**.
5. At (3, 3): the numerator is 6 − 9 = −3 and the denominator is 9 − 6 = 3, so the slope is **−1**.

The point (3, 3) lies on the curve (27 + 27 = 54 = 6 × 9), so the question is valid. The tangent there is y − 3 = −(x − 3), that is x + y = 6. This curve is the *folium of Descartes*, and the symmetry about y = x explains the slope −1 at its point on that line.

**Q (10 marks). Define the derivative and explain its geometrical meaning. State and illustrate the main rules of differentiation, and explain implicit, logarithmic and parametric differentiation with one example each.**

**Introduction.** The derivative of y = f(x) is f′(x) = dy/dx = lim (h→0) [f(x + h) − f(x)]/h. Geometrically it is the **slope of the tangent** at the point (x, f(x)), the limit of secant slopes as the second point approaches the first (Figure 3.1). Physically it is the instantaneous rate of change, such as speed from distance (Plate 3.1a).

**Rules of differentiation.**

| Rule | Formula | Example |
|---|---|---|
| Constant, power | d(xⁿ)/dx = nxⁿ⁻¹ | d(x⁴ − 2x³)/dx = 4x³ − 6x² |
| Sum | (u + v)′ = u′ + v′ | |
| Product | (uv)′ = u′v + uv′ | d(x² eˣ)/dx = eˣ(x² + 2x) |
| Quotient | (u/v)′ = (u′v − uv′)/v² | d((x + 1)/(x − 1))/dx = −2/(x − 1)² |
| Chain | d f(g(x))/dx = f′(g(x)) g′(x) | d(sin x²)/dx = 2x cos x² |

**Standard derivatives.** (sin x)′ = cos x, (cos x)′ = −sin x, (eˣ)′ = eˣ, (ln x)′ = 1/x, (tan x)′ = sec² x.

**Implicit differentiation.** For x² + y² = 25 differentiate both sides: 2x + 2y·dy/dx = 0, so dy/dx = −x/y; at (3, 4) the slope is −3/4 (Figure 3.3).

**Logarithmic differentiation.** For y = xˣ take logarithms: ln y = x ln x. Differentiate: y′/y = ln x + 1, so **y′ = xˣ(ln x + 1)**. It is the method for variable exponents and long products.

**Parametric differentiation.** If x = a cos t, y = a sin t, then dy/dx = (dy/dt)/(dx/dt) = a cos t / (−a sin t) = **−cot t**, and the second derivative is d²y/dx² = (d/dt of dy/dx)/(dx/dt) = csc² t / (−a sin t) = **−1/(a sin³ t)**.

**Higher derivatives.** Differentiating again gives f″, which measures curvature: f″ > 0 means the graph bends upward, f″ < 0 downward. If s is position, then s″ is acceleration.

**Relation to the graph.** Where f′ > 0 the function rises; where f′ = 0 the tangent is flat, giving a possible maximum or minimum (Figure 3.2).

**Conclusion.** The derivative is a limit, and the rules allow us to compute it quickly without returning to the limit each time. In Unit 4 it will be used to optimise, approximate and sketch.
