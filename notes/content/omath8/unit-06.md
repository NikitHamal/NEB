---
subject: Optional Mathematics
grade: 8
unit: 6
title: Coordinate Geometry
hours: 0
---

In grade 7 you learned to locate a point by its coordinates. Coordinate geometry goes one step further: it uses the coordinates to **measure**. From the coordinates of two points we can find the distance between them without a ruler, find the point that cuts the line between them in any ratio, measure how steep the line is, write the line as an equation, and find the area of a triangle or a field from the coordinates of its corners. Surveyors marking land plots, engineers laying a road from Butwal to Narayangadh, and the map app on a phone all do exactly these calculations. This chapter develops four formulas, each from a picture, and shows how to use them.

::: key What your examination asks from this chapter
Expect: (i) the **distance** between two points, and using it to show that a triangle is isosceles, equilateral or right-angled, that three points are **collinear**, or that four points form a square, rhombus or rectangle; (ii) finding an unknown coordinate from a given distance; (iii) the point dividing a segment in a given **ratio**, the **mid-point**, the points of trisection, or a missing end point; (iv) the **slope** of a line through two points, and the equation of a line in the form $y=mx+c$; (v) lines parallel to the axes; (vi) the **area** of a triangle or quadrilateral from its vertices. Draw a quick sketch: it shows whether your answer is reasonable.
:::

## 6.1 Distance formula and its applications

### Deriving the formula

Let $P(x_1,y_1)$ and $Q(x_2,y_2)$ be two points. Through $P$ draw a horizontal line and through $Q$ a vertical line; they meet at $R(x_2,y_1)$. Triangle $PRQ$ has a right angle at $R$.

