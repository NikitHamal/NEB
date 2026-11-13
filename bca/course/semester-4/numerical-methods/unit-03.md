---
subject: Numerical Methods
grade: BCA Semester 4
unit: 3
title: Numerical Differentiation and Integration
hours: 5
area: BCA 253 · Numerical Methods · Unit 3
---

A speedometer log gives positions every few seconds: what is the speed? A sensor gives readings: what is the total? Differentiation and integration of *tabulated* data, or of functions with no elementary antiderivative such as $e^{- x^{2}}$ and $\frac{1}{\ln x}$, must be done numerically. The formulas here come from differentiating or integrating the interpolating polynomials of Unit 2.

::: key What this unit gives you
- Finite-difference formulas for derivatives and their errors; Newton's differentiation formulas.
- Newton–Cotes integration: trapezoidal, Simpson's $\frac{1}{3}$ and $\frac{3}{8}$ rules, composite versions and error behaviour.
- Romberg integration and numerical double integration.
:::

## 3.1 Numerical differentiation

From $f (x + h) = f (x) + h f' (x) + \left( \frac{h^{2}}{2} \right) f'' (x) + \ldots$ we get three basic formulas:

| Formula | Expression | Error order |
|---|---|---|
| Forward difference | $f' (x) \approx \frac{f (x + h) - f (x)}{h}$ | $O (h)$ |
| Backward difference | $f' (x) \approx \frac{f (x) - f (x - h)}{h}$ | $O (h)$ |
| **Central difference** | $f' (x) \approx \frac{f (x + h) - f (x - h)}{2 h}$ | **$O (h^{2})$** |
| Central, second derivative | $f'' (x) \approx \frac{f (x + h) - 2 f (x) + f (x - h)}{h^{2}}$ | $O (h^{2})$ |

The central formula is better because the first error term cancels. Halving *h* should cut the forward error by 2 and the central error by 4.

::: example f(x) = eˣ at x = 1 (true f′ = e = 2.718282)
| *h* | forward $\frac{f (x + h) - f (x)}{h}$ | error | central $\frac{f (x + h) - f (x - h)}{2 h}$ | error |

|---|---|---|---|---|

| 0.1 | 2.858842 | 0.140560 | 2.722815 | 0.0045327 |

| 0.01 | 2.731919 | 0.013637 | 2.718327 | 0.0000453 |

| 0.001 | 2.719641 | 0.001360 | 2.718282 | 0.0000005 |

Each tenfold reduction of *h* reduces the forward error about tenfold and the central error about a hundredfold, exactly as the orders say. (The backward formula with $h = 0.1$ gives 2.586787, an error of the opposite sign to the forward one.) If *h* is made too small, round-off error (subtracting nearly equal numbers) eventually dominates: there is an optimal *h* (roughly $10^{-8}$ for the forward formula and $10^{-5}$ for the central formula in double precision), below which the total error grows again.
:::

### Newton's differentiation formulas (tabulated, equally spaced data)

Differentiating Newton's forward formula (Unit 2) with respect to *x* at $x = x_{0} (u = 0)$ gives

$$f' (x_{0}) = \left( \frac{1}{h} \right) \left[ \Delta y_{0} - \frac{\Delta^{2} y_{0}}{2} + \frac{\Delta^{3} y_{0}}{3} - \frac{\Delta^{4} y_{0}}{4} + \ldots \right]$$

$$f'' (x_{0}) = \left( \frac{1}{h^{2}} \right) \left[ \Delta^{2} y_{0} - \Delta^{3} y_{0} + \left( \frac{11}{12} \right) \Delta^{4} y_{0} - \ldots \right]$$

(At the end of a table use the backward versions with *∇* and plus signs.)

::: example Derivatives of ln x at x = 1.0 from a table (true f′(1) = 1, f″(1) = −1)
| *x* | $y = \ln x$ | $\Delta y$ | $\Delta^{2} y$ | $\Delta^{3} y$ | $\Delta^{4} y$ |

|---|---|---|---|---|---|

| 1.0 | 0.000000 | 0.095310 | -0.008299 | 0.001330 | -0.000296 |

| 1.1 | 0.095310 | 0.087011 | -0.006969 | 0.001034 |  |

| 1.2 | 0.182322 | 0.080043 | -0.005935 |  |  |

| 1.3 | 0.262364 | 0.074108 |  |  |  |

| 1.4 | 0.336472 |  |  |  |  |

With $h = 0.1$, using more terms improves the answer: one term gives 0.953102, two terms 0.994596, three 0.999030, and four terms **$f' (1.0) \approx 0.999770$** (error 0.000230). The second derivative from the formula is **$f'' (1.0) \approx - 0.990045$** (true −1; the error is larger because a second derivative loses accuracy).

For an interior point use central formulas instead. At $x = 1.2$: $f' \approx \frac{\ln 1.3 - \ln 1.1}{0.2} = 0.835270$ (true $1 / 1.2 = 0.833333$) and $f'' \approx \frac{\ln 1.1 - 2 \ln 1.2 + \ln 1.3}{0.01} = - 0.696867$ (true $- 1 / 1.2^{2} = - 0.694444$).
:::

**Maxima and minima of a tabulated function.** Differentiate Newton's formula, set $\frac{d y}{d u} = 0$, solve for *u* (usually a quadratic) and convert to $x = x_{0} + h u$; use the second derivative to classify.

## 3.2 Numerical integration: Newton–Cotes rules

To compute $I = \int_{a}^{b} f (x) \,d x$, divide $[a ,\  b]$ into *n* equal strips of width $h = \frac{b - a}{n} ,\  x_{i} = a$ + ih, $y_{i} = f (x_{i})$, replace *f* on groups of strips by an interpolating polynomial, and integrate that exactly.

| Rule | Polynomial | Formula (composite) | *n* must be | Error |
|---|---|---|---|---|
| **Trapezoidal** | line (1 strip) | $\left( \frac{h}{2} \right) [y_{0} + 2 (y_{1} + \ldots + y_{n-1}) + y_{n}]$ | any | $- \frac{(b - a) h^{2} f'' (\xi)}{12} ,\  O (h^{2})$ |
| **Simpson's $\frac{1}{3}$** | parabola (2 strips) | $\left( \frac{h}{3} \right) [y_{0} + 4 (y_{1} + y_{3} + \ldots) + 2 (y_{2} + y_{4} + \ldots) + y_{n}]$ | **even** | $- \frac{(b - a) h^{4} f'''' (\xi)}{180} ,\  O (h^{4})$ |
| **Simpson's $\frac{3}{8}$** | cubic (3 strips) | $\left( \frac{3 h}{8} \right) [y_{0} + 3 (y_{1} + y_{2} + y_{4} + y_{5} + \ldots) + 2 (y_{3} + y_{6} + \ldots) + y_{n}]$ | **multiple of 3** | $- \frac{(b - a) h^{4} f'''' (\xi)}{80} ,\  O (h^{4})$ |

