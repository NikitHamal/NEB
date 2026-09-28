---
subject: Biology
grade: 11
unit: 5
title: Vegetation
hours: 3
area: Botany
---

Nepal is a small country — about 147,181 km², a little over a tenth of one per
cent of the Earth's land — yet it holds about **3.2 % of the world's known
flora**. The reason is height. In a north–south line barely 193 km long the land
climbs from 59 m in the Terai to 8,848.86 m at Sagarmatha, and every thousand
metres of that climb cools the air by roughly 6 °C. A traveller walking from
Birgunj to the Khumbu passes through as many vegetation belts as a traveller
walking from India to the Arctic. This unit maps those belts, names the trees
that mark them, and asks what Nepal is doing to keep them.

::: key What the examiner asks from this unit
Three things, again and again: (i) **name the vegetation zones with their
altitude ranges and two indicator species each**; (ii) **differentiate in-situ
and ex-situ conservation with named Nepali examples**; (iii) **list human
activities that damage vegetation and the measures that repair it**. Botanical
names are worth marks — write *Shorea robusta*, not just "Sal".
:::

## 5.1 Vegetation

::: definition Vegetation
**Vegetation** is the total plant cover of an area — all the plants growing
there, described by their form and arrangement (forest, scrub, grassland,
meadow) rather than by their names. **Flora**, in contrast, is the *list of
species* found in that area. The Terai has a Sal-forest **vegetation**; its
**flora** includes *Shorea robusta*, *Terminalia alata*, *Mallotus
philippensis* and some 1,800 other flowering plants.
:::

### What decides the vegetation of a place

Four controls do nearly all the work in Nepal:

1. **Altitude.** Temperature falls about **6 °C for every 1,000 m** of climb.
   This single fact produces the belts described below.
2. **Rainfall and the monsoon.** Nepal averages about **1,600 mm** of rain a
   year and roughly **80 % of it falls between June and September**. The east is
   wetter than the west — Taplejung gets about 2,000 mm, Baitadi about 1,000 mm
   — so eastern forests are evergreen and dense where western forests of the
   same altitude are drier and more open. The wettest station, Lumle in Kaski,
   records about 5,550 mm; Jomsom in Mustang, in the rain shadow behind the
   Annapurnas, records under 300 mm.
3. **Aspect** — which way a slope faces. South-facing slopes are hot and dry and
   carry chir pine (*Pinus roxburghii*) and *Quercus semecarpifolia*;
   north-facing slopes at the same height are cool and moist and carry laurels,
   firs and rhododendrons.
4. **Soil and landform.** Fresh river gravel carries khair and sissoo; the
   older, well-drained alluvium behind it carries Sal.

```figure caption="Altitudinal vegetation zones of Nepal along a south–north transect. Temperature falls about $6^\circ$C per 1000 m of climb, and the plant cover changes with it."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.1, 3.4))

XR = 8.6            # terrain occupies x = 0 .. XR ; labels sit to the right
bands = [
    (0,    1000, '#dff0d8', 'Tropical',    'below 1000 m',
     'Sal, khair–sissoo, simal'),
    (1000, 2000, '#e8f0cf', 'Subtropical', '1000–2000 m',
     'chilaune–katus, khote salla, utis'),
    (2000, 3000, '#d9ecef', 'Temperate',   '2000–3000 m',
     'khasru oak, lali gurans, gobre salla'),
    (3000, 4000, '#dfe2f2', 'Subalpine',   '3000–4000 m',
     'talispatra fir, bhojpatra birch'),
    (4000, 5000, '#efe2ee', 'Alpine',      '4000–5000 m',
     'sunpati, dhupi, kharka meadow'),
    (5000, 8800, '#eef1f4', 'Nival',       'above 5000 m',
     'snow, rock; mosses and lichens only'),
]
for y0, y1, col, name, alt, spp in bands:
    ax.add_patch(plt.Rectangle((0, y0), XR, y1 - y0, fc=col, ec='none', zorder=1))
    ax.plot([0, XR + 0.40], [y0, y0], color=GRID, lw=0.6, zorder=2)
    yc = (y0 + y1) / 2 if y1 < 8000 else 6400
    ax.text(XR + 0.55, yc + 175, name + '  ' + alt, fontsize=6.1, color=INK,
            ha='left', va='center', fontweight='bold')
    ax.text(XR + 0.55, yc - 185, spp, fontsize=5.2, color=ACCENT,
            ha='left', va='center')

# terrain profile: Terai -> Chure -> Dun -> Mahabharat -> High Himal -> plateau
xk = [0.0, 1.5, 2.3, 2.9, 3.6, 4.6, 5.4, 6.3, 7.1, 7.7, 8.1, 8.6]
yk = [120, 180, 1250, 700, 2500, 1350, 3100, 4300, 6100, 8100, 6200, 4300]
xs = np.linspace(0, XR, 500)
ys = np.interp(xs, xk, yk)
ax.fill_between(xs, 0, ys, color='#9a9287', alpha=0.62, zorder=3)
ax.plot(xs, ys, color='#5b554e', lw=1.0, zorder=4)

ax.plot([0, XR], [4000, 4000], color='#A8271F', lw=1.0, ls=(0, (4, 2)), zorder=5)
ax.text(0.15, 4180, 'tree line ≈ 4000 m', fontsize=6.0, color='#A8271F',
        ha='left', va='bottom', zorder=6)

ax.set_ylim(0, 8800); ax.set_xlim(0, 13.6)
ax.set_ylabel('altitude (m)', fontsize=7.5)
ax.set_yticks([0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000])
ax.tick_params(axis='y', labelsize=6.4)
ax.set_xticks([0.75, 2.35, 4.5, 6.45, 8.2])
ax.set_xticklabels(['Terai', 'Chure', 'Middle Mts', 'High Mts', 'High Himal'],
                   fontsize=5.5)
ax.tick_params(axis='x', length=0, pad=2)
ax.spines[['top', 'right', 'bottom']].set_visible(False)
```

