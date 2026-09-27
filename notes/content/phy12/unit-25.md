---
subject: Physics
grade: 12
unit: 25
title: Recent trends in physics
hours: 6
area: Modern Physics
---

The last unit looks outward. Gravitational waves, nanotechnology and the Higgs
boson are results of the past two decades; seismology is the physics of the
ground under Nepal. The mathematics is light — what is examined is whether you
can explain the physics clearly and quote the key numbers.

::: key What the exam wants from this unit
Descriptive answers with correct detail: the four wave types and their order of
arrival, the facts of the Gorkha earthquake, what LIGO measured in 2015, what
"nanoscale" means, and what the Higgs field does. Numbers earn marks: $M_w$ 7.8,
strain $10^{-21}$, 1–100 nm, 125 GeV.
:::

## 25.1 Seismology: Surface waves (Rayleigh and Love waves); Internal waves (S and P-waves); Wave patterns of Gorkha Earthquake 2015

**Seismology** is the study of elastic waves travelling through the Earth. Nepal
sits where the Indian plate pushes north under Eurasia at about 20 mm per year
along the **Main Himalayan Thrust**; strain stored on that locked fault for
centuries is released in minutes as an earthquake. The point of rupture inside
the Earth is the **focus**; the point on the surface above it is the
**epicentre**.

### Body waves: P and S

Waves travelling *through* the interior are **body waves** (internal waves).

```figure caption="The four seismic wave types. P and S waves travel through the Earth's interior; Rayleigh and Love waves run along the surface and die away with depth."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(2, 2, figsize=(5.1, 3.4))
k = 2*np.pi/3.2
xg = np.linspace(0.2, 9.8, 46)

# --- P wave: compression / rarefaction ---
ax = axes[0, 0]
for row in (0.55, 0.0, -0.55):
    u = 0.42*np.sin(k*xg)
    ax.plot(xg + u, np.full_like(xg, row), 'o', color=ACCENT, ms=2.0)
ax.annotate('', xy=(6.2, -1.10), xytext=(4.0, -1.10),
            arrowprops=dict(arrowstyle='<|-|>', color=SERIES[1], lw=1.2, mutation_scale=9))
ax.set_title('P wave — particles move along\nthe direction of travel', fontsize=7.6)

# --- S wave: shear ---
ax = axes[0, 1]
for row in (0.55, 0.0, -0.55):
    ax.plot(xg, row + 0.34*np.sin(k*xg), 'o', color=SERIES[2], ms=2.0)
ax.annotate('', xy=(9.9, -0.35), xytext=(9.9, -1.35),
            arrowprops=dict(arrowstyle='<|-|>', color=SERIES[1], lw=1.2, mutation_scale=9))
ax.set_title('S wave — particles move across\nthe direction of travel', fontsize=7.6)

# --- Rayleigh: retrograde ellipse, decays with depth ---
ax = axes[1, 0]
for j, z in enumerate((0.0, 0.45, 0.90, 1.35)):
    a = np.exp(-1.15*z)
    ax.plot(xg - a*0.38*np.sin(k*xg), (0.55 - z) + a*0.50*np.cos(k*xg),
            'o', color=SERIES[3], ms=2.0)
th = np.linspace(0, 2*np.pi, 60)
ax.plot(1.4 + 0.32*np.cos(th), -1.60 + 0.42*np.sin(th), color=SERIES[1], lw=1.1)
ax.annotate('', xy=(1.06, -1.50), xytext=(1.16, -1.86),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.1, mutation_scale=9))
ax.set_title('Rayleigh wave — rolling,\nelliptical, dies away with depth', fontsize=7.6)

# --- Love: horizontal shear seen from above ---
ax = axes[1, 1]
for j, z in enumerate((0.0, 0.45, 0.90, 1.35)):
    a = np.exp(-1.15*z)
    ax.plot(xg, (0.55 - z) + a*0.42*np.sin(k*xg), color=SERIES[5], lw=1.2)
ax.annotate('', xy=(9.9, -1.05), xytext=(9.9, -0.3),
            arrowprops=dict(arrowstyle='<|-|>', color=SERIES[1], lw=1.1, mutation_scale=8))
ax.set_title('Love wave (seen from above) —\nside-to-side, horizontal only', fontsize=7.6)

for ax in axes.ravel():
    ax.set_xlim(-0.2, 10.6); ax.set_ylim(-2.15, 1.30)
    ax.axis('off')
fig.subplots_adjust(hspace=0.55, wspace=0.06)
```

