---
subject: Physics
grade: 11
unit: 18
title: Dispersion
hours: 3
area: Waves and Optics
---

White light is a mixture. A glass prism bends violet light a little more than
red light, so the mixture comes apart into a band of colours — this is
**dispersion**. The same effect that gives a rainbow over the Kathmandu valley
also spoils the image in a cheap lens, and most of this unit is about
understanding the spoiling and then curing it.

::: key The one fact behind the whole unit
Refractive index depends on wavelength: $n_{violet} > n_{red}$. Every result
here — angular dispersion, dispersive power, chromatic aberration, the
achromatic doublet — is that single fact worked through.
:::

## 18.1 Pure spectrum and dispersive power

### Dispersion by a prism

For a prism of small refracting angle $A$, the deviation of a ray is

$$ \delta = (n-1)A $$

Since $n$ is different for each colour, each colour is deviated by a different
amount and the emergent beam is spread into a **spectrum** with red deviated
least and violet most.

```figure caption="Dispersion of white light by a prism. Violet is deviated most, red least; the angular dispersion is $\theta = \delta_V - \delta_R$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.9))

V = np.array([[0.0,1.25],[-1.05,-0.55],[1.05,-0.55]])
ax.fill(V[:,0], V[:,1], color=ACCENT, alpha=0.10, lw=0)
ax.plot(np.append(V[:,0],V[0,0]), np.append(V[:,1],V[0,1]), color=INK, lw=1.4)
ax.annotate('$A$', (0.0, 0.70), ha='center', color=INK, fontsize=9.5)

P = (-0.52, 0.33); Q = (0.52, 0.33)
ax.annotate('', xy=P, xytext=(-2.75, 0.55),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.8,
                            shrinkA=0, shrinkB=0, mutation_scale=13))
ax.annotate('white light', (-2.78, 0.66), color=INK, fontsize=8.8, ha='left')
ax.plot([P[0],Q[0]],[P[1],Q[1]], color=MUTED, lw=1.5)

ax.plot([Q[0], 2.85],[Q[1], Q[1]-0.0952*(2.85-Q[0])],
        color=GRID, lw=1.1, ls=(0,(4,3)))
ax.annotate('undeviated direction', (2.88, 0.10), color=MUTED, fontsize=7.8, ha='left')

cols = ['#c0392b','#e07b39','#d4b106','#2e8b57','#1d6fb8','#4b3f9e','#6a0dad']
names = ['R','O','Y','G','B','I','V']
for k,(c,nm) in enumerate(zip(cols,names)):
    dy = -0.30 - 0.055*k
    xe, ye = 2.55, Q[1] + dy*(2.55-Q[0])
    ax.plot([Q[0], xe],[Q[1], ye], color=c, lw=1.6)
    if nm in ('R','V'):
        ax.annotate(nm, (xe+0.09, ye-0.04), color=c, fontsize=9.0)
ax.annotate('spectrum', (3.30, -0.62), color=INK, fontsize=8.6, ha='center')
ax.annotate(r'$\delta_R$', (2.38, -0.04), color='#c0392b', fontsize=9.2,
            ha='center', va='center')
ax.annotate(r'$\delta_V$', (1.55, -0.80), color='#6a0dad', fontsize=9.2)
ax.set_xlim(-2.95, 4.15); ax.set_ylim(-1.55, 1.45)
ax.set_aspect('equal'); ax.axis('off')
```

The **angular dispersion** between the extreme colours is

$$ \theta = \delta_V - \delta_R = (n_V - 1)A - (n_R - 1)A = (n_V - n_R)A $$

and the **mean deviation** is taken as that of yellow, the middle of the
spectrum:

$$ \delta_Y = (n_Y - 1)A $$

::: definition Dispersive power
The dispersive power $\omega$ of the material of a prism is the ratio of the
angular dispersion between two chosen colours to the mean deviation:

$$ \omega = \frac{\theta}{\delta_Y} = \frac{\delta_V - \delta_R}{\delta_Y}
 = \frac{n_V - n_R}{n_Y - 1} $$

It is a **pure number** (no unit, no dimensions) and depends only on the
material, not on the refracting angle of the prism.
:::

::: derivation Dispersive power is dimensionless and independent of the prism angle
We start from the thin-prism deviation formula and reach an expression for $\omega$ in which the
prism's own angle $A$ has disappeared.

**Step 1 — write the deviation of each colour** using $\delta = (n-1)A$ for the same thin prism.
The angle $A$ is the same for all three, only $n$ changes:

$$ \delta_V = (n_V - 1)A, \qquad \delta_R = (n_R - 1)A, \qquad \delta_Y = (n_Y - 1)A $$

**Step 2 — form the angular dispersion,** the spread between the extreme colours:

$$ \theta = \delta_V - \delta_R = (n_V - 1)A - (n_R - 1)A $$

**Step 3 — remove the brackets.** The two $-A$ terms cancel:

$$ \theta = n_V A - n_R A $$

**Step 4 — take out the common factor $A$:**

$$ \theta = (n_V - n_R)A $$

**Step 5 — form the ratio that defines $\omega$:**

