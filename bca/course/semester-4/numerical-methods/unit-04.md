---
subject: Numerical Methods
grade: BCA Semester 4
unit: 4
title: Solution of Linear Algebraic Equations
hours: 10
area: BCA 253 · Numerical Methods · Unit 4
---

Circuit analysis, structural frames, the Google PageRank vector and the normal equations of Unit 2 all lead to systems of linear equations Ax = b, sometimes with thousands of unknowns. This unit covers direct methods (Gauss elimination, Gauss–Jordan, LU), iterative methods (Jacobi, Gauss–Seidel), the dangers of ill-conditioning, and the power method for eigenvalues.

::: key What this unit gives you
- Gauss elimination with partial pivoting, Gauss–Jordan inversion, LU factorisation.
- Jacobi and Gauss–Seidel iteration; convergence and diagonal dominance.
- Ill-conditioning and the condition number.
- Eigenvalue estimation by the power method.
:::

*Syllabus note.* The mirror of the TU CACS252 outline used for this book (see `bca/SOURCES.md`) lists Units 1, 2, 3, 5, 6 but mentions "Linear Algebraic Equations" in the course description and lab list. The unit is included here as Unit 4, as in other TU outlines; its 10 hours are the remainder of 45.

## 4.1 Gauss elimination

**Forward elimination** converts Ax = b to an upper-triangular system by subtracting multiples mᵢₖ = aᵢₖ/aₖₖ of the pivot row from the rows below. **Back substitution** then solves from the last equation upwards. The cost is about n³/3 multiplications.

**Partial pivoting.** Before eliminating column k, swap the row with the largest |aᵢₖ| (i ≥ k) into the pivot position. This avoids dividing by a zero or tiny pivot and keeps the multipliers |m| ≤ 1, which controls round-off. Always use it on a computer.

::: example Solve 2x + y − z = 8, −3x − y + 2z = −11, −2x + y + 2z = −3
Operations (with partial pivoting): swap R1 ↔ R2; m21 = -0.6667; m31 = 0.6667; swap R2 ↔ R3; m32 = 0.2000. The reduced upper-triangular augmented matrix is

| x | y | z | RHS |
|---|---|---|---|
| -3.0000 | -1.0000 | 2.0000 | -11.0000 |
| 0.0000 | 1.6667 | 0.6667 | 4.3333 |
| 0.0000 | 0.0000 | 0.2000 | -0.2000 |

Back substitution: z = −0.2/0.2 = −1; y = (4.3333 − 0.6667(−1))/1.6667 = 3; x = (−11 + 3 − 2(−1))/(−3) = 2. The solution is **(x, y, z) = (2.0000, 3.0000, -1.0000)**, which agrees with `numpy.linalg.solve`. Check in the first original equation: 2(2) + 3 − (−1) = 8 ✓.
:::

**Singular and inconsistent systems.** If a zero pivot remains in a column after trying all rows below, the matrix is singular: either no solution (a row 0 = nonzero) or infinitely many (a row 0 = 0). The determinant equals the product of the pivots times (−1) to the number of swaps.

## 4.2 Gauss–Jordan method and matrix inversion

Gauss–Jordan continues eliminating *above* the pivots too, reducing A to the identity; the right-hand side becomes the solution. Applied to the augmented matrix [A | I] it produces **A⁻¹**.

::: example Inverse of [[2, 1], [5, 3]]
[A | I]: R₁ ← R₁/2 gives [1, 0.5 | 0.5, 0]; R₂ ← R₂ − 5R₁ gives [0, 0.5 | −2.5, 1]; R₂ ← 2R₂ gives [0, 1 | −5, 2]; R₁ ← R₁ − 0.5R₂ gives [1, 0 | 3, −1]. So A⁻¹ = [[3, −1], [−5, 2]]. Numerical check by NumPy: 3.0000, -1.0000, -5.0000, 2.0000 (row-wise). Check: A·A⁻¹ = [[6 − 5, −2 + 2], [15 − 15, −5 + 6]] = I ✓.
:::

