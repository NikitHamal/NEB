---
subject: Physics
grade: 11
unit: 2
title: Vectors
hours: 4
area: Mechanics
---

Some physical quantities are fully described by a number and a unit — mass,
time, temperature. Others are useless until you also say *which way*: a force of
10 N pushing north is not the force of 10 N pushing south. Quantities of the
second kind are **vectors**, and they obey their own arithmetic. This unit builds
that arithmetic: how vectors add, how they are broken into components, and the
two ways of multiplying them. Every later unit — dynamics, circular motion,
gravitation, fields — is written in this language.

::: key The one idea behind the whole unit
Vectors never add arithmetically. $3 + 4$ is $7$ only if the two vectors point
the same way; it is $5$ if they are perpendicular and $1$ if they are opposite.
Adding vectors means adding *displacements drawn head to tail*, and the fastest
safe way to do that is always to resolve into components.
:::

## 2.1 Triangle, parallelogram and polygon laws of vectors

A **scalar** has magnitude only and obeys ordinary algebra (mass, speed, work,
energy, charge, temperature). A **vector** has magnitude *and* direction and
obeys the laws of this section (displacement, velocity, acceleration, force,
momentum, torque). A vector is drawn as an arrow whose length, to some scale,
is the magnitude and whose arrowhead gives the direction. It is written
$\vec{A}$, and its magnitude as $A$ or $|\vec{A}|$.

| Type of vector | Meaning |
|---|---|
| Equal vectors | same magnitude **and** same direction, wherever they are drawn |
| Negative vector | same magnitude, exactly opposite direction |
| Unit vector | magnitude exactly 1; only carries direction |
| Null (zero) vector | magnitude zero, direction indeterminate |
| Collinear vectors | act along the same line or parallel lines |
| Coplanar vectors | all lie in one plane |
| Position vector | drawn from a chosen origin to the point |

### Triangle law of vector addition

::: definition Triangle law
If two vectors are represented in magnitude and direction by the two sides of a
triangle taken in order, then their resultant is represented in magnitude and
direction by the third side of the triangle taken in the opposite order.
:::

So to add $\vec{P}$ and $\vec{Q}$ you draw $\vec{P}$, then start $\vec{Q}$ at the
head of $\vec{P}$; the arrow from the tail of $\vec{P}$ to the head of $\vec{Q}$
is $\vec{R} = \vec{P} + \vec{Q}$. Because the same third side results whichever
vector is drawn first, vector addition is **commutative**,
$\vec{P} + \vec{Q} = \vec{Q} + \vec{P}$, and it is also **associative**,
$(\vec{P} + \vec{Q}) + \vec{S} = \vec{P} + (\vec{Q} + \vec{S})$.

### Parallelogram law of vector addition

::: definition Parallelogram law
If two vectors acting simultaneously at a point are represented in magnitude and
direction by the two adjacent sides of a parallelogram drawn from that point,
their resultant is represented in magnitude and direction by the diagonal of the
parallelogram drawn from the same point.
:::

```figure caption="Parallelogram law. $OC$ is the resultant of $\vec{P}$ and $\vec{Q}$; the perpendicular $CD$ dropped on $OA$ produced supplies the derivation."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Arc
fig, ax = plt.subplots(figsize=(4.8, 3.0))
O = np.array([0.0, 0.0]); P = np.array([4.4, 0.0])
th = np.radians(55); Q = 3.0 * np.array([np.cos(th), np.sin(th)])
C = P + Q; D = np.array([C[0], 0.0])
def arrow(a, b, c, lw=1.8):
    ax.annotate('', xy=b, xytext=a, arrowprops=dict(arrowstyle='-|>', color=c,
                lw=lw, shrinkA=0, shrinkB=0, mutation_scale=13))
arrow(O, P, ACCENT); arrow(O, Q, '#2e8b57'); arrow(O, C, '#d9534f')
ax.plot([Q[0], C[0]], [Q[1], C[1]], color=MUTED, lw=1.0, ls='--')
ax.plot([P[0], C[0]], [P[1], C[1]], color=MUTED, lw=1.0, ls='--')
ax.plot([P[0], D[0]], [0, 0], color=MUTED, lw=1.0, ls=':')
ax.plot([C[0], D[0]], [C[1], 0], color=MUTED, lw=1.0, ls=':')
s = 0.22
ax.plot([D[0]-s, D[0]-s, D[0]], [0, s, s], color=MUTED, lw=0.9)
ax.add_patch(Arc(O, 1.9, 1.9, theta1=0, theta2=55, color=INK, lw=0.9))
ax.add_patch(Arc(O, 3.0, 3.0, theta1=0, theta2=np.degrees(np.arctan2(C[1], C[0])),
                 color='#d9534f', lw=0.9))
# angle labels: theta sits between OC and OB, alpha between OA and OC, both
# clear of every stroke
ta = np.radians(38.0); aa = np.radians(11.0)
ax.annotate(r'$\theta$', (1.28*np.cos(ta), 1.28*np.sin(ta)), ha='center',
            va='center', color=INK, fontsize=10)
ax.annotate(r'$\alpha$', (1.98*np.cos(aa), 1.98*np.sin(aa)), ha='center',
            va='center', color='#d9534f', fontsize=10)
lab = [(P/2, r'$\vec{P}$', (0, -14), ACCENT), (Q/2, r'$\vec{Q}$', (-20, 0), '#2e8b57'),
       (C/2, r'$\vec{R}$', (-4, 12), '#d9534f'),
       (O, 'O', (-11, -11), INK), (P, 'A', (-2, -14), INK),
       (Q, 'B', (-13, 2), INK), (C, 'C', (5, 2), INK), (D, 'D', (2, -13), INK)]
for pt, t, off, c in lab:
    ax.annotate(t, pt, textcoords='offset points', xytext=off, color=c, fontsize=10)
ax.set_xlim(-0.9, 7.4); ax.set_ylim(-0.9, 3.4); ax.set_aspect('equal'); ax.axis('off')
```
::: derivation Magnitude and direction of the resultant of two vectors
We start from the parallelogram of the figure — two vectors $\vec{P}$ and
$\vec{Q}$ drawn from the same point $O$ with angle $\theta$ between them — and we
finish with a formula for how long the diagonal is and which way it points.