### The vegetation zones of Nepal

| Zone | Altitude | Forest type and indicator species | Where in Nepal |
|---|---|---|---|
| **Tropical** | below 1000 m | **Sal forest** — *Shorea robusta* (sal), with *Terminalia alata* (saj), *Anogeissus latifolia*, *Mallotus philippensis*; **khair–sissoo riverine forest** — *Acacia catechu* (khayar) and *Dalbergia sissoo* (sissau) on fresh river gravel; *Bombax ceiba* (simal) savanna; *khar-patter* grassland of *Saccharum spontaneum*; tropical **evergreen** forest of *Michelia champaca* (chanp) in the east | Terai, Bhabar, inner Terai (Dun) valleys and Chure slopes — Jhapa to Kanchanpur; Chitwan, Bardiya, Shuklaphanta, Banke, Parsa, Koshi Tappu |
| **Subtropical** | 1000–2000 m | **Schima–Castanopsis forest** — *Schima wallichii* (chilaune) with *Castanopsis indica* (dhalne katus); **chir pine forest** — *Pinus roxburghii* (khote salla) on dry south-facing slopes; *Alnus nepalensis* (utis), a pioneer on landslides and stream banks | Mahabharat midlands — Kathmandu valley rim, Kavre, Dhading, Tanahun, Palpa, Surkhet, Dhankuta, Ilam; Shivapuri Nagarjun NP |
| **Temperate** | 2000–3000 m | **Oak–rhododendron forest** — *Quercus semecarpifolia* (khasru), *Q. lamellosa*, with *Rhododendron arboreum* (lali gurans); **conifers** *Pinus wallichiana* (gobre salla), *Tsuga dumosa* (thingre salla), and in the far west *Cedrus deodara* (devdar); *Acer* and *Juglans regia* (okhar) on moist slopes | Ghorepani and Ghandruk in ACA, Rara NP, Khaptad NP, Langtang, Ilam and Taplejung |
| **Subalpine** | 3000–4000 m | **Fir–birch forest** — *Abies spectabilis* (talispatra, Himalayan silver fir) with *Rhododendron campanulatum* (nilo chimal) beneath; **birch** *Betula utilis* (bhojpatra) in near-pure belts up to the tree line; *Juniperus recurva* (dhupi) in dry inner valleys | Sagarmatha NP, Langtang NP, Makalu Barun, Manaslu and Kanchenjunga CAs, Dhorpatan |
| **Alpine** | 4000–5000 m | **Treeless.** Alpine **scrub** of *Rhododendron anthopogon* (sunpati) and *Juniperus indica*; above it **alpine meadow** (*kharka*, *patan*) of *Kobresia* and *Carex* sedges with *Primula*, *Gentiana* and *Meconopsis*; the medicinal belt of yarsagumba, jatamansi, panchaunle and kutki | High Himal of all northern districts — Solukhumbu, Rasuwa, Manang, Mustang, Dolpa, Humla, Darchula |
| **Nival (Arctic)** | above 5000 m | Permanent snow, rock and glacier. Only mosses, lichens and cushion plants such as *Stellaria decumbens*, recorded as high as about 6,100 m | Above the snow line everywhere; Sagarmatha, Kanchenjunga, Api Nampa |

