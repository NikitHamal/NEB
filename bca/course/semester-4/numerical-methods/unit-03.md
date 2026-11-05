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

## 3.5 Seeing the ideas: areas under curves, Romberg's table and the error of a derivative

Before computers, engineers measured the area of an irregular shape with a mechanical **planimeter**, a hand-driven integrator. Numerical integration does the same job with arithmetic.

```photogrid label="3.1" cols="2" ratio="1.2" caption="Integration by machine and by rule. (a) A Keuffel and Esser polar planimeter in its case: tracing the boundary of a shape with the pointer gives its area on the dial, a mechanical integrator used by surveyors and engineers. (b) The trapezoidal rule on one quarter-wave of sin x with step pi/4: straight tops replace the curve, so the area is slightly underestimated for a concave curve."
@ photo id="bca204/planimeter" cap="Polar planimeter"
fit 1.2
focus 0.5 0.5
@ svg cap="Trapezoids under sin x"
f = Fig(300, 230)
ax = Axes(f, 30, 14, 250, 170, (0, 3.2), (0, 1.2))
ax.grid(0.8, 0.4)
ax.axes("", "")
import math
h = math.pi / 4
for k in range(4):
    x0, x1 = k * h, (k + 1) * h
    f.poly([(ax.X(x0), ax.Y(0)), (ax.X(x0), ax.Y(math.sin(x0))), (ax.X(x1), ax.Y(math.sin(x1))), (ax.X(x1), ax.Y(0))], fill="#bfdbfe", stroke=NAVY, sw=1.2)
ax.curve(math.sin, 0, math.pi, color=RED)
f.text(165, 210, "T = 1.89612 vs exact 2 (error 0.104)", size=10, color=NAVY, bold=True)
```

```svgfig label="3.1" caption="Simpson's one-third rule fits a parabola through each pair of strips. On the same four strips for the integral of sin x from 0 to pi, the trapezoidal rule gives 1.89612 (error 0.10388) while Simpson gives 2.00456 (error -0.00456), more than twenty times better for the same ordinates 0, 0.70711, 1, 0.70711, 0."
f = Fig(580, 200)
ax = Axes(f, 50, 14, 510, 150, (0, 3.2), (0, 1.2))
ax.grid(0.4, 0.4)
ax.axes("", "")
import math
ax.area(math.sin, 0, math.pi)
ax.curve(math.sin, 0, math.pi, color=NAVY)
for k in range(5): ax.pt(k * math.pi / 4, math.sin(k * math.pi / 4), "y%d" % k, dx=0, dy=-10, anchor="middle", size=10)
f.text(306, 190, "S = (h/3)[y0 + 4(y1 + y3) + 2 y2 + y4] = 2.00456 | weights 1 4 2 4 1", size=10.5, color=TEAL, bold=True)
```

```svgfig label="3.2" caption="Romberg integration of e^x on [0, 1] (exact value 1.718282). The first column is the trapezoidal rule with 1, 2 and 4 strips; each later column is Richardson extrapolation R(i,j) = R(i,j-1) + [R(i,j-1) - R(i-1,j-1)]/(4^j - 1). Three trapezoid values combine into 1.718283, correct to six decimals."
f = Fig(580, 168)
T = [["1.859141"], ["1.753931", "1.718861"], ["1.727222", "1.718319", "1.718283"]]
H = ["h = 1", "h = 1/2", "h = 1/4"]
for j, h in enumerate(["trapezoid", "O(h^4)", "O(h^6)"]): f.box(130 + j * 150, 8, 140, 22, h, fill=NAVY, stroke=NAVY, color="#ffffff", bold=True, size=10.5)
for i, r in enumerate(T):
    f.box(8, 38 + i * 36, 110, 28, H[i], fill=BLUE, stroke=NAVY, size=10.5)
    for j, v in enumerate(r):
        f.box(130 + j * 150, 38 + i * 36, 140, 28, v, fill=[MINT, SAND, ROSE][j], stroke=[TEAL, AMBER, RED][j], size=11, bold=(i == 2 and j == 2))
f.text(290, 160, "exact value: 1.718282", size=10.5, color=TEAL, bold=True)
```

```svgfig label="3.3" caption="Error of two derivative formulas for f(x) = e^x at x = 1 (exact 2.71828). Halving h halves the forward-difference error (0.14056 to 0.06910) but quarters the central-difference error (0.00453 to 0.00113), because the forward formula is O(h) and the central formula is O(h^2)."
f = Fig(580, 180)
D = [("Forward h = 0.1", 0.14056, AMBER, SAND), ("Forward h = 0.05", 0.0691, AMBER, SAND), ("Central h = 0.1", 0.00453, TEAL, MINT), ("Central h = 0.05", 0.00113, TEAL, MINT)]
for i, (t, e, st, fl) in enumerate(D):
    y = 14 + i * 40
    f.text(120, y + 17, t, size=10.5, color=NAVY, bold=True, anchor="end")
    f.box(130, y, max(e * 2800, 4), 28, "", fill=fl, stroke=st)
    f.text(130 + max(e * 2800, 4) + 8, y + 18, "error %.5f" % e, size=10.5, color=SLATE, bold=True, anchor="start")
```

### 3.5.1 Eight uses of numerical integration and differentiation

