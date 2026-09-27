---
subject: Physics
grade: 12
unit: 10
title: Nature and propagation of light
hours: 3
area: Waves and Optics
---

Ray optics treats light as a straight line and gets mirrors and lenses right, but
it cannot say *why* light bends, or what happens when it meets an obstacle only a
few thousandths of a millimetre across. Wave optics can. This unit replaces the
ray by the **wavefront**, states Huygens' principle, and uses it to rebuild the
two laws you already know — reflection and refraction — from scratch. Everything
in the next three units (interference, diffraction, polarization) stands on the
geometry you learn here.

::: key What the examiner asks from this unit
Two things, almost every year: *state Huygens' principle and explain the
construction*, and *prove the laws of reflection or Snell's law using Huygens'
construction*. Both are pure marks if you can draw the diagram correctly, so
practise the diagram until you can produce it from memory in ninety seconds.
:::

## 10.1 Huygen's principle

A source of light sends energy out in all directions. At any instant, the points
that the disturbance has just reached all started vibrating at the same moment, so
they are all vibrating **in step**.

::: definition Wavefront
A **wavefront** is the locus of all points of a medium that are vibrating in the
same phase. The perpendicular drawn to a wavefront, in the direction in which the
wave advances, is a **ray**. The speed with which a wavefront advances is the
speed of the wave in that medium.
:::

Close to a point source the wavefronts are spheres; close to a long thin slit they
are cylinders. Very far from any source a small patch of the sphere is
indistinguishable from a flat plane, so sunlight reaching the Earth arrives as
**plane wavefronts**. A converging lens turns an incoming plane wavefront into a
spherical wavefront that shrinks onto the focus.

| Type of wavefront | Shape | Source | Amplitude falls as |
|---|---|---|---|
| Spherical | sphere | point source | $1/r$ |
| Cylindrical | cylinder | linear source (slit) | $1/\sqrt{r}$ |
| Plane | plane | very distant source | constant |

### Statement of the principle

Christiaan Huygens (1678) gave a rule for advancing a wavefront from one instant
to the next. It has two parts:

1. **Every point on a wavefront acts as a fresh source of secondary wavelets**,
   which spread out in all forward directions with the speed of the wave in that
   medium.
2. **The new wavefront**, after a time $t$, is the surface that touches all these
   secondary wavelets — their forward **envelope** or common tangent surface.

If the wave speed in the medium is $v$, every secondary wavelet drawn from the
old wavefront is a sphere of radius

$$ r = vt $$

So to advance a wavefront you take a compass, set it to $vt$, strike arcs from a
row of points on the old wavefront, and draw the tangent.

