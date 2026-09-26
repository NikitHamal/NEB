---
subject: Physics
grade: 12
unit: 8
title: Wave in pipes and strings
hours: 4
area: Waves and Optics
---

A flute made from Kathmandu bamboo, a sarangi string, a bottle you blow across —
all of them make a musical note the same way. A wave is trapped between two
boundaries, reflects back and forth, and only those wavelengths that fit the
boundaries survive. This unit works out exactly which wavelengths fit, for air
columns and for stretched strings, and turns each answer into a frequency you
can calculate.

::: key The one question every problem asks
*Which whole number of quarter- or half-wavelengths fits between the two ends?*
Fix the node/antinode at each end from the physics, count the loops, read off
$\lambda$, and use $f = v/\lambda$. Everything in this unit is that one step.
:::

## 8.1 Stationary waves in closed and open pipes

When a progressive wave reaches the end of a pipe it is reflected. The reflected
wave and the incident wave, of equal frequency and amplitude but opposite
direction, superpose to give a **stationary (standing) wave** with fixed
**nodes** (zero displacement) and **antinodes** (maximum displacement). Adjacent
nodes are $\lambda/2$ apart; a node and the next antinode are $\lambda/4$ apart.

What decides where the nodes are is the **boundary condition** at each end:

| End of pipe | Can the air move? | Can the pressure change? | Displacement | Pressure |
|---|---|---|---|---|
| Closed (rigid) | no | yes | **node** | antinode |
| Open (to atmosphere) | yes | no | **antinode** | node |

At a closed end the rigid surface stops the air moving, so the displacement must
be zero — a displacement node. At an open end the air is in contact with the
atmosphere, whose pressure it cannot change, so the pressure variation is zero —
a pressure node, which is the same place as a displacement antinode.

::: caution Displacement node = pressure antinode
The two descriptions are always a quarter wavelength out of step. A closed end
is a *displacement* node but a *pressure* antinode. If a question says "pressure
antinode at the closed end" it is saying exactly the same thing as "displacement
node". Decide which quantity you are drawing before you draw.
:::

A **closed pipe** (closed organ pipe) is closed at one end and open at the
other. An **open pipe** (open organ pipe) is open at both ends. A flute or bansuri
behaves as an open pipe; a stopped organ pipe and a test-tube behave as closed
pipes.

## 8.2 Harmonics and overtones in closed and open organ pipes

### Closed organ pipe

The closed end must be a node and the open end an antinode, so the shortest
column that fits is a quarter of a wavelength.

```figure caption="The first three modes of a closed organ pipe of length $L$. The closed end is always a displacement node (N), the open end an antinode (A). Only odd harmonics are possible."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,4.3))
L, A, R = 4.0, 0.46, 0.56
x = np.linspace(0, L, 400)
modes = [(1, 'Fundamental\n(1st harmonic)', '$L=\\lambda/4$\n$f_1=v/4L$'),
         (3, '1st overtone\n(3rd harmonic)', '$L=3\\lambda/4$\n$f_2=3f_1$'),
         (5, '2nd overtone\n(5th harmonic)', '$L=5\\lambda/4$\n$f_3=5f_1$')]
for i, (h, left, right) in enumerate(modes):
    yc = -2.20*i
    ax.plot([0, L], [yc+R, yc+R], color=INK, lw=1.5)
    ax.plot([0, L], [yc-R, yc-R], color=INK, lw=1.5)
    ax.plot([0, 0], [yc-R, yc+R], color=INK, lw=2.8)
    for t in np.linspace(yc-R, yc+R, 7):
        ax.plot([-0.18, 0], [t-0.10, t], color=MUTED, lw=0.8)
    env = A*np.sin(h*np.pi*x/(2*L))
    ax.plot(x, yc+env, color=ACCENT, lw=1.8)
    ax.plot(x, yc-env, color=ACCENT, lw=1.8)
    ax.fill_between(x, yc-env, yc+env, color=ACCENT, alpha=0.10)
    for m in range(h):
        xn = m*2.0*L/h
        if xn <= L+1e-9:
            ax.plot([xn], [yc], 'o', color='#A8271F', ms=4.0, zorder=6)
            ax.annotate('N', (xn, yc-R-0.08), ha='center', va='top',
                        color='#A8271F', fontsize=9)
        xa = (2*m+1)*L/h
        if xa <= L+1e-9:
            ax.annotate('A', (xa, yc-R-0.08), ha='center', va='top',
                        color='#0B6A62', fontsize=9)
    ax.annotate(left, (-0.42, yc), ha='right', va='center', color=INK, fontsize=8.5)
    ax.annotate(right, (L+0.30, yc), ha='left', va='center', color=MUTED, fontsize=8.5)
ax.annotate('closed end', (0, R+0.72), ha='center', va='bottom', color=MUTED, fontsize=8.2)
ax.annotate('open end', (L, R+0.72), ha='center', va='bottom', color=MUTED, fontsize=8.2)
for xx in (0, L):
    ax.annotate('', xy=(xx, R+0.10), xytext=(xx, R+0.70),
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.9, mutation_scale=8))
ax.set_xlim(-2.45, L+1.70); ax.set_ylim(-5.45, 1.75)
ax.axis('off')
```