**Setting up.** Let $\vec{P} = \vec{OA}$ and $\vec{Q} = \vec{OB}$, with
$\angle AOB = \theta$. Complete the parallelogram $OACB$, so the diagonal
$\vec{OC} = \vec{R}$ is the resultant. Extend the line $OA$ forwards and drop a
perpendicular from $C$ onto it, meeting it at $D$. We now have two right-angled
triangles to work with, $ADC$ and $ODC$.

**Step 1 — the side $AC$ equals $Q$.** In a parallelogram opposite sides are equal
and parallel, so $AC$ is equal in length to $OB$ and points the same way:

$$ AC = OB = Q $$

Because $AC$ is parallel to $OB$, the angle $CAD$ that $AC$ makes with the
extended line $OA$ is also $\theta$ (corresponding angles).

**Step 2 — split $AC$ into its two perpendicular parts.** Triangle $ADC$ has a
right angle at $D$, with hypotenuse $AC = Q$ and angle $\theta$ at $A$. Ordinary
trigonometry ($\cos = $ adjacent/hypotenuse, $\sin = $ opposite/hypotenuse) gives

$$ AD = AC\cos\theta = Q\cos\theta, \qquad DC = AC\sin\theta = Q\sin\theta $$

**Step 3 — find the whole base $OD$.** The point $D$ lies beyond $A$, so the base
is made of two pieces laid end to end:

$$ OD = OA + AD $$

Put in $OA = P$ and $AD = Q\cos\theta$ from Step 2:

$$ OD = P + Q\cos\theta $$

**Step 4 — use Pythagoras in triangle $ODC$.** This triangle is right-angled at
$D$ and its hypotenuse is exactly the resultant $OC = R$:

$$ R^{2} = OD^{2} + DC^{2} $$

Substitute the two sides we found:

$$ R^{2} = (P + Q\cos\theta)^{2} + (Q\sin\theta)^{2} $$

**Step 5 — expand the first bracket.** Using $(x+y)^{2} = x^{2} + 2xy + y^{2}$:

$$ R^{2} = P^{2} + 2PQ\cos\theta + Q^{2}\cos^{2}\theta + Q^{2}\sin^{2}\theta $$

**Step 6 — collect the two $Q^{2}$ terms.** They share a factor $Q^{2}$:

$$ R^{2} = P^{2} + 2PQ\cos\theta + Q^{2}(\cos^{2}\theta + \sin^{2}\theta) $$

**Step 7 — use the identity.** For any angle, $\sin^{2}\theta + \cos^{2}\theta = 1$,
so the bracket is simply 1:

$$ R^{2} = P^{2} + Q^{2} + 2PQ\cos\theta $$

**Step 8 — take the square root.** A magnitude is never negative, so we keep the
positive root:

$$ R = \sqrt{P^{2} + Q^{2} + 2PQ\cos\theta} $$

**Step 9 — the direction.** Let $\alpha$ be the angle between $\vec{R}$ and
$\vec{P}$, i.e. $\angle COD$ in the right triangle $ODC$. Then
$\tan\alpha = $ opposite/adjacent:

$$ \tan\alpha = \frac{DC}{OD} $$

Substitute $DC = Q\sin\theta$ and $OD = P + Q\cos\theta$:

$$ \tan\alpha = \frac{Q\sin\theta}{P + Q\cos\theta} $$

Finally take the inverse tangent of both sides:

$$ \alpha = \tan^{-1}\left(\frac{Q\sin\theta}{P + Q\cos\theta}\right) $$

**Result.**

$$ R = \sqrt{P^{2} + Q^{2} + 2PQ\cos\theta}, \qquad
\tan\alpha = \frac{Q\sin\theta}{P + Q\cos\theta} $$

