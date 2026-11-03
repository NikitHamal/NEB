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

```svgfig label="6.1" caption="A slope field for dy/dx = x − y. At each grid point a short segment shows the slope that the equation demands, so a solution is a curve that follows the segments. The general solution is y = x − 1 + Ce⁻ˣ; the three curves drawn have C = −1, 0 and 2. The IVP y(0) = 1 selects C = 2."
f = Fig(740, 300)
a = Axes(f, 30, 10, 280, 280, (-2, 4), (-2, 4)); a.grid(1, 1, size=8.5)
for i in range(13):
    for j in range(13):
        x, y = -2 + i * 0.5, -2 + j * 0.5; s = x - y; n = math.hypot(1, s)
        dx, dy = 8 / n, -8 * s / n; cx, cy = a.X(x), a.Y(y)
        f.line(cx - dx, cy - dy, cx + dx, cy + dy, color="#94a3b8", sw=1.3)
a.axes()
for C, col in [(-1, TEAL), (0, AMBER), (2, RED)]: a.curve(lambda x, C=C: x - 1 + C * math.exp(-x), color=col, sw=2.4)
a.pt(0, 1, "y(0) = 1", dx=8, dy=-10)
rows = [("y = x − 1 + 2e⁻ˣ", "C = 2 (red): passes through (0, 1)", RED), ("y = x − 1", "C = 0 (amber): the straight-line solution", AMBER), ("y = x − 1 − e⁻ˣ", "C = −1 (teal)", TEAL)]
f.text(350, 30, "Check the red curve against the equation", size=12, color=NAVY, bold=True, anchor="start")
for i, (e, d, col) in enumerate(rows):
    f.box(350, 44 + i * 56, 370, 46, "", fill=SOFT, stroke=col); f.text(362, 64 + i * 56, e, size=12, color=col, bold=True, anchor="start"); f.text(362, 82 + i * 56, d, size=10, color=SLATE, anchor="start")
f.text(350, 232, "y′ = 1 − 2e⁻ˣ and x − y = 1 − 2e⁻ˣ  ✓", size=11.5, color=TEAL, bold=True, anchor="start")
f.text(350, 252, "A DE has a family of solutions; initial conditions pick one.", size=10.5, color=SLATE, anchor="start")
```

```svgfig label="6.2" caption="Which method? A decision chain for first-order equations: test the equation against each form in turn. If none fits, try an integrating factor or a substitution, or solve numerically."
f = Fig(740, 270)
qs = [("Can it be written dy/dx = f(x)·g(y)?", "Separable: dy/g(y) = f(x) dx, integrate both sides"), ("Is it dy/dx + P(x)y = Q(x)?", "Linear: multiply by μ = e^(∫P dx), then (μy)′ = μQ"), ("Is M dx + N dy = 0 with ∂M/∂y = ∂N/∂x?", "Exact: find F with F_x = M, F_y = N; F = C"), ("Is dy/dx = F(y/x) (all terms of same degree)?", "Homogeneous: put y = vx, then it becomes separable")]
for i, (q, ans) in enumerate(qs):
    y = 10 + i * 64
    f.box(10, y, 330, 46, q, fill=BLUE, stroke=NAVY, size=11, bold=True)
    f.arrow([(340, y + 23), (385, y + 23)], color=TEAL, sw=2, label="yes", lpos=(362, y + 14))
    f.box(390, y, 340, 46, ans, fill=MINT, stroke=TEAL, size=10.5)
    if i < 3: f.arrow([(175, y + 46), (175, y + 64)], color=RED, sw=1.8, label="no", lpos=(190, y + 58))
```

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

