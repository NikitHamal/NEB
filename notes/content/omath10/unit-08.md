---
subject: Optional Mathematics
grade: 10
unit: 8
title: Vector
hours: 0
area: Units
---

A force on a rope, the velocity of an aeroplane against the wind and the displacement of a trekker from Lukla to Namche are all quantities that have **size and direction**. Such quantities are vectors. In earlier classes you added vectors and multiplied them by numbers. In this chapter you meet the second kind of product, the **scalar (dot) product**, which turns two vectors into a single number and gives a clean way to find angles and to test perpendicularity. You then use vectors to prove facts of ordinary geometry: the midpoint theorem, the diagonals of a rhombus, and the right angle in a semicircle.

::: key What the SEE asks from this chapter
Expect (i) a dot product from components, the angle between two vectors and the length of a vector; (ii) a value of $k$ that makes two vectors perpendicular or parallel; (iii) position-vector questions: midpoint, section formula, a missing vertex of a parallelogram, collinear points; (iv) a **vector proof** of a theorem on triangles or quadrilaterals (4-mark question). A proof earns marks for naming the vectors, using the triangle law, and stating the conclusion in words.
:::

```photo id="omath10/tower-crane" caption="A tower crane. The load's weight, the weight of the jib and the tension in the tie are three forces that add as vectors; equilibrium means their vector sum is zero." width="96"
```

**Notation.** A vector in the plane is written $\vec{a}=(a_1,a_2)$, which is the same as $a_1\hat{i}+a_2\hat{j}$. (The CDC textbook stacks the two numbers in a column; they are the same numbers. We write them in a row so they can be typed inside a line of text.) The vector from the origin $O$ to a point $A$ is the **position vector** $\vec{OA}=\vec{a}$, and the vector from $A$ to $B$ is $\vec{AB}=\vec{b}-\vec{a}$, the position vector of the end point minus that of the start. Its length is $|\vec{a}|=\sqrt{a_1^2+a_2^2}$.

## 8.1 Scalar (dot) product of two vectors

::: definition Scalar product
The **scalar product** (or dot product) of two non-zero vectors $\vec{a}$ and $\vec{b}$, with angle $\theta$ between them (between $0^\circ$ and $180^\circ$), is the **number**

$$ \vec{a}\cdot\vec{b}=|\vec{a}|\,|\vec{b}|\cos\theta $$

The angle $\theta$ is measured when both vectors start from the same point.
:::

### Geometrical meaning

Drop a perpendicular from the tip of $\vec{b}$ onto the line of $\vec{a}$. The length cut off along $\vec{a}$ is $|\vec{b}|\cos\theta$, the **projection of $\vec{b}$ on $\vec{a}$**. So

$$ \vec{a}\cdot\vec{b}=|\vec{a}|\times(\text{projection of }\vec{b}\text{ on }\vec{a}) $$

