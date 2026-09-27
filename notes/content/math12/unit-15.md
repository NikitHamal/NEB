---
subject: Mathematics
grade: 12
unit: 15
title: Computational Methods
hours: 12
area: Computational Methods OR Mechanics
---

Some problems have no tidy algebraic answer, and many that do have one are faster
to solve by a fixed recipe. **Computational methods** are those recipes: finite
sequences of arithmetic steps that a person with a calculator — or a machine —
can carry out without thinking. This unit gives you three of them. Two solve a
system of linear equations, one by systematic cancelling (**Gauss elimination**)
and one by repeated guessing that improves itself (**Gauss–Seidel**); the third,
the **simplex method**, finds the best value of a linear quantity subject to
linear restrictions. The unit closes with the question every computed answer must
answer: *how wrong is it?*

::: key This unit or Unit 16 — not both
The CDC syllabus offers Computational Methods **or** Mechanics as the final
$12$-hour unit. Your school teaches one of them, and the question paper gives the
two as alternatives: attempt only the one you studied. If your school chose
Mechanics, turn to Unit 16.
:::

::: key What the exam asks
Group B almost always wants one full method carried out on a $3\times3$ system —
elimination with back substitution, or three Gauss–Seidel iterations laid out in
a table. Group C is usually a simplex problem: set up the tableau, pivot twice,
read the optimum. Marks are awarded **per row operation and per pivot**, so show
every tableau. Never skip to the answer.
:::

## 15.1 System of linear equations: Gauss Elimination Method

### The augmented matrix

Write the system

$$ a_{11}x + a_{12}y + a_{13}z = b_1 $$
$$ a_{21}x + a_{22}y + a_{23}z = b_2 $$
$$ a_{31}x + a_{32}y + a_{33}z = b_3 $$

as a table of its numbers only. The coefficient matrix $A$ has entries $a_{ij}$;
attaching the right-hand column $b$ to it gives the **augmented matrix**, written
$[A \,|\, b]$. Every step of the method is a change to the rows of this table, and
the vertical bar just reminds you which column is the right-hand side.

```figure caption="Gauss elimination turns $[A\,|\,b]$ into an upper triangular table by row operations. Once the two shaded zeros are in place the last row reads off $z$ directly."
fig, ax = plt.subplots(figsize=(5.0,2.2))
ax.axis('off')
rows1 = [["$a_{11}$","$a_{12}$","$a_{13}$","$b_1$"],
         ["$a_{21}$","$a_{22}$","$a_{23}$","$b_2$"],
         ["$a_{31}$","$a_{32}$","$a_{33}$","$b_3$"]]
rows2 = [["$a_{11}$","$a_{12}$","$a_{13}$","$b_1$"],
         ["$0$","$a'_{22}$","$a'_{23}$","$b'_2$"],
         ["$0$","$0$","$a''_{33}$","$b''_3$"]]
cw = 0.66
w, h = matrix(ax, rows1, x=0.0, y=0.0, colw=cw, fontsize=10.5)
ax.plot([3*cw, 3*cw], [-0.02, h+0.02], color=MUTED, lw=0.9, ls=(0,(2,2)))
x2 = w + 1.35
w2, h2 = matrix(ax, rows2, x=x2, y=0.0, colw=cw, fontsize=10.5)
ax.plot([x2+3*cw, x2+3*cw], [-0.02, h2+0.02], color=MUTED, lw=0.9, ls=(0,(2,2)))
ax.annotate('', xy=(x2-0.30, h/2), xytext=(w+0.32, h/2),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.5, mutation_scale=11))
ax.text((w+x2)/2, h/2+0.12, 'row\noperations', ha='center', va='bottom',
        fontsize=8.6, color=ACCENT)
for cx, cy in [(x2+0.5*cw, h2-0.5*0.44), (x2+0.5*cw, h2-1.5*0.44), (x2+1.5*cw, h2-2.5*0.44)]:
    pass
ax.add_patch(plt.Circle((x2+0.5*cw, h2-1.5*0.44), 0.19, facecolor=ACCENT, alpha=0.16, edgecolor='none'))
ax.add_patch(plt.Circle((x2+0.5*cw, h2-2.5*0.44), 0.19, facecolor=ACCENT, alpha=0.16, edgecolor='none'))
ax.add_patch(plt.Circle((x2+1.5*cw, h2-2.5*0.44), 0.19, facecolor=ACCENT, alpha=0.16, edgecolor='none'))
ax.text(w/2, -0.36, 'augmented matrix  $[A\\,|\\,b]$', ha='center', fontsize=9.0, color=INK)
ax.text(x2+w2/2, -0.36, 'upper triangular', ha='center', fontsize=9.0, color=INK)
ax.set_xlim(-0.3, x2+w2+0.3); ax.set_ylim(-0.6, h+0.55)
ax.set_aspect('equal')
```

### The three elementary row operations

Only three moves are allowed, and none of them changes the solution set:

1. swap two rows ($R_i \leftrightarrow R_j$);
2. multiply a row by a non-zero constant ($R_i \rightarrow kR_i$);
3. add a multiple of one row to another ($R_i \rightarrow R_i - mR_j$).

The third is the workhorse. To kill the entry in column $k$ of row $i$, use the
**multiplier**

$$ m_{ik} = \frac{a_{ik}}{a_{kk}}, \qquad R_i \rightarrow R_i - m_{ik}R_k $$

where row $k$ is the **pivot row** and $a_{kk}$ the **pivot**.

::: key The two phases
**Forward elimination.** Use $R_1$ to clear column $1$ below the diagonal, then
$R_2$ to clear column $2$ below the diagonal, and so on, until the table is upper
triangular.

**Back substitution.** The last row now involves one unknown only. Solve it, put
the value into the row above, and climb upwards.
:::

::: example Worked example 15.1
**Problem.** Solve by Gauss elimination:
$\;x+y+z=6,\;\;2x+3y+z=11,\;\;3x+y+4z=17.$

**Solution.** Augmented matrix, written as a table:

| step | $x$ | $y$ | $z$ | RHS | operation |
|---|---|---|---|---|---|
| $R_1$ | $1$ | $1$ | $1$ | $6$ | pivot row |
| $R_2$ | $2$ | $3$ | $1$ | $11$ | |
| $R_3$ | $3$ | $1$ | $4$ | $17$ | |

Multipliers for column $1$: $m_{21} = 2/1 = 2$ and $m_{31} = 3/1 = 3$.

| step | $x$ | $y$ | $z$ | RHS | operation |
|---|---|---|---|---|---|
| $R_1$ | $1$ | $1$ | $1$ | $6$ | unchanged |
| $R_2'$ | $0$ | $1$ | $-1$ | $-1$ | $R_2 - 2R_1$ |
| $R_3'$ | $0$ | $-2$ | $1$ | $-1$ | $R_3 - 3R_1$ |

Now column $2$, with $R_2'$ as pivot row: $m_{32} = -2/1 = -2$.

| step | $x$ | $y$ | $z$ | RHS | operation |
|---|---|---|---|---|---|
| $R_1$ | $1$ | $1$ | $1$ | $6$ | |
| $R_2'$ | $0$ | $1$ | $-1$ | $-1$ | |
| $R_3''$ | $0$ | $0$ | $-1$ | $-3$ | $R_3' + 2R_2'$ |

**Back substitution.** From $R_3''$: $\;-z = -3 \Rightarrow z = 3$.
From $R_2'$: $\;y - z = -1 \Rightarrow y = -1 + 3 = 2$.
From $R_1$: $\;x + y + z = 6 \Rightarrow x = 6 - 2 - 3 = 1$.

$$ x = 1,\qquad y = 2,\qquad z = 3 $$

**Check** in the equation not used last: $3(1) + 2 + 4(3) = 3+2+12 = 17$. Correct.
:::

::: example Worked example 15.2
**Problem.** Solve $\;2x+y-z=8,\;\;-3x-y+2z=-11,\;\;-2x+y+2z=-3.$

**Solution.** Pivot $a_{11} = 2$, so $m_{21} = -3/2$ and $m_{31} = -2/2 = -1$.

| step | $x$ | $y$ | $z$ | RHS | operation |
|---|---|---|---|---|---|
| $R_1$ | $2$ | $1$ | $-1$ | $8$ | |
| $R_2'$ | $0$ | $\frac12$ | $\frac12$ | $1$ | $R_2 + \frac32 R_1$ |
| $R_3'$ | $0$ | $2$ | $1$ | $5$ | $R_3 + R_1$ |

Column $2$: $m_{32} = 2 \div \frac12 = 4$.

