---
subject: Physics
grade: CEE
unit: 11
title: Waves and Sound
hours: 3
area: Waves and Optics
---

Sound is the wave you can hear, and almost every question on it is a ratio or a
sign. The Waves and Optics area carries **8 of the 50 Physics questions** (official
MEC weightage), and we estimate about **3** of them come from this chapter. They
cluster on five things: reading $y = A\sin(\omega t - kx)$, the speed of sound in a
gas, the harmonic series of a pipe, the decibel, and the Doppler formula — with the
sign in the Doppler formula the single most common place to lose the mark.

::: key What the paper asks from this chapter
- $y = A\sin(\omega t - kx)$: read off $A$, $\omega$, $k$, then $f = \omega/2\pi$, $\lambda = 2\pi/k$, $v = \omega/k = f\lambda$.
- Particle velocity against wave velocity: $v_p = -v\times(\text{slope of the wave profile})$; maximum particle speed $A\omega$, not $v$.
- $v = \sqrt{\gamma P/\rho} = \sqrt{\gamma RT/M}$: independent of pressure, $v \propto \sqrt{T}$, $v \propto 1/\sqrt{M}$; solids $\sqrt{Y/\rho}$, liquids $\sqrt{B/\rho}$.
- Strings: $f = \frac{n}{2L}\sqrt{T/\mu}$. Open pipe: all harmonics, $f_n = nv/2L$. Closed pipe: odd harmonics only, $f_n = (2n-1)v/4L$.
- Intensity $I = 2\pi^2\rho v f^2A^2 = p_m^2/2\rho v$; $I \propto 1/r^2$; $L = 10\log_{10}(I/I_0)$ with $I_0 = 10^{-12}\ \text{W m}^{-2}$.
- Doppler: $f' = f\frac{v \pm v_o}{v \mp v_s}$ — upper sign for approach; the source in the denominator, the observer in the numerator.
- Beats: $f_b = |f_1 - f_2|$; beats are heard only when the two frequencies are close.
:::

## 11.1 Progressive waves and the wave equation

A **wave** is a disturbance that carries energy and momentum from one place to
another **without carrying matter**. A **mechanical wave** needs a material medium
(sound, waves on a string, ripples); an **electromagnetic wave** does not (light,
radio). In a **transverse** wave the particles vibrate perpendicular to the
direction of travel; in a **longitudinal** wave they vibrate along it.

| | Transverse | Longitudinal |
|---|---|---|
| Particle motion | perpendicular to the wave direction | parallel to the wave direction |
| Form | crests and troughs | compressions and rarefactions |
| Can be polarized | yes | no |
| Can travel in a solid | yes | yes |
| Can travel in a liquid or gas | no (no shear) | yes |
| Examples | light, wave on a string, ripple | sound in air, sound in steel |

Sound in air is longitudinal: the air layers vibrate back and forth along the
direction the sound travels, producing alternate regions of high pressure
(**compression**) and low pressure (**rarefaction**).

### The wave quantities

| Quantity | Symbol | Definition | SI unit |
|---|---|---|---|
| Amplitude | $A$ | maximum displacement of a particle from its mean position | m |
| Wavelength | $\lambda$ | distance between two nearest particles in the same phase | m |
| Frequency | $f$ | number of complete waves passing a point per second | Hz |
| Period | $T$ | time for one complete wave; $T = 1/f$ | s |
| Wave speed | $v$ | distance travelled by a given phase per second | m s⁻¹ |
| Angular frequency | $\omega$ | $\omega = 2\pi f = 2\pi/T$ | rad s⁻¹ |
| Angular wave number | $k$ | $k = 2\pi/\lambda$ | rad m⁻¹ |

One complete wave passes a point in one period and occupies one wavelength, so

$$ v = f\lambda = \frac{\omega}{k} $$

### The progressive wave equation

For a wave of amplitude $A$ travelling in the **positive $x$ direction**,

$$ y = A\sin(\omega t - kx) $$

Every symbol: $y$ is the displacement of the particle at position $x$ at time $t$;
$A$ is the amplitude; $\omega = 2\pi f$ is the angular frequency; $k = 2\pi/\lambda$
is the angular wave number; and $(\omega t - kx)$ is the **phase** of that particle,
measured in radians.

Why the minus sign means "towards $+x$": follow a point of constant phase. If
$\omega t - kx = $ constant, then differentiating gives $\omega - k\,dx/dt = 0$, so
$dx/dt = \omega/k = v > 0$ — the phase pattern moves to the right. With a plus sign,
$y = A\sin(\omega t + kx)$, the same argument gives $dx/dt = -v$: the wave travels
towards $-x$. $y = A\sin(kx - \omega t)$ is the same wave as the first, since
$\sin(-\theta) = -\sin\theta$ only flips the sign of $y$.

**Phase difference.** Two points a distance $\Delta x$ apart differ in phase by
$\Delta\phi = \frac{2\pi}{\lambda}\Delta x$; one point at two times $\Delta t$ apart
differs by $\frac{2\pi}{T}\Delta t$. A path difference of $\lambda$ is a phase
difference of $2\pi$; a path difference of $\lambda/2$ is $\pi$.

### Particle velocity is not wave velocity

This is the single most examined distinction in the chapter. Differentiate
$y = A\sin(\omega t - kx)$:

$$ v_p = \frac{\partial y}{\partial t} = A\omega\cos(\omega t - kx) $$

and the **slope** of the wave profile at that instant is

$$ \frac{\partial y}{\partial x} = -Ak\cos(\omega t - kx) $$

Dividing, $\dfrac{\partial y/\partial t}{\partial y/\partial x} = -\dfrac{\omega}{k} = -v$, so

$$ v_p = -v \times \text{slope of the wave profile} $$

The minus sign is the physics: where the profile slopes **up** to the right, the
particle is moving **down**, because the wave is arriving from the left and the
crest has not reached it yet.

| | Wave speed $v$ | Particle speed $v_p$ |
|---|---|---|
| What moves | the phase pattern (energy) | the medium's particles |
| Value | $\omega/k$, fixed by the medium | $A\omega\cos(\omega t - kx)$, changes with time |
| Maximum | $v$ | $A\omega$ |
| Direction | along the wave | along the vibration (perpendicular for a transverse wave) |
| Depends on | medium only | amplitude and frequency as well |

The ratio of the two maxima is $\dfrac{A\omega}{v} = Ak = \dfrac{2\pi A}{\lambda}$ —
usually a small number. In a sound wave in air the particles move a few millimetres
per second while the wave moves at 340 m s⁻¹.

```figure caption="A progressive wave at two instants, one eighth of a period apart. The pattern has moved to the right by $\lambda/8$. At the marked point the profile slopes upward, so by $v_p = -v\times\text{slope}$ the particle there is moving downward."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.8))
lam, A = 2.0, 1.0
x = np.linspace(0, 4.0, 600)
ax.axhline(0, color=MUTED, lw=0.7)
ax.plot(x, A*np.sin(2*np.pi*x/lam), color=ACCENT, lw=1.9, label='t = 0')
ax.plot(x, A*np.sin(2*np.pi*x/lam - np.pi/4), color=SERIES[1], lw=1.9,
        ls=(0,(5,2)), label='t = T/8')
ax.annotate('', xy=(2.5,1.30), xytext=(0.5,1.30),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=0.9, mutation_scale=8))
ax.text(1.5, 1.40, r'$\lambda$', ha='center', va='bottom', fontsize=10)
ax.annotate('', xy=(2.25,0.02), xytext=(2.25,0.68),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[2], lw=1.5, mutation_scale=10))
ax.text(2.33, -0.30, r'$v_p$ is downward here', fontsize=8.5, color=SERIES[2],
        ha='left', va='top')
ax.annotate('', xy=(3.85,1.62), xytext=(3.05,1.62),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.2, mutation_scale=9))
ax.text(2.98, 1.62, 'wave travels +x', fontsize=8, color=MUTED, ha='right', va='center')
ax.set_xlim(-0.1, 4.1); ax.set_ylim(-1.55, 1.85)
ax.set_xlabel('position  x  (m)'); ax.set_ylabel('displacement  y')
ax.set_yticks([-1,0,1])
ax.spines[['top','right']].set_visible(False)
ax.legend(loc='lower left', fontsize=8, frameon=False, ncol=2, bbox_to_anchor=(0.0,0.0))
```

