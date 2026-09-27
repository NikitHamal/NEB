---
subject: Physics
grade: 12
unit: 9
title: Acoustic phenomena
hours: 5
area: Waves and Optics
---

Everything you hear — the pitch of a temple bell, the roar of a bus on the Ring
Road, the rising whine of an ambulance as it passes — is a pressure wave
arriving at your eardrum. This unit turns the everyday words *loud*, *shrill*
and *sweet* into measurable physical quantities, and then works out what happens
to a note when the source or the listener is moving.

::: key Three separate ideas, three separate symbols
Do not let **intensity** ($I$, in W m⁻²), **intensity level** ($\beta$, in dB)
and **loudness** ($L$, a sensation) blur together. Intensity is energy per
second per square metre; intensity level is a logarithmic comparison with a
standard; loudness is what your ear reports. The exam tests the difference.
:::

## 9.1 Sound waves: pressure amplitude

A sound wave can be described in two equivalent ways: by the **displacement** of
the air particles, or by the **excess pressure** — the small amount by which the
pressure rises above or falls below the steady atmospheric value.

Let a plane progressive wave travel along $x$ with displacement

$$ y = a\sin(\omega t - kx) $$

Consider a thin layer of air of original thickness $\Delta x$. When the wave
passes, its two faces move by different amounts, so its new thickness is
$\Delta x + (\partial y/\partial x)\Delta x$. The volume strain is therefore
$\partial y/\partial x$, and by the definition of the bulk modulus $B$ the
excess pressure is

$$ \Delta P = -B\frac{\partial y}{\partial x} $$

::: derivation Pressure amplitude of a sound wave
Differentiating $y = a\sin(\omega t - kx)$ with respect to $x$,

$$ \frac{\partial y}{\partial x} = -ka\cos(\omega t - kx) $$

so

$$ \Delta P = Bak\cos(\omega t - kx) $$

The **pressure amplitude** is the largest value of $\Delta P$:

$$ P_0 = Bak $$

For a sound wave $v = \sqrt{B/\rho}$, so $B = \rho v^{2}$, and $k = \omega/v$.
Substituting,

$$ P_0 = \rho v^{2}\cdot a\cdot\frac{\omega}{v} = \rho v\omega a = 2\pi\rho v f a $$
:::

Two consequences matter. First, $\Delta P$ contains $\cos$ where $y$ contains
$\sin$: **the pressure wave is a quarter of a wavelength out of step with the
displacement wave.** Where the displacement is zero the pressure change is
greatest, and vice versa. Second, for a given displacement amplitude the
pressure amplitude grows in proportion to the frequency.

