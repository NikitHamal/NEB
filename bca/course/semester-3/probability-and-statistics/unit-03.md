---
subject: Probability and Statistics
grade: BCA Semester 3
unit: 3
title: Correlation and Regression Analysis
hours: 6
area: BCA 205 · Probability and Statistics · Unit 3
---

Do students who study more score more? Does server load rise with users? **Correlation** measures the strength and direction of a linear relationship between two variables; **regression** gives an equation to predict one from the other.

::: key What this unit gives you
- Scatter diagrams and Karl Pearson's correlation coefficient *r*.
- Regression lines by the least squares method; prediction.
- Worked numerical problems.
:::

## 3.1 Correlation

Two variables are **correlated** if they change together: **positive** (both rise: study hours and marks), **negative** (one rises as the other falls: price and demand), or **zero/no correlation**. **Correlation is not causation:** ice-cream sales and drowning both rise in summer without either causing the other.

**Scatter diagram:** plot each pair $(x ,\  y)$ as a point. Points rising from lower left to upper right indicate positive correlation, falling points negative, a shapeless cloud none; points close to a straight line indicate strong linear correlation.

**Karl Pearson's coefficient of correlation** *r* = Cov(x, y)/(σₓσᵧ) = Σ(x − x̄)(y − ȳ)/√[Σ(x − x̄)² · Σ(y − ȳ)²]. Computational form:

$$r = \frac{n \sum x y - \sum x \sum y}{\sqrt{\{\left[ n \sum x^{2} - \left( \sum x \right)^{2} \right] \left[ n \sum y^{2} - \left( \sum y \right)^{2} \right]\}}}$$

Properties: **$- 1 \leq r \leq + 1$**; $r = + 1$ perfect positive, −1 perfect negative, 0 no *linear* correlation; *r* is unchanged by a change of origin or positive scale; *r* has no units. Rough interpretation: $|r| < 0.3$ weak, 0.3–0.7 moderate, > 0.7 strong. The **coefficient of determination** $r^{2}$ is the proportion of variation in *y* explained by *x*. **Spearman's rank correlation** for ordered data is $r_{s} = 1 - \frac{6 \sum d^{2}}{n (n^{2} - 1)}$.

::: example Worked example: study hours and marks
*x* (hours per day): 1, 2, 3, 4, 5. *y* (marks out of 10): 2, 4, 5, 4, 5. $n = 5 ,\  \bar{x} = 3$, ȳ = 4.

$\sum (x - \bar{x})^{2} = 4 + 1 + 0 + 1 + 4$ = **10**; Σ(y − ȳ)² = 4 + 0 + 1 + 0 + 1 = **6**; $\sum (x - \bar{x}) ( y$ − ȳ) = $(- 2) (- 2) + (- 1) (0)$ + 0·1 + $(1) (0) + (2) (1) = 4 + 0 + 0 + 0 + 2$ = **6**.

$r = \frac{6}{\sqrt{10 \times 6}} = \frac{6}{\sqrt{60}}$ = **0.7746**: strong positive correlation. $r^{2}$ = **0.60**: 60% of the variation in marks is associated with study hours.
:::

## 3.2 Regression analysis

**Regression** finds the **line of best fit** used to estimate the **dependent** variable (*y*, the response) from the **independent** variable (*x*, the predictor). The **least squares method** chooses the line $y = a + b x$ that minimises Σ(y − ŷ)², the sum of squared vertical errors. Setting derivatives to zero gives the **normal equations**:

$$\sum y = n a + b \sum x$$

$$\sum x y = a \sum x + b \sum x^{2}$$

