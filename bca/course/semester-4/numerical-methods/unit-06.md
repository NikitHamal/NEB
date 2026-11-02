---
subject: Numerical Methods
grade: BCA Semester 4
unit: 6
title: Solution of Partial Differential Equations
hours: 5
area: BCA 253 · Numerical Methods · Unit 6
---

Heat flowing through a metal plate, the electric potential around a charged conductor, the pressure of groundwater under a dam: each is described by an equation in two or three space variables. This final unit shows how to turn such a **partial differential equation (PDE)** into a system of ordinary algebraic equations on a grid, and solve it with the tools of Unit 4.

::: key What this unit gives you
- Classification of second-order PDEs and the idea of finite differences.
- Deriving the difference equations for the Laplace and Poisson equations.
- Solving Laplace's equation on a square (direct solve and Liebmann/Gauss–Seidel iteration) and Poisson's equation, with verified numbers.
:::

## 6.1 Introduction and classification

A second-order linear PDE in two variables, A uₓₓ + B uₓᵧ + C uᵧᵧ + (lower terms) = 0, is classified by B² − 4AC:

| B² − 4AC | Type | Model equation | Physical meaning |
|---|---|---|---|
| < 0 | **Elliptic** | Laplace uₓₓ + uᵧᵧ = 0; Poisson uₓₓ + uᵧᵧ = f(x, y) | steady state (potential, steady heat) |
| = 0 | **Parabolic** | heat uₜ = c² uₓₓ | diffusion in time |
| > 0 | **Hyperbolic** | wave uₜₜ = c² uₓₓ | vibration, waves |

This unit treats the elliptic equations of Laplace and Poisson. For them the solution is determined by the values of u on the **boundary** of the region (a **Dirichlet** problem), and the interior values depend on all boundary values at once, so the whole grid is solved together.

## 6.2 Deriving difference equations

Cover the region with a grid of spacing h in both directions and write uᵢⱼ = u(xᵢ, yⱼ). Adding the Taylor series of u(x ± h) gives the **central second difference**

**uₓₓ ≈ (uᵢ₊₁,ⱼ − 2uᵢⱼ + uᵢ₋₁,ⱼ)/h²**, and likewise **uᵧᵧ ≈ (uᵢ,ⱼ₊₁ − 2uᵢⱼ + uᵢ,ⱼ₋₁)/h²**,

each with error O(h²). Substituting into the PDE:

- **Laplace (uₓₓ + uᵧᵧ = 0):** uᵢ₊₁,ⱼ + uᵢ₋₁,ⱼ + uᵢ,ⱼ₊₁ + uᵢ,ⱼ₋₁ − 4uᵢⱼ = 0, i.e. **uᵢⱼ = ¼(sum of the four neighbours)**: each interior value is the average of its neighbours (the *five-point formula*).
- **Poisson (uₓₓ + uᵧᵧ = f):** uᵢ₊₁,ⱼ + uᵢ₋₁,ⱼ + uᵢ,ⱼ₊₁ + uᵢ,ⱼ₋₁ − 4uᵢⱼ = **h² fᵢⱼ**.

Writing one equation for each interior grid point gives a linear system, with 4 on the diagonal and −1 for each neighbour: diagonally dominant, so the Gauss–Seidel method of Unit 4 converges. Applied to this system, Gauss–Seidel is called **Liebmann's iterative method**: sweep over the grid and replace each value by the average of its neighbours until nothing changes.

## 6.3 Laplace's equation on a square plate

::: example Plate with the top edge held at 100° and the other three edges at 0°
Take a mesh whose interior has 2 × 2 points. By symmetry the two top interior points are equal (call them *a*) and the two bottom ones are equal (*b*). The equations are 4a = 100 + 0 + a + b and 4b = 0 + 0 + a + b, since each interior point has two boundary neighbours and two interior ones. Then 3a − b = 100 and 3b − a = 0; so a = 3b and 8b = 100, giving **b = 12.5 and a = 37.5**. The computer solution of the four coupled equations is (37.5000, 37.5000, 12.5000, 12.5000), in agreement.
:::

A finer grid has 3 × 3 interior points, nine unknowns uᵢⱼ (i = row from the top, 1 to 3; j = column, 1 to 3), with the top boundary at 100 and the others 0.

::: example 3 × 3 interior points: direct solution
Solving the 9 × 9 linear system exactly gives:

|  | col 1 | col 2 | col 3 |
|---|---|---|---|
| row 1 (from top) | 42.8571 | 52.6786 | 42.8571 |
| row 2 (from top) | 18.7500 | 25.0000 | 18.7500 |
| row 3 (from top) | 7.1429 | 9.8214 | 7.1429 |

