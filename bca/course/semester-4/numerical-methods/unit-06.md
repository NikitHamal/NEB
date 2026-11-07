---
subject: Numerical Methods
grade: BCA Semester 4
unit: 6
title: Solution of Partial Differential Equations
hours: 5
area: BCA 253 · Numerical Methods · Unit 6
---

Heat flowing through a metal plate, the electric potential around a charged conductor, the pressure of groundwater under a $d a m$: each is described by an equation in two or three space variables. This final unit shows how to turn such a **partial differential equation (PDE)** into a system of ordinary algebraic equations on a grid, and solve it with the tools of Unit 4.

::: key What this unit gives you
- Classification of second-order PDEs and the idea of finite differences.
- Deriving the difference equations for the Laplace and Poisson equations.
- Solving Laplace's equation on a square (direct solve and Liebmann/Gauss–Seidel iteration) and Poisson's equation, with verified numbers.
:::

## 6.1 Introduction and classification

A second-order linear PDE in two variables, A uₓₓ + B uₓᵧ + C uᵧᵧ + (lower terms) = 0, is classified by $B^{2}$ − 4AC:

| $B^{2}$ − 4AC | Type | Model equation | Physical meaning |
|---|---|---|---|
| < 0 | **Elliptic** | Laplace $u_{xx}$ + uᵧᵧ = 0; Poisson $u_{xx}$ + uᵧᵧ = $f (x ,\  y)$ | steady state (potential, steady heat) |
| = 0 | **Parabolic** | heat $u_{t} = c^{2} u_{xx}$ | diffusion in time |
| > 0 | **Hyperbolic** | wave $u_{tt} = c^{2} u_{xx}$ | vibration, waves |

This unit treats the elliptic equations of Laplace and Poisson. For them the solution is determined by the values of *u* on the **boundary** of the region (a **Dirichlet** problem), and the interior values depend on all boundary values at once, so the whole grid is solved together.

## 6.2 Deriving difference equations

Cover the region with a grid of spacing *h* in both directions and write $u_{ij} = u (x_{i} ,\  y_{j})$. Adding the Taylor series of $u (x \pm h)$ gives the **central second difference**

**uₓₓ ≈ (uᵢ₊₁,ⱼ − 2uᵢⱼ + uᵢ₋₁,ⱼ)/h²**, and likewise **uᵧᵧ ≈ (uᵢ,ⱼ₊₁ − 2uᵢⱼ + uᵢ,ⱼ₋₁)/h²**,

each with error $O (h^{2})$. Substituting into the PDE:

- **Laplace ($u_{xx}$ + uᵧᵧ = 0):** uᵢ₊₁,ⱼ + uᵢ₋₁,ⱼ + uᵢ,ⱼ₊₁ + uᵢ,ⱼ₋₁ − 4uᵢⱼ = 0, i.e. **$u_{ij} = \frac{1}{4} ( \mathrm{sum}$ of the four neighbours)**: each interior value is the average of its neighbours (the *five-point formula*).
- **Poisson ($u_{xx}$ + uᵧᵧ = *f*):** uᵢ₊₁,ⱼ + uᵢ₋₁,ⱼ + uᵢ,ⱼ₊₁ + uᵢ,ⱼ₋₁ − 4uᵢⱼ = **$h^{2} f_{ij}$**.

Writing one equation for each interior grid point gives a linear system, with 4 on the diagonal and −1 for each neighbour: diagonally dominant, so the Gauss–Seidel method of Unit 4 converges. Applied to this system, Gauss–Seidel is called **Liebmann's iterative method**: sweep over the grid and replace each value by the average of its neighbours until nothing changes.

## 6.3 Laplace's equation on a square plate

::: example Plate with the top edge held at 100° and the other three edges at 0°
Take a mesh whose interior has $2 \times 2$ points. By symmetry the two top interior points are equal (call them $\ast a \ast$) and the two bottom ones are equal $(\ast b \ast)$. The equations are $4 a = 100 + 0 + a + b$ and $4 b = 0 + 0 + a + b$, since each interior point has two boundary neighbours and two interior ones. Then $3 a - b = 100$ and $3 b - a = 0$; so $a = 3 b$ and $8 b = 100$, giving **$b = 12.5$ and $a = 37.5$**. The computer solution of the four coupled equations is (37.5000, 37.5000, 12.5000, 12.5000), in agreement.
:::

