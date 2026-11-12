---
subject: Mathematics II
grade: BCA Semester 2
unit: 6
title: Computational Methods
area: BCA 154 · Mathematics II · Unit 6
---

Calculus tells us how things change; **computational methods** tell us how to *get numbers out* when no neat formula exists. This unit covers the last unit of the TU syllabus: linear programming (graphical method, simplex method up to three variables, duality) and the numerical methods that a computer actually runs: matrix inversion, Gauss elimination, Gauss-Seidel iteration, the bisection method and the Newton-Raphson method.

::: key What this unit gives you
- Formulating a linear programming problem (LPP) and solving two-variable problems graphically with corner points.
- The simplex method in tableau form, slack variables, pivoting, and reading the optimum.
- The dual of an LPP and the duality theorem.
- Solving $A X = B$ by matrix inversion, Gauss elimination (with back substitution) and Gauss-Seidel iteration.
- Finding roots of $f(x) = 0$ by bisection and Newton-Raphson, with error control.
:::

## 6.1 Linear programming problems

A **linear programming problem** asks us to maximise or minimise a linear **objective function** subject to linear **constraints** (inequalities) and **non-negativity** conditions. Typical uses: product mix, diet cost, transport, and scheduling.

**Steps of formulation:** (1) name the decision variables ($x$, $y$); (2) write the objective $Z = c_{1} x + c_{2} y$; (3) write each resource limit as an inequality; (4) add $x, y \ge 0$.

::: example Worked example: formulating a product-mix problem
A computer lab assembles two products. A **router kit** gives a profit of Rs 3,000 and uses 1 hour of soldering and 1 hour of testing. A **sensor kit** gives Rs 2,000 and uses 3 hours of soldering and 1 hour of testing. The lab has 6 soldering hours and 4 testing hours per day. Let $x$ = routers, $y$ = sensors (in units of Rs 1,000 profit).
Maximise $Z = 3 x + 2 y$ subject to $x + 3 y \le 6$ (soldering), $x + y \le 4$ (testing), $x, y \ge 0$.
:::

### Linear inequalities and the feasible region

A linear inequality in two variables, $a x + b y \le c$, describes a **half-plane**. To graph it: draw the line $a x + b y = c$, test the origin $(0, 0)$ and shade the side that satisfies the inequality. The **feasible region** is the intersection of all the half-planes. It is a convex polygon (or unbounded region).

### The graphical (corner point) method

The key theorem: if an optimum exists, it occurs at a **corner point (vertex)** of the feasible region. So: (1) draw the region, (2) find every corner by solving pairs of boundary lines, (3) evaluate $Z$ at each corner, (4) choose the largest (maximum) or smallest (minimum).

```svgfig label="6.1" caption="Feasible region of the product-mix problem. Corner points are O(0,0), A(4,0), B(3,1) and C(0,2). The dashed line is the objective 3x + 2y = 6; sliding it outwards parallel to itself, the last corner it touches is A(4,0), where Z = 12."
f = Fig(560, 300)
f.line(50, 260, 420, 260, color=NAVY, sw=1.8)
f.line(50, 260, 50, 30, color=NAVY, sw=1.8)
f.text(430, 264, "x", size=12, color=NAVY, bold=True, anchor="start")
f.text(50, 22, "y", size=12, color=NAVY, bold=True)
f.poly([(50, 260), (270, 260), (215, 205), (50, 150)], fill="#bbf7d0", stroke=TEAL, sw=2)
f.line(50, 40, 270, 260, color=RED, sw=1.6)
f.line(50, 150, 380, 260, color=AMBER, sw=1.6)
f.line(160, 260, 50, 95, color=NAVY, sw=1.6, dash=True)
f.circle(270, 260, 5, fill=RED, stroke=RED)
f.circle(215, 205, 4, fill=NAVY, stroke=NAVY)
f.circle(50, 150, 4, fill=NAVY, stroke=NAVY)
f.text(285, 248, "A (4, 0)  Z = 12", size=11, color=RED, bold=True, anchor="start")
f.text(228, 196, "B (3, 1)  Z = 11", size=11, color=NAVY, bold=True, anchor="start")
f.text(62, 144, "C (0, 2)  Z = 4", size=11, color=NAVY, bold=True, anchor="start")
f.text(80, 276, "O  Z = 0", size=11, color=NAVY, bold=True, anchor="start")
f.text(270, 100, "x + y = 4", size=11, color=RED, bold=True, anchor="start")
f.text(300, 200, "x + 3y = 6", size=11, color=AMBER, bold=True, anchor="start")
f.text(130, 118, "3x + 2y = 6", size=10.5, color=NAVY, anchor="start")
```

