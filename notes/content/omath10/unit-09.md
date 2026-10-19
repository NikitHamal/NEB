---
subject: Optional Mathematics
grade: 10
unit: 9
title: Linear Programming and Transformation
hours: 0
area: Units
---

This chapter has two halves. The first uses straight-line graphs to make **decisions**: how many bags, tables or kilograms of feed should a business choose so that profit is largest or cost is smallest, when time, money and materials are limited? That is **linear programming**. The second half studies **transformations** of the plane — reflection, rotation, translation, enlargement — and shows how to combine them, how to turn points inside a circle into points outside it (**inversion**), and how a $2\times2$ matrix can carry out a whole transformation in one step.

::: key What the SEE asks from this chapter
Expect (i) the graph of a system of inequalities and the shaded solution region; (ii) a word problem in linear programming, with the constraints, the feasible region, the corner points and the optimum value (4–6 marks); (iii) the image of a point or triangle under a **combined transformation**; (iv) the inverse point $P'$ of $P$ with respect to a circle; (v) the image of a point or a figure under a given matrix, or the matrix that maps given points to given images.
:::

```photo id="omath10/warehouse" caption="A warehouse. Deciding how many shelves of each product to hold, under limits of space, money and staff, is a linear-programming problem: maximise a linear profit subject to linear constraints." width="66"
```

## 9.1 Linear inequalities in two variables and systems of inequalities

An inequality such as $ax+by+c\geq 0$ (or $>$, $\leq $, $<$) is a **linear inequality in two variables**. Its graph is a **region** of the plane bounded by the straight line $ax+by+c=0$, called the **boundary line**.

::: key How to graph a linear inequality
1. Draw the boundary line (replace the inequality sign by $=$). Use a **solid** line for $\geq $ or $\leq $ (the line belongs to the region) and a **dashed** line for $>$ or $<$.
2. Choose a **test point** not on the line — the origin $(0,0)$ if the line does not pass through it.
3. Substitute the test point. If the inequality is **true**, shade the side of the line that contains the point; if **false**, shade the other side.
:::

::: example One inequality
**Problem.** Draw the graph of $x\geq 3$.

**Solution.** The boundary line $x=3$ is vertical, through $(3,0)$. It is solid because of "$\geq $". Test $(0,0)$: $0\geq 3$ is false, so shade the side that does **not** contain the origin: the region to the **right** of the line, including the line.
:::

A **system** of inequalities is a set of two or more inequalities. Its solution is the region where all the shaded regions **overlap**.

::: example System of two inequalities
**Problem.** Draw the graph of $x-2y\geq 4$ and $2x+y\leq 8$.

**Solution.** *First line:* $x-2y=4$ passes through $(4,0)$ and $(0,-2)$. Test $(0,0)$: $0\geq 4$ is false, so shade the side **not** containing the origin (below the line).

*Second line:* $2x+y=8$ passes through $(4,0)$ and $(0,8)$. Test $(0,0)$: $0\leq 8$ is true, so shade the side **containing** the origin.

The two boundary lines meet at $(4,0)$. The solution is the overlap of the two regions, an unbounded wedge to the left and below $(4,0)$.
:::

```figure caption="The solution region of $x-2y\geq 4$ and $2x+y\leq 8$ is the shaded wedge below both lines. The lines meet at $(4,0)$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4, 3.2))
x = np.linspace(-1, 9, 200)
y1 = (x-4)/2
y2 = 8-2*x
ax.fill_between(x, -4, np.minimum(y1, y2), color='#bfdbfe', alpha=0.8)
ax.plot(x, y1, color=ACCENT, lw=1.6)
ax.plot(x, y2, color=SERIES[1], lw=1.6)
ax.plot([4], [0], 'o', color=INK, ms=4)
ax.text(4.15, 0.25, '(4, 0)', fontsize=8.5)
ax.text(7.0, 1.2, 'x − 2y = 4', color=ACCENT, fontsize=8.5)
ax.text(-0.9, 6.3, '2x + y = 8', color=SERIES[1], fontsize=8.5)
ax.text(0.5, -2.7, 'solution\nregion', fontsize=8.5)
ax.axhline(0, color=MUTED, lw=0.7); ax.axvline(0, color=MUTED, lw=0.7)
ax.set_xlim(-1, 9); ax.set_ylim(-4, 8)
ax.grid(color=GRID, lw=0.5); ax.spines[['top','right']].set_visible(False)
fig.tight_layout(pad=0.4)
```

::: example Writing inequalities from a region
**Problem.** Write the inequalities that describe the triangle with vertices $(0,0)$, $(4,0)$ and $(0,3)$ (including its boundary).

**Solution.** The triangle lies on or above the $x$-axis: $y\geq 0$; on or right of the $y$-axis: $x\geq 0$. The third side joins $(4,0)$ and $(0,3)$: its equation is $\dfrac x4+\dfrac y3=1$, i.e. $3x+4y=12$. The origin is on the region's side, and $0\leq 12$ is true. So the region is

$$ x\geq 0,\qquad y\geq 0,\qquad 3x+4y\leq 12 $$
:::

