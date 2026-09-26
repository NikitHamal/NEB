---
subject: Physics
grade: 12
unit: 11
title: Interference
hours: 2
area: Waves and Optics
---

Two torches pointed at the same wall never produce dark bands. Yet light from a
single lamp, split into two and recombined, produces a ladder of bright and dark
stripes. That is **interference**, and it was Thomas Young's demonstration of it
in 1801 that finally proved light is a wave. This short unit sets out the
conditions under which interference can be seen, and works through the one
experiment the NEB asks about every year — Young's double slit.

::: key The two things this unit is worth
A derivation of the fringe width $\beta = \lambda D/d$ from the path difference,
and numericals built on it. Get the path difference $\Delta = yd/D$ right and
every question in the unit follows from it.
:::

## 11.1 Phenomenon of Interference: Coherent sources

When two waves arrive at the same point, the **principle of superposition** says
the resultant displacement is the vector sum of the individual displacements. For
two waves of the same frequency and amplitudes $a_1$, $a_2$ arriving with a phase
difference $\phi$, the resultant amplitude is

$$ A = \sqrt{a_1^{2} + a_2^{2} + 2a_1a_2\cos\phi} $$

Since intensity is proportional to the square of the amplitude, $I \propto A^2$,

$$ I = I_1 + I_2 + 2\sqrt{I_1I_2}\,\cos\phi $$

The last term is the **interference term**. It is positive where the waves arrive
in step and negative where they arrive out of step.

::: definition Interference of light
Interference is the modification of intensity produced by the superposition of
two or more light waves. Where the resultant intensity is a maximum the
interference is **constructive**; where it is a minimum it is **destructive**.
:::

A path difference $\Delta$ corresponds to a phase difference

$$ \phi = \frac{2\pi}{\lambda}\,\Delta $$

so the conditions can be written either way:

| | Path difference $\Delta$ | Phase difference $\phi$ | Resultant |
|---|---|---|---|
| Constructive (bright) | $n\lambda$ | $2n\pi$ | $A = a_1+a_2$, $I_{\max} = (\sqrt{I_1}+\sqrt{I_2})^2$ |
| Destructive (dark) | $(2n-1)\lambda/2$ | $(2n-1)\pi$ | $A = |a_1-a_2|$, $I_{\min} = (\sqrt{I_1}-\sqrt{I_2})^2$ |

with $n = 0, 1, 2, \dots$ For two equal sources of intensity $I_0$ each,
$I_{\max} = 4I_0$ and $I_{\min} = 0$, and the general result is

$$ I = 4I_0\cos^{2}\!\left(\frac{\phi}{2}\right) $$

```figure caption="Superposition of two waves of equal amplitude. Left: in phase, the crests add and the amplitude doubles. Right: a phase difference of $\pi$ (path difference $\lambda/2$) cancels them completely."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(5.2, 2.5), sharey=True)
x = np.linspace(0, 4*np.pi, 700)
for ax, ph, ttl in [(axes[0], 0.0, 'in phase: bright'),
                    (axes[1], np.pi, 'out of phase: dark')]:
    y1 = np.sin(x); y2 = np.sin(x + ph)
    ax.plot(x, y1, color=ACCENT, lw=1.3, ls='-', label='wave 1')
    ax.plot(x, y2, color='#2e8b57', lw=1.3, ls=(0, (4, 2)), label='wave 2')
    ax.plot(x, y1+y2, color='#d9534f', lw=2.0, label='resultant')
    ax.axhline(0, color=MUTED, lw=0.7)
    ax.set_title(ttl, fontsize=9)
    ax.set_xticks([]); ax.set_xlim(0, 4*np.pi)
    ax.spines[['top', 'right', 'bottom']].set_visible(False)
axes[1].spines['left'].set_visible(False)
axes[0].set_ylabel('displacement')
axes[0].set_yticks([-2, 0, 2]); axes[0].set_ylim(-2.4, 2.4)
axes[1].legend(loc='lower center', ncol=3, fontsize=7.6,
               bbox_to_anchor=(-0.05, -0.30), columnspacing=1.0)
```

### Coherent sources

The stripes only stay put if $\phi$ at each point stays the same from one instant
to the next.

::: definition Coherent sources
Two sources are **coherent** if they emit light of the same frequency (and
ideally the same amplitude) with a **constant phase difference** that does not
change with time.
:::

