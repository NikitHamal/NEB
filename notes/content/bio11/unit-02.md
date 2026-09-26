---
subject: Biology
grade: 11
unit: 2
title: Floral Diversity
hours: 30
area: Botany
---

Nepal occupies about one tenth of one per cent of the land surface of the Earth,
yet more than three per cent of all known plant species grow inside its borders.
Walk from the Terai at 60 m to the Kanchenjunga snowline at 8,586 m and you pass
through sal forest, subtropical *Schima*–*Castanopsis* forest, oak and
rhododendron, blue pine, birch, juniper scrub and finally cushion plants on bare
moraine — the whole latitudinal sweep of the northern hemisphere compressed into
200 km. This unit is the catalogue of that diversity. It is the largest unit in
the Grade 11 course (30 of the 64 Botany hours) and it carries the largest share
of the Botany marks, so it rewards steady work rather than last-week cramming.

The plan is simple and it is the plan evolution itself followed. We begin with
how biologists name and sort organisms, then climb the plant kingdom step by
step: fungi (not plants at all, but traditionally studied here), lichens, algae,
bryophytes, pteridophytes, gymnosperms and finally the angiosperms, where four
named families are studied in detail. At every step ask the same three questions
— what is the plant body like, how does it reproduce, and what is it used for?

::: key What the examiner asks from this unit
The Botany section of the paper draws four short answers and one long answer, and
this unit supplies most of them. Expect: a **comparison table** (bryophyta vs
pteridophyta, gymnosperm vs angiosperm, monocot vs dicot, algae vs fungi); a
**labelled diagram** of *Rhizopus*, *Spirogyra*, *Funaria*, a fern sorus, a
*Pinus* shoot or an L.S. of a flower; a **life cycle** with ploidy levels marked;
**economic importance** of a group with named examples; and for 8 marks the full
account of one family with floral formula and floral diagram. The four families
are the single most reliable long question in the whole paper.
:::

## 2.1 Introduction

### Three domains of life

For a century all living things were sorted into two groups, plants and animals.
The electron microscope destroyed that scheme by revealing a far deeper divide
than the one between an oak and an ox: the divide between cells that keep their
DNA in a nucleus and cells that do not. Then in 1977 **Carl Woese** compared the
base sequences of 16S ribosomal RNA across hundreds of organisms and found that
the prokaryotes were not one group but two, as different from each other as
either is from us. He proposed the **three domains** — the highest rank in modern
classification, above kingdom.

```figure caption="The three domains of life on a ribosomal-RNA cladogram, and Whittaker's five kingdoms with the criteria that separate them. Archaea and Bacteria are prokaryotic; the other three kingdoms are eukaryotic."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, (axL, axR) = plt.subplots(1, 2, figsize=(5.2, 2.6),
                               gridspec_kw={'width_ratios': [1.0, 1.25], 'wspace': 0.10})

def seg(ax, x1, y1, x2, y2, lw=1.3):
    ax.plot([x1, x2], [y1, y2], color=INK, lw=lw, solid_capstyle='round')

# ---- left: three domains -------------------------------------------------
seg(axL, 0.02, 0.52, 0.18, 0.52)
seg(axL, 0.18, 0.15, 0.18, 0.66)
seg(axL, 0.18, 0.15, 0.82, 0.15)
seg(axL, 0.18, 0.66, 0.44, 0.66)
seg(axL, 0.44, 0.46, 0.44, 0.86)
seg(axL, 0.44, 0.46, 0.82, 0.46)
seg(axL, 0.44, 0.86, 0.82, 0.86)

for y, s, sub in [(0.15, 'BACTERIA', 'prokaryotic'),
                  (0.46, 'ARCHAEA', 'prokaryotic'),
                  (0.86, 'EUKARYA', 'eukaryotic')]:
    axL.text(0.88, y + 0.055, s, ha='left', va='bottom', fontsize=6.5,
             color=INK, fontweight='bold')
    axL.text(0.88, y - 0.055, sub, ha='left', va='top', fontsize=5.9,
             color=MUTED, style='italic')
axL.text(0.00, 0.52, 'common ancestor', rotation=90, ha='right', va='center',
         fontsize=5.9, color=MUTED)
axL.set_title('Three domains (Woese, 1990)', fontsize=7.2, color=INK, pad=4)
axL.set_xlim(-0.16, 1.98)
axL.set_ylim(-0.04, 1.06)

# ---- right: five kingdoms -----------------------------------------------
tints = ['#f3e7d4', '#e3eef7', '#eae3f2', '#e2f0e2', '#f7e2e2']
boxes = [
    (0.04, 0.02, 0.92, 0.22, 'MONERA\nprokaryotic', tints[0]),
    (0.17, 0.35, 0.66, 0.22, 'PROTISTA\nunicellular eukaryotes', tints[1]),
    (0.02, 0.70, 0.30, 0.22, 'FUNGI\nabsorptive', tints[2]),
    (0.35, 0.70, 0.30, 0.22, 'PLANTAE\nautotrophic', tints[3]),
    (0.68, 0.70, 0.30, 0.22, 'ANIMALIA\ningestive', tints[4]),
]
for x, y, w, h, s, c in boxes:
    axR.add_patch(FancyBboxPatch((x, y), w, h,
                                 boxstyle='round,pad=0,rounding_size=0.035',
                                 fc=c, ec=INK, lw=0.9))
    axR.text(x + w / 2, y + h / 2, s, ha='center', va='center',
             fontsize=6.3, color=INK, linespacing=1.35)

seg(axR, 0.50, 0.24, 0.50, 0.35, lw=1.0)
seg(axR, 0.50, 0.57, 0.50, 0.635, lw=1.0)
seg(axR, 0.17, 0.635, 0.83, 0.635, lw=1.0)
for x in (0.17, 0.50, 0.83):
    seg(axR, x, 0.635, x, 0.70, lw=1.0)
axR.set_title('Five kingdoms (Whittaker, 1969)', fontsize=7.2, color=INK, pad=4)
axR.set_xlim(-0.02, 1.02)
axR.set_ylim(-0.10, 1.05)

for ax in (axL, axR):
    ax.axis('off')
```

| Feature | Archaea | Bacteria | Eukarya |
|---|---|---|---|
| Nucleus | absent | absent | present |
| Cell wall | pseudopeptidoglycan or protein | peptidoglycan (murein) | cellulose, chitin or none |
| Membrane lipids | branched, ether-linked | unbranched, ester-linked | unbranched, ester-linked |
| Ribosome | 70S | 70S | 80S (cytoplasmic) |
| Introns in genes | present in some | absent | present |
| Sensitive to streptomycin | no | yes | no |
| Histone proteins | present | absent | present |
| Habitat | often extreme (hot springs, brine, gut) | everywhere | everywhere |
| Examples | *Methanobacterium*, *Halobacterium*, *Sulfolobus* | *Escherichia coli*, *Rhizobium*, *Nostoc* | *Spirogyra*, *Agaricus*, mango, human |

Archaea are the extremophiles: the **methanogens** that make marsh gas and
biogas, the **halophiles** of salt pans, and the **thermoacidophiles** of the hot
springs at Tatopani, some of which grow happily above 100 °C. Their tough,
ether-linked lipids are what let them do it.

::: definition Domain
The highest taxonomic rank, above kingdom, based chiefly on ribosomal RNA
sequence and cell architecture. The three domains are Archaea, Bacteria and
Eukarya; the first two together were formerly the single kingdom Monera.
:::

### Binomial nomenclature

Common names are useless for science. "Chyau" means any mushroom; the plant a
Kathmandu shopkeeper calls *tulsi* is not the plant a Bengali calls *tulsi*; and
the marigold of Nepal, Mexico and Africa are three different species. The cure is
**binomial nomenclature**, formalised by the Swedish naturalist **Carl Linnaeus**
in *Species Plantarum* (1753), which is taken as the starting point of all modern
plant names.

::: definition Binomial nomenclature
The system of giving every species a two-word Latin name, in which the first word
is the **genus** (generic name) and the second is the **species epithet** (specific
epithet). Together the two words, and only the two together, name the species.
:::

The rules are laid down in the **International Code of Nomenclature for algae,
fungi, and plants (ICN)**, revised at each International Botanical Congress. The
ones you must be able to state are:

- The name is written in Latin or latinised form, whatever the language of origin.
- It has exactly two parts. The genus begins with a **capital** letter, the species
  epithet with a **small** letter, even when it honours a person — *Pinus
  wallichiana*, not *Pinus Wallichiana*.
- The whole binomial is **italicised** in print and **underlined separately**
  (each word underlined on its own) in handwriting.
- The author's name may be added, unitalicised and abbreviated, after the
  binomial: *Oryza sativa* L. means the species was first validly described by
  Linnaeus.
- Names must be published with a description and a preserved **type specimen**
  lodged in a herbarium. For Nepal the National Herbarium and Plant Laboratories
  (KATH) at Godawari holds that role.
- The **principle of priority** applies: where two names exist for one species,
  the earliest validly published name wins, the later one becoming a synonym.
- A tautonym (the same word twice, as in *Bison bison*) is allowed in zoology but
  **not** in botany.

| Plant | Binomial | Family |
|---|---|---|
| Rice (dhan) | *Oryza sativa* | Poaceae |
| Sal | *Shorea robusta* | Dipterocarpaceae |
| Lali gurans (national flower) | *Rhododendron arboreum* | Ericaceae |
| Mustard (tori) | *Brassica campestris* | Brassicaceae |
| Potato (alu) | *Solanum tuberosum* | Solanaceae |
| Onion (pyaj) | *Allium cepa* | Liliaceae (sensu lato) |
| Chilaune | *Schima wallichii* | Theaceae |
| Yew (loth salla) | *Taxus wallichiana* | Taxaceae |

### Five-kingdom classification

**Robert H. Whittaker** proposed the five-kingdom system in **1969**, using three
criteria that Linnaeus could not have used: cell structure (prokaryotic or
eukaryotic), body organisation (unicellular, colonial, multicellular with or
without tissues) and **mode of nutrition** (autotrophic, saprophytic by
absorption, or heterotrophic by ingestion). That last criterion is what finally
pulled fungi out of the plant kingdom, where they had sat for two centuries.

| Kingdom | Cell type | Wall | Nutrition | Body | Examples |
|---|---|---|---|---|---|
| Monera | prokaryotic | peptidoglycan | autotrophic or heterotrophic | unicellular | bacteria, *Nostoc*, mycoplasma |
| Protista | eukaryotic | variable or absent | photosynthetic or heterotrophic | unicellular or colonial | *Chlamydomonas*, diatoms, *Amoeba*, *Plasmodium* |
| Fungi | eukaryotic | chitin | saprophytic or parasitic, absorptive | mycelial (coenocytic or septate) | *Rhizopus*, *Agaricus*, yeast |
| Plantae | eukaryotic | cellulose | autotrophic (photosynthetic) | multicellular with tissues | mosses, ferns, *Pinus*, mango |
| Animalia | eukaryotic | absent | heterotrophic by ingestion | multicellular with tissues and organs | *Hydra*, earthworm, frog, human |

**Monera** deserves a paragraph because everything else in the unit is
eukaryotic. Its members are prokaryotes: no nucleus, no membrane-bound
organelle, a single circular DNA molecule, 70S ribosomes and a wall of
peptidoglycan. They may be autotrophic (photoautotrophic cyanobacteria such as
*Nostoc* and *Anabaena*, which fix both carbon and nitrogen; chemoautotrophic
*Nitrosomonas* and *Nitrobacter*, which run the nitrogen cycle) or heterotrophic
(saprophytic decomposers, symbiotic *Rhizobium* in root nodules, and pathogens
such as *Xanthomonas oryzae* of rice). Cyanobacteria used to be called
blue-green algae, and some books still place them with the algae; on the
five-kingdom scheme they are Monera, because the cell is prokaryotic. Viruses
are excluded from all five kingdoms altogether — they are acellular, obligate
intracellular parasites, and they are dealt with with the bacteria in Unit 3.

::: caution Where the system creaks
Whittaker's scheme is a teaching scheme, not the last word. Protista is a
dustbin: it holds photosynthetic *Chlamydomonas*, animal-like *Amoeba* and
fungus-like slime moulds together only because they are all "simple
eukaryotes". Monera lumps the two prokaryotic domains that Woese later showed
are profoundly different. Modern classification has moved on, but the NEB
syllabus asks for the five kingdoms, so learn them — and be able to say why
they are imperfect.
:::

### Flora status of Nepal

Nepal covers **147,181 km²**, about 0.1 % of the Earth's land, and squeezes an
altitudinal range of more than 8,500 m into an average north–south width of
193 km. That vertical compression, plus its position at the meeting point of the
Palaearctic and Oriental realms, gives the country a flora out of all proportion
to its size: over **3 %** of the world's known plants. The figures below follow
Nepal's National Biodiversity Strategy and Action Plan (2014) and the Department
of Plant Resources; they are revised upward almost every year as new collections
are described, so quote them as approximations.

| Group | Species recorded in Nepal | Share of world total |
|---|---|---|
| Angiosperms (flowering plants) | about 6,500 (NBSAP lists 6,973) | about 2.7 % |
| Gymnosperms | 28 (about 20 indigenous) | about 2.8 % |
| Pteridophytes (ferns and allies) | 534 | about 5 % |
| Bryophytes | 1,150 | about 6 % |
| Lichens | 771 | about 4 % |
| Fungi | about 2,000 | under 2 % |
| Algae | about 800 | about 2 % |

Nepal recognises **118 ecosystems**, **75 vegetation types** and **35 forest
types**. About **300 flowering plants are endemic** — found nowhere else on Earth
(published estimates range from 284 to over 400 depending on the treatment of
doubtful taxa), most of them in the high Himalaya where isolation by ridge and
valley is greatest. Forest covers roughly 45 % of the country if shrubland is
included. Against that richness stand real threats: over-collection of medicinal
plants such as *Nardostachys jatamansi* (jatamansi), *Neopicrorhiza
scrophulariiflora* (kutki) and *Ophiocordyceps sinensis* (yarsagumba), the
clearing of Terai forest for settlement, invasive species such as *Mikania
micrantha* and *Lantana camara*, and the upslope creep of vegetation belts under
a warming climate.

::: example Worked example 2.1 — Nepal's flora in proportion
Nepal's land area is 147,181 km²; the world's land area is about
148,940,000 km². Nepal has about 6,500 flowering plants; the world has about
250,000. Show that Nepal's flora is disproportionately rich, and express that
disproportion as a single number.

**Share of land area**

(147,181 ÷ 148,940,000) × 100 = 0.0988 % ≈ **0.1 %**

**Share of flowering plants**

(6,500 ÷ 250,000) × 100 = **2.6 %**

**The disproportion** is the ratio of these two shares:

2.6 ÷ 0.0988 ≈ **26**

So a square kilometre of Nepal carries, on average, about **26 times** as many
species of flowering plant as an average square kilometre of the Earth's land
surface. This single figure is the quantitative statement of "Nepal is a
biodiversity hotspot", and the cause is the altitudinal range: climbing 1,000 m
is climatically equivalent to travelling roughly 1,000 km towards the pole, so a
single Nepali hillside stacks many climates one above another.
:::

## 2.2 Fungi

Fungi are eukaryotic, **achlorophyllous**, heterotrophic organisms with a body of
thread-like **hyphae** and a cell wall of **chitin**. They cannot make their own
food and they cannot swallow it either, so they do the only thing left: they
secrete digestive enzymes onto the substrate and absorb the soluble products.
That single habit — **absorptive heterotrophy** — explains almost everything
else about them. It explains the hypha, which is the ideal shape for
penetrating a substrate and maximising surface area; it explains why fungi are
the chief decomposers of the biosphere; and it explains why so many are
parasites. The study of fungi is **mycology**.

**The plant body.** Except in the unicellular yeasts, the fungal body is a
**mycelium**, a network of hyphae. A hypha is a tube of cytoplasm bounded by a
chitinous wall, growing only at its tip. Hyphae are of two kinds: **coenocytic**
(aseptate) hyphae have no cross-walls, so the whole mycelium is one long
multinucleate cell, as in *Rhizopus* and *Mucor*; **septate** hyphae are divided
by cross-walls into uninucleate, binucleate or multinucleate compartments, as in
*Penicillium* and *Agaricus*. Reserve food is stored as **glycogen** and oil, never
as starch. In the higher fungi the hyphae may be packed into hard, tissue-like
masses called **plectenchyma** that form the stalk and cap of a mushroom.

