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
- The heat equation (explicit and Crank-Nicolson), the wave equation, stability conditions, insulated edges, the diagonal formula and SOR.
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
- For **parabolic** (heat) problems, the explicit scheme $u_{i}^{j+1} = r u_{i-1}^{j} + (1 - 2 r) u_{i}^{j} + r u_{i+1}^{j}$ with $r = \frac{c^{2} \Delta t}{h^{2}}$ is stable only if $r \leq \frac{1}{2}$; the implicit Crank–Nicolson scheme is stable for all *r*. Hyperbolic problems need the Courant condition $\frac{c \Delta t}{h} \leq 1$. They are developed in Sections 6.7 to 6.9 because they explain why time-dependent problems need more care than the steady-state ones.

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

## 6.7 Parabolic equations: the heat equation by the explicit method

Section 6.1 listed three types; Sections 6.2 to 6.6 solved the elliptic one. A **parabolic** equation describes diffusion in time, and the model is the one-dimensional **heat equation**

$$\frac{\partial u}{\partial t} = c^{2}\,\frac{\partial^{2} u}{\partial x^{2}},\qquad 0 < x < L,\ t > 0,$$

with an **initial condition** $u(x, 0) = g(x)$ and **boundary conditions** such as $u(0, t) = u(L, t) = 0$ (the ends of a thin bar held at zero). Unlike Laplace's equation, the values are not all solved together: the solution is found **row by row in time**, each row from the previous one, like the marching methods of Unit 5.

**Difference equation.** Use a grid $x_i = ih$ and $t_j = jk$ and write $u_i^{j} = u(x_i, t_j)$. Replace $u_t$ by the forward difference (error $O(k)$) and $u_{xx}$ by the central difference (error $O(h^{2})$):

$$\frac{u_i^{j+1} - u_i^{j}}{k} = c^{2}\,\frac{u_{i-1}^{j} - 2u_i^{j} + u_{i+1}^{j}}{h^{2}}.$$

Solving for the new value gives the **explicit scheme** (the Schmidt or FTCS formula)

$$u_i^{j+1} = r\,u_{i-1}^{j} + (1 - 2r)\,u_i^{j} + r\,u_{i+1}^{j},\qquad r = \frac{c^{2}k}{h^{2}}.$$

Each new value is a weighted average of three old values: nothing has to be solved, which makes the method easy to program or to run by hand. For the special choice **$r = \frac{1}{2}$** (the **Bender-Schmidt formula**) the middle term vanishes and $u_i^{j+1} = \frac{1}{2}\,(u_{i-1}^{j} + u_{i+1}^{j})$.

::: example u_t = u_xx, u(x, 0) = sin πx, u(0, t) = u(1, t) = 0, with h = 0.1 and r = 1/2 (so k = 0.005)
The exact solution is $u = e^{-\pi^{2}t}\sin \pi x$: the shape stays a sine and its height decays. The scheme gives, for the left half of the bar (the right half is the mirror image):

| *t* | $x = 0.1$ | 0.2 | 0.3 | 0.4 | 0.5 | exact at $x = 0.5$ |
|---|---|---|---|---|---|---|
| 0 | 0.3090 | 0.5878 | 0.8090 | 0.9511 | 1.0000 | 1.0000 |
| 0.005 | 0.2939 | 0.5590 | 0.7694 | 0.9045 | 0.9511 | 0.9518 |
| 0.010 | 0.2795 | 0.5317 | 0.7318 | 0.8602 | 0.9045 | 0.9060 |
| 0.015 | 0.2658 | 0.5056 | 0.6959 | 0.8181 | 0.8602 | 0.8624 |
| 0.020 | 0.2528 | 0.4809 | 0.6619 | 0.7781 | 0.8181 | 0.8209 |

The first entry of the second row is $\frac{1}{2}(0 + 0.5878) = 0.2939$, the next $\frac{1}{2}(0.3090 + 0.8090) = 0.5590$, and so on. After 20 steps ($t = 0.1$) the value at the middle is 0.36654 against the exact 0.37271, an error of 0.0062 (1.7%).
:::

**Accuracy and the special value $r = 1/6$.** The local error of the explicit scheme is $O(k) + O(h^{2})$. Expanding both differences in Taylor series, the leading error term is proportional to $\frac{h^{2}}{12}\,(1 - 6r)\,u_{xxxx}$. For $r = 1/6$ it cancels and the error becomes $O(h^{4})$ (with $k = h^{2}/6$). The same example at $t = 0.1$:

| *r* | Step $k$ | Number of steps | $u(0.5,\ 0.1)$ | Error |
|---|---|---|---|---|
| 1/2 | 0.005 | 20 | 0.366544 | 6.2e-03 |
| 1/4 | 0.0025 | 40 | 0.371188 | 1.5e-03 |
| 1/6 | 0.001667 | 60 | 0.372715 | 6.7e-06 |

