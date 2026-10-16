---
subject: Mathematics
grade: 8
unit: 17
title: Coordinates
hours: 0
area: Compulsory Mathematics
---

A coordinate is a pair of numbers that says exactly where a point is: how far
across and how far up. With that one idea, geometry becomes arithmetic — a shape
is a list of points, a distance is a subtraction and a square root, and a
straight line is an equation. This chapter fixes the vocabulary, shows how to
plot and read points, and shows how to find the distance between two of them.

::: key What this chapter asks of you
You should be able to plot a point given its coordinates, name the quadrant a
point lies in, find the distance between two points on the same horizontal or
vertical line and between any two points using the distance formula, and
identify a simple shape from the coordinates of its vertices.
:::

## 17.1 The coordinate plane

Two number lines crossing at right angles make the **coordinate plane**. The
horizontal line is the **$x$-axis**, the vertical line is the **$y$-axis**, and
their crossing point $O$ is the **origin**, with coordinates $(0,0)$.

A point is written as an ordered pair $(x,y)$:

- the **$x$-coordinate** (abscissa) is how far the point is from the $y$-axis,
  positive to the right;
- the **$y$-coordinate** (ordinate) is how far it is from the $x$-axis, positive
  upwards.

The axes divide the plane into four **quadrants**, numbered anticlockwise from
the top right.

| Quadrant | $x$ | $y$ | Example |
|---|---|---|---|
| I (top right) | positive | positive | $(3,4)$ |
| II (top left) | negative | positive | $(-3,4)$ |
| III (bottom left) | negative | negative | $(-3,-4)$ |
| IV (bottom right) | positive | negative | $(3,-4)$ |

A point on an axis belongs to no quadrant: $(5,0)$ lies on the $x$-axis and
$(0,-2)$ on the $y$-axis.

```figure caption="The coordinate plane. The signs of the two coordinates tell you the quadrant, which is the quickest check that a point has been plotted on the right side of both axes."
fig, ax = plt.subplots(figsize=(4.8, 3.0))
ax.set_xlim(-6, 6)
ax.set_ylim(-5, 5)
ax.axhline(0, color=INK, lw=0.9)
ax.axvline(0, color=INK, lw=0.9)
ax.grid(True, color=GRID, lw=0.5)
for x, y, name, c in [(3, 4, "I", ACCENT), (-3, 4, "II", SERIES[1]),
                      (-3, -4, "III", SERIES[2]), (3, -4, "IV", SERIES[3])]:
    ax.plot([x], [y], "o", color=c, ms=5)
    ax.annotate("$(%d,%d)$" % (x, y), (x, y), xytext=(x + 0.25, y + 0.45),
                fontsize=7, color=c)
    ax.text(x * 2.1, y * 1.05, name, fontsize=9, color=c, ha="center", va="center")
ax.text(5.6, -0.5, "x", fontsize=8.5, color=INK)
ax.text(0.2, 4.7, "y", fontsize=8.5, color=INK)
ax.set_xticks(range(-6, 7, 2))
ax.set_yticks(range(-4, 6, 2))
ax.tick_params(labelsize=7.5, length=0)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
```

::: caution The order is fixed: across, then up
$(3,4)$ and $(4,3)$ are different points. Always write $x$ first. When plotting,
go across from the $y$-axis first and then up or down from the $x$-axis — doing
it in the other order swaps every point in the figure.
:::

## 17.2 Distance between two points

### 17.2.1 Points on the same horizontal or vertical line

If two points have the same $y$-coordinate, the distance between them is the
difference of their $x$-coordinates. If they have the same $x$-coordinate, it is
the difference of their $y$-coordinates. Take the positive value in each case.

::: example Horizontal and vertical distances
**Problem.** Find the distance between (a) $A(2,3)$ and $B(7,3)$, and
(b) $C(2,3)$ and $D(2,-4)$.

**Solution.** (a) The $y$-coordinates are equal, so
$AB=7-2=5$ units.

(b) The $x$-coordinates are equal, so $CD=3-(-4)=7$ units.

**Check.** In (a) both points lie on the line $y=3$; in (b) both lie on
$x=2$ ✓. For (b), the subtraction $3-(-4)=7$ shows why the sign must be handled
carefully — the points are on opposite sides of the $x$-axis.
:::

### 17.2.2 Any two points: the distance formula

Join the two points to make a right-angled triangle whose horizontal and
vertical sides are the differences of the coordinates. Then Pythagoras gives

$$d=\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}$$