**What it means.** The single vector $\vec{R}$ has exactly the same effect as
$\vec{P}$ and $\vec{Q}$ acting together. The whole answer depends on the angle
between them, not on their magnitudes alone — so "3 N and 4 N" has no single
resultant until you are told $\theta$.

**Assumptions used.** Both vectors act at the **same point** (they are concurrent)
and they are the same kind of quantity (you may not add a force to a velocity).
$\alpha$ is measured from $\vec{P}$; measuring from $\vec{Q}$ instead swaps $P$
and $Q$ in the direction formula.
:::

::: derivation When is the resultant largest and smallest?
We start from the result just derived and reach the two extreme cases NEB likes
to ask about.

In $R = \sqrt{P^{2}+Q^{2}+2PQ\cos\theta}$, the only part that can change if $P$
and $Q$ are fixed is $\cos\theta$. So $R$ is largest when $\cos\theta$ is largest
and smallest when $\cos\theta$ is smallest.

For any angle, $\cos\theta$ can never be more than $+1$ and never less than $-1$.

**Largest.** Put $\cos\theta = +1$, which happens at $\theta = 0^{\circ}$ (the two
vectors point the same way):

$$ R_{\max} = \sqrt{P^{2} + Q^{2} + 2PQ} $$

The quantity under the root is a perfect square, $(P+Q)^{2}$:

$$ R_{\max} = \sqrt{(P+Q)^{2}} = P + Q $$

**Smallest.** Put $\cos\theta = -1$, which happens at $\theta = 180^{\circ}$ (the
vectors point in opposite directions):

$$ R_{\min} = \sqrt{P^{2} + Q^{2} - 2PQ} $$

Again the inside is a perfect square, $(P-Q)^{2}$:

$$ R_{\min} = \sqrt{(P-Q)^{2}} = |P - Q| $$

**Result.** $R$ always lies between $|P-Q|$ and $P+Q$.

**What it means.** Two 3 N and 4 N pulls can give anything from 1 N to 7 N. The
modulus sign matters: a magnitude cannot be negative, so if $Q > P$ the answer is
$Q - P$.
:::

::: tip The examiner is looking for
For the 5-mark parallelogram-law question: (i) statement of the law; (ii) a
labelled parallelogram with the perpendicular $CD$ drawn and $O$, $A$, $B$, $C$,
$D$ marked; (iii) $AD = Q\cos\theta$ and $DC = Q\sin\theta$ written down;
(iv) Pythagoras in $ODC$; (v) the identity $\sin^{2}\theta+\cos^{2}\theta=1$ used
*visibly*; (vi) both final boxed formulas — magnitude **and** direction. Leaving
out the direction formula costs a full mark every time.
:::

| Angle $\theta$ between them | Resultant $R$ | Note |
|---|---|---|
| $0^{\circ}$ | $P + Q$ | maximum possible |
| $90^{\circ}$ | $\sqrt{P^{2}+Q^{2}}$ | $\tan\alpha = Q/P$ |
| $180^{\circ}$ | $P - Q$ in magnitude | minimum possible |
| $120^{\circ}$ with $P = Q$ | $P$ | three equal vectors at $120^{\circ}$ give zero |

::: caution Never add magnitudes
A body pulled by 3 N and 4 N does not feel 7 N unless the pulls are parallel.
The resultant of 3 N and 4 N can be anything from 1 N to 7 N. Always ask for the
angle first.
:::

::: example Worked example 2.1
**Problem.** Two forces of $5\ \text{N}$ and $3\ \text{N}$ act at a point with an
angle of $60^{\circ}$ between them. Find the magnitude and direction of their
resultant.

**Solution.** With $P = 5\ \text{N}$, $Q = 3\ \text{N}$, $\theta = 60^{\circ}$ and
$\cos 60^{\circ} = 0.5$:

$$ R = \sqrt{5^{2} + 3^{2} + 2(5)(3)(0.5)} = \sqrt{25 + 9 + 15} = \sqrt{49} = 7\ \text{N} $$

For the direction, with $\sin 60^{\circ} = 0.866$:

$$ \tan\alpha = \frac{3(0.866)}{5 + 3(0.5)} = \frac{2.598}{6.5} = 0.3997 $$

so $\alpha = 21.8^{\circ}$. The resultant is $7\ \text{N}$ acting at $21.8^{\circ}$
to the $5\ \text{N}$ force.
:::

### Polygon law and subtraction

::: definition Polygon law
If a number of vectors are represented in magnitude and direction by the sides
of an open polygon taken in order, their resultant is represented by the closing
side of the polygon taken in the opposite order.
:::

It follows that if the polygon **closes**, the resultant is zero — which is
exactly the condition for a set of concurrent forces to be in equilibrium.