$$ \omega = \frac{\theta}{\delta_Y} = \frac{(n_V - n_R)A}{(n_Y - 1)A} $$

**Step 6 — cancel $A$, which appears on the top and on the bottom:**

$$ \omega = \frac{n_V - n_R}{n_Y - 1} $$

**Result.**

$$ \theta = (n_V - n_R)A, \qquad \omega = \frac{n_V - n_R}{n_Y - 1} $$

**What it means.** Two things follow from Step 6. First, $\omega$ is a **ratio of refractive
indices**, and refractive index is itself a ratio of two speeds, so $\omega$ has no unit and no
dimensions. Second, $A$ cancelled, so $\omega$ is a property of the **glass alone**: a
$5^{\circ}$ prism and a $60^{\circ}$ prism of the same glass have the same dispersive power,
even though their spectra are very different in width.

**Conditions used.** A thin prism, so that $\delta = (n-1)A$ applies; the same three chosen
colours throughout; and yellow taken as the mean colour.
:::

Typical values: crown glass $\omega \approx 0.017$–$0.020$, flint glass
$\omega \approx 0.03$–$0.05$. Flint glass disperses roughly twice as strongly as
crown glass for the same mean deviation — the fact on which every achromatic
lens is built.

::: caution $\omega$ has nothing to do with the prism angle
$A$ cancels when you form the ratio. Two prisms of the same glass but angles
$5^{\circ}$ and $60^{\circ}$ have the *same* dispersive power even though their
spectra are very different in width.
:::

### Impure and pure spectrum

If white light from a wide slit simply falls on a prism and then on a screen, the
coloured bands overlap: each point of the slit produces its own complete
spectrum, displaced from the others. That is an **impure spectrum**.

::: definition Pure spectrum
A pure spectrum is one in which the light at each point of the spectrum is of a
single wavelength, so that no two colours overlap.
:::

```figure caption="Apparatus for a pure spectrum: narrow slit at the focus of the collimating lens $L_1$, prism at minimum deviation, and lens $L_2$ focusing each parallel colour beam to its own sharp line on the screen."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.2,2.8))

def lens(x, h, c=ACCENT):
    yy = np.linspace(-h, h, 100); sg = 1-(yy/h)**2
    XL = x-0.012-0.09*sg; XR = x+0.012+0.09*sg
    ax.fill(np.concatenate([XL, XR[::-1]]), np.concatenate([yy, yy[::-1]]),
            color=c, alpha=0.18, lw=0, zorder=3)
    ax.plot(np.concatenate([XL, XR[::-1]]), np.concatenate([yy, yy[::-1]]),
            color=INK, lw=1.2, zorder=4)

# --- slit
ax.plot([0,0],[0.10,1.05], color=INK, lw=3.2, zorder=5)
ax.plot([0,0],[-1.05,-0.10], color=INK, lw=3.2, zorder=5)
ax.annotate('slit $S$', (0.0,1.16), ha='center', color=INK, fontsize=8.5)

# --- collimator
lens(1.25, 0.66)
ax.annotate('$L_1$', (1.25,0.80), ha='center', color=INK, fontsize=8.8)
ax.annotate('collimator', (1.25,-1.16), ha='center', color=MUTED, fontsize=7.8)

# --- prism, tilted so the horizontal beam crosses it at minimum deviation
tlt = np.radians(-12.0)
Rm = np.array([[np.cos(tlt), -np.sin(tlt)], [np.sin(tlt), np.cos(tlt)]])
V0 = np.array([[3.05,1.15],[2.35,-0.60],[3.75,-0.60]])
Ctr = V0.mean(axis=0)
P = np.array([Ctr + Rm @ (v - Ctr) for v in V0])
ax.fill(P[:,0], P[:,1], color=ACCENT, alpha=0.10, lw=0, zorder=2)
ax.plot(np.append(P[:,0],P[0,0]), np.append(P[:,1],P[0,1]), color=INK, lw=1.3, zorder=4)
ax.annotate('prism', (2.90,-1.02), ha='center', color=MUTED, fontsize=7.8)

def cross(p0, d, q0, q1):
    e = q1 - q0
    s = np.linalg.solve(np.array([[d[0], -e[0]], [d[1], -e[1]]]), q0 - p0)
    return p0 + s[0]*d

uin  = Rm @ np.array([1.0, 0.0])          # inside the glass: parallel to the base
edge = [0.38, -0.04]
ent  = [cross(np.array([0.0, y]), np.array([1.0, 0.0]), P[0], P[1]) for y in edge]
ext  = [cross(E, uin, P[0], P[2]) for E in ent]

for y, E in zip(edge, ent):
    ax.plot([0.03, 1.22],[0, y], color=MUTED, lw=1.0, zorder=3)
    ax.plot([1.28, E[0]],[y, y], color=MUTED, lw=1.0, zorder=3)
for E, X in zip(ent, ext):
    ax.plot([E[0], X[0]],[E[1], X[1]], color=MUTED, lw=1.0, zorder=3)

# --- focusing lens and screen
xL2, fL2 = 4.30, 1.30
xS = xL2 + fL2
lens(xL2, 0.86)
ax.annotate('$L_2$', (xL2,1.00), ha='center', color=INK, fontsize=8.8)
ax.annotate('focusing lens', (xL2,-1.16), ha='center', color=MUTED, fontsize=7.8)

cols  = ['#c0392b','#d4b106','#2e8b57','#1d6fb8','#6a0dad']
slope = [-0.30, -0.40, -0.50, -0.60, -0.70]
for c, m in zip(cols, slope):
    yf = m*fL2
    for X in ext:
        yL = X[1] + m*(xL2-X[0])
        ax.plot([X[0], xL2],[X[1], yL], color=c, lw=1.15, zorder=3)
        ax.plot([xL2, xS],[yL, yf], color=c, lw=1.15, zorder=3)
    ax.plot([xS, xS+0.10],[yf, yf], color=c, lw=5.0,
            solid_capstyle='butt', zorder=6)

ax.plot([xS,xS],[-1.15,1.15], color=INK, lw=2.2, zorder=5)
ax.annotate('screen', (xS+0.58,0.0), color=INK, fontsize=8.5, rotation=90,
            va='center', ha='left')
ax.annotate('R', (xS+0.17,-0.39), color='#c0392b', fontsize=8.4, ha='left', va='center')
ax.annotate('V', (xS+0.17,-0.91), color='#6a0dad', fontsize=8.4, ha='left', va='center')
ax.set_xlim(-0.35, 6.30); ax.set_ylim(-1.45, 1.40); ax.axis('off')
```
::: memory Four conditions for a pure spectrum
1. The source slit must be **narrow**.
2. Light must fall on the prism as a **parallel beam** (slit at the focus of the
   collimating lens).
