---
subject: Optional Mathematics
grade: 8
unit: 8
title: Vector
hours: 0
---

"The bus stop is 500 m away" is useful, but "the bus stop is 500 m away, due north" is what you need to actually get there. Some quantities, such as mass, time and temperature, are described completely by a number with a unit. Others, such as a displacement, a velocity or a force, need a **direction** as well. Quantities of the second kind are **vectors**. A pilot flying from Kathmandu to Pokhara, an engineer working out the pull on the cables of a suspension bridge in Dolakha, and a footballer passing the ball all deal with vectors. In this chapter you will learn to represent vectors by arrows and by columns of numbers, find their magnitude and direction, recognise the different types of vector, and multiply, add and subtract them.

::: key What your examination asks from this chapter
Expect: (i) separating **scalar** and **vector** quantities, with examples; (ii) writing $\overrightarrow{AB}$ from the coordinates of $A$ and $B$, and finding its **magnitude** and **direction**; (iii) naming the **type** of a vector (position, unit, null, equal, negative, like, unlike) and finding a **unit vector**; (iv) finding unknowns from **equal vectors**; (v) multiplying a vector by a scalar and using the **condition for parallel vectors**; (vi) adding and subtracting vectors by components and by the **triangle and parallelogram laws**, often in a displacement or force problem. Always draw the arrows: a sketch shows the direction of the answer.
:::

## 8.1 Vector and scalar quantities; magnitude and direction of a vector

### Scalars and vectors

::: definition Scalar and vector quantities
A **scalar quantity** has **magnitude only**: it is fully described by a number and a unit. A **vector quantity** has both **magnitude and direction**.
:::

| Scalar quantities | Vector quantities |
|---|---|
| mass (50 kg) | displacement (3 km to the east) |
| length, distance (7 km) | velocity (60 km/h towards Pokhara) |
| time (2 hours) | acceleration ($9.8$ m/s² downwards) |
| temperature ($25^\circ$C) | force (20 N pulling to the left) |
| speed (60 km/h) | weight (500 N, downwards) |
| area, volume, money | momentum |

Notice the pairs: **distance** is a scalar but **displacement** is a vector; **speed** is a scalar but **velocity** is a vector.

A quick test tells the two kinds apart: ask "**in which direction?**". For a force, a push or a journey the question makes sense and matters, so the quantity is a vector. For a mass, a price or a temperature the question has no meaning, so the quantity is a scalar. Weight is a vector (it always acts downwards, towards the centre of the earth), but mass is a scalar: a 50 kg bag of rice has the same mass in Kathmandu and on the Moon, although its weight is much smaller on the Moon.

Ram walks 3 km east and then 4 km north. The **distance** he has walked is $3+4=7$ km. But his **displacement**, the straight-line change in position from start to finish, is only $\sqrt{3^2+4^2}=5$ km, in a direction between east and north. Two walks of 7 km can end in completely different places; their displacements tell them apart.

### Representing a vector

A vector is drawn as an **arrow** (a directed line segment). The length of the arrow shows the magnitude and the arrowhead shows the direction. The arrow from $A$ to $B$ is written $\overrightarrow{AB}$; $A$ is its **initial point** (tail) and $B$ its **terminal point** (head). A single small letter with an arrow, $\vec{a}$, is also used.

On a grid, a vector is described by how far it goes **across** and how far it goes **up**: its $x$-component and $y$-component. These are written in a column:
$$ \vec{a}=\binom{x}{y} $$
If $A$ is $(x_1,y_1)$ and $B$ is $(x_2,y_2)$, then to go from $A$ to $B$ we move $x_2-x_1$ across and $y_2-y_1$ up:
$$ \overrightarrow{AB}=\binom{x_2-x_1}{y_2-y_1}\qquad\text{(head minus tail)} $$

```figure caption="The vector $\overrightarrow{AB}$ from $A(1,2)$ to $B(4,6)$ has $x$-component 3 and $y$-component 4, so $\overrightarrow{AB}=\binom{3}{4}$. Its magnitude is the length $\sqrt{3^2+4^2}=5$ and its direction is the angle $\theta$ with the positive $x$-direction, where $\tan\theta=\frac{4}{3}$."
from matplotlib.patches import Arc
fig, ax = plt.subplots(figsize=(4.6, 3.2))
A, B = (1, 2), (4, 6)
ax.annotate('', xy=B, xytext=A, arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=2.0, mutation_scale=14))
ax.plot([A[0], B[0]], [A[1], A[1]], color=SERIES[1], lw=1.2, ls='--')
ax.plot([B[0], B[0]], [A[1], B[1]], color=SERIES[2], lw=1.2, ls='--')
ax.plot(*A, 'o', color=INK, ms=4.5); ax.plot(*B, 'o', color=INK, ms=4.5)
ax.text(A[0] - 0.15, A[1] - 0.1, 'A(1, 2)', ha='right', fontsize=9)
ax.text(B[0] + 0.15, B[1], 'B(4, 6)', fontsize=9)
ax.text(2.5, 1.55, 'x-component = 3', ha='center', fontsize=8.5, color=SERIES[1])
ax.text(4.15, 4.0, 'y-component = 4', fontsize=8.5, color=SERIES[2], va='center')
ax.text(2.05, 4.35, '|AB| = 5', fontsize=9, color=ACCENT, ha='center')
ax.add_patch(Arc(A, 1.4, 1.4, theta1=0, theta2=np.degrees(np.arctan2(4, 3)), color=INK, lw=1.0))
ax.text(1.85, 2.25, 'θ', fontsize=10)
ax.set_xlim(-0.5, 7.0); ax.set_ylim(0, 7)
ax.set_xticks(range(0, 7)); ax.set_yticks(range(0, 8))
ax.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
ax.spines[['top', 'right']].set_visible(False); ax.tick_params(labelsize=8)
ax.set_aspect('equal')
fig.tight_layout(pad=0.3)
```

