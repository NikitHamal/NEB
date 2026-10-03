---
subject: Biology
grade: 12
unit: 10
title: Applied Biology
hours: 16
area: Zoology
---

Everything in the previous nine units was biology for its own sake. This unit is
biology that earns a living. Sixteen hours are given to two questions: what do
people actually *do* with animals, and what do microorganisms do to us and for
us. The answers are local — the honey in a Gandaki bazaar, the carp in a Terai
pond, the buffalo that supplies more than half of Nepal's milk, the sputum smear
read in a district hospital. Learn the organism's correct name, the technique,
and one Nepali number for each; that combination is what an 8-mark answer needs.

::: key What the examiner asks from this unit
Section II reliably takes two or three short questions from here and often one
long question. The long question is almost always either "describe the method of
X culture and its economic importance" (apiculture, sericulture, pisciculture,
poultry) or a disease question — "name the causative agent, mode of
transmission, symptoms and preventive measures of any four communicable
diseases". Both are pure recall, so the marks are cheap if your scientific names
and vectors are exact. Markers deduct for *Salmonella typhi*, for "*Apis
indica*", and for naming *Culex* as the malaria vector.
:::

## 10.1 Application of Zoology

**Applied zoology** is the use of animals, and of knowledge about animals, for
human benefit. In Nepal it is not a minor sideline: livestock and fisheries
together contribute roughly a quarter of agricultural value, and for a hill
household a few hives or a buffalo may be the only source of cash income. The
seven practices below are the ones the syllabus names.

::: note Where the Nepali figures in this section come from
Every production number quoted here is from one source — the Ministry of
Agriculture and Livestock Development, *Statistical Information on Nepalese
Agriculture 2081/82 (2024/25)*. Do not mix these fiscal-year figures with
FAOSTAT calendar-year figures in the same table; the two series are counted
differently. Note also that Nepal re-based its livestock census in 2022/23, so
cattle and buffalo numbers before and after that year cannot be compared.
:::

| Product | Nepal, FY 2081/82 (2024/25) |
|---|---|
| Honey | 4,278 metric tonnes from 276,000 hives |
| Milk (total) | 2,718,177 MT — buffalo 1,416,083 (52.1 %), cow 1,302,094 (47.9 %) |
| Fish (total) | 131,112 MT — aquaculture 110,112 (84 %), capture 21,000 (16 %) |
| Pond carp culture | 88,254 MT from 15,707 ha; yield 5.62 t ha⁻¹; Terai gives 96 % |
| Rainbow trout | 1,332 MT |
| Eggs | 1,632,289 thousand (about 1.63 billion) |
| Chicken meat | 182,516 MT |
| Livestock numbers | cattle 5,141,391; buffalo 3,294,723; goat 15,954,080; sheep 652,742; fowl 56,391,680 |

### Apiculture — beekeeping

**Apiculture** is the rearing and management of honey bees in artificial hives
for honey, beeswax and, above all, pollination. The bees belong to the genus
*Apis* (order Hymenoptera, family Apidae).

Five species of *Apis* matter economically in Nepal, and only one of them is not
native.

| Species | Common name | Nest | Hiveable? |
|---|---|---|---|
| *Apis cerana* | Asian hive bee, *mauri* | several parallel combs inside a dark cavity | **yes** — the traditional and the movable-frame hive bee |
| *Apis mellifera* | European hive bee | several combs in a cavity | **yes** — introduced to Nepal in **1992** |
| *Apis dorsata* | giant rock bee, *bhanmauri* | one huge open comb on a tree or cliff, sometimes nearly 3 m across | no — wild, honey hunted |
| *Apis laboriosa* | Himalayan cliff bee | one open comb under a vertical cliff overhang, 2,500–3,000 m | no — wild, honey hunted |
| *Apis florea* | little bee | one small open comb on a shrub | no |

*A. cerana* is the mainstay of Nepali beekeeping — about three-quarters of the
country's hives — because it nests in cavities and so can be persuaded into a
box, and because it survives at altitude up to about 3,500 m. Its colonies are
small, roughly 6,000–7,000 workers, against tens of thousands in *A. mellifera*.
*A. laboriosa* is the **largest honey bee in the world**, with adults reaching
3 cm; a single comb may hold 60 kg of honey, and it was confirmed as a full
species distinct from *A. dorsata* only in 2020.

::: caution Names that lose marks
Write ***Apis cerana***. "*Apis indica*" and "*Apis cerana indica*" are obsolete
names still printed in old textbooks. And *A. laboriosa* is the largest **honey
bee**, not the largest bee — the leaf-cutter *Megachile pluto* is bigger.
:::

**The colony.** A honey bee colony is a rigid caste society of one **queen**, a
few hundred **drones** and thousands of **workers**, all of them the queen's
offspring.

- **Queen** — the only fertile female; lays up to a couple of thousand eggs a
  day; stores sperm from her mating flights in a **spermatheca** and controls
  whether each egg is fertilised.
- **Drone** — male, develops from an **unfertilised egg** and is therefore
  **haploid** (this is *arrhenotokous parthenogenesis*); its only function is
  mating.
- **Worker** — a sterile female; in sequence over her life she cleans cells,
  nurses larvae, builds comb, guards the entrance and finally forages.

All three castes hatch from the egg in **3 days**. The adult emerges after
**16 days** in the queen, **21 days** in the worker and **24 days** in the drone
(figures for *A. mellifera*). The difference is diet, not genes: **royal jelly**,
secreted by the hypopharyngeal glands of nurse workers, is fed to *every* larva
for the first three days or so, but only the queen larva continues on it.

::: caution "Only the queen gets royal jelly"
A very common error. All larvae are fed royal jelly for about three days; worker
and drone larvae are then weaned onto a bread of honey and pollen, while the
queen larva is kept on royal jelly throughout. Continuous feeding, not exclusive
feeding, makes the queen.
:::

```figure caption="Vertical section of a modern movable-frame hive. The whole design rests on one discovery: bees neither build comb in nor seal up a gap of 6.4–9.5 mm, so every frame surrounded by that gap lifts out clean."
fig, ax = plt.subplots(figsize=(5.0, 4.1))
ax.set_xlim(0, 15.2); ax.set_ylim(0, 10.4); ax.axis("off")
R = matplotlib.patches.Rectangle
HX = 3.25; HW = 5.30

def band(y0, h, fc, ec, lw=1.2):
    ax.add_patch(R((HX, y0), HW, h, fc=fc, ec=ec, lw=lw, zorder=3))

def tag(y, text, sub=None):
    ax.plot([HX + HW, HX + HW + 0.55], [y, y], color=MUTED, lw=0.8, zorder=2)
    ax.text(HX + HW + 0.72, y, text, ha="left", va="center",
            fontsize=6.6, color=INK, zorder=4)
    if sub:
        ax.text(HX + HW + 0.72, y - 0.44, sub, ha="left", va="center",
                fontsize=5.7, color=MUTED, style="italic", zorder=4)

band(8.95, 0.75, "#e6e9ee", INK); tag(9.32, "outer cover (roof)")
band(8.35, 0.60, "#f3f1ea", INK); tag(8.62, "inner cover")
band(6.05, 2.30, "#fbf6e6", "#b8860b", 1.3)
tag(7.20, "super (honey chamber)", "capped honey is harvested from here")
for xs in np.linspace(HX + 0.44, HX + HW - 0.44, 7):
    ax.add_patch(R((xs - 0.20, 6.18), 0.40, 2.04, fc="#f0e2b6",
                   ec="#b8860b", lw=0.8, zorder=4))
    ax.add_patch(R((xs - 0.20, 7.55), 0.40, 0.67, fc="#fdfbf2",
                   ec="#b8860b", lw=0.6, zorder=5))
band(5.60, 0.45, "#eef0f3", INK)
for xq in np.linspace(HX + 0.25, HX + HW - 0.25, 16):
    ax.plot([xq, xq], [5.66, 5.99], color=MUTED, lw=0.7, zorder=4)
tag(5.82, "queen excluder", "workers pass, the larger queen cannot")
band(2.20, 3.40, "#f6efe6", "#8F5507", 1.3)
tag(3.90, "brood chamber", "the queen lays here; frames of brood")
fx = np.linspace(HX + 0.44, HX + HW - 0.44, 7)
for xf in fx:
    ax.add_patch(R((xf - 0.20, 2.42), 0.40, 2.96, fc="#e5d4ba",
                   ec="#8F5507", lw=0.8, zorder=4))
band(1.45, 0.75, "#e6e9ee", INK)
ax.add_patch(R((HX + 1.5, 1.52), 2.3, 0.28, fc=INK, ec="none", zorder=5))
tag(1.82, "bottom board and entrance")
ax.add_patch(R((HX + 0.35, 0.55), HW - 0.70, 0.60, fc="#dfe3ea",
               ec=MUTED, lw=1.0, zorder=3))
ax.text(HX + HW / 2, 0.85, "hive stand", ha="center", va="center",
        fontsize=6.0, color=MUTED, zorder=4)

# highlight one inter-frame gap and label it from the left margin
gx = (fx[2] + fx[3]) / 2
gw = (fx[3] - fx[2]) - 0.40
ax.add_patch(R((gx - gw / 2, 2.42), gw, 2.96, fc="#d9534f", alpha=0.30,
                ec="#d9534f", lw=1.0, zorder=5))
ax.annotate("", xy=(gx - gw / 2, 3.90), xytext=(2.05, 3.90),
            arrowprops=dict(arrowstyle="-|>", color="#d9534f", lw=1.0,
                            mutation_scale=9), zorder=6)
ax.text(1.90, 3.90, "bee space\n6.4–9.5 mm", ha="right", va="center",
        fontsize=6.4, color="#d9534f", linespacing=1.3, zorder=6)
ax.text(1.90, 2.85, "the gap bees\nneither fill with comb\nnor seal with propolis",
        ha="right", va="center", fontsize=5.6, color=MUTED,
        style="italic", linespacing=1.3, zorder=6)
fig.tight_layout()
```

**The movable-frame hive.** Before 1851 a hive could be robbed only by cutting
out the comb and usually destroying the colony. In that year the American
clergyman **L. L. Langstroth** observed that bees leave a gap of about
**6.4–9.5 mm** — the **bee space** — free of both comb and propolis. Build a box
whose frames are separated from each other and from the walls by exactly that
gap and every frame lifts out undamaged. Langstroth patented the design on
**5 October 1852**, and every commercial hive since is a variation on it. In
Nepal, *A. cerana* is also kept in the **Newton hive**, a movable-frame hive
sized for the smaller Asian bee, and still, widely, in traditional log and wall
hives.

```photo id="bio12/bee-frame" caption="An open hive with the cover lifted off. The top bars of the frames run across the back; one comb is seen in full face. Pale wax cappings seal stored honey along the top of the comb and biscuit-brown cappings seal worker brood below it — the arrangement a beekeeper reads at a glance when inspecting a colony." width="96"
crop 0.00 0.28 0.93 1.00
mark 0.161 0.660 "1"
mark 0.667 0.285 "2"
mark 0.473 0.438 "3"
mark 0.323 0.826 "4"
key 1 Capped honey — pale, almost white wax cappings, stored above the brood
key 2 Capped worker brood — biscuit-brown cappings over pupating larvae, with cells from which young bees have already emerged
key 3 Adult workers covering the comb; this is the caste that does all of this work
key 4 A wooden top bar, with the top bars of the other frames behind it; every frame is surrounded by the bee space, which is why it lifts out clean
```