```figure caption="Huygens' construction. (a) A plane wavefront AB advances to the plane A'B'. (b) A spherical wavefront from S advances to a larger sphere. In each case the new wavefront is the forward envelope of secondary wavelets of radius $ct$."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(5.2, 2.7))

ax = axes[0]
r = 1.0
ax.plot([0, 0], [-1.5, 1.5], color=ACCENT, lw=2.2, zorder=4)
th = np.linspace(-np.pi/2, np.pi/2, 160)
for y0 in np.linspace(-1.2, 1.2, 5):
    ax.plot(r*np.cos(th), y0 + r*np.sin(th), color=MUTED, lw=0.8,
            ls=(0, (3, 2)), zorder=2)
    ax.plot([0], [y0], 'o', color=ACCENT, ms=3.4, zorder=5)
ax.plot([r, r], [-1.5, 1.5], color='#d9534f', lw=2.2, zorder=4)
ax.annotate('', xy=(r, 0.0), xytext=(0, 0.0),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.2, mutation_scale=9))
ax.annotate('$ct$', (0.5*r, 0), textcoords='offset points', xytext=(-7, 5), fontsize=9)
ax.annotate('A', (0, 1.5), textcoords='offset points', xytext=(-12, -2), color=ACCENT, fontsize=9)
ax.annotate('B', (0, -1.5), textcoords='offset points', xytext=(-12, -4), color=ACCENT, fontsize=9)
ax.annotate("A'", (r, 1.5), textcoords='offset points', xytext=(3, -2), color='#d9534f', fontsize=9)
ax.annotate("B'", (r, -1.5), textcoords='offset points', xytext=(3, -4), color='#d9534f', fontsize=9)
ax.set_title('(a) plane wavefront', fontsize=9)
ax.set_xlim(-0.55, 1.75); ax.set_ylim(-2.0, 2.0)
ax.set_aspect('equal'); ax.axis('off')

ax = axes[1]
R1, rw = 1.15, 0.72
a = np.radians(np.linspace(-54, 54, 240))
ax.plot(R1*np.cos(a), R1*np.sin(a), color=ACCENT, lw=2.2, zorder=4)
ax.plot((R1+rw)*np.cos(a), (R1+rw)*np.sin(a), color='#d9534f', lw=2.2, zorder=4)
for ang in np.radians([-45, -22.5, 0, 22.5, 45]):
    cx, cy = R1*np.cos(ang), R1*np.sin(ang)
    ax.plot([0, (R1+rw+0.25)*np.cos(ang)], [0, (R1+rw+0.25)*np.sin(ang)],
            color=GRID, lw=0.8, zorder=1)
    t2 = np.linspace(ang-1.25, ang+1.25, 120)
    ax.plot(cx+rw*np.cos(t2), cy+rw*np.sin(t2), color=MUTED, lw=0.8,
            ls=(0, (3, 2)), zorder=2)
    ax.plot([cx], [cy], 'o', color=ACCENT, ms=3.4, zorder=5)
ax.plot([0], [0], '*', color=INK, ms=10, zorder=6)
ax.annotate('S', (0, 0), textcoords='offset points', xytext=(-11, -4), fontsize=9)
ax.set_title('(b) spherical wavefront', fontsize=9)
ax.set_xlim(-0.45, 2.35); ax.set_ylim(-2.0, 2.0)
ax.set_aspect('equal'); ax.axis('off')
```

### Why there is no backward wave

Drawn honestly, the secondary wavelets are complete spheres, so they also have a
backward envelope — a wavefront travelling back towards the source. We never
observe one. Huygens simply asserted that the wavelets have zero intensity in the
backward direction. Fresnel and later Kirchhoff showed the amplitude of a
secondary wavelet actually varies with the angle $\theta$ measured from the
forward direction as the **obliquity factor**

$$ K = \tfrac{1}{2}(1+\cos\theta) $$

which equals $1$ straight ahead and $0$ straight backwards. That is why only the
forward envelope survives. For NEB purposes it is enough to say: *secondary
wavelets are effective only in the forward direction*.

::: caution Wavelets are not rays
A secondary wavelet is a tiny spherical wave, not a ray. Drawing straight arrows
from points on the wavefront instead of arcs earns no marks — the whole proof
depends on the arcs and on their common tangent.
:::

## 10.2 Reflection and Refraction according to wave theory

### Reflection at a plane surface

Let a plane wavefront AB travel through a medium in which light has speed $c$ and
strike a plane mirror. Take the moment when the end A has just touched the mirror
at A while the other end is still at B. Let the wavefront meet the mirror again at
C after a further time $t$.

