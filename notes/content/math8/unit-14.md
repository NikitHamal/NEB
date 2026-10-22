---
subject: Mathematics
grade: 8
title: Plane Figures
unit: 14
hours: 0
area: Compulsory Mathematics
---

A plane figure is a flat shape: a triangle, a quadrilateral, a polygon, a
circle. Geometry at this level is mostly bookkeeping with two facts — the angles
of a triangle add to 180°, and the angles of a polygon follow from splitting it
into triangles. Everything else is a consequence, and the figures are what make
those consequences visible.

::: key What this chapter asks of you
You should be able to classify triangles and quadrilaterals and state their
properties, find the interior and exterior angles of a polygon, construct a
triangle or a quadrilateral from given measurements, and use the vocabulary of
the circle.
:::

## 14.1 Triangles

A triangle is a closed figure with three sides and three angles. Its three
interior angles always add to **180°**, and any exterior angle equals the sum of
the two interior opposite angles.

| Classified by sides | Property |
|---|---|
| Equilateral | all three sides equal, all three angles 60° |
| Isosceles | two sides equal, and the angles opposite them equal |
| Scalene | no sides equal, no angles equal |

| Classified by angles | Property |
|---|---|
| Acute-angled | all three angles less than 90° |
| Right-angled | one angle is 90°; the side opposite it is the hypotenuse |
| Obtuse-angled | one angle more than 90° |

**Properties verified in class (by cutting, folding and measuring):**

- The three angles of any triangle add to 180° (tear off the corners and put
  them together: they make a straight angle).
- All three angles of an **equilateral** triangle are equal, so each is
  $180°\div3=60°$.
- The **base angles** of an isosceles triangle (the angles opposite the equal
  sides) are equal.
- In a **right-angled isosceles** triangle each base angle is
  $\frac{180°-90°}{2}=45°$.

::: example Angles of a triangle
**Problem.** In a triangle the angles are in the ratio $2:3:4$. Find each angle
and classify the triangle.

**Solution.** Let the angles be $2x$, $3x$ and $4x$. Their sum is 180°:

$$2x+3x+4x=180\;\Longrightarrow\;9x=180\;\Longrightarrow\;x=20$$

The angles are $40°$, $60°$ and $80°$. All three are less than 90°, so the
triangle is **acute-angled**.

**Check.** $40+60+80=180$ ✓, and the ratios $40:60:80=2:3:4$ ✓.
:::

::: example Isosceles triangle
**Problem.** In an isosceles triangle the vertex angle is 40°. Find the base
angles.

**Solution.** The two base angles are equal; let each be $x$. Then

$$40+x+x=180\;\Longrightarrow\;2x=140\;\Longrightarrow\;x=70$$

**Answer.** Each base angle is 70°.

**Check.** $40+70+70=180$ ✓. The vertex angle is the odd one out, and the two
angles opposite the equal sides are equal.
:::

## 14.2 Quadrilaterals

A quadrilateral has four sides and four angles, and its angles add to **360°**.

| Quadrilateral | Sides | Angles | Diagonals |
|---|---|---|---|
| Parallelogram | both pairs of opposite sides parallel and equal | opposite angles equal; adjacent angles supplementary | bisect each other |
| Rectangle | parallelogram with a right angle | all four angles 90° | equal and bisect each other |
| Square | rectangle with all sides equal | all four angles 90° | equal, bisect at right angles |
| Rhombus | parallelogram with all sides equal | opposite angles equal | bisect each other at right angles |
| Trapezium | exactly one pair of opposite sides parallel | angles on the same side of a leg supplementary | — |
| Kite | two pairs of adjacent equal sides | one pair of opposite angles equal | cross at right angles |

**Diagonal properties to remember.**

- **Rhombus:** the diagonals bisect each other at right angles, and each
  diagonal bisects the angles at its ends.
- **Kite:** the diagonals cut at right angles; the longer diagonal bisects the
  shorter one (the shorter is **not** bisected by the longer).
- **Trapezium:** only one pair of opposite sides is parallel, so a trapezium is
  **not** a parallelogram. In an isosceles trapezium the non-parallel sides are
  equal.
- Every square is a rhombus, but not every rhombus is a square.