::: caution Which side to shade
Never shade by guesswork. Always test a point. A common slip is shading "above the line" automatically for $\geq $: that works only when the coefficient of $y$ is positive and you have rearranged to $y\geq \dots$.
:::

## 9.2 Linear programming: objective function, constraints and corner points

::: definition Linear programming
**Linear programming** is a mathematical method for finding the **maximum** or **minimum** value of a linear expression (the **objective function**) when the variables must satisfy a system of linear inequalities (the **constraints**).
:::

| Term | Meaning |
|---|---|
| **Decision variables** $x,y$ | the quantities we choose (number of items, kg of feed, …) |
| **Objective function** $z=px+qy$ | the profit to maximise or cost to minimise |
| **Constraints** | inequalities from limited resources, e.g. $2x+y\leq 12$ |
| **Non-negativity** | $x\geq 0,\ y\geq 0$ (we cannot make a negative number of items) |
| **Feasible region** | the overlap of all the constraint regions |
| **Corner (vertex) points** | the points where boundary lines of the feasible region meet |
| **Optimal solution** | the feasible point giving the best value of $z$ |

::: key The corner point rule
If a linear programming problem has an optimal solution, it occurs at a **corner point** of the feasible region. So: (1) find all the corner points, (2) calculate $z$ at each, (3) the largest value is the maximum and the smallest value is the minimum.
:::

Why does the optimum sit at a corner? The lines $z=px+qy=\text{constant}$ are parallel. As $z$ grows, the line slides across the plane; the last point of the feasible region that it touches before leaving is a vertex of the region (or a whole edge, which also contains two vertices).

### Steps for a word problem

1. Name the variables $x$ and $y$.
2. Write the objective function and the constraints (including $x\geq 0$, $y\geq 0$).
3. Draw the feasible region (boundary lines, test points, shade the overlap).
4. Read or solve for the corner points.
5. Evaluate $z$ at each corner; choose the maximum or minimum. Answer in words with units.

::: example A maximising problem with an algebraic objective
**Problem.** Maximise and minimise $z=2x+3y$ subject to $x+y\leq 8$, $x+3y\leq 12$, $x\geq 0$, $y\geq 0$.

**Solution.** *Boundary lines.* $x+y=8$ meets the axes at $(8,0)$ and $(0,8)$. $x+3y=12$ meets them at $(12,0)$ and $(0,4)$. The two lines intersect where $x+y=8$ and $x+3y=12$: subtracting gives $2y=4$, so $y=2$ and $x=6$: the point $(6,2)$.

*Feasible region.* The origin satisfies both inequalities, so the region is on the origin's side of each line. Its corner points are $(0,0)$, $(8,0)$, $(6,2)$ and $(0,4)$.

| Corner | $z=2x+3y$ |
|---|---|
| $(0,0)$ | $0$ |
| $(8,0)$ | $16$ |
| $(6,2)$ | $12+6=18$ |
| $(0,4)$ | $12$ |

Maximum $z=18$ at $(6,2)$; minimum $z=0$ at $(0,0)$.
:::

```figure caption="Feasible region of $x+y\leq 8$, $x+3y\leq 12$, $x,y\geq 0$. The corners are $(0,0)$, $(8,0)$, $(6,2)$, $(0,4)$; the maximum of $2x+3y$ is 18 at $(6,2)$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4, 3.0))
pts = np.array([[0, 0], [8, 0], [6, 2], [0, 4]])
ax.fill(pts[:, 0], pts[:, 1], color='#bfdbfe', alpha=0.85)
x = np.linspace(0, 12, 50)
ax.plot(x, 8-x, color=ACCENT, lw=1.4)
ax.plot(x, (12-x)/3, color=SERIES[1], lw=1.4)
xx = np.linspace(0, 9, 10)
ax.plot(xx, (18-2*xx)/3, color=INK, lw=1.0, ls='--')
labels = [('(0,0)', -0.3, -0.6), ('(8,0)', -0.1, -0.7), ('(6,2)', 0.3, 0.2), ('(0,4)', 0.25, 0.15)]
for (a, b), (n, dx, dy) in zip(pts, labels):
    ax.plot([a], [b], 'o', color=INK, ms=4)
    ax.text(a+dx, b+dy, n, fontsize=8.5)
ax.text(0.0, 6.5, '2x + 3y = 18', fontsize=8, rotation=-34)
ax.text(3.3, 5.2, 'x + y = 8', color=ACCENT, fontsize=8, rotation=-45)
ax.text(9.0, 1.1, 'x + 3y = 12', color=SERIES[1], fontsize=8, rotation=-18)
ax.set_xlim(-1, 12.6); ax.set_ylim(-1.2, 8.2)
ax.grid(color=GRID, lw=0.5); ax.spines[['top','right']].set_visible(False)
fig.tight_layout(pad=0.4)
```

::: example A profit problem (maximise)
**Problem.** A workshop in Bhaktapur makes two kinds of bags, A and B. Each bag A needs 2 hours on machine P and 1 hour on machine Q. Each bag B needs 1 hour on P and 2 hours on Q. Machine P is available for at most 12 hours a day and Q for at most 12 hours. Profit is Rs 30 on a bag A and Rs 40 on a bag B. How many of each should be made per day for maximum profit?

