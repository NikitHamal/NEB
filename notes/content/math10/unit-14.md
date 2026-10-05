---
subject: Mathematics
grade: 10
unit: 14
title: Construction
hours: 0
area: Compulsory Mathematics
---

A **construction** is a drawing made with only two tools: an unmarked **ruler** (straightedge) for straight lines and a **compass** for circles and arcs. A protractor may be used only when an angle is given in degrees. Constructions turn the theorems of the previous chapter into practice: since a triangle between the same parallels keeps its area, we can **replace a quadrilateral by a triangle of exactly the same area**, or change a triangle into a parallelogram or a rectangle with the same area. Surveyors do this to simplify the shape of a plot without changing its size. In the SEE, construction questions are worth 3 or 4 marks and are scored on **accuracy, clear arcs, labelled letters, and a short statement of the steps**.

::: key What the SEE asks from this chapter
Expect one of: (i) construct a **triangle equal in area** to a given quadrilateral; (ii) construct a **parallelogram equal in area to a triangle** with a given angle; (iii) construct a **rectangle** or a **square** equal in area to a given figure; (iv) construct a triangle or quadrilateral from the given sides and angles first, then do (i)–(iii). Always write **Steps of construction** in order, leave all compass arcs visible, and add a line of justification ("Proof") explaining why the areas are equal.
:::

```photo id="math10/drawing-pen" caption="Technical drawing pens. Every construction in this chapter is done with a compass and a straight edge, and the result is only as accurate as the instrument and the hand that holds it." width="58"
```

## 14.1 Construction: concepts, formulas and worked problems

### Equipment and conventions

| Tool | Used for |
|---|---|
| Sharp pencil (HB / 2H) | thin, accurate lines and arcs |
| Ruler | straight lines, measuring given lengths |
| Compass | arcs of a given radius, copying a length |
| Protractor | drawing a given angle (e.g. $60^\circ$) |
| Set squares | parallel lines and right angles (optional) |

Conventions: label every point; draw given figures with **thin full lines**; draw construction lines (parallels, perpendiculars) in **light lines**; keep **arcs visible**; the required figure should be drawn darker. Write the given data at the top of the page.

### Basic constructions you need

::: key Four basic constructions
1. **Perpendicular bisector** of $AB$: arcs of the same radius (more than $\frac{1}{2}AB$) from $A$ and from $B$ meet at two points; join them.
2. **Bisector of an angle**: arc cutting both arms; two equal arcs from those points meet; join the vertex to the intersection.
3. **Perpendicular from a point to a line**: arc from the point cutting the line twice; then bisect the segment between the cut points.
4. **Line through a point parallel to a given line** — shown below, using a rhombus.
:::

### Parallel line through a point

