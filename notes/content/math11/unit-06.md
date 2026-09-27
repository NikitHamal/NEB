---
subject: Mathematics
grade: 11
unit: 6
title: Matrices and Determinants
hours: 6
area: Algebra
---

A **matrix** is a rectangular array of numbers, and a **determinant** is a single
number that a *square* matrix carries with it. Together they turn a system of
linear equations into a single equation $AX = B$ that can be solved by a
recipe — no guessing which variable to eliminate first. This unit builds that
recipe: transpose, minors and cofactors, the adjoint, the inverse, and the
properties of determinants that make large ones quick to evaluate.

::: key The order of operations in every inverse question
$$ \text{minors} \rightarrow \text{cofactors} \rightarrow \text{cofactor matrix}
\rightarrow \text{transpose it} = \mathrm{adj}\,A \rightarrow A^{-1} = \frac{\mathrm{adj}\,A}{|A|} $$
Skipping the transpose is the single commonest reason students lose marks in this
unit. And no inverse exists at all unless $|A| \ne 0$ — always compute $|A|$ first.
:::

## 6.1 Transpose of a matrix and its properties

### The operations you already have

A matrix with $m$ rows and $n$ columns has **order** $m \times n$. The entry in
row $i$ and column $j$ is $a_{ij}$, so a $3\times3$ matrix has entries
$a_{11}, a_{12}, a_{13}$ in its first row, and so on down to $a_{33}$.

- **Equality.** $A = B$ only if they have the same order *and* $a_{ij} = b_{ij}$
  for every $i$ and $j$.
- **Addition** and **subtraction** work entry by entry, and are defined only for
  matrices of the *same* order.
- **Scalar multiplication**: $kA$ multiplies *every* entry by $k$.
- **Multiplication**: $AB$ exists only when the number of columns of $A$ equals
  the number of rows of $B$. If $A$ is $m\times n$ and $B$ is $n\times p$, then
  $AB$ is $m \times p$, and

$$ (AB)_{ij} = a_{i1}b_{1j} + a_{i2}b_{2j} + \cdots + a_{in}b_{nj} $$

That is: **row $i$ of $A$ against column $j$ of $B$**, multiplying in pairs and
adding.

```figure caption="Matrix multiplication. Row 1 of $A$ is paired term by term with column 1 of $B$ to give the $(1,1)$ entry of $AB$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.0,2.6))
cw, rh = 0.50, 0.45
A = [["$1$","$2$","$3$"], ["$4$","$5$","$6$"]]
B = [["$1$","$0$"], ["$2$","$1$"], ["$1$","$1$"]]
P = [["$8$","$5$"], ["$20$","$11$"]]
matrix(ax, A, x=0.35, y=1.15, colw=cw, rowh=rh, fontsize=10)
matrix(ax, B, x=2.60, y=0.925, colw=cw, rowh=rh, fontsize=10)
matrix(ax, P, x=4.40, y=1.15, colw=cw, rowh=rh, fontsize=10)
ax.text(2.20, 1.60, '×', ha='center', va='center', fontsize=11, color=INK)
ax.text(4.02, 1.60, '=', ha='center', va='center', fontsize=11, color=INK)
ax.add_patch(Rectangle((0.33, 1.60), 3*cw+0.04, rh, facecolor=ACCENT, alpha=0.16,
                       edgecolor=ACCENT, lw=0.9))
ax.add_patch(Rectangle((2.58, 0.905), cw+0.04, 3*rh, facecolor='#d9534f', alpha=0.16,
                       edgecolor='#d9534f', lw=0.9))
ax.add_patch(Rectangle((4.38, 1.60), cw+0.04, rh, facecolor='#2e8b57', alpha=0.18,
                       edgecolor='#2e8b57', lw=0.9))
ax.annotate('', xy=(4.40, 1.62), xytext=(3.55, 0.60),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.0, mutation_scale=9))
ax.text(2.55, 0.42, '$1(1) + 2(2) + 3(1) = 8$', ha='center', va='center',
        fontsize=10, color=INK)
ax.text(0.95, 2.62, '$A$  (2×3)', ha='center', fontsize=9.2, color=MUTED)
ax.text(3.10, 2.62, '$B$  (3×2)', ha='center', fontsize=9.2, color=MUTED)
ax.text(4.92, 2.62, '$AB$  (2×2)', ha='center', fontsize=9.2, color=MUTED)
ax.set_xlim(-0.2, 5.7); ax.set_ylim(0.05, 3.12)
ax.set_aspect('equal'); ax.axis('off')
```

::: caution $AB$ and $BA$ are different matrices
Matrix multiplication is **not commutative**. Usually $AB \ne BA$; often one of
them does not even exist. Also, $AB = O$ does **not** force $A = O$ or $B = O$.
:::

### The transpose