| step | $x$ | $y$ | $z$ | RHS | operation |
|---|---|---|---|---|---|
| $R_1$ | $2$ | $1$ | $-1$ | $8$ | |
| $R_2'$ | $0$ | $\frac12$ | $\frac12$ | $1$ | |
| $R_3''$ | $0$ | $0$ | $-1$ | $1$ | $R_3' - 4R_2'$ |

Back substitution: $-z = 1 \Rightarrow z = -1$; then
$\frac12 y + \frac12(-1) = 1 \Rightarrow \frac12 y = \frac32 \Rightarrow y = 3$;
then $2x + 3 - (-1) = 8 \Rightarrow 2x = 4 \Rightarrow x = 2$.

$$ x = 2,\qquad y = 3,\qquad z = -1 $$
:::

### When the pivot is zero: partial pivoting

If a pivot comes out $0$ you cannot divide by it. Swap the pivot row with a lower
row whose entry in that column is non-zero — operation (1), so nothing is lost.
Choosing the row with the **largest** entry in that column is called *partial
pivoting*; it also keeps rounding errors small, which is why every computer
program does it.

::: example Worked example 15.3
**Problem.** Solve $\;x+y+z=6,\;\;2x+2y+5z=21,\;\;4x+6y+8z=40$ by Gauss
elimination with row interchange where necessary.

**Solution.** $m_{21} = 2$, $m_{31} = 4$:

| step | $x$ | $y$ | $z$ | RHS | operation |
|---|---|---|---|---|---|
| $R_1$ | $1$ | $1$ | $1$ | $6$ | |
| $R_2'$ | $0$ | $0$ | $3$ | $9$ | $R_2 - 2R_1$ |
| $R_3'$ | $0$ | $2$ | $4$ | $16$ | $R_3 - 4R_1$ |

The next pivot would be the $0$ in position $(2,2)$ — impossible. **Swap
$R_2' \leftrightarrow R_3'$:**

| step | $x$ | $y$ | $z$ | RHS |
|---|---|---|---|---|
| $R_1$ | $1$ | $1$ | $1$ | $6$ |
| $R_2''$ | $0$ | $2$ | $4$ | $16$ |
| $R_3''$ | $0$ | $0$ | $3$ | $9$ |

The table is already upper triangular, so no more elimination is needed.
$3z = 9 \Rightarrow z = 3$; $2y + 12 = 16 \Rightarrow y = 2$;
$x = 6 - 2 - 3 = 1$.

$$ x = 1,\qquad y = 2,\qquad z = 3 $$
:::

::: caution A zero pivot is not "no solution"
A zero in the pivot position only means *swap rows*. You may conclude something
about the system only when a whole row of the coefficient part becomes zero:
- $0\;0\;0\,|\,k$ with $k \ne 0$ — impossible equation, the system is
  **inconsistent** (no solution);
- $0\;0\;0\,|\,0$ — a redundant equation, so there are **infinitely many
  solutions**.
:::

::: example Worked example 15.4
**Problem.** In a Pokhara stationery shop, $1$ pen, $1$ notebook and $1$ eraser
cost Rs $60$ together. Two pens, three notebooks and one eraser cost Rs $110$;
three pens, one notebook and four erasers cost Rs $170$. Find each price.

**Solution.** Let the prices be $x$, $y$, $z$ rupees. Then

$$ x+y+z = 60,\qquad 2x+3y+z = 110,\qquad 3x+y+4z = 170 $$

These are the equations of Worked example 15.1 with every right-hand side
multiplied by $10$, so every unknown is $10$ times larger:

$$ x = 10,\qquad y = 20,\qquad z = 30 $$

A pen costs Rs $10$, a notebook Rs $20$ and an eraser Rs $30$.
**Check:** $3(10)+20+4(30) = 30+20+120 = 170$. Correct.
:::

::: tip Keep fractions as fractions
Do not convert $\frac12$ to $0.5$ and $\frac13$ to $0.333$ during elimination. In
a hand-worked exam answer, fractions stay exact and the final check works
perfectly; decimals accumulate rounding error and cost you the check mark.
:::

## 15.2 System of linear equations: Gauss–Seidel Method

Elimination is *direct*: a fixed number of steps and you are finished. The
Gauss–Seidel method is *iterative*: you start with a guess and improve it over
and over, stopping when the numbers stop changing to the accuracy you want.

### Setting up the iteration

Solve each equation for the unknown on its own diagonal:

::: key The Gauss–Seidel iteration formulas
For $a_{11}x + a_{12}y + a_{13}z = b_1$ and its two companions,

$$ x^{(k+1)} = \frac{1}{a_{11}}\left(b_1 - a_{12}y^{(k)} - a_{13}z^{(k)}\right) $$
$$ y^{(k+1)} = \frac{1}{a_{22}}\left(b_2 - a_{21}x^{(k+1)} - a_{23}z^{(k)}\right) $$
$$ z^{(k+1)} = \frac{1}{a_{33}}\left(b_3 - a_{31}x^{(k+1)} - a_{32}y^{(k+1)}\right) $$

The point of Gauss–Seidel is the superscript $(k+1)$ on the right: **use each new
value the moment you have it**, within the same iteration. (Waiting until the end
of the sweep gives the slower Jacobi method.)
:::

Start from $x^{(0)} = y^{(0)} = z^{(0)} = 0$ unless the question says otherwise.

### Will it converge?

::: definition Diagonal dominance
A square matrix is **diagonally dominant** if in every row the size of the
diagonal entry exceeds the sum of the sizes of the other entries in that row:

$$ |a_{ii}| > \sum_{j \ne i} |a_{ij}| \quad \text{for every } i $$
:::

If the coefficient matrix is diagonally dominant, Gauss–Seidel converges from
*any* starting guess. If it is not, the iteration may still converge — but it may
also fly apart, and then no amount of patience helps. If the rows of the given
system are not dominant, **reorder the equations** before you start.

```figure caption="Error $\max|x - x^{\ast}|$ after each Gauss–Seidel sweep, on a log scale. The diagonally dominant system of Worked example 15.5 divides its error by about $65$ per sweep; the non-dominant system of the caution box multiplies its error by exactly $12$ each sweep."
import numpy as np
fig, ax = plt.subplots(figsize=(5.0,2.9))
def sweep(A, b, n):
    A = np.array(A, float); b = np.array(b, float)
    xs = np.linalg.solve(A, b); x = np.zeros(len(b)); errs = []
    for _ in range(n):
        for i in range(len(b)):
            x[i] = (b[i] - sum(A[i][j]*x[j] for j in range(len(b)) if j != i))/A[i][i]
        errs.append(np.abs(x - xs).max())
    return np.array(errs)
e1 = sweep([[20,1,-2],[3,20,-1],[2,-3,20]], [17,-18,25], 6)
e2 = sweep([[1,3],[4,1]], [5,6], 6)
k = np.arange(1, 7)
ax.semilogy(k, np.maximum(e1, 1e-16), 'o-', color=ACCENT, ms=5,
            label='diagonally dominant → converges')
ax.semilogy(k, e2, 's-', color='#d9534f', ms=5,
            label='not dominant → diverges')
ax.axhline(1e-6, color=MUTED, lw=0.9, ls='--')
ax.text(6.25, 1.8e-6, '6 d.p.', fontsize=8.2, color=MUTED, ha='right')
ax.set_xlabel('iteration  $k$'); ax.set_ylabel('largest error in a variable')
ax.set_xlim(0.7, 6.3); ax.set_ylim(1e-11, 1e8)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, which='major', alpha=.5); ax.legend(loc='upper center')
```

::: example Worked example 15.5
**Problem.** Solve, correct to three decimal places, by the Gauss–Seidel method:

$$ 20x + y - 2z = 17,\qquad 3x + 20y - z = -18,\qquad 2x - 3y + 20z = 25 $$

**Solution.** Each row is dominant ($20 > 1+2$, $20 > 3+1$, $20 > 2+3$), so the
method will converge. Rearranged:

$$ x = \frac{17 - y + 2z}{20},\quad y = \frac{-18 - 3x + z}{20},\quad
z = \frac{25 - 2x + 3y}{20} $$

Start at $x=y=z=0$ and tabulate. (In each row, $y$ uses the $x$ just found, and
$z$ uses both.)

| $k$ | $x^{(k)}$ | $y^{(k)}$ | $z^{(k)}$ |
|---|---|---|---|
| $0$ | $0$ | $0$ | $0$ |
| $1$ | $0.850000$ | $-1.027500$ | $1.010875$ |
| $2$ | $1.002462$ | $-0.999826$ | $0.999780$ |
| $3$ | $0.999969$ | $-1.000006$ | $1.000002$ |
| $4$ | $1.000001$ | $-1.000000$ | $1.000000$ |
| $5$ | $1.000000$ | $-1.000000$ | $1.000000$ |

