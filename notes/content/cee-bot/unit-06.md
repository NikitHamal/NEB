---
subject: Botany
grade: CEE
unit: 6
title: Ecology and Vegetation
hours: 4
area: Ecology and Vegetation
---

Ecology and Vegetation carries **4 of the 40 Botany questions**, spread evenly over four
blocks: ecosystem structure and biotic interactions, the carbon and nitrogen cycles with
their named bacteria, Nepal's forest belts and invasive plants, and succession. Almost
nothing here needs calculation; almost everything needs **a name attached to the right
process**. Learn the tables and the two cycle figures and this unit is free marks.

::: key What the paper asks from this chapter
- **Trophic structure** — producer, consumer, decomposer; grazing and detrital chains; the 10 % law (Lindeman) and why the pyramid of energy is never inverted.
- **Biotic interactions** — the six named relationships with their signs (+ +, + 0, + −, − −, 0 −) and a Nepali example for each.
- **Nitrogen cycle names** — *Rhizobium*, *Azotobacter*, *Clostridium*, *Anabaena* (fixation); *Nitrosomonas* (NH₄⁺ → NO₂⁻); *Nitrobacter* (NO₂⁻ → NO₃⁻); *Pseudomonas* and *Clostridium* (denitrification).
- **Carbon cycle** — the four fluxes and the reservoirs in order of size.
- **Pollution** — greenhouse gases and the mechanism, acid rain (pH 5.6), CFC → Cl → ozone, and Nepal's climate exposure.
- **Forest belts of Nepal** — species against altitude, from sal below 1 000 m to cushion plants above 4 000 m.
- **Invasive plants** — *Lantana*, *Mikania*, water hyacinth and *Parthenium*, and why each is a problem.
- **Succession** — the hydrosere and xerosere sequences in order, pioneer and climax, and the trends in biomass and diversity.
:::

## 6.1 Pond and forest ecosystems: structure and function

### What an ecosystem is

An **ecosystem** is a self-regulating unit in which a community of organisms interacts
with its physical environment, **energy flowing through it one way** and **matter
cycling within it** (Tansley, 1935). Its **abiotic** half is light, temperature, water,
air, soil, pH and the inorganic nutrients; its **biotic** half is **producers**
(autotrophs), **consumers** (heterotrophs) and **decomposers** (saprotrophs — bacteria
and fungi, with earthworms and termites as detritivores). *Structure* is who is there
and in what layers; *function* is productivity, decomposition, energy flow and nutrient
cycling.

### Structure of a pond ecosystem

A pond is a small **freshwater standing (lentic)** ecosystem. Its abiotic part is the
water itself — temperature, dissolved O₂ and CO₂, pH, light penetration, nitrates and
phosphates. Its biotic part is arranged in four zones:

| Zone | Position | Producers | Consumers |
|---|---|---|---|
| **Littoral** | shallow margin, light reaches the bottom | emergent *Typha*, *Phragmites*; floating *Nymphaea*, *Pistia* | snails, insects, tadpoles, small fish |
| **Limnetic** | open water, well lit | **phytoplankton** — *Chlorella*, *Scenedesmus*, diatoms | **zooplankton** — *Daphnia*, *Cyclops*, *Rotifera*; fish |
| **Profundal** | deep water, little light | none | fish and large crustaceans on falling detritus |
| **Benthic** | bottom mud | none | bacteria and fungi (decomposers), chironomid larvae, mussels |

Submerged plants (*Hydrilla*, *Vallisneria*) root in the littoral mud and reach into the
limnetic zone. The decomposers sit in the mud and take everything that sinks, so a pond
recycles its nutrients fast — a nutrient spill can choke it with algae within days.

### Structure of a forest ecosystem

A forest is **terrestrial**, and its structure is vertical. A sal forest in Chitwan has
five layers:

| Layer | What is there |
|---|---|
| **Canopy** | *Shorea robusta* (sal), 25–35 m, closing overhead |
| **Understorey** | *Syzygium cumini*, *Semecarpus anacardium*, *Bauhinia* |
| **Shrub** | *Lantana*, *Clerodendrum*, saplings of the canopy trees |
| **Herb** | fodder grasses, ferns, a dense monsoon ground flora |
| **Litter and root** | fallen leaves, and the soil fungi, bacteria, termites and earthworms |

Consumers are layered too: deer and insects below, monkeys and birds in the canopy,
tiger and leopard through all of them; the decomposers work in the litter.

### Function: energy flow and the 10 % law

**Photosynthesis** is the only route by which new energy enters an ecosystem. The total
fixed by the producers is the **gross primary productivity (GPP)**; what is left after
they pay for their own respiration is the **net primary productivity (NPP)**:

$$\text{NPP} = \text{GPP} - R$$

Energy passes along a **food chain**, and at every transfer most of it is lost as
**heat** in respiration, plus what is not eaten, not digested or excreted. Raymond
**Lindeman (1942)** measured this and stated the **10 % law**: only about **10 % of the
energy of one trophic level reaches the next**, the other 90 % being lost, mostly as heat.

```figure caption="Energy flow up the trophic levels of a grassland. Only about 10 % of the energy passes up at each step; the rest is lost as heat in respiration, and none flows back down."
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.7, 3.5))
levels = [
    ("Sunlight", "1 000 000 kJ", 0.74, "#C9A227"),
    ("Producers (grass)", "10 000 kJ", 0.56, "#3F7D3A"),
    ("Primary consumers (grasshopper)", "1 000 kJ", 0.38, "#C97B2E"),
    ("Secondary consumers (frog, snake)", "100 kJ", 0.20, "#B5482F"),
    ("Tertiary consumers (hawk)", "10 kJ", 0.02, "#7B2D26"),
]
for name, val, y, col in levels:
    ax.add_patch(plt.Rectangle((0.06, y), 0.78, 0.13, facecolor=col, edgecolor="none", alpha=0.93))
    ax.text(0.09, y + 0.065, name, ha="left", va="center", color="white", fontsize=7.4)
    ax.text(0.81, y + 0.065, val, ha="right", va="center", color="white", fontsize=7.4, fontweight="bold")
for i in range(4):
    y0 = levels[i][2]
    ax.annotate("", xy=(0.45, y0 - 0.005), xytext=(0.45, y0 - 0.045),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2, mutation_scale=8))
    ax.text(0.48, y0 - 0.025, "10 %", ha="left", va="center", fontsize=7.0, color=INK)
ax.text(0.06, -0.06, "the other 90 % leaves each level as heat", fontsize=7.0, color=MUTED, ha="left")
ax.set_xlim(0, 1); ax.set_ylim(-0.10, 0.90)
ax.axis("off")
```

Two consequences follow. **Energy flow is unidirectional** — once degraded to heat it is
useless to a producer, whereas matter cycles. And **food chains are short**, because
only a tenth survives each transfer.

**Types of food chain.** A **grazing (predator) chain** starts from a living plant:
grass → grasshopper → frog → snake → hawk. A **detrital (decomposer) chain** starts from
dead organic matter: leaf litter → earthworm → bird. In a forest most energy travels
through the detrital chain. Real chains interlock into a **food web**, which is what
makes an ecosystem stable — if one prey disappears, a predator can switch to another.

::: example Problem. In a grassland the producers fix 50 000 kJ m⁻² yr⁻¹. Apply the 10 % law and find the energy reaching the third trophic level.
**Solution.** Producers = level 1 = 50 000 kJ. Primary consumers (level 2) receive
10 % = 5 000 kJ. Secondary consumers (level 3) receive 10 % of that = **500 kJ m⁻²
yr⁻¹**. Each step is one multiplication by 0.1, so from level 1 to level $n$ the
energy is $50\,000 \times 0.1^{\,n-1}$. Working backwards, multiply by 10 for each
step down the chain.
:::

### Ecological pyramids

An **ecological pyramid** plots the numbers, biomass or energy at each trophic level,
producers at the base.

| Type | What is plotted | Unit | Shape | Inverted when |
|---|---|---|---|---|
| **Pyramid of numbers** | number of individuals per level | count | usually upright | a single large tree supports thousands of insects; many small parasites on one host |
| **Pyramid of biomass** | mass of living matter per level | g m⁻² or kg ha⁻¹ | usually upright | **in a pond**, where the standing crop of phytoplankton is smaller than that of the zooplankton feeding on it |
| **Pyramid of energy** | energy passing a level per unit time | kJ m⁻² yr⁻¹ | **always upright** | never |

::: caution The two traps in pyramids
1. **A pyramid of biomass can be inverted; a pyramid of energy cannot.** Phytoplankton
   are eaten as fast as they divide, so a small standing crop supports a larger mass of
   zooplankton. Energy is still lost at every transfer, so the energy pyramid stays
   upright. "Inverted energy pyramid" is a favourite distractor.
2. **Decomposers are not a trophic level of the standard pyramid.** They draw energy
   from *every* level — leaves, dung, corpses — so they cannot be stacked above the
   carnivores; they form a separate **detritus pathway**. Where do they belong? "At
   every level", not "the top".
:::

### Biotic interactions

The relationship between two species is classified by its **effect on each partner**:
**+** benefited, **−** harmed, **0** unaffected.