### Magnitude and direction

::: key Magnitude and direction of a vector
For $\vec{a}=\binom{x}{y}$:
$$ |\vec{a}|=\sqrt{x^2+y^2} \qquad\qquad \tan\theta=\frac{y}{x} $$
The **magnitude** $|\vec{a}|$ (also called the modulus or length) comes from Pythagoras' theorem. The **direction** $\theta$ is the angle the vector makes with the positive $x$-direction, measured anticlockwise. Find the quadrant from the signs of $x$ and $y$ first, then the angle.
:::

The direction needs care, because $\tan\theta$ has the same value in two opposite quadrants. Use the signs of the components:

| Signs of $x$, $y$ | Quadrant | Direction $\theta$ (with $\alpha$ the acute angle with $\tan\alpha=\left|\frac{y}{x}\right|$) |
|---|---|---|
| $+$, $+$ | I | $\theta=\alpha$ |
| $-$, $+$ | II | $\theta=180^\circ-\alpha$ |
| $-$, $-$ | III | $\theta=180^\circ+\alpha$ |
| $+$, $-$ | IV | $\theta=360^\circ-\alpha$ |

::: example A vector from two points
**Problem.** Find $\overrightarrow{AB}$, its magnitude and its direction for $A(1,2)$ and $B(4,6)$.

**Solution.** Head minus tail:
$$ \overrightarrow{AB}=\binom{4-1}{6-2}=\binom{3}{4},\qquad |\overrightarrow{AB}|=\sqrt{3^2+4^2}=\sqrt{25}=5 \text{ units} $$
Both components are positive, so the vector points into the first quadrant, with $\tan\theta=\frac{4}{3}$. A calculator gives $\theta\approx53.13^\circ$. This is also Ram's walk: 3 km east and 4 km north is a displacement of 5 km at about $53^\circ$ north of east.
:::

::: example Directions using standard angles
**Problem.** Find the magnitude and direction of (i) $\vec{a}=\binom{2}{2}$ (ii) $\vec{b}=\binom{-\sqrt{3}}{1}$ (iii) $\vec{c}=\binom{1}{-\sqrt{3}}$ (iv) $\vec{d}=\binom{0}{-3}$.

**Solution.** (i) $|\vec{a}|=\sqrt{4+4}=2\sqrt{2}$. Quadrant I, $\tan\theta=1$, so $\theta=45^\circ$.

(ii) $|\vec{b}|=\sqrt{3+1}=2$. $x<0$, $y>0$: quadrant II. The acute angle has $\tan\alpha=\frac{1}{\sqrt{3}}$, so $\alpha=30^\circ$ and $\theta=180^\circ-30^\circ=150^\circ$.

(iii) $|\vec{c}|=\sqrt{1+3}=2$. $x>0$, $y<0$: quadrant IV, with $\tan\alpha=\sqrt{3}$, $\alpha=60^\circ$. So $\theta=360^\circ-60^\circ=300^\circ$ (or $-60^\circ$, measured clockwise).

(iv) $|\vec{d}|=3$, pointing straight down: $\theta=270^\circ$.
:::

### Directions and compass bearings

In geography and in map work (see "Bearing and Scale Drawing" in your compulsory mathematics book) a direction is given as a **bearing**: an angle measured **clockwise from north**, written with three figures. In vector work the direction is measured **anticlockwise from the positive $x$-direction (east)**. The two are easily changed into each other when you draw the arrow: for a direction in the first quadrant, the vector angle is $90^\circ$ minus the bearing.

::: example From a bearing to components
**Problem.** A helicopter flies 10 km from Lukla on a bearing of $060^\circ$. Write its displacement as a column vector, taking east and north as the $x$- and $y$-directions.

**Solution.** A bearing of $060^\circ$ is $60^\circ$ clockwise from north, which is $90^\circ-60^\circ=30^\circ$ anticlockwise from east. The components are the base and perpendicular of a right triangle with hypotenuse 10 km and angle $30^\circ$:
$$ x=10\cos30^\circ=5\sqrt{3}\approx8.66 \text{ km},\qquad y=10\sin30^\circ=5 \text{ km} $$
So the displacement is about $\binom{8.66}{5}$ km: 8.66 km east and 5 km north. Check: $\sqrt{75+25}=10$ ✓.
:::

::: caution The arrow goes from the first letter to the second
$\overrightarrow{AB}$ is "head minus tail", $B-A$. Working out $A-B$ gives $\overrightarrow{BA}$, which has the same length but points the opposite way. Every component then has the wrong sign, and so does the direction.
:::

## 8.2 Types of vectors: row, column, position, unit, null, equal and negative vectors; like and unlike vectors

### Row and column vectors

The two components can be written in a column, $\binom{3}{4}$, called a **column vector**, or in a row, $(3,\ 4)$, called a **row vector**. Both describe the same displacement: 3 across and 4 up. Books on vectors usually use column vectors, so that a vector is not confused with the coordinates of a point; this book does the same.

### Position vector

::: definition Position vector
The **position vector** of a point $P(x,y)$ is the vector $\overrightarrow{OP}$ from the origin $O$ to $P$:
$$ \overrightarrow{OP}=\binom{x}{y} $$
:::

The components of a position vector are just the coordinates of the point. For $A$ and $B$ with position vectors $\vec{a}=\overrightarrow{OA}$ and $\vec{b}=\overrightarrow{OB}$, the rule "head minus tail" becomes $\overrightarrow{AB}=\vec{b}-\vec{a}$.

### Unit vector and null vector