An ordinary lamp emits light in bursts lasting about $10^{-8}\ \text{s}$, each
burst starting with a random phase. Two separate lamps therefore have a phase
difference that reshuffles about $10^{8}$ times a second — far faster than the eye
or any detector can follow — so $\cos\phi$ averages to zero and

$$ I = I_1 + I_2 $$

The intensities simply add and no fringes are seen. The way round this is to
**derive both beams from a single source**, so that whatever phase jump occurs
happens in both beams together and cancels out of $\phi$. Two methods are used:

- **Division of wavefront** — two parts of the same wavefront are used: Young's
  double slit, Fresnel's biprism, Lloyd's mirror.
- **Division of amplitude** — one beam is partly reflected and partly transmitted:
  thin films, soap bubbles, the colours on a layer of oil on a Kathmandu street
  after rain, Newton's rings.

Lasers are naturally coherent over long distances, which is why a laser pointer
makes the double-slit experiment easy to show in a school laboratory.

::: caution Interference does not destroy energy
At a dark fringe the intensity is zero, but energy is not lost — it has been
**redistributed** to the bright fringes, where the intensity is $4I_0$ instead of
the $2I_0$ you would get without interference. Averaged over one fringe spacing,
the mean of $4I_0\cos^2(\phi/2)$ is exactly $2I_0$, so energy is conserved.
:::

## 11.2 Young's double slit experiment

Light from a monochromatic source falls on a narrow slit $S$. The cylindrical
wavefront spreading from $S$ reaches two more narrow slits $S_1$ and $S_2$, placed
symmetrically a small distance $d$ apart. Because $S_1$ and $S_2$ are carved out
of the **same** wavefront, they are coherent. They act as two line sources, and
the overlapping light falls on a screen a distance $D$ away.

```figure caption="Young's double slit. $S_1$ and $S_2$ are coherent sources a distance $d$ apart; the screen is at a distance $D$. For a point P at height $y$ the wave from $S_2$ travels the extra distance $S_2N = d\sin\theta \approx yd/D$. The slit separation is greatly exaggerated."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Arc
fig, ax = plt.subplots(figsize=(5.2, 3.2))
d = 1.8
S1 = np.array([0.0,  d/2]); S2 = np.array([0.0, -d/2])
Dx = 6.5
O = np.array([Dx, 0.0]); P = np.array([Dx, 2.6])
for y0, y1 in [(-2.9, -d/2-0.14), (-d/2+0.14, d/2-0.14), (d/2+0.14, 2.9)]:
    ax.add_patch(Rectangle((-0.09, y0), 0.18, y1-y0, color=INK, lw=0))
Sx = -1.7
ax.add_patch(Rectangle((Sx-0.07, -2.9), 0.14, 2.76, color=INK, lw=0))
ax.add_patch(Rectangle((Sx-0.07, 0.14), 0.14, 2.76, color=INK, lw=0))
for R in (0.40, 0.68, 0.96):
    a = np.radians(np.linspace(-58, 58, 120))
    ax.plot(Sx+R*np.cos(a), R*np.sin(a), color=GRID, lw=1.0)
ax.annotate('S', (Sx, 0), textcoords='offset points', xytext=(-12, -4), fontsize=9.5)
ax.plot([Dx, Dx], [-2.9, 3.1], color=INK, lw=2.2)
ax.annotate('screen', (Dx, 3.1), textcoords='offset points', xytext=(0, 4),
            ha='center', fontsize=8.6, color=MUTED)
u = (P - S2)/np.hypot(*(P - S2))
N = S2 + np.dot(S1 - S2, u)*u
ax.plot([S1[0], P[0]], [S1[1], P[1]], color=ACCENT, lw=1.3)
ax.plot([S2[0], P[0]], [S2[1], P[1]], color='#2e8b57', lw=1.3)
ax.plot([S1[0], N[0]], [S1[1], N[1]], color=MUTED, lw=1.0, ls=(0, (3, 2)))
ax.plot([S2[0], N[0]], [S2[1], N[1]], color='#d9534f', lw=3.2, zorder=6)
e1 = (S1-N)/np.hypot(*(S1-N)); e2 = (S2-N)/np.hypot(*(S2-N))
sq = np.array([N+0.20*e1, N+0.20*e1+0.20*e2, N+0.20*e2])
ax.plot(sq[:, 0], sq[:, 1], color=INK, lw=0.8)
for q, lab, off in [(S1, '$S_1$', (-24, -5)), (S2, '$S_2$', (-24, -5)),
                    (N, 'N', (5, 4))]:
    ax.plot([q[0]], [q[1]], 'o', color=INK, ms=4.0, zorder=7)
    ax.annotate(lab, tuple(q), textcoords='offset points', xytext=off, fontsize=9.5)
ax.annotate(r'path difference  $S_2N = d\sin\theta$', xy=tuple(0.5*(S2+N)),
            xytext=(3.3, -2.7), ha='center', color='#d9534f', fontsize=9,
            arrowprops=dict(arrowstyle='-', color='#d9534f', lw=0.8))
ax.plot([0, Dx], [0, 0], color=MUTED, lw=0.8, ls=':')
th = np.degrees(np.arctan2(P[1], Dx))
ax.add_patch(Arc((0, 0), 5.2, 5.2, theta1=0, theta2=th, color=INK, lw=0.9))
ax.annotate(r'$\theta$', (2.72, 0.30), fontsize=10)
ax.annotate('', xy=tuple(S1+[-0.40, 0]), xytext=tuple(S2+[-0.40, 0]),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=0.9, mutation_scale=7))
ax.annotate('$d$', (-0.40, 0), textcoords='offset points', xytext=(-10, -4), fontsize=9.5)
ax.annotate('', xy=(Dx, -3.35), xytext=(0, -3.35),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=0.9, mutation_scale=7))
ax.annotate('$D$', (Dx/2, -3.35), textcoords='offset points', xytext=(0, -14),
            ha='center', fontsize=9.5)
ax.annotate('', xy=tuple(P+[0.32, 0]), xytext=tuple(O+[0.32, 0]),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=0.9, mutation_scale=7))
ax.annotate('$y$', (Dx+0.32, 1.3), textcoords='offset points', xytext=(7, -4), fontsize=9.5)
for q, lab, off in [(O, 'O', (7, -4)), (P, 'P', (7, -3))]:
    ax.plot([q[0]], [q[1]], 'o', color=INK, ms=3.4, zorder=7)
    ax.annotate(lab, tuple(q), textcoords='offset points', xytext=off, fontsize=9.5)
ax.set_xlim(-2.6, 8.0); ax.set_ylim(-4.3, 3.6)
ax.set_aspect('equal'); ax.axis('off')
```
### Path difference