| Interaction | Signs | What happens | Nepali example |
|---|---|---|---|
| **Mutualism** | + + | both benefit; often obligate | **lichen** — alga feeds the fungus, fungus gives shelter and minerals (Phulchoki rocks); ***Rhizobium*** in lentil (masuro) and chickpea nodules fixes N₂ for sugar |
| **Commensalism** | + 0 | one benefits, the other unaffected | **cattle egret** (*Bubulcus ibis*) follows buffalo in the Terai and catches the insects they flush; **epiphytic orchids** (*Vanda*) on sal branches |
| **Parasitism** | + − | one lives on or in the other and draws food from it | ***Cuscuta*** (amarbel) sends haustoria into host stems; ***Scurrula*** (liwang) on mango; liver fluke in sheep and goats |
| **Predation** | + − | one animal kills and eats another | **tiger** on chital in Chitwan; leopard on livestock; ladybird on aphids in mustard |
| **Competition** | − − | both need the same limited resource | **sal and *Terminalia*** seedlings for light and water; **Mikania** against fodder grasses |
| **Amensalism** | 0 − | one harmed, the other unaffected | ***Penicillium*** releases penicillin and kills bacteria around it; a large tree shading out herbs below |

::: memory Six interactions, six signs
**M**utualism **+ +**, **C**ommensalism **+ 0**, **P**arasitism **+ −**,
**P**redation **+ −**, **C**ompetition **− −**, **A**mensalism **0 −**.
A parasite lives **on or in** its host and usually does not kill it at once; a predator
**kills** its prey.
:::

```photogrid label="6.1" cols="2" ratio="1.2" caption="Energy runs out up a food chain. (a) A pond community: algae and submerged plants are the producers, and every animal depends on them. (b) Only about one tenth of the energy of one level reaches the next (the 10 per cent law); the rest is lost as heat in respiration or stays in dead matter. Starting from 10,000 kJ per square metre per year in the producers, the levels carry 1,000, 100 and 10 kJ, so a top carnivore gets only 0.1 per cent of what the plants fixed and needs about 1,000 kg of plant matter for each kilogram of its own growth. This is why food chains rarely have more than four or five links."
@ photo id="ceebot/pond" cap="A pond community: water, algae and plants"
fit 1.2
focus 0.5 0.5
@ svg cap="Energy at each trophic level (kJ per sq m per year)"
levels = (("Producers (algae, plants)", 10000), ("Primary consumers (snails)", 1000), ("Secondary (small fish)", 100), ("Tertiary (large fish)", 10))
for (a, x), (b, y) in zip(levels, levels[1:]):
    assert abs(y / x - 0.1) < 1e-12
top = 100 * levels[-1][1] / levels[0][1]
facts = dict(top="%.1f" % top, ratio="{:,}".format(levels[0][1] // levels[-1][1]))
f = Fig(300, 236)
f.text(150, 12, "10 per cent law (bar length = log10)", size=10.5, color=NAVY, bold=True)
cols = ((TEAL, MINT), (TEAL, "#d1fae5"), (AMBER, SAND), (RED, ROSE))
for i, ((lab, e), (c, fl)) in enumerate(zip(levels, cols)):
    y = 30 + i * 44
    w = 52 * math.log10(e) - 10
    f.box(150 - w / 2, y + 12, w, 22, fill=fl, stroke=c, r=2)
    f.text(150, y + 23, "{:,} kJ".format(e), size=10.5, color=c, bold=True, vmid=True)
    f.text(150, y + 6, lab, size=10.5, color=SLATE)
f.text(150, 214, "90 per cent is lost at each step as heat", size=10.5, color=NAVY, bold=True)
```

## 6.2 Carbon and nitrogen cycles; greenhouse effect, acid rain, ozone depletion and climate change

### The carbon cycle

Carbon is exchanged between four reservoirs: the **atmosphere** (as CO₂, about
900 Gt C), **living organisms and soil** (about 2 000 Gt C), the **oceans** (about
38 000 Gt C of dissolved inorganic carbon) and **fossil fuels**. Carbonate rock holds far more, but exchanges only over millions of years.

- **Photosynthesis** removes CO₂ and fixes it into carbohydrate — the only large biological *sink*.
- **Respiration** by plants, animals and microbes returns CO₂ to the air.
- **Decomposition** of litter and humus is, globally, the largest single return flux.
- **Feeding** moves carbon from plants to animals as organic matter.
- **Combustion** of fossil fuel and firewood returns carbon locked away for millions of years.
- **Ocean exchange** — the sea absorbs roughly a quarter of the CO₂ humans release.

```figure caption="The carbon cycle. Photosynthesis is the only large biological sink; respiration and decomposition are the return fluxes; burning fossil fuel adds carbon that had been out of the cycle for millions of years."
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0, 3.3))
def box(x, y, w, h, text, col, fs=7.4):
    ax.add_patch(plt.Rectangle((x, y), w, h, facecolor=col, edgecolor="none", alpha=0.93))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", color="white", fontsize=fs, linespacing=1.25)
box(0.06, 0.74, 0.26, 0.14, "Atmosphere\nCO₂ ≈ 900 Gt C", "#4C5B6B")
box(0.68, 0.74, 0.26, 0.14, "Producers\n(green plants)", "#3F7D3A")
box(0.68, 0.36, 0.26, 0.14, "Consumers\n(animals)", "#B5482F")
box(0.06, 0.36, 0.26, 0.14, "Decomposers\n(soil microbes)", "#7A5C3E")
ax.annotate("", xy=(0.675, 0.805), xytext=(0.325, 0.805),
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.3, mutation_scale=9))
ax.text(0.50, 0.822, "photosynthesis", ha="center", va="bottom", fontsize=7.2, color=INK)
ax.plot([0.81, 0.81, 0.19], [0.88, 0.94, 0.94], color="#A8271F", lw=1.3)
ax.annotate("", xy=(0.19, 0.88), xytext=(0.19, 0.94),
            arrowprops=dict(arrowstyle="-|>", color="#A8271F", lw=1.3, mutation_scale=9))
ax.text(0.50, 0.952, "respiration", ha="center", va="bottom", fontsize=7.2, color="#A8271F")
ax.annotate("", xy=(0.81, 0.505), xytext=(0.81, 0.735),
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.3, mutation_scale=9))
ax.text(0.795, 0.62, "feeding", ha="right", va="center", fontsize=7.2, color=INK)
ax.annotate("", xy=(0.325, 0.43), xytext=(0.675, 0.43),
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.3, mutation_scale=9))
ax.text(0.50, 0.405, "death and litter", ha="center", va="top", fontsize=7.2, color=INK)
ax.annotate("", xy=(0.19, 0.735), xytext=(0.19, 0.505),
            arrowprops=dict(arrowstyle="-|>", color="#A8271F", lw=1.3, mutation_scale=9))
ax.text(0.205, 0.62, "decomposition", ha="left", va="center", fontsize=7.2, color="#A8271F")
ax.text(0.06, 0.24, "Burning coal, oil and gas returns CO₂ to the air;\nthe ocean takes up about a quarter of human emissions.", fontsize=6.9, color=MUTED, ha="left", va="top", linespacing=1.4)
ax.set_xlim(0, 1); ax.set_ylim(0.14, 1.00)
ax.axis("off")
```

### The nitrogen cycle

Nitrogen is 78 % of the air, but as N₂ it is almost inert: the two atoms are held by a
triple bond no plant or animal can break. The nitrogen cycle is the story of how that
bond is broken and how nitrogen passes from one form to another.

| Step | Change | Organisms that do it |
|---|---|---|
| **Nitrogen fixation** | N₂ → NH₃ / NH₄⁺ | **symbiotic**: *Rhizobium* in legume root nodules, *Frankia* in alder; **free-living aerobic**: *Azotobacter*, *Beijerinckia*; **free-living anaerobic**: *Clostridium pasteurianum*; **cyanobacteria**: *Anabaena*, *Nostoc* (in heterocysts); also lightning and the Haber–Bosch process |
| **Ammonification** | organic N (dead plants, animals, dung) → NH₄⁺ | *Bacillus*, *Clostridium*, fungi and other saprotrophs |
| **Nitrification** | NH₄⁺ → NO₂⁻ | ***Nitrosomonas*** (also *Nitrosococcus*) |
| | NO₂⁻ → NO₃⁻ | ***Nitrobacter*** (also *Nitrospira*) |
| **Assimilation** | NO₃⁻ and NH₄⁺ → plant protein | plants (nitrate is first reduced to nitrite by nitrate reductase, then to ammonia) |
| **Denitrification** | NO₃⁻ → NO₂⁻ → N₂O → N₂ | ***Pseudomonas***, ***Clostridium***, *Thiobacillus* |

