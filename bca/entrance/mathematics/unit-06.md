---
subject: Mathematics
grade: BCA
unit: 6
title: Matrices and Determinants
hours: 2
area: Algebra
---

Matrices carry about two questions: the order of a matrix or a product, a 2 × 2 determinant or inverse, and one property question (singular, symmetric, effect of scalar multiplication). The Dean's Office model asks "how many elements in a single column of a 5 × 3 matrix". Matrices are written here in rows as `[[a, b], [c, d]]`.

::: key What the paper asks from this chapter
- **Order and operations**: $m\times n$, when $AB$ exists and its order, transpose rule.
- **Determinants**: $ad-bc$, 3 × 3 expansion, row properties, $|kA|=k^n|A|$.
- **Inverse**: exists iff $|A|\ne0$; 2 × 2 formula; $|A^{-1}|=\frac{1}{|A|}$, $|\text{adj}A|=|A|^{n-1}$.
- **Linear systems**: Cramer's rule and the matrix method.
:::

## 6.1 Types, order and operations on matrices

- A matrix with $m$ rows and $n$ columns has order $m\times n$ and $mn$ elements; each column has $m$ elements.
- Types: row, column, square, diagonal, scalar, identity $I$, zero (null), symmetric ($A=A^T$), skew-symmetric ($A=-A^T$, diagonal zero).
- $A+B$ needs equal order. $AB$ exists only if columns of $A$ = rows of $B$; order of $AB$ is (rows of $A$)×(columns of $B$). In general $AB\ne BA$; $AI=IA=A$.
- $(A+B)^T=A^T+B^T$ and $(AB)^T=B^TA^T$.

```photogrid label="6.1" cols="2" ratio="1.0" caption="The two mathematicians who named the subject. (a) Arthur Cayley (1821-1895), who in 1858 published the first theory of matrices and proved that a matrix satisfies its own characteristic equation. (b) James Joseph Sylvester (1814-1897), who coined the word matrix in 1850 (Latin for womb or mould: a matrix produces determinants)."
@ photo id="bcamath/cayley" cap="Arthur Cayley, theory of matrices (1858)"
focus 0.5 0.3
@ photo id="bcamath/sylvester" cap="J. J. Sylvester, who named the matrix"
focus 0.5 0.3
```

