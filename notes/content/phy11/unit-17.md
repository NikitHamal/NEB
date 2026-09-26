---
subject: Physics
grade: 11
unit: 17
title: Lenses
hours: 3
area: Waves and Optics
---

A lens is a piece of transparent material bounded by two surfaces, at least one
of which is curved. Because the two surfaces refract light one after the other,
a lens can gather a diverging bundle of rays back to a point, or spread a
parallel bundle out. Spectacles, the camera in a phone, a hand lens, the
objective of a telescope on a Pokhara rooftop — all of them are the same three
formulas applied over and over.

::: key What the examiner asks for
Three things carry almost all the marks in this unit: a correctly drawn ray
diagram with the sign convention respected, the derivation of the lens maker's
formula from refraction at two spherical surfaces, and numerical work with
$P = 1/f$ in dioptres. Learn those and the unit is done.
:::

## 17.1 Spherical lenses, angular magnification

### Types and basic terms

A **spherical lens** is bounded by two surfaces that are parts of spheres (a flat
face is a sphere of infinite radius). Lenses fall into two families.

```figure caption="The six common thin lenses. A lens thicker at the centre than at the rim converges light; one thinner at the centre diverges it."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.9))
h = 0.40
y = np.linspace(-h, h, 160)
s = 1 - (y/h)**2

def lens(x0, y0, e, cL, cR, col):
    xl = -e + cL*s
    xr =  e + cR*s
    X = np.concatenate([xl, xr[::-1]]) + x0
    Y = np.concatenate([y,  y[::-1]])  + y0
    ax.fill(X, Y, color=col, alpha=0.22, lw=0, zorder=2)
    ax.plot(X, Y, color=INK, lw=1.25, zorder=3)

conv = [(0.0, 'Bi-convex',       0.05, -0.20,  0.20),
        (1.60,'Plano-convex',    0.05,  0.00,  0.24),
        (3.20,'Convex meniscus', 0.05,  0.11,  0.31)]
div  = [(0.0, 'Bi-concave',      0.26,  0.21, -0.21),
        (1.60,'Plano-concave',   0.26,  0.00, -0.21),
        (3.20,'Concave meniscus',0.26,  0.31,  0.11)]

for x0, name, e, cL, cR in conv:
    lens(x0, 0.0, e, cL, cR, ACCENT)
    ax.annotate(name, (x0, -0.58), ha='center', color=INK, fontsize=8.4)
for x0, name, e, cL, cR in div:
    lens(x0, -1.45, e, cL, cR, '#d9534f')
    ax.annotate(name, (x0, -2.03), ha='center', color=INK, fontsize=8.4)

ax.annotate('CONVERGING  (convex)', (-0.80, 0.62), color=ACCENT, fontsize=9.0, ha='left')
ax.annotate('DIVERGING  (concave)', (-0.80, -0.83), color='#d9534f', fontsize=9.0, ha='left')
ax.set_xlim(-0.95, 4.00); ax.set_ylim(-2.25, 0.85)
ax.set_aspect('equal'); ax.axis('off')
```

| Term | Meaning |
|---|---|
| Centres of curvature $C_1, C_2$ | centres of the spheres of which the two faces are parts |
| Radii of curvature $R_1, R_2$ | radii of those spheres |
| Principal axis | the line joining $C_1$ and $C_2$ |
| Optical centre $O$ | point inside the lens through which a ray passes undeviated |
| Principal focus $F$ | point where a beam parallel to the axis converges (convex) or appears to diverge from (concave) |
| Focal length $f$ | distance $OF$ |
| Aperture | effective diameter of the lens |

A lens has **two** foci, one on each side, at equal distances from $O$ when the
same medium lies on both sides.

::: definition Sign convention (New Cartesian)
All distances are measured from the optical centre. Distances measured **in the
direction of the incident light are positive**, those measured against it are
negative. Heights **above** the principal axis are positive, below it negative.
Hence a real object on the left always has $u$ negative; $f$ is positive for a
convex lens and negative for a concave lens.
:::

### Image formation

Only two of these three standard rays are needed for any construction:

1. A ray parallel to the principal axis passes, after refraction, through the
   second focus $F_2$ (convex) or appears to come from $F_1$ (concave).
2. A ray through the optical centre goes straight on, undeviated.
3. A ray through the first focus $F_1$ emerges parallel to the principal axis.