```figure caption="Three fungi: the coenocytic mycelium of *Rhizopus stolonifer*, the basidiocarp of *Agaricus*, and a budding yeast cell of *Saccharomyces cerevisiae*."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Polygon, FancyArrowPatch

fig, (a, b, c) = plt.subplots(1, 3, figsize=(5.2, 2.7),
                              gridspec_kw={'width_ratios': [1.05, 1.0, 0.60],
                                           'wspace': 0.06})
rng = np.random.default_rng(4)

def lab(ax, s, xy, xytext, ha='left', fs=6.2):
    ax.annotate(s, xy=xy, xytext=xytext, ha=ha, va='center', fontsize=fs,
                color=INK, arrowprops=dict(arrowstyle='-', lw=0.6, color=MUTED,
                                           shrinkA=1, shrinkB=1))

# ---------------- (a) Rhizopus ------------------------------------------
a.plot([0.30, 2.55], [1.05, 1.05], color=INK, lw=1.2)
for bx in (0.62, 2.25):
    a.plot([bx, bx], [1.05, 2.05], color=INK, lw=1.2)
    a.add_patch(Circle((bx, 2.28), 0.245, fc='#5b4636', ec=INK, lw=0.9))
    for k in range(16):
        t = rng.uniform(0, 2 * np.pi)
        r = 0.20 * np.sqrt(rng.uniform(0, 1))
        a.plot([bx + r * np.cos(t)], [2.28 + r * np.sin(t)], marker='o',
               ms=1.1, color='#e8e0d4')
    a.plot([bx - 0.10, bx, bx + 0.10], [2.10, 2.16, 2.10], color=INK, lw=0.8)
    # rhizoids
    for dx in (-0.20, -0.07, 0.07, 0.20):
        a.plot([bx, bx + dx * 1.3], [1.02, 0.62], color=INK, lw=0.8)
        a.plot([bx + dx * 1.3, bx + dx * 1.9], [0.62, 0.42], color=INK, lw=0.7)
a.text(0.02, 2.96, 'a', ha='left', va='top', fontsize=7,
       color=MUTED, fontweight='bold')
lab(a, 'sporangium\n(spores)', (0.85, 2.32), (1.06, 2.70), fs=6.0)
lab(a, 'columella', (0.70, 2.13), (1.06, 2.26), fs=6.0)
lab(a, 'sporangiophore', (2.25, 1.55), (2.10, 1.55), ha='right', fs=6.0)
lab(a, 'stolon', (1.60, 1.05), (1.60, 0.82), ha='center', fs=6.0)
lab(a, 'rhizoids', (0.50, 0.50), (1.15, 0.36), fs=6.0)
a.set_xlim(-0.05, 3.00)
a.set_ylim(0.10, 3.00)

# ---------------- (b) Agaricus ------------------------------------------
t = np.linspace(0, np.pi, 200)
cap = np.column_stack([1.35 + 1.05 * np.cos(t), 1.92 + 0.60 * np.sin(t)])
b.add_patch(Polygon(cap, closed=True, fc='#c9a882', ec=INK, lw=1.0))
for gx in np.linspace(0.45, 2.25, 15):
    b.plot([gx, gx], [1.92, 1.64], color='#8c6b52', lw=0.8)
b.plot([0.35, 2.35], [1.92, 1.92], color=INK, lw=1.0)
b.add_patch(FancyBboxPatch((1.18, 0.45), 0.34, 1.50,
                           boxstyle='round,pad=0,rounding_size=0.08',
                           fc='#f0e6d6', ec=INK, lw=1.0))
b.add_patch(Ellipse((1.35, 1.32), 0.66, 0.16, fc='#e2d2ba', ec=INK, lw=0.9))
for k, x0 in enumerate(np.linspace(0.55, 2.15, 5)):
    tt = np.linspace(0, 1, 60)
    b.plot(x0 + 0.34 * tt, 0.44 - 0.11 * np.sin(np.pi * tt * 2) - 0.05 * tt,
           color=MUTED, lw=0.7)
b.text(-0.50, 2.88, 'b', ha='left', va='top', fontsize=7,
       color=MUTED, fontweight='bold')
lab(b, 'pileus (cap)', (1.35, 2.40), (1.35, 2.74), ha='center', fs=6.0)
lab(b, 'gills', (2.15, 1.76), (2.62, 2.05), fs=6.0)
lab(b, 'annulus', (1.66, 1.32), (2.62, 1.42), fs=6.0)
lab(b, 'stipe', (1.52, 0.90), (2.62, 0.90), fs=6.0)
lab(b, 'mycelium', (0.75, 0.40), (0.30, 0.66), ha='right', fs=6.0)
b.set_xlim(-0.55, 3.55)
b.set_ylim(0.02, 2.92)

# ---------------- (c) yeast --------------------------------------------
c.add_patch(Ellipse((0.55, 2.25), 0.70, 0.86, fc='#f4ecdc', ec=INK, lw=1.0))
c.add_patch(Circle((0.52, 2.25), 0.13, fc='#cfe3f3', ec=INK, lw=0.8))
c.add_patch(Ellipse((1.00, 2.62), 0.30, 0.34, fc='#f4ecdc', ec=INK, lw=1.0))
c.add_patch(FancyArrowPatch((0.62, 1.66), (0.62, 1.34),
                            arrowstyle='-|>', mutation_scale=7,
                            lw=0.9, color=MUTED))
c.add_patch(Ellipse((0.55, 0.82), 0.70, 0.86, fc='#f4ecdc', ec=INK, lw=1.0))
c.add_patch(Circle((0.48, 0.82), 0.13, fc='#cfe3f3', ec=INK, lw=0.8))
c.add_patch(Ellipse((1.12, 1.24), 0.52, 0.58, fc='#f4ecdc', ec=INK, lw=1.0))
c.add_patch(Circle((1.18, 1.26), 0.11, fc='#cfe3f3', ec=INK, lw=0.8))
c.text(0.02, 0.30, 'c', ha='left', va='top', fontsize=7,
       color=MUTED, fontweight='bold')
lab(c, 'bud', (1.06, 2.66), (1.34, 2.90), fs=6.0)
lab(c, 'nucleus', (0.52, 2.25), (0.06, 2.86), ha='left', fs=6.0)
lab(c, 'nucleus\ndivides', (1.18, 1.26), (1.42, 0.92), fs=6.0)
c.set_xlim(0.00, 2.30)
c.set_ylim(0.02, 3.12)

for ax in (a, b, c):
    ax.set_aspect('equal')
    ax.axis('off')
```

**Nutrition.** Saprophytes (*Mucor*, *Agaricus*) live on dead organic matter;
parasites live on living hosts and may be **obligate** (*Puccinia*, which grows
only on a living host) or **facultative**; symbionts live in mutually beneficial
partnership, as in lichens and in the **mycorrhiza** of pine and orchid roots,
where the fungus supplies water and phosphate and receives sugars.

**Reproduction** occurs by all three routes. *Vegetative* reproduction is by
fragmentation, budding (yeast) or fission. *Asexual* reproduction is by spores:
motile **zoospores** in aquatic forms, non-motile **sporangiospores** formed
inside a sporangium (*Rhizopus*), **conidia** cut off from the tip of a
conidiophore (*Penicillium*, *Aspergillus*), **chlamydospores** and
**oidia**. *Sexual* reproduction runs through three steps that are worth
memorising as a sequence, because the fungal classes are defined by what happens
between them:

1. **Plasmogamy** — fusion of the protoplasts of two compatible gametes or
   hyphae, bringing two nuclei into one cell.
2. **Karyogamy** — fusion of the two nuclei to give a diploid nucleus.
3. **Meiosis** — restoring the haploid condition and producing spores.

In the lower fungi steps 1 and 2 follow immediately. In Ascomycetes and
Basidiomycetes they are separated by a long-lived **dikaryotic (n + n)** phase in
which the two nuclei divide side by side without fusing — a stage unique to
fungi.

| Class | Hyphae | Asexual spores | Sexual spores (in) | Common name | Examples |
|---|---|---|---|---|---|
| Phycomycetes (Zygomycetes) | coenocytic | zoospores, sporangiospores | zygospore | algal fungi | *Rhizopus*, *Mucor*, *Albugo* |
| Ascomycetes | septate | conidia | 8 ascospores in an ascus | sac fungi | *Saccharomyces*, *Penicillium*, *Morchella*, *Claviceps* |
| Basidiomycetes | septate, dikaryotic | usually none | 4 basidiospores on a basidium | club fungi | *Agaricus*, *Puccinia*, *Ustilago*, *Polyporus* |
| Deuteromycetes | septate | conidia only | **not known** | fungi imperfecti | *Alternaria*, *Colletotrichum*, *Fusarium* |

::: memory The four classes, by their sexual spore
**Zygo–Asco–Basidio**, then the class with none: *Deuteromycetes*. Remember the
spore counts as **8 in a sac, 4 on a club** — eight ascospores inside an ascus,
four basidiospores outside on a basidium. Deuteromycetes is a holding pen: once
a sexual stage is discovered, the fungus is moved to its proper class.
:::

**Three fungi to know by name.** *Rhizopus stolonifer*, the black bread mould, is
a coenocytic saprophyte that spreads by aerial **stolons** anchored by
**rhizoids**; erect **sporangiophores** bear a black **sporangium** with a domed
**columella** inside, releasing thousands of sporangiospores. Sexual reproduction
is by conjugation of two morphologically identical but physiologically different
(+ and −) hyphae, producing a thick-walled resting **zygospore**. *Agaricus*, the
cultivated mushroom, spends most of its life as an underground mycelium; the part
we eat is the **basidiocarp**, with a **pileus** (cap) bearing radiating
**gills** on its underside, a ring or **annulus**, and a **stipe** (stalk). The
basidia line the gills and each shoots off four basidiospores. *Saccharomyces
cerevisiae*, yeast, is unicellular, reproduces by **budding**, and ferments sugar
to ethanol and carbon dioxide.

| Field | Economic importance of fungi |
|---|---|
| Food | *Agaricus bisporus*, *Volvariella volvacea* and the prized *Morchella esculenta* (guchchi chyau) are eaten; yeast is a protein and vitamin-B source |
| Baking and brewing | *Saccharomyces cerevisiae* raises bread and ferments beer, wine and jaand |
| Antibiotics | penicillin from *Penicillium notatum* (Alexander Fleming, 1928); griseofulvin from *P. griseofulvum* |
| Other industry | citric acid from *Aspergillus niger*; enzymes; cheese ripened by *Penicillium roqueforti* and *P. camemberti*; gibberellin from *Gibberella* |
| Soil fertility | the chief decomposers of cellulose and lignin; mycorrhizae improve phosphate uptake in forest trees |
| Crop diseases | *Puccinia graminis* (black stem rust of wheat), *Ustilago* (smuts), *Phytophthora infestans* (late blight of potato — the 1845 Irish famine), *Albugo candida* (white rust of crucifers) |
| Human disease | ringworm and athlete's foot (*Trichophyton*), candidiasis (*Candida albicans*), aspergillosis |
| Toxins | *Amanita phalloides* (death cap) and ergot of rye (*Claviceps purpurea*) are deadly; aflatoxin from *Aspergillus flavus* contaminates stored maize and groundnut |

::: caution Never taste-test a wild mushroom
Every year Nepal records deaths from wild mushroom poisoning, because the edible
*Amanita* relatives and the lethal *Amanita phalloides* look alike to the
untrained eye, and no cooking destroys the amatoxins. In the examination, if you
are asked for poisonous fungi, *Amanita phalloides* and *Claviceps purpurea* are
the two safe answers.
:::

## 2.3 Lichen

A lichen is not one organism but two living as one: a fungus and a
photosynthetic partner in such intimate and permanent association that the
composite has its own shape, its own chemistry and its own scientific name. The
study of lichens is **lichenology**.

::: definition Lichen
A stable, self-supporting symbiotic association between a fungus (the
**mycobiont**, usually an Ascomycete) and a photosynthetic alga or cyanobacterium
(the **phycobiont** or photobiont, usually *Trebouxia* or *Nostoc*), forming a
thallus quite unlike either partner grown alone.
:::

The fungus contributes the body: it makes up 90–95 % of the thallus, absorbs and
retains water and mineral salts, and shelters the alga from drying and strong
light. The alga contributes the food, fixing carbon dioxide into sugars; if the
partner is a cyanobacterium it fixes atmospheric nitrogen as well. Because the
fungus takes more than it gives and can keep the alga on short rations, the
relationship is sometimes described as **helotism** (controlled parasitism)
rather than true mutualism.

```figure caption="The three growth forms of lichens -- crustose, foliose and fruticose -- and a vertical section of a heteromerous foliose thallus showing the algal zone sandwiched between fungal layers."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Ellipse, Circle, Rectangle

fig, (a, b) = plt.subplots(1, 2, figsize=(5.2, 2.5),
                           gridspec_kw={'width_ratios': [1.15, 1.0], 'wspace': 0.10})
rng = np.random.default_rng(11)

def lab(ax, s, xy, xytext, ha='left', fs=6.2):
    ax.annotate(s, xy=xy, xytext=xytext, ha=ha, va='center', fontsize=fs,
                color=INK, arrowprops=dict(arrowstyle='-', lw=0.6, color=MUTED,
                                           shrinkA=1, shrinkB=1))

# ---- (a) three growth forms -------------------------------------------
BASE = 0.60
# crustose: a thin crust fused to the surface of a rock
t = np.linspace(0, np.pi, 120)
rock = np.column_stack([1.00 + 0.92 * np.cos(t), BASE + 0.34 * np.sin(t)])
rock = np.vstack([rock, [[0.08, BASE], [1.92, BASE]]])
a.add_patch(Polygon(rock, closed=True, fc='#d7d3cc', ec=MUTED, lw=0.8))
tt = np.linspace(0.06, np.pi - 0.06, 120)
a.plot(1.00 + 0.92 * np.cos(tt), BASE + 0.015 + 0.34 * np.sin(tt),
       color='#6a7f4f', lw=2.4, solid_capstyle='round')
a.text(1.00, 0.30, 'crustose', ha='center', va='center', fontsize=6.3, color=INK)

# foliose: flat leafy lobes held on by rhizines
for cx, cy, w, h, ang in [(3.25, 0.86, 1.50, 0.34, 3),
                          (3.02, 1.06, 1.16, 0.30, -7),
                          (3.52, 1.16, 0.92, 0.26, 9)]:
    a.add_patch(Ellipse((cx, cy), w, h, angle=ang, fc='#9fb27a',
                        ec=INK, lw=0.8))
a.plot([2.42, 4.08], [BASE, BASE], color=MUTED, lw=1.0)
for rx in np.linspace(2.75, 3.80, 5):
    a.plot([rx, rx], [0.72, BASE], color='#8a7a5c', lw=0.7)
a.text(3.25, 0.30, 'foliose', ha='center', va='center', fontsize=6.3, color=INK)

# fruticose: shrubby and branched
def branch(x, y, ang, L, d):
    x2 = x + L * np.cos(ang)
    y2 = y + L * np.sin(ang)
    a.plot([x, x2], [y, y2], color='#7f8f5e', lw=max(0.7, 2.3 - 0.5 * d),
           solid_capstyle='round')
    if d < 3:
        branch(x2, y2, ang + 0.55, L * 0.72, d + 1)
        branch(x2, y2, ang - 0.50, L * 0.70, d + 1)

branch(5.55, BASE, np.pi / 2, 0.44, 0)
a.plot([4.85, 6.25], [BASE, BASE], color=MUTED, lw=1.0)
a.text(5.55, 0.30, 'fruticose', ha='center', va='center', fontsize=6.3, color=INK)
a.set_title('Growth forms of the thallus', fontsize=7.2, color=INK, pad=3)
a.set_xlim(-0.05, 7.05)
a.set_ylim(0.14, 1.98)

# ---- (b) V.S. of foliose thallus --------------------------------------
W = 4.6
b.add_patch(Rectangle((0.0, 3.05), W, 0.42, fc='#cdbb9a', ec=INK, lw=0.8))
b.add_patch(Rectangle((0.0, 2.35), W, 0.70, fc='#e7efdf', ec=INK, lw=0.8))
b.add_patch(Rectangle((0.0, 0.95), W, 1.40, fc='#f6f2e8', ec=INK, lw=0.8))
b.add_patch(Rectangle((0.0, 0.58), W, 0.37, fc='#cdbb9a', ec=INK, lw=0.8))
# dense hyphae in cortices
for y0 in (3.05, 0.58):
    for k in range(70):
        x = rng.uniform(0.05, W - 0.05)
        y = rng.uniform(y0 + 0.05, y0 + 0.32)
        ang = rng.uniform(0, np.pi)
        b.plot([x, x + 0.09 * np.cos(ang)], [y, y + 0.09 * np.sin(ang)],
               color='#8a7a5c', lw=0.6)
# algal cells
for k in range(26):
    x = rng.uniform(0.18, W - 0.18)
    y = rng.uniform(2.50, 2.92)
    b.add_patch(Circle((x, y), 0.085, fc='#4f8f4f', ec='#2f5f2f', lw=0.5))
# loose medulla
for k in range(70):
    x = rng.uniform(0.22, W - 0.22)
    y = rng.uniform(1.08, 2.22)
    ang = rng.uniform(0, 2 * np.pi)
    b.plot([x, x + 0.18 * np.cos(ang)], [y, y + 0.18 * np.sin(ang)],
           color='#b6a887', lw=0.6)
# rhizines
for x in np.linspace(0.45, W - 0.45, 6):
    b.plot([x, x - 0.05], [0.58, 0.20], color='#8a7a5c', lw=0.9)
    b.plot([x, x + 0.12], [0.58, 0.28], color='#8a7a5c', lw=0.7)
lab(b, 'upper cortex', (W - 0.3, 3.26), (W + 0.35, 3.40), fs=6.0)
lab(b, 'algal zone', (W - 0.3, 2.70), (W + 0.35, 2.78), fs=6.0)
lab(b, 'medulla\n(loose hyphae)', (W - 0.3, 1.65), (W + 0.35, 1.72), fs=6.0)
lab(b, 'lower cortex', (W - 0.3, 0.76), (W + 0.35, 0.86), fs=6.0)
lab(b, 'rhizine', (1.55, 0.32), (W + 0.35, 0.22), fs=6.0)
b.set_title('V.S. of a foliose thallus', fontsize=7.2, color=INK, pad=3)
b.set_xlim(-0.15, 7.30)
b.set_ylim(0.02, 3.80)

for ax in (a, b):
    ax.set_aspect('equal')
    ax.axis('off')
```

**Growth forms.** Three are recognised and are easy marks in a diagram question.
**Crustose** lichens form a thin crust fused to rock or bark and cannot be
removed intact (*Graphis*, *Lecanora*). **Foliose** lichens are leaf-like, lobed,
and attached loosely by root-like **rhizines** (*Parmelia*, *Peltigera*).
**Fruticose** lichens are shrubby or beard-like and hang free, attached at one
point only (*Cladonia*, *Usnea*, the "old man's beard" of hill oak forests).

**Internal structure.** A vertical section of a foliose thallus is stratified
into four layers: an **upper cortex** of compacted fungal hyphae; an **algal
zone** just beneath it, where the photobiont cells lie in the light; a loose
**medulla** of hyphae with air spaces, which stores water; and a **lower cortex**
from which the rhizines arise. Such a lichen is **heteromerous**. If the algal
cells are scattered throughout instead of forming a layer, the thallus is
**homoiomerous** (*Collema*).

**Reproduction.** Vegetative reproduction dominates, because both partners must
travel together: by **fragmentation** of the thallus; by **soredia**, minute
powdery outgrowths each containing a few algal cells wrapped in hyphae; and by
**isidia**, small firm coral-like projections of the upper surface. The fungus
alone reproduces sexually, forming an **apothecium** (a disc, as in *Parmelia*)
or a **perithecium** (a flask, as in *Graphis*) containing ascospores; a
germinating ascospore must find a suitable alga or die.

**Economic and ecological importance.** Lichens are the classic **pioneers of
xerophytic succession**: they colonise bare rock, secrete carbonic and oxalic
acids that etch the surface, and their dead thalli add the first humus, so that
mosses and then higher plants can follow. They are highly sensitive to **sulphur
dioxide** and are used worldwide as **bio-indicators of air pollution** — the
absence of *Usnea* from a valley is a measurement of its air. They are also used
as food (*Cetraria islandica*, Iceland moss; *Lecanora* as "manna"), as fodder
(reindeer moss, *Cladonia rangiferina*), in dyeing and in the manufacture of
**litmus** from *Roccella tinctoria*, in perfumery (*Evernia*, *Ramalina*, the
*jhyau* traded from the Nepali hills and used in garam masala), and in medicine —
**usnic acid** is a genuine antibiotic. Lichens accumulate radioisotopes and
heavy metals, which is why Chernobyl fallout concentrated in lichen-eating
reindeer.

## 2.4 Algae