::: example Worked example 11.1 — reading a wave equation
**Problem.** A wave is described by $y = 0.02\sin(100t - 2x)$ (SI units). Find its
amplitude, frequency, wavelength, speed and maximum particle speed.

**Solution.** Compare with $y = A\sin(\omega t - kx)$: $A = 0.02$ m, $\omega = 100$
rad s⁻¹, $k = 2$ rad m⁻¹.
$f = \omega/2\pi = 100/6.28 = 15.9$ Hz; $\lambda = 2\pi/k = 3.14$ m;
$v = \omega/k = 50$ m s⁻¹. Maximum particle speed $= A\omega = 0.02\times100 =
2$ m s⁻¹.
:::

::: caution Three traps in the wave equation
1. $\omega$ is **not** the frequency; $f = \omega/2\pi$.
2. The particle speed is **not** the wave speed. Here the wave crosses 50 m every
   second while a particle never moves faster than 2 m s⁻¹.
3. In $y = A\sin(\omega t - kx)$ the coefficient of $t$ is $\omega$ and the
   coefficient of $x$ is $k$ — but only if the equation is written that way. If the
   bracket is $(kx - \omega t)$ the coefficients swap places, and $v = \omega/k$
   still, not $k/\omega$.
:::

### Superposition and reflection

The **principle of superposition** states that when two or more waves arrive at a
point, the resultant displacement is the algebraic sum of the separate
displacements. Waves pass through one another unchanged.

When a wave meets a boundary:

- at a **rigid (fixed) end** it reflects with a phase change of $\pi$ — a crest
  comes back as a trough, and the displacement at the boundary is always zero;
- at a **free (open) end** it reflects with no phase change — a crest comes back as
  a crest, and the displacement at the boundary is maximum.

This difference is exactly why a string fixed at both ends and a pipe open at both
ends have different harmonic series, and why a pipe closed at one end has none of
the even harmonics.

## 11.2 Speed of sound in solids, liquids and gases

Sound is an elastic wave, so its speed is fixed by two properties of the medium:
how **stiff** it is (the elastic modulus $E$) and how **heavy** it is (the density
$\rho$):

$$ v = \sqrt{\frac{E}{\rho}} $$

Stiffness pushes the disturbed layer back quickly; inertia slows it down. That one
formula explains every comparison in the table below.

| Medium | Modulus to use | Formula | Typical speed (m s⁻¹) |
|---|---|---|---|
| Solid (long thin rod) | Young's modulus $Y$ | $v = \sqrt{Y/\rho}$ | steel 5000, aluminium 5100, glass 5000 |
| Liquid | Bulk modulus $B$ | $v = \sqrt{B/\rho}$ | water 1480 (20 °C), sea water 1530 |
| Gas | Bulk modulus, adiabatic | $v = \sqrt{\gamma P/\rho}$ | air 331 (0 °C), 343 (20 °C) |

Solids are fastest because their elastic moduli are enormous compared with their
densities; gases are slowest because a gas is easy to squeeze.

### Newton's value and Laplace's correction

::: derivation Laplace's correction to the speed of sound
Start from $v = \sqrt{B/\rho}$ and ask what the bulk modulus of a gas actually is.

**Step 1 — Newton's assumption.** Newton supposed the compressions and rarefactions
pass so gently that the temperature stays constant. Then Boyle's law holds,
$PV = $ constant, and the bulk modulus is just the pressure: $B = P$.

**Step 2 — the number it gives.** At STP, $P = 1.013\times10^5$ Pa and
$\rho = 1.293$ kg m⁻³, so $v = \sqrt{1.013\times10^5/1.293} = 280$ m s⁻¹. The
measured value is 331 m s⁻¹ — 15 % higher. Newton's formula fails.

**Step 3 — Laplace's correction.** A sound wave compresses and rarefies the air
hundreds of times a second. Heat has no time to flow from a compression to the
neighbouring rarefaction, so the process is **adiabatic**, not isothermal:
$PV^{\gamma} = $ constant, with $\gamma = C_P/C_V$.

**Step 4 — the adiabatic bulk modulus.** Differentiate:
$\gamma P V^{\gamma-1}\,dV + V^{\gamma}\,dP = 0$, so
$\dfrac{dP}{dV} = -\gamma\dfrac{P}{V}$ and
$B = -V\dfrac{dP}{dV} = \gamma P$.

**Step 5 — the result.**
$$ v = \sqrt{\frac{\gamma P}{\rho}} = \sqrt{\frac{1.4\times1.013\times10^5}{1.293}} = 331\ \text{m s}^{-1} $$

**Step 6 — the working form.** For one mole, $P = \rho RT/M$, so
$$ v = \sqrt{\frac{\gamma RT}{M}} $$

**What it means.** Sound travels faster in a gas that is lighter (smaller $M$) or
hotter (larger $T$), and the ratio $\gamma$ matters: monatomic gases ($\gamma = 1.67$)
beat diatomic ones ($\gamma = 1.4$) at the same temperature and molar mass.
:::

::: tip The examiner is looking for
The words **adiabatic**, $PV^{\gamma}$ = constant, $B = \gamma P$, and the final
$\sqrt{\gamma P/\rho}$. A derivation that says "Laplace assumed adiabatic" without
producing $B = \gamma P$ loses the marks that carry the result.
:::

### The factors that change the speed of sound

| Factor | Effect on $v$ in a gas | Reason |
|---|---|---|
| Temperature | increases; $v \propto \sqrt{T}$ (kelvin) | $v = \sqrt{\gamma RT/M}$ |
| Pressure | **none**, at constant temperature | $\rho \propto P$, so $P/\rho$ is unchanged |
| Molar mass | decreases as $M$ rises; $v \propto 1/\sqrt{M}$ | lighter gas, faster sound |
| Humidity | increases slightly in air | water vapour ($M = 18$) is lighter than air ($M \approx 29$) |
| Wind | adds vectorially to $v$ | the medium itself is moving |
| Frequency | none (in air, over the audible range) | air is non-dispersive for sound |
| Amplitude | none, for ordinary sounds | small-amplitude elasticity is linear |

Near 0 °C, $v = 331\sqrt{1 + t/273} \approx 331 + 0.61t$, so the speed rises by
about **0.61 m s⁻¹ for each °C**.

::: caution Pressure does not change the speed of sound
Doubling the pressure of a gas at constant temperature doubles its density too, and
$P/\rho$ stays the same. Students who answer "it increases" are thinking of the
density alone. Temperature is the variable that matters, and it must be in kelvin:
going from 27 °C to 54 °C does **not** double the speed — $T$ goes from 300 K to
327 K, and $v$ rises by only $\sqrt{327/300} = 1.04$, about 4 %.
:::

::: example Worked example 11.2 — speed at a hill station
**Problem.** The speed of sound in air at 0 °C is 331 m s⁻¹. Find it at 27 °C.

