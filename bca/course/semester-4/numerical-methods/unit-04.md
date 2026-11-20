---
subject: Numerical Methods
grade: BCA Semester 4
unit: 4
title: Solution of Linear Algebraic Equations
hours: 10
area: BCA 253 · Numerical Methods · Unit 4
---

Circuit analysis, structural frames, the Google PageRank vector and the normal equations of Unit 2 all lead to systems of linear equations Ax = *b*, sometimes with thousands of unknowns. This unit covers direct methods (Gauss elimination, Gauss–Jordan, LU), iterative methods (Jacobi, Gauss–Seidel), the dangers of ill-conditioning, and the power method for eigenvalues.

::: key What this unit gives you
- Gauss elimination with partial pivoting, Gauss–Jordan inversion, LU factorisation.
- Jacobi and Gauss–Seidel iteration; convergence and diagonal dominance.
- Ill-conditioning and the condition number.
- Eigenvalue estimation by the power method.
:::


## 4.1 Gauss elimination

**Forward elimination** converts Ax = *b* to an upper-triangular system by subtracting multiples $m_{ik} = \frac{a_{ik}}{a_{kk}}$ of the pivot row from the rows below. **Back substitution** then solves from the last equation upwards. The cost is about $\frac{n^{3}}{3}$ multiplications.

**Partial pivoting.** Before eliminating column *k*, swap the row with the largest $|a_{ik}| (i \geq k)$ into the pivot position. This avoids dividing by a zero or tiny pivot and keeps the multipliers $|m| \leq 1$, which controls round-off. Always use it on a computer.

::: example Solve 2x + y − z = 8, −3x − y + 2z = −11, −2x + y + 2z = −3
Operations (with partial pivoting): swap R1 ↔ R2; m21 = -0.6667; m31 = 0.6667; swap R2 ↔ R3; m32 = 0.2000. The reduced upper-triangular augmented matrix is

| *x* | *y* | *z* | RHS |

|---|---|---|---|

| -3.0000 | -1.0000 | 2.0000 | -11.0000 |

| 0.0000 | 1.6667 | 0.6667 | 4.3333 |

| 0.0000 | 0.0000 | 0.2000 | -0.2000 |

Back substitution: $z = - 0.2 / 0.2 = - 1 ;\  y = \frac{4.3333 - 0.6667 (- 1)}{1.6667} = 3 ;\  x = \frac{- 11 + 3 - 2 (- 1)}{- 3} = 2$. The solution is **$(x ,\  y ,\  z) = (2.0000 ,\  3.0000 ,\  - 1.0000)$**, which agrees with `numpy.linalg.solve`. Check in the first original equation: $2 (2) + 3 - (- 1) = 8$ ✓.
:::

**Singular and inconsistent systems.** If a zero pivot remains in a column after trying all rows below, the matrix is singular: either no solution (a row 0 = nonzero) or infinitely many (a row $0 = 0$). The determinant equals the product of the pivots times (−1) to the number of swaps.

## 4.2 Gauss–Jordan method and matrix inversion

Gauss–Jordan continues eliminating *above* the pivots too, reducing A to the identity; the right-hand side becomes the solution. Applied to the augmented matrix [A | I] it produces **$A^{-1}$**.

::: example Inverse of [[2, 1], [5, 3]]
[A | I]: $R_{1} \leftarrow \frac{R_{1}}{2}$ gives [1, 0.5 | $0.5 ,\  0 ] ;\  R_{2} \leftarrow R_{2} - 5 R_{1}$ gives [0, 0.5 | $- 2.5 ,\  1 ] ;\  R_{2} \leftarrow 2 R_{2}$ gives [0, 1 | $- 5 ,\  2 ] ;\  R_{1} \leftarrow R_{1} - 0.5 R_{2}$ gives [1, 0 | 3, −1]. So $A^{-1} = \begin{bmatrix} 3 & - 1 \\ - 5 & 2 \end{bmatrix}$. Numerical check by NumPy: 3.0000, -1.0000, -5.0000, 2.0000 (row-wise). Check: $A \cdot A^{-1} = \begin{bmatrix} 6 - 5 & - 2 + 2 \\ 15 - 15 & - 5 + 6 \end{bmatrix} = I$ ✓.
:::

Gauss–Jordan costs about $\frac{n^{3}}{2}$, more than Gauss elimination, so use it for inverses, not for single systems.

## 4.3 LU factorisation

If no row swaps are needed, $A = L U$ with L unit-lower-triangular (1s on the diagonal, the multipliers below) and U upper-triangular (the result of elimination). Then Ax = *b* becomes two cheap triangular solves: **Ly = *b*** (forward substitution), **Ux = *y*** (back substitution). Once A is factorised, new right-hand sides cost only $O (n^{2})$, which is why LU is the workhorse of numerical libraries (with pivoting: $P A = L U$). The determinant is the product of U's diagonal.

::: example Doolittle LU for A = [[2, 1, 1], [4, 3, 3], [8, 7, 9]], b = (4, 10, 24)
Elimination multipliers: $m_{21} = 2 ,\  m_{31} = 4$, then $m_{32} = 3$. So $L = [ 1 ,\  0 ,\  0 ;\  2 ,\  1 ,\  0 ;\  4 ,\  3$, 1] and $U = [ 2 ,\  1 ,\  1 ;\  0 ,\  1 ,\  1 ;\  0 ,\  0$, 2] (rows separated by semicolons). Forward substitution Ly = *b* gives $y = (4 ,\  2 ,\  2)$; back substitution Ux = *y* gives $x = (1 ,\  1 ,\  1)$. The determinant is $2 \times 1 \times 2 = 4$. Check: LU reproduces A and A $x = b$ in code.
:::

Variants: **Crout** (U has the unit diagonal), **Cholesky** $A = L L^{T}$ for symmetric positive-definite matrices (half the work, no pivoting needed).

## 4.4 Iterative methods: Jacobi and Gauss–Seidel

For large sparse systems direct methods fill in zeros and cost too much. Iterative methods start from a guess and improve it. Solve equation $\ast i \ast$ for $x_{i}$:

$$x_{i}^{(k+1)} = \frac{b_{i} - \sum_{j \neq i} a_{ij} x_{j}}{a_{ii}}$$

- **Jacobi**: use only the old iterate $x^{(k)}$ on the right (all components updated "simultaneously").
- **Gauss–Seidel**: use the **newest** values as soon as they are available (components updated one after another), so it normally converges about twice as fast.

**Convergence.** Both converge for any start if A is **strictly diagonally dominant** ($|a_{ii}| > \sum_{j \neq i} |a_{ij}|$ in every row). That is sufficient, not necessary; the exact condition is that the iteration matrix has spectral radius below 1. Rearranging the equations so that large coefficients lie on the diagonal often helps.

::: example 10x₁ − x₂ + 2x₃ = 6; −x₁ + 11x₂ − x₃ + 3x₄ = 25; 2x₁ − x₂ + 10x₃ − x₄ = −11; 3x₂ − x₃ + 8x₄ = 15, start 0
The matrix is strictly diagonally dominant $(10 > 3 ,\  11 > 5 ,\  10 > 4 ,\  8 > 4)$; the exact solution is (1.0000, 2.0000, -1.0000, 1.0000).

**Jacobi** (first six sweeps):

| *k* | $x_{1}$ | $x_{2}$ | $x_{3}$ | $x_{4}$ |

|---|---|---|---|---|

| 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

| 1 | 0.6000 | 2.2727 | -1.1000 | 1.8750 |

| 2 | 1.0473 | 1.7159 | -0.8052 | 0.8852 |

