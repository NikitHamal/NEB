---
subject: Physics
grade: 11
unit: 26
title: Recent Trends in physics
hours: 6
area: Modern Physics
---

The last hundred years have pushed physics to both ends of the scale. Downwards,
the atom has been opened up to reveal quarks and leptons — particles with no
known internal structure. Upwards, the same equations describe a universe
13.8 billion years old, still expanding, and mostly made of something nobody has
yet held in a laboratory. This unit tours both frontiers. Much of it is
descriptive, but the numbers matter too: Hubble's law, the size of a black
hole and the charge of a quark are all things you can be asked to calculate.

::: key How this unit is examined
Most marks come from **definitions, classifications and evidence**: the quark
content of a proton, why neutrinos are hard to detect, three pieces of evidence
for the Big Bang. Learn the tables and the dates. But be ready for short
numerical parts as well — adding up quark charges, using $v = H_0 d$, and
putting a mass into $R_s = 2GM/c^{2}$ are all fair game.
:::

## 26.1 Particle physics

### Particles and antiparticles

In 1928 **P. A. M. Dirac** combined quantum mechanics with special relativity.
His equation had negative-energy solutions which he interpreted as a new
particle: an electron with positive charge. In 1932 **Carl Anderson** found it
in cosmic-ray tracks in a cloud chamber and named it the **positron**.

::: definition Antiparticle
For every particle there exists an antiparticle having the **same mass, the same
spin and the same lifetime**, but **opposite** electric charge, magnetic moment
and other internal quantum numbers (lepton number, baryon number, strangeness).
:::

Antiparticles are written with a bar or the opposite charge sign: antiproton
$\bar{p}$, antineutrino $\bar{\nu}$, antielectron $e^{+}$. The antiproton was made
in 1955 at the Bevatron. A few particles — the photon, the neutral pion — are
their own antiparticles.

Two processes connect matter and energy directly:

- **Pair production.** A photon passing close to a heavy nucleus converts into a
  particle–antiparticle pair: $\gamma \rightarrow e^{-} + e^{+}$. It needs at
  least $2m_ec^{2} = 1.02\ \text{MeV}$; the nucleus is needed to conserve momentum.
- **Annihilation.** A particle meeting its antiparticle disappears, the whole
  rest energy becoming radiation: $e^{-} + e^{+} \rightarrow 2\gamma$, with each
  photon carrying $0.511\ \text{MeV}$ — the principle behind the hospital PET scan.

::: example Worked example 26.1
**Problem.** An electron and a positron, both at rest, annihilate to give two
identical photons. Find the energy, frequency and wavelength of each photon.
Take $m_e = 9.1\times10^{-31}\ \text{kg}$, $h = 6.63\times10^{-34}\ \text{J s}$.

**Solution.** The total rest energy shared between two photons is $2m_ec^{2}$, so
each photon gets $m_ec^{2}$:

$$ E = m_ec^{2} = 9.1\times10^{-31}\times(3\times10^{8})^{2}
= 8.19\times10^{-14}\ \text{J} $$

$$ f = \frac{E}{h} = \frac{8.19\times10^{-14}}{6.63\times10^{-34}}
= 1.24\times10^{20}\ \text{Hz} $$

$$ \lambda = \frac{c}{f} = \frac{3\times10^{8}}{1.24\times10^{20}}
= 2.4\times10^{-12}\ \text{m} $$

Both are gamma rays, emitted back to back so that momentum stays zero.
:::

### Classification of particles

Every particle is either a **fermion** (matter, half-integer spin, obeys the
Pauli exclusion principle) or a **boson** (force carrier, integer spin). Fermions
divide into **quarks**, which feel the strong force, and **leptons**, which
do not.

```figure caption="Classification of the fundamental particles. Hadrons are not elementary: they are bound states of quarks."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.2,3.0))
def node(x, y, txt, c=INK, fs=8.0):
    ax.annotate(txt, (x, y), ha='center', va='center', fontsize=fs, color=c,
                bbox=dict(boxstyle='round,pad=0.30', fc='none', ec=c, lw=0.9))
def link(x1, y1, x2, y2):
    ax.plot([x1, x1, x2, x2], [y1, (y1+y2)/2, (y1+y2)/2, y2],
            color=MUTED, lw=0.9, solid_joinstyle='miter')
node(3.0, 3.55, 'ELEMENTARY PARTICLES', INK, 8.6)
for x, t in [(1.25,'Quarks  (6 flavours)'), (4.65,'Leptons  (6)')]:
    link(3.0, 3.40, x, 2.74); node(x, 2.58, t, ACCENT, 8.0)
for xa, xb, t in [(1.25,0.62,'Baryons  $qqq$\np, n, $\\Lambda^{0}$'),
                  (1.25,2.08,'Mesons  $q\\bar{q}$\n$\\pi^{\\pm}$, $K^{+}$')]:
    link(xa, 2.42, xb, 1.68); node(xb, 1.44, t, SERIES[1], 7.8)
for xa, xb, t in [(4.65,3.82,'Charged\n$e,\\ \\mu,\\ \\tau$'),
                  (4.65,5.42,'Neutral\n$\\nu_e,\\nu_\\mu,\\nu_\\tau$')]:
    link(xa, 2.42, xb, 1.68); node(xb, 1.44, t, SERIES[2], 7.8)
ax.plot([0.14, 0.14, 2.60, 2.60], [1.02, 0.86, 0.86, 1.02], color=SERIES[1], lw=0.9)
ax.annotate('HADRONS — the particles that feel the strong force', (1.37, 0.74),
            ha='center', va='top', fontsize=7.6, color=SERIES[1])
ax.set_xlim(-0.1, 6.2); ax.set_ylim(0.32, 3.92); ax.axis('off')
```

