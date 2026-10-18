---
subject: Mathematics
grade: 10
unit: 15
title: Circle
hours: 0
area: Compulsory Mathematics
---

Wheels, coins, clocks, pizza and the Moon all show the circle, the most symmetrical of shapes. In earlier classes you measured circles (circumference and area) and met the language: centre, radius, diameter, chord, arc, segment and sector. In this chapter we study the **geometry** of the circle: how angles at the centre and at the circumference are related, why the angle in a semicircle is a right angle, why the opposite angles of a **cyclic quadrilateral** add to $180^\circ$, and how **tangents** behave. Each result is a theorem that you must be able to **prove** with a figure, and then **use** to find unknown angles and lengths.

::: key What the SEE asks from this chapter
Expect: (i) **prove** a theorem: the angle at the centre is twice the angle at the circumference; angles in the same segment are equal; the angle in a semicircle is $90^\circ$; the opposite angles of a cyclic quadrilateral are supplementary (4 marks, figure required); (ii) find unknown angles, often with algebra such as $(2x+10)^\circ$; (iii) problems with **tangents**: tangent $\perp$ radius, two tangents from a point are equal, with Pythagoras; (iv) chord problems with a perpendicular from the centre. Always write **Given, To prove, Construction, Proof** and a reason beside every step.
:::

```photo id="math10/ferris-wheel" caption="A Ferris wheel. Every point on the rim is the same distance from the centre, and the whole rim turns about that fixed centre — the two facts that define a circle." width="86"
```

## 15.1 Circle: concepts, formulas and worked problems

### Vocabulary and chords

| Term | Meaning |
|---|---|
| Chord | a line segment joining two points of the circle |
| Diameter | a chord through the centre (the longest chord, $2r$) |
| Arc | a part of the circumference; the **minor** arc is the shorter, the **major** the longer |
| Segment | the region between a chord and an arc |
| Angle at the centre | angle made at $O$ by two radii, e.g. $\angle AOB$ |
| Angle at the circumference | angle made at a point of the circle by two chords, e.g. $\angle ACB$ |
| Cyclic quadrilateral | a quadrilateral whose four vertices lie on a circle |
| Tangent | a line that touches the circle at exactly one point |

::: key Chord facts from earlier classes
- The perpendicular from the centre to a chord **bisects** the chord; the line from the centre to the midpoint of a chord is perpendicular to it.
- Equal chords are equally distant from the centre.
- For a chord of length $2c$ at distance $d$ from the centre of a circle of radius $r$: $\;r^2=c^2+d^2$.
:::

::: example Chord and distance
**Problem.** A chord of length 24 cm lies in a circle of radius 13 cm. Find its distance from the centre.

**Solution.** The perpendicular from the centre bisects the chord: half-chord $=12$ cm. The radius to an end of the chord, the half-chord and the perpendicular form a right triangle, so $d^2=13^2-12^2=169-144=25$ and $d=5$ cm.
:::

::: example Radius from a chord
**Problem.** A chord of length 16 cm is 6 cm from the centre. Find the radius.

**Solution.** Half-chord $=8$ cm. $r^2=8^2+6^2=100$, so $r=10$ cm.
:::

### Angle at the centre and at the circumference

