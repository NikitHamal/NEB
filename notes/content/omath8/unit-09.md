---
subject: Optional Mathematics
grade: 8
unit: 9
title: Transformation
hours: 0
---

Look in a mirror and your right hand becomes a left hand. Turn a page of a book through a right angle and every word on it turns too. Slide a chessboard piece three squares forward and it lands, unchanged, in a new place. Each of these is a **transformation**: a rule that sends every point of a figure to a new position. In grade 8 compulsory mathematics you drew reflections, rotations and translations. In optional mathematics we study them with coordinates and rules: we prove why the rules work, separate the transformations that keep size and shape from those that do not, find the object when only the image is known, and combine two transformations into one. These ideas lead on to transformations by matrices in grade 10, and they are the mathematics behind the "flip", "rotate" and "move" tools in every drawing and photo app.

::: key What your examination asks from this chapter
Expect: (i) the meaning of **transformation**, object and image, and the difference between **isometric** and **non-isometric** transformations, with examples; (ii) the image of a point or a triangle under **reflection** in the $x$-axis or the $y$-axis; (iii) the image under **rotation** about the origin through $\pm90^\circ$, $180^\circ$, $270^\circ$ or $360^\circ$, or the angle and direction of a rotation from a point and its image; (iv) the image under **translation** by a vector, or the vector from a point and its image; (v) finding the **object** from the image; (vi) a 4-mark question that draws a triangle and its image on graph paper, often with two transformations one after the other. Plot every figure: the graph earns marks and catches sign mistakes.
:::

## 9.1 Transformation: meaning; isometric and non-isometric transformations

::: definition Transformation, object and image
A **transformation** is a rule that changes the position (and sometimes the size or shape) of a figure by moving **every point** of it to a new point. The original figure is the **object** and the new figure is the **image**. If a point $P$ is sent to $P'$, we write $P\rightarrow P'$ and read "$P$ maps to $P$ dash".
:::

An object triangle $ABC$ has the image triangle $A'B'C'$: each vertex goes to the vertex with the same letter. Because a transformation acts on every point, it is enough to transform the vertices of a polygon and join the images in the same order.

Transformations are easy to find around you. The two halves of a butterfly, or of the eyes painted on the stupa at Swayambhunath, are reflections of each other in a vertical line. The pattern on a *dhaka topi* or a mandala repeats when it is turned about its centre, a rotation. A row of identical carved windows on a Newar house, or the bricks in a wall, repeat by sliding along, a translation. A photocopy at 150% is an enlargement. Artists and engineers use exactly these four moves to build patterns.

### Isometric and non-isometric transformations

The word **isometric** comes from Greek *isos*, equal, and *metron*, measure.

::: definition Isometric and non-isometric transformations
A transformation is **isometric** if it keeps the **distance between every pair of points** unchanged. Then lengths, angles, area, shape and size are all unchanged, and the image is **congruent** to the object. Reflection, rotation and translation are isometric.

A transformation that changes distances is **non-isometric**. An **enlargement** with scale factor other than 1 or $-1$ is non-isometric: the image is **similar** to the object (same shape) but of a different size.
:::

```figure caption="One object (the grey flag) under four transformations. Reflection, rotation and translation give a congruent image, so they are isometric. Enlargement with scale factor 2 about $O$ doubles every length, so it is non-isometric: the image is similar, not congruent."
fig, axs = plt.subplots(2, 2, figsize=(5.0, 4.2))
flag = np.array([[1, 1], [1, 4], [3, 3.5], [1, 3], [1, 1]], dtype=float)
imgs = [(flag*np.array([-1, 1]), 'reflection in y-axis : isometric', SERIES[2]),
        (np.column_stack([-flag[:, 1], flag[:, 0]]), 'rotation +90° about O : isometric', SERIES[2]),
        (flag + np.array([3, -4]), 'translation by (3, −4) : isometric', SERIES[2]),
        (flag*2, 'enlargement ×2 about O : non-isometric', SERIES[1])]
for ax, (im, title, c) in zip(axs.flat, imgs):
    ax.fill(flag[:, 0], flag[:, 1], color='#d9dde3'); ax.plot(flag[:, 0], flag[:, 1], color=MUTED, lw=1.2)
    ax.fill(im[:, 0], im[:, 1], color=c, alpha=0.25); ax.plot(im[:, 0], im[:, 1], color=c, lw=1.5)
    ax.axhline(0, color=INK, lw=0.8); ax.axvline(0, color=INK, lw=0.8)
    lim = 8.5 if 'enlargement' in title else (7 if 'translation' in title else 5)
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_aspect('equal')
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_title(title, fontsize=8, color=c, pad=2)
fig.tight_layout(pad=0.4)
```

| Transformation | Lengths | Angles | Orientation (order of labels round the figure) | Image |
|---|---|---|---|---|
| Reflection | unchanged | unchanged | **reversed** (clockwise becomes anticlockwise) | congruent |
| Rotation | unchanged | unchanged | kept | congruent |
| Translation | unchanged | unchanged | kept | congruent |
| Enlargement ($k\neq\pm1$) | multiplied by $k$ | unchanged | kept for $k>0$ | similar |

