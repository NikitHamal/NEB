---
subject: Numerical Methods
grade: BCA Semester 4
unit: 3
title: Numerical Differentiation and Integration
hours: 5
area: BCA 253 · Numerical Methods · Unit 3
---

A speedometer log gives positions every few seconds: what is the speed? A sensor gives readings: what is the total? Differentiation and integration of *tabulated* data, or of functions with no elementary antiderivative such as e^(−x²) and 1/ln x, must be done numerically. The formulas here come from differentiating or integrating the interpolating polynomials of Unit 2.

::: key What this unit gives you
- Finite-difference formulas for derivatives and their errors; Newton's differentiation formulas.
- Newton–Cotes integration: trapezoidal, Simpson's 1/3 and 3/8 rules, composite versions and error behaviour.
- Romberg integration and numerical double integration.
:::

## 3.1 Numerical differentiation

From f(x + h) = f(x) + hf′(x) + (h²/2)f″(x) + … we get three basic formulas:

| Formula | Expression | Error order |
|---|---|---|
| Forward difference | f′(x) ≈ [f(x + h) − f(x)] / h | O(h) |
| Backward difference | f′(x) ≈ [f(x) − f(x − h)] / h | O(h) |
| **Central difference** | f′(x) ≈ [f(x + h) − f(x − h)] / (2h) | **O(h²)** |
| Central, second derivative | f″(x) ≈ [f(x + h) − 2f(x) + f(x − h)] / h² | O(h²) |

The central formula is better because the first error term cancels. Halving h should cut the forward error by 2 and the central error by 4.

::: example f(x) = eˣ at x = 1 (true f′ = e = 2.718282)
| h | forward (f(x+h)−f(x))/h | error | central (f(x+h)−f(x−h))/2h | error |
|---|---|---|---|---|
| 0.1 | 2.858842 | 0.140560 | 2.722815 | 0.0045327 |
| 0.01 | 2.731919 | 0.013637 | 2.718327 | 0.0000453 |
| 0.001 | 2.719641 | 0.001360 | 2.718282 | 0.0000005 |

Each tenfold reduction of h reduces the forward error about tenfold and the central error about a hundredfold, exactly as the orders say. (The backward formula with h = 0.1 gives 2.586787, an error of the opposite sign to the forward one.) If h is made too small, round-off error (subtracting nearly equal numbers) eventually dominates: there is an optimal h (roughly 10⁻⁸ for the forward formula and 10⁻⁵ for the central formula in double precision), below which the total error grows again.
:::

### Newton's differentiation formulas (tabulated, equally spaced data)

Differentiating Newton's forward formula (Unit 2) with respect to x at x = x₀ (u = 0) gives

**f′(x₀) = (1/h)[Δy₀ − Δ²y₀/2 + Δ³y₀/3 − Δ⁴y₀/4 + …]**

**f″(x₀) = (1/h²)[Δ²y₀ − Δ³y₀ + (11/12)Δ⁴y₀ − …]**

(At the end of a table use the backward versions with ∇ and plus signs.)

::: example Derivatives of ln x at x = 1.0 from a table (true f′(1) = 1, f″(1) = −1)
| x | y = ln x | Δy | Δ²y | Δ³y | Δ⁴y |
|---|---|---|---|---|---|
| 1.0 | 0.000000 | 0.095310 | -0.008299 | 0.001330 | -0.000296 |
| 1.1 | 0.095310 | 0.087011 | -0.006969 | 0.001034 |  |
| 1.2 | 0.182322 | 0.080043 | -0.005935 |  |  |
| 1.3 | 0.262364 | 0.074108 |  |  |  |
| 1.4 | 0.336472 |  |  |  |  |

With h = 0.1, using more terms improves the answer: one term gives 0.953102, two terms 0.994596, three 0.999030, and four terms **f′(1.0) ≈ 0.999770** (error 0.000230). The second derivative from the formula is **f″(1.0) ≈ -0.990045** (true −1; the error is larger because a second derivative loses accuracy).

For an interior point use central formulas instead. At x = 1.2: f′ ≈ (ln 1.3 − ln 1.1)/0.2 = 0.835270 (true 1/1.2 = 0.833333) and f″ ≈ (ln 1.1 − 2 ln 1.2 + ln 1.3)/0.01 = -0.696867 (true −1/1.2² = -0.694444).
:::

**Maxima and minima of a tabulated function.** Differentiate Newton's formula, set dy/du = 0, solve for u (usually a quadratic) and convert to x = x₀ + hu; use the second derivative to classify.

## 3.2 Numerical integration: Newton–Cotes rules

To compute I = ∫ₐᵇ f(x)dx, divide [a, b] into n equal strips of width h = (b − a)/n, xᵢ = a + ih, yᵢ = f(xᵢ), replace f on groups of strips by an interpolating polynomial, and integrate that exactly.