Algae are simple, chlorophyll-bearing, thalloid plants with no true roots, stems,
leaves or vascular tissue, whose sex organs are **unicellular** and whose
zygote never develops into a multicellular embryo inside the female organ. Most
are aquatic. The study of algae is **phycology**, and the classification below is
that of **F. E. Fritsch (1935)**, which the NEB syllabus follows.

**Range of form.** Algae span almost every level of organisation below the true
plant: unicellular motile (*Chlamydomonas*), unicellular non-motile
(*Chlorella*), colonial (*Volvox*), filamentous unbranched (*Spirogyra*,
*Ulothrix*), filamentous branched (*Cladophora*), heterotrichous
(*Draparnaldia*), siphonaceous and multinucleate (*Vaucheria*), and finally
massive parenchymatous thalli up to 60 m long (*Macrocystis*, the giant kelp).

```figure caption="Two algae: a filament of *Spirogyra* with its spiral ribbon chloroplast and pyrenoids, and a single cell of *Chlamydomonas* with its cup-shaped chloroplast, eyespot and two apical flagella."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Ellipse, Polygon

fig, (a, b) = plt.subplots(1, 2, figsize=(5.2, 2.5),
                           gridspec_kw={'width_ratios': [1.45, 1.0], 'wspace': 0.08})

def lab(ax, s, xy, xytext, ha='left', fs=6.0):
    ax.annotate(s, xy=xy, xytext=xytext, ha=ha, va='center', fontsize=fs,
                color=INK, arrowprops=dict(arrowstyle='-', lw=0.6, color=MUTED,
                                           shrinkA=1, shrinkB=1))

# ---------------- (a) Spirogyra filament --------------------------------
Y0, Y1 = 0.75, 2.45
a.add_patch(FancyBboxPatch((-0.45, Y0), 4.05, Y1 - Y0,
                           boxstyle='round,pad=0,rounding_size=0.05',
                           fc='#fbfdfb', ec=INK, lw=1.1))
a.plot([-0.45, 3.60], [Y1 + 0.10, Y1 + 0.10], color=MUTED, lw=0.8, ls=(0, (2, 2)))
a.plot([-0.45, 3.60], [Y0 - 0.10, Y0 - 0.10], color=MUTED, lw=0.8, ls=(0, (2, 2)))
for sx in (0.25, 2.95):
    a.plot([sx, sx], [Y0, Y1], color=INK, lw=1.1)

YC = 0.5 * (Y0 + Y1)
xs = np.linspace(0.30, 2.90, 400)
yc = YC + 0.62 * np.sin(2 * np.pi * (xs - 0.30) / 1.30)
a.fill_between(xs, yc - 0.085, yc + 0.085, color='#3f8f4f', lw=0)
for px in (0.62, 1.28, 1.93, 2.58):
    py = YC + 0.62 * np.sin(2 * np.pi * (px - 0.30) / 1.30)
    a.add_patch(Circle((px, py), 0.085, fc='#d8ecd8', ec='#1f5f2f', lw=0.7))

a.add_patch(Circle((1.60, YC), 0.16, fc='#cfe3f3', ec=INK, lw=0.9))
for ang in np.linspace(0, 2 * np.pi, 9)[:-1]:
    a.plot([1.60 + 0.17 * np.cos(ang), 1.60 + 0.62 * np.cos(ang)],
           [YC + 0.17 * np.sin(ang), YC + 0.50 * np.sin(ang)],
           color=MUTED, lw=0.6)

lab(a, 'spiral (ribbon) chloroplast', (0.62, YC + 0.60), (-0.85, 3.12), ha='left')
lab(a, 'mucilage sheath', (2.40, Y1 + 0.10), (4.65, 3.12), ha='right')
lab(a, 'cell wall', (3.35, 2.20), (3.80, 2.62), ha='left')
lab(a, 'pyrenoid', (2.58, YC - 0.62), (3.80, 1.15), ha='left')
lab(a, 'septum', (2.95, 0.92), (3.80, 0.48), ha='left')
lab(a, 'nucleus', (1.60, YC), (0.95, 0.24), ha='center')
lab(a, 'cytoplasmic strand', (1.98, YC + 0.30), (2.58, 0.24), ha='center')
a.text(-0.95, -0.28, 'a   $Spirogyra$ - a filament of identical cells',
       ha='left', va='center', fontsize=6.2, color=MUTED)
a.set_xlim(-1.00, 4.80)
a.set_ylim(-0.48, 3.40)

# ---------------- (b) Chlamydomonas -------------------------------------
b.add_patch(Ellipse((0, 0), 1.44, 1.94, fc='#fbfdfb', ec=INK, lw=1.1))
th = np.linspace(np.deg2rad(155), np.deg2rad(385), 200)
outer = np.column_stack([0.66 * np.cos(th), 0.89 * np.sin(th)])
inner = np.column_stack([0.44 * np.cos(th), 0.62 * np.sin(th)])[::-1]
b.add_patch(Polygon(np.vstack([outer, inner]), closed=True,
                    fc='#4f9a5c', ec='#1f5f2f', lw=0.8))
b.add_patch(Circle((0.0, -0.50), 0.155, fc='#eef7ee', ec='#1f5f2f', lw=0.8))
b.add_patch(Circle((0.0, -0.50), 0.085, fc='#2f6f3f', ec='none'))
b.add_patch(Circle((0.0, 0.10), 0.195, fc='#cfe3f3', ec=INK, lw=0.9))
b.add_patch(Circle((0.0, 0.10), 0.075, fc='#7fb0d8', ec='none'))
for sx in (-0.21, 0.21):
    b.add_patch(Circle((sx, 0.70), 0.085, fc='#ffffff', ec=INK, lw=0.8))
b.add_patch(Ellipse((0.50, 0.14), 0.19, 0.11, angle=70,
                    fc='#e06b2a', ec='#a04a18', lw=0.6))
tf = np.linspace(0, 1, 120)
for sgn in (-1, 1):
    fx = sgn * (0.16 + 0.52 * tf) + sgn * 0.075 * np.sin(9 * tf)
    fy = 0.94 + 0.86 * tf
    b.plot(fx, fy, color=INK, lw=0.9)
lab(b, 'flagella (2)', (0.52, 1.55), (0.95, 1.80), ha='left')
lab(b, 'contractile\nvacuoles', (-0.21, 0.70), (-1.30, 1.45), ha='left')
lab(b, 'nucleus', (0.0, 0.10), (-1.30, 0.62), ha='left')
lab(b, 'cup-shaped\nchloroplast', (-0.56, -0.42), (-1.30, -0.30), ha='left')
lab(b, 'eyespot\n(stigma)', (0.56, 0.16), (0.90, 0.40), ha='left')
lab(b, 'pyrenoid', (0.10, -0.52), (0.90, -0.70), ha='left')
lab(b, 'cell wall', (0.60, -0.62), (0.90, -1.16), ha='left')
b.text(-1.45, -1.70, 'b   $Chlamydomonas$ - a motile unicell',
       ha='left', va='center', fontsize=6.2, color=MUTED)
b.set_xlim(-1.45, 2.05)
b.set_ylim(-1.92, 2.05)

for ax in (a, b):
    ax.set_aspect('equal')
    ax.axis('off')
```

*Spirogyra*, the commonest pond alga of Nepal and the standard laboratory
specimen, is an unbranched filament of cylindrical cells in a slippery mucilage
sheath — hence "pond silk". Each cell holds one to several **spiral ribbon
chloroplasts** studded with **pyrenoids** (protein-plus-starch bodies), a large
central vacuole and a nucleus suspended in the middle by cytoplasmic strands.
It grows by ordinary cell division, reproduces vegetatively by fragmentation, and
reproduces sexually by **conjugation**: two filaments lie side by side, papillae
grow out and meet to form a conjugation tube, and the whole protoplast of one
cell passes over and fuses with the other, giving a thick-walled **zygospore**
that germinates after the dry season. Conjugation is **scalariform** (ladder-like,
between two filaments) or **lateral** (between adjacent cells of one filament).
*Chlamydomonas* is the other required drawing: a single pear-shaped cell with two
equal apical **flagella**, one cup-shaped chloroplast with a pyrenoid, two
**contractile vacuoles**, a nucleus and a red **eyespot** (stigma) for
phototaxis.

| Class | Pigments | Reserve food | Wall | Flagella | Habitat | Examples |
|---|---|---|---|---|---|---|
| Chlorophyceae (green algae) | chlorophyll a, b | starch | cellulose | 2, equal, apical | mostly fresh water | *Chlamydomonas*, *Volvox*, *Spirogyra*, *Chara* |
| Xanthophyceae (yellow-green) | chlorophyll a, e; xanthophylls | oil, chrysolaminarin | cellulose and pectin | 2, unequal | fresh water, damp soil | *Vaucheria*, *Botrydium* |
| Bacillariophyceae (diatoms) | chlorophyll a, c; fucoxanthin | oil, chrysolaminarin | silica frustule | 1 in male gametes | fresh and marine | *Navicula*, *Pinnularia* |
| Phaeophyceae (brown algae) | chlorophyll a, c; **fucoxanthin** | **laminarin**, mannitol | cellulose and **algin** | 2, unequal, lateral | almost all marine | *Laminaria*, *Fucus*, *Sargassum*, *Macrocystis* |
| Rhodophyceae (red algae) | chlorophyll a, d; **r-phycoerythrin** | **floridean starch** | cellulose and pectin, often with agar | **absent** | mostly marine | *Polysiphonia*, *Gelidium*, *Gracilaria*, *Batrachospermum* |

::: memory Reserve food by colour
**Green stores starch, brown stores laminarin, red stores floridean starch.**
For pigments: the dominant accessory pigment gives the colour — **fucoxanthin**
makes brown algae brown, **phycoerythrin** makes red algae red. And only the red
algae are completely **flagella-free**, which is why their male gametes must
drift passively to the female.
:::

**Reproduction.** Vegetative reproduction is by fragmentation, hormogonia or
cell division. Asexual reproduction is by zoospores (motile, flagellate),
aplanospores (non-motile), hypnospores (thick-walled) or akinetes. Sexual
reproduction ranges through three grades of gamete: **isogamy** (both gametes
motile and alike, *Ulothrix*), **anisogamy** (both motile, one larger,
*Chlamydomonas braunii*) and **oogamy** (a large non-motile egg and a small
motile sperm, *Volvox*, *Fucus*), plus the special case of conjugation in
*Spirogyra*. This isogamy–anisogamy–oogamy series is one of the classic
evolutionary progressions in botany and is worth quoting whenever a question asks
about advancement in the algae.

| Field | Economic importance of algae |
|---|---|
| Oxygen and food chains | marine phytoplankton, mostly diatoms, produce a large share of the world's oxygen and start almost every aquatic food chain |
| Human food | *Porphyra* (nori), *Laminaria* (kombu), *Ulva*, *Sargassum*; *Chlorella* and *Spirulina* as single-cell protein |
| Agar | from the red algae *Gelidium* and *Gracilaria*; the standard culture medium of microbiology, also used in ice cream and jellies |
| Algin (alginic acid) | from brown algae; thickener in ice cream, paint, toothpaste and textile printing |
| Carrageenan | from *Chondrus crispus*; emulsifier in chocolate milk and cosmetics |
| Diatomite | fossil diatom frustules, used for filtration, insulation, polishing and as the absorbent in dynamite |
| Iodine and potash | extracted from kelps such as *Laminaria* |
| Fertiliser and fodder | seaweed manure, rich in potash; *Nostoc* and *Anabaena* fix nitrogen in rice fields |
| Harm | algal blooms and **eutrophication** deoxygenate water and kill fish; red tides (*Gonyaulax*) are toxic; *Cephaleuros* parasitises tea leaves |

## 2.5 Bryophyta

Bryophytes are the simplest land plants: green, embryo-forming, but with **no
vascular tissue** and **no true roots**. They are called the **amphibians of the
plant kingdom** because although they live on land, they cannot complete their
life cycle without water — the sperm must swim. They are also the group in which
**alternation of generations** first becomes obvious, with the gametophyte
dominant and the sporophyte permanently attached to and dependent on it. That
reversal — gametophyte big, sporophyte small — is unique to this division, and
almost every examination question on bryophytes turns on it.

**General characters.**

- The plant body is a **gametophyte (n)**: either a flat, dorsiventral **thallus**
  (*Riccia*, *Marchantia*) or an erect, leafy axis with spirally arranged leaves
  (*Funaria*, *Sphagnum*). There are no roots; anchorage and absorption are by
  unicellular or multicellular **rhizoids**.
- There is **no xylem or phloem**; water travels by capillarity over the surface
  and by diffusion, which is why bryophytes are small and confined to damp,
  shaded places.
- Sex organs are **multicellular and jacketed** — the male **antheridium**, a
  club-shaped body producing biflagellate antherozoids, and the female
  **archegonium**, a flask-shaped body with a neck and a swollen venter holding a
  single egg. The sterile jacket of cells is the advance on the algae.
- **Fertilisation requires external water.** Antherozoids swim down the
  mucilage-filled neck of the archegonium, attracted chemotactically by sucrose
  and potassium salts.
- The zygote divides *in situ* to form a multicellular **embryo**, which grows
  into the **sporophyte (2n)** — typically a **foot**, **seta** and **capsule** —
  that remains attached to the gametophyte and draws nutrition from it.
- Inside the capsule, **spore mother cells (2n)** undergo **meiosis** to give
  haploid **spores**. The spore germinates into a green filamentous
  **protonema**, which buds to produce the leafy plant, closing the cycle.

```figure caption="*Funaria hygrometrica*: the leafy gametophyte carrying the attached sporophyte, and the capsule enlarged to show the operculum, peristome teeth, theca and columella."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Ellipse, Circle, FancyBboxPatch

fig, (a, b) = plt.subplots(1, 2, figsize=(5.0, 3.6),
                           gridspec_kw={'width_ratios': [1.0, 1.05], 'wspace': 0.05})

def lab(ax, s, xy, xytext, ha='left', fs=6.1):
    ax.annotate(s, xy=xy, xytext=xytext, ha=ha, va='center', fontsize=fs,
                color=INK, arrowprops=dict(arrowstyle='-', lw=0.6, color=MUTED,
                                           shrinkA=1, shrinkB=1))

def leaf(ax, x0, y0, ang, L, W, fc='#7fae63'):
    t = np.linspace(0, 1, 40)
    d = np.array([np.cos(ang), np.sin(ang)])
    p = np.array([-d[1], d[0]])
    half = (W / 2) * np.sin(np.pi * t) ** 0.8
    base = np.array([x0, y0])
    up = base + np.outer(t * L, d) + np.outer(half, p)
    dn = (base + np.outer(t * L, d) - np.outer(half, p))[::-1]
    ax.add_patch(Polygon(np.vstack([up, dn]), closed=True, fc=fc, ec='#3f6b30', lw=0.7))
    ax.plot([x0, x0 + L * d[0]], [y0, y0 + L * d[1]], color='#3f6b30', lw=0.5)

# ---------------- (a) whole plant ---------------------------------------
AX = 0.0
a.plot([AX, AX], [0.0, 1.85], color='#6f8f55', lw=2.4, solid_capstyle='round')
for y, ang, L in [(0.30, 0.55, 0.62), (0.30, np.pi - 0.55, 0.62),
                  (0.62, 0.42, 0.72), (0.62, np.pi - 0.42, 0.72),
                  (0.98, 0.35, 0.80), (0.98, np.pi - 0.35, 0.80),
                  (1.34, 0.50, 0.70), (1.34, np.pi - 0.50, 0.70),
                  (1.66, 0.85, 0.52), (1.66, np.pi - 0.85, 0.52)]:
    leaf(a, AX, y, ang, L, 0.26)
for ang in (-2.5, -2.0, -1.55, -1.1, -0.65):
    a.plot([AX, AX + 0.55 * np.cos(ang)], [0.0, 0.55 * np.sin(ang)],
           color='#8a6b4a', lw=0.9)
    a.plot([AX + 0.55 * np.cos(ang), AX + 0.85 * np.cos(ang - 0.25)],
           [0.55 * np.sin(ang), 0.85 * np.sin(ang - 0.25)],
           color='#8a6b4a', lw=0.7)

# sporophyte: foot in the gametophyte apex, then seta and capsule
a.add_patch(Ellipse((AX, 1.88), 0.16, 0.22, fc='#c9a882', ec=INK, lw=0.8))
ts = np.linspace(0, 1, 120)
sx = AX + 0.30 * ts ** 2.6
sy = 1.95 + 1.55 * ts
a.plot(sx, sy, color='#a8763f', lw=1.8, solid_capstyle='round')
CX, CY = sx[-1] + 0.06, sy[-1] + 0.30
a.add_patch(Ellipse((CX, CY), 0.42, 0.62, angle=18, fc='#c07a3a', ec=INK, lw=0.9))
kal = np.array([[CX - 0.24, CY + 0.10], [CX - 0.16, CY + 0.50],
                [CX + 0.34, CY + 0.72], [CX + 0.20, CY + 0.28],
                [CX + 0.26, CY + 0.02]])
a.add_patch(Polygon(kal, closed=True, fc='#efe2cc', ec=INK, lw=0.8, alpha=0.95))
lab(a, 'calyptra', (CX + 0.18, CY + 0.52), (CX + 0.55, CY + 0.80), ha='left')
lab(a, 'capsule', (CX - 0.14, CY - 0.12), (CX + 0.55, CY - 0.18), ha='left')
lab(a, 'seta', (sx[60], sy[60]), (sx[60] + 0.60, sy[60]), ha='left')
lab(a, 'foot', (AX + 0.05, 1.88), (AX + 0.70, 1.80), ha='left')
lab(a, 'leaf', (AX + 0.62, 1.20), (AX + 0.95, 1.05), ha='left')
lab(a, 'axis (stem)', (AX, 0.46), (AX + 0.98, 0.30), ha='left')
lab(a, 'rhizoids', (AX - 0.40, -0.35), (AX - 0.70, -0.62), ha='right')
a.text(AX - 2.05, -1.18, 'a   the moss plant', ha='left', va='center',
       fontsize=6.4, color=MUTED)
a.plot([AX - 1.22, AX - 1.22], [0.0, 1.85], color=MUTED, lw=0.8)
a.text(AX - 1.30, 0.92, 'gametophyte (n)', rotation=90, ha='right',
       va='center', fontsize=6.1, color=MUTED)
a.plot([AX - 1.22, AX - 1.22], [1.95, 3.95], color='#a8763f', lw=0.8)
a.text(AX - 1.30, 2.95, 'sporophyte (2n)', rotation=90, ha='right',
       va='center', fontsize=6.1, color='#8a5f30')
a.set_xlim(-2.10, 1.95)
a.set_ylim(-1.35, 4.45)

# ---------------- (b) capsule, calyptra removed -------------------------
PX, PY = 0.0, 0.0
b.plot([PX, PX], [-1.35, -0.62], color='#a8763f', lw=2.6, solid_capstyle='round')
b.add_patch(Ellipse((PX, -0.48), 0.72, 0.42, fc='#b8703a', ec=INK, lw=1.0))
b.add_patch(Ellipse((PX, 0.22), 0.86, 1.18, fc='#c07a3a', ec=INK, lw=1.0))
b.add_patch(Ellipse((PX, 0.80), 0.72, 0.16, fc='#8a5424', ec=INK, lw=0.9))
b.add_patch(Ellipse((PX, 0.88), 0.62, 0.12, fc='#e6d3b4', ec=INK, lw=0.9))
th = np.linspace(0, np.pi, 80)
b.add_patch(Polygon(np.column_stack([PX + 0.40 * np.cos(th),
                                     0.93 + 0.34 * np.sin(th)]),
                    closed=True, fc='#d8b98a', ec=INK, lw=0.9))
b.plot([PX, PX], [1.27, 1.45], color=INK, lw=1.0)
for k in range(11):
    xk = PX - 0.28 + 0.056 * k
    b.plot([xk, xk], [0.80, 0.86], color='#f0e2c8', lw=0.6)
lab(b, 'operculum (lid)', (PX + 0.24, 1.10), (PX + 0.75, 1.42), ha='left')
lab(b, 'peristome teeth', (PX + 0.18, 0.84), (PX + 0.75, 0.96), ha='left')
lab(b, 'annulus', (PX + 0.34, 0.78), (PX + 0.75, 0.56), ha='left')
lab(b, 'theca\n(spore sac)', (PX + 0.40, 0.26), (PX + 0.75, 0.10), ha='left')
lab(b, 'columella', (PX, 0.22), (PX - 0.62, 0.62), ha='right')
lab(b, 'apophysis', (PX - 0.32, -0.48), (PX - 0.62, -0.30), ha='right')
lab(b, 'seta', (PX, -1.05), (PX - 0.62, -1.05), ha='right')
b.plot([PX, PX], [-0.30, 0.74], color='#8a5424', lw=1.0, ls=(0, (3, 2)))
b.text(-1.65, -1.75, 'b   the capsule, calyptra removed', ha='left',
       va='center', fontsize=6.4, color=MUTED)
b.set_xlim(-1.65, 2.30)
b.set_ylim(-1.95, 2.00)

for ax in (a, b):
    ax.set_aspect('equal')
    ax.axis('off')
```

