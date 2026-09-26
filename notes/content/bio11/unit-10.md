---
subject: Biology
grade: 11
unit: 10
title: Conservation Biology
hours: 4
area: Zoology
---

Nepal covers barely one tenth of one per cent of the world's land, yet it holds
around 3 % of the world's known plants and about 1 % of its known animals. That
richness comes from altitude: in less than 200 km you climb from 59 m in the
Terai to 8,848.86 m at Sagarmatha, passing through tropical sal forest,
subtropical hills, temperate oak, subalpine fir, alpine meadow and permanent
snow. Conservation biology is the science that asks how to keep that inheritance
alive while 30 million people make a living from the same land. This is the
shortest unit of the course but one of the most heavily examined, because the
examiner can ask about it in either a factual way (name the IUCN categories) or
an applied way (suggest measures to conserve the one-horned rhinoceros).

::: key What this unit is worth
Expect one MCQ and, very often, a short question worth 4 marks on either the
IUCN Red List categories or in-situ versus ex-situ conservation. Learn the seven
main Red List categories **in order**, and be able to name at least eight
threatened animals of Nepal with their scientific names, their status and where
they live. Numerical work on biodiversity indices and population growth is fair
game in the long questions.
:::

## 10.1 Conservation Biology

::: definition Conservation biology
**Conservation biology** is the branch of applied biology that studies the
causes of loss of biological diversity and develops practical methods to
protect, restore and sustainably manage species, their habitats and whole
ecosystems.
:::

It is a **crisis discipline** and a **mission-oriented** one: it accepts that
decisions must often be taken before the data are complete, because a species
that is lost cannot be recovered. It borrows from ecology, genetics, taxonomy,
economics, law and sociology, which is why a conservation plan for Chitwan
involves not only biologists but also the Nepal Army, buffer-zone user
committees and the hotels of Sauraha.

### Biodiversity and its three levels

**Biodiversity** (biological diversity) is the total variety of living organisms
at all levels of organisation. It is measured at three levels.

| Level | What varies | Example in Nepal |
|---|---|---|
| Genetic diversity | Alleles within a species | The 400-odd rice landraces (*Oryza sativa*) grown from the Terai to Jumla; the small, isolated rhino gene pool of Bardiya |
| Species diversity | Number and abundance of species in an area | 208 mammals, 867 birds and over 6,500 flowering plants recorded from Nepal |
| Ecosystem diversity | Variety of habitats and ecological processes | 118 ecosystems and 35 forest types, from Terai sal forest to trans-Himalayan steppe |

Species diversity itself has two components. **Species richness** is simply the
number of species present. **Species evenness** describes how equally the
individuals are shared among those species. A grassland with 40 chital, 30 hog
deer, 20 sambar and 10 barking deer is more even, and therefore more diverse,
than one with 97 chital and one individual each of the other three species,
even though the richness is 4 in both.

### Why biodiversity matters

- **Provisioning services** — food, timber, fuelwood, fodder, fibre and about
  1,700 species of medicinal plants used in Nepal, including *Nardostachys
  jatamansi* and *Ophiocordyceps sinensis* (yarsagumba).
- **Regulating services** — pollination of crops by bees and other insects,
  seed dispersal by birds and bats, decomposition and nutrient recycling,
  flood control by forests, carbon storage.
- **Supporting services** — soil formation, primary production, the water cycle.
- **Cultural and aesthetic value** — sacred groves, the rhino and the danphe
  (*Lophophorus impejanus*, the national bird), and the wildlife tourism that
  earns Chitwan and Sagarmatha a large share of Nepal's tourist income.
- **Ethical value** — every species has an intrinsic right to exist, and each is
  the unique product of millions of years of evolution.
- **Option value** — genes we have not yet found a use for. The wild relatives
  of crops carry the disease-resistance alleles that plant breeders will need.

### Measuring diversity: Simpson's and Shannon's indices

Counting species is not enough, because richness ignores abundance. Two indices
are used in NEB-level work. In both, $n_i$ is the number of individuals of the
$i$th species, $N$ is the total number of individuals and $S$ is the number of
species.

**Simpson's index of dominance** is the probability that two individuals drawn
at random from the community belong to the *same* species:

$$ D = \frac{\sum n_i (n_i - 1)}{N (N - 1)} $$

$D$ runs from 0 to 1 and gets *larger* as diversity falls, so it is usually
reported as **Simpson's index of diversity**, $1 - D$, or as the **reciprocal
index** $1/D$, which equals the effective number of equally common species.

**Shannon–Wiener index** measures the uncertainty in predicting the species of
the next individual you pick:

$$ H = - \sum_{i=1}^{S} p_i \ln p_i \qquad \text{where} \quad p_i = n_i / N $$

$H$ is 0 for a single-species community and reaches its maximum,
$H_{max} = \ln S$, only when all species are equally abundant. The ratio
$E = H / \ln S$ is **Pielou's evenness**, a number between 0 and 1.

::: example Simpson's index for a grassland census
**Problem.** A 1 ha block of the Chitwan grassland is censused and yields
40 chital, 30 hog deer, 20 sambar and 10 barking deer. Calculate Simpson's
index of dominance, Simpson's index of diversity and the reciprocal index.

**Solution.**
Total individuals $N = 40 + 30 + 20 + 10 = 100$, so $N(N-1) = 100 \times 99 = 9900$.

Now find $\sum n_i(n_i - 1)$ species by species:

| Species | $n_i$ | $n_i - 1$ | $n_i(n_i-1)$ |
|---|---|---|---|
| Chital | 40 | 39 | 1560 |
| Hog deer | 30 | 29 | 870 |
| Sambar | 20 | 19 | 380 |
| Barking deer | 10 | 9 | 90 |
| **Total** | **100** | — | **2900** |

$$ D = \frac{2900}{9900} = 0.293 $$