```svgfig label="6.1" caption="Matrix multiplication row by column, computed. A is 2 x 3 and B is 3 x 2, so AB exists and is 2 x 2: the entry in row i, column j is row i of A dotted with column j of B, e.g. 1 x 2 + 2 x 0 + 3 x 1 = 5. Below, for two 2 x 2 matrices AB and BA differ, so multiplication is NOT commutative."
def mm(A, B): return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
A = [[1, 2, 3], [4, 5, 6]]; B = [[2, 1], [0, 3], [1, 2]]; C = mm(A, B); assert C == [[5, 13], [14, 31]]
P = [[1, 2], [3, 4]]; Q = [[0, 1], [1, 0]]; assert mm(P, Q) == [[2, 1], [4, 3]] and mm(Q, P) == [[3, 4], [1, 2]] and mm(P, Q) != mm(Q, P)
f = Fig(780, 330)
def mat(x, y, M, hi=None, col="#dbeafe", w=34, h=30):
    f.box(x - 6, y - 4, len(M[0]) * w + 12, len(M) * h + 8, "", fill="#ffffff", stroke=SLATE, r=8)
    for i, row in enumerate(M):
        for j, v in enumerate(row):
            c = col
            if hi and (hi[0] == i or hi[1] == j): c = "#fde68a"
            if hi and hi[0] == i and hi[1] == j: c = "#bbf7d0"
            f.box(x + j * w + 2, y + i * h + 1, w - 4, h - 2, str(v), fill=c, stroke="#cbd5e1", size=12, bold=True, color=NAVY, r=3)
mat(30, 40, A, col="#dbeafe", hi=(0, -1)); f.text(150, 28, "A (2 x 3)", size=10.5, color=SLATE, bold=True)
f.text(168, 72, "x", size=16, color=NAVY, bold=True)
mat(190, 40, B, hi=(-1, 0), col="#dbeafe"); f.text(225, 28, "B (3 x 2)", size=10.5, color=SLATE, bold=True)
f.text(280, 72, "=", size=16, color=NAVY, bold=True)
mat(305, 40, C, hi=(0, 0), col="#f1f5f9"); f.text(340, 28, "AB (2 x 2)", size=10.5, color=SLATE, bold=True)
f.text(200, 150, "entry (1,1) = 1 x 2 + 2 x 0 + 3 x 1 = 5", size=11.5, color=RED, bold=True)
f.text(200, 174, "entry (1,2) = 1 x 1 + 2 x 3 + 3 x 2 = 13", size=10.5, color=SLATE)
f.text(200, 196, "inner sizes match (3 = 3); outer sizes give 2 x 2", size=10.5, color=TEAL, bold=True)
f.text(590, 28, "AB is not BA", size=11.5, color=NAVY, bold=True)
mat(440, 60, P); f.text(470, 52, "P", size=11, color=SLATE, bold=True); f.text(528, 92, "x", size=14, color=NAVY, bold=True); mat(550, 60, Q); f.text(582, 52, "Q", size=11, color=SLATE, bold=True)
mat(440, 150, mm(P, Q), col="#bbf7d0"); f.text(485, 142, "PQ", size=11, color=TEAL, bold=True)
mat(580, 150, mm(Q, P), col="#fecaca"); f.text(625, 142, "QP", size=11, color=RED, bold=True)
f.text(560, 234, "PQ = [[2,1],[4,3]]  but  QP = [[3,4],[1,2]]", size=10.5, color=RED, bold=True)
f.text(390, 276, "Remember: (AB)^T = B^T A^T and (AB)^-1 = B^-1 A^-1 (the order reverses)", size=11, color=NAVY, bold=True)
f.text(390, 300, "Also AB = 0 does not force A = 0 or B = 0", size=10.5, color=SLATE)
```

## 6.2 Determinants, minors and cofactors

- For `[[a, b], [c, d]]`, $|A|=ad-bc$. For a 3 × 3, expand along any row: $a_{11}C_{11}+a_{12}C_{12}+a_{13}C_{13}$ with cofactor $C_{ij}=(-1)^{i+j}M_{ij}$.
- A determinant is $0$ if two rows (or columns) are equal or proportional or a row is all zero. Swapping two rows changes the sign. A triangular matrix has $|A|=$ product of the diagonal.
- $|AB|=|A||B|$, $|A^T|=|A|$, and $|kA|=k^n|A|$ for order $n$.

