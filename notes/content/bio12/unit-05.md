---
subject: Biology
grade: 12
unit: 5
title: Biotechnology
hours: 7
area: Botany
---

Biotechnology is the use of living organisms, or parts of them, to make
products and services that people need. It is old — curd, *gundruk*, *jaand*
and *chhurpi* are all biotechnology — but since the 1970s the ability to cut
and rejoin DNA has turned it into the fastest-moving branch of biology. This
unit covers what plant biotechnology can actually do: grow a whole plant from a
few cells, breed better crops, build disease resistance, replace chemicals with
living fertilisers and pesticides, move a gene from one species to another, and
help keep a country's food both sufficient and safe.

::: key What the examiner asks from this unit
Long questions come from **tissue culture** (steps plus applications) and
**genetic engineering** (tools, steps of recombinant DNA technology, and GMOs
with named examples). Short questions come from **bio-fertilizers and
bio-pesticides** (name the organism, name what it does), **Bt crops** and the
**difference between food safety and food security**. Learn the named organisms
and the named enzymes — marks here are given for the right name, not for
general description.
:::

## 5.1 Tissue culture

::: definition Plant tissue culture
Plant tissue culture is the growth of cells, tissues or organs of a plant on a
sterile, chemically defined nutrient medium under controlled conditions of
temperature, light and humidity — that is, *in vitro*. It rests on
**totipotency**, the ability of a single living plant cell to divide and
regenerate a complete plant.
:::

Totipotency was proposed by **Haberlandt in 1902** and first demonstrated by
**F. C. Steward in 1957**, who grew whole carrot plants (*Daucus carota*) from
single phloem cells suspended in coconut water.

### The medium

The standard medium is **MS medium (Murashige and Skoog, 1962)**. It contains:

| Component | Examples | Role |
|---|---|---|
| Macronutrients | N, P, K, Ca, Mg, S salts | bulk nutrition |
| Micronutrients | Fe, Mn, Zn, B, Cu, Mo | enzyme cofactors |
| Carbon source | sucrose, 2–3 % | energy (cultures are not photosynthetic) |
| Vitamins | thiamine, nicotinic acid, pyridoxine, myo-inositol | growth factors |
| Amino acid | glycine | nitrogen source |
| Growth regulators | **auxin** (IAA, NAA, 2,4-D) and **cytokinin** (kinetin, BAP) | control what the tissue becomes |
| Gelling agent | agar, 0.8 % | support |

The **ratio of auxin to cytokinin** decides the result (Skoog and Miller, 1957):
a **high auxin : low cytokinin** ratio makes **roots**, a **low auxin : high
cytokinin** ratio makes **shoots**, and a roughly equal ratio keeps the tissue
as an unorganised mass of dividing cells, the **callus**.

### The steps

1. **Choice of explant** — a small piece of tissue (shoot tip, node, leaf disc,
   anther, embryo) from a healthy, disease-free mother plant.
2. **Surface sterilisation** — 70 % ethanol for a few seconds, then 0.1 %
   mercuric chloride or 1 % sodium hypochlorite, followed by several rinses in
   sterile distilled water.
3. **Inoculation** — the explant is transferred aseptically to the medium inside
   a laminar air-flow cabinet.
4. **Callus formation and multiplication** — incubation at about 25 °C with a
   16-hour photoperiod; the callus is subcultured every 3–4 weeks.
5. **Organogenesis** — the callus is shifted to a high-cytokinin medium to make
   shoots, then to a high-auxin medium to make roots.
6. **Hardening (acclimatisation)** — the tiny plantlets are moved to a
   greenhouse with high humidity, then gradually to normal conditions.
7. **Transfer to the field.**

```figure caption="The steps of micropropagation, from explant to field-ready plant."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon, FancyBboxPatch, Rectangle
fig, ax = plt.subplots(figsize=(5.2, 3.2))
FS = 5.7
X = [0.75 + 2.20*k for k in range(3)]
Y1, Y2 = 1.15, -1.15
def tube(cx, cy, w=0.72, h=1.05, fc='#f6efdc'):
    ax.add_patch(FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                                boxstyle='round,pad=0.02,rounding_size=0.16',
                                fc='#ffffff', ec=INK, lw=1.1, zorder=3))
    ax.add_patch(Rectangle((cx - w/2 + 0.04, cy - h/2 + 0.04), w - 0.08, 0.30,
                           fc=fc, ec='none', zorder=4))
def cap(x, y, txt):
    ax.text(x, y, txt, ha='center', va='top', fontsize=FS, color=INK, linespacing=1.35)
def arr(x0, y0, x1, y1):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.0, mutation_scale=10))
# 1 mother plant + explant
ax.plot([X[0], X[0]], [Y1 - 0.55, Y1 + 0.35], color='#4f7a42', lw=1.8, zorder=3)
for s in (-1, 1):
    ax.add_patch(Ellipse((X[0] + s*0.26, Y1 + 0.02), 0.44, 0.24, angle=s*22,
                         fc='#cfe3d4', ec='#4f7a42', lw=0.9, zorder=3))
    ax.add_patch(Ellipse((X[0] + s*0.24, Y1 - 0.34), 0.40, 0.22, angle=s*22,
                         fc='#cfe3d4', ec='#4f7a42', lw=0.9, zorder=3))
ax.add_patch(Circle((X[0], Y1 + 0.42), 0.11, fc='#f3cfcb', ec='#b5544f', lw=1.0, zorder=4))
ax.annotate('explant (shoot tip)', xy=(X[0] + 0.11, Y1 + 0.46), xytext=(X[0] - 0.98, Y1 + 0.80),
            fontsize=FS, color=INK, ha='left',
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7))
cap(X[0], Y1 - 0.72, '1. mother plant,\nexplant cut off')
arr(X[0] + 0.55, Y1, X[1] - 0.50, Y1)
# 2 sterilise + inoculate
tube(X[1], Y1)
ax.add_patch(Circle((X[1], Y1 - 0.26), 0.11, fc='#f3cfcb', ec='#b5544f', lw=1.0, zorder=5))
ax.annotate('sterile MS medium', xy=(X[1], Y1 - 0.40), xytext=(X[1], Y1 + 0.80),
            fontsize=FS, color=INK, ha='center',
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7))
cap(X[1], Y1 - 0.72, '2. sterilised and\ninoculated')
arr(X[1] + 0.50, Y1, X[2] - 0.50, Y1)
# 3 callus
tube(X[2], Y1)
rng = np.random.default_rng(3)
for _ in range(16):
    r, th = 0.19*np.sqrt(rng.random()), rng.random()*2*np.pi
    ax.add_patch(Circle((X[2] + r*np.cos(th), Y1 - 0.20 + 0.7*r*np.sin(th)), 0.055,
                        fc='#e5d6a8', ec='#a6802f', lw=0.5, zorder=5))
cap(X[2], Y1 - 0.72, '3. callus\n(high 2,4-D)')
arr(X[2] + 0.62, Y1 - 0.25, X[2] + 0.62, Y2 + 0.25)
# 4 shoots  (row 2 runs right to left)
tube(X[2], Y2)
for s, dx in ((-1, -0.16), (0, 0.0), (1, 0.16)):
    ax.plot([X[2] + dx, X[2] + dx*1.5], [Y2 - 0.26, Y2 + 0.30], color='#4f7a42', lw=1.3,
            zorder=5)
    ax.add_patch(Ellipse((X[2] + dx*1.7, Y2 + 0.33), 0.22, 0.13, angle=s*25,
                         fc='#cfe3d4', ec='#4f7a42', lw=0.8, zorder=5))
cap(X[2], Y2 - 0.72, '4. shoots\n(high cytokinin)')
arr(X[2] - 0.50, Y2, X[1] + 0.50, Y2)
# 5 roots
tube(X[1], Y2)
ax.plot([X[1], X[1]], [Y2 - 0.26, Y2 + 0.34], color='#4f7a42', lw=1.4, zorder=5)
ax.add_patch(Ellipse((X[1] - 0.16, Y2 + 0.34), 0.24, 0.14, angle=22, fc='#cfe3d4',
                     ec='#4f7a42', lw=0.8, zorder=5))
ax.add_patch(Ellipse((X[1] + 0.16, Y2 + 0.34), 0.24, 0.14, angle=-22, fc='#cfe3d4',
                     ec='#4f7a42', lw=0.8, zorder=5))
for dx in (-0.13, 0.0, 0.13):
    ax.plot([X[1], X[1] + dx], [Y2 - 0.26, Y2 - 0.44], color='#8b6a3f', lw=1.0, zorder=5)
cap(X[1], Y2 - 0.72, '5. roots\n(high auxin)')
arr(X[1] - 0.50, Y2, X[0] + 0.50, Y2)
# 6 hardening / field
ax.add_patch(Polygon([(X[0] - 0.34, Y2 - 0.44), (X[0] + 0.34, Y2 - 0.44),
                      (X[0] + 0.26, Y2 - 0.04), (X[0] - 0.26, Y2 - 0.04)], closed=True,
                     fc='#e0c3a2', ec=INK, lw=1.0, zorder=3))
ax.plot([X[0], X[0]], [Y2 - 0.04, Y2 + 0.44], color='#4f7a42', lw=1.6, zorder=4)
for s in (-1, 1):
    ax.add_patch(Ellipse((X[0] + s*0.22, Y2 + 0.42), 0.36, 0.18, angle=s*24,
                         fc='#cfe3d4', ec='#4f7a42', lw=0.9, zorder=4))
    ax.add_patch(Ellipse((X[0] + s*0.19, Y2 + 0.16), 0.32, 0.16, angle=s*24,
                         fc='#cfe3d4', ec='#4f7a42', lw=0.9, zorder=4))
cap(X[0], Y2 - 0.60, '6. hardened, then\nplanted out')
ax.set_xlim(-0.56, 6.46); ax.set_ylim(-2.35, 2.05); ax.set_aspect('equal'); ax.axis('off')
```
### Kinds of culture and what they are used for