::: definition Transpose
The **transpose** of an $m\times n$ matrix $A$, written $A^{T}$ (or $A'$), is the
$n\times m$ matrix obtained by interchanging the rows and columns: the entry in
row $i$, column $j$ of $A^{T}$ is $a_{ji}$.
:::

```figure caption="Transposing turns rows into columns. The first row $1,2,3$ of $A$ becomes the first column of $A^{T}$."
fig = mateq(["$A =$", [["$1$","$2$","$3$"],["$4$","$5$","$6$"]],
             "$A^{T} =$", [["$1$","$4$"],["$2$","$5$"],["$3$","$6$"]]],
            fontsize=11, colw=0.52, scale=0.66)
```

The properties below are the examinable ones. All are proved by comparing the
$(i,j)$ entry of the two sides.

| Property | Statement |
|---|---|
| Involution | $\left(A^{T}\right)^{T} = A$ |
| Sum | $(A+B)^{T} = A^{T} + B^{T}$ |
| Scalar | $(kA)^{T} = kA^{T}$ |
| **Reversal law** | $(AB)^{T} = B^{T}A^{T}$ |
| Determinant | $|A^{T}| = |A|$ |

::: caution The reversal law
$(AB)^{T} = B^{T}A^{T}$, **not** $A^{T}B^{T}$. The order flips. You can see why
from the orders alone: if $A$ is $2\times3$ and $B$ is $3\times2$ then $A^{T}B^{T}$
is $(3\times2)(2\times3)$ — a different size from $(AB)^{T}$, which is $2\times2$.
:::

A square matrix is **symmetric** if $A^{T} = A$ (so $a_{ij} = a_{ji}$) and
**skew-symmetric** if $A^{T} = -A$ (so $a_{ij} = -a_{ji}$, which forces every
diagonal entry to be zero). Every square matrix splits into one of each:

$$ A = \tfrac{1}{2}\left(A + A^{T}\right) + \tfrac{1}{2}\left(A - A^{T}\right) $$

The first bracket is symmetric (transposing it gives itself) and the second is
skew-symmetric (transposing it changes every sign).

```figure caption="Every square matrix is the sum of a symmetric and a skew-symmetric matrix: $A = \frac12(A+A^{T}) + \frac12(A-A^{T})$."
fig = mateq(["$A =$", [["$2$","$3$"],["$7$","$4$"]], "$=$",
             [["$2$","$5$"],["$5$","$4$"]], "$+$",
             [["$0$","$-2$"],["$2$","$0$"]]],
            fontsize=10.5, colw=0.52, scale=0.62)
```

::: example Worked example 6.1
**Problem.** With $A$ the $2\times3$ matrix whose rows are $(1,2,3)$ and $(4,5,6)$,
and $B$ the $3\times2$ matrix whose rows are $(1,0)$, $(2,1)$ and $(1,1)$, verify
that $(AB)^{T} = B^{T}A^{T}$.

**Solution.** First $AB$, row against column:

$$ (AB)_{11} = 1(1)+2(2)+3(1) = 8, \qquad (AB)_{12} = 1(0)+2(1)+3(1) = 5 $$
$$ (AB)_{21} = 4(1)+5(2)+6(1) = 20, \qquad (AB)_{22} = 4(0)+5(1)+6(1) = 11 $$

So $AB$ has rows $(8,5)$ and $(20,11)$, and therefore $(AB)^{T}$ has rows
$(8,20)$ and $(5,11)$.

Now the other side. $B^{T}$ is $2\times3$ with rows $(1,2,1)$ and $(0,1,1)$;
$A^{T}$ is $3\times2$ with rows $(1,4)$, $(2,5)$, $(3,6)$. Multiplying,

$$ (B^{T}A^{T})_{11} = 1(1)+2(2)+1(3) = 8, \qquad (B^{T}A^{T})_{12} = 1(4)+2(5)+1(6) = 20 $$
$$ (B^{T}A^{T})_{21} = 0(1)+1(2)+1(3) = 5, \qquad (B^{T}A^{T})_{22} = 0(4)+1(5)+1(6) = 11 $$

The rows are $(8,20)$ and $(5,11)$ — identical to $(AB)^{T}$. Verified.
:::

::: example Worked example 6.2
**Problem.** Express the matrix $A$ with rows $(2,3)$ and $(7,4)$ as the sum of a
symmetric and a skew-symmetric matrix.

**Solution.** $A^{T}$ has rows $(2,7)$ and $(3,4)$.

$$ A + A^{T} \text{ has rows } (4,10),\ (10,8) \;\Longrightarrow\;
P = \tfrac12\left(A+A^{T}\right) \text{ has rows } (2,5),\ (5,4) $$

$$ A - A^{T} \text{ has rows } (0,-4),\ (4,0) \;\Longrightarrow\;
Q = \tfrac12\left(A-A^{T}\right) \text{ has rows } (0,-2),\ (2,0) $$

$P^{T} = P$, so $P$ is symmetric; $Q^{T} = -Q$, so $Q$ is skew-symmetric. Adding,
$P+Q$ has rows $(2,3)$ and $(7,4)$, which is $A$. (See the figure above.)
:::

## 6.2 Minors and cofactors

Every square matrix carries a single number called its **determinant**, written
$|A|$ or $\det A$. For a second-order (that is, $2\times2$) matrix it is

$$ |A| = a_{11}a_{22} - a_{12}a_{21} $$

— the product along the leading diagonal minus the product along the other
diagonal. Third-order determinants are reduced to second-order ones using minors.

::: definition Minor and cofactor
The **minor** $M_{ij}$ of the entry $a_{ij}$ is the determinant of the smaller
matrix left after **deleting row $i$ and column $j$**.

The **cofactor** is the minor with a sign attached:

$$ C_{ij} = (-1)^{\,i+j} M_{ij} $$
:::

```figure caption="The minor $M_{23}$: delete row 2 and column 3, then take the determinant of what is left. The sign board on the right gives $(-1)^{i+j}$ at a glance."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.7))
cw, rh = 0.62, 0.50
A = [["$1$","$2$","$3$"], ["$0$","$1$","$4$"], ["$5$","$6$","$0$"]]
matrix(ax, A, x=0.30, y=1.05, colw=cw, rowh=rh, fontsize=10.5)
# strike out row 2 and column 3
ax.plot([0.22, 0.30+3*cw+0.08], [1.05+1.5-1.5*rh]*2, color='#d9534f', lw=1.3)
ax.plot([0.30+2.5*cw]*2, [0.97, 1.05+1.5+0.08], color='#d9534f', lw=1.3)
ax.annotate('', xy=(3.05, 1.80), xytext=(2.35, 1.80),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.1, mutation_scale=10))
matrix(ax, [["$1$","$2$"],["$5$","$6$"]], x=3.25, y=1.30, colw=cw, rowh=rh,
       fontsize=10.5, bracket="|")
ax.text(4.95, 1.80, '$= -4$', ha='left', va='center', fontsize=10.5, color=INK)
ax.text(1.20, 0.52, 'delete $R_2$ and $C_3$', ha='center', va='top', fontsize=9.4,
        color='#d9534f')
ax.text(4.20, 0.62, '$M_{23} = -4$\n$C_{23} = (-1)^{5}M_{23} = 4$', ha='center',
        va='top', fontsize=9.4, color='#2e8b57', linespacing=1.6)
matrix(ax, [["$+$","$-$","$+$"],["$-$","$+$","$-$"],["$+$","$-$","$+$"]],
       x=6.55, y=1.05, colw=0.42, rowh=rh, fontsize=10.5, bracket="")
ax.text(7.18, 0.55, 'sign board', ha='center', fontsize=9.2, color=MUTED)
ax.set_xlim(-0.1, 8.3); ax.set_ylim(-0.42, 3.02)
ax.set_aspect('equal'); ax.axis('off')
```

With cofactors, the determinant can be expanded along **any** row or **any**
column:

$$ |A| = a_{i1}C_{i1} + a_{i2}C_{i2} + a_{i3}C_{i3} \quad\text{(along row } i)$$
$$ |A| = a_{1j}C_{1j} + a_{2j}C_{2j} + a_{3j}C_{3j} \quad\text{(along column } j)$$

Every choice gives the same answer, which is why you should always expand along
the row or column containing the **most zeros**.

::: tip One sign rule, memorised as a board
The signs alternate like a chessboard starting with $+$ at the top-left. For a
$3\times3$ you never need $(-1)^{i+j}$ arithmetic — just read the board.
:::

::: example Worked example 6.3
**Problem.** For the matrix $A$ with rows $(1,2,3)$, $(0,1,4)$, $(5,6,0)$, find all
nine minors and cofactors, and hence $|A|$.

**Solution.** Delete the relevant row and column each time.

| | $j=1$ | $j=2$ | $j=3$ |
|---|---|---|---|
| $i=1$: minor | $1(0)-4(6) = -24$ | $0(0)-4(5) = -20$ | $0(6)-1(5) = -5$ |
| $i=1$: cofactor | $-24$ | $+20$ | $-5$ |
| $i=2$: minor | $2(0)-3(6) = -18$ | $1(0)-3(5) = -15$ | $1(6)-2(5) = -4$ |
| $i=2$: cofactor | $+18$ | $-15$ | $+4$ |
| $i=3$: minor | $2(4)-3(1) = 5$ | $1(4)-3(0) = 4$ | $1(1)-2(0) = 1$ |
| $i=3$: cofactor | $+5$ | $-4$ | $+1$ |

Expanding along the **first row**:

$$ |A| = a_{11}C_{11} + a_{12}C_{12} + a_{13}C_{13} = 1(-24) + 2(20) + 3(-5) $$
$$ = -24 + 40 - 15 = 1 $$

**Check by expanding along the second row** (which contains a zero):

$$ |A| = 0(18) + 1(-15) + 4(4) = -15 + 16 = 1 $$

Same answer, as it must be. So $|A| = 1$.
:::

::: example Worked example 6.4
**Problem.** Evaluate the determinant of the matrix with rows $(2,3,1)$, $(4,7,3)$
and $(6,8,5)$.

**Solution.** Expand along the first row.

$$ |A| = 2\left(7(5) - 3(8)\right) - 3\left(4(5) - 3(6)\right) + 1\left(4(8) - 7(6)\right) $$
$$ = 2(35-24) - 3(20-18) + (32-42) = 2(11) - 3(2) - 10 $$
$$ = 22 - 6 - 10 = 6 $$
:::

## 6.3 Adjoint and inverse of a matrix

::: definition Adjoint
The **adjoint** of a square matrix $A$, written $\mathrm{adj}\,A$, is the
**transpose of the matrix of cofactors**:

$$ \left(\mathrm{adj}\,A\right)_{ij} = C_{ji} $$
:::

::: derivation Why $A\,(\mathrm{adj}\,A) = |A|\,I$
Take the $(i,j)$ entry of the product $A\,(\mathrm{adj}\,A)$. By the definition of
the adjoint it equals

$$ a_{i1}C_{j1} + a_{i2}C_{j2} + a_{i3}C_{j3} $$

If $i = j$ this is exactly the cofactor expansion of $|A|$ along row $i$, so every
**diagonal** entry is $|A|$.

If $i \ne j$ we are multiplying the entries of row $i$ by the cofactors of a
*different* row $j$. That sum is the cofactor expansion of a determinant whose
row $j$ has been replaced by a copy of row $i$ — a determinant with two identical
rows, which is zero. So every **off-diagonal** entry is $0$.

A matrix with $|A|$ down the diagonal and zeros elsewhere is $|A|\,I$. Hence

$$ A\,(\mathrm{adj}\,A) = (\mathrm{adj}\,A)\,A = |A|\,I $$
:::

Divide by $|A|$ — legal only when $|A| \ne 0$ — and you have the inverse.

::: key Inverse of a matrix
$$ A^{-1} = \frac{1}{|A|}\,\mathrm{adj}\,A, \qquad\text{provided } |A| \ne 0 $$
A square matrix with $|A| \ne 0$ is called **non-singular** and has exactly one
inverse; if $|A| = 0$ it is **singular** and has no inverse at all. Also
$AA^{-1} = A^{-1}A = I$, $(A^{-1})^{-1} = A$ and $(AB)^{-1} = B^{-1}A^{-1}$.
:::

For a $2\times2$ matrix the recipe collapses to something worth memorising.

```figure caption="The $2\times2$ shortcut: swap the diagonal entries, negate the other two, divide by the determinant."
fig = mateq(["$A =$", [["$a$","$b$"],["$c$","$d$"]], "⇒",
             "$A^{-1} = \\frac{1}{ad-bc}$", [["$d$","$-b$"],["$-c$","$a$"]]],
            fontsize=11, colw=0.52, scale=0.62)
```

For a $3\times3$ matrix you must do the full job. Using the cofactors already
found in Worked example 6.3:

```figure caption="Cofactor matrix $C$ of $A$, and $\mathrm{adj}\,A = C^{T}$. Note how the transpose moves $20$ from position $(1,2)$ to position $(2,1)$."
fig = mateq(["$C =$", [["$-24$","$20$","$-5$"],["$18$","$-15$","$4$"],["$5$","$-4$","$1$"]],
             "⇒  $C^{T} =$",
             [["$-24$","$18$","$5$"],["$20$","$-15$","$-4$"],["$-5$","$4$","$1$"]]],
            fontsize=10.5, colw=0.64, scale=0.56)
```

```figure caption="Because $|A| = 1$ here, $A^{-1} = \mathrm{adj}\,A$ exactly. Multiplying out confirms $AA^{-1} = I$."
fig = mateq(["$A A^{-1} =$", [["$1$","$2$","$3$"],["$0$","$1$","$4$"],["$5$","$6$","$0$"]],
             [["$-24$","$18$","$5$"],["$20$","$-15$","$-4$"],["$-5$","$4$","$1$"]],
             "$=$", [["$1$","$0$","$0$"],["$0$","$1$","$0$"],["$0$","$0$","$1$"]]],
            fontsize=10.5, colw=0.62, scale=0.50)
```

### Solving linear equations with the inverse

Three equations in three unknowns,

$$ a_1x + b_1y + c_1z = d_1,\quad a_2x + b_2y + c_2z = d_2,\quad a_3x + b_3y + c_3z = d_3 $$

can be written as the single matrix equation $AX = B$, where $A$ is the
$3\times3$ matrix of coefficients, $X$ is the column of unknowns and $B$ is the
column of constants. If $|A| \ne 0$, multiply on the **left** by $A^{-1}$:

$$ A^{-1}(AX) = A^{-1}B \;\Longrightarrow\; IX = A^{-1}B \;\Longrightarrow\;
X = A^{-1}B $$

```figure caption="A $2\times2$ system written as $AX = B$ and solved by $X = A^{-1}B$. Here $|A| = 1$."
fig = mateq(["$X = A^{-1}B =$", [["$2$","$-3$"],["$-1$","$2$"]], [["$8$"],["$5$"]],
             "$=$", [["$1$"],["$2$"]]],
            fontsize=10.5, colw=0.52, scale=0.60)
```

::: caution Multiply on the left, and only on the left
Matrix multiplication is not commutative, so from $AX = B$ you may write
$X = A^{-1}B$ but **never** $X = BA^{-1}$ — the second product usually does not
even exist.
:::

::: example Worked example 6.5
**Problem.** Find the inverse of the matrix $A$ with rows $(3,5)$ and $(1,2)$, and
verify your answer.

**Solution.** $|A| = 3(2) - 5(1) = 6 - 5 = 1 \ne 0$, so $A^{-1}$ exists.

Using the $2\times2$ shortcut — swap $3$ and $2$, negate $5$ and $1$ —

$$ A^{-1} = \frac{1}{1}\times \text{(matrix with rows } (2,-5),\ (-1,3)) $$

so $A^{-1}$ has rows $(2,-5)$ and $(-1,3)$.

**Check.** $\;(AA^{-1})_{11} = 3(2)+5(-1) = 1$, $(AA^{-1})_{12} = 3(-5)+5(3) = 0$,
$(AA^{-1})_{21} = 1(2)+2(-1) = 0$, $(AA^{-1})_{22} = 1(-5)+2(3) = 1$. That is $I$.
:::

::: example Worked example 6.6
**Problem.** Find the inverse of the matrix $A$ with rows $(1,2,3)$, $(0,1,4)$,
$(5,6,0)$.

**Solution.** From Worked example 6.3, $|A| = 1 \ne 0$, and the cofactor matrix
$C$ has rows $(-24, 20, -5)$, $(18, -15, 4)$ and $(5, -4, 1)$.

Transposing $C$ gives

$$ \mathrm{adj}\,A = C^{T} \text{ with rows } (-24, 18, 5),\ (20, -15, -4),\ (-5, 4, 1) $$

Since $|A| = 1$,

$$ A^{-1} = \frac{\mathrm{adj}\,A}{|A|} = \mathrm{adj}\,A $$

**Check one entry.** Row 1 of $A$ times column 1 of $A^{-1}$ is
$1(-24) + 2(20) + 3(-5) = -24 + 40 - 15 = 1$, the correct diagonal entry; and row 1
times column 2 is $1(18) + 2(-15) + 3(4) = 18 - 30 + 12 = 0$, as required.
:::

::: example Worked example 6.7
**Problem.** Solve by the matrix-inverse method: $\;2x + 3y = 8$, $\;x + 2y = 5$.

**Solution.** $A$ has rows $(2,3)$ and $(1,2)$; $B$ is the column $(8,5)$.

$$ |A| = 2(2) - 3(1) = 1 \ne 0 $$

so $A^{-1}$ has rows $(2,-3)$ and $(-1,2)$. Then

$$ X = A^{-1}B: \qquad x = 2(8) + (-3)(5) = 16 - 15 = 1 $$
$$ y = (-1)(8) + 2(5) = -8 + 10 = 2 $$

So $x = 1$, $y = 2$. **Check:** $2(1)+3(2) = 8$ and $1 + 2(2) = 5$. Correct.
:::

::: example Worked example 6.8
**Problem.** Solve by the matrix-inverse method:

$$ x + 2y + 3z = 6, \qquad y + 4z = 5, \qquad 5x + 6y = 11 $$

**Solution.** The coefficient matrix is exactly the $A$ of Worked example 6.6, with
$|A| = 1$ and $A^{-1}$ of rows $(-24,18,5)$, $(20,-15,-4)$, $(-5,4,1)$. The
constant column is $B = (6,5,11)$.

$$ x = -24(6) + 18(5) + 5(11) = -144 + 90 + 55 = 1 $$
$$ y = 20(6) - 15(5) - 4(11) = 120 - 75 - 44 = 1 $$
$$ z = -5(6) + 4(5) + 1(11) = -30 + 20 + 11 = 1 $$

So $x = y = z = 1$. **Check in the third equation:** $5(1) + 6(1) = 11$. Correct.
:::

## 6.4 Determinant and its properties (without proof)

These properties are stated without proof in the NEB syllabus, but you are
expected to *use* them to shorten a calculation. Throughout, "row" may be replaced
by "column".

| No. | Property |
|---|---|
| P1 | $|A^{T}| = |A|$ — a determinant is unchanged by transposing. |
| P2 | Interchanging two rows **changes the sign** of the determinant. |
| P3 | If two rows are identical (or proportional), the determinant is $0$. |
| P4 | If every entry of one row is multiplied by $k$, the determinant is multiplied by $k$. Hence for an $n\times n$ matrix, $|kA| = k^{n}|A|$. |
| P5 | If a row is all zeros, the determinant is $0$. |
| P6 | **Row operation:** adding a multiple of one row to another leaves the determinant unchanged. |
| P7 | If one row is a sum, the determinant splits into the sum of two determinants. |
| P8 | $|AB| = |A|\,|B|$, and if $A^{-1}$ exists, $|A^{-1}| = 1/|A|$. |

::: tip P6 is the workhorse
Use P6 to manufacture zeros, then expand along the row or column that now has
them. A $3\times3$ with two zeros in a column costs you one $2\times2$ determinant
instead of three.
:::

::: example Worked example 6.9
**Problem.** Evaluate the determinant of the matrix with rows $(2,3,1)$,
$(4,7,3)$, $(6,8,5)$ again, this time using row operations.

**Solution.** Apply $R_2 \rightarrow R_2 - 2R_1$ and $R_3 \rightarrow R_3 - 3R_1$.
By P6 neither changes the value. The rows become

$$ (2,\ 3,\ 1), \qquad (0,\ 1,\ 1), \qquad (0,\ -1,\ 2) $$

Now expand along the **first column**, which has two zeros — only one term
survives:

$$ |A| = 2\left(1(2) - 1(-1)\right) = 2(2+1) = 6 $$

This matches Worked example 6.4, with far less arithmetic.
:::

::: example Worked example 6.10
**Problem.** Show that the determinant with rows $(1,1,1)$, $(a,b,c)$,
$(a^{2},b^{2},c^{2})$ equals $(a-b)(b-c)(c-a)$.

**Solution.** Use column operations $C_1 \rightarrow C_1 - C_2$ and
$C_2 \rightarrow C_2 - C_3$ (P6). The rows become

$$ (0,\ 0,\ 1), \qquad (a-b,\ b-c,\ c), \qquad (a^{2}-b^{2},\ b^{2}-c^{2},\ c^{2}) $$

Take out the factor $(a-b)$ from column 1 and $(b-c)$ from column 2 (P4):

$$ |A| = (a-b)(b-c)\times \text{determinant with rows } (0,0,1),\ (1,1,c),\ (a+b,\ b+c,\ c^{2}) $$

Expand along the first row — only the $(1,3)$ entry is non-zero, and its cofactor
sign is $+$:

$$ |A| = (a-b)(b-c)\left[1\cdot\left(1(b+c) - 1(a+b)\right)\right] = (a-b)(b-c)(c-a) $$
:::

::: example Worked example 6.11
**Problem.** Verify $|AB| = |A||B|$ for $A$ with rows $(1,2)$, $(3,4)$ and $B$ with
rows $(2,0)$, $(1,3)$.

**Solution.** $|A| = 1(4)-2(3) = -2$ and $|B| = 2(3)-0(1) = 6$, so
$|A||B| = -12$.

$AB$ has entries $(AB)_{11} = 1(2)+2(1) = 4$, $(AB)_{12} = 1(0)+2(3) = 6$,
$(AB)_{21} = 3(2)+4(1) = 10$, $(AB)_{22} = 3(0)+4(3) = 12$.

$$ |AB| = 4(12) - 6(10) = 48 - 60 = -12 $$

The two agree.
:::

### Cramer's rule

For $AX = B$ with $|A| = D \ne 0$, replace the column of coefficients of one
unknown by the constant column and take the determinant. Writing $D_x$, $D_y$,
$D_z$ for those three determinants,

$$ x = \frac{D_x}{D}, \qquad y = \frac{D_y}{D}, \qquad z = \frac{D_z}{D} $$

```figure caption="Cramer's rule applied to $x+y+z=6$, $2x-y+z=3$, $x+2y-z=2$. Each unknown's column is swapped for the constant column $(6,3,2)$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.9))
cw, rh = 0.46, 0.42
rows = lambda R: [[f"${v}$" for v in r] for r in R]
D  = [[1,1,1],[2,-1,1],[1,2,-1]]
Dx = [[6,1,1],[3,-1,1],[2,2,-1]]
Dy = [[1,6,1],[2,3,1],[1,2,-1]]
Dz = [[1,1,6],[2,-1,3],[1,2,2]]
items = [("$D =$", D, "$= 7$", 0.00, 1.75), ("$D_x =$", Dx, "$= 7$", 3.55, 1.75),
         ("$D_y =$", Dy, "$= 14$", 0.00, 0.10), ("$D_z =$", Dz, "$= 21$", 3.55, 0.10)]
for lab, R, res, x0, y0 in items:
    ax.text(x0 + 0.34, y0 + 1.5*rh, lab, ha='center', va='center', fontsize=10.5, color=INK)
    matrix(ax, rows(R), x=x0 + 0.80, y=y0, colw=cw, rowh=rh, fontsize=10.5, bracket="|")
    ax.text(x0 + 2.42, y0 + 1.5*rh, res, ha='left', va='center', fontsize=10.5, color=ACCENT)
ax.text(3.35, 3.24, '$x = 7/7 = 1$,   $y = 14/7 = 2$,   $z = 21/7 = 3$',
        ha='center', fontsize=10, color='#2e8b57')
ax.set_xlim(-0.15, 6.85); ax.set_ylim(-0.15, 3.55)
ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 6.12
**Problem.** Solve by Cramer's rule: $\;x+y+z = 6$, $\;2x-y+z = 3$,
$\;x+2y-z = 2$.

**Solution.** Expanding each determinant along its first row (see the figure):

$$ D = 1(1-2) - 1(-2-1) + 1(4+1) = -1 + 3 + 5 = 7 \ne 0 $$
$$ D_x = 6(1-2) - 1(-3-2) + 1(6+2) = -6 + 5 + 8 = 7 $$
$$ D_y = 1(-3-2) - 6(-2-1) + 1(4-3) = -5 + 18 + 1 = 14 $$
$$ D_z = 1(-2-6) - 1(4-3) + 6(4+1) = -8 - 1 + 30 = 21 $$

Hence $x = \dfrac{7}{7} = 1$, $y = \dfrac{14}{7} = 2$, $z = \dfrac{21}{7} = 3$.

**Check in the second equation:** $2(1) - 2 + 3 = 3$. Correct.
:::

::: caution Cramer's rule needs $D \ne 0$
If $D = 0$ the rule gives nothing. The system then has either no solution
(inconsistent) or infinitely many — decide which by row-reducing, not by dividing
by zero.
:::

### Row-equivalent matrices and Gauss elimination

Two matrices are **row-equivalent** if one can be turned into the other by
elementary row operations: swapping two rows, multiplying a row by a non-zero
constant, or adding a multiple of one row to another. Row-equivalent augmented
matrices represent systems with exactly the same solutions.

**Gauss elimination** uses these operations to drive the coefficient block into
upper-triangular form, after which the unknowns drop out one at a time by back
substitution.

```figure caption="Gauss elimination on the augmented matrix of $x+2y+3z=14$, $2x+3y+4z=20$, $3x+4y+6z=29$. The dashed line separates the constants."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.2,4.50))
cw, rh = 0.52, 0.42
stages = [
    ([[1,2,3,14],[2,3,4,20],[3,4,6,29]], ''),
    ([[1,2,3,14],[0,-1,-2,-8],[0,-2,-3,-13]],
     '$R_2 \\rightarrow R_2 - 2R_1$\n$R_3 \\rightarrow R_3 - 3R_1$'),
    ([[1,2,3,14],[0,-1,-2,-8],[0,0,1,3]], '$R_3 \\rightarrow R_3 - 2R_2$'),
]
y = 4.60
for k, (R, op) in enumerate(stages):
    rows = [[f"${v}$" for v in r] for r in R]
    w, h = matrix(ax, rows, x=0.55, y=y, colw=cw, rowh=rh, fontsize=10)
    ax.plot([0.55 + 3*cw - 0.05]*2, [y - 0.03, y + h + 0.03], color=MUTED, lw=0.9, ls=(0,(2,2)))
    if k < 2:
        ax.annotate('', xy=(0.55 + w/2, y - 0.88), xytext=(0.55 + w/2, y - 0.16),
                    arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.2, mutation_scale=10))
        ax.text(0.55 + w/2 + 0.30, y - 0.52, stages[k+1][1], ha='left', va='center',
                fontsize=9.0, color=ACCENT)
    y -= (h + 1.00)
