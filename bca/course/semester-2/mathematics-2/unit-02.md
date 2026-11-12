---
subject: Mathematics II
grade: BCA Semester 2
unit: 2
title: Systems of Linear Equations
area: BCA 154 · Mathematics II · Unit 2
---

Systems of linear equations appear everywhere: balancing circuits, fitting curves, balancing chemical equations, solving for the weights in a model. This unit gives the systematic method (Gaussian elimination), the theory of when solutions exist (rank), and the alternatives (Cramer's rule, inverse).

::: key What this unit gives you
- Matrix form $A X = B$; augmented matrix; row-echelon forms.
- Gaussian and Gauss–Jordan elimination with worked examples.
- Rank and the consistency test: unique, infinitely many, or no solution.
- Cramer's rule; homogeneous systems; computational cost.
:::

## 2.1 Systems and their solutions

A system of *m* linear equations in *n* unknowns can be written **$A X = B$**, where A is the coefficient matrix, X the unknowns, B the right-hand side. The **augmented matrix** is [A | B]. Geometrically, in two variables each equation is a line (unique solution: lines meet at a point; none: parallel; infinitely many: the same line); in three variables each equation is a plane.

**Elementary row operations** (do not change the solution set): swap two rows; multiply a row by a non-zero constant; add a multiple of one row to another.

## 2.2 Gaussian elimination

**Row echelon form**: all-zero rows at the bottom; each leading entry (pivot) is to the right of the one above. **Reduced** row echelon form (Gauss–Jordan): pivots are 1 and are the only non-zero entry in their column. Method: use a pivot to clear the entries below it (forward elimination), then solve upward (**back-substitution**).

::: example Worked example: unique solution

$$x + y + z = 6 ,\  2 x - y + z = 3 ,\  x + 2 y - z = 2$$

Augmented $\begin{bmatrix} 1 & 1 & 1 \mid 6 \\ 2 & - 1 & 1 \mid 3 \\ 1 & 2 & - 1 \mid 2 \end{bmatrix}$.

$R_{2} \to R_{2} - 2 R_{1}$: [0, −3, −1 | −9]. $R_{3} \to R_{3} - R_{1}$: [0, 1, −2 | −4].

Swap $R_{2}$ and $R_{3}$: [0, 1, −2 | −4], [0, −3, −1 | −9]. $R_{3} \to R_{3} + 3 R_{2}$: [0, 0, −7 | −21].

Back-substitute: $z = 3 ;\  y - 2 (3) = - 4 \Rightarrow y = 2 ;\  x + 2 + 3 = 6 \Rightarrow x = 1$. **$(x ,\  y ,\  z) = (1 ,\  2 ,\  3)$.** Check in the 2nd equation: $2 - 2 + 3 = 3$ ✓.
:::

::: example Worked example: infinitely many solutions
$x + y + z = 3 ,\  x - y = 1$. Augmented $\begin{bmatrix} 1 & 1 & 1 \mid 3 \\ 1 & - 1 & 0 \mid 1 \end{bmatrix} \to R_{2} - R_{1}$: [0, −2, −1 | −2]. So $y = 1 - \frac{z}{2}$ (from $- 2 y - z = - 2$), and $x = 1 + y = 2 - \frac{z}{2}$. Let $z = t ( a$ **free variable**): **$(x ,\  y ,\  z) = \left( 2 - \frac{t}{2} ,\  1 - \frac{t}{2} ,\  t \right)$**, a line of solutions. Two equations in three unknowns can never have a unique solution.
:::

::: example Worked example: no solution
$x + y = 1 ,\  2 x + 2 y = 3$. $R_{2} - 2 R_{1}$: [0, 0 | 1], i.e. $0 = 1$, a contradiction. **Inconsistent**: the lines are parallel.
:::

## 2.3 Rank and consistency

The **rank** of a matrix is the number of non-zero rows in its echelon form (the number of pivots), i.e. the number of independent rows (equal to the number of independent columns).

::: example Worked example
$A = \begin{bmatrix} 1 & 2 & 3 \\ 2 & 4 & 6 \\ 1 & 0 & 1 \end{bmatrix}$: $R_{2} - 2 R_{1} = [0 ,\  0 ,\  0] ;\  R_{3} - R_{1} = [0 ,\  - 2 ,\  - 2]$. Two non-zero rows, so **rank $A = 2$**. (Row 2 is twice row 1.)
:::

**Rouché–Capelli theorem** for $A X = B$ with *n* unknowns:

| Condition | Result |
|---|---|
| rank A < rank [A \| B] | **inconsistent** (no solution) |
| rank A = rank [A \| $B ] = n$ | **unique** solution |
| rank A = rank [A \| $B ] = r < n$ | **infinitely many**, with $n - r$ free parameters |

**Homogeneous systems $A X = 0$** always have the trivial solution $X = 0$; a non-trivial solution exists iff rank $A < n$, equivalently (for square $A ) \det A = 0$. Example: $x + y = 0 ,\  2 x + 2 y = 0$ has the non-trivial solutions $(t ,\  - t)$.

**Square system** with $\det A \neq 0$: the unique solution $X = A^{-1} B$.

## 2.4 Cramer's rule

For a square system with $\det A \neq 0$, **$x_{i} = \frac{\det A_{i}}{\det A}$**, where $A_{i}$ is A with column *i* replaced by B.

::: example Worked example
$2 x + y = 5 ,\  x - y = 1$. $\det A = - 2 - 1 = - 3$. $A_{x} = \begin{bmatrix} 5 & 1 \\ 1 & - 1 \end{bmatrix}$: $\det = - 5 - 1 = - 6$, so $x = - 6 / - 3$ = **2**. $A_{y} = \begin{bmatrix} 2 & 5 \\ 1 & 1 \end{bmatrix}$: $\det = 2 - 5 = - 3$, so *y* = **1**.
:::

Cramer's rule is useful for small systems and for theory (it shows the solution depends continuously on the data); it is **far too slow** for large ones: it needs $n + 1$ determinants, each about $n^{3}$ operations or worse by cofactors, whereas elimination costs about $\left( \frac{2}{3} \right) n^{3}$ operations in total. For $n = 1000$ that is about $6.7 \times 10^{8}$ operations: a fraction of a second.

## 2.5 Applications and numerical issues

- **Curve fitting:** find the parabola $y = a x^{2} + b x + c$ through (1, 2), (2, 3), (3, 6): $a + b + c = 2 ,\  4 a + 2 b + c = 3 ,\  9 a + 3 b + c = 6$. Subtracting: $3 a + b = 1$ and $5 a + b = 3 \Rightarrow a = 1 ,\  b = - 2 ,\  c = 3$. **$y = x^{2} - 2 x + 3$.**
- **Balancing a chemical equation:** $C_{2} H_{6} + O_{2} \to C O_{2} + H_{2} O$: unknowns for each coefficient, carbon: $2 a = c$; hydrogen: $6 a = 2 d$; oxygen: $2 b = 2 c + d$. With $a = 2$: $c = 4 ,\  d = 6 ,\  b = 7$. **$2 C_{2} H_{6} + 7 O_{2} \to 4 C O_{2} + 6 H_{2} O$.**
- **Circuits (Kirchhoff):** current and voltage laws give linear systems in the currents.
- **Networks and traffic flow:** conservation at each node gives a system, usually with free variables.
- **Partial pivoting:** choose the largest available pivot in a column to limit rounding error. A system like 0.0001x + $y = 1 ,\  x + y = 2$ solved without pivoting in low precision can give badly wrong *x*. **Ill-conditioned** systems (nearly parallel lines or planes) amplify small data errors; the **condition number** measures this.
- **LU decomposition:** factor $A = L U$ (lower × upper triangular) once, then solve many right-hand sides cheaply; **least squares** solves overdetermined systems (more equations than unknowns) by $A^{T} A X = A^{T} B$, the basis of linear regression.

## 2.6 Three pictures of a linear system

Every system of two equations in two unknowns is a pair of lines, and the lines can meet in exactly three ways (Figure 2.1). Rank says which: **rank A = rank [A | *b*] = number of unknowns** gives one solution; **rank A = rank [A | *b*] < unknowns** gives infinitely many; **rank A < rank [A | *b*]** gives none. The same trichotomy holds for three planes in space and for systems with thousands of unknowns.

```svgfig label="2.1" caption="Three outcomes for two equations. (a) $x + y = 2$ and $x - y = 0$ cross at (1, 1): rank 2 = rank 2, one solution. (b) $x + y = 2$ and $x + y = 2.5$ are parallel: rank $A = 1$ but rank [A|b] = 2, no solution. (c) $x + y = 2$ and $2 x + 2 y = 4$ are the same line: rank 1 = rank $1 < 2$, infinitely many solutions."
f = Fig(580, 205)
for k, (title, l2, note) in enumerate([("(a) unique", lambda t: t, "(1, 1)"), ("(b) none", lambda t: 2.5 - t, "parallel"), ("(c) infinite", lambda t: 2 - t, "same line")]):
    ax = Axes(f, 14 + k * 192, 28, 168, 150, (-1, 4), (-1, 4))
    ax.grid(1, 1, labels=False)
    ax.curve(lambda t: 2 - t, -1, 4, color=NAVY, sw=2.4)
    ax.curve(l2, -1, 4, color=RED, sw=2.4, dash=(k == 2))
    if k == 0:
        ax.pt(1, 1, "(1, 1)", dx=8, dy=-10)
    f.text(98 + k * 192, 16, title, size=11, color=NAVY, bold=True)
    f.text(98 + k * 192, 194, note, size=10.5, color=SLATE, italic=True)
```

## 2.7 Eight uses of linear systems

1. **Electric circuits.** Kirchhoff's laws turn a network of resistors into a system of linear equations in the currents. Engineers solve it to size wires and fuses. The Nepal Electricity Authority's load-flow studies are huge systems of this kind.
2. **Traffic and network flow.** The cars entering and leaving each junction must balance, which gives one equation per junction. Solving the system shows the flow on every road. Ring Road planning in Kathmandu uses the same idea.
3. **Balancing chemical equations.** The number of atoms of each element on both sides must match, giving a linear system for the coefficients. The solution gives the smallest whole numbers. Chemistry software does this automatically.
4. **Diet and mixing problems.** A feed mix must supply given amounts of protein, fat and minerals from several ingredients. The unknowns are the quantities. A dairy cooperative uses this to design cattle feed at the lowest cost.
5. **Curve fitting.** To pass a quadratic through three measured points, write $y = a x^{2} + b x + c$ for each point and solve for $a ,\  b ,\  c$. Sensors and calibration charts use this daily.
6. **GPS positioning.** Distances to several satellites give equations whose solution is your position and clock error. Your phone solves such a system many times a second.
7. **Economic planning.** An input-output model asks how much each industry must produce so that supply meets demand. This is a linear system with a matrix of industry links. Planners solve it with Gaussian elimination.
8. **Computer graphics and simulation.** Finding where a ray meets a plane, or the shape of a loaded bridge in a simulation, leads to linear systems with thousands of unknowns. Computers solve them with the same elimination steps you learn here, tuned for speed.

```photogrid label="2.1" cols="2" ratio="1.2" caption="Elimination is cheap, cofactors are not. (a) Carl Friedrich Gauss, whose name is attached to the method of elimination (it was known in China two thousand years earlier, in the Nine Chapters). (b) The system $2 x + y - z = 8 ,\  - 3 x - y + 2 z = - 11 ,\  - 2 x + y + 2 z = - 3$ is reduced to triangular form by R2 + $\left( \frac{3}{2} \right) R 1$ and R3 + R1, then R3 - 4R2, giving $z = - 1$, then $y = 3$, then $x = 2$ by back substitution, all checked in exact fractions. Counting every multiplication and division, elimination on an $n x n$ system costs $\frac{n^{3} + 3 n^{2} - n}{3}$ operations: 17 for $n = 3$ and 430, 3,060, 22,920, 177,040 for $n = 10 ,\  20 ,\  40 ,\  80$. Doubling *n* multiplies the cost by about 8."
@ photo id="bcamath/gauss" cap="Carl Friedrich Gauss"
fit 1.2
focus 0.5 0.4
@ svg cap="Gaussian elimination: one example and its cost"
from fractions import Fraction as Fr
M = [[Fr(2), Fr(1), Fr(-1), Fr(8)], [Fr(-3), Fr(-1), Fr(2), Fr(-11)], [Fr(-2), Fr(1), Fr(2), Fr(-3)]]
S0 = [r[:] for r in M]
def addrow(M, i, k, c): M[i] = [a + c * b for a, b in zip(M[i], M[k])]
addrow(M, 1, 0, Fr(3, 2)); addrow(M, 2, 0, Fr(1)); S1 = [r[:] for r in M]
addrow(M, 2, 1, Fr(-4)); S2 = [r[:] for r in M]
z = S2[2][3] / S2[2][2]; y = (S2[1][3] - S2[1][2] * z) / S2[1][1]; x = (S2[0][3] - S2[0][1] * y - S2[0][2] * z) / S2[0][0]
assert (x, y, z) == (2, 3, -1) and S1[1] == [0, Fr(1, 2), Fr(1, 2), 1] and S2[2] == [0, 0, -1, 1]
def count(n):
    c = 0
    for k in range(n - 1):
        for i in range(k + 1, n): c += 1 + (n - k)
    for i in range(n - 1, -1, -1): c += (n - 1 - i) + 1
    return c
cs = {n: count(n) for n in (3, 10, 20, 40, 80)}
assert all(cs[n] == (n ** 3 + 3 * n ** 2 - n) // 3 for n in cs) and cs[3] == 17 and cs[10] == 430 and cs[80] == 177040
f = Fig(300, 240)
def show(x, y, S, title):
    f.text(x + 48, y - 8, title, size=10.5, color=NAVY, bold=True)
    for i in range(3):
        for j in range(4):
            v = S[i][j]
            f.box(x + j * 24, y + i * 20, 24, 20, str(v), fill=(SAND if j == 3 else BLUE), stroke=(AMBER if j == 3 else NAVY), size=10.5, r=0)
show(4, 22, S0, "start"); show(102, 22, S1, "R2+3/2R1, R3+R1"); show(200, 22, S2, "R3-4R2")
f.text(150, 104, "back substitution: z = -1, y = 3, x = 2", size=10.5, color=TEAL, bold=True)
f.text(10, 128, "n", size=10.5, color=SLATE, bold=True, anchor="start"); f.text(150, 128, "operations (mult + div)", size=10.5, color=SLATE, bold=True)
mx = cs[80]
for i, n in enumerate((10, 20, 40, 80)):
    y = 138 + i * 22
    f.text(10, y + 9, str(n), size=10.5, color=SLATE, anchor="start", vmid=True)
    w = max(3, cs[n] / mx * 190)
    f.box(40, y, w, 18, "", fill=MINT, stroke=TEAL, r=2)
    f.text(40 + w + 6, y + 9, f"{cs[n]:,}", size=10.5, color=TEAL, bold=True, anchor="start", vmid=True)
f.text(150, 236, "doubling n costs about 8 times more", size=10.5, color=SLATE)
```

```photogrid label="2.2" cols="2" ratio="1.2" caption="A circuit is a linear system. (a) A resistor circuit built on a breadboard: Kirchhoff's voltage law gives one equation for each loop. (b) Two loops share a 6 ohm resistor. Loop 1 (12 V battery, 2 ohm, shared 6 ohm): 8 I1 - 6 I2 = 12. Loop 2 (6 V battery in opposition, 3 ohm, shared 6 ohm): -6 I1 + 9 I2 = -6. The determinant is 8 $x 9 - 36 = 36$, so Cramer's rule gives I1 = $\frac{72}{36} = 2$ A and I2 = $\frac{24}{36} = \frac{2}{3} A$, and the shared resistor carries I1 - I2 = $\frac{4}{3} A$. Energy balances exactly: the 12 V battery supplies 24 W, the three resistors dissipate $8 + \frac{4}{3} + \frac{32}{3} = 20 W$ and the second battery absorbs 4 W (it is being charged)."
@ photo id="bcamath/breadboard" cap="Resistors on a breadboard"
fit 1.2
focus 0.5 0.5
@ svg cap="Two-loop circuit solved with Cramer's rule"
from fractions import Fraction as Fr
a, b, c, d, e, g = Fr(8), Fr(-6), Fr(-6), Fr(9), Fr(12), Fr(-6)
D = a * d - b * c
I1 = (e * d - b * g) / D; I2 = (a * g - e * c) / D; I3 = I1 - I2
assert D == 36 and I1 == 2 and I2 == Fr(2, 3) and I3 == Fr(4, 3)
P1 = 12 * I1; Pr = 2 * I1 ** 2 + 3 * I2 ** 2 + 6 * I3 ** 2; P2 = 6 * I2
assert P1 == 24 and Pr == 20 and P2 == 4 and P1 == Pr + P2
f = Fig(300, 240)
for (x1, y1, x2, y2) in [(30, 24, 270, 24), (30, 124, 270, 124), (30, 24, 30, 124), (270, 24, 270, 124), (150, 24, 150, 124)]:
    f.line(x1, y1, x2, y2, color=SLATE, sw=1.8)
f.box(14, 62, 32, 24, "12 V", fill=SAND, stroke=AMBER, size=10.5, bold=True, r=3)
f.box(254, 62, 32, 24, "6 V", fill=SAND, stroke=AMBER, size=10.5, bold=True, r=3)
f.box(66, 12, 48, 24, "2 ohm", fill=BLUE, stroke=NAVY, size=10.5, bold=True, r=3)
f.box(186, 12, 48, 24, "3 ohm", fill=BLUE, stroke=NAVY, size=10.5, bold=True, r=3)
f.box(126, 62, 48, 24, "6 ohm", fill=BLUE, stroke=NAVY, size=10.5, bold=True, r=3)
f.text(90, 78, "I1 = 2 A", size=10.5, color=TEAL, bold=True); f.text(210, 78, "I2 = 2/3 A", size=10.5, color=RED, bold=True)
f.text(150, 112, "I1 - I2 = 4/3 A", size=10.5, color=NAVY, bold=True)
f.text(150, 150, "8 I1 - 6 I2 = 12;  -6 I1 + 9 I2 = -6", size=10.5, color=SLATE)
f.text(150, 170, "det = 36, I1 = 72/36, I2 = 24/36", size=10.5, color=SLATE)
f.text(150, 196, "battery 24 W = resistors 20 W + charging 4 W", size=10.5, color=NAVY, bold=True)
f.text(150, 216, "all values exact fractions", size=10.5, color=SLATE)
```

## Formula and fact sheet

- $A X = B$; augmented [A | B]; three row operations.
- Rank = number of pivots. rank A < rank [A | B]: none; = *n*: unique; < *n*: infinite with $n - r$ parameters.
- Homogeneous: non-trivial solutions iff rank < $n ( \det = 0$ when square).
- Cramer: $x_{i} = \frac{\det A_{i}}{\det A}$. Gaussian elimination ≈ $\left( \frac{2}{3} \right) n^{3}$ operations.

## Chapter summary

- Elimination reduces any system to echelon form and then solves by back-substitution.
- Rank decides the number of solutions; free variables parametrise infinite families.
- Cramer's rule and inverses give formulas but elimination is the practical method.
- Applications range from curve fitting to chemistry, circuits and regression.

## Practice

1. Solve by Gaussian elimination: $x + 2 y + z = 8 ,\  2 x + y - z = 1 ,\  x - y + 2 z = 5$.
2. Solve $x + y - z = 1 ,\  2 x + 2 y - 2 z = 2 ,\  x - y + z = 3$ and describe the solution set.
3. For what values of *k* does $x + y = 2 ,\  2 x + k y = 5$ have no solution? A unique one?
4. Find the rank of $\begin{bmatrix} 1 & 2 & 3 & 4 \\ 2 & 4 & 6 & 8 \\ 1 & 0 & 1 & 0 \end{bmatrix}$.
5. Solve by Cramer's rule: $3 x + 2 y = 7 ,\  x - y = 1$.
6. Find all solutions of the homogeneous system $x + 2 y + 3 z = 0 ,\  2 x + 4 y + 6 z = 0$.
7. Fit $y = a x^{2} + b x + c$ through (0, 1), (1, 4), (2, 9).
8. Balance: Fe + $O_{2} \to F e_{2} O_{3}$.
9. Determine whether the system $x + y = 2 ,\  x - y = 0 ,\  2 x + y = 3$ is consistent.
10. A 400-equation system takes 1 *s* on a computer. Estimate the time for 4000 equations.

::: note Answers and worked solutions
**1.** $R_{2} - 2 R_{1}$: [0, −3, −3 | $- 15 ] ;\  R_{3} - R_{1}$: [0, −3, 1 | −3]. $R_{3} - R_{2}$: [0, 0, 4 | $12 ] \Rightarrow z = 3 ;\  - 3 y - 9 = - 15 \Rightarrow y = 2 ;\  x + 4 + 3 = 8 \Rightarrow x = 1$. **(1, 2, 3).**

**2.** Equation 2 is twice equation 1. Adding eqs 1 and 3: $2 x = 4 \Rightarrow x = 2$; then $2 + y - z = 1 \Rightarrow y - z = - 1$. Solutions **$(2 ,\  t - 1 ,\  t)$**: infinitely many (one free parameter).

**3.** Eliminate: $R_{2} - 2 R_{1} = [ 0 ,\  k - 2$ | 1]. If $k = 2$: $0 = 1$, **no solution**. If $k \neq 2$: **unique** solution.

**4.** $R_{2} - 2 R_{1} = 0 ;\  R_{3} - R_{1} = [0 ,\  - 2 ,\  - 2 ,\  - 4]$. Two independent rows: **rank 2**.

**5.** $\det A = - 3 - 2 = - 5 ;\  x = \det \begin{bmatrix} 7 & 2 \\ 1 & - 1 \end{bmatrix} / - 5 = (- 7 - 2) / - 5$ = **$\frac{9}{5}$**; $y = \det \begin{bmatrix} 3 & 7 \\ 1 & 1 \end{bmatrix} / - 5 = (3 - 7) / - 5$ = **$\frac{4}{5}$**. Check: $3 \left( \frac{9}{5} \right) + 2 \left( \frac{4}{5} \right) = \frac{35}{5} = 7$ ✓.

**6.** Row 2 is twice row 1, so one equation: $x = - 2 y - 3 z$ with $y = s ,\  z = t$ free: **$(- 2 s - 3 t ,\  s ,\  t)$**, a plane through the origin (rank 1, 2 free parameters).

**7.** $c = 1 ;\  a + b + 1 = 4 ;\  4 a + 2 b + 1 = 9 \Rightarrow a + b = 3 ,\  2 a + b = 4 \Rightarrow a = 1 ,\  b = 2$: **$y = x^{2} + 2 x + 1 = (x + 1)^{2}$**.

**8.** a Fe + $b O_{2} \to c F e_{2} O_{3}$: Fe: $a = 2 c ;\  O$: $2 b = 3 c$. With $c = 2$: $a = 4 ,\  b = 3$. **4Fe + $3 O_{2} \to 2 F e_{2} O_{3}$.**

**9.** From the first two: $x = 1 ,\  y = 1$; the third gives $2 (1) + 1 = 3$ ✓. **Consistent**, unique solution (1, 1) (rank 2 = rank of the augmented matrix).

**10.** Elimination is $O (n^{3})$: 10 times more equations is 1000 times more work, about **1000 $s \approx 17$ minutes**.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Solve by Gaussian elimination: $x + y + z = 6 ,\  2 x - y + z = 3 ,\  x + 2 y - z = 2$.**

*Introduction.* Gaussian elimination reduces the augmented matrix to upper-triangular form by row operations, then back-substitutes.

*Augmented matrix.* $\begin{bmatrix} 1 & 1 & 1 \mid 6 \\ 2 & - 1 & 1 \mid 3 \\ 1 & 2 & - 1 \mid 2 \end{bmatrix}$.

*Elimination.* R2 → R2 − 2R1 gives [0, −3, −1 | −9]. R3 → R3 − R1 gives [0, 1, −2 | −4]. Swap to use the simple row: R2 ↔ R3, so [0, 1, −2 | −4] and [0, −3, −1 | −9]. Then R3 → R3 + 3R2 gives [0, 0, −7 | −21].

*Back-substitution.* $- 7 z = - 21$, so **$z = 3$**. Then $y - 2 (3) = - 4$ gives **$y = 2$**. Then $x + 2 + 3 = 6$ gives **$x = 1$**.

*Check.* $2 (1) - 2 + 3 = 3$ and $1 + 2 (2) - 3 = 2$, both correct. *Conclusion.* The unique solution is $(x ,\  y ,\  z) = (1 ,\  2 ,\  3)$; the pivots 1, 1, −7 are all non-zero, so the rank is 3.

**Q2 (10 marks). State and explain the conditions for consistency of a linear system using rank, with an example of each case, and mention Cramer's rule.**

*Introduction.* A system $A X = b$ with *n* unknowns is **consistent** if it has at least one solution. The rank of a matrix is the number of non-zero rows after elimination (equivalently, the number of independent rows). Rank settles consistency completely.

*The rank test (Rouché–Capelli).*

1. **Compare ranks.** Compute rank A and the rank of the augmented matrix [A | *b*].
2. **Inconsistent.** If rank A < rank [A | *b*], there is no solution. Example: $x + y = 2$ and $2 x + 2 y = 5$ give rank $A = 1$ but rank [A | $b ] = 2$.
3. **Unique solution.** If rank A = rank [A | $b ] = n$, there is exactly one solution. Example: $x + y = 2 ,\  x - y = 0$ gives $x = y = 1$.
4. **Infinitely many.** If rank A = rank [A | $b ] < n$, there are *n* − rank free parameters. Example: $x + y = 2$ and $2 x + 2 y = 4$ give $y = t ,\  x = 2 - t$.
5. **Geometry.** Cases (a), (b) and (c) of Figure 2.1 are lines that meet once, are parallel, or coincide.

*Cramer's rule.* When A is square and $\det A \neq 0 ,\  x_{i} = \det A_{i} \div \det A$, where $A_{i}$ has column *i* replaced by *b*. For $x + y = 2 ,\  x - y = 0$: $\det A = - 2 ,\  \det A_{1} = \det \begin{bmatrix} 2 & 1 \\ 0 & - 1 \end{bmatrix} = - 2$, so $x = (- 2) \div (- 2) = 1$. It is elegant but costly for large systems, where elimination is preferred.

| Rank condition | Meaning | Example |
|---|---|---|
| rank A < rank [A\|b] | no solution | $x + y = 2 ,\  2 x + 2 y = 5$ |
| rank A = rank [A\|b] = *n* | one solution | $x + y = 2 ,\  x - y = 0$ |
| rank A = rank [A\|b] < *n* | infinitely many | $x + y = 2 ,\  2 x + 2 y = 4$ |

*Conclusion.* Two numbers, rank A and rank [A | *b*], decide whether a system has no, one or infinitely many solutions, and elimination then finds them.