Smaller $r$ is more accurate but needs more time steps; $r = 1/6$ is the best compromise and a thousand times better than $r = 1/2$ at three times the cost.

**Stability: why $r \le \frac{1}{2}$.** The weights $r$, $1 - 2r$, $r$ add up to 1. If $r \le \frac{1}{2}$ all three are non-negative, each new value is an average of old ones and cannot exceed their maximum: errors cannot grow. If $r > \frac{1}{2}$ the middle weight is negative and a zig-zag error pattern is *multiplied* at every step by $|1 - 4r| > 1$ (for the worst, alternating pattern). This is the same phenomenon as the Euler instability of Section 5.10.

::: example What happens with r = 0.6 (k = 0.006), the same problem with a small bump of size 0.001 added at x = 0.5
The true solution decays, so the largest value should fall steadily to about 0.03 by step 60. The computed maximum is 0.37 after 20 steps, **25** after 40 steps and **8953** after 60: the bump has grown into a violent oscillation that swamps the solution. Taking a larger time step to save work therefore does not save anything; the step is limited by $k \le \frac{h^{2}}{2c^{2}}$, and halving $h$ forces **four** times as many time steps.
:::

## 6.8 The implicit Crank-Nicolson method

The restriction $k \le \frac{h^{2}}{2c^{2}}$ is painful: for fine grids the time step becomes tiny. The **Crank-Nicolson** method averages the space difference at the old and the new time level, which is the trapezoidal idea of Section 3.2 applied in time:

$$\frac{u_i^{j+1} - u_i^{j}}{k} = \frac{c^{2}}{2}\left[\frac{u_{i-1}^{j+1} - 2u_i^{j+1} + u_{i+1}^{j+1}}{h^{2}} + \frac{u_{i-1}^{j} - 2u_i^{j} + u_{i+1}^{j}}{h^{2}}\right].$$

Collecting the unknown (new) values on the left:

$$-r\,u_{i-1}^{j+1} + (2 + 2r)\,u_i^{j+1} - r\,u_{i+1}^{j+1} = r\,u_{i-1}^{j} + (2 - 2r)\,u_i^{j} + r\,u_{i+1}^{j}.$$

The right side is known, so every row needs the solution of a **tridiagonal linear system** (the elimination of Section 4.8, cost proportional to the number of points), which is why the method is called *implicit*. Its error is $O(k^{2}) + O(h^{2})$ and, more important, it is **stable for every $r$** (unconditionally stable), so $k$ can be chosen for accuracy alone.

::: example The same bar with Crank-Nicolson at r = 1 (k = 0.01)
The nine unknowns $u_1, \ldots, u_9$ at $t = 0.01$ come from a $9 \times 9$ tridiagonal system with 4 on the diagonal and $-1$ beside it. The first time step gives

| *x* | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 |
|---|---|---|---|---|---|
| Crank-Nicolson, $t = 0.01$ | 0.28018 | 0.53293 | 0.73352 | 0.86230 | 0.90668 |
| Exact | 0.27997 | 0.53254 | 0.73298 | 0.86167 | 0.90602 |

and after ten steps ($t = 0.1$) the middle value is 0.375442 against the exact 0.372708 (error 0.0027, less than half of the explicit error 0.0062 for $r = 1/2$, with **ten** steps instead of twenty).

With the huge value $r = 5$ ($k = 0.05$, only **two** steps to $t = 0.1$) the scheme still works: $u(0.5, 0.1) = 0.36819$, error 0.0045, whereas the explicit scheme would have blown up by a factor of $|1 - 4r| = 19$ per step.
:::

**Choosing between them.**

| | Explicit (FTCS) | Crank-Nicolson |
|---|---|---|
| Work per step | a few operations per point | one tridiagonal solve (about 8 operations per point) |
| Stability | only if $r \le \frac{1}{2}$ | for every $r$ |
| Order | $O(k) + O(h^{2})$ | $O(k^{2}) + O(h^{2})$ |
| Best for | coarse grids, hand work, quick experiments | fine grids, long times |

**Other boundary conditions.** If the end of the bar is insulated, $u_x = 0$ there, and the fictitious-point device of Section 6.10 applies. A non-zero boundary temperature simply enters the first and last equations as a known value. A source term gives $u_t = c^{2}u_{xx} + f$ and adds $k f_i^{j}$ to the right side.

## 6.9 Hyperbolic equations: the wave equation

The model is the vibrating string, $\dfrac{\partial^{2} u}{\partial t^{2}} = c^{2}\,\dfrac{\partial^{2} u}{\partial x^{2}}$ for $0 < x < L$, with *two* initial conditions, the shape $u(x, 0) = g(x)$ and the velocity $u_t(x, 0) = v(x)$, and fixed ends $u(0, t) = u(L, t) = 0$. Disturbances travel at speed $c$ and, unlike heat, do not die out by themselves.

Central differences in both variables give