| 3 | 0.9326 | 2.0533 | -1.0493 | 1.1309 |

| 4 | 1.0152 | 1.9537 | -0.9681 | 0.9738 |

| 5 | 0.9890 | 2.0114 | -1.0103 | 1.0214 |

| 6 | 1.0032 | 1.9922 | -0.9945 | 0.9944 |

**Gauss–Seidel** (first six sweeps):

| *k* | $x_{1}$ | $x_{2}$ | $x_{3}$ | $x_{4}$ |

|---|---|---|---|---|

| 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

| 1 | 0.6000 | 2.3273 | -0.9873 | 0.8789 |

| 2 | 1.0302 | 2.0369 | -1.0145 | 0.9843 |

| 3 | 1.0066 | 2.0036 | -1.0025 | 0.9984 |

| 4 | 1.0009 | 2.0003 | -1.0003 | 0.9998 |

| 5 | 1.0001 | 2.0000 | -1.0000 | 1.0000 |

| 6 | 1.0000 | 2.0000 | -1.0000 | 1.0000 |

To get all components within $5 \times 10^{-5}$ of the exact answer Jacobi needs **12** sweeps and Gauss–Seidel **6**. The spectral radius of the iteration matrix is 0.4264 for Jacobi and 0.0898 for Gauss–Seidel; the smaller it is, the faster the convergence. Because each sweep is cheap ($n^{2}$ operations for a dense matrix, far less for sparse ones), iterative methods win for huge sparse systems.
:::

::: caution Equation order matters
For $x + 3 y = 5 ,\  4 x + y = 6$ (solution (1.1818, 1.2727)), Gauss–Seidel from (0, 0) gives $(5.00 ,\  - 14.00) \to (47.00 ,\  - 182.00) \to (551 ,\  - 2198) \to (6599 ,\  - 26390)$: it diverges because the matrix is not diagonally dominant. Writing the equations in the other order, $4 x + y = 6$ first, gives $(1.5000 ,\  1.1667) \to (1.2083 ,\  1.2639) \to (1.1840 ,\  1.2720) \to (1.1820 ,\  1.2727) \to (1.1818 ,\  1.2727)$, which converges. The two systems are mathematically identical.
:::

## 4.5 Ill-conditioning

A system is **ill-conditioned** if tiny changes in A or *b* cause large changes in *x*. The culprit is a nearly singular matrix, and no algorithm can repair it; pivoting only avoids *additional* damage.

::: example A nearly singular system
$x + y = 2 ,\  x$ + 1.0001y = 2.0001 has the solution (1, 1). Change the right-hand side by 0.0001 to 2.0002: the solution jumps to (0, 2). A change of 0.005 % in one coefficient moved the answer by 100 %. The two equations describe almost parallel lines, so their intersection point is very sensitive.
:::

The **condition number** κ(A) = ‖A‖·‖A⁻¹‖ measures the amplification: relative error in $x \leq \kappa (A)$ × relative error in the data. For the matrix above $\kappa = 40002$, so a relative data error of $10^{-4}$ may produce a relative solution error of order one. The $3 \times 3$ Hilbert matrix, with entries $\frac{1}{i + j - 1}$, has $\kappa = 524$; it is moderately conditioned for $n = 3$ but becomes terrible as *n* grows. Rules of thumb: $\kappa \approx 10^{k}$ loses about *k* significant digits. Remedies: scaling, pivoting, higher precision, iterative refinement, or reformulating the problem.

## 4.6 Eigenvalues: the power method

The **power method** finds the **dominant** eigenvalue (largest in magnitude) $\lambda_{1}$ and its eigenvector. Start with any $v_{0}$ (with a component along the dominant eigenvector). Repeat: $w = A v_{k-1} ;\  \lambda_{k}$ = the entry of *w* with the largest magnitude; $v_{k} = \frac{w}{\lambda_{k}}$. Then $\lambda_{k} \to \lambda_{1}$ and $v_{k}$ → eigenvector, at a rate $|\frac{\lambda_{2}}{\lambda_{1}}|$.

::: example A = [[2, −1, 0], [−1, 2, −1], [0, −1, 2]], v₀ = (0, 1, 0)
| *k* | $A \cdot v_{k-1}$ | $\lambda_{k}$ (largest entry) | $v_{k}$ (scaled) |

|---|---|---|---|

| 1 | (-1.0000, 2.0000, -1.0000) | 2.0000 | (-0.5000, 1.0000, -0.5000) |

| 2 | (-2.0000, 3.0000, -2.0000) | 3.0000 | (-0.6667, 1.0000, -0.6667) |

| 3 | (-2.3333, 3.3333, -2.3333) | 3.3333 | (-0.7000, 1.0000, -0.7000) |

| 4 | (-2.4000, 3.4000, -2.4000) | 3.4000 | (-0.7059, 1.0000, -0.7059) |

| 5 | (-2.4118, 3.4118, -2.4118) | 3.4118 | (-0.7069, 1.0000, -0.7069) |

| 6 | (-2.4138, 3.4138, -2.4138) | 3.4138 | (-0.7071, 1.0000, -0.7071) |

| 7 | (-2.4141, 3.4141, -2.4141) | 3.4141 | (-0.7071, 1.0000, -0.7071) |

The eigenvalue estimates climb towards **$2 + \sqrt{2} = 3.4142$**, and the vector towards $(- 0.7071 ,\  1 ,\  - 0.7071) \propto \left( 1 ,\  - \sqrt{2} ,\  1 \right)$. The Rayleigh quotient $\frac{v^{T} A v}{v^{T} v}$ of the final vector gives 3.4142, a faster-converging estimate. The smallest eigenvalue can be found by applying the method to $A^{-1}$ (inverse iteration); shifts find the others.
:::

## 4.7 Seeing the ideas: elimination, iteration speed and the geometry of ill-conditioning

Carl Friedrich Gauss gave elimination its name, and his portrait opens Plate 4.1. The plate also shows why some systems are dangerous: when two lines are nearly parallel, a tiny change moves their intersection a long way.

```photogrid label="4.1" cols="2" ratio="1.1" caption="Solving linear systems. (a) Carl Friedrich Gauss, whose name is attached to elimination (the method itself appears in the Chinese Nine Chapters about 2,000 years earlier). (b) Geometry of a 2 *x* 2 system: a well-conditioned pair of lines (left) crosses at a clear angle, so a small error in the data moves the solution a little; a nearly parallel pair (right) crosses at a shallow angle and the solution is unstable."
@ photo id="bca204/gauss" cap="Gauss"
fit 1.1
focus 0.5 0.7
@ svg cap="Well and badly conditioned"
f = Fig(300, 240)
f.text(78, 14, "well-conditioned", size=10.5, color=TEAL, bold=True)
f.line(14, 190, 142, 40, color=NAVY, sw=2.2); f.line(14, 60, 142, 190, color=RED, sw=2.2)
f.circle(78, 125, 5, fill=TEAL, stroke=TEAL)
f.text(78, 214, "clear crossing angle", size=9.5, color=SLATE)
f.text(228, 14, "ill-conditioned", size=10.5, color=RED, bold=True)
f.line(160, 150, 290, 98, color=NAVY, sw=2.2); f.line(160, 156, 290, 92, color=RED, sw=2.2)
f.circle(225, 124, 5, fill=RED, stroke=RED)
f.text(228, 214, "almost parallel", size=9.5, color=SLATE)
```

