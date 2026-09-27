---
subject: Biology
grade: 11
unit: 4
title: Ecology
hours: 11
area: Botany
---

Ecology is the study of the relationship between organisms and their
surroundings. At eleven hours this is the largest Botany unit after Floral
Diversity, and it is the one that connects biology to daily life in Nepal —
why a Chitwan grassland supports so many deer, why the Chure hills slip after
every monsoon, why *Mikania* is choking the sal forest. The unit works outward
from the single ecosystem to the ways plants fit themselves into harsh places,
and finally to what happens when the fit is broken.

::: key What the examiner asks from this unit
Two long questions come from here almost every year: **energy flow with the
ten per cent law**, or a **biogeochemical cycle (nitrogen or carbon) with a
labelled flow diagram**. Short questions favour the ecological pyramids,
xerophytic and hydrophytic adaptations, and named causes and effects of
ecological imbalance. Always give a **named Nepali example** — it is worth a
mark on its own.
:::

## 4.1 Ecosystem ecology

::: definition Ecosystem
An ecosystem is a self-regulating unit of nature in which the living organisms
of an area interact among themselves and with their non-living surroundings,
exchanging materials in cycles and energy in one direction. The term was coined
by **A. G. Tansley** in 1935.
:::

An ecosystem has no fixed size. A rain-filled hoof print, a paddy field in
Bhaktapur, Phewa Lake, the Chitwan sal forest and the whole biosphere are all
ecosystems. They are grouped as:

| Class | Sub-class | Nepali examples |
|---|---|---|
| Natural — terrestrial | forest, grassland, desert | sal forest of the Terai; *phanta* grassland of Shuklaphanta; trans-Himalayan desert of Mustang |
| Natural — aquatic | freshwater lentic (still), freshwater lotic (running), marine | Rara Lake; the Karnali river; none in Nepal (landlocked) |
| Artificial | crop field, orchard, aquarium, garden | paddy field, tea garden of Ilam, fish pond |

### Components of an ecosystem

**Abiotic components** are the non-living ones:

- *Climatic factors* — light, temperature, rainfall, humidity, wind, atmospheric
  pressure.
- *Edaphic factors* — soil texture, soil water, soil air, pH, topography.
- *Inorganic substances* — CO₂, O₂, N₂, water, and the mineral salts of
  nitrogen, phosphorus, potassium, calcium and sulphur, which move in cycles.
- *Organic substances* — proteins, carbohydrates, lipids and humus, which link
  the living to the non-living.

**Biotic components** are grouped by how they obtain food:

1. **Producers (autotrophs)** — green plants, algae, cyanobacteria and
   photosynthetic bacteria. They alone convert solar energy into chemical energy
   and bring it into the ecosystem.
2. **Consumers (heterotrophs / phagotrophs)** — primary consumers
   (herbivores: chital deer, grasshopper, rabbit), secondary consumers (primary
   carnivores: frog, jackal, snake), tertiary consumers (top carnivores: tiger,
   crested serpent eagle) and omnivores (humans, bear, crow).
3. **Decomposers (saprotrophs)** — bacteria and fungi, which break dead bodies
   and excreta into simple minerals and return them to the abiotic pool. Without
   them every nutrient cycle stops.

::: caution Decomposers are not "the lowest" level
Decomposers are not a fourth trophic level at the bottom of the chain. They draw
on **every** level — dead grass, dead deer and dead tiger alike — which is why
they are drawn to one side of a food web, not underneath it.
:::

### Food chain, food web and trophic levels

A **food chain** is a straight-line sequence along which food energy passes from
one organism to the next by eating. Each step is a **trophic (feeding) level**.
There are two kinds:

- **Grazing food chain (GFC)** — starts from living green plants.
  Grass → grasshopper → frog → snake → eagle (Terai grassland);
  phytoplankton → zooplankton → small fish → large fish (Phewa Lake).
- **Detritus food chain (DFC)** — starts from dead organic matter.
  Leaf litter → earthworm → frog → snake. In a forest the DFC actually carries
  **more** of the energy than the GFC, because most leaves are never eaten alive.

Food chains rarely have more than four or five links, because so much energy is
lost at each step. In nature the chains cross into a **food web**, which makes
the ecosystem stable: if the deer population crashes, the tiger can switch to
wild boar.

```figure caption="A simplified food web of a Terai grassland such as Chitwan. Each arrow points in the direction that energy travels — from the eaten to the eater."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.2, 3.4))

N = {}
def node(k, x, y, s, fc, w=2.70, h=0.82, fs=6.1):
    ax.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h,
                 boxstyle='round,pad=0,rounding_size=0.16',
                 fc=fc, ec=INK, lw=0.85, zorder=4))
    ax.text(x, y, s, fontsize=fs, ha='center', va='center', color=INK, zorder=5)
    N[k] = (x, y, w, h)

def link(a, b):
    x1, y1, w1, h1 = N[a]; x2, y2, w2, h2 = N[b]
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=0.9, alpha=0.9,
                                shrinkA=13, shrinkB=13, mutation_scale=8), zorder=3)

GRN='#d8ead8'; YEL='#f6ecd8'; BLU='#cfe3f3'; RED='#f6d7d5'
node('prod', 6.4, 0.9, 'PRODUCERS: grass, herbs, shrubs and sal saplings',
     GRN, w=8.2, h=0.9, fs=6.3)
node('hop', 1.5, 3.3, 'grasshopper', YEL)
node('deer', 4.8, 3.3, 'chital deer', YEL)
node('rat', 8.1, 3.3, 'field rat', YEL)
node('lang', 11.4, 3.3, 'langur monkey', YEL)
node('frog', 1.5, 5.7, 'frog', BLU)
node('pea', 4.8, 5.7, 'peacock', BLU)
node('jack', 9.2, 5.7, 'jackal', BLU)
node('snake', 5.0, 8.1, 'rat snake', BLU)
node('eag', 5.0, 10.5, 'crested serpent eagle', RED, w=3.3)
node('tig', 9.5, 10.5, 'Royal Bengal tiger', RED, w=3.1)
node('dec', 14.6, 5.7, 'DECOMPOSERS\nbacteria and fungi\nact on every level',
     '#e5d4ef', w=3.0, h=1.8, fs=6.0)

for t in ('hop', 'deer', 'rat', 'lang'):
    link('prod', t)
link('hop', 'frog'); link('hop', 'pea')
link('rat', 'jack'); link('rat', 'snake')
link('frog', 'snake'); link('snake', 'eag')
link('deer', 'tig'); link('pea', 'tig'); link('lang', 'tig'); link('jack', 'tig')

ax.annotate('', xy=(13.05, 5.2), xytext=(10.55, 1.2),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.8, ls=(0, (2.5, 2)),
                            mutation_scale=8), zorder=2)
ax.annotate('', xy=(13.6, 6.65), xytext=(11.1, 10.2),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.8, ls=(0, (2.5, 2)),
                            mutation_scale=8), zorder=2)

for y, s in [(0.9, 'T₁'), (3.3, 'T₂'), (5.7, 'T₃'), (8.1, 'T₄'), (10.5, 'T₅')]:
    ax.text(-0.9, y, s, fontsize=7.4, ha='center', va='center', color=MUTED)
ax.text(-0.9, 11.5, 'trophic\nlevel', fontsize=6.0, ha='center', va='center', color=MUTED)
ax.set_xlim(-1.7, 16.5); ax.set_ylim(0.1, 12.0)
ax.axis('off')
```
### Energy flow and the ten per cent law

