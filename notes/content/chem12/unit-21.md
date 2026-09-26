---
subject: Chemistry
grade: 12
unit: 21
title: Nuclear Chemistry and Applications of Radioactivity
hours: 2
area: Applied Chemistry
---

Ordinary chemistry rearranges electrons; nuclear chemistry rearranges the nucleus
itself. Because nuclear binding energies are about a million times larger than
bond energies, a gram of uranium can release as much energy as three tonnes of
coal — and the same radiation that images a patient's thyroid will, in a large
enough dose, destroy the tissue it passes through. This unit covers both sides of
that bargain.

::: key What the examiner wants from this unit
Distinguish natural from artificial radioactivity; complete and balance nuclear
equations (mass number and atomic number must balance on both sides); define the
curie, becquerel, gray and sievert; explain fission and fusion with equations; and
give named examples of industrial and medical uses. Radiocarbon dating numericals
appear regularly.
:::

## 21.1 Natural and artificial radioactivity

::: definition Radioactivity
Radioactivity is the spontaneous disintegration of an unstable nucleus with the
emission of α-particles, β-particles or γ-rays. It is a **nuclear** property: it
is unaffected by temperature, pressure, or the chemical state of the element.
:::

**Natural radioactivity** was discovered by **Henri Becquerel in 1896**, when a
uranium salt fogged a wrapped photographic plate; Marie and Pierre Curie isolated
polonium and radium from pitchblende in 1898. Every nucleus with Z > 83 is
naturally radioactive, and a few lighter ones (⁴⁰₁₉K, ¹⁴₆C) are as well.

| Property | α-particle | β-particle | γ-ray |
|---|---|---|---|
| Nature | helium nucleus, ⁴₂He²⁺ | fast electron, ⁰₋₁e | electromagnetic wave |
| Charge | +2 | −1 | 0 |
| Mass (u) | 4 | 1/1837 | 0 |
| Speed | ≈ 0.1 c | up to 0.99 c | c |
| Deflection in a field | small, towards −ve plate | large, towards +ve plate | none |
| Ionising power | very high (10 000) | medium (100) | low (1) |
| Penetrating power | low — stopped by paper | medium — stopped by 3 mm Al | very high — needs thick lead |

```figure caption="Penetrating power of the three radiations. Alpha particles are stopped by a sheet of paper, beta particles by a few millimetres of aluminium; gamma rays are only attenuated, by thick lead or concrete."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.2,2.8))
ax.set_xlim(0, 13.4); ax.set_ylim(0.3, 6.6); ax.axis('off')
ax.add_patch(FancyBboxPatch((0.3, 2.6), 1.5, 1.6, boxstyle='round,pad=0.08',
                            fc='#f2f4f7', ec=INK, lw=1.1))
ax.text(1.05, 3.4, 'source', ha='center', va='center', fontsize=7.4, color=INK)
barriers = [(4.2, 0.18, '#c9a227', 'paper'),
            (7.4, 0.45, '#9aa3ad', '3 mm\naluminium'),
            (10.6, 0.95, '#5b6472', '5 cm\nlead')]
for x, w, c, lab in barriers:
    ax.add_patch(Rectangle((x, 1.5), w, 3.9, fc=c, ec=INK, lw=0.9))
    ax.text(x + w/2, 1.05, lab, ha='center', va='top', fontsize=7.2, color=INK)
rays = [(4.65, 'α', SERIES[1], 4.9), (7.75, 'β', SERIES[0], 4.0),
        (13.2, 'γ', SERIES[2], 3.1)]
for xend, lab, c, y in rays:
    ax.annotate('', xy=(xend, y), xytext=(1.85, y),
                arrowprops=dict(arrowstyle='-|>', color=c, lw=1.6,
                                mutation_scale=12))
    ax.text(1.95, y + 0.38, lab, fontsize=9.5, color=c, ha='left')
ax.text(13.3, 3.3, 'γ only\nweakened', fontsize=6.8, color=SERIES[2],
        ha='right', va='bottom')
ax.text(6.7, 6.1, 'increasing penetrating power  →', fontsize=7.4, color=MUTED,
        ha='center')
```

Emission changes the nucleus according to the **group displacement law**:

| Emission | Change in mass number A | Change in atomic number Z | Example |
|---|---|---|---|
| α | −4 | −2 | ²³⁸₉₂U → ²³⁴₉₀Th + ⁴₂He |
| β | 0 | +1 | ²³⁴₉₀Th → ²³⁴₉₁Pa + ⁰₋₁e |
| γ | 0 | 0 | excited nucleus loses energy only |

**Artificial (induced) radioactivity** was discovered by **Irène Curie and
Frédéric Joliot in 1934**. Bombarding aluminium with α-particles gave a
radioactive isotope of phosphorus that does not occur in nature:

²⁷₁₃Al + ⁴₂He → ³⁰₁₅P + ¹₀n

³⁰₁₅P → ³⁰₁₄Si + ⁰₊₁e  (positron, half-life 2.5 min)

| Natural radioactivity | Artificial radioactivity |
|---|---|
| Shown by heavy nuclei, mostly Z > 83 | can be induced in almost any element |
| Spontaneous; cannot be started or stopped | produced by bombardment in a reactor or accelerator |
| Emits α, β, γ | often emits positrons or neutrons as well |
| Half-lives usually long | usually short, which is why such isotopes are safer in medicine |

## 21.2 Units of radioactivity

| Quantity | SI unit | Older unit | Relation |
|---|---|---|---|
| **Activity** (disintegrations per second) | becquerel, Bq = 1 dps | curie, Ci | 1 Ci = 3.7 × 10¹⁰ Bq |
| | | rutherford, Rd | 1 Rd = 10⁶ Bq |
| **Absorbed dose** (energy per kg of tissue) | gray, Gy = 1 J kg⁻¹ | rad | 1 rad = 0.01 Gy |
| **Equivalent dose** (absorbed dose × quality factor) | sievert, Sv | rem | 1 rem = 0.01 Sv |
| **Exposure** (ionisation in air) | C kg⁻¹ | roentgen, R | 1 R = 2.58 × 10⁻⁴ C kg⁻¹ |

The curie was originally the activity of 1 g of radium-226. The quality factor Q
is 1 for β and γ, but **20 for α-particles**, because an α deposits its energy
over a very short track and does far more damage per joule.

## 21.3 Nuclear reactions

A nuclear reaction is a change in the composition of a nucleus caused by
bombardment with a particle. The first artificial transmutation was carried out by
**Rutherford in 1919**:

¹⁴₇N + ⁴₂He → ¹⁷₈O + ¹₁H  , written in short as ¹⁴N(α, p)¹⁷O

**Chadwick's discovery of the neutron (1932)** used the same technique:

⁹₄Be + ⁴₂He → ¹²₆C + ¹₀n

::: key Rules for balancing a nuclear equation
1. The sum of the **mass numbers** (superscripts) is the same on both sides.
2. The sum of the **atomic numbers** (subscripts) is the same on both sides.
3. Mass and energy together are conserved: the small mass loss Δm appears as
   energy, $E = \\Delta m\\,c^2$, where 1 u releases **931.5 MeV**.
:::

| Chemical reaction | Nuclear reaction |
|---|---|
| Involves outer electrons only | involves the nucleus |
| Element identity is preserved | one element changes into another |
| Energy change 10–1000 kJ mol⁻¹ | energy change ≈ 10⁹ kJ mol⁻¹ |
| Rate depends on temperature, pressure, catalyst | independent of all of these |
| Mass is conserved | measurable mass is converted to energy |

## 21.4 Nuclear fission and fusion reactions

