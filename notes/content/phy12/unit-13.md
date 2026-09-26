---
subject: Physics
grade: 12
unit: 13
title: Polarization
hours: 3
area: Waves and Optics
---

Interference and diffraction prove that light is a **wave**, but they cannot say
whether it is a longitudinal wave like sound or a transverse one. Polarization
settles that question. Only a transverse wave can be filtered so that its
vibrations survive in one direction and not another, and light can. This unit
explains what polarized light is, how it is produced, and the two formulae the
NEB asks for: Brewster's law and Malus's law.

::: key What polarization tells us
Sound cannot be polarized; light can. That single experimental fact proves that
light vibrations are **perpendicular to the direction of travel** — light is a
transverse wave. In an electromagnetic wave it is the electric field vector that
we mean by "the vibration".
:::

## 13.1 Phenomenon of polarization

In a light wave from an ordinary source — a lamp, the Sun, a burning stick — the
electric field vibrates in a direction at right angles to the direction of travel,
but that direction changes randomly millions of times a second as one atom after
another emits its short wave train. Such light is **unpolarized**.

::: definition Polarization of light
**Polarization** is the process of confining the vibrations of the electric
vector of a light wave to a single plane. Light in which the vibrations are
confined to one plane is called **plane polarized** (or linearly polarized)
light.
:::

Two planes are named, and students regularly confuse them:

| Plane | Definition |
|---|---|
| **Plane of vibration** | the plane containing the direction of vibration and the direction of propagation |
| **Plane of polarization** | the plane through the direction of propagation and **perpendicular** to the plane of vibration |

The two planes are always at $90^\circ$ to each other. No vibration takes place in
the plane of polarization.

```figure caption="End-on view, looking straight along the beam. (a) Unpolarized light: the electric vector takes every direction in the plane of the page, at random. (b) Plane polarized light: the vibration is confined to one direction."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle
fig, axes = plt.subplots(1, 2, figsize=(4.6, 2.4))
for ax, mode, ttl in [(axes[0], 'un', '(a) unpolarized'),
                      (axes[1], 'pol', '(b) plane polarized')]:
    ax.add_patch(Circle((0, 0), 1.30, fill=False, color=MUTED, lw=0.9, ls=(0, (3, 2))))
    if mode == 'un':
        for ang in np.arange(0, 180, 15):
            a = np.radians(ang); v = np.array([np.cos(a), np.sin(a)])
            ax.annotate('', xy=tuple(v), xytext=tuple(-v),
                        arrowprops=dict(arrowstyle='<|-|>', color=ACCENT, lw=1.0,
                                        mutation_scale=6))
    else:
        ax.annotate('', xy=(0, 1.0), xytext=(0, -1.0),
                    arrowprops=dict(arrowstyle='<|-|>', color='#d9534f', lw=2.2,
                                    mutation_scale=9))
        ax.annotate('plane of\nvibration', (0.16, 0.55), fontsize=7.8, color='#d9534f')
    ax.plot([0], [0], 'o', color=INK, ms=4.5, zorder=5)
    ax.annotate('beam out of page', (0, -1.75), ha='center', fontsize=7.6, color=MUTED)
    ax.set_title(ttl, fontsize=9)
    ax.set_xlim(-1.75, 1.75); ax.set_ylim(-2.05, 1.6)
    ax.set_aspect('equal'); ax.axis('off')
```

In diagrams drawn side-on, vibrations **in** the plane of the page are shown as
short double-headed arrows (↕) and vibrations **perpendicular** to the page as
dots (•). Unpolarized light is drawn with both, plane polarized light with only
one of the two.

### Ways of producing polarized light

| Method | How it works | Example |
|---|---|---|
| Reflection | at the polarizing angle the reflected light is fully plane polarized | glare from a wet road or from Phewa Lake |
| Refraction (pile of plates) | the transmitted beam becomes progressively polarized after many glass plates | pile-of-plates polarizer |
| Selective absorption (dichroism) | one component is absorbed, the other transmitted | Polaroid sheet |
| Double refraction | a calcite crystal splits the beam into two oppositely polarized rays | Nicol prism |
| Scattering | light scattered at $90^\circ$ from air molecules is plane polarized | the blue sky at right angles to the Sun |