```figure caption="Displacement $y$ and excess pressure $\Delta P$ for the same sound wave at one instant. They are $\lambda/4$ out of step: at a compression (C) the displacement is zero but $\Delta P$ is maximum."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,3.2))
lam, N = 2.0, 4.2
x = np.linspace(0, N, 700)
k = 2*np.pi/lam
ax.plot(x, 2.3+0.72*np.sin(k*x), color=ACCENT, lw=1.9)
ax.plot(x, -0.1-0.72*np.cos(k*x), color='#A8271F', lw=1.9)
ax.plot([0, N], [2.3, 2.3], color=MUTED, lw=0.7, ls=':')
ax.plot([0, N], [-0.1, -0.1], color=MUTED, lw=0.7, ls=':')
for xc in (1.0, 3.0):
    ax.plot([xc, xc], [-1.0, 3.25], color=MUTED, lw=0.7, ls=(0,(3,3)))
    ax.annotate('C', (xc, 3.30), ha='center', va='bottom', color='#A8271F', fontsize=9.5)
for xc in (0.0, 2.0, 4.0):
    ax.plot([xc, xc], [-1.0, 3.25], color=MUTED, lw=0.7, ls=(0,(1,3)))
    ax.annotate('R', (xc, 3.30), ha='center', va='bottom', color='#0B6A62', fontsize=9.5)
ax.annotate('displacement  $y$', (4.28, 2.3), ha='left', va='center',
            color=ACCENT, fontsize=8.8)
ax.annotate('excess pressure  $\\Delta P$', (4.28, -0.1), ha='left', va='center',
            color='#A8271F', fontsize=8.8)
ax.plot([1.5, 1.5], [1.02, 1.58], color=MUTED, lw=0.7, ls=(0,(3,3)))
ax.annotate('', xy=(1.0, 1.10), xytext=(1.5, 1.10),
            arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=1.0,
                            mutation_scale=8, shrinkA=0, shrinkB=0))
ax.annotate('$\\lambda/4$', (1.25, 1.16), ha='center', va='bottom',
            color=MUTED, fontsize=9)
ax.annotate('$a$', (0.66, 2.66), ha='center', va='center', color=ACCENT, fontsize=9)
ax.annotate('', xy=(0.5, 2.3), xytext=(0.5, 3.02),
            arrowprops=dict(arrowstyle='<|-|>', color=ACCENT, lw=0.9,
                            mutation_scale=7, shrinkA=0, shrinkB=0))
ax.annotate('$P_0$', (3.68, 0.26), ha='center', va='center', color='#A8271F', fontsize=9)
ax.annotate('', xy=(3.5, -0.1), xytext=(3.5, 0.62),
            arrowprops=dict(arrowstyle='<|-|>', color='#A8271F', lw=0.9,
                            mutation_scale=7, shrinkA=0, shrinkB=0))
ax.set_xlabel('distance  $x$')
ax.set_xlim(-0.2, 5.9); ax.set_ylim(-1.15, 3.85)
ax.set_yticks([]); ax.set_xticks([])
ax.spines[['top','right','left','bottom']].set_visible(False)
```

The ear is astonishingly sensitive. At 1 kHz the faintest audible sound has a
root-mean-square pressure of only about $2\times10^{-5}\ \text{Pa}$ — one
five-thousand-millionth of atmospheric pressure — which corresponds to a
displacement amplitude of roughly $10^{-11}\ \text{m}$, smaller than the
diameter of an atom.

## 9.2 Characteristics of sound: intensity, loudness, quality and pitch

A musical note has three characteristics you can hear — loudness, pitch and
quality — and each is governed by a measurable physical quantity.

### Intensity

::: definition Intensity of sound
The intensity of sound at a point is the energy carried by the wave per second
through unit area held perpendicular to the direction of propagation. Its SI
unit is the watt per square metre (W m⁻²).
:::

For a plane progressive wave the intensity works out to

$$ I = \frac{1}{2}\rho v\omega^{2}a^{2} = 2\pi^{2}\rho v f^{2}a^{2} = \frac{P_0^{2}}{2\rho v} $$

So intensity depends on the **square** of the amplitude and the **square** of
the frequency, and on the medium through $\rho v$. For a point source radiating
power $P$ uniformly in all directions, the energy at distance $r$ is spread over
a sphere of area $4\pi r^{2}$:

$$ I = \frac{P}{4\pi r^{2}} \qquad\text{so}\qquad I \propto \frac{1}{r^{2}} $$

This **inverse-square law** is why you must stand close to hear a soft speaker.

### Intensity level and the decibel

The ear can cope with intensities spanning a factor of $10^{12}$, so a
logarithmic scale is used. Taking the standard reference
$I_0 = 10^{-12}\ \text{W m}^{-2}$ (roughly the threshold of hearing at 1 kHz),
the **intensity level** is

$$ \beta = 10\log_{10}\!\left(\frac{I}{I_0}\right) \quad\text{decibel (dB)} $$

| Sound | $I$ (W m⁻²) | $\beta$ (dB) |
|---|---|---|
| Threshold of hearing | $10^{-12}$ | 0 |
| Rustling leaves, soft whisper | $10^{-10}$ | 20 |
| Quiet room at night | $10^{-8}$ | 40 |
| Normal conversation | $10^{-6}$ | 60 |
| Busy Kathmandu street | $10^{-4}$ | 80 |
| Motorcycle horn at 1 m | $10^{-1}$ | 110 |
| Threshold of pain | $1$ | 120 |