```svgfig label="6.2" caption="What a determinant measures. The matrix M = [[3, 1], [1, 2]] sends the unit square (area 1) to a parallelogram of area |det M| = 3 x 2 - 1 x 1 = 5. A zero determinant would flatten the square onto a line, which is why such a matrix has no inverse. Right: the 3 x 3 determinant by cofactors, 2(12 - 2) - 0 + 1(1 - 3) = 18, checked with Sarrus' rule."
def det2(a, b, c, d): return a * d - b * c
M = [[3, 1], [1, 2]]; assert det2(3, 1, 1, 2) == 5
T = [[2, 0, 1], [1, 3, 2], [1, 1, 4]]
d3 = T[0][0] * det2(T[1][1], T[1][2], T[2][1], T[2][2]) - T[0][1] * det2(T[1][0], T[1][2], T[2][0], T[2][2]) + T[0][2] * det2(T[1][0], T[1][1], T[2][0], T[2][1])
sar = T[0][0] * T[1][1] * T[2][2] + T[0][1] * T[1][2] * T[2][0] + T[0][2] * T[1][0] * T[2][1] - T[0][2] * T[1][1] * T[2][0] - T[0][0] * T[1][2] * T[2][1] - T[0][1] * T[1][0] * T[2][2]
assert d3 == sar == 18
f = Fig(780, 320)
ax = Axes(f, 30, 20, 330, 270, (-1, 5), (-1, 4))
ax.grid(1, 1, size=10); ax.axes("x", "y")
img = lambda p: (3 * p[0] + 1 * p[1], 1 * p[0] + 2 * p[1])
sq = [(0, 0), (1, 0), (1, 1), (0, 1)]; pa = [img(p) for p in sq]
assert pa == [(0, 0), (3, 1), (4, 3), (1, 2)]
f.poly([(ax.X(x), ax.Y(y)) for x, y in pa], fill="#fde68a", stroke=AMBER, sw=2)
f.poly([(ax.X(x), ax.Y(y)) for x, y in sq], fill="#bfdbfe", stroke=NAVY, sw=2)
f.text(ax.X(2.4), ax.Y(1.8), "area 5", size=13, color=RED, bold=True); f.text(ax.X(0.5), ax.Y(0.5), "1", size=11, color=NAVY, bold=True)
f.text(ax.X(3.6), ax.Y(0.5), "(3, 1)", size=10.5, color=AMBER, bold=True); f.text(ax.X(4.2), ax.Y(3.2), "(4, 3)", size=10.5, color=AMBER, bold=True); f.text(ax.X(0.6), ax.Y(2.4), "(1, 2)", size=10.5, color=AMBER, bold=True)
f.text(570, 26, "3 x 3 determinant", size=11.5, color=NAVY, bold=True)
for i, row in enumerate(T):
    for j, v in enumerate(row):
        f.box(430 + j * 40, 44 + i * 32, 36, 28, str(v), fill=("#bbf7d0" if i == 0 else "#dbeafe"), stroke="#cbd5e1", size=12, bold=True, color=NAVY, r=3)
for j, t in enumerate(["expand along row 1:", "2 x (3x4 - 2x1) = 2 x 10 = 20", "- 0 x (1x4 - 2x1) = 0", "+ 1 x (1x1 - 3x1) = -2", "det = 20 + 0 - 2 = 18", "Sarrus: 24 + 0 + 1 - 3 - 4 - 0 = 18"]):
    f.text(580, 160 + j * 24, t, size=10.5, color=(RED if j == 4 else SLATE), anchor="start", bold=(j == 4))
f.text(580, 312, "", size=1)
```

## 6.3 Adjoint, inverse and linear systems

- $A^{-1}=\frac{\text{adj}A}{|A|}$ exists iff $|A|\ne0$ (non-singular). For 2 × 2 `[[a, b], [c, d]]`: $\text{adj}A=$ `[[d, -b], [-c, a]]`.
- $AA^{-1}=I$, $(AB)^{-1}=B^{-1}A^{-1}$, $|A^{-1}|=\frac{1}{|A|}$, $|\text{adj}A|=|A|^{n-1}$.
- **Cramer's rule** for $a_1x+b_1y=c_1$, $a_2x+b_2y=c_2$: $x=\frac{D_x}{D}$, $y=\frac{D_y}{D}$, $D=a_1b_2-a_2b_1$, with $D\ne0$.