**Double refraction.** When unpolarized light enters a calcite (Iceland spar) or
quartz crystal it splits into two refracted rays: the **ordinary ray**, which
obeys Snell's law, and the **extraordinary ray**, which does not. The two rays are
plane polarized in mutually perpendicular planes. A Nicol prism is a calcite
crystal cut and cemented with Canada balsam so that the ordinary ray is totally
internally reflected away and only the plane polarized extraordinary ray emerges.

**Partial polarization.** In most of these processes the emerging light is a
mixture. The **degree of polarization** is

$$ P = \frac{I_{\max} - I_{\min}}{I_{\max} + I_{\min}} $$

where $I_{\max}$ and $I_{\min}$ are the largest and smallest intensities observed
as an analyser is rotated through a full turn. $P = 1$ for fully plane polarized
light and $P = 0$ for unpolarized light.

## 13.2 Brewster's law; transverse nature of light

When unpolarized light strikes a transparent surface, both the reflected and the
refracted beams are **partially** polarized. In 1811 David Brewster found that at
one particular angle of incidence the reflected beam is **completely** plane
polarized, with its vibrations perpendicular to the plane of incidence. That angle
is the **polarizing angle** or **Brewster angle**, $\theta_p$.

```figure caption="Polarization by reflection. At the polarizing angle $\theta_p$ the reflected beam is completely plane polarized (dots = vibrations perpendicular to the page) and the reflected and refracted beams are exactly $90^\circ$ apart, so $\theta_p + r = 90^\circ$ and $n = \tan\theta_p$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Arc, Rectangle
fig, ax = plt.subplots(figsize=(5.0, 3.35))
n = 1.5
tp = np.arctan(n); r = np.pi/2 - tp
O = np.array([0.0, 0.0])
Pi = np.array([-3.5*np.sin(tp),  3.5*np.cos(tp)])
Pr = np.array([ 3.5*np.sin(tp),  3.5*np.cos(tp)])
Pt = np.array([ 3.1*np.sin(r), -3.1*np.cos(r)])
ax.add_patch(Rectangle((-4.6, -3.3), 9.2, 3.3, color=ACCENT, alpha=0.07, lw=0))
ax.plot([-4.6, 4.6], [0, 0], color=INK, lw=1.6, zorder=3)
ax.plot([0, 0], [-3.1, 3.1], color=MUTED, lw=0.9, ls=':')
ax.annotate('normal', (0, 3.1), textcoords='offset points', xytext=(0, 4),
            ha='center', fontsize=8.2, color=MUTED)
def beam(p0, p1, col):
    ax.annotate('', xy=tuple(p1), xytext=tuple(p0),
                arrowprops=dict(arrowstyle='-|>', color=col, lw=1.5, mutation_scale=11))
def marks(p0, p1, pattern, col):
    v = p1 - p0; L = np.hypot(*v); e = v/L; q = np.array([-e[1], e[0]])
    for f, kind in pattern:
        P = p0 + f*v
        if kind == 'd':
            ax.plot([P[0]], [P[1]], 'o', color=col, ms=4.2, zorder=7)
        else:
            ax.plot([P[0]-0.22*q[0], P[0]+0.22*q[0]],
                    [P[1]-0.22*q[1], P[1]+0.22*q[1]], color=col, lw=2.0, zorder=7)
beam(Pi, O, ACCENT)
beam(O, Pr, '#d9534f')
beam(O, Pt, '#2e8b57')
marks(Pi, O, [(0.10, 'd'), (0.24, 'b'), (0.38, 'd'), (0.52, 'b'), (0.66, 'd')], ACCENT)
marks(O, Pr, [(0.28, 'd'), (0.44, 'd'), (0.60, 'd'), (0.76, 'd')], '#d9534f')
marks(O, Pt, [(0.24, 'b'), (0.40, 'd'), (0.56, 'b'), (0.72, 'b')], '#2e8b57')
ax.add_patch(Arc((0, 0), 3.4, 3.4, theta1=90, theta2=180-np.degrees(tp),
                 color=INK, lw=0.9))
ax.add_patch(Arc((0, 0), 3.4, 3.4, theta1=np.degrees(np.pi/2-tp), theta2=90,
                 color=INK, lw=0.9))
ax.add_patch(Arc((0, 0), 3.4, 3.4, theta1=270, theta2=270+np.degrees(r),
                 color=INK, lw=0.9))
ax.add_patch(Arc((0, 0), 4.4, 4.4, theta1=-np.degrees(tp),
                 theta2=np.degrees(np.pi/2-tp), color='#8a5cd6', lw=1.1))
ax.annotate(r'$\theta_p$', (-0.95, 1.55), fontsize=10)
ax.annotate(r'$\theta_p$', (0.62, 1.62), fontsize=10)
ax.annotate('$r$', (0.42, -1.98), fontsize=10)
ax.annotate(r'$90^\circ$', (2.42, 0.16), fontsize=9.5, color='#8a5cd6')
ax.annotate('unpolarized', tuple(Pi), textcoords='offset points', xytext=(6, 8),
            fontsize=8.4, color=ACCENT, ha='left')
ax.annotate('completely\nplane polarized', tuple(Pr), textcoords='offset points',
            xytext=(-6, 6), fontsize=8.4, color='#d9534f', ha='right')
ax.annotate('partially polarized', tuple(Pt), textcoords='offset points',
            xytext=(8, -4), fontsize=8.4, color='#2e8b57', ha='left')
ax.annotate('air', (-4.4, 0.25), fontsize=8.6, color=MUTED)
ax.annotate('medium, index $n$', (-4.4, -0.55), fontsize=8.6, color=MUTED)
ax.set_xlim(-5.0, 5.4); ax.set_ylim(-3.9, 3.9)
ax.set_aspect('equal'); ax.axis('off')
```