::: tip The 3 dB and 10 dB shortcuts
Doubling the intensity adds $10\log_{10}2 = 3.0\ \text{dB}$; multiplying it by
ten adds exactly 10 dB. Doubling the *distance* from a point source quarters the
intensity, so the level falls by $10\log_{10}4 = 6.0\ \text{dB}$. These three
numbers answer most decibel questions without a calculator.
:::

### Loudness

**Loudness** is the *sensation* produced in the ear. It grows with intensity,
but not in proportion to it: by the **Weber–Fechner law** the sensation is
proportional to the logarithm of the stimulus,

$$ L = k\log_{10} I $$

Loudness also depends on frequency — the human ear is most sensitive between
about 1 kHz and 5 kHz, so a 100 Hz note and a 3 kHz note of the *same* intensity
do not sound equally loud. Loudness is measured in phon or sone, intensity level
in decibels; they are not the same thing.

::: caution Intensity is physical, loudness is physiological
Two sounds of equal intensity can have very different loudness if their
frequencies differ, and a sound can be perfectly measurable yet completely
inaudible (an ultrasonic whistle). Never write "loudness = $10\log(I/I_0)$" —
that is the intensity *level*.
:::

### Pitch

**Pitch** is the sensation of how high or low a note is, and it is decided by
**frequency**: the higher the frequency, the higher the pitch. A normal human
ear responds from about 20 Hz to 20 000 Hz. Below 20 Hz is **infrasonic**
(earthquake waves, elephant calls); above 20 kHz is **ultrasonic** (bat and
dolphin echolocation, medical scanning).

### Quality (timbre)

Two instruments playing the same note at the same loudness still sound
different. A real instrument produces the fundamental *plus* a set of overtones,
and the **number of overtones and their relative intensities** decide the shape
of the resulting waveform. That shape is the **quality** or **timbre**.

```figure caption="Three sounds of the same pitch and the same loudness but different quality. The waveform repeats at the same period; only the harmonic mixture differs."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,3.0))
t = np.linspace(0, 2, 900)
w = 2*np.pi
waves = [(np.sin(w*t), 'tuning fork\n(pure tone)'),
         (np.sin(w*t)+0.50*np.sin(2*w*t)+0.30*np.sin(3*w*t), 'bansuri\n(flute)'),
         (np.sin(w*t)+0.62*np.sin(3*w*t)+0.42*np.sin(5*w*t)+0.24*np.sin(7*w*t),
          'sarangi\n(bowed string)')]
for i, (y, lab) in enumerate(waves):
    yc = -2.6*i
    y = 1.05*y/np.max(np.abs(y))
    ax.plot(t, yc+y, color=SERIES[i], lw=1.7)
    ax.plot([0, 2], [yc, yc], color=MUTED, lw=0.6, ls=':')
    ax.annotate(lab, (-0.09, yc), ha='right', va='center', color=INK, fontsize=8.5)
ax.annotate('', xy=(0, 1.70), xytext=(1, 1.70),
            arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=1.0,
                            mutation_scale=8, shrinkA=0, shrinkB=0))
ax.annotate('one period $T = 1/f_1$ — same for all three',
            (0.5, 1.78), ha='center', va='bottom', color=MUTED, fontsize=8.4)
ax.set_xlim(-0.95, 2.25); ax.set_ylim(-6.6, 2.75)
ax.axis('off')
```

| Characteristic | Physical quantity | Depends on |
|---|---|---|
| Loudness | intensity | square of amplitude, $1/r^{2}$, sensitivity of ear |
| Pitch | frequency | frequency of the fundamental |
| Quality | waveform | number and relative intensity of overtones |