| Culture | What is grown | Chief use |
|---|---|---|
| **Callus culture** | unorganised mass on solid medium | starting point for regeneration; somaclonal variation |
| **Suspension culture** | free cells in shaken liquid | industrial production of secondary metabolites |
| **Meristem / shoot-tip culture** | the 0.2–0.5 mm apical dome | **virus-free plants**, because viruses do not reach the meristem |
| **Anther / pollen culture** | microspores | **haploid plants**; doubling with colchicine gives instantly homozygous lines |
| **Embryo culture (embryo rescue)** | a young hybrid embryo | saves wide-cross hybrids that would abort in the seed |
| **Protoplast culture** | wall-less cells made by cellulase and pectinase | **somatic hybridisation** — the "pomato" from potato + tomato protoplasts |

**Applications.** Micropropagation multiplies elite plants by the thousand —
banana, orchid, potato, sugarcane and strawberry are produced this way in
commercial labs, including in Kathmandu and Chitwan. Meristem culture gives
virus-free seed potato. Cryopreservation in liquid nitrogen at −196 °C conserves
germplasm. Cell suspensions make alkaloids and other secondary metabolites. And
tissue culture is the essential last step of **every** genetic engineering
project in plants: the transformed cell must be regenerated into a whole plant.

Its limits are real too: it is expensive, it needs skilled staff and absolute
asepsis, contamination can destroy a whole batch, and unwanted **somaclonal
variation** can creep in.

::: example 5.1 How fast does micropropagation multiply?
**Problem.** A single shoot-tip explant of banana is subcultured every 4 weeks,
and each subculture multiplies the number of shoots by 4. (a) How many shoots
are available after 24 weeks? (b) If 5 % are lost during hardening, how many
plants reach the field?

**Solution.**

(a) In 24 weeks there are $24 \div 4 = 6$ subcultures, so

$$ N = 1 \times 4^{6} = 4096 \text{ shoots} $$

(b) Survivors $= 4096 \times 0.95 = 3891.2$, that is about **3891 plants**.
From one bud in under six months — which is why the method is used for banana,
whose seeds are useless because it is a sterile triploid.
:::

## 5.2 Plant breeding

::: definition Plant breeding
Plant breeding is the deliberate improvement of the heredity of crop plants for
human benefit — raising yield, quality and resistance — by selecting and
recombining the variation that exists in a species and its relatives.
:::

**Objectives:** higher yield; better quality (more protein, oil, vitamins);
resistance to diseases and pests; tolerance of drought, cold, heat and salinity;
early maturity, so that two or three crops fit into one year; dwarf, stiff-strawed
habit that does not lodge under heavy fertiliser; and suitability for machinery.

**The steps of a breeding programme:**

1. **Collection of germplasm** — gathering landraces, wild relatives and released
   varieties into a gene bank.
2. **Evaluation and selection of parents** — screening the collection for the
   desired character.
3. **Hybridisation** — the chosen female parent is **emasculated** (its anthers
   removed before they dehisce) and **bagged**; when the stigma is receptive,
   pollen from the male parent is dusted on and the flower is bagged and tagged
   again.
4. **Selection among the progeny** — the F₁ is selfed and superior recombinants
   are selected from the F₂ onwards, generation after generation.
5. **Testing, release and multiplication** — yield trials at several sites over
   several years, then release by the National Seed Board and multiplication of
   certified seed.

**Methods of breeding:** **introduction** of a variety from elsewhere;
**selection** (mass selection, pure-line selection, clonal selection);
**hybridisation** (intervarietal, interspecific, intergeneric);
**mutation breeding** with gamma rays or EMS; **polyploidy breeding** with
colchicine; and, most recently, **marker-assisted selection**, in which DNA
markers linked to a useful gene let the breeder pick the right seedling in the
laboratory instead of waiting for the adult plant.

The **Green Revolution** of the 1960s was plant breeding on a national scale:
**Norman Borlaug's** semi-dwarf, rust-resistant wheats and IRRI's **IR8** rice
(1966) roughly doubled cereal yields in South Asia. Nepal's own programme, run
by the **Nepal Agricultural Research Council (NARC)**, has released wheat
varieties such as **Bhrikuti** (1994) and **Gautam**, rice varieties such as
**Sabitri**, **Radha-4** and **Khumal-4**, and maize varieties such as **Rampur
Composite** and **Manakamana-3**.

Two ideas underlie hybrid breeding. **Heterosis (hybrid vigour)** is the
superiority of an F₁ hybrid over both its parents in size, yield and vigour;
**inbreeding depression** is the opposite loss of vigour when a
cross-pollinating crop such as maize is repeatedly selfed. Hybrid seed must
therefore be bought fresh each season, because the F₂ segregates and the vigour
is lost.

**Biofortification** is the newest objective: breeding varieties that are richer
in iron, zinc, protein or vitamins, so that nutrition improves without anyone
having to change what they eat.

## 5.3 Disease-resistant plants

A plant is **resistant** when it can prevent or limit infection by a pathogen.
Resistance is of two kinds:

| | Vertical (race-specific) resistance | Horizontal (field) resistance |
|---|---|---|
| Genetic basis | one or a few major genes | many genes, each of small effect |
| Effect | complete immunity to *some* races | partial protection against *all* races |
| Durability | breaks down when a new race appears | durable |
| Inheritance | simple, easy to breed | difficult to breed |

The **gene-for-gene hypothesis** (H. H. Flor, 1956) explains vertical
resistance: for every resistance (R) gene in the host there is a matching
avirulence (Avr) gene in the pathogen, and the plant resists only when both are
present.

**Sources of resistance genes** are wild relatives and old landraces, which is
why gene banks matter: the terraces of Nepal's mid-hills still hold rice and
barley landraces carrying genes that modern varieties have lost.

**Methods of producing resistant plants:**

- **Conventional breeding**, usually by the **backcross method** — the resistance
  gene is crossed into a good variety, and the hybrid is repeatedly backcrossed
  to that variety so that only the resistance gene is retained.
- **Mutation breeding** — mildew-resistant barley (the *mlo* mutants) came this
  way.
- **Genetic engineering**, which can bring in a gene from any organism at all.

The best-known transgenic resistance uses the **cry genes** of the soil
bacterium *Bacillus thuringiensis*.

::: key How the Bt toxin works
*B. thuringiensis* makes the toxin as an inactive **crystal protoxin**, which is
why it is harmless to the bacterium itself and to us. When a caterpillar eats
it, the **alkaline pH of the insect midgut** dissolves the crystal, gut
proteases cut it into the active toxin, the toxin binds to specific receptors on
the midgut epithelium and punches pores in the cells. The cells swell, burst,
and the larva stops feeding and dies. Our stomachs are acidic and have no such
receptors, so the toxin passes through us unchanged.
:::