A **unit vector** is a vector of magnitude 1. The unit vector in the direction of $\vec{a}$ is written $\hat{a}$ ("$a$ hat"); it is found by dividing $\vec{a}$ by its own magnitude:
$$ \hat{a}=\frac{\vec{a}}{|\vec{a}|} $$
The unit vectors along the axes are $\hat{i}=\binom{1}{0}$ and $\hat{j}=\binom{0}{1}$; every vector $\binom{x}{y}$ can be written as $x\hat{i}+y\hat{j}$.

A **null (zero) vector** $\vec{0}=\binom{0}{0}$ has magnitude 0 and no definite direction. $\overrightarrow{AA}$, the "journey" from a point to itself, is a null vector.

### Equal and negative vectors

::: definition Equal vectors and the negative of a vector
Two vectors are **equal** if they have the **same magnitude and the same direction**; then their components are equal. The **negative** of $\vec{a}$, written $-\vec{a}$, has the **same magnitude** as $\vec{a}$ but the **opposite direction**: if $\vec{a}=\binom{x}{y}$, then $-\vec{a}=\binom{-x}{-y}$. In particular $\overrightarrow{BA}=-\overrightarrow{AB}$.
:::

Equal vectors need not start at the same point. A vector says how far and which way, not where.

### Like and unlike vectors

Vectors that are parallel and point the **same way** are **like vectors**; parallel vectors that point in **opposite ways** are **unlike vectors**. Their lengths may differ. $\binom{2}{1}$ and $\binom{4}{2}$ are like vectors; $\binom{2}{1}$ and $\binom{-6}{-3}$ are unlike vectors.

```figure caption="Types of vector on a grid. (1) The position vector $\overrightarrow{OP}$ of $P(3,2)$, with the unit vectors $\hat{i}$ and $\hat{j}$. (2) Two equal vectors: same length, same direction, different places. (3) $\overrightarrow{AB}$ and its negative $\overrightarrow{BA}$. (4) Like vectors point the same way; unlike vectors point opposite ways."
fig, axs = plt.subplots(2, 2, figsize=(5.0, 4.0))
kw = dict(arrowstyle='-|>', lw=1.8, mutation_scale=11)
def arrow(ax, p, q, c):
    ax.annotate('', xy=q, xytext=p, arrowprops=dict(color=c, **kw))
ax = axs[0, 0]
arrow(ax, (0, 0), (3, 2), ACCENT); arrow(ax, (0, 0), (1, 0), SERIES[1]); arrow(ax, (0, 0), (0, 1), SERIES[2])
ax.plot(3, 2, 'o', color=INK, ms=4); ax.text(3.15, 2.1, 'P(3, 2)', fontsize=8)
ax.text(1.0, 1.25, 'OP', fontsize=8.5, color=ACCENT); ax.text(0.55, -0.45, 'î', fontsize=9, color=SERIES[1]); ax.text(-0.45, 0.4, 'ĵ', fontsize=9, color=SERIES[2])
ax.text(-0.35, -0.45, 'O', fontsize=8)
ax.set_title('(1) position vector', fontsize=8.5, pad=2)
ax = axs[0, 1]
arrow(ax, (0, 0), (3, 2), ACCENT); arrow(ax, (1, -2), (4, 0), ACCENT)
ax.text(1.0, 1.2, 'a', fontsize=9, color=ACCENT); ax.text(2.0, -1.55, 'a', fontsize=9, color=ACCENT)
ax.set_title('(2) equal vectors', fontsize=8.5, pad=2)
ax = axs[1, 0]
arrow(ax, (0, 1), (3, 3), ACCENT); arrow(ax, (3, 0), (0, -2), SERIES[1])
ax.text(0.9, 2.35, 'AB', fontsize=8.5, color=ACCENT); ax.text(2.2, -2.45, 'BA = −AB', fontsize=8.5, color=SERIES[1], ha='center')
ax.set_title('(3) negative vectors', fontsize=8.5, pad=2)
ax = axs[1, 1]
arrow(ax, (0, 2), (2, 3), ACCENT); arrow(ax, (0, 0), (4, 2), ACCENT); arrow(ax, (4, -0.5), (1, -2), SERIES[1])
ax.text(0.5, 2.85, 'a', fontsize=9, color=ACCENT); ax.text(2.4, 0.65, '2a  (like)', fontsize=8.5, color=ACCENT)
ax.text(2.3, -2.15, '−1.5a  (unlike)', fontsize=8.5, color=SERIES[1])
ax.set_title('(4) like and unlike', fontsize=8.5, pad=2)
for ax in axs.flat:
    ax.set_xlim(-0.8, 5.2); ax.set_ylim(-2.8, 3.6); ax.set_aspect('equal')
    ax.set_xticks(range(0, 6)); ax.set_yticks(range(-2, 4))
    ax.tick_params(labelbottom=False, labelleft=False, length=0)
    ax.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
    for s in ax.spines.values(): s.set_visible(False)
fig.tight_layout(pad=0.4)
```

::: example A unit vector
**Problem.** Find the unit vector in the direction of $\vec{a}=\binom{3}{-4}$, and check that its magnitude is 1.

**Solution.** $|\vec{a}|=\sqrt{9+16}=5$, so
$$ \hat{a}=\frac{1}{5}\binom{3}{-4}=\binom{\frac{3}{5}}{-\frac{4}{5}} $$
Check: $\sqrt{\left(\frac{3}{5}\right)^2+\left(-\frac{4}{5}\right)^2}=\sqrt{\frac{9+16}{25}}=1$ ✓.
:::

::: example Equal vectors
**Problem.** (i) Find $x$ and $y$ if $\binom{x+1}{5}=\binom{4}{y-2}$. (ii) Show that for $A(1,1)$, $B(4,3)$, $C(2,5)$ and $D(5,7)$, $\overrightarrow{AB}=\overrightarrow{CD}$. What kind of figure is $ABDC$?

