---
subject: Mathematics I
grade: BCA Semester 1
unit: 6
title: Differential Equations
area: BCA 104 · Mathematics I · Unit 6
---

A **differential equation (DE)** relates a function to its derivatives. Populations, cooling, circuits, vibrations and algorithms' running times all obey differential equations. This unit covers the methods that solve the common first-order types and second-order linear equations with constant coefficients, and shows how to model with them.

::: key What this unit gives you
- Order, degree, general and particular solutions; forming a DE.
- First-order methods: separable, homogeneous, linear (integrating factor), exact.
- Second-order linear homogeneous equations with constant coefficients.
- Models: growth and decay, Newton's law of cooling.
:::

## 6.1 Basic terms

The **order** of a DE is the order of the highest derivative; the **degree** is the power of that derivative once the equation is a polynomial in derivatives. dy/dx = xy is order 1, degree 1; (y″)² + y′ = 0 is order 2, degree 2.

The **general solution** has as many arbitrary constants as the order. A **particular solution** fixes them with **initial conditions**, giving an initial-value problem (IVP).

**Forming a DE** from a family of curves: differentiate to eliminate the constants. For y = Ae^{2x} + Be^{−x}: y′ = 2Ae^{2x} − Be^{−x}, y″ = 4Ae^{2x} + Be^{−x}. Then y″ − y′ − 2y = 0 (check: coefficient of A: 4 − 2 − 2 = 0, of B: 1 + 1 − 2 = 0 ✓).

## 6.2 Separable equations

If dy/dx = f(x) g(y), separate: dy/g(y) = f(x) dx and integrate both sides.

::: example Worked example
**dy/dx = xy.** dy/y = x dx ⇒ ln|y| = x²/2 + c ⇒ **y = Ce^{x²/2}**.
**dy/dx = (1 + y²)/(1 + x²), y(0) = 1.** tan⁻¹y = tan⁻¹x + c; y(0) = 1 gives c = π/4, so y = tan(tan⁻¹x + π/4) = (x + 1)/(1 − x).
**(1 + x²) dy = (1 + y) x dx.** Separate: dy/(1 + y) = x dx/(1 + x²) ⇒ ln|1 + y| = ½ ln(1 + x²) + c ⇒ 1 + y = C√(1 + x²).
:::

## 6.3 Homogeneous equations

dy/dx = F(y/x), or more generally M and N homogeneous of the same degree. Substitute **y = vx**, dy/dx = v + x dv/dx; it becomes separable in v and x.

::: example Worked example
**dy/dx = (x + y)/x.** With y = vx: v + x v′ = 1 + v ⇒ x v′ = 1 ⇒ v = ln|x| + C. So **y = x(ln|x| + C)**.
**dy/dx = (x² + y²)/(2xy).** v + x v′ = (1 + v²)/(2v) ⇒ x v′ = (1 − v²)/(2v) ⇒ 2v dv/(1 − v²) = dx/x ⇒ −ln|1 − v²| = ln|x| + c ⇒ x(1 − v²) = C ⇒ **x² − y² = Cx**.
:::

## 6.4 Linear first-order equations

Standard form **dy/dx + P(x) y = Q(x)**. Multiply by the **integrating factor** μ = e^{∫P dx}; the left side becomes (μ y)′, so **μ y = ∫ μ Q dx + C**.

::: example Worked example
**dy/dx + 2y = e^{−x}.** μ = e^{2x}. (y e^{2x})′ = e^{x} ⇒ y e^{2x} = eˣ + C ⇒ **y = e^{−x} + Ce^{−2x}**. Check: y′ + 2y = −e^{−x} − 2Ce^{−2x} + 2e^{−x} + 2Ce^{−2x} = e^{−x} ✓.
**x dy/dx + y = x².** Divide by x: y′ + y/x = x, μ = e^{ln x} = x, (xy)′ = x² ⇒ xy = x³/3 + C ⇒ **y = x²/3 + C/x**.
**dy/dx − y tan x = sec x.** μ = e^{−∫tan x dx} = cos x; (y cos x)′ = 1 ⇒ y cos x = x + C ⇒ y = (x + C) sec x.
:::

## 6.5 Exact equations