**Products and services.** Honey is an invert-sugar syrup of nectar ripened by
the bees to below about 20 % water; **beeswax** is secreted from abdominal wax
glands of young workers; **propolis** is plant resin used as a sealant; **royal
jelly** and **bee venom** have small specialist markets. But the largest value
by far is **pollination**: of the leading crops grown for human food worldwide,
**87 depend to some degree on animal pollination**, and those crops make up
about 35 % of global production volume. In Jumla, *A. cerana* supplies more than
half of all flower visits to apple, cucumber and pumpkin.

::: example Honey yield per hive in Nepal
Nepal produced 4,278 MT of honey from 276,000 hives in 2081/82. What is the
average yield per hive, and how does it compare with the national average of
16.45 kg per hive reported in 2019?

$$ \text{yield} = \frac{4\,278\,000\ \text{kg}}{276\,000\ \text{hives}}
= 15.5\ \text{kg per hive} $$

So the average hive now gives about **15.5 kg**, slightly below the 16.45 kg of
2019. The decline is real: a 2024 study across Nepali beekeeping districts found
yield per hive down by about half and the number of occupied hives down by about
44 % over 2012–22, blamed on forage loss, pesticide use and brood disease.
:::

**Enemies of the hive.** The mite ***Varroa destructor*** — recognised as a
species separate from *V. jacobsoni* only in **2000** — is the great pest of
*A. mellifera*; it feeds on developing brood and spreads viruses. *A. cerana* in
western Nepal has suffered **Thai sacbrood virus** and **European foulbrood**
since the 1990s. *Tropilaelaps* mites, wax moths and hornets complete the list;
*A. cerana* famously smears animal faeces round its nest entrance to deter the
giant hornet *Vespa soror*.

::: note Mad honey — *bishe mahi*
Where *A. laboriosa* forages on ***Rhododendron arboreum*** — **laliguras**,
Nepal's national flower — the honey carries **grayanotoxins**, which lock open
voltage-gated Na⁺ channels and over-stimulate the vagus nerve. Nearly every
patient shows **bradycardia and hypotension**, with dizziness, nausea and
sweating. About 68 Nepali cases are on record over five decades, clustered in
**Gandaki Province** in spring, mostly middle-aged men self-medicating — and no
deaths have been recorded. The honey is harvested by Gurung honey hunters on
cliff ladders and sells for around five times the price of ordinary honey.
(Turkish "mad honey" comes from different species, *R. ponticum* and *R. luteum*
— do not transplant those names to Nepal.)
:::

### Sericulture — silk production

**Sericulture** is the rearing of silkworms for raw silk. The mulberry silkworm
is ***Bombyx mori*** (order Lepidoptera, family Bombycidae), domesticated from
the wild *Bombyx mandarina* about 4,600 years ago and now so thoroughly
domesticated that it is **flightless and unknown in the wild**. It is
**monophagous**: it eats the leaves of mulberry, *Morus alba*, and nothing else.
Growing the mulberry is therefore half of sericulture — the branch of the subject
called **moriculture**.

```photo id="bio12/silkworm-cycle" caption="Life cycle of the silkworm *Bombyx mori*, from an old plate, with its printed legend. The commercially important fact is where the cycle is interrupted: the cocoon is harvested and the pupa killed by stifling, because a moth that emerges bites its way out and cuts the single filament into short lengths." width="92"
```

**The rearing cycle.** Eggs are incubated and hatch in about 10–14 days into
tiny larvae called *chawki* worms. The larva passes through **five instars
separated by four moults**, eating chopped mulberry leaf continuously for about
**29–30 days**. After the fourth moult the fifth-instar larva stops feeding,
becomes translucent, climbs into a mountage and spins for **2–3 days**, moving
its head in a figure-of-eight and paying out silk from a pair of modified
salivary glands through a single spinneret. Inside the finished cocoon it moults
once more into a pupa. If left alone, the moth would emerge, mate, lay 300–500
eggs and die without ever feeding — the adult has vestigial mouthparts and
cannot fly.

::: caution Five instars, four moults
Textbooks routinely print "four instars" or "five moults". The larva has
**five instars and four larval moults**; the fifth moult, larva to pupa, happens
*inside* the cocoon. Also: the larva is monophagous on mulberry, so a
sericulture failure is almost always a mulberry failure.
:::

```photo id="bio12/silkworm-cocoon" caption="An adult *Bombyx mori* moth on a cocoon. This is the stage sericulture prevents from ever happening: a moth that completes its development bites its way out, and the single filament of that cocoon is left in short, unreelable pieces." width="90"
crop 0.03 0.13 0.90 0.95
mark 0.236 0.421 "1"
mark 0.466 0.754 "2"
mark 0.506 0.305 "3"
mark 0.730 0.390 "4"
key 1 Creamy wings — present, but the domesticated moth cannot fly
key 2 Head, with a bipectinate (feathery) antenna on each side; the antennae are much larger in the male and detect the female's pheromone
key 3 Stout hairy body; the adult has vestigial mouthparts and never feeds
key 4 The cocoon, spun from one continuous filament 600–900 m long
```

**From cocoon to cloth.** The steps are fixed and are commonly asked in
sequence.

1. **Harvesting** — cocoons are picked from the mountages 5–7 days after spinning.
2. **Stifling** — the pupa is killed by steam, hot air or sun, before it can emerge.
3. **Deflossing** — the loose outer floss is stripped off.
4. **Cooking** — cocoons are soaked in hot water to soften the sericin gum.
5. **Reeling** — filaments from several cocoons are drawn together onto a reel;
   this is done in a factory called a **filature**.
6. **Throwing, degumming, dyeing, weaving.**

A cocoon contains about **1,000–1,600 m** of spun filament, of which
**600–900 m** can be reeled off as one continuous thread. Raw silk is about
**75–80 % fibroin** (the fibre protein, a stack of antiparallel β-sheets with the
repeat Gly-Ser-Gly-Ala-Gly-Ala) and **20–25 % sericin** (the water-soluble gum);
degumming removes up to 30 % of the weight and gives silk its final lustre.
Cocoons too damaged to reel are carded and **spun** like cotton into spun silk.

::: example How many cocoons for a sari?
Between **4,000 and 7,000** cocoons are needed for one kilogram of raw silk. A
Kavre farmer delivers 30,000 cocoons to the reeling centre, which works at 5,000
cocoons per kg. If a silk sari needs about 0.5 kg of raw silk, how many saris is
that?

$$ \text{raw silk} = \frac{30\,000}{5000} = 6.0\ \text{kg}
\qquad
\text{saris} = \frac{6.0}{0.5} = 12 $$

**Twelve saris**, from thirty thousand caterpillars.

Beware the commonest error in this topic: the familiar figure "2,000–3,000
cocoons" is **per pound**, not per kilogram.
:::

**The four silks.** Mulberry silk is only one of four commercial silks. The
other three — tasar, eri and muga — are the **vanya** or wild silks, all from
the family Saturniidae. Oak tasar is a second form of tasar reared on oak.

| Silk | Insect | Host plant | Note |
|---|---|---|---|
| Mulberry | *Bombyx mori* | *Morus alba* | about 90 % of world silk; reeled |
| Tasar | *Antheraea paphia* | *Terminalia*, sal (*Shorea robusta*) | coarse, coppery; "*A. mylitta*" is a junior synonym |
| Oak tasar | *Antheraea* × *proylei* | oak (*Quercus* spp.) | a **man-made hybrid**, not a natural species |
| Eri | *Samia ricini* | castor, *Ricinus communis* | open-mouthed cocoon → **spun**, not reeled; "ahimsa silk" |
| Muga | *Antheraea assamensis* | som (*Persea bombycina*), soalu (*Litsea*) | golden; 99 % from Assam |

::: caution Eri is spun, not reeled
The eri cocoon is **open at one end** — the moth walks out without cutting
anything. That is exactly why eri can be produced without killing the pupa, which
is why it is called *ahimsa* silk, and also why it cannot be reeled as a
continuous filament and must be spun as a staple fibre.
:::

**Sericulture in Nepal.** Nepal is classed by the International Sericultural
Commission among producers of negligible quantities. Silk was first attempted
under Prime Minister Chandra Shamsher in **1911**; a state Silk Farming Centre
followed in **1975**; today the **Sericulture Development Centre at Khopasi,
Kavrepalanchok** is the national hub, with nine government farms. Around
**1,538 ha** of mulberry produce roughly **39 MT** annually, all of it bivoltine
*B. mori* — there is no commercial wild-silk sector. Thirty-eight mid-hill
districts between 750 and 1,500 m have been declared climatically suitable, so
the ceiling is far above the present output. China is the world's largest
producer; India is the only country that produces all four silks.

### Pisciculture — fish farming

**Pisciculture** is the controlled rearing of fish in ponds, tanks or cages.
Nepal now takes **84 %** of its fish from aquaculture and only 16 % from capture
fisheries, and 96 % of the pond output comes from the Terai.

**Composite fish culture (polyculture).** The central idea is simple and is the
most examinable point in this section. A pond is not one habitat but several: a
surface layer of phytoplankton and zooplankton, a middle column, a weedy margin
and a muddy bottom. Stock one species and most of that food is wasted. Stock six
species with **different feeding niches** and the same pond feeds them all, with
no competition, so the yield per hectare rises sharply.

| Species | Scientific name | Zone | Natural food |
|---|---|---|---|
| Silver carp | *Hypophthalmichthys molitrix* | surface | **phytoplankton** |
| Catla | *Labeo catla* | surface and mid-water | **zooplankton** |
| Rohu | *Labeo rohita* | column | omnivore — plankton, detritus |
| Grass carp | *Ctenopharyngodon idella* | weedy margins | **macrophytes**, aquatic weeds |
| Mrigal | *Cirrhinus mrigala* | bottom | detritus and decaying vegetation |
| Common carp | *Cyprinus carpio* | bottom | omnivore — benthic animals, detritus |

All six belong to the family **Cyprinidae**. Rohu, catla and mrigal are the
three **Indian major carps**; silver, grass and common carp are exotic. The
bighead carp *Hypophthalmichthys nobilis* — a zooplankton feeder — sometimes
substitutes for a species in Nepal's six-species system.

::: caution Silver carp and bighead carp are not interchangeable
**Silver carp eats phytoplankton; bighead carp eats zooplankton.** This pair is
swapped in a large fraction of South Asian textbooks and is a favourite MCQ.
Two more from the same family of errors: rohu is a **column** feeder, not a
bottom feeder, and catla feeds on **zooplankton**, not phytoplankton.
:::

```photo id="bio12/fish-catla" caption="Catla (*Labeo catla*) — a surface feeder on zooplankton; the deep, broad head carries an upturned mouth." width="54"
```

```photo id="bio12/fish-silver-carp" caption="Silver carp (*Hypophthalmichthys molitrix*) — a surface feeder on phytoplankton." width="54"
```

```photo id="bio12/fish-rohu" caption="Rohu (*Labeo rohita*) — a column feeder, shown here as market fish." width="54"
```

```photo id="bio12/fish-grass-carp" caption="Grass carp (*Ctenopharyngodon idella*) — a herbivore that eats aquatic weeds and cut grass." width="54"
```

```photo id="bio12/fish-mrigal" caption="Mrigal (*Cirrhinus mrigala*) — a bottom feeder on detritus and decaying matter (engraving)." width="54"
```