$$\frac{u_i^{j+1} - 2u_i^{j} + u_i^{j-1}}{k^{2}} = c^{2}\,\frac{u_{i-1}^{j} - 2u_i^{j} + u_{i+1}^{j}}{h^{2}},$$

that is, with the **Courant number** $r = \dfrac{ck}{h}$,

$$u_i^{j+1} = 2\,(1 - r^{2})\,u_i^{j} + r^{2}\,(u_{i-1}^{j} + u_{i+1}^{j}) - u_i^{j-1}.$$

The scheme uses *two* previous time levels, so the first step needs a special formula. With zero initial velocity the central-difference version $u_i^{-1} = u_i^{1}$ gives

$$u_i^{1} = u_i^{0} + \frac{r^{2}}{2}\,(u_{i-1}^{0} - 2u_i^{0} + u_{i+1}^{0}),$$

and with initial velocity $v_i$ one adds $k\,v_i$.

**Stability: the Courant (CFL) condition $r \le 1$.** The numerical scheme must be able to "see" the information that the true wave carries. In one time step the wave moves $ck$, while the scheme at point $i$ only uses neighbours at distance $h$. If $ck > h$ the true solution depends on data outside what the scheme uses, and the scheme goes unstable; for $r \le 1$ it is stable.

::: example u_tt = u_xx, u(x, 0) = sin πx, u_t(x, 0) = 0, ends fixed, h = 0.1 (the exact solution is cos πt · sin πx)
**Case r = 1 (k = 0.1).** The formula becomes $u_i^{j+1} = u_{i-1}^{j} + u_{i+1}^{j} - u_i^{j-1}$. The middle value and its neighbours are:

| *t* | $x = 0.1$ | 0.2 | 0.3 | 0.4 | 0.5 | exact at $x = 0.5$ |
|---|---|---|---|---|---|---|
| 0 | 0.3090 | 0.5878 | 0.8090 | 0.9511 | 1.0000 | 1.0000 |
| 0.1 | 0.2939 | 0.5590 | 0.7694 | 0.9045 | 0.9511 | 0.9511 |
| 0.2 | 0.2500 | 0.4755 | 0.6545 | 0.7694 | 0.8090 | 0.8090 |
| 0.3 | 0.1816 | 0.3455 | 0.4755 | 0.5590 | 0.5878 | 0.5878 |
| 0.4 | 0.0955 | 0.1816 | 0.2500 | 0.2939 | 0.3090 | 0.3090 |
| 0.5 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

At $r = 1$ the numbers agree with the exact solution to all four decimals shown (for this equation $r = 1$ makes the scheme exact for sine waves, because the numerical and true domains of dependence coincide). The string is flat at $t = 0.5$ and then moves to the negative side.

**Case r = 0.5 (k = 0.05).** Stable but less accurate: at $t = 0.5$ the middle point is 0.0049 instead of 0. **Case r = 0.8:** at $t = 0.8$ the value is $-0.8068$ against $-0.8090$.

**Case r = 1.1** (beyond the Courant limit). Add a tiny 0.001 ripple of high frequency: the largest value grows to 2.7 after 10 steps, $7.4 \times 10^{3}$ after 20, $2.9 \times 10^{7}$ after 30. With $r = 1$ the same ripple stays at 0.001 for as long as we compute, and with $r = 0.9$ the solution stays bounded.
:::

Notice the contrast of the three types. **Elliptic** problems need the whole region solved together (a linear system for all points). **Parabolic** problems march in time with a stability limit $r \le \frac{1}{2}$ unless an implicit method is used. **Hyperbolic** problems march in time with the milder limit $r \le 1$ and, since the waves do not decay, accumulated numerical errors do not fade either: they must be kept small by the choice of $h$ and $k$.

## 6.10 Derivative boundary conditions and the diagonal formula

**Insulated and sloping edges.** So far the temperature was given on every edge (a Dirichlet problem). On an insulated edge no heat crosses, so instead the normal derivative is zero (a **Neumann** condition, $u_x = 0$), and in general $u_x = \gamma$ may be prescribed. The edge values are now **unknowns**, and the trick is the **fictitious point**: imagine the grid continued one step beyond the edge. For an edge at $x = 0$ the central difference $\dfrac{u_{1,j} - u_{-1,j}}{2h} = \gamma$ gives $u_{-1,j} = u_{1,j} - 2h\gamma$. The five-point equation at an edge point then involves the ghost value, which is replaced by the formula above:

$$4u_{0,j} = 2u_{1,j} + u_{0,j+1} + u_{0,j-1} - 2h\gamma \qquad(\gamma = 0:\ \text{insulated, the ghost equals the mirror image}).$$

::: example Rectangular plate, 3 units wide and 4 units high: top edge 100°, bottom and right edges 0°, left edge insulated (h = 1)
The unknowns are now the three columns $x = 0$ (on the insulated edge), $x = 1$, $x = 2$ in each of three rows, nine unknowns again. At the edge points the equation is $4u_{i,0} = 2u_{i,1} + u_{i-1,0} + u_{i+1,0}$; the other points use the ordinary formula. For the top-left point $4u = 2u_{\text{right}} + 100 + u_{\text{below}}$. The solution is

