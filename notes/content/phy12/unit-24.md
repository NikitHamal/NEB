---
subject: Physics
grade: 12
unit: 24
title: Radioactivity and nuclear reaction
hours: 6
area: Modern Physics
---

Becquerel found in 1896 that uranium salts fogged a wrapped photographic plate
in a locked drawer. No chemistry, no heating and no light could switch the
effect on or off — it came from inside the nucleus. **Radioactivity** is the
spontaneous breakup of an unstable nucleus, and because it is spontaneous and
random it obeys a statistical law rather than a mechanical one. This unit sets
out that law, the instrument that counts the decays, and the two places Nepali
students meet radioactivity in ordinary life: dating old things and treating
cancer.

::: key What the exam wants from this unit
The derivation of $N = N_0e^{-\lambda t}$ from $dN/dt = -\lambda N$, the three
relations $T_{1/2} = 0.693/\lambda$, $\tau = 1/\lambda = 1.44\,T_{1/2}$ and
$A = \lambda N$, the labelled GM tube, and a dating or activity numerical.
Learn to spot "$n$ half-lives" problems — they need no calculus at all.
:::

## 24.1 Alpha-particles, Beta-particles, Gamma rays

A nucleus is held together by the short-range **strong nuclear force** against
the electrostatic repulsion of its protons. Plotting the **binding energy per
nucleon** against mass number shows where stability lies.

```figure caption="Binding energy per nucleon against mass number. The peak near $A \\approx 56$ (iron and nickel) is the most tightly bound region; light nuclei gain energy by fusing and heavy nuclei by splitting or by emitting an $\\alpha$-particle."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0, 3.0))
A = np.array([2,3,4,6,7,9,11,12,14,16,19,20,23,24,27,28,32,35,40,45,50,56,
              59,63,75,85,100,120,140,160,180,200,220,235,238])
B = np.array([1.11,2.83,7.07,5.33,5.61,6.46,6.93,7.68,7.48,7.98,7.78,8.03,
              8.11,8.26,8.33,8.45,8.49,8.52,8.55,8.62,8.76,8.79,8.77,8.75,
              8.70,8.70,8.61,8.50,8.38,8.18,8.02,7.91,7.74,7.59,7.57])
ax.plot(A, B, color=ACCENT, lw=1.7, zorder=3)
for a, b, lab, off in [(4,7.07,'⁴He',(7,-2)), (56,8.79,'⁵⁶Fe',(-5,8)),
                       (235,7.59,'²³⁵U',(-26,-15)), (2,1.11,'²H',(6,-3))]:
    ax.plot([a],[b],'o',color=SERIES[1], ms=5, zorder=4)
    ax.annotate(lab, (a,b), xytext=off, textcoords='offset points',
                fontsize=8.4, color=SERIES[1])
ax.annotate('', xy=(46,4.0), xytext=(8,4.0),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[2], lw=1.4, mutation_scale=11))
ax.annotate('fusion', (27,4.3), ha='center', fontsize=8.4, color=SERIES[2])
ax.annotate('', xy=(70,4.0), xytext=(232,4.0),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[3], lw=1.4, mutation_scale=11))
ax.annotate('fission / α-emission', (151,4.3), ha='center', fontsize=8.4, color=SERIES[3])
ax.set_xlabel('mass number  A'); ax.set_ylabel('binding energy per nucleon (MeV)')
ax.set_xlim(0, 250); ax.set_ylim(0, 9.6)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=0.45)
```

Nuclei with $A > 209$ have no stable form: emitting particles moves them towards
the peak and releases energy. Three kinds of radiation come out.