| Rule | Polynomial | Formula (composite) | n must be | Error |
|---|---|---|---|---|
| **Trapezoidal** | line (1 strip) | (h/2)[y₀ + 2(y₁ + … + yₙ₋₁) + yₙ] | any | −(b − a)h²f″(ξ)/12, O(h²) |
| **Simpson's 1/3** | parabola (2 strips) | (h/3)[y₀ + 4(y₁ + y₃ + …) + 2(y₂ + y₄ + …) + yₙ] | **even** | −(b − a)h⁴f⁗(ξ)/180, O(h⁴) |
| **Simpson's 3/8** | cubic (3 strips) | (3h/8)[y₀ + 3(y₁ + y₂ + y₄ + y₅ + …) + 2(y₃ + y₆ + …) + yₙ] | **multiple of 3** | −(b − a)h⁴f⁗(ξ)/80, O(h⁴) |

Simpson's 1/3 rule is exact for polynomials up to degree **3** (not just 2) because the odd error term vanishes; the 3/8 rule is also exact to degree 3. The trapezoidal rule is exact only for lines.

::: example I = ∫₀¹ dx/(1 + x²) = π/4 = 0.785398, with n = 6 (h = 1/6)
Function values:

| i | xᵢ | f(xᵢ) = 1/(1+xᵢ²) |
|---|---|---|
| 0 | 0/6 | 1.000000 |
| 1 | 1/6 | 0.972973 |
| 2 | 2/6 | 0.900000 |
| 3 | 3/6 | 0.800000 |
| 4 | 4/6 | 0.692308 |
| 5 | 5/6 | 0.590164 |
| 6 | 6/6 | 0.500000 |

**Trapezoidal.** h/2 × [y₀ + y₆ + 2(y₁ + … + y₅)] = (1/6)[(1.000000 + 0.500000)/2 + Σ y₁…y₅]: the bracketed sum is 4.705445, so I ≈ **0.784241**, error 0.001157.

**Simpson's 1/3.** (h/3)[y₀ + y₆ + 4(y₁ + y₃ + y₅) + 2(y₂ + y₄)] = (1/18)[1.500000 + 4(2.363137) + 2(1.592308)] = (1/18)(14.137163) = **0.785398**, error 0.0000002.

**Simpson's 3/8.** (3h/8)[y₀ + y₆ + 3(y₁ + y₂ + y₄ + y₅) + 2y₃] gives **0.785396**, error 0.0000023.

Simpson's rules are about a thousand times more accurate than the trapezoidal rule with the same data. (All three results were checked against SciPy's `quad`.)
:::

### Convergence as n grows

| n | trapezoid | error | Simpson 1/3 | error |
|---|---|---|---|---|
| 2 | 0.775000 | 1.04e-02 | 0.783333 | 2.06e-03 |
| 4 | 0.782794 | 2.60e-03 | 0.785392 | 6.01e-06 |
| 8 | 0.784747 | 6.51e-04 | 0.785398 | 3.78e-08 |
| 16 | 0.785235 | 1.63e-04 | 0.785398 | 5.91e-10 |

Each doubling of n divides the trapezoidal error by about 4 (order h²) and the Simpson error by about 16 (order h⁴), as the error terms predict.

**Choosing a rule:** use Simpson's 1/3 when the number of strips is even, the 3/8 rule when it is a multiple of 3, or combine them (3/8 on three strips plus 1/3 on the rest) for odd n. Use the trapezoidal rule for rough work, noisy data, or periodic functions integrated over a full period.

## 3.3 Romberg integration

**Richardson extrapolation** combines two estimates with step h and h/2 to cancel the leading error term. Applied repeatedly to trapezoidal values, it gives the **Romberg table**:

R(k, 0) = trapezoidal rule with 2ᵏ strips; **R(k, j) = R(k, j − 1) + [R(k, j − 1) − R(k − 1, j − 1)] / (4ʲ − 1)**.

Column 1 is Simpson's 1/3 rule, column 2 is Boole's rule, and each further column cancels the next error power (h², h⁴, h⁶, …).

::: example Romberg for ∫₀¹ dx/(1 + x²)
| h | R(k,0) trapezoid | R(k,1) | R(k,2) | R(k,3) | R(k,4) |
|---|---|---|---|---|---|
| 1 | 0.75000000 |  |  |  |  |
| 1/2 | 0.77500000 | 0.78333333 |  |  |  |
| 1/4 | 0.78279412 | 0.78539216 | 0.78552941 |  |  |
| 1/8 | 0.78474712 | 0.78539813 | 0.78539852 | 0.78539645 |  |
| 1/16 | 0.78523540 | 0.78539816 | 0.78539817 | 0.78539816 | 0.78539817 |

The best estimate **R(4, 4) = 0.78539817** differs from π/4 = 0.78539816 by only 2.92e-09 (using just 17 function values). Note that the extrapolated values do not improve in every single entry: R(3, 3) = 0.78539645 has error 1.72e-06, which is larger than R(3, 2). The table improves *in the limit*; the stopping rule is |R(k, k) − R(k − 1, k − 1)| < ε.
:::

## 3.4 Numerical double integration