::: example Worked example: graphical solution
Corners: $O(0,0)$; $A(4,0)$ from $y = 0$ and $x + y = 4$ (check $x + 3 y = 4 \le 6$); $C(0,2)$ from $x = 0$ and $x + 3 y = 6$; $B$ from $x + y = 4$ and $x + 3 y = 6$: subtract to get $2 y = 2$, $y = 1$, $x = 3$.
$Z(O) = 0$, $Z(A) = 12$, $Z(B) = 9 + 2 = 11$, $Z(C) = 4$.
**Maximum $Z = 12$ at $x = 4$, $y = 0$** (4 router kits, no sensor kits; profit Rs 12,000). Soldering time used is 4 of 6 hours, so 2 hours are left over (slack).
:::

**Special cases.** *No feasible region*: the constraints contradict each other. *Unbounded*: the region extends forever in the direction of improvement and the maximum does not exist. *Multiple optima*: the objective line is parallel to a boundary edge, so every point on that edge (and both its corners) is optimal. *Degeneracy*: more than two lines meet at a corner.

## 6.2 The simplex method (up to three variables)

The graphical method fails beyond two variables. The **simplex method** moves from corner to better corner algebraically, using a table (tableau).

**Standard form (maximise).** Convert each $\le$ constraint to an equation by adding a **slack variable** ($s_{1}, s_{2} \ge 0$) that measures unused resource. The objective is written $Z - 3 x - 2 y = 0$ so that its row holds the coefficients $-3$ and $-2$.

**Algorithm.**
1. Write the initial tableau. The slack variables are the first **basic** variables (value = right-hand side).
2. **Entering variable:** the column with the most negative entry in the objective row. If no entry is negative, stop: the solution is optimal.
3. **Leaving variable (minimum ratio test):** divide each right-hand side by the positive entry of the entering column and choose the smallest ratio; that row is the **pivot row**.
4. **Pivot:** divide the pivot row by the pivot element, then use row operations to make all other entries of the entering column zero.
5. Repeat from step 2.

::: example Worked example: simplex on the product-mix problem
Maximise $Z = 3 x + 2 y$, $x + y + s_{1} = 4$, $x + 3 y + s_{2} = 6$.

| Basis | $x$ | $y$ | $s_1$ | $s_2$ | RHS | ratio |
|---|---|---|---|---|---|---|
| $s_1$ | 1 | 1 | 1 | 0 | 4 | 4 / 1 = **4** |
| $s_2$ | 1 | 3 | 0 | 1 | 6 | 6 / 1 = 6 |
| $Z$ | -3 | -2 | 0 | 0 | 0 | |

$x$ enters (most negative $-3$); ratios 4 and 6, so row $s_1$ leaves; pivot element 1. Row operations: $R_{2} \leftarrow R_{2} - R_{1}$, $R_{Z} \leftarrow R_{Z} + 3 R_{1}$.

| Basis | $x$ | $y$ | $s_1$ | $s_2$ | RHS |
|---|---|---|---|---|---|
| $x$ | 1 | 1 | 1 | 0 | 4 |
| $s_2$ | 0 | 2 | -1 | 1 | 2 |
| $Z$ | 0 | 1 | 3 | 0 | 12 |

The objective row has no negative entry, so this is optimal: **$x = 4$, $y = 0$, $s_{2} = 2$, $Z = 12$**, the same as the graphical answer (and the slack of 2 matches the 2 unused soldering hours).
:::

**Reading the tableau.** A basic variable equals the RHS of its row; non-basic variables are zero. In the final objective row, the entries under the slack variables ($3$ under $s_{1}$) are the **shadow prices**: one more testing hour would raise $Z$ by 3 (Rs 3,000). The entry 0 under $s_{2}$ says extra soldering time is worthless now. For a **minimisation** problem, either maximise $-Z$, or solve the dual (6.3). For $\ge$ constraints the **big-M** or two-phase method is used; the TU syllabus requires only the $\le$ type with up to three variables.

## 6.3 Duality