```figure caption="Reflection of a plane wavefront. While B travels to C, the secondary wavelet from A grows to radius $ct$, and CD is the reflected wavefront. Since $BC = AD$, the angle of incidence equals the angle of reflection."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Arc
fig, ax = plt.subplots(figsize=(5.0, 2.9))
i = np.radians(50.0)
A = np.array([2.0, 0.0]); C = np.array([8.0, 0.0])
L = C[0] - A[0]; vt = L*np.sin(i)
u  = np.array([ np.sin(i), -np.cos(i)])
up = np.array([ np.sin(i),  np.cos(i)])
B = C - vt*u
D = A + vt*up
ax.plot([0.4, 9.7], [0, 0], color=INK, lw=2.0, zorder=3)
for x in np.arange(0.5, 9.7, 0.42):
    ax.plot([x, x-0.26], [0, -0.30], color=MUTED, lw=0.7, zorder=2)
t = np.radians(np.linspace(18, 64, 220))
ax.plot(A[0]+vt*np.cos(t), A[1]+vt*np.sin(t), color=MUTED, lw=0.9, ls=(0, (3, 2)))
ax.plot([A[0], B[0]], [A[1], B[1]], color=ACCENT, lw=2.4, zorder=4)
ax.plot([C[0], D[0]], [C[1], D[1]], color='#d9534f', lw=2.4, zorder=4)
def ray(p0, p1, c):
    ax.annotate('', xy=tuple(p1), xytext=tuple(p0),
                arrowprops=dict(arrowstyle='-|>', color=c, lw=1.1, mutation_scale=9))
ray(A-2.4*u, A, ACCENT); ray(B, C, ACCENT)
ray(A, D+1.5*up, '#d9534f'); ray(C, C+2.3*up, '#d9534f')
ax.plot([A[0], A[0]], [0, 3.2], color=MUTED, lw=0.8, ls=':')
ax.annotate('normal', (A[0], 3.2), textcoords='offset points', xytext=(-3, 3),
            ha='center', color=MUTED, fontsize=8.2)
ax.add_patch(Arc(A, 3.0, 3.0, theta1=0, theta2=50, color=INK, lw=0.9))
ax.add_patch(Arc(C, 3.0, 3.0, theta1=130, theta2=180, color=INK, lw=0.9))
ax.annotate('$i$', (A[0]+1.72, 0.58), fontsize=10)
ax.annotate('$r$', (C[0]-2.05, 0.58), fontsize=10)
def lead(pt, txt, xy, col):
    ax.annotate(txt, xy=tuple(pt), xytext=xy, color=col, fontsize=9, ha='center',
                arrowprops=dict(arrowstyle='-', color=col, lw=0.8))
lead(0.5*(B+C), '$BC = ct$', (10.1, 3.0), ACCENT)
lead(0.5*(A+D), '$AD = ct$', (0.1, 2.9), '#d9534f')
def rt(P, Q, R, s=0.30):
    e1 = (Q-P)/np.hypot(*(Q-P)); e2 = (R-P)/np.hypot(*(R-P))
    pts = np.array([P+s*e1, P+s*e1+s*e2, P+s*e2])
    ax.plot(pts[:, 0], pts[:, 1], color=INK, lw=0.8)
rt(B, A, C); rt(D, A, C)
for p, lab, off in [(A, 'A', (-4, -15)), (B, 'B', (-12, 3)), (C, 'C', (2, -15)),
                    (D, 'D', (5, 2))]:
    ax.plot([p[0]], [p[1]], 'o', color=INK, ms=3.6, zorder=6)
    ax.annotate(lab, tuple(p), textcoords='offset points', xytext=off, fontsize=9.5)
ax.annotate('incident wavefront AB', (-1.0, 4.55), color=ACCENT, fontsize=8.6, ha='left')
ax.annotate('reflected wavefront CD', (11.3, 4.55), color='#d9534f', fontsize=8.6, ha='right')
ax.set_xlim(-1.2, 11.5); ax.set_ylim(-1.0, 4.9)
ax.set_aspect('equal'); ax.axis('off')
```
While B travels the distance $BC$, every point of the mirror between A and C has
in turn started a secondary wavelet. The wavelet from A, which started earliest,
has had the full time $t$ to grow, so it is a hemisphere of radius $AD = ct$. The
wavelet from C has just started and has zero radius. The tangent drawn from C to
the wavelet centred on A is the **reflected wavefront** CD.

::: derivation The laws of reflection
In the right-angled triangles $ABC$ and $ADC$:

- $BC = ct$ is the distance travelled by B in the medium, and $AD = ct$ is the
  radius of the wavelet from A. Hence $BC = AD$.
- $AC$ is common, and angle $ABC$ = angle $ADC$ = $90^\circ$ (a wavefront is
  always perpendicular to its ray).

From triangle $ABC$: $\sin i = \dfrac{BC}{AC}$, and from triangle $ADC$:
$\sin r = \dfrac{AD}{AC}$.

