---
subject: Physics
grade: CEE
unit: 20
title: Nuclear Physics and Radioactivity
hours: 3
area: Modern Physics
---

Nuclear physics is the heaviest chapter of Modern Physics: the area carries **12 of
the 50 Physics questions**, and we estimate about **3** come from here — more than
any other modern topic. The paper asks for the size and density of a nucleus, a
mass defect or binding-energy calculation, the difference between fission and
fusion, the three radiations, and — above all — the half-life. The half-life
questions are the easiest marks in the chapter *if* you count in halves rather than
reach for the exponential, and the easiest to lose if you forget that a half-life
does not change with temperature, pressure or chemical combination.

::: key What the paper asks from this chapter
- $R = R_0A^{1/3}$ with $R_0 \approx 1.2$ fm, and why nuclear density is the same for every nucleus.
- Mass defect, $\Delta E = \Delta m\,c^2$, and the conversion 1 u = 931.5 MeV.
- The binding-energy-per-nucleon curve: peak at iron, fission of heavy nuclei, fusion of light nuclei.
- Fission and fusion, one example of each, and why each releases energy.
- Alpha, beta and gamma: charge, mass, penetration, ionising power, deflection in a field.
- $N = N_0e^{-\lambda t}$, $T_{1/2} = 0.693/\lambda$, $\tau = 1/\lambda$, activity $A = \lambda N$.
- Carbon dating as a half-life calculation.
- Medical uses (diagnosis vs therapy) and the hazards of ionising radiation.
:::

## 20.1 The nucleus: charge, size, mass and density; mass defect, binding energy and E = mc²

### What is inside the nucleus

A nucleus of element $X$ is written $^{A}_{Z}X$, where $Z$ is the **atomic number**
(the number of protons) and $A$ the **mass number** (protons + neutrons). The
**neutrons** number $N = A - Z$. Protons and neutrons together are **nucleons**.

| Property | Value or rule |
|---|---|
| Charge | $+Ze$; the electron cloud carries $-Ze$, so the atom is neutral |
| Radius | $R = R_0A^{1/3}$, $R_0 \approx 1.2$ fm ($1\ \text{fm} = 10^{-15}$ m) |
| Volume | $\frac{4}{3}\pi R^3 = \frac{4}{3}\pi R_0^3A \propto A$ |
| Density | $\rho = \dfrac{3m}{4\pi R_0^3} \approx 2.3\times10^{17}$ kg m⁻³ |
| Mass of proton | $1.007276$ u $= 938.3$ MeV/$c^2$ |
| Mass of neutron | $1.008665$ u $= 939.6$ MeV/$c^2$ |
| Mass of electron | $0.000549$ u $= 0.511$ MeV/$c^2$ |

The key point about the radius formula is the **cube root**. If $A$ becomes eight
times larger, the radius only doubles. So the volume is proportional to $A$, and
the density is the **same for every nucleus** — about $2.3\times10^{17}$ kg m⁻³,
some $10^{14}$ times the density of water. A teaspoon of nuclear matter would
weigh about a billion tonnes.

::: caution Radius, not diameter
The formula gives the **radius**. A question that asks for the diameter wants
$2R_0A^{1/3}$. And $R_0$ is about 1.2 fm; if a question gives 1.1 or 1.3 fm, use
the value given.
:::

::: example Worked example 20.1 — the size of a uranium nucleus
**Problem.** Find the radius and density of a $^{238}$U nucleus ($R_0 = 1.2$ fm).

**Solution.** $A^{1/3} = 238^{1/3} = 6.20$, so $R = 1.2\times6.20 = 7.4$ fm.
Density $\rho = \dfrac{3(1.66\times10^{-27})}{4\pi(1.2\times10^{-15})^3}
= 2.3\times10^{17}$ kg m⁻³. The same answer comes from any nucleus — that is the
point of $R \propto A^{1/3}$.
:::

### Mass defect and binding energy

A nucleus weighs **less** than the sum of its separate protons and neutrons. The
missing mass is the **mass defect**:

$$ \Delta m = \left[Zm_p + (A-Z)m_n\right] - M_{nucleus} $$

The missing mass has become **binding energy**, the energy that would be needed to
pull the nucleus apart:

$$ E_b = \Delta m\,c^2 $$

This is Einstein's mass–energy relation $E = mc^2$ applied to the nucleus: mass
and energy are two forms of the same thing, related by the square of the speed of
light. A mass of 1 u corresponds to

$$ 1\ \text{u} \times c^2 = 931.5\ \text{MeV} $$

so the practical rule is **energy in MeV = mass defect in u × 931.5**.

When atomic masses are used instead of nuclear masses, the electron masses cancel
if you use the mass of the **hydrogen atom** in place of the proton:

$$ \Delta m = Zm_H + (A-Z)m_n - M_{atom} $$

::: derivation Binding energy of a helium nucleus
**Setting up.** A $^4$He nucleus has 2 protons and 2 neutrons.
$m_H = 1.007825$ u, $m_n = 1.008665$ u, and the atomic mass of $^4$He is
$4.002603$ u.

**Step 1 — mass of the separate parts.**
$2(1.007825) + 2(1.008665) = 2.015650 + 2.017330 = 4.032980$ u.

**Step 2 — mass defect.**
$\Delta m = 4.032980 - 4.002603 = 0.030377$ u.

**Step 3 — convert to energy.**
$E_b = 0.030377 \times 931.5 = 28.3$ MeV.

**Step 4 — per nucleon.**
$28.3/4 = 7.07$ MeV per nucleon.

**What it means.** Each nucleon in helium is bound by about 7 MeV, which is why
helium is unusually stable for such a light nucleus.
:::

### The binding-energy-per-nucleon curve

Plot $E_b/A$ against $A$ and you get the most important graph in nuclear physics.

- It rises steeply for the lightest nuclei: deuterium 1.1, helium-4 7.07,
  carbon-12 7.68, oxygen-16 7.98 MeV per nucleon.
- It reaches a broad **maximum of about 8.8 MeV near iron-56** (and nickel-62 is
  marginally higher — the difference is small and not examinable).
- It then falls slowly for heavy nuclei: lead about 7.9, uranium-238 about 7.6.