Every LPP (the **primal**) has a companion LPP (the **dual**). For the primal *maximise $c^{T} x$ subject to $A x \le b,\ x \ge 0$*, the dual is *minimise $b^{T} w$ subject to $A^{T} w \ge c,\ w \ge 0$*. Rules: the number of dual variables equals the number of primal constraints; the RHS of the primal becomes the objective of the dual; the objective coefficients become the RHS; the inequality direction reverses; the matrix is transposed.

::: example Worked example: writing and solving the dual
Primal: maximise $Z = 3 x + 2 y$ s.t. $x + y \le 4$, $x + 3 y \le 6$.
**Dual:** minimise $W = 4 u + 6 v$ s.t. $u + v \ge 3$ (from $x$), $u + 3 v \ge 2$ (from $y$), $u, v \ge 0$.
Corner points of the dual region: $(3, 0)$ (where $u + v = 3$ meets $v = 0$) with $W = 12$; $(0, 3)$ with $W = 18$ and the point where the two lines meet, $u + v = 3$, $u + 3 v = 2$: $v = -0.5$, not allowed. The minimum is **$W = 12$** at $u = 3$, $v = 0$. It equals the primal maximum 12, and $u = 3$, $v = 0$ are the shadow prices read from the simplex tableau.
:::

**Duality theorem.** If the primal has an optimal solution, so has the dual, and the optimal values are **equal**. **Weak duality:** any feasible $Z \le$ any feasible $W$. Why it matters: the dual often has fewer constraints (easier to solve), and its variables are the **economic value of each resource**.

## 6.4 Solving linear systems on a computer

### Matrix inversion method

Write the system as $A X = B$. If $\det A \ne 0$ then $X = A^{-1} B$, where $A^{-1} = \frac{1}{\det A}\,\mathrm{adj}\,A$.

::: example Worked example: matrix inversion
Solve $2 x + y = 5$, $x + 3 y = 10$. Here $A = \begin{bmatrix} 2 & 1 \\ 1 & 3 \end{bmatrix}$, $\det A = 6 - 1 = 5$, $A^{-1} = \frac{1}{5} \begin{bmatrix} 3 & -1 \\ -1 & 2 \end{bmatrix}$. Then $X = \frac{1}{5} \begin{bmatrix} 3 \cdot 5 - 10 \\ -5 + 2 \cdot 10 \end{bmatrix} = \begin{bmatrix} 1 \\ 3 \end{bmatrix}$. Check: $2 + 3 = 5$ and $1 + 9 = 10$.
:::

Inversion is clear on paper but costs about $n^{3}$ operations and is less accurate than elimination, so software solves $A X = B$ directly without forming $A^{-1}$.

### Gauss elimination

Use row operations to turn the augmented matrix $[A \mid B]$ into **upper-triangular** form (forward elimination), then solve from the last equation upward (**back substitution**). **Partial pivoting** swaps rows so that the pivot is the largest available entry in its column, which controls rounding error.

::: example Worked example: Gauss elimination
Solve $2 x + y - z = 8$, $-3 x - y + 2 z = -11$, $-2 x + y + 2 z = -3$.
Augmented: $\left[\begin{array}{ccc|c} 2 & 1 & -1 & 8 \\ -3 & -1 & 2 & -11 \\ -2 & 1 & 2 & -3 \end{array}\right]$.
$R_{2} \leftarrow R_{2} + \frac{3}{2} R_{1}$: $(0,\ 0.5,\ 0.5 \mid 1)$. $R_{3} \leftarrow R_{3} + R_{1}$: $(0,\ 2,\ 1 \mid 5)$.
$R_{3} \leftarrow R_{3} - 4 R_{2}$: $(0,\ 0,\ -1 \mid 1)$.
Back substitution: $-z = 1 \Rightarrow z = -1$; $0.5 y + 0.5(-1) = 1 \Rightarrow y = 3$; $2 x + 3 + 1 = 8 \Rightarrow x = 2$.
**Solution $(2, 3, -1)$.** Check in the second equation: $-6 - 3 - 2 = -11$.
:::

Work for a system of $n$ equations is about $\frac{2}{3} n^{3}$ multiplications. If a zero pivot cannot be removed by swapping rows, $\det A = 0$ and the system has no unique solution.

### Gauss-Seidel iteration

For large sparse systems an **iterative** method is better: start with a guess and improve it. Solve the $i$-th equation for $x_{i}$ and **use every new value immediately**. Convergence is guaranteed when the matrix is **strictly diagonally dominant** ($|a_{ii}| > \sum_{j \ne i} |a_{ij}|$ in each row); arrange the equations that way first.