```figure caption="Convex lens with the object beyond $2F_1$. The three standard rays meet at the image, which is real, inverted and diminished."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyArrow
fig, ax = plt.subplots(figsize=(5.1,2.9))

f = 1.0; u = -3.0; ho = 0.80
v = 1.0/(1.0/f + 1.0/u); hi = ho*v/u          # v = 1.5, hi = -0.4

ax.plot([-3.7, 3.0], [0,0], color=MUTED, lw=0.9, zorder=1)
yy = np.linspace(-1.05, 1.05, 160); sg = 1-(yy/1.05)**2
XL = -0.03 - 0.11*sg; XR = 0.03 + 0.11*sg
ax.fill(np.concatenate([XL, XR[::-1]]), np.concatenate([yy, yy[::-1]]),
        color=ACCENT, alpha=0.14, lw=0, zorder=2)
ax.plot(np.concatenate([XL, XR[::-1]]), np.concatenate([yy, yy[::-1]]),
        color=INK, lw=1.3, zorder=4)

for x, lab, dy in [(-1,'$F_1$',-0.32), (-2,'$2F_1$',-0.32),
                   (1,'$F_2$',0.30), (2,'$2F_2$',0.16)]:
    ax.plot([x],[0],'o', color=MUTED, ms=3.4, zorder=5)
    ax.annotate(lab, (x,dy), ha='center', color=MUTED, fontsize=8.6)
ax.annotate('$O$', (0.0, 1.14), ha='center', color=MUTED, fontsize=8.6)

def ray(pts, c, lw=1.4):
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=c, lw=lw, zorder=3)
    a, b = pts[0], pts[1]
    ax.annotate('', xy=((a[0]+b[0])/2, (a[1]+b[1])/2), xytext=a,
                arrowprops=dict(arrowstyle='-|>', color=c, lw=lw,
                                shrinkA=0, shrinkB=0, mutation_scale=11))

ray([(u,ho), (0,ho), (2.6, ho + (hi-ho)*2.6/v)], SERIES[0])
ray([(u,ho), (0,0), (2.6, hi*2.6/v)], SERIES[2])
ray([(u,ho), (0,-0.40), (2.6,-0.40)], SERIES[3])

ax.add_patch(FancyArrow(u, 0, 0, ho, width=0.012, head_width=0.10,
                        head_length=0.12, length_includes_head=True,
                        color=INK, zorder=6))
ax.add_patch(FancyArrow(v, 0, 0, hi, width=0.014, head_width=0.11,
                        head_length=0.13, length_includes_head=True,
                        color='#A8271F', zorder=6))
ax.annotate('object', (u, ho+0.10), ha='center', color=INK, fontsize=8.6)
ax.annotate('image', xy=(v, hi - 0.06), xytext=(v, -0.98), ha='center',
            color='#A8271F', fontsize=8.6,
            arrowprops=dict(arrowstyle='-', color='#A8271F', lw=0.8,
                            shrinkA=2, shrinkB=1))
ax.set_xlim(-3.9, 3.1); ax.set_ylim(-1.50, 1.42); ax.axis('off')
```
The results are summarised by the **thin lens formula**, valid with the sign
convention above:

$$ \frac{1}{v} - \frac{1}{u} = \frac{1}{f} $$

and the **linear (transverse) magnification**

$$ m = \frac{h_i}{h_o} = \frac{v}{u} $$

A negative $m$ means the image is inverted (and therefore real); a positive $m$
means erect and virtual.

| Position of object (convex lens) | Image position | Nature | Size |
|---|---|---|---|
| At infinity | at $F_2$ | real, inverted | point |
| Beyond $2F_1$ | between $F_2$ and $2F_2$ | real, inverted | diminished |
| At $2F_1$ | at $2F_2$ | real, inverted | same size |
| Between $F_1$ and $2F_1$ | beyond $2F_2$ | real, inverted | magnified |
| At $F_1$ | at infinity | real, inverted | highly magnified |
| Between $F_1$ and $O$ | same side as object | virtual, erect | magnified |

A **concave lens** is simpler: for every real object it gives a virtual, erect,
diminished image between the focus and the lens.

```figure caption="Concave lens. The emergent rays diverge; their backward extensions (dashed) meet at a virtual, erect, diminished image between $F_1$ and the lens."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyArrow
fig, ax = plt.subplots(figsize=(4.7,3.0))

f = -1.0; u = -2.0; ho = 0.80
v = 1.0/(1.0/f + 1.0/u); hi = ho*v/u          # v = -2/3, hi = +4/15

ax.plot([-2.6, 1.9], [0,0], color=MUTED, lw=0.9, zorder=1)
yy = np.linspace(-1.0, 1.0, 160); sg = 1-(yy/1.0)**2
XL = -0.17 + 0.12*sg; XR = 0.17 - 0.12*sg
ax.fill(np.concatenate([XL, XR[::-1]]), np.concatenate([yy, yy[::-1]]),
        color='#d9534f', alpha=0.12, lw=0, zorder=2)
ax.plot(np.concatenate([XL, XR[::-1]]), np.concatenate([yy, yy[::-1]]),
        color=INK, lw=1.3, zorder=4)

for x, lab in [(-1,'$F_1$'), (1,'$F_2$')]:
    ax.plot([x],[0],'o', color=MUTED, ms=3.4, zorder=5)
    ax.annotate(lab, (x,0.16), ha='center', color=MUTED, fontsize=8.6)
ax.annotate('$O$', (0.0, 1.10), ha='center', color=MUTED, fontsize=8.6)

def seg(pts, c, ls='-', lw=1.4, arrow=True):
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=c, lw=lw, ls=ls, zorder=3)
    if arrow:
        a, b = pts[0], pts[1]
        ax.annotate('', xy=((a[0]+b[0])/2, (a[1]+b[1])/2), xytext=a,
                    arrowprops=dict(arrowstyle='-|>', color=c, lw=lw,
                                    shrinkA=0, shrinkB=0, mutation_scale=11))

seg([(u,ho), (0,ho), (1.6, ho + 0.8*1.6)], SERIES[0])
seg([(0,ho), (-1,0)], SERIES[0], ls=(0,(3,2)), arrow=False)
seg([(u,ho), (0,0), (1.6, -0.4*1.6)], SERIES[2])
seg([(0,0), (v,hi)], SERIES[2], ls=(0,(3,2)), arrow=False)

ax.add_patch(FancyArrow(u, 0, 0, ho, width=0.012, head_width=0.09,
                        head_length=0.11, length_includes_head=True,
                        color=INK, zorder=6))
ax.add_patch(FancyArrow(v, 0, 0, hi, width=0.016, head_width=0.11,
                        head_length=0.12, length_includes_head=True,
                        color='#A8271F', zorder=6))
ax.annotate('object', (u, ho+0.10), ha='center', color=INK, fontsize=8.6)
ax.annotate('virtual image', (v, -0.36), ha='center',
            color='#A8271F', fontsize=8.2)
ax.set_xlim(-2.7, 2.0); ax.set_ylim(-0.62, 2.20); ax.axis('off')
```
::: example Worked example 17.1
**Problem.** An object $3\ \text{cm}$ tall stands $30\ \text{cm}$ in front of a
converging lens of focal length $20\ \text{cm}$. Find the position, nature and
size of the image.

