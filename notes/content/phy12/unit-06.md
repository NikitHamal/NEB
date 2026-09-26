---
subject: Physics
grade: 12
unit: 6
title: Wave motion
hours: 2
area: Waves and Optics
---

Drop a stone in the Phewa lake and rings spread outwards, but a leaf floating on
the surface only bobs up and down — it does not travel with the ring. That is the
whole idea of a wave: the *disturbance* moves, carrying energy with it, while the
matter stays put. This short unit sets up the language and the equation of a
travelling wave, and then shows what happens when two such waves meet head-on.
Everything in Units 7 to 9 is built on it.

::: key What the exam wants from this unit
Be able to write the wave equation $y = a\sin(\omega t - kx)$ and read off $a$,
$f$, $\lambda$ and $v$ from any given form of it; derive the stationary-wave
equation $y = 2a\cos kx\,\sin\omega t$; and list the differences between
progressive and stationary waves.
:::

## 6.1 Progressive waves

::: definition Progressive (travelling) wave
A progressive wave is a disturbance that travels continuously through a medium in
a definite direction, transferring energy and momentum from one point to the
next, **without any net transport of the medium itself**.
:::

A mechanical wave needs a material medium with two properties: *elasticity*, to
provide a restoring force, and *inertia*, to make the displaced particle
overshoot. Light and radio waves are electromagnetic and need no medium; they are
not treated in this unit.

Waves are classified by the direction in which the particles vibrate.

| | Transverse wave | Longitudinal wave |
|---|---|---|
| Particle vibration | perpendicular to propagation | parallel to propagation |
| Form of the wave | crests and troughs | compressions and rarefactions |
| Travels through | solids and liquid surfaces | solids, liquids and gases |
| Can be polarised? | yes | no |
| Examples | wave on a string, ripple, light | sound in air, wave in a spring pushed lengthwise |

```figure caption="A transverse wave has crests and troughs; a longitudinal wave has compressions (C) and rarefactions (R). In both, one wavelength $\lambda$ is the distance between successive identical points."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(2, 1, figsize=(5.0,3.4))
lam = 4.0
ax = axes[0]
x = np.linspace(0, 10, 500); y = 1.0*np.sin(2*np.pi*x/lam)
ax.plot(x, y, color=ACCENT, lw=2.0)
ax.axhline(0, color=MUTED, lw=0.8, ls=':')
ax.annotate('crest',(1.0,1.0),textcoords='offset points',xytext=(-10,6),
            color=INK,fontsize=8.6,ha='center')
ax.annotate('trough',(3.0,-1.0),textcoords='offset points',xytext=(0,-16),
            color=INK,fontsize=8.6,ha='center')
ax.annotate('', xy=(5.0,1.42), xytext=(1.0,1.42),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=1.0, mutation_scale=9))
ax.text(3.0,1.52,r'$\lambda$',ha='center',color=INK,fontsize=9.5)
ax.annotate('', xy=(7.0,1.05), xytext=(7.0,-1.05),
            arrowprops=dict(arrowstyle='<|-|>', color='#2e8b57', lw=1.2, mutation_scale=9))
ax.text(7.0,1.20,'particle motion',color='#2e8b57',fontsize=7.6,ha='center',va='bottom')
ax.annotate('', xy=(10.1,-1.70), xytext=(8.0,-1.70),
            arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.4, mutation_scale=11))
ax.text(9.05,-1.60,'direction of travel',color='#d9534f',fontsize=7.6,ha='center',va='bottom')
ax.set_ylim(-2.3,2.3); ax.set_title('transverse', fontsize=9.2, loc='left')

ax = axes[1]
x0 = np.linspace(0.15, 9.85, 130)
xp = x0 + 0.42*np.sin(2*np.pi*x0/lam)
ax.plot(xp, np.zeros_like(xp)+0.15, '|', color=ACCENT, ms=12, mew=1.1)
for xc,lab,col in [(2.0,'C','#d9534f'),(6.0,'C','#d9534f'),
                   (4.0,'R',ACCENT),(8.0,'R',ACCENT)]:
    ax.text(xc,-0.34,lab,ha='center',va='top',color=col,fontsize=9)
ax.annotate('', xy=(6.0,0.92), xytext=(2.0,0.92),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=1.0, mutation_scale=9))
ax.text(4.0,1.04,r'$\lambda$',ha='center',color=INK,fontsize=9.5)
ax.annotate('', xy=(9.35,0.55), xytext=(8.25,0.55),
            arrowprops=dict(arrowstyle='<|-|>', color='#2e8b57', lw=1.2, mutation_scale=9))
ax.text(8.80,0.64,'particle motion',color='#2e8b57',fontsize=7.6,ha='center',va='bottom')
ax.set_ylim(-1.05,1.55); ax.set_title('longitudinal', fontsize=9.2, loc='left')
for ax in axes:
    ax.set_xlim(-0.2,10.6); ax.set_xticks([]); ax.set_yticks([]); ax.axis('off')
fig.subplots_adjust(hspace=0.35)
```