```figure caption="Polygon law: four vectors drawn head to tail, with the closing side (red) as the resultant. If the last head met the first tail, the resultant would be zero."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4, 3.2))
v = [np.array([2.6, 0.5]), np.array([1.2, 1.7]), np.array([-1.9, 1.0]),
     np.array([1.3, -1.5])]
pts = [np.array([0.0, 0.0])]
for x in v:
    pts.append(pts[-1] + x)
names = [r'$\vec{A}$', r'$\vec{B}$', r'$\vec{C}$', r'$\vec{D}$']
cols = [ACCENT, '#2e8b57', '#b8860b', '#6a5acd']
# each label parked on the free side of its own arrow, clear of the others
labpos = [(1.36, -0.14), (3.58, 1.10), (3.06, 3.04), (2.22, 2.18)]
for i, x in enumerate(v):
    a, b = pts[i], pts[i + 1]
    ax.annotate('', xy=b, xytext=a, arrowprops=dict(arrowstyle='-|>', color=cols[i],
                lw=1.7, shrinkA=0, shrinkB=0, mutation_scale=12))
    ax.annotate(names[i], labpos[i], ha='center', va='center',
                color=cols[i], fontsize=10)
ax.annotate('', xy=pts[-1], xytext=pts[0], arrowprops=dict(arrowstyle='-|>',
            color='#d9534f', lw=2.0, shrinkA=0, shrinkB=0, mutation_scale=13))
ax.annotate(r'$\vec{R}$', (1.40, 1.14), ha='center', va='center',
            color='#d9534f', fontsize=10.5)
ax.set_xlim(-0.5, 4.3); ax.set_ylim(-0.6, 3.5); ax.set_aspect('equal'); ax.axis('off')
```
Subtraction is addition of the negative vector:

$$ \vec{P} - \vec{Q} = \vec{P} + (-\vec{Q}), \qquad
|\vec{P} - \vec{Q}| = \sqrt{P^{2} + Q^{2} - 2PQ\cos\theta} $$

## 2.2 Resolution of vectors; Unit vectors

Resolution is the reverse of addition: replacing one vector by two (or three)
vectors that together have the same effect. The useful choice is always two
**mutually perpendicular** components, because perpendicular components never
interfere with each other.

```figure caption="Rectangular resolution. $A_x = A\cos\theta$ and $A_y = A\sin\theta$ are the sides of the right triangle whose hypotenuse is $\vec{A}$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Arc
fig, ax = plt.subplots(figsize=(4.2, 2.7))
th = np.radians(38); A = 4.2 * np.array([np.cos(th), np.sin(th)])
ax.annotate('', xy=(5.2, 0), xytext=(-0.5, 0), arrowprops=dict(arrowstyle='-|>',
            color=MUTED, lw=1.0, shrinkA=0, shrinkB=0, mutation_scale=10))
ax.annotate('', xy=(0, 3.4), xytext=(0, -0.5), arrowprops=dict(arrowstyle='-|>',
            color=MUTED, lw=1.0, shrinkA=0, shrinkB=0, mutation_scale=10))
ax.annotate('', xy=A, xytext=(0, 0), arrowprops=dict(arrowstyle='-|>', color='#d9534f',
            lw=2.0, shrinkA=0, shrinkB=0, mutation_scale=13))
ax.annotate('', xy=(A[0], 0), xytext=(0, 0), arrowprops=dict(arrowstyle='-|>',
            color=ACCENT, lw=1.8, shrinkA=0, shrinkB=0, mutation_scale=12))
ax.annotate('', xy=(0, A[1]), xytext=(0, 0), arrowprops=dict(arrowstyle='-|>',
            color='#2e8b57', lw=1.8, shrinkA=0, shrinkB=0, mutation_scale=12))
ax.plot([A[0], A[0]], [0, A[1]], color=MUTED, lw=0.9, ls=':')
ax.plot([0, A[0]], [A[1], A[1]], color=MUTED, lw=0.9, ls=':')
s = 0.2
ax.plot([A[0]-s, A[0]-s, A[0]], [0, s, s], color=MUTED, lw=0.8)
ax.add_patch(Arc((0, 0), 1.7, 1.7, theta1=0, theta2=38, color=INK, lw=0.9))
ax.annotate(r'$\theta$', (1.0, 0.24), color=INK, fontsize=10)
ax.annotate(r'$\vec{A}$', A / 2, textcoords='offset points', xytext=(-6, 10),
            color='#d9534f', fontsize=11)
ax.annotate(r'$A_x = A\cos\theta$', (A[0] / 2, -0.10), ha='center', va='top',
            color=ACCENT, fontsize=9.5)
ax.annotate(r'$A_y = A\sin\theta$', (-0.15, A[1] / 2), ha='right', va='center',
            color='#2e8b57', fontsize=9.5, rotation=90)
ax.set_xlim(-1.9, 5.4); ax.set_ylim(-0.9, 3.6); ax.set_aspect('equal'); ax.axis('off')
```

If $\vec{A}$ makes an angle $\theta$ with the $x$-axis, the right triangle gives

$$ A_x = A\cos\theta, \qquad A_y = A\sin\theta $$

and going back the other way,

$$ A = \sqrt{A_x^{2} + A_y^{2}}, \qquad \tan\theta = \frac{A_y}{A_x} $$