```figure caption="Binding energy per nucleon against mass number. The peak near $A = 56$ is the most tightly bound region. Moving *up* the curve releases energy: fusion does this for light nuclei, fission for heavy ones."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,3.1))
A = np.array([2,3,4,6,9,12,16,20,40,56,84,120,160,200,238], float)
B = np.array([1.11,2.57,7.07,5.33,6.46,7.68,7.98,8.03,8.55,8.79,8.71,8.50,8.10,7.87,7.57])
grid = np.linspace(2,238,600)
ax.plot(grid, np.interp(grid, A, B), color=ACCENT, lw=2.0)
ax.plot(A, B, 'o', ms=3.4, color=ACCENT)
ax.annotate('Fe-56\n8.8 MeV', xy=(56,8.79), xytext=(86,8.20), fontsize=8.2, color=INK,
            ha='left', va='center',
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
ax.annotate('He-4', xy=(4,7.07), xytext=(24,6.20), fontsize=8.2, color=INK,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
ax.annotate('U-238\n7.6 MeV', xy=(238,7.57), xytext=(180,5.40), fontsize=8.2, color=INK,
            ha='center', va='center',
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
ax.annotate('', xy=(30,8.35), xytext=(10,7.30),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[2], lw=1.3, mutation_scale=9))
ax.text(20, 7.05, 'fusion', fontsize=8.2, color=SERIES[2], ha='center')
ax.annotate('', xy=(205,8.55), xytext=(235,7.75),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.3, mutation_scale=9))
ax.text(218, 8.85, 'fission', fontsize=8.2, color=SERIES[1], ha='center')
ax.set_xlabel('mass number  $A$'); ax.set_ylabel('binding energy per nucleon  (MeV)')
ax.set_xlim(0,250); ax.set_ylim(0,9.6)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.45)
```

**Why the curve matters.** A system tends towards the **lowest energy**, which
means the **highest binding energy per nucleon**. Any change that moves a nucleus
*up* the curve releases energy.

- **Fusion** of light nuclei (moving towards the peak) releases energy — the Sun
  runs this way.
- **Fission** of heavy nuclei (splitting into two mid-mass fragments nearer the
  peak) releases energy — reactors and bombs run this way.
- **Iron is the end of the road.** You cannot get energy by fusing iron into
  heavier nuclei, because that moves *down* the curve. This is why massive stars
  develop iron cores and then collapse.

::: caution Binding energy is not "energy stored in the nucleus"
A high binding energy means the nucleus is **hard to break apart**, so it is
stable. The energy is *released* when the nucleus forms, not stored for later use.
When students say "the nucleus contains 28 MeV of binding energy", they mean the
nucleus is bound by 28 MeV relative to its separated nucleons.
:::

## 20.2 Nuclear fission and fusion

### Fission

**Nuclear fission** is the splitting of a heavy nucleus into two medium-mass
nuclei, with the release of two or three neutrons and about 200 MeV of energy.

A typical reaction:
$$ ^{235}_{92}\text{U} + ^{1}_{0}\text{n} \rightarrow\ ^{141}_{56}\text{Ba}
+ ^{92}_{36}\text{Kr} + 3\,^{1}_{0}\text{n} + 200\ \text{MeV} $$

Check the bookkeeping: mass numbers $235 + 1 = 141 + 92 + 3 = 236$; charges
$92 = 56 + 36$. Both are conserved.

The energy appears because the fragments have **higher binding energy per nucleon**
(about 8.5 MeV) than uranium-238 (7.6 MeV). The mass lost is about 0.2 u per
fission, which is $0.2 \times 931.5 \approx 200$ MeV.

**Chain reaction.** Each fission releases 2–3 neutrons, which can trigger further
fissions. If on average more than one neutron succeeds, the reaction is
**self-sustaining**. The minimum mass needed to sustain it is the **critical mass**;
below it too many neutrons escape.

| Reactor part | Job | Material |
|---|---|---|
| Fuel | provides fissile nuclei | enriched uranium (U-235) |
| Moderator | slows neutrons so they are captured more easily | heavy water, graphite, ordinary water |
| Control rods | absorb neutrons and hold the rate steady | boron, cadmium |
| Coolant | carries heat to the turbine | water, CO₂ |
| Shield | absorbs radiation | thick concrete |

### Fusion

**Nuclear fusion** is the joining of light nuclei into a heavier one, with the
release of energy. It is the source of the Sun's energy.

$$ ^{2}_{1}\text{H} + ^{3}_{1}\text{H} \rightarrow\ ^{4}_{2}\text{He}
+ ^{1}_{0}\text{n} + 17.6\ \text{MeV} $$

In the Sun the **proton–proton chain** combines four protons into one helium
nucleus, with two positrons and two neutrinos:
$$ 4\,^{1}_{1}\text{H} \rightarrow\ ^{4}_{2}\text{He} + 2e^{+} + 2\nu
+ 26.7\ \text{MeV} $$

**Why fusion needs a very high temperature.** Both nuclei are positively charged,
so they repel each other. To get close enough for the short-range strong force to
act, they must approach at high speed — which means a temperature of the order of
$10^7$ K. This is the **Coulomb barrier**, and it is why fusion is hard to sustain
on Earth.

| | Fission | Fusion |
|---|---|---|
| What happens | heavy nucleus splits | light nuclei join |
| Fuel | uranium-235, plutonium-239 | deuterium, tritium |
| Energy per event | about 200 MeV | about 17.6 MeV (D–T) |
| Energy per nucleon | about 0.85 MeV | about 3.5 MeV |
| Needs | a critical mass and a neutron | extremely high temperature |
| Where | reactors, weapons | stars; experimental reactors |

::: caution Which way does the energy go?
Fission releases energy because the **fragments** are more tightly bound than the
parent. Fusion releases energy because the **product** is more tightly bound than
the reactants. Both are "moving up the curve". Fusing nuclei heavier than iron
*absorbs* energy instead.
:::

## 20.3 Radioactivity: alpha, beta and gamma rays; the decay law, half-life and mean life; carbon dating

### The three radiations

**Radioactivity** is the spontaneous emission of radiation from an unstable
nucleus. It was discovered by Becquerel in 1896 and studied by Marie and Pierre
Curie. It is a **nuclear** process: it does not depend on temperature, pressure or
chemical combination, because the energy involved is millions of times larger than
chemical energies.

| Property | Alpha ($\alpha$) | Beta ($\beta^-$) | Gamma ($\gamma$) |
|---|---|---|---|
| Nature | helium nucleus $^{4}_{2}$He | electron $e^-$ | photon |
| Charge | $+2e$ | $-e$ | 0 |
| Mass | 4 u | $\approx 1/1836$ u | 0 |
| Speed | $\sim 0.05c$ | up to $\sim 0.99c$ | $c$ |
| Ionising power | very strong | moderate | weak |
| Penetration | a few cm of air, stopped by paper | a few mm of aluminium | needs cm of lead or concrete |
| Deflection in an electric field | towards the negative plate | towards the positive plate | none |
| Effect on nucleus | $A$ falls by 4, $Z$ falls by 2 | $Z$ rises by 1 (for $\beta^-$) | no change |

