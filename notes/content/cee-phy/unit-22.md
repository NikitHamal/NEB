---
subject: Physics
grade: CEE
unit: 22
title: Particle Physics and Recent Trends
hours: 2
area: Modern Physics
---

The last chapter of the Physics paper looks outward twice: inward to the smallest
objects we know, and outward to the whole universe. Modern Physics carries **12 of
the 50 Physics questions** (official MEC weightage), and we estimate about **2** come
from here. The paper asks for the **inventory** — six quarks, six leptons, which
particles make a proton, which force is carried by which boson — and for the
**evidence** behind the Big Bang, especially Hubble's law. Nothing needs a long
calculation; what it needs is precision, because this is the area where careless
books print sentences that are simply false.

::: key What the paper asks from this chapter
- Six quarks (u, d, c, s, t, b) with charges $+\frac{2}{3}$ and $-\frac{1}{3}$; six leptons (e, μ, τ and their neutrinos); antiparticles for every particle.
- Hadrons: baryons are three quarks (p = uud, n = udd), mesons are a quark–antiquark pair ($\pi^+=u\bar d$).
- The four interactions, their exchange bosons, ranges and approximate relative strengths.
- The Higgs boson: quantum of the Higgs field, about 125 GeV/$c^2$, found at CERN in 2012; it gives mass to **fundamental** particles, not to everything.
- Nanotechnology: the 1–100 nm scale, why the properties change, and two or three real applications.
- The Big Bang: expansion, the CMB at 2.7 K, redshift, $v=H_0d$, and the age estimate $1/H_0\approx14$ Gyr (accepted age 13.8 Gyr).
:::

## 22.1 Particles and antiparticles; leptons and quarks; the Higgs boson

### 22.1.1 The inventory

By the 1970s the hundreds of particles found in cosmic rays and accelerators had been
reduced to a small list of **fundamental** particles — particles with no known
internal structure. This list is the **Standard Model**.

| Family | Members | Charge | Notes |
|---|---|---|---|
| Quarks (6) | up, down, charm, strange, top, bottom | $+\frac{2}{3}$ (u, c, t); $-\frac{1}{3}$ (d, s, b) | feel the strong force; never found alone |
| Leptons (6) | electron, muon, tau | $-1$ | feel the weak force and, if charged, electromagnetism |
| | electron neutrino, muon neutrino, tau neutrino | $0$ | almost massless; feel only the weak force |
| Gauge bosons | photon, gluon, $W^+$, $W^-$, $Z^0$ | 0, 0, ±1, 0 | carry the forces |
| Higgs boson | $H^0$ | 0 | gives mass to the fundamental particles |

The quarks and leptons come in **three generations** of increasing mass: (u, d, e,
$\nu_e$), then (c, s, μ, $\nu_\mu$), then (t, b, τ, $\nu_\tau$). Ordinary matter uses
only the first generation plus the muon and neutrinos made in cosmic-ray showers and
radioactive decays.

```figure caption="The twelve fundamental fermions of the Standard Model, in three generations. Every entry has an antiparticle of the same mass and opposite charge; the antiparticles are not shown. The charges are in units of the proton charge $e$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,3.0))
rows = [(['u','c','t'],'+2/3'),(['d','s','b'],'−1/3'),
        (['e','μ','τ'],'−1'),([r'$\nu_e$',r'$\nu_\mu$',r'$\nu_\tau$'],'0')]
for i,(syms,q) in enumerate(rows):
    y = 4.25 - 0.95*i
    for j,s in enumerate(syms):
        x = 1.85 + 1.12*j
        ax.add_patch(plt.Rectangle((x-0.44,y-0.30),0.88,0.60, fc='#EDF2F9', ec=ACCENT, lw=0.9))
        ax.text(x,y,s,ha='center',va='center',fontsize=10,color=INK)
    ax.text(5.45,y,q,ha='center',va='center',fontsize=9,color=INK)
for j,c in enumerate(['I','II','III']):
    ax.text(1.85+1.12*j,5.05,c,ha='center',va='center',fontsize=9,color=MUTED)
ax.text(5.45,5.05,'charge',ha='center',va='center',fontsize=9,color=MUTED)
ax.text(0.62,3.78,'quarks',ha='center',va='center',fontsize=9.5,color=INK,rotation=90)
ax.text(0.62,1.88,'leptons',ha='center',va='center',fontsize=9.5,color=INK,rotation=90)
ax.plot([1.30,1.30],[3.15,4.62],color=MUTED,lw=0.8)
ax.plot([1.30,1.30],[1.25,2.72],color=MUTED,lw=0.8)
ax.text(3.0,0.72,'each particle has an antiparticle (not shown)',ha='center',fontsize=8,color=MUTED)
ax.set_xlim(0.15,6.05); ax.set_ylim(0.45,5.35)
ax.axis('off')
```

### 22.1.2 Antiparticles