Take O as the foot of the perpendicular from the midpoint of $S_1S_2$ to the
screen, and let P be a point at height $y$ above O. From the right-angled
triangles,

$$ (S_2P)^{2} = D^{2} + \left(y + \frac{d}{2}\right)^{2}, \qquad
   (S_1P)^{2} = D^{2} + \left(y - \frac{d}{2}\right)^{2} $$

Subtracting,

$$ (S_2P)^{2} - (S_1P)^{2} = 2yd
\;\Longrightarrow\; (S_2P - S_1P)(S_2P + S_1P) = 2yd $$

In practice $D$ is about a metre while $y$ and $d$ are under a millimetre, so both
distances are very nearly $D$ and $S_2P + S_1P \approx 2D$. Hence the path
difference is

$$ \Delta = S_2P - S_1P = \frac{yd}{D} \;\;(= d\sin\theta \approx d\theta) $$

### Positions of the fringes

**Bright fringes** need $\Delta = n\lambda$:

$$ \frac{y_nd}{D} = n\lambda \;\Longrightarrow\;
   y_n = \frac{n\lambda D}{d}, \qquad n = 0, 1, 2, \dots $$

**Dark fringes** need $\Delta = (2n-1)\lambda/2$:

$$ y_n = \frac{(2n-1)\lambda D}{2d}, \qquad n = 1, 2, 3, \dots $$

::: derivation Fringe width
The **fringe width** $\beta$ is the distance between two consecutive bright (or
two consecutive dark) fringes:

$$ \beta = y_{n+1} - y_n = \frac{(n+1)\lambda D}{d} - \frac{n\lambda D}{d} $$

$$ \beta = \frac{\lambda D}{d} $$