**Solution.** (i) Equal vectors have equal components: $x+1=4$, so $x=3$; $5=y-2$, so $y=7$.

(ii) $\overrightarrow{AB}=\binom{4-1}{3-1}=\binom{3}{2}$ and $\overrightarrow{CD}=\binom{5-2}{7-5}=\binom{3}{2}$. So $\overrightarrow{AB}=\overrightarrow{CD}$: the segments $AB$ and $CD$ are equal in length and parallel. A quadrilateral with one pair of opposite sides equal and parallel is a **parallelogram**, so $ABDC$ is a parallelogram.
:::

::: example Naming the types
**Problem.** For $\vec{p}=\binom{2}{1}$, $\vec{q}=\binom{-4}{-2}$, $\vec{r}=\binom{6}{3}$, $\vec{s}=\binom{0}{1}$ and $\vec{t}=\binom{0}{0}$, say which vectors are like, which are unlike, which are unit vectors and which is null.

**Solution.** $\vec{r}=3\vec{p}$, so $\vec{p}$ and $\vec{r}$ are **like**. $\vec{q}=-2\vec{p}$, so $\vec{q}$ is **unlike** $\vec{p}$ (and unlike $\vec{r}$). $|\vec{s}|=1$, so $\vec{s}$ is a **unit vector** ($\hat{j}$). $\vec{t}$ is the **null vector**.
:::

## 8.3 Multiplication of a vector by a scalar; condition for parallel vectors

### Scalar multiples

Multiplying a vector by a number (a scalar) stretches or shrinks it, and a negative number also turns it round.

::: definition Scalar multiple of a vector
If $\vec{a}=\binom{x}{y}$ and $k$ is a scalar, then
$$ k\vec{a}=\binom{kx}{ky},\qquad |k\vec{a}|=|k|\,|\vec{a}| $$
If $k>0$, $k\vec{a}$ has the same direction as $\vec{a}$; if $k<0$, the opposite direction; if $k=0$, $k\vec{a}$ is the null vector.
:::

```figure caption="Scalar multiples of $\vec{a}=\binom{2}{1}$. $2\vec{a}$ is twice as long in the same direction, $\frac{1}{2}\vec{a}$ half as long, and $-\vec{a}$ the same length in the opposite direction. All of them are parallel to $\vec{a}$."
fig, ax = plt.subplots(figsize=(4.8, 2.8))
kw = dict(arrowstyle='-|>', lw=1.9, mutation_scale=12)
for (p, q, c, lab, lp) in [((0, 0), (2, 1), ACCENT, 'a', (0.75, 0.75)), ((3, 0), (7, 2), SERIES[2], '2a', (4.7, 1.35)),
                           ((8, 0), (9, 0.5), SERIES[3], '½a', (8.1, 0.65)), ((12, 1), (10, 0), SERIES[1], '−a', (10.7, 0.75))]:
    ax.annotate('', xy=q, xytext=p, arrowprops=dict(color=c, **kw))
    ax.text(lp[0], lp[1], lab, fontsize=10, color=c)
ax.set_xlim(-0.5, 12.5); ax.set_ylim(-0.8, 2.8); ax.set_aspect('equal')
ax.set_xticks(range(0, 13)); ax.set_yticks(range(0, 3))
ax.tick_params(labelbottom=False, labelleft=False, length=0)
ax.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
for s in ax.spines.values(): s.set_visible(False)
fig.tight_layout(pad=0.3)
```

::: example Multiplying by scalars
**Problem.** If $\vec{a}=\binom{2}{-1}$, find $3\vec{a}$, $-2\vec{a}$, $\frac{1}{2}\vec{a}$ and $|3\vec{a}|$.

**Solution.**
$$ 3\vec{a}=\binom{6}{-3},\qquad -2\vec{a}=\binom{-4}{2},\qquad \frac{1}{2}\vec{a}=\binom{1}{-\frac{1}{2}} $$
$|\vec{a}|=\sqrt{4+1}=\sqrt{5}$, so $|3\vec{a}|=3\sqrt{5}$. Check directly: $\sqrt{36+9}=\sqrt{45}=3\sqrt{5}$ ✓.
:::

### The condition for parallel vectors

Two non-zero vectors are parallel when one is a scalar multiple of the other.

::: key Condition for parallel vectors
$\vec{a}=\binom{x_1}{y_1}$ and $\vec{b}=\binom{x_2}{y_2}$ are **parallel** if $\vec{a}=k\vec{b}$ for some scalar $k$, that is, when
$$ \frac{x_1}{x_2}=\frac{y_1}{y_2}\qquad\text{or, without fractions,}\qquad x_1y_2-x_2y_1=0 $$
If $k>0$ they are **like** vectors; if $k<0$ they are **unlike**.
:::

::: example Testing for parallel vectors
**Problem.** (i) Show that $\binom{2}{-3}$ and $\binom{-4}{6}$ are parallel. Are they like or unlike? (ii) Find $k$ if $\binom{2}{k}$ is parallel to $\binom{6}{9}$. (iii) Find $p$ if $\binom{p}{4}$ and $\binom{3}{6}$ are parallel.

**Solution.** (i) $\binom{-4}{6}=-2\binom{2}{-3}$. The scalar is negative, so they are parallel and **unlike**. (Check: $2\times6-(-4)\times(-3)=12-12=0$.)

(ii) $2\times9-6\times k=0$ gives $18=6k$, so $k=3$. Check: $\binom{6}{9}=3\binom{2}{3}$ ✓.

(iii) $p\times6-3\times4=0$ gives $p=2$.
:::

::: example Collinear points by vectors
**Problem.** Show that $A(1,2)$, $B(3,6)$ and $C(4,8)$ are collinear.

