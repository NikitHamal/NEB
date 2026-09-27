---
subject: Physics
grade: 11
unit: 14
title: Reflection at curved mirror
hours: 2
area: Waves and Optics
---

A curved mirror is a polished part of a sphere. Because the surface curves, the
normals at different points of it point in different directions, so a bundle of
parallel rays is brought together at a point or spread out from a point. That one
fact is behind the shaving mirror, the dentist's mirror, the headlight reflector
and the wide-angle mirror on a Sajha bus. This unit fixes the language (pole,
centre of curvature, focus), separates real images from virtual ones, and derives
the single equation that ties object distance, image distance and focal length
together.

::: key What the exam asks
Two things, almost every year: *state the nature of the image* for a given object
position, and *use the mirror formula with correct signs*. Marks are lost on signs
far more often than on arithmetic.
:::

## 14.1 Real and virtual images

### The words you must use correctly

```figure caption="Terms used for spherical mirrors. For a concave mirror $F$ and $C$ lie in front of the mirror; for a convex mirror they lie behind it and are only virtual points."
import numpy as np, matplotlib.pyplot as plt
fig, axs = plt.subplots(2, 1, figsize=(4.9, 3.6))
R = 6.0
th = np.linspace(-0.45, 0.45, 240)

ax = axs[0]
ax.plot(-R + R*np.cos(th), R*np.sin(th), color=INK, lw=2.4, zorder=5)
ax.plot([-8.6, 7.2], [0, 0], color=MUTED, lw=0.9, ls=':')
for y in (1.9, 1.0):
    xm = -R + np.sqrt(R*R - y*y)
    ax.annotate('', xy=(xm, y), xytext=(-8.4, y),
                arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.3,
                                mutation_scale=11, shrinkA=0, shrinkB=0))
    ax.plot([xm, -3.0], [y, 0.0], color=ACCENT, lw=1.3, zorder=4)
    ax.annotate('', xy=(xm + 0.62*(-3.0 - xm), y*0.38), xytext=(xm + 0.50*(-3.0 - xm), y*0.50),
                arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.3,
                                mutation_scale=11, shrinkA=0, shrinkB=0))
ax.annotate('', xy=(0, -1.55), xytext=(-6, -1.55),
            arrowprops=dict(arrowstyle='<|-|>', color=SERIES[1], lw=1.1, mutation_scale=9))
ax.text(-3.0, -2.55, 'radius  $R$', ha='center', color=SERIES[1], fontsize=9)
ax.annotate('', xy=(0, -1.55), xytext=(-3, -1.55),
            arrowprops=dict(arrowstyle='<|-|>', color=SERIES[2], lw=2.0, mutation_scale=9))
ax.text(-1.5, -1.45, '$f$', ha='center', va='bottom', color=SERIES[2], fontsize=10)
ax.text(6.9, 1.4, 'concave', ha='right', fontsize=10, color=INK, weight='bold')
ax.text(6.9, 0.45, '(converging)', ha='right', fontsize=9, color=MUTED)
for x, lab, off in [(0, 'P', (7, -4)), (-3, 'F', (-4, -15)), (-6, 'C', (-4, -15))]:
    ax.plot([x], [0], 'o', color=INK, ms=4.2, zorder=6)
    ax.annotate(lab, (x, 0), textcoords='offset points', xytext=off, color=INK, fontsize=10)

ax = axs[1]
ax.plot(R - R*np.cos(th), R*np.sin(th), color=INK, lw=2.4, zorder=5)
ax.plot([-8.6, 0], [0, 0], color=MUTED, lw=0.9, ls=':')
ax.plot([0, 7.2], [0, 0], color=MUTED, lw=0.9, ls=(0, (4, 3)))
for y in (1.9, 1.0):
    xm = R - np.sqrt(R*R - y*y)
    ax.annotate('', xy=(xm, y), xytext=(-8.4, y),
                arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.3,
                                mutation_scale=11, shrinkA=0, shrinkB=0))
    dx, dy = xm - 3.0, y
    ax.annotate('', xy=(xm + 0.80*dx, y + 0.80*dy), xytext=(xm, y),
                arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.3,
                                mutation_scale=11, shrinkA=0, shrinkB=0))
    ax.plot([xm, 3.0], [y, 0], color=MUTED, lw=0.9, ls=(0, (3, 2)))
ax.annotate('', xy=(6, -1.55), xytext=(0, -1.55),
            arrowprops=dict(arrowstyle='<|-|>', color=SERIES[1], lw=1.1, mutation_scale=9))
ax.text(3.0, -2.55, 'radius  $R$', ha='center', color=SERIES[1], fontsize=9)
ax.annotate('', xy=(3, -1.55), xytext=(0, -1.55),
            arrowprops=dict(arrowstyle='<|-|>', color=SERIES[2], lw=2.0, mutation_scale=9))
ax.text(1.5, -1.45, '$f$', ha='center', va='bottom', color=SERIES[2], fontsize=10)
ax.text(-8.4, -2.35, 'convex', ha='left', fontsize=10, color=INK, weight='bold')
ax.text(-8.4, -3.3, '(diverging)', ha='left', fontsize=9, color=MUTED)
for x, lab, fc, off in [(0, 'P', INK, (-12, -4)), (3, 'F', 'none', (-4, -15)),
                        (6, 'C', 'none', (-4, -15))]:
    ax.plot([x], [0], 'o', color=INK, ms=4.2, mfc=fc, zorder=6)
    ax.annotate(lab, (x, 0), textcoords='offset points', xytext=off, color=INK, fontsize=10)

for ax in axs:
    ax.set_xlim(-8.8, 7.4); ax.set_ylim(-3.4, 2.9)
    ax.set_aspect('equal'); ax.axis('off')
fig.subplots_adjust(hspace=0.02)
```
| Term | Meaning |
|---|---|
| Pole $P$ | the geometrical centre of the reflecting surface |
| Centre of curvature $C$ | the centre of the sphere of which the mirror is a part |
| Radius of curvature $R$ | the distance $PC$ |
| Principal axis | the straight line through $P$ and $C$ |
| Principal focus $F$ | the point on the axis where paraxial rays parallel to the axis converge (concave) or from which they appear to diverge (convex) |
| Focal length $f$ | the distance $PF$, and $f = R/2$ |
| Aperture | the effective diameter of the reflecting surface |