```figure caption="Separating the three radiations. With the magnetic field into the page, the positive $\\alpha$-particles bend one way, the negative $\\beta$-particles bend much further the other way (they are far lighter), and the uncharged $\\gamma$-rays go straight on."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(4.6, 3.2))

ax.add_patch(Rectangle((-0.9, -1.25), 1.8, 0.95, fc='#c9ced8', ec=INK, lw=1.1))
ax.add_patch(Rectangle((-0.16, -0.95), 0.32, 0.65, fc='white', ec=INK, lw=0.9))
ax.plot([0], [-0.75], 'o', color=SERIES[1], ms=5)
ax.annotate('radioactive source\nin lead block', (0, -1.38), ha='center',
            va='top', fontsize=7.8, color=INK)

for x in np.arange(-1.6, 1.7, 0.45):
    for y in np.arange(0.2, 2.9, 0.45):
        ax.annotate('×', (x, y), ha='center', va='center', fontsize=7, color=GRID)
ax.annotate('magnetic field into page', (-1.85, 1.5), rotation=90, ha='center',
            va='center', fontsize=7.6, color=MUTED)

ax.plot([0, 0], [-0.75, 0.0], color=MUTED, lw=1.6)
y = np.linspace(0, 3.0, 200)
ax.plot(-0.055*y**2, y, color=SERIES[3], lw=1.8)
ax.plot(0.126*y**2, y, color=SERIES[0], lw=1.8)
ax.plot(np.zeros_like(y), y, color=SERIES[2], lw=1.8, ls='-')
ax.annotate('α', (-0.055*9, 3.05), ha='center', fontsize=11, color=SERIES[3])
ax.annotate('γ', (0.0, 3.05), ha='center', fontsize=11, color=SERIES[2])
ax.annotate('β', (0.126*9, 3.05), ha='center', fontsize=11, color=SERIES[0])
ax.plot([-1.9, 1.9], [3.35, 3.35], color=INK, lw=2.2)
ax.annotate('photographic plate', (0, 3.48), ha='center', fontsize=7.8, color=INK)
ax.set_xlim(-2.3, 2.1); ax.set_ylim(-2.0, 3.9)
ax.axis('off')
```

| Property | Alpha ($\alpha$) | Beta ($\beta^-$) | Gamma ($\gamma$) |
|---|---|---|---|
| Nature | helium nucleus, ⁴₂He | fast electron | electromagnetic photon |
| Charge | $+2e$ | $-e$ | 0 |
| Mass | $4u = 6.64\times10^{-27}$ kg | $9.1\times10^{-31}$ kg | 0 (rest mass) |
| Speed | $\approx 0.05c$ | up to $0.99c$ | $c$ |
| Ionizing power | very high (10⁴) | moderate (10²) | low (1) |
| Penetrating power | low (1) | moderate (100) | very high (10⁴) |
| Stopped by | a sheet of paper | 3 mm aluminium | several cm of lead |
| Deflection in field | small | large, opposite way | none |
| Effect on nucleus | $A-4$, $Z-2$ | $A$ same, $Z+1$ | no change |

::: memory Ionizing and penetrating power run opposite ways
$\alpha$ is the best ionizer and the worst penetrator; $\gamma$ is the reverse.
The reason is the same for both: an $\alpha$-particle is heavy and doubly
charged, so it loses energy fast in a short distance.
:::

The last row is the **Soddy–Fajans displacement law**:

²³⁸₉₂U → ²³⁴₉₀Th + ⁴₂He  (alpha decay)
²³⁴₉₀Th → ²³⁴₉₁Pa + ⁰₋₁e + ν̄  (beta decay; inside the nucleus n → p + e⁻ + ν̄)

Gamma emission follows either of these: the daughter nucleus is left excited and
drops to its ground state by emitting a photon, typically 0.1–3 MeV.

::: caution The beta particle is not an orbital electron
The nucleus contains no electrons (see the uncertainty-principle argument in
Unit 23). The $\beta$-particle is **created** at the instant a neutron converts
into a proton. An antineutrino is emitted with it, which is why $\beta$ energies
form a continuous spectrum while $\alpha$ energies are sharp.
:::

The energy released in a decay is the **Q-value**, $Q = \Delta m \times 931.5$
MeV, where $\Delta m$ is the mass lost. A positive $Q$ means the decay is
energetically allowed.

::: example Worked example 24.1
**Problem.** Find the energy released when ²³⁸U decays by alpha emission. Atomic
masses: ²³⁸U $= 238.050788$ u, ²³⁴Th $= 234.043601$ u, ⁴He $= 4.002603$ u.