Energy enters an ecosystem only as sunlight and leaves it only as heat. Two laws
of thermodynamics govern the journey. By the **first law**, energy is neither
created nor destroyed — it is only converted from light to chemical to heat. By
the **second law**, every conversion wastes some energy as heat, so the flow is
**one-way (unidirectional)** and never cyclic.

Of the sunlight falling on a green leaf, only about **50 %** is
photosynthetically active radiation, and green plants fix only about **1 %** of
that as gross primary production. Thereafter, **Lindeman's ten per cent law**
(R. L. Lindeman, 1942) applies.

::: key Lindeman's ten per cent law
Only about **10 %** of the energy stored at one trophic level is passed on to the
next; the other 90 % is lost as respiratory heat, in undigested matter and in the
parts that are never eaten. This is why food chains are short and why top
carnivores are always few.
:::

```figure caption="Unidirectional flow of energy through a grassland ecosystem, in kJ m⁻² yr⁻¹. At every step about 90 % of the energy is lost, which is Lindeman's ten per cent law."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.2, 3.0))

def box(xc, yc, w, h, s, fc, fs=6.2):
    ax.add_patch(FancyBboxPatch((xc-w/2, yc-h/2), w, h,
                 boxstyle='round,pad=0,rounding_size=0.15',
                 fc=fc, ec=INK, lw=0.95, zorder=4))
    ax.text(xc, yc, s, fontsize=fs, ha='center', va='center', color=INK, zorder=5)

xs = [2.9, 8.1, 13.3, 18.2]
W  = 3.9
names = ['PRODUCERS\ngrass\n10 000', 'HERBIVORES\ndeer, grasshopper\n1 000',
         'CARNIVORES\nsnake, jackal\n100', 'TOP CARNIVORE\ntiger, eagle\n10']
cols  = ['#d8ead8', '#f6ecd8', '#cfe3f3', '#f6d7d5']
hs    = [2.50, 2.00, 1.55, 1.15]

ax.text(2.9, 9.7, 'SUNLIGHT   1 000 000', fontsize=7.0, ha='center', color='#b8860b')
ax.annotate('', xy=(2.9, 7.95), xytext=(2.9, 9.3),
            arrowprops=dict(arrowstyle='-|>', color='#b8860b', lw=1.5, mutation_scale=11))
ax.text(3.4, 8.6, 'only ≈ 1 % is fixed', fontsize=6.1, ha='left', va='center', color='#b8860b')

for x, n, c, h in zip(xs, names, cols, hs):
    box(x, 6.6, W, h, n, c)

for k in range(3):
    x0 = xs[k] + W/2 + 0.05
    x1 = xs[k+1] - W/2 - 0.05
    ax.annotate('', xy=(x1, 6.6), xytext=(x0, 6.6),
                arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.7, mutation_scale=11))
    ax.text((x0+x1)/2, 7.25, '10 %', fontsize=6.8, ha='center', color=ACCENT)

for x, h, loss in zip(xs, hs, ['9 000', '900', '90', '9']):
    ax.annotate('', xy=(x, 4.30), xytext=(x, 6.6-h/2-0.05),
                arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.2, mutation_scale=9))
    ax.text(x, 4.00, 'heat lost in\nrespiration\n' + loss, fontsize=5.9, ha='center',
            va='top', color='#d9534f')

box(10.55, 1.35, 17.5, 1.15,
    'DECOMPOSERS — bacteria and fungi act on the dead bodies and excreta of every level,\n'
    'releasing the last of the energy as heat and returning the minerals to the soil',
    '#e5d4ef', fs=6.1)
for x in xs:
    ax.annotate('', xy=(x, 1.95), xytext=(x, 2.95),
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.85,
                                ls=(0, (2.5, 2)), mutation_scale=8))
ax.text(21.3, 6.6, 'energy leaves\nthe ecosystem\nas heat and\nnever returns',
        fontsize=6.1, ha='center', va='center', color=MUTED)
ax.set_xlim(0.3, 23.4); ax.set_ylim(0.3, 10.3)
ax.axis('off')
```
**Productivity** measures how fast energy is stored.

::: definition Primary productivity
*Gross primary productivity* (GPP) is the total organic matter fixed by producers
per unit area per unit time. Part of it is burnt in the plant's own respiration
(R). What is left is *net primary productivity* (NPP), the food actually
available to consumers:

$$ \text{NPP} = \text{GPP} - R $$

*Secondary productivity* is the rate at which consumers store energy. Productivity
is measured in g m⁻² yr⁻¹ or kJ m⁻² yr⁻¹, whereas **standing crop** is the
biomass present at one moment, in g m⁻².
:::

::: example Worked example 4.1
**Problem.** The producers of a grassland fix $20{,}000\ \text{kJ m}^{-2}\ \text{yr}^{-1}$.
Using the ten per cent law, find the energy available to the herbivores, to the
carnivores and to the top carnivores, and the total energy lost as heat between
the producer and the top-carnivore levels.

**Solution.** Each level receives one tenth of the previous one:

$$ E_2 = 0.10 \times 20{,}000 = 2000\ \text{kJ m}^{-2}\ \text{yr}^{-1} $$
$$ E_3 = 0.10 \times 2000 = 200\ \text{kJ m}^{-2}\ \text{yr}^{-1} $$
$$ E_4 = 0.10 \times 200 = 20\ \text{kJ m}^{-2}\ \text{yr}^{-1} $$