Behind the Himalayan wall lies a seventh kind of country. **Upper Mustang,
Manang, Dolpa and Humla** lie in the **rain shadow** and receive only about
**250 mm** of rain a year — less than a tenth of Pokhara. The vegetation there is
**trans-Himalayan steppe**, or cold desert: thorny cushion shrubs of *Caragana*
and *Lonicera spinosa*, *Artemisia*, *Ephedra gerardiana*, with *Hippophae*
(sea buckthorn) and willows along the streams and *Juniperus indica* on the
better-watered slopes. Ground cover is thin and bare gravel is everywhere.

::: memory The six zones, bottom to top
**T–S–T–S–A–N** — **T**ropical, **S**ubtropical, **T**emperate, **S**ubalpine,
**A**lpine, **N**ival. The first five boundaries fall at neat thousands:
1000, 2000, 3000, 4000, 5000 m. Remember the tree line at about **4000 m** —
below it you can still find a forest, above it you cannot.
:::

```photo id="bio11/sal-forest" caption="Tropical Sal (*Shorea robusta*) forest in Chitwan National Park — the dominant vegetation of Nepal below 1000 m." width="92"
crop 0.02 0.02 0.98 0.99
```

```photo id="bio11/rhododendron-forest" caption="Temperate oak–rhododendron forest in the Annapurna Conservation Area. *Rhododendron arboreum* (lali gurans), Nepal's national flower, flowers between about 2000 and 3000 m in March and April." width="86"
crop 0.14 0.00 0.80 1.00
```

```photo id="bio11/khaptad-patan" caption="A subalpine meadow (*patan*) in Khaptad National Park, with the conifer forest ending on the ridge above it. Meadows like this are grazed by cattle and sheep through the summer and left empty in winter." width="88"
crop 0.00 0.34 0.56 1.00
call 0.45 0.88 0.76 0.61 "conifer forest and tree line"
call 0.30 0.47 0.52 0.27 "open grazing meadow"
```

::: example Worked example 5.1
**Problem.** The mean March temperature at Hetauda (altitude 400 m) is 26 °C. A
student walks from Hetauda up to Daman (altitude 2,300 m). Taking the lapse rate
as 6 °C per 1,000 m, estimate the temperature at Daman, and name the vegetation
zones crossed on the way.

**Solution.** The gain in height is

$$ \Delta h = 2300 - 400 = 1900\ \text{m} $$

The fall in temperature is the lapse rate multiplied by the height gained:

$$ \Delta T = 6\ ^\circ\text{C per 1000 m} \times \frac{1900}{1000}
= 11.4\ ^\circ\text{C} $$

$$ T_{\text{Daman}} = 26 - 11.4 = 14.6\ ^\circ\text{C} $$

The walk starts at 400 m in the **tropical** zone (Sal forest), crosses 1,000 m
into the **subtropical** zone (chir pine and chilaune–katus) and ends at 2,300 m
in the **temperate** zone (oak and rhododendron). Three zones in one day's walk.
:::

### The flora of Nepal in numbers

| Group | Species recorded in Nepal |
|---|---|
| Flowering plants (angiosperms) | about **5,600** |
| Gymnosperms | 26 |
| Pteridophytes (ferns and allies) | 583 |
| Bryophytes | 1,217 |
| Lichens | 1,086 |
| Fungi | 2,470 |
| Algae | 1,101 |
| **Endemic** flowering plants (found nowhere else) | **348** |

*Figures: Department of Plant Resources, 2025.* Orchidaceae is the largest
family, with about **500 orchid species**; Nepal has roughly **30 species of
Rhododendron**, of which *Rhododendron arboreum* (lali gurans) is the **national
flower**. Forest covers **43.4 %** of the country, and forest together with other
wooded land covers **46.1 %** (Forest Research and Training Centre, 2024) —
second only to Bhutan in South Asia.

### In-situ conservation

::: definition In-situ and ex-situ conservation
**In-situ conservation** is the protection of species **inside their natural
habitat**, by protecting the habitat itself — national parks, reserves,
conservation areas, community forests. **Ex-situ conservation** is the
protection of species **outside their natural habitat**, in botanical gardens,
gene banks, herbaria, tissue-culture laboratories and zoos.
:::

In-situ conservation is the stronger method, because it saves not one species
but the whole community it belongs to, and the species keeps evolving in the
conditions it is adapted to. Nepal's legal instrument is the **National Parks
and Wildlife Conservation Act, 1973 (2029 BS)**, which created the first
protected area, **Chitwan National Park, in 1973**.