**Solution.** Let $x$ = number of bags A and $y$ = number of bags B.

Maximise $z=30x+40y$ subject to

$$ 2x+y\leq 12 \quad(\text{machine P}),\qquad x+2y\leq 12 \quad(\text{machine Q}),\qquad x\geq 0,\ y\geq 0 $$

*Corner points.* $2x+y=12$ meets the axes at $(6,0)$ and $(0,12)$. $x+2y=12$ meets them at $(12,0)$ and $(0,6)$. They intersect where $2x+y=12$ and $x+2y=12$: adding gives $3x+3y=24$, so $x+y=8$; subtracting gives $x-y=0$, so $x=y=4$. The feasible region has corners $(0,0)$, $(6,0)$, $(4,4)$ and $(0,6)$.

| Corner | $z=30x+40y$ (Rs) |
|---|---|
| $(0,0)$ | $0$ |
| $(6,0)$ | $180$ |
| $(4,4)$ | $120+160=280$ |
| $(0,6)$ | $240$ |

The maximum profit is **Rs 280 per day**, by making 4 bags of A and 4 bags of B.
:::

::: example A cost problem (minimise)
**Problem.** A farmer needs at least 8 units of nitrogen and at least 9 units of phosphorus for a field. Fertiliser A (Rs 4 per kg) gives 1 unit of nitrogen and 3 units of phosphorus per kg. Fertiliser B (Rs 3 per kg) gives 2 units of nitrogen and 1 unit of phosphorus per kg. How many kg of each should be bought to meet the need at least cost?

**Solution.** Let $x$ kg of A and $y$ kg of B. Minimise $z=4x+3y$ subject to

$$ x+2y\geq 8 \quad(\text{nitrogen}),\qquad 3x+y\geq 9 \quad(\text{phosphorus}),\qquad x\geq 0,\ y\geq 0 $$

*Corner points.* The region is **above** both lines (the origin fails both $\geq $ tests) and is unbounded. $x+2y=8$ meets the axes at $(8,0)$ and $(0,4)$; $3x+y=9$ meets them at $(3,0)$ and $(0,9)$. They intersect: $x=8-2y$, so $3(8-2y)+y=9\Rightarrow24-5y=9\Rightarrow y=3$, $x=2$: the point $(2,3)$. The corner points are $(0,9)$, $(2,3)$ and $(8,0)$.

| Corner | $z=4x+3y$ (Rs) |
|---|---|
| $(0,9)$ | $27$ |
| $(2,3)$ | $8+9=17$ |
| $(8,0)$ | $32$ |

The least cost is **Rs 17**, by buying 2 kg of A and 3 kg of B.
:::

::: tip The examiner is looking for
(1) $x$ and $y$ defined in words. (2) The objective function and **all** constraints, including $x,y\geq 0$. (3) A neat graph with the feasible region shaded and corner points labelled. (4) A table of $z$ at every corner. (5) A final sentence answering the question in context, with units.
:::

## 9.3 Composition of transformations

You know four basic transformations of the plane. Their effect on a point $P(x,y)$:

| Transformation | Image of $P(x,y)$ |
|---|---|
| Translation by vector $(a,b)$ | $(x+a,\ y+b)$ |
| Reflection in the $x$-axis | $(x,\,-y)$ |
| Reflection in the $y$-axis | $(-x,\,y)$ |
| Reflection in the line $y=x$ | $(y,\,x)$ |
| Reflection in the line $y=-x$ | $(-y,\,-x)$ |
| Rotation about $O$ through $90^\circ$ anticlockwise | $(-y,\,x)$ |
| Rotation about $O$ through $180^\circ$ | $(-x,\,-y)$ |
| Rotation about $O$ through $270^\circ$ anticlockwise ($90^\circ$ clockwise) | $(y,\,-x)$ |
| Enlargement, centre $O$, scale factor $k$ | $(kx,\ ky)$ |

::: definition Composition of transformations
When one transformation $T_1$ is followed by a second transformation $T_2$, the result is a **combined (composite) transformation**, written $T_2\circ T_1$: do $T_1$ **first**, then $T_2$ on the image. The composite is itself a single transformation.
:::

::: example Two translations
**Problem.** $A(2,1)$ is translated by $(0,2)$ to $A'$, then $A'$ is translated by $(-2,0)$ to $A''$. Find $A'$, $A''$ and the single translation that maps $A$ to $A''$.

**Solution.** $A'=(2+0,\ 1+2)=(2,3)$. $A''=(2-2,\ 3+0)=(0,3)$.

The single translation: $(0,3)-(2,1)=(-2,2)$, which is the **sum** $(0,2)+(-2,0)$ of the two translation vectors.
:::

::: example Reflection then rotation
**Problem.** Find the image of $P(3,2)$ under a reflection in the $x$-axis followed by a rotation of $90^\circ$ anticlockwise about the origin.

**Solution.** Reflection in the $x$-axis: $(x,y)\to(x,-y)$, so $P\to P'(3,-2)$.