Simpson's $\frac{1}{3}$ rule is exact for polynomials up to degree **3** (not just 2) because the odd error term vanishes; the $\frac{3}{8}$ rule is also exact to degree 3. The trapezoidal rule is exact only for lines.

::: example I = ∫₀¹ dx/(1 + x²) = π/4 = 0.785398, with n = 6 (h = 1/6)
Function values:

| *i* | $x_{i}$ | $f (x_{i}) = \frac{1}{(1 + x_{i}^{2})}$ |

|---|---|---|

| 0 | $\frac{0}{6}$ | 1.000000 |

| 1 | $\frac{1}{6}$ | 0.972973 |

| 2 | $\frac{2}{6}$ | 0.900000 |

| 3 | $\frac{3}{6}$ | 0.800000 |

| 4 | $\frac{4}{6}$ | 0.692308 |

| 5 | $\frac{5}{6}$ | 0.590164 |

| 6 | $\frac{6}{6}$ | 0.500000 |

**Trapezoidal.** $\frac{h}{2} \times [y_{0} + y_{6} + 2 (y_{1} + \ldots + y_{5})] = \left( \frac{1}{6} \right) \left[ \frac{1.000000 + 0.500000}{2} + \sum y_{1} \ldots y_{5} \right]$: the bracketed sum is 4.705445, so I ≈ **0.784241**, error 0.001157.

**Simpson's $\frac{1}{3}$.** $\left( \frac{h}{3} \right) [y_{0} + y_{6} + 4 (y_{1} + y_{3} + y_{5}) + 2 (y_{2} + y_{4})] = \left( \frac{1}{18} \right) [1.500000 + 4 (2.363137) + 2 (1.592308)] = \left( \frac{1}{18} \right) (14.137163)$ = **0.785398**, error 0.0000002.

**Simpson's $\frac{3}{8}$.** $\left( \frac{3 h}{8} \right) [y_{0} + y_{6} + 3 (y_{1} + y_{2} + y_{4} + y_{5}) + 2 y_{3}]$ gives **0.785396**, error 0.0000023.

Simpson's rules are about a thousand times more accurate than the trapezoidal rule with the same data. (All three results were checked against SciPy's `quad`.)
:::

### Convergence as n grows

| *n* | trapezoid | error | Simpson $\frac{1}{3}$ | error |
|---|---|---|---|---|
| 2 | 0.775000 | 1.04e-02 | 0.783333 | 2.06e-03 |
| 4 | 0.782794 | 2.60e-03 | 0.785392 | 6.01e-06 |
| 8 | 0.784747 | 6.51e-04 | 0.785398 | 3.78e-08 |
| 16 | 0.785235 | 1.63e-04 | 0.785398 | 5.91e-10 |

Each doubling of *n* divides the trapezoidal error by about 4 (order $h^{2}$) and the Simpson error by about 16 (order $h^{4}$), as the error terms predict.

**Choosing a rule:** use Simpson's $\frac{1}{3}$ when the number of strips is even, the $\frac{3}{8}$ rule when it is a multiple of 3, or combine them ($\frac{3}{8}$ on three strips plus $\frac{1}{3}$ on the rest) for odd *n*. Use the trapezoidal rule for rough work, noisy data, or periodic functions integrated over a full period.

## 3.3 Romberg integration

**Richardson extrapolation** combines two estimates with step *h* and $\frac{h}{2}$ to cancel the leading error term. Applied repeatedly to trapezoidal values, it gives the **Romberg table**:

$R ( k$, 0) = trapezoidal rule with $2^{k}$ strips; **$R (k ,\  j) = R (k ,\  j - 1) + \frac{R (k ,\  j - 1) - R (k - 1 ,\  j - 1)}{4^{j} - 1}$**.

Column 1 is Simpson's $\frac{1}{3}$ rule, column 2 is Boole's rule, and each further column cancels the next error power $(h^{2} ,\  h^{4} ,\  h^{6} ,\  \ldots)$.

::: example Romberg for ∫₀¹ dx/(1 + x²)
| *h* | $R (k ,\  0)$ trapezoid | $R (k ,\  1)$ | $R (k ,\  2)$ | $R (k ,\  3)$ | $R (k ,\  4)$ |

|---|---|---|---|---|---|

| 1 | 0.75000000 |  |  |  |  |

| $\frac{1}{2}$ | 0.77500000 | 0.78333333 |  |  |  |

| $\frac{1}{4}$ | 0.78279412 | 0.78539216 | 0.78552941 |  |  |

| $\frac{1}{8}$ | 0.78474712 | 0.78539813 | 0.78539852 | 0.78539645 |  |

| $\frac{1}{16}$ | 0.78523540 | 0.78539816 | 0.78539817 | 0.78539816 | 0.78539817 |

The best estimate **$R (4 ,\  4) = 0.78539817$** differs from $\frac{\pi}{4} = 0.78539816$ by only 2.92e-09 (using just 17 function values). Note that the extrapolated values do not improve in every single entry: $R (3 ,\  3) = 0.78539645$ has error 1.72e-06, which is larger than $R (3 ,\  2)$. The table improves *in the limit*; the stopping rule is $\mid R (k ,\  k) - R ( k - 1 ,\  k$ − 1)| < *ε*.
:::

## 3.4 Numerical double integration

For $I = \int_{a}^{b} \int_{c}^{d} f (x ,\  y) \,d y \,d x$, apply a one-dimensional rule in each direction. With a grid $h_{x} \times k_{y}$, the composite rule is a double sum of the weights times function values. For Simpson's $\frac{1}{3}$ with two strips in each direction the weights form the grid

|  | $y_{0}$ | $y_{1}$ | $y_{2}$ |
|---|---|---|---|
| **$x_{0}$** | 1 | 4 | 1 |
| **$x_{1}$** | 4 | 16 | 4 |
| **$x_{2}$** | 1 | 4 | 1 |

and $I \approx \left( \frac{h_{x} k}{9} \right) \sum w_{ij} f (x_{i} ,\  y_{j})$. For the trapezoidal rule the weights are $\frac{1}{4} ,\  \frac{1}{2} ,\  \frac{1}{4}$ products and $I \approx h_{x} k \sum w_{ij} f$.

::: example ∫₀¹∫₁² dy dx/(x + y), with h = k = 0.5
The exact value is $3 \ln 3 - 4 \ln 2 = 0.523248$.

| $f (x ,\  y) = \frac{1}{x + y}$ | $y = 1$ | $y = 1.5$ | $y = 2$ |

|---|---|---|---|

| $x = 0$ | 1.000000 | 0.666667 | 0.500000 |

| $x = 0.5$ | 0.666667 | 0.500000 | 0.400000 |

| $x = 1.0$ | 0.500000 | 0.400000 | 0.333333 |

Simpson (weights 1, 4, 1): $I \approx (0.5 \times 0.5 / 9) \times \sum$ = **0.524074**, error 0.000826. Trapezoidal: **0.537500**, error 0.014252. Even with only nine points Simpson is accurate to 3 decimals. A smaller step or a Romberg refinement in each direction would improve both.
:::