```figure caption="The nitrogen cycle, with the bacterium that carries out each step. The two nitrifying steps are separate: *Nitrosomonas* makes nitrite, *Nitrobacter* makes nitrate."
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9, 3.9))
def box(x, y, w, h, text, col):
    ax.add_patch(plt.Rectangle((x, y), w, h, facecolor=col, edgecolor="none", alpha=0.93))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", color="white", fontsize=7.4)
box(0.22, 0.86, 0.36, 0.10, "N₂ in the atmosphere", "#4C5B6B")
box(0.22, 0.66, 0.36, 0.10, "NH₄⁺  ammonium", "#3F7D3A")
box(0.22, 0.46, 0.36, 0.10, "NO₂⁻  nitrite", "#7A9A3E")
box(0.22, 0.26, 0.36, 0.10, "NO₃⁻  nitrate", "#C97B2E")
box(0.22, 0.06, 0.36, 0.10, "Organic N in plants", "#B5482F")
for y0 in (0.76, 0.56, 0.36, 0.16):
    ax.annotate("", xy=(0.40, y0 - 0.002), xytext=(0.40, y0 + 0.098),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.3, mutation_scale=8))
ax.text(0.615, 0.81, "fixation\nRhizobium, Azotobacter,\nClostridium, Anabaena", fontsize=6.9, va="center", ha="left", color=INK, linespacing=1.35)
ax.text(0.615, 0.61, "nitrification\nNitrosomonas", fontsize=6.9, va="center", ha="left", color=INK, linespacing=1.35)
ax.text(0.615, 0.41, "nitrification\nNitrobacter", fontsize=6.9, va="center", ha="left", color=INK, linespacing=1.35)
ax.text(0.615, 0.21, "assimilation\nby plants", fontsize=6.9, va="center", ha="left", color=INK, linespacing=1.35)
ax.plot([0.58, 0.93, 0.93, 0.58], [0.31, 0.31, 0.91, 0.91], color="#A8271F", lw=1.3)
ax.annotate("", xy=(0.575, 0.91), xytext=(0.60, 0.91),
            arrowprops=dict(arrowstyle="-|>", color="#A8271F", lw=1.3, mutation_scale=8))
ax.text(0.975, 0.61, "denitrification\nPseudomonas, Clostridium", fontsize=6.9, va="center", ha="center", rotation=90, color="#A8271F", linespacing=1.35)
ax.plot([0.22, 0.07, 0.07, 0.22], [0.11, 0.11, 0.71, 0.71], color="#2C6E9B", lw=1.3)
ax.annotate("", xy=(0.225, 0.71), xytext=(0.19, 0.71),
            arrowprops=dict(arrowstyle="-|>", color="#2C6E9B", lw=1.3, mutation_scale=8))
ax.text(0.028, 0.41, "ammonification", fontsize=6.9, va="center", ha="center", rotation=90, color="#2C6E9B")
ax.set_xlim(-0.03, 1.03); ax.set_ylim(0.02, 0.99)
ax.axis("off")
```

::: caution Nitrogen: the four mistakes students make
1. **Nitrosomonas makes nitrite, Nitrobacter makes nitrate.** The order is ammonium → nitrite → nitrate; reversing them is the commonest error in the unit.
2. **Nitrogen fixation is not nitrification.** Fixation joins N₂ into ammonia; nitrification only shuffles ammonia up to nitrate.
3. **Denitrification is a loss, not a gain.** It returns nitrogen to the air. A drained paddy loses nitrogen this way; a flooded one keeps it as ammonium, which is why paddy fields are kept flooded.
4. *Rhizobium* is **symbiotic**; *Azotobacter* and *Clostridium* are **free-living**. "Free-living aerobic" means *Azotobacter*.
:::

### The greenhouse effect

Short-wave radiation from the Sun passes almost unchanged through the atmosphere and
is absorbed by the surface, which warms. The warm surface re-emits energy as **long-wave
infrared**, and **greenhouse gases absorb this infrared** and re-radiate it in all
directions, so part of it returns to the surface instead of escaping. The surface
therefore settles at about **+15 °C instead of −18 °C**. That natural greenhouse effect
makes life possible; adding gases to it — the **enhanced greenhouse effect** — drives
current climate change.

| Gas | Main source | Relative contribution | Notes |
|---|---|---|---|
| **Water vapour** | evaporation from oceans | largest share of the natural effect | rises with warming (a positive feedback) |
| **Carbon dioxide** | fossil fuel, deforestation, cement | about three-quarters of the human contribution | reference gas, GWP = 1 |
| **Methane** | paddy fields, cattle, landfill | second largest | GWP ≈ 28 over 100 years |
| **Nitrous oxide** | fertiliser, manure, industry | small but long-lived | GWP ≈ 265 |
| **CFCs and HFCs** | refrigerants, aerosols | tiny in amount, very powerful | GWP of CFC-12 ≈ 10 900 |

::: example Problem. Using $\Delta F = 5.35\ln(C/C_0)$, find the radiative forcing when CO₂ rises from 280 ppm to 560 ppm.
**Solution.** $\Delta F = 5.35 \ln(560/280) = 5.35 \ln 2 = 5.35 \times 0.693$ =
**3.71 W m⁻²**. A doubling of CO₂ always gives this figure, whatever the starting
concentration, because the formula depends on the *ratio*.
:::

### Acid rain

Normal rain is already slightly acidic, **pH ≈ 5.6**, because it dissolves atmospheric
CO₂ to form weak carbonic acid. Rain is called **acid rain** when its pH falls below
about **5.0**, which happens when it dissolves sulphur dioxide and nitrogen oxides:

- SO₂ + H₂O → H₂SO₃, which oxidises to **H₂SO₄** (sulphuric acid)
- 2NO₂ + H₂O → HNO₃ + HNO₂, giving **HNO₃** (nitric acid)

The sources are coal and oil burning (SO₂) and vehicle and power-station exhausts (NOₓ).
The damage is indirect as well as direct: acid water dissolves aluminium from the soil,
and the Al³⁺ reaching a lake is what kills fish. It also leaches calcium and magnesium from soil and eats into limestone and marble. Nepal's emissions are small, but
Kathmandu Valley brick kilns and traffic make local acid aerosols, and Himalayan lakes
are poorly buffered.

### Depletion of the ozone layer

Ozone (O₃) forms in the **stratosphere** (15–35 km up) when UV light splits O₂ and the
free oxygen atoms recombine with O₂. This layer absorbs most of the Sun's **UV-B**,
which would otherwise damage DNA and cause skin cancer and cataracts. Its thickness is
measured in **Dobson units (DU)**; the normal column is about 300 DU.

**The CFC mechanism, step by step:**

1. **Chlorofluorocarbons** (CFCl₃, CF₂Cl₂) — refrigerants, propellants, foam-blowing agents — are chemically inert, so they drift up into the stratosphere without being destroyed.
2. There **UV-C light breaks the C–Cl bond**, releasing a **chlorine radical**:
   CF₂Cl₂ --UV--> CF₂Cl• + Cl•.
3. The chlorine radical attacks ozone: **Cl• + O₃ → ClO• + O₂**.
4. The chlorine monoxide then takes an oxygen atom from another ozone molecule:
   **ClO• + O₃ → Cl• + 2O₂** — and the chlorine atom is **regenerated**.
5. Because it is not used up, one atom can destroy **about 100 000 ozone molecules**
   before it is removed. Chlorine is a **catalyst**.

The **Antarctic "ozone hole"** is a spring phenomenon. In the extreme cold of the polar
night, **polar stratospheric clouds** of ice form, and reactions on their surfaces
convert the inactive reservoir forms (HCl, ClONO₂) into active chlorine; when sunlight
returns, ozone is destroyed very fast. The **Montreal Protocol (1987)** phased out CFCs,
and stratospheric chlorine is now falling, though full recovery will take decades.

### Climate change and Nepal's exposure

The enhanced greenhouse effect has raised the global mean surface temperature by about
**1.1–1.2 °C** above the pre-industrial value. Nepal is exposed in four ways:

- **Glacier retreat.** Meltwater first increases, then falls away, so glacier-fed rivers swell and later run low in the dry season.
- **Glacial lake outburst floods (GLOF).** Meltwater collects behind a loose moraine dam; when it breaks, a wall of water and debris runs down the valley. Imja and Tsho Rolpa are the classic examples, and Thame in Solukhumbu was damaged in 2024.
- **A shifting monsoon.** Longer dry spells inside the season, then very heavy rain in a few days — drought at transplanting, floods at harvest.
- **Upward migration of the belts.** As the tree line climbs, alpine species lose the ground above them and the highest ones are lost first.

The consequences are already visible: more landslides, winter water shortage in mid-hill
towns and a longer dengue season in the Terai. Adaptation means community forest
management, GLOF early-warning systems and check dams on fragile slopes.

```photogrid label="6.2" cols="2" ratio="1.2" caption="More carbon dioxide, more trapped heat. (a) A sal forest in Chitwan stores carbon in wood and soil and is one of the sinks that slow the build-up in the air. (b) The extra radiative forcing from carbon dioxide is approximately 5.35 x ln(C/280) watts per square metre, with C in parts per million and 280 ppm as the pre-industrial value. At 420 ppm it is 2.17 W/m2, at 560 ppm (a doubling) 3.71 W/m2 and at 840 ppm 5.88 W/m2. The curve bends over, so each extra ppm adds less than the one before, but the total still grows without limit."
@ photo id="bio11/sal-forest" cap="Sal forest in Chitwan, a carbon sink"
fit 1.2
focus 0.5 0.5
@ svg cap="Forcing from CO2 compared with 280 ppm"
F = lambda c: 5.35 * math.log(c / 280)
assert abs(F(420) - 2.169) < 0.001 and abs(F(560) - 3.708) < 0.001 and abs(F(840) - 5.877) < 0.001
facts = dict(f420="%.2f" % F(420), f560="%.2f" % F(560), f840="%.2f" % F(840))
f = Fig(300, 236)
f.text(150, 12, "Forcing (W/m2) against CO2 (ppm)", size=10.5, color=NAVY, bold=True)
ax = Axes(f, 44, 34, 232, 150, (280, 840), (0, 6))
ax.grid(140, 2).axes("ppm", "W/m2")
ax.curve(F, 280, 840, color=RED)
ax.pt(420, F(420), "2.17", dx=6, dy=16)
ax.pt(560, F(560), "3.71", dx=6, dy=16)
ax.pt(840, F(840), "5.88", dx=-4, dy=20, anchor="middle")
f.text(150, 224, "each doubling adds 3.71 W/m2", size=10.5, color=NAVY, bold=True)
```

