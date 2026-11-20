---
subject: Physics
grade: CEE
unit: 12
title: "Ray Optics: Reflection, Refraction and Dispersion"
hours: 3
area: Waves and Optics
---

Ray optics is the chapter of straight lines: rays, normals, angles and images. The
Waves and Optics area carries **8 of the 50 Physics questions** (official MEC
weightage), with about **3** questions from this chapter. Almost every
question is one of five calculations — a mirror or lens position, an apparent depth,
a critical angle, a prism deviation, or the power of a combination — and almost every
lost mark comes from a **sign**.

::: key What the paper asks from this chapter
- The Cartesian sign convention, once: distances from the pole or optical centre, positive along the incident light. Concave mirror $f<0$, convex mirror $f>0$; convex lens $f>0$, concave lens $f<0$; a real object has $u<0$.
- Mirror: $\frac{1}{v} + \frac{1}{u} = \frac{1}{f}$, $m = -\frac{v}{u}$, $R = 2f$.
- Lens: $\frac{1}{v} - \frac{1}{u} = \frac{1}{f}$, $m = \frac{v}{u}$.
- Refraction: $\mu = c/v$, $\mu_1\sin i = \mu_2\sin r$; apparent depth $=$ real depth $/\mu$; $\sin C = 1/\mu$; TIR needs dense $\to$ rare and $i > C$.
- Prism: $A = r_1 + r_2$, $\delta = i_1 + i_2 - A$, $\mu = \frac{\sin((A+\delta_m)/2)}{\sin(A/2)}$, thin prism $\delta = (\mu-1)A$.
- Lens maker: $\frac{1}{f} = (\mu-1)\left(\frac{1}{R_1} - \frac{1}{R_2}\right)$; power $P = 1/f$ in dioptre.
- Combinations: $P = P_1 + P_2$ **in contact only**; separated by $d$, $P = P_1 + P_2 - dP_1P_2$.
- Dispersion: $\mu$ falls as $\lambda$ rises, so violet deviates most; $\omega = \frac{\mu_v - \mu_r}{\mu_y - 1}$; achromatism needs $\frac{\omega_1}{f_1} + \frac{\omega_2}{f_2} = 0$.
:::

## 12.1 Reflection at curved mirrors: mirror formula and magnification

### The laws of reflection

1. The angle of incidence equals the angle of reflection: $i = r$.
2. The incident ray, the reflected ray and the normal at the point of incidence lie
   in the same plane.

Both angles are measured from the **normal**, not from the surface.

A **spherical mirror** is part of a hollow sphere. Its **pole** $P$ is the centre of
its surface, its **centre of curvature** $C$ the centre of that sphere, and its
**principal focus** $F$ the point where rays parallel to the principal axis converge
(concave) or appear to diverge from (convex) after reflection. The **radius of
curvature** is $R = 2f$, and the focal length is half the radius — a fact worth
memorising on its own.

| | Concave mirror | Convex mirror |
|---|---|---|
| Reflecting surface | inner (hollow) side | outer (bulging) side |
| Effect on parallel rays | converges them to $F$ | diverges them, as if from $F$ behind |
| Focal length | real focus, in front | virtual focus, behind |
| Images | real or virtual, depending on the object distance | always virtual, erect, diminished |
| Uses | shaving mirror, headlight reflector, dentist's mirror, solar cooker | rear-view mirror, security mirror, blind corners |

::: key The Cartesian sign convention — stated once, used throughout
Take the **pole (mirror) or optical centre (lens) as the origin**, and the principal
axis as the $x$-axis. Measure every distance **from the origin**, and take the
direction of the **incident light as positive**.

For a mirror the light travels towards the mirror, so the object side is negative:
$u<0$ for a real object, and a real image in front of the mirror also has $v<0$.
A concave mirror has its focus in front, so $f<0$; a convex mirror has its focus
behind, so $f>0$.

Heights are positive above the axis. A positive magnification means an erect image;
a negative magnification means an inverted one.
:::

### The mirror formula

