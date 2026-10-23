---
subject: Mathematics
grade: 8
unit: 19
title: Transformation
hours: 0
area: Compulsory Mathematics
---

A transformation moves a shape without changing what it is made of. Slide a
booking form across the desk, look at it in the mirror, spin it round, or make a
photocopy at 150 % — those are the four transformations of this chapter:
translation, reflection, rotation and enlargement. The first three leave the
shape the same size; the fourth changes it, and everything about the arithmetic
of enlargement follows from one ratio.

::: key What this chapter asks of you
You should be able to describe a translation as a vector, reflect a point or a
figure in the axes and in simple lines, rotate a figure about a point through
90°, 180° or 270°, enlarge a figure by a given scale factor, and state the
coordinates of the image in each case.
:::

## 19.1 Translation

A **translation** slides every point of a figure the same distance in the same
direction. Nothing is turned, nothing is flipped and the size does not change,
so the image is **congruent** to the object.

A translation is described by a pair of numbers: a movement of $a$ units in
the $x$-direction and $b$ units in the $y$-direction, written as the column
$(a,b)$ read downwards.

$$(x,y)\longrightarrow(x+a,\;y+b)$$

::: example Translating points
**Problem.** Translate the point $A(2,3)$ by 4 units to the right and 5 units
down. Find the image, and translate the same point 3 units left and 2 units up.

**Solution.** Right and down: $(2+4,\;3-5)=(6,-2)$.

Left and up: $(2-3,\;3+2)=(-1,5)$.

**Answer.** $(6,-2)$ and $(-1,5)$.

**Check.** For the first, the point moves from quadrant I into quadrant IV,
because it has gone down past the $x$-axis: $3-5=-2$ ✓. For the second, it moves
from quadrant I into quadrant II, because $x$ becomes negative ✓.
:::

::: example Translating a triangle
**Problem.** A triangle has vertices $A(1,1)$, $B(4,1)$, $C(1,3)$. Find the
vertices of its image under a translation of 2 units right and 3 units up, and
say what kind of figure the image is.

**Solution.**

$$A'=(1+2,\;1+3)=(3,4)$$
$$B'=(4+2,\;1+3)=(6,4)$$
$$C'=(1+2,\;3+3)=(3,6)$$

The image has a horizontal side $A'B'$ of length 3 and a vertical side $A'C'$ of
length 2, exactly as the original.

**Answer.** $A'(3,4)$, $B'(6,4)$, $C'(3,6)$; a right-angled triangle congruent
to the original.

**Check.** $AB=4-1=3$ and $A'B'=6-3=3$ ✓; the side lengths are unchanged, as a
translation must leave them.
:::

::: caution A translation is not a rotation
Sliding a shape to the right does not change which way it faces. A common error
is to "translate" a figure and draw it turned round. Check that the image is
parallel to the object: the corresponding sides must point in the same
directions.
:::

## 19.2 Reflection

A **reflection** flips a figure across a line, the **mirror line** or axis. The
image is congruent to the object, but the two face opposite ways.

| Mirror line | Rule | Example: $(2,5)$ goes to |
|---|---|---|
| $x$-axis ($y=0$) | $y$ changes sign | $(2,-5)$ |
| $y$-axis ($x=0$) | $x$ changes sign | $(-2,5)$ |
| line $y=x$ | coordinates swap | $(5,2)$ |
| line $y=-x$ | coordinates swap and both change sign | $(-5,-2)$ |
| line $x=a$ | $x$ becomes $2a-x$ | for $x=3$: $(4,5)$ |
| line $y=b$ | $y$ becomes $2b-y$ | for $y=1$: $(2,-3)$ |

A point on the mirror line does not move at all — it is its own image.