```figure caption="The distance formula is Pythagoras in disguise. The horizontal side is the difference of the x-coordinates and the vertical side is the difference of the y-coordinates, so the distance is the hypotenuse."
fig, ax = plt.subplots(figsize=(4.8, 2.8))
ax.set_xlim(-1, 8)
ax.set_ylim(-1, 6)
ax.axhline(0, color=INK, lw=0.8)
ax.axvline(0, color=INK, lw=0.8)
ax.grid(True, color=GRID, lw=0.5)
ax.plot([1, 6], [1, 1], color=SERIES[1], lw=1.6)
ax.plot([6, 6], [1, 5], color=SERIES[2], lw=1.6)
ax.plot([1, 6], [1, 5], color=ACCENT, lw=1.8)
ax.plot([1, 6], [1, 5], "o", color=INK, ms=4)
ax.annotate("$A(1,1)$", (1, 1), xytext=(1.05, 0.35), fontsize=7, color=INK)
ax.annotate("$B(6,5)$", (6, 5), xytext=(5.4, 5.25), fontsize=7, color=INK)
ax.text(3.5, 0.55, "$x_2-x_1=5$", fontsize=7, color=SERIES[1], ha="center")
ax.text(6.15, 3.0, "$y_2-y_1=4$", fontsize=7, color=SERIES[2])
ax.text(2.6, 3.6, "$d=\\sqrt{5^2+4^2}$", fontsize=7.5, color=ACCENT)
ax.set_xticks(range(0, 8, 2))
ax.set_yticks(range(0, 6, 2))
ax.tick_params(labelsize=7.5, length=0)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
```

::: example Using the distance formula
**Problem.** Find the distance between $A(1,1)$ and $B(6,5)$.

**Solution.**

$$d=\sqrt{(6-1)^2+(5-1)^2}=\sqrt{25+16}=\sqrt{41}\approx6.4\ \text{units}$$

**Answer.** About 6.4 units.

**Check.** The horizontal difference is 5 and the vertical is 4, so the distance
must be between 5 and 7 (it is the hypotenuse of a 5-4-right triangle), and 6.4
lies in that interval ✓.
:::

::: example Finding a missing coordinate
**Problem.** The distance between $A(2,3)$ and $B(7,y)$ is 13 units. Find the
possible values of $y$.

**Solution.**

$$13=\sqrt{(7-2)^2+(y-3)^2}=\sqrt{25+(y-3)^2}$$

Squaring both sides: $169=25+(y-3)^2$, so $(y-3)^2=144$ and $y-3=\pm12$.

$$y=15\quad\text{or}\quad y=-9$$

**Answer.** $y=15$ or $y=-9$.

**Check.** $y=15$: $d=\sqrt{25+144}=\sqrt{169}=13$ ✓. $y=-9$:
$d=\sqrt{25+(-12)^2}=\sqrt{169}=13$ ✓. Two answers, one above $A$ and one
below — and both are correct, because a circle of radius 13 about $A$ meets the
line $x=7$ twice.
:::

## 17.3 Shapes from coordinates

A set of points can be joined to make a shape, and the coordinates tell you what
kind it is.

| Shape | What to check |
|---|---|
| Square | four equal sides and one right angle; diagonals equal and bisecting |
| Rectangle | opposite sides equal, adjacent sides perpendicular |
| Parallelogram | opposite sides equal and parallel (equal in both directions) |
| Rhombus | four equal sides |
| Right triangle | the squares of two sides add to the square of the longest |
| Isosceles triangle | two sides equal |
| Collinear points | the slopes between consecutive pairs are all equal |

::: example Identifying a quadrilateral
**Problem.** The points $A(0,0)$, $B(4,0)$, $C(4,3)$ and $D(0,3)$ are joined in
order. What shape is $ABCD$? Find its perimeter and area.

**Solution.** The four sides are

$$AB=4,\quad BC=3,\quad CD=4,\quad DA=3$$

Opposite sides are equal, and $AB$ is horizontal while $BC$ is vertical, so the
angle at $B$ is a right angle. The figure is a **rectangle**.

Perimeter $=4+3+4+3=14$ units, and
area $=4\times3=12$ square units.

**Check.** The diagonal $AC=\sqrt{(4-0)^2+(3-0)^2}=\sqrt{25}=5$, and the
diagonals of a rectangle are equal, so $BD$ must also be 5: from $B(4,0)$ to
$D(0,3)$, $BD=\sqrt{16+9}=5$ ✓.
:::

::: example A right-angled triangle from coordinates
**Problem.** Show that the triangle with vertices $P(1,1)$, $Q(5,1)$ and
$R(1,4)$ is right-angled, and find its area.

**Solution.** Compute the three sides:

$$PQ=\sqrt{(5-1)^2+0}=4,\qquad PR=\sqrt{0+(4-1)^2}=3$$

$$QR=\sqrt{(5-1)^2+(1-4)^2}=\sqrt{16+9}=5$$

