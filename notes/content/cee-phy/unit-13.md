---
subject: Physics
grade: CEE
unit: 13
title: Wave Optics: Interference, Diffraction and Polarization
area: Waves and Optics
hours: 2
---

Light behaves as a wave in three experiments that no particle model explains: two
beams that add to darkness (interference), light that spreads into the shadow of an
edge (diffraction), and light that refuses to pass through two crossed sheets
(polarization). The Waves and Optics area carries **8 of the 50 Physics questions**, with about **2** questions from this chapter — usually
one numerical on a fringe or a slit and one short conceptual item. The whole chapter
turns on a single question asked at a point on a screen: *what is the path
difference here, and is it a whole number of wavelengths?*

::: key What the paper asks from this chapter
- What makes two sources **coherent**, and the two ways of producing coherent beams (wavefront and amplitude).
- The interference conditions: path difference $n\lambda$ for bright, $(2n-1)\lambda/2$ for dark; and $\phi = 2\pi\Delta/\lambda$.
- Young's double slit: $\beta = \lambda D/d$, its three proportionalities, $\beta$ in a liquid, and the shift made by a slab.
- Intensity: $I = I_1 + I_2 + 2\sqrt{I_1I_2}\cos\phi$ and $I_{max}/I_{min} = (a_1+a_2)^2/(a_1-a_2)^2$.
- Single slit: **minima** at $a\sin\theta = n\lambda$; central maximum width $2D\lambda/a$.
- Grating: $(a+b)\sin\theta = n\lambda$; how many orders fit; resolving power of a telescope and a microscope.
- Malus's law $I = I_0\cos^2\theta$; Brewster's law $\tan\theta_p = \mu$; why reflected light is partly polarized.
:::

## 13.1 Coherent sources and the conditions for interference; Young's double-slit experiment

### 13.1.1 Superposition, and what interference actually is

When two waves reach the same point, the resultant displacement is the **vector sum**
of the two displacements. The waves pass through one another and separate again
unchanged. What we see on a screen is not the displacement but the **intensity**,
which is proportional to the square of the resultant amplitude:

```photo id="cee-phy/ripple-interference" caption="Two-source interference in a ripple tank. The bright curved bands are lines of constructive interference (antinodal lines) and the darker gaps between them are destructive interference - the water-wave version of Young's double-slit fringes." width="72"
call 0.22 0.92 0.30 0.68 "Antinodal line: crests meet crests"
call 0.84 0.92 0.66 0.56 "Nodal line: calm water"
```


$$ I = I_1 + I_2 + 2\sqrt{I_1I_2}\cos\phi $$

where $I_1$ and $I_2$ are the intensities the waves would have separately and $\phi$
is the phase difference between them at that point. Three cases matter:

| Phase difference | Path difference | Intensity | Name |
|---|---|---|---|
| $0, 2\pi, 4\pi, \dots$ | $0, \lambda, 2\lambda, \dots$ | $(\sqrt{I_1}+\sqrt{I_2})^2$, maximum | constructive |
| $\pi, 3\pi, 5\pi, \dots$ | $\lambda/2, 3\lambda/2, \dots$ | $(\sqrt{I_1}-\sqrt{I_2})^2$, minimum | destructive |
| $\pi/2$ | $\lambda/4$ | $I_1 + I_2$ | neither |

For two **equal** sources, $I_1 = I_2 = I_0$: the maximum is $4I_0$ (not $2I_0$ —
amplitudes add, and $2^2 = 4$) and the minimum is exactly zero. Energy is not
destroyed; it is redistributed from the dark fringes into the bright ones, and the
average intensity over the pattern is still $2I_0$.

```photo id="cee-phy/newtons-rings" caption="Newton's rings in monochromatic light: concentric bright and dark fringes formed by interference between light reflected at the curved lens surface and the flat plate beneath it. The rings crowd together towards the edge because the air film thickens faster there." width="62"
call 0.74 0.08 0.50 0.50 "Centre: point of contact"
call 0.22 0.92 0.30 0.78 "Fringes crowd outward"
```


::: caution Adding intensities is wrong
Two identical lamps lighting a wall give $2I$. Two *coherent* beams of the same
intensity give $4I$ at a bright fringe and $0$ at a dark one. Whenever a question
says "coherent", add **amplitudes** first and then square; never add intensities
unless the sources are incoherent.
:::

The **contrast** of a pattern is measured by its visibility,

$$ V = \frac{I_{max} - I_{min}}{I_{max} + I_{min}} $$

which is 1 for equal amplitudes and falls as the amplitudes become unequal. Writing
the amplitude ratio as $a_1/a_2$,

$$ \frac{I_{max}}{I_{min}} = \left(\frac{a_1+a_2}{a_1-a_2}\right)^2 = \left(\frac{\sqrt{I_1}+\sqrt{I_2}}{\sqrt{I_1}-\sqrt{I_2}}\right)^2 $$

This one formula generates a whole family of paper questions, and the trap is always
the same: an **intensity** ratio must be square-rooted before it is put into the
amplitude formula.

### 13.1.2 Coherent sources

::: definition Coherent sources
Two sources are **coherent** if they emit waves of the same frequency whose phase
difference at any point remains constant in time. Only then is the interference
pattern stationary and visible.
:::

Two independent lamps, even two identical sodium lamps, are **not** coherent. Each
atom emits a wave train lasting about $10^{-8}$ s, and the phase of the next train is
random; the pattern from one pair of trains is wiped out by the next, long before the
eye or a photographic plate can record it. A laser is different: stimulated emission
keeps the phase fixed over a coherence length of metres, so two beams from one laser
interfere easily.

Since independent sources will not do, one source must be **split** and the two parts
recombined. There are two ways:

| Method | What is divided | Examples |
|---|---|---|
| Division of **wavefront** | one wavefront is cut into two parts by slits, mirrors or a prism | Young's double slit, Fresnel biprism, Lloyd's mirror |
| Division of **amplitude** | one beam is partly reflected and partly transmitted at a surface | thin films, Newton's rings, Michelson interferometer |

### 13.1.3 The conditions for sustained interference

For a pattern that can be seen and measured, all of the following must hold:

1. The two sources must be **coherent** — same frequency, constant phase difference.
2. They must have the same **wavelength** (monochromatic light gives clean fringes).
3. Their **amplitudes must be comparable**; if one beam is much weaker the minima
   are only slightly darker than the maxima and the fringes are washed out.
4. The two waves must have the same (or nearly the same) **plane of polarization**;
   perpendicularly polarized beams do not interfere at all.
5. The source must be **narrow**. A wide source behaves as many independent point
   sources whose patterns are displaced from one another and overlap into uniform
   brightness.
6. The path difference must be within the **coherence length** of the light;
   beyond it the phase relationship is lost.

### 13.1.4 Path difference and phase difference

A path difference $\Delta$ means one wave has travelled a distance $\Delta$ further
than the other. One whole wavelength corresponds to a phase change of $2\pi$, so

$$ \phi = \frac{2\pi}{\lambda}\,\Delta \qquad\text{and}\qquad \Delta = \frac{\lambda}{2\pi}\,\phi $$

| Path difference $\Delta$ | Phase difference $\phi$ | Result with equal sources |
|---|---|---|
| $0$ | $0$ | bright, $4I_0$ |
| $\lambda/4$ | $\pi/2$ | $2I_0$ |
| $\lambda/2$ | $\pi$ | dark, zero |
| $3\lambda/4$ | $3\pi/2$ | $2I_0$ |
| $n\lambda$ | $2n\pi$ | bright |
| $(2n-1)\lambda/2$ | $(2n-1)\pi$ | dark |

**Optical path.** In a medium of refractive index $\mu$ the wavelength is $\lambda/\mu$
while the frequency is unchanged, so the same geometrical distance contains $\mu$
times as many wavelengths. The **optical path** is $\mu \times$ (geometrical path),
and it is optical paths that are compared when the two beams pass through different
media.

### 13.1.5 Young's double slit: where the fringes come from

A single slit S is placed in front of two narrow slits $S_1$ and $S_2$ a distance $d$
apart, and a screen stands a distance $D$ beyond them, with $D \gg d$. Light from S
reaches $S_1$ and $S_2$ in phase, so they act as two coherent sources. At a point P on
the screen, at distance $y$ from the centre O, the two beams have travelled slightly
different distances and interfere.

::: derivation Fringe width in Young's double slit
We start from the geometry of the two paths and want the spacing between neighbouring
bright fringes.

**Setting up.** Slits $S_1$, $S_2$ separated by $d$; screen at distance $D \gg d$;
P at height $y$ above the centre O.

**Step 1 — write the two path lengths by Pythagoras.**
$$ S_2P^2 = D^2 + \left(y + \frac{d}{2}\right)^2, \qquad S_1P^2 = D^2 + \left(y - \frac{d}{2}\right)^2 $$