**Solution.** $\overrightarrow{AB}=\binom{2}{4}$ and $\overrightarrow{BC}=\binom{1}{2}$. Since $\overrightarrow{AB}=2\overrightarrow{BC}$, the two vectors are parallel. They also share the point $B$, so $A$, $B$ and $C$ lie on one straight line. (You proved the same fact with distances and slopes in chapter 6.)
:::

## 8.4 Addition and subtraction of vectors

### Adding by components

To add vectors, add the corresponding components:
$$ \binom{x_1}{y_1}+\binom{x_2}{y_2}=\binom{x_1+x_2}{y_1+y_2} $$
This makes sense as journeys: going $x_1$ across and $y_1$ up, then $x_2$ across and $y_2$ up, is the same as going $x_1+x_2$ across and $y_1+y_2$ up. The sum is called the **resultant**.

### The triangle law and the parallelogram law

```figure caption="Two ways to draw $\vec{a}+\vec{b}$ for $\vec{a}=\binom{3}{1}$ and $\vec{b}=\binom{1}{2}$. Left, the triangle law: put the tail of $\vec{b}$ at the head of $\vec{a}$; the sum goes from the first tail to the last head. Right, the parallelogram law: draw both from one point; the sum is the diagonal from that point. Either way $\vec{a}+\vec{b}=\binom{4}{3}$."
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.0, 2.7))
kw = dict(arrowstyle='-|>', lw=1.9, mutation_scale=12)
def arr(ax, p, q, c, ls='-'):
    ax.annotate('', xy=q, xytext=p, arrowprops=dict(color=c, linestyle=ls, **kw))
arr(ax1, (0, 0), (3, 1), ACCENT); arr(ax1, (3, 1), (4, 3), SERIES[2]); arr(ax1, (0, 0), (4, 3), SERIES[1])
ax1.text(1.6, 0.15, 'a', fontsize=10, color=ACCENT); ax1.text(3.65, 1.75, 'b', fontsize=10, color=SERIES[2])
ax1.text(1.3, 1.6, 'a + b', fontsize=9.5, color=SERIES[1])
ax1.set_title('triangle law', fontsize=8.5, pad=2)
arr(ax2, (0, 0), (3, 1), ACCENT); arr(ax2, (0, 0), (1, 2), SERIES[2]); arr(ax2, (0, 0), (4, 3), SERIES[1])
ax2.plot([3, 4], [1, 3], color=MUTED, lw=1.0, ls='--'); ax2.plot([1, 4], [2, 3], color=MUTED, lw=1.0, ls='--')
ax2.text(1.6, 0.15, 'a', fontsize=10, color=ACCENT); ax2.text(0.15, 1.3, 'b', fontsize=10, color=SERIES[2])
ax2.text(2.5, 1.3, 'a + b', fontsize=9.5, color=SERIES[1], ha='center', va='center')
ax2.set_title('parallelogram law', fontsize=8.5, pad=2)
for ax in (ax1, ax2):
    ax.set_xlim(-0.5, 4.8); ax.set_ylim(-0.6, 3.6); ax.set_aspect('equal')
    ax.set_xticks(range(0, 5)); ax.set_yticks(range(0, 4))
    ax.tick_params(labelbottom=False, labelleft=False, length=0)
    ax.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
    for s in ax.spines.values(): s.set_visible(False)
fig.tight_layout(pad=0.4)
```

::: definition Triangle law and parallelogram law of vector addition
**Triangle law.** If two vectors are represented by two sides of a triangle taken in order ($\overrightarrow{AB}$ and $\overrightarrow{BC}$), their sum is represented by the third side taken from the start to the end:
$$ \overrightarrow{AB}+\overrightarrow{BC}=\overrightarrow{AC} $$
**Parallelogram law.** If two vectors are represented by two adjacent sides of a parallelogram drawn from the same point, their sum is represented by the diagonal through that point.
:::

### Subtraction

Subtracting a vector is adding its negative:
$$ \vec{a}-\vec{b}=\vec{a}+(-\vec{b})=\binom{x_1-x_2}{y_1-y_2} $$
This gives a short proof of "head minus tail": by the triangle law $\overrightarrow{OA}+\overrightarrow{AB}=\overrightarrow{OB}$, so $\overrightarrow{AB}=\overrightarrow{OB}-\overrightarrow{OA}=\vec{b}-\vec{a}$.

Subtraction can be drawn too. Draw $\vec{a}$ and $\vec{b}$ from the **same point**. Then $\vec{a}-\vec{b}$ is the vector from the **head of $\vec{b}$ to the head of $\vec{a}$**, because going along $\vec{b}$ and then along that vector lands at the head of $\vec{a}$: $\vec{b}+(\vec{a}-\vec{b})=\vec{a}$. In the parallelogram of the figure above, one diagonal is $\vec{a}+\vec{b}$ and the other diagonal is $\vec{a}-\vec{b}$. For $\vec{a}=\binom{3}{1}$ and $\vec{b}=\binom{1}{2}$, the heads are at $(3,1)$ and $(1,2)$, and the vector from $(1,2)$ to $(3,1)$ is $\binom{2}{-1}=\vec{a}-\vec{b}$ ✓.

### Properties of vector addition

| Property | Statement |
|---|---|
| Commutative | $\vec{a}+\vec{b}=\vec{b}+\vec{a}$ (the two routes round a parallelogram) |
| Associative | $(\vec{a}+\vec{b})+\vec{c}=\vec{a}+(\vec{b}+\vec{c})$ |
| Identity | $\vec{a}+\vec{0}=\vec{a}$ |
| Inverse | $\vec{a}+(-\vec{a})=\vec{0}$ |