```figure caption="Composite fish culture. Six species are stocked together because each feeds in a different part of the pond, so the whole standing crop of food is harvested instead of one layer of it."
fig, ax = plt.subplots(figsize=(5.1, 3.2))
ax.set_xlim(0, 10.6); ax.set_ylim(0, 6.6); ax.axis("off")
P = matplotlib.patches.Polygon
# pond basin
ax.add_patch(P([[0.4, 5.55], [10.2, 5.55], [9.3, 0.75], [1.3, 0.75]],
               closed=True, fc="#eaf1f8", ec=ACCENT, lw=1.4, zorder=1))
# zone bands
for y0, y1, fc in [(4.30, 5.55, "#dbeaf6"), (2.85, 4.30, "#eaf1f8"),
                   (1.55, 2.85, "#f2f5f9")]:
    ax.add_patch(P([[0.4 + (5.55 - y1) * 0.187, y1],
                    [10.2 - (5.55 - y1) * 0.187, y1],
                    [10.2 - (5.55 - y0) * 0.187, y0],
                    [0.4 + (5.55 - y0) * 0.187, y0]],
                   closed=True, fc=fc, ec="none", zorder=1))
ax.plot([0.4, 10.2], [5.55, 5.55], color=ACCENT, lw=1.8, zorder=4)
ax.text(0.45, 5.78, "water surface", fontsize=6.0, color=ACCENT, va="bottom")
# mud
ax.add_patch(P([[1.3, 0.75], [9.3, 0.75], [9.52, 1.55], [1.08, 1.55]],
               closed=True, fc="#e6dccb", ec="#8F5507", lw=1.0, zorder=2))
ax.text(5.3, 1.12, "mud and detritus", ha="center", va="center",
        fontsize=6.0, color="#8F5507", zorder=5)

def fish(x, y, c, name, food, flip=False):
    d = -1 if flip else 1
    ax.add_patch(matplotlib.patches.Ellipse((x, y), 1.15, 0.44, fc=c,
                 ec="none", alpha=0.92, zorder=6))
    ax.add_patch(P([[x - d * 0.58, y], [x - d * 0.92, y + 0.26],
                    [x - d * 0.92, y - 0.26]], closed=True, fc=c,
                   ec="none", alpha=0.92, zorder=6))
    ax.text(x, y + 0.42, name, ha="center", va="bottom", fontsize=6.3,
            color=INK, zorder=7)
    ax.text(x, y - 0.42, food, ha="center", va="top", fontsize=5.7,
            color=MUTED, style="italic", zorder=7)

fish(2.55, 4.90, SERIES[0], "silver carp", "phytoplankton")
fish(7.55, 4.90, SERIES[2], "catla", "zooplankton", flip=True)
fish(5.05, 3.55, SERIES[4], "rohu", "column omnivore")
fish(8.20, 3.30, SERIES[3], "grass carp", "water weeds")
fish(3.05, 2.15, SERIES[1], "mrigal", "bottom detritus")
fish(6.60, 2.15, SERIES[5], "common carp", "bottom omnivore")
# weeds at margin
for wx in [9.00, 9.18, 9.36]:
    ax.plot([wx, wx - 0.06], [1.55, 3.10], color="#2e8b57", lw=1.1, zorder=3)
fig.tight_layout()
```

**Induced breeding.** Carps kept in ponds **mature perfectly well but fail to
spawn**, because they need the riverine cues — rising water, a current, monsoon
turbidity — that a still pond never supplies. The problem was solved by
**Hiralal Chaudhuri at Cuttack on 10 July 1956**, by injecting pituitary
extract (hypophysation) into ripe brooders; India keeps that date as National
Fish Farmers' Day. Today a synthetic analogue is normally used — **Ovaprim**,
which combines a salmon GnRH analogue with **domperidone**, a dopamine blocker
that removes the brain's inhibition of the gonadotrophin surge. The injected
pair is kept in a breeding hapa or circular hatchery, spawns within hours, and
the eggs are moved to hatching jars.

::: caution "Carps cannot mature in ponds"
They mature. What they cannot do in a pond is **spawn**. Say it precisely: pond
conditions lack the environmental stimuli for the final maturation and release of
gametes, so the hormone is supplied artificially.
:::

**Nepal's cold-water and indigenous fishes.** **Rainbow trout**, *Oncorhynchus
mykiss*, was introduced from India in 1969 and again from England and Japan in
1988; government farms began production in 1995 and private farms in 1998, with
Rasuwa and Nuwakot the commercial centres. It needs water below about 21 °C, and
now yields 1,332 MT a year. Among native fishes the **sahar** or golden mahseer
*Tor putitora* is prized but is assessed **Endangered** by IUCN; the snow trout
or **asala** *Schizothorax richardsonii* is **Vulnerable**; **katle**
*Neolissochilus hexagonolepis* is Near Threatened. Conservation of these three,
and hatchery ranching of sahar, is an active field in Nepal.

::: caution *Tor putitora* is not Nepal's national fish
Nepal's gazetted national symbols are the cow, the Himalayan monal (*danphe*)
and *Rhododendron arboreum*. No fish has been gazetted. *Tor putitora* is also
**Endangered**, not Critically Endangered.
:::

::: example Stocking a composite carp pond
A farmer in Bara has a **0.6 ha** pond and stocks at 5,000 fingerlings per
hectare in the ratio surface 30 % : column 30 % : bottom 40 %. How many
fingerlings of each group, and what harvest can be expected at the national
average yield of 5.62 t ha⁻¹?

Total fingerlings $= 5000 \times 0.6 = 3000$.

$$ \text{surface} = 0.30\times 3000 = 900 \qquad
\text{column} = 0.30\times 3000 = 900 $$

$$ \text{bottom} = 0.40\times 3000 = 1200 $$

So about 900 silver carp and catla together, 900 rohu, and 1200 mrigal and
common carp together.

$$ \text{harvest} = 5.62\ \text{t ha}^{-1}\times 0.6\ \text{ha}
= 3.37\ \text{t} \approx 3370\ \text{kg} $$
:::

### Poultry farming

**Poultry farming** is the rearing of domestic birds for meat and eggs. The
domestic fowl is ***Gallus gallus domesticus*** (order Galliformes, family
Phasianidae), descended principally from the **red junglefowl** *Gallus gallus*
about 8,000 years ago, with some genes from three other junglefowl species.
Nepal's own junglefowl subspecies is *G. g. murghi*.

Commercial stock is divided into two lines that have been bred to do quite
different things.

| | Broiler | Layer |
|---|---|---|
| Purpose | meat | eggs |
| Typical strains | Cobb, Ross, Hubbard | Hy-Line Brown, Lohmann, White Leghorn |
| Growth | reaches slaughter weight in **4–6 weeks** | grows slowly, matures for laying |
| Housing | deep litter, high density | cages or deep litter with nest boxes |
| Feed | high-energy broiler starter, grower, finisher | layer mash high in calcium for shell |

A modern brown layer strain approaches **500 eggs by 100 weeks** of age. Nepal's
own recognised indigenous breeds number exactly **three**: **Sakini**, **Ghanti
Khuile** (the naked-neck bird, carrying the *Na* gene) and **Pwankh Ulte** (the
frizzle, whose feathers curl outwards). All three are dual-purpose, hardy and
slow — valuable for scavenging village systems and for the genes they carry, not
for output. NARC has run several generations of selection on Sakini.

::: caution Nepal has three indigenous chicken breeds
Kadaknath, Aseel and Kuroiler are Indian breeds or commercial crosses. They are
not Nepali indigenous breeds. The three are **Sakini, Ghanti Khuile, Pwankh
Ulte**.
:::

**Poultry diseases** are the standard short-answer topic.

| Disease | Causative agent | Type | Key features | Control |
|---|---|---|---|---|
| Newcastle (**Ranikhet**) | avian paramyxovirus type 1 | **virus** | respiratory and nervous signs, twisted neck; mortality up to 100 % | live and killed vaccines; strict biosecurity |
| Marek's disease | *Gallid alphaherpesvirus 2* | **virus** | tumours, enlarged peripheral nerves, leg paralysis | HVT or CVI988-Rispens vaccine at hatch or *in ovo* on day 18 |
| Fowl pox | *Avipoxvirus* | virus | wart-like nodules on comb and wattles; diphtheritic form in mouth | wing-web vaccination |
| Coccidiosis | *Eimeria* spp. (**protozoa**, Apicomplexa) | protozoan | bloody droppings; *E. tenella* damages the **caeca** | coccidiostats in feed, dry litter |
| Avian influenza | influenza A H5N1, H9 | virus | sudden death, cyanotic comb | culling, movement control, biosecurity |

Newcastle disease and Ranikhet disease are **the same disease under two names**.
Nepal's first H5N1 outbreaks were in **Jhapa in 2009**, followed by Pokhara in
2010 where over 11,000 birds were culled; H5 and H9 viruses have recurred
periodically since, the first human case was reported in April 2019, and 2023
brought outbreaks in Bagmati caused by clade 2.3.4.4b.

### Animal husbandry — dairy and livestock

**Animal husbandry** is the science of breeding, feeding, housing and managing
domestic animals. In Nepal it is dominated by the buffalo.

**Buffalo.** *Bubalus bubalis* supplies **52.1 %** of Nepal's milk, more than
all cattle put together, and Nepal holds one of the largest buffalo populations
in the world. Almost every buffalo in the country is of the **riverine** type
(the swamp type survives only as the wild population at Koshi Tappu). About
65 % are indigenous — **Lime**, **Parkote** and **Gaddi**, with the **Terai
buffalo** recently recognised as a fourth — and the remaining 35 % are **Murrah**
and Murrah crosses. Buffalo milk is richer in fat than cow milk, which is why
Nepali *ghiu* and *khuwa* are traditionally made from it.

::: caution Riverine, not swamp
Nepali hill buffaloes (Lime, Parkote) are **riverine** type. Calling them swamp
buffalo is a standard textbook error, as is writing "*Bubalus bubalus*" for
*Bubalus bubalis*.
:::

**Cattle.** Two indigenous breeds are worth knowing for their extremes.
**Lulu** cattle of Manang and Mustang live between 2,500 and 4,500 m and are
**humpless and predominantly taurine**, with some zebu and even yak ancestry;
cows stand 74–90 cm and give 1–2 kg of milk a day. **Achhami** cattle of Achham,
Bajhang, Bajura and Doti are zebu, and stand **less than a metre at the
withers** — the local name *Naumuthe*, "nine fists", describes the height. The
**Siri** is a draught breed from the eastern hills and Sikkim.

**Yak and chauri.** The yak is kept above about 3,000 m. Crossing a yak with
hill cattle produces the hybrid called **chauri** in Nepal (*dzo* in Tibetan
areas), which yields more milk than a pure yak and tolerates lower altitudes.
The genetics is an exam favourite: **female hybrids are fully fertile, but
F₁ males are sterile** — their semen contains no sperm, so they are used only as
teaser bulls. Fertility returns to males only after several generations of
backcrossing. Hybrid milk yield exceeds the yak's, but its **fat percentage is
usually lower**. Yak milk in Nepal runs about 17.4 % total solids and 6.5 % fat,
and the butter and the rock-hard cheese **chhurpi** are made from it.

::: caution Chauri is the hybrid, and the males are sterile
Do not write "chauri = male yak" or "the hybrids are fertile". Correct: chauri is
the yak–cattle hybrid; **females fertile, F₁ males sterile**; and hybrid milk fat
is **lower** than pure yak milk, not higher.
:::