A finer grid has $3 \times 3$ interior points, nine unknowns $u_{ij} ( i$ = row from the top, 1 to $3 ;\  j$ = column, 1 to 3), with the top boundary at 100 and the others 0.

::: example 3 × 3 interior points: direct solution
Solving the $9 \times 9$ linear system exactly gives:

|  | col 1 | col 2 | col 3 |

|---|---|---|---|

| row 1 (from top) | 42.8571 | 52.6786 | 42.8571 |

| row 2 (from top) | 18.7500 | 25.0000 | 18.7500 |

| row 3 (from top) | 7.1429 | 9.8214 | 7.1429 |

The centre value is $25 = \frac{1}{4} (100 + 0 + 0 + 0)$, the average of the four edge temperatures, as the **symmetry** of the problem requires (the centre sees each edge equally). Values decrease downward, away from the hot edge, and are symmetric left to right: $u_{11} = 42.8571 ,\  u_{12} = 52.6786 ,\  u_{21} = 18.7500 ,\  u_{31} = 7.1429 ,\  u_{32} = 9.8214$.
:::

::: example Same problem by Liebmann (Gauss–Seidel) iteration from all zeros
Each sweep replaces every interior value, row by row, by the average of its four current neighbours:

| *k* | $u_{11}$ | $u_{12}$ | $u_{13}$ | $u_{21}$ | $u_{22}$ | $u_{23}$ | $u_{31}$ | $u_{32}$ | $u_{33}$ |

|---|---|---|---|---|---|---|---|---|---|

| 1 | 25.0000 | 31.2500 | 32.8125 | 6.2500 | 9.3750 | 10.5469 | 1.5625 | 2.7344 | 3.3203 |

| 2 | 34.3750 | 44.1406 | 38.6719 | 11.3281 | 17.1875 | 14.7949 | 3.5156 | 6.0059 | 5.2002 |

| 3 | 38.8672 | 48.6816 | 40.8691 | 14.8926 | 21.0938 | 16.7908 | 5.2246 | 7.8796 | 6.1676 |

| 4 | 40.8936 | 50.7141 | 41.8762 | 16.8030 | 23.0469 | 17.7727 | 6.1707 | 8.8463 | 6.6547 |

| 5 | 41.8793 | 51.7006 | 42.3683 | 17.7742 | 24.0234 | 18.2616 | 6.6551 | 9.3333 | 6.8987 |

| 8 | 42.7351 | 52.5565 | 42.7961 | 18.6279 | 24.8779 | 18.6890 | 7.0818 | 9.7604 | 7.1123 |

After eight sweeps the largest difference from the exact solution is 0.1221. Each additional sweep multiplies the error by roughly a constant factor below one; a $100 \times 100$ grid would need many hundreds of sweeps, which is why practical codes use successive over-relaxation (SOR) or multigrid.
:::

**Other boundary conditions.** If part of the boundary is **insulated** ($\frac{\partial u}{\partial n} = 0$, a *Neumann* condition), a ghost point outside the grid is introduced with the value of its mirror image inside, so the neighbour sum doubles one interior term. On irregular boundaries, special difference formulas with unequal spacing are used.

## 6.4 Poisson's equation

::: example ∇²u = −10(x² + y² + 10) on the square 0 ≤ x, y ≤ 3, u = 0 on the boundary, h = 1
The interior grid points are (1, 1), (2, 1), (1, 2), (2, 2). The right-hand sides are $f (1 ,\  1) = - 120 ,\  f (2 ,\  1) = - 150 ,\  f (1 ,\  2) = - 150 ,\  f (2 ,\  2) = - 180$. With $h = 1$ the difference equation $4 u_{ij}$ − (neighbours) = $- h^{2} f$ gives right-hand sides 120, 150, 150, 180 for the four points in that order. Unknowns $u_{1} = u (1 ,\  1) ,\  u_{2} = u (2 ,\  1) ,\  u_{3} = u (1 ,\  2) ,\  u_{4} = u (2 ,\  2)$:

- $4 u_{1} - u_{2} - u_{3} = 120$
- $- u_{1} + 4 u_{2} - u_{4} = 150$
- $- u_{1} + 4 u_{3} - u_{4} = 150$
- $- u_{2} - u_{3} + 4 u_{4} = 180$