```figure caption="The distance formula comes from Pythagoras' theorem. The horizontal side $PR$ has length $x_2-x_1$ and the vertical side $RQ$ has length $y_2-y_1$, so $PQ^2=(x_2-x_1)^2+(y_2-y_1)^2$."
fig, ax = plt.subplots(figsize=(4.6, 3.0))
P, Q, R = (1.0, 1.0), (5.0, 4.0), (5.0, 1.0)
ax.plot([P[0], R[0], Q[0], P[0]], [P[1], R[1], Q[1], P[1]], color=INK, lw=1.4)
ax.plot([P[0], Q[0]], [P[1], Q[1]], color=ACCENT, lw=2.2)
ax.add_patch(Rectangle((R[0] - 0.25, R[1]), 0.25, 0.25, fill=False, ec=INK, lw=0.9))
for (x, y), lab, dx, dy, ha in [(P, 'P(x₁, y₁)', -0.1, -0.35, 'right'), (Q, 'Q(x₂, y₂)', 0.12, 0.1, 'left'), (R, 'R(x₂, y₁)', 0.12, -0.35, 'left')]:
    ax.plot(x, y, 'o', color=INK, ms=4.5)
    ax.text(x + dx, y + dy, lab, fontsize=9, ha=ha)
ax.text(3.0, 0.6, 'x₂ − x₁', ha='center', fontsize=9, color=SERIES[1])
ax.text(5.25, 2.5, 'y₂ − y₁', ha='left', va='center', fontsize=9, color=SERIES[1])
ax.text(2.75, 2.75, 'd = PQ', ha='right', fontsize=9.5, color=ACCENT)
ax.axhline(0, color=MUTED, lw=0.8); ax.axvline(0, color=MUTED, lw=0.8)
ax.text(6.9, -0.35, 'x', fontsize=9, color=MUTED); ax.text(-0.35, 4.75, 'y', fontsize=9, color=MUTED)
ax.set_xlim(-0.5, 7.2); ax.set_ylim(-0.6, 5.0); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: derivation The distance between two points
We start from the right-angled triangle $PRQ$ and are heading for a formula for $PQ$.

**Step 1 — the two shorter sides.** $PR$ is horizontal, so its length is the difference of the $x$-coordinates: $PR=x_2-x_1$. $RQ$ is vertical, so $RQ=y_2-y_1$.

**Step 2 — Pythagoras' theorem in triangle $PRQ$.**
$$ PQ^2=PR^2+RQ^2=(x_2-x_1)^2+(y_2-y_1)^2 $$

**Step 3 — take the square root.**
$$ d=PQ=\sqrt{(x_2-x_1)^2+(y_2-y_1)^2} $$

**What it means.** Subtract the $x$-coordinates, subtract the $y$-coordinates, square both, add, and take the square root. Because the differences are squared, it does not matter which point is called $P$: $(x_1-x_2)^2=(x_2-x_1)^2$.
:::

::: key Distance formula
$$ PQ=\sqrt{(x_2-x_1)^2+(y_2-y_1)^2} $$
The distance of $P(x,y)$ from the origin $O$ is
$$ OP=\sqrt{x^2+y^2} $$
If the two points have the same $y$-coordinate the distance is $|x_2-x_1|$; if they have the same $x$-coordinate it is $|y_2-y_1|$.
:::

::: example Distance between two points
**Problem.** Find the distance between (i) $A(2,3)$ and $B(8,11)$ (ii) $P(-3,4)$ and $Q(2,-8)$.

**Solution.** (i) $AB=\sqrt{(8-2)^2+(11-3)^2}=\sqrt{36+64}=\sqrt{100}=10$ units.

(ii) $PQ=\sqrt{(2-(-3))^2+(-8-4)^2}=\sqrt{5^2+(-12)^2}=\sqrt{25+144}=\sqrt{169}=13$ units.

Use brackets for negative coordinates: $2-(-3)=5$, not $-1$.
:::

### Applications

The distance formula turns questions about shapes into arithmetic.

| To show that … | find … and check that … |
|---|---|
| a triangle is **isosceles** | the three sides; two are equal |
| a triangle is **equilateral** | the three sides; all are equal |
| a triangle is **right-angled** | the three sides; the square of the longest equals the sum of the squares of the other two |
| three points $A$, $B$, $C$ are **collinear** | $AB$, $BC$, $AC$; the two shorter ones add up to the longest |
| $ABCD$ is a **rhombus** | all four sides are equal |
| $ABCD$ is a **square** | all four sides are equal **and** the diagonals are equal |
| $ABCD$ is a **rectangle** | opposite sides are equal **and** the diagonals are equal |
| $ABCD$ is a **parallelogram** | both pairs of opposite sides are equal |

::: example An isosceles triangle
**Problem.** Show that $A(1,2)$, $B(5,5)$ and $C(9,2)$ are the vertices of an isosceles triangle, and find its perimeter.

**Solution.**
$$ AB=\sqrt{4^2+3^2}=5,\qquad BC=\sqrt{4^2+(-3)^2}=5,\qquad AC=\sqrt{8^2+0^2}=8 $$
Since $AB=BC$, the triangle is **isosceles**. Its perimeter is $5+5+8=18$ units.
:::

::: example A right-angled triangle
**Problem.** Show that $A(2,1)$, $B(5,3)$ and $C(1,9)$ form a right-angled triangle. At which vertex is the right angle?

**Solution.** Work with the squares of the sides, to avoid square roots:
$$ AB^2=3^2+2^2=13,\qquad BC^2=(-4)^2+6^2=52,\qquad AC^2=(-1)^2+8^2=65 $$
$AB^2+BC^2=13+52=65=AC^2$. By the converse of Pythagoras' theorem the triangle is right-angled, and the right angle is at $B$, the vertex opposite the longest side $AC$.
:::

::: example Collinear points
**Problem.** Show that $A(1,2)$, $B(3,6)$ and $C(4,8)$ lie on one straight line.

**Solution.**
$$ AB=\sqrt{4+16}=\sqrt{20}=2\sqrt{5},\qquad BC=\sqrt{1+4}=\sqrt{5} $$
$$ AC=\sqrt{9+36}=\sqrt{45}=3\sqrt{5} $$
$AB+BC=2\sqrt{5}+\sqrt{5}=3\sqrt{5}=AC$. The path from $A$ to $C$ through $B$ is no longer than the direct path, so $B$ lies on $AC$: the points are **collinear**.
:::

::: example An unknown coordinate, and an equidistant point
**Problem.** (i) Find $k$ if the distance between $(k,3)$ and $(2,-1)$ is 5 units. (ii) Find the point on the $x$-axis that is equidistant from $A(1,4)$ and $B(5,2)$.

**Solution.** (i) $(k-2)^2+(3+1)^2=5^2$, so $(k-2)^2=25-16=9$ and $k-2=\pm3$. Hence $k=5$ or $k=-1$. Both points, $(5,3)$ and $(-1,3)$, are 5 units from $(2,-1)$.

(ii) A point on the $x$-axis is $P(x,0)$. Equal distances means $PA^2=PB^2$:
$$ (x-1)^2+16=(x-5)^2+4\ \Rightarrow\ x^2-2x+17=x^2-10x+29\ \Rightarrow\ 8x=12 $$
So $x=1.5$ and the point is $P(1.5,0)$. Check: $PA^2=0.25+16=16.25$ and $PB^2=12.25+4=16.25$ ✓.
:::

::: example A rhombus that is not a square
**Problem.** Show that $A(0,0)$, $B(4,1)$, $C(5,5)$ and $D(1,4)$ are the vertices of a rhombus. Is it a square?

**Solution.** $AB^2=16+1=17$, $BC^2=1+16=17$, $CD^2=16+1=17$, $DA^2=1+16=17$. All four sides are $\sqrt{17}$, so $ABCD$ is a **rhombus**.

Diagonals: $AC^2=25+25=50$ and $BD^2=9+9=18$. The diagonals are not equal, so it is **not a square**.
:::

::: caution Square roots do not add like that
$\sqrt{36+64}$ is $\sqrt{100}=10$, not $\sqrt{36}+\sqrt{64}=14$. Add the squares **first**, then take the square root. When you compare sides, compare their squares, which avoids roots altogether.
:::

## 6.2 Section formula: dividing a line segment in a given ratio; mid-point

A point $P$ on the segment $AB$ **divides it internally in the ratio $m_1:m_2$** when $AP:PB=m_1:m_2$. For example, if $AB$ is 10 cm and $AP:PB=2:3$, then $AP=4$ cm and $PB=6$ cm.

```figure caption="$P(x,y)$ divides $AB$ in the ratio $m_1:m_2$. The two shaded right triangles are similar, so their horizontal sides are in the same ratio: $(x-x_1):(x_2-x)=m_1:m_2$, and likewise the vertical sides."
fig, ax = plt.subplots(figsize=(4.8, 3.0))
A, B = np.array([1.0, 1.0]), np.array([7.0, 5.0])
P = A + 0.4*(B - A)
L, M = (P[0], A[1]), (B[0], P[1])
ax.fill([A[0], L[0], P[0]], [A[1], L[1], P[1]], color='#cfe3f6')
ax.fill([P[0], M[0], B[0]], [P[1], M[1], B[1]], color='#fbe3e2')
ax.plot([A[0], B[0]], [A[1], B[1]], color=INK, lw=1.6)
ax.plot([A[0], L[0], P[0]], [A[1], L[1], P[1]], color=ACCENT, lw=1.1)
ax.plot([P[0], M[0], B[0]], [P[1], M[1], B[1]], color=SERIES[1], lw=1.1)
for pt, lab, dx, dy, ha in [(A, 'A(x₁, y₁)', -0.1, 0.15, 'right'), (B, 'B(x₂, y₂)', 0.12, 0.05, 'left'), (P, 'P(x, y)', -0.15, 0.2, 'right')]:
    ax.plot(pt[0], pt[1], 'o', color=INK, ms=4.5)
    ax.text(pt[0] + dx, pt[1] + dy, lab, fontsize=9, ha=ha)
ax.text((A[0] + L[0])/2, A[1] - 0.38, 'x − x₁', ha='center', fontsize=8.5, color=ACCENT)
ax.text(L[0] + 0.12, (A[1] + P[1])/2, 'y − y₁', va='center', fontsize=8.5, color=ACCENT)
ax.text((P[0] + M[0])/2, P[1] - 0.38, 'x₂ − x', ha='center', fontsize=8.5, color=SERIES[1])
ax.text(M[0] + 0.12, (P[1] + B[1])/2, 'y₂ − y', va='center', fontsize=8.5, color=SERIES[1])
ax.text((A[0] + P[0])/2 - 0.3, (A[1] + P[1])/2 + 0.3, 'm₁', fontsize=9.5, color=INK)
ax.text((P[0] + B[0])/2 - 0.3, (P[1] + B[1])/2 + 0.3, 'm₂', fontsize=9.5, color=INK)
ax.set_xlim(-1.4, 8.8); ax.set_ylim(0.2, 5.7); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: derivation The section formula
We start from $P(x,y)$ on $AB$ with $AP:PB=m_1:m_2$, and are heading for $x$ and $y$.

