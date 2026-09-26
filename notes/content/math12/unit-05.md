---
subject: Mathematics
grade: 12
unit: 5
title: Matrix Based System of Linear Equations
hours: 8
area: Algebra
---

A system of linear equations is a set of straight-line (or plane) equations that
must hold at the same time. Solving one by "substitute and eliminate" works for
two unknowns and becomes a mess for three. Matrices turn the whole system into
one equation, $AX = B$, and then offer three mechanical methods: **Cramer's
rule** (determinants), the **row-equivalent** or **Gauss** method (row
operations), and the **inverse matrix method** ($X = A^{-1}B$). This unit builds
all three and finishes with the question the board asks most often: when does a
system have exactly one solution, when infinitely many, and when none at all?

::: key Every system starts the same way
Write the equations with the unknowns in the same order, put the missing
coefficients in as zeros, and read off three objects: the **coefficient matrix**
$A$, the **column of unknowns** $X$ and the **column of constants** $B$. Then
$AX = B$. The determinant $|A|$ decides which method will work: if
$|A| \ne 0$ all three methods give the one answer; if $|A| = 0$ neither Cramer's
rule nor the inverse exists, and only row operations can tell you what is going
on.
:::

For the system $x + 2y + z = 8$, $\;2x + 3y - z = 5$, $\;3x - y + 2z = 7$, the
matrix form is shown below. Multiplying the first row of $A$ into the column $X$
reproduces $x + 2y + z$, which is why the single matrix equation says the same
thing as all three original equations.

```figure caption="The system $x+2y+z=8$, $2x+3y-z=5$, $3x-y+2z=7$ written as $AX = B$. Row $i$ of $A$ times the column $X$ gives the left side of equation $i$."
fig = mateq([[["$1$","$2$","$1$"],["$2$","$3$","$-1$"],["$3$","$-1$","$2$"]],
             [["$x$"],["$y$"],["$z$"]], "$=$", [["$8$"],["$5$"],["$7$"]]],
            fontsize=11, colw=0.56, scale=0.62)
```

## 5.1 Cramer's rule (up to three variables)

### Two variables

::: derivation Cramer's rule for $a_1x + b_1y = c_1$, $a_2x + b_2y = c_2$
Eliminate $y$: multiply the first equation by $b_2$, the second by $b_1$, and
subtract.

$$ a_1b_2x + b_1b_2y = c_1b_2 $$
$$ a_2b_1x + b_1b_2y = c_2b_1 $$

$$ (a_1b_2 - a_2b_1)\,x = c_1b_2 - c_2b_1 $$

Eliminating $x$ the same way gives $(a_1b_2 - a_2b_1)\,y = a_1c_2 - a_2c_1$. Each
bracket is a $2\times 2$ determinant: writing $D$ for the determinant of the
coefficients, $D_x$ for $D$ with the $x$-column replaced by the constants, and
$D_y$ likewise,

$$ x = \frac{D_x}{D}, \qquad y = \frac{D_y}{D}, \qquad D \ne 0 $$
:::

### Three variables

The same statement holds with $3\times 3$ determinants. For $AX = B$ with
$D = |A| \ne 0$,

::: key Cramer's rule
$$ x = \frac{D_x}{D}, \qquad y = \frac{D_y}{D}, \qquad z = \frac{D_z}{D} $$
where $D_x$, $D_y$, $D_z$ are $D$ with the first, second, third **column**
replaced by the column of constants. Replace a column, never a row.
:::

