---
subject: Physics
grade: 12
unit: 12
title: Diffraction
hours: 3
area: Waves and Optics
---

Stand inside a room in Bhaktapur with the shutters almost closed and the sunlight
squeezing through does not stop at a sharp edge — it fans out. Light **bends round
obstacles and spreads after passing through narrow openings**. This is
**diffraction**, and it is the direct consequence of Huygens' secondary wavelets
interfering with one another. It sets a hard limit on what any telescope or
microscope can see, and it is the working principle of the diffraction grating,
the most accurate instrument we have for measuring wavelength.

::: key The one inequality behind the whole unit
Diffraction is only noticeable when the width of the obstacle or aperture is
**comparable with the wavelength**. Sound ($\lambda \approx 1\ \text{m}$) bends
round a doorway easily; light ($\lambda \approx 5\times10^{-7}\ \text{m}$) needs a
slit a fraction of a millimetre wide before the spreading can be seen.
:::

## 12.1 Diffraction from a single slit

::: definition Diffraction
Diffraction is the bending of waves round the edges of an obstacle or aperture,
and the resulting redistribution of intensity, when the size of the obstacle or
aperture is comparable with the wavelength of the wave.
:::

Two classes are distinguished:

| | Fresnel diffraction | Fraunhofer diffraction |
|---|---|---|
| Source and screen | at finite distance from the slit | effectively at infinity |
| Incident wavefront | spherical or cylindrical | plane |
| Lenses needed | none | collimating lens and focusing lens |
| Mathematics | difficult | simple |

Everything in this unit is **Fraunhofer** diffraction: parallel light in, parallel
light out, brought to a focus by a converging lens.

### Condition for the minima

Let a plane wavefront of wavelength $\lambda$ fall normally on a slit AB of width
$a$. By Huygens' principle every point of the slit sends out secondary wavelets.
Consider those that leave at an angle $\theta$ to the original direction; the lens
brings them to a single point P on the screen. The wavelet from the bottom edge B
travels farther than the one from the top edge A by

$$ \Delta = a\sin\theta $$

```figure caption="Fraunhofer diffraction at a single slit of width $a$. All wavelets leaving at angle $\theta$ meet at one point of the screen. The path difference between the edges is $BN = a\sin\theta$; when this equals $\lambda$ the slit splits into two halves that cancel in pairs."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Arc
fig, ax = plt.subplots(figsize=(5.1, 3.2))
th = np.radians(20.0)
u = np.array([np.cos(th), np.sin(th)])
A = np.array([0.0,  1.5]); B = np.array([0.0, -1.5]); M = np.array([0.0, 0.0])
ax.add_patch(Rectangle((-0.12, 1.5), 0.24, 1.7, color=INK, lw=0))
ax.add_patch(Rectangle((-0.12, -3.2), 0.24, 1.7, color=INK, lw=0))
for y0 in np.linspace(-1.5, 1.5, 7):
    P0 = np.array([0.0, y0])
    ax.annotate('', xy=tuple(P0+4.3*u), xytext=tuple(P0),
                arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.0, mutation_scale=8))
for yin in np.linspace(-2.9, 2.9, 9):
    ax.annotate('', xy=(-0.22, yin), xytext=(-1.5, yin),
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.9, mutation_scale=7))
for xw in (-1.35, -0.95, -0.55):
    ax.plot([xw, xw], [-3.1, 3.1], color=GRID, lw=1.2)
N = B + np.dot(A-B, u)*u
ax.plot([A[0], N[0]], [A[1], N[1]], color=MUTED, lw=1.0, ls=(0, (3, 2)))
ax.plot([B[0], N[0]], [B[1], N[1]], color='#d9534f', lw=3.2, zorder=6)
e1 = (A-N)/np.hypot(*(A-N)); e2 = (B-N)/np.hypot(*(B-N))
sq = np.array([N+0.22*e1, N+0.22*e1+0.22*e2, N+0.22*e2])
ax.plot(sq[:, 0], sq[:, 1], color=INK, lw=0.8)
ax.plot([-0.35, 4.6], [0, 0], color=MUTED, lw=0.8, ls=':')
ax.add_patch(Arc((0, 0), 4.6, 4.6, theta1=0, theta2=20, color=INK, lw=0.9))
ax.annotate(r'$\theta$', (2.42, 0.22), fontsize=10)
ax.add_patch(Arc(tuple(A), 1.5, 1.5, theta1=-90, theta2=-70, color=INK, lw=0.9))
ax.annotate(r'$\theta$', (0.14, 0.72), fontsize=9)
for q, lab, off in [(A, 'A', (-12, 2)), (B, 'B', (-12, -10)), (N, 'N', (2, -13)),
                    (M, 'M', (9, -13))]:
    ax.plot([q[0]], [q[1]], 'o', color=INK, ms=4.0, zorder=7)
    ax.annotate(lab, tuple(q), textcoords='offset points', xytext=off, fontsize=9.5)
ax.annotate(r'$BN = a\sin\theta$', xy=tuple(0.5*(B+N)), xytext=(2.5, -2.55),
            ha='center', color='#d9534f', fontsize=9.2,
            arrowprops=dict(arrowstyle='-', color='#d9534f', lw=0.8))
ax.annotate('', xy=(-0.62, 1.5), xytext=(-0.62, -1.5),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=0.9, mutation_scale=7))
ax.annotate('$a$', (-0.62, 0), textcoords='offset points', xytext=(-11, -4), fontsize=9.5)
ax.annotate('plane\nwavefronts', (-1.6, 3.0), ha='center', fontsize=8.4, color=MUTED)
ax.annotate('to lens and screen', (4.95, 3.15), ha='right', fontsize=8.4, color=ACCENT)
ax.set_xlim(-2.3, 5.0); ax.set_ylim(-3.6, 3.6)
ax.set_aspect('equal'); ax.axis('off')
```