**Paraxial rays** are rays close to the principal axis and nearly parallel to it.
Everything in this unit assumes paraxial rays and a small aperture; otherwise the
mirror suffers from *spherical aberration* and the rays do not meet at one point.

::: derivation The focal length of a spherical mirror is half its radius, $f = R/2$
We start from the law of reflection at one point on the mirror, and reach a relation between
the focal length $f = PF$ and the radius of curvature $R = PC$.

**Setting up.** $P$ is the pole, $C$ the centre of curvature and $F$ the principal focus. A
ray parallel to the axis strikes the mirror at $M$, a small height $h$ above the axis, and
after reflection passes through $F$.

**Step 1 — identify the normal.** The normal to a spherical surface at any point passes
through the centre of curvature, so the normal at $M$ is the line $MC$.

**Step 2 — the angle of incidence.** The incident ray is parallel to the axis $PC$, and $MC$
cuts both. Alternate angles between parallel lines are equal, so if the angle of incidence is
$\theta$, then

$$ \angle MCP = \theta $$

**Step 3 — the angle of reflection.** By the law of reflection the reflected ray makes the
same angle $\theta$ with the normal $MC$:

$$ \angle CMF = \theta $$

**Step 4 — use the exterior-angle rule on triangle $MCF$.** The exterior angle at $F$ equals
the sum of the two opposite interior angles, which are both $\theta$:

$$ \angle MFP = \theta + \theta = 2\theta $$

**Step 5 — drop a perpendicular from $M$ to the axis.** Call the foot $N$, so $MN = h$. From
the right-angled triangle $MNC$:

$$ \tan\theta = \frac{h}{NC} $$

**Step 6 — do the same for triangle $MNF$:**

$$ \tan 2\theta = \frac{h}{NF} $$

**Step 7 — use the paraxial approximation.** The ray is close to the axis, so $\theta$ is
small and, in radians, $\tan\theta \approx \theta$ and $\tan 2\theta \approx 2\theta$. Also
$N$ lies practically at the pole $P$, so $NC \approx PC$ and $NF \approx PF$:

$$ \theta \approx \frac{h}{PC}, \qquad 2\theta \approx \frac{h}{PF} $$

**Step 8 — divide the second by the first** so that $h$ and $\theta$ both cancel:

$$ \frac{2\theta}{\theta} = \frac{h/PF}{h/PC} = \frac{PC}{PF} $$

**Step 9 — simplify the left side:**

$$ 2 = \frac{PC}{PF} $$

**Step 10 — rearrange, and rename $PC = R$, $PF = f$:**

$$ PF = \tfrac{1}{2}PC \qquad \Longrightarrow \qquad f = \frac{R}{2} $$

**Result.**

$$ f = \frac{R}{2} \qquad \text{equivalently} \qquad R = 2f $$

**What it means.** The focus sits exactly halfway between the pole and the centre of
curvature. Notice that $h$ dropped out in Step 8 — so *every* paraxial ray, whatever its
height, crosses the axis at the same point $F$. That is precisely why a mirror forms a sharp
image.