$$ \frac{\sin i}{\sin r} = \frac{BC}{AD} = \frac{ct}{ct} = 1
\;\Longrightarrow\; i = r $$

That is the **second law of reflection**. Also, the incident wavefront, the
mirror and the reflected wavefront are all built on the same plane of the
diagram, so the incident ray, the reflected ray and the normal are coplanar —
the **first law**.
:::

### Refraction at a plane surface

Now let the same plane wavefront AB fall on the flat surface separating medium 1
(speed $v_1$) from a denser medium 2 (speed $v_2 < v_1$). Again A touches the
surface first, and B reaches C after time $t$, so $BC = v_1 t$. In that same time
the wavelet that started at A has spread **into medium 2** and has grown only to
radius $AD = v_2 t$, which is smaller. The tangent CD from C to this wavelet is
the refracted wavefront, and it is tilted towards the normal.

```figure caption="Refraction of a plane wavefront. In time $t$ the wavefront covers $BC = v_1t$ in the rarer medium while the wavelet from A grows to only $AD = v_2t$ in the denser medium, so the refracted wavefront CD bends towards the normal."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Arc, Rectangle
fig, ax = plt.subplots(figsize=(5.0, 3.35))
i = np.radians(50.0); n = 1.5
r = np.arcsin(np.sin(i)/n)
A = np.array([2.0, 0.0]); C = np.array([8.0, 0.0]); L = C[0]-A[0]
v1t = L*np.sin(i); v2t = L*np.sin(r)
u  = np.array([ np.sin(i), -np.cos(i)])
w  = np.array([ np.sin(r), -np.cos(r)])
B = C - v1t*u
D = A + v2t*w
ax.add_patch(Rectangle((0.2, -3.6), 10.2, 3.6, color=ACCENT, alpha=0.07, lw=0))
ax.plot([0.3, 10.3], [0, 0], color=INK, lw=1.6, zorder=3)
t = np.radians(np.linspace(238, 338, 220))
ax.plot(A[0]+v2t*np.cos(t), A[1]+v2t*np.sin(t), color=MUTED, lw=0.9, ls=(0, (3, 2)))
ax.plot([A[0], B[0]], [A[1], B[1]], color=ACCENT, lw=2.1, zorder=4)
ax.plot([C[0], D[0]], [C[1], D[1]], color='#d9534f', lw=2.1, zorder=4)
def ray(p0, p1, c):
    ax.annotate('', xy=tuple(p1), xytext=tuple(p0),
                arrowprops=dict(arrowstyle='-|>', color=c, lw=1.2, mutation_scale=9))
ray(A-2.4*u, A, ACCENT); ray(B, C, ACCENT)
ray(A, D, '#d9534f'); ray(D, D+1.3*w, '#d9534f')
ax.plot([A[0], A[0]], [-3.3, 3.5], color=MUTED, lw=0.8, ls=':')
ax.add_patch(Arc(A, 3.0, 3.0, theta1=0, theta2=50, color=INK, lw=0.9))
ax.add_patch(Arc(C, 3.2, 3.2, theta1=180, theta2=180+np.degrees(r), color=INK, lw=0.9))
ax.annotate('$i$', (A[0]+1.75, 0.58), fontsize=10)
ax.annotate('$r$', (C[0]-1.95, -0.72), fontsize=10)
for p, lab, off in [(A, 'A', (2, 7)), (B, 'B', (-13, 2)), (C, 'C', (4, 5)),
                    (D, 'D', (-14, -5))]:
    ax.plot([p[0]], [p[1]], 'o', color=INK, ms=3.6, zorder=6)
    ax.annotate(lab, tuple(p), textcoords='offset points', xytext=off, fontsize=9.5)
ax.annotate('$v_1t$', (0.5*(B[0]+C[0]), 0.5*(B[1]+C[1])), textcoords='offset points',
            xytext=(7, 4), color=ACCENT, fontsize=9)
ax.annotate('$v_2t$', (0.5*(A[0]+D[0]), 0.5*(A[1]+D[1])), textcoords='offset points',
            xytext=(-6, -14), color='#d9534f', fontsize=9)
def rt(P, Q, R, s=0.30):
    e1 = (Q-P)/np.hypot(*(Q-P)); e2 = (R-P)/np.hypot(*(R-P))
    pts = np.array([P+s*e1, P+s*e1+s*e2, P+s*e2])
    ax.plot(pts[:, 0], pts[:, 1], color=INK, lw=0.8)
rt(B, A, C); rt(D, A, C)
ax.annotate('medium 1  (speed $v_1$)', (10.3, 3.0), ha='right', fontsize=9, color=MUTED)
ax.annotate('medium 2  (speed $v_2 < v_1$)', (10.3, -3.4), ha='right', fontsize=9, color=MUTED)
ax.set_xlim(0.1, 10.7); ax.set_ylim(-4.1, 3.9)
ax.set_aspect('equal'); ax.axis('off')
```