Reading the modes off the diagram, the possible lengths are
$L = \lambda/4,\ 3\lambda/4,\ 5\lambda/4,\dots$, i.e.

$$ L = (2n-1)\frac{\lambda_n}{4} \;\Longrightarrow\; \lambda_n = \frac{4L}{2n-1} $$

and since $f = v/\lambda$,

$$ f_n = (2n-1)\frac{v}{4L} = (2n-1)f_1, \qquad f_1 = \frac{v}{4L} $$

So a closed pipe produces **only the odd harmonics** $f_1 : 3f_1 : 5f_1 : \dots$
The even harmonics are missing.

### Open organ pipe

Both ends are antinodes, so the shortest column is half a wavelength.

```figure caption="The first three modes of an open organ pipe. Both ends are antinodes (A), so all harmonics — odd and even — are present."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,4.3))
L, A, R = 4.0, 0.46, 0.56
x = np.linspace(0, L, 400)
modes = [(1, 'Fundamental\n(1st harmonic)', '$L=\\lambda/2$\n$f_1=v/2L$'),
         (2, '1st overtone\n(2nd harmonic)', '$L=\\lambda$\n$f_2=2f_1$'),
         (3, '2nd overtone\n(3rd harmonic)', '$L=3\\lambda/2$\n$f_3=3f_1$')]
for i, (n, left, right) in enumerate(modes):
    yc = -2.20*i
    ax.plot([0, L], [yc+R, yc+R], color=INK, lw=1.5)
    ax.plot([0, L], [yc-R, yc-R], color=INK, lw=1.5)
    env = A*np.cos(n*np.pi*x/L)
    ax.plot(x, yc+env, color=ACCENT, lw=1.8)
    ax.plot(x, yc-env, color=ACCENT, lw=1.8)
    ax.fill_between(x, yc-env, yc+env, color=ACCENT, alpha=0.10)
    for m in range(n+1):
        ax.annotate('A', (m*L/n, yc-R-0.08), ha='center', va='top',
                    color='#0B6A62', fontsize=9)
    for m in range(n):
        xn = (2*m+1)*L/(2.0*n)
        ax.plot([xn], [yc], 'o', color='#A8271F', ms=4.0, zorder=6)
        ax.annotate('N', (xn, yc-R-0.08), ha='center', va='top',
                    color='#A8271F', fontsize=9)
    ax.annotate(left, (-0.42, yc), ha='right', va='center', color=INK, fontsize=8.5)
    ax.annotate(right, (L+0.30, yc), ha='left', va='center', color=MUTED, fontsize=8.5)
for xx in (0, L):
    ax.annotate('open end', (xx, R+0.72), ha='center', va='bottom',
                color=MUTED, fontsize=8.2)
    ax.annotate('', xy=(xx, R+0.10), xytext=(xx, R+0.70),
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.9, mutation_scale=8))
ax.set_xlim(-2.45, L+1.70); ax.set_ylim(-5.45, 1.75)
ax.axis('off')
```