Rotation by $90^\circ$ anticlockwise: $(x,y)\to(-y,x)$, so $P'(3,-2)\to P''(2,3)$.

The image is $P''(2,3)$.
:::

::: caution Order matters
Reverse the order of the two transformations and the answer usually changes. Rotating $P(3,2)$ by $90^\circ$ first gives $(-2,3)$; reflecting that in the $x$-axis gives $(-2,-3)$ — not $(2,3)$. Always apply the transformations in the order the question states.
:::

::: example A triangle under two transformations
**Problem.** The triangle $ABC$ has $A(1,1)$, $B(3,1)$, $C(1,2)$. Find its image under a reflection in the $y$-axis followed by a rotation of $90^\circ$ anticlockwise about the origin. Name the single transformation that does the same.

**Solution.** Reflection in the $y$-axis, $(x,y)\to(-x,y)$: $A'(-1,1)$, $B'(-3,1)$, $C'(-1,2)$.

Rotation $(x,y)\to(-y,x)$: $A''(-1,-1)$, $B''(-1,-3)$, $C''(-2,-1)$.

Combined effect: $(x,y)\to(-x,y)\to(-y,-x)$. The map $(x,y)\to(-y,-x)$ is the **reflection in the line $y=-x$**.
:::

```figure caption="Triangle $ABC$, its reflection in the $y$-axis $A'B'C'$, and the rotation of that image by $90^\circ$ anticlockwise $A''B''C''$. The single equivalent transformation is a reflection in $y=-x$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4, 3.6))
def tri(pts, col, name):
    p = np.array(pts + [pts[0]])
    ax.fill(p[:, 0], p[:, 1], color=col, alpha=0.25)
    ax.plot(p[:, 0], p[:, 1], color=col, lw=1.5)
    for (px, py), n in zip(pts, ['A', 'B', 'C']):
        ax.text(px + (0.1 if px >= 0 else -0.1), py + 0.12, n + name, fontsize=8, ha='left' if px >= 0 else 'right')
tri([(1, 1), (3, 1), (1, 2)], ACCENT, '')
tri([(-1, 1), (-3, 1), (-1, 2)], SERIES[1], "'")
tri([(-1, -1), (-1, -3), (-2, -1)], SERIES[2], "''")
x = np.linspace(-4, 4, 10)
ax.plot(x, -x, color=MUTED, lw=0.9, ls='--')
ax.text(2.6, -3.0, 'y = −x', fontsize=8, color=MUTED)
ax.axhline(0, color=MUTED, lw=0.7); ax.axvline(0, color=MUTED, lw=0.7)
ax.set_xlim(-4, 4.2); ax.set_ylim(-3.6, 3); ax.set_aspect('equal')
ax.grid(color=GRID, lw=0.5); ax.spines[['top','right']].set_visible(False)
fig.tight_layout(pad=0.4)
```

::: example Enlargement then translation
**Problem.** Find the image of $P(2,3)$ under an enlargement with centre $O$ and scale factor $2$, followed by a translation by $(1,-2)$.

**Solution.** Enlargement: $(2,3)\to(4,6)$. Translation: $(4,6)\to(4+1,\ 6-2)=(5,4)$.
:::

::: example Two reflections
**Problem.** Show that a reflection in the $x$-axis followed by a reflection in the $y$-axis is a rotation through $180^\circ$ about the origin.

**Solution.** For any point $(x,y)$: reflection in the $x$-axis gives $(x,-y)$; then reflection in the $y$-axis gives $(-x,-y)$. The map $(x,y)\to(-x,-y)$ is the rotation through $180^\circ$ about the origin.
:::

## 9.4 Inversion transformation and the inversion circle

::: definition Inverse point
Let $O$ be the centre and $r$ the radius of a circle. For a point $P\ne O$, the **inverse point** $P'$ is the point on the ray $OP$ such that

$$ OP\times OP'=r^2 $$

The circle is the **circle of inversion**, $O$ the **centre of inversion** and $r$ the **radius of inversion**. If $r=1$, then $OP\times OP'=1$, i.e. $OP'=\dfrac{1}{OP}$.
:::

### Properties

- Every point of the plane except the centre has exactly one inverse point.
- $O$, $P$ and $P'$ are **collinear**, with $P$ and $P'$ on the same side of $O$.
- A point on the circle is its own inverse ($r\times r=r^2$).
- If $P$ is **inside** the circle, $P'$ is **outside**, and vice versa. The nearer $P$ is to $O$, the farther $P'$ is.
- The inverse of $P'$ is $P$: the two points can be interchanged.