::: derivation Positions of the minima
Imagine the slit divided into **two halves**, AM and MB, each of width $a/2$.
Pair off a point in the top half with the point exactly $a/2$ below it in the
bottom half. The path difference for such a pair is $\frac{a}{2}\sin\theta$.

Every pair cancels if that equals half a wavelength:

$$ \frac{a}{2}\sin\theta = \frac{\lambda}{2} \;\Longrightarrow\; a\sin\theta = \lambda $$

Every wavelet from the top half is then cancelled by its partner from the bottom
half, and P is **dark**. Dividing the slit into four equal strips instead gives
$a\sin\theta = 2\lambda$, into six strips $a\sin\theta = 3\lambda$, and so on.
The general condition for a **minimum** is

$$ a\sin\theta = n\lambda, \qquad n = \pm 1, \pm 2, \pm 3, \dots $$

Note that $n = 0$ is excluded: at $\theta = 0$ every wavelet arrives in phase and
the centre is the brightest point of the pattern.
:::

The **secondary maxima** lie roughly halfway between the minima, at

$$ a\sin\theta \approx \left(n + \tfrac{1}{2}\right)\lambda $$

and they are very weak — the first is only about 4.7% of the central intensity,
the second about 1.7%. The full intensity distribution is

$$ I = I_0\left(\frac{\sin\beta}{\beta}\right)^{2}, \qquad
   \beta = \frac{\pi a\sin\theta}{\lambda} $$

```figure caption="Intensity in single-slit diffraction against $a\sin\theta/\lambda$. Minima fall at $\pm1, \pm2, \pm3\dots$; the central maximum is twice as wide as the others and carries most of the light."
import numpy as np, matplotlib.pyplot as plt
fig = plt.figure(figsize=(5.0, 3.2))
gs = fig.add_gridspec(2, 1, height_ratios=[3.1, 0.9], hspace=0.10)
ax = fig.add_subplot(gs[0]); ax2 = fig.add_subplot(gs[1])
x = np.linspace(-3.6, 3.6, 3000)
I = np.sinc(x)**2
ax.plot(x, I, color=ACCENT, lw=1.8)
ax.fill_between(x, 0, I, color=ACCENT, alpha=0.10)
for m in range(-3, 4):
    if m:
        ax.plot([m], [0], 'o', color='#d9534f', ms=3.4, zorder=5)
ax.annotate('', xy=(-1, 1.16), xytext=(1, 1.16),
            arrowprops=dict(arrowstyle='<|-|>', color='#d9534f', lw=1.0, mutation_scale=7))
ax.annotate('central maximum,  angular width $2\\lambda/a$', (0, 1.21),
            ha='center', color='#d9534f', fontsize=8.4)
ax.annotate('4.7%', (1.43, 0.0472), textcoords='offset points', xytext=(9, 6),
            fontsize=8.0, color=INK)
ax.annotate('1.7%', (2.46, 0.0165), textcoords='offset points', xytext=(9, 5),
            fontsize=8.0, color=INK)
ax.set_ylabel('$I/I_0$')
ax.set_xlim(-3.6, 3.6); ax.set_ylim(0, 1.40)
ax.set_yticks([0, 0.5, 1.0]); ax.set_xticks([])
ax.spines[['top', 'right']].set_visible(False)
ax2.imshow(np.tile(I**0.42, (2, 1)), extent=[-3.6, 3.6, 0, 1], aspect='auto',
           cmap='gray', vmin=0, vmax=1)
ax2.set_yticks([]); ax2.set_xticks(np.arange(-3, 4))
ax2.set_xlabel(r'$a\sin\theta/\lambda$')
```