**Solution.** With the sign convention, $u = -30\ \text{cm}$, $f = +20\ \text{cm}$.

$$ \frac{1}{v} = \frac{1}{f} + \frac{1}{u} = \frac{1}{20} - \frac{1}{30}
   = \frac{3-2}{60} = \frac{1}{60} $$

So $v = +60\ \text{cm}$: the image is $60\ \text{cm}$ behind the lens, and
because $v$ is positive it is **real**.

$$ m = \frac{v}{u} = \frac{+60}{-30} = -2 $$

The image is inverted and twice as tall: $h_i = -2 \times 3 = -6\ \text{cm}$,
i.e. $6\ \text{cm}$ tall and upside down.
:::

### Angular magnification

How big something *looks* depends not on its real size but on the angle it
subtends at the eye. A lens used as a magnifier does not change the object; it
lets you bring the object closer than the near point while still seeing it
sharply, so the angle grows.

::: definition Angular magnification (magnifying power)
The angular magnification $M$ of an optical instrument is the ratio of the angle
$\beta$ subtended at the eye by the final image to the angle $\alpha$ subtended
at the unaided eye by the object placed at the least distance of distinct vision
$D$ ($D = 25\ \text{cm}$ for a normal eye):

$$ M = \frac{\beta}{\alpha} $$
:::

```figure caption="Angular magnification. Left: the object at the near point subtends $\\alpha$ at the unaided eye. Right: a convex lens forms an enlarged virtual image at the near point, subtending the much larger angle $\\beta$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyArrow
fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.1,2.8))

# ---- (a) unaided eye
a1.plot([-2.9, 0.20], [0,0], color=MUTED, lw=0.9)
a1.add_patch(FancyArrow(-2.6, 0, 0, 0.50, width=0.013, head_width=0.10,
                        head_length=0.11, length_includes_head=True, color=INK))
a1.plot([-2.6,0],[0.50,0], color=SERIES[0], lw=1.3)
a1.plot([-2.6,0],[0,0],   color=SERIES[0], lw=1.3)
a1.text(-2.10, 0.202, r'$\alpha$', color=SERIES[0], fontsize=9.5,
        ha='center', va='center')
a1.plot([0],[0],'o',color=INK, ms=6.5)
a1.annotate('eye', (0.22,-0.09), fontsize=8.4, color=INK)
a1.annotate('$h$', (-2.72,0.22), fontsize=8.8, color=INK, ha='right')
a1.annotate('$D$', (-1.3,-0.30), fontsize=8.8, color=MUTED, ha='center')
a1.annotate('(a) unaided eye', (-1.3, 1.85), ha='center', fontsize=8.8, color=INK)
a1.set_xlim(-3.25, 0.85); a1.set_ylim(-0.66, 2.05); a1.axis('off')

# ---- (b) with magnifier, final image at D
f = 1.0; v = -2.5
u = 1.0/(1.0/v - 1.0/f); ho = 0.40; hi = ho*v/u     # u = -5/7, hi = 1.4
a2.plot([-2.95, 1.30], [0,0], color=MUTED, lw=0.9)
yy = np.linspace(-0.48,0.48,120); sg = 1-(yy/0.48)**2
XL = -0.02 - 0.16*sg; XR = 0.02 + 0.16*sg
a2.fill(np.concatenate([XL, XR[::-1]]), np.concatenate([yy, yy[::-1]]),
        color=ACCENT, alpha=0.16, lw=0)
a2.plot(np.concatenate([XL, XR[::-1]]), np.concatenate([yy, yy[::-1]]),
        color=INK, lw=1.3)
a2.plot([-1],[0],'o',color=MUTED,ms=3.2)
a2.annotate('$F$',(-1,0.16), ha='center', color=MUTED, fontsize=8.4)
a2.add_patch(FancyArrow(u, 0, 0, ho, width=0.012, head_width=0.085,
                        head_length=0.10, length_includes_head=True, color=INK))
a2.add_patch(FancyArrow(v, 0, 0, hi, width=0.014, head_width=0.10,
                        head_length=0.11, length_includes_head=True, color='#A8271F'))
a2.plot([u,0],[ho,ho], color=SERIES[0], lw=1.2)
a2.plot([0,1.2],[ho, ho-0.4*1.2], color=SERIES[0], lw=1.2)
a2.plot([v,0],[hi,ho], color=SERIES[0], lw=1.0, ls=(0,(3,2)))
a2.plot([u,1.2],[ho, ho-0.56*(1.2-u)], color=SERIES[2], lw=1.2)
a2.plot([v,u],[hi,ho], color=SERIES[2], lw=1.0, ls=(0,(3,2)))
a2.text(0.70, -0.136, r'$\beta$', color=SERIES[2], fontsize=9.5,
        ha='center', va='center')
a2.plot([0.33],[0.0],'o',color=INK, ms=6.5)
a2.annotate('eye', (0.40,-0.58), ha='center', fontsize=8.4, color=INK)
a2.annotate('virtual image at $D$', (v+0.10, hi+0.14), ha='left',
            color='#A8271F', fontsize=8.0)
a2.annotate('object', (u, -0.32), ha='center', fontsize=8.0, color=INK)
a2.annotate('(b) with magnifier', (-0.8, 1.85), ha='center', fontsize=8.8, color=INK)
a2.set_xlim(-3.25, 1.45); a2.set_ylim(-0.66, 2.05); a2.axis('off')
```
::: derivation Magnifying power of a simple microscope
We start from the definition of angular magnification and reach the two standard formulas, one
for each way of using a magnifying glass.

**Setting up.** A simple microscope is a single convex lens of short focal length $f$. The
object has height $h$, and the eye is held close behind the lens. $D$ is the least distance of
distinct vision (the near-point distance, $25$ cm for a normal eye). The object is placed
between the lens and its focus, so the image is virtual, erect and enlarged.