ax.text(0.55 + 1.04, -0.52, '$z = 3 \\Rightarrow y = 2 \\Rightarrow x = 1$', ha='center',
        fontsize=10, color='#2e8b57')
ax.set_xlim(-0.15, 6.34); ax.set_ylim(-0.95, 6.01)
ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 6.13
**Problem.** Solve by Gauss elimination:

$$ x + 2y + 3z = 14, \qquad 2x + 3y + 4z = 20, \qquad 3x + 4y + 6z = 29 $$

**Solution.** Write the augmented matrix with rows $(1,2,3\,|\,14)$,
$(2,3,4\,|\,20)$, $(3,4,6\,|\,29)$.

$R_2 \rightarrow R_2 - 2R_1$ gives $(0,-1,-2\,|\,-8)$, i.e. $-y - 2z = -8$.
$R_3 \rightarrow R_3 - 3R_1$ gives $(0,-2,-3\,|\,-13)$.

$R_3 \rightarrow R_3 - 2R_2$ gives $(0,0,1\,|\,3)$, i.e. $z = 3$.

Back-substituting into $-y-2z = -8$: $\;-y - 6 = -8$, so $y = 2$. Then from the
first row, $x + 4 + 9 = 14$, so $x = 1$.

**Solution:** $x = 1$, $y = 2$, $z = 3$. **Check in the third equation:**
$3 + 8 + 18 = 29$. Correct.
:::