```figure caption="The angle at the centre AOB is twice the angle at the circumference ACB standing on the same arc AB. CD is drawn through O."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4, 3.8))
def pt(d): return np.array([np.cos(np.radians(d)), np.sin(np.radians(d))])
t = np.linspace(0, 2*np.pi, 300)
ax.plot(np.cos(t), np.sin(t), color=INK, lw=1.3)
A, B, C, D, O = pt(220), pt(320), pt(90), pt(270), np.array([0, 0.])
for X, Y, st, lw in [(O, A, '-', 1.2), (O, B, '-', 1.2), (C, A, '-', 1.2), (C, B, '-', 1.2), (C, D, '--', 0.9)]:
    ax.plot([X[0], Y[0]], [X[1], Y[1]], color=INK if st == '-' else MUTED, lw=lw, ls=st)
for P, tt, dx, dy in [(A, 'A', -0.17, -0.1), (B, 'B', 0.06, -0.1), (C, 'C', -0.05, 0.08), (D, 'D', -0.04, -0.2), (O, 'O', 0.05, 0.05)]:
    ax.text(P[0] + dx, P[1] + dy, tt, fontsize=9)
ax.text(0.0, -0.45, '2x', fontsize=8.5, ha='center', color='#dc2626')
ax.text(0.0, 0.62, 'x', fontsize=8.5, ha='center', color=ACCENT)
ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.25); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: derivation Angle at the centre is twice the angle at the circumference
**Given.** A circle with centre $O$; $A$ and $B$ are points on it; $C$ is a point on the major arc $AB$.

**To prove.** $\angle AOB=2\angle ACB$.

**Construction.** Join $CO$ and produce it to meet the circle at $D$.

**Proof.**

**Step 1.** In $\Delta OAC$, $OA=OC$ (radii), so $\angle OAC=\angle OCA$. Let $\angle OCA=\alpha$, so $\angle OAC=\alpha$.

**Step 2 — exterior angle.** The exterior angle of $\Delta OAC$ at $O$ is $\angle AOD$, which equals the sum of the two opposite interior angles:

$$ \angle AOD=\angle OAC+\angle OCA=2\alpha $$

**Step 3.** In the same way in $\Delta OBC$ with $\angle OCB=\beta$: $\angle BOD=2\beta$.

**Step 4 — add.**

$$ \angle AOB=\angle AOD+\angle BOD=2\alpha+2\beta=2(\alpha+\beta)=2\angle ACB $$

**Result.** $\angle AOB=2\angle ACB$. Proved.

**What it means.** The angle at the centre is double any angle at the circumference on the same arc. A central angle of $100^\circ$ means an angle of $50^\circ$ at any point of the major arc.
:::

::: example Using the theorem
**Problem.** $O$ is the centre of a circle and $\angle AOB=100^\circ$. Find $\angle ACB$ where $C$ is on the major arc. Also find $\angle ADB$ where $D$ is on the **minor** arc.

**Solution.** $\angle ACB=\frac{1}{2}\times100^\circ=50^\circ$. Points $C$ and $D$ are on opposite arcs, so $ACBD$ is a cyclic quadrilateral and $\angle ADB=180^\circ-50^\circ=130^\circ$.
:::

::: example Isosceles triangle in a circle
**Problem.** $OA$ and $OB$ are radii and $\angle OAB=25^\circ$. Find $\angle AOB$ and the angle at the circumference $\angle ACB$ ($C$ on the major arc).

**Solution.** $OA=OB$, so $\angle OBA=25^\circ$ and $\angle AOB=180^\circ-2\times25^\circ=130^\circ$. Then $\angle ACB=\frac{1}{2}\times130^\circ=65^\circ$.
:::

### Angles in the same segment; angle in a semicircle

```figure caption="Left: angles ACB and ADB in the same segment are equal. Right: AB is a diameter, so the angle in a semicircle ACB is 90°."
import numpy as np, matplotlib.pyplot as plt
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.0, 2.7))
def pt(d): return np.array([np.cos(np.radians(d)), np.sin(np.radians(d))])
t = np.linspace(0, 2*np.pi, 300)
for ax in (ax1, ax2):
    ax.plot(np.cos(t), np.sin(t), color=INK, lw=1.2)
    ax.set_aspect('equal'); ax.axis('off')
A, B, C, D = pt(210), pt(330), pt(70), pt(120)
for X, Y in [(A, B), (C, A), (C, B), (D, A), (D, B)]:
    ax1.plot([X[0], Y[0]], [X[1], Y[1]], color=INK, lw=1.1)