For every particle there is an **antiparticle** with the **same mass** and **opposite
charge** (and opposite quantum numbers). The antiparticle of the electron is the
**positron** ($e^+$); of the proton, the **antiproton**; of the neutrino, the
antineutrino; of a quark, the antiquark.

Two processes matter for the paper:

- **Annihilation.** A particle and its antiparticle can disappear, their mass-energy
  appearing as radiation. An electron and a positron at rest give two photons, each of
  energy $m_ec^2=0.511$ MeV, travelling in opposite directions so that momentum is
  conserved. Two photons, not one: a single photon could not carry away zero momentum.
- **Pair production.** A photon of sufficient energy near a nucleus can create an
  electron–positron pair. The minimum energy is $2m_ec^2=1.02$ MeV, and any excess
  becomes kinetic energy of the pair. A single photon in empty space cannot do this —
  momentum conservation again requires a third body, the nucleus.

::: example Worked example 22.1 — the photons from an annihilation
**Problem.** An electron and a positron, both nearly at rest, annihilate. Find the
energy of each photon in joules and the wavelength of the radiation.

**Solution.** The total rest energy is $2m_ec^2=1.02$ MeV, shared equally, so each
photon has $0.511$ MeV $=0.511\times10^{6}\times1.6\times10^{-19}=8.2\times10^{-14}$ J.

$\lambda=\dfrac{hc}{E}=\dfrac{1.99\times10^{-25}}{8.2\times10^{-14}}
=2.4\times10^{-12}$ m $=2.4$ pm.

**Check.** 2.4 pm is a gamma ray, far shorter than any X-ray tube produces. The two
photons must also travel in opposite directions, so that the total momentum stays
zero.
:::

::: caution Antimatter is not "negative mass"
An antiparticle has **positive** mass and positive energy. Only its charge and its
other quantum numbers are reversed. Antimatter does not fall upwards, and it does not
have negative energy. It annihilates with matter because particle number is not
conserved in that interaction, not because the masses cancel.
:::

### 22.1.3 Quarks and hadrons

Quarks are never found in isolation. They are held by the **strong force**, whose
carrier is the **gluon**, and the force grows as quarks are pulled apart: separating
two quarks creates a new quark–antiquark pair rather than a free quark. This is
**confinement**, and it is why every experiment sees only combinations of quarks.

| Combination | Name | Examples |
|---|---|---|
| three quarks ($qqq$) | **baryon** | proton $uud$, neutron $udd$, $\Lambda$ ($uds$), $\Omega^-$ ($sss$) |
| quark + antiquark ($q\bar q$) | **meson** | $\pi^+=u\bar d$, $\pi^-=\bar ud$, $K^+=u\bar s$ |

Both classes are **hadrons** — particles that feel the strong force. The charges work
out exactly:

$$ p=uud:\ \tfrac{2}{3}+\tfrac{2}{3}-\tfrac{1}{3}=+1, \qquad
n=udd:\ \tfrac{2}{3}-\tfrac{1}{3}-\tfrac{1}{3}=0 $$

$$ \pi^+=u\bar d:\ \tfrac{2}{3}-\left(-\tfrac{1}{3}\right)=+1 $$

Notice that the neutron is neutral even though all three of its quarks are charged:
the charges simply add to zero. That is a favourite exam trap.

**Baryon number** is a conserved quantity: each quark has $B=+\frac{1}{3}$, each
antiquark $-\frac{1}{3}$. A proton or neutron therefore has $B=+1$, a meson has $B=0$,
and in any reaction the total baryon number is unchanged. This is why the proton cannot decay
into a positron and a pion, for example: those have $B=0$, and $B$ must be conserved.
No proton decay has ever been observed (the experimental limit on its lifetime is
beyond $10^{34}$ years).

### 22.1.4 The four fundamental interactions

| Interaction | Exchange boson | Range | Relative strength | Acts on |
|---|---|---|---|---|
| Strong | gluon (8 kinds) | about $10^{-15}$ m (a nucleon) | 1 | quarks and therefore hadrons |
| Electromagnetic | photon | infinite ($1/r^2$) | about $10^{-2}$ | all charged particles |
| Weak | $W^+$, $W^-$, $Z^0$ | about $10^{-18}$ m | about $10^{-6}$ | all quarks and leptons |
| Gravitational | graviton (not yet observed) | infinite | about $10^{-38}$ | everything with mass-energy |

The numbers in the strength column are **approximate** and depend on which pair of
particles is being compared; they are meant only to rank the forces. Two protons in a
nucleus repel each other electrically and are held together by the strong force,
which is about a hundred times stronger at nuclear distances. Gravity, weaker than
the strong force by some 38 powers of ten, only becomes important when a very large
mass is collected together — which is why it rules the planets and the galaxies but
not the nucleus.

The **weak** interaction is the one responsible for beta decay: a neutron turns into a
proton by emitting a $W^-$, which becomes an electron and an antineutrino. It is weak
in strength but essential — without it the Sun could not burn hydrogen by the
proton–proton chain.