| row (from the top) | $x = 0$ (insulated) | $x = 1$ | $x = 2$ |
|---|---|---|---|
| 1 | 64.981 | 61.221 | 45.883 |
| 2 | 37.482 | 34.021 | 22.312 |
| 3 | 16.904 | 15.067 | 9.345 |

Check the top-left value: $4 \times 64.981 = 259.92$ and $2 \times 61.221 + 100 + 37.482 = 259.92$. The temperature along the insulated edge is higher than the temperature one step in: since no heat can leave there, the edge behaves as a line of symmetry (it is the right half of a plate twice as wide, with both side edges at 0).
:::

**The diagonal five-point formula.** The Laplace equation is unchanged if the axes are rotated by $45^{\circ}$. In the rotated directions the grid points are the diagonal neighbours, at distance $h\sqrt{2}$, and the same derivation gives

$$u_{i,j} = \frac{1}{4}\left(u_{i+1,j+1} + u_{i-1,j+1} + u_{i+1,j-1} + u_{i-1,j-1}\right),$$

again with error $O(h^{2})$. It is not used for the final answer but to obtain **good starting values** without solving anything, because the corner values of a mesh are boundary values. The standard procedure for a mesh with four intervals per side (nine interior points):

1. Centre point: average of the four **corner** values of the mesh (its diagonal neighbours two steps away).
2. The four interior corner points: diagonal formula using the nearby boundary corners and the centre.
3. The four mid-side points: ordinary five-point formula using the points just found.
4. Improve by Liebmann sweeps or solve the system.

::: example u = eˣ cos y (a harmonic function) on the unit square, h = 1/4: boundary values taken from the exact function
Centre $(0.5, 0.5)$: the corners are $u(0,0) = 1$, $u(1,0) = 2.7183$, $u(0,1) = 0.5403$, $u(1,1) = 1.4687$, so the diagonal formula gives $\frac{1}{4}(1 + 2.7183 + 0.5403 + 1.4687) = 1.4318$ against the exact 1.4469. One pass of steps 1 to 3 and the full linear solution give:

| Point $(x, y)$ | Exact | After one pass (steps 1-3) | Converged (full solution) |
|---|---|---|---|
| (0.25, 0.25) | 1.24411 | 1.23953 | 1.24471 |
| (0.50, 0.25) | 1.59747 | 1.59154 | 1.59834 |
| (0.75, 0.25) | 2.05119 | 2.04608 | 2.05197 |
| (0.25, 0.50) | 1.12684 | 1.12102 | 1.12757 |
| (0.50, 0.50) | 1.44689 | 1.43182 | 1.44795 |
| (0.75, 0.50) | 1.85784 | 1.85191 | 1.85877 |
| (0.25, 0.75) | 0.93951 | 0.93513 | 0.94003 |
| (0.50, 0.75) | 1.20635 | 1.20049 | 1.20711 |
| (0.75, 0.75) | 1.54899 | 1.54421 | 1.54966 |

One pass is already correct to about two decimals (largest error 0.015 at the centre) and the converged difference solution to three (largest error 0.0011, the $O(h^{2})$ truncation error). Starting Liebmann's iteration from the diagonal values it needs **8** sweeps to change by less than $10^{-4}$, from all zeros **15**.
:::

## 6.11 Faster iteration (SOR) and the accuracy of the grid

**Over-relaxation on the grid.** Liebmann's iteration is Gauss-Seidel (Section 4.4) and it becomes slow on fine grids. **Successive over-relaxation** (Section 4.11) moves each value past the neighbour average:

$$u_{ij}^{\text{new}} = u_{ij}^{\text{old}} + \omega\left(\frac{u_{i+1,j} + u_{i-1,j} + u_{i,j+1} + u_{i,j-1}}{4} - u_{ij}^{\text{old}}\right),\qquad 1 \le \omega < 2.$$

For the square plate with $N$ interior points on each side, the best factor is $\omega_{\text{opt}} = \dfrac{2}{1 + \sin\left(\pi/(N + 1)\right)}$, which tends to 2 as the grid gets finer.

::: example Plate with the top edge at 100°, the others at 0°, stop when the largest change is below 10⁻⁶
| Interior points | Unknowns | $\omega_{\text{opt}}$ | Gauss-Seidel ($\omega = 1$) | SOR with $\omega_{\text{opt}}$ | SOR $\omega = 1.5$ | SOR $\omega = 1.9$ |
|---|---|---|---|---|---|---|
| $3 \times 3$ | 9 | 1.172 | 25 | 13 | 27 | 171 |
| $7 \times 7$ | 49 | 1.446 | 99 | 26 | 28 | 171 |
| $15 \times 15$ | 225 | 1.674 | 365 | 49 | 121 | 168 |