**Step 1 — similar triangles.** The shaded triangles in the figure have parallel sides, so they are similar. Corresponding sides are in the ratio $AP:PB=m_1:m_2$.

**Step 2 — compare horizontal sides.**
$$ \frac{x-x_1}{x_2-x}=\frac{m_1}{m_2} $$

**Step 3 — cross-multiply and solve for $x$.**
$$ m_2(x-x_1)=m_1(x_2-x)\ \Rightarrow\ m_2x-m_2x_1=m_1x_2-m_1x $$
$$ \Rightarrow\ (m_1+m_2)x=m_1x_2+m_2x_1 $$

**Step 4 — the same with vertical sides** gives $(m_1+m_2)y=m_1y_2+m_2y_1$.

**Result.**
$$ P(x,y)=\left(\frac{m_1x_2+m_2x_1}{m_1+m_2},\ \frac{m_1y_2+m_2y_1}{m_1+m_2}\right) $$
:::

::: key Section formula and mid-point
If $P$ divides the join of $A(x_1,y_1)$ and $B(x_2,y_2)$ internally in the ratio $m_1:m_2$:
$$ P=\left(\frac{m_1x_2+m_2x_1}{m_1+m_2},\ \frac{m_1y_2+m_2y_1}{m_1+m_2}\right) $$
For the **mid-point** ($m_1=m_2$): $M=\left(\frac{x_1+x_2}{2},\ \frac{y_1+y_2}{2}\right)$.

Memory aid: $m_1$ goes with the **far** end $B$, and $m_2$ with the **near** end $A$: "cross the ratio over".
:::

::: example A point in a given ratio
**Problem.** Find the point that divides the join of (i) $A(2,3)$ and $B(7,8)$ in the ratio $2:3$; (ii) $A(-1,4)$ and $B(5,-2)$ in the ratio $1:2$.

**Solution.** (i) $m_1=2$, $m_2=3$:
$$ x=\frac{2(7)+3(2)}{5}=\frac{20}{5}=4,\qquad y=\frac{2(8)+3(3)}{5}=\frac{25}{5}=5 $$
The point is $(4,5)$. Check with distances: $AP=\sqrt{4+4}=2\sqrt{2}$ and $PB=\sqrt{9+9}=3\sqrt{2}$, ratio $2:3$ ✓.

(ii) $x=\frac{1(5)+2(-1)}{3}=\frac{3}{3}=1$ and $y=\frac{1(-2)+2(4)}{3}=\frac{6}{3}=2$. The point is $(1,2)$.
:::

::: example Mid-point and a missing end point
**Problem.** (i) Find the mid-point of $(3,-2)$ and $(-5,6)$. (ii) $M(2,3)$ is the mid-point of $AB$, where $A$ is $(-1,5)$. Find $B$.

**Solution.** (i) $\left(\frac{3-5}{2},\ \frac{-2+6}{2}\right)=(-1,2)$.

(ii) Let $B=(x,y)$. Then $\frac{-1+x}{2}=2$, so $x=5$; and $\frac{5+y}{2}=3$, so $y=1$. So $B$ is $(5,1)$.
:::

::: example Points of trisection
**Problem.** Find the two points that divide the join of $A(1,2)$ and $B(7,11)$ into three equal parts.

**Solution.** The first point $P$ is one-third of the way from $A$, so $AP:PB=1:2$:
$$ P=\left(\frac{1(7)+2(1)}{3},\ \frac{1(11)+2(2)}{3}\right)=(3,5) $$
The second point $Q$ has $AQ:QB=2:1$:
$$ Q=\left(\frac{2(7)+1(1)}{3},\ \frac{2(11)+1(2)}{3}\right)=(5,8) $$
The $x$-coordinates go $1, 3, 5, 7$ in equal steps, as they should.
:::

::: example Finding the ratio
**Problem.** In what ratio does the point $(3,4)$ divide the join of $A(1,2)$ and $B(6,7)$?

**Solution.** Let the ratio be $k:1$. From the $x$-coordinates:
$$ \frac{6k+1}{k+1}=3\ \Rightarrow\ 6k+1=3k+3\ \Rightarrow\ k=\frac{2}{3} $$
So the ratio is $\frac{2}{3}:1=2:3$. Check with $y$: $\frac{7\cdot\frac{2}{3}+2}{\frac{2}{3}+1}=\frac{\frac{20}{3}}{\frac{5}{3}}=4$ ✓.
:::

### Two useful applications

**Centroid of a triangle.** The centroid $G$ is the point where the medians meet; it divides each median in the ratio $2:1$ from the vertex. For $A(1,2)$, $B(5,4)$, $C(3,9)$: the mid-point of $BC$ is $D(4,\ 6.5)$, and dividing $AD$ in the ratio $2:1$ gives $G=\left(\frac{2(4)+1(1)}{3},\ \frac{2(6.5)+1(2)}{3}\right)=(3,5)$. The same answer comes from the short rule $G=\left(\frac{x_1+x_2+x_3}{3},\ \frac{y_1+y_2+y_3}{3}\right)=\left(\frac{9}{3},\frac{15}{3}\right)=(3,5)$.

**Fourth vertex of a parallelogram.** The diagonals of a parallelogram bisect each other, so they have the same mid-point. If $A(1,1)$, $B(5,2)$ and $C(7,5)$ are three vertices of the parallelogram $ABCD$, then the mid-point of $AC$, $(4,3)$, is also the mid-point of $BD$. So $D=(2\times4-5,\ 2\times3-2)=(3,4)$.

## 6.3 Slope of a line; lines parallel to the axes; slope-intercept form y = mx + c

### Slope

The road up to Nagarkot climbs; the road along the Terai plain is flat. The **slope** (or gradient) of a line measures how steep it is: how much it rises for each unit it runs to the right.