$$ \frac{1}{v} + \frac{1}{u} = \frac{1}{f}, \qquad m = \frac{h'}{h} = -\frac{v}{u} $$

$u$ is the object distance, $v$ the image distance, $f$ the focal length, $h$ the
object height and $h'$ the image height. The formula holds for concave and convex
mirrors alike, for real and virtual objects and images, **provided the signs are put
in correctly**. It is accurate only for paraxial rays (a small aperture).

::: derivation The mirror formula
**Setting up.** An object $BQ$ stands on the axis, its foot $B$ at distance $u$ from
the pole and its tip $Q$ at height $h$. A ray from $Q$ parallel to the axis hits the
mirror at $M$ and reflects through $F$; a second ray from $Q$ through $F$ reflects
parallel to the axis. They meet at $Q'$, the image tip, at distance $v$ from the
pole with height $h'$ above the image foot $B'$. Take all lengths as magnitudes for
now.

**Step 1 — the ray through the focus.** The triangles $Q'B'F$ and $MPF$ are similar
($MP$ is the mirror height where the parallel ray strikes). The parallel ray keeps
its height, so $MP = h$, and
$$ \frac{h'}{h} = \frac{v - f}{f} $$

**Step 2 — the ray through the pole.** The triangles $Q'B'P$ and $QBP$ are similar,
because the ray through the pole is undeviated and the two verticals are parallel:
$$ \frac{h'}{h} = \frac{v}{u} $$

**Step 3 — equate the two expressions.**
$$ \frac{v}{u} = \frac{v-f}{f} \;\Rightarrow\; vf = uv - uf $$

**Step 4 — divide every term by $uvf$.**
$$ \frac{1}{u} = \frac{1}{f} - \frac{1}{v} \;\Rightarrow\; \frac{1}{v} + \frac{1}{u} = \frac{1}{f} $$

**Result.** $\dfrac{1}{v} + \dfrac{1}{u} = \dfrac{1}{f}$.

**What it means.** The magnitudes above were used only for a real image of a concave
mirror. Because every distance is measured from the pole with a sign, the same
equation covers virtual images, convex mirrors and virtual objects without change —
provided the signs go in. **Conditions:** paraxial rays only (small aperture), and a
thin mirror.
:::

::: tip Key writing criteria
The sign convention written down **before** substitution, the formula, the
substitution with signs, and the statement "real, inverted, magnified" — not just a
number. A bare answer of "30 cm" earns half the marks; "30 cm in front of the mirror,
real and inverted" earns all of them.
:::

### Where the image forms

For a concave mirror:

| Object position | Image position | Nature |
|---|---|---|
| at infinity | at $F$ | real, inverted, highly diminished (a point) |
| beyond $C$ | between $F$ and $C$ | real, inverted, diminished |
| at $C$ | at $C$ | real, inverted, same size ($m = -1$) |
| between $C$ and $F$ | beyond $C$ | real, inverted, magnified |
| at $F$ | at infinity | real, inverted, infinitely magnified |
| between $F$ and $P$ | behind the mirror | virtual, erect, magnified |

A convex mirror gives a virtual, erect, diminished image **between $P$ and $F$** for
every real object, which is exactly why it is used as a rear-view mirror: a wide
field of view in a small, upright image.

```figure caption="A concave mirror with $f = 4$ cm and an object 10 cm in front of it. The parallel ray reflects through $F$; the ray to the pole reflects at an equal angle. They meet 6.7 cm in front of the mirror, giving a real, inverted image with $m = -0.67$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.9))
R, f, u, h = 8.0, 4.0, 10.0, 2.0
v = 1/(1/f - 1/u)
hi = h*v/u
ax.axhline(0, color=MUTED, lw=0.7)
yy = np.linspace(-2.55, 2.55, 200)
ax.plot(R - np.sqrt(R**2 - yy**2), yy, color=INK, lw=1.8, zorder=3)
ax.annotate('', xy=(-u, h), xytext=(-u, 0),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.6, mutation_scale=10))
ax.annotate('', xy=(-v, -hi), xytext=(-v, 0),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.4,
                            mutation_scale=10, ls=(0,(3,2))))
xarc = R - np.sqrt(R**2 - h**2)
ax.plot([-u, xarc], [h, h], color=ACCENT, lw=1.1)
ax.plot([xarc, -7.7], [h, h + 0.5*(-7.7-xarc)], color=ACCENT, lw=1.1)
ax.plot([-u, 0], [h, 0], color=SERIES[2], lw=1.1)
ax.plot([0, -7.7], [0, 0.2*(-7.7)], color=SERIES[2], lw=1.1)
ax.plot([-4], [0], 'o', color=INK, ms=3.4, zorder=6)
ax.plot([-8], [0], 'o', color=INK, ms=3.4, zorder=6)
ax.plot([0], [0], 'o', color=INK, ms=3.4, zorder=6)
ax.text(-u-0.3, h+0.05, 'O', fontsize=9, ha='right', va='center')
ax.text(-6.30, -1.58, 'I', fontsize=9, color=SERIES[1], ha='left', va='center')
ax.text(-4, -0.26, 'F', fontsize=9, ha='center', va='top')
ax.text(-8, -0.26, 'C', fontsize=9, ha='center', va='top')
ax.text(0.40, -0.26, 'P', fontsize=9, ha='left', va='top')
ax.set_xlim(-12, 1.5); ax.set_ylim(-2.9, 2.9)
ax.axis('off')
```

::: example Worked example 12.1 — a concave mirror
**Problem.** An object is 15 cm in front of a concave mirror of focal length 10 cm.
Find the position, nature and magnification of the image.

**Solution.** Convention: $u = -15$ cm, $f = -10$ cm.
$\dfrac{1}{v} = \dfrac{1}{f} - \dfrac{1}{u} = -\dfrac{1}{10} + \dfrac{1}{15} =
\dfrac{-3+2}{30} = -\dfrac{1}{30}$, so $v = -30$ cm.
The image is 30 cm in front of the mirror — **real** (negative $v$), and
$m = -\dfrac{v}{u} = -\dfrac{-30}{-15} = -2$: inverted and twice the size.
:::

::: caution Four sign traps in mirrors
1. **Concave $f$ is negative** in this convention. Using $f = +10$ with $u = -15$
   gives $v = +6$ — a virtual image where a real one belongs.
2. A **positive $v$** means behind the mirror: the image is virtual and cannot be
   caught on a screen.
3. $m = -v/u$, not $v/u$. The minus sign is what tells you the image is inverted.
4. $R = 2f$, so a mirror of radius 40 cm has $f = 20$ cm, not 40.
:::

## 12.2 Refraction at plane surfaces, critical angle and TIR; refraction through a prism

### Refraction and Snell's law

**Refraction** is the change in direction of light when it crosses a boundary between
two transparent media, caused by a change in its **speed**. The frequency does not
change; the wavelength does.

$$ \mu = \frac{c}{v}, \qquad \mu_1\sin i = \mu_2\sin r $$

$\mu$ is the **absolute refractive index** of a medium (relative to vacuum), $c$ the
speed of light in vacuum and $v$ the speed in that medium. For two media,
$\dfrac{\sin i}{\sin r} = \dfrac{\mu_2}{\mu_1} = \dfrac{v_1}{v_2}$: light bends
**towards the normal** on entering a denser medium and **away** from it on leaving.

| Medium | $\mu$ | Speed of light (m s⁻¹) |
|---|---|---|
| vacuum / air | 1 (1.0003) | $3.0\times10^8$ |
| water | 1.33 | $2.25\times10^8$ |
| crown glass | 1.52 | $1.97\times10^8$ |
| diamond | 2.42 | $1.24\times10^8$ |

### Real and apparent depth

A pool looks shallower than it is, and a coin at the bottom of a glass of water looks
raised. The rule is simple:

$$ \text{apparent depth} = \frac{\text{real depth}}{\mu} $$

so the shift is $t\left(1 - \dfrac{1}{\mu}\right)$ for a layer of thickness $t$.

::: derivation Apparent depth
**Setting up.** An object $O$ lies a real depth $d$ below a plane surface; the
observer is in air above. Take a ray from $O$ that reaches the surface at a small
angle of incidence $i$ (measured in the liquid) and leaves at angle $r$ in air.

**Step 1 — Snell's law.** $\mu\sin i = 1\cdot\sin r$.

**Step 2 — small angles.** For a ray close to the normal, $\sin i \approx \tan i$
and $\sin r \approx \tan r$, so $\mu\tan i = \tan r$.

**Step 3 — geometry.** If the ray leaves the surface a horizontal distance $x$ from
the point above the object, then $\tan i = x/d$ and $\tan r = x/d'$, where $d'$ is
where the backward extension of the emergent ray meets the vertical.

**Step 4 — substitute.** $\mu\dfrac{x}{d} = \dfrac{x}{d'}$, so $d' = d/\mu$.

**Result.** The object appears at the **apparent depth** $d/\mu$, i.e. raised.

**Conditions.** Near-normal viewing, observer in the rarer medium, flat surface.
Viewing at a steep angle makes the bottom look curved and the simple rule fails.
:::

::: example Worked example 12.2 — how deep is the tank?
**Problem.** A water tank is 4.0 m deep ($\mu = 4/3$). How deep does it look from
directly above? How much does the bottom appear to be raised?

**Solution.** $d' = d/\mu = 4.0/(4/3) = 3.0$ m.
Shift $= 4.0 - 3.0 = 1.0$ m, which also follows from
$t(1 - 1/\mu) = 4(1 - 3/4) = 1$ m.
:::

**Through a slab.** A ray crossing a parallel-sided glass slab emerges **parallel to
its original direction** but displaced sideways by

$$ \text{lateral shift} = \frac{t\,\sin(i-r)}{\cos r} $$

The slab changes the path but not the direction — that is why a window pane does not
distort what you see through it.

### Critical angle and total internal reflection

When light travels from a **denser** to a **rarer** medium it bends away from the
normal, so the angle of refraction is larger than the angle of incidence. At a
particular angle of incidence the refracted ray grazes the surface ($r = 90^{\circ}$);
beyond it there is no refracted ray at all and the light is **totally internally
reflected**.

$$ \sin C = \frac{1}{\mu} \qquad (\text{denser} \to \text{air}) $$

| Medium | $\mu$ | Critical angle |
|---|---|---|
| water | 1.33 | 48.6° |
| crown glass | 1.52 | 41.1° |
| flint glass | 1.62 | 38.1° |
| diamond | 2.42 | 24.4° |

**Two conditions for TIR**, and both are needed:

1. light must be travelling from a denser to a rarer medium;
2. the angle of incidence must exceed the critical angle.

A larger $\mu$ means a **smaller** critical angle, which is why diamond sparkles: its
critical angle is only 24.4°, so most light entering it is totally reflected several
times before escaping.

```figure caption="Refraction from glass into air at three angles of incidence ($\mu = 1.5$, $C = 41.8^{\circ}$). Below the critical angle the ray refracts away from the normal; at the critical angle it grazes the surface; beyond it there is no refracted ray and the light is totally reflected."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 3, figsize=(5.0, 2.45))
mu = 1.5
Cc = np.degrees(np.arcsin(1/mu))
for ax, i_deg, ttl in zip(axes, [30, Cc, 60],
                          ['i = 30° < C', 'i = C = 41.8°', 'i = 60° > C']):
    i = np.radians(i_deg)
    ax.axhline(0, color=INK, lw=1.0)
    ax.plot([0,0], [-1.28, 1.10], color=MUTED, lw=0.8, ls=(0,(3,2)))
    ax.annotate('', xy=(0,0), xytext=(-1.02*np.sin(i), -1.02*np.cos(i)),
                arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.3, mutation_scale=8))
    s = mu*np.sin(i)
    if s < 0.999:
        r = np.arcsin(s)
        ax.annotate('', xy=(1.0*np.sin(r), 1.0*np.cos(r)), xytext=(0,0),
                    arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.3, mutation_scale=8))
        ax.text(0.74, 0.90, 'refracted', fontsize=7.8, color=SERIES[1],
                ha='center', va='bottom')
    elif s < 1.001:
        ax.annotate('', xy=(1.04,0), xytext=(0,0),
                    arrowprops=dict(arrowstyle='-|>', color=SERIES[3], lw=1.3, mutation_scale=8))
        ax.text(1.02, 0.16, 'grazes', fontsize=7.8, color=SERIES[3],
                ha='right', va='bottom')
    else:
        ax.annotate('', xy=(1.0*np.sin(i), -1.0*np.cos(i)), xytext=(0,0),
                    arrowprops=dict(arrowstyle='-|>', color=SERIES[2], lw=1.3, mutation_scale=8))
        ax.text(0.98, -0.78, 'reflected', fontsize=7.8, color=SERIES[2],
                ha='right', va='center')
    ax.set_title(ttl, fontsize=8.4, pad=5)
    ax.set_xlim(-1.14, 1.14); ax.set_ylim(-1.28, 1.10)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_aspect('equal'); ax.axis('off')
axes[0].text(-1.10, 0.07, 'air', fontsize=7.8, color=MUTED, ha='left', va='bottom')
axes[0].text(-1.10, -0.07, 'glass', fontsize=7.8, color=MUTED, ha='left', va='top')
fig.subplots_adjust(wspace=0.05)
```

### Where TIR is used

- **Optical fibres.** A core of high $\mu$ is surrounded by a cladding of slightly
  lower $\mu$; light entering at a small angle strikes the core–cladding boundary at
  an angle far above the critical angle and is totally reflected again and again,
  following the fibre around bends with almost no loss. This carries telephone,
  internet and TV signals, and lets an endoscope look inside the body.
- **Mirage.** On a hot road the air near the ground is hotter and less dense, so its
  $\mu$ is slightly lower than the cooler air above. Rays from the sky bend gradually
  and are totally reflected near the ground, so the road appears to be covered with
  water.
- **Prism periscope and binoculars.** A right-angled isosceles prism reflects light
  through 90° (or 180°) by TIR at its hypotenuse, where $i = 45^{\circ}$ exceeds the
  critical angle of glass. Prisms are used instead of mirrors because there is no
  silvering to tarnish and no double image from a front and a back surface.
- **Diamond sparkle**, and the **light pipe** used to carry light into a room.

### Refraction through a prism

A **prism** is a transparent body with two plane refracting faces meeting at the
**refracting angle** $A$ (the angle of the prism). A ray entering one face and
leaving the other is bent twice, both times towards the base, through a total
**angle of deviation** $\delta$.

$$ A = r_1 + r_2, \qquad \delta = i_1 + i_2 - A $$

where $i_1$ is the angle of incidence at the first face, $r_1$ the angle of
refraction there, $r_2$ the angle of incidence at the second face and $i_2$ the
angle of emergence.

::: derivation The prism relations
**Setting up.** The ray meets the first face at $Q$ and leaves the second face at
$R$. The normals at $Q$ and $R$ meet at $N$, and $A$ is the apex.

**Step 1 — the quadrilateral.** In quadrilateral $AQNR$ the angles at $Q$ and $R$ are
$90^{\circ}$ each, so $\angle QNR = 180^{\circ} - A$.

**Step 2 — the triangle $QNR$.** Its angles are $r_1$, $r_2$ and
$180^{\circ} - A$, and they add to $180^{\circ}$:
$$ r_1 + r_2 = A $$

**Step 3 — deviation at each face.** At the first face the ray is turned by
$i_1 - r_1$; at the second by $i_2 - r_2$. The two turns are in the same sense, so
$$ \delta = (i_1 - r_1) + (i_2 - r_2) = i_1 + i_2 - (r_1 + r_2) = i_1 + i_2 - A $$

**Result.** $A = r_1 + r_2$ and $\delta = i_1 + i_2 - A$.

**Conditions.** A triangular prism in air, with the ray crossing both faces (not
totally reflected at the second).
:::

### Minimum deviation

As the angle of incidence is increased from zero, $\delta$ first falls, reaches a
**minimum** $\delta_m$, then rises again. At the minimum the path is **symmetrical**:
the ray passes through the prism parallel to the base, and

$$ i_1 = i_2 = i, \qquad r_1 = r_2 = \frac{A}{2}, \qquad \delta_m = 2i - A $$

so $i = \dfrac{A + \delta_m}{2}$, and Snell's law at either face gives the prism
formula

$$ \mu = \frac{\sin\left(\dfrac{A+\delta_m}{2}\right)}{\sin\left(\dfrac{A}{2}\right)} $$

For a **thin prism** ($A$ a few degrees) the sines can be replaced by their angles,
and the result collapses to

$$ \delta = (\mu - 1)A $$

which is the form used for small-angle prisms in spectacles and rangefinders.

```figure caption="A ray through a $60^{\circ}$ prism of $\mu = 1.5$ at minimum deviation: the ray inside is parallel to the base, $r_1 = r_2 = 30^{\circ}$, $i_1 = i_2 = 48.6^{\circ}$ and $\delta = 37.2^{\circ}$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,3.1))
A = np.array([0.0, 0.90]); B = np.array([-0.52, 0.0]); C = np.array([0.52, 0.0])
ax.add_patch(plt.Polygon([A,B,C], closed=True, fill=True, fc='#eef2f8', ec=INK, lw=1.4))
P1 = np.array([-0.318, 0.35]); P2 = np.array([0.318, 0.35])
d_in = np.array([np.cos(np.radians(18.59)), np.sin(np.radians(18.59))])
d_out = np.array([np.cos(np.radians(-18.59)), np.sin(np.radians(-18.59))])
S = P1 - 0.55*d_in
E = P2 + 0.50*d_out
ax.annotate('', xy=P1, xytext=S, arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.6, mutation_scale=10))
ax.plot([P1[0],P2[0]], [P1[1],P2[1]], color=ACCENT, lw=1.6)
ax.annotate('', xy=E, xytext=P2, arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.6, mutation_scale=10))
V = np.array([0.0, 0.457])
ax.plot([P1[0],V[0]],[P1[1],V[1]], color=MUTED, lw=0.8, ls=(0,(3,2)))
ax.plot([P2[0],V[0]],[P2[1],V[1]], color=MUTED, lw=0.8, ls=(0,(3,2)))
n1 = np.array([-0.866, 0.5]); n2 = np.array([0.866, 0.5])
ax.plot([P1[0]-0.26*n1[0], P1[0]+0.26*n1[0]], [P1[1]-0.26*n1[1], P1[1]+0.26*n1[1]], color=MUTED, lw=0.8, ls=(0,(2,2)))
ax.plot([P2[0]-0.26*n2[0], P2[0]+0.26*n2[0]], [P2[1]-0.26*n2[1], P2[1]+0.26*n2[1]], color=MUTED, lw=0.8, ls=(0,(2,2)))
th = np.linspace(np.radians(-18.59), np.radians(18.59), 40)
ax.plot(V[0]+0.15*np.cos(th), V[1]+0.15*np.sin(th), color=INK, lw=0.9)
ax.plot([V[0], V[0]+0.30*np.cos(np.radians(18.59))],
        [V[1], V[1]+0.30*np.sin(np.radians(18.59))],
        color=MUTED, lw=0.8, ls=(0,(3,2)))
ax.text(0.195, 0.457, 'δ', fontsize=8.6, ha='left', va='center')
ta = np.linspace(np.radians(240), np.radians(300), 30)
ax.plot(0.12*np.cos(ta), 0.90+0.12*np.sin(ta), color=INK, lw=0.9)
ax.text(0.0, 0.735, 'A', fontsize=8.6, ha='center', va='center')
ax.text(-0.52, 0.58, 'i₁', fontsize=8.6, color=ACCENT, ha='center')
ax.text(-0.19, 0.25, 'r₁', fontsize=8.6, color=MUTED, ha='center')
ax.text(0.21, 0.25, 'r₂', fontsize=8.6, color=MUTED, ha='center')
ax.text(0.53, 0.52, 'i₂', fontsize=8.6, color=SERIES[1], ha='center')
ax.set_xlim(-0.95, 0.95); ax.set_ylim(-0.12, 1.02)
ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 12.3 — refractive index from a prism
**Problem.** A prism of angle 60° gives a minimum deviation of 30°. Find $\mu$.

**Solution.** $i = \dfrac{A+\delta_m}{2} = \dfrac{60+30}{2} = 45^{\circ}$ and
$r = A/2 = 30^{\circ}$, so
$\mu = \dfrac{\sin 45^{\circ}}{\sin 30^{\circ}} = \dfrac{0.707}{0.500} = 1.41$.
:::

::: caution Prism traps
1. $\delta = i_1 + i_2 - A$ is **not** $\delta_m$; it is the deviation for that
   particular ray. Only at minimum deviation is $i_1 = i_2$.
2. At minimum deviation $r = A/2$, not $A$. Using $r = 60^{\circ}$ in the formula
   gives nonsense.
3. The thin-prism result $\delta = (\mu-1)A$ is a **small-angle** approximation. It is
   good to about 1 % for $A$ below 10°, and $\delta$ comes out in whatever unit $A$
   is given in — degrees with degrees, radians with radians.
:::

## 12.3 Lenses: lens formula, lens maker's formula, power and combinations

A **lens** is a transparent medium bounded by two refracting surfaces. A **convex**
(biconvex) lens is thicker at the middle and converges parallel rays to a real focus;
a **concave** (biconcave) lens is thinner at the middle and diverges them, so its
focus is virtual.

| | Convex (converging) | Concave (diverging) |
|---|---|---|
| Shape | thicker at the centre | thinner at the centre |
| Effect on parallel rays | converges to a real focus | diverges, as if from a virtual focus |
| Focal length (convention) | positive | negative |
| Power | positive | negative |
| Images of a real object | real or virtual, depending on distance | always virtual, erect, diminished |

### The lens formula

With the **same Cartesian convention as §12.1** (distances from the optical centre,
positive along the incident light, real object $u<0$):

$$ \frac{1}{v} - \frac{1}{u} = \frac{1}{f}, \qquad m = \frac{h'}{h} = \frac{v}{u} $$

Note the difference from the mirror: a **minus** before $1/u$, and no minus in $m$.
For a convex lens with $u = -30$ cm and $f = 20$ cm,
$\frac{1}{v} = \frac{1}{20} - \frac{1}{30} = \frac{1}{60}$, so $v = +60$ cm — a real
image 60 cm beyond the lens, with $m = 60/(-30) = -2$: inverted and twice as large.

| Object position (convex lens) | Image position | Nature |
|---|---|---|
| at infinity | at $F$ | real, inverted, a point |
| beyond $2F$ | between $F$ and $2F$ | real, inverted, diminished |
| at $2F$ | at $2F$ | real, inverted, same size ($m = -1$) |
| between $F$ and $2F$ | beyond $2F$ | real, inverted, magnified |
| at $F$ | at infinity | real, inverted, infinitely magnified |
| between $F$ and the lens | same side | virtual, erect, magnified |

A concave lens gives a virtual, erect, diminished image between the lens and $F$ for
every real object.

### The lens maker's formula

The focal length of a thin lens is fixed by its material and its two surfaces:

$$ \frac{1}{f} = (\mu - 1)\left(\frac{1}{R_1} - \frac{1}{R_2}\right) $$

$R_1$ is the radius of the first surface (the one the light meets first) and $R_2$
the second, each **positive if that surface bulges towards the incident light**. For
a biconvex lens $R_1 > 0$ and $R_2 < 0$, so both terms add; for a biconcave lens
$R_1 < 0$ and $R_2 > 0$, so $f$ comes out negative.

### Power

The **power** of a lens is the reciprocal of its focal length in metres:

$$ P = \frac{1}{f\ (\text{in metres})}, \qquad \text{unit: dioptre (D)} = \text{m}^{-1} $$

A converging lens has positive power, a diverging lens negative. $f = +25$ cm gives
$P = +4$ D; $f = -50$ cm gives $P = -2$ D. Opticians write a prescription in
dioptres because powers, unlike focal lengths, simply add.

### Combinations of lenses

**In contact.** For thin lenses touching each other, the powers add:

$$ P = P_1 + P_2 + P_3 + \cdots, \qquad \frac{1}{f} = \frac{1}{f_1} + \frac{1}{f_2} $$

so a $+5$ D and a $-2$ D lens in contact behave as a single $+3$ D lens of focal
length $100/3 = 33.3$ cm.

**Separated by a distance $d$.** The formula changes:

$$ P = P_1 + P_2 - dP_1P_2, \qquad \frac{1}{f} = \frac{1}{f_1} + \frac{1}{f_2} - \frac{d}{f_1f_2} $$

with $d$ in metres. The extra term appears because the second lens receives the
image of the first as its object, and the two lens equations combine to give
$-\dfrac{d}{f_1f_2}$. A $+5$ D and a $-5$ D lens in contact give $P = 0$ (no net
power), but separated by 20 cm they give $P = 0 - (0.2)(5)(-5) = +5$ D — a
converging combination. The separation term is not a detail; it is the whole answer.

**Magnification of a combination** is the product: $m = m_1\times m_2$.

```figure caption="Two convex lenses 40 cm apart ($f_1 = 10$ cm, $f_2 = 15$ cm) with the object 20 cm in front of the first. $L_1$ forms $I_1$ at 20 cm; $I_1$ acts as the object for $L_2$, which forms the final image $I_2$ at 100 cm with $m = +3$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.1,2.9))
ax.axhline(0, color=MUTED, lw=0.7)
for x0, lab in [(0.0, 'L₁   f₁ = 10 cm'), (40.0, 'L₂   f₂ = 15 cm')]:
    ax.plot([x0,x0], [-3.6,3.6], color=INK, lw=1.3)
    ax.text(x0, 3.80, lab, fontsize=8.4, ha='center', va='bottom')
ax.annotate('', xy=(-20,1), xytext=(-20,0),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.5, mutation_scale=9))
ax.annotate('', xy=(20,-1), xytext=(20,0),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[3], lw=1.2,
                            mutation_scale=9, ls=(0,(3,2))))
ax.annotate('', xy=(100,3), xytext=(100,0),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.5, mutation_scale=9))
ax.plot([-20,0,40,100], [1,1,-3,3], color=ACCENT, lw=1.0)
ax.plot([-20,0,40,100], [1,0,-2,3], color=SERIES[2], lw=1.0)
ax.text(-20.8, 0.95, 'O', fontsize=9, ha='right', va='center')
ax.text(21.6, -0.55, 'I₁', fontsize=9, color=SERIES[3], ha='left', va='center')
ax.text(101.2, 2.72, 'I₂', fontsize=9, color=SERIES[1], ha='left', va='center')
ax.set_xlim(-30, 112); ax.set_ylim(-4.2, 4.6)
ax.axis('off')
```

::: example Worked example 12.4 — two lenses in contact
**Problem.** A convex lens of power +5 D and a concave lens of power −2 D are placed
in contact. Find the power and focal length of the combination, and its nature.

**Solution.** $P = P_1 + P_2 = 5 + (-2) = +3$ D.
$f = 1/P = 1/3\ \text{m} = 33.3$ cm, positive, so the combination is **converging**.
The two lenses share the same axis and the same image position; only the powers add.
:::

::: example Worked example 12.5 — the same lenses, 20 cm apart
**Problem.** A convex lens of power $+5$ D and a concave lens of power $-5$ D are
mounted on one axis, 20 cm apart. Find the equivalent power and focal length, and
compare with the result when they touch.

**Solution.** In contact, $P = 5 + (-5) = 0$ and $f = \infty$: the pair behaves like
a plain glass plate.
Separated by $d = 0.20$ m,
$P = P_1 + P_2 - dP_1P_2 = 0 - (0.20)(5)(-5) = +5$ D, so
$f = 1/5 = 0.20$ m = 20 cm, converging.
Moving the lenses apart has turned a powerless pair into a $+5$ D combination — the
separation term is as large as either power.
:::

::: caution The three lens traps
1. **$P = P_1 + P_2$ holds only in contact.** Separated by $d$, the power is
   $P_1 + P_2 - dP_1P_2$. Two lenses of $+5$ D and $-5$ D are powerless in contact
   but $+5$ D when 20 cm apart.
2. **A converging lens in water is weaker.** The lens maker's formula uses
   $\mu_{\text{lens}}/\mu_{\text{medium}} - 1$, not $\mu - 1$. Glass ($\mu = 1.5$) in
   water ($\mu = 4/3$) has $1/f$ smaller by a factor
   $\dfrac{1.5/1.333 - 1}{1.5 - 1} = \dfrac{0.125}{0.5} = \frac{1}{4}$, so the focal
   length becomes **four times** longer. A lens of $\mu$ less than the liquid's would
   even change from converging to diverging.
3. **$m = v/u$, not $-v/u$**, for a lens. The mirror formula has the minus; the lens
   formula does not.
:::

## 12.4 Dispersion, chromatic aberration and achromatism

### Dispersion

**Dispersion** is the splitting of white light into its component colours by
refraction. It happens because the refractive index of a material is **not the same
for all wavelengths**: it is largest for violet and smallest for red.

```photo id="cee-phy/prism-dispersion" caption="White light dispersed into its spectrum. Red is deviated least and violet most, because the refractive index of glass rises as the wavelength falls." width="46"
call 0.24 0.12 0.32 0.30 "Red end: least deviated"
call 0.72 0.06 0.62 0.30 "Blue-violet end: most deviated"
```


$$ \mu_{\text{violet}} > \mu_{\text{yellow}} > \mu_{\text{red}} $$

Since $\delta = (\mu-1)A$ for a thin prism, violet is deviated most and red least, so
a prism spreads white light into a band — the spectrum, in the order **VIBGYOR**
(violet, indigo, blue, green, yellow, orange, red) from the most deviated end.

The physical reason is speed: in glass, violet travels more slowly than red, so it
bends more. In vacuum all colours travel at the same speed and there is no
dispersion.

```figure caption="Refractive index against wavelength for a typical crown glass. $\mu$ falls steeply as $\lambda$ rises, so violet light (short $\lambda$) is deviated more than red by the same prism."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9,2.8))
lam = np.linspace(400, 700, 300)
mu = 1.5048 + 4038.0/lam**2
ax.axvspan(400, 700, color=ACCENT, alpha=0.06, lw=0)
ax.plot(lam, mu, color=ACCENT, lw=1.9)
for L, name, c in [(486,'F (blue)',SERIES[1]), (589,'D (yellow)',SERIES[3]), (656,'C (red)',SERIES[2])]:
    m = 1.5048 + 4038.0/L**2
    ax.plot([L],[m],'o', color=c, ms=4.5, zorder=5)
    ax.annotate('%s\n%.4f' % (name, m), xy=(L, m), xytext=(L+8, m+0.0075),
                fontsize=7.6, color=c, va='bottom')