## 3.5 Seeing the ideas: areas under curves, Romberg's table and the error of a derivative

Before computers, engineers measured the area of an irregular shape with a mechanical **planimeter**, a hand-driven integrator. Numerical integration does the same job with arithmetic.

```photogrid label="3.1" cols="2" ratio="1.2" caption="Integration by machine and by rule. (a) A Keuffel and Esser polar planimeter in its case: tracing the boundary of a shape with the pointer gives its area on the dial, a mechanical integrator used by surveyors and engineers. (b) The trapezoidal rule on one quarter-wave of $\sin x$ with step pi/4: straight tops replace the curve, so the area is slightly underestimated for a concave curve."
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

```svgfig label="3.1" caption="Simpson's one-third rule fits a parabola through each pair of strips. On the same four strips for the integral of $\sin x$ from 0 to pi, the trapezoidal rule gives 1.89612 (error 0.10388) while Simpson gives 2.00456 (error -0.00456), more than twenty times better for the same ordinates 0, 0.70711, 1, 0.70711, 0."
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

```svgfig label="3.2" caption="Romberg integration of $e^{x}$ on [0, 1] (exact value 1.718282). The first column is the trapezoidal rule with 1, 2 and 4 strips; each later column is Richardson extrapolation $R (i ,\  j) = R (i ,\  j - 1) + \frac{R (i ,\  j - 1) - R (i - 1 ,\  j - 1)}{4^{j} - 1}$. Three trapezoid values combine into 1.718283, correct to six decimals."
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

```svgfig label="3.3" caption="Error of two derivative formulas for $f (x) = e^{x}$ at $x = 1$ (exact 2.71828). Halving *h* halves the forward-difference error (0.14056 to 0.06910) but quarters the central-difference error (0.00453 to 0.00113), because the forward formula is $O (h)$ and the central formula is $O (h^{2})$."
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

```photogrid label="3.2" cols="2" ratio="1.2" caption="From depth readings to river flow. (a) A river gauging station: staff measure the depth at fixed distances across the channel, integrate the depths to get the cross-section area, and multiply by the mean velocity to get the discharge. (b) An idealised 10-metre channel with a smooth bed has an exact area of 15.279 square metres. Four trapezoids give 14.485 (an error of 5.2 per cent), while Simpson's rule with the same four strips gives 15.314 (error 0.23 per cent), because it fits parabolas instead of straight lines. Ten trapezoids reach 15.153. At an assumed mean velocity of 0.8 metres a second the flow is 12.2 cubic metres a second. The shape is invented for the exercise; real beds are rough, so the more strips surveyed the better."
@ photo id="bcanm/gauging" cap="A river gauging station: depth and flow are integrated"
fit 1.2
focus 0.5 0.5
@ svg cap="Channel cross-section: trapezoid vs Simpson"
import math
L = 10.0
d = lambda x: 2.4 * math.sin(math.pi * x / L)
exact = 2.4 * 2 * L / math.pi
def trap(n):
    h = L / n
    return h * (d(0) / 2 + sum(d(i * h) for i in range(1, n)) + d(L) / 2)
def simp(n):
    h = L / n
    return h / 3 * (d(0) + d(L) + 4 * sum(d(i * h) for i in range(1, n, 2)) + 2 * sum(d(i * h) for i in range(2, n, 2)))
ns = [2, 4, 10]
et = [abs(trap(n) - exact) for n in ns]
es = [abs(simp(n) - exact) for n in ns]
assert et[0] > et[1] > et[2] and es[1] < et[1] / 10
Q = exact * 0.8
facts = dict(ex=round(exact, 3), t4=round(trap(4), 3), s4=round(simp(4), 3), t10=round(trap(10), 3), q=round(Q, 1), e4t=round(100 * et[1] / exact, 1), e4s=round(100 * es[1] / exact, 2))
f = Fig(300, 236)
f.text(150, 12, "10 m wide channel, depth 2.4 sin(pi x / 10)", size=10.5, color=NAVY, bold=True)
x0, y0, W = 20, 36, 260
X = lambda x: x0 + x / L * W
Y = lambda v: y0 + v * 30
pts = [(X(i * L / 4), Y(d(i * L / 4))) for i in range(5)]
f.poly([(X(0), y0)] + pts + [(X(L), y0)], fill="#dbeafe", stroke=BLUE, sw=1)
for i in range(1, 100):
    a, b = (i - 1) * L / 99, i * L / 99
    f.line(X(a), Y(d(a)), X(b), Y(d(b)), color=NAVY, sw=2)
f.line(x0, y0, x0 + W, y0, color=SLATE)
f.text(150, 28 + 0, "water surface", size=10.5, color=SLATE)
f.text(150, 124, "blue = 4 trapezoids, line = true bed", size=10.5, color=SLATE)
hdr = ["strips", "trapezoid", "Simpson"]
for j, t in enumerate(hdr):
    f.text(60 + j * 90, 146, t, size=10.5, color=NAVY, bold=True)
for i, n in enumerate(ns):
    y = 164 + i * 20
    f.text(60, y, str(n), size=10.5, color=NAVY, bold=True)
    f.text(150, y, "%.3f" % trap(n), size=10.5, color=RED)
    f.text(240, y, "%.3f" % simp(n), size=10.5, color=TEAL, bold=True)
f.text(150, 228, "exact area %.3f m2, flow at 0.8 m/s = %.1f m3/s" % (exact, Q), size=10.5, color=NAVY, bold=True)
```

## 3.6 Choosing the step: truncation error against round-off, and Richardson extrapolation

A difference formula has **truncation error** that shrinks as $h \to 0$ (forward difference $O(h)$, central difference $O(h^{2})$), but the subtraction $f(x+h) - f(x)$ loses digits to cancellation (Section 1.12) and the division by a tiny $h$ magnifies what remains. The two effects pull in opposite directions, so there is a best $h$, and going below it makes the answer *worse*.

::: example d/dx of eˣ at x = 1 in double precision (true value e = 2.718281828459)
| $h$ | forward-difference error | central-difference error |
|---|---|---|
| $10^{-1}$ | $1.4\times 10^{-1}$ | $4.5\times 10^{-3}$ |
| $10^{-2}$ | $1.4\times 10^{-2}$ | $4.5\times 10^{-5}$ |
| $10^{-4}$ | $1.4\times 10^{-4}$ | $4.5\times 10^{-9}$ |
| $10^{-6}$ | $1.4\times 10^{-6}$ | $1.6\times 10^{-10}$ |
| $10^{-8}$ | $6.6\times 10^{-9}$ | $6.6\times 10^{-9}$ |
| $10^{-10}$ | $1.5\times 10^{-6}$ | $6.7\times 10^{-7}$ |
| $10^{-12}$ | $4.3\times 10^{-4}$ | $2.1\times 10^{-4}$ |
| $10^{-14}$ | $9.3\times 10^{-3}$ | $9.3\times 10^{-3}$ |
| $10^{-16}$ | 2.72 (answer 0) | 2.72 (answer 0) |