Energy lost as heat is the difference between what enters a level and what leaves
it:

$$ \text{loss} = (20{,}000-2000) + (2000-200) + (200-20) = 18{,}000 + 1800 + 180 $$

$$ = 19{,}980\ \text{kJ m}^{-2}\ \text{yr}^{-1} $$

That is 99.9 % of the producers' energy — the tiger lives on the last 0.1 %.
:::

::: example Worked example 4.2
**Problem.** In one year a hectare of sal forest fixes a gross primary production
of $12{,}000\ \text{kJ m}^{-2}$ and uses $7500\ \text{kJ m}^{-2}$ in its own
respiration. Calculate the net primary productivity and express it as a
percentage of GPP.

**Solution.**

$$ \text{NPP} = \text{GPP} - R = 12{,}000 - 7500 = 4500\ \text{kJ m}^{-2}\ \text{yr}^{-1} $$

$$ \frac{\text{NPP}}{\text{GPP}} \times 100 = \frac{4500}{12{,}000} \times 100 = 37.5\ \% $$

Only 37.5 % of what the forest fixes is available to every animal and decomposer
in it; a forest spends more on respiration than a crop field does because it
carries a large mass of non-photosynthetic wood.
:::

### Ecological pyramids

An **ecological pyramid** (Charles Elton, 1927) is a graphical model in which
each trophic level is drawn as a horizontal bar whose length is proportional to
the number, the biomass or the energy at that level. Producers form the base.

```figure caption="The three ecological pyramids. Pyramids of number and of biomass may be inverted; the pyramid of energy is always upright, because energy can only be lost upwards."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon
fig, axes = plt.subplots(2, 2, figsize=(5.0, 3.8),
                         gridspec_kw=dict(hspace=0.75, wspace=0.28))

COLS = ['#d8ead8', '#f6ecd8', '#cfe3f3', '#f6d7d5']

def pyramid(ax, widths, labels, title, sub, subcol):
    for i, (w, lab) in enumerate(zip(widths, labels)):
        y0 = i*1.0
        ax.add_patch(Polygon([(-w/2, y0), (w/2, y0), (w/2, y0+0.86), (-w/2, y0+0.86)],
                     closed=True, fc=COLS[i % 4], ec=INK, lw=0.85))
        ax.text(2.6, y0+0.43, lab, fontsize=5.6, ha='left', va='center', color=INK)
    ax.set_title(title, fontsize=6.5, pad=4)
    ax.text(-2.4, -0.72, sub, fontsize=6.1, ha='left', va='center', color=subcol)
    ax.set_xlim(-2.6, 12.4); ax.set_ylim(-1.30, len(widths)*1.0 + 0.10)
    ax.axis('off')

pyramid(axes[0][0], [4.6, 2.4, 1.15, 0.45],
        ['grass   10⁶', 'grasshoppers   10⁴', 'frogs   10³', 'snakes   10²'],
        '(a)  Numbers — grassland', 'UPRIGHT', '#2e8b57')

pyramid(axes[0][1], [0.55, 4.4, 1.8, 3.3],
        ['one big tree   1', 'leaf-eating\ninsects   10⁴',
         'insect-eating\nbirds   10²', 'parasites and\nhyperparasites   10⁵'],
        '(b)  Numbers — one tree', 'INVERTED (spindle)', '#d9534f')

pyramid(axes[1][0], [0.75, 4.0, 2.1],
        ['phytoplankton\n4 g m⁻²', 'zooplankton\n21 g m⁻²', 'small fish\n11 g m⁻²'],
        '(c)  Biomass — a pond', 'INVERTED', '#d9534f')

pyramid(axes[1][1], [4.6, 2.3, 1.0, 0.42],
        ['producers   10 000', 'herbivores   1000', 'carnivores   100',
         'top carnivore   10'],
        '(d)  Energy (kJ m⁻² yr⁻¹)', 'ALWAYS UPRIGHT', '#2e8b57')
```
| Pyramid | What the bar measures | Grassland | Pond | Single tree |
|---|---|---|---|---|
| Number | individuals per unit area | upright | upright | **inverted** (spindle) |
| Biomass | dry weight per unit area | upright | **inverted** | upright |
| Energy | energy fixed per unit area per unit time | upright | upright | upright |

::: caution Why the pond's biomass pyramid is inverted
The phytoplankton of a pond weigh less at any one moment than the zooplankton
feeding on them — but they **reproduce far faster**, so over a year they produce
far more. A pyramid of biomass is a snapshot; a pyramid of energy is a rate, and
a rate can never be inverted without breaking the second law of thermodynamics.
:::

### Population attributes

A **population** is a group of individuals of one species living in a defined
area. Its measurable attributes are **density** (individuals per unit area),
**natality** (birth rate), **mortality** (death rate), **immigration**,
**emigration** and **age structure**.

$$ \text{Density } D = \frac{N}{A}, \qquad
\text{Frequency } F = \frac{\text{quadrats in which the species occurs}}{\text{total quadrats}} \times 100 $$

When resources are unlimited a population grows **exponentially**, giving a
J-shaped curve:

$$ \frac{dN}{dt} = rN \qquad \Longrightarrow \qquad N_t = N_0\,e^{rt} $$

where $r$ is the intrinsic rate of natural increase. In the real world food and
space run out, and growth becomes **logistic**, giving an S-shaped (sigmoid)
curve that levels off at the **carrying capacity** $K$:

$$ \frac{dN}{dt} = rN\left(\frac{K-N}{K}\right) $$

::: example Worked example 4.3
**Problem.** A student lays 20 quadrats, each $1\ \text{m}^{2}$, in a Shivapuri
grassland. *Imperata cylindrica* occurs in 15 of them, and 240 shoots are counted
altogether. Calculate its density, frequency and abundance.

**Solution.**

$$ \text{Density} = \frac{\text{total individuals}}{\text{total quadrats studied}}
= \frac{240}{20} = 12\ \text{shoots m}^{-2} $$

$$ \text{Frequency} = \frac{15}{20} \times 100 = 75\ \% $$

$$ \text{Abundance} = \frac{\text{total individuals}}{\text{quadrats of occurrence}}
= \frac{240}{15} = 16\ \text{shoots per occupied quadrat} $$
:::