for P, tt, dx, dy in [(A, 'A', -0.17, -0.12), (B, 'B', 0.05, -0.12), (C, 'C', 0.04, 0.06), (D, 'D', -0.17, 0.06)]:
    ax1.text(P[0] + dx, P[1] + dy, tt, fontsize=9)
ax1.text(0.0, 0.5, 'x   x', fontsize=8.5, ha='center', color='#dc2626')
ax1.set_xlim(-1.35, 1.35); ax1.set_ylim(-1.35, 1.35)
A2, B2, C2 = np.array([-1, 0.]), np.array([1, 0.]), pt(65)
for X, Y in [(A2, B2), (C2, A2), (C2, B2)]:
    ax2.plot([X[0], Y[0]], [X[1], Y[1]], color=INK, lw=1.1)
ax2.plot([0], [0], 'o', color=INK, ms=2.5)
ax2.text(0.05, -0.2, 'O', fontsize=8.5)
ax2.plot([C2[0] - 0.14 * np.cos(np.radians(25)) * 0 , C2[0]], [C2[1], C2[1]], alpha=0)
ax2.text(C2[0] - 0.02, C2[1] - 0.38, '90°', fontsize=8.5, ha='center', color='#dc2626')
for P, tt, dx, dy in [(A2, 'A', -0.2, -0.05), (B2, 'B', 0.06, -0.05), (C2, 'C', 0.05, 0.06)]:
    ax2.text(P[0] + dx, P[1] + dy, tt, fontsize=9)
ax2.set_xlim(-1.35, 1.35); ax2.set_ylim(-1.35, 1.35)
fig.tight_layout(pad=0.3)
```

::: derivation Angles in the same segment are equal
**Given.** $C$ and $D$ are points on the same arc of a circle standing on chord $AB$ (in the same segment).

**To prove.** $\angle ACB=\angle ADB$.

**Construction.** Join $OA$ and $OB$ ($O$ the centre).

**Proof.** The angle at the centre standing on arc $AB$ is $\angle AOB$. By the previous theorem

$$ \angle ACB=\frac{1}{2}\angle AOB \qquad \angle ADB=\frac{1}{2}\angle AOB $$

**Result.** Both equal half of $\angle AOB$, so $\angle ACB=\angle ADB$. Proved.
:::

::: derivation The angle in a semicircle is a right angle
**Given.** $AB$ is a diameter of a circle with centre $O$; $C$ is any point on the circle.

**To prove.** $\angle ACB=90^\circ$.

**Proof.**

**Step 1.** $AB$ is a straight line through $O$, so the angle at the centre on arc $AB$ is the straight angle $\angle AOB=180^\circ$.

**Step 2.** The angle at the circumference is half of it: $\angle ACB=\frac{1}{2}\times180^\circ=90^\circ$.

**Result.** $\angle ACB=90^\circ$. Proved.

**What it means.** Every triangle that has a diameter for one side and its third vertex on the circle is right-angled at that vertex. This is also why the converse is used to find the centre: the hypotenuse of a right triangle is a diameter of its circumcircle.
:::

::: example Same segment
**Problem.** Chord $AB$ subtends $\angle ACB=35^\circ$ at point $C$ of the major arc, and $D$ is another point on the same arc. Find $\angle ADB$ and $\angle AOB$.

**Solution.** $\angle ADB=\angle ACB=35^\circ$ (same segment), and $\angle AOB=2\times35^\circ=70^\circ$.
:::

::: example Semicircle
**Problem.** $AB$ is a diameter and $C$ is a point on the circle with $\angle CAB=35^\circ$. Find $\angle ABC$.

**Solution.** $\angle ACB=90^\circ$ (angle in a semicircle). In $\Delta ABC$: $\angle ABC=180^\circ-90^\circ-35^\circ=55^\circ$.
:::

::: example Finding a diameter
**Problem.** A right-angled triangle has sides 6 cm, 8 cm and 10 cm. Find the radius of the circle through its three vertices.

**Solution.** The right angle is at the circumference, so the hypotenuse is a diameter: $2r=10$ and $r=5$ cm.
:::

### Cyclic quadrilaterals

```figure caption="Cyclic quadrilateral ABCD. The opposite angles A and C (and B and D) add up to 180°, and each exterior angle equals the interior opposite angle."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4, 3.6))
def pt(d): return np.array([np.cos(np.radians(d)), np.sin(np.radians(d))])
t = np.linspace(0, 2*np.pi, 300)
ax.plot(np.cos(t), np.sin(t), color=INK, lw=1.2)
A, B, C, D, O = pt(120), pt(210), pt(330), pt(60), np.array([0, 0.])
Q = [A, B, C, D, A]
ax.plot([p[0] for p in Q], [p[1] for p in Q], color=INK, lw=1.3)
ax.plot([A[0], C[0]], [A[1], C[1]], color=MUTED, lw=0.8, ls='--')
ax.plot([B[0], D[0]], [B[1], D[1]], color=MUTED, lw=0.8, ls='--')
for P, tt, dx, dy in [(A, 'A', -0.17, 0.05), (B, 'B', -0.17, -0.12), (C, 'C', 0.05, -0.12), (D, 'D', 0.05, 0.05)]:
    ax.text(P[0] + dx, P[1] + dy, tt, fontsize=9)
