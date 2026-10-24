---
subject: Optional Mathematics
grade: 8
unit: 5
title: Matrix
hours: 0
---

A class teacher records the marks of three students in four subjects in a table of 3 rows and 4 columns. A shopkeeper with two shops records the pens, copies and bags sold in each shop in a table of 2 rows and 3 columns. When we keep only the numbers of such a table and put them in brackets, we get a **matrix** (plural: **matrices**). A matrix lets us treat a whole table of numbers as one object: we can compare two tables, add them, subtract them, or scale a whole table up or down in one step. Matrices are used in computer graphics, in economics and in solving equations, as you will see in grade 9 and 10. This chapter introduces the language of matrices, the main types of matrix, and the three operations of addition, subtraction and multiplication by a number.

::: key What your examination asks from this chapter
Expect: (i) the **order** of a matrix and the position of an **element** such as $a_{23}$; (ii) constructing a matrix from a rule such as $a_{ij}=i+2j$; (iii) naming the **type** of a matrix (row, column, square, diagonal, scalar, unit, symmetric, triangular) with a reason; (iv) finding unknowns from **equal matrices**; (v) adding and subtracting matrices, and **verifying** a property such as $A+B=B+A$; (vi) finding $kA$, $2A+3B$ or a matrix $X$ from an equation such as $X+A=B$ or $2X-A=B$; (vii) a word problem about sales or marks set out as matrices.
:::

## 5.1 Matrix: elements, rows, columns and order

Here are the marks of three students of a school in Hetauda.

| Student | Maths | Science | English | Opt. Maths |
|---|---|---|---|---|
| Anish | 78 | 65 | 70 | 82 |
| Bipana | 85 | 90 | 72 | 88 |
| Chandra | 60 | 74 | 81 | 69 |

Keeping only the numbers, in the same places, gives the matrix $M$ drawn below.