::: example Sums, differences and combinations
**Problem.** If $\vec{a}=\binom{3}{1}$ and $\vec{b}=\binom{1}{2}$, find $\vec{a}+\vec{b}$, $|\vec{a}+\vec{b}|$, $\vec{a}-\vec{b}$ and $2\vec{a}+3\vec{b}$. Compare $|\vec{a}+\vec{b}|$ with $|\vec{a}|+|\vec{b}|$.

**Solution.**
$$ \vec{a}+\vec{b}=\binom{4}{3},\qquad |\vec{a}+\vec{b}|=\sqrt{16+9}=5,\qquad \vec{a}-\vec{b}=\binom{2}{-1} $$
$$ 2\vec{a}+3\vec{b}=\binom{6}{2}+\binom{3}{6}=\binom{9}{8} $$
$|\vec{a}|+|\vec{b}|=\sqrt{10}+\sqrt{5}\approx3.16+2.24=5.40$, which is **more** than $|\vec{a}+\vec{b}|=5$. Two sides of a triangle are together longer than the third, so magnitudes do not simply add (unless the vectors are like).
:::

::: example The triangle law with coordinates
**Problem.** For $A(2,1)$, $B(5,3)$ and $C(4,7)$, verify that $\overrightarrow{AB}+\overrightarrow{BC}=\overrightarrow{AC}$.

**Solution.** $\overrightarrow{AB}=\binom{3}{2}$, $\overrightarrow{BC}=\binom{-1}{4}$ and $\overrightarrow{AC}=\binom{2}{6}$. Then $\overrightarrow{AB}+\overrightarrow{BC}=\binom{3-1}{2+4}=\binom{2}{6}=\overrightarrow{AC}$ ✓.
:::

::: example A trek and a pair of forces
**Problem.** (i) A trekker in Mustang walks 6 km east and then 8 km north. Find the magnitude and direction of her displacement. (ii) Two forces $\binom{3}{4}$ N and $\binom{5}{-2}$ N act on a box. Find the resultant force and its magnitude.

**Solution.** (i) The displacement is $\binom{6}{0}+\binom{0}{8}=\binom{6}{8}$, with magnitude $\sqrt{36+64}=10$ km. Its direction has $\tan\theta=\frac{8}{6}=\frac{4}{3}$, so $\theta\approx53.13^\circ$ north of east. She has walked 14 km but is only 10 km from her start.

(ii) Resultant $=\binom{3+5}{4-2}=\binom{8}{2}$ N, with magnitude $\sqrt{64+4}=\sqrt{68}=2\sqrt{17}\approx8.25$ N.
:::

::: example Solving a vector equation
**Problem.** If $\vec{a}=\binom{2}{5}$ and $\vec{b}=\binom{-1}{3}$, find the vector $\vec{x}$ such that $\vec{a}+\vec{x}=\vec{b}$, and the vector $\vec{y}$ such that $2\vec{y}-\vec{a}=\vec{b}$.

**Solution.** $\vec{x}=\vec{b}-\vec{a}=\binom{-1-2}{3-5}=\binom{-3}{-2}$.

$2\vec{y}=\vec{a}+\vec{b}=\binom{1}{8}$, so $\vec{y}=\binom{\frac{1}{2}}{4}$. Check: $2\vec{y}-\vec{a}=\binom{1-2}{8-5}=\binom{-1}{3}=\vec{b}$ ✓.
:::

::: caution Add components, not magnitudes
$\binom{3}{1}+\binom{1}{2}$ is $\binom{4}{3}$, with magnitude 5, not $\sqrt{10}+\sqrt{5}$. Find the resultant **vector** first, then its magnitude. Adding lengths gives the right answer only when the vectors point the same way.
:::

::: tip Draw the arrows before you calculate
A quick sketch on squared paper shows roughly where the resultant points and how long it is. If your calculated answer points into a different quadrant, or is longer than the two arrows put end to end, look for a sign error.
:::

::: note Activity — a treasure hunt in vectors
In the school ground, mark a starting peg $O$ and let east and north be the $x$- and $y$-directions, with 1 step as the unit. Write a route as a list of vectors, for example $\binom{5}{0}$, $\binom{0}{3}$, $\binom{-2}{4}$, $\binom{4}{-1}$, and hide a "treasure" at the end. (1) A partner walks the route step by step. (2) Add the vectors to find the single vector from $O$ to the treasure, and its magnitude. (3) Walk the single vector directly. Do both routes end at the same place? (They should: the resultant here is $\binom{7}{6}$, about 9.2 steps.)
:::

## Chapter summary

- A **scalar** has magnitude only (mass, distance, speed); a **vector** has magnitude and direction (displacement, velocity, force).
- $\overrightarrow{AB}=\binom{x_2-x_1}{y_2-y_1}$ (head minus tail); $|\vec{a}|=\sqrt{x^2+y^2}$; direction $\tan\theta=\frac{y}{x}$, with the quadrant fixed by the signs.
- Position vector $\overrightarrow{OP}=\binom{x}{y}$; unit vector $\hat{a}=\frac{\vec{a}}{|\vec{a}|}$; null vector $\binom{0}{0}$; $\hat{i}=\binom{1}{0}$, $\hat{j}=\binom{0}{1}$.
- **Equal** vectors: same magnitude and direction (equal components); **negative** $-\vec{a}$: same magnitude, opposite direction; $\overrightarrow{BA}=-\overrightarrow{AB}$.
- $k\vec{a}=\binom{kx}{ky}$, $|k\vec{a}|=|k||\vec{a}|$; parallel: $\vec{a}=k\vec{b}$, i.e. $x_1y_2-x_2y_1=0$; like if $k>0$, unlike if $k<0$.
- $\vec{a}\pm\vec{b}=\binom{x_1\pm x_2}{y_1\pm y_2}$; triangle law $\overrightarrow{AB}+\overrightarrow{BC}=\overrightarrow{AC}$; parallelogram law; $\overrightarrow{AB}=\vec{b}-\vec{a}$.
- Addition is commutative and associative, with identity $\vec{0}$ and inverse $-\vec{a}$; magnitudes do not add unless the vectors are like.