```figure caption="Binding energy per nucleon against mass number. Nuclei climb towards the maximum at iron-56 — heavy nuclei by splitting, light nuclei by fusing — and the energy released is the height climbed."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.9))
A = [2, 3, 4, 6, 7, 9, 12, 14, 16, 20, 24, 32, 40, 56, 63, 84, 107, 136, 184, 208, 235, 238]
B = [1.11, 2.83, 7.07, 5.33, 5.61, 6.46, 7.68, 7.48, 7.98, 8.03, 8.26, 8.49,
     8.55, 8.79, 8.75, 8.72, 8.55, 8.39, 8.00, 7.87, 7.59, 7.57]
ax.plot(A, B, '-', color=ACCENT, lw=1.4)
ax.plot(A, B, 'o', color=ACCENT, ms=2.6)
ax.plot([56], [8.79], 'o', color=SERIES[1], ms=5)
ax.annotate('⁵⁶Fe, 8.79 MeV\nmost stable', xy=(56, 8.79), xytext=(88, 6.6),
            fontsize=7.2, color=SERIES[1],
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.0,
                            mutation_scale=9))
ax.annotate('fusion', xy=(26, 8.1), xytext=(9, 4.2), fontsize=7.6,
            color=SERIES[2],
            arrowprops=dict(arrowstyle='-|>', color=SERIES[2], lw=1.2,
                            mutation_scale=10))
ax.annotate('fission', xy=(150, 8.3), xytext=(214, 6.4), fontsize=7.6,
            color=SERIES[3],
            arrowprops=dict(arrowstyle='-|>', color=SERIES[3], lw=1.2,
                            mutation_scale=10))
ax.text(238, 6.75, '²³⁵U', fontsize=7.0, color=INK, ha='center')
ax.set_xlabel('mass number A'); ax.set_ylabel('binding energy per\nnucleon (MeV)')
ax.set_xlim(0, 250); ax.set_ylim(0, 9.6)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.4)
```

**Nuclear fission** is the splitting of a heavy nucleus into two nuclei of
comparable mass, with the release of neutrons and a large amount of energy:

²³⁵₉₂U + ¹₀n → ¹⁴¹₅₆Ba + ⁹²₃₆Kr + 3¹₀n + 200 MeV

Because each fission releases more neutrons than it consumes, a **chain reaction**
is possible once the sample exceeds its **critical mass** (about 15 kg for pure
²³⁵U). Below that size too many neutrons escape from the surface.

```figure caption="Chain reaction. Each fission of a uranium-235 nucleus releases three neutrons, so the number of fissions can multiply 3, 9, 27 … in successive generations."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle
fig, ax = plt.subplots(figsize=(4.8,2.9))
ax.set_xlim(0, 11.6); ax.set_ylim(0.2, 8.4); ax.axis('off')
gens = [[4.35], [1.65, 4.35, 7.05],
        [0.75, 1.65, 2.55, 3.45, 4.35, 5.25, 6.15, 7.05, 7.95]]
ys = [7.2, 4.6, 2.0]
for g, (xs, y) in enumerate(zip(gens, ys)):
    for x in xs:
        ax.add_patch(Circle((x, y), 0.30, fc=SERIES[0] if g < 2 else '#9fc2e0',
                            ec=INK, lw=0.8))

def fan(p, y0, kids, y1):
    for k in kids:
        ax.annotate('', xy=(k, y1 + 0.32), xytext=(p, y0 - 0.32),
                    arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=0.9,
                                    mutation_scale=8))

fan(gens[0][0], 7.2, gens[1], 4.6)
for i, p in enumerate(gens[1]):
    fan(p, 4.6, gens[2][3*i:3*i+3], 2.0)
ax.annotate('', xy=(4.35, 7.6), xytext=(2.75, 8.1),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.1, mutation_scale=9))
ax.text(2.55, 8.15, 'neutron', fontsize=7.2, color=INK, ha='right')
ax.text(9.3, 7.2, '1 fission', fontsize=7.4, color=MUTED, va='center')
ax.text(9.3, 4.6, '3 fissions', fontsize=7.4, color=MUTED, va='center')
ax.text(9.3, 2.0, '9 fissions', fontsize=7.4, color=MUTED, va='center')
ax.text(0.2, 0.65, 'each circle is a ²³⁵U nucleus; red arrows are the neutrons it releases',
        fontsize=7.0, color=MUTED, ha='left')
```

**Nuclear fusion** is the joining of two light nuclei into a heavier one. It powers
the Sun, where the overall change is

4 ¹₁H → ⁴₂He + 2 ⁰₊₁e + 26.7 MeV

and the reaction used in thermonuclear devices and in experimental reactors is

²₁H + ³₁H → ⁴₂He + ¹₀n + 17.6 MeV

| | Fission | Fusion |
|---|---|---|
| Nuclei | heavy (²³⁵U, ²³⁹Pu) split | light (²H, ³H) combine |
| Starting condition | a slow neutron | 10⁷–10⁸ K ("thermonuclear") |
| Energy per reaction | ≈ 200 MeV | ≈ 17.6 MeV |
| Energy per nucleon | ≈ 0.85 MeV | ≈ 3.5 MeV — fusion is richer |
| Products | radioactive fission fragments | mostly non-radioactive helium |
| Control | achieved (reactors) | not yet achieved commercially |