Gauss–Jordan costs about n³/2, more than Gauss elimination, so use it for inverses, not for single systems.

## 4.3 LU factorisation

If no row swaps are needed, A = LU with L unit-lower-triangular (1s on the diagonal, the multipliers below) and U upper-triangular (the result of elimination). Then Ax = b becomes two cheap triangular solves: **Ly = b** (forward substitution), **Ux = y** (back substitution). Once A is factorised, new right-hand sides cost only O(n²), which is why LU is the workhorse of numerical libraries (with pivoting: PA = LU). The determinant is the product of U's diagonal.

::: example Doolittle LU for A = [[2, 1, 1], [4, 3, 3], [8, 7, 9]], b = (4, 10, 24)
Elimination multipliers: m₂₁ = 2, m₃₁ = 4, then m₃₂ = 3. So L = [1, 0, 0; 2, 1, 0; 4, 3, 1] and U = [2, 1, 1; 0, 1, 1; 0, 0, 2] (rows separated by semicolons). Forward substitution Ly = b gives y = (4, 2, 2); back substitution Ux = y gives x = (1, 1, 1). The determinant is 2 × 1 × 2 = 4. Check: LU reproduces A and A x = b in code.
:::

Variants: **Crout** (U has the unit diagonal), **Cholesky** A = LLᵀ for symmetric positive-definite matrices (half the work, no pivoting needed).

## 4.4 Iterative methods: Jacobi and Gauss–Seidel

For large sparse systems direct methods fill in zeros and cost too much. Iterative methods start from a guess and improve it. Solve equation *i* for xᵢ:

**xᵢ⁽ᵏ⁺¹⁾ = (bᵢ − Σ_{j≠i} aᵢⱼ xⱼ)/aᵢᵢ**

- **Jacobi**: use only the old iterate x⁽ᵏ⁾ on the right (all components updated "simultaneously").
- **Gauss–Seidel**: use the **newest** values as soon as they are available (components updated one after another), so it normally converges about twice as fast.

**Convergence.** Both converge for any start if A is **strictly diagonally dominant** (|aᵢᵢ| > Σ_{j≠i}|aᵢⱼ| in every row). That is sufficient, not necessary; the exact condition is that the iteration matrix has spectral radius below 1. Rearranging the equations so that large coefficients lie on the diagonal often helps.

::: example 10x₁ − x₂ + 2x₃ = 6; −x₁ + 11x₂ − x₃ + 3x₄ = 25; 2x₁ − x₂ + 10x₃ − x₄ = −11; 3x₂ − x₃ + 8x₄ = 15, start 0
The matrix is strictly diagonally dominant (10 > 3, 11 > 5, 10 > 4, 8 > 4); the exact solution is (1.0000, 2.0000, -1.0000, 1.0000).

**Jacobi** (first six sweeps):

| k | x₁ | x₂ | x₃ | x₄ |
|---|---|---|---|---|
| 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 1 | 0.6000 | 2.2727 | -1.1000 | 1.8750 |
| 2 | 1.0473 | 1.7159 | -0.8052 | 0.8852 |
| 3 | 0.9326 | 2.0533 | -1.0493 | 1.1309 |
| 4 | 1.0152 | 1.9537 | -0.9681 | 0.9738 |
| 5 | 0.9890 | 2.0114 | -1.0103 | 1.0214 |
| 6 | 1.0032 | 1.9922 | -0.9945 | 0.9944 |

**Gauss–Seidel** (first six sweeps):

| k | x₁ | x₂ | x₃ | x₄ |
|---|---|---|---|---|
| 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 1 | 0.6000 | 2.3273 | -0.9873 | 0.8789 |
| 2 | 1.0302 | 2.0369 | -1.0145 | 0.9843 |
| 3 | 1.0066 | 2.0036 | -1.0025 | 0.9984 |
| 4 | 1.0009 | 2.0003 | -1.0003 | 0.9998 |
| 5 | 1.0001 | 2.0000 | -1.0000 | 1.0000 |
| 6 | 1.0000 | 2.0000 | -1.0000 | 1.0000 |