Five quantities describe any progressive wave:

- **Amplitude** $a$ — the maximum displacement of a particle from its mean
  position.
- **Wavelength** $\lambda$ — the distance between two successive particles in the
  same phase (crest to crest, or compression to compression).
- **Period** $T$ — the time for one complete vibration of a particle.
- **Frequency** $f = 1/T$ — vibrations per second, in hertz.
- **Wave velocity** $v$ — the speed at which the disturbance advances.

In one period the wave advances exactly one wavelength, so

$$ v = \frac{\lambda}{T} = f\lambda $$

This **wave equation** holds for every wave, mechanical or electromagnetic. In a
given medium $v$ is fixed by the medium's elasticity and density, so changing the
frequency of the source changes the wavelength, not the speed.

Two further facts are worth remembering: in a progressive wave **every** particle
vibrates with the same amplitude and frequency, and each particle starts its
vibration slightly later than the one before it — the phase lags steadily behind
along the direction of travel.

## 6.2 Mathematical description of a wave

Let the particle at the origin perform SHM, $y = a\sin\omega t$. A wave moving in
the $+x$ direction with speed $v$ reaches a particle at distance $x$ after a
delay $t' = x/v$, so that particle simply repeats what the origin did $x/v$
seconds earlier:

$$ y = a\sin\omega\left(t - \frac{x}{v}\right) $$

::: derivation The standard forms of the wave equation
Putting $\omega = 2\pi/T$ and $v = \lambda/T$ into the expression above,

$$ y = a\sin\frac{2\pi}{T}\left(t - \frac{x}{v}\right)
 = a\sin 2\pi\left(\frac{t}{T} - \frac{x}{\lambda}\right) $$

Defining the **angular frequency** $\omega = 2\pi/T$ and the **propagation
constant** (or wave number) $k = 2\pi/\lambda$, this becomes

$$ y = a\sin(\omega t - kx), \qquad v = \frac{\omega}{k} $$

An equivalent form often quoted in NEB papers is

$$ y = a\sin\frac{2\pi}{\lambda}(vt - x) $$

For a wave travelling in the $-x$ direction, replace $x$ by $-x$:
$y = a\sin(\omega t + kx)$.
:::

The quantity $(\omega t - kx)$ is the **phase**. Two particles separated by a path
difference $\Delta x$ differ in phase by

$$ \Delta\phi = \frac{2\pi}{\lambda}\,\Delta x $$

so a separation of one whole wavelength means a phase difference of $2\pi$ (the
particles are in step), and a separation of $\lambda/2$ means $\pi$ (exactly out
of step).