```figure caption="Triangle ABC with A(1, 1), B(3, 1), C(1, 3) and its images. Reflection in the y-axis changes the sign of x; reflection in the x-axis changes the sign of y. Each point and its image are the same distance from the mirror line."
fig, ax = plt.subplots(figsize=(4.4, 3.4))
T = np.array([[1, 1], [3, 1], [1, 3], [1, 1]])
for M, c, lab, pos in [(np.array([1, 1]), ACCENT, "ABC", (1.6, 3.2)), (np.array([-1, 1]), SERIES[1], "A′B′C′ (in y-axis)", (-4.6, 3.3)),
                       (np.array([1, -1]), SERIES[2], "A″B″C″ (in x-axis)", (1.2, -3.7))]:
    P = T * M
    ax.plot(P[:, 0], P[:, 1], color=c, lw=1.6); ax.fill(P[:, 0], P[:, 1], color=c, alpha=0.12)
    ax.text(pos[0], pos[1], lab, fontsize=8.5, color=c)
ax.plot([1, -1], [3, 3], color=MUTED, lw=0.8, ls=":"); ax.plot([1, 1], [1, -1], color=MUTED, lw=0.8, ls=":")
ax.axhline(0, color=INK, lw=1.0); ax.axvline(0, color=INK, lw=1.0)
ax.set_xlim(-5, 5); ax.set_ylim(-4.2, 4.2)
ax.set_xticks([-4, -2, 2, 4]); ax.set_yticks([-4, -2, 2, 4]); ax.tick_params(labelsize=7.5, length=0)
ax.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
for sp in ax.spines.values(): sp.set_visible(False)
```

::: example Reflecting in the axes
**Problem.** A triangle has vertices $A(2,1)$, $B(5,1)$, $C(2,4)$. Reflect it in
the $x$-axis and then in the $y$-axis, and give the coordinates of both images.

**Solution.** In the $x$-axis, $y$ changes sign:

$$A'(2,-1),\quad B'(5,-1),\quad C'(2,-4)$$

In the $y$-axis, $x$ changes sign:

$$A''(-2,1),\quad B''(-5,1),\quad C''(-2,4)$$

**Answer.** As above.

**Check.** $AB=3$ and $A'B'=5-2=3$ ✓; $A''B''=3$ ✓. Reflection never changes
lengths.
:::

::: example Reflecting in the line $y=x$
**Problem.** Find the image of $P(3,7)$ in the line $y=x$ and show that the
mirror line passes through the midpoint of $PP'$.

**Solution.** Reflection in $y=x$ swaps the coordinates, so $P'=(7,3)$.

Midpoint of $PP'$ $=\left(\frac{3+7}{2},\frac{7+3}{2}\right)=(5,5)$, and
$(5,5)$ lies on $y=x$ ✓.
:::

## 19.3 Rotation

A **rotation** turns a figure about a fixed point, the **centre of rotation**,
through a given angle and in a given direction (clockwise or anticlockwise). The
image is congruent to the object, and the orientation changes.

Three things describe a rotation: the **centre**, the **angle** and the
**direction**. Anticlockwise is the **positive** direction ($+90°$) and
clockwise (the way the hands of a clock move) is the **negative** direction
($-90°$).

**Drawing a rotation with protractor and compasses.** To rotate $A$ through
$+90°$ about O: join OA; at O draw $\angle AOB=90°$ anticlockwise; with centre
O and radius OA cut OB at $A'$. Then $A'$ is the image.

The rotations most often asked for are about the origin $O(0,0)$.

| Rotation about the origin | Rule | $(3,2)$ goes to |
|---|---|---|
| $+90°$ (anticlockwise) | $(-y,x)$ | $(-2,3)$ |
| $180°$ | $(-x,-y)$ | $(-3,-2)$ |
| $-90°$ (clockwise) | $(y,-x)$ | $(2,-3)$ |
| $270°$ anticlockwise | $(y,-x)$ | $(2,-3)$ |

::: example Rotating about the origin
**Problem.** A point $A(3,2)$ is rotated about the origin through $90°$
anticlockwise. Find the image. Then rotate the same point through $180°$.

**Solution.** For $90°$ anticlockwise, $(x,y)\to(-y,x)$:

$$A'=(-2,3)$$

For $180°$, $(x,y)\to(-x,-y)$:

$$A''=(-3,-2)$$

**Check.** In every rotation about the origin, the distance from the origin does
not change: $OA=\sqrt{9+4}=\sqrt{13}$, $OA'=\sqrt{4+9}=\sqrt{13}$ ✓ and
$OA''=\sqrt{9+4}=\sqrt{13}$ ✓. That is the quickest test that a rotation has been
done correctly.
:::