Row $1$ in full, to show the arithmetic:
$x^{(1)} = \frac{17-0+0}{20} = 0.85$;
$y^{(1)} = \frac{-18-3(0.85)+0}{20} = \frac{-20.55}{20} = -1.0275$;
$z^{(1)} = \frac{25-2(0.85)+3(-1.0275)}{20} = \frac{20.2175}{20} = 1.010875$.

Iterations $4$ and $5$ agree to six decimal places, so

$$ x = 1.000,\qquad y = -1.000,\qquad z = 1.000 $$
:::

::: example Worked example 15.6
**Problem.** Perform four Gauss–Seidel iterations on
$\;10x+y+z=12,\;\;2x+10y+z=13,\;\;2x+2y+10z=14.$

**Solution.** $x = \frac{12-y-z}{10}$, $y = \frac{13-2x-z}{10}$,
$z = \frac{14-2x-2y}{10}$.

| $k$ | $x^{(k)}$ | $y^{(k)}$ | $z^{(k)}$ |
|---|---|---|---|
| $0$ | $0$ | $0$ | $0$ |
| $1$ | $1.200000$ | $1.060000$ | $0.948000$ |
| $2$ | $0.999200$ | $1.005360$ | $0.999088$ |
| $3$ | $0.999555$ | $1.000180$ | $1.000053$ |
| $4$ | $0.999977$ | $0.999999$ | $1.000005$ |

The values are settling on $x = y = z = 1$, which satisfies all three equations
exactly ($10+1+1 = 12$, $2+10+1 = 13$, $2+2+10 = 14$).
:::

The reason iteration works is easy to see with two unknowns. Solving for $x$ moves
you horizontally onto the first line; solving for $y$ moves you vertically onto
the second. The path is a staircase that closes in on the intersection.

```figure caption="Gauss–Seidel on $5x+y=13$ and $x+4y=14$. From $(0,0)$ each half-step lands on one of the two lines, and the staircase converges to the solution $(2,3)$."
import numpy as np
fig, ax = plt.subplots(figsize=(4.8,3.0))
xs = np.linspace(0, 3.4, 50)
ax.plot(xs, 13-5*xs, color=ACCENT, lw=1.6, label='$5x+y=13$')
ax.plot(xs, (14-xs)/4, color='#2e8b57', lw=1.6, label='$x+4y=14$')
x, y = 0.0, 0.0
px, py = [x], [y]
for _ in range(4):
    x = (13-y)/5; px.append(x); py.append(y)
    y = (14-x)/4; px.append(x); py.append(y)
ax.plot(px, py, '-', color='#d9534f', lw=1.3)
ax.plot(px, py, 'o', color='#d9534f', ms=3.2)
ax.plot([2], [3], '*', color=INK, ms=13)
ax.annotate('solution $(2,3)$', (2, 3), textcoords='offset points',
            xytext=(-96, 22), fontsize=9.0, color=INK,
            arrowprops=dict(arrowstyle='-', color=INK, lw=0.8))
ax.annotate('start $(0,0)$', (0, 0), textcoords='offset points',
            xytext=(6, 6), fontsize=9.0, color='#d9534f')
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.set_xlim(-0.3, 3.4); ax.set_ylim(-0.5, 4.4)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.45); ax.legend(loc='upper right')
```

::: caution Check dominance before you iterate
For $x + 3y = 5$, $4x + y = 6$ the first row has $|1| < |3|$, so the system is
not dominant and Gauss–Seidel explodes: $(5, -14)$, $(47, -182)$,
$(551, -2198)$, …, although the true solution is only
$x = \tfrac{13}{11}$, $y = \tfrac{14}{11}$. **Swap the two equations** to get
$4x + y = 6$, $x + 3y = 5$; both rows are then dominant and the iteration
converges. One row interchange is the difference between an answer and a
disaster.
:::

::: example Worked example 15.7
**Problem.** Explain why Gauss–Seidel applied as written to
$\;x + 4y - z = 6,\;\;5x - y + z = 7,\;\;x + y + 6z = 12$ is unsafe, and fix it.

**Solution.** Row $1$: $|1| < |4| + |-1| = 5$ — not dominant. Row $2$:
$|-1| < |5| + |1| = 6$ — not dominant. Row $3$: $|6| > |1| + |1|$ — dominant.

Reorder the equations so the largest coefficient of each unknown sits on the
diagonal. Put the $5x$ equation first and the $4y$ equation second:

$$ 5x - y + z = 7,\qquad x + 4y - z = 6,\qquad x + y + 6z = 12 $$

Now $5 > 1+1$, $4 > 1+1$ and $6 > 1+1$: all three rows are dominant, so the
iteration $x = \frac{7+y-z}{5}$, $y = \frac{6-x+z}{4}$, $z = \frac{12-x-y}{6}$ is
safe to run.
:::

## 15.3 Linear programming problems (LPP): simplex method (two variables)

A **linear programming problem** asks for the largest (or smallest) value of a
linear expression when the variables obey linear inequalities.

::: definition The parts of an LPP
- **Decision variables** $x, y \ge 0$ — what you choose.
- **Objective function** $Z = c_1x + c_2y$ — what you maximise.
- **Constraints** $a_1x + b_1y \le d_1$, … — the limits you must respect.
- **Feasible region** — the set of points satisfying every constraint.
:::

The feasible region of a two-variable problem is a convex polygon, and the
optimum always sits at a **corner** of it. That is the whole idea: instead of
testing infinitely many points, test the corners.

```figure caption="Feasible region for $x+y \le 4$, $x+3y \le 6$, $x,y \ge 0$. The objective line $3x+5y = c$ is drawn for $c = 5, 14, 20$. Sliding it outwards, the last corner it touches is $C(3,1)$, where $Z = 14$."
import numpy as np
fig, ax = plt.subplots(figsize=(5.1,3.0))
V = np.array([[0,0],[4,0],[3,1],[0,2]])
ax.fill(V[:,0], V[:,1], color=ACCENT, alpha=0.18, zorder=1)
xb = np.linspace(-0.2, 4.9, 30)
ax.plot(xb, 4-xb, color=ACCENT, lw=1.7, zorder=3)
xg = np.linspace(-0.2, 6.4, 30)
ax.plot(xg, (6-xg)/3, color='#2e8b57', lw=1.7, zorder=3)
ax.text(4.62, -0.83, '$x+y=4$', color=ACCENT, fontsize=8.8)
ax.text(5.55, 0.20, '$x+3y=6$', color='#2e8b57', fontsize=8.8)
xo = np.linspace(-0.2, 6.6, 30)
for c, st, lw in [(5,(0,(3,2)),1.0), (14,'-',1.9), (20,(0,(3,2)),1.0)]:
    ax.plot(xo, (c - 3*xo)/5, ls=st, color='#d9534f', lw=lw, zorder=2)
ax.text(0.07, 1.10, '$Z=5$', color='#d9534f', fontsize=8.4)
ax.text(0.63, 2.50, '$Z=14$', color='#d9534f', fontsize=9.2)
ax.text(2.56, 2.56, '$Z=20$', color='#d9534f', fontsize=8.4)
ax.annotate('', xy=(5.35, 2.55), xytext=(4.15, 1.95),
            arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.3, mutation_scale=11))
ax.text(4.10, 2.70, '$Z$ increases', color='#d9534f', fontsize=8.8)
for (px, py), lab, off in zip(V, ['O(0,0)', 'B(4,0)', 'C(3,1)', 'A(0,2)'],
                              [(7,-13), (0,-15), (11,1), (7,5)]):
    ax.plot([px], [py], 'o', color=INK, ms=4.8, zorder=6)
    ax.annotate(lab, (px, py), textcoords='offset points', xytext=off,
                fontsize=9.0, color=INK, zorder=6)
ax.plot([3], [1], 'o', color='#d9534f', ms=10, mfc='none', mew=1.8, zorder=7)
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.set_xlim(-0.4, 6.7); ax.set_ylim(-0.95, 3.15)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.4)
```

### Slack variables and standard form

An inequality cannot be put in a table, so turn each $\le$ constraint into an
equation by adding a non-negative **slack variable** that soaks up the unused
capacity:

$$ x+y \le 4 \;\Longrightarrow\; x+y+s_1 = 4, \qquad s_1 \ge 0 $$