| Force | Relative strength | Exchange particle | Range |
|---|---|---|---|
| Strong | $1$ | gluon | $\sim 10^{-15}\ \text{m}$ |
| Electromagnetic | $10^{-2}$ | photon | infinite |
| Weak | $10^{-6}$ | $W^{\pm}, Z^{0}$ | $\sim 10^{-18}\ \text{m}$ |
| Gravitational | $10^{-39}$ | graviton (not yet found) | infinite |

### Quarks: baryons and mesons

In 1964 **Murray Gell-Mann** and **George Zweig** independently proposed that the
hundreds of known hadrons are not elementary but are built from a few
constituents, which Gell-Mann named **quarks**. Six flavours are known; the
last, the top quark, was found at Fermilab in 1995.

| Generation | Flavour | Symbol | Charge |
|---|---|---|---|
| First | up | $u$ | $+\frac{2}{3}e$ |
| First | down | $d$ | $-\frac{1}{3}e$ |
| Second | charm | $c$ | $+\frac{2}{3}e$ |
| Second | strange | $s$ | $-\frac{1}{3}e$ |
| Third | top | $t$ | $+\frac{2}{3}e$ |
| Third | bottom | $b$ | $-\frac{1}{3}e$ |

Quarks alone carry fractional charge. Each has baryon number $+\frac{1}{3}$ and a
property called **colour** — the "charge" of the strong force. Hadrons come in
exactly two combinations:

- **Baryons** — three quarks, $qqq$, baryon number $+1$. Proton $= uud$, giving
  charge $\frac{2}{3}+\frac{2}{3}-\frac{1}{3} = +1$. Neutron $= udd$, giving
  $\frac{2}{3}-\frac{1}{3}-\frac{1}{3} = 0$. The $\Lambda^{0} = uds$.
- **Mesons** — a quark and an antiquark, $q\bar{q}$, baryon number $0$. The
  $\pi^{+} = u\bar{d}$ and the $K^{+} = u\bar{s}$. All mesons are unstable.

::: example Worked example 26.2
**Problem.** Using the quark charges in the table, work out the electric charge
and the baryon number of (a) the combination $uds$ and (b) the combination
$u\bar{s}$. In each case say whether it is a baryon or a meson and name it.

**Solution.** Every quark has baryon number $+\frac{1}{3}$; every antiquark has
$-\frac{1}{3}$. An antiquark also carries the **opposite** charge to its quark.

(a) $uds$ is three quarks, so it is a **baryon**. Adding the charges from the
table,

$$ Q = +\frac{2}{3} - \frac{1}{3} - \frac{1}{3} = \frac{2 - 1 - 1}{3} = 0 $$

$$ B = \frac{1}{3} + \frac{1}{3} + \frac{1}{3} = +1 $$

A neutral baryon: this is the $\Lambda^{0}$.

(b) $u\bar{s}$ is one quark with one antiquark, so it is a **meson**. The $s$
quark has charge $-\frac{1}{3}$, so $\bar{s}$ has $+\frac{1}{3}$:

$$ Q = +\frac{2}{3} + \frac{1}{3} = \frac{2 + 1}{3} = +1 $$

$$ B = +\frac{1}{3} - \frac{1}{3} = 0 $$

A meson of charge $+1$: this is the $K^{+}$.
:::

::: key Quark confinement
No free quark has ever been seen. The strong force between two quarks does not
weaken with distance, so pulling them apart costs ever more energy until it is
cheaper to create a new quark–antiquark pair. You always end up with more
hadrons, never a loose quark.
:::

### Leptons and neutrinos

**Leptons** are elementary fermions that do not feel the strong force. There are
six, in three generations, each charged lepton paired with its own neutrino.

| Generation | Charged lepton | Rest energy | Neutrino |
|---|---|---|---|
| First | electron $e^{-}$ | $0.511\ \text{MeV}$ | $\nu_e$ |
| Second | muon $\mu^{-}$ | $105.7\ \text{MeV}$ | $\nu_{\mu}$ |
| Third | tau $\tau^{-}$ | $1777\ \text{MeV}$ | $\nu_{\tau}$ |