**Solution.** Mass of products $= 234.043601 + 4.002603 = 238.046204$ u.

$$ \Delta m = 238.050788 - 238.046204 = 0.004584\ \text{u} $$

$$ Q = 0.004584 \times 931.5 = 4.27\ \text{MeV} $$

Almost all of this appears as kinetic energy of the light $\alpha$-particle,
which is why $\alpha$-particles from a given nuclide all have the same energy.
:::

## 24.2 Laws of radioactive disintegration

::: definition The laws of radioactive disintegration
1. Radioactivity is a **spontaneous and random** nuclear process. It is not
   affected by temperature, pressure, chemical combination or any other physical
   condition. Which particular nucleus decays next cannot be predicted.
2. The **rate of disintegration** at any instant is directly proportional to the
   number of undecayed nuclei present at that instant.
:::

::: derivation The exponential decay law
Let $N$ be the number of undecayed nuclei at time $t$. By the second law,

$$ -\frac{dN}{dt} \propto N \qquad \Rightarrow \qquad \frac{dN}{dt} = -\lambda N $$

where $\lambda$ is the **decay constant**, a property of the nuclide. The minus
sign shows $N$ decreases. Separating the variables,

$$ \frac{dN}{N} = -\lambda\,dt $$

and integrating from $N = N_0$ at $t = 0$ to $N$ at time $t$:

$$ \int_{N_0}^{N}\frac{dN}{N} = -\lambda\int_{0}^{t} dt
\qquad \Rightarrow \qquad \ln\frac{N}{N_0} = -\lambda t $$

$$ \boxed{N = N_0 e^{-\lambda t}} $$
:::

The **activity** $A$ is the number of disintegrations per second,
$A = -dN/dt = \lambda N$. Multiplying the decay law by $\lambda$,

$$ A = A_0 e^{-\lambda t} $$

so activity — which is what a counter actually measures — falls off with the
same exponential. The SI unit of activity is the **becquerel** (1 Bq = 1
disintegration per second); the older unit is the **curie**,
$1\ \text{Ci} = 3.7\times10^{10}$ Bq.

::: definition Decay constant
$\lambda$ is the probability per unit time that a given nucleus will decay. Its
unit is s⁻¹. From $N = N_0e^{-\lambda t}$, putting $t = 1/\lambda$ gives
$N = N_0/e$, so $\lambda$ is the reciprocal of the time in which the number of
undecayed nuclei falls to $1/e$ (about 37%) of its initial value.
:::

## 24.3 Half-life, mean-life and decay constant

```figure caption="Radioactive decay curve. In every half-life $T_{1/2}$ the number of undecayed nuclei is halved, whatever the starting point. The mean life $\\tau = 1.44\\,T_{1/2}$ is where the curve has fallen to $1/e = 0.37$ of $N_0$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0, 3.0))
x = np.linspace(0, 4.6, 500)
ax.plot(x, 0.5**x, color=ACCENT, lw=1.9, zorder=3)
for k in (1, 2, 3):
    y = 0.5**k
    ax.plot([0, k], [y, y], color=MUTED, lw=0.9, ls=':')
    ax.plot([k, k], [0, y], color=MUTED, lw=0.9, ls=':')
    ax.plot([k], [y], 'o', color=ACCENT, ms=4.5, zorder=4)
tau = 1/np.log(2)
ax.plot([0, tau], [1/np.e]*2, color=SERIES[1], lw=1.0, ls='--')
ax.plot([tau, tau], [0, 1/np.e], color=SERIES[1], lw=1.0, ls='--')
ax.annotate('τ = 1.44 T₁/₂', (tau, 0.40), xytext=(26, 16),
            textcoords='offset points', fontsize=8.4, color=SERIES[1],
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.0, mutation_scale=9))
ax.annotate('N₀/e = 0.37 N₀', (0.05, 1/np.e + 0.03), fontsize=8, color=SERIES[1])
ax.set_xticks([0, 1, 2, 3, 4])
ax.set_xticklabels(['0', 'T₁/₂', '2T₁/₂', '3T₁/₂', '4T₁/₂'])
ax.set_yticks([0, 0.125, 0.25, 0.5, 1.0])
ax.set_yticklabels(['0', 'N₀/8', 'N₀/4', 'N₀/2', 'N₀'])
ax.set_xlabel('time  t'); ax.set_ylabel('undecayed nuclei  N')
ax.set_xlim(0, 4.6); ax.set_ylim(0, 1.08)
ax.spines[['top', 'right']].set_visible(False); ax.grid(True, alpha=0.4)
```