::: tip Resolve, add, recombine
To add any number of vectors: resolve each one into $x$ and $y$ components, add
the components separately to get $R_x = \sum A_x$ and $R_y = \sum A_y$, then
$R = \sqrt{R_x^{2} + R_y^{2}}$ and $\tan\theta = R_y/R_x$. This method never
fails, however many vectors there are.
:::

### Unit vectors

::: definition Unit vector
A unit vector is a vector of magnitude one that specifies a direction only. The
unit vector along $\vec{A}$ is

$$ \hat{A} = \frac{\vec{A}}{|\vec{A}|}, \qquad \text{so} \qquad \vec{A} = A\,\hat{A} $$
:::

The unit vectors along the $x$, $y$ and $z$ axes of a right-handed set are
written $\hat{i}$, $\hat{j}$ and $\hat{k}$. Any vector in space is then

$$ \vec{A} = A_x\hat{i} + A_y\hat{j} + A_z\hat{k}, \qquad
A = \sqrt{A_x^{2} + A_y^{2} + A_z^{2}} $$

The cosines of the angles $\alpha$, $\beta$, $\gamma$ that $\vec{A}$ makes with
the three axes are its **direction cosines**:

$$ l = \frac{A_x}{A}, \quad m = \frac{A_y}{A}, \quad n = \frac{A_z}{A},
\qquad l^{2} + m^{2} + n^{2} = 1 $$

In component form addition is simply componentwise:

$$ \vec{A} + \vec{B} = (A_x + B_x)\hat{i} + (A_y + B_y)\hat{j} + (A_z + B_z)\hat{k} $$

::: example Worked example 2.2
**Problem.** A vector is given by $\vec{A} = 2\hat{i} + 3\hat{j} - 6\hat{k}$. Find
(a) its magnitude, (b) the unit vector along it, and (c) its direction cosines.

**Solution.**

(a) $A = \sqrt{2^{2} + 3^{2} + (-6)^{2}} = \sqrt{4 + 9 + 36} = \sqrt{49} = 7$.

(b) $\hat{A} = \dfrac{2\hat{i} + 3\hat{j} - 6\hat{k}}{7}
= \dfrac{2}{7}\hat{i} + \dfrac{3}{7}\hat{j} - \dfrac{6}{7}\hat{k}$.

(c) $l = 2/7 = 0.286$, $m = 3/7 = 0.429$, $n = -6/7 = -0.857$.

Check: $l^{2} + m^{2} + n^{2} = (4 + 9 + 36)/49 = 1$, as it must be.
:::

A standard application: a block of weight $mg$ on a plane inclined at $\theta$
has weight components $mg\sin\theta$ **down the slope** and $mg\cos\theta$
**perpendicular into the slope**. Almost every inclined-plane problem in the next
four units starts from that one resolution.

## 2.3 Scalar and vector products

### Scalar (dot) product

::: definition Scalar product
The scalar product of $\vec{A}$ and $\vec{B}$ is the scalar

$$ \vec{A}\cdot\vec{B} = AB\cos\theta $$

where $\theta$ is the angle between them when they are drawn from a common point.
:::

Geometrically, $\vec{A}\cdot\vec{B}$ is the magnitude of one vector times the
**projection** of the other onto it. Its key properties:

- Commutative: $\vec{A}\cdot\vec{B} = \vec{B}\cdot\vec{A}$.
- Distributive: $\vec{A}\cdot(\vec{B} + \vec{C}) = \vec{A}\cdot\vec{B} + \vec{A}\cdot\vec{C}$.
- If the vectors are perpendicular, $\vec{A}\cdot\vec{B} = 0$; if parallel, $AB$; if antiparallel, $-AB$.
- $\vec{A}\cdot\vec{A} = A^{2}$.
- For the base unit vectors: $\hat{i}\cdot\hat{i} = \hat{j}\cdot\hat{j} = \hat{k}\cdot\hat{k} = 1$ and $\hat{i}\cdot\hat{j} = \hat{j}\cdot\hat{k} = \hat{k}\cdot\hat{i} = 0$.

Hence in component form

$$ \vec{A}\cdot\vec{B} = A_xB_x + A_yB_y + A_zB_z,
\qquad \cos\theta = \frac{A_xB_x + A_yB_y + A_zB_z}{AB} $$

Physical examples: work $W = \vec{F}\cdot\vec{s}$, power $P = \vec{F}\cdot\vec{v}$,
and magnetic flux $\Phi = \vec{B}\cdot\vec{A}$.

### Vector (cross) product

::: definition Vector product
The vector product of $\vec{A}$ and $\vec{B}$ is the vector

$$ \vec{A}\times\vec{B} = AB\sin\theta\,\hat{n} $$

whose magnitude is $AB\sin\theta$ and whose direction $\hat{n}$ is perpendicular
to the plane of $\vec{A}$ and $\vec{B}$, given by the right-hand screw rule:
turn $\vec{A}$ into $\vec{B}$ and the screw advances along $\hat{n}$.
:::