The **neutrino** was proposed by **Wolfgang Pauli in 1930** to rescue the
conservation of energy and momentum in beta decay: the emitted electrons had a
continuous range of energies instead of a single value, so an unseen third
particle must be carrying the balance away. Its beta-decay role is

n → p + e⁻ + ν̄ₑ

Neutrinos are electrically neutral, have almost no mass and interact **only**
through the weak force and gravity. About $6.5\times10^{14}$ solar neutrinos
cross each square metre of your body every second, and almost none interact;
detecting them needs thousands of tonnes of material deep underground.
**Cowan and Reines** finally did so in 1956.

Neutrinos were long assumed massless. Then **Super-Kamiokande** (1998) and
**SNO** (2001–02) showed that neutrinos change flavour in flight — **neutrino
oscillation** — which is possible only if they have a non-zero mass (Nobel Prize
2015). The tightest direct laboratory limit, from the KATRIN experiment in 2025, is
$m_{\nu} < 0.45\ \text{eV}/c^{2}$ — less than a millionth of the electron's mass.

The six quarks, six leptons, the force-carrying bosons and the **Higgs boson**
(found at CERN's Large Hadron Collider in July 2012, mass about
$125\ \text{GeV}/c^{2}$) form the **Standard Model** of particle physics.

## 26.2 Universe

### The Big Bang and Hubble's law

Observing distant galaxies in 1929, **Edwin Hubble** found that almost all of
them are moving away from us, and that the recession speed $v$ is proportional
to the distance $d$:

$$ v = H_0 d $$

$H_0$ is the **Hubble constant**. The speed comes from the **redshift** of the
galaxy's spectral lines; for $v \ll c$,

$$ z = \frac{\Delta\lambda}{\lambda} = \frac{v}{c} $$

```figure caption="Hubble diagram. Each point is a galaxy; the slope of the line is $H_0 \approx 70$ km s$^{-1}$ Mpc$^{-1}$ (1 Mpc $= 3.086\times10^{22}$ m)."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,2.8))
rng = np.random.default_rng(7)
d = np.sort(rng.uniform(20, 480, 22)); H0 = 70.0
v = H0*d + rng.normal(0, 1700, d.size)
ax.plot(d, v, 'o', color=ACCENT, ms=4.6, mec='none', label='galaxies')
dd = np.linspace(0, 500, 10)
ax.plot(dd, H0*dd, color=SERIES[1], lw=1.6, label=r'$v = H_0 d$')
ax.set_xlabel('distance  $d$  (Mpc)')
ax.set_ylabel(r'recession speed  $v$  (km s$^{-1}$)')
ax.set_xlim(0, 500); ax.set_ylim(0, 38000)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.5); ax.legend(loc='upper left')
```

Run the expansion backwards and all the matter was once packed into an extremely
hot, dense state. The **Big Bang** model says the universe began in such a state
about **13.8 billion years ago** and has expanded and cooled ever since. Three
independent observations support it:

| Evidence | What is observed |
|---|---|
| Hubble expansion | every distant galaxy recedes, with $v \propto d$ |
| Cosmic microwave background | a $2.725\ \text{K}$ blackbody glow from every direction, found by Penzias and Wilson in 1965 — the cooled radiation of the hot early universe |
| Light-element abundance | about 75% hydrogen and 25% helium by mass everywhere, exactly the amount predicted to form in the first few minutes |

::: example Worked example 26.3
**Problem.** Taking $H_0 = 70\ \text{km s}^{-1}\text{Mpc}^{-1}$ and
$1\ \text{Mpc} = 3.086\times10^{22}\ \text{m}$, find (a) the recession speed of a
galaxy $150\ \text{Mpc}$ away and (b) the Hubble time $1/H_0$ in years.

**Solution.**

(a) $v = H_0 d = 70 \times 150 = 1.05\times10^{4}\ \text{km s}^{-1}$, i.e.
$3.5\%$ of the speed of light.

(b) In SI units,

$$ H_0 = \frac{70\times10^{3}\ \text{m s}^{-1}}{3.086\times10^{22}\ \text{m}}
= 2.27\times10^{-18}\ \text{s}^{-1} $$

$$ \frac{1}{H_0} = 4.41\times10^{17}\ \text{s}
= \frac{4.41\times10^{17}}{3.15\times10^{7}} = 1.4\times10^{10}\ \text{years} $$

About 14 billion years — close to the measured age of 13.8 billion years.
:::

::: caution The universe has no centre
Galaxies are not flying outwards through space from an explosion at some point.
**Space itself stretches**, carrying the galaxies with it, so every observer in
every galaxy sees the same law $v = H_0 d$. Think of dots on an inflating
balloon, not of shrapnel.
:::

### Expansion of the universe and dark energy

In 1998 two teams found distant Type Ia supernovae to be **fainter than
expected**: the expansion is not slowing under gravity but **accelerating**.
The agent driving it is called **dark energy**: an unknown energy of empty space
that pushes outwards.