```figure caption="The dot product $\vec{a}\cdot\vec{b}=|\vec{a}|\,|\vec{b}|\cos\theta$. The projection of $\vec{b}$ on $\vec{a}$ has length $|\vec{b}|\cos\theta$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6, 2.6))
th = np.radians(38)
a = np.array([4.0, 0.0]); b = 3.0*np.array([np.cos(th), np.sin(th)])
ar = dict(arrowstyle='-|>', lw=1.8, mutation_scale=12)
ax.annotate('', xy=a, xytext=(0, 0), arrowprops=dict(color=ACCENT, **ar))
ax.annotate('', xy=b, xytext=(0, 0), arrowprops=dict(color=SERIES[1], **ar))
ax.plot([b[0], b[0]], [b[1], 0], color=MUTED, lw=1, ls='--')
ax.plot([0, b[0]], [-0.18, -0.18], color=INK, lw=1.2)
ax.text(b[0]/2, -0.55, r'projection $=|\vec{b}|\cos\theta$', fontsize=8.5, ha='center')
t = np.linspace(0, th, 30)
ax.plot(0.8*np.cos(t), 0.8*np.sin(t), color=INK, lw=0.8)
ax.text(0.95, 0.22, r'$\theta$', fontsize=9)
ax.text(4.1, -0.05, r'$\vec{a}$', fontsize=11, color=ACCENT, va='center')
ax.text(b[0]+0.05, b[1]+0.12, r'$\vec{b}$', fontsize=11, color=SERIES[1])
ax.set_xlim(-0.4, 5.0); ax.set_ylim(-0.9, 2.3); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

### Dot products of $\hat{i}$ and $\hat{j}$

$\hat{i}$ and $\hat{j}$ are unit vectors ($|\hat{i}|=|\hat{j}|=1$) along the axes, and they are at $90^\circ$:

$$ \hat{i}\cdot\hat{i}=1\times1\times\cos0^\circ=1, \qquad \hat{j}\cdot\hat{j}=1, \qquad \hat{i}\cdot\hat{j}=\hat{j}\cdot\hat{i}=1\times1\times\cos90^\circ=0 $$

::: derivation Dot product in components
**Setting up.** Let $\vec{a}=a_1\hat{i}+a_2\hat{j}$ and $\vec{b}=b_1\hat{i}+b_2\hat{j}$.

**Step 1 — expand using the distributive law.**

$$ \vec{a}\cdot\vec{b}=(a_1\hat{i}+a_2\hat{j})\cdot(b_1\hat{i}+b_2\hat{j}) $$

$$ =a_1b_1(\hat{i}\cdot\hat{i})+a_1b_2(\hat{i}\cdot\hat{j})+a_2b_1(\hat{j}\cdot\hat{i})+a_2b_2(\hat{j}\cdot\hat{j}) $$

**Step 2 — use the values above.** The two cross terms are $0$, and $\hat{i}\cdot\hat{i}=\hat{j}\cdot\hat{j}=1$.

**Result.**

$$ \vec{a}\cdot\vec{b}=a_1b_1+a_2b_2 $$

**What it means.** To find a dot product from coordinates, multiply the first components, multiply the second components and **add**. No angle is needed.

**Length.** Put $\vec{b}=\vec{a}$: $\vec{a}\cdot\vec{a}=a_1^2+a_2^2=|\vec{a}|^2$, so $|\vec{a}|=\sqrt{a_1^2+a_2^2}$.
:::

::: key Dot product: three things to know
- $\vec{a}\cdot\vec{b}=|\vec{a}||\vec{b}|\cos\theta=a_1b_1+a_2b_2$ (a **number**, not a vector).
- $\vec{a}\cdot\vec{a}=|\vec{a}|^2$, and $\vec{a}\cdot\vec{b}=\vec{b}\cdot\vec{a}$ (commutative).
- $\vec{a}\cdot(\vec{b}+\vec{c})=\vec{a}\cdot\vec{b}+\vec{a}\cdot\vec{c}$ (distributive). Also $(k\vec{a})\cdot\vec{b}=k(\vec{a}\cdot\vec{b})$.
:::

### Algebraic relations

Using the properties, with $|\vec{a}|^2=\vec{a}\cdot\vec{a}$:

$$ |\vec{a}+\vec{b}|^2=|\vec{a}|^2+2\,\vec{a}\cdot\vec{b}+|\vec{b}|^2 $$

$$ |\vec{a}-\vec{b}|^2=|\vec{a}|^2-2\,\vec{a}\cdot\vec{b}+|\vec{b}|^2 $$

$$ (\vec{a}+\vec{b})\cdot(\vec{a}-\vec{b})=|\vec{a}|^2-|\vec{b}|^2 $$

The dot product is largest ($|\vec{a}||\vec{b}|$) when $\theta=0^\circ$ and smallest ($-|\vec{a}||\vec{b}|$) when $\theta=180^\circ$.

::: caution Dot product is a number
$\vec{a}\cdot\vec{b}$ is a **scalar**. Writing a vector answer, or writing $\vec{a}\cdot\vec{b}\cdot\vec{c}$, is meaningless. Also, $\vec{a}\cdot\vec{b}=0$ does **not** mean $\vec{a}=\vec{0}$ or $\vec{b}=\vec{0}$: it may mean the vectors are perpendicular.
:::

::: example Dot product and length
**Problem.** If $\vec{a}=(3,-2)$ and $\vec{b}=(4,5)$, find $\vec{a}\cdot\vec{b}$, $|\vec{a}|$ and $|\vec{b}|$.

**Solution.** $\vec{a}\cdot\vec{b}=3\times4+(-2)\times5=12-10=2$.

$|\vec{a}|=\sqrt{9+4}=\sqrt{13}$ and $|\vec{b}|=\sqrt{16+25}=\sqrt{41}$.
:::

::: example Using $|\vec{a}+\vec{b}|^2$
**Problem.** If $|\vec{a}|=3$, $|\vec{b}|=4$ and the angle between them is $60^\circ$, find $\vec{a}\cdot\vec{b}$, $|\vec{a}+\vec{b}|$ and $|\vec{a}-\vec{b}|$.

**Solution.** $\vec{a}\cdot\vec{b}=3\times4\times\cos60^\circ=12\times\dfrac12=6$.

$|\vec{a}+\vec{b}|^2=9+2\times6+16=37$, so $|\vec{a}+\vec{b}|=\sqrt{37}$.

$|\vec{a}-\vec{b}|^2=9-12+16=13$, so $|\vec{a}-\vec{b}|=\sqrt{13}$.
:::

## 8.2 Angle between vectors, perpendicular and parallel vectors

Solve $\vec{a}\cdot\vec{b}=|\vec{a}||\vec{b}|\cos\theta$ for $\cos\theta$:

::: key Angle, perpendicular and parallel
$$ \cos\theta=\frac{\vec{a}\cdot\vec{b}}{|\vec{a}||\vec{b}|}=\frac{a_1b_1+a_2b_2}{\sqrt{a_1^2+a_2^2}\,\sqrt{b_1^2+b_2^2}} $$

| Condition | Test |
|---|---|
| **Perpendicular** ($\theta=90^\circ$, $\cos\theta=0$) | $\vec{a}\cdot\vec{b}=0$, i.e. $a_1b_1+a_2b_2=0$ |
| **Parallel** ($\theta=0^\circ$ or $180^\circ$) | $\vec{a}=m\vec{b}$, i.e. $\dfrac{a_1}{b_1}=\dfrac{a_2}{b_2}$, i.e. $a_1b_2-a_2b_1=0$ |
| Angle is **acute** | $\vec{a}\cdot\vec{b}>0$ |
| Angle is **obtuse** | $\vec{a}\cdot\vec{b}<0$ |

The **projection of $\vec{a}$ on $\vec{b}$** is $\dfrac{\vec{a}\cdot\vec{b}}{|\vec{b}|}$.
:::

::: example Angle between two vectors
**Problem.** Find the angle between $\vec{a}=(3,1)$ and $\vec{b}=(1,2)$.

**Solution.** $\vec{a}\cdot\vec{b}=3\times1+1\times2=5$. $|\vec{a}|=\sqrt{10}$, $|\vec{b}|=\sqrt{5}$.

$$ \cos\theta=\frac{5}{\sqrt{10}\sqrt{5}}=\frac{5}{\sqrt{50}}=\frac{5}{5\sqrt{2}}=\frac{1}{\sqrt{2}} $$

So $\theta=45^\circ$.
:::

::: example Angle of a triangle
**Problem.** The vertices of a triangle are $A(1,1)$, $B(4,1)$ and $C(1,5)$. Find $\angle B$.

**Solution.** At $B$ the two sides are $\vec{BA}$ and $\vec{BC}$ (both start at $B$).

$\vec{BA}=(1-4,\,1-1)=(-3,0)$ and $\vec{BC}=(1-4,\,5-1)=(-3,4)$.

$\vec{BA}\cdot\vec{BC}=9+0=9$, $|\vec{BA}|=3$, $|\vec{BC}|=\sqrt{9+16}=5$.

$$ \cos B=\frac{9}{3\times5}=\frac35 \quad\Rightarrow\quad B\approx53.13^\circ $$

(At $A$: $\vec{AB}=(3,0)$ and $\vec{AC}=(0,4)$ have dot product $0$, so $\angle A=90^\circ$.)
:::

::: example Perpendicular and parallel vectors
**Problem.** (a) Find $k$ so that $\vec{a}=(k,2)$ is perpendicular to $\vec{b}=(3,-6)$. (b) Find $k$ so that $\vec{p}=(2,k)$ is parallel to $\vec{q}=(6,9)$.

**Solution.** (a) $\vec{a}\cdot\vec{b}=3k-12=0$, so $k=4$.

(b) Parallel: $2\times9-k\times6=0$, so $k=3$. Check: $\vec{q}=3\vec{p}=(6,9)$. ✓
:::

::: example Show that two vectors are perpendicular
**Problem.** Show that $\vec{a}=(1,-2)$ and $\vec{b}=(4,2)$ are perpendicular, and find a unit vector perpendicular to $\vec{c}=(3,4)$.

**Solution.** $\vec{a}\cdot\vec{b}=4-4=0$, so $\vec{a}\perp\vec{b}$.

A vector perpendicular to $(3,4)$ is $(-4,3)$ (dot product $-12+12=0$). Its length is $\sqrt{16+9}=5$, so the unit vector is $\dfrac{1}{5}(-4,3)=\left(-\dfrac45,\dfrac35\right)$.
:::

::: example Projection
**Problem.** Find the projection of $\vec{a}=(2,3)$ on $\vec{b}=(3,4)$.

**Solution.** $\vec{a}\cdot\vec{b}=6+12=18$, $|\vec{b}|=5$. Projection $=\dfrac{18}{5}=3.6$.
:::

::: example Condition $|\vec{a}+\vec{b}|=|\vec{a}-\vec{b}|$
**Problem.** If $|\vec{a}+\vec{b}|=|\vec{a}-\vec{b}|$, show that $\vec{a}\perp\vec{b}$.

**Solution.** Square both sides: $|\vec{a}|^2+2\vec{a}\cdot\vec{b}+|\vec{b}|^2=|\vec{a}|^2-2\vec{a}\cdot\vec{b}+|\vec{b}|^2$. So $4\,\vec{a}\cdot\vec{b}=0$, i.e. $\vec{a}\cdot\vec{b}=0$, so the vectors are perpendicular (the diagonals of a parallelogram are equal only for a rectangle).
:::

## 8.3 Vector geometry: section formula and collinear points

### Position vectors and the triangle law

For points $A$ and $B$ with position vectors $\vec{a}$ and $\vec{b}$, the **triangle law** gives $\vec{OA}+\vec{AB}=\vec{OB}$, so $\vec{AB}=\vec{b}-\vec{a}$.

::: derivation Section formula (internal division)
**Setting up.** Let $P$ divide $AB$ internally in the ratio $m:n$, i.e. $AP:PB=m:n$.

**Step 1 — compare vectors along the line.** $\vec{AP}$ and $\vec{PB}$ are in the same direction, and $n\,\vec{AP}=m\,\vec{PB}$.

**Step 2 — write in position vectors.** With $\vec{p}$ the position vector of $P$:

$$ n(\vec{p}-\vec{a})=m(\vec{b}-\vec{p}) $$

**Step 3 — solve for $\vec{p}$.**

$$ n\vec{p}-n\vec{a}=m\vec{b}-m\vec{p} \;\Rightarrow\; (m+n)\vec{p}=m\vec{b}+n\vec{a} $$

**Result.**

$$ \vec{p}=\frac{m\vec{b}+n\vec{a}}{m+n} $$

**What it means.** $P$ is a weighted average of $A$ and $B$, closer to the end with the **larger weight**. For $m=n$ (the midpoint) $\vec{p}=\dfrac{\vec{a}+\vec{b}}{2}$.
:::

```figure caption="Position vectors $\vec{a}$, $\vec{b}$ and $\vec{p}$ from the origin $O$. $P$ divides $AB$ in the ratio $m:n$, so $\vec{p}=\dfrac{m\vec{b}+n\vec{a}}{m+n}$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6, 2.9))
O = np.array([0.0, 0.0]); A = np.array([1.0, 2.2]); B = np.array([4.6, 1.6])
P = (2*B + 3*A)/5
ar = dict(arrowstyle='-|>', lw=1.3, mutation_scale=10)
for pt, col in [(A, ACCENT), (B, ACCENT), (P, SERIES[1])]:
    ax.annotate('', xy=pt, xytext=O, arrowprops=dict(color=col, **ar))