Here $L = n\lambda_n/2$, so $\lambda_n = 2L/n$ and

$$ f_n = n\frac{v}{2L} = nf_1, \qquad f_1 = \frac{v}{2L} $$

| | Closed pipe | Open pipe |
|---|---|---|
| Fundamental | $f_1 = v/4L$ | $f_1 = v/2L$ |
| Harmonics present | odd only: 1, 3, 5, … | all: 1, 2, 3, … |
| 1st overtone | 3rd harmonic, $3f_1$ | 2nd harmonic, $2f_1$ |
| 2nd overtone | 5th harmonic, $5f_1$ | 3rd harmonic, $3f_1$ |
| Quality of note | poorer (few harmonics) | richer (many harmonics) |
| Same length $L$ | note one octave **lower** | note one octave **higher** |

::: memory Harmonic or overtone?
A **harmonic** is any whole-number multiple of the fundamental. An **overtone**
is any tone actually produced above the fundamental, counted in order. So for a
closed pipe the 1st overtone *is* the 3rd harmonic — the 2nd harmonic does not
exist. Confusing the two words loses marks in almost every paper.
:::

::: example Worked example 8.1
**Problem.** A closed organ pipe is 25 cm long. Taking the speed of sound as
340 m s⁻¹, find its fundamental frequency and the frequencies of its first two
overtones. What would the fundamental be if the same pipe were open at both ends?

**Solution.** Closed pipe, $L = 0.25\ \text{m}$:

$$ f_1 = \frac{v}{4L} = \frac{340}{4\times0.25} = \frac{340}{1.00} = 340\ \text{Hz} $$

Only odd harmonics occur, so the first overtone is the 3rd harmonic and the
second overtone is the 5th harmonic:

$$ f_2 = 3f_1 = 1020\ \text{Hz}, \qquad f_3 = 5f_1 = 1700\ \text{Hz} $$

If the same pipe were open at both ends,

$$ f_1' = \frac{v}{2L} = \frac{340}{0.50} = 680\ \text{Hz} $$

exactly twice as high — one octave above.
:::

## 8.3 End correction in pipes

The air just outside an open end still takes part in the vibration, so the
antinode does not sit exactly at the rim: it lies a small distance **outside**.
That distance is the **end correction** $e$. Rayleigh showed that for a pipe of
internal radius $r$,

$$ e = 0.6\,r $$

The pipe therefore behaves as though it were longer than it measures:

$$ \text{closed pipe: } f_1 = \frac{v}{4(L+e)}, \qquad
\text{open pipe: } f_1 = \frac{v}{2(L+2e)} $$

(an open pipe has two open ends, so it gets two corrections). End correction
matters most for short, wide pipes.