ax.set_xlim(395,705); ax.set_ylim(1.510, 1.536)
ax.set_xlabel('wavelength  λ  (nm)'); ax.set_ylabel('refractive index  μ')
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.5)
```

Two numbers describe the spreading:

| Quantity | Formula | Meaning |
|---|---|---|
| Angular dispersion | $\delta_v - \delta_r = (\mu_v - \mu_r)A$ | the angle between the violet and red rays after a thin prism |
| Dispersive power | $\omega = \dfrac{\mu_v - \mu_r}{\mu_y - 1}$ | how strongly the material spreads colours, independent of $A$ |

$\omega$ is a property of the **material** alone — about 0.017 for crown glass and
0.030 for flint glass. That is why flint glass is used for the dispersing prism of a
spectrometer and crown glass for the lenses.

### Chromatic aberration

A lens behaves like a stack of prisms, so it too disperses. Rays of different colours
come to focus at different points: **violet focuses nearest the lens** (it is bent
most) and **red farthest**. This defect is **chromatic aberration**.

- **Longitudinal (axial) aberration:** the images lie along the axis at different
  distances, so a white object has a coloured blur.
- **Lateral (transverse) aberration:** the images have different sizes, so the edges
  of a white object are fringed with colour even when the centre is sharp.

A mirror does **not** suffer from chromatic aberration: reflection does not depend on
wavelength. That is why large astronomical telescopes are reflectors.

### Achromatism

A combination of two lenses can cancel the dispersion while keeping some net power.
For two thin lenses **in contact**, the condition for an achromatic doublet is

$$ \frac{\omega_1}{f_1} + \frac{\omega_2}{f_2} = 0 \qquad\Rightarrow\qquad \frac{f_1}{f_2} = -\frac{\omega_1}{\omega_2} $$

The powers must have **opposite signs** — one converging, one diverging — and the
ratio of focal lengths must equal the inverse ratio of dispersive powers. Since flint
glass has about twice the dispersive power of crown glass, the flint element must
have about **twice** the focal length of the crown element, and therefore half its
power. The combination is achromatic but not free of spherical aberration, and its
net power is only about half that of the converging element alone.

::: example Worked example 12.6 — dispersive power
**Problem.** A glass has $\mu_v = 1.53$, $\mu_r = 1.51$ and $\mu_y = 1.52$. Find its
dispersive power and the angular dispersion of a 10° prism of this glass.

**Solution.** $\omega = \dfrac{1.53-1.51}{1.52-1} = \dfrac{0.02}{0.52} = 0.038$.
Angular dispersion $= (\mu_v - \mu_r)A = 0.02\times10^{\circ} = 0.2^{\circ}$.
:::

::: tip Reading an optics question
Write the convention first, then list the three knowns with signs, then choose the
formula. In a combination question ask at once: *in contact or separated?* In a
"which defect" question ask: *lens or mirror?* These two questions settle most of the
chapter.
:::

```photogrid label="12.1" cols="2" ratio="1.2" caption="A rainbow is refraction plus one internal reflection. (a) Sunlight entering a raindrop is bent, reflected at the back and bent again, so the ray turns through D = 180 + 2i - 4r. (b) The elevation 4r - 2i of the emerging ray peaks at i with cos^2 i = (n^2 - 1) / 3: 59.5 degrees and 42.4 degrees for red (n = 1.331) and 58.8 degrees and 40.5 degrees for violet (n = 1.344). Rays pile up near these maxima, so red appears at 42.4 degrees and violet at 40.5 degrees from the anti-solar point, red outside, as in the photograph."
@ photo id="ceephy/rainbow" cap="A double rainbow over hills: raindrops refract, reflect once inside and refract again"
fit 1.2
focus 0.5 0.5
@ svg cap="Elevation of the primary bow against angle of incidence"
def eps(i, n): return 4 * math.asin(math.sin(i) / n) - 2 * i
def peak(n):
    i = math.acos(math.sqrt((n * n - 1) / 3)); return math.degrees(eps(i, n)), math.degrees(i)