A point that a transformation does not move is an **invariant point**. In a reflection every point of the mirror line is invariant; in a rotation only the centre is invariant; a translation (other than by the null vector) has no invariant point at all.

::: example Isometric or not?
**Problem.** The triangle $A(1,1)$, $B(3,1)$, $C(1,2)$ has two images: $P(-1,1)$, $Q(-3,1)$, $R(-1,2)$, and $X(2,2)$, $Y(6,2)$, $Z(2,4)$. Which image comes from an isometric transformation?

**Solution.** Compare the lengths of corresponding sides.

Object: $AB=3-1=2$, $AC=2-1=1$. First image: $PQ=|-3-(-1)|=2$, $PR=1$. Second image: $XY=6-2=4$, $XZ=4-2=2$.

The first image keeps every length, so it comes from an **isometric** transformation (each $x$ has changed sign: a reflection in the $y$-axis). The second doubles every length, so it is **non-isometric** (an enlargement with scale factor 2 about the origin). Its area is $\frac{1}{2}\times4\times2=4$ square units, four times the object's area of 1.
:::

## 9.2 Reflection in the x-axis and the y-axis

A **reflection** flips a figure over a straight line called the **mirror line** (or axis of reflection), as a mirror does. For every point $P$ and its image $P'$:

- $P$ and $P'$ are the **same distance** from the mirror line, on opposite sides;
- the segment $PP'$ is **perpendicular** to the mirror line, and the mirror line **bisects** it.

In other words, the mirror line is the perpendicular bisector of $PP'$.

### Reflection in the x-axis

If $P(x,y)$ is reflected in the $x$-axis, it stays at the same horizontal position but goes to the other side of the axis, the same distance away. So the $x$-coordinate is unchanged and the $y$-coordinate changes sign:
$$ P(x,y)\ \longrightarrow\ P'(x,-y) \qquad \text{(reflection in the } x\text{-axis)} $$

### Reflection in the y-axis

Reflecting in the $y$-axis keeps the height and changes the side, so the $x$-coordinate changes sign:
$$ P(x,y)\ \longrightarrow\ P'(-x,y) \qquad \text{(reflection in the } y\text{-axis)} $$

```figure caption="Triangle $ABC$ with $A(2,1)$, $B(5,2)$, $C(3,4)$ and its images: $A'B'C'$ after reflection in the $x$-axis (the sign of $y$ changes) and $A''B''C''$ after reflection in the $y$-axis (the sign of $x$ changes). Dotted lines join $C$ to its images; each crosses the mirror line at right angles and is bisected by it."
fig, ax = plt.subplots(figsize=(4.8, 3.8))
T = np.array([[2, 1], [5, 2], [3, 4]], dtype=float)
for M, c, names in [(np.array([1, 1]), ACCENT, ['A', 'B', 'C']), (np.array([1, -1]), SERIES[1], ["A'", "B'", "C'"]), (np.array([-1, 1]), SERIES[2], ['A″', 'B″', 'C″'])]:
    P = T*M
    Q = np.vstack([P, P[:1]])
    ax.fill(Q[:, 0], Q[:, 1], color=c, alpha=0.15); ax.plot(Q[:, 0], Q[:, 1], color=c, lw=1.5)
    G = P.mean(axis=0)
    for (x, y), n in zip(P, names):
        ax.plot(x, y, 'o', color=c, ms=3.5)
        u = np.array([x, y]) - G; u = u/np.linalg.norm(u)
        ax.text(x + 0.5*u[0], y + 0.5*u[1], n, fontsize=8.5, color=c, ha='center', va='center')
ax.plot([3, 3], [4, -4], color=MUTED, lw=0.9, ls=':'); ax.plot([3, -3], [4, 4], color=MUTED, lw=0.9, ls=':')
ax.axhline(0, color=INK, lw=1.0); ax.axvline(0, color=INK, lw=1.0)
ax.set_xlim(-6.2, 6.2); ax.set_ylim(-5, 5); ax.set_aspect('equal')
ax.set_xticks(range(-6, 7, 2)); ax.set_yticks(range(-4, 5, 2)); ax.tick_params(labelsize=7.5, length=0)
ax.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
for s in ax.spines.values(): s.set_visible(False)
fig.tight_layout(pad=0.3)
```

### Why reflection keeps distances

Take any two points $A(x_1,y_1)$ and $B(x_2,y_2)$. Their images in the $x$-axis are $A'(x_1,-y_1)$ and $B'(x_2,-y_2)$. By the distance formula,
$$ A'B'^2=(x_2-x_1)^2+(-y_2+y_1)^2=(x_2-x_1)^2+(y_2-y_1)^2=AB^2 $$
because $(-y_2+y_1)^2=(y_2-y_1)^2$. So $A'B'=AB$ for **every** pair of points: reflection in the $x$-axis is isometric. The same argument, with the signs of the $x$-coordinates changed instead, works for the $y$-axis. In the same way, a rotation through $+90^\circ$ sends $A$ and $B$ to $(-y_1,x_1)$ and $(-y_2,x_2)$, and the squared distance between these is $(y_2-y_1)^2+(x_2-x_1)^2$, again $AB^2$.