```figure caption="Cramer's rule for $x+y+z=4$, $x-y+z=6$, $2x+y-z=0$. The shaded column of each determinant is the one that has been replaced by the constants $(4, 6, 0)$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.0,2.9))
cw, rh = 0.46, 0.42
rows = lambda R: [[f"${v}$" for v in r] for r in R]
D  = [[1,1,1],[1,-1,1],[2,1,-1]]
Dx = [[4,1,1],[6,-1,1],[0,1,-1]]
Dy = [[1,4,1],[1,6,1],[2,0,-1]]
Dz = [[1,1,4],[1,-1,6],[2,1,0]]
items = [("$D =$", D, "$= 6$", None, 0.00, 1.75), ("$D_x =$", Dx, "$= 12$", 0, 3.55, 1.75),
         ("$D_y =$", Dy, "$= -6$", 1, 0.00, 0.10), ("$D_z =$", Dz, "$= 18$", 2, 3.55, 0.10)]
for lab, R, res, col, x0, y0 in items:
    ax.text(x0 + 0.34, y0 + 1.5*rh, lab, ha='center', va='center', fontsize=10.5, color=INK)
    if col is not None:
        ax.add_patch(Rectangle((x0 + 0.80 + col*cw, y0 - 0.04), cw, 3*rh + 0.08,
                               facecolor=ACCENT, alpha=0.16, edgecolor='none'))
    matrix(ax, rows(R), x=x0 + 0.80, y=y0, colw=cw, rowh=rh, fontsize=10.5, bracket="|")
    ax.text(x0 + 2.38, y0 + 1.5*rh, res, ha='left', va='center', fontsize=10.5, color=ACCENT)
ax.text(3.35, 3.26, '$x = 12/6 = 2$,   $y = -6/6 = -1$,   $z = 18/6 = 3$',
        ha='center', fontsize=10, color='#2e8b57')
ax.set_xlim(-0.15, 6.85); ax.set_ylim(-0.15, 3.60)
ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 5.1
**Problem.** Solve by Cramer's rule: $\;2x + 3y = 13$, $\;3x - y = 3$.

**Solution.**

$$ D = (2)(-1) - (3)(3) = -2 - 9 = -11 \ne 0 $$

so a unique solution exists. Replacing the first column by $(13, 3)$,

$$ D_x = (13)(-1) - (3)(3) = -13 - 9 = -22 $$

and replacing the second column,

$$ D_y = (2)(3) - (13)(3) = 6 - 39 = -33 $$

$$ x = \frac{D_x}{D} = \frac{-22}{-11} = 2, \qquad
y = \frac{D_y}{D} = \frac{-33}{-11} = 3 $$

**Check in the first equation:** $2(2) + 3(3) = 13$. Correct.
:::

::: example Worked example 5.2
**Problem.** Solve by Cramer's rule: $\;x + y + z = 4$, $\;x - y + z = 6$,
$\;2x + y - z = 0$.

**Solution.** Expand every determinant along its first row.

$$ D = 1(1-1) - 1(-1-2) + 1(1+2) = 0 + 3 + 3 = 6 \ne 0 $$

$$ D_x = 4(1-1) - 1(-6-0) + 1(6-0) = 0 + 6 + 6 = 12 $$
$$ D_y = 1(-6-0) - 4(-1-2) + 1(0-12) = -6 + 12 - 12 = -6 $$
$$ D_z = 1(0-6) - 1(0-12) + 4(1+2) = -6 + 12 + 12 = 18 $$

$$ x = \frac{12}{6} = 2, \qquad y = \frac{-6}{6} = -1, \qquad z = \frac{18}{6} = 3 $$

**Check in the third equation:** $2(2) + (-1) - 3 = 0$. Correct.
:::

::: example Worked example 5.3
**Problem.** In a shop in Bhaktapur, $2\ \text{kg}$ of apples and $3\ \text{kg}$
of oranges cost Rs $640$, while $3\ \text{kg}$ of apples and $2\ \text{kg}$ of
oranges cost Rs $610$. Find the price per kilogram of each fruit using Cramer's
rule.

**Solution.** Let apples cost Rs $x$ per kg and oranges Rs $y$ per kg. Then

$$ 2x + 3y = 640, \qquad 3x + 2y = 610 $$

$$ D = (2)(2) - (3)(3) = 4 - 9 = -5 $$
$$ D_x = (640)(2) - (3)(610) = 1280 - 1830 = -550 $$
$$ D_y = (2)(610) - (640)(3) = 1220 - 1920 = -700 $$

$$ x = \frac{-550}{-5} = 110, \qquad y = \frac{-700}{-5} = 140 $$

Apples cost **Rs 110 per kg** and oranges **Rs 140 per kg**. Check:
$2(110) + 3(140) = 220 + 420 = 640$. Correct.
:::

::: caution Cramer's rule dies when $D = 0$
If $D = 0$ you may not divide, and the rule says nothing at all. The system then
has either no solution or infinitely many — §5.4 shows how to tell which. Writing
"$x = 0/0$" earns no marks.
:::

## 5.2 Matrix method: row-equivalent (Gauss) method

### Elementary row operations

Two matrices are **row-equivalent** (written $\sim$) if one can be obtained from
the other by a sequence of **elementary row operations**:

| Operation | Symbol | Effect on the system |
|---|---|---|
| Swap two rows | $R_i \leftrightarrow R_j$ | write the equations in a different order |
| Multiply a row by $c \ne 0$ | $R_i \rightarrow cR_i$ | multiply an equation through by $c$ |
| Add a multiple of one row to another | $R_i \rightarrow R_i + cR_j$ | add $c\times$(one equation) to another |

Each operation is reversible and none of them changes the solution set — they are
exactly the moves you already make when eliminating by hand. So we apply them to
the **augmented matrix** $[A\,|\,B]$, the coefficient matrix with the constant
column attached, and read the answer off at the end.

**Gauss elimination** drives the coefficient block to **echelon form** (all zeros
below the leading diagonal), after which the unknowns come out one at a time by
**back substitution**, starting with the last equation.

```figure caption="Gauss elimination for $x+2y+z=8$, $2x+3y-z=5$, $3x-y+2z=7$. The dashed line separates the constants; each arrow shows the row operations used."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4,4.40))
cw, rh = 0.64, 0.44
stages = [
    ([[1,2,1,8],[2,3,-1,5],[3,-1,2,7]], ''),
    ([[1,2,1,8],[0,-1,-3,-11],[0,-7,-1,-17]],
     '$R_2 \\rightarrow R_2 - 2R_1$\n$R_3 \\rightarrow R_3 - 3R_1$'),
    ([[1,2,1,8],[0,-1,-3,-11],[0,0,20,60]], '$R_3 \\rightarrow R_3 - 7R_2$'),
]
y = 4.60
for k, (R, op) in enumerate(stages):
    rows = [[f"${v}$" for v in r] for r in R]
    w, h = matrix(ax, rows, x=0.55, y=y, colw=cw, rowh=rh, fontsize=10)
    ax.plot([0.55 + 3*cw]*2, [y - 0.03, y + h + 0.03], color=MUTED, lw=0.9, ls=(0,(2,2)))
    if k < 2:
        ax.annotate('', xy=(0.55 + w/2, y - 0.92), xytext=(0.55 + w/2, y - 0.16),
                    arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.2, mutation_scale=10))
        ax.text(0.55 + w/2 + 0.34, y - 0.54, stages[k+1][1], ha='left', va='center',
                fontsize=9.0, color=ACCENT)
    y -= (h + 1.04)
ax.text(1.70, -0.62, '$20z = 60 \\Rightarrow z = 3 \\Rightarrow y = 2 \\Rightarrow x = 1$',
        ha='center', fontsize=9.6, color='#2e8b57')
ax.set_xlim(-0.15, 6.60); ax.set_ylim(-1.05, 6.05)
ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 5.4
**Problem.** Solve by the row-equivalent (Gauss) method:

$$ x + 2y + z = 8, \qquad 2x + 3y - z = 5, \qquad 3x - y + 2z = 7 $$

**Solution.** The augmented matrix has rows $(1, 2, 1 \,|\, 8)$,
$(2, 3, -1 \,|\, 5)$, $(3, -1, 2 \,|\, 7)$.