```figure caption="The marks table written as a matrix $M$. Horizontal lines of numbers are rows and vertical lines are columns. The element in row 2 and column 3 is $m_{23}=72$, Bipana's English mark. $M$ has 3 rows and 4 columns, so its order is $3\times4$."
fig, ax = plt.subplots(figsize=(5.0, 2.9))
rows = [['78', '65', '70', '82'], ['85', '90', '72', '88'], ['60', '74', '81', '69']]
x0, y0, cw, rh = 2.0, 0.4, 0.8, 0.55
matrix(ax, rows, x=x0, y=y0, fontsize=11, colw=cw, rowh=rh)
ax.text(x0 - 0.65, y0 + 3*rh/2, 'M =', ha='right', va='center', fontsize=11)
for i, name in enumerate(['row 1', 'row 2', 'row 3']):
    ax.text(x0 + 4*cw + 0.35, y0 + 3*rh - (i + 0.5)*rh, name, va='center', fontsize=8, color=MUTED)
for j, name in enumerate(['col 1', 'col 2', 'col 3', 'col 4']):
    ax.text(x0 + (j + 0.5)*cw, y0 + 3*rh + 0.25, name, ha='center', fontsize=8, color=MUTED)
cx, cy = x0 + 2.5*cw, y0 + 3*rh - 1.5*rh
ax.add_patch(Rectangle((x0 + 0.04, cy - rh/2 + 0.03), 4*cw - 0.08, rh - 0.06, fc='#e3eefa', ec='none', zorder=0))
ax.add_patch(Rectangle((x0 + 2*cw + 0.04, y0 + 0.02), cw - 0.08, 3*rh - 0.04, fc='#fbe3e2', ec='none', zorder=0))
ax.add_patch(Rectangle((cx - 0.3, cy - 0.21), 0.6, 0.42, fill=False, ec=SERIES[1], lw=1.4))
ax.text(x0 + 2*cw, -0.45, 'row 2 (blue band) and column 3 (red band) cross at  m₂₃ = 72', ha='center', fontsize=8.5, color=INK)
ax.text(x0 + 2*cw, -0.85, 'order 3 × 4  (rows × columns)', ha='center', fontsize=8.5, color=MUTED)
ax.set_xlim(-0.6, 6.6); ax.set_ylim(-1.1, 2.6); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: definition Matrix, element, order
A **matrix** is a rectangular arrangement of numbers in **rows** (horizontal lines) and **columns** (vertical lines), enclosed in square brackets $[\ ]$ or round brackets $(\ )$. Each number in it is an **element** (or entry). A matrix with $m$ rows and $n$ columns has **order** $m\times n$, read "$m$ by $n$"; it has $m\times n$ elements.
:::

Matrices are named with capital letters $A, B, M, \ldots$ and their elements with the matching small letter and two little numbers. The element in the $i$th row and $j$th column of $A$ is written $a_{ij}$: **row first, column second**. In the marks matrix, $m_{23}=72$ and $m_{34}=69$. A matrix of order $2\times3$ looks, in general, like this:

| | column 1 | column 2 | column 3 |
|---|---|---|---|
| row 1 | $a_{11}$ | $a_{12}$ | $a_{13}$ |
| row 2 | $a_{21}$ | $a_{22}$ | $a_{23}$ |

We write it briefly as $A=[a_{ij}]_{2\times3}$.

Matrices are everywhere once you look for them. A black-and-white photograph on a phone is stored as a matrix: the screen is divided into tiny squares called **pixels**, and each element of the matrix is the brightness of one pixel, from 0 (black) to 255 (white). A photo 1200 pixels wide and 800 pixels high is a matrix of order $800\times1200$ with 960,000 elements. Brightening the photo adds the same number to every element; making a "negative" replaces each element $a$ by $255-a$. The operations of this chapter are exactly what photo-editing apps do.

**Writing a matrix inside a line of text.** A matrix needs a rectangle of space, and a line of print has none. So in running text this book sometimes lists the rows in order, each row in round brackets: $[(3,5,7),(4,6,8)]$ means the $2\times3$ matrix whose first row is 3, 5, 7 and whose second row is 4, 6, 8. In your own work, always draw the full rectangular array, as in the figures.

::: example Reading a matrix
**Problem.** For the marks matrix $M$: (i) write its order and the number of its elements; (ii) find $m_{23}$ and $m_{34}$ and say what they mean; (iii) what does the second row stand for?

**Solution.** (i) $M$ has 3 rows and 4 columns, so its order is $3\times4$ and it has $3\times4=12$ elements.

(ii) $m_{23}$ is in row 2, column 3: $m_{23}=72$, Bipana's English mark. $m_{34}$ is in row 3, column 4: $m_{34}=69$, Chandra's Optional Maths mark.

(iii) Row 2 is $85, 90, 72, 88$: all four marks of Bipana.
:::

::: example Possible orders
**Problem.** A matrix has 12 elements. What orders can it have? What if it has 7 elements?

**Solution.** The order $m\times n$ must have $m\times n=12$, so the possible orders are
$$ 1\times12,\quad 2\times6,\quad 3\times4,\quad 4\times3,\quad 6\times2,\quad 12\times1 $$
Six orders in all. Note that $3\times4$ and $4\times3$ are different orders. A matrix with 7 elements can only be $1\times7$ or $7\times1$, because 7 is prime.
:::

::: example Constructing a matrix from a rule
**Problem.** Construct (i) the $2\times3$ matrix $A=[a_{ij}]$ with $a_{ij}=i+2j$; (ii) the $3\times2$ matrix $B=[b_{ij}]$ with $b_{ij}=2i-j$.

**Solution.** (i) Work out each element from its row number $i$ and column number $j$:
$$ a_{11}=1+2=3,\quad a_{12}=1+4=5,\quad a_{13}=1+6=7 $$
$$ a_{21}=2+2=4,\quad a_{22}=2+4=6,\quad a_{23}=2+6=8 $$
So $A=[(3,5,7),(4,6,8)]$.

(ii) $b_{11}=2-1=1$, $b_{12}=2-2=0$, $b_{21}=4-1=3$, $b_{22}=2$, $b_{31}=5$, $b_{32}=4$. So $B=[(1,0),(3,2),(5,4)]$, three rows and two columns.
:::

::: caution Rows first, then columns
The order $3\times4$ means 3 **rows** and 4 **columns**, not the other way round, and $a_{23}$ means row 2, column 3. Think of a cinema ticket: it gives the **row** first and then the seat number along that row. Matrices follow the same order, **R**ow before **C**olumn.
:::

## 5.2 Types of matrices: row, column, zero, rectangular, square, diagonal, scalar, unit, equal, symmetric and triangular

Matrices are named by their shape and by the pattern of their elements. The figure shows one example of each type; the table below it gives the definitions.

```figure caption="One example of each type of matrix. In a square matrix the elements $a_{11}, a_{22}, a_{33}, \ldots$ form the leading diagonal (shaded); diagonal, scalar, unit, symmetric and triangular matrices are all described by what happens on and around that diagonal."
fig, ax = plt.subplots(figsize=(5.2, 3.9))
M = '−'
items = [('row  1 × 3', [['2', '5', M + '1']]), ('column  3 × 1', [['3'], ['0'], ['7']]), ('zero  O', [['0', '0'], ['0', '0']]),
         ('rectangular  2 × 3', [['1', '2', '3'], ['4', '5', '6']]), ('square  2 × 2', [['4', M + '1'], ['2', '3']]),
         ('diagonal', [['2', '0', '0'], ['0', M + '1', '0'], ['0', '0', '5']]), ('scalar', [['3', '0'], ['0', '3']]),
         ('unit  I', [['1', '0', '0'], ['0', '1', '0'], ['0', '0', '1']]), ('symmetric', [['1', '4', '5'], ['4', '2', '6'], ['5', '6', '3']]),
         ('upper triangular', [['1', '2', '3'], ['0', '4', '5'], ['0', '0', '6']]), ('lower triangular', [['1', '0', '0'], ['2', '3', '0'], ['4', '5', '6']]),
         ('equal matrices', None)]