Gauss-Seidel needs about four times as many sweeps each time the grid is halved in spacing (25, 99, 365); with the optimal factor the count only doubles (13, 26, 49). For the finest grid this is a **seven-fold** saving, and the saving grows with the grid. A badly chosen $\omega$ (1.9 for the small grid) is much worse than none.
:::

**Accuracy: halving $h$.** The five-point formula has truncation error $O(h^{2})$. A test with a known answer shows it: Poisson's equation $\nabla^{2}u = -2\pi^{2}\sin\pi x\,\sin\pi y$ on the unit square with $u = 0$ on the edges has the exact solution $u = \sin\pi x\,\sin\pi y$, whose centre value is 1.

| $h$ | Unknowns | Centre value | Error | Ratio to previous error |
|---|---|---|---|---|
| 1/2 | 1 | 1.23370 | 0.23370 | |
| 1/4 | 9 | 1.05303 | 0.05303 | 4.41 |
| 1/8 | 49 | 1.01295 | 0.01295 | 4.09 |
| 1/16 | 225 | 1.00322 | 0.00322 | 4.02 |

Each halving divides the error by about 4, as $O(h^{2})$ predicts, and multiplies the number of unknowns by about 4. **Richardson extrapolation** (Section 3.6) of the two finest results, $\frac{4 \times 1.00322 - 1.01295}{3} = 0.99998$, has an error of only $2.5 \times 10^{-5}$: a cheap way to gain two more digits without a finer grid. For a function whose fourth derivatives vanish, such as $u = x^{2} - y^{2}$, the five-point formula is exact and the computed answer has zero error apart from round-off.

::: key Summary of the three types
| Type | Example | Method | Condition |
|---|---|---|---|
| Elliptic | Laplace, Poisson | solve all grid points together (elimination, Liebmann, SOR) | none, but SOR needs $0 < \omega < 2$ |
| Parabolic | heat | march in time: explicit or Crank-Nicolson | explicit: $r = c^{2}k/h^{2} \le \frac{1}{2}$; CN none |
| Hyperbolic | wave | march in time, two levels | $r = ck/h \le 1$ |
:::

## Formula and fact sheet

- uₓₓ ≈ (uᵢ₊₁,ⱼ − 2uᵢⱼ + uᵢ₋₁,ⱼ)/h².
- Laplace: uᵢⱼ = ¼(uᵢ₊₁,ⱼ + uᵢ₋₁,ⱼ + uᵢ,ⱼ₊₁ + uᵢ,ⱼ₋₁).
- Poisson: uᵢ₊₁,ⱼ + uᵢ₋₁,ⱼ + uᵢ,ⱼ₊₁ + uᵢ,ⱼ₋₁ − 4uᵢⱼ = h² fᵢⱼ.
- Classification by $B^{2}$ − 4AC: < 0 elliptic, = 0 parabolic, > 0 hyperbolic.
- Liebmann = Gauss–Seidel on the grid.
- Heat, explicit: $u_i^{j+1} = r u_{i-1}^{j} + (1 - 2r)u_i^{j} + r u_{i+1}^{j}$, $r = c^{2}k/h^{2} \le \frac{1}{2}$; $r = \frac{1}{6}$ gives $O(h^{4})$-type accuracy; Crank-Nicolson is stable for every $r$.
- Wave: $u_i^{j+1} = 2(1 - r^{2})u_i^{j} + r^{2}(u_{i-1}^{j} + u_{i+1}^{j}) - u_i^{j-1}$, $r = ck/h \le 1$.
- Insulated edge: $4u_{0,j} = 2u_{1,j} + u_{0,j+1} + u_{0,j-1}$. Diagonal formula: $u = \frac{1}{4}$(sum of the four diagonal neighbours).
- SOR on a square: $\omega_{\text{opt}} = 2/(1 + \sin(\pi/(N + 1)))$.

## Chapter summary

- Elliptic PDEs such as Laplace's and Poisson's equations describe steady states and are determined by their boundary values.
- Replacing derivatives by central differences turns the PDE into one algebraic equation per grid point: the value is the average of its neighbours (Laplace) plus a source term (Poisson).
- The resulting diagonally dominant system is solved directly or by Liebmann's iteration, accelerated by over-relaxation.
- Parabolic (heat) and hyperbolic (wave) equations are marched in time; the explicit heat scheme needs $r \le \frac{1}{2}$, the wave scheme $r \le 1$, and Crank-Nicolson is stable for any $r$.

## Practice