::: key Standard form for the simplex method
$$ \text{Maximise } Z = c_1x + c_2y \quad\text{written as}\quad Z - c_1x - c_2y = 0 $$
subject to $a_ix + b_iy + s_i = d_i$ and $x, y, s_i \ge 0$.

All $d_i$ must be $\ge 0$. To **minimise** $Z$, maximise $-Z$ instead and change
the sign of the answer at the end.
:::

### The tableau and the pivot rules

The starting tableau lists the constraint equations, then the objective row. The
**basic** variables are the slacks (value $d_i$) and the non-basic variables $x$,
$y$ are zero — that is the corner $(0,0)$.

::: memory Three rules, in order
1. **Pivot column** — the objective row's *most negative* entry. (No negative
   entry left $\Rightarrow$ you are at the optimum; stop.)
2. **Pivot row** — compute ratio $= \dfrac{\text{RHS}}{\text{pivot-column entry}}$
   for the **positive** entries only, and choose the *smallest* ratio.
3. **Pivot** — divide the pivot row by the pivot element to make it $1$, then add
   multiples of that row to every other row (including the objective row) to make
   the rest of the pivot column $0$.
:::

::: example Worked example 15.8
**Problem.** Maximise $Z = 3x + 5y$ subject to $x+y \le 4$, $x+3y \le 6$,
$x, y \ge 0$, by the simplex method.

**Solution.** Add slacks: $x+y+s_1 = 4$, $x+3y+s_2 = 6$, and write
$Z - 3x - 5y = 0$.

**Tableau 1.**

| basic | $x$ | $y$ | $s_1$ | $s_2$ | RHS | ratio |
|---|---|---|---|---|---|---|
| $s_1$ | $1$ | $1$ | $1$ | $0$ | $4$ | $4/1 = 4$ |
| $s_2$ | $1$ | $\mathbf{3}$ | $0$ | $1$ | $6$ | $6/3 = 2$ ← |
| $Z$ | $-3$ | $-5$ | $0$ | $0$ | $0$ | |

Most negative entry is $-5$, so $y$ enters. Smallest ratio is $2$, so row $s_2$
leaves; the pivot is $3$.

Divide the pivot row by $3$, then $R_1 \rightarrow R_1 - R_2$ and
$Z \rightarrow Z + 5R_2$.

**Tableau 2.**

| basic | $x$ | $y$ | $s_1$ | $s_2$ | RHS | ratio |
|---|---|---|---|---|---|---|
| $s_1$ | $\mathbf{\frac23}$ | $0$ | $1$ | $-\frac13$ | $2$ | $2 \div \frac23 = 3$ ← |
| $y$ | $\frac13$ | $1$ | $0$ | $\frac13$ | $2$ | $2 \div \frac13 = 6$ |
| $Z$ | $-\frac43$ | $0$ | $0$ | $\frac53$ | $10$ | |

Still one negative, $-\frac43$, so $x$ enters; smallest ratio $3$, so $s_1$
leaves and the pivot is $\frac23$. Multiply that row by $\frac32$, then
$R_2 \rightarrow R_2 - \frac13 R_1$ and $Z \rightarrow Z + \frac43 R_1$.

**Tableau 3.**

| basic | $x$ | $y$ | $s_1$ | $s_2$ | RHS |
|---|---|---|---|---|---|
| $x$ | $1$ | $0$ | $\frac32$ | $-\frac12$ | $3$ |
| $y$ | $0$ | $1$ | $-\frac12$ | $\frac12$ | $1$ |
| $Z$ | $0$ | $0$ | $2$ | $1$ | $14$ |

No negative entry in the $Z$ row, so this is optimal:

$$ x = 3,\qquad y = 1,\qquad Z_{\max} = 14 $$

**Check.** $x+y = 4 \le 4$ and $x+3y = 6 \le 6$ — both tight, so both slacks are
zero, and $3(3)+5(1) = 14$. The corner is $C(3,1)$ in the figure above.
:::

Each tableau is one corner of the feasible region, and each pivot is a walk along
one edge to a better corner. The simplex method never goes backwards, which is
why it stops.

```figure caption="The same problem seen as a walk on corners. Tableau 1 is $O(0,0)$, Tableau 2 is $A(0,2)$ and Tableau 3 is $C(3,1)$, where $Z=14$. The value of $Z$ rises $0 \rightarrow 10 \rightarrow 14$."
import numpy as np
fig, ax = plt.subplots(figsize=(4.8,2.9))
V = np.array([[0,0],[4,0],[3,1],[0,2]])
ax.fill(V[:,0], V[:,1], color=ACCENT, alpha=0.14, zorder=1)
ax.plot(np.append(V[:,0], V[0,0]), np.append(V[:,1], V[0,1]), color=MUTED, lw=1.1)
path = np.array([[0,0],[0,2],[3,1]])
for i in range(2):
    ax.annotate('', xy=path[i+1], xytext=path[i],
                arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.9,
                                mutation_scale=13, shrinkA=7, shrinkB=9))
for (px, py), lab, z in [((0,0), 'O(0,0)', '$Z=0$'), ((0,2), 'A(0,2)', '$Z=10$'),
                         ((3,1), 'C(3,1)', '$Z=14$'), ((4,0), 'B(4,0)', '$Z=12$')]:
    ax.plot([px], [py], 'o', color=INK, ms=4.8, zorder=5)
    ax.annotate(f'{lab}\n{z}', (px, py), textcoords='offset points',
                xytext=(8, 4) if px < 3.5 else (-4, 8), fontsize=8.8, color=INK)
ax.text(0.13, 0.95, 'pivot 1', color='#d9534f', fontsize=8.6)
ax.text(1.35, 1.72, 'pivot 2', color='#d9534f', fontsize=8.6)
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.set_xlim(-0.4, 5.2); ax.set_ylim(-0.45, 2.9)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.4)
```

::: example Worked example 15.9
**Problem.** A furniture workshop in Butwal makes chairs and tables. A chair needs
$4$ hours of carpentry and $2$ hours of finishing; a table needs $2$ hours of
carpentry and $4$ hours of finishing. Only $60$ carpentry hours and $48$
finishing hours are available in a week. The profit is Rs $800$ on a chair and
Rs $600$ on a table. How many of each should be made, and what is the maximum
profit?

**Solution.** Let $x$ chairs and $y$ tables be made, and measure profit in
hundreds of rupees, $Z = 8x + 6y$.

$$ 4x + 2y \le 60,\qquad 2x + 4y \le 48,\qquad x, y \ge 0 $$

**Tableau 1.**

| basic | $x$ | $y$ | $s_1$ | $s_2$ | RHS | ratio |
|---|---|---|---|---|---|---|
| $s_1$ | $\mathbf{4}$ | $2$ | $1$ | $0$ | $60$ | $15$ ← |
| $s_2$ | $2$ | $4$ | $0$ | $1$ | $48$ | $24$ |
| $Z$ | $-8$ | $-6$ | $0$ | $0$ | $0$ | |

$x$ enters, $s_1$ leaves, pivot $4$. Divide $R_1$ by $4$;
$R_2 \rightarrow R_2 - 2R_1$; $Z \rightarrow Z + 8R_1$.

**Tableau 2.**

| basic | $x$ | $y$ | $s_1$ | $s_2$ | RHS | ratio |
|---|---|---|---|---|---|---|
| $x$ | $1$ | $\frac12$ | $\frac14$ | $0$ | $15$ | $30$ |
| $s_2$ | $0$ | $\mathbf{3}$ | $-\frac12$ | $1$ | $18$ | $6$ ← |
| $Z$ | $0$ | $-2$ | $2$ | $0$ | $120$ | |

$y$ enters, $s_2$ leaves, pivot $3$. Divide $R_2$ by $3$;
$R_1 \rightarrow R_1 - \frac12 R_2$; $Z \rightarrow Z + 2R_2$.

**Tableau 3.**

| basic | $x$ | $y$ | $s_1$ | $s_2$ | RHS |
|---|---|---|---|---|---|
| $x$ | $1$ | $0$ | $\frac13$ | $-\frac16$ | $12$ |
| $y$ | $0$ | $1$ | $-\frac16$ | $\frac13$ | $6$ |
| $Z$ | $0$ | $0$ | $\frac53$ | $\frac23$ | $132$ |

All entries of the $Z$ row are $\ge 0$, so stop: $x = 12$, $y = 6$, $Z = 132$.

Make **$12$ chairs and $6$ tables** for a maximum profit of
$132 \times 100 =$ **Rs $13{,}200$**.
**Check:** carpentry $4(12)+2(6) = 60$ h, finishing $2(12)+4(6) = 48$ h — both
fully used, and $800(12) + 600(6) = 9600 + 3600 = 13{,}200$.
:::