ax.text(-0.38, 0.56, '105°', fontsize=8, color='#dc2626', ha='center')
ax.text(0.5, -0.62, '75°', fontsize=8, color='#dc2626', ha='center')
ax.set_xlim(-1.35, 1.35); ax.set_ylim(-1.3, 1.3); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: derivation Opposite angles of a cyclic quadrilateral are supplementary
**Given.** $ABCD$ is a cyclic quadrilateral in a circle with centre $O$.

**To prove.** $\angle A+\angle C=180^\circ$ and $\angle B+\angle D=180^\circ$.

**Construction.** Join $OB$ and $OD$.

**Proof.**

**Step 1 — two central angles.** The arc $BCD$ and the arc $DAB$ together make the whole circle, so the angles at the centre on them add up to a full turn:

$$ \angle BOD\ (\text{on arc } BCD)+\text{reflex}\ \angle BOD\ (\text{on arc } DAB)=360^\circ $$

**Step 2 — halve each.** The angle at the circumference is half the angle at the centre on the same arc: $\angle A=\frac{1}{2}\angle BOD$ (arc $BCD$) and $\angle C=\frac{1}{2}\,\text{reflex}\angle BOD$ (arc $DAB$).

**Step 3 — add.**

$$ \angle A+\angle C=\frac{1}{2}\left(\angle BOD+\text{reflex}\,\angle BOD\right)=\frac{1}{2}\times360^\circ=180^\circ $$

**Result.** $\angle A+\angle C=180^\circ$. Similarly $\angle B+\angle D=180^\circ$. Proved.

**Corollary.** Extend $BC$ to $E$. Then $\angle DCE=180^\circ-\angle BCD=\angle A$: the **exterior angle** of a cyclic quadrilateral equals the interior opposite angle.
:::

::: example Opposite angles
**Problem.** In a cyclic quadrilateral $ABCD$, $\angle A=105^\circ$ and $\angle B=75^\circ$. Find $\angle C$ and $\angle D$.

**Solution.** $\angle C=180^\circ-105^\circ=75^\circ$ and $\angle D=180^\circ-75^\circ=105^\circ$.
:::

::: example Algebra and angles
**Problem.** The opposite angles of a cyclic quadrilateral are $(2x+10)^\circ$ and $(3x-5)^\circ$. Find $x$ and the two angles.

**Solution.** They are supplementary: $(2x+10)+(3x-5)=180$, so $5x+5=180$ and $x=35$. The angles are $2(35)+10=80^\circ$ and $3(35)-5=100^\circ$. Check: $80+100=180$ ✓.
:::