1. Classify $u_{xx}$ + uᵧᵧ = $0 ,\  u_{t} = u_{xx}$ and $u_{tt} = u_{xx}$.
2. Derive the five-point difference formula for Laplace's equation.
3. A square plate has its top edge at $100 ^{\circ}$ and the other edges at $0 ^{\circ}$. Using a mesh with four interior points, find the temperatures.
4. Do two Liebmann sweeps for the $3 \times 3$ interior problem starting from zero, in row order, and compare with the exact solution.
5. Write the difference equations for $\nabla^{2} u = - 10 (x^{2} + y^{2} + 10)$ with $h = 1$ on $[0 ,\  3] \times [0 ,\  3] ,\  u = 0$ on the boundary, and solve them.
6. Why is the Gauss–Seidel iteration guaranteed to converge for the five-point system?
7. Explain what changes in the difference equation at an insulated edge.
8. What is the effect of halving *h* on the accuracy and on the size of the system?

9. For $u_t = u_{xx}$ on $0 \le x \le 1$ with $u(x, 0) = 4x(1 - x)$ and $u(0, t) = u(1, t) = 0$, use the Bender-Schmidt formula with $h = 0.25$ ($r = \frac{1}{2}$, $k = 0.03125$) for two time steps.
10. For the heat equation with $c^{2} = 1$ find the largest stable time step of the explicit scheme for $h = 0.2$ and for $h = 0.1$. How do the number of steps for a fixed time compare?
11. Write and solve the Crank-Nicolson equations for the first time step of Question 9 with $h = 0.25$ and $k = 0.0625$ ($r = 1$).
12. For $u_{tt} = u_{xx}$ with $u(x, 0) = \sin\pi x$, $u_t(x, 0) = 0$, fixed ends, $h = 0.25$ and $k = 0.25$, find $u$ at $t = 0.25$ and $t = 0.5$.
13. A string with wave speed $c = 2$ is simulated with $h = 0.1$. What is the largest stable time step? Explain the condition.
14. The edge $x = 0$ of a plate has $u_x = 5$. With $h = 0.5$ write the difference equation for an edge point $u_{0,j}$.
15. A square mesh with four intervals per side has corner boundary values 20, 40, 60 and 80. Find the centre value by the diagonal formula.
16. Compute the optimal SOR factor for a square plate with $3 \times 3$ and with $15 \times 15$ interior points.
17. A five-point solution has error $0.00322$ with $h = \frac{1}{16}$. Estimate the error for $h = \frac{1}{32}$ and the number of unknowns for $h = \frac{1}{32}$.

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

::: note Answers and worked solutions (9 to 17)
**9.** Initial values at $x = 0, 0.25, 0.5, 0.75, 1$: $0, 0.75, 1, 0.75, 0$. Step 1 uses $u_i^{1} = \frac{1}{2}(u_{i-1} + u_{i+1})$: $0.5,\ 0.75,\ 0.5$. Step 2: $0.375,\ 0.5,\ 0.375$. (The exact middle value at $t = 0.0625$ is about 0.557, so with the coarse step $h = 0.25$ the scheme is some 10% low; the error shrinks as $h$ and $k$ shrink, as in Section 6.7.)

**10.** $k \le \frac{h^{2}}{2c^{2}}$: $0.02$ for $h = 0.2$ and $0.005$ for $h = 0.1$. Halving $h$ forces a four-fold smaller step, so four times as many steps for a fixed time, and twice as many points in space: eight times the work.

**11.** $(2 + 2r)u_i^{1} - r u_{i-1}^{1} - r u_{i+1}^{1} = r u_{i-1}^{0} + (2 - 2r)u_i^{0} + r u_{i+1}^{0}$ with $r = 1$: $4u_1 - u_2 = 1$, $-u_1 + 4u_2 - u_3 = 1.5$, $-u_2 + 4u_3 = 1$. By symmetry $u_1 = u_3$, $u_2 = 4u_1 - 1$ and $-2u_1 + 4(4u_1 - 1) = 1.5$, so $u_1 = u_3 = 0.3929$, $u_2 = 0.5714$.

**12.** $r = ck/h = 1$. Initial row $0,\ 0.7071,\ 1,\ 0.7071,\ 0$. First step $u_i^{1} = u_i^{0} + \frac{1}{2}(u_{i-1}^{0} - 2u_i^{0} + u_{i+1}^{0})$: $0.5,\ 0.7071,\ 0.5$ (exact $\cos\frac{\pi}{4}\sin\pi x$). Then $u_i^{2} = u_{i-1}^{1} + u_{i+1}^{1} - u_i^{0}$: $0,\ 0,\ 0$ (the string is flat at $t = 0.5$, as $\cos\frac{\pi}{2} = 0$).

**13.** $r = \frac{ck}{h} \le 1$, so $k \le \frac{h}{c} = 0.05$. In one step the wave travels $ck$; if that is more than one cell $h$ the scheme cannot use the information the true wave carries and becomes unstable.

**14.** The ghost point satisfies $\frac{u_{1,j} - u_{-1,j}}{2h} = 5$, so $u_{-1,j} = u_{1,j} - 5$. Then $4u_{0,j} = u_{-1,j} + u_{1,j} + u_{0,j+1} + u_{0,j-1}$ becomes $4u_{0,j} = 2u_{1,j} + u_{0,j+1} + u_{0,j-1} - 5$.