**Goats and sheep.** Goats are Nepal's largest livestock population by head —
nearly 16 million — with four indigenous breeds arranged by altitude:
**Chyangra** (high Himalaya), **Sinhal** (high hills), **Khari** (mid-hills) and
**Terai**. Sheep have four major breeds — **Bhyanglung**, **Baruwal**, **Kage**
and **Lampuchhre** — which together make up over 90 % of the national flock.

```figure caption="Two Nepali livestock statistics an examiner may ask you to interpret (MoALD 2081/82). Left: buffalo supply more milk than all cattle. Right: farmed fish now outweigh wild-caught fish by more than five to one."
fig, axes = plt.subplots(1, 2, figsize=(5.1, 2.6))
a1, a2 = axes
lab1 = ["buffalo", "cow"]
val1 = [1416083 / 1000, 1302094 / 1000]
b1 = a1.bar(lab1, val1, color=[SERIES[0], SERIES[3]], width=0.58)
a1.set_ylabel("milk (thousand MT)", fontsize=7)
a1.set_title("Milk, 2,718 thousand MT total", fontsize=7.4, color=INK, pad=7)
for r, v, p in zip(b1, val1, ["52.1 %", "47.9 %"]):
    a1.text(r.get_x() + r.get_width() / 2, v + 40, f"{v:,.0f}\n{p}",
            ha="center", va="bottom", fontsize=6.2, color=INK,
            linespacing=1.2)
a1.set_ylim(0, 1900)

lab2 = ["aquaculture", "capture"]
val2 = [110.112, 21.000]
b2 = a2.bar(lab2, val2, color=[SERIES[2], SERIES[1]], width=0.58)
a2.set_ylabel("fish (thousand MT)", fontsize=7)
a2.set_title("Fish, 131 thousand MT total", fontsize=7.4, color=INK, pad=7)
for r, v, p in zip(b2, val2, ["84 %", "16 %"]):
    a2.text(r.get_x() + r.get_width() / 2, v + 3, f"{v:,.0f}\n{p}",
            ha="center", va="bottom", fontsize=6.2, color=INK,
            linespacing=1.2)
a2.set_ylim(0, 150)

for a in axes:
    a.tick_params(labelsize=6.6)
    a.spines["top"].set_visible(False)
    a.spines["right"].set_visible(False)
    a.grid(axis="y", color=GRID, lw=0.7)
    a.set_axisbelow(True)
fig.tight_layout()
```

### Vermicomposting

**Vermicomposting** is the conversion of organic waste into a fine, nutrient-rich
manure by earthworms working together with microorganisms. The product is
**vermicompost** (worm castings); the liquid that drains or is percolated
through the bed is **vermiwash**.

Not every earthworm will do the job. Earthworms fall into three ecological
groups, and only the first is useful.

| Group | Where it lives | Suitable for a worm bin? |
|---|---|---|
| **Epigeic** | in the surface litter layer; no permanent burrow; eats fast, breeds fast | **yes — these are the vermicomposting worms** |
| **Anecic** | deep permanent vertical burrows, pulls litter down (*Lumbricus terrestris*) | **no** — adapts badly to a shallow bed |
| **Endogeic** | horizontal burrows in mineral soil; eats soil (geophagous) | no |

```figure caption="The three ecological groups of earthworms. Vermicomposting uses epigeic species only: they live in the litter layer itself, which is exactly what a worm bed is."
fig, ax = plt.subplots(figsize=(5.0, 2.8))
ax.set_xlim(0, 10.8); ax.set_ylim(0, 6.2); ax.axis("off")
R = matplotlib.patches.Rectangle
for i, (t, sub) in enumerate([
        ("EPIGEIC", "litter dweller\nno burrow"),
        ("ANECIC", "deep vertical\nburrow"),
        ("ENDOGEIC", "horizontal burrows\nin mineral soil")]):
    x0 = 0.35 + i * 3.55
    ax.add_patch(R((x0, 0.65), 3.10, 3.55, fc="#f0e6d6", ec=MUTED, lw=0.9))
    ax.add_patch(R((x0, 3.55), 3.10, 0.65, fc="#d9c7a7", ec=MUTED, lw=0.9))
    ax.text(x0 + 1.55, 5.42, t, ha="center", fontsize=7.4,
            color=[SERIES[2], SERIES[1], SERIES[3]][i])
    ax.text(x0 + 1.55, 4.55, sub, ha="center", va="center", fontsize=6.0,
            color=MUTED, linespacing=1.3)
    ax.text(x0 + 0.10, 3.88, "litter", fontsize=5.6, color="#8F5507",
            va="center")

def worm(pts, c):
    p = np.array(pts)
    ax.plot(p[:, 0], p[:, 1], color=c, lw=2.6, solid_capstyle="round",
            zorder=5)

worm([[1.15, 3.86], [1.60, 4.04], [2.05, 3.72], [2.55, 3.96],
      [3.10, 3.76]], SERIES[2])
worm([[5.45, 3.95], [5.45, 3.30], [5.30, 2.70], [5.48, 2.10],
      [5.35, 1.60]], SERIES[1])
worm([[7.70, 2.55], [8.30, 2.32], [8.95, 2.62], [9.60, 2.34],
      [10.25, 2.58]], SERIES[3])
ax.text(1.90, 1.95, "the only group\nused in a worm bed", ha="center",
        va="center", fontsize=6.0, color=SERIES[2], linespacing=1.3)
for cx in (5.45, 9.00):
    ax.text(cx, 1.20, "not used in\na worm bed", ha="center", va="center",
            fontsize=6.0, color="#d9534f", linespacing=1.3, zorder=6)
fig.tight_layout()
```

The standard species is ***Eisenia fetida***, the tiger worm or red wiggler
(family Lumbricidae). *Eudrilus eugeniae* (the African night crawler),
*Perionyx excavatus* and the South Asian *Lampito mauritii* are also used.

::: caution *Eisenia fetida*, not *foetida*
*Eisenia fetida* is the accepted spelling; *E. foetida* is a synonym. And
*Lumbricus terrestris*, which appears in many textbook lists, is an **anecic**
species and is unsuitable for vermicomposting.
:::

**Running a bed.** A shallow bed 1 m × 1 m × 0.5 m is stocked with about
**1 kg of worms — roughly 1,000 individuals**. The waste is first pre-digested
for about 20 days with dung slurry (fresh manure overheats and releases ammonia),
then mixed with about **30 % cattle dung**. Moisture is held near **60 %** and
the bed is shaded; *E. fetida* works between about 4.5 °C and 32 °C. The worms
are fed roughly half their body weight of waste per day. Harvest takes
**about 60–140 days** — two to four months, not the "30 days" often claimed. The
finished compost is dark, odourless, nearly neutral in pH and crumbly, with a
C : N ratio around 21.

```photo id="bio12/vermicompost" caption="*Eisenia fetida* massed on the rim and walls of a compost bin. Epigeic worms live in the surface litter and not in deep burrows, so when the bed turns against them — waterlogged, too acid, too hot — they climb out of it. Reading a mass escape like this is one of the first skills a vermicompost operator learns." width="94"
crop 0.05 0.10 0.98 0.88
mark 0.624 0.814 "1"
mark 0.242 0.359 "2"
mark 0.522 0.256 "3"
key 1 Worms crowded at the rim; an epigeic species lives at the surface, never in deep burrows
key 2 A single worm; the body is a chain of ring-like segments, kept moist by mucus because the worm breathes through its skin
key 3 Worms out on the vertical wall — an escape on this scale means conditions in the bed are wrong, most often that it has been over-watered
```

**Why it is worth doing.** Vermicompost analyses at **0.5–1.5 % N,
0.1–0.3 % P and 0.15–0.56 % K** with 9.5–18 % organic carbon, against about
0.5 % N in well-rotted farmyard manure. Castings contain roughly five times the
available nitrogen and seven times the available potash of the surrounding
topsoil, plus plant hormones (auxins and cytokinins), enzymes, and nitrogen-fixing
and phosphate-solubilising bacteria. Vermiwash diluted to 5–10 % inhibits the
mycelium of pathogenic fungi and is used as a foliar spray. A Nepali trial
recorded an okra yield increase of about 126 %, with benefit : cost ratios of
1.0–1.6; four commercial brands are now on sale in Nepal, though published work
in the country remains thin.

::: caution Vermicompost is not "2–3 % nitrogen"
Measured values are **0.5–1.5 % N**. Over-quoting the nutrient content and
under-quoting the time (it takes **60–140 days**, not 30–45) are the two
standard errors in this topic.
:::

::: example Vermicompost against farmyard manure
A farmer can apply either 5 t ha⁻¹ of vermicompost at 1.0 % N or 5 t ha⁻¹ of
well-rotted FYM at 0.5 % N. How much nitrogen does each supply, and how much
urea (46 % N) would make up the difference?

$$ N_{\text{vermi}} = 5000\ \text{kg}\times 0.010 = 50\ \text{kg N ha}^{-1} $$
$$ N_{\text{FYM}} = 5000\ \text{kg}\times 0.005 = 25\ \text{kg N ha}^{-1} $$

The difference is 25 kg N ha⁻¹, which as urea is

$$ \frac{25}{0.46} = 54.3\ \text{kg of urea per hectare.} $$

Note what the arithmetic does **not** capture: the vermicompost also supplies
P, K, micronutrients, organic carbon and microorganisms, none of which urea does.
:::

### Pearl culture and lac culture

Both of these appear in the syllabus's general heading, and both need an honest
Nepali footnote: **neither is practised in Nepal.**

**Pearl culture.** A pearl is formed when the **mantle** of a bivalve is
displaced or irritated, forms a closed **pearl sac**, and that sac secretes
**nacre** — aragonite tablets about 10–20 µm across and 0.5 µm thick, laid in
sheets separated by the protein **conchiolin**. Because each tablet is about as
thick as a wavelength of visible light, the stack produces iridescence. Marine
pearls come from *Pinctada* species (family Margaritidae) — *P. fucata*,
*P. margaritifera*, *P. maxima*; freshwater pearls from mussels such as
*Lamellidens marginalis* and *Sinohyriopsis cumingii*.

In **culture**, a technician inserts a round bead nucleus cut from mussel shell
**together with a small graft of mantle tissue, the *saibo***; it is the graft,
not the bead, that grows into the pearl sac. Marine culture places one bead in
the gonad; freshwater culture inserts tissue alone, without a bead, and up to 25
grafts per valve. The sac is complete in about five days and regular nacre
begins around day 25–30. **Kōkichi Mikimoto** produced the first semi-spherical
cultured pearls in the 1890s and patented the method in 1896; the technique for
whole spherical pearls was devised independently by **Tatsuhei Mise** and
**Tokichi Nishikawa**. More than 95 % of pearls sold today are cultured, and
China produces over 95 % of the world's freshwater pearls.

::: caution The grain of sand is a myth
A grain of sand is **rarely** the cause. Typical natural stimuli are organic
material, a **parasite**, or damage that displaces mantle tissue. And a cultured
pearl is not "just a bead" — without the mantle graft there is no pearl sac and
no nacre. Pearl oysters are not true oysters (Ostreidae); *Pinctada* is placed in
**Margaritidae**.
:::

