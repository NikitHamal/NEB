---
subject: Mathematics I
grade: BCA Semester 1
unit: 5
title: Integration
area: BCA 104 · Mathematics I · Unit 5
---

Integration reverses differentiation and also adds up infinitely many infinitesimal pieces. With it we compute areas, volumes, total change, averages and, in the next unit, solve differential equations.

::: key What this unit gives you
- Antiderivatives, the table of standard integrals, and the substitution, parts and partial-fraction methods.
- The definite integral, the Fundamental Theorem of Calculus, and its properties.
- Area between curves, volume of revolution, average value, and improper integrals.
:::

## 5.1 Indefinite integrals

F is an **antiderivative** of f if F′ = f. The family of all antiderivatives is the **indefinite integral** ∫ f(x) dx = F(x) + C, where C is an arbitrary constant.

| f(x) | ∫ f dx | f(x) | ∫ f dx |
|---|---|---|---|
| xⁿ (n ≠ −1) | xⁿ⁺¹/(n + 1) | 1/x | ln\|x\| |
| eˣ | eˣ | aˣ | aˣ/ln a |
| sin x | −cos x | cos x | sin x |
| sec²x | tan x | cosec²x | −cot x |
| sec x tan x | sec x | 1/(1 + x²) | tan⁻¹x |
| 1/√(1 − x²) | sin⁻¹x | tan x | ln\|sec x\| |
| 1/√(x² + a²) | ln\|x + √(x² + a²)\| | 1/(x² − a²) | (1/2a) ln\|(x − a)/(x + a)\| |

Linearity: ∫ (af + bg) = a∫ f + b∫ g. Always check an answer by differentiating it.

::: example Worked example
∫ (3x² + 2x + 1) dx = x³ + x² + x + C.
∫ (√x + 1/x²) dx = (2/3)x^{3/2} − 1/x + C.
∫ sin²x dx = ∫ (1 − cos 2x)/2 dx = x/2 − (sin 2x)/4 + C.
:::

## 5.2 Integration by substitution

If an integral has the form ∫ f(g(x)) g′(x) dx, put u = g(x), du = g′(x) dx, and integrate in u.

::: example Worked example
**(a)** ∫ 2x e^{x²} dx: u = x², du = 2x dx, so ∫ eᵘ du = e^{x²} + C.
**(b)** ∫ x/(x² + 1) dx: u = x² + 1, du = 2x dx, so ½ ∫ du/u = **½ ln(x² + 1) + C**.
**(c)** ∫ tan x dx = ∫ sin x/cos x dx: u = cos x, du = −sin x dx, so −ln|cos x| + C = ln|sec x| + C.
**(d)** ∫ cos³x dx = ∫ (1 − sin²x) cos x dx: u = sin x, so sin x − sin³x/3 + C.
**(e)** ∫ 1/(x ln x) dx: u = ln x, so ln|ln x| + C.
**(f)** ∫ (2x + 3)⁵ dx = (2x + 3)⁶/12 + C.
:::

## 5.3 Integration by parts

From (uv)′ = u′v + uv′: **∫ u dv = uv − ∫ v du**. Choose u in the order **LIATE** (Logarithmic, Inverse trig, Algebraic, Trig, Exponential): the first type that appears becomes u.

::: example Worked example
**(a)** ∫ x eˣ dx: u = x, dv = eˣ dx ⇒ x eˣ − ∫ eˣ dx = **(x − 1)eˣ + C**.
**(b)** ∫ x² ln x dx: u = ln x, dv = x² dx ⇒ (x³/3) ln x − ∫ x²/3 dx = **(x³/3) ln x − x³/9 + C**.
**(c)** ∫ ln x dx: u = ln x, dv = dx ⇒ x ln x − x + C.
**(d)** ∫ x sin x dx = −x cos x + sin x + C.
**(e)** ∫ eˣ sin x dx = I. By parts twice, I = eˣ sin x − eˣ cos x − I, so **I = eˣ(sin x − cos x)/2 + C**.
**(f)** ∫ tan⁻¹x dx = x tan⁻¹x − ½ ln(1 + x²) + C.
:::

## 5.4 Partial fractions

A proper rational function P(x)/Q(x) (degree P < degree Q) is split into simpler fractions by factors of Q: a linear factor (x − a) gives A/(x − a); a repeated factor (x − a)² gives A/(x − a) + B/(x − a)²; an irreducible quadratic gives (Ax + B)/(x² + px + q). If the degree of P ≥ degree of Q, divide first.