3. The prism must be set in the **minimum deviation** position.
4. A converging lens must bring each parallel emergent beam to its **own focus**
   on the screen, with the screen in the focal plane.
:::

::: example Worked example 18.1
**Problem.** A thin prism of angle $5^{\circ}$ is made of glass for which
$n_V = 1.532$, $n_Y = 1.523$ and $n_R = 1.514$. Find (a) the mean deviation,
(b) the angular dispersion between violet and red, and (c) the dispersive power.

**Solution.**

(a) $\delta_Y = (n_Y-1)A = (1.523-1)\times 5^{\circ} = 0.523 \times 5^{\circ} = 2.615^{\circ}$

(b) $\theta = (n_V-n_R)A = (1.532-1.514)\times 5^{\circ} = 0.018\times 5^{\circ} = 0.090^{\circ}$

(c) $\omega = \dfrac{\theta}{\delta_Y} = \dfrac{0.090}{2.615} = 0.0344$

Equivalently $\omega = \dfrac{n_V-n_R}{n_Y-1} = \dfrac{0.018}{0.523} = 0.0344$ —
the same number, and notice $A$ has vanished.
:::

## 18.2 Chromatic and spherical aberration

An **aberration** is any departure of a real image from the perfect, sharp,
undistorted image predicted by the paraxial theory.

### Chromatic aberration

From the lens maker's formula, $\dfrac{1}{f} = (n-1)\left(\dfrac{1}{R_1}-\dfrac{1}{R_2}\right)$.
Since $n_V > n_R$, we get $f_V < f_R$: a lens focuses violet nearer than red.
There is no single image plane, and a white object gives an image fringed with
colour.

```figure caption="Chromatic aberration. A converging lens brings violet to a focus at $F_V$ and red at $F_R$; the separation $f_R - f_V$ is the longitudinal chromatic aberration."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.1,2.9))

fV, fR = 1.55, 2.15
ax.plot([-2.5, 3.1], [0,0], color=MUTED, lw=0.9, zorder=1)
yy = np.linspace(-0.95,0.95,140); sg = 1-(yy/0.95)**2
XL = -0.03-0.12*sg; XR = 0.03+0.12*sg
ax.fill(np.concatenate([XL, XR[::-1]]), np.concatenate([yy, yy[::-1]]),
        color=ACCENT, alpha=0.14, lw=0, zorder=2)
ax.plot(np.concatenate([XL, XR[::-1]]), np.concatenate([yy, yy[::-1]]),
        color=INK, lw=1.3, zorder=3)

for h in (0.72, 0.36, -0.36, -0.72):
    ax.plot([-2.4, 0],[h, h], color=INK, lw=1.5, zorder=4)
    ax.annotate('', xy=(-1.35,h), xytext=(-1.9,h),
                arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.5,
                                shrinkA=0, shrinkB=0, mutation_scale=12))
    for f, c in ((fV,'#6a0dad'), (fR,'#c0392b')):
        xe = 2.95
        ax.plot([0, xe],[h, h - h*xe/f], color=c, lw=1.3, zorder=4)

ax.annotate('white\nlight', (-2.42, 1.10), ha='left', color=INK, fontsize=8.4)
for x, lab, c, xt in ((fV,'$F_V$','#6a0dad',1.15), (fR,'$F_R$','#c0392b',2.60)):
    ax.plot([x],[0],'o', color=c, ms=4.5, zorder=6)
    ax.annotate(lab, xy=(x, 0.05), xytext=(xt, 0.72), ha='center',
                color=c, fontsize=9.2, zorder=7,
                arrowprops=dict(arrowstyle='-|>', color=c, lw=0.9, mutation_scale=9))
for x in (fV, fR):
    ax.plot([x,x],[0,-0.46], color=GRID, lw=0.9, ls=':', zorder=2)
ax.annotate('', xy=(fR,-0.46), xytext=(fV,-0.46),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=1.0, mutation_scale=9))
ax.annotate(r'$f_R-f_V=\omega f$', ((fV+fR)/2, -0.74), ha='center',
            color=INK, fontsize=8.6)
ax.set_xlim(-2.6, 3.4); ax.set_ylim(-1.30, 1.45); ax.axis('off')
```