```figure caption="The three radiations in an electric field. Alpha particles bend towards the negative plate, beta particles towards the positive plate (and bend much more, being lighter), and gamma rays pass straight through because they are uncharged."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9,3.0))
ax.add_patch(Rectangle((0.05,0.62),0.62,0.035, facecolor=SERIES[0], alpha=0.35, ec='none'))
ax.add_patch(Rectangle((0.05,0.22),0.62,0.035, facecolor=SERIES[1], alpha=0.35, ec='none'))
ax.text(0.36, 0.675, 'negative plate', ha='center', va='bottom', fontsize=8.0, color=INK)
ax.text(0.36, 0.205, 'positive plate', ha='center', va='top', fontsize=8.0, color=INK)
ax.plot([0.10,0.10],[0.30,0.58], color=INK, lw=2.4)
ax.text(0.085, 0.44, 'source', rotation=90, ha='right', va='center', fontsize=8.0)
t = np.linspace(0,1,120)
ax.plot(0.11+0.46*t, 0.44+0.17*t**2, color=SERIES[0], lw=1.8)
ax.text(0.60, 0.625, r'$\alpha$', fontsize=9.0, color=SERIES[0])
ax.plot(0.11+0.52*t, 0.44-0.20*t**1.5, color=SERIES[1], lw=1.8)
ax.text(0.65, 0.235, r'$\beta$', fontsize=9.0, color=SERIES[1])
ax.plot([0.11,0.74],[0.44,0.44], color=SERIES[2], lw=1.8)
ax.text(0.76, 0.44, r'$\gamma$', fontsize=9.0, color=SERIES[2], va='center')
ax.set_xlim(0,0.88); ax.set_ylim(0.12,0.80)
ax.axis('off')
```

**Alpha decay** reduces both $A$ and $Z$:
$$ ^{238}_{92}\text{U} \rightarrow\ ^{234}_{90}\text{Th} + ^{4}_{2}\text{He} $$

**Beta-minus decay** converts a neutron into a proton inside the nucleus:
$$ ^{14}_{6}\text{C} \rightarrow\ ^{14}_{7}\text{N} + e^- + \bar\nu_e $$
$A$ is unchanged and $Z$ rises by one. The emitted electron is **created at the
moment of decay** — it was not orbiting the nucleus.

**Beta-plus decay** converts a proton into a neutron, emitting a positron:
$$ ^{22}_{11}\text{Na} \rightarrow\ ^{22}_{10}\text{Ne} + e^+ + \nu_e $$

**Gamma emission** is a photon emitted when an excited daughter nucleus drops to a
lower energy state. It changes neither $A$ nor $Z$.

::: caution Where the beta electron comes from
Students often say "the nucleus contains electrons". It does not. In $\beta^-$
decay a neutron turns into a proton, an electron and an antineutrino:
$n \to p + e^- + \bar\nu_e$. The electron is born in the decay. The **continuous**
beta energy spectrum (the electron rarely gets the full available energy) was the
evidence that a second particle, the neutrino, carries the rest.
:::

### The decay law

Radioactive decay is **random**: we cannot say when a particular nucleus will
decay, only the probability per unit time, $\lambda$, the **decay constant**. For
$N$ nuclei,

$$ \frac{dN}{dt} = -\lambda N \quad\Longrightarrow\quad N = N_0e^{-\lambda t} $$

The **activity** $A$ is the number of decays per second:
$$ A = \lambda N = A_0e^{-\lambda t} $$
Its SI unit is the **becquerel** (Bq), one decay per second. The older unit, the
**curie** (Ci), is $3.7\times10^{10}$ Bq — roughly the activity of 1 g of radium-226.

### Half-life and mean life

The **half-life** $T_{1/2}$ is the time for half of the nuclei (or half the
activity) to decay. Putting $N = N_0/2$ in the decay law:

$$ \frac{1}{2} = e^{-\lambda T_{1/2}}
\quad\Longrightarrow\quad T_{1/2} = \frac{\ln 2}{\lambda} = \frac{0.693}{\lambda} $$

The **mean life** $\tau$ is the average lifetime of a nucleus:
$$ \tau = \frac{1}{\lambda} = \frac{T_{1/2}}{\ln 2} = 1.44\,T_{1/2} $$

After $n$ half-lives the fraction left is $(1/2)^n$:

| Half-lives elapsed | Fraction remaining | Fraction decayed |
|---|---|---|
| 0 | 1 | 0 |
| 1 | 1/2 | 1/2 |
| 2 | 1/4 | 3/4 |
| 3 | 1/8 | 7/8 |
| 4 | 1/16 | 15/16 |
| $n$ | $2^{-n}$ | $1 - 2^{-n}$ |

```figure caption="The decay curve. Each half-life halves the number of nuclei and the activity, so the curve never reaches zero in a finite time. After three half-lives, one eighth remains."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.9))
t = np.linspace(0,4.2,400)
ax.plot(t, 0.5**t, color=ACCENT, lw=2.0)
for n in range(1,5):
    ax.plot([n,n],[0,0.5**n], color=GRID, lw=0.9, ls='--')
    ax.plot([0,n],[0.5**n,0.5**n], color=GRID, lw=0.9, ls='--')
    ax.plot(n, 0.5**n, 'o', ms=4, color=ACCENT)
    ax.text(n+0.06, 0.5**n+0.02, f'{0.5**n:.3g}', fontsize=7.8, color=MUTED)
ax.set_xlabel('time  (in half-lives)'); ax.set_ylabel('$N/N_0$  and  $A/A_0$')
ax.set_xlim(0,4.3); ax.set_ylim(0,1.05)
ax.set_xticks([0,1,2,3,4]); ax.set_yticks([0,0.25,0.5,0.75,1.0])
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.35)
```

::: caution Half-life is a nuclear property
$T_{1/2}$ does **not** change with temperature, pressure, chemical state, or
whether the element is free or in a compound. Chemical reactions involve electron
energies of a few eV; nuclear decay involves MeV. Heating a radium salt does not
make it decay faster.
:::

::: example Worked example 20.2 — counting in halves
**Problem.** A sample has an activity of 6400 Bq and a half-life of 5 days. What
is its activity after 20 days?

**Solution.** $20/5 = 4$ half-lives. Activity $= 6400/2^4 = 6400/16 = 400$ Bq.
No logarithms needed — count the halvings.
:::

::: example Worked example 20.3 — from activity to half-life
**Problem.** A source contains $4.0\times10^{15}$ nuclei and has an activity of
$2.0\times10^{8}$ Bq. Find the decay constant and the half-life.

**Solution.** $\lambda = A/N = 2.0\times10^8/4.0\times10^{15} = 5.0\times10^{-8}$ s⁻¹.
$T_{1/2} = 0.693/\lambda = 1.4\times10^7$ s $\approx 160$ days.
:::

### Carbon dating

Carbon-14 is produced in the upper atmosphere when cosmic-ray neutrons strike
nitrogen-14:
$$ ^{14}_{7}\text{N} + ^{1}_{0}\text{n} \rightarrow\ ^{14}_{6}\text{C} + ^{1}_{1}\text{H} $$
Living things take in carbon continuously, so the ratio of $^{14}$C to $^{12}$C in
their tissue stays at the atmospheric value (about 1 part in $10^{12}$). When the
organism dies, intake stops and the $^{14}$C decays with a half-life of **5730
years**. Measuring the remaining activity gives the time since death.