The solution (verified by substitution in all four equations) is $u (1 ,\  1) = 67.5000 ,\  u (2 ,\  1) = 75.0000 ,\  u (1 ,\  2) = 75.0000 ,\  u (2 ,\  2) = 82.5000$. For example, $4 (67.5) - 75 - 75 = 120$ ✓ and $4 (82.5) - 75 - 75 = 180$ ✓. The symmetry about the diagonal $(u_{2} = u_{3})$ lets you reduce the system to three equations by hand.

Gauss–Seidel from zero ($u_{1} ,\  u_{2} ,\  u_{3} ,\  u_{4}$ updated in turn):

| *k* | $u_{1}$ | $u_{2}$ | $u_{3}$ | $u_{4}$ |

|---|---|---|---|---|

| 1 | 30.0000 | 45.0000 | 45.0000 | 67.5000 |

| 2 | 52.5000 | 67.5000 | 67.5000 | 78.7500 |

| 3 | 63.7500 | 73.1250 | 73.1250 | 81.5625 |

| 4 | 66.5625 | 74.5312 | 74.5312 | 82.2656 |

| 5 | 67.2656 | 74.8828 | 74.8828 | 82.4414 |

The iterates approach (67.5000, 75.0000, 75.0000, 82.5) steadily.
:::

## 6.5 Accuracy and practical notes

- The difference equations are accurate to $O (h^{2})$; halving *h* quarters the truncation error but quadruples the number of unknowns.
- Direct solution (Gauss elimination, banded LU) costs more memory than iteration for large grids; iterative methods exploit the sparsity (only five nonzeros per row).
- For **parabolic** (heat) problems, the explicit scheme $u_{i}^{j+1} = r u_{i-1}^{j} + (1 - 2 r) u_{i}^{j} + r u_{i+1}^{j}$ with $r = \frac{c^{2} \Delta t}{h^{2}}$ is stable only if $r \leq \frac{1}{2}$; the implicit Crank–Nicolson scheme is stable for all *r*. Hyperbolic problems need the Courant condition $\frac{c \Delta t}{h} \leq 1$. These are outside the syllabus but explain why time-dependent problems need more care than the steady-state ones here.

## 6.6 Seeing the ideas: the five-point stencil, the solved plate and Gauss-Seidel on the grid

A cup of coffee loses heat to its surroundings; the temperature inside any object settles to a smooth pattern once its boundaries are held steady. That settled pattern obeys Laplace's equation, and the grid methods of this unit compute it.

```photogrid label="6.1" cols="2" ratio="1.2" caption="Heat and the grid. (a) A steaming cup of coffee: heat flows from hot to cold, and once the surfaces are held at fixed temperatures the interior settles to a steady pattern described by Laplace's equation. (b) The five-point stencil: the temperature at a grid point is the average of its four neighbours (plus a source term for Poisson's equation)."
@ photo id="bca104/coffee" cap="Heat flowing out of a cup"
fit 1.2
focus 0.5 0.5
@ svg cap="Five-point stencil"
f = Fig(300, 240)
f.circle(150, 120, 20, fill=ROSE, stroke=RED, label="u(i,j)", size=9)
for (x, y, t) in [(150, 52, "u(i,j+1)"), (150, 188, "u(i,j-1)"), (62, 120, "u(i-1,j)"), (238, 120, "u(i+1,j)")]:
    f.circle(x, y, 22, fill=BLUE, stroke=NAVY, label=t, size=8)
    f.line(150, 120, x, y, color=SLATE, sw=1.5)
f.text(150, 226, "u(i,j) = [N + S + E + W] / 4", size=10.5, color=TEAL, bold=True)
```