```figure caption="Rotation of P(4, 2) about the origin O: through +90° (anticlockwise) it goes to P′(−2, 4); through −90° (clockwise) it goes to P″(2, −4). OP = OP′ = OP″ and each turn is a right angle."
fig, ax = plt.subplots(figsize=(4.2, 3.4))
from matplotlib.patches import Arc
P, P1, P2 = (4, 2), (-2, 4), (2, -4)
for Q, c in [(P, INK), (P1, ACCENT), (P2, SERIES[1])]:
    ax.plot([0, Q[0]], [0, Q[1]], color=c, lw=1.3); ax.plot(*Q, "o", color=c, ms=5)
ax.text(4.15, 2.15, "P(4, 2)", fontsize=8.5, color=INK)
ax.text(-3.9, 4.25, "P′(−2, 4)", fontsize=8.5, color=ACCENT)
ax.text(2.2, -4.3, "P″(2, −4)", fontsize=8.5, color=SERIES[1])
ax.add_patch(Arc((0, 0), 2.4, 2.4, theta1=26.6, theta2=116.6, color=ACCENT, lw=1.2))
ax.add_patch(Arc((0, 0), 1.6, 1.6, theta1=-63.4, theta2=26.6, color=SERIES[1], lw=1.2))
ax.text(-0.2, 1.45, "+90°", fontsize=8.5, color=ACCENT)
ax.text(0.95, -0.55, "−90°", fontsize=8.5, color=SERIES[1])
ax.axhline(0, color=MUTED, lw=0.8); ax.axvline(0, color=MUTED, lw=0.8)
ax.set_xlim(-4.5, 5.6); ax.set_ylim(-4.8, 4.8); ax.set_aspect("equal")
ax.set_xticks([-4, -2, 2, 4]); ax.set_yticks([-4, -2, 2, 4]); ax.tick_params(labelsize=7.5, length=0)
ax.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
for sp in ax.spines.values(): sp.set_visible(False)
```

::: example Rotating a triangle
**Problem.** The vertices of a triangle are $A(1,0)$, $B(3,0)$, $C(1,2)$. Rotate
it $90°$ anticlockwise about the origin and give the image.

**Solution.** Apply $(-y,x)$ to each vertex:

$$A'=(0,1),\quad B'=(0,3),\quad C'=(-2,1)$$

**Check.** $AB=2$ and $A'B'=3-1=2$ ✓; $AC=2$ and $A'C'=2$ ✓. The sides are
unchanged, and the right angle at $A$ is still a right angle at $A'$ ✓.
:::

::: caution Clockwise or anticlockwise?
A $90°$ clockwise rotation and a $270°$ anticlockwise rotation give the same
image, but a $90°$ **anticlockwise** rotation does not. Read the direction, and
check the sign of the result against the quadrant it should land in: starting
from $(3,2)$ in quadrant I and turning anticlockwise, the image must be in
quadrant II, so $(-2,3)$ is right and $(2,-3)$ would be wrong.
:::

## 19.4 Enlargement

An **enlargement** changes the size of a figure by a **scale factor** $k$ about a
**centre of enlargement**. The image is **similar** to the object, not congruent
(unless $k=1$).

For an enlargement with centre the origin and scale factor $k$:

$$(x,y)\longrightarrow(kx,\;ky)$$

| Scale factor | Effect |
|---|---|
| $k>1$ | the figure grows |
| $0<k<1$ | the figure shrinks |
| $k=1$ | the figure is unchanged |
| $k$ negative | the image is on the other side of the centre and inverted |

With a scale factor $k$:

- every length of the image $=k\times$ the corresponding length of the object;
- the area of the image $=k^2\times$ the area of the object.