::: example Worked example 20.4 — dating a bone
**Problem.** A bone sample has 25 % of the $^{14}$C activity of living tissue.
How old is it? ($T_{1/2} = 5730$ yr)

**Solution.** $25\% = 1/4 = (1/2)^2$, so two half-lives have passed:
$t = 2\times5730 = 11{,}460$ years.
:::

The method works up to about 50,000 years (about nine half-lives), beyond which
the remaining activity is too small to measure reliably. It also assumes the
atmospheric $^{14}$C ratio has stayed constant; calibration with tree rings and
other methods corrects for the small variations.

### Parent–daughter chains

A radioactive nucleus usually decays into another radioactive nucleus, and so on,
until a stable one is reached. These are the **decay series**:

| Series | Parent | Stable end | Half-life of parent |
|---|---|---|---|
| Uranium | $^{238}$U | $^{206}$Pb | $4.5\times10^9$ yr |
| Thorium | $^{232}$Th | $^{208}$Pb | $1.4\times10^{10}$ yr |
| Actinium | $^{235}$U | $^{207}$Pb | $7.0\times10^8$ yr |

If the parent has $N_0$ nuclei at $t = 0$ and the daughter is stable, the number
of daughter nuclei at time $t$ is the number that have decayed:
$$ N_d = N_0\left(1 - e^{-\lambda t}\right) $$
At $t = T_{1/2}$ half the parent has become daughter; as $t \to \infty$ all of it
does. In a long chain the slowest step controls the overall rate, and after enough
time the whole chain reaches **secular equilibrium**, in which every member decays
at the same activity.

```photogrid label="20.2" cols="2" ratio="1.2" caption="Half-life decides how an isotope is used. (a) A survey Geiger counter with its probe: the count rate falls with the activity of the source, A = A0 (1/2)^(t / T). (b) Technetium-99m, the workhorse of diagnostic imaging, has a half-life of 6.01 hours, so after 24 hours only 6.3 per cent is left and the patient's dose is small. Iodine-131, used for thyroid treatment, has a half-life of 8.02 days: 91.7 per cent remains after a day and 84.1 per cent after two, so it irradiates the thyroid for weeks. Cobalt-60 (5.27 years) loses only 1.1 per cent in 30 days, which suits a radiotherapy source that is replaced every few years. A short half-life gives less dose; a long half-life gives a steady source."
@ photo id="ceephy2/geiger" cap="A survey Geiger counter with its probe"
fit 1.2
focus 0.5 0.5
@ svg cap="Activity left over 48 hours for Tc-99m and I-131"
T_tc, T_i, T_co = 6.01, 8.02 * 24, 5.27 * 365.25 * 24
rem = lambda t, T: 100 * 0.5 ** (t / T)
assert round(rem(24, T_tc), 1) == 6.3 and round(rem(24, T_i), 1) == 91.7 and round(rem(48, T_i), 1) == 84.1
assert round(100 - rem(30 * 24, T_co), 1) == 1.1
f = Fig(300, 236)
f.text(150, 12, "Percentage of activity left", size=10.5, color=NAVY, bold=True)
ax = Axes(f, 44, 28, 234, 150, (0, 48), (0, 100))
ax.grid(12, 25, xfmt=lambda x: "%dh" % x).axes("t", "%")
ax.curve(lambda t: rem(t, T_i), 0, 48, color=TEAL)
ax.curve(lambda t: rem(t, T_tc), 0, 48, color=RED)
ax.pt(24, rem(24, T_tc), "Tc-99m: 6.3%", dx=8, dy=-8)
ax.pt(24, rem(24, T_i), "I-131: 91.7%", dx=8, dy=-8, color=TEAL)
f.text(150, 206, "Tc-99m (6.01 h): 6.3 per cent left at 24 h", size=10.5, color=NAVY, bold=True)
f.text(150, 222, "I-131 (8.02 d): 91.7 per cent left at 24 h", size=10.5, color=SLATE, bold=True)
```

## 20.4 Medical uses of nuclear radiation and its health hazards

### Diagnosis

Diagnosis uses **small** doses to *see* inside the body. The radiation must be
penetrating enough to escape and be detected outside.

| Technique | Radiation | What it shows |
|---|---|---|
| X-ray radiograph | X-rays | bones, lungs, dental work |
| CT scan | X-rays from many angles | cross-sectional images |
| Bone scan | $^{99m}$Tc (γ, $T_{1/2}$ 6 h) | bone tumours, fractures |
| PET scan | $^{18}$F in glucose (β⁺, $T_{1/2}$ 110 min) | metabolic activity, cancer |
| Thyroid scan | $^{131}$I (γ and β) | thyroid function |

A **tracer** should be a gamma emitter with a short half-life: gamma rays escape
the body, and a short half-life keeps the dose low. Alpha emitters are a poor
choice for tracers because alpha particles are stopped inside the body and deposit
all their energy in a small volume.

### Therapy

Therapy uses **large** doses to *destroy* tissue — usually a tumour.

- **External radiotherapy:** a beam of gamma rays from cobalt-60 is aimed at the
  tumour from several directions, so the tumour receives a high dose while each
  patch of healthy skin receives less.
- **Brachytherapy:** a sealed source is placed inside or next to the tumour.
- **Targeted therapy:** radioactive iodine-131 is taken up by thyroid cells, so it
  irradiates the thyroid from inside — useful for hyperthyroidism and thyroid
  cancer.

The difference between diagnosis and therapy is **dose and intent**: the same
isotope can do both, but at very different activities.

### Hazards

Ionising radiation damages cells by breaking chemical bonds, especially in DNA.

| Effect | When | Examples |
|---|---|---|
| Somatic (in the exposed person) | soon after a large dose | skin burns, nausea, hair loss, radiation sickness |
| Long-term somatic | years later | leukaemia, thyroid and lung cancer, cataracts |
| Genetic | in the next generation | mutations in germ cells |

**Dose units.** The **gray** (Gy) is the absorbed energy per unit mass
(1 Gy = 1 J kg⁻¹). The **sievert** (Sv) is the *equivalent* dose, which allows
for the fact that alpha particles do more biological damage per joule than gamma
rays. Natural background radiation gives about 2–3 mSv per year.

**Protection.** Three rules:

1. **Time** — spend as little time near the source as possible.
2. **Distance** — dose falls as $1/r^2$, so doubling the distance quarters it.
3. **Shielding** — lead for gamma, plastic or paper for beta, and never alpha
   emitters inside the body.

Workers wear **film badges** or electronic dosimeters, and hospitals follow the
**ALARA** principle: doses as low as reasonably achievable.

::: caution The danger is not "radioactivity" in general
A smoke detector contains a tiny americium-241 source and is safe because the
alpha particles cannot escape the casing. A diagnostic tracer is safe because the
activity is small and the half-life short. The hazard comes from **dose**, not from
the mere presence of a radioactive atom.
:::