::: definition Slope of a line
The **slope** of the line through $A(x_1,y_1)$ and $B(x_2,y_2)$, with $x_1\neq x_2$, is
$$ m=\frac{\text{rise}}{\text{run}}=\frac{y_2-y_1}{x_2-x_1} $$
If the line makes an angle $\theta$ with the positive direction of the $x$-axis (its **inclination**), then $m=\tan\theta$.
:::

```figure caption="The four kinds of slope. A line that rises to the right has a positive slope, one that falls has a negative slope, a horizontal line has slope 0, and a vertical line has no defined slope (its run is 0)."
fig, axs = plt.subplots(1, 4, figsize=(5.2, 2.2))
specs = [('m > 0', (0.5, 0.6), (3.5, 3.2)), ('m < 0', (0.5, 3.2), (3.5, 0.6)), ('m = 0', (0.4, 2.0), (3.6, 2.0)), ('m undefined', (2.0, 0.4), (2.0, 3.6))]
for ax, (title, p, q) in zip(axs, specs):
    ax.plot([p[0], q[0]], [p[1], q[1]], color=ACCENT, lw=2.0)
    if title in ('m > 0', 'm < 0'):
        x0, y0 = 1.5, p[1] + (q[1] - p[1])*(1.0/3.0)
        y1 = p[1] + (q[1] - p[1])*(2.0/3.0)
        ax.plot([x0, x0 + 1.0, x0 + 1.0], [y0, y0, y1], color=SERIES[1], lw=1.0, ls='--')
    ax.axhline(0, color=MUTED, lw=0.7); ax.axvline(0, color=MUTED, lw=0.7)
    ax.set_xlim(-0.3, 4); ax.set_ylim(-0.3, 4); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title(title, fontsize=8.5, pad=2)
fig.tight_layout(pad=0.3)
```

::: example Slopes from two points
**Problem.** Find the slope of the line through (i) $(2,3)$ and $(6,11)$ (ii) $(-1,4)$ and $(3,-2)$ (iii) $(1,5)$ and $(7,5)$ (iv) $(4,1)$ and $(4,9)$.

**Solution.** (i) $m=\frac{11-3}{6-2}=\frac{8}{4}=2$; the line rises 2 units for each unit to the right.

(ii) $m=\frac{-2-4}{3-(-1)}=\frac{-6}{4}=-\frac{3}{2}$; the line falls.

(iii) $m=\frac{5-5}{7-1}=\frac{0}{6}=0$; the line is horizontal.

(iv) $m=\frac{9-1}{4-4}=\frac{8}{0}$, which is not defined; the line is vertical.
:::

When the inclination is one of the standard angles of the next chapter, the slope is a known number: $\tan0^\circ=0$, $\tan30^\circ=\frac{1}{\sqrt{3}}$, $\tan45^\circ=1$ and $\tan60^\circ=\sqrt{3}$. So a line inclined at $45^\circ$ has slope 1, and a line of slope $\sqrt{3}$ is inclined at $60^\circ$.

### Using slopes: parallel lines and collinear points

Two non-vertical lines are **parallel** exactly when they have the **same slope**: they rise at the same rate, so they never meet. And three points $A$, $B$, $C$ are collinear when the slope of $AB$ equals the slope of $BC$, because then the two segments have the same direction and share the point $B$.

::: example Collinearity and parallel lines by slopes
**Problem.** (i) Use slopes to show that $A(1,2)$, $B(3,6)$ and $C(4,8)$ are collinear. (ii) Show that the line through $P(1,1)$ and $Q(4,7)$ is parallel to the line through $R(0,3)$ and $S(2,7)$.

**Solution.** (i) Slope of $AB=\frac{6-2}{3-1}=2$ and slope of $BC=\frac{8-6}{4-3}=2$. The slopes are equal and $B$ is common, so the points are collinear (agreeing with the distance method in 6.1).

(ii) Slope of $PQ=\frac{7-1}{4-1}=2$ and slope of $RS=\frac{7-3}{2-0}=2$. Equal slopes, so $PQ\parallel RS$. (They are not the same line: $R(0,3)$ is not on $PQ$, which crosses the $y$-axis at $-1$.)
:::

### Lines parallel to the axes

Every point on a vertical line has the **same $x$-coordinate**; every point on a horizontal line has the **same $y$-coordinate**. That fact is the whole equation of the line.

| Line | Equation | Slope |
|---|---|---|
| parallel to the $y$-axis, through $(a,b)$ | $x=a$ | not defined |
| parallel to the $x$-axis, through $(a,b)$ | $y=b$ | 0 |
| the $x$-axis itself | $y=0$ | 0 |
| the $y$-axis itself | $x=0$ | not defined |

So the line through $(3,-2)$ parallel to the $x$-axis is $y=-2$, and the line through the same point parallel to the $y$-axis is $x=3$.

### The slope-intercept form y = mx + c

A non-vertical line crosses the $y$-axis at some point $(0,c)$. The number $c$ is the **$y$-intercept**.

::: derivation Equation of a line with slope m and y-intercept c
We start from a line of slope $m$ through $(0,c)$ and are heading for its equation.

**Step 1 — take any point on the line.** Let $(x,y)$ be any point of the line other than $(0,c)$.

**Step 2 — the slope from $(0,c)$ to $(x,y)$ is $m$.**
$$ \frac{y-c}{x-0}=m $$

**Step 3 — multiply by $x$ and rearrange.** $y-c=mx$, so
$$ y=mx+c $$

**What it means.** In $y=mx+c$, the coefficient of $x$ is the **slope** and the constant is the **$y$-intercept**. Every point $(x,y)$ on the line satisfies the equation, and every point satisfying it is on the line.
:::