Now test: $3^2+4^2=9+16=25=5^2$. Since the squares of the two shorter sides add
to the square of the longest, the angle between $PQ$ and $PR$ is a right angle,
so the triangle is **right-angled at $P$**.

$$\text{Area}=\frac12\times4\times3=6\ \text{square units}$$

**Check.** $PQ$ is horizontal and $PR$ is vertical, so they are perpendicular by
inspection as well as by Pythagoras ✓.
:::

::: caution A square needs the right angles as well as equal sides
Four equal sides give a **rhombus**, not necessarily a square. Four equal sides
with one right angle (or with equal diagonals) give a square. Check the angles,
not only the lengths.
:::

## 17.4 Reading a point in four quadrants

```figure caption="The four quadrants with the sign pattern of (x, y). Mixing up the order of the coordinates is the commonest error — x always comes first."
fig, ax = plt.subplots(figsize=(4.3, 3.6))
ax.axhline(0, color=INK, linewidth=1.2)
ax.axvline(0, color=INK, linewidth=1.2)
quad = [("I\n$(+,+)$", 2.2, 2.2), ("II\n$(-,+)$", -2.2, 2.2),
        ("III\n$(-,-)$", -2.2, -2.2), ("IV\n$(+,-)$", 2.2, -2.2)]
for lab, x, y in quad:
    ax.text(x, y, lab, ha="center", va="center", color=MUTED, fontsize=9)
pts = [("A(3,2)", 3, 2), ("B(-3,1)", -3, 1), ("C(-2,-3)", -2, -3),
       ("D(4,-2)", 4, -2)]
for lab, x, y in pts:
    ax.plot([x], [y], marker="o", markersize=6, color=SERIES[0])
    ax.annotate(lab, xy=(x, y), xytext=(x + 0.25, y + 0.3), fontsize=8,
                color=INK)
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_xticks(range(-4, 5, 2))
ax.set_yticks(range(-4, 5, 2))
ax.grid(color=GRID, linewidth=0.7)
ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.tick_params(colors=MUTED, labelsize=8)
ax.set_aspect("equal")
```

| Task | Rule |
|---|---|
| Plot $(x, y)$ | $x$ along the horizontal axis first, then $y$ |
| Distance from the origin | $\sqrt{x^2 + y^2}$ |
| Distance between two points | $\sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}$ |
| Point on the $x$-axis | $y = 0$, e.g. $(5, 0)$ |
| Point on the $y$-axis | $x = 0$, e.g. $(0, -3)$ |
| Midpoint of a segment | $\left(\frac{x_1+x_2}{2}, \frac{y_1+y_2}{2}\right)$ |

::: example Distance and midpoint together
**Question.** For $P(2, 3)$ and $Q(8, 11)$, find (i) the distance $PQ$
(ii) the midpoint of $PQ$.

**Answer.**
(i) $PQ = \sqrt{(8-2)^2 + (11-3)^2} = \sqrt{36 + 64} = \sqrt{100} =
\textbf{10 units}$.
(ii) Midpoint $= \left(\frac{2+8}{2}, \frac{3+11}{2}\right) = \textbf{(5, 7)}$.
:::

::: example Area of a triangle from coordinates
**Question.** Find the area of the triangle with vertices $A(1,1)$, $B(5,1)$
and $C(1,6)$.

**Answer.** $AB$ is horizontal with length $5 - 1 = 4$; $AC$ is vertical with
length $6 - 1 = 5$; the angle at $A$ is a right angle.
Area $= \frac{1}{2} \times 4 \times 5 = \textbf{10 square units}$.
:::

::: note Activity — treasure hunt on squared paper
In pairs, each student hides a "treasure" at a lattice point on a grid from
$-6$ to $6$ and writes down its coordinates. Partners take turns guessing a
point; the hider answers only with the **distance** to the treasure, worked out
with the distance formula. Three correct distances are usually enough to locate
it.
:::

## Chapter summary

- A point is written $(x,y)$, $x$ first; the axes divide the plane into four
  quadrants, and the signs of the coordinates decide which.
- On a horizontal line the distance is the difference of the $x$-coordinates; on
  a vertical line it is the difference of the $y$-coordinates.
- For any two points,
  $d=\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}$, which is Pythagoras' theorem.
- Joining points and comparing the side lengths and the angles identifies the
  shape; equal sides alone give a rhombus, not a square.
- A triangle is right-angled exactly when the squares of two sides add to the
  square of the third.

## Practice questions

**Group A — Objective (1 mark each)**

1. The point $(-2,5)$ lies in quadrant <span class="marks">[1]</span>
   (a) I (b) II (c) III (d) IV
