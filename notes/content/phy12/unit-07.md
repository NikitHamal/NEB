---
subject: Physics
grade: 12
unit: 7
title: Mechanical waves
hours: 4
area: Waves and Optics
---

A mechanical wave carries energy through matter without carrying the matter
along with it. Sound is the mechanical wave you meet every day, and this short
unit answers one question about it: **what fixes its speed?** The answer turns
out to depend on only two properties of the medium — how stiff it is and how
heavy it is — plus, for a gas, one subtlety about heat that took physics a
century to get right.

::: key What the examiner wants from this unit
Four things, over and over: the general formula $v=\sqrt{E/\rho}$ applied to a
named medium; the derivation of **Newton's formula**; **Laplace's correction**
and why it was needed; and a numerical using $v_t = v_0\sqrt{T/273}$. Learn
those four and the unit is finished.
:::

## 7.1 Speed of wave motion; velocity of sound in solid and liquid

Every wave obeys the kinematic relation

$$ v = f\lambda $$

but this only *relates* speed, frequency and wavelength — it does not say what
the speed is. The speed is decided by the medium, not by the source. If you
sound a horn louder or at a higher pitch, the sound still arrives at the same
time.

A mechanical wave travels because a disturbed part of the medium pulls its
neighbour back (elasticity) and because that neighbour resists being moved
(inertia). Newton showed that these two combine as

$$ v = \sqrt{\frac{E}{\rho}} $$

where $\rho$ is the density of the medium and $E$ is the **modulus of elasticity
appropriate to the kind of deformation the wave produces**. Choosing the right
modulus is the whole skill.

| Medium and wave | Deformation | Modulus used | Speed |
|---|---|---|---|
| Long thin solid rod, longitudinal | stretch/squeeze along rod | Young's modulus $Y$ | $v=\sqrt{Y/\rho}$ |
| Liquid, longitudinal | change of volume | Bulk modulus $B$ | $v=\sqrt{B/\rho}$ |
| Gas, longitudinal | change of volume | Bulk modulus of gas | $v=\sqrt{B/\rho}$ |
| Stretched string, transverse | change of shape | tension $T$, mass per length $\mu$ | $v=\sqrt{T/\mu}$ |

::: definition Newton's general formula for wave speed
The speed of a mechanical wave in a medium is the square root of the ratio of
the relevant elastic modulus of the medium to its density:
$v = \sqrt{E/\rho}$.
:::

A liquid and a gas have no rigidity, so they cannot be sheared: **sound in a
fluid is always longitudinal**. A solid resists both squeezing and shearing, so
a solid carries *both* longitudinal and transverse waves — which is exactly why
an earthquake such as Gorkha 2015 produces two body waves, the fast longitudinal
P-wave and the slower transverse S-wave, and why seismologists at the National
Seismological Centre can locate an epicentre from the gap between their arrivals.

```figure caption="A longitudinal wave. The dotted rows show particles crowded at compressions (C) and thinned at rarefactions (R). The blue curve is the particle displacement $y$ measured along the direction of travel."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,3.0))
lam = 2.0; L = 4.0; A = 0.155
x0 = np.linspace(0, L, 45)
xs = x0 + A*np.sin(2*np.pi*x0/lam)
for yy in np.linspace(2.10, 2.80, 4):
    ax.plot(xs, np.full_like(xs, yy), ls='none', marker='o', ms=3.1,
            color=INK, alpha=0.9)
for xc, lab in [(1.0,'C'), (3.0,'C')]:
    ax.annotate(lab, (xc, 3.05), ha='center', color='#A8271F', fontsize=10)
for xc, lab in [(0.0,'R'), (2.0,'R'), (4.0,'R')]:
    ax.annotate(lab, (xc, 3.05), ha='center', color='#0B6A62', fontsize=10)
xc = np.linspace(0, L, 500)
ax.plot(xc, 0.95 + 0.62*np.sin(2*np.pi*xc/lam), color=ACCENT, lw=1.9)
ax.axhline(0.95, color=MUTED, lw=0.8, ls=':')
ax.annotate('', xy=(2.0, 0.28), xytext=(0.0, 0.28),
            arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=1.1,
                            mutation_scale=10, shrinkA=0, shrinkB=0))
ax.annotate(r'$\lambda$', (1.0, 0.36), ha='center', color=MUTED, fontsize=10)
ax.annotate('direction of travel', xy=(4.42, 2.45), xytext=(2.58, 1.84),
            color=INK, fontsize=8.4, va='center',
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.1, mutation_scale=11))
ax.set_xlim(-0.35, 4.6); ax.set_ylim(0.05, 3.35)
ax.axis('off')
```