For I = ∫ₐᵇ∫_c^d f(x, y) dy dx, apply a one-dimensional rule in each direction. With a grid hₓ × k_y, the composite rule is a double sum of the weights times function values. For Simpson's 1/3 with two strips in each direction the weights form the grid

| | y₀ | y₁ | y₂ |
|---|---|---|---|
| **x₀** | 1 | 4 | 1 |
| **x₁** | 4 | 16 | 4 |
| **x₂** | 1 | 4 | 1 |

and I ≈ (hₓk/9) Σ wᵢⱼ f(xᵢ, yⱼ). For the trapezoidal rule the weights are ¼, ½, ¼ products and I ≈ hₓk Σ wᵢⱼ f.

::: example ∫₀¹∫₁² dy dx/(x + y), with h = k = 0.5
The exact value is 3 ln 3 − 4 ln 2 = 0.523248.

| f(x,y) = 1/(x+y) | y = 1 | y = 1.5 | y = 2 |
|---|---|---|---|
| x = 0 | 1.000000 | 0.666667 | 0.500000 |
| x = 0.5 | 0.666667 | 0.500000 | 0.400000 |
| x = 1.0 | 0.500000 | 0.400000 | 0.333333 |

Simpson (weights 1, 4, 1): I ≈ (0.5 × 0.5/9) × Σ = **0.524074**, error 0.000826. Trapezoidal: **0.537500**, error 0.014252. Even with only nine points Simpson is accurate to 3 decimals. A smaller step or a Romberg refinement in each direction would improve both.
:::

## Formula and fact sheet

- Forward/backward: O(h); central: [f(x + h) − f(x − h)]/2h, O(h²); f″ ≈ [f(x + h) − 2f(x) + f(x − h)]/h².
- Trapezoidal: (h/2)[y₀ + 2Σyᵢ + yₙ]. Simpson 1/3 (n even): (h/3)[y₀ + 4Σodd + 2Σeven + yₙ]. Simpson 3/8 (n multiple of 3): (3h/8)[…].
- Error orders: trapezoid h², Simpson h⁴.
- Romberg: R(k, j) = R(k, j − 1) + [R(k, j − 1) − R(k − 1, j − 1)]/(4ʲ − 1).
- Double integral: weighted sum with product weights.

## Chapter summary

- Derivatives come from differentiating interpolation polynomials; central differences are second-order and best; too small an h lets round-off dominate.
- Newton–Cotes rules integrate interpolating polynomials; Simpson's rules beat the trapezoidal rule at the same cost.
- Romberg extrapolation turns cheap trapezoidal values into a high-order estimate.
- Double integrals reuse the one-dimensional rules with product weights.

## Practice

1. Derive the forward-difference formula for f′(x) from Taylor's series and state its order.
2. For f(x) = eˣ at x = 1 with h = 0.1, compute forward and central estimates and their errors.
3. Estimate f′(1.0) and f″(1.0) for ln x from the difference table, using Newton's forward formulas.
4. Evaluate ∫₀¹ dx/(1 + x²) with n = 6 by the trapezoidal, Simpson 1/3 and Simpson 3/8 rules.
5. Why must n be even for Simpson's 1/3 rule and a multiple of 3 for the 3/8 rule?
6. How many times smaller is the error expected after halving h for the trapezoidal rule and for Simpson's rule?
7. Build a Romberg table with four trapezoidal estimates and extrapolate.
8. Estimate ∫₀¹∫₁² dy dx/(x + y) with Simpson's rule, h = k = 0.5, and compare it with the exact value.
9. State two reasons why a very small h does not give a better numerical derivative.

::: note Answers and worked solutions
**1.** f(x + h) = f(x) + hf′(x) + (h²/2)f″(ξ). Rearranging, f′(x) = [f(x + h) − f(x)]/h − (h/2)f″(ξ). The truncation error is proportional to h: first order, O(h).
**2.** The table in Section 3.1 gives forward 2.858842 (error 0.140560) and central 2.722815 (error 0.0045327) for h = 0.1.
**3.** From the difference table: f′(1.0) ≈ 0.999770 and f″(1.0) ≈ -0.990045 (true values 1 and −1).
**4.** Trapezoidal 0.784241; Simpson 1/3 0.785398; Simpson 3/8 0.785396; true 0.785398.
**5.** Simpson's 1/3 fits a parabola through three points, covering two strips, so strips must be paired. The 3/8 rule fits a cubic through four points, covering three strips.
**6.** Trapezoid error ∝ h², so halving h divides it by about 4; Simpson ∝ h⁴, so by about 16 (compare the convergence table in Section 3.2).
**7.** See the Romberg table in Section 3.3: the extrapolated R(4, 4) = 0.78539817.
**8.** Simpson: 0.524074; exact: 0.523248; error 0.000826 (the trapezoidal rule gives 0.537500).
**9.** Truncation error falls with h, but round-off grows because f(x + h) − f(x) subtracts nearly equal numbers, then is divided by a tiny h; and measured data carry noise which is amplified by 1/h. Beyond an optimal h the total error increases.
:::