**Step 2 — subtract, so that $D^2$ cancels.**
$$ S_2P^2 - S_1P^2 = \left(y + \frac{d}{2}\right)^2 - \left(y - \frac{d}{2}\right)^2 = 2yd $$

**Step 3 — factor the left side.**
$$ (S_2P - S_1P)(S_2P + S_1P) = 2yd $$

**Step 4 — use $D \gg d$ and $D \gg y$**, so that $S_2P + S_1P \approx 2D$. Then
$$ \Delta = S_2P - S_1P = \frac{2yd}{2D} = \frac{yd}{D} $$

**Step 5 — bright fringes need $\Delta = n\lambda$.**
$$ \frac{y_n d}{D} = n\lambda \qquad\Longrightarrow\qquad y_n = \frac{n\lambda D}{d} $$

**Step 6 — the spacing is the difference between consecutive orders.**
$$ \beta = y_{n+1} - y_n = \frac{(n+1)\lambda D}{d} - \frac{n\lambda D}{d} = \frac{\lambda D}{d} $$

**Result.**
$$ \beta = \frac{\lambda D}{d} $$

**What it means.** Every bright fringe is the same distance $\beta$ from the next — the
pattern is a comb of equally spaced lines. $\beta$ grows with $\lambda$ and $D$ and
shrinks as the slits are moved apart. The result assumes $D \gg d$, small angles
($\sin\theta \approx \tan\theta \approx \theta$), a monochromatic coherent source and
one medium throughout.
:::

::: tip The examiner is looking for
The Pythagoras step, the difference-of-squares factorisation, and the explicit
approximation $S_2P + S_1P \approx 2D$. Write the reason for the approximation in
words; that sentence usually carries a mark.
:::

| Quantity | Formula |
|---|---|
| Position of the $n$th bright fringe | $y_n = n\lambda D/d$, $n = 0, 1, 2, \dots$ |
| Position of the $n$th dark fringe | $y_n = (2n-1)\lambda D/d$, $n = 1, 2, \dots$ |
| Fringe width | $\beta = \lambda D/d$ |
| Angular fringe width | $\theta = \lambda/d$ |
| Path difference at P | $\Delta = yd/D$ |

The central fringe ($n = 0$) is bright because the paths are equal. The first dark
fringe is at half a fringe width from the centre, the first bright fringe at one full
fringe width.

```figure caption="Young's double slit. The two slits act as coherent sources; at P the path difference is $yd/D$, which decides bright or dark."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,3.0))
ax.axis('off'); ax.set_xlim(0,7.6); ax.set_ylim(0,5.3)
ax.plot([2.2,2.2],[0.6,2.32], color=INK, lw=5.0, solid_capstyle='butt')
ax.plot([2.2,2.2],[2.42,2.58], color=INK, lw=5.0, solid_capstyle='butt')
ax.plot([2.2,2.2],[2.68,4.4], color=INK, lw=5.0, solid_capstyle='butt')
ax.plot([6.6,6.6],[0.6,4.4], color=MUTED, lw=3.5, solid_capstyle='butt')
ax.text(6.62,4.52,'screen', fontsize=8.5, color=MUTED, ha='right')
ax.plot(0.45,2.5,'o', color=ACCENT, ms=6.5)
ax.text(0.45,2.78,'S', ha='center', fontsize=9.5)
for ys in (2.37,2.63):
    ax.plot([0.45,2.2],[2.5,ys], color=ACCENT, lw=1.2)
ax.plot([2.2,6.6],[2.63,3.62], color=ACCENT, lw=1.2)
ax.plot([2.2,6.6],[2.37,3.62], color=ACCENT, lw=1.2)
ax.plot([2.62,6.78],[2.5,2.5], color=MUTED, lw=1.0, ls=(0,(3,2)))
ax.text(6.70,2.44,'O', fontsize=9, va='top')
ax.plot(6.6,3.62,'o', color=INK, ms=4.5)
ax.text(6.74,3.66,'P', fontsize=9.5, va='center')
ax.annotate('', xy=(6.42,3.60), xytext=(6.42,2.52), arrowprops=dict(arrowstyle='<->', color=MUTED, lw=1.0, mutation_scale=8))
ax.text(6.34,3.06,'y', fontsize=9.5, color=MUTED, ha='right', va='center')
ax.annotate('', xy=(2.3,0.95), xytext=(6.5,0.95), arrowprops=dict(arrowstyle='<->', color=MUTED, lw=1.0, mutation_scale=8))
ax.text(4.4,0.55,'D', fontsize=9.5, color=MUTED, ha='center')
ax.text(2.42,2.86,'S₁', fontsize=9)
ax.text(2.42,2.50,'d', fontsize=9.5)
ax.text(2.42,2.14,'S₂', fontsize=9)
```

### 13.1.6 What changes the fringe width — and what does not

| Change made | Effect on $\beta$ | Reason |
|---|---|---|
| Longer wavelength (red instead of violet) | increases | $\beta \propto \lambda$ |
| Screen moved further away | increases | $\beta \propto D$ |
| Slits moved further apart | decreases | $\beta \propto 1/d$ |
| Whole apparatus immersed in a liquid of index $\mu$ | falls to $\beta/\mu$ | $\lambda_{liquid} = \lambda/\mu$ |
| A slab of thickness $t$, index $\mu$, over one slit | unchanged; the pattern **shifts** by $(\mu-1)t/\beta$ fringes towards that slit | extra optical path $(\mu-1)t$ |
| White light instead of monochromatic | central fringe white, coloured fringes either side, red outermost | $\beta \propto \lambda$ |
| One slit covered | fringes disappear, only a broad diffraction pattern remains | one source only |
| Order $n$ of the fringe | no effect | $\beta$ is independent of $n$ |

**Why the pattern shifts with a slab.** The slab adds $(\mu-1)t$ to the optical path
of one beam. To bring the paths back to equality the point P must move towards the
covered slit, so the whole pattern — including the white central fringe — moves that
way. The number of fringes through which it moves is the extra optical path divided
by one fringe width.

::: caution Three traps in one formula
1. $\beta \propto 1/d$, **not** $1/d^2$ and not $1/D$.
2. Immersing the apparatus in water changes $\lambda$, not the frequency, and not $D$
   or $d$; so $\beta$ falls by the factor $\mu$ — it does not rise.
3. The **fringe width** is unchanged by a slab; only the **position** of the pattern
   moves. Many students wrongly say the fringes get wider.
:::

::: example Worked example 13.1 — fringe width, in air and in water
**Problem.** Light of wavelength 600 nm falls on two slits 0.5 mm apart; the screen is
1.0 m away. Find the fringe width. What does it become if the whole set-up is
immersed in water of refractive index 4/3?

**Solution.** $\beta = \lambda D/d = (600\times10^{-9})(1.0)/(0.5\times10^{-3}) = 1.2\times10^{-3}$ m $= 1.2$ mm.
In water $\lambda' = 600/1.333 = 450$ nm, so $\beta' = \beta/\mu = 1.2/(4/3) = 0.9$ mm.
The frequency is unchanged; only the wavelength in the medium matters.
:::

::: example Worked example 13.2 — shift produced by a glass sheet
**Problem.** In a double-slit experiment $\beta = 0.1$ mm. A glass sheet 0.2 mm thick
and of refractive index 1.5 is placed in front of one slit. Through how many fringes
does the pattern shift, and in which direction?

**Solution.** Extra optical path $= (\mu-1)t = 0.5\times0.2 = 0.1$ mm. Number of
fringes $= 0.1/0.1 = 1$. The pattern shifts by one fringe **towards the covered
slit**, because that beam has been delayed.
:::

::: example Worked example 13.3 — intensity ratio from an intensity ratio
**Problem.** Two coherent beams of intensities $I$ and $4I$ interfere. Find
$I_{max}/I_{min}$.

**Solution.** Amplitudes are proportional to $\sqrt{I}$, so $a_1:a_2 = 1:2$. Then
$I_{max}/I_{min} = (3/1)^2 = 9$. Answer 9 : 1. Note that the intensity ratio 1 : 4
becomes an amplitude ratio 1 : 2 before it is used — the commonest slip is to write
$(4+1)/(4-1)$.
:::

### 13.1.7 Thin films and Newton's rings

A soap film or a thin oil slick shows coloured bands in daylight. The two interfering
beams here are the reflection from the **top** surface and the reflection from the
**bottom** surface of the film, so this is division of amplitude.

For a film of thickness $t$ and refractive index $\mu$, with light travelling at angle
$r$ inside the film, the second beam covers a distance $2t/\cos r$ in the film; but the
extra optical path, measured between wavefronts of the two emerging rays, works out to
$2\mu t\cos r$ (the $\cos r$ appears because the rays leave along the same direction).
In addition, the reflection at the top surface is from a denser medium (air to film),
which changes the phase by $\pi$, equivalent to an extra $\lambda/2$. Hence