| Category | Number | Examples and notes |
|---|---|---|
| National parks | **13** | Chitwan (1973, the first, and a natural World Heritage Site since 1984); Sagarmatha (1976, World Heritage 1979); Langtang; Rara (106 km², the smallest); Shey Phoksundo (the largest park); Khaptad; Bardiya; Makalu Barun; Shivapuri Nagarjun; Banke (2010); Shuklaphanta and Parsa (upgraded from reserves in 2017); Chhayanath, Mugu (2025) |
| Wildlife reserve | **1** | Koshi Tappu (1976), Sunsari–Saptari–Udayapur — the last home of the wild buffalo (*arna*) |
| Hunting reserve | **1** | Dhorpatan (1987), Baglung–Myagdi–Rukum — the only reserve where licensed hunting is allowed |
| Conservation areas | **6** | Annapurna (1992; 7,629 km², the largest protected area in Nepal), Kanchenjunga, Manaslu, Gaurishankar, Api Nampa, and Krishnasar (Blackbuck) in Bardiya — at 16.95 km² the smallest |
| Buffer zones | 13 | Declared around parks and reserves; **30–50 %** of the park's income is returned to buffer-zone communities |
| Ramsar (wetland) sites | **10** | Koshi Tappu (1987, the first), Beeshazari Tal, Ghodaghodi Tal, Jagdishpur reservoir, Rara, Phoksundo, Gosaikunda, Gokyo, Mai Pokhari, and the Lake Cluster of Pokhara Valley (2016, the largest) |

Together the protected areas cover about **34,420 km², roughly 23.4 % of
Nepal's land area** — one of the highest proportions in Asia. Outside them,
**community forestry** does the same work by another route: about **23,000
community forest user groups (CFUGs)** manage some **2.5 million hectares**,
close to **39 % of the national forest**, on behalf of more than three million
households. Religious forests, leasehold forests for poor households, and the
sacred groves around temples and *deurali* resting places add to the total.

::: caution How many national parks does Nepal have?
Older textbooks and the department's own website still say **12 national parks
and 20 protected areas**. Chhayanath National Park (Mugu) was declared in 2025
by **splitting off part of Shey Phoksundo**, so the number of parks rose to 13
and the total to 21 while the total protected **area** hardly changed. Either
count is accepted in the exam **provided you name the parks correctly** — the
marks are for the names and the categories, not for the total.
:::

### Ex-situ conservation

Ex-situ methods are the back-up. They matter most for species already too rare
to survive in the wild, for crop varieties that farmers have stopped growing,
and for keeping material available to researchers and breeders.

```photo id="bio11/godawari-garden" caption="The National Botanical Garden at Godawari, Lalitpur. Every accession carries a plate with its Nepali name, English name, botanical name and family — here *Pandanus nepalensis* (kewara, Pandanaceae). Documented identity is what separates a botanical garden from a park." width="82"
crop 0.06 0.04 0.94 0.99
call 0.50 0.15 0.40 0.31 "species name-plate"
```

| Facility | Where | What it conserves |
|---|---|---|
| **National Botanical Garden** (est. **1962**, 82 ha) | **Godawari, Lalitpur** | Over 1,285 living plant species in about 30 themed gardens; one of **11 botanical gardens** run by the Department of Plant Resources, from Ilam in the east to Kailali in the west |
| **National Herbarium and Plant Laboratories (KATH)** (est. 1961) | Godawari, Lalitpur | About **170,000 dried, mounted and named herbarium specimens** — the reference collection against which any Nepali plant is identified |
| **National Gene Bank** — National Agriculture Genetic Resources Centre, NARC (est. **2010**) | **Khumaltar, Lalitpur** | About **11,800 seed accessions of more than 330 crop species** stored at **−20 °C**, plus a field gene bank, an in-vitro (tissue-culture) bank and a DNA bank |
| **Community seed banks** (first at Dalchowki, Lalitpur, 1994) | About 54 across the country | Local landraces of rice, maize, millet and beans, kept and exchanged by farmers themselves |
| **Central Zoo** (est. **1932**, about 6 ha; run by NTNC since 1995) | **Jawalakhel, Lalitpur** | Nepal's only zoo — roughly 1,300 animals of about 120 species, and a rescue centre |
| **Gharial Breeding Centre** (est. 1978) | Kasara, Chitwan | Captive breeding of the gharial crocodile; over 1,800 juveniles released into Nepal's rivers |