::: example Worked example: Gauss-Seidel
Solve $10 x + y + z = 12$, $2 x + 10 y + z = 13$, $2 x + 2 y + 10 z = 14$ (diagonally dominant). Formulas: $x = \frac{12 - y - z}{10}$, $y = \frac{13 - 2 x - z}{10}$, $z = \frac{14 - 2 x - 2 y}{10}$. Start $(0, 0, 0)$.

| Iteration | $x$ | $y$ | $z$ |
|---|---|---|---|
| 1 | 1.2000 | 1.0600 | 0.9480 |
| 2 | 0.9992 | 1.0054 | 0.9991 |
| 3 | 0.9996 | 1.0002 | 1.0001 |
| 4 | 1.0000 | 1.0000 | 1.0000 |

The solution is $(1, 1, 1)$. Iteration 1: $x = (12 - 0 - 0)/10 = 1.2$; $y = (13 - 2.4 - 0)/10 = 1.06$ (it uses the *new* $x$); $z = (14 - 2.4 - 2.12)/10 = 0.948$. Stop when two successive iterations differ by less than the tolerance.
:::

## 6.5 Solving non-linear equations f(x) = 0

### Bisection method

If $f$ is continuous on $[a, b]$ and $f(a) f(b) < 0$, the Intermediate Value Theorem guarantees a root in between. Take the midpoint $m = \frac{a + b}{2}$; keep the half where the sign changes; repeat. After $n$ steps the interval has length $\frac{b - a}{2^{n}}$, so the iterations needed for tolerance $\varepsilon$ are $n \ge \log_{2} \frac{b - a}{\varepsilon}$. It always converges, but slowly (one binary digit per step).

::: example Worked example: bisection for $x^{3} - x - 2 = 0$
$f(1) = -2 < 0$ and $f(2) = 4 > 0$, so a root lies in $[1, 2]$.

| $n$ | $a$ | $b$ | $m$ | $f(m)$ |
|---|---|---|---|---|
| 1 | 1 | 2 | 1.5 | -0.1250 |
| 2 | 1.5 | 2 | 1.75 | 1.6094 |
| 3 | 1.5 | 1.75 | 1.625 | 0.6660 |
| 4 | 1.5 | 1.625 | 1.5625 | 0.2522 |
| 5 | 1.5 | 1.5625 | 1.53125 | 0.0591 |
| 6 | 1.5 | 1.53125 | 1.5156 | -0.0341 |
| 7 | 1.5156 | 1.53125 | 1.5234 | 0.0123 |

After 7 steps the root is in $[1.5156, 1.5313]$, about 1.52. Accuracy $0.001$ needs $n \ge \log_{2} (1 / 0.001) = 9.97$, so **10 iterations**.
:::

### Newton-Raphson method

