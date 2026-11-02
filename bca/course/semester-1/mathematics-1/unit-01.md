---
subject: Mathematics I
grade: BCA Semester 1
unit: 1
title: Functions and Graphs
area: BCA 104 · Mathematics I · Unit 1
---

Calculus is the mathematics of change, and its objects are **functions**. Everything in later units (limits, derivatives, integrals, differential equations) is something we *do to a function*, so this unit makes sure you can read, build and combine functions fluently.

::: key What this unit gives you
- Function, domain, range; how to find them from a formula.
- The standard families: polynomial, rational, power, exponential, logarithmic, trigonometric, absolute value, piecewise.
- Even/odd, one-to-one, composition and inverse functions.
- Graph transformations, and the exponent, logarithm and trigonometric facts used throughout the course.
:::

## 1.1 Functions, domain and range

A **function** f from a set A to a set B assigns to every x in A exactly one y = f(x) in B. A is the **domain**; the set of values actually produced is the **range**. A curve is the graph of a function exactly when every vertical line meets it at most once (**vertical line test**).

**Finding the domain.** Start from ℝ and remove values that break the formula:

- division by zero (denominator = 0);
- even roots of negative numbers (radicand < 0);
- logarithm of a non-positive number (argument ≤ 0).

::: example Worked example: domains
**(a)** f(x) = √(x − 2) / (x − 5). Need x − 2 ≥ 0 and x ≠ 5. Domain = [2, 5) ∪ (5, ∞).
**(b)** g(x) = ln(4 − x²). Need 4 − x² > 0, so −2 < x < 2. Domain = (−2, 2).
**(c)** h(x) = 1/√(x² − 3x + 2). Need x² − 3x + 2 > 0, i.e. (x − 1)(x − 2) > 0, so x < 1 or x > 2. Domain = (−∞, 1) ∪ (2, ∞).
:::

**Finding the range.** Complete the square, use known ranges, or solve y = f(x) for x and see which y give a real x.

::: example Worked example: range
f(x) = x² − 4x + 5 = (x − 2)² + 1. Since (x − 2)² ≥ 0, f(x) ≥ 1, and 1 is reached at x = 2. Range = [1, ∞).
:::

## 1.2 Standard families of functions

| Family | Form | Notes |
|---|---|---|
| Linear | f(x) = mx + c | slope m, intercept c |
| Quadratic | ax² + bx + c | parabola, vertex at x = −b/(2a) |
| Polynomial | aₙxⁿ + … + a₀ | domain ℝ; degree n gives at most n roots |
| Rational | P(x)/Q(x) | undefined where Q = 0 (vertical asymptotes or holes) |
| Power / root | xᵃ, ⁿ√x | √x needs x ≥ 0 |
| Exponential | aˣ (a > 0, a ≠ 1) | range (0, ∞); growth if a > 1, decay if 0 < a < 1 |
| Logarithmic | logₐ x | inverse of aˣ; domain (0, ∞) |
| Trigonometric | sin, cos, tan … | periodic |
| Absolute value | \|x\| | = x if x ≥ 0, −x if x < 0 |
| Piecewise | different formulas on different intervals | check the join points |
| Floor / step | ⌊x⌋ | greatest integer ≤ x |

**Exponent laws** (a, b > 0): aᵐ·aⁿ = aᵐ⁺ⁿ; aᵐ / aⁿ = aᵐ⁻ⁿ; (aᵐ)ⁿ = aᵐⁿ; (ab)ⁿ = aⁿbⁿ; a⁰ = 1; a⁻ⁿ = 1/aⁿ; a^(1/n) = ⁿ√a.

**Logarithm laws.** logₐ(xy) = logₐ x + logₐ y; logₐ(x/y) = logₐ x − logₐ y; logₐ(xᵖ) = p logₐ x; change of base logₐ x = ln x / ln a; logₐ a = 1; logₐ 1 = 0. **e** ≈ 2.71828 is the base of the natural logarithm ln.