::: tip Answering "differentiate in-situ and ex-situ conservation"
Draw a two-column table and fill **four rows**: (i) where the organism is kept;
(ii) whether the whole ecosystem is conserved; (iii) whether evolution continues;
(iv) cost and number of individuals possible. Then give **two named Nepali
examples of each**. A pair of examples is usually worth a mark on its own.
:::

```figure caption="Conservation of plant diversity in Nepal: the two routes, with the institutions that carry them out."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1, 3.6))

def box(xc, yc, w, h, s, fc, fs=5.5, bold=False):
    ax.add_patch(FancyBboxPatch((xc - w/2, yc - h/2), w, h,
                 boxstyle='round,pad=0,rounding_size=0.14',
                 fc=fc, ec=INK, lw=0.85, zorder=4))
    ax.text(xc, yc, s, fontsize=fs, ha='center', va='center', color=INK,
            zorder=5, fontweight='bold' if bold else 'normal')

def link(x1, y1, x2, y2):
    ax.plot([x1, x1, x2, x2], [y1, (y1+y2)/2, (y1+y2)/2, y2],
            color=MUTED, lw=0.9, zorder=2, solid_joinstyle='miter')

GRN, BLU, CRM = '#d8ead8', '#cfe3f3', '#f6ecd8'
box(6.0, 11.35, 7.4, 0.95, 'CONSERVATION OF PLANT DIVERSITY', CRM, fs=6.4, bold=True)
box(2.85, 9.75, 4.9, 0.95, 'IN-SITU\nin the natural habitat', GRN, fs=6.2, bold=True)
box(9.15, 9.75, 4.9, 0.95, 'EX-SITU\noutside the natural habitat', BLU, fs=6.2, bold=True)
link(6.0, 10.87, 2.85, 10.23)
link(6.0, 10.87, 9.15, 10.23)

L = ['National parks — 13\nChitwan (1973), Sagarmatha',
     'Wildlife reserve — Koshi Tappu\nHunting reserve — Dhorpatan',
     'Conservation areas — 6\nAnnapurna (largest, 7629 km²)',
     'Buffer zones — 13\nRamsar wetland sites — 10',
     'Community, leasehold and\nreligious forests; sacred groves']
R = ['Botanical gardens — 11\nGodawari, Lalitpur (1962)',
     'Herbarium\nNational Herbarium (KATH), Godawari',
     'Seed gene bank\nNAGRC, Khumaltar (2010)',
     'Tissue culture, in-vitro and\nDNA banks; community seed banks',
     'Zoo and captive breeding\nCentral Zoo (1932); Kasara gharials']

ys = [8.15, 6.55, 4.95, 3.35, 1.75]
for i, y in enumerate(ys):
    box(2.85, y, 5.1, 1.20, L[i], GRN)
    box(9.15, y, 5.1, 1.20, R[i], BLU)
link(2.85, 9.27, 2.85, 8.75)
link(9.15, 9.27, 9.15, 8.75)
for a, b in zip(ys[:-1], ys[1:]):
    ax.plot([2.85, 2.85], [a - 0.60, b + 0.60], color=MUTED, lw=0.9, zorder=2)
    ax.plot([9.15, 9.15], [a - 0.60, b + 0.60], color=MUTED, lw=0.9, zorder=2)

ax.set_xlim(0.1, 11.9); ax.set_ylim(1.0, 11.95)
ax.axis('off')
```

::: example Worked example 5.2
**Problem.** Nepal's protected areas cover 34,420 km² and its total land area is
147,181 km². Forest covers 43.4 % of the country. Calculate (a) the percentage
of Nepal that is protected, and (b) the area of Nepal under forest, in km² and
in hectares.

**Solution.**

(a) Percentage protected:

$$ \frac{34{,}420}{147{,}181} \times 100 = 23.4\ \% $$

(b) Forest area:

$$ A = \frac{43.4}{100} \times 147{,}181 = 63{,}876\ \text{km}^2 $$

One square kilometre is 100 hectares, so

$$ 63{,}876 \times 100 = 6.39 \times 10^{6}\ \text{hectares} $$

About **6.4 million hectares** of Nepal is forest, and just under a quarter of
the country is inside a protected area.
:::

::: example Worked example 5.3
**Problem.** About 23,000 community forest user groups manage 2.5 million
hectares of Nepal's forest. Taking the national forest area as 6.4 million
hectares, find (a) the average area handed to one user group, and (b) the
percentage of Nepal's forest that is community-managed.

**Solution.**

(a) Average area per group:

$$ \frac{2{,}500{,}000\ \text{ha}}{23{,}000} = 108.7\ \text{ha} $$

(b) Share of the national forest:

$$ \frac{2.5}{6.4} \times 100 = 39.1\ \% $$

So a typical community forest is only about **109 hectares** — roughly a square
kilometre — yet together these small patches make up nearly **two-fifths** of
Nepal's forest. That is why community forestry, not the protected-area system,
is what most Nepali villagers actually experience as conservation.
:::

## 5.2 Natural environment, vegetation and human activities

Vegetation sits between the physical environment and the people who live in it,
and the influence runs in all three directions.

### What people take from vegetation

Firewood is still the main cooking fuel in most rural Nepali households.
Forests also supply timber, fodder for stall-fed cattle, leaf litter that
becomes compost for the fields, bamboo, and **non-timber forest products
(NTFPs)** — *Swertia chirayita* (chiraito), *Nardostachys jatamansi*
(jatamansi), *Zanthoxylum armatum* (timur), *Cinnamomum tamala* (tejpat) and
yarsagumba, which together earn rural households a large cash income. Beyond the
products, vegetation holds soil on steep slopes, slows monsoon runoff, recharges
springs, stores carbon, and brings the trekkers whose money supports whole
districts.

### How human activities damage vegetation

| Activity | What it does |
|---|---|
| **Deforestation and encroachment** | Clearing for settlement, roads and cropland; worst in the Terai and inner Terai after malaria control opened them to settlement in the 1950s and 60s |
| **Shifting cultivation (*khoriya*)** | Slash-and-burn on hill slopes in the east; the fallow period is now too short for the forest to recover |
| **Overgrazing** | Too many cattle, goats and sheep on the same pasture; seedlings are eaten before they can establish, and alpine meadows are worn to bare soil |
| **Forest fire** | Deliberate pre-monsoon burning (March–May) to bring on fresh grass; it kills regeneration and dries the soil |
| **Lopping and illegal felling** | Repeated lopping of Sal and oak for fodder and fuel leaves stunted, hollow trees |
| **Over-collection of NTFPs** | Yarsagumba, panchaunle and jatamansi are dug up before they can set seed |
| **Quarrying and road building in the Chure** | Sand, gravel and boulder extraction destabilises the Chure, which is the recharge zone for Terai groundwater |
| **Invasive alien species** | *Mikania micrantha* smothers Sal regeneration in Chitwan; *Eichhornia crassipes* (water hyacinth) blankets Phewa Tal; *Lantana camara*, *Chromolaena odorata* and *Parthenium hysterophorus* take over grazing land |
| **Pollution and infrastructure** | Brick kilns, cement dust, hydropower reservoirs and transmission lines |

The consequences are visible: soil erosion and landslides, sheet flooding when
the Chure rivers spill onto the Terai, a falling Terai water table, the loss of
species before they are even described, and an upward shift of the tree line as
the climate warms.

### What is being done

- **Community forestry** — handing national forest to local user groups. Forest
  cover in the mid-hills has increased measurably since the 1990s, the clearest
  conservation success Nepal has had.
- **Leasehold forestry** for poor households, and **agroforestry** — growing
  fodder and fruit trees on private land so that pressure on the forest falls.
- **Protected areas and buffer zones**, with revenue sharing so that local
  people gain from conservation rather than lose by it.
- **The President Chure–Terai Madhesh Conservation Programme**, which bans
  riverbed mining in sensitive stretches and restores degraded Chure catchments.
- **Alternative energy** — biogas plants, improved cooking stoves, micro-hydro
  and LPG reduce firewood demand.
- **Law.** The **Forest Act, 2019 (2076 BS)** protects named species. Two are
  banned outright from collection, sale, transport and export —
  *Dactylorhiza hatagirea* (panchaunle) and the bark of *Juglans regia* (okhar).
  Seven, including *Abies spectabilis*, *Nardostachys jatamansi*, *Taxus* spp.
  and *Rauvolfia serpentina*, may not be exported unprocessed. Four trees —
  *Shorea robusta*, *Dalbergia latifolia* (satisal), *Pterocarpus marsupium*
  (bijayasal) and *Juglans regia* — may not be felled or transported for
  commercial purposes.

::: caution Conservation is not the same as preservation
**Preservation** locks people out. **Conservation** manages use so that the
resource survives — a community forest that supplies firewood every year and
still grows thicker is being conserved, not preserved. NEB answers that describe
conservation as "stopping all use of the forest" lose marks.
:::

## Chapter summary

