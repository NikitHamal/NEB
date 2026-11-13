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
- How the methods behave: special LPP cases, degeneracy and sensitivity, pivoting and ill-conditioning, convergence order, and when Newton-Raphson fails.
- Running everything in Excel, MATLAB and Python, as the syllabus's "(Excel/Matlab)" note requires.
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

### Formulating more problems

The hardest step in any LPP is not the arithmetic but the translation from words to inequalities. Two further models show the usual patterns: a **minimisation** with $\ge$ constraints (a diet or cost problem) and a **three-variable maximisation** (a product mix with three resources).

::: example Worked example: a minimum-cost diet
A hostel mess mixes two foods. **Food 1** costs Rs 20 per unit and gives 2 units of protein and 1 unit of iron. **Food 2** costs Rs 30 per unit and gives 1 unit of protein and 2 units of iron. Each student needs at least 8 units of protein and 10 units of iron per day. Find the cheapest mix.

Let $x$ = units of Food 1 and $y$ = units of Food 2. **Minimise** $Z = 20 x + 30 y$ subject to $2 x + y \ge 8$ (protein), $x + 2 y \ge 10$ (iron), $x, y \ge 0$.

The feasible region lies *above* both lines and is unbounded, but because the costs are positive $Z$ cannot fall forever, so a minimum exists at a corner. Corners: $(0, 8)$ from $x = 0$ and $2 x + y = 8$; $(10, 0)$ from $y = 0$ and $x + 2 y = 10$; and the intersection of the two lines: subtract $2 \times$ (iron) from (protein) to get $-3 y = -12$, $y = 4$, $x = 2$.
$Z(0, 8) = 240$, $Z(2, 4) = 40 + 120 = 160$, $Z(10, 0) = 200$.
**Minimum cost Rs 160 at $x = 2$, $y = 4$.** Both nutrient constraints are exactly met, so nothing is wasted.
:::

::: example Worked example: three products, three resources
A workshop makes products $A$, $B$, $C$ with profits Rs 5, 4 and 3 (in thousands) per unit. Machine hours, labour hours and material (kg) are limited to 5, 11 and 8. Per unit of $A$, $B$, $C$: machine time is $2, 3, 1$; labour $4, 1, 2$; material $3, 4, 2$.
Let $x, y, z$ be the quantities. **Maximise** $Z = 5 x + 4 y + 3 z$ subject to
$2 x + 3 y + z \le 5$, $\quad 4 x + y + 2 z \le 11$, $\quad 3 x + 4 y + 2 z \le 8$, $\quad x, y, z \ge 0$.
This has three variables, so a drawing is impossible and we use the simplex method in 6.2, which gives $x = 2$, $y = 0$, $z = 1$ and $Z = 13$.
:::

::: tip How to translate a word problem
Underline the **quantity you control** (these are the variables), the **single number to maximise or minimise** (objective), and every phrase like *at most*, *at least*, *no more than*, *a minimum of* (constraints). "At most" gives $\le$, "at least" gives $\ge$. Always write the units next to each constraint, and state $x, y \ge 0$.
:::

### The three special cases in pictures

Not every LPP has one neat optimum. Three things can go wrong, and each has a clear graphical signature.

```svgfig label="6.2" caption="The three special cases of a two-variable LPP. (a) Infeasible: x + y <= 2 and x + y >= 4 share no point, so there is no feasible region. (b) Unbounded: the strip between x - y = 2 and y - x = 3 runs off to infinity, so Z = x + y can be made as large as we like. (c) Many optima: the objective line 2x + 2y = 8 lies along the edge from (1, 3) to (3, 1), so every point of that edge gives Z = 8."
f = Fig(740, 262)
s = 34
def P(i, x, y):
    return (34 + i * 245 + x * s, 215 - y * s)
titles = ["(a) Infeasible", "(b) Unbounded", "(c) Many optimal points"]
for i in range(3):
    f.text(34 + i * 245 + 85, 20, titles[i], size=12, color=NAVY, bold=True)
    f.arrow([P(i, 0, 0), P(i, 5.3, 0)], color=SLATE, sw=1.3)
    f.arrow([P(i, 0, 0), P(i, 0, 5.3)], color=SLATE, sw=1.3)
    f.text(P(i, 5.3, 0)[0] + 4, 232, "x", size=11, color=SLATE, italic=True, anchor="start")
    f.text(P(i, 0, 5.3)[0] + 6, P(i, 0, 5.3)[1] + 4, "y", size=11, color=SLATE, italic=True, anchor="start")
f.poly([P(0, 0, 0), P(0, 2, 0), P(0, 0, 2)], fill="#fecaca", stroke=RED, sw=1.6)
f.line(*P(0, 4, 0), *P(0, 0, 4), color=AMBER, sw=2)
f.text(P(0, 2.2, 2.2)[0], P(0, 2.2, 2.2)[1] - 4, "x + y = 4", size=10.5, color=AMBER, bold=True, anchor="start")
f.text(P(0, 0.2, 0.35)[0], P(0, 0.2, 0.35)[1] - 2, "x+y<=2", size=9.5, color=RED, bold=True, anchor="start")
f.text(P(0, 2.5, 4.4)[0], P(0, 2.5, 4.4)[1], "needs x + y >= 4", size=10, color=AMBER, anchor="start")
f.text(P(0, 2.5, 4.4)[0], P(0, 2.5, 4.4)[1] + 14, "no common point", size=10, color=SLATE, anchor="start")
f.poly([P(1, 0, 0), P(1, 2, 0), P(1, 5, 3), P(1, 5, 5), P(1, 2, 5), P(1, 0, 3)], fill="#bbf7d0", stroke=TEAL, sw=1.6)
f.text(P(1, 3.6, 0.6)[0], P(1, 3.6, 0.6)[1], "x - y = 2", size=10, color=TEAL, bold=True, anchor="start")
f.text(P(1, 0.1, 4.2)[0], P(1, 0.1, 4.2)[1], "y - x = 3", size=10, color=TEAL, bold=True, anchor="start")
f.arrow([P(1, 2.2, 2.5), P(1, 3.8, 4.1)], color=RED, sw=2.2, label="Z grows", lpos=(P(1, 1.25, 3.55)[0] + 70, P(1, 1.25, 3.55)[1] + 38))
f.poly([P(2, 0, 0), P(2, 3, 0), P(2, 3, 1), P(2, 1, 3), P(2, 0, 3)], fill="#bbf7d0", stroke=TEAL, sw=1.6)
f.line(*P(2, 1, 3), *P(2, 3, 1), color=RED, sw=4)
f.circle(*P(2, 1, 3), 4, fill=RED, stroke=RED)
f.circle(*P(2, 3, 1), 4, fill=RED, stroke=RED)
f.text(P(2, 0.9, 3.3)[0] - 4, P(2, 0.9, 3.3)[1], "(1, 3)", size=10, color=RED, bold=True, anchor="end")
f.text(P(2, 3.15, 1.0)[0], P(2, 3.15, 1.0)[1] - 6, "(3, 1)", size=10, color=RED, bold=True, anchor="start")
f.text(P(2, 2.1, 2.3)[0] + 10, P(2, 2.1, 2.3)[1] - 6, "Z = 8 along the edge", size=10, color=RED, bold=True, anchor="start")
```

::: definition Special cases of an LPP
**Infeasible:** the constraints contradict each other, so the feasible region is empty and there is no solution. **Unbounded:** the region extends to infinity in the direction in which $Z$ improves, so the optimum does not exist (this almost always means a constraint was left out of the model). **Alternative (multiple) optima:** the objective line is parallel to a boundary edge, so a whole edge is optimal. The theory of the simplex method tells us how each case appears in the tableau (6.2).
:::

::: example Worked example: recognising each case
(a) Maximise $Z = x + y$ subject to $x + y \le 2$ and $x + y \ge 4$. No point can have $x + y$ both at most 2 and at least 4: **infeasible**.
(b) Maximise $Z = x + y$ subject to $x - y \le 2$ and $y - x \le 3$. Along the line $y = x$, every point is feasible and $Z = 2 x$ grows without limit: **unbounded**.
(c) Maximise $Z = 2 x + 2 y$ subject to $x + y \le 4$, $x \le 3$, $y \le 3$. Corners: $(0,0)$, $(3,0)$, $(3,1)$, $(1,3)$, $(0,3)$ with $Z = 0, 6, 8, 8, 6$. Two adjacent corners tie at the maximum $Z = 8$, so every point on the edge between them, such as $(2, 2)$, is also optimal: **multiple optima**.
:::

::: note Why only corners matter
The feasible region is **convex**: the segment joining any two feasible points stays inside. The objective is a *linear* function, so on any line segment it is largest at an end, never in the middle. Applying this idea again and again shows that no interior point or edge point can beat the best corner. This is also why the simplex method only needs to visit corners.
:::

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

### What the simplex method does geometrically