$$ \Delta = 2\mu t\cos r + \frac{\lambda}{2} $$

| Reflected light from a film in air | Condition |
|---|---|
| Bright | $2\mu t\cos r = (2n-1)\lambda/2$ |
| Dark | $2\mu t\cos r = n\lambda$ |

```figure caption="Thin-film interference. Ray 1 reflects at the top surface and suffers a phase change of π; ray 2 goes down and back through the film, so the two differ in optical path by $2\mu t\cos r$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.9))
ax.axis('off'); ax.set_xlim(0.4,7.5); ax.set_ylim(1.55,5.15)
ax.add_patch(plt.Rectangle((1.2,2.0), 5.2, 1.0, facecolor=ACCENT, alpha=0.13, edgecolor='none'))
ax.plot([1.2,6.4],[3.0,3.0], color=INK, lw=2.0)
ax.plot([1.2,6.4],[2.0,2.0], color=INK, lw=2.0)
ax.text(1.40,2.38,'film, refractive index μ', fontsize=8.5, color=MUTED)
ax.plot([2.8,2.8],[2.62,3.58], color=MUTED, lw=0.9, ls=(0,(3,2)))
ax.text(2.86,3.62,'normal', fontsize=7.8, color=MUTED)
ax.annotate('', xy=(2.8,3.0), xytext=(1.15,4.55),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.3, mutation_scale=9))
ax.text(1.02,4.72,'incident', fontsize=8.5, color=ACCENT, ha='left')
ax.annotate('', xy=(4.55,4.55), xytext=(2.8,3.0),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.3, mutation_scale=9))
ax.plot([2.8,3.4],[3.0,2.0], color=ACCENT, lw=1.3)
ax.plot([3.4,4.0],[2.0,3.0], color=SERIES[1], lw=1.3)
ax.annotate('', xy=(5.55,4.55), xytext=(4.0,3.0),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.3, mutation_scale=9))
ax.plot(2.8,3.0,'o', color=INK, ms=3.6, zorder=6)
ax.text(3.88,4.44,'ray 1', fontsize=8.6, color=SERIES[1], ha='right')
ax.text(5.05,3.76,'ray 2', fontsize=8.6, color=SERIES[1], ha='left')
ax.annotate('', xy=(6.62,3.0), xytext=(6.62,2.0),
            arrowprops=dict(arrowstyle='<->', color=MUTED, lw=1.0, mutation_scale=8))
ax.text(6.72,2.5,'t', fontsize=9.5, color=MUTED, ha='left', va='center')
```

At near-normal incidence $\cos r \approx 1$. This is why a soap film appears black just
before it bursts: as $t \to 0$ the condition $2\mu t = 0 = n\lambda$ with $n = 0$ is a
dark condition.

**Anti-reflection coating.** A coating whose refractive index lies between those of
air and glass gives a $\pi$ phase change at *both* surfaces, so the two shifts cancel.
Destruction then needs $2\mu t = \lambda/2$, i.e. $t = \lambda/(4\mu)$ — a
quarter-wavelength layer.

**Newton's rings.** A plano-convex lens of radius of curvature $R$ rests on a flat
glass plate, trapping a thin air film whose thickness at radius $r$ is $t = r^2/(2R)$.
With $\mu = 1$ and normal incidence:

| Feature (reflected light) | Result |
|---|---|
| Centre | **dark**, because $t = 0$ gives the dark condition |
| Dark rings | $r_n = \sqrt{n\lambda R}$, $n = 1, 2, 3, \dots$ (the centre is $n = 0$) |
| Bright rings | $r_n = \sqrt{(2n-1)\lambda R/2}$, $n = 1, 2, 3, \dots$ |
| Spacing | rings crowd together as $r$ grows, since $r \propto \sqrt{n}$ |
| In transmitted light | centre **bright**, pattern complementary to the reflected one |
| Gap filled with liquid of index $\mu$ | rings shrink, $r \propto 1/\sqrt{\mu}$ |

::: example Worked example 13.4 — radius of a Newton's ring
**Problem.** A plano-convex lens of radius of curvature 1.0 m rests on a glass plate
and is viewed in reflected light of wavelength 600 nm. Find the radius of the third
dark ring.

**Solution.** $r_3 = \sqrt{3\lambda R} = \sqrt{3(600\times10^{-9})(1.0)} = \sqrt{1.8\times10^{-6}} = 1.34\times10^{-3}$ m
$= 1.34$ mm.
:::

## 13.2 Diffraction at a single slit and at a grating; resolving power of optical instruments

### 13.2.1 What diffraction is

**Diffraction** is the spreading of a wave after it passes an obstacle or an aperture,
so that light appears inside the geometrical shadow. It becomes noticeable when the
size of the obstacle or slit is comparable with the wavelength. Sound bends round
doorways easily because its wavelength is about a metre; light does not noticeably
bend round a door because its wavelength is a fraction of a micrometre — but round a
razor edge or through a narrow slit the fringes are clear.

| | Fresnel diffraction | Fraunhofer diffraction |
|---|---|---|
| Source and screen | at finite distances | effectively at infinity (lenses used) |
| Wavefronts at the aperture | spherical or cylindrical | plane |
| Treatment | complicated | simple; the standard school case |

### 13.2.2 Single slit: where the minima fall

Let parallel rays fall on a slit of width $a$. Consider the secondary wavelets leaving
the slit at angle $\theta$ to the straight-through direction. The ray from the top edge
and the ray from the bottom edge differ in path by $a\sin\theta$.

**The first minimum.** Divide the slit into two halves. The ray from the top edge and
the ray from the centre of the slit differ by $\frac{a}{2}\sin\theta$. If that equals
$\lambda/2$, each pair of points (one in each half) cancels, and the whole slit cancels
itself:

$$ \frac{a}{2}\sin\theta = \frac{\lambda}{2} \qquad\Longrightarrow\qquad a\sin\theta = \lambda $$

The same pairing argument, with the slit divided into $2n$ parts, gives the $n$th
minimum:

$$ a\sin\theta = n\lambda, \qquad n = 1, 2, 3, \dots $$

Between the minima lie **secondary maxima**, approximately at

$$ a\sin\theta = (2n+1)\frac{\lambda}{2}, \qquad n = 1, 2, 3, \dots $$

but they are much weaker than the central maximum, and their exact positions are
slightly displaced from this formula.

::: caution Minima here, maxima there
For a **single slit**, $a\sin\theta = n\lambda$ gives **minima** (dark).
For a **double slit or grating**, $d\sin\theta = n\lambda$ gives **maxima** (bright).
The same-looking equation describes opposite things, because in the single slit the
$n\lambda$ is the path difference between the two **edges of one slit**, while in the
grating it is between **corresponding points of two neighbouring slits**. Examiners
build a distractor on exactly this swap.
:::

### 13.2.3 The central maximum

The first minimum is at $\sin\theta_1 = \lambda/a$, so for small angles
$\theta_1 \approx \lambda/a$. The central maximum therefore has

| Quantity | Value |
|---|---|
| Angular half-width | $\theta_1 = \lambda/a$ |
| Full angular width | $2\lambda/a$ |
| Linear width on a screen at distance $D$ | $2D\lambda/a$ |
| Width of each secondary maximum | $D\lambda/a$ (half the central one) |

So the central maximum is **twice as wide** as any secondary maximum and far
brighter. A narrower slit ($a$ smaller) gives a **wider** central maximum — the
opposite of what the word "narrow" suggests, and a favourite question.

```figure caption="The same slit, two experiments. Dashed: single slit of width $a$ — a broad envelope whose first minimum is at $y = \lambda D/a = 3.0$ mm. Solid: two such slits a distance $d = 5a$ apart — fine fringes of width $\lambda D/d = 0.6$ mm inside that envelope. The two patterns have minima in completely different places."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.9))
lam, D, a, d = 600e-9, 1.0, 0.2e-3, 1.0e-3
y = np.linspace(-6.2e-3, 6.2e-3, 6000)
th = y/D
env = np.sinc(a*th/lam)**2
fringes = env*np.cos(np.pi*d*th/lam)**2
ax.plot(y*1e3, env, color=MUTED, lw=1.4, ls=(0,(4,2)), label='single slit, width a')
ax.plot(y*1e3, fringes, color=ACCENT, lw=1.0, label='two slits, separation d = 5a')
ax.axhline(0, color=INK, lw=0.7)
ax.annotate('first minimum\na sinθ = λ', xy=(3.0,0.02), xytext=(4.20,0.52), fontsize=8.4,
            ha='center', va='center',
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.9, mutation_scale=8))
ax.annotate('fringe width\nλD/d = 0.6 mm', xy=(-1.8,0.33), xytext=(-4.30,0.44), fontsize=8.4,
            ha='center', va='center',
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=0.9, mutation_scale=8))
ax.set_xlabel('position on screen  y  (mm)'); ax.set_ylabel('relative intensity')
ax.set_xlim(-6.2,6.2); ax.set_ylim(-0.03,1.30)
ax.set_xticks([-6,-4,-2,0,2,4,6])
ax.spines[['top','right']].set_visible(False)
ax.legend(loc='upper right', fontsize=7.9, frameon=False, handlelength=1.8)
```