| Transgene | Source | Protects against | Crop |
|---|---|---|---|
| *cry1Ac*, *cry2Ab* | *Bacillus thuringiensis* | cotton bollworm | Bt cotton |
| *cry1Ab* | *Bacillus thuringiensis* | maize stem borer | Bt maize |
| *cry1Ac* | *Bacillus thuringiensis* | brinjal fruit-and-shoot borer | Bt brinjal |
| viral coat protein gene | papaya ringspot virus | the virus itself | virus-resistant papaya |
| chitinase, glucanase | fungi, plants | fungal pathogens | several |
| RNA interference construct | the nematode's own gene | root-knot nematode *Meloidogyne incognita* | tobacco |

Bt cotton was approved for commercial planting in India by the GEAC in **2002**
and now covers roughly 90 % of the cotton area there. **Bt brinjal** was
approved by Bangladesh's National Committee on Biosafety on **30 October 2013**
and has been grown there since 2014 — the first genetically engineered food crop
released in South Asia.

## 5.4 Green manure, bio-fertilizer, bio-pesticide

### Green manure

::: definition Green manure
Green manure is undecomposed green plant material — usually a quick-growing
legume — that is grown in a field and then ploughed into the same soil while
still green, to enrich it with nitrogen and organic matter.
:::

The common green-manure crops are **dhaincha** *Sesbania aculeata*, **sunn hemp**
*Crotalaria juncea*, cowpea *Vigna unguiculata*, guar *Cyamopsis tetragonoloba*
and *Trifolium*. When the leaves of a tree are cut and carried to a field
instead, it is called **green-leaf manure** — in Nepal the leaves of
*Azadirachta indica* (neem), *Gliricidia* and *Artocarpus* are used this way.

Green manuring adds nitrogen (a good dhaincha crop can add 60–90 kg N per
hectare), raises the organic-matter content, improves soil structure and
water-holding capacity, encourages soil microbes, suppresses weeds and checks
erosion between crops.

### Bio-fertilizers

A **bio-fertilizer** is a preparation of living micro-organisms that, when
applied to seed, soil or root, increases the supply of nutrients to the plant.
It does not itself contain the nutrient; it makes the nutrient available.

| Group | Organism | What it does |
|---|---|---|
| Symbiotic N-fixers | *Rhizobium* in legume root nodules | fixes atmospheric N₂ |
| | *Frankia* in *Alnus nepalensis* (utis) | fixes N₂ in a non-legume tree |
| | *Anabaena azollae* inside the fern *Azolla* | classic bio-fertilizer of paddy fields |
| Free-living N-fixers | *Azotobacter* (aerobic), *Clostridium* (anaerobic) | fix N₂ in the soil |
| Associative N-fixer | *Azospirillum* | lives around the roots of cereals |
| Blue-green algae | *Nostoc*, *Anabaena*, *Aulosira* | fix N₂ in flooded rice fields |
| Phosphate solubilisers | *Bacillus megaterium*, *Pseudomonas striata*, *Aspergillus* | release insoluble soil phosphate as acids |
| Mycorrhiza | vesicular-arbuscular mycorrhiza, *Glomus* | greatly extends the root surface for **phosphorus** and water uptake |

### Bio-pesticides

A **bio-pesticide** is a living organism, or a substance obtained from one, used
to control pests.

| Type | Agent | Target |
|---|---|---|
| Bacterial | *Bacillus thuringiensis* | caterpillars (Lepidoptera) |
| Fungal | *Trichoderma viride*, *T. harzianum* | soil-borne fungal diseases |
| | *Beauveria bassiana*, *Metarhizium anisopliae* | many insects |
| Viral | nuclear polyhedrosis virus (NPV) | *Helicoverpa*, *Spodoptera* |
| Botanical | neem *Azadirachta indica* (azadirachtin) | broad-spectrum antifeedant |
| | pyrethrum *Chrysanthemum cinerariifolium*, *Derris* (rotenone) | many insects |
| Predator / parasitoid | *Trichogramma* wasp, ladybird beetle | eggs of borers, aphids |

Compared with chemical pesticides, bio-pesticides are **specific** (they spare
bees, birds and natural enemies), **biodegradable** so they leave no residue on
food, and they do not accumulate along food chains or cause resistance as
quickly. Against that, they act slowly, they are sensitive to sunlight and
temperature, and they have a short shelf life.

::: caution "Bio-fertilizer" is not the same as "manure"
Manure and compost *supply* nutrients directly. A bio-fertilizer supplies
almost no nutrients itself — it is a culture of **living organisms** that fix
nitrogen or unlock phosphate. If a question asks for a bio-fertilizer, the
answer must be an **organism** (*Rhizobium*, *Azolla*, *Glomus*), not a
substance.
:::

## 5.5 Genetic engineering and GMOs

::: definition Genetic engineering
Genetic engineering is the deliberate alteration of an organism's genome by
isolating a gene, joining it to a carrier DNA molecule *in vitro* and
introducing it into a living cell, so that the cell expresses a character it
could never have obtained by breeding. Because the DNA made in the test tube
combines pieces from two sources, it is called **recombinant DNA**, and the
method is **recombinant DNA (rDNA) technology**.
:::

### The tools

**1. Restriction endonucleases — the molecular scissors.** These bacterial
enzymes recognise a short **palindromic** sequence of 4–8 base pairs and cut the
DNA within it. *Eco*RI, from *Escherichia coli* strain RY13, recognises
G↓AATTC and cuts between G and A on both strands, leaving four-base single-stranded
**sticky (cohesive) ends** that can base-pair with any other fragment cut by the
same enzyme. Some enzymes, such as *Sma*I, cut straight across and give **blunt
ends**. Arber, Nathans and Smith shared the 1978 Nobel Prize for this discovery.

**2. DNA ligase — the molecular glue.** It seals the phosphodiester backbone
between the joined fragments.

**3. Vectors — the carriers.** A good vector needs an **origin of replication
(*ori*)** so that it multiplies in the host, **selectable marker genes** such as
antibiotic resistance so that transformed cells can be picked out, and **unique
restriction sites** where the foreign gene can be slotted in. The commonest are
**plasmids** — small circular extra-chromosomal DNA of bacteria, such as
**pBR322** — along with bacteriophages, cosmids and, for plants, the **Ti
plasmid of *Agrobacterium tumefaciens***, a natural genetic engineer that
normally inserts its own T-DNA into plant cells and causes crown gall.

**4. Host cells** — *Escherichia coli*, yeast, or the plant cell itself.

