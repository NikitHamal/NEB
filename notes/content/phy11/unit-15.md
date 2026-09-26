---
subject: Physics
grade: 11
unit: 15
title: Refraction at plane surfaces
hours: 4
area: Waves and Optics
---

Light changes speed when it crosses from one transparent medium into another, and
wherever it meets the boundary obliquely that change of speed makes it change
direction. This bending is **refraction**. It is why a straw in a glass of water
looks broken, why a fish in the Bagmati is never quite where it seems to be, why
a glass slab shifts an image sideways, and — through total internal reflection —
why a thread of glass thinner than a hair can carry telephone calls across Nepal.
This unit develops the laws of refraction, the relations between refractive
indices, lateral shift and total internal reflection.

::: key The one equation behind the whole unit
Snell's law $n_1\sin i = n_2\sin r$. Every formula in this chapter — relative
refractive index, apparent depth, lateral shift, critical angle — is Snell's law
with different things known.
:::

## 15.1 Laws of refraction: Refractive index

When a ray of light travelling in medium 1 meets a plane boundary with medium 2,
part of it is reflected back and part enters medium 2 with a changed direction.
The angle between the incident ray and the normal is the **angle of incidence**
$i$; the angle between the refracted ray and the normal is the **angle of
refraction** $r$.

```figure caption="Refraction at a plane boundary. Going into the denser medium the ray bends towards the normal; coming out of it the ray bends away from the normal. The faint grey ray is the partially reflected light."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Arc
fig, axs = plt.subplots(1, 2, figsize=(5.2, 2.9))
n = 1.5
d2r = np.pi/180

def frame(ax, dens='left'):
    ax.add_patch(plt.Rectangle((-2.5, -2.4), 5.0, 2.4, color=ACCENT, alpha=0.10))
    ax.plot([-2.5, 2.5], [0, 0], color=INK, lw=1.7)
    ax.plot([0, 0], [-2.3, 2.3], color=MUTED, lw=0.9, ls=(0, (3, 2)))
    ax.text(0.14, 2.06, 'normal', fontsize=8.5, color=MUTED, ha='left')
    ax.text(-2.45, 1.75, 'air  (rarer)', fontsize=9, color=MUTED, ha='left')
    ax.text(-2.45 if dens == 'left' else 2.45, -2.18, 'glass  (denser)',
            fontsize=9, color=MUTED, ha=dens)
    ax.set_xlim(-2.6, 2.6); ax.set_ylim(-2.5, 2.5)
    ax.set_aspect('equal'); ax.axis('off')

def arrow(ax, p, q, c, lw=1.6):
    ax.annotate('', xy=tuple(q), xytext=tuple(p),
                arrowprops=dict(arrowstyle='-|>', color=c, lw=lw,
                                mutation_scale=12, shrinkA=0, shrinkB=0))

ax = axs[0]; frame(ax)
i = 55*d2r; r = np.arcsin(np.sin(i)/n)
arrow(ax, (-2.15*np.sin(i), 2.15*np.cos(i)), (0, 0), SERIES[0])
arrow(ax, (0, 0), (2.15*np.sin(r), -2.15*np.cos(r)), SERIES[1])
arrow(ax, (0, 0), (1.55*np.sin(i), 1.55*np.cos(i)), MUTED, 1.0)
ax.add_patch(Arc((0, 0), 1.7, 1.7, theta1=90, theta2=90 + np.degrees(i),
                 color=SERIES[0], lw=1.0))
ax.add_patch(Arc((0, 0), 1.7, 1.7, theta1=270, theta2=270 + np.degrees(r),
                 color=SERIES[1], lw=1.0))
a = (90 + np.degrees(i)/2)*d2r
ax.text(1.06*np.cos(a), 1.06*np.sin(a), '$i$', color=SERIES[0], fontsize=11,
        ha='center', va='center')
a = (270 + np.degrees(r)/2)*d2r
ax.text(1.06*np.cos(a), 1.06*np.sin(a), '$r$', color=SERIES[1], fontsize=11,
        ha='center', va='center')
ax.set_title('air $\\rightarrow$ glass:  $r < i$', fontsize=9.5)

ax = axs[1]; frame(ax, dens='right')
i2 = 30*d2r; r2 = np.arcsin(n*np.sin(i2))
arrow(ax, (-2.15*np.sin(i2), -2.15*np.cos(i2)), (0, 0), SERIES[0])
arrow(ax, (0, 0), (2.15*np.sin(r2), 2.15*np.cos(r2)), SERIES[1])
arrow(ax, (0, 0), (1.55*np.sin(i2), -1.55*np.cos(i2)), MUTED, 1.0)
ax.add_patch(Arc((0, 0), 1.7, 1.7, theta1=270 - np.degrees(i2), theta2=270,
                 color=SERIES[0], lw=1.0))
ax.add_patch(Arc((0, 0), 1.7, 1.7, theta1=90 - np.degrees(r2), theta2=90,
                 color=SERIES[1], lw=1.0))
a = (270 - np.degrees(i2)/2)*d2r
ax.text(1.06*np.cos(a), 1.06*np.sin(a), '$i$', color=SERIES[0], fontsize=11,
        ha='center', va='center')
a = (90 - np.degrees(r2)/2)*d2r
ax.text(1.10*np.cos(a), 1.10*np.sin(a), '$r$', color=SERIES[1], fontsize=11,
        ha='center', va='center')
ax.set_title('glass $\\rightarrow$ air:  $r > i$', fontsize=9.5)
```
::: definition The laws of refraction
**First law.** The incident ray, the refracted ray and the normal to the surface
at the point of incidence all lie in the same plane.

