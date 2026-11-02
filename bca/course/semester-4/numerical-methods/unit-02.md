---
subject: Numerical Methods
grade: BCA Semester 4
unit: 2
title: Interpolation and Approximation
hours: 8
area: BCA 253 · Numerical Methods · Unit 2
---

An experiment gives you the temperature at 6, 9, 12 and 15 hours; what was it at 10:30? A table of sin x lists whole degrees; what is sin 5°? **Interpolation** constructs a function that passes exactly through the known data points and reads off intermediate values. **Approximation** (least squares) instead fits a simple curve *near* noisy data without passing through every point.

::: key What this unit gives you
- Interpolating polynomials: Lagrange, Newton divided differences, Newton forward and backward differences.
- The error of polynomial interpolation.
- Cubic spline interpolation.
- Least-squares fitting of lines, exponentials and polynomials.
:::

## 2.1 Introduction and uniqueness

Given n + 1 distinct points (x₀, y₀), …, (xₙ, yₙ), there is **exactly one polynomial of degree at most n** through all of them. Lagrange's and Newton's formulas are different ways to write the *same* polynomial, so they must give the same value; that is a handy check.

Estimating inside [x₀, xₙ] is **interpolation**; estimating outside is **extrapolation**, which is far less reliable.

## 2.2 Errors in polynomial interpolation

If f has n + 1 continuous derivatives and Pₙ interpolates f at x₀ … xₙ, then for some ξ in the interval

**f(x) − Pₙ(x) = f⁽ⁿ⁺¹⁾(ξ)/(n + 1)! · (x − x₀)(x − x₁)…(x − xₙ)**