The forward error falls like $h$ down to $h \approx 10^{-8}$ and then rises like $\varepsilon/h$; the central error falls like $h^{2}$ and bottoms out near $10^{-10}$ to $10^{-11}$ (at $h = 10^{-5}$ it is $5.9\times 10^{-11}$), then rises. At $h = 10^{-16}$ the points $1 + h$ and $1$ are the same number, the numerator is exactly zero and the derivative is "0".
:::

Balancing a truncation error $Ch^{p}$ against a round-off error $\varepsilon/h$ gives the optimum $h \approx \varepsilon^{1/(p+1)}$: about $10^{-8}$ for the forward formula and $6\times 10^{-6}$ for the central formula. In single precision these become about $3\times 10^{-4}$ and $5\times 10^{-3}$.

```svgfig label="3.4" caption="Error of two derivative formulas for $e^{x}$ at $x = 1$ against the step $h$ (both axes logarithmic, double precision). Each curve falls with the slope of its truncation error (1 for forward, 2 for central) and then turns up where round-off dominates. Values from the table above."
import math
f = Fig(560, 250)
ax = Axes(f, 56, 14, 520, 190, (-16.5, -0.5), (-12, 1))
ax.grid(2, 2)
ax.axes("", "")
H = [-1, -2, -4, -6, -8, -10, -12, -14, -16]
fw = [1.41e-1, 1.36e-2, 1.36e-4, 1.36e-6, 6.6e-9, 1.55e-6, 4.32e-4, 9.34e-3, 2.72]
ce = [4.53e-3, 4.53e-5, 4.53e-9, 1.63e-10, 6.6e-9, 6.73e-7, 2.1e-4, 9.34e-3, 2.72]
for vals, col in ((fw, RED), (ce, NAVY)):
    P = [(h, math.log10(v)) for h, v in zip(H, vals)]
    for (x1, y1), (x2, y2) in zip(P, P[1:]):
        f.line(ax.X(x1), ax.Y(y1), ax.X(x2), ax.Y(y2), color=col, sw=2.4)
    for x, y in P:
        f.circle(ax.X(x), ax.Y(y), 3.4, fill=col, stroke=col)
f.text(150, 60, "forward: slope 1", size=10.5, color=RED, bold=True)
f.text(120, 176, "central: slope 2", size=10.5, color=NAVY, bold=True)
f.text(300, 226, "log10 of the step h", size=10.5, color=SLATE)
f.text(300, 244, "log10 of the error", size=10, color=SLATE)
```

**Richardson extrapolation.** If a formula $D(h)$ has error $c_2h^{2} + c_4h^{4} + \cdots$, then the combination
$$D^{(1)}(h) = \frac{4\,D(h/2) - D(h)}{3}$$
cancels the $h^{2}$ term, leaving $O(h^{4})$. A second round, $D^{(2)} = \dfrac{16\,D^{(1)}(h/2) - D^{(1)}(h)}{15}$, leaves $O(h^{6})$. This is the same idea as Romberg integration (Section 3.3) applied to differentiation.

::: example Derivative of cos x at x = 1 (true value −sin 1 = −0.8414709848)
The central difference $D(h) = \dfrac{\cos(1+h) - \cos(1-h)}{2h}$ gives $D(0.4) = -0.819211$, $D(0.2) = -0.835872$ and $D(0.1) = -0.840069$ (errors 0.0223, 0.0056, 0.0015). One extrapolation: $D^{(1)}(0.4) = -0.841426$ and $D^{(1)}(0.2) = -0.841468$ (errors $4.5\times 10^{-5}$ and $2.8\times 10^{-6}$, a factor 16 each time). The second: $D^{(2)} = \dfrac{16(-0.841468183) - (-0.841426320)}{15} = -0.84147097$, error $1.1\times 10^{-8}$. Three cheap central differences, no tiny $h$, and eight correct digits.
:::

**The five-point formula.** Using $f(x \pm h)$ and $f(x \pm 2h)$ with weights chosen to cancel the $h^{2}$ error:
$$f'(x) \approx \frac{f(x-2h) - 8f(x-h) + 8f(x+h) - f(x+2h)}{12h}, \qquad \text{error } = O(h^{4}).$$
For $\cos$ at $x = 1$, $h = 0.1$ it gives $-0.841468$ (error $2.8\times 10^{-6}$), exactly the first Richardson value above (the two are the same formula). The three-point second-derivative formula $f''(x) \approx \dfrac{f(x+h) - 2f(x) + f(x-h)}{h^{2}}$ gives $-0.539852$ for $\cos$ at $1$ with $h = 0.1$, against $-0.540302$ (error $4.5\times 10^{-4}$, $O(h^{2})$).

## 3.7 Error bounds and the number of strips needed

The composite rules have known error terms. For $n$ strips of width $h = (b-a)/n$:

$$E_{\text{trap}} = -\frac{(b-a)\,h^{2}}{12}\,f''(\xi), \qquad E_{\text{Simpson}} = -\frac{(b-a)\,h^{4}}{180}\,f^{(4)}(\xi).$$

Bound the derivative by its maximum $M$ on $[a, b]$ and solve for $h$ to get the number of strips guaranteeing a tolerance, **before** computing anything.

::: example Strips to compute the integral of eˣ on [0, 1] to within 10⁻⁶
Here $M = e = 2.718$ for every derivative. Trapezoidal: $\dfrac{e\,h^{2}}{12} \le 10^{-6}$ gives $h \le 0.00210$, so $n \ge 476$ strips. Simpson: $\dfrac{e\,h^{4}}{180} \le 10^{-6}$ gives $h \le 0.0902$, so $n \ge 11.1$, and Simpson needs an even number: **$n = 12$**. The actual errors with these $n$ are $6.3\times 10^{-7}$ (trapezoid, $n = 476$) and $4.6\times 10^{-7}$ (Simpson, $n = 12$): the bounds are honest. Simpson needs forty times fewer function values for the same accuracy.
:::

**Order checks from the table.** Doubling $n$ should cut the trapezoidal error by 4 and the Simpson error by 16. For $e^{x}$ on $[0,1]$:

| $n$ | trapezoid error | ratio | Simpson error | ratio |
|---|---|---|---|---|
| 2 | $3.56\times 10^{-2}$ | | $5.79\times 10^{-4}$ | |
| 4 | $8.94\times 10^{-3}$ | 3.99 | $3.70\times 10^{-5}$ | 15.7 |
| 8 | $2.24\times 10^{-3}$ | 4.00 | $2.33\times 10^{-6}$ | 15.9 |
| 16 | $5.59\times 10^{-4}$ | 4.00 | $1.46\times 10^{-7}$ | 16.0 |

This ratio test is also a practical way to estimate the error of an answer when no derivative bound is available: if $I_n$ and $I_{2n}$ are two Simpson results, the error of $I_{2n}$ is about $(I_{2n} - I_n)/15$.