::: derivation Half-life and mean life
**Half-life** $T_{1/2}$ is the time in which half the nuclei present decay.
Putting $N = N_0/2$ at $t = T_{1/2}$ in $N = N_0e^{-\lambda t}$:

$$ \frac{1}{2} = e^{-\lambda T_{1/2}} \Rightarrow e^{\lambda T_{1/2}} = 2
\Rightarrow \lambda T_{1/2} = \ln 2 $$

$$ \boxed{T_{1/2} = \frac{\ln 2}{\lambda} = \frac{0.693}{\lambda}} $$

**Mean life** $\tau$ is the average lifetime of all the nuclei. The number
decaying between $t$ and $t+dt$ is $\lambda N\,dt$, each having lived a time $t$,
so

$$ \tau = \frac{1}{N_0}\int_{0}^{\infty} t\,\lambda N_0 e^{-\lambda t}\,dt
= \lambda \int_{0}^{\infty} t e^{-\lambda t}\,dt = \lambda \cdot \frac{1}{\lambda^{2}} $$

$$ \boxed{\tau = \frac{1}{\lambda} = \frac{T_{1/2}}{0.693} = 1.44\,T_{1/2}} $$
:::

After $n$ half-lives ($n = t/T_{1/2}$), the surviving fraction is

$$ \frac{N}{N_0} = \left(\frac{1}{2}\right)^{n} $$

which handles most exam numericals without any logarithms.

| $T_{1/2}$ | Nuclide | Typical use |
|---|---|---|
| 110 minutes | fluorine-18 | PET brain and cancer scans |
| 6.0 hours | technetium-99m | bone and kidney scans |
| 8.0 days | iodine-131 | thyroid diagnosis and therapy |
| 5.27 years | cobalt-60 | teletherapy, sterilizing equipment |
| 5730 years | carbon-14 | archaeological dating |
| $4.5\times10^{9}$ years | uranium-238 | dating rocks and the Earth |

::: example Worked example 24.2
**Problem.** The activity of a radioactive sample falls from 8000 counts per
minute to 500 counts per minute in 24 hours. Find the half-life, the decay
constant and the mean life.

**Solution.** $\dfrac{A_0}{A} = \dfrac{8000}{500} = 16 = 2^{4}$, so 4 half-lives
have passed.

$$ T_{1/2} = \frac{24\ \text{h}}{4} = 6\ \text{h} $$

$$ \lambda = \frac{0.693}{T_{1/2}} = \frac{0.693}{6} = 0.1155\ \text{h}^{-1}
= \frac{0.1155}{3600} = 3.21\times10^{-5}\ \text{s}^{-1} $$

$$ \tau = \frac{1}{\lambda} = \frac{1}{0.1155} = 8.66\ \text{h} $$
:::

::: example Worked example 24.3
**Problem.** Calculate the activity of 1.0 g of radium-226, whose half-life is
1600 years. Take 1 year $= 3.156\times10^{7}$ s and
$N_A = 6.022\times10^{23}\ \text{mol}^{-1}$.

**Solution.** Number of nuclei in 1.0 g:

$$ N = \frac{1.0}{226}\times 6.022\times10^{23} = 2.665\times10^{21} $$

Decay constant:

$$ \lambda = \frac{0.693}{1600 \times 3.156\times10^{7}}
= \frac{0.693}{5.050\times10^{10}} = 1.372\times10^{-11}\ \text{s}^{-1} $$