**Conditions used.** Only paraxial rays (small aperture, $h \ll R$). Rays far from the axis
cross the axis nearer the mirror — the defect called **spherical aberration** — and for them
$f = R/2$ is no longer true.
:::

### Real and virtual images

::: definition Real and virtual image
A **real image** is formed when reflected rays actually *meet* at a point. Light
energy reaches that point, so a real image can be caught on a screen.
A **virtual image** is formed when reflected rays only *appear* to come from a
point, because their backward extensions meet there. No light reaches that point,
so a virtual image cannot be caught on a screen — it can only be seen by an eye
looking into the mirror.
:::

| | Real image | Virtual image |
|---|---|---|
| Formed by | actual intersection of rays | intersection of backward extensions |
| Screen test | can be caught on a screen | cannot be caught on a screen |
| Orientation | inverted (for a single mirror) | erect |
| Position | in front of the mirror | behind the mirror |
| Sign of $v$ | negative (new Cartesian) | positive |
| Sign of $m$ | negative | positive |

To locate an image by drawing, use any two of these four standard rays:

1. A ray **parallel to the principal axis** reflects through $F$ (concave), or
   appears to come from $F$ (convex).
2. A ray **through $F$** reflects parallel to the principal axis.
3. A ray **through $C$** strikes the mirror normally and retraces its path.
4. A ray **striking the pole $P$** reflects making an equal angle with the axis.

```figure caption="Concave mirror with the object beyond $C$. The three reflected rays actually cross in front of the mirror, so the image is real, inverted and diminished."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.1, 3.0))
R, ho = 6.0, 1.6
xo, xi, hi = -8.0, -4.8, -0.96
RED = "#A8271F"
mx = lambda y: -R + np.sqrt(R*R - y*y)
th = np.linspace(-0.45, 0.45, 240)
ax.plot(-R + R*np.cos(th), R*np.sin(th), color=INK, lw=2.4, zorder=5)
ax.plot([-9.6, 1.2], [0, 0], color=MUTED, lw=0.9, ls=':')

def ray(pts, c, lw=1.35, ls='-', head=True):
    pts = np.array(pts, float)
    ax.plot(pts[:, 0], pts[:, 1], color=c, lw=lw, ls=ls, zorder=3)
    if head:
        for k in range(len(pts) - 1):
            a, b = pts[k], pts[k + 1]
            ax.annotate('', xy=a + 0.60*(b - a), xytext=a + 0.50*(b - a),
                        arrowprops=dict(arrowstyle='-|>', color=c, lw=lw,
                                        mutation_scale=11, shrinkA=0, shrinkB=0))

m1 = (mx(ho), ho)
slope = (hi - ho) / (xi - m1[0])
ray([(xo, ho), m1, (-6.6, ho + (-6.6 - m1[0])*slope)], ACCENT)
ray([(xo, ho), (mx(hi), hi), (-7.4, hi)], SERIES[2])
ray([(xo, ho), (0.0, 0.0), (-6.6, -ho*6.6/(-xo))], SERIES[3])

ax.annotate('', xy=(xo, ho), xytext=(xo, 0),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=2.2, mutation_scale=13))
ax.annotate('', xy=(xi, hi), xytext=(xi, 0),
            arrowprops=dict(arrowstyle='-|>', color=RED, lw=2.2, mutation_scale=13))
for x, lab, off in [(0, 'P', (7, 4)), (-3, 'F', (-4, -16)), (-6, 'C', (-12, 6))]:
    ax.plot([x], [0], 'o', color=INK, ms=4.2, zorder=6)
    ax.annotate(lab, (x, 0), textcoords='offset points', xytext=off, color=INK, fontsize=10)
ax.annotate('A', (xo, ho), textcoords='offset points', xytext=(-14, -4), color=INK, fontsize=10)
ax.annotate('B', (xo, 0), textcoords='offset points', xytext=(-14, -13), color=INK, fontsize=10)
ax.annotate('image', (xi, hi), textcoords='offset points', xytext=(0, -24),
            ha='center', color=RED, fontsize=9)
ax.annotate('object', (xo, ho), textcoords='offset points', xytext=(0, 10),
            ha='center', color=INK, fontsize=9)
ax.set_xlim(-9.8, 1.4); ax.set_ylim(-2.7, 2.7)
ax.set_aspect('equal'); ax.axis('off')
```
The same construction repeated for every object position gives the table every
NEB candidate should know by heart.