::: example Worked example 15.10
**Problem.** Maximise $Z = 5x + 3y$ subject to $x + y \le 6$, $2x + 3y \le 15$,
$x, y \ge 0$.

**Solution.** **Tableau 1.**

| basic | $x$ | $y$ | $s_1$ | $s_2$ | RHS | ratio |
|---|---|---|---|---|---|---|
| $s_1$ | $\mathbf{1}$ | $1$ | $1$ | $0$ | $6$ | $6$ ← |
| $s_2$ | $2$ | $3$ | $0$ | $1$ | $15$ | $7.5$ |
| $Z$ | $-5$ | $-3$ | $0$ | $0$ | $0$ | |

Pivot $1$ in row $s_1$, column $x$. Row $1$ is already divided;
$R_2 \rightarrow R_2 - 2R_1$; $Z \rightarrow Z + 5R_1$.

**Tableau 2.**

| basic | $x$ | $y$ | $s_1$ | $s_2$ | RHS |
|---|---|---|---|---|---|
| $x$ | $1$ | $1$ | $1$ | $0$ | $6$ |
| $s_2$ | $0$ | $1$ | $-2$ | $1$ | $3$ |
| $Z$ | $0$ | $2$ | $5$ | $0$ | $30$ |

No negative entry remains, so the optimum has been reached after **one** pivot:

$$ x = 6,\qquad y = 0,\qquad Z_{\max} = 30 $$

The second constraint is slack ($s_2 = 3$, i.e. $2(6) + 0 = 12 < 15$), which the
tableau tells you directly.
:::

::: caution Ratios use positive entries only
When choosing the pivot row, ignore any row whose pivot-column entry is $0$ or
negative — a negative ratio is meaningless and would let a variable go negative.
If *every* entry in the pivot column is $\le 0$, the feasible region is unbounded
in that direction and $Z$ has no maximum; say so.
:::

## 15.4 How accurate is a computed answer?

Gauss–Seidel and the simplex method both *stop somewhere*. A computed answer is
therefore only as good as the error attached to it, and every numerical method
comes with an error estimate. Two more retained methods make the point sharply;
Unit 17 §17.3 revises the integration rules in exam form.

### Newton–Raphson: doubling the correct digits each step

To solve $f(x) = 0$, take a guess $x_0$, follow the tangent to the curve down to
the $x$-axis, and use where it lands as the next guess. The tangent at
$(x_n, f(x_n))$ meets $y = 0$ at

::: key Newton–Raphson formula
$$ x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}, \qquad f'(x_n) \ne 0 $$
Near a simple root the error is **squared** each step, so the number of correct
decimal places roughly doubles per iteration.
:::

```figure caption="Newton–Raphson on $f(x) = x^3 - 2x - 5$ from $x_0 = 3$. Each tangent (dashed) crosses the axis much closer to the root $\alpha \approx 2.0946$ than the point it was drawn at."
import numpy as np
fig, ax = plt.subplots(figsize=(5.0,3.0))
f = lambda x: x**3 - 2*x - 5
fp = lambda x: 3*x**2 - 2
xs = np.linspace(1.7, 3.15, 300)
ax.plot(xs, f(xs), color=ACCENT, lw=1.9, label='$f(x)=x^3-2x-5$')
ax.axhline(0, color=INK, lw=1.0)
x = 3.0
cols = ['#d9534f', '#b8860b', '#2e8b57']
for i in range(3):
    xn = x - f(x)/fp(x)
    ax.plot([x, xn], [f(x), 0], ls='--', color=cols[i], lw=1.2)
    ax.plot([x, x], [0, f(x)], ls=':', color=MUTED, lw=0.9)
    ax.plot([x], [f(x)], 'o', color=cols[i], ms=4.4)
    ax.plot([xn], [0], 'o', color=cols[i], ms=4.4)
    ax.annotate(f'$x_{i}$', (x, 0), textcoords='offset points',
                xytext=(-3, -14) if i < 2 else (13, -11), fontsize=9.2, color=cols[i])
    x = xn
ax.plot([2.0945515], [0], '*', color=INK, ms=13)
ax.annotate('root $\\alpha = 2.0946$', (2.0945515, 0), textcoords='offset points',
            xytext=(-14, -34), fontsize=9.0, color=INK, ha='left',
            arrowprops=dict(arrowstyle='-', color=INK, lw=0.8))
ax.set_xlabel('$x$'); ax.set_ylabel('$f(x)$')
ax.set_xlim(1.7, 3.2); ax.set_ylim(-5.0, 17)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.4); ax.legend(loc='upper left')
```

::: example Worked example 15.11
**Problem.** Find the real root of $x^3 - 2x - 5 = 0$ correct to four decimal
places, taking $x_0 = 2$.

**Solution.** $f(x) = x^3 - 2x - 5$, $f'(x) = 3x^2 - 2$, so

$$ x_{n+1} = x_n - \frac{x_n^3 - 2x_n - 5}{3x_n^2 - 2} $$

$f(2) = -1 < 0$ and $f(3) = 16 > 0$, so a root lies in $(2,3)$.

| $n$ | $x_n$ | $f(x_n)$ | $f'(x_n)$ | $x_{n+1}$ |
|---|---|---|---|---|
| $0$ | $2.000000$ | $-1.000000$ | $10.000000$ | $2.100000$ |
| $1$ | $2.100000$ | $0.061000$ | $11.230000$ | $2.094568$ |
| $2$ | $2.094568$ | $0.000186$ | $11.161647$ | $2.094551$ |
| $3$ | $2.094551$ | $0.000000$ | $11.161438$ | $2.094551$ |

Two successive iterates agree to six decimal places, so the root is

$$ x = 2.0946 \quad (4 \text{ d.p.}) $$

Notice the error sizes: $10^{-1}$, then $10^{-3}$, then $10^{-6}$ — squared each
time, as promised.
:::

::: example Worked example 15.12
**Problem.** Use the Newton–Raphson method to compute $\sqrt{5}$ to five decimal
places.

**Solution.** $\sqrt{5}$ is the positive root of $f(x) = x^2 - 5$, with
$f'(x) = 2x$. The formula simplifies:

$$ x_{n+1} = x_n - \frac{x_n^2 - 5}{2x_n} = \frac{x_n^2 + 5}{2x_n}
= \frac12\left(x_n + \frac{5}{x_n}\right) $$

Take $x_0 = 2$ (since $2^2 = 4$ is close to $5$).

| $n$ | $x_n$ | $x_{n+1} = \frac12\left(x_n + 5/x_n\right)$ |
|---|---|---|
| $0$ | $2.000000$ | $2.250000$ |
| $1$ | $2.250000$ | $2.236111$ |
| $2$ | $2.236111$ | $2.236068$ |
| $3$ | $2.236068$ | $2.236068$ |

$$ \sqrt{5} = 2.23607 \quad (5 \text{ d.p.}) $$
:::

### Order of a quadrature rule

For $\int_a^b f(x)\,dx$ with $n$ equal strips of width $h = \dfrac{b-a}{n}$ and
ordinates $y_0, y_1, \ldots, y_n$:

::: key The two rules and their error bounds
$$ \int_a^b f\,dx \approx \frac{h}{2}\left[y_0 + y_n + 2(y_1 + y_2 + \cdots + y_{n-1})\right] \quad \text{(trapezium)} $$
$$ \int_a^b f\,dx \approx \frac{h}{3}\left[y_0 + y_n + 4(y_1 + y_3 + \cdots) + 2(y_2 + y_4 + \cdots)\right] \quad \text{(Simpson, } n \text{ even)} $$

$$ |E_T| \le \frac{(b-a)h^2}{12}\max_{[a,b]}|f''(x)|, \qquad
|E_S| \le \frac{(b-a)h^4}{180}\max_{[a,b]}\left|f^{(4)}(x)\right| $$
:::

The trapezium rule replaces the curve by chords, so its error is proportional to
$h^2$; Simpson's rule replaces it by parabolas through three ordinates at a time,
so its error is proportional to $h^4$. Halving $h$ divides the trapezium error by
$4$ but the Simpson error by $16$.