```svgfig label="6.3" caption="The three cases of y″ + by′ + cy = 0 with y(0) = 1, y′(0) = 0, as the motion of a mass on a spring with a shock absorber. Complex roots give a decaying wave (under-damped), a repeated root gives the fastest return without overshoot (critically damped), and two distinct real roots give a slow creep back (over-damped)."
f = Fig(780, 280)
a = Axes(f, 44, 14, 400, 235, (0, 6), (-0.4, 1.15)); a.grid(1, 0.2, size=8.5).axes("t", "y")
a.curve(lambda t: math.exp(-t) * (math.cos(2 * t) + 0.5 * math.sin(2 * t)), color=NAVY, sw=2.6)
a.curve(lambda t: (1 + t) * math.exp(-t), color=TEAL, sw=2.6); a.curve(lambda t: 2 * math.exp(-t) - math.exp(-2 * t), color=RED, sw=2.6)
rows = [("Under-damped", "y″ + 2y′ + 5y = 0", "m = −1 ± 2i", "y = e⁻ᵗ(cos 2t + ½ sin 2t)", NAVY), ("Critically damped", "y″ + 2y′ + y = 0", "m = −1 (repeated)", "y = (1 + t)e⁻ᵗ", TEAL), ("Over-damped", "y″ + 3y′ + 2y = 0", "m = −1, −2", "y = 2e⁻ᵗ − e⁻²ᵗ", RED)]
for i, (n, eq, r, sol, c) in enumerate(rows):
    y = 14 + i * 84
    f.box(470, y, 300, 76, "", fill=SOFT, stroke=c); f.text(482, y + 18, n, size=12, color=c, bold=True, anchor="start"); f.text(482, y + 36, eq + "   " + r, size=10, color=SLATE, anchor="start"); f.text(482, y + 60, sol, size=11.5, color=c, bold=True, anchor="start")
```

```svgfig label="6.4" caption="Two models from the chapter. (a) Newton's law of cooling, dT/dt = −k(T − 25): a cup of tea at 80 °C in a 25 °C room follows T = 25 + 55e⁻ᵏᵗ with k = 0.0452 per minute (60 °C after 10 min). (b) Logistic growth, dP/dt = 0.5P(1 − P/1000): a colony starting at 100 levels off at the carrying capacity 1000."
f = Fig(780, 270)
f.box(8, 4, 380, 262, "", fill=SOFT, stroke="#cbd5e1"); f.text(198, 22, "(a) cooling of tea", size=11.5, color=NAVY, bold=True)
k = math.log(55 / 35) / 10
a = Axes(f, 50, 34, 316, 190, (0, 60), (0, 90)); a.grid(10, 20, size=8.5).axes("t (min)", "T (°C)")
a.curve(lambda t: 25 + 55 * math.exp(-k * t), color=NAVY, sw=2.6); a.hline(25, color=AMBER)
a.pt(0, 80, "80 °C", dx=8, dy=-6); a.pt(10, 60, "60 °C at 10 min", color=TEAL, dx=10, dy=-8); a.pt(28.7, 40, "40 °C at 28.7 min", color=RED, dx=10, dy=-10)
f.text(a.X(42), a.Y(25) + 14, "room 25 °C", size=10, color=AMBER, bold=True, anchor="start"); f.text(198, 254, "T = 25 + 55e^(−0.0452t)", size=11, color=TEAL, bold=True)
f.box(396, 4, 376, 262, "", fill=SOFT, stroke="#cbd5e1"); f.text(584, 22, "(b) logistic growth", size=11.5, color=NAVY, bold=True)
b = Axes(f, 436, 34, 316, 190, (0, 20), (0, 1100)); b.grid(5, 250, size=8.5).axes("t", "P")
b.curve(lambda t: 1000 / (1 + 9 * math.exp(-0.5 * t)), color=NAVY, sw=2.6); b.hline(1000, color=AMBER)
b.pt(0, 100, "P₀ = 100", dx=8, dy=-8); b.pt(math.log(9) / 0.5, 500, "fastest growth at P = 500", color=RED, dx=10, dy=18)
f.text(b.X(11), b.Y(1000) - 6, "carrying capacity K = 1000", size=10, color=AMBER, bold=True, anchor="start"); f.text(584, 254, "P = 1000 / (1 + 9e^(−0.5t))", size=11, color=TEAL, bold=True)
```

