---
subject: Mathematics I
grade: BCA Semester 1
unit: 4
title: Applications of Derivatives
area: BCA 104 · Mathematics I · Unit 4
---

Derivatives are used to describe tangents, rates, optimum values and approximations. This unit turns the differentiation rules of Unit 3 into tools for solving problems: tangent lines, related rates, maxima and minima, the mean value theorems, L'Hôpital's rule and Taylor/Maclaurin series.

::: key What this unit gives you
- Tangent and normal lines; rates of change and related rates.
- Increasing/decreasing functions, maxima and minima, optimisation, concavity.
- Rolle's theorem, the mean value theorem, L'Hôpital's rule.
- Maclaurin and Taylor series, with numerical approximation.
:::

## 4.1 Tangent and normal

The tangent to y = f(x) at (a, f(a)) has slope m = f′(a): **y − f(a) = f′(a)(x − a)**. The normal is perpendicular, with slope −1/f′(a) (if f′(a) ≠ 0).

::: example Worked example
For y = x³ − 2x + 1 at x = 1: y(1) = 0 and y′ = 3x² − 2 = 1. Tangent: y = x − 1. Normal: slope −1, so y = −(x − 1) = 1 − x.
:::

## 4.2 Rates of change and related rates

dy/dx is the rate of change of y with respect to x. For a position function s(t): velocity v = ds/dt, acceleration a = dv/dt = d²s/dt².

**Related rates**: two quantities are tied by an equation; differentiate it with respect to time.

::: example Worked example: sliding ladder
A 10 m ladder leans on a wall; the foot slides away at 2 m/s. How fast does the top fall when the foot is 6 m from the wall? x² + y² = 100 ⇒ 2x x′ + 2y y′ = 0 ⇒ y′ = −(x/y) x′. When x = 6, y = 8, so y′ = −(6/8)(2) = **−1.5 m/s** (the top slides down at 1.5 m/s).
:::

::: example Worked example: expanding circle
The radius of a circular oil slick grows at 3 cm/s. At r = 10 cm, dA/dt = 2πr dr/dt = 2π(10)(3) = **60π ≈ 188.5 cm²/s**.
:::

## 4.3 Increasing, decreasing, maxima and minima

- f′(x) > 0 on an interval ⇒ f increasing; f′(x) < 0 ⇒ decreasing.
- A **critical point** is where f′(x) = 0 or f′ does not exist. Local maxima and minima occur only at critical points.
- **First-derivative test**: f′ changes + to − ⇒ local max; − to + ⇒ local min; no change ⇒ neither.
- **Second-derivative test**: at f′(c) = 0, if f″(c) > 0 then local min; f″(c) < 0 ⇒ local max; f″(c) = 0 ⇒ test fails.
- **Concavity**: f″ > 0 concave up (holds water); f″ < 0 concave down. A **point of inflection** is where concavity changes (f″ = 0 and changes sign).
- On a closed interval [a, b] the **absolute** extremes occur at critical points or the endpoints, so compare all candidates.

::: example Worked example: full analysis of a cubic
f(x) = x³ − 6x² + 9x + 1. f′ = 3x² − 12x + 9 = 3(x − 1)(x − 3). f″ = 6x − 12.
At x = 1: f″ = −6 < 0, local **maximum**, f(1) = 5. At x = 3: f″ = 6 > 0, local **minimum**, f(3) = 1. Inflection at f″ = 0, x = 2, f(2) = 3. f is increasing on (−∞, 1) and (3, ∞), decreasing on (1, 3).
On [0, 4]: f(0) = 1, f(1) = 5, f(3) = 1, f(4) = 5. Absolute max 5 (at x = 1 and x = 4), absolute min 1 (at x = 0 and x = 3).
:::

## 4.4 Optimisation

Steps: (1) draw and name variables; (2) write the quantity to optimise; (3) use the constraint to reduce it to one variable; (4) find critical points and test; (5) answer the question asked, with units.

::: example Worked example: open box
From a 12 cm × 12 cm square, cut equal squares of side x from the corners and fold up an open box. V = x(12 − 2x)² for 0 < x < 6. V′ = (12 − 2x)² − 4x(12 − 2x) = (12 − 2x)(12 − 6x) = 0 ⇒ x = 2 (x = 6 gives V = 0). V″ at x = 2 is negative (V′ goes + to −), so maximum **V = 2 × 8² = 128 cm³**.
:::