```svgfig label="6.1" caption="A square plate with the top edge held at 100 degrees and the other three edges at 0. The nine interior values from the five-point formula are shown in the cells; the centre is exactly one quarter of the top temperature (25), as symmetry requires."
f = Fig(580, 272)
V = [[42.857, 52.679, 42.857], [18.75, 25.0, 18.75], [7.143, 9.821, 7.143]]
x0, y0, s = 150, 60, 56
for j in range(5): f.box(x0 + j * s - s, y0 - s, s, s * 0.6, "100", fill=ROSE, stroke=RED, size=10, bold=True)
for i in range(3):
    f.box(x0 - s, y0 + i * s, s * 0.6, s, "0", fill=BLUE, stroke=NAVY, size=10, bold=True)
    f.box(x0 + 3 * s + s * 0.4, y0 + i * s, s * 0.6, s, "0", fill=BLUE, stroke=NAVY, size=10, bold=True)
    for j in range(3):
        v = V[i][j]
        f.box(x0 + j * s, y0 + i * s, s, s, "%.3f" % v, fill=["#fee2e2", "#fef3c7", "#e0f2fe"][i], stroke=SLATE, size=11, bold=True)
for j in range(5): f.box(x0 + j * s - s, y0 + 3 * s + 4, s, s * 0.35, "0", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.text(480, 90, "hot edge 100", size=10.5, color=RED, bold=True)
f.text(480, 140, "other edges 0", size=10.5, color=NAVY, bold=True)
f.text(480, 190, "heat flows downwards", size=10, color=SLATE)
```

```svgfig label="6.2" caption="Gauss-Seidel iteration on the plate, starting from zero. The top-centre value u12 (red) and the centre value u22 (teal) approach their exact values 52.679 and 25 over successive sweeps: 31.25, 44.14, 48.68, 50.71, 51.70 and 9.38, 17.19, 21.09, 23.05, 24.02."
f = Fig(580, 200)
ax = Axes(f, 50, 14, 510, 150, (0.5, 5.5), (0, 60))
ax.grid(1, 10)
ax.axes("", "")
A = [31.25, 44.14, 48.68, 50.71, 51.70]; B = [9.38, 17.19, 21.09, 23.05, 24.02]
for S, c in ((A, RED), (B, TEAL)):
    for k in range(4): ax.curve(lambda t, k=k, S=S: S[k] + (S[k + 1] - S[k]) * (t - k - 1), k + 1, k + 2, color=c, sw=2.4)
    for k, v in enumerate(S): ax.pt(k + 1, v, "", color=c)
ax.hline(52.679, color=RED); ax.hline(25, color=TEAL)
f.text(130, 40, "u12 exact 52.679", size=10, color=RED, bold=True)
f.text(130, 120, "u22 exact 25", size=10, color=TEAL, bold=True)
f.text(306, 190, "Gauss-Seidel sweep number", size=10, color=SLATE)
```

### 6.6.1 Eight uses of Laplace and Poisson equations

1. **Steady heat in a plate or wall.** After enough time the temperature in a wall stops changing and obeys Laplace's equation. Engineers use grid methods to estimate heat loss through brick walls and cooling fins of electronics. This helps in designing warm houses for the Nepali hills.
2. **Electric potential.** The voltage in the empty space between conductors satisfies Laplace's equation. The grid method gives the potential around chips, cables and insulators. Designers find where the field is strongest and sparks may occur.
3. **Groundwater and seepage.** Water moving slowly through soil under a $d a m$ follows Laplace's equation. The solution shows the pressure and the flow paths. Dam designers use it to avoid leaks and failure.
4. **Fluid flow.** Ideal flow of a fluid around a pipe bend or a bridge pier can be described by a potential that satisfies Laplace's equation. The grid solution shows speed and pressure. It is the first step before more advanced models.
5. **Poisson's equation and charge.** If charges or heat sources are present, the equation becomes Poisson's equation. The source term is added to the stencil. Computing the field of a charged body or heat inside an electronic part uses it.
6. **Deflection of membranes and plates.** The shape of a stretched drum skin under pressure satisfies Poisson's equation. A civil engineer can estimate how a thin slab bends under a load. The same equation appears in many different fields.
7. **Image processing.** Filling a hole in a photograph can be done by solving Laplace's equation with the edge of the hole as the boundary. The result blends smoothly with its surroundings. Photo-editing tools use this idea.
8. **Teaching and checking bigger programs.** A simple plate with known boundary values has a solution one can verify by symmetry, as in the exercise here. It is the standard test for larger simulation software. Learning it builds the habit of checking results.