::: example Exterior angle
**Problem.** $ABCD$ is cyclic and the side $BC$ is produced to $E$. If $\angle DCE=78^\circ$, find $\angle A$. If also $\angle B=64^\circ$, find $\angle D$.

**Solution.** The exterior angle equals the interior opposite angle: $\angle A=\angle DCE=78^\circ$. Opposite angles add to $180^\circ$: $\angle D=180^\circ-64^\circ=116^\circ$.
:::

::: example Is it cyclic?
**Problem.** In quadrilateral $PQRS$, $\angle P=98^\circ$ and $\angle R=82^\circ$. Can a circle pass through all four vertices?

**Solution.** $98^\circ+82^\circ=180^\circ$: opposite angles are supplementary, so $PQRS$ is cyclic (converse of the theorem). Yes.
:::

### Tangents

A **tangent** touches the circle at one point, the **point of contact**. Two facts are used constantly.

::: key Tangent theorems
1. The tangent at a point is **perpendicular to the radius** through the point of contact.
2. The two tangents drawn to a circle from an external point are **equal in length**, and the line from the point to the centre bisects the angle between them.
3. **Alternate segment theorem:** the angle between a tangent and a chord at the point of contact equals the angle in the alternate segment.
4. **Tangent–secant:** $PT^2=PA\times PB$, where $PT$ is a tangent and $PAB$ a secant through $P$.
:::

```figure caption="Tangents PA and PB from an external point P to a circle with centre O. OA ⊥ PA and OB ⊥ PB; PA = PB."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8, 3.4))
t = np.linspace(0, 2*np.pi, 300)
ax.plot(np.cos(t), np.sin(t), color=INK, lw=1.3)
d = 2.6
phi = np.arccos(1 / d)
O = np.array([0, 0.]); P = np.array([d, 0.])
A = np.array([np.cos(phi), np.sin(phi)]); B = np.array([np.cos(phi), -np.sin(phi)])
for X, Y, c in [(P, A, INK), (P, B, INK), (O, A, MUTED), (O, B, MUTED), (O, P, MUTED)]:
    ax.plot([X[0], Y[0]], [X[1], Y[1]], color=c, lw=1.2, ls='-' if c == INK else '--')
ax.plot([A[0], B[0]], [A[1], B[1]], color=ACCENT, lw=0.9, ls=':')
for X, tt, dx, dy in [(O, 'O', -0.15, -0.08), (P, 'P', 0.08, -0.05), (A, 'A', -0.05, 0.1), (B, 'B', -0.05, -0.22)]:
    ax.text(X[0] + dx, X[1] + dy, tt, fontsize=9)
ax.text(1.5, 0.55, '∠ APB', fontsize=8, ha='center', color='#dc2626')
ax.text(0.05, 0.5, 'r', fontsize=8.5, color=MUTED)
ax.set_xlim(-1.3, 3.1); ax.set_ylim(-1.45, 1.45); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: derivation Two tangents from an external point are equal
**Given.** $PA$ and $PB$ are tangents from $P$ to a circle with centre $O$, touching at $A$ and $B$.

**To prove.** $PA=PB$ and $\angle APO=\angle BPO$.

**Construction.** Join $OA$, $OB$ and $OP$.

**Proof.** In $\Delta OAP$ and $\Delta OBP$:

- $\angle OAP=\angle OBP=90^\circ$ (tangent $\perp$ radius),
- $OA=OB$ (radii of the same circle),
- $OP$ is common (hypotenuse).

So $\Delta OAP\cong\Delta OBP$ by RHS. Therefore $PA=PB$ and $\angle APO=\angle BPO$. Proved.
:::

::: example Length of a tangent
**Problem.** $P$ is 13 cm from the centre of a circle of radius 5 cm. Find the length of the tangent from $P$.

**Solution.** $OA\perp PA$, so in right-angled $\Delta OAP$: $PA^2=OP^2-OA^2=169-25=144$, hence $PA=12$ cm.
:::

::: example Angle between tangents
**Problem.** Tangents $PA$ and $PB$ meet at $P$ with $\angle APB=50^\circ$. Find $\angle PAB$ and $\angle AOB$.

**Solution.** $PA=PB$, so $\Delta PAB$ is isosceles: $\angle PAB=\frac{180^\circ-50^\circ}{2}=65^\circ$. In the quadrilateral $OAPB$: $\angle OAP=\angle OBP=90^\circ$, so $\angle AOB=360^\circ-90^\circ-90^\circ-50^\circ=130^\circ$ (equivalently $180^\circ-50^\circ$).
:::

::: example Perimeter of a triangle round a circle
**Problem.** From a point $P$, 10 cm from the centre of a circle of radius 6 cm, two tangents $PA$ and $PB$ are drawn. Find the length $PA$ and the area of the quadrilateral $OAPB$.

**Solution.** $PA=\sqrt{10^2-6^2}=8$ cm. The quadrilateral is two right triangles, each of area $\frac{1}{2}\times6\times8=24$, so the area is $48\text{ cm}^2$.
:::

```figure caption="Alternate segment theorem: the angle between the tangent TA and the chord AB (40°) equals the angle ACB in the alternate segment."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Arc
fig, ax = plt.subplots(figsize=(4.6, 3.8))
def pt(d): return np.array([np.cos(np.radians(d)), np.sin(np.radians(d))])
t = np.linspace(0, 2*np.pi, 300)
ax.plot(np.cos(t), np.sin(t), color=INK, lw=1.3)
A = pt(270); B = pt(270 + 160 - 0)
B = pt(190)
C = pt(60)
ax.plot([-1.6, 1.6], [-1, -1], color=INK, lw=1.2)
for X, Y in [(A, B), (C, A), (C, B)]:
    ax.plot([X[0], Y[0]], [X[1], Y[1]], color=INK, lw=1.1)