```figure caption="Left: a snapshot at one instant, where the repeat distance is the wavelength $\lambda$. Right: the motion of one particle in time, whose repeat interval is the period $T$."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(5.0,2.6))
ax = axes[0]
x = np.linspace(0, 9, 400)
ax.plot(x, np.sin(2*np.pi*x/4.0), color=ACCENT, lw=2.0)
ax.annotate('', xy=(5.0,1.30), xytext=(1.0,1.30),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=1.0, mutation_scale=9))
ax.text(3.0,1.40,r'$\lambda$',ha='center',color=INK,fontsize=10)
ax.set_xlabel('distance  $x$'); ax.set_ylabel('displacement  $y$')
ax.set_title('snapshot: $y$ against $x$  (fixed $t$)', fontsize=8.4)
ax = axes[1]
t = np.linspace(0, 9, 400)
ax.plot(t, np.sin(2*np.pi*t/3.0), color='#d9534f', lw=2.0)
ax.annotate('', xy=(3.75,1.30), xytext=(0.75,1.30),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=1.0, mutation_scale=9))
ax.text(2.25,1.40,'$T$',ha='center',color=INK,fontsize=10)
ax.set_xlabel('time  $t$')
ax.set_title('history: $y$ against $t$  (fixed $x$)', fontsize=8.4)
for ax in axes:
    ax.axhline(0, color=MUTED, lw=0.8, ls=':')
    ax.set_ylim(-1.75,1.85); ax.set_xticks([]); ax.set_yticks([])
    ax.spines[['top','right']].set_visible(False)
fig.subplots_adjust(wspace=0.22)
```

Differentiating $y$ with respect to time at a fixed $x$ gives the **particle
velocity**:

$$ v_p = \frac{\partial y}{\partial t} = a\omega\cos(\omega t - kx),
\qquad (v_p)_{\max} = a\omega $$

::: caution Particle velocity is not wave velocity
The wave velocity $v = f\lambda$ is a constant property of the medium. The
particle velocity $v_p = a\omega\cos(\omega t - kx)$ changes from instant to
instant, is zero at the crests and troughs and greatest at the mean position.
Differentiating $y$ with respect to $x$ instead gives the slope of the curve, and
the two are linked by $v_p = -v\,(\partial y/\partial x)$.
:::

::: example Worked example 6.1
**Problem.** A progressive wave is given by
$y = 0.05\sin(100\pi t - 0.5\pi x)$, all quantities in SI units. Find the
amplitude, frequency, wavelength, wave speed and maximum particle velocity.

**Solution.** Comparing with $y = a\sin(\omega t - kx)$:
$a = 0.05\ \text{m}$, $\omega = 100\pi\ \text{rad s}^{-1}$,
$k = 0.5\pi\ \text{rad m}^{-1}$.

$$ f = \frac{\omega}{2\pi} = \frac{100\pi}{2\pi} = 50\ \text{Hz},
\qquad \lambda = \frac{2\pi}{k} = \frac{2\pi}{0.5\pi} = 4\ \text{m} $$

$$ v = \frac{\omega}{k} = \frac{100\pi}{0.5\pi} = 200\ \text{m s}^{-1} $$

Check: $f\lambda = 50 \times 4 = 200\ \text{m s}^{-1}$. Finally

$$ (v_p)_{\max} = a\omega = 0.05 \times 100\pi = 15.7\ \text{m s}^{-1} $$
:::

::: example Worked example 6.2
**Problem.** A sound wave of frequency $500\ \text{Hz}$ travels through air at
$350\ \text{m s}^{-1}$. Find its wavelength and the phase difference between two
points $0.175\ \text{m}$ apart along the direction of travel.

**Solution.**

$$ \lambda = \frac{v}{f} = \frac{350}{500} = 0.7\ \text{m} $$

$$ \Delta\phi = \frac{2\pi}{\lambda}\Delta x
 = \frac{2\pi}{0.7} \times 0.175 = 2\pi \times 0.25 = \frac{\pi}{2}\ \text{rad} $$

That is $90^{\circ}$ — the two points are a quarter of a wavelength apart, so one
is at a crest when the other is at its mean position.
:::

## 6.3 Stationary waves

When two progressive waves of the **same amplitude, frequency and speed** travel
along the same line in **opposite directions**, they superpose to give a wave that
does not travel at all. This is a **stationary** (or standing) wave. In practice
the second wave is usually the reflection of the first from a fixed end — a
plucked sarangi string, or the air column in a flute.

::: derivation Equation of a stationary wave
Let the incident wave travelling in the $+x$ direction and the reflected wave
travelling in the $-x$ direction be

$$ y_1 = a\sin(\omega t - kx), \qquad y_2 = a\sin(\omega t + kx) $$