```figure caption="Left: the line $y=2x+1$ crosses the $y$-axis at $c=1$ and rises 2 units for every 1 unit to the right ($m=2$). Right: the lines $x=3$ and $y=-2$ are parallel to the $y$-axis and the $x$-axis."
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.0, 2.8))
x = np.linspace(-1.5, 2.6, 50)
ax1.plot(x, 2*x + 1, color=ACCENT, lw=1.8)
ax1.plot(0, 1, 'o', color=SERIES[1], ms=5)
ax1.text(-0.2, 1.25, 'c = 1', ha='right', fontsize=8.5, color=SERIES[1])
ax1.plot([1, 2, 2], [3, 3, 5], color=SERIES[2], lw=1.2, ls='--')
ax1.text(1.5, 2.55, 'run 1', ha='center', fontsize=8, color=SERIES[2])
ax1.text(2.1, 4.0, 'rise 2', ha='left', fontsize=8, color=SERIES[2])
ax1.text(0.7, 5.3, 'y = 2x + 1', fontsize=9, color=ACCENT)
ax1.set_xlim(-2, 3.4); ax1.set_ylim(-2.5, 6.2)
ax2.axvline(3, color=ACCENT, lw=1.8); ax2.axhline(-2, color=SERIES[1], lw=1.8)
ax2.text(3.15, 2.4, 'x = 3', fontsize=9, color=ACCENT)
ax2.text(-3.6, -1.6, 'y = −2', fontsize=9, color=SERIES[1])
ax2.text(3.6, 0.25, 'y = 0', fontsize=8, color=MUTED)
ax2.text(0.15, 3.3, 'x = 0', fontsize=8, color=MUTED)
ax2.plot(3, -2, 'o', color=INK, ms=4.5); ax2.text(3.15, -2.6, '(3, −2)', fontsize=8.5)
ax2.set_xlim(-4, 4.8); ax2.set_ylim(-4, 4)
ax2.set_xticks([-2, 2]); ax2.set_yticks([-2, 2])
for ax in (ax1, ax2):
    ax.axhline(0, color=MUTED, lw=0.8); ax.axvline(0, color=MUTED, lw=0.8)
    ax.grid(True, color=GRID, lw=0.5); ax.set_axisbelow(True)
    ax.tick_params(labelsize=7.5, length=0)
    for s in ax.spines.values(): s.set_visible(False)
fig.tight_layout(pad=0.4)
```

::: example Writing and reading y = mx + c
**Problem.** (i) Write the equation of the line with slope 3 and $y$-intercept $-2$. (ii) Find the slope and $y$-intercept of $2x+3y=12$.

**Solution.** (i) $y=3x-2$.

(ii) Make $y$ the subject: $3y=-2x+12$, so $y=-\frac{2}{3}x+4$. Comparing with $y=mx+c$: slope $m=-\frac{2}{3}$, $y$-intercept $c=4$.
:::

::: example A line through given points
**Problem.** (i) Find the equation of the line of slope 2 through $(3,5)$. (ii) Find the equation of the line through $(1,2)$ and $(3,8)$. (iii) Does $(4,7)$ lie on the line in (i)?

**Solution.** (i) $y=2x+c$ passes through $(3,5)$, so $5=2(3)+c$ and $c=-1$: the line is $y=2x-1$.

(ii) The slope is $m=\frac{8-2}{3-1}=3$. Then $y=3x+c$ through $(1,2)$ gives $2=3+c$, so $c=-1$ and the line is $y=3x-1$. Check with $(3,8)$: $3(3)-1=8$ ✓.

(iii) Put $x=4$ in $y=2x-1$: $y=7$. So $(4,7)$ **does** lie on the line.
:::

::: caution Make y the subject before reading m and c
In $2x+3y=12$ the slope is **not** 2 and the intercept is **not** 12. The numbers can be read off only when the equation is written as $y=mx+c$. Divide every term by the coefficient of $y$, including the constant.
:::

## 6.4 Area of a triangle and a quadrilateral from the coordinates of the vertices

### Deriving the area of a triangle

Let the vertices be $A(x_1,y_1)$, $B(x_2,y_2)$ and $C(x_3,y_3)$, and drop perpendiculars $AL$, $BM$, $CN$ to the $x$-axis. The triangle is what is left of two trapeziums when a third is taken away.

```figure caption="Area of triangle $ABC$ = area of trapezium $ALMB$ + area of trapezium $BMNC$ − area of trapezium $ALNC$. Each trapezium has two vertical parallel sides, the $y$-coordinates, and a width along the $x$-axis."
fig, ax = plt.subplots(figsize=(4.8, 3.2))
A, B, C = (1.0, 2.0), (4.0, 6.0), (7.0, 3.0)
ax.fill([A[0], B[0], B[0], A[0]], [A[1], B[1], 0, 0], color='#cfe3f6')
ax.fill([B[0], C[0], C[0], B[0]], [B[1], C[1], 0, 0], color='#d5efdf')
ax.plot([A[0], A[0]], [0, A[1]], color=MUTED, lw=1.0, ls='--')
ax.plot([B[0], B[0]], [0, B[1]], color=MUTED, lw=1.0, ls='--')
ax.plot([C[0], C[0]], [0, C[1]], color=MUTED, lw=1.0, ls='--')
ax.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], color=INK, lw=1.6)
ax.plot([-0.4, 8.2], [0, 0], color=INK, lw=1.0)
for pt, lab, dx, dy, ha in [(A, 'A(x₁, y₁)', -0.12, 0.15, 'right'), (B, 'B(x₂, y₂)', 0.0, 0.25, 'center'), (C, 'C(x₃, y₃)', 0.12, 0.15, 'left')]:
    ax.plot(pt[0], pt[1], 'o', color=INK, ms=4.5)
    ax.text(pt[0] + dx, pt[1] + dy, lab, fontsize=9, ha=ha)
for xv, lab in [(A[0], 'L'), (B[0], 'M'), (C[0], 'N')]:
    ax.text(xv, -0.45, lab, ha='center', fontsize=9)
ax.text(2.5, 1.2, 'ALMB', ha='center', fontsize=8.5, color=ACCENT)
ax.text(5.5, 1.2, 'BMNC', ha='center', fontsize=8.5, color=SERIES[2])
ax.set_xlim(-0.8, 9.2); ax.set_ylim(-0.8, 7.0); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: derivation Area of a triangle from its vertices
We start from the trapeziums in the figure and are heading for a formula in the coordinates.

**Step 1 — area of a trapezium** $=\frac{1}{2}\times$(sum of the parallel sides)$\times$(distance between them):
$$ ALMB=\tfrac{1}{2}(y_1+y_2)(x_2-x_1),\qquad BMNC=\tfrac{1}{2}(y_2+y_3)(x_3-x_2) $$
$$ ALNC=\tfrac{1}{2}(y_1+y_3)(x_3-x_1) $$

**Step 2 — combine.** $\triangle ABC=ALMB+BMNC-ALNC$:
$$ \triangle=\tfrac{1}{2}\left[(y_1+y_2)(x_2-x_1)+(y_2+y_3)(x_3-x_2)-(y_1+y_3)(x_3-x_1)\right] $$

**Step 3 — expand and cancel.** The terms $x_1y_1$, $x_2y_2$ and $x_3y_3$ cancel, leaving
$$ \triangle=\tfrac{1}{2}\left[x_2y_1-x_1y_2+x_3y_2-x_2y_3+x_1y_3-x_3y_1\right] $$

**Step 4 — group by $x_1$, $x_2$, $x_3$.** This is $-\frac{1}{2}\left[x_1(y_2-y_3)+x_2(y_3-y_1)+x_3(y_1-y_2)\right]$. The sign depends only on the order in which the vertices were named, so we take the absolute value.

**Result.**
$$ \text{Area}=\frac{1}{2}\left|x_1(y_2-y_3)+x_2(y_3-y_1)+x_3(y_1-y_2)\right| $$
:::

### The cross-multiplication (arrow) method

The same formula can be laid out in a pattern that is easy to remember and extends to any polygon. Write the coordinates in two rows, **repeat the first vertex at the end**, multiply along the arrows and subtract.

```figure caption="The arrow method for $A(1,2)$, $B(5,3)$, $C(3,7)$. Blue products (down-right) are added: $1\times3+5\times7+3\times2=44$. Red products (up-right) are subtracted: $5\times2+3\times3+1\times7=26$. Area $=\frac{1}{2}|44-26|=9$ square units."
fig, ax = plt.subplots(figsize=(4.6, 2.3))
xs, ys = [1, 5, 3, 1], [2, 3, 7, 2]
for i in range(4):
    ax.text(i*1.4, 1.0, str(xs[i]), ha='center', va='center', fontsize=12)
    ax.text(i*1.4, 0.0, str(ys[i]), ha='center', va='center', fontsize=12)