::: example Worked example 21.1 — energy from one gram of uranium-235
**Problem.** Each fission of ²³⁵U releases 200 MeV. Calculate the energy released
by the complete fission of 1.00 g of ²³⁵U.
(1 MeV = 1.602 × 10⁻¹³ J, N_A = 6.022 × 10²³ mol⁻¹)

**Solution.**

Number of nuclei in 1.00 g:

$$ N = \\frac{1.00}{235} \\times 6.022 \\times 10^{23} = 2.56 \\times 10^{21} $$

Energy = 2.56 × 10²¹ × 200 MeV = 5.12 × 10²³ MeV

$$ E = 5.12 \\times 10^{23} \\times 1.602 \\times 10^{-13} = 8.2 \\times 10^{10}\\ \\mathrm{J} $$

That is **8.2 × 10⁷ kJ from one gram**. Burning one gram of coal gives about
30 kJ, so uranium yields nearly three million times more energy per gram.
:::

## 21.5 Nuclear power and nuclear weapons

In a **nuclear reactor** the chain reaction is held at exactly one new fission per
fission — a *controlled* chain reaction — and the heat raises steam for a turbine.

| Part | Material | Function |
|---|---|---|
| Fuel | UO₂ enriched to 3–4 % ²³⁵U, or ²³⁹Pu | undergoes fission |
| Moderator | graphite, heavy water D₂O, or ordinary water | slows fast neutrons so they can be captured by ²³⁵U |
| Control rods | boron steel or cadmium | absorb surplus neutrons; pushed in to slow the reactor down |
| Coolant | water, CO₂, liquid sodium | carries the heat to the boiler |
| Shield | thick concrete and lead | stops neutrons and γ-rays escaping |

A **nuclear weapon** is the same reaction left *uncontrolled*: two sub-critical
pieces of ²³⁵U or ²³⁹Pu are slammed together to exceed the critical mass, and the
whole chain runs in about a microsecond. The bomb dropped on Hiroshima in 1945
used ²³⁵U and that on Nagasaki ²³⁹Pu. A **hydrogen bomb** uses a fission bomb only
as a trigger, to reach the 10⁸ K needed for the fusion of deuterium and lithium
deuteride, and is far more powerful.

::: caution "Nuclear reactors can explode like a bomb" — they cannot
A reactor uses fuel enriched to only 3–4 % ²³⁵U, far below the ~90 % needed for a
weapon, and the assembly cannot be held together long enough for a nuclear
explosion. The real dangers of a reactor are a **steam or hydrogen explosion**
and the escape of radioactive fission products — what happened at Chernobyl
(1986) and Fukushima (2011).
:::

Nepal has no nuclear power plant; its electricity is hydro. But radioisotopes are
imported and used daily in Nepali hospitals and industry, which is why the
Nepal Atomic Energy Act and a national regulatory framework exist.

## 21.6 Industrial uses of radioactivity

| Use | Isotope | Principle |
|---|---|---|
| Thickness gauge for paper, plastic and steel sheet | ⁸⁵Kr, ⁹⁰Sr (β) | transmitted intensity falls as thickness rises; the rollers adjust automatically |
| Level gauge in sealed tanks and cement silos | ⁶⁰Co (γ) | γ-beam is blocked when material reaches the detector |
| Industrial radiography of welds and castings | ⁶⁰Co, ¹⁹²Ir (γ) | cracks show as dark lines on film — a "γ X-ray" for steel |
| Leak detection in buried pipelines | ²⁴Na (t½ = 15 h) | the tracer collects at the leak and is found with a counter at the surface |
| Engine wear and lubricant testing | ⁵⁹Fe | activity of the oil measures metal worn off the piston rings |
| Food preservation and sterilisation of syringes | ⁶⁰Co | γ-rays kill bacteria and insects without heating |
| Smoke detectors | ²⁴¹Am (α) | smoke absorbs the α-particles and the ionisation current falls |
| Polymerisation and vulcanisation | ⁶⁰Co | radiation starts free-radical cross-linking |

## 21.7 Medical uses of radioactivity

