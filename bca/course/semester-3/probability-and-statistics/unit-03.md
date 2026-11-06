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
- Scatter diagrams and Karl Pearson's correlation coefficient r.
- Regression lines by the least squares method; prediction.
- Worked numerical problems.
:::

## 3.1 Correlation

Two variables are **correlated** if they change together: **positive** (both rise: study hours and marks), **negative** (one rises as the other falls: price and demand), or **zero/no correlation**. **Correlation is not causation:** ice-cream sales and drowning both rise in summer without either causing the other.

**Scatter diagram:** plot each pair (x, y) as a point. Points rising from lower left to upper right indicate positive correlation, falling points negative, a shapeless cloud none; points close to a straight line indicate strong linear correlation.

**Karl Pearson's coefficient of correlation** r = Cov(x, y)/(σₓσᵧ) = Σ(x − x̄)(y − ȳ)/√[Σ(x − x̄)² · Σ(y − ȳ)²]. Computational form:

r = [nΣxy − ΣxΣy] / √{[nΣx² − (Σx)²][nΣy² − (Σy)²]}

Properties: **−1 ≤ r ≤ +1**; r = +1 perfect positive, −1 perfect negative, 0 no *linear* correlation; r is unchanged by a change of origin or positive scale; r has no units. Rough interpretation: |r| < 0.3 weak, 0.3–0.7 moderate, > 0.7 strong. The **coefficient of determination** r² is the proportion of variation in y explained by x. **Spearman's rank correlation** for ordered data is r_s = 1 − 6Σd²/(n(n² − 1)).

::: example Worked example: study hours and marks
x (hours per day): 1, 2, 3, 4, 5. y (marks out of 10): 2, 4, 5, 4, 5. n = 5, x̄ = 3, ȳ = 4.
Σ(x − x̄)² = 4 + 1 + 0 + 1 + 4 = **10**; Σ(y − ȳ)² = 4 + 0 + 1 + 0 + 1 = **6**; Σ(x − x̄)(y − ȳ) = (−2)(−2) + (−1)(0) + 0·1 + (1)(0) + (2)(1) = 4 + 0 + 0 + 0 + 2 = **6**.
r = 6/√(10 × 6) = 6/√60 = **0.7746**: strong positive correlation. r² = **0.60**: 60% of the variation in marks is associated with study hours.
:::

## 3.2 Regression analysis

**Regression** finds the **line of best fit** used to estimate the **dependent** variable (y, the response) from the **independent** variable (x, the predictor). The **least squares method** chooses the line y = a + bx that minimises Σ(y − ŷ)², the sum of squared vertical errors. Setting derivatives to zero gives the **normal equations**:

Σy = na + bΣx
Σxy = aΣx + bΣx²