Notice from the table that steel is about **eight times denser than water**, yet
sound goes more than three times faster in steel. Density alone never decides
the answer: Young's modulus of steel is roughly a hundred times the bulk modulus
of water, and stiffness wins.

::: example Worked example 7.1
**Problem.** Find the speed of sound (a) in a steel rail, for which
$Y = 2.0\times10^{11}\ \text{Pa}$ and $\rho = 7800\ \text{kg m}^{-3}$, and
(b) in water, for which $B = 2.2\times10^{9}\ \text{Pa}$ and
$\rho = 1000\ \text{kg m}^{-3}$.

**Solution.**

(a) A rail is a long thin solid, so use Young's modulus:

$$ v = \sqrt{\frac{Y}{\rho}} = \sqrt{\frac{2.0\times10^{11}}{7800}} = \sqrt{2.56\times10^{7}} = 5.06\times10^{3}\ \text{m s}^{-1} $$

(b) Water is a liquid, so use the bulk modulus:

$$ v = \sqrt{\frac{B}{\rho}} = \sqrt{\frac{2.2\times10^{9}}{1000}} = \sqrt{2.2\times10^{6}} = 1.48\times10^{3}\ \text{m s}^{-1} $$

So sound travels about **5060 m s⁻¹** in steel and **1480 m s⁻¹** in water,
against roughly 340 m s⁻¹ in air. Put your ear to a rail and you hear the train
long before the air carries the sound to you.
:::

## 7.2 Velocity of sound in gas

For a gas the deformation is a change of volume, so the modulus needed is the
bulk modulus

$$ B = -\frac{\Delta P}{\Delta V / V} $$

The minus sign is there because an increase in pressure produces a *decrease* in
volume, and it makes $B$ positive.

Newton (1686) now had to decide **how** the gas is compressed. He argued that
the compressions and rarefactions are slow enough, and the gas thin enough, for
the heat generated in a compression to leak away at once, so the temperature of
the gas stays constant. That is an **isothermal** change.

::: derivation Newton's formula for the velocity of sound in a gas
For an isothermal change of an ideal gas, Boyle's law gives

$$ PV = \text{constant} $$

Differentiating the product,

$$ P\,dV + V\,dP = 0 \;\Longrightarrow\; -\frac{dP}{dV/V} = P $$

The left-hand side is precisely the bulk modulus, so the **isothermal bulk
modulus is $B_{iso} = P$**. Substituting in $v = \sqrt{B/\rho}$:

$$ v = \sqrt{\frac{P}{\rho}} $$

This is **Newton's formula**.
:::

Test it at normal temperature and pressure, where
$P = 1.013\times10^{5}\ \text{Pa}$ and $\rho = 1.293\ \text{kg m}^{-3}$ for air:

$$ v = \sqrt{\frac{1.013\times10^{5}}{1.293}} = \sqrt{7.835\times10^{4}} = 280\ \text{m s}^{-1} $$

The measured value at 0 °C is about **332 m s⁻¹**. Newton's answer is too small
by 52 m s⁻¹ — an error of about **16 %**. No experiment of that era was that
bad, so the assumption, not the measurement, had to be wrong.

## 7.3 Laplace's correction

In 1816 Laplace located the faulty assumption. Sound of even the lowest audible
frequency, 20 Hz, compresses a given layer of air 20 times a second; at 1000 Hz
the compression lasts about half a millisecond. Air is also a very poor
conductor of heat. In that time practically **no heat leaves a compression or
enters a rarefaction**. The changes are therefore not isothermal but
**adiabatic**.

::: derivation Laplace's correction
For an adiabatic change of an ideal gas,

$$ PV^{\gamma} = \text{constant}, \qquad \gamma = \frac{C_p}{C_v} $$

Differentiating the product,

$$ \gamma P V^{\gamma-1}\,dV + V^{\gamma}\,dP = 0 $$