**Lac culture.** Lac is a resin secreted by the **female** scale insect
***Kerria lacca*** (Hemiptera, family Kerriidae) as it feeds on the twigs of
host trees. It is the **only commercial resin of animal origin**. The main hosts
are **kusum** *Schleichera oleosa* (best yield and palest lac, 6–10 kg a tree),
**ber** *Ziziphus mauritiana* (1.5–6 kg) and **palas** *Butea monosperma*
(1–4 kg). Encrusted twigs are cut as **sticklac**, washed and sieved to
**seedlac**, then melted and stretched into **shellac** flakes. The red **lac
dye** consists of laccaic acids extracted from the insect's haemolymph. Shellac
goes into varnish, sealing wax, confectioner's glaze and citrus coatings, and
once went into gramophone records. India produces at least half the world total,
around 20,000 tonnes of raw lac a year, led by Jharkhand.

::: caution Names and geography
The insect is ***Kerria lacca***, family **Kerriidae** — not "*Laccifer lacca*,
Tachardiidae". The resin comes from the **female**, and the encrustation is not a
cocoon. Host is *Butea monosperma*, not "*B. frondosa*". And **do not write that
lac or pearl culture is practised in Nepal** — Nepal is landlocked, and appears
on no list of lac-producing countries.
:::

## 10.2 Microbial diseases and application of microbiology

**Microbiology** is the study of organisms too small to see unaided —
bacteria, archaea, viruses, protozoa, microscopic fungi and algae. It has two
faces, and the syllabus asks for both. Microorganisms cause most of the
infectious disease in Nepal; they also make our curd, fix our nitrogen, digest
our sewage, brew our biogas and supply every antibiotic we have.

::: note This section builds on Unit 9
Unit 9 (§9.2) already gave you the general table of communicable diseases, the
life cycle of *Plasmodium*, HIV/AIDS and the outline of immunity. This section
takes the **microbiologist's** view of the same ground: what kind of organism
each agent is, how it is identified in a laboratory, and how it is attacked. Read
§9.2 first; do not learn the two sections as if they were unrelated.
:::

### The four groups of agents

| Group | What it is | Size | Sensitive to antibiotics? | Examples |
|---|---|---|---|---|
| **Bacteria** | prokaryotes — no nucleus, 70S ribosomes, peptidoglycan wall | 0.5–5 µm | **yes** | *Mycobacterium tuberculosis*, *Vibrio cholerae*, *Salmonella* Typhi |
| **Viruses** | acellular; nucleic acid in a protein coat; obligate intracellular parasites | 20–300 nm | **no** — antivirals only | SARS-CoV-2, HBV, dengue virus, HIV |
| **Protozoa** | unicellular eukaryotes | 5–100 µm | no — antiprotozoals | *Plasmodium*, *Leishmania donovani*, *Entamoeba histolytica* |
| **Fungi** | eukaryotes with chitinous walls; yeasts and moulds | variable | no — antifungals | *Trichophyton*, *Candida albicans* |

Bacteria are classified by shape (**coccus**, **bacillus**, **spirillum**,
**vibrio**), by their reaction to the **Gram stain** (Gram-positive cells retain
crystal violet because of a thick peptidoglycan layer; Gram-negative cells do
not and take the safranin counterstain), and by their oxygen requirement. A few
genera — *Mycobacterium*, *Nocardia* — have a waxy **mycolic acid** wall that
resists the Gram stain altogether and must be stained by the acid-fast method.

::: definition Pathogen, infection, disease
A **pathogen** is an organism capable of causing disease. **Infection** is the
entry and multiplication of that organism in a host. **Disease** appears only
when the infection damages the host enough to produce signs and symptoms — which
is why a person can be **infected but healthy**, and in the case of *Salmonella*
Typhi can remain a lifelong **carrier** who infects others.
:::

::: key Koch's postulates
Robert Koch's rules for proving that a particular microbe causes a particular
disease, used for anthrax (1876) and tuberculosis (1882):

1. The organism must be found in **every** case of the disease and absent from
   healthy individuals.
2. It must be **isolated** from the host and grown in **pure culture**.
3. The pure culture, inoculated into a healthy susceptible host, must
   **reproduce the disease**.
4. The organism must be **re-isolated** from that experimental host and shown to
   be the same.

Know the limitation too: some pathogens cannot be grown in pure culture
(*Mycobacterium leprae*, most viruses), some infections are symptomless carriers,
and some diseases need more than one agent. Modern practice supplements the
postulates with molecular evidence.
:::

### Modes of transmission

Learn the categories, because a disease question usually wants transmission
named precisely.

- **Airborne / droplet** — tuberculosis, influenza, COVID-19, measles.
- **Faecal–oral (water and food)** — typhoid, cholera, hepatitis A and E,
  amoebic dysentery, giardiasis.
- **Vector-borne** — malaria (*Anopheles*), dengue (*Aedes*), kala-azar
  (*Phlebotomus*), Japanese encephalitis (*Culex*), scrub typhus (chigger mite).
- **Blood and body fluids** — hepatitis B and C, HIV.
- **Direct contact and fomites** — ringworm, scabies, conjunctivitis.
- **From the environment, not person to person** — tetanus (soil spores).

### The diseases the examiner asks for