- **Vegetation** is the plant cover of an area; **flora** is the list of species
  in it. Nepal holds about 3.2 % of world flora on under 0.1 % of world land.
- Temperature falls about **6 °C per 1000 m**, which produces six altitudinal
  zones: **Tropical** (<1000 m, Sal), **Subtropical** (1000–2000 m,
  chilaune–katus and chir pine), **Temperate** (2000–3000 m, oak and
  rhododendron), **Subalpine** (3000–4000 m, fir and birch), **Alpine**
  (4000–5000 m, scrub and meadow) and **Nival** (>5000 m, snow).
- The **tree line** lies near **4000 m**. Behind the Himalaya, the
  **trans-Himalayan steppe** of Mustang, Manang and Dolpa gets only about
  250 mm of rain and carries *Caragana*, *Artemisia* and *Hippophae*.
- **In-situ** conservation protects the habitat: 13 national parks, 1 wildlife
  reserve (Koshi Tappu), 1 hunting reserve (Dhorpatan), 6 conservation areas,
  13 buffer zones and 10 Ramsar sites — about **23.4 %** of the country.
  Chitwan (1973) was the first; Annapurna (1992) is the largest.
- **Ex-situ** conservation protects the organism away from its habitat: the
  National Botanical Garden at **Godawari** (1962), the National Herbarium
  (KATH), the **National Gene Bank at Khumaltar** (2010), community seed banks,
  and the **Central Zoo, Jawalakhel** (1932).
- About **23,000 CFUGs** manage **2.5 million ha**, nearly 39 % of Nepal's
  forest. Forest covers **43.4 %** of the country.
- Vegetation is damaged by deforestation, *khoriya*, overgrazing, fire,
  over-collection of NTFPs, Chure quarrying and invasive species such as
  *Mikania micrantha* and *Eichhornia crassipes*; it is repaired by community
  forestry, agroforestry, buffer-zone sharing, alternative energy and the
  Forest Act, 2019.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The altitudinal range of the temperate vegetation zone of Nepal is <span class="marks">[1]</span>
   (a) below 1000 m (b) 1000–2000 m (c) 2000–3000 m (d) 3000–4000 m
2. *Shorea robusta* is the dominant tree of the <span class="marks">[1]</span>
   (a) tropical zone (b) subtropical zone (c) temperate zone (d) subalpine zone
3. The first national park of Nepal, established in 1973, is <span class="marks">[1]</span>
   (a) Sagarmatha (b) Langtang (c) Chitwan (d) Rara
4. The National Gene Bank of Nepal is located at <span class="marks">[1]</span>
   (a) Godawari (b) Khumaltar (c) Jawalakhel (d) Kasara
5. *Betula utilis* (bhojpatra) is characteristic of the <span class="marks">[1]</span>
   (a) tropical zone (b) temperate zone (c) subalpine zone (d) nival zone
6. Conservation of a species in a botanical garden is an example of <span class="marks">[1]</span>
   (a) in-situ conservation (b) ex-situ conservation (c) buffer zone management (d) community forestry

::: note Answers to Group A
**1.** (c) — the temperate belt runs from 2000 m to 3000 m, the oak–rhododendron zone.
**2.** (a) — Sal is the dominant tree of the Terai, Bhabar and Dun valleys, below 1000 m.
**3.** (c) — Chitwan, 1973; Sagarmatha, Langtang and Rara followed in 1976.
**4.** (b) — the National Agriculture Genetic Resources Centre, NARC, Khumaltar, Lalitpur.
**5.** (c) — Himalayan birch forms near-pure belts from about 3300 m to the tree line.
**6.** (b) — the plant is kept outside its natural habitat, so it is ex-situ.
:::

**Group B — Short answer (4 marks each)**

1. Name the six altitudinal vegetation zones of Nepal with their altitude
   ranges, and give one indicator species of each. <span class="marks">[4]</span>
2. Differentiate between in-situ and ex-situ conservation, giving two named
   Nepali examples of each. <span class="marks">[4]</span>
3. The mean annual temperature at Pokhara (altitude 820 m) is 20 °C. Using a
   lapse rate of 6 °C per 1000 m, estimate the temperature at Ghorepani
   (2,870 m), and name the vegetation zone and the indicator tree species you
   would expect to find there. <span class="marks">[4]</span>
4. List any four human activities that degrade the vegetation of Nepal, and
   state one control measure for each. <span class="marks">[4]</span>