::: derivation Longitudinal chromatic aberration equals $\omega f$
We start from the lens maker's formula applied separately to violet and red light, and reach the
remarkably simple result that the gap between the two foci is just $\omega f$.

**Setting up.** The lens has a fixed shape, so write

$$ K = \frac{1}{R_1} - \frac{1}{R_2} $$

which is the same number for every colour. Only $n$ changes with colour. Let $f_V$, $f_R$, $f_Y$
be the focal lengths for violet, red and (mean) yellow light.

**Step 1 — lens maker's formula for violet and for red:**

$$ \frac{1}{f_V} = (n_V - 1)K, \qquad \frac{1}{f_R} = (n_R - 1)K $$

**Step 2 — subtract the second from the first:**

$$ \frac{1}{f_V} - \frac{1}{f_R} = (n_V - 1)K - (n_R - 1)K $$

**Step 3 — simplify the right side.** The two $-K$ terms cancel, then take out $K$:

$$ \frac{1}{f_V} - \frac{1}{f_R} = (n_V - n_R)K $$

**Step 4 — combine the left side over a common denominator:**

$$ \frac{f_R - f_V}{f_R f_V} = (n_V - n_R)K $$

**Step 5 — approximate the denominator.** For any usable lens $f_V$ and $f_R$ differ by less
than about one per cent, so their product is very close to the square of the mean focal length:

$$ f_R f_V \approx f_Y^{2} $$

**Step 6 — substitute that in:**

$$ \frac{f_R - f_V}{f_Y^{2}} = (n_V - n_R)K $$

**Step 7 — multiply both sides by $f_Y^{2}$:**

$$ f_R - f_V = (n_V - n_R)K f_Y^{2} $$

**Step 8 — get rid of $K$.** The lens maker's formula for yellow gives
$\dfrac{1}{f_Y} = (n_Y - 1)K$, so

$$ K f_Y = \frac{1}{n_Y - 1} $$

**Step 9 — split one $f_Y$ off in Step 7 and use Step 8:**

$$ f_R - f_V = (n_V - n_R)\cdot (K f_Y) \cdot f_Y
= \frac{n_V - n_R}{n_Y - 1}\,f_Y $$

**Step 10 — recognise the fraction as the dispersive power $\omega$:**

$$ f_R - f_V = \omega f_Y $$

**Result.**

$$ f_R - f_V = \omega f_Y $$

**What it means.** The separation of the violet and red foci depends on nothing but the
dispersive power of the glass and the mean focal length. So the defect cannot be cured by
grinding the surfaces differently — only by changing the glass, or by combining two glasses. A
crown-glass lens of $f = 20$ cm with $\omega = 0.018$ has its two foci $0.36$ cm apart.

**Conditions used.** A thin lens, paraxial rays, and $f_V \approx f_R \approx f_Y$ so that Step 5
is safe.
:::

Two kinds are distinguished: **longitudinal** (axial) chromatic aberration,
the distance $f_R-f_V$ along the axis, and **lateral** (transverse) chromatic
aberration, the difference in the *sizes* of the violet and red images on a
given screen, which shows up as coloured fringes at the edges of the image.

### Spherical aberration

A spherical surface is easy to grind but is not the ideal shape for focusing.
Rays striking the **marginal** (outer) zone of a lens are bent more than the
**paraxial** rays near the axis, so they cross the axis closer to the lens.
There is no point at which all rays meet; the smallest patch of light, the
**circle of least confusion**, is where the image is sharpest.