| Disease | Causative agent | Type | Transmission | Incubation | Cardinal signs | Prevention |
|---|---|---|---|---|---|---|
| Tuberculosis | *Mycobacterium tuberculosis* | acid-fast bacterium | airborne droplet nuclei | 2–12 weeks to infection | cough over 2 weeks, blood in sputum, evening fever, night sweats, weight loss | BCG at birth; DOTS treatment; ventilation |
| Typhoid | *Salmonella* Typhi | Gram-negative bacillus | faecal–oral, water and food, carriers | 7–14 days | step-ladder fever, rose spots, abdominal pain, enlarged liver and spleen | safe water, TCV vaccine, sanitation |
| Cholera | *Vibrio cholerae* O1 / O139 | comma-shaped Gram-negative | faecal–oral, contaminated water | 12 hours – 5 days | painless rice-water stools, vomiting, rapid dehydration | chlorination, ORS, oral cholera vaccine |
| Hepatitis A | hepatitis A virus | RNA virus | **faecal–oral** | 15–50 days | jaundice, dark urine, nausea; never becomes chronic | inactivated vaccine, safe water |
| Hepatitis B | hepatitis B virus | **DNA** virus | blood, sexual contact, mother to child | 30–180 days | jaundice, chronic hepatitis, cirrhosis, liver cancer | recombinant HBsAg vaccine (in Nepal's pentavalent) |
| Hepatitis E | hepatitis E virus | RNA virus | **faecal–oral, waterborne** | 15–60 days | jaundice; case fatality 20–25 % in late pregnancy | safe water; the only vaccine is licensed in China alone |
| Malaria | *Plasmodium vivax*, *P. falciparum* and three others | protozoan | bite of **female *Anopheles*** | 9–17 days | cold–hot–sweating paroxysms, anaemia, enlarged spleen | bed nets, indoor spraying, prompt ACT treatment |
| Kala-azar | *Leishmania donovani* | protozoan | bite of **female *Phlebotomus argentipes*** sandfly | 2–6 months | twice-daily fever spikes, huge spleen, darkened skin, wasting | sandfly control, plastered walls, rK39 testing |
| Dengue | dengue virus, serotypes 1–4 | RNA virus | **day-biting *Aedes aegypti*, *Ae. albopictus*** | 4–10 days | retro-orbital pain, severe body ache, rash, low platelets | destroy clean-water breeding sites, screens |
| COVID-19 | **SARS-CoV-2** | RNA virus | respiratory droplets and aerosols | 2–14 days (median 5) | fever, dry cough, fatigue, loss of smell and taste, breathlessness | vaccination, ventilation, masks |
| AIDS | HIV-1 and HIV-2 | retrovirus | unsafe sex, infected blood and needles, mother to child | AIDS after 8–10 years untreated | falling CD4⁺ count, opportunistic infections, wasting | safe sex, screened blood, ART, PrEP |
| Ringworm | *Trichophyton*, *Microsporum*, *Epidermophyton* | **fungi** | contact, shared towels and combs | 4–14 days | itchy ring-shaped scaly patch with central clearing | keep skin dry, do not share clothing |

::: caution Six names that cost marks every year
1. ***Salmonella* Typhi** — the full name is *Salmonella enterica* subsp.
   *enterica* serovar Typhi. "*Salmonella typhi*" is obsolete. Typhoid is not
   typhus.
2. **El Tor is a biotype**, not a serotype, of *V. cholerae* serogroup **O1**;
   Ogawa and Inaba are the serotypes; O139 is a separate serogroup.
3. **Hepatitis B does not spread through food and water** — A and E do.
4. **Dengue is carried by day-biting *Aedes***, not by night-biting *Culex*.
5. **COVID-19 is the disease; SARS-CoV-2 is the virus.**
6. **Ringworm is a fungus**, not a worm.
:::

### Tuberculosis and the acid-fast smear

Tuberculosis deserves separate treatment because it is Nepal's most important
bacterial disease and because its laboratory diagnosis is examinable.
*Mycobacterium tuberculosis* is a slender rod whose cell wall is loaded with
waxy **mycolic acids**. That wall makes it slow-growing (a generation time of
about 18 hours, against 20 minutes for *E. coli*), resistant to drying, and
impossible to stain by ordinary methods — so the **Ziehl–Neelsen** method is
used instead.

::: key The Ziehl–Neelsen (acid-fast) stain
1. Flood the fixed sputum smear with **carbol fuchsin** and heat until it steams
   — the heat drives the dye through the waxy wall.
2. Decolourise with **acid–alcohol**. Every other cell in the smear loses the
   red dye; mycobacteria hold it, and are therefore called **acid-fast**.
3. Counterstain with **methylene blue**.

Result: **red bacilli against a blue background.** A positive smear means the
patient is infectious.
:::

```photo id="bio12/afb-sputum" caption="Sputum smear stained by the Ziehl–Neelsen method. Every red rod is an acid-fast bacillus; everything that is not a mycobacterium has been decolourised and has taken only the blue counterstain." width="96"
crop 0.05 0.22 0.78 0.98
mark 0.527 0.522 "1"
mark 0.651 0.678 "2"
mark 0.534 0.362 "3"
mark 0.151 0.289 "4"
key 1 A single acid-fast bacillus — a slender, slightly curved red rod a few micrometres long
key 2 A second bacillus well away from the first; the bacilli are scattered right across the field, and the laboratory grades the smear (1+, 2+, 3+) by counting how many appear per field
key 3 A clump of pus cells and mucus, stained blue — these are not acid-fast, so the acid–alcohol washed the carbol fuchsin straight out of them
key 4 A third bacillus, here against the pale background of the rest of the sputum; only the mycobacteria have held the red dye
```

Treatment follows the **DOTS** strategy — *Directly Observed Treatment,
Short-course* — under which a health worker watches each dose swallowed. The
standard regimen is four drugs (isoniazid, rifampicin, pyrazinamide,
ethambutol) for two months, then two drugs (isoniazid, rifampicin) for four.
**MDR-TB** is tuberculosis resistant to **at least isoniazid and rifampicin**
together; Nepal's sixth national drug-resistance survey (2022–24) found
rifampicin resistance in 2.2 % of new patients and 10.1 % of previously treated
patients, and Nepal has entered WHO's regional high-burden list for drug-resistant
TB.

::: caution BCG and DOTS
**BCG** is a live attenuated strain of ***Mycobacterium bovis***, not of
*M. tuberculosis*. It chiefly prevents **miliary TB and TB meningitis in young
children**; its protection against adult pulmonary TB is variable and wanes, so
it is not a guarantee of lifelong immunity. **DOTS is a strategy, not a drug.**
And MDR-TB is not "resistant to all drugs" — that is a different, rarer category.
:::

### Immunity, seen from the microbiology side

The classification of immunity was given in §9.2.4 and is not repeated here.
What matters for this section is the shape of the response, because it is the
whole basis of vaccination.

On **first** contact with an antigen there is a lag of 5–10 days while the few
matching B cells find the antigen, divide and mature; antibody titre then rises
to a modest peak, and the first antibody made is **IgM**. On **second** contact
the memory cells are already present: the lag falls to 1–3 days, the titre rises
a hundred- to a thousand-fold higher, the antibody is mostly **IgG**, and it
binds far more tightly. That difference is why a vaccine works and why booster
doses exist.

```figure caption="Primary and secondary antibody responses to the same antigen. The secondary response is faster, far larger, longer-lasting and dominated by IgG — the reason a vaccine protects and a booster dose is given."
fig, ax = plt.subplots(figsize=(5.0, 3.0))
t = np.linspace(0, 60, 1200)

def pulse(t, t0, amp, rise, fall):
    y = np.zeros_like(t)
    m = t > t0
    y[m] = amp * (1 - np.exp(-(t[m] - t0) / rise)) * np.exp(-(t[m] - t0) / fall)
    return y

igm1 = pulse(t, 5, 1.25, 2.2, 9.0)
igg1 = pulse(t, 8, 1.75, 3.2, 22.0)
igm2 = pulse(t, 31, 1.40, 1.6, 8.0)
igg2 = pulse(t, 32, 62.0, 1.8, 30.0)
ax.semilogy(t, igm1 + igm2 + 0.02, color=SERIES[1], lw=1.7, label="IgM")
ax.semilogy(t, igg1 + igg2 + 0.02, color=ACCENT, lw=2.1, label="IgG")
ax.set_ylim(0.02, 400)
ax.set_xlim(0, 60)
ax.set_xlabel("days after first contact with the antigen", fontsize=7)
ax.set_ylabel("antibody in serum (log scale)", fontsize=7)
ax.tick_params(labelsize=6.6)
ax.set_yticks([0.1, 1, 10, 100])
ax.set_yticklabels(["0.1", "1", "10", "100"])
for x, lab in [(3, "1st dose"), (30, "2nd dose\n(booster)")]:
    ax.axvline(x, color=MUTED, lw=0.9, ls="--")
    ax.text(x + 0.8, 250, lab, fontsize=6.2, color=MUTED, va="top",
            linespacing=1.25)
ax.text(17.0, 30.0, "PRIMARY\nlag 5–10 days\nmostly IgM", ha="center",
        va="center", fontsize=6.3, color=MUTED, linespacing=1.35)
ax.text(46.0, 3.6, "SECONDARY\nlag 1–3 days\n100–1000× the titre\nmostly IgG",
        ha="center", va="center", fontsize=6.3, color=INK, linespacing=1.35)
ax.legend(fontsize=6.6, frameon=False, loc="upper right")
ax.grid(color=GRID, lw=0.7)
ax.set_axisbelow(True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.tight_layout()
```

### Vaccines

A **vaccine** is a preparation of a pathogen, or part of one, given deliberately
to provoke a primary immune response and leave memory cells behind — that is,
to produce **artificial active immunity**.

**Edward Jenner**, in **1796**, inoculated the boy James Phipps with matter from
a **cowpox** sore and showed that it protected him against smallpox. **Louis
Pasteur** generalised the idea to attenuated cultures — fowl cholera in 1879,
anthrax in 1881, rabies in 1885 — and it was Pasteur who coined the word
*vaccine*, in Jenner's honour.

| Type | How it is made | Examples |
|---|---|---|
| **Live attenuated** | the pathogen weakened until it cannot cause disease | BCG, measles–rubella, oral polio, Japanese encephalitis SA 14-14-2 |
| **Killed (inactivated)** | the whole pathogen killed by heat or chemicals | injectable polio (Salk), hepatitis A, cell-culture rabies, Covaxin |
| **Subunit / recombinant / conjugate** | only the protective antigen | hepatitis B (HBsAg), HPV, Hib, pneumococcal, typhoid conjugate |
| **Toxoid** | the toxin, chemically inactivated | tetanus, diphtheria |
| **mRNA** | mRNA for the antigen, delivered in lipid nanoparticles | Comirnaty (BNT162b2) |
| **Viral vector** | a harmless virus carrying the antigen's gene | ChAdOx1 / Covishield |

Nepal's national immunisation programme covers tuberculosis (BCG), polio,
diphtheria, pertussis, tetanus, hepatitis B and *Haemophilus influenzae* type b
(the pentavalent vaccine), pneumococcal disease, rotavirus, measles–rubella,
Japanese encephalitis, and since 2022 **typhoid conjugate vaccine**, plus Td in
pregnancy and HPV vaccine for girls.

Two achievements are worth the dates. **Smallpox**: the last natural case was in
Somalia in October 1977 and the World Health Assembly declared eradication on
**8 May 1980** — the only human disease ever eradicated. **Polio**: Nepal's last
indigenous wild poliovirus case was in **August 2010**, and the WHO South-East
Asia Region was certified polio-free on **27 March 2014**; globally, wild types 2
and 3 are eradicated but type 1 persists in Pakistan and Afghanistan.

::: caution Vaccination is *active* immunity
A vaccine makes **your** immune system do the work, so it is **artificial
active** immunity — slow to appear, long-lasting, with memory. Ready-made
antibodies (anti-tetanus serum, anti-rabies immunoglobulin, antivenom) are
**artificial passive** immunity — immediate, short-lived, no memory. Also: Jenner
used **cowpox**, not smallpox pus, and it was **Pasteur**, not Jenner, who coined
the word *vaccine*.
:::

### Antibiotics

An **antibiotic** is a substance produced by one microorganism that kills or
inhibits another. The word was coined by **Selman Waksman** in the early 1940s.

**Penicillin.** In **1928**, at St Mary's Hospital in London, **Alexander
Fleming** returned to a *Staphylococcus* plate that had been contaminated by a
mould and found the bacterial colonies dissolved around it. He named the mould
*Penicillium notatum*; in **2011** his preserved strain was re-identified as
***Penicillium rubens***. Fleming could not purify the substance. **Howard
Florey**, **Ernst Chain** and Norman Heatley did, at Oxford in 1940–41, and the
**1945 Nobel Prize went to Fleming, Chain and Florey together.**

**Streptomycin**, the first drug effective against tuberculosis, was isolated in
**1943** by **Albert Schatz** in Waksman's laboratory from ***Streptomyces
griseus*** — which is not a fungus but a **filamentous Gram-positive
bacterium**, an actinomycete.

```figure caption="Where antibiotics attack. Every target is a structure or pathway that bacteria have and human cells do not — which is what makes an antibiotic selectively toxic, and why none of these targets exists in a virus."
fig, ax = plt.subplots(figsize=(5.0, 3.5))
ax.set_xlim(0, 12.6); ax.set_ylim(0, 8.4); ax.axis("off")
E = matplotlib.patches.Ellipse
# cell envelope
ax.add_patch(E((4.3, 4.2), 6.6, 5.6, fc="#eaf1f8", ec=ACCENT, lw=2.6, zorder=2))
ax.add_patch(E((4.3, 4.2), 6.0, 4.9, fc="#f7fafd", ec=MUTED, lw=1.1, zorder=3))
ax.text(4.3, 7.45, "bacterial cell", ha="center", fontsize=7.0, color=ACCENT,
        zorder=6)
# nucleoid
th = np.linspace(0, 6.3, 400)
ax.plot(4.3 + 1.5 * np.cos(th) + 0.28 * np.cos(4 * th),
        3.6 + 0.95 * np.sin(th) + 0.22 * np.sin(3 * th),
        color="#6a5acd", lw=1.5, zorder=4)
ax.text(4.3, 3.6, "DNA", ha="center", va="center", fontsize=6.4,
        color="#6a5acd", zorder=5)
# ribosomes
rng = [(2.35, 5.55), (5.95, 5.35), (2.95, 2.20), (5.90, 2.45)]
for rx, ry in rng:
    ax.add_patch(E((rx, ry), 0.62, 0.48, fc="#2e8b57", ec="none", zorder=4))
ax.text(4.32, 2.00, "70S ribosomes", ha="center", fontsize=6.1,
        color="#2e8b57", zorder=5)

def target(y, n, site, drugs):
    ax.plot([8.15, 8.75], [y, y], color=MUTED, lw=0.8, zorder=3)
    ax.add_patch(E((8.05, y), 0.44, 0.40, fc="#d9534f", ec="none", zorder=6))
    ax.text(8.05, y, n, ha="center", va="center", fontsize=6.0,
            color="white", zorder=7)
    ax.text(8.95, y + 0.22, site, ha="left", va="center", fontsize=6.4,
            color=INK, zorder=6)
    ax.text(8.95, y - 0.30, drugs, ha="left", va="center", fontsize=5.8,
            color=MUTED, style="italic", zorder=6)

target(7.55, "1", "cell wall synthesis", "penicillins, cephalosporins")
target(6.05, "2", "protein synthesis, 30S", "streptomycin, tetracyclines")
target(4.55, "3", "protein synthesis, 50S", "erythromycin, chloramphenicol")
target(3.05, "4", "DNA gyrase / RNA polymerase", "ciprofloxacin; rifampicin")
target(1.55, "5", "folate synthesis", "sulfonamides, trimethoprim")
# leaders into the cell
ax.annotate("", xy=(6.40, 6.28), xytext=(7.85, 7.40),
            arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7), zorder=3)
ax.annotate("", xy=(6.22, 5.38), xytext=(7.85, 6.00),
            arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7), zorder=3)
ax.annotate("", xy=(6.23, 2.50), xytext=(7.85, 4.45),
            arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7), zorder=3)
ax.annotate("", xy=(5.85, 3.45), xytext=(7.85, 3.05),
            arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7), zorder=3)
ax.annotate("", xy=(5.40, 1.95), xytext=(7.85, 1.55),
            arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7), zorder=3)
fig.tight_layout()
```

Antibiotics are classified in three ways worth knowing.

- **Spectrum** — **broad-spectrum** (tetracycline, chloramphenicol, ampicillin)
  act on both Gram-positive and Gram-negative bacteria; **narrow-spectrum**
  (penicillin G, vancomycin, isoniazid) act on a limited range.
- **Effect** — **bactericidal** drugs kill (β-lactams, aminoglycosides,
  fluoroquinolones, rifampicin); **bacteriostatic** drugs merely stop growth and
  leave the killing to the immune system (tetracyclines, macrolides,
  sulfonamides, chloramphenicol).
- **Target**, as in the figure above.

::: caution Antibiotics do nothing against a cold or flu
Every antibiotic target — the peptidoglycan wall, the 70S ribosome, DNA gyrase,
the bacterial folate pathway — is a **prokaryotic** structure. A virus has no
wall, no ribosomes and no metabolism of its own; it replicates using the host
cell's machinery. Viral infections need **antivirals** (acyclovir, oseltamivir,
antiretrovirals) or nothing at all.
:::