**Solution.** $v \propto \sqrt{T}$ with $T$ in kelvin:
$v = 331\sqrt{\dfrac{273+27}{273}} = 331\sqrt{\dfrac{300}{273}} = 331(1.048) =
347$ m s⁻¹.
The temperature has risen by 10 % in kelvin, so the speed rises by about 5 % — the
square root halves the effect.
:::

::: example Worked example 11.3 — comparing two gases
**Problem.** Find the ratio of the speed of sound in hydrogen ($M = 2$ g mol⁻¹) to
that in oxygen ($M = 32$ g mol⁻¹) at the same temperature.

**Solution.** Both are diatomic, so $\gamma$ is the same and cancels:
$\dfrac{v_{H_2}}{v_{O_2}} = \sqrt{\dfrac{M_{O_2}}{M_{H_2}}} = \sqrt{\dfrac{32}{2}} = 4$.
Sound travels four times faster in hydrogen.
:::

## 11.3 Stationary waves: harmonics and overtones in strings and pipes

### How a stationary wave is made

Send a wave along a string and let it reflect at the fixed end. The incident and
reflected waves have the same amplitude and frequency and travel in opposite
directions, so they superpose:

$$ y = A\sin(\omega t - kx) + A\sin(\omega t + kx) = 2A\sin(kx)\cos(\omega t) $$

The result is a **stationary (standing) wave**. It is no longer a travelling wave:
the $x$ and $t$ parts have separated, so every particle vibrates with the same
frequency $\cos(\omega t)$ but with an amplitude $2A\sin(kx)$ that depends on where
it is.

| Feature | Where | What happens there |
|---|---|---|
| **Node** | $\sin(kx) = 0$, i.e. $x = 0, \lambda/2, \lambda,\dots$ | permanently at rest |
| **Antinode** | $\sin(kx) = \pm1$, i.e. $x = \lambda/4, 3\lambda/4,\dots$ | vibrates with amplitude $2A$ |

Distance between two neighbouring nodes $= \lambda/2$; between a node and the next
antinode $= \lambda/4$. All particles between two consecutive nodes vibrate **in
phase**; particles in adjacent loops vibrate in **opposite phase**. Energy shuttles
back and forth between the loops but there is **no net transfer of energy** along
the wave — that is what "stationary" means.

```figure caption="The first three harmonics of a string fixed at both ends. Each extra harmonic adds one half-wavelength, one node and one antinode; the frequency rises in the ratio 1 : 2 : 3."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(3, 1, figsize=(4.9, 3.3), sharex=True)
x = np.linspace(0, 1, 400)
for ax, n in zip(axes, [1, 2, 3]):
    y = np.sin(n*np.pi*x)
    ax.plot(x, y, color=ACCENT, lw=1.7)
    ax.plot(x, -y, color=GRID, lw=1.0, ls=(0,(4,2)))
    ax.axhline(0, color=GRID, lw=0.8)
    ax.plot(np.linspace(0,1,n+1), np.zeros(n+1), 'o', color=INK, ms=3.4, zorder=4)
    ax.text(0.008, 1.30, 'n = %d' % n, fontsize=8.5, color=INK, va='center')
    ax.text(0.992, 1.30, 'f = %dv/2L' % n, fontsize=8.5, color=MUTED,
            va='center', ha='right')
    ax.set_ylim(-1.35, 1.55); ax.axis('off')
fig.subplots_adjust(hspace=0.10)
```

### Strings fixed at both ends

Both ends are nodes, so the string holds a whole number of half-wavelengths:

$$ L = n\frac{\lambda}{2} \;\Rightarrow\; \lambda_n = \frac{2L}{n}, \qquad f_n = \frac{nv}{2L}, \quad n = 1,2,3,\dots $$

All harmonics are present. The fundamental $f_1 = v/2L$ is the **first harmonic**;
$2f_1$ is the second harmonic or **first overtone**; $3f_1$ the third harmonic or
second overtone. For a string of mass per unit length $\mu$ under tension $T$,
$v = \sqrt{T/\mu}$, so

$$ f_n = \frac{n}{2L}\sqrt{\frac{T}{\mu}} $$

The three **laws of the vibrating string** follow at once: $f \propto 1/L$ (length),
$f \propto \sqrt{T}$ (tension), $f \propto 1/\sqrt{\mu}$ (mass per unit length).

### Pipes

A pipe has a **node of displacement** at a closed end (the air cannot move against
the solid cap) and an **antinode** at an open end (the air is free to swing).

| | Open pipe (both ends open) | Closed pipe (one end closed) |
|---|---|---|
| Boundary conditions | antinode at each end | node at the closed end, antinode at the open end |
| Length in the $n$th mode | $L = n\lambda/2$ | $L = (2n-1)\lambda/4$ |
| Wavelength | $\lambda_n = 2L/n$ | $\lambda_n = 4L/(2n-1)$ |
| Frequency | $f_n = nv/2L$ | $f_n = (2n-1)v/4L$ |
| Harmonics present | **all**: $f_1, 2f_1, 3f_1,\dots$ | **odd only**: $f_1, 3f_1, 5f_1,\dots$ |
| Fundamental | $v/2L$ | $v/4L$ |
| First overtone | $2v/2L$ (2nd harmonic) | $3v/4L$ (3rd harmonic) |
| Second overtone | $3v/2L$ (3rd harmonic) | $5v/4L$ (5th harmonic) |
| Nodes / antinodes in the $n$th mode | $n+1$ nodes, $n$ antinodes | $n$ nodes, $n$ antinodes |
| Effective length with end correction | $L + 2e$ | $L + e$ |

For a 0.5 m pipe with $v = 340$ m s⁻¹ the numbers are:

| Mode | Open pipe | Closed pipe |
|---|---|---|
| Fundamental | 340 Hz | 170 Hz |
| 1st overtone | 680 Hz | 510 Hz |
| 2nd overtone | 1020 Hz | 850 Hz |

Notice the closed pipe has **half** the fundamental of the open pipe of the same
length, and every second harmonic is missing.

```figure caption="Displacement patterns in pipes. Left: open at both ends — antinodes at both ends, every harmonic. Right: closed at one end — a node at the closed end, and only the odd harmonics."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(3, 2, figsize=(5.0, 3.3), sharex=True)
x = np.linspace(0, 1, 500)
flab = [('v/2L', 'v/4L'), ('2v/2L', '3v/4L'), ('3v/2L', '5v/4L')]
for r in range(3):
    axo, axc = axes[r]
    yo = np.cos((r+1)*np.pi*x)
    yc = np.sin((2*r+1)*np.pi*x/2)
    axo.plot(x, yo, color=ACCENT, lw=1.6)
    axc.plot(x, yc, color=SERIES[2], lw=1.6)
    for ax in (axo, axc):
        ax.axhline(0, color=GRID, lw=0.8)
        ax.set_ylim(-1.62, 1.30); ax.axis('off')
        ax.plot([0,1], [1.16,1.16], color=MUTED, lw=1.1)
        ax.plot([0,1], [-1.16,-1.16], color=MUTED, lw=1.1)
    axo.plot([0,1], [1, yo[-1]], 'o', color=INK, ms=4.2, zorder=5)
    axc.plot([0,1], [0, yc[-1]], 'o', color=INK, ms=4.2, zorder=5)
    axo.text(0.5, -1.44, 'f = %s' % flab[r][0], fontsize=8.2, ha='center',
             va='center', color=INK)
    axc.text(0.5, -1.44, 'f = %s' % flab[r][1], fontsize=8.2, ha='center',
             va='center', color=INK)
axes[0][0].set_title('Open pipe: A at both ends', fontsize=8.6, pad=10)
axes[0][1].set_title('Closed pipe: N at closed end', fontsize=8.6, pad=10)
fig.subplots_adjust(hspace=0.16, wspace=0.10)
```