Solution: **b = Sxy/Sxx = [nΣxy − ΣxΣy]/[nΣx² − (Σx)²]**, **a = ȳ − b x̄**. The slope b is the **regression coefficient of y on x** (b_yx): the change in y per unit x. If we regress x on y we get a different line, x = a′ + b′y, with **b_xy = Sxy/Syy**. The two lines intersect at (x̄, ȳ), and **r² = b_yx × b_xy** (r takes the sign of the b's). If r = ±1 the two lines coincide; if r = 0 they are perpendicular (horizontal and vertical).

::: example Worked example: regression for the same data
b_yx = Sxy/Sxx = 6/10 = **0.6**; a = 4 − 0.6 × 3 = **2.2**. Regression line of y on x: **ŷ = 2.2 + 0.6x**. Prediction: study 6 hours → ŷ = 2.2 + 3.6 = **5.8** marks (interpolation is safer than extrapolating far outside the observed range of 1–5 hours).
b_xy = Sxy/Syy = 6/6 = **1.0**; x on y: x̂ = 3 + 1.0(y − 4) = y − 1. Check: r² = 0.6 × 1.0 = 0.6, so r = √0.6 = 0.7746 ✓. Both lines pass through (3, 4).
The residual at x = 2: ŷ = 3.4, actual 4, error 0.6. The residuals sum to zero.
:::

**Dependent and independent variables:** choose which to predict *before* fitting; the y-on-x line minimises vertical errors, and is wrong for predicting x from y. **Assumptions:** linear relationship, errors independent with roughly constant variance, no influential outliers. **Using software:** Excel `=CORREL(x,y)`, `=SLOPE(y,x)`, `=INTERCEPT(y,x)`; SPSS *Analyze → Correlate / Regression*; Python `numpy.polyfit`.

## 3.3 Seeing correlation and regression

```svgfig label="3.1" caption="Three scatter diagrams of 12 points each. (a) The points hug a rising line: r = +0.98, very strong positive correlation. (b) A shapeless cloud: r = −0.19, practically no linear correlation. (c) The points hug a falling line: r = −0.96, very strong negative correlation. The sign of r gives the direction and its size gives the tightness."
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

```svgfig label="3.2" caption="Two regression lines for the same data. The line of y on x (navy, slope b_yx = 0.6) minimises vertical errors; the line of x on y (red, equivalent to y = x + 1, slope 1/b_xy = 1) minimises horizontal errors. They cross at the mean point (3, 4); the product of the two regression coefficients is 0.6 × 1.0 = 0.6 = r²."
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
4. **Finding related features.** Correlation between columns of a data set shows duplicated information. If two sensors have r = 0.99, one can be dropped to save storage. Analysts also use r to pick features that relate to the target.
5. **Performance modelling in computing.** Run time often grows with input size, and regression estimates by how much. A developer fits time against file size to predict when a script will become too slow. Server planners do the same with traffic and CPU load.
6. **Economics and public policy.** Economists relate income to spending, and rainfall to paddy yield. Nepal Rastra Bank studies relationships such as remittance and consumption this way. Policy makers still remember that correlation alone does not prove cause.
7. **Health and agriculture.** Doctors relate dose to response, and farmers relate fertiliser to yield. The slope tells how much extra yield one more kilogram of fertiliser gives. The r² value shows how much of the yield variation fertiliser explains.
8. **Quality checks of other methods.** Calibration of a cheap instrument against an accurate one uses a regression line. An r close to 1 shows the cheap instrument is trustworthy. The residuals reveal where it fails.

```photogrid label="3.2" cols="2" ratio="1.2" caption="Regression began with fathers and sons. (a) Sir Francis Galton, who in the 1880s measured the heights of parents and children and noticed that tall fathers had sons who were tall, but on average not as tall: heights regress towards the mean. (b) A simulation of 1,000 father-son pairs with mean height 170 cm, standard deviation 6 cm and a true correlation of 0.5 (random seed 2081). The least-squares line has slope 0.54 and the sample correlation is r = 0.53. A slope below 1 is the regression effect: the dashed line y = x is where sons would be as tall as their fathers, and the fitted line is flatter. For a 180 cm father the line predicts a son of 175.6 cm, not 180 cm."
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

```photogrid label="3.3" cols="2" ratio="1.2" caption="Correlation is not causation. (a) An ice-cream seller on a beach. (b) A simulation of 60 hot and cool days (seed 2081): temperature drives ice-cream sales (r = 0.84) and, because more people swim, also the number of drownings (r = 0.62). Ice-cream sales and drownings are therefore correlated too, r = 0.46, although neither causes the other. When temperature is held fixed, the partial correlation of ice cream with drownings is (0.46 - 0.84 x 0.62) / sqrt((1 - 0.84^2)(1 - 0.62^2)) = -0.16, close to zero. A hidden common cause (a confounder) can create a correlation; before you claim that one thing causes another you need an experiment or a control for the confounder."
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

## Formula and fact sheet

- r = Sxy/√(Sxx·Syy); −1 ≤ r ≤ 1; r² = proportion explained.
- Least squares: b = Sxy/Sxx, a = ȳ − b x̄; ŷ = a + bx; lines meet at (x̄, ȳ).
- b_yx × b_xy = r². Spearman r_s = 1 − 6Σd²/(n(n² − 1)).

## Chapter summary

- Correlation measures linear association with r from −1 to +1; correlation does not prove causation.
- Least squares regression gives the best-fitting line for predicting y from x; the two regression lines meet at the means and their slopes multiply to r².

## Practice

1. Differentiate correlation and regression.
2. For x = 2, 4, 6, 8 and y = 3, 7, 5, 10 compute r and the regression line of y on x; predict y for x = 10.
3. Interpret r = −0.85 and r = 0.1.
4. If b_yx = 0.8 and b_xy = 0.45, find r.
5. Why must the regression line of y on x not be used to predict x?
6. State three properties of r.

::: note Answers and worked solutions
**1.** Correlation measures strength and direction of association (symmetric); regression gives an equation to predict a dependent variable from an independent one (asymmetric).
**2.** x̄ = 5, ȳ = 6.25. Sxx = 9 + 1 + 1 + 9 = 20; Syy = 26.75; Sxy = (−3)(−3.25) + (−1)(0.75) + (1)(−1.25) + (3)(3.75) = 9.75 − 0.75 − 1.25 + 11.25 = 19. r = 19/√(20 × 26.75) = 19/23.13 = **0.821**. b = 19/20 = **0.95**; a = 6.25 − 0.95 × 5 = **1.5**; ŷ = 1.5 + 0.95x; at x = 10, ŷ = **11.0**.
**3.** −0.85: strong negative linear relationship; 0.1: practically no linear relationship.
**4.** r² = 0.8 × 0.45 = 0.36, r = **+0.6** (both coefficients positive).
**5.** That line minimises errors in y, not in x; the x-on-y line is the correct one for estimating x.
**6.** Between −1 and 1; independent of origin and scale; unitless.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). A shop records advertising spend x (in thousand rupees) and weekly sales y (in tens of thousands): x = 2, 4, 6, 8, 10 and y = 5, 7, 10, 12, 16. Find Karl Pearson's coefficient of correlation and the regression line of y on x.**

*Introduction.* Karl Pearson's r measures the strength and direction of a *linear* relationship between two quantitative variables. Regression then gives the line for prediction.

*Working.* n = 5, Σx = 30, Σy = 50, Σxy = 354, Σx² = 220, Σy² = 574.