**Step 1 — the angle without the lens.** To see the object as big as possible with the bare eye,
you bring it to the near point, a distance $D$ away. The angle it then subtends is small, so

$$ \alpha \approx \frac{h}{D} $$

---

**Case 1 — final image at the near point (maximum magnification).**

**Step 2 — where the object must be.** The image must be at the near point, so with the sign
convention $v = -D$. Let the object distance be $u = -u_0$.

**Step 3 — the angle with the lens.** The eye is at the lens, so it receives the rays at the
angle the *object* subtends at the lens:

$$ \beta \approx \frac{h}{u_0} $$

**Step 4 — form the ratio, by the definition of magnifying power:**

$$ M = \frac{\beta}{\alpha} = \frac{h/u_0}{h/D} $$

**Step 5 — cancel $h$ and simplify the divided fraction:**

$$ M = \frac{D}{u_0} $$

**Step 6 — now find $u_0$ from the lens formula** $\dfrac{1}{v} - \dfrac{1}{u} = \dfrac{1}{f}$,
putting $v = -D$ and $u = -u_0$:

$$ \frac{1}{-D} - \frac{1}{-u_0} = \frac{1}{f} $$

**Step 7 — clean up the signs:**

$$ -\frac{1}{D} + \frac{1}{u_0} = \frac{1}{f} $$

**Step 8 — move $1/D$ across:**

$$ \frac{1}{u_0} = \frac{1}{f} + \frac{1}{D} $$

**Step 9 — multiply every term by $D$,** because Step 5 needs $D/u_0$:

$$ \frac{D}{u_0} = \frac{D}{f} + \frac{D}{D} $$

**Step 10 — simplify the last term and use Step 5:**

$$ M = 1 + \frac{D}{f} $$

---

**Case 2 — final image at infinity (relaxed eye).**

**Step 11 — where the object must be.** For the image to go to infinity, the object must sit
exactly at the focus, so $u_0 = f$.

**Step 12 — the angle with the lens** is then

$$ \beta \approx \frac{h}{f} $$

**Step 13 — form the ratio again:**

$$ M = \frac{\beta}{\alpha} = \frac{h/f}{h/D} $$

**Step 14 — cancel $h$:**

$$ M = \frac{D}{f} $$

**Result.**

$$ M_{near\ point} = 1 + \frac{D}{f}, \qquad M_{infinity} = \frac{D}{f} $$

**What it means.** A shorter focal length gives a bigger magnification, which is why a
magnifying glass is a strongly curved little lens. The near-point setting gives exactly **one**
extra unit of magnification, but the eye must accommodate, which tires it; the infinity setting
is more comfortable for long use.

**Conditions used.** The eye is close to the lens, all angles are small (so that
$\tan\theta \approx \theta$ in Steps 1, 3 and 12), and $D = 25$ cm for a normal eye.
:::

The near-point setting gives one extra unit of magnification but the eye must
accommodate, which tires it; the infinity setting is more comfortable.

::: example Worked example 17.2
**Problem.** A magnifying glass has focal length $5\ \text{cm}$. Taking
$D = 25\ \text{cm}$, find its magnifying power when the final image is
(a) at the near point and (b) at infinity. Where must the object be placed in
case (a)?

**Solution.**

(a) $M = 1 + D/f = 1 + 25/5 = 6$.

(b) $M = D/f = 25/5 = 5$.

For (a), $\dfrac{1}{u_0} = \dfrac{1}{f} + \dfrac{1}{D} = \dfrac{1}{5} + \dfrac{1}{25} = \dfrac{6}{25}$,
so $u_0 = 25/6 = 4.17\ \text{cm}$ — just inside the focus, as expected.
:::

## 17.2 Lens maker's formula

A lens refracts light twice, once at each face. So we first need the result for
refraction at **one** spherical surface.

::: derivation Refraction at a single spherical surface
We start from Snell's law at one curved boundary and reach the equation that a single spherical
refracting surface obeys. This one result, used twice, gives the whole lens theory.

**Setting up.** Light travels from a medium of index $n_1$ into one of index $n_2$ across a
spherical surface of radius $R$, with pole $P$ and centre of curvature $C$. A paraxial ray from
the axial object $O$ meets the surface at $A$, a small height $h$ above the axis, and after
refraction crosses the axis at $I$. Let $\alpha$, $\beta$, $\gamma$ be the (small) angles that
$AO$, $AC$ and $AI$ make with the axis. Note $AC$ is the **normal** at $A$, since a radius is
always normal to a sphere.

**Step 1 — find the angle of incidence.** In triangle $AOC$, the angle at $C$ is the exterior
angle rule applied the other way round: the exterior angle at $A$ (which is $i$) equals the sum
of the two opposite interior angles:

$$ i = \alpha + \beta $$

**Step 2 — find the angle of refraction.** In triangle $AIC$, $\beta$ is the exterior angle, so
it equals the sum of the two opposite interior angles $r$ and $\gamma$:

$$ \beta = r + \gamma $$

**Step 3 — make $r$ the subject:**

$$ r = \beta - \gamma $$

**Step 4 — write Snell's law at $A$:**

$$ n_1\sin i = n_2\sin r $$

**Step 5 — use the paraxial approximation.** $A$ is close to the axis, so $i$ and $r$ are small
and $\sin\theta \approx \theta$:

$$ n_1 i = n_2 r $$

**Step 6 — substitute Steps 1 and 3:**

$$ n_1(\alpha + \beta) = n_2(\beta - \gamma) $$

**Step 7 — express the three angles as ratios.** For a small angle, angle $\approx$ opposite
side over adjacent side, and $A$ is practically at $P$. With the Cartesian convention ($u$
negative for a real object):