```figure caption="(a) A plasmid vector with unique restriction sites, an origin of replication and two marker genes. (b) EcoRI cuts the palindrome GAATTC and leaves sticky ends."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc
fig, axs = plt.subplots(1, 2, figsize=(5.2, 2.9),
                        gridspec_kw=dict(width_ratios=[1.0, 1.25], wspace=0.05))
# ---------------- (a) plasmid map ----------------
ax = axs[0]
R = 1.0
ax.add_patch(Circle((0, 0), R, fill=False, ec=INK, lw=1.4, zorder=3))
ax.add_patch(Circle((0, 0), R - 0.085, fill=False, ec=INK, lw=1.0, zorder=3))
def place(a, r, txt, col, fs=6.6):
    t = np.deg2rad(a); c, s = np.cos(t), np.sin(t)
    ha = 'left' if c > 0.15 else ('right' if c < -0.15 else 'center')
    va = 'bottom' if s > 0.45 else ('top' if s < -0.45 else 'center')
    ax.text(r*c, r*s, txt, fontsize=fs, color=col, ha=ha, va=va, style='italic')
def arc(a0, a1, col, name, rr=R - 0.042):
    th = np.deg2rad(np.linspace(a0, a1, 80))
    ax.plot(rr*np.cos(th), rr*np.sin(th), color=col, lw=5.0, solid_capstyle='butt',
            zorder=4)
    place((a0 + a1)/2, 1.14, name, col)
arc(18, 98, SERIES[2], 'amp$^R$')
arc(196, 286, SERIES[1], 'tet$^R$')
am = np.deg2rad(330)
ax.plot([0.86*np.cos(am)], [0.86*np.sin(am)], marker='o', ms=5, color=ACCENT, zorder=5)
place(330, 1.14, 'ori', ACCENT)
for a, name in ((118, 'EcoRI'), (148, 'HindIII'), (176, 'BamHI'), (300, 'PstI')):
    t = np.deg2rad(a)
    ax.plot([0.88*np.cos(t), 1.14*np.cos(t)], [0.88*np.sin(t), 1.14*np.sin(t)],
            color='#d9534f', lw=1.3, zorder=5)
    place(a, 1.20, name, '#d9534f', fs=6.3)
ax.text(0, 0, 'plasmid\nvector', fontsize=6.8, color=MUTED, ha='center', va='center',
        linespacing=1.35)
ax.set_title('(a) plasmid vector', fontsize=7.8, loc='left', pad=4)
ax.set_xlim(-2.05, 2.05); ax.set_ylim(-2.15, 2.15); ax.set_aspect('equal'); ax.axis('off')
# ---------------- (b) EcoRI cut ----------------
ax = axs[1]
S = 0.36
def strand(letters, x0, y, col=INK):
    for i, L in enumerate(letters):
        ax.text(x0 + i*S, y, L, fontsize=8.0, color=col, ha='center', va='center',
                family='monospace')
strand('GAATTC', 0.0, 2.32)
strand('CTTAAG', 0.0, 1.86)
for i in range(6):
    ax.plot([i*S, i*S], [2.16, 2.02], color=MUTED, lw=0.7)
ax.text(-0.42, 2.32, '5′', fontsize=6.6, color=MUTED, ha='center', va='center')
ax.text(-0.42, 1.86, '3′', fontsize=6.6, color=MUTED, ha='center', va='center')
ax.text(5*S + 0.42, 2.32, '3′', fontsize=6.6, color=MUTED, ha='center', va='center')
ax.text(5*S + 0.42, 1.86, '5′', fontsize=6.6, color=MUTED, ha='center', va='center')
ax.plot([0.5*S, 0.5*S, 4.5*S, 4.5*S], [2.52, 2.09, 2.09, 1.66], color='#d9534f', lw=1.4,
        zorder=5)
ax.text(2.5*S, 2.66, 'EcoRI cuts here', fontsize=6.4, color='#d9534f', ha='center')
ax.annotate('', xy=(2.5*S, 1.14), xytext=(2.5*S, 1.50),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.0, mutation_scale=10))
XR = 1.94
strand('G', 0.0, 0.86)
strand('CTTAA', 0.0, 0.40)
strand('AATTC', XR, 0.86)
strand('G', XR + 4*S, 0.40)
ax.text(-0.42, 0.86, '5′', fontsize=6.6, color=MUTED, ha='center', va='center')
ax.text(-0.42, 0.40, '3′', fontsize=6.6, color=MUTED, ha='center', va='center')
ax.text(XR + 4*S + 0.42, 0.86, '3′', fontsize=6.6, color=MUTED, ha='center', va='center')
ax.text(XR + 4*S + 0.42, 0.40, '5′', fontsize=6.6, color=MUTED, ha='center', va='center')
ax.annotate('sticky ends — four unpaired\nbases that will pair with any\nfragment cut by EcoRI',
            xy=(2.2*S, 0.34), xytext=(1.72, -0.18), fontsize=6.3, color=INK, ha='center',
            va='top', linespacing=1.35,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7))
ax.set_title('(b) EcoRI and sticky ends', fontsize=7.8, loc='left', pad=4)
ax.set_xlim(-1.05, 3.90); ax.set_ylim(-1.10, 3.00); ax.set_aspect('equal'); ax.axis('off')
```

### Steps of recombinant DNA technology

1. **Isolation of DNA.** The cells of the donor organism are broken open with
   lysozyme (bacteria) or cellulase (plant cells), the proteins are digested
   with protease and the RNA removed with ribonuclease. Chilled ethanol is then
   added; the DNA separates out as fine white threads that can be spooled on a
   glass rod.
2. **Cutting.** The donor DNA and the vector are cut with the **same**
   restriction enzyme, so that both carry complementary sticky ends.
3. **Ligation.** The gene of interest and the cut vector are mixed. Their sticky
   ends base-pair, and DNA ligase seals the nicks. The product is
   **recombinant DNA (rDNA)**.
4. **Transformation.** The rDNA is pushed into a host cell.
5. **Selection and screening.** Only a few host cells actually take up the
   rDNA, so the marker genes are used to pick them out (see below).
6. **Multiplication and downstream processing.** The selected cell is grown in
   a fermenter or regenerated into a whole plant, and the product — protein,
   metabolite or transgenic plantlet — is harvested and purified.

::: definition Cloning vector versus gene cloning
A **vector** is the DNA molecule that carries the foreign gene into the host.
**Gene cloning** is the production of many identical copies of one gene by
multiplying the host cell that carries it.
:::

**Methods of transferring DNA into the host**

| Method | How it works | Chiefly used for |
|---|---|---|
| CaCl₂ + heat shock | Ca²⁺ makes the bacterial wall porous; a 42 °C pulse draws plasmid in | *E. coli* |
| Electroporation | A brief high-voltage pulse opens transient pores in the membrane | bacteria, protoplasts |
| Microinjection | DNA injected into the nucleus with a fine glass needle | animal cells, eggs |
| Gene gun (biolistics) | Gold or tungsten particles coated with DNA fired at cells | monocots, chloroplasts |
| *Agrobacterium* method | T-DNA of the Ti plasmid is transferred naturally into the plant genome | dicots |

**Selection.** In pBR322 the gene is inserted into *tet*ᴿ. Cells carrying the
recombinant plasmid have a working *amp*ᴿ but a broken *tet*ᴿ, so they grow on
ampicillin but die on tetracycline — this is **insertional inactivation**.
Modern vectors use *lacZ* instead: recombinant colonies cannot make
β-galactosidase and stay **white**, while non-recombinants turn **blue** on
X-gal. This is called blue–white screening.