::: example Worked example 13.5 — width of the central maximum
**Problem.** Light of wavelength 600 nm passes through a slit 0.2 mm wide and falls on
a screen 1.0 m away. Find the width of the central maximum.

**Solution.** $2D\lambda/a = 2(1.0)(600\times10^{-9})/(0.2\times10^{-3}) = 6.0\times10^{-3}$ m
$= 6$ mm. The half-width, 3 mm, is the distance to the first minimum.
:::

### 13.2.4 Interference and diffraction compared

| | Interference | Diffraction |
|---|---|---|
| Origin | two separate coherent sources | secondary wavelets from different parts of one wavefront |
| Fringe widths | all equal | central maximum twice as wide as the others |
| Intensity of maxima | equal, if the sources are equally bright | falls off rapidly away from the centre |
| Minima | perfectly dark for equal amplitudes | not perfectly dark |
| Number of fringes | few, and they are broad | many, crowding together |

### 13.2.5 The diffraction grating

A grating is a plate ruled with $N$ parallel slits per metre. The distance between
the centres of neighbouring slits is the **grating element**

$$ d = a + b = \frac{1}{N} $$

where $a$ is the slit width and $b$ the opaque width. Parallel rays diffracted at
angle $\theta$ from neighbouring slits differ in path by $d\sin\theta$, and they add
in phase when

$$ (a+b)\sin\theta = n\lambda, \qquad n = 0, 1, 2, \dots $$

$n$ is the **order** of the spectrum; $n = 0$ is the central white image. Because
hundreds of slits contribute, the maxima are extremely sharp and bright (intensity
proportional to $N^2$) while the space between them is almost dark. That is why a
grating, not a double slit, is used to measure wavelengths.

**How many orders fit.** Since $\sin\theta$ cannot exceed 1,

$$ n_{max} = \frac{d}{\lambda} $$

rounded **down** to a whole number. The highest order appears on each side of the
centre, so the total number of principal maxima is $2n_{max} + 1$ including the
central one.

**Missing orders.** If $d/a$ is a whole number, the diffraction minimum of each
individual slit falls on the $n = d/a$ interference maximum and that order is missing.

::: example Worked example 13.6 — orders from a grating
**Problem.** A grating has 5000 lines per cm and is used with light of wavelength
500 nm. Find the grating element and the highest order visible.

**Solution.** $d = 1/(5000\ \text{cm}^{-1}) = 1/(5\times10^{5}\ \text{m}^{-1}) = 2\times10^{-6}$ m.
$n_{max} = d/\lambda = 2\times10^{-6}/500\times10^{-9} = 4$. Orders 1 to 4 appear on
each side, so 9 principal maxima are seen in all.
:::

### 13.2.6 Resolving power of optical instruments

Two stars, or two nearby points of a specimen, are not point images: each is spread by
diffraction into a disc with a ring around it. The **Rayleigh criterion** says they are
just resolved when the centre of one diffraction pattern falls on the first minimum of
the other.

| Instrument | Limit of resolution | Resolving power |
|---|---|---|
| Telescope (objective diameter $D$) | $\theta_{min} = 1.22\lambda/D$ | $D/(1.22\lambda)$ |
| Microscope (numerical aperture $\mu\sin\theta$) | $d_{min} = \lambda/(2\mu\sin\theta)$ | $2\mu\sin\theta/\lambda$ |
| Grating ($N$ lines, order $n$) | — | $nN$ |

For the telescope, only the **diameter** of the objective matters — not its focal
length, not the magnification. A larger objective collects more light *and* resolves
finer detail, which is why research telescopes are built large. For the microscope,
the **numerical aperture** $\text{NA} = \mu\sin\theta$ is what counts; immersion oil
raises $\mu$ from 1 to about 1.5 and so improves resolution by that factor. Some books
quote the same limit in Rayleigh's form, $0.61\lambda/(\mu\sin\theta)$; use whichever
form the numbers in the question fit.

::: example Worked example 13.7 — resolution of a telescope
**Problem.** A telescope has an objective of diameter 10 cm and is used at wavelength
600 nm. What is the smallest angular separation it can resolve?

**Solution.** $\theta_{min} = 1.22\lambda/D = 1.22(600\times10^{-9})/(0.10) = 7.3\times10^{-6}$ rad.
Doubling the diameter would halve this angle.
:::

## 13.3 Polarization and Brewster's law

### 13.3.1 Unpolarized and plane-polarized light

Light is a transverse wave: the electric field oscillates perpendicular to the
direction of travel. In **unpolarized** light the direction of that oscillation
changes at random from instant to instant, so on average all directions across the
beam are equally represented. In **plane-polarized** light the electric field is
confined to one plane containing the ray.

- The **plane of vibration** is the plane containing the electric vector and the ray.
- The **plane of polarization** is perpendicular to the plane of vibration and also
  contains the ray.

Only transverse waves can be polarized. Sound, a longitudinal wave, cannot be, and
this is the experimental proof that light is transverse — a fact that interference and
diffraction alone cannot establish.

### 13.3.2 How light is polarized