for i in range(3):
    ax.annotate('', xy=((i + 1)*1.4 - 0.18, 0.15), xytext=(i*1.4 + 0.18, 0.85), arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.3))
    ax.annotate('', xy=((i + 1)*1.4 - 0.18, 0.85), xytext=(i*1.4 + 0.18, 0.15), arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.3))
ax.text(-0.9, 1.0, 'x', ha='center', va='center', fontsize=11, color=MUTED)
ax.text(-0.9, 0.0, 'y', ha='center', va='center', fontsize=11, color=MUTED)
ax.text(5.0, 0.85, '+ (3 + 35 + 6) = 44', fontsize=9, color=ACCENT)
ax.text(5.0, 0.15, '− (10 + 9 + 7) = 26', fontsize=9, color=SERIES[1])
ax.set_xlim(-1.3, 8.6); ax.set_ylim(-0.5, 1.5); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: key Area from coordinates
Triangle: $\text{Area}=\frac{1}{2}\left|x_1(y_2-y_3)+x_2(y_3-y_1)+x_3(y_1-y_2)\right|$, or by the arrow method
$$ \text{Area}=\frac{1}{2}\left|(x_1y_2-x_2y_1)+(x_2y_3-x_3y_2)+(x_3y_1-x_1y_3)\right| $$
Quadrilateral $ABCD$: take the vertices **in order round the figure** and use four cross terms, or split it into two triangles by a diagonal. Three points are **collinear** exactly when the "triangle" they form has area 0.
:::

::: example Area of a triangle, checked by another method
**Problem.** Find the area of the triangle with vertices $A(1,2)$, $B(5,3)$ and $C(3,7)$.

**Solution.**
$$ \text{Area}=\frac{1}{2}\left|1(3-7)+5(7-2)+3(2-3)\right|=\frac{1}{2}\left|-4+25-3\right|=\frac{1}{2}\times18=9 \text{ square units} $$
**Check by the box method.** The rectangle enclosing the triangle runs from $x=1$ to 5 and from $y=2$ to 7, area $4\times5=20$. The three right triangles outside $ABC$ have areas $\frac{1}{2}(4)(1)=2$, $\frac{1}{2}(2)(4)=4$ and $\frac{1}{2}(2)(5)=5$. So the area is $20-11=9$ ✓.
:::

::: example Area zero means collinear; an unknown vertex
**Problem.** (i) Use area to show that $(1,2)$, $(3,6)$ and $(4,8)$ are collinear. (ii) Find $k$ if the area of the triangle with vertices $(k,0)$, $(4,0)$ and $(0,2)$ is 4 square units.

**Solution.** (i) $\frac{1}{2}\left|1(6-8)+3(8-2)+4(2-6)\right|=\frac{1}{2}\left|-2+18-16\right|=0$. Zero area: the points are collinear.

(ii) $\frac{1}{2}\left|k(0-2)+4(2-0)+0(0-0)\right|=4$, so $|8-2k|=8$. Then $8-2k=8$ gives $k=0$, or $8-2k=-8$ gives $k=8$. Both $(0,0)$ and $(8,0)$ work: each makes a base of 4 along the $x$-axis with height 2.
:::

::: example Area of a quadrilateral
**Problem.** Find the area of the quadrilateral with vertices $A(1,1)$, $B(6,2)$, $C(5,6)$, $D(2,5)$, (i) by splitting it along $AC$, (ii) by the arrow method.

**Solution.** (i) $\triangle ABC=\frac{1}{2}\left|1(2-6)+6(6-1)+5(1-2)\right|=\frac{1}{2}\left|-4+30-5\right|=\frac{21}{2}$.

$\triangle ACD=\frac{1}{2}\left|1(6-5)+5(5-1)+2(1-6)\right|=\frac{1}{2}\left|1+20-10\right|=\frac{11}{2}$.

Area $=\frac{21}{2}+\frac{11}{2}=16$ square units.

(ii) Rows $x$: 1, 6, 5, 2, 1 and $y$: 1, 2, 6, 5, 1. The cross terms are
$$ (1\cdot2-6\cdot1)+(6\cdot6-5\cdot2)+(5\cdot5-2\cdot6)+(2\cdot1-1\cdot5)=-4+26+13-3=32 $$
Area $=\frac{1}{2}\times32=16$ square units, the same.
:::