er, ir = peak(1.331); ev, iv = peak(1.344)
brute = max(math.degrees(eps(math.radians(k / 100), 1.331)) for k in range(100, 8900))
assert 42.2 < er < 42.5 and 40.5 < ev < 40.8 and abs(brute - er) < 0.01
facts = dict(er="%.1f" % er, ir="%.1f" % ir, ev="%.1f" % ev, iv="%.1f" % iv)
f = Fig(300, 236)
f.text(150, 14, "elevation e = 4r - 2i against i", size=10.5, color=NAVY, bold=True)
X = lambda i: 40 + i * 2.6; Y = lambda e: 160 - e * 2.9
f.line(X(0), Y(0), 280, Y(0), color=SLATE, sw=1.4); f.line(X(0), Y(0), X(0), 34, color=SOFT, sw=1.2)
for n, col in ((1.331, RED), (1.344, "#6d28d9")):
    pts = [(X(k), Y(math.degrees(eps(math.radians(k), n)))) for k in range(0, 90, 2)]
    for (a, b), (c, d) in zip(pts, pts[1:]): f.line(a, b, c, d, color=col, sw=2.4)
f.line(X(ir), Y(0), X(ir), Y(er), color=AMBER, sw=1.2, dash=True)
f.text(X(ir) - 10, Y(er) + 50, "red %.1f" % er, size=10.5, color=RED, bold=True, anchor="end")
f.text(X(ir) - 10, Y(er) + 64, "violet %.1f" % ev, size=10.5, color="#6d28d9", bold=True, anchor="end")
for i in (0, 30, 60, 90): f.text(X(i), Y(0) + 13, "%d" % i, size=10.5, color=SLATE)
f.text(150, 192, "peak at i = %.1f (red), %.1f (violet)" % (ir, iv), size=10.5, color=NAVY, bold=True)
f.text(150, 210, "bow width %.1f degrees; red outside" % (er - ev), size=10.5, color=NAVY, bold=True)
f.text(150, 228, "angles in degrees; i = incidence", size=10.5, color=SLATE)
```

```photogrid label="12.2" cols="2" ratio="1.2" caption="Light trapped in glass. (a) An optical fibre cable carries many glass fibres, each thinner than a hair, that guide light by total internal reflection. (b) The cell computes the critical angle from sin c = n2 / n1: 41.8 degrees for glass in air, 48.8 for water, and 24.4 for diamond, whose small angle explains its sparkle. In a fibre, a core of index 1.48 is wrapped in a cladding of index 1.46, so the critical angle at their boundary is 80.6 degrees. The numerical aperture is 0.2425, which means only light entering within 14.0 degrees of the axis is guided. Such fibres carry internet traffic with tiny loss over many kilometres."
@ photo id="ceephy3/fibre" cap="An optical fibre cable"
fit 1.2
focus 0.5 0.5
@ svg cap="Total internal reflection and the optical fibre"
import math
def crit(n1, n2=1.0):
    return math.degrees(math.asin(n2 / n1))