```photogrid label="20.1" cols="2" ratio="1.2" caption="Alpha decay and half-life. (a) Each straight track is a helium nucleus slowing down in supersaturated vapour, all about the same length. (b) For Ra-226 to Rn-222 + He-4 the mass loss gives Q = 4.87 MeV; momentum conservation gives the alpha 4.78 MeV and the recoiling radon only 0.09 MeV. Geiger's rule R = 0.318 E^1.5 cm predicts about 3.3 cm in air, matching the short tracks. With T = 1,600 y, N / N0 = (1/2)^(t / T): 95.8 per cent remains after 100 y and 25 per cent after 3,200 y."
@ photo id="ceephy/cloud" cap="Straight, thick alpha tracks from a radium source in a cloud chamber"
fit 1.2
focus 0.5 0.5
@ svg cap="Decay of radium-226 against time"
u = 931.494; mRa, mRn, mHe = 226.0254098, 222.0175782, 4.0026033
Q = (mRa - mRn - mHe) * u; Ka = Q * 222 / 226; Kr = Q - Ka; rng = 0.318 * Ka ** 1.5
frac = lambda t: 0.5 ** (t / 1600)
assert abs(Q - 4.87) < 0.01 and abs(Ka - 4.784) < 0.01 and abs(rng - 3.33) < 0.02 and abs(frac(3200) - 0.25) < 1e-12
facts = dict(q="%.2f" % Q, ka="%.2f" % Ka, kr="%.2f" % Kr, rng="%.1f" % rng, f100="%.1f" % (frac(100) * 100), f3200="%.0f" % (frac(3200) * 100))
f = Fig(300, 244)
f.text(150, 14, "N / N0 = (1/2)^(t / 1600 y)", size=10.5, color=NAVY, bold=True)
X = lambda t: 40 + t / 4800 * 240; Y = lambda v: 150 - v * 105
f.line(X(0), Y(0), 285, Y(0), color=SLATE, sw=1.4); f.line(X(0), Y(0), X(0), 34, color=SOFT, sw=1.2)
pts = [(X(t), Y(frac(t))) for t in range(0, 4801, 100)]
for (a, b), (c, d) in zip(pts, pts[1:]): f.line(a, b, c, d, color=NAVY, sw=2.6)
for t, v in ((1600, 0.5), (3200, 0.25)):
    f.line(X(t), Y(0), X(t), Y(v), color=AMBER, sw=1.2, dash=True); f.line(X(0), Y(v), X(t), Y(v), color=AMBER, sw=1.2, dash=True)
    f.circle(X(t), Y(v), 4, fill=AMBER, stroke=AMBER)
    f.text(X(t) + 8, Y(v) - 8, "%g" % v, size=10.5, color=AMBER, bold=True, anchor="start")
for t in (0, 1600, 3200, 4800): f.text(X(t), Y(0) + 13, "%d" % t, size=10.5, color=SLATE)
f.text(150, 178, "years", size=10.5, color=SLATE)
f.text(150, 196, "Q = %.2f MeV: alpha %.2f, Rn %.2f MeV" % (Q, Ka, Kr), size=10.5, color=NAVY, bold=True)
f.text(150, 214, "air range about %.1f cm (Geiger)" % rng, size=10.5, color=NAVY, bold=True)
f.text(150, 230, "%.1f per cent left after 100 years" % (frac(100) * 100), size=10.5, color=NAVY, bold=True)
```

## Formula and fact sheet

| Quantity | Formula or value |
|---|---|
| Nuclear radius | $R = R_0A^{1/3}$, $R_0 \approx 1.2$ fm |
| Nuclear density | $\rho \approx 2.3\times10^{17}$ kg m⁻³, independent of $A$ |
| Mass defect | $\Delta m = Zm_H + (A-Z)m_n - M_{atom}$ |
| Binding energy | $E_b = \Delta m\,c^2$; 1 u = 931.5 MeV |
| BE per nucleon | maximum 8.8 MeV near Fe-56 |
| Fission | $^{235}$U + n → Ba + Kr + 3n + 200 MeV |
| Fusion | $^{2}$H + $^{3}$H → $^{4}$He + n + 17.6 MeV |
| Sun's chain | 4 $^{1}$H → $^{4}$He + 2e⁺ + 2ν + 26.7 MeV |
| Alpha decay | $A \to A-4$, $Z \to Z-2$ |
| Beta-minus | $A$ same, $Z \to Z+1$; $n \to p + e^- + \bar\nu$ |
| Beta-plus | $A$ same, $Z \to Z-1$; $p \to n + e^+ + \nu$ |
| Gamma | $A$ and $Z$ unchanged |
| Decay law | $N = N_0e^{-\lambda t}$; $A = \lambda N$ |
| Half-life | $T_{1/2} = 0.693/\lambda$ |
| Mean life | $\tau = 1/\lambda = 1.44\,T_{1/2}$ |
| After $n$ half-lives | $N = N_0/2^n$ |
| Activity unit | 1 Bq = 1 decay s⁻¹; 1 Ci = $3.7\times10^{10}$ Bq |
| Carbon-14 | $T_{1/2} = 5730$ yr; useful to ~50,000 yr |
| Dose | 1 Gy = 1 J kg⁻¹; equivalent dose in Sv |
| Background | about 2–3 mSv per year |

## Chapter summary

- The nucleus has $Z$ protons and $A-Z$ neutrons; $R = R_0A^{1/3}$, so volume
  $\propto A$ and density is the same for all nuclei ($2.3\times10^{17}$ kg m⁻³).
- A nucleus is lighter than its parts by $\Delta m$; the missing mass is the
  binding energy, $E_b = \Delta m c^2$, with 1 u = 931.5 MeV.
- Binding energy per nucleon peaks near iron-56 at 8.8 MeV. Fusion of light nuclei
  and fission of heavy nuclei both move nuclei up this curve and release energy.
- Fission: a heavy nucleus splits into two mid-mass fragments plus neutrons,
  releasing about 200 MeV; a chain reaction needs a critical mass.
- Fusion: light nuclei join, releasing energy; it needs about $10^7$ K to overcome
  the Coulomb barrier, and powers the Sun.
- Alpha is a helium nucleus ($A-4$, $Z-2$), beta is an electron or positron
  ($Z\pm1$), gamma is a photon (no change). Alpha ionises most and penetrates
  least; gamma is the reverse.
- $N = N_0e^{-\lambda t}$, $T_{1/2} = 0.693/\lambda$, $\tau = 1/\lambda$; after
  $n$ half-lives a fraction $2^{-n}$ remains. Half-life is unaffected by
  temperature or chemical state.
- Activity $A = \lambda N$, measured in becquerels; 1 Ci = $3.7\times10^{10}$ Bq.
- Carbon dating uses the 5730-year half-life of carbon-14; 25 % activity means two
  half-lives, about 11,460 years.
- Diagnosis uses small doses of gamma emitters; therapy uses large doses to kill
  cells. Hazards are somatic and genetic; protection is time, distance and
  shielding.

## Practice questions

**Set A — Recall (25 questions)**