**More rules.** The *midpoint rule* $M_n = h\sum f(\text{midpoints})$ has error $+\dfrac{(b-a)h^{2}}{24}f''$, half the trapezoid's and of opposite sign: for $e^{x}$ with $n = 4$ it gives 1.713815 (error $-4.5\times 10^{-3}$) against the trapezoid's 1.727222 (error $+8.9\times 10^{-3}$). **Boole's rule**, the next closed Newton-Cotes rule, uses five points:
$$\int_{x_0}^{x_4} f\,dx \approx \frac{2h}{45}\left[7f_0 + 32f_1 + 12f_2 + 32f_3 + 7f_4\right], \qquad \text{error } O(h^{7}) \text{ per application.}$$
For $e^{x}$ with $h = 0.25$ it gives 1.7182827 (error $8.6\times 10^{-7}$) from the same five points where Simpson's rule gives an error of $3.7\times 10^{-5}$. Boole's rule is exactly the third column of the Romberg table.

## 3.8 Gauss–Legendre quadrature

Newton–Cotes rules fix the node positions (equally spaced) and choose the weights; a rule with $n$ points is exact for polynomials of degree $n - 1$ (or $n$ for odd $n$). **Gaussian quadrature** chooses the nodes *and* the weights, using $2n$ free numbers to be exact for every polynomial up to degree $2n - 1$. On $[-1, 1]$:

$$\int_{-1}^{1} f(x)\,dx \approx \sum_{i=1}^{n} w_i\,f(x_i),\qquad x_i = \text{zeros of the Legendre polynomial } P_n .$$

| $n$ | nodes $x_i$ | weights $w_i$ | exact up to degree |
|---|---|---|---|
| 1 | 0 | 2 | 1 |
| 2 | $\pm 0.577350$ ($\pm 1/\sqrt{3}$) | 1, 1 | 3 |
| 3 | $0,\ \pm 0.774597$ ($\pm\sqrt{3/5}$) | 0.888889 ($8/9$), 0.555556 ($5/9$) | 5 |
| 4 | $\pm 0.339981,\ \pm 0.861136$ | 0.652145, 0.347855 | 7 |

For a general interval $[a, b]$ substitute $x = \frac{b-a}{2}t + \frac{a+b}{2}$, so that $\int_a^b f\,dx = \dfrac{b-a}{2}\int_{-1}^{1} f(x(t))\,dt$.

::: example Two-point Gauss rule is exact for cubics: ∫ from −1 to 1 of (x³ + x² + 1) dx
Exact value: $0 + \frac{2}{3} + 2 = \frac{8}{3}$. Two-point rule: $f(-0.57735) + f(0.57735) = (-0.19245 + 0.33333 + 1) + (0.19245 + 0.33333 + 1) = 2.66667$. Exact with only two function values; Simpson needs three.
:::

::: example ∫ eˣ dx on [0, 1] (true value e − 1 = 1.718281828) by Gauss–Legendre
With $t_i$ mapped to $x_i = (t_i + 1)/2$: two points give 1.717896 (error $3.9\times 10^{-4}$), three points give 1.7182810 (error $8.2\times 10^{-7}$) and four points give 1.7182818275 (error $9.3\times 10^{-10}$). For $\int_0^{\pi}\sin x\,dx = 2$: two points give 1.935820, three points 2.001389, four points 1.999984. For $\int_0^1 \frac{dx}{1+x^{2}} = \frac{\pi}{4}$ two points give 0.786885 and three points 0.785267 (true 0.785398).
:::

```svgfig label="3.5" caption="Accuracy against the number of function evaluations for the integral of $e^{x}$ on [0, 1] (log scale). The trapezoidal rule (red) gains a factor of 4 for each doubling, Simpson's rule (amber) a factor of 16, and Gauss-Legendre (navy), which also chooses its nodes, gains about two to three digits for every added point."
import math
f = Fig(560, 250)
ax = Axes(f, 56, 14, 520, 190, (0, 34), (-13, 0))
ax.grid(5, 2)
ax.axes("", "")
series = [
    (RED, [(2, 1.409e-1), (3, 3.565e-2), (5, 8.94e-3), (9, 2.237e-3), (17, 5.593e-4), (33, 1.398e-4)]),
    (AMBER, [(3, 5.793e-4), (5, 3.701e-5), (9, 2.326e-6), (17, 1.456e-7), (33, 9.103e-9)]),
    (NAVY, [(1, 6.956e-2), (2, 3.855e-4), (3, 8.241e-7), (4, 9.33e-10), (5, 6.537e-13)]),
]
for col, pts in series:
    P = [(n, math.log10(e)) for n, e in pts]
    for (x1, y1), (x2, y2) in zip(P, P[1:]):
        f.line(ax.X(x1), ax.Y(y1), ax.X(x2), ax.Y(y2), color=col, sw=2.4)
    for x, y in P:
        f.circle(ax.X(x), ax.Y(y), 3.4, fill=col, stroke=col)
f.text(440, 62, "trapezoid", size=10.5, color=RED, bold=True)
f.text(440, 128, "Simpson", size=10.5, color=AMBER, bold=True)
f.text(150, 150, "Gauss-Legendre", size=10.5, color=NAVY, bold=True)
f.text(300, 226, "number of function evaluations", size=10.5, color=SLATE)
f.text(300, 244, "log10 of the error", size=10, color=SLATE)
```

## 3.9 Adaptive Simpson and improper integrals

**Adaptive quadrature.** A uniform grid spends as many points on the smooth parts of an integrand as on the hard parts. *Adaptive Simpson* compares one Simpson estimate $S_{[a,b]}$ on an interval with the sum $S_{[a,m]} + S_{[m,b]}$ of the two half-intervals. If $|S_{[a,m]} + S_{[m,b]} - S_{[a,b]}| \le 15\,\varepsilon$ the interval is accepted (with the Richardson correction $+\frac{1}{15}$ of the difference) and otherwise each half is treated recursively with tolerance $\varepsilon/2$. Subdivision therefore concentrates where the integrand changes fast.

::: example A sharp peak: ∫ from 0 to 1 of dx/(0.01 + (x − 0.3)²) = 26.7794504459
The integrand has a peak of height 100 at $x = 0.3$ and width about 0.1. Adaptive Simpson with $\varepsilon = 10^{-8}$ returns 26.7794504459 (error $1.8\times 10^{-12}$) using **934** function evaluations. Fixed-step Simpson gives errors $1.0$ ($n = 10$), $3.9\times 10^{-2}$ ($n = 20$), $2.0\times 10^{-6}$ ($n = 50$), $2.0\times 10^{-8}$ ($n = 200$), $1.3\times 10^{-9}$ ($n = 400$) and needs about 2,100 strips to reach the same $10^{-12}$ accuracy: more than twice the work, because it refines the flat parts too.
:::