::: example A field on a map grid
**Problem.** A field in Chitwan is drawn on a grid in which 1 unit is 10 m. Its corners are at $(0,0)$, $(8,0)$, $(10,6)$ and $(2,7)$. Find its area in square metres.

**Solution.** By the arrow method:
$$ (0\cdot0-8\cdot0)+(8\cdot6-10\cdot0)+(10\cdot7-2\cdot6)+(2\cdot0-0\cdot7) $$
$$ =0+48+58+0=106 $$
Area $=\frac{1}{2}\times106=53$ square units. One square unit is $10\text{ m}\times10\text{ m}=100$ m², so the field is $53\times100=5300$ m².
:::

::: tip Take the vertices in order
For a quadrilateral, list the vertices **in order round the boundary**, either clockwise or anticlockwise. If you jump across (for example $A, C, B, D$), the arrows trace a crossed figure and the answer is wrong. A quick sketch on the grid shows the correct order at once.
:::

::: note Activity — survey the school garden
Mark the four corners of a flower bed or a corner of the school ground with pegs. Choose one corner as the origin, lay a measuring tape along one edge as the $x$-axis, and measure the $x$ and $y$ distances of the other corners in metres. (1) Plot the corners on squared paper. (2) Find the length of each side and each diagonal with the distance formula, and check one of them with the tape. (3) Find the area with the arrow method. (4) Find the mid-point of the longest side and mark it with a peg. How close is it to the real middle?
:::

## Chapter summary

- **Distance:** $PQ=\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}$; from the origin $\sqrt{x^2+y^2}$. Compare squared lengths to classify triangles and quadrilaterals; $AB+BC=AC$ means collinear.
- **Section formula** (internal, $m_1:m_2$): $\left(\frac{m_1x_2+m_2x_1}{m_1+m_2},\ \frac{m_1y_2+m_2y_1}{m_1+m_2}\right)$.
- **Mid-point:** $\left(\frac{x_1+x_2}{2},\ \frac{y_1+y_2}{2}\right)$; centroid $\left(\frac{x_1+x_2+x_3}{3},\ \frac{y_1+y_2+y_3}{3}\right)$.
- **Slope:** $m=\frac{y_2-y_1}{x_2-x_1}=\tan\theta$; horizontal lines have slope 0, vertical lines have no defined slope; parallel lines have equal slopes.
- Lines parallel to the axes: $x=a$ and $y=b$; the axes are $y=0$ and $x=0$.
- **Slope-intercept form:** $y=mx+c$, with slope $m$ and $y$-intercept $c$; make $y$ the subject before reading them.
- **Area of a triangle:** $\frac{1}{2}\left|x_1(y_2-y_3)+x_2(y_3-y_1)+x_3(y_1-y_2)\right|$; for a quadrilateral, use the arrow method with the vertices in order, or split into two triangles. Zero area means collinear.

## Practice questions

**Group A — Objective (1 mark each)**

1. The distance between $(0,0)$ and $(6,8)$ is <span class="marks">[1]</span>
   (a) 14 (b) 10 (c) 48 (d) 100
2. The distance between $(2,3)$ and $(2,9)$ is <span class="marks">[1]</span>
   (a) 6 (b) 12 (c) 4 (d) 36
3. The mid-point of $(4,-2)$ and $(-2,6)$ is <span class="marks">[1]</span>
   (a) $(1,2)$ (b) $(2,4)$ (c) $(3,-4)$ (d) $(1,4)$
4. The point dividing the join of $(0,0)$ and $(6,9)$ in the ratio $1:2$ is <span class="marks">[1]</span>
   (a) $(2,3)$ (b) $(4,6)$ (c) $(3,4.5)$ (d) $(1,2)$
5. The slope of the line through $(1,2)$ and $(4,8)$ is <span class="marks">[1]</span>
   (a) 2 (b) $\frac{1}{2}$ (c) 6 (d) 3
6. The slope of a line parallel to the $x$-axis is <span class="marks">[1]</span>
   (a) 1 (b) 0 (c) not defined (d) $-1$
7. The line through $(3,-5)$ parallel to the $y$-axis is <span class="marks">[1]</span>
   (a) $y=-5$ (b) $x=3$ (c) $y=3$ (d) $x=-5$
8. The slope and $y$-intercept of $y=4x-7$ are <span class="marks">[1]</span>
   (a) 4 and 7 (b) $-7$ and 4 (c) 4 and $-7$ (d) $-4$ and 7
9. The $y$-intercept of $2x+y=6$ is <span class="marks">[1]</span>
   (a) 2 (b) $-2$ (c) 6 (d) 3
10. The area of the triangle with vertices $(0,0)$, $(4,0)$ and $(0,3)$ is <span class="marks">[1]</span>
    (a) 12 (b) 6 (c) 7 (d) 5
11. Three points are collinear if the area of the triangle they form is <span class="marks">[1]</span>
    (a) 1 (b) 0 (c) negative (d) 180
12. A line of slope 1 has inclination <span class="marks">[1]</span>
    (a) $0^\circ$ (b) $30^\circ$ (c) $45^\circ$ (d) $90^\circ$

::: note Answers to Group A
**1.** (b) — $\sqrt{36+64}=10$.
**2.** (a) — same $x$-coordinate, so the distance is $9-3=6$.
**3.** (a) — $\left(\frac{4-2}{2},\frac{-2+6}{2}\right)=(1,2)$.
**4.** (a) — $\left(\frac{1(6)+2(0)}{3},\frac{1(9)+2(0)}{3}\right)=(2,3)$.
**5.** (a) — $\frac{8-2}{4-1}=2$.
**6.** (b) — a horizontal line has zero rise.
**7.** (b) — every point on it has $x=3$.
**8.** (c) — compare with $y=mx+c$.
**9.** (c) — $y=-2x+6$, so $c=6$.
**10.** (b) — a right triangle with legs 4 and 3: $\frac{1}{2}\times4\times3=6$.
**11.** (b) — the points then lie on one line.
**12.** (c) — $\tan45^\circ=1$.
:::

**Group B — Short answer (2 marks each)**