```figure caption="The six steps of recombinant DNA technology, from isolating the donor DNA to harvesting the product."
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Polygon
fig, ax = plt.subplots(figsize=(5.2, 3.2))
X = [0.85 + 2.35*k for k in range(3)]
Y1, Y2 = 1.16, -1.22
R = 0.50

def cap(x, y, lines):
    for i, s in enumerate(lines):
        ax.text(x, y - 0.30*i, s, fontsize=5.9, color=INK, ha='center', va='top')

def num(x, y, n):
    ax.add_patch(Circle((x - R - 0.20, y + R + 0.02), 0.16, fc=ACCENT, ec='none', zorder=6))
    ax.text(x - R - 0.20, y + R + 0.02, str(n), fontsize=6.0, color='white',
            ha='center', va='center', zorder=7)

# 1 donor cell with DNA
ax.add_patch(Circle((X[0], Y1), R, fc='#eef4fb', ec=INK, lw=1.1))
t = np.linspace(0, 2.6*np.pi, 200)
ax.plot(X[0] - 0.30 + 0.60*t/(2.6*np.pi), Y1 + 0.16*np.sin(t), color=SERIES[0], lw=1.2)
ax.plot(X[0] - 0.30 + 0.60*t/(2.6*np.pi), Y1 + 0.16*np.sin(t + np.pi), color=SERIES[0], lw=1.2)
num(X[0], Y1, 1); cap(X[0], Y1 - R - 0.14, ['isolate DNA from', 'the donor cell'])

# 2 cutting
ax.plot([X[1] - 0.44, X[1] + 0.44], [Y1 + 0.22, Y1 + 0.22], color=SERIES[0], lw=3.2,
        solid_capstyle='butt')
ax.plot([X[1] - 0.06, X[1] - 0.06], [Y1 + 0.02, Y1 + 0.42], color='#d9534f', lw=1.3)
ax.plot([X[1] + 0.22, X[1] + 0.22], [Y1 + 0.02, Y1 + 0.42], color='#d9534f', lw=1.3)
ax.add_patch(Circle((X[1], Y1 - 0.30), 0.27, fc='none', ec=INK, lw=1.1))
ax.plot([X[1] + 0.27, X[1] + 0.27], [Y1 - 0.50, Y1 - 0.10], color='#d9534f', lw=1.3)
ax.text(X[1] + 0.50, Y1 + 0.22, 'gene', fontsize=5.7, color=SERIES[0], ha='left', va='center')
ax.text(X[1] + 0.42, Y1 - 0.40, 'vector', fontsize=5.7, color=MUTED, ha='left', va='center')
num(X[1], Y1, 2); cap(X[1], Y1 - R - 0.14, ['cut both with the', 'same enzyme'])

# 3 ligation
ax.add_patch(Circle((X[2], Y1), 0.36, fc='none', ec=INK, lw=1.4))
th = np.deg2rad(np.linspace(40, 140, 60))
ax.plot(0.36*np.cos(th) + X[2], 0.36*np.sin(th) + Y1, color=SERIES[0], lw=3.0)
ax.text(X[2], Y1 + 0.52, 'insert', fontsize=5.7, color=SERIES[0], ha='center', va='bottom')
num(X[2], Y1, 3); cap(X[2], Y1 - R - 0.14, ['seal with DNA', 'ligase'])

def arrow(x0, y0, x1, y1):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.2, mutation_scale=10))
arrow(X[0] + 0.62, Y1, X[1] - 0.68, Y1)
arrow(X[1] + 0.68, Y1, X[2] - 0.62, Y1)
ax.plot([X[2] + 0.52, X[2] + 0.92, X[2] + 0.92], [Y1, Y1, Y2 + 0.04], color=ACCENT, lw=1.2,
        solid_joinstyle='round')
arrow(X[2] + 0.92, Y2, X[2] + 0.60, Y2)
arrow(X[2] - 0.62, Y2, X[1] + 0.62, Y2)
arrow(X[1] - 0.62, Y2, X[0] + 0.62, Y2)

# 4 transformation
ax.add_patch(FancyBboxPatch((X[2] - 0.40, Y2 - 0.24), 0.80, 0.48,
                            boxstyle='round,pad=0.10,rounding_size=0.22',
                            fc='#eef4fb', ec=INK, lw=1.1))
ax.add_patch(Circle((X[2] + 0.06, Y2), 0.14, fc='none', ec=SERIES[0], lw=1.3))
ax.annotate('', xy=(X[2] - 0.26, Y2 + 0.06), xytext=(X[2] - 0.72, Y2 + 0.30),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.9, mutation_scale=9))
num(X[2], Y2, 4); cap(X[2], Y2 - R - 0.14, ['transfer into a', 'host cell'])

# 5 selection
ax.add_patch(Circle((X[1], Y2), 0.44, fc='#f6f8fb', ec=INK, lw=1.1))
rng = [(-0.20, 0.16), (0.12, 0.22), (0.20, -0.12), (-0.14, -0.20), (0.00, 0.02)]
for i, (dx, dy) in enumerate(rng):
    ax.add_patch(Circle((X[1] + dx, Y2 + dy), 0.075,
                        fc=(SERIES[0] if i < 2 else '#ffffff'), ec=INK, lw=0.7))
num(X[1], Y2, 5); cap(X[1], Y2 - R - 0.14, ['select transformants', 'on marker medium'])

# 6 product
ax.add_patch(Polygon([[X[0] - 0.30, Y2 + 0.40], [X[0] + 0.30, Y2 + 0.40],
                      [X[0] + 0.42, Y2 - 0.36], [X[0] - 0.42, Y2 - 0.36]],
                     closed=True, fc='#eef4fb', ec=INK, lw=1.1))
ax.add_patch(Polygon([[X[0] - 0.36, Y2 + 0.06], [X[0] + 0.36, Y2 + 0.06],
                      [X[0] + 0.42, Y2 - 0.36], [X[0] - 0.42, Y2 - 0.36]],
                     closed=True, fc=SERIES[0], ec='none', alpha=0.45))
num(X[0], Y2, 6); cap(X[0], Y2 - R - 0.14, ['multiply and harvest', 'the product'])

ax.set_xlim(-0.35, 6.95); ax.set_ylim(-2.62, 1.92); ax.set_aspect('equal'); ax.axis('off')
```

### The polymerase chain reaction (PCR)

PCR, devised by **Kary Mullis in 1983** (Nobel Prize 1993), makes millions of
copies of one chosen stretch of DNA *in vitro*, without any host cell. The
reaction tube contains the template DNA, two short primers (about 18–25
nucleotides) that flank the target, the four dNTPs, Mg²⁺ buffer and a
heat-stable DNA polymerase — **Taq polymerase**, isolated from the hot-spring
bacterium *Thermus aquaticus*, which survives 95 °C. A thermal cycler then
repeats three temperature steps:

| Step | Temperature | What happens |
|---|---|---|
| Denaturation | 94–95 °C, 30 s | hydrogen bonds break; the duplex separates into two strands |
| Annealing | 50–65 °C, 30 s | primers base-pair with their complementary sites |
| Extension | 72 °C, ~1 min per kb | Taq polymerase adds dNTPs 5′ → 3′ from each primer |

Each cycle doubles the number of target molecules, so after $n$ cycles one
molecule becomes $2^n$ copies. Thirty cycles take about two hours and give over
a billion copies. PCR is used in disease diagnosis, DNA fingerprinting,
prenatal testing, detecting GM material in imported grain, and amplifying a
gene before cloning it.

```figure caption="PCR. (a) The three temperature steps of one cycle, repeated by the thermal cycler. (b) Each cycle doubles the target, so $n$ cycles give $2^n$ copies."
import numpy as np
fig, (ax, bx) = plt.subplots(1, 2, figsize=(5.2, 2.9), gridspec_kw={'width_ratios': [1.25, 1.0]})

T, Y = [], []
for c in range(3):
    t0 = 4.6*c
    for dt, v in [(0.0, 95), (1.0, 95), (1.2, 55), (2.2, 55), (2.4, 72), (4.0, 72), (4.2, 95)]:
        T.append(t0 + dt); Y.append(v)
ax.plot(T, Y, color=ACCENT, lw=1.6, clip_on=True)
for v, lab in [(95, 'denature 94–95 °C'), (55, 'anneal 50–65 °C'), (72, 'extend 72 °C')]:
    ax.axhline(v, color=GRID, lw=0.8, zorder=0)
ax.annotate('denature 94–95 °C', xy=(5.0, 95), xytext=(7.4, 100), fontsize=5.9, color=INK,
            ha='center', arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7))
ax.annotate('anneal 50–65 °C', xy=(1.7, 55), xytext=(3.1, 44), fontsize=5.9, color=INK,
            ha='center', arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7))
ax.annotate('extend 72 °C', xy=(3.2, 72), xytext=(5.6, 63), fontsize=5.9, color=INK,
            ha='center', arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7))
ax.annotate('', xy=(4.2, 106), xytext=(0.0, 106),
            arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=0.9, mutation_scale=8))
ax.text(2.1, 107.5, 'one cycle', fontsize=6.0, color=MUTED, ha='center', va='bottom')
ax.set_xlim(-0.3, 11.2); ax.set_ylim(38, 114)
ax.set_yticks([55, 72, 95]); ax.set_yticklabels(['55', '72', '95'], fontsize=6.4)
ax.set_xticks([])
ax.set_ylabel('temperature (°C)', fontsize=6.6)
ax.set_xlabel('time →', fontsize=6.6)
ax.spines[['top', 'right']].set_visible(False)
ax.set_title('(a) thermal cycle', fontsize=7.6, loc='left', pad=4)

def duplex(x, y, col):
    bx.plot([x - 0.34, x + 0.34], [y + 0.10, y + 0.10], color=col, lw=2.4,
            solid_capstyle='butt')
    bx.plot([x - 0.34, x + 0.34], [y - 0.10, y - 0.10], color=col, lw=2.4,
            solid_capstyle='butt')

rows = [(3.0, 1, '1 copy'), (2.0, 2, '2 copies'), (1.0, 4, '4 copies')]
for y, n, lab in rows:
    for k in range(n):
        duplex(4.0 - 0.85*(n - 1)/2 + 0.85*k, y, SERIES[0] if n == 1 else ACCENT)
    bx.text(-0.55, y, f'cycle {[1, 2, 4].index(n)}', fontsize=6.0, color=MUTED,
            ha='right', va='center')
    bx.text(8.6, y, lab, fontsize=6.0, color=INK, ha='right', va='center')
for y in (2.5, 1.5):
    bx.annotate('', xy=(4.0, y - 0.28), xytext=(4.0, y + 0.28),
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.9, mutation_scale=9))
bx.text(4.0, 0.42, '⋮', fontsize=9, color=MUTED, ha='center', va='center')
bx.text(4.0, -0.15, 'after $n$ cycles: $2^n$ copies', fontsize=6.6, color=INK,
        ha='center', va='center')
bx.set_xlim(-3.2, 8.9); bx.set_ylim(-0.6, 3.7); bx.axis('off')
bx.set_title('(b) exponential amplification', fontsize=7.6, loc='left', pad=4)
fig.subplots_adjust(wspace=0.32)
```