$$ A = \lambda N = (1.372\times10^{-11})(2.665\times10^{21})
= 3.66\times10^{10}\ \text{Bq} $$

This is almost exactly $3.7\times10^{10}$ Bq — and that is no accident: the
curie was originally *defined* as the activity of one gram of radium.
:::

::: caution Half-life is not "half the total life"
A sample never disappears. After $2T_{1/2}$ one quarter remains, after
$3T_{1/2}$ one eighth, and so on — the decay law is exponential, so the number
never reaches zero. Also, $T_{1/2}$ is fixed for a nuclide: it cannot be changed
by heating, cooling or chemical reaction.
:::

## 24.4 Geiger-Muller Tube

The GM tube converts a single ionizing particle into an electrical pulse big
enough to count.

```figure caption="Geiger–Müller tube. A particle entering the mica window ionizes the argon; the freed electrons are accelerated to the thin central anode, where they trigger an avalanche that produces a pulse across $R$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.0, 3.2))

ax.add_patch(Rectangle((1.0, 1.3), 5.6, 2.4, fc='#eef2f7', ec=INK, lw=1.4))
ax.add_patch(Rectangle((1.3, 1.6), 5.0, 1.8, fc='none', ec=MUTED, lw=1.8))
ax.annotate('glass envelope', (3.8, 3.86), ha='center', fontsize=7.8, color=INK)
ax.annotate('metal cathode (cylinder, −)', (3.8, 3.12), ha='center',
            va='center', fontsize=7.6, color=MUTED)

ax.plot([1.5, 6.1], [2.60, 2.60], color=SERIES[3], lw=2.0)
ax.annotate('thin tungsten anode wire (+)', (3.9, 2.42), ha='center', va='top',
            fontsize=7.6, color=SERIES[3])
ax.annotate('low-pressure argon + bromine vapour', (3.9, 1.88),
            ha='center', va='center', fontsize=7.4, color=MUTED)

ax.plot([1.0, 1.0], [1.3, 3.7], color=SERIES[2], lw=3.2)
ax.annotate('thin mica\nwindow', (0.80, 2.4), ha='right', va='center',
            fontsize=7.6, color=SERIES[2])
ax.annotate('', xy=(1.75, 2.95), xytext=(0.35, 4.05),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.5, mutation_scale=11))
ax.annotate('ionizing particle', (0.25, 4.14), ha='left', va='bottom',
            fontsize=7.6, color=SERIES[1])

ax.plot([6.1, 7.25], [2.60, 2.60], color=INK, lw=1.1)
ax.add_patch(Rectangle((7.25, 2.42), 0.95, 0.36, fc='white', ec=INK, lw=1.1))
ax.annotate('R', (7.72, 2.60), ha='center', va='center', fontsize=8.6, color=INK)
ax.plot([8.20, 8.95], [2.60, 2.60], color=INK, lw=1.1)
ax.plot([8.95, 8.95], [2.60, 0.60], color=INK, lw=1.1)
ax.plot([8.95, 1.0], [0.60, 0.60], color=INK, lw=1.1)
ax.plot([1.0, 1.0], [0.60, 1.3], color=INK, lw=1.1)
ax.plot([4.9, 4.9], [0.40, 0.80], color=INK, lw=1.7)
ax.plot([5.2, 5.2], [0.50, 0.70], color=INK, lw=1.7)
ax.annotate('400 V d.c.', (5.05, 0.22), ha='center', fontsize=7.8, color=INK)
ax.plot([7.72, 7.72], [2.78, 3.42], color=INK, lw=1.1)
ax.add_patch(Rectangle((7.05, 3.42), 1.35, 0.62, fc='#eef2f7', ec=INK, lw=1.1))
ax.annotate('counter', (7.72, 3.73), ha='center', va='center', fontsize=7.8, color=INK)

ax.set_xlim(-0.3, 9.4); ax.set_ylim(0.0, 4.4)
ax.axis('off')
```