```photogrid label="6.2" cols="2" ratio="1.4" caption="Halve the mesh, quarter the error. (a) A thermal image: temperature across a surface is a field that satisfies Laplace's equation when nothing heats or cools the inside. (b) The unit square has $u = \sin (p i x)$ on the top edge and $u = 0$ on the other three, so the exact value at the centre is $\frac{1}{2 \cosh \left( \frac{p i}{2} \right)} = 0.19927$. The five-point scheme, solved exactly as a linear system, gives 0.25000 for 2 *x* 2 cells, 0.21339 for 4 $x 4$, 0.20292 for 8 $x 8$, 0.20019 for 16 *x* 16 and 0.19950 for 32 $x 32$, with errors 5.1e-2, 1.4e-2, 3.7e-3, 9.2e-4 and 2.3e-4. Each halving of *h* shrinks the error by a factor close to 4, because the scheme is second-order accurate (error proportional to *h* squared). The price is a system four times larger each time."
@ photo id="bcanm/thermal" cap="A thermal image: a temperature field"
fit 1.4
focus 0.5 0.5
@ svg cap="Centre-point error of the five-point scheme"
import numpy as np
def lap(N):
    h = 1.0 / N; n = N - 1; A = np.zeros((n * n, n * n)); b = np.zeros(n * n)
    for i in range(n):
        for j in range(n):
            k = i * n + j; A[k, k] = 4
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ii, jj = i + di, j + dj
                if 0 <= ii < n and 0 <= jj < n: A[k, ii * n + jj] = -1
            if j == n - 1: b[k] += np.sin(np.pi * (i + 1) * h)
    return np.linalg.solve(A, b).reshape(n, n)
ex = 1 / (2 * np.cosh(np.pi / 2)); assert round(float(ex), 5) == 0.19927
Ns = [2, 4, 8, 16, 32]; val = [float(lap(N)[N // 2 - 1, N // 2 - 1]) for N in Ns]; er = [abs(v - ex) for v in val]
assert [round(v, 5) for v in val] == [0.25, 0.21339, 0.20292, 0.20019, 0.1995]
assert all(3.5 < er[i] / er[i + 1] < 4.1 for i in range(4))
f = Fig(300, 240)
f.text(150, 14, "error at the centre, longer bar = smaller", size=10.5, color=NAVY, bold=True)
for i, (N, e) in enumerate(zip(Ns, er)):
    y = 28 + i * 34
    f.text(10, y + 11, f"{N} x {N}", size=10.5, color=NAVY, anchor="start", bold=True, vmid=True)
    w = 48 * (-np.log10(e) )
    f.box(62, y, w, 20, "", fill="#1d6fb8", stroke=NAVY, r=0, sw=1)
    f.text(62 + w + 5, y + 11, f"{e:.1e}", size=10.5, color=NAVY, anchor="start", bold=True, vmid=True)
f.text(150, 206, "exact centre value 0.19927", size=10.5, color=SLATE)
f.text(150, 224, "ratio per halving: 3.6, 3.9, 4.0, 4.0", size=10.5, color=TEAL, bold=True)
```

## Formula and fact sheet

- uₓₓ ≈ (uᵢ₊₁,ⱼ − 2uᵢⱼ + uᵢ₋₁,ⱼ)/h².
- Laplace: uᵢⱼ = ¼(uᵢ₊₁,ⱼ + uᵢ₋₁,ⱼ + uᵢ,ⱼ₊₁ + uᵢ,ⱼ₋₁).
- Poisson: uᵢ₊₁,ⱼ + uᵢ₋₁,ⱼ + uᵢ,ⱼ₊₁ + uᵢ,ⱼ₋₁ − 4uᵢⱼ = h² fᵢⱼ.
- Classification by $B^{2}$ − 4AC: < 0 elliptic, = 0 parabolic, > 0 hyperbolic.
- Liebmann = Gauss–Seidel on the grid.

## Chapter summary

- Elliptic PDEs such as Laplace's and Poisson's equations describe steady states and are determined by their boundary values.
- Replacing derivatives by central differences turns the PDE into one algebraic equation per grid point: the value is the average of its neighbours (Laplace) plus a source term (Poisson).
- The resulting diagonally dominant system is solved directly or by Liebmann's iteration.

## Practice