::: caution The two closed-pipe traps
1. A closed pipe has **no even harmonics**. Its "first overtone" is the **third
   harmonic** (three times the fundamental), not the second. So a 100 Hz closed
   pipe sounds 100, 300, 500 Hz — never 200 Hz.
2. The closed pipe fundamental is **half** that of an open pipe of the same length,
   not the same. Ratio open : closed $= 2 : 1$.
:::

### End correction

The antinode at an open end does not sit exactly at the cut edge — the air just
outside the pipe moves too, so the effective length is slightly longer. For a pipe
of diameter $d$, each open end adds

$$ e \approx 0.3d \qquad (\text{that is } 0.6r) $$

so a closed pipe has effective length $L + e$ and an open pipe $L + 2e$. End
correction lowers every frequency slightly.

The **resonance tube** measures it. A tuning fork of frequency $f$ is held over a
tube whose water level can be raised. Resonance (loudest sound) occurs when the air
column is a quarter-wavelength, then three-quarters:

$$ l_1 + e = \frac{\lambda}{4}, \qquad l_2 + e = \frac{3\lambda}{4} $$

Subtracting, $l_2 - l_1 = \lambda/2$, so

$$ \lambda = 2(l_2 - l_1), \qquad v = 2f(l_2 - l_1), \qquad e = \frac{l_2 - 3l_1}{2} $$

The subtraction kills $e$, which is why the tube gives a good value of $v$ even
though the end correction is unknown.

::: example Worked example 11.4 — a closed pipe
**Problem.** A pipe closed at one end has a fundamental frequency of 100 Hz. What
are the next two frequencies it can produce?

**Solution.** A closed pipe gives odd multiples only: $f_n = (2n-1)\times100$ Hz.
So 100, 300, 500 Hz. The 300 Hz note is the **first overtone** and the **third
harmonic**; 200 Hz is impossible in this pipe.
:::

::: example Worked example 11.5 — resonance tube
**Problem.** A tuning fork of 500 Hz gives resonance at air-column lengths of 17 cm
and 51 cm. Find the speed of sound and the end correction.

**Solution.** $v = 2f(l_2 - l_1) = 2(500)(0.51 - 0.17) = 2(500)(0.34) = 340$ m s⁻¹.
$e = \dfrac{l_2 - 3l_1}{2} = \dfrac{0.51 - 0.51}{2} = 0$.
A zero end correction is unusual but consistent: the numbers were chosen so that
$l_2 = 3l_1$, which happens only when $e = 0$.
:::

### Beats

Two waves of **slightly different** frequencies travelling in the same direction
superpose. At a point the two displacements are $A\cos(2\pi f_1 t)$ and
$A\cos(2\pi f_2 t)$; their sum is

$$ 2A\cos\left(2\pi\frac{f_1 - f_2}{2}t\right)\cos\left(2\pi\frac{f_1 + f_2}{2}t\right) $$

a wave of the average frequency whose amplitude is slowly modulated. The amplitude
is maximum twice per modulation cycle, so the **beat frequency** is

$$ f_b = |f_1 - f_2|, \qquad T_b = \frac{1}{f_b} $$

Beats are heard only when $f_b$ is small — below about 10 Hz the ear hears separate
pulses; above about 15 Hz it hears a rough, dissonant note instead.

```figure caption="Beats from two waves of 10 Hz and 11 Hz. The dashed envelope has amplitude $2A\cos(\pi(f_1-f_2)t)$; the loudness rises and falls once per second, so the beat frequency is 1 Hz."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9,2.7))
t = np.linspace(0, 2, 4000)
y = np.cos(2*np.pi*10*t) + np.cos(2*np.pi*11*t)
env = 2*np.cos(np.pi*1.0*t)
ax.plot(t, env, color=MUTED, lw=0.9, ls=(0,(4,2)))
ax.plot(t, -env, color=MUTED, lw=0.9, ls=(0,(4,2)))
ax.plot(t, y, color=ACCENT, lw=1.1)
ax.axhline(0, color=GRID, lw=0.8)
ax.annotate('', xy=(1.0,2.42), xytext=(0.0,2.42),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=0.9, mutation_scale=8))
ax.text(0.5, 2.52, r'$T_b = 1$ s', ha='center', va='bottom', fontsize=8.5)
ax.set_xlim(0,2); ax.set_ylim(-2.6, 2.85)
ax.set_xlabel('time  t  (s)'); ax.set_ylabel('displacement')
ax.set_yticks([-2,0,2])
ax.spines[['top','right']].set_visible(False)
```

::: tip Tuning-fork beat problems
Loading a fork with wax **lowers** its frequency; filing it **raises** it. So if
loading the unknown fork *reduces* the beat rate, the unknown was the higher of the
two; if loading *increases* it, the unknown was the lower. Work out which fork moved
in which direction before doing any arithmetic.
:::

## 11.4 Pressure amplitude, intensity and loudness, pitch and quality

### The pressure wave

A sound wave can be described either by the displacement of the air particles,
$y = A\sin(\omega t - kx)$, or by the excess pressure it creates. The two are a
quarter-cycle out of phase: where the particles are crowded together (displacement
zero, changing fastest) the pressure is greatest.

$$ \Delta p = p_m\cos(\omega t - kx), \qquad p_m = \rho v \omega A = BAk $$

$p_m$ is the **pressure amplitude**, in pascal. Because $p_m \propto \omega A =
2\pi fA$, a high-frequency wave of the same displacement carries far more pressure
variation — and far more energy.

A consequence worth memorising: at a **closed end** the air cannot move, so it is a
**displacement node** and a **pressure antinode**; at an **open end** the air swings
freely, a **displacement antinode** and a **pressure node**.

### Intensity

**Intensity** is the energy crossing unit area per second, perpendicular to the
direction of travel: $I = P/A$, unit W m⁻².

$$ I = \frac{1}{2}\rho v \omega^2 A^2 = 2\pi^2\rho v f^2 A^2 = \frac{p_m^2}{2\rho v} $$

So for the same medium and frequency, $I \propto A^2$; for the same amplitude,
$I \propto f^2$.

**Inverse-square law.** A point source radiating power $P$ equally in all directions
spreads it over a sphere of area $4\pi r^2$:

$$ I = \frac{P}{4\pi r^2} \;\Rightarrow\; I \propto \frac{1}{r^2} $$

Double the distance and the intensity falls to a quarter; the **amplitude** falls to
a half, because $A \propto \sqrt{I}$.

### Loudness in decibels

The ear responds to intensity over about thirteen powers of ten, so a logarithmic
scale is used. The **loudness level** in decibels is

$$ L = 10\log_{10}\frac{I}{I_0}, \qquad I_0 = 10^{-12}\ \text{W m}^{-2} $$

$I_0$ is the threshold of hearing at 1 kHz. Some landmarks:

| Source | $L$ (dB) | $I$ (W m⁻²) |
|---|---|---|
| threshold of hearing | 0 | $10^{-12}$ |
| rustling leaves | 10 | $10^{-11}$ |
| whisper | 20 | $10^{-10}$ |
| normal conversation | 60 | $10^{-6}$ |
| busy street in Kathmandu | 80 | $10^{-4}$ |
| rock concert | 110 | $10^{-1}$ |
| jet engine at 30 m | 130 | $10$ |

Two rules that answer most dB questions:

- $+10$ dB means **ten times** the intensity; $+20$ dB means a hundred times, and
  also **ten times** the pressure amplitude and ten times the displacement amplitude.