::: example Worked example 6.14
**Problem.** For what value of $k$ is the matrix with rows $(2,4)$ and $(3,k)$
singular? What happens to the system $2x+4y = 5$, $3x + ky = 7$ at that value?

**Solution.** Singular means $|A| = 0$:

$$ 2k - 4(3) = 0 \;\Longrightarrow\; 2k = 12 \;\Longrightarrow\; k = 6 $$

At $k = 6$ the second equation is $3x + 6y = 7$, i.e.
$x + 2y = \tfrac73$, while the first is $x + 2y = \tfrac52$. The same expression
cannot equal two different numbers, so the system is **inconsistent** — no
solution. Geometrically the two lines are parallel, which is exactly what a zero
determinant detects.
:::

## Chapter summary

- $(AB)_{ij}$ is row $i$ of $A$ against column $j$ of $B$; $AB$ needs
  (columns of $A$) = (rows of $B$), and $AB \ne BA$ in general.
- Transpose swaps rows and columns: $(A^{T})^{T} = A$, $(A+B)^{T} = A^{T}+B^{T}$,
  $(kA)^{T} = kA^{T}$, and the reversal law $(AB)^{T} = B^{T}A^{T}$.
- Symmetric: $A^{T} = A$. Skew-symmetric: $A^{T} = -A$ (zero diagonal). Every
  square $A = \frac12(A+A^{T}) + \frac12(A-A^{T})$.