::: derivation Snell's law from Huygens' construction
From the right-angled triangle $ABC$, with the angle at A equal to $i$:

$$ \sin i = \frac{BC}{AC} = \frac{v_1 t}{AC} $$

From the right-angled triangle $ADC$, with the angle at C equal to $r$:

$$ \sin r = \frac{AD}{AC} = \frac{v_2 t}{AC} $$

Dividing, the common factors $AC$ and $t$ cancel:

$$ \frac{\sin i}{\sin r} = \frac{v_1}{v_2} = {}_1n_2 $$

The right-hand side depends only on the two media, not on $i$. So the ratio
$\sin i/\sin r$ is a constant — **Snell's law**.

Writing the absolute refractive index of a medium as $n = c/v$, we get
$v_1 = c/n_1$ and $v_2 = c/n_2$, so

$$ \frac{\sin i}{\sin r} = \frac{n_2}{n_1}
\;\Longrightarrow\; n_1\sin i = n_2\sin r $$
:::

### Frequency, wavelength and optical path

The secondary wavelets in medium 2 are started by the vibrations arriving from
medium 1, so they must vibrate at the same rate. **Frequency does not change on
refraction** — it is fixed by the source. Since $v = f\lambda$ and $v$ falls,

$$ \frac{\lambda_1}{\lambda_2} = \frac{v_1}{v_2} = \frac{n_2}{n_1},
\qquad \lambda_{\text{medium}} = \frac{\lambda_{\text{vacuum}}}{n} $$

Light slows down and its wavelength shrinks, but its colour (frequency) is
unchanged. A path of geometrical length $x$ inside a medium of index $n$ holds the
same number of waves as a length $nx$ in vacuum, so we define the **optical path**

$$ \Delta_{\text{opt}} = n\,x $$

This single idea is used constantly in the next two units: whenever light passes
through glass or water, replace the real distance by the optical path.

| Prediction | Newton's corpuscular theory | Huygens' wave theory |
|---|---|---|
| Nature of light | stream of tiny particles | disturbance spreading as wavefronts |
| Speed in water compared with air | **greater** | **smaller** |
| Reflection | explained | explained |
| Refraction | explained, wrong speed | explained, correct speed |
| Interference, diffraction, polarization | not explained | explained |
| Experimental verdict | disproved by Foucault (1850) | confirmed |

Foucault's rotating-mirror measurement in 1850 showed that light travels more
slowly in water than in air. That single result killed the corpuscular theory and
established the wave picture used in Units 11–13.

::: example Worked example 10.1
**Problem.** Light strikes a glass block of refractive index $1.5$ at an angle of
incidence of $60^\circ$. Take $c = 3\times10^{8}\ \text{m s}^{-1}$ and a vacuum
wavelength of $600\ \text{nm}$. Find (a) the angle of refraction, (b) the speed of
light in the glass, (c) the wavelength in the glass.

**Solution.**

(a) $\sin r = \dfrac{\sin 60^\circ}{1.5} = \dfrac{0.8660}{1.5} = 0.5774$, so
$r = 35.3^\circ$.