- Two identical sources sounding together give $+3$ dB, because the intensities add
  ($2I$), not the amplitudes.

::: caution Decibels add, intensities multiply
A level of 60 dB plus a level of 60 dB is **63 dB**, not 120 dB. And a sound of
80 dB is not "twice as loud" as 40 dB in the everyday sense — it is ten thousand
times the intensity. To combine two sources, add their **intensities** and convert
back to decibels; never add the decibel numbers themselves.
:::

::: example Worked example 11.6 — decibels and distance
**Problem.** A loudspeaker radiates 1 W uniformly. Find the intensity and the
loudness level at 10 m, and the change in level when you move to 100 m.

**Solution.** $I = P/4\pi r^2 = 1/(4\pi\times100) = 7.96\times10^{-4}$ W m⁻²;
$L = 10\log(7.96\times10^{-4}/10^{-12}) = 10\log(7.96\times10^8) = 89$ dB.
At 100 m the distance is ten times larger, so $I$ falls by $10^2$ and
$L$ falls by $10\log 100 = 20$ dB, to 69 dB.
:::

### Pitch, loudness and quality

| Sensation | Physical quantity it follows | How it changes |
|---|---|---|
| **Pitch** | frequency | higher frequency → higher pitch |
| **Loudness** | intensity (and frequency, through the ear's response) | more intensity → louder |
| **Quality** (timbre) | the number and relative strength of the overtones | same pitch, different waveform → different instrument |

A violin and a flute playing the same 440 Hz note have the same pitch and can have
the same loudness, but they sound different because their overtone mixtures differ.
That mixture is the **quality** of the note.

::: tip Fast dB arithmetic
Every factor of 10 in intensity is 10 dB; every factor of 2 is 3 dB; every factor
of 4 is 6 dB. To find a level, write the intensity as a power of ten times a small
factor and add the pieces: $2\times10^{-6}$ W m⁻² is $60 + 3 = 63$ dB.
:::

## 11.5 Doppler effect

The **Doppler effect** is the apparent change in the frequency of a wave when the
source, the observer, or both, move relative to the medium.

::: key One formula, one sign rule
$$ f' = f\,\frac{v \pm v_o}{v \mp v_s} $$

$v$ is the speed of sound in the medium (not relative to the ground), $v_o$ the
speed of the observer, $v_s$ the speed of the source.

**The rule:** choose the sign that **increases** $f'$ when the motion brings the
source and observer **closer**. So the numerator takes $+$ for an observer moving
**towards** the source and $-$ for away; the denominator takes $-$ for a source
moving **towards** the observer and $+$ for away. The observer is on top, the source
below.
:::

| Source | Observer | Apparent frequency |
|---|---|---|
| at rest | at rest | $f$ |
| at rest | moving towards, $v_o$ | $f\dfrac{v + v_o}{v}$ (higher) |
| at rest | moving away, $v_o$ | $f\dfrac{v - v_o}{v}$ (lower) |
| moving towards, $v_s$ | at rest | $f\dfrac{v}{v - v_s}$ (higher) |
| moving away, $v_s$ | at rest | $f\dfrac{v}{v + v_s}$ (lower) |
| moving towards, $v_s$ | moving towards, $v_o$ | $f\dfrac{v + v_o}{v - v_s}$ |
| moving away, $v_s$ | moving away, $v_o$ | $f\dfrac{v - v_o}{v + v_s}$ |

### Where the formula comes from

**Moving source.** The source emits $f$ waves per second and at the same time moves
towards the observer at $v_s$. During one period $T = 1/f$ it advances $v_sT$, so the
waves it has emitted are squeezed into the shorter distance

$$ \lambda' = vT - v_sT = \frac{v - v_s}{f} $$

These waves still travel at $v$ through the air, so the observer receives

$$ f' = \frac{v}{\lambda'} = f\,\frac{v}{v - v_s} $$

**Moving observer.** The source is at rest, so the wavelength in the air is the
normal $\lambda = v/f$. The observer meets the waves at the relative speed $v + v_o$,
so

$$ f' = \frac{v + v_o}{\lambda} = f\,\frac{v + v_o}{v} $$

**Both.** Put the two together: the wavelength is set by the source's motion and the
rate of meeting is set by the observer's motion, giving the combined formula above.