```figure caption="Resonance-tube experiment. The air column resonates at $l_1$ and again at $l_2$. The antinode lies a distance $e$ above the rim ($e$ is exaggerated here)."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.0,4.4))
TOP, W, lam, e, Ae = 5.0, 0.42, 6.0, 0.50, 0.34
for xc, l, lab, ln in [(0.0, 1.0, 'first resonance', '$l_1$'),
                       (3.7, 4.0, 'second resonance', '$l_2$')]:
    ys = TOP - l
    ax.add_patch(Rectangle((xc-W, -0.45), 2*W, ys+0.45, facecolor='#bcd9f0',
                           edgecolor='none', alpha=0.8))
    ax.plot([xc-W, xc-W], [-0.45, TOP], color=INK, lw=1.5)
    ax.plot([xc+W, xc+W], [-0.45, TOP], color=INK, lw=1.5)
    ax.plot([xc-W, xc+W], [-0.45, -0.45], color=INK, lw=1.5)
    ax.plot([xc-W, xc+W], [ys, ys], color='#1d6fb8', lw=1.3)
    yi = np.linspace(ys, TOP, 240); yo = np.linspace(TOP, TOP+e, 40)
    for sgn in (1, -1):
        ax.plot(xc+sgn*Ae*np.sin(2*np.pi*(yi-ys)/lam), yi, color='#A8271F', lw=1.7)
        ax.plot(xc+sgn*Ae*np.sin(2*np.pi*(yo-ys)/lam), yo, color='#A8271F',
                lw=1.3, ls=(0,(3,2)))
    ax.plot([xc], [ys], 'o', color='#A8271F', ms=4.2, zorder=6)
    ax.annotate('N', (xc+W+0.12, ys), ha='left', va='center',
                color='#A8271F', fontsize=8.8)
    if l > 2:
        yn = ys + lam/2
        ax.plot([xc], [yn], 'o', color='#A8271F', ms=4.2, zorder=6)
        ax.annotate('N', (xc+W+0.12, yn), ha='left', va='center',
                    color='#A8271F', fontsize=8.8)
        ax.annotate('A', (xc+W+0.12, ys+lam/4), ha='left', va='center',
                    color='#0B6A62', fontsize=8.8)
    ax.annotate('A', (xc+W+0.12, TOP+e), ha='left', va='center',
                color='#0B6A62', fontsize=8.8)
    xd = xc - 1.10
    ax.annotate('', xy=(xd, ys), xytext=(xd, TOP),
                arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=1.0,
                                mutation_scale=8, shrinkA=0, shrinkB=0))
    ax.plot([xd, xc-W], [ys, ys], color=MUTED, lw=0.6, ls=':')
    ax.plot([xd, xc-W], [TOP, TOP], color=MUTED, lw=0.6, ls=':')
    ax.annotate(ln, (xd-0.12, (ys+TOP)/2), ha='right', va='center',
                color=MUTED, fontsize=10)
    ax.annotate(lab, (xc, -0.85), ha='center', va='top', color=INK, fontsize=8.8)
    ax.annotate('water', (xc, ys-0.22), ha='center', va='top',
                color='#12639c', fontsize=8.2)
    fy = TOP + 1.30
    ax.plot([xc, xc], [fy-0.32, fy], color=INK, lw=1.7)
    ax.plot([xc-0.24, xc-0.24], [fy, fy+0.58], color=INK, lw=1.7)
    ax.plot([xc+0.24, xc+0.24], [fy, fy+0.58], color=INK, lw=1.7)
    ax.plot([xc-0.24, xc+0.24], [fy, fy], color=INK, lw=1.7)
for xa, xb in [(-1.60, 0.46), (0.94, 4.16)]:
    ax.plot([xa, xb], [TOP+e, TOP+e], color='#0B6A62', lw=0.8, ls=(0,(4,3)))
ax.annotate('', xy=(1.75, TOP), xytext=(1.75, TOP+e),
            arrowprops=dict(arrowstyle='<|-|>', color='#0B6A62', lw=1.1,
                            mutation_scale=8, shrinkA=0, shrinkB=0))
ax.annotate('end correction $e$:\nthe antinode lies\noutside the open end',
            (1.75, TOP-0.35), ha='center', va='top', color='#0B6A62', fontsize=8.2)
ax.annotate('tuning fork of frequency $f$', (1.85, TOP+2.05), ha='center',
            va='bottom', color=MUTED, fontsize=8.6)
ax.set_xlim(-2.25, 5.35); ax.set_ylim(-1.55, 7.35)
ax.axis('off')
```

::: derivation Eliminating the end correction in a resonance tube
Lower the water level below a sounding tuning fork of frequency $f$ and the air
column resonates first at length $l_1$ and next at $l_2$. Including the
correction,

$$ l_1 + e = \frac{\lambda}{4}, \qquad l_2 + e = \frac{3\lambda}{4} $$

**Subtracting** the first from the second removes $e$ altogether:

$$ l_2 - l_1 = \frac{\lambda}{2} \;\Longrightarrow\; \lambda = 2(l_2-l_1) $$
$$ v = f\lambda = 2f(l_2 - l_1) $$

**Multiplying** the first by 3 and subtracting the second instead gives $e$:

$$ 3l_1 + 3e = l_2 + e \;\Longrightarrow\; e = \frac{l_2 - 3l_1}{2} $$