*Funaria hygrometrica*, the cord moss, is the prescribed type. Its leafy shoot
bears antheridia in a terminal cluster surrounded by orange perigonial leaves
(the male "flower") and archegonia on a separate branch. After fertilisation the
sporophyte grows out as a long reddish **seta** carrying a pear-shaped
**capsule** capped by the **calyptra**, the torn-off remains of the archegonial
neck. The capsule itself is worth learning in detail: the sterile **apophysis**
at its base, the spore-bearing **theca** with its central sterile **columella**,
and at the top the **operculum** (lid) which falls away to expose a double ring
of hygroscopic **peristome teeth** that flex with humidity and flick the spores
out on dry days — the specific name *hygrometrica* records exactly this.

```figure caption="Alternation of generations in a moss. The gametophyte generation (green) is dominant; the sporophyte (brown) stays attached to it. Ploidy changes only at fertilisation and at meiosis."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

fig, ax = plt.subplots(figsize=(5.2, 2.8))
A, B = 2.78, 1.46
GREEN, BROWN = '#2f7f4f', '#a8763f'

nodes = [
    (90,  'spores (n)', GREEN),
    (45,  'protonema (n)', GREEN),
    (0,   'leafy gametophyte (n)\nantheridia + archegonia', GREEN),
    (-45, 'antherozoid (n)\n+ egg (n)', GREEN),
    (-90, 'zygote (2n)', BROWN),
    (-135, 'embryo (2n)', BROWN),
    (180, 'sporophyte (2n)\nfoot, seta, capsule', BROWN),
    (135, 'spore mother\ncells (2n)', BROWN),
]
pos = {}
for ang, s, c in nodes:
    r = np.deg2rad(ang)
    pos[ang] = (A * np.cos(r), B * np.sin(r))

order = [90, 45, 0, -45, -90, -135, 180, 135, 90]
for i in range(8):
    p, q = pos[order[i]], pos[order[i + 1]]
    col = GREEN if order[i] in (90, 45, 0, -45) else BROWN
    ax.add_patch(FancyArrowPatch(p, q, connectionstyle='arc3,rad=-0.18',
                                 arrowstyle='-|>', mutation_scale=9,
                                 lw=1.1, color=col, shrinkA=26, shrinkB=26))

for ang, s, c in nodes:
    x, y = pos[ang]
    ax.text(x, y, s, ha='center', va='center', fontsize=6.2, color=INK,
            linespacing=1.3,
            bbox=dict(boxstyle='round,pad=0.30', fc='#f6faf6' if c == GREEN
                      else '#fbf3e8', ec=c, lw=0.9))

ax.text(0.0, 0.30, 'ALTERNATION OF GENERATIONS', ha='center', va='center',
        fontsize=6.5, color=INK, fontweight='bold')
ax.text(0.0, 0.02, 'gametophyte dominant, free-living;\n'
        'sporophyte attached and dependent',
        ha='center', va='center', fontsize=5.8, color=MUTED, linespacing=1.35)
ax.text(1.45, -1.80, 'FERTILISATION   n + n → 2n', ha='center', va='center',
        fontsize=6.0, color='#b03030', fontweight='bold')
ax.text(-1.45, 1.80, 'MEIOSIS   2n → n', ha='center', va='center',
        fontsize=6.0, color='#b03030', fontweight='bold')
ax.text(3.30, 1.80, 'haploid (n)', ha='center', va='center', fontsize=6.2,
        color=GREEN, fontweight='bold')
ax.text(-3.30, -1.80, 'diploid (2n)', ha='center', va='center', fontsize=6.2,
        color=BROWN, fontweight='bold')
ax.set_xlim(-3.95, 3.95)
ax.set_ylim(-2.10, 2.10)
ax.axis('off')
```

| Class | Body | Sporophyte | Examples |
|---|---|---|---|
| Hepaticopsida (liverworts) | thalloid or leafy, dorsiventral; rhizoids unicellular | simple; often only foot and capsule, no true columella | *Riccia*, *Marchantia*, *Pellia* |
| Anthocerotopsida (hornworts) | simple thallus; one large chloroplast with a pyrenoid per cell | long horn-like capsule with stomata and columella, growing from a basal meristem | *Anthoceros*, *Notothylas* |
| Bryopsida (mosses) | leafy axis with spirally set leaves; rhizoids multicellular | foot, seta and capsule with operculum and peristome | *Funaria*, *Polytrichum*, *Sphagnum* |

::: example Worked example 2.2 — Ploidy through the life cycle
A moss has a haploid chromosome number of n = 14. State the chromosome number of
(i) a spore, (ii) the protonema, (iii) a leaf cell of the green plant,
(iv) an antherozoid, (v) the egg, (vi) the zygote, (vii) a cell of the seta,
(viii) a spore mother cell, and (ix) the spores it produces. Then find how many
spores 10 spore mother cells yield.

**Method.** Draw one line through the cycle and mark the only two events that
change ploidy: **fertilisation doubles** it, **meiosis halves** it. Everything
between those two events has the same number.

Fertilisation happens when egg meets antherozoid; meiosis happens in the spore
mother cells inside the capsule. So *everything from the spore up to the
gametes* is haploid, and *everything from the zygote to the spore mother cell*
is diploid.

| Stage | Ploidy | Chromosome number |
|---|---|---|
| (i) spore | n | 14 |
| (ii) protonema | n | 14 |
| (iii) leaf cell of the gametophyte | n | 14 |
| (iv) antherozoid | n | 14 |
| (v) egg | n | 14 |
| (vi) zygote | 2n | 28 |
| (vii) seta (part of the sporophyte) | 2n | 28 |
| (viii) spore mother cell | 2n | 28 |
| (ix) spores produced from it | n | 14 |

**Spore count.** Meiosis of one spore mother cell gives four spores, so

10 × 4 = **40 spores**.

Note the trap in (vii): the seta *looks* like part of the moss plant and is
attached to it, but it belongs to the sporophyte and is therefore diploid. The
same logic answers every ploidy question in this unit — including the fern, where
the answers come out the other way round because the *sporophyte* is the big
plant there.
:::

## 2.6 Pteridophyta

Pteridophytes are the **first vascular plants** — the first to possess xylem and
phloem — and the first in which the **sporophyte is the dominant, independent
generation**. They still reproduce by spores and still need water for
fertilisation, so they are called **vascular cryptogams**: cryptogams because
they are seedless and flowerless, vascular because they have conducting tissue.
In the Carboniferous they formed the forests whose remains are our coal.

**General characters.**

- The plant body is the **sporophyte (2n)**, differentiated into true **root**,
  **stem** and **leaf**. In *Dryopteris* the stem is an underground **rhizome**
  bearing **adventitious roots** below and large **pinnately compound fronds**
  above; young fronds show **circinate vernation**, unrolling from a coiled
  "crozier" or fiddlehead.
- **Vascular tissue** is present: xylem of **tracheids only** (no vessels, except
  in *Selaginella*, *Equisetum* and *Pteridium*) and phloem of **sieve cells**
  without companion cells. There is no cambium, so no secondary growth.
- **Sporangia** are borne on specialised leaves called **sporophylls**. In ferns
  they are grouped into **sori** on the underside of the frond, each sorus
  protected by a flap, the **indusium**, and each sporangium possessing a row of
  thick-walled cells, the **annulus**, which dries, springs back and catapults
  the spores out.
- Spores germinate into a small, green, independent **prothallus** — the
  **gametophyte (n)** — heart-shaped in *Dryopteris*, bearing rhizoids,
  **antheridia** among the rhizoids and **archegonia** near the notch.
- **Fertilisation needs water**; multiflagellate antherozoids swim to the egg.
  The zygote grows into a new sporophyte, which at first is parasitic on the
  prothallus and then becomes independent as the prothallus withers.

```figure caption="*Dryopteris*: the sporophyte with its rhizome, adventitious roots and circinate young frond; a vertical section of a sorus showing sporangia with the annulus, under the indusium; and the heart-shaped prothallus bearing antheridia and archegonia."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Ellipse, Circle, FancyBboxPatch, Rectangle

fig, (a, b, c) = plt.subplots(1, 3, figsize=(5.2, 2.9),
                              gridspec_kw={'width_ratios': [1.0, 1.05, 0.85],
                                           'wspace': 0.05})

def lab(ax, s, xy, xytext, ha='left', fs=6.0):
    ax.annotate(s, xy=xy, xytext=xytext, ha=ha, va='center', fontsize=fs,
                color=INK, arrowprops=dict(arrowstyle='-', lw=0.6, color=MUTED,
                                           shrinkA=1, shrinkB=1))

def leaf(ax, x0, y0, ang, L, W, fc='#5f9a4f', ec='#2f6b2f', lw=0.6):
    t = np.linspace(0, 1, 34)
    d = np.array([np.cos(ang), np.sin(ang)])
    p = np.array([-d[1], d[0]])
    half = (W / 2) * np.sin(np.pi * t) ** 0.75
    base = np.array([x0, y0])
    up = base + np.outer(t * L, d) + np.outer(half, p)
    dn = (base + np.outer(t * L, d) - np.outer(half, p))[::-1]
    ax.add_patch(Polygon(np.vstack([up, dn]), closed=True, fc=fc, ec=ec, lw=lw))

# ---------------- (a) sporophyte ----------------------------------------
a.add_patch(FancyBboxPatch((0.10, 0.72), 2.05, 0.30,
                           boxstyle='round,pad=0,rounding_size=0.15',
                           fc='#8a6b4a', ec=INK, lw=0.9))
for sx in np.linspace(0.30, 1.95, 7):
    a.plot([sx, sx + 0.10], [0.80, 0.94], color='#5f4530', lw=0.6)
for rx in np.linspace(0.30, 2.00, 6):
    tt = np.linspace(0, 1, 40)
    a.plot(rx + 0.16 * np.sin(4 * tt), 0.72 - 0.62 * tt, color='#8a6b4a', lw=0.8)

for fx in (0.62, 1.42):
    s = np.linspace(0, 1, 60)
    rx = fx + 0.42 * s ** 1.7
    ry = 1.02 + 1.72 * s
    a.plot(rx, ry, color='#4f7f3f', lw=1.4, solid_capstyle='round')
    for k in range(4, 55, 6):
        ang = np.arctan2(ry[k + 1] - ry[k], rx[k + 1] - rx[k])
        L = 0.46 * (1 - 0.72 * s[k])
        leaf(a, rx[k], ry[k], ang + 1.05, L, 0.17)
        leaf(a, rx[k], ry[k], ang - 1.05, L, 0.17)

th = np.linspace(0, 4.4 * np.pi, 220)
rr = 0.012 + 0.0135 * th
a.plot(2.28 + rr * np.cos(th + np.pi / 2) - 0.0,
       2.10 + rr * np.sin(th + np.pi / 2) + 0.0, color='#4f7f3f', lw=1.3)
a.plot([2.20, 2.28], [1.02, 2.10 - 0.02], color='#4f7f3f', lw=1.3)

lab(a, 'circinate\nyoung leaf', (2.36, 2.22), (2.66, 2.62), ha='left')
lab(a, 'pinna', (1.10, 2.02), (0.30, 2.62), ha='left')
lab(a, 'rachis', (1.72, 2.18), (2.66, 1.92), ha='left')
lab(a, 'rhizome', (1.20, 0.87), (2.66, 1.08), ha='left')
lab(a, 'adventitious\nroots', (1.32, 0.30), (2.66, 0.32), ha='left')
a.text(-0.10, -0.42, 'a   sporophyte of $Dryopteris$', ha='left',
       va='center', fontsize=6.2, color=MUTED)
a.set_xlim(-0.20, 4.10)
a.set_ylim(-0.62, 3.00)

# ---------------- (b) V.S. of a sorus -----------------------------------
LAMY = 2.85
b.add_patch(Rectangle((0.08, LAMY), 1.95, 0.15, fc='#7fae63', ec='#2f6b2f', lw=0.8))
b.add_patch(Ellipse((1.05, LAMY + 0.075), 0.26, 0.12, fc='#d8c8a8', ec=INK, lw=0.7))
b.add_patch(Ellipse((1.05, LAMY - 0.06), 0.30, 0.20, fc='#c9a882', ec=INK, lw=0.8))
ti = np.linspace(-1.0, 1.0, 120)
b.plot(1.05 + 0.92 * ti, LAMY - 0.12 - 0.52 * ti ** 2, color=INK, lw=1.2)
for sx, sy in [(0.38, 1.84), (0.74, 1.34), (1.36, 1.34), (1.72, 1.84)]:
    b.plot([1.05, sx], [LAMY - 0.16, sy + 0.24], color='#8a6b4a', lw=0.8)
    b.add_patch(Ellipse((sx, sy), 0.38, 0.46, fc='#f2e6cc', ec=INK, lw=0.8))
    for u in np.linspace(-0.35, 3.45, 12):
        b.add_patch(Rectangle((sx + 0.175 * np.cos(u) - 0.042,
                               sy + 0.212 * np.sin(u) - 0.042),
                              0.085, 0.085, angle=np.degrees(u),
                              fc='#b07a3a', ec=INK, lw=0.4))
    for jx in range(4):
        b.plot([sx - 0.075 + 0.05 * jx], [sy - 0.03], marker='o', ms=1.4,
               color='#6f5a3a')
lab(b, 'lamina', (0.30, LAMY + 0.08), (2.30, 3.22), ha='left')
lab(b, 'vein', (1.05, LAMY + 0.08), (2.30, 2.94), ha='left')
lab(b, 'placenta', (1.05, LAMY - 0.06), (2.30, 2.66), ha='left')
lab(b, 'indusium', (1.80, LAMY - 0.50), (2.30, 2.32), ha='left')
lab(b, 'sporangium', (1.72, 1.98), (2.30, 1.98), ha='left')
lab(b, 'annulus', (1.94, 1.76), (2.30, 1.52), ha='left')
lab(b, 'spores', (1.36, 1.31), (2.30, 1.02), ha='left')
b.text(-0.15, 0.50, 'b   V.S. of a sorus', ha='left', va='center',
       fontsize=6.2, color=MUTED)
b.set_xlim(-0.20, 3.35)
b.set_ylim(0.32, 3.52)

# ---------------- (c) prothallus ----------------------------------------
t = np.linspace(0, 2 * np.pi, 400)
hx = 16 * np.sin(t) ** 3
hy = (13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t))
hx, hy = 0.072 * hx, 0.072 * hy
c.add_patch(Polygon(np.column_stack([hx, hy]), closed=True,
                    fc='#8fbf72', ec='#2f6b2f', lw=1.0))
for u in np.linspace(np.pi - 0.95, np.pi + 0.95, 9):
    px = 0.072 * 16 * np.sin(u) ** 3
    py = 0.072 * (13 * np.cos(u) - 5 * np.cos(2 * u)
                  - 2 * np.cos(3 * u) - np.cos(4 * u))
    vx, vy = px - 0.0, py - 0.15
    n = np.hypot(vx, vy)
    c.plot([px, px + 0.30 * vx / n], [py, py + 0.30 * vy / n],
           color='#8a6b4a', lw=0.8)
# archegonia near the apical notch
for dx in (-0.16, 0.16):
    c.add_patch(Circle((dx, 0.62), 0.085, fc='#f2f7ef', ec='#2f6b2f', lw=0.7))
    c.plot([dx, dx + 0.5 * dx], [0.70, 0.90], color='#2f6b2f', lw=1.0)
# antheridia among the rhizoids
for dx, dy in [(-0.44, -0.42), (-0.16, -0.62), (0.18, -0.60), (0.46, -0.40)]:
    c.add_patch(Circle((dx, dy), 0.075, fc='#ffffff', ec='#2f6b2f', lw=0.7))
lab(c, 'apical notch', (0.0, 0.40), (0.66, 1.26), ha='left')
lab(c, 'archegonium\n(flask-shaped)', (0.16, 0.62), (0.86, 0.66), ha='left')
lab(c, 'antheridium', (0.46, -0.40), (0.86, -0.22), ha='left')
lab(c, 'rhizoids', (0.28, -1.18), (0.74, -1.30), ha='left')
c.text(-1.40, -1.86, 'c   prothallus (gametophyte),\n      ventral view',
       ha='left', va='center', fontsize=6.2, color=MUTED, linespacing=1.4)
c.set_xlim(-1.45, 2.40)
c.set_ylim(-2.12, 1.55)

for ax in (a, b, c):
    ax.set_aspect('equal')
    ax.axis('off')
```