::: example Worked example 4.4
**Problem.** A protected population of 1000 chital deer grows exponentially with
$r = 0.20\ \text{yr}^{-1}$. What will the population be after 5 years?
Take $e = 2.718$.

**Solution.**

$$ N_t = N_0\,e^{rt} = 1000 \times e^{0.20 \times 5} = 1000 \times e^{1} $$

$$ = 1000 \times 2.718 = 2718\ \text{deer} $$

The population has nearly trebled in five years — which is why a fenced reserve
must either expand or cull, since $K$ is fixed.
:::

### Biogeochemical cycles

Energy flows through an ecosystem and is lost; **matter moves in circles and is
reused**. The circular path of a chemical element from the abiotic pool through
the living world and back is a **biogeochemical cycle**. Cycles whose reservoir
is the atmosphere (carbon, nitrogen, oxygen) are **gaseous cycles**; those whose
reservoir is rock (phosphorus, sulphur, calcium) are **sedimentary cycles**.

```figure caption="The nitrogen cycle. Nitrogen gas is useless to plants until it is fixed; it returns to the air only by denitrification. The bacteria responsible for each step are named."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.2, 3.4))

def box(xc, yc, w, h, s, fc, fs=6.2):
    ax.add_patch(FancyBboxPatch((xc-w/2, yc-h/2), w, h,
                 boxstyle='round,pad=0,rounding_size=0.16',
                 fc=fc, ec=INK, lw=0.95, zorder=4))
    ax.text(xc, yc, s, fontsize=fs, ha='center', va='center', color=INK, zorder=5)

def arr(x1, y1, x2, y2, col=ACCENT, lw=1.25):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='-|>', color=col, lw=lw, mutation_scale=10),
                zorder=3)

box(9.0, 10.6, 12.6, 1.0, 'ATMOSPHERIC NITROGEN   N₂   (78 % of the air)', '#cfe3f3', fs=6.9)
box(2.6, 7.2, 3.3, 1.05, 'ammonia / ammonium\nNH₃ · NH₄⁺', '#f6ecd8', fs=6.0)
box(2.6, 4.6, 3.3, 1.05, 'nitrite\nNO₂⁻', '#f6ecd8')
box(2.6, 2.0, 3.3, 1.05, 'nitrate\nNO₃⁻', '#f6ecd8')
box(9.0, 2.0, 3.8, 1.25, 'PLANT PROTEINS\nassimilated in roots\nand leaves', '#d8ead8', fs=6.0)
box(14.6, 2.0, 3.0, 1.15, 'ANIMAL\nPROTEINS', '#f6d7d5')
box(14.6, 7.2, 3.4, 1.55, 'DEAD BODIES,\nEXCRETA AND\nLEAF LITTER', '#e5d4ef', fs=6.0)

# 1 fixation
arr(5.2, 10.1, 3.1, 7.8, '#2e8b57')
ax.text(5.9, 9.1, 'nitrogen fixation by Rhizobium,\nAzotobacter and Anabaena,\nand by lightning',
        fontsize=5.9, ha='left', va='center', color='#2e8b57')
# 2 nitrification ladder
arr(2.6, 6.65, 2.6, 5.18)
ax.text(3.0, 5.92, 'Nitrosomonas', fontsize=5.9, ha='left', va='center', color=ACCENT)
arr(2.6, 4.05, 2.6, 2.58)
ax.text(3.0, 3.32, 'Nitrobacter', fontsize=5.9, ha='left', va='center', color=ACCENT)
ax.plot([5.55, 5.55], [2.9, 6.5], color='#2e8b57', lw=0.8)
ax.text(5.75, 4.7, 'NITRIFICATION', fontsize=6.1, rotation=90, ha='center',
        va='center', color='#2e8b57')
# 3 uptake and feeding
arr(4.30, 2.0, 7.05, 2.0)
ax.text(5.68, 2.50, 'absorbed\nby roots', fontsize=5.9, ha='center', va='center', color=ACCENT)
arr(10.95, 2.0, 13.05, 2.0)
ax.text(12.0, 2.45, 'eaten', fontsize=5.9, ha='center', va='center', color=ACCENT)
arr(14.6, 2.62, 14.6, 6.38)
ax.text(15.0, 4.5, 'death and\nexcretion', fontsize=5.9, ha='left', va='center', color=ACCENT)
arr(9.9, 2.68, 12.75, 6.45)
ax.text(10.2, 4.5, 'litter\nfall', fontsize=5.9, ha='left', va='center', color=ACCENT)
# 4 ammonification
arr(12.85, 7.2, 4.30, 7.2, '#b8860b')
ax.text(8.6, 7.85, 'ammonification by decomposer bacteria and fungi',
        fontsize=5.9, ha='center', va='center', color='#b8860b')
# 5 denitrification routed down the far left
ax.plot([0.95, 0.30], [2.0, 2.0], color='#d9534f', lw=1.25, zorder=3)
ax.plot([0.30, 0.30], [2.0, 10.6], color='#d9534f', lw=1.25, zorder=3)
arr(0.30, 10.6, 2.60, 10.6, '#d9534f')
ax.text(-0.10, 6.3, 'denitrification — Pseudomonas denitrificans',
        fontsize=5.8, rotation=90, ha='center', va='center', color='#d9534f')
ax.set_xlim(-0.6, 17.0); ax.set_ylim(0.6, 11.5)
ax.axis('off')
```
The four steps of the nitrogen cycle are worth learning as a sequence:

1. **Nitrogen fixation** — N₂ → NH₃. Done biologically by free-living
   *Azotobacter* and *Clostridium*, symbiotic *Rhizobium leguminosarum* in the
   root nodules of lentil, soybean and gram, and *Anabaena* in the leaf cavities
   of *Azolla*; physically by lightning; industrially by the Haber process.
2. **Ammonification** — decomposer bacteria and fungi convert the nitrogen of
   dead bodies and urea back into ammonia.
3. **Nitrification** — NH₄⁺ → NO₂⁻ by *Nitrosomonas*, then NO₂⁻ → NO₃⁻ by
   *Nitrobacter*. Only now is the nitrogen in the form roots absorb.
4. **Denitrification** — NO₃⁻ → N₂ by *Pseudomonas denitrificans* and
   *Thiobacillus denitrificans* in waterlogged soil. This is the only route back
   to the atmosphere, and it is why paddy soils lose fertiliser nitrogen.