::: example Worked example 9.1
**Problem.** A sound wave of frequency 1000 Hz in air has a displacement
amplitude of $1.0\times10^{-8}\ \text{m}$. Taking
$\rho = 1.29\ \text{kg m}^{-3}$ and $v = 340\ \text{m s}^{-1}$, find (a) the
pressure amplitude, (b) the intensity, and (c) the intensity level in decibels.

**Solution.**

(a) $\omega = 2\pi f = 2\pi\times1000 = 6.283\times10^{3}\ \text{rad s}^{-1}$ and
$\rho v = 1.29\times340 = 438.6\ \text{kg m}^{-2}\text{s}^{-1}$.

$$ P_0 = \rho v\omega a = 438.6\times6.283\times10^{3}\times1.0\times10^{-8} = 2.76\times10^{-2}\ \text{Pa} $$

(b) $$ I = \frac{P_0^{2}}{2\rho v} = \frac{(2.76\times10^{-2})^{2}}{2\times438.6} = \frac{7.60\times10^{-4}}{877.2} = 8.66\times10^{-7}\ \text{W m}^{-2} $$

(c) $$ \beta = 10\log_{10}\frac{8.66\times10^{-7}}{10^{-12}} = 10\log_{10}(8.66\times10^{5}) = 10\times5.94 = 59.4\ \text{dB} $$

That is a little under 60 dB — the level of ordinary conversation — produced by
air particles moving only a hundredth of a micrometre.
:::

::: example Worked example 9.2
**Problem.** A small loudspeaker radiates 2.0 W of sound power uniformly in all
directions. Find the intensity and the intensity level at 10 m, and the
intensity level at 20 m.

**Solution.** At $r = 10\ \text{m}$,

$$ I = \frac{P}{4\pi r^{2}} = \frac{2.0}{4\pi(10)^{2}} = \frac{2.0}{1256.6} = 1.59\times10^{-3}\ \text{W m}^{-2} $$
$$ \beta = 10\log_{10}\frac{1.59\times10^{-3}}{10^{-12}} = 10\log_{10}(1.59\times10^{9}) = 92.0\ \text{dB} $$

Doubling the distance to 20 m quarters the intensity, so the level falls by
$10\log_{10}4 = 6.0\ \text{dB}$:

$$ \beta' = 92.0 - 6.0 = 86.0\ \text{dB} $$
:::

## 9.3 Doppler's effect

::: definition Doppler effect
The apparent change in the frequency of a wave observed when the source, the
observer, or both are in motion relative to the medium is called the Doppler
effect. The frequency emitted by the source never changes; only the frequency
received changes.
:::

```figure caption="Wavefronts from a source S moving to the right. Ahead of the source the wavelength is squeezed to $(v-v_s)/f$ and the pitch rises; behind it the wavelength is stretched to $(v+v_s)/f$ and the pitch falls."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle
fig, ax = plt.subplots(figsize=(5.0,2.95))
v, vs, T, N = 1.0, 0.6, 1.0, 6
for n in range(N):
    ax.add_patch(Circle((vs*n*T, 0), v*(N-n)*T, fill=False,
                        edgecolor=ACCENT, lw=1.1, alpha=0.85))
ax.plot([vs*(N-1)*T], [0], 'o', color='#A8271F', ms=6, zorder=6)
ax.annotate('S', (vs*(N-1)*T, 0), textcoords='offset points', xytext=(-2, 9),
            ha='center', color='#A8271F', fontsize=10)
ax.annotate('', xy=(vs*(N-1)*T+1.1, 0), xytext=(vs*(N-1)*T+0.25, 0),
            arrowprops=dict(arrowstyle='-|>', color='#A8271F', lw=1.4, mutation_scale=11))
ax.annotate('$v_s$', (vs*(N-1)*T+0.68, 0.20), ha='center', color='#A8271F', fontsize=9.5)
ax.annotate('ahead: crowded, pitch rises', (5.4, -2.25),
            ha='center', va='top', color=INK, fontsize=8.6)
ax.annotate('behind: spread out, pitch falls', (-5.4, -2.25),
            ha='center', va='top', color=INK, fontsize=8.6)
ax.plot([5.2], [0], marker='>', color='#0B6A62', ms=8, zorder=6)
ax.plot([-6.6], [0], marker='<', color='#0B6A62', ms=8, zorder=6)
ax.annotate('observer', (5.2, 0.42), ha='center', color='#0B6A62', fontsize=8.4)
ax.annotate('observer', (-6.6, 0.42), ha='center', color='#0B6A62', fontsize=8.4)
ax.set_xlim(-8.4, 8.4); ax.set_ylim(-3.25, 2.45)
ax.set_aspect('equal')
ax.axis('off')
```