**Homospory and heterospory.** Most pteridophytes are **homosporous**: they
produce one kind of spore, which gives a bisexual prothallus. A few are
**heterosporous**, producing large **megaspores** that give a female gametophyte
and small **microspores** that give a male gametophyte — *Selaginella*,
*Salvinia*, *Marsilea* and *Isoetes*. Heterospory matters far beyond this unit,
because it is the evolutionary threshold to the seed: in *Selaginella* the
megaspore is already retained on the parent plant, and the seed habit of
gymnosperms is the next step.

```figure caption="Alternation of generations in a fern. Compare with the moss: here the sporophyte (brown) is the large independent plant and the gametophyte (green) is a short-lived prothallus."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

fig, ax = plt.subplots(figsize=(5.2, 2.8))
A, B = 2.78, 1.46
GREEN, BROWN = '#2f7f4f', '#a8763f'

nodes = [
    (90,   'spores (n)', GREEN),
    (45,   'prothallus (n)\nthe gametophyte', GREEN),
    (0,    'antheridia + archegonia\non the prothallus (n)', GREEN),
    (-45,  'antherozoid (n)\n+ egg (n)', GREEN),
    (-90,  'zygote (2n)', BROWN),
    (-135, 'embryo (2n)', BROWN),
    (180,  'fern plant (2n)\nthe sporophyte', BROWN),
    (135,  'spore mother\ncells in sporangia', BROWN),
]
pos = {}
for ang, s, col in nodes:
    r = np.deg2rad(ang)
    pos[ang] = (A * np.cos(r), B * np.sin(r))

order = [90, 45, 0, -45, -90, -135, 180, 135, 90]
for i in range(8):
    p, q = pos[order[i]], pos[order[i + 1]]
    col = GREEN if order[i] in (90, 45, 0, -45) else BROWN
    ax.add_patch(FancyArrowPatch(p, q, connectionstyle='arc3,rad=-0.18',
                                 arrowstyle='-|>', mutation_scale=9,
                                 lw=1.1, color=col, shrinkA=26, shrinkB=26))

for ang, s, col in nodes:
    x, y = pos[ang]
    ax.text(x, y, s, ha='center', va='center', fontsize=6.0, color=INK,
            linespacing=1.3,
            bbox=dict(boxstyle='round,pad=0.30',
                      fc='#f6faf6' if col == GREEN else '#fbf3e8',
                      ec=col, lw=0.9))

ax.text(0.0, 0.30, 'ALTERNATION OF GENERATIONS', ha='center', va='center',
        fontsize=6.5, color=INK, fontweight='bold')
ax.text(0.0, 0.02, 'sporophyte dominant, long-lived;\n'
        'gametophyte small but independent',
        ha='center', va='center', fontsize=5.8, color=MUTED, linespacing=1.35)
ax.text(1.45, -1.80, 'FERTILISATION   n + n → 2n', ha='center', va='center',
        fontsize=6.0, color='#b03030', fontweight='bold')
ax.text(-1.45, 1.80, 'MEIOSIS   2n → n', ha='center', va='center',
        fontsize=6.0, color='#b03030', fontweight='bold')
ax.text(3.30, 1.80, 'haploid (n)', ha='center', va='center', fontsize=6.2,
        color=GREEN, fontweight='bold')
ax.text(-3.30, -1.80, 'diploid (2n)', ha='center', va='center', fontsize=6.2,
        color=BROWN, fontweight='bold')
ax.set_xlim(-3.95, 3.95)
ax.set_ylim(-2.10, 2.10)
ax.axis('off')
```

| Class | Stem | Leaves | Spores | Examples |
|---|---|---|---|---|
| Psilopsida | dichotomously branched, rootless | absent or minute scales | homosporous | *Psilotum*, *Rhynia* (fossil) |
| Lycopsida | herbaceous or arborescent | small, simple **microphylls** | homo- or heterosporous | *Lycopodium*, *Selaginella* |
| Sphenopsida | jointed, ribbed, silica-rich | small, whorled, scale-like | homosporous | *Equisetum* (horsetail) |
| Pteropsida | rhizome or erect trunk | large, pinnate **megaphylls** (fronds) | mostly homosporous | *Dryopteris*, *Pteris*, *Adiantum*, *Marsilea*, *Cyathea* |

| Character | Bryophyta | Pteridophyta |
|---|---|---|
| Dominant generation | gametophyte (n) | sporophyte (2n) |
| Plant body | thallus or leafy axis, no true organs | true root, stem and leaf |
| Vascular tissue | absent | present (xylem and phloem) |
| Roots | absent; rhizoids only | true roots present |
| Sporophyte | attached and dependent on gametophyte | independent and free-living |
| Gametophyte | large, long-lived, green | small, short-lived prothallus |
| Water for fertilisation | essential | essential |
| Examples | *Riccia*, *Marchantia*, *Funaria* | *Selaginella*, *Equisetum*, *Dryopteris* |

**Economic importance.** Young fronds of *Diplazium esculentum* (**niuro**) are a
familiar Nepali vegetable, and the rhizome starch of *Marsilea* and *Cyathea* is
eaten in times of scarcity. *Azolla*, a tiny floating fern, harbours the
nitrogen-fixing cyanobacterium *Anabaena azollae* in its leaf cavities and is
used as a **biofertiliser** in rice paddies. *Dryopteris* yields the vermifuge
filicin; *Lycopodium* spores are used as a dusting powder and in fireworks;
*Equisetum* was once used as a scouring rush because of its silica; tree ferns
(*Cyathea*) and *Adiantum* (maidenhair) are grown as ornamentals; and the
coal we burn is the fossilised remains of Carboniferous lycopods and horsetails.

## 2.7 Gymnosperm

Gymnosperms are seed plants in which the ovule sits **naked** on the surface of
an open **megasporophyll**, with no ovary wall around it — Greek *gymnos*, naked,
*sperma*, seed. Because there is no ovary there can be no fruit, and because
there is no flower in the angiosperm sense the reproductive structures are
cones (**strobili**). They are the plants of cold and dry places, and in Nepal
they form the great conifer belts of the temperate and subalpine zones.

**General characters.**

- Mostly evergreen woody **trees or shrubs**, never herbs; often with a distinct
  **tap root** bearing **mycorrhiza** (*Pinus*) or **coralloid roots** with
  cyanobacteria (*Cycas*).
- The stem is usually branched, and in *Pinus* is dimorphic: unlimited **long
  shoots** bearing scale leaves, and limited **dwarf shoots** (spurs) each
  carrying a **fascicle** of needle leaves.
- **Leaves** are of two kinds — green needles adapted to drought (thick cuticle,
  **sunken stomata**, hypodermis of sclerenchyma) and brown scale leaves.
- **Xylem has tracheids but no vessels**, and **phloem has sieve cells but no
  companion cells** (the exception is the order Gnetales, which does have
  vessels). Secondary growth is present and produces the timber.
- They are **heterosporous**, with microspores (pollen) in **male cones** and
  megaspores in ovules on the scales of **female cones**. In *Pinus* the male
  cones are small and clustered at the base of long shoots; the female cones are
  large, woody and take two to three years to mature.
- **Pollination is by wind (anemophily)** and is **direct**: the pollen grain,
  usually with two air bladders, is carried straight to the micropyle of the
  ovule, not to a stigma.
- The **female gametophyte forms endosperm before fertilisation**, and it is
  therefore **haploid (n)** — the single most examined difference from
  angiosperms, where a triploid endosperm forms only after double fertilisation.
- **Polyembryony** is common — several embryos begin in one seed, though usually
  only one survives. The seed is naked on the cone scale and often winged for
  dispersal. **Double fertilisation and fruit formation do not occur.**

```figure caption="*Pinus*: a long shoot bearing dwarf shoots with fascicles of needles, the male and female cones, and a winged seed lying naked on a cone scale."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Ellipse, Circle, FancyBboxPatch

fig, (a, b, c) = plt.subplots(1, 3, figsize=(5.2, 2.8),
                              gridspec_kw={'width_ratios': [1.0, 1.0, 0.72],
                                           'wspace': 0.05})

def lab(ax, s, xy, xytext, ha='left', fs=6.0):
    ax.annotate(s, xy=xy, xytext=xytext, ha=ha, va='center', fontsize=fs,
                color=INK, arrowprops=dict(arrowstyle='-', lw=0.6, color=MUTED,
                                           shrinkA=1, shrinkB=1))

# ---------------- (a) branch with dwarf shoots --------------------------
a.plot([1.00, 1.00], [0.10, 2.85], color='#8a6b4a', lw=3.0,
       solid_capstyle='round')
for y, sgn in [(0.55, -1), (0.95, 1), (1.35, -1), (1.75, 1), (2.15, -1),
               (2.50, 1)]:
    bx = 1.00 + sgn * 0.14
    a.add_patch(Ellipse((bx, y), 0.20, 0.13, angle=sgn * 18,
                        fc='#a8763f', ec=INK, lw=0.7))
    for k, dth in enumerate((-0.30, 0.0, 0.30)):
        ang = (0.95 if sgn > 0 else np.pi - 0.95) + dth
        a.plot([bx, bx + 0.86 * np.cos(ang)], [y, y + 0.86 * np.sin(ang)],
               color='#2f6b3f', lw=0.9, solid_capstyle='round')
for y in (0.35, 0.75, 1.15, 1.55, 1.95):
    a.plot([0.94, 0.82], [y, y + 0.10], color='#6f5230', lw=0.8)
lab(a, 'needles in a\nfascicle (3)', (1.72, 2.86), (0.05, 3.28), ha='left')
lab(a, 'dwarf shoot\n(spur)', (1.14, 1.75), (2.20, 2.10), ha='left')
lab(a, 'long shoot', (1.00, 0.95), (2.20, 0.90), ha='left')
lab(a, 'scale leaf', (0.86, 1.60), (-0.25, 1.30), ha='right')
a.text(-0.35, -0.35, 'a   branch', ha='left', va='center',
       fontsize=6.2, color=MUTED)
a.set_xlim(-0.40, 3.40)
a.set_ylim(-0.55, 3.55)

# ---------------- (b) male and female cones -----------------------------
b.plot([0.75, 0.75], [0.25, 1.35], color='#8a6b4a', lw=2.2)
for y, sgn in [(0.60, -1), (0.85, 1), (1.10, -1), (1.30, 1)]:
    b.add_patch(Ellipse((0.75 + sgn * 0.30, y + 0.10), 0.46, 0.26,
                        angle=sgn * 28, fc='#e0c56a', ec=INK, lw=0.8))
    for u in (-0.12, 0.0, 0.12):
        b.plot([0.75 + sgn * (0.18 + u), 0.75 + sgn * (0.42 + u)],
               [y + 0.10 + sgn * u * 1.6 + 0.09, y + 0.10 + sgn * u * 1.6 - 0.04],
               color='#a8883a', lw=0.5)

t = np.linspace(0, 2 * np.pi, 300)
CX, CY = 2.55, 1.35
ox, oy = CX + 0.58 * np.sin(t), CY + 1.00 * np.cos(t) - 0.10 * np.cos(2 * t)
b.add_patch(Polygon(np.column_stack([ox, oy]), closed=True,
                    fc='#a8763f', ec=INK, lw=1.0))
for row, yy in enumerate(np.linspace(CY - 0.82, CY + 0.80, 8)):
    hw = 0.58 * np.sqrt(max(0.04, 1 - ((yy - CY) / 1.02) ** 2))
    xs = np.linspace(-hw, hw, 60)
    b.plot(CX + xs, yy - 0.10 * (1 - (xs / max(hw, 1e-3)) ** 2),
           color='#5f4530', lw=0.7)
    for j in (-0.5, 0.5):
        if abs(j * hw) < hw:
            b.plot([CX + j * hw, CX + j * hw], [yy - 0.06, yy + 0.14],
                   color='#5f4530', lw=0.6)
b.plot([CX, CX], [CY - 1.05, CY - 1.45], color='#8a6b4a', lw=2.0)
lab(b, 'male cones\n(microsporangiate)', (0.48, 1.15), (-1.15, 2.25), ha='left')
lab(b, 'female cone\n(megasporangiate)', (CX + 0.50, CY + 0.55),
    (CX + 0.72, CY + 1.05), ha='left')
lab(b, 'cone scale', (CX + 0.30, CY - 0.30), (CX + 0.72, CY - 0.60), ha='left')
b.text(-1.50, -0.55, 'b   cones', ha='left', va='center',
       fontsize=6.2, color=MUTED)
b.set_xlim(-1.55, 4.55)
b.set_ylim(-0.80, 3.05)

# ---------------- (c) winged seed ---------------------------------------
c.add_patch(Ellipse((0.58, 0.62), 1.95, 0.62, angle=52,
                    fc='#efe2c8', ec=INK, lw=0.8))
c.add_patch(Ellipse((-0.05, -0.28), 0.50, 0.66, angle=-38,
                    fc='#8a6b4a', ec=INK, lw=0.9))
lab(c, 'membranous\nwing', (0.92, 1.12), (0.40, 1.82), ha='left')
lab(c, 'seed', (-0.05, -0.30), (0.52, -0.78), ha='left')
c.text(-1.00, -1.32, 'c   winged seed', ha='left', va='center',
       fontsize=6.2, color=MUTED)
c.set_xlim(-1.05, 2.45)
c.set_ylim(-1.55, 2.10)

for ax in (a, b, c):
    ax.set_aspect('equal')
    ax.axis('off')
```

| Character | Gymnosperm | Angiosperm |
|---|---|---|
| Ovule | naked, on an open megasporophyll | enclosed in an ovary |
| Reproductive structure | cone (strobilus) | flower |
| Fruit | absent | present, from the ovary wall |
| Xylem vessels | absent (except Gnetales) | present |
| Phloem companion cells | absent | present |
| Pollination | wind, direct to the micropyle | wind, insect, bird, water; on to a stigma |
| Fertilisation | single | **double** |
| Endosperm | haploid, formed **before** fertilisation | triploid, formed **after** fertilisation |
| Polyembryony | common | rare |
| Habit | woody trees and shrubs only | herbs, shrubs, trees, climbers |
| Number of living species | about 1,000 | about 250,000 |

**Gymnosperms of Nepal, and their uses.** *Pinus roxburghii* (khote salla, the
chir pine, three needles per fascicle) covers the drier hills from 800 to
2,000 m and yields resin, turpentine and rosin; *Pinus wallichiana* (gobre
salla, blue pine, five needles) takes over higher up. *Abies*, *Picea*,
*Tsuga*, *Cedrus deodara* and *Juniperus* (dhupi, burned as incense) build the
subalpine forests. *Taxus wallichiana*, the Himalayan yew (loth salla), is the
source of **taxol (paclitaxel)**, an anticancer drug, and is now a protected
species because of over-harvesting. *Ephedra gerardiana* yields **ephedrine**,
used for asthma. *Cycas* is grown ornamentally and its pith gives sago, and
*Ginkgo biloba*, a living fossil, is a well-known memory tonic. Beyond these,
conifers supply the world's **softwood timber, plywood, resin, and the pulp for
most of its paper**.

## 2.8 Angiosperm

Angiosperms are the flowering plants: seed plants in which the ovules are
enclosed in an **ovary**, which after fertilisation ripens into a **fruit**
(Greek *angeion*, a vessel). They are the dominant vegetation of the modern
world, about 250,000 species, and they include almost every plant we eat. Three
features explain their success: the **flower**, which makes precise animal
pollination possible; **double fertilisation**, which provides the embryo with a
triploid food tissue only when it is actually needed; and the **fruit**, which
protects and disperses the seed. This section takes sixteen of the thirty hours
of the unit, and the four families at the end of it are the most dependable long
question in the Botany paper.

### Morphology

Morphology is the study of external form. A typical angiosperm has an underground
**root system** and an aerial **shoot system** of stem, leaves, flowers and
fruits. The great value of morphology in this unit is that **modifications** are
the evidence for adaptation, and examiners ask for them by name.

**Root.** The primary root of a dicot persists as a **tap root** with lateral
branches; in monocots it dies and is replaced by a cluster of **fibrous
adventitious roots**. Roots are modified for **storage** (fusiform in radish,
conical in carrot, napiform in turnip, tuberous in sweet potato), for
**support** (prop roots of banyan, stilt roots of maize and sugarcane, clinging
roots of betel), for **respiration** (pneumatophores of *Rhizophora*), for
**assimilation** (*Tinospora*), for **parasitism** (haustoria of *Cuscuta*), and
for **symbiosis** (nodulated roots of legumes, mycorrhizal roots of pine).

**Stem.** The stem bears **nodes** and **internodes** with **axillary buds** —
the test that distinguishes a stem from a root. Underground modifications store
food and survive the dry season: **rhizome** (ginger, turmeric), **tuber**
(potato, with "eyes" that are axillary buds), **bulb** (onion, garlic) and
**corm** (*Colocasia*, *Crocus*). Sub-aerial modifications propagate the plant:
**runner** (grass, *Oxalis*), **stolon** (strawberry), **sucker** (mint,
chrysanthemum) and **offset** (water hyacinth). Aerial modifications include
stem **tendrils** (grapevine, *Passiflora*), stem **thorns** (*Bougainvillea*,
*Citrus*), **phylloclades** (*Opuntia*, *Euphorbia* — flattened green stems doing
the work of leaves) and **bulbils** (*Dioscorea*, *Agave*).

**Leaf.** A leaf has a **leaf base**, **petiole** and **lamina**. Venation is
**reticulate** in dicots and **parallel** in monocots. A **simple** leaf has an
undivided lamina; a **compound** leaf is cut right down to the midrib or petiole
and is **pinnately** compound (neem, *Cassia*) or **palmately** compound (silk
cotton, *Trifolium*). Phyllotaxy is **alternate** (mustard), **opposite**
(*Calotropis*) or **whorled** (*Nerium*). Leaves are modified into **tendrils**
(pea, where the upper leaflets become tendrils), **spines** (*Opuntia*,
*Argemone*), **storage organs** (onion scales), **pitchers** (*Nepenthes*) and
**phyllodes** (*Australian acacia*).

