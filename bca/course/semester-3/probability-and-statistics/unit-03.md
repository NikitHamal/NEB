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