- Minor $M_{ij}$ = determinant after deleting row $i$ and column $j$; cofactor
  $C_{ij} = (-1)^{i+j}M_{ij}$. Expand $|A|$ along the row or column with most zeros.
- $\mathrm{adj}\,A$ = transpose of the cofactor matrix, and
  $A(\mathrm{adj}\,A) = (\mathrm{adj}\,A)A = |A|I$.
- $A^{-1} = \dfrac{\mathrm{adj}\,A}{|A|}$ exists **iff** $|A| \ne 0$;
  $(AB)^{-1} = B^{-1}A^{-1}$ and $|A^{-1}| = 1/|A|$.
- Determinant properties: $|A^{T}| = |A|$; a row swap flips the sign; equal or
  proportional rows give $0$; $|kA| = k^{n}|A|$; adding a multiple of one row to
  another changes nothing; $|AB| = |A||B|$.
- Systems: $AX = B$ gives $X = A^{-1}B$; Cramer's rule gives $x = D_x/D$ etc. for
  $D \ne 0$; Gauss elimination row-reduces the augmented matrix to
  upper-triangular form and back-substitutes.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. If $A$ is of order $3 \times 2$, then $A^{T}$ is of order <span class="marks">[1]</span>
   (a) $3\times2$ (b) $2\times3$ (c) $3\times3$ (d) $2\times2$