```figure caption="Longitudinal section of a typical hypogynous flower, showing the four whorls -- calyx, corolla, androecium and gynoecium -- on the receptacle, with ovules on an axile placenta."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Ellipse, Circle, FancyBboxPatch

fig, ax = plt.subplots(figsize=(5.0, 3.2))

def lab(s, xy, xytext, ha='left', fs=6.3):
    ax.annotate(s, xy=xy, xytext=xytext, ha=ha, va='center', fontsize=fs,
                color=INK, arrowprops=dict(arrowstyle='-', lw=0.6, color=MUTED,
                                           shrinkA=1, shrinkB=1))

def blade(x0, y0, ang, L, W, fc, ec, curve=0.0):
    t = np.linspace(0, 1, 60)
    d = np.array([np.cos(ang), np.sin(ang)])
    p = np.array([-d[1], d[0]])
    half = (W / 2) * np.sin(np.pi * t) ** 0.7
    axis = np.array([x0, y0]) + np.outer(t * L, d) + np.outer(curve * t ** 2, p)
    up = axis + np.outer(half, p)
    dn = (axis - np.outer(half, p))[::-1]
    ax.add_patch(Polygon(np.vstack([up, dn]), closed=True, fc=fc, ec=ec, lw=0.8))

# pedicel and receptacle
ax.plot([0.0, 0.0], [-1.40, -0.36], color='#5f8f4f', lw=3.0, solid_capstyle='round')
ax.add_patch(Ellipse((0.0, -0.22), 1.10, 0.46, fc='#9fc27f', ec='#3f6b30', lw=0.9))

# sepals
blade(-0.42, -0.24, np.deg2rad(150), 1.15, 0.36, '#6f9f57', '#3f6b30', curve=0.16)
blade(0.42, -0.24, np.deg2rad(30), 1.15, 0.36, '#6f9f57', '#3f6b30', curve=-0.16)
# petals
blade(-0.34, -0.08, np.deg2rad(122), 1.85, 0.62, '#e8b7cf', '#a85f83', curve=0.34)
blade(0.34, -0.08, np.deg2rad(58), 1.85, 0.62, '#e8b7cf', '#a85f83', curve=-0.34)

# stamens
for sgn in (-1, 1):
    s = np.linspace(0, 1, 60)
    fx = sgn * (0.20 + 0.52 * s ** 1.4)
    fy = -0.06 + 1.42 * s
    ax.plot(fx, fy, color='#c9a24a', lw=1.2)
    ax.add_patch(Ellipse((fx[-1], fy[-1] + 0.16), 0.20, 0.38,
                         angle=sgn * 14, fc='#e0c14a', ec=INK, lw=0.8))
    ax.plot([fx[-1] - sgn * 0.035, fx[-1] - sgn * 0.035],
            [fy[-1] + 0.02, fy[-1] + 0.30], color='#8a6b2a', lw=0.5)

# gynoecium: ovary, style, stigma
ax.add_patch(Ellipse((0.0, 0.38), 0.86, 1.02, fc='#cfe3c5', ec='#2f6b2f', lw=1.0))
ax.add_patch(Ellipse((0.0, 0.38), 0.56, 0.72, fc='#f2f8ef', ec='#2f6b2f', lw=0.7))
for oy in (0.62, 0.14):
    for ox in (-0.18, 0.18):
        ax.add_patch(Circle((ox, oy), 0.115, fc='#f7e6a8', ec='#8a6b2a', lw=0.7))
        ax.plot([0.0, ox * 0.55], [0.38, oy], color='#8a6b2a', lw=0.6)
ax.plot([0.0, 0.0], [0.89, 1.72], color='#5f8f4f', lw=1.6)
ax.add_patch(Ellipse((0.0, 1.85), 0.40, 0.20, fc='#b0864f', ec=INK, lw=0.8))
for k in range(9):
    u = -0.17 + 0.042 * k
    ax.plot([u, u * 1.15], [1.92, 2.02], color='#8a6b2a', lw=0.6)

lab('stigma', (0.18, 1.90), (0.80, 2.16), ha='left')
lab('style', (-0.02, 1.32), (-1.55, 1.66), ha='right')
lab('anther', (0.78, 1.52), (1.55, 1.14), ha='left')
lab('filament', (0.50, 0.60), (1.55, 0.62), ha='left')
lab('petal (corolla)', (1.14, 0.92), (1.55, 2.24), ha='left')
lab('sepal (calyx)', (0.90, 0.28), (1.55, -0.20), ha='left')
lab('receptacle\n(thalamus)', (0.40, -0.30), (1.55, -0.76), ha='left')
lab('pedicel', (0.0, -1.15), (0.36, -1.42), ha='left')
lab('ovary wall', (-0.42, 0.50), (-1.55, 1.10), ha='right')
lab('ovule', (-0.18, 0.62), (-1.55, 0.58), ha='right')
lab('placenta', (-0.10, 0.36), (-1.55, 0.06), ha='right')
lab('ovary', (-0.36, 0.02), (-1.55, -0.46), ha='right')

ax.text(-0.60, 2.66, 'androecium = all the stamens      gynoecium = all the carpels',
        ha='center', va='center', fontsize=6.0, color=MUTED)
ax.set_xlim(-3.20, 3.20)
ax.set_ylim(-1.75, 2.85)
ax.set_aspect('equal')
ax.axis('off')
```

**Inflorescence.** The arrangement of flowers on the floral axis. In a
**racemose** inflorescence the main axis keeps growing and the oldest flowers are
at the base — raceme (radish), spike (*Achyranthes*), catkin (mulberry), spadix
(*Colocasia*), corymb (candytuft), umbel (coriander) and **capitulum** or head
(sunflower, marigold), where many tiny sessile florets sit on a flat receptacle
and mimic one flower. In a **cymose** inflorescence the main axis ends in a
flower, so the oldest flower is at the top — uniparous or **helicoid**
(*Heliotropium*), biparous or **dichasial** (jasmine), and multiparous
(*Calotropis*). **Special types** include the verticillaster (*Ocimum*),
cyathium (*Euphorbia*) and hypanthodium (fig, *Ficus*).

**Flower.** A flower is a condensed shoot with four whorls on a swollen
**receptacle**: **calyx** of sepals, **corolla** of petals, **androecium** of
stamens (each a filament plus a two-lobed anther) and **gynoecium** of one or
more carpels (each an ovary with ovules, a style and a stigma). Learn these
descriptive terms, because family descriptions are written entirely in them.

- **Symmetry**: **actinomorphic** (radially symmetrical, mustard, *Datura*) or
  **zygomorphic** (bilaterally symmetrical, pea, *Ocimum*).
- **Sex**: **bisexual** (both whorls) or **unisexual** (staminate or pistillate).
- **Bracts**: a flower with a bract is **bracteate**, without one **ebracteate**.
- **Position of the ovary**: **hypogynous** (ovary superior, other whorls below —
  mustard, *Datura*), **perigynous** (ovary half-sunk in a cup-shaped receptacle —
  rose, plum) and **epigynous** (ovary inferior, whorls arising above it —
  sunflower, cucumber, guava).
- **Cohesion of stamens**: **monadelphous** (all united in one bundle by their
  filaments — *Hibiscus*), **diadelphous** (two bundles — pea), **polyadelphous**
  (many bundles — *Citrus*); **epipetalous** when attached to the petals
  (*Datura*), **epiphyllous** when attached to the perianth (*Allium*).
- **Placentation**: how ovules are attached inside the ovary — **marginal**
  (pea), **axile** (*Datura*, tomato, *Allium*), **parietal** (mustard,
  *Argemone*), **free central** (*Dianthus*, *Primula*), **basal** (sunflower,
  marigold) and **superficial** (water lily).
- **Aestivation**: how sepals or petals overlap in bud — **valvate**,
  **twisted**, **imbricate** and **vexillary** (the pea, where the standard
  covers the wings and the wings cover the keel).

**Fruit and seed.** The fruit develops from the ovary and the seed from the
ovule. **Simple** fruits come from one ovary and are **dry** (dehiscent —
legume of pea, siliqua of mustard, capsule of *Datura*; indehiscent — achene,
caryopsis of rice and wheat, cypsela of sunflower, nut of cashew; schizocarpic —
lomentum, cremocarp of coriander) or **fleshy** (drupe of mango with its stony
endocarp, berry of tomato and grape, pome of apple, hesperidium of orange, pepo
of cucumber). **Aggregate** fruits come from a multicarpellary apocarpous ovary
of a single flower (*Polyalthia*, strawberry) and **composite** or multiple
fruits from a whole inflorescence (sorosis of jackfruit and pineapple,
syconus of fig). A **false fruit** develops partly from the receptacle (apple,
cashew, strawberry). A seed consists of a **seed coat** (testa and tegmen), a
**hilum**, and the **embryo** of radicle, plumule and one or two **cotyledons**;
the food may be stored in the cotyledons (**non-endospermic**, pea, gram) or in
the **endosperm** (**endospermic**, maize, castor, coconut).

```figure caption="Monocotyledon and dicotyledon compared through the seed, leaf venation, root system and a transverse section of the stem."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon, FancyBboxPatch

fig, axes = plt.subplots(2, 4, figsize=(5.2, 2.9),
                         gridspec_kw={'wspace': 0.04, 'hspace': 0.06})
rng = np.random.default_rng(7)
GRN, BRN = '#6f9f57', '#8a6b4a'

for ax in axes.ravel():
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-1.10, 1.10)
    ax.set_aspect('equal')
    ax.axis('off')

def head(ax, s):
    ax.text(0, 1.14, s, ha='center', va='bottom', fontsize=6.4,
            color=INK, fontweight='bold')

# ------------- column 1: seed -------------------------------------------
ax = axes[0][0]; head(ax, 'seed')
ax.add_patch(Ellipse((0, 0), 1.05, 1.55, fc='#f0e2c4', ec=INK, lw=0.9))
ax.add_patch(Ellipse((0.14, 0.05), 0.52, 1.05, fc='#e0c98c', ec=INK, lw=0.7))
ax.add_patch(Ellipse((-0.20, -0.02), 0.34, 0.80, fc='#cfe3c5', ec='#2f6b2f', lw=0.7))
ax.text(0, -0.98, 'one cotyledon', ha='center', va='top', fontsize=5.8, color=MUTED)
ax = axes[1][0]
ax.add_patch(Ellipse((-0.26, 0), 0.62, 1.40, fc='#e8dcbe', ec=INK, lw=0.9))
ax.add_patch(Ellipse((0.26, 0), 0.62, 1.40, fc='#f0e6cc', ec=INK, lw=0.9))
ax.add_patch(Ellipse((0, -0.40), 0.22, 0.46, fc='#cfe3c5', ec='#2f6b2f', lw=0.7))
ax.text(0, -0.98, 'two cotyledons', ha='center', va='top', fontsize=5.8, color=MUTED)

# ------------- column 2: leaf venation ----------------------------------
ax = axes[0][1]; head(ax, 'leaf')
t = np.linspace(0, 1, 80)
blade = np.column_stack([np.concatenate([-0.42 * np.sin(np.pi * t), 0.42 * np.sin(np.pi * t)[::-1]]),
                         np.concatenate([-0.95 + 1.90 * t, (-0.95 + 1.90 * t)[::-1]])])
ax.add_patch(Polygon(blade, closed=True, fc='#9fc27f', ec='#3f6b30', lw=0.8))
for u in np.linspace(-0.30, 0.30, 7):
    ax.plot(u * np.sin(np.pi * t), -0.95 + 1.90 * t, color='#3f6b30', lw=0.5)
ax.text(0, -0.98, 'parallel veins', ha='center', va='top', fontsize=5.8, color=MUTED)
ax = axes[1][1]
blade2 = np.column_stack([np.concatenate([-0.52 * np.sin(np.pi * t) ** 0.8,
                                          0.52 * np.sin(np.pi * t)[::-1] ** 0.8]),
                          np.concatenate([-0.85 + 1.70 * t, (-0.85 + 1.70 * t)[::-1]])])
ax.add_patch(Polygon(blade2, closed=True, fc='#9fc27f', ec='#3f6b30', lw=0.8))
ax.plot([0, 0], [-0.85, 0.85], color='#3f6b30', lw=0.7)
for y0 in np.linspace(-0.58, 0.46, 6):
    y1 = y0 + 0.28
    t1 = (y1 + 0.85) / 1.70
    w1 = 0.52 * np.sin(np.pi * min(max(t1, 0.001), 0.999)) ** 0.8
    for sgn in (-1, 1):
        s = np.linspace(0, 1, 30)
        ax.plot(sgn * 0.82 * w1 * s, y0 + 0.28 * s, color='#3f6b30', lw=0.5)
ax.text(0, -0.98, 'reticulate veins', ha='center', va='top', fontsize=5.8, color=MUTED)

# ------------- column 3: root -------------------------------------------
ax = axes[0][2]; head(ax, 'root')
ax.plot([0, 0], [0.95, 0.30], color=GRN, lw=1.6)
for ang in np.linspace(-2.75, -0.40, 9):
    s = np.linspace(0, 1, 30)
    ax.plot(0.95 * s * np.cos(ang) * 1.0, 0.30 + 1.15 * s * np.sin(ang),
            color=BRN, lw=0.8)
ax.text(0, -0.98, 'fibrous', ha='center', va='top', fontsize=5.8, color=MUTED)
ax = axes[1][2]
ax.plot([0, 0], [0.95, 0.30], color=GRN, lw=1.6)
s = np.linspace(0, 1, 60)
ax.plot(0.10 * s ** 2, 0.30 - 1.20 * s, color=BRN, lw=2.2 - 1.4 * 0)
for y0, sgn in [(0.05, -1), (-0.15, 1), (-0.40, -1), (-0.60, 1)]:
    u = np.linspace(0, 1, 25)
    ax.plot(sgn * 0.42 * u, y0 - 0.32 * u, color=BRN, lw=0.8)
ax.text(0, -0.98, 'tap root', ha='center', va='top', fontsize=5.8, color=MUTED)

# ------------- column 4: vascular bundles in the stem -------------------
ax = axes[0][3]; head(ax, 'T.S. of stem')
ax.add_patch(Circle((0, 0.05), 0.85, fc='#f4f7f1', ec=INK, lw=0.9))
pts = [(0.0, 0.62), (-0.42, 0.44), (0.42, 0.44), (-0.60, 0.05), (0.60, 0.05),
       (-0.30, -0.10), (0.30, -0.10), (0.0, 0.18), (-0.40, -0.44), (0.40, -0.44),
       (0.0, -0.58)]
for px, py in pts:
    ax.add_patch(Circle((px, py), 0.095, fc='#c9dff0', ec=ACCENT, lw=0.7))
ax.text(0, -0.98, 'bundles scattered', ha='center', va='top', fontsize=5.8, color=MUTED)
ax = axes[1][3]
ax.add_patch(Circle((0, 0.05), 0.85, fc='#f4f7f1', ec=INK, lw=0.9))
for k in range(8):
    u = np.deg2rad(90 + k * 45)
    ax.add_patch(Circle((0.60 * np.cos(u), 0.05 + 0.60 * np.sin(u)), 0.105,
                        fc='#c9dff0', ec=ACCENT, lw=0.7))
ax.text(0, -0.98, 'bundles in a ring', ha='center', va='top', fontsize=5.8, color=MUTED)

fig.text(0.055, 0.695, 'MONOCOT', ha='center', va='center', fontsize=6.8,
         color=INK, fontweight='bold', rotation=90)
fig.text(0.055, 0.285, 'DICOT', ha='center', va='center', fontsize=6.8,
         color=INK, fontweight='bold', rotation=90)
fig.subplots_adjust(left=0.10)
```

| Character | Monocotyledon | Dicotyledon |
|---|---|---|
| Cotyledons in the seed | one | two |
| Root system | fibrous, adventitious | tap root |
| Leaf venation | parallel | reticulate |
| Leaf base | usually sheathing | not sheathing |
| Vascular bundles in the stem | many, scattered, closed (no cambium) | few, in a ring, open (with cambium) |
| Secondary growth | absent | usually present |
| Flower | usually trimerous (in threes) | tetra- or pentamerous |
| Perianth | usually undifferentiated (tepals) | calyx and corolla distinct |
| Pollen grain | monosulcate | trisulcate or tricolpate |
| Examples | rice, maize, onion, banana, palm | mustard, pea, *Datura*, mango |

### Taxonomic hierarchy

Taxonomy sorts organisms into a nested series of ranks, each a **taxon**. As you
climb the hierarchy the number of shared characters falls and the number of
organisms included rises; as you descend, the reverse. The obligatory ranks for
plants are:

**Kingdom → Division (Phylum) → Class → Order → Family → Genus → Species**

Intermediate ranks may be inserted with the prefixes *sub-* and *super-*
(subclass, subfamily, subspecies), and family names in botany end in **-aceae**
while order names end in **-ales**.

::: memory The hierarchy in order
**King David Came Over For Good Soup** — **K**ingdom, **D**ivision, **C**lass,
**O**rder, **F**amily, **G**enus, **S**pecies. (If you were taught the zoological
version, replace Division with Phylum: *King Philip Came Over...*) Remember also
that **the species is the only taxon that exists in nature**; every rank above it
is a human judgement about how to group species.
:::

::: definition Species
A group of individuals that resemble one another in all essential morphological
and reproductive characters, can interbreed freely among themselves to produce
fertile offspring, and are reproductively isolated from other such groups. It is
the basic unit of classification.
:::

| Rank | Mustard | Onion |
|---|---|---|
| Kingdom | Plantae | Plantae |
| Division | Angiospermae (Magnoliophyta) | Angiospermae (Magnoliophyta) |
| Class | Dicotyledonae | Monocotyledonae |
| Order | Brassicales | Liliales |
| Family | Brassicaceae | Liliaceae |
| Genus | *Brassica* | *Allium* |
| Species | *campestris* | *cepa* |

::: example Worked example 2.3 — Using a dichotomous key
A key is a branching set of paired statements (**couplets**); at each couplet you
choose the half that fits your specimen and follow the number at its end. Use the
key below to identify four specimens: **A** a small green plant, 2 cm tall, with
no roots and a stalked capsule; **B** a plant with an underground rhizome and
coiled young leaves bearing brown patches beneath the mature ones; **C** a tree
with needle leaves in threes and a woody cone; **D** a herb with yellow
four-petalled flowers and a long pod.

```
1a. Vascular tissue absent; no true roots ................................... 2
1b. Vascular tissue present; true roots present ............................. 3
2a. Plant a flat thallus .......................................... Liverwort
2b. Plant a leafy axis with a stalked capsule .......................... Moss
3a. Seeds absent; reproduction by spores ............................... Fern
3b. Seeds present ........................................................... 4
4a. Seeds naked on a cone scale; leaves needle-like ............... Gymnosperm
4b. Seeds enclosed in a fruit; flowers present .................... Angiosperm
```

**A.** No roots, so take 1a, then 2. It has a leafy axis and a stalked capsule, so
2b → **moss** (a bryophyte such as *Funaria*). The stalked capsule is the
sporophyte.