The product term is small near the middle of the data and large near the ends, so interpolate near the centre. Raising the degree does not always help: for equally spaced points and some functions (Runge's example 1/(1 + 25x²)) the error at the ends *grows* with n. This is one reason to prefer splines for many points.

## 2.3 Lagrange interpolation

Each point has a **basis polynomial** Lᵢ(x) = Π_{j≠i} (x − xⱼ)/(xᵢ − xⱼ), which is 1 at xᵢ and 0 at all other nodes; then **Pₙ(x) = Σ yᵢ Lᵢ(x)**. It works for unequal spacing, but adding a point means starting again.

::: example Interpolating ln x at x = 2.5
Data:

| i | xᵢ | yᵢ = ln xᵢ |
|---|---|---|
| 0 | 1 | 0.000000 |
| 1 | 2 | 0.693147 |
| 2 | 3 | 1.098612 |
| 3 | 4 | 1.386294 |

For x = 2.5 and four nodes the weights L₀ … L₃ are -0.0625, 0.5625, 0.5625, -0.0625 (they always sum to 1). Then P₃(2.5) = 0.921221. The true ln 2.5 = 0.916291, so the error is 0.004931. The theoretical bound uses f⁗(x) = −6/x⁴, at most 6 on [1, 4], and the product |(2.5 − 1)(2.5 − 2)(2.5 − 3)(2.5 − 4)| = 0.5625, giving |error| ≤ (6/4!)(0.5625) = 0.140625. The actual error is well inside the bound. Using only the three nearest nodes 2, 3, 4 gives 0.910603 with error 0.005688: more points here helped only slightly.
:::

## 2.4 Newton's interpolation with divided differences

**Divided differences** are defined by f[xᵢ] = yᵢ, f[xᵢ, xᵢ₊₁] = (f[xᵢ₊₁] − f[xᵢ]) / (xᵢ₊₁ − xᵢ), and so on, each order dividing by the total span. The interpolating polynomial is

**Pₙ(x) = f[x₀] + f[x₀, x₁](x − x₀) + f[x₀, x₁, x₂](x − x₀)(x − x₁) + …**

Adding a new data point adds one term and one table diagonal; nothing already computed is wasted. Works for unequal spacing.

::: example Divided-difference table for ln x
| xᵢ | f[xᵢ] | f[xᵢ,xᵢ₊₁] | f[·,·,·] | f[·,·,·,·] |
|---|---|---|---|---|
| 1 | 0.000000 | 0.693147 | -0.143841 | 0.028317 |
| 2 | 0.693147 | 0.405465 | -0.058892 |  |
| 3 | 1.098612 | 0.287682 |  |  |
| 4 | 1.386294 |  |  |  |

The top diagonal gives the coefficients 0.000000, 0.693147, -0.143841, 0.028317. Then P₃(2.5) = 0 + 0.693147(1.5) − 0.143841(1.5)(0.5) + 0.028317(1.5)(0.5)(−0.5) = 0.921221, identical to the Lagrange value, as it must be.
:::

## 2.5 Newton's forward and backward difference formulas (equal spacing)

For equally spaced nodes with step h define **forward differences** Δy₀ = y₁ − y₀, Δ²y₀ = Δy₁ − Δy₀, and so on. With **u = (x − x₀)/h**:

**Forward:** y(x) ≈ y₀ + uΔy₀ + u(u − 1)/2! Δ²y₀ + u(u − 1)(u − 2)/3! Δ³y₀ + …

Use it near the **start** of the table. Near the **end**, use the **backward** formula with **u = (x − xₙ)/h**, the last entry of each difference column (∇):

**Backward:** y(x) ≈ yₙ + u∇yₙ + u(u + 1)/2! ∇²yₙ + u(u + 1)(u + 2)/3! ∇³yₙ + …

::: example sin x from a table of whole 10° steps (four-decimal data)
| x° | y = sin x | Δy | Δ²y | Δ³y | Δ⁴y |
|---|---|---|---|---|---|
| 0 | 0.0000 | 0.1736 | -0.0052 | -0.0052 | 0.0004 |
| 10 | 0.1736 | 0.1684 | -0.0104 | -0.0048 |  |
| 20 | 0.3420 | 0.1580 | -0.0152 |  |  |
| 30 | 0.5000 | 0.1428 |  |  |  |
| 40 | 0.6428 |  |  |  |  |

**sin 5° by the forward formula:** h = 10, u = (5 − 0)/10 = 0.5. The top-row differences are 0.0000, 0.1736, -0.0052, -0.0052, 0.0004. The result is sin 5° ≈ 0.08711; the true value is 0.08716.

**sin 35° by the backward formula:** u = (35 − 40)/10 = -0.5. The bottom-diagonal differences are 0.6428, 0.1428, -0.0152, -0.0048, 0.0004, giving sin 35° ≈ 0.57358; the true value is 0.57358.

The differences become small and nearly constant at the fourth order, a sign that a quartic fits well. The forward result is off in the fourth decimal because the table itself is rounded to four decimals and differences amplify that rounding.
:::

**Choosing a formula.** Divided differences for unequal spacing; forward formula for a point near the beginning; backward near the end; for the middle use central-difference formulas (Gauss, Stirling, not required here).

## 2.6 Cubic spline interpolation

A single high-degree polynomial through many points can oscillate. A **cubic spline** instead uses a different cubic on each interval [xᵢ, xᵢ₊₁], joined so that the function, its first derivative and its second derivative are continuous at every interior node. It is smooth to the eye and well behaved, and is the mathematical form of a draughtsman's flexible ruler.

With n intervals there are 4n unknown coefficients. Interpolation (2n conditions) plus continuity of S′ and S″ at the n − 1 interior nodes (2n − 2) leaves two conditions; for a **natural spline** we set S″ = 0 at both ends.

**Method.** Let Mᵢ = S″(xᵢ) and hᵢ = xᵢ₊₁ − xᵢ. The continuity of S′ gives, for each interior node *i*,

hᵢ₋₁Mᵢ₋₁ + 2(hᵢ₋₁ + hᵢ)Mᵢ + hᵢMᵢ₊₁ = 6[(yᵢ₊₁ − yᵢ)/hᵢ − (yᵢ − yᵢ₋₁)/hᵢ₋₁]

a tridiagonal system. On each interval, with t = x − xᵢ,

S(x) = yᵢ + bᵢt + (Mᵢ/2)t² + ((Mᵢ₊₁ − Mᵢ)/(6hᵢ))t³, where bᵢ = (yᵢ₊₁ − yᵢ)/hᵢ − hᵢ(2Mᵢ + Mᵢ₊₁)/6.

::: example Natural spline through (1, 2), (2, 3), (3, 5), (4, 4)
With h = 1 the two interior equations are 4M₁ + M₂ = 6(2 − 1) = 6 and M₁ + 4M₂ = 6(−1 − 2) = −18 (with M₀ = M₃ = 0, using index 0 to 3 for the four nodes). Solving gives the second derivatives M = (0.00000, 2.80000, -5.20000, 0.00000). The pieces:

| interval | a | b | c | d  (S = a + b t + c t² + d t³, t = x − xᵢ) |
|---|---|---|---|---|
| [1, 2] | 2.00000 | 0.53333 | 0.00000 | 0.46667 |
| [2, 3] | 3.00000 | 1.93333 | 1.40000 | -1.33333 |
| [3, 4] | 5.00000 | 0.73333 | -2.60000 | 0.86667 |

Then S(1.5) = 2.32500 and S(2.5) = 4.15000. (A straight line through the neighbours of 2.5 would give 4.0, but the spline bends to reflect the whole data set.) The results agree with SciPy's CubicSpline(bc_type="natural").
:::

## 2.7 Least-squares approximation

When data come from measurement they carry noise and passing through every point is pointless. The **least-squares method** chooses the curve that minimises the sum of squared vertical residuals S = Σ (yᵢ − f(xᵢ))².

### Straight line y = a + bx

Setting ∂S/∂a = ∂S/∂b = 0 gives the **normal equations**

Σy = na + bΣx, Σxy = aΣx + bΣx²,

so **b = (nΣxy − ΣxΣy)/(nΣx² − (Σx)²)** and **a = (Σy − bΣx)/n**.

::: example Fit a line to five points
| x | y | x² | xy |
|---|---|---|---|
| 1 | 2.2 | 1 | 2.2 |
| 2 | 2.8 | 4 | 5.6 |
| 3 | 3.6 | 9 | 10.8 |
| 4 | 4.5 | 16 | 18.0 |
| 5 | 5.1 | 25 | 25.5 |
| Σ = 15 | 18.2 | 55 | 62.1 |

Σx = 15, Σy = 18.2, Σx² = 55, Σxy = 62.1 with n = 5. Then b = (5 × 62.1 − 15 × 18.2)/(5 × 55 − 15²) = 0.7500 and a = (18.2 − 0.7500 × 15)/5 = 1.3900. The line is **y = 1.3900 + 0.7500 x**. The residual sum of squares is 0.0270 and R² = 0.9952, an excellent fit. Predicting x = 6 gives 5.890 (extrapolation, so treat it with caution).
:::

### Non-linear data: reduction to linear form

| Model | Transformation | Fit line to |
|---|---|---|
| y = A e^(Bx) | ln y = ln A + Bx | (x, ln y) |
| y = A x^B | ln y = ln A + B ln x | (ln x, ln y) |
| y = 1/(a + bx) | 1/y = a + bx | (x, 1/y) |
| y = a + b/x | y = a + b·(1/x) | (1/x, y) |

::: example Exponential model y = A e^(Bx)
| x | y | ln y | x·ln y |
|---|---|---|---|
| 1 | 2.7 | 0.9933 | 0.9933 |
| 2 | 4.0 | 1.3863 | 2.7726 |
| 3 | 6.1 | 1.8083 | 5.4249 |
| 4 | 9.2 | 2.2192 | 8.8768 |
| 5 | 13.5 | 2.6027 | 13.0134 |

Fitting a straight line to (x, ln y) gives B = 0.4052 and ln A = 0.5864, so A = 1.7975 and **y = 1.7975 e^(0.4052 x)**. The prediction at x = 6 is 20.44. Note that this minimises the error in ln y, not in y, which weights small values more; it is the standard quick method.
:::

### Polynomial (quadratic) fit

For y = a + bx + cx² the normal equations are Σy = na + bΣx + cΣx², Σxy = aΣx + bΣx² + cΣx³, Σx²y = aΣx² + bΣx³ + cΣx⁴. For the line data above, solving gives (a, b, c) = (1.4400, 0.7071, 0.0071): the x² coefficient is nearly zero, confirming that the straight line was enough.

## Formula and fact sheet

- Error: f(x) − Pₙ(x) = f⁽ⁿ⁺¹⁾(ξ)/(n + 1)! · Π(x − xᵢ).
- Lagrange: P(x) = Σ yᵢ Π_{j≠i} (x − xⱼ)/(xᵢ − xⱼ).
- Newton divided differences: P = f[x₀] + f[x₀,x₁](x − x₀) + …
- Forward: u = (x − x₀)/h, terms u(u − 1)…/k! Δᵏy₀. Backward: u = (x − xₙ)/h, terms u(u + 1)…/k! ∇ᵏyₙ.
- Spline: continuity of S, S′, S″; natural ends S″ = 0; tridiagonal system for Mᵢ.
- Line fit: b = (nΣxy − ΣxΣy)/(nΣx² − (Σx)²), a = (Σy − bΣx)/n.

## Chapter summary

- Through n + 1 points there is one polynomial of degree ≤ n; Lagrange, Newton divided-difference and Newton difference formulas all give it.
- The error depends on the (n + 1)th derivative and the product of distances to the nodes: interpolate near the centre and avoid very high degrees.
- Cubic splines give a smooth piecewise fit by solving a tridiagonal system.
- Least squares fits noisy data by minimising squared residuals; many non-linear models reduce to straight lines after a transformation.

## Practice

1. State the interpolation error formula and explain why it is smallest near the centre of the data.
2. Use Lagrange's formula with nodes 1, 2, 3, 4 and ln x to estimate ln 2.5. Find the error.
3. Build the divided-difference table for the same data and confirm the value.
4. From the 10° table of sin x, estimate sin 5° (forward) and sin 35° (backward).
5. Why is the forward formula used near the beginning of a table and the backward near the end?
6. Find the natural cubic spline value at x = 2.5 for the points (1, 2), (2, 3), (3, 5), (4, 4).
7. Fit y = a + bx to (1, 2.2), (2, 2.8), (3, 3.6), (4, 4.5), (5, 5.1). Predict y at x = 6.
8. Fit y = A e^(Bx) to (1, 2.7), (2, 4.0), (3, 6.1), (4, 9.2), (5, 13.5).
9. Distinguish interpolation from least-squares approximation.
10. What is Runge's phenomenon, and how do splines avoid it?

::: note Answers and worked solutions
**1.** f(x) − Pₙ(x) = f⁽ⁿ⁺¹⁾(ξ)(x − x₀)…(x − xₙ)/(n + 1)!. Near the middle the factors |x − xᵢ| are smaller (some nodes lie on either side), whereas near the ends all distances are large, so the product and the error are bigger.
**2.** The weights at 2.5 are -0.0625, 0.5625, 0.5625, -0.0625; P₃(2.5) = 0.921221, true 0.916291, error 0.004931 (bound 0.140625).
**3.** The table in Section 2.4 gives coefficients 0.000000, 0.693147, -0.143841, 0.028317; evaluating at 2.5 gives 0.921221, the same as Lagrange.
**4.** Forward with u = 0.5: sin 5° ≈ 0.08711 (true 0.08716). Backward with u = -0.5: sin 35° ≈ 0.57358 (true 0.57358).
**5.** Forward differences use the top row of the table, which has all its later columns available only if the point is near the start; near the end the top-row differences of high order don't exist or are poorly centred, while the bottom diagonal (backward differences) has them and reaches back from the end.
**6.** M = (0.00000, 2.80000, -5.20000, 0.00000), S(2.5) = 4.15000 from the piece on [2, 3]: 3 + 1.93333(0.5) + 1.4(0.25) − 1.33333(0.125) = 4.15000.
**7.** Σx = 15, Σy = 18.2, Σx² = 55, Σxy = 62.1; b = 0.7500, a = 1.3900; at x = 6, y = 5.890.
**8.** ln y values in Section 2.7; B = 0.4052, ln A = 0.5864, A = 1.7975: y = 1.7975 e^(0.4052x).
**9.** Interpolation reproduces the data points exactly and is suited to exact (or very accurate) data; least squares gives a smoother curve that need not pass through any point and is suited to noisy data.
**10.** For equally spaced nodes, a high-degree interpolating polynomial may oscillate wildly near the interval ends (for example 1/(1 + 25x²)). A spline uses low-degree cubic pieces, so a local change affects only nearby intervals and no big oscillations build up.
:::