The same subtraction on the dark-fringe formula gives the same answer, so bright
and dark fringes are **equally spaced** and the pattern is a set of uniformly
spaced, equally bright straight lines parallel to the slits. Rearranged,
$\lambda = \beta d/D$ — this is how Young measured the wavelength of light.
:::

The intensity across the screen follows from $\phi = 2\pi\Delta/\lambda$:

$$ I = 4I_0\cos^{2}\!\left(\frac{\pi y d}{\lambda D}\right) $$

```figure caption="Intensity across the screen in Young's experiment, for $\lambda = 600$ nm, $d = 0.5$ mm, $D = 1.5$ m. The fringes are evenly spaced with $\beta = \lambda D/d = 1.8$ mm and every maximum has the same height $4I_0$."
import numpy as np, matplotlib.pyplot as plt
fig = plt.figure(figsize=(5.0, 3.2))
gs = fig.add_gridspec(2, 1, height_ratios=[3.1, 1.0], hspace=0.10)
ax = fig.add_subplot(gs[0]); ax2 = fig.add_subplot(gs[1])
beta = 1.8
y = np.linspace(-6.3, 6.3, 2600)
I = np.cos(np.pi*y/beta)**2
ax.plot(y, 4*I, color=ACCENT, lw=1.8)
ax.fill_between(y, 0, 4*I, color=ACCENT, alpha=0.10)
ax.axhline(2, color=MUTED, lw=0.9, ls=':')
ax.annotate('mean $2I_0$', (-6.1, 2.10), fontsize=8.0, color=MUTED,
            bbox=dict(facecolor='white', edgecolor='none', pad=1.0))
ax.annotate('', xy=(0, 5.05), xytext=(beta, 5.05),
            arrowprops=dict(arrowstyle='<|-|>', color='#d9534f', lw=1.0, mutation_scale=7))
ax.annotate(r'$\beta$', (beta/2, 5.15), ha='center', color='#d9534f', fontsize=10)
for n in range(-3, 4):
    ax.annotate(f'$n={n}$', (n*beta, 4.20), ha='center', fontsize=7.8, color=INK)
ax.set_ylabel('intensity $I$')
ax.set_yticks([0, 2, 4]); ax.set_yticklabels(['$0$', '$2I_0$', '$4I_0$'])
ax.set_xlim(-6.3, 6.3); ax.set_ylim(0, 5.7); ax.set_xticks([])
ax.spines[['top', 'right']].set_visible(False)
ax2.imshow(np.tile(I, (2, 1)), extent=[-6.3, 6.3, 0, 1], aspect='auto',
           cmap='gray', vmin=0, vmax=1)
ax2.set_yticks([])
ax2.set_xlabel('distance from centre of screen,  $y$ (mm)')
ax2.set_xticks(np.arange(-5.4, 5.5, 1.8))
ax2.set_xlim(-6.3, 6.3)
```
### What changes the fringes

| Change | Effect on $\beta = \lambda D/d$ |
|---|---|
| Longer wavelength (red instead of blue) | $\beta$ increases |
| Slits moved further apart ($d$ up) | $\beta$ decreases |
| Screen moved back ($D$ up) | $\beta$ increases |
| Whole apparatus in water, index $n$ | $\lambda \to \lambda/n$, so $\beta \to \beta/n$ |
| One slit covered | fringes vanish, uniform illumination |
| White light used | central fringe white, coloured fringes on either side, violet nearest the centre |

::: tip Why the central fringe is white
At O the path difference is zero **for every wavelength**, so all colours are
bright there and the central fringe is white. Away from O, $\beta \propto \lambda$,
so violet fringes crowd nearer the centre and red spread out further, giving a few
coloured fringes before they overlap into white.
:::

::: example Worked example 11.1
**Problem.** In a Young's double slit experiment the slits are $0.50\ \text{mm}$
apart and the screen is $1.5\ \text{m}$ away. Light of wavelength $600\ \text{nm}$
is used. Find (a) the fringe width, (b) the distance of the 3rd bright fringe from
the centre, (c) the distance of the 3rd dark fringe from the centre.

**Solution.**

(a) $\beta = \dfrac{\lambda D}{d} = \dfrac{600\times10^{-9} \times 1.5}{0.50\times10^{-3}}
= 1.8\times10^{-3}\ \text{m} = 1.8\ \text{mm}$.

(b) $y_3 = 3\beta = 3 \times 1.8 = 5.4\ \text{mm}$.