cw, rh = 0.42, 0.36
for k, (name, rows) in enumerate(items):
    c, r = k % 4, k // 4
    cx, top = 1.5 + 3.0*c, 6.5 - 2.25*r
    if rows is None:
        for dx in (-0.75, 0.75):
            matrix(ax, [['2', '1'], ['0', '3']], x=cx + dx - cw, y=top - 1.45, fontsize=9, colw=cw, rowh=rh)
        ax.text(cx, top - 1.45 + rh, '=', ha='center', va='center', fontsize=10)
    else:
        nr, nc = len(rows), len(rows[0])
        x, y = cx - nc*cw/2, top - 0.35 - nr*rh
        if nr == nc and nr > 1:
            for d in range(nr):
                ax.add_patch(Rectangle((x + d*cw + 0.03, y + (nr - 1 - d)*rh + 0.03), cw - 0.06, rh - 0.06, fc='#e3eefa', ec='none', zorder=0))
        matrix(ax, rows, x=x, y=y, fontsize=9, colw=cw, rowh=rh)
    ax.text(cx, top - 1.95, name, ha='center', fontsize=8, color=ACCENT)
ax.set_xlim(-0.1, 12.1); ax.set_ylim(-0.4, 6.6); ax.axis('off')
fig.tight_layout(pad=0.2)
```

| Type | Definition | Example |
|---|---|---|
| **Row matrix** | only one row; order $1\times n$ | $[(2,5,-1)]$ |
| **Column matrix** | only one column; order $m\times1$ | $[(3),(0),(7)]$ |
| **Zero (null) matrix** $O$ | every element is 0; any order | $[(0,0),(0,0)]$ |
| **Rectangular matrix** | number of rows $\neq$ number of columns | order $2\times3$ |
| **Square matrix** | number of rows $=$ number of columns; order $n\times n$, or "order $n$" | order $2\times2$ |
| **Diagonal matrix** | a square matrix whose elements **off** the leading diagonal are all 0 | $[(2,0,0),(0,-1,0),(0,0,5)]$ |
| **Scalar matrix** | a diagonal matrix whose diagonal elements are all **equal** | $[(3,0),(0,3)]$ |
| **Unit (identity) matrix** $I$ | a scalar matrix whose diagonal elements are all **1** | $[(1,0),(0,1)]$ |
| **Symmetric matrix** | a square matrix with $a_{ij}=a_{ji}$ for every $i$ and $j$ | $[(1,4,5),(4,2,6),(5,6,3)]$ |
| **Upper triangular matrix** | a square matrix whose elements **below** the leading diagonal are all 0 | $[(1,2,3),(0,4,5),(0,0,6)]$ |
| **Lower triangular matrix** | a square matrix whose elements **above** the leading diagonal are all 0 | $[(1,0,0),(2,3,0),(4,5,6)]$ |

The **leading (principal) diagonal** of a square matrix runs from the top-left corner to the bottom-right corner: the elements $a_{11}, a_{22}, a_{33}, \ldots$. Only square matrices have one, which is why the last six types in the table are all square.

### Symmetric matrices and the transpose

In a symmetric matrix the leading diagonal acts like a mirror: the element in row 1, column 2 equals the element in row 2, column 1, and so on. Interchanging the rows and columns of a matrix $A$ (row 1 becomes column 1, row 2 becomes column 2, …) gives its **transpose**, written $A^T$ or $A'$. A matrix is symmetric exactly when it equals its own transpose, $A^T=A$.

### A family of special square matrices

Some types sit inside others:

- every **unit** matrix is a **scalar** matrix (all its diagonal elements are equal to 1);
- every **scalar** matrix is a **diagonal** matrix;
- every **diagonal** matrix is both **upper** and **lower triangular**, and it is also **symmetric**.

So $I$ deserves all five names. But a symmetric matrix need not be diagonal, and a triangular matrix need not be symmetric.

### Equal matrices

::: definition Equal matrices
Two matrices $A$ and $B$ are **equal**, $A=B$, when (i) they have the **same order**, and (ii) their **corresponding elements are equal**: $a_{ij}=b_{ij}$ for every $i$ and $j$.
:::

Matrices of different orders are never equal, even if they contain the same numbers: the row matrix $[(1,2)]$ is not equal to the column matrix $[(1),(2)]$.

::: example Unknowns from equal matrices
**Problem.** Find $x$ and $y$ if $[(x+2,\ 3),(5,\ y-1)]=[(7,\ 3),(5,\ 4)]$. Then find $a$ and $b$ if $[(a+b,\ 2),(4,\ a-b)]=[(9,\ 2),(4,\ 1)]$.

**Solution.** Both pairs of matrices are $2\times2$, so we may equate corresponding elements.

First pair: $x+2=7$ gives $x=5$; $y-1=4$ gives $y=5$.

Second pair: $a+b=9$ and $a-b=1$. Adding, $2a=10$, so $a=5$ and $b=4$.
:::

::: example Making a matrix symmetric
**Problem.** Find $x$ and $y$ so that $A=[(1,\ x,\ 4),(3,\ 2,\ y),(4,\ 6,\ 5)]$ is symmetric.

**Solution.** For symmetry, $a_{ij}=a_{ji}$. Compare the elements on either side of the leading diagonal:

$a_{12}=a_{21}$: $x=3$. $\quad a_{23}=a_{32}$: $y=6$. $\quad a_{13}=a_{31}$: $4=4$ ✓.

So $x=3$ and $y=6$, and $A=[(1,3,4),(3,2,6),(4,6,5)]$.
:::

::: example Naming the type
**Problem.** If $[(a-2,\ 0),(0,\ b+1)]$ is the unit matrix of order 2, find $a$ and $b$. Name all the types that describe $[(5,0,0),(0,5,0),(0,0,5)]$.

**Solution.** The unit matrix has 1 on the diagonal: $a-2=1$ gives $a=3$, and $b+1=1$ gives $b=0$.

$[(5,0,0),(0,5,0),(0,0,5)]$ is square, diagonal, **scalar** (all diagonal elements are 5), symmetric, and both upper and lower triangular. It is not a unit matrix, because its diagonal elements are 5, not 1.
:::

## 5.3 Addition and subtraction of matrices and the properties of matrix addition

### Addition and subtraction

Two matrices can be added or subtracted **only if they have the same order**. Then we add (or subtract) the elements that are in the same position.

::: definition Sum and difference of matrices
If $A=[a_{ij}]$ and $B=[b_{ij}]$ have the same order, then
$$ A+B=[a_{ij}+b_{ij}] \qquad\text{and}\qquad A-B=[a_{ij}-b_{ij}] $$
The result has the same order as $A$ and $B$.
:::

```figure caption="Adding and subtracting two $2\times3$ matrices element by element: each element of the answer comes from the two elements in the same position."
fig, ax = plt.subplots(figsize=(5.2, 3.3))
M = '−'
A = [['2', M + '1', '3'], ['0', '4', '5']]; B = [['5', '2', M + '3'], ['1', M + '2', '6']]
rh = 0.5
def put(rows, x, y, cw):
    matrix(ax, rows, x=x, y=y, fontsize=10, colw=cw, rowh=rh)
    return x + len(rows[0])*cw