The microwave background fixes the present composition of the universe (Planck
mission, 2018 values):

```figure caption="Energy content of the present universe (Planck 2018 values). Everything ever seen with a telescope is the 5% slice."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4,2.9))
vals = [68.0, 27.0, 5.0]
labs = ['Dark energy\n68%', 'Dark matter\n27%', 'Ordinary matter\n5%']
cols = [SERIES[4], SERIES[0], SERIES[3]]
w, t = ax.pie(vals, labels=labs, colors=cols, startangle=90, counterclock=False,
              textprops=dict(fontsize=8.4, color=INK),
              wedgeprops=dict(width=0.42, edgecolor='white', lw=1.2))
ax.set_aspect('equal')
```

One open problem: the distance-ladder value $H_0 = 73.0 \pm 1.0$ (SH0ES, 2022)
and the microwave-background value $H_0 = 67.4 \pm 0.5\ \text{km s}^{-1}\text{Mpc}^{-1}$
(Planck, 2018) disagree by far more than their error bars. This **Hubble
tension** is still unresolved.

### Dark matter

Stars in the outer parts of a spiral galaxy orbit far too fast. To see why that
is a problem, work out what speed they *should* have.

::: derivation Why the rotation curve ought to fall away
**Step 1 — what holds a star in its orbit?** A star of mass $m$ moving in a
circle of radius $r$ about the centre of its galaxy needs a centripetal force
$mv^{2}/r$, and gravity must supply it. If $M(r)$ is the total mass lying
*inside* radius $r$, then

$$ \frac{GM(r)m}{r^{2}} = \frac{mv^{2}}{r} $$

**Step 2 — cancel $m$,** which appears on both sides (the answer cannot depend
on which star we pick):

$$ \frac{GM(r)}{r^{2}} = \frac{v^{2}}{r} $$

**Step 3 — multiply both sides by $r$:**

$$ \frac{GM(r)}{r} = v^{2} $$

**Step 4 — take the square root:**

$$ v = \sqrt{\frac{GM(r)}{r}} $$

**Step 5 — apply this outside the bright disc.** Out there almost no visible
stars are left, so if visible matter were all there is, $M(r)$ would stop
growing and settle down to a constant $M$. Putting a constant into Step 4,

$$ v = \sqrt{GM}\cdot\frac{1}{\sqrt{r}} \;\Longrightarrow\; v \propto \frac{1}{\sqrt{r}} $$

The speed should **fall off**, in exactly the way Neptune crawls round the Sun
more slowly than Mercury.

**Step 6 — compare with what is measured.** Real rotation curves stay flat:
$v \approx$ constant, far beyond the edge of the light. Put $v =$ constant back
into Step 3 and make $M(r)$ the subject:

$$ M(r) = \frac{v^{2}r}{G} \;\Longrightarrow\; M(r) \propto r $$

Mass must go on piling up in proportion to $r$ long after the light has stopped.
A spiral galaxy needs roughly ten times more of this invisible mass than of the
matter we can see.
:::

```figure caption="Rotation curve of a spiral galaxy. The flat measured curve needs far more mass than the visible matter can supply."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,2.8))
r = np.linspace(0.3, 30, 400); R0 = 3.0; v0 = 220.0
v_vis = np.where(r < R0, v0*r/R0, v0*np.sqrt(R0/r))
ax.plot(r, v0*np.tanh(r/1.6), color=ACCENT, lw=2.0, label='observed')
ax.plot(r, v_vis, color=SERIES[1], lw=1.7, ls='--',
        label='expected from visible matter')
ax.fill_between(r, v_vis, v0*np.tanh(r/1.6), color=ACCENT, alpha=0.10)
ax.annotate('missing mass\n= dark matter', (17, 140), fontsize=8.4, color=MUTED,
            ha='center')
ax.set_xlabel('distance from galactic centre  $r$  (kpc)')
ax.set_ylabel(r'orbital speed  $v$  (km s$^{-1}$)')
ax.set_xlim(0, 30); ax.set_ylim(0, 280)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.5); ax.legend(loc='lower right')
```

::: definition Dark matter
Dark matter is matter that exerts gravitational attraction but neither emits,
absorbs nor reflects electromagnetic radiation. It is detected only through its
gravity — flat galaxy rotation curves, the speeds of galaxies in clusters
(noticed by Zwicky in 1933), gravitational lensing, and the ripple pattern of the
microwave background.
:::

It cannot be ordinary matter that merely fails to shine, because the
light-element abundances cap how much ordinary matter exists. Leading candidates
are weakly interacting massive particles (WIMPs), axions and sterile neutrinos —
none yet found, despite decades of searching in underground laboratories.

### Black holes

Squeeze a body small enough and its escape velocity reaches the speed of light.
Beyond that point nothing at all can leave it.