## 6.3 Forest types of Nepal; biological invasion

### Forest belts by altitude

Nepal spans only 147 000 km², but rises from about 60 m in the Terai to 8 848 m at
Sagarmatha, so a day's walk uphill passes the belts of a whole continent. About **45 % of
the land is forest or other wooded land**. Temperature falls by roughly **0.6 °C for
every 100 m of ascent**, and the monsoon is heaviest in the east.

```photo id="bio11/sal-forest" caption="Tropical Sal (*Shorea robusta*) forest in Chitwan National Park — the dominant vegetation of Nepal below 1000 m." width="92"
crop 0.02 0.02 0.98 0.99
```


| Belt | Altitude | Climate | Characteristic species |
|---|---|---|---|
| **Tropical** | below 1 000 m — Terai, inner Terai, Chitwan, Bardia | hot, monsoon 1 500–2 500 mm, mean above 24 °C | **sal** *Shorea robusta*, **sissoo** *Dalbergia sissoo*, **khair** *Acacia catechu*, **simal** *Bombax ceiba*, tall elephant grass (*Saccharum–Phragmites*) |
| **Subtropical** | 1 000–2 000 m — mid-hills, Kathmandu, Pokhara | warm, 1 000–2 000 mm | **chir pine** *Pinus roxburghii*, **chilaune** *Schima wallichii*, **katus** *Castanopsis indica*, **utis** *Alnus nepalensis*, **lali gurans** *Rhododendron arboreum* |
| **Temperate** | 2 000–3 000 m | cool, winter snow | **oak** *Quercus semecarpifolia* and *Q. lamellosa*, rhododendron, **spruce** *Picea smithiana*, **hemlock** *Tsuga dumosa*, maple *Acer* |
| **Subalpine** | 3 000–4 000 m | cold, long snow cover | **fir** *Abies spectabilis*, **birch** *Betula utilis* (bhojpatra), *Rhododendron campanulatum*, juniper |
| **Alpine** | 4 000–5 000 m, above the tree line | very cold, short growing season, strong UV | dwarf juniper, cushion plants, tussock grasses, mosses, lichens; no trees |
| **Nival** | above 5 000 m | permanent snow and ice | snow algae, lichens on rock; no vascular plants |

```figure caption="The forest belts of Nepal. Temperature falls about 0.6 °C per 100 m of ascent, so altitude acts as latitude: a walk from Chitwan to the Khumbu passes from sal forest to bare rock."
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9, 3.4))
bands = [
    (5000, 5200, "Nival  > 5 000 m", "snow algae, lichens", "#DCE6EE", "#33414D"),
    (4000, 5000, "Alpine  4 000–5 000 m", "cushion plants, juniper scrub", "#B9C7A8", "#22301F"),
    (3000, 4000, "Subalpine  3 000–4 000 m", "fir, birch, rhododendron", "#8FA98C", "white"),
    (2000, 3000, "Temperate  2 000–3 000 m", "oak, spruce, hemlock", "#5C7F55", "white"),
    (1000, 2000, "Subtropical  1 000–2 000 m", "chir pine, chilaune, katus", "#7FA35A", "white"),
    (0, 1000, "Tropical  below 1 000 m", "sal, sissoo, khair", "#C9B45A", "#2B2B1A"),
]
for lo, hi, name, spp, col, tc in bands:
    ax.add_patch(plt.Rectangle((0, lo), 1.0, hi - lo, facecolor=col, edgecolor="white", lw=1.1))
    ax.text(0.025, (lo + hi) / 2, name, ha="left", va="center", fontsize=7.2, color=tc, fontweight="bold")
    ax.text(0.975, (lo + hi) / 2, spp, ha="right", va="center", fontsize=7.0, color=tc)
ax.set_xlim(0, 1); ax.set_ylim(0, 5200)
ax.set_yticks([0, 1000, 2000, 3000, 4000, 5000])
ax.set_yticklabels(["0", "1 000", "2 000", "3 000", "4 000", "5 000"], fontsize=7.2)
ax.set_xticks([])
ax.set_ylabel("altitude (m)", fontsize=7.6)
ax.spines[["top", "right", "bottom"]].set_visible(False)
ax.tick_params(axis="y", length=2.5, pad=2)
```

::: memory The belts, in one line
**Sal in the Terai, chir pine on the lower hills, oak and rhododendron in the middle,
fir and birch above, cushion plants at the top.**
:::

### Biological invasion

An **invasive alien species** is a plant or animal moved by humans outside its natural
range that then spreads on its own and causes harm. Nepal's roads and disturbed
riverbanks give invaders the bare, sunny ground they need, and without their natural
enemies they outgrow the native flora.

| Species | Nepali name | Origin | Where it has spread | Why it is a problem |
|---|---|---|---|---|
| ***Lantana camara*** | **banmara** ("forest killer") | tropical America | Chitwan, Bardia, most Terai forests | thorny thickets block sal regeneration; toxic to livestock; replaces fodder |
| ***Mikania micrantha*** | mikaniya, "mile-a-minute" | Central and South America | eastern and central Terai, Chitwan | grows centimetres a day, smothers shrubs and saplings |
| ***Eichhornia crassipes*** | **jal kumbhi** | Amazon basin | Phewa, Rupa, Begnas, Terai ponds | mats block boats and nets, cut light and oxygen, kill fish, breed mosquitoes |
| ***Parthenium hysterophorus*** | congress grass | tropical America | roadsides, wasteland, Terai fields | pollen and leaf hairs cause dermatitis and rhinitis; allelopathy suppresses crops |

Control is **manual removal before flowering**, **biological control** with host-specific
insects against *Mikania* and water hyacinth, and above all **keeping the ground covered**
so invaders cannot establish.

```photo id="bio11/khaptad-patan" caption="A subalpine meadow (*patan*) in Khaptad National Park, with the conifer forest ending on the ridge above it. Meadows like this are grazed by cattle and sheep through the summer and left empty in winter." width="88"
crop 0.00 0.34 0.56 1.00
call 0.45 0.88 0.76 0.61 "conifer forest and tree line"
call 0.30 0.47 0.52 0.27 "open grazing meadow"
```


```photo id="bio11/rhododendron-forest" caption="Temperate oak–rhododendron forest in the Annapurna Conservation Area. *Rhododendron arboreum* (lali gurans), Nepal's national flower, flowers between about 2000 and 3000 m in March and April." width="86"
crop 0.14 0.00 0.80 1.00
```


## 6.4 Ecological succession: hydrosere and xerosere; ecological adaptation

### The idea of succession

**Ecological succession** is the directional change in species composition at one place
over time, until a stable community — the **climax** — is reached. The sequence of communities is a **sere**; each intermediate community is a
**seral stage**; the first is the **pioneer community**.

- **Primary succession** starts on a surface that has never carried vegetation and has **no soil** — bare rock, a new lava flow, a retreating glacier's moraine, a fresh landslide scar.
- **Secondary succession** starts where a community has been destroyed but **soil and seeds remain** — an abandoned field (khoriya), a burnt forest, a cleared hillside. It is much faster because the soil is already made.

A succession that begins in water is a **hydrosere**; one that begins on dry rock is a
**xerosere**.

### The hydrosere, stage by stage

| Stage | Community | What happens |
|---|---|---|
| 1. **Phytoplankton** | *Chlorella*, diatoms | open water is colonised; dead cells build an ooze on the bottom |
| 2. **Rooted submerged** | *Hydrilla*, *Vallisneria* | rooted plants trap sediment; the bottom rises |
| 3. **Rooted floating** | *Nymphaea*, *Nelumbo* | broad leaves shade the submerged plants; more humus forms |
| 4. **Reed swamp** | *Typha*, *Phragmites* | water is shallow; tall emergents fill the margin and their litter raises the bed |
| 5. **Sedge meadow** | *Carex*, *Juncus* | the water table falls below the surface; marsh becomes wet meadow |
| 6. **Woodland** | *Salix*, *Alnus* | shrubs and fast-growing trees invade the meadow |
| 7. **Climax forest** | sal in the Terai, oak in the hills | a closed canopy forms; the community is in equilibrium with the climate |

### The xerosere, stage by stage

| Stage | Community | What happens |
|---|---|---|
| 1. **Crustose lichen** | *Graphis*, *Lecanora* | lichens dissolve rock with organic acids and trap wind-blown dust — the first soil |
| 2. **Foliose lichen** | *Parmelia* | a deeper mat of organic matter holds moisture |
| 3. **Moss stage** | *Grimmia*, *Tortula* | mosses hold water and add humus; a thin soil forms |
| 4. **Herb stage** | annual grasses, *Selaginella*, ferns | roots break the rock further; soil deepens |
| 5. **Shrub stage** | *Berberis*, *Rubus*, *Lantana* | woody plants shade out the herbs |
| 6. **Tree / climax stage** | sal, oak or pine according to climate | trees close the canopy; the climax forest is reached |