```svgfig label="4.1" caption="Gauss elimination on $10 x + y + z = 12 ,\  2 x + 10 y + z = 13 ,\  2 x + 2 y + 10 z = 14$. Multipliers 0.2, 0.2 and 0.18367 reduce the augmented matrix to upper-triangular form, and back substitution gives $z = 1 ,\  y = 1 ,\  x = 1$."
f = Fig(580, 150)
def M(x, rows, title, fl, st):
    f.text(x + 70, 14, title, size=10.5, color=st, bold=True)
    for i, r in enumerate(rows): f.box(x, 22 + i * 34, 140, 28, r, fill=fl, stroke=st, size=10.5)
M(8, ["10   1   1 | 12", "2   10   1 | 13", "2    2  10 | 14"], "start", BLUE, NAVY)
M(212, ["10    1    1 | 12", "0   9.8  0.8 | 10.6", "0   1.8  9.8 | 11.6"], "after step 1 (m = 0.2, 0.2)", SAND, AMBER)
M(416, ["10    1      1 | 12", "0   9.8    0.8 | 10.6", "0    0   9.6531 | 9.6531"], "after step 2 (m = 0.18367)", MINT, TEAL)
f.arrow([(150, 66), (212, 66)]); f.arrow([(354, 66), (416, 66)])
f.text(290, 136, "back substitution: z = 9.6531 / 9.6531 = 1, y = (10.6 - 0.8) / 9.8 = 1, x = (12 - 1 - 1) / 10 = 1", size=10, color=TEAL, bold=True)
```

```svgfig label="4.2" caption="Jacobi versus Gauss-Seidel on the same system, starting from (0, 0, 0). The largest error after each sweep (true answer 1, 1, 1): Jacobi 0.4, 0.1, 0.03, 0.0084; Gauss-Seidel 0.2, 0.0054, 0.00044, 0.00002. Using the newest values makes Gauss-Seidel roughly twice as fast."
import math
f = Fig(580, 200)
ax = Axes(f, 50, 14, 510, 150, (0.5, 4.5), (-5.5, 0))
ax.grid(1, 1)
ax.axes("", "")
J = [0.4, 0.1, 0.03, 0.0084]; G = [0.2, 0.00536, 0.00044, 0.00002]
for S, c in ((J, AMBER), (G, TEAL)):
    pts = [(k + 1, math.log10(v)) for k, v in enumerate(S)]
    for (a, b), (c2, d) in zip(pts, pts[1:]):
        ax.curve(lambda t, a=a, b=b, c2=c2, d=d: b + (d - b) * (t - a) / (c2 - a), a, c2, color=c, sw=2.4)
    for a, b in pts: ax.pt(a, b, "", color=c)
f.text(420, 60, "Jacobi", size=11, color=AMBER, bold=True)
f.text(200, 150, "Gauss-Seidel", size=11, color=TEAL, bold=True)
f.text(306, 188, "iteration (vertical axis: log10 of the largest error)", size=10, color=SLATE)
```

### 4.7.1 Eight uses of linear systems and their numerical solution

1. **Electrical networks.** Kirchhoff's laws turn a circuit with many loops into a set of linear equations. A hydropower grid has thousands of nodes and is solved by computer. Elimination or iteration gives all currents at once.
2. **Structures and bridges.** Engineers divide a truss or bridge into joints and write force-balance equations for each. The unknown forces in every member come from one big linear system. The same method checks buildings against earthquake loads.
3. **Economics and planning.** Input-output tables describe how each industry uses the products of others. Solving a linear system shows how much each sector must produce to meet final demand. Governments use it in planning.
4. **Curve fitting.** The normal equations of least squares are linear equations in the unknown coefficients. Every trend line and calibration uses them. A spreadsheet solves them in a moment.
5. **Computer graphics.** Moving, rotating and projecting a 3D model involves solving linear systems for the transformation. Games solve millions of such equations per second. Graphics cards are built for it.
6. **Search and ranking.** The ranking of web pages is an eigenvector problem solved by repeating a matrix multiplication, a method close to the power method. Recommendation systems use the same idea. Linear algebra runs behind the screen.
7. **Weather and flow simulation.** Dividing the air or a river into small cells gives millions of linked equations, solved by fast iterative methods. Direct elimination would be far too slow. Choosing the right method decides whether a forecast arrives in time.
8. **Network and traffic analysis.** Flow of traffic, water in a pipe network and data in a computer network follow balance equations. Solving them locates bottlenecks. Planners in Kathmandu can test a road change on paper first.

```photogrid label="4.2" cols="2" ratio="1.4" caption="How many digits can an ill-conditioned system burn? (a) A slide rule gives about three correct digits, and engineers knew to stop trusting any answer beyond them. (b) The Hilbert matrix H with entries $\frac{1}{i + j - 1}$ is the classic ill-conditioned system. Its condition number is about 19 for $n = 2 ,\  1.6 x 10^{4}$ for $n = 4 ,\  1.5 x 10^{7}$ for $n = 6 ,\  1.5 x 10^{10}$ for $n = 8$ and 1.6 $x 10^{13}$ for $n = 10$. A rule of thumb says the solution loses about $\log 10 ( \mathrm{condition}$ number) digits of the 16 carried by double precision. For $n = 8$ we solved Hx = *b* with a known solution of all ones and got a largest error of about 1 $x 10^{- 7}$, so only about 7 of 16 digits were correct; for $n = 10$ only about 3 would remain. A small residual does not prove a small error when the matrix is ill-conditioned."
@ photo id="bcanm/sliderule" cap="A slide rule: three digits of precision"
fit 1.4
focus 0.5 0.5
@ svg cap="Digits lost = log10 of the condition number"
import numpy as np
ns = [2, 4, 6, 8, 10]
cond = [np.linalg.cond(1 / (np.arange(1, n + 1)[:, None] + np.arange(n)[None, :])) for n in ns]
lost = [int(round(float(np.log10(c)))) for c in cond]
assert lost == [1, 4, 7, 10, 13]
n = 8; H = 1 / (np.arange(1, n + 1)[:, None] + np.arange(n)[None, :]); err = float(np.abs(np.linalg.solve(H, H @ np.ones(n)) - 1).max())
assert 1e-9 < err < 1e-5
f = Fig(300, 240)
f.text(150, 14, "digits lost out of 16 (double precision)", size=10.5, color=NAVY, bold=True)
base, sc = 170, 120 / 16.0
for i, (n_, l) in enumerate(zip(ns, lost)):
    x = 20 + i * 54; h = l * sc
    f.box(x, base - h, 40, h, "", fill="#b91c1c" if l >= 10 else "#1d6fb8", stroke=NAVY, r=0, sw=1)
    f.text(x + 20, base - h - 8, str(l), size=10.5, color=NAVY, bold=True)
    f.text(x + 20, base + 14, f"n = {n_}", size=10.5, color=SLATE)
f.line(10, base, 292, base, color=SLATE, sw=1.2)
f.line(10, base - 120, 292, base - 120, color="#0f766e", sw=1.2, dash=True)
f.text(150, 206, "dashed line = all 16 digits", size=10.5, color=SLATE)
f.text(150, 224, "n = 8: error about 1e-7, 7 digits left", size=10.5, color=RED, bold=True)
```

## 4.8 Pivoting, operation counts and tridiagonal systems