::: derivation Brewster's law
At the polarizing angle the reflected and refracted rays are found
experimentally to be at right angles to each other. From the figure the three
angles at O must add to a straight angle:

$$ \theta_p + 90^\circ + r = 180^\circ \;\Longrightarrow\; r = 90^\circ - \theta_p $$

Apply Snell's law for light going from air into the medium:

$$ n = \frac{\sin\theta_p}{\sin r} = \frac{\sin\theta_p}{\sin(90^\circ - \theta_p)}
 = \frac{\sin\theta_p}{\cos\theta_p} $$

$$ n = \tan\theta_p $$

This is **Brewster's law**: *the tangent of the polarizing angle of a medium is
equal to its refractive index.*
:::

The physical reason is neat. The refracted wave sets the electrons of the medium
vibrating along its own electric vector, at right angles to the refracted ray. A
vibrating charge radiates nothing **along** its own line of vibration. At the
Brewster angle the reflected direction is exactly along that line for the
component in the plane of incidence, so that component simply cannot be reflected.
Only the component perpendicular to the plane of incidence survives — and the
reflected light is fully plane polarized.

Because $n$ varies slightly with wavelength (dispersion), $\theta_p$ is not quite
the same for every colour: for crown glass it is about $56.3^\circ$ for yellow
light and a fraction of a degree larger for violet.

::: caution Brewster's angle is not the critical angle
$\theta_p = \tan^{-1}n$ applies when light goes from a **rarer** medium into a
denser one, and the reflected beam is the polarized one. The critical angle
$C = \sin^{-1}(1/n)$ applies going the other way, from denser to rarer. For
$n = 1.5$, $\theta_p = 56.3^\circ$ but $C = 41.8^\circ$ — different angles, different
phenomena.
:::

### Transverse nature of light

Take two Polaroid sheets, P and A. Send light through P; the beam that emerges
looks slightly dimmer but otherwise normal. Now rotate A about the beam as axis.
The transmitted intensity rises and falls, and twice in every complete turn it
drops to **zero**.

If light were a longitudinal wave, its vibrations would be along the direction of
travel, and a rotation of A about that same axis could make no difference
whatsoever — the wave has no "sideways" direction to be picky about. The fact that
rotating A extinguishes the beam shows the vibrations must lie **across** the beam.
Polarization is therefore the only optical phenomenon that establishes the
**transverse** nature of light waves.