M(x, y) dx + N(x, y) dy = 0 is **exact** if ∂M/∂y = ∂N/∂x. Then there is F with F_x = M, F_y = N and the solution is F(x, y) = C. Find F by integrating M with respect to x (treating y as constant), adding a function g(y), and matching F_y = N.

::: example Worked example
(2xy + 3) dx + (x² + 4y) dy = 0. M_y = 2x = N_x ✓ exact. F = ∫ (2xy + 3) dx = x²y + 3x + g(y); F_y = x² + g′(y) = x² + 4y ⇒ g = 2y². Solution: **x²y + 3x + 2y² = C**.
:::

## 6.6 Second-order linear equations with constant coefficients

**a y″ + b y′ + c y = 0.** Try y = e^{mx}: it gives the **auxiliary (characteristic) equation** a m² + b m + c = 0. The roots decide the solution:

| Roots | General solution |
|---|---|
| Real, distinct m₁ ≠ m₂ | y = C₁e^{m₁x} + C₂e^{m₂x} |
| Real, repeated m | y = (C₁ + C₂x) e^{mx} |
| Complex α ± iβ | y = e^{αx}(C₁ cos βx + C₂ sin βx) |

::: example Worked example
**y″ − 5y′ + 6y = 0.** m² − 5m + 6 = 0 ⇒ m = 2, 3 ⇒ **y = C₁e^{2x} + C₂e^{3x}**.
**y″ − 4y′ + 4y = 0.** (m − 2)² = 0 ⇒ **y = (C₁ + C₂x)e^{2x}**.
**y″ + 4y = 0.** m = ±2i ⇒ **y = C₁ cos 2x + C₂ sin 2x** (simple harmonic motion).
**y″ + 2y′ + 5y = 0.** m = −1 ± 2i ⇒ y = e^{−x}(C₁ cos 2x + C₂ sin 2x), a decaying oscillation.
**IVP: y″ − 3y′ + 2y = 0, y(0) = 1, y′(0) = 0.** m = 1, 2: y = C₁eˣ + C₂e^{2x}. y(0): C₁ + C₂ = 1; y′(0): C₁ + 2C₂ = 0 ⇒ C₂ = −1, C₁ = 2. So **y = 2eˣ − e^{2x}**.
:::

**Non-homogeneous equation** a y″ + b y′ + c y = f(x): the general solution is y = y_c + y_p, where y_c is the solution of the homogeneous equation and y_p is any particular solution (found by trial form). For y″ − 3y′ + 2y = 4: try y_p = k, so 2k = 4, k = 2 and y = C₁eˣ + C₂e^{2x} + 2.

## 6.7 Modelling with differential equations

**Growth and decay**: dN/dt = kN ⇒ N = N₀e^{kt}. (k > 0 growth, k < 0 decay.)

**Newton's law of cooling**: dT/dt = −k (T − Tₛ) ⇒ T(t) = Tₛ + (T₀ − Tₛ) e^{−kt}.

::: example Worked example: radioactive decay
A sample of 80 g has half-life 5 years. N = 80 e^{−kt}, and N(5) = 40 ⇒ e^{−5k} = ½. After 15 years: N = 80 (½)³ = **10 g**.
:::

::: example Worked example: population
A population doubles in 10 years. N = N₀e^{kt}, e^{10k} = 2, k = ln 2/10. Tripling: e^{kt} = 3 ⇒ t = ln 3/k = 10 ln 3/ln 2 ≈ **15.85 years**.
:::

::: example Worked example: cooling coffee
Coffee at 90 °C in a 30 °C room cools to 70 °C in 5 minutes. T = 30 + 60e^{−kt}; 70 = 30 + 60 e^{−5k} ⇒ e^{−5k} = 2/3. At 10 min: T = 30 + 60 (2/3)² = 30 + 26.67 = **56.7 °C**.
:::

**Algorithms and recurrence.** The divide-and-conquer recurrence T(n) = 2T(n/2) + n has the continuous analogue whose solution is T(n) = n log₂ n; the same exponential patterns (e^{kt}) appear in compound interest, cache decay and network traffic models.

## Formula and fact sheet