Each tableau is one **corner** of the feasible region. A pivot slides along one edge to a neighbouring corner with a better $Z$; the minimum-ratio test stops the slide exactly where the next constraint is reached, so the new point stays feasible. For $Z = 2 x + 3 y$ on the region of the product-mix problem, the path is $O \to C \to B$.

```svgfig label="6.3" caption="Simplex path for maximise Z = 2x + 3y subject to x + y <= 4 and x + 3y <= 6. Start at O (Z = 0), the entering variable y (most negative entry -3) slides up the y-axis until x + 3y = 6 is hit at C (0, 2), Z = 6. Then x enters and the path slides along x + 3y = 6 to B (3, 1), Z = 9, where no objective entry is negative. The dashed line 2x + 3y = 9 only touches the region at B."
f = Fig(560, 300)
f.line(50, 260, 420, 260, color=NAVY, sw=1.8)
f.line(50, 260, 50, 30, color=NAVY, sw=1.8)
f.text(430, 264, "x", size=12, color=NAVY, bold=True, anchor="start")
f.text(50, 22, "y", size=12, color=NAVY, bold=True)
f.poly([(50, 260), (270, 260), (215, 205), (50, 150)], fill="#bbf7d0", stroke=TEAL, sw=2)
f.line(298, 260, 50, 95, color=NAVY, sw=1.6, dash=True)
f.text(305, 252, "2x + 3y = 9", size=10.5, color=NAVY, anchor="start")
f.arrow([(50, 258), (50, 154)], color=RED, sw=2.6)
f.arrow([(54, 148), (211, 203)], color=RED, sw=2.6)
for (px, py) in [(50, 260), (50, 150), (215, 205), (270, 260)]:
    f.circle(px, py, 5, fill=RED if (px, py) != (270, 260) else BLUE, stroke=RED)
f.text(64, 276, "O  Z = 0", size=11, color=NAVY, bold=True, anchor="start")
f.text(42, 150, "C (0, 2)", size=10.5, color=RED, bold=True, anchor="end")
f.text(42, 163, "Z = 6", size=10.5, color=RED, bold=True, anchor="end")
f.text(228, 196, "B (3, 1)  Z = 9  optimal", size=11, color=RED, bold=True, anchor="start")
f.text(285, 280, "A (4, 0)  Z = 8 (not visited)", size=10, color=SLATE, anchor="start")
f.text(100, 245, "feasible region", size=11, color=TEAL, bold=True, anchor="start")
f.text(62, 215, "pivot 1: y enters", size=10, color=RED, anchor="start")
f.text(150, 128, "pivot 2: x enters", size=10, color=RED, anchor="start")
```

### Simplex with three variables

The method is identical; only the tableau is wider. We solve the three-product problem formulated above: maximise $Z = 5 x + 4 y + 3 z$ subject to $2 x + 3 y + z \le 5$, $4 x + y + 2 z \le 11$, $3 x + 4 y + 2 z \le 8$.

::: example Worked example: a full three-variable simplex
**Initial tableau** (three slack variables $s_1, s_2, s_3$ form the starting basis).

| Basis | $x$ | $y$ | $z$ | $s_1$ | $s_2$ | $s_3$ | RHS | ratio |
|---|---|---|---|---|---|---|---|---|
| $s_1$ | 2 | 3 | 1 | 1 | 0 | 0 | 5 | 5/2 |
| $s_2$ | 4 | 1 | 2 | 0 | 1 | 0 | 11 | 11/4 |
| $s_3$ | 3 | 4 | 2 | 0 | 0 | 1 | 8 | 8/3 |
| $Z$ | -5 | -4 | -3 | 0 | 0 | 0 | 0 | |

$x$ enters (most negative, $-5$). Ratios $2.5,\ 2.75,\ 2.667$: the smallest is $2.5$, so $s_1$ leaves; pivot element 2. Divide row 1 by 2, then eliminate $x$ from the other rows.

| Basis | $x$ | $y$ | $z$ | $s_1$ | $s_2$ | $s_3$ | RHS | ratio |
|---|---|---|---|---|---|---|---|---|
| $x$ | 1 | 3/2 | 1/2 | 1/2 | 0 | 0 | 5/2 | 5 |
| $s_2$ | 0 | -5 | 0 | -2 | 1 | 0 | 1 | none (entry 0) |
| $s_3$ | 0 | -1/2 | 1/2 | -3/2 | 0 | 1 | 1/2 | **1** |
| $Z$ | 0 | 7/2 | -1/2 | 5/2 | 0 | 0 | 25/2 | |

Only the $z$ column entry $-1/2$ is negative, so $z$ enters. Ratios are only taken for **positive** entries: $5$ and $1$. Row $s_3$ leaves; pivot element $\frac{1}{2}$.

| Basis | $x$ | $y$ | $z$ | $s_1$ | $s_2$ | $s_3$ | RHS |
|---|---|---|---|---|---|---|---|
| $x$ | 1 | 2 | 0 | 2 | 0 | -1 | 2 |
| $s_2$ | 0 | -5 | 0 | -2 | 1 | 0 | 1 |
| $z$ | 0 | -1 | 1 | -3 | 0 | 2 | 1 |
| $Z$ | 0 | 3 | 0 | 1 | 0 | 1 | 13 |

No negative entry remains. **Optimal: $x = 2$, $y = 0$, $z = 1$, $s_2 = 1$, $Z = 13$.** Product $B$ is not made. Check: machine $4 + 0 + 1 = 5 \le 5$ (used up), labour $8 + 0 + 2 = 10 \le 11$ (slack $s_2 = 1$), material $6 + 0 + 2 = 8 \le 8$ (used up). The shadow prices under $s_1, s_2, s_3$ are $1, 0, 1$: an extra machine hour is worth Rs 1,000, an extra labour hour is worth nothing (there is already a spare hour), an extra kg of material is worth Rs 1,000. The entry 3 under $y$ is the **reduced cost**: forcing one unit of $B$ into the plan would lower profit by 3.
:::

### Reading special cases from the tableau

::: key What each special case looks like in a simplex tableau
- **Unbounded:** the entering column has *no positive entry*, so no ratio can be formed and the variable can grow forever.
- **Alternative optima:** in the final tableau a *non-basic* variable has a **0** in the objective row. Pivoting on it gives another optimal corner with the same $Z$.
- **Degenerate:** two rows tie in the minimum-ratio test. After the pivot one basic variable equals 0.
- **Infeasible** (with $\ge$ constraints): an artificial variable stays positive in the final tableau (big-M, below).
:::

::: example Worked example: a degenerate corner
Maximise $Z = x + y$ subject to $x \le 2$, $y \le 2$, $x + y \le 4$. All three lines pass through $(2, 2)$.

| Basis | $x$ | $y$ | $s_1$ | $s_2$ | $s_3$ | RHS |
|---|---|---|---|---|---|---|
| $x$ | 1 | 0 | 1 | 0 | 0 | 2 |
| $s_2$ | 0 | 1 | 0 | 1 | 0 | 2 |
| $s_3$ | 0 | 1 | -1 | 0 | 1 | 2 |
| $Z$ | 0 | -1 | 1 | 0 | 0 | 2 |