::: example Worked example 13.1
**Problem.** Find the polarizing angle for a glass of refractive index $1.5$, and
the corresponding angle of refraction. Verify that the reflected and refracted
rays are perpendicular.

**Solution.** By Brewster's law,

$$ \tan\theta_p = n = 1.5 \;\Longrightarrow\; \theta_p = \tan^{-1}(1.5) = 56.3^\circ $$

$$ r = 90^\circ - \theta_p = 90^\circ - 56.3^\circ = 33.7^\circ $$

Check with Snell's law: $\dfrac{\sin 56.3^\circ}{\sin 33.7^\circ}
= \dfrac{0.832}{0.555} = 1.50$ — correct. The angle between the reflected ray and
the refracted ray is $180^\circ - 56.3^\circ - 33.7^\circ = 90^\circ$.
:::

## 13.3 Polaroid

A **Polaroid** is a thin commercial sheet that transmits light vibrating in one
direction only. Edwin Land made the first one in 1928 by embedding tiny aligned
needle-shaped crystals of **herapathite** (quinine iodosulphate) in nitrocellulose
— the J-type sheet. Modern **H-Polaroid** is made from a sheet of polyvinyl
alcohol that is stretched so that its long molecules all lie parallel, then soaked
in iodine. The iodine-doped chains conduct along their length, so they absorb the
component of the electric field parallel to the chains and transmit the
perpendicular component. The direction that is passed is called the **transmission
axis** or pass axis.

When two Polaroids are used, the first is the **polarizer** and the second the
**analyser**.

```figure caption="(a) Unpolarized light of intensity $I_0$ passes a polarizer (axis vertical) and emerges plane polarized with intensity $I_0/2$; the analyser, whose axis makes an angle $\theta$ with it, transmits $(I_0/2)\cos^2\theta$. (b) Malus's law: transmitted intensity against the angle between the two axes."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Arc
fig, axes = plt.subplots(1, 2, figsize=(5.2, 2.7),
                         gridspec_kw={'width_ratios': [1.18, 1.0]})

ax = axes[0]
th = np.radians(35.0)
for cx, ang, lab in [(0.0, np.pi/2, 'polarizer'),
                     (3.0, np.pi/2 - th, 'analyser')]:
    rect = Rectangle((cx-0.85, -0.85), 1.70, 1.70, facecolor='#eef2f7',
                     edgecolor=INK, lw=1.0, zorder=2)
    ax.add_patch(rect)
    e = np.array([np.cos(ang), np.sin(ang)]); q = np.array([-e[1], e[0]])
    for t in np.arange(-1.15, 1.16, 0.19):
        p0 = t*q - 1.25*e; p1 = t*q + 1.25*e
        ln, = ax.plot([cx+p0[0], cx+p1[0]], [p0[1], p1[1]],
                      color=MUTED, lw=0.8, zorder=3)
        ln.set_clip_path(rect)
    ln, = ax.plot([cx-1.25*e[0], cx+1.25*e[0]], [-1.25*e[1], 1.25*e[1]],
                  color='#d9534f', lw=2.2, zorder=4)
    ln.set_clip_path(rect)
    ax.annotate(lab, (cx, -1.00), ha='center', va='top', fontsize=8.4, color=INK)
eA = np.array([np.cos(np.pi/2 - th), np.sin(np.pi/2 - th)])
ax.plot([3.0, 3.0], [0.0, 1.55], color=INK, lw=0.9, ls=(0, (2, 2)), zorder=5)
ax.plot([3.0, 3.0+1.55*eA[0]], [0.0, 1.55*eA[1]], color='#d9534f', lw=1.1,
        ls=(0, (2, 2)), zorder=5)
ax.add_patch(Arc((3.0, 0.0), 2.5, 2.5, theta1=np.degrees(np.pi/2-th), theta2=90,
                 color=INK, lw=1.0, zorder=6))
ax.annotate(r'$\theta$', (3.40, 1.32), fontsize=10, color=INK)
for x0, x1 in [(-2.2, -0.95), (0.95, 2.95), (3.95, 5.4)]:
    ax.annotate('', xy=(x1, 0), xytext=(x0, 0),
                arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.5, mutation_scale=11))
ax.annotate('$I_0$\nunpolarized', (-1.6, -1.92), ha='center', va='top',
            fontsize=8.2, color=INK)
ax.annotate('$I_0/2$\npolarized', (1.60, -1.92), ha='center', va='top',
            fontsize=8.2, color=INK)
ax.annotate(r'$\frac{I_0}{2}\cos^2\theta$', (4.80, -1.80), ha='center', va='top',
            fontsize=9.0, color=INK)
ax.annotate('(a) polarizer and analyser', (1.6, 2.30), ha='center',
            fontsize=9, color=INK, weight='600')
ax.set_xlim(-2.9, 6.1); ax.set_ylim(-3.1, 2.6)
ax.set_aspect('equal'); ax.axis('off')

ax = axes[1]
a = np.linspace(0, 360, 900)
ax.plot(a, np.cos(np.radians(a))**2, color=ACCENT, lw=1.9)
ax.fill_between(a, 0, np.cos(np.radians(a))**2, color=ACCENT, alpha=0.10)
for xv in (90, 270):
    ax.plot([xv], [0], 'o', color='#d9534f', ms=4.5, zorder=5)
ax.annotate('crossed\nPolaroids', xy=(90, 0.02), xytext=(150, 0.34),
            fontsize=7.8, color='#d9534f', ha='center',
            arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=0.9,
                            mutation_scale=7))
ax.set_xlabel(r'angle $\theta$ between axes')
ax.set_ylabel('$I/I_{max}$')
ax.set_xticks([0, 90, 180, 270, 360])
ax.set_xticklabels(['$0$', '$90$', '$180$', '$270$', '$360$'])
ax.set_yticks([0, 0.5, 1.0])
ax.set_xlim(0, 360); ax.set_ylim(0, 1.18)
ax.set_title("(b) Malus's law", fontsize=9)
ax.spines[['top', 'right']].set_visible(False)
ax.grid(True, alpha=0.5)
```
::: derivation Malus's law
Let plane polarized light of amplitude $A$ fall on an analyser whose transmission
axis makes an angle $\theta$ with the plane of vibration of the incoming light.
Resolve $A$ into two components:

- $A\cos\theta$ **along** the transmission axis — this is transmitted;
- $A\sin\theta$ **perpendicular** to it — this is absorbed.

Intensity is proportional to the square of the amplitude, so if $I_0$ is the
intensity of the light reaching the analyser,

$$ I = k(A\cos\theta)^{2} = kA^{2}\cos^{2}\theta $$

$$ I = I_0\cos^{2}\theta $$

This is **Malus's law**. It gives $I = I_0$ for parallel axes
($\theta = 0^\circ$) and $I = 0$ for **crossed** axes ($\theta = 90^\circ$).
:::

::: caution The first polaroid always halves the intensity
Malus's law applies to light that is **already** plane polarized. When
*unpolarized* light of intensity $I_0$ falls on the first Polaroid, $\theta$ takes
every value at random and the average of $\cos^2\theta$ is $\frac{1}{2}$, so the
emergent intensity is $I_0/2$ **whatever the orientation of the sheet**. Only then
does $\cos^2\theta$ apply, at the second sheet.
:::

### Uses of Polaroids

- **Sunglasses.** Glare reflected from water or a wet road is largely horizontally
  polarized, so the lenses are cut with a vertical transmission axis and the glare
  is removed.
- **Photography.** A rotatable polarizing filter darkens a blue sky and kills
  reflections from glass and water.
- **LCD screens** in calculators, watches, laptops and mobile phones work by
  rotating polarized light between two crossed Polaroids.
- **3-D cinema**, where the two eyes receive images polarized at right angles.
- **Photoelastic stress analysis**: a plastic model of a bridge or a machine part
  placed between crossed Polaroids shows coloured fringes wherever it is strained.
- **Controlling light intensity** smoothly in optical instruments and in
  laboratory work, using two Polaroids in series.