1. Find the distance between $P(-3,4)$ and $Q(2,-8)$. <span class="marks">[2]</span>
2. Find the point that divides the join of $A(2,3)$ and $B(7,8)$ internally in the ratio $2:3$. <span class="marks">[2]</span>
3. $M(2,3)$ is the mid-point of $AB$, where $A$ is $(-1,5)$. Find $B$. <span class="marks">[2]</span>
4. Find the slope of the line through $(-1,4)$ and $(3,-2)$, and say whether the line rises or falls to the right. <span class="marks">[2]</span>
5. Write the equation of the line whose slope is $-2$ and whose $y$-intercept is 5. <span class="marks">[2]</span>
6. Find the slope and the $y$-intercept of $3x-4y=12$. <span class="marks">[2]</span>
7. Find $k$ if the distance between $(k,3)$ and $(2,-1)$ is 5 units. <span class="marks">[2]</span>
8. Find the area of the triangle with vertices $(1,2)$, $(5,3)$ and $(3,7)$. <span class="marks">[2]</span>
9. Use slopes to show that $(1,2)$, $(3,6)$ and $(4,8)$ are collinear. <span class="marks">[2]</span>
10. Write the equations of the lines through $(-2,4)$ parallel to the $x$-axis and to the $y$-axis. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $PQ=\sqrt{(2+3)^2+(-8-4)^2}=\sqrt{25+144}=\sqrt{169}=13$ units.
**2.** $\left(\frac{2(7)+3(2)}{5},\ \frac{2(8)+3(3)}{5}\right)=\left(\frac{20}{5},\frac{25}{5}\right)=(4,5)$.
**3.** $\frac{-1+x}{2}=2$ gives $x=5$; $\frac{5+y}{2}=3$ gives $y=1$. So $B=(5,1)$.
**4.** $m=\frac{-2-4}{3+1}=-\frac{6}{4}=-\frac{3}{2}$. The slope is negative, so the line **falls** to the right.
**5.** $y=-2x+5$.
**6.** $-4y=-3x+12$, so $y=\frac{3}{4}x-3$: slope $\frac{3}{4}$, $y$-intercept $-3$.
**7.** $(k-2)^2+16=25$, so $(k-2)^2=9$ and $k-2=\pm3$: $k=5$ or $k=-1$.
**8.** $\frac{1}{2}\left|1(3-7)+5(7-2)+3(2-3)\right|=\frac{1}{2}\left|-4+25-3\right|=9$ square units.
**9.** Slope of the first two points $=\frac{6-2}{3-1}=2$; slope of the last two $=\frac{8-6}{4-3}=2$. Equal slopes through the common point $(3,6)$: collinear.
**10.** Parallel to the $x$-axis: $y=4$. Parallel to the $y$-axis: $x=-2$.
:::

**Group C — Long answer (4 marks each)**

1. Show that $A(2,1)$, $B(5,3)$ and $C(1,9)$ are the vertices of a right-angled triangle, and find its area in two ways. <span class="marks">[4]</span>
2. Find the points of trisection of the segment joining $A(1,2)$ and $B(7,11)$, and the mid-point of $AB$. <span class="marks">[4]</span>
3. Find the equation of the line through $(1,2)$ and $(3,8)$ in the form $y=mx+c$. State its slope and $y$-intercept, and check whether $(-1,-4)$ lies on it. <span class="marks">[4]</span>
4. Show that $A(0,0)$, $B(4,1)$, $C(5,5)$ and $D(1,4)$ are the vertices of a rhombus but not of a square, and find its area. <span class="marks">[4]</span>
5. Find the area of the quadrilateral with vertices $A(1,1)$, $B(6,2)$, $C(5,6)$ and $D(2,5)$ (i) by dividing it into two triangles along $AC$, (ii) by the arrow method. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** $AB^2=9+4=13$, $BC^2=16+36=52$, $AC^2=1+64=65$. Since $13+52=65$, $AB^2+BC^2=AC^2$ and the triangle is right-angled at $B$. Area (i) $=\frac{1}{2}\times AB\times BC=\frac{1}{2}\sqrt{13}\sqrt{52}=\frac{1}{2}\sqrt{676}=\frac{1}{2}\times26=13$ square units. (ii) By the formula: $\frac{1}{2}\left|2(3-9)+5(9-1)+1(1-3)\right|=\frac{1}{2}\left|-12+40-2\right|=13$ ✓.
**2.** $P$ (ratio $1:2$) $=\left(\frac{7+2}{3},\frac{11+4}{3}\right)=(3,5)$; $Q$ (ratio $2:1$) $=\left(\frac{14+1}{3},\frac{22+2}{3}\right)=(5,8)$. Mid-point $=\left(\frac{1+7}{2},\frac{2+11}{2}\right)=(4,\ 6.5)$, which lies between $P$ and $Q$, as it should.
**3.** $m=\frac{8-2}{3-1}=3$; $2=3(1)+c$ gives $c=-1$. The line is $y=3x-1$, with slope 3 and $y$-intercept $-1$. At $x=-1$: $y=-3-1=-4$, so $(-1,-4)$ **does** lie on the line.
**4.** $AB^2=17$, $BC^2=17$, $CD^2=17$, $DA^2=17$: all sides are $\sqrt{17}$, so it is a rhombus. Diagonals: $AC^2=50$, $BD^2=18$; they are unequal, so it is not a square. Area by the arrow method: $(0-0)+(20-5)+(20-5)+(0-0)=30$, so the area is $\frac{1}{2}\times30=15$ square units. (Check: for a rhombus, area $=\frac{1}{2}d_1d_2=\frac{1}{2}\sqrt{50}\sqrt{18}=\frac{1}{2}\sqrt{900}=15$ ✓.)
**5.** (i) $\triangle ABC=\frac{1}{2}\left|1(2-6)+6(6-1)+5(1-2)\right|=\frac{21}{2}$ and $\triangle ACD=\frac{1}{2}\left|1(6-5)+5(5-1)+2(1-6)\right|=\frac{11}{2}$, total $16$ square units. (ii) Cross terms $(2-6)+(36-10)+(25-12)+(2-5)=-4+26+13-3=32$, area $=\frac{1}{2}\times32=16$ square units.
:::