rows = [("diamond", crit(2.42)), ("glass-air", crit(1.5)), ("water-air", crit(1.33)), ("fibre core", crit(1.48, 1.46))]
NA = math.sqrt(1.48 ** 2 - 1.46 ** 2)
acc = math.degrees(math.asin(NA))
assert round(rows[1][1], 1) == 41.8 and round(rows[3][1], 1) == 80.6 and round(acc, 1) == 14.0
f = Fig(300, 236)
f.text(150, 12, "Critical angle, degrees", size=10.5, color=NAVY, bold=True)
hbars(f, rows, vmax=90, fmt="%.1f", x0=76, y0=30, bw=170, gap=30,
      colors=[(ROSE, RED), (BLUE, NAVY), (MINT, TEAL), (SAND, AMBER)])
f.text(150, 158, "sin(c) = n2 / n1", size=10.5, color=NAVY, bold=True)
f.text(150, 178, "core 1.48, cladding 1.46: rays hitting at", size=10, color=SLATE, bold=True)
f.text(150, 194, "more than %.1f deg to the normal are trapped" % rows[3][1], size=10, color=SLATE, bold=True)
f.text(150, 214, "NA = %.4f, acceptance half-angle %.1f deg" % (NA, acc), size=10.5, color=NAVY, bold=True)
facts = dict(g=rows[1][1], w=rows[2][1], d=rows[0][1], c=rows[3][1], na=NA, acc=acc)
```

## Formula and fact sheet

| Topic | Formula or fact |
|---|---|
| Reflection | $i = r$; angles from the normal; $R = 2f$ |
| Mirror formula | $\frac{1}{v} + \frac{1}{u} = \frac{1}{f}$; $m = -\frac{v}{u}$ |
| Sign convention | origin at pole/optical centre; $+$ along the incident light; real object $u<0$; concave mirror $f<0$; convex mirror $f>0$ |
| Concave mirror images | beyond $C$: between $F$ and $C$, real inverted diminished; at $C$: at $C$, same size; between $C$ and $F$: beyond $C$, magnified; inside $F$: virtual erect magnified |
| Convex mirror | always virtual, erect, diminished, between $P$ and $F$ |
| Refractive index | $\mu = c/v$; $\mu_1\sin i = \mu_2\sin r$; $\frac{\sin i}{\sin r} = \frac{\mu_2}{\mu_1}$ |
| Apparent depth | $d' = d/\mu$; shift $= t(1 - 1/\mu)$ |
| Slab | emergent ray parallel; lateral shift $= t\sin(i-r)/\cos r$ |
| Critical angle | $\sin C = 1/\mu$; water 48.6°, crown glass 41.1°, diamond 24.4° |
| TIR | denser $\to$ rarer **and** $i > C$ |
| Prism | $A = r_1 + r_2$; $\delta = i_1 + i_2 - A$ |
| Minimum deviation | $r = A/2$, $i = (A+\delta_m)/2$, $\mu = \frac{\sin((A+\delta_m)/2)}{\sin(A/2)}$ |
| Thin prism | $\delta = (\mu-1)A$ |
| Lens formula | $\frac{1}{v} - \frac{1}{u} = \frac{1}{f}$; $m = \frac{v}{u}$ |
| Lens maker | $\frac{1}{f} = (\mu-1)\left(\frac{1}{R_1} - \frac{1}{R_2}\right)$ |
| Power | $P = 1/f$ (m); dioptre; convex $+$, concave $-$ |
| Lenses in contact | $P = P_1 + P_2$; $\frac{1}{f} = \frac{1}{f_1} + \frac{1}{f_2}$; $m = m_1m_2$ |
| Lenses separated | $P = P_1 + P_2 - dP_1P_2$ |
| Lens in water | $\frac{1}{f} = \left(\frac{\mu_l}{\mu_m}-1\right)\left(\frac{1}{R_1}-\frac{1}{R_2}\right)$; glass in water: $f$ becomes 4 times |
| Dispersion | $\mu$ falls as $\lambda$ rises; violet deviates most; VIBGYOR |
| Dispersive power | $\omega = \frac{\mu_v-\mu_r}{\mu_y-1}$; angular dispersion $= (\mu_v-\mu_r)A$ |
| Achromatism | $\frac{\omega_1}{f_1} + \frac{\omega_2}{f_2} = 0$; crown $+$ flint, opposite signs |
| Chromatic aberration | violet focus nearest the lens; mirrors are free of it |

## Chapter summary

- The Cartesian convention fixes everything: origin at the pole or optical centre,
  positive along the incident light; a real object has $u<0$, a concave mirror
  $f<0$, a convex lens $f>0$.
- Mirror: $\frac{1}{v}+\frac{1}{u}=\frac{1}{f}$ and $m=-\frac{v}{u}$; $R = 2f$; a
  convex mirror is always virtual, erect and diminished.
- Refraction: $\mu = c/v$ and $\mu_1\sin i = \mu_2\sin r$; frequency is unchanged at
  a boundary, wavelength and speed are not.
- Apparent depth $= d/\mu$; a slab shifts the ray sideways without changing its
  direction; $\sin C = 1/\mu$, and TIR needs dense-to-rare plus $i>C$.
- Prism: $A = r_1+r_2$ and $\delta = i_1+i_2-A$; at minimum deviation the ray is
  symmetrical and $\mu = \sin((A+\delta_m)/2)/\sin(A/2)$; a thin prism gives
  $\delta = (\mu-1)A$.
- Lens: $\frac{1}{v}-\frac{1}{u}=\frac{1}{f}$, $m=\frac{v}{u}$,
  $\frac{1}{f}=(\mu-1)(1/R_1-1/R_2)$, $P = 1/f$ in dioptres.
- In contact $P = P_1+P_2$; separated by $d$, $P = P_1+P_2-dP_1P_2$. A converging
  lens in water has a longer focal length — about four times longer for glass.
- Dispersion: $\mu$ falls as $\lambda$ rises, so violet bends most; $\omega$ measures
  the spread; a crown–flint doublet with $\omega_1/f_1+\omega_2/f_2=0$ is achromatic,
  and mirrors never show chromatic aberration.

## Practice questions

**Set A — Recall (28 questions)**

1. The mirror formula is
   (a) $\frac{1}{v} + \frac{1}{u} = \frac{1}{f}$ (b) $\frac{1}{v} - \frac{1}{u} = \frac{1}{f}$ (c) $\frac{1}{v} + \frac{1}{u} = \frac{1}{2f}$ (d) $v + u = f$
2. The magnification produced by a spherical mirror is
   (a) $v/u$ (b) $-u/v$ (c) $-v/u$ (d) $uv$
3. In the Cartesian sign convention, the focal length of a concave mirror is
   (a) positive (b) negative (c) zero (d) infinite
4. A convex mirror always forms an image that is
   (a) real and inverted (b) real and erect (c) virtual and magnified (d) virtual, erect and diminished
5. An object placed at the centre of curvature of a concave mirror forms its image at
   (a) the centre of curvature (b) the focus (c) infinity (d) the pole
6. An object placed at the focus of a concave mirror forms its image at
   (a) the centre of curvature (b) the pole (c) infinity (d) the focus
7. The refractive index of a medium is defined as
   (a) $v/c$ (b) $c/v$ (c) $cv$ (d) $c + v$
8. The critical angle $C$ for a medium of refractive index $\mu$ is given by
   (a) $\cos C = 1/\mu$ (b) $\tan C = 1/\mu$ (c) $\sin C = \mu$ (d) $\sin C = 1/\mu$
9. Total internal reflection occurs when light travels
   (a) from a denser to a rarer medium beyond the critical angle (b) from a rarer to a denser medium (c) normally across a boundary (d) exactly at the critical angle
10. The apparent depth of a tank of real depth $d$, viewed from above, is
   (a) $\mu d$ (b) $d/\mu^2$ (c) $d/\mu$ (d) $d(\mu - 1)$
11. For a prism, the angle of deviation is
   (a) $i_1 + i_2 + A$ (b) $i_1 + i_2 - A$ (c) $A - i_1 - i_2$ (d) $i_1 - i_2 + A$
12. At the angle of minimum deviation, the ray inside the prism is
   (a) along the base (b) perpendicular to the base (c) along the normal (d) parallel to the base
13. The relation between the angles of a prism is
   (a) $A = r_1 + r_2$ (b) $A = r_1 - r_2$ (c) $A = i_1 + i_2$ (d) $A = \delta + r_1$
14. For a thin prism of angle $A$ and refractive index $\mu$, the deviation is
   (a) $(\mu + 1)A$ (b) $\mu A$ (c) $(\mu - 1)A$ (d) $A/\mu$
15. The power of a lens is
   (a) $f$ (b) $1/f$ (c) $f^2$ (d) $1/f^2$
16. The SI unit of the power of a lens is the
   (a) metre (b) watt (c) joule (d) dioptre
17. The lens maker's formula is
   (a) $\frac{1}{f} = (\mu - 1)\left(\frac{1}{R_1} - \frac{1}{R_2}\right)$ (b) $\frac{1}{f} = (\mu + 1)\left(\frac{1}{R_1} + \frac{1}{R_2}\right)$ (c) $\frac{1}{f} = (\mu - 1)\left(\frac{1}{R_1} + \frac{1}{R_2}\right)$ (d) $f = (\mu - 1)(R_1 - R_2)$
18. The power of two thin lenses in contact is
   (a) $P_1 - P_2$ (b) $P_1P_2$ (c) $P_1 + P_2$ (d) $(P_1 + P_2)/2$
19. Dispersion of light by a prism occurs because
   (a) the prism is triangular (b) the refractive index depends on wavelength (c) all colours travel at the same speed in vacuum (d) light travels in straight lines
20. In the spectrum from a glass prism, the colour deviated most is
   (a) red (b) yellow (c) green (d) violet
21. Chromatic aberration is a defect of
   (a) lenses (b) plane mirrors (c) spherical mirrors (d) vacuum
22. Achromatism is the removal of
   (a) spherical aberration (b) coma (c) chromatic aberration (d) astigmatism
23. The dispersive power of a material is
   (a) $(\mu_v - \mu_r)/\mu_y$ (b) $(\mu_v - \mu_r)/(\mu_y - 1)$ (c) $(\mu_y - 1)/(\mu_v - \mu_r)$ (d) $(\mu_v + \mu_r)/(\mu_y - 1)$
24. The image formed by a plane mirror is
   (a) real and inverted (b) real and erect (c) virtual and diminished (d) virtual, erect and the same size
25. The refractive index of water is 4/3. The speed of light in water is
   (a) $4.0\times10^8$ m s⁻¹ (b) $3.0\times10^8$ m s⁻¹ (c) $2.25\times10^8$ m s⁻¹ (d) $1.33\times10^8$ m s⁻¹
26. A prism periscope works on the principle of
   (a) total internal reflection (b) dispersion (c) diffraction (d) refraction at a plane surface
27. The focal length of a plane mirror is
   (a) zero (b) infinite (c) equal to its radius (d) half its radius
28. For a convex lens the focal length is taken as
   (a) negative (b) zero (c) infinite (d) positive

::: note Answers and explanations — Set A
**1.** (a) — $\frac{1}{v}+\frac{1}{u}=\frac{1}{f}$ for every spherical mirror. Option (b) is the lens formula, where the sign before $1/u$ differs.
**2.** (c) — $m = h'/h = -v/u$. The minus sign is what marks an inverted image; dropping it is the commonest error in the chapter.
**3.** (b) — a concave mirror has its focus in front of it, on the side from which the light comes, which is the negative direction in the convention.
**4.** (d) — the reflected rays always diverge, so the image is virtual, erect and smaller than the object, lying between the pole and the focus.
**5.** (a) — $u = -2f$ gives $v = -2f$: the image is at $C$, real, inverted and the same size.
**6.** (c) — $u = -f$ gives $1/v = 0$, so $v = \infty$: the reflected rays are parallel.
**7.** (b) — $\mu = c/v$, the ratio of the speed in vacuum to the speed in the medium. It is always at least 1.
**8.** (d) — at the critical angle the refracted ray grazes the surface, so $r = 90^{\circ}$ and $\mu\sin C = 1\cdot\sin 90^{\circ} = 1$.
**9.** (a) — both conditions are needed: denser to rarer, and beyond $C$. At exactly $C$ the ray grazes the surface rather than being reflected.
**10.** (c) — the object appears raised to $d/\mu$. Option (a) would make the tank look deeper, which never happens.
**11.** (b) — the ray is turned by $(i_1-r_1)$ and again by $(i_2-r_2)$, and $r_1+r_2 = A$, giving $\delta = i_1+i_2-A$.
**12.** (d) — the symmetrical path at minimum deviation passes parallel to the base of the prism.
**13.** (a) — in the quadrilateral formed by the two normals and the two faces, $\angle QNR = 180^{\circ}-A$, and the triangle $QNR$ gives $r_1+r_2 = A$.
**14.** (c) — for small angles $\delta = (\mu-1)A$; the deviation grows with $\mu$ and with the prism angle.
**15.** (b) — power is the reciprocal of the focal length in metres, $P = 1/f$.
**16.** (d) — one dioptre is one reciprocal metre, $\text{D} = \text{m}^{-1}$.
**17.** (a) — $\frac{1}{f} = (\mu-1)\left(\frac{1}{R_1}-\frac{1}{R_2}\right)$, with $R_2$ negative for a biconvex lens so that the two terms add.
**18.** (c) — powers add for thin lenses in contact. They do not multiply and they do not subtract.
**19.** (b) — $\mu$ varies with $\lambda$, so each colour leaves the prism at a slightly different angle. In vacuum all colours travel at the same speed.
**20.** (d) — violet has the shortest wavelength and the largest refractive index, so it is deviated most.
**21.** (a) — refraction depends on wavelength, so lenses disperse; mirrors reflect all wavelengths equally.
**22.** (c) — an achromatic doublet brings two colours to the same focus, removing chromatic aberration.
**23.** (b) — $\omega = (\mu_v-\mu_r)/(\mu_y-1)$, a pure number characteristic of the material.
**24.** (d) — a plane mirror gives a virtual, erect image of the same size, as far behind the mirror as the object is in front.
**25.** (c) — $v = c/\mu = 3.0\times10^8/(4/3) = 2.25\times10^8$ m s⁻¹.
**26.** (a) — light strikes the hypotenuse at 45°, which exceeds the critical angle of glass (about 42°), so it is totally reflected through 90°.
**27.** (b) — a plane mirror has infinite radius, so $f = R/2$ is infinite: parallel rays come back parallel.
**28.** (d) — a convex lens converges light to a real focus on the far side, the positive direction.
:::

**Set B — Understanding (17 questions)**

1. A concave mirror is used as a shaving mirror because, with the face inside the focus, it gives
   (a) a real inverted image (b) a virtual diminished image (c) a virtual erect magnified image (d) a real erect image
2. A convex mirror is used as a rear-view mirror because it
   (a) gives an erect diminished image with a wide field of view (b) gives a magnified image (c) forms a real image on a screen (d) has a very long focal length
3. A fish looking up through a still water surface sees the whole sky within a cone of semi-vertical angle
   (a) 90° (b) 41.8° (c) 60° (d) 48.6°
4. A ray passes through a rectangular glass slab. The emergent ray is
   (a) deviated towards the base (b) parallel to the incident ray (c) perpendicular to the incident ray (d) totally reflected
5. A ray falls normally on one face of an equilateral prism of $\mu = 1.5$. At the second face it
   (a) emerges with a small deviation (b) passes straight through (c) is totally reflected (d) is absorbed
6. A converging lens is immersed in water. Its focal length
   (a) increases (b) decreases (c) stays the same (d) becomes zero
7. A lens of power $+5$ D and a lens of power $-5$ D are placed in contact. The combination behaves as
   (a) a convex lens of 10 D (b) a concave lens of 10 D (c) a plane mirror (d) a plane glass plate of zero power
8. The focal length of a lens is 25 cm. Its power is
   (a) $+25$ D (b) $+4$ D (c) $+0.25$ D (d) $-4$ D
9. Chromatic aberration in a telescope objective is reduced by using
   (a) an achromatic doublet (b) a longer tube (c) a larger aperture (d) a plane mirror
10. Violet light is deviated more than red by a glass prism because in glass
   (a) violet has a longer wavelength (b) red travels more slowly (c) violet travels more slowly (d) both travel at the same speed
11. An object is placed between the pole and the focus of a concave mirror. The image is
   (a) real, inverted and magnified (b) real, inverted and diminished (c) virtual, erect and diminished (d) virtual, erect and magnified
12. With a convex lens, an object at $2F$ gives an image that is
   (a) at $F$ and magnified (b) at $2F$, the same size and inverted (c) at infinity (d) virtual and erect
13. A converging lens forms a real image of the same size as the object when the object is at
   (a) $2f$ (b) $f$ (c) $f/2$ (d) infinity
14. The power of a lens is $-2.5$ D. Its focal length is
   (a) $+40$ cm (b) $-25$ cm (c) $-40$ cm (d) $+25$ cm
15. Lenses of power $+4$ D and $-6$ D are in contact. The focal length of the combination is
   (a) $+50$ cm (b) $-50$ cm (c) $+12.5$ cm (d) $-12.5$ cm
16. A glass slab of thickness $t$ and refractive index $\mu$ shifts an object seen through it by
   (a) $t\mu$ (b) $t/\mu$ (c) $t(\mu - 1)$ (d) $t(1 - 1/\mu)$
17. The splitting of white light into its colours by a prism is called
   (a) dispersion (b) deviation (c) diffraction (d) scattering

::: note Answers and explanations — Set B
**1.** (c) — inside the focus a concave mirror gives a virtual, erect, magnified image, so the face looks larger and the right way up.
**2.** (a) — a convex mirror always gives an erect, diminished image between $P$ and $F$, and its wide field of view shows more traffic.
**3.** (d) — the cone is bounded by rays at the critical angle, $C = \sin^{-1}(1/1.33) = 48.6^{\circ}$; beyond that the fish sees only the reflection of the water.
**4.** (b) — the two refractions at parallel faces are equal and opposite, so the ray emerges parallel to its original direction, only shifted sideways.
**5.** (c) — normal incidence gives $r_1 = 0$, so $r_2 = A = 60^{\circ}$, which exceeds the critical angle $41.8^{\circ}$; the ray is totally reflected inside the prism.
**6.** (a) — the lens maker's formula uses $\mu_{\text{lens}}/\mu_{\text{medium}}-1$, which is smaller in water, so $1/f$ falls and $f$ rises (four times for glass in water).
**7.** (d) — powers add: $+5-5 = 0$, so the combination has infinite focal length and acts like a plane parallel plate.
**8.** (b) — $P = 1/f = 1/0.25 = +4$ D. The power is positive because the lens is converging.
**9.** (a) — a doublet made of two glasses of different dispersive power brings two colours to a common focus.
**10.** (c) — smaller speed means larger refractive index, and a larger $\mu$ means a larger deviation.
**11.** (d) — inside the focus the reflected rays diverge; traced backwards they give a virtual, erect, magnified image behind the mirror.
**12.** (b) — $u = -2f$ gives $v = +2f$ on the other side, with $m = -1$: same size, inverted, real.
**13.** (a) — $m = v/u = -1$ needs $v = -u = 2f$, so the object must be at $2f$ and the image at $2f$ on the other side.
**14.** (c) — $f = 1/P = 1/(-2.5) = -0.40$ m = $-40$ cm: a diverging lens.
**15.** (b) — $P = 4-6 = -2$ D, so $f = 1/(-2) = -0.5$ m = $-50$ cm.
**16.** (d) — the apparent thickness is $t/\mu$, so the object appears raised by $t - t/\mu = t(1-1/\mu)$.
**17.** (a) — dispersion is the splitting by wavelength; deviation is the bending of the whole beam, and diffraction is the spreading by an obstacle.
:::

**Set C — Application (12 questions)**

1. An object is 15 cm in front of a concave mirror of focal length 10 cm. The image is formed at
   (a) 6 cm in front of the mirror (b) 30 cm in front of the mirror (c) 20 cm in front of the mirror (d) 45 cm in front of the mirror
2. An object is 10 cm in front of a concave mirror of focal length 15 cm. The image is
   (a) real, 6 cm from the mirror (b) real, 30 cm from the mirror (c) virtual, 6 cm from the mirror (d) virtual, 30 cm from the mirror
3. An object is 10 cm in front of a convex mirror of focal length 15 cm. The image is formed
   (a) 6 cm behind the mirror (b) 30 cm behind the mirror (c) 6 cm in front of the mirror (d) 15 cm behind the mirror
4. A water tank is 4 m deep ($\mu = 4/3$). The bottom appears to be at a depth of
   (a) 5.33 m (b) 4 m (c) 3 m (d) 1 m
5. The critical angle for a medium of refractive index 1.5 is about
   (a) 30° (b) 42° (c) 49° (d) 60°
6. A prism of angle 60° gives a minimum deviation of 30°. Its refractive index is
   (a) 1.50 (b) 1.73 (c) 1.33 (d) 1.41
7. A thin prism of angle 6° is made of glass of $\mu = 1.5$. Its deviation is
   (a) 3° (b) 6° (c) 9° (d) 1.5°
8. A convex lens of focal length 20 cm forms the image of an object 30 cm away at
   (a) 12 cm (b) 50 cm (c) 60 cm (d) 10 cm
9. A biconvex lens of $\mu = 1.5$ has radii of curvature 20 cm and 30 cm. Its focal length is
   (a) 12 cm (b) 30 cm (c) 10 cm (d) 24 cm
10. Lenses of power $+5$ D and $-2$ D are in contact. The power and focal length of the combination are
   (a) 7 D, 14.3 cm (b) 3 D, 33.3 cm (c) 3 D, 3.0 cm (d) $-3$ D, $-33.3$ cm
11. A convex lens of power $+5$ D and a concave lens of power $-5$ D are separated by 20 cm. The power of the combination is
   (a) zero (b) $-5$ D (c) $+5$ D (d) $+10$ D
12. A convex lens of focal length 20 cm in air ($\mu = 1.5$) is placed in water ($\mu = 4/3$). Its focal length becomes
   (a) 80 cm (b) 20 cm (c) 26.7 cm (d) 5 cm

::: note Answers and explanations — Set C
**1.** (b) — $u = -15$, $f = -10$: $\frac{1}{v} = -\frac{1}{10}+\frac{1}{15} = -\frac{1}{30}$, so $v = -30$ cm, i.e. 30 cm in front. Option (a) comes from dropping a sign.
**2.** (d) — $u = -10$, $f = -15$: $\frac{1}{v} = -\frac{1}{15}+\frac{1}{10} = +\frac{1}{30}$, so $v = +30$ cm. A positive $v$ is behind the mirror: virtual, and $m = +3$, erect and magnified.
**3.** (a) — $u = -10$, $f = +15$: $\frac{1}{v} = \frac{1}{15}+\frac{1}{10} = \frac{1}{6}$, so $v = +6$ cm behind the mirror, virtual and erect with $m = +0.6$.
**4.** (c) — $d' = d/\mu = 4/(4/3) = 3$ m. The bottom appears 1 m higher than it is.
**5.** (b) — $\sin C = 1/1.5 = 0.667$, so $C = 41.8^{\circ}$, about 42°.
**6.** (d) — $\mu = \frac{\sin 45^{\circ}}{\sin 30^{\circ}} = \frac{0.707}{0.500} = 1.41$. Option (b), $\sqrt{3} = 1.73$, would need a minimum deviation of 60°.
**7.** (a) — $\delta = (\mu-1)A = 0.5\times6^{\circ} = 3^{\circ}$.
**8.** (c) — $\frac{1}{v} = \frac{1}{20}-\frac{1}{30} = \frac{1}{60}$, so $v = +60$ cm; $m = 60/(-30) = -2$.
**9.** (d) — $\frac{1}{f} = 0.5\left(\frac{1}{20}+\frac{1}{30}\right) = 0.5\times\frac{5}{60} = \frac{1}{24}$, so $f = 24$ cm. Option (a) comes from forgetting the $(\mu-1)$ factor.
**10.** (b) — $P = 5-2 = +3$ D and $f = 1/3$ m = 33.3 cm. The powers add because the lenses touch.
**11.** (c) — in contact the power would be zero, but separated by $d = 0.2$ m, $P = 0 - (0.2)(5)(-5) = +5$ D. The separation term revives the power.
**12.** (a) — the factor $(\mu-1)$ becomes $(\mu/1.333 - 1) = 0.125$, one quarter of 0.5, so $1/f$ is quartered and $f$ is four times larger: 80 cm.
:::

**Group D — Model answers for long questions (10 marks each, for deeper revision)**

1. Explain refraction, total internal reflection and the optical fibre. Derive the prism formula and solve a numerical. <span class="marks">[10]</span>
2. Derive the lens formula and lens maker's formula, and explain dispersion with a numerical. <span class="marks">[10]</span>

```photogrid label="12.H" cols="3" ratio="1.25" caption="Light bending in practice. (a) A glass prism disperses white light into its spectrum. (b) An optical fibre carries light by repeated total internal reflection. (c) A rainbow forms by refraction, internal reflection and dispersion in raindrops."
@ photo id="cee-phy/prism-dispersion" cap="(a) Dispersion by a prism"
fit 1.25
focus 0.5 0.5
@ photo id="ceephy3/fibre" cap="(b) Optical fibre"
fit 1.25
focus 0.5 0.5
@ photo id="ceephy/rainbow" cap="(c) Rainbow"
fit 1.25
focus 0.5 0.5
```

### Model answer D1: refraction, total internal reflection and the prism (10 marks)

**Introduction.** **Refraction** is the bending of light at the boundary of two media because its speed changes. **Snell's law:** $\dfrac{\sin i}{\sin r} = {}_1n_2 = \dfrac{n_2}{n_1} = \dfrac{v_1}{v_2}$, where $n = c/v$ is the refractive index.

**Total internal reflection (TIR).** When light goes from a denser to a rarer medium, the angle of refraction exceeds the angle of incidence. At the **critical angle** $C$ the refracted ray grazes the surface, with $\sin C = \dfrac{n_2}{n_1} = \dfrac1n$ (rarer medium air). For $i > C$ all the light is reflected.

*Conditions:* (1) the light goes from a denser to a rarer medium; (2) the angle of incidence is greater than $C$.

**Applications of TIR.** Optical fibre (core $n_1$ greater than cladding $n_2$), endoscope, diamond sparkle, mirage, totally reflecting prisms in binoculars and periscopes, and the shine of an air bubble in water.

**Prism.** For a prism of angle $A$, the angle of deviation is $\delta = i + e - A$. The deviation is minimum when the ray passes symmetrically ($i = e$, $r_1 = r_2 = A/2$) and

$$ n = \frac{\sin\left(\dfrac{A + \delta_m}{2}\right)}{\sin\left(\dfrac A2\right)} $$

For a thin prism ($A$ small), $\delta = (n - 1)A$. The $i$-$\delta$ graph is a U-shaped curve with a minimum at $\delta_m$.

| Medium | $n$ | Critical angle (to air) |
|---|---|---|
| Water | 1.33 | $48.8^{\circ}$ |
| Crown glass | 1.5 | $41.8^{\circ}$ |
| Diamond | 2.42 | $24.4^{\circ}$ |

**Numerical.** For glass with $n = 1.5$: $\sin C = 1/1.5$ gives $C = 41.8^{\circ}$. For a $60^{\circ}$ prism of the same glass, $\sin\dfrac{A + \delta_m}{2} = 1.5\sin30^{\circ} = 0.75$, so $\dfrac{A + \delta_m}{2} = 48.6^{\circ}$ and $\delta_m = 37.2^{\circ}$.

**Conclusion.** TIR needs a denser-to-rarer path with $i > C$, and a prism gives its minimum deviation when the ray passes symmetrically.

### Model answer D2: lens formula, lens maker's formula and dispersion (10 marks)

**Introduction.** A lens refracts light at two spherical surfaces. For a thin lens we use the Cartesian sign convention, with distances measured from the optical centre and positive in the direction of the incident light.

**Lens formula.** $\dfrac1v - \dfrac1u = \dfrac1f$. The linear magnification is $m = \dfrac vu$. For a real image $m < 0$ (inverted).

**Lens maker's formula.** $\dfrac1f = (n - 1)\left(\dfrac1{R_1} - \dfrac1{R_2}\right)$, where $n$ is the refractive index of the lens relative to the medium. Immersing a glass lens in a liquid of higher index makes a convex lens behave as a concave one. The **power** is $P = 1/f$ in dioptre ($f$ in metres). For lenses in contact $P = P_1 + P_2$.

**Dispersion.** White light splits into seven colours because $n$ depends on wavelength (violet bends most, red least). The **dispersive power** is $\omega = \dfrac{n_v - n_r}{n_y - 1}$. A combination of two prisms of different glass can give dispersion without deviation (achromatic) or deviation without dispersion. A single lens has **chromatic aberration** (colour fringes), corrected by an achromatic doublet, with $\dfrac{\omega_1}{f_1} + \dfrac{\omega_2}{f_2} = 0$.

| Defect | Cause | Cure |
|---|---|---|
| Spherical aberration | marginal rays focus nearer | stop, parabolic mirror |
| Chromatic aberration | $n$ varies with colour | achromatic doublet |
| Myopia | image in front of retina | concave lens |
| Hypermetropia | image behind retina | convex lens |

**Numerical.** A convex lens has $f = 20\ \text{cm}$ and an object is placed $30\ \text{cm}$ away: $\dfrac1v = \dfrac1{20} - \dfrac1{30} = \dfrac1{60}$, so $v = 60\ \text{cm}$ and $m = 60/(-30) = -2$: real, inverted, twice as large. For a double-convex lens of glass $n = 1.5$ and $R_1 = 20\ \text{cm}$, $R_2 = -20\ \text{cm}$, $\dfrac1f = 0.5\times\dfrac2{20}$, so $f = 20\ \text{cm}$ and $P = +5\ \text{D}$.

**Conclusion.** The lens formula and lens maker's formula together link the image position to the shape and material of the lens, and dispersion arises because $n$ varies with colour.