```figure caption="$\int_1^5 \frac{dx}{x}$ with $n = 4$. Left: the four chords lie above the curve, so the trapezium rule over-estimates, giving $1.68333$ against $\ln 5 = 1.60944$. Right: the two parabolas of Simpson's rule sit almost on the curve, giving $1.62222$."
import numpy as np
fig, axes = plt.subplots(1, 2, figsize=(5.2,2.6), sharey=True)
f = lambda x: 1/x
xf = np.linspace(1, 5, 400)
xs = np.linspace(1, 5, 5); ys = f(xs)
for ax, title in zip(axes, ['trapezium,  $n=4$', "Simpson,  $n=4$"]):
    ax.set_title(title, fontsize=9.2)
    ax.set_xlim(0.75, 5.25); ax.set_ylim(0, 1.22)
    ax.spines[['top','right']].set_visible(False)
    ax.set_xlabel('$x$'); ax.set_xticks([1,2,3,4,5])
    for x0 in xs:
        ax.plot([x0, x0], [0, f(x0)], color=MUTED, lw=0.8, ls=':', zorder=3)
axes[0].fill_between(xs, 0, ys, color=ACCENT, alpha=0.18, zorder=2)
axes[0].plot(xs, ys, '-', color=ACCENT, lw=1.6, zorder=5)
for i in range(0, 4, 2):
    xa, xc = xs[i], xs[i+2]
    A = np.polyfit(xs[i:i+3], ys[i:i+3], 2)
    xp = np.linspace(xa, xc, 80)
    axes[1].fill_between(xp, 0, np.polyval(A, xp), color='#2e8b57', alpha=0.18, zorder=2)
    axes[1].plot(xp, np.polyval(A, xp), color='#2e8b57', lw=1.6, zorder=5)
for ax, c in zip(axes, [ACCENT, '#2e8b57']):
    ax.plot(xf, f(xf), color=INK, lw=2.2, zorder=6)
    ax.plot(xs, ys, 'o', color=c, ms=4.2, zorder=7)
axes[0].fill_between(xf, f(xf), np.interp(xf, xs, ys), color='#d9534f', alpha=0.45, zorder=4)
axes[0].annotate('error', (1.5, 0.71), textcoords='offset points', xytext=(10, 22),
                 fontsize=8.6, color='#d9534f',
                 arrowprops=dict(arrowstyle='-', color='#d9534f', lw=0.8))
axes[0].set_ylabel('$y = 1/x$')
for i, lab in enumerate(['$y_0$','$y_1$','$y_2$','$y_3$','$y_4$']):
    axes[0].text(xs[i], f(xs[i])+0.07, lab, fontsize=8.0, ha='center', color=MUTED)
axes[1].text(3.0, 0.90, 'curve and\nparabolas\nalmost coincide', fontsize=8.0,
             color=MUTED, ha='center', va='center')
fig.tight_layout()
```

```figure caption="Error against number of strips for $\int_0^1 \frac{dx}{1+x^2} = \frac{\pi}{4}$, both axes logarithmic. The slopes are $-2$ and $-4$: the trapezium error falls like $h^2$, Simpson's like $h^4$."
import numpy as np
fig, ax = plt.subplots(figsize=(4.8,2.9))
f = lambda x: 1/(1+x*x)
exact = np.pi/4
ns = np.array([2,4,8,16,32,64])
ET, ES = [], []
for n in ns:
    h = 1.0/n
    x = np.linspace(0, 1, n+1); y = f(x)
    T = h/2*(y[0] + y[-1] + 2*y[1:-1].sum())
    S = h/3*(y[0] + y[-1] + 4*y[1:-1:2].sum() + 2*y[2:-1:2].sum())
    ET.append(abs(T-exact)); ES.append(abs(S-exact))
ax.loglog(ns, ET, 'o-', color=ACCENT, ms=5, label='trapezium  (slope $-2$)')
ax.loglog(ns, ES, 's-', color='#2e8b57', ms=5, label="Simpson  (slope $-4$)")
ax.set_xlabel('number of strips  $n$  (log scale)')
ax.set_ylabel('absolute error (log scale)')
ax.set_xticks(ns); ax.set_xticklabels([str(v) for v in ns])
ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
ax.text(15.0, 2.2e-3, 'error $\\propto h^{2}$', color=ACCENT, fontsize=8.8)
ax.text(5.2, 1.2e-10, 'error $\\propto h^{4}$', color='#2e8b57', fontsize=8.8)
ax.set_ylim(1e-14, 1e-1)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, which='major', alpha=.45); ax.legend(loc='lower left')
```

::: example Worked example 15.13
**Problem.** Evaluate $\displaystyle\int_0^1 \frac{dx}{1+x^2}$ with $n = 4$ by
both the trapezium rule and Simpson's rule, state the error bound for each, and
compare with the exact value $\frac{\pi}{4}$.

**Solution.** $h = \dfrac{1-0}{4} = 0.25$. Ordinate table:

| $i$ | $x_i$ | $y_i = 1/(1+x_i^2)$ | used as |
|---|---|---|---|
| $0$ | $0.00$ | $1.000000$ | end |
| $1$ | $0.25$ | $0.941176$ | odd |
| $2$ | $0.50$ | $0.800000$ | even |
| $3$ | $0.75$ | $0.640000$ | odd |
| $4$ | $1.00$ | $0.500000$ | end |

**Trapezium.** Ends $= 1.000000 + 0.500000 = 1.500000$; others
$= 0.941176+0.800000+0.640000 = 2.381176$.

$$ T = \frac{0.25}{2}\left[1.500000 + 2(2.381176)\right] = 0.125(6.262353) = 0.782794 $$

**Simpson.** Odd ordinates $y_1 + y_3 = 1.581176$; even (interior)
$y_2 = 0.800000$.

$$ S = \frac{0.25}{3}\left[1.500000 + 4(1.581176) + 2(0.800000)\right]
= \frac{0.25}{3}(9.424706) = 0.785392 $$

**Error bounds.** Here $f''(x) = \dfrac{2(3x^2-1)}{(1+x^2)^3}$ and
$f^{(4)}(x)$ have maximum sizes $2$ and $24$ on $[0,1]$, so

$$ |E_T| \le \frac{1 \times (0.25)^2}{12}(2) = 0.01042, \qquad
|E_S| \le \frac{1 \times (0.25)^4}{180}(24) = 0.00052 $$

**Comparison.** $\frac{\pi}{4} = 0.785398$. The actual errors are
$0.002604$ and $0.000006$ — both comfortably inside their bounds, and Simpson is
about $400$ times more accurate for the same five ordinates.
:::

## Chapter summary

- **Gauss elimination.** Form $[A\,|\,b]$; use $R_i \rightarrow R_i - m_{ik}R_k$
  with $m_{ik} = a_{ik}/a_{kk}$ to make it upper triangular; back substitute. Swap
  rows if a pivot is $0$ (partial pivoting).
- A row $0\;0\;0\,|\,k$ with $k \ne 0$ means **no solution**; $0\;0\;0\,|\,0$
  means **infinitely many**.
- **Gauss–Seidel.** $x^{(k+1)} = \frac{1}{a_{11}}(b_1 - a_{12}y^{(k)} - a_{13}z^{(k)})$,
  and so on, always using the newest value available. Converges for certain when
  $|a_{ii}| > \sum_{j\ne i}|a_{ij}|$ in every row — reorder the equations if it is
  not so.
- Direct methods (elimination) finish in a set number of steps; iterative methods
  (Gauss–Seidel) are stopped when successive iterates agree to the required
  accuracy.
- **LPP.** Maximise $Z = c_1x + c_2y$ over a convex feasible region; the optimum
  lies at a corner.
- **Simplex.** Add slacks, write $Z - c_1x - c_2y = 0$. Pivot column = most
  negative $Z$ entry; pivot row = smallest positive ratio RHS $\div$ column
  entry; pivot to make the column $(1,0,\ldots,0)$. Stop when no $Z$ entry is
  negative.
- **Newton–Raphson.** $x_{n+1} = x_n - f(x_n)/f'(x_n)$; correct digits roughly
  double each step.
- **Quadrature.** Trapezium
  $\frac{h}{2}[y_0+y_n+2(\text{rest})]$ with $|E| \le \frac{(b-a)h^2}{12}\max|f''|$;
  Simpson $\frac{h}{3}[y_0+y_n+4(\text{odd})+2(\text{even})]$, $n$ even, with
  $|E| \le \frac{(b-a)h^4}{180}\max|f^{(4)}|$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. In Gauss elimination the augmented matrix is reduced to <span class="marks">[1]</span>
   (a) a diagonal matrix (b) an upper triangular matrix (c) an identity matrix (d) a symmetric matrix
2. The Gauss–Seidel method is certain to converge if the coefficient matrix is <span class="marks">[1]</span>
   (a) symmetric (b) singular (c) diagonally dominant (d) triangular
3. In a simplex tableau the entering variable is chosen from the objective row's <span class="marks">[1]</span>
   (a) largest positive entry (b) most negative entry (c) smallest ratio (d) last column