```figure caption="The magnitude of $\vec{A}\times\vec{B}$ equals the area of the parallelogram they span, base $A$ times height $B\sin\theta$. The product vector points out of the page."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Arc, Circle
fig, ax = plt.subplots(figsize=(4.6, 2.8))
A = np.array([4.0, 0.0]); th = np.radians(52)
B = 2.7 * np.array([np.cos(th), np.sin(th)])
ax.add_patch(Polygon([[0, 0], A, A + B, B], closed=True, facecolor=ACCENT,
                     alpha=0.12, edgecolor='none'))
for a, b, c, lab, off in [((0, 0), A, ACCENT, r'$\vec{A}$', (0, -14)),
                          ((0, 0), B, '#2e8b57', r'$\vec{B}$', (-20, -2))]:
    ax.annotate('', xy=b, xytext=a, arrowprops=dict(arrowstyle='-|>', color=c,
                lw=1.9, shrinkA=0, shrinkB=0, mutation_scale=13))
    ax.annotate(lab, np.array(b) / 2, textcoords='offset points', xytext=off,
                color=c, fontsize=10.5)
ax.plot([A[0], (A + B)[0]], [A[1], (A + B)[1]], color=MUTED, lw=1.0, ls='--')
ax.plot([B[0], (A + B)[0]], [B[1], (A + B)[1]], color=MUTED, lw=1.0, ls='--')
ax.plot([B[0], B[0]], [0, B[1]], color='#d9534f', lw=1.1, ls=':')
s = 0.18
ax.plot([B[0], B[0] + s, B[0] + s], [s, s, 0], color=MUTED, lw=0.8)
ax.annotate(r'$B\sin\theta$', (B[0] + 0.20, B[1] * 0.72), color='#d9534f', fontsize=9.5,
            va='center')
ax.add_patch(Arc((0, 0), 1.6, 1.6, theta1=0, theta2=52, color=INK, lw=0.9))
ax.annotate(r'$\theta$', (1.05, 0.30), color=INK, fontsize=10)
ax.add_patch(Circle((6.2, 1.25), 0.30, fill=False, edgecolor='#6a5acd', lw=1.3))
ax.plot([6.2], [1.25], 'o', color='#6a5acd', ms=3.5)
ax.annotate(r'$\vec{A}\times\vec{B}$', (6.2, 0.82), ha='center', va='top',
            color='#6a5acd', fontsize=10)
ax.annotate('area $= AB\\sin\\theta$', (3.15, 1.02), ha='center', va='center',
            color=INK, fontsize=9.5)
ax.set_xlim(-1.2, 7.5); ax.set_ylim(-0.8, 2.9); ax.set_aspect('equal'); ax.axis('off')
```
Properties:

- **Anticommutative**: $\vec{A}\times\vec{B} = -\,\vec{B}\times\vec{A}$.
- $\vec{A}\times\vec{A} = \vec{0}$, and the product of parallel or antiparallel vectors is zero.
- It is maximum, $AB$, when the vectors are perpendicular.
- $\hat{i}\times\hat{i} = \hat{j}\times\hat{j} = \hat{k}\times\hat{k} = \vec{0}$, while $\hat{i}\times\hat{j} = \hat{k}$, $\hat{j}\times\hat{k} = \hat{i}$, $\hat{k}\times\hat{i} = \hat{j}$ (reverse the order and the sign flips).

In components,

$$ \vec{A}\times\vec{B} = (A_yB_z - A_zB_y)\hat{i} + (A_zB_x - A_xB_z)\hat{j} + (A_xB_y - A_yB_x)\hat{k} $$

The magnitude $AB\sin\theta$ is the **area of the parallelogram** with the two
vectors as adjacent sides; half of it is the area of the triangle. Physical
examples: torque $\vec{\tau} = \vec{r}\times\vec{F}$, angular momentum
$\vec{L} = \vec{r}\times\vec{p}$, and the magnetic force
$\vec{F} = q\,\vec{v}\times\vec{B}$.

| | Scalar product | Vector product |
|---|---|---|
| Result | scalar | vector |
| Formula | $AB\cos\theta$ | $AB\sin\theta\,\hat{n}$ |
| Zero when | vectors are perpendicular | vectors are parallel |
| Maximum when | vectors are parallel | vectors are perpendicular |
| Order matters? | no | yes — reversing changes the sign |
| Example | work, power | torque, angular momentum |

::: caution Sine and cosine get swapped
The dot product uses $\cos\theta$, the cross product $\sin\theta$. So two
perpendicular vectors have **zero dot product but maximum cross product** —
which is why no work is done by a centripetal force, yet a force at right angles
to the radius gives the largest torque.
:::

::: example Worked example 2.3
**Problem.** For $\vec{A} = \hat{i} + \hat{j}$ and $\vec{B} = \hat{j} + \hat{k}$,
find (a) $\vec{A}\cdot\vec{B}$ and the angle between the vectors, and
(b) $\vec{A}\times\vec{B}$ and its magnitude.

**Solution.** Here $A = \sqrt{1^{2}+1^{2}+0^{2}} = \sqrt{2}$ and likewise
$B = \sqrt{2}$.