**Clear the first column.** $R_2 \rightarrow R_2 - 2R_1$ gives
$(0, -1, -3 \,|\, -11)$; $R_3 \rightarrow R_3 - 3R_1$ gives $(0, -7, -1 \,|\, -17)$.

**Clear the second column.** $R_3 \rightarrow R_3 - 7R_2$ gives
$(0, 0, 20 \,|\, 60)$.

The system is now triangular:

$$ x + 2y + z = 8, \qquad -y - 3z = -11, \qquad 20z = 60 $$

**Back substitute.** $z = 3$. Then $-y - 9 = -11$, so $y = 2$. Then
$x + 4 + 3 = 8$, so $x = 1$.

**Solution:** $x = 1$, $y = 2$, $z = 3$. **Check in the third equation:**
$3(1) - 2 + 2(3) = 7$. Correct.
:::

::: example Worked example 5.5
**Problem.** Solve by Gauss elimination:
$\;y + z = 5$, $\;x + y - z = 0$, $\;2x - y + z = 3$.

**Solution.** The first pivot position is $0$, so start by swapping rows.

$R_1 \leftrightarrow R_2$: rows become $(1, 1, -1 \,|\, 0)$, $(0, 1, 1 \,|\, 5)$,
$(2, -1, 1 \,|\, 3)$.

$R_3 \rightarrow R_3 - 2R_1$: $(0, -3, 3 \,|\, 3)$.

$R_3 \rightarrow R_3 + 3R_2$: $(0, 0, 6 \,|\, 18)$.

So $6z = 18$, giving $z = 3$; then $y + 3 = 5$, so $y = 2$; then $x + 2 - 3 = 0$,
so $x = 1$.

**Check:** $2(1) - 2 + 3 = 3$. Correct.
:::

::: tip A zero in the pivot place is not an error
Swap it with a lower row that has a non-zero entry in that column and carry on.
Only if the **whole** column below is zero is something special happening — then
the determinant is zero and you are in §5.4.
:::

### Gauss-Jordan method

Gauss-Jordan keeps going after echelon form: make every pivot $1$ and clear the
entries **above** the pivots as well as below. The augmented matrix ends as
$[I \,|\, X]$ and the solution is simply read off — no back substitution at all.

```figure caption="Gauss-Jordan continues from the echelon form of the same system until the left block is the identity. The last column is then the solution $(1, 2, 3)$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.0,4.55))
cw, rh = 0.64, 0.44
stages = [
    ([[1,2,1,8],[0,-1,-3,-11],[0,0,20,60]], ''),
    ([[1,2,1,8],[0,1,3,11],[0,0,1,3]],
     '$R_2 \\rightarrow -R_2$\n$R_3 \\rightarrow \\frac{1}{20}R_3$'),
    ([[1,2,0,5],[0,1,0,2],[0,0,1,3]],
     '$R_1 \\rightarrow R_1 - R_3$\n$R_2 \\rightarrow R_2 - 3R_3$'),
    ([[1,0,0,1],[0,1,0,2],[0,0,1,3]], '$R_1 \\rightarrow R_1 - 2R_2$'),
]
y = 7.30
for k, (R, op) in enumerate(stages):
    rows = [[f"${v}$" for v in r] for r in R]
    w, h = matrix(ax, rows, x=0.55, y=y, colw=cw, rowh=rh, fontsize=10)
    ax.plot([0.55 + 3*cw]*2, [y - 0.03, y + h + 0.03], color=MUTED, lw=0.9, ls=(0,(2,2)))
    if k < 3:
        ax.annotate('', xy=(0.55 + w/2, y - 0.90), xytext=(0.55 + w/2, y - 0.16),
                    arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.2, mutation_scale=10))
        ax.text(0.55 + w/2 + 0.34, y - 0.53, stages[k+1][1], ha='left', va='center',
                fontsize=9.0, color=ACCENT)
    y -= (h + 1.20)
ax.text(1.75, -0.75, '$x = 1$,  $y = 2$,  $z = 3$', ha='center', fontsize=9.8, color='#2e8b57')
ax.set_xlim(-0.10, 5.75); ax.set_ylim(-1.15, 8.85)
ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 5.6
**Problem.** Solve the system of Worked example 5.4 by the Gauss-Jordan method.

**Solution.** Start from the echelon form already obtained:
$(1, 2, 1 \,|\, 8)$, $(0, -1, -3 \,|\, -11)$, $(0, 0, 20 \,|\, 60)$.

**Make the pivots $1$.** $R_2 \rightarrow -R_2$ gives $(0, 1, 3 \,|\, 11)$;
$R_3 \rightarrow \frac{1}{20}R_3$ gives $(0, 0, 1 \,|\, 3)$.

**Clear above the third pivot.** $R_1 \rightarrow R_1 - R_3$ gives
$(1, 2, 0 \,|\, 5)$; $R_2 \rightarrow R_2 - 3R_3$ gives $(0, 1, 0 \,|\, 2)$.

**Clear above the second pivot.** $R_1 \rightarrow R_1 - 2R_2$ gives
$(1, 0, 0 \,|\, 1)$.

The matrix is now $[I \,|\, X]$ with last column $(1, 2, 3)$, so $x = 1$,
$y = 2$, $z = 3$ — the same answer, read straight off.
:::

## 5.3 Matrix method: inverse matrix method

::: derivation $X = A^{-1}B$
Start from the matrix equation and multiply **on the left** by $A^{-1}$, which
exists exactly when $|A| \ne 0$:

$$ AX = B \;\Longrightarrow\; A^{-1}(AX) = A^{-1}B \;\Longrightarrow\;
(A^{-1}A)X = A^{-1}B $$

$$ IX = A^{-1}B \;\Longrightarrow\; X = A^{-1}B $$

Since $A^{-1} = \dfrac{\mathrm{adj}\,A}{|A|}$, the practical formula is

$$ X = \frac{1}{|A|}\left(\mathrm{adj}\,A\right)B $$

so the whole job is: find $|A|$, find the cofactors, transpose them to get
$\mathrm{adj}\,A$, multiply by $B$, divide by $|A|$.
:::

For a $2\times2$ matrix the inverse is the familiar swap-and-negate rule.

```figure caption="Inverse method for $2x+3y=13$, $3x-y=3$. Here $|A| = -11$ and $A^{-1} = \frac{1}{11}$ times the matrix shown, giving $X = (2, 3)$."
fig = mateq(["$X = \\frac{1}{11}$", [["$1$","$3$"],["$3$","$-2$"]],
             [["$13$"],["$3$"]], "$= \\frac{1}{11}$", [["$22$"],["$33$"]],
             "$=$", [["$2$"],["$3$"]]],
            fontsize=10.5, colw=0.54, scale=0.50)