**Trigonometric facts used in calculus.** sin²θ + cos²θ = 1; 1 + tan²θ = sec²θ; sin 2θ = 2 sin θ cos θ; cos 2θ = cos²θ − sin²θ = 1 − 2 sin²θ = 2 cos²θ − 1; sin(A ± B) = sin A cos B ± cos A sin B; cos(A ± B) = cos A cos B ∓ sin A sin B. Angles in calculus are always in **radians** (π rad = 180°).

| θ | 0 | π/6 | π/4 | π/3 | π/2 |
|---|---|---|---|---|---|
| sin θ | 0 | 1/2 | √2/2 | √3/2 | 1 |
| cos θ | 1 | √3/2 | √2/2 | 1/2 | 0 |
| tan θ | 0 | 1/√3 | 1 | √3 | undefined |

## 1.3 Even, odd and one-to-one functions

- **Even**: f(−x) = f(x); graph symmetric about the y-axis (x², cos x, |x|).
- **Odd**: f(−x) = −f(x); symmetric about the origin (x³, sin x, tan x).
- Most functions are neither. Sums of even functions are even; product of two odd functions is even.

::: example Worked example: classify
f(x) = x³ − x: f(−x) = −x³ + x = −f(x), so **odd**. g(x) = x⁴ + cos x: g(−x) = x⁴ + cos x = g(x), so **even**. h(x) = x² + x: h(−x) = x² − x, which is neither h(x) nor −h(x), so **neither**.
:::

A function is **one-to-one** (injective) if different inputs give different outputs; the **horizontal line test** checks it on a graph. Only one-to-one functions have inverses. x² is not one-to-one on ℝ but is on [0, ∞).

## 1.4 Composition and inverse

The **composite** (f∘g)(x) = f(g(x)): apply g first. In general f∘g ≠ g∘f. The domain of f∘g is those x in the domain of g for which g(x) is in the domain of f.

::: example Worked example: composition
f(x) = 2x + 3, g(x) = x². Then (f∘g)(x) = 2x² + 3, and (g∘f)(x) = (2x + 3)². At x = 1: f∘g = 5 but g∘f = 25.
:::

The **inverse** f⁻¹ undoes f: f⁻¹(f(x)) = x. To find it: write y = f(x), solve for x, swap the names. The graph of f⁻¹ is the mirror image of f's graph in the line y = x; domain and range swap.

::: example Worked example: inverse of a rational function
f(x) = (3x − 1)/(x + 2). Put y = (3x − 1)/(x + 2), so y(x + 2) = 3x − 1, giving xy + 2y = 3x − 1, so x(y − 3) = −1 − 2y, hence x = (2y + 1)/(3 − y). Therefore **f⁻¹(x) = (2x + 1)/(3 − x)**. Check: f(0) = −1/2 and f⁻¹(−1/2) = (−1 + 1)/(3.5) = 0. ✓
:::

The logarithm is the inverse of the exponential: y = aˣ ⇔ x = logₐ y.

## 1.5 Graph transformations

From the graph of y = f(x):

| Change | Effect |
|---|---|
| y = f(x) + k | shift up k (down if k < 0) |
| y = f(x − h) | shift right h (left if h < 0) |
| y = −f(x) | reflect in the x-axis |
| y = f(−x) | reflect in the y-axis |
| y = a·f(x), a > 1 | stretch vertically by a |
| y = f(bx), b > 1 | compress horizontally by b |
| y = \|f(x)\| | reflect the part below the x-axis upward |

Example: y = (x − 3)² + 2 is the parabola y = x² moved 3 right and 2 up, with vertex (3, 2).

**Piecewise and absolute-value functions.** |x − 2| = x − 2 for x ≥ 2 and 2 − x for x < 2. Solving |x − 2| < 3 means −3 < x − 2 < 3, so −1 < x < 5. Solving |x − 2| ≥ 3 gives x ≤ −1 or x ≥ 5.

## Formula and fact sheet