1. The radius of a nucleus of mass number A is proportional to
   (a) A (b) $A^2$ (c) $A^{2/3}$ (d) $A^{1/3}$
2. One atomic mass unit (1 u) is equivalent in energy to
   (a) 931.5 MeV (b) 13.6 eV (c) 1 MeV (d) 0.511 MeV
3. The binding energy of a nucleus equals the
   (a) mass of the nucleus (b) total KE of nucleons (c) mass defect × c² (d) energy of electrons
4. The binding energy per nucleon is maximum for nuclei near
   (a) helium (b) iron (A ≈ 56) (c) uranium (d) hydrogen
5. In alpha decay, the daughter nucleus has, compared with the parent,
   (a) Z − 2, A − 4 (b) Z + 2, A + 4 (c) Z − 1, same A (d) the same Z and A
6. In beta-minus decay, the atomic number
   (a) decreases by 1 (b) decreases by 2 (c) is unchanged in value but A falls (d) increases by 1
7. The decay law for radioactive nuclei is
   (a) $N = N_0 e^{\lambda t}$ (b) $N = N_0 e^{-\lambda t}$ (c) $N = N_0/(1+\lambda t)$ (d) $N = N_0 - \lambda t$
8. Half-life is related to the decay constant by
   (a) $T_{1/2} = \lambda/0.693$ (b) $T_{1/2} = 1/\lambda$ exactly (c) $T_{1/2} = 0.693/\lambda$ (d) $T_{1/2} = 0.693\lambda$
9. The mean life of a radioactive nucleus equals
   (a) $T_{1/2}$ (b) $1.44\,T_{1/2}$ (c) $0.693\,T_{1/2}$ (d) $2\,T_{1/2}$
10. The unit of activity (SI) is the
    (a) becquerel (b) curie (c) gray (d) sievert
11. Carbon dating uses the isotope
    (a) C-12 (b) C-13 (c) C-11 (d) C-14 (half-life 5730 yr)
12. In a nuclear reactor, the moderator serves to
    (a) absorb neutrons (b) cool the fuel only (c) slow down neutrons (d) start fusion
13. The energy released per fission of U-235 is about
    (a) 200 MeV (b) 200 eV (c) 17.6 MeV (d) 2 MeV
14. The Sun's energy comes mainly from
    (a) fission (b) chemical burning (c) fusion of hydrogen into helium (d) gravitational collapse only at present
15. Gamma rays are
    (a) electrons (b) electromagnetic photons of nuclear origin (c) helium nuclei (d) protons
16. The radiation stopped by a sheet of paper is
    (a) gamma (b) beta (c) X-rays (d) alpha
17. Absorbed dose is measured in
    (a) becquerels (b) curies (c) gray (1 Gy = 1 J kg⁻¹) (d) Tesla
18. The isotope most used as a medical tracer (pure gamma, ~6 h half-life) is
    (a) Co-60 (b) Tc-99m (c) U-235 (d) Ra-226
19. The continuous energy spectrum of beta particles is explained by the simultaneous emission of a
    (a) (anti)neutrino sharing the energy (b) second electron (c) photon (d) proton
20. Which particle starts the fission of U-235?
    (a) proton (b) alpha (c) electron (d) (slow) neutron
21. Isotopes of an element have the same number of
    (a) neutrons (b) protons (c) nucleons (d) electrons in ions always
22. The density of nuclear matter (across all nuclei) is approximately
    (a) proportional to A (b) that of steel (c) proportional to Z (d) constant (~$10^{17}$ kg m⁻³)
23. In PET scanning, the detected 511 keV photons come from
    (a) nuclear fission (b) X-ray tubes (c) annihilation of a positron with an electron (d) bremsstrahlung only
24. The half-life of a radioactive isotope can be changed by
    (a) none of these (it is a nuclear constant) (b) pressure (c) chemical combination (d) heating
25. Control rods in a reactor are made of materials such as boron or cadmium because they
    (a) reflect neutrons (b) slow neutrons (c) absorb neutrons strongly (d) produce neutrons