Simpson's index of diversity $= 1 - D = 1 - 0.293 = \mathbf{0.707}$.

Reciprocal index $= 1/D = 1/0.293 = \mathbf{3.41}$ — the community behaves like
one with about 3.4 equally common species, slightly less than its richness of 4
because the chital dominate.
:::

::: example Shannon–Wiener index and evenness for the same block
**Problem.** For the census above, calculate $H$, $H_{max}$ and the evenness $E$.

**Solution.** First the proportions: $p = 0.4,\ 0.3,\ 0.2,\ 0.1$.

| $p_i$ | $\ln p_i$ | $p_i \ln p_i$ |
|---|---|---|
| 0.4 | −0.9163 | −0.3665 |
| 0.3 | −1.2040 | −0.3612 |
| 0.2 | −1.6094 | −0.3219 |
| 0.1 | −2.3026 | −0.2303 |
| | **Total** | **−1.2799** |

$$ H = -(-1.2799) = \mathbf{1.280} $$

$$ H_{max} = \ln S = \ln 4 = 1.386 $$

$$ E = \frac{H}{H_{max}} = \frac{1.280}{1.386} = \mathbf{0.923} $$

An evenness of 0.923 is high: no single species is strongly dominant. If the
same 100 animals were 97 chital and one of each other species, $H$ would fall to
about 0.17 and $E$ to about 0.12.
:::

::: caution Do not confuse the two Simpson forms
$D$ itself is a **dominance** index — a high $D$ means *low* diversity. The
number the examiner usually wants is $1 - D$. Always state which form you have
calculated. Also note that $D$ uses $n(n-1)$, not $n^2$; the $n^2$ version is
for an infinite population and gives a slightly different answer.
:::

### Threats to biodiversity — the HIPPO checklist

The five great drivers of extinction are easy to remember as **HIPPO**.

| Letter | Driver | How it works in Nepal |
|---|---|---|
| **H** | Habitat loss, degradation and fragmentation | Conversion of Terai forest to cropland and settlement; roads, transmission lines and hydropower cutting corridors; overgrazing of alpine pasture. The single biggest cause of species loss worldwide. |
| **I** | Invasive alien species | Of roughly 179 naturalised alien plants in Nepal, about 26 behave invasively. *Mikania micrantha* smothers rhino habitat in Chitwan, *Lantana camara* and *Chromolaena odorata* choke Terai forest floors, *Eichhornia crassipes* (water hyacinth) blankets wetlands and *Parthenium hysterophorus* invades grassland. Four of these are on the global "100 worst invaders" list. |
| **P** | Pollution | Pesticide and fertiliser run-off causing eutrophication; sewage in the Bagmati; veterinary diclofenac, which destroyed over 90 % of Nepal's *Gyps* vultures. |
| **P** | Population growth and overconsumption | Rising demand for firewood, fodder, land and water. |
| **O** | Overexploitation | Poaching of rhino horn, tiger bone and pangolin scales for illegal trade; overfishing; uncontrolled collection of yarsagumba and medicinal herbs. |

Climate change now acts as a multiplier on all five: treelines are creeping
upwards, glacial lakes are growing, and alpine species such as the snow leopard
are being squeezed against the top of the mountain, with nowhere higher to go.

### Small populations: why rarity itself is dangerous

Once a population becomes small, it is in trouble for reasons that have nothing
to do with the original threat.

- **Inbreeding depression** — close relatives mate, harmful recessive alleles
  become homozygous, and fertility and survival fall.
- **Genetic drift and the bottleneck effect** — alleles are lost at random, so
  the population loses the variation it needs to adapt to new diseases or a
  changing climate.
- **Demographic stochasticity** — in a population of 20, a run of male-only
  births is simply bad luck, but it can end the line.
- **Allee effect** — below a threshold density, animals cannot find mates and
  the per-capita growth rate itself becomes negative.

The **minimum viable population (MVP)** is the smallest number of individuals
that gives a population a high probability (commonly 95 %) of surviving for a
stated period (commonly 100 years). Estimating it is the job of **population
viability analysis (PVA)**, and it depends strongly on the population's **age
structure** — the proportion of pre-reproductive, reproductive and
post-reproductive individuals.

```figure caption="Age-structure pyramids. The shape of the pyramid predicts what the population will do next, whether the population is human or wild: a broad base means many individuals about to enter the breeding age group."
import numpy as np, matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 3, figsize=(5.2, 2.7), sharey=True)
titles = ['Expanding\n(rapid growth)', 'Stable\n(zero growth)', 'Declining\n(negative growth)']
groups = ['post-\nreproductive', 'reproductive', 'pre-\nreproductive']
data = [[14, 30, 56], [28, 34, 38], [40, 36, 24]]
ys = np.array([2.0, 1.0, 0.0])
h = 0.82

for ax, t, d in zip(axes, titles, data):
    for y, w in zip(ys, d):
        ax.barh(y, -w, height=h, color=SERIES[0], alpha=0.85,
                edgecolor='white', lw=0.8)
        ax.barh(y, w, height=h, color=SERIES[4], alpha=0.85,
                edgecolor='white', lw=0.8)
    ax.set_title(t, fontsize=7.8, color=INK, pad=5)
    ax.set_xlim(-64, 64)
    ax.set_ylim(-0.7, 2.75)
    ax.axvline(0, color='white', lw=1.0)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines[['top', 'right', 'bottom', 'left']].set_visible(False)

for y, g in zip(ys, groups):
    axes[0].text(-70, y, g, ha='right', va='center', fontsize=6.6,
                 color=MUTED, clip_on=False)
axes[1].text(-32, 2.52, 'male', ha='center', fontsize=6.8, color=SERIES[0])
axes[1].text(32, 2.52, 'female', ha='center', fontsize=6.8, color=SERIES[4])
fig.subplots_adjust(wspace=0.12)
```

### In-situ and ex-situ conservation