**Why pivoting is not optional.** Gauss elimination divides by the pivot $a_{kk}$. A tiny pivot makes the multipliers enormous, and the rounding errors they carry swamp the answer. Take
$$10^{-20}\,x + y = 1,\qquad x + y = 2 .$$
The true solution is $x \approx 1$, $y \approx 1$. Without row exchange the multiplier is $10^{20}$, the second equation becomes $(1 - 10^{20})\,y = 2 - 10^{20}$, and in double precision both sides round to $-10^{20}$, so $y = 1$ and then $x = (1 - 1)/10^{-20} = \mathbf{0}$: a completely wrong $x$. **Partial pivoting** swaps rows so that the largest $|a_{ik}|$ in the column (from row $k$ down) becomes the pivot. Here the rows are exchanged, the multiplier is $10^{-20}$ and the computed solution is correct. *Scaled* partial pivoting compares entries after dividing each row by its largest coefficient, which protects against badly scaled equations.

**Cost of the methods.** For an $n \times n$ system:

| Operation | Multiplications (approx.) | $n = 10$ | $n = 100$ | $n = 1000$ |
|---|---|---|---|---|
| Gauss elimination or LU factorisation | $n^{3}/3$ | 333 | 333 333 | 333 333 333 |
| Forward and back substitution (one right-hand side) | $n^{2}$ | 100 | 10 000 | 1 000 000 |
| Gauss–Jordan, or finding $A^{-1}$ | about $n^{3}$ | 1 000 | $10^{6}$ | $10^{9}$ |
| Cramer's rule with determinants by expansion | about $(n+1)!$ | $4\times 10^{7}$ | impossible | impossible |

Two lessons follow. LU is the right choice when the *same* matrix has many right-hand sides: factorise once for $n^{3}/3$ and each new $b$ costs only $n^{2}$. And one should almost never compute $A^{-1}$ to solve $Ax = b$; it costs three times as much as elimination and is less accurate.

**The Thomas algorithm (tridiagonal systems).** Equations from splines (Section 2.6), differential equations (Unit 5) and the Laplace problem in one dimension have a **tridiagonal** matrix: nonzero entries only on the diagonal and its two neighbours, with sub-diagonal $a_i$, diagonal $b_i$, super-diagonal $c_i$. Elimination then needs only two sweeps and about $8n$ operations in total, not $n^{3}/3$.

*Forward sweep* ($i = 2, \dots, n$): $c'_1 = \dfrac{c_1}{b_1},\ d'_1 = \dfrac{d_1}{b_1}$, and $c'_i = \dfrac{c_i}{b_i - a_i c'_{i-1}},\ d'_i = \dfrac{d_i - a_i d'_{i-1}}{b_i - a_i c'_{i-1}}$. *Back substitution:* $x_n = d'_n$, $x_i = d'_i - c'_i x_{i+1}$.

::: example Five equations with 2 on the diagonal and −1 on both neighbours, right side (1, 0, 0, 0, 1)
| $i$ | $a_i$ | $b_i$ | $c_i$ | $d_i$ | $c'_i$ | $d'_i$ | $x_i$ |
|---|---|---|---|---|---|---|---|
| 1 | | 2 | −1 | 1 | −0.5000 | 0.5000 | 1 |
| 2 | −1 | 2 | −1 | 0 | −0.6667 | 0.3333 | 1 |
| 3 | −1 | 2 | −1 | 0 | −0.7500 | 0.2500 | 1 |
| 4 | −1 | 2 | −1 | 0 | −0.8000 | 0.2000 | 1 |
| 5 | −1 | 2 | 0 | 1 | | 1.0000 | 1 |

The solution is $x = (1, 1, 1, 1, 1)$, which a direct solver confirms. The algorithm is stable when the matrix is diagonally dominant (as here and in splines), and a system of a million unknowns takes a fraction of a second.
:::

## 4.9 Cholesky factorisation for symmetric positive definite matrices

If $A$ is **symmetric** ($A = A^{T}$) and **positive definite** ($x^{T}Ax > 0$ for every $x \ne 0$; equivalently all eigenvalues are positive, or all leading principal minors are positive), it can be factorised as $A = LL^{T}$ with $L$ lower triangular with a positive diagonal. This needs only $n^{3}/6$ operations (half the cost of LU), no pivoting, and fails (a square root of a negative number) exactly when the matrix is not positive definite, so it doubles as a test for definiteness. The entries are

$$l_{jj} = \sqrt{a_{jj} - \sum_{k<j} l_{jk}^{2}},\qquad l_{ij} = \frac{1}{l_{jj}}\left(a_{ij} - \sum_{k<j} l_{ik}\,l_{jk}\right)\quad (i > j).$$

::: example Cholesky factor of A = [[4, 12, −16], [12, 37, −43], [−16, −43, 98]]
Column 1: $l_{11} = \sqrt{4} = 2$, $l_{21} = 12/2 = 6$, $l_{31} = -16/2 = -8$.
Column 2: $l_{22} = \sqrt{37 - 36} = 1$, $l_{32} = (-43 - (-8)(6))/1 = 5$.
Column 3: $l_{33} = \sqrt{98 - 64 - 25} = \sqrt{9} = 3$.

$$L = \begin{bmatrix} 2 & 0 & 0 \\ 6 & 1 & 0 \\ -8 & 5 & 3 \end{bmatrix},\qquad LL^{T} = A .$$

To solve $Ax = b$: forward-substitute $Ly = b$, then back-substitute $L^{T}x = y$.
:::

Cholesky factorisation underlies least squares through the normal equations $A^{T}A\,c = A^{T}y$ (the matrix is symmetric positive definite) and many statistical routines, although for ill-conditioned problems QR is safer (Section 2.13).

## 4.10 Norms, condition number and the meaning of a small residual

To say that one vector or matrix is "small" or that two are "close" we need a **norm**. For a vector: $\|x\|_{1} = \sum |x_i|$, $\|x\|_{2} = \sqrt{\sum x_i^{2}}$, $\|x\|_{\infty} = \max |x_i|$. The matching matrix norms: $\|A\|_{\infty} = \max_i \sum_j |a_{ij}|$ (largest absolute row sum) and $\|A\|_{1}$ = largest absolute column sum. They satisfy $\|Ax\| \le \|A\|\,\|x\|$.

The **condition number** is $\kappa(A) = \|A\|\,\|A^{-1}\|$. It is at least 1 and measures how much the relative error of the data can be magnified in the solution:

$$\frac{\|\delta x\|}{\|x\|} \le \kappa(A)\,\frac{\|\delta b\|}{\|b\|}.$$

::: example An almost singular system
$$\begin{bmatrix} 1 & 2 \\ 1.0001 & 2.0001 \end{bmatrix}\begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} 3 \\ 3.0002 \end{bmatrix}$$
has the solution $x = y = 1$. Change the second right-hand side by $10^{-4}$ (from 3.0002 to 3.0001) and the solution jumps to $x = -1,\ y = 2$. Here $\|A\|_{\infty} = 3.0002$, $A^{-1} = \begin{bmatrix} -20001 & 20000 \\ 10001 & -10000 \end{bmatrix}$ with $\|A^{-1}\|_{\infty} = 40001$, so $\kappa_{\infty}(A) = 3.0002 \times 40001 = 1.2\times 10^{5}$. The data error of $3\times 10^{-5}$ (relative) was magnified by about $10^{5}$, in line with the bound. Rows that are nearly multiples of each other (the two lines are almost parallel) always give a large $\kappa$.
:::

For comparison, the $3 \times 3$ Hilbert matrix has $\kappa_{\infty} = 748$, the $5 \times 5$ one $4.8\times 10^{5}$ (Section 2.13). A rule of thumb: you lose about $\log_{10}\kappa(A)$ correct digits of the solution, so with $\kappa = 10^{5}$ and double precision you can trust about eleven digits, but with $\kappa = 10^{15}$ none.