```svgfig label="6.3" caption="Solving 2x + y = 7, x - y = 2 with the inverse. A = [[2, 1], [1, -1]] has det = -3, adj A = [[-1, -1], [-1, 2]] (swap the diagonal, negate the off-diagonal), so A^-1 = adj A / det = [[1/3, 1/3], [1/3, -2/3]]. Then X = A^-1 B = (3, 1), checked by A x A^-1 = I with exact fractions."
from fractions import Fraction as F
A = [[2, 1], [1, -1]]; B = [7, 2]; d = A[0][0] * A[1][1] - A[0][1] * A[1][0]; assert d == -3
adj = [[A[1][1], -A[0][1]], [-A[1][0], A[0][0]]]; assert adj == [[-1, -1], [-1, 2]]
inv = [[F(adj[i][j], d) for j in range(2)] for i in range(2)]
assert inv == [[F(1, 3), F(1, 3)], [F(1, 3), F(-2, 3)]]
prod = [[sum(A[i][k] * inv[k][j] for k in range(2)) for j in range(2)] for i in range(2)]; assert prod == [[1, 0], [0, 1]]
X = [sum(inv[i][k] * B[k] for k in range(2)) for i in range(2)]; assert X == [3, 1]
f = Fig(780, 320)
def mat(x, y, M, col="#dbeafe", w=48, h=34, s=12):
    f.box(x - 6, y - 4, len(M[0]) * w + 12, len(M) * h + 8, "", fill="#ffffff", stroke=SLATE, r=8)
    for i, row in enumerate(M):
        for j, v in enumerate(row): f.box(x + j * w + 2, y + i * h + 1, w - 4, h - 2, str(v), fill=col, stroke="#cbd5e1", size=s, bold=True, color=NAVY, r=3)
f.text(60, 24, "A", size=12, color=NAVY, bold=True); mat(30, 36, A)
f.text(175, 24, "adj A", size=12, color=NAVY, bold=True); mat(150, 36, adj, col="#fde68a")
f.text(310, 24, "A inverse = adj A / (-3)", size=12, color=NAVY, bold=True); mat(300, 36, [["1/3", "1/3"], ["1/3", "-2/3"]], col="#bbf7d0")
f.text(138, 82, "->", size=14, color=SLATE, bold=True); f.text(268, 82, "->", size=14, color=SLATE, bold=True)
f.text(390, 150, "X = A inverse B:", size=12, color=NAVY, bold=True)
mat(190, 170, [["1/3", "1/3"], ["1/3", "-2/3"]], col="#bbf7d0"); f.text(325, 205, "x", size=14, color=NAVY, bold=True)
mat(350, 170, [[7], [2]], col="#dbeafe", w=48); f.text(420, 205, "=", size=14, color=NAVY, bold=True); mat(445, 170, [[3], [1]], col="#fecaca", w=48)
f.text(390, 264, "x = 3, y = 1:  (1/3)(7) + (1/3)(2) = 3  and  (1/3)(7) - (2/3)(2) = 1", size=11, color=RED, bold=True)
f.text(390, 292, "A x A inverse = I (identity): checked with exact fractions", size=10.5, color=TEAL, bold=True)
f.text(640, 60, "Inverse exists only if det not 0", size=11, color=NAVY, bold=True)
for j, t in enumerate(["2 x 2: swap diagonal, negate the rest", "|adj A| = |A|^(n-1)", "A (adj A) = |A| I", "(A^-1)^-1 = A,  |A^-1| = 1/|A|", "|A| = 0: no inverse (singular)"]):
    f.text(560, 92 + j * 28, t, size=10.5, color=SLATE, anchor="start")
```

```svgfig label="6.4" caption="A matrix is a machine that moves points. The rotation matrix R = [[0, -1], [1, 0]] turns every point 90 degrees anticlockwise: (2, 1) goes to (-1, 2) and the triangle (0,0), (2,0), (2,1) turns into (0,0), (0,2), (-1,2). The reflection [[1, 0], [0, -1]] flips it in the x-axis. Both have determinant +1 or -1, so the area (1) does not change."
tri = [(0, 0), (2, 0), (2, 1)]
R = [[0, -1], [1, 0]]; Fl = [[1, 0], [0, -1]]
ap = lambda M, p: (M[0][0] * p[0] + M[0][1] * p[1], M[1][0] * p[0] + M[1][1] * p[1])
tr = [ap(R, p) for p in tri]; tf = [ap(Fl, p) for p in tri]
assert tr == [(0, 0), (0, 2), (-1, 2)] and tf == [(0, 0), (2, 0), (2, -1)]
ar = lambda t: abs((t[1][0] - t[0][0]) * (t[2][1] - t[0][1]) - (t[2][0] - t[0][0]) * (t[1][1] - t[0][1])) / 2
assert ar(tri) == ar(tr) == ar(tf) == 1 and R[0][0] * R[1][1] - R[0][1] * R[1][0] == 1 and Fl[0][0] * Fl[1][1] == -1
f = Fig(780, 320)
ax = Axes(f, 50, 20, 330, 270, (-3, 3), (-3, 3))
ax.grid(1, 1, size=10); ax.axes("x", "y")
for pts, fill, st in [(tri, "#bfdbfe", NAVY), (tr, "#fde68a", AMBER), (tf, "#bbf7d0", TEAL)]:
    f.poly([(ax.X(x), ax.Y(y)) for x, y in pts], fill=fill, stroke=st, sw=2)
f.text(ax.X(2.2), ax.Y(0.45), "T", size=12, color=NAVY, bold=True); f.text(ax.X(-0.9), ax.Y(1.2), "R T", size=12, color=AMBER, bold=True); f.text(ax.X(2.3), ax.Y(-0.6), "F T", size=12, color=TEAL, bold=True)
f.text(580, 40, "Common 2 x 2 transformations", size=11.5, color=NAVY, bold=True)
for j, (t, c) in enumerate([("rotation 90 deg: [[0,-1],[1,0]]", AMBER), ("(x, y) -> (-y, x),  det = 1", AMBER), ("reflection in x-axis: [[1,0],[0,-1]]", TEAL), ("(x, y) -> (x, -y),  det = -1", TEAL), ("scaling by 2: [[2,0],[0,2]], det = 4", NAVY), ("area is multiplied by |det|", RED), ("det = 0 flattens the plane: no inverse", RED)]):
    f.text(460, 76 + j * 30, t, size=10.5, color=c, anchor="start", bold=(c == RED))
```