```figure caption="Spherical aberration. Marginal rays cross the axis at $F_M$, paraxial rays at $F_P$. The narrowest waist between them is the circle of least confusion."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.1,2.8))

ax.plot([-2.5, 3.2], [0,0], color=MUTED, lw=0.9, zorder=1)
yy = np.linspace(-1.0,1.0,140); sg = 1-(yy/1.0)**2
XL = -0.03-0.13*sg; XR = 0.03+0.13*sg
ax.fill(np.concatenate([XL, XR[::-1]]), np.concatenate([yy, yy[::-1]]),
        color=ACCENT, alpha=0.14, lw=0, zorder=2)
ax.plot(np.concatenate([XL, XR[::-1]]), np.concatenate([yy, yy[::-1]]),
        color=INK, lw=1.3, zorder=3)

xe = 3.05
for h, f, c in ((0.85,1.40,'#c0392b'), (-0.85,1.40,'#c0392b'),
                (0.30,2.30,SERIES[0]), (-0.30,2.30,SERIES[0])):
    ax.plot([-2.4, 0],[h, h], color=INK, lw=1.4, zorder=4)
    ax.plot([0, xe],[h, h - h*xe/f], color=c, lw=1.35, zorder=4)
ax.annotate('', xy=(-1.35,0.85), xytext=(-1.95,0.85),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.4,
                            shrinkA=0, shrinkB=0, mutation_scale=12))
ax.annotate('', xy=(-1.35,-0.30), xytext=(-1.95,-0.30),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.4,
                            shrinkA=0, shrinkB=0, mutation_scale=12))
ax.annotate('marginal rays', (-2.42, 1.06), ha='left', color='#c0392b', fontsize=8.3)
ax.annotate('paraxial rays', (-2.42, -0.72), ha='left', color=SERIES[0], fontsize=8.3)

for x, c in ((1.40,'#c0392b'), (2.30,SERIES[0])):
    ax.plot([x],[0],'o', color=c, ms=4.5, zorder=6)
ax.annotate('$F_M$', xy=(1.40, 0.07), xytext=(0.86, 0.62), ha='center',
            color='#c0392b', fontsize=9.0, zorder=7,
            arrowprops=dict(arrowstyle='-|>', color='#c0392b', lw=0.9,
                            mutation_scale=9, shrinkA=3, shrinkB=1))
ax.annotate('$F_P$', (2.30, 0.21), ha='center', color=SERIES[0], fontsize=9.0)
ax.plot([1.56,1.56],[-0.097,0.097], color=INK, lw=2.8, zorder=6)
ax.annotate('circle of least\nconfusion', (1.60, -0.98), ha='center',
            color=INK, fontsize=8.0)
ax.annotate('', xy=(1.56,-0.62), xytext=(1.60,-0.30),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=0.9, mutation_scale=9))
ax.set_xlim(-2.6, 3.5); ax.set_ylim(-1.45, 1.35); ax.axis('off')
```

| | Chromatic aberration | Spherical aberration |
|---|---|---|
| Cause | $n$ depends on wavelength | spherical surface, wide aperture |
| Occurs with monochromatic light? | No | Yes |
| Occurs in mirrors? | No | Yes |
| Depends on | dispersive power $\omega$ | aperture and shape of the lens |
| Remedy | achromatic doublet (crown + flint) | stops, crossed lens, plano-convex pair sharing the deviation, parabolic mirror, aplanatic lenses |

::: example Worked example 18.2
**Problem.** A convex lens of mean focal length $20\ \text{cm}$ is made of glass
of dispersive power $0.03$. Find its longitudinal chromatic aberration, and the
focal lengths for violet and red light.

**Solution.** The longitudinal chromatic aberration is

$$ f_R - f_V = \omega f_Y = 0.03 \times 20 = 0.60\ \text{cm} $$

Taking $f_Y = 20\ \text{cm}$ as the mean of the two,

$$ f_R = 20 + 0.30 = 20.30\ \text{cm}, \qquad f_V = 20 - 0.30 = 19.70\ \text{cm} $$

The violet focus lies $6\ \text{mm}$ closer to the lens than the red one.
:::

## 18.3 Achromatism and its applications

::: definition Achromatism
A combination of lenses (or prisms) is said to be achromatic when it brings two
chosen colours — usually red and violet — to the same focus, so that the
chromatic aberration between them is eliminated.
:::

::: derivation Condition for achromatism of two thin lenses in contact
We start from the rule for two lenses in contact and demand that the combination have the same
focal length for violet as for red. That single demand gives the condition.

**Setting up.** The two lenses have mean focal lengths $f_1$, $f_2$ and dispersive powers
$\omega_1$, $\omega_2$. Write $K_1$ and $K_2$ for their shape factors,
$K = \dfrac{1}{R_1} - \dfrac{1}{R_2}$.

**Step 1 — lenses in contact add their powers:**

$$ \frac{1}{F} = \frac{1}{f_1} + \frac{1}{f_2} $$

**Step 2 — write this for violet and for red separately:**

$$ \frac{1}{F_V} = \frac{1}{f_{1V}} + \frac{1}{f_{2V}}, \qquad
\frac{1}{F_R} = \frac{1}{f_{1R}} + \frac{1}{f_{2R}} $$

**Step 3 — impose the achromatic condition.** "Achromatic" means the two colours focus at the
same place, so $F_V = F_R$, and therefore $1/F_V = 1/F_R$:

$$ \frac{1}{f_{1V}} + \frac{1}{f_{2V}} = \frac{1}{f_{1R}} + \frac{1}{f_{2R}} $$

**Step 4 — move everything to the left and pair up each lens with itself:**

$$ \left(\frac{1}{f_{1V}} - \frac{1}{f_{1R}}\right)
+ \left(\frac{1}{f_{2V}} - \frac{1}{f_{2R}}\right) = 0 $$