```figure caption="To draw the line through P parallel to l: arc from Q through P meets l at R; arcs of the same radius from P and R meet at S. Then PQRS is a rhombus, so PS ∥ QR."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Arc
fig, ax = plt.subplots(figsize=(4.8, 2.4))
Q = np.array([2.0, 0.0]); P = np.array([3.0, 2.2])
r = np.linalg.norm(P - Q)
R = Q + np.array([r, 0.0]); S = P + (R - Q)
ax.plot([0, 9.2], [0, 0], color=INK, lw=1.2)
ax.text(9.0, 0.12, 'l', fontsize=9)
th = np.degrees(np.arctan2(P[1], P[0] - Q[0]))
ax.add_patch(Arc(Q, 2*r, 2*r, theta1=-2, theta2=th + 6, color=ACCENT, lw=0.9))
ax.add_patch(Arc(P, 2*r, 2*r, theta1=-28, theta2=28, color='#dc2626', lw=0.9))
ax.add_patch(Arc(R, 2*r, 2*r, theta1=th - 28, theta2=th + 28, color='#dc2626', lw=0.9))
ax.plot([P[0], S[0] + 1.4], [P[1], S[1]], color=INK, lw=1.2)
ax.plot([P[0] - 1.3, P[0]], [P[1], P[1]], color=INK, lw=1.2)
ax.plot([Q[0], P[0]], [Q[1], P[1]], color=MUTED, lw=0.9, ls='--')
ax.plot([R[0], S[0]], [R[1], S[1]], color=MUTED, lw=0.9, ls='--')
for pt, t, dx, dy in [(Q, 'Q', -0.1, -0.4), (R, 'R', -0.05, -0.4), (P, 'P', -0.45, 0.1), (S, 'S', -0.05, 0.15)]:
    ax.plot(*pt, 'o', color=INK, ms=3)
    ax.text(pt[0] + dx, pt[1] + dy, t, fontsize=9)
ax.text(7.2, 2.35, 'line through P ∥ l', fontsize=8.5)
ax.set_xlim(-0.2, 9.8); ax.set_ylim(-0.8, 3.0); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: example Construct a line parallel to l through P
**Steps.**

1. Draw a line $l$ and mark a point $P$ not on it.
2. Mark any point $Q$ on $l$. Join $PQ$.
3. With centre $Q$ and radius $QP$ draw an arc cutting $l$ at $R$.
4. With centres $P$ and $R$ and the **same radius** $QP$ draw two arcs that cross at $S$.
5. Join $P$ and $S$ and extend both ways. $PS\parallel l$.

**Proof.** $PQ=QR=RS=SP$ (all equal to the radius), so $PQRS$ is a rhombus; opposite sides of a rhombus are parallel, hence $PS\parallel QR$, that is $PS\parallel l$.
:::

### A triangle equal in area to a quadrilateral

The idea: the diagonal $AC$ splits quadrilateral $ABCD$ into $\Delta ABC$ and $\Delta ACD$. We replace $\Delta ACD$ by a triangle $\Delta ACE$ with the **same base $AC$** and the apex $E$ on a line through $D$ parallel to $AC$. By the theorem of Chapter 13, $\Delta ACE=\Delta ACD$.

```figure caption="Quadrilateral ABCD is replaced by triangle ABE of the same area: DE ∥ AC meets BC produced at E, so ΔACD = ΔACE."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon
fig, ax = plt.subplots(figsize=(4.8, 3.6))
A = np.array([0, 0.]); B = np.array([5, 0.]); C = np.array([6, 3.5]); D = np.array([1.5, 3.])
M = np.array([C - A, -(C - B)]).T
t, s = np.linalg.solve(M, B - D)
E = B + s * (C - B)
ax.add_patch(Polygon([A, B, E], fc='#dbeafe', ec='none'))
ax.add_patch(Polygon([A, B, C, D], fc='#fde68a', ec=INK, lw=1.3))
ax.plot([C[0], E[0]], [C[1], E[1]], color=INK, lw=1.1)
ax.plot([A[0], E[0]], [A[1], E[1]], color=INK, lw=1.1)
ax.plot([A[0], C[0]], [A[1], C[1]], color=MUTED, lw=1.0, ls='--')
ax.plot([D[0] - 0.5, E[0]], [D[1] - 0.5 * (C[1] / C[0]), E[1]], color='#dc2626', lw=1.0, ls='--')
ax.text(2.2, 1.0, 'quadrilateral\nABCD', fontsize=8, ha='center')
ax.text(5.2, 4.6, 'ΔACD = ΔACE', fontsize=8.5, color='#dc2626')
for pt, tt, dx, dy in [(A, 'A', -0.4, -0.35), (B, 'B', 0.1, -0.4), (C, 'C', 0.15, -0.1), (D, 'D', -0.4, 0.1), (E, 'E', 0.15, 0.1)]:
    ax.text(pt[0] + dx, pt[1] + dy, tt, fontsize=9)
ax.set_xlim(-0.8, 8.2); ax.set_ylim(-0.8, 6.8); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: example Triangle equal to a quadrilateral
**Problem.** Construct a quadrilateral $ABCD$ with $AB=5$ cm, $BC=4$ cm, $CD=4$ cm, $DA=3.5$ cm and $\angle B=70^\circ$, and construct a triangle equal in area to it.