```figure caption="An enlargement with scale factor 2 about the origin. Every coordinate is doubled, so every side is twice as long and the area is four times as large."
fig, ax = plt.subplots(figsize=(4.8, 2.9))
ax.set_xlim(-1, 8)
ax.set_ylim(-1, 6)
ax.axhline(0, color=INK, lw=0.9)
ax.axvline(0, color=INK, lw=0.9)
ax.grid(True, color=GRID, lw=0.5)
obj = [(1, 0.5), (2.5, 0.5), (1, 2)]
img = [(2 * x, 2 * y) for x, y in obj]
ax.add_patch(plt.Polygon(obj, fill=False, ec=ACCENT, lw=1.5))
ax.add_patch(plt.Polygon(img, fill=False, ec=SERIES[1], lw=1.5))
for (x, y), (u, v) in zip(obj, img):
    ax.plot([0, u], [0, v], color=GRID, lw=0.7, ls=":")
ax.text(1.35, 2.2, "object", fontsize=7, color=ACCENT)
ax.text(3.4, 4.0, "image, $k=2$", fontsize=7, color=SERIES[1])
ax.plot([0], [0], "o", color=INK, ms=3.5)
ax.text(0.1, -0.4, "$O$", fontsize=7.5, color=INK)
ax.set_xticks(range(0, 8, 2))
ax.set_yticks(range(0, 6, 2))
ax.tick_params(labelsize=7.5, length=0)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
```

::: example Enlarging a triangle
**Problem.** A triangle has vertices $A(1,1)$, $B(3,1)$, $C(1,2)$. Enlarge it
with centre the origin and scale factor 3. Find the image and the ratio of the
areas.

**Solution.** Multiply every coordinate by 3:

$$A'(3,3),\quad B'(9,3),\quad C'(3,6)$$

The object's area is $\frac12\times2\times1=1$ square unit, and the image's area
is $\frac12\times6\times3=9$ square units.

**Answer.** $A'(3,3)$, $B'(9,3)$, $C'(3,6)$; areas are in the ratio $1:9$, which
is $1^2:3^2$.

**Check.** $A'B'=6$ and $AB=2$, so the scale factor is 3 ✓, and the area ratio is
$3^2=9$ ✓.
:::

::: example A shrinking enlargement
**Problem.** Enlarge $P(4,6)$ with centre the origin and scale factor
$\frac12$.

**Solution.** $(4\times\frac12,\;6\times\frac12)=(2,3)$.

**Check.** The distance from the origin halves:
$OP=\sqrt{16+36}=\sqrt{52}$, and
$OP'=\sqrt{4+9}=\sqrt{13}=\frac{1}{2}\sqrt{52}$ ✓.
:::

::: caution Enlargement is not a translation
A translation moves a figure without changing its size; an enlargement changes
its size without moving its angles. A common error is to add the scale factor to
each coordinate instead of multiplying: from $A(2,3)$ with $k=3$ the image is
$(6,9)$, not $(5,6)$.
:::

## Chapter summary

- Translation slides a figure: $(x,y)\to(x+a,y+b)$; the image is congruent and
  faces the same way.
- Reflection flips it in a mirror line: in the $x$-axis $y$ changes sign, in the
  $y$-axis $x$ changes sign, in $y=x$ the coordinates swap.
- Rotation turns it about a centre: about the origin, $90°$ anticlockwise is
  $(-y,x)$, $180°$ is $(-x,-y)$ and $270°$ anticlockwise (or $90°$ clockwise) is
  $(y,-x)$.
- Enlargement multiplies every coordinate by the scale factor $k$; lengths
  become $k$ times and areas $k^2$ times as large.
- Translation, reflection and rotation give congruent images; enlargement gives
  a similar image.

## Practice questions

**Group A — Objective (1 mark each)**

1. A translation of 3 units right and 2 units up sends $(1,4)$ to
   <span class="marks">[1]</span>
   (a) $(4,6)$ (b) $(4,2)$ (c) $(-2,2)$ (d) $(3,6)$
2. Reflection in the $x$-axis sends $(2,5)$ to <span class="marks">[1]</span>
   (a) $(2,-5)$ (b) $(-2,5)$ (c) $(5,2)$ (d) $(-2,-5)$
3. Reflection in the $y$-axis sends $(3,-4)$ to
   <span class="marks">[1]</span>
   (a) $(-3,-4)$ (b) $(3,4)$ (c) $(-3,4)$ (d) $(4,-3)$
4. Rotation of $180°$ about the origin sends $(5,-2)$ to
   <span class="marks">[1]</span>
   (a) $(-5,2)$ (b) $(5,2)$ (c) $(2,-5)$ (d) $(-2,5)$