### Width of the central maximum

The first minima lie at $\sin\theta = \pm\lambda/a$. For small angles
$\sin\theta \approx \theta$, so the **angular half-width** of the central maximum
is $\lambda/a$ and its **angular width** is

$$ 2\theta_1 = \frac{2\lambda}{a} $$

On a screen a distance $D$ from the slit (or in the focal plane of a lens of focal
length $f$), the linear width of the central bright band is

$$ w = \frac{2\lambda D}{a} \qquad\text{or}\qquad w = \frac{2\lambda f}{a} $$

::: caution Narrower slit, wider patch
Students expect a narrower slit to give a narrower patch of light. The opposite
is true: $w \propto 1/a$, so **halving the slit width doubles the spread**. Only
when $a \gg \lambda$ does the patch shrink to the geometrical shadow of the slit,
which is why ray optics works for everyday apertures.
:::

::: example Worked example 12.1
**Problem.** A slit $0.20\ \text{mm}$ wide is illuminated normally by light of
wavelength $600\ \text{nm}$. The diffraction pattern is observed on a screen
$1.5\ \text{m}$ away. Find (a) the angular position of the first minimum,
(b) the linear width of the central maximum, (c) the distance of the second
minimum from the centre.

**Solution.**

(a) $\sin\theta_1 = \dfrac{\lambda}{a} = \dfrac{600\times10^{-9}}{0.20\times10^{-3}}
 = 3.0\times10^{-3}$, so $\theta_1 = 3.0\times10^{-3}\ \text{rad} = 0.17^\circ$.

(b) $w = \dfrac{2\lambda D}{a} = 2 \times 3.0\times10^{-3} \times 1.5
 = 9.0\times10^{-3}\ \text{m} = 9.0\ \text{mm}$.

(c) $\sin\theta_2 = 2\lambda/a = 6.0\times10^{-3}$, so
$y_2 = D\tan\theta_2 \approx 1.5 \times 6.0\times10^{-3} = 9.0\ \text{mm}$.
:::

## 12.2 Diffraction pattern of image; Diffraction grating

### The image of a slit

Geometrical optics says the image of an illuminated slit is a sharp bright
rectangle. What is actually seen in the focal plane of the lens is a **broad
central bright band** flanked by progressively fainter bands separated by dark
lines — the pattern of the previous figure. Every optical image is really a
diffraction pattern; a "point" image is never a point.

Interference and diffraction are both superposition effects, but the NEB expects
you to be able to separate them:

| Interference (Young) | Diffraction (single slit) |
|---|---|
| Superposition of waves from **two separate** coherent sources | Superposition of secondary wavelets from **different parts of the same** wavefront |
| Fringes of **equal width** | Central band twice as wide as the rest |
| All bright fringes of **equal intensity** | Intensity falls off rapidly away from the centre |
| Dark fringes are perfectly dark | Minima are dark but the pattern never fully repeats |
| Bright: $\Delta = n\lambda$ | Dark: $a\sin\theta = n\lambda$ |

### Diffraction grating

A **diffraction grating** is a glass or plastic plate ruled with a very large
number of equidistant parallel lines; the ruled lines are opaque and the gaps
between them act as slits. If there are $N$ lines per metre, the distance from the
centre of one slit to the centre of the next is the **grating element**

$$ d = \frac{1}{N} = e + b $$

where $e$ is the width of a transparent slit and $b$ that of an opaque ruling. A
good grating has 5000–15000 lines per centimetre, so $d$ is a couple of micrometres.