ax.text(A[0] + 0.05, A[1] - 0.2, 'A', fontsize=9)
ax.text(B[0] - 0.2, B[1] + 0.02, 'B', fontsize=9)
ax.text(C[0] + 0.06, C[1] + 0.04, 'C', fontsize=9)
ax.text(-1.58, -0.9, 'T', fontsize=9)
ax.text(-0.45, -0.88, '40°', fontsize=8, color='#dc2626', ha='center')
ax.text(C[0] - 0.15, C[1] - 0.3, '40°', fontsize=8, color='#dc2626', ha='center')
ax.set_xlim(-1.75, 1.75); ax.set_ylim(-1.35, 1.3); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: example Alternate segment
**Problem.** $TA$ is a tangent at $A$ and $AB$ is a chord with $\angle TAB=40^\circ$. Find the angle $\angle ACB$ at a point $C$ of the alternate segment and the central angle $\angle AOB$.

**Solution.** $\angle ACB=\angle TAB=40^\circ$ (alternate segment theorem). Then $\angle AOB=2\times40^\circ=80^\circ$. Since $OA=OB$, $\angle OAB=\frac{180-80}{2}=50^\circ$, and $\angle TAB+\angle OAB=40+50=90^\circ=\angle TAO$, which agrees with tangent $\perp$ radius. ✓
:::

::: example Tangent and secant
**Problem.** From $P$ a tangent $PT=6$ cm and a secant $PAB$ are drawn, with $PA=4$ cm. Find $PB$ and the chord $AB$.

**Solution.** $PT^2=PA\times PB$, so $36=4\times PB$ and $PB=9$ cm. Then $AB=PB-PA=9-4=5$ cm.
:::