Dividing throughout by $V^{\gamma-1}$ and rearranging,

$$ -\frac{dP}{dV/V} = \gamma P \;\Longrightarrow\; B_{adi} = \gamma P $$

The adiabatic bulk modulus is $\gamma$ times the isothermal one. Hence the
corrected speed is

$$ v = \sqrt{\frac{\gamma P}{\rho}} $$
:::

For air $\gamma = 1.4$, so the corrected value at NTP is

$$ v = \sqrt{1.4}\times 280 = 1.183\times280 = 331\ \text{m s}^{-1} $$

which agrees with experiment. The graph below shows why $\gamma$ appears: an
adiabatic curve through a given state is **steeper** than the isothermal curve
through the same state, by exactly the factor $\gamma$, so the gas is harder to
squeeze and the wave travels faster.

```figure caption="Isothermal ($PV=$ const) and adiabatic ($PV^{1.4}=$ const) curves through the same state. The adiabatic curve is steeper, so $B_{adi}=\gamma P > B_{iso}=P$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,2.9))
V0, P0 = 1.0, 1.0
V = np.linspace(0.55, 1.75, 300)
ax.plot(V, P0*V0/V, color=ACCENT, lw=1.9, label='isothermal  $PV=$ const')
ax.plot(V, P0*(V0/V)**1.4, color='#A8271F', lw=1.9,
        label=r'adiabatic  $PV^{1.4}=$ const')
ax.plot([V0], [P0], 'o', color=INK, ms=5, zorder=5)
ax.annotate('same state', (V0, P0), textcoords='offset points',
            xytext=(12, 10), color=INK, fontsize=8.6,
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.0, mutation_scale=9))
ax.set_xlabel('volume  $V$'); ax.set_ylabel('pressure  $P$')
ax.set_xlim(0.5, 1.8); ax.set_ylim(0.35, 2.4)
ax.set_xticks([]); ax.set_yticks([])
ax.spines[['top','right']].set_visible(False)
ax.legend(loc='upper right', fontsize=8.2)
```

| | Newton | Laplace |
|---|---|---|
| Assumed process | isothermal | adiabatic |
| Reason given | heat escapes instantly | air is a bad conductor, changes are fast |
| Bulk modulus | $B = P$ | $B = \gamma P$ |
| Speed formula | $v=\sqrt{P/\rho}$ | $v=\sqrt{\gamma P/\rho}$ |
| Value for air at 0 °C | 280 m s⁻¹ | 331 m s⁻¹ |
| Agreement with experiment | 16 % too low | agrees |

::: caution Laplace did not change the formula, only the modulus
A very common slip is to write "Laplace's correction is $v=\sqrt{\gamma P/\rho}$
because sound is a longitudinal wave". The longitudinal nature has nothing to do
with it. The correction is *only* that the compressions are adiabatic, so the
bulk modulus is $\gamma P$ and not $P$. Say that sentence in the exam and the
mark is yours.
:::

::: example Worked example 7.2
**Problem.** Calculate the velocity of sound in hydrogen at 0 °C, given
$\gamma = 1.4$, $P = 1.013\times10^{5}\ \text{Pa}$ and density of hydrogen
$= 0.09\ \text{kg m}^{-3}$. Compare it with the value in air.

**Solution.**

$$ v = \sqrt{\frac{\gamma P}{\rho}} = \sqrt{\frac{1.4\times1.013\times10^{5}}{0.09}} = \sqrt{1.576\times10^{6}} = 1.26\times10^{3}\ \text{m s}^{-1} $$

Since $\gamma$ is the same for both diatomic gases, the ratio of speeds is

$$ \frac{v_{H}}{v_{air}} = \sqrt{\frac{\rho_{air}}{\rho_{H}}} = \sqrt{\frac{1.293}{0.09}} = 3.79 $$

Sound travels about **3.8 times faster in hydrogen** than in air, because
hydrogen is far lighter while its stiffness $\gamma P$ is the same.
:::

## 7.4 Effect of temperature, pressure, humidity on velocity of sound

To see which quantities really matter, eliminate $\rho$ using the ideal gas
equation. For $n$ moles of gas of molar mass $M$ in volume $V$,
$\rho = nM/V$ and $PV = nRT$, so $P/\rho = RT/M$ and