**15.** $\frac{20 + 40 + 60 + 80}{4} = 50$.

**16.** $\omega_{\text{opt}} = \frac{2}{1 + \sin(\pi/(N + 1))}$: for $N = 3$, $\frac{2}{1 + \sin 45^{\circ}} = 1.172$; for $N = 15$, $\frac{2}{1 + \sin 11.25^{\circ}} = 1.674$.

**17.** Error $O(h^{2})$: about $0.00322/4 = 0.0008$. Interior points per side: 31, so $31^{2} = 961$ unknowns (four times as many as 225, roughly).
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

*Classification.* For $A u_{xx} + B u_{xy} + C u_{yy}$ + lower terms $= 0$, the sign of $B^{2} - 4AC$ decides the type: **elliptic** if negative (Laplace $u_{xx} + u_{yy} = 0$, Poisson $u_{xx} + u_{yy} = f$; steady state), **parabolic** if zero (heat $u_{t} = c^{2} u_{xx}$; diffusion in time), **hyperbolic** if positive (wave $u_{tt} = c^{2} u_{xx}$; vibration). This unit treats the elliptic type first and then the other two (Sections 6.7 to 6.9).

*Difference equations.* Cover the region with a grid of spacing $h$. Taylor series give $u_{xx} \approx \frac{u_{i+1,j} - 2u_{i,j} + u_{i-1,j}}{h^{2}}$ and likewise for $u_{yy}$, with error $O(h^{2})$. Adding them gives for **Laplace**: $u_{i,j} = \frac{u_{i+1,j} + u_{i-1,j} + u_{i,j+1} + u_{i,j-1}}{4}$, the average of the four neighbours (the stencil of Plate 6.1). For **Poisson**: $u_{i,j} = \frac{u_{i+1,j} + u_{i-1,j} + u_{i,j+1} + u_{i,j-1} - h^{2} f_{i,j}}{4}$.

*Dirichlet problem.* The values of *u* on the boundary are given. Each interior point gives one linear equation, so an $n \times n$ interior grid gives $n^{2}$ equations (nine for the $3 \times 3$ plate of Figure 6.1). They are solved by Gauss elimination or by iteration (Gauss-Seidel, SOR; Figure 6.2), the latter being preferred for fine grids.

*Worked Poisson example.* For $u_{xx} + u_{yy} = -10$ on a square with $u = 0$ on all edges and $h = 1$, the single interior point of a $3 \times 3$ grid has $4u = 0 + 0 + 0 + 0 - h^{2}(-10)$, so **$u = 2.5$**. Halving $h$ gives a more accurate answer with more points.

| Type | Example | Physical meaning | Numerical idea |
|---|---|---|---|
| Elliptic | Laplace, Poisson | steady state | solve a system on the grid |
| Parabolic | Heat equation | diffusion | step in time (explicit, Crank-Nicolson) |
| Hyperbolic | Wave equation | vibration | step in time with a stability limit |

*Accuracy.* The error is $O (h^{2})$; halving *h* cuts it to about a quarter but multiplies the number of unknowns by four. Corner and curved boundaries need special treatment. *Conclusion.* Elliptic problems reduce to large sparse linear systems that links this unit to Unit 4; symmetry checks and a convergence test on the sweeps make the answers trustworthy.

**Q4 (5 marks). Derive the explicit difference scheme for the heat equation $u_t = c^{2}u_{xx}$, state its stability condition and solve $u_t = u_{xx}$, $u(x, 0) = 4x(1 - x)$, $u(0, t) = u(1, t) = 0$, for two steps with $h = 0.25$, $k = 0.03125$.**

*Derivation.* Replace $u_t$ by $\frac{u_i^{j+1} - u_i^{j}}{k}$ and $u_{xx}$ by $\frac{u_{i-1}^{j} - 2u_i^{j} + u_{i+1}^{j}}{h^{2}}$. Solving for the new value: $u_i^{j+1} = r u_{i-1}^{j} + (1 - 2r)u_i^{j} + r u_{i+1}^{j}$ with $r = \frac{c^{2}k}{h^{2}}$.

*Stability.* The weights $r$, $1 - 2r$, $r$ sum to 1 and are all non-negative only if $r \le \frac{1}{2}$; then each value is an average of old ones and errors cannot grow. For $r > \frac{1}{2}$ an alternating error is multiplied by $|1 - 4r| > 1$ per step.

*Calculation.* Here $r = \frac{0.03125}{0.0625} = \frac{1}{2}$, so $u_i^{j+1} = \frac{1}{2}(u_{i-1}^{j} + u_{i+1}^{j})$. Initial values at $x = 0, 0.25, 0.5, 0.75, 1$: $0, 0.75, 1, 0.75, 0$.