**Antimicrobial resistance (AMR).** Bacteria resist antibiotics by producing
enzymes that destroy the drug (**β-lactamases**, including ESBL and NDM-1), by
pumping it out (**efflux pumps**), by altering the target (MRSA makes an altered
penicillin-binding protein), and by reducing wall permeability. Resistance
genes travel between bacteria on **plasmids** by conjugation, and on transposons
and integrons — which is why resistance can appear in a species that was never
treated. The drivers are human: antibiotics sold over the counter without
prescription, courses abandoned as soon as the fever drops, and heavy use in
poultry and livestock. A 2024 global analysis attributed about **1.14 million
deaths** directly to resistant bacterial infections in 2021.

::: example How fast does a bacterial population grow?
*Escherichia coli* in good conditions has a generation time of about 20 minutes.
Starting from a single cell, how many cells are there after 6 hours, and how does
that compare with *M. tuberculosis*, whose generation time is about 18 hours?

Number of generations in 6 hours:

$$ n = \frac{6\times 60}{20} = 18 \qquad
N = N_0 \times 2^{n} = 1\times 2^{18} = 262\,144 $$

Over a quarter of a million cells from one, in an afternoon. For
*M. tuberculosis* in the same 6 hours, $n = 6/18 = 0.33$, so the population has
not even doubled once.

This single number explains a great deal of clinical practice: cholera and food
poisoning strike within hours, whereas tuberculosis takes weeks to declare
itself, needs weeks of culture to diagnose by growth, and needs **six months**
of treatment rather than five days.
:::

### Microorganisms at work

The second half of applied microbiology is the useful side. Group the examples
by field; the examiner usually asks for four or five with the organism named.

| Field | Organism | What it does |
|---|---|---|
| Dairy | *Lactobacillus* spp. with *Streptococcus thermophilus* | ferments **lactose to lactic acid**, which coagulates casein: curd (*dahi*), yoghurt |
| Baking and brewing | *Saccharomyces cerevisiae* | ferments sugar to CO₂ (raises dough) and ethanol (beer, wine, *raksi*, bioethanol) |
| Cheese | *Penicillium roqueforti*, *P. camemberti*; *Propionibacterium freudenreichii* | ripening and flavour; the propionibacterium's CO₂ makes the holes in Swiss cheese |
| Industrial chemicals | *Aspergillus niger*; *Clostridium acetobutylicum* | citric acid; acetone–butanol–ethanol fermentation |
| Medicine | *Penicillium rubens*; *Streptomyces griseus*; *Streptococcus equisimilis*; *Monascus purpureus* | penicillin; streptomycin; **streptokinase**, used to dissolve clots after a heart attack; monacolin K, the statin lovastatin |
| Nitrogen fixation | *Rhizobium* (symbiotic, in legume root nodules); *Azotobacter* (free-living, aerobic); *Anabaena azollae* in *Azolla* | convert N₂ to ammonia — the basis of **biofertiliser** |
| Biopesticide | *Bacillus thuringiensis* | crystal **Cry δ-endotoxin**, activated in the alkaline insect midgut; the source of *Bt* genes |
| Biocontrol of fungi | *Trichoderma harzianum*, *T. viride* | suppresses soil-borne fungal pathogens; also a source of cellulase |
| Single-cell protein | *Arthrospira platensis* (spirulina), *Fusarium venenatum* | protein-rich biomass for food and feed |
| Biogas | methanogenic **archaea**, *Methanobacterium*, *Methanobrevibacter* | anaerobic digestion of dung and slurry to a gas of 50–70 % methane |

::: caution Three misfilings
**Spirulina is a cyanobacterium** (*Arthrospira platensis*), not an alga.
**Methanogens are archaea**, not bacteria. ***Anabaena azollae* lives in the
dorsal leaf cavities of *Azolla***, not in its roots. And *Lactobacillus*
ferments **lactose, a sugar** — the milk protein casein is then coagulated by the
acid produced, which is a consequence, not the fermentation itself.
:::

**Biogas** deserves a Nepali note. A domestic plant is fed cattle dung and water
into an airtight digester where three groups of microorganisms work in sequence:
hydrolytic bacteria break polymers into sugars and amino acids, acidogens and
acetogens convert these into organic acids, hydrogen and acetate, and finally
**methanogenic archaea** produce methane. The gas burns for cooking and light,
and the spent slurry is a good manure — so a biogas plant replaces firewood,
removes the smoke from the kitchen, and fertilises the field at the same time.

```photo id="bio12/aeration-tank" caption="An aeration tank in a working sewage treatment plant (Bengaluru, India). Air is bubbled through the sewage so that the flocs of bacteria and fungi in it can consume the organic matter — the secondary stage that cuts the BOD." width="80"
```

```figure caption="Sewage treatment. Primary treatment is purely physical; it is the secondary stage — an aeration tank full of flocs of bacteria and fungi — that actually consumes the organic matter and cuts the BOD by around 90 per cent."
fig, ax = plt.subplots(figsize=(5.0, 3.4))
ax.set_xlim(0, 10.6); ax.set_ylim(-0.32, 8.80); ax.axis("off")
FB = matplotlib.patches.FancyBboxPatch

def box(x, y, w, h, title, body, col, fc):
    ax.add_patch(FB((x, y), w, h, boxstyle="round,pad=0.09",
                    fc=fc, ec=col, lw=1.3, zorder=3))
    ax.text(x + w / 2, y + h - 0.34, title, ha="center", va="center",
            fontsize=6.8, color=col, zorder=4)
    ax.text(x + w / 2, y + h / 2 - 0.34, body, ha="center", va="center",
            fontsize=5.9, color=INK, linespacing=1.3, zorder=4)

def down(x, y0, y1, c=MUTED):
    ax.annotate("", xy=(x, y1), xytext=(x, y0),
                arrowprops=dict(arrowstyle="-|>", color=c, lw=1.3,
                                mutation_scale=10), zorder=2)

box(1.15, 7.10, 6.20, 1.30, "SEWAGE IN",
    "domestic waste water: organic matter, microbes, high BOD",
    MUTED, "#eef0f3")
down(4.25, 7.05, 6.55)
box(1.15, 5.10, 6.20, 1.40, "PRIMARY  (physical)",
    "screening, grit removal, sedimentation\n→ primary sludge settles out",
    ACCENT, "#eaf1f8")
down(4.25, 5.05, 3.55)
box(1.15, 2.10, 6.20, 1.40, "SECONDARY  (biological)",
    "aeration tank: flocs of aerobic bacteria + fungi\noxidise the organics; BOD falls by about 90 %",
    "#2e8b57", "#eaf6ee")
down(4.25, 2.05, 0.95)
box(1.15, 0.05, 6.20, 0.85, "settling tank → treated effluent released",
    "", INK, "#f7f8fa")
# activated sludge recycle
ax.annotate("", xy=(7.95, 2.80), xytext=(7.95, 0.62),
            arrowprops=dict(arrowstyle="-|>", color="#b8860b", lw=1.3,
                            mutation_scale=10,
                            connectionstyle="arc3,rad=0.0"), zorder=2)
ax.plot([7.45, 7.95], [0.62, 0.62], color="#b8860b", lw=1.3, zorder=2)
ax.plot([7.95, 7.45], [2.80, 2.80], color="#b8860b", lw=1.3, zorder=2)
ax.annotate("", xy=(7.48, 2.80), xytext=(7.80, 2.80),
            arrowprops=dict(arrowstyle="-|>", color="#b8860b", lw=1.3,
                            mutation_scale=10), zorder=2)
ax.text(8.15, 1.72, "activated\nsludge\nrecycled", ha="left", va="center",
        fontsize=5.9, color="#b8860b", linespacing=1.3, zorder=4)
ax.text(8.15, 5.80, "sludge to an\nanaerobic digester\n→ biogas",
        ha="left", va="center", fontsize=5.9, color=MUTED,
        linespacing=1.3, zorder=4)
ax.annotate("", xy=(8.05, 5.80), xytext=(7.45, 5.80),
            arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.0,
                            mutation_scale=9), zorder=2)
fig.tight_layout()
```

## Chapter summary

- **Apiculture** is the keeping of *Apis* species in hives. Nepal's hive bee is
  ***Apis cerana***; *A. mellifera* was introduced in 1992; *A. dorsata*,
  *A. laboriosa* and *A. florea* build single open combs and are hunted, not
  kept. The movable-frame hive works because bees leave a **bee space** of
  6.4–9.5 mm, discovered by Langstroth in 1851 and patented in 1852. Pollination
  is worth more than the honey: 87 leading food crops depend on animal
  pollinators.
- A colony has one **queen**, sterile female **workers** and haploid **drones**
  from unfertilised eggs. All larvae get royal jelly for about three days; only
  the queen larva stays on it.
- **Sericulture** rears ***Bombyx mori*** on mulberry (*Morus alba*). The larva
  passes **five instars and four moults** in 29–30 days, then spins a cocoon of
  one filament 600–900 m long. The pupa is killed by **stifling** before it can
  emerge and cut the filament. **4,000–7,000 cocoons make one kilogram of raw
  silk**, which is 75–80 % fibroin and 20–25 % sericin.
- **Composite fish culture** stocks six carps with different feeding niches in
  one pond: silver carp (**phytoplankton**), catla (**zooplankton**), rohu
  (column), grass carp (weeds), mrigal and common carp (bottom). Carps mature in
  ponds but will not **spawn** there, so breeding is induced by hormone
  injection — Hiralal Chaudhuri, 1956.
- **Poultry**: *Gallus gallus domesticus* from the red junglefowl; broilers reach
  slaughter weight in 4–6 weeks, layers approach 500 eggs by 100 weeks. Nepal has
  exactly three indigenous breeds — **Sakini, Ghanti Khuile, Pwankh Ulte**.
  Ranikhet is Newcastle disease, caused by avian paramyxovirus type 1.
- **Animal husbandry**: buffalo (*Bubalus bubalis*, **riverine** type) give
  **52.1 %** of Nepal's milk. The yak–cattle hybrid is the **chauri**: females
  fertile, **F₁ males sterile**, milk yield higher but fat percentage lower than
  pure yak. **Vermicomposting** uses **epigeic** worms only, chiefly *Eisenia
  fetida*; the bed takes 60–140 days and yields compost of 0.5–1.5 % N.
- **Pearl culture** inserts a shell bead **together with a mantle graft
  (*saibo*)**, which forms the pearl sac that secretes nacre; the grain of sand
  is a myth, and neither pearl culture nor **lac culture** (*Kerria lacca*) is
  practised in Nepal.
- **Microbial disease**: know agent, type, vector and prevention exactly —
  *Mycobacterium tuberculosis* (airborne, BCG, DOTS, ZN stain giving **red
  bacilli on a blue ground**), *Salmonella* Typhi and *Vibrio cholerae* O1/O139
  (faecal–oral), *Plasmodium* (**female *Anopheles***), *Leishmania donovani*
  (**female *Phlebotomus argentipes***), dengue virus (**day-biting *Aedes***),
  SARS-CoV-2 (the virus; COVID-19 the disease).
- **Applied microbiology**: a vaccine gives **artificial active** immunity, and
  the secondary response is faster, a hundred- to a thousand-fold larger and
  mostly **IgG**. Antibiotics attack prokaryote-only targets — wall, 70S
  ribosome, gyrase, folate pathway — and are therefore useless against viruses;
  misuse breeds resistance carried on plasmids. Useful microbes run our curd
  (*Lactobacillus*), bread and beer (*Saccharomyces*), biofertiliser
  (*Rhizobium*, *Azotobacter*, *Anabaena*), biopesticide (*Bacillus
  thuringiensis*), biogas (methanogenic **archaea**) and the secondary stage of
  sewage treatment.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The hive bee of Nepal is <span class="marks">[1]</span>
   (a) *Apis dorsata* (b) *Apis cerana* (c) *Apis laboriosa* (d) *Apis florea*