::: example Using the rhombus diagonals
**Problem.** The diagonals of rhombus PQRS meet at O. If ∠PQO $=35°$, find
∠POQ, ∠QPO and ∠PQR.

**Solution.** ∠POQ $=90°$ (diagonals of a rhombus cut at right angles).
In $\triangle POQ$: ∠QPO $=180°-90°-35°=55°$.
∠PQR $=2\times$∠PQO $=70°$ (the diagonal QS bisects ∠PQR).
:::

```figure caption="The family of quadrilaterals. Every square is a rectangle and every rectangle is a parallelogram, but not the other way round — the arrows show which property is inherited from which."
fig, ax = plt.subplots(figsize=(5.0, 2.8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis("off")
def box(x, y, t, c):
    ax.text(x, y, t, ha="center", va="center", fontsize=6.9, color=c,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=c, lw=1.0))
box(5.0, 5.2, "Quadrilateral", INK)
box(3.0, 3.6, "Trapezium\n(one pair parallel)", MUTED)
box(7.0, 3.6, "Parallelogram\n(both pairs parallel)", ACCENT)
box(7.0, 2.1, "Rectangle", SERIES[1])
box(4.6, 2.1, "Rhombus", SERIES[2])
box(5.8, 0.8, "Square", SERIES[3])
ax.plot([5.0, 3.0], [4.9, 3.9], color=GRID, lw=1.0)
ax.plot([5.0, 7.0], [4.9, 3.9], color=GRID, lw=1.0)
ax.plot([7.0, 7.0], [3.3, 2.4], color=GRID, lw=1.0)
ax.plot([6.7, 5.0], [3.3, 2.4], color=GRID, lw=1.0)
ax.plot([7.0, 5.9], [1.8, 1.0], color=GRID, lw=1.0)
ax.plot([4.6, 5.7], [1.8, 1.0], color=GRID, lw=1.0)
fig.tight_layout()
```

::: example Angles of a quadrilateral
**Problem.** Three angles of a quadrilateral are 85°, 95° and 110°. Find the
fourth.

**Solution.** The four angles add to 360°, so the fourth is

$$360-(85+95+110)=360-290=70°$$

**Answer.** 70°.

**Check.** $85+95+110+70=360$ ✓.
:::

::: example Properties of a parallelogram
**Problem.** In a parallelogram, one angle is 65°. Find the other three and
state the property you used each time.

**Solution.** The opposite angle is **65°** (opposite angles of a parallelogram
are equal). Each of the other two is the supplement: $180-65=115°$ (adjacent
angles of a parallelogram are supplementary), and they are equal to each other
by the opposite-angle property.

**Answer.** 65°, 115°, 115°.

**Check.** $65+115+65+115=360$ ✓.
:::

## 14.3 Polygons

A **polygon** is a closed plane figure bounded by straight sides. A polygon is
**regular** when all its sides and all its angles are equal.

For a polygon with $n$ sides:

$$\text{sum of interior angles}=(n-2)\times180°$$

$$\text{each interior angle of a regular polygon}=\frac{(n-2)\times180°}{n}$$

$$\text{sum of exterior angles}=360°\qquad\text{(always, for every polygon)}$$

$$\text{each exterior angle of a regular polygon}=\frac{360°}{n}$$

The first formula comes from splitting the polygon into triangles by drawing all
the diagonals from one vertex: an $n$-sided polygon gives $n-2$ triangles.

| Polygon | Sides $n$ | Sum of interior angles | Each angle (regular) |
|---|---|---|---|
| Triangle | 3 | 180° | 60° |
| Quadrilateral | 4 | 360° | 90° |
| Pentagon | 5 | 540° | 108° |
| Hexagon | 6 | 720° | 120° |
| Octagon | 8 | 1080° | 135° |
| Decagon | 10 | 1440° | 144° |

::: example Interior and exterior angles
**Problem.** Each exterior angle of a regular polygon is 24°. Find the number of
sides, the sum of the interior angles, and each interior angle.

**Solution.** The exterior angles add to 360°, so

$$n=\frac{360}{24}=15$$

Sum of interior angles:
$(15-2)\times180=13\times180=2340°$.