ax.plot([A[0], B[0]], [A[1], B[1]], color=INK, lw=1.5)
for pt, n, dx, dy in [(O, 'O', -0.25, -0.1), (A, 'A', -0.1, 0.18), (B, 'B', 0.1, 0.1), (P, 'P', 0.0, 0.2)]:
    ax.plot([pt[0]], [pt[1]], 'o', color=INK, ms=3.5)
    ax.text(pt[0]+dx, pt[1]+dy, n, fontsize=9)
ax.text(0.15, 1.35, r'$\vec{a}$', fontsize=10, color=ACCENT)
ax.text(2.8, 0.55, r'$\vec{b}$', fontsize=10, color=ACCENT)
ax.text(1.6, 0.95, r'$\vec{p}$', fontsize=10, color=SERIES[1])
ax.text(3.4, 2.5, r'$AP:PB=m:n$', fontsize=8.5)
ax.set_xlim(-0.6, 5.2); ax.set_ylim(-0.3, 2.9); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

Further results from the same triangle-law reasoning:

| Result | Formula |
|---|---|
| Vector $\vec{AB}$ | $\vec{b}-\vec{a}$ |
| Midpoint of $AB$ | $\dfrac{\vec{a}+\vec{b}}{2}$ |
| Centroid of $\triangle ABC$ | $\dfrac{\vec{a}+\vec{b}+\vec{c}}{3}$ |
| $ABCD$ is a parallelogram | $\vec{AB}=\vec{DC}$, so $\vec{d}=\vec{a}+\vec{c}-\vec{b}$ |
| $A,B,C$ collinear | $\vec{AB}=k\,\vec{AC}$ for some number $k$ |