::: note Answers and explanations — Set A
**1.** (d) — $R = R_0A^{1/3}$: volume ∝ A at constant density.
**2.** (a) — $1\ \mathrm{u} \times c^2 = 931.5$ MeV; (d) 0.511 MeV is the electron's rest energy.
**3.** (c) — the vanished mass is the binding energy, $E = \Delta m c^2$.
**4.** (b) — ≈ 8.8 MeV per nucleon near Fe-56/Ni-62.
**5.** (a) — the α carries away 2 protons and 2 neutrons.
**6.** (d) — a neutron becomes a proton: $Z + 1$, $A$ unchanged.
**7.** (b) — exponential decay: each nucleus has the same decay probability per second, λ.
**8.** (c) — $T_{1/2} = \ln 2/\lambda$.
**9.** (b) — $\tau = 1/\lambda = T_{1/2}/0.693 = 1.44\,T_{1/2}$.
**10.** (a) — 1 Bq = 1 decay per second; the curie ($3.7\times10^{10}$ Bq) is the older unit.
**11.** (d) — C-14, replenished by cosmic rays in life, decaying after death.
**12.** (c) — slow (thermal) neutrons fission U-235 best; rods (b-option confusion) absorb.
**13.** (a) — about 200 MeV, mostly the fragments' KE.
**14.** (c) — the proton–proton chain fusing H into He at $1.5\times10^7$ K in the core.
**15.** (b) — high-energy photons emitted by de-exciting nuclei.
**16.** (d) — α, massive and doubly charged, spends itself within ~40 μm of tissue or a paper sheet.
**17.** (c) — gray is absorbed dose; sievert is weighted dose (risk).
**18.** (b) — Tc-99m: 140 keV γ, 6 h half-life, versatile chemistry — the workhorse of nuclear medicine.
**19.** (a) — the antineutrino (in β⁻) takes a variable share (Pauli's prophecy, confirmed 1956).
**20.** (d) — a thermal neutron tips U-235 into fission; the 2–3 emitted neutrons sustain the chain.
**21.** (b) — same Z, different N: same element, (nearly) same chemistry.
**22.** (d) — radius ∝ $A^{1/3}$ ⇒ constant nuclear density, $\sim 10^{17}$ kg m⁻³.
**23.** (c) — $e^+e^- \to 2\gamma$, each 511 keV, back-to-back: PET's coincidence signature.
**24.** (a) — λ is fixed by the nucleus; ordinary physical/chemical means do not touch it.
**25.** (c) — boron-10 and cadmium greedily capture neutrons, throttling the chain.
:::

**Set B — Understanding (15 questions)**

1. Fusing two light nuclei or splitting a heavy one both release energy because both processes move the products
   (a) to lower BE per nucleon (b) to the same A (c) to higher BE per nucleon (towards iron) (d) apart magnetically
2. If a nucleus's actual mass were greater than the sum of its nucleons' masses, the nucleus would
   (a) be extra stable (b) emit unlimited energy (c) emit gamma only (d) be unbound — it could not exist as a bound system
3. Alpha particles are dangerous mainly when the source is inside the body, because externally they
   (a) cannot pass the dead outer skin (but ionize densely where they stop) (b) are too fast (c) become gamma (d) decay instantly
4. A sample shows one-eighth of its original activity after 15 days. Its half-life is
   (a) 15 days (b) 5 days (c) 3 days (d) 45 days
5. In beta-minus decay the emitted electron comes from
   (a) the electron cloud (b) the nucleus's stored electrons (there are none resident) (c) another atom (d) inside the nucleus, where a neutron changes into a proton
6. Why does a reactor need a minimum (critical) mass of fuel?
   (a) to be heavy enough (b) neutrons must cause fission faster than they escape or are absorbed (c) to slow neutrons (d) to shield radiation
7. Two samples have the same number of radioactive atoms; one has twice the half-life of the other. Its initial activity is
   (a) twice (b) the same (c) half ($A = \lambda N$, longer life = smaller λ) (d) four times
8. Tc-99m (half-life 6 h) is preferred over a long-lived gamma emitter for a scan mainly because
   (a) the patient’s radiation dose ends quickly (and its γ suits the camera) (b) it is cheaper (c) it has no gamma (d) it is stable
9. Gamma emission usually follows alpha or beta decay because the daughter nucleus is left
   (a) with missing electrons (b) in an excited energy state, which then de-excites (c) negatively charged (d) with too many neutrons only
10. Fusion on earth is harder to achieve than fission chiefly because the fusing nuclei must
    (a) overcome their mutual electrostatic repulsion (needing ~$10^8$ K) (b) be radioactive (c) find electrons (d) lose neutrons first
11. The BE-per-nucleon curve is fairly flat between A = 30 and A = 170. This tells us the nuclear force
    (a) acts between all pairs equally over any distance (b) weakens with Z only (c) is electromagnetic (d) saturates — each nucleon binds only its near neighbours
12. In carbon dating, the clock starts when the organism dies because only then does it stop
    (a) absorbing neutrons (b) decaying C-12 (c) absorbing C-14 (exchanging carbon with the environment) (d) being irradiated by the Sun at all
13. Standing twice as far from a small gamma source reduces the dose rate to
    (a) one quarter (inverse-square law) (b) one half (c) one eighth (d) zero
14. A nucleus ${}^{238}_{92}U$ emits an alpha and then two beta-minus particles (in some order with gammas). The final nucleus has
    (a) Z = 90, A = 234 (b) Z = 94, A = 234 (c) Z = 88, A = 230 (d) Z = 92, A = 234 (an isotope of uranium)
15. After ten half-lives, a radioactive sample is considered nearly safe/decayed away because the fraction remaining is about
    (a) 10 % (b) 0.1 % ($1/2^{10} \approx 1/1024$) (c) 1 % (d) 50 %

::: note Answers and explanations — Set B
**1.** (c) — products sit higher on the BE/$A$ curve; the gain in binding is paid out as energy.
**2.** (d) — positive "binding energy" would mean it falls apart for free: bound systems must mass *less* than their parts.
**3.** (a) — α's range is tens of μm in tissue: paper/dead skin stops them outside, but inhaled radon daughters deposit that dense ionization in lung tissue (weighting factor 20).
**4.** (b) — 1/8 = three halvings in 15 days: $T_{1/2} = 5$ days.
**5.** (d) — $n \to p + e^- + \bar\nu_e$ creates the electron at the moment of decay; nuclei contain no electrons (d's caveat). Electron-cloud electrons (a) are unaffected apart from the changed $Z$.
**6.** (b) — criticality is neutron bookkeeping: production must at least balance escape + absorption, which needs enough fuel volume per surface.
**7.** (c) — slower decayer, fewer decays per second from the same stock.
**8.** (a) — in a day it is ~94 % gone: good pictures, minimal residual dose.
**9.** (b) — decay often lands the daughter on an upper rung of its own ladder; γ is the step down. $^{99m}$Tc's "m" is exactly such a metastable rung.
**10.** (a) — two positive nuclei must be thrown together hard enough for the strong force (range ~fm) to grab: hence thermonuclear temperatures.
**11.** (d) — if every nucleon bound every other, BE would grow with the number of pairs (~$A^2$) and BE/$A$ would keep rising with $A$; saturation (near-neighbour-only) flattens it, letting Coulomb's $Z^2$ drag win at large $A$.
**12.** (c) — while alive, intake replenishes C-14 as fast as it decays; death stops the exchange.
**13.** (a) — point source: intensity $\propto 1/r^2$ — the cheapest shielding is distance.
**14.** (d) — α: (90, 234); each β⁻: Z + 1 keeping A → (92, 234): back to uranium, a lighter isotope. (This is why decay chains meander.)
**15.** (b) — $(1/2)^{10} = 1/1024 \approx 0.1\%$: the ten-half-life rule of hospital waste stores.
:::

**Set C — Application (10 questions)**

1. The mass defect of the helium-4 nucleus is 0.0304 u. Its binding energy is about
   (a) 2.83 MeV (b) 28.3 MeV (c) 283 MeV (d) 7.1 MeV
2. A radioactive sample has a half-life of 5 days. The fraction remaining after 20 days is
   (a) 1/4 (b) 1/8 (c) 1/16 (d) 1/32
3. The decay constant of an isotope with half-life 3.8 days (radon-222) is about
   (a) 0.18 day⁻¹ (b) 5.5 day⁻¹ (c) 0.26 day⁻¹ (d) 3.8 day⁻¹
4. A sample contains $10^{20}$ nuclei with decay constant $10^{-6}$ s⁻¹. Its activity is
   (a) $10^{6}$ Bq (b) $10^{26}$ Bq (c) $10^{10}$ Bq (d) $10^{14}$ Bq
5. A wooden artifact shows C-14 activity equal to 1/16 of that of living wood. Its age is about
   (a) 5730 years (b) 11 460 years (c) 22 920 years (d) 45 840 years
6. Fission of one U-235 nucleus releases 200 MeV. The energy from complete fission of 1 g of U-235 ($\approx 2.56\times10^{21}$ nuclei) is about
   (a) $8.2\times10^{10}$ J (b) $8.2\times10^{7}$ J (c) $8.2\times10^{13}$ J (d) 200 J
7. A nucleus has binding energy 492 MeV and mass number 56 (Fe). The BE per nucleon is about
   (a) 4.9 MeV (b) 7.6 MeV (c) 28 MeV (d) 8.8 MeV
8. The activity of a source falls from 800 MBq to 100 MBq in 24 days. Its half-life is
   (a) 3 days (b) 8 days (c) 6 days (d) 12 days
9. A nucleus of mass number 27 has a radius of about ($R_0 = 1.2$ fm)
   (a) 3.6 fm (b) 1.2 fm (c) 10.8 fm (d) 32 fm
10. How much mass disappears when 931.5 MeV of energy is released in a nuclear reaction?
    (a) 1 kg (b) 1 u (c) 500 u (d) 0.001 u

::: note Answers and explanations — Set C
**1.** (b) — $0.0304 \times 931.5 = 28.3$ MeV in total; (d) 7.1 MeV is per nucleon — read which is asked.
**2.** (c) — 20 days = 4 half-lives: $(1/2)^4 = 1/16$.
**3.** (a) — $\lambda = 0.693/3.8 = 0.18$ day⁻¹.
**4.** (d) — $A = \lambda N = 10^{-6}\times10^{20} = 10^{14}$ Bq.
**5.** (c) — four halvings: $4\times5730 = 22\,920$ years.
**6.** (a) — $2.56\times10^{21}\times200\times1.6\times10^{-13}\ \mathrm{J} = 8.2\times10^{10}$ J (about a day's output of a megawatt — from a gram). (c) is the per-kg value.
**7.** (d) — $492/56 = 8.8$ MeV — the curve's summit.
**8.** (b) — 800 → 100 is three halvings (800, 400, 200, 100) in 24 days: 8 days each (I-131's, as it happens).
**9.** (a) — $R = 1.2\times27^{1/3} = 1.2\times3 = 3.6$ fm.
**10.** (b) — by definition of the conversion: 1 u of mass ↔ 931.5 MeV.
:::

**Group D — Model answers for long questions (10 marks each, for deeper revision)**

1. State the law of radioactive decay and derive the relation between half-life, mean life and decay constant. Explain the types of radiation and solve numericals. <span class="marks">[10]</span>
2. Define mass defect and binding energy, and explain nuclear fission and fusion with numericals. <span class="marks">[10]</span>

```photogrid label="20.H" cols="2" ratio="1.4" caption="Detecting radiation. (a) A Geiger-Muller counter clicks for each ionising particle that enters its tube. (b) The same counter, in a laboratory set-up, is used to measure the activity of a source and to find the half-life."
@ photo id="ceephy2/geiger" cap="(a) Geiger-Muller counter"
fit 1.4
focus 0.5 0.5
@ photo id="ioephy/geiger" cap="(b) Counter in the laboratory"
fit 1.4
focus 0.5 0.5
```

### Model answer D1: radioactive decay (10 marks)

**Introduction.** **Radioactivity** is the spontaneous emission of radiation from unstable nuclei (Becquerel, 1896). It is a random, statistical process unaffected by temperature, pressure or chemical state.

**Radiations.**

| Property | Alpha | Beta | Gamma |
|---|---|---|---|
| Nature | helium nucleus ${}^4_2\text{He}$ | electron (or positron) | photon |
| Charge | $+2e$ | $-e$ | 0 |
| Penetration | paper stops it | few mm of aluminium | thick lead |
| Ionising power | highest | medium | lowest |
| Effect on the nucleus | $A$ decreases by 4, $Z$ by 2 | $Z$ changes by 1, $A$ same | no change in $A$, $Z$ |

**Law of decay.** The rate of decay is proportional to the number of undecayed nuclei: $\dfrac{dN}{dt} = -\lambda N$, so $N = N_0e^{-\lambda t}$, where $\lambda$ is the **decay constant**.

1. **Half-life** $T_{1/2}$: time for half the nuclei to decay, $T_{1/2} = \dfrac{\ln2}{\lambda} = \dfrac{0.693}{\lambda}$.
2. **Mean life** $\tau = \dfrac1\lambda = 1.44\,T_{1/2}$.
3. **Activity** $A = \lambda N = A_0e^{-\lambda t}$, in becquerel ($1\ \text{Bq} = 1\ \text{decay per second}$; $1\ \text{Ci} = 3.7\times10^{10}\ \text{Bq}$).
4. After $n$ half-lives, $N = N_0/2^n$.

**Uses.** Carbon dating, medical tracers and cancer therapy (cobalt-60), sterilisation of food, smoke detectors and thickness gauges.

**Numerical.** A sample of $64\ \text{g}$ with $T_{1/2} = 8$ days leaves $64/2^3 = 8\ \text{g}$ after $24$ days. In carbon dating, a wooden relic that has $25\%$ of the original ${}^{14}\text{C}$ is $2\times5730 = 11\,460$ years old. For $T_{1/2} = 5\ \text{days}$, $\lambda = 0.693/5 = 0.139\ \text{day}^{-1}$ and the mean life is $7.2$ days.

**Conclusion.** Decay is exponential. After each half-life the activity halves, whatever the starting amount.

### Model answer D2: binding energy, fission and fusion (10 marks)

**Introduction.** The mass of a nucleus is less than the sum of the masses of its nucleons. This difference is the **mass defect** $\Delta m = Zm_p + (A - Z)m_n - M$. By Einstein's relation $E = mc^2$, the **binding energy** is $E_b = \Delta m\times931.5\ \text{MeV}$ (for $\Delta m$ in u).

**Binding energy curve.** $E_b/A$ rises steeply to about $8.8\ \text{MeV}$ at ${}^{56}\text{Fe}$ (the most stable) and then falls slowly to $7.6\ \text{MeV}$ for uranium. Light nuclei can release energy by **fusion**, and heavy nuclei by **fission**.

| Feature | Fission | Fusion |
|---|---|---|
| Process | heavy nucleus splits | light nuclei join |
| Example | ${}^{235}\text{U} + n \to {}^{141}\text{Ba} + {}^{92}\text{Kr} + 3n$ | $\text{D} + \text{T} \to {}^4\text{He} + n$ |
| Energy per reaction | about $200\ \text{MeV}$ | $17.6\ \text{MeV}$ |
| Energy per kilogram | high | even higher |
| Conditions | slow neutrons | $10^7$ to $10^8\ \text{K}$ |
| Use | reactors, bombs | the sun, hydrogen bomb |
| Waste | radioactive | little |

**Nuclear reactor.** The fuel is enriched uranium, the **moderator** (heavy water or graphite) slows neutrons, **control rods** (cadmium, boron) absorb neutrons to keep the multiplication factor $k = 1$, and the coolant removes heat. In a bomb, $k > 1$ and the chain reaction is uncontrolled.

**Numerical.** For ${}^4_2\text{He}$: $\Delta m = 2(1.007825) + 2(1.008665) - 4.002603 = 0.029377\ \text{u}$, so $E_b = 0.029377\times931.5 = 27.4\ \text{MeV}$ and $E_b/A = 6.84\ \text{MeV}$ per nucleon. Fission of $1\ \text{kg}$ of ${}^{235}\text{U}$ involves $\dfrac{1000}{235}\times6.02\times10^{23} = 2.56\times10^{24}$ nuclei, giving $2.56\times10^{24}\times200\ \text{MeV} = 8.2\times10^{13}\ \text{J}$, which equals about $2.3\times10^{7}\ \text{kWh}$.

**Conclusion.** Energy is released when nuclei move toward the peak of the binding energy curve, by fission for heavy nuclei and by fusion for light ones.