Replace the curve by its tangent at the current guess and take the tangent's zero as the next guess:
$$x_{n+1} = x_{n} - \frac{f(x_{n})}{f'(x_{n})}.$$
Near a simple root it converges **quadratically** (the number of correct digits roughly doubles each step), but it needs $f'$, can fail if $f'(x_{n}) \approx 0$, and may diverge from a bad start.

::: example Worked example: Newton-Raphson for the same equation
$f(x) = x^{3} - x - 2$, $f'(x) = 3 x^{2} - 1$, $x_{0} = 1.5$.
$x_{1} = 1.5 - \frac{-0.125}{5.75} = 1.521739$.
$x_{2} = 1.521739 - \frac{f(1.521739)}{f'(1.521739)} = 1.521380$. The next step stays at $1.52138$.
**Root $\approx 1.52138$** in two steps, against ten bisection steps for a similar accuracy.
:::

**Choosing a method.** Use bisection when a safe bracket exists and reliability matters; Newton-Raphson when $f'$ is easy and a good start is known; in practice, software starts with bisection and switches to Newton-like steps.

## Formula and fact sheet

- LPP: maximise $Z = c^{T} x$, $A x \le b$, $x \ge 0$. Optimum at a corner point.
- Simplex: enter most negative objective entry; leave minimum ratio; pivot; stop when no negative entry remains.
- Dual: $\min b^{T} w$, $A^{T} w \ge c$; optimal values are equal.
- Gauss elimination: forward elimination then back substitution, about $\frac{2}{3} n^{3}$ operations.
- Gauss-Seidel: use new values at once; converges for strictly diagonally dominant $A$.
- Bisection: $n \ge \log_{2} \frac{b - a}{\varepsilon}$. Newton-Raphson: $x_{n+1} = x_{n} - \frac{f}{f'}$.

## Chapter summary

- A linear programming problem has a linear objective and linear constraints; the optimum lies at a corner of the feasible region and can be found graphically (two variables) or by the simplex tableau.
- The dual problem has the same optimal value, and its variables are the shadow prices of the resources.
- Linear systems are solved by inversion, Gauss elimination or Gauss-Seidel iteration; roots of non-linear equations by bisection (safe, slow) or Newton-Raphson (fast, needs a derivative).

## Practice

1. Maximise $Z = 2 x + 3 y$ subject to $x + y \le 4$, $x + 3 y \le 6$, $x, y \ge 0$ by the graphical method.
2. Solve problem 1 by the simplex method and read the shadow prices.
3. Write the dual of problem 1 and solve it.
4. Solve by Gauss elimination: $x + y + z = 6$, $2 y + 5 z = -4$, $2 x + 5 y - z = 27$.
5. Solve $3 x + 2 y = 7$, $x + 4 y = 9$ by the matrix inversion method.
6. Perform two Gauss-Seidel iterations on $4 x + y = 9$, $x + 3 y = 7$ starting from $(0, 0)$.
7. Apply three bisection steps to $x^{2} - 5 = 0$ on $[2, 3]$.
8. Apply two Newton-Raphson steps to $x^{2} - 5 = 0$ from $x_{0} = 2$.

::: note Answers and worked solutions
**1.** Corners $(0,0), (4,0), (3,1), (0,2)$ give $Z = 0, 8, 9, 6$. **Maximum $Z = 9$ at $(3, 1)$.**

**2.** $y$ enters (most negative $-3$); ratios $4/1 = 4$ and $6/3 = 2$, so $s_{2}$ leaves. After pivoting, $x$ enters (entry $-1$); ratios $2 / \frac{2}{3} = 3$ and $2 / \frac{1}{3} = 6$, so $s_{1}$ leaves. Final row: $Z = 9$, $x = 3$, $y = 1$; shadow prices $\frac{3}{2}$ and $\frac{1}{2}$.

**3.** Minimise $W = 4 u + 6 v$ s.t. $u + v \ge 2$, $u + 3 v \ge 3$. Corners: $(1.5, 0.5)$ with $W = 9$; $(0, 2)$ with $W = 12$; $(3, 0)$ with $W = 12$. **Minimum $W = 9$**, equal to the primal maximum.

**4.** From the second equation $2 y + 5 z = -4$; eliminating $x$: $R_{3} - 2 R_{1}$ gives $3 y - 3 z = 15$, so $y - z = 5$. With $R_{2}$: $2 (z + 5) + 5 z = -4 \Rightarrow z = -2$, $y = 3$, $x = 6 - 3 + 2 = 5$. **$(5, 3, -2)$.**

**5.** $\det = 12 - 2 = 10$; $A^{-1} = \frac{1}{10} \begin{bmatrix} 4 & -2 \\ -1 & 3 \end{bmatrix}$; $X = \frac{1}{10} (28 - 18, -7 + 27) = (1, 2)$. **$x = 1$, $y = 2$.**

**6.** Iteration 1: $x = 9/4 = 2.25$, $y = (7 - 2.25)/3 = 1.5833$. Iteration 2: $x = (9 - 1.5833)/4 = 1.8542$, $y = (7 - 1.8542)/3 = 1.7153$. (Exact: $x = 20/11 = 1.8182$, $y = 1.7273$.)

**7.** $f(2) = -1$, $f(3) = 4$. $m = 2.5$: $f = 1.25$, root in $[2, 2.5]$. $m = 2.25$: $f = 0.0625$, root in $[2, 2.25]$. $m = 2.125$: $f = -0.4844$, root in $[2.125, 2.25]$. Estimate **2.1875** (true root $\sqrt{5} = 2.2361$).

**8.** $x_{1} = 2 - \frac{-1}{4} = 2.25$; $x_{2} = 2.25 - \frac{0.0625}{4.5} = 2.2361$. **$\sqrt{5} \approx 2.2361$.**
:::