2. The bee space exploited by the movable-frame hive is about <span class="marks">[1]</span>
   (a) 1–2 mm (b) 6.4–9.5 mm (c) 15–20 mm (d) 25–30 mm
3. The larva of *Bombyx mori* passes through <span class="marks">[1]</span>
   (a) three instars and two moults (b) four instars and four moults
   (c) five instars and four moults (d) five instars and five moults
4. In composite fish culture the surface phytoplankton feeder is <span class="marks">[1]</span>
   (a) catla (b) mrigal (c) silver carp (d) grass carp
5. Ranikhet disease of poultry is caused by <span class="marks">[1]</span>
   (a) a bacterium (b) a protozoan (c) avian paramyxovirus type 1 (d) *Eimeria tenella*
6. The earthworm species normally used in vermicomposting is <span class="marks">[1]</span>
   (a) *Lumbricus terrestris* (b) *Eisenia fetida* (c) *Pheretima posthuma* (d) *Lampito mauritii*
7. In the Ziehl–Neelsen stain, acid-fast bacilli appear <span class="marks">[1]</span>
   (a) blue on a red ground (b) red on a blue ground (c) purple on a pink ground (d) colourless
8. Kala-azar is transmitted by the bite of <span class="marks">[1]</span>
   (a) female *Anopheles* (b) *Aedes aegypti* (c) female *Phlebotomus argentipes* (d) a chigger mite
9. Which of these is **not** a target of any antibiotic? <span class="marks">[1]</span>
   (a) peptidoglycan cell wall (b) 70S ribosome (c) DNA gyrase (d) viral capsid
10. Methane in a biogas plant is produced by <span class="marks">[1]</span>
    (a) *Lactobacillus* (b) methanogenic archaea (c) *Saccharomyces cerevisiae* (d) *Rhizobium*

::: note Answers to Group A
**1.** (b) — *A. cerana* nests in cavities and so can be hived; the other three
build single open combs.
**2.** (b) — 6.4–9.5 mm, the gap bees neither fill with comb nor seal with propolis.
**3.** (c) — five instars, four **larval** moults; the fifth moult happens inside
the cocoon.
**4.** (c) — silver carp takes phytoplankton; catla takes zooplankton. Do not swap them.
**5.** (c) — Ranikhet and Newcastle disease are the same viral disease.
**6.** (b) — *Eisenia fetida* is epigeic. *Lumbricus terrestris* is anecic and unsuitable.
**7.** (b) — carbol fuchsin is retained through acid-alcohol; methylene blue counterstains everything else.
**8.** (c) — the female sandfly *Phlebotomus argentipes*.
**9.** (d) — a virus has no wall, no ribosome and no gyrase, which is why
antibiotics do not work on it.
**10.** (b) — methanogens are **archaea**, not bacteria.
:::

**Group B — Short answer (4 marks each)**

1. Define apiculture. Name any two species of *Apis* found in Nepal and state one
   difference between them. <span class="marks">[4]</span>
2. What is bee space, and why did its discovery matter? Describe the castes of a
   honey bee colony. <span class="marks">[4]</span>
3. Nepal produced 4,278 MT of honey from 276,000 hives. Calculate the yield per
   hive and comment on the figure. <span class="marks">[4]</span>
4. Describe the life cycle of *Bombyx mori* and explain why the pupa is killed
   before the moth emerges. <span class="marks">[4]</span>
5. What is composite fish culture? Give the six species used and the feeding zone
   of each. <span class="marks">[4]</span>
6. Why do carps fail to breed in ponds, and how is the problem
   overcome? <span class="marks">[4]</span>
7. Write short notes on the three ecological groups of earthworms and state which
   is used in vermicomposting, with a reason. <span class="marks">[4]</span>
8. Differentiate between a broiler and a layer. Name Nepal's three indigenous
   chicken breeds. <span class="marks">[4]</span>
9. State Koch's postulates and give one limitation of
   them. <span class="marks">[4]</span>
10. Why are antibiotics ineffective against viral infections? Name two
    antibiotics with their target site. <span class="marks">[4]</span>
11. Distinguish between the primary and the secondary immune response, and
    explain why a booster dose is given. <span class="marks">[4]</span>
12. Name the causative agent, mode of transmission, two symptoms and one
    preventive measure of (a) cholera and (b) dengue. <span class="marks">[4]</span>

::: note Answers to Group B
**1.** Apiculture is the rearing and management of honey bees in hives for honey,
wax and pollination. Any two of *Apis cerana*, *A. mellifera*, *A. dorsata*,
*A. laboriosa*, *A. florea*. A usable difference: *A. cerana* builds **several
combs inside a cavity** and can therefore be kept in a hive, while *A. dorsata*
builds a **single open comb** on a tree or cliff and cannot.

**3.** $\dfrac{4\,278\,000\ \text{kg}}{276\,000} = 15.5$ kg per hive. Comment:
this is slightly below the 16.45 kg per hive reported in 2019, and recent studies
report both yield per hive and the number of occupied hives falling, attributed
to loss of bee forage, pesticides and brood disease.

**4.** Egg (10–14 d) → larva, five instars and four moults, feeding only on
mulberry (29–30 d) → spins a cocoon over 2–3 days and pupates inside → adult
moth, which does not feed and cannot fly. The pupa is killed by **stifling**
because an emerging moth secretes a softening fluid and bites its way out,
**cutting the single continuous filament into useless short lengths** so the
cocoon can no longer be reeled.

**5.** See the table in §10.1: silver carp — surface, phytoplankton; catla —
surface and mid-water, zooplankton; rohu — column, omnivore; grass carp —
margins, macrophytes; mrigal — bottom, detritus; common carp — bottom, omnivore.
The point of the arrangement is that the six occupy different **feeding niches**,
so all layers of the pond's food are harvested and no two species compete.

**6.** Carps **mature** in a pond but do not **spawn**, because still water gives
none of the riverine stimuli — rising level, current, monsoon turbidity — needed
for final maturation and the release of gametes. The problem is overcome by
**induced breeding**: an injection of pituitary extract or of a synthetic GnRH
analogue with domperidone (Ovaprim) into ripe brooders, which then spawn in a
hapa or circular hatchery within a few hours.

**10.** Because every antibiotic target is a **prokaryotic** structure —
peptidoglycan wall, 70S ribosome, DNA gyrase, bacterial folate synthesis — and a
virus has none of them; it is acellular and replicates using the host cell's own
machinery, so antivirals are required instead. Two examples: **penicillin**
inhibits cell-wall synthesis; **streptomycin** binds the **30S** ribosomal
subunit. (Also acceptable: erythromycin — 50S; ciprofloxacin — DNA gyrase;
rifampicin — RNA polymerase; sulfonamide — folate synthesis.)

**12.** (a) Cholera — *Vibrio cholerae* serogroup O1 or O139; faecal–oral through
contaminated water; painless rice-water stools and rapid dehydration with cramps;
prevented by chlorinated safe water (and treated with ORS). (b) Dengue — dengue
virus, serotypes 1–4; bite of the **day-biting** *Aedes aegypti* or
*Ae. albopictus*; high fever with retro-orbital pain, severe body and joint ache,
rash and low platelet count; prevented by destroying clean-water breeding sites
around the house.
:::

**Group C — Long answer (8 marks each)**

1. What is sericulture? Describe the life cycle of *Bombyx mori* with a labelled
   diagram, and outline the steps from harvested cocoon to reeled raw
   silk. <span class="marks">[8]</span>
2. Describe composite fish culture. Explain with a diagram why six species are
   stocked together, and describe how carps are bred
   artificially. <span class="marks">[8]</span>
3. Describe apiculture under the headings: bee species of Nepal, castes of a
   colony, the movable-frame hive, and economic importance. <span class="marks">[8]</span>
4. "Microorganisms are both our worst enemies and our most useful servants."
   Justify this statement with four named diseases (agent, transmission,
   prevention) and four named useful applications. <span class="marks">[8]</span>
5. Write an account of vaccines and antibiotics: what each is, how each works,
   the main types of each, and why an antibiotic cannot be used to treat
   COVID-19. <span class="marks">[8]</span>

::: note Answers to Group C — outlines
**1.** Definition; *Bombyx mori*, Bombycidae, monophagous on *Morus alba*.
Cycle: egg (10–14 d) → five larval instars with four moults (29–30 d) → spinning
2–3 days → pupa in cocoon → non-feeding flightless adult. Diagram: the
four-stage cycle, with the harvest point marked between cocoon and adult. Steps:
harvesting → **stifling** → deflossing → cooking → reeling in a filature →
throwing → degumming → weaving. Add numbers for the marks: filament 600–900 m
reelable; 4,000–7,000 cocoons per kg raw silk; raw silk = fibroin 75–80 % +
sericin 20–25 %. Close with Nepal: Khopasi centre, about 1,538 ha of mulberry.

**2.** Definition of polyculture; the pond as several habitats; the six species
with zone and food (silver carp/phytoplankton, catla/zooplankton, rohu/column,
grass carp/weeds, mrigal/detritus, common carp/bottom); the argument that
different niches mean no competition and full use of the natural food, so yield
per hectare rises. Diagram: pond section with the six placed at their depths.
Induced breeding: carps mature but do not spawn without riverine cues;
hypophysation (Chaudhuri, 1956) or Ovaprim; brooders in a hapa; eggs to hatching
jars. Finish with Nepal's 5.62 t ha⁻¹ pond yield and the 84 % aquaculture share.

**4.** Enemies — choose four from the table and give all three required facts for
each, e.g. TB (*M. tuberculosis*, airborne, BCG + DOTS), cholera (*V. cholerae*
O1/O139, faecal–oral, chlorination + ORS), malaria (*Plasmodium*, female
*Anopheles*, bed nets + ACT), COVID-19 (SARS-CoV-2, droplets, vaccination).
Servants — four from: *Lactobacillus* for curd; *Saccharomyces cerevisiae* for
bread and alcohol; *Rhizobium* or *Azotobacter* as biofertiliser; *Bacillus
thuringiensis* as biopesticide; *Penicillium rubens* and *Streptomyces griseus*
for antibiotics; methanogenic archaea for biogas; aerobic flocs in the secondary
stage of sewage treatment. A sentence of judgement at the end earns the last
mark.

**5.** Vaccine = preparation of a pathogen or its antigen that provokes a primary
response and leaves memory cells, i.e. **artificial active immunity**; Jenner
1796 (cowpox), Pasteur coined the word 1881. Types with examples: live
attenuated, killed, subunit/conjugate, toxoid, mRNA, viral vector. Mechanism:
primary response slow and IgM; secondary fast, 100–1000× larger, IgG — hence
boosters. Antibiotic = substance from one microorganism that kills or inhibits
another; Fleming 1928, Florey and Chain 1940–41, Nobel 1945. Targets: cell wall,
70S ribosome (30S and 50S), DNA gyrase and RNA polymerase, folate synthesis;
broad vs narrow spectrum, bactericidal vs bacteriostatic. Why not for COVID-19:
SARS-CoV-2 is a **virus** with no wall, no ribosome, no gyrase and no metabolism
of its own, so no antibiotic target exists; it needs antivirals or vaccination,
and using antibiotics anyway only selects for resistant bacteria.
:::