$y$ enters, and the ratios for $s_2$ and $s_3$ are both $2/1 = 2$ (a tie). Choosing $s_2$ gives
$x = 2$, $y = 2$ and $s_3 = 0$, $Z = 4$. The slack $s_3$ is still **basic but equals zero**: the corner $(2, 2)$ is degenerate. The solution is correct; the only risk is that a pivot with a zero ratio may not improve $Z$, and in rare cases the method can cycle. Practical codes use tie-breaking rules (for example Bland's rule: choose the lowest-numbered candidate).
:::

### Sensitivity analysis: how long does the answer stay valid?

Prices and resource limits change. We can read how far, without re-solving, from the final tableau of the product-mix problem (maximise $3 x + 2 y$, testing $x + y \le 4$, soldering $x + 3 y \le 6$).

::: example Worked example: ranging the right-hand side and a profit
**Testing hours** $b_1$. The final basis is $\{x, s_2\}$ with $x = b_1$ and $s_2 = 6 - b_1$. Both must stay $\ge 0$, so $0 \le b_1 \le 6$. Within that range the shadow price 3 holds: $b_1 = 4 \to Z = 12$, $b_1 = 5 \to Z = 15$, $b_1 = 6 \to Z = 18$. Beyond 6 hours, soldering ($x \le 6$ when $y = 0$) becomes the limit and extra testing time is worthless.
**Profit of a router kit** $c_1$ (currently 3). The corner $A(4, 0)$ stays optimal while $4 c_1 \ge 3 c_1 + 2$ (compare with $B(3, 1)$), that is $c_1 \ge 2$. At $c_1 = 2$ the corners $A$ and $B$ tie at $Z = 8$ (multiple optima); at $c_1 = 1.5$ the best plan jumps to $B$ with $Z = 6.5$.
:::

::: note The big-M method (beyond the TU syllabus, for understanding)
A $\ge$ or $=$ constraint has no slack variable that can start the basis. We add an **artificial variable** $a_i \ge 0$ and charge it a huge penalty $M$ in the objective ($-M a_i$ when maximising, $+M a_i$ when minimising). The simplex method then drives the artificial variables to zero if the problem is feasible. If an artificial variable is still positive at the optimum, the original problem is **infeasible**. The two-phase method does the same in two stages. For this course, minimisation problems are solved through the dual (next section), which avoids artificial variables.
:::

## 6.3 Duality

Every LPP (the **primal**) has a companion LPP (the **dual**). For the primal *maximise $c^{T} x$ subject to $A x \le b,\ x \ge 0$*, the dual is *minimise $b^{T} w$ subject to $A^{T} w \ge c,\ w \ge 0$*. Rules: the number of dual variables equals the number of primal constraints; the RHS of the primal becomes the objective of the dual; the objective coefficients become the RHS; the inequality direction reverses; the matrix is transposed.

::: example Worked example: writing and solving the dual
Primal: maximise $Z = 3 x + 2 y$ s.t. $x + y \le 4$, $x + 3 y \le 6$.
**Dual:** minimise $W = 4 u + 6 v$ s.t. $u + v \ge 3$ (from $x$), $u + 3 v \ge 2$ (from $y$), $u, v \ge 0$.
Corner points of the dual region: $(3, 0)$ (where $u + v = 3$ meets $v = 0$) with $W = 12$; $(0, 3)$ with $W = 18$ and the point where the two lines meet, $u + v = 3$, $u + 3 v = 2$: $v = -0.5$, not allowed. The minimum is **$W = 12$** at $u = 3$, $v = 0$. It equals the primal maximum 12, and $u = 3$, $v = 0$ are the shadow prices read from the simplex tableau.
:::

**Duality theorem.** If the primal has an optimal solution, so has the dual, and the optimal values are **equal**. **Weak duality:** any feasible $Z \le$ any feasible $W$. Why it matters: the dual often has fewer constraints (easier to solve), and its variables are the **economic value of each resource**.

### Solving a minimisation problem through its dual

A minimisation problem with $\ge$ constraints cannot start the simplex method directly (there is no slack to form a starting corner). Its **dual is a maximisation with $\le$ constraints**, which can. Rule: for *minimise $c^{T} x$ subject to $A x \ge b$, $x \ge 0$* the dual is *maximise $b^{T} w$ subject to $A^{T} w \le c$, $w \ge 0$*.

::: example Worked example: the hostel diet by simplex on the dual
Primal: minimise $Z = 20 x + 30 y$ s.t. $2 x + y \ge 8$, $x + 2 y \ge 10$.
**Dual:** maximise $W = 8 u + 10 v$ s.t. $2 u + v \le 20$ (from the column of $x$), $u + 2 v \le 30$ (from the column of $y$), $u, v \ge 0$.

| Basis | $u$ | $v$ | $s_1$ | $s_2$ | RHS | ratio |
|---|---|---|---|---|---|---|
| $s_1$ | 2 | 1 | 1 | 0 | 20 | 20 |
| $s_2$ | 1 | 2 | 0 | 1 | 30 | **15** |
| $W$ | -8 | -10 | 0 | 0 | 0 | |

$v$ enters (most negative $-10$), $s_2$ leaves (ratio 15). After pivoting:

| Basis | $u$ | $v$ | $s_1$ | $s_2$ | RHS | ratio |
|---|---|---|---|---|---|---|
| $s_1$ | 3/2 | 0 | 1 | -1/2 | 5 | **10/3** |
| $v$ | 1/2 | 1 | 0 | 1/2 | 15 | 30 |
| $W$ | -3 | 0 | 0 | 5 | 150 | |

$u$ enters, $s_1$ leaves (pivot $\frac{3}{2}$):

| Basis | $u$ | $v$ | $s_1$ | $s_2$ | RHS |
|---|---|---|---|---|---|
| $u$ | 1 | 0 | 2/3 | -1/3 | 10/3 |
| $v$ | 0 | 1 | -1/3 | 2/3 | 40/3 |
| $W$ | 0 | 0 | 2 | 4 | 160 |

Optimal dual: $u = \frac{10}{3}$, $v = \frac{40}{3}$, $W = 160$. **The minimum diet cost is Rs 160**, equal to $W$ by the duality theorem.
**Reading the primal answer:** the entries of the objective row under the slack variables $s_1, s_2$ are the primal variables: $x = 2$, $y = 4$. This matches the corner found graphically.
:::

### Complementary slackness and what the dual variables mean

At the optimum, a constraint and its partner variable are never both loose: **if a constraint has slack, its dual variable is 0; if a dual variable is positive, its constraint is tight.** Check with the diet: $u = \frac{10}{3} > 0$ and $v = \frac{40}{3} > 0$, and indeed both nutrient constraints are exactly met ($2 \cdot 2 + 4 = 8$ and $2 + 2 \cdot 4 = 10$). In the product-mix problem, soldering has 2 spare hours and its shadow price is 0.

::: key Interpreting dual variables
A dual variable is the **marginal value of one more unit of its resource**. In the diet, $u = \frac{10}{3}$ says that one extra unit of protein requirement raises the cheapest cost by about Rs 3.33, and $v = \frac{40}{3}$ says one extra unit of iron raises it by about Rs 13.33. A manager can use these numbers to decide what is worth buying more of: pay up to the shadow price for another unit of a scarce resource, never more.
:::

::: note Four possible outcomes for a primal-dual pair
(1) both have optimal solutions with equal values; (2) the primal is unbounded and the dual is infeasible; (3) the dual is unbounded and the primal is infeasible; (4) both are infeasible. It is impossible for one to have an optimum and the other not.
:::

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

### Gauss-Jordan elimination and the inverse by row operations

Gauss-Jordan continues elimination until the left block becomes the identity. Applied to the augmented matrix $[A \mid I]$, it turns $I$ into $A^{-1}$. This is how a computer (or Excel's `MINVERSE`) gets an inverse, and it avoids the long adjoint calculation for $3 \times 3$ and larger matrices.

::: example Worked example: inverse of a 3 by 3 matrix
Find $A^{-1}$ for $A = \begin{bmatrix} 2 & 1 & 1 \\ 1 & 3 & 2 \\ 1 & 0 & 0 \end{bmatrix}$ and solve $2 x + y + z = 7$, $x + 3 y + 2 z = 13$, $x = 1$.
Start with $[A \mid I]$ and use row operations (a row swap is always allowed).

1. $R_{1} \leftrightarrow R_{3}$: rows become $(1, 0, 0 \mid 0, 0, 1)$, $(1, 3, 2 \mid 0, 1, 0)$, $(2, 1, 1 \mid 1, 0, 0)$.
2. $R_{2} \leftarrow R_{2} - R_{1}$ gives $(0, 3, 2 \mid 0, 1, -1)$; $R_{3} \leftarrow R_{3} - 2 R_{1}$ gives $(0, 1, 1 \mid 1, 0, -2)$.
3. $R_{2} \leftrightarrow R_{3}$, so the pivot of column 2 is 1: rows $(0, 1, 1 \mid 1, 0, -2)$ and $(0, 3, 2 \mid 0, 1, -1)$.
4. $R_{3} \leftarrow R_{3} - 3 R_{2}$: $(0, 0, -1 \mid -3, 1, 5)$; then $R_{3} \leftarrow -R_{3}$: $(0, 0, 1 \mid 3, -1, -5)$.
5. $R_{2} \leftarrow R_{2} - R_{3}$: $(0, 1, 0 \mid -2, 1, 3)$.

$$A^{-1} = \begin{bmatrix} 0 & 0 & 1 \\ -2 & 1 & 3 \\ 3 & -1 & -5 \end{bmatrix}, \qquad \det A = -1.$$
Then $X = A^{-1} B$ with $B = (7, 13, 1)^{T}$: $x = 1$, $y = -14 + 13 + 3 = 2$, $z = 21 - 13 - 5 = 3$. **Solution $(1, 2, 3)$.** Check: $2 + 2 + 3 = 7$ and $1 + 6 + 6 = 13$.
:::

If any column has no non-zero pivot available, $\det A = 0$ and **no inverse exists**; the system then has either no solution or infinitely many.

### Why pivoting matters

Computers keep only a few significant digits, so dividing by a *tiny* pivot magnifies rounding errors. Take $0.0001 x + y = 1$, $x + y = 2$, whose true solution is $x = 1.0001$, $y = 0.9999$, and imagine a machine that keeps **3 significant figures**.

::: example Worked example: elimination with and without pivoting
**Without pivoting.** The multiplier is $1 / 0.0001 = 10^{4}$. Row 2 becomes $(1 - 10^{4} \cdot 0.0001) x + (1 - 10^{4}) y = 2 - 10^{4}$, i.e. $-9999 y = -9998$. Rounded to 3 figures, this is $-10000 y = -10000$, so $y = 1.00$. Back substitution gives $x = (1 - y) / 0.0001 = \mathbf{0}$. The answer $x = 0$ is badly wrong.
**With partial pivoting.** Swap the rows so that the larger entry 1 is the pivot: $x + y = 2$ and $0.0001 x + y = 1$. The multiplier is $0.0001$: $(1 - 0.0001) y = 1 - 0.0002$, which rounds to $1.00 y = 1.00$, $y = 1.00$ and $x = 2 - 1 = \mathbf{1.00}$. Correct to the 3 figures kept.
:::

::: tip Rule for hand and machine work
At each step, choose as pivot the entry of **largest absolute value** in the column (among the remaining rows) and swap it into place. It costs only a comparison and a row swap, and it keeps every multiplier at most 1 in size.
:::

### Ill-conditioned systems

Some systems are **ill-conditioned**: tiny changes in the data change the answer enormously, whatever the method. Consider $x + y = 2$ and $x + 1.0001 y = 2.0001$. Its solution is $(1, 1)$. Change the right-hand side by only $0.0001$ to $2.0002$ and the solution jumps to $(0, 2)$. The two lines are almost parallel, so their intersection slides a long way when one line moves slightly. The **condition number** $\kappa (A) = \|A\| \, \|A^{-1}\|$ measures this magnification; here $\kappa \approx 40{,}000$. A well-conditioned matrix has $\kappa$ near 1. With $\kappa \approx 10^{k}$ you lose about $k$ decimal digits of accuracy, so one should check the **residual** $B - A X$ and, if possible, rescale or reformulate the problem.

### LU factorisation: elimination you can reuse

Gauss elimination can be recorded as a product $A = L U$, where $U$ is the upper-triangular matrix produced by forward elimination and $L$ is a lower-triangular matrix holding the **multipliers** (1 on the diagonal). Once $A = L U$ is known, any new right-hand side $B$ is solved cheaply in two triangular steps: $L Y = B$ (forward substitution) then $U X = Y$ (back substitution). Only the factorisation costs $\frac{2}{3} n^{3}$; each new $B$ costs about $n^{2}$.

::: example Worked example: LU for the earlier system
For $A = \begin{bmatrix} 2 & 1 & -1 \\ -3 & -1 & 2 \\ -2 & 1 & 2 \end{bmatrix}$ the multipliers used in the Gauss elimination example were $l_{21} = -\frac{3}{2}$, $l_{31} = -1$, $l_{32} = 4$, giving
$$L = \begin{bmatrix} 1 & 0 & 0 \\ -\frac{3}{2} & 1 & 0 \\ -1 & 4 & 1 \end{bmatrix}, \qquad U = \begin{bmatrix} 2 & 1 & -1 \\ 0 & \frac{1}{2} & \frac{1}{2} \\ 0 & 0 & -1 \end{bmatrix}.$$
Check, row 3 of $L U$: $-1 (2, 1, -1) + 4 (0, \frac{1}{2}, \frac{1}{2}) + (0, 0, -1) = (-2, 1, 2)$, which is row 3 of $A$.
Now solve for a *new* right-hand side $B = (1, 0, 3)^{T}$ without repeating elimination. Forward: $y_{1} = 1$; $-\frac{3}{2} y_{1} + y_{2} = 0 \Rightarrow y_{2} = 1.5$; $-y_{1} + 4 y_{2} + y_{3} = 3 \Rightarrow y_{3} = -2$. Back: $-z = -2 \Rightarrow z = 2$; $\frac{1}{2} y + \frac{1}{2} (2) = 1.5 \Rightarrow y = 1$; $2 x + 1 - 2 = 1 \Rightarrow x = 1$. **Solution $(1, 1, 2)$.**
:::

### Jacobi against Gauss-Seidel, and the need for diagonal dominance

The **Jacobi** method is the simpler cousin of Gauss-Seidel: every new value is computed from the *old* iteration only. Gauss-Seidel uses new values as soon as they exist, so it normally converges about twice as fast. Both need a (nearly) diagonally dominant matrix and **the equations written in the right order**.

::: example Worked example: Jacobi, Gauss-Seidel and a bad ordering
System (solution $(1, 2, 3)$): $10 x + y + z = 15$, $2 x + 10 y + z = 25$, $x + 2 y + 10 z = 35$. Start at $(0, 0, 0)$.

| Iteration | Jacobi $(x, y, z)$ | Gauss-Seidel $(x, y, z)$ |
|---|---|---|
| 1 | 1.5000, 2.5000, 3.5000 | 1.5000, 2.2000, 2.9100 |
| 2 | 0.9000, 1.8500, 2.8500 | 0.9890, 2.0112, 2.9989 |
| 3 | 1.0300, 2.0350, 3.0400 | 0.9990, 2.0003, 3.0000 |
| 4 | 0.9925, 1.9900, 2.9900 | 1.0000, 2.0000, 3.0000 |
| 5 | 1.0020, 2.0025, 3.0027 | 1.0000, 2.0000, 3.0000 |

Gauss-Seidel is correct to 4 decimals after four sweeps; Jacobi is still off in the third decimal after five. Now write the *same* equations in a different order: $x + 2 y + 10 z = 35$, $10 x + y + z = 15$, $2 x + 10 y + z = 25$. The diagonal entries are now $1, 1, 1$, so the matrix is not diagonally dominant. Solving each equation for its diagonal variable gives, after the first sweep from $(0, 0, 0)$, $(35,\ -335,\ 3305)$, then $(-32345,\ 320160,\ -3136885)$: **the iteration diverges**. Re-ordering the rows so that the largest coefficient of each row sits on the diagonal is enough to fix it.
:::

```svgfig label="6.4" caption="How fast the iterations converge for the 3 by 3 system above. The vertical axis is log10 of the largest error in x, y, z; a drop of 1 means one more correct decimal digit. Gauss-Seidel gains about 1.5 digits per sweep, Jacobi about 0.6, so Gauss-Seidel needs less than half as many sweeps for the same accuracy."
f = Fig(560, 300)
L, T, W, H = 70, 34, 440, 210
def X(k):
    return L + (k - 1) / 7 * W
def Y(v):
    return T + (-v) / 10.5 * H
for v in range(0, -11, -2):
    f.line(L, Y(v), L + W, Y(v), color="#e2e8f0", sw=0.8)
    f.text(L - 8, Y(v) + 4, str(v), size=10, color=SLATE, anchor="end")
for k in range(1, 9):
    f.line(X(k), T, X(k), T + H, color="#e2e8f0", sw=0.8)
    f.text(X(k), T + H + 16, str(k), size=10, color=SLATE)
f.line(L, T, L, T + H, color=SLATE, sw=1.4)
f.line(L, Y(0), L + W, Y(0), color=SLATE, sw=1.4)
f.text(L + W / 2, T + H + 36, "iteration number", size=11, color=SLATE)
f.text(L, T - 8, "log10 error", size=11, color=SLATE, anchor="start")
gs = [-0.3, -1.95, -3.0, -4.45, -6.21, -7.97, -9.03, -10.44]
ja = [-0.3, -0.82, -1.4, -2.0, -2.56, -3.15, -3.73, -4.31]
for series, col in ((gs, TEAL), (ja, AMBER)):
    for i in range(7):
        f.line(X(i + 1), Y(series[i]), X(i + 2), Y(series[i + 1]), color=col, sw=2.4)
    for i in range(8):
        f.circle(X(i + 1), Y(series[i]), 4, fill=col, stroke=col)
f.text(X(6.1), Y(-8.2) - 8, "Gauss-Seidel", size=11, color=TEAL, bold=True, anchor="start")
f.text(X(5.2), Y(-3.0) - 8, "Jacobi", size=11, color=AMBER, bold=True, anchor="start")
```

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

### Finding a starting bracket

Both methods need a good start. Tabulate $f$ at integers and look for a **sign change**. For $f (x) = x^{3} - x - 2$: $f (0) = -2$, $f (1) = -2$, $f (2) = 4$. The sign changes between 1 and 2, so a root lies in $[1, 2]$; since $f' (x) = 3 x^{2} - 1 > 0$ for $x \ge 1$ the function is increasing there and the root is unique. Plotting $f$ (or using a spreadsheet column of values) is the quickest way to bracket roots of other equations.

### Regula falsi (false position)

Bisection ignores the *sizes* of $f (a)$ and $f (b)$. **Regula falsi** joins $(a, f (a))$ and $(b, f (b))$ by a straight line and takes the point where it crosses the $x$-axis:
$$c = \frac{a f (b) - b f (a)}{f (b) - f (a)}.$$
Then it keeps the sub-interval where the sign still changes, exactly like bisection.

::: example Worked example: regula falsi for $x^{3} - x - 2 = 0$ on $[1, 2]$
$f (1) = -2$, $f (2) = 4$. $c_{1} = \frac{1 \cdot 4 - 2 \cdot (-2)}{4 - (-2)} = \frac{8}{6} = 1.33333$, $f (c_{1}) = -0.96296 < 0$, so $a = 1.33333$.

| Step | $c$ | $f (c)$ | End kept |
|---|---|---|---|
| 1 | 1.33333 | -0.96296 | $a \leftarrow c$ |
| 2 | 1.46269 | -0.33334 | $a \leftarrow c$ |
| 3 | 1.50402 | -0.10182 | $a \leftarrow c$ |
| 4 | 1.51633 | -0.02989 | $a \leftarrow c$ |
| 5 | 1.51992 | -0.00868 | $a \leftarrow c$ |

The estimates approach $1.52138$ steadily and the error shrinks by a roughly constant factor (about 3.4) each step: **linear convergence**, but faster than bisection. Notice that the end $b = 2$ never moves; for a curve bent like this the method stays "stuck" on one side, which is its known weakness.
:::

### Secant method

The secant method takes the same chord idea but drops the bracketing requirement and always uses the **two most recent** points: $x_{n+1} = x_{n} - \dfrac{f (x_{n}) (x_{n} - x_{n-1})}{f (x_{n}) - f (x_{n-1})}$. It needs no derivative (unlike Newton-Raphson) and converges faster than regula falsi, with order about $1.618$, but it can leave the interval and is not guaranteed to converge.

::: example Worked example: secant for the same equation, $x_{0} = 1$, $x_{1} = 2$
$x_{2} = 1.33333$ ($f = -0.96296$); $x_{3} = 1.46269$ ($f = -0.33334$); $x_{4} = 1.53117$ ($f = 0.05863$); $x_{5} = 1.52093$ ($f = -0.00269$); $x_{6} = 1.52138$ ($f = -0.00002$). Five steps give $1.52138$ to five decimals, with no derivative needed.
:::

### Speed of convergence compared

If $e_{n}$ is the error after $n$ steps, a method has **order** $p$ when $e_{n+1} \approx C\, e_{n}^{p}$. Bisection and regula falsi are order 1 (linear); the secant method is order $\approx 1.62$; Newton-Raphson is order 2 (quadratic). In decimal digits: bisection gains 0.3 digit per step, Newton roughly doubles the digits.

| Method | Order | Needs $f'$? | Needs a bracket? | Always converges? |
|---|---|---|---|---|
| Bisection | 1 | No | Yes | Yes |
| Regula falsi | 1 | No | Yes | Yes |
| Secant | 1.62 | No | No | No |
| Newton-Raphson | 2 | Yes | No | No |

```svgfig label="6.5" caption="Error of four methods on x^3 - x - 2 = 0 (root 1.5213797). The vertical axis is log10 of the absolute error. Bisection zig-zags down at about 0.3 per step; regula falsi falls steadily at about 0.55 per step; the secant method steepens as it closes in; Newton-Raphson from x0 = 1.5 reaches machine precision (1e-16) in four steps."
f = Fig(560, 310)
L, T, W, H = 70, 34, 350, 222
def X(k):
    return L + (k - 1) / 7 * W
def Y(v):
    return T + (-v) / 16 * H
for v in range(0, -17, -4):
    f.line(L, Y(v), L + W, Y(v), color="#e2e8f0", sw=0.8)
    f.text(L - 8, Y(v) + 4, str(v), size=10, color=SLATE, anchor="end")
for k in range(1, 9):
    f.line(X(k), T, X(k), T + H, color="#e2e8f0", sw=0.8)
    f.text(X(k), T + H + 16, str(k), size=10, color=SLATE)
f.line(L, T, L, T + H, color=SLATE, sw=1.4)
f.line(L, Y(0), L + W, Y(0), color=SLATE, sw=1.4)
f.text(L + W / 2, T + H + 36, "step number", size=11, color=SLATE)
f.text(L, T - 8, "log10 error", size=11, color=SLATE, anchor="start")
data = [
    ([-1.67, -0.64, -0.98, -1.39, -2.01, -2.24, -2.69, -2.73], AMBER, "Bisection", 8, -2.2),
    ([-0.73, -1.23, -1.76, -2.3, -2.84, -3.37, -3.91, -4.45], SLATE, "Regula falsi", 8, -5.4),
    ([-0.73, -1.23, -2.01, -3.34, -5.47, -8.93], TEAL, "Secant", 6, -9.8),
    ([-3.44, -7.0, -14.12, -16.0], RED, "Newton-Raphson", 4, -15.0),
]
for ys, col, name, n, ty in data:
    for i in range(n - 1):
        f.line(X(i + 1), Y(ys[i]), X(i + 2), Y(ys[i + 1]), color=col, sw=2.3)
    for i in range(n):
        f.circle(X(i + 1), Y(ys[i]), 3.8, fill=col, stroke=col)
    f.text(X(n) + 8, Y(ys[n - 1]) + 4, name, size=10.5, color=col, bold=True, anchor="start")
```

### When Newton-Raphson fails

The tangent idea can go wrong. Typical failures: (1) **$f' (x_{n}) = 0$** (flat tangent): division by zero or a gigantic jump. (2) **A cycle**: for $f (x) = x^{3} - 2 x + 2$ with $x_{0} = 0$, the tangent at 0 hits the axis at 1, and the tangent at 1 hits the axis at 0, so the iterates are $1, 0, 1, 0, \dots$ forever although a real root exists near $-1.77$. (3) **Divergence**: for $f (x) = \sqrt[3]{x}$ the root is 0, but $x_{n+1} = -2 x_{n}$, so every step doubles the distance. (4) **A different root** than the one wanted when the start is far away.

```svgfig label="6.6" caption="A Newton-Raphson cycle. For f(x) = x^3 - 2x + 2 starting at x0 = 0, the tangent y = 2 - 2x meets the axis at x = 1; the tangent at x = 1 is y = x and meets the axis at x = 0. The iteration bounces between 0 and 1 and never approaches the real root near -1.77, so a better starting value (for example x0 = -2) is needed."
f = Fig(560, 300)
ax = Axes(f, 60, 20, 440, 250, (-2.2, 2.2), (-3, 4))
ax.grid(1, 1)
ax.axes("x", "y")
ax.curve(lambda x: x**3 - 2 * x + 2, color=NAVY, sw=2.6)
ax.curve(lambda x: 2 - 2 * x, -0.4, 1.4, color=AMBER, sw=1.8, dash=True)
ax.curve(lambda x: x, -0.4, 1.6, color=TEAL, sw=1.8, dash=True)
ax.vline(0, 0, 2, color=SLATE, dash=True)
ax.vline(1, 0, 1, color=SLATE, dash=True)
ax.pt(0, 2, "", color=NAVY)
ax.pt(1, 1, "", color=NAVY)
ax.pt(0, 0, "x0 = 0", color=RED, dx=-8, dy=32, anchor="end")
ax.pt(1, 0, "x1 = 1", color=RED, dx=10, dy=-8)
ax.pt(-1.77, 0, "root", color=TEAL, dx=0, dy=-12, anchor="middle", hollow=True)
ax.tag(-1.7, 3.3, "f(x) = x^3 - 2x + 2", size=11, color=NAVY, bold=True, anchor="start")
ax.tag(1.3, -1.0, "tangent at 0", size=10, color=AMBER, bold=True, anchor="start")
ax.tag(1.62, 1.35, "tangent at 1", size=10, color=TEAL, bold=True, anchor="start")
```

::: tip Safeguards in practice
Plot or tabulate first; start Newton-Raphson inside a bracket; stop and switch to bisection if a step leaves the bracket or if $|f' (x_{n})|$ is tiny; limit the number of iterations (for example 50); and **test the answer** by checking $|f (x_{n})|$ as well as $|x_{n+1} - x_{n}|$.
:::

### Newton-Raphson as a square-root algorithm

For $f (x) = x^{2} - a$ the formula becomes $x_{n+1} = \dfrac{1}{2} \left( x_{n} + \dfrac{a}{x_{n}} \right)$, the ancient Babylonian method, which calculators and `sqrt` routines still use in some form: each new guess is the **average** of $x_{n}$ and $a / x_{n}$.

::: example Worked example: $\sqrt{10}$
Start with $x_{0} = 3$. $x_{1} = \frac{1}{2} (3 + \frac{10}{3}) = 3.1666667$; $x_{2} = \frac{1}{2} (3.1666667 + \frac{10}{3.1666667}) = 3.1622807$; $x_{3} = 3.1622777$; $x_{4} = 3.1622777$. The digits that are correct go $1 \to 3 \to 6 \to 8+$, roughly doubling each step, as quadratic convergence promises.
:::

### Stopping criteria

An iteration must know when to stop. Use one or more of: **absolute change** $|x_{n+1} - x_{n}| < \varepsilon$; **relative change** $\frac{|x_{n+1} - x_{n}|}{|x_{n+1}|} < \varepsilon$ (better for very large or very small roots); **residual** $|f (x_{n+1})| < \varepsilon$; and a **maximum number of iterations** as a safety net. A small residual does not guarantee a small error when $f$ is very flat near the root, and a small change does not guarantee a small residual when $f$ is very steep.

### An application: the interest rate hidden in an EMI

A bank offers a loan of Rs 100,000 repaid in 12 monthly instalments (EMI) of Rs 9,000. What monthly interest rate $r$ is it charging? The present value of the instalments must equal the loan: $9000 \cdot \dfrac{1 - (1 + r)^{-12}}{r} = 100000$. There is no formula that solves this for $r$, which is exactly the situation numerical methods are for. Define $h (r) = 9000 \cdot \dfrac{1 - (1 + r)^{-12}}{r} - 100000$; $h$ is positive when $r$ is too small and negative when $r$ is too large.

::: example Worked example: bisection on $[0.001, 0.05]$
Try $r = 0.001$ (so $h > 0$) and $r = 0.05$ (so $h < 0$); the root is bracketed.

| Step | $r$ (midpoint) | $h (r)$ | New bracket |
|---|---|---|---|
| 1 | 0.02550 | -7959.0 | $[0.00100, 0.02550]$ |
| 2 | 0.01325 | -753.8 | $[0.00100, 0.01325]$ |
| 3 | 0.00713 | 3160.2 | $[0.00713, 0.01325]$ |
| 4 | 0.01019 | 1175.8 | $[0.01019, 0.01325]$ |
| 5 | 0.01172 | 204.3 | $[0.01172, 0.01325]$ |
| 6 | 0.01248 | -276.4 | $[0.01172, 0.01248]$ |
| 7 | 0.01210 | -36.5 | $[0.01172, 0.01210]$ |

More steps (or the secant method) give $r = 0.012043$, that is **1.20 percent per month**, a nominal annual rate of $12 \times 1.2043 = 14.45$ percent. In Excel the same answer comes from `=RATE(12, -9000, 100000)`, which itself uses an iteration of this kind. Notice how much more informative this is than the "flat rate" quoted in advertisements: total interest is $12 \times 9000 - 100000 = 8000$, a 8 percent flat rate on the original loan, yet the true yearly rate is much higher because the borrower repays the principal gradually.
:::


## 6.6 Computer lab: Excel, MATLAB and Python

The TU outline marks this unit "(Excel/Matlab)": the methods above are meant to be *run*, not only worked by hand. This section shows the same problems on a spreadsheet, in MATLAB and in Python (whose NumPy and SciPy libraries mirror MATLAB's). All Python programs below were executed and the output shown is the real output.

### Excel: bisection, Newton-Raphson, Gauss-Seidel

**Bisection sheet** for $f (x) = x^{3} - x - 2$ on $[1, 2]$. Put the headings in row 1 and the first bracket in row 2, then fill row 3 downward.

| Cell | Heading | Formula in row 2 | Formula in row 3 (fill down) |
|---|---|---|---|
| A | $n$ | `1` | `=A2+1` |
| B | $a$ | `1` | `=IF(F2<0, B2, D2)` |
| C | $b$ | `2` | `=IF(F2<0, D2, C2)` |
| D | $m$ | `=(B2+C2)/2` | `=(B3+C3)/2` |
| E | $f (m)$ | `=D2^3-D2-2` | `=D3^3-D3-2` |
| F | sign test | `=E2*(B2^3-B2-2)` | `=E3*(B3^3-B3-2)` |
| G | width | `=C2-B2` | `=C3-B3` |

Column F is negative when the root lies in the left half, so the `IF` keeps the correct half. Fill down about 12 rows, stop when column G is below your tolerance, and the last $m$ is the root. **Newton-Raphson sheet:** A2 holds the start `1.5`; in A3 type `=A2-(A2^3-A2-2)/(3*A2^2-1)` and fill down; the column settles at 1.5213797 after four rows. **Gauss-Seidel sheet:** enter the start $(0,0,0)$ in row 2; in row 3 type `=(15-C2-D2)/10` (for $x$), `=(25-2*B3-D2)/10` (for $y$, using the *new* $x$ in B3) and `=(35-B3-2*C3)/10` (for $z$) and fill down. Using the new cell B3 in the second formula is the entire difference from Jacobi.

**Linear systems.** With $A$ in A1:C3 and $B$ in E1:E3, select a $3 \times 1$ block and enter the array formula `=MMULT(MINVERSE(A1:C3), E1:E3)` (Ctrl+Shift+Enter in older versions) to get $X$; `=MDETERM(A1:C3)` gives the determinant and `=MINVERSE(A1:C3)` the inverse. **LPP with Solver:** enter the decision cells, the objective formula (for example `=3*B1+2*B2`) and each constraint's left-hand side as formulas; then *Data > Solver*: set the objective to *Max*, the changing cells to B1:B2, add constraints such as `$D$1 <= $E$1`, tick *Make unconstrained variables non-negative*, choose the *Simplex LP* method and press *Solve*. The *Sensitivity Report* it can produce contains exactly the shadow prices and ranges of 6.2.

### Python: the methods as short programs

```python
def bisection(f, a, b, tol=1e-6):
    n = 0
    while (b - a) / 2 > tol:
        m = (a + b) / 2
        if f(a) * f(m) < 0:
            b = m
        else:
            a = m
        n += 1
    return (a + b) / 2, n

def newton(f, df, x, tol=1e-10):
    n = 0
    while abs(f(x)) > tol:
        x = x - f(x) / df(x)
        n += 1
    return x, n

f = lambda x: x**3 - x - 2
df = lambda x: 3 * x**2 - 1
root, steps = bisection(f, 1, 2)
print("bisection  :", round(root, 6), "in", steps, "steps")
root, steps = newton(f, df, 1.5)
print("newton     :", round(root, 6), "in", steps, "steps")
r, k = bisection(lambda r: 9000 * (1 - (1 + r) ** -12) / r - 100000, 0.001, 0.05)
print("EMI rate   :", round(r, 6), "per month =", round(12 * r * 100, 2), "percent a year")
```
```output
bisection  : 1.52138 in 19 steps
newton     : 1.52138 in 3 steps
EMI rate   : 0.012044 per month = 14.45 percent a year
```

Bisection needs about twenty steps for six decimals (the interval must shrink from 1 to $10^{-6}$, and $\log_{2} 10^{6} \approx 20$) whereas Newton-Raphson needs three.

```python
def gauss_seidel(A, b, tol=1e-6, max_iter=100):
    n = len(b)
    x = [0.0] * n
    for k in range(1, max_iter + 1):
        biggest = 0.0
        for i in range(n):
            s = sum(A[i][j] * x[j] for j in range(n) if j != i)
            new = (b[i] - s) / A[i][i]
            biggest = max(biggest, abs(new - x[i]))
            x[i] = new
        if biggest < tol:
            return x, k
    return x, max_iter

A = [[10, 1, 1], [2, 10, 1], [1, 2, 10]]
b = [15, 25, 35]
x, k = gauss_seidel(A, b)
print("Gauss-Seidel:", [round(v, 5) for v in x], "after", k, "sweeps")
bad = [[1, 2, 10], [10, 1, 1], [2, 10, 1]]
x, k = gauss_seidel(bad, [35, 15, 25], max_iter=6)
print("bad order    :", [f"{v:.3g}" for v in x], "after", k, "sweeps (diverging)")
```
```output
Gauss-Seidel: [1.0, 2.0, 3.0] after 6 sweeps
bad order    : ['-2.63e+16', '2.61e+17', '-2.55e+18'] after 6 sweeps (diverging)
```

```python
import numpy as np

A = np.array([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], dtype=float)
b = np.array([8, -11, -3], dtype=float)
print("solve      :", np.linalg.solve(A, b))
print("det        :", round(np.linalg.det(A), 6))
print("A inverse  :")
print(np.round(np.linalg.inv(A), 4))
print("max residual:", float(np.max(np.abs(b - A @ np.linalg.solve(A, b)))) < 1e-12, "(below 1e-12)")
H = np.array([[1, 1], [1, 1.0001]])
print("cond number:", round(np.linalg.cond(H)))
print("same A, b+0.0001 ->", np.round(np.linalg.solve(H, [2, 2.0001]), 4), "and", np.round(np.linalg.solve(H, [2, 2.0002]), 4))
```
```output
solve      : [ 2.  3. -1.]
det        : -1.0
A inverse  :
[[ 4.  3. -1.]
 [-2. -2.  1.]
 [ 5.  4. -1.]]
max residual: True (below 1e-12)
cond number: 40002
same A, b+0.0001 -> [1. 1.] and [0. 2.]
```

```python
from scipy.optimize import linprog

# linprog always minimises, so maximise Z by minimising -Z.
r = linprog([-3, -2], A_ub=[[1, 1], [1, 3]], b_ub=[4, 6])
print("product mix  : x, y =", r.x, " Z =", -r.fun)
r = linprog([-5, -4, -3], A_ub=[[2, 3, 1], [4, 1, 2], [3, 4, 2]], b_ub=[5, 11, 8])
print("three-product: x, y, z =", r.x.round(6), " Z =", round(-r.fun, 6))
r = linprog([20, 30], A_ub=[[-2, -1], [-1, -2]], b_ub=[-8, -10])
print("diet (min)   : x, y =", r.x.round(6), " cost =", round(r.fun, 6))
r = linprog([-1, -1], A_ub=[[1, 1], [-1, -1]], b_ub=[2, -4])
print("infeasible   : status", r.status, "-", r.message.split(".")[0])
r = linprog([-1, -1], A_ub=[[1, -1], [-1, 1]], b_ub=[2, 3])
print("unbounded    : status", r.status, "-", r.message.split(".")[0])
```
```output
product mix  : x, y = [4. 0.]  Z = 12.0
three-product: x, y, z = [2. 0. 1.]  Z = 13.0
diet (min)   : x, y = [2. 4.]  cost = 160.0
infeasible   : status 2 - The problem is infeasible
unbounded    : status 3 - The problem is unbounded
```

### MATLAB: the same problems

MATLAB (and the free GNU Octave) uses the same ideas with shorter syntax. These commands are standard MATLAB; the numbers they print are the ones above.

```matlab
% Linear system A x = b
A = [2 1 -1; -3 -1 2; -2 1 2];  b = [8; -11; -3];
x = A \ b            % Gauss elimination with partial pivoting: [2; 3; -1]
inv(A)               % inverse
det(A)               % determinant

% Roots of f(x) = x^3 - x - 2
f = @(x) x.^3 - x - 2;
root = fzero(f, [1 2])      % bracketing method, 1.5214
p = [1 0 -1 -2];  roots(p)  % polynomial roots (one real, two complex)

% Linear programming: maximise 3x + 2y,  x + y <= 4,  x + 3y <= 6,  x,y >= 0
c = [-3; -2];  Aineq = [1 1; 1 3];  bineq = [4; 6];
[xopt, fval] = linprog(c, Aineq, bineq, [], [], [0; 0])   % x = [4; 0], fval = -12
```

::: note Which tool when
A spreadsheet is best for **seeing every iteration** and for business users; MATLAB or Python for **larger problems** and for repeating the work with new data; and hand calculation for exams. In every case the checks are the same: substitute the answer back into the equations, confirm that constraints hold, and compare two different methods.
:::

## Formula and fact sheet

- LPP: maximise $Z = c^{T} x$, $A x \le b$, $x \ge 0$. Optimum at a corner point.
- Simplex: enter most negative objective entry; leave minimum ratio; pivot; stop when no negative entry remains.
- Dual: $\min b^{T} w$, $A^{T} w \ge c$; optimal values are equal.
- Gauss elimination: forward elimination then back substitution, about $\frac{2}{3} n^{3}$ operations.
- Gauss-Seidel: use new values at once; converges for strictly diagonally dominant $A$.
- Bisection: $n \ge \log_{2} \frac{b - a}{\varepsilon}$. Newton-Raphson: $x_{n+1} = x_{n} - \frac{f}{f'}$.
- Minimisation with $\ge$ constraints: solve the dual (maximise $b^{T} w$, $A^{T} w \le c$); the primal answer is the objective-row entries under the slacks.
- Special cases: no feasible region = infeasible; no positive entry in the entering column = unbounded; a zero in the objective row for a non-basic variable = multiple optima; a tied ratio = degenerate.
- Shadow price of a resource = entry under its slack in the final objective row; it is valid while the basic variables stay $\ge 0$.
- Partial pivoting: pick the largest $|a_{ik}|$ in the column; LU: $A = L U$, then $L Y = B$ and $U X = Y$; $\kappa (A) = \|A\|\,\|A^{-1}\|$.
- Regula falsi, order 1: the chord meets the axis at $c = \left( a f (b) - b f (a) \right) / \left( f (b) - f (a) \right)$. Secant: order 1.62. Newton: order 2.
- Babylonian square root: $x_{n+1} = \dfrac{1}{2} \left( x_{n} + \dfrac{a}{x_{n}} \right)$.

## Chapter summary

- A linear programming problem has a linear objective and linear constraints; the optimum lies at a corner of the feasible region and can be found graphically (two variables) or by the simplex tableau.
- The dual problem has the same optimal value, and its variables are the shadow prices of the resources.
- Linear systems are solved by inversion, Gauss elimination or Gauss-Seidel iteration; roots of non-linear equations by bisection (safe, slow) or Newton-Raphson (fast, needs a derivative).
- Real problems bring complications: infeasible, unbounded and multiple-optima LPPs, degenerate corners, minimisation through the dual, and sensitivity ranges for the shadow prices.
- Numerical methods trade reliability for speed: pivoting and conditioning decide accuracy for linear systems, and the order of convergence (1, 1.62, 2) separates bisection, secant and Newton-Raphson. Newton-Raphson can cycle or diverge, so bracket first.
- Excel (`MINVERSE`, `MMULT`, Solver, fill-down formulas), MATLAB (`\`, `fzero`, `linprog`) and Python (`numpy`, `scipy`) run all of these methods.

## Practice

1. Maximise $Z = 2 x + 3 y$ subject to $x + y \le 4$, $x + 3 y \le 6$, $x, y \ge 0$ by the graphical method.
2. Solve problem 1 by the simplex method and read the shadow prices.
3. Write the dual of problem 1 and solve it.
4. Solve by Gauss elimination: $x + y + z = 6$, $2 y + 5 z = -4$, $2 x + 5 y - z = 27$.
5. Solve $3 x + 2 y = 7$, $x + 4 y = 9$ by the matrix inversion method.
6. Perform two Gauss-Seidel iterations on $4 x + y = 9$, $x + 3 y = 7$ starting from $(0, 0)$.
7. Apply three bisection steps to $x^{2} - 5 = 0$ on $[2, 3]$.
8. Apply two Newton-Raphson steps to $x^{2} - 5 = 0$ from $x_{0} = 2$.
9. A canteen makes samosas (profit Rs 8) and momos (profit Rs 10). A samosa needs 2 min of frying and 3 min of preparation; a momo needs 3 min of frying and 2 min of preparation. Frying time is 120 min and preparation time is 120 min per day. Formulate the LPP and solve it graphically.
10. Minimise $Z = 3 x + 4 y$ subject to $x + 2 y \ge 8$, $3 x + 2 y \ge 12$, $x, y \ge 0$.
11. Use the simplex method: maximise $Z = 3 x + 2 y + 4 z$ subject to $x + y + 2 z \le 4$, $2 x + 3 z \le 5$, $2 x + y + 3 z \le 7$.
12. Write the dual of problem 11 and state its optimal solution using the final tableau.
13. Identify the special case (infeasible, unbounded or multiple optima) and justify: (a) maximise $Z = 3 x + 3 y$ subject to $x + y \le 6$, $x \le 4$, $y \le 4$; (b) maximise $Z = 2 x + y$ subject to $x - 2 y \le 4$, $x, y \ge 0$.
14. Solve by Gauss elimination with partial pivoting: $2 y + z = 7$, $x + y + z = 6$, $2 x + y + 3 z = 13$. Why must rows be swapped at the start?
15. Find the inverse of $\begin{bmatrix} 1 & 2 & 3 \\ 0 & 1 & 4 \\ 5 & 6 & 0 \end{bmatrix}$ by Gauss-Jordan elimination and use it to solve $A X = (1, 2, 3)^{T}$.
16. Check that $5 x - y + z = 10$, $2 x + 8 y - z = 11$, $-x + y + 4 z = 3$ is strictly diagonally dominant and perform three Gauss-Seidel iterations from $(0, 0, 0)$. Compare with the exact solution.
17. For $f (x) = \cos x - x$ (x in radians) perform three bisection steps on $[0, 1]$ and two regula falsi steps on the same interval.
18. Apply three Newton-Raphson steps to $\cos x - x = 0$ from $x_{0} = 0.5$.
19. Use Newton-Raphson to find $\sqrt[3]{20}$ by solving $x^{3} - 20 = 0$ from $x_{0} = 3$ (three steps).
20. How many bisection steps are certain to locate a root in $[2, 3]$ with an error below $0.00005$?
21. Write the Excel formulas for a Newton-Raphson column for $f (x) = x^{2} - 5$, starting from 2 in cell A2, and describe the settings of Solver for problem 9.
22. State two situations in which Newton-Raphson fails and one safeguard for each. Also state two differences between the Jacobi and Gauss-Seidel methods.
23. The final simplex tableau of a maximisation problem has objective row $(0, 0, 2, 4 \mid 20)$ under $x, y, s_{1}, s_{2}$ and RHS. Interpret the numbers 2, 4 and 20.

::: note Answers and worked solutions
**1.** Corners $(0,0), (4,0), (3,1), (0,2)$ give $Z = 0, 8, 9, 6$. **Maximum $Z = 9$ at $(3, 1)$.**

**2.** $y$ enters (most negative $-3$); ratios $4/1 = 4$ and $6/3 = 2$, so $s_{2}$ leaves. After pivoting, $x$ enters (entry $-1$); ratios $2 / \frac{2}{3} = 3$ and $2 / \frac{1}{3} = 6$, so $s_{1}$ leaves. Final row: $Z = 9$, $x = 3$, $y = 1$; shadow prices $\frac{3}{2}$ and $\frac{1}{2}$.

**3.** Minimise $W = 4 u + 6 v$ s.t. $u + v \ge 2$, $u + 3 v \ge 3$. Corners: $(1.5, 0.5)$ with $W = 9$; $(0, 2)$ with $W = 12$; $(3, 0)$ with $W = 12$. **Minimum $W = 9$**, equal to the primal maximum.

**4.** From the second equation $2 y + 5 z = -4$; eliminating $x$: $R_{3} - 2 R_{1}$ gives $3 y - 3 z = 15$, so $y - z = 5$. With $R_{2}$: $2 (z + 5) + 5 z = -4 \Rightarrow z = -2$, $y = 3$, $x = 6 - 3 + 2 = 5$. **$(5, 3, -2)$.**

**5.** $\det = 12 - 2 = 10$; $A^{-1} = \frac{1}{10} \begin{bmatrix} 4 & -2 \\ -1 & 3 \end{bmatrix}$; $X = \frac{1}{10} (28 - 18, -7 + 27) = (1, 2)$. **$x = 1$, $y = 2$.**

**6.** Iteration 1: $x = 9/4 = 2.25$, $y = (7 - 2.25)/3 = 1.5833$. Iteration 2: $x = (9 - 1.5833)/4 = 1.8542$, $y = (7 - 1.8542)/3 = 1.7153$. (Exact: $x = 20/11 = 1.8182$, $y = 1.7273$.)

**7.** $f(2) = -1$, $f(3) = 4$. $m = 2.5$: $f = 1.25$, root in $[2, 2.5]$. $m = 2.25$: $f = 0.0625$, root in $[2, 2.25]$. $m = 2.125$: $f = -0.4844$, root in $[2.125, 2.25]$. Estimate **2.1875** (true root $\sqrt{5} = 2.2361$).

**8.** $x_{1} = 2 - \frac{-1}{4} = 2.25$; $x_{2} = 2.25 - \frac{0.0625}{4.5} = 2.2361$. **$\sqrt{5} \approx 2.2361$.**

**9.** Let $x$ = samosas, $y$ = momos. Maximise $Z = 8 x + 10 y$ subject to $2 x + 3 y \le 120$, $3 x + 2 y \le 120$, $x, y \ge 0$. Corners: $(0, 0)$, $(40, 0)$, $(24, 24)$ (add the two equations: $5 (x + y) = 240$, so $x = y = 24$) and $(0, 40)$, with $Z = 0, 320, 432, 400$. **Maximum Rs 432 at 24 samosas and 24 momos.** Both machines are fully used.

**10.** Corners of the region above both lines: $(0, 6)$ with $Z = 24$; $(8, 0)$ with $Z = 24$; and the intersection $x + 2 y = 8$, $3 x + 2 y = 12$, so $2 x = 4$, $x = 2$, $y = 3$, with $Z = 6 + 12 = 18$. **Minimum $Z = 18$ at $(2, 3)$.**

**11.** Start: $z$ enters (most negative, $-4$); ratios $\frac{4}{2} = 2$, $\frac{5}{3} = 1.667$, $\frac{7}{3} = 2.333$, so $s_{2}$ leaves. Then $y$ enters (entry $-2$); ratios $\frac{2/3}{1} = \frac{2}{3}$ and $\frac{2}{1} = 2$, so $s_{1}$ leaves, giving $Z = 8$ with $y = \frac{2}{3}$, $z = \frac{5}{3}$. Then $x$ enters (entry $-1$); ratios $\frac{5/3}{2/3} = 2.5$ and $\frac{4/3}{1/3} = 4$, so $z$ leaves. Final row: $(0, 0, \frac{3}{2} \mid 2, \frac{1}{2}, 0 \mid 10.5)$. **$x = \frac{5}{2}$, $y = \frac{3}{2}$, $z = 0$, $Z = 10.5$.**

**12.** Minimise $W = 4 u + 5 v + 7 w$ subject to $u + 2 v + 2 w \ge 3$, $u + w \ge 2$, $2 u + 3 v + 3 w \ge 4$, $u, v, w \ge 0$. The shadow prices under $s_{1}, s_{2}, s_{3}$ are $u = 2$, $v = \frac{1}{2}$, $w = 0$, and $W = 8 + 2.5 + 0 = 10.5$, equal to the primal maximum. The third resource ($w = 0$) has $\frac{1}{2}$ unit of slack.

**13.** (a) Corners $(0, 0)$, $(4, 0)$, $(4, 2)$, $(2, 4)$, $(0, 4)$ give $Z = 0, 12, 18, 18, 12$. The objective $3 (x + y)$ is parallel to the edge $x + y = 6$, so the whole edge from $(4, 2)$ to $(2, 4)$ is optimal: **multiple optima**, $Z = 18$. (b) Take $y = t \ge 0$ and $x = 2 t + 4$: the constraint $x - 2 y = 4$ holds, and $Z = 2 (2 t + 4) + t = 5 t + 8 \to \infty$ as $t$ grows: **unbounded**.

**14.** The coefficient of $x$ in the first equation is 0, so it cannot serve as the first pivot; swap rows 1 and 2. Then: $x + y + z = 6$, $2 y + z = 7$, $2 x + y + 3 z = 13$. $R_{3} - 2 R_{1}$: $-y + z = 1$. $R_{3} + \frac{1}{2} R_{2}$: $\frac{3}{2} z = \frac{9}{2}$, so $z = 3$; then $2 y = 4$, $y = 2$; $x = 1$. **$(1, 2, 3)$.**

**15.** $A^{-1} = \begin{bmatrix} -24 & 18 & 5 \\ 20 & -15 & -4 \\ -5 & 4 & 1 \end{bmatrix}$ ($\det A = 1$). Then $X = A^{-1} (1, 2, 3)^{T} = (-24 + 36 + 15,\ 20 - 30 - 12,\ -5 + 8 + 3) = (27, -22, 6)$. Check the first equation: $27 - 44 + 18 = 1$.

**16.** $|5| > 1 + 1$, $|8| > 2 + 1$, $|4| > 1 + 1$: strictly diagonally dominant. Iteration 1: $x = 10 / 5 = 2$; $y = (11 - 4) / 8 = 0.875$; $z = (3 + 2 - 0.875) / 4 = 1.0313$. Iteration 2: $x = (10 + 0.875 - 1.0313) / 5 = 1.9688$; $y = (11 - 3.9375 + 1.0313) / 8 = 1.0117$; $z = (3 + 1.9688 - 1.0117) / 4 = 0.9893$. Iteration 3: $(2.0045,\ 0.9975,\ 1.0017)$. The exact solution is $(2, 1, 1)$.

**17.** $f (0) = 1 > 0$, $f (1) = -0.4597 < 0$. Bisection: $m = 0.5$, $f = 0.3776$, root in $[0.5, 1]$; $m = 0.75$, $f = -0.0183$, root in $[0.5, 0.75]$; $m = 0.625$, $f = 0.1860$, root in $[0.625, 0.75]$. Regula falsi: $c_{1} = 0.68507$, $f = 0.0893$; $c_{2} = 0.73630$, $f = 0.00466$. Both approach $0.7391$.

**18.** $x_{n+1} = x_{n} + \dfrac{\cos x_{n} - x_{n}}{\sin x_{n} + 1}$. $x_{1} = 0.755222$, $x_{2} = 0.739142$, $x_{3} = 0.739085$. **Root $0.739085$** (the "Dottie number").

**19.** $x_{n+1} = x_{n} - \dfrac{x_{n}^{3} - 20}{3 x_{n}^{2}}$: $x_{1} = 2.740741$, $x_{2} = 2.714670$, $x_{3} = 2.714418$. **$\sqrt[3]{20} \approx 2.7144$.**

**20.** Need $\frac{1}{2^{n}} < 0.00005$, so $n > \log_{2} 20000 = 14.29$: **15 steps.**

**21.** Newton for $x^{2} - 5$: in A3 type `=A2-(A2^2-5)/(2*A2)` and fill down; the column reads 2, 2.25, 2.236111, 2.236068 and settles at $\sqrt{5} = 2.2360680$. Solver for problem 9: objective cell `=8*B1+10*B2` set to *Max*; changing cells B1:B2; constraints `2*B1+3*B2 <= 120` and `3*B1+2*B2 <= 120`; tick *Make unconstrained variables non-negative*; method *Simplex LP*; Solve.

**22.** Failures: (i) $f' (x_{n}) \approx 0$, safeguard: stop and bracket the root or switch to bisection; (ii) cycling or divergence from a poor start (for example $x^{3} - 2 x + 2$ from 0), safeguard: choose a start inside a sign-change bracket and cap the iterations. Jacobi uses only the previous iteration's values and can be run in parallel; Gauss-Seidel uses new values at once, so it normally converges about twice as fast and needs less memory, but each sweep is sequential.

**23.** The entries 2 and 4 under the slack variables are the **shadow prices**: one more unit of resource 1 raises $Z$ by 2 and one more unit of resource 2 raises it by 4 (within the range over which the basis stays optimal). The 20 is the **maximum value of $Z$**. Zeros under $x$ and $y$ show they are basic (in the solution), so both products are made.
:::