| $t$ | $x = 0.25$ | $x = 0.5$ | $x = 0.75$ |
|---|---|---|---|
| 0 | 0.75 | 1.00 | 0.75 |
| 0.03125 | 0.50 | 0.75 | 0.50 |
| 0.0625 | 0.375 | 0.50 | 0.375 |

*Conclusion.* The temperature falls everywhere as the bar loses heat through its cold ends; the explicit scheme needs no equation solving but its step is limited by $k \le \frac{h^{2}}{2c^{2}}$.

**Q5 (5 marks). The wave equation $u_{tt} = u_{xx}$ with $u(x, 0) = \sin\pi x$, $u_t(x, 0) = 0$, $u(0, t) = u(1, t) = 0$ is solved with $h = k = 0.25$. Find the values up to $t = 0.5$ and state the condition for stability.**

*Scheme.* With $r = \frac{ck}{h} = 1$: $u_i^{j+1} = u_{i-1}^{j} + u_{i+1}^{j} - u_i^{j-1}$. The first step (zero velocity) is $u_i^{1} = u_i^{0} + \frac{r^{2}}{2}(u_{i-1}^{0} - 2u_i^{0} + u_{i+1}^{0})$.

| $t$ | $x = 0.25$ | $x = 0.5$ | $x = 0.75$ | Exact at $x = 0.5$ |
|---|---|---|---|---|
| 0 | 0.7071 | 1.0000 | 0.7071 | 1.0000 |
| 0.25 | 0.5000 | 0.7071 | 0.5000 | 0.7071 |
| 0.5 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

*Check.* $u_{0.25}(0.25) = 0.7071 + \frac{1}{2}(0 - 1.4142 + 1) = 0.5$; $u_{0.5}(0.5) = 0.5 + 0.5 - 1 = 0$. The exact solution is $\cos(\pi t)\sin(\pi x)$, so for $r = 1$ the scheme reproduces it exactly here.

*Stability.* The Courant condition $r = \frac{ck}{h} \le 1$: the true wave moves $ck$ per step and the scheme can only look one cell $h$ either side. For $r = 1.1$ a ripple of 0.001 grows to about 2.7 within 10 steps and $10^{7}$ within 30.

**Q6 (10 marks). Classify the heat, wave and Laplace equations and compare the numerical methods for them, including stability, with the examples of this unit.**

*Classification.* By the sign of $B^{2} - 4AC$: Laplace ($u_{xx} + u_{yy} = 0$) is **elliptic**, since $B^{2} - 4AC = -4$; the heat equation ($u_t = c^{2}u_{xx}$) is **parabolic** (zero); the wave equation ($u_{tt} = c^{2}u_{xx}$) is **hyperbolic** ($4c^{2} > 0$).

*Elliptic (steady state).* A boundary value problem: the five-point formula gives one equation per interior point and the whole grid is solved together by elimination or iteration (Liebmann, SOR with $\omega_{\text{opt}} = 2/(1 + \sin\frac{\pi}{N + 1})$). Error $O(h^{2})$: for $u = \sin\pi x\sin\pi y$ the centre error falls 0.0530, 0.0130, 0.0032 as $h$ halves from $\frac{1}{4}$. There is no stability limit, but plain Gauss-Seidel needs 25, 99, 365 sweeps for $3 \times 3$, $7 \times 7$, $15 \times 15$ interior points while SOR needs 13, 26, 49.

*Parabolic (diffusion).* An initial-boundary value problem solved by marching in time. *Explicit:* $u_i^{j+1} = r u_{i-1}^{j} + (1 - 2r)u_i^{j} + r u_{i+1}^{j}$, stable only for $r \le \frac{1}{2}$ (with $r = 0.6$ a 0.001 bump grew to 8953 in 60 steps), error $O(k) + O(h^{2})$, best at $r = \frac{1}{6}$ (error $6.7 \times 10^{-6}$ against $6.2 \times 10^{-3}$ at $r = \frac{1}{2}$). *Crank-Nicolson:* a tridiagonal system per step, stable for all $r$, error $O(k^{2}) + O(h^{2})$ (even $r = 5$ worked).

*Hyperbolic (waves).* Also a marching problem but with two time levels and two initial conditions: $u_i^{j+1} = 2(1 - r^{2})u_i^{j} + r^{2}(u_{i-1}^{j} + u_{i+1}^{j}) - u_i^{j-1}$, stable for $r = \frac{ck}{h} \le 1$ (exact for sine waves at $r = 1$). Waves do not decay, so numerical errors do not fade either.

| Type | Problem kind | Method | Stability |
|---|---|---|---|
| Elliptic | boundary values | simultaneous solve, SOR | none needed |
| Parabolic | initial + boundary | explicit / Crank-Nicolson | $r \le \frac{1}{2}$ / unconditional |
| Hyperbolic | initial + boundary | three-level explicit | $r \le 1$ |

*Conclusion.* The type of equation, not the grid, decides whether to solve all points together or to march in time and what limits the step.