::: example Worked example 13.2
**Problem.** Unpolarized light of intensity $I_0$ falls on a polarizer. An
analyser is placed behind it with its axis at $60^\circ$ to that of the polarizer.
Find the intensity of the emergent light.

**Solution.** After the polarizer the light is plane polarized with intensity

$$ I_1 = \frac{I_0}{2} $$

By Malus's law, the analyser transmits

$$ I_2 = I_1\cos^{2}60^\circ = \frac{I_0}{2}\left(\frac{1}{2}\right)^{2}
 = \frac{I_0}{8} = 0.125\,I_0 $$
:::

::: example Worked example 13.3
**Problem.** Three Polaroids are placed one behind the other. The first and the
third are crossed. The middle one makes an angle of $30^\circ$ with the first.
Unpolarized light of intensity $I_0$ enters. Find the intensity emerging from the
third sheet.

**Solution.** After sheet 1: $I_1 = I_0/2$.

Sheet 2 is at $30^\circ$ to sheet 1:

$$ I_2 = \frac{I_0}{2}\cos^{2}30^\circ = \frac{I_0}{2}(0.866)^{2} = 0.375\,I_0 $$

Sheet 3 is at $90^\circ$ to sheet 1, hence at $90^\circ - 30^\circ = 60^\circ$ to
sheet 2:

$$ I_3 = 0.375\,I_0 \times \cos^{2}60^\circ = 0.375\,I_0 \times 0.25
 = 0.09375\,I_0 = \frac{3I_0}{32} $$

Note that with the middle sheet removed nothing at all would get through — adding
a third Polaroid *increases* the transmitted light.
:::

::: example Worked example 13.4
**Problem.** The polarizing angle of a certain transparent medium is $60^\circ$.
Find (a) its refractive index, (b) the speed of light in it, and (c) its critical
angle. Take $c = 3\times10^{8}\ \text{m s}^{-1}$.

**Solution.**

(a) $n = \tan 60^\circ = \sqrt{3} = 1.732$.

(b) $v = \dfrac{c}{n} = \dfrac{3\times10^{8}}{1.732} = 1.73\times10^{8}\ \text{m s}^{-1}$.

(c) $\sin C = \dfrac{1}{n} = \dfrac{1}{1.732} = 0.5774$, so $C = 35.3^\circ$.
:::

## Chapter summary

- **Unpolarized** light vibrates in all directions perpendicular to the ray;
  **plane polarized** light vibrates in one plane only. The plane of polarization
  is perpendicular to the plane of vibration.
- Polarized light is produced by reflection, refraction through a pile of plates,
  selective absorption (Polaroid), double refraction (Nicol prism) and scattering.
- Degree of polarization
  $P = (I_{\max}-I_{\min})/(I_{\max}+I_{\min})$.
- **Brewster's law**: $n = \tan\theta_p$, with $\theta_p + r = 90^\circ$; the
  reflected and refracted rays are then perpendicular and the reflected beam is
  fully plane polarized.
- Brewster's angle ($\tan^{-1}n$, rarer to denser) is **not** the critical angle
  ($\sin^{-1}(1/n)$, denser to rarer).
- **Malus's law**: $I = I_0\cos^2\theta$. Unpolarized light through the first
  Polaroid always gives $I_0/2$; crossed Polaroids give zero.
- Polarization occurs for transverse waves only, so it proves that light is a
  transverse wave. Sound, being longitudinal, cannot be polarized.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Polarization of light establishes that light waves are <span class="marks">[1]</span>
   (a) longitudinal (b) transverse (c) stationary (d) mechanical
2. Brewster's law is stated as <span class="marks">[1]</span>
   (a) $n = \sin\theta_p$ (b) $n = \tan\theta_p$ (c) $n = \cot\theta_p$ (d) $n = \cos\theta_p$
3. At the polarizing angle, the angle between the reflected and the refracted ray is <span class="marks">[1]</span>
   (a) $0^\circ$ (b) $45^\circ$ (c) $90^\circ$ (d) $180^\circ$
4. Unpolarized light of intensity $I_0$ passes through a single Polaroid. The
   emergent intensity is <span class="marks">[1]</span>
   (a) $I_0$ (b) $I_0/2$ (c) $I_0/4$ (d) zero