**Steps of construction.**

1. Draw $AB=5$ cm. At $B$ construct $\angle ABX=70^\circ$ and cut $BC=4$ cm along $BX$.
2. With centre $A$ radius 3.5 cm and centre $C$ radius 4 cm draw arcs meeting at $D$. Join $AD$ and $CD$. $ABCD$ is the quadrilateral.
3. Join the diagonal $AC$.
4. Through $D$ draw a line parallel to $AC$ (use the rhombus method above).
5. Produce $BC$ to meet that line at $E$.
6. Join $AE$. **$\Delta ABE$ is the required triangle.**

**Proof.** $\Delta ACD$ and $\Delta ACE$ are on the same base $AC$ and between the same parallels $AC$ and $DE$, so $\text{area}(\Delta ACD)=\text{area}(\Delta ACE)$. Adding $\text{area}(\Delta ABC)$ to both:

$$ \text{area}(ABCD)=\text{area}(\Delta ABC)+\text{area}(\Delta ACD) $$

$$ =\text{area}(\Delta ABC)+\text{area}(\Delta ACE)=\text{area}(\Delta ABE) $$

**Numerical check.** For the quadrilateral $A(0,0)$, $B(5,0)$, $C(6,3.5)$, $D(1.5,3)$ of the figure, the shoelace formula gives area $15.125\text{ cm}^2$, and the triangle $ABE$ with $E=(6.73,6.05)$ has area $\frac{1}{2}\times5\times6.05=15.125\text{ cm}^2$. ✓
:::

::: caution Common mistakes in constructions
- Rubbing out arcs. The examiner needs them as evidence of the method.
- A line through $D$ that is only *nearly* parallel to $AC$ — use the rhombus or set-square method carefully.
- Forgetting to **produce** (extend) $BC$ far enough to meet the parallel line.
- Giving no steps or no proof: construction marks are usually split among figure, steps and justification.
- Measuring the given angle with the wrong scale on the protractor ($70^\circ$ vs $110^\circ$).
:::

### A parallelogram equal in area to a triangle

The idea: $\text{area}(\Delta)=\frac{1}{2}\times\text{base}\times\text{height}$ and $\text{area}(\text{parallelogram})=\text{base}\times\text{height}$. So a parallelogram with **half the base** and the same height has the same area as the triangle.