2. The distance between $(0,0)$ and $(3,4)$ is <span class="marks">[1]</span>
   (a) 5 (b) 7 (c) 12 (d) 25
3. The point $(0,-6)$ lies <span class="marks">[1]</span>
   (a) on the $x$-axis (b) on the $y$-axis (c) in quadrant III (d) at the origin
4. The distance between $(2,7)$ and $(9,7)$ is <span class="marks">[1]</span>
   (a) 5 (b) 7 (c) 9 (d) 14
5. The distance formula is a form of <span class="marks">[1]</span>
   (a) the area formula (b) Pythagoras' theorem (c) the cosine rule
   (d) Euler's relation
6. $(4,3)$ and $(3,4)$ are <span class="marks">[1]</span>
   (a) the same point (b) different points (c) both on the $x$-axis
   (d) both in quadrant II

::: note Answers to Group A
**1.** (b) — $x$ negative, $y$ positive.
**2.** (a) — $\sqrt{9+16}=5$.
**3.** (b) — $x=0$ means the point is on the $y$-axis.
**4.** (b) — $9-2=7$.
**5.** (b) — the differences of the coordinates are the legs of a right triangle.
**6.** (b) — the order matters.
:::

**Group B — Short answer (2 marks each)**

1. Plot $A(1,2)$, $B(4,2)$ and $C(4,6)$ and find the length of $BC$.
   <span class="marks">[2]</span>
2. Find the distance between $(-2,-3)$ and $(3,9)$.
   <span class="marks">[2]</span>
3. In which quadrant does each of $(5,-2)$, $(-4,-6)$ and $(-1,7)$ lie?
   <span class="marks">[2]</span>
4. Find the distance of the point $(6,8)$ from the origin.
   <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $BC$ is vertical, so $BC=6-2=4$ units.
**2.** $d=\sqrt{(3+2)^2+(9+3)^2}=\sqrt{25+144}=\sqrt{169}=13$.
**3.** $(5,-2)$ — quadrant IV; $(-4,-6)$ — quadrant III; $(-1,7)$ — quadrant II.
**4.** $\sqrt{36+64}=\sqrt{100}=10$.
:::

**Group C — Long answer (4 marks each)**

1. The points $A(-2,1)$, $B(2,1)$, $C(2,-2)$ and $D(-2,-2)$ are joined in order.
   Identify the shape, find its perimeter and area, and find the length of a
   diagonal. <span class="marks">[4]</span>
2. Show that $P(0,0)$, $Q(6,0)$ and $R(0,8)$ form a right-angled triangle, find
   its area, and find the length of the hypotenuse.
   <span class="marks">[4]</span>

::: note Answers to Group C
**1.** $AB=2-(-2)=4$ and $BC=1-(-2)=3$, with $AB$ horizontal and $BC$
vertical, so the figure is a **rectangle** 4 units by 3 units.
Perimeter $=2(4+3)=14$ units; area $=4\times3=12$ square units.
Diagonal $=\sqrt{4^2+3^2}=\sqrt{25}=5$ units.
**Check.** The other diagonal is also 5 ✓, as a rectangle's diagonals are equal.
**2.** $PQ=6$ (horizontal), $PR=8$ (vertical), and
$QR=\sqrt{(6-0)^2+(0-8)^2}=\sqrt{36+64}=10$.
Since $6^2+8^2=36+64=100=10^2$, the angle at $P$ is a right angle and the
triangle is right-angled at $P$. Area $=\frac12\times6\times8=24$ square units.
Hypotenuse $=QR=10$ units.
**Check.** $PQ$ lies along the $x$-axis and $PR$ along the $y$-axis, so they meet
at 90° ✓, and the hypotenuse is the side opposite the right angle, which is
$QR$.
:::

**Extra practice**

**Group B (2 marks)**

11. State the quadrant of $(-7, 4)$ and of $(5, -9)$.
12. Find the distance of $(-6, 8)$ from the origin.

**Group C (4 marks)**

13. $P(2,-1)$, $Q(6,-1)$ and $R(6,4)$ are the vertices of a triangle. Find
    (i) $PQ$ (ii) $QR$ (iii) $PR$ (iv) the area of the triangle.

::: note Extra practice — answers
**11.** $(-7,4)$ is in the second quadrant; $(5,-9)$ is in the fourth.
**12.** $\sqrt{36+64} = 10$ units.
**13.** (i) $PQ = 6 - 2 = 4$ units (horizontal).
(ii) $QR = 4 - (-1) = 5$ units (vertical).
(iii) $PR = \sqrt{4^2 + 5^2} = \sqrt{41} \approx 6.4$ units.
(iv) The right angle is at $Q$, so area $= \frac{1}{2} \times 4 \times 5 =
10$ square units.
:::