```figure caption="(a) Plane waves on a grating of element $d$; adjacent slits contribute a path difference $d\sin\theta$. (b) Intensity from $N = 6$ slits: the principal maxima at $d\sin\theta = n\lambda$ are far sharper than two-slit fringes."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, axes = plt.subplots(1, 2, figsize=(5.2, 2.6))

ax = axes[0]
thd = 26.0
th = np.radians(thd); u = np.array([np.cos(th), np.sin(th)])
d = 1.0; slit = 0.30
ys = np.arange(-2, 3)*d
edges = [-3.0] + [v for y in ys for v in (y-slit/2, y+slit/2)] + [3.0]
for k in range(0, len(edges)-1, 2):
    ax.add_patch(Rectangle((-0.10, edges[k]), 0.20, edges[k+1]-edges[k],
                           color=INK, lw=0))
for y0 in ys:
    P0 = np.array([0.0, y0])
    ax.annotate('', xy=tuple(P0+2.3*u), xytext=tuple(P0),
                arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.0, mutation_scale=7))
for yin in np.linspace(-2.7, 2.7, 7):
    ax.annotate('', xy=(-0.18, yin), xytext=(-1.05, yin),
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.9, mutation_scale=6))
S0 = np.array([0.0, -1.0]); S1 = np.array([0.0, 0.0])
Nf = S0 + np.dot(S1-S0, u)*u
ax.plot([S1[0], Nf[0]], [S1[1], Nf[1]], color=MUTED, lw=1.0, ls=(0, (3, 2)))
ax.plot([S0[0], Nf[0]], [S0[1], Nf[1]], color='#d9534f', lw=3.0, zorder=6)
ax.annotate(r'$d\sin\theta$', xy=tuple(0.5*(S0+Nf)), xytext=(1.55, -2.35),
            ha='center', color='#d9534f', fontsize=8.8,
            arrowprops=dict(arrowstyle='-', color='#d9534f', lw=0.8))
ax.annotate('', xy=(-0.38, 1.0), xytext=(-0.38, 2.0),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=0.9, mutation_scale=6))
ax.annotate('$d$', (-0.38, 1.5), textcoords='offset points', xytext=(-9, -4), fontsize=9.5)
ax.annotate(r'$\theta$', (1.45, 0.42), fontsize=9.5, color=ACCENT)
ax.set_title('(a) grating geometry', fontsize=9)
ax.set_xlim(-1.5, 2.6); ax.set_ylim(-3.0, 3.0)
ax.set_aspect('equal'); ax.axis('off')

ax = axes[1]
Ns = 6
s = np.linspace(-2.45, 2.45, 6000)
num = np.sin(Ns*np.pi*s); den = Ns*np.sin(np.pi*s)
safe = np.where(np.abs(den) < 1e-7, 1.0, den)
g = np.where(np.abs(den) < 1e-7, 1.0, num/safe)**2
ax.plot(s, g, color=ACCENT, lw=1.3)
ax.fill_between(s, 0, g, color=ACCENT, alpha=0.12)
for n in range(-2, 3):
    ax.annotate(f'$n={n}$', (n, 1.06), ha='center', fontsize=7.6, color=INK)
ax.set_xlabel(r'$d\sin\theta/\lambda$'); ax.set_ylabel('$I/I_{max}$')
ax.set_xlim(-2.45, 2.45); ax.set_ylim(0, 1.32)
ax.set_xticks([-2, -1, 0, 1, 2]); ax.set_yticks([0, 0.5, 1])
ax.set_title('(b) $N = 6$ slits', fontsize=9)
ax.spines[['top', 'right']].set_visible(False)
```

::: derivation The grating equation
Plane monochromatic light falls normally on the grating. Take the parallel rays
that leave every slit at an angle $\theta$; a lens brings them to one point. The
path difference between the wavelets from any two **adjacent** slits is the same,
namely $d\sin\theta$.

All $N$ slits then reinforce one another only when this common path difference is
a whole number of wavelengths:

$$ d\sin\theta = n\lambda, \qquad n = 0, 1, 2, 3, \dots $$

This is the **grating equation**, and $n$ is the order of the spectrum. Because
$N$ is huge (tens of thousands), the slightest departure from the condition throws
the contributions of distant slits out of step, so the maxima are extremely sharp
— which is what makes a grating a precision wavelength-measuring instrument.
:::

Two consequences follow:

- Since $\sin\theta \le 1$, the **highest order** obtainable is
  $n_{\max} = d/\lambda$ (rounded down to a whole number).
- For a given order, $\sin\theta \propto \lambda$, so white light is spread into a
  spectrum with **violet closest to the centre and red furthest out** — the
  opposite way round from a prism, where red is deviated least.

::: example Worked example 12.2
**Problem.** A plane diffraction grating has $5000$ lines per centimetre. Light
of wavelength $500\ \text{nm}$ falls normally on it. Find the angles of the first,
second and third order maxima, and the highest order that can be observed.

**Solution.** The grating element is

$$ d = \frac{1\ \text{cm}}{5000} = \frac{10^{-2}}{5000} = 2.0\times10^{-6}\ \text{m} $$

From $d\sin\theta = n\lambda$, $\sin\theta = n\lambda/d = n(0.25)$.

- $n = 1$: $\sin\theta = 0.25$, $\theta_1 = 14.5^\circ$
- $n = 2$: $\sin\theta = 0.50$, $\theta_2 = 30.0^\circ$
- $n = 3$: $\sin\theta = 0.75$, $\theta_3 = 48.6^\circ$

The highest order needs $\sin\theta \le 1$, i.e. $n \le d/\lambda = 4$. But
$n = 4$ gives $\sin\theta = 1$, i.e. $\theta = 90^\circ$ — light grazing along the
grating, which cannot be collected. So only **three** orders are actually seen on
each side of the centre.
:::

## 12.3 Resolving power of optical instruments

Because every image is a diffraction patch, two nearby stars produce two
overlapping patches. If the patches overlap too much they merge into one and the
stars cannot be told apart. Lord Rayleigh gave the practical dividing line.

::: definition Rayleigh criterion
Two point objects are said to be **just resolved** when the central maximum of the
diffraction pattern of one falls exactly on the first minimum of the pattern of
the other.
:::

```figure caption="Rayleigh's criterion for a circular aperture. The dashed curves are the two individual diffraction patterns and the solid curve is what the eye actually receives. At the Rayleigh separation the combined curve has a dip of about 26% and the pair is just resolved."
import numpy as np, matplotlib.pyplot as plt
def airy(x):
    t = np.linspace(0.0, np.pi, 500)
    z = np.abs(x)[:, None]
    j1 = np.trapezoid(np.cos(t - z*np.sin(t)), t, axis=1)/np.pi
    out = np.ones_like(x)
    m = np.abs(x) > 1e-9
    out[m] = (2*j1[m]/x[m])**2
    return out
fig, axes = plt.subplots(1, 3, figsize=(5.2, 2.3), sharey=True)
x = np.linspace(-11, 11, 900)
R = 3.8317
for ax, f, ttl in [(axes[0], 0.55, 'not resolved'),
                   (axes[1], 1.00, 'just resolved'),
                   (axes[2], 1.70, 'well resolved')]:
    s = f*R
    I1 = airy(x - s/2); I2 = airy(x + s/2)
    ax.plot(x, I1, color=MUTED, lw=0.9, ls=(0, (3, 2)))
    ax.plot(x, I2, color=MUTED, lw=0.9, ls=(0, (3, 2)))
    ax.plot(x, I1+I2, color=ACCENT, lw=1.8)
    ax.set_title(ttl, fontsize=8.8)
    ax.set_xticks([]); ax.set_xlim(-11, 11)
    ax.spines[['top', 'right']].set_visible(False)
axes[1].axvline(R/2, color='#d9534f', lw=0.8, ls=':')
axes[1].axvline(-R/2, color='#d9534f', lw=0.8, ls=':')
axes[0].set_ylabel('intensity'); axes[0].set_yticks([])
axes[0].set_ylim(0, 2.25)
```

### Telescope

For a circular aperture of diameter $a$ the first dark ring of the diffraction
pattern lies at an angle $1.22\lambda/a$ (the factor $1.22$ comes from the circular
shape; for a slit it would be $1$). So two stars are just resolved when their
angular separation is

$$ \theta_{\min} = \frac{1.22\lambda}{a} $$

and the **resolving power** of the telescope, defined as the reciprocal of the
limit of resolution, is

$$ \text{R.P.} = \frac{1}{\theta_{\min}} = \frac{a}{1.22\lambda} $$