::: caution Common mistakes
- Calling an angle "at the centre" when its vertex is on the circle (or the opposite).
- Using the theorem on the **wrong arc**: the angle at the circumference is half the central angle *on the same arc*.
- Writing a statement without a reason; each line of a proof needs "because …".
- Forgetting that the tangent is perpendicular to the **radius**, not the chord.
- Taking $PA^2=OP^2+OA^2$ — it is a *difference*, since $OP$ is the hypotenuse.
:::

## 15.2 Exercises of the SEE type

### Method for any question

1. Draw a large clear figure; mark the centre $O$ and every given angle.
2. List the facts available: radii equal; angle at centre $=2\times$ angle at circumference; same segment; semicircle $90^\circ$; cyclic quadrilateral supplementary; tangent $\perp$ radius.
3. Work step by step, writing the reason beside each angle ("angle in a semicircle", "isosceles triangle").
4. For a proof, state **Given, To prove, Construction, Proof** and finish with "Proved".
5. For algebraic angles, form an equation, solve it, and check that all angles are positive.

::: example SEE type: mixed angles
**Problem.** $AB$ is a diameter of a circle and $C$ is a point on the circle. $D$ is a point on the arc so that $ABCD$ is cyclic and $\angle ABC=50^\circ$. Find $\angle BAC$ and $\angle ADC$.

**Solution.** $\angle ACB=90^\circ$ (semicircle), so $\angle BAC=180^\circ-90^\circ-50^\circ=40^\circ$. In the cyclic quadrilateral $ABCD$, opposite angles $B$ and $D$ add to $180^\circ$: $\angle ADC=180^\circ-50^\circ=130^\circ$.
:::

::: example SEE type: prove
**Problem.** Prove that the tangents drawn to a circle from an external point are equal in length.

**Solution.** Draw the figure with $O,A,B,P$; join $OA$, $OB$, $OP$. In $\Delta OAP$ and $\Delta OBP$, $\angle OAP=\angle OBP=90^\circ$ (tangent $\perp$ radius), $OA=OB$ (radii), and $OP$ is common. So the triangles are congruent (RHS) and $PA=PB$. Proved.
:::

::: example SEE type: algebra with tangents
**Problem.** Tangents $PA$ and $PB$ are drawn from $P$ to a circle with centre $O$ and radius 8 cm. If $\angle AOB=120^\circ$, find $\angle APB$ and the length $OP$.

**Solution.** In quadrilateral $OAPB$ two angles are $90^\circ$, so $\angle APB=180^\circ-120^\circ=60^\circ$. $OP$ bisects $\angle AOB$ so $\angle AOP=60^\circ$ and in right-angled $\Delta OAP$, $\cos60^\circ=\frac{OA}{OP}$. Hence $OP=\frac{8}{0.5}=16$ cm.
:::

## Chapter summary

- Angle at the centre $=2\times$ angle at the circumference on the same arc.
- Angles in the same segment are equal.
- Angle in a semicircle $=90^\circ$; the hypotenuse of a right triangle is a diameter of its circumcircle.
- Cyclic quadrilateral: opposite angles add to $180^\circ$; exterior angle = interior opposite angle.
- Tangent $\perp$ radius; tangent length $=\sqrt{OP^2-r^2}$; two tangents from a point are equal.
- Alternate segment theorem; tangent–secant $PT^2=PA\times PB$.
- Chord of length $2c$ at distance $d$: $r^2=c^2+d^2$.
- A good proof: Given, To prove, Construction, Proof, with a reason for each step.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The angle at the centre of a circle is $80^\circ$. The angle at the circumference on the same arc is <span class="marks">[1]</span>
   (a) $160^\circ$ (b) $80^\circ$ (c) $40^\circ$ (d) $20^\circ$
2. The angle in a semicircle is <span class="marks">[1]</span>
   (a) $45^\circ$ (b) $60^\circ$ (c) $90^\circ$ (d) $180^\circ$
3. In a cyclic quadrilateral $ABCD$, $\angle A=70^\circ$. Then $\angle C$ is <span class="marks">[1]</span>
   (a) $70^\circ$ (b) $110^\circ$ (c) $20^\circ$ (d) $140^\circ$