::: derivation The Doppler formula
Let the source emit sound of frequency $f$, let $v$ be the speed of sound in
still air, $v_s$ the speed of the source and $v_o$ the speed of the observer.

**Case 1: source moving towards a stationary observer.** In one period
$T = 1/f$ the wave front advances $vT$ but the source itself advances $v_sT$.
The next wave front is therefore emitted from a point closer to the observer,
and the waves are packed into a shorter wavelength:

$$ \lambda' = vT - v_sT = \frac{v - v_s}{f} $$

The observer is at rest, so the waves reach her at speed $v$ and

$$ f' = \frac{v}{\lambda'} = \frac{v}{v-v_s}f $$

**Case 2: observer moving towards a stationary source.** Now the wavelength is
unchanged, $\lambda = v/f$, but the observer runs into the waves, so their speed
relative to her is $v + v_o$:

$$ f' = \frac{v+v_o}{\lambda} = \frac{v+v_o}{v}f $$

**General case.** Combining the two,

$$ f' = \left(\frac{v + v_o}{v - v_s}\right)f $$
:::

::: memory Getting the signs right
Use $f' = \dfrac{v+v_o}{v-v_s}f$ always, and fix the signs by asking only one
question: **does this motion bring them closer?**

- Observer moving **towards** the source: $v_o$ is **positive**; moving away, negative.
- Source moving **towards** the observer: $v_s$ is **positive**; moving away, negative.

Any approach makes the numerator bigger or the denominator smaller, so $f'>f$.
If your answer disagrees with that check, you have a sign wrong.
:::

| Situation | Apparent frequency |
|---|---|
| Source approaches, observer at rest | $f' = \dfrac{v}{v-v_s}f$ |
| Source recedes, observer at rest | $f' = \dfrac{v}{v+v_s}f$ |
| Observer approaches, source at rest | $f' = \dfrac{v+v_o}{v}f$ |
| Observer recedes, source at rest | $f' = \dfrac{v-v_o}{v}f$ |
| Both approach each other | $f' = \dfrac{v+v_o}{v-v_s}f$ |
| Both recede from each other | $f' = \dfrac{v-v_o}{v+v_s}f$ |

**When there is no Doppler effect.** If the source and observer move with the
same velocity in the same direction, their separation is constant and $f' = f$.
If the motion is perpendicular to the line joining them — the instant a train
passes you broadside — there is no shift either. And a steady **wind** produces
no change for a stationary source and observer, because it increases the speed
of sound and the wavelength in exactly the same proportion.

**Applications.** Traffic police speed guns and weather radar; SONAR for
measuring the speed of a submarine or shoal of fish; Doppler ultrasound
(echocardiography) to measure the speed of blood in an artery; and, in
astronomy, the **red shift** of light from distant galaxies, which is the
evidence that the universe is expanding.

::: example Worked example 9.3
**Problem.** A train approaching a station sounds a whistle of frequency 640 Hz
while moving at $20\ \text{m s}^{-1}$. Taking the speed of sound as
$340\ \text{m s}^{-1}$, find the frequency heard by a stationary passenger on
the platform (a) as the train approaches and (b) after it has passed. What is
the change in frequency as the train goes by?

**Solution.**

(a) Source approaching, observer at rest, so $v_s = +20\ \text{m s}^{-1}$:

$$ f' = \frac{v}{v-v_s}f = \frac{340}{340-20}\times640 = \frac{340}{320}\times640 = 680\ \text{Hz} $$

(b) Source receding, so $v_s = -20\ \text{m s}^{-1}$:

$$ f'' = \frac{v}{v+v_s}f = \frac{340}{360}\times640 = 604.4\ \text{Hz} $$

The pitch drops by $680 - 604.4 = 75.6\ \text{Hz}$ as the train passes — a fall
of more than a musical tone, which is exactly what you hear.
:::

::: example Worked example 9.4
**Problem.** Two vehicles approach each other on the Prithvi Highway. A jeep
sounding a horn of frequency 400 Hz travels at $20\ \text{m s}^{-1}$; a
motorcycle comes towards it at $15\ \text{m s}^{-1}$. Taking
$v = 340\ \text{m s}^{-1}$, find the frequency heard by the motorcyclist.

**Solution.** Both are approaching, so both signs are positive:
$v_o = +15\ \text{m s}^{-1}$ and $v_s = +20\ \text{m s}^{-1}$.

$$ f' = \left(\frac{v+v_o}{v-v_s}\right)f = \left(\frac{340+15}{340-20}\right)\times400 = \frac{355}{320}\times400 $$
$$ f' = 1.1094\times400 = 443.8\ \text{Hz} $$

The horn sounds about 44 Hz sharper than it really is.
:::

## Chapter summary

- Excess pressure $\Delta P = -B\,\partial y/\partial x$; the pressure amplitude
  is $P_0 = Bak = \rho v\omega a = 2\pi\rho v f a$.
- The pressure wave is $\lambda/4$ out of phase with the displacement wave: a
  displacement node is a pressure antinode.
- Intensity $I = \frac{1}{2}\rho v\omega^{2}a^{2} = P_0^{2}/2\rho v$, in W m⁻²;
  for a point source $I = P/4\pi r^{2}$, so $I\propto 1/r^{2}$.
- Intensity level $\beta = 10\log_{10}(I/I_0)$ dB with
  $I_0 = 10^{-12}\ \text{W m}^{-2}$. Doubling $I$ adds 3 dB; doubling the
  distance subtracts 6 dB.
- Loudness (Weber–Fechner, $L = k\log I$) is the *sensation*; pitch is set by
  frequency; quality is set by the overtones present, i.e. by the waveform.
- Doppler effect: $f' = \dfrac{v+v_o}{v-v_s}f$, with $v_o$ and $v_s$ counted
  positive when the motion brings source and observer closer.
- There is no Doppler shift for motion perpendicular to the line of sight, for
  equal velocities in the same direction, or for a steady wind.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The pressure amplitude of a sound wave of displacement amplitude $a$ and angular frequency $\omega$ is <span class="marks">[1]</span>
   (a) $\rho v a$ (b) $\rho v\omega a$ (c) $\rho v\omega^{2}a$ (d) $\rho\omega a$
2. The displacement wave and the pressure wave in air differ in phase by <span class="marks">[1]</span>
   (a) $0$ (b) $\pi/4$ (c) $\pi/2$ (d) $\pi$
3. If the intensity of a sound is doubled, its intensity level increases by about <span class="marks">[1]</span>
   (a) 2 dB (b) 3 dB (c) 6 dB (d) 10 dB
4. The quality of a musical note depends on <span class="marks">[1]</span>
   (a) frequency (b) amplitude (c) number and intensity of overtones (d) speed of sound
5. A source and an observer move with the same velocity in the same direction. The apparent frequency is <span class="marks">[1]</span>
   (a) greater than $f$ (b) less than $f$ (c) equal to $f$ (d) zero

::: note Answers to Group A
**1.** (b) — $P_0 = Bak$ and $B=\rho v^{2}$, $k=\omega/v$, giving $\rho v\omega a$.
**2.** (c) — $\Delta P \propto \cos$ where $y\propto\sin$, a quarter cycle apart.
**3.** (b) — $10\log_{10}2 = 3.0\ \text{dB}$.
**4.** (c) — the harmonic mixture fixes the waveform, and the waveform is the quality.
**5.** (c) — the separation does not change, so no wavefronts are gained or lost.
:::