| Object position (concave mirror) | Image position | Nature | Size |
|---|---|---|---|
| At infinity | At $F$ | Real, inverted | Point-sized |
| Beyond $C$ | Between $F$ and $C$ | Real, inverted | Diminished |
| At $C$ | At $C$ | Real, inverted | Same size |
| Between $C$ and $F$ | Beyond $C$ | Real, inverted | Magnified |
| At $F$ | At infinity | Real, inverted | Highly magnified |
| Between $F$ and $P$ | Behind the mirror | Virtual, erect | Magnified |

```figure caption="Convex mirror. The reflected rays diverge; only their backward extensions (dashed) meet, behind the mirror, so the image is virtual, erect and diminished."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.1, 2.7))
R, ho = 6.0, 1.5
xo, xi, hi = -4.5, 1.8, 0.6
RED = "#A8271F"
mx = lambda y: R - np.sqrt(R*R - y*y)
th = np.linspace(-0.42, 0.42, 240)
ax.plot(R - R*np.cos(th), R*np.sin(th), color=INK, lw=2.4, zorder=5)
ax.plot([-6.4, 0], [0, 0], color=MUTED, lw=0.9, ls=':')
ax.plot([0, 6.9], [0, 0], color=MUTED, lw=0.9, ls=(0, (4, 3)))

def ray(pts, c, lw=1.35, ls='-', head=True):
    pts = np.array(pts, float)
    ax.plot(pts[:, 0], pts[:, 1], color=c, lw=lw, ls=ls, zorder=3)
    if head:
        for k in range(len(pts) - 1):
            a, b = pts[k], pts[k + 1]
            ax.annotate('', xy=a + 0.60*(b - a), xytext=a + 0.50*(b - a),
                        arrowprops=dict(arrowstyle='-|>', color=c, lw=lw,
                                        mutation_scale=11, shrinkA=0, shrinkB=0))

xm = mx(ho)
dx, dy = xm - 3.0, ho
ray([(xo, ho), (xm, ho), (xm + 0.80*dx, ho + 0.80*dy)], ACCENT)
ray([(xm, ho), (3.0, 0.0)], MUTED, 0.9, ls=(0, (3, 2)), head=False)
ray([(xo, ho), (0.0, 0.0), (-3.6, -ho*3.6/(-xo))], SERIES[3])
ray([(0.0, 0.0), (2.7, 2.7*ho/(-xo))], MUTED, 0.9, ls=(0, (3, 2)), head=False)

ax.annotate('', xy=(xo, ho), xytext=(xo, 0),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=2.2, mutation_scale=13))
ax.annotate('', xy=(xi, hi), xytext=(xi, 0),
            arrowprops=dict(arrowstyle='-|>', color=RED, lw=2.0, mutation_scale=9))
for x, lab, fc, off in [(0, 'P', INK, (8, -14)), (3, 'F', 'none', (-4, 7)),
                        (6, 'C', 'none', (-4, 7))]:
    ax.plot([x], [0], 'o', color=INK, ms=4.2, mfc=fc, zorder=6)
    ax.annotate(lab, (x, 0), textcoords='offset points', xytext=off, color=INK, fontsize=10)
ax.annotate('A', (xo, ho), textcoords='offset points', xytext=(-13, -4), color=INK, fontsize=10)
ax.annotate('B', (xo, 0), textcoords='offset points', xytext=(-13, -13), color=INK, fontsize=10)
ax.annotate('virtual\nimage', (xi, 0), textcoords='offset points', xytext=(6, -10),
            ha='center', va='top', color=RED, fontsize=9)
ax.set_xlim(-6.6, 6.9); ax.set_ylim(-2.2, 3.0)
ax.set_aspect('equal'); ax.axis('off')
```
## 14.2 Mirror formula

### The new Cartesian sign convention

Before any formula can be used, the signs must be fixed.

::: memory The four rules of the new Cartesian convention
1. All distances are measured **from the pole $P$**.
2. Distances measured **in the direction of the incident light** are **positive**;
   those measured against it are **negative**.
3. Heights **above** the principal axis are positive, heights **below** it are negative.
4. Light is always drawn as travelling from left to right, so a real object in
   front of the mirror always has $u$ **negative**.
:::

It follows that for a **concave** mirror $f$ and $R$ are negative, and for a
**convex** mirror they are positive. A real image has $v$ negative; a virtual
image has $v$ positive.

### Deriving the formula