A bigger objective therefore resolves better *and* collects more light — which is
why research telescopes are built with mirrors metres across.

### Microscope

For a microscope the useful quantity is the smallest separation $x$ between two
points in the object that can still be distinguished:

$$ x_{\min} = \frac{1.22\lambda}{2\mu\sin\theta}, \qquad
   \text{R.P.} = \frac{1}{x_{\min}} = \frac{2\mu\sin\theta}{1.22\lambda} $$

Here $\theta$ is the half-angle of the cone of light entering the objective and
$\mu$ is the refractive index of the medium between object and objective. The
product $\mu\sin\theta$ is the **numerical aperture**. Two ways of improving a
microscope follow at once: use shorter wavelengths (blue light, or electrons in
an electron microscope), and raise $\mu$ by putting a drop of cedar oil
($\mu \approx 1.5$) between the slide and the objective — oil immersion.

For a **grating** the corresponding quantity is the ability to separate two close
wavelengths, and it works out to $\lambda/\mathrm{d}\lambda = nN$, where $N$ is the
total number of lines actually illuminated and $n$ is the order.

::: example Worked example 12.3
**Problem.** A telescope objective has a diameter of $100\ \text{mm}$. Taking the
mean wavelength of light as $550\ \text{nm}$, find (a) its limit of resolution and
(b) the smallest distance between two objects on the Moon, $3.84\times10^{8}\ \text{m}$
away, that this telescope could just resolve.

**Solution.**

(a) $\theta_{\min} = \dfrac{1.22\lambda}{a}
 = \dfrac{1.22 \times 550\times10^{-9}}{0.100}
 = 6.71\times10^{-6}\ \text{rad}$

(b) For small angles the linear separation is $x = r\theta_{\min}$:

$$ x = 3.84\times10^{8} \times 6.71\times10^{-6} = 2.58\times10^{3}\ \text{m} $$

so about $2.6\ \text{km}$ — a small telescope cannot show anything on the Moon
smaller than a large town.
:::

::: example Worked example 12.4
**Problem.** An oil-immersion microscope objective works with light of wavelength
$500\ \text{nm}$, a half-angle of $60^\circ$ and oil of refractive index $1.5$.
Find the smallest separation it can resolve.

**Solution.** The numerical aperture is
$\mu\sin\theta = 1.5 \times \sin 60^\circ = 1.5 \times 0.866 = 1.299$.

$$ x_{\min} = \frac{1.22\lambda}{2\mu\sin\theta}
 = \frac{1.22 \times 500\times10^{-9}}{2 \times 1.299}
 = \frac{6.10\times10^{-7}}{2.598} = 2.35\times10^{-7}\ \text{m} $$

That is $235\ \text{nm}$ — smaller than a bacterium, but far larger than a virus,
which is why viruses need an electron microscope.
:::

## Chapter summary

- **Diffraction** is the bending of light round edges, noticeable only when the
  aperture is comparable with $\lambda$. Fraunhofer diffraction uses plane waves.
- Single slit **minima**: $a\sin\theta = n\lambda$ for $n = \pm1, \pm2, \dots$;
  secondary maxima near $a\sin\theta = (n+\frac{1}{2})\lambda$, of relative
  intensity 4.7%, 1.7%, …
- Intensity: $I = I_0(\sin\beta/\beta)^2$ with $\beta = \pi a\sin\theta/\lambda$.
- Central maximum: angular width $2\lambda/a$, linear width $2\lambda D/a$ — it
  gets **wider** as the slit gets narrower.
- Grating element $d = 1/N$; **grating equation** $d\sin\theta = n\lambda$; highest
  order $n_{\max} = d/\lambda$; in each order violet is deviated least.
- **Rayleigh criterion**: just resolved when one central maximum sits on the
  other's first minimum.
- Telescope: $\theta_{\min} = 1.22\lambda/a$, R.P. $= a/1.22\lambda$.
  Microscope: $x_{\min} = 1.22\lambda/2\mu\sin\theta$. Grating:
  $\lambda/\mathrm{d}\lambda = nN$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. In Fraunhofer diffraction at a single slit, the condition for the $n$th minimum is <span class="marks">[1]</span>
   (a) $a\sin\theta = n\lambda$ (b) $a\sin\theta = (2n+1)\lambda/2$
   (c) $d\sin\theta = n\lambda$ (d) $a\cos\theta = n\lambda$