```photogrid label="6.1" cols="3" ratio="1.2" caption="Differential equations in the real world. (a) A hot cup cools at a rate proportional to the temperature difference with the room, dT/dt = −k(T − Tₛ). (b) Bacterial colonies on an agar plate grow almost exponentially at first and then slow down as food runs out (logistic). (c) A coil spring obeys Hooke's law, so a mass on it satisfies m y″ + k y = 0, simple harmonic motion."
@ photo id="bca104/coffee" cap="Hot drink: Newton's cooling law"
fit 1.2
call 0.5 0.93 0.5 0.6 "dT/dt = −k(T − 25)"
@ photo id="bca104/ecoli" cap="E. coli colonies on agar: growth"
fit 1.2
call 0.5 0.93 0.5 0.6 "dP/dt = rP(1 − P/K)"
@ photo id="bca104/spring" cap="Coil spring: oscillation"
fit 1.2
call 0.5 0.93 0.5 0.62 "m y″ + k y = 0"
```

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

## 6.8 Eight uses of differential equations

1. **Cooling and heating.** Newton's law dT/dt = −k(T − Tₛ) tells how fast tea, a motor or a server cools (Figure 6.4a). A hostel kitchen can use it to know when soup is safe to serve. Forensic doctors use the same law to estimate the time of death.
2. **Population and bacteria growth.** Simple growth dP/dt = kP gives exponential growth, and the logistic equation adds a limit (Figure 6.4b). Health workers use these models to predict how fast an infection spreads in a ward. City planners use them for the population of Kathmandu Valley.
3. **Money and finance.** Interest compounded continuously satisfies dA/dt = rA, so A = A₀eʳᵗ. A bank in Nepal can compare a deposit that earns 8% yearly with one that compounds daily. Loan repayments with continuous payments are also modelled by a linear first-order equation.
4. **Spring and vibration systems.** A mass on a spring obeys m y″ + c y′ + k y = 0, and the roots of its characteristic equation decide the motion (Figure 6.3). Vehicle shock absorbers on rough Nepali roads are designed as critically damped systems. Earthquake engineers study the same equation for buildings.
5. **Electric circuits.** An RC circuit obeys R dq/dt + q/C = V and an RLC circuit is a second-order equation like the spring. The charging curve of a capacitor in a phone charger has the same shape as a cooling curve. Circuit designers use these to select resistor and capacitor values.
6. **Mixing and pollution problems.** If polluted water flows into a lake and clean water flows out, the amount of pollutant satisfies a linear first-order equation. Environmental officers estimate how long the Phewa lake takes to recover. A tank of salt solution in the laboratory is the classic exercise.
7. **Motion with resistance.** A parachutist or a vehicle with air drag obeys m dv/dt = mg − kv, which is separable. The speed rises towards a terminal value mg/k. This is why a hanging-glider pilot reaches a steady speed.
8. **Computer simulation and games.** Weather forecasts, flight simulators and physics engines in games solve differential equations step by step on a computer (Euler's and Runge-Kutta methods). Each step uses the slope field idea of Figure 6.1. The results are the animations we see on a weather map.

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

## Model answers: medium (5 marks) and long (10 marks) questions

**Q (5 marks). Solve the linear equation dy/dx + 2y = x by the integrating-factor method.**

A **first-order linear** equation has the form dy/dx + P(x)y = Q(x). Multiplying by a suitable factor μ(x) turns the left side into the derivative of a product, which can then be integrated.

1. Here P = 2 and Q = x. The **integrating factor** is μ = e^(∫P dx) = e^(2x).
2. Multiply the equation by e^(2x): e^(2x) y′ + 2e^(2x) y = x e^(2x), and the left side is exactly d/dx (e^(2x) y).
3. Integrate both sides: e^(2x) y = ∫ x e^(2x) dx.
4. By parts (u = x, dv = e^(2x) dx) this is x e^(2x)/2 − e^(2x)/4 + C.
5. Divide by e^(2x): **y = x/2 − 1/4 + C e^(−2x)**.

*Check:* y′ = 1/2 − 2Ce^(−2x), so y′ + 2y = 1/2 − 2Ce^(−2x) + x − 1/2 + 2Ce^(−2x) = x ✓. The term Ce^(−2x) dies away, so every solution approaches the line y = x/2 − 1/4 for large x.

**Q (5 marks). A cup of tea at 80 °C is placed in a room at 25 °C and cools to 60 °C in 10 minutes. Use Newton's law of cooling to find when it reaches 40 °C.**

**Newton's law:** the rate of cooling is proportional to the difference between the body and its surroundings, dT/dt = −k(T − 25), with k > 0 (Figure 6.4a). It is separable.

1. Separate and integrate: dT/(T − 25) = −k dt, so ln(T − 25) = −kt + c, that is T = 25 + Ae^(−kt).
2. At t = 0, T = 80: A = 55, so T = 25 + 55e^(−kt).
3. At t = 10, T = 60: 35 = 55e^(−10k), so e^(−10k) = 7/11 and k = (1/10) ln(11/7) = **0.0452 per minute**.
4. For T = 40: 15 = 55e^(−kt), so t = (1/k) ln(55/15) = ln(3.667)/0.0452 = 1.2993/0.0452 ≈ **28.7 minutes**.

*Check:* at t = 30 the formula gives 25 + 55e^(−1.356) = 39.2 °C, consistent with 40 °C near 28.7 min. The tea never goes below 25 °C, the room temperature.

**Q (10 marks). Define order, degree and the general and particular solutions of a differential equation. Describe the methods for solving first-order equations with one example each, and solve a second-order equation with constant coefficients including an initial-value problem.**

**Introduction.** A **differential equation (DE)** is an equation involving an unknown function and its derivatives. The **order** is that of the highest derivative and the **degree** is its power. The **general solution** has as many arbitrary constants as the order; a **particular solution** fixes them by initial conditions (Figure 6.1). Many laws of physics, biology and finance are DEs (Plate 6.1).

**First-order methods (Figure 6.2).**

| Type | Form | Example | Solution |
|---|---|---|---|
| Separable | dy/dx = f(x)g(y) | dy/dx = xy | y = Ce^(x²/2) |
| Homogeneous | dy/dx = F(y/x) | dy/dx = (x + y)/x, put y = vx | y = x(ln\|x\| + C) |
| Linear | y′ + Py = Q | y′ + 2y = x | y = x/2 − 1/4 + Ce^(−2x) |
| Exact | M dx + N dy = 0, M_y = N_x | (2xy + 1)dx + (x² + y)dy = 0 | x²y + x + y²/2 = C |

For the exact example M = 2xy + 1 and N = x² + y; since ∂M/∂y = 2x = ∂N/∂x it is exact. Find F with F_x = M: F = x²y + x + g(y); then F_y = x² + g′(y) = x² + y gives g = y²/2.

**Second-order equation with constant coefficients.** For ay″ + by′ + cy = 0 try y = e^(mx), giving the auxiliary equation am² + bm + c = 0. The roots decide the solution: real and distinct gives C₁e^(m₁x) + C₂e^(m₂x); repeated gives (C₁ + C₂x)e^(mx); complex α ± iβ gives e^(αx)(C₁ cos βx + C₂ sin βx) (Figure 6.3).

*Example (IVP).* y″ + 4y′ + 3y = 0, y(0) = 2, y′(0) = 0. The auxiliary equation m² + 4m + 3 = 0 gives m = −1, −3, so y = C₁e^(−x) + C₂e^(−3x). From y(0) = 2: C₁ + C₂ = 2. From y′(0) = 0: −C₁ − 3C₂ = 0. Hence C₂ = −1 and C₁ = 3, so **y = 3e^(−x) − e^(−3x)**. *Check:* y(0) = 3 − 1 = 2 ✓ and y′(0) = −3 + 3 = 0 ✓.

**Modelling.** Cooling, growth and spring motion lead to dT/dt = −k(T − Tₛ), dP/dt = rP(1 − P/K) and my″ + ky = 0 respectively (Figure 6.4).

**Conclusion.** Identify the type first (Figure 6.2), then apply its method, then check by substituting back. This routine solves nearly every examination problem in the unit.