```figure caption="The carbon cycle. Photosynthesis is the only large route into the living world; respiration, decomposition and the combustion of fossil fuels are the routes out."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.2, 3.2))

def box(xc, yc, w, h, s, fc, fs=6.2):
    ax.add_patch(FancyBboxPatch((xc-w/2, yc-h/2), w, h,
                 boxstyle='round,pad=0,rounding_size=0.16',
                 fc=fc, ec=INK, lw=0.95, zorder=4))
    ax.text(xc, yc, s, fontsize=fs, ha='center', va='center', color=INK, zorder=5)

def arr(x1, y1, x2, y2, col=ACCENT, lw=1.25, style='-|>'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=col, lw=lw, mutation_scale=10),
                zorder=3)

box(9.0, 10.0, 15.0, 1.0, 'CARBON DIOXIDE IN THE ATMOSPHERE   (≈ 0.04 % of the air)',
    '#cfe3f3', fs=6.9)
box(3.0, 5.4, 3.4, 1.5, 'PRODUCERS\ngreen plants and\nphytoplankton', '#d8ead8', fs=6.0)
box(8.6, 5.4, 3.4, 1.5, 'CONSUMERS\nherbivores and\ncarnivores', '#f6ecd8', fs=6.0)
box(6.0, 1.6, 5.4, 1.3, 'DEAD ORGANIC MATTER\nbroken down by decomposers', '#e5d4ef', fs=6.0)
box(13.6, 1.6, 3.6, 1.5, 'FOSSIL FUELS\ncoal, petroleum,\nnatural gas', '#f2c9a0', fs=6.0)
box(15.6, 5.4, 3.2, 1.5, 'OCEANS\ndissolved CO₂,\ncarbonates, shells', '#bcd9ea', fs=6.0)

arr(2.4, 9.45, 2.4, 6.20, '#2e8b57', lw=1.5)
ax.text(2.7, 8.3, 'photosynthesis', fontsize=6.1, ha='left', va='center', color='#2e8b57')
arr(4.2, 6.20, 4.2, 9.45, '#d9534f')
ax.text(4.5, 7.2, 'respiration', fontsize=6.1, ha='left', va='center', color='#d9534f')
arr(4.75, 5.4, 6.85, 5.4)
ax.text(5.80, 5.90, 'feeding', fontsize=6.0, ha='center', va='center', color=ACCENT)
arr(9.0, 6.20, 9.0, 9.45, '#d9534f')
ax.text(9.3, 8.3, 'respiration', fontsize=6.1, ha='left', va='center', color='#d9534f')
arr(3.4, 4.60, 4.7, 2.30)
ax.text(0.9, 3.20, 'litter fall', fontsize=6.0, ha='left', va='center', color=ACCENT)
arr(8.4, 4.60, 7.3, 2.30)
ax.text(9.0, 3.40, 'death and excreta', fontsize=6.0, ha='left', va='center', color=ACCENT)
# decomposition, routed down the far left
ax.plot([3.25, 0.50], [1.6, 1.6], color='#d9534f', lw=1.25, zorder=3)
ax.plot([0.50, 0.50], [1.6, 10.0], color='#d9534f', lw=1.25, zorder=3)
arr(0.50, 10.0, 1.55, 10.0, '#d9534f')
ax.text(0.10, 6.0, 'decomposition returns CO₂', fontsize=5.8, rotation=90,
        ha='center', va='center', color='#d9534f')
arr(8.75, 1.6, 11.75, 1.6)
ax.text(10.25, 2.55, 'fossilisation over\nmillions of years', fontsize=5.9,
        ha='center', va='center', color=ACCENT)
arr(12.6, 2.40, 12.6, 9.45, '#d9534f')
ax.text(12.9, 7.2, 'combustion of fuel —\nthe human contribution', fontsize=6.0,
        ha='left', va='center', color='#d9534f')
arr(15.8, 6.20, 15.8, 9.45, MUTED, style='<|-|>')
ax.text(16.1, 7.8, 'diffusion', fontsize=6.0, ha='left', va='center', color=MUTED)
ax.set_xlim(-0.4, 18.9); ax.set_ylim(0.5, 11.0)
ax.axis('off')
```
### Ecological succession

::: definition Ecological succession
Ecological succession is the orderly, progressive and predictable replacement of
one community by another at the same site, until a stable, self-perpetuating
**climax community** in equilibrium with the climate is reached.
:::

The first community to arrive is the **pioneer community**; each intermediate
community is a **seral stage** and the whole series is a **sere**. Succession is
**primary** when it begins on a bare surface that never carried life (a new
landslide scar in Sindhupalchok, cooled lava, a fresh sandbar of the Koshi), and
**secondary** when it restarts on a site that was stripped of its community but
still has soil (an abandoned *bari* field, a burnt forest). Secondary succession
is far faster, because the soil and its seed bank already exist.

A succession that begins in water is a **hydrosere**; one that begins on bare
rock is a **xerosere**. Both converge on the same mesic forest climax.