::: example Reflecting a triangle in both axes
**Problem.** Find the images of the triangle $A(2,1)$, $B(5,2)$, $C(3,4)$ after reflection (i) in the $x$-axis, (ii) in the $y$-axis. Show that $AB=A'B'$.

**Solution.** (i) Change the sign of $y$: $A'(2,-1)$, $B'(5,-2)$, $C'(3,-4)$.

(ii) Change the sign of $x$: $A''(-2,1)$, $B''(-5,2)$, $C''(-3,4)$.

$AB=\sqrt{(5-2)^2+(2-1)^2}=\sqrt{10}$ and $A'B'=\sqrt{(5-2)^2+(-2+1)^2}=\sqrt{10}$, so $AB=A'B'$, as an isometric transformation requires. The figure above shows all three triangles. Notice that $A$, $B$, $C$ run anticlockwise, while $A'$, $B'$, $C'$ run clockwise: a reflection reverses orientation.
:::

::: example Finding the object from the image
**Problem.** (i) After reflection in the $x$-axis, the image of a point is $(-3,4)$. Find the point. (ii) Which of the points $(4,0)$, $(0,4)$, $(4,4)$ is unchanged by reflection in the $x$-axis?

**Solution.** (i) Reflecting twice in the same mirror brings a point back, so reflect the image: the object is $(-3,-4)$. Check: $(-3,-4)\rightarrow(-3,4)$ ✓.

(ii) $(4,0)\rightarrow(4,-0)=(4,0)$: it lies **on** the mirror line, so it is invariant. The other two move to $(0,-4)$ and $(4,-4)$.
:::

::: example One reflection after another
**Problem.** The point $P(3,5)$ is reflected in the $x$-axis to $P_1$, and $P_1$ is reflected in the $y$-axis to $P_2$. Find $P_1$ and $P_2$, and describe the single transformation from $P$ to $P_2$.

**Solution.** $P_1=(3,-5)$ and $P_2=(-3,-5)$. Both coordinates have changed sign: $(x,y)\rightarrow(-x,-y)$. This is the rule for a **rotation through $180^\circ$** about the origin (section 9.3). Two reflections in perpendicular lines make a half turn, and the orientation, reversed twice, is back to the original.
:::

::: caution Which coordinate changes sign?
Reflection in the $x$-axis changes the **$y$**-coordinate, not the $x$-coordinate. It is easy to mix up. Think of the $x$-axis as a horizontal mirror on the floor: your image is below you (the height changes), while your position along the floor stays the same.
:::

## 9.3 Rotation about the origin through 90°, 180°, 270° and 360°

A **rotation** turns a figure about a fixed point, the **centre of rotation**, through a given **angle** in a given **direction**. Anticlockwise rotation is taken as **positive** and clockwise rotation as **negative**. Every point stays the same distance from the centre, so a rotation is isometric. In this chapter the centre is always the origin $O$.

### Why the rule for +90° works