- Domain restrictions: denominators ≠ 0, even-root radicands ≥ 0, log arguments > 0.
- Even: f(−x) = f(x). Odd: f(−x) = −f(x).
- (f∘g)(x) = f(g(x)). Inverse: swap x and y, solve; graph reflects in y = x.
- log(xy) = log x + log y; log(xᵖ) = p log x; logₐ x = ln x / ln a.
- sin²θ + cos²θ = 1; sin 2θ = 2 sin θ cos θ; cos 2θ = 1 − 2 sin²θ.
- |x| < a ⇔ −a < x < a; |x| > a ⇔ x < −a or x > a.

## Chapter summary

- A function pairs each input with exactly one output; domain and range come from restrictions of the formula.
- Even and odd symmetry, composition and inverses are the algebra of functions.
- Transformations shift, stretch and reflect graphs; knowing them saves plotting.
- Exponent, logarithm and trigonometric rules are the toolkit used in every later unit.

## Practice

1. Find the domain of (a) f(x) = √(6 − x − x²), (b) g(x) = ln(x² − 5x + 6), (c) h(x) = (x + 1)/(x² − 4).
2. Find the range of f(x) = 3 − 2x² and of g(x) = 2ˣ + 1.
3. If f(x) = x² + 1 and g(x) = 1/(x − 1), find f∘g, g∘f and their domains.
4. Show that f(x) = (2x + 1)/(x − 3) is one-to-one and find f⁻¹.
5. Classify as even, odd or neither: (a) x sin x, (b) x² + sin x, (c) (eˣ − e⁻ˣ)/2.
6. Solve |2x − 3| ≤ 5.
7. Sketch y = |x² − 4| by describing the transformation.
8. Simplify log₂ 40 − log₂ 5 + 2 log₂ 3.
9. If f(x + 1) = x² + 3x + 2 find f(x).
10. A taxi charges Rs 60 for the first km and Rs 40 for each further km (or part). Write the fare as a piecewise function of distance d and evaluate f(3.5).

::: note Answers and worked solutions
**1.** (a) 6 − x − x² ≥ 0 ⇔ x² + x − 6 ≤ 0 ⇔ (x + 3)(x − 2) ≤ 0, so **[−3, 2]**. (b) x² − 5x + 6 = (x − 2)(x − 3) > 0, so **x < 2 or x > 3**. (c) x² ≠ 4, so **all reals except ±2**.
**2.** f(x) = 3 − 2x² ≤ 3, maximum 3 at x = 0: **(−∞, 3]**. g: 2ˣ > 0, so g > 1: **(1, ∞)**.
**3.** (f∘g)(x) = 1/(x − 1)² + 1, domain x ≠ 1. (g∘f)(x) = 1/(x² + 1 − 1) = 1/x², domain x ≠ 0.
**4.** If (2a + 1)/(a − 3) = (2b + 1)/(b − 3), cross-multiplying gives 2ab − 6a + b − 3 = 2ab − 6b + a − 3, so 7b = 7a, hence a = b. Inverse: y(x − 3) = 2x + 1 ⇒ x(y − 2) = 3y + 1 ⇒ **f⁻¹(x) = (3x + 1)/(x − 2)**.
**5.** (a) x sin x is odd × odd = **even**. (b) x² is even, sin x is odd, so **neither**. (c) **odd** (this is sinh x).
**6.** −5 ≤ 2x − 3 ≤ 5 ⇒ −2 ≤ 2x ≤ 8 ⇒ **−1 ≤ x ≤ 4**.
**7.** Draw the parabola y = x² − 4 (vertex (0, −4), roots ±2), then reflect the part between x = −2 and 2 (below the axis) upward: a "W" with a peak (0, 4).
**8.** log₂(40/5) + log₂ 9 = log₂ 8 + log₂ 9 = 3 + log₂ 9 = **log₂ 72 ≈ 6.17**.
**9.** Put t = x + 1: f(t) = (t − 1)² + 3(t − 1) + 2 = t² + t. So **f(x) = x² + x**.
**10.** f(d) = 60 for 0 < d ≤ 1, and f(d) = 60 + 40·⌈d − 1⌉ for d > 1. f(3.5) = 60 + 40 × ⌈2.5⌉ = 60 + 120 = **Rs 180**.
:::