```figure caption="Parallelogram MCZY equal to ΔABC: M is the midpoint of BC, MY makes the given angle 60° with MC, AY ∥ BC, and CZ ∥ MY."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Arc
fig, ax = plt.subplots(figsize=(4.8, 2.8))
B = np.array([0, 0.]); C = np.array([6, 0.]); A = np.array([2, 3.2])
M = (B + C) / 2
u = np.array([np.cos(np.pi / 3), np.sin(np.pi / 3)])
Y = np.array([M[0] + (A[1] / u[1]) * u[0], A[1]])
Z = C + (Y - M)
ax.add_patch(Polygon([M, C, Z, Y], fc='#dcfce7', ec=INK, lw=1.3))
ax.add_patch(Polygon([A, B, C], fc='none', ec=INK, lw=1.3))
ax.plot([A[0] - 0.8, Z[0] + 0.6], [A[1], A[1]], color='#dc2626', lw=1.0, ls='--')
ax.add_patch(Arc(M, 1.4, 1.4, theta1=0, theta2=60, color=ACCENT, lw=1.0))
ax.text(M[0] + 0.55, 0.18, '60°', fontsize=8, color=ACCENT)
ax.plot([M[0], Y[0] + 0.25], [0, A[1] + 0.25 * u[1] / u[0] * 0 + 0.25 * u[1] / u[0]], color=MUTED, lw=0.8, ls=':')
for pt, tt, dx, dy in [(B, 'B', -0.35, -0.4), (C, 'C', 0.05, -0.4), (A, 'A', -0.45, 0.05), (M, 'M', -0.1, -0.45), (Y, 'Y', -0.1, 0.15), (Z, 'Z', 0.05, 0.15)]:
    ax.text(pt[0] + dx, pt[1] + dy, tt, fontsize=9)
ax.plot([0, 9], [0, 0], color=INK, lw=0.8)
ax.set_xlim(-0.8, 9.0); ax.set_ylim(-0.9, 4.0); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: example Parallelogram equal to a triangle, with a given angle
**Problem.** Construct $\Delta ABC$ with $BC=6$ cm, $AB=3.8$ cm and $\angle B=57^\circ$. Then construct a parallelogram equal in area to it having one angle of $60^\circ$.

**Steps of construction.**

1. Construct $\Delta ABC$ from the given data.
2. Bisect $BC$ (perpendicular bisector): $M$ is the midpoint of $BC$.
3. At $M$ construct $\angle CMX=60^\circ$ (the given angle).
4. Through $A$ draw a line parallel to $BC$ meeting $MX$ at $Y$.
5. Through $C$ draw a line parallel to $MY$ meeting $AY$ produced at $Z$.
6. **$MCZY$ is the required parallelogram.**

**Proof.** $MC\parallel YZ$ and $MY\parallel CZ$, so $MCZY$ is a parallelogram with $\angle YMC=60^\circ$. It stands on base $MC=\frac{1}{2}BC$ and has the same height as $\Delta ABC$ (the distance between the parallels $BC$ and $AY$). So

$$ \text{area}(MCZY)=MC\times h=\frac{1}{2}BC\times h=\text{area}(\Delta ABC) $$

**Numerical check** (figure: $BC=6$, height $h=3.2$): triangle $\frac{1}{2}\times6\times3.2=9.6$; parallelogram $3\times3.2=9.6$. ✓
:::

::: key Replacing a figure by one with the same area
| Start with | Replace by | Key theorem |
|---|---|---|
| Triangle $ACD$ | Triangle $ACE$ (apex slid along a parallel to the base) | same base, same parallels |
| Quadrilateral | Triangle (one diagonal used) | as above, then add $\Delta ABC$ |
| Triangle | Parallelogram on **half the base** (any angle) | triangle $=\frac{1}{2}$ parallelogram |
| Triangle | Rectangle on half the base (angle $90^\circ$) | special case of above |
| Pentagon | Quadrilateral, then triangle | apply the "slide the apex" step twice |
:::

### A rectangle equal to a triangle

::: example Rectangle equal to a triangle
**Problem.** Construct a rectangle equal in area to $\Delta ABC$ ($BC=6$ cm, height 3.2 cm).

**Steps.** (1) Draw the triangle. (2) Bisect $BC$ at $M$. (3) At $M$ draw $MX\perp BC$. (4) Through $A$ draw $AY\parallel BC$ meeting $MX$ at $Y$. (5) Through $C$ draw $CZ\perp BC$ meeting $AY$ produced at $Z$. $MCZY$ is a rectangle.

**Proof.** Its sides are $MC=\frac{1}{2}BC=3$ cm and $MY=3.2$ cm, so area $=3\times3.2=9.6\text{ cm}^2=\frac{1}{2}\times6\times3.2=\text{area}(\Delta ABC)$.
:::

### A square equal to a rectangle

A square of side $x$ equal to a rectangle $a\times b$ needs $x^2=ab$, i.e. $x=\sqrt{ab}$: the **geometric mean** of the sides. The semicircle gives this length.

```figure caption="Square equal to a rectangle 4 cm × 2.25 cm: on PQ = 4 + 2.25 draw a semicircle; the perpendicular at the junction O meets it at T; OT = √(4 × 2.25) = 3 cm."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Arc, Rectangle
fig, ax = plt.subplots(figsize=(4.8, 3.6))
a, b = 4.0, 2.25
P = np.array([0, 0.]); O = np.array([a, 0.]); Q = np.array([a + b, 0.])
c = np.array([(a + b) / 2, 0.]); R = (a + b) / 2
ax.add_patch(Arc(c, 2*R, 2*R, theta1=0, theta2=180, color=ACCENT, lw=1.3))
ax.plot([0, a + b], [0, 0], color=INK, lw=1.2)
h = np.sqrt(a * b)
ax.plot([O[0], O[0]], [0, h], color='#dc2626', lw=1.3)
ax.add_patch(Rectangle((0, -2.9), a, b, fc='#dbeafe', ec=INK, lw=0.9))
ax.text(a / 2, -2.9 + b / 2, 'rectangle\n4 × 2.25', fontsize=8, ha='center', va='center')
ax.text(O[0] + 0.12, h / 2, 'OT = 3', fontsize=8.5, color='#dc2626')
ax.plot([O[0]], [h], 'o', color='#dc2626', ms=3.5)
ax.text(O[0] - 0.1, h + 0.15, 'T', fontsize=9)
ax.text(-0.1, 0.15, 'P', fontsize=9, ha='right'); ax.text(O[0] + 0.05, -0.38, 'O', fontsize=9); ax.text(Q[0] + 0.1, 0.1, 'Q', fontsize=9)
ax.text(a / 2, 0.12, 'a = 4', fontsize=8, ha='center'); ax.text(a + b / 2, 0.12, 'b = 2.25', fontsize=8, ha='center')
ax.set_xlim(-0.8, 7.0); ax.set_ylim(-3.1, 3.5); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: example Square equal to a rectangle
**Problem.** Construct a square equal in area to a rectangle of sides 4 cm and 2.25 cm.