2. $(AB)^{T}$ equals <span class="marks">[1]</span>
   (a) $A^{T}B^{T}$ (b) $B^{T}A^{T}$ (c) $AB$ (d) $BA$
3. The determinant of the matrix with rows $(2,3)$ and $(4,5)$ is <span class="marks">[1]</span>
   (a) $22$ (b) $2$ (c) $-2$ (d) $-22$
4. A square matrix $A$ has an inverse if and only if <span class="marks">[1]</span>
   (a) $|A| = 0$ (b) $|A| \ne 0$ (c) $A = A^{T}$ (d) $A$ is of order $2$
5. $A\,(\mathrm{adj}\,A)$ equals <span class="marks">[1]</span>
   (a) $I$ (b) $A^{-1}$ (c) $|A|\,I$ (d) $O$
6. Every diagonal entry of a skew-symmetric matrix is <span class="marks">[1]</span>
   (a) $1$ (b) $0$ (c) equal to $|A|$ (d) negative

::: note Answers to Group A
**1.** (b) — transposing swaps the two numbers in the order.

**2.** (b) — the reversal law.

**3.** (c) — $2(5) - 3(4) = 10 - 12 = -2$.

**4.** (b) — $A^{-1} = \mathrm{adj}\,A/|A|$ requires division by $|A|$.