By the principle of superposition the resultant displacement is
$y = y_1 + y_2$. Using $\sin C + \sin D = 2\sin\frac{C+D}{2}\cos\frac{C-D}{2}$
with $C = \omega t + kx$ and $D = \omega t - kx$,

$$ y = 2a\cos kx\,\sin\omega t
 = \left[2a\cos\frac{2\pi x}{\lambda}\right]\sin\frac{2\pi t}{T} $$

This is **not** of the form $f(vt - x)$: the $x$ and $t$ dependences have
separated, so nothing travels. Each particle performs SHM of period $T$, but with
an amplitude

$$ A = 2a\cos\frac{2\pi x}{\lambda} $$

that depends on where the particle is.
:::

The amplitude $A$ vanishes at some points and is maximum at others.

**Nodes** are points of permanently zero displacement, where
$\cos(2\pi x/\lambda) = 0$:

$$ \frac{2\pi x}{\lambda} = (2n+1)\frac{\pi}{2}
\;\Longrightarrow\; x = \frac{\lambda}{4},\ \frac{3\lambda}{4},\ \frac{5\lambda}{4},\ \ldots $$

**Antinodes** are points of maximum amplitude $2a$, where
$\cos(2\pi x/\lambda) = \pm 1$:

$$ x = 0,\ \frac{\lambda}{2},\ \lambda,\ \frac{3\lambda}{2},\ \ldots $$

So successive nodes are $\lambda/2$ apart, successive antinodes are $\lambda/2$
apart, and a node and the next antinode are $\lambda/4$ apart. Measuring the
distance between two nodes is therefore the standard laboratory way of finding a
wavelength.

If the origin is chosen at a *node* instead of an antinode, the same superposition
gives $y = 2a\sin kx\,\cos\omega t$. Only the labelling has changed: the nodes
are then at $x = 0, \lambda/2, \lambda,\ldots$ and the antinodes midway between
them. The spacings $\lambda/2$ and $\lambda/4$ are the same either way.

```figure caption="A stationary wave at several instants. The nodes N never move; the antinodes A swing between $+2a$ and $-2a$. Successive nodes are $\lambda/2$ apart."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.8))
lam = 4.0
x = np.linspace(0, 9, 600)
env = 2*np.cos(2*np.pi*x/lam)
ax.plot(x, env, color=MUTED, lw=1.0, ls=(0,(4,3)))
ax.plot(x, -env, color=MUTED, lw=1.0, ls=(0,(4,3)))
for s, alpha, lw in [(1.0,1.0,2.0), (0.71,0.55,1.3), (0.38,0.40,1.1),
                     (-0.71,0.55,1.3), (-1.0,0.9,1.6)]:
    ax.plot(x, env*s, color=ACCENT if s > 0 else '#d9534f', lw=lw, alpha=alpha)
ax.axhline(0, color=INK, lw=0.9)
for xn in [1.0, 3.0, 5.0, 7.0]:
    ax.plot([xn],[0],'o',color=INK,ms=5,zorder=6)
    ax.text(xn, -0.42, 'N', ha='center', va='top', color=INK, fontsize=9)
for xa in [0.0, 2.0, 4.0, 6.0, 8.0]:
    ax.text(xa, 2.30, 'A', ha='center', color='#2e8b57', fontsize=9)
ax.annotate('', xy=(3.0,-2.72), xytext=(1.0,-2.72),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=1.0, mutation_scale=9))
ax.text(2.0,-3.18,r'$\lambda/2$',ha='center',va='top',color=INK,fontsize=9.5)
ax.set_xlim(-0.35,9.35); ax.set_ylim(-3.9,2.95)
ax.set_xlabel('distance  $x$'); ax.set_xticks([]); ax.set_yticks([])
ax.set_ylabel('displacement  $y$')
ax.spines[['top','right','bottom']].set_visible(False)
```

| | Progressive wave | Stationary wave |
|---|---|---|
| Disturbance | advances through the medium | confined between the boundaries |
| Energy | transported along the wave | not transported; only exchanged locally |
| Amplitude | same for every particle | varies from $0$ at nodes to $2a$ at antinodes |
| Phase | changes continuously with $x$ | same for all particles between two nodes; reverses across a node |
| Nodes and antinodes | none | present, spaced $\lambda/2$ apart |
| Particle at rest | no particle is permanently at rest | particles at the nodes never move |