```

::: example Worked example 5.7
**Problem.** Solve $\;2x + 3y = 13$, $\;3x - y = 3$ by the inverse matrix method.

**Solution.** Here $A$ has rows $(2, 3)$ and $(3, -1)$, and $B = (13, 3)$.

$$ |A| = (2)(-1) - (3)(3) = -11 \ne 0 $$

For a $2\times2$ matrix, swap the diagonal entries and negate the other two:
$\mathrm{adj}\,A$ has rows $(-1, -3)$ and $(-3, 2)$, so

$$ A^{-1} = \frac{1}{-11}\,\mathrm{adj}\,A = \frac{1}{11}\times
\text{(the matrix with rows } (1, 3) \text{ and } (3, -2)\text{)} $$

Then

$$ X = A^{-1}B = \frac{1}{11}\left[(1)(13) + (3)(3),\ (3)(13) + (-2)(3)\right]^{T}
= \frac{1}{11}(22,\ 33)^{T} = (2,\ 3)^{T} $$

So $x = 2$, $y = 3$, agreeing with Worked example 5.1.
:::

### Three unknowns

```figure caption="The cofactor matrix $C$ of $A$ (rows of $A$: $(1,1,1)$, $(1,0,2)$, $(3,1,1)$) and its transpose $\mathrm{adj}\,A$. Note that $5$ moves from position $(2,1)$ to position $(1,2)$."
fig = mateq(["$C =$", [["$-2$","$5$","$1$"],["$0$","$-2$","$2$"],["$2$","$-1$","$-1$"]],
             "⇒  $C^{T} = \\mathrm{adj}A =$",
             [["$-2$","$0$","$2$"],["$5$","$-2$","$-1$"],["$1$","$2$","$-1$"]]],
            fontsize=10.5, colw=0.60, scale=0.56)
```

```figure caption="The inverse method finished: $X = \frac{1}{|A|}(\mathrm{adj}A)B$ with $|A| = 4$ and $B = (6, 7, 12)$."
fig = mateq(["$X = \\frac{1}{4}$", [["$-2$","$0$","$2$"],["$5$","$-2$","$-1$"],["$1$","$2$","$-1$"]],
             [["$6$"],["$7$"],["$12$"]], "$= \\frac{1}{4}$", [["$12$"],["$4$"],["$8$"]],
             "$=$", [["$3$"],["$1$"],["$2$"]]],
            fontsize=10.5, colw=0.58, scale=0.47)