```figure caption="Rotating $P(x,y)$ through $+90^\circ$ about $O$. The right triangle $OMP$, with legs $x$ along the $x$-axis and $y$ upwards, turns into the congruent triangle $OM'P'$, with leg $x$ along the $y$-axis and leg $y$ to the left. So $P'$ is the point $(-y,x)$."
from matplotlib.patches import Arc
fig, ax = plt.subplots(figsize=(4.6, 3.4))
P, M = np.array([4.0, 2.0]), np.array([4.0, 0.0])
P1, M1 = np.array([-2.0, 4.0]), np.array([0.0, 4.0])
ax.fill([0, M[0], P[0]], [0, M[1], P[1]], color='#cfe3f6'); ax.plot([0, M[0], P[0], 0], [0, M[1], P[1], 0], color=ACCENT, lw=1.5)
ax.fill([0, M1[0], P1[0]], [0, M1[1], P1[1]], color='#d5efdf'); ax.plot([0, M1[0], P1[0], 0], [0, M1[1], P1[1], 0], color=SERIES[2], lw=1.5)
ax.add_patch(Arc((0, 0), 2.4, 2.4, theta1=np.degrees(np.arctan2(2, 4)), theta2=np.degrees(np.arctan2(4, -2)), color=SERIES[1], lw=1.3))
ax.text(-0.55, 1.35, '90°', fontsize=9, color=SERIES[1])
ax.text(4.15, 2.05, 'P(x, y)', fontsize=9, color=ACCENT); ax.text(-2.15, 4.15, "P'(−y, x)", fontsize=9, color=SERIES[2], ha='right')
ax.text(2.0, -0.4, 'x', ha='center', fontsize=9, color=ACCENT); ax.text(4.15, 1.0, 'y', fontsize=9, color=ACCENT)
ax.text(0.15, 2.0, 'x', fontsize=9, color=SERIES[2]); ax.text(-1.0, 4.2, 'y', ha='center', fontsize=9, color=SERIES[2])
ax.text(4.0, -0.4, 'M', ha='center', fontsize=8.5); ax.text(0.15, 4.15, "M'", fontsize=8.5)
ax.text(-0.3, -0.4, 'O', fontsize=8.5)
ax.axhline(0, color=INK, lw=0.9); ax.axvline(0, color=INK, lw=0.9)
ax.set_xlim(-4.0, 5.6); ax.set_ylim(-1.0, 5.0); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

Take $P(x,y)$ in the first quadrant and drop the perpendicular $PM$ to the $x$-axis, so $OM=x$ and $MP=y$. A quarter turn anticlockwise sends the $x$-axis onto the $y$-axis, so $M$ goes to $M'(0,x)$, and the segment $MP$, which pointed up, now points to the **left**. So $P$ goes to the point $y$ units to the left of $M'$, which is $P'(-y,x)$. Turning through $+90^\circ$ twice gives $(x,y)\rightarrow(-y,x)\rightarrow(-x,-y)$, the rule for $180^\circ$; three times gives $(y,-x)$, the rule for $270^\circ$; and four times brings the point back.

::: key Rules for rotation about the origin
| Rotation about $O$ | Image of $P(x,y)$ | Same as |
|---|---|---|
| $+90^\circ$ (anticlockwise) | $(-y,\ x)$ | $-270^\circ$ |
| $180^\circ$ (either direction) | $(-x,\ -y)$ | $-180^\circ$ |
| $+270^\circ$ (anticlockwise) | $(y,\ -x)$ | $-90^\circ$ (clockwise) |
| $360^\circ$ | $(x,\ y)$ | no change |
:::

::: example Rotating a point through every angle
**Problem.** Find the image of $P(4,2)$ under rotation about the origin through (i) $+90^\circ$ (ii) $180^\circ$ (iii) $+270^\circ$ (iv) $-90^\circ$ (v) $360^\circ$. Check that $OP$ does not change.

**Solution.** (i) $(-y,x)=(-2,4)$. (ii) $(-x,-y)=(-4,-2)$. (iii) $(y,-x)=(2,-4)$. (iv) $-90^\circ$ is the same as $+270^\circ$: $(2,-4)$. (v) $(4,2)$.

$OP=\sqrt{16+4}=\sqrt{20}$, and every image, such as $(-2,4)$ or $(2,-4)$, is also $\sqrt{4+16}=\sqrt{20}$ from $O$ ✓.
:::

```figure caption="The triangle $A(1,2)$, $B(4,1)$, $C(3,4)$ rotated about $O$ through $+90^\circ$ (into quadrant II), $180^\circ$ (quadrant III) and $+270^\circ$ (quadrant IV). Every image is congruent to the object and each vertex stays the same distance from $O$."
fig, ax = plt.subplots(figsize=(4.6, 4.0))
T = np.array([[1, 2], [4, 1], [3, 4]], dtype=float)
rots = [(T, ACCENT, 'object', (2.6, 4.4)), (np.column_stack([-T[:, 1], T[:, 0]]), SERIES[2], '+90°', (-4.9, 4.3)),
        (-T, SERIES[1], '180°', (-4.9, -4.6)), (np.column_stack([T[:, 1], -T[:, 0]]), SERIES[3], '+270°', (3.4, -4.6))]
for P, c, lab, pos in rots:
    Q = np.vstack([P, P[:1]])
    ax.fill(Q[:, 0], Q[:, 1], color=c, alpha=0.18); ax.plot(Q[:, 0], Q[:, 1], color=c, lw=1.5)
    ax.text(pos[0], pos[1], lab, fontsize=9, color=c)