::: example 5.2 How many copies?
**Problem.** A PCR tube starts with 5 copies of a target gene and is run for
30 cycles at 100 % efficiency. How many copies of the target are present at the
end? Roughly how many would 35 cycles give?

**Solution.**
Copies after $n$ cycles $= N_0 \times 2^n$.

$N = 5 \times 2^{30} = 5 \times 1.0737 \times 10^{9} = 5.37 \times 10^{9}$ copies.

For 35 cycles, $N = 5 \times 2^{35} = 5 \times 3.436 \times 10^{10}
= 1.72 \times 10^{11}$ copies.

Five extra cycles multiply the yield by $2^5 = 32$. In practice the enzyme and
the dNTPs run out, so the curve flattens after about 30–35 cycles — this is the
plateau phase.
:::

### Gel electrophoresis

To check that the right fragment has been cut or amplified, the DNA is
separated by **agarose gel electrophoresis**. A slab of agarose gel is laid in
a buffer tank; the samples are loaded into wells at the cathode (−) end.
Because its phosphate groups make DNA **negatively charged at all pH values**,
every fragment moves towards the **anode (+)**. The gel acts as a molecular
sieve: **short fragments thread through the pores quickly and travel far, long
fragments lag behind**, so distance moved is inversely related to the logarithm
of fragment length. The bands are stained with **ethidium bromide** and seen as
orange bands under UV light. Comparing them with a **DNA ladder** of known
sizes run alongside gives the size of each fragment. The wanted band is then
cut out of the gel and the DNA recovered — this is called elution.

```figure caption="Agarose gel electrophoresis. DNA is negatively charged, so it runs from the cathode towards the anode; small fragments travel furthest. Lane M is a ladder of known sizes."
import numpy as np
from matplotlib.patches import Rectangle, FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.8, 3.2))
ax.add_patch(Rectangle((0.0, 0.2), 6.0, 4.9, fc='#f2f5f9', ec=GRID, lw=1.0))
LAD = [10, 5, 3, 1.5, 0.5]

def ypos(kb):
    return 4.35 - 3.30*(np.log10(10.0/kb)/np.log10(10.0/0.5))

lanes = [(0.85, 'M', LAD), (2.20, '1', [9.0]), (3.55, '2', [6.0, 3.0]),
         (4.90, '3', [6.0, 2.0, 1.0])]
for x, name, bands in lanes:
    ax.add_patch(Rectangle((x - 0.42, 4.62), 0.84, 0.30, fc='white', ec=INK, lw=0.9))
    ax.text(x, 5.02, name, fontsize=7.0, color=INK, ha='center', va='bottom')
    for kb in bands:
        ax.add_patch(Rectangle((x - 0.42, ypos(kb) - 0.075), 0.84, 0.15,
                               fc=(MUTED if name == 'M' else ACCENT), ec='none'))
for kb in LAD:
    ax.plot([-0.22, -0.02], [ypos(kb)]*2, color=MUTED, lw=0.8)
    ax.text(-0.34, ypos(kb), f'{kb:g}', fontsize=6.1, color=MUTED, ha='right', va='center')
ax.text(-0.34, 4.86, 'kb', fontsize=6.1, color=INK, ha='right', va='center')
ax.add_patch(FancyBboxPatch((0.6, 5.70), 4.8, 0.16, boxstyle='round,pad=0.05,rounding_size=0.08',
                            fc=INK, ec='none'))
ax.text(3.0, 6.06, 'cathode  −   (wells loaded here)', fontsize=6.3, color=INK,
        ha='center', va='bottom')
ax.add_patch(FancyBboxPatch((0.6, -0.34), 4.8, 0.16, boxstyle='round,pad=0.05,rounding_size=0.08',
                            fc='#d9534f', ec='none'))
ax.text(3.0, -0.60, 'anode  +', fontsize=6.3, color='#d9534f', ha='center', va='top')
ax.annotate('', xy=(6.45, 0.55), xytext=(6.45, 4.35),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.2, mutation_scale=11))
ax.text(6.45, 4.52, 'migration', fontsize=6.3, color=ACCENT, ha='center', va='bottom')
ax.annotate('large fragments\nstay near the wells', xy=(5.35, ypos(6.0)), xytext=(8.15, 3.55),
            fontsize=6.1, color=INK, ha='center', va='center', linespacing=1.35,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7))
ax.annotate('small fragments\ntravel furthest', xy=(5.35, ypos(1.0)), xytext=(8.15, 1.15),
            fontsize=6.1, color=INK, ha='center', va='center', linespacing=1.35,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7))
ax.text(3.0, -1.18, 'M ladder   1 uncut plasmid   2 single digest   3 double digest',
        fontsize=6.1, color=MUTED, ha='center', va='center')
ax.set_xlim(-1.35, 9.95); ax.set_ylim(-1.55, 6.65); ax.axis('off')
```

::: example 5.3 Reading a digest
**Problem.** A linear DNA molecule 12 kb long has three *Eco*RI sites. A
circular plasmid 12 kb long also has three *Eco*RI sites. How many bands does
each give after complete digestion, and what is the total length in each lane?

**Solution.**
A **linear** molecule cut at $n$ internal sites gives $n + 1 = 3 + 1 = 4$
fragments, so up to **4 bands**.
A **circular** molecule cut at $n$ sites gives $n = 3$ fragments, so **3 bands**.
In both lanes the fragment lengths must add up to the original 12 kb, because
digestion removes no DNA.

If the linear fragments were 5, 4, 2 and 1 kb, the 1 kb band lies nearest the
anode and the 5 kb band nearest the well. (Two fragments of equal size would
run together and appear as one brighter band — a common trap in questions.)
:::

### Genetically modified organisms

A **genetically modified organism (GMO)** is an organism whose genome has been
deliberately altered by inserting, deleting or silencing a gene using rDNA
technology. A GMO that carries a gene from a different species is called
**transgenic**.

| GMO | Gene transferred | Result |
|---|---|---|
| *E. coli* producing humulin (1982) | human insulin genes A and B | cheap, non-allergenic human insulin |
| Bt cotton (India, 2002) | *cry1Ac* from *Bacillus thuringiensis* | resists bollworm; now over 90 % of India's cotton area |
| Bt brinjal (Bangladesh, approved 2013) | *cry1Ac* | resists fruit and shoot borer |
| Golden Rice | *psy* (daffodil/maize) + *crtI* (*Erwinia*) | grain makes β-carotene, a vitamin A precursor |
| Flavr Savr tomato (1994) | antisense polygalacturonase | slower softening, longer shelf life |
| Roundup Ready soybean | bacterial *EPSPS* | tolerates the herbicide glyphosate |
| Bt maize | *cry1Ab* | resists stem borer |

**Benefits.** Higher yield with less pesticide, tolerance of drought, salt and
herbicides, longer shelf life, biofortified food such as Golden Rice, and cheap
medicines (insulin, human growth hormone, hepatitis B vaccine, clotting factor
VIII).

**Concerns.** Possible allergens in new proteins; antibiotic-resistance marker
genes; gene flow to wild relatives, creating "superweeds"; harm to non-target
insects; loss of local landraces and farmer dependence on bought seed; and the
ethical objection to patenting life. Because of these risks, every country
that ratified the **Cartagena Protocol on Biosafety** regulates GM release.