::: example Section formula with coordinates
**Problem.** Find the point $P$ that divides the line joining $A(2,3)$ and $B(7,8)$ internally in the ratio $2:3$.

**Solution.** $\vec{p}=\dfrac{2\vec{b}+3\vec{a}}{2+3}=\dfrac{2(7,8)+3(2,3)}{5}=\dfrac{(14,16)+(6,9)}{5}=\dfrac{(20,25)}{5}=(4,5)$.

So $P=(4,5)$. Check: $AP=(2,2)$, $PB=(3,3)$, ratio $2:3$. ✓
:::

::: example Collinear points
**Problem.** Show that $A(1,2)$, $B(3,6)$ and $C(4,8)$ are collinear.

**Solution.** $\vec{AB}=(3-1,\,6-2)=(2,4)$ and $\vec{AC}=(4-1,\,8-2)=(3,6)$.

$\vec{AB}=k\vec{AC}$ requires $\dfrac23=\dfrac46$, which is true ($k=\dfrac23$). The two vectors are parallel and share the point $A$, so $A$, $B$, $C$ lie on one line.
:::

::: example Fourth vertex of a parallelogram
**Problem.** $A(1,1)$, $B(5,2)$ and $C(7,5)$ are three vertices of a parallelogram $ABCD$ (in order). Find $D$.

**Solution.** For a parallelogram $\vec{AB}=\vec{DC}$, so $\vec{d}=\vec{a}+\vec{c}-\vec{b}=(1,1)+(7,5)-(5,2)=(3,4)$.

Check: the midpoints of the diagonals $AC$ and $BD$ are $(4,3)$ and $\dfrac{(5,2)+(3,4)}{2}=(4,3)$. ✓
:::

::: example Centroid
**Problem.** Find the centroid of the triangle with vertices $A(1,2)$, $B(5,4)$ and $C(3,9)$.

**Solution.** $\vec{g}=\dfrac{\vec{a}+\vec{b}+\vec{c}}{3}=\dfrac{(1+5+3,\;2+4+9)}{3}=\dfrac{(9,15)}{3}=(3,5)$.
:::

## 8.4 Theorems on triangles

All proofs below follow the same plan: **state what is given, state what is to prove, give the proof with the triangle law, conclude.**

::: derivation Theorem 1 — the midpoint theorem
**Statement.** The line joining the midpoints of two sides of a triangle is parallel to the third side and half of it.

**Given.** In $\triangle ABC$, $D$ and $E$ are the midpoints of $AB$ and $AC$.

**To prove.** $\vec{DE}=\dfrac12\vec{BC}$ (so $DE\parallel BC$ and $DE=\dfrac12BC$).

**Proof.** In $\triangle ADE$, by the triangle law, $\vec{DE}=\vec{DA}+\vec{AE}$.

Since $D$ and $E$ are midpoints, $\vec{DA}=\dfrac12\vec{BA}$ and $\vec{AE}=\dfrac12\vec{AC}$. So