ax.plot(0, 0, 'o', color=INK, ms=4); ax.text(0.2, -0.55, 'O', fontsize=8.5)
ax.axhline(0, color=INK, lw=0.9); ax.axvline(0, color=INK, lw=0.9)
ax.set_xlim(-5.4, 5.4); ax.set_ylim(-5.2, 5.2); ax.set_aspect('equal')
ax.set_xticks(range(-4, 5, 2)); ax.set_yticks(range(-4, 5, 2)); ax.tick_params(labelsize=7.5, length=0)
ax.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
for s in ax.spines.values(): s.set_visible(False)
fig.tight_layout(pad=0.3)
```

::: example Rotating a triangle
**Problem.** Rotate the triangle $A(1,2)$, $B(4,1)$, $C(3,4)$ about the origin through $+90^\circ$, $180^\circ$ and $-90^\circ$.

**Solution.**

| Vertex | $+90^\circ$: $(-y,x)$ | $180^\circ$: $(-x,-y)$ | $-90^\circ$: $(y,-x)$ |
|---|---|---|---|
| $A(1,2)$ | $(-2,1)$ | $(-1,-2)$ | $(2,-1)$ |
| $B(4,1)$ | $(-1,4)$ | $(-4,-1)$ | $(1,-4)$ |
| $C(3,4)$ | $(-4,3)$ | $(-3,-4)$ | $(4,-3)$ |

The figure above shows the three images. Check: $OA=\sqrt{1+4}=\sqrt{5}$ and the image $(-2,1)$ is also $\sqrt{4+1}=\sqrt{5}$ from $O$ ✓.
:::

::: example Finding the angle of rotation
**Problem.** Find the angle and direction of the rotation about $O$ that maps (i) $P(3,-2)$ to $(-3,2)$; (ii) $Q(2,5)$ to $(5,-2)$; (iii) $R(5,-1)$ to $(1,5)$.

**Solution.** Compare the image with each rule.

(i) Both signs changed: $(-x,-y)$, a rotation through $180^\circ$.

(ii) $(5,-2)=(y,-x)$ for $Q(2,5)$: a rotation through $+270^\circ$, i.e. $90^\circ$ clockwise.

(iii) For $R(5,-1)$, $(-y,x)=(1,5)$: a rotation through $+90^\circ$ (anticlockwise).
:::

::: caution Do not mix up the 90° rules
$+90^\circ$ gives $(-y,x)$ and $-90^\circ$ gives $(y,-x)$: in both the coordinates **swap**, but the minus sign goes in different places. Check the quadrant: turning $(4,2)$ in quadrant I anticlockwise by a quarter turn must land in quadrant II, where $x$ is negative and $y$ positive, so $(-2,4)$ is right and $(2,-4)$ is wrong.
:::

## 9.4 Translation by a vector

A **translation** slides every point of a figure the **same distance in the same direction**. Nothing turns and nothing flips, so a translation is isometric and keeps orientation. A translation is described by a vector $T=\binom{a}{b}$: move $a$ units horizontally (right if $a>0$, left if $a<0$) and $b$ units vertically (up if $b>0$, down if $b<0$).
$$ P(x,y)\ \longrightarrow\ P'(x+a,\ y+b) \qquad \text{(translation by } \binom{a}{b}\text{)} $$
The vector $\overrightarrow{PP'}$ is the same, $\binom{a}{b}$, for every point of the figure. This is why a translation is the transformation most closely tied to vectors.

```figure caption="The triangle $A(1,1)$, $B(4,2)$, $C(2,4)$ translated by $T=\binom{3}{-2}$ to $A'(4,-1)$, $B'(7,0)$, $C'(5,2)$. The three arrows $\overrightarrow{AA'}$, $\overrightarrow{BB'}$, $\overrightarrow{CC'}$ are equal vectors, and each side of the image is parallel and equal to the matching side of the object."
fig, ax = plt.subplots(figsize=(4.6, 3.3))
T = np.array([[1, 1], [4, 2], [2, 4]], dtype=float); v = np.array([3, -2])
for P, c, names in [(T, ACCENT, ['A', 'B', 'C']), (T + v, SERIES[1], ["A'", "B'", "C'"])]:
    Q = np.vstack([P, P[:1]])
    ax.fill(Q[:, 0], Q[:, 1], color=c, alpha=0.15); ax.plot(Q[:, 0], Q[:, 1], color=c, lw=1.5)
    G = P.mean(axis=0)
    for (x, y), n in zip(P, names):
        u = np.array([x, y]) - G; u = u/np.linalg.norm(u)
        ax.text(x + 0.42*u[0], y + 0.42*u[1], n, fontsize=9, color=c, ha='center', va='center')
for p in T:
    ax.annotate('', xy=p + v, xytext=p, arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.0, ls='--'))