```figure caption="Geometry for the mirror formula. The two shaded triangles about the pole are similar; so are the triangles that meet at $F$, because $MP \\approx AB$ for paraxial rays."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.1, 3.0))
R, ho = 6.0, 1.6
xo, xi, hi = -8.0, -4.8, -0.96
RED = "#A8271F"
mx = lambda y: -R + np.sqrt(R*R - y*y)
th = np.linspace(-0.45, 0.45, 240)
ax.plot(-R + R*np.cos(th), R*np.sin(th), color=INK, lw=2.4, zorder=5)
ax.plot([-9.6, 1.2], [0, 0], color=MUTED, lw=0.9, ls=':')
ax.fill([xo, xo, 0], [0, ho, 0], color=ACCENT, alpha=0.16, zorder=1)
ax.fill([xi, xi, 0], [0, hi, 0], color=SERIES[3], alpha=0.22, zorder=1)
m1 = (mx(ho), ho)
slope = (hi - ho) / (xi - m1[0])
ax.plot([xo, m1[0], -6.6], [ho, ho, ho + (-6.6 - m1[0])*slope],
        color=SERIES[1], lw=1.3, zorder=3)
ax.plot([xo, 0.0, -6.6], [ho, 0.0, -ho*6.6/(-xo)], color=SERIES[2], lw=1.3, zorder=3)
ax.plot([m1[0], m1[0]], [0, ho], color=MUTED, lw=0.8, ls=(0, (2, 2)))
ax.annotate('', xy=(xo, ho), xytext=(xo, 0),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=2.2, mutation_scale=13))
ax.annotate('', xy=(xi, hi), xytext=(xi, 0),
            arrowprops=dict(arrowstyle='-|>', color=RED, lw=2.2, mutation_scale=13))
for x, lab, off in [(0, 'P', (7, 3)), (-3, 'F', (-4, 8)), (-6, 'C', (-11, 5))]:
    ax.plot([x], [0], 'o', color=INK, ms=4.2, zorder=6)
    ax.annotate(lab, (x, 0), textcoords='offset points', xytext=off, color=INK, fontsize=10)
ax.annotate('A', (xo, ho), textcoords='offset points', xytext=(-14, -4), color=INK, fontsize=10)
ax.annotate('B', (xo, 0), textcoords='offset points', xytext=(-14, -13), color=INK, fontsize=10)
ax.annotate('M', m1, textcoords='offset points', xytext=(-6, 7), ha='right', color=INK, fontsize=10)
ax.annotate('image', (xi, hi), textcoords='offset points', xytext=(0, -26),
            ha='center', color=RED, fontsize=9)
ax.set_xlim(-9.8, 1.4); ax.set_ylim(-2.7, 2.7)
ax.set_aspect('equal'); ax.axis('off')
```
::: derivation The mirror formula $\dfrac{1}{v}+\dfrac{1}{u}=\dfrac{1}{f}$
We start from two pairs of similar triangles in the ray diagram, and reach the relation
between object distance, image distance and focal length.

**Setting up.** An object $AB$ stands upright on the axis in front of a concave mirror, and
its real inverted image is $A'B'$. The strategy is important: first do all the geometry with
**plain lengths**, which are all positive numbers, and only at the end put in the signs of the
Cartesian convention. Mixing the two is where most marks are lost.

**Step 1 — the first pair of similar triangles.** The ray $AP$ hits the pole and reflects
along $PA'$, making equal angles with the axis (the axis is the normal at $P$). So the
right-angled triangles $ABP$ and $A'B'P$ have equal angles at $P$, and are similar.

**Step 2 — write the ratio of corresponding sides:**