::: memory Generations and carriers
Quarks: **u**p **d**own, **c**harm **s**trange, **t**op **b**ottom — "up down, charm
strange, top bottom" in pairs.
Leptons: the three charged ones (e, μ, τ) and their three neutrinos.
Bosons: **g**luon for **g**lue (strong), **p**hoton for electromagnetism, **W/Z** for
the **w**eak force, and the Higgs on its own.
:::

### 22.1.5 The Higgs boson

Most of the Standard Model works with **massless** particles. But the $W$ and $Z$
bosons are heavy (80.4 and 91.2 GeV/$c^2$), and quarks and leptons have mass. The
**Higgs mechanism** explains this: the universe is filled with a field — the **Higgs
field** — and particles that interact with it behave as if they have mass. The
**Higgs boson** is the quantum of that field, the ripple that can be produced in a
collision.

The Higgs boson was discovered at CERN's Large Hadron Collider in **2012**, with a
mass of about **125 GeV/$c^2$** — about 133 times the mass of a proton. Higgs and
Englert shared the 2013 Nobel Prize for the theory.

::: caution What the Higgs does and does not do
It gives mass to **fundamental** particles — the $W$ and $Z$ bosons, the quarks and
the charged leptons — through their interaction with the field. It does **not** give
mass to the photon or the gluon (they remain massless), and it is **not** the source
of most of the mass of a proton or a neutron. About 99 % of a nucleon's mass is the
energy of the gluon field and of the confined quarks, converted by $E=mc^2$. Saying
"the Higgs gives mass to everything" is wrong, and it is exactly the sort of sentence
a sloppy book prints.
:::

One more honest qualification: in the original Standard Model the neutrinos are
massless, but neutrino **oscillation** (one flavour turning into another) shows that
they have small, different masses. That is a known gap between the simplest version of
the model and experiment, and it is why neutrino physics is an active field.

## 22.2 Nanotechnology

### 22.2.1 The scale

A **nanometre** is $10^{-9}$ m — one millionth of a millimetre. **Nanotechnology** is
the design and use of structures with at least one dimension between about **1 nm and
100 nm**. For comparison:

| Object | Size |
|---|---|
| hydrogen atom | about 0.1 nm |
| width of a DNA double helix | about 2 nm |
| a typical protein | 5–10 nm |
| a small virus | 20–300 nm |
| gate length in a modern processor | a few nm |
| red blood cell | about 7 000 nm (7 μm) |
| human hair | about 80 000 nm (80 μm) |

```figure caption="The nanoscale. The shaded band is the 1–100 nm range that defines nanotechnology: larger than a single atom, smaller than a virus, and far below the wavelength of visible light."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.8))
ax.axvspan(1,100, color=ACCENT, alpha=0.13, lw=0)
items = [(0.1,'atom\n0.1 nm',1.0),(2,'DNA\n2 nm',-1.0),(10,'protein\n10 nm',1.7),
         (100,'virus\n100 nm',-1.7),(7000,'red blood cell\n7 μm',1.0),(80000,'hair\n80 μm',-1.0)]
for x,lab,h in items:
    ax.plot([x,x],[0,0.55*np.sign(h)],color=INK,lw=0.9)
    ax.text(x,0.62*np.sign(h),lab,ha='center',va='bottom' if h>0 else 'top',
            fontsize=7.6,color=INK)
ax.axhline(0,color=INK,lw=1.0)
ax.set_xscale('log')
ax.set_xlim(0.05,3e5); ax.set_ylim(-2.4,2.4)
ax.set_yticks([])
ax.set_xlabel('size (nm, logarithmic scale)')
ax.spines[['top','right','left']].set_visible(False)
ax.text(10,2.15,'1–100 nm',ha='center',fontsize=8.5,color=ACCENT)
```

### 22.2.2 Why the properties change

Two things happen when a piece of material is made very small.

1. **Surface dominates.** The fraction of atoms on the surface grows as $1/r$. A
   10 nm particle has roughly a fifth of its atoms on the surface, so surface
   chemistry — catalysis, adhesion, dissolution — controls its behaviour.
2. **Quantum effects appear.** When the particle is smaller than the electron's
   quantum wavelength, the allowed energies become discrete, and the colour, melting
   point and electrical behaviour change with size. Gold nanoparticles, for example,
   are red or purple rather than golden, and their colour depends on their diameter.

### 22.2.3 Real applications

- **Medicine — targeted drug delivery.** Drugs are packaged in liposomes or polymer
  nanoparticles of 50–200 nm, which can pass through leaky tumour blood vessels and
  release the drug where it is needed, reducing side effects. Several such
  formulations are in clinical use.
- **Water treatment.** Nanoscale iron particles and nanomembranes remove arsenic and
  other contaminants from groundwater. This matters in the Terai, where arsenic in
  tube-well water is a real public-health problem.