To get all components within 5 × 10⁻⁵ of the exact answer Jacobi needs **12** sweeps and Gauss–Seidel **6**. The spectral radius of the iteration matrix is 0.4264 for Jacobi and 0.0898 for Gauss–Seidel; the smaller it is, the faster the convergence. Because each sweep is cheap (n² operations for a dense matrix, far less for sparse ones), iterative methods win for huge sparse systems.
:::

::: caution Equation order matters
For x + 3y = 5, 4x + y = 6 (solution (1.1818, 1.2727)), Gauss–Seidel from (0, 0) gives (5.00, -14.00) → (47.00, -182.00) → (551, -2198) → (6599, -26390): it diverges because the matrix is not diagonally dominant. Writing the equations in the other order, 4x + y = 6 first, gives (1.5000, 1.1667) → (1.2083, 1.2639) → (1.1840, 1.2720) → (1.1820, 1.2727) → (1.1818, 1.2727), which converges. The two systems are mathematically identical.
:::

## 4.5 Ill-conditioning

A system is **ill-conditioned** if tiny changes in A or b cause large changes in x. The culprit is a nearly singular matrix, and no algorithm can repair it; pivoting only avoids *additional* damage.

::: example A nearly singular system
x + y = 2, x + 1.0001y = 2.0001 has the solution (1, 1). Change the right-hand side by 0.0001 to 2.0002: the solution jumps to (0, 2). A change of 0.005 % in one coefficient moved the answer by 100 %. The two equations describe almost parallel lines, so their intersection point is very sensitive.
:::

The **condition number** κ(A) = ‖A‖·‖A⁻¹‖ measures the amplification: relative error in x ≤ κ(A) × relative error in the data. For the matrix above κ = 40002, so a relative data error of 10⁻⁴ may produce a relative solution error of order one. The 3 × 3 Hilbert matrix, with entries 1/(i + j − 1), has κ = 524; it is moderately conditioned for n = 3 but becomes terrible as n grows. Rules of thumb: κ ≈ 10ᵏ loses about k significant digits. Remedies: scaling, pivoting, higher precision, iterative refinement, or reformulating the problem.

## 4.6 Eigenvalues: the power method

The **power method** finds the **dominant** eigenvalue (largest in magnitude) λ₁ and its eigenvector. Start with any v₀ (with a component along the dominant eigenvector). Repeat: w = Avₖ₋₁; λₖ = the entry of w with the largest magnitude; vₖ = w/λₖ. Then λₖ → λ₁ and vₖ → eigenvector, at a rate |λ₂/λ₁|.

::: example A = [[2, −1, 0], [−1, 2, −1], [0, −1, 2]], v₀ = (0, 1, 0)
| k | A·vₖ₋₁ | λₖ (largest entry) | vₖ (scaled) |
|---|---|---|---|
| 1 | (-1.0000, 2.0000, -1.0000) | 2.0000 | (-0.5000, 1.0000, -0.5000) |
| 2 | (-2.0000, 3.0000, -2.0000) | 3.0000 | (-0.6667, 1.0000, -0.6667) |
| 3 | (-2.3333, 3.3333, -2.3333) | 3.3333 | (-0.7000, 1.0000, -0.7000) |
| 4 | (-2.4000, 3.4000, -2.4000) | 3.4000 | (-0.7059, 1.0000, -0.7059) |
| 5 | (-2.4118, 3.4118, -2.4118) | 3.4118 | (-0.7069, 1.0000, -0.7069) |
| 6 | (-2.4138, 3.4138, -2.4138) | 3.4138 | (-0.7071, 1.0000, -0.7071) |
| 7 | (-2.4141, 3.4141, -2.4141) | 3.4141 | (-0.7071, 1.0000, -0.7071) |