::: note GM crops and Nepal
Nepal ratified the Cartagena Protocol in **2001** and adopted a National
Biosafety Framework in **2006**, the same year as the Biotechnology Policy
2063 BS. A Supreme Court interim order in **January 2014** stopped the import
of GM seed; the restriction was partly relaxed in **November 2021** for
imported canola, soybean and maize grain, which is screened by the Plant
Quarantine and Pesticides Management Centre. **No GM crop is registered for
cultivation in Nepal**, and the Seed Quality Control Centre laboratory tests
border samples by PCR each year. Golden Rice was given a commercial biosafety
permit in the Philippines in **July 2021**, but a Court of Appeals order in
**April 2024** halted it pending further safety review.
:::

::: caution Transgenic is not the same as hybrid
A hybrid is produced by ordinary sexual crossing within or between closely
related species; a transgenic plant carries a gene inserted in the laboratory,
often from an unrelated kingdom. Bt cotton is transgenic; a maize hybrid from
two inbred lines is not a GMO. Do not write "GMO" for every improved variety.
:::

## 5.6 Bio-engineering

**Bio-engineering (biochemical engineering)** applies engineering design to
living systems so that biological reactions can be run on an industrial scale.
The central piece of hardware is the **bioreactor** or **fermenter** — a
stirred, sterilised stainless-steel vessel in which temperature, pH, dissolved
oxygen and nutrient feed are controlled automatically while microbes or
cultured cells make the product.

| Area | Principle | Example |
|---|---|---|
| Industrial fermentation | microbes grown in a bioreactor secrete a product | penicillin from *Penicillium chrysogenum*, citric acid from *Aspergillus niger* |
| Enzyme technology | enzymes immobilised on beads and reused | glucose isomerase for high-fructose syrup |
| Biofuel | plant biomass or oil converted to fuel | ethanol from sugarcane, biodiesel from *Jatropha curcas* |
| Biogas | anaerobic digestion of dung by methanogens | about 450,000 household biogas plants in Nepal |
| Bioremediation | microbes break down pollutants | *Pseudomonas putida* ("superbug") degrades oil |
| Phytoremediation | plants take up heavy metals from soil | *Brassica juncea* accumulates lead |
| Biosensors | an enzyme or microbe coupled to an electrode | glucometer for blood sugar |
| Bioleaching | bacteria release metal from low-grade ore | *Thiobacillus ferrooxidans* leaches copper |
| Single-cell protein | microbial biomass used as food or feed | *Spirulina*, *Methylophilus methylotrophus* |
| Biomedical engineering | engineered tissues and devices | artificial skin, dialysis membranes, stents |

Nepal's biogas programme, begun in **1992**, is the best local example: a fixed
dome digester loaded with cattle dung and water produces a gas of roughly 60 %
methane for cooking and lighting, and the spent slurry returns to the field as
manure. It replaces firewood, cuts indoor smoke and reduces pressure on
forests.

## 5.7 Food safety and food security

These two terms are often confused. **Food safety** is about the *quality* of
food — that it is free from anything that could harm the eater. **Food
security** is about *access* — that everyone always has enough of it.

::: definition Food security (FAO, 1996)
Food security exists when **all people, at all times, have physical, social and
economic access to sufficient, safe and nutritious food** that meets their
dietary needs and food preferences for an active and healthy life. Its four
pillars are **availability, access, utilisation and stability**.
:::

**Hazards in food**

| Type of hazard | Examples |
|---|---|
| Biological | *Salmonella*, *E. coli* O157:H7, *Vibrio cholerae*, hepatitis A virus, *Entamoeba*, aflatoxin from *Aspergillus flavus* on damp maize and groundnut |
| Chemical | pesticide residue, heavy metals, excess food colour, adulterants such as melamine or chemical ripening agents |
| Physical | glass, metal, stone, hair, insect parts |

**How safety is ensured.** Good agricultural and hygienic practice in the
field; correct drying and storage to keep grain below the moisture level at
which moulds grow; pasteurisation, canning, refrigeration and irradiation;
**HACCP** (Hazard Analysis and Critical Control Points), in which every step of
processing is examined and the critical points are monitored; and labelling to
**Codex Alimentarius** standards. In Nepal the **Food Act 2023 BS (1966)** and
the **Department of Food Technology and Quality Control (DFTQC)** enforce these
rules, and the **Right to Food and Food Sovereignty Act, 2075 (2018)** gives
every citizen a legal right to food, implementing Article 36 of the
Constitution of Nepal.

**Where biotechnology helps.** Higher-yielding and stress-tolerant varieties
raise availability; **biofortified** crops such as Golden Rice, iron-rich beans
and zinc-rich wheat improve utilisation; tissue culture supplies
disease-free planting material; bio-pesticides and bio-fertilizers cut chemical
residues; and **PCR and ELISA** allow rapid detection of pathogens, aflatoxin
and undeclared GM material in a consignment. Post-harvest technology matters
just as much: Nepal loses roughly a fifth of its cereal harvest to poor storage
and transport, and saving that loss adds as much food as a large rise in yield.

::: tip Answering the 8-mark biotechnology question
Long questions almost always ask you to "describe the steps" of something —
tissue culture, rDNA technology, PCR, or plant breeding. Number the steps,
give one sentence and the key reagent or temperature for each, and finish with
two applications. A labelled sketch of the plasmid or the cycle earns marks
even when the question does not ask for a diagram.
:::

## Chapter summary

- **Tissue culture** works because plant cells are **totipotent**. Explant →
  surface sterilisation → MS medium → callus → shoots (high cytokinin) → roots
  (high auxin) → hardening. It gives disease-free, genetically identical
  clones all year round.
- **Plant breeding** improves crops by selection, introduction, hybridisation
  and mutation breeding; the Green Revolution used dwarf, fertiliser-responsive
  varieties such as wheat **Bhrikuti** and rice **Sabitri** in Nepal.
- Disease resistance is **vertical** (one R gene, complete but easily broken,
  gene-for-gene) or **horizontal** (many genes, partial but durable).
  *Bacillus thuringiensis* **cry** genes make a protoxin that becomes active
  only in the alkaline insect gut, so Bt crops kill the pest but not the eater.
- **Green manure** adds organic matter and nitrogen by ploughing in a legume;
  **bio-fertilizers** are living organisms (*Rhizobium*, *Azotobacter*,
  *Azolla–Anabaena*, mycorrhiza, blue-green algae) that supply nutrients;
  **bio-pesticides** are living or natural agents (Bt, *Trichoderma*, neem)
  that control pests without residues.
- **Genetic engineering** needs four tools: restriction enzymes to cut
  (*Eco*RI cuts G↓AATTC and leaves sticky ends), DNA ligase to join, a vector
  with *ori* + marker + unique sites, and a host cell. Steps: isolate → cut →
  ligate → transform → select → multiply.
- **PCR** copies a target *in vitro* using primers and Taq polymerase from
  *Thermus aquaticus*: denature 94–95 °C, anneal 50–65 °C, extend 72 °C; after
  $n$ cycles one molecule becomes $2^n$ copies.
- In **gel electrophoresis** DNA is negatively charged and moves to the anode;
  small fragments travel furthest. A linear molecule with $n$ cut sites gives
  $n+1$ fragments, a circular one gives $n$.
- **GMOs** include Bt cotton, Bt brinjal, Golden Rice and humulin-producing
  *E. coli*. Their release is controlled under the Cartagena Protocol; no GM
  crop is approved for cultivation in Nepal.
- **Food safety** is freedom from biological, chemical and physical hazards
  (HACCP, DFTQC); **food security** is availability, access, utilisation and
  stability of enough safe food for all.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The capacity of a single differentiated plant cell to regenerate a complete plant is called <span class="marks">[1]</span>
   (a) totipotency (b) pluripotency (c) apomixis (d) senescence
2. In a tissue culture medium, shoot formation from callus is favoured by <span class="marks">[1]</span>
   (a) high auxin : low cytokinin (b) high cytokinin : low auxin (c) auxin alone (d) gibberellin alone
3. *Eco*RI recognises and cuts the sequence <span class="marks">[1]</span>
   (a) GGATCC (b) AAGCTT (c) GAATTC (d) CTGCAG
4. Taq polymerase used in PCR is obtained from <span class="marks">[1]</span>
   (a) *Escherichia coli* (b) *Thermus aquaticus* (c) *Agrobacterium tumefaciens* (d) *Bacillus thuringiensis*