**Construction.** A cylindrical metal tube (the cathode) is sealed in glass with
a fine tungsten wire along its axis (the anode). One end is closed by a thin
**mica window** so that even $\alpha$-particles can get in. The tube is filled
with **argon** at about 0.1 atmosphere together with a little **bromine or
ethyl alcohol vapour**, which acts as a quenching agent. A p.d. of about 400 V
is applied through a high resistance $R$.

**Working.** An ionizing particle entering the window produces a few ion pairs.
The electric field near the thin wire is intense, so the freed electrons are
accelerated hard enough to ionize further atoms. The result is an **avalanche**
of about $10^{8}$ electrons reaching the anode within a microsecond. The current
through $R$ produces a voltage pulse, which is amplified and counted.

**Quenching and dead time.** The positive argon ions drift slowly to the
cathode, where they would release fresh electrons and restart the discharge. The
quenching vapour absorbs their energy and dissociates instead, stopping the
pulse. During the roughly $200\ \mu\text{s}$ the ions take to clear — the **dead
time** — the tube cannot register another particle, so true counts exceed
recorded counts at high rates.

**The plateau.** Plotting count rate against tube voltage for a fixed source
gives a flat **plateau** about 100 V wide. The tube is operated in the middle of
the plateau, so that small supply fluctuations do not change the reading. Above
the plateau a continuous discharge starts and destroys the tube.

::: tip What a GM tube can and cannot do
It counts $\alpha$, $\beta$ and $\gamma$ particles, but the pulse size is the
same whatever the particle's energy. So a GM tube measures **how many**, never
**how energetic** — energy measurement needs a scintillation counter instead.
:::

## 24.5 Carbon dating

Cosmic-ray neutrons striking nitrogen in the upper atmosphere make radioactive
carbon-14:

¹⁴₇N + ¹₀n → ¹⁴₆C + ¹₁H

The ¹⁴C mixes into atmospheric CO₂, so every living plant and animal keeps a
fixed ratio ¹⁴C : ¹²C of about $1.3\times10^{-12}$, giving an activity of
**15.3 disintegrations per minute per gram of carbon**. At death, intake stops
while the ¹⁴C keeps decaying back to nitrogen ($T_{1/2} = 5730$ years):

¹⁴₆C → ¹⁴₇N + ⁰₋₁e + ν̄

Measuring the present activity $A$ therefore dates the specimen:

$$ A = A_0e^{-\lambda t} \qquad \Rightarrow \qquad
t = \frac{1}{\lambda}\ln\frac{A_0}{A} = \frac{T_{1/2}}{0.693}\ln\frac{A_0}{A} $$

After about 10 half-lives the remaining activity is lost in the background, so
the method is useful to roughly **50,000 years**. It works only on once-living
material — wood, charcoal, bone, cloth. Radiocarbon dating of charcoal and
timber beneath the Maya Devi temple at **Lumbini** placed a wooden structure
there in about the sixth century BCE.

::: example Worked example 24.4
**Problem.** A piece of wood from an old temple beam gives 9.2 disintegrations
per minute per gram of carbon. Living wood gives 15.3 per minute per gram. Take
$T_{1/2}(^{14}\text{C}) = 5730$ years. How old is the beam?

**Solution.**

$$ \lambda = \frac{0.693}{5730} = 1.209\times10^{-4}\ \text{year}^{-1} $$

$$ t = \frac{1}{\lambda}\ln\frac{A_0}{A}
= \frac{1}{1.209\times10^{-4}}\ln\frac{15.3}{9.2} $$

$$ \ln(1.663) = 0.5087 \qquad \Rightarrow \qquad
t = \frac{0.5087}{1.209\times10^{-4}} = 4.21\times10^{3}\ \text{years} $$

The beam is about **4200 years** old.
:::

## 24.6 Medical use of nuclear radiation and possible health hazard

**Diagnosis.** A short-lived $\gamma$-emitting **tracer** is injected and a gamma
camera images where it collects. Technetium-99m ($T_{1/2} = 6$ h) is used for
bone, kidney and heart scans; iodine-131 concentrates in the thyroid;
fluorine-18 is the tracer in PET scans. Short half-lives are chosen so that the
activity dies away within a day.