1. **Area and volume of irregular shapes.** Land surveyors in Nepal measure a field boundary at fixed intervals, and Simpson's rule gives the area. The same idea gives the volume of earth to cut for a road. No formula for the shape is needed.
2. **Water in a river or reservoir.** Flow is measured at several depths and widths. Integrating velocity times area gives the discharge in cubic metres per second. Hydropower planning for rivers such as the Kaligandaki depends on this.
3. **Distance from speed.** A vehicle log gives speed at each minute, and integration adds it into distance travelled. Fitness watches and GPS units do this all day. The trapezoidal rule is enough for such data.
4. **Work, energy and charge.** The work done by a variable force and the charge stored from a varying current are integrals of measured tables. Engineers use numerical integration when the signal is only a list of readings. Oscilloscopes do this inside.
5. **Probability and statistics.** The normal distribution has no closed-form integral, so the tables in textbooks were made numerically. Computers still integrate to find probabilities and p-values. This is the root of all statistical software.
6. **Rates of change from data.** Speed from positions, growth rate from population counts and slope of a sensor curve are numerical derivatives. A central difference gives a good estimate from two neighbouring readings. It is used in control systems and tracking.
7. **Error control by Romberg and step halving.** Halving the step and extrapolating improves the answer without a formula for the error. We know how many digits to trust. This makes numerical results reliable.
8. **Solving differential equations.** Euler and Runge-Kutta methods in the next unit are built from the same ideas of stepping and averaging slopes. Understanding integration therefore opens the way to simulation. Weather and engineering models rest on it.

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

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Evaluate the integral of sin x from 0 to pi using the trapezoidal rule and Simpson's one-third rule with four strips. Compare with the exact value.**

*Data.* h = pi/4 = 0.785398; the ordinates are y0 = 0, y1 = 0.70711, y2 = 1, y3 = 0.70711, y4 = 0.

*Trapezoidal rule.* T = (h/2)[y0 + 2(y1 + y2 + y3) + y4] = 0.392699 x [0 + 2(2.41421) + 0] = **1.89612**.

*Simpson's rule.* S = (h/3)[y0 + 4(y1 + y3) + 2 y2 + y4] = 0.261799 x [0 + 4(1.41421) + 2 + 0] = 0.261799 x 7.65685 = **2.00456**.

| Rule | Value | Exact | Error |
|---|---|---|---|
| Trapezoidal | 1.89612 | 2 | 0.10388 |
| Simpson 1/3 | 2.00456 | 2 | -0.00456 |

Simpson is more than twenty times more accurate for the same ordinates (Figure 3.1) because it fits parabolas, not straight lines; its error is of order h^4, against h^2 for the trapezoidal rule. *Condition:* Simpson's 1/3 rule needs an even number of strips. *Conclusion:* use Simpson's rule for smooth functions.

**Q2 (5 marks). Estimate the derivative of e^x at x = 1 by the forward and central difference formulas with h = 0.1 and h = 0.05, and comment on the errors.**

*Formulas.* Forward: f'(x) is about [f(x+h) - f(x)]/h, error O(h). Central: f'(x) is about [f(x+h) - f(x-h)]/(2h), error O(h^2). Exact value e = 2.71828.

| h | Forward | Error | Central | Error |
|---|---|---|---|---|
| 0.1 | 2.85884 | 0.14056 | 2.72281 | 0.00453 |
| 0.05 | 2.78739 | 0.06910 | 2.71941 | 0.00113 |

Halving h halves the forward error (0.14056 to 0.06910) but divides the central error by four (0.00453 to 0.00113), as the orders predict (Figure 3.3). *Warning:* making h extremely small loses accuracy through rounding error in the subtraction. *Conclusion:* prefer the central formula when values on both sides are available.

**Q3 (10 marks). Explain the Newton-Cotes rules and Romberg integration. Apply Romberg's method to the integral of e^x on [0, 1].**

*Introduction.* When an integral has no closed form or the integrand is only a table, we replace f by an interpolating polynomial and integrate that (Plate 3.1 shows an older mechanical way). The resulting formulas are the **Newton-Cotes rules**.

*Rules.* (1) **Trapezoidal:** integral is about (h/2)[y0 + 2(y1 + ... + y(n-1)) + yn], error -(b-a)h^2 f''/12. (2) **Simpson 1/3:** (h/3)[y0 + 4(odd) + 2(even) + yn], n even, error -(b-a)h^4 f''''/180. (3) **Simpson 3/8:** (3h/8)[y0 + 3y1 + 3y2 + 2y3 + ... + yn], n a multiple of 3, same order. Figure 3.1 compares the first two.

*Romberg.* The trapezoidal error expands in even powers of h, so **Richardson extrapolation** removes them one by one: R(i,j) = R(i,j-1) + [R(i,j-1) - R(i-1,j-1)]/(4^j - 1). Start with trapezoid values for h = 1, 1/2, 1/4: T(1) = 0.5(1 + 2.718282) = 1.859141; T(2) = 1.753931; T(4) = 1.727222.

First extrapolation: R(2,1) = 1.753931 + (1.753931 - 1.859141)/3 = **1.718861**; R(3,1) = 1.727222 + (1.727222 - 1.753931)/3 = **1.718319**. Second: R(3,2) = 1.718319 + (1.718319 - 1.718861)/15 = **1.718283**, against the exact e - 1 = 1.718282 (Figure 3.2).

| Rule | Order of error | Needs | Best for |
|---|---|---|---|
| Trapezoidal | h^2 | any n | rough data, periodic functions |
| Simpson 1/3 | h^4 | even n | smooth functions |
| Simpson 3/8 | h^4 | n multiple of 3 | odd strips |
| Romberg | h^2, h^4, h^6 ... | halving h | high accuracy by reuse |

*Conclusion.* Romberg integration reaches six correct decimals from only four function evaluations beyond the trapezoid starts, and the difference between successive entries gives a built-in error estimate. Use Simpson for a quick answer and Romberg when high accuracy is required.