1. Classify $u_{xx}$ + uᵧᵧ = $0 ,\  u_{t} = u_{xx}$ and $u_{tt} = u_{xx}$.
2. Derive the five-point difference formula for Laplace's equation.
3. A square plate has its top edge at $100 ^{\circ}$ and the other edges at $0 ^{\circ}$. Using a mesh with four interior points, find the temperatures.
4. Do two Liebmann sweeps for the $3 \times 3$ interior problem starting from zero, in row order, and compare with the exact solution.
5. Write the difference equations for $\nabla^{2} u = - 10 (x^{2} + y^{2} + 10)$ with $h = 1$ on $[0 ,\  3] \times [0 ,\  3] ,\  u = 0$ on the boundary, and solve them.
6. Why is the Gauss–Seidel iteration guaranteed to converge for the five-point system?
7. Explain what changes in the difference equation at an insulated edge.
8. What is the effect of halving *h* on the accuracy and on the size of the system?

::: note Answers and worked solutions
**1.** $u_{xx}$ + uᵧᵧ = 0: $A = 1 ,\  B = 0 ,\  C = 1 ,\  B^{2}$ − 4AC = $- 4 < 0$: elliptic. $u_{t} = u_{xx}$: only one second-derivative term, $B^{2}$ − 4AC = 0: parabolic. $u_{tt} = u_{xx}$: $A = 1 ,\  C = - 1 ,\  B^{2}$ − 4AC = $4 > 0$: hyperbolic.

**2.** Using uₓₓ ≈ (uᵢ₊₁,ⱼ − 2uᵢⱼ + uᵢ₋₁,ⱼ)/h² and the same for $y ,\  u_{xx}$ + uᵧᵧ = 0 gives uᵢ₊₁,ⱼ + uᵢ₋₁,ⱼ + uᵢ,ⱼ₊₁ + uᵢ,ⱼ₋₁ − 4uᵢⱼ = 0 and so $u_{ij} = \frac{1}{4} ( \mathrm{sum}$ of neighbours).

**3.** Top interior points 37.5, bottom interior points 12.5 (full solution (37.5000, 37.5000, 12.5000, 12.5000)); derivation in Section 6.3.

**4.** The first rows of the Liebmann table in Section 6.3 are the answers for sweeps 1 and 2; they are still far from the exact values $(u_{22} = 25.0000 ,\  u_{12} = 52.6786)$, which are reached after about eight sweeps to within 0.1221.

**5.** The four equations in Section 6.4; solution $u (1 ,\  1) = 67.5000 ,\  u (2 ,\  1) = 75.0000 ,\  u (1 ,\  2) = 75.0000 ,\  u (2 ,\  2) = 82.5000$.

**6.** The matrix has 4 on the diagonal and at most four $- 1 s$ per row, so it is (weakly) diagonally dominant, and irreducibly so because every interior point is connected to a boundary point. This guarantees convergence of both Jacobi and Gauss–Seidel.

**7.** The normal derivative is zero, so the ghost value outside the edge equals the value inside; the neighbour sum includes twice the interior neighbour, e.g. 4uᵢⱼ = 2uᵢ,ⱼ₊₁ + uᵢ₊₁,ⱼ + uᵢ₋₁,ⱼ.

**8.** Truncation error falls by about 4 $(O (h^{2}))$; the number of unknowns grows by 4, and the work of an iterative solver by more (the iterations needed also increase).
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). A square plate has its top edge at 100 degrees and the other three edges at 0 degrees. Find the temperatures at the nine interior points of a 4 *x* 4 mesh using the five-point formula and symmetry.**

*Formula.* For Laplace's equation, $u (i ,\  j) = \frac{u (i + 1 ,\  j) + u (i - 1 ,\  j) + u (i ,\  j + 1) + u (i ,\  j - 1)}{4}$. By left-right symmetry, name the unknowns: top row $a ,\  b ,\  a$; middle row $c ,\  d ,\  c$; bottom row $e ,\  f ,\  e$.

*Equations.* $a = \frac{100 + b + c}{4} ;\  b = \frac{100 + 2 a + d}{4} ;\  c = \frac{a + e + d}{4} ;\  d = \frac{b + f + 2 c}{4} ;\  e = \frac{c + f}{4} ;\  f = \frac{d + 2 e}{4}$. Solving gives **$a = 42.857 ,\  b = 52.679 ,\  c = 18.750 ,\  d = 25.000 ,\  e = 7.143 ,\  f = 9.821$**.