This is why the resonance tube is the standard school experiment for measuring
the velocity of sound: the awkward unknown $e$ cancels.
:::

::: example Worked example 8.2
**Problem.** In a resonance-tube experiment a tuning fork of frequency 480 Hz
gives resonance when the air column is 17.0 cm long and again when it is
53.0 cm long. Find the velocity of sound in air and the end correction.

**Solution.** $l_1 = 0.170\ \text{m}$, $l_2 = 0.530\ \text{m}$.

$$ \lambda = 2(l_2-l_1) = 2(0.530-0.170) = 0.720\ \text{m} $$
$$ v = f\lambda = 480\times0.720 = 345.6\ \text{m s}^{-1} $$

For the end correction,

$$ e = \frac{l_2 - 3l_1}{2} = \frac{0.530 - 0.510}{2} = 0.010\ \text{m} = 1.0\ \text{cm} $$

Since $e = 0.6r$, the internal radius of the tube is $r = 1.0/0.6 = 1.7\ \text{cm}$.
:::

## 8.4 Velocity of transverse waves along a stretched string

A stretched string carries **transverse** waves. Two quantities control their
speed: the tension $T$ that pulls a displaced element back, and the mass per
unit length (linear density) $\mu = m/L$ that resists the pull.

::: derivation Speed of a transverse wave on a string
Let a pulse travel with speed $v$ along a string of tension $T$ and linear
density $\mu$. View it from a frame moving with the pulse: the pulse stands
still and the string streams backwards through it with speed $v$.

Take a short element at the crest of the pulse. It is very nearly an arc of a
circle of radius $R$ subtending a small angle $\Delta\theta$ at the centre, so
its length is $R\Delta\theta$ and its mass is

$$ \Delta m = \mu R \Delta\theta $$

The tension $T$ pulls tangentially at each end of the arc. The tangential
directions make angles $\Delta\theta/2$ with the horizontal, so the horizontal
components cancel and the vertical components add, giving a resultant towards
the centre of curvature:

$$ F = 2T\sin\frac{\Delta\theta}{2} \approx 2T\cdot\frac{\Delta\theta}{2} = T\Delta\theta $$

In this frame the element moves along the arc with speed $v$, so $F$ is the
centripetal force:

$$ T\Delta\theta = \Delta m\,\frac{v^{2}}{R} = \mu R\Delta\theta\cdot\frac{v^{2}}{R} = \mu v^{2}\Delta\theta $$

Cancelling $\Delta\theta$,

$$ v^{2} = \frac{T}{\mu} \;\Longrightarrow\; v = \sqrt{\frac{T}{\mu}} $$
:::

Check the dimensions: $[T]/[\mu] = (\text{M L T}^{-2})/(\text{M L}^{-1}) = \text{L}^2\text{T}^{-2}$,
whose square root is a velocity. If the wire has radius $r$ and material density
$\rho$ then $\mu = \pi r^{2}\rho$, so a thicker or denser wire carries slower
waves.

## 8.5 Vibration of string and overtones

A sonometer wire is clamped at both ends, so **both ends must be nodes**. The
string is therefore a whole number of half-wavelength loops long:

$$ L = n\frac{\lambda_n}{2} \;\Longrightarrow\; \lambda_n = \frac{2L}{n},
\qquad n = 1, 2, 3, \dots $$

Combining with $f = v/\lambda$ and $v=\sqrt{T/\mu}$,

$$ f_n = \frac{n}{2L}\sqrt{\frac{T}{\mu}}, \qquad
f_1 = \frac{1}{2L}\sqrt{\frac{T}{\mu}} $$

Unlike a closed pipe, a string gives **every** harmonic. That is why a plucked
string sounds far richer than a stopped pipe of the same pitch.