| | **In-situ conservation** | **Ex-situ conservation** |
|---|---|---|
| Meaning | Protecting the species *in its natural habitat* | Protecting the species *outside its natural habitat* |
| Unit protected | The whole ecosystem, with all its interactions | Individuals, gametes, seeds or tissue |
| Evolution | Natural selection continues, so the species keeps adapting | Selection is relaxed; animals may become tame and lose wild behaviour |
| Cost per species | Low once the area is established | Very high |
| Numbers possible | Large populations | Small populations only |
| Methods | National parks, wildlife reserves, conservation areas, hunting reserves, buffer zones, biosphere reserves, community and religious forests, sacred groves | Zoos, safari parks, botanical gardens, arboreta, aquaria, seed and gene banks, cryopreservation of gametes and embryos, tissue culture, captive breeding and reintroduction |
| Nepali examples | Chitwan National Park, Annapurna Conservation Area, Koshi Tappu Wildlife Reserve, buffer-zone community forests | Central Zoo Jawalakhel, Gharial Breeding Centre at Kasara, vulture breeding centre at Kasara (Chitwan), National Botanical Garden Godawari, National Gene Bank Khumaltar |

The two are complementary, not rival. Gharials bred at Kasara are released into
the Rapti and Narayani rivers; vultures bred in captivity were released into a
Vulture Safe Zone in 2017. Ex-situ work buys time; only in-situ work gives a
species a future.

### Nepal's protected-area network

Nepal's protected areas were created under the **National Parks and Wildlife
Conservation Act, 2029 B.S. (1973 A.D.)** — still the main wildlife law of the
country. The network now comprises **13 national parks, 1 wildlife reserve,
1 hunting reserve and 7 conservation areas**, together with buffer zones around
most of the parks. The Department of National Parks and Wildlife Conservation
(DNPWC) puts total coverage at **23.39 % of Nepal's land area**, and Nepal has
committed to reaching 30 % by 2030.

The categories differ in how strictly people are excluded.