**Therapy.** Cancer cells divide fast and are more easily killed by radiation
than normal cells. A **cobalt-60 teletherapy** unit aims 1.17 and 1.33 MeV
$\gamma$-rays at a tumour from several directions, so the tumour receives a
large dose while surrounding tissue receives little. In **brachytherapy** a
sealed iridium-192 seed is placed inside or beside the tumour. Iodine-131 is
drunk as a solution to destroy an over-active thyroid.

**Sterilization.** Syringes, dressings and surgical gloves are sealed in plastic
and sterilized by $\gamma$-rays, which kill bacteria without heating.

**Health hazards.** Radiation ionizes the molecules of living cells and can
break DNA strands. The effects are of two kinds:

- **Somatic** — affecting the exposed person: radiation burns, hair loss,
  sterility, cataract, anaemia, leukaemia and other cancers.
- **Genetic** — mutations in reproductive cells that are passed to children.

| Quantity | Definition | SI unit |
|---|---|---|
| Absorbed dose $D$ | energy absorbed per kg of tissue | gray (Gy), 1 Gy = 1 J kg⁻¹ |
| Equivalent dose $H$ | $H = D \times Q$ (quality factor: 1 for $\beta,\gamma$; 20 for $\alpha$) | sievert (Sv) |
| Activity $A$ | disintegrations per second | becquerel (Bq) |

Natural background radiation in Nepal delivers roughly 2–3 mSv per year from
cosmic rays, rocks and radon. Safety follows three simple rules: keep the
**time** of exposure short, keep your **distance** (intensity falls as
$1/r^{2}$), and use **shielding** — lead aprons, thick concrete walls, remote
handling tongs. Workers wear film badges or thermoluminescent dosimeters, and
radioactive waste is sealed in lead-lined containers.

## Chapter summary

- Binding energy per nucleon peaks near $A \approx 56$ at about 8.8 MeV; nuclei
  move towards the peak by fusing, splitting or emitting $\alpha$-particles.
- $\alpha$ = ⁴₂He ($A-4$, $Z-2$); $\beta^-$ = electron created when n → p
  ($Z+1$); $\gamma$ = photon (no change). Ionizing power $\alpha > \beta > \gamma$;
  penetrating power is the reverse.
- $Q = \Delta m \times 931.5$ MeV is the energy released in a decay.
- Decay law: $dN/dt = -\lambda N$ gives $N = N_0e^{-\lambda t}$ and
  $A = \lambda N = A_0e^{-\lambda t}$. 1 Ci $= 3.7\times10^{10}$ Bq.
- $T_{1/2} = 0.693/\lambda$; $\tau = 1/\lambda = 1.44\,T_{1/2}$; after $n$
  half-lives $N/N_0 = (1/2)^n$.
- A GM tube uses avalanche ionization in argon at 400 V, with a quenching vapour
  and a dead time of about $200\ \mu$s; it counts particles but not their energy.
- Carbon dating: $t = (T_{1/2}/0.693)\ln(A_0/A)$ with $A_0 = 15.3$ min⁻¹ g⁻¹ and
  $T_{1/2} = 5730$ y; useful to about 50,000 years.
- Medical tracers are short-lived $\gamma$-emitters; therapy uses cobalt-60.
  Dose is measured in gray (absorbed) and sievert (equivalent).

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. When a nucleus emits a $\beta^-$ particle, its mass number and atomic number <span class="marks">[1]</span>
   (a) both decrease (b) $A$ unchanged, $Z$ increases by 1
   (c) $A$ decreases by 4, $Z$ by 2 (d) both unchanged
2. The decay constant of a nuclide of half-life 20 minutes is <span class="marks">[1]</span>
   (a) $0.0347\ \text{min}^{-1}$ (b) $0.693\ \text{min}^{-1}$
   (c) $20\ \text{min}^{-1}$ (d) $28.8\ \text{min}^{-1}$
3. After 3 half-lives, the fraction of a radioactive sample left undecayed is <span class="marks">[1]</span>
   (a) $1/3$ (b) $1/6$ (c) $1/8$ (d) $1/9$