## Practice questions

**Group A — Objective (1 mark each)**

1. Which of these is a vector quantity? <span class="marks">[1]</span>
   (a) mass (b) temperature (c) displacement (d) time
2. Which of these is a scalar quantity? <span class="marks">[1]</span>
   (a) force (b) velocity (c) speed (d) acceleration
3. The magnitude of $\binom{3}{4}$ is <span class="marks">[1]</span>
   (a) 7 (b) 5 (c) 25 (d) 1
4. If $A$ is $(1,2)$ and $B$ is $(4,6)$, then $\overrightarrow{AB}$ is <span class="marks">[1]</span>
   (a) $\binom{3}{4}$ (b) $\binom{5}{8}$ (c) $\binom{-3}{-4}$ (d) $\binom{4}{3}$
5. The position vector of the point $P(-2,5)$ is <span class="marks">[1]</span>
   (a) $\binom{-2}{5}$ (b) $\binom{2}{-5}$ (c) $\binom{5}{-2}$ (d) $\binom{-5}{2}$
6. A unit vector has magnitude <span class="marks">[1]</span>
   (a) 0 (b) 1 (c) 2 (d) any number
7. The negative of $\binom{2}{-3}$ is <span class="marks">[1]</span>
   (a) $\binom{-2}{3}$ (b) $\binom{2}{3}$ (c) $\binom{-2}{-3}$ (d) $\binom{3}{-2}$
8. If $\binom{x}{4}=\binom{3}{y}$, then $x+y$ is <span class="marks">[1]</span>
   (a) 7 (b) 1 (c) 12 (d) $-1$
9. $3\binom{2}{-1}$ is equal to <span class="marks">[1]</span>
   (a) $\binom{6}{-3}$ (b) $\binom{5}{2}$ (c) $\binom{6}{-1}$ (d) $\binom{2}{-3}$
10. The vectors $\binom{2}{k}$ and $\binom{4}{6}$ are parallel when $k$ is <span class="marks">[1]</span>
    (a) 2 (b) 3 (c) 4 (d) 12
11. $\binom{1}{2}+\binom{3}{-5}$ is equal to <span class="marks">[1]</span>
    (a) $\binom{4}{-3}$ (b) $\binom{4}{7}$ (c) $\binom{-2}{7}$ (d) $\binom{3}{-10}$
12. $\overrightarrow{AB}+\overrightarrow{BC}$ is equal to <span class="marks">[1]</span>
    (a) $\overrightarrow{CA}$ (b) $\overrightarrow{AC}$ (c) $\overrightarrow{BA}$ (d) $\vec{0}$

::: note Answers to Group A
**1.** (c) — displacement has a direction; the others do not.
**2.** (c) — speed is the size of velocity without its direction.
**3.** (b) — $\sqrt{9+16}=5$.
**4.** (a) — head minus tail: $\binom{4-1}{6-2}$.
**5.** (a) — the components of a position vector are the coordinates of the point.
**6.** (b) — by definition.
**7.** (a) — change the sign of both components.
**8.** (a) — $x=3$, $y=4$, so $x+y=7$.
**9.** (a) — multiply both components by 3.
**10.** (b) — $2\times6-4k=0$, so $k=3$.
**11.** (a) — $\binom{1+3}{2-5}$.
**12.** (b) — the triangle law.
:::

**Group B — Short answer (2 marks each)**

1. Write two differences between scalar and vector quantities, with one example of each. <span class="marks">[2]</span>
2. If $A$ is $(-1,3)$ and $B$ is $(2,7)$, find $\overrightarrow{AB}$ and $|\overrightarrow{AB}|$. <span class="marks">[2]</span>
3. Find the magnitude and direction of $\vec{a}=\binom{2}{2}$. <span class="marks">[2]</span>
4. Find the unit vector in the direction of $\binom{3}{-4}$. <span class="marks">[2]</span>
5. Find $x$ and $y$ if $\binom{2x-1}{5}=\binom{7}{y+2}$. <span class="marks">[2]</span>
6. If $\vec{a}=\binom{2}{-1}$, find $3\vec{a}$, $-2\vec{a}$ and $|3\vec{a}|$. <span class="marks">[2]</span>
7. Show that $\binom{2}{-3}$ and $\binom{-4}{6}$ are parallel, and say whether they are like or unlike. <span class="marks">[2]</span>
8. Find $k$ if $\binom{k}{4}$ and $\binom{3}{6}$ are parallel. <span class="marks">[2]</span>
9. If $\vec{a}=\binom{3}{1}$ and $\vec{b}=\binom{1}{2}$, find $\vec{a}+\vec{b}$ and $|\vec{a}+\vec{b}|$. <span class="marks">[2]</span>
10. If $\vec{p}=\binom{5}{-2}$ and $\vec{q}=\binom{2}{3}$, find $2\vec{p}-\vec{q}$. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** A scalar has magnitude only, a vector has magnitude and direction; two scalars are added as ordinary numbers, but vectors are added by the triangle law (by components). Examples: mass 5 kg (scalar); a force of 10 N upwards (vector).
**2.** $\overrightarrow{AB}=\binom{2+1}{7-3}=\binom{3}{4}$ and $|\overrightarrow{AB}|=\sqrt{9+16}=5$ units.
**3.** $|\vec{a}|=\sqrt{4+4}=2\sqrt{2}$. Both components are positive and $\tan\theta=\frac{2}{2}=1$, so $\theta=45^\circ$.
**4.** $|\vec{a}|=5$, so $\hat{a}=\binom{\frac{3}{5}}{-\frac{4}{5}}$.
**5.** $2x-1=7$ gives $x=4$; $5=y+2$ gives $y=3$.
**6.** $3\vec{a}=\binom{6}{-3}$, $-2\vec{a}=\binom{-4}{2}$, and $|3\vec{a}|=3\sqrt{5}$ (since $|\vec{a}|=\sqrt{5}$).
**7.** $\binom{-4}{6}=-2\binom{2}{-3}$: parallel, and **unlike** because the scalar $-2$ is negative.
**8.** $k\times6-3\times4=0$, so $k=2$.
**9.** $\vec{a}+\vec{b}=\binom{4}{3}$ and $|\vec{a}+\vec{b}|=\sqrt{16+9}=5$.
**10.** $2\vec{p}=\binom{10}{-4}$, so $2\vec{p}-\vec{q}=\binom{10-2}{-4-3}=\binom{8}{-7}$.
:::