## 6.4 Eight traps in matrices and determinants

Matrix questions reward a clear habit: check the order, then the sign, then the rule. These eight traps cover the model-paper style questions on products, determinants and inverses.

1. **Check the order before you multiply.** $A_{m\times n}B_{n\times p}$ is defined only if the columns of $A$ equal the rows of $B$, and the product is $m\times p$ (Fig 6.1). A $2\times3$ times a $3\times2$ gives $2\times2$, but a $2\times3$ times another $2\times3$ is undefined. Always write the orders beside the matrices first.
2. **$AB\neq BA$ in general.** Even when both products exist they are usually different, as $PQ$ and $QP$ show in Fig 6.1. So $(A+B)^2=A^2+AB+BA+B^2$, not $A^2+2AB+B^2$. The reversal laws are $(AB)^T=B^TA^T$ and $(AB)^{-1}=B^{-1}A^{-1}$.
3. **A zero product does not mean a zero factor.** $AB=0$ can happen with $A\neq0$ and $B\neq0$, for example $\begin{pmatrix}1&0\\0&0\end{pmatrix}\begin{pmatrix}0&0\\0&1\end{pmatrix}=0$. Likewise $AB=AC$ does not give $B=C$ unless $A$ is invertible. Do not cancel matrices as you cancel numbers.
4. **Only square matrices have determinants, and they obey set rules.** $|kA|=k^n|A|$ for an $n\times n$ matrix, so doubling a $2\times2$ multiplies the determinant by 4, not 2. Also $|AB|=|A||B|$ and $|A^T|=|A|$. Swapping two rows changes the sign, and two equal rows give zero (Fig 6.2).
5. **Cofactor signs follow a checkerboard.** The cofactor is $C_{ij}=(-1)^{i+j}M_{ij}$, so the signs start $+,-,+$ along the first row. The minor $M_{ij}$ has no sign of its own. When expanding, pick the row or column with the most zeros, as the zero in Fig 6.2 saved a product.
6. **The adjoint is the transpose of the cofactor matrix.** Many students forget the transpose. For a $2\times2$ matrix the shortcut is to swap the diagonal entries and negate the other two (Fig 6.3). The key identity is $A\,(\operatorname{adj}A)=|A|\,I$, and $|\operatorname{adj}A|=|A|^{n-1}$.
7. **An inverse exists only when $|A|\neq0$.** Then $A^{-1}=\frac{\operatorname{adj}A}{|A|}$, and $|A^{-1}|=\frac{1}{|A|}$. A matrix with determinant zero is singular and has no inverse, as when two rows are proportional. In Fig 6.2 a zero determinant would collapse the square onto a line.
8. **Solve $AX=B$ with $X=A^{-1}B$ in that order.** Writing $BA^{-1}$ is wrong because the product is not commutative. If $|A|=0$ the system has no unique solution: it has none or infinitely many. Cramer's rule gives each unknown as a ratio of determinants, $x=\frac{D_x}{D}$.