ax.text(0.0, 3.0, 'A =', va='center', fontsize=10.5); put(A, 0.95, 2.5, 0.55)
ax.text(3.4, 3.0, 'B =', va='center', fontsize=10.5); put(B, 4.35, 2.5, 0.55)
ax.text(0.0, 1.55, 'A + B =', va='center', fontsize=10.5)
put([['2+5', M + '1+2', '3+(' + M + '3)'], ['0+1', '4+(' + M + '2)', '5+6']], 1.55, 1.05, 1.05)
ax.text(5.05, 1.55, '=', va='center', fontsize=10.5)
put([['7', '1', '0'], ['1', '2', '11']], 5.6, 1.05, 0.5)
ax.text(0.0, 0.1, 'A − B =', va='center', fontsize=10.5)
put([['2' + M + '5', M + '1' + M + '2', '3' + M + '(' + M + '3)'], ['0' + M + '1', '4' + M + '(' + M + '2)', '5' + M + '6']], 1.55, -0.4, 1.05)
ax.text(5.05, 0.1, '=', va='center', fontsize=10.5)
put([[M + '3', M + '3', '6'], [M + '1', '6', M + '1']], 5.6, -0.4, 0.5)
ax.set_xlim(-0.2, 7.4); ax.set_ylim(-0.7, 3.7); ax.axis('off')
fig.tight_layout(pad=0.2)
```

::: example Adding and subtracting
**Problem.** If $A=[(2,-1,3),(0,4,5)]$ and $B=[(5,2,-3),(1,-2,6)]$, find $A+B$, $A-B$ and $B-A$. How are $A-B$ and $B-A$ related?

**Solution.** Both are $2\times3$, so the operations are possible. Element by element (see the figure above):
$$ A+B=[(7,1,0),(1,2,11)],\qquad A-B=[(-3,-3,6),(-1,6,-1)] $$
$$ B-A=[(5-2,\ 2+1,\ -3-3),(1-0,\ -2-4,\ 6-5)]=[(3,3,-6),(1,-6,1)] $$
Every element of $B-A$ is the negative of the matching element of $A-B$, so $B-A=-(A-B)$. Subtraction of matrices, like subtraction of numbers, depends on the order.
:::

::: example Sales in two shops
**Problem.** Ram has stationery shops in Butwal and Pokhara. The numbers of pens and copies sold are given by the matrices below (rows: Butwal, Pokhara; columns: pens, copies).

Baisakh: $B=[(120,80),(95,60)]$. Jestha: $J=[(140,70),(110,75)]$.

Find the total sales of the two months and the change from Baisakh to Jestha.

**Solution.** Total: $B+J=[(120+140,\ 80+70),(95+110,\ 60+75)]=[(260,150),(205,135)]$.

Change: $J-B=[(140-120,\ 70-80),(110-95,\ 75-60)]=[(20,-10),(15,15)]$.

So Butwal sold 20 more pens but **10 fewer copies** (the negative element), and Pokhara sold 15 more of each.
:::

::: caution Different orders cannot be added
$[(1,2),(3,4)]+[(1,2,3)]$ has **no meaning**: a $2\times2$ matrix and a $1\times3$ matrix have no elements in matching positions. Before adding or subtracting, write the two orders side by side and check that they are the same. If they are not, the answer is "not possible", and that is a correct answer.
:::

### Properties of matrix addition

Let $A$, $B$ and $C$ be matrices of the same order, and $O$ the zero matrix of that order.

| Property | Statement |
|---|---|
| Closure | $A+B$ is again a matrix of the same order |
| Commutative | $A+B=B+A$ |
| Associative | $(A+B)+C=A+(B+C)$ |
| Additive identity | $A+O=O+A=A$; the zero matrix changes nothing |
| Additive inverse | $A+(-A)=O$, where $-A$ has every element of $A$ with its sign changed |

These hold because each element of a sum is an ordinary sum of numbers, and numbers obey the same laws. Matrix subtraction is **not** commutative: in general $A-B\neq B-A$.

The additive inverse also explains subtraction: $A-B=A+(-B)$. To subtract $B$, change the sign of every element of $B$ and add. This is the same rule you used for subtracting polynomials, and it is the safest way to avoid sign errors when an element of $B$ is negative, as with $3-(-3)=3+3=6$ in the figure above.

::: example Verifying the associative property
**Problem.** If $A=[(1,2),(3,4)]$, $B=[(5,-1),(0,2)]$ and $C=[(-2,3),(4,1)]$, verify that $(A+B)+C=A+(B+C)$ and that $A+B=B+A$.

**Solution.** $A+B=[(6,1),(3,6)]$, and $B+A=[(5+1,\ -1+2),(0+3,\ 2+4)]=[(6,1),(3,6)]$, so $A+B=B+A$.

Left side: $(A+B)+C=[(6-2,\ 1+3),(3+4,\ 6+1)]=[(4,4),(7,7)]$.

Right side: $B+C=[(3,2),(4,3)]$, so $A+(B+C)=[(1+3,\ 2+2),(3+4,\ 4+3)]=[(4,4),(7,7)]$.

Both sides are $[(4,4),(7,7)]$, so the property is verified.
:::

::: example Solving a matrix equation
**Problem.** (i) Find the matrix $X$ such that $X+A=B$, where $A=[(3,-2),(1,4)]$ and $B=[(5,0),(-2,7)]$. (ii) Find $x$ and $y$ if $[(x,3),(2,y)]+[(4,-1),(y,5)]=[(9,2),(8,11)]$.

**Solution.** (i) Add $-A$ to both sides: $X=B-A=[(5-3,\ 0+2),(-2-1,\ 7-4)]=[(2,2),(-3,3)]$.

Check: $X+A=[(2+3,\ 2-2),(-3+1,\ 3+4)]=[(5,0),(-2,7)]=B$ ✓.

(ii) Add the left side element by element: $[(x+4,\ 2),(2+y,\ y+5)]=[(9,2),(8,11)]$. So $x+4=9$ gives $x=5$; $2+y=8$ gives $y=6$; and $y+5=11$ gives $y=6$ again, which agrees.
:::

## 5.4 Multiplication of a matrix by a scalar

In matrix work an ordinary number is called a **scalar**. If every price in a list goes up by 10%, every element is multiplied by the same number 1.1. This is **scalar multiplication**.

::: definition Scalar multiple of a matrix
If $A=[a_{ij}]$ and $k$ is a scalar (a number), then $kA$ is the matrix obtained by multiplying **every element** of $A$ by $k$:
$$ kA=[k\,a_{ij}] $$
$kA$ has the same order as $A$. In particular $(-1)A=-A$, the negative of $A$.
:::

```figure caption="Scalar multiplication: every element of $A$ is multiplied by the scalar 3."
fig = mateq(["$3A=3$", [["2", "−1"], ["0", "3"]], "$=$", [["3×2", "3×(−1)"], ["3×0", "3×3"]], "$=$", [["6", "−3"], ["0", "9"]]], fontsize=10.5, colw=1.05, scale=0.5)
```

::: example Scalar multiples
**Problem.** If $A=[(2,-1),(0,3)]$, find $3A$, $-A$ and $\frac{1}{2}A$.

**Solution.** Multiply every element by the scalar:
$$ 3A=[(6,-3),(0,9)],\qquad -A=[(-2,1),(0,-3)],\qquad \frac{1}{2}A=\left[\left(1,-\frac{1}{2}\right),\left(0,\frac{3}{2}\right)\right] $$
Notice that $A+(-A)=[(0,0),(0,0)]=O$, the additive inverse property.
:::

### Properties of scalar multiplication

For matrices $A$, $B$ of the same order and scalars $k$, $l$:

| Property | Statement |
|---|---|
| Distributive over matrix addition | $k(A+B)=kA+kB$ |
| Distributive over scalar addition | $(k+l)A=kA+lA$ |
| Associative | $k(lA)=(kl)A$ |
| Multiplying by 1 and by 0 | $1A=A$ and $0A=O$ |

::: example Combining scalar multiples
**Problem.** If $A=[(1,2),(3,4)]$ and $B=[(2,0),(-1,3)]$, find $2A+3B$ and $3A-2B$, and verify that $2(A+B)=2A+2B$.

**Solution.** $2A=[(2,4),(6,8)]$, $3B=[(6,0),(-3,9)]$, so
$$ 2A+3B=[(2+6,\ 4+0),(6-3,\ 8+9)]=[(8,4),(3,17)] $$
$3A=[(3,6),(9,12)]$ and $2B=[(4,0),(-2,6)]$, so
$$ 3A-2B=[(3-4,\ 6-0),(9+2,\ 12-6)]=[(-1,6),(11,6)] $$
For the property: $A+B=[(3,2),(2,7)]$, so $2(A+B)=[(6,4),(4,14)]$. Also $2A+2B=[(2+4,\ 4+0),(6-2,\ 8+6)]=[(6,4),(4,14)]$. They are equal ✓.
:::

::: example An equation with a scalar
**Problem.** Find $X$ if $2X-A=B$, where $A=[(1,2),(3,4)]$ and $B=[(5,0),(-1,6)]$.

**Solution.** Add $A$ to both sides, then multiply both sides by $\frac{1}{2}$:
$$ 2X=A+B=[(6,2),(2,10)] \quad\Longrightarrow\quad X=\frac{1}{2}[(6,2),(2,10)]=[(3,1),(1,5)] $$
Check: $2X-A=[(6,2),(2,10)]-[(1,2),(3,4)]=[(5,0),(-1,6)]=B$ ✓.
:::

::: example Unknowns with a scalar
**Problem.** Find $x$ and $y$ if $2[(x,3),(1,y)]+[(1,-2),(4,3)]=[(7,4),(6,9)]$.

**Solution.** $2[(x,3),(1,y)]=[(2x,6),(2,2y)]$. Adding, $[(2x+1,\ 4),(6,\ 2y+3)]=[(7,4),(6,9)]$.

So $2x+1=7$, giving $x=3$, and $2y+3=9$, giving $y=3$. The other two elements, $4=4$ and $6=6$, agree.
:::

::: example A price list in a row matrix
**Problem.** A stationery shop sells a pen for Rs 40, a copy for Rs 25 and a geometry box for Rs 120. Write the prices as a row matrix $P$ and find the new price matrix after a 10% increase.

**Solution.** $P=[(40,25,120)]$, a $1\times3$ row matrix. A 10% increase multiplies every price by $1.1$:
$$ 1.1P=[(1.1\times40,\ 1.1\times25,\ 1.1\times120)]=[(44,\ 27.5,\ 132)] $$
The new prices are Rs 44, Rs 27.50 and Rs 132.
:::

::: caution Multiply every element, not just one row
$3A$ multiplies **all** the elements of $A$ by 3. A common slip is to multiply only the first row, or only the first element, as you might when taking a factor out of a single number. Also, $kA$ is not the same as $A+k$: adding a number to a matrix is not defined at all.
:::

::: tip Check by one element
After a long calculation such as $3A-2B$, pick one position, say row 2, column 1, and compute it again on its own: $3a_{21}-2b_{21}$. If it matches your answer, the method is right; if not, you will find the slip in seconds.
:::

::: note Activity — the canteen matrix
With two friends, record for one week how many cups of tea, plates of chowmein and bottles of water the school canteen sells each day before and after the lunch break. (1) Write the morning sales as a matrix $M$ and the afternoon sales as a matrix $N$ (rows: days; columns: items). What is the order? (2) Find $M+N$, the total sales, and $N-M$; explain the negative entries. (3) If the canteen expects to sell 20% more next week, find $1.2(M+N)$. (4) Which type of matrix would you get if nothing was sold at all?
:::

### The matrices used in the practice questions

Some practice questions below refer to the matrices in this figure.

```figure caption="The matrices P, Q, R, S, T, U, V and W used in the practice questions."
fig, ax = plt.subplots(figsize=(5.2, 3.0))
M = '−'
items = [('P', [['2', M + '1'], ['0', '5']]), ('Q', [['3', '4'], [M + '2', '1']]), ('R', [['1', '0', '2'], ['3', M + '1', '4']]),
         ('S', [['4', '2'], ['2', '7']]), ('T', [['5', '0', '0'], ['0', '5', '0'], ['0', '0', '5']]),
         ('U', [['1', '2', '3'], ['0', '4', '5'], ['0', '0', '6']]), ('V', [['7', M + '3', '2']]), ('W', [['1'], ['0'], [M + '4']])]