$$ \vec{DE}=\frac12\vec{BA}+\frac12\vec{AC}=\frac12\left(\vec{BA}+\vec{AC}\right) $$

In $\triangle ABC$, $\vec{BA}+\vec{AC}=\vec{BC}$. Therefore

$$ \vec{DE}=\frac12\vec{BC} $$

**Conclusion.** $\vec{DE}$ is a scalar multiple of $\vec{BC}$, so $DE\parallel BC$, and $DE=\dfrac12BC$.
:::

```figure caption="Midpoint theorem: $D$ and $E$ are the midpoints of $AB$ and $AC$, so $DE\parallel BC$ and $DE=\frac12BC$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4, 2.8))
A = np.array([2.2, 3.0]); B = np.array([0.0, 0.0]); C = np.array([5.0, 0.0])
D = (A+B)/2; E = (A+C)/2
ax.fill([A[0], B[0], C[0]], [A[1], B[1], C[1]], color='#eff6ff', zorder=0)
ax.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], color=INK, lw=1.4)
ax.plot([D[0], E[0]], [D[1], E[1]], color=SERIES[1], lw=1.8)
for p, n, dx, dy in [(A, 'A', 0, 0.12), (B, 'B', -0.2, -0.1), (C, 'C', 0.1, -0.1), (D, 'D', -0.22, 0.05), (E, 'E', 0.1, 0.05)]:
    ax.plot([p[0]], [p[1]], 'o', color=INK, ms=3.5)
    ax.text(p[0]+dx, p[1]+dy, n, fontsize=9)
ax.text(2.5, 1.62, 'DE', fontsize=8.5, color=SERIES[1], ha='center')
ax.text(2.5, -0.35, 'BC = 2 DE', fontsize=8.5, ha='center')
ax.set_xlim(-0.6, 5.6); ax.set_ylim(-0.7, 3.5); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: derivation Theorem 2 — the median of an isosceles triangle
**Statement.** In an isosceles triangle, the median drawn from the vertex to the base is perpendicular to the base.

**Given.** In $\triangle ABC$, $AB=AC$ and $D$ is the midpoint of $BC$.

**To prove.** $AD\perp BC$, i.e. $\vec{AD}\cdot\vec{BC}=0$.

**Proof.** Since $D$ is the midpoint of $BC$, $\vec{AD}=\dfrac12\left(\vec{AB}+\vec{AC}\right)$ and $\vec{BC}=\vec{AC}-\vec{AB}$.

$$ \vec{AD}\cdot\vec{BC}=\frac12\left(\vec{AB}+\vec{AC}\right)\cdot\left(\vec{AC}-\vec{AB}\right)=\frac12\left(|\vec{AC}|^2-|\vec{AB}|^2\right) $$

But $AB=AC$, so $|\vec{AC}|^2-|\vec{AB}|^2=0$.

**Conclusion.** $\vec{AD}\cdot\vec{BC}=0$, so $AD\perp BC$.
:::

::: derivation Theorem 3 — Pythagoras' theorem by vectors
**Statement.** In a right-angled triangle, the square on the hypotenuse equals the sum of the squares on the other two sides.

**Given.** In $\triangle ABC$, $\angle A=90^\circ$.

**To prove.** $BC^2=AB^2+AC^2$.

**Proof.** $\vec{BC}=\vec{AC}-\vec{AB}$, so

$$ |\vec{BC}|^2=|\vec{AC}|^2-2\,\vec{AB}\cdot\vec{AC}+|\vec{AB}|^2 $$

Since $\angle A=90^\circ$, $\vec{AB}\cdot\vec{AC}=0$.

**Conclusion.** $BC^2=AB^2+AC^2$.
:::

::: derivation Theorem 4 — a line through a midpoint parallel to a side
**Statement.** The line drawn through the midpoint of one side of a triangle parallel to another side bisects the third side.

**Given.** In $\triangle ABC$, $D$ is the midpoint of $AB$, and $DE\parallel BC$ meets $AC$ at $E$.

**To prove.** $E$ is the midpoint of $AC$.

**Proof.** Let $\vec{AE}=t\,\vec{AC}$ for some number $t$ (as $E$ lies on $AC$). Then $\vec{DE}=\vec{DA}+\vec{AE}=-\dfrac12\vec{AB}+t\vec{AC}$.

Since $DE\parallel BC$, $\vec{DE}=s\,\vec{BC}=s(\vec{AC}-\vec{AB})$. Compare coefficients of the independent vectors $\vec{AB}$ and $\vec{AC}$:

$$ \text{coefficient of }\vec{AB}:\; -\frac12=-s,\qquad \text{coefficient of }\vec{AC}:\; t=s $$

So $s=\dfrac12$ and $t=\dfrac12$.

**Conclusion.** $\vec{AE}=\dfrac12\vec{AC}$: $E$ is the midpoint of $AC$.
:::

## 8.5 Theorems on quadrilaterals and the semicircle

::: derivation Theorem 5 — the midpoints of the sides of a quadrilateral
**Statement.** The figure formed by joining, in order, the midpoints of the sides of any quadrilateral is a parallelogram.

**Given.** In quadrilateral $ABCD$, $P$, $Q$, $R$, $S$ are the midpoints of $AB$, $BC$, $CD$, $DA$.

**To prove.** $\vec{PQ}=\vec{SR}$, so $PQRS$ is a parallelogram.

**Proof.** Join $AC$. In $\triangle ABC$, $P$ and $Q$ are midpoints of $AB$ and $BC$, so by the midpoint theorem

$$ \vec{PQ}=\frac12\vec{AC} $$

In $\triangle ADC$, $S$ and $R$ are midpoints of $AD$ and $DC$, so

$$ \vec{SR}=\frac12\vec{AC} $$

**Conclusion.** $\vec{PQ}=\vec{SR}$: one pair of opposite sides is equal and parallel, so $PQRS$ is a parallelogram.
:::

```figure caption="Joining the midpoints $P,Q,R,S$ of the sides of any quadrilateral $ABCD$ always gives a parallelogram, because $PQ$ and $SR$ are both parallel to $AC$ and half of it."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4, 3.2))
A, B, C, D = map(np.array, [(0, 0), (6, 0), (8, 6), (2, 8)])
P, Q, R, S = (A+B)/2, (B+C)/2, (C+D)/2, (D+A)/2
ax.plot(*zip(A, B, C, D, A), color=INK, lw=1.4)
ax.plot(*zip(P, Q, R, S, P), color=SERIES[1], lw=1.8)
ax.plot(*zip(A, C), color=MUTED, lw=0.9, ls='--')
for p, n, dx, dy in [(A, 'A', -0.5, -0.5), (B, 'B', 0.2, -0.5), (C, 'C', 0.25, 0.1), (D, 'D', -0.5, 0.2), (P, 'P', 0.0, -0.6), (Q, 'Q', 0.25, -0.2), (R, 'R', 0.1, 0.3), (S, 'S', -0.6, 0.1)]:
    ax.plot([p[0]], [p[1]], 'o', color=INK, ms=3.2)
    ax.text(p[0]+dx, p[1]+dy, n, fontsize=9)