### 6.4.1 Worked checks

**Q. If $A=\begin{pmatrix}1&2&3\\4&5&6\end{pmatrix}$ and $B=\begin{pmatrix}2&1\\0&3\\1&2\end{pmatrix}$, find $AB$.**

**Answer.** $AB$ is $2\times2$. Row 1 by column 1: $1\cdot2+2\cdot0+3\cdot1=5$. Row 1 by column 2: $1+6+6=13$. Row 2 by column 1: $8+0+6=14$. Row 2 by column 2: $4+15+12=31$. So $AB=\begin{pmatrix}5&13\\14&31\end{pmatrix}$.

**Q. Evaluate $\begin{vmatrix}2&0&1\\1&3&2\\1&1&4\end{vmatrix}$ and say whether the matrix is invertible.**

**Answer.** Expand along row 1: $2(12-2)-0+1(1-3)=20-2=18$. Since $18\neq0$ the matrix is non-singular, so the inverse exists. Sarrus' rule gives the same value, $24+0+1-3-4-0=18$.

**Q. Solve $2x+y=7$ and $x-y=2$ using the inverse.**

**Answer.** $A=\begin{pmatrix}2&1\\1&-1\end{pmatrix}$, $|A|=-3$, $A^{-1}=\frac{1}{-3}\begin{pmatrix}-1&-1\\-1&2\end{pmatrix}$. Then $X=A^{-1}\begin{pmatrix}7\\2\end{pmatrix}=\frac{1}{-3}\begin{pmatrix}-9\\-3\end{pmatrix}=\begin{pmatrix}3\\1\end{pmatrix}$. So $x=3,y=1$, which agrees with Fig 6.3.

## Formula and fact sheet

| Item | Result |
|---|---|
| $2\times2$ determinant | $ad-bc$ |
| Product order | $(m\times n)(n\times p)=m\times p$ |
| $(AB)^T$, $(AB)^{-1}$ | $B^TA^T$, $B^{-1}A^{-1}$ |
| $\lvert kA\rvert$ | $k^n\lvert A\rvert$ |
| $\lvert \text{adj}A\rvert$ | $\lvert A\rvert^{n-1}$ |

## Chapter summary

- Order $m\times n$: $m$ rows, $n$ columns; a column holds $m$ elements.
- $AB$ exists only if inner orders match, and $AB\ne BA$ in general.
- A zero determinant means singular: no inverse, and a row dependency.
- $|kA|=k^n|A|$: the factor is raised to the order.
- Reverse the order for $(AB)^T$ and $(AB)^{-1}$.
- Use Cramer's rule when $D\ne0$.

## Practice questions

**Set A — Recall (20 questions)**

1. A matrix of order 5 × 3 has how many elements in a single column?
   (a) 5 (b) 3 (c) 4 (d) 15
2. The determinant of `[[2, 3], [1, 4]]` is
   (a) 11 (b) 7 (c) 5 (d) 1
3. The product of a 2 × 3 matrix and a 3 × 4 matrix has order
   (a) 3 × 3 (b) 2 × 4 (c) 4 × 2 (d) not defined
4. A square matrix whose determinant is zero is called
   (a) identity (b) symmetric (c) orthogonal (d) singular
5. For a square matrix $A$ of order $n$, $AI$ equals
   (a) $A$ (b) 0 (c) $I$ (d) $A^2$
6. The transpose of a 2 × 3 matrix has order
   (a) 2 × 3 (b) 3 × 2 (c) 2 × 2 (d) 3 × 3
7. $(AB)^T$ equals
   (a) $A^TB^T$ (b) $AB$ (c) $B^TA^T$ (d) $BA$
8. The inverse of a square matrix $A$ exists if and only if
   (a) $A$ is symmetric (b) $|A|=0$ (c) $A$ is null (d) $|A|\ne0$