::: example Worked example 6.3
**Problem.** A stationary wave on a string is described by
$y = 4\sin(0.5\pi x)\cos(200\pi t)$, where $y$ and $x$ are in centimetres and $t$
in seconds. Find (a) the amplitude of the two component waves, (b) the
wavelength, (c) the frequency, (d) the wave speed, and (e) the distance between
successive nodes.

**Solution.** Compare with $y = 2a\sin kx\cos\omega t$.

(a) $2a = 4\ \text{cm}$, so each component wave has amplitude
$a = 2\ \text{cm}$.

(b) $k = 0.5\pi\ \text{cm}^{-1}$, so
$\lambda = 2\pi/k = 2\pi/0.5\pi = 4\ \text{cm}$.

(c) $\omega = 200\pi\ \text{rad s}^{-1}$, so
$f = \omega/2\pi = 100\ \text{Hz}$.

(d) $v = f\lambda = 100 \times 0.04 = 4\ \text{m s}^{-1}$.

(e) Successive nodes are $\lambda/2 = 2\ \text{cm}$ apart; here $\sin(0.5\pi x)=0$
gives $x = 0, 2, 4, 6\ \text{cm}$, confirming the spacing.
:::

## Chapter summary

- A progressive wave carries energy and momentum through a medium without
  carrying the medium. Transverse waves vibrate perpendicular to the direction of
  travel, longitudinal waves parallel to it.
- $v = f\lambda = \lambda/T$ for every wave; in a given medium $v$ is fixed, so
  raising $f$ shortens $\lambda$.
- Wave equation: $y = a\sin(\omega t - kx) = a\sin 2\pi(t/T - x/\lambda)$, with
  $\omega = 2\pi/T$, $k = 2\pi/\lambda$ and $v = \omega/k$. Use $+kx$ for a wave
  travelling in the $-x$ direction.
- Phase difference and path difference are linked by
  $\Delta\phi = (2\pi/\lambda)\Delta x$.
- Particle velocity $v_p = a\omega\cos(\omega t - kx)$, maximum $a\omega$; it is
  not the wave velocity.
- Two identical waves travelling in opposite directions superpose to give a
  stationary wave, $y = 2a\cos kx\,\sin\omega t$, whose amplitude
  $2a\cos(2\pi x/\lambda)$ depends on position.
- Nodes (zero amplitude) lie at $x = \lambda/4, 3\lambda/4, \ldots$ and antinodes
  (amplitude $2a$) at $x = 0, \lambda/2, \lambda, \ldots$. Successive nodes are
  $\lambda/2$ apart and a node is $\lambda/4$ from the nearest antinode.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The distance between two consecutive nodes of a stationary wave is <span class="marks">[1]</span>
   (a) $\lambda$ (b) $\lambda/2$ (c) $\lambda/4$ (d) $2\lambda$
2. For the wave $y = a\sin(\omega t - kx)$, the speed of the wave is <span class="marks">[1]</span>
   (a) $\omega k$ (b) $\omega/k$ (c) $k/\omega$ (d) $a\omega$
3. Two points in a progressive wave are $\lambda/4$ apart. Their phase difference is <span class="marks">[1]</span>
   (a) $\pi/4$ (b) $\pi/2$ (c) $\pi$ (d) $2\pi$
4. Sound waves travelling through air are <span class="marks">[1]</span>
   (a) transverse (b) longitudinal (c) electromagnetic (d) always stationary
5. In a stationary wave, the net energy transported across a node is <span class="marks">[1]</span>
   (a) maximum (b) zero (c) equal to $2a$ (d) proportional to $f$

::: note Answers to Group A
**1.** (b) — nodes occur at $x = \lambda/4, 3\lambda/4, \ldots$, spaced $\lambda/2$ apart.
**2.** (b) — $v = \omega/k = (2\pi/T)(\lambda/2\pi) = \lambda/T$.
**3.** (b) — $\Delta\phi = (2\pi/\lambda)(\lambda/4) = \pi/2$.
**4.** (b) — air has no shear elasticity, so it can carry only longitudinal waves.
**5.** (b) — a node never moves, so no energy crosses it; energy is only exchanged
between neighbouring nodes.
:::