**Integrals with a singularity or an infinite range.** Newton-Cotes and Gauss rules assume a smooth integrand on a finite interval. For $\int_0^1 x^{-1/2}\,dx = 2$ the integrand is infinite at 0; the midpoint rule (which never evaluates there) crawls: 1.9395 with $n = 100$ and 1.99395 with $n = 10000$, an error that falls only like $1/\sqrt{n}$. The cure is a **change of variable** that removes the singularity: with $x = t^{2}$, $dx = 2t\,dt$ the integral becomes $\int_0^1 2\,dt = 2$, which any rule integrates exactly. For an infinite range such as $\int_0^{\infty} e^{-x^{2}}dx = \frac{\sqrt{\pi}}{2} = 0.886227$, put $x = \dfrac{t}{1-t}$, $dx = \dfrac{dt}{(1-t)^{2}}$, giving $\int_0^1 \dfrac{e^{-t^{2}/(1-t)^{2}}}{(1-t)^{2}}\,dt$; Simpson's rule with 40 strips gives 0.88622691 (error $1.6\times 10^{-8}$). The alternatives are to truncate at a large $b$ (when the tail is negligible) or to use Gauss-Laguerre or Gauss-Hermite rules built for such integrals.

## 3.10 Monte Carlo integration

For integrals in many dimensions, grids become impossible (ten strips per axis in 10 dimensions is $10^{10}$ points). **Monte Carlo integration** estimates $\int_a^b f\,dx \approx (b-a)\,\overline{f}$, where $\overline{f}$ is the average of $f$ at $N$ random points in $[a, b]$. The error is statistical: about $\sigma/\sqrt{N}$, where $\sigma$ is the standard deviation of $f$ on the interval, **independent of the dimension**. To gain one more decimal digit you need 100 times more points.

::: example ∫ eˣ dx on [0, 1] with N random points (true value 1.718282; seeded generator)
| $N$ | estimate | error | standard error $\sigma/\sqrt{N}$ |
|---|---|---|---|
| 100 | 1.59130 | −0.1270 | 0.0452 |
| 10 000 | 1.72099 | +0.0027 | 0.0049 |
| 1 000 000 | 1.71787 | −0.00041 | 0.00049 |

For this one-dimensional integral Simpson's rule with 33 points is better than a million random ones by five orders of magnitude, so Monte Carlo is the **wrong** tool in one dimension and the right one in ten.
:::

## Formula and fact sheet

- Forward/backward: $O (h)$; central: $\frac{f (x + h) - f (x - h)}{2 h} ,\  O (h^{2}) ;\  f'' \approx \frac{f (x + h) - 2 f (x) + f (x - h)}{h^{2}}$.
- Trapezoidal: $\left( \frac{h}{2} \right) \left[ y_{0} + 2 \sum y_{i} + y_{n} \right]$. Simpson $\frac{1}{3} ( n$ even): $\left( \frac{h}{3} \right) \left[ y_{0} + 4 \sum \mathrm{odd} + 2 \sum \mathrm{even} + y_{n} \right]$. Simpson $\frac{3}{8} ( n$ multiple of 3): $\left( \frac{3 h}{8} \right) [\ldots]$.
- Error orders: trapezoid $h^{2}$, Simpson $h^{4}$.
- Romberg: $R (k ,\  j) = R (k ,\  j - 1) + \frac{R (k ,\  j - 1) - R (k - 1 ,\  j - 1)}{4^{j} - 1}$.
- Double integral: weighted sum with product weights.
- Best step: forward difference $h \approx \varepsilon^{1/2}$, central $h \approx \varepsilon^{1/3}$; Richardson: $D^{(1)} = \dfrac{4D(h/2) - D(h)}{3}$, $D^{(2)} = \dfrac{16D^{(1)}(h/2) - D^{(1)}(h)}{15}$.
- Five-point: $f' \approx \dfrac{f_{-2} - 8f_{-1} + 8f_{1} - f_{2}}{12h}$; second derivative $\dfrac{f_{1} - 2f_0 + f_{-1}}{h^{2}}$.
- Errors: trapezoid $\dfrac{(b-a)h^2}{12}M_2$, midpoint $\dfrac{(b-a)h^2}{24}M_2$, Simpson $\dfrac{(b-a)h^4}{180}M_4$; Boole $\dfrac{2h}{45}[7, 32, 12, 32, 7]$.
- Gauss–Legendre $n$ points: exact to degree $2n-1$; 2-point nodes $\pm 1/\sqrt{3}$, weights 1; 3-point nodes $0, \pm\sqrt{3/5}$, weights $8/9, 5/9$; map $[a,b]$ by $x = \frac{b-a}{2}t + \frac{a+b}{2}$.
- Monte Carlo error $\approx \sigma/\sqrt{N}$, independent of dimension.

## Chapter summary

- Derivatives come from differentiating interpolation polynomials; central differences are second-order and best; too small an *h* lets round-off dominate.
- Newton–Cotes rules integrate interpolating polynomials; Simpson's rules beat the trapezoidal rule at the same cost.
- Romberg extrapolation turns cheap trapezoidal values into a high-order estimate.
- Double integrals reuse the one-dimensional rules with product weights.
- Step choice in differentiation balances truncation against round-off; Richardson extrapolation and five-point formulas give high accuracy without a tiny $h$. Error formulas tell how many strips are needed, Gauss-Legendre rules reach degree $2n - 1$ with $n$ nodes, adaptive Simpson focuses effort on hard regions, substitutions remove singularities and infinite ranges, and Monte Carlo is the tool for high dimensions.

## Practice

1. Derive the forward-difference formula for $f' (x)$ from Taylor's series and state its order.
2. For $f (x) = e^{x}$ at $x = 1$ with $h = 0.1$, compute forward and central estimates and their errors.
3. Estimate $f' (1.0)$ and $f'' (1.0)$ for $\ln x$ from the difference table, using Newton's forward formulas.
4. Evaluate $\frac{\int_{0}^{1} d x}{(1 + x^{2})}$ with $n = 6$ by the trapezoidal, Simpson $\frac{1}{3}$ and Simpson $\frac{3}{8}$ rules.
5. Why must *n* be even for Simpson's $\frac{1}{3}$ rule and a multiple of 3 for the $\frac{3}{8}$ rule?
6. How many times smaller is the error expected after halving *h* for the trapezoidal rule and for Simpson's rule?
7. Build a Romberg table with four trapezoidal estimates and extrapolate.
8. Estimate $\frac{\int_{0}^{1} \int_{1}^{2} d y d x}{x + y}$ with Simpson's rule, $h = k = 0.5$, and compare it with the exact value.
9. State two reasons why a very small *h* does not give a better numerical derivative.
10. Explain why the forward-difference error for $e^{x}$ at $x = 1$ stops falling at about $h = 10^{-8}$ and then rises.
11. Given the central differences $D(0.4) = -0.819211$ and $D(0.2) = -0.835872$ for $\cos x$ at $x = 1$, compute the Richardson value $D^{(1)}(0.4)$ and its error ($-\sin 1 = -0.841471$).
12. Use the five-point formula with $h = 0.1$ to estimate $f'(1)$ for $f(x) = \ln x$.
13. How many strips guarantee that the trapezoidal rule gives $\int_1^2 \dfrac{dx}{x}$ with error below $10^{-4}$? How many for Simpson's rule?
14. Apply the midpoint rule with $n = 4$ and the trapezoidal rule with $n = 4$ to $\int_0^1 x^{2}\,dx$. Compare their errors.
15. Apply Boole's rule with $h = 0.25$ to $\int_0^1 x^{4}\,dx$. Why is the answer exact?
16. Evaluate $\int_{0}^{2}(x^{3} + 1)\,dx$ by the two-point Gauss–Legendre rule and verify that it is exact.
17. Evaluate $\int_{1}^{3}\dfrac{dx}{x}$ by the three-point Gauss–Legendre rule. Compare with $\ln 3$.
18. Substitute $x = t^{2}$ in $\int_{0}^{1}\dfrac{dx}{\sqrt{x}(1+x)}$ and evaluate by Simpson's rule with $n = 4$. The exact value is $\pi/2$.
19. How does the error of a Monte Carlo estimate change when $N$ is multiplied by 100? Why is the method used in 10 dimensions but not in 1?