::: example Worked example: fixed perimeter
A rectangle has perimeter 40 m. Width w, length 20 − w; A = w(20 − w), A′ = 20 − 2w = 0 ⇒ w = 10, A″ = −2 < 0. Maximum area 100 m², a square.
:::

::: example Worked example: minimum cost can
A closed cylindrical can must hold 500 cm³. Minimise surface area S = 2πr² + 2πrh with h = 500/(πr²): S = 2πr² + 1000/r. S′ = 4πr − 1000/r² = 0 ⇒ r³ = 250/π, r ≈ 4.30 cm, h = 2r ≈ 8.60 cm. The best can has height equal to its diameter.
:::

## 4.5 Mean value theorems

**Rolle's theorem.** If f is continuous on [a, b], differentiable on (a, b) and f(a) = f(b), then f′(c) = 0 for some c in (a, b).

**Mean value theorem (MVT).** If f is continuous on [a, b] and differentiable on (a, b), there is c in (a, b) with **f′(c) = [f(b) − f(a)]/(b − a)**, a tangent parallel to the chord.

::: example Worked example
**Rolle:** f(x) = x² − 4x + 3 on [1, 3]: f(1) = f(3) = 0; f′(x) = 2x − 4 = 0 at c = 2, inside the interval ✓.
**MVT:** f(x) = x³ on [0, 2]: slope of chord = (8 − 0)/2 = 4 = 3c² ⇒ c = 2/√3 ≈ 1.155 ✓.
**Use:** MVT proves that if f′ = 0 on an interval then f is constant, and gives inequalities such as |sin a − sin b| ≤ |a − b|.
:::

## 4.6 L'Hôpital's rule

If lim f/g gives **0/0 or ∞/∞** and lim f′/g′ exists (or is ±∞), then **lim f/g = lim f′/g′**. It can be applied repeatedly. Other forms (0·∞, ∞ − ∞, 1^∞, 0⁰, ∞⁰) are first rewritten as a quotient, using ln for exponent forms.

::: example Worked example
**(a)** lim (x→0) (eˣ − 1 − x)/x²: 0/0 → (eˣ − 1)/(2x): 0/0 → eˣ/2 → **1/2**.
**(b)** lim (x→0) (sin x − x)/x³ → (cos x − 1)/(3x²) → (−sin x)/(6x) → (−cos x)/6 → **−1/6**.
**(c)** lim (x→0⁺) x ln x = lim ln x/(1/x) = lim (1/x)/(−1/x²) = lim (−x) = **0**.
**(d)** lim (x→0⁺) xˣ: ln y = x ln x → 0, so y → e⁰ = **1**.
**(e)** lim (x→∞) (ln x)/x = lim (1/x)/1 = **0** (logs grow slower than any power).
**(f)** lim (x→∞) (1 + 1/x)ˣ: ln y = ln(1 + 1/x)/(1/x) → [(−1/x²)/(1 + 1/x)]/(−1/x²) = 1/(1 + 1/x) → 1, so the limit is **e**.
:::

## 4.7 Taylor and Maclaurin series

If f has derivatives of all orders at a, its **Taylor series** is
f(x) = f(a) + f′(a)(x − a) + f″(a)(x − a)²/2! + f‴(a)(x − a)³/3! + …
With a = 0 it is the **Maclaurin series**. The first n terms form a polynomial approximation, the remainder is the error.

| Function | Maclaurin series | Valid for |
|---|---|---|
| eˣ | 1 + x + x²/2! + x³/3! + … | all x |
| sin x | x − x³/3! + x⁵/5! − … | all x |
| cos x | 1 − x²/2! + x⁴/4! − … | all x |
| ln(1 + x) | x − x²/2 + x³/3 − … | −1 < x ≤ 1 |
| 1/(1 − x) | 1 + x + x² + x³ + … | \|x\| < 1 |
| (1 + x)ⁿ | 1 + nx + n(n − 1)x²/2! + … | \|x\| < 1 |

::: example Worked example: approximation
sin(0.1) ≈ 0.1 − (0.1)³/6 = 0.1 − 0.000167 = **0.099833** (true value 0.0998334). √1.02 = (1 + 0.02)^{1/2} ≈ 1 + 0.01 − 0.00005 = **1.00995**. Also e^{0.2} ≈ 1 + 0.2 + 0.02 + 0.001333 + 0.0000667 = 1.221400 (true 1.221403).
:::