5. During agarose gel electrophoresis DNA fragments move towards the anode because DNA is <span class="marks">[1]</span>
   (a) positively charged (b) neutral (c) negatively charged (d) amphoteric
6. Which one of the following is a bio-fertilizer? <span class="marks">[1]</span>
   (a) urea (b) *Rhizobium* (c) *Bacillus thuringiensis* (d) neem oil

::: note Answers to Group A
**1.** (a) — totipotency is the basis of all plant tissue culture.
**2.** (b) — a high cytokinin to auxin ratio induces shoots; the reverse induces roots.
**3.** (c) — *Eco*RI cuts the palindrome G↓AATTC, leaving four-base sticky ends.
**4.** (b) — *T. aquaticus* lives in hot springs, so its polymerase survives 95 °C.
**5.** (c) — the phosphate groups of the backbone carry a negative charge at all pH.
**6.** (b) — *Rhizobium* fixes nitrogen; Bt and neem are bio-pesticides, urea is chemical.
:::

**Group B — Short answer (4 marks each)**

1. What is micropropagation? List its steps in order and give two advantages over conventional propagation. <span class="marks">[4]</span>
2. Differentiate between vertical and horizontal resistance in plants, with one example of each. <span class="marks">[4]</span>
3. Explain how the Bt toxin kills a caterpillar but is harmless to human beings. <span class="marks">[4]</span>
4. A PCR tube contains 8 copies of a target sequence and is run for 25 cycles at full efficiency. Calculate the number of copies formed, and state why the actual yield is lower after about 35 cycles. <span class="marks">[4]</span>
5. Distinguish between green manure and bio-fertilizer, giving two examples of each. <span class="marks">[4]</span>

::: note Answers to Group B
**1.** Micropropagation is the rapid multiplication of plants *in vitro* from
small explants using tissue culture. Steps: (i) select and surface-sterilise
the explant with 0.1 % HgCl₂ or sodium hypochlorite; (ii) inoculate on MS
medium with a high cytokinin : auxin ratio to get shoots (through callus if
needed); (iii) transfer the shoots to a high auxin medium for rooting;
(iv) harden the plantlets in a greenhouse, then transfer to the field.
Advantages: thousands of genetically identical, disease-free plants from one
mother plant in a small space, all the year round; it works for species that
are sterile or slow to propagate, such as banana and orchids.

**2.**
| Vertical resistance | Horizontal resistance |
|---|---|
| Governed by one or a few major R genes | Governed by many minor genes (polygenic) |
| Complete immunity, but only to certain races | Partial, slows the disease down |
| Breaks down when a new race appears | Durable across races |
| Easy to transfer by breeding | Difficult, needs many crosses |
| Example: *Sr* stem-rust genes in wheat | Example: field resistance to late blight of potato |

**3.** *Bacillus thuringiensis* makes a crystalline **protoxin** (Cry protein)
that is inactive as made. The caterpillar eats leaf tissue containing it. The
insect midgut is strongly **alkaline** (pH about 9–10), so the crystal
dissolves there and gut proteases cut it into the active toxin. The toxin binds
to specific receptors on the midgut epithelium and makes pores, so the cells
swell and burst; the insect stops feeding and dies. The human stomach is
strongly **acidic** (pH 1.5–3), the crystal does not dissolve, the activating
proteases are absent and human gut cells carry no receptor for it — so the
protein is simply digested like any other protein.

**4.** Copies $= N_0 \times 2^n = 8 \times 2^{25}$.
$2^{25} = 33{,}554{,}432$, so $N = 8 \times 33{,}554{,}432 = 268{,}435{,}456
\approx 2.68 \times 10^{8}$ copies.
After about 35 cycles the primers and dNTPs are used up, Taq polymerase loses
activity from repeated heating, and the many product strands re-anneal to each
other instead of to primers, so the reaction enters the **plateau phase** and
the number of copies stops doubling.

**5.**
| Green manure | Bio-fertilizer |
|---|---|
| A green crop grown and ploughed back into the same field | A preparation of living micro-organisms applied to seed, soil or root |
| Adds organic matter, nitrogen and improves soil structure | Supplies nutrients by fixing N₂ or solubilising phosphate |
| Acts after decomposition, over one season | Acts as long as the organism stays alive in the soil |
| Examples: *Sesbania aculeata* (dhaincha), *Crotalaria juncea* (sunn hemp) | Examples: *Rhizobium*, *Azotobacter*, *Azolla–Anabaena*, mycorrhiza |
:::

**Group C — Long answer (8 marks each)**

1. Describe the steps of recombinant DNA technology. Mention the role of restriction endonuclease, DNA ligase and a cloning vector, and explain how recombinant cells are selected. <span class="marks">[8]</span>
2. Describe plant tissue culture under the headings: principle, medium, steps and applications. <span class="marks">[8]</span>
3. Define food safety and food security. Explain the four pillars of food security and describe four ways in which biotechnology can improve food safety and food security in Nepal. <span class="marks">[8]</span>

::: note Answers to Group C
**1.** Outline. (i) **Isolation of DNA** — lyse cells with lysozyme or
cellulase, digest protein with protease and RNA with ribonuclease, precipitate
DNA with chilled ethanol. (ii) **Cutting** — a **restriction endonuclease**
such as *Eco*RI cuts both the donor DNA and the vector at the same palindromic
sequence (G↓AATTC), giving complementary **sticky ends**. (iii) **Ligation** —
the sticky ends base-pair and **DNA ligase** seals the phosphodiester bonds,
producing recombinant DNA. (iv) **Vector** — the plasmid (pBR322) or Ti plasmid
carries an *ori* so it replicates in the host, selectable marker genes, and
unique restriction sites. (v) **Transformation** — the rDNA is introduced by
CaCl₂ + heat shock, electroporation, gene gun or *Agrobacterium*.
(vi) **Selection** — insertional inactivation: the insert destroys *tet*ᴿ, so
recombinants grow on ampicillin but not on tetracycline; or blue–white
screening on X-gal, where recombinant colonies are white. (vii) **Culture and
downstream processing** — the selected clone is grown in a bioreactor or
regenerated into a plant and the product purified. Applications: insulin,
vaccines, Bt crops, Golden Rice.

**2.** *Principle*: **totipotency** — every living plant cell carries the whole
genome and can regenerate a complete plant under the right conditions.
*Medium*: Murashige and Skoog (1962) medium supplying macronutrients,
micronutrients, 2–3 % sucrose, vitamins, myo-inositol, agar and growth
regulators; autoclaved at 121 °C and kept at pH 5.6–5.8.
*Steps*: choose the explant (shoot tip, node, anther, embryo) → surface
sterilise → inoculate aseptically → callus induction with 2,4-D →
**organogenesis**: high cytokinin : auxin gives shoots, high auxin gives roots →
subculture → **hardening** and transfer to soil.
*Types*: callus, suspension, meristem, anther (haploids), embryo rescue and
protoplast culture.
*Applications*: rapid clonal multiplication of banana, orchid, potato and
sugarcane; virus-free plants from meristem tips; haploids and homozygous lines
from anther culture; somatic hybrids by protoplast fusion; **germplasm
conservation** by cryopreservation; secondary metabolites from cell suspension;
and it is the essential regeneration step in making any transgenic plant.

**3.** **Food safety** means food that is free from biological, chemical and
physical hazards and is fit to eat. **Food security** (FAO, 1996) exists when
all people, at all times, have physical, social and economic access to
sufficient, safe and nutritious food for an active, healthy life.
*Four pillars*: **availability** (enough food produced or imported);
**access** (people can afford and reach it); **utilisation** (the body can use
it — safe food, clean water, balanced diet); **stability** (the first three do
not fail in drought, flood or price shock).
*Contribution of biotechnology in Nepal*: (i) tissue culture supplies
disease-free potato, banana and orchid planting material, raising yield;
(ii) improved and stress-tolerant varieties bred with marker-assisted selection
add availability and stability; (iii) bio-fertilizers and bio-pesticides cut
chemical residues, so food is safer and cheaper to grow; (iv) PCR and ELISA in
the DFTQC and Seed Quality Control Centre laboratories detect pathogens,
aflatoxin and unapproved GM material in imports; (v) biofortified crops such as
Golden Rice and zinc-rich wheat and better post-harvest storage reduce
malnutrition and the large storage losses.
:::