| Purpose | Isotope | Use |
|---|---|---|
| Thyroid imaging and treatment | ¹³¹I (t½ 8 d) | iodine concentrates in the thyroid; small doses scan it, large doses destroy a tumour |
| General imaging (bone, heart, kidney) | ⁹⁹ᵐTc (t½ 6 h) | pure γ-emitter, short-lived — the workhorse of nuclear medicine |
| PET scanning | ¹⁸F (t½ 110 min) | as fluorodeoxyglucose, it shows where tissue is most active |
| Cancer radiotherapy (teletherapy) | ⁶⁰Co (t½ 5.3 y) | a focused γ-beam kills dividing tumour cells |
| Brachytherapy (implants) | ¹²⁵I, ¹⁹²Ir | the source is placed inside or beside the tumour |
| Blood volume, circulation studies | ²⁴Na, ⁵¹Cr | tracer dilution |
| Sterilisation of sutures, syringes, dressings | ⁶⁰Co | cold sterilisation of sealed packets |
| Bone-marrow and leukaemia therapy | ³²P (β) | concentrates in rapidly dividing tissue |

The isotopes chosen for **diagnosis** are γ-emitters with short half-lives, so
that they leave the body quickly; those chosen for **therapy** are α- or
β-emitters, whose short range concentrates the damage on the tumour.

::: example Worked example 21.2 — activity and dose
**Problem.** (a) Convert 2.5 mCi of ⁹⁹ᵐTc to becquerel. (b) If this activity is
injected at 8 a.m., what will it be at 2 p.m. (t½ = 6 h)? (c) A 60 kg worker
absorbs 1.2 J of γ-radiation. Find the absorbed dose in gray and the equivalent
dose in sievert.

**Solution.**

(a) 1 Ci = 3.7 × 10¹⁰ Bq, so
2.5 × 10⁻³ × 3.7 × 10¹⁰ = **9.25 × 10⁷ Bq** (92.5 MBq).

(b) From 8 a.m. to 2 p.m. is 6 h = one half-life, so the activity falls to
½ × 9.25 × 10⁷ = **4.63 × 10⁷ Bq**.

(c) Absorbed dose = energy ÷ mass = 1.2 / 60 = **0.020 Gy = 20 mGy**.
For γ-rays the quality factor Q = 1, so equivalent dose
= 0.020 × 1 = **0.020 Sv = 20 mSv**. That single exposure equals the whole annual
limit for a radiation worker.
:::

## 21.8 Radiocarbon dating

Cosmic-ray neutrons in the upper atmosphere convert nitrogen into radioactive
carbon-14:

¹⁴₇N + ¹₀n → ¹⁴₆C + ¹₁H

The ¹⁴C mixes into atmospheric CO₂ and enters every living thing through
photosynthesis, so a living organism keeps a fixed ¹⁴C level giving about
**15.3 disintegrations per minute per gram of carbon**. At death the intake stops
and the ¹⁴C decays with a half-life of **5730 years**:

¹⁴₆C → ¹⁴₇N + ⁰₋₁e

Comparing the activity of a dead sample with that of living matter therefore gives
its age. The method was developed by **W. F. Libby** (Nobel Prize 1960) and works
up to about 50 000 years — beyond that too little ¹⁴C is left.

$$ \\lambda = \\frac{0.693}{t_{1/2}} \\qquad t = \\frac{2.303}{\\lambda}\\log\\frac{N_0}{N} $$

```figure caption="Decay of carbon-14. After each half-life of 5730 years the activity halves, so 25 % activity means an age of two half-lives, 11 460 years."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.8))
T = 5730.0
t = np.linspace(0, 4*T, 400)
ax.plot(t/1000, 100*0.5**(t/T), color=ACCENT, lw=1.6)
for k in (1, 2, 3):
    y = 100*0.5**k
    ax.plot([0, k*T/1000], [y, y], color=MUTED, lw=0.8, ls='--')
    ax.plot([k*T/1000, k*T/1000], [0, y], color=MUTED, lw=0.8, ls='--')
    dx, ha = (0.4, 'left') if k != 2 else (-0.5, 'right')
    ax.text(k*T/1000 + dx, y + 2.5, f'{y:.1f} %', fontsize=7.0, color=MUTED,
            ha=ha)
ax.plot([2*T/1000], [25], 'o', color=SERIES[1], ms=5)
ax.annotate('2 half-lives\n11 460 years', xy=(2*T/1000, 25), xytext=(14.5, 46),
            fontsize=7.2, color=SERIES[1],
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.0,
                            mutation_scale=9))
ax.set_xlabel('age of sample (thousands of years)')
ax.set_ylabel('¹⁴C activity remaining (%)')
ax.set_xlim(0, 23); ax.set_ylim(0, 104)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.4)
```