The eigenvalue estimates climb towards **2 + √2 = 3.4142**, and the vector towards (−0.7071, 1, −0.7071) ∝ (1, −√2, 1). The Rayleigh quotient vᵀAv/vᵀv of the final vector gives 3.4142, a faster-converging estimate. The smallest eigenvalue can be found by applying the method to A⁻¹ (inverse iteration); shifts find the others.
:::

## Formula and fact sheet

- Multiplier mᵢₖ = aᵢₖ/aₖₖ; partial pivoting: swap to the largest |aᵢₖ|; det = ±Π pivots.
- Gauss–Jordan on [A | I] gives A⁻¹. LU: Ly = b then Ux = y.
- Jacobi: old values; Gauss–Seidel: newest values; converge if diagonally dominant.
- κ(A) = ‖A‖‖A⁻¹‖; digits lost ≈ log₁₀ κ.
- Power method: w = Av, λ = largest entry, v = w/λ; rate |λ₂/λ₁|.

## Chapter summary

- Direct methods (Gauss, Gauss–Jordan, LU) give the exact answer in a fixed number of steps; use partial pivoting.
- Iterative methods suit large sparse systems; Gauss–Seidel usually converges faster than Jacobi, and diagonal dominance guarantees it.
- Ill-conditioned systems amplify data errors regardless of method; the condition number quantifies this.
- The power method estimates the dominant eigenpair using repeated multiplication.

## Practice

1. Solve 2x + y − z = 8, −3x − y + 2z = −11, −2x + y + 2z = −3 by Gauss elimination with partial pivoting.
2. Find the inverse of [[2, 1], [5, 3]] by Gauss–Jordan.
3. Factorise A = [[2, 1, 1], [4, 3, 3], [8, 7, 9]] as LU and solve Ax = (4, 10, 24).
4. Do two Jacobi and two Gauss–Seidel iterations for the 4 × 4 system of Section 4.4 from zero; which gives the better x₂?
5. State the sufficient condition for convergence of Jacobi and Gauss–Seidel. Is it necessary?
6. Why does Gauss–Seidel diverge for x + 3y = 5, 4x + y = 6 but converge after swapping the equations?
7. What is an ill-conditioned system? Illustrate with an example and name the condition number.
8. Apply the power method to A = [[2, −1, 0], [−1, 2, −1], [0, −1, 2]] and report the eigenvalue after four iterations.
9. Compare Gauss elimination and LU factorisation when there are many right-hand sides.

::: note Answers and worked solutions
**1.** (x, y, z) = (2.0000, 3.0000, -1.0000); the elimination is shown in Section 4.1.
**2.** A⁻¹ = [[3, −1], [−5, 2]] (Section 4.2).
**3.** L = [1, 0, 0; 2, 1, 0; 4, 3, 1], U = [2, 1, 1; 0, 1, 1; 0, 0, 2], y = (4, 2, 2), x = (1, 1, 1).
**4.** From the tables in Section 4.4: after two sweeps Jacobi and Gauss–Seidel give the rows k = 2; Gauss–Seidel's x₂ = 2.0369 is closer to the exact 2.0000 than Jacobi's value in its table row k = 2, because it uses the new values at once.
**5.** Strict diagonal dominance of rows: |aᵢᵢ| > Σ_{j≠i}|aᵢⱼ|. It is sufficient but not necessary; convergence actually requires the spectral radius of the iteration matrix to be < 1.
**6.** In the first order the matrix is not diagonally dominant (|1| < |3|) and the iteration matrix has spectral radius above 1; after swapping, the large entries 4 and 3 sit on the diagonal and the iteration contracts (compare the sequences in Section 4.4).
**7.** Small input changes cause large output changes, as in x + y = 2, x + 1.0001y = 2.0001 → (1, 1), versus right side 2.0002 → (0, 2). The condition number κ(A) = ‖A‖‖A⁻¹‖ (here 40002) measures the amplification.
**8.** From the table in Section 4.6, the fourth iteration gives λ ≈ 3.4000 (true 3.4142).
**9.** Plain elimination repeats the O(n³) work for every new b. LU factorises once (O(n³)) and then each right-hand side costs only O(n²) for the two triangular solves.
:::