```figure caption="Hydrosere — the six seral stages by which an oxbow lake of the Terai silts up and becomes forest. Each community makes the site less suitable for itself and more suitable for the next."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.2, 3.2))

x = np.linspace(0, 13.0, 400)
bed = 1.0 + 3.05*(x/13.0)**2.1                      # rising silt bed
ax.fill_between(x, 0.0, bed, color='#e4d7bf', zorder=2)
ax.plot(x, bed, color='#a98f63', lw=1.0, zorder=3)
water = np.where(bed < 4.05, 4.05, bed)
ax.fill_between(x, bed, water, color='#cfe3f3', zorder=1)
ax.plot([0, 13.0], [4.05, 4.05], color='#1d6fb8', lw=0.9, zorder=3)

rng = np.random.default_rng(3)
# 1 phytoplankton
for _ in range(26):
    ax.add_patch(Circle((rng.uniform(0.3, 2.0), rng.uniform(1.4, 3.9)), 0.055,
                 fc='#2e8b57', ec='none', zorder=4))
# 2 submerged
for xx in np.linspace(2.5, 4.0, 6):
    yy = np.linspace(np.interp(xx, x, bed), 3.75, 40)
    ax.plot(xx + 0.13*np.sin(np.linspace(0, 8, 40)), yy, color='#2e8b57', lw=0.8, zorder=4)
# 3 rooted floating
for xx in (4.6, 5.3, 6.0):
    ax.plot([xx, xx], [np.interp(xx, x, bed), 4.05], color='#2e8b57', lw=0.8, zorder=4)
    ax.add_patch(Polygon([(xx-0.36, 4.05), (xx+0.36, 4.05), (xx+0.30, 4.22), (xx-0.30, 4.22)],
                 closed=True, fc='#8fc08f', ec=INK, lw=0.6, zorder=5))
# 4 reed swamp
for xx in np.linspace(6.6, 8.0, 6):
    b = np.interp(xx, x, bed)
    ax.plot([xx, xx], [b, b+1.55], color='#2e8b57', lw=1.0, zorder=4)
    ax.add_patch(Polygon([(xx-0.07, b+1.55), (xx+0.07, b+1.55), (xx, b+1.95)],
                 closed=True, fc='#b8860b', ec='none', zorder=4))
# 5 sedge meadow
for xx in np.linspace(8.6, 10.0, 9):
    b = np.interp(xx, x, bed)
    for d in (-0.10, 0.0, 0.10):
        ax.plot([xx, xx+d*3], [b, b+0.75], color='#6aa84f', lw=0.7, zorder=4)
# 6 woodland then climax forest
for xx, ht in [(10.7, 1.15), (11.4, 1.65), (12.2, 2.2), (12.8, 1.8)]:
    b = np.interp(xx, x, bed)
    ax.plot([xx, xx], [b, b+ht*0.55], color='#7a5a33', lw=1.5, zorder=4)
    ax.add_patch(Circle((xx, b+ht*0.82), ht*0.36, fc='#8fc08f', ec=INK, lw=0.6, zorder=5))

labels = [(1.1, '1. phytoplankton\n(pioneer)'), (3.2, '2. rooted\nsubmerged'),
          (5.3, '3. rooted\nfloating'), (7.3, '4. reed\nswamp'),
          (9.3, '5. sedge\nmeadow'), (11.9, '6. woodland →\nclimax forest')]
for xx, s in labels:
    ax.text(xx, -0.25, s, fontsize=5.9, ha='center', va='top', color=INK)
    ax.plot([xx, xx], [-0.05, 0.12], color=MUTED, lw=0.6)

ax.annotate('', xy=(12.9, 6.55), xytext=(0.3, 6.55),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.4, mutation_scale=11))
ax.text(6.6, 6.95, 'direction of succession — the pond silts up and shallows with time',
        fontsize=6.3, ha='center', color=ACCENT)
ax.text(0.3, 4.35, 'water surface', fontsize=5.9, ha='left', color='#1d6fb8')
ax.text(11.6, 0.55, 'silt and humus', fontsize=5.9, ha='center', color='#8a7350')
ax.set_xlim(-0.3, 14.1); ax.set_ylim(-2.0, 7.4)
ax.axis('off')
```

| Sere | Starts on | Pioneer | Order of seral stages | Climax |
|---|---|---|---|---|
| Hydrosere | open water | phytoplankton | submerged → rooted floating → reed swamp → sedge meadow → woodland | mesic forest |
| Xerosere | bare rock | crustose lichen | foliose lichen → moss → herb → shrub → woodland | mesic forest |

::: memory Seral stages of a xerosere
**Crusty Foliage Makes Her Shoes Filthy** — **C**rustose lichen, **F**oliose
lichen, **M**oss, **H**erb, **S**hrub, **F**orest (climax).
:::

## 4.2 Ecological adaptation

::: definition Adaptation
Adaptation is any inherited change in the form, structure, physiology or
behaviour of an organism that fits it to survive and reproduce in a particular
habitat. Adaptations are the result of natural selection acting over many
generations, not of an individual's effort within its lifetime.
:::

Plants are grouped by the water available in their habitat.

### Hydrophytes — plants of water

| Sub-type | Position | Examples |
|---|---|---|
| Free floating | float on the surface, roots hang free | *Eichhornia crassipes*, *Pistia stratiotes*, *Lemna*, *Wolffia* |
| Rooted floating | rooted in mud, leaves on the surface | *Nelumbo nucifera* (lotus), *Nymphaea*, *Trapa* |
| Rooted submerged | wholly under water | *Hydrilla verticillata*, *Vallisneria* |
| Free submerged | under water, not rooted | *Ceratophyllum*, *Utricularia* |
| Amphibious | part in, part out of water | *Typha*, *Ranunculus*, paddy |

Their problem is not water but **oxygen, support and anchorage**, so:

- roots are poorly developed or absent, with no root hairs and only a root pocket
  instead of a root cap;
- stems and petioles are soft, flexible and spongy, so the current bends them
  instead of breaking them;
- the cortex contains large air chambers, **aerenchyma**, which store oxygen and
  give buoyancy;
- the cuticle is very thin or absent, and the epidermis itself contains
  chloroplasts and absorbs water and minerals directly;
- stomata are **absent** in submerged leaves, and confined to the upper surface
  (**epistomatic**) in floating leaves such as the lotus;
- submerged leaves are thin, ribbon-like or finely dissected, which increases the
  surface for gas exchange and reduces drag;
- mechanical and vascular tissue is much reduced, since water supports the plant;
- reproduction is largely **vegetative**, by runners, offsets and turions.

### Xerophytes — plants of dry places

| Sub-type | Strategy | Examples |
|---|---|---|
| Ephemerals ("drought escapers") | complete the whole life cycle in a few weeks of rain | *Argemone*, *Tribulus* |
| Succulents | store water in swollen stems or leaves | *Opuntia*, *Euphorbia royleana* (*siundi*), *Aloe vera* |
| Non-succulent perennials | endure drought by cutting losses | *Casuarina*, *Nerium oleander*, *Calotropis*, *Acacia catechu* (*khayar*) |

Adaptations run in two directions — get more water, lose less:

- roots are long, much branched and deep, often reaching the water table;
- stems are woody, covered with wax or hair; in *Opuntia* the flattened green
  stem is a **phylloclade** that does the photosynthesis;
- leaves are small, leathery, or reduced to spines and scales, cutting the
  transpiring surface; in *Acacia* the petiole flattens into a **phyllode**;
- the cuticle is very thick, and the epidermis is multilayered with a
  sclerenchymatous **hypodermis**;
- stomata are few, **sunken** in pits lined with hairs, so that a still, humid
  layer of air sits over the pore;
- many succulents use **CAM** photosynthesis — the stomata open at night to take
  in CO₂ as an organic acid, and stay shut through the hot day.

### Other ecological groups