Each interior angle: $\frac{2340}{15}=156°$, or equivalently
$180-24=156°$.

**Answer.** 15 sides; 2340°; 156°.

**Check.** $156+24=180$ ✓ — an interior and its exterior angle form a linear
pair.
:::

::: example Finding the number of sides
**Problem.** The sum of the interior angles of a polygon is 1260°. Find the
number of sides.

**Solution.** $(n-2)\times180=1260$, so $n-2=7$ and $n=9$.

**Answer.** A nonagon, with 9 sides.

**Check.** $(9-2)\times180=1260$ ✓.
:::

::: caution Exterior angles are not supplementary to each other
A polygon has one exterior angle at each vertex, and those $n$ angles add to
360° for every polygon, regular or not. The fact that an interior angle and its
own exterior angle add to 180° is a separate statement about the **same**
vertex. Do not confuse the two.
:::

## 14.4 Construction

Constructions are done with a ruler and a pair of compasses, and every line must
be drawn, not estimated.

| To construct | Given | Method |
|---|---|---|
| A triangle | three sides (SSS) | draw one side, then arcs of the other two lengths from its ends |
| A triangle | two sides and the included angle (SAS) | draw the included angle with a protractor or compasses, then mark off both sides |
| A triangle | two angles and a side (ASA) | draw the side, then the two angles at its ends |
| A quadrilateral | four sides and one diagonal | draw the diagonal, then construct the two triangles on either side |
| A right angle | — | bisect a straight angle with compasses |

::: tip Four habits that earn the construction marks
**(1)** Draw the given side first and label it with its length. **(2)** Keep the
compass opening unchanged while striking a pair of arcs. **(3)** Draw arcs long
enough to cross clearly — a faint arc gives a faint intersection. **(4)** Mark
every given measurement on the figure and leave all construction arcs in place;
an erased construction loses the method marks even if the figure is right.
:::

### 14.4.1 Constructing a rectangle and a parallelogram

The Grade 8 textbook asks for these constructions (ruler, compasses and
protractor). Always draw a rough sketch with the measurements first.

**Rectangle ABCD with AB = 6 cm, AD = 4 cm.**
1. Draw AB = 6 cm.
2. At A and at B construct angles of 90°.
3. Cut AD = 4 cm and BC = 4 cm on these lines.
4. Join DC. Check: DC should measure 6 cm.

**Parallelogram — three cases.** (Opposite sides of a parallelogram are equal,
so after drawing two adjacent sides the fourth vertex is found with two arcs.)

| Given | Steps |
|---|---|
| two adjacent sides and the included angle (AB = 5 cm, BC = 4 cm, ∠B = 60°) | draw BC; make 60° at B; cut BA = 5 cm; from A arc 4 cm, from C arc 5 cm; they meet at D |
| two adjacent sides and a diagonal (AB = 5 cm, BC = 4 cm, AC = 6 cm) | draw AC; from A arc 5 cm and from C arc 4 cm to get B; then from A arc 4 cm and from C arc 5 cm on the other side to get D |
| a side, a diagonal and the angle between them | draw the side, make the angle, cut the diagonal on it; complete with two arcs as above |

```figure caption="Constructing parallelogram ABCD with BC = 4 cm, AB = 5 cm and ∠ABC = 60°. After A is marked, an arc of 4 cm from A and an arc of 5 cm from C meet at D."
fig, ax = plt.subplots(figsize=(4.6, 3.0))
from matplotlib.patches import Arc
B = np.array([0.0, 0.0]); C = np.array([4.0, 0.0])
A = 5*np.array([np.cos(np.radians(60)), np.sin(np.radians(60))]); D = A + (C - B)
ax.plot([B[0], C[0]], [B[1], C[1]], color=INK, lw=1.5)
ax.plot([B[0], A[0]], [B[1], A[1]], color=INK, lw=1.5)
ax.plot([A[0], D[0]], [A[1], D[1]], color=ACCENT, lw=1.3, ls="--")
ax.plot([C[0], D[0]], [C[1], D[1]], color=ACCENT, lw=1.3, ls="--")
ax.add_patch(Arc(A, 8, 8, theta1=-12, theta2=12, color=SERIES[1], lw=1))
ax.add_patch(Arc(C, 10, 10, theta1=52, theta2=68, color=SERIES[1], lw=1))
ax.add_patch(Arc(B, 1.2, 1.2, theta1=0, theta2=60, color=INK, lw=1))
ax.text(0.75, 0.25, "60°", fontsize=9, color=INK)
for P, t, off in [(A, "A", (-0.35, 0.05)), (B, "B", (-0.35, -0.3)), (C, "C", (0.1, -0.35)), (D, "D", (0.15, 0.05))]:
    ax.text(P[0] + off[0], P[1] + off[1], t, fontsize=10, color=INK)
ax.text(2.0, -0.45, "4 cm", ha="center", fontsize=9, color=INK)
ax.text(0.7, 2.3, "5 cm", fontsize=9, color=INK, ha="right")
ax.set_xlim(-0.9, 7.6); ax.set_ylim(-0.8, 5.0); ax.set_aspect("equal"); ax.axis("off")
```