**Second law (Snell's law).** For two given media and light of a given colour, the
ratio of the sine of the angle of incidence to the sine of the angle of
refraction is a constant:

$$ \frac{\sin i}{\sin r} = {}_1n_2 = \text{constant} $$

This constant is the **refractive index of medium 2 with respect to medium 1**.
:::

### Why light bends: refractive index and speed

Refraction happens because light travels at different speeds in different media.
If $v_1$ and $v_2$ are the speeds in the two media, it can be shown that

$$ {}_1n_2 = \frac{\sin i}{\sin r} = \frac{v_1}{v_2} = \frac{\lambda_1}{\lambda_2} $$

The **frequency does not change** on refraction — it is fixed by the source — so
if the speed falls, the wavelength must fall in the same ratio.

::: definition Absolute refractive index
The **absolute refractive index** $n$ of a medium is the refractive index of that
medium with respect to vacuum:

$$ n = \frac{c}{v} $$

where $c = 3\times10^{8}\ \text{m s}^{-1}$ is the speed of light in vacuum and $v$
is its speed in the medium. Since $v < c$ always, $n > 1$ for every material
medium. $n$ has no unit.
:::

In terms of absolute refractive indices, Snell's law takes its most useful form:

$$ n_1\sin i = n_2\sin r $$

| Medium | Absolute refractive index $n$ | Speed of light ($10^{8}$ m s⁻¹) |
|---|---|---|
| Vacuum | 1 (exactly) | 3.00 |
| Air (at STP) | 1.0003 | 3.00 |
| Ice | 1.31 | 2.29 |
| Water | 1.33 ($= 4/3$) | 2.26 |
| Crown glass | 1.52 | 1.97 |
| Dense flint glass | 1.65 | 1.82 |
| Diamond | 2.42 | 1.24 |

A medium of larger $n$ is called **optically denser**. Optical density is not the
same as mass density: turpentine ($n = 1.47$) is optically denser than water but
less dense in kg m⁻³.

::: caution "Bends towards the normal" — which way?
Going from rarer to denser (air → glass) the ray slows down and bends **towards**
the normal, so $r < i$. Going from denser to rarer (glass → air) it speeds up and
bends **away** from the normal, so $r > i$. A ray striking the surface normally
($i = 0$) is not bent at all, though its speed still changes.
:::

::: example Worked example 15.1
**Problem.** A ray of light of wavelength $600\ \text{nm}$ in air strikes a glass
surface at $60^{\circ}$ to the normal. The refractive index of the glass is
$1.5$. Find (a) the angle of refraction, (b) the speed of light in the glass,
(c) the wavelength and frequency of the light inside the glass.

**Solution.**

(a) By Snell's law, $1 \times \sin 60^{\circ} = 1.5\sin r$, so

$$ \sin r = \frac{0.8660}{1.5} = 0.5774 \qquad \Rightarrow \qquad r = 35.3^{\circ} $$

(b) $n = c/v$, so

$$ v = \frac{c}{n} = \frac{3\times10^{8}}{1.5} = 2\times10^{8}\ \text{m s}^{-1} $$

(c) The wavelength shrinks in the same ratio as the speed:

$$ \lambda_{glass} = \frac{\lambda_{air}}{n} = \frac{600}{1.5} = 400\ \text{nm} $$

The frequency is unchanged:
$f = c/\lambda_{air} = (3\times10^{8})/(600\times10^{-9}) = 5\times10^{14}\ \text{Hz}$.
Check: $v/\lambda_{glass} = (2\times10^{8})/(400\times10^{-9}) = 5\times10^{14}\ \text{Hz}$ — the same.
:::

## 15.2 Relation between refractive indices

Three relations follow directly from the definitions and are asked as standard
five-mark questions.

::: derivation The three relations between refractive indices
We start from Snell's law and the principle of reversibility, and reach three results that
let you convert freely between any pair of media.

**Part (a): ${}_1n_2 = n_2/n_1 = v_1/v_2$**

**Step 1 — Snell's law in its two-medium form.** For a ray passing from medium 1 (angle $i$)
into medium 2 (angle $r$):

$$ n_1\sin i = n_2\sin r $$

**Step 2 — make $\sin i/\sin r$ the subject.** Divide both sides by $n_1\sin r$:

$$ \frac{\sin i}{\sin r} = \frac{n_2}{n_1} $$

**Step 3 — name the left-hand side.** By definition, $\sin i/\sin r$ for this pair of media
*is* the refractive index of 2 with respect to 1:

$$ {}_1n_2 = \frac{n_2}{n_1} $$

**Step 4 — bring in the speeds.** Absolute index is defined as $n = c/v$, so
$n_1 = c/v_1$ and $n_2 = c/v_2$. Substituting:

$$ {}_1n_2 = \frac{c/v_2}{c/v_1} $$

**Step 5 — cancel $c$ and flip the divided fraction:**

$$ {}_1n_2 = \frac{v_1}{v_2} $$

---

**Part (b): ${}_1n_2 \times {}_2n_1 = 1$**

**Step 6 — state the principle of reversibility.** If the direction of a ray is exactly
reversed, it retraces its own path. So send a ray *back* from medium 2 along the old
refracted ray. It now strikes the boundary at angle $r$ and must emerge along the old
incident ray, at angle $i$.

**Step 7 — apply the definition to this reversed journey.** The ray now goes from 2 to 1, so
the angle in medium 2 is the incidence angle and the angle in medium 1 is the refraction
angle:

$$ {}_2n_1 = \frac{\sin r}{\sin i} $$

**Step 8 — compare with ${}_1n_2 = \sin i/\sin r$ from Step 3.** The right-hand side of
Step 7 is the reciprocal of the right-hand side of Step 3:

$$ {}_2n_1 = \frac{1}{{}_1n_2} $$

**Step 9 — multiply both sides by ${}_1n_2$:**

$$ {}_1n_2 \times {}_2n_1 = 1 $$

---

**Part (c): the chain relation**

**Step 10 — write each relative index as a ratio of absolute indices,** using Part (a):

$$ {}_1n_2 \times {}_2n_3 = \frac{n_2}{n_1}\times\frac{n_3}{n_2} $$

**Step 11 — cancel $n_2$, which appears once on top and once below:**

$$ {}_1n_2 \times {}_2n_3 = \frac{n_3}{n_1} $$

**Step 12 — recognise the right-hand side** as ${}_1n_3$, again by Part (a):

$$ {}_1n_2 \times {}_2n_3 = {}_1n_3 $$

**Step 13 — multiply both sides by ${}_3n_1$** and use Part (b) on the right, since
${}_1n_3 \times {}_3n_1 = 1$:

$$ {}_1n_2 \times {}_2n_3 \times {}_3n_1 = 1 $$

**Result.**

$$ {}_1n_2 = \frac{n_2}{n_1} = \frac{v_1}{v_2}, \qquad
{}_1n_2 \times {}_2n_1 = 1, \qquad
{}_1n_2 \times {}_2n_3 \times {}_3n_1 = 1 $$

**What it means.** You only ever need a table of *absolute* indices; any relative index is a
ratio of two of them. Part (b) says glass-with-respect-to-water is the exact reciprocal of
water-with-respect-to-glass, and Part (c) says a chain of media closing back on itself
multiplies to one — like walking round a loop and returning to the same height.

**Conditions used.** A single wavelength (since $n$ depends on colour), and media that are
transparent and uniform.
:::

::: tip Reading the subscripts
$_1n_2$ always means "the refractive index of 2 **with respect to** 1", and equals
$n_2/n_1$ — the *second* subscript goes on top. Getting this upside down turns
$1.5$ into $0.67$ and is the commonest slip in this section.
:::

### Refractive index from real and apparent depth

```figure caption="Real and apparent depth. Rays from the coin at $O$ bend away from the normal as they leave the water, so to the eye above they seem to come from the shallower point $I$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle
fig, ax = plt.subplots(figsize=(4.4, 3.4))
n = 4/3.0
H = 3.0
ax.add_patch(plt.Rectangle((-2.4, -H), 4.8, H, color=ACCENT, alpha=0.10))
ax.plot([-2.4, 2.4], [0, 0], color=ACCENT, lw=1.6)
ax.plot([-2.4, -2.4, 2.4, 2.4], [1.0, -H, -H, 1.0], color=INK, lw=1.8)

xq = 0.7
th = np.arctan(xq/H)
rr = np.arcsin(n*np.sin(th))
yI = -xq/np.tan(rr)
ax.plot([0, 0], [-H, 2.45], color=SERIES[1], lw=1.4, zorder=3)
ax.annotate('', xy=(0, 1.6), xytext=(0, 0.6),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.4, mutation_scale=11))
ax.plot([0, xq], [-H, 0], color=SERIES[1], lw=1.4, zorder=3)
ax.annotate('', xy=(0.42*xq, -H + 0.42*H), xytext=(0.30*xq, -H + 0.30*H),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.4, mutation_scale=11))
xe = xq + (2.45 - 0)*np.tan(rr)
yr = 1.90
xr = xq + yr*np.tan(rr)
ax.plot([xq, xr], [0, yr], color=SERIES[1], lw=1.4, zorder=3)
ax.annotate('', xy=(xq + 0.66*(xr - xq), 0.66*yr), xytext=(xq + 0.52*(xr - xq), 0.52*yr),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.4, mutation_scale=11))
ax.plot([0, xq], [yI, 0], color=MUTED, lw=1.0, ls=(0, (3, 2)), zorder=2)
ax.plot([0, 0], [-2.3, 0.9], color=MUTED, lw=0.8, ls=(0, (2, 2)), zorder=1)

ax.plot([0], [-H], 'o', color=INK, ms=7, zorder=5)
ax.annotate('O  (coin)', (0, -H), textcoords='offset points', xytext=(9, 5),
            color=INK, fontsize=9)
ax.plot([0], [yI], 'o', color='#A8271F', ms=6, mfc='none', zorder=5)
ax.annotate('I', (0, yI), textcoords='offset points', xytext=(-14, -4),
            color='#A8271F', fontsize=10)
ax.add_patch(Ellipse((xe - 0.1, 2.2), 0.95, 0.46, fc='none', ec=INK, lw=1.2))
ax.add_patch(Circle((xe - 0.1, 2.2), 0.14, color=INK))
ax.annotate('', xy=(-1.85, -H), xytext=(-1.85, 0),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=1.1, mutation_scale=9))
ax.text(-1.95, -H/2, 'real depth', rotation=90, va='center', ha='right',
        fontsize=9, color=INK)
ax.annotate('', xy=(-1.0, yI), xytext=(-1.0, 0),
            arrowprops=dict(arrowstyle='<|-|>', color='#A8271F', lw=1.1, mutation_scale=9))
ax.text(-1.1, yI/2, 'apparent depth', rotation=90, va='center', ha='right',
        fontsize=9, color='#A8271F')
ax.text(1.35, -2.6, 'water', fontsize=9, color=MUTED)
ax.set_xlim(-2.7, 2.8); ax.set_ylim(-3.3, 2.7)
ax.set_aspect('equal'); ax.axis('off')
```

::: derivation $n = \dfrac{\text{real depth}}{\text{apparent depth}}$
We start from Snell's law applied to a ray leaving the water, and reach a way of measuring
$n$ with nothing but a ruler.

**Setting up.** A coin lies at $O$, a depth $OA$ vertically below $A$ on the flat surface of
water of refractive index $n$. Take two rays from the coin: $OA$ straight up along the normal,
which passes out undeviated, and $OQ$ making a small angle $\theta$ with the normal.

**Step 1 — apply Snell's law at $Q$.** The ray goes from water into air, so the water term
carries $n$ and the air term carries 1. Let $\phi$ be the angle in air:

$$ n\sin\theta = 1 \times \sin\phi $$

**Step 2 — make $n$ the subject:**

$$ n = \frac{\sin\phi}{\sin\theta} $$

**Step 3 — locate the image.** The emergent ray bends *away* from the normal (air is rarer,
so $\phi > \theta$). Produced backwards, it meets the normal $OA$ at a point $I$ above $O$.
The eye receives both rays as if they came from $I$, so $IA$ is the **apparent depth**.

**Step 4 — use the right-angled triangle $OAQ$,** right-angled at $A$, with $\theta$ at $O$:

$$ \tan\theta = \frac{AQ}{OA} $$

**Step 5 — use the right-angled triangle $IAQ$,** right-angled at $A$, with $\phi$ at $I$
(the angle at $I$ equals $\phi$ because $IQ$ is the emergent ray and $IA$ is parallel to the
normal at $Q$):

$$ \tan\phi = \frac{AQ}{IA} $$

**Step 6 — restrict to a nearly normal view.** If we look almost straight down, $\theta$ and
$\phi$ are both small, and for small angles $\sin x \approx \tan x$:

$$ \sin\theta \approx \tan\theta, \qquad \sin\phi \approx \tan\phi $$

**Step 7 — replace the sines in Step 2 by tangents:**

$$ n \approx \frac{\tan\phi}{\tan\theta} $$

**Step 8 — substitute Steps 4 and 5:**

$$ n \approx \frac{AQ/IA}{AQ/OA} $$

**Step 9 — divide the fractions.** $AQ$ cancels, and dividing by $AQ/OA$ means multiplying by
$OA/AQ$:

$$ n = \frac{OA}{IA} $$

**Step 10 — name the two lengths:**

$$ n = \frac{\text{real depth}}{\text{apparent depth}} $$

**Step 11 — how far the coin seems to rise.** The shift is the difference of the two depths,
and from Step 10, $IA = OA/n$:

$$ \text{shift} = OA - IA = OA - \frac{OA}{n} $$

**Step 12 — take out the common factor $OA$:**

$$ \text{shift} = OA\left(1 - \frac{1}{n}\right) $$

**Result.**

$$ n = \frac{\text{real depth}}{\text{apparent depth}}, \qquad
\text{apparent shift} = \text{real depth}\left(1 - \frac{1}{n}\right) $$

**What it means.** Because $n > 1$, the apparent depth is always *less* than the real depth —
a pond always looks shallower than it is, which is a genuine danger. Both lengths are
measured with a ruler, so this gives a simple laboratory method for $n$.

**Conditions used.** The viewing must be **nearly normal** (Step 6). If you look at the water
at a slant, the small-angle step fails and the simple ratio no longer holds. The surface must
also be flat and the liquid uniform.
:::

For several liquid layers stacked one above the other, each layer contributes its
own apparent depth, so the total apparent depth is $\sum t_i/n_i$.

::: example Worked example 15.2
**Problem.** A tank contains water ($n = 4/3$) to a depth of $12\ \text{cm}$, and
on top of the water floats a layer of oil ($n = 1.6$) of thickness $8\ \text{cm}$.
A coin lies at the bottom. By how much does the coin appear to be raised when
viewed from vertically above?

**Solution.** Each layer is treated separately.

$$ \text{apparent depth of water layer} = \frac{12}{4/3} = 9\ \text{cm} $$
$$ \text{apparent depth of oil layer} = \frac{8}{1.6} = 5\ \text{cm} $$

Total apparent depth $= 9 + 5 = 14\ \text{cm}$, while the real depth is
$12 + 8 = 20\ \text{cm}$.

$$ \text{apparent shift} = 20 - 14 = 6\ \text{cm} $$

The coin appears raised by $6\ \text{cm}$.
:::

## 15.3 Lateral shift

A **parallel-sided glass slab** (a glass block, a window pane) has two plane
faces that are parallel. A ray entering it is refracted twice — once in, once
out — and the two refractions cancel in direction but not in position.

```figure caption="A ray through a parallel-sided slab of thickness $t$. The emergent ray is parallel to the incident ray but displaced sideways by the lateral shift $d$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Arc
fig, ax = plt.subplots(figsize=(4.5, 3.4))
t, n = 2.0, 1.5
i = np.radians(45.0)
r = np.arcsin(np.sin(i)/n)
ideg, rdeg = np.degrees(i), np.degrees(r)
A = np.array([0.0, 1.2])
B = np.array([t, A[1] - t*np.tan(r)])
ui = np.array([np.cos(i), -np.sin(i)])
ax.add_patch(plt.Rectangle((0, -1.75), t, 3.75, color=ACCENT, alpha=0.11))
ax.plot([0, 0, t, t, 0], [-1.75, 2.0, 2.0, -1.75, -1.75], color=INK, lw=1.5)

S = A - 1.75*ui
ax.annotate('', xy=tuple(A), xytext=tuple(S),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[0], lw=1.6,
                            mutation_scale=12, shrinkA=0, shrinkB=0))
ax.annotate('', xy=tuple(B), xytext=tuple(A),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[0], lw=1.6,
                            mutation_scale=12, shrinkA=0, shrinkB=0))
E = B + 1.85*ui
ax.annotate('', xy=tuple(E), xytext=tuple(B),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[0], lw=1.6,
                            mutation_scale=12, shrinkA=0, shrinkB=0))
U = A + 3.55*ui
ax.plot([A[0], U[0]], [A[1], U[1]], color=MUTED, lw=1.0, ls=(0, (3, 2)))
ax.plot([-0.85, 0.85], [A[1], A[1]], color=MUTED, lw=0.9, ls=(0, (2, 2)))
ax.plot([t - 0.85, t + 0.95], [B[1], B[1]], color=MUTED, lw=0.9, ls=(0, (2, 2)))

P = B + 1.05*ui
foot = A + np.dot(P - A, ui)*ui
ax.annotate('', xy=tuple(P), xytext=tuple(foot),
            arrowprops=dict(arrowstyle='<|-|>', color='#A8271F', lw=1.4, mutation_scale=9))
Dm = (P + foot)/2 + 0.52*ui
ax.text(Dm[0], Dm[1], '$d$', ha='center', va='center', color='#A8271F', fontsize=11)
ax.add_patch(Arc(tuple(A), 1.4, 1.4, theta1=180 - ideg, theta2=180, color=SERIES[1], lw=1.0))
ax.text(A[0] - 0.86, A[1] + 0.36, '$i$', color=SERIES[1], fontsize=11)
ax.add_patch(Arc(tuple(A), 1.05, 1.05, theta1=-rdeg, theta2=0, color=SERIES[2], lw=1.0))
Rr, rb = 0.95, r/2
ax.text(A[0] + Rr*np.cos(rb), A[1] - Rr*np.sin(rb), '$r$', ha='center', va='center',
        color=SERIES[2], fontsize=11)
ax.add_patch(Arc(tuple(B), 1.05, 1.05, theta1=180 - rdeg, theta2=180, color=SERIES[2], lw=1.0))
ax.text(B[0] - Rr*np.cos(rb), B[1] + Rr*np.sin(rb), '$r$', ha='center', va='center',
        color=SERIES[2], fontsize=11)
ax.add_patch(Arc(tuple(B), 1.4, 1.4, theta1=-ideg, theta2=0, color=SERIES[1], lw=1.0))
ax.text(B[0] + 0.66, B[1] - 0.45, '$i$', color=SERIES[1], fontsize=11)
ax.annotate('A', tuple(A), textcoords='offset points', xytext=(-17, -19), color=INK, fontsize=10)
ax.annotate('B', tuple(B), textcoords='offset points', xytext=(7, 9), color=INK, fontsize=10)
ax.annotate('', xy=(t, -1.45), xytext=(0, -1.45),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=1.0, mutation_scale=9))
ax.text(t/2, -1.38, '$t$', ha='center', va='bottom', color=INK, fontsize=11)
ax.set_xlim(-1.5, 4.0); ax.set_ylim(-2.05, 2.6)
ax.set_aspect('equal'); ax.axis('off')
```
Because the faces are parallel, the normal at $B$ is parallel to the normal at
$A$. The angle of incidence inside the glass at $B$ equals $r$, so by Snell's law
at the second face $\sin i' = n\sin r = \sin i$, giving $i' = i$: **the emergent
ray is parallel to the incident ray**. The slab does not change the direction of
the light, only its line of travel. That sideways displacement is the **lateral
shift**.

::: derivation The lateral shift $d = t\,\dfrac{\sin(i-r)}{\cos r}$
We start by showing the emergent ray is parallel to the incident ray, then find how far
sideways it has been pushed.

**Setting up.** The slab has thickness $t$ and refractive index $n$. The ray enters at $A$
with angle of incidence $i$ and angle of refraction $r$, travels inside along $AB$, and leaves
at $B$ with angle of incidence $r$ (inside) and angle of emergence $e$.

**Step 1 — Snell's law at the first face,** air into glass:

$$ \frac{\sin i}{\sin r} = n $$

**Step 2 — why the angle inside at $B$ is also $r$.** The two faces are parallel, so their
normals are parallel. $AB$ cuts both normals, and alternate angles between parallel lines are
equal. So the angle of incidence inside the glass at $B$ equals $r$.

**Step 3 — Snell's law at the second face,** glass into air:

$$ \frac{\sin e}{\sin r} = n $$

**Step 4 — compare Steps 1 and 3.** Both left-hand sides equal $n$, so

$$ \frac{\sin e}{\sin r} = \frac{\sin i}{\sin r} $$

**Step 5 — cancel $\sin r$ and take the inverse sine:**

$$ e = i $$

So the emergent ray is **parallel** to the incident ray: the slab changes the ray's position
but not its direction. That is the first part of the Group C question.

---

**Now the shift itself.**

**Step 6 — define the shift.** Produce the incident ray straight on, as if the glass were not
there. Drop the perpendicular $BN$ from $B$ onto this undeviated line. Then

$$ d = BN $$

**Step 7 — find the angle at $B$ in triangle $ABN$.** $AN$ lies along the original direction,
which makes angle $i$ with the normal at $A$; $AB$ makes angle $r$ with the same normal. The
angle between them is therefore their difference:

$$ \angle BAN = i - r $$

**Step 8 — use the right-angled triangle $ABN$,** right-angled at $N$:

$$ \sin(i - r) = \frac{BN}{AB} = \frac{d}{AB} $$

**Step 9 — make $d$ the subject:**

$$ d = AB\,\sin(i - r) $$

**Step 10 — now find $AB$.** Drop the perpendicular $AM$ from $A$ onto the second face; its
length is the thickness of the slab, $AM = t$. In the right-angled triangle $ABM$ the angle at
$A$ is $r$ (both $AM$ and the normal at $A$ are perpendicular to the faces):

$$ \cos r = \frac{AM}{AB} = \frac{t}{AB} $$

**Step 11 — make $AB$ the subject:**

$$ AB = \frac{t}{\cos r} $$

**Step 12 — substitute this into Step 9:**

$$ d = \frac{t\,\sin(i - r)}{\cos r} $$

**Result.**

$$ e = i \qquad \text{and} \qquad d = \frac{t\,\sin(i - r)}{\cos r} $$

**What it means.** A window pane does not distort the direction of what you see, only shifts it
a little sideways — which is why you can read through a glass block at an angle without the
scene tilting. The shift grows with the thickness $t$ and with the angle of incidence.

**Conditions used.** The two faces must be **parallel** (Step 2 fails otherwise — that is why
a prism *does* deviate light), and the same medium (air) lies on both sides.
:::

::: tip The examiner is looking for
1. Snell's law written at **both** faces.
2. The statement that the angle inside at the second face is $r$, *because the faces are
   parallel*.
3. The conclusion $e = i$, i.e. emergent ray parallel to incident ray.
4. The construction of the perpendicular $BN$ and the identification $\angle BAN = i - r$.
5. $AB = t/\cos r$ from the second triangle.
6. The final substitution giving $d = t\sin(i-r)/\cos r$.
:::

Two special cases are worth noting:

- At **normal incidence** $i = r = 0$, so $d = 0$: a slab looked through
  straight-on shifts nothing sideways.
- At **grazing incidence** $i \to 90^{\circ}$, $r \to C$ (the critical angle) and
  $d \to t$: the shift is greatest and approaches the thickness of the slab.

For a slab viewed almost normally there is still a shift **along** the line of
sight — the **normal shift**. It is the same calculation as apparent depth:

$$ \text{normal shift} = t\left(1 - \frac{1}{n}\right) $$

so an object seen through a $6\ \text{cm}$ glass block ($n = 1.5$) appears
$6(1 - 1/1.5) = 2\ \text{cm}$ nearer than it really is.

::: example Worked example 15.3
**Problem.** A ray of light strikes a glass slab of thickness $6\ \text{cm}$ and
refractive index $1.5$ at an angle of incidence of $60^{\circ}$. Calculate the
angle of refraction and the lateral shift.

**Solution.** From Snell's law,

$$ \sin r = \frac{\sin 60^{\circ}}{1.5} = \frac{0.8660}{1.5} = 0.5774 \qquad \Rightarrow \qquad r = 35.26^{\circ} $$

Then $i - r = 60^{\circ} - 35.26^{\circ} = 24.74^{\circ}$, so
$\sin(i-r) = 0.4183$ and $\cos r = 0.8165$.

$$ d = \frac{t\sin(i-r)}{\cos r} = \frac{6 \times 0.4183}{0.8165} = 3.07\ \text{cm} $$

The emergent ray is parallel to the incident ray but displaced sideways by about
$3.1\ \text{cm}$.
:::

## 15.4 Total internal reflection

When light goes from a **denser** medium to a **rarer** one it bends away from
the normal, so $r > i$. Increase $i$ and $r$ grows faster, until at one particular
angle of incidence $r$ reaches $90^{\circ}$ and the refracted ray grazes along the
boundary. Beyond that angle there is no refracted ray at all: **all** the light
is reflected back into the denser medium.

```figure caption="Total internal reflection. As $i$ grows the refracted ray bends further from the normal; at $i = C$ it grazes the surface, and for $i > C$ no light escapes at all."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Arc
fig, ax = plt.subplots(figsize=(5.0, 3.1))
n = 1.5
C = np.degrees(np.arcsin(1/n))
h = 1.6
S = np.array([0.0, -h])
ax.add_patch(plt.Rectangle((-0.9, -2.0), 5.6, 2.0, color=ACCENT, alpha=0.11))
ax.plot([-0.9, 4.7], [0, 0], color=INK, lw=1.7)
ax.text(4.6, 1.12, 'air (rarer)', fontsize=9, color=MUTED, ha='right')
ax.text(4.6, -1.88, 'glass (denser)', fontsize=9, color=MUTED, ha='right')

for ideg, col in [(20.0, SERIES[0]), (C, SERIES[2]), (58.0, SERIES[1])]:
    irad = np.radians(ideg)
    Q = np.array([h*np.tan(irad), 0.0])
    ax.annotate('', xy=tuple(Q), xytext=tuple(S),
                arrowprops=dict(arrowstyle='-|>', color=col, lw=1.5,
                                mutation_scale=11, shrinkA=0, shrinkB=0))
    ax.plot([Q[0], Q[0]], [-1.15, 1.22], color=MUTED, lw=0.8, ls=(0, (2, 2)), zorder=0)
    s = n*np.sin(irad)
    if s < 0.999:
        rr = np.arcsin(s)
        ax.annotate('', xy=(Q[0] + 1.35*np.sin(rr), 1.35*np.cos(rr)), xytext=tuple(Q),
                    arrowprops=dict(arrowstyle='-|>', color=col, lw=1.5,
                                    mutation_scale=11, shrinkA=0, shrinkB=0))
    elif s < 1.001:
        ax.annotate('', xy=(Q[0] + 1.35, 0.06), xytext=(Q[0], 0.06),
                    arrowprops=dict(arrowstyle='-|>', color=col, lw=1.5,
                                    mutation_scale=11, shrinkA=0, shrinkB=0))
    strong = ideg > C + 0.5
    ax.annotate('', xy=(Q[0] + (1.6 if strong else 0.85)*np.sin(irad),
                        -(1.6 if strong else 0.85)*np.cos(irad)), xytext=tuple(Q),
                arrowprops=dict(arrowstyle='-|>', color=col,
                                lw=1.5 if strong else 0.9,
                                alpha=1.0 if strong else 0.5,
                                mutation_scale=11, shrinkA=0, shrinkB=0))

QC = h*np.tan(np.radians(C))
ax.add_patch(Arc((QC, 0), 1.15, 1.15, theta1=270 - C, theta2=270,
                 color=SERIES[2], lw=1.0))
ax.text(QC + 0.78*np.cos(np.radians(270 - C/2)), 0.78*np.sin(np.radians(270 - C/2)),
        '$C$', ha='center', va='center', color=SERIES[2], fontsize=11)
ax.plot([S[0]], [S[1]], 'o', color=INK, ms=6)
ax.annotate('S', tuple(S), textcoords='offset points', xytext=(-14, -3),
            color=INK, fontsize=10)
ax.text(0.30, 1.36, '$i < C$', color=SERIES[0], fontsize=9.5, ha='center')
ax.text(1.72, 0.32, '$i = C$', color=SERIES[2], fontsize=9.5, ha='left')
ax.text(3.35, -1.55, '$i > C$', color=SERIES[1], fontsize=9.5, ha='center')
ax.set_xlim(-1.1, 4.9); ax.set_ylim(-2.15, 1.7)
ax.set_aspect('equal'); ax.axis('off')
```
::: definition Critical angle and total internal reflection
The **critical angle** $C$ for a pair of media is the angle of incidence *in the
denser medium* for which the angle of refraction in the rarer medium is
$90^{\circ}$.

**Total internal reflection** is the complete reflection of light back into the
denser medium, which occurs when light travelling in the denser medium strikes
the boundary at an angle of incidence greater than the critical angle.
:::

::: memory The two conditions — both must hold
1. Light must travel from the **denser** medium towards the **rarer** medium.
2. The angle of incidence must be **greater than the critical angle**.
:::

::: derivation The critical angle: $\sin C = 1/n$
We start from Snell's law at the one special angle where the refracted ray just grazes the
boundary, and reach a relation between the critical angle and the refractive index.

**Setting up.** Light travels in a denser medium of absolute index $n_1$ and meets a rarer
medium of index $n_2$. By the definition of the critical angle, when the angle of incidence is
$C$ the angle of refraction is exactly $90^{\circ}$.

**Step 1 — write Snell's law for this boundary:**

$$ n_1\sin i = n_2\sin r $$

**Step 2 — substitute the critical condition** $i = C$ and $r = 90^{\circ}$:

$$ n_1\sin C = n_2\sin 90^{\circ} $$

**Step 3 — evaluate $\sin 90^{\circ} = 1$:**

$$ n_1\sin C = n_2 $$

**Step 4 — divide both sides by $n_1$:**

$$ \sin C = \frac{n_2}{n_1} $$

**Step 5 — take the usual case of a denser medium in air.** Then $n_2 = 1$ and we write
$n_1 = n$:

$$ \sin C = \frac{1}{n} $$

**Step 6 — invert to get $n$ from a measured $C$:**

$$ n = \frac{1}{\sin C} $$

**Result.**

$$ \sin C = \frac{n_2}{n_1}, \qquad \text{and against air} \qquad
\sin C = \frac{1}{n} \quad \text{or} \quad n = \frac{1}{\sin C} $$

**What it means.** A bigger $n$ makes $1/n$ smaller, so a denser material has a *smaller*
critical angle and traps light more easily — this is exactly why diamond sparkles. Step 4 also
explains why total internal reflection can never happen from rarer to denser: then
$n_2/n_1 > 1$, and no angle has a sine greater than 1, so no critical angle exists.

**Conditions used.** Light must be going from denser to rarer, and one wavelength at a time
(since $n$, and hence $C$, depends slightly on colour).
:::

| Denser medium (against air) | $n$ | Critical angle $C$ |
|---|---|---|
| Ice | 1.31 | $49.8^{\circ}$ |
| Water | 1.33 | $48.6^{\circ}$ |
| Crown glass | 1.52 | $41.1^{\circ}$ |
| Dense flint glass | 1.65 | $37.3^{\circ}$ |
| Diamond | 2.42 | $24.4^{\circ}$ |

The smaller the critical angle, the easier it is to trap light. Diamond has the
smallest $C$ of common materials, so light entering a cut diamond is reflected
many times inside before it escapes — that is its "fire".

**Applications**

| Application | How it uses total internal reflection |
|---|---|
| Optical fibre | A glass core of higher $n$ is coated with cladding of lower $n$; light striking the core–cladding boundary above $C$ is reflected over and over and travels kilometres with little loss. Used for internet backbones and endoscopes. |
| Totally reflecting prism | A $45^{\circ}$–$45^{\circ}$–$90^{\circ}$ glass prism has $C = 41.8^{\circ} < 45^{\circ}$, so it turns light through $90^{\circ}$ or $180^{\circ}$ with no silvering and no loss. Used in periscopes and binoculars. |
| Mirage | Hot air just above a road is less dense, so its $n$ is smaller. Light from the sky curves, is totally internally reflected in the air layers, and the road looks wet. |
| Shine of a diamond | $C = 24.4^{\circ}$, so most rays entering are trapped and emerge through the top facets. |
| Optical levelling and light pipes | Light follows a bent glass or plastic rod. |

::: caution Total internal reflection is not "partial reflection"
At *every* boundary a little light is reflected, whatever the angle. That is
ordinary partial reflection. Total internal reflection is different: past the
critical angle **100 %** of the light is reflected because a refracted ray is
geometrically impossible. It also cannot happen when light goes from rarer to
denser — there is no $i$ for which $r$ can reach $90^{\circ}$.
:::

::: example Worked example 15.4
**Problem.** A fish is at a depth of $2.0\ \text{m}$ in Phewa Lake
($n_{water} = 4/3$). Looking up, the fish sees the whole sky compressed into a
bright circular window on the surface. Find (a) the critical angle for water and
(b) the radius of that window.

**Solution.**

(a) $\sin C = 1/n = 3/4 = 0.75$, so

$$ C = \sin^{-1}(0.75) = 48.6^{\circ} $$

(b) Light can enter the water from the sky only within the cone of half-angle $C$
about the vertical through the fish. On the surface this cone cuts a circle of
radius $R$ where

$$ \tan C = \frac{R}{h} \qquad \Rightarrow \qquad R = h\tan C $$

With $\sin C = 0.75$, $\cos C = \sqrt{1 - 0.5625} = 0.6614$, so
$\tan C = 0.75/0.6614 = 1.134$. Hence

$$ R = 2.0 \times 1.134 = 2.27\ \text{m} $$

The window is about $4.5\ \text{m}$ across; outside it the fish sees only the
reflected lake bed.
:::

## Chapter summary

- Laws of refraction: incident ray, refracted ray and normal are coplanar; and
  $\dfrac{\sin i}{\sin r} = {}_1n_2$ (Snell's law), usually written
  $n_1\sin i = n_2\sin r$.
- Absolute refractive index $n = c/v$; also
  ${}_1n_2 = n_2/n_1 = v_1/v_2 = \lambda_1/\lambda_2$. Frequency never changes on
  refraction.
- Reversibility gives ${}_1n_2 = 1/{}_2n_1$, and the chain rule gives
  ${}_1n_2 \times {}_2n_3 \times {}_3n_1 = 1$.
- $n = \dfrac{\text{real depth}}{\text{apparent depth}}$ for near-normal viewing;
  apparent shift $= t(1 - 1/n)$, and layers add: apparent depth $= \sum t_i/n_i$.
- A parallel-sided slab leaves the direction unchanged but displaces the ray
  laterally by $d = \dfrac{t\sin(i-r)}{\cos r}$, which is zero at normal incidence.
- Total internal reflection needs light going denser → rarer with $i > C$, where
  $\sin C = n_2/n_1$, or $\sin C = 1/n$ against air.
- Optical fibres, totally reflecting prisms, mirages and the sparkle of diamond
  are all total internal reflection.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The refractive index of a medium in which light travels at $2.0\times10^{8}\ \text{m s}^{-1}$ is <span class="marks">[1]</span>
   (a) $1.33$ (b) $1.5$ (c) $1.6$ (d) $2.0$
2. When a ray of light passes from glass into air it <span class="marks">[1]</span>
   (a) bends towards the normal (b) bends away from the normal
   (c) is not deviated (d) is always totally reflected
3. The critical angle for a glass of refractive index $1.5$ is about <span class="marks">[1]</span>
   (a) $30^{\circ}$ (b) $42^{\circ}$ (c) $49^{\circ}$ (d) $60^{\circ}$
4. The lateral shift produced by a parallel-sided glass slab is zero when the angle of incidence is <span class="marks">[1]</span>
   (a) $0^{\circ}$ (b) $30^{\circ}$ (c) $45^{\circ}$ (d) $90^{\circ}$
5. A coin lies at the bottom of a beaker containing water ($n = 4/3$) $8\ \text{cm}$ deep. Seen from directly above it appears to be at a depth of <span class="marks">[1]</span>
   (a) $4\ \text{cm}$ (b) $6\ \text{cm}$ (c) $8\ \text{cm}$ (d) $10.7\ \text{cm}$
6. On passing from air into glass, the quantity that does **not** change is the <span class="marks">[1]</span>
   (a) speed (b) wavelength (c) frequency (d) direction

::: note Answers to Group A
**1.** (b) — $n = c/v = (3\times10^{8})/(2\times10^{8}) = 1.5$.
**2.** (b) — denser to rarer, so $r > i$.
**3.** (b) — $\sin C = 1/1.5 = 0.667$, $C = 41.8^{\circ}$.
**4.** (a) — $d = t\sin(i-r)/\cos r$ and $i = r = 0$ gives $d = 0$.
**5.** (b) — apparent depth $= 8/(4/3) = 6\ \text{cm}$.
**6.** (c) — frequency is set by the source; speed and wavelength both fall by the factor $n$.
:::

**Group B — Short answer (5 marks each)**

1. State the laws of refraction of light. Define absolute refractive index and
   relative refractive index, and write the relation between them. <span class="marks">[5]</span>
2. Using the principle of reversibility of light, show that
   ${}_1n_2 = 1/{}_2n_1$, and hence prove
   ${}_1n_2 \times {}_2n_3 \times {}_3n_1 = 1$. <span class="marks">[5]</span>
3. Derive the relation $n = \dfrac{\text{real depth}}{\text{apparent depth}}$ for
   a liquid viewed normally from above. <span class="marks">[5]</span>
4. A ray of light falls at $45^{\circ}$ on a glass slab $8\ \text{cm}$ thick of
   refractive index $1.5$. Calculate the angle of refraction and the lateral
   shift. <span class="marks">[5]</span>
5. Define critical angle and derive $\sin C = 1/n$. Explain with a diagram how an
   optical fibre carries light around bends. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Laws and definitions as in §15.1; ${}_1n_2 = n_2/n_1$.

**2.** See §15.2 (b) and (c). Reversing the ray interchanges $i$ and $r$, so
${}_2n_1 = \sin r/\sin i = 1/{}_1n_2$. Writing each relative index as a ratio of
absolute indices, ${}_1n_2\,{}_2n_3\,{}_3n_1 = \dfrac{n_2}{n_1}\cdot\dfrac{n_3}{n_2}\cdot\dfrac{n_1}{n_3} = 1$.

**3.** See the derivation in §15.2.

**4.** $\sin r = \sin 45^{\circ}/1.5 = 0.7071/1.5 = 0.4714$, so
$r = 28.13^{\circ}$. Then $i - r = 16.87^{\circ}$, $\sin(i-r) = 0.2903$,
$\cos r = 0.8819$, and

$$ d = \frac{8 \times 0.2903}{0.8819} = 2.63\ \text{cm} $$

**5.** Definition and derivation as in §15.4. In a fibre the core has a larger
refractive index than the cladding, so light that enters nearly along the axis
always meets the core–cladding wall at an angle greater than $C$ and is totally
reflected, again and again, following the fibre even round bends.
:::

**Group C — Long answer (8 marks each)**

1. (a) Show that a ray emerging from a parallel-sided glass slab is parallel to
   the incident ray, and derive an expression for the lateral shift. <span class="marks">[5]</span>
   (b) A slab of glass of refractive index $1.5$ is $10\ \text{cm}$ thick. Find
   the lateral shift when light strikes it at $30^{\circ}$. <span class="marks">[3]</span>
2. (a) Define total internal reflection and state the conditions under which it
   occurs. Derive the relation between the critical angle and the refractive
   indices of the two media. <span class="marks">[4]</span>
   (b) Calculate the critical angle for a glass–water interface, given
   $n_{glass} = 1.5$ and $n_{water} = 1.33$. <span class="marks">[2]</span>
   (c) An optical fibre has a core of refractive index $1.52$ and cladding of
   refractive index $1.48$. Find the critical angle at the core–cladding
   boundary. <span class="marks">[2]</span>

::: note Answers to Group C
**1.** (a) See §15.3. (b) $\sin r = \sin 30^{\circ}/1.5 = 0.5/1.5 = 0.3333$, so
$r = 19.47^{\circ}$. Then $i - r = 10.53^{\circ}$, $\sin(i-r) = 0.1828$ and
$\cos r = 0.9428$, giving

$$ d = \frac{10 \times 0.1828}{0.9428} = 1.94\ \text{cm} $$

**2.** (a) See §15.4; $\sin C = n_2/n_1$ from $n_1\sin C = n_2\sin 90^{\circ}$.

(b) $\sin C = n_{water}/n_{glass} = 1.33/1.5 = 0.8867$, so $C = 62.5^{\circ}$.

(c) $\sin C = 1.48/1.52 = 0.9737$, so $C = 76.8^{\circ}$. Any ray meeting the
wall at more than $76.8^{\circ}$ to the normal stays inside the core.
:::