::: example Worked example
**(a)** 1/((x − 1)(x + 2)) = A/(x − 1) + B/(x + 2). Then 1 = A(x + 2) + B(x − 1); x = 1 gives A = 1/3; x = −2 gives B = −1/3. So ∫ = ⅓ ln|x − 1| − ⅓ ln|x + 2| = **⅓ ln|(x − 1)/(x + 2)| + C**.
**(b)** (3x + 5)/((x + 1)²) = 3/(x + 1) + 2/(x + 1)². ∫ = 3 ln|x + 1| − 2/(x + 1) + C.
**(c)** ∫ (x² + 1)/(x − 1) dx: divide, x² + 1 = (x − 1)(x + 1) + 2, so ∫ (x + 1 + 2/(x − 1)) dx = x²/2 + x + 2 ln|x − 1| + C.
:::

## 5.5 The definite integral and the Fundamental Theorem

The **definite integral** ∫ₐᵇ f(x) dx is the limit of Riemann sums Σ f(xᵢ) Δx, the signed area between the graph and the x-axis from a to b. The **Fundamental Theorem of Calculus** connects it to antiderivatives:

- **Part 1**: if F(x) = ∫ₐˣ f(t) dt then F′(x) = f(x).
- **Part 2**: **∫ₐᵇ f(x) dx = F(b) − F(a)** for any antiderivative F.

**Properties.** ∫ₐᵇ f = −∫ᵇₐ f; ∫ₐᵃ f = 0; ∫ₐᵇ f = ∫ₐᶜ f + ∫ᶜᵇ f; ∫ₐᵇ f(x) dx = ∫ₐᵇ f(a + b − x) dx; for even f, ∫₋ₐᵃ f = 2∫₀ᵃ f; for odd f, ∫₋ₐᵃ f = 0. When substituting in a definite integral, change the limits too.

::: example Worked example
**(a)** ∫₀^π sin x dx = [−cos x]₀^π = 1 + 1 = **2**.
**(b)** ∫₁² dx/x = ln 2 − ln 1 = **ln 2 ≈ 0.693**.
**(c)** ∫₀¹ 2x e^{x²} dx: u = x², limits 0 → 1: ∫₀¹ eᵘ du = **e − 1 ≈ 1.718**.
**(d)** ∫₀^{π/2} sin³x dx = ∫₀^{π/2} (1 − cos²x) sin x dx, u = cos x: ∫₀¹ (1 − u²) du = 1 − 1/3 = **2/3**.
**(e)** ∫₋₁¹ x³ dx = **0** (odd function).
**(f)** ∫₀¹ x eˣ dx = [(x − 1)eˣ]₀¹ = 0 − (−1) = **1**.
:::

## 5.6 Applications

**Area between curves.** If f ≥ g on [a, b]: A = ∫ₐᵇ [f(x) − g(x)] dx. If the curves cross, split at the intersections.

**Volume of revolution** about the x-axis (disc method): V = π ∫ₐᵇ [f(x)]² dx; with a hole (washer): V = π ∫ (R² − r²) dx. About the y-axis (shell method): V = 2π ∫ x f(x) dx.

**Average value** of f on [a, b]: (1/(b − a)) ∫ₐᵇ f dx. **Arc length**: L = ∫ₐᵇ √(1 + (f′)²) dx. **Total change**: ∫ of a rate gives the net change (distance = ∫ speed dt).

::: example Worked example
**Area** between y = x and y = x²: intersections x = 0, 1; A = ∫₀¹ (x − x²) dx = ½ − ⅓ = **1/6**.
**Area** under y = sin x from 0 to π: **2**.
**Volume** of y = x² about the x-axis from 0 to 1: V = π ∫₀¹ x⁴ dx = **π/5**. For y = √x on [0, 4]: V = π ∫₀⁴ x dx = **8π**.
**Average value** of f(x) = x² on [0, 3]: (1/3)(27/3) = **3**.
**Net displacement** for velocity v(t) = 3t² − 6t + 2 from t = 0 to 2: [t³ − 3t² + 2t]₀² = 8 − 12 + 4 = **0** (the body returns to its start; the *distance* travelled is ∫|v| dt, which is larger).
:::

## 5.7 Improper integrals

An integral with an infinite limit or an infinite integrand is defined as a limit.