(b) $v = \dfrac{c}{n} = \dfrac{3\times10^{8}}{1.5} = 2.0\times10^{8}\ \text{m s}^{-1}$.

(c) $\lambda_g = \dfrac{\lambda_0}{n} = \dfrac{600}{1.5} = 400\ \text{nm}$.

The frequency stays at $f = c/\lambda_0 = 5.0\times10^{14}\ \text{Hz}$ in both media.
:::

::: example Worked example 10.2
**Problem.** A beam of frequency $5.0\times10^{14}\ \text{Hz}$ passes from air into
a liquid in which its wavelength is $375\ \text{nm}$. Find the refractive index of
the liquid and the speed of light in it.

**Solution.** Frequency is unchanged, so in the liquid

$$ v = f\lambda_m = (5.0\times10^{14})(375\times10^{-9}) = 1.875\times10^{8}\ \text{m s}^{-1} $$

$$ n = \frac{c}{v} = \frac{3\times10^{8}}{1.875\times10^{8}} = 1.6 $$

Check with wavelengths: $\lambda_0 = c/f = 600\ \text{nm}$, and
$\lambda_0/\lambda_m = 600/375 = 1.6$. The two routes agree.
:::

::: example Worked example 10.3
**Problem.** A glass plate of thickness $2.0\ \text{mm}$ and refractive index
$1.5$ is placed in a beam of light of vacuum wavelength $500\ \text{nm}$. Find
(a) the optical path through the plate, (b) the number of waves contained in the
plate, (c) the extra time the light takes compared with travelling the same
$2.0\ \text{mm}$ in vacuum.

**Solution.**

(a) $\Delta_{\text{opt}} = nx = 1.5 \times 2.0\times10^{-3} = 3.0\times10^{-3}\ \text{m}$.

(b) The number of waves is the optical path divided by the **vacuum** wavelength:

$$ N = \frac{nx}{\lambda_0} = \frac{3.0\times10^{-3}}{500\times10^{-9}} = 6000 $$

(c) Time in glass $= nx/c$, time in vacuum $= x/c$, so the delay is

$$ \Delta t = \frac{(n-1)x}{c} = \frac{0.5 \times 2.0\times10^{-3}}{3\times10^{8}}
 = 3.3\times10^{-12}\ \text{s} $$
:::

## Chapter summary

- A **wavefront** is the locus of points vibrating in the same phase; a **ray** is
  the normal to the wavefront. Wavefronts may be spherical, cylindrical or plane.
- **Huygens' principle**: every point of a wavefront is a source of secondary
  wavelets of radius $vt$; the new wavefront is their forward envelope. Backward
  wavelets are suppressed by the obliquity factor $K = \frac{1}{2}(1+\cos\theta)$.
- **Reflection**: $BC = AD = ct$ gives $\sin i/\sin r = 1$, so $i = r$, and the
  incident ray, reflected ray and normal are coplanar.
- **Refraction**: $BC = v_1t$, $AD = v_2t$ give
  $\dfrac{\sin i}{\sin r} = \dfrac{v_1}{v_2} = \dfrac{n_2}{n_1}$, i.e.
  $n_1\sin i = n_2\sin r$.
- On refraction the **frequency is unchanged**; the speed and wavelength both fall
  by the factor $n$: $v = c/n$ and $\lambda_m = \lambda_0/n$.
- **Optical path** $= n \times$ geometrical path; it is the vacuum distance holding
  the same number of waves.
- The wave theory predicts $v_{\text{water}} < v_{\text{air}}$, confirmed by
  Foucault in 1850; the corpuscular theory predicted the opposite and failed.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. A wavefront is a surface on which all points have the same <span class="marks">[1]</span>
   (a) amplitude (b) phase (c) wavelength (d) intensity
2. When light travels from air into glass, the quantity that does **not** change is <span class="marks">[1]</span>
   (a) speed (b) wavelength (c) frequency (d) direction
3. Secondary wavelets in Huygens' construction travel with <span class="marks">[1]</span>
   (a) the speed of the source (b) the speed of light in that medium
   (c) infinite speed (d) half the wave speed
