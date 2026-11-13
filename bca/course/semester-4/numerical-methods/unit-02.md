---
subject: Numerical Methods
grade: BCA Semester 4
unit: 2
title: Interpolation and Approximation
hours: 8
area: BCA 253 · Numerical Methods · Unit 2
---

An experiment gives you the temperature at 6, 9, 12 and 15 hours; what was it at 10:30? A table of $\sin x$ lists whole degrees; what is $\sin 5 ^{\circ}$? **Interpolation** constructs a function that passes exactly through the known data points and reads off intermediate values. **Approximation** (least squares) instead fits a simple curve *near* noisy data without passing through every point.

::: key What this unit gives you
- Interpolating polynomials: Lagrange, Newton divided differences, Newton forward and backward differences.
- The error of polynomial interpolation.
- Cubic spline interpolation.
- Least-squares fitting of lines, exponentials and polynomials.
:::

## 2.1 Introduction and uniqueness

Given $n + 1$ distinct points $(x_{0} ,\  y_{0}) ,\  \ldots ,\  (x_{n} ,\  y_{n})$, there is **exactly one polynomial of degree at most *n*** through all of them. Lagrange's and Newton's formulas are different ways to write the *same* polynomial, so they must give the same value; that is a handy check.

Estimating inside $[x_{0} ,\  x_{n}]$ is **interpolation**; estimating outside is **extrapolation**, which is far less reliable.

## 2.2 Errors in polynomial interpolation

If *f* has $n + 1$ continuous derivatives and $P_{n}$ interpolates *f* at $x_{0} \ldots x_{n}$, then for some *ξ* in the interval

$$f (x) - P_{n} (x) = \frac{f^{(n+1)} (\xi)}{(n + 1) !} \cdot (x - x_{0}) (x - x_{1}) \ldots (x - x_{n})$$