9. If $A=$ `[[1, 2], [3, 4]]` and $B=$ `[[0, 1], [1, 0]]`, the element in row 2, column 1 of $A+B$ is
   (a) 3 (b) 4 (c) 5 (d) 1
10. The determinant of the 3 × 3 identity matrix is
    (a) 1 (b) 0 (c) 3 (d) 9
11. A square matrix is symmetric if
    (a) $A=-A^T$ (b) $A=A^{-1}$ (c) $|A|=1$ (d) $A=A^T$
12. If $A$ is 3 × 3 and $|A|=2$, then $|2A|$ is
    (a) 4 (b) 8 (c) 16 (d) 6
13. The determinant of a matrix with two identical rows is
    (a) 0 (b) 1 (c) $-1$ (d) 2
14. The inverse of the 2 × 2 matrix $2I$ is
    (a) $2I$ (b) $\frac{1}{2}I$ (c) $I$ (d) $-2I$
15. A matrix all of whose elements are zero is called a
    (a) identity matrix (b) scalar matrix (c) diagonal matrix (d) null matrix
16. The number of elements in a 3 × 4 matrix is
    (a) 7 (b) 10 (c) 12 (d) 34
17. The determinant of `[[1, 2], [2, 4]]` is
    (a) 4 (b) 0 (c) 8 (d) $-4$
18. In the adjoint of `[[a, b], [c, d]]`, the element in row 1, column 2 is
    (a) $-b$ (b) $b$ (c) $-c$ (d) $c$
19. The diagonal elements of a skew-symmetric matrix are
    (a) 1 (b) $-1$ (c) all equal (d) zero
20. $|A^{-1}|$ equals
    (a) $|A|$ (b) $-|A|$ (c) $\frac{1}{|A|}$ (d) $|A|^2$

::: note Answers and explanations — Set A
**1.** (a) — a 5 × 3 matrix has 5 rows, so each column holds 5 entries.
**2.** (c) — 2·4 − 3·1 = 5.
**3.** (b) — (2×3)(3×4) gives 2 × 4.
**4.** (d) — zero determinant means singular.
**5.** (a) — I is the multiplicative identity.
**6.** (b) — rows and columns swap.
**7.** (c) — the order reverses.
**8.** (d) — |A| = 0 means no inverse.
**9.** (b) — row 2, column 1: 3 + 1 = 4.
**10.** (a) — diagonal product 1·1·1.
**11.** (d) — (a) defines skew-symmetric.
**12.** (c) — 2³ × 2 = 16, not 2 × 2 = 4.
**13.** (a) — equal rows make the determinant vanish.
**14.** (b) — (2I)(½I) = I.
**15.** (d) — null or zero matrix.
**16.** (c) — 3 × 4 = 12.
**17.** (b) — 1·4 − 2·2 = 0, rows proportional.
**18.** (a) — adj has −b in the top right.
**19.** (d) — aᵢᵢ = −aᵢᵢ forces 0.
**20.** (c) — |A||A⁻¹| = |I| = 1.
:::

**Set B — Understanding (12 questions)**

1. If the determinant of `[[x, 2], [3, 4]]` is $-2$, then $x$ is
   (a) 3 (b) 2 (c) $-1$ (d) 1
2. For $A=$ `[[1, 2], [3, 4]]`, the element in row 1, column 1 of $A^2$ is
   (a) 1 (b) 7 (c) 10 (d) 15
3. For $A=$ `[[1, 2], [0, 1]]` and $B=$ `[[1, 0], [3, 1]]`, the element in row 2, column 1 of $AB$ is
   (a) 3 (b) 7 (c) 1 (d) 0
4. In the inverse of `[[3, 1], [5, 2]]`, the element in row 1, column 2 is
   (a) 1 (b) 5 (c) $-1$ (d) 3
5. The matrix `[[k, 2], [3, 6]]` is singular when $k$ equals
   (a) 0 (b) 2 (c) 3 (d) 1
6. If $A$ is 3 × 3 and $|A|=5$, then $|\text{adj}A|$ is
   (a) 25 (b) 5 (c) 125 (d) 15