$$ \frac{A'B'}{AB} = \frac{B'P}{BP} \qquad (1) $$

**Step 3 — the second pair of similar triangles.** The ray $AM$ travels parallel to the axis
and so reflects through the focus $F$, going on to $A'$. Triangles $MPF$ and $A'B'F$ are
similar, because they have equal vertically opposite angles at $F$ and a right angle each:

$$ \frac{A'B'}{MP} = \frac{B'F}{PF} $$

**Step 4 — replace $MP$ by $AB$.** For paraxial rays the point $M$ lies practically at the
pole, so the vertical height $MP$ is the same as the object height $AB$:

$$ \frac{A'B'}{AB} = \frac{B'F}{PF} \qquad (2) $$

**Step 5 — equate (1) and (2).** Both are equal to the same ratio $A'B'/AB$:

$$ \frac{B'P}{BP} = \frac{B'F}{PF} $$

**Step 6 — split $B'F$ into lengths we have names for.** From the diagram, $F$ lies between
$P$ and $B'$, so

$$ B'F = B'P - PF $$

**Step 7 — substitute that in:**

$$ \frac{B'P}{BP} = \frac{B'P - PF}{PF} \qquad (3) $$

**Step 8 — now put in the signs.** All three points $B$, $B'$ and $F$ lie in *front* of the
mirror, i.e. on the side from which light comes, so all three distances are negative in the
new Cartesian convention:

$$ BP = -u, \qquad B'P = -v, \qquad PF = -f $$

**Step 9 — substitute these into (3):**

$$ \frac{-v}{-u} = \frac{-v - (-f)}{-f} $$

**Step 10 — tidy both sides.** On the left the two minus signs cancel; on the right the
numerator becomes $-v + f$:

$$ \frac{v}{u} = \frac{f - v}{-f} $$

**Step 11 — take the minus sign out of the denominator on the right:**

$$ \frac{v}{u} = \frac{v - f}{f} $$

**Step 12 — cross-multiply:**

$$ vf = u(v - f) $$

**Step 13 — remove the bracket:**

$$ vf = uv - uf $$

**Step 14 — divide every single term by $uvf$:**

$$ \frac{vf}{uvf} = \frac{uv}{uvf} - \frac{uf}{uvf} $$

**Step 15 — cancel in each term:**

$$ \frac{1}{u} = \frac{1}{f} - \frac{1}{v} $$

**Step 16 — move $1/v$ to the left:**

$$ \frac{1}{v} + \frac{1}{u} = \frac{1}{f} $$

**Result.**

$$ \frac{1}{v} + \frac{1}{u} = \frac{1}{f} $$

**What it means.** This is the **mirror formula**. Although it was derived for one particular
case — a concave mirror forming a real image — it holds for concave and convex mirrors and for
images of either kind, *provided* the sign convention is obeyed throughout. That is the whole
point of having a sign convention: one equation instead of four.

**Conditions used.** Paraxial rays only (Step 4 needs $MP \approx AB$), a mirror of small
aperture, and all distances measured from the pole with the new Cartesian convention.
:::

::: tip The examiner is looking for
1. A labelled ray diagram with $P$, $F$, $C$, the object and the image marked.
2. The first similar-triangle pair and equation (1).
3. The second similar-triangle pair, **with the statement $MP \approx AB$ for paraxial
   rays** — a mark is usually reserved for this.
4. The substitution $B'F = B'P - PF$.
5. The sign-convention line $BP = -u$, $B'P = -v$, $PF = -f$, applied *after* the geometry.
6. Division by $uvf$ to reach the final form.
:::

Since $f = R/2$, the formula may also be written

$$ \frac{1}{v} + \frac{1}{u} = \frac{2}{R} $$

### Linear magnification

From equation (1) above, $A'B'/AB = B'P/BP$. Putting in signs, the image height
$h_i$ is negative (image inverted) while $h_o$ is positive, $B'P = -v$ and
$BP = -u$, so

$$ m = \frac{h_i}{h_o} = -\frac{v}{u} $$

Using the mirror formula to eliminate $u$ or $v$ gives two useful alternatives:

$$ m = \frac{f-v}{f} = \frac{f}{f-u} $$

::: caution Signs, not sizes
$m = -v/u$, **not** $v/u$. A negative $m$ means the image is inverted, and for a
single mirror that also means it is real. A positive $m$ means erect and virtual.
Students who drop the minus sign report a real image as erect and lose the
"nature of image" mark even when the numbers are right.
:::

::: example Worked example 14.1
**Problem.** An object $4\ \text{cm}$ tall is placed $25\ \text{cm}$ in front of a
concave mirror of radius of curvature $30\ \text{cm}$. Find the position, nature
and size of the image.

**Solution.** Concave mirror: $R = -30\ \text{cm}$, so
$f = R/2 = -15\ \text{cm}$. The object is in front, so $u = -25\ \text{cm}$.

$$ \frac{1}{v} = \frac{1}{f} - \frac{1}{u} = \frac{1}{-15} - \frac{1}{-25} = \frac{-5+3}{75} = -\frac{2}{75} $$

so $v = -37.5\ \text{cm}$. The negative sign means the image is $37.5\ \text{cm}$
in front of the mirror, i.e. **real**.

$$ m = -\frac{v}{u} = -\frac{-37.5}{-25} = -1.5 $$

The image is **inverted** and $1.5$ times as large:
$h_i = m\,h_o = -1.5 \times 4 = -6\ \text{cm}$, i.e. $6\ \text{cm}$ tall and below
the axis.
:::

::: example Worked example 14.2
**Problem.** The rear-view mirror of a bus is convex with radius of curvature
$4.0\ \text{m}$. A motorcycle is $6.0\ \text{m}$ behind the bus. Where is its
image and how large is it compared with the motorcycle?

**Solution.** Convex mirror: $R = +4.0\ \text{m}$, $f = +2.0\ \text{m}$;
$u = -6.0\ \text{m}$.

$$ \frac{1}{v} = \frac{1}{f} - \frac{1}{u} = \frac{1}{2.0} + \frac{1}{6.0} = \frac{3+1}{6.0} = \frac{2}{3}\ \text{m}^{-1} $$

so $v = +1.5\ \text{m}$: the image is $1.5\ \text{m}$ **behind** the mirror and
therefore **virtual** and **erect**.

$$ m = -\frac{v}{u} = -\frac{1.5}{-6.0} = +0.25 $$

The image is one quarter of the size of the motorcycle. This is exactly why
convex mirrors are used on vehicles: a wide field of view, at the price of
objects looking smaller (and so further away) than they really are.
:::

::: example Worked example 14.3
**Problem.** A concave mirror forms, on a screen, a real image three times the
size of the object. The screen and the object are $80\ \text{cm}$ apart. Find the
focal length and the radius of curvature of the mirror.

**Solution.** The image is real and magnified three times, so $m = -3$:

$$ -\frac{v}{u} = -3 \qquad \Rightarrow \qquad v = 3u $$

Both object and image are in front of the mirror. If $u = -d$ then
$v = -3d$, and the object-to-screen separation is
$|v| - |u| = 3d - d = 2d = 80\ \text{cm}$, giving $d = 40\ \text{cm}$.
Hence $u = -40\ \text{cm}$ and $v = -120\ \text{cm}$.

$$ \frac{1}{f} = \frac{1}{v} + \frac{1}{u} = -\frac{1}{120} - \frac{1}{40} = -\frac{1+3}{120} = -\frac{1}{30} $$

So $f = -30\ \text{cm}$ and $R = 2f = -60\ \text{cm}$: a concave mirror of focal
length $30\ \text{cm}$ and radius of curvature $60\ \text{cm}$.
:::

::: tip Checking an answer in one line
After solving, test the answer against the table in §14.1. Here the object at
$40\ \text{cm}$ lies between $C$ ($60\ \text{cm}$) and $F$ ($30\ \text{cm}$), and
the table says the image must be beyond $C$, real, inverted and magnified — which
is exactly what $v = -120\ \text{cm}$, $m = -3$ says. If the two disagree, a sign
has gone wrong.
:::

## Chapter summary

- For a spherical mirror the pole $P$, centre of curvature $C$ and focus $F$ lie
  on the principal axis, and $f = R/2$ (derived from the paraxial approximation).
- A **real** image is formed where reflected rays actually meet; it can be caught
  on a screen and is inverted. A **virtual** image is formed where the backward
  extensions meet; it cannot be caught on a screen and is erect.
- New Cartesian convention: distances from $P$, positive along the incident light.
  Concave $f<0$, convex $f>0$; real image $v<0$, virtual image $v>0$.
- Mirror formula: $\dfrac{1}{v} + \dfrac{1}{u} = \dfrac{1}{f} = \dfrac{2}{R}$.
- Magnification: $m = \dfrac{h_i}{h_o} = -\dfrac{v}{u} = \dfrac{f-v}{f} = \dfrac{f}{f-u}$.
  Negative $m$ = inverted and real; positive $m$ = erect and virtual.
- A concave mirror gives a real image for every object beyond $F$, and a magnified
  virtual image only when the object is between $F$ and $P$.
- A convex mirror gives a virtual, erect, diminished image for **every** position
  of a real object.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The focal length of a concave mirror of radius of curvature $40\ \text{cm}$ is <span class="marks">[1]</span>
   (a) $10\ \text{cm}$ (b) $20\ \text{cm}$ (c) $40\ \text{cm}$ (d) $80\ \text{cm}$
2. An object is placed between the focus and the pole of a concave mirror. The image is <span class="marks">[1]</span>
   (a) real, inverted, diminished (b) real, erect, magnified
   (c) virtual, erect, magnified (d) virtual, inverted, diminished
3. For a real image formed by a concave mirror, the linear magnification is <span class="marks">[1]</span>
   (a) positive (b) negative (c) always $+1$ (d) always zero
4. A convex mirror of focal length $f$ forms, of a real object, an image that is always <span class="marks">[1]</span>
   (a) real and inverted (b) real and erect
   (c) virtual and inverted (d) virtual and erect
5. An object is placed at the centre of curvature of a concave mirror. The image is formed <span class="marks">[1]</span>
   (a) at $F$ (b) at $C$ (c) at infinity (d) behind the mirror

::: note Answers to Group A
**1.** (b) — $f = R/2 = 40/2 = 20\ \text{cm}$.
**2.** (c) — inside the focus a concave mirror acts as a magnifying mirror.
**3.** (b) — a real image has $v$ and $u$ of the same sign, so $m = -v/u < 0$.
**4.** (d) — the reflected rays always diverge, so the image is virtual, erect and diminished.
**5.** (b) — the ray through $C$ retraces itself; $u = -R$ gives $v = -R$.
:::

**Group B — Short answer (5 marks each)**

1. Distinguish between a real image and a virtual image, giving one example of
   each from everyday life. <span class="marks">[5]</span>
2. Show that the focal length of a spherical mirror is half its radius of
   curvature for paraxial rays. <span class="marks">[5]</span>
3. An object $4\ \text{cm}$ tall is placed $20\ \text{cm}$ from a concave mirror of
   focal length $15\ \text{cm}$. Find the position, nature and size of the image. <span class="marks">[5]</span>
4. A convex rear-view mirror has a radius of curvature of $2.0\ \text{m}$. A car is
   $4.0\ \text{m}$ behind it. Find the position of the image and the magnification. <span class="marks">[5]</span>
5. State the new Cartesian sign convention and use it to explain why the focal
   length of a convex mirror is taken as positive. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Real: rays actually meet, screen-catchable, inverted, formed in front of
the mirror (the image on a cinema screen, or on the film of a reflecting
telescope). Virtual: only the backward extensions meet, not screen-catchable,
erect, formed behind the mirror (your face in a plane or convex mirror).

**2.** See the derivation in §14.1: $PC \approx h/\theta$, $PF \approx h/2\theta$,
hence $f = R/2$.

**3.** $u = -20\ \text{cm}$, $f = -15\ \text{cm}$.
$\dfrac{1}{v} = \dfrac{1}{-15} + \dfrac{1}{20} = \dfrac{-4+3}{60} = -\dfrac{1}{60}$,
so $v = -60\ \text{cm}$: real, $60\ \text{cm}$ in front of the mirror.
$m = -v/u = -(-60)/(-20) = -3$, so the image is inverted and
$3 \times 4 = 12\ \text{cm}$ tall.

**4.** $f = +1.0\ \text{m}$, $u = -4.0\ \text{m}$.
$\dfrac{1}{v} = \dfrac{1}{1.0} + \dfrac{1}{4.0} = 1.25\ \text{m}^{-1}$, so
$v = +0.8\ \text{m}$ — virtual, $0.8\ \text{m}$ behind the mirror.
$m = -0.8/(-4.0) = +0.2$: erect and one-fifth the size.

**5.** Rules as in §14.2. Light is drawn travelling left to right and strikes the
convex surface from the left; its focus lies **behind** the mirror, i.e. further
along the direction of the incident light, so $PF$ is a positive distance and
$f > 0$.
:::

**Group C — Long answer (8 marks each)**

1. (a) Define real and virtual images and state the new Cartesian sign
   convention. <span class="marks">[3]</span>
   (b) Derive the mirror formula $\dfrac{1}{v}+\dfrac{1}{u}=\dfrac{1}{f}$ for a
   concave mirror forming a real image, and hence obtain an expression for the
   linear magnification. <span class="marks">[5]</span>
2. A concave mirror throws on a wall an image of a lamp filament magnified four
   times. The wall is $3.0\ \text{m}$ from the mirror. Find (a) the distance of the
   filament from the mirror, (b) the focal length and radius of curvature of the
   mirror, and (c) the nature, position and magnification of the image if the
   filament is moved to $0.40\ \text{m}$ from the mirror. <span class="marks">[8]</span>

::: note Answer to Group C question 2
(a) The image on a wall is real and magnified $4\times$, so $m = -4 = -v/u$,
giving $v = 4u$. With $v = -3.0\ \text{m}$ we get $u = -0.75\ \text{m}$: the
filament is $75\ \text{cm}$ from the mirror.

(b) $\dfrac{1}{f} = \dfrac{1}{v} + \dfrac{1}{u} = -\dfrac{1}{3.0} - \dfrac{1}{0.75}
= -\dfrac{1}{3} - \dfrac{4}{3} = -\dfrac{5}{3}\ \text{m}^{-1}$, so
$f = -0.60\ \text{m}$ and $R = 2f = -1.2\ \text{m}$. The mirror has focal length
$60\ \text{cm}$ and radius of curvature $1.2\ \text{m}$.

(c) Now $u = -0.40\ \text{m}$, which is inside the focus.
$\dfrac{1}{v} = \dfrac{1}{-0.60} + \dfrac{1}{0.40} = -1.6667 + 2.5 = 0.8333\ \text{m}^{-1}$,
so $v = +1.2\ \text{m}$. The image is virtual, $1.2\ \text{m}$ behind the mirror,
with $m = -1.2/(-0.40) = +3$ — erect and three times as large. It can no longer
be caught on the wall.
:::
