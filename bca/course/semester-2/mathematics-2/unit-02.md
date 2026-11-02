---
subject: Mathematics II
grade: BCA Semester 2
unit: 2
title: Systems of Linear Equations
area: BCA 154 · Mathematics II · Unit 2
---

Systems of linear equations appear everywhere: balancing circuits, fitting curves, balancing chemical equations, solving for the weights in a model. This unit gives the systematic method (Gaussian elimination), the theory of when solutions exist (rank), and the alternatives (Cramer's rule, inverse).

::: key What this unit gives you
- Matrix form AX = B; augmented matrix; row-echelon forms.
- Gaussian and Gauss–Jordan elimination with worked examples.
- Rank and the consistency test: unique, infinitely many, or no solution.
- Cramer's rule; homogeneous systems; computational cost.
:::

## 2.1 Systems and their solutions

A system of m linear equations in n unknowns can be written **AX = B**, where A is the coefficient matrix, X the unknowns, B the right-hand side. The **augmented matrix** is [A | B]. Geometrically, in two variables each equation is a line (unique solution: lines meet at a point; none: parallel; infinitely many: the same line); in three variables each equation is a plane.

**Elementary row operations** (do not change the solution set): swap two rows; multiply a row by a non-zero constant; add a multiple of one row to another.

## 2.2 Gaussian elimination

**Row echelon form**: all-zero rows at the bottom; each leading entry (pivot) is to the right of the one above. **Reduced** row echelon form (Gauss–Jordan): pivots are 1 and are the only non-zero entry in their column. Method: use a pivot to clear the entries below it (forward elimination), then solve upward (**back-substitution**).

::: example Worked example: unique solution
x + y + z = 6, 2x − y + z = 3, x + 2y − z = 2.
Augmented [[1, 1, 1 | 6], [2, −1, 1 | 3], [1, 2, −1 | 2]].
R₂ → R₂ − 2R₁: [0, −3, −1 | −9]. R₃ → R₃ − R₁: [0, 1, −2 | −4].
Swap R₂ and R₃: [0, 1, −2 | −4], [0, −3, −1 | −9]. R₃ → R₃ + 3R₂: [0, 0, −7 | −21].
Back-substitute: z = 3; y − 2(3) = −4 ⇒ y = 2; x + 2 + 3 = 6 ⇒ x = 1. **(x, y, z) = (1, 2, 3).** Check in the 2nd equation: 2 − 2 + 3 = 3 ✓.
:::

::: example Worked example: infinitely many solutions
x + y + z = 3, x − y = 1. Augmented [[1, 1, 1 | 3], [1, −1, 0 | 1]] → R₂ − R₁: [0, −2, −1 | −2]. So y = 1 − z/2 (from −2y − z = −2), and x = 1 + y = 2 − z/2. Let z = t (a **free variable**): **(x, y, z) = (2 − t/2, 1 − t/2, t)**, a line of solutions. Two equations in three unknowns can never have a unique solution.
:::

::: example Worked example: no solution
x + y = 1, 2x + 2y = 3. R₂ − 2R₁: [0, 0 | 1], i.e. 0 = 1, a contradiction. **Inconsistent**: the lines are parallel.
:::

## 2.3 Rank and consistency

The **rank** of a matrix is the number of non-zero rows in its echelon form (the number of pivots), i.e. the number of independent rows (equal to the number of independent columns).

::: example Worked example
A = [[1, 2, 3], [2, 4, 6], [1, 0, 1]]: R₂ − 2R₁ = [0, 0, 0]; R₃ − R₁ = [0, −2, −2]. Two non-zero rows, so **rank A = 2**. (Row 2 is twice row 1.)
:::

**Rouché–Capelli theorem** for AX = B with n unknowns:

| Condition | Result |
|---|---|
| rank A < rank [A \| B] | **inconsistent** (no solution) |
| rank A = rank [A \| B] = n | **unique** solution |
| rank A = rank [A \| B] = r < n | **infinitely many**, with n − r free parameters |

**Homogeneous systems AX = 0** always have the trivial solution X = 0; a non-trivial solution exists iff rank A < n, equivalently (for square A) det A = 0. Example: x + y = 0, 2x + 2y = 0 has the non-trivial solutions (t, −t).

**Square system** with det A ≠ 0: the unique solution X = A⁻¹B.

## 2.4 Cramer's rule

For a square system with det A ≠ 0, **xᵢ = det Aᵢ / det A**, where Aᵢ is A with column i replaced by B.

::: example Worked example
2x + y = 5, x − y = 1. det A = −2 − 1 = −3. A_x = [[5, 1], [1, −1]]: det = −5 − 1 = −6, so x = −6/−3 = **2**. A_y = [[2, 5], [1, 1]]: det = 2 − 5 = −3, so y = **1**.
:::

Cramer's rule is useful for small systems and for theory (it shows the solution depends continuously on the data); it is **far too slow** for large ones: it needs n + 1 determinants, each about n³ operations or worse by cofactors, whereas elimination costs about (2/3)n³ operations in total. For n = 1000 that is about 6.7 × 10⁸ operations: a fraction of a second.

## 2.5 Applications and numerical issues

- **Curve fitting:** find the parabola y = ax² + bx + c through (1, 2), (2, 3), (3, 6): a + b + c = 2, 4a + 2b + c = 3, 9a + 3b + c = 6. Subtracting: 3a + b = 1 and 5a + b = 3 ⇒ a = 1, b = −2, c = 3. **y = x² − 2x + 3.**
- **Balancing a chemical equation:** C₂H₆ + O₂ → CO₂ + H₂O: unknowns for each coefficient, carbon: 2a = c; hydrogen: 6a = 2d; oxygen: 2b = 2c + d. With a = 2: c = 4, d = 6, b = 7. **2C₂H₆ + 7O₂ → 4CO₂ + 6H₂O.**
- **Circuits (Kirchhoff):** current and voltage laws give linear systems in the currents.
- **Networks and traffic flow:** conservation at each node gives a system, usually with free variables.
- **Partial pivoting:** choose the largest available pivot in a column to limit rounding error. A system like 0.0001x + y = 1, x + y = 2 solved without pivoting in low precision can give badly wrong x. **Ill-conditioned** systems (nearly parallel lines or planes) amplify small data errors; the **condition number** measures this.
- **LU decomposition:** factor A = LU (lower × upper triangular) once, then solve many right-hand sides cheaply; **least squares** solves overdetermined systems (more equations than unknowns) by AᵀAX = AᵀB, the basis of linear regression.

## Formula and fact sheet

- AX = B; augmented [A | B]; three row operations.
- Rank = number of pivots. rank A < rank [A | B]: none; = n: unique; < n: infinite with n − r parameters.
- Homogeneous: non-trivial solutions iff rank < n (det = 0 when square).
- Cramer: xᵢ = det Aᵢ / det A. Gaussian elimination ≈ (2/3)n³ operations.

## Chapter summary

- Elimination reduces any system to echelon form and then solves by back-substitution.
- Rank decides the number of solutions; free variables parametrise infinite families.
- Cramer's rule and inverses give formulas but elimination is the practical method.
- Applications range from curve fitting to chemistry, circuits and regression.

## Practice

1. Solve by Gaussian elimination: x + 2y + z = 8, 2x + y − z = 1, x − y + 2z = 5.
2. Solve x + y − z = 1, 2x + 2y − 2z = 2, x − y + z = 3 and describe the solution set.
3. For what values of k does x + y = 2, 2x + ky = 5 have no solution? A unique one?
4. Find the rank of [[1, 2, 3, 4], [2, 4, 6, 8], [1, 0, 1, 0]].
5. Solve by Cramer's rule: 3x + 2y = 7, x − y = 1.
6. Find all solutions of the homogeneous system x + 2y + 3z = 0, 2x + 4y + 6z = 0.
7. Fit y = ax² + bx + c through (0, 1), (1, 4), (2, 9).
8. Balance: Fe + O₂ → Fe₂O₃.
9. Determine whether the system x + y = 2, x − y = 0, 2x + y = 3 is consistent.
10. A 400-equation system takes 1 s on a computer. Estimate the time for 4000 equations.

::: note Answers and worked solutions
**1.** R₂ − 2R₁: [0, −3, −3 | −15]; R₃ − R₁: [0, −3, 1 | −3]. R₃ − R₂: [0, 0, 4 | 12] ⇒ z = 3; −3y − 9 = −15 ⇒ y = 2; x + 4 + 3 = 8 ⇒ x = 1. **(1, 2, 3).**
**2.** Equation 2 is twice equation 1. Adding eqs 1 and 3: 2x = 4 ⇒ x = 2; then 2 + y − z = 1 ⇒ y − z = −1. Solutions **(2, t − 1, t)**: infinitely many (one free parameter).
**3.** Eliminate: R₂ − 2R₁ = [0, k − 2 | 1]. If k = 2: 0 = 1, **no solution**. If k ≠ 2: **unique** solution.
**4.** R₂ − 2R₁ = 0; R₃ − R₁ = [0, −2, −2, −4]. Two independent rows: **rank 2**.
**5.** det A = −3 − 2 = −5; x = det[[7, 2], [1, −1]]/−5 = (−7 − 2)/−5 = **9/5**; y = det[[3, 7], [1, 1]]/−5 = (3 − 7)/−5 = **4/5**. Check: 3(9/5) + 2(4/5) = 35/5 = 7 ✓.
**6.** Row 2 is twice row 1, so one equation: x = −2y − 3z with y = s, z = t free: **(−2s − 3t, s, t)**, a plane through the origin (rank 1, 2 free parameters).
**7.** c = 1; a + b + 1 = 4; 4a + 2b + 1 = 9 ⇒ a + b = 3, 2a + b = 4 ⇒ a = 1, b = 2: **y = x² + 2x + 1 = (x + 1)²**.
**8.** a Fe + b O₂ → c Fe₂O₃: Fe: a = 2c; O: 2b = 3c. With c = 2: a = 4, b = 3. **4Fe + 3O₂ → 2Fe₂O₃.**
**9.** From the first two: x = 1, y = 1; the third gives 2(1) + 1 = 3 ✓. **Consistent**, unique solution (1, 1) (rank 2 = rank of the augmented matrix).
**10.** Elimination is O(n³): 10 times more equations is 1000 times more work, about **1000 s ≈ 17 minutes**.
:::