4. A slack variable added to $3x + 4y \le 12$ satisfies <span class="marks">[1]</span>
   (a) $s \le 0$ (b) $s = 0$ (c) $s \ge 0$ (d) $s = 12$
5. If a row of the reduced augmented matrix reads $0\;0\;0\,|\,5$, the system has <span class="marks">[1]</span>
   (a) a unique solution (b) no solution (c) infinitely many solutions (d) exactly two solutions
6. Simpson's rule can be applied only when the number of strips $n$ is <span class="marks">[1]</span>
   (a) odd (b) even (c) a multiple of $3$ (d) prime
7. For the Newton–Raphson method, $x_{n+1}$ equals <span class="marks">[1]</span>
   (a) $x_n + \frac{f(x_n)}{f'(x_n)}$ (b) $x_n - \frac{f'(x_n)}{f(x_n)}$ (c) $x_n - \frac{f(x_n)}{f'(x_n)}$ (d) $\frac{f(x_n)}{f'(x_n)}$

::: note Answers to Group A
**1.** (b) — forward elimination puts zeros below the diagonal so the last row has one unknown.

**2.** (c) — diagonal dominance guarantees convergence from any starting guess.

**3.** (b) — the most negative coefficient promises the fastest increase in $Z$.

**4.** (c) — slack measures unused capacity, which cannot be negative.

**5.** (b) — it states $0 = 5$, an impossibility, so the system is inconsistent.

**6.** (b) — the ordinates are taken three at a time (two strips per parabola).

**7.** (c) — the tangent at $x_n$ meets the $x$-axis at $x_n - f(x_n)/f'(x_n)$.
:::

**Group B — Short answer (5 marks each)**

1. Solve by Gauss elimination: $\;x + 2y + 3z = 14$, $\;2x + 5y + 2z = 18$,
   $\;3x + y + 5z = 20$. <span class="marks">[5]</span>
2. State the three elementary row operations and explain, with the system
   $2x + 4y = 6$, $\;3x + y = -1$, why a row interchange can be necessary during
   Gauss elimination. Solve the system. <span class="marks">[5]</span>
3. Carry out three iterations of the Gauss–Seidel method on
   $\;8x - 3y + 2z = 20$, $\;4x + 11y - z = 33$, $\;6x + 3y + 12z = 35$,
   starting from $(0,0,0)$. Give your answers to four decimal places. <span class="marks">[5]</span>
4. Test whether $\;x + 5y = 7$, $\;4x + y = 6$ is suitable for Gauss–Seidel as
   written. Rearrange if necessary and perform three iterations. <span class="marks">[5]</span>
5. Maximise $Z = 5x + 7y$ subject to $x + y \le 4$, $3x + 8y \le 24$,
   $x, y \ge 0$ by the simplex method. <span class="marks">[5]</span>
6. Using the Newton–Raphson method with $x_0 = 1$, find the root of
   $x^3 + x - 3 = 0$ correct to four decimal places. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Augmented matrix rows $(1,2,3\,|\,14)$, $(2,5,2\,|\,18)$, $(3,1,5\,|\,20)$.

$m_{21} = 2$: $R_2 - 2R_1 = (0,1,-4\,|\,-10)$.
$m_{31} = 3$: $R_3 - 3R_1 = (0,-5,-4\,|\,-22)$.
$m_{32} = -5$: $R_3 + 5R_2 = (0,0,-24\,|\,-72)$.

Back substitution: $-24z = -72 \Rightarrow z = 3$;
$y - 4(3) = -10 \Rightarrow y = 2$; $x + 2(2) + 3(3) = 14 \Rightarrow x = 1$.

$$ x = 1,\quad y = 2,\quad z = 3 $$

Check in equation $2$: $2(1) + 5(2) + 2(3) = 2 + 10 + 6 = 18$. Correct.

**2.** The operations are (i) $R_i \leftrightarrow R_j$, (ii) $R_i \rightarrow kR_i$
with $k \ne 0$, (iii) $R_i \rightarrow R_i - mR_j$. None of them changes the
solution set.

A swap is needed whenever the intended pivot $a_{kk}$ is zero, because the
multiplier $m_{ik} = a_{ik}/a_{kk}$ would require division by zero. (Swapping to
the largest available entry — partial pivoting — also limits rounding error.)

Here the pivot $2$ is non-zero, so no swap is needed: $m_{21} = \frac32$ gives
$R_2 - \frac32 R_1 = (0, -5\,|\,-10)$, so $y = 2$ and then
$2x + 8 = 6 \Rightarrow x = -1$. So $x = -1$, $y = 2$.

**3.** The rows are dominant ($8 > 5$, $11 > 5$, $12 > 9$). The formulas are
$x = \frac{20 + 3y - 2z}{8}$, $y = \frac{33 - 4x + z}{11}$,
$z = \frac{35 - 6x - 3y}{12}$.

| $k$ | $x^{(k)}$ | $y^{(k)}$ | $z^{(k)}$ |
|---|---|---|---|
| $1$ | $2.5000$ | $2.0909$ | $1.1439$ |
| $2$ | $2.9981$ | $2.0138$ | $0.9142$ |
| $3$ | $3.0266$ | $1.9825$ | $0.9077$ |

Row $1$ in detail: $x = \frac{20+0-0}{8} = 2.5$;
$y = \frac{33-4(2.5)+0}{11} = \frac{23}{11} = 2.0909$;
$z = \frac{35-6(2.5)-3(2.0909)}{12} = \frac{13.7273}{12} = 1.1439$.

Continuing gives $x \to 3.0168$, $y \to 1.9859$, $z \to 0.9118$; after three
iterations every value is already correct to one decimal place.

**4.** Row $1$ has $|1| < |5|$, so the system is **not** diagonally dominant as
written and Gauss–Seidel is unsafe. Interchange the equations:

$$ 4x + y = 6, \qquad x + 5y = 7 $$

Now $4 > 1$ and $5 > 1$: both rows dominant. With
$x = \frac{6-y}{4}$, $y = \frac{7-x}{5}$ from $(0,0)$:

| $k$ | $x^{(k)}$ | $y^{(k)}$ |
|---|---|---|
| $1$ | $1.500000$ | $1.100000$ |
| $2$ | $1.225000$ | $1.155000$ |
| $3$ | $1.211250$ | $1.157750$ |

The exact solution is $x = \frac{23}{19} = 1.210526$, $y = \frac{22}{19} = 1.157895$.

**5.** Slacks: $x+y+s_1 = 4$, $3x+8y+s_2 = 24$, and $Z - 5x - 7y = 0$.

| basic | $x$ | $y$ | $s_1$ | $s_2$ | RHS | ratio |
|---|---|---|---|---|---|---|
| $s_1$ | $1$ | $1$ | $1$ | $0$ | $4$ | $4$ |
| $s_2$ | $3$ | $\mathbf{8}$ | $0$ | $1$ | $24$ | $3$ ← |
| $Z$ | $-5$ | $-7$ | $0$ | $0$ | $0$ | |

$y$ enters, $s_2$ leaves, pivot $8$. After $R_2 \div 8$,
$R_1 - R_2$, $Z + 7R_2$:

| basic | $x$ | $y$ | $s_1$ | $s_2$ | RHS | ratio |
|---|---|---|---|---|---|---|
| $s_1$ | $\mathbf{\frac58}$ | $0$ | $1$ | $-\frac18$ | $1$ | $\frac85$ ← |
| $y$ | $\frac38$ | $1$ | $0$ | $\frac18$ | $3$ | $8$ |
| $Z$ | $-\frac{19}{8}$ | $0$ | $0$ | $\frac78$ | $21$ | |

$x$ enters, $s_1$ leaves, pivot $\frac58$. After $R_1 \times \frac85$,
$R_2 - \frac38 R_1$, $Z + \frac{19}{8}R_1$:

| basic | $x$ | $y$ | $s_1$ | $s_2$ | RHS |
|---|---|---|---|---|---|
| $x$ | $1$ | $0$ | $\frac85$ | $-\frac15$ | $\frac85$ |
| $y$ | $0$ | $1$ | $-\frac35$ | $\frac15$ | $\frac{12}{5}$ |
| $Z$ | $0$ | $0$ | $\frac{19}{5}$ | $\frac25$ | $\frac{124}{5}$ |

$$ x = \frac85 = 1.6,\qquad y = \frac{12}{5} = 2.4,\qquad Z_{\max} = \frac{124}{5} = 24.8 $$

Check: $1.6 + 2.4 = 4$ and $3(1.6) + 8(2.4) = 4.8 + 19.2 = 24$ — both tight.