- Separable: ∫ dy/g = ∫ f dx. Homogeneous: y = vx.
- Linear: μ = e^{∫P}; μy = ∫ μQ + C.
- Exact: M_y = N_x; F = C.
- a m² + b m + c = 0: distinct → eᵐ¹ˣ, eᵐ²ˣ; repeated → (C₁ + C₂x)eᵐˣ; complex → eᵅˣ(cos, sin).
- Growth: N = N₀e^{kt}. Half-life t½ = ln 2/k. Cooling: T = Tₛ + (T₀ − Tₛ)e^{−kt}.

## Chapter summary

- The order sets the number of constants; initial conditions pick a particular solution.
- Separable, homogeneous, linear and exact first-order equations each have a systematic method.
- Constant-coefficient second-order equations reduce to an auxiliary quadratic whose roots give exponentials, polynomial-times-exponential, or oscillations.
- Growth, decay and cooling are first-order linear models with exponential solutions.

## Practice

1. Solve dy/dx = y/x, y(1) = 3.
2. Solve dy/dx = (1 + y²)x.
3. Solve the homogeneous equation dy/dx = (x² + y²)/(xy).
4. Solve dy/dx + y/x = x³ and find the solution with y(1) = 1.
5. Check exactness and solve (3x² y + 2) dx + (x³ + 4y) dy = 0.
6. Solve y″ + y′ − 6y = 0, y″ − 6y′ + 9y = 0 and y″ + 9y = 0.
7. Solve y″ − 4y = 0, y(0) = 2, y′(0) = 0.
8. A culture of 1000 bacteria grows to 3000 in 4 hours. How many after 10 hours?
9. A body at 100 °C is placed in 20 °C surroundings and cools to 60 °C in 10 minutes. When does it reach 30 °C?
10. Form the differential equation of the family y = A cos x + B sin x.

::: note Answers and worked solutions
**1.** dy/y = dx/x ⇒ y = Cx; y(1) = 3 ⇒ **y = 3x**.
**2.** dy/(1 + y²) = x dx ⇒ tan⁻¹y = x²/2 + c ⇒ **y = tan(x²/2 + c)**.
**3.** Put y = vx: v + x v′ = (1 + v²)/v ⇒ x v′ = 1/v ⇒ v dv = dx/x ⇒ v²/2 = ln|x| + c ⇒ **y² = 2x²(ln|x| + C)**. Check by differentiating: 2yy′ = 4x ln|x| + 2x + 2Cx, which equals 2y·(x² + y²)/(xy) = 2(x² + y²)/x once y² is substituted ✓.
**4.** μ = x; (xy)′ = x⁴ ⇒ xy = x⁵/5 + C ⇒ y = x⁴/5 + C/x. y(1) = 1: 1/5 + C = 1 ⇒ C = 4/5: **y = x⁴/5 + 4/(5x)**.
**5.** M_y = 3x² = N_x ✓. F = x³y + 2x + g(y); F_y = x³ + g′ = x³ + 4y ⇒ g = 2y². **x³y + 2x + 2y² = C**.
**6.** m² + m − 6 = (m + 3)(m − 2): **y = C₁e^{−3x} + C₂e^{2x}**. (m − 3)² = 0: **y = (C₁ + C₂x)e^{3x}**. m = ±3i: **y = C₁ cos 3x + C₂ sin 3x**.
**7.** m = ±2: y = C₁e^{2x} + C₂e^{−2x}; C₁ + C₂ = 2, 2C₁ − 2C₂ = 0 ⇒ C₁ = C₂ = 1: **y = 2 cosh 2x = e^{2x} + e^{−2x}**.
**8.** N = 1000e^{kt}, e^{4k} = 3, k = ln 3/4. N(10) = 1000 · 3^{2.5} = 1000 × 15.59 ≈ **15,588**.
**9.** T = 20 + 80e^{−kt}; 60 = 20 + 80e^{−10k} ⇒ e^{−10k} = ½, k = ln 2/10. T = 30: 80 e^{−kt} = 10 ⇒ e^{−kt} = 1/8 ⇒ t = 3 × 10 = **30 minutes**.
**10.** y″ = −A cos x − B sin x = −y, so **y″ + y = 0**.
:::