- **Materials and coatings.** Titanium dioxide and zinc oxide nanoparticles make
  transparent sunscreens that block ultraviolet light; carbon nanotubes and graphene
  add strength and conductivity to composites; quantum dots are used as colour
  converters in some displays.
- **Electronics.** Transistor gates are now a few nanometres long, and this is
  nanotechnology in mass production, not in a laboratory.

::: caution No nanobot hype
Most "nanotechnology" in the market is **materials** — particles, coatings, composites
— not tiny machines. Medical nanorobots that repair the body from inside are research
ideas, not products. A question that offers "nanobots that cure all diseases" as an
option is offering a distractor. Also, nanoparticles are not automatically safe: their
large surface area makes some of them more reactive and potentially more toxic than
the bulk material, which is why regulation exists.
:::

The instruments that made the field possible are the **scanning tunnelling microscope**
(STM, 1981) and the **atomic force microscope** (AFM), which can image and even move
individual atoms.

## 22.3 The Big Bang theory and Hubble's law

### 22.3.1 The evidence

The **Big Bang theory** says that the universe was once far hotter and denser than it
is now, and that it has been expanding and cooling ever since. It is supported by
three independent observations.

```photo id="phy11/hudf" caption="The Hubble Ultra Deep Field: almost every smear and speck in this small patch of sky is an entire galaxy, each receding from us." width="60"
```


1. **The expansion.** Distant galaxies recede from us, and the farther one is, the
   faster it recedes.
2. **The cosmic microwave background (CMB).** A faint radiation fills all of space,
   with a nearly perfect blackbody spectrum at **2.725 K**. It is the cooled remnant
   of the hot, opaque plasma that filled the universe until about **380 000 years**
   after the beginning, when atoms formed and light could travel freely.
3. **The light elements.** The observed abundances of hydrogen, helium-4 (about 25 %
   by mass), deuterium and lithium match the predictions of nuclear reactions in the
   first few minutes.

The CMB was found by accident by Penzias and Wilson in 1965 and mapped in detail by
COBE, WMAP and Planck. Its tiny temperature ripples (about one part in $10^{5}$) are
the seeds from which galaxies grew.

### 22.3.2 Redshift

Light from a receding source is stretched to longer wavelengths. The **redshift** is

```photo id="phy11/cmb" caption="The cosmic microwave background as mapped by ESA's Planck satellite. Blue and red patches differ by only about one part in 100 000 in temperature; they are the seeds of today's galaxies." width="75"
```


$$ z=\frac{\lambda_{obs}-\lambda_{emit}}{\lambda_{emit}} $$

For small redshifts (small compared with 1) the recession speed is

$$ v\approx cz $$

so $z=0.01$ means about 3000 km s⁻¹. For large redshifts this linear formula fails and
the full relativistic relation is needed; the paper only uses the small-$z$ form.

The cosmological redshift is not quite a Doppler shift through space: space itself is
expanding while the light travels, so the wavelength is stretched all the way along
the path. For exam purposes the difference does not matter, but the correct picture is
"expansion of space", not "galaxies rushing through space".

### 22.3.3 Hubble's law

In 1929 Hubble found that the recession speed of a galaxy is proportional to its
distance:

$$ v=H_0d $$