| Method | What happens |
|---|---|
| Selective absorption | a Polaroid absorbs the component along its long molecular chains and transmits the perpendicular one |
| Reflection | at one particular angle (Brewster's) the reflected beam is completely polarized |
| Refraction | a pile of glass plates transmits a beam that is partially, and after many plates almost completely, polarized |
| Scattering | light scattered at 90° by air molecules is strongly polarized |
| Double refraction | calcite splits a beam into ordinary and extraordinary rays, polarized at right angles |

A **Polaroid** is a sheet of aligned long-chain molecules. Light with its electric
vector along the chains drives electrons along them and is absorbed; light
perpendicular to the chains passes. The first sheet is called the **polarizer**, the
second (used to examine the light) the **analyser**.

### 13.3.3 Malus's law

If plane-polarized light of intensity $I_0$ falls on an analyser whose transmission
axis makes an angle $\theta$ with the plane of polarization, the transmitted intensity
is

$$ I = I_0\cos^2\theta $$

The transmitted beam remains plane-polarized, with its plane along the analyser's
axis.

| Situation | Transmitted intensity |
|---|---|
| Unpolarized light $I_0$ through **one** Polaroid | $I_0/2$ |
| Plane-polarized $I_0$ through an analyser at $\theta$ | $I_0\cos^2\theta$ |
| Unpolarized $I_0$ through two Polaroids at $\theta$ | $(I_0/2)\cos^2\theta$ |
| Two Polaroids crossed ($\theta = 90^{\circ}$) | zero |
| Three sheets, first and third crossed, middle at 45° | $(I_0/2)(\cos^2 45^{\circ})(\cos^2 45^{\circ}) = I_0/8$ |

```figure caption="Malus's law: transmitted intensity against the angle between polarizer and analyser. Half the light survives at 45°, none at 90°."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9,2.8))
th = np.linspace(0,360,1200)
ax.plot(th, np.cos(np.radians(th))**2, color=ACCENT, lw=2.0)
ax.axhline(0.5, color=MUTED, lw=0.8, ls=(0,(3,2)))
ax.plot([45],[0.5],'o', color=INK, ms=4.5, zorder=5)
ax.plot([90],[0.0],'o', color=INK, ms=4.5, zorder=5)
ax.annotate('45°:  I₀/2', xy=(47,0.5), xytext=(78,0.70), fontsize=8.5,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
ax.annotate('90°: crossed, zero', xy=(90,0.015), xytext=(132,0.20), fontsize=8.5,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
ax.text(252,0.28,'I = I₀ cos²θ', fontsize=9.2, color=ACCENT, ha='center')
ax.set_xlabel('angle between the two axes  θ  (degrees)')
ax.set_ylabel('I / I₀')
ax.set_xlim(0,360); ax.set_ylim(-0.04,1.08)
ax.set_xticks([0,45,90,180,270,360])
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=0.5)
```

::: caution One sheet halves, it does not pass
Unpolarized light through a single Polaroid comes out at **half** intensity, not at
full intensity: the sheet removes the component perpendicular to its axis. Students
who forget the factor $1/2$ get twice the right answer for every stacked-sheet
question. And a **crossed** pair gives zero no matter how bright the source is.
:::

::: example Worked example 13.8 — two Polaroids at 60°
**Problem.** Unpolarized light of intensity $I_0$ passes through two Polaroids whose
axes are at 60° to each other. Find the emergent intensity.

**Solution.** The first sheet halves it: $I_0/2$. Malus then gives
$(I_0/2)\cos^2 60^{\circ} = (I_0/2)(1/4) = I_0/8$. The answer $I_0/4$ comes from
forgetting the halving; $3I_0/8$ from using $\sin^2$ instead of $\cos^2$.
:::

### 13.3.4 Polarization by reflection: Brewster's law

When unpolarized light strikes a transparent surface, both the reflected and the
refracted beams are partially polarized. At one particular angle of incidence — the
**polarizing angle** or **Brewster angle** $\theta_p$ — the reflected beam is
*completely* plane-polarized, with its electric vector perpendicular to the plane of
incidence. Brewster found that

$$ \tan\theta_p = \mu $$

where $\mu$ is the refractive index of the reflecting medium relative to the medium
the light comes from. At this angle the reflected and refracted rays are at right
angles:

$$ \theta_p + r = 90^{\circ} $$

| Medium (from air) | $\mu$ | $\theta_p$ |
|---|---|---|
| Water | 1.33 | 53° |
| Glass | 1.50 | 56.3° |
| A medium with $\mu = \sqrt{3}$ | 1.732 | 60° |

::: example Worked example 13.9 — Brewster angle and the refracted ray
**Problem.** Light is incident from air on a medium of refractive index $\sqrt{3}$.
Find the polarizing angle and the angle of refraction.

**Solution.** $\tan\theta_p = \sqrt{3}$, so $\theta_p = 60^{\circ}$. Then
$r = 90^{\circ} - 60^{\circ} = 30^{\circ}$. Check with Snell's law:
$\sin 60^{\circ}/\sin 30^{\circ} = 0.866/0.5 = 1.732 = \sqrt{3}$. ✓
:::

### 13.3.5 Why reflected light is partially polarized

The reflected beam is the radiation of the electric dipoles that the incident wave sets
oscillating in the medium. A dipole does not radiate along its own axis of oscillation.

- Dipoles oscillating **perpendicular** to the plane of incidence (parallel to the
  surface) can always radiate back into the reflected direction.
- Dipoles oscillating **in** the plane of incidence cannot radiate along their axis.
  At the Brewster angle the refracted ray is at 90° to the reflected ray, so those
  dipoles point exactly along the direction in which the reflected beam would travel —
  and they radiate nothing into it.

So at $\theta_p$ only the perpendicular component is reflected: the reflected beam is
100 % polarized. At any other angle the in-plane component is only partly suppressed,
so the reflected beam is **partially** polarized. The refracted beam is also partially
polarized, but in the complementary sense (it is richer in the in-plane component).

### 13.3.6 Where polarization is used

- **Sunglasses.** Glare from a horizontal road or water surface is largely
  horizontally polarized; a Polaroid with a vertical transmission axis blocks it while
  passing about half of the rest of the scene.
- **Photography.** A rotating polarizing filter removes reflections from glass and
  water and darkens the sky, because scattered skylight is polarized.
- **Liquid-crystal displays** work by switching the polarization of light between
  crossed polaroids.
- **3-D cinema** projects two images with perpendicular polarizations, and each
  eyepiece passes only one.
- **Stress analysis** in transparent models, and the study of optically active
  substances (a sugar solution rotates the plane of polarization).

```photogrid label="13.1" cols="2" ratio="1.2" caption="A CD is a reflection grating. (a) The 1.6 micrometre track spacing splits white light into rainbow arcs. (b) From d sin(theta) = m lambda, violet (400 nm) and red (700 nm) leave at 14.5 and 25.9 degrees in order 1, 30.0 and 61.0 degrees in order 2, while order 3 starts at 48.6 degrees and reaches the grazing limit at 533 nm because 3 x 700 / 1600 is more than 1. Orders 2 and 3 overlap from 48.6 to 61.0 degrees, so higher orders are not pure colours. Red bends more than violet, the reverse of a prism."
@ photo id="ceephy/cdrainbow" cap="Light from a window diffracted by the closely spaced tracks of a compact disc"
fit 1.2
focus 0.5 0.5
@ svg cap="Where the first three orders of a CD fall"
d = 1.6e-6
ang = lambda lam, m: math.degrees(math.asin(m * lam / d)) if m * lam / d <= 1 else None
def rgb(l):
    if l < 440: r, g, b = (440 - l) / 40, 0, 1
    elif l < 490: r, g, b = 0, (l - 440) / 50, 1
    elif l < 510: r, g, b = 0, 1, (510 - l) / 20
    elif l < 580: r, g, b = (l - 510) / 70, 1, 0
    elif l < 645: r, g, b = 1, (645 - l) / 65, 0
    else: r, g, b = 1, 0, 0
    return "#%02x%02x%02x" % tuple(int(255 * c) for c in (r, g, b))
a1v, a1r, a2v, a2r, a3v = ang(400e-9, 1), ang(700e-9, 1), ang(400e-9, 2), ang(700e-9, 2), ang(400e-9, 3)
assert ang(700e-9, 3) is None and abs(a1v - 14.48) < 0.01 and abs(a2r - 61.04) < 0.01 and abs(a2v - 30.0) < 1e-9
lo, hi = a3v, a2r
assert abs(lo - 48.59) < 0.01
facts = dict(a1v="%.1f" % a1v, a1r="%.1f" % a1r, a2v="%.1f" % a2v, a2r="%.1f" % a2r, a3v="%.1f" % a3v, lo="%.1f" % lo, hi="%.1f" % hi)
f = Fig(300, 236)
f.text(150, 14, "d sin(theta) = m lambda, d = 1.6 um", size=10.5, color=NAVY, bold=True)
X = lambda t: 40 + t * 2.6
for m, y in ((1, 40), (2, 80), (3, 120)):
    f.text(20, y + 13, "m=%d" % m, size=10.5, color=SLATE, bold=True)
    for lam in range(400, 700, 6):
        s1, s2 = m * lam * 1e-9 / d, m * (lam + 6) * 1e-9 / d
        if s2 > 1: break
        x1, x2 = X(math.degrees(math.asin(s1))), X(math.degrees(math.asin(s2)))
        f.box(x1, y, max(x2 - x1, 1.2), 26, fill=rgb(lam), stroke=rgb(lam), r=0, sw=0.3)
f.line(X(0), 160, X(90), 160, color=SLATE, sw=1.4)
for t in (0, 30, 60, 90): f.text(X(t), 173, "%d" % t, size=10.5, color=SLATE)
f.text(150, 192, "orders 2 and 3 overlap %.1f to %.1f" % (lo, hi), size=10.5, color=RED, bold=True)
f.text(150, 210, "order 1: %.1f (violet) to %.1f (red)" % (a1v, a1r), size=10.5, color=NAVY, bold=True)
f.text(150, 228, "angle theta in degrees from the normal", size=10.5, color=SLATE)
```

```photogrid label="13.2" cols="2" ratio="1.2" caption="Cutting glare with polarisers. (a) Polarising sunglasses pass light vibrating in one direction only, arranged to block the horizontal vibrations of glare. (b) The cell applies Malus's law I = I0 cos2(theta): the transmitted fraction is 75 per cent at 30 degrees, 50 per cent at 45 degrees and zero at 90 degrees. Light reflected from water or glass is partly polarised and is completely polarised parallel to the surface at Brewster's angle, tan(p) = n, which is 53.1 degrees for water and 56.3 degrees for glass. A lens turned across that direction therefore removes the glare from a lake or a windscreen while the rest of the scene stays visible."
@ photo id="ceephy3/sunglasses" cap="Polarising sunglasses"
fit 1.2
focus 0.5 0.5
@ svg cap="Malus's law and Brewster's angle"
import math
rows = [("%d deg" % a, math.cos(math.radians(a)) ** 2 * 100) for a in (0, 30, 45, 60, 90)]
bw_, bg = math.degrees(math.atan(1.33)), math.degrees(math.atan(1.5))
assert round(rows[1][1]) == 75 and round(rows[2][1]) == 50 and round(bw_, 1) == 53.1 and round(bg, 1) == 56.3
f = Fig(300, 236)
f.text(150, 12, "Malus: I / I0 = cos^2(theta), per cent", size=10.5, color=NAVY, bold=True)
hbars(f, rows, vmax=100, fmt="%.0f", x0=56, y0=28, bw=170, gap=26)
f.text(150, 168, "theta = angle between polariser and analyser", size=10, color=SLATE, bold=True)
f.text(150, 188, "Brewster angle: water %.1f deg, glass %.1f deg" % (bw_, bg), size=10.5, color=NAVY, bold=True)
f.text(150, 206, "unpolarised light through one polariser: 50%", size=10, color=SLATE, bold=True)
f.text(150, 222, "then a second at 45 deg: 25% of the original", size=10, color=SLATE, bold=True)
facts = dict(bw=bw_, bg=bg, a30=rows[1][1], a45=rows[2][1])
```

## Formula and fact sheet

| Topic | Formula or fact |
|---|---|
| Superposition | $I = I_1 + I_2 + 2\sqrt{I_1I_2}\cos\phi$ |
| Phase from path | $\phi = 2\pi\Delta/\lambda$ |
| Bright / dark | $\Delta = n\lambda$ / $\Delta = (2n-1)\lambda/2$ |
| Amplitude and intensity | $I \propto a^2$; equal sources: $I_{max} = 4I_0$, $I_{min} = 0$ |
| Intensity ratio | $I_{max}/I_{min} = (a_1+a_2)^2/(a_1-a_2)^2$ |
| Visibility | $V = (I_{max}-I_{min})/(I_{max}+I_{min})$ |
| YDSE bright | $y_n = n\lambda D/d$ |
| YDSE dark | $y_n = (2n-1)\lambda D/d$ |
| Fringe width | $\beta = \lambda D/d$; in a medium $\beta/\mu$; angular width $\lambda/d$ |
| Slab in one path | shift $= (\mu-1)t/\beta$ fringes, towards the slab |
| Thin film, reflected | $2\mu t\cos r + \lambda/2 = n\lambda$ (bright), $= (2n-1)\lambda/2$ (dark) |
| Anti-reflection coating | $t = \lambda/(4\mu)$ |
| Newton's rings | dark $r_n = \sqrt{n\lambda R}$; bright $r_n = \sqrt{(2n-1)\lambda R/2}$; centre dark in reflection |
| Single-slit minima | $a\sin\theta = n\lambda$ |
| Single-slit secondary maxima | $a\sin\theta \approx (2n+1)\lambda/2$ |
| Central maximum width | $2D\lambda/a$; secondary maximum $D\lambda/a$ |
| Grating | $(a+b)\sin\theta = n\lambda$; $d = 1/N$; $n_{max} = d/\lambda$ |
| Grating resolving power | $nN$ |
| Telescope | $\theta_{min} = 1.22\lambda/D$; RP $= D/(1.22\lambda)$ |
| Microscope | $d_{min} = \lambda/(2\mu\sin\theta)$; RP $= 2\mu\sin\theta/\lambda$ |
| Malus | $I = I_0\cos^2\theta$; one Polaroid halves unpolarized light |
| Brewster | $\tan\theta_p = \mu$; $\theta_p + r = 90^{\circ}$ |
| Standard values | glass $\mu = 1.5$, $\theta_p \approx 56.3^{\circ}$; water $\mu = 4/3$, $\theta_p \approx 53^{\circ}$ |

## Chapter summary

- Interference is superposition of **coherent** waves; intensity is
  $I_1+I_2+2\sqrt{I_1I_2}\cos\phi$ with $\phi = 2\pi\Delta/\lambda$. Equal sources give
  $4I_0$ bright and zero dark.
- Bright fringes need $\Delta = n\lambda$; dark fringes need
  $\Delta = (2n-1)\lambda/2$. Optical path is $\mu$ times geometrical path.
- Coherent beams are made by dividing a wavefront (double slit) or an amplitude (thin
  film). Two independent lamps never interfere.
- Young's double slit: $y_n = n\lambda D/d$ for bright fringes and $\beta = \lambda D/d$
  for the spacing — independent of the order, proportional to $\lambda$ and $D$,
  inversely proportional to $d$, and divided by $\mu$ in a liquid.
- A slab of thickness $t$ shifts the whole pattern by $(\mu-1)t/\beta$ fringes towards
  the covered slit without changing $\beta$.
- In a thin film the reflected beams differ by $2\mu t\cos r + \lambda/2$; in Newton's
  rings the reflected centre is dark and $r_n = \sqrt{n\lambda R}$ for dark rings.
- Single slit: **minima** at $a\sin\theta = n\lambda$, central maximum of width
  $2D\lambda/a$, twice the width of the secondary maxima.
- Grating: $(a+b)\sin\theta = n\lambda$; highest order $n_{max} = d/\lambda$; the
  maxima are sharp because many slits contribute.
- Resolving power: telescope $D/(1.22\lambda)$, microscope $2\mu\sin\theta/\lambda$ —
  bigger aperture or higher refractive index resolves finer detail.
- Polarization proves light is transverse. Malus: $I = I_0\cos^2\theta$, with one
  Polaroid halving unpolarized light. Brewster: $\tan\theta_p = \mu$, and at that angle
  the reflected and refracted rays are perpendicular and the reflected beam is fully
  polarized.

## Practice questions

**Set A — Recall (24 questions)**

1. Two light sources are coherent when they emit waves of
   (a) the same amplitude (b) equal intensity (c) the same frequency with a constant phase difference (d) the same wavelength with rapidly changing phase
2. In Young's double-slit experiment the fringe width is given by
   (a) $\lambda d/D$ (b) $\lambda D/d$ (c) $2\lambda D/d$ (d) $\lambda D/d^2$
3. The path difference required for constructive interference is
   (a) $(2n-1)\lambda/2$ (b) $n\lambda/2$ (c) $(2n+1)\lambda$ (d) $n\lambda$
4. A path difference of one wavelength corresponds to a phase difference of
   (a) $2\pi$ (b) $\pi$ (c) $\pi/2$ (d) $4\pi$
5. When the whole double-slit apparatus is immersed in water, the fringe width
   (a) increases (b) decreases (c) is unchanged (d) becomes zero
6. In single-slit diffraction the first minimum occurs where
   (a) $a\sin\theta = \lambda/2$ (b) $a\sin\theta = 3\lambda/2$ (c) $a\sin\theta = \lambda$ (d) $a\sin\theta = 2\lambda$
7. The width of the central maximum in single-slit diffraction, on a screen at distance D, is
   (a) $2\lambda D/a$ (b) $\lambda D/a$ (c) $\lambda D/2a$ (d) $2aD/\lambda$
8. The grating equation for the nth principal maximum is
   (a) $a\sin\theta = n\lambda$ (b) $(a+b)\sin\theta = (2n-1)\lambda$ (c) $d\cos\theta = n\lambda$ (d) $(a+b)\sin\theta = n\lambda$
9. The resolving power of a telescope of objective diameter D at wavelength $\lambda$ is
   (a) $1.22\lambda/D$ (b) $\lambda/D$ (c) $D/1.22\lambda$ (d) $1.22D/\lambda$
10. Malus's law gives the intensity transmitted through an analyser as
   (a) $I_0\cos\theta$ (b) $I_0\cos^2\theta$ (c) $I_0\sin^2\theta$ (d) $I_0/2$
11. Brewster's law states that the polarizing angle satisfies
   (a) $\tan\theta_p = \mu$ (b) $\sin\theta_p = \mu$ (c) $\cos\theta_p = \mu$ (d) $\tan\theta_p = 1/\mu$
12. At the polarizing angle the reflected and refracted rays are
   (a) parallel (b) at 45° (c) at 60° (d) at 90°
13. Two independent sodium lamps cannot give a sustained interference pattern because
   (a) they are too dim (b) their wavelengths differ too much (c) their phase difference changes at random (d) they emit white light
14. For fixed slit separation and screen distance, the fringe width is directly proportional to
   (a) the intensity (b) the wavelength (c) the frequency (d) the square of the wavelength
15. A Polaroid produces plane-polarized light from unpolarized light by
   (a) double refraction (b) scattering (c) reflection at the Brewster angle (d) selective absorption
16. In Newton's rings seen in reflected light, the centre of the pattern is
   (a) dark (b) bright (c) coloured (d) equally bright and dark
17. Two waves of equal intensity $I_0$ meet in phase. The resultant intensity is
   (a) $I_0$ (b) $2I_0$ (c) $4I_0$ (d) zero
18. The angular fringe width in Young's double-slit experiment is
   (a) $\lambda D/d$ (b) $\lambda/d$ (c) $d/\lambda$ (d) $\lambda D/d^2$
19. The path difference at the third dark fringe in Young's experiment is
   (a) $3\lambda$ (b) $2\lambda$ (c) $3\lambda/2$ (d) $5\lambda/2$
20. Diffraction of light is most noticeable when the obstacle is
   (a) comparable in size with the wavelength (b) much larger than the wavelength (c) much smaller than the wavelength (d) of any size, independent of wavelength
21. The phenomenon that shows light is a transverse wave is
   (a) interference (b) diffraction (c) polarization (d) dispersion
22. A grating has N lines per metre. Its grating element is
   (a) $N$ (b) $1/N$ (c) $N/2$ (d) $2/N$
23. In Young's experiment with white light, the central fringe is
   (a) red (b) violet (c) dark (d) white
24. The fringe width in Young's experiment does NOT depend on
   (a) the order n of the fringe (b) the wavelength used (c) the slit separation (d) the distance to the screen

::: note Answers and explanations — Set A
**1.** (c) — coherence means a fixed phase relationship, which requires the same frequency. Equal amplitude or equal intensity alone gives no stable pattern.
**2.** (b) — $\beta = \lambda D/d$. Option (a) is the reciprocal arrangement and (c) is the central-maximum width of a single slit.
**3.** (d) — constructive interference needs a whole number of wavelengths, $\Delta = n\lambda$; $(2n-1)\lambda/2$ is the destructive condition.
**4.** (a) — one wavelength is one full cycle, so $\phi = 2\pi\Delta/\lambda = 2\pi$.
**5.** (b) — in water $\lambda$ falls to $\lambda/\mu$, and $\beta \propto \lambda$, so the fringes get closer together.
**6.** (c) — pairing the slit into halves gives $\frac{a}{2}\sin\theta = \lambda/2$, hence $a\sin\theta = \lambda$. (a) is the *double-slit* path-difference condition misapplied.
**7.** (a) — the first minimum is at $y = \lambda D/a$, and the central maximum extends symmetrically to both sides, so its full width is $2\lambda D/a$.
**8.** (d) — the path difference between neighbouring slits is $(a+b)\sin\theta$, set equal to $n\lambda$ for a maximum.
**9.** (c) — resolving power is the reciprocal of the angular limit $1.22\lambda/D$. Option (a) is the limit of resolution itself, not the power.
**10.** (b) — the transmitted amplitude is $a_0\cos\theta$, so the intensity is $I_0\cos^2\theta$.
**11.** (a) — $\tan\theta_p = \mu$. At this angle $\theta_p + r = 90^{\circ}$.
**12.** (d) — the two rays are perpendicular at the polarizing angle; this is what allows the dipoles to radiate nothing into the reflected direction.
**13.** (c) — each atom emits a train of about $10^{-8}$ s with random phase, so the phase difference is not constant.
**14.** (b) — $\beta = \lambda D/d$, so $\beta \propto \lambda$. Frequency is inversely related to wavelength, so (c) is wrong.
**15.** (d) — a Polaroid absorbs the component along its aligned molecules and transmits the perpendicular one: selective absorption.
**16.** (a) — at the centre the air film has zero thickness, which satisfies the dark condition, so the centre is dark.
**17.** (c) — amplitudes add to $2a$, and intensity goes as amplitude squared: $4I_0$.
**18.** (b) — the angle subtended at the slits by one fringe is $\beta/D = \lambda/d$.
**19.** (d) — the $n$th dark fringe needs $\Delta = (2n-1)\lambda/2$; with $n = 3$ this is $5\lambda/2$.
**20.** (a) — diffraction is strong only when the obstacle or aperture is of the order of a wavelength.
**21.** (c) — only transverse waves can be polarized, so polarization proves light is transverse. Interference and diffraction occur for longitudinal waves too.
**22.** (b) — the grating element is the slit spacing, $d = 1/N$ when N is in lines per metre.
**23.** (d) — all wavelengths have zero path difference at the centre, so all colours arrive in phase and the central fringe is white.
**24.** (a) — $\beta = \lambda D/d$ contains no n; every fringe is the same distance from the next.
:::

**Set B — Understanding (14 questions)**

1. In Young's experiment both the slit separation and the screen distance are doubled. The fringe width
   (a) doubles (b) is unchanged (c) halves (d) becomes four times as large
2. The fringes disappear when the source slit is made wide because
   (a) different parts of the source give overlapping patterns of different phase (b) the light becomes monochromatic (c) the wavelength changes (d) diffraction stops
3. A thin glass plate is placed in front of the upper slit. The fringe pattern
   (a) disappears (b) becomes wider (c) shifts downward, away from the plate (d) shifts upward, towards the plate
4. Two coherent beams of intensities I and 4I interfere. The ratio $I_{max}:I_{min}$ is
   (a) 4 : 1 (b) 5 : 1 (c) 9 : 1 (d) 25 : 1
5. The width of a single slit is increased. Its central diffraction maximum
   (a) becomes narrower (b) becomes wider (c) keeps the same width (d) becomes wider and brighter
6. Compared with double-slit fringes, the principal maxima of a grating are
   (a) wider and dimmer (b) of the same width (c) narrower and brighter (d) narrower and dimmer
7. Two crossed Polaroids transmit no light. A third Polaroid, with its axis at 45° to both, is inserted between them. The transmitted intensity is now
   (a) zero (b) $I_0/8$ (c) $I_0/4$ (d) $I_0/2$
8. Light reflected from a glass surface at the polarizing angle is
   (a) unpolarized (b) circularly polarized (c) partially polarized (d) completely plane-polarized
9. A telescope's objective is replaced by one of larger diameter, other things unchanged. Its resolving power
   (a) increases (b) decreases (c) is unchanged (d) becomes zero
10. The resolving power of a microscope is increased by
   (a) using light of longer wavelength (b) reducing the numerical aperture (c) increasing only the tube length (d) immersing the objective and specimen in oil
11. With white light in Young's experiment only a few coloured fringes are seen because
   (a) white light is incoherent (b) the central fringe absorbs the colours (c) fringes of different wavelengths overlap and wash out (d) glass absorbs most colours
12. The source slit in Young's experiment is moved slightly upward. The fringe pattern on the screen
   (a) stays where it was (b) shifts downward (c) becomes wider (d) disappears
13. Red light replaces violet light in the same double-slit set-up. The fringes
   (a) become wider (b) become narrower (c) keep the same width (d) disappear
14. Interference and diffraction both come from superposition, but in diffraction the superposing waves come from
   (a) two independent sources (b) two images of one source (c) different parts of the same wavefront (d) two perpendicular polarizations

::: note Answers and explanations — Set B
**1.** (b) — $\beta = \lambda D/d$; doubling both D and d leaves the ratio unchanged.
**2.** (a) — a wide source is many independent point sources side by side, each giving its own pattern displaced sideways; the patterns overlap into uniform brightness.
**3.** (d) — the plate adds optical path to the upper beam, so equality is restored only when P moves up, towards the plate. The whole pattern, central fringe included, shifts that way.
**4.** (c) — amplitudes are 1 : 2, so $I_{max}/I_{min} = (1+2)^2/(1-2)^2 = 9$. Option (d) uses the intensities directly and is the classic error.
**5.** (a) — the half-width is $\lambda/a$, so a wider slit gives a narrower central maximum.
**6.** (c) — with hundreds of slits the maxima are very sharp (intensity $\propto N^2$), so they are narrower and much brighter.
**7.** (b) — the first sheet halves the light; each of the two 45° steps multiplies by $\cos^2 45^{\circ} = 1/2$: $(I_0/2)(1/2)(1/2) = I_0/8$.
**8.** (d) — at the polarizing angle the in-plane component is not reflected at all, so the reflected beam is completely plane-polarized.
**9.** (a) — resolving power is $D/(1.22\lambda)$, which rises with the diameter.
**10.** (d) — oil raises $\mu$ and hence the numerical aperture $\mu\sin\theta$, improving resolution. Longer wavelength and a smaller aperture both make it worse.
**11.** (c) — $\beta \propto \lambda$, so each colour has its own fringe spacing; after a few orders the bright fringes of one colour fall on the dark fringes of another and the pattern becomes white again.
**12.** (b) — the central fringe lies on the straight line joining the source to the midpoint of the slits; raising the source tilts that line downward at the screen.
**13.** (a) — $\beta \propto \lambda$ and red has the longer wavelength, so the fringes spread out.
**14.** (c) — diffraction uses many secondary wavelets from one wavefront; interference uses two (or a few) separate coherent sources.
:::

**Set C — Application (10 questions)**

1. Light of wavelength 600 nm falls on two slits 0.5 mm apart, with the screen 1 m away. The fringe width is
   (a) 0.6 mm (b) 2.4 mm (c) 1.2 mm (d) 0.3 mm
2. The same set-up is immersed in water of refractive index 4/3. The fringe width becomes
   (a) 0.9 mm (b) 1.6 mm (c) 0.45 mm (d) 1.2 mm
3. In a double-slit experiment the fringe width is 0.1 mm. A glass sheet 0.2 mm thick (μ = 1.5) covers one slit. The pattern shifts by
   (a) 0.5 fringe (b) 1 fringe (c) 2 fringes (d) 4 fringes
4. Two coherent sources give $I_{max}/I_{min} = 25/9$. The ratio of their intensities is
   (a) 25 : 9 (b) 5 : 3 (c) 9 : 4 (d) 16 : 1
5. Light of 600 nm passes through a slit 0.2 mm wide; the screen is 1 m away. The width of the central maximum is
   (a) 3 mm (b) 1.5 mm (c) 6 mm (d) 12 mm
6. A grating has 5000 lines per cm and is used with light of 500 nm. The highest order visible is
   (a) 4 (b) 5 (c) 10 (d) 2
7. A telescope has an objective 10 cm in diameter and works at 600 nm. The smallest resolvable angular separation is about
   (a) $7.3\times10^{-4}$ rad (b) $7.3\times10^{-6}$ rad (c) $1.2\times10^{-5}$ rad (d) $6.0\times10^{-7}$ rad
8. Unpolarized light of intensity $I_0$ passes through two Polaroids whose axes are at 60°. The emergent intensity is
   (a) $I_0/2$ (b) $I_0/4$ (c) $3I_0/8$ (d) $I_0/8$
9. Light is incident from air on a medium of refractive index $\sqrt{3}$. The polarizing angle is
   (a) 30° (b) 45° (c) 60° (d) 56°
10. A plano-convex lens of radius of curvature 1 m rests on a glass plate and is viewed in reflected light of 600 nm. The radius of the third dark ring is
   (a) 1.34 mm (b) 0.77 mm (c) 2.68 mm (d) 0.60 mm

::: note Answers and explanations — Set C
**1.** (c) — $\beta = \lambda D/d = (600\times10^{-9})(1)/(0.5\times10^{-3}) = 1.2\times10^{-3}$ m = 1.2 mm. Option (a) divides by 2 twice.
**2.** (a) — $\beta' = \beta/\mu = 1.2/(4/3) = 0.9$ mm. The frequency does not change, but the wavelength in water does.
**3.** (b) — extra optical path $= (\mu-1)t = 0.5\times0.2 = 0.1$ mm; dividing by $\beta = 0.1$ mm gives 1 fringe.
**4.** (d) — amplitude ratio $= (\sqrt{25/9}+1)/(\sqrt{25/9}-1) = (5/3+1)/(5/3-1) = 4$, so the intensity ratio is $4^2 = 16$. Option (a) is the given ratio, not the answer.
**5.** (c) — $2D\lambda/a = 2(1)(600\times10^{-9})/(0.2\times10^{-3}) = 6$ mm. Option (a) is only the half-width.
**6.** (a) — $d = 1/(5\times10^{5}) = 2\ \mu$m; $n_{max} = d/\lambda = 2\times10^{-6}/5\times10^{-7} = 4$.
**7.** (b) — $\theta_{min} = 1.22\lambda/D = 1.22(600\times10^{-9})/0.1 = 7.3\times10^{-6}$ rad. Option (a) has the decimal point one place out.
**8.** (d) — the first sheet halves the intensity, then Malus gives $(I_0/2)\cos^2 60^{\circ} = I_0/8$. Option (b) omits the $\cos^2$ and (c) uses $\sin^2$.
**9.** (c) — $\tan\theta_p = \sqrt{3}$ gives $\theta_p = 60^{\circ}$; the refracted ray is then at 30° and the two are perpendicular.
**10.** (a) — $r_3 = \sqrt{3\lambda R} = \sqrt{3(600\times10^{-9})(1)} = 1.34\times10^{-3}$ m. Option (b) is the first dark ring.
:::

**Group D — Model answers for long questions (10 marks each, for deeper revision)**

1. Describe Young's double-slit experiment and derive the fringe width. State the conditions for sustained interference. <span class="marks">[10]</span>
2. Explain single-slit diffraction, the diffraction grating, and polarisation with Brewster's and Malus' laws. <span class="marks">[10]</span>

```photogrid label="13.H" cols="3" ratio="1.25" caption="Wave optics in pictures. (a) Ripples from two sources interfere, leaving lines of constructive and destructive interference. (b) A diffraction grating splits light into spectra at angles given by d sin(theta) = n lambda. (c) Polarising sunglasses block horizontally polarised glare."
@ photo id="cee-phy/ripple-interference" cap="(a) Two-source interference"
fit 1.25
focus 0.5 0.5
@ photo id="phy12b/grating" cap="(b) Diffraction grating"
fit 1.25
focus 0.5 0.5
@ photo id="ceephy3/sunglasses" cap="(c) Polarising sunglasses"
fit 1.25
focus 0.5 0.5
```

### Model answer D1: Young's double-slit experiment (10 marks)

**Introduction.** **Interference** is the redistribution of energy when two coherent waves overlap. It supports the wave nature of light. Young obtained two coherent sources by dividing one wavefront with two narrow slits $S_1$ and $S_2$ separated by $d$, with the screen at a distance $D$.

**Derivation.** A point $P$ at a distance $y$ from the central point $O$ receives waves from both slits. The path difference is $\Delta = S_2P - S_1P \approx \dfrac{yd}{D}$ for $d, y \ll D$.

1. **Bright fringe:** $\Delta = n\lambda$, so $y_n = \dfrac{n\lambda D}{d}$, with $n = 0, 1, 2, \ldots$
2. **Dark fringe:** $\Delta = (n + \tfrac12)\lambda$, so $y_n = \dfrac{(n + \tfrac12)\lambda D}{d}$.
3. **Fringe width** (distance between consecutive bright or dark fringes): $\beta = \dfrac{\lambda D}{d}$.
4. **Intensity.** With equal slits, $I = 4I_0\cos^2\dfrac\phi2$, where $\phi = \dfrac{2\pi}{\lambda}\Delta$ is the phase difference. $I_{max} = 4I_0$, $I_{min} = 0$, and the average is $2I_0$, so energy is conserved.

**Conditions for sustained interference.** The two sources must be **coherent** (constant phase difference), of the same frequency, have nearly equal amplitudes for good contrast, and be close together. The slits must be narrow and the screen far away.

| Change | Effect on fringe width |
|---|---|
| Blue light instead of red | decreases ($\lambda$ smaller) |
| Slit separation doubled | halves |
| Screen moved farther | increases |
| Whole set-up in water | decreases by factor $n$ |
| Thin sheet of thickness $t$ over one slit | pattern shifts by $(n - 1)tD/d$, width unchanged |

White light gives a white central fringe with coloured edges on both sides.

**Numerical.** For $\lambda = 600\ \text{nm}$, $d = 0.5\ \text{mm}$ and $D = 1.5\ \text{m}$: $\beta = \dfrac{600\times10^{-9}\times1.5}{0.5\times10^{-3}} = 1.8\times10^{-3}\ \text{m} = 1.8\ \text{mm}$. The third bright fringe is at $3\times1.8 = 5.4\ \text{mm}$ and the second dark fringe at $1.5\times1.8 = 2.7\ \text{mm}$.

**Conclusion.** Fringe width $\beta = \lambda D/d$ is uniform, and the experiment gives a simple way to measure the wavelength of light.

### Model answer D2: diffraction, grating and polarisation (10 marks)

**Introduction.** **Diffraction** is the bending of waves around obstacles or through openings of size comparable to the wavelength.

**Single slit** (width $a$). The minima are at $a\sin\theta = n\lambda$ ($n = \pm1, \pm2, \ldots$), and the central maximum, twice as wide as the others, has width $\dfrac{2\lambda D}{a}$ on the screen. Narrower slits give a wider pattern. The secondary maxima are much weaker (about $4.5\%$ and $1.6\%$ of the central one).

**Diffraction grating.** A grating has many equally spaced slits with spacing $d = 1/N$ ($N$ lines per metre). The principal maxima obey $d\sin\theta = n\lambda$. The maxima are sharp, so the grating separates wavelengths far better than a prism. The maximum order is $n_{max} < d/\lambda$.

**Polarisation.** Light is a transverse wave, so it can be polarised. Longitudinal waves such as sound cannot be.

1. **Malus' law.** The intensity transmitted by an analyser at angle $\theta$ to the polariser is $I = I_0\cos^2\theta$. An unpolarised beam falls to half its intensity on passing a polariser.
2. **Brewster's law.** At the **polarising angle** $\theta_p$, the reflected light is completely plane-polarised and $\tan\theta_p = n$. The reflected and refracted rays are then at $90^{\circ}$.
3. **Uses.** Sunglasses, 3-D cinema, stress analysis in glass, and sugar solution analysis (optical activity).

| Feature | Interference | Diffraction |
|---|---|---|
| Sources | two coherent sources | single wavefront, many points |
| Fringes | equal width | unequal width |
| Intensity of minima | zero | not exactly zero |

**Numerical.**

- A slit of width $0.1\ \text{mm}$ with $\lambda = 500\ \text{nm}$ and $D = 1\ \text{m}$ gives a central maximum of width $\dfrac{2\times5\times10^{-7}\times1}{10^{-4}} = 1\ \text{cm}$.
- A grating with $5000$ lines per cm has $d = 2\times10^{-6}\ \text{m}$. For $500\ \text{nm}$, $\sin\theta_1 = 0.25$, $\theta_1 = 14.5^{\circ}$, and $d/\lambda = 4$, so the highest order is $3$ (the fourth falls at $90^{\circ}$). Total number of maxima $= 7$.
- For glass with $n = 1.5$, $\theta_p = \tan^{-1}1.5 = 56.3^{\circ}$. An unpolarised beam of intensity $100$ passes two polarisers at $60^{\circ}$ to each other: $100\times\tfrac12\times\cos^260^{\circ} = 12.5$.

**Conclusion.** Diffraction limits the resolution of instruments, the grating exploits it to analyse light, and polarisation proves that light is transverse.