4. The gas commonly used in a Geiger–Müller tube is <span class="marks">[1]</span>
   (a) hydrogen (b) argon (c) oxygen (d) nitrogen
5. Carbon dating cannot be used to find the age of <span class="marks">[1]</span>
   (a) an old wooden beam (b) charcoal from a fireplace
   (c) a granite boulder (d) a bone

::: note Answers to Group A
**1.** (b) — a neutron becomes a proton, so $Z$ rises by 1 and $A$ is unchanged.
**2.** (a) — $\lambda = 0.693/20 = 0.0347\ \text{min}^{-1}$.
**3.** (c) — $(1/2)^3 = 1/8$.
**4.** (b) — argon, an inert gas, with a bromine or alcohol quenching vapour.
**5.** (c) — granite was never alive, so it never took up ¹⁴C.
:::

**Group B — Short answer (5 marks each)**

1. State the laws of radioactive disintegration and hence derive
   $N = N_0e^{-\lambda t}$. <span class="marks">[5]</span>
2. Define half-life and mean life, and show that
   $\tau = 1.44\,T_{1/2}$. <span class="marks">[5]</span>
3. Calculate the binding energy per nucleon of ⁴₂He. Take mass of ⁴He
   $= 4.002603$ u, of ¹H $= 1.007825$ u, of a neutron $= 1.008665$ u and
   $1\ \text{u} = 931.5\ \text{MeV}$. <span class="marks">[5]</span>
4. A radioactive sample has a half-life of 10 days. Find its decay constant in
   s⁻¹ and the fraction of the sample remaining after 30 days. <span class="marks">[5]</span>

::: note Answers to Group B
**2.** Definitions as in §24.3. $T_{1/2} = 0.693/\lambda$ and
$\tau = 1/\lambda$, so $\tau = T_{1/2}/0.693 = 1.44\,T_{1/2}$.

**3.** ⁴He has 2 protons and 2 neutrons. Sum of separate masses
$= 2(1.007825) + 2(1.008665) = 2.015650 + 2.017330 = 4.032980$ u.
$\Delta m = 4.032980 - 4.002603 = 0.030377$ u.
Binding energy $= 0.030377 \times 931.5 = 28.30$ MeV, so
BE per nucleon $= 28.30/4 = 7.07$ MeV.

**4.** $\lambda = 0.693/T_{1/2} = 0.693/10 = 0.0693\ \text{day}^{-1}$. In SI,
$\lambda = 0.693/(10 \times 86400\ \text{s}) = 0.693/864000
= 8.02\times10^{-7}\ \text{s}^{-1}$.
After 30 days $= 3$ half-lives, $N/N_0 = (1/2)^3 = 1/8 = 0.125$, i.e. 12.5%.
:::

**Group C — Long answer (8 marks each)**

1. (a) Draw a labelled diagram of a Geiger–Müller tube and explain how it
   detects a single ionizing particle. <span class="marks">[5]</span>
   (b) What is meant by quenching and dead time? Why is the tube operated on the
   plateau of its characteristic curve? <span class="marks">[3]</span>
2. (a) Derive the relation between half-life and decay constant. <span class="marks">[3]</span>
   (b) A radioactive source contains $1.0\times10^{20}$ nuclei of a nuclide whose
   half-life is 8 hours. Calculate the decay constant, the initial activity, and
   the activity after 24 hours. <span class="marks">[5]</span>

::: note Answer to Group C question 2(b)
$$ \lambda = \frac{0.693}{8 \times 3600} = \frac{0.693}{28800}
= 2.41\times10^{-5}\ \text{s}^{-1} $$

$$ A_0 = \lambda N_0 = (2.41\times10^{-5})(1.0\times10^{20})
= 2.41\times10^{15}\ \text{Bq} $$

24 hours is exactly 3 half-lives, so $N = N_0/8 = 1.25\times10^{19}$ and

$$ A = \lambda N = (2.41\times10^{-5})(1.25\times10^{19})
= 3.01\times10^{14}\ \text{Bq} $$

(equivalently $A = A_0/8$).
:::