$$ \alpha = \frac{h}{-u}, \qquad \beta = \frac{h}{R}, \qquad \gamma = \frac{h}{v} $$

**Step 8 — substitute these into Step 6:**

$$ n_1\left(\frac{h}{-u} + \frac{h}{R}\right)
= n_2\left(\frac{h}{R} - \frac{h}{v}\right) $$

**Step 9 — cancel $h$,** which multiplies every term. (This is the important moment: the answer
does not depend on the ray's height, which is why a sharp image forms at all.)

$$ -\frac{n_1}{u} + \frac{n_1}{R} = \frac{n_2}{R} - \frac{n_2}{v} $$

**Step 10 — collect the $v$ and $u$ terms on the left and the $R$ terms on the right:**

$$ \frac{n_2}{v} - \frac{n_1}{u} = \frac{n_2}{R} - \frac{n_1}{R} $$

**Step 11 — combine the right-hand side over the common denominator $R$:**

$$ \frac{n_2}{v} - \frac{n_1}{u} = \frac{n_2 - n_1}{R} $$

**Result.**

$$ \frac{n_2}{v} - \frac{n_1}{u} = \frac{n_2 - n_1}{R} $$

**What it means.** One equation covers every single curved refracting boundary — the front of a
lens, the back of a lens, the cornea of an eye — provided you put in the right $n_1$, $n_2$ and
the right sign for $R$. Applied twice in succession it gives the lens maker's formula.

**Conditions used.** Paraxial rays only (Steps 5 and 7), a surface of small aperture, and all
distances measured from the pole $P$ using the new Cartesian convention.
:::

```figure caption="A thin lens refracts twice. The first surface (radius $R_1$) alone would form the image $I_1$; the second surface (radius $R_2$) takes $I_1$ as its object and forms the final image $I$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.1,2.9))

ax.plot([-5.2, 5.4], [0,0], color=MUTED, lw=0.9, zorder=1)
yy = np.linspace(-1.15, 1.15, 160); sg = 1-(yy/1.15)**2
xl = -0.10 - 0.42*sg; xr = 0.10 + 0.42*sg
X = np.concatenate([xl, xr[::-1]]); Y = np.concatenate([yy, yy[::-1]])
ax.fill(X, Y, color=ACCENT, alpha=0.16, lw=0, zorder=2)
ax.plot(X, Y, color=INK, lw=1.3, zorder=3)

A = (-0.44, 0.95); B = (0.44, 0.72)
O = (-4.6, 0.0)
xI1 = B[0] + B[1]*(B[0]-A[0])/(A[1]-B[1])          # = 3.19
xI  = 1.55

def seg(p, q, c, ls='-', lw=1.5, arrow=True, z=5):
    ax.plot([p[0],q[0]], [p[1],q[1]], color=c, lw=lw, ls=ls, zorder=z)
    if arrow:
        ax.annotate('', xy=((p[0]+q[0])/2, (p[1]+q[1])/2), xytext=p,
                    arrowprops=dict(arrowstyle='-|>', color=c, lw=lw,
                                    shrinkA=0, shrinkB=0, mutation_scale=11))

ax.plot([A[0], 4.25],[A[1], 0], color=GRID, lw=1.0, ls=':', zorder=2)
ax.plot([B[0], -3.05],[B[1], 0], color=GRID, lw=1.0, ls=':', zorder=2)
seg(O, A, SERIES[0])
seg(A, B, SERIES[2])
seg(B, (xI1, 0.0), MUTED, ls=(0,(3,2)), arrow=False)
seg(B, (xI, 0.0), '#A8271F')
seg((xI,0.0), (2.85, -0.84), '#A8271F', arrow=False)

for x, lab, dy in [(xI1,'$I_1$',0.16), (xI,'$I$',-0.36),
                   (4.25,'$C_1$',-0.36), (-3.05,'$C_2$',-0.36)]:
    ax.plot([x],[0],'o', color=MUTED, ms=3.6, zorder=6)
    ax.annotate(lab, (x,dy), ha='center', color=MUTED, fontsize=8.8)
ax.plot([O[0]],[0],'o',color=INK, ms=4, zorder=6)
ax.annotate('$O$', (O[0],-0.34), ha='center', color=INK, fontsize=8.8)
ax.annotate('$A$', (A[0]-0.16, A[1]+0.14), color=INK, fontsize=8.8, ha='right')
ax.annotate('$B$', (B[0]+0.16, B[1]+0.16), color=INK, fontsize=8.8)
ax.annotate('glass, index $n$', (0.0, -1.42), ha='center', color=ACCENT, fontsize=8.6)
ax.annotate('air', (-2.4, 0.95), ha='center', color=MUTED, fontsize=8.6)
ax.annotate('air', (2.4, 0.95), ha='center', color=MUTED, fontsize=8.6)
ax.set_xlim(-5.4, 5.2); ax.set_ylim(-1.70, 1.45); ax.axis('off')
```
::: derivation Lens maker's formula
We start from the single-surface equation just derived, apply it twice, and reach the formula
that connects a lens's focal length to its shape and its glass.

**Setting up.** A thin lens of material index $n$ sits in air. Its faces have radii $R_1$ (the
first surface the light meets) and $R_2$. A real object is at $u$; the first surface alone would
form an image at $v_1$, which the second surface then uses as *its* object to form the final
image at $v$.

**Step 1 — apply the single-surface equation to the first face.** Light goes from air into
glass, so $n_1 = 1$, $n_2 = n$, radius $R_1$, image distance $v_1$:

$$ \frac{n}{v_1} - \frac{1}{u} = \frac{n - 1}{R_1} \qquad (1) $$

**Step 2 — apply it again to the second face.** Now light goes from glass into air, so
$n_1 = n$, $n_2 = 1$, radius $R_2$, and the object is $I_1$. Because the lens is **thin**, the
distance of $I_1$ from the second surface is still $v_1$:

$$ \frac{1}{v} - \frac{n}{v_1} = \frac{1 - n}{R_2} \qquad (2) $$

**Step 3 — add equations (1) and (2).** We add rather than subtract because the $n/v_1$ terms
have opposite signs and so will cancel:

$$ \frac{n}{v_1} - \frac{1}{u} + \frac{1}{v} - \frac{n}{v_1}
= \frac{n-1}{R_1} + \frac{1-n}{R_2} $$

**Step 4 — cancel the two $n/v_1$ terms on the left.** The intermediate image has now
disappeared from the problem entirely:

$$ \frac{1}{v} - \frac{1}{u} = \frac{n-1}{R_1} + \frac{1-n}{R_2} $$

**Step 5 — rewrite $(1-n)$ as $-(n-1)$** so that the same factor appears in both terms:

$$ \frac{1}{v} - \frac{1}{u} = \frac{n-1}{R_1} - \frac{n-1}{R_2} $$

**Step 6 — take out the common factor $(n-1)$:**

$$ \frac{1}{v} - \frac{1}{u} = (n-1)\left(\frac{1}{R_1} - \frac{1}{R_2}\right) $$

**Step 7 — now specialise to an object at infinity.** Then $1/u = 0$, and by the definition of
focal length the image forms at $v = f$:

$$ \frac{1}{f} - 0 = (n-1)\left(\frac{1}{R_1} - \frac{1}{R_2}\right) $$

**Step 8 — write it out:**

$$ \boxed{\frac{1}{f} = (n-1)\left(\frac{1}{R_1} - \frac{1}{R_2}\right)} $$

**Step 9 — recover the thin lens formula.** The right-hand side of Step 6 is now known to equal
$1/f$, so

$$ \frac{1}{v} - \frac{1}{u} = \frac{1}{f} $$

**Result.**

$$ \frac{1}{f} = (n-1)\left(\frac{1}{R_1} - \frac{1}{R_2}\right),
\qquad \frac{1}{v} - \frac{1}{u} = \frac{1}{f} $$

**What it means.** A lens's power comes from two things only: how different its glass is from the
surroundings ($n - 1$) and how sharply its faces are curved. Make either bigger and $f$ gets
shorter. Notice also that a lens immersed in a liquid of the same index ($n - 1 \to 0$) has
$f = \infty$ — it becomes invisible and does nothing.

**Conditions used.** The lens is **thin** (Step 2 needs the two surfaces to be at effectively the
same place), rays are paraxial, light is monochromatic, and the surrounding medium is air.
:::

::: tip The examiner is looking for
1. The single-surface equation quoted correctly.
2. Its application to the **first** surface, with $n_1 = 1$, $n_2 = n$.
3. Its application to the **second** surface, with $n_1 = n$, $n_2 = 1$, **and the sentence
   explaining that the lens is thin** so the intermediate image distance is unchanged.
4. Adding the two equations and cancelling $n/v_1$.
5. Putting $u = \infty$, $v = f$ to reach the boxed result.
:::

If the lens of index $n_l$ sits in a medium of index $n_m$ the same derivation
gives

$$ \frac{1}{f} = \left(\frac{n_l}{n_m} - 1\right)\left(\frac{1}{R_1} - \frac{1}{R_2}\right) $$

::: caution Do not forget the sign of $R_2$
For a bi-convex lens, $R_1$ is positive and $R_2$ is **negative**, so
$1/R_1 - 1/R_2$ is a *sum* of two positive terms. Students who write
$1/R_1 - 1/R_2 = 1/20 - 1/20 = 0$ for an equiconvex lens have forgotten the
convention and get $f = \infty$.
:::

::: example Worked example 17.3
**Problem.** An equiconvex lens of glass ($n = 1.5$) has faces of radius
$20\ \text{cm}$. Find its focal length in air, and its focal length when the
whole lens is immersed in water ($n_w = 4/3$).

**Solution.** For an equiconvex lens $R_1 = +20\ \text{cm}$ and
$R_2 = -20\ \text{cm}$, so

$$ \frac{1}{R_1} - \frac{1}{R_2} = \frac{1}{20} + \frac{1}{20} = \frac{1}{10}\ \text{cm}^{-1} $$

**In air:**

$$ \frac{1}{f} = (1.5-1)\times\frac{1}{10} = \frac{1}{20}
\;\Rightarrow\; f = 20\ \text{cm} $$

**In water:**

$$ \frac{1}{f_w} = \left(\frac{1.5}{4/3}-1\right)\times\frac{1}{10}
 = (1.125-1)\times\frac{1}{10} = 0.0125\ \text{cm}^{-1} $$

so $f_w = 80\ \text{cm}$. The lens is four times weaker in water, because the
glass–water index contrast is much smaller than the glass–air one. This is
exactly why your eyes cannot focus under water.
:::

## 17.3 Power of a lens

A short focal length bends light strongly. It is therefore convenient to grade
lenses by the reciprocal of the focal length.

::: definition Power of a lens
The power of a lens is the reciprocal of its focal length expressed in metres:

$$ P = \frac{1}{f\ (\text{in m})} $$

Its SI unit is the **dioptre** (D); $1\ \text{D} = 1\ \text{m}^{-1}$. A convex
lens has positive power, a concave lens negative power.
:::

So $f = 50\ \text{cm} = 0.5\ \text{m}$ gives $P = +2\ \text{D}$, and
$f = -25\ \text{cm}$ gives $P = -4\ \text{D}$. Combining with the lens maker's
formula,

$$ P = (n-1)\left(\frac{1}{R_1} - \frac{1}{R_2}\right) $$

with the radii in metres.

::: derivation Lenses in contact
We start by tracing the light through the two lenses one at a time, and reach the focal length of
the pair treated as one lens.

**Setting up.** Two thin lenses of focal lengths $f_1$ and $f_2$ are placed in contact, so the
distance between them is zero. An object is at $u$. The first lens forms an intermediate image at
$v_1$; the second lens then uses that image as its own object and forms the final image at $v$.
Let $F$ be the focal length of the equivalent single lens.

**Step 1 — apply the lens formula to the first lens:**

$$ \frac{1}{v_1} - \frac{1}{u} = \frac{1}{f_1} \qquad (1) $$

**Step 2 — apply it to the second lens.** Its object is $I_1$, and because the lenses are in
contact the object distance for the second lens is the same $v_1$:

$$ \frac{1}{v} - \frac{1}{v_1} = \frac{1}{f_2} \qquad (2) $$

**Step 3 — add (1) and (2).** Again we add because the $1/v_1$ terms carry opposite signs:

$$ \frac{1}{v_1} - \frac{1}{u} + \frac{1}{v} - \frac{1}{v_1}
= \frac{1}{f_1} + \frac{1}{f_2} $$

**Step 4 — cancel the two $1/v_1$ terms:**

$$ \frac{1}{v} - \frac{1}{u} = \frac{1}{f_1} + \frac{1}{f_2} $$

**Step 5 — compare with the lens formula for the equivalent lens,**
$\dfrac{1}{v} - \dfrac{1}{u} = \dfrac{1}{F}$. The same object gives the same final image, so the
left-hand sides are identical:

$$ \frac{1}{F} = \frac{1}{f_1} + \frac{1}{f_2} $$

**Step 6 — restate in terms of power,** since $P = 1/f$:

$$ P = P_1 + P_2 $$

**Result.**

$$ \frac{1}{F} = \frac{1}{f_1} + \frac{1}{f_2}, \qquad P = P_1 + P_2,
\qquad m = m_1 \times m_2 $$

**What it means.** **Powers add; focal lengths do not.** Two $+2$ D lenses in contact make a
$+4$ D lens. Because a diverging lens has negative power, a $+5$ D lens combined with a $-2$ D
lens gives $+3$ D — this is how an optician builds any prescription out of a small stock of
lenses. The magnifications multiply, not add, because each lens magnifies what the previous one
produced.

**Conditions used.** Both lenses are **thin** and in **contact** (zero separation), rays are
paraxial, and the two lenses share the same principal axis. If they are separated by a distance
$d$ the extra term below is needed.
:::

If the two lenses are separated by a distance $d$, the result becomes

$$ \frac{1}{F} = \frac{1}{f_1} + \frac{1}{f_2} - \frac{d}{f_1 f_2},
\qquad P = P_1 + P_2 - d\,P_1P_2 $$

::: tip Powers add, focal lengths do not
In any numerical on lens combinations in contact, convert every focal length to
a power in dioptres first, add them algebraically (watch the minus signs), and
convert back at the end. It is faster and far less error-prone than adding
reciprocals.
:::

::: example Worked example 17.4
**Problem.** A student in Biratnagar can read comfortably only when the page is
at least $50\ \text{cm}$ from her eye. What spectacle lens will let her read at
the normal near point of $25\ \text{cm}$? If a protective lens of power
$-0.5\ \text{D}$ is cemented to it, what is the power and focal length of the
pair?

**Solution.** The spectacle lens must take an object at $25\ \text{cm}$ and form
a virtual image at her own near point, $50\ \text{cm}$, on the same side. So
$u = -25\ \text{cm}$ and $v = -50\ \text{cm}$.

$$ \frac{1}{f} = \frac{1}{v} - \frac{1}{u} = -\frac{1}{50} + \frac{1}{25}
 = \frac{-1+2}{50} = \frac{1}{50} $$

so $f = +50\ \text{cm} = 0.50\ \text{m}$ and

$$ P = \frac{1}{0.50} = +2.0\ \text{D} $$

a converging lens, the standard correction for **hypermetropia** (long sight).

With the protective lens in contact,

$$ P = P_1 + P_2 = 2.0 + (-0.5) = +1.5\ \text{D},
\qquad F = \frac{1}{1.5} = 0.667\ \text{m} = 66.7\ \text{cm} $$
:::

## Chapter summary

- Thin lens formula $\dfrac{1}{v} - \dfrac{1}{u} = \dfrac{1}{f}$ with linear
  magnification $m = h_i/h_o = v/u$, in the New Cartesian convention.
- A convex lens gives a real inverted image for any object beyond $F_1$, and a
  virtual magnified one inside $F_1$; a concave lens always gives a virtual,
  erect, diminished image.
- Angular magnification $M = \beta/\alpha$. For a simple microscope,
  $M = 1 + D/f$ (image at the near point) and $M = D/f$ (image at infinity),
  with $D = 25\ \text{cm}$.
- Refraction at one spherical surface: $\dfrac{n_2}{v} - \dfrac{n_1}{u} = \dfrac{n_2-n_1}{R}$.
- Lens maker's formula: $\dfrac{1}{f} = (n-1)\left(\dfrac{1}{R_1}-\dfrac{1}{R_2}\right)$;
  in a medium, replace $n$ by $n_l/n_m$.
- Power $P = 1/f$ (f in metres), unit dioptre; convex positive, concave negative.
- Lenses in contact: $\dfrac{1}{F} = \dfrac{1}{f_1}+\dfrac{1}{f_2}$, i.e.
  $P = P_1+P_2$ and $m = m_1m_2$; separated by $d$, $P = P_1+P_2-dP_1P_2$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The power of a lens of focal length $-25\ \text{cm}$ is <span class="marks">[1]</span>
   (a) $+4\ \text{D}$ (b) $-4\ \text{D}$ (c) $+0.25\ \text{D}$ (d) $-0.25\ \text{D}$
2. A convex lens of focal length $10\ \text{cm}$ is used as a magnifying glass with
   the image at the near point. Its magnifying power is <span class="marks">[1]</span>
   (a) $1.5$ (b) $2.5$ (c) $3.5$ (d) $10$
3. An equiconvex glass lens ($n = 1.5$) has focal length $20\ \text{cm}$ in air.
   Immersed in water ($n = 4/3$), its focal length becomes <span class="marks">[1]</span>
   (a) $20\ \text{cm}$ (b) $40\ \text{cm}$ (c) $60\ \text{cm}$ (d) $80\ \text{cm}$
4. For a real object, a concave lens always forms an image that is <span class="marks">[1]</span>
   (a) real and inverted (b) virtual, erect and diminished
   (c) virtual, erect and magnified (d) real and erect
5. A ray directed at the optical centre of a thin lens <span class="marks">[1]</span>
   (a) passes through the focus (b) emerges parallel to the axis
   (c) emerges undeviated (d) is totally reflected

::: note Answers to Group A
**1.** (b) — $P = 1/(-0.25\ \text{m}) = -4\ \text{D}$.
**2.** (c) — $M = 1 + D/f = 1 + 25/10 = 3.5$.
**3.** (d) — $(1.5/1.333-1)/(1.5-1) = 0.25$, so $f$ is multiplied by $4$.
**4.** (b) — the emergent rays always diverge, so the image is virtual, erect and smaller.
**5.** (c) — the two faces are locally parallel there, so the ray is only laterally shifted, and for a thin lens that shift is negligible.
:::

**Group B — Short answer (5 marks each)**

1. Define optical centre, principal focus and focal length of a thin lens. State
   the three rules used to construct ray diagrams and draw the diagram for an
   object placed between $F_1$ and $2F_1$ of a convex lens. <span class="marks">[5]</span>
2. An object $4\ \text{cm}$ high is placed $25\ \text{cm}$ from a converging lens
   of focal length $15\ \text{cm}$. Find the position, nature and size of the
   image. <span class="marks">[5]</span>
3. Define the power of a lens and its unit. Two thin lenses of powers
   $+5\ \text{D}$ and $-3\ \text{D}$ are placed in contact. Find the focal length
   of the combination and state whether it converges or diverges. <span class="marks">[5]</span>
4. Define angular magnification and show that, for a simple microscope with the
   final image at the least distance of distinct vision, $M = 1 + D/f$. <span class="marks">[5]</span>
5. A double convex lens has faces of radii $20\ \text{cm}$ and $30\ \text{cm}$ and
   is made of glass of refractive index $1.5$. Calculate its focal length and
   power. <span class="marks">[5]</span>

::: note Answers to Group B
**2.** $u = -25\ \text{cm}$, $f = +15\ \text{cm}$.
$\dfrac{1}{v} = \dfrac{1}{15} - \dfrac{1}{25} = \dfrac{5-3}{75} = \dfrac{2}{75}$,
so $v = +37.5\ \text{cm}$ (real, behind the lens).
$m = v/u = 37.5/(-25) = -1.5$, so $h_i = -1.5 \times 4 = -6\ \text{cm}$:
real, inverted, $6\ \text{cm}$ tall.

**3.** $P = P_1 + P_2 = 5 - 3 = +2\ \text{D}$, so $F = 1/2 = 0.5\ \text{m} = 50\ \text{cm}$.
The power is positive, so the combination **converges**.

**4.** See the derivation in §17.3 — the marks are for $M = \beta/\alpha = D/u_0$,
for substituting $v = -D$ in the lens formula, and for the final step
$D/u_0 = 1 + D/f$.

**5.** Taking the light to meet the $20\ \text{cm}$ face first,
$R_1 = +20\ \text{cm}$, $R_2 = -30\ \text{cm}$:

$$ \frac{1}{f} = (1.5-1)\left(\frac{1}{20}+\frac{1}{30}\right)
 = 0.5\times\frac{5}{60} = \frac{1}{24}\ \text{cm}^{-1} $$

So $f = 24\ \text{cm} = 0.24\ \text{m}$ and $P = 1/0.24 = +4.17\ \text{D}$.
:::

**Group C — Long answer (8 marks each)**

1. (a) Derive the lens maker's formula $\dfrac{1}{f} = (n-1)\left(\dfrac{1}{R_1}-\dfrac{1}{R_2}\right)$
   for a thin lens, starting from the formula for refraction at a single
   spherical surface. <span class="marks">[5]</span>
   (b) A plano-convex lens of glass of refractive index $1.5$ has a focal length
   of $30\ \text{cm}$. Find the radius of curvature of its curved face. <span class="marks">[3]</span>
2. (a) Define angular magnification and derive expressions for the magnifying
   power of a simple microscope when the final image is formed (i) at the near
   point and (ii) at infinity. <span class="marks">[5]</span>
   (b) A hand lens of focal length $5\ \text{cm}$ is used by a normal eye.
   Calculate its magnifying power in both cases and comment on which setting is
   more comfortable. <span class="marks">[3]</span>

::: note Answers to Group C
**1.(b)** Let light strike the flat face first: $R_1 = \infty$ and
$R_2 = -R$. Then

$$ \frac{1}{30} = (1.5-1)\left(0 + \frac{1}{R}\right) = \frac{0.5}{R} $$

so $R = 0.5 \times 30 = 15\ \text{cm}$. (The same answer follows if the curved
face is met first, with $R_1 = +R$, $R_2 = \infty$.)

**2.(b)** Near point: $M = 1 + D/f = 1 + 25/5 = 6$.
Infinity: $M = D/f = 25/5 = 5$.
The near-point setting gives the larger magnification, but the eye must
accommodate fully and tires quickly; the infinity setting ($M = 5$) is used for
prolonged viewing because the eye stays relaxed.
:::