5. Two Polaroids are crossed. The intensity of the light coming out is <span class="marks">[1]</span>
   (a) $I_0$ (b) $I_0/2$ (c) $I_0/4$ (d) zero

::: note Answers to Group A
**1.** (b) — only a transverse wave has a vibration direction across the ray that can be selected.
**2.** (b) — $n = \tan\theta_p$.
**3.** (c) — that perpendicularity is what makes $\theta_p + r = 90^\circ$.
**4.** (b) — averaging $\cos^2\theta$ over all directions gives $\frac{1}{2}$.
**5.** (d) — $\theta = 90^\circ$ gives $I = I_0\cos^2 90^\circ = 0$.
:::

**Group B — Short answer (5 marks each)**

1. What is plane polarized light? How does it differ from unpolarized light?
   Explain how plane polarized light can be produced by reflection. <span class="marks">[5]</span>
2. State and prove Brewster's law, and show that at the polarizing angle the
   reflected and refracted rays are perpendicular to each other. <span class="marks">[5]</span>
3. State Malus's law and derive it. Unpolarized light of intensity $I_0$ passes
   through two Polaroids whose axes are at $30^\circ$. Find the emergent intensity. <span class="marks">[5]</span>
4. What is a Polaroid? Describe how it is made and state four of its uses. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Outline: plane polarized = vibrations in one plane only; unpolarized =
vibrations in all directions perpendicular to the ray. At the polarizing angle
$\theta_p = \tan^{-1}n$ the reflected beam contains only the component
perpendicular to the plane of incidence, so it is fully plane polarized.

**3.** Derivation as in §13.3. Numerically, after the first Polaroid
$I_1 = I_0/2$; after the second,

$$ I_2 = \frac{I_0}{2}\cos^{2}30^\circ = \frac{I_0}{2}(0.75) = 0.375\,I_0 = \frac{3I_0}{8} $$

**4.** Outline: a sheet of stretched iodine-treated polyvinyl alcohol whose long
aligned molecules absorb the electric vector parallel to them and transmit the
perpendicular component. Uses: sunglasses, camera filters, LCD displays, 3-D
glasses, photoelastic stress analysis, intensity control.
:::

**Group C — Long answer (8 marks each)**

1. (a) Explain the phenomenon of polarization by reflection and derive Brewster's
   law. <span class="marks">[4]</span>
   (b) Explain how polarization proves the transverse nature of light. <span class="marks">[2]</span>
   (c) The polarizing angle of a medium is $58^\circ$. Calculate its refractive
   index and the speed of light in it. <span class="marks">[2]</span>
2. (a) State and derive Malus's law. <span class="marks">[4]</span>
   (b) Unpolarized light of intensity $I_0$ is passed through three Polaroids. The
   first and the third are crossed and the second makes an angle $\theta$ with the
   first. Show that the emergent intensity is $\frac{I_0}{8}\sin^{2}2\theta$, and
   find the value of $\theta$ for which it is maximum. <span class="marks">[4]</span>

::: note Answers to Group C
**1. (c)** $n = \tan 58^\circ = 1.60$, and
$v = c/n = 3\times10^{8}/1.60 = 1.87\times10^{8}\ \text{m s}^{-1}$.

**2. (b)** After the first Polaroid, $I_1 = I_0/2$. After the second,
$I_2 = \frac{I_0}{2}\cos^{2}\theta$. The third is at $(90^\circ - \theta)$ to the
second, so

$$ I_3 = \frac{I_0}{2}\cos^{2}\theta\,\cos^{2}(90^\circ-\theta)
 = \frac{I_0}{2}\cos^{2}\theta\,\sin^{2}\theta $$

Using $2\sin\theta\cos\theta = \sin 2\theta$,

$$ I_3 = \frac{I_0}{2}\cdot\frac{\sin^{2}2\theta}{4}
 = \frac{I_0}{8}\sin^{2}2\theta $$

This is maximum when $\sin 2\theta = 1$, i.e. $\theta = 45^\circ$, giving
$I_3 = I_0/8$.
:::