::: example Worked example 21.3 — dating a temple beam
**Problem.** A wooden beam taken from an old temple gives 12.0 disintegrations per
minute per gram of carbon, while fresh wood of the same kind gives 15.3. The
half-life of ¹⁴C is 5730 years. Estimate the age of the beam.

**Solution.**

$$ \\lambda = \\frac{0.693}{5730} = 1.209 \\times 10^{-4}\\ \\mathrm{year^{-1}} $$

$$ t = \\frac{2.303}{\\lambda}\\log\\frac{N_0}{N} = \\frac{2.303}{1.209\\times10^{-4}}\\log\\frac{15.3}{12.0} $$

$$ t = 1.905 \\times 10^{4} \\times \\log(1.275) = 1.905\\times10^{4} \\times 0.1055 $$

t = **2.01 × 10³ years**, so the timber was cut about 2000 years ago.

*Check:* the activity has fallen only to 78 % of its original value, much less
than one half-life, so an age well under 5730 years is reasonable.
:::

## 21.9 Harmful effects of nuclear radiations

Radiation damages tissue by **ionising** the molecules it passes through. The
ions and free radicals formed (especially from water) break DNA strands and
destroy enzymes.

| Effect | Description |
|---|---|
| **Somatic** — in the exposed person | burns, hair loss, nausea and vomiting, fall in white cell count, sterility, cataract, leukaemia and other cancers years later |
| **Genetic** — in the descendants | mutation of the germ cells, causing inherited defects |
| **Acute radiation sickness** | a whole-body dose above about 1 Sv; above 5 Sv death is likely within weeks |
| **Environmental** | fallout isotopes ⁹⁰Sr (follows calcium into bone) and ¹³¹I (into the thyroid); waste that stays dangerous for thousands of years |

Recommended limits are **1 mSv per year** for the public and **20 mSv per year**
for radiation workers, against a natural background of about 2–3 mSv a year (much
of it radon gas seeping from the ground). Protection rests on three things:
**distance** (intensity falls as 1/r²), **shielding** (lead, concrete) and
**time** (minimum exposure), with film badges or dosimeters worn to record the
dose received.

## Chapter summary

- Radioactivity is the spontaneous disintegration of an unstable nucleus;
  discovered by Becquerel (1896), it is unaffected by temperature, pressure or
  chemical combination.
- α = ⁴₂He (high ionising, low penetrating), β = ⁰₋₁e, γ = electromagnetic (low
  ionising, high penetrating). α emission: A − 4, Z − 2; β emission: A same,
  Z + 1.
- Artificial radioactivity (Joliot-Curie, 1934):
  ²⁷₁₃Al + ⁴₂He → ³⁰₁₅P + ¹₀n, and ³⁰₁₅P → ³⁰₁₄Si + ⁰₊₁e.
- Units: activity 1 Bq = 1 dps, 1 Ci = 3.7 × 10¹⁰ Bq; absorbed dose
  1 Gy = 1 J kg⁻¹ = 100 rad; equivalent dose 1 Sv = 100 rem.
- In every nuclear equation the mass numbers and the atomic numbers must balance;
  the mass defect appears as energy, with 1 u = 931.5 MeV.
- Fission: ²³⁵₉₂U + ¹₀n → ¹⁴¹₅₆Ba + ⁹²₃₆Kr + 3¹₀n + 200 MeV, giving a chain
  reaction above the critical mass. Fusion:
  ²₁H + ³₁H → ⁴₂He + ¹₀n + 17.6 MeV, needing 10⁷–10⁸ K.
- Reactor parts: fuel (3–4 % ²³⁵U), moderator (graphite or D₂O), control rods
  (boron or cadmium), coolant and concrete shield; a weapon is the same reaction
  uncontrolled.