**Group B — Short answer (5 marks each)**

1. Show that the pressure amplitude of a sound wave is $P_0 = \rho v\omega a$
   and explain why the pressure wave leads the displacement wave by a quarter of
   a wavelength. <span class="marks">[5]</span>
2. Distinguish between intensity, intensity level and loudness of sound, giving
   the unit of each. <span class="marks">[5]</span>
3. The intensity level of a sound is 70 dB. Find its intensity, and the new
   intensity level if the intensity is increased 100 times. <span class="marks">[5]</span>
4. Explain how the pitch and the quality of a note are related to the physical
   properties of the sound wave. Why do a bansuri and a sarangi sounding the same
   note sound different? <span class="marks">[5]</span>
5. A whistle of frequency 500 Hz is sounded on a car moving away from a
   stationary listener at $25\ \text{m s}^{-1}$. Taking $v = 340\ \text{m s}^{-1}$,
   find the frequency heard. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** With $y = a\sin(\omega t-kx)$, $\Delta P = -B\,\partial y/\partial x
= Bak\cos(\omega t-kx)$, so $P_0 = Bak$. Using $B=\rho v^{2}$ and $k=\omega/v$
gives $P_0 = \rho v\omega a$. The cosine leads the sine by $\pi/2$, which in
space is a quarter wavelength.

**3.** $\beta = 10\log_{10}(I/I_0) = 70$ gives $I/I_0 = 10^{7}$, so
$I = 10^{7}\times10^{-12} = 1.0\times10^{-5}\ \text{W m}^{-2}$. Multiplying the
intensity by $100 = 10^{2}$ adds $10\log_{10}10^{2} = 20\ \text{dB}$, giving
$\beta' = 90\ \text{dB}$.

**5.** The source recedes, so $v_s = -25\ \text{m s}^{-1}$:

$$ f' = \frac{v}{v+25}f = \frac{340}{365}\times500 = 465.8\ \text{Hz} $$

The whistle sounds about 34 Hz flatter than it really is.
:::

**Group C — Long answer (8 marks each)**

1. (a) State the Doppler effect and derive an expression for the apparent
   frequency when both the source and the observer are in motion along the line
   joining them. <span class="marks">[5]</span>
   (b) Give two situations in which there is relative motion but no Doppler
   shift, and state two practical applications of the effect. <span class="marks">[3]</span>
2. A point source emits sound uniformly with a power of 0.50 W.
   (a) Find the intensity and the intensity level at a distance of 5.0 m. <span class="marks">[4]</span>
   (b) At what distance does the intensity level fall to 60 dB? <span class="marks">[4]</span>
   (Take $I_0 = 10^{-12}\ \text{W m}^{-2}$.)

::: note Answer to Group C question 2
(a) $$ I = \frac{P}{4\pi r^{2}} = \frac{0.50}{4\pi(5.0)^{2}} = \frac{0.50}{314.16} = 1.59\times10^{-3}\ \text{W m}^{-2} $$
$$ \beta = 10\log_{10}\frac{1.59\times10^{-3}}{10^{-12}} = 10\log_{10}(1.59\times10^{9}) = 92.0\ \text{dB} $$

(b) A level of 60 dB means $I' = 10^{6}I_0 = 1.0\times10^{-6}\ \text{W m}^{-2}$.
From $I' = P/4\pi r'^{2}$,

$$ r'^{2} = \frac{P}{4\pi I'} = \frac{0.50}{4\pi\times1.0\times10^{-6}} = 3.979\times10^{4}\ \text{m}^{2} $$
$$ r' = 199\ \text{m} $$

So the level drops from 92 dB to 60 dB — a factor of about 1600 in intensity —
between 5 m and about 200 m, exactly as the inverse-square law requires.
:::