ax.text(6.0, 3.6, 'T = (3, −2)', fontsize=9, color=MUTED)
ax.axhline(0, color=INK, lw=0.9); ax.axvline(0, color=INK, lw=0.9)
ax.set_xlim(-0.8, 8.2); ax.set_ylim(-2.0, 4.8); ax.set_aspect('equal')
ax.set_xticks(range(0, 9, 2)); ax.set_yticks(range(-2, 5, 2)); ax.tick_params(labelsize=7.5, length=0)
ax.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
for s in ax.spines.values(): s.set_visible(False)
fig.tight_layout(pad=0.3)
```

::: example Translating a triangle
**Problem.** Translate the triangle $A(1,1)$, $B(4,2)$, $C(2,4)$ by $T=\binom{3}{-2}$, and show that $AB$ and $A'B'$ are equal and parallel.

**Solution.** Add 3 to every $x$ and $-2$ to every $y$: $A'(4,-1)$, $B'(7,0)$, $C'(5,2)$.

$\overrightarrow{AB}=\binom{3}{1}$ and $\overrightarrow{A'B'}=\binom{7-4}{0+1}=\binom{3}{1}$. The vectors are equal, so $AB$ and $A'B'$ are equal in length and parallel.
:::

::: example Finding the translation vector, then using it
**Problem.** A translation maps $P(2,-1)$ to $P'(5,3)$. Find the translation vector and the image of $Q(-1,2)$ under the same translation.

**Solution.** $T=\overrightarrow{PP'}=\binom{5-2}{3+1}=\binom{3}{4}$. Then $Q'=(-1+3,\ 2+4)=(2,6)$.
:::

::: example Object from image, and two translations
**Problem.** (i) The image of a point under translation by $\binom{-2}{5}$ is $(4,-3)$. Find the point. (ii) A figure is translated by $\binom{2}{1}$ and then by $\binom{-5}{3}$. Find the single translation that does the same job, and the translation that brings the figure back.

**Solution.** (i) Undo the translation by subtracting the vector: $(4+2,\ -3-5)=(6,-8)$. Check: $(6-2,\ -8+5)=(4,-3)$ ✓.

(ii) Two slides add like vectors: $\binom{2}{1}+\binom{-5}{3}=\binom{-3}{4}$. The translation back is the negative vector $\binom{3}{-4}$.
:::

### Undoing a transformation

To find an **object** when its **image** is known, apply the **inverse** transformation, the one that undoes the first.

| Transformation | Its inverse |
|---|---|
| Reflection in the $x$-axis (or the $y$-axis) | the same reflection: reflecting twice gives back the object |
| Rotation through $+90^\circ$ about $O$ | rotation through $-90^\circ$ (that is, $+270^\circ$) |
| Rotation through $180^\circ$ about $O$ | the same rotation |
| Translation by $\binom{a}{b}$ | translation by $\binom{-a}{-b}$ |

For example, if a rotation through $+90^\circ$ about $O$ gives the image $(-1,6)$, the object is found with the $-90^\circ$ rule $(y,-x)$: it is $(6,1)$. Check: $(6,1)\rightarrow(-1,6)$ under $(-y,x)$ ✓.

### All the rules together

| Transformation | Image of $P(x,y)$ | Isometric? |
|---|---|---|
| Reflection in the $x$-axis | $(x,-y)$ | yes |
| Reflection in the $y$-axis | $(-x,y)$ | yes |
| Rotation $+90^\circ$ about $O$ | $(-y,x)$ | yes |
| Rotation $180^\circ$ about $O$ | $(-x,-y)$ | yes |
| Rotation $+270^\circ$ ($=-90^\circ$) about $O$ | $(y,-x)$ | yes |
| Rotation $360^\circ$ about $O$ | $(x,y)$ | yes |
| Translation by $\binom{a}{b}$ | $(x+a,\ y+b)$ | yes |
| Enlargement, scale factor $k$, centre $O$ | $(kx,\ ky)$ | no, unless $k=\pm1$ |

::: example A chain of transformations
**Problem.** The point $P(3,2)$ is reflected in the $y$-axis to $P_1$; $P_1$ is rotated through $+90^\circ$ about $O$ to $P_2$; and $P_2$ is translated by $\binom{1}{-4}$ to $P_3$. Find $P_1$, $P_2$, $P_3$ and the distance $PP_3$.

**Solution.** $P_1=(-3,2)$. $P_2$: apply $(-y,x)$ to $(-3,2)$, giving $(-2,-3)$. $P_3=(-2+1,\ -3-4)=(-1,-7)$.
$$ PP_3=\sqrt{(3+1)^2+(2+7)^2}=\sqrt{16+81}=\sqrt{97}\approx9.85 \text{ units} $$
The order matters: doing the same three steps in a different order generally ends at a different point.
:::

::: tip Plot, then check one vertex
In a graph question, write the rule at the top, transform each vertex in a small table, plot the image with the dashed labels $A'$, $B'$, $C'$, and finally check one vertex by eye: is it the right distance from the mirror, the right quarter turn, the right slide? A single wrong sign shows up immediately on the graph.
:::

::: note Activity — the transformation game
Work in pairs on graph paper. Player 1 draws a scalene triangle in the first quadrant and secretly chooses one transformation from this chapter (a reflection in an axis, a rotation about $O$, or a translation). Player 1 draws only the image. Player 2 must name the transformation exactly (for example "rotation through $-90^\circ$ about $O$" or "translation by $\binom{-4}{1}$") and justify it from the coordinates. Swap roles. After four rounds, try a chain of two transformations and see whether your partner can find a single transformation that does the same job.
:::

## Chapter summary

- A **transformation** maps every point $P$ of an object to a point $P'$ of the image.
- **Isometric** transformations keep all lengths: reflection, rotation and translation give **congruent** images. **Non-isometric** ones, such as enlargement, change lengths and give similar images.
- Reflection reverses orientation; rotation and translation keep it. Points on the mirror line, and the centre of a rotation, are invariant.
- Reflection in the $x$-axis: $(x,y)\rightarrow(x,-y)$; in the $y$-axis: $(x,y)\rightarrow(-x,y)$. Two reflections, one in each axis, make a rotation of $180^\circ$.
- Rotation about $O$: $+90^\circ\rightarrow(-y,x)$, $180^\circ\rightarrow(-x,-y)$, $+270^\circ$ (or $-90^\circ$) $\rightarrow(y,-x)$, $360^\circ\rightarrow(x,y)$; distances from $O$ are unchanged.
- Translation by $\binom{a}{b}$: $(x,y)\rightarrow(x+a,y+b)$; the vector $\overrightarrow{PP'}$ is the same for every point; two translations add as vectors.
- To find an object from its image, apply the reverse transformation.

## Practice questions

**Group A — Objective (1 mark each)**

1. Which of these transformations is non-isometric? <span class="marks">[1]</span>
   (a) reflection (b) rotation (c) translation (d) enlargement
2. The image of $(3,-5)$ after reflection in the $x$-axis is <span class="marks">[1]</span>
   (a) $(3,5)$ (b) $(-3,-5)$ (c) $(-3,5)$ (d) $(-5,3)$
3. The image of $(-2,7)$ after reflection in the $y$-axis is <span class="marks">[1]</span>
   (a) $(2,7)$ (b) $(-2,-7)$ (c) $(2,-7)$ (d) $(7,-2)$
4. Under a rotation of $+90^\circ$ about the origin, $(x,y)$ maps to <span class="marks">[1]</span>
   (a) $(y,-x)$ (b) $(-y,x)$ (c) $(-x,-y)$ (d) $(y,x)$
5. The image of $(4,1)$ under rotation through $180^\circ$ about the origin is <span class="marks">[1]</span>
   (a) $(-4,-1)$ (b) $(1,4)$ (c) $(-1,4)$ (d) $(4,-1)$
6. A rotation of $270^\circ$ anticlockwise is the same as a rotation of <span class="marks">[1]</span>
   (a) $90^\circ$ anticlockwise (b) $90^\circ$ clockwise (c) $180^\circ$ (d) $360^\circ$
7. The image of $(2,3)$ under rotation through $360^\circ$ about the origin is <span class="marks">[1]</span>
   (a) $(-2,-3)$ (b) $(3,2)$ (c) $(2,3)$ (d) $(-3,2)$
8. Translation by $\binom{2}{-3}$ maps $(1,4)$ to <span class="marks">[1]</span>
   (a) $(3,1)$ (b) $(-1,7)$ (c) $(3,7)$ (d) $(2,-12)$
9. If $P(2,5)$ is translated to $P'(6,3)$, the translation vector is <span class="marks">[1]</span>
   (a) $\binom{4}{-2}$ (b) $\binom{-4}{2}$ (c) $\binom{8}{8}$ (d) $\binom{4}{2}$
10. Which point is unchanged by reflection in the $x$-axis? <span class="marks">[1]</span>
    (a) $(0,3)$ (b) $(3,0)$ (c) $(3,3)$ (d) $(-3,3)$
11. Reflection in the $x$-axis followed by reflection in the $y$-axis is the same as <span class="marks">[1]</span>
    (a) rotation through $90^\circ$ (b) rotation through $180^\circ$ (c) a translation (d) reflection in the $x$-axis
12. Under an isometric transformation the image is always <span class="marks">[1]</span>
    (a) larger than the object (b) smaller than the object (c) congruent to the object (d) a single point

::: note Answers to Group A
**1.** (d) — enlargement changes lengths.
**2.** (a) — the sign of $y$ changes.
**3.** (a) — the sign of $x$ changes.
**4.** (b) — the coordinates swap and the new $x$ is negative.
**5.** (a) — both signs change.
**6.** (b) — $270^\circ$ anticlockwise leaves the figure where $90^\circ$ clockwise would.
**7.** (c) — a full turn changes nothing.
**8.** (a) — $(1+2,\ 4-3)$.
**9.** (a) — $\binom{6-2}{3-5}$.
**10.** (b) — it lies on the mirror line.
**11.** (b) — $(x,y)\rightarrow(x,-y)\rightarrow(-x,-y)$.
**12.** (c) — distances are kept, so shape and size are kept.
:::

**Group B — Short answer (2 marks each)**

1. Define isometric and non-isometric transformations, with one example of each. <span class="marks">[2]</span>
2. Find the image of the triangle $A(1,2)$, $B(3,5)$, $C(4,1)$ after reflection in the $x$-axis. <span class="marks">[2]</span>
3. After reflection in the $y$-axis, the image of a point is $(-4,6)$. Find the point. <span class="marks">[2]</span>
4. Find the image of $P(-3,2)$ under rotation about the origin through $+90^\circ$ and through $-90^\circ$. <span class="marks">[2]</span>
5. A rotation about the origin maps $P(5,-1)$ to $P'(1,5)$. Find the angle and direction of the rotation. <span class="marks">[2]</span>
6. Find the image of $(2,-3)$ under translation by $\binom{-4}{6}$. <span class="marks">[2]</span>
7. Find the translation vector that maps $A(3,1)$ to $A'(-1,4)$. <span class="marks">[2]</span>
8. Find the image of $(-2,-5)$ under rotation through $180^\circ$ about the origin, and show that the same image comes from reflection in the $x$-axis followed by reflection in the $y$-axis. <span class="marks">[2]</span>
9. A translation maps $(1,2)$ to $(4,-1)$. Find the image of $(-3,5)$ under the same translation. <span class="marks">[2]</span>
10. Show that reflection in the $y$-axis keeps the length of $AB$, where $A(1,3)$ and $B(4,7)$. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** An isometric transformation keeps the distance between every two points, so the image is congruent to the object; example: rotation. A non-isometric transformation changes distances, so the image differs in size; example: enlargement with scale factor 2.
**2.** $(x,y)\rightarrow(x,-y)$: $A'(1,-2)$, $B'(3,-5)$, $C'(4,-1)$.
**3.** Reflect the image back in the $y$-axis: the point is $(4,6)$.
**4.** $+90^\circ$: $(-y,x)=(-2,-3)$. $-90^\circ$: $(y,-x)=(2,3)$.
**5.** For $P(5,-1)$, $(-y,x)=(1,5)$, which is the image. So it is a rotation through $+90^\circ$, anticlockwise.
**6.** $(2-4,\ -3+6)=(-2,3)$.
**7.** $\binom{-1-3}{4-1}=\binom{-4}{3}$.
**8.** $180^\circ$: $(2,5)$. In the $x$-axis: $(-2,5)$; then in the $y$-axis: $(2,5)$. The same image.
**9.** $T=\binom{3}{-3}$, so $(-3+3,\ 5-3)=(0,2)$.
**10.** $AB=\sqrt{9+16}=5$. The images are $A'(-1,3)$ and $B'(-4,7)$, and $A'B'=\sqrt{(-4+1)^2+(7-3)^2}=\sqrt{9+16}=5$. The length is unchanged.
:::

**Group C — Long answer (4 marks each)**

1. The triangle $ABC$ has vertices $A(2,1)$, $B(5,2)$ and $C(3,4)$. (i) Find its image after reflection in the $x$-axis. (ii) Find its image after reflection in the $y$-axis. (iii) Draw all three triangles on one graph. (iv) Show that $AB=A'B'$. <span class="marks">[4]</span>
2. Rotate the triangle $P(1,2)$, $Q(4,1)$, $R(3,4)$ about the origin through (i) $+90^\circ$ (ii) $180^\circ$ (iii) $-90^\circ$. Write the images and verify that $OP=OP'$ for the rotation in (i). <span class="marks">[4]</span>
3. The triangle $A(1,1)$, $B(4,2)$, $C(2,4)$ is translated by $\binom{3}{-2}$. (i) Find the image. (ii) Plot both triangles. (iii) Show that $AB$ and $A'B'$ are equal and parallel. (iv) Which single translation brings the image back to the object? <span class="marks">[4]</span>
4. The point $P(3,2)$ is reflected in the $y$-axis to $P_1$; $P_1$ is rotated through $+90^\circ$ about the origin to $P_2$; $P_2$ is translated by $\binom{1}{-4}$ to $P_3$. Find $P_1$, $P_2$, $P_3$ and the distance $PP_3$. <span class="marks">[4]</span>
5. A triangle with vertices $(1,1)$, $(3,1)$, $(1,2)$ has the image $(2,2)$, $(6,2)$, $(2,4)$. (i) Compare the lengths of corresponding sides and the areas. (ii) Is the transformation isometric? (iii) Name it and write its rule. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** (i) $A'(2,-1)$, $B'(5,-2)$, $C'(3,-4)$. (ii) $A''(-2,1)$, $B''(-5,2)$, $C''(-3,4)$. (iii) The object is in quadrant I, the first image in quadrant IV and the second in quadrant II, as in the reflection figure of section 9.2. (iv) $AB=\sqrt{3^2+1^2}=\sqrt{10}$ and $A'B'=\sqrt{3^2+(-1)^2}=\sqrt{10}$, so $AB=A'B'$.
**2.** (i) $(-y,x)$: $P'(-2,1)$, $Q'(-1,4)$, $R'(-4,3)$. (ii) $(-x,-y)$: $(-1,-2)$, $(-4,-1)$, $(-3,-4)$. (iii) $(y,-x)$: $(2,-1)$, $(1,-4)$, $(4,-3)$. $OP=\sqrt{1+4}=\sqrt{5}$ and $OP'=\sqrt{4+1}=\sqrt{5}$, so $OP=OP'$.
**3.** (i) $A'(4,-1)$, $B'(7,0)$, $C'(5,2)$. (ii) Plot both triangles and join each vertex to its image with an arrow; the three arrows are parallel and equal. (iii) $\overrightarrow{AB}=\binom{3}{1}$ and $\overrightarrow{A'B'}=\binom{3}{1}$: equal vectors, so $AB$ and $A'B'$ are equal and parallel. (iv) The translation by $\binom{-3}{2}$.
**4.** $P_1=(-3,2)$; $P_2=(-2,-3)$ (applying $(-y,x)$); $P_3=(-1,-7)$. $PP_3=\sqrt{4^2+9^2}=\sqrt{97}\approx9.85$ units.
**5.** (i) Object: base $3-1=2$ and height $2-1=1$, area $\frac{1}{2}\times2\times1=1$. Image: base $6-2=4$ and height $4-2=2$, area $\frac{1}{2}\times4\times2=4$. Every length is doubled and the area is multiplied by 4. (ii) No: lengths change, so it is **non-isometric**; the image is similar but not congruent. (iii) An enlargement with centre $O$ and scale factor 2: $(x,y)\rightarrow(2x,2y)$.
:::