## 14.5 The circle

| Term | Meaning |
|---|---|
| Centre | the fixed point inside the circle |
| Radius | the distance from the centre to any point on the circle |
| Chord | a line segment joining two points on the circle |
| Diameter | a chord through the centre, equal to $2r$ |
| Arc | a part of the circle's boundary |
| Sector | the region between two radii and an arc |
| Segment | the region between a chord and an arc |
| Circumference | the whole distance round the circle, $2\pi r$ |

**Results worth knowing.**

- A diameter is the longest chord.
- A perpendicular from the centre to a chord bisects the chord.
- Equal chords are at equal distances from the centre.
- The angle in a semicircle is a right angle.

::: example A chord and the centre
**Problem.** A chord of length 16 cm is drawn in a circle of radius 10 cm. Find
the distance of the chord from the centre.

**Solution.** The perpendicular from the centre bisects the chord, so half the
chord is 8 cm. That, the radius and the distance $d$ form a right triangle with
the radius as the hypotenuse:

$$d=\sqrt{10^2-8^2}=\sqrt{100-64}=\sqrt{36}=6\ \text{cm}$$

**Answer.** 6 cm from the centre.

**Check.** $\sqrt{6^2+8^2}=\sqrt{36+64}=10$ ✓, which is the radius.
:::

## Chapter summary

- The angles of a triangle add to 180°; an exterior angle equals the sum of the
  two interior opposite angles.
- Equilateral, isosceles and scalene are classified by sides; acute, right and
  obtuse by angles.
- The angles of a quadrilateral add to 360°; a parallelogram has equal opposite
  angles and supplementary adjacent angles, and its diagonals bisect each other.
- For a polygon of $n$ sides: interior angles sum to $(n-2)\times180°$; exterior
  angles always sum to 360°.
- The perpendicular from the centre to a chord bisects the chord; the angle in a
  semicircle is 90°.
- Constructions are done with ruler and compasses, with every arc left in place.

## Practice questions

**Group A — Objective (1 mark each)**

1. The sum of the angles of a triangle is <span class="marks">[1]</span>
   (a) 90° (b) 180° (c) 270° (d) 360°
2. An equilateral triangle has each angle equal to
   <span class="marks">[1]</span>
   (a) 45° (b) 60° (c) 90° (d) 120°
3. The sum of the angles of a quadrilateral is <span class="marks">[1]</span>
   (a) 180° (b) 270° (c) 360° (d) 540°
4. Each interior angle of a regular hexagon is <span class="marks">[1]</span>
   (a) 60° (b) 108° (c) 120° (d) 135°
5. The sum of the exterior angles of any polygon is
   <span class="marks">[1]</span>
   (a) 180° (b) 360° (c) 540° (d) $n\times180°$
6. The longest chord of a circle is its <span class="marks">[1]</span>
   (a) radius (b) arc (c) diameter (d) tangent

::: note Answers to Group A
**1.** (b) — 180°.
**2.** (b) — $180\div3=60$.
**3.** (c) — 360°.
**4.** (c) — $\frac{(6-2)180}{6}=120$.
**5.** (b) — 360° for every polygon.
**6.** (c) — the diameter passes through the centre.
:::

**Group B — Short answer (2 marks each)**