**Steps.** (1) Draw $PO=4$ cm and produce it to $Q$ so that $OQ=2.25$ cm. (2) Bisect $PQ$ and draw a semicircle on $PQ$ as diameter. (3) At $O$ draw $OT\perp PQ$ to meet the semicircle at $T$. (4) Construct a square on $OT$ as a side.

**Proof.** The angle in a semicircle is a right angle: $\angle PTQ=90^\circ$. In the right triangle $PTQ$ with altitude $TO$, the triangles $POT$ and $TOQ$ are similar, so $\frac{PO}{OT}=\frac{OT}{OQ}$ and $OT^2=PO\times OQ=4\times2.25=9$. So $OT=3$ cm, and the square on $OT$ has area $9\text{ cm}^2=4\times2.25$. ✓
:::

### Constructing the triangle first

Many questions start with a triangle or quadrilateral described by lengths and angles. The standard cases are:

| Given | Method |
|---|---|
| SSS: three sides | base; two arcs from its ends |
| SAS: two sides and the included angle | base, angle at one end, cut off the side |
| ASA: two angles and the included side | base; two angles at its ends |
| Quadrilateral: 4 sides and 1 diagonal | two triangles on the diagonal |
| Quadrilateral: 4 sides and 1 angle | triangle from SAS, then arcs |

::: example Triangle from SSS, then half its area
**Problem.** Construct $\Delta PQR$ with $PQ=7$ cm, $QR=5$ cm and $PR=6$ cm. Find its area by Heron's formula and then construct a rectangle of the same area.

**Solution.** Area: $s=\frac{7+5+6}{2}=9$; $\text{area}=\sqrt{9\times2\times4\times3}=\sqrt{216}=14.70\text{ cm}^2$. Construct the triangle by drawing $PQ=7$ cm and arcs of radius 6 cm from $P$ and 5 cm from $Q$. The rectangle has base $\frac{1}{2}PQ=3.5$ cm and height equal to the height of $R$ above $PQ$: $h=\frac{2\times14.70}{7}=4.20$ cm. Check: $3.5\times4.20=14.7$. ✓
:::

## 14.2 Exercises of the SEE type

### Method for any question

1. Read the data and draw a **rough sketch** with all measurements.
2. Construct the given figure accurately (SSS/SAS/ASA, etc.).
3. Draw the diagonal or the median that the method needs, in a light line.
4. Draw the parallel line **through the vertex** you are replacing; produce the side to meet it.
5. Darken the required figure; label every vertex; keep the arcs.
6. Write the **steps** and a two-line **proof** referring to "same base, same parallels".