```figure caption="Inversion in a circle of centre $O$ and radius $r$. $P$ is inside, $P'$ is outside on the same ray, and $OP\times OP'=r^2$. Here $r=3$, $OP=1.5$, $OP'=6$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6, 3.0))
t = np.linspace(0, 2*np.pi, 300)
ax.plot(3*np.cos(t), 3*np.sin(t), color=ACCENT, lw=1.6)
d = np.array([np.cos(np.radians(25)), np.sin(np.radians(25))])
P, Pp, Q = 1.5*d, 6*d, 3*d
ax.plot([0, Pp[0]], [0, Pp[1]], color=INK, lw=1.2)
for p, n, dx, dy in [((0, 0), 'O', -0.3, -0.5), (P, 'P', 0.05, -0.55), (Q, 'Q', -0.15, 0.3), (Pp, "P'", 0.12, 0.1)]:
    ax.plot([p[0]], [p[1]], 'o', color=INK, ms=4)
    ax.text(p[0]+dx, p[1]+dy, n, fontsize=9)
ax.text(-3.4, 3.3, 'OP × OP′ = r²', fontsize=9)
ax.set_xlim(-3.6, 7.2); ax.set_ylim(-3.4, 3.8); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: derivation Coordinates of the inverse point (centre at the origin)
**Setting up.** The inversion circle is $x^2+y^2=r^2$. Let $P(x,y)$ and its inverse $P'(x',y')$.

**Step 1 — same direction.** $P$ and $P'$ are on the same ray from $O$, so $x'$ and $y'$ are in the same ratio to $x$ and $y$:

$$ \frac{x'}{x}=\frac{y'}{y}=\frac{OP'}{OP} $$

**Step 2 — use the definition.** $OP\times OP'=r^2$, so $OP'=\dfrac{r^2}{OP}$ and

$$ \frac{OP'}{OP}=\frac{r^2}{OP^2}=\frac{r^2}{x^2+y^2} $$

**Result.**

$$ x'=\frac{r^2x}{x^2+y^2}, \qquad y'=\frac{r^2y}{x^2+y^2} $$

**What it means.** Multiply each coordinate by the same factor $\dfrac{r^2}{OP^2}$. If the centre of inversion is $C(h,k)$, apply the same formula to the shifted coordinates: $x'=h+\dfrac{r^2(x-h)}{(x-h)^2+(y-k)^2}$ and $y'=k+\dfrac{r^2(y-k)}{(x-h)^2+(y-k)^2}$.
:::

::: example Inverse of a point inside the circle
**Problem.** Find the inverse of $P(1,2)$ with respect to the circle $x^2+y^2=25$.

**Solution.** $x^2+y^2=1+4=5$ and $r^2=25$, so the factor is $\dfrac{25}{5}=5$.

$$ P'=(5\times1,\ 5\times2)=(5,10) $$

Check: $OP=\sqrt{5}$, $OP'=\sqrt{25+100}=\sqrt{125}=5\sqrt{5}$, and $OP\times OP'=\sqrt{5}\times5\sqrt{5}=25=r^2$. ✓
:::

::: example Inverse of a point outside the circle
**Problem.** Find the inverse of $P(6,8)$ in the circle $x^2+y^2=25$.

**Solution.** $x^2+y^2=36+64=100$. Factor $=\dfrac{25}{100}=\dfrac14$.

$$ P'=\left(\frac{6}{4},\ \frac84\right)=(1.5,\ 2) $$

Check: $OP=10$, $OP'=\sqrt{2.25+4}=2.5$, and $10\times2.5=25$. ✓ ($P$ is outside, $P'$ is inside.)
:::

::: example Point on the circle; centre not at the origin
**Problem.** (a) Find the inverse of $(3,4)$ in $x^2+y^2=25$. (b) Find the inverse of $P(2,1)$ in the circle with centre $C(1,1)$ and radius $2$.

**Solution.** (a) $x^2+y^2=25=r^2$, factor $1$: $P'=(3,4)$. A point on the circle is its own inverse.

(b) Shift coordinates: $P$ is at $(2-1,\,1-1)=(1,0)$ from $C$; $OP^2=1$ and $r^2=4$, so the factor is $4$. The shifted inverse is $(4,0)$, i.e. $P'=(1+4,\ 1+0)=(5,1)$. Check: $CP=1$, $CP'=4$, product $4=r^2$. ✓
:::

::: example Radius from a pair of inverse points
**Problem.** $P$ and $P'$ are inverse points with respect to a circle with centre at the origin, $OP=4$ and $OP'=9$. Find the radius of inversion.

**Solution.** $r^2=OP\times OP'=4\times9=36$, so $r=6$.
:::

## 9.5 Transformation using matrices

### Translation as a $2\times1$ matrix

Write the point $P(x,y)$ as a $2\times1$ column matrix with entries $x$ above $y$ (in running text we write it as the pair $(x,y)$). A translation by $(a,b)$ **adds** the translation matrix: $(x,y)+(a,b)=(x+a,\ y+b)$.

### A $2\times2$ matrix as a transformation

A matrix $M$ with two rows and two columns transforms a point by **pre-multiplying** its column. The row-by-column rule gives

```figure caption="A 2×2 matrix acting on the point (x, y): each row of the matrix is multiplied with the column and added."
fig = mateq([[["a", "b"], ["c", "d"]], [["x"], ["y"]], "=", [["ax + by"], ["cx + dy"]]], colw=1.25)
```

::: derivation Reading a matrix from the images of $(1,0)$ and $(0,1)$
**Step 1.** Multiply $M$ by the column $(1,0)$: the result is $(a,c)$, the **first column** of $M$.

**Step 2.** Multiply $M$ by the column $(0,1)$: the result is $(b,d)$, the **second column** of $M$.

**Result.** The columns of $M$ are the images of $(1,0)$ and $(0,1)$.

**What it means.** To find the matrix of a transformation, find where it sends $(1,0)$ and $(0,1)$ and write those images as columns. Example: rotation by $90^\circ$ sends $(1,0)\to(0,1)$ and $(0,1)\to(-1,0)$, so $M$ has first column $(0,1)$ and second column $(-1,0)$; its rows are $[0,\,-1]$ and $[1,\,0]$.
:::

```figure caption="Standard transformation matrices. Each is read as rows; the first column is the image of (1, 0) and the second column is the image of (0, 1)."
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6, 3.3)); ax.axis('off')
items = [
    ('Reflection in x-axis', [['1', '0'], ['0', '−1']], 'Reflection in y-axis', [['−1', '0'], ['0', '1']]),
    ('Reflection in y = x', [['0', '1'], ['1', '0']], 'Reflection in y = −x', [['0', '−1'], ['−1', '0']]),
    ('Rotation 90° (anticlockwise)', [['0', '−1'], ['1', '0']], 'Rotation 180°', [['−1', '0'], ['0', '−1']]),
    ('Rotation 270° (anticlockwise)', [['0', '1'], ['−1', '0']], 'Enlargement, scale factor k', [['k', '0'], ['0', 'k']]),
]
for i, (n1, m1, n2, m2) in enumerate(items):
    y = 3.6 - i*1.2
    ax.text(0.0, y + 0.55, n1, fontsize=8, ha='left')
    matrix(ax, m1, x=0.5, y=y-0.4, fontsize=10, colw=0.55, rowh=0.38)
    ax.text(3.0, y + 0.55, n2, fontsize=8, ha='left')
    matrix(ax, m2, x=3.5, y=y-0.4, fontsize=10, colw=0.55, rowh=0.38)