```figure caption="Wavefronts from a source moving to the right at half the speed of sound. The circles are crowded ahead of the source, where $\lambda' = (v-v_s)/f$, and stretched behind it, where $\lambda' = (v+v_s)/f$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.7,3.3))
for i in range(4):
    ax.add_patch(plt.Circle((0.5*i, 0), 3.5-i, fill=False, ec=ACCENT, lw=1.1, alpha=0.9))
ax.plot([1.5],[0],'o', color=SERIES[1], ms=6, zorder=5)
ax.annotate('', xy=(1.88,0), xytext=(1.55,0),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.5, mutation_scale=10))
ax.text(1.56, 0.15, r'$v_s$', fontsize=9, color=SERIES[1])
ax.annotate('', xy=(2.5,0), xytext=(2.0,0),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=1.0, mutation_scale=8))
ax.text(2.25, -0.30, r"$\lambda'$", fontsize=9, ha='center', va='center')
ax.annotate('', xy=(-2.0,0), xytext=(-3.5,0),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=1.0, mutation_scale=8))
ax.text(-2.75, -0.30, r"$\lambda'$", fontsize=9, ha='center', va='center')
ax.text(4.10, 3.45, 'crowded ahead', fontsize=8.2, color=ACCENT, ha='right', va='center')
ax.text(-4.05, 3.45, 'stretched behind', fontsize=8.2, color=MUTED, ha='left', va='center')
ax.set_xlim(-4.1, 4.2); ax.set_ylim(-3.7, 3.7)
ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 11.7 — both moving
**Problem.** A train sounding a 640 Hz horn moves at 20 m s⁻¹ towards a station.
A porter runs towards the train at 10 m s⁻¹. What frequency does he hear?
($v = 340$ m s⁻¹)

**Solution.** Both are approaching, so the numerator takes $+$ and the denominator
$-$: $f' = 640\times\dfrac{340 + 10}{340 - 20} = 640\times\dfrac{350}{320} =
700$ Hz.
Check the size: 640 → 700 is a rise of 9 %, about 1.5 semitones — clearly audible.
The same shift runs the other way once the train has passed, and that sudden fall is
what makes a passing siren so recognisable.
:::

::: caution The three Doppler mistakes
1. **Source moving away** puts $v + v_s$ in the denominator, not $v - v_s$. If your
   answer comes out *higher* than $f$ for a receding source, you have the sign
   backwards.
2. **$v$ is the speed of sound in still air**, not relative to the source or the
   observer. Only $f'$ changes; the sound still travels at 340 m s⁻¹ through the air.
3. **Motion across the line of sight** gives no shift to first order. An ambulance
   crossing in front of you at constant distance has the same pitch as when it is
   standing still.
:::

### Echoes and reflections

When the sound reflects from a wall, treat the problem in two steps: first the wall
is an observer receiving $f_1$; then the wall is a stationary source re-emitting
$f_1$. If the source itself moves towards the wall at $v_s$, the wave arriving at
the wall has $f_1 = f\dfrac{v}{v - v_s}$, and the source (still moving) hears the
echo as

$$ f'' = f_1\frac{v + v_s}{v} = f\,\frac{v + v_s}{v - v_s} $$

so the beat frequency between the emitted note and its echo is
$f'' - f = f\dfrac{2v_s}{v - v_s}$.

### Where it is used

- **Ambulance and train sirens:** the pitch drops abruptly as the vehicle passes.
- **Police speed radar and weather radar:** the shift in the reflected signal gives
  the speed of the target (for light, the same idea with $c$).
- **Doppler echocardiography:** ultrasound reflected from moving blood measures flow
  speed and direction.
- **Astronomical redshift:** light from receding galaxies is shifted to longer
  wavelengths — evidence that the universe is expanding.

## Formula and fact sheet

| Topic | Formula or fact |
|---|---|
| Wave equation | $y = A\sin(\omega t - kx)$ travels $+x$; $\omega = 2\pi f$, $k = 2\pi/\lambda$ |
| Wave speed | $v = f\lambda = \omega/k$ |
| Phase difference | $\Delta\phi = 2\pi\Delta x/\lambda = 2\pi\Delta t/T$ |
| Particle velocity | $v_p = A\omega\cos(\omega t - kx) = -v\times\text{slope}$; maximum $A\omega$ |
| Speed in a medium | $v = \sqrt{E/\rho}$: solid $\sqrt{Y/\rho}$, liquid $\sqrt{B/\rho}$, gas $\sqrt{\gamma P/\rho}$ |
| Gas | $v = \sqrt{\gamma RT/M}$; $v \propto \sqrt{T}$, $v \propto 1/\sqrt{M}$; independent of $P$ at constant $T$ |
| Air | 331 m s⁻¹ at 0 °C, 343 at 20 °C, +0.61 m s⁻¹ per °C |
| String | $v = \sqrt{T/\mu}$; $f_n = \frac{n}{2L}\sqrt{T/\mu}$, all $n$ |
| Open pipe | $f_n = nv/2L$; fundamental $v/2L$; all harmonics |
| Closed pipe | $f_n = (2n-1)v/4L$; fundamental $v/4L$; odd harmonics only |
| End correction | $e = 0.3d$ per open end; closed $L+e$, open $L+2e$ |
| Resonance tube | $v = 2f(l_2 - l_1)$; $e = (l_2 - 3l_1)/2$ |
| Beats | $f_b = f_1 - f_2$ (the difference, taken positive); $T_b = 1/f_b$; heard for $f_b < 10$ Hz |
| Pressure amplitude | $p_m = \rho v\omega A = BAk$; $\Delta p$ leads displacement by $90^{\circ}$ |
| Intensity | $I = \frac{1}{2}\rho v\omega^2A^2 = 2\pi^2\rho vf^2A^2 = p_m^2/2\rho v$ |
| Inverse square | $I \propto 1/r^2$, $A \propto 1/r$ |
| Decibel | $L = 10\log_{10}(I/I_0)$, $I_0 = 10^{-12}$ W m⁻²; $+10$ dB $= 10\times I$; $+3$ dB $= 2\times I$ |
| Doppler | $f' = f\frac{v \pm v_o}{v \mp v_s}$; upper sign for approach |
| Echo | $f'' = f\frac{v + v_s}{v - v_s}$; beat $= f\frac{2v_s}{v - v_s}$ |
| Node / antinode | node–node $\lambda/2$; node–antinode $\lambda/4$ |

## Chapter summary

- A progressive wave is $y = A\sin(\omega t - kx)$, with $v = \omega/k = f\lambda$;
  the minus sign means it travels towards $+x$.
- Particle velocity is $v_p = -v\times\text{slope}$ of the profile, with maximum
  $A\omega$ — a completely different number from the wave speed.
- Sound speed is set by stiffness and density: $\sqrt{Y/\rho}$ in solids,
  $\sqrt{B/\rho}$ in liquids, $\sqrt{\gamma P/\rho} = \sqrt{\gamma RT/M}$ in gases.
  It rises with temperature, falls with molar mass, and does not change with
  pressure at constant temperature.
- A string fixed at both ends and an open pipe give every harmonic,
  $f_n = nv/2L$; a closed pipe gives odd harmonics only, $f_n = (2n-1)v/4L$, and has
  half the fundamental of the open pipe of the same length.
- End correction $e = 0.3d$ per open end; the resonance tube removes it by using
  $l_2 - l_1 = \lambda/2$.
- Beats: $f_b = |f_1 - f_2|$, audible only for small differences; waxing a fork lowers
  its frequency, filing raises it.
- Intensity is $2\pi^2\rho vf^2A^2$, falls as $1/r^2$, and converts to loudness by
  $L = 10\log(I/I_0)$; $+10$ dB is ten times the intensity, $+3$ dB is two sources.
- Doppler: $f' = f(v \pm v_o)/(v \mp v_s)$ with the upper sign for approach; a source
  moving away lowers the pitch, and motion across the line of sight gives no shift.

## Practice questions

**Set A — Recall (28 questions)**

1. In $y = A\sin(\omega t - kx)$, the quantity $\omega/k$ is the
   (a) wave speed (b) particle speed (c) frequency (d) wavelength
2. The SI unit of the intensity of a wave is
   (a) W (b) W m⁻¹ (c) W m⁻² (d) J m⁻²
3. Sound cannot travel through
   (a) steel (b) vacuum (c) water (d) hydrogen
4. A pipe closed at one end can produce
   (a) all harmonics (b) only even harmonics (c) only the fundamental (d) only odd harmonics
5. The beat frequency of two waves of frequencies $f_1$ and $f_2$ is
   (a) $|f_1 - f_2|$ (b) $f_1 + f_2$ (c) $(f_1 + f_2)/2$ (d) $\sqrt{f_1f_2}$
6. The loudness level in decibels is defined with the reference intensity
   (a) 1 W m⁻² (b) 10⁻⁶ W m⁻² (c) 10⁻¹² W m⁻² (d) 10⁻¹⁶ W m⁻²
7. The pitch of a musical note is determined by its
   (a) intensity (b) frequency (c) waveform (d) speed
8. The number of nodes in the $n$th harmonic of a string fixed at both ends is
   (a) $n$ (b) $n - 1$ (c) $2n$ (d) $n + 1$
9. At constant temperature, the speed of sound in a gas is
   (a) independent of pressure (b) proportional to pressure (c) proportional to $\sqrt{P}$ (d) inversely proportional to pressure
10. Laplace corrected Newton's formula by treating the propagation of sound as
   (a) isothermal (b) isobaric (c) adiabatic (d) isochoric
11. For a gas at absolute temperature $T$, the speed of sound is
   (a) $\sqrt{RT/M}$ (b) $\sqrt{\gamma RT/M}$ (c) $\gamma\sqrt{RT/M}$ (d) $\sqrt{\gamma M/RT}$
12. An observer moving towards a stationary source with speed $v_o$ hears a frequency
   (a) $f(v - v_o)/v$ (b) $fv/(v + v_o)$ (c) $fv/(v - v_o)$ (d) $f(v + v_o)/v$
13. The distance between two consecutive nodes in a stationary wave is
   (a) $\lambda/2$ (b) $\lambda$ (c) $\lambda/4$ (d) $2\lambda$
14. Two points on a wave separated by $\lambda/4$ differ in phase by
   (a) $\pi$ (b) $2\pi$ (c) $\pi/2$ (d) $\pi/4$
15. The relation between wave speed, frequency and wavelength is
   (a) $v = f/\lambda$ (b) $v = f\lambda$ (c) $v = \lambda/f$ (d) $v = f^2\lambda$
16. In a stationary wave
   (a) energy is carried at speed $v$ (b) all particles have equal amplitude (c) the wave travels in one direction (d) there is no net transfer of energy
17. The end correction of a pipe of diameter $d$, open at one end, is about
   (a) $0.3d$ (b) $0.6d$ (c) $0.15d$ (d) $d$
18. The intensity of a wave is proportional to
   (a) the amplitude (b) the square root of the amplitude (c) the square of the amplitude (d) the wavelength
19. The unit of loudness level is the
   (a) watt (b) decibel (c) hertz (d) pascal
20. A sound wave of frequency 170 Hz travels at 340 m s⁻¹. Its wavelength is
   (a) 0.5 m (b) 1 m (c) 4 m (d) 2 m
21. Which of the following is a longitudinal wave?
   (a) sound in air (b) light in vacuum (c) a wave on a string (d) a ripple on water
22. In a pipe open at both ends, the frequencies produced are
   (a) odd multiples of the fundamental only (b) even multiples only (c) all integral multiples of the fundamental (d) unrelated to the fundamental
23. The frequency of a stretched string is proportional to
   (a) the tension (b) the square root of the tension (c) the length (d) the square root of the length
24. When a source of sound moves away from a stationary observer, the frequency heard is
   (a) higher (b) the same (c) doubled (d) lower
25. The speed of sound is greatest in
   (a) air (b) water (c) steel (d) vacuum
26. Beats are clearly heard when the frequencies of the two sources differ by less than about
   (a) 10 Hz (b) 100 Hz (c) 1000 Hz (d) 10000 Hz
27. The third harmonic of a closed pipe contains
   (a) 1 node and 1 antinode (b) 2 nodes and 2 antinodes (c) 3 nodes and 3 antinodes (d) 2 nodes and 3 antinodes
28. The speed of a wave is determined by
   (a) its frequency (b) its amplitude (c) its wavelength (d) the medium

::: note Answers and explanations — Set A
**1.** (a) — $v = \omega/k$; multiplying $\omega$ by $t$ and $k$ by $x$ leaves a phase, and $\omega/k$ has the unit rad s⁻¹ ÷ rad m⁻¹ = m s⁻¹.
**2.** (c) — intensity is power per unit area, W m⁻². The watt alone is power; J m⁻² is energy per area, not per area per second.
**3.** (b) — sound is a mechanical wave and needs particles to compress; in vacuum there is nothing to vibrate, so no sound (light still passes).
**4.** (d) — the closed end forces a node and the open end an antinode, which fits an odd number of quarter-wavelengths: $L = (2n-1)\lambda/4$. Even harmonics would need a node at both ends.
**5.** (a) — the envelope repeats $|f_1 - f_2|$ times a second. The sum $f_1 + f_2$ is the frequency you would hear inside the beats, not the beat rate.
**6.** (c) — $I_0 = 10^{-12}$ W m⁻² is the threshold of hearing at 1 kHz, the zero of the dB scale.
**7.** (b) — pitch is the ear's judgement of frequency. Intensity gives loudness and waveform gives quality.
**8.** (d) — $n$ half-wavelengths need $n+1$ nodes: two ends plus $n-1$ interior nodes.
**9.** (a) — doubling $P$ doubles $\rho$ as well, so $P/\rho$ and hence $v = \sqrt{\gamma P/\rho}$ are unchanged. Only temperature (or molar mass) changes the speed.
**10.** (c) — compressions follow too quickly for heat to flow, so $PV^{\gamma}$ is constant and $B = \gamma P$; that raises 280 m s⁻¹ to 331 m s⁻¹.
**11.** (b) — $v = \sqrt{\gamma P/\rho}$ and $P = \rho RT/M$ give $v = \sqrt{\gamma RT/M}$. Option (a) omits $\gamma$, which is about 1.4 for air.
**12.** (d) — the observer meets the waves at relative speed $v + v_o$ while the wavelength stays $v/f$, so $f' = f(v + v_o)/v$. Option (c) is the moving-source formula.
**13.** (a) — the displacement repeats every half-wavelength, so nodes are $\lambda/2$ apart; node to antinode is $\lambda/4$.
**14.** (c) — a quarter of a wavelength is a quarter of $2\pi$, that is $\pi/2$.
**15.** (b) — one wave passes per period and occupies one wavelength, so $v = f\lambda$.
**16.** (d) — the two travelling waves carry equal energy in opposite directions; energy oscillates between kinetic and elastic forms but does not travel.
**17.** (a) — the standard value is $e = 0.3d$ (equivalently $0.6r$) for each open end.
**18.** (c) — $I = 2\pi^2\rho vf^2A^2$, so doubling the amplitude quadruples the intensity.
**19.** (b) — the decibel. The watt is power, the hertz frequency and the pascal pressure.
**20.** (d) — $\lambda = v/f = 340/170 = 2$ m.
**21.** (a) — sound in air is a pressure (compression) wave; light is transverse, and so are waves on a string and water ripples.
**22.** (c) — an open pipe holds any number of half-wavelengths, so every harmonic $nv/2L$ appears.
**23.** (b) — $f = \frac{1}{2L}\sqrt{T/\mu}$, so $f \propto \sqrt{T}$; quadrupling the tension only doubles the frequency.
**24.** (d) — a receding source stretches the wavelength, $f' = fv/(v + v_s) < f$.
**25.** (c) — steel has by far the largest elastic modulus for its density; gases are slowest because they are easy to compress.
**26.** (a) — above about 10–15 Hz the separate pulses merge into a rough note and the beats are no longer heard as beats.
**27.** (b) — the third harmonic is $3\lambda/4$ long: nodes at the closed end and at $2L/3$, antinodes at $L/3$ and at the open end — two of each.
**28.** (d) — $v$ is fixed by the elasticity and inertia of the medium; $f$ and $\lambda$ can change, but their product stays at the value the medium allows.
:::

**Set B — Understanding (17 questions)**

1. A wave $y = A\sin(\omega t - kx)$ travels towards $+x$. At a point where the profile slopes upward, the particle there is moving
   (a) upward (b) towards $+x$ (c) downward (d) with the wave
2. Sound passes from air into water. Which quantity is unchanged?
   (a) frequency (b) speed (c) wavelength (d) amplitude
3. Two pipes of equal length, one open at both ends and one closed at one end, have fundamental frequencies in the ratio (open : closed)
   (a) 1 : 2 (b) 1 : 1 (c) 4 : 1 (d) 2 : 1
4. The first overtone of a closed pipe is the
   (a) second harmonic (b) third harmonic (c) fourth harmonic (d) fifth harmonic
5. The tension in a sonometer wire is made four times larger. The frequency of the wire becomes
   (a) 4 times (b) half (c) 2 times (d) $\sqrt{2}$ times
6. An unknown fork gives 4 beats per second with a 256 Hz fork. On loading the unknown fork with wax the beat rate falls to 2 per second. Its frequency is
   (a) 260 Hz (b) 252 Hz (c) 254 Hz (d) 264 Hz
7. A source moves away from a stationary observer at half the speed of sound. The frequency heard is
   (a) $f/2$ (b) $3f/2$ (c) $f$ (d) $2f/3$
8. An observer moves away from a stationary source at half the speed of sound. The frequency heard is
   (a) $2f/3$ (b) $f/2$ (c) $3f/2$ (d) $f$
9. The intensity of sound 2 m from a point source is $I$. At 8 m from the same source it is
   (a) $I/16$ (b) $I/4$ (c) $I/8$ (d) $I/64$
10. An increase of 10 dB in the loudness level means the intensity has increased by a factor of
   (a) 2 (b) 5 (c) 10 (d) 100
11. An increase of 20 dB means the pressure amplitude has increased by a factor of
   (a) 2 (b) 20 (c) 100 (d) 10
12. Two identical sources sounding together give a level 3 dB above one alone. Their combined intensity is
   (a) 3 times (b) 2 times (c) 1.5 times (d) 10 times
13. The speed of sound in a gas doubles when the absolute temperature is
   (a) increased four times (b) doubled (c) halved (d) increased eight times
14. On a humid day the speed of sound in air
   (a) decreases (b) stays the same (c) increases (d) becomes zero
15. At a point where the displacement of a sound wave is zero, the pressure variation is
   (a) zero (b) maximum (c) half its maximum (d) always negative
16. In a stationary wave, particles in two adjacent loops
   (a) vibrate in phase (b) are at rest (c) have different frequencies (d) vibrate in opposite phase
17. The second resonance length in a resonance tube is about
   (a) three times the first (b) twice the first (c) four times the first (d) half the first

::: note Answers and explanations — Set B
**1.** (c) — $v_p = -v\times\text{slope}$; a positive slope with a wave moving towards $+x$ gives a negative (downward) particle velocity. The crest is still to the left, so the particle is on its way down.
**2.** (a) — the frequency is fixed by the source and cannot change at a boundary; the higher speed in water forces a longer wavelength ($\lambda = v/f$).
**3.** (d) — open $v/2L$, closed $v/4L$, so the ratio is 2 : 1. The closed pipe sounds an octave lower.
**4.** (b) — closed pipes skip the second harmonic, so the first overtone is the third harmonic, $3v/4L$.
**5.** (c) — $f \propto \sqrt{T}$, and $\sqrt{4} = 2$. Quadrupling the tension doubles the frequency, not quadruples it.
**6.** (a) — wax lowers the unknown frequency. If it was 260 Hz it falls to about 258 and the beats with 256 fall from 4 to 2, as stated. Had it been 252, waxing would have taken it further from 256 and the beats would have risen.
**7.** (d) — $f' = f\dfrac{v}{v + v/2} = \dfrac{2}{3}f$. The denominator grows, so the frequency falls.
**8.** (b) — the observer meets fewer waves: $f' = f\dfrac{v - v/2}{v} = \dfrac{f}{2}$.
**9.** (a) — $I \propto 1/r^2$; the distance is four times larger, so the intensity is $1/16$.
**10.** (c) — $10\log_{10}x = 10$ gives $x = 10$. Option (d) would be 20 dB.
**11.** (d) — 20 dB is a factor $10^2$ in intensity, and amplitude goes as the square root of intensity, so a factor 10.
**12.** (b) — two incoherent identical sources add their intensities, $2I$, which is $10\log 2 = 3$ dB.
**13.** (a) — $v \propto \sqrt{T}$, so doubling $v$ needs $T$ four times larger. Doubling $T$ only multiplies $v$ by $\sqrt{2}$.
**14.** (c) — water vapour has molar mass 18 against about 29 for dry air, so humid air is less dense and sound travels slightly faster.
**15.** (b) — displacement and pressure are a quarter-cycle apart: a displacement node (particles crowded, zero displacement but maximum compression change) is a pressure antinode.
**16.** (d) — the loops on either side of a node move in opposite directions at every instant; particles inside one loop are in phase.
**17.** (a) — $l_2 \approx 3l_1$, because the second resonance is at three quarter-wavelengths against one at the first.
:::

**Set C — Application (12 questions)**

1. A wave is $y = 0.02\sin(100t - 2x)$ in SI units. Its speed is
   (a) 2 m s⁻¹ (b) 50 m s⁻¹ (c) 100 m s⁻¹ (d) 200 m s⁻¹
2. For the same wave, the maximum speed of a particle of the medium is
   (a) 50 m s⁻¹ (b) 0.04 m s⁻¹ (c) 100 m s⁻¹ (d) 2 m s⁻¹
3. The speed of sound in air at 0 °C is 331 m s⁻¹. At 27 °C it is about
   (a) 347 m s⁻¹ (b) 331 m s⁻¹ (c) 356 m s⁻¹ (d) 363 m s⁻¹
4. The ratio of the speed of sound in hydrogen to that in oxygen at the same temperature is
   (a) 2 (b) 2.8 (c) 4 (d) 16
5. A pipe closed at one end is 0.5 m long. Taking $v = 340$ m s⁻¹, its fundamental frequency is
   (a) 85 Hz (b) 170 Hz (c) 340 Hz (d) 510 Hz
6. A pipe open at both ends is 0.5 m long. Taking $v = 340$ m s⁻¹, its fundamental frequency is
   (a) 85 Hz (b) 170 Hz (c) 680 Hz (d) 340 Hz
7. A train sounding a 500 Hz horn approaches a stationary listener at 34 m s⁻¹ ($v = 340$ m s⁻¹). The frequency heard is
   (a) 556 Hz (b) 550 Hz (c) 455 Hz (d) 444 Hz
8. The same train, now receding at 34 m s⁻¹, is heard at
   (a) 556 Hz (b) 545 Hz (c) 455 Hz (d) 500 Hz
9. A source of 680 Hz moves at 20 m s⁻¹ directly towards a wall. A listener standing at the source hears the echo with a beat frequency of ($v = 340$ m s⁻¹)
   (a) 20 Hz (b) 40 Hz (c) 42 Hz (d) 85 Hz
10. The intensity of a sound is $10^{-8}$ W m⁻². Its loudness level is
   (a) 8 dB (b) 40 dB (c) 80 dB (d) 120 dB
11. Two tuning forks of 512 Hz and 516 Hz are sounded together. The beat frequency is
   (a) 2 Hz (b) 8 Hz (c) 4 Hz (d) 514 Hz
12. A 500 Hz fork resonates with air columns of 17 cm and 51 cm in a resonance tube. The speed of sound is
   (a) 340 m s⁻¹ (b) 330 m s⁻¹ (c) 350 m s⁻¹ (d) 170 m s⁻¹

::: note Answers and explanations — Set C
**1.** (b) — $v = \omega/k = 100/2 = 50$ m s⁻¹. The amplitude 0.02 plays no part in the wave speed.
**2.** (d) — $v_{p,\max} = A\omega = 0.02\times100 = 2$ m s⁻¹. Option (a) is the wave speed, which is 25 times larger.
**3.** (a) — $v = 331\sqrt{300/273} = 331(1.048) = 347$ m s⁻¹. Adding 27 to the Celsius reading is not the same as increasing $T$ by 10 %.
**4.** (c) — both diatomic, so $\gamma$ cancels: $\sqrt{M_{O_2}/M_{H_2}} = \sqrt{32/2} = 4$.
**5.** (b) — closed pipe: $f_1 = v/4L = 340/(4\times0.5) = 170$ Hz.
**6.** (d) — open pipe: $f_1 = v/2L = 340/(2\times0.5) = 340$ Hz, twice the closed-pipe value.
**7.** (a) — $f' = 500\times\dfrac{340}{340 - 34} = 500\times\dfrac{340}{306} = 556$ Hz. Option (b) is the observer-moving answer, not the source-moving one.
**8.** (c) — $f' = 500\times\dfrac{340}{340 + 34} = 500\times\dfrac{340}{374} = 455$ Hz.
**9.** (d) — the wall receives $680\times340/320 = 722.5$ Hz and re-emits it; the moving source hears $722.5\times360/340 = 765$ Hz. The beat with the emitted 680 Hz is 85 Hz.
**10.** (b) — $L = 10\log(10^{-8}/10^{-12}) = 10\log 10^4 = 40$ dB.
**11.** (c) — $f_b = |512 - 516| = 4$ Hz.
**12.** (a) — $v = 2f(l_2 - l_1) = 2(500)(0.34) = 340$ m s⁻¹. The end correction cancels in the subtraction, which is why the tube works.
:::