ax.set_xlim(-1.2, 9.4); ax.set_ylim(-1.3, 9.2); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: derivation Theorem 6 — the diagonals of a rhombus
**Statement.** The diagonals of a rhombus are perpendicular to each other.

**Given.** $ABCD$ is a rhombus: $AB=BC=CD=DA$.

**To prove.** $AC\perp BD$.

**Proof.** Take $A$ as the origin with $\vec{AB}=\vec{u}$ and $\vec{AD}=\vec{v}$. Then $\vec{AC}=\vec{u}+\vec{v}$ and $\vec{BD}=\vec{v}-\vec{u}$.

$$ \vec{AC}\cdot\vec{BD}=(\vec{u}+\vec{v})\cdot(\vec{v}-\vec{u})=|\vec{v}|^2-|\vec{u}|^2 $$

All sides are equal, so $|\vec{u}|=|\vec{v}|$.

**Conclusion.** $\vec{AC}\cdot\vec{BD}=0$, so the diagonals are perpendicular.
:::

::: derivation Theorem 7 — the angle in a semicircle
**Statement.** The angle in a semicircle is a right angle.

**Given.** $AB$ is a diameter of a circle with centre $O$, and $P$ is any point on the circle.

**To prove.** $\angle APB=90^\circ$.

**Proof.** Take $O$ as the origin. $\vec{OA}=\vec{a}$, $\vec{OB}=-\vec{a}$ (opposite ends of a diameter) and $\vec{OP}=\vec{p}$, with $|\vec{p}|=|\vec{a}|=r$ (the radius).

$$ \vec{PA}=\vec{a}-\vec{p}, \qquad \vec{PB}=-\vec{a}-\vec{p} $$

$$ \vec{PA}\cdot\vec{PB}=(\vec{a}-\vec{p})\cdot(-\vec{a}-\vec{p})=|\vec{p}|^2-|\vec{a}|^2=r^2-r^2=0 $$

**Conclusion.** $\vec{PA}\perp\vec{PB}$, so $\angle APB=90^\circ$.
:::