4. According to the wave theory of light, the speed of light in water is <span class="marks">[1]</span>
   (a) greater than in air (b) less than in air (c) equal to that in air (d) zero
5. The optical path of a ray covering $4\ \text{cm}$ in a medium of index $1.5$ is <span class="marks">[1]</span>
   (a) 2.67 cm (b) 4 cm (c) 6 cm (d) 9 cm

::: note Answers to Group A
**1.** (b) — a wavefront is by definition a surface of constant phase.
**2.** (c) — frequency is set by the source and is not altered by the medium.
**3.** (b) — each wavelet expands at the wave speed $v = c/n$ of that medium.
**4.** (b) — the wave theory needs $v_2 < v_1$ to bend light towards the normal; Foucault confirmed it.
**5.** (c) — optical path $= nx = 1.5\times4 = 6\ \text{cm}$.
:::

**Group B — Short answer (5 marks each)**

1. Define a wavefront and state Huygens' principle. Using it, show how a plane
   wavefront and a spherical wavefront advance. <span class="marks">[5]</span>
2. Using Huygens' construction, prove the laws of reflection of light at a plane
   surface. <span class="marks">[5]</span>
3. Light of wavelength $600\ \text{nm}$ in vacuum enters a medium of refractive
   index $1.25$. Find its speed, frequency and wavelength in the medium. <span class="marks">[5]</span>
4. Explain why the frequency of light does not change on refraction while its
   wavelength does. Hence define optical path. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Outline: wavefront = locus of points in the same phase; each point emits
secondary wavelets of radius $vt$; new wavefront = forward envelope. A plane
wavefront gives a plane envelope, a spherical one a larger sphere (Figure 1).

**3.** $v = c/n = 3\times10^{8}/1.25 = 2.4\times10^{8}\ \text{m s}^{-1}$.
Frequency is unchanged: $f = c/\lambda_0 = 3\times10^{8}/600\times10^{-9}
= 5.0\times10^{14}\ \text{Hz}$.
Wavelength: $\lambda_m = v/f = 2.4\times10^{8}/5.0\times10^{14}
= 4.8\times10^{-7}\ \text{m} = 480\ \text{nm}$ (equivalently $600/1.25$).

**4.** Outline: the vibrations in medium 2 are driven by those arriving from
medium 1, so they repeat at the same rate — $f$ is fixed. Since $v = f\lambda$ and
$v$ falls to $c/n$, the wavelength falls to $\lambda_0/n$. Optical path
$= n \times$ geometrical path is the equivalent vacuum distance containing the same
number of waves.
:::

**Group C — Long answer (8 marks each)**

1. (a) State Huygens' principle and explain the meaning of a secondary wavelet. <span class="marks">[3]</span>
   (b) Using Huygens' construction, derive Snell's law of refraction and hence show
   that the refractive index of a medium equals $c/v$. <span class="marks">[5]</span>
2. A ray of light is incident at $45^\circ$ on a parallel-sided glass slab of
   refractive index $1.5$ and thickness $6.0\ \text{cm}$. Find (a) the angle of
   refraction, (b) the speed of light inside the slab, (c) the time taken to cross
   the slab, and (d) the lateral displacement of the emergent ray. <span class="marks">[8]</span>

::: note Answer to Group C question 2
(a) $\sin r = \sin 45^\circ/1.5 = 0.7071/1.5 = 0.4714$, so $r = 28.1^\circ$.

(b) $v = c/n = 3\times10^{8}/1.5 = 2.0\times10^{8}\ \text{m s}^{-1}$.

(c) Path length inside the slab $= t/\cos r = 6.0/0.8819 = 6.80\ \text{cm}$, so

$$ \text{time} = \frac{6.80\times10^{-2}}{2.0\times10^{8}} = 3.4\times10^{-10}\ \text{s} $$

(d) Lateral displacement

$$ d = \frac{t\,\sin(i-r)}{\cos r} = \frac{6.0 \times \sin 16.9^\circ}{0.8819}
 = \frac{6.0 \times 0.2902}{0.8819} = 1.97\ \text{cm} $$
:::