::: derivation The Schwarzschild radius
**Step 1 — the condition for escaping.** To get away from the surface of a body
of mass $M$ and radius $R$, a projectile of mass $m$ must have just enough
kinetic energy to pay off its gravitational potential energy. At the surface the
potential energy is $-GMm/R$; infinitely far away it is zero. So the smallest
launch speed $v_e$ satisfies

$$ \frac{1}{2}mv_e^{2} = \frac{GMm}{R} $$

**Step 2 — cancel $m$** from both sides; the escape speed does not depend on
what you throw:

$$ \frac{1}{2}v_e^{2} = \frac{GM}{R} $$

**Step 3 — multiply both sides by $2$:**

$$ v_e^{2} = \frac{2GM}{R} $$

**Step 4 — take the square root:**

$$ v_e = \sqrt{\frac{2GM}{R}} $$

**Step 5 — now shrink the body.** Keep $M$ fixed and make $R$ smaller and
smaller. $v_e$ grows. Call $R_s$ the radius at which $v_e$ has just reached $c$:

$$ c^{2} = \frac{2GM}{R_s} $$

**Step 6 — multiply both sides by $R_s$:**

$$ c^{2}R_s = 2GM $$

**Step 7 — divide both sides by $c^{2}$:**

$$ R_s = \frac{2GM}{c^{2}} $$

This $R_s$ is the **Schwarzschild radius**.
:::

::: caution The Newtonian shortcut gives the right answer for the wrong reason
Light does not slow down as it climbs out of a gravitational field, so the
escape-velocity argument above is not strictly valid for light. Karl
Schwarzschild obtained the very same formula in 1916 from Einstein's field
equations, which is why NEB accepts the short derivation. Quote it — but
remember the real reason: inside $R_s$, every path leads inwards.
:::

::: definition Black hole
A black hole is a region where matter has collapsed to such a density that the
escape velocity exceeds the speed of light. Its boundary, at $r = R_s$, is the
**event horizon**: a one-way surface. Nothing that crosses it can return, so the
object is seen only through its gravitational effect on its surroundings.
:::

A star heavier than about 20 solar masses leaves a black hole when its core
collapses. Far larger **supermassive** black holes, millions to billions of
solar masses, sit at the centres of galaxies. Evidence includes X-ray emission
from gas spiralling into Cygnus X-1; the orbits of stars whipping around an
invisible $4.3\times10^{6}\ M_{\odot}$ object at our galactic centre (Nobel Prize
2020); and direct images from the **Event Horizon Telescope** — M87\* on
10 April 2019 ($6.5\times10^{9}\ M_{\odot}$, 55 million light-years away) and
**Sagittarius A\*** on 12 May 2022, 27,000 light-years away.

::: example Worked example 26.4
**Problem.** Calculate the Schwarzschild radius of (a) the Sun
($M = 2\times10^{30}\ \text{kg}$) and (b) the Earth
($M = 6\times10^{24}\ \text{kg}$). Take $G = 6.67\times10^{-11}$ SI units.

**Solution.**

(a) $$ R_s = \frac{2GM}{c^{2}}
= \frac{2\times6.67\times10^{-11}\times2\times10^{30}}{(3\times10^{8})^{2}}
= \frac{2.67\times10^{20}}{9\times10^{16}} = 2.96\times10^{3}\ \text{m} $$

so about $3\ \text{km}$: the Sun would have to be squeezed from
$7\times10^{5}\ \text{km}$ to the size of a small town.

(b) $$ R_s = \frac{2\times6.67\times10^{-11}\times6\times10^{24}}{9\times10^{16}}
= \frac{8.0\times10^{14}}{9\times10^{16}} = 8.9\times10^{-3}\ \text{m} $$

— the Earth squeezed to the size of a marble.
:::

### Gravitational waves

General relativity treats gravity as curvature of spacetime. When a massive
object accelerates asymmetrically — two black holes spiralling together — that
curvature ripples outwards at the speed of light. These **gravitational waves**
are transverse: they alternately stretch and squeeze space in two perpendicular
directions.

Einstein predicted them in 1916 and believed they would never be measured,
because the **strain** $h = \Delta L/L$ they produce on Earth is only about
$10^{-21}$.