$$ v = \sqrt{\frac{\gamma P}{\rho}} = \sqrt{\frac{\gamma R T}{M}} $$

This single result settles every case, because it contains **no pressure at
all**.

### Pressure — no effect

At a fixed temperature, doubling the pressure of a gas doubles its density too
(Boyle's law), so the ratio $P/\rho$ is unchanged and the speed is unchanged.
This is why sound does not travel measurably faster at sea level in Biratnagar
than high in Kathmandu valley *for the same temperature* — any difference you
actually hear comes from the temperature difference, not the pressure.

### Temperature — the one that matters

From $v=\sqrt{\gamma RT/M}$, at constant composition

$$ v \propto \sqrt{T} \qquad\text{(}T\text{ in kelvin)} $$

So if $v_0$ is the speed at 0 °C (273 K) and $v_t$ the speed at $t$ °C,

$$ \frac{v_t}{v_0} = \sqrt{\frac{273+t}{273}} \;\Longrightarrow\; v_t = v_0\sqrt{1+\frac{t}{273}} $$

For small $t$, using the binomial approximation $(1+x)^{1/2}\approx 1+x/2$,

$$ v_t \approx v_0\left(1+\frac{t}{546}\right) = v_0 + \frac{v_0}{546}t $$

With $v_0 = 332\ \text{m s}^{-1}$ this gives $v_0/546 = 0.61$, so

$$ v_t \approx 332 + 0.61\,t \quad \text{m s}^{-1} $$

**The velocity of sound in air increases by about 0.61 m s⁻¹ for each 1 °C rise
in temperature.** The graph shows how good the straight-line rule is over
ordinary Nepali temperatures.

```figure caption="Speed of sound in air against temperature. The exact law $v=v_0\sqrt{1+t/273}$ and the rule of thumb $v \approx 332+0.61t$ differ by less than 1.5 m s$^{-1}$ up to 50 °C."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.8))
t = np.linspace(-20, 50, 300); v0 = 332.0
ax.plot(t, v0*np.sqrt(1+t/273.0), color=ACCENT, lw=2.0,
        label=r'exact  $v_0\sqrt{1+t/273}$')
ax.plot(t, v0 + 0.61*t, color='#A8271F', lw=1.5, ls='--',
        label=r'linear  $332+0.61\,t$')
for tt, lab in [(0,'0 °C'), (25,'25 °C')]:
    vv = v0*np.sqrt(1+tt/273.0)
    ax.plot([tt],[vv],'o',color=INK,ms=4.2,zorder=5)
    ax.annotate(f'{vv:.0f} m s$^{{-1}}$', (tt,vv), textcoords='offset points',
                xytext=(6,-12), color=MUTED, fontsize=8.2)
ax.set_xlabel('temperature  $t$  (°C)')
ax.set_ylabel('speed  $v$  (m s$^{-1}$)')
ax.set_xlim(-20, 50); ax.set_ylim(316, 366)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=0.5)
ax.legend(loc='upper left', fontsize=8.2)
```

### Humidity — a small increase

Water vapour has molar mass 18 g mol⁻¹ while dry air averages about
28.8 g mol⁻¹. When water vapour is added to air it *replaces* some of the
heavier nitrogen and oxygen molecules, so at the same pressure and temperature
**moist air is less dense than dry air**. Since $v\propto 1/\sqrt{\rho}$, the
speed rises. The effect is small — a few metres per second between bone-dry and
saturated air — but it is real, and it is one reason distant sounds seem to
carry unusually well in the humid air just before a monsoon shower.

| Factor changed | Effect on $v$ | Reason |
|---|---|---|
| Pressure (at constant $T$) | none | $P/\rho$ fixed by Boyle's law |
| Temperature | increases, $v\propto\sqrt{T}$ | $v=\sqrt{\gamma RT/M}$ |
| Humidity | increases slightly | moist air is less dense than dry air |
| Wind | adds vectorially | the medium itself is moving |
| Amplitude (loudness) | none | speed is a property of the medium |
| Frequency (pitch) | none | air is non-dispersive for sound |

**Wind** does not change the speed *relative to the air*; it moves the air
itself. If a wind of speed $w$ blows at an angle $\theta$ to the direction in
which the sound travels, the speed relative to the ground is

$$ v_{eff} = v + w\cos\theta $$

Sound therefore carries further downwind than upwind.

::: example Worked example 7.3
**Problem.** The velocity of sound in air at 0 °C is 332 m s⁻¹. Find its value
at 27 °C (a) exactly, and (b) using the linear rule.

**Solution.**

(a) $T = 273+27 = 300\ \text{K}$, so

$$ v_{27} = v_0\sqrt{\frac{300}{273}} = 332\times\sqrt{1.0989} = 332\times1.0483 = 348\ \text{m s}^{-1} $$

(b) $v_{27}\approx 332 + 0.61\times27 = 332+16.5 = 348.5\ \text{m s}^{-1}$.

The two agree to within 0.5 m s⁻¹, so the linear rule is perfectly safe for
everyday temperatures.
:::

::: example Worked example 7.4
**Problem.** A trekker claps her hands facing a cliff across a valley in
Godavari and hears the echo 3.0 s later. The air temperature is 15 °C and the
speed of sound at 0 °C is 332 m s⁻¹. How far away is the cliff?

**Solution.** First correct the speed for temperature:

$$ v = 332 + 0.61\times15 = 332 + 9.2 = 341.2\ \text{m s}^{-1} $$

The sound travels to the cliff **and back**, so the path length is $2d$:

$$ 2d = vt = 341.2\times3.0 = 1023.6\ \text{m} \;\Longrightarrow\; d = 512\ \text{m} $$

The cliff is about **512 m** away. Using the uncorrected 332 m s⁻¹ would have
given 498 m — an error of 14 m, which is why the temperature correction is
worth doing.
:::

## Chapter summary

- Every wave obeys $v=f\lambda$, but the speed itself is set by the medium:
  $v=\sqrt{E/\rho}$, elasticity over inertia.
- Solid rod: $v=\sqrt{Y/\rho}$ ($\approx 5060\ \text{m s}^{-1}$ in steel).
  Liquid: $v=\sqrt{B/\rho}$ ($\approx 1480\ \text{m s}^{-1}$ in water). Fluids
  carry only longitudinal sound; solids carry longitudinal and transverse waves.
- **Newton's formula**: assuming isothermal compressions, $B_{iso}=P$ and
  $v=\sqrt{P/\rho}$, giving 280 m s⁻¹ for air — 16 % too low.
- **Laplace's correction**: the compressions are adiabatic, so $B_{adi}=\gamma P$
  and $v=\sqrt{\gamma P/\rho} = 331\ \text{m s}^{-1}$, which matches experiment.
- Eliminating density gives $v=\sqrt{\gamma RT/M}$: the speed depends on
  temperature and on the gas, never on the pressure.
- $v_t=v_0\sqrt{1+t/273}\approx v_0+0.61t$ for air: **+0.61 m s⁻¹ per °C**.
- Humidity raises $v$ slightly (moist air is lighter); wind adds vectorially,
  $v_{eff}=v+w\cos\theta$; amplitude and frequency have no effect.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The velocity of sound in a gas is independent of <span class="marks">[1]</span>
   (a) temperature (b) pressure (c) density (d) nature of the gas
2. Laplace's correction to Newton's formula multiplies the velocity by <span class="marks">[1]</span>
   (a) $\gamma$ (b) $\sqrt{\gamma}$ (c) $1/\gamma$ (d) $\gamma^{2}$
3. Sound travels fastest in <span class="marks">[1]</span>
   (a) vacuum (b) air (c) water (d) steel
4. If the absolute temperature of a gas is made four times, the velocity of sound in it becomes <span class="marks">[1]</span>
   (a) half (b) twice (c) four times (d) unchanged
5. The velocity of sound in moist air is <span class="marks">[1]</span>
   (a) greater than in dry air (b) less than in dry air (c) equal to that in dry air (d) zero

::: note Answers to Group A
**1.** (b) — $v=\sqrt{\gamma RT/M}$ contains no $P$; at constant $T$, $P/\rho$ is fixed.
**2.** (b) — the modulus changes from $P$ to $\gamma P$, so $v$ changes by $\sqrt{\gamma}$.
**3.** (d) — Young's modulus of steel is enormous compared with the moduli of fluids.
**4.** (b) — $v\propto\sqrt{T}$, and $\sqrt{4}=2$.
**5.** (a) — water vapour (M = 18) is lighter than air (M = 28.8), so $\rho$ falls and $v$ rises.
:::

**Group B — Short answer (5 marks each)**

1. Derive Newton's formula for the velocity of sound in a gas and state the
   assumption on which it rests. Why does it fail? <span class="marks">[5]</span>
2. State and explain Laplace's correction. Show that it raises the calculated
   velocity in air at NTP from about 280 m s⁻¹ to about 331 m s⁻¹.
   (Take $P=1.013\times10^{5}\ \text{Pa}$, $\rho=1.293\ \text{kg m}^{-3}$, $\gamma=1.4$.) <span class="marks">[5]</span>
3. Show that the velocity of sound in air increases by about 0.61 m s⁻¹ for a
   rise of 1 °C, given that it is 332 m s⁻¹ at 0 °C. <span class="marks">[5]</span>
4. The velocity of sound in a certain liquid is 1500 m s⁻¹ and its density is
   1200 kg m⁻³. Find the bulk modulus of the liquid. <span class="marks">[5]</span>
5. Explain why sound travels faster in solids than in liquids, and faster in
   liquids than in gases, even though solids are the densest of the three. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Isothermal assumption, $PV=$ const, $P\,dV+V\,dP=0$, hence $B=P$ and
$v=\sqrt{P/\rho}$. It gives 280 m s⁻¹ against a measured 332 m s⁻¹ — a 16 %
error — because sound compressions are far too rapid, and air far too poor a
conductor, for the heat to escape.

**2.** Adiabatic: $PV^{\gamma}=$ const gives $B=\gamma P$, so $v=\sqrt{\gamma P/\rho}$.
Numerically $\sqrt{1.013\times10^{5}/1.293}=280\ \text{m s}^{-1}$, and
$280\times\sqrt{1.4}=280\times1.183=331\ \text{m s}^{-1}$.

**3.** $v_t=v_0(1+t/273)^{1/2}\approx v_0(1+t/546)$, so
$v_t-v_0 = v_0 t/546 = (332/546)t = 0.61t$. For $t=1\ ^{\circ}\text{C}$ the
increase is 0.61 m s⁻¹.

**4.** $v=\sqrt{B/\rho}\Rightarrow B=\rho v^{2}=1200\times(1500)^{2}
= 1200\times2.25\times10^{6} = 2.7\times10^{9}\ \text{Pa}$.

**5.** Speed is $\sqrt{E/\rho}$. Going gas → liquid → solid the density rises by
a factor of roughly $10^{3}$ and then 8, but the elastic modulus rises by a far
larger factor (about $10^{4}$ from air to water and about $10^{2}$ again from
water to steel). Stiffness therefore wins over inertia.
:::

**Group C — Long answer (8 marks each)**

1. (a) Starting from $v=\sqrt{E/\rho}$, derive Newton's formula for the speed of
   sound in a gas and explain why it disagrees with experiment. <span class="marks">[4]</span>
   (b) State Laplace's correction, derive the corrected formula, and hence show
   that $v=\sqrt{\gamma RT/M}$. Use this to explain the effect of pressure,
   temperature and humidity on the speed of sound. <span class="marks">[4]</span>
2. (a) A gun is fired in a valley at Pokhara and the echo from a cliff is heard
   after 2.5 s on a day when the temperature is 20 °C. Taking the speed of sound
   at 0 °C as 332 m s⁻¹, find the distance of the cliff. <span class="marks">[4]</span>
   (b) The same gun is fired when the temperature has fallen to 5 °C. By how much
   does the echo time change? <span class="marks">[4]</span>

::: note Answer to Group C question 2
(a) $v_{20} = 332 + 0.61\times20 = 332+12.2 = 344.2\ \text{m s}^{-1}$.
Path length $=2d = 344.2\times2.5 = 860.5\ \text{m}$, so $d = 430\ \text{m}$.

(b) $v_{5} = 332 + 0.61\times5 = 335.05\ \text{m s}^{-1}$.
The cliff has not moved, so $2d = 860.5\ \text{m}$ still and

$$ t = \frac{860.5}{335.05} = 2.57\ \text{s} $$

The echo now takes about 0.07 s longer — a small but measurable delay, and a
reminder that any echo or resonance-tube measurement of $v$ must record the air
temperature.
:::