**P-waves (primary, longitudinal).** The ground is alternately compressed and
stretched *along* the direction of travel, like sound in air. At about
6 km s⁻¹ in the crust they are the fastest waves and arrive first. A compression
needs only a change of volume, so P-waves pass through **solids and liquids
alike**.

**S-waves (secondary, transverse).** Particles move *at right angles* to the
direction of travel, shearing the rock sideways, at about 3.5 km s⁻¹. A liquid
has no rigidity, so **S-waves cannot pass through liquids** — the S-wave shadow
zone beyond $103^{\circ}$ from an epicentre is the direct evidence that the
outer core is molten.

### Surface waves: Rayleigh and Love

Surface waves are guided along the boundary between ground and air. They are
slower than body waves, so they arrive last, but they carry the largest
amplitude and do most of the damage, and they die away exponentially with
depth.

| Wave | Type | Particle motion | Typical speed | Note |
|---|---|---|---|---|
| P | body, longitudinal | along the ray | 6 km s⁻¹ | passes through liquids |
| S | body, transverse | perpendicular to the ray | 3.5 km s⁻¹ | blocked by liquids |
| Love | surface, transverse | horizontal, across the ray | 3 km s⁻¹ | needs a slow surface layer |
| Rayleigh | surface | retrograde vertical ellipse | 2.7 km s⁻¹ | "ground roll"; largest |

::: memory Order of arrival
**P** before **S** before **L**ove before **R**ayleigh — "**P**lease **S**tart
**L**eaving **R**ightaway".
:::

Because P and S travel at different speeds, the gap between their arrival times
measures the distance to the epicentre:

$$ \Delta t = \frac{d}{v_S} - \frac{d}{v_P}
\qquad \Rightarrow \qquad d = \Delta t\left(\frac{v_Pv_S}{v_P - v_S}\right) $$

Three stations give three circles on a map, and the epicentre is where they
meet.

```figure caption="Shape of a seismogram close to the 2015 Gorkha epicentre. The small, fast P arrival is followed by the larger S waves, and then by long-period surface waves. Kathmandu's soft basin sediments amplified the 4–5 s surface-wave motion and kept it going for tens of seconds."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0, 2.8))
t = np.linspace(0, 90, 9000)
rng = np.random.default_rng(7)

def packet(t0, amp, f, dec, rise=0.4):
    s = np.clip(t - t0, 0, None)
    env = (1 - np.exp(-s/rise))*np.exp(-s/dec)*(t > t0)
    return amp*env*np.sin(2*np.pi*f*(t - t0))

trace = (packet(12, 0.30, 2.6, 3.5) + packet(22, 0.70, 1.2, 4.5)
         + packet(29, 1.00, 0.22, 15.0) + 0.012*rng.standard_normal(t.size))
ax.plot(t, trace, color=INK, lw=0.7)
for x, lab, col in [(12, 'P', ACCENT), (22, 'S', SERIES[2])]:
    ax.plot([x, x], [-0.95, 1.25], color=col, lw=0.9, ls='--')
    ax.annotate(lab, (x, 1.32), color=col, fontsize=9, ha='center')
ax.plot([29, 29], [-0.95, 1.25], color=SERIES[3], lw=0.9, ls='--')
ax.annotate('surface waves', xy=(29.4, 1.30), xytext=(34, 1.72),
            color=SERIES[3], fontsize=8.6, ha='left',
            arrowprops=dict(arrowstyle='-', color=SERIES[3], lw=0.8))
ax.annotate('', xy=(22, -1.15), xytext=(12, -1.15),
            arrowprops=dict(arrowstyle='<|-|>', color=SERIES[1], lw=1.2, mutation_scale=9))
ax.annotate('S − P = 10 s  →  d ≈ 84 km', (17, -1.28), ha='center', va='top',
            fontsize=8.2, color=SERIES[1])
ax.set_xlabel('time after the rupture (s)'); ax.set_ylabel('ground velocity (arb.)')
ax.set_xlim(0, 90); ax.set_ylim(-1.95, 2.05)
ax.set_yticks([])
ax.spines[['top', 'right', 'left']].set_visible(False)
```