- **Mesophytes** — ordinary land plants of moderate water, such as mango, maize
  and rose; they have well-developed roots, broad thin leaves, normal cuticle and
  stomata on both surfaces.
- **Halophytes** — plants of saline soil and tidal mud, such as *Rhizophora* and
  *Avicennia*. They have breathing roots (**pneumatophores**) with lenticel-like
  pores, stilt roots, salt-secreting glands, succulent leaves, and **viviparous
  germination**, in which the seed germinates while still on the parent.
- **Epiphytes** — plants that perch on another plant for support only, such as
  the orchids *Vanda* and *Dendrobium* common on Nepal's mid-hill trees. Clinging
  roots grip the bark and hanging aerial roots carry a spongy sheath of dead
  cells, the **velamen**, which soaks up rain and dew.
- **High-altitude plants** of Nepal's alpine zone — *Saussurea gossypiphora*, the
  snowball plant, wraps itself in dense white wool that traps heat and blocks
  ultraviolet light; cushion plants such as *Arenaria* grow as tight hemispheres
  that hold a warm still layer of air near the ground.

::: tip Answer structure for an adaptation question
Answer under three fixed headings — **morphological** (root, stem, leaf),
**anatomical** (cuticle, epidermis, stomata, aerenchyma or sclerenchyma) and
**physiological** (CAM, osmotic concentration, vegetative reproduction). Give a
scientific name for each point. Examiners tick headings, not prose.
:::

## 4.3 Ecological imbalances

::: definition Ecological imbalance
Ecological imbalance is a disturbance of the natural equilibrium between the
biotic and abiotic components of an ecosystem, in which the rate of destruction
of a resource exceeds the rate at which the ecosystem can replace it.
:::

### Causes

1. **Population growth.** Nepal's population has roughly trebled since 1961, and
   every extra household needs fuelwood, fodder and land.
2. **Deforestation.** Clearing for cultivation, settlement, timber and fuelwood.
   The Terai lost much of its forest to resettlement after malaria was controlled
   in the 1960s.
3. **Overgrazing** on the mid-hill and alpine pastures removes the ground cover
   that holds the soil.
4. **Unplanned urbanisation and industrialisation**, which replace farmland with
   concrete and put untreated effluent into rivers such as the Bagmati.
5. **Pollution** of air, water and soil, including pesticide residues.
6. **Quarrying of the Chure (Siwalik) hills** for boulders, sand and gravel. The
   Chure is young, loose sedimentary rock; stripping it lowers the Terai water
   table and sends floods and debris onto farmland below.
7. **Invasive alien species.** *Mikania micrantha* (*lahare banmara*) is
   smothering the sal forest and grassland of Chitwan; *Lantana camara*,
   *Parthenium hysterophorus* and the water hyacinth *Eichhornia crassipes*,
   which blankets Phewa Lake, do the same on land and water.
8. **Overexploitation** — poaching of rhinoceros and tiger, and uncontrolled
   collection of medicinal herbs such as *yarsagumba* (*Ophiocordyceps
   sinensis*) and *Nardostachys jatamansi*.

### Consequences

| Problem | Chief cause | Effect |
|---|---|---|
| Greenhouse effect and global warming | CO₂, CH₄, N₂O and CFCs trap outgoing infrared radiation | rising temperature, retreating glaciers, glacial lake outburst floods |
| Ozone layer depletion | chlorofluorocarbons release Cl atoms that destroy O₃ | more ultraviolet-B reaches the ground; skin cancer, cataract, reduced crop yield |
| Acid rain | SO₂ and NOₓ dissolve to give H₂SO₄ and HNO₃; rain pH falls below 5.6 | leaches soil nutrients, kills fish, corrodes buildings |
| Eutrophication | fertiliser and sewage enrich water with nitrate and phosphate | algal bloom → decomposition → oxygen falls → fish die |
| Biomagnification | non-degradable pesticides such as DDT | concentration multiplies at each trophic level; eggshells of fish-eating birds thin |
| Soil erosion and landslides | loss of vegetation cover on steep slopes | loss of topsoil, silting of rivers and reservoirs |
| Loss of biodiversity | habitat destruction, poaching, invasive species | species extinction and narrower gene pools |

Nepal shows all of these. Himalayan glaciers are retreating; the 1985 outburst of
**Dig Tsho** above Thame destroyed the almost-finished Namche hydropower plant,
and **Imja Tsho** and **Tsho Rolpa** are now monitored and partly drained for the
same reason. The June 2021 **Melamchi flood** carried away bridges and intake
works after debris built up in the upper catchment. Kathmandu's winter air
regularly exceeds the WHO guideline for fine particulate matter.

### Control measures

- **Afforestation and reforestation**, especially on degraded Chure slopes.
- **Community forestry.** More than 22,000 community forest user groups now
  manage a large share of Nepal's hill forest, and forest cover has risen again
  to about **45 % of the country** (forest plus other wooded land,
  Forest Resource Assessment 2015).
- **Soil conservation** — terracing, contour bunding, check dams, gully plugging
  and agroforestry.
- **Pollution control** — treatment of sewage and industrial effluent,
  Euro-standard vehicle emission norms, promotion of electric vehicles, biogas
  and improved cooking stoves in place of firewood.
- **Legal and institutional measures** — the Environment Protection Act, the
  Forest Act, compulsory Environmental Impact Assessment for large projects, and
  the national protected-area network described in Unit 5.
- **Education and public awareness**, so that conservation is done by the people
  who live with the resource.

::: caution Global warming and ozone depletion are different problems
Global warming is caused by **greenhouse gases** trapping heat in the
troposphere. Ozone depletion is caused by **chlorofluorocarbons** destroying O₃
in the stratosphere and lets in ultraviolet light. They have different gases,
different layers and different effects. Mixing them up is the commonest error in
this unit.
:::

## Chapter summary

- An ecosystem (Tansley, 1935) has abiotic components (climatic, edaphic,
  inorganic, organic) and biotic components (producers, consumers, decomposers).
- Food chains are grazing or detritus type; crossing chains form a food web,
  which gives the ecosystem stability.
- Energy flow is **unidirectional**: about 1 % of incident light is fixed, and
  only ~10 % passes from each trophic level to the next (Lindeman's ten per cent
  law). Matter, in contrast, moves in cycles.
- $\text{NPP} = \text{GPP} - R$; standing crop is a mass, productivity is a rate.
- Pyramids of number and of biomass may be inverted; the **pyramid of energy is
  always upright**.