(c) The 3rd dark fringe has $\Delta = (2\times3-1)\lambda/2 = 2.5\lambda$, so
$y = 2.5\beta = 4.5\ \text{mm}$.
:::

::: example Worked example 11.2
**Problem.** In an interference experiment the distance between the 2nd and the
7th bright fringes on the same side of the centre is $9.0\ \text{mm}$. The slit
separation is $0.50\ \text{mm}$ and the screen is $1.5\ \text{m}$ away. Find the
wavelength of the light used.

**Solution.** Between the 2nd and 7th bright fringes there are $7-2 = 5$ fringe
widths, so

$$ 5\beta = 9.0\ \text{mm} \;\Longrightarrow\; \beta = 1.8\ \text{mm} $$

$$ \lambda = \frac{\beta d}{D}
= \frac{1.8\times10^{-3} \times 0.50\times10^{-3}}{1.5}
= 6.0\times10^{-7}\ \text{m} = 600\ \text{nm} $$

This is orange-red light.
:::

::: example Worked example 11.3
**Problem.** The apparatus of Example 11.1 is now completely immersed in water of
refractive index $4/3$. Find the new fringe width. What would the fringe width
become if, in air, $D$ were doubled and $d$ halved?

**Solution.** Inside water the wavelength becomes $\lambda_w = \lambda/n$, so

$$ \beta_w = \frac{\lambda_w D}{d} = \frac{\beta}{n}
= \frac{1.8}{4/3} = 1.8 \times \frac{3}{4} = 1.35\ \text{mm} $$

With $D \to 2D$ and $d \to d/2$ in air, $\beta \to 4\beta = 7.2\ \text{mm}$.
:::

::: example Worked example 11.4
**Problem.** Two coherent sources have intensities in the ratio $4:1$. Find
(a) the ratio of their amplitudes, (b) the ratio $I_{\max}:I_{\min}$.
(c) For two **equal** sources, what fraction of $I_{\max}$ is the intensity at a
point where the path difference is $\lambda/3$?

**Solution.**

(a) $I \propto a^{2}$, so $a_1/a_2 = \sqrt{4/1} = 2$.

(b) $\dfrac{I_{\max}}{I_{\min}} = \dfrac{(a_1+a_2)^{2}}{(a_1-a_2)^{2}}
= \dfrac{(2+1)^{2}}{(2-1)^{2}} = \dfrac{9}{1}$.

(c) $\phi = \dfrac{2\pi}{\lambda}\cdot\dfrac{\lambda}{3} = \dfrac{2\pi}{3}$, so

$$ I = 4I_0\cos^{2}\!\left(\frac{\pi}{3}\right)
= 4I_0 (0.5)^{2} = I_0 = \frac{I_{\max}}{4} $$
:::

## Chapter summary

- Superposition gives $I = I_1 + I_2 + 2\sqrt{I_1I_2}\cos\phi$, with
  $\phi = 2\pi\Delta/\lambda$.
- Bright when $\Delta = n\lambda$; dark when $\Delta = (2n-1)\lambda/2$. For equal
  sources $I = 4I_0\cos^2(\phi/2)$, with $I_{\max} = 4I_0$, $I_{\min} = 0$.
- $I_{\max}:I_{\min} = (\sqrt{I_1}+\sqrt{I_2})^2 : (\sqrt{I_1}-\sqrt{I_2})^2$.
- **Coherent sources** have the same frequency and a constant phase difference;
  they must be obtained from one source, by division of wavefront or of amplitude.
- In Young's experiment $\Delta = yd/D$, bright fringes at $y_n = n\lambda D/d$,
  dark at $y_n = (2n-1)\lambda D/2d$.
- Fringe width $\beta = \lambda D/d$; all fringes are equally spaced and equally
  bright. In a medium of index $n$, $\beta$ shrinks to $\beta/n$.
- Energy is redistributed, not destroyed: the average intensity across the pattern
  is $2I_0$, exactly what the two beams carry.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Two sources are coherent if they have the same frequency and <span class="marks">[1]</span>
   (a) a constant phase difference (b) zero phase difference
   (c) the same amplitude only (d) the same intensity only
2. In Young's double slit experiment the fringe width is <span class="marks">[1]</span>
   (a) $\lambda d/D$ (b) $\lambda D/d$ (c) $Dd/\lambda$ (d) $\lambda/Dd$