**B.** It has roots and vascular tissue, so 1b → 3. There are no seeds; the brown
patches are **sori** of sporangia, so 3a → **fern** (a pteridophyte such as
*Dryopteris*). Circinate vernation confirms it.

**C.** 1b → 3, seeds present → 4, needles and a woody cone → 4a → **gymnosperm**
(*Pinus roxburghii*, since the needles are in threes).

**D.** 1b → 3 → 4; flowers and a fruit are present → 4b → **angiosperm**. Four
petals and a long pod make it a crucifer — *Brassica campestris*.

The two points to notice are that a key uses only **contrasting, easily observed**
characters, and that each couplet must be **mutually exclusive and exhaustive**,
so that exactly one path is possible for any specimen.
:::

### Artificial, natural and phylogenetic systems

Classification systems are of three kinds, and they appeared in that order.

An **artificial system** uses one or a few arbitrarily chosen characters for
convenience, ignoring overall relationship. **Linnaeus (1753)** classified
flowering plants by the number and union of stamens and carpels alone — a *sexual
system* — which is quick to use but puts unrelated plants together and separates
close relatives. Theophrastus, who in about 300 BC sorted plants into herbs,
shrubs, undershrubs and trees, had done the same thing with habit.

A **natural system** uses **as many characters as possible**, chiefly
morphological, so that groups reflect real overall resemblance. The great natural
system is that of **George Bentham and Joseph Dalton Hooker**, published as
*Genera Plantarum* (1862–1883) from Kew, which treated 97,205 species in 202
orders. It remains the most-used system in Indian and Nepali herbaria for
practical identification because its descriptions were made from actual
specimens. Bentham and Hooker divided **Dicotyledons** into **Polypetalae**
(petals free), **Gamopetalae** (petals united) and **Monochlamydeae** (one whorl
of perianth), and then placed the **Gymnosperms between the Dicotyledons and the
Monocotyledons** — its most-criticised feature, and an examination favourite.

A **phylogenetic system** groups plants according to **evolutionary descent**, so
that each taxon contains one ancestor and all its descendants; it uses
morphology, anatomy, embryology, cytology, palynology, chemistry and now DNA
sequence. The first was **Engler and Prantl's** *Die natürlichen
Pflanzenfamilien* (1887–1915), which treated naked, unisexual, wind-pollinated
flowers as primitive. Later systems include **Hutchinson** (1926–34, who
separated woody and herbaceous dicot lines), **Takhtajan**, **Cronquist**, and
today the **Angiosperm Phylogeny Group (APG)** classification, built directly
from gene sequences.

| Basis | Artificial | Natural | Phylogenetic |
|---|---|---|---|
| Characters used | one or a few, arbitrary | as many as possible | all, including molecular |
| Aim | convenience of identification | true overall resemblance | evolutionary relationship |
| Relationships shown | none | affinity, but not descent | descent, as a family tree |
| Chief worker | Linnaeus (1753) | Bentham and Hooker (1862–83) | Engler and Prantl (1887–1915) |
| Chief drawback | unrelated plants grouped together | does not show evolution | needs data Linnaeus never had |

```figure caption="Floral diagrams of the four prescribed families. The dot at the top of each is the position of the mother axis; brackets in the formulae mean fused members."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, Wedge, Ellipse, Polygon

fig, axes = plt.subplots(2, 2, figsize=(5.0, 4.0),
                         gridspec_kw={'wspace': 0.02, 'hspace': 0.10})
axes = axes.ravel()

SEP, PET, STA = '#4f8f4f', '#d08fb0', '#c9a24a'

def crescent(ax, ang, r, w, span, fc, ec, notch=False):
    """A crescent-shaped member of a floral whorl at angle ang (degrees)."""
    th = np.linspace(np.deg2rad(ang - span / 2), np.deg2rad(ang + span / 2), 60)
    out = np.column_stack([(r + w) * np.cos(th), (r + w) * np.sin(th)])
    inn = np.column_stack([r * np.cos(th), r * np.sin(th)])[::-1]
    ax.add_patch(Polygon(np.vstack([out, inn]), closed=True, fc=fc, ec=ec, lw=0.7))

def stamen(ax, ang, r, s=0.075, fc=STA):
    x, y = r * np.cos(np.deg2rad(ang)), r * np.sin(np.deg2rad(ang))
    ax.add_patch(Ellipse((x, y), 2.4 * s, 1.5 * s, angle=ang + 90,
                         fc=fc, ec=INK, lw=0.6))
    ax.plot([x - 0.5 * s * np.cos(np.deg2rad(ang + 90)),
             x + 0.5 * s * np.cos(np.deg2rad(ang + 90))],
            [y - 0.5 * s * np.sin(np.deg2rad(ang + 90)),
             y + 0.5 * s * np.sin(np.deg2rad(ang + 90))], color=INK, lw=0.5)

def axisdot(ax, r=1.10):
    ax.plot([0], [r], marker='o', ms=3.2, color=INK)
    ax.text(0, r + 0.16, 'mother axis', ha='center', va='bottom',
            fontsize=5.5, color=MUTED)

def finish(ax, title, formula):
    ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(-1.45, 1.42)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.text(0, -1.42, title, ha='center', va='bottom', fontsize=6.6,
            color=INK, fontweight='bold')
    ax.text(0, -1.20, formula, ha='center', va='bottom', fontsize=6.0,
            color='#1d6fb8')

# ---- Brassicaceae: K2+2, C4, A2+4, G(2) --------------------------------
ax = axes[0]
for ang in (90, 270):
    crescent(ax, ang, 0.86, 0.11, 58, '#d8e8d0', SEP)
for ang in (0, 180):
    crescent(ax, ang, 0.98, 0.11, 58, '#d8e8d0', SEP)
for ang in (45, 135, 225, 315):
    crescent(ax, ang, 0.66, 0.13, 62, '#f2d3e2', PET)
for ang in (100, 260):
    stamen(ax, ang, 0.46)
for ang in (20, 50, 200, 230):
    stamen(ax, ang, 0.42)
ax.add_patch(Ellipse((0, 0), 0.40, 0.30, fc='#cfe3c5', ec='#2f6b2f', lw=0.9))
ax.plot([-0.20, 0.20], [0, 0], color='#2f6b2f', lw=0.7, ls=(0, (2, 1.5)))
for ox in (-0.10, 0.10):
    ax.add_patch(Circle((ox, 0), 0.045, fc='#f7e6a8', ec='#8a6b2a', lw=0.5))
axisdot(ax)
finish(ax, 'Brassicaceae (mustard)', 'K 2+2   C 4   A 2+4   G (2)')

# ---- Fabaceae: K(5), C5 papilionaceous, A(9)+1, G1 ---------------------
ax = axes[1]
for k in range(5):
    crescent(ax, 234 + k * 72, 0.92, 0.11, 66, '#d8e8d0', SEP)
crescent(ax, 90, 0.62, 0.17, 86, '#f2d3e2', PET)
for ang in (30, 150):
    crescent(ax, ang, 0.60, 0.14, 62, '#f2d3e2', PET)
for ang in (300, 240):
    crescent(ax, ang, 0.58, 0.13, 56, '#f7e2ec', PET)
th = np.linspace(np.deg2rad(200), np.deg2rad(-20), 9)
for u in th:
    stamen(ax, np.degrees(u), 0.40, s=0.055)
stamen(ax, 90, 0.40, s=0.055, fc='#efe0b0')
ax.add_patch(Ellipse((0, -0.02), 0.26, 0.34, fc='#cfe3c5', ec='#2f6b2f', lw=0.9))
for oy in (-0.10, 0.06):
    ax.add_patch(Circle((0.055, oy), 0.040, fc='#f7e6a8', ec='#8a6b2a', lw=0.5))
axisdot(ax)
finish(ax, 'Fabaceae (pea)', 'K (5)   C 1+2+(2)   A (9)+1   G 1')

# ---- Solanaceae: K(5), C(5), A5, G(2) oblique --------------------------
ax = axes[2]
th = np.linspace(0, 2 * np.pi, 200)
ax.plot(0.96 * np.cos(th), 0.96 * np.sin(th), color=SEP, lw=1.4)
for k in range(5):
    crescent(ax, 234 + k * 72, 0.86, 0.11, 64, '#d8e8d0', SEP)
ax.plot(0.68 * np.cos(th), 0.68 * np.sin(th), color=PET, lw=1.4)
for k in range(5):
    crescent(ax, 270 + k * 72, 0.58, 0.13, 64, '#f2d3e2', PET)
for k in range(5):
    ang = 306 + k * 72
    u = np.deg2rad(ang)
    ax.plot([0.44 * np.cos(u), 0.68 * np.cos(u)],
            [0.44 * np.sin(u), 0.68 * np.sin(u)], color=PET, lw=0.7)
    stamen(ax, ang, 0.42)
ax.add_patch(Ellipse((0, 0), 0.44, 0.30, angle=42, fc='#cfe3c5',
                     ec='#2f6b2f', lw=0.9))
ax.plot([-0.16, 0.16], [-0.145, 0.145], color='#2f6b2f', lw=0.7, ls=(0, (2, 1.5)))
for s in (-1, 1):
    ax.add_patch(Circle((s * 0.075, s * -0.068), 0.042, fc='#f7e6a8',
                        ec='#8a6b2a', lw=0.5))
axisdot(ax)
finish(ax, 'Solanaceae (potato)', 'K (5)   C (5)   A 5   G (2)  oblique')

# ---- Liliaceae: P3+3, A3+3, G(3) ---------------------------------------
ax = axes[3]
for k in range(3):
    crescent(ax, 90 + k * 120, 0.88, 0.12, 74, '#e6dcf0', '#7f5fa8')
for k in range(3):
    crescent(ax, 30 + k * 120, 0.66, 0.13, 74, '#efe6f7', '#7f5fa8')
for k in range(3):
    stamen(ax, 90 + k * 120, 0.46)
for k in range(3):
    stamen(ax, 30 + k * 120, 0.44)
ax.add_patch(Circle((0, 0), 0.24, fc='#cfe3c5', ec='#2f6b2f', lw=0.9))
for k in range(3):
    u = np.deg2rad(90 + k * 120)
    ax.plot([0, 0.24 * np.cos(u)], [0, 0.24 * np.sin(u)],
            color='#2f6b2f', lw=0.7)
    v = np.deg2rad(30 + k * 120)
    ax.add_patch(Circle((0.115 * np.cos(v), 0.115 * np.sin(v)), 0.042,
                        fc='#f7e6a8', ec='#8a6b2a', lw=0.5))
axisdot(ax)
finish(ax, 'Liliaceae (onion, lily)', 'P 3+3   A 3+3   G (3)')
```

::: caution Old family names, new family limits
The NEB syllabus teaches **Liliaceae** in the broad sense of Bentham and Hooker,
which includes onion and garlic. Molecular work has since split that family up:
APG places *Allium* in **Amaryllidaceae** and *Aloe* in **Asphodelaceae**, and
restricts Liliaceae to *Lilium*, *Tulipa* and their close relatives. Similarly
Brassicaceae was once Cruciferae, Fabaceae was Leguminosae, and Poaceae was
Gramineae. Write the name your syllabus uses, but if you know the modern one, add
it in brackets — it never loses marks and it shows you understand that
classification is a moving target.
:::

### Brassicaceae

**Brassicaceae** (formerly Cruciferae, the mustard family) has about 350 genera
and 3,000 species, mostly herbs of the north temperate zone; Nepal grows several
as staple oilseeds and vegetables.

- **Habit**: annual or biennial **herbs**, rarely undershrubs, often with pungent
  watery juice.
- **Root**: tap root, sometimes swollen (radish, turnip).
- **Stem**: herbaceous, erect, cylindrical, often hairy.
- **Leaves**: alternate, simple, **exstipulate**, often with a sheathing base;
  radical leaves usually form a rosette and are lyrate or pinnatifid.
- **Inflorescence**: **racemose** — a raceme or corymbose raceme.
- **Flower**: **ebracteate**, pedicellate, complete, **bisexual**,
  **actinomorphic**, **hypogynous**, **tetramerous**.
- **Calyx**: 4 sepals in two whorls of 2, free (**polysepalous**), imbricate.
- **Corolla**: 4 petals, free (**polypetalous**), arranged in the form of a
  **cross** — the **cruciform** corolla that named the old family — valvate, with
  a clawed base.
- **Androecium**: **6 stamens in two whorls**, the outer 2 short and the inner 4
  long — the condition called **tetradynamous**; anthers dithecous, basifixed,
  introrse.
- **Gynoecium**: **bicarpellary, syncarpous**; ovary superior, at first
  unilocular but divided into two chambers by a false septum, the **replum**;
  **parietal placentation**; style short, stigma bilobed.
- **Fruit**: a **siliqua** (long, as in mustard) or **silicula** (short, as in
  *Capsella*), dehiscing from below upward and leaving the replum with the seeds.