The centre value is 25 = ¼(100 + 0 + 0 + 0), the average of the four edge temperatures, as the **symmetry** of the problem requires (the centre sees each edge equally). Values decrease downward, away from the hot edge, and are symmetric left to right: u₁₁ = 42.8571, u₁₂ = 52.6786, u₂₁ = 18.7500, u₃₁ = 7.1429, u₃₂ = 9.8214.
:::

::: example Same problem by Liebmann (Gauss–Seidel) iteration from all zeros
Each sweep replaces every interior value, row by row, by the average of its four current neighbours:

| k | u₁₁ | u₁₂ | u₁₃ | u₂₁ | u₂₂ | u₂₃ | u₃₁ | u₃₂ | u₃₃ |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 25.0000 | 31.2500 | 32.8125 | 6.2500 | 9.3750 | 10.5469 | 1.5625 | 2.7344 | 3.3203 |
| 2 | 34.3750 | 44.1406 | 38.6719 | 11.3281 | 17.1875 | 14.7949 | 3.5156 | 6.0059 | 5.2002 |
| 3 | 38.8672 | 48.6816 | 40.8691 | 14.8926 | 21.0938 | 16.7908 | 5.2246 | 7.8796 | 6.1676 |
| 4 | 40.8936 | 50.7141 | 41.8762 | 16.8030 | 23.0469 | 17.7727 | 6.1707 | 8.8463 | 6.6547 |
| 5 | 41.8793 | 51.7006 | 42.3683 | 17.7742 | 24.0234 | 18.2616 | 6.6551 | 9.3333 | 6.8987 |
| 8 | 42.7351 | 52.5565 | 42.7961 | 18.6279 | 24.8779 | 18.6890 | 7.0818 | 9.7604 | 7.1123 |

After eight sweeps the largest difference from the exact solution is 0.1221. Each additional sweep multiplies the error by roughly a constant factor below one; a 100 × 100 grid would need many hundreds of sweeps, which is why practical codes use successive over-relaxation (SOR) or multigrid.
:::

**Other boundary conditions.** If part of the boundary is **insulated** (∂u/∂n = 0, a *Neumann* condition), a ghost point outside the grid is introduced with the value of its mirror image inside, so the neighbour sum doubles one interior term. On irregular boundaries, special difference formulas with unequal spacing are used.

## 6.4 Poisson's equation

::: example ∇²u = −10(x² + y² + 10) on the square 0 ≤ x, y ≤ 3, u = 0 on the boundary, h = 1
The interior grid points are (1, 1), (2, 1), (1, 2), (2, 2). The right-hand sides are f(1,1) = -120, f(2,1) = -150, f(1,2) = -150, f(2,2) = -180. With h = 1 the difference equation 4uᵢⱼ − (neighbours) = −h² f gives right-hand sides 120, 150, 150, 180 for the four points in that order. Unknowns u₁ = u(1, 1), u₂ = u(2, 1), u₃ = u(1, 2), u₄ = u(2, 2):

- 4u₁ − u₂ − u₃ = 120
- −u₁ + 4u₂ − u₄ = 150
- −u₁ + 4u₃ − u₄ = 150
- −u₂ − u₃ + 4u₄ = 180

The solution (verified by substitution in all four equations) is u(1,1) = 67.5000, u(2,1) = 75.0000, u(1,2) = 75.0000, u(2,2) = 82.5000. For example, 4(67.5) − 75 − 75 = 120 ✓ and 4(82.5) − 75 − 75 = 180 ✓. The symmetry about the diagonal (u₂ = u₃) lets you reduce the system to three equations by hand.

Gauss–Seidel from zero (u₁, u₂, u₃, u₄ updated in turn):

| k | u₁ | u₂ | u₃ | u₄ |
|---|---|---|---|---|
| 1 | 30.0000 | 45.0000 | 45.0000 | 67.5000 |
| 2 | 52.5000 | 67.5000 | 67.5000 | 78.7500 |
| 3 | 63.7500 | 73.1250 | 73.1250 | 81.5625 |
| 4 | 66.5625 | 74.5312 | 74.5312 | 82.2656 |
| 5 | 67.2656 | 74.8828 | 74.8828 | 82.4414 |

The iterates approach (67.5000, 75.0000, 75.0000, 82.5) steadily.
:::

## 6.5 Accuracy and practical notes