**5.** (c) — proved in §6.3.

**6.** (b) — $a_{ii} = -a_{ii}$ forces $a_{ii} = 0$.
:::

**Group B — Short answer (5 marks each)**

1. Define the transpose of a matrix. For $A$ with rows $(1,2)$, $(3,4)$ and $B$
   with rows $(2,0)$, $(1,3)$, verify that $(AB)^{T} = B^{T}A^{T}$. <span class="marks">[5]</span>
2. Find the adjoint and the inverse of the matrix with rows $(2,1)$ and $(7,4)$,
   and verify that $AA^{-1} = I$. <span class="marks">[5]</span>
3. Solve by Cramer's rule: $\;2x + 3y = 13$, $\;3x - y = 3$. <span class="marks">[5]</span>
4. Using properties of determinants, show that the determinant with rows
   $(1,a,a^{2})$, $(1,b,b^{2})$, $(1,c,c^{2})$ equals $(a-b)(b-c)(c-a)$. <span class="marks">[5]</span>
5. Express the matrix with rows $(3,5)$ and $(1,7)$ as the sum of a symmetric and
   a skew-symmetric matrix. <span class="marks">[5]</span>
6. If $A$ is a non-singular matrix of order $3$ with $|A| = 5$, find
   $|\mathrm{adj}\,A|$ and $|A^{-1}|$. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** The transpose $A^{T}$ is obtained by interchanging rows and columns, so
$(A^{T})_{ij} = a_{ji}$.

$AB$ has entries $1(2)+2(1) = 4$, $1(0)+2(3) = 6$, $3(2)+4(1) = 10$,
$3(0)+4(3) = 12$; so $AB$ has rows $(4,6)$, $(10,12)$ and $(AB)^{T}$ has rows
$(4,10)$, $(6,12)$.

$B^{T}$ has rows $(2,1)$, $(0,3)$; $A^{T}$ has rows $(1,3)$, $(2,4)$. Then
$B^{T}A^{T}$ has entries $2(1)+1(2) = 4$, $2(3)+1(4) = 10$, $0(1)+3(2) = 6$,
$0(3)+3(4) = 12$ — rows $(4,10)$ and $(6,12)$. The two agree.

**2.** $|A| = 2(4) - 1(7) = 1$. The cofactors are $C_{11} = 4$, $C_{12} = -7$,
$C_{21} = -1$, $C_{22} = 2$, so the cofactor matrix has rows $(4,-7)$, $(-1,2)$
and $\mathrm{adj}\,A$ (its transpose) has rows $(4,-1)$, $(-7,2)$.

Since $|A| = 1$, $A^{-1} = \mathrm{adj}\,A$, with rows $(4,-1)$ and $(-7,2)$.