2. The width of the central maximum in single-slit diffraction <span class="marks">[1]</span>
   (a) increases with slit width (b) decreases with slit width
   (c) does not depend on the slit width (d) is always zero
3. A grating has $2000$ lines per centimetre. Its grating element is <span class="marks">[1]</span>
   (a) 2 μm (b) 5 μm (c) 0.5 μm (d) 20 μm
4. The resolving power of a telescope can be increased by <span class="marks">[1]</span>
   (a) increasing the wavelength (b) increasing the aperture
   (c) decreasing the aperture (d) increasing the eyepiece magnification
5. Diffraction is most easily observed when the size of the aperture is <span class="marks">[1]</span>
   (a) much larger than $\lambda$ (b) comparable with $\lambda$
   (c) exactly zero (d) infinite

::: note Answers to Group A
**1.** (a) — pairing the two halves of the slit gives $a\sin\theta = n\lambda$ for **darkness**.
**2.** (b) — $w = 2\lambda D/a$, so $w$ and $a$ are inversely related.
**3.** (b) — $d = 1\ \text{cm}/2000 = 5\times10^{-4}\ \text{cm} = 5\ \text{μm}$.
**4.** (b) — R.P. $= a/1.22\lambda$, so a larger objective resolves better.
**5.** (b) — bending is appreciable only when the aperture is of the order of the wavelength.
:::

**Group B — Short answer (5 marks each)**

1. What is diffraction of light? Distinguish between interference and diffraction. <span class="marks">[5]</span>
2. Derive the condition for minima in Fraunhofer diffraction at a single slit and
   hence obtain the width of the central maximum. <span class="marks">[5]</span>
3. Light of wavelength $500\ \text{nm}$ falls normally on a slit of width
   $0.10\ \text{mm}$. The pattern is seen on a screen $1.0\ \text{m}$ away. Find
   the distance between the first minima on the two sides of the centre. <span class="marks">[5]</span>
4. What is a diffraction grating? Obtain the grating equation and explain why the
   maxima are sharp. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Outline: diffraction = bending of light at an aperture comparable with
$\lambda$, caused by superposition of secondary wavelets from one wavefront;
interference involves two separate coherent sources. Compare fringe width,
intensity of successive maxima and the darkness of the minima (see the table in
§12.2).

**3.** $\sin\theta_1 = \dfrac{\lambda}{a} = \dfrac{500\times10^{-9}}{1.0\times10^{-4}}
= 5.0\times10^{-3}$. Distance of one first minimum from the centre is
$y_1 = D\theta_1 = 1.0 \times 5.0\times10^{-3} = 5.0\ \text{mm}$, so the separation
of the two first minima (the width of the central maximum) is
$2y_1 = 10\ \text{mm} = 1.0\ \text{cm}$.
:::

**Group C — Long answer (8 marks each)**

1. (a) Explain Fraunhofer diffraction at a single slit and derive the positions of
   the minima. <span class="marks">[5]</span>
   (b) Sketch the intensity distribution and state the Rayleigh criterion for
   resolution. <span class="marks">[3]</span>
2. A diffraction grating has $6000$ lines per centimetre and is illuminated
   normally by light of wavelength $600\ \text{nm}$. Find (a) the grating element,
   (b) the angles of the first and second order maxima, (c) the highest order that
   can be seen, and (d) the smallest wavelength difference the grating can resolve
   in the second order if $8000$ lines are illuminated. <span class="marks">[8]</span>

::: note Answer to Group C question 2
(a) $d = \dfrac{10^{-2}}{6000} = 1.667\times10^{-6}\ \text{m} = 1.667\ \text{μm}$.

(b) $\sin\theta = n\lambda/d$ with $\lambda/d = 600\times10^{-9}/1.667\times10^{-6} = 0.36$.
For $n = 1$: $\sin\theta_1 = 0.36$, $\theta_1 = 21.1^\circ$.
For $n = 2$: $\sin\theta_2 = 0.72$, $\theta_2 = 46.1^\circ$.

(c) $n_{\max} = d/\lambda = 1/0.36 = 2.78$, so the highest observable order is
$n = 2$.

(d) $\dfrac{\lambda}{\mathrm{d}\lambda} = nN = 2 \times 8000 = 16000$, so

$$ \mathrm{d}\lambda = \frac{600}{16000} = 0.0375\ \text{nm} $$
:::