**Step 5 — work out the first bracket.** Apply the lens maker's formula to lens 1 for each
colour and subtract, exactly as in the previous derivation:

$$ \frac{1}{f_{1V}} - \frac{1}{f_{1R}} = (n_{1V} - n_{1R})K_1 $$

**Step 6 — replace the index difference using the definition of dispersive power.** Since
$\omega_1 = \dfrac{n_{1V} - n_{1R}}{n_{1Y} - 1}$, multiplying across gives
$n_{1V} - n_{1R} = \omega_1(n_{1Y} - 1)$:

$$ \frac{1}{f_{1V}} - \frac{1}{f_{1R}} = \omega_1(n_{1Y} - 1)K_1 $$

**Step 7 — recognise $(n_{1Y} - 1)K_1$ as $1/f_1$,** by the lens maker's formula for the mean
colour:

$$ \frac{1}{f_{1V}} - \frac{1}{f_{1R}} = \frac{\omega_1}{f_1} $$

**Step 8 — repeat Steps 5–7 for the second lens:**

$$ \frac{1}{f_{2V}} - \frac{1}{f_{2R}} = \frac{\omega_2}{f_2} $$

**Step 9 — substitute both results into Step 4:**

$$ \boxed{\frac{\omega_1}{f_1} + \frac{\omega_2}{f_2} = 0} $$

**Result.**

$$ \frac{\omega_1}{f_1} + \frac{\omega_2}{f_2} = 0 $$

**What it means.** Dispersive power is always a positive number, so the only way the two terms can
cancel is for $f_1$ and $f_2$ to have **opposite signs**: one lens must converge and the other
diverge. The colour spread introduced by the first is then undone by the second, while a useful
net power survives because the two glasses have different $\omega$.

**Conditions used.** Both lenses are thin and in contact, and only two colours (violet and red)
are brought together — other colours are still slightly out of focus, a residual defect called
the *secondary spectrum*.
:::

Two consequences follow immediately.

- Dispersive powers are always positive, so $f_1$ and $f_2$ must have
  **opposite signs**: one lens must converge and the other diverge.
- $\dfrac{f_2}{f_1} = -\dfrac{\omega_2}{\omega_1}$. To leave a useful net power
  the two dispersive powers must differ, which is why the pair is made of
  **crown glass** (low $\omega$, convex) cemented to **flint glass**
  (high $\omega$, concave).

```figure caption="Achromatic doublet: a strong crown-glass convex lens cemented to a weaker flint-glass concave lens. The dispersion of the second cancels that of the first, so red and violet meet at the same focus $F$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.8))

ax.plot([-2.6, 3.3], [0,0], color=MUTED, lw=0.9, zorder=1)
h = 0.95
yy = np.linspace(-h, h, 160); sg = 1-(yy/h)**2
# crown convex : left face bulges left, right face at x = 0.05 + 0.20*sg
XL = -0.05 - 0.26*sg
XM =  0.05 + 0.20*sg
ax.fill(np.concatenate([XL, XM[::-1]]), np.concatenate([yy, yy[::-1]]),
        color=ACCENT, alpha=0.20, lw=0, zorder=2)
# flint concave : left face matches XM, right face nearly flat
XR = 0.30 + 0.0*sg
ax.fill(np.concatenate([XM, XR+0*yy]), np.concatenate([yy, yy[::-1]]),
        color='#d9534f', alpha=0.18, lw=0, zorder=2)
ax.plot(XL, yy, color=INK, lw=1.3, zorder=3)
ax.plot(XM, yy, color=INK, lw=1.1, zorder=3)
ax.plot([0.30,0.30], [-h,h], color=INK, lw=1.3, zorder=3)
ax.plot([XL[0],0.30],[-h,-h], color=INK, lw=1.3, zorder=3)
ax.plot([XL[-1],0.30],[h,h], color=INK, lw=1.3, zorder=3)

F = 2.35
for hh in (0.80, 0.40, -0.40, -0.80):
    ax.plot([-2.5, XL[np.argmin(abs(yy-hh))]],[hh, hh], color=INK, lw=1.5, zorder=4)
    ax.plot([0.30, 3.15],[hh, hh - hh*(3.15-0.30)/(F-0.30)], color='#c0392b',
            lw=2.0, zorder=4)
    ax.plot([0.30, 3.15],[hh, hh - hh*(3.15-0.30)/(F-0.30)], color='#6a0dad',
            lw=1.2, ls=(0,(4,3)), zorder=5)
ax.annotate('', xy=(-1.45,0.80), xytext=(-2.05,0.80),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.5,
                            shrinkA=0, shrinkB=0, mutation_scale=12))
ax.annotate('white light', (-2.52, 1.06), ha='left', color=INK, fontsize=8.4)
ax.plot([F],[0],'o', color=INK, ms=4.5, zorder=6)
ax.annotate('$F$', (F, 0.16), ha='center', color=INK, fontsize=9.2)
ax.annotate('red and violet\nfocus together', (3.15, 0.92), ha='right',
            color=INK, fontsize=8.0)
ax.annotate('crown\n(convex, $\\omega_1$)', (-0.55, -1.22), ha='center',
            color=ACCENT, fontsize=8.0)
ax.annotate('flint\n(concave, $\\omega_2$)', (0.95, -1.22), ha='center',
            color='#d9534f', fontsize=8.0)
ax.set_xlim(-2.7, 3.5); ax.set_ylim(-1.70, 1.35); ax.axis('off')
```