5. An enlargement with scale factor 4 makes the area
   <span class="marks">[1]</span>
   (a) 4 times (b) 8 times (c) 16 times (d) unchanged
6. Which transformation always gives a congruent image?
   <span class="marks">[1]</span>
   (a) translation (b) enlargement (c) both (d) neither

::: note Answers to Group A
**1.** (a) — add 3 to $x$ and 2 to $y$.
**2.** (a) — $y$ changes sign.
**3.** (a) — $x$ changes sign.
**4.** (a) — both coordinates change sign.
**5.** (c) — the area ratio is the square of the scale factor.
**6.** (a) — an enlargement changes the size unless $k=1$.
:::

**Group B — Short answer (2 marks each)**

1. Translate $A(-1,3)$ by 5 units right and 4 units down.
   <span class="marks">[2]</span>
2. Reflect $(4,-3)$ in the line $y=x$.
   <span class="marks">[2]</span>
3. Rotate $(2,5)$ through $90°$ anticlockwise about the origin.
   <span class="marks">[2]</span>
4. Enlarge $(3,4)$ with scale factor 2 about the origin and state the new
   distance from the origin. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $(-1+5,\;3-4)=(4,-1)$.
**2.** The coordinates swap: $(-3,4)$.
**3.** $(-y,x)=(-5,2)$.
**4.** $(6,8)$; the distance doubles from 5 to 10.
:::

**Group C — Long answer (4 marks each)**

1. A triangle has vertices $A(1,1)$, $B(4,1)$ and $C(1,3)$. (i) Reflect it in
   the $y$-axis and give the image. (ii) Find the area of both triangles and
   compare them. <span class="marks">[4]</span>
2. A square has vertices $(1,1)$, $(3,1)$, $(3,3)$ and $(1,3)$. Enlarge it with
   centre the origin and scale factor 3, give the image vertices, and find the
   ratio of the areas of the image and the object.
   <span class="marks">[4]</span>

::: note Answers to Group C
**1.** (i) Reflection in the $y$-axis changes the sign of $x$:
$A'(-1,1)$, $B'(-4,1)$, $C'(-1,3)$. (ii) The object has a horizontal side
$AB=3$ and a vertical side $AC=2$, so
$\text{area}=\frac12\times3\times2=3$ square units. The image has
$A'B'=3$ and $A'C'=2$, so its area is also 3 square units.
**Conclusion.** The areas are equal, which is what a reflection must give: it is
a rigid motion, so every length and every area is unchanged, even though the
figure faces the other way.
**2.** Multiply every coordinate by 3:
$$(3,3),\ (9,3),\ (9,9),\ (3,9)$$
The object is a square of side 2, so its area is 4 square units. The image is a
square of side 6, so its area is 36 square units.
$$\text{ratio}=4:36=1:9=1^2:3^2$$
**Check.** The side ratio is $6:2=3:1$, and the area ratio must be the square of
that, $9:1$ ✓.
:::

## Objective practice

**Choose the correct answer.** <span class="marks">[5×1=5]</span>

**1.** The image of $(5, -3)$ after reflection in the $x$-axis is
   (a) $(-5,-3)$ (b) $(5,3)$ (c) $(-5,3)$ (d) $(3,5)$
**2.** Translation by $\binom{-2}{3}$ maps $(4,1)$ to
   (a) $(2,4)$ (b) $(6,4)$ (c) $(2,-2)$ (d) $(-8,3)$
**3.** Rotation through $180°$ about the origin maps $(x,y)$ to
   (a) $(-x,y)$ (b) $(x,-y)$ (c) $(-x,-y)$ (d) $(y,x)$
**4.** Which transformation does **not** preserve size?
   (a) reflection (b) rotation (c) translation (d) enlargement
**5.** Reflection in the $y$-axis maps $(x,y)$ to
   (a) $(x,-y)$ (b) $(-x,y)$ (c) $(-x,-y)$ (d) $(y,x)$

::: note Objective practice — answers
**1.** (b) — the sign of $y$ changes. **2.** (a) — $(4-2,\,1+3)$. **3.** (c) — both signs change. **4.** (d) — an enlargement changes the size. **5.** (b) — the sign of $x$ changes.
:::