::: note Answers to Group B
**1.** Tropical, below 1000 m — *Shorea robusta*. Subtropical, 1000–2000 m —
*Schima wallichii* or *Pinus roxburghii*. Temperate, 2000–3000 m —
*Quercus semecarpifolia* or *Rhododendron arboreum*. Subalpine, 3000–4000 m —
*Abies spectabilis* or *Betula utilis*. Alpine, 4000–5000 m —
*Rhododendron anthopogon* with *Kobresia* meadow. Nival, above 5000 m —
mosses and lichens only.

**2.** In-situ = conserved **inside** the natural habitat, so the whole
ecosystem is saved and the species keeps evolving; cheap per species but needs
large areas. Examples: **Chitwan National Park**, **Koshi Tappu Wildlife
Reserve**. Ex-situ = conserved **outside** the natural habitat, under human
care; useful for species too rare to survive in the wild, but expensive and only
a few individuals can be held. Examples: **National Botanical Garden, Godawari**;
**National Gene Bank, Khumaltar** (or the Central Zoo, Jawalakhel).

**3.** Height gained $= 2870 - 820 = 2050\ \text{m}$. Temperature fall
$= 6 \times 2050/1000 = 12.3\ ^\circ\text{C}$, so
$T = 20 - 12.3 = 7.7\ ^\circ\text{C}$. At 2,870 m Ghorepani lies in the
**temperate zone**, where the expected species are *Quercus semecarpifolia*
(khasru), *Rhododendron arboreum* (lali gurans) and *Pinus wallichiana*
(gobre salla).

**4.** (i) Deforestation and encroachment — hand the forest to community forest
user groups and register boundaries. (ii) Overgrazing — fix a stocking limit and
rotate the *kharka*, and promote stall feeding on fodder trees. (iii) Forest
fire — build fire lines, train community fire-fighting groups and ban
pre-monsoon burning. (iv) Over-collection of NTFPs such as yarsagumba — issue
harvesting permits with a closed season, and cultivate the species instead of
digging it from the wild. (A fifth: invasive species such as *Mikania micrantha*
— manual uprooting before flowering and replanting with native species.)
:::

**Group C — Long answer (8 marks each)**

1. Describe the types of vegetation found in Nepal from the Terai to the snow
   line, with a labelled diagram showing altitude, and explain why so many
   vegetation types occur in such a small country. <span class="marks">[8]</span>
2. (a) Define in-situ and ex-situ conservation. <span class="marks">[2]</span>
   (b) Describe the protected area system of Nepal, naming the categories, their
   numbers and one example of each. <span class="marks">[4]</span>
   (c) Describe any two ex-situ conservation facilities of Nepal, stating where
   each is and what it conserves. <span class="marks">[2]</span>

::: note Answer outline to Group C question 1
Diagram: the altitude profile of this chapter — a rising transect from Terai to
High Himal with horizontal bands at 1000, 2000, 3000, 4000 and 5000 m, each band
named and given two indicator species, and the tree line marked at about 4000 m.

Points to make: (i) **Tropical** below 1000 m — Sal forest of *Shorea robusta*
with *Terminalia alata*, khair–sissoo riverine forest of *Acacia catechu* and
*Dalbergia sissoo*, and *Saccharum* grassland; Terai, Bhabar and Dun valleys.
(ii) **Subtropical** 1000–2000 m — *Schima wallichii* with *Castanopsis indica*,
chir pine *Pinus roxburghii* on dry south slopes, *Alnus nepalensis* on stream
banks; the Mahabharat midlands. (iii) **Temperate** 2000–3000 m — oak
*Quercus semecarpifolia* with *Rhododendron arboreum*, blue pine
*Pinus wallichiana*, *Tsuga dumosa*. (iv) **Subalpine** 3000–4000 m — silver fir
*Abies spectabilis* and birch *Betula utilis* with *Rhododendron campanulatum*.
(v) **Alpine** 4000–5000 m — treeless scrub of *Rhododendron anthopogon* and
*Juniperus*, and *Kobresia* meadows grazed in summer. (vi) **Nival** above
5000 m — snow and rock, mosses and lichens only. (vii) The **trans-Himalayan**
cold desert of Mustang, Manang and Dolpa, with about 250 mm of rain,
*Caragana*, *Artemisia* and *Hippophae*.

Why so many: the land rises from 59 m to 8,848 m within 193 km, so temperature
falls about 6 °C per 1000 m and produces belt after belt; the monsoon makes the
east wetter than the west; aspect separates dry south-facing from moist
north-facing slopes; and the Himalaya casts a rain shadow that creates a cold
desert on its northern side. Nepal therefore carries tropical and arctic
vegetation in the same country.
:::