**6.** $f(x) = x^3 + x - 3$, $f'(x) = 3x^2 + 1$. $f(1) = -1 < 0$, $f(2) = 7 > 0$,
so the root lies in $(1,2)$.

| $n$ | $x_n$ | $f(x_n)$ | $f'(x_n)$ | $x_{n+1}$ |
|---|---|---|---|---|
| $0$ | $1.000000$ | $-1.000000$ | $4.000000$ | $1.250000$ |
| $1$ | $1.250000$ | $0.203125$ | $5.687500$ | $1.214286$ |
| $2$ | $1.214286$ | $0.004738$ | $5.423469$ | $1.213412$ |
| $3$ | $1.213412$ | $0.000003$ | $5.417107$ | $1.213412$ |

$$ x = 1.2134 \quad (4 \text{ d.p.}) $$
:::

**Group C — Long answer (8 marks each)**

1. (a) Describe the Gauss elimination method, explaining the roles of the pivot,
   the multiplier and back substitution. <span class="marks">[3]</span>
   (b) Hence solve $\;2x + y + z = 10$, $\;3x + 2y + 3z = 18$,
   $\;x + 4y + 9z = 16$. <span class="marks">[5]</span>
2. (a) Write down the Gauss–Seidel iteration formulas for a $3 \times 3$ system
   and state the condition for convergence. Contrast a direct with an iterative
   method. <span class="marks">[3]</span>
   (b) Solve, correct to three decimal places,
   $\;10x + y - z = 11.19$, $\;x + 10y + z = 28.08$,
   $\;-x + y + 10z = 35.61$. <span class="marks">[5]</span>
3. (a) Explain what slack variables are and why the optimum of an LPP must occur
   at a corner of the feasible region. <span class="marks">[3]</span>
   (b) Maximise $Z = 4x + 3y$ subject to $2x + y \le 10$, $x + 3y \le 15$,
   $x, y \ge 0$ by the simplex method, and verify your answer by evaluating $Z$ at
   every corner of the feasible region. <span class="marks">[5]</span>

::: note Answers to Group C
**1.** (a) Write the system as the augmented matrix $[A\,|\,b]$. For each column
$k$ in turn, the diagonal entry $a_{kk}$ is the **pivot** and its row is the pivot
row; for every row $i$ below it form the **multiplier**
$m_{ik} = a_{ik}/a_{kk}$ and replace $R_i$ by $R_i - m_{ik}R_k$, which makes the
entry in column $k$ zero. If a pivot is zero, interchange with a lower row
(partial pivoting). After all columns are treated the matrix is upper triangular,
and **back substitution** solves the last equation for one unknown, substitutes
it into the row above, and works upwards.

(b) Rows $(2,1,1\,|\,10)$, $(3,2,3\,|\,18)$, $(1,4,9\,|\,16)$.

$m_{21} = \frac32$: $R_2 - \frac32R_1$ gives the row $0,\ \frac12,\ \frac32\ |\ 3$.
$m_{31} = \frac12$: $R_3 - \frac12R_1$ gives the row $0,\ \frac72,\ \frac{17}{2}\ |\ 11$.

$m_{32} = \frac72 \div \frac12 = 7$:
$R_3 - 7R_2 = (0, 0, -2\,|\,-10)$.

Back substitution: $-2z = -10 \Rightarrow z = 5$;
$\frac12 y + \frac{15}{2} = 3 \Rightarrow \frac12 y = -\frac92 \Rightarrow y = -9$;
$2x - 9 + 5 = 10 \Rightarrow 2x = 14 \Rightarrow x = 7$.

$$ x = 7,\qquad y = -9,\qquad z = 5 $$

Check in equation $3$: $7 + 4(-9) + 9(5) = 7 - 36 + 45 = 16$. Correct.

**2.** (a) With $x^{(0)} = y^{(0)} = z^{(0)} = 0$,

$$ x^{(k+1)} = \frac{b_1 - a_{12}y^{(k)} - a_{13}z^{(k)}}{a_{11}},\quad
y^{(k+1)} = \frac{b_2 - a_{21}x^{(k+1)} - a_{23}z^{(k)}}{a_{22}},\quad
z^{(k+1)} = \frac{b_3 - a_{31}x^{(k+1)} - a_{32}y^{(k+1)}}{a_{33}} $$

Convergence is guaranteed when the coefficient matrix is diagonally dominant,
$|a_{ii}| > \sum_{j \ne i}|a_{ij}|$ for every $i$. A **direct** method such as
Gauss elimination reaches the exact answer in a fixed, known number of arithmetic
steps; an **iterative** method produces a sequence of approximations and is
stopped when two successive ones agree to the wanted accuracy, so its cost depends
on the accuracy demanded and on how fast it converges.

(b) All rows are dominant ($10 > 2$ in each). Using
$x = \frac{11.19 - y + z}{10}$, $y = \frac{28.08 - x - z}{10}$,
$z = \frac{35.61 + x - y}{10}$:

| $k$ | $x^{(k)}$ | $y^{(k)}$ | $z^{(k)}$ |
|---|---|---|---|
| $1$ | $1.119000$ | $2.696100$ | $3.403290$ |
| $2$ | $1.189719$ | $2.348699$ | $3.445102$ |
| $3$ | $1.228640$ | $2.340626$ | $3.449801$ |
| $4$ | $1.229918$ | $2.340028$ | $3.449989$ |
| $5$ | $1.229996$ | $2.340001$ | $3.449999$ |

$$ x = 1.230,\qquad y = 2.340,\qquad z = 3.450 $$

Check in equation $3$: $-1.23 + 2.34 + 10(3.45) = 35.61$. Correct.

**3.** (a) A **slack variable** $s_i \ge 0$ is added to a $\le$ constraint to turn
it into an equation, $a_ix + b_iy + s_i = d_i$; its value is the amount of that
resource left unused. Because every constraint is linear, the feasible region is
the intersection of half-planes and is therefore a convex polygon. The objective
$Z = c_1x + c_2y$ is constant along a family of parallel lines; pushing such a
line in the direction of increasing $Z$, the last point of the polygon it meets is
either a vertex or (if the line is parallel to an edge) a whole edge whose
endpoints are vertices. Either way a vertex attains the maximum, so only the
corners need testing.

(b) Slacks: $2x + y + s_1 = 10$, $x + 3y + s_2 = 15$, and $Z - 4x - 3y = 0$.

| basic | $x$ | $y$ | $s_1$ | $s_2$ | RHS | ratio |
|---|---|---|---|---|---|---|
| $s_1$ | $\mathbf{2}$ | $1$ | $1$ | $0$ | $10$ | $5$ ← |
| $s_2$ | $1$ | $3$ | $0$ | $1$ | $15$ | $15$ |
| $Z$ | $-4$ | $-3$ | $0$ | $0$ | $0$ | |

$x$ enters, $s_1$ leaves, pivot $2$. After $R_1 \div 2$, $R_2 - R_1$, $Z + 4R_1$:

| basic | $x$ | $y$ | $s_1$ | $s_2$ | RHS | ratio |
|---|---|---|---|---|---|---|
| $x$ | $1$ | $\frac12$ | $\frac12$ | $0$ | $5$ | $10$ |
| $s_2$ | $0$ | $\mathbf{\frac52}$ | $-\frac12$ | $1$ | $10$ | $4$ ← |
| $Z$ | $0$ | $-1$ | $2$ | $0$ | $20$ | |

$y$ enters, $s_2$ leaves, pivot $\frac52$. After $R_2 \times \frac25$,
$R_1 - \frac12R_2$, $Z + R_2$:

| basic | $x$ | $y$ | $s_1$ | $s_2$ | RHS |
|---|---|---|---|---|---|
| $x$ | $1$ | $0$ | $\frac35$ | $-\frac15$ | $3$ |
| $y$ | $0$ | $1$ | $-\frac15$ | $\frac25$ | $4$ |
| $Z$ | $0$ | $0$ | $\frac95$ | $\frac25$ | $24$ |

No negative entry remains, so $x = 3$, $y = 4$, $Z_{\max} = 24$.

**Corner check.** The lines $2x+y=10$ and $x+3y=15$ meet where
$x = 3$, $y = 4$. The corners are $(0,0)$, $(5,0)$, $(3,4)$, $(0,5)$:

| corner | $(0,0)$ | $(5,0)$ | $(3,4)$ | $(0,5)$ |
|---|---|---|---|---|
| $Z = 4x+3y$ | $0$ | $20$ | $\mathbf{24}$ | $15$ |

The maximum is $24$ at $(3,4)$, agreeing with the simplex result.
:::