**A small residual does not mean a small error.** The residual of an approximate solution $\hat{x}$ is $r = b - A\hat{x}$ and the error is $e = x - \hat{x}$; they are related by $e = A^{-1}r$, so $\|e\| \le \|A^{-1}\|\,\|r\|$. For the system above, take the poor guess $\hat{x} = (2, 0.5)$: the residual is only $(0, 5\times 10^{-5})$ yet the error is $(-1, 0.5)$. A tiny residual certifies an accurate answer only when $\kappa$ is small.

**Iterative refinement.** After solving $Ax = b$ in ordinary precision to get $\hat{x}$, compute the residual $r = b - A\hat{x}$ (preferably in higher precision), solve $A\,\delta = r$ with the *same* LU factors (cost $n^{2}$) and replace $\hat{x}$ by $\hat{x} + \delta$. A step or two removes the round-off error if $\kappa(A)$ is not too large; if $\kappa \gtrsim 1/\varepsilon$ the refinement cannot help.

## 4.11 Convergence of iterations and successive over-relaxation

**When do Jacobi and Gauss-Seidel converge?** Write the iteration as $x^{(k+1)} = T x^{(k)} + c$. It converges for every start if and only if the **spectral radius** $\rho(T) = \max|\lambda_i(T)| < 1$, and the error shrinks by about $\rho$ per iteration. *Strict diagonal dominance* ($|a_{ii}| > \sum_{j\ne i}|a_{ij}|$ for every row) is a convenient sufficient condition for both methods, but not necessary.

::: example Spectral radii for the system 10x + y + z = 12, 2x + 10y + z = 13, 2x + 2y + 10z = 14
The iteration matrices have $\rho_{\text{Jacobi}} = 0.2847$ and $\rho_{\text{Gauss-Seidel}} = 0.0447$. Gauss-Seidel therefore gains $-\log_{10} 0.0447 = 1.35$ digits per iteration, Jacobi only $0.55$ digits, so Gauss-Seidel is about 2.5 times faster, which matches the tables of Section 4.4.

For the system $x + 2y = 3,\ 3x + y = 4$ (not diagonally dominant in this order) Jacobi has $\rho = 2.449 > 1$ and diverges, but exchanging the two equations to $3x + y = 4,\ x + 2y = 3$ puts a dominant diagonal and makes it converge.
:::

**Successive over-relaxation (SOR).** Gauss-Seidel computes a new value $x_i^{\text{GS}}$ for each unknown. SOR *overshoots* in the direction of the change by a factor $\omega$:

$$x_i^{(k+1)} = (1 - \omega)\,x_i^{(k)} + \frac{\omega}{a_{ii}}\left(b_i - \sum_{j<i} a_{ij}\,x_j^{(k+1)} - \sum_{j>i} a_{ij}\,x_j^{(k)}\right),\qquad 0 < \omega < 2 .$$

$\omega = 1$ is Gauss-Seidel; $1 < \omega < 2$ is over-relaxation and can be dramatically faster; the method diverges outside $0 < \omega < 2$. For symmetric positive definite *tridiagonal* matrices the optimum is $\omega_{\text{opt}} = \dfrac{2}{1 + \sqrt{1 - \rho_J^{2}}}$, where $\rho_J$ is the Jacobi spectral radius.

::: example 8 × 8 system with 2 on the diagonal and −1 beside it (right side all 1), stop when the change is below 10⁻⁶
Here $\rho_J = 0.9397$ and $\omega_{\text{opt}} = 1.490$. Iterations needed:

| Method | Iterations |
|---|---|
| Jacobi | 216 |
| Gauss–Seidel ($\omega = 1$) | 115 |
| SOR, $\omega = 1.2$ | 76 |
| SOR, $\omega = 1.4$ | 45 |
| SOR, $\omega = 1.5$ (near optimum) | **26** |
| SOR, $\omega = 1.6$ | 33 |
| SOR, $\omega = 1.8$ | 72 |
| SOR, $\omega = 1.9$ | 152 |

The right value of $\omega$ cuts the work by a factor of 8 against Gauss-Seidel and 4 against Jacobi, but a value slightly too large costs much more than one slightly too small.
:::

```svgfig label="4.3" caption="Iterations needed by SOR for the 8 x 8 system against the relaxation factor $\omega$ (tolerance $10^{-6}$). The curve has a sharp minimum at $\omega_{\text{opt}} = 1.49$ and rises steeply on the high side; $\omega = 1$ is Gauss-Seidel (115 iterations). Jacobi needs 216."
f = Fig(560, 240)
ax = Axes(f, 56, 14, 520, 180, (0.95, 2.0), (0, 320))
ax.grid(0.1, 50)
ax.axes("", "")
W = [1.0, 1.2, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 1.95]
N = [115, 76, 45, 26, 33, 45, 72, 152, 304]
P = list(zip(W, N))
for (x1, y1), (x2, y2) in zip(P, P[1:]):
    f.line(ax.X(x1), ax.Y(y1), ax.X(x2), ax.Y(y2), color=NAVY, sw=2.4)
for x, y in P:
    f.circle(ax.X(x), ax.Y(y), 3.6, fill=NAVY, stroke=NAVY)
f.line(ax.X(0.95), ax.Y(216), ax.X(2.0), ax.Y(216), color=AMBER, sw=1.4, dash=True)
f.text(450, ax.Y(216) - 10, "Jacobi: 216", size=10, color=AMBER, bold=True)
f.text(ax.X(1.5), ax.Y(26) + 22, "optimum near 1.49", size=10.5, color=RED, bold=True)
f.text(300, 214, "relaxation factor omega", size=10.5, color=SLATE)
f.text(300, 232, "iterations to reach 1e-6", size=10, color=SLATE)
```

## 4.12 More on eigenvalues: Rayleigh quotient, inverse power method, Gershgorin and QR

**Rayleigh quotient.** For a symmetric matrix and a current vector $x$, the quotient $\dfrac{x^{T}Ax}{x^{T}x}$ is a far better estimate of the dominant eigenvalue than the largest component of $Ax$ used in Section 4.6: its error is of the second order in the error of $x$.

::: example Power method on A = [[4, 1, 0], [1, 3, 1], [0, 1, 2]] from (1, 1, 1)
The true eigenvalues are 4.73205, 3 and 1.26795 (ratio $3/4.732 = 0.634$, so the power method is slow). After the same iterations the two estimates are:

| Step | scale factor (largest component of $Ax$) | Rayleigh quotient |
|---|---|---|
| 1 | 5.0000 | 4.3333 |
| 4 | 4.8537 | 4.7170 |
| 6 | 4.7806 | 4.7296 |
| 8 | 4.7513 | 4.7317 |

After eight steps the scale factor is still off by 0.02 while the Rayleigh quotient is within $5\times 10^{-4}$ of 4.73205.
:::

**Inverse power method and shifts.** Applying the power method to $A^{-1}$ finds the eigenvalue of $A$ *nearest zero*; applying it to $(A - sI)^{-1}$ finds the eigenvalue **nearest the shift** $s$. Each step solves $(A - sI)\,y = x$ (factorise once, then reuse), takes $x \leftarrow y/\max(y)$ and estimates $\lambda \approx s + 1/\max(y)$.

::: example Inverse power with shift s = 1.5 for the same matrix
Estimates of the eigenvalue after steps 1 to 5: 2.1429, 1.7442, 1.2602, 1.2690, 1.2678, converging to the eigenvalue **1.26795** nearest 1.5 and with the eigenvector (0.268, −0.732, 1). A shift closer to the eigenvalue gives faster convergence; using the latest Rayleigh quotient as the shift gives cubic convergence for symmetric matrices.
:::