::: note Answers and worked solutions
**1.** $f (x + h) = f (x) + h f' (x) + \left( \frac{h^{2}}{2} \right) f'' (\xi)$. Rearranging, $f' (x) = \frac{f (x + h) - f (x)}{h} - \left( \frac{h}{2} \right) f'' (\xi)$. The truncation error is proportional to *h*: first order, $O (h)$.

**2.** The table in Section 3.1 gives forward 2.858842 (error 0.140560) and central 2.722815 (error 0.0045327) for $h = 0.1$.

**3.** From the difference table: $f' (1.0) \approx 0.999770$ and $f'' (1.0) \approx - 0.990045$ (true values 1 and −1).

**4.** Trapezoidal 0.784241; Simpson $\frac{1}{3} 0.785398$; Simpson $\frac{3}{8} 0.785396$; true 0.785398.

**5.** Simpson's $\frac{1}{3}$ fits a parabola through three points, covering two strips, so strips must be paired. The $\frac{3}{8}$ rule fits a cubic through four points, covering three strips.

**6.** Trapezoid error ∝ $h^{2}$, so halving *h* divides it by about 4; Simpson ∝ $h^{4}$, so by about 16 (compare the convergence table in Section 3.2).

**7.** See the Romberg table in Section 3.3: the extrapolated $R (4 ,\  4) = 0.78539817$.

**8.** Simpson: 0.524074; exact: 0.523248; error 0.000826 (the trapezoidal rule gives 0.537500).

**9.** Truncation error falls with *h*, but round-off grows because $f (x + h) - f (x)$ subtracts nearly equal numbers, then is divided by a tiny *h*; and measured data carry noise which is amplified by $\frac{1}{h}$. Beyond an optimal *h* the total error increases.

**10.** The truncation error of the forward difference is about $\frac{h}{2}f''$ and falls with $h$. The round-off error is about $\varepsilon\,|f|/h$ (the subtraction of nearly equal numbers with relative error $10^{-16}$, divided by $h$). The sum is smallest where the two are equal, at $h \approx 10^{-8}$; below this the round-off term grows like $1/h$ (Section 3.6 table, 6.6e-9 at the minimum, 2.7 at $h = 10^{-16}$).

**11.** $D^{(1)}(0.4) = \dfrac{4(-0.835872) - (-0.819211)}{3} = \dfrac{-3.343488 + 0.819211}{3} = -0.841426$. The error is $|-0.841426 + 0.841471| = 4.5\times 10^{-5}$, a gain of about 500 over $D(0.4)$ (error 0.0223).

**12.** $f'(1) \approx \dfrac{\ln 0.8 - 8\ln 0.9 + 8\ln 1.1 - \ln 1.2}{1.2} = 0.999917$ against the true $1/x = 1$ (error $8.3\times 10^{-5}$).

**13.** $f = 1/x$ on $[1, 2]$: $|f''| = 2/x^{3} \le 2$ and $|f^{(4)}| = 24/x^{5} \le 24$. Trapezoid: $\dfrac{(1)h^{2}}{12}(2) \le 10^{-4}$ gives $h \le 0.0245$, so $n \ge 40.8$: **41 strips**. Simpson: $\dfrac{h^{4}}{180}(24) \le 10^{-4}$ gives $h \le 0.1655$, so $n \ge 6.04$, and with an even $n$: **8 strips**.

**14.** The exact value is $1/3$. Midpoint (points 0.125, 0.375, 0.625, 0.875): $0.25(0.015625 + 0.140625 + 0.390625 + 0.765625) = 0.328125$, error $-0.00521$. Trapezoid: $0.25\left(0 + 0.0625 + 0.25 + 0.5625 + 0.5\right) = 0.34375$, error $+0.01042$. The trapezoid error is twice the midpoint error and of opposite sign.

**15.** With $f(x) = x^{4}$ at 0, 0.25, 0.5, 0.75, 1: $0, 0.003906, 0.0625, 0.316406, 1$. Boole: $\dfrac{2(0.25)}{45}\left[0 + 32(0.003906) + 12(0.0625) + 32(0.316406) + 7\right] = \dfrac{0.5}{45}(18) = 0.2$. It is exact because the five-point Newton-Cotes rule is exact for all polynomials up to degree 5 (its error involves $f^{(6)}$, which is zero here).

**16.** Substitute $x = t + 1$, so $\int_0^2 (x^{3}+1)\,dx = \int_{-1}^{1}\left((t+1)^{3} + 1\right)dt$. The two-point rule gives $f(-0.57735) + f(0.57735)$ with $f(t) = (t+1)^{3} + 1$: $(0.42265)^{3} + 1 = 1.07550$ and $(1.57735)^{3} + 1 = 4.92450$, whose sum is **6.00000**. Exact: $\left[\frac{x^{4}}{4} + x\right]_0^2 = 4 + 2 = 6$. It is exact because the integrand is a cubic.

**17.** Map to $[1, 3]$: $x = t + 2$ and $dx = dt$. Nodes $t = 0, \pm 0.774597$ give $x = 2, 1.225403, 2.774597$ and the sum is $\frac{8}{9}\cdot\frac{1}{2} + \frac{5}{9}\left(\frac{1}{1.225403} + \frac{1}{2.774597}\right) = 1.098039$. True $\ln 3 = 1.098612$, error $-5.7\times 10^{-4}$ from only three function values.

**18.** With $x = t^{2}$: $\int_0^1 \dfrac{2t\,dt}{t(1+t^{2})} = \int_0^1 \dfrac{2\,dt}{1 + t^{2}}$, smooth. Values at $t = 0, 0.25, 0.5, 0.75, 1$: 2, 1.882353, 1.6, 1.28, 1. Simpson ($h = 0.25$): $\dfrac{0.25}{3}\left[2 + 1 + 4(1.882353 + 1.28) + 2(1.6)\right] = 1.570784$, against $\pi/2 = 1.570796$ (error $1.2\times 10^{-5}$).