where $H_0$ is the **Hubble constant**. Its measured value is about
**70 km s⁻¹ Mpc⁻¹** (different methods give 67–73; the disagreement is the "Hubble
tension"). One megaparsec is $3.09\times10^{22}$ m, or 3.26 million light years.

```figure caption="Hubble's law. The recession speed is proportional to distance, so the graph is a straight line through the origin whose slope is $H_0$. The points are real galaxies, scattered about the line because peculiar motions add to the expansion."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.9))
d = np.linspace(0,500,100)
ax.plot(d, 0.070*d, color=ACCENT, lw=1.9)
pts = [(80,5.1),(160,11.9),(240,16.2),(320,23.1),(420,28.6)]
ax.plot([p[0] for p in pts],[p[1] for p in pts],'o', color='#A8271F', ms=4.5, zorder=5)
ax.annotate('slope $=H_0$', xy=(300,21.0), xytext=(215,32.0), fontsize=9, color=INK,
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.8, mutation_scale=8))
ax.text(30,29.0,'$v=H_0d$',fontsize=9.5,color=INK)
ax.set_xlabel('distance  $d$  (Mpc)')
ax.set_ylabel('recession speed  $v$  ($10^3$ km s$^{-1}$)')
ax.set_xlim(0,500); ax.set_ylim(0,36)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.4)
```

The law does not mean that we are at the centre. Every observer, in every galaxy, sees
the same proportional recession: the expansion is uniform, like raisins moving apart
in a rising loaf of bread. There is no centre and no edge.

### 22.3.4 The age of the universe

If the expansion had always had its present rate, a galaxy now at distance $d$ would
have been at our position a time $d/v=1/H_0$ ago. So $1/H_0$ is a rough estimate of
the age:

$$ \frac{1}{H_0}=\frac{3.09\times10^{22}\ \text{m}}{70\times10^{3}\ \text{m s}^{-1}}
=4.4\times10^{17}\ \text{s}\approx14\ \text{Gyr} $$

The accepted age is **13.8 billion years**, slightly less than 14 Gyr because the
expansion was faster in the past (the galaxies were braking under their mutual
gravity) and is speeding up now under dark energy. The estimate $1/H_0$ is therefore
an **upper limit** for a universe whose expansion is slowing, and a rough figure in
any case. Quote it as "about 14 billion years", and quote the accepted value as 13.8.

| Quantity | Value (approximate) |
|---|---|
| Age of the universe | 13.8 Gyr |
| Hubble constant $H_0$ | 70 km s⁻¹ Mpc⁻¹ |
| $1/H_0$ | 14 Gyr |
| CMB temperature | 2.725 K |
| CMB last-scattering time | 380 000 years after the Big Bang |
| Redshift of the CMB | $z\approx1100$ |
| Ordinary (baryonic) matter | about 5 % of the energy budget |
| Dark matter | about 27 % |
| Dark energy | about 68 % |

::: caution Three statements that are wrong
1. **"The Big Bang was an explosion in space."** It was an expansion *of* space; there
   is no centre from which galaxies fly out.
2. **"The universe has an edge."** The observable universe has a horizon, but the
   whole universe is not known to have an edge.
3. **"Hubble's law proves the galaxies are moving away through space."** It describes
   the expansion of the space between them. On small scales — inside a galaxy or a
   cluster — gravity holds things together, and Hubble's law does not apply.
:::

::: example Worked example 22.2 — a galaxy's distance
**Problem.** A galaxy is observed with a redshift $z=0.02$. Taking
$H_0=70$ km s⁻¹ Mpc⁻¹, estimate its distance.

**Solution.** $v\approx cz=3.0\times10^{5}\times0.02=6.0\times10^{3}$ km s⁻¹.

$d=\dfrac{v}{H_0}=\dfrac{6000}{70}=86$ Mpc.

**Check.** $86$ Mpc is about 280 million light years. The redshift is small enough
that the linear formula is acceptable (2 % error at this level).
:::

::: example Worked example 22.3 — the Hubble time
**Problem.** Show that $1/H_0$ with $H_0=70$ km s⁻¹ Mpc⁻¹ gives about 14 billion
years.

**Solution.** Convert $H_0$ to SI:
$H_0=\dfrac{70\times10^{3}\ \text{m s}^{-1}}{3.09\times10^{22}\ \text{m}}
=2.27\times10^{-18}\ \text{s}^{-1}$.

$\dfrac{1}{H_0}=\dfrac{1}{2.27\times10^{-18}}=4.4\times10^{17}$ s
$=\dfrac{4.4\times10^{17}}{3.16\times10^{7}}=1.4\times10^{10}$ years.

**Check.** 14 billion years is the right order; the accepted 13.8 Gyr is close because
the correction for the changing expansion rate is only a few per cent.
:::

## Formula and fact sheet

| Item | Fact or formula |
|---|---|
| Quarks | u, d, c, s, t, b; charges $+\frac{2}{3},-\frac{1}{3},+\frac{2}{3},-\frac{1}{3},+\frac{2}{3},-\frac{1}{3}$ |
| Leptons | e, μ, τ (charge $-1$) and $\nu_e,\nu_\mu,\nu_\tau$ (charge 0) |
| Proton, neutron | $uud$ (charge $+1$), $udd$ (charge 0) |
| Pions | $\pi^+=u\bar d$, $\pi^-=\bar ud$, $\pi^0$ a $u\bar u/d\bar d$ mixture |
| Hadrons | baryons $=qqq$; mesons $=q\bar q$; both feel the strong force |
| Baryon number | $+\frac{1}{3}$ per quark, $-\frac{1}{3}$ per antiquark; conserved |
| Annihilation | $e^++e^-\to2\gamma$, each $0.511$ MeV |
| Pair production | threshold $2m_ec^2=1.02$ MeV, needs a nucleus nearby |
| Strong force | gluon; range $\sim10^{-15}$ m; strength 1 |
| Electromagnetic | photon; infinite range; strength $\sim10^{-2}$ |
| Weak | $W^\pm$, $Z^0$; range $\sim10^{-18}$ m; strength $\sim10^{-6}$ |
| Gravity | graviton (hypothetical); infinite range; strength $\sim10^{-38}$ |
| Higgs | $H^0$, mass about 125 GeV/$c^2$, discovered at CERN 2012; gives mass to fundamental particles |
| Nanoscale | 1–100 nm; $1\ \text{nm}=10^{-9}$ m |
| Redshift | $z=(\lambda_{obs}-\lambda_{emit})/\lambda_{emit}$; $v\approx cz$ for small $z$ |
| Hubble's law | $v=H_0d$; $H_0\approx70$ km s⁻¹ Mpc⁻¹; $1\ \text{Mpc}=3.09\times10^{22}$ m |
| Hubble time | $1/H_0\approx4.4\times10^{17}$ s $\approx14$ Gyr |
| Age of universe | 13.8 Gyr |
| CMB | 2.725 K, emitted 380 000 years after the Big Bang, $z\approx1100$ |

## Chapter summary

- The Standard Model has six quarks and six leptons, in three generations, each with
  an antiparticle of the same mass and opposite charge.
- Quarks are confined: only combinations are seen. Baryons are three quarks
  ($p=uud$, $n=udd$); mesons are a quark–antiquark pair ($\pi^+=u\bar d$).
- The four interactions are strong (gluon), electromagnetic (photon), weak ($W$, $Z$)
  and gravitational (graviton, not yet observed), with strengths in the approximate
  ratio $1:10^{-2}:10^{-6}:10^{-38}$ and ranges from $10^{-18}$ m to infinity.
- The Higgs boson (about 125 GeV/$c^2$, found at CERN in 2012) is the quantum of the
  field that gives mass to fundamental particles — not to the photon or gluon, and not
  most of the mass of a proton.
- Nanotechnology works at 1–100 nm, where the surface-to-volume ratio is large and
  quantum effects set in; real uses include drug delivery, water treatment, coatings
  and nanoscale transistors.
- The Big Bang is supported by the expansion, the 2.725 K CMB and the abundances of
  the light elements.
- Redshift $z=\Delta\lambda/\lambda$, with $v\approx cz$ for small $z$; Hubble's law
  $v=H_0d$ with $H_0\approx70$ km s⁻¹ Mpc⁻¹.
- $1/H_0\approx14$ Gyr is a rough age; the accepted age is 13.8 Gyr, and the expansion
  has no centre.

## Practice questions

**Set A — Recall (21 questions)**

1. The number of quarks in the Standard Model is
   (a) three (b) four (c) six (d) twelve
2. The quark content of a proton is
   (a) $udd$ (b) $uud$ (c) $u\bar u$ (d) $ud$
3. The charge of an up quark is
   (a) $-\frac{1}{3}e$ (b) $-e$ (c) zero (d) $+\frac{2}{3}e$
4. A positron is the antiparticle of
   (a) an electron (b) a proton (c) a neutron (d) a neutrino
5. Which of the following is a lepton?
   (a) proton (b) neutron (c) muon (d) pion
6. The particle that carries the strong force is the
   (a) photon (b) gluon (c) $W$ boson (d) graviton
7. The range of the weak interaction is about
   (a) $10^{-18}$ m (b) infinite (c) $10^{-15}$ m (d) 1 m
8. The Higgs boson was discovered in 2012 at
   (a) a laboratory in Chicago (b) the Cavendish Laboratory (c) the Stanford linear collider (d) CERN
9. The mass of the Higgs boson is about
   (a) 1 GeV/$c^2$ (b) 125 GeV/$c^2$ (c) 938 MeV/$c^2$ (d) 511 keV/$c^2$
10. Hadrons are particles that
   (a) do not feel the strong force (b) are all leptons (c) feel the strong force and are made of quarks (d) are all massless
11. A baryon is made of
   (a) three quarks (b) two quarks (c) a quark and an antiquark (d) one quark
12. A meson consists of
   (a) three quarks (b) two leptons (c) two baryons (d) a quark and an antiquark
13. The quark content of the $\pi^+$ meson is
   (a) $ud$ (b) $u\bar u$ (c) $u\bar d$ (d) $d\bar d$
14. The baryon number of a proton is
   (a) 0 (b) $+1$ (c) $-1$ (d) $+\frac{1}{3}$
15. The ratio of the strong force to the electromagnetic force between two nucleons is about
   (a) $1:10^{-2}$ (b) $1:10^{-6}$ (c) $1:10^{-38}$ (d) $1:1$
16. Nanotechnology deals with structures whose size is about
   (a) 1–100 μm (b) 0.1–1 nm (c) 100–1000 nm (d) 1–100 nm
17. One nanometre equals
   (a) $10^{-6}$ m (b) $10^{-9}$ m (c) $10^{-12}$ m (d) $10^{-3}$ m
18. The temperature of the cosmic microwave background is about
   (a) 0.27 K (b) 27 K (c) 2.7 K (d) 300 K
19. Hubble's law is written as
   (a) $v=H_0d$ (b) $v=H_0/d$ (c) $d=H_0v$ (d) $v=H_0d^2$
20. The Hubble constant is about
   (a) 70 km s⁻¹ per light year (b) 70 m s⁻¹ per Mpc (c) 70 km s⁻¹ per kpc (d) 70 km s⁻¹ per Mpc
21. The accepted age of the universe is about
   (a) 4.6 billion years (b) 13.8 billion years (c) 100 billion years (d) 1.4 million years

::: note Answers and explanations — Set A
**1.** (c) — six: up, down, charm, strange, top and bottom, in three generations of two.
**2.** (b) — two up quarks and one down: $+\frac{2}{3}+\frac{2}{3}-\frac{1}{3}=+1$, the proton charge.
**3.** (d) — up-type quarks (u, c, t) carry $+\frac{2}{3}e$; down-type (d, s, b) carry $-\frac{1}{3}e$.
**4.** (a) — the positron has the electron's mass and the opposite charge; it is the first antiparticle found (1932).
**5.** (c) — the muon is a heavy electron, a fundamental lepton. Protons and neutrons are baryons, the pion is a meson.
**6.** (b) — gluons bind quarks and hold the nucleons together; the photon carries the electromagnetic force.
**7.** (a) — the $W$ and $Z$ bosons are very heavy, which confines the weak force to about $10^{-18}$ m, far less than a nucleon.
**8.** (d) — ATLAS and CMS at CERN's Large Hadron Collider announced the discovery in July 2012.
**9.** (b) — about 125 GeV/$c^2$, roughly 133 proton masses. 938 MeV is the proton and 511 keV the electron.
**10.** (c) — hadrons are the strongly interacting composite particles: baryons and mesons.
**11.** (a) — three quarks, as in the proton and neutron. A quark–antiquark pair is a meson.
**12.** (d) — a meson is a quark bound to an antiquark, which is why it has integer charge and baryon number zero.
**13.** (c) — $u\bar d$: $+\frac{2}{3}-(-\frac{1}{3})=+1$, the charge of $\pi^+$.
**14.** (b) — three quarks at $+\frac{1}{3}$ each give $B=+1$; the antiproton has $B=-1$.
**15.** (a) — the strong force is roughly a hundred times the electromagnetic force at nuclear separations, hence the ratio $1:10^{-2}$.
**16.** (d) — 1 to 100 nm: above a single atom (0.1 nm) and below a virus (about 100 nm).
**17.** (b) — a nanometre is $10^{-9}$ m, a millionth of a millimetre.
**18.** (c) — 2.725 K, the cooled remnant of the hot early universe; 300 K would be room temperature.
**19.** (a) — recession speed is proportional to distance, with $H_0$ as the constant of proportionality.
**20.** (d) — about 70 km s⁻¹ for every megaparsec of distance; the unit must have distance in the denominator.
**21.** (b) — 13.8 billion years from the Planck measurements; 4.6 billion is the age of the Earth.
:::

**Set B — Understanding (12 questions)**

1. A neutron contains three charged quarks, yet it is neutral because
   (a) the quarks are neutral inside a nucleon (b) the charges add to zero (c) it contains an electron (d) the strong force cancels the charge
2. When an electron and a positron annihilate at rest, the products are
   (a) one photon of 1.02 MeV (b) two protons (c) one photon of 0.51 MeV (d) two photons of 0.51 MeV each
3. A single free quark has never been observed because
   (a) quarks are confined by the strong force (b) quarks have no charge (c) quarks are too light to detect (d) quarks decay immediately
4. Beta decay, in which a neutron becomes a proton, is caused by the
   (a) strong force (b) electromagnetic force (c) weak force (d) gravitational force
5. Gravity is negligible between two protons because
   (a) protons have no mass (b) it is enormously weaker than the other forces (c) it has an infinite range (d) it acts only on electrons
6. The Higgs field gives mass to
   (a) all particles without exception (b) photons and gluons (c) only the proton and neutron (d) fundamental particles such as the $W$ boson and the quarks
7. Nanoparticles have properties different from the bulk material mainly because
   (a) they are radioactive (b) they contain fewer protons (c) their surface-to-volume ratio is very large (d) they have no crystal structure
8. The cosmic microwave background is evidence for the Big Bang because it is
   (a) the cooled radiation of the hot early universe, arriving from all directions (b) light from the nearest star (c) the glow of our own galaxy (d) radiation from black holes only
9. According to Hubble's law, if a galaxy's distance is doubled, its recession speed
   (a) halves (b) doubles (c) stays the same (d) becomes four times
10. The light from a distant galaxy is redshifted because
   (a) the galaxy is made of different atoms (b) the galaxy is moving towards us (c) the light loses energy in dust (d) space expands while the light travels
11. $1/H_0$ gives only an estimate of the age of the universe because
   (a) the expansion rate has not been constant (b) $H_0$ is not measured in SI units (c) the speed of light changes (d) galaxies have finite size
12. Which of the following is NOT a baryon?
   (a) proton (b) neutron (c) pion (d) $\Lambda$ particle

::: note Answers and explanations — Set B
**1.** (b) — $+\frac{2}{3}-\frac{1}{3}-\frac{1}{3}=0$. The quarks keep their charges; the total is zero, so the neutron is neutral.
**2.** (d) — energy $2m_ec^2=1.02$ MeV shared by two photons, emitted back to back so that momentum also balances.
**3.** (a) — the strong force between quarks does not weaken with distance in the usual way; pulling them apart makes new quark pairs instead of freeing one.
**4.** (c) — the weak force changes quark flavour, turning a down quark into an up quark and emitting a $W^-$; the strong and electromagnetic forces cannot do this.
**5.** (b) — gravity is about $10^{-38}$ of the strong force; between two protons the electrical repulsion is some 36 powers of ten larger than their gravitational attraction.
**6.** (d) — the Higgs mechanism gives mass to the $W$ and $Z$ bosons, quarks and charged leptons. Photons and gluons stay massless, and most of a nucleon's mass comes from gluon-field energy.
**7.** (c) — at 10 nm a large fraction of the atoms sit on the surface, and quantum confinement changes the allowed energies, so colour, melting point and reactivity all shift.
**8.** (a) — the CMB is a nearly perfect 2.725 K blackbody coming from every direction, exactly what a hot, dense early universe cooled to about 3000 K and then released would leave behind.
**9.** (b) — $v=H_0d$ is linear, so doubling $d$ doubles $v$.
**10.** (d) — the wavelength is stretched by the expansion of space during the light's journey; it is not a Doppler shift through a static space.
**11.** (a) — the formula assumes a constant rate; the real expansion was faster in the past, so the true age (13.8 Gyr) is a little less than 14 Gyr.
**12.** (c) — the pion is a meson (quark–antiquark), with baryon number zero. The other three are three-quark states.
:::

**Set C — Application (9 questions)**

1. A galaxy is 100 Mpc away. Taking $H_0=70$ km s⁻¹ Mpc⁻¹, its recession speed is
   (a) 700 km s⁻¹ (b) 70 km s⁻¹ (c) 7000 km s⁻¹ (d) $7\times10^{5}$ km s⁻¹
2. A galaxy is receding at 2100 km s⁻¹. With $H_0=70$ km s⁻¹ Mpc⁻¹, its distance is
   (a) 30 Mpc (b) 3 Mpc (c) 300 Mpc (d) 147 Mpc
3. With $H_0=70$ km s⁻¹ Mpc⁻¹, the Hubble time $1/H_0$ is about
   (a) 4.6 Gyr (b) 1.4 Gyr (c) 138 Gyr (d) 14 Gyr
4. A quasar has a redshift $z=0.02$. Its recession speed is about
   (a) 600 km s⁻¹ (b) 6000 km s⁻¹ (c) 60 km s⁻¹ (d) $6\times10^{5}$ km s⁻¹
5. A galaxy has $z=0.05$. Taking $H_0=70$ km s⁻¹ Mpc⁻¹, its distance is about
   (a) 21 Mpc (b) 75 Mpc (c) 214 Mpc (d) 1500 Mpc
6. The minimum photon energy needed to produce an electron–positron pair near a nucleus is
   (a) 0.511 MeV (b) 1.5 MeV (c) 2.04 MeV (d) 1.02 MeV
7. The total charge of the quark combination $u\bar u$ is
   (a) zero (b) $+e$ (c) $-e$ (d) $+\frac{2}{3}e$
8. An electron and a positron annihilate at rest into two photons. The energy of each photon is
   (a) 1.02 MeV (b) 0.511 MeV (c) 0.255 MeV (d) 2.04 MeV
9. If the Hubble constant were 140 instead of 70 km s⁻¹ Mpc⁻¹, the Hubble time would be about
   (a) 28 Gyr (b) 14 Gyr (c) 3.5 Gyr (d) 7 Gyr

::: note Answers and explanations — Set C
**1.** (c) — $v=H_0d=70\times100=7000$ km s⁻¹. Option (a) divides instead of multiplying.
**2.** (a) — $d=v/H_0=2100/70=30$ Mpc.
**3.** (d) — $H_0=70$ km s⁻¹ Mpc⁻¹ $=2.27\times10^{-18}$ s⁻¹, so $1/H_0=4.4\times10^{17}$ s $\approx14$ Gyr.
**4.** (b) — $v\approx cz=3.0\times10^{5}\times0.02=6000$ km s⁻¹.
**5.** (c) — $v=3.0\times10^{5}\times0.05=1.5\times10^{4}$ km s⁻¹, then $d=15000/70=214$ Mpc.
**6.** (d) — the pair has rest energy $2m_ec^2=2\times0.511=1.02$ MeV, so that is the threshold.
**7.** (a) — $+\frac{2}{3}-\frac{2}{3}=0$; a quark and its own antiquark always give zero, which is why such a pair can appear in a meson with another quark.
**8.** (b) — the total energy $1.02$ MeV is shared equally by two photons, so each carries $0.511$ MeV.
**9.** (d) — the Hubble time is inversely proportional to $H_0$, so doubling $H_0$ halves it to about 7 Gyr.
:::