```figure caption="The first four modes of a string fixed at both ends. Every harmonic is possible, and the $n$th mode has $n$ loops, $n+1$ nodes and $n$ antinodes."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,4.2))
L, A = 4.0, 0.40
x = np.linspace(0, L, 500)
modes = [(1, 'Fundamental\n(1st harmonic)', '$\\lambda_1=2L$\n$f_1=\\frac{1}{2L}\\sqrt{T/\\mu}$'),
         (2, '1st overtone\n(2nd harmonic)', '$\\lambda_2=L$\n$f_2=2f_1$'),
         (3, '2nd overtone\n(3rd harmonic)', '$\\lambda_3=2L/3$\n$f_3=3f_1$'),
         (4, '3rd overtone\n(4th harmonic)', '$\\lambda_4=L/2$\n$f_4=4f_1$')]
for i, (n, left, right) in enumerate(modes):
    yc = -1.62*i
    env = A*np.sin(n*np.pi*x/L)
    ax.plot(x, yc+env, color=ACCENT, lw=1.8)
    ax.plot(x, yc-env, color=ACCENT, lw=1.8)
    ax.fill_between(x, yc-env, yc+env, color=ACCENT, alpha=0.10)
    ax.plot([0, L], [yc, yc], color=MUTED, lw=0.7, ls=':')
    for m in range(n+1):
        xn = m*L/n
        ax.plot([xn], [yc], 'o', color='#A8271F', ms=4.0, zorder=6)
        if 0 < m < n:
            ax.annotate('N', (xn, yc-A-0.06), ha='center', va='top',
                        color='#A8271F', fontsize=8.3)
    for m in range(n):
        ax.annotate('A', ((2*m+1)*L/(2.0*n), yc+A+0.04), ha='center', va='bottom',
                    color='#0B6A62', fontsize=8.3)
    for xx in (0, L):
        ax.plot([xx, xx], [yc-0.62, yc+0.62], color=INK, lw=2.2)
    ax.annotate(left, (-0.40, yc), ha='right', va='center', color=INK, fontsize=8.4)
    ax.annotate(right, (L+0.30, yc), ha='left', va='center', color=MUTED, fontsize=8.4)
ax.annotate('fixed', (0, 0.80), ha='center', va='bottom', color=MUTED, fontsize=8.2)
ax.annotate('fixed', (L, 0.80), ha='center', va='bottom', color=MUTED, fontsize=8.2)
ax.set_xlim(-2.55, L+1.75); ax.set_ylim(-5.55, 1.30)
ax.axis('off')
```

::: example Worked example 8.3
**Problem.** A sonometer wire 50 cm long has a mass per unit length of
1.0 g m⁻¹ and is stretched by a tension of 160 N. Find the speed of transverse
waves on it, its fundamental frequency, and the frequency of its second overtone.

**Solution.** $\mu = 1.0\ \text{g m}^{-1} = 1.0\times10^{-3}\ \text{kg m}^{-1}$,
$L = 0.50\ \text{m}$, $T = 160\ \text{N}$.

$$ v = \sqrt{\frac{T}{\mu}} = \sqrt{\frac{160}{1.0\times10^{-3}}} = \sqrt{1.6\times10^{5}} = 400\ \text{m s}^{-1} $$
$$ f_1 = \frac{v}{2L} = \frac{400}{2\times0.50} = 400\ \text{Hz} $$

A string gives all harmonics, so the second overtone is the 3rd harmonic:

$$ f_3 = 3f_1 = 1200\ \text{Hz} $$
:::

## 8.6 Laws of vibration of fixed string

Writing $f_1 = \dfrac{1}{2L}\sqrt{\dfrac{T}{\mu}}$ and holding two factors fixed
at a time gives the three laws, all verifiable on a sonometer.

| Law | Statement | Form |
|---|---|---|
| **Law of length** | $f \propto 1/L$ when $T$ and $\mu$ are constant | $fL = $ constant |
| **Law of tension** | $f \propto \sqrt{T}$ when $L$ and $\mu$ are constant | $f/\sqrt{T} = $ constant |
| **Law of mass** | $f \propto 1/\sqrt{\mu}$ when $L$ and $T$ are constant | $f\sqrt{\mu} = $ constant |

Because $\mu = \pi r^{2}\rho$ for a wire of radius $r$ and density $\rho$, the
third law is often split into a **law of diameter** ($f\propto 1/D$) and a **law
of density** ($f\propto 1/\sqrt{\rho}$). Putting $\mu = \pi D^{2}\rho/4$ in the
fundamental gives the compact working form

