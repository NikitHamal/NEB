---
subject: Chemistry
grade: CEE
unit: 12
title: Nuclear Chemistry
hours: 1
area: Physical Chemistry
---

Nuclear chemistry is the shortest chapter in the Chemistry paper — **one question** in the
fifty — but it is almost free marks, because the same six facts are asked year after year:
which radiation penetrates most, what happens to $A$ and $Z$ in alpha and beta decay, what
half-life means, how fission differs from fusion, which isotope is used for which job, and
one line of arithmetic on carbon dating. Nothing here needs a laboratory; everything needs
the table in §12.2 to be memorised exactly.

::: key What the paper asks from this chapter
- The three radiations with **charge, mass, penetration and ionising power** — the two orders run in opposite directions.
- **Alpha decay:** $A$ falls by 4, $Z$ falls by 2, the element moves two places **left**. **Beta decay:** $A$ unchanged, $Z$ rises by 1, one place **right**. **Gamma:** neither changes.
- Half-life: $t_{1/2} = 0.693/\lambda$; after $n$ half-lives the fraction left is $(1/2)^n$, and the activity falls in exactly the same way.
- Half-life is a **nuclear** property: temperature, pressure, chemical combination and physical state do not touch it.
- **Fission** splits a heavy nucleus (about 200 MeV each time); **fusion** joins light nuclei (the Sun's reaction). Both release energy because the products are more tightly bound.
- The isotope–use pairs: **Tc-99m** imaging, **I-131** thyroid, **Co-60** radiotherapy and sterilisation, **C-14** dating.
- Radiocarbon dating: $t = (t_{1/2}/0.693)\ln(A_0/A)$, with the assumption that the $^{14}$C : $^{12}$C ratio in living things has stayed constant.
:::

## 12.1 Radioactivity and the types of nuclear reaction

### What radioactivity is

::: definition Radioactivity
**Radioactivity** is the spontaneous emission of particles or electromagnetic radiation
from the nucleus of an unstable atom, accompanied by the change of that atom into a
different nuclide. It is a **nuclear** change, not a chemical one: the electrons are not
rearranged, the nucleus itself breaks up.
:::

The nucleus is held together by the strong force, which acts over a very short range and
must overcome the electrostatic repulsion of the protons. A nucleus is stable when the
neutron-to-proton ratio lies in a narrow band. Outside that band it decays:

| What is wrong with the nucleus | What it does |
|---|---|
| too many neutrons ($n/p$ too high) | beta-minus decay: a neutron turns into a proton |
| too few neutrons ($n/p$ too low) | positron emission or electron capture |
| too heavy (large $Z$, whatever the ratio) | alpha decay, or spontaneous fission |

**The history worth knowing.** Henri Becquerel found in 1896 that a uranium salt darkened a
photographic plate through black paper, with no exposure to light — the first observation of
radioactivity. Marie and Pierre Curie separated polonium and radium from pitchblende in
1898. Rutherford named the alpha and beta rays in 1899, and Villard found the third, gamma,
in 1900.

**Natural radioactivity** is shown by nuclides that exist in nature and decay on their own.
All elements beyond bismuth ($Z = 83$) are radioactive, and a few lighter nuclides are too:
potassium-40, rubidium-87, carbon-14 and tritium. The three natural series are headed by
uranium-238, uranium-235 and thorium-232; each ends in a stable isotope of lead.

**Artificial (induced) radioactivity** is radioactivity in a nuclide made in the laboratory
by bombarding a stable nucleus. Irène and Frédéric Joliot-Curie made the first one in 1934:

²⁷₁₃Al + ⁴₂He → ³⁰₁₅P + ¹₀n, and the phosphorus-30 produced is itself a positron emitter
(half-life 2.5 min). Every radioisotope used in medicine and industry is made this way, in a
nuclear reactor or a cyclotron.

| | Natural radioactivity | Artificial radioactivity |
|---|---|---|
| Source of the nuclide | found in nature (U-238, Th-232, K-40, C-14) | made by bombarding a stable nucleus |
| What is emitted | mostly α, β⁻ and γ | α, β⁻, β⁺, γ, and often neutrons |
| Number of nuclides | about 60 | over 2,000 |
| Energy of the radiation | fixed by the parent nuclide | can be chosen by choosing the reaction |
| Example | ²³⁸₉₂U → ²³⁴₉₀Th + ⁴₂He | ²⁷₁₃Al + ⁴₂He → ³⁰₁₅P + ¹₀n |

### Nuclear reactions compared with chemical reactions

| Feature | Chemical reaction | Nuclear reaction |
|---|---|---|
| What changes | the arrangement of electrons and atoms | the nucleus itself |
| New element formed? | no | usually yes (transmutation) |
| $A$ and $Z$ | unchanged | change (but the totals are conserved) |
| Energy per event | a few eV per molecule | MeV per nucleus — about a million times more |
| Mass | conserved to any measurable precision | a small **mass defect** appears as energy, $E = \Delta m\,c^2$ |
| Rate depends on | temperature, pressure, concentration, catalyst | nothing external — only on the nuclide and its half-life |
| Example | 2H₂ + O₂ → 2H₂O | ²³⁵₉₂U + ¹₀n → ¹⁴¹₅₆Ba + ⁹²₃₆Kr + 3¹₀n |

### The types of nuclear reaction

1. **Radioactive decay** — spontaneous: alpha, beta-minus, positron, electron capture, gamma,
   and spontaneous fission of very heavy nuclei.
2. **Artificial transmutation** — a nucleus is struck by a projectile (α particle, proton,
   deuteron, neutron or a gamma photon) and changes into another nuclide. Rutherford produced
   the first one in 1919: ¹⁴₇N + ⁴₂He → ¹⁷₈O + ¹₁H.
3. **Nuclear fission** — a heavy nucleus splits into two medium-sized nuclei after absorbing
   a neutron.
4. **Nuclear fusion** — two light nuclei join to make a heavier one.
5. **Neutron capture (neutron activation)** — a nucleus absorbs a neutron and becomes a
   heavier isotope of the same element, usually gamma-emitting: ⁵⁹₂₇Co + ¹₀n → ⁶⁰₂₇Co + γ.
   This is how cobalt-60 is manufactured.

::: caution "Radioactivity cannot be switched off"
A radioactive sample cannot be heated, cooled, compressed, dissolved or combined with
another element to change its half-life. The decay of a *given* nucleus is a random event
governed by the weak or strong force inside the nucleus; chemistry happens in the electron
cloud, far outside. What *can* be changed is the **chemical form**, and that changes only
where the isotope goes in the body or in a plant — not how fast it decays.
:::

## 12.2 The three radiations

| Property | Alpha, α | Beta, β⁻ | Gamma, γ |
|---|---|---|---|
| Nature | helium nucleus, ⁴₂He²⁺ | fast electron from the nucleus | electromagnetic wave (photon) |
| Charge | +2 | −1 | 0 |
| Mass | 4 u (2 protons + 2 neutrons) | 1/1837 u (about 0.00055 u) | zero rest mass |
| Speed | about 0.05$c$ (up to 0.1$c$) | up to 0.99$c$ | $c$ |
| Penetration in air | 2–8 cm | a few metres | hundreds of metres |
| Stopped by | a sheet of paper, skin | a few mm of aluminium | several cm of lead, thick concrete |
| Ionising power | very high (about 10⁴ × gamma) | moderate (about 100 × gamma) | low |
| Deflection in an electric field | towards the negative plate, slightly | towards the positive plate, strongly | not deflected |
| Effect of a magnetic field | deflected | deflected the other way | not deflected |

```figure caption="The three radiations in an electric field. Alpha particles bend towards the negative plate and only slightly, because they are heavy; beta particles bend strongly towards the positive plate because they are light; gamma rays pass straight through because they carry no charge."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.0, 3.1))
ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis('off')
# lead block with a narrow channel
ax.add_patch(Rectangle((0.4, 2.2), 1.3, 1.7, fc='#9aa4b2', ec=INK, lw=1.0, zorder=3))
ax.add_patch(Rectangle((1.55, 2.85), 0.5, 0.42, fc='white', ec=INK, lw=0.8, zorder=4))
ax.text(1.05, 4.15, 'lead', ha='center', fontsize=8.8, color=INK)
ax.text(1.05, 1.85, 'source', ha='center', fontsize=8.8, color=INK)
# plates
ax.add_patch(Rectangle((4.3, 4.35), 3.6, 0.22, fc='#c9d6e6', ec=INK, lw=0.9))
ax.add_patch(Rectangle((4.3, 1.35), 3.6, 0.22, fc='#c9d6e6', ec=INK, lw=0.9))
ax.text(6.1, 4.75, 'negative plate', ha='center', fontsize=8.6, color=INK)
ax.text(6.1, 1.02, 'positive plate', ha='center', fontsize=8.6, color=INK)
# beams
x = np.linspace(2.05, 9.2, 100)
ax.plot(x, 3.06 - 0.035*(x-2.05)**2/2, color=SERIES[1], lw=1.6)
ax.plot(x, 3.06 + 0.16*(x-2.05)**2/2, color=SERIES[0], lw=1.6)
ax.plot([2.05, 9.2], [3.06, 3.06], color=SERIES[3], lw=1.6, ls=(0, (5, 2)))
ax.text(9.0, 1.62, 'α', ha='left', va='center', fontsize=11, color=SERIES[1])
ax.text(9.0, 4.95, 'β', ha='left', va='center', fontsize=11, color=SERIES[0])
ax.text(9.05, 3.32, 'γ', ha='left', va='center', fontsize=11, color=SERIES[3])
ax.annotate('', xy=(8.6, 2.55), xytext=(8.6, 1.75),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.0))
ax.annotate('', xy=(8.6, 4.55), xytext=(8.6, 5.3),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.0))
ax.text(8.42, 2.15, 'bent', ha='right', fontsize=8.2, color=MUTED)
ax.text(8.42, 4.95, 'bent', ha='right', fontsize=8.2, color=MUTED)
ax.text(0.35, 5.55, 'field between the plates', fontsize=8.6, color=MUTED)
```

**Alpha particle.** Two protons and two neutrons, identical to a helium nucleus, emitted by
heavy nuclei that have too little binding energy per nucleon. It is heavy and slow, so it
rips electrons off every atom it passes — high ionising power — but it loses its energy
within a few centimetres of air and is stopped by paper or the dead outer layer of skin. That
makes it **harmless outside the body and the most dangerous radiation inside it**: an alpha
emitter breathed in or swallowed deposits all its energy in a few cells. Radium watch-dial
painters and radon in basements are the classic examples.

**Beta particle.** A fast electron created in the nucleus when a neutron changes into a
proton: n → p + e⁻ + ν̄ (the antineutrino, which carries away the missing energy — that is why
the beta spectrum is continuous while the alpha spectrum is a set of sharp lines). The
electron is **not** one of the orbital electrons. Beta particles are light, so they are
easily deflected and moderately penetrating, and they are stopped by a few millimetres of
aluminium or perspex.

**Gamma ray.** A high-energy photon, emitted when a nucleus left in an excited state drops to
a lower state. It carries away energy but no mass and no charge, so the nuclide does not
change: ⁶⁰₂₇Co* → ⁶⁰₂₇Co + γ. Gamma rays are the most penetrating of the three and the least
ionising; thick lead or concrete is needed.

::: caution The two orders are opposite
**Penetration:** γ > β > α. **Ionising power:** α > β > γ. A question that asks "which
radiation is most penetrating" and a question that asks "which is most ionising" have
**different** answers — this is the single most common trap in the chapter. The reason is
simple: a particle that gives up its energy quickly (strong ionisation) cannot travel far.
:::

::: memory One line for the table
**Alpha is a helium nucleus (+2, heavy, paper); beta is a nuclear electron (−1, light,
aluminium); gamma is light itself (0, no mass, lead).** Then remember that the heavy, charged,
slow one ionises most and penetrates least.
:::

## 12.3 Nuclear equations and the shift in the periodic table

### The two conservation rules

In every nuclear equation two totals are conserved:

1. **Nucleon number $A$** (mass number): the sum of the superscripts is the same on both sides.
2. **Charge $Z$** (atomic number): the sum of the subscripts, including the charge of an
   electron written as −1, is the same on both sides.

Mass itself is *not* exactly conserved — a tiny amount becomes energy — but $A$ and $Z$
always are. Balance $A$ first, then $Z$; the element symbol then follows from $Z$.

### Alpha decay

²³⁸₉₂U → ²³⁴₉₀Th + ⁴₂He

Check: $238 = 234 + 4$ and $92 = 90 + 2$. The daughter has $A$ smaller by 4 and $Z$ smaller by
2, so it sits **two places to the left** in the periodic table. Two more examples:

²²⁶₈₈Ra → ²²²₈₆Rn + ⁴₂He  (radium → radon, the gas that seeps into basements)

²¹⁸₈₄Po → ²¹⁴₈₂Pb + ⁴₂He

### Beta-minus decay

¹⁴₆C → ¹⁴₇N + ⁰₋₁e

Check: $14 = 14 + 0$ and $6 = 7 + (-1)$. $A$ is unchanged, $Z$ rises by one, so the element
moves **one place to the right**. The product has the same mass number as the parent — the
two are **isobars**. More examples:

³²₁₅P → ³²₁₆S + ⁰₋₁e  (the phosphorus-32 used as a tracer)

²¹⁴₈₂Pb → ²¹⁴₈₃Bi + ⁰₋₁e

### Positron emission and electron capture

A nucleus with too few neutrons can convert a proton into a neutron in two ways.

**Positron emission** — a positive electron leaves the nucleus:

²²₁₁Na → ²²₁₀Ne + ⁰₊₁e

Check: $22 = 22 + 0$ and $11 = 10 + 1$. Here $Z$ **falls** by one, so the element moves one
place to the left. This is the decay of the isotopes used in PET scanning.

**Electron capture** — the nucleus grabs one of its own inner electrons:

⁴⁰₁₉K + ⁰₋₁e → ⁴⁰₁₈Ar

Check: $40 = 40$ and $19 - 1 = 18$. The result is the same as positron emission: $Z$ falls by
one, $A$ unchanged. Electron capture competes with positron emission whenever the energy
available is small.

### Gamma emission

⁶⁰₂₇Co* → ⁶⁰₂₇Co + γ (or, written fully, ⁶⁰₂₇Co* → ⁶⁰₂₇Co + ⁰₀γ)

The asterisk marks a nucleus in an excited state. Nothing about $A$ or $Z$ changes, so gamma
emission alone never produces a new element. It usually follows alpha or beta decay, when the
daughter is left excited. Technetium-99m is the important case: the "m" means metastable, an
excited state that lasts long enough (6 hours) to be used in a hospital.

| Decay | Change in $A$ | Change in $Z$ | Periodic-table shift | Parent and daughter are |
|---|---|---|---|---|
| alpha, α | −4 | −2 | two places **left** | different elements, $A$ differs by 4 |
| beta-minus, β⁻ | 0 | +1 | one place **right** | **isobars** |
| positron, β⁺ | 0 | −1 | one place **left** | **isobars** |
| electron capture | 0 | −1 | one place **left** | **isobars** |
| gamma, γ | 0 | 0 | no shift | **isomers** (same nuclide, different energy) |

```figure caption="Part of the uranium-238 decay series on a neutron-number against proton-number chart. An alpha step moves the nucleus two places down and two places left; a beta step moves it one place up and one place left. The zigzag continues until lead-206."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9, 3.2))
pts = [(146, 92, '²³⁸U'), (144, 90, '²³⁴Th'), (143, 91, '²³⁴Pa'), (142, 92, '²³⁴U'),
       (140, 90, '²³⁰Th'), (138, 88, '²²⁶Ra'), (136, 86, '²²²Rn')]
for i in range(len(pts) - 1):
    x0, y0, _ = pts[i]; x1, y1, _ = pts[i + 1]
    col = SERIES[0] if y1 < y0 else SERIES[1]
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='-|>', color=col, lw=1.3, mutation_scale=9))
for x, y, lab in pts:
    ax.plot([x], [y], 'o', ms=4.2, color=INK, zorder=4)
offs = {'²³⁸U': (-1.1, 0.28), '²³⁴Th': (0.35, -0.05), '²³⁴Pa': (0.45, -0.45),
        '²³⁴U': (0.45, 0.25), '²³⁰Th': (0.35, -0.05), '²²⁶Ra': (0.35, 0.28),
        '²²²Rn': (0.35, -0.05)}
for x, y, lab in pts:
    dx, dy = offs[lab]
    ax.text(x + dx, y + dy, lab, fontsize=8.4, color=INK)
ax.annotate('α step', xy=(139.2, 89.2), xytext=(141.6, 87.1), fontsize=8.6, color=SERIES[0],
            arrowprops=dict(arrowstyle='-', color=SERIES[0], lw=0.8))
ax.annotate('β step', xy=(142.4, 91.4), xytext=(135.2, 92.2), fontsize=8.6, color=SERIES[1],
            arrowprops=dict(arrowstyle='-', color=SERIES[1], lw=0.8))
ax.set_xlabel('neutron number $N$')
ax.set_ylabel('proton number $Z$')
ax.set_xlim(133.5, 148.5); ax.set_ylim(85, 93.8)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=0.45)
```

::: example Finding the daughter nuclide
**Problem.** Radium-226 emits an alpha particle. Write the equation and state where the
daughter sits in the periodic table relative to radium.

**Solution.** An alpha particle is ⁴₂He, so the daughter has $A = 226 - 4 = 222$ and
$Z = 88 - 2 = 86$. Element 86 is radon: **²²⁶₈₈Ra → ²²²₈₆Rn + ⁴₂He**. Radon is two places to
the left of radium (group 18 instead of group 2), and still in period 6.
:::

::: example How many alpha and beta particles in a series?
**Problem.** The uranium series starts at ²³⁸₉₂U and ends at ²⁰⁶₈₂Pb. How many alpha and how
many beta particles are emitted in the whole series?

**Solution.** Only alpha decay changes $A$, and each alpha removes 4:
$(238 - 206)/4 = 8$ alpha particles. Those 8 alphas remove $8 \times 2 = 16$ units of charge,
taking $Z$ from 92 to 76. The final $Z$ is 82, which is 6 more, and each beta raises $Z$ by 1:
**6 beta particles**. Answer: 8 α and 6 β.
:::

::: caution The three mistakes that cost the mark
- In beta decay $Z$ goes **up** by one, not down, and $A$ does **not** change. The electron
  leaves with a charge of −1, so the nucleus must gain +1 to keep the charge balance.
- In alpha decay $A$ falls by **4**, not 2, and $Z$ by 2 — not by 4.
- Gamma emission changes **nothing**: an option that says "gamma decay produces a new
  element" is always wrong. If a question asks which decay leaves $A$ *and* $Z$ unchanged,
  the answer is gamma.
:::

## 12.4 The decay law and half-life

### The law

Radioactive decay is random: we cannot say when one particular nucleus will decay, but in a
large sample the rate is proportional to the number of nuclei present. With $N$ nuclei at
time $t$ and decay constant $\lambda$ (the probability of decay per nucleus per second):

$$ \frac{dN}{dt} = -\lambda N \quad\Longrightarrow\quad N = N_0 e^{-\lambda t} $$

$N_0$ is the number at $t = 0$, $N$ the number left at time $t$, and $\lambda$ has the unit
s⁻¹ (or y⁻¹ if $t$ is in years). Because the activity $A$ is proportional to $N$
($A = \lambda N$), the activity obeys exactly the same law:

$$ A = A_0 e^{-\lambda t} $$

**Half-life** $t_{1/2}$ is the time in which half of the nuclei in a sample decay. Put
$N = N_0/2$:

$$ \frac{N_0}{2} = N_0 e^{-\lambda t_{1/2}} \quad\Longrightarrow\quad \ln 2 = \lambda t_{1/2} \quad\Longrightarrow\quad t_{1/2} = \frac{0.693}{\lambda} $$

That single relation is worth more marks than the rest of the chapter, because it converts a
question about $\lambda$ into a question about $t_{1/2}$ and back.

**Counting half-lives is faster than using $e$.** If a time $t$ contains $n = t/t_{1/2}$
half-lives, then

$$ \frac{N}{N_0} = \left(\frac{1}{2}\right)^{n}, \qquad \text{fraction decayed} = 1 - \left(\frac{1}{2}\right)^{n} $$

The same fraction applies to mass of the isotope, to number of atoms and to activity — but
**not** to the total mass of the sample, because the daughter nuclei stay behind.

```figure caption="Decay of a radioisotope with a half-life of 8 days. Each 8-day step halves what is left: 100 % → 50 % → 25 % → 12.5 %. The curve never reaches zero, so the fraction decayed after three half-lives is 87.5 %, not 100 %."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9, 2.9))
t = np.linspace(0, 40, 400)
ax.plot(t, 100*np.exp(-0.693*t/8), color=ACCENT, lw=2.0)
for k in range(4):
    tk = 8*k
    ax.plot([tk, tk], [0, 100*0.5**k], color=GRID, lw=0.9, ls=':')
    ax.plot([0, tk], [100*0.5**k, 100*0.5**k], color=GRID, lw=0.9, ls=':')
    ax.plot([tk], [100*0.5**k], 'o', ms=4.5, color=ACCENT, zorder=4)
    ax.text(tk + 0.7, 100*0.5**k + 3.0, f'{100*0.5**k:g} %', fontsize=8.6, color=INK)
ax.set_xlabel('time (days)')
ax.set_ylabel('activity remaining (%)')
ax.set_xlim(0, 40); ax.set_ylim(0, 108)
ax.set_xticks([0, 8, 16, 24, 32, 40])
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=0.4)
```

::: example Three half-lives, worked the MCQ way
**Problem.** A source contains 64 mg of a radioisotope of half-life 12 hours. What mass of
that isotope remains after 36 hours, and what fraction has decayed?

**Solution.** $n = 36/12 = 3$ half-lives. Remaining $= 64 \times (1/2)^3 = 64/8 =$ **8 mg**.
Fraction decayed $= 1 - 1/8 = 7/8 =$ **87.5 %**. Note that the answer is *not* zero and not
"64 − 3 × 32": halving is not subtracting.
:::

::: example Half-life from a fraction
**Problem.** A radioisotope has fallen to 1/16 of its original activity in 60 days. Find its
half-life.

**Solution.** $(1/2)^n = 1/16$ gives $n = 4$ half-lives. $t_{1/2} = 60/4 =$ **15 days**.
:::

::: example The decay constant of carbon-14
**Problem.** Find $\lambda$ for $^{14}$C ($t_{1/2} = 5730$ y), and the time for 90 % of a
sample to decay.

**Solution.** $\lambda = 0.693/5730 = 1.21 \times 10^{-4}$ y⁻¹.
For 90 % decayed, 10 % remains: $t = \ln(10)/\lambda = 2.303/(1.21 \times 10^{-4}) \approx$
**1.9 × 10⁴ y**. That is why carbon dating is unreliable beyond about 40,000–50,000 years:
so little $^{14}$C is left that contamination by a speck of modern carbon ruins the count.
:::

### Units of radioactivity

| Unit | Symbol | What it measures | Size |
|---|---|---|---|
| becquerel | Bq | activity: decays per second | 1 Bq = 1 decay s⁻¹ (SI unit) |
| curie | Ci | activity | 1 Ci = 3.7 × 10¹⁰ Bq (activity of 1 g of radium-226) |
| rutherford | Rd | activity | 1 Rd = 10⁶ Bq (rarely used) |
| gray | Gy | absorbed dose | 1 Gy = 1 J of energy per kg of tissue |
| sievert | Sv | equivalent dose (biological harm) | 1 Sv = 1 Gy × quality factor (α: 20, β and γ: 1) |

::: caution Four statements that are false
- "After one half-life all the atoms have decayed." No — half remain; after $n$ half-lives,
  $(1/2)^n$ remain.
- "The half-life of a sample depends on how much of it there is." No — $t_{1/2}$ is a
  constant of the nuclide; a 1 g sample and a 1 kg sample both halve in the same time.
- "Cooling a radioactive source slows its decay." No — temperature has no effect.
- "The activity falls to half, so the mass of the sample falls to half." Only the mass of
  *that isotope* halves; the daughter nuclei remain in the sample.
:::

## 12.5 Nuclear fission and fusion

### Fission

**Fission** is the splitting of a heavy nucleus into two medium-sized nuclei of comparable
mass, with the release of two or three neutrons and a large amount of energy. It is started
by absorbing a slow (thermal) neutron, because the neutron has no charge and so faces no
Coulomb barrier:

²³⁵₉₂U + ¹₀n → ¹⁴¹₅₆Ba + ⁹²₃₆Kr + 3¹₀n + about 200 MeV

Check the balance: $235 + 1 = 236$ on the left and $141 + 92 + 3 = 236$ on the right;
$92 = 56 + 36$. Barium and krypton are only one possible pair — the same uranium nucleus can
split in dozens of ways (xenon-144 and strontium-90, caesium-137 and rubidium-95, and so on),
which is why reactor waste is such a mixture.

The three neutrons can split three more nuclei, which release nine neutrons, and so on: a
**chain reaction**. If on average fewer than one neutron from each fission causes another
fission, the reaction dies out (sub-critical); exactly one, it runs steadily (critical); more
than one, it grows explosively (super-critical). The **critical mass** is the smallest mass
that can sustain a chain reaction — for uranium-235 it is a few tens of kilograms, depending
on shape and the moderator around it.

**In a reactor** the chain reaction is held at exactly one neutron per fission:

| Part | Material | Job |
|---|---|---|
| fuel rods | enriched U-235 (a few per cent) sealed in zirconium or steel | supply the fissionable nuclei |
| moderator | heavy water, ordinary water or graphite | slow fast neutrons to thermal speed (slow neutrons fission U-235 far more readily) |
| control rods | boron, cadmium or hafnium | absorb surplus neutrons; pushed in to slow the reaction, pulled out to speed it |
| coolant | water, heavy water, liquid sodium or CO₂ | carry the heat to the steam generator |
| shielding | thick concrete and lead | stop the neutrons and gamma rays |

Note that the moderator and the control rods do opposite jobs: the moderator *slows*
neutrons (making them more effective), the control rods *remove* them.

### Fusion

**Fusion** is the joining of two light nuclei into one heavier nucleus. It is the reaction of
the Sun and of every star, and it powers the hydrogen bomb. The easiest reaction to ignite is
deuterium + tritium:

²₁H + ³₁H → ⁴₂He + ¹₀n + 17.6 MeV

and the Sun's main sequence burns hydrogen through the proton–proton chain, whose net result
is 4¹₁H → ⁴₂He + 2⁰₊₁e + energy (about 26.7 MeV). Fusion needs temperatures of the order of
10⁷–10⁸ K: the nuclei must be moving fast enough to come within about 10⁻¹⁵ m, against the
electrostatic repulsion of their protons.

### Why both release energy

The binding energy per nucleon rises steeply through the light elements, peaks at iron-56
(8.79 MeV per nucleon) and then falls slowly to about 7.6 MeV per nucleon at uranium. Moving
**towards** the peak releases energy, and it can be done from either side: splitting uranium
moves its nucleons to more tightly bound middle-mass nuclei (fission), and joining hydrogen
moves its nucleons to helium (fusion). Iron-56 sits at the bottom of the energy valley, so
neither fission nor fusion of iron releases energy.

```figure caption="Binding energy per nucleon against mass number. Energy is released by moving towards the peak at iron-56: heavy nuclei release it by fission, light nuclei by fusion. The curve is steep at the light end, which is why fusion gives so much energy per kilogram."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9, 3.0))
A = np.array([2, 4, 6, 9, 12, 16, 20, 24, 32, 40, 56, 84, 98, 120, 140, 170, 208, 235, 238])
B = np.array([1.11, 7.07, 5.33, 6.46, 7.68, 7.98, 8.03, 8.06, 8.49, 8.55, 8.79,
              8.71, 8.62, 8.50, 8.41, 8.23, 7.87, 7.59, 7.57])
ax.plot(A, B, color=ACCENT, lw=1.8)
ax.plot(A, B, 'o', ms=3.2, color=ACCENT)
ax.annotate('Fe-56\n8.79 MeV', xy=(56, 8.79), xytext=(66, 9.35), fontsize=8.4, color=INK,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
ax.annotate('', xy=(215, 7.75), xytext=(240, 8.45),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.4, mutation_scale=10))
ax.text(228, 8.62, 'fission', fontsize=8.6, color=SERIES[1], ha='center')
ax.annotate('', xy=(22, 7.4), xytext=(6, 5.6),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[0], lw=1.4, mutation_scale=10))
ax.text(12, 5.15, 'fusion', fontsize=8.6, color=SERIES[0], ha='center')
ax.set_xlabel('mass number $A$')
ax.set_ylabel('binding energy per nucleon (MeV)')
ax.set_xlim(0, 250); ax.set_ylim(0, 9.9)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=0.4)
```

| | Fission | Fusion |
|---|---|---|
| What happens | one heavy nucleus splits into two | two light nuclei join into one |
| Fuel | U-235, Pu-239 (scarce, mined) | deuterium and tritium (deuterium is abundant in sea water) |
| Trigger | a slow neutron | extremely high temperature (10⁷–10⁸ K) |
| Energy per event | about 200 MeV | about 17.6 MeV for D–T |
| Energy per kilogram of fuel | large | much larger (about four times fission, gram for gram) |
| Products | radioactive fission fragments, long-lived waste | helium, and a neutron; little long-lived waste |
| Status | commercial power stations since the 1950s | experimental (ITER); not yet a power source |
| Where it happens naturally | not on Earth naturally (reactors and bombs only) | in the Sun and stars |

::: caution Fission and fusion are not the same word with two spellings
**Fission** = splitting (think *scissors*), heavy nucleus, needs a neutron, works at room
temperature, produces radioactive waste. **Fusion** = joining (think *fuse*), light nuclei,
needs millions of kelvin, produces helium. An option that says "the Sun's energy comes from
fission" is a standard wrong key. Also: both release energy, but only fission is used in
today's power stations.
:::

## 12.6 Radioisotopes: how they are made and what they are used for

### How a radioisotope is made

1. **Neutron bombardment in a reactor.** The nucleus absorbs a neutron and becomes a heavier
   isotope of the same element, usually emitting a gamma ray. This is cheap and gives
   neutron-rich isotopes, which decay by beta emission:
   ⁵⁹₂₇Co + ¹₀n → ⁶⁰₂₇Co + γ; ³²₁₆S + ¹₀n → ³²₁₅P + ¹₁H (a (n,p) reaction).
2. **Charged-particle bombardment in a cyclotron.** Protons, deuterons or alpha particles are
   accelerated and fired at a target; the product is usually proton-rich and decays by
   positron emission or electron capture. This is how short-lived hospital isotopes are made
   on site: ¹⁸₈O + ¹₁H → ¹⁸₉F + ¹₀n gives fluorine-18 for PET scans, and the classic teaching
   example of the first artificial radioisotope is ²⁷₁₃Al + ⁴₂He → ³⁰₁₅P + ¹₀n.
3. **Separation from fission products.** A reactor's spent fuel contains a whole periodic
   table of isotopes; ⁹⁰Sr, ¹³¹I and ¹³⁷Cs are recovered from it.
4. **From a generator.** A long-lived parent is shipped to the hospital and its short-lived
   daughter is "milked" on the spot: ⁹⁹₄₂Mo (66 h) → ⁹⁹₄₃Tc* (6 h). This is the source of
   nearly all technetium-99m used in the world.

### The isotope–use pairs the paper tests

| Isotope | Half-life | Radiation | Main use |
|---|---|---|---|
| Tc-99m | 6 h | γ (140 keV) | imaging of bone, heart, kidney, thyroid, lungs — the workhorse of nuclear medicine |
| I-131 | 8.0 d | β⁻ and γ | thyroid imaging **and** treatment of hyperthyroidism and thyroid cancer |
| I-123 | 13 h | γ | thyroid imaging with a lower dose than I-131 |
| Co-60 | 5.27 y | β⁻ and γ (1.17, 1.33 MeV) | radiotherapy of cancer; sterilising syringes and surgical instruments; food irradiation; industrial radiography of welds |
| C-14 | 5730 y | β⁻ | radiocarbon dating; tracing carbon in photosynthesis |
| P-32 | 14.3 d | β⁻ | tracing DNA and RNA; fertiliser-uptake studies in plants; treatment of polycythaemia |
| Fe-59 | 44.5 d | β⁻ and γ | tracing iron in blood and the study of anaemia |
| Na-24 | 15 h | γ | detecting leaks in underground pipes; measuring blood flow |
| Am-241 | 432 y | α | household smoke detectors (ionises the air in the chamber) |
| Sr-90 | 28.8 y | β⁻ | thickness gauges; superficial radiotherapy of the eye |
| U-235 | 7.0 × 10⁸ y | α | reactor fuel; uranium–lead dating of rocks |
| K-40 | 1.25 × 10⁹ y | β⁻ and γ | potassium–argon dating of rocks |
| H-3 (tritium) | 12.3 y | β⁻ | tracer in water and in reaction mechanisms; luminous paint |

**Why Tc-99m dominates medicine.** It emits a single gamma ray of 140 keV — energetic enough
to leave the body, gentle enough to be imaged by a gamma camera; it has no beta emission, so
the patient's tissue dose is small; its 6-hour half-life is long enough to prepare and inject
but short enough to disappear in a day; and it can be attached to many different carrier
molecules that go to bone, heart muscle or kidney. A generator in the hospital supplies it
fresh each morning.

### Uses by field

- **Medicine.** Imaging (Tc-99m, I-123, F-18, Ga-67); therapy (I-131 for thyroid, Co-60 and
  linear accelerators for deep tumours, Sr-90 for the eye, Y-90 for liver tumours); sterilising
  heat-sensitive instruments and gloves with Co-60 gamma rays; radioimmunoassay of hormones.
- **Agriculture.** Tracing the uptake of phosphorus and nitrogen fertilisers (P-32, N-15);
  following the path of water and pesticides in soil; mutation breeding of new crop varieties
  (gamma irradiation of seeds); preserving onions and potatoes by stopping sprouting;
  sterilising male insects to control pests.
- **Industry.** Thickness gauges for paper, plastic and sheet metal (absorption of beta or
  gamma rays); level and density gauges; leak detection in buried pipelines (Na-24); testing
  welds and castings by gamma radiography (Co-60, Ir-192); smoke detectors (Am-241);
  tracing wear in engine parts; static elimination.
- **Archaeology and geology.** Carbon-14 for organic remains up to about 50,000 years;
  uranium–lead for the age of the Earth and of rocks; potassium–argon for volcanic rock;
  thermoluminescence for pottery (a different technique, not C-14).
- **Energy and research.** U-235 as fuel; tracers in reaction-mechanism studies (isotopic
  labelling with D, C-14, O-18).

::: caution Which isotope for which job
Learn the four the paper returns to: **Tc-99m — imaging; I-131 — thyroid; Co-60 —
radiotherapy and sterilisation; C-14 — dating.** Distractors usually swap them (Co-60 for
imaging, I-131 for dating). Also note that **I-131 treats as well as images**, because it
emits beta particles as well as gamma; Tc-99m only images, because it is a pure gamma
emitter.
:::

## 12.7 Radiocarbon dating

### Where the carbon-14 comes from

Cosmic rays knock neutrons out of atoms in the upper atmosphere, and those neutrons react with
nitrogen:

¹⁴₇N + ¹₀n → ¹⁴₆C + ¹₁H

The carbon-14 is oxidised to ¹⁴CO₂, mixes with ordinary ¹²CO₂, and enters plants by
photosynthesis and animals by eating. While an organism is alive its carbon is exchanged with
the atmosphere continuously, so the ratio ¹⁴C : ¹²C in its tissues stays at the atmospheric
value — about **1 : 10¹²**. When it dies, the exchange stops. The ¹⁴C already inside decays
with a half-life of **5730 years**, and the ¹²C stays put, so the ratio falls. Measure the
ratio (or the beta activity) and the time since death follows.

$$ t = \frac{t_{1/2}}{0.693}\,\ln\frac{A_0}{A} = \frac{t_{1/2}}{0.693}\,\ln\frac{N_0}{N} $$

$A_0$ is the activity of a living sample of the same material, $A$ the activity now, and
$t_{1/2} = 5730$ y. For a whole number of half-lives the logarithm is not needed: just count
the halvings.

::: example Carbon dating with a whole number of half-lives
**Problem.** A wooden beam from a temple gives a ¹⁴C activity that is 25 % of that of living
wood. Find its age ($t_{1/2} = 5730$ y).

**Solution.** $25\% = 1/4 = (1/2)^2$, so **2 half-lives** have passed:
$t = 2 \times 5730 =$ **11,460 years**.
:::

::: example Carbon dating with a fraction that is not a simple power
**Problem.** A bone sample has 35 % of the ¹⁴C activity of living bone. Find its age
($t_{1/2} = 5730$ y, $\ln(1/0.35) = 1.05$).

**Solution.** $t = (5730/0.693) \times 1.05 = 8268 \times 1.05 \approx$ **8,700 years**.
Always check the answer against the halving picture: 35 % lies between 50 % (5730 y) and 25 %
(11,460 y), so an answer near 8,700 y is reasonable, while 5,730 y or 17,190 y is not.
:::

### The assumption it rests on

The whole method assumes that **the proportion of ¹⁴C in the atmosphere — and therefore in
living tissue — has been constant** over the period being dated. That requires the cosmic-ray
flux to have been constant, the Earth's magnetic field (which shields us from cosmic rays) to
have been constant, and the amount of fossil carbon burnt (which dilutes ¹⁴C) to have been
negligible. Tree-ring and coral calibration curves correct for the small known variations.
The method also assumes that the sample has stayed a **closed system** — no carbon added or
lost after death (no contamination by modern carbon, no exchange with groundwater) — and that
the half-life is accurately known.

| Question | Answer |
|---|---|
| What is dated? | material that was once alive: wood, charcoal, bone, shell, peat, cloth, paper |
| What is measured? | the ¹⁴C activity (or the ¹⁴C : ¹²C ratio) left in it |
| Half-life used | 5730 years (the "Libby" value; the modern measured value is 5700 ± 30 y) |
| Useful range | about 100 to 50,000 years (after 9 half-lives too little is left) |
| Key assumption | the ¹⁴C : ¹²C ratio in living things has been constant |
| Cannot date | rocks, metals, pottery itself (only organic matter in or on it) |

::: caution Carbon dating dates the death of the organism
It does **not** date the age of the Earth, of a rock, or of a metal tool. A wooden handle on a
bronze axe gives the age of the tree, not of the metal. And a sample contaminated with a
little modern carbon — a fingerprint, mould, or museum glue — will read far too young, because
modern carbon has the full ¹⁴C level.
:::

## 12.8 Hazards and safe handling

### What radiation does to tissue

Ionising radiation removes electrons from molecules. In the body it ionises water, producing
free radicals (OH•, H•) that attack DNA. A cell whose DNA is badly damaged either dies or
reproduces with a mutation. The effects are grouped as:

- **Somatic** (in the exposed person): reddening and burns of the skin, nausea and radiation
  sickness at high dose, cataracts, and after a delay of years, leukaemia and other cancers.
- **Genetic** (in the person's children): mutations in the germ cells, which may cause birth
  defects. These have been shown in animals and are assumed in humans.
- **Deterministic** effects (burns, sickness) appear only above a threshold dose;
  **stochastic** effects (cancer) have no threshold — any dose adds a small probability.

The average person receives about 2–3 mSv a year from natural sources, of which the largest
single contributor is radon gas seeping from the ground into houses.

### The rules of safe handling

| Principle | What it means in practice |
|---|---|
| **Shielding** | keep sources in lead pots; use lead glass or concrete walls for gamma; perspex for beta (lead would produce X-rays by bremsstrahlung) |
| **Distance** | dose falls as $1/r^2$; use long tongs and never hold a source in the hand |
| **Time** | plan the work, then do it quickly; the dose is rate × time |
| **Containment** | work with open sources in a fume cupboard or glove box, on a tray with absorbent paper |
| **Monitoring** | film badge or TLD dosimeter for every worker; Geiger–Müller counter to check benches and hands |
| **Labelling and records** | trefoil sign, isotope, activity and date on every container; a log of receipts and disposals |
| **Disposal** | solid waste in shielded drums, liquid waste in approved sinks or drums, gaseous waste through filters; short-lived waste is left to decay |
| **Personal rules** | no eating, drinking or smoking in the lab; gloves; wash hands; pregnant staff avoid work with open sources |
| **Medical use** | the smallest activity that gives a diagnostic image; a pure gamma emitter such as Tc-99m; the isotope is chosen to leave the body quickly |

::: caution The alpha paradox, and the beta shielding trap
An alpha source in a sealed tube is almost harmless — a sheet of paper stops it. The same
isotope swallowed or inhaled is the most damaging of all, because all of its energy is
deposited in a few micrometres of living tissue. That is why radon, an alpha emitter, is a
serious indoor hazard, and why plutonium is dangerous mainly as dust. Conversely, **beta
sources should be shielded with perspex or aluminium, not lead**: the heavy lead nucleus
decelerates the electron and converts its energy into X-rays (bremsstrahlung), which are
harder to stop than the beta particles themselves.
:::

```photogrid label="12.2" cols="2" ratio="1.2" caption="Radiocarbon dating. (a) A Geiger counter detects the beta particles of carbon-14. (b) Living wood gives about 15.3 counts per minute per gram and the activity then halves every 5,730 years: A = A0 (1/2)^(t / 5730). A bone sample giving 7.2 counts per minute per gram has A / A0 = 0.471, so t = 5,730 log2(A0 / A) = 6,231 years. A sample at one quarter of the modern activity is 11,460 years old, and after 57,300 years, ten half-lives, less than 0.10 per cent is left, which limits the method to about 50,000 years."
@ photo id="ioephy/geiger" cap="A Geiger counter clicks once for each ionising particle detected"
fit 1.2
focus 0.5 0.5
@ svg cap="Carbon-14 activity against age of a sample"
A0 = 15.3; T = 5730
A = lambda t: A0 * 0.5 ** (t / T)
t = T * math.log2(A0 / 7.2); t4 = T * 2; t10 = T * 10
assert abs(t - 6231) < 3 and abs(7.2 / A0 - 0.4706) < 1e-3 and 0.5 ** 10 < 0.001
facts = dict(r="%.3f" % (7.2 / A0), t="{:,.0f}".format(t), t4="{:,.0f}".format(t4), t10="{:,.0f}".format(t10), p10="%.2f" % (0.5 ** 10 * 100))
f = Fig(300, 236)
f.text(150, 14, "activity (counts per min per g)", size=10.5, color=NAVY, bold=True)
X = lambda y: 40 + y / 17190 * 240; Y = lambda a: 150 - a * 6.6
f.line(X(0), Y(0), 285, Y(0), color=SLATE, sw=1.4); f.line(X(0), Y(0), X(0), 34, color=SOFT, sw=1.2)
pts = [(X(y), Y(A(y))) for y in range(0, 17191, 400)]
for (a, b), (c, d) in zip(pts, pts[1:]): f.line(a, b, c, d, color=NAVY, sw=2.6)
f.line(X(0), Y(7.2), X(t), Y(7.2), color=AMBER, sw=1.2, dash=True); f.line(X(t), Y(7.2), X(t), Y(0), color=AMBER, sw=1.2, dash=True)
f.circle(X(t), Y(7.2), 4, fill=AMBER, stroke=AMBER)
f.text(X(t) + 8, Y(7.2) - 8, "7.2 at %s y" % "{:,.0f}".format(t), size=10.5, color=AMBER, bold=True, anchor="start")
for y in (0, 5730, 11460, 17190): f.text(X(y), Y(0) + 13, "%d" % y, size=10, color=SLATE)
f.text(150, 188, "age in years", size=10.5, color=SLATE)
f.text(150, 206, "A / A0 = %.3f, t = %s y" % (7.2 / A0, "{:,.0f}".format(t)), size=10.5, color=NAVY, bold=True)
f.text(150, 224, "1/4 of modern: %s y" % "{:,.0f}".format(t4), size=10.5, color=NAVY, bold=True)
```

## Formula and fact sheet

| Topic | Fact |
|---|---|
| Conservation | ΣA and ΣZ balance always; mass itself does not (→ energy) |
| Displacement | α: 2 groups left (Z−2); β⁻: 1 group right (Z+1); β⁺/EC: Z−1; γ: none |
| Stability | belt N≈Z bending to n/p ≈ 1.5; magic 2, 8, 20, 28, 50, 82, 126; Z > 82 all radioactive |
| Transmutation | ${}^{14}N(\alpha,p){}^{17}O$ (Rutherford); ${}^{27}Al(\alpha,n){}^{30}P$ then β⁺ (Joliot-Curie) |
| Series | U-238 → Pb-206: 8 α + 6 β⁻; families 4n, 4n+2, 4n+3 |
| ¹⁴C clock | made by $n + {}^{14}N$; $t½ = 5730$ y; living ≈ 15 min⁻¹ g⁻¹; range to ~50 000 y |
| Tracers | same chemistry, detectable emissions: ³²P, ¹³¹I, ⁹⁹ᵐTc, ²⁴¹Am… |

## Chapter summary

- Write the two bookkeeping integers (A, Z) honestly and every nuclear equation,
  including series staircases of a dozen steps, falls into place.
- Stability is geography: inside the neutron-bending belt (magic addresses preferred)
  nuclei endure; outside, β-decays walk them home and the heavies shed α-particles.
- Bombardment extends the map: artificial transmutation and induced radioactivity brew
  the isotopes that medicine and industry now order by catalogue.
- Carbon-14 is the belt's most famous emigrant: made in the sky, eaten by everything
  alive, and read back as a 50 000-year clock.

## Practice questions

**Set A — Recall (20 questions)**

1. In a nuclear reaction, the quantities always conserved (summed on both sides) are
   (a) mass only (b) volume (c) number of molecules (d) A (mass number) and Z (charge)
2. Emission of an α-particle decreases the atomic number by
   (a) 2 (b) 1 (c) 4 (d) 0
3. β⁻ emission from a nucleus increases its atomic number by one because a
   (a) proton changes to a neutron (b) electron is captured (c) neutron changes into a proton (d) α is emitted too
4. The first artificial transmutation (Rutherford, 1919) was
   (a) U fission (b) ${}^{14}N + \alpha \rightarrow {}^{17}O + p$ (c) Al to P (d) H fusion in the lab first time claimed
5. Which set lists only magic numbers (for nucleons)?
   (a) 2, 8, 20, 28, 50, 82, 126 (b) 1, 3, 5, 7, 11 (c) 6, 12, 18, 24 (d) 10, 18, 36, 54 only
6. The heaviest element with any stable isotopes is
   (a) uranium (Z = 92) (b) gold Z=79 (c) bismuth Z=83 (now known slightly radioactive) (d) lead (Z = 82)
7. Radioactive dating of once-living matter uses the isotope
   (a) C-12 (b) C-14 (c) O-16 (d) N-14
8. The half-life of C-14 is about
   (a) 4.5 billion years (b) 14.3 days (c) 5730 years (d) 8 days
9. Carbon-14 is produced in the atmosphere by the action of cosmic-ray neutrons on
   (a) O-16 (b) N-14 (c) C-12 (d) H-1
10. A smoke detector commonly uses the radioisotope
    (a) ²⁴¹Am (b) ⁶⁰Co (c) ¹³¹I (d) ³²P
11. The isotope used to study phosphorus uptake (fertilizers) in plants is
    (a) ³¹P (b) ¹⁴C gas route (c) ³⁵S only always (d) ³²P
12. In the notation ${}^{A}Z$ style, a neutron is written
    (a) ${}^1_1n$ (b) ${}^0_1n$ (c) ${}^1_0n$ (d) ${}^0_{-1}n$
13. The end product of the natural uranium-238 decay series is a stable isotope of
    (a) lead (Pb-206) (b) radium (c) thorium (d) radon
14. Positron emission changes the atomic number of the nucleus by
    (a) +1 (b) −2 (c) −1 (d) no change and A down 1
15. Which nuclide is doubly magic (magic Z and magic N)?
    (a) Fe-56 (b) Pb-208 (c) U-238 (d) C-12
16. Induced (artificial) radioactivity was discovered by
    (a) Becquerel (b) Fermi first (for phosphorus) (c) Rutherford alone for Al→P (d) Irene and Frederic Joliot-Curie
17. The tracer principle works because a radioisotope of an element has (chemically)
    (a) different chemistry (b) no electrons (c) (practically) identical chemical behaviour (d) larger atoms always
18. Compared with light stable nuclei (n/p ≈ 1), heavy stable nuclei have n/p about
    (a) 0.5 (b) 1.5 (c) 1.0 (d) 3.0
19. Gamma emission from a nucleus changes
    (a) neither A nor Z (energy only) (b) Z only (c) A only (d) both
20. Spacecraft electrical power far from the Sun (RTGs) commonly uses
    (a) ⁶⁰Co mainly (b) ¹⁴C (c) ³H fusion cells consumer type (d) ²³⁸Pu

::: note Answers and explanations — Set A
**1.** (d) — nucleons (A) and charge (Z) balance; the measured mass shrinks by the binding-energy account (Physics §20.1).
**2.** (a) — the helium nucleus carries off 2 protons (and A by 4).
**3.** (c) — $n \rightarrow p + e^- + \bar\nu_e$: a new proton appears, the electron is the β⁻ particle.
**4.** (b) — nitrogen plus natural α-particles gave oxygen-17 and a proton: humanity's first deliberate element change.
**5.** (a) — the nuclear shell closures. (Noble-gas electron counts, option (d), are the chemical cousins, not magic numbers.)
**6.** (d) — lead, Z = 82 (itself a magic proton number); bismuth-209 (c) was found in 2003 to α-decay with a 10¹⁹-year half-life, so "stable" stops at Pb.
**7.** (b) — C-14, the radiocarbon clock.
**8.** (c) — 5730 years. (b) is P-32's, (d) is I-131's.)
**9.** (b) — ${}^{14}N(n,p){}^{14}C$ in the upper atmosphere.
**10.** (a) — americium-241 α-source ionizes the detector's air gap; smoke interrupts the ion current. (Kitchen physics of §12.2.)
**11.** (d) — ${}^{32}P$ (β⁻, 14.3 days) is traced from fertilizer to leaf with counters/autoradiography.
**12.** (c) — mass 1, charge 0.
**13.** (a) — Pb-206 after 8 α and 6 β⁻ steps (Example 12.1).
**14.** (c) — a proton became a neutron: Z − 1, A unchanged (electron capture does the same arithmetic).
**15.** (b) — Z = 82 and N = 126 are both magic — ${}^{208}Pb$ is the doubly-magic terminus of two decay series. (${}^4He$ and ${}^{16}O$ and ${}^{40}Ca$ are the smaller doubles.)
**16.** (d) — 1934: aluminium bombarded with α gave radioactive ${}^{30}P$ (Nobel 1935).
**17.** (c) — same electrons, same chemistry; only the nucleus reports in.
**18.** (b) — up to about 1.5–1.6 at lead/uranium: neutron dilution of proton repulsion.
**19.** (a) — the nucleus merely de-excites; identity unchanged (${}^{99m}Tc \rightarrow {}^{99}Tc$).
**20.** (d) — plutonium-238's α-decay heat, converted directly to electricity — Voyager still phones home on it after 45+ years.
:::

**Set B — Understanding (12 questions)**

1. An element X emits a β⁻ particle. In the periodic table the product is found
   (a) one group to the left of X (b) at the same place (c) one group to the right of X (d) two groups right
2. ${}^{14}C$ (n/p = 8/6 = 1.33) is radioactive while ${}^{12}C$ (1.00) is stable because for such a light nucleus the neutron excess puts it
   (a) below the belt (b) at a magic number (c) beyond Z=82 (d) above the belt of stability, so it β⁻-decays ($n\to p$)
3. Radiocarbon dating cannot be used for a 200-million-year-old fossil because
   (a) after ~10 half-lives (≈57 000 y) essentially no ¹⁴C remains to count (b) fossils contain no carbon (c) the fossil is too big (d) ¹⁴C was not formed then
4. A nucleus too rich in protons (below the belt) most likely decays by
   (a) β⁻ emission (b) positron emission or electron capture (c) α emission always (d) γ only
5. The end products of natural decay series are lead isotopes because lead (Z = 82, magic) nuclei are
   (a) the heaviest (b) artificial (c) gases escaping (d) exceptionally stable (further decay is energetically blocked)
6. ${}^{60}Co$ for radiotherapy units is manufactured by placing stable ${}^{59}Co$ in a reactor because neutron capture converts it by a
   (a) fission (b) (n,γ) reaction into radioactive Co-60 (c) (α,n) reaction with the steel (d) chemical oxidation
7. If a wooden sample's ¹⁴C activity is half that of living wood, it is approximately
   (a) 2865 years old (b) 11 460 years old (c) 5730 years old (d) undatable
8. Why does the neutron fraction required for stability grow with Z?
   (a) proton repulsion grows with Z; extra neutrons add binding, not repulsion (b) neutrons get heavier (c) electrons demand it (d) magic numbers shrink
9. In a decay series, an α-emission followed by two β⁻ emissions brings the nucleus to
   (a) the same nuclide (b) an isotope of the original element (same Z, A − 4) (c) an isobar of the original (d) a different element with higher Z overall
10. Tritium (³H) used in biological labelling emits only weak β⁻ (max 18.6 keV), which is an advantage for autoradiography resolution but requires care because tritium as water can
    (a) enter the body's water completely (internal exposure) (b) explode (c) stop all reactions (d) turn into gold
11. The K-40 in bananas and in our own bodies makes us faintly radioactive. K-40 ("primordial") still exists on Earth because its half-life is
    (a) minutes (b) 5730 years and replenished by rain (c) exactly infinite (d) about 1.25 billion years — comparable to the Earth's age
12. A Geiger counter over a sample reads steady counts, and the same sample next year reads almost the same. The isotope probably has a half-life that is
    (a) much shorter than a year (b) exactly one year always (c) much longer than a year (or is in secular equilibrium in a series) (d) zero

::: note Answers and explanations — Set B
**1.** (c) — Z rises by 1: one place to the right (Fajans–Soddy). Sodium's isotope β⁻-decays to magnesium, group 2.
**2.** (d) — light nuclei want N ≈ Z; ¹⁴C sheds the extra neutron as a β⁻ to become ${}^{14}N$ (7,7 — near-perfect balance).
**3.** (a) — the signal dies exponentially under background; long clocks (K–Ar, U–Pb) take over for geology.
**4.** (b) — $p \rightarrow n$ lowers Z towards the belt; which of β⁺/EC wins depends on the available energy (EC always allowed).
**5.** (d) — magic-Z lead sits at a local energy floor: the decay staircases (4n, 4n+2, 4n+3) terminate at Pb-208/206/207 (and Bi-209 in the extinct 4n+1).
**6.** (b) — induced radioactivity by neutron activation: ${}^{59}Co(n,\gamma){}^{60}Co$.
**7.** (c) — one half-life: 5730 years (after calibration refinements).
**8.** (a) — Coulomb repulsion is long-range (√ pair sums ∝ Z²) while strong attraction saturates with neighbours; extra neutrons add binding without adding repulsion.
**9.** (b) — α: Z−2, A−4; two β⁻: Z+2, A same — net same element, mass 4 less (as in Physics §20's U chain).
**10.** (a) — tritiated water mixes with body water (biological half-life ~10 days); low-energy β is harmless outside but must be kept from getting in (the α-particle lesson of §20.4 in reverse).
**11.** (d) — primordial survivors need t½ comparable to or greater than 4.5 Gyr (K-40 1.25 Gyr, U-238 4.5 Gyr, Th-232 14 Gyr).
**12.** (c) — a year's decay is negligible for a long t½ (or a daughter continually remade by a long-lived parent — secular equilibrium, as with radon from radium-bearing rock).
:::

**Set C — Application (10 questions)**

1. ${}^{238}_{92}U$ emits an α-particle. The daughter nuclide is
   (a) ${}^{234}_{92}U$ (b) ${}^{234}_{90}Th$ (c) ${}^{242}_{94}Pu$ (d) ${}^{238}_{90}Th$
2. Complete the reaction ${}^{27}_{13}Al + {}^{4}_{2}He \rightarrow {}^{30}_{15}P + X$. X is a
   (a) proton (b) electron (c) neutron (d) α-particle
3. A nuclide ${}^{A}_{Z}X$ undergoes 2 α-emissions and 1 β⁻-emission. The final atomic and mass numbers are
   (a) Z − 3, A − 8 (b) Z − 5, A − 8 (c) Z − 4, A − 9 (d) Z + 1, A − 8
4. Charcoal shows ¹⁴C activity of 1.875 decays min⁻¹ g⁻¹ against 15 for living wood. Its age is about
   (a) 5730 y (b) 11 460 y (c) 22 920 y (d) 17 190 y
5. The total number of α and β⁻ decays converting ${}^{232}_{90}Th$ to ${}^{208}_{82}Pb$ is
   (a) 6 α, 0 β (b) 8 α, 6 β (c) 6 α, 4 β (d) 4 α, 6 β
6. A radioactive isotope with t½ = 5 days starts at 320 MBq. After 20 days its activity is
   (a) 20 MBq (b) 40 MBq (c) 80 MBq (d) 10 MBq
7. In the reaction ${}^{9}_{4}Be + {}^{4}_{2}He \rightarrow {}^{12}_{6}C + X$ (Chadwick), X is
   (a) ${}^1_1H$ (b) γ only (c) ${}^0_{-1}e$ (d) ${}^1_0n$ (the discovered neutron)
8. If 1/16 of a sample remains after 60 days, the half-life is
   (a) 4 days (b) 15 days (c) 20 days (d) 30 days
9. ${}^{11}_6C$ is a positron emitter; its decay product is
   (a) ${}^{11}_5B$ (b) ${}^{11}_7N$ (c) ${}^{10}_5B$ (d) ${}^{12}_6C$
10. A rock contains equal numbers of ${}^{40}K$ atoms and its daughter ${}^{40}Ar$ atoms (formed only by K decay). Given t½(K-40) = 1.25×10⁹ y, the rock's age is about
    (a) 0.625×10⁹ y (b) 1.25×10⁹ y (c) 2.5×10⁹ y (d) 4.5×10⁹ y

::: note Answers and explanations — Set C
**1.** (b) — A−4, Z−2: ${}^{234}_{90}Th$.
**2.** (c) — A left over: 27+4−30 = 1 with Z = 0: a neutron.
**3.** (a) — A: −8; Z: −4 (two α) + 1 (β⁻) = −3.
**4.** (d) — 1.875/15 = 1/8: three half-lives = 17 190 years.
**5.** (c) — A drops 24 ⇒ **6 α**; Z then = 90 − 12 = 78, need 82 ⇒ **4 β⁻**. (The 4n series, vs the U-238 (b) pattern of the worked example.)
**6.** (a) — four half-lives: 320/16 = 20 MBq.
**7.** (d) — A: 13−12 = 1, Z: 6−6 = 0 — the neutron, whose discovery (1932) this reaction announced.
**8.** (b) — 1/16 = four halvings: 60/4 = 15 days.
**9.** (a) — β⁺: Z − 1 at constant A: ${}^{11}B$ (the C-11 of PET chemistry).
**10.** (b) — half the parent has become daughter: exactly one half-life (with the standard K–Ar caveats about argon loss, which geologists audit with step-heating).
:::

**Group D — Model answers for long questions (10 marks each, for deeper revision)**

1. Explain nuclear stability and the modes of radioactive decay, with the group displacement laws and a decay-series numerical. <span class="marks">[10]</span>
2. Describe nuclear fission, fusion and the applications of radioisotopes, with half-life numericals. <span class="marks">[10]</span>

### Model answer D1: nuclear stability and modes of decay (10 marks)

**Introduction.** The nucleus contains protons and neutrons (nucleons) held together by the strong nuclear force, which acts over about $10^{-15}\ \text{m}$ and overcomes the proton-proton repulsion. A nuclide is written ${}^A_ZX$.

**Nuclear stability.**

1. **Neutron-proton ratio.** For $Z < 20$ stable nuclei have $n/p \approx 1$. Heavier nuclei need more neutrons to dilute the repulsion, with $n/p$ up to about $1.5$. All nuclei with $Z > 83$ are unstable.
2. **Magic numbers.** Nuclei with $2, 8, 20, 28, 50, 82$ or $126$ protons or neutrons are unusually stable (${}^4\text{He}$, ${}^{16}\text{O}$, ${}^{40}\text{Ca}$, ${}^{208}\text{Pb}$).
3. **Even-odd rule.** Even-even nuclei are the most numerous and stable, odd-odd the least.
4. **Binding energy per nucleon** is maximum ($8.8\ \text{MeV}$) near ${}^{56}\text{Fe}$.

**Modes of decay.**

| Mode | Change | When it occurs | Example |
|---|---|---|---|
| $\alpha$ emission | $A - 4$, $Z - 2$ | heavy nuclei, $Z > 82$ | ${}^{238}\text{U} \to {}^{234}\text{Th} + {}^4\text{He}$ |
| $\beta^-$ emission | $Z + 1$, $A$ same | $n/p$ too high | ${}^{14}\text{C} \to {}^{14}\text{N} + e^- + \bar\nu$ |
| $\beta^+$ emission | $Z - 1$ | $n/p$ too low | ${}^{11}\text{C} \to {}^{11}\text{B} + e^+ + \nu$ |
| Electron capture | $Z - 1$ | $n/p$ too low | ${}^{7}\text{Be} + e^- \to {}^{7}\text{Li}$ |
| $\gamma$ emission | none | excited nucleus | ${}^{60}\text{Ni}^* \to {}^{60}\text{Ni}$ |

**Soddy-Fajans group displacement laws.** Emission of an $\alpha$ particle moves the element two places left in the periodic table, emission of a $\beta^-$ particle moves it one place right. A nucleus with $n/p$ above the stability belt emits $\beta^-$, and below it emits $\beta^+$ or captures an electron.

**Radioactive series.** The 4n (thorium), 4n+1 (neptunium), 4n+2 (uranium) and 4n+3 (actinium) series end in stable lead (or bismuth) isotopes.

**Numerical.** ${}^{238}_{92}\text{U}$ decays to ${}^{206}_{82}\text{Pb}$. The mass number change is $32$, so there are $32/4 = 8$ alpha particles. These reduce $Z$ by $16$, but the actual decrease is $10$, so $16 - 10 = 6$ beta particles are emitted. The decay series therefore has $8\alpha$ and $6\beta^-$ emissions.

**Conclusion.** Nuclei decay to reach a stable $n/p$ ratio, with $\alpha$ for heavy nuclei and $\beta$ or electron capture for those with a wrong $n/p$.

### Model answer D2: fission, fusion, half-life and applications (10 marks)

**Introduction.** In nuclear reactions the energy change is millions of times larger than in chemical reactions, from the mass defect through $E = \Delta mc^2$ ($1\ \text{u} = 931.5\ \text{MeV}$).

**Fission and fusion.**

| Feature | Fission | Fusion |
|---|---|---|
| Reaction | ${}^{235}\text{U} + n \to {}^{141}\text{Ba} + {}^{92}\text{Kr} + 3n + 200\ \text{MeV}$ | ${}^2\text{H} + {}^3\text{H} \to {}^4\text{He} + n + 17.6\ \text{MeV}$ |
| Chain reaction | yes, self-sustaining above critical mass | needs very high temperature |
| Control | control rods (Cd, B), moderator (heavy water, graphite) | magnetic confinement |
| Fuel and waste | enriched U, radioactive waste | hydrogen isotopes, little waste |
| Use | reactors, atom bomb | stars, hydrogen bomb |

**Half-life.** For decay $N = N_0e^{-\lambda t}$ and $t_{1/2} = 0.693/\lambda$. After $n$ half-lives $N = N_0/2^n$.

**Applications of radioisotopes.**

1. **Carbon-14 dating:** the age of wood, bone and fossils from the remaining ${}^{14}\text{C}$ ($t_{1/2} = 5730$ years).
2. **Uranium-lead dating** for rocks and the age of the earth.
3. **Medicine:** ${}^{131}\text{I}$ for the thyroid, ${}^{60}\text{Co}$ for cancer, ${}^{99m}\text{Tc}$ for imaging, ${}^{24}\text{Na}$ for blood circulation.
4. **Agriculture:** ${}^{32}\text{P}$ as a tracer for fertiliser uptake, and irradiation of food.
5. **Industry:** thickness gauges, leak detection and radiography.
6. **Chemistry:** isotopic tracers show reaction mechanisms, for example ${}^{18}\text{O}$ in ester hydrolysis.

**Numerical.** ${}^{131}\text{I}$ has $t_{1/2} = 8$ days. From $100\ \text{mg}$, after $32\ \text{days}$ (four half-lives) $100/16 = 6.25\ \text{mg}$ is left. A fossil with $12.5\%$ of the original ${}^{14}\text{C}$ is $3\times5730 = 17\,190$ years old. For ${}^{14}\text{C}$, $\lambda = \dfrac{0.693}{5730} = 1.21\times10^{-4}\ \text{y}^{-1}$.

**Conclusion.** Fission splits heavy nuclei and fusion joins light ones, both releasing energy through the mass defect, and radioisotopes have uses from dating to medicine.