```figure caption="The angle in a semicircle. With $O$ as origin, $\vec{PA}\cdot\vec{PB}=|\vec{p}|^2-|\vec{a}|^2=0$ for every point $P$ on the circle."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.2, 2.6))
t = np.linspace(0, np.pi, 200)
ax.plot(2*np.cos(t), 2*np.sin(t), color=ACCENT, lw=1.7)
ax.plot([-2, 2], [0, 0], color=INK, lw=1.4)
P = np.array([2*np.cos(np.radians(65)), 2*np.sin(np.radians(65))])
ax.plot([-2, P[0], 2], [0, P[1], 0], color=SERIES[1], lw=1.4)
ax.plot([P[0]+0.0], [P[1]], 'o', color=INK, ms=3.5)
u = (np.array([-2, 0]) - P); u /= np.linalg.norm(u)
v = (np.array([2, 0]) - P); v /= np.linalg.norm(v)
s = 0.3
ax.plot(*zip(P+s*u, P+s*u+s*v, P+s*v), color=INK, lw=0.8)
for p, n, dx, dy in [((-2, 0), 'A', -0.3, -0.1), ((2, 0), 'B', 0.12, -0.1), ((0, 0), 'O', -0.05, -0.38), (tuple(P), 'P', 0.1, 0.1)]:
    ax.plot([p[0]], [p[1]], 'o', color=INK, ms=3.2)
    ax.text(p[0]+dx, p[1]+dy, n, fontsize=9)
ax.set_xlim(-2.6, 2.6); ax.set_ylim(-0.6, 2.4); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: derivation Theorem 8 — the diagonals of a parallelogram
**Statement.** The diagonals of a parallelogram bisect each other.

**Given.** $ABCD$ is a parallelogram; diagonals $AC$ and $BD$ meet at $O$.

**To prove.** $O$ is the midpoint of $AC$ and of $BD$.

**Proof.** Let $M$ be the midpoint of $AC$: $\vec{m}=\dfrac{\vec{a}+\vec{c}}{2}$. For a parallelogram $\vec{d}=\vec{a}+\vec{c}-\vec{b}$, so the midpoint of $BD$ is

$$ \frac{\vec{b}+\vec{d}}{2}=\frac{\vec{b}+\vec{a}+\vec{c}-\vec{b}}{2}=\frac{\vec{a}+\vec{c}}{2} $$

**Conclusion.** The midpoints of $AC$ and $BD$ are the same point, so the diagonals bisect each other.
:::

::: tip The examiner is looking for
(1) A labelled diagram. (2) "Given" and "To prove" written out. (3) Each vector equation justified: "by the triangle law", "since $D$ is the midpoint". (4) For perpendicularity, a dot product equal to $0$. (5) A final sentence in geometric words.
:::

## 8.6 Exercises of the SEE type

### Method for any question

1. Component questions: write $\vec{a}\cdot\vec{b}=a_1b_1+a_2b_2$, find the two lengths, then $\cos\theta$.
2. For $k$ in perpendicular/parallel questions: perpendicular $\Rightarrow$ dot product $0$; parallel $\Rightarrow a_1b_2=a_2b_1$.
3. For vectors between points, always **end minus start**: $\vec{AB}=\vec{b}-\vec{a}$.
4. For a proof: draw, give, prove, conclude; use the triangle law and the midpoint formula; expand dot products with $|\vec{a}|^2=\vec{a}\cdot\vec{a}$.

## Chapter summary

- $\vec{a}\cdot\vec{b}=|\vec{a}||\vec{b}|\cos\theta=a_1b_1+a_2b_2$; the result is a **number**.
- $\hat{i}\cdot\hat{i}=\hat{j}\cdot\hat{j}=1$, $\hat{i}\cdot\hat{j}=0$; $\vec{a}\cdot\vec{a}=|\vec{a}|^2$.
- $|\vec{a}\pm\vec{b}|^2=|\vec{a}|^2\pm2\vec{a}\cdot\vec{b}+|\vec{b}|^2$; $(\vec{a}+\vec{b})\cdot(\vec{a}-\vec{b})=|\vec{a}|^2-|\vec{b}|^2$.
- $\cos\theta=\dfrac{\vec{a}\cdot\vec{b}}{|\vec{a}||\vec{b}|}$; perpendicular $\Leftrightarrow\vec{a}\cdot\vec{b}=0$; parallel $\Leftrightarrow a_1b_2-a_2b_1=0$.
- Projection of $\vec{a}$ on $\vec{b}$ $=\dfrac{\vec{a}\cdot\vec{b}}{|\vec{b}|}$.
- $\vec{AB}=\vec{b}-\vec{a}$; midpoint $\dfrac{\vec{a}+\vec{b}}{2}$; section formula $\dfrac{m\vec{b}+n\vec{a}}{m+n}$; centroid $\dfrac{\vec{a}+\vec{b}+\vec{c}}{3}$; parallelogram $\vec{d}=\vec{a}+\vec{c}-\vec{b}$.
- Collinear: $\vec{AB}=k\vec{AC}$.
- Theorems proved: midpoint theorem; isosceles median; Pythagoras; midpoints of a quadrilateral form a parallelogram; rhombus diagonals perpendicular; angle in a semicircle; parallelogram diagonals bisect.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. If $\vec{a}=(2,3)$ and $\vec{b}=(4,-1)$, then $\vec{a}\cdot\vec{b}$ is <span class="marks">[1]</span>
   (a) $5$ (b) $11$ (c) $(8,-3)$ (d) $-5$
2. Two non-zero vectors are perpendicular if their dot product is <span class="marks">[1]</span>
   (a) $1$ (b) $-1$ (c) $0$ (d) $|\vec{a}||\vec{b}|$
3. $|\vec{a}|=3$, $|\vec{b}|=2$, angle $60^\circ$. Then $\vec{a}\cdot\vec{b}=$ <span class="marks">[1]</span>
   (a) $6$ (b) $3$ (c) $3\sqrt{3}$ (d) $\frac32$
4. The midpoint of the line joining $(2,6)$ and $(8,2)$ is <span class="marks">[1]</span>
   (a) $(10,8)$ (b) $(5,4)$ (c) $(3,2)$ (d) $(6,4)$
5. $\vec{a}=(1,k)$ and $\vec{b}=(2,6)$ are parallel when $k=$ <span class="marks">[1]</span>
   (a) $2$ (b) $3$ (c) $6$ (d) $\frac13$

::: note Answers to Group A
**1.** (a) — $8-3=5$.
**2.** (c) — $\cos90^\circ=0$.
**3.** (b) — $3\times2\times\frac12=3$.
**4.** (b) — $\left(\frac{2+8}{2},\frac{6+2}{2}\right)=(5,4)$.
**5.** (b) — $1\times6-k\times2=0$, so $k=3$.
:::

**Group B — Short answer (2 marks each)**

1. Find $|\vec{a}|$ if $\vec{a}=(5,-12)$. <span class="marks">[2]</span>
2. Find $k$ so that $(k,3)$ and $(2,-4)$ are perpendicular. <span class="marks">[2]</span>
3. Find the position vector of the point dividing $A(1,2)$ and $B(6,7)$ in the ratio $2:3$ internally. <span class="marks">[2]</span>
4. If $|\vec{a}|=5$, $|\vec{b}|=12$ and $\vec{a}\perp\vec{b}$, find $|\vec{a}+\vec{b}|$. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $\sqrt{25+144}=13$.
**2.** $2k-12=0$, so $k=6$.
**3.** $\dfrac{2(6,7)+3(1,2)}{5}=\dfrac{(12,14)+(3,6)}{5}=\dfrac{(15,20)}{5}=(3,4)$.
**4.** $|\vec{a}+\vec{b}|^2=25+0+144=169$, so $|\vec{a}+\vec{b}|=13$.
:::

**Group C — Short answer (3 marks each)**

1. Find the angle between $\vec{a}=(1,\sqrt{3})$ and $\vec{b}=(2,0)$. <span class="marks">[3]</span>
2. Show that $A(1,1)$, $B(2,3)$ and $C(4,7)$ are collinear. <span class="marks">[3]</span>
3. Three vertices of a parallelogram $ABCD$ are $A(0,0)$, $B(4,1)$ and $C(7,5)$. Find $D$. <span class="marks">[3]</span>
4. If $|\vec{a}|=2$, $|\vec{b}|=3$ and $\vec{a}\cdot\vec{b}=3$, find $|\vec{a}-\vec{b}|$ and the angle between $\vec{a}$ and $\vec{b}$. <span class="marks">[3]</span>

::: note Answers to Group C
**1.** $\vec{a}\cdot\vec{b}=2$, $|\vec{a}|=2$, $|\vec{b}|=2$. $\cos\theta=\frac{2}{4}=\frac12$, so $\theta=60^\circ$.
**2.** $\vec{AB}=(1,2)$ and $\vec{AC}=(3,6)=3\vec{AB}$. The vectors are parallel and share $A$, so the points are collinear.
**3.** $\vec{d}=\vec{a}+\vec{c}-\vec{b}=(0,0)+(7,5)-(4,1)=(3,4)$.
**4.** $|\vec{a}-\vec{b}|^2=4-6+9=7$, so $|\vec{a}-\vec{b}|=\sqrt{7}$. $\cos\theta=\frac{3}{6}=\frac12$, $\theta=60^\circ$.
:::

**Group D — Long answer (4 marks each)**

1. Prove that the line joining the midpoints of two sides of a triangle is parallel to the third side and half of it. <span class="marks">[4]</span>
2. Prove by vectors that the diagonals of a rhombus are perpendicular. <span class="marks">[4]</span>
3. Prove that the angle in a semicircle is a right angle. <span class="marks">[4]</span>
4. The vertices of a triangle are $A(2,1)$, $B(6,1)$, $C(2,4)$. Show that it is right-angled, and find $\angle B$ and the centroid. <span class="marks">[4]</span>

::: note Answers to Group D
**1.** See Theorem 1: $\vec{DE}=\vec{DA}+\vec{AE}=\frac12\vec{BA}+\frac12\vec{AC}=\frac12\vec{BC}$.
**2.** See Theorem 6: with $\vec{AB}=\vec{u}$, $\vec{AD}=\vec{v}$, $\vec{AC}\cdot\vec{BD}=|\vec{v}|^2-|\vec{u}|^2=0$ because the sides are equal.
**3.** See Theorem 7: $\vec{PA}\cdot\vec{PB}=|\vec{p}|^2-|\vec{a}|^2=0$.
**4.** $\vec{AB}=(4,0)$, $\vec{AC}=(0,3)$; $\vec{AB}\cdot\vec{AC}=0$, so $\angle A=90^\circ$. At $B$: $\vec{BA}=(-4,0)$, $\vec{BC}=(-4,3)$; dot $=16$, lengths $4$ and $5$: $\cos B=\frac{16}{20}=\frac45$, $B\approx36.87^\circ$. Centroid $=\dfrac{(2+6+2,\;1+1+4)}{3}=\left(\dfrac{10}{3},2\right)$.
:::



## Retrieval practice and investigation

::: key Work before reading the key
Answer these short retrieval questions without consulting the chapter. Explain the reason, not only the result. These are revision checks, not a prediction of the examination paper.
:::

**1.** Find the magnitude of (3, 4).

**2.** Find (2, −1) + (−3, 4).

**3.** Does a · b = 0 prove both vectors are nonzero and perpendicular?

::: note Reasoned key
**1.** √(3² + 4²) = 5. Magnitudes are nonnegative.

**2.** (−1, 3), by adding corresponding components.

**3.** No. A zero vector also has zero dot product with every vector. Perpendicular directions follow only when both vectors are nonzero.

:::

::: tip Investigation — Draw vector addition two ways
Draw a = (3, 0) and b = (0, 4) with a common origin. Construct their parallelogram and then use head-to-tail addition. Compare the resultant in both drawings and calculate its magnitude.

Submit a one-page record: your method, working or evidence, conclusion, and one limitation. Exchange it with a classmate and check the reasoning against the chapter.
:::