4. A tangent is perpendicular to the <span class="marks">[1]</span>
   (a) chord (b) radius at the point of contact (c) diameter parallel to it (d) secant
5. The length of the tangent from a point 5 cm from the centre of a circle of radius 3 cm is <span class="marks">[1]</span>
   (a) 2 cm (b) 4 cm (c) 8 cm (d) 34 cm

::: note Answers to Group A
**1.** (c) — half of $80^\circ$.
**2.** (c).
**3.** (b) — $180-70$.
**4.** (b).
**5.** (b) — $\sqrt{25-9}=4$.
:::

**Group B — Short answer (2 marks each)**

1. $\angle AOB=130^\circ$ at the centre. Find $\angle ACB$ at the circumference (major arc). <span class="marks">[2]</span>
2. The opposite angles of a cyclic quadrilateral are $(x+30)^\circ$ and $(2x+15)^\circ$. Find $x$. <span class="marks">[2]</span>
3. A chord 10 cm long is 12 cm from the centre of a circle. Find the radius. <span class="marks">[2]</span>
4. $PT$ is a tangent of length 12 cm from $P$, and $OP=13$ cm. Find the radius. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $65^\circ$.
**2.** $(x+30)+(2x+15)=180$, $3x=135$, $x=45$.
**3.** Half-chord 5; $r=\sqrt{25+144}=13$ cm.
**4.** $r=\sqrt{13^2-12^2}=5$ cm.
:::

**Group C — Short answer (3 marks each)**

1. Prove that the angle in a semicircle is a right angle. <span class="marks">[3]</span>
2. In a circle with centre $O$, $\angle OAB=25^\circ$, where $AB$ is a chord. Find $\angle AOB$ and the angle at the major arc. <span class="marks">[3]</span>
3. $PA$ and $PB$ are tangents from $P$ and $\angle APB=50^\circ$. Find $\angle PAB$ and $\angle AOB$. <span class="marks">[3]</span>
4. A tangent $PT=6$ cm and a secant $PAB$ with $PA=4$ cm are drawn. Find $AB$. <span class="marks">[3]</span>

::: note Answers to Group C
**1.** The angle at the centre on a diameter is $180^\circ$; the angle at the circumference is half: $90^\circ$.
**2.** $\angle AOB=180-50=130^\circ$; angle at circumference $65^\circ$.
**3.** $\angle PAB=65^\circ$, $\angle AOB=130^\circ$.
**4.** $PB=\frac{36}{4}=9$, $AB=9-4=5$ cm.
:::

**Group D — Long answer (4 marks each)**

1. Prove that the angle at the centre of a circle is twice the angle at the circumference on the same arc. <span class="marks">[4]</span>
2. Prove that the opposite angles of a cyclic quadrilateral are supplementary. <span class="marks">[4]</span>
3. Prove that the two tangents from an external point to a circle are equal. <span class="marks">[4]</span>
4. $P$ is 10 cm from the centre of a circle of radius 6 cm. Tangents $PA$ and $PB$ are drawn. Find $PA$, the area of quadrilateral $OAPB$, and $\angle APB$ (to the nearest degree). <span class="marks">[4]</span>

::: note Answers to Group D
**1.** See the derivation (join $CO$ produced to $D$; exterior angles of the isosceles triangles $OAC$ and $OBC$).
**2.** See the derivation (the two angles at the centre make $360^\circ$).
**3.** See the derivation (RHS congruence of $\Delta OAP$ and $\Delta OBP$).
**4.** $PA=\sqrt{100-36}=8$ cm; area $=2\times\frac{1}{2}\times6\times8=48\text{ cm}^2$; $\sin(\frac{1}{2}\angle APB)=\frac{6}{10}=0.6$, so $\frac{1}{2}\angle APB\approx36.87^\circ$ and $\angle APB\approx74^\circ$.
:::