(a) $\vec{A}\cdot\vec{B} = (1)(0) + (1)(1) + (0)(1) = 1$. So

$$ \cos\theta = \frac{1}{\sqrt{2}\sqrt{2}} = \frac{1}{2}
\;\Rightarrow\; \theta = 60^{\circ} $$

(b) With $\vec{A} = (1,1,0)$ and $\vec{B} = (0,1,1)$,

$$ \vec{A}\times\vec{B} = (1\cdot1 - 0\cdot1)\hat{i} + (0\cdot0 - 1\cdot1)\hat{j} + (1\cdot1 - 1\cdot0)\hat{k} = \hat{i} - \hat{j} + \hat{k} $$

Its magnitude is $\sqrt{1 + 1 + 1} = \sqrt{3} = 1.73$. As a check,
$AB\sin\theta = 2\sin60^{\circ} = 2(0.866) = 1.73$. The two answers agree.
:::

::: example Worked example 2.4
**Problem.** (a) A force $\vec{F} = (3\hat{i} + 4\hat{j})\ \text{N}$ moves a body
from the point $(1, 1, 0)\ \text{m}$ to $(4, 5, 0)\ \text{m}$. Find the work done.
(b) A force $\vec{F} = (3\hat{i} + 2\hat{j} - 4\hat{k})\ \text{N}$ acts at the
point $\vec{r} = (2\hat{i} + \hat{j} - \hat{k})\ \text{m}$ from the origin. Find
the torque about the origin.

**Solution.**

(a) Displacement $\vec{s} = (4-1)\hat{i} + (5-1)\hat{j} = 3\hat{i} + 4\hat{j}$ m.

$$ W = \vec{F}\cdot\vec{s} = (3)(3) + (4)(4) = 9 + 16 = 25\ \text{J} $$

(b) $\vec{\tau} = \vec{r}\times\vec{F}$ with $\vec{r} = (2,1,-1)$ and
$\vec{F} = (3,2,-4)$:

$$ \tau_x = (1)(-4) - (-1)(2) = -2, \quad \tau_y = (-1)(3) - (2)(-4) = 5,
\quad \tau_z = (2)(2) - (1)(3) = 1 $$

$$ \vec{\tau} = (-2\hat{i} + 5\hat{j} + \hat{k})\ \text{N m} $$

with magnitude $\sqrt{4 + 25 + 1} = \sqrt{30} = 5.48\ \text{N m}$.
:::

## Chapter summary

- Scalars need a magnitude only; vectors need magnitude **and** direction and
  add by the triangle, parallelogram or polygon law.
- Parallelogram law: $R = \sqrt{P^{2} + Q^{2} + 2PQ\cos\theta}$ and
  $\tan\alpha = Q\sin\theta/(P + Q\cos\theta)$. Maximum $P+Q$ at $0^{\circ}$,
  minimum $P-Q$ at $180^{\circ}$.
- A closed polygon of vectors means zero resultant — the equilibrium condition.
- Resolution: $A_x = A\cos\theta$, $A_y = A\sin\theta$; recombine with
  $A = \sqrt{A_x^{2} + A_y^{2}}$, $\tan\theta = A_y/A_x$.
- $\hat{A} = \vec{A}/A$; $\vec{A} = A_x\hat{i} + A_y\hat{j} + A_z\hat{k}$ with
  $A = \sqrt{A_x^{2} + A_y^{2} + A_z^{2}}$ and $l^{2}+m^{2}+n^{2}=1$.
- Dot product $\vec{A}\cdot\vec{B} = AB\cos\theta = A_xB_x + A_yB_y + A_zB_z$; it
  is a scalar and vanishes for perpendicular vectors.
- Cross product $\vec{A}\times\vec{B} = AB\sin\theta\,\hat{n}$; it is a vector,
  vanishes for parallel vectors, reverses sign on swapping, and its magnitude is
  the area of the parallelogram formed by the two vectors.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Which of the following is a vector quantity? <span class="marks">[1]</span>
   (a) work (b) temperature (c) torque (d) electric charge
2. The resultant of two forces of $3\ \text{N}$ and $4\ \text{N}$ acting at right angles is <span class="marks">[1]</span>
   (a) $1\ \text{N}$ (b) $5\ \text{N}$ (c) $7\ \text{N}$ (d) $12\ \text{N}$
3. If $\vec{A}\cdot\vec{B} = 0$ for two non-zero vectors, then the angle between them is <span class="marks">[1]</span>
   (a) $0^{\circ}$ (b) $45^{\circ}$ (c) $90^{\circ}$ (d) $180^{\circ}$
4. The magnitude of $\hat{i}\times\hat{j}$ is <span class="marks">[1]</span>
   (a) 0 (b) 1 (c) $\sqrt{2}$ (d) 2
5. Two equal vectors of magnitude $P$ give a resultant of magnitude $P$. The angle between them is <span class="marks">[1]</span>
   (a) $60^{\circ}$ (b) $90^{\circ}$ (c) $120^{\circ}$ (d) $180^{\circ}$