Solution: ***b* = Sxy/Sxx = $\frac{n \sum x y - \sum x \sum y}{n \sum x^{2} - \left( \sum x \right)^{2}}$**, **a = ȳ − $b \bar{x}$**. The slope *b* is the **regression coefficient of *y* on *x*** $(b_{y} x)$: the change in *y* per unit *x*. If we regress *x* on *y* we get a different line, $x = a' + b' y$, with **$b_{x} y$ = Sxy/Syy**. The two lines intersect at ($\bar{x}$, ȳ), and **$r^{2} = b_{y} x \times b_{x} y$** (*r* takes the sign of the b's). If $r = \pm 1$ the two lines coincide; if $r = 0$ they are perpendicular (horizontal and vertical).

::: example Worked example: regression for the same data
$b_{y} x$ = Sxy/Sxx = $\frac{6}{10}$ = **0.6**; $a = 4 - 0.6 \times 3$ = **2.2**. Regression line of *y* on *x*: **ŷ = 2.2 + 0.6x**. Prediction: study 6 hours → ŷ = $2.2 + 3.6$ = **5.8** marks (interpolation is safer than extrapolating far outside the observed range of 1–5 hours).

$b_{x} y$ = Sxy/Syy = $\frac{6}{6}$ = **1.0**; *x* on *y*: x̂ = $3 + 1.0 (y - 4) = y - 1$. Check: $r^{2} = 0.6 \times 1.0 = 0.6$, so $r = \sqrt{0.6} = 0.7746$ ✓. Both lines pass through (3, 4).

The residual at $x = 2$: ŷ = 3.4, actual 4, error 0.6. The residuals sum to zero.
:::

**Dependent and independent variables:** choose which to predict *before* fitting; the y-on-x line minimises vertical errors, and is wrong for predicting *x* from *y*. **Assumptions:** linear relationship, errors independent with roughly constant variance, no influential outliers. **Using software:** Excel `=CORREL(x,y)`, `=SLOPE(y,x)`, `=INTERCEPT(y,x)`; SPSS *Analyze → Correlate / Regression*; Python `numpy.polyfit`.

## 3.3 Seeing correlation and regression

```svgfig label="3.1" caption="Three scatter diagrams of 12 points each. (a) The points hug a rising line: $r = + 0.98$, very strong positive correlation. (b) A shapeless cloud: $r = - 0.19$, practically no linear correlation. (c) The points hug a falling line: $r = - 0.96$, very strong negative correlation. The sign of *r* gives the direction and its size gives the tightness."
f = Fig(580, 205)
X = [1.0, 1.7, 2.5, 3.2, 3.9, 4.6, 5.4, 6.1, 6.8, 7.5, 8.3, 9.0]
sets = [("(a) r = +0.98", [1.0, 2.0, 2.3, 2.4, 3.5, 3.7, 5.5, 7.3, 6.4, 6.9, 8.7, 9.3], TEAL),
        ("(b) r = −0.19", [1.3, 5.1, 4.7, 8.3, 6.0, 5.1, 5.0, 3.0, 1.1, 2.5, 6.5, 2.6], AMBER),
        ("(c) r = −0.96", [9.1, 7.4, 7.5, 7.5, 4.8, 4.9, 2.7, 2.6, 1.4, 2.3, 0.5, 1.3], RED)]
for k, (t, Y, c) in enumerate(sets):
    ax = Axes(f, 14 + k * 192, 30, 168, 140, (0, 10), (0, 10))
    ax.grid(2, 2, labels=False); ax.axes("x", "y")
    for a, b in zip(X, Y):
        ax.pt(a, b, "", r=3.8, color=c)
    f.text(98 + k * 192, 16, t, size=11.5, color=NAVY, bold=True)
f.text(290, 196, "Correlation describes association only: a high r never proves that x causes y.", size=10.5, color=SLATE, italic=True)
```

```photogrid label="3.1" cols="2" ratio="1.0" caption="Karl Pearson and the line of best fit. (a) Karl Pearson (1857-1936) defined the product-moment correlation coefficient used in this unit. (b) The least-squares line ŷ = 2.2 + 0.6x for the study-hours data; the dashed segments are the residuals, and the line is chosen so that the sum of their squares is as small as possible."
@ photo id="bca205/pearson" cap="Karl Pearson, English statistician"
fit 1.0
focus 0.5 0.4
@ svg cap="Least squares: residuals of the worked example"
f = Fig(300, 300)
ax = Axes(f, 42, 12, 245, 235, (0, 6.5), (0, 7))
ax.grid(1, 1); ax.axes("hours", "marks")
ax.curve(lambda x: 2.2 + 0.6 * x, 0.4, 6.2, color=NAVY, sw=2.6)
for a, b in zip([1, 2, 3, 4, 5], [2, 4, 5, 4, 5]):
    f.line(ax.X(a), ax.Y(b), ax.X(a), ax.Y(2.2 + 0.6 * a), color=RED, sw=1.6, dash=True)
    ax.pt(a, b, "", r=4.2, color=RED)
f.text(ax.X(3.6), ax.Y(1.0), "ŷ = 2.2 + 0.6x", size=13, color=NAVY, bold=True)
f.text(ax.X(1.3), ax.Y(6.4), "r = 0.775", size=13, color=SLATE, bold=True)
```

```svgfig label="3.2" caption="Two regression lines for the same data. The line of *y* on *x* (navy, slope $b_{y} x = 0.6$) minimises vertical errors; the line of *x* on *y* (red, equivalent to $y = x + 1$, slope $\frac{1}{b_{x} y} = 1$) minimises horizontal errors. They cross at the mean point (3, 4); the product of the two regression coefficients is $0.6 \times 1.0 = 0.6 = r^{2}$."
f = Fig(580, 215)
ax = Axes(f, 50, 14, 300, 175, (0, 7), (0, 7))
ax.grid(1, 1); ax.axes("x (hours)", "y (marks)")
ax.curve(lambda x: 2.2 + 0.6 * x, 0, 7, color=NAVY, sw=2.4)
ax.curve(lambda x: x + 1, 0, 6, color=RED, sw=2.4)
for a, b in zip([1, 2, 3, 4, 5], [2, 4, 5, 4, 5]):
    ax.pt(a, b, "", r=3.8, color=TEAL)
ax.pt(3, 4, "(x̄, ȳ) = (3, 4)", r=5.5, color=AMBER, dx=10, dy=18)
f.text(372, 40, "y on x:  ŷ = 2.2 + 0.6x", size=11.5, color=NAVY, bold=True, anchor="start")
f.text(372, 62, "x on y:  x̂ = y − 1", size=11.5, color=RED, bold=True, anchor="start")
f.text(372, 96, "b_yx × b_xy = r²", size=11.5, color=SLATE, anchor="start", bold=True)
f.text(372, 116, "0.6 × 1.0 = 0.6", size=11.5, color=SLATE, anchor="start")
f.text(372, 150, "r = 0 → lines perpendicular", size=10.5, color=SLATE, anchor="start", italic=True)
f.text(372, 168, "|r| = 1 → one single line", size=10.5, color=SLATE, anchor="start", italic=True)
```

## 3.4 Eight uses of correlation and regression

1. **Predicting a number from another.** A simple regression can estimate a student's final mark from internal marks. The line gives a quick, honest estimate with a known error. A college can then warn students who are likely to fail early.
2. **Forecasting demand and sales.** Shops link sales to price, festival season or rainfall. Before Dashain, a Kathmandu electronics shop fits a line of past sales on advertising spend to plan stock. Better forecasts reduce both lost sales and unsold goods.
3. **Machine learning baseline.** Linear regression is the first model every data scientist tries. It is fast, easy to explain and a yardstick for complex models. Slope and intercept show directly which factor matters.
4. **Finding related features.** Correlation between columns of a data set shows duplicated information. If two sensors have $r = 0.99$, one can be dropped to save storage. Analysts also use *r* to pick features that relate to the target.
5. **Performance modelling in computing.** Run time often grows with input size, and regression estimates by how much. A developer fits time against file size to predict when a script will become too slow. Server planners do the same with traffic and CPU load.
6. **Economics and public policy.** Economists relate income to spending, and rainfall to paddy yield. Nepal Rastra Bank studies relationships such as remittance and consumption this way. Policy makers still remember that correlation alone does not prove cause.
7. **Health and agriculture.** Doctors relate dose to response, and farmers relate fertiliser to yield. The slope tells how much extra yield one more kilogram of fertiliser gives. The $r^{2}$ value shows how much of the yield variation fertiliser explains.
8. **Quality checks of other methods.** Calibration of a cheap instrument against an accurate one uses a regression line. An *r* close to 1 shows the cheap instrument is trustworthy. The residuals reveal where it fails.

```photogrid label="3.2" cols="2" ratio="1.2" caption="Regression began with fathers and sons. (a) Sir Francis Galton, who in the 1880s measured the heights of parents and children and noticed that tall fathers $h a d$ sons who were tall, but on average not as tall: heights regress towards the mean. (b) A simulation of 1,000 father-son pairs with mean height 170 cm, standard deviation 6 cm and a true correlation of 0.5 (random seed 2081). The least-squares line has slope 0.54 and the sample correlation is $r = 0.53$. A slope below 1 is the regression effect: the dashed line $y = x$ is where sons would be as tall as their fathers, and the fitted line is flatter. For a 180 cm father the line predicts a son of 175.6 cm, not 180 cm."
@ photo id="bcamath/galton" cap="Sir Francis Galton (regression, correlation)"
fit 1.2
focus 0.5 0.4
@ svg cap="Regression to the mean in 1,000 simulated pairs"
import numpy as np
rng = np.random.default_rng(2081); fa = rng.normal(170, 6, 1000); so = 170 + 0.5 * (fa - 170) + rng.normal(0, 6 * (0.75 ** 0.5), 1000)
r = np.corrcoef(fa, so)[0, 1]; b, a = np.polyfit(fa, so, 1)
assert round(r, 2) == 0.53 and round(b, 2) == 0.54 and round(a + b * 180, 1) == 175.6 and b < 1
f = Fig(300, 240)
X = lambda v: 34 + (v - 150) / 40 * 240; Y = lambda v: 196 - (v - 150) / 40 * 170
f.line(34, 196, 274, 196, color=SLATE, sw=1.2); f.line(34, 196, 34, 26, color=SLATE, sw=1.2)
for t in (150, 160, 170, 180, 190):
    f.text(X(t), 210, str(t), size=10.5, color=SLATE)
for i in range(220):
    if 150 <= fa[i] <= 190 and 150 <= so[i] <= 190: f.circle(X(fa[i]), Y(so[i]), 2.2, fill="#93c5fd", stroke="#3b82f6", sw=0.6)
f.line(X(150), Y(150), X(190), Y(190), color=SLATE, sw=1.4, dash=True)
f.line(X(150), Y(a + b * 150), X(190), Y(a + b * 190), color=AMBER, sw=2.4)
f.circle(X(180), Y(a + b * 180), 4.5, fill=RED, stroke=RED)
f.text(X(180) + 8, Y(a + b * 180) + 18, "175.6", size=10.5, color=RED, bold=True, anchor="start")
f.text(40, 22, "son (cm)", size=10.5, color=SLATE, anchor="start")
f.text(150, 230, "father (cm); r = 0.53, slope 0.54 (dashed: y = x)", size=10.5, color=NAVY, bold=True)
```

```photogrid label="3.3" cols="2" ratio="1.2" caption="Correlation is not causation. (a) An ice-cream seller on a beach. (b) A simulation of 60 hot and cool days (seed 2081): temperature drives ice-cream sales $(r = 0.84)$ and, because more people swim, also the number of drownings $(r = 0.62)$. Ice-cream sales and drownings are therefore correlated too, $r = 0.46$, although neither causes the other. When temperature is held fixed, the partial correlation of ice cream with drownings is ($0.46 - 0.84 x$ 0.62) / sqrt((1 - $0.84^{2} ) (1 - 0.62^{2}) ) = - 0.16$, close to zero. A hidden common cause (a confounder) can create a correlation; before you claim that one thing causes another you need an experiment or a control for the confounder."
@ photo id="bcamath/icecream" cap="An ice-cream cart on the beach"
fit 1.2
focus 0.5 0.5
@ svg cap="A confounder creates a correlation"
import numpy as np
rng = np.random.default_rng(2081); T = rng.uniform(15, 38, 60); ice = 20 + 3 * T + rng.normal(0, 12, 60); dr = 0.1 * T + rng.normal(0, 0.9, 60)
r = lambda a, b: np.corrcoef(a, b)[0, 1]
r1, r2, r12 = r(T, ice), r(T, dr), r(ice, dr)
part = (r12 - r1 * r2) / ((1 - r1 ** 2) * (1 - r2 ** 2)) ** 0.5
assert (round(r1, 2), round(r2, 2), round(r12, 2), round(part, 2)) == (0.84, 0.62, 0.46, -0.16)
f = Fig(300, 240)
f.box(95, 14, 110, 30, "Temperature", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(8, 130, 120, 30, "Ice-cream sales", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(190, 130, 100, 30, "Drownings", fill=ROSE, stroke=RED, size=11, bold=True)
f.arrow([(120, 44), (68, 130)], color=AMBER, sw=2); f.arrow([(180, 44), (240, 130)], color=AMBER, sw=2)
f.line(128, 145, 190, 145, color=RED, sw=2, dash=True)
f.box(70, 66, 40, 20, "0.84", fill=SOFT, stroke=AMBER, size=10.5, bold=True, r=3)
f.box(190, 66, 40, 20, "0.62", fill=SOFT, stroke=AMBER, size=10.5, bold=True, r=3)
f.box(139, 135, 40, 20, "0.46", fill=SOFT, stroke=RED, size=10.5, bold=True, r=3)
f.text(150, 190, "partial r (ice cream, drownings | temperature) = -0.16", size=10.5, color=NAVY, bold=True)
f.text(150, 212, "dashed link is only a confounder effect", size=10.5, color=RED, bold=True)
f.text(150, 230, "60 simulated days", size=10.5, color=SLATE)
```

## 3.5 How good is the fit: $r^2$, standard error of estimate and probable error

Fitting a line is easy; judging it is the real skill. Four tools do this.

**Coefficient of determination.** $r^2$ is the fraction of the variation in *y* explained by the regression on *x*. Write the total variation as $SS_T = \sum (y - \bar{y})^2$, the unexplained part as $SS_E = \sum (y - \hat{y})^2$ (the squared residuals), then $r^2 = 1 - \frac{SS_E}{SS_T}$. If $r = 0.8$ then $r^2 = 0.64$: 64% of the variation in *y* is explained, 36% is not.

**Standard error of estimate.** It is the typical size of a residual: $s_e = \sqrt{\frac{SS_E}{n - 2}}$. (Some books divide by *n* and get $\sigma_y\sqrt{1 - r^2}$; use *n* − 2 when generalising from a sample.) A prediction is then roughly $\hat{y} \pm 2 s_e$ for about 95% of cases.

**Probable error of *r*.** $\mathrm{PE} = 0.6745 \times \frac{1 - r^2}{\sqrt{n}}$. Old rule of thumb: if $|r| < \mathrm{PE}$ there is no evidence of correlation; if $|r| > 6\,\mathrm{PE}$ it is certainly significant. Modern practice uses the *t* test below, but the PE appears in the TU syllabus questions.

**Test of *r*.** For the null hypothesis of no correlation, $t = \frac{r\sqrt{n - 2}}{\sqrt{1 - r^2}}$ with $n - 2$ degrees of freedom. A significant *r* is not a causal link.

::: example Worked example: hours studied and marks
Seven students: hours studied *x* = 2, 3, 4, 5, 6, 7, 8 and marks *y* = 45, 50, 58, 60, 68, 72, 80. Here $\bar{x} = 5$, $\bar{y} = 61.86$, $S_{xx} = 28$, $S_{xy} = 159$ and $SS_T = 912.86$.

Slope $b = \frac{159}{28} = 5.679$ and intercept $a = 61.857 - 5.679(5) = 33.464$, so $\hat{y} = 33.46 + 5.679x$. Correlation $r = \frac{159}{\sqrt{28 \times 912.86}} = 0.9945$ and $r^2 = $ **0.9891**.

| *x* | *y* | $\hat{y}$ | residual $y - \hat{y}$ |
|---|---|---|---|
| 2 | 45 | 44.82 | 0.18 |
| 3 | 50 | 50.50 | −0.50 |
| 4 | 58 | 56.18 | 1.82 |
| 5 | 60 | 61.86 | −1.86 |
| 6 | 68 | 67.54 | 0.46 |
| 7 | 72 | 73.21 | −1.21 |
| 8 | 80 | 78.89 | 1.11 |

$SS_E = 9.964$, so $s_e = \sqrt{\frac{9.964}{5}} = $ **1.41 marks**. A student studying 6.5 hours is predicted to score $33.46 + 5.679(6.5) = 70.4$, give or take about 2.8 marks (2$s_e$). The *t* statistic is $\frac{0.9945\sqrt{5}}{\sqrt{1 - 0.9891}} = 21.3$, far above the critical value 2.571 for 5 d.f. at the 5% level, so the correlation is significant. **Extrapolation warning:** the line says 9 hours gives 84.6, but nothing in the data covers 9 hours, so that figure is a guess.
:::

::: example Worked example: probable error
$r = 0.8$ from $n = 25$ pairs: $\mathrm{PE} = 0.6745 \times \frac{1 - 0.64}{\sqrt{25}} = 0.6745 \times \frac{0.36}{5} = 0.0486$. Since $\frac{r}{\mathrm{PE}} = 16.5 > 6$, the correlation is significant by the old rule.
:::

```svgfig label="3.3" caption="The fitted line for the hours-and-marks data with the residuals drawn as vertical segments. The segments are all short, which is what r squared = 0.989 and s_e = 1.41 mean."
f = Fig(580, 230)
ax = Axes(f, 60, 14, 470, 165, (1, 9), (40, 90))
ax.grid(1, 10, labels=True); ax.axes("hours studied", "marks")
ax.curve(lambda t: 33.464 + 5.6786 * t, 1.5, 8.5, color=NAVY, sw=2.2)
for xv, yv in zip([2, 3, 4, 5, 6, 7, 8], [45, 50, 58, 60, 68, 72, 80]):
    yh = 33.464 + 5.6786 * xv
    f.line(ax.X(xv), ax.Y(yh), ax.X(xv), ax.Y(yv), color=RED, sw=2)
    ax.pt(xv, yv, "", r=4.2, color=NAVY)
f.text(ax.X(2.1) + 6, ax.Y(78), "y-hat = 33.46 + 5.679 x", size=10.5, color=NAVY, bold=True, anchor="start")
f.text(ax.X(2.1) + 6, ax.Y(73), "red = residual (y - y-hat)", size=10.5, color=RED, bold=True, anchor="start")
f.text(290, 224, "r = 0.9945   r squared = 0.989   s_e = 1.41", size=10.5, color=SLATE, italic=True)
```

## 3.6 Partial and multiple correlation, and a warning about pooled data

Often more than two variables are involved. Let 1 = marks, 2 = hours studied and 3 = attendance. Attendance affects both hours and marks, so the simple $r_{12}$ may overstate the direct link between hours and marks.

**Partial correlation** removes the effect of a third variable: $r_{12.3} = \frac{r_{12} - r_{13} r_{23}}{\sqrt{(1 - r_{13}^2)(1 - r_{23}^2)}}$. It reads: the correlation between 1 and 2 when 3 is held fixed.

**Multiple correlation** measures how well variables 2 and 3 *together* predict 1: $R_{1.23}^2 = \frac{r_{12}^2 + r_{13}^2 - 2 r_{12} r_{13} r_{23}}{1 - r_{23}^2}$, and always $R_{1.23} \geq |r_{12}|$ and $\geq |r_{13}|$. The regression equation of $X_1$ on $X_2$ and $X_3$ is $X_1 = a + b_{12.3} X_2 + b_{13.2} X_3$; it is fitted by the normal equations or software (Excel LINEST, Python `numpy.linalg.lstsq`).

::: example Worked example: three variables
Given $r_{12} = 0.8$, $r_{13} = 0.7$ and $r_{23} = 0.6$:

$r_{12.3} = \frac{0.8 - 0.7 \times 0.6}{\sqrt{(1 - 0.49)(1 - 0.36)}} = \frac{0.38}{\sqrt{0.51 \times 0.64}} = \frac{0.38}{0.5713} = $ **0.665**.

$r_{13.2} = \frac{0.7 - 0.8 \times 0.6}{\sqrt{(1 - 0.64)(1 - 0.36)}} = \frac{0.22}{0.48} = $ **0.458**.

$R_{1.23}^2 = \frac{0.64 + 0.49 - 2(0.8)(0.7)(0.6)}{1 - 0.36} = \frac{0.458}{0.64} = 0.7156$, so $R_{1.23} = $ **0.846**.

Hours alone explain $r_{12}^2 = 64\%$ of the variation in marks; hours and attendance together explain 71.6%. Once attendance is held fixed, the hours-marks link falls from 0.80 to 0.665, which tells us part of the original correlation came through attendance.
:::

**Simpson's paradox.** A trend present in every sub-group can reverse when the groups are pooled, because the groups have different sizes. This is why one must look at the structure of the data before reporting a single correlation or percentage.

::: example Worked example: two debugging tools
Tool A and tool B were each used on 110 bugs, split into easy and hard ones.

| | Easy bugs fixed | Hard bugs fixed | Overall |
|---|---|---|---|
| Tool A | 8 of 10 (80%) | 30 of 100 (30%) | 38 of 110 (**34.5%**) |
| Tool B | 70 of 100 (70%) | 2 of 10 (20%) | 72 of 110 (**65.5%**) |

Tool A is better on easy bugs *and* on hard bugs, yet its overall rate is far lower, because A was given mostly hard bugs and B mostly easy ones. Comparing the overall figures says B is the better tool; comparing like with like says A is. The lurking variable here is bug difficulty.
:::

## Formula and fact sheet

- $r = \frac{\mathrm{Sxy}}{\sqrt{\mathrm{Sxx} \cdot \mathrm{Syy}}} ;\  - 1 \leq r \leq 1 ;\  r^{2}$ = proportion explained.
- Least squares: *b* = Sxy/Sxx, a = ȳ − $b \bar{x}$; ŷ = $a + b x$; lines meet at ($\bar{x}$, ȳ).
- $b_{y} x \times b_{x} y = r^{2}$. Spearman $r_{s} = 1 - \frac{6 \sum d^{2}}{n (n^{2} - 1)}$.
- $r^2 = 1 - \frac{SS_E}{SS_T}$; $s_e = \sqrt{\frac{SS_E}{n - 2}}$; $\mathrm{PE} = 0.6745\frac{1 - r^2}{\sqrt{n}}$; $t = \frac{r\sqrt{n - 2}}{\sqrt{1 - r^2}}$.
- $r_{12.3} = \frac{r_{12} - r_{13} r_{23}}{\sqrt{(1 - r_{13}^2)(1 - r_{23}^2)}}$; $R_{1.23}^2 = \frac{r_{12}^2 + r_{13}^2 - 2 r_{12} r_{13} r_{23}}{1 - r_{23}^2}$.

## Chapter summary

- Correlation measures linear association with *r* from −1 to +1; correlation does not prove causation.
- Least squares regression gives the best-fitting line for predicting *y* from *x*; the two regression lines meet at the means and their slopes multiply to $r^{2}$.
- $r^2$, the standard error of estimate and the probable error judge a fitted line; partial and multiple correlation handle a third variable; pooled data can mislead (Simpson's paradox).

## Practice

1. Differentiate correlation and regression.
2. For $x = 2 ,\  4 ,\  6$, 8 and $y = 3 ,\  7 ,\  5$, 10 compute *r* and the regression line of *y* on *x*; predict *y* for $x = 10$.
3. Interpret $r = - 0.85$ and $r = 0.1$.
4. If $b_{y} x = 0.8$ and $b_{x} y = 0.45$, find *r*.
5. Why must the regression line of *y* on *x* not be used to predict *x*?
6. State three properties of *r*.
7. For $r = 0.6$ from $n = 36$ pairs compute $r^2$, the probable error, and decide if $r$ is significant by the PE rule.
8. If $\sigma_y = 10$ and $r = 0.8$ find the standard error of estimate using $\sigma_y\sqrt{1 - r^2}$.
9. Given $r_{12} = 0.6$, $r_{13} = 0.5$ and $r_{23} = 0.4$, find $r_{12.3}$ and $R_{1.23}$.
10. Using the line $\hat{y} = 33.46 + 5.679x$ of section 3.5, predict the marks for 4.5 hours of study, and say why a prediction for 12 hours is unreliable.
11. Tool A fixes 8 of 10 easy and 30 of 100 hard bugs; tool B fixes 70 of 100 easy and 2 of 10 hard bugs. Which tool is better, and why do the overall rates disagree?

::: note Answers and worked solutions
**1.** Correlation measures strength and direction of association (symmetric); regression gives an equation to predict a dependent variable from an independent one (asymmetric).

**2.** $\bar{x} = 5$, ȳ = 6.25. Sxx = $9 + 1 + 1 + 9 = 20$; Syy = 26.75; Sxy = $(- 3) (- 3.25) + (- 1) (0.75) + (1) (- 1.25) + (3) (3.75) = 9.75 - 0.75 - 1.25 + 11.25 = 19$. $r = \frac{19}{\sqrt{20 \times 26.75}} = 19 / 23.13$ = **0.821**. $b = \frac{19}{20}$ = **0.95**; $a = 6.25 - 0.95 \times 5$ = **1.5**; ŷ = 1.5 + 0.95x; at $x = 10$, ŷ = **11.0**.

**3.** −0.85: strong negative linear relationship; 0.1: practically no linear relationship.

**4.** $r^{2} = 0.8 \times 0.45 = 0.36 ,\  r$ = **+0.6** (both coefficients positive).

**5.** That line minimises errors in *y*, not in *x*; the x-on-y line is the correct one for estimating *x*.

**6.** Between −1 and 1; independent of origin and scale; unitless.

**7.** $r^2 = 0.36$: 36% of the variation is explained. $\mathrm{PE} = 0.6745 \times \frac{1 - 0.36}{6} = $ **0.0719**. $\frac{r}{\mathrm{PE}} = \frac{0.6}{0.0719} = 8.3 > 6$, so the correlation is significant.

**8.** $s_e = 10\sqrt{1 - 0.64} = 10 \times 0.6$ = **6**.

**9.** $r_{12.3} = \frac{0.6 - 0.5 \times 0.4}{\sqrt{(1 - 0.25)(1 - 0.16)}} = \frac{0.4}{\sqrt{0.63}}$ = **0.504**. $R_{1.23}^2 = \frac{0.36 + 0.25 - 2(0.6)(0.5)(0.4)}{0.84} = \frac{0.37}{0.84} = 0.4405$, so $R_{1.23}$ = **0.664**.

**10.** $33.46 + 5.679 \times 4.5 = 33.46 + 25.56$ = **59.0 marks**. The observed *x* values are only 2 to 8 hours, so 12 hours is extrapolation: the straight line may bend (a ceiling of 100 marks, tiredness) and the formula cannot know.

**11.** Tool A is better on both easy (80% against 70%) and hard bugs (30% against 20%). Overall A gets 38/110 = 34.5% and B gets 72/110 = 65.5% because A was used mostly on hard bugs and B on easy ones. This is Simpson's paradox; compare within difficulty groups, not overall.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). A shop records advertising spend *x* (in thousand rupees) and weekly sales *y* (in tens of thousands): $x = 2 ,\  4 ,\  6 ,\  8$, 10 and $y = 5 ,\  7 ,\  10 ,\  12 ,\  16$. Find Karl Pearson's coefficient of correlation and the regression line of *y* on *x*.**

*Introduction.* Karl Pearson's *r* measures the strength and direction of a *linear* relationship between two quantitative variables. Regression then gives the line for prediction.

*Working.* $n = 5 ,\  \sum x = 30 ,\  \sum y = 50 ,\  \sum x y = 354 ,\  \sum x^{2} = 220 ,\  \sum y^{2} = 574$.

*Correlation.* $r = \frac{n \sum x y - \sum x \sum y}{\sqrt{\{\left[ n \sum x^{2} - \left( \sum x \right)^{2} \right] \left[ n \sum y^{2} - \left( \sum y \right)^{2} \right]\}}} = \frac{5 \times 354 - 30 \times 50}{\sqrt{(1100 - 900) (2870 - 2500)}} = \frac{270}{\sqrt{200 \times 370}} = 270 / 272.03$ = **0.9925**. This is a very strong positive correlation.

*Regression.* *b* = Sxy/Sxx = 270/200 = **1.35**. $\bar{x} = 6$, ȳ = 10, so $a = 10 - 1.35 \times 6$ = **1.9**. The line is **ŷ = 1.9 + 1.35x**.

*Interpretation.* Every extra thousand rupees of advertising goes with 1.35 tens of thousands of extra sales, and $r^{2} = 0.985$ means 98.5% of the variation in sales is associated with advertising. *Conclusion.* Spend and sales move together very closely, but this data alone does not prove that advertising caused the sales.

**Q2 (5 marks). Six students have marks in Mathematics: 86, 72, 65, 91, 58, 77 and in Statistics: 80, 70, 60, 88, 62, 75. Calculate Spearman's rank correlation coefficient and say when it is preferred to Pearson's *r*.**

*Introduction.* **Spearman's rank correlation** $r_{s} = 1 - \frac{6 \sum d^{2}}{n (n^{2} - 1)}$ measures association between the *ranks* of two variables, where *d* is the difference of ranks.

*Ranking (highest = $1 ) . \ast$

| Maths | 86 | 72 | 65 | 91 | 58 | 77 |
|---|---|---|---|---|---|---|
| Rank $R_{1}$ | 2 | 4 | 5 | 1 | 6 | 3 |
| Statistics | 80 | 70 | 60 | 88 | 62 | 75 |
| Rank $R_{2}$ | 2 | 4 | 6 | 1 | 5 | 3 |
| $d = R_{1} - R_{2}$ | 0 | 0 | −1 | 0 | 1 | 0 |

$\sum d^{2} = 0 + 0 + 1 + 0 + 1 + 0 = 2$, and $n = 6$. So $r_{s} = 1 - \frac{6 \times 2}{6 \times 35} = 1$ − 12/210 = **0.943**.

*Interpretation.* The two rankings agree almost perfectly: students strong in Mathematics are strong in Statistics. *When preferred:* Spearman is used when data are only ordinal (ranks, grades), when the relation is monotonic but not a straight line, or when outliers would distort Pearson's *r*. *Conclusion.* $r_{s} = 0.943$ shows a very strong positive association.

**Q3 (10 marks). Explain correlation and regression. The CPU load *x* (%) and response time *y* (ms) of a server were: $x = 10 ,\  20 ,\  30 ,\  40 ,\  50$, 60 and $y = 12 ,\  15 ,\  21 ,\  23 ,\  30 ,\  31$. Find *r*, both regression lines, verify $r^{2} = b_{y} x \times b_{x} y$, and predict *y* at $x = 45$.**

*Introduction.* **Correlation** measures how closely two variables move together; **regression** fits a line to predict one variable (*y*, dependent) from the other (*x*, independent). Figure 3.1 shows the patterns of *r* and Figure 3.2 the two regression lines.

*Key ideas.*

1. **Scatter diagram.** Plot the pairs first; a curve or an outlier makes *r* misleading.
2. **Pearson's *r*** = $\frac{\mathrm{Sxy}}{\sqrt{\mathrm{Sxx} \cdot \mathrm{Syy}}}$, with $- 1 \leq r \leq + 1$, unit-free and unchanged by a change of origin or scale.
3. **Coefficient of determination** $r^{2}$ is the share of variation in *y* explained by *x*.
4. **Least squares** chooses ŷ = $a + b x$ to minimise Σ(y − ŷ)²; b = Sxy/Sxx and a = ȳ − $b \bar{x}$.
5. **Two lines.** *y* on *x* has slope $b_{y} x$ = Sxy/Sxx; *x* on *y* has slope $b_{x} y$ = Sxy/Syy. They intersect at ($\bar{x}$, ȳ).
6. **Link.** $r^{2} = b_{y} x \times b_{x} y$, and *r* has the sign of both coefficients.

*Calculation.* $n = 6 ,\  \sum x = 210 ,\  \sum y = 132 ,\  \sum x^{2} = 9100 ,\  \sum y^{2} = 3200 ,\  \sum x y = 5330$. $\bar{x} = 35$, ȳ = 22. Sxx = $9100 - 210^{2} / 6$ = **1750**. Syy = $3200 - 132^{2} / 6$ = **296**. Sxy = $5330 - \frac{210 \times 132}{6}$ = **710**.

*Correlation.* $r = \frac{710}{\sqrt{1750 \times 296}} = 710 / 719.7$ = **0.9865**, $r^{2}$ = **0.973**.

*Regression of *y* on $x . \ast b_{y} x$ = 710/1750 = **0.4057**; $a = 22 - 0.4057 \times 35$ = **7.80**. So **ŷ = 7.80 + 0.4057x**.

*Regression of *x* on $y . \ast b_{x} y$ = 710/296 = **2.3986**, so x̂ = $35 + 2.3986 (y - 22)$.

*Verification.* $b_{y} x \times b_{x} y = 0.4057 \times 2.3986$ = **$0.9732 = r^{2}$** ✓.

*Prediction.* At *x* = 45%: ŷ = $7.80 + 0.4057 \times 45$ = **26.06 ms**. This is interpolation (45 lies inside 10-60) and is reliable; predicting at 90% load would be extrapolation and may fail.

*Comparison (Table).*

| Point | Correlation | Regression |
|---|---|---|
| Purpose | strength of association | prediction of *y* from *x* |
| Variables | symmetric, *x* and *y* interchangeable | asymmetric, dependent and independent |
| Result | one number *r* | an equation $a + b x$ |
| Units | none | units of *y* per unit of *x* |

*Conclusion.* Response time rises by about 0.41 ms for every extra 1% of CPU load, and 97% of the variation is explained by load. The relation is strong, but the model is valid only within the observed range.