```

::: example Worked example 5.8
**Problem.** The sum of three numbers is $6$. Twice the third number added to the
first gives $7$. Three times the first, added to the sum of the second and third,
gives $12$. Find the numbers by the inverse matrix method.

**Solution.** Let the numbers be $x$, $y$, $z$:

$$ x + y + z = 6, \qquad x + 0y + 2z = 7, \qquad 3x + y + z = 12 $$

So $A$ has rows $(1,1,1)$, $(1,0,2)$, $(3,1,1)$ and $B = (6, 7, 12)$.

**Determinant.** Expanding along the first row,

$$ |A| = 1(0 - 2) - 1(1 - 6) + 1(1 - 0) = -2 + 5 + 1 = 4 \ne 0 $$

**Cofactors.** $C_{11} = -2$, $C_{12} = 5$, $C_{13} = 1$; $C_{21} = 0$,
$C_{22} = -2$, $C_{23} = 2$; $C_{31} = 2$, $C_{32} = -1$, $C_{33} = -1$.

**Adjoint.** Transpose the cofactor matrix: $\mathrm{adj}\,A$ has rows
$(-2, 0, 2)$, $(5, -2, -1)$, $(1, 2, -1)$.

**Multiply and divide.**

$$ (\mathrm{adj}\,A)B = \left(-12 + 0 + 24,\; 30 - 14 - 12,\; 6 + 14 - 12\right)^{T}
= (12,\ 4,\ 8)^{T} $$

$$ X = \frac{1}{4}(12,\ 4,\ 8)^{T} = (3,\ 1,\ 2)^{T} $$

The numbers are $3$, $1$ and $2$. **Check:** $3+1+2 = 6$; $3 + 2(2) = 7$;
$9 + 1 + 2 = 12$. Correct.
:::

::: example Worked example 5.9
**Problem.** A hotel in Pokhara charges Rs $x$ a night for a single room, Rs $y$
for a double and Rs $z$ for a deluxe room. One group paid Rs $9000$ for
$2$ singles, $1$ double and $1$ deluxe; a second paid Rs $10\,000$ for $1$
single, $2$ doubles and $1$ deluxe; a third paid Rs $12\,000$ for $1$ single,
$1$ double and $2$ deluxe. Find the three tariffs.

**Solution.** The system is

$$ 2x + y + z = 9000, \qquad x + 2y + z = 10\,000, \qquad x + y + 2z = 12\,000 $$

$$ |A| = 2(4-1) - 1(2-1) + 1(1-2) = 6 - 1 - 1 = 4 \ne 0 $$

Adding all three equations gives a shortcut worth spotting:
$4(x+y+z) = 31\,000$, so $x + y + z = 7750$. Subtracting this from each equation
in turn,

$$ x = 9000 - 7750 = 1250, \quad y = 10\,000 - 7750 = 2250,
\quad z = 12\,000 - 7750 = 4250 $$

(The same answer comes from $X = \frac14(\mathrm{adj}\,A)B$ with
$\mathrm{adj}\,A$ having rows $(3,-1,-1)$, $(-1,3,-1)$, $(-1,-1,3)$.)

Single **Rs 1250**, double **Rs 2250**, deluxe **Rs 4250**. Check:
$2(1250) + 2250 + 4250 = 9000$. Correct.
:::

::: caution Left-multiply, and check $|A|$ first
$X = A^{-1}B$, never $BA^{-1}$: matrix multiplication is not commutative, and
$BA^{-1}$ is not even defined here ($3\times1$ times $3\times3$). And always
compute $|A|$ before starting the cofactors — if $|A| = 0$ there is no inverse
and the method cannot be used at all.
:::

| Method | Needs | Best when |
|---|---|---|
| Cramer's rule | $\|A\| \ne 0$; four determinants | 2 or 3 unknowns, coefficients small |
| Inverse matrix | $\|A\| \ne 0$; adjoint | several systems share the same $A$ |
| Gauss / Gauss-Jordan | nothing | always — and the only method when $\|A\| = 0$ |

## 5.4 Consistency: unique solution, infinitely many, or none

A system is **consistent** if it has at least one solution and **inconsistent**
if it has none. Row reduce the augmented matrix and one of exactly three
pictures appears in the last row.

```figure caption="The three outcomes, read off the last row of the row-reduced augmented matrix: a pivot in every column (unique), a row of zeros (infinitely many), or $0 = $ non-zero (none)."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.1,2.7))
cw, rh = 0.46, 0.40
cases = [
    ([[1,2,1,8],[0,-1,-3,-11],[0,0,20,60]], 'unique solution', '$|A| \\ne 0$', '#2e8b57'),
    ([[1,1,1,6],[0,1,2,8],[0,0,0,0]], 'infinitely many', '$|A| = 0$', ACCENT),
    ([[1,1,1,6],[0,1,2,8],[0,0,0,1]], 'no solution', '$|A| = 0$', '#d9534f'),
]
for k, (R, title, det, col) in enumerate(cases):
    x0 = k*2.62
    rows = [[f"${v}$" for v in r] for r in R]
    w, h = matrix(ax, rows, x=x0 + 0.12, y=0.0, colw=cw, rowh=rh, fontsize=9.6)
    ax.plot([x0 + 0.12 + 3*cw - 0.05]*2, [-0.03, h + 0.03], color=MUTED, lw=0.8, ls=(0,(2,2)))
    ax.text(x0 + 0.12 + w/2, h + 0.62, title, ha='center', fontsize=9.6, color=col)
    ax.text(x0 + 0.12 + w/2, h + 0.24, det, ha='center', fontsize=9.4, color=MUTED)
    tail = ['last row: $20z = 60$', 'last row: $0 = 0$', 'last row: $0 = 1$']
    ax.text(x0 + 0.12 + w/2, -0.50, tail[k], ha='center', fontsize=9.0, color=col)