cw, rh = 0.45, 0.4
for k, (name, rows) in enumerate(items):
    c, r = k % 4, k // 4
    cx, cy = 1.7 + 3.0*c, 3.3 - 2.0*r
    nr, nc = len(rows), len(rows[0])
    x, y = cx - nc*cw/2 + 0.25, cy - nr*rh/2
    matrix(ax, rows, x=x, y=y, fontsize=9.5, colw=cw, rowh=rh)
    ax.text(x - 0.35, cy, name + ' =', ha='right', va='center', fontsize=10)
ax.set_xlim(-0.2, 12.2); ax.set_ylim(0.3, 4.4); ax.axis('off')
fig.tight_layout(pad=0.2)
```

## Chapter summary

- A **matrix** is a rectangular array of numbers in rows and columns; a matrix with $m$ rows and $n$ columns has **order** $m\times n$ and $mn$ elements; $a_{ij}$ is the element in row $i$, column $j$.
- **Row** $1\times n$, **column** $m\times1$, **zero** (all 0), **rectangular** ($m\neq n$), **square** ($m=n$).
- In a square matrix: **diagonal** (zero off the leading diagonal), **scalar** (diagonal with equal diagonal elements), **unit** $I$ (scalar with 1s), **symmetric** ($a_{ij}=a_{ji}$), **upper/lower triangular** (zeros below/above the leading diagonal).
- **Equal matrices** have the same order and equal corresponding elements.
- $A\pm B=[a_{ij}\pm b_{ij}]$, possible **only for the same order**.
- Addition is closed, commutative and associative, with identity $O$ and inverse $-A$; subtraction is not commutative.
- $kA=[k\,a_{ij}]$; $k(A+B)=kA+kB$, $(k+l)A=kA+lA$, $k(lA)=(kl)A$, $1A=A$, $0A=O$.

## Practice questions

The matrices $P$, $Q$, $R$, $S$, $T$, $U$, $V$ and $W$ are those in the figure above.

**Group A — Objective (1 mark each)**

1. A matrix with 3 rows and 2 columns has order <span class="marks">[1]</span>
   (a) $2\times3$ (b) $3\times2$ (c) 6 (d) $3+2$
2. The number of elements in a matrix of order $4\times3$ is <span class="marks">[1]</span>
   (a) 7 (b) 12 (c) 43 (d) 1
3. In the matrix $R$, the element $r_{23}$ is <span class="marks">[1]</span>
   (a) 2 (b) 4 (c) $-1$ (d) 3
4. The matrix $V$ is a <span class="marks">[1]</span>
   (a) column matrix (b) row matrix (c) square matrix (d) zero matrix
5. The best name for the matrix $T$ is <span class="marks">[1]</span>
   (a) unit matrix (b) scalar matrix (c) row matrix (d) zero matrix
6. The matrix $S$ is <span class="marks">[1]</span>
   (a) symmetric (b) a unit matrix (c) a row matrix (d) lower triangular
7. The matrix $U$ is <span class="marks">[1]</span>
   (a) lower triangular (b) upper triangular (c) diagonal (d) scalar
8. If $[(x,2),(3,4)]=[(5,2),(3,4)]$, then $x$ is <span class="marks">[1]</span>
   (a) 2 (b) 3 (c) 4 (d) 5
9. $P+Q$ equals <span class="marks">[1]</span>
   (a) $[(5,3),(-2,6)]$ (b) $[(-1,-5),(2,4)]$ (c) $[(6,-4),(0,5)]$ (d) $[(5,4),(-2,6)]$
10. $2P$ equals <span class="marks">[1]</span>
    (a) $[(4,-2),(0,10)]$ (b) $[(4,-1),(0,5)]$ (c) $[(2,-1),(0,5)]$ (d) $[(4,1),(0,10)]$
11. Which pair of matrices can be added? <span class="marks">[1]</span>
    (a) $P$ and $R$ (b) $P$ and $Q$ (c) $V$ and $W$ (d) $R$ and $S$
12. The additive inverse of $P$ is <span class="marks">[1]</span>
    (a) $[(-2,1),(0,-5)]$ (b) $[(2,1),(0,5)]$ (c) $[(-2,-1),(0,-5)]$ (d) $[(\frac{1}{2},-1),(0,\frac{1}{5})]$

::: note Answers to Group A
**1.** (b) — rows first, then columns.
**2.** (b) — $4\times3=12$ elements.
**3.** (b) — row 2, column 3 of $R$ is 4.
**4.** (b) — $V$ has one row and three columns.
**5.** (b) — a diagonal matrix with every diagonal element equal to 5 (not 1, so not the unit matrix).
**6.** (a) — $s_{12}=s_{21}=2$.
**7.** (b) — all the elements below the leading diagonal are 0.
**8.** (d) — corresponding elements: $x=5$.
**9.** (a) — $[(2+3,\ -1+4),(0-2,\ 5+1)]$.
**10.** (a) — every element is doubled.
**11.** (b) — only $P$ and $Q$ have the same order, $2\times2$.
**12.** (a) — change the sign of every element: $-P$.
:::

**Group B — Short answer (2 marks each)**

1. Write the order of $R$ and its elements $r_{12}$ and $r_{21}$. <span class="marks">[2]</span>
2. Construct the $2\times2$ matrix $A=[a_{ij}]$ with $a_{ij}=2i+j$. <span class="marks">[2]</span>
3. Find $x$ and $y$ if $[(x+3,\ 4),(6,\ 2y)]=[(8,\ 4),(6,\ 10)]$. <span class="marks">[2]</span>
4. Find $P-Q$ and $Q-P$. <span class="marks">[2]</span>
5. Find $3Q-2P$. <span class="marks">[2]</span>
6. If $[(a,\ 3),(b,\ 5)]$ is symmetric and $a+b=7$, find $a$ and $b$. <span class="marks">[2]</span>
7. Find the matrix $X$ such that $X+P=Q$. <span class="marks">[2]</span>
8. Write the unit matrix of order 3 and the scalar matrix of order 2 whose diagonal elements are $-3$. <span class="marks">[2]</span>
9. Verify that $P+Q=Q+P$. <span class="marks">[2]</span>
10. If $A=[(4,-6),(2,8)]$, find $\frac{1}{2}A$ and $-A$. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $R$ has 2 rows and 3 columns, so its order is $2\times3$; $r_{12}=0$ and $r_{21}=3$.
**2.** $a_{11}=3$, $a_{12}=4$, $a_{21}=5$, $a_{22}=6$, so $A=[(3,4),(5,6)]$.
**3.** $x+3=8$ gives $x=5$; $2y=10$ gives $y=5$.
**4.** $P-Q=[(2-3,\ -1-4),(0+2,\ 5-1)]=[(-1,-5),(2,4)]$ and $Q-P=[(1,5),(-2,-4)]=-(P-Q)$.
**5.** $3Q=[(9,12),(-6,3)]$ and $2P=[(4,-2),(0,10)]$, so $3Q-2P=[(5,14),(-6,-7)]$.
**6.** Symmetric means $a_{12}=a_{21}$, so $b=3$; then $a=7-3=4$.
**7.** $X=Q-P=[(1,5),(-2,-4)]$. Check: $X+P=[(3,4),(-2,1)]=Q$ ✓.
**8.** $I=[(1,0,0),(0,1,0),(0,0,1)]$ and $[(-3,0),(0,-3)]$.
**9.** $P+Q=[(5,3),(-2,6)]$ and $Q+P=[(3+2,\ 4-1),(-2+0,\ 1+5)]=[(5,3),(-2,6)]$; they are equal.
**10.** $\frac{1}{2}A=[(2,-3),(1,4)]$ and $-A=[(-4,6),(-2,-8)]$.
:::

**Group C — Long answer (4 marks each)**

1. If $A=[(1,2),(3,4)]$, $B=[(5,-1),(0,2)]$ and $C=[(-2,3),(4,1)]$, verify that $(A+B)+C=A+(B+C)$. <span class="marks">[4]</span>
2. Find $x$, $y$ and $z$ if $[(x+y,\ 4),(z,\ x-y)]+[(1,\ -2),(3,\ 2)]=[(9,\ 2),(5,\ 4)]$. <span class="marks">[4]</span>
3. Two shops sell pens, copies and bags. In Baisakh their sales were $B=[(120,80,15),(95,60,20)]$ and in Jestha $J=[(140,70,18),(110,75,12)]$ (rows: shops; columns: pens, copies, bags). (i) Find the total sales of the two months. (ii) Find the change from Baisakh to Jestha and explain the negative entries. (iii) If the target for Asar is double the Jestha sales, find the target matrix. <span class="marks">[4]</span>
4. If $A=[(2,0),(-1,3)]$ and $B=[(2,4),(3,-1)]$, verify that $3(A+B)=3A+3B$ and find the matrix $X$ such that $2X-A=B$. <span class="marks">[4]</span>
5. Classify each of the matrices $P$, $Q$, $R$, $S$, $T$, $U$, $V$, $W$ by every type that applies to it. Then find $T-5I$, where $I$ is the unit matrix of order 3, and comment on the result. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** $A+B=[(6,1),(3,6)]$, so $(A+B)+C=[(4,4),(7,7)]$. $B+C=[(3,2),(4,3)]$, so $A+(B+C)=[(1+3,\ 2+2),(3+4,\ 4+3)]=[(4,4),(7,7)]$. The two sides are equal, so addition is associative here.
**2.** The left side is $[(x+y+1,\ 2),(z+3,\ x-y+2)]$. Equating: $x+y+1=9$, so $x+y=8$; $x-y+2=4$, so $x-y=2$; $z+3=5$, so $z=2$. Adding the first two, $2x=10$, so $x=5$ and $y=3$. The element $2=2$ agrees.
**3.** (i) $B+J=[(260,150,33),(205,135,32)]$. (ii) $J-B=[(20,-10,3),(15,15,-8)]$: the first shop sold 10 fewer copies and the second shop 8 fewer bags in Jestha; every other entry rose. (iii) $2J=[(280,140,36),(220,150,24)]$.
**4.** $A+B=[(4,4),(2,2)]$, so $3(A+B)=[(12,12),(6,6)]$. $3A=[(6,0),(-3,9)]$ and $3B=[(6,12),(9,-3)]$, so $3A+3B=[(12,12),(6,6)]$; verified. From $2X-A=B$: $2X=A+B=[(4,4),(2,2)]$, so $X=[(2,2),(1,1)]$. Check: $2X-A=[(4-2,\ 4-0),(2+1,\ 2-3)]=[(2,4),(3,-1)]=B$ ✓.
**5.** $P$: square, upper triangular (its element below the diagonal is 0). $Q$: square. $R$: rectangular, $2\times3$. $S$: square, symmetric. $T$: square, diagonal, scalar, symmetric, upper and lower triangular. $U$: square, upper triangular. $V$: row, rectangular. $W$: column, rectangular. $T-5I=[(5,0,0),(0,5,0),(0,0,5)]-[(5,0,0),(0,5,0),(0,0,5)]=O$, the zero matrix; so $T=5I$: every scalar matrix is a scalar multiple of the unit matrix.
:::