7. If $A$ is 3 × 2 and $B$ is 2 × 3, the order of $AB$ is
   (a) 2 × 2 (b) 3 × 2 (c) 3 × 3 (d) 2 × 3
8. For the system $x+y=5$, $x-y=1$, the value of $x$ is
   (a) 2 (b) 3 (c) 4 (d) 1
9. The determinant of `[[2, 5, 1], [0, 3, 7], [0, 0, 4]]` is
   (a) 24 (b) 14 (c) 9 (d) 0
10. If $A$ is 2 × 2 with $|A|=3$, then $|3A|$ is
    (a) 9 (b) 81 (c) 6 (d) 27
11. The cofactor of the element in row 1, column 2 of `[[1, 2], [3, 4]]` is
    (a) 3 (b) $-3$ (c) 4 (d) $-4$
12. If `[[a, 0], [0, a]]` squared equals $I$, a possible value of $a$ is
    (a) 0 (b) 2 (c) $-1$ (d) 3

::: note Answers and explanations — Set B
**1.** (d) — 4x − 6 = −2, x = 1.
**2.** (b) — 1·1 + 2·3 = 7.
**3.** (a) — row 2 of A is (0, 1); column 1 of B is (1, 3); 0 + 3 = 3.
**4.** (c) — |A| = 1; inverse is `[[2, -1], [-5, 3]]`.
**5.** (d) — 6k − 6 = 0, k = 1.
**6.** (a) — |A|^(3−1) = 25.
**7.** (c) — (3×2)(2×3) = 3 × 3, while BA would be 2 × 2.
**8.** (b) — adding the equations gives 2x = 6.
**9.** (a) — triangular: 2·3·4 = 24.
**10.** (d) — 3² × 3 = 27.
**11.** (b) — C₁₂ = −(minor 3) = −3.
**12.** (c) — a² = 1, so a = ±1; only −1 is listed.
:::

**Set C — Application (8 questions)**

1. Solving $2x+3y=8$ and $x+y=3$ by Cramer's rule gives $x+2y$ equal to
   (a) 4 (b) 5 (c) 6 (d) 3
2. If $A$ is a 3 × 3 matrix with $|A|=-2$, then $|A^{-1}|$ is
   (a) 2 (b) $-2$ (c) $\frac{1}{2}$ (d) $-\frac{1}{2}$
3. If $A=$ `[[1, 1], [0, 1]]`, the element in row 1, column 2 of $A^3$ is
   (a) 3 (b) 1 (c) 2 (d) 6
4. The determinant of `[[1, 2, 3], [4, 5, 6], [7, 8, 9]]` is
   (a) 1 (b) 45 (c) 0 (d) $-6$
5. For $A=$ `[[2, 1], [1, 1]]`, the element in row 1, column 1 of $A^{-1}$ is
   (a) 2 (b) $-1$ (c) $\frac{1}{2}$ (d) 1
6. The product of `[[1, 2], [3, 4]]` and the column `[[1], [1]]` is a column whose entries add up to
   (a) 7 (b) 10 (c) 3 (d) 14
7. If the determinant of `[[x, 2], [3, x]]` is 3, a possible value of $x$ is
   (a) 9 (b) 6 (c) 3 (d) 0
8. If $A$ is the 2 × 2 matrix with $a_{ij}=i+j$, then $|A|$ is
   (a) $-1$ (b) 1 (c) 0 (d) 17

::: note Answers and explanations — Set C
**1.** (b) — D = −1, Dₓ = −1, so x = 1; y = 2 and x + 2y = 5.
**2.** (d) — 1/|A| = −1/2.
**3.** (a) — each multiplication adds 1 to the corner entry.
**4.** (c) — rows are in AP, so row 3 − row 2 = row 2 − row 1.
**5.** (d) — |A| = 1 and adj has d = 1 at the top left.
**6.** (b) — the column is (3, 7).
**7.** (c) — x² − 6 = 3 gives x = ±3.
**8.** (a) — `[[2, 3], [3, 4]]`: 8 − 9 = −1.
:::