3. At a point where the path difference is $\lambda/2$, the intensity due to two
   equal coherent sources of intensity $I_0$ each is <span class="marks">[1]</span>
   (a) $4I_0$ (b) $2I_0$ (c) $I_0$ (d) zero
4. If the whole double-slit apparatus is immersed in water, the fringe width <span class="marks">[1]</span>
   (a) increases (b) decreases (c) is unchanged (d) becomes zero
5. In white-light interference, the central fringe is <span class="marks">[1]</span>
   (a) violet (b) red (c) white (d) dark

::: note Answers to Group A
**1.** (a) — the phase difference must be constant in time; it need not be zero.
**2.** (b) — $\beta = \lambda D/d$.
**3.** (d) — $\Delta = \lambda/2$ gives $\phi = \pi$ and $I = 4I_0\cos^2(\pi/2) = 0$.
**4.** (b) — the wavelength shrinks to $\lambda/n$, so $\beta$ shrinks to $\beta/n$.
**5.** (c) — zero path difference at the centre for every wavelength, so all colours are bright.
:::

**Group B — Short answer (5 marks each)**

1. What are coherent sources? Explain why two independent bulbs of the same
   colour cannot produce a steady interference pattern. <span class="marks">[5]</span>
2. Derive an expression for the fringe width in Young's double slit experiment. <span class="marks">[5]</span>
3. In a double slit experiment $d = 0.28\ \text{mm}$, $D = 1.4\ \text{m}$ and
   $\lambda = 600\ \text{nm}$. Find the fringe width and the distance of the 4th
   dark fringe from the central bright fringe. <span class="marks">[5]</span>
4. Show that interference of light does not violate the principle of conservation
   of energy. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Outline: coherent = same frequency, constant phase difference. An ordinary
source emits wave trains of about $10^{-8}\ \text{s}$ with random phase, so the
phase difference between two independent lamps changes about $10^{8}$ times per
second; $\cos\phi$ averages to zero, giving $I = I_1+I_2$ and no fringes.

**3.** $\beta = \dfrac{\lambda D}{d} = \dfrac{600\times10^{-9}\times1.4}{0.28\times10^{-3}}
= 3.0\times10^{-3}\ \text{m} = 3.0\ \text{mm}$.
The 4th dark fringe is at $y = \dfrac{(2\times4-1)\lambda D}{2d} = 3.5\beta
= 10.5\ \text{mm}$.

**4.** Outline: $I = 4I_0\cos^2(\phi/2)$; the average of $\cos^2$ over a fringe is
$\frac{1}{2}$, so the mean intensity is $2I_0$ — exactly the sum of the two beams.
The energy missing from the dark fringes reappears in the bright ones.
:::

**Group C — Long answer (8 marks each)**

1. (a) Describe Young's double slit experiment with a labelled diagram. <span class="marks">[3]</span>
   (b) Derive expressions for the positions of the bright and dark fringes and
   hence for the fringe width. State two ways in which the fringe width can be
   increased. <span class="marks">[5]</span>
2. In a Young's double slit experiment, light of wavelength $589\ \text{nm}$ falls
   on two slits $1.0\ \text{mm}$ apart and the fringes are observed on a screen
   $1.0\ \text{m}$ away. Find (a) the fringe width, (b) the distance between the
   3rd bright fringe on one side and the 3rd dark fringe on the other side of the
   centre, and (c) the new fringe width if the source is changed to one of
   wavelength $442\ \text{nm}$. <span class="marks">[8]</span>

::: note Answer to Group C question 2
(a) $\beta = \dfrac{\lambda D}{d} = \dfrac{589\times10^{-9}\times1.0}{1.0\times10^{-3}}
= 5.89\times10^{-4}\ \text{m} = 0.589\ \text{mm}$.

(b) 3rd bright fringe: $y_1 = 3\beta = 1.767\ \text{mm}$ on one side.
3rd dark fringe: $y_2 = 2.5\beta = 1.4725\ \text{mm}$ on the other side.
Since they are on opposite sides, the separation is
$1.767 + 1.4725 = 3.24\ \text{mm}$.

(c) $\beta' = \dfrac{442\times10^{-9}\times1.0}{1.0\times10^{-3}} = 0.442\ \text{mm}$
— blue light gives narrower fringes.
:::