### Achromatic prism combinations

The same idea applied to prisms gives two useful devices.

| Device | What it must do | Condition |
|---|---|---|
| Achromatic prism combination | deviation without dispersion | $(n_V-n_R)A + (n'_V-n'_R)A' = 0$ |
| Direct-vision prism | dispersion without deviation | $(n_Y-1)A + (n'_Y-1)A' = 0$ |

In both, the second prism is inverted with respect to the first, so its
contribution has the opposite sign.

::: tip Which condition is which
"Achromatic" always means *the colours must not separate*, so the condition is
written in terms of the **dispersions**. "Direct vision" means *the beam must
come out straight*, so the condition is written in terms of the **deviations**.
:::

### Applications

- **Achromatic doublet objectives** in refracting telescopes, microscopes,
  binoculars and camera lenses — the standard cure for coloured fringes.
- **Direct-vision spectroscopes**, in which a train of crown and flint prisms
  spreads the spectrum while letting the observer look straight at the source.
- **Reflecting telescopes** avoid the problem completely: a mirror has no
  dispersion at all, which is why all large research telescopes use mirrors.
- Spectacle and projector lenses, where coloured edges would be objectionable.

::: example Worked example 18.3
**Problem.** An achromatic doublet of focal length $20\ \text{cm}$ is to be made
by cementing a crown-glass lens ($\omega_1 = 0.020$) to a flint-glass lens
($\omega_2 = 0.040$). Find the focal length and the power of each lens.

**Solution.** The achromatism condition gives

$$ \frac{\omega_1}{f_1} + \frac{\omega_2}{f_2} = 0
 \;\Rightarrow\; \frac{0.020}{f_1} = -\frac{0.040}{f_2}
 \;\Rightarrow\; f_2 = -2f_1 $$

Substituting into $\dfrac{1}{F} = \dfrac{1}{f_1}+\dfrac{1}{f_2}$ with
$F = 20\ \text{cm}$:

$$ \frac{1}{20} = \frac{1}{f_1} - \frac{1}{2f_1} = \frac{1}{2f_1}
 \;\Rightarrow\; f_1 = 10\ \text{cm} $$

and therefore $f_2 = -20\ \text{cm}$.

Check: $\dfrac{1}{10}-\dfrac{1}{20} = \dfrac{1}{20}$, so $F = 20\ \text{cm}$.

Powers: $P_1 = 1/0.10 = +10\ \text{D}$ (crown, convex) and
$P_2 = 1/(-0.20) = -5\ \text{D}$ (flint, concave), giving $P = +5\ \text{D}$.
:::

::: example Worked example 18.4
**Problem.** A crown-glass prism of refracting angle $10^{\circ}$
($n_Y = 1.52$) is to be combined with a flint-glass prism ($n'_Y = 1.65$) so
that white light passes through the pair without net deviation. Find the
refracting angle of the flint prism.

**Solution.** For no net deviation the two deviations must be equal and
opposite, so in magnitude

$$ (n_Y - 1)A = (n'_Y - 1)A' $$

$$ (1.52-1)\times 10^{\circ} = (1.65-1)\times A' $$

$$ 5.2^{\circ} = 0.65\,A' \;\Rightarrow\; A' = 8^{\circ} $$

The flint prism is placed inverted with respect to the crown prism. Because
flint has the larger dispersive power, the emergent light is still dispersed —
the combination gives **dispersion without deviation**, which is exactly what a
direct-vision spectroscope needs.
:::

## Chapter summary

- Dispersion happens because $n$ depends on wavelength, with $n_V > n_R$; for a
  thin prism $\delta = (n-1)A$.
- Angular dispersion $\theta = (n_V-n_R)A$; mean deviation $\delta_Y = (n_Y-1)A$.
- Dispersive power $\omega = \dfrac{n_V-n_R}{n_Y-1}$ — dimensionless, a property
  of the material only. Flint glass has roughly twice the $\omega$ of crown glass.
- A pure spectrum needs a narrow slit, a parallel incident beam, the prism at
  minimum deviation, and a lens focusing each colour separately on the screen.
- Chromatic aberration: $f_V < f_R$; longitudinal chromatic aberration $= \omega f$.
  Spherical aberration: marginal rays focus nearer than paraxial rays, leaving a
  circle of least confusion.
- Condition for achromatism of two thin lenses in contact:
  $\dfrac{\omega_1}{f_1} + \dfrac{\omega_2}{f_2} = 0$, so one lens must be convex
  (crown) and the other concave (flint).
- Prism pairs: $(n_V-n_R)A + (n'_V-n'_R)A' = 0$ gives deviation without
  dispersion; $(n_Y-1)A + (n'_Y-1)A' = 0$ gives dispersion without deviation.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The dispersive power of the material of a prism depends on <span class="marks">[1]</span>
   (a) the refracting angle (b) the angle of incidence
   (c) the material only (d) the height of the prism
2. For a prism of small refracting angle $A$, the deviation is <span class="marks">[1]</span>
   (a) $(n-1)A$ (b) $nA$ (c) $A/(n-1)$ (d) $(n+1)A$
3. The condition for achromatism of two thin lenses in contact is <span class="marks">[1]</span>
   (a) $\omega_1 f_1 + \omega_2 f_2 = 0$ (b) $\dfrac{\omega_1}{f_1}+\dfrac{\omega_2}{f_2}=0$
   (c) $\dfrac{f_1}{\omega_1}+\dfrac{f_2}{\omega_2}=0$ (d) $\omega_1 f_2 = \omega_2 f_1$
4. Chromatic aberration in a lens is caused by <span class="marks">[1]</span>
   (a) the spherical shape of the surfaces (b) a large aperture
   (c) the dependence of refractive index on wavelength (d) the thickness of the lens
5. Spherical aberration of a lens can be reduced by <span class="marks">[1]</span>
   (a) using monochromatic light (b) placing a stop to cut off marginal rays
   (c) increasing the aperture (d) cementing a flint lens to it

::: note Answers to Group A
**1.** (c) — $A$ cancels in $\omega = (n_V-n_R)/(n_Y-1)$.
**2.** (a) — the small-angle result derived from the prism formula.
**3.** (b) — obtained by setting $F_V = F_R$ for lenses in contact.
**4.** (c) — $n_V > n_R$ makes $f_V < f_R$; it persists even with perfect surfaces.
**5.** (b) — a stop blocks the marginal rays that focus too near the lens. (Option (d) cures chromatic, not spherical, aberration.)
:::

**Group B — Short answer (5 marks each)**

1. What is dispersion of light? Define dispersive power and show that it is a
   dimensionless quantity independent of the angle of the prism. <span class="marks">[5]</span>
2. The refractive indices of flint glass for violet, yellow and red light are
   $1.663$, $1.649$ and $1.635$. Calculate the dispersive power of the glass, and
   the angular dispersion produced by a flint prism of angle $6^{\circ}$. <span class="marks">[5]</span>
3. Distinguish between a pure and an impure spectrum, and state the conditions
   necessary for obtaining a pure spectrum. <span class="marks">[5]</span>
4. Distinguish between chromatic and spherical aberration. State one method of
   reducing each. <span class="marks">[5]</span>
5. A convex lens of focal length $25\ \text{cm}$ is made of glass of dispersive
   power $0.024$. Calculate its longitudinal chromatic aberration and the focal
   lengths for red and violet light. <span class="marks">[5]</span>

::: note Answers to Group B
**2.** $\omega = \dfrac{n_V-n_R}{n_Y-1} = \dfrac{1.663-1.635}{1.649-1}
= \dfrac{0.028}{0.649} = 0.0431$.

Angular dispersion $\theta = (n_V-n_R)A = 0.028 \times 6^{\circ} = 0.168^{\circ}$.

**5.** $f_R - f_V = \omega f = 0.024 \times 25 = 0.60\ \text{cm}$.
Hence $f_R = 25.30\ \text{cm}$ and $f_V = 24.70\ \text{cm}$.
:::

**Group C — Long answer (8 marks each)**

1. (a) What is achromatism? Derive the condition $\dfrac{\omega_1}{f_1}+\dfrac{\omega_2}{f_2}=0$
   for two thin lenses in contact to form an achromatic combination, and explain
   why one lens must be converging and the other diverging. <span class="marks">[5]</span>
   (b) An achromatic doublet of focal length $30\ \text{cm}$ is made from crown
   glass of dispersive power $0.018$ and flint glass of dispersive power $0.036$.
   Find the focal length of each lens. <span class="marks">[3]</span>
2. (a) What is chromatic aberration? Show that the longitudinal chromatic
   aberration of a thin lens is $\omega f$. <span class="marks">[5]</span>
   (b) For a certain lens the focal lengths for violet and red light are
   $19.6\ \text{cm}$ and $20.4\ \text{cm}$. Calculate the dispersive power of the
   glass. <span class="marks">[3]</span>

::: note Answers to Group C
**1.(b)** From $\dfrac{0.018}{f_1} = -\dfrac{0.036}{f_2}$ we get $f_2 = -2f_1$.
Then

$$ \frac{1}{30} = \frac{1}{f_1} - \frac{1}{2f_1} = \frac{1}{2f_1} $$

so $f_1 = +15\ \text{cm}$ (crown, convex) and $f_2 = -30\ \text{cm}$ (flint,
concave).

**2.(b)** The mean focal length is $f_Y \approx \sqrt{f_Vf_R} = \sqrt{19.6\times20.4}
= \sqrt{399.84} = 20.0\ \text{cm}$. Then

$$ \omega = \frac{f_R-f_V}{f_Y} = \frac{20.4-19.6}{20.0} = \frac{0.8}{20.0} = 0.04 $$
:::