::: example Worked example
**(a)** ∫₁^∞ x⁻² dx = lim (b→∞) [−1/x]₁ᵇ = 1 − 0 = **1** (converges).
**(b)** ∫₁^∞ 1/x dx = lim ln b = ∞ (**diverges**).
**(c)** ∫₀¹ x^{−1/2} dx = lim (a→0⁺) [2√x]ₐ¹ = **2** (converges).
**(d)** ∫₀^∞ e^{−x} dx = **1**.
**Rule:** ∫₁^∞ x^{−p} dx converges iff p > 1; ∫₀¹ x^{−p} dx converges iff p < 1.
:::

## Formula and fact sheet

- ∫ xⁿ dx = xⁿ⁺¹/(n + 1); ∫ dx/x = ln|x|; ∫ eˣ = eˣ; ∫ sin = −cos; ∫ cos = sin.
- Substitution: u = g(x). Parts: ∫u dv = uv − ∫v du, LIATE.
- FTC: ∫ₐᵇ f = F(b) − F(a). Even: 2∫₀ᵃ; odd: 0.
- Area = ∫ (top − bottom). Disc volume = π∫ f². Average = (1/(b − a))∫ f.
- Improper: ∫₁^∞ x^{−p} converges for p > 1.

## Chapter summary

- Integration is reverse differentiation; always add C for indefinite integrals and verify by differentiating.
- Substitution undoes the chain rule, parts undoes the product rule, partial fractions handle rational functions.
- The Fundamental Theorem lets us compute definite integrals from antiderivatives.
- Areas, volumes, averages and total change are all definite integrals; improper integrals are limits.

## Practice

1. Evaluate (a) ∫ (4x³ − 3/x + eˣ) dx, (b) ∫ (x² + 1)² dx, (c) ∫ cos²x dx.
2. Evaluate by substitution (a) ∫ x√(x² + 4) dx, (b) ∫ e^{3x + 1} dx, (c) ∫ sin x cos⁴x dx.
3. Evaluate by parts (a) ∫ x cos x dx, (b) ∫ x e^{2x} dx, (c) ∫ x ln x dx.
4. Evaluate ∫ (2x + 3)/((x − 1)(x + 2)) dx.
5. Evaluate (a) ∫₀² (3x² − 2x) dx, (b) ∫₀^{π/4} sec²x dx, (c) ∫₁^e (ln x)/x dx.
6. Find the area enclosed by y = x² and y = 4x − x².
7. Find the volume generated by revolving y = x² about the x-axis between x = 1 and x = 2.
8. Find the average value of sin x on [0, π].
9. Does ∫₁^∞ 1/√x dx converge? Does ∫₁^∞ 1/x^{3/2} dx?
10. If F(x) = ∫₀ˣ t e^{t} dt find F′(x) and F(1).

::: note Answers and worked solutions
**1.** (a) x⁴ − 3 ln|x| + eˣ + C. (b) x⁵/5 + 2x³/3 + x + C. (c) x/2 + (sin 2x)/4 + C.
**2.** (a) u = x² + 4: ⅓(x² + 4)^{3/2} + C. (b) ⅓ e^{3x + 1} + C. (c) u = cos x: −cos⁵x/5 + C.
**3.** (a) x sin x + cos x + C. (b) (x/2)e^{2x} − e^{2x}/4 + C. (c) (x²/2) ln x − x²/4 + C.
**4.** (2x + 3)/((x − 1)(x + 2)) = A/(x − 1) + B/(x + 2): A = 5/3, B = 1/3. ∫ = **(5/3) ln|x − 1| + (1/3) ln|x + 2| + C**.
**5.** (a) [x³ − x²]₀² = 8 − 4 = **4**. (b) tan(π/4) − 0 = **1**. (c) [ (ln x)²/2 ]₁^e = **1/2**.
**6.** Intersections: x² = 4x − x² ⇒ x = 0, 2. A = ∫₀² (4x − 2x²) dx = [2x² − 2x³/3]₀² = 8 − 16/3 = **8/3**.
**7.** V = π ∫₁² x⁴ dx = π (32 − 1)/5 = **31π/5 ≈ 19.48**.
**8.** (1/π)[−cos x]₀^π = 2/π ≈ **0.637**.
**9.** ∫₁^∞ x^{−1/2} diverges (p = 1/2 ≤ 1). ∫₁^∞ x^{−3/2} = [−2x^{−1/2}]₁^∞ = **2**, converges.
**10.** F′(x) = x eˣ. F(1) = ∫₀¹ t eᵗ dt = [(t − 1)eᵗ]₀¹ = **1**.
:::