ax.set_xlim(-0.15, 7.60); ax.set_ylim(-0.95, 2.60)
ax.set_aspect('equal'); ax.axis('off')
```

::: key What the determinant tells you
- $|A| \ne 0$: **exactly one** solution, $X = A^{-1}B$. The system is consistent
  and *determinate*. Cramer and the inverse both work.
- $|A| = 0$ and every $D_x, D_y, D_z = 0$: the equations are dependent, so there
  are **infinitely many** solutions — write one unknown as a parameter $t$.
- $|A| = 0$ but at least one of $D_x, D_y, D_z \ne 0$: the equations contradict
  each other and there is **no** solution.

A homogeneous system ($B = 0$) is never inconsistent: $x = y = z = 0$ always
works. It has a non-trivial solution exactly when $|A| = 0$.
:::

::: example Worked example 5.10
**Problem.** Show that $\;x + y + z = 6$, $\;2x + 3y + 4z = 20$,
$\;x + 2y + 3z = 14$ has infinitely many solutions, and find them.

**Solution.** $|A| = 1(9-8) - 1(6-4) + 1(4-3) = 1 - 2 + 1 = 0$, so there is no
unique solution. Row reduce:

$R_2 \rightarrow R_2 - 2R_1$ gives $(0, 1, 2 \,|\, 8)$;
$R_3 \rightarrow R_3 - R_1$ gives $(0, 1, 2 \,|\, 8)$ — the same row.

$R_3 \rightarrow R_3 - R_2$ gives $(0, 0, 0 \,|\, 0)$, the statement $0 = 0$,
which is true but empty. Only two independent equations remain:

$$ x + y + z = 6, \qquad y + 2z = 8 $$

Put $z = t$ (any real number). Then $y = 8 - 2t$ and

$$ x = 6 - y - z = 6 - (8-2t) - t = t - 2 $$

So the solutions are $(x, y, z) = (t-2,\ 8-2t,\ t)$ for every real $t$ — a whole
line of them. **Check in the second equation:**
$2(t-2) + 3(8-2t) + 4t = 2t - 4 + 24 - 6t + 4t = 20$ for every $t$. Correct.
:::

::: example Worked example 5.11
**Problem.** Show that $\;x + y + z = 6$, $\;2x + 3y + 4z = 20$,
$\;x + 2y + 3z = 15$ is inconsistent.

**Solution.** The coefficient matrix is the same as in the last example, so
$|A| = 0$ again. Row reducing the augmented matrix:

$R_2 \rightarrow R_2 - 2R_1$ gives $(0, 1, 2 \,|\, 8)$;
$R_3 \rightarrow R_3 - R_1$ gives $(0, 1, 2 \,|\, 9)$.

$R_3 \rightarrow R_3 - R_2$ gives $(0, 0, 0 \,|\, 1)$, i.e. $0 = 1$, which is
false. The three planes have no common point: the system is **inconsistent** and
has no solution.

(Changing a single constant from $14$ to $15$ turned infinitely many solutions
into none — this is why the constants must be row-reduced along with the
coefficients.)
:::

::: example Worked example 5.12
**Problem.** For what values of $\lambda$ and $\mu$ does the system
$\;x + y + z = 6$, $\;x + 2y + 3z = 10$, $\;x + 2y + \lambda z = \mu$ have
(i) a unique solution, (ii) no solution, (iii) infinitely many solutions?

**Solution.** Expanding along the first row,

$$ |A| = 1(2\lambda - 6) - 1(\lambda - 3) + 1(2 - 2) = \lambda - 3 $$

**(i)** If $\lambda \ne 3$ then $|A| \ne 0$ and there is a unique solution for
every $\mu$.

If $\lambda = 3$, row reduce: $R_2 \rightarrow R_2 - R_1$ gives
$(0, 1, 2 \,|\, 4)$ and $R_3 \rightarrow R_3 - R_1$ gives
$(0, 1, 2 \,|\, \mu - 6)$. Then $R_3 \rightarrow R_3 - R_2$ gives
$(0, 0, 0 \,|\, \mu - 10)$.

**(ii)** If $\lambda = 3$ and $\mu \ne 10$ the last row reads
$0 = \mu - 10 \ne 0$: **no solution**.

**(iii)** If $\lambda = 3$ and $\mu = 10$ the last row is $0 = 0$: **infinitely
many solutions**, namely $z = t$, $y = 4 - 2t$, $x = 6 - y - z = 2 + t$.

**Check** (iii) in the second equation: $(2+t) + 2(4-2t) + 3t = 10$ for all $t$.
Correct.
:::

::: example Worked example 5.13
**Problem.** Show that $\;x + y + z = 0$, $\;2x - y + 3z = 0$,
$\;4x + y + 5z = 0$ has a non-trivial solution and find it.

**Solution.** The system is homogeneous, so $x = y = z = 0$ is always a solution.
A non-trivial one exists only if

$$ |A| = 1(-5 - 3) - 1(10 - 12) + 1(2 + 4) = -8 + 2 + 6 = 0 $$

which it is. Row reduce: $R_2 \rightarrow R_2 - 2R_1$ gives $(0, -3, 1 \,|\, 0)$
and $R_3 \rightarrow R_3 - 4R_1$ gives $(0, -3, 1 \,|\, 0)$, the same row, so
$R_3 \rightarrow R_3 - R_2$ gives all zeros. We are left with

$$ x + y + z = 0, \qquad -3y + z = 0 $$

Put $z = 3t$: then $y = t$ and $x = -y - z = -4t$. The solutions are
$(-4t,\ t,\ 3t)$; taking $t = 1$ gives $(-4, 1, 3)$.

**Check in the third equation:** $4(-4) + 1 + 5(3) = -16 + 16 = 0$. Correct.
:::

## Chapter summary

- Every linear system is $AX = B$ with $A$ the coefficient matrix, $X$ the column
  of unknowns and $B$ the column of constants.
- **Cramer:** $x = D_x/D$, $y = D_y/D$, $z = D_z/D$, where $D = |A|$ and each
  $D_x$ replaces the matching **column** of $D$ by $B$. Requires $D \ne 0$.
- **Row-equivalent (Gauss):** apply elementary row operations
  ($R_i \leftrightarrow R_j$, $R_i \rightarrow cR_i$, $R_i \rightarrow R_i + cR_j$)
  to $[A\,|\,B]$ until the coefficient block is upper triangular, then back
  substitute. Row operations never change the solution set.
- **Gauss-Jordan:** carry on until $[I\,|\,X]$; the solution is the last column.
- **Inverse method:** $X = A^{-1}B = \dfrac{1}{|A|}(\mathrm{adj}\,A)B$, valid only
  when $|A| \ne 0$. Multiply on the left.
- **Consistency:** $|A| \ne 0$ → unique; $|A| = 0$ with a zero row in the reduced
  augmented matrix → infinitely many (use a parameter $t$); $|A| = 0$ with a row
  $0 = k \ne 0$ → no solution.
- A homogeneous system has a non-trivial solution if and only if $|A| = 0$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The system $AX = B$ has a unique solution if <span class="marks">[1]</span>
   (a) $|A| = 0$ (b) $|A| \ne 0$ (c) $B = 0$ (d) $A$ is symmetric
2. In Cramer's rule, $D_y$ is obtained from $D$ by replacing <span class="marks">[1]</span>
   (a) row 2 by $B$ (b) column 2 by $B$ (c) row 1 by $B$ (d) column 1 by $B$
3. Which of these is **not** an elementary row operation? <span class="marks">[1]</span>
   (a) $R_1 \leftrightarrow R_2$ (b) $R_2 \rightarrow 3R_2$ (c) $R_2 \rightarrow 0 \cdot R_2$ (d) $R_2 \rightarrow R_2 - 4R_1$
4. If the last row of a row-reduced augmented matrix is $(0\ 0\ 0 \,|\, 5)$, the system has <span class="marks">[1]</span>
   (a) a unique solution (b) two solutions (c) infinitely many solutions (d) no solution
5. For $AX = B$ with $|A| \ne 0$, the solution is <span class="marks">[1]</span>
   (a) $X = BA^{-1}$ (b) $X = A^{-1}B$ (c) $X = AB^{-1}$ (d) $X = B^{-1}A$
6. A homogeneous system $AX = O$ in three unknowns has a non-trivial solution if <span class="marks">[1]</span>
   (a) $|A| \ne 0$ (b) $|A| = 0$ (c) $|A| = 1$ (d) never

::: note Answers to Group A
**1.** (b) — only then does $A^{-1}$ exist, and then $X = A^{-1}B$ is the one
solution.

**2.** (b) — always a column, and the column belonging to that unknown.

**3.** (c) — multiplying a row by $0$ destroys the equation; the multiplier must
be non-zero.

**4.** (d) — that row says $0 = 5$, which is impossible, so the system is
inconsistent.

**5.** (b) — multiply $AX = B$ on the **left** by $A^{-1}$.

**6.** (b) — if $|A| \ne 0$ the only solution is $X = A^{-1}O = O$, the trivial
one.
:::

**Group B — Short answer (5 marks each)**

1. Solve by Cramer's rule: $\;4x + 3y = 18$, $\;3x - 2y = 5$. <span class="marks">[5]</span>
2. Solve by Cramer's rule: $\;x + y + z = 6$, $\;x + 2y + 3z = 14$,
   $\;x + 4y + 9z = 36$. <span class="marks">[5]</span>
3. Solve by the row-equivalent (Gauss) method: $\;x + y + z = 2$,
   $\;2x - y + 3z = 0$, $\;3x + 2y - z = 9$. <span class="marks">[5]</span>
4. Solve by the inverse matrix method: $\;2x + y = 8$, $\;x + 3y = 9$. <span class="marks">[5]</span>
5. Examine the consistency of $\;x + 2y = 4$, $\;2x + 4y = 8$, $\;3x + 6y = 12$
   and solve it if it is consistent. <span class="marks">[5]</span>
6. Find the value of $k$ for which $\;x + y + z = 1$, $\;x + 2y + 3z = 4$,
   $\;x + 4y + kz = 6$ fails to have a unique solution, and say what happens for
   that value. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** $D = (4)(-2) - (3)(3) = -8 - 9 = -17$.

$$ D_x = (18)(-2) - (3)(5) = -36 - 15 = -51, \qquad
D_y = (4)(5) - (18)(3) = 20 - 54 = -34 $$

$$ x = \frac{-51}{-17} = 3, \qquad y = \frac{-34}{-17} = 2 $$

Check: $4(3) + 3(2) = 18$. Correct.

**2.** Expanding along the first row each time,

$$ D = 1(18-12) - 1(9-3) + 1(4-2) = 6 - 6 + 2 = 2 $$
$$ D_x = 6(18-12) - 1(126-108) + 1(56-72) = 36 - 18 - 16 = 2 $$
$$ D_y = 1(126-108) - 6(9-3) + 1(36-14) = 18 - 36 + 22 = 4 $$
$$ D_z = 1(72-56) - 1(36-14) + 6(4-2) = 16 - 22 + 12 = 6 $$

$$ x = \frac{2}{2} = 1, \qquad y = \frac{4}{2} = 2, \qquad z = \frac{6}{2} = 3 $$

Check in the third equation: $1 + 8 + 27 = 36$. Correct.

**3.** Augmented rows $(1,1,1\,|\,2)$, $(2,-1,3\,|\,0)$, $(3,2,-1\,|\,9)$.

$R_2 \rightarrow R_2 - 2R_1$: $(0,-3,1\,|\,-4)$.
$R_3 \rightarrow R_3 - 3R_1$: $(0,-1,-4\,|\,3)$.
$R_3 \rightarrow 3R_3 - R_2$: $(0,0,-13\,|\,13)$.

So $z = -1$; then $-3y + (-1) = -4$ gives $y = 1$; then $x + 1 - 1 = 2$ gives
$x = 2$.

**Solution** $x = 2$, $y = 1$, $z = -1$. Check: $3(2) + 2(1) - (-1) = 9$. Correct.

**4.** $A$ has rows $(2,1)$, $(1,3)$ and $B = (8, 9)$. $|A| = 6 - 1 = 5 \ne 0$,
and $\mathrm{adj}\,A$ has rows $(3, -1)$, $(-1, 2)$, so

$$ X = \frac{1}{5}\left[(3)(8) + (-1)(9),\ (-1)(8) + (2)(9)\right]^{T}
= \frac{1}{5}(15,\ 10)^{T} = (3,\ 2)^{T} $$

So $x = 3$, $y = 2$. Check: $2(3) + 2 = 8$ and $3 + 3(2) = 9$. Correct.

**5.** The second and third equations are just $2\times$ and $3\times$ the first,
so row reduction ($R_2 \rightarrow R_2 - 2R_1$, $R_3 \rightarrow R_3 - 3R_1$)
gives two rows of zeros. The system is **consistent** with only one independent
equation, so it has infinitely many solutions: put $y = t$, then $x = 4 - 2t$,
i.e. $(4-2t,\ t)$ for every real $t$.

**6.** $D = 1(2k - 12) - 1(k - 3) + 1(4 - 2) = k - 7$, so the unique solution
fails exactly when $k = 7$.

With $k = 7$: $R_2 \rightarrow R_2 - R_1$ gives $(0,1,2\,|\,3)$ and
$R_3 \rightarrow R_3 - R_1$ gives $(0,3,6\,|\,5)$. Then
$R_3 \rightarrow R_3 - 3R_2$ gives $(0,0,0\,|\,-4)$, i.e. $0 = -4$. So for
$k = 7$ the system is **inconsistent** and has no solution. (Had the right-hand
side of the third equation been $10$ instead of $6$, the last row would read
$0 = 0$ and there would be infinitely many solutions.)
:::

**Group C — Long answer (8 marks each)**

1. (a) Derive Cramer's rule for the system $a_1x + b_1y = c_1$,
   $a_2x + b_2y = c_2$. <span class="marks">[4]</span>
   (b) Hence solve $\;x + y + z = 4$, $\;2x + y - z = 3$, $\;x - y + 2z = 8$ by
   Cramer's rule. <span class="marks">[4]</span>
2. (a) Show that $AX = B$ has the solution $X = A^{-1}B$ when $|A| \ne 0$, and
   solve $\;x + 2y - z = 2$, $\;2x - y + z = 3$, $\;x + y + z = 6$ by the
   inverse matrix method. <span class="marks">[5]</span>
   (b) Solve the same system by Gauss-Jordan and compare the labour. <span class="marks">[3]</span>
3. (a) Explain, with the determinant in each case, when a system of three linear
   equations in three unknowns has a unique solution, infinitely many solutions,
   or no solution. <span class="marks">[4]</span>
   (b) Discuss the system $\;x + y + z = 6$, $\;x + 2y + 3z = 10$,
   $\;x + 2y + \lambda z = \mu$ for all values of $\lambda$ and $\mu$. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** (a) Multiply the first equation by $b_2$ and the second by $b_1$ and
subtract:

$$ (a_1b_2 - a_2b_1)x = c_1b_2 - c_2b_1 $$

Similarly, multiplying by $a_2$ and $a_1$ and subtracting,

$$ (a_1b_2 - a_2b_1)y = a_1c_2 - a_2c_1 $$

Writing $D = a_1b_2 - a_2b_1$, $D_x = c_1b_2 - c_2b_1$ and
$D_y = a_1c_2 - a_2c_1$ as determinants, $x = D_x/D$ and $y = D_y/D$ provided
$D \ne 0$.

(b) Expanding along the first row,

$$ D = 1(2-1) - 1(4+1) + 1(-2-1) = 1 - 5 - 3 = -7 $$
$$ D_x = 4(2-1) - 1(6+8) + 1(-3-8) = 4 - 14 - 11 = -21 $$
$$ D_y = 1(6+8) - 4(4+1) + 1(16-3) = 14 - 20 + 13 = 7 $$
$$ D_z = 1(8+3) - 1(16-3) + 4(-2-1) = 11 - 13 - 12 = -14 $$

$$ x = \frac{-21}{-7} = 3, \qquad y = \frac{7}{-7} = -1, \qquad
z = \frac{-14}{-7} = 2 $$

Check in the third equation: $3 - (-1) + 2(2) = 8$. Correct.

**2.** (a) If $|A| \ne 0$ then $A^{-1}$ exists; multiplying $AX = B$ on the left
by it gives $(A^{-1}A)X = A^{-1}B$, i.e. $IX = X = A^{-1}B$.

Here $A$ has rows $(1,2,-1)$, $(2,-1,1)$, $(1,1,1)$ and $B = (2, 3, 6)$.

$$ |A| = 1(-1-1) - 2(2-1) + (-1)(2+1) = -2 - 2 - 3 = -7 \ne 0 $$

Cofactors: $C_{11} = -2$, $C_{12} = -1$, $C_{13} = 3$; $C_{21} = -3$,
$C_{22} = 2$, $C_{23} = 1$; $C_{31} = 1$, $C_{32} = -3$, $C_{33} = -5$.
Transposing, $\mathrm{adj}\,A$ has rows $(-2, -3, 1)$, $(-1, 2, -3)$,
$(3, 1, -5)$. Then

$$ (\mathrm{adj}\,A)B = (-4 - 9 + 6,\; -2 + 6 - 18,\; 6 + 3 - 30)^{T}
= (-7,\ -14,\ -21)^{T} $$

$$ X = \frac{1}{-7}(-7,\ -14,\ -21)^{T} = (1,\ 2,\ 3)^{T} $$

So $x = 1$, $y = 2$, $z = 3$. Check: $1 + 4 - 3 = 2$. Correct.

(b) Augmented rows $(1,2,-1\,|\,2)$, $(2,-1,1\,|\,3)$, $(1,1,1\,|\,6)$.

$R_2 \rightarrow R_2 - 2R_1$: $(0,-5,3\,|\,-1)$.
$R_3 \rightarrow R_3 - R_1$: $(0,-1,2\,|\,4)$.
$R_2 \leftrightarrow R_3$, then $R_2 \rightarrow -R_2$: $(0,1,-2\,|\,-4)$.
$R_3 \rightarrow R_3 + 5R_2$: $(0,0,-7\,|\,-21)$, so
$R_3 \rightarrow -\frac{1}{7}R_3$ gives $(0,0,1\,|\,3)$.
$R_2 \rightarrow R_2 + 2R_3$: $(0,1,0\,|\,2)$;
$R_1 \rightarrow R_1 + R_3$: $(1,2,0\,|\,5)$;
$R_1 \rightarrow R_1 - 2R_2$: $(1,0,0\,|\,1)$.

The matrix is $[I\,|\,(1,2,3)]$, the same answer. Gauss-Jordan needed no
cofactors and no division until the very end, so for a single system it is much
less work than the inverse method; the inverse only pays off when several systems
share the same $A$.

**3.** (a) Let $D = |A|$.

- $D \ne 0$: the inverse exists, $X = A^{-1}B$ is the only solution — **unique**
  (the three planes meet in one point).
- $D = 0$ and the row-reduced augmented matrix has a row of zeros: the equations
  are dependent, giving **infinitely many** solutions (the planes meet in a line,
  or coincide). Equivalently $D_x = D_y = D_z = 0$.
- $D = 0$ but a row reduces to $0 = k$ with $k \ne 0$: the equations contradict
  each other, so there is **no solution** (at least one of $D_x$, $D_y$, $D_z$ is
  non-zero).

(b) $D = 1(2\lambda - 6) - 1(\lambda - 3) + 1(2-2) = \lambda - 3$.

*If $\lambda \ne 3$:* $D \ne 0$, so there is a unique solution for every $\mu$.

*If $\lambda = 3$:* row reducing gives $(0,1,2\,|\,4)$ from $R_2 - R_1$ and
$(0,1,2\,|\,\mu-6)$ from $R_3 - R_1$; subtracting leaves
$(0,0,0\,|\,\mu-10)$.

- $\lambda = 3$, $\mu \ne 10$: last row is $0 = \mu - 10 \ne 0$ — **no solution**.
- $\lambda = 3$, $\mu = 10$: last row is $0 = 0$ — **infinitely many solutions**,
  $z = t$, $y = 4 - 2t$, $x = 2 + t$ for every real $t$.
:::