::: example SEE type: quadrilateral to triangle
**Problem.** Construct a quadrilateral $ABCD$ with $AB=4.5$ cm, $BC=3.5$ cm, $CD=4$ cm, $DA=3$ cm and diagonal $AC=5$ cm. Construct a triangle equal in area to it.

**Solution (outline).** Triangle $ABC$ from three sides (4.5, 3.5, 5). Triangle $ACD$ on the other side of $AC$ from sides $AD=3$ and $CD=4$ (arcs from $A$ and $C$). Through $D$ draw $DE\parallel AC$ meeting $BC$ produced at $E$. Join $AE$: $\Delta ABE$ is the answer, because $\Delta ACD=\Delta ACE$.

**Area check.** $\Delta ACD$ has sides $3,4,5$, a right-angled triangle of area $6\text{ cm}^2$. $\Delta ABC$: $s=6.5$, area $=\sqrt{6.5\times2\times3\times1.5}=\sqrt{58.5}=7.65\text{ cm}^2$. Quadrilateral area $=13.65\text{ cm}^2$, which equals $\text{area}(\Delta ABE)$.
:::

::: example SEE type: parallelogram from a triangle
**Problem.** Construct $\Delta ABC$ with $AB=5$ cm, $BC=6$ cm, $CA=4.5$ cm and a parallelogram equal in area to it with one angle of $45^\circ$.

**Solution (outline).** $\Delta ABC$ from SSS. Mark the midpoint $M$ of $BC$. At $M$ construct $45^\circ$ to $MC$. Through $A$ draw $AY\parallel BC$ meeting the new ray at $Y$. Through $C$ draw $CZ\parallel MY$ meeting $AY$ produced at $Z$. $MCZY$ is the parallelogram, with area $MC\times h=\frac{1}{2}BC\times h=\text{area}(\Delta ABC)$.

**Area check.** $s=7.75$; area $=\sqrt{7.75\times2.75\times1.75\times3.25}=\sqrt{121.2}=11.01\text{ cm}^2$, height on $BC$ is $\frac{2\times11.01}{6}=3.67$ cm; parallelogram $3\times3.67=11.01$. ✓
:::

## Chapter summary

- Constructions use only a ruler and compass (a protractor only for a given angle); keep all arcs.
- Parallel through a point: rhombus method with equal radii.
- **Triangle = quadrilateral:** join diagonal $AC$; through $D$ draw $DE\parallel AC$ meeting $BC$ produced at $E$; $\Delta ABE$ has the same area.
- **Parallelogram = triangle:** bisect the base; draw the given angle at the midpoint; parallels through the apex and through the end of the base.
- **Rectangle = triangle:** same, with $90^\circ$. **Square = rectangle:** semicircle on $a+b$; the perpendicular at the junction is $\sqrt{ab}$.
- The proofs rest on: triangles on the same base between the same parallels are equal in area; a triangle is half a parallelogram.
- Steps + figure + proof earns the full marks.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Which tool may be used to draw an arc in a construction? <span class="marks">[1]</span>
   (a) ruler (b) compass (c) calculator (d) set square only
2. To change a quadrilateral into a triangle of equal area we draw a line through a vertex parallel to <span class="marks">[1]</span>
   (a) a side (b) the diagonal that does not pass through that vertex (c) the perpendicular bisector (d) the angle bisector
3. A parallelogram equal in area to a triangle is constructed on <span class="marks">[1]</span>
   (a) the full base (b) half the base (c) double the base (d) the hypotenuse
4. The side of a square equal in area to a rectangle $9\times4$ is <span class="marks">[1]</span>
   (a) 5 (b) 6 (c) 36 (d) 13
5. The angle in a semicircle is <span class="marks">[1]</span>
   (a) $60^\circ$ (b) $45^\circ$ (c) $90^\circ$ (d) $180^\circ$

::: note Answers to Group A
**1.** (b).
**2.** (b) — parallel to the diagonal $AC$ through $D$.
**3.** (b) — base halves, height unchanged.
**4.** (b) — $\sqrt{9\times4}=6$.
**5.** (c).
:::