**Gershgorin's theorem.** Every eigenvalue of $A$ lies in at least one disc centred at a diagonal entry $a_{ii}$ with radius $r_i = \sum_{j \ne i}|a_{ij}|$ (the sum of the other absolute entries in the row). For the matrix above the discs are centred at 4 (radius 1), 3 (radius 2) and 2 (radius 1), so every eigenvalue lies in $[1, 5]$, and since the matrix is symmetric the eigenvalues are real. This gives a free bracket for the power method and a free test for singularity: if no disc contains 0 the matrix is nonsingular.

```svgfig label="4.4" caption="Gershgorin discs for the symmetric matrix [[4,1,0],[1,3,1],[0,1,2]], shown on the real axis as intervals (centre plus or minus radius), and the true eigenvalues 1.268, 3 and 4.732 (red dots). Each eigenvalue lies inside the union of the discs, which spans [1, 5]."
f = Fig(560, 210)
x0, x1 = 50, 520
def X(v): return x0 + (v - 0.0) / 6.0 * (x1 - x0)
f.line(X(0), 150, X(6), 150, color=SLATE, sw=1.6)
for v in range(0, 7):
    f.line(X(v), 145, X(v), 155, color=SLATE, sw=1.2)
    f.text(X(v), 170, str(v), size=10, color=SLATE)
for k, (c, r, col) in enumerate(((4, 1, NAVY), (3, 2, TEAL), (2, 1, AMBER))):
    y = 40 + 30 * k
    f.line(X(c - r), y, X(c + r), y, color=col, sw=5)
    f.line(X(c - r), y - 7, X(c - r), y + 7, color=col, sw=2)
    f.line(X(c + r), y - 7, X(c + r), y + 7, color=col, sw=2)
    f.circle(X(c), y, 4, fill=BLUE, stroke=col)
    f.text(X(c + r) + 44, y, "centre %d, radius %d" % (c, r), size=10, color=col, bold=True)
for e in (1.26795, 3.0, 4.73205):
    f.circle(X(e), 150, 5, fill=ROSE, stroke=RED)
    f.line(X(e), 150, X(e), 128, color=RED, sw=1, dash=True)
f.text(X(3), 196, "true eigenvalues (red)", size=10.5, color=RED, bold=True)
```

**The QR algorithm.** All eigenvalues at once are found by the QR iteration used in library routines: factorise $A_k = Q_kR_k$ and form $A_{k+1} = R_kQ_k$ (a similarity transformation, so the eigenvalues are unchanged). Under mild conditions $A_k$ tends to an upper triangular matrix with the eigenvalues on the diagonal, largest first. For the matrix above six unshifted steps give the diagonal 4.72815, 3.00387, 1.26798 (true values 4.73205, 3, 1.26795), with all off-diagonal entries below 0.09. Practical codes first reduce $A$ to tridiagonal (symmetric case) or Hessenberg form and use shifts so that the iteration converges in a few steps per eigenvalue.

## Formula and fact sheet

- Multiplier $m_{ik} = \frac{a_{ik}}{a_{kk}}$; partial pivoting: swap to the largest $|a_{ik}| ;\  \det = \pm \Pi$ pivots.
- Gauss–Jordan on [A | I] gives $A^{-1}$. LU: Ly = *b* then Ux = *y*.
- Jacobi: old values; Gauss–Seidel: newest values; converge if diagonally dominant.
- κ(A) = ‖A‖‖A⁻¹‖; digits lost ≈ $\log_{10} \kappa$.
- Power method: *w* = Av, *λ* = largest entry, $v = \frac{w}{\lambda}$; rate $|\frac{\lambda_{2}}{\lambda_{1}}|$.
- Costs: LU $n^3/3$, substitution $n^2$, inverse $\approx n^3$; Thomas algorithm for tridiagonal $\approx 8n$; Cholesky $A = LL^T$ costs $n^3/6$ (needs $A$ symmetric positive definite).
- $\kappa(A) = \|A\|\,\|A^{-1}\|$; $\dfrac{\|\delta x\|}{\|x\|} \le \kappa\,\dfrac{\|\delta b\|}{\|b\|}$; digits lost $\approx \log_{10}\kappa$; $\|A\|_\infty$ = largest row sum.
- Iteration converges iff $\rho(T) < 1$; SOR: $x_i \leftarrow (1-\omega)x_i + \omega\,x_i^{GS}$, $0 < \omega < 2$, $\omega_{opt} = \dfrac{2}{1+\sqrt{1-\rho_J^2}}$.
- Rayleigh quotient $\dfrac{x^TAx}{x^Tx}$; inverse power with shift $s$: $(A - sI)y = x$, $\lambda \approx s + 1/\max y$; Gershgorin discs: centre $a_{ii}$, radius $\sum_{j\ne i}|a_{ij}|$.

## Chapter summary

- Direct methods (Gauss, Gauss–Jordan, LU) give the exact answer in a fixed number of steps; use partial pivoting.
- Iterative methods suit large sparse systems; Gauss–Seidel usually converges faster than Jacobi, and diagonal dominance guarantees it.
- Ill-conditioned systems amplify data errors regardless of method; the condition number quantifies this.
- The power method estimates the dominant eigenpair using repeated multiplication.
- Pivoting prevents division by tiny numbers, the Thomas and Cholesky algorithms exploit structure, norms and the condition number quantify sensitivity (a small residual is not a small error), spectral radius governs iteration speed and SOR with a good $\omega$ is several times faster than Gauss-Seidel; Rayleigh quotients, shifts, Gershgorin discs and QR extend the eigenvalue toolkit.

## Practice

1. Solve $2 x + y - z = 8 ,\  - 3 x - y + 2 z = - 11 ,\  - 2 x + y + 2 z = - 3$ by Gauss elimination with partial pivoting.
2. Find the inverse of $\begin{bmatrix} 2 & 1 \\ 5 & 3 \end{bmatrix}$ by Gauss–Jordan.
3. Factorise $A = \begin{bmatrix} 2 & 1 & 1 \\ 4 & 3 & 3 \\ 8 & 7 & 9 \end{bmatrix}$ as LU and solve Ax = (4, 10, 24).
4. Do two Jacobi and two Gauss–Seidel iterations for the $4 \times 4$ system of Section 4.4 from zero; which gives the better $x_{2}$?
5. State the sufficient condition for convergence of Jacobi and Gauss–Seidel. Is it necessary?
6. Why does Gauss–Seidel diverge for $x + 3 y = 5 ,\  4 x + y = 6$ but converge after swapping the equations?
7. What is an ill-conditioned system? Illustrate with an example and name the condition number.
8. Apply the power method to $A = \begin{bmatrix} 2 & - 1 & 0 \\ - 1 & 2 & - 1 \\ 0 & - 1 & 2 \end{bmatrix}$ and report the eigenvalue after four iterations.
9. Compare Gauss elimination and LU factorisation when there are many right-hand sides.
10. Solve $0.0001x + y = 1,\ x + y = 2$ by Gauss elimination with and without pivoting in three-digit arithmetic. Which is right?
11. How many multiplications does LU factorisation need for $n = 50$? How many for each additional right-hand side?
12. Solve the tridiagonal system $2x_1 - x_2 = 1,\ -x_1 + 2x_2 - x_3 = 0,\ -x_2 + 2x_3 = 1$ by the Thomas algorithm.
13. Find the Cholesky factor of $\begin{bmatrix} 9 & 3 \\ 3 & 5 \end{bmatrix}$ and use it to solve $Ax = (12, 8)^{T}$.
14. Find $\|A\|_{\infty}$, $\|A^{-1}\|_{\infty}$ and $\kappa_{\infty}(A)$ for $A = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}$.
15. Explain why the residual $(0, 5\times 10^{-5})$ for $\hat{x} = (2, 0.5)$ in Section 4.10 does not mean the solution is accurate.
16. Is $\begin{bmatrix} 2 & 3 \\ 5 & 1 \end{bmatrix}$ diagonally dominant? Rearrange $2x + 3y = 8,\ 5x + y = 7$ so that Gauss-Seidel converges, and take two iterations from $(0, 0)$.
17. The Jacobi spectral radius of a matrix is 0.9. Estimate the number of iterations to reduce the error by a factor $10^{-6}$ for Jacobi and (assuming $\rho_{GS} = \rho_J^{2}$) for Gauss-Seidel.
18. Write the SOR formula for the first equation of $4x - y = 3,\ -x + 4y = 3$ with $\omega = 1.1$ and do one sweep from $(0, 0)$.
19. Use Gershgorin's theorem to bound the eigenvalues of $\begin{bmatrix} 5 & 1 & 0 \\ 1 & 4 & 1 \\ 0 & 1 & 3 \end{bmatrix}$ and explain why all are positive.
20. Do two steps of the inverse power method with shift $s = 0$ for $A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}$ starting from $(1, 0)$. Which eigenvalue does it approach?