::: example Worked example 25.1
**Problem.** A Kathmandu station records the first P-wave at 11:56:22 and the
first S-wave at 11:56:32. Taking $v_P = 6.0\ \text{km s}^{-1}$ and
$v_S = 3.5\ \text{km s}^{-1}$, find the distance to the epicentre.

**Solution.** $\Delta t = 10\ \text{s}$.

$$ d = \Delta t\left(\frac{v_Pv_S}{v_P - v_S}\right)
= 10 \times \frac{6.0 \times 3.5}{6.0 - 3.5} = 10 \times \frac{21}{2.5} $$

$$ d = 10 \times 8.4 = 84\ \text{km} $$

Barpak, the 2015 epicentre, is about 80 km from Kathmandu.
:::

### Wave patterns of the Gorkha Earthquake 2015

| Quantity | Value |
|---|---|
| Date and time | 25 April 2015, 11:56 NST (06:11 UTC) |
| Moment magnitude | $M_w$ 7.8 (Nepal's National Seismological Centre: $M_L$ 7.6) |
| Epicentre | Barpak, Gorkha district (28.2° N, 84.7° E), ~80 km WNW of Kathmandu |
| Focal depth | about 15 km — **shallow** |
| Fault | Main Himalayan Thrust, dipping a few degrees |
| Rupture | ~140 km **eastwards** at ~3.3 km s⁻¹, maximum slip ~6 m |
| Largest aftershock | $M_w$ 7.3, 12 May 2015, near Dolakha |
| Casualties | about 8,970 killed, 22,300 injured |

Three features of the recorded waves explain the damage.

1. **Little high-frequency energy.** The fault slipped smoothly rather than
   jerkily, so peak ground acceleration in Kathmandu was only about $0.16g$ —
   far less than expected for $M_w$ 7.8. Many ordinary houses therefore survived.
2. **Strong long-period shaking.** The soft lake sediments filling the Kathmandu
   valley resonated at a period of **4–5 s**, amplifying the surface waves and
   keeping the ground moving for tens of seconds. Tall flexible buildings, whose
   natural period is near 4–5 s, were shaken hardest; short stiff ones were not.
3. **Eastward directivity.** The rupture ran east, so the waves piled up in that
   direction. Sindhupalchok, east of the epicentre, lost the most lives.

::: caution Magnitude and intensity are different quantities
**Magnitude** ($M_w$) is one number for the whole earthquake, fixed by the energy
released at the source. **Intensity** (Modified Mercalli, I–XII) describes the
shaking *at one place* and differs from village to village with distance and
soil. One earthquake has one magnitude but many intensities; an increase of 1 in
$M_w$ means about 32 times more energy.
:::

## 25.2 Gravitational Wave; Nanotechnology; Higgs Boson

### Gravitational waves

Einstein's general theory of relativity (1915) describes gravity not as a force
but as curvature of spacetime. When a massive body accelerates
non-symmetrically, that curvature ripples outwards at the speed of light: these
ripples are **gravitational waves**.

A passing wave stretches space in one direction while squeezing it in the
perpendicular direction. The quantity measured is the **strain**

$$ h = \frac{\Delta L}{L} $$

and even for the strongest sources reaching Earth $h \approx 10^{-21}$ — which
is why detection took a century.

**LIGO.** Each detector is a giant Michelson interferometer with two evacuated
arms **4 km** long at right angles. A laser beam is split between the arms,
reflected and recombined; a passing wave lengthens one arm and shortens the
other, shifting the interference fringes. Two detectors 3,000 km apart (Hanford
and Livingston, USA) must see the same signal within milliseconds, which rules
out local disturbances.

::: example Worked example 25.2
**Problem.** A wave of strain $h = 1.0\times10^{-21}$ passes through a LIGO arm
of length $L = 4.0$ km. Find the change in the arm's length and compare it with
a proton radius, $0.84\times10^{-15}$ m.

**Solution.**

$$ \Delta L = hL = (1.0\times10^{-21})(4.0\times10^{3}) = 4.0\times10^{-18}\ \text{m} $$

$$ \frac{\Delta L}{r_{proton}} = \frac{4.0\times10^{-18}}{0.84\times10^{-15}}
= 4.8\times10^{-3} \approx \frac{1}{210} $$

LIGO measures a length change about **one two-hundredth of a proton radius** —
hence the multi-stage pendulums and ultra-high vacuum.
:::

**GW150914 — the first detection.** On 14 September 2015 both LIGO detectors
recorded a 0.2 s signal whose frequency swept up from 35 Hz to 250 Hz — a
"chirp". Its source was two black holes of about 36 and 29 solar masses
spiralling together 1.3 billion light-years away. They merged into one black
hole of 62 solar masses, the missing **3 solar masses** being radiated as
gravitational waves; the peak strain was $1.0\times10^{-21}$. The result was
announced on 11 February 2016 and won the 2017 Nobel Prize in Physics for Weiss,
Barish and Thorne.

```figure caption="Model of the GW150914 chirp. As the two black holes spiral in, the frequency and amplitude rise together (inspiral), peak at the merger, and then decay as the new black hole settles down (ringdown)."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0, 2.7))

Mc = 28.1                       # chirp mass in solar masses
tau0 = 28.1*4.925e-6            # G*Mc/c^3 in seconds
t1 = np.linspace(-0.20, -0.0016, 6000)
tau = -t1
f = (1/np.pi)*(5.0/(256.0*tau))**0.375 * tau0**(-0.625)
dt = t1[1] - t1[0]
phi = 2*np.pi*np.cumsum(f)*dt
h1 = (f/f[-1])**(2.0/3.0)*np.cos(phi)

t2 = np.linspace(-0.0016, 0.034, 1600)
fr = 250.0
h2 = np.exp(-(t2 - t2[0])/0.0035)*np.cos(phi[-1] + 2*np.pi*fr*(t2 - t2[0]))

t = np.concatenate([t1, t2]); h = np.concatenate([h1, h2])
h = h/np.max(np.abs(h))
ax.plot(t, h, color=ACCENT, lw=1.1)
ax.axvline(-0.0016, color=MUTED, lw=0.9, ls=':')
ax.annotate('inspiral', (-0.120, 1.20), ha='center', fontsize=8.4, color=MUTED)
ax.annotate('merger', (-0.005, 1.20), ha='right', fontsize=8.4, color=SERIES[1])
ax.annotate('ringdown', (0.003, 1.20), ha='left', fontsize=8.4, color=MUTED)
ax.annotate('35 Hz', (-0.196, -1.38), fontsize=8, color=MUTED)
ax.annotate('250 Hz', (-0.030, -1.38), fontsize=8, color=MUTED)
ax.set_xlabel('time before and after merger (s)')
ax.set_ylabel('strain  h  ($\\times 10^{-21}$)')
ax.set_xlim(-0.212, 0.040); ax.set_ylim(-1.60, 1.42)
ax.set_yticks([-1, 0, 1])
ax.spines[['top', 'right']].set_visible(False)
```

Gravitational-wave astronomy is now routine. **GW170817** (2017), two merging
neutron stars, was also seen by optical and gamma-ray telescopes — the start of
"multi-messenger" astronomy. LIGO's fourth observing run ended in November 2025,
and the catalogues now hold several hundred confirmed mergers.

::: caution Gravitational waves are not electromagnetic waves
They are ripples in spacetime itself, not oscillating electric and magnetic
fields. Nothing can shield you from them, and they come only from accelerating
**mass** distributions that are not spherically symmetric — a perfectly
spherical collapsing star radiates none.
:::

### Nanotechnology

::: definition Nanotechnology
Nanotechnology is the design and use of structures with at least one dimension
in the range **1 to 100 nanometres** ($1\ \text{nm} = 10^{-9}$ m), where the
properties of matter differ from those of the bulk material.
:::

```figure caption="The nanoscale in context. The shaded band from 1 nm to 100 nm is the working range of nanotechnology — larger than single atoms, smaller than the wavelength of visible light."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0, 2.8))
items = [(0.1, 'H atom', 1, 0.22), (0.34, 'graphene\n(1 atom thick)', -1, 0.20),
         (1.0, 'C₆₀', 1, 0.54), (2.0, 'DNA', -1, 0.56),
         (6.0, 'quantum dot', 1, 0.22), (100.0, 'virus', -1, 0.20),
         (550.0, 'light wavelength', 1, 0.54), (7000.0, 'red cell', -1, 0.20),
         (80000.0, 'human hair', 1, 0.22)]
ax.axvspan(1, 100, color=ACCENT, alpha=0.10)
ax.annotate('NANOSCALE  1–100 nm', (10, 0.90), ha='center', fontsize=8.4,
            color=ACCENT, weight='bold')
ax.axhline(0, color=INK, lw=1.2)
for x, lab, side, hgt in items:
    ax.plot([x], [0], 'o', color=SERIES[1] if 1 <= x <= 100 else MUTED, ms=5)
    ax.plot([x, x], [0, hgt*side], color=MUTED, lw=0.8)
    ax.annotate(lab, (x, (hgt + 0.04)*side), ha='center',
                va='bottom' if side > 0 else 'top', fontsize=7.6, color=INK)
ax.set_xscale('log'); ax.set_xlim(0.04, 1e6); ax.set_ylim(-1.05, 1.10)
ax.set_xlabel('size (nm, logarithmic scale)')
ax.set_yticks([])
ax.spines[['top', 'right', 'left']].set_visible(False)
```

**Why the nanoscale is different.** Two effects take over.

1. **Surface dominates.** For a cube of side $L$ the surface-to-volume ratio is
   $6/L$, so shrinking a 1 cm grain to a 10 nm grain multiplies it by a million
   and almost every atom sits on the surface. Nanoparticles are therefore superb
   catalysts and absorbers.
2. **Quantum confinement.** In a particle only a few nanometres across the
   electron's de Broglie wave is squeezed and its energy levels spread apart
   (Unit 23), so the band gap — and hence the colour — depends on *size*.
   Semiconductor "quantum dots" of one material glow red at 6 nm and blue at
   2 nm.

| Nanomaterial | Structure | Property and use |
|---|---|---|
| Fullerene C₆₀ (1985) | hollow ball of 60 carbon atoms, ~1 nm | drug carriers, lubricants |
| Carbon nanotube (1991) | rolled graphene cylinder, 1–2 nm | ~100× the tensile strength of steel |
| Graphene (2004) | one carbon layer, 0.34 nm thick | strongest known material; Nobel Prize 2010 |
| Quantum dot | semiconductor crystal 2–10 nm | size-tunable colour; QLED screens |
| TiO₂ / ZnO nanoparticle | oxide crystal ~30 nm | absorbs UV, looks clear — sunscreen |

Uses already in the field include targeted drug delivery, nanofiltration
membranes that strip arsenic and iron from tube-well water, water-repellent
coatings, chemical sensors and the transistors in every phone. The guiding idea
goes back to Feynman's 1959 lecture *There's Plenty of Room at the Bottom*.

### Higgs boson

The **Standard Model** lists the fundamental particles: six quarks, six leptons
and the force-carrying bosons (photon, gluon, W, Z). Its equations, however, stay
consistent only if all of them are **massless**, which they plainly are not.

The way out, proposed in 1964 by Peter Higgs and independently by Englert and
Brout and by others, is the **Higgs field**, which fills all of space with a
non-zero value. Particles moving through it are dragged, and that resistance is
what we measure as mass: the top quark and the W and Z bosons couple strongly
and are heavy, while the photon does not couple at all and stays massless.

The quantum of the Higgs field is the **Higgs boson**, and finding it was the
last great test of the Standard Model.

| Fact | Value |
|---|---|
| Announced | 4 July 2012, CERN, by ATLAS and CMS |
| Machine | Large Hadron Collider — 27 km proton ring, 13 TeV |
| Mass | about 125 GeV/$c^{2}$ (~133 proton masses) |
| Spin | 0 — the only known fundamental scalar |
| Lifetime | ~$1.6\times10^{-22}$ s; seen only via its decay products |
| Nobel Prize | Physics 2013, Higgs and Englert |

::: example Worked example 25.3
**Problem.** The Higgs boson has a rest energy of 125 GeV. Find its mass in kg
and in proton masses ($1\ \text{eV} = 1.6\times10^{-19}$ J,
$m_p = 1.67\times10^{-27}$ kg).

**Solution.**

$$ E = 125\times10^{9} \times 1.6\times10^{-19} = 2.0\times10^{-8}\ \text{J} $$

$$ m = \frac{E}{c^{2}} = \frac{2.0\times10^{-8}}{(3\times10^{8})^{2}}
= \frac{2.0\times10^{-8}}{9.0\times10^{16}} = 2.22\times10^{-25}\ \text{kg} $$

$$ \frac{m}{m_p} = \frac{2.22\times10^{-25}}{1.67\times10^{-27}} = 133 $$

One Higgs boson weighs as much as 133 protons — about a caesium atom.
:::

::: tip A sentence examiners like
"The Higgs field gives mass to the elementary particles; the Higgs boson is a
ripple in that field, and detecting it in 2012 confirmed the mechanism." It does
**not** explain everyday mass — over 98% of an atom's mass is the binding energy
of the quarks inside its nucleons.
:::

## Chapter summary

- Body waves: **P** (longitudinal, ~6 km s⁻¹, passes through liquids) and **S**
  (transverse, ~3.5 km s⁻¹, blocked by liquids). Surface waves: **Love**
  (horizontal transverse) and **Rayleigh** (rolling ellipse, largest amplitude).
  Arrival order P, S, Love, Rayleigh.
- Epicentral distance from the S–P interval:
  $d = \Delta t\,v_Pv_S/(v_P - v_S)$; three stations fix the epicentre.
- Gorkha: 25 April 2015, $M_w$ 7.8, focus ~15 km deep near Barpak, rupture
  ~140 km eastwards on the Main Himalayan Thrust; PGA in Kathmandu only ~$0.16g$
  but strong 4–5 s basin resonance; about 8,970 deaths.
- Gravitational waves are ripples of spacetime travelling at $c$, of strain
  $h = \Delta L/L \approx 10^{-21}$. LIGO's 4 km interferometers detected
  GW150914 on 14 September 2015 (36 + 29 → 62 solar masses, 3 radiated).
- Nanotechnology works between **1 and 100 nm**, where surface-to-volume ratio
  ($6/L$) and quantum confinement change behaviour: fullerenes, nanotubes,
  graphene, quantum dots.
- The Higgs field gives elementary particles their mass; its quantum, the Higgs
  boson ($\approx 125$ GeV/$c^2$, spin 0), was found at the LHC on 4 July 2012.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Which seismic wave cannot travel through a liquid? <span class="marks">[1]</span>
   (a) P-wave (b) S-wave (c) both (d) neither
2. The wave that usually does most damage to buildings is the <span class="marks">[1]</span>
   (a) P-wave (b) S-wave (c) Rayleigh wave (d) sound wave
3. The strain at LIGO from the first detected gravitational wave was about <span class="marks">[1]</span>
   (a) $10^{-9}$ (b) $10^{-15}$ (c) $10^{-21}$ (d) $10^{-31}$
4. A structure is said to be nanoscale if one of its dimensions lies between <span class="marks">[1]</span>
   (a) 1 and 100 pm (b) 1 and 100 nm (c) 1 and 100 μm (d) 1 and 100 mm
5. The Higgs boson was discovered in 2012 at <span class="marks">[1]</span>
   (a) LIGO (b) Fermilab (c) CERN (d) the ISS

::: note Answers to Group A
**1.** (b) — a liquid has no rigidity, so it cannot carry a shear wave.
**2.** (c) — surface waves have the largest amplitude and longest period.
**3.** (c) — $h \approx 1.0\times10^{-21}$ for GW150914.
**4.** (b) — 1 nm $= 10^{-9}$ m.
**5.** (c) — by ATLAS and CMS on CERN's Large Hadron Collider.
:::

**Group B — Short answer (5 marks each)**

1. Distinguish between body waves and surface waves. Explain why P-waves arrive
   before S-waves, and why S-waves prove the outer core is liquid. <span class="marks">[5]</span>
2. A station notes an S–P interval of 25 s. Taking
   $v_P = 6.0\ \text{km s}^{-1}$ and $v_S = 3.5\ \text{km s}^{-1}$, find the
   distance to the epicentre, and explain why three stations are needed. <span class="marks">[5]</span>
3. What is a gravitational wave? Describe how LIGO detects one, and state two
   results from the 2015 detection. <span class="marks">[5]</span>
4. Define nanotechnology. Give two reasons why materials behave differently at
   the nanoscale, with an example of each. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Body waves (P, S) travel through the interior; surface waves (Love,
Rayleigh) run along the surface and decay with depth. P-waves are longitudinal
and depend on the bulk modulus, which exceeds the shear modulus, so $v_P > v_S$
and P arrives first. S-waves need rigidity, and they vanish beyond
$103^{\circ}$ from the epicentre — the outer core must be liquid.

**2.** $d = \Delta t\,\dfrac{v_Pv_S}{v_P - v_S}
= 25 \times \dfrac{6.0 \times 3.5}{2.5} = 25 \times 8.4 = 210\ \text{km}$.
One station gives only a circle of possible epicentres; two circles meet at two
points; a third picks out the correct one.

**3.** A ripple in the curvature of spacetime travelling at $c$, produced by
accelerating masses. LIGO uses a Michelson interferometer with 4 km arms: the
wave stretches one arm and squeezes the other, shifting the fringes. GW150914
showed (i) that black-hole binaries exist and merge, and (ii) that the waves
travel at the speed of light, as relativity predicts.

**4.** Definition as in §25.2. (i) The surface-to-volume ratio $6/L$ becomes
huge, so nanoparticles are highly reactive — platinum in catalytic converters.
(ii) Quantum confinement spaces out the energy levels, so the band gap depends
on size — quantum dots change colour with diameter.
:::

**Group C — Long answer (8 marks each)**

1. (a) Describe the four types of seismic wave, sketching the particle motion in
   each. <span class="marks">[4]</span>
   (b) Give an account of the wave pattern of the Gorkha Earthquake of 2015, and
   explain why damage in Kathmandu fell mainly on tall buildings. <span class="marks">[4]</span>
2. (a) What is the Higgs field, and what problem does it solve? <span class="marks">[4]</span>
   (b) The Higgs boson's rest energy is 125 GeV. Find its mass in kg, and the
   minimum uncertainty in that energy if it lives only $1.6\times10^{-22}$ s
   ($h = 6.63\times10^{-34}$ J s). <span class="marks">[4]</span>

::: note Answer to Group C question 2(b)
$E = 125\times10^{9}\times1.6\times10^{-19} = 2.0\times10^{-8}$ J, so
$m = E/c^{2} = 2.0\times10^{-8}/9.0\times10^{16} = 2.22\times10^{-25}$ kg.
From $\Delta E\,\Delta t \ge h/4\pi$,

$$ \Delta E \ge \frac{6.63\times10^{-34}}{4\pi \times 1.6\times10^{-22}}
= \frac{6.63\times10^{-34}}{2.011\times10^{-21}} = 3.30\times10^{-13}\ \text{J} $$

In electronvolts, $\Delta E = 3.30\times10^{-13}/1.6\times10^{-19}
\approx 2$ MeV — the measured "width" of the Higgs peak. The shorter the
lifetime, the broader the peak.
:::