**19.** The standard error falls like $1/\sqrt{N}$, so multiplying $N$ by 100 reduces it by 10 (one more decimal digit). The rate does not depend on the dimension, whereas a grid with $m$ points per axis needs $m^{d}$ points in $d$ dimensions. In one dimension Simpson or Gauss rules converge much faster; in ten dimensions grids are impossible but Monte Carlo keeps its $1/\sqrt{N}$ rate.

:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Evaluate the integral of $\sin x$ from 0 to pi using the trapezoidal rule and Simpson's one-third rule with four strips. Compare with the exact value.**

*Data.* *h* = pi/4 = 0.785398; the ordinates are y0 = 0, y1 = 0.70711, y2 = 1, y3 = 0.70711, y4 = 0.

*Trapezoidal rule.* $T = \left( \frac{h}{2} \right) [ y 0 + 2 ( y 1$ + y2 + y3) + y4] = 0.392699 $x [0 + 2 (2.41421) + 0]$ = **1.89612**.

*Simpson's rule.* $S = \left( \frac{h}{3} \right) [ y 0 + 4 ( y 1$ + y3) + 2 y2 + y4] = 0.261799 $x [0 + 4 (1.41421) + 2 + 0] = 0.261799 x$ 7.65685 = **2.00456**.

| Rule | Value | Exact | Error |
|---|---|---|---|
| Trapezoidal | 1.89612 | 2 | 0.10388 |
| Simpson $\frac{1}{3}$ | 2.00456 | 2 | -0.00456 |

Simpson is more than twenty times more accurate for the same ordinates (Figure 3.1) because it fits parabolas, not straight lines; its error is of order $h^{4}$, against $h^{2}$ for the trapezoidal rule. *Condition:* Simpson's $\frac{1}{3}$ rule needs an even number of strips. *Conclusion:* use Simpson's rule for smooth functions.

**Q2 (5 marks). Estimate the derivative of $e^{x}$ at $x = 1$ by the forward and central difference formulas with $h = 0.1$ and $h = 0.05$, and comment on the errors.**

*Formulas.* Forward: $f' (x)$ is about $\frac{f (x + h) - f (x)}{h}$, error $O (h)$. Central: $f' (x)$ is about $\frac{f (x + h) - f (x - h)}{2 h}$, error $O (h^{2})$. Exact value $e = 2.71828$.

| *h* | Forward | Error | Central | Error |
|---|---|---|---|---|
| 0.1 | 2.85884 | 0.14056 | 2.72281 | 0.00453 |
| 0.05 | 2.78739 | 0.06910 | 2.71941 | 0.00113 |

Halving *h* halves the forward error (0.14056 to 0.06910) but divides the central error by four (0.00453 to 0.00113), as the orders predict (Figure 3.3). *Warning:* making *h* extremely small loses accuracy through rounding error in the subtraction. *Conclusion:* prefer the central formula when values on both sides are available.

**Q3 (10 marks). Explain the Newton-Cotes rules and Romberg integration. Apply Romberg's method to the integral of $e^{x}$ on [0, 1].**

*Introduction.* When an integral has no closed form or the integrand is only a table, we replace *f* by an interpolating polynomial and integrate that (Plate 3.1 shows an older mechanical way). The resulting formulas are the **Newton-Cotes rules**.

*Rules.* (1) **Trapezoidal:** integral is about $\left( \frac{h}{2} \right) [y 0 + 2 (y 1 + \ldots + y (n - 1)) + y n]$, error $- \frac{(b - a) h^{2} f''}{12}$. (2) **Simpson $\frac{1}{3}$:** $\left( \frac{h}{3} \right) [y 0 + 4 (\mathrm{odd}) + 2 (\mathrm{even}) + y n] ,\  n$ even, error $- \frac{(b - a) h^{4} f''''}{180}$. (3) **Simpson $\frac{3}{8}$:** $\left( \frac{3 h}{8} \right) [ y 0$ + 3y1 + 3y2 + 2y3 + $\ldots + y n ] ,\  n$ a multiple of 3, same order. Figure 3.1 compares the first two.

*Romberg.* The trapezoidal error expands in even powers of *h*, so **Richardson extrapolation** removes them one by one: $R (i ,\  j) = R (i ,\  j - 1) + \frac{R (i ,\  j - 1) - R (i - 1 ,\  j - 1)}{4^{j} - 1}$. Start with trapezoid values for $h = 1 ,\  \frac{1}{2} ,\  \frac{1}{4}$: $T (1) = 0.5 (1 + 2.718282) = 1.859141 ;\  T (2) = 1.753931 ;\  T (4) = 1.727222$.

First extrapolation: $R (2 ,\  1) = 1.753931 + \frac{1.753931 - 1.859141}{3}$ = **1.718861**; $R (3 ,\  1) = 1.727222 + \frac{1.727222 - 1.753931}{3}$ = **1.718319**. Second: $R (3 ,\  2) = 1.718319 + \frac{1.718319 - 1.718861}{15}$ = **1.718283**, against the exact $e - 1 = 1.718282$ (Figure 3.2).

| Rule | Order of error | Needs | Best for |
|---|---|---|---|
| Trapezoidal | $h^{2}$ | any *n* | rough data, periodic functions |
| Simpson $\frac{1}{3}$ | $h^{4}$ | even *n* | smooth functions |
| Simpson $\frac{3}{8}$ | $h^{4}$ | *n* multiple of 3 | odd strips |
| Romberg | $h^{2} ,\  h^{4} ,\  h^{6} \ldots$ | halving *h* | high accuracy by reuse |

*Conclusion.* Romberg integration reaches six correct decimals from only four function evaluations beyond the trapezoid starts, and the difference between successive entries gives a built-in error estimate. Use Simpson for a quick answer and Romberg when high accuracy is required.

**Q4 (5 marks). Evaluate $\int_0^1 \dfrac{dx}{1 + x^{2}}$ by the two-point and three-point Gauss–Legendre rules and compare with the exact value $\pi/4$.**

*Formula.* $\int_0^1 f\,dx = \dfrac{1}{2}\int_{-1}^{1} f\!\left(\dfrac{t+1}{2}\right)dt \approx \dfrac{1}{2}\sum w_i f(x_i)$ with $x_i = (t_i + 1)/2$.

| Rule | nodes $x_i$ | $f(x_i)$ | weights | estimate | error |
|---|---|---|---|---|---|
| 2 points | 0.211325, 0.788675 | 0.957251, 0.616520 | 1, 1 | 0.786885 | +1.5e-03 |
| 3 points | 0.112702, 0.5, 0.887298 | 0.987458, 0.8, 0.559504 | 0.555556, 0.888889, 0.555556 | 0.785267 | −1.3e-04 |

*Working for three points.* $\tfrac{1}{2}\left[0.555556(0.987458 + 0.559504) + 0.888889(0.8)\right] = \tfrac{1}{2}(0.859423 + 0.711111) = 0.785267$.

*Conclusion.* The exact value is $\pi/4 = 0.785398$. Three function values give three correct digits (Simpson's rule with the same three points gives 0.783333, an error of hBc6.5\times 10^{-4}$, five times worse).