$$ f_1 = \frac{1}{LD}\sqrt{\frac{T}{\pi\rho}} $$

::: tip Ratio method beats substitution
Almost every exam numerical on these laws is a *ratio* question. Write
$\dfrac{f_2}{f_1} = \dfrac{L_1}{L_2}\sqrt{\dfrac{T_2}{T_1}}\sqrt{\dfrac{\mu_1}{\mu_2}}$
and substitute only the quantities that changed. You never need $v$ or $\mu$ in
absolute terms.
:::

::: example Worked example 8.4
**Problem.** A sonometer wire sounds its fundamental at 256 Hz under a tension
of 100 N. (a) To what value must the tension be raised to make it sound 320 Hz
at the same length? (b) Instead, keeping the tension at 100 N, where should a
bridge be placed on the 60 cm wire to obtain 320 Hz?

**Solution.**

(a) By the law of tension, $f \propto \sqrt{T}$ at constant $L$ and $\mu$:

$$ \frac{T_2}{T_1} = \left(\frac{f_2}{f_1}\right)^{2} = \left(\frac{320}{256}\right)^{2} = (1.25)^{2} = 1.5625 $$
$$ T_2 = 1.5625\times100 = 156.25\ \text{N} $$

(b) By the law of length, $f \propto 1/L$ at constant $T$ and $\mu$:

$$ L_2 = L_1\frac{f_1}{f_2} = 60\times\frac{256}{320} = 60\times0.8 = 48\ \text{cm} $$

The bridge must be set 48 cm from the fixed end — that is, the vibrating length
must be shortened by 12 cm.
:::

## Chapter summary

- A stationary wave forms when incident and reflected waves superpose. Closed end
  → displacement **node**; open end → displacement **antinode**. Adjacent nodes
  are $\lambda/2$ apart.
- **Closed pipe**: $L=(2n-1)\lambda/4$, so $f_n = (2n-1)v/4L$ — odd harmonics
  only. The 1st overtone is the 3rd harmonic.
- **Open pipe**: $L=n\lambda/2$, so $f_n = nv/2L$ — all harmonics. An open pipe
  sounds one octave above a closed pipe of the same length and gives a richer note.
- **End correction** $e = 0.6r$: closed pipe $f_1 = v/4(L+e)$, open pipe
  $f_1 = v/2(L+2e)$.
- Resonance tube: $v = 2f(l_2-l_1)$ and $e = (l_2-3l_1)/2$.
- Transverse waves on a string: $v = \sqrt{T/\mu}$, derived from the centripetal
  force on a curved element.
- String fixed at both ends: $f_n = \dfrac{n}{2L}\sqrt{\dfrac{T}{\mu}}$, all
  harmonics present.
- Laws of a vibrating string: $f\propto 1/L$, $f\propto\sqrt{T}$,
  $f\propto 1/\sqrt{\mu}$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. A closed organ pipe of length $L$ produces harmonics of frequency <span class="marks">[1]</span>
   (a) $nv/2L$ (b) $(2n-1)v/4L$ (c) $nv/4L$ (d) $(2n-1)v/2L$
2. The first overtone of a closed pipe is its <span class="marks">[1]</span>
   (a) 2nd harmonic (b) 3rd harmonic (c) 4th harmonic (d) 5th harmonic
3. If the tension in a stretched string is made four times, its fundamental frequency becomes <span class="marks">[1]</span>
   (a) half (b) twice (c) four times (d) unchanged
4. The end correction of a cylindrical pipe of internal radius $r$ is about <span class="marks">[1]</span>
   (a) $0.3r$ (b) $0.6r$ (c) $r$ (d) $1.2r$
5. At the open end of an organ pipe there is always a <span class="marks">[1]</span>
   (a) displacement node (b) pressure antinode (c) displacement antinode (d) point of zero velocity