*Check.* a: $\frac{100 + 52.679 + 18.75}{4} = 42.857$. *d*: $\frac{52.679 + 9.821 + 37.5}{4} = 25$. The centre is one quarter of 100, as superposition of the four edges (each contributing 25 at the centre by symmetry) requires (Figure 6.1). *Conclusion:* temperature falls smoothly from the hot edge towards the cold edges.

**Q2 (5 marks). Explain how the Gauss-Seidel iteration is used for the plate problem. Show its early progress.**

*Method.* Start with a guess (all zeros) and sweep through the grid, replacing each interior value by the average of its four neighbours using the newest values; repeat until changes are below a tolerance. The system is diagonally dominant (each unknown has coefficient 4 against four neighbours of 1), so convergence is guaranteed.

| Sweep | u12 (top centre) | u22 (centre) |
|---|---|---|
| 1 | 31.25 | 9.38 |
| 2 | 44.14 | 17.19 |
| 3 | 48.68 | 21.09 |
| 4 | 50.71 | 23.05 |
| 5 | 51.70 | 24.02 |
| Exact | 52.679 | 25.000 |

The error shrinks by a factor of about two each sweep here (Figure 6.2). *Speed-up:* successive over-relaxation (SOR) with a factor between 1 and 2 converges much faster on fine grids. *Conclusion:* iterative solution is the practical way to solve large grids.

**Q3 (10 marks). Classify second-order partial differential equations. Derive the difference equations for Laplace's and Poisson's equations and explain how a Dirichlet problem is solved numerically.**

*Classification.* For A $u_{x} x + B u_{x} y + C u_{y} y$ + lower terms = 0, the sign of $B^{2}$ - 4AC decides the type: **elliptic** if negative (Laplace $u_{x} x + u_{y} y = 0$, Poisson $u_{x} x + u_{y} y = f$; steady state), **parabolic** if zero (heat $u_{t} = c^{2} u_{x} x$; diffusion in time), **hyperbolic** if positive (wave $u_{t} t = c^{2} u_{x} x$; vibration). This unit treats the elliptic type.

*Difference equations.* Cover the region with a grid of spacing *h*. Taylor series give $u_{x} x$ is about $\frac{u (i + 1 ,\  j) - 2 u (i ,\  j) + u (i - 1 ,\  j)}{h^{2}}$ and likewise for $u_{y} y$, with error $O (h^{2})$. Adding them gives for **Laplace**: $u (i ,\  j) = \frac{u (i + 1 ,\  j) + u (i - 1 ,\  j) + u (i ,\  j + 1) + u (i ,\  j - 1)}{4}$, the average of the four neighbours (the stencil of Plate 6.1). For **Poisson**: $u (i ,\  j)$ = [sum of four neighbours - $h^{2} f (i ,\  j) ] / 4$.

*Dirichlet problem.* The values of *u* on the boundary are given. Each interior point gives one linear equation, so an $n x n$ interior grid gives $n^{2}$ equations (nine for the 3 *x* 3 plate of Figure 6.1). They are solved by Gauss elimination or by iteration (Gauss-Seidel, SOR; Figure 6.2), the latter being preferred for fine grids.

*Worked Poisson example.* For $u_{x} x + u_{y} y = - 10$ on a square with $u = 0$ on all edges and $h = 1$, the single interior point of a 3 *x* 3 grid has 4u = $0 + 0 + 0 + 0 - h^{2} (- 10)$, so **$u = 2.5$**. Halving *h* gives a more accurate answer with more points.

| Type | Example | Physical meaning | Numerical idea |
|---|---|---|---|
| Elliptic | Laplace, Poisson | steady state | solve a system on the grid |
| Parabolic | Heat equation | diffusion | step in time (explicit, Crank-Nicolson) |
| Hyperbolic | Wave equation | vibration | step in time with a stability limit |

*Accuracy.* The error is $O (h^{2})$; halving *h* cuts it to about a quarter but multiplies the number of unknowns by four. Corner and curved boundaries need special treatment. *Conclusion.* Elliptic problems reduce to large sparse linear systems that links this unit to Unit 4; symmetry checks and a convergence test on the sweeps make the answers trustworthy.