::: note Answers and worked solutions
**1.** $(x ,\  y ,\  z) = (2.0000 ,\  3.0000 ,\  - 1.0000)$; the elimination is shown in Section 4.1.

**2.** $A^{-1} = \begin{bmatrix} 3 & - 1 \\ - 5 & 2 \end{bmatrix}$ (Section 4.2).

**3.** $L = [1 ,\  0 ,\  0 ;\  2 ,\  1 ,\  0 ;\  4 ,\  3 ,\  1] ,\  U = [2 ,\  1 ,\  1 ;\  0 ,\  1 ,\  1 ;\  0 ,\  0 ,\  2] ,\  y = (4 ,\  2 ,\  2) ,\  x = (1 ,\  1 ,\  1)$.

**4.** From the tables in Section 4.4: after two sweeps Jacobi and Gauss–Seidel give the rows $k = 2$; Gauss–Seidel's $x_{2} = 2.0369$ is closer to the exact 2.0000 than Jacobi's value in its table row $k = 2$, because it uses the new values at once.

**5.** Strict diagonal dominance of rows: $|a_{ii}| > \sum_{j \neq i} |a_{ij}|$. It is sufficient but not necessary; convergence actually requires the spectral radius of the iteration matrix to be < 1.

**6.** In the first order the matrix is not diagonally dominant $(|1| < |3|)$ and the iteration matrix has spectral radius above 1; after swapping, the large entries 4 and 3 sit on the diagonal and the iteration contracts (compare the sequences in Section 4.4).

**7.** Small input changes cause large output changes, as in $x + y = 2 ,\  x$ + 1.0001y = $2.0001 \to (1 ,\  1)$, versus right side $2.0002 \to (0 ,\  2)$. The condition number κ(A) = ‖A‖‖A⁻¹‖ (here 40002) measures the amplification.

**8.** From the table in Section 4.6, the fourth iteration gives $\lambda \approx 3.4000$ (true 3.4142).

**9.** Plain elimination repeats the $O (n^{3})$ work for every new *b*. LU factorises once $(O (n^{3}))$ and then each right-hand side costs only $O (n^{2})$ for the two triangular solves.

**10.** *Without pivoting* (pivot 0.0001): the multiplier is 10 000; row 2 becomes $(1 - 10000)y = 2 - 10000$, i.e. $-10000\,y = -10000$ in three digits, so $y = 1.00$ and $x = (1 - 1.00)/0.0001 = 0$. The true solution is $x = 1.0001,\ y = 0.9999$, so $x$ is completely wrong. *With pivoting* (swap rows): $x + y = 2,\ 0.0001x + y = 1$; the multiplier is 0.0001, $y(1 - 0.0001) = 1 - 0.0002$ gives $y = 1.00$ and $x = 2 - 1.00 = 1.00$, correct. Pivoting is right.

**11.** $n^{3}/3 = 125000/3 \approx 41\,667$ multiplications for the factorisation; each extra right-hand side costs one forward and one back substitution, $n^{2} = 2500$.

**12.** $c'_1 = -0.5,\ d'_1 = 0.5$; $c'_2 = -1/(2 - 0.5) = -0.6667,\ d'_2 = (0 + 0.5)/1.5 = 0.3333$; $d'_3 = (1 + 0.3333)/(2 - 0.6667) = 1$. Back substitution: $x_3 = 1$, $x_2 = 0.3333 + 0.6667(1) = 1$, $x_1 = 0.5 + 0.5(1) = 1$. Solution $(1, 1, 1)$.

**13.** $l_{11} = 3$, $l_{21} = 3/3 = 1$, $l_{22} = \sqrt{5 - 1} = 2$: $L = \begin{bmatrix} 3 & 0 \\ 1 & 2 \end{bmatrix}$. Forward: $3y_1 = 12 \Rightarrow y_1 = 4$; $y_1 + 2y_2 = 8 \Rightarrow y_2 = 2$. Back with $L^{T}$: $2x_2 = 2 \Rightarrow x_2 = 1$; $3x_1 + x_2 = 4 \Rightarrow x_1 = 1$. Solution $(1, 1)$.

**14.** $\|A\|_{\infty} = \max(3, 7) = 7$. $A^{-1} = \begin{bmatrix} -2 & 1 \\ 1.5 & -0.5 \end{bmatrix}$, $\|A^{-1}\|_{\infty} = \max(3, 2) = 3$. $\kappa_{\infty} = 7 \times 3 = 21$: well conditioned.

**15.** The error is $e = A^{-1}r$ and $\|A^{-1}\|_{\infty} = 40001$ is huge. A residual of $5\times 10^{-5}$ can therefore hide an error of order $40001\times 5\times 10^{-5} \approx 2$; the actual error is $(-1, 0.5)$. A small residual proves a small error only for a well-conditioned matrix.

**16.** Row 1: $|2| < |3|$, so no. Interchange the equations: $5x + y = 7,\ 2x + 3y = 8$; now $5 > 1$ and $3 > 2$. Gauss-Seidel: $x = (7 - y)/5,\ y = (8 - 2x)/3$. Iteration 1: $x = 1.4,\ y = 1.7333$; iteration 2: $x = 1.0533,\ y = 1.9644$; the exact solution is $(1, 2)$.

**17.** Reduction by $10^{-6}$ needs $k \ge \ln(10^{-6})/\ln(0.9) = 131.1$, so **132** Jacobi iterations. With $\rho_{GS} = 0.81$: $k \ge 65.6$, so **66** Gauss-Seidel iterations: half the work.

**18.** First equation: $x^{(k+1)} = (1 - 1.1)x^{(k)} + \dfrac{1.1}{4}\left(3 + y^{(k)}\right)$. From $(0, 0)$: $x = 0.275 \cdot 3 = 0.825$. Second equation with the new $x$: $y = 0 + \dfrac{1.1}{4}(3 + 0.825) = 1.0519$.

**19.** Discs: centre 5 radius 1 ($[4, 6]$), centre 4 radius 2 ($[2, 6]$), centre 3 radius 1 ($[2, 4]$). All eigenvalues lie in $[2, 6]$. The matrix is symmetric, so the eigenvalues are real, and since none can be below 2 they are all positive: the matrix is positive definite. (Exact eigenvalues: 2.268, 4, 5.732.)