- **Seed**: non-endospermic, with a curved embryo.
- **Floral formula**: **Bisexual, actinomorphic — K2+2 C4 A2+4 G(2)**
- **Economic importance**: oilseeds (*Brassica campestris*, tori; *B. juncea*,
  rayo; *B. napus*); vegetables (*B. oleracea* var. *capitata* cabbage, var.
  *botrytis* cauliflower, var. *gongylodes* knol-khol; *Raphanus sativus*,
  radish); condiments (*Brassica nigra*, black mustard); medicine (*Iberis
  amara*); ornamentals (*Iberis*, *Matthiola*, *Cheiranthus*, wallflower);
  and the weed *Capsella bursa-pastoris* (shepherd's purse).

### Fabaceae

**Fabaceae** (Leguminosae, the pea family), taken here in the sense of the
subfamily **Papilionoideae**, is the third largest family of flowering plants and
by far the most important for soil fertility, because its roots carry
nitrogen-fixing *Rhizobium*.

- **Habit**: herbs, shrubs, trees and **climbers** (pea, *Lathyrus*, *Butea*,
  *Dalbergia*).
- **Root**: tap root with **nodules** containing *Rhizobium leguminosarum*, which
  fixes atmospheric nitrogen.
- **Stem**: erect or twining; sometimes winged or modified into tendrils.
- **Leaves**: alternate, **stipulate**, usually **pinnately compound** with
  **pulvinate** leaf base; the terminal leaflets of pea are tendrils; in
  *Lathyrus aphaca* the whole leaf is a tendril and the stipules photosynthesise.
- **Inflorescence**: racemose — raceme or, in *Trifolium*, a head.
- **Flower**: bracteate, **bisexual**, **zygomorphic**, hypogynous,
  pentamerous.
- **Calyx**: 5 sepals, **gamosepalous**, campanulate, imbricate or valvate.
- **Corolla**: 5 petals, polypetalous but **papilionaceous** — one large posterior
  **standard (vexillum)**, two lateral **wings (alae)** and two anterior petals
  fused to form the **keel (carina)** that encloses the stamens and style;
  aestivation **vexillary**.
- **Androecium**: **10 stamens, diadelphous (9) + 1** — nine united by their
  filaments into a sheath and the tenth, opposite the standard, free; anthers
  dithecous, basifixed.
- **Gynoecium**: **monocarpellary**; ovary superior, unilocular, with **marginal
  placentation**; style bent, with a hairy tip below a simple stigma.
- **Fruit**: a **legume** or pod, dehiscing along both sutures.
- **Seed**: one to many, non-endospermic, with a large hilum.
- **Floral formula**: **Bisexual, zygomorphic — K(5) C1+2+(2) A(9)+1 G1**
- **Economic importance**: **pulses**, the chief vegetable protein of Nepal
  (*Cicer arietinum* chana, *Lens culinaris* musuro, *Cajanus cajan* rahar,
  *Pisum sativum* pea, *Glycine max* soyabean, *Phaseolus* and *Vigna* beans);
  **oils** (groundnut *Arachis hypogaea*, soyabean); **fodder** (*Medicago
  sativa* lucerne, *Trifolium* clover); **timber and fuel** (*Dalbergia sissoo*
  sisau, *Pterocarpus*); **dyes** (indigo from *Indigofera tinctoria*); **gum**
  (*Astragalus*); **fish poison and insecticide** (*Derris*, rotenone);
  **ornamentals** (*Lupinus*, *Clitoria*, *Butea monosperma* palas); and above
  all **green manure and crop rotation**, because a legume leaves the soil richer
  in nitrogen than it found it.

### Solanaceae

**Solanaceae**, the potato or nightshade family, has about 90 genera and 2,800
species and includes both our most valuable vegetables and some of our most
dangerous poisons, since the family is rich in **alkaloids**.

- **Habit**: mostly **herbs** and shrubs, rarely small trees; often with a
  disagreeable smell.
- **Root**: tap root; **stem tubers** in potato.
- **Stem**: herbaceous or woody, erect, branched, sometimes prickly
  (*Solanum xanthocarpum*); underground stem tuber in *Solanum tuberosum*.
- **Leaves**: alternate, simple, exstipulate, entire or lobed, with **bicollateral
  vascular bundles** in the petiole.
- **Inflorescence**: usually a **cymose** inflorescence — a helicoid or
  scorpioid cyme, solitary axillary in *Datura*.
- **Flower**: ebracteate, pedicellate, bisexual, **actinomorphic**, hypogynous,
  pentamerous.
- **Calyx**: 5 sepals, **gamosepalous**, valvate, **persistent** and often
  enlarging around the fruit (the papery bladder of *Physalis*).
- **Corolla**: 5 petals, gamopetalous, rotate, campanulate or infundibuliform,
  valvate or twisted.
- **Androecium**: **5 stamens, epipetalous**, inserted on the corolla tube and
  **alternating with the petals**; anthers dithecous, basifixed, often
  **connivent** around the style and in *Solanum* opening by apical pores.
- **Gynoecium**: **bicarpellary, syncarpous**; ovary superior, **bilocular**, the
  two chambers set **obliquely** to the median plane because of a false septum;
  **axile placentation** on a swollen axis, with many ovules; style simple,
  stigma bilobed.
- **Fruit**: a **berry** (tomato, brinjal) or a **capsule** (*Datura*, spiny and
  four-valved).
- **Seed**: endospermic, with a curved embryo.
- **Floral formula**: **Bisexual, actinomorphic — K(5) C(5) A5 G(2)**, ovary
  obliquely placed.
- **Economic importance**: **food** (*Solanum tuberosum* potato — the world's
  fourth staple, *S. melongena* brinjal, *Lycopersicon esculentum* tomato,
  *Capsicum annuum* chilli and capsicum); **drugs** (belladonna and atropine from
  *Atropa belladonna*, used to dilate the pupil; hyoscine from *Hyoscyamus
  niger*; *Datura stramonium* for asthma; *Withania somnifera*, ashwagandha);
  **narcotic** (nicotine from *Nicotiana tabacum*, tobacco, the family's most
  destructive gift); **ornamentals** (*Petunia*, *Cestrum nocturnum* raat ki
  rani, *Solanum pseudocapsicum*); and **poisons** — the green parts of potato and
  the seeds of *Datura* contain solanine and hyoscyamine and have caused deaths.

### Liliaceae

**Liliaceae**, the lily family, is the representative **monocot** family of the
syllabus, taken in the broad Bentham and Hooker sense that includes *Allium*. It
has about 250 genera and 4,000 species and is the monocot equivalent of a
textbook family: perfectly trimerous throughout.

- **Habit**: perennial **herbs** with underground perennating organs, rarely
  shrubs (*Yucca*) or climbers (*Smilax*, *Gloriosa*).
- **Root**: **adventitious**, fibrous, often fleshy or contractile.
- **Stem**: underground **bulb** (*Allium*, *Lilium*, *Tulipa*), **rhizome**
  (*Asparagus*, *Aloe*) or corm; aerial stem sometimes modified into a
  **phylloclade** or cladode (*Asparagus*, where the apparent leaves are stems
  and the true leaves are scales).
- **Leaves**: mostly radical, alternate or whorled, simple, exstipulate, sessile
  with a sheathing base, **parallel-veined**, often fleshy (*Aloe*).
- **Inflorescence**: racemose — a raceme, or a scapigerous **umbel** enclosed at
  first by papery bracts (*Allium*), or solitary (*Tulipa*).
- **Flower**: bracteate, pedicellate, bisexual, actinomorphic, **hypogynous**,
  **trimerous**.
- **Perianth**: **6 tepals in two whorls of 3**, the calyx and corolla not
  distinguishable, hence **perianth (P)** in the formula; usually petaloid,
  free or united into a tube, valvate.
- **Androecium**: **6 stamens in two whorls of 3**, **epiphyllous** (attached to
  the tepals) and opposite them; anthers dithecous, introrse, dehiscing
  longitudinally.
- **Gynoecium**: **tricarpellary, syncarpous**; ovary superior, **trilocular**,
  with **axile placentation** and usually many ovules; style one, stigma
  trilobed.
- **Fruit**: a **capsule** (*Lilium*, *Allium*), rarely a berry (*Asparagus*,
  *Smilax*).
- **Seed**: endospermic, with a straight embryo.
- **Floral formula**: **Bisexual, actinomorphic — P3+3 A3+3 G(3)**
- **Economic importance**: **food and condiment** (*Allium cepa* onion, *A.
  sativum* garlic, *Asparagus officinalis*); **medicine** (*Aloe barbadensis*
  ghiukumari, for burns and cosmetics; *Colchicum autumnale*, the source of
  **colchicine**, used to induce polyploidy and to treat gout; *Smilax*,
  sarsaparilla; *Urginea*, a cardiac stimulant); **fibre** (*Yucca*, *Phormium*);
  **ornamentals** (*Lilium*, *Tulipa*, *Gloriosa superba*, *Hyacinthus*,
  *Dracaena*); and the poisonous *Colchicum* and *Gloriosa*, whose tubers kill.

| Character | Brassicaceae | Fabaceae | Solanaceae | Liliaceae |
|---|---|---|---|---|
| Class | Dicot | Dicot | Dicot | **Monocot** |
| Habit | herbs | herbs to trees, climbers | herbs, shrubs | herbs with bulb or rhizome |
| Inflorescence | raceme | raceme | cyme | umbel or raceme |
| Symmetry | actinomorphic | **zygomorphic** | actinomorphic | actinomorphic |
| Perianth | K4 C4, cruciform | K(5) C papilionaceous | K(5) C(5) | **P3+3** |
| Androecium | 6, **tetradynamous** | 10, **diadelphous** | 5, **epipetalous** | 6, **epiphyllous** |
| Gynoecium | bicarpellary, parietal, replum | monocarpellary, marginal | bicarpellary, axile, oblique | tricarpellary, axile |
| Fruit | siliqua or silicula | legume | berry or capsule | capsule or berry |
| Floral formula | K2+2 C4 A2+4 G(2) | K(5) C1+2+(2) A(9)+1 G1 | K(5) C(5) A5 G(2) | P3+3 A3+3 G(3) |
| Type plant | *Brassica campestris* | *Pisum sativum* | *Solanum nigrum* | *Allium cepa* |

::: example Worked example 2.4 — Writing a floral formula from a description
"The flower is subtended by a bract. It is bisexual and can be divided into two
equal halves in one plane only. There are five united sepals, five free petals of
which one is large and posterior, two are lateral and two are fused below, ten
stamens of which nine are joined by their filaments and one is free, and a single
carpel whose ovary lies above the other whorls." Write the floral formula, name
the family and predict the fruit.

**Step 1 — decode each phrase into a symbol.**

| Phrase in the description | Meaning | Symbol |
|---|---|---|
| subtended by a bract | bracteate | Br |
| divisible into two equal halves in one plane only | zygomorphic | % (or state in words) |
| five united sepals | gamosepalous calyx of 5 | K(5) |
| one posterior + two lateral + two fused | papilionaceous corolla | C1+2+(2) |
| nine joined, one free | diadelphous androecium of 10 | A(9)+1 |
| single carpel | monocarpellary gynoecium | G1 |
| ovary above the other whorls | hypogynous, superior ovary | underline G |

**Step 2 — assemble.** Brackets mean united, a plus sign separates whorls or
groups, and a bar under the G means the ovary is superior:

**Bisexual, zygomorphic — K(5) C1+2+(2) A(9)+1 G1**

**Step 3 — identify.** A zygomorphic papilionaceous corolla with a diadelphous
(9)+1 androecium and a monocarpellary superior ovary is diagnostic of
**Fabaceae** (Papilionoideae) — for example *Pisum sativum*.

**Step 4 — predict the fruit.** A single carpel with marginal placentation
dehiscing along both sutures gives a **legume** (pod), and the seeds will be
non-endospermic with food stored in the two fleshy cotyledons.

Work the same three steps backwards to answer the commoner version of this
question: "given the formula K(5) C(5) A5 G(2), describe the flower" — five
united sepals, five united petals, five epipetalous stamens, a bicarpellary
syncarpous superior ovary, actinomorphic and bisexual, so **Solanaceae**, and the
fruit is a berry or a capsule.
:::

## Chapter summary

- **Three domains** — Archaea, Bacteria, Eukarya — were proposed by Woese (1977)
  from 16S rRNA sequences. Archaea and Bacteria are prokaryotic; only Archaea have
  branched, ether-linked membrane lipids.
- **Binomial nomenclature** (Linnaeus, *Species Plantarum*, 1753) gives every
  species a two-word Latin name: capitalised genus, lower-case species epithet,
  italicised in print, underlined separately in handwriting, governed by the ICN
  and the principle of priority.
- **Whittaker's five kingdoms** (1969) — Monera, Protista, Fungi, Plantae,
  Animalia — separate organisms by cell type, body organisation and **mode of
  nutrition**. Viruses fall outside the scheme entirely.
- **Nepal** holds over **3 %** of the world's known plants on **0.1 %** of its
  land: about 6,500 angiosperms, 28 gymnosperms, 534 pteridophytes, 1,150
  bryophytes, 771 lichens, with about 300 endemic flowering plants.
- **Fungi** are achlorophyllous absorptive heterotrophs with chitin walls,
  glycogen reserve and a mycelium of coenocytic or septate hyphae. Sexual
  reproduction runs plasmogamy → karyogamy → meiosis, with a **dikaryotic** stage
  in the higher classes. Four classes: Phycomycetes (zygospore), Ascomycetes
  (8 ascospores in an ascus), Basidiomycetes (4 basidiospores on a basidium),
  Deuteromycetes (sexual stage unknown).
- **Lichens** are fungus + alga: the mycobiont gives the body and absorbs water,
  the photobiont gives the food. Crustose, foliose and fruticose growth forms;
  reproduction chiefly by **soredia** and **isidia**. They are pioneers of rock
  succession, indicators of SO₂ pollution and the source of litmus.
- **Algae** are thalloid autotrophs with unicellular sex organs and no embryo.
  Fritsch's classes are recognised by pigment and reserve food: green (starch),
  brown (laminarin, fucoxanthin), red (floridean starch, phycoerythrin, **no
  flagella**). Sexual reproduction advances through isogamy → anisogamy → oogamy.
- **Bryophytes** are the amphibians of the plant kingdom: **gametophyte dominant**,
  no vascular tissue, rhizoids instead of roots, jacketed antheridia and
  archegonia, water needed for fertilisation, and a dependent sporophyte of foot,
  seta and capsule.
- **Pteridophytes** are **vascular cryptogams**: **sporophyte dominant** with true
  root, stem and leaf, xylem of tracheids, sporangia in sori with an annulus and
  indusium, and a small independent prothallus. Heterospory (*Selaginella*,
  *Marsilea*, *Salvinia*) is the evolutionary step towards the seed.
- **Gymnosperms** bear **naked seeds** on open megasporophylls in cones, lack
  vessels (except Gnetales), are wind-pollinated directly on to the micropyle,
  form **haploid endosperm before fertilisation**, show polyembryony, and never
  form fruit.
- **Angiosperms** enclose the ovule in an ovary, undergo **double fertilisation**
  and form fruit; they divide into monocots (one cotyledon, fibrous roots,
  parallel venation, scattered closed bundles, trimerous flowers) and dicots.
- The **taxonomic hierarchy** is Kingdom → Division → Class → Order → Family →
  Genus → Species; only the species is a natural unit.
- Classification systems are **artificial** (Linnaeus, a few characters),
  **natural** (Bentham and Hooker, *Genera Plantarum* 1862–83, many characters,
  gymnosperms wrongly placed between dicots and monocots) and **phylogenetic**
  (Engler and Prantl, and today APG, based on descent).
- The four families reduce to four formulae: **Brassicaceae K2+2 C4 A2+4 G(2)**,
  **Fabaceae K(5) C1+2+(2) A(9)+1 G1**, **Solanaceae K(5) C(5) A5 G(2)**,
  **Liliaceae P3+3 A3+3 G(3)**.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Which one of the following is **not** a criterion of Whittaker's five-kingdom classification? <span class="marks">[1]</span>
   (a) cell structure (b) mode of nutrition (c) body organisation (d) chromosome number
2. The reserve food of brown algae is <span class="marks">[1]</span>
   (a) starch (b) laminarin (c) floridean starch (d) glycogen
3. In bryophytes the dominant phase of the life cycle is the <span class="marks">[1]</span>
   (a) diploid sporophyte (b) haploid gametophyte (c) dikaryotic mycelium (d) prothallus
4. The endosperm of a gymnosperm seed is <span class="marks">[1]</span>
   (a) haploid and formed before fertilisation (b) triploid and formed after fertilisation (c) diploid and formed before fertilisation (d) absent
5. The androecium described as tetradynamous, with two short and four long stamens, is characteristic of <span class="marks">[1]</span>
   (a) Fabaceae (b) Solanaceae (c) Brassicaceae (d) Liliaceae

::: note Answers to Group A
**1.** (d) — Whittaker used cell structure, body organisation, mode of nutrition, reproduction and phylogeny, not chromosome number.
**2.** (b) — laminarin and mannitol; the brown colour is due to fucoxanthin.
**3.** (b) — the leafy moss plant is the gametophyte; the sporophyte is attached to it and dependent on it.
**4.** (a) — the female gametophyte tissue forms before fertilisation, so it is haploid; there is no double fertilisation.
**5.** (c) — 6 stamens in whorls of 2 (short) and 4 (long), written A2+4.
:::

**Group B — Short answer questions (4 marks each)**

1. Give any four general characters of Bryophyta and explain why bryophytes are
   called the amphibians of the plant kingdom. <span class="marks">[4]</span>
2. Tabulate any four differences between gymnosperms and angiosperms.
   <span class="marks">[4]</span>
3. What is a lichen? Name its two components, state the contribution of each, and
   give two uses of lichens. <span class="marks">[4]</span>
4. Draw a labelled floral diagram of *Pisum sativum* and write its floral
   formula, explaining what each symbol in the formula means.
   <span class="marks">[4]</span>

::: note Answers to Group B
**1.** Any four of: the plant body is a haploid gametophyte, thalloid or leafy,
with **no true roots** (only rhizoids) and **no vascular tissue**; sex organs are
multicellular and jacketed (antheridium and archegonium); fertilisation needs
**external water**; the zygote forms an embryo and then a sporophyte of foot, seta
and capsule which stays **attached to and dependent on** the gametophyte; spores
formed by meiosis germinate into a protonema. They are called amphibians because,
like frogs, they live on land but must return to water to reproduce — the
biflagellate antherozoids can only reach the egg by swimming through a film of
water, so bryophytes are confined to moist, shaded habitats.

**2.** Ovule naked on an open megasporophyll / enclosed in an ovary; no fruit /
fruit present; xylem without vessels (except Gnetales) / with vessels; single
fertilisation / **double fertilisation**; endosperm haploid and formed before
fertilisation / triploid and formed after; reproductive structure a cone / a
flower; polyembryony common / rare; woody habit only / all habits. (Any four,
properly tabulated with both columns filled.)

**3.** A lichen is a stable symbiotic association of a fungus and a
photosynthetic partner forming a thallus unlike either alone. The **mycobiont**
(usually an Ascomycete, 90–95 % of the thallus) forms the body, absorbs and
retains water and minerals, and protects the alga from desiccation and intense
light; the **phycobiont** (a green alga such as *Trebouxia*, or a cyanobacterium
such as *Nostoc*) photosynthesises and, if a cyanobacterium, also fixes nitrogen.
Uses (any two): source of **litmus** from *Roccella tinctoria*; **bio-indicators
of SO₂ air pollution**; food and fodder (*Cetraria*, *Cladonia rangiferina*);
perfumery (*Evernia*); the antibiotic usnic acid; pioneers of xerophytic
succession on bare rock.

**4.** Floral formula: **Bisexual, zygomorphic — K(5) C1+2+(2) A(9)+1 G1**. In the
diagram show the mother axis at the top, the bract below, then five united sepals,
the papilionaceous corolla with the posterior standard outermost, two lateral
wings and two fused keel petals, the nine fused stamens with the tenth free
opposite the standard, and at the centre a single carpel with marginal
placentation. Meaning of the symbols: K = calyx and the bracket means the sepals
are fused; C1+2+(2) = five petals in three groups, of which two are fused;
A(9)+1 = ten stamens, nine united by their filaments (diadelphous) and one free;
G1 = one carpel; the bar under G shows the ovary is superior (hypogynous); the
flower is zygomorphic, so it can be halved in only one plane.
:::

**Group C — Long answer questions (8 marks each)**

1. Describe the family Solanaceae under the headings habit, leaf, inflorescence,
   flower (calyx, corolla, androecium and gynoecium), fruit and floral formula,
   and give four points of economic importance with named examples.
   <span class="marks">[8]</span>
2. With the help of a labelled diagram, describe the life cycle of a moss such as
   *Funaria*, marking the ploidy of each stage, and explain how alternation of
   generations in a fern differs from it. <span class="marks">[8]</span>

::: note Answers to Group C
**1.** *Habit*: mostly annual or perennial **herbs** and shrubs, rarely small
trees, with a tap root; potato has an underground stem tuber and *Solanum
xanthocarpum* is prickly. *Leaf*: alternate, simple, exstipulate, entire or
lobed, with bicollateral vascular bundles. *Inflorescence*: usually a **cymose**
inflorescence (helicoid or scorpioid cyme), solitary and axillary in *Datura*.
*Flower*: ebracteate, pedicellate, complete, bisexual, **actinomorphic**,
hypogynous, pentamerous. *Calyx*: 5 sepals, gamosepalous, valvate,
**persistent** and enlarging in fruit. *Corolla*: 5 petals, gamopetalous, rotate
or infundibuliform, valvate or twisted. *Androecium*: **5 stamens, epipetalous**,
inserted on the corolla tube and alternating with the petals; anthers dithecous,
basifixed, often connivent and in *Solanum* opening by apical pores. *Gynoecium*:
**bicarpellary, syncarpous**; ovary superior, bilocular with the locules set
**obliquely**, **axile placentation** on a swollen placenta, many ovules; style
simple, stigma bilobed. *Fruit*: a **berry** (tomato, brinjal) or a **capsule**
(*Datura*). *Seed*: endospermic. *Floral formula*: bisexual, actinomorphic —
**K(5) C(5) A5 G(2)**. *Economic importance*: **food** — *Solanum tuberosum*
(potato), *S. melongena* (brinjal), *Lycopersicon esculentum* (tomato),
*Capsicum annuum* (chilli); **medicine** — atropine from *Atropa belladonna*,
hyoscine from *Hyoscyamus niger*, *Withania somnifera* (ashwagandha);
**narcotic** — nicotine from *Nicotiana tabacum*; **ornamental** — *Petunia*,
*Cestrum nocturnum*. Credit is also given for noting that the family is rich in
**alkaloids**, so that *Datura* seeds and the green parts of potato are poisonous.

**2.** *Diagram*: a circular flow diagram with the haploid half and the diploid
half distinguished, as in the figure in section 2.5. *Description*: the spore
(n) germinates on damp soil into a green, branched, filamentous **protonema**
(n), which buds to produce the erect **leafy gametophyte** (n) anchored by
multicellular rhizoids. At its apex the gametophyte bears clusters of
**antheridia** (producing biflagellate antherozoids) and, on another branch,
flask-shaped **archegonia** each with one egg. **Water is essential**: the
antherozoids swim down the mucilage-filled neck and one fuses with the egg —
**fertilisation**, the point at which ploidy doubles — giving a **zygote (2n)**.
The zygote divides *in situ* into an embryo and then the **sporophyte (2n)** of
**foot** (embedded in the gametophyte, absorbing food), **seta** and
**capsule**. Inside the capsule the spore mother cells (2n) undergo **meiosis**,
the point at which ploidy halves, giving haploid **spores** that are flicked out
by the hygroscopic **peristome teeth** when the operculum falls. The cycle is
therefore a **heteromorphic alternation of generations** with the gametophyte
dominant. *Difference in the fern*: the two generations swap importance. In
*Dryopteris* the **sporophyte is the large, long-lived, independent plant** with
true roots, stem and leaves and with vascular tissue, while the gametophyte is
reduced to a small, short-lived, heart-shaped **prothallus** that is quite
independent of the sporophyte. Spores are produced in **sporangia grouped in
sori** on the underside of the frond, protected by an indusium and thrown out by
the **annulus**, not by peristome teeth; and the young fern sporophyte is at
first nourished by the prothallus but soon becomes free-living, whereas the moss
sporophyte never becomes independent. Water is still needed for fertilisation in
both.
:::