*Correlation.* r = [nΣxy − ΣxΣy] / √{[nΣx² − (Σx)²][nΣy² − (Σy)²]} = (5 × 354 − 30 × 50) / √[(1100 − 900)(2870 − 2500)] = 270 / √(200 × 370) = 270/272.03 = **0.9925**. This is a very strong positive correlation.

*Regression.* b = Sxy/Sxx = 270/200 = **1.35**. x̄ = 6, ȳ = 10, so a = 10 − 1.35 × 6 = **1.9**. The line is **ŷ = 1.9 + 1.35x**.

*Interpretation.* Every extra thousand rupees of advertising goes with 1.35 tens of thousands of extra sales, and r² = 0.985 means 98.5% of the variation in sales is associated with advertising. *Conclusion.* Spend and sales move together very closely, but this data alone does not prove that advertising caused the sales.

**Q2 (5 marks). Six students have marks in Mathematics: 86, 72, 65, 91, 58, 77 and in Statistics: 80, 70, 60, 88, 62, 75. Calculate Spearman's rank correlation coefficient and say when it is preferred to Pearson's r.**

*Introduction.* **Spearman's rank correlation** r_s = 1 − 6Σd²/[n(n² − 1)] measures association between the *ranks* of two variables, where d is the difference of ranks.

*Ranking (highest = 1).*

| Maths | 86 | 72 | 65 | 91 | 58 | 77 |
|---|---|---|---|---|---|---|
| Rank R₁ | 2 | 4 | 5 | 1 | 6 | 3 |
| Statistics | 80 | 70 | 60 | 88 | 62 | 75 |
| Rank R₂ | 2 | 4 | 6 | 1 | 5 | 3 |
| d = R₁ − R₂ | 0 | 0 | −1 | 0 | 1 | 0 |

Σd² = 0 + 0 + 1 + 0 + 1 + 0 = 2, and n = 6. So r_s = 1 − (6 × 2)/(6 × 35) = 1 − 12/210 = **0.943**.

*Interpretation.* The two rankings agree almost perfectly: students strong in Mathematics are strong in Statistics. *When preferred:* Spearman is used when data are only ordinal (ranks, grades), when the relation is monotonic but not a straight line, or when outliers would distort Pearson's r. *Conclusion.* r_s = 0.943 shows a very strong positive association.

**Q3 (10 marks). Explain correlation and regression. The CPU load x (%) and response time y (ms) of a server were: x = 10, 20, 30, 40, 50, 60 and y = 12, 15, 21, 23, 30, 31. Find r, both regression lines, verify r² = b_yx × b_xy, and predict y at x = 45.**

*Introduction.* **Correlation** measures how closely two variables move together; **regression** fits a line to predict one variable (y, dependent) from the other (x, independent). Figure 3.1 shows the patterns of r and Figure 3.2 the two regression lines.

*Key ideas.*

1. **Scatter diagram.** Plot the pairs first; a curve or an outlier makes r misleading.
2. **Pearson's r** = Sxy/√(Sxx·Syy), with −1 ≤ r ≤ +1, unit-free and unchanged by a change of origin or scale.
3. **Coefficient of determination** r² is the share of variation in y explained by x.
4. **Least squares** chooses ŷ = a + bx to minimise Σ(y − ŷ)²; b = Sxy/Sxx and a = ȳ − b x̄.
5. **Two lines.** y on x has slope b_yx = Sxy/Sxx; x on y has slope b_xy = Sxy/Syy. They intersect at (x̄, ȳ).
6. **Link.** r² = b_yx × b_xy, and r has the sign of both coefficients.

*Calculation.* n = 6, Σx = 210, Σy = 132, Σx² = 9100, Σy² = 3200, Σxy = 5330. x̄ = 35, ȳ = 22. Sxx = 9100 − 210²/6 = **1750**. Syy = 3200 − 132²/6 = **296**. Sxy = 5330 − (210 × 132)/6 = **710**.

*Correlation.* r = 710/√(1750 × 296) = 710/719.7 = **0.9865**, r² = **0.973**.

*Regression of y on x.* b_yx = 710/1750 = **0.4057**; a = 22 − 0.4057 × 35 = **7.80**. So **ŷ = 7.80 + 0.4057x**.

*Regression of x on y.* b_xy = 710/296 = **2.3986**, so x̂ = 35 + 2.3986(y − 22).

*Verification.* b_yx × b_xy = 0.4057 × 2.3986 = **0.9732 = r²** ✓.

*Prediction.* At x = 45%: ŷ = 7.80 + 0.4057 × 45 = **26.06 ms**. This is interpolation (45 lies inside 10-60) and is reliable; predicting at 90% load would be extrapolation and may fail.

*Comparison (Table).*

| Point | Correlation | Regression |
|---|---|---|
| Purpose | strength of association | prediction of y from x |
| Variables | symmetric, x and y interchangeable | asymmetric, dependent and independent |
| Result | one number r | an equation a + bx |
| Units | none | units of y per unit of x |

*Conclusion.* Response time rises by about 0.41 ms for every extra 1% of CPU load, and 97% of the variation is explained by load. The relation is strong, but the model is valid only within the observed range.