**20.** Solve $Ay = x$ with $A^{-1} = \tfrac{1}{3}\begin{bmatrix} 2 & -1 \\ -1 & 2 \end{bmatrix}$. Step 1: $y = (0.6667, -0.3333)$, scaled $x = (1, -0.5)$, estimate $1/0.6667 = 1.5$. Step 2: $y = (0.8333, -0.6667)$, $x = (1, -0.8)$, estimate 1.2. Step 3 would give 1.071. The estimates fall towards **1**, the eigenvalue nearest 0 (the eigenvalues are 1 and 3), with eigenvector $(1, -1)$.

:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Solve $10 x + y + z = 12 ,\  2 x + 10 y + z = 13 ,\  2 x + 2 y + 10 z = 14$ by Gauss elimination.**

*Augmented matrix.* [10 1 1 | 12; 2 10 1 | 13; 2 2 10 | 14].

*Step 1 (pivot $10 ) . \ast$ m21 = $\frac{2}{10} = 0.2$ and m31 = 0.2: R2 = R2 - 0.2R1 gives [0 9.8 0.8 | 10.6]; R3 = R3 - 0.2R1 gives [0 1.8 9.8 | 11.6].

*Step 2 (pivot $9.8 ) . \ast$ m32 = $1.8 / 9.8 = 0.18367$: R3 = R3 - 0.18367R2 gives [0 0 9.6531 | 9.6531] (Figure 4.1).

*Back substitution.* $z = 9.6531 / 9.6531$ = **1**; $y = \frac{10.6 - 0.8 x 1}{9.8}$ = **1**; $x = \frac{12 - 1 - 1}{10}$ = **1**. *Check:* $10 + 1 + 1 = 12 ,\  2 + 10 + 1 = 13 ,\  2 + 2 + 10 = 14$. *Note:* with a zero or very small pivot, rows must be swapped (partial pivoting) to keep rounding errors small. The work is about $\frac{n^{3}}{3}$ multiplications. *Conclusion:* the solution is $x = y = z = 1$.

**Q2 (5 marks). Solve the same system by the Jacobi and Gauss-Seidel methods (four iterations from zero). State the condition for convergence.**

*Formulas.* $x = \frac{12 - y - z}{10} ,\  y = \frac{13 - 2 x - z}{10} ,\  z = \frac{14 - 2 x - 2 y}{10}$. Jacobi uses only old values of an iteration; Gauss-Seidel uses each new value immediately.

| Iteration | Jacobi $(x ,\  y ,\  z)$ | Gauss-Seidel $(x ,\  y ,\  z)$ |
|---|---|---|
| 1 | 1.2000, 1.3000, 1.4000 | 1.2000, 1.0600, 0.9480 |
| 2 | 0.9300, 0.9200, 0.9000 | 0.9992, 1.0054, 0.9991 |
| 3 | 1.0180, 1.0240, 1.0300 | 0.9996, 1.0002, 1.0000 |
| 4 | 0.9946, 0.9934, 0.9916 | 1.0000, 1.0000, 1.0000 |

Gauss-Seidel is already correct to four decimals after four sweeps, while Jacobi still has an error of 0.008 (Figure 4.2). *Convergence:* guaranteed when the matrix is **strictly diagonally dominant**, that is $|a (i i)|$ > sum of $|a (i j)|$ for *j* not equal *i* in every row; here $10 > 2 ,\  10 > 3$ and $10 > 4$. *Conclusion:* iterative methods suit large sparse systems and Gauss-Seidel is usually about twice as fast.

**Q3 (10 marks). Compare direct and iterative methods for linear systems. Explain LU factorisation and ill-conditioning with an example.**

*Introduction.* To solve Ax = *b*, **direct methods** (Gauss elimination, Gauss-Jordan, LU) give the answer after a fixed number of operations, while **iterative methods** (Jacobi, Gauss-Seidel) improve a guess until it is accurate enough.

*Direct methods.* Gauss elimination reduces A to upper-triangular form and back-substitutes, with cost about $\frac{n^{3}}{3}$. **LU factorisation** writes $A = L U$ with L lower triangular (holding the multipliers, here 0.2, 0.2, 0.18367) and U upper triangular (the reduced matrix). To solve for any *b*, first solve Ly = *b* by forward substitution, then Ux = *y* by back substitution, each costing only $n^{2}$. LU is therefore ideal when the same matrix is used with many right-hand sides. Gauss-Jordan continues to a diagonal form and can find an inverse but costs more.

*Iterative methods.* They store only the nonzero entries and need diagonal dominance (Figure 4.2). For a system with a million unknowns, such as a weather grid, they are the only practical choice.

*Ill-conditioning.* A system is ill-conditioned when small changes in the data cause large changes in the solution (Plate 4.1b). Example: $x + y = 2$ and *x* + 1.0001y = 2.0001 has the solution $x = 1 ,\  y = 1$. Changing the right side to 2.0002 gives $y = 0.0002 / 0.0001 = 2$ and $x = 0$: a change of 0.0001 in one datum changed the answer from (1, 1) to (0, 2). The condition number is $\mid |A| \mid x \mid |A^{- 1}| \mid = 2.0001 x$ 20,001, about 40,000, so relative errors in the data can be magnified up to 40,000 times.

| Point | Direct (LU) | Iterative (Gauss-Seidel) |
|---|---|---|
| Answer after | Fixed steps | Until tolerance met |
| Cost | $\frac{n^{3}}{3}$ | $n^{2}$ per sweep, few sweeps |
| Memory | Fills in zeros | Keeps matrix sparse |
| Condition | Works for any nonsingular A | Needs diagonal dominance |
| Best for | Small and medium systems | Very large sparse systems |

*Conclusion.* Use LU with partial pivoting for ordinary systems, iterative methods for huge sparse ones, and always check the condition number before trusting an answer.

**Q4 (5 marks). Apply Gauss–Seidel and SOR with $\omega = 1.25$ to $4x - y = 3,\ -x + 4y = 3$ (four sweeps from zero). Is over-relaxation always faster?**

*Formula.* SOR: $x^{(k+1)} = (1 - \omega)x^{(k)} + \dfrac{\omega}{4}\left(3 + y^{(k)}\right)$, $y^{(k+1)} = (1 - \omega)y^{(k)} + \dfrac{\omega}{4}\left(3 + x^{(k+1)}\right)$; $\omega = 1$ is Gauss–Seidel. The exact solution is $x = y = 1$.

| Sweep | G–S $x$ | G–S $y$ | G–S max error | SOR $x$ | SOR $y$ | SOR max error |
|---|---|---|---|---|---|---|
| 1 | 0.750000 | 0.937500 | 2.5e-01 | 0.937500 | 1.230469 | 2.3e-01 |
| 2 | 0.984375 | 0.996094 | 1.6e-02 | 1.087646 | 0.969772 | 8.8e-02 |
| 3 | 0.999023 | 0.999756 | 9.8e-04 | 0.968642 | 0.997758 | 3.1e-02 |
| 4 | 0.999939 | 0.999985 | 6.1e-05 | 1.007139 | 1.002791 | 7.1e-03 |

*Explanation.* The Jacobi spectral radius is 0.25, so $\omega_{\text{opt}} = 2/(1 + \sqrt{1 - 0.0625}) = 1.016$, almost 1. Gauss–Seidel is already near the optimum, and $\omega = 1.25$ overshoots (the error changes sign each sweep). *Conclusion:* over-relaxation helps only when the system is slowly convergent (a spectral radius near 1, as in the 8 × 8 example of Section 4.11); choosing $\omega$ carelessly can be worse than $\omega = 1$.