```figure caption="A LIGO detector: a Michelson interferometer with 4 km arms. A passing wave lengthens one arm and shortens the other, shifting the interference pattern at the photodetector."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(4.8,3.0))
ax.add_patch(Rectangle((0.0,1.85), 0.75, 0.42, fc='none', ec=INK, lw=1.0))
ax.annotate('laser', (0.375,2.06), ha='center', va='center', fontsize=8.0)
ax.plot([0.75,1.9],[2.06,2.06], color=ACCENT, lw=1.6)
ax.plot([1.72,2.08],[1.88,2.24], color=INK, lw=2.0)
ax.annotate('beam\nsplitter', (1.66,1.62), ha='right', va='center',
            fontsize=7.6, color=MUTED)
ax.plot([1.9,4.5],[2.06,2.06], color=ACCENT, lw=1.6)
ax.plot([1.9,1.9],[2.06,3.5], color=ACCENT, lw=1.6)
ax.plot([4.5,4.5],[1.80,2.32], color=SERIES[1], lw=3.0)
ax.plot([1.64,2.16],[3.5,3.5], color=SERIES[1], lw=3.0)
ax.annotate('mirror', (4.62,2.06), fontsize=7.8, color=SERIES[1], va='center')
ax.annotate('mirror', (1.9,3.62), fontsize=7.8, color=SERIES[1], ha='center')
ax.annotate('', xy=(4.5,1.42), xytext=(2.22,1.42),
            arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=1.0, mutation_scale=9))
ax.annotate('4 km', (3.36,1.28), ha='center', va='top', fontsize=7.8, color=MUTED)
ax.annotate('', xy=(0.95,3.5), xytext=(0.95,2.06),
            arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=1.0, mutation_scale=9))
ax.annotate('4 km', (0.86,2.78), ha='right', va='center', fontsize=7.8, color=MUTED)
ax.plot([1.9,1.9],[2.06,0.75], color=ACCENT, lw=1.6, ls=(0,(4,2)))
ax.add_patch(Rectangle((1.45,0.30), 0.9, 0.42, fc='none', ec=INK, lw=1.0))
ax.annotate('detector', (1.9,0.51), ha='center', va='center', fontsize=8.0)
ax.set_xlim(-0.1,5.6); ax.set_ylim(0.1,3.95); ax.axis('off')
```

**LIGO** solved the problem with two Michelson interferometers, at Hanford and
Livingston in the USA, with $4\ \text{km}$ arms. A laser beam is
split, sent along both arms, reflected and recombined; if one arm changes length
relative to the other, the interference pattern shifts. Two detectors far apart
are used so that a local disturbance — a truck, an earthquake — is not mistaken
for a wave from space.

::: example Worked example 26.5
**Problem.** A gravitational wave of strain $h = 1.0\times10^{-21}$ passes
through a LIGO arm of length $L = 4.0\ \text{km}$. (a) By how much does the arm
change in length? (b) Compare that with the diameter of a proton,
$1.7\times10^{-15}\ \text{m}$.

**Solution.**

(a) The strain is defined as $h = \Delta L/L$. Multiplying both sides by $L$,

$$ \Delta L = hL = (1.0\times10^{-21})\times(4.0\times10^{3}\ \text{m}) $$

$$ \Delta L = 4.0\times10^{-18}\ \text{m} $$

(b) $$ \frac{\Delta L}{d_{\text{proton}}} = \frac{4.0\times10^{-18}}{1.7\times10^{-15}}
= 2.4\times10^{-3} $$

The mirrors shift by about one four-hundredth of the width of a proton — and
that has to be measured over a $4\ \text{km}$ baseline. This is why the
detection took a century after the prediction.
:::

The first detection, **GW150914**, was made on **14 September 2015** and
announced in February 2016. Two black holes of about 36 and 29 solar masses
merged into one of 62 solar masses, roughly $3\ M_{\odot}$ vanishing as pure
gravitational-wave energy in a fraction of a second. The 2017 Nobel Prize
followed. In August 2017 the neutron-star merger GW170817 was seen in gravitational waves
and gamma rays together, opening *multi-messenger astronomy*. With Virgo and
KAGRA now joining the network, the cumulative LIGO–Virgo–KAGRA catalogue
(GWTC-5.0, 2026) lists **391 confirmed events** — the count grows with every
observing run, so quote it with its date.

::: example Worked example 26.6
**Problem.** In GW150914 about $3.0\ M_{\odot}$ of mass was converted into
gravitational-wave energy, where $M_{\odot} = 2\times10^{30}\ \text{kg}$. How
much energy was released?

**Solution.** By Einstein's mass–energy relation,

$$ E = \Delta m\,c^{2} = (3.0\times2\times10^{30})\times(3\times10^{8})^{2} $$

$$ E = 6\times10^{30}\times9\times10^{16} = 5.4\times10^{47}\ \text{J} $$

Briefly, the merger radiated more power than every star in the observable
universe combined.
:::

## Chapter summary

- Every particle has an antiparticle of equal mass and opposite charge. Pair
  production needs $\geq 1.02\ \text{MeV}$; annihilation of $e^{-}e^{+}$ gives
  two $0.511\ \text{MeV}$ photons.
- Quarks come in six flavours: $u, c, t$ with charge $+\frac{2}{3}e$ and
  $d, s, b$ with $-\frac{1}{3}e$. Baryons are $qqq$ ($p = uud$, $n = udd$);
  mesons are $q\bar{q}$ ($\pi^{+} = u\bar{d}$). Free quarks are never seen.
- The six leptons are $e, \mu, \tau$ and their neutrinos. Neutrinos are neutral,
  feel only the weak force, and oscillate between flavours — proof of tiny mass.