1. Two angles of a triangle are 55° and 65°. Find the third and say what kind
   of triangle it is. <span class="marks">[2]</span>
2. Find the sum of the interior angles of a decagon.
   <span class="marks">[2]</span>
3. In a parallelogram one angle is 72°. Find the other three angles.
   <span class="marks">[2]</span>
4. A chord of length 24 cm is 5 cm from the centre of a circle. Find the radius.
   <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $180-(55+65)=60°$; all angles are less than 90°, so it is acute-angled.
**2.** $(10-2)\times180=1440°$.
**3.** The opposite angle is 72° and the other two are each
$180-72=108°$.
**4.** Half the chord is 12 cm, so
$r=\sqrt{12^2+5^2}=\sqrt{169}=13$ cm.
:::

**Group C — Long answer (4 marks each)**

1. Each interior angle of a regular polygon is 150°. Find the number of sides,
   each exterior angle, and the sum of the interior angles.
   <span class="marks">[4]</span>
2. Construct a triangle $ABC$ in which $BC=6$ cm, $AB=4.5$ cm and
   $\angle B=60°$. Measure $AC$ and the other two angles, and check that the
   angles add to 180°. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** If each interior angle is 150°, each exterior angle is
$180-150=30°$. The exterior angles add to 360°, so
$n=\frac{360}{30}=12$ sides. The sum of the interior angles is
$(12-2)\times180=1800°$.
**Check.** $\frac{1800}{12}=150°$ ✓, which is the given interior angle, so the
answer is consistent.
**2.** **Construction.** Draw $BC=6$ cm with a ruler. At $B$, construct an angle
of 60° (an equilateral triangle on $BC$ gives it exactly with compasses). With
centre $B$ and radius 4.5 cm, strike an arc on that ray; call the intersection
$A$. Join $AC$. **Measurements.** $AC\approx5.4$ cm, $\angle A\approx74°$ and
$\angle C\approx46°$.
**Check.** $60+74+46=180$ ✓. The construction is the SAS case, and it always
gives exactly one triangle, which is why the two measurements agree from any
correct drawing. The side opposite the 60° angle is the one you were asked to
measure, and it is the middle length, as it must be.
:::

**Extra practice — textbook-style questions**

**1.** True or false? Correct the false ones. (a) All the angles of an isosceles triangle are equal. (b) All rhombuses are squares. (c) The diagonals of a rhombus bisect each other at right angles. (d) All trapeziums are parallelograms.
**2.** Find the sum of the interior angles and each interior angle of a regular octagon.
**3.** Find each exterior angle of a regular polygon with 9 sides.
**4.** Construct a rectangle PQRS with PQ = 7 cm and QR = 4 cm.

::: note Extra practice — answers
**1.** (a) False — only the two base angles are equal. (b) False — all squares are rhombuses, not the other way round. (c) True. (d) False — a trapezium has only one pair of parallel sides.
**2.** Sum $=(8-2)\times180°=1080°$; each angle $=\frac{1080°}{8}=135°$.
**3.** $\frac{360°}{9}=40°$.
**4.** Draw PQ = 7 cm; make 90° at P and Q; cut PS = QR = 4 cm; join SR (it measures 7 cm).
:::

## Objective practice

**Choose the correct answer.** <span class="marks">[5×1=5]</span>

**1.** The sum of the interior angles of a quadrilateral is
   (a) $180°$ (b) $270°$ (c) $360°$ (d) $540°$
**2.** Each interior angle of a regular pentagon is
   (a) $72°$ (b) $108°$ (c) $120°$ (d) $135°$
**3.** A quadrilateral with all sides equal and no right angle is a
   (a) square (b) rhombus (c) rectangle (d) trapezium
**4.** The diagonals of a rectangle are
   (a) equal and bisect each other (b) perpendicular (c) unequal (d) parallel
**5.** The number of sides of a regular polygon whose exterior angle is $36°$ is
   (a) 8 (b) 9 (c) 10 (d) 12

::: note Objective practice — answers
**1.** (c) — $360°$. **2.** (b) — $\frac{(5-2)180°}{5} = 108°$. **3.** (b) — a rhombus. **4.** (a) — equal and bisecting. **5.** (c) — $\frac{360°}{36°} = 10$.
:::