**Group B — Short answer (2 marks each)**

1. Describe how to draw a line through a point $P$ parallel to a line $l$ using only compass and ruler. <span class="marks">[2]</span>
2. A triangle has base 8 cm and height 5 cm. What base and height does a rectangle of equal area have if its base is half the triangle's base? <span class="marks">[2]</span>
3. Why are triangles $ACD$ and $ACE$ equal in area in the quadrilateral construction? <span class="marks">[2]</span>
4. Find the side of a square equal in area to a rectangle $12\text{ cm}\times3\text{ cm}$. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** Mark $Q$ on $l$; arc centre $Q$ radius $QP$ cuts $l$ at $R$; arcs of the same radius from $P$ and $R$ meet at $S$; line $PS$ is parallel to $l$ (rhombus $PQRS$).
**2.** Base 4 cm, height 5 cm: $4\times5=20=\frac{1}{2}\times8\times5$.
**3.** Same base $AC$ and same parallels $AC$, $DE$, hence the same height.
**4.** $\sqrt{36}=6$ cm.
:::

**Group C — Short answer (3 marks each)**

1. Construct $\Delta ABC$ with $AB=5$ cm, $BC=6$ cm, $\angle B=60^\circ$. Bisect $BC$ at $M$. <span class="marks">[3]</span>
2. Construct a parallelogram equal in area to the triangle of question 1, having an angle of $60^\circ$ at $M$. <span class="marks">[3]</span>
3. Construct a rectangle of sides 5 cm and 3.2 cm; state the steps to construct a square of equal area. <span class="marks">[3]</span>
4. Show by calculation that a triangle with base 10 cm and height 7.2 cm equals a parallelogram of base 5 cm and height 7.2 cm. <span class="marks">[3]</span>

::: note Answers to Group C
**1.** Draw $BC=6$, angle $60^\circ$ at $B$, cut $BA=5$; the perpendicular bisector of $BC$ gives $M$.
**2.** As in the worked example: $MY$ at $60^\circ$ to $MC$, $AY\parallel BC$, $CZ\parallel MY$.
**3.** Extend 5 to $5+3.2=8.2$; semicircle; perpendicular at the junction gives $\sqrt{5\times3.2}=\sqrt{16}=4$ cm; square of side 4 cm (area 16 = $5\times3.2$).
**4.** Triangle: $\frac{1}{2}\times10\times7.2=36$; parallelogram: $5\times7.2=36$.
:::

**Group D — Long answer (4 marks each)**

1. Construct quadrilateral $ABCD$ with $AB=5$ cm, $BC=4$ cm, $CD=4$ cm, $DA=3.5$ cm and $\angle B=70^\circ$, and construct a triangle equal in area to it. Give steps and proof. <span class="marks">[4]</span>
2. Construct $\Delta ABC$ with $BC=6$ cm, $\angle B=57^\circ$, $AB=3.8$ cm. Construct a parallelogram equal in area with one angle of $60^\circ$. <span class="marks">[4]</span>
3. Construct a square equal in area to a rectangle $6\text{ cm}\times 2\text{ cm}$ and prove that your square has the right area. <span class="marks">[4]</span>
4. Construct $\Delta PQR$ with sides 7, 5, 6 cm and a rectangle equal to it, giving the rectangle's dimensions. <span class="marks">[4]</span>

::: note Answers to Group D
**1.** Follow the worked example; area check $15.125\text{ cm}^2$ for the coordinates used there.
**2.** Follow the worked example; area of the triangle is $\frac{1}{2}\times6\times3.8\times\sin57^\circ\approx9.56\text{ cm}^2$.
**3.** $\sqrt{6\times2}=\sqrt{12}\approx3.46$ cm: semicircle on $PQ=8$ with the perpendicular at the junction of 6 and 2; $OT^2=12$.
**4.** Area $\sqrt{216}\approx14.70\text{ cm}^2$; rectangle $3.5\text{ cm}\times4.2\text{ cm}$.
:::