The product term is small near the middle of the data and large near the ends, so interpolate near the centre. Raising the degree does not always help: for equally spaced points and some functions (Runge's example $\frac{1}{(1 + 25 x^{2})}$) the error at the ends *grows* with *n*. This is one reason to prefer splines for many points.

## 2.3 Lagrange interpolation

Each point has a **basis polynomial** $L_{i} (x) = \frac{\Pi_{j \neq i} (x - x_{j})}{(x_{i} - x_{j})}$, which is 1 at $x_{i}$ and 0 at all other nodes; then **$P_{n} (x) = \sum y_{i} L_{i} (x)$**. It works for unequal spacing, but adding a point means starting again.

::: example Interpolating ln x at x = 2.5
Data:

| *i* | $x_{i}$ | $y_{i} = \ln x_{i}$ |

|---|---|---|

| 0 | 1 | 0.000000 |

| 1 | 2 | 0.693147 |

| 2 | 3 | 1.098612 |

| 3 | 4 | 1.386294 |

For $x = 2.5$ and four nodes the weights $L_{0} \ldots L_{3}$ are -0.0625, 0.5625, 0.5625, -0.0625 (they always sum to 1). Then $P_{3} (2.5) = 0.921221$. The true $\ln 2.5 = 0.916291$, so the error is 0.004931. The theoretical bound uses $f'''' (x) = - \frac{6}{x^{4}}$, at most 6 on [1, 4], and the product |(2.5 − $1 ) (2.5 - 2) (2.5 - 3) ( 2.5$ − 4)| = 0.5625, giving $|\mathrm{error}| \leq \left( \frac{6}{4 !} \right) (0.5625) = 0.140625$. The actual error is well inside the bound. Using only the three nearest nodes 2, 3, 4 gives 0.910603 with error 0.005688: more points here helped only slightly.
:::

## 2.4 Newton's interpolation with divided differences

**Divided differences** are defined by $f [x_{i}] = y_{i} ,\  f [x_{i} ,\  x_{i+1}] = \frac{(f [x_{i+1}] - f [x_{i}])}{(x_{i+1} - x_{i})}$, and so on, each order dividing by the total span. The interpolating polynomial is

$$P_{n} (x) = f [x_{0}] + f [x_{0} ,\  x_{1}] (x - x_{0}) + f [x_{0} ,\  x_{1} ,\  x_{2}] (x - x_{0}) (x - x_{1}) + \ldots$$

Adding a new data point adds one term and one table diagonal; nothing already computed is wasted. Works for unequal spacing.

::: example Divided-difference table for ln x
| $x_{i}$ | $f [x_{i}]$ | $f [x_{i} ,\  x_{i+1}]$ | f[·,·,·] | f[·,·,·,·] |

|---|---|---|---|---|

| 1 | 0.000000 | 0.693147 | -0.143841 | 0.028317 |

| 2 | 0.693147 | 0.405465 | -0.058892 |  |

| 3 | 1.098612 | 0.287682 |  |  |

| 4 | 1.386294 |  |  |  |

The top diagonal gives the coefficients 0.000000, 0.693147, -0.143841, 0.028317. Then $P_{3} (2.5) = 0 + 0.693147 (1.5) - 0.143841 (1.5) (0.5) + 0.028317 (1.5) (0.5) (- 0.5) = 0.921221$, identical to the Lagrange value, as it must be.
:::

## 2.5 Newton's forward and backward difference formulas (equal spacing)

For equally spaced nodes with step *h* define **forward differences** $\Delta y_{0} = y_{1} - y_{0} ,\  \Delta^{2} y_{0} = \Delta y_{1} - \Delta y_{0}$, and so on. With **$u = \frac{(x - x_{0})}{h}$**:

**Forward:** $y (x) \approx y_{0} + u \Delta y_{0} + \frac{u (u - 1)}{2 !} \Delta^{2} y_{0} + \frac{u (u - 1) (u - 2)}{3 !} \Delta^{3} y_{0} + \ldots$

Use it near the **start** of the table. Near the **end**, use the **backward** formula with **$u = \frac{(x - x_{n})}{h}$**, the last entry of each difference column $(\nabla)$:

**Backward:** $y (x) \approx y_{n} + u \nabla y_{n} + \frac{u (u + 1)}{2 !} \nabla^{2} y_{n} + \frac{u (u + 1) (u + 2)}{3 !} \nabla^{3} y_{n} + \ldots$

::: example sin x from a table of whole 10° steps (four-decimal data)
| $x ^{\circ}$ | $y = \sin x$ | $\Delta y$ | $\Delta^{2} y$ | $\Delta^{3} y$ | $\Delta^{4} y$ |

|---|---|---|---|---|---|

| 0 | 0.0000 | 0.1736 | -0.0052 | -0.0052 | 0.0004 |

| 10 | 0.1736 | 0.1684 | -0.0104 | -0.0048 |  |

| 20 | 0.3420 | 0.1580 | -0.0152 |  |  |

| 30 | 0.5000 | 0.1428 |  |  |  |

| 40 | 0.6428 |  |  |  |  |

**$\sin 5 ^{\circ}$ by the forward formula:** $h = 10 ,\  u = \frac{5 - 0}{10} = 0.5$. The top-row differences are 0.0000, 0.1736, -0.0052, -0.0052, 0.0004. The result is $\sin 5 ^{\circ} \approx 0.08711$; the true value is 0.08716.

**$\sin 35 ^{\circ}$ by the backward formula:** $u = \frac{35 - 40}{10} = - 0.5$. The bottom-diagonal differences are 0.6428, 0.1428, -0.0152, -0.0048, 0.0004, giving $\sin 35 ^{\circ} \approx 0.57358$; the true value is 0.57358.

The differences become small and nearly constant at the fourth order, a sign that a quartic fits well. The forward result is off in the fourth decimal because the table itself is rounded to four decimals and differences amplify that rounding.
:::

**Choosing a formula.** Divided differences for unequal spacing; forward formula for a point near the beginning; backward near the end; for the middle use central-difference formulas (Gauss, Stirling, not required here).

## 2.6 Cubic spline interpolation

A single high-degree polynomial through many points can oscillate. A **cubic spline** instead uses a different cubic on each interval $[x_{i} ,\  x_{i+1}]$, joined so that the function, its first derivative and its second derivative are continuous at every interior node. It is smooth to the eye and well behaved, and is the mathematical form of a draughtsman's flexible ruler.

With *n* intervals there are $4 n$ unknown coefficients. Interpolation ($2 n$ conditions) plus continuity of $S'$ and $S''$ at the $n - 1$ interior nodes $(2 n - 2)$ leaves two conditions; for a **natural spline** we set $S'' = 0$ at both ends.

**Method.** Let $M_{i} = S'' (x_{i})$ and $h_{i} = x_{i+1} - x_{i}$. The continuity of $S'$ gives, for each interior node $\ast i \ast$,

$$h_{i-1} M_{i-1} + 2 (h_{i-1} + h_{i}) M_{i} + h_{i} M_{i+1} = 6 \left[ \frac{(y_{i+1} - y_{i})}{h_{i}} - \frac{y_{i} - y_{i-1}}{h_{i-1}} \right]$$

a tridiagonal system. On each interval, with $t = x - x_{i}$,

$S (x) = y_{i} + b_{i} t + \left( \frac{M_{i}}{2} \right) t^{2} + \left( \frac{(M_{i+1} - M_{i})}{(6 h_{i})} \right) t^{3}$, where $b_{i} = \frac{(y_{i+1} - y_{i})}{h_{i}} - \frac{h_{i} (2 M_{i} + M_{i+1})}{6}$.

::: example Natural spline through (1, 2), (2, 3), (3, 5), (4, 4)
With $h = 1$ the two interior equations are $4 M_{1} + M_{2} = 6 (2 - 1) = 6$ and $M_{1} + 4 M_{2} = 6 (- 1 - 2) = - 18$ (with $M_{0} = M_{3} = 0$, using index 0 to 3 for the four nodes). Solving gives the second derivatives $M = (0.00000 ,\  2.80000 ,\  - 5.20000 ,\  0.00000)$. The pieces:

| interval | a | *b* | *c* | $d (S = a + b t + c t^{2} + d t^{3} ,\  t = x - x_{i})$ |

|---|---|---|---|---|

| [1, 2] | 2.00000 | 0.53333 | 0.00000 | 0.46667 |

| [2, 3] | 3.00000 | 1.93333 | 1.40000 | -1.33333 |

| [3, 4] | 5.00000 | 0.73333 | -2.60000 | 0.86667 |

Then $S (1.5) = 2.32500$ and $S (2.5) = 4.15000$. (A straight line through the neighbours of 2.5 would give 4.0, but the spline bends to reflect the whole data set.) The results agree with SciPy's CubicSpline(bc_type="natural").
:::

## 2.7 Least-squares approximation

When data come from measurement they carry noise and passing through every point is pointless. The **least-squares method** chooses the curve that minimises the sum of squared vertical residuals $S = \sum (y_{i} - f (x_{i}))^{2}$.

### Straight line y = a + bx

Setting $\frac{\partial S}{\partial a} = \frac{\partial S}{\partial b} = 0$ gives the **normal equations**

$\sum y = n a + b \sum x ,\  \sum x y = a \sum x + b \sum x^{2}$,

so **$b = \frac{n \sum x y - \sum x \sum y}{n \sum x^{2} - \left( \sum x \right)^{2}}$** and **$a = \frac{\sum y - b \sum x}{n}$**.

::: example Fit a line to five points
| *x* | *y* | $x^{2}$ | $x y$ |

|---|---|---|---|

| 1 | 2.2 | 1 | 2.2 |

| 2 | 2.8 | 4 | 5.6 |

| 3 | 3.6 | 9 | 10.8 |

| 4 | 4.5 | 16 | 18.0 |

| 5 | 5.1 | 25 | 25.5 |

| $\sum = 15$ | 18.2 | 55 | 62.1 |

$\sum x = 15 ,\  \sum y = 18.2 ,\  \sum x^{2} = 55 ,\  \sum x y = 62.1$ with $n = 5$. Then $b = \frac{5 \times 62.1 - 15 \times 18.2}{(5 \times 55 - 15^{2})} = 0.7500$ and $a = \frac{18.2 - 0.7500 \times 15}{5} = 1.3900$. The line is **$y = 1.3900 + 0.7500 x$**. The residual sum of squares is 0.0270 and $R^{2} = 0.9952$, an excellent fit. Predicting $x = 6$ gives 5.890 (extrapolation, so treat it with caution).
:::

### Non-linear data: reduction to linear form

| Model | Transformation | Fit line to |
|---|---|---|
| $y = A e^{B x}$ | $\ln y = \ln A$ + Bx | $(x ,\  \ln y)$ |
| $y = A x^{B}$ | $\ln y = \ln A + B \ln x$ | $(\ln x ,\  \ln y)$ |
| $y = \frac{1}{a + b x}$ | $\frac{1}{y} = a + b x$ | $\left( x ,\  \frac{1}{y} \right)$ |
| $y = a + \frac{b}{x}$ | $y = a$ + b·(1/x) | $\left( \frac{1}{x} ,\  y \right)$ |

::: example Exponential model y = A e^(Bx)
| *x* | *y* | $\ln y$ | x·ln *y* |

|---|---|---|---|

| 1 | 2.7 | 0.9933 | 0.9933 |

| 2 | 4.0 | 1.3863 | 2.7726 |

| 3 | 6.1 | 1.8083 | 5.4249 |

| 4 | 9.2 | 2.2192 | 8.8768 |

| 5 | 13.5 | 2.6027 | 13.0134 |

Fitting a straight line to $(x ,\  \ln y)$ gives $B = 0.4052$ and $\ln A = 0.5864$, so $A = 1.7975$ and **$y = 1.7975 e^{0.4052 x}$**. The prediction at $x = 6$ is 20.44. Note that this minimises the error in $\ln y$, not in *y*, which weights small values more; it is the standard quick method.
:::

### Polynomial (quadratic) fit

For $y = a + b x + c x^{2}$ the normal equations are $\sum y = n a + b \sum x + c \sum x^{2} ,\  \sum x y = a \sum x + b \sum x^{2} + c \sum x^{3} ,\  \sum x^{2} y = a \sum x^{2} + b \sum x^{3} + c \sum x^{4}$. For the line data above, solving gives $(a ,\  b ,\  c) = (1.4400 ,\  0.7071 ,\  0.0071)$: the $x^{2}$ coefficient is nearly zero, confirming that the straight line was enough.

## 2.8 Seeing the ideas: one polynomial, divided differences, Runge's warning and the best-fit line

The three people in Plate 2.1 gave their names to the three tools of this unit. The figures that follow show what each tool does on real numbers.

```photogrid label="2.1" cols="3" ratio="1.0" caption="Three founders. (a) Joseph-Louis Lagrange (1736-1813), whose basis-polynomial form of interpolation appeared in the 1790s. (b) Isaac Newton, who built the divided-difference form that lets a new data point be added without redoing the work. (c) Carl Friedrich Gauss, who used least squares in 1801 to recover the lost orbit of the asteroid Ceres from a few noisy observations."
@ photo id="bca204/lagrange" cap="Lagrange"
fit 1.0
focus 0.5 0.7
@ photo id="bca104/newton" cap="Newton"
fit 1.0
focus 0.5 0.7
@ photo id="bca204/gauss" cap="Gauss"
fit 1.0
focus 0.5 0.7
```

```svgfig label="2.1" caption="Interpolating $\ln x$ through the points $x = 1 ,\  2 ,\  4 ,\  6$. The cubic (red) passes exactly through the four points but is only approximate between them: at $x = 3$ it gives 1.12342 against the true 1.09861 (error 0.02481), and at $x = 5$ it gives 1.57725 against 1.60944 (error 0.03219)."
import math
f = Fig(580, 230)
ax = Axes(f, 50, 14, 510, 170, (0.5, 6.5), (-0.5, 2.2))
ax.grid(1, 0.5)
ax.axes("", "")
xs = [1, 2, 4, 6]; ys = [math.log(v) for v in xs]
def P(t):
    s = 0
    for i in range(4):
        p = ys[i]
        for j in range(4):
            if i != j: p *= (t - xs[j]) / (xs[i] - xs[j])
        s += p
    return s
ax.curve(math.log, 0.5, 6.5, color=NAVY)
ax.curve(P, 0.5, 6.5, color=RED, dash=True)
for x_, y_ in zip(xs, ys): ax.pt(x_, y_, "", color=NAVY)
ax.pt(3, P(3), "P(3) = 1.1234", dx=8, dy=14, color=RED, size=10)
ax.pt(5, P(5), "P(5) = 1.5773", dx=-8, dy=16, color=RED, size=10, anchor="end")
f.text(120, 38, "ln x (true)", size=10, color=NAVY, bold=True)
f.text(120, 54, "cubic P(x)", size=10, color=RED, bold=True)
f.text(306, 222, "data points at x = 1, 2, 4, 6", size=10, color=SLATE)
```

```svgfig label="2.2" caption="The divided-difference table for the same four points. Each column is made from the column to its left: (right - left) divided by the span of *x* values. The top diagonal 0, 0.69315, -0.11552, 0.01591 gives the Newton form $P (x) = 0 + 0.69315 (x - 1) - 0.11552 (x - 1) (x - 2) + 0.01591 (x - 1) (x - 2) (x - 4)$."
f = Fig(580, 190)
H = ["x", "f(x)", "1st", "2nd", "3rd"]
for i, h in enumerate(H): f.box(10 + i * 112, 8, 100, 22, h, fill=NAVY, stroke=NAVY, color="#ffffff", bold=True, size=10.5)
X = ["1", "2", "4", "6"]; F = ["0.00000", "0.69315", "1.38629", "1.79176"]
D1 = ["0.69315", "0.34657", "0.20273"]; D2 = ["-0.11552", "-0.03596"]; D3 = ["0.01591"]
for i in range(4):
    y = 38 + i * 36
    f.box(10, y, 100, 28, X[i], fill=BLUE, stroke=NAVY, size=10.5)
    f.box(122, y, 100, 28, F[i], fill=BLUE, stroke=NAVY, size=10.5)
for i, v in enumerate(D1): f.box(234, 56 + i * 36, 100, 28, v, fill=MINT, stroke=TEAL, size=10.5)
for i, v in enumerate(D2): f.box(346, 74 + i * 36, 100, 28, v, fill=SAND, stroke=AMBER, size=10.5)
f.box(458, 92, 100, 28, "0.01591", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.text(290, 184, "top diagonal = Newton coefficients", size=10.5, color=TEAL, bold=True)
```

```svgfig label="2.3" caption="Runge's phenomenon. For $f (x) = \frac{1}{(1 + 25 x^{2})}$ on [-1, 1], the degree-10 polynomial through 11 equally spaced points (red) wiggles wildly near the ends although it matches at every node; the true curve (blue) is smooth. More points of equal spacing make it worse, which is why splines or Chebyshev nodes are used instead."
f = Fig(580, 230)
ax = Axes(f, 50, 14, 510, 170, (-1, 1), (-0.6, 1.4))
ax.grid(0.5, 0.2)
ax.axes("", "")
fn = lambda x: 1 / (1 + 25 * x * x)
nodes = [-1 + 0.2 * k for k in range(11)]
def L(t):
    s = 0
    for i, xi in enumerate(nodes):
        p = fn(xi)
        for j, xj in enumerate(nodes):
            if i != j: p *= (t - xj) / (xi - xj)
        s += p
    return s
ax.curve(L, -1, 1, color=RED, dash=True)
ax.curve(fn, -1, 1, color=NAVY)
for xi in nodes: ax.pt(xi, fn(xi), "", color=NAVY, r=3)
f.text(150, 60, "true function", size=10, color=NAVY, bold=True)
f.text(110, 186, "degree-10 interpolant", size=10, color=RED, bold=True)
f.text(306, 222, "11 equally spaced nodes", size=10, color=SLATE)
```

```svgfig label="2.4" caption="Least-squares line through five noisy points (1, 2.1), (2, 3.9), (3, 6.2), (4, 7.8), (5, 10.1). The line $y = 0.05$ + 1.99x minimises the sum of the squared vertical residuals (the red segments), $S = 0.107$. At $x = 6$ it predicts 11.99."
f = Fig(580, 230)
ax = Axes(f, 50, 14, 510, 170, (0, 7), (0, 14))
ax.grid(1, 2)
ax.axes("", "")
D = [(1, 2.1), (2, 3.9), (3, 6.2), (4, 7.8), (5, 10.1)]
ax.curve(lambda x: 0.05 + 1.99 * x, 0, 7, color=NAVY)
for x_, y_ in D:
    f.line(ax.X(x_), ax.Y(y_), ax.X(x_), ax.Y(0.05 + 1.99 * x_), color=RED, sw=2)
    ax.pt(x_, y_, "", color=TEAL)
ax.pt(6, 11.99, "prediction x = 6: 11.99", dx=-8, dy=-12, anchor="end", hollow=True, color=NAVY, size=10)
f.text(150, 40, "y = 0.05 + 1.99 x", size=11, color=NAVY, bold=True)
f.text(306, 222, "x", size=10, color=SLATE)
```

### 2.8.1 Eight uses of interpolation and curve fitting

1. **Filling gaps in tables.** A weather office records temperature every three hours, and interpolation estimates the value at any time between readings. The same idea fills missing rows in a data sheet. It is the first step of most data cleaning.
2. **Estimating values from old tables.** Before calculators, logarithm and trigonometry tables gave values at fixed steps, and interpolation gave the rest. Engineers still read steam tables and statistical tables this way. The error formula tells how close the answer is.
3. **Smooth curves in computer graphics.** Splines pass through control points and give smooth roads, fonts and animation paths. A letter in a font file is a few spline pieces. Cubic splines are used because they avoid the wiggles seen in Figure 2.3.
4. **Image and video resizing.** When a photo is enlarged, the computer must invent the new pixels by interpolating between neighbours. Bilinear and bicubic interpolation are the common methods. Mobile phone zoom depends on them.
5. **Trend lines and forecasting.** A least-squares line through exam marks, sales or population counts shows the trend and predicts the next value. A Nepali college can project next year's admissions. The residual sum tells how reliable the line is.
6. **Calibrating instruments.** A sensor gives voltage while the true reading is temperature or pressure. A fitted line or curve converts voltage to the true unit. Every digital thermometer does this inside.
7. **Numerical integration and differentiation.** Rules such as Simpson's are derived by fitting a polynomial through a few points and integrating it. Interpolation is therefore the base of the next unit. Without it there would be no Newton-Cotes formulas.
8. **Machine learning and data science.** Linear regression is least squares, and curve fitting underlies many models that learn from noisy data. Understanding it explains overfitting, which is the modern form of Runge's wiggles. The idea of balance between fit and smoothness appears everywhere.

## 2.9 Neville's algorithm and inverse interpolation

**Neville's algorithm** evaluates the interpolating polynomial at *one* value $x$ without ever finding its coefficients. Write $P_{i,j}(x)$ for the value at $x$ of the polynomial through the nodes $x_i, \dots, x_j$. Single nodes give $P_{i,i} = y_i$, and each higher entry blends two neighbours:

$$P_{i,j}(x) = \frac{(x - x_i)\,P_{i+1,j}(x) - (x - x_j)\,P_{i,j-1}(x)}{x_j - x_i} .$$

The table is built column by column and the top-right entry is the answer. It is the method of choice when the interpolant is needed at a single point, and the intermediate columns show how the estimate settles as nodes are added.

::: example cos 0.8 from the nodes 0, 0.5, 1.0, 1.5
Node values: $\cos 0 = 1.000000$, $\cos 0.5 = 0.877583$, $\cos 1.0 = 0.540302$, $\cos 1.5 = 0.070737$.

| $x_i$ | $P_{i,i}$ | $P_{i,i+1}$ | $P_{i,i+2}$ | $P_{i,i+3}$ |
|---|---|---|---|---|
| 0.0 | 1.000000 | 0.804132 | 0.700998 | **0.695713** |
| 0.5 | 0.877583 | 0.675214 | 0.691089 | |
| 1.0 | 0.540302 | 0.728128 | | |
| 1.5 | 0.070737 | | | |

The true value is $\cos 0.8 = 0.696707$, so the cubic interpolant is in error by $9.9\times 10^{-4}$. The successive top-row entries 1.000, 0.804, 0.701, 0.696 show the estimate converging, and the last step changes it by only 0.005, which is a useful warning of the size of the remaining error. Newton's divided differences (Section 2.4) give the *same* polynomial; Neville avoids storing its coefficients.
:::

**Inverse interpolation.** Given a table of $y = f(x)$ and a target value $y^{*}$, find the $x$ with $f(x) = y^{*}$. If $f$ is monotonic on the table, interchange the roles: interpolate $x$ as a function of $y$ with Lagrange or Newton, and evaluate at $y^{*}$. Setting $y^{*} = 0$ gives a **root-finding method** that needs only tabulated values (no derivative). The $x$ values need not be equally spaced, so Lagrange's form is the natural tool.

::: example Root of x³ − x − 2 from a table
For $x = 1.4, 1.5, 1.6, 1.7$ the values are $-0.656, -0.125, +0.496, +1.213$. Lagrange interpolation of $x$ against $y$ at $y = 0$ gives $x = 1.52143$ (true root 1.52138, error $5\times 10^{-5}$). A coarser table with $x = 1.0, 1.2, 1.4, 1.6$ gives only 1.5136, an error of 0.008: the polynomial in $y$ must follow $x = f^{-1}(y)$, which curves more sharply when the table spacing is wide. Narrow the bracket first.
:::

## 2.10 Error bound and the choice of nodes: Chebyshev points

For $n+1$ nodes the interpolation error at $x$ is

$$f(x) - p_n(x) = \frac{f^{(n+1)}(\xi)}{(n+1)!}\,(x - x_0)(x - x_1)\cdots(x - x_n),\qquad \xi \in (\min, \max).$$

The first factor is a property of $f$; the product $w(x) = \prod (x - x_i)$ is a property of the **nodes**, and we are free to choose them.

::: example Error bound for sin x at x = π/8 with three nodes 0, π/4, π/2
Here $|f'''| = |\cos \xi| \le 1$ and $w(\pi/8) = (\pi/8)(-\pi/8)(-3\pi/8) = 0.18168$. So $|E| \le \dfrac{0.18168}{3!} = 0.0303$. The actual error of the quadratic through the three nodes is 0.0226, comfortably inside the bound. The bound is only as good as the estimate for the derivative.
:::

**Which nodes make $\max|w(x)|$ smallest?** Equally spaced nodes make $w$ small in the middle and large near the ends, which is the cause of Runge's phenomenon (Section 2.8). The minimum possible maximum over $[-1, 1]$ is achieved by the **Chebyshev nodes**, the zeros of the Chebyshev polynomial $T_{n+1}$:

$$x_k = \cos\!\left(\frac{(2k+1)\pi}{2(n+1)}\right),\qquad k = 0, 1, \dots, n,$$

which bunch up towards the ends of the interval. For a general interval $[a, b]$ map them with $x = \frac{a+b}{2} + \frac{b-a}{2}\,x_k$. For $n = 4$ the nodes on $[-1, 1]$ are $\pm 0.9511$, $\pm 0.5878$ and 0. With them $\max|w| = 2^{-n}$ (for $[-1, 1]$) which is the best possible.

::: example Interpolating 1/(1 + 25x²) on [−1, 1]
Maximum error over the interval for a polynomial of degree $n$ (computed on a fine grid):

| Degree $n$ | Equally spaced nodes | Chebyshev nodes |
|---|---|---|
| 4 | 0.438 | 0.402 |
| 8 | 1.045 | 0.171 |
| 12 | 3.663 | 0.0692 |
| 16 | 14.39 | 0.0326 |
| 20 | 59.82 | 0.0153 |

With equally spaced nodes the error *grows* by a factor of about four for every four extra nodes; with Chebyshev nodes it shrinks steadily. Same function, same degree, same method; only the node positions differ.
:::

```svgfig label="2.5" caption="Maximum interpolation error of $1/(1 + 25x^{2})$ on [-1, 1] against polynomial degree (log scale; 0 means an error of 1, 1 means an error of 10). Equally spaced nodes (red) get steadily worse, Chebyshev nodes (navy) steadily better. Values from the table above."
import math
f = Fig(540, 240)
ax = Axes(f, 56, 14, 500, 180, (2, 22), (-2.2, 2.2))
ax.grid(4, 1)
ax.axes("", "")
deg = [4, 8, 12, 16, 20]
eq = [0.4384, 1.0452, 3.6634, 14.3939, 59.8223]
ch = [0.402, 0.1708, 0.0692, 0.0326, 0.0153]
for vals, col in ((eq, RED), (ch, NAVY)):
    P = [(d, math.log10(v)) for d, v in zip(deg, vals)]
    for (x1, y1), (x2, y2) in zip(P, P[1:]):
        f.line(ax.X(x1), ax.Y(y1), ax.X(x2), ax.Y(y2), color=col, sw=2.4)
    for x, y in P:
        f.circle(ax.X(x), ax.Y(y), 3.6, fill=col, stroke=col)
f.text(380, 40, "equally spaced nodes", size=10.5, color=RED, bold=True)
f.text(380, 160, "Chebyshev nodes", size=10.5, color=NAVY, bold=True)
f.text(280, 214, "polynomial degree n", size=10.5, color=SLATE)
f.text(280, 230, "log10 of the maximum error", size=10, color=SLATE)
```

```svgfig label="2.6" caption="Where to place the nodes. Equal angles on a semicircle project onto the axis as the Chebyshev nodes (navy): they crowd towards both ends. Equally spaced nodes of the same number (red, below the axis) are uniform. Fourteen nodes on [-1, 1]."
import math
f = Fig(560, 230)
cx, cy, R = 280, 150, 215
f.line(cx - R - 10, cy, cx + R + 10, cy, color=SLATE, sw=1.4)
pts = []
for i in range(0, 61):
    t = math.pi * i / 60
    pts.append((cx + R * math.cos(t), cy - R * 0.6 * math.sin(t)))
for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
    f.line(x1, y1, x2, y2, color=SLATE, sw=1.2)
for k in range(14):
    t = math.pi * (2 * k + 1) / 28
    x, y = cx + R * math.cos(t), cy - R * 0.6 * math.sin(t)
    f.line(x, y, x, cy, color=NAVY, sw=0.9, dash=True)
    f.circle(x, y, 3, fill=BLUE, stroke=NAVY)
    f.circle(x, cy, 4.5, fill=BLUE, stroke=NAVY)
    xe = cx - R + 2 * R * k / 13
    f.circle(xe, cy + 26, 4.5, fill=ROSE, stroke=RED)
f.text(cx - R - 8, cy + 54, "-1", size=10, color=SLATE)
f.text(cx + R - 6, cy + 54, "+1", size=10, color=SLATE)
f.text(cx - 4, cy + 54, "0", size=10, color=SLATE)
f.text(cx - 60, 24, "Chebyshev nodes (navy)", size=10.5, color=NAVY, bold=True)
f.text(cx - 100, cy + 76, "equally spaced nodes (red)", size=10.5, color=RED, bold=True)
```

## 2.11 Central differences and checking a difference table

**Stirling's formula.** Newton's forward and backward formulas are best at the start and end of a table. For a point near the **middle**, central-difference formulas use values on both sides and converge faster. With $p = (x - x_0)/h$ and the central entry $y_0$, *Stirling's formula* is

$$y_p = y_0 + p\,\frac{\Delta y_{-1} + \Delta y_0}{2} + \frac{p^{2}}{2}\Delta^{2}y_{-1} + \frac{p(p^{2}-1)}{3!}\cdot\frac{\Delta^{3}y_{-2} + \Delta^{3}y_{-1}}{2} + \frac{p^{2}(p^{2}-1)}{4!}\Delta^{4}y_{-2} + \cdots$$

It is most accurate for $|p| \le 0.25$ but works well up to about 0.5.

::: example e^1.04 from the table e^x at 0.8, 0.9, 1.0, 1.1, 1.2 (x₀ = 1.0, h = 0.1, p = 0.4)
Values: 2.225541, 2.459603, 2.718282, 3.004166, 3.320117.

| $x$ | $y$ | $\Delta y$ | $\Delta^2 y$ | $\Delta^3 y$ | $\Delta^4 y$ |
|---|---|---|---|---|---|
| 0.8 | 2.225541 | 0.234062 | 0.024617 | 0.002589 | 0.000272 |
| 0.9 | 2.459603 | 0.258679 | 0.027205 | 0.002861 | |
| 1.0 | 2.718282 | 0.285884 | 0.030067 | | |
| 1.1 | 3.004166 | 0.315951 | | | |
| 1.2 | 3.320117 | | | | |

With two terms plus the second-difference term the estimate is 2.829371 (error $1.5\times 10^{-4}$); with all terms through $\Delta^{4}$ it is **2.829217**, against the true $e^{1.04} = 2.829217$ (error $3\times 10^{-7}$). Every added difference gains roughly two decimals, so the size of the next difference tells you when to stop.
:::

**Finding bad data with differences.** The $k$-th differences of a polynomial of degree $k$ are constant, and for smooth data they are small and smooth. A single wrong entry spreads into the table in the **binomial pattern** $\varepsilon\,(1, -1)$, $\varepsilon\,(1, -2, 1)$, $\varepsilon\,(1, -3, 3, -1)$, ... growing in each column, with the middle value in line with the mistake.

::: example A typo in a table of x³
The true values for $x = 0, 1, \dots, 7$ are 0, 1, 8, 27, 64, 125, 216, 343; a clerk writes 74 for 64. Third differences should be a constant 6:

| | | | | | | | |
|---|---|---|---|---|---|---|---|
| $y$ | 0 | 1 | 8 | 27 | 74 | 125 | 216 | 343 |
| $\Delta^3 y$ | 6 | 16 | −24 | 36 | −4 | | | |

The deviations from 6 are 0, 10, −30, 30, −10, which is $10\times(1, -3, 3, -1)$: the pattern of a single error of size $\varepsilon = 10$, centred on the fifth value, 74. Correcting it to 64 restores the constant 6.
:::

## 2.12 Piecewise interpolation compared: linear, spline and one polynomial

A single high-degree polynomial through many points oscillates (Section 2.8). The remedy is a **piecewise** interpolant: low-degree pieces joined at the nodes. Piecewise linear interpolation joins the points with straight lines: continuous but with corners, and error $\le \dfrac{h^{2}}{8}\max|f''|$. A **cubic spline** (Section 2.6) uses a cubic on every sub-interval and demands matching $y$, $y'$ and $y''$ at every interior node, which makes it smooth to the eye. Two extra conditions are needed at the ends: the **natural** spline sets $S'' = 0$ there; the **clamped** spline sets $S'$ to the known end slopes. The clamped spline is more accurate when the end slopes are known; the natural spline forces a zero second derivative that the data may not have.

::: example Five points of sin x on [0, π] (h = π/4): maximum error over the whole interval
| Interpolant | Maximum error |
|---|---|
| Piecewise linear | 0.0704 |
| One polynomial of degree 4 | 0.00181 |
| Natural cubic spline | 0.00107 |
| Clamped cubic spline (slopes +1 and −1) | 0.00112 |

At $x = 1.0$ (true $\sin 1 = 0.841471$) the linear value is 0.787137, the natural spline 0.840726 and the clamped spline 0.840662. On smooth data like this the spline beats the degree-4 polynomial although it uses the same five points, and unlike the polynomial it does not get worse as points are added. Natural and clamped agree to about $5\times 10^{-4}$ because the true end curvature of sine is near zero, so the natural condition is nearly right here.
:::

## 2.13 How good is the fit? Residuals, weighted least squares and conditioning

**Residuals and the fit measure.** After fitting $\hat{y}_i = a + bx_i$, the residuals $r_i = y_i - \hat{y}_i$ always satisfy $\sum r_i = 0$ and $\sum x_i r_i = 0$ (the normal equations). Two summary numbers are used: the **sum of squared errors** $SSE = \sum r_i^{2}$ and the **coefficient of determination**

$$R^{2} = 1 - \frac{SSE}{SST},\qquad SST = \sum (y_i - \bar{y})^{2},$$

the fraction of the variation in $y$ explained by the fit ($R^{2} = 1$ is perfect). The standard error $s_e = \sqrt{SSE/(n-2)}$ for a straight line is a typical size of the residual in the units of $y$.

::: example The five-point line of Section 2.7
For the data (1, 2.1), (2, 3.9), (3, 6.2), (4, 7.8), (5, 10.1) the line is $y = 0.05 + 1.99x$. The residuals are +0.06, −0.13, +0.18, −0.21, +0.10 (sum 0), $SSE = 0.107$ and $SST = 39.708$, so $R^{2} = 0.9973$ and $s_e = \sqrt{0.107/3} = 0.189$. The fit explains 99.7 % of the variation, and a prediction is typically wrong by about 0.19.
:::

**Outliers.** Squaring the residuals gives a bad point a big vote. Replacing the last observation 10.1 by 5.0 changes the fitted line to $y = 2.09 + 0.97x$: the slope halves because of one point.

**Weighted least squares.** If observation $i$ is trusted with weight $w_i$, minimise $\sum w_i r_i^{2}$. The normal equations become $(A^{T}WA)\,c = A^{T}W y$ with $W = \operatorname{diag}(w_i)$. Giving the doubtful point weight 0.1 (others 1) turns the line above into $y = 0.57 + 1.73x$, which is again close to the trend of the other four points. Use weights $w_i = 1/\sigma_i^{2}$ when the measurement variances $\sigma_i^{2}$ are known.

**Conditioning of the normal equations.** For a polynomial fit of degree $m$ the matrix $A^{T}A$ of the normal equations is nearly singular once $m$ is more than four or five. For $x = 1, 2, \dots, 10$ the condition number of the design matrix $A$ and of $A^{T}A$ (the square, since cond$(A^{T}A) = $ cond$(A)^{2}$) are:

| Degree | cond($A$) | cond($A^{T}A$) |
|---|---|---|
| 1 | 14 | $1.9\times 10^{2}$ |
| 2 | $2.0\times 10^{2}$ | $4.1\times 10^{4}$ |
| 4 | $6.6\times 10^{4}$ | $4.4\times 10^{9}$ |
| 6 | $3.7\times 10^{7}$ | $1.4\times 10^{15}$ |

At degree 6 the normal equations hold no reliable digits in double precision. The cures are to centre and scale $x$ (use $t = (x - \bar{x})/s$), to solve the least-squares problem by **QR factorisation** (which works with $A$ itself, not $A^{T}A$), or to use **orthogonal polynomials** (Legendre, Chebyshev) for which $A^{T}A$ is diagonal. The Hilbert matrix, the normal-equation matrix of fitting by powers on $[0, 1]$, has condition number $4.8\times 10^{5}$ at size 5 and grows exponentially.

::: caution Do not fit a high degree just because you can
Degree $n - 1$ passes through all $n$ points ($R^{2} = 1$, zero residual) and says nothing about the next observation. Compare fits on data that were *not* used (a hold-out set) and choose the smallest degree whose residuals look like noise.
:::

## Formula and fact sheet

- Error: $f (x) - P_{n} (x) = \frac{f^{(n+1)} (\xi)}{(n + 1) !} \cdot \Pi (x - x_{i})$.
- Lagrange: $P (x) = \frac{\sum y_{i} \Pi_{j \neq i} (x - x_{j})}{(x_{i} - x_{j})}$.
- Newton divided differences: $P = f [x_{0}] + f$[x₀,x₁](x − x₀) + …
- Forward: $u = \frac{(x - x_{0})}{h}$, terms $\frac{u (u - 1) \ldots}{k}$! $\Delta^{k} y_{0}$. Backward: $u = \frac{(x - x_{n})}{h}$, terms $\frac{u (u + 1) \ldots}{k}$! $\nabla^{k} y_{n}$.
- Spline: continuity of $S ,\  S' ,\  S''$; natural ends $S'' = 0$; tridiagonal system for $M_{i}$.
- Line fit: $b = \frac{n \sum x y - \sum x \sum y}{n \sum x^{2} - \left( \sum x \right)^{2}} ,\  a = \frac{\sum y - b \sum x}{n}$.
- Neville: $P_{i,j} = \dfrac{(x - x_i)P_{i+1,j} - (x - x_j)P_{i,j-1}}{x_j - x_i}$; inverse interpolation swaps the roles of $x$ and $y$.
- Interpolation error $= \dfrac{f^{(n+1)}(\xi)}{(n+1)!}\prod (x - x_i)$; Chebyshev nodes $\cos\frac{(2k+1)\pi}{2(n+1)}$ minimise the product (max $= 2^{-n}$ on $[-1,1]$).
- Stirling (central): $y_0 + p\frac{\Delta y_{-1} + \Delta y_0}{2} + \frac{p^2}{2}\Delta^2 y_{-1} + \cdots$; one wrong entry $\varepsilon$ spreads as $\varepsilon(1, -3, 3, -1)$ in $\Delta^3$.
- Fit quality: $R^2 = 1 - SSE/SST$; weighted LS: $(A^TWA)c = A^TWy$; cond$(A^TA) = $ cond$(A)^2$.

## Chapter summary

- Through $n + 1$ points there is one polynomial of degree ≤ *n*; Lagrange, Newton divided-difference and Newton difference formulas all give it.
- The error depends on the (*n* + 1)th derivative and the product of distances to the nodes: interpolate near the centre and avoid very high degrees.
- Cubic splines give a smooth piecewise fit by solving a tridiagonal system.
- Least squares fits noisy data by minimising squared residuals; many non-linear models reduce to straight lines after a transformation.
- Neville's algorithm and inverse interpolation extend the Lagrange/Newton tools; node choice (Chebyshev) controls the error bound; central differences suit mid-table values and detect bad data; splines beat one high-degree polynomial; least-squares quality is judged by residuals and $R^2$, weights handle unequal trust and the normal equations become ill-conditioned for high degree.

## Practice

1. State the interpolation error formula and explain why it is smallest near the centre of the data.
2. Use Lagrange's formula with nodes 1, 2, 3, 4 and $\ln x$ to estimate $\ln 2.5$. Find the error.
3. Build the divided-difference table for the same data and confirm the value.
4. From the $10 ^{\circ}$ table of $\sin x$, estimate $\sin 5 ^{\circ}$ (forward) and $\sin 35 ^{\circ}$ (backward).
5. Why is the forward formula used near the beginning of a table and the backward near the end?
6. Find the natural cubic spline value at $x = 2.5$ for the points (1, 2), (2, 3), (3, 5), (4, 4).
7. Fit $y = a + b x$ to (1, 2.2), (2, 2.8), (3, 3.6), (4, 4.5), (5, 5.1). Predict *y* at $x = 6$.
8. Fit $y = A e^{B x}$ to (1, 2.7), (2, 4.0), (3, 6.1), (4, 9.2), (5, 13.5).
9. Distinguish interpolation from least-squares approximation.
10. What is Runge's phenomenon, and how do splines avoid it?
11. Use Neville's algorithm to estimate $\sqrt{5}$ from the nodes $x = 1, 4, 9$ ($y = 1, 2, 3$).
12. The table $x = 0, 0.1, 0.2, 0.3$ gives $y = 1.0000, 1.1052, 1.2214, 1.3499$ (values of $e^{x}$). Estimate the $x$ for which $y = 1.15$ by inverse Lagrange interpolation and compare with $\ln 1.15$.
13. Bound the error of linear interpolation of $\ln x$ between $x = 2$ and $x = 3$ at $x = 2.5$, and compare with the actual error.
14. Find the Chebyshev nodes of degree 2 (three nodes) on $[-1, 1]$ and on $[0, 4]$.
15. The values 3, 8, 15, 24, 38, 48, 63 are meant to be $x^{2} - 1$ for $x = 2, \dots, 8$. Locate the wrong entry with a difference table.
16. Estimate $e^{1.04}$ using only Stirling's terms up to $\Delta^{2}$ with the table of Section 2.11, and state the error.
17. Why can a natural cubic spline be less accurate than a clamped one near the ends?
18. For the data (1, 2.1), (2, 3.9), (3, 6.2), (4, 7.8), (5, 10.1) verify that the residuals of the least-squares line sum to zero and find $R^{2}$.
19. Explain why fitting a degree-9 polynomial through ten noisy points is a poor idea even though the fit error is zero.
20. A fit is made with weights 1, 1, 1, 1, 0.1 on the last point. Write the weighted normal equations for a line in terms of $\sum w$, $\sum wx$, $\sum wx^{2}$, $\sum wy$, $\sum wxy$.

::: note Answers and worked solutions
**1.** $f (x) - P_{n} (x) = \frac{f^{(n+1)} (\xi) (x - x_{0}) \ldots (x - x_{n})}{(n + 1) !}$. Near the middle the factors |x − $x_{i} \mid$ are smaller (some nodes lie on either side), whereas near the ends all distances are large, so the product and the error are bigger.

**2.** The weights at 2.5 are $- 0.0625 ,\  0.5625 ,\  0.5625 ,\  - 0.0625 ;\  P_{3} (2.5) = 0.921221$, true 0.916291, error 0.004931 (bound 0.140625).

**3.** The table in Section 2.4 gives coefficients 0.000000, 0.693147, -0.143841, 0.028317; evaluating at 2.5 gives 0.921221, the same as Lagrange.

**4.** Forward with $u = 0.5$: $\sin 5 ^{\circ} \approx 0.08711$ (true 0.08716). Backward with $u = - 0.5$: $\sin 35 ^{\circ} \approx 0.57358$ (true 0.57358).

**5.** Forward differences use the top row of the table, which has all its later columns available only if the point is near the start; near the end the top-row differences of high order don't exist or are poorly centred, while the bottom diagonal (backward differences) has them and reaches back from the end.

**6.** $M = (0.00000 ,\  2.80000 ,\  - 5.20000 ,\  0.00000) ,\  S (2.5) = 4.15000$ from the piece on [2, 3]: $3 + 1.93333 (0.5) + 1.4 (0.25) - 1.33333 (0.125) = 4.15000$.

**7.** $\sum x = 15 ,\  \sum y = 18.2 ,\  \sum x^{2} = 55 ,\  \sum x y = 62.1 ;\  b = 0.7500 ,\  a = 1.3900$; at $x = 6 ,\  y = 5.890$.

**8.** $\ln y$ values in Section $2.7 ;\  B = 0.4052 ,\  \ln A = 0.5864 ,\  A = 1.7975$: $y = 1.7975 e^{0.4052 x}$.

**9.** Interpolation reproduces the data points exactly and is suited to exact (or very accurate) data; least squares gives a smoother curve that need not pass through any point and is suited to noisy data.

**10.** For equally spaced nodes, a high-degree interpolating polynomial may oscillate wildly near the interval ends (for example $\frac{1}{(1 + 25 x^{2})}$). A spline uses low-degree cubic pieces, so a local change affects only nearby intervals and no big oscillations build up.

**11.** Nodes 1, 4, 9 with $y = 1, 2, 3$ and $x = 5$. $P_{1,2} = \dfrac{(5-1)(2) - (5-4)(1)}{4-1} = \dfrac{8 - 1}{3} = 2.3333$; $P_{2,3} = \dfrac{(5-4)(3) - (5-9)(2)}{9-4} = \dfrac{3 + 8}{5} = 2.2$; $P_{1,3} = \dfrac{(5-1)(2.2) - (5-9)(2.3333)}{9-1} = \dfrac{8.8 + 9.3333}{8} = \mathbf{2.2667}$. True $\sqrt{5} = 2.2361$ (error 0.031: three widely spaced nodes).

**12.** Interpolate $x$ against $y$ and evaluate at $y = 1.15$: $x = 0.139759$. Exact $\ln 1.15 = 0.139762$, error $3\times 10^{-6}$ (the table is narrow and monotone, so inverse interpolation works well).

**13.** $|E| \le \dfrac{|(x-2)(x-3)|}{2}\max|f''| = \dfrac{0.25}{2}\cdot\dfrac{1}{4} = 0.03125$ since $f'' = -1/x^{2}$ has maximum modulus $1/4$ on $[2, 3]$. The linear estimate is $(\ln 2 + \ln 3)/2 = 0.895880$ against $\ln 2.5 = 0.916291$: actual error 0.0204, inside the bound.

**14.** Degree 2 means three nodes $\cos\frac{(2k+1)\pi}{6}$: $+0.8660,\ 0,\ -0.8660$ on $[-1, 1]$. On $[0, 4]$ use $x = 2 + 2x_k$: $3.7321,\ 2,\ 0.2679$.

**15.** Second differences of $x^{2} - 1$ must be the constant 2. The table gives 2, 2, 5, −4, 5. The deviations from 2 are 0, 0, 3, −6, 3 = $3\times(1, -2, 1)$, centred on the fifth value in the list (that is $x = 6$): it was written as 38 instead of $6^{2} - 1 = 35$ (error $+3$).

**16.** Here $p = 0.4$ and $y_0 = 2.718282$. First-order term: $p\,\dfrac{\Delta y_{-1} + \Delta y_0}{2} = 0.4(0.272281) = 0.108913$. Second-order term: $\dfrac{p^{2}}{2}\Delta^{2}y_{-1} = 0.08(0.027205) = 0.002176$. Sum: $\mathbf{2.829371}$. True $e^{1.04} = 2.829217$, error $1.5\times 10^{-4}$; the omitted third-difference term is $\approx \dfrac{p(p^{2}-1)}{6}(0.002725) = -0.000153$, which is about the size of the error, so including it removes it.

**17.** The natural spline forces $S'' = 0$ at both ends whether or not the function has zero curvature there; the error is largest next to the ends where this wrong condition acts. The clamped spline uses the true end slopes and loses this error. If the true $f''$ is near zero at the ends (as for sine on $[0, \pi]$) the two are nearly equal (maximum errors 0.00107 and 0.00112).

**18.** The line is $y = 0.05 + 1.99x$. Fitted values: 2.04, 4.03, 6.02, 8.01, 10.00; residuals $+0.06, -0.13, +0.18, -0.21, +0.10$, which sum to 0. $SSE = 0.0036 + 0.0169 + 0.0324 + 0.0441 + 0.01 = 0.107$; $SST = \sum (y - 6.02)^{2} = 39.708$; $R^{2} = 1 - 0.107/39.708 = 0.9973$.

**19.** Nine degrees of freedom for ten points means zero residual at the data, but the polynomial then has to wiggle through the noise (Runge-type oscillation between and beyond the points) and the monomial normal equations are badly conditioned. The model memorises the noise (over-fitting) and predicts new points poorly. Use a low degree or a spline, and check on held-out data.

**20.** With $W = \operatorname{diag}(1, 1, 1, 1, 0.1)$: $\left(\sum w\right) a + \left(\sum wx\right) b = \sum wy$ and $\left(\sum wx\right) a + \left(\sum wx^{2}\right) b = \sum wxy$, where $\sum w = 4.1$ and the last point enters every sum with one tenth of its usual size.

:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Using Newton's divided-difference formula, estimate $\ln 3$ from $\ln 1 ,\  \ln 2 ,\  \ln 4$ and $\ln 6$. Estimate the error.**

*Data.* $x = 1 ,\  2 ,\  4 ,\  6 ;\  f = 0 ,\  0.69315 ,\  1.38629 ,\  1.79176$.

| *x* | *f* | 1st | 2nd | 3rd |
|---|---|---|---|---|
| 1 | 0.00000 |  |  |  |
|  |  | 0.69315 |  |  |
| 2 | 0.69315 |  | -0.11552 |  |
|  |  | 0.34657 |  | 0.01591 |
| 4 | 1.38629 |  | -0.03596 |  |
|  |  | 0.20273 |  |  |
| 6 | 1.79176 |  |  |  |

*Newton form.* $P (x) = 0 + 0.69315 (x - 1) - 0.11552 (x - 1) (x - 2) + 0.01591 (x - 1) (x - 2) (x - 4)$ (Figure 2.2). At $x = 3$: $0.69315 (2) - 0.11552 (2) (1) + 0.01591 (2) (1) (- 1) = 1.38630 - 0.23104 - 0.03182$ = **1.12344** (about 1.1234). The true $\ln 3 = 1.09861$, so the actual error is 0.0248.

*Error formula.* $f (x) - P (x) = \frac{f'''' (x i)}{4 !} x (x - 1) (x - 2) (x - 4) (x - 6)$. Here $f'''' = - \frac{6}{x^{4}}$ and the product at 3 is 2 $x 1 x (- 1) x (- 3) = 6$, so the error magnitude is $\left( \frac{6}{x i^{4}} \right) \left( \frac{6}{24} \right) = \frac{1.5}{x i^{4}}$; the observed 0.0248 corresponds to xi = 2.79, inside [1, 6], as the theory requires. *Conclusion:* the estimate is accurate to about two decimals; a closer, centred set of points would be better.

**Q2 (5 marks). Fit a straight line $y = a + b x$ by least squares to (1, 2.1), (2, 3.9), (3, 6.2), (4, 7.8), (5, 10.1) and predict *y* at $x = 6$.**

*Normal equations.* Sum $y = n a + b$ sum *x*; sum $x y = a$ sum $x + b$ sum $x^{2}$.

| *x* | *y* | $x^{2}$ | $x y$ |
|---|---|---|---|
| 1 | 2.1 | 1 | 2.1 |
| 2 | 3.9 | 4 | 7.8 |
| 3 | 6.2 | 9 | 18.6 |
| 4 | 7.8 | 16 | 31.2 |
| 5 | 10.1 | 25 | 50.5 |
| **15** | **30.1** | **55** | **110.2** |

$b = \frac{n \sum x y - \sum x \sum y}{n \sum x^{2} - \left( \sum x \right)^{2}} = \frac{5 x 110.2 - 15 x 30.1}{5 x 55 - 225} = \frac{551 - 451.5}{50}$ = **1.99**. $a = \frac{30.1 - 1.99 x 15}{5}$ = **0.05**. The line is **$y = 0.05$ + 1.99x** (Figure 2.4). At $x = 6$: $y = 0.05 + 11.94$ = **11.99**. The residuals are 0.06, -0.13, 0.18, -0.21, 0.10, so the sum of squares is 0.107. *Conclusion:* the very small S shows a strong linear trend, and the prediction one step outside the data is acceptable because it is an extrapolation of only one unit.

**Q3 (10 marks). Explain polynomial interpolation. Derive the Lagrange and Newton forms, discuss the error and Runge's phenomenon, and compare interpolation with least-squares approximation.**

*Introduction.* Given $n + 1$ distinct points (x0, y0) $\ldots (x n ,\  y n)$, **interpolation** finds a function that passes through every point and uses it to estimate values between them. There is exactly **one polynomial of degree at most *n*** through the points, so the Lagrange and Newton forms are the same polynomial written differently (Plate 2.1 names the founders).

*Lagrange form.* $P (x)$ = sum of yi Li(x), where Li(x) = product over *j* not equal *i* of (*x* - xj)/(xi - xj) equals 1 at xi and 0 at other nodes. It is simple to write, but adding a point means recomputing every term.

*Newton form.* $P(x) = f[x_{0}] + f[x_{0}, x_{1}](x - x_{0}) + f[x_{0}, x_{1}, x_{2}](x - x_{0})(x - x_{1}) + \cdots$, where the coefficients are divided differences made by the table of Figure 2.2. A new point adds one new term, so the work already done is kept. For equally spaced data the divided differences become forward or backward differences and the Gregory-Newton formulas are used.

*Error.* $f(x) - P(x) = \frac{f^{(n+1)}(\xi)}{(n+1)!}\,(x - x_{0})(x - x_{1})\cdots(x - x_{n})$. The product is small near the middle of the data and large near the ends, so interpolate near the centre. In Figure 2.1 the cubic through four points of $\ln x$ has error 0.0248 at $x = 3$ and 0.0322 at $x = 5$.

*Runge's phenomenon.* Raising the degree with equally spaced nodes does not always improve accuracy: for $\frac{1}{(1 + 25 x^{2})}$ the degree-10 interpolant oscillates wildly near the ends (Figure 2.3). Remedies are low-degree piecewise polynomials such as **cubic splines** (continuous first and second derivatives) or Chebyshev-spaced nodes.

*Least squares.* When data are noisy, passing through every point is wrong. Least squares chooses the curve minimising the sum of squared residuals; for a line, $b = \frac{n \sum x y - \sum x \sum y}{n \sum x^{2} - \left( \sum x \right)^{2}}$ (Figure 2.4).

| Point | Interpolation | Least-squares fit |
|---|---|---|
| Passes through data | Exactly | Not required |
| Suitable for | Exact tables, noise-free values | Noisy measurements |
| Degree | Rises with number of points | Chosen by the user (low) |
| Risk | Oscillation (Runge) | Underfit if model poor |
| Typical use | Table look-up, graphics | Trend lines, calibration |

*Conclusion.* Use interpolation for accurate tabulated values within the range, using Newton's form for convenience and splines for many points; use least squares for measurement data. Extrapolation is less reliable than interpolation in both cases.

**Q4 (5 marks). Use Neville's algorithm to estimate $\cos 0.8$ from the values of $\cos x$ at $x = 0, 0.5, 1.0, 1.5$. State the error.**

*Formula.* $P_{i,j}(x) = \dfrac{(x - x_i)P_{i+1,j} - (x - x_j)P_{i,j-1}}{x_j - x_i}$ with $P_{i,i} = y_i$.

| $x_i$ | $P_{i,i}$ | $P_{i,i+1}$ | $P_{i,i+2}$ | $P_{i,i+3}$ |
|---|---|---|---|---|
| 0.0 | 1.000000 | 0.804132 | 0.700998 | 0.695713 |
| 0.5 | 0.877583 | 0.675214 | 0.691089 | |
| 1.0 | 0.540302 | 0.728128 | | |
| 1.5 | 0.070737 | | | |

*Result.* $\cos 0.8 \approx 0.695713$; true 0.696707, error $9.9\times 10^{-4}$. *Check by bound:* $\dfrac{|f^{(4)}|}{4!}|w(0.8)|$ with $|f^{(4)}| \le 1$ and $w(0.8) = (0.8)(0.3)(-0.2)(-0.7) = 0.0336$ gives $\le 0.0014$, consistent with the actual error. *Conclusion:* the cubic through four nodes gives three decimals.