**Linear approximation (differentials).** f(x + Δx) ≈ f(x) + f′(x) Δx. For ∛8.1: f(x) = x^{1/3}, f′(8) = 1/12, so ∛8.1 ≈ 2 + 0.1/12 = 2.00833.

## Formula and fact sheet

- Tangent at a: y − f(a) = f′(a)(x − a); normal slope −1/f′(a).
- Critical point: f′ = 0 or undefined. f″ > 0 min, f″ < 0 max.
- MVT: f′(c) = (f(b) − f(a))/(b − a); Rolle is the case f(a) = f(b).
- L'Hôpital: 0/0 or ∞/∞ → differentiate top and bottom separately.
- Maclaurin: eˣ, sin x, cos x, ln(1 + x), (1 + x)ⁿ as in the table.
- Related rates: write the relation, differentiate with respect to t, substitute.

## Chapter summary

- The derivative gives tangents, rates, and the shape of a graph (increasing, decreasing, concave).
- Optimisation reduces a real problem to one variable and tests critical points and endpoints.
- Rolle and the MVT link the average slope to an instantaneous slope; L'Hôpital turns indeterminate limits into derivative quotients.
- Taylor series replace a function by polynomials and enable numerical approximation.

## Practice

1. Find the tangent and normal to y = x² − 3x + 2 at x = 2.
2. A balloon's radius grows at 2 cm/s. Find the rate at which its volume grows when r = 5 cm.
3. Find the local extrema and inflection point of f(x) = 2x³ − 9x² + 12x.
4. Find the dimensions of the rectangle of maximum area inscribed in a circle of radius R.
5. A farmer has 200 m of fence for a rectangular pen against a river wall (no fence along the river). Find the maximum area.
6. Verify the MVT for f(x) = x² on [1, 3].
7. Evaluate (a) lim (x→0) (e^{x} − e^{−x})/sin x, (b) lim (x→0) (tan x − x)/x³, (c) lim (x→0) (cos x)^{1/x²}.
8. Write the Maclaurin series of cos x up to x⁴ and use it to estimate cos(0.2).
9. Use a linear approximation for √26.
10. Show that x − x²/2 < ln(1 + x) < x for x > 0.

::: note Answers and worked solutions
**1.** y(2) = 0, y′ = 2x − 3 = 1. Tangent y = x − 2; normal y = −(x − 2) = 2 − x.
**2.** V = (4/3)πr³, dV/dt = 4πr² dr/dt = 4π·25·2 = **200π ≈ 628.3 cm³/s**.
**3.** f′ = 6x² − 18x + 12 = 6(x − 1)(x − 2); f″ = 12x − 18. x = 1: f″ = −6, **max** f(1) = 5. x = 2: f″ = 6, **min** f(2) = 4. Inflection at x = 1.5, f(1.5) = 4.5.
**4.** With sides x and y, x² + y² = 4R² and A = xy. Maximising A² = x²(4R² − x²) gives x² = 2R², so x = y = R√2: a **square** of area 2R².
**5.** Width w (two sides), length 200 − 2w: A = w(200 − 2w), A′ = 200 − 4w = 0 ⇒ w = 50, length 100, **A = 5000 m²**.
**6.** Chord slope (9 − 1)/2 = 4; f′(c) = 2c = 4 ⇒ c = 2 ∈ (1, 3) ✓.
**7.** (a) 0/0 → (e^x + e^{−x})/cos x → **2**. (b) → (sec²x − 1)/(3x²) = tan²x/(3x²) → **1/3**. (c) ln y = ln cos x/x² → (−tan x)/(2x) → **−1/2**, so the limit is **e^{−1/2}**.
**8.** cos x ≈ 1 − x²/2 + x⁴/24; cos 0.2 ≈ 1 − 0.02 + 0.0000667 = **0.980067** (true 0.980067).
**9.** f(x) = √x at 25: f′ = 1/(2·5) = 0.1; √26 ≈ 5 + 0.1 = **5.1** (true 5.0990).
**10.** Let g(x) = ln(1 + x) − x + x²/2. g(0) = 0 and g′ = 1/(1 + x) − 1 + x = x²/(1 + x) > 0, so g > 0 for x > 0. Let h(x) = x − ln(1 + x); h(0) = 0, h′ = x/(1 + x) > 0, so h > 0. ∎
:::