- The difference equations are accurate to O(h²); halving h quarters the truncation error but quadruples the number of unknowns.
- Direct solution (Gauss elimination, banded LU) costs more memory than iteration for large grids; iterative methods exploit the sparsity (only five nonzeros per row).
- For **parabolic** (heat) problems, the explicit scheme uᵢʲ⁺¹ = r uᵢ₋₁ʲ + (1 − 2r)uᵢʲ + r uᵢ₊₁ʲ with r = c²Δt/h² is stable only if r ≤ ½; the implicit Crank–Nicolson scheme is stable for all r. Hyperbolic problems need the Courant condition cΔt/h ≤ 1. These are outside the syllabus but explain why time-dependent problems need more care than the steady-state ones here.

## Formula and fact sheet

- uₓₓ ≈ (uᵢ₊₁,ⱼ − 2uᵢⱼ + uᵢ₋₁,ⱼ)/h².
- Laplace: uᵢⱼ = ¼(uᵢ₊₁,ⱼ + uᵢ₋₁,ⱼ + uᵢ,ⱼ₊₁ + uᵢ,ⱼ₋₁).
- Poisson: uᵢ₊₁,ⱼ + uᵢ₋₁,ⱼ + uᵢ,ⱼ₊₁ + uᵢ,ⱼ₋₁ − 4uᵢⱼ = h² fᵢⱼ.
- Classification by B² − 4AC: < 0 elliptic, = 0 parabolic, > 0 hyperbolic.
- Liebmann = Gauss–Seidel on the grid.

## Chapter summary

- Elliptic PDEs such as Laplace's and Poisson's equations describe steady states and are determined by their boundary values.
- Replacing derivatives by central differences turns the PDE into one algebraic equation per grid point: the value is the average of its neighbours (Laplace) plus a source term (Poisson).
- The resulting diagonally dominant system is solved directly or by Liebmann's iteration.

## Practice

1. Classify uₓₓ + uᵧᵧ = 0, uₜ = uₓₓ and uₜₜ = uₓₓ.
2. Derive the five-point difference formula for Laplace's equation.
3. A square plate has its top edge at 100° and the other edges at 0°. Using a mesh with four interior points, find the temperatures.
4. Do two Liebmann sweeps for the 3 × 3 interior problem starting from zero, in row order, and compare with the exact solution.
5. Write the difference equations for ∇²u = −10(x² + y² + 10) with h = 1 on [0, 3] × [0, 3], u = 0 on the boundary, and solve them.
6. Why is the Gauss–Seidel iteration guaranteed to converge for the five-point system?
7. Explain what changes in the difference equation at an insulated edge.
8. What is the effect of halving h on the accuracy and on the size of the system?

::: note Answers and worked solutions
**1.** uₓₓ + uᵧᵧ = 0: A = 1, B = 0, C = 1, B² − 4AC = −4 < 0: elliptic. uₜ = uₓₓ: only one second-derivative term, B² − 4AC = 0: parabolic. uₜₜ = uₓₓ: A = 1, C = −1, B² − 4AC = 4 > 0: hyperbolic.
**2.** Using uₓₓ ≈ (uᵢ₊₁,ⱼ − 2uᵢⱼ + uᵢ₋₁,ⱼ)/h² and the same for y, uₓₓ + uᵧᵧ = 0 gives uᵢ₊₁,ⱼ + uᵢ₋₁,ⱼ + uᵢ,ⱼ₊₁ + uᵢ,ⱼ₋₁ − 4uᵢⱼ = 0 and so uᵢⱼ = ¼(sum of neighbours).
**3.** Top interior points 37.5, bottom interior points 12.5 (full solution (37.5000, 37.5000, 12.5000, 12.5000)); derivation in Section 6.3.
**4.** The first rows of the Liebmann table in Section 6.3 are the answers for sweeps 1 and 2; they are still far from the exact values (u₂₂ = 25.0000, u₁₂ = 52.6786), which are reached after about eight sweeps to within 0.1221.
**5.** The four equations in Section 6.4; solution u(1,1) = 67.5000, u(2,1) = 75.0000, u(1,2) = 75.0000, u(2,2) = 82.5000.
**6.** The matrix has 4 on the diagonal and at most four −1s per row, so it is (weakly) diagonally dominant, and irreducibly so because every interior point is connected to a boundary point. This guarantees convergence of both Jacobi and Gauss–Seidel.
**7.** The normal derivative is zero, so the ghost value outside the edge equals the value inside; the neighbour sum includes twice the interior neighbour, e.g. 4uᵢⱼ = 2uᵢ,ⱼ₊₁ + uᵢ₊₁,ⱼ + uᵢ₋₁,ⱼ.
**8.** Truncation error falls by about 4 (O(h²)); the number of unknowns grows by 4, and the work of an iterative solver by more (the iterations needed also increase).
:::