- Industrial uses: thickness and level gauges, radiography of welds (⁶⁰Co, ¹⁹²Ir),
  leak detection (²⁴Na), sterilisation and food preservation, smoke detectors
  (²⁴¹Am). Medical uses: ⁹⁹ᵐTc imaging, ¹³¹I thyroid, ⁶⁰Co teletherapy, ³²P.
- Radiocarbon dating: ¹⁴₇N + ¹₀n → ¹⁴₆C + ¹₁H; living carbon gives 15.3 dpm g⁻¹;
  t½ = 5730 y; t = (2.303/λ) log(N₀/N).
- Radiation causes somatic and genetic damage; limits are 1 mSv yr⁻¹ (public) and
  20 mSv yr⁻¹ (workers); protect by distance, shielding and time.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Which radiation has the greatest penetrating power? <span class="marks">[1]</span>
   (a) α (b) β (c) γ (d) all are equal
2. When a nucleus emits an α-particle, its atomic number <span class="marks">[1]</span>
   (a) increases by 1 (b) decreases by 2 (c) decreases by 4 (d) is unchanged
3. 1 curie is equal to <span class="marks">[1]</span>
   (a) 3.7 × 10¹⁰ Bq (b) 10⁶ Bq (c) 1 J kg⁻¹ (d) 100 rem
4. The moderator in a nuclear reactor is used to <span class="marks">[1]</span>
   (a) absorb neutrons (b) slow down neutrons
   (c) cool the core (d) enrich the fuel
5. The half-life of ¹⁴C used in radiocarbon dating is <span class="marks">[1]</span>
   (a) 5730 days (b) 1600 years (c) 5730 years (d) 4.5 × 10⁹ years
6. The isotope most widely used for diagnostic imaging is <span class="marks">[1]</span>
   (a) ⁶⁰Co (b) ²³⁵U (c) ⁹⁹ᵐTc (d) ²⁴¹Am

::: note Answers to Group A
**1.** (c) — γ-rays are uncharged and massless, so they ionise little and travel far.
**2.** (b) — α emission removes 2 protons and 2 neutrons.
**3.** (a) — the activity of 1 g of radium-226.
**4.** (b) — slow (thermal) neutrons are captured by ²³⁵U far more readily.
**5.** (c) — 5730 years.
**6.** (c) — ⁹⁹ᵐTc is a short-lived pure γ-emitter.
:::

**Group B — Short answer (5 marks each)**

1. Distinguish between natural and artificial radioactivity with one example of
   each. <span class="marks">[5]</span>
2. Compare α, β and γ radiations under nature, charge, ionising power and
   penetrating power. <span class="marks">[5]</span>
3. Define becquerel, curie, gray and sievert, and state the relations between the
   SI and the older units. <span class="marks">[5]</span>
4. What is nuclear fission? Write the equation for the fission of ²³⁵U and explain
   the terms *chain reaction* and *critical mass*. <span class="marks">[5]</span>
5. Give four industrial and four medical applications of radioactivity, naming the
   isotope used in each. <span class="marks">[5]</span>
6. A sample of charcoal from a cave gives 3.83 dpm per gram of carbon, while
   living wood gives 15.3. Calculate the age of the charcoal
   (t½ = 5730 years). <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Natural radioactivity is the spontaneous disintegration of heavy nuclei
found in nature (²³⁸₉₂U → ²³⁴₉₀Th + ⁴₂He); artificial radioactivity is induced by
bombarding a stable nucleus with particles
(²⁷₁₃Al + ⁴₂He → ³⁰₁₅P + ¹₀n, followed by ³⁰₁₅P → ³⁰₁₄Si + ⁰₊₁e). Natural activity
occurs mostly for Z > 83 and has long half-lives; induced activity can be made in
almost any element and is usually short-lived.

**2.** See the table in §21.1: α is ⁴₂He²⁺, charge +2, ionising power ≈ 10 000,
stopped by paper; β is an electron, charge −1, ionising power ≈ 100, stopped by
3 mm of aluminium; γ is an electromagnetic wave, no charge, ionising power 1,
needs thick lead.

**3.** Becquerel = one disintegration per second; curie = 3.7 × 10¹⁰ Bq; gray =
absorbed dose of 1 J kg⁻¹ (1 rad = 0.01 Gy); sievert = absorbed dose × quality
factor (1 rem = 0.01 Sv). For β and γ, Q = 1; for α, Q = 20.