- Population density $D = N/A$; unlimited growth is exponential,
  $N_t = N_0 e^{rt}$ (J-shaped); limited growth is logistic,
  $dN/dt = rN(K-N)/K$ (S-shaped), levelling at the carrying capacity $K$.
- Nitrogen cycle: fixation → ammonification → nitrification (*Nitrosomonas*,
  then *Nitrobacter*) → assimilation → denitrification (*Pseudomonas
  denitrificans*).
- Carbon cycle: photosynthesis takes CO₂ in; respiration, decomposition and
  combustion of fossil fuels put it back.
- Succession runs pioneer → seral stages → climax; hydrosere begins in water,
  xerosere on bare rock, and both end in the same mesic forest.
- Hydrophytes have aerenchyma, thin cuticle and reduced roots; xerophytes have
  deep roots, thick cuticle, sunken stomata and often CAM.
- Ecological imbalance in Nepal shows as Chure degradation, invasive *Mikania*
  and *Eichhornia*, retreating glaciers and glacial lake outburst floods; the
  answers are afforestation, community forestry, soil conservation, pollution
  control and law.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The term *ecosystem* was coined by <span class="marks">[1]</span>
   (a) E. P. Odum (b) A. G. Tansley (c) C. Elton (d) R. L. Lindeman
2. The pyramid that is always upright is the pyramid of <span class="marks">[1]</span>
   (a) number (b) biomass (c) energy (d) standing crop
3. Conversion of nitrite into nitrate in the soil is carried out by <span class="marks">[1]</span>
   (a) *Nitrosomonas* (b) *Nitrobacter* (c) *Rhizobium* (d) *Pseudomonas denitrificans*
4. Aerenchyma is a characteristic tissue of <span class="marks">[1]</span>
   (a) xerophytes (b) hydrophytes (c) epiphytes (d) mesophytes
5. If the producers of an ecosystem store 5000 kJ, the energy available to the
   secondary consumers by the ten per cent law is <span class="marks">[1]</span>
   (a) 500 kJ (b) 50 kJ (c) 5 kJ (d) 0.5 kJ
6. The pioneer community of a xerosere is <span class="marks">[1]</span>
   (a) moss (b) crustose lichen (c) herb (d) phytoplankton

::: note Answers to Group A
**1.** (b) — Tansley proposed the term in 1935; Lindeman gave the ten per cent law.
**2.** (c) — energy is a rate and is always lost upward, so it cannot invert.
**3.** (b) — *Nitrosomonas* makes nitrite, *Nitrobacter* oxidises it to nitrate.
**4.** (b) — the air chambers give buoyancy and store oxygen.
**5.** (b) — herbivores get 500 kJ, secondary consumers one tenth of that, 50 kJ.
**6.** (b) — crustose lichens alone can colonise bare rock and begin soil formation.
:::

**Group B — Short answer (4 marks each)**

1. Define an ecosystem and describe its biotic components with one example of
   each. <span class="marks">[4]</span>
2. What is an ecological pyramid? Explain, with a reason, why the pyramid of
   biomass in a pond ecosystem is inverted. <span class="marks">[4]</span>
3. The producers of a pond fix $8000\ \text{kJ m}^{-2}\ \text{yr}^{-1}$, of which
   they respire $5600\ \text{kJ m}^{-2}\ \text{yr}^{-1}$. Calculate the net primary
   productivity, and the energy that would reach a fish at the third trophic level
   under the ten per cent law. <span class="marks">[4]</span>
4. List any four morphological and anatomical adaptations of xerophytes, naming a
   plant that shows each. <span class="marks">[4]</span>

::: note Answers to Group B
**1.** Definition as in the text. **Producers** — autotrophs that fix solar
energy, e.g. grass, *Hydrilla*. **Consumers** — heterotrophs: primary
(herbivore, e.g. chital deer), secondary (primary carnivore, e.g. frog),
tertiary (top carnivore, e.g. Royal Bengal tiger). **Decomposers** — saprotrophic
bacteria and fungi that mineralise dead matter and return nutrients to the soil.

**3.** $\text{NPP} = \text{GPP} - R = 8000 - 5600 = 2400\ \text{kJ m}^{-2}\ \text{yr}^{-1}$.
The energy passed on is taken from the NPP, so the second trophic level receives
$0.10 \times 2400 = 240\ \text{kJ m}^{-2}\ \text{yr}^{-1}$ and the third trophic
level receives $0.10 \times 240 = 24\ \text{kJ m}^{-2}\ \text{yr}^{-1}$.

**4.** (i) Long, deeply penetrating branched roots — *Acacia catechu*.
(ii) Leaves reduced to spines with a photosynthetic phylloclade — *Opuntia*.
(iii) Very thick cuticle and multilayered epidermis with sclerenchymatous
hypodermis — *Nerium oleander*. (iv) Stomata few and sunken in hairy pits —
*Nerium*, *Casuarina*. A fifth, physiological, point: CAM photosynthesis with
stomata open only at night — *Aloe vera*.
:::

**Group C — Long answer (8 marks each)**

1. Describe the flow of energy through an ecosystem with the help of a labelled
   diagram. State the ten per cent law and explain why food chains rarely have
   more than four or five links. <span class="marks">[8]</span>
2. (a) Draw a labelled diagram of the nitrogen cycle. <span class="marks">[4]</span>
   (b) Explain nitrogen fixation, nitrification and denitrification, naming the
   bacteria responsible for each, and state what happens to soil fertility if
   denitrifying bacteria become very active. <span class="marks">[4]</span>

::: note Answer outline to Group C question 1
Diagram: sun → producers → herbivores → carnivores → top carnivores, with a
respiratory heat-loss arrow at every level and a decomposer box receiving from
all levels, as in the energy-flow figure.

Points to make: (i) the sun is the only source, and only about 1 % of the
photosynthetically active radiation reaching a leaf becomes gross primary
production; (ii) by the first law of thermodynamics the energy is converted, not
destroyed; (iii) by the second law each conversion releases heat, so the flow is
unidirectional and energy can never be recycled the way nutrients are;
(iv) Lindeman's ten per cent law — only about a tenth of the energy at one
trophic level is stored at the next, the rest going in respiration, in
undigested faeces and in parts never eaten; (v) hence with producers at
10,000 kJ the fifth level would hold only 1 kJ, too little to support a viable
population, so chains stop at four or five links and top carnivores are large,
few and vulnerable to extinction.
:::