```figure caption="The two seres compared. A hydrosere starts in open water and dries out as sediment accumulates; a xerosere starts on bare rock and builds soil. Both end in the climax forest."
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.1, 2.9))
hydro = ["Phyto-\nplankton", "Submerged\n(Hydrilla)", "Floating\n(Nymphaea)", "Reed swamp\n(Typha)", "Sedge\nmeadow", "Climax\nforest"]
xero = ["Crustose\nlichen", "Foliose\nlichen", "Moss\nstage", "Herb\nstage", "Shrub\nstage", "Climax\nforest"]
for row, (title, stages, y, col) in enumerate([
        ("Hydrosere: water → land", hydro, 0.60, "#2C6E9B"),
        ("Xerosere: bare rock → soil", xero, 0.16, "#8A6A3B")]):
    ax.text(0.005, y + 0.26, title, fontsize=7.6, color=col, fontweight="bold", ha="left")
    for i, s in enumerate(stages):
        x = 0.005 + i * 0.166
        ax.add_patch(plt.Rectangle((x, y), 0.145, 0.22, facecolor=col, edgecolor="none",
                                   alpha=0.16 + 0.06 * i))
        ax.text(x + 0.0725, y + 0.11, s, ha="center", va="center", fontsize=6.9,
                color=INK, linespacing=1.2)
        if i < 5:
            ax.annotate("", xy=(x + 0.164, y + 0.11), xytext=(x + 0.147, y + 0.11),
                        arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.0, mutation_scale=7))
ax.text(0.005, 0.03, "biomass, diversity and soil organic matter rise along both series",
        fontsize=6.9, color=MUTED, ha="left")
ax.set_xlim(0, 1); ax.set_ylim(0, 0.98)
ax.axis("off")
```

### Trends during succession, and the climax

| Feature | Direction from pioneer to climax |
|---|---|
| Biomass and standing crop | **increases**, then levels off |
| Species diversity | **increases**, then levels off or falls slightly in a very dense climax |
| Soil depth and organic matter | **increases** |
| Nutrient cycling | becomes **tighter** — less leakage, more internal recycling |
| Food webs | become more complex, with more specialised niches |
| Net production | rises at first, then falls; at climax **gross production ≈ respiration** |
| Stability | **increases** |

The **climax community** is the end point: a community in equilibrium with the regional
climate, whose species composition stays roughly constant from year to year. **F. E.
Clements** held that every region has one climax set by climate (the **monoclimax**
theory); **A. G. Tansley** held that soil, fire and grazing can produce several stable
end points in one climate (**polyclimax**). Climate sets the potential; local factors
decide which climax is reached.

::: caution Succession: the traps
- **Primary succession has no soil at the start.** If the stem mentions soil, seeds or a plough, it is secondary.
- **The pioneer of a hydrosere is phytoplankton, not a reed.** *Typha* comes at stage 4.
- **The pioneer of a xerosere is a crustose lichen, not a moss.**
:::

### Ecological adaptation

An **adaptation** is an inherited feature that helps an organism survive in its
environment. The examinable sets are the ones named by their habitat:

| Group | Habitat | Adaptations | Examples |
|---|---|---|---|
| **Hydrophytes** | wholly or partly in water | air spaces (**aerenchyma**); thin cuticle; stomata on the upper surface or none; weak roots; flexible stems | *Hydrilla*, *Nymphaea*, *Eichhornia* |
| **Xerophytes** | dry habitats | thick waxy cuticle; **sunken stomata**; leaves reduced to spines; succulent water-storing stems; deep roots; rolled leaves | *Opuntia*, *Acacia*, *Euphorbia* |
| **Epiphytes** | on other plants, not parasitic | aerial roots with a **velamen** that absorbs rain; water-holding leaves; CAM photosynthesis | *Vanda*, *Dendrobium*, ferns, mosses on sal trees |
| **Halophytes** | salty soil | salt glands, succulent leaves, high internal osmotic pressure | mangroves (not in Nepal) |
| **Alpine plants** | cold, strong UV, short season | cushion or rosette habit, woolly hairs, dark UV-screening pigments, long taproots, rapid flowering | *Rhododendron campanulatum*, *Saussurea* |

The Himalayan belt adds **dwarf and cushion forms** that stay close to the warm ground,
**hairy or waxy surfaces** that cut water loss in the dry winter, and **early flowering**
in the brief snow-free window. *Betula utilis* at the tree line grows as a stunted,
twisted shrub — the same species, a different shape, because the environment sets the
form.

::: example Lindeman 10 % law across a four-trophic pond chain
**Problem.** In a Terai fishpond, phytoplankton fix $20{,}000\text{ kJ m}^{-2}\text{ yr}^{-1}$ of net primary production. In the chain phytoplankton $\rightarrow$ zooplankton $\rightarrow$ small fish $\rightarrow$ kingfisher, how much energy reaches the kingfisher under the 10 % law?

**Solution.** Three transfers of $10\%$ ($0.1^3 = 10^{-3}$) leave $20{,}000 \times 10^{-3} = \mathbf{20\text{ kJ m}^{-2}\text{ yr}^{-1}}$ at the fourth trophic level (tertiary consumer).
:::

## Formula and fact sheet