6. The area of the triangle formed by $\vec{A}$ and $\vec{B}$ as two of its sides is <span class="marks">[1]</span>
   (a) $AB\sin\theta$ (b) $\frac{1}{2}AB\sin\theta$ (c) $AB\cos\theta$ (d) $\frac{1}{2}AB\cos\theta$

::: note Answers to Group A
**1.** (c) — torque has a direction given by the right-hand rule; work and charge are scalars.
**2.** (b) — $\sqrt{3^{2}+4^{2}} = 5\ \text{N}$.
**3.** (c) — $AB\cos\theta = 0$ requires $\cos\theta = 0$.
**4.** (b) — $\sin 90^{\circ} = 1$ and both are unit vectors.
**5.** (c) — $P^{2} = 2P^{2}(1 + \cos\theta)$ gives $\cos\theta = -1/2$.
**6.** (b) — the cross product gives the parallelogram area; the triangle is half of it.
:::

**Group B — Short answer (5 marks each)**

1. State the parallelogram law of vector addition and derive expressions for the
   magnitude and direction of the resultant of two vectors. <span class="marks">[5]</span>
2. Define a unit vector. If $\vec{A} = 3\hat{i} - 4\hat{j} + 12\hat{k}$, find its
   magnitude, the unit vector along it and its direction cosines. <span class="marks">[5]</span>
3. Two forces of $6\ \text{N}$ and $8\ \text{N}$ act on a body at right angles to
   each other. Find the magnitude and direction of the resultant force. <span class="marks">[5]</span>
4. Distinguish between the scalar and the vector product of two vectors, giving
   one physical example of each. <span class="marks">[5]</span>
5. Find the angle between the vectors $\vec{A} = 2\hat{i} + 2\hat{j} - \hat{k}$
   and $\vec{B} = 6\hat{i} - 3\hat{j} + 2\hat{k}$. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Outline: state the law, then reproduce the derivation of
$R = \sqrt{P^{2}+Q^{2}+2PQ\cos\theta}$ and $\tan\alpha = Q\sin\theta/(P+Q\cos\theta)$
given in §2.1.

**2.** $A = \sqrt{9 + 16 + 144} = \sqrt{169} = 13$.
$\hat{A} = (3\hat{i} - 4\hat{j} + 12\hat{k})/13$; direction cosines
$l = 3/13 = 0.231$, $m = -4/13 = -0.308$, $n = 12/13 = 0.923$.

**3.** $R = \sqrt{6^{2}+8^{2}} = 10\ \text{N}$;
$\tan\alpha = 8/6 = 1.333$, so $\alpha = 53.1^{\circ}$ from the $6\ \text{N}$ force.

**4.** Outline: use the comparison table in §2.3 — scalar versus vector result,
$\cos\theta$ versus $\sin\theta$, order dependence; work and torque as examples.

**5.** $\vec{A}\cdot\vec{B} = 12 - 6 - 2 = 4$; $A = \sqrt{4+4+1} = 3$ and
$B = \sqrt{36+9+4} = 7$. So $\cos\theta = 4/21 = 0.1905$ and
$\theta = 79.0^{\circ}$.
:::

**Group C — Long answer (8 marks each)**

1. (a) State and explain the triangle, parallelogram and polygon laws of vector
   addition. <span class="marks">[4]</span>
   (b) Two forces $P$ and $Q$ act at a point. Show that the resultant is maximum
   when they are parallel and minimum when they are antiparallel. Hence find the
   two forces whose maximum resultant is $14\ \text{N}$ and whose minimum
   resultant is $2\ \text{N}$. <span class="marks">[4]</span>
2. (a) Define the scalar and vector products and state two properties of each. <span class="marks">[4]</span>
   (b) Given $\vec{A} = 4\hat{i} + 3\hat{j}$ and $\vec{B} = 2\hat{i} + 5\hat{j}$,
   find $\vec{A}\cdot\vec{B}$, $\vec{A}\times\vec{B}$, the angle between the
   vectors, and the area of the triangle having $\vec{A}$ and $\vec{B}$ as two
   of its sides. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** (b) $R^{2} = P^{2}+Q^{2}+2PQ\cos\theta$ increases with $\cos\theta$, which is
greatest ($+1$) at $\theta = 0^{\circ}$, giving $R_{\max} = P+Q$, and least
($-1$) at $\theta = 180^{\circ}$, giving $R_{\min} = P-Q$. Then
$P + Q = 14$ and $P - Q = 2$, so $P = 8\ \text{N}$ and $Q = 6\ \text{N}$.

**2.** (b) $\vec{A}\cdot\vec{B} = (4)(2) + (3)(5) = 23$.
$\vec{A}\times\vec{B} = (4\times5 - 3\times2)\hat{k} = 14\hat{k}$, of magnitude 14.
$A = 5$, $B = \sqrt{29} = 5.385$, so $\cos\theta = 23/26.93 = 0.854$ and
$\theta = 31.3^{\circ}$. Area of the triangle
$= \frac{1}{2}(14) = 7$ square units.
:::