Check: $(AA^{-1})_{11} = 2(4)+1(-7) = 1$, $(AA^{-1})_{12} = 2(-1)+1(2) = 0$,
$(AA^{-1})_{21} = 7(4)+4(-7) = 0$, $(AA^{-1})_{22} = 7(-1)+4(2) = 1$. So
$AA^{-1} = I$.

**3.** $D = 2(-1) - 3(3) = -11 \ne 0$.

$$ D_x = 13(-1) - 3(3) = -22, \qquad D_y = 2(3) - 13(3) = -33 $$

$$ x = \frac{-22}{-11} = 2, \qquad y = \frac{-33}{-11} = 3 $$

Check: $2(2)+3(3) = 13$ and $3(2) - 3 = 3$. Correct.

**4.** The determinant is the transpose of the one in Worked example 6.10, and by
P1 transposing does not change the value, so it is $(a-b)(b-c)(c-a)$. (Directly:
$R_1 \rightarrow R_1 - R_2$ and $R_2 \rightarrow R_2 - R_3$, take out $(a-b)$ and
$(b-c)$, then expand.)

**5.** $A^{T}$ has rows $(3,1)$, $(5,7)$. Then $\frac12(A+A^{T})$ has rows
$(3,3)$ and $(3,7)$ — symmetric; and $\frac12(A-A^{T})$ has rows $(0,2)$ and
$(-2,0)$ — skew-symmetric. Their sum has rows $(3,5)$, $(1,7)$, which is $A$.

**6.** Take determinants of $A(\mathrm{adj}\,A) = |A|I$. By P8 and P4 (with
$n = 3$),

$$ |A|\cdot|\mathrm{adj}\,A| = \left(|A|\right)^{3}|I| = |A|^{3}
\;\Longrightarrow\; |\mathrm{adj}\,A| = |A|^{2} = 25 $$

And from $AA^{-1} = I$, $|A||A^{-1}| = 1$, so
$|A^{-1}| = \dfrac15$.
:::

**Group C — Long answer (8 marks each)**

1. (a) Define the minor and the cofactor of an element of a square matrix, and
   state how the adjoint is built from them. <span class="marks">[3]</span>
   (b) Find the inverse of the matrix $A$ with rows $(3,-3,4)$, $(2,-3,4)$,
   $(0,-1,1)$ by the adjoint method, and verify that $AA^{-1} = I$. <span class="marks">[5]</span>
2. (a) State any four properties of determinants. <span class="marks">[3]</span>
   (b) Solve the system $\;x+2y+3z = 14$, $\;2x+3y+4z = 20$, $\;3x+4y+6z = 29$
   by Gauss elimination. <span class="marks">[5]</span>
3. (a) Show that $A(\mathrm{adj}\,A) = |A|\,I$ and deduce the formula for
   $A^{-1}$. <span class="marks">[4]</span>
   (b) Solve $\;x+y+z = 6$, $\;2x-y+z = 3$, $\;x+2y-z = 2$ by Cramer's rule. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** (a) The minor $M_{ij}$ is the determinant left after deleting row $i$ and
column $j$; the cofactor is $C_{ij} = (-1)^{i+j}M_{ij}$; the adjoint is the
**transpose** of the matrix of cofactors.

(b) Expanding along the third row,
$|A| = 0 - (-1)\left[3(4)-4(2)\right] + 1\left[3(-3)-(-3)(2)\right] = 4 + (-3) = 1$.

The cofactors are
$C_{11} = (-3)(1) - 4(-1) = 1$, $C_{12} = -\left[2(1)-4(0)\right] = -2$,
$C_{13} = 2(-1) - (-3)(0) = -2$;
$C_{21} = -\left[(-3)(1) - 4(-1)\right] = -1$, $C_{22} = 3(1)-4(0) = 3$,
$C_{23} = -\left[3(-1) - (-3)(0)\right] = 3$;
$C_{31} = (-3)(4) - 4(-3) = 0$, $C_{32} = -\left[3(4)-4(2)\right] = -4$,
$C_{33} = 3(-3) - (-3)(2) = -3$.

So the cofactor matrix has rows $(1,-2,-2)$, $(-1,3,3)$, $(0,-4,-3)$, and
$\mathrm{adj}\,A = C^{T}$ has rows $(1,-1,0)$, $(-2,3,-4)$, $(-2,3,-3)$. Since
$|A| = 1$, $A^{-1} = \mathrm{adj}\,A$.

Check the first row of $AA^{-1}$: $3(1)+(-3)(-2)+4(-2) = 3+6-8 = 1$;
$3(-1)+(-3)(3)+4(3) = -3-9+12 = 0$; $3(0)+(-3)(-4)+4(-3) = 12-12 = 0$. So the
first row of $AA^{-1}$ is $(1,0,0)$, as required.

**2.** (a) Any four of P1–P8 in the table above, for example: $|A^{T}| = |A|$;
interchanging two rows changes the sign; two identical rows give zero; adding a
multiple of one row to another leaves the value unchanged.

(b) See Worked example 6.13: the augmented matrix row-reduces to rows
$(1,2,3\,|\,14)$, $(0,-1,-2\,|\,-8)$, $(0,0,1\,|\,3)$, giving $z = 3$, then
$y = 2$, then $x = 1$.

**3.** (a) The $(i,j)$ entry of $A(\mathrm{adj}\,A)$ is
$\sum_k a_{ik}C_{jk}$. For $i = j$ this is the cofactor expansion of $|A|$ along
row $i$; for $i \ne j$ it is the expansion of a determinant with row $j$ replaced
by row $i$ — two identical rows — so it is $0$. Hence
$A(\mathrm{adj}\,A) = |A|I$, and dividing by $|A| \ne 0$ gives
$A^{-1} = \mathrm{adj}\,A / |A|$.

(b) See Worked example 6.12: $D = 7$, $D_x = 7$, $D_y = 14$, $D_z = 21$, so
$x = 1$, $y = 2$, $z = 3$.
:::