| Item | Fact |
|---|---|
| GPP, NPP | NPP = GPP − R |
| 10 % law | Lindeman (1942); about 10 % of energy passes to the next level |
| Energy pyramid | **always upright**; biomass pyramid inverted in a pond; number pyramid inverted on one tree |
| Decomposers | act at **every** trophic level; not a level of the standard pyramid |
| Mutualism | + + — lichen, *Rhizobium*–legume, fig–fig wasp |
| Commensalism | + 0 — cattle egret with cattle, epiphytic orchid on a tree |
| Parasitism | + − — *Cuscuta* (amarbel), *Scurrula* (liwang) on mango, liver fluke |
| Predation | + − — tiger on chital, ladybird on aphid |
| Competition | − − — two grass species; sal versus *Terminalia* seedlings |
| Amensalism | 0 − — *Penicillium* killing bacteria |
| Carbon reservoirs, large to small | carbonate rocks ≫ ocean (≈ 38 000 Gt C) > fossil fuels > soil and biota (≈ 2 000 Gt C) > atmosphere (≈ 900 Gt C) |
| N₂ fixation | *Rhizobium* (symbiotic), *Azotobacter* (free-living aerobic), *Clostridium* (anaerobic), *Anabaena*/*Nostoc* (heterocysts), *Frankia* (alder) |
| Ammonification | *Bacillus*, *Clostridium*, fungi |
| Nitrification | **NH₄⁺ → NO₂⁻ by *Nitrosomonas*; NO₂⁻ → NO₃⁻ by *Nitrobacter*** |
| Denitrification | *Pseudomonas*, *Clostridium* → N₂ |
| Greenhouse gases | water vapour (largest natural share), CO₂, CH₄ (GWP ≈ 28), N₂O (≈ 265), CFC-12 (≈ 10 900) |
| Natural greenhouse effect | surface at about +15 °C instead of −18 °C |
| Radiative forcing of doubling CO₂ | $\Delta F = 5.35\ln 2$ = 3.71 W m⁻² |
| Clean rain | pH ≈ 5.6 (dissolved CO₂); acid rain below about 5.0 |
| Acid rain acids | H₂SO₄ from SO₂, HNO₃ from NOₓ |
| Ozone | stratosphere 15–35 km; absorbs UV-B; measured in Dobson units (~300 DU) |
| CFC → ozone | UV splits C–Cl → Cl•; Cl• + O₃ → ClO• + O₂; ClO• + O₃ → Cl• + 2O₂; one Cl destroys ~100 000 O₃ |
| Montreal Protocol | 1987, phase-out of ozone-depleting substances |
| Nepal forest cover | about 45 % of the land |
| Nepal belts | tropical < 1 000 m; subtropical 1 000–2 000 m; temperate 2 000–3 000 m; subalpine 3 000–4 000 m; alpine 4 000–5 000 m; nival above 5 000 m |
| Belt species | sal, sissoo, khair (tropical); chir pine, chilaune, katus (subtropical); oak, spruce, hemlock (temperate); fir, birch (subalpine); cushion plants (alpine) |
| Lapse rate | about 0.6 °C per 100 m of ascent |
| Invasive plants | *Lantana camara* (banmara), *Mikania micrantha*, *Eichhornia crassipes* (jal kumbhi), *Parthenium hysterophorus* |
| Hydrosere order | phytoplankton → submerged → floating → reed swamp → sedge meadow → woodland → climax forest |
| Xerosere order | crustose lichen → foliose lichen → moss → herb → shrub → tree (climax) |
| Primary vs secondary | no soil, slow / soil and seeds present, fast |
| Climax theories | monoclimax (Clements); polyclimax (Tansley) |
| Succession trends | biomass ↑, diversity ↑, soil organic matter ↑, P/R → 1 at climax |
| Adaptations | hydrophytes (aerenchyma), xerophytes (sunken stomata, spines, succulence), epiphytes (velamen), alpine (cushion habit, hairs) |

## Chapter summary

- An ecosystem has a structure (abiotic factors plus producers, consumers and decomposers) and a function (productivity, decomposition, energy flow, nutrient cycling).
- A pond is zoned into littoral, limnetic, profundal and benthic; a forest is layered from canopy to litter.
- Energy flow is unidirectional and follows Lindeman's 10 % law, so food chains are short; the energy pyramid is always upright while number and biomass pyramids can invert.
- Decomposers work at every trophic level and form a detrital pathway, not the apex of the pyramid.
- The six interactions: mutualism (+ +), commensalism (+ 0), parasitism (+ −), predation (+ −), competition (− −), amensalism (0 −).
- In the nitrogen cycle *Rhizobium*, *Azotobacter*, *Clostridium* and *Anabaena* fix N₂; *Nitrosomonas* makes nitrite; *Nitrobacter* makes nitrate; *Pseudomonas* and *Clostridium* denitrify.
- Greenhouse gases absorb outgoing infrared; doubling CO₂ forces the climate by 3.71 W m⁻². Acid rain (pH below 5) comes from SO₂ and NOₓ; ozone loss is a chlorine-catalysed chain started by CFCs.
- Nepal runs from tropical sal below 1 000 m through subtropical chir pine, temperate oak and subalpine fir to alpine cushion plants; the four named invaders are *Lantana*, *Mikania*, water hyacinth and *Parthenium*.
- Succession is primary (no soil) or secondary (soil present); the hydrosere begins with phytoplankton and the xerosere with crustose lichens, and both end in a climax forest with high biomass, high diversity and production balanced by respiration.

## Practice questions

**Set A — Recall (30 questions)**

1. The law that only about 10 % of the energy at one trophic level passes to the next was proposed by
   (a) E. P. Odum (b) A. G. Tansley (c) R. L. Lindeman (d) F. E. Clements
2. Organisms that break down dead organic matter into inorganic nutrients are called
   (a) decomposers (b) primary consumers (c) producers (d) tertiary consumers
3. Which ecological pyramid can never be inverted?
   (a) pyramid of numbers (b) pyramid of biomass (c) pyramid of numbers in a grassland (d) pyramid of energy
4. The association between the fungus and the alga in a lichen is an example of
   (a) commensalism (b) mutualism (c) parasitism (d) amensalism
5. Cattle egrets that follow grazing buffalo in the Terai to catch the insects they disturb show
   (a) commensalism (b) mutualism (c) predation (d) amensalism
6. *Cuscuta* (amarbel) growing over a host shrub is an example of
   (a) epiphytism (b) saprophytism (c) parasitism (d) commensalism
7. The free-living aerobic nitrogen-fixing bacterium of soil is
   (a) *Nitrosomonas* (b) *Azotobacter* (c) *Nitrobacter* (d) *Pseudomonas*
8. The conversion of ammonium to nitrite in the nitrogen cycle is carried out by
   (a) *Nitrobacter* (b) *Rhizobium* (c) *Azotobacter* (d) *Nitrosomonas*
9. Nitrate is reduced step by step to nitrogen gas mainly by
   (a) *Nitrosomonas* (b) *Pseudomonas* (c) *Rhizobium* (d) *Nitrobacter*
10. Among the reservoirs that exchange carbon quickly with the atmosphere, the largest is
   (a) the atmosphere (b) living organisms (c) soil organic matter (d) the ocean
11. The gas that contributes the largest share of the natural greenhouse effect is
   (a) water vapour (b) carbon dioxide (c) methane (d) CFC-12
12. Clean rain is slightly acidic, with a pH of about 5.6, mainly because it dissolves
   (a) sulphur dioxide (b) ammonia (c) carbon dioxide (d) nitrogen oxides
13. The thickness of the ozone layer is expressed in
   (a) pascals (b) sieverts (c) decibels (d) Dobson units
14. Chlorofluorocarbons destroy stratospheric ozone because ultraviolet light releases from them
   (a) fluorine atoms (b) chlorine atoms (c) carbon atoms (d) hydrogen atoms
15. The Montreal Protocol (1987) is an international agreement to
   (a) reduce greenhouse gas emissions from industry (b) protect wetlands of international importance (c) phase out ozone-depleting substances (d) control trade in endangered species
16. In Nepal, sal (*Shorea robusta*) forests are characteristic of the
   (a) tropical zone below about 1 000 m (b) temperate zone at 2 000–3 000 m (c) alpine zone above 4 000 m (d) subalpine zone at 3 000–4 000 m
17. Chir pine (*Pinus roxburghii*) is a characteristic tree of Nepal's
   (a) alpine zone (b) tropical Terai (c) subtropical zone (d) nival zone
18. Water hyacinth (*Eichhornia crassipes*), which chokes Nepali lakes, was introduced from
   (a) Africa (b) South America (c) Australia (d) Europe
19. The pioneer community of a hydrosere is
   (a) reed swamp (b) sedge meadow (c) submerged plants (d) phytoplankton
20. The pioneer organisms of a xerosere on bare rock are
   (a) crustose lichens (b) mosses (c) annual herbs (d) shrubs
21. The final stable community of a succession, in equilibrium with the climate, is called the
   (a) seral community (b) climax community (c) pioneer community (d) edaphic community
22. Succession that begins on a bare surface with no soil and no seeds is
   (a) secondary succession (b) autogenic succession (c) primary succession (d) allogenic succession
23. *Lantana camara*, called banmara in Nepali, is an example of
   (a) an invasive alien species (b) an endemic species (c) a rare medicinal plant (d) a nitrogen-fixing tree
24. The decomposers of a pond ecosystem are chiefly
   (a) phytoplankton (b) zooplankton (c) fish (d) bacteria and fungi
25. In a forest food chain, the herbivores form the
   (a) first trophic level (b) third trophic level (c) second trophic level (d) fourth trophic level
26. The "mile-a-minute" weed that smothers regeneration in Chitwan's forests is
   (a) *Lantana camara* (b) *Mikania micrantha* (c) *Parthenium hysterophorus* (d) *Eichhornia crassipes*
27. Nepal's alpine zone, above the tree line, is dominated by
   (a) sal and sissoo (b) chir pine and chilaune (c) oak and spruce (d) dwarf shrubs, cushion plants and grasses
28. The greenhouse gas with the highest global warming potential per molecule among these is
   (a) CFC-12 (b) carbon dioxide (c) methane (d) nitrous oxide
29. Amensalism is a relationship in which
   (a) both species benefit (b) one species is harmed and the other is unaffected (c) both species are harmed (d) one benefits and the other is unaffected
30. In a food chain, the proportion of energy transferred from one trophic level to the next is about
   (a) 1 % (b) 50 % (c) 10 % (d) 90 %

::: note Answers and explanations — Set A
**1.** (c) — Lindeman's trophic-dynamic concept (1942) gives the 10 % law. Odum popularised energy-flow diagrams, Tansley coined "ecosystem", Clements gave the monoclimax theory.
**2.** (a) — Decomposers (saprotrophs) are bacteria and fungi that digest dead matter outside their bodies and release inorganic nutrients. Consumers eat living or recently dead material; producers make their own food.
**3.** (d) — The energy pyramid is always upright because energy is lost as heat at every transfer. Number and biomass pyramids can invert (many insects on one tree; phytoplankton smaller than zooplankton).
**4.** (b) — The alga photosynthesises and the fungus supplies water, minerals and shelter; both benefit, so the signs are + +. Neither is harmed, so it is not parasitism.
**5.** (a) — The egret gains food (+); the buffalo is neither helped nor harmed (0). This is the standard + 0 example of commensalism.
**6.** (c) — *Cuscuta* has no chlorophyll and draws food through haustoria pushed into the host's vascular tissue; the host loses, the parasite gains.
**7.** (b) — *Azotobacter* is a free-living aerobic fixer. *Rhizobium* is symbiotic, *Clostridium* is anaerobic, and *Nitrosomonas* nitrifies rather than fixes.
**8.** (d) — *Nitrosomonas* oxidises NH₄⁺ to NO₂⁻. *Nitrobacter* carries out the next step, NO₂⁻ to NO₃⁻.
**9.** (b) — *Pseudomonas* (with *Clostridium*) reduces nitrate through nitrite and N₂O to N₂. This is denitrification, a loss of nitrogen from the soil.
**10.** (d) — The ocean holds about 38 000 Gt C as dissolved inorganic carbon, against about 900 Gt C in the atmosphere and about 2 000 Gt C in soil and living matter.
**11.** (a) — Water vapour accounts for the largest share of the natural greenhouse effect, though it is not directly controlled by human emissions.
**12.** (c) — CO₂ dissolves to form weak carbonic acid, giving a natural pH near 5.6. SO₂ and NOₓ push it below about 5.0 in polluted air.
**13.** (d) — One Dobson unit is 0.01 mm of ozone at standard temperature and pressure; the normal column is about 300 DU.
**14.** (b) — UV-C breaks the C–Cl bond and releases a chlorine radical, which then attacks ozone catalytically. The C–F bond is too strong to break at these wavelengths.
**15.** (c) — Montreal (1987) phased out CFCs and other ozone-depleting substances. The climate treaty is Kyoto/Paris, the wetland treaty is Ramsar, and species trade is CITES.
**16.** (a) — Sal is the dominant tree of the Terai and inner Terai below about 1 000 m, where the monsoon is heavy and the winter mild.
**17.** (c) — Chir pine dominates the warm, dry slopes of the mid-hills between about 1 000 and 2 000 m, often on south-facing slopes.
**18.** (b) — Water hyacinth is native to the Amazon basin and was spread worldwide as an ornamental. It now mats the surfaces of Phewa, Rupa and Begnas.
**19.** (d) — Open water is first colonised by phytoplankton; their dead cells start the ooze that eventually fills the pond.
**20.** (a) — Crustose lichens are the only organisms that can hold on to bare rock and begin to dissolve it; mosses need the thin soil the lichens create.
**21.** (b) — The climax community is stable and in equilibrium with the regional climate. A seral community is any intermediate stage.
**22.** (c) — Primary succession starts where no soil exists. Secondary succession starts after a disturbance that leaves soil and seeds behind.
**23.** (a) — *Lantana* was brought from tropical America as an ornamental and has become a thicket-forming invader of Terai forests; "banmara" means forest killer.
**24.** (d) — Bacteria and fungi in the bottom mud break down the organic matter that settles. Phytoplankton are producers and zooplankton are consumers.
**25.** (c) — Producers occupy the first trophic level and herbivores the second. The third level holds the carnivores that eat the herbivores.
**26.** (b) — *Mikania micrantha* can grow several centimetres a day, hence "mile-a-minute"; it blankets shrubs and young trees. *Lantana* is a thorny shrub, not a vine.
**27.** (d) — Above the tree line the growing season is too short for trees, so the flora is dwarf juniper, cushion plants, tussock grasses, mosses and lichens.
**28.** (a) — CFC-12 has a 100-year global warming potential of about 10 900, against about 265 for N₂O, 28 for methane and 1 for CO₂.
**29.** (b) — In amensalism one partner is harmed and the other is unaffected (0 −), as when *Penicillium* kills bacteria with penicillin.
**30.** (c) — Lindeman's figure is about 10 %; the other 90 % is lost mainly as heat in respiration, which is why food chains are short.
:::

**Set B — Understanding (18 questions)**

1. A pyramid of numbers is inverted in
   (a) a grassland (b) a single large tree carrying thousands of insects (c) a pond full of phytoplankton (d) a maize field
2. Energy flow in an ecosystem is described as unidirectional because
   (a) energy is recycled by decomposers (b) energy passes only through herbivores (c) energy is stored as biomass (d) heat lost at each level cannot be used again by producers
3. Decomposers are not placed at the top of an energy pyramid because they
   (a) take energy from every level and release it as heat by a detrital pathway (b) are too small to count (c) are producers (d) do not respire
4. Two grass species in one field need the same light, water and nitrogen. Their relationship is
   (a) mutualism (b) commensalism (c) competition (d) parasitism
5. A *Penicillium* mould releases a substance that kills bacteria around it while the mould is unaffected. This is
   (a) parasitism (b) predation (c) commensalism (d) amensalism
6. Lentil and chickpea enrich the soil because *Rhizobium* in their root nodules
   (a) decomposes dead roots (b) reduces atmospheric N₂ to ammonia using nitrogenase (c) oxidises nitrate to nitrogen gas (d) converts ammonia to nitrite
7. A farmer keeps a paddy field flooded instead of draining it. This reduces nitrogen loss because flooding
   (a) increases nitrogen fixation (b) prevents ammonification (c) stops the conversion of ammonium to nitrate, which would then be denitrified (d) stops nitrate uptake by rice
8. Greenhouse gases warm the surface because they
   (a) absorb outgoing long-wave infrared radiation and re-radiate part of it back (b) absorb incoming ultraviolet radiation (c) reflect short-wave radiation from the Sun (d) stop conduction from the ground
9. Acid rain kills fish in poorly buffered mountain lakes mainly by
   (a) heating the water (b) adding nutrients that cause algal blooms (c) lowering the pH and releasing toxic aluminium ions from the soil (d) raising the dissolved oxygen
10. One chlorine atom can destroy thousands of ozone molecules because chlorine acts as
   (a) a reactant that is used up (b) a catalyst that is regenerated in the cycle (c) a solvent (d) an oxidising agent that is consumed
11. The Antarctic ozone hole appears in spring because
   (a) the Sun is brightest over the pole then (b) most CFCs are made in Antarctica (c) volcanic ash destroys ozone (d) ice crystals in polar clouds turn stored chlorine into active forms
12. A glacier-fed river in Nepal now peaks earlier in summer than it did fifty years ago. The most likely cause is
   (a) earlier snowmelt and glacier retreat under a warming climate (b) an increase in winter snowfall (c) a decrease in monsoon rainfall (d) tectonic uplift of the Himalaya
13. After a landslide strips a Himalayan slope to bare rock, the first colonists are likely to be
   (a) sal seedlings (b) lichens and mosses (c) tall grasses (d) oak saplings
14. During succession from an open pond to a forest, total biomass and species diversity generally
   (a) both decrease (b) stay constant (c) both increase (d) rise and then fall to zero
15. *Mikania micrantha* threatens Chitwan's sal forest mainly because it
   (a) grows over and smothers native shrubs and regeneration (b) is a root parasite of sal (c) poisons the soil with heavy metals (d) attracts elephants that fell trees
16. The biomass of phytoplankton in a pond is often less than that of the zooplankton feeding on it. This is possible because
   (a) zooplankton also photosynthesise (b) phytoplankton are decomposers (c) the energy pyramid is inverted (d) phytoplankton divide fast, so a small crop supports a large consumer biomass
17. Forests matter in the carbon cycle mainly because they
   (a) release CO₂ during photosynthesis (b) prevent nitrogen fixation (c) store carbon in wood and soil and remove CO₂ from the air (d) convert carbon into nitrogen
18. A xerosere differs from a hydrosere in that a xerosere
   (a) starts dry and soil-less, and depends on lichens to make the first soil (b) starts in open water (c) has no pioneer stage (d) always ends in a grassland

::: note Answers and explanations — Set B
**1.** (b) — One tree, a single producer, supports thousands of herbivores, so the base is narrow. Option (c) is an inverted *biomass* pyramid, not a numbers one.
**2.** (d) — Heat cannot be captured again by a producer; matter cycles because it is not degraded in this way.
**3.** (a) — They feed on litter, dung and corpses from every level, so they cannot be stacked in one tier.
**4.** (c) — Both lose (− −) because each takes what the other needs.
**5.** (d) — Bacteria harmed (−), mould unaffected (0): amensalism.
**6.** (b) — Nitrogenase in the nodule reduces N₂ to NH₃, which the plant then assimilates.
**7.** (c) — Nitrification needs oxygen, so in a flooded field ammonium is not converted to nitrate; with little nitrate present, the denitrifiers have nothing to reduce. Draining lets ammonium nitrify, and the nitrate is then lost as N₂ or by leaching.
**8.** (a) — The gases absorb the surface's infrared and re-radiate part of it downwards; they do not reflect sunlight.
**9.** (c) — H⁺ displaces Al³⁺ from soil particles, and the aluminium coating the gills kills the fish.
**10.** (b) — Cl is regenerated each cycle (Cl• + O₃ → ClO• + O₂; ClO• + O₃ → Cl• + 2O₂), so one atom destroys about 100 000 molecules.
**11.** (d) — Polar stratospheric clouds form only in the polar night; reactions on them free active chlorine, which acts when sunlight returns.
**12.** (a) — Warmer air melts the snowpack earlier and shrinks the glaciers, so the peak arrives sooner and late-summer flow falls.
**13.** (b) — A landslide scar has no soil and no seeds: a primary site, where lichens and mosses must make the first soil.
**14.** (c) — Biomass accumulates and more niches appear, so both rise and then level off.
**15.** (a) — It is a fast vine that blankets shrubs and saplings and cuts their light; it is not a parasite.
**16.** (d) — Phytoplankton are eaten as fast as they divide, so a small standing crop supports a larger biomass of longer-lived zooplankton.
**17.** (c) — Growing trees remove CO₂ and lock the carbon in wood and soil, so a standing forest is a carbon sink.
**18.** (a) — A xerosere starts on dry, soil-less rock and is built by lichens; a hydrosere starts in water.
:::

**Set C — Application (12 questions)**

1. In a grassland the producers fix 20 000 kJ of energy in a year. If the 10 % law holds at each step, the energy available to the secondary consumers is
   (a) 2 000 kJ (b) 1 000 kJ (c) 100 kJ (d) 200 kJ
2. A food chain is grass → grasshopper → frog → snake → hawk. If the hawk receives 10 kJ, the energy fixed by the grass was about
   (a) 10 000 kJ (b) 100 000 kJ (c) 1 000 kJ (d) 1 000 000 kJ
3. A lake beside farmland receives heavy fertiliser runoff. Algae bloom, then die, and fish die. The oxygen sequence is
   (a) oxygen rises in the bloom by day, then falls as decomposers use it (b) oxygen falls at once and stays low (c) oxygen is unchanged (d) oxygen rises permanently
4. A student counts 1 000 000 phytoplankton, 200 000 zooplankton, 2 000 small fish and 5 large fish in a pond. The pyramid of numbers from these data is
   (a) inverted at the base (b) spindle-shaped (c) upright (d) inverted at the top
5. In a legume field *Rhizobium* fixes 20 kg of N₂ per hectare per year; 5 kg is lost by denitrification and 3 kg by leaching. The nitrogen added to the soil is
   (a) 28 kg (b) 12 kg (c) 20 kg (d) 8 kg
6. A forest is cleared and then abandoned. Forty years later a young forest stands on the site. This is
   (a) primary succession (b) a hydrosere (c) a xerosere (d) secondary succession
7. In a pond the sequence phytoplankton → zooplankton → small fish → kingfisher is a
   (a) grazing food chain (b) detrital food chain (c) food web (d) parasitic chain
8. The Terai lies below 300 m, the mid-hills reach 2 500 m and the tree line is near 4 000 m. A forest of oak, rhododendron and spruce at 2 600 m belongs to the
   (a) tropical zone (b) alpine zone (c) temperate zone (d) subtropical zone
9. Using $\Delta F = 5.35\ln(C/C_0)$, the radiative forcing when CO₂ rises from 280 ppm to 560 ppm is
   (a) 5.35 W m⁻² (b) 1.50 W m⁻² (c) 7.40 W m⁻² (d) 3.71 W m⁻²
10. A 1 000 ha forest stores 120 t of carbon per hectare. If a fire destroys half of it, the CO₂ released is about (1 t C = 3.67 t CO₂)
   (a) 220 000 t (b) 120 000 t (c) 60 000 t (d) 440 000 t
11. A river receives effluent at pH 3; downstream its pH is 5. The hydrogen-ion concentration has
   (a) increased 100 times (b) decreased 2 times (c) decreased 100 times (d) decreased 1 000 times
12. A crop field is abandoned. Annual weeds appear in year 1, grasses dominate by year 3, shrubs by year 10 and a sal forest by year 40. Biomass and soil organic matter
   (a) both fall (b) both rise (c) biomass rises while soil organic matter falls (d) biomass falls while soil organic matter rises

::: note Answers and explanations — Set C
**1.** (d) — 20 000 → 2 000 (primary) → **200 kJ** (secondary). Two steps multiply by 0.01.
**2.** (b) — Four transfers separate grass from hawk: 10 × 10⁴ = **100 000 kJ**. Option (a) allows only three.
**3.** (a) — The bloom raises oxygen by day, but when the algae die the bacteria decomposing them strip it and the fish suffocate — eutrophication.
**4.** (c) — Each level has fewer individuals (10⁶ > 2 × 10⁵ > 2 000 > 5), so the pyramid is upright.
**5.** (b) — 20 − 5 − 3 = **12 kg N per hectare per year**.
**6.** (d) — Soil and a seed bank survived, so recolonisation is fast; primary succession on bare rock takes centuries.
**7.** (a) — The chain begins with a living producer: a grazing (predator) chain. A detrital chain begins with dead matter.
**8.** (c) — 2 600 m is in the temperate belt (2 000–3 000 m), where oak, rhododendron and spruce dominate.
**9.** (d) — $\Delta F = 5.35 \ln 2 = 5.35 \times 0.693 = 3.71$ W m⁻²; the forcing depends on the ratio, not the absolute concentrations.
**10.** (a) — 1 000 × 120 × 0.5 = 60 000 t C; × 3.67 ≈ **220 000 t CO₂**.
**11.** (c) — pH 3 is 10⁻³ mol L⁻¹ and pH 5 is 10⁻⁵ mol L⁻¹: a fall by a factor of 100.
**12.** (b) — Biomass accumulates in the trees and soil organic matter from litter, so both rise.
:::

**Group D — Model answers for long questions (10 marks each, for deeper revision)**

1. Explain the structure and function of an ecosystem: energy flow, food chains, ecological pyramids and nutrient cycling. <span class="marks">[10]</span>
2. Describe ecological succession, the major vegetation types of Nepal and the attributes of a population. <span class="marks">[10]</span>

```photogrid label="6.H" cols="2" ratio="1.4" caption="Ecosystems. (a) A pond is a self-contained aquatic ecosystem with producers (algae, plants), consumers and decomposers. (b) A bee visiting a rose shows the interaction of pollinators and plants, a mutualism that sustains the food web."
@ photo id="ceebot/pond" cap="(a) Pond ecosystem"
fit 1.4
focus 0.5 0.5
@ photo id="ceebot/bee-rose" cap="(b) Plant-pollinator mutualism"
fit 1.4
focus 0.5 0.5
```

### Model answer D1: ecosystem structure, energy flow and nutrient cycling (10 marks)

**Introduction.** An **ecosystem** (Tansley, 1935) is a functional unit of nature consisting of the living community (biotic) and its non-living environment (abiotic), interacting with each other.

**Components.** (1) **Abiotic:** light, temperature, water, soil and minerals. (2) **Producers:** green plants and algae. (3) **Consumers:** primary (herbivores), secondary and tertiary (carnivores), and omnivores. (4) **Decomposers:** bacteria and fungi, which release minerals back.

**Energy flow.** The sun is the source, and only about $1\%$ of the incident light is fixed in photosynthesis. Energy flows in **one direction** (it is not recycled), and at each trophic level much is lost as heat in respiration.

1. **Gross primary productivity (GPP)** is the total organic matter made by producers. **Net primary productivity** $\text{NPP} = \text{GPP} - R$, the energy available to consumers.
2. **Lindeman's 10% law:** only about $10\%$ of the energy passes from one trophic level to the next.
3. **Food chain:** grass → grasshopper → frog → snake → eagle (grazing food chain). In a **detritus food chain** the dead matter is the start.
4. A **food web** is the network of interlinked food chains and gives stability.

**Ecological pyramids.**

| Pyramid | Shape in a grassland | Shape in a pond | Reason |
|---|---|---|---|
| Number | upright | may be inverted (a tree with many insects) | |
| Biomass | upright | inverted in the sea (phytoplankton) | |
| Energy | always upright | always upright | energy is lost at each step |

**Nutrient cycling.** Minerals move between the living and non-living in **biogeochemical cycles**. In the **carbon cycle** CO₂ is fixed in photosynthesis and returned by respiration, decay and burning. In the **nitrogen cycle**: nitrogen fixation (*Rhizobium*, *Azotobacter*, lightning), ammonification, nitrification (*Nitrosomonas* then *Nitrobacter*) and denitrification (*Pseudomonas*).

**Numerical.** If producers have $10\,000\ \text{kJ}$ of energy, the primary consumers get $1000\ \text{kJ}$, the secondary consumers $100\ \text{kJ}$ and the tertiary consumers $10\ \text{kJ}$. For GPP $= 20\,000$ and respiration $= 8000\ \text{kcal m}^{-2}\text{y}^{-1}$, $\text{NPP} = 12\,000$.

**Conclusion.** Energy flows in one direction and is lost at each step, while nutrients are cycled again and again.

### Model answer D2: succession, vegetation and populations (10 marks)

**Introduction.** **Ecological succession** is the orderly, gradual and predictable replacement of one community by another until a stable **climax community** is reached.

**Types and stages.**

1. **Primary succession** starts on a bare area with no soil (new rock, lava, a dry pond). **Pioneer** species (lichens and algae) are followed by mosses, herbs, shrubs and trees. Lichens secrete acids that weather the rock.
2. **Secondary succession** occurs where soil exists after a disturbance (an abandoned field, a fire), and is faster.
3. **Hydrosere** begins in water: phytoplankton → submerged → floating → reed swamp → sedge-meadow → woodland. **Xerosere** begins on dry rock.

During succession the biomass, species diversity and complexity rise, and the community modifies the environment so much that it favours the next seral stage.

**Vegetation of Nepal.** The altitude gives a range from tropical to alpine.

| Zone (altitude) | Vegetation |
|---|---|
| Tropical, Terai (below $1000$ m) | sal (*Shorea robusta*) forest, grasslands in Chitwan |
| Subtropical ($1000$ to $2000$ m) | *Schima-Castanopsis*, chir pine |
| Temperate ($2000$ to $3000$ m) | oak, rhododendron (the national flower, *lali gurans*) |
| Subalpine ($3000$ to $4000$ m) | fir, birch, juniper |
| Alpine (above $4000$ m) | alpine meadows and shrubs |

**Population attributes.** Natality, mortality, age structure, sex ratio and density. Growth is **exponential** ($\dfrac{dN}{dt} = rN$, J-shaped, in unlimited conditions) or **logistic** ($\dfrac{dN}{dt} = rN\left(\dfrac{K - N}{K}\right)$, S-shaped, with a carrying capacity $K$). Interactions: competition, predation, parasitism, mutualism, commensalism and amensalism.

**Biodiversity.** Nepal is only $0.1\%$ of the world's land but holds about $3\%$ of its flowering plants. It has protected areas (Chitwan, Sagarmatha) covering about $23\%$ of the land and is a biodiversity hotspot of the Himalaya.

**Numerical.** A population of $100$ with a growth rate $r = 0.1\ \text{per year}$ in exponential growth is $100e^{1} = 272$ after $10$ years. For logistic growth with $K = 1000$ and $N = 500$, $\dfrac{dN}{dt} = 0.1\times500\times0.5 = 25$ per year, the maximum rate.

**Conclusion.** Succession ends in a stable climax, and populations grow logistically up to the carrying capacity of the environment.