**4.** Fission is the splitting of a heavy nucleus into two lighter nuclei with
the release of neutrons and energy:
²³⁵₉₂U + ¹₀n → ¹⁴¹₅₆Ba + ⁹²₃₆Kr + 3¹₀n + 200 MeV. The three neutrons can cause
three further fissions, so the process becomes self-sustaining — a chain reaction.
The critical mass is the smallest mass of fissile material in which enough
neutrons are retained (rather than escaping through the surface) for the chain to
continue; for pure ²³⁵U it is about 15 kg.

**5.** Industrial: thickness gauges (⁸⁵Kr), radiography of welds (⁶⁰Co or ¹⁹²Ir),
pipeline leak detection (²⁴Na), smoke detectors (²⁴¹Am). Medical: thyroid scan and
therapy (¹³¹I), general imaging (⁹⁹ᵐTc), cancer teletherapy (⁶⁰Co), sterilisation
of syringes (⁶⁰Co) or bone-marrow therapy (³²P).

**6.** 3.83/15.3 = 0.25, that is ¼ of the original activity = 2 half-lives.
Age = 2 × 5730 = **11 460 years**.
By formula: λ = 0.693/5730 = 1.209 × 10⁻⁴ yr⁻¹;
t = (2.303/1.209 × 10⁻⁴) log 4 = 1.905 × 10⁴ × 0.602 = 1.15 × 10⁴ years.
:::

**Group C — Long answer (8 marks each)**

1. (a) What are nuclear fission and nuclear fusion? Write one equation for each
   and compare them under four headings. <span class="marks">[4]</span>
   (b) Describe the parts of a nuclear reactor and the function of each, and
   explain why a reactor cannot explode like a bomb. <span class="marks">[4]</span>
2. (a) Explain the principle of radiocarbon dating and state its limitations. <span class="marks">[4]</span>
   (b) Each fission of ²³⁵U releases 200 MeV. Calculate the energy released when
   0.50 g of ²³⁵U undergoes complete fission.
   (1 MeV = 1.602 × 10⁻¹³ J) <span class="marks">[4]</span>

::: note Answers to Group C
**1.** (a) Fission is the splitting of a heavy nucleus
(²³⁵₉₂U + ¹₀n → ¹⁴¹₅₆Ba + ⁹²₃₆Kr + 3¹₀n); fusion is the union of light nuclei
(²₁H + ³₁H → ⁴₂He + ¹₀n + 17.6 MeV). Compare on the nuclei involved, the starting
condition (a slow neutron versus 10⁷–10⁸ K), energy per nucleon (0.85 versus
3.5 MeV) and products (radioactive fragments versus helium) — see the table in
§21.4.
(b) Fuel (UO₂, 3–4 % ²³⁵U) provides the fissile nuclei; the moderator (graphite or
D₂O) slows the fast neutrons; control rods of boron or cadmium absorb surplus
neutrons and hold the multiplication factor at 1; the coolant carries heat to the
boiler; the concrete-and-lead shield stops radiation. It cannot explode like a
bomb because the fuel is far too dilute in ²³⁵U and the core would blow itself
apart long before a nuclear explosion could build up; the hazards are steam or
hydrogen explosions and the escape of fission products.

**2.** (a) Cosmic-ray neutrons make ¹⁴C in the atmosphere
(¹⁴₇N + ¹₀n → ¹⁴₆C + ¹₁H); it enters living matter as CO₂ and stays at a steady
level of 15.3 dpm per gram of carbon. On death the intake stops and the ¹⁴C decays
(¹⁴₆C → ¹⁴₇N + ⁰₋₁e, t½ = 5730 y), so the age follows from
t = (2.303/λ) log(N₀/N). Limitations: only for once-living material; an upper
limit of about 50 000 years; it assumes the atmospheric ¹⁴C level has been
constant, which fossil-fuel burning and bomb tests have disturbed; and the sample
must not be contaminated with modern carbon.
(b) N = (0.50/235) × 6.022 × 10²³ = 1.28 × 10²¹ nuclei.
Energy = 1.28 × 10²¹ × 200 = 2.56 × 10²³ MeV
= 2.56 × 10²³ × 1.602 × 10⁻¹³ = **4.1 × 10¹⁰ J** (4.1 × 10⁷ kJ).
:::