- Hubble's law $v = H_0 d$ with $H_0 \approx 70\ \text{km s}^{-1}\text{Mpc}^{-1}$;
  the Hubble time $1/H_0 \approx 14$ billion years.
- Big Bang evidence: the expansion, the $2.725\ \text{K}$ cosmic microwave
  background, and the 75% H / 25% He abundance. Age $= 13.8$ billion years.
- Space itself expands, with no centre, and ever faster: the universe is 68%
  dark energy, 27% dark matter, 5% ordinary matter.
- Dark matter is inferred from flat rotation curves, cluster dynamics and
  lensing; it has never been detected directly. Newtonian orbits give
  $v = \sqrt{GM(r)/r}$, so a flat curve means $M(r) \propto r$.
- Black hole: escape velocity exceeds $c$; event horizon at
  $R_s = 2GM/c^{2}$. Imaged by the Event Horizon Telescope (M87\* 2019,
  Sgr A\* 2022).
- Gravitational waves are ripples of spacetime travelling at $c$, of strain
  $h = \Delta L/L \approx 10^{-21}$, detected by km-scale Michelson
  interferometers; first detection GW150914, 14 September 2015; 391 events in
  the catalogue by 2026.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The quark composition of a neutron is <span class="marks">[1]</span>
   (a) $uud$ (b) $udd$ (c) $u\bar{d}$ (d) $uds$
2. Which of the following is **not** a lepton? <span class="marks">[1]</span>
   (a) electron (b) muon (c) pion (d) neutrino
3. The cosmic microwave background has a temperature of about <span class="marks">[1]</span>
   (a) $0\ \text{K}$ (b) $2.7\ \text{K}$ (c) $27\ \text{K}$ (d) $273\ \text{K}$
4. The Schwarzschild radius of a body of mass $M$ is <span class="marks">[1]</span>
   (a) $GM/c^{2}$ (b) $2GM/c^{2}$ (c) $GM/2c^{2}$ (d) $2GM/c$
5. Flat rotation curves of spiral galaxies are evidence for <span class="marks">[1]</span>
   (a) dark energy (b) dark matter (c) black holes (d) antimatter

::: note Answers to Group A
**1.** (b) — $udd$ gives $\frac{2}{3}-\frac{1}{3}-\frac{1}{3} = 0$.
**2.** (c) — the pion is a meson, made of a quark and an antiquark.
**3.** (b) — a $2.725\ \text{K}$ blackbody, found by Penzias and Wilson in 1965.
**4.** (b) — from $\sqrt{2GM/R} = c$.
**5.** (b) — the extra unseen mass keeps the outer stars moving fast.
:::

**Group B — Short answer (5 marks each)**

1. What is an antiparticle? Describe pair production and annihilation, giving the
   threshold energy for electron–positron pair production. <span class="marks">[5]</span>
2. Distinguish between baryons and mesons, and show that the quark contents $uud$
   and $u\bar{d}$ give the correct charges of the proton and the $\pi^{+}$. <span class="marks">[5]</span>
3. Why was the neutrino proposed, and why is it so difficult to detect? What does
   neutrino oscillation tell us about its mass? <span class="marks">[5]</span>
4. State Hubble's law. A galaxy is $200\ \text{Mpc}$ away. Taking
   $H_0 = 70\ \text{km s}^{-1}\text{Mpc}^{-1}$, find its recession speed and the
   fractional redshift $z$ of its spectral lines. <span class="marks">[5]</span>
5. What is dark matter? Give two pieces of observational evidence for it. <span class="marks">[5]</span>
6. Show that a star orbiting at radius $r$ inside a galaxy of enclosed mass
   $M(r)$ has speed $v = \sqrt{GM(r)/r}$, and explain why a **flat** rotation
   curve requires $M(r) \propto r$. <span class="marks">[5]</span>
7. A gravitational wave of strain $1.0\times10^{-21}$ crosses a detector whose
   arms are $4.0\ \text{km}$ long. Calculate the change in length of one arm. <span class="marks">[5]</span>

::: note Answers to Group B
**2.** Outline: baryons are three quarks with baryon number $+1$; mesons are a
quark and an antiquark with baryon number $0$, and all mesons are unstable.
Charges: $uud = \frac{2}{3}+\frac{2}{3}-\frac{1}{3} = +1$ for the proton;
$u\bar{d} = \frac{2}{3}+\frac{1}{3} = +1$ for the $\pi^{+}$.

**3.** Outline: beta-decay electrons emerge with a continuous energy spectrum, so
Pauli (1930) proposed an unseen neutral particle carrying off the missing energy
and momentum. The neutrino is chargeless and interacts only weakly, so its chance
of interacting in a detector is minute. Oscillation between flavours is possible
only if at least two neutrino states have non-zero mass.