| Category | Management | Example |
|---|---|---|
| **National park** | Strict protection of the whole ecosystem; hunting, grazing, farming and removal of resources are prohibited | Chitwan (1973, Nepal's first, a UNESCO World Heritage Site since 1984); Chhayanath in Mugu is the newest, declared in 2025 |
| **Wildlife reserve** | Set aside for the protection of particular species and their habitat | Koshi Tappu (1976), Nepal's only wildlife reserve, famous for the wild water buffalo and for migratory birds |
| **Hunting reserve** | Regulated trophy hunting under licence, with quotas | Dhorpatan (1987), Nepal's only one, where blue sheep and Himalayan tahr may be hunted |
| **Conservation area** | Multiple use; local people live inside and manage resources through committees | Annapurna (1992), at 7,629 km² the largest protected area in Nepal |
| **Buffer zone** | Belt of forest and settlement around a park; 30–50 % of park revenue is returned to local user groups | Buffer zones of Chitwan and Bardiya |

::: example Closing the gap to the 30 % target
**Problem.** Nepal's total land area is 147,181 km² and 23.39 % of it is
protected. How many km² are protected, and how much more must be protected to
reach the 30 % target?

**Solution.**
Area protected now:

$$ A_1 = 0.2339 \times 147181 = 34426\ \text{km}^2 $$

Area needed at 30 %:

$$ A_2 = 0.30 \times 147181 = 44154\ \text{km}^2 $$

Extra area required:

$$ \Delta A = 44154 - 34426 = \mathbf{9728\ km^2} $$

That is an area larger than Annapurna Conservation Area — which shows why the
target will have to be met mostly through community forests and other
"other effective area-based conservation measures" rather than new parks.
:::

```figure caption="Schematic map of Nepal's protected-area network, keyed by number. Green = national park, red = wildlife reserve, gold = hunting reserve, blue = conservation area. The outline and the positions are approximate and not to scale."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon

fig, ax = plt.subplots(figsize=(5.2, 4.6))

border = [(80.06, 28.80), (80.25, 29.30), (80.55, 29.75), (80.75, 30.15),
          (81.05, 30.25), (81.40, 30.42), (81.80, 30.32), (82.20, 30.15),
          (82.55, 29.85), (83.00, 29.60), (83.40, 29.45), (83.80, 29.30),
          (84.25, 29.10), (84.70, 28.90), (85.10, 28.70), (85.60, 28.55),
          (86.00, 28.10), (86.55, 28.10), (87.00, 27.90), (87.45, 27.85),
          (87.90, 27.95), (88.15, 27.55), (88.20, 27.10), (87.90, 26.75),
          (87.45, 26.60), (87.05, 26.40), (86.50, 26.55), (85.90, 26.60),
          (85.30, 26.85), (84.90, 27.10), (84.45, 27.35), (84.00, 27.45),
          (83.60, 27.45), (83.20, 27.40), (82.75, 27.60), (82.30, 27.75),
          (81.90, 27.90), (81.45, 28.05), (81.00, 28.30), (80.55, 28.60)]
ax.add_patch(Polygon(border, closed=True, facecolor='#f4f6f9',
                     edgecolor=INK, lw=1.3, zorder=1))

NP, WR, HR, CA = SERIES[2], SERIES[1], SERIES[3], SERIES[0]
sites = [
    (1, 'Shuklaphanta NP', 80.28, 28.90, NP),
    (2, 'Khaptad NP', 81.15, 29.38, NP),
    (3, 'Bardiya NP', 81.42, 28.42, NP),
    (4, 'Banke NP', 81.95, 28.22, NP),
    (5, 'Rara NP', 82.10, 29.55, NP),
    (6, 'Chhayanath NP', 82.55, 29.80, NP),
    (7, 'Shey Phoksundo NP', 82.95, 29.35, NP),
    (8, 'Chitwan NP', 84.32, 27.58, NP),
    (9, 'Parsa NP', 84.88, 27.38, NP),
    (10, 'Langtang NP', 85.55, 28.20, NP),
    (11, 'Shivapuri Nagarjun NP', 85.38, 27.82, NP),
    (12, 'Sagarmatha NP', 86.82, 27.90, NP),
    (13, 'Makalu Barun NP', 87.25, 27.75, NP),
    (14, 'Koshi Tappu WR', 86.98, 26.85, WR),
    (15, 'Dhorpatan HR', 83.12, 28.52, HR),
    (16, 'Api Nampa CA', 80.82, 29.85, CA),
    (17, 'Blackbuck CA', 81.20, 28.12, CA),
    (18, 'Annapurna CA', 83.92, 28.70, CA),
    (19, 'Manaslu CA', 84.82, 28.55, CA),
    (20, 'Gaurishankar CA', 86.20, 27.95, CA),
    (21, 'Kanchenjunga CA', 88.00, 27.62, CA),
]
for n, name, x, y, c in sites:
    ax.plot(x, y, marker='o', ms=9.0, color=c, mec='white', mew=0.9, zorder=3)
    ax.text(x, y, str(n), ha='center', va='center', fontsize=5.3,
            color='white', zorder=4)

ax.text(79.95, 30.30, 'NEPAL', fontsize=10.0, color=INK, ha='left')
ax.annotate('', xy=(88.35, 26.95), xytext=(88.35, 26.35),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.0,
                            mutation_scale=9))
ax.text(88.35, 26.15, 'N', fontsize=7.2, color=MUTED, ha='center')

for k, (n, name, x, y, c) in enumerate(sites):
    col, row = k // 7, k % 7
    ax.plot(80.10 + col*3.32, 25.30 - row*0.42, marker='o', ms=6.5, color=c,
            mec='white', mew=0.7)
    ax.text(80.30 + col*3.32, 25.30 - row*0.42, f'{n}. {name}',
            fontsize=6.3, color=INK, ha='left', va='center')

ax.set_xlim(79.7, 89.6)
ax.set_ylim(22.15, 30.75)
ax.axis('off')
```


```figure caption="The twelve largest protected areas of Nepal by land area (km$^2$). Conservation areas dominate the top of the list because they are multiple-use areas in the high mountains; Chitwan and Bardiya are small by comparison but carry most of the large mammals."
import numpy as np, matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(5.2, 3.4))
names = ['Annapurna CA', 'Shey Phoksundo NP', 'Gaurishankar CA', 'Kanchenjunga CA',
         'Api Nampa CA', 'Langtang NP', 'Manaslu CA', 'Makalu Barun NP',
         'Dhorpatan HR', 'Sagarmatha NP', 'Bardiya NP', 'Chitwan NP']
area = [7629, 2712, 2179, 2035, 1903, 1710, 1663, 1500, 1325, 1148, 968, 953]
kind = ['CA', 'NP', 'CA', 'CA', 'CA', 'NP', 'CA', 'NP', 'HR', 'NP', 'NP', 'NP']
cmap = {'NP': SERIES[2], 'CA': SERIES[0], 'HR': SERIES[3]}
y = np.arange(len(names))[::-1]

ax.barh(y, area, height=0.68, color=[cmap[k] for k in kind], alpha=0.9)
for yy, a in zip(y, area):
    ax.text(a + 130, yy, f'{a:,}', va='center', fontsize=6.6, color=MUTED)

ax.set_yticks(y)
ax.set_yticklabels(names, fontsize=7.0, color=INK)
ax.set_xlabel('area (km$^2$)', fontsize=7.6, color=MUTED)
ax.set_xlim(0, 8900)
ax.tick_params(axis='x', labelsize=6.8, colors=MUTED)
ax.tick_params(axis='y', length=0)
ax.xaxis.grid(True, color=GRID, lw=0.7)
ax.set_axisbelow(True)
ax.spines[['top', 'right', 'left']].set_visible(False)

handles = [plt.Rectangle((0, 0), 1, 1, color=cmap[k], alpha=0.9) for k in ['NP', 'CA', 'HR']]
ax.legend(handles, ['national park', 'conservation area', 'hunting reserve'],
          fontsize=6.6, frameon=False, loc='lower right')
```

### Other conservation instruments in Nepal

- **Buffer-zone programme** (1993 amendment to the Act) — local user groups get
  back 30–50 % of park income for community development, which turns neighbours
  into allies rather than poachers.
- **Community forestry** — more than 22,000 community forest user groups manage
  forest outside the protected areas; forest cover in Nepal has risen since the
  1990s largely because of them.
- **Ramsar Convention** (joined 1988) — Nepal has **10 Ramsar sites**, wetlands
  of international importance, including Koshi Tappu, Beeshazari Tal, Ghodaghodi
  Tal, Rara, Phoksundo, Gosaikunda, Gokyo, Mai Pokhari, Jagadishpur Reservoir
  and the Lake Cluster of Pokhara Valley.
- **CITES** — the Convention on International Trade in Endangered Species.
  Nepal has been a party since **1975** and passed its own CITES Act in 2073 B.S.
  (2017 A.D.). Appendix **I** lists species threatened with extinction, for which
  commercial international trade is banned (tiger, rhinoceros, snow leopard, red
  panda, elephant, gharial, pangolins). Appendix **II** lists species not yet
  threatened but which may become so unless trade is controlled; trade needs an
  export permit. Appendix **III** lists species protected by at least one country
  that has asked others for help in controlling trade.
- **Environment Protection Act, 2076 B.S. (2019 A.D.)** — makes environmental
  impact assessment compulsory for large projects.

## 10.2 Wildlife

**Wildlife** means all undomesticated organisms — animals, plants and
micro-organisms — living in their natural habitat. In common NEB usage, and in
the wording of the National Parks and Wildlife Conservation Act, it refers
chiefly to wild animals. The Act's schedules list **26 mammals, 9 birds and
3 reptiles** as *protected species*: killing, injuring, buying, selling or
possessing any part of them is a criminal offence carrying heavy fines and
imprisonment.

### IUCN Red List categories

The **International Union for Conservation of Nature (IUCN)**, founded in 1948,
maintains the **Red List of Threatened Species** — the global standard for
judging how close a species is to extinction. A species is placed in a category
using five quantitative criteria (labelled A–E): rate of population decline,
geographic range size, small population size with continuing decline, very small
or restricted population, and quantitative analysis of extinction probability.

```figure caption="The IUCN Red List categories, with Nepali examples. The three categories in the middle — CR, EN and VU — together make up the 'threatened' species; a species is 'Red-listed' when it falls in one of them."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(5.2, 3.6))

rows = [
    ('EX  Extinct', INK, 1.0, 'no Nepali species confirmed; the dodo is the classic case'),
    ('EW  Extinct in the Wild', MUTED, 1.0, "survives only in captivity, e.g. Pere David's deer"),
    ('CR  Critically Endangered', SERIES[1], 1.0, 'gharial, Chinese pangolin, white-rumped vulture,\nBengal florican'),
    ('EN  Endangered', SERIES[1], 0.62, 'Bengal tiger, red panda, Asian elephant,\nwild water buffalo (arna), Himalayan musk deer'),
    ('VU  Vulnerable', SERIES[3], 1.0, 'one-horned rhinoceros, snow leopard, gaur,\nswamp deer, clouded leopard'),
    ('NT  Near Threatened', SERIES[0], 0.85, 'Indian rock python'),
    ('LC  Least Concern', SERIES[2], 0.9, 'chital, rhesus monkey, wild boar'),
]
ytop = 7.9
for i, (lab, c, al, ex) in enumerate(rows):
    y = ytop - i
    ax.add_patch(FancyBboxPatch((0.30, y - 0.34), 4.80, 0.68,
                                boxstyle='round,pad=0.04,rounding_size=0.12',
                                facecolor=c, alpha=al, edgecolor='none', zorder=2))
    ax.text(2.70, y, lab, ha='center', va='center', fontsize=7.0,
            color='white', zorder=3)
    ax.text(5.45, y, ex, ha='left', va='center', fontsize=6.4, color=INK)

for j, (lab, ex) in enumerate([('DD  Data Deficient', 'not enough information to judge'),
                               ('NE  Not Evaluated', 'never assessed against the criteria')]):
    y = 0.72 - j*0.78
    ax.add_patch(FancyBboxPatch((0.30, y - 0.30), 4.80, 0.60,
                                boxstyle='round,pad=0.04,rounding_size=0.12',
                                facecolor=MUTED, alpha=0.45, edgecolor='none', zorder=2))
    ax.text(2.70, y, lab, ha='center', va='center', fontsize=7.0, color=INK, zorder=3)
    ax.text(5.45, y, ex, ha='left', va='center', fontsize=6.4, color=INK)

ax.plot([0.05, 0.05], [6.28, 3.62], color=SERIES[1], lw=2.2)
ax.text(-0.18, 4.95, 'THREATENED', rotation=90, ha='center', va='center',
        fontsize=6.8, color=SERIES[1])
ax.annotate('', xy=(-0.95, 7.9), xytext=(-0.95, 1.9),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.1, mutation_scale=10))
ax.text(-1.18, 4.9, 'increasing risk of extinction', rotation=90, ha='center',
        va='center', fontsize=6.6, color=MUTED)

ax.set_xlim(-1.5, 13.9)
ax.set_ylim(-0.55, 8.5)
ax.axis('off')
```

::: memory Order of the categories
**E**very **E**vening **C**hildren **E**at **V**ery **N**ice **L**addu —
**EX, EW, CR, EN, VU, NT, LC** (then DD and NE, which are not risk categories
at all). Write them in this order and never put VU above EN.
:::

::: caution "Endangered" is a category, not a loose word
In an exam answer, *Endangered* (EN) means a species that meets the IUCN
criteria for EN — for example a population reduction of at least 50 % over ten
years or three generations. The one-horned rhinoceros is **Vulnerable**, not
Endangered, because its numbers have recovered. Writing "the endangered rhino"
will cost you the mark in a question that asks for IUCN status.
:::

### Threatened animals of Nepal

| Common name | Scientific name | IUCN status | Where found in Nepal |
|---|---|---|---|
| Greater one-horned rhinoceros | *Rhinoceros unicornis* | Vulnerable | Chitwan, Bardiya, Shuklaphanta, Parsa |
| Royal Bengal tiger | *Panthera tigris* | Endangered | Chitwan, Bardiya, Parsa, Banke, Shuklaphanta |
| Snow leopard | *Panthera uncia* | Vulnerable | Himalaya above 3,000 m — Shey Phoksundo, Sagarmatha, Api Nampa |
| Red panda | *Ailurus fulgens* | Endangered | Temperate bamboo forest, Langtang to Kanchenjunga |
| Asian elephant | *Elephas maximus* | Endangered | Terai forests, Bardiya to Jhapa |
| Wild water buffalo (arna) | *Bubalus arnee* | Endangered | Koshi Tappu Wildlife Reserve |
| Swamp deer (barasingha) | *Rucervus duvaucelii* | Vulnerable | Shuklaphanta phanta grassland |
| Gharial | *Gavialis gangeticus* | Critically Endangered | Narayani, Rapti, Karnali, Babai rivers |
| Chinese pangolin | *Manis pentadactyla* | Critically Endangered | Mid-hills, widely poached |
| White-rumped vulture | *Gyps bengalensis* | Critically Endangered | Terai and lower hills |
| Bengal florican | *Houbaropsis bengalensis* | Critically Endangered | Terai grasslands of Chitwan, Shuklaphanta |
| Himalayan musk deer | *Moschus leucogaster* | Endangered | Subalpine forest, 2,500–4,000 m |

### Two Nepali success stories

```figure caption="Recovery of Nepal's two flagship mammals from national censuses. Rhino counts come from the National Rhino Count (block count from elephant back); tiger numbers come from the National Tiger and Prey Base Survey, which uses camera traps and individual stripe patterns."
import numpy as np, matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.2, 2.7))

ry = [2005, 2011, 2015, 2021]
rn = [409, 534, 645, 752]
ax1.plot(ry, rn, marker='o', ms=5, color=SERIES[0], lw=1.8)
for x, v in zip(ry, rn):
    ax1.annotate(str(v), (x, v), textcoords='offset points', xytext=(0, 7),
                 ha='center', fontsize=6.6, color=SERIES[0])
ax1.set_title('One-horned rhinoceros', fontsize=8.0, color=INK, pad=6)
ax1.set_ylim(320, 880)
ax1.set_xticks(ry)

ty = [2010, 2013, 2018, 2022, 2026]
tn = [121, 198, 235, 355, 429]
ax2.plot(ty, tn, marker='s', ms=5, color=SERIES[1], lw=1.8)
for x, v in zip(ty, tn):
    ax2.annotate(str(v), (x, v), textcoords='offset points', xytext=(0, 7),
                 ha='center', fontsize=6.6, color=SERIES[1])
ax2.set_title('Royal Bengal tiger', fontsize=8.0, color=INK, pad=6)
ax2.set_ylim(60, 510)
ax2.set_xticks(ty)

for ax in (ax1, ax2):
    ax.set_xlabel('census year', fontsize=7.4, color=MUTED)
    ax.set_ylabel('number of animals', fontsize=7.4, color=MUTED)
    ax.tick_params(labelsize=6.6, colors=MUTED)
    ax.yaxis.grid(True, color=GRID, lw=0.7)
    ax.set_axisbelow(True)
    ax.spines[['top', 'right']].set_visible(False)

fig.subplots_adjust(wspace=0.38)
```

**The rhinoceros.** Poaching and habitat loss cut Nepal's rhinos to about 100 in
the late 1960s. Army posts inside Chitwan, the buffer-zone programme,
translocation of founder animals to Bardiya and Shuklaphanta, and
community-based anti-poaching units have taken the national total from 409 in
2005 to **752 in 2021** — 694 of them in Chitwan. Nepal has recorded several
complete years with zero rhino poaching since 2011.

**The tiger.** At the 2010 St Petersburg summit Nepal pledged to double its
tigers by 2022. It succeeded, and the fifth national survey (camera-trapping
from December 2025 to April 2026) put the population at **429**, up from 355 in
2022 and 121 in 2010. The problem has now changed shape: with tigers at high
density, human–tiger conflict and habitat carrying capacity have become the
leading management worries.

::: example Growth rate of Nepal's tiger population
**Problem.** Nepal's tiger population rose from 355 in the 2022 census to 429 in
the 2026 census. Calculate (a) the percentage increase, (b) the intrinsic rate
of natural increase $r$, assuming exponential growth, and (c) the doubling time
at this rate.

**Solution.**
**(a)** Increase $= 429 - 355 = 74$ tigers.

$$ \text{percentage increase} = \frac{74}{355} \times 100 = 20.8\ \% $$

**(b)** For exponential growth $N_t = N_0 e^{rt}$, so

$$ r = \frac{1}{t} \ln \frac{N_t}{N_0} = \frac{1}{4} \ln \frac{429}{355} $$

$$ \frac{429}{355} = 1.2085, \qquad \ln 1.2085 = 0.1893 $$

$$ r = \frac{0.1893}{4} = \mathbf{0.0473\ year^{-1}} \ (4.73\ \%\ \text{per year}) $$

**(c)** Doubling time:

$$ t_d = \frac{\ln 2}{r} = \frac{0.693}{0.0473} = \mathbf{14.7\ years} $$

In practice the population will not double again: the parks are approaching
their carrying capacity $K$, so growth will follow the logistic curve and level
off.
:::

**The vultures.** Nepal's *Gyps* vultures fell by more than 90 % in the 1990s
and 2000s because the painkiller **diclofenac**, given to cattle, causes kidney
failure in any vulture that feeds on the carcass. Nepal banned veterinary
diclofenac in **2006**, promoted the safe alternative meloxicam, and opened the
world's first community-managed **"Jatayu" vulture restaurant** at Pithauli,
Nawalparasi, in the same year — a feeding site supplied with drug-free carcasses
of old cattle. A Vulture Safe Zone of roughly 30,000 km² now stretches from
Nawalparasi to Kailali, and in 2017 the first captive-bred white-rumped vultures
in South Asia were released there. Counts have been rising since about 2013.

### Threats to wildlife in Nepal, and what is being done

| Threat | Measures in use |
|---|---|
| Poaching and illegal trade (rhino horn, tiger bone, pangolin scales, musk pods) | Army posts inside parks, community-based anti-poaching units, informant networks, CITES Act 2073, wildlife crime control bureau |
| Habitat loss and fragmentation | Terai Arc Landscape programme linking Nepali and Indian parks through biological corridors; wildlife underpasses on new highways |
| Human–wildlife conflict (crop raiding by elephants and rhinos, livestock killed by snow leopards and tigers) | Relief and compensation scheme, predator-proof corrals, electric and biofence, community insurance |
| Invasive species | Manual removal of *Mikania micrantha* in Chitwan grassland, grassland burning and cutting |
| Small, isolated populations | Translocation of rhinos to Bardiya and Shuklaphanta; captive breeding of gharial and vultures |
| Chemical threats | Ban on veterinary diclofenac; regulation of pesticides |

Community-based conservation is the thread that runs through all of these. The
Annapurna Conservation Area, run by the National Trust for Nature Conservation,
was the first protected area in Nepal where local people were made managers
rather than trespassers, and it remains the model that buffer zones and
community forests follow.

## Chapter summary

- **Conservation biology** is the mission-oriented science of protecting
  biodiversity; **biodiversity** exists at genetic, species and ecosystem levels.
- Species diversity combines **richness** (how many species) and **evenness**
  (how equally shared). Simpson: $D = \sum n_i(n_i-1) / N(N-1)$; diversity is
  $1-D$. Shannon: $H = -\sum p_i \ln p_i$, with $H_{max} = \ln S$ and evenness
  $E = H/\ln S$.
- The drivers of loss are **HIPPO**: habitat loss, invasive species, pollution,
  population growth, overexploitation — amplified by climate change.
- Small populations then suffer **inbreeding depression, genetic drift,
  demographic stochasticity and the Allee effect**; the **MVP** is the smallest
  population with a high chance of long-term survival.
- **In-situ** conservation protects species in their habitat (parks, reserves,
  conservation areas, buffer zones); **ex-situ** conservation protects them
  outside it (zoos, gene banks, captive breeding). They are complementary.
- Nepal has **13 national parks, 1 wildlife reserve (Koshi Tappu), 1 hunting
  reserve (Dhorpatan) and 7 conservation areas**, covering **23.39 %** of the
  country, all under the **National Parks and Wildlife Conservation Act, 2029
  (1973)**. The Act protects **26 mammals, 9 birds and 3 reptiles**.
- The **IUCN Red List** categories in order are **EX, EW, CR, EN, VU, NT, LC**,
  plus DD and NE; CR, EN and VU together are the **threatened** species.
- Nepal is party to **CITES** (since 1975; Appendix I bans commercial trade) and
  **Ramsar** (since 1988; 10 sites).
- Flagship recoveries: rhinos **409 (2005) → 752 (2021)**; tigers
  **121 (2010) → 429 (2026)**; *Gyps* vultures recovering after the 2006
  diclofenac ban.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Which of the following is the correct order of IUCN categories from the
   highest to the lowest risk of extinction? <span class="marks">[1]</span>
   (a) CR, EN, VU, NT, LC (b) EN, CR, VU, LC, NT (c) VU, EN, CR, NT, LC (d) CR, VU, EN, LC, NT
2. The only wildlife reserve of Nepal is <span class="marks">[1]</span>
   (a) Dhorpatan (b) Koshi Tappu (c) Shuklaphanta (d) Parsa
3. Simpson's index of diversity of a community containing only one species is
   <span class="marks">[1]</span>
   (a) 1 (b) 0.5 (c) 0 (d) infinite
4. Conservation of the gharial by breeding it at Kasara and releasing the young
   into the Rapti is an example of <span class="marks">[1]</span>
   (a) in-situ conservation only (b) ex-situ conservation followed by
   reintroduction (c) a hunting reserve (d) a buffer zone
5. The collapse of *Gyps* vulture populations in South Asia was caused mainly by
   <span class="marks">[1]</span>
   (a) DDT (b) diclofenac (c) organophosphates (d) methyl mercury
6. The IUCN status of the greater one-horned rhinoceros is
   <span class="marks">[1]</span>
   (a) Critically Endangered (b) Endangered (c) Vulnerable (d) Near Threatened

::: note Answers to Group A
**1.** (a) — CR is the highest risk, then EN, VU, NT, LC.
**2.** (b) — Shuklaphanta and Parsa were upgraded to national parks in 2017, leaving Koshi Tappu as the only wildlife reserve; Dhorpatan is a hunting reserve.
**3.** (c) — with one species every pair drawn belongs to the same species, so $D = 1$ and $1 - D = 0$.
**4.** (b) — breeding outside the natural habitat is ex-situ; putting the animals back is reintroduction.
**5.** (b) — diclofenac in cattle carcasses causes fatal kidney failure in *Gyps* vultures.
**6.** (c) — numbers have recovered enough for the species to be downlisted to Vulnerable.
:::

**Group B — Short answer (4 marks each)**

1. Define conservation biology and state its three levels of biodiversity with
   one Nepali example of each. <span class="marks">[4]</span>
2. Differentiate between in-situ and ex-situ conservation on any four bases,
   giving one Nepali example of each. <span class="marks">[4]</span>
3. A sample of 100 birds from Koshi Tappu contains 50 of species A, 25 of
   species B, 15 of species C and 10 of species D. Calculate the Shannon–Wiener
   index and the evenness. <span class="marks">[4]</span>
4. List the IUCN Red List categories in order and explain the difference between
   *Extinct in the Wild* and *Critically Endangered*.
   <span class="marks">[4]</span>
5. Why is a small population at risk even after the original threat has been
   removed? Explain any four reasons. <span class="marks">[4]</span>

::: note Answers to Group B
**1.** Conservation biology is the applied science that studies the loss of
biological diversity and develops methods to protect, restore and sustainably
manage species, habitats and ecosystems. Levels: **genetic** — the many rice
landraces of Jumla and the Terai; **species** — the 208 mammals and 867 birds
recorded in Nepal; **ecosystem** — the 118 ecosystems from Terai sal forest to
trans-Himalayan steppe.

**2.** Any four of: meaning (in habitat / outside habitat); unit protected
(whole ecosystem / individuals, seeds, gametes); evolution (natural selection
continues / relaxed, behaviour may be lost); cost (low per species / very high);
numbers supported (large / small). Examples: Chitwan National Park (in-situ);
Central Zoo Jawalakhel or the Kasara gharial breeding centre (ex-situ).

**3.** $p = 0.50,\ 0.25,\ 0.15,\ 0.10$.
$0.50 \ln 0.50 = 0.50 \times (-0.6931) = -0.3466$;
$0.25 \ln 0.25 = 0.25 \times (-1.3863) = -0.3466$;
$0.15 \ln 0.15 = 0.15 \times (-1.8971) = -0.2846$;
$0.10 \ln 0.10 = 0.10 \times (-2.3026) = -0.2303$.
Sum $= -1.2081$, so $H = 1.208$.
$H_{max} = \ln 4 = 1.386$, therefore $E = 1.208 / 1.386 = 0.871$.
The community is slightly less even than one in which all four species were
equally common.

**4.** EX, EW, CR, EN, VU, NT, LC (plus DD and NE, which are not risk ratings).
**Extinct in the Wild** means no individual survives in the natural habitat and
the species persists only in cultivation, captivity or a naturalised population
outside its past range. **Critically Endangered** means wild individuals still
exist but the species faces an extremely high risk of extinction in the
immediate future, for example a population reduction of 80 % or more over three
generations.

**5.** Any four: **inbreeding depression** — mating between close relatives
exposes harmful recessive alleles and lowers fertility and survival; **genetic
drift / bottleneck effect** — random loss of alleles leaves the population
unable to adapt; **demographic stochasticity** — chance runs of one sex or of
deaths matter enormously when numbers are small; **Allee effect** — below a
threshold density individuals fail to find mates, so per-capita growth becomes
negative; **environmental stochasticity and catastrophes** — one flood, fire or
epidemic can remove the whole population.
:::

**Group C — Long answer (8 marks each)**

1. (a) Describe the protected-area system of Nepal, naming the categories, the
   number in each and one example of each. <span class="marks">[5]</span>
   (b) Explain how the buffer-zone programme makes local people partners in
   conservation. <span class="marks">[3]</span>
2. (a) A grassland census in Shuklaphanta records 60 swamp deer, 25 hog deer,
   10 wild boar and 5 nilgai. Calculate Simpson's index of dominance and
   Simpson's index of diversity. <span class="marks">[4]</span>
   (b) Nepal's rhino population grew from 645 in 2015 to 752 in 2021. Assuming
   exponential growth, find $r$ and the doubling time.
   <span class="marks">[4]</span>
3. Describe the major threats to the wildlife of Nepal and the conservation
   measures taken against each. Support your answer with the example of either
   the tiger or the vulture. <span class="marks">[8]</span>

::: note Answers to Group C
**1. (a)** Nepal's protected areas are managed under the National Parks and
Wildlife Conservation Act, 2029 (1973) and cover 23.39 % of the country.
*National parks* (13) give the strictest protection of a whole ecosystem, with
hunting, grazing and resource removal prohibited — example, Chitwan (1973), a
World Heritage Site. *Wildlife reserve* (1) protects particular species and
their habitat — Koshi Tappu, home of the wild water buffalo. *Hunting reserve*
(1) permits licensed, quota-controlled hunting — Dhorpatan, for blue sheep and
Himalayan tahr. *Conservation areas* (7) are multiple-use areas in which
resident people manage resources through committees — Annapurna, 7,629 km², the
largest protected area in the country. *Buffer zones* surround most parks and
reserves.
**(b)** The 1993 amendment created buffer zones and required that 30–50 % of
park revenue be returned to buffer-zone user committees, which spend it on
schools, drinking water, biogas, alternative energy and predator-proof corrals.
Local people therefore gain directly from a living park; they supply
community-based anti-poaching units with information, plant community forest
that widens wildlife habitat, and accept the cost of crop damage because it is
offset by relief payments. Conservation stops being a contest between park and
village.

**2. (a)** $N = 60 + 25 + 10 + 5 = 100$, so $N(N-1) = 9900$.
$\sum n_i(n_i-1) = 60 \times 59 + 25 \times 24 + 10 \times 9 + 5 \times 4
= 3540 + 600 + 90 + 20 = 4250$.
$D = 4250/9900 = 0.429$; Simpson's index of diversity $= 1 - D = 0.571$.
Dominance is high because swamp deer make up 60 % of the individuals.
**(b)** $t = 2021 - 2015 = 6$ years.
$r = \frac{1}{6}\ln\frac{752}{645} = \frac{1}{6}\ln 1.1659 = \frac{0.1535}{6}
= 0.0256$ year$^{-1}$, i.e. 2.56 % per year.
$t_d = \dfrac{\ln 2}{r} = \dfrac{0.693}{0.0256} = 27.1$ years.

**3.** Expected content — six threats with matched measures. *Poaching and
illegal trade* in rhino horn, tiger bone, musk pods and pangolin scales: army
posts inside parks, community-based anti-poaching units, informant networks,
the CITES Act 2073 and CITES Appendix I listing. *Habitat loss and
fragmentation*: the Terai Arc Landscape links Nepali and Indian parks through
biological corridors, and new highways carry wildlife underpasses. *Human–
wildlife conflict*: relief and compensation payments, predator-proof corrals,
biofences and electric fences. *Invasive species*: manual clearing of *Mikania
micrantha* and grassland management in Chitwan. *Pollution and chemicals*: the
2006 ban on veterinary diclofenac. *Small, isolated populations*: translocation
and captive breeding. Example — the **tiger**: Nepal pledged at the 2010 St
Petersburg summit to double its tigers, protected and connected the five
tiger-bearing parks, controlled poaching, and raised the population from 121 in
2010 to 355 in 2022 and 429 in the 2026 camera-trap survey; the new challenge
is carrying capacity and human–tiger conflict, which Nepal plans to address with
its first tiger sanctuary in Chitwan. Or the **vulture**: *Gyps* populations
fell by over 90 % because diclofenac in cattle carcasses causes kidney failure;
Nepal banned the drug in 2006, promoted meloxicam, opened the Jatayu vulture
restaurant at Pithauli, declared a Vulture Safe Zone of about 30,000 km², bred
birds in captivity and released the first captive-bred white-rumped vultures in
South Asia in 2017, and counts have risen since about 2013.
:::