**Group C — Long answer (4 marks each)**

1. A trekker walks 6 km east and then 8 km north. (i) Write the two walks as column vectors and draw their sum by the triangle law. (ii) Find the distance walked and the magnitude of the displacement. (iii) Find the direction of the displacement. <span class="marks">[4]</span>
2. If $\vec{a}=\binom{3}{1}$, $\vec{b}=\binom{1}{2}$ and $\vec{c}=\binom{-2}{4}$: (i) verify that $\vec{a}+\vec{b}=\vec{b}+\vec{a}$; (ii) verify that $(\vec{a}+\vec{b})+\vec{c}=\vec{a}+(\vec{b}+\vec{c})$; (iii) find $|\vec{a}+\vec{b}+\vec{c}|$. <span class="marks">[4]</span>
3. The points $A(1,1)$, $B(4,3)$, $C(5,6)$ and $D(2,4)$ are given. (i) Show that $\overrightarrow{AB}=\overrightarrow{DC}$ and say what this tells you about $ABCD$. (ii) Verify the parallelogram law $\overrightarrow{AB}+\overrightarrow{AD}=\overrightarrow{AC}$. (iii) Find $\overrightarrow{BD}$ and show that it equals $\overrightarrow{AD}-\overrightarrow{AB}$. <span class="marks">[4]</span>
4. Find the magnitude and direction of (i) $\binom{\sqrt{3}}{1}$ (ii) $\binom{-1}{\sqrt{3}}$ (iii) $\binom{0}{-5}$, and draw each on a grid. <span class="marks">[4]</span>
5. (i) Using vectors, show that $A(1,2)$, $B(3,6)$ and $C(4,8)$ are collinear. (ii) Find $p$ if $P(2,3)$, $Q(5,9)$ and $R(p,13)$ are collinear. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** (i) $\binom{6}{0}$ and $\binom{0}{8}$; drawn head to tail, the resultant runs from the start to the end: $\binom{6}{0}+\binom{0}{8}=\binom{6}{8}$. (ii) Distance walked $=6+8=14$ km; displacement $=\sqrt{36+64}=10$ km. (iii) $\tan\theta=\frac{8}{6}=\frac{4}{3}$, so $\theta\approx53.13^\circ$ north of east.
**2.** (i) $\vec{a}+\vec{b}=\binom{4}{3}$ and $\vec{b}+\vec{a}=\binom{1+3}{2+1}=\binom{4}{3}$; equal. (ii) $(\vec{a}+\vec{b})+\vec{c}=\binom{4-2}{3+4}=\binom{2}{7}$; $\vec{b}+\vec{c}=\binom{-1}{6}$, so $\vec{a}+(\vec{b}+\vec{c})=\binom{3-1}{1+6}=\binom{2}{7}$; equal. (iii) $|\vec{a}+\vec{b}+\vec{c}|=\sqrt{4+49}=\sqrt{53}\approx7.28$.
**3.** (i) $\overrightarrow{AB}=\binom{3}{2}$ and $\overrightarrow{DC}=\binom{5-2}{6-4}=\binom{3}{2}$. They are equal, so $AB$ and $DC$ are equal and parallel: $ABCD$ is a parallelogram. (ii) $\overrightarrow{AD}=\binom{1}{3}$, so $\overrightarrow{AB}+\overrightarrow{AD}=\binom{4}{5}$; and $\overrightarrow{AC}=\binom{5-1}{6-1}=\binom{4}{5}$ ✓. (iii) $\overrightarrow{BD}=\binom{2-4}{4-3}=\binom{-2}{1}$ and $\overrightarrow{AD}-\overrightarrow{AB}=\binom{1-3}{3-2}=\binom{-2}{1}$ ✓.
**4.** (i) $\sqrt{3+1}=2$; quadrant I with $\tan\theta=\frac{1}{\sqrt{3}}$, so $\theta=30^\circ$. (ii) $\sqrt{1+3}=2$; $x<0$, $y>0$, quadrant II, acute angle $60^\circ$ (since $\tan\alpha=\sqrt{3}$), so $\theta=180^\circ-60^\circ=120^\circ$. (iii) Magnitude 5, pointing straight down: $\theta=270^\circ$. On the grid: (i) 1.73 right and 1 up; (ii) 1 left and 1.73 up; (iii) 5 down.
**5.** (i) $\overrightarrow{AB}=\binom{2}{4}$ and $\overrightarrow{BC}=\binom{1}{2}$, so $\overrightarrow{AB}=2\overrightarrow{BC}$: parallel with the common point $B$, hence collinear. (ii) $\overrightarrow{PQ}=\binom{3}{6}$ and $\overrightarrow{PR}=\binom{p-2}{10}$ must be parallel: $3\times10-6(p-2)=0$, so $30=6p-12$ and $p=7$. Check: $\overrightarrow{PR}=\binom{5}{10}=\frac{5}{3}\overrightarrow{PQ}$ ✓.
:::