::: note Answers to Group A
**1.** (b) — only odd multiples of $v/4L$ fit a node-to-antinode column.
**2.** (b) — the 2nd harmonic is forbidden, so the first tone above the fundamental is $3f_1$.
**3.** (b) — $f\propto\sqrt{T}$ and $\sqrt{4}=2$.
**4.** (b) — Rayleigh's result, $e = 0.6r$.
**5.** (c) — the air is free to move there but cannot change the atmospheric pressure.
:::

**Group B — Short answer (5 marks each)**

1. Show that a closed organ pipe produces only odd harmonics while an open pipe
   of the same length produces all harmonics, and hence compare their fundamental
   frequencies. <span class="marks">[5]</span>
2. What is meant by end correction? In a resonance-tube experiment, show that
   $v = 2f(l_2-l_1)$ and $e = (l_2-3l_1)/2$. <span class="marks">[5]</span>
3. State the three laws of vibration of a stretched string and write the single
   formula from which all three follow. <span class="marks">[5]</span>
4. The third harmonic of a closed pipe has the same frequency as the first
   overtone of an open pipe 50 cm long. Find the length of the closed pipe. <span class="marks">[5]</span>
5. A closed pipe 20 cm long has an internal radius of 2.0 cm. Taking
   $v = 340\ \text{m s}^{-1}$, find its fundamental frequency with and without
   the end correction. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Closed: node at one end, antinode at the other, so $L = (2n-1)\lambda/4$
and $f_n = (2n-1)v/4L$ — odd harmonics. Open: antinodes at both ends, so
$L = n\lambda/2$ and $f_n = nv/2L$ — all harmonics. For the same $L$,
$f_1(\text{open}) = 2f_1(\text{closed})$.

**4.** The first overtone of an open pipe is its 2nd harmonic,
$f = 2\times\dfrac{v}{2L_o} = \dfrac{v}{L_o}$. The third harmonic of a closed
pipe is $f = \dfrac{3v}{4L_c}$. Equating the two,

$$ \frac{3v}{4L_c} = \frac{v}{L_o} \;\Longrightarrow\; L_c = \frac{3L_o}{4} = \frac{3\times0.50}{4} = 0.375\ \text{m} = 37.5\ \text{cm} $$

**5.** Without correction, $f_1 = v/4L = 340/(4\times0.20) = 425\ \text{Hz}$.
With correction, $e = 0.6\times0.020 = 0.012\ \text{m}$, so

$$ f_1 = \frac{340}{4(0.200+0.012)} = \frac{340}{0.848} = 401\ \text{Hz} $$

The correction lowers the predicted note by 24 Hz — about a semitone, which is
easily heard.
:::

**Group C — Long answer (8 marks each)**

1. (a) Derive the expression $v = \sqrt{T/\mu}$ for the speed of a transverse
   wave on a stretched string. <span class="marks">[4]</span>
   (b) Hence obtain the frequencies of the harmonics of a string fixed at both
   ends and state the laws of vibration of a fixed string. <span class="marks">[4]</span>
2. A wire 1.0 m long has a mass per unit length of $5.0\times10^{-3}\ \text{kg m}^{-1}$
   and is stretched by a tension of 200 N.
   (a) Find the speed of transverse waves and the fundamental frequency. <span class="marks">[3]</span>
   (b) What tension would raise the fundamental to 150 Hz? <span class="marks">[3]</span>
   (c) With the original tension restored, where must a bridge be placed to give
   a fundamental of 250 Hz? <span class="marks">[2]</span>

::: note Answer to Group C question 2
(a) $v = \sqrt{T/\mu} = \sqrt{200/(5.0\times10^{-3})} = \sqrt{4.0\times10^{4}}
= 200\ \text{m s}^{-1}$, and

$$ f_1 = \frac{v}{2L} = \frac{200}{2\times1.0} = 100\ \text{Hz} $$

(b) $f\propto\sqrt{T}$, so $T' = T(f'/f_1)^{2} = 200\times(150/100)^{2}
= 200\times2.25 = 450\ \text{N}$.

(c) $f\propto 1/L$, so $L' = L f_1/f' = 1.0\times(100/250) = 0.40\ \text{m}$.
The bridge must be placed 40 cm from one end.
:::