**4.** $v = H_0 d = 70 \times 200 = 1.4\times10^{4}\ \text{km s}^{-1}$.
$$ z = \frac{v}{c} = \frac{1.4\times10^{4}}{3\times10^{5}} = 0.047 $$
so the lines are shifted about 4.7% towards the red.

**6.** Gravity supplies the centripetal force, $GM(r)m/r^{2} = mv^{2}/r$.
Cancelling $m$ and multiplying by $r$ gives $v^{2} = GM(r)/r$, so
$v = \sqrt{GM(r)/r}$. If $v$ is constant then $M(r) = v^{2}r/G$, which is
proportional to $r$: mass keeps accumulating outside the visible disc.

**7.** $\Delta L = hL = 1.0\times10^{-21}\times4.0\times10^{3}
= 4.0\times10^{-18}\ \text{m}$, roughly one four-hundredth of a proton diameter.

**1.** Outline: an antiparticle has the same mass and spin as its particle but
opposite charge and opposite quantum numbers (§26.1). In **pair production** a
photon passing close to a nucleus turns into a particle–antiparticle pair; for
$e^{-}e^{+}$ the photon must carry at least $2m_ec^{2} = 1.02\ \text{MeV}$, and
the nearby nucleus is needed to take up recoil momentum. In **annihilation** an
electron and a positron meet and vanish, and two photons of $0.511\ \text{MeV}$
go out in opposite directions so that momentum is conserved.

**5.** Outline: dark matter is matter that has mass and therefore gravitates, but
neither emits nor absorbs light, so it is seen only through its gravity (§26.2).
Evidence: (i) **flat galactic rotation curves** — outer stars orbit far faster
than the visible mass allows, requiring $M(r) \propto r$ out to large radii;
(ii) **gravitational lensing** by clusters, which bends background light by far
more than the luminous mass could; (iii) the **speeds of galaxies inside
clusters** (Zwicky, Coma cluster), which are too high for the cluster to stay
bound on visible mass alone.
:::

**Group C — Long answer (8 marks each)**

1. (a) State Hubble's law and explain how it leads to the Big Bang model. <span class="marks">[3]</span>
   (b) Give three independent pieces of evidence supporting the Big Bang. <span class="marks">[3]</span>
   (c) Show that the Hubble time $1/H_0$ for
   $H_0 = 70\ \text{km s}^{-1}\text{Mpc}^{-1}$ is about $14$ billion years, given
   $1\ \text{Mpc} = 3.086\times10^{22}\ \text{m}$. <span class="marks">[2]</span>
2. (a) Define a black hole and derive the expression for its Schwarzschild
   radius. <span class="marks">[3]</span>
   (b) What are gravitational waves? Describe with a diagram how LIGO detects
   them, and state one major observation. <span class="marks">[5]</span>

::: note Answers to Group C
**1.(a)** Outline: Hubble's law is $v = H_0 d$ — every distant galaxy recedes
with a speed proportional to its distance. Running the motion backwards, every
galaxy was at the same place at a time $t \approx 1/H_0$ ago, which is the Big
Bang. The recession is not galaxies flying through space but space itself
expanding, so there is no centre.

**1.(b)** Any three of: the redshift–distance relation itself; the cosmic
microwave background at $2.7\ \text{K}$, the cooled relic of the hot early
universe; the observed abundance of light elements (about 75% hydrogen, 25%
helium by mass) predicted by Big-Bang nucleosynthesis; and the fact that distant
galaxies look younger than nearby ones.

**1.(c)** $H_0 = \frac{70\times10^{3}}{3.086\times10^{22}}
= 2.27\times10^{-18}\ \text{s}^{-1}$, so

$$ \frac{1}{H_0} = \frac{1}{2.27\times10^{-18}} = 4.41\times10^{17}\ \text{s} $$

Dividing by $3.156\times10^{7}\ \text{s per year}$ gives
$1.40\times10^{10}\ \text{years}$, about 14 billion years — close to the
accepted age of 13.8 billion years.

**2.(b)** Outline: gravitational waves are ripples in spacetime radiated by
accelerating masses, stretching space in one direction while squeezing it in the
perpendicular direction (§26.2). Marks for the labelled Michelson interferometer
diagram (laser, beam splitter, two 4 km arms with mirrors, detector), for the
statement that a passing wave lengthens one arm and shortens the other so the
recombined beams fall out of step and the fringe pattern shifts, and for one
named observation such as GW150914, the merger of two black holes of about 36
and 29 solar masses detected on 14 September 2015.

**2.(a)** A black hole is a region whose escape velocity exceeds the speed of light, so no
radiation can leave it; its boundary at $r = R_s$ is the event horizon. For the
derivation set out step by step, see §26.2. The marks go to: equating kinetic
energy with the magnitude of the gravitational potential energy,
$\frac{1}{2}mv_e^{2} = GMm/R$; cancelling $m$ and rearranging to
$v_e = \sqrt{2GM/R}$; and putting $v_e = c$ to obtain

$$ R_s = \frac{2GM}{c^{2}} $$
:::