**Group B — Short answer (5 marks each)**

1. What is a progressive wave? Derive the expression
   $y = a\sin\dfrac{2\pi}{\lambda}(vt - x)$ for a wave travelling along the
   positive $x$ direction. <span class="marks">[5]</span>
2. Distinguish between progressive and stationary waves, giving any five points
   of difference. <span class="marks">[5]</span>
3. A transverse wave is represented by $y = 0.03\sin(40\pi t - 0.2\pi x)$ in SI
   units. Find its amplitude, frequency, wavelength, speed and maximum particle
   velocity. <span class="marks">[5]</span>
4. A stationary wave is given by $y = 5\sin(0.4\pi x)\cos(100\pi t)$, with $y$ and
   $x$ in centimetres. Find the wavelength, frequency, wave speed and the
   distance between a node and the next antinode. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** See §6.2: the particle at $x$ repeats the motion of the origin after a
delay $x/v$, so $y = a\sin\omega(t - x/v)$; substituting $\omega = 2\pi/T$ and
$v = \lambda/T$ gives the required form.

**2.** Any five rows of the comparison table in §6.3.

**3.** $a = 0.03\ \text{m}$; $\omega = 40\pi$, so $f = 20\ \text{Hz}$;
$k = 0.2\pi$, so $\lambda = 2\pi/0.2\pi = 10\ \text{m}$;
$v = \omega/k = 40\pi/0.2\pi = 200\ \text{m s}^{-1}$ (check: $f\lambda = 20\times10$);
$(v_p)_{\max} = a\omega = 0.03\times40\pi = 3.77\ \text{m s}^{-1}$.

**4.** $k = 0.4\pi\ \text{cm}^{-1}$, so $\lambda = 2\pi/0.4\pi = 5\ \text{cm}$;
$\omega = 100\pi$, so $f = 50\ \text{Hz}$;
$v = f\lambda = 50 \times 0.05 = 2.5\ \text{m s}^{-1}$; node to next antinode
$= \lambda/4 = 1.25\ \text{cm}$.
:::

**Group C — Long answer (8 marks each)**

1. Explain how a stationary wave is formed. Derive its equation by superposing
   two identical progressive waves travelling in opposite directions, and hence
   obtain the positions of the nodes and antinodes. Show that successive nodes
   are half a wavelength apart. <span class="marks">[8]</span>
2. A progressive wave of frequency $250\ \text{Hz}$ and amplitude $2\ \text{cm}$
   travels along a stretched string at $400\ \text{m s}^{-1}$.
   (a) Find its wavelength and period. <span class="marks">[2]</span>
   (b) Find the phase difference and the time lag between two points
   $0.4\ \text{m}$ apart. <span class="marks">[3]</span>
   (c) Write the equation of the wave, and find the maximum particle velocity. <span class="marks">[3]</span>

::: note Answer to Group C question 2
(a) $\lambda = v/f = 400/250 = 1.6\ \text{m}$ and
$T = 1/f = 4\times10^{-3}\ \text{s} = 4\ \text{ms}$.

(b) $\Delta\phi = (2\pi/\lambda)\Delta x = (2\pi/1.6)(0.4) = \pi/2\ \text{rad}
= 90^{\circ}$. The time lag is
$\Delta t = \Delta x/v = 0.4/400 = 1\times10^{-3}\ \text{s} = 1\ \text{ms}$,
which is indeed $T/4$.

(c) $\omega = 2\pi f = 500\pi\ \text{rad s}^{-1}$ and
$k = 2\pi/\lambda = 2\pi/1.6 = 1.25\pi\ \text{rad m}^{-1}$, so

$$ y = 0.02\sin(500\pi t - 1.25\pi x)\ \text{m} $$

$(v_p)_{\max} = a\omega = 0.02 \times 500\pi = 10\pi = 31.4\ \text{m s}^{-1}$.
:::