ax.set_xlim(-0.2, 5.8); ax.set_ylim(-0.7, 4.4)
fig.tight_layout(pad=0.3)
```

::: example Image of a point under a matrix
**Problem.** Find the image of $P(3,2)$ under the matrix with rows $[2,\,0]$ and $[1,\,1]$.

**Solution.** Row 1: $2\times3+0\times2=6$. Row 2: $1\times3+1\times2=5$. The image is $P'(6,5)$.
:::

::: example Image of a triangle under a matrix
**Problem.** The triangle $PQR$ has $P(1,1)$, $Q(4,1)$, $R(1,3)$. Find its image under the matrix with rows $[0,\,1]$ and $[1,\,0]$ and name the transformation.

**Solution.** The matrix sends $(x,y)\to(0\cdot x+1\cdot y,\ 1\cdot x+0\cdot y)=(y,x)$.

$P'(1,1)$, $Q'(1,4)$, $R'(3,1)$. The transformation is a **reflection in the line $y=x$**.
:::

::: example Finding the matrix from two points and their images
**Problem.** A matrix $M$ maps $A(1,2)$ to $A'(-2,1)$ and $B(3,1)$ to $B'(-1,3)$. Find $M$ and describe the transformation.

**Solution.** Let $M$ have rows $[a,\,b]$ and $[c,\,d]$.

From $A\to A'$: $a+2b=-2$ and $c+2d=1$.
From $B\to B'$: $3a+b=-1$ and $3c+d=3$.

Solving the first pair: $b=-1-3a$, so $a+2(-1-3a)=-2\Rightarrow-5a=0$, $a=0$, $b=-1$.
Solving the second pair: $d=3-3c$, so $c+2(3-3c)=1\Rightarrow-5c=-5$, $c=1$, $d=0$.

$M$ has rows $[0,\,-1]$ and $[1,\,0]$: the transformation $(x,y)\to(-y,x)$ is a **rotation through $90^\circ$ anticlockwise about the origin**.
:::

::: example Combined transformation with matrices
**Problem.** Find the single matrix for a rotation through $90^\circ$ followed by a reflection in the $x$-axis.

**Solution.** Rotation $R$ has rows $[0,\,-1],[1,\,0]$; reflection $X$ has rows $[1,\,0],[0,\,-1]$. Doing $R$ **first** means the combined matrix is $XR$ (the later transformation is written on the left):

```figure caption="The product XR: first row $[1,0]\cdot$ columns of R gives $[0,-1]$; second row $[0,-1]\cdot$ columns of R gives $[-1,0]$."
fig = mateq([[["1", "0"], ["0", "−1"]], "×", [["0", "−1"], ["1", "0"]], "=", [["0", "−1"], ["−1", "0"]]], colw=0.55)
```

The result maps $(x,y)\to(-y,-x)$, a reflection in the line $y=-x$. Check with $P(3,2)$: rotation gives $(-2,3)$, then the $x$-axis reflection gives $(-2,-3)$, and $(-y,-x)=(-2,-3)$. ✓
:::

::: tip The examiner is looking for
For composition: the intermediate point written out, in the stated order. For inversion: the factor $\dfrac{r^2}{x^2+y^2}$ shown, and $OP\times OP'=r^2$ as a check. For matrices: the row-by-column working, and the name of the transformation (reflection, rotation, enlargement) with its axis, angle or centre.
:::

## 9.6 Exercises of the SEE type

### Method for any question

1. Inequalities: boundary line, test point, shade, overlap.
2. Linear programming: variables, objective, constraints, region, corners, table of $z$, answer in words.
3. Composition: apply the transformations one at a time, in order, writing each image.
4. Inversion: $\text{factor}=\dfrac{r^2}{x^2+y^2}$; multiply both coordinates by it.
5. Matrices: image $=M\times$ column; columns of $M$ are the images of $(1,0)$ and $(0,1)$.

## Chapter summary

- Graph of $ax+by+c\geq 0$: boundary line (solid for $\geq ,\leq $; dashed for $>,<$) and the side confirmed by a test point; a system's solution is the overlap.
- Linear programming: maximise or minimise $z=px+qy$ under linear constraints with $x,y\geq 0$; the optimum occurs at a corner point of the feasible region.
- Method: variables, objective function, constraints, feasible region, corners, evaluate $z$, choose.
- Basic images: reflection in $x$-axis $(x,-y)$; in $y$-axis $(-x,y)$; in $y=x$ $(y,x)$; in $y=-x$ $(-y,-x)$; rotation $90^\circ$ $(-y,x)$; $180^\circ$ $(-x,-y)$; enlargement $(kx,ky)$; translation $(x+a,y+b)$.
- $T_2\circ T_1$ means $T_1$ first, then $T_2$; order matters.
- Inversion: $OP\times OP'=r^2$; $x'=\dfrac{r^2x}{x^2+y^2}$, $y'=\dfrac{r^2y}{x^2+y^2}$; a point on the circle is its own inverse.
- A $2\times2$ matrix transforms $(x,y)$ by row-by-column multiplication; its columns are the images of $(1,0)$ and $(0,1)$.
- The matrix of $T_1$ followed by $T_2$ is the product $M_2M_1$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The boundary line of the inequality $2x+3y\leq 12$ is drawn <span class="marks">[1]</span>
   (a) dashed (b) solid (c) not drawn (d) as a curve
2. The image of $(4,-3)$ under reflection in the $x$-axis is <span class="marks">[1]</span>
   (a) $(-4,-3)$ (b) $(4,3)$ (c) $(-4,3)$ (d) $(-3,4)$
3. If $OP=2$ and the radius of inversion is $6$, then $OP'$ is <span class="marks">[1]</span>
   (a) $3$ (b) $12$ (c) $18$ (d) $36$
4. The rotation through $90^\circ$ anticlockwise about the origin maps $(x,y)$ to <span class="marks">[1]</span>
   (a) $(y,-x)$ (b) $(-y,x)$ (c) $(-x,-y)$ (d) $(y,x)$
5. In linear programming the optimum value of the objective function occurs at <span class="marks">[1]</span>
   (a) the origin only (b) a corner point of the feasible region (c) the centre of the region (d) any interior point

::: note Answers to Group A
**1.** (b) — "$\leq $" includes the line.
**2.** (b) — $(x,-y)=(4,3)$.
**3.** (c) — $OP'=\frac{r^2}{OP}=\frac{36}{2}=18$.
**4.** (b) — $(x,y)\to(-y,x)$.
**5.** (b) — the corner point rule.
:::

**Group B — Short answer (2 marks each)**

1. Test whether $(1,2)$ lies in the region $x+y\leq 4$. Is the boundary line solid or dashed for $x+y<4$? <span class="marks">[2]</span>
2. Find the image of $(3,-1)$ under a translation by $(-2,5)$. <span class="marks">[2]</span>
3. Find the inverse of $(3,0)$ with respect to the circle $x^2+y^2=36$. <span class="marks">[2]</span>
4. Find the image of $(2,5)$ under the matrix with rows $[1,\,0]$ and $[0,\,-1]$. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $1+2=3\leq 4$ is true, so $(1,2)$ is in the region. For $x+y<4$ the line is dashed.
**2.** $(3-2,\ -1+5)=(1,4)$.
**3.** $x^2+y^2=9$; factor $\frac{36}{9}=4$; $P'=(12,0)$. Check $3\times12=36$. ✓
**4.** Row 1: $2$; row 2: $-5$. Image $(2,-5)$ (reflection in the $x$-axis).
:::

**Group C — Short answer (3 marks each)**

1. Find the image of $P(4,1)$ under a rotation of $90^\circ$ anticlockwise about the origin followed by a translation by $(2,3)$. <span class="marks">[3]</span>
2. Find the inverse of $P(8,6)$ with respect to the circle $x^2+y^2=100$ and verify $OP\times OP'=r^2$. <span class="marks">[3]</span>
3. Find the corner points of the region $x+y\leq 6$, $x\leq 4$, $x\geq 0$, $y\geq 0$, and the maximum of $z=3x+2y$. <span class="marks">[3]</span>
4. A matrix maps $(1,0)$ to $(3,0)$ and $(0,1)$ to $(0,3)$. Write the matrix and name the transformation. <span class="marks">[3]</span>

::: note Answers to Group C
**1.** Rotation: $(4,1)\to(-1,4)$. Translation: $(-1+2,\ 4+3)=(3,7)$.
**2.** $x^2+y^2=64+36=100$; factor $\frac{100}{100}=1$, so $P'=(8,6)$. The point is on the circle, so it is its own inverse; $OP=OP'=10$ and $10\times10=100$. ✓
**3.** Corners: $(0,0)$, $(4,0)$, $(4,2)$ (where $x=4$ meets $x+y=6$), $(0,6)$. $z$: $0$, $12$, $12+4=16$, $12$. Maximum $z=16$ at $(4,2)$.
**4.** Columns are the images: rows $[3,\,0]$ and $[0,\,3]$. It is an enlargement with centre the origin and scale factor $3$.
:::

**Group D — Long answer (4 marks each)**

1. A tailor makes two kinds of shirts. Type A needs 1 hour of cutting and 3 hours of stitching; type B needs 2 hours of cutting and 1 hour of stitching. At most 10 hours of cutting and 15 hours of stitching are available. Profit is Rs 20 on A and Rs 30 on B. Find the number of each for maximum profit. <span class="marks">[4]</span>
2. The triangle $ABC$ has $A(1,1)$, $B(4,1)$, $C(1,3)$. Find the image under a reflection in the line $y=x$ followed by a reflection in the $x$-axis, and name the single equivalent transformation. <span class="marks">[4]</span>
3. A matrix maps $A(2,1)$ to $A'(-1,2)$ and $B(1,3)$ to $B'(-3,1)$. Find the matrix and name the transformation. <span class="marks">[4]</span>
4. Find the inverse points of $P(2,4)$ and $Q(-3,-6)$ with respect to the circle $x^2+y^2=40$. Show that $O$, $P'$ and $Q'$ are collinear. <span class="marks">[4]</span>

::: note Answers to Group D
**1.** Let $x$ of A and $y$ of B. Maximise $z=20x+30y$ subject to $x+2y\leq 10$, $3x+y\leq 15$, $x,y\geq 0$. Corners: $(0,0)$; $(5,0)$ (from $3x\leq 15$); $(0,5)$ (from $2y\leq 10$); intersection of $x+2y=10$ and $3x+y=15$: $x=10-2y$, $30-6y+y=15$, $y=3$, $x=4$: $(4,3)$. $z$: $0$; $100$; $150$; $80+90=170$. Maximum profit **Rs 170** with 4 shirts of A and 3 of B.
**2.** Reflection in $y=x$: $(x,y)\to(y,x)$: $A'(1,1)$, $B'(1,4)$, $C'(3,1)$. Reflection in the $x$-axis: $(x,y)\to(x,-y)$: $A''(1,-1)$, $B''(1,-4)$, $C''(3,-1)$. Combined: $(x,y)\to(y,x)\to(y,-x)$, which is the rotation through $270^\circ$ anticlockwise ($90^\circ$ clockwise) about the origin.
**3.** Rows $[a,b]$, $[c,d]$. $2a+b=-1$ and $a+3b=-3$: $b=-1-2a$, $a+3(-1-2a)=-3\Rightarrow-5a=0$, $a=0$, $b=-1$. $2c+d=2$ and $c+3d=1$: $d=2-2c$, $c+6-6c=1\Rightarrow c=1$, $d=0$. Matrix rows $[0,-1]$, $[1,0]$: rotation through $90^\circ$ anticlockwise about the origin.
**4.** $P$: $x^2+y^2=20$, factor $\frac{40}{20}=2$, $P'=(4,8)$. $Q$: $9+36=45$, factor $\frac{40}{45}=\frac89$, $Q'=\left(-\frac{8}{3},-\frac{16}{3}\right)$. Both $P'$ and $Q'$ have $y=2x$ ($8=2\times4$ and $-\frac{16}{3}=2\times-\frac83$), so they lie on the line $y=2x$ through $O$: collinear with $O$.
:::



## Retrieval practice and investigation

::: key Work before reading the key
Answer these short retrieval questions without consulting the chapter. Explain the reason, not only the result. These are revision checks, not a prediction of the examination paper.
:::

**1.** Maximise Z = 3x + 2y under those constraints.

**2.** Reflect (3, −2) in the y-axis.

**3.** Can an infeasible corner provide the optimum?

::: note Reasoned key
**1.** Corners are (0,0), (4,0), (4,2), (0,6). Z values are 0, 12, 16, 12, so the maximum is 16 at (4,2).

**2.** (−3, −2). Reflection in the y-axis changes x and preserves y.

**3.** No. It must satisfy every constraint, even if its objective value is large.

:::

::: tip Investigation — Test every feasible corner
Draw x ≥ 0, y ≥ 0, x + y ≤ 6, x ≤ 4. List all corner coordinates and evaluate Z = 3x + 2y at each. Explain why checking only the axis intercepts misses a possible optimum.

Submit a one-page record: your method, working or evidence, conclusion, and one limitation. Exchange it with a classmate and check the reasoning against the chapter.
:::
