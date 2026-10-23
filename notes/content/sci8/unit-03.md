---
subject: Science and Technology
grade: 8
title: Living Beings and Their Structure
unit: 3
hours: 0
area: Science and Technology
---

There are many kinds of plants and animals on the earth, from microscopic
germs to huge trees and whales. Animals usually have a head, trunk, tail and
limbs; plants usually have roots, stems, leaves, flowers and fruits. Many tiny
organisms have no such organs at all. Yet the body of every living being is made
of very small units called **cells**. Because the cells work together in perfect
coordination, the body can digest, breathe, grow and reproduce. In this unit we
study the cell and its parts, how cells build tissues, organs and systems, how
living beings are classified, and how microorganisms help and harm us.

::: key What this unit asks of you
Draw and label a plant cell and an animal cell; give the structure and function
of the cell wall, cell membrane, cytoplasm, mitochondria, plastids, ribosomes,
ER, Golgi body, lysosome, vacuole and nucleus; explain cell → tissue → organ →
organ system; compare the two-kingdom and five-kingdom systems; describe
viruses, bacteria, amoeba and fungi with their good and bad effects; and explain
dry, wet and cold preservation of food.
:::

## 3.1 The cell: plant and animal cells, organelles and their functions

::: definition Cell
The **cell** is the basic structural and functional unit of life. Every
organism is made of one or many cells, and all life processes — digestion,
respiration, reproduction, transport and photosynthesis — take place in or by
cells. The study of cells is called **cytology**.
:::

**History.** The cell was first seen by **Robert Hooke** in **1665** in a thin
slice of cork under a microscope he made himself. He called the little rooms
*cellulae* ("tiny rooms" in Latin). Later, **Schleiden** (plants), **Schwann**
(animals) and **Rudolf Virchow** concluded that all living bodies are made of
cells and that new cells come from existing cells.

### 3.1.1 Shape and size of cells

Animal cells are usually irregular: oval, round, rod-like, cubical or columnar.
Nerve cells are long and thread-like; most muscle cells are spindle-shaped.
Plant cells are usually box-like or hexagonal. Bacteria are round, rod-shaped,
thread-like or spiral. Most cells are too small to see with the naked eye. The
smallest known cell is *Mycoplasma* (a bacterium), about **0.2 micrometre**
across; the biggest single cell is the **ostrich egg**, about 15 cm long.

::: example Real size of a cell under a microscope
**Problem.** Under a microscope of magnification 400×, an onion cell appears 8 mm long. Find
its real length in mm and in micrometres (1 mm = 1000 μm).
**Solution.** Real size $=\frac{\text{image size}}{\text{magnification}}=\frac{8\ \text{mm}}{400}=0.02$ mm
$=0.02\times1000=20$ μm.
:::

### 3.1.2 Observing cells (Activities 3.2 and 3.3)

**Onion peel (plant cell).** Take a thin, transparent peel from an onion scale
and cut small pieces. Stain them in **safranin** in a watch glass for a few
minutes, then wash in clean water. Put a drop of **glycerine** on a clean slide,
place one piece in it with a needle, spread it flat and lower a cover slip
gently so that no air bubbles are trapped. Observe under the microscope: you see
box-like cells joined side by side, each with a thick wall and a nucleus.

**Cheek cells (animal cell).** Gently scrape the inside of your cheek with a
clean, **blunt toothpick** (never a sharp metal needle). Put a drop of 1 %
**methylene blue** and a drop of salt solution on a slide, mix the scraping in
it and cover. The cells are flat and irregular, with a dark-stained nucleus and
no cell wall.

```photo id="sci8/cheek-cells" caption="Human cheek cells under a light microscope. Each cell is flat and irregular, with no cell wall." width="66"
key 1 Nucleus
key 2 Cytoplasm
key 3 Cell membrane
```

### 3.1.3 Parts of a cell

A cell has four main groups of parts: **cell covering, cytoplasm, cell
components** and **nucleus**.

```figure caption="A plant cell (left) and an animal cell (right). Only the plant cell has a cell wall, chloroplasts and one large central vacuole."
from matplotlib.patches import Rectangle, Circle, Ellipse, FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.2, 3.3))
ax.set_xlim(0, 10.4)
ax.set_ylim(0, 6.6)
ax.axis("off")
# plant cell
ax.add_patch(Rectangle((0.3, 0.9), 3.9, 4.6, fc="#e4efd9", ec=INK, lw=2.6))
ax.add_patch(Rectangle((0.45, 1.05), 3.6, 4.3, fc="none", ec=SERIES[2], lw=0.9))
ax.add_patch(Rectangle((1.0, 1.5), 1.6, 2.2, fc="white", ec=ACCENT, lw=1.0))
ax.add_patch(Circle((3.2, 4.4), 0.45, fc="#9fb7d9", ec=INK, lw=1))
ax.add_patch(Circle((3.2, 4.4), 0.13, fc=INK))
for cx, cy in [(0.9, 4.7), (1.9, 4.8), (3.5, 2.1), (3.4, 3.1)]:
    ax.add_patch(Ellipse((cx, cy), 0.42, 0.24, fc=SERIES[2], ec="none"))
ax.add_patch(Ellipse((2.9, 1.5), 0.5, 0.24, fc=SERIES[3], ec="none"))
ax.text(2.25, 6.15, "Plant cell", ha="center", fontsize=8.6, color=INK)
lab = dict(fontsize=7.4, color=INK, va="center")
def tag(x, y, tx, ty, s, ha):
    ax.annotate(s, xy=(x, y), xytext=(tx, ty), ha=ha, **lab,
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7))
tag(0.3, 5.2, 0.05, 5.85, "cell wall", "left")
tag(1.8, 2.6, 1.8, 0.45, "large vacuole", "center")
tag(3.4, 3.1, 4.7, 2.7, "chloroplast", "left")
tag(3.6, 4.6, 4.7, 5.1, "nucleus", "left")
tag(4.05, 1.3, 4.7, 1.5, "cell membrane", "left")
tag(2.9, 1.5, 3.2, 0.45, "mitochondrion", "left")
# animal cell
ax.add_patch(Ellipse((8.0, 3.3), 3.6, 3.9, fc="#f6e3dc", ec=INK, lw=1.1))
ax.add_patch(Circle((8.0, 3.5), 0.5, fc="#9fb7d9", ec=INK, lw=1))
ax.add_patch(Circle((8.0, 3.5), 0.14, fc=INK))
ax.add_patch(Circle((7.1, 2.4), 0.22, fc="white", ec=ACCENT, lw=1))
ax.add_patch(Ellipse((8.9, 2.3), 0.5, 0.24, fc=SERIES[3], ec="none"))
ax.text(8.0, 6.15, "Animal cell", ha="center", fontsize=8.6, color=INK)
tag(9.6, 4.2, 9.2, 5.65, "cell membrane", "center")
tag(7.55, 3.7, 6.1, 4.0, "nucleus", "right")
tag(7.1, 2.4, 6.5, 0.9, "small vacuole", "center")
tag(8.9, 2.3, 9.0, 0.7, "mitochondrion", "center")
tag(7.3, 4.2, 6.6, 5.4, "cytoplasm", "center")
fig.tight_layout()
```

**1. Cell covering: cell wall and cell membrane**

| Cell wall | Cell membrane (plasma membrane) |
|---|---|
| found only in plant, fungal and bacterial cells | found in all cells |
| outermost layer in those cells | outermost layer in animal cells; just inside the wall in plant cells |
| tough, rough, non-living | thin, smooth, elastic, living |
| freely permeable | **semi-permeable**: controls what enters and leaves |
| gives a **fixed shape** and mechanical support; protects from germs; in root hairs helps absorb water and minerals | controls transport of fluids; in amoeba forms pseudopodia for movement and catching food |

**2. Cytoplasm.** A clear, sticky, semi-liquid between the cell membrane and the
nucleus, made of water, salts, minerals, proteins and vitamins. **Functions:**
the chemical reactions of life (metabolism) take place in it; it balances water
and minerals; it holds the organelles.

**3. Cell components.** These are of two kinds. **Cell organelles** are living
parts that each do a special job (mitochondria, plastids, ribosomes, ER, Golgi
body, lysosome). **Cell inclusions** are non-living things in the cytoplasm —
droplets of water, crystals of salts, enzymes, hormones, vitamins, stored food
and wastes. They act as raw materials and energy sources for the organelles.

| Organelle | Structure | Function |
|---|---|---|
| **Mitochondria** | rod-like or thread-like, double membrane; inner membrane folded | **power house**: oxidise glucose with oxygen to release energy (stored as **ATP**); give CO₂ and water; contain some DNA |
| **Chloroplast** (green plastid) | round or oval, double membrane, contains **chlorophyll**; spiral ribbon in *Spirogyra* | makes food by **photosynthesis**; makes plants green; contains DNA |
| **Chromoplast** | coloured (not green) plastid in flowers, ripe fruits, some leaves | gives colour that attracts insects and birds for pollination and seed dispersal |
| **Leucoplast** | colourless plastid in roots, seeds, white parts | stores starch, protein and fat |
| **Ribosome** | very small, no membrane; free or on ER | makes proteins — the **protein factory** |
| **Endoplasmic reticulum (ER)** | network of folded membrane canals from nucleus to cell membrane; *rough* ER has ribosomes, *smooth* ER has none | framework and support (**endoskeleton** of the cell); transport inside the cell; helps make new membranes |
| **Golgi body** | stack of flat sacs (cisternae) with vesicles; discovered by Camillo Golgi, 1898 | **secretion** of mucus, saliva, sweat, tears, gum; sorts and packs proteins; forms the cell plate in plant cell division |
| **Lysosome** | small round sac with a single membrane, full of digestive enzymes | digests food, worn-out and dead parts; can digest its own cell — the **suicidal bag** |
| **Vacuole** | space bounded by a membrane (tonoplast), filled with **cell sap**; large in old plant cells, small in animal cells | balances water and salts; stores wastes before they are removed |

Plastids are found only in plant cells (and some bacteria and protists). The
vacuole is not a true organelle but a space filled with liquid.

**4. Nucleus.** The nucleus is a round body, usually near the centre, enclosed by
a double, porous **nuclear membrane**. It is found in the cells of plants,
animals, protists and fungi (**eukaryotes**). Bacteria are **prokaryotes**: their
genetic material lies free in the cell without a membrane.

| Part of nucleus | Description and function |
|---|---|
| Nuclear membrane | double membrane with pores; protects the nucleus and lets substances pass in and out |
| Nucleolus | round body without a membrane; made of protein and RNA; helps in cell division |
| Nucleoplasm | liquid inside the nucleus; holds the nucleolus and chromatin |
| Chromatin fibres | thin threads of **DNA** and protein; become thick, visible **chromosomes** during cell division; carry hereditary characters. A human cell has **23 pairs (46)** |

**Functions of the nucleus:** controls and coordinates all activities of the
cell, so it is called the **brain of the cell**; passes hereditary characters
from parents to offspring; takes part in cell division (needed for growth); in
unicellular organisms takes part directly in reproduction.

### 3.1.4 Plant cell and animal cell compared

| Plant cell | Animal cell | Both |
|---|---|---|
| has a cell wall of cellulose | no cell wall | cell membrane |
| usually box-like, fixed shape | irregular or round | cytoplasm |
| has plastids (chloroplasts) | no plastids | nucleus |
| one large central vacuole | many small vacuoles or none | mitochondria, ribosomes, ER, Golgi body |
| nucleus pushed to one side | nucleus near the centre | cellular respiration |

::: caution Three mistakes in cell diagrams
**(1)** Drawing the cell wall and cell membrane as one line in a plant cell —
draw a thick wall with a thin membrane just inside. **(2)** Putting chloroplasts
in an animal cell. **(3)** Writing names without label lines: a label must touch
the part with a straight line.
:::

::: example Identify the cell
**Question.** A cell has a rigid outer boundary, one large central space and many
small green bodies. Identify it, giving three reasons.

**Answer.** It is a **plant cell**. (i) The rigid boundary is the **cell wall**,
absent in animal cells. (ii) The large central space is the **vacuole**, large
only in plant cells. (iii) The green bodies are **chloroplasts**, found only in
plant cells.
:::

## 3.2 Cell, tissue, organ and organ system in the human body

Cells of similar kind join to form a **tissue**. Different tissues join at a
place to form an **organ**, which does one or more special jobs. Organs that
work together for one function form an **organ system**. All the organ systems
together make the **body** (organism).

```figure caption="Levels of organisation, using the digestive system as the example."
fig, ax = plt.subplots(figsize=(5.0, 2.2))
ax.set_xlim(0, 10)
ax.set_ylim(0, 3.6)
ax.axis("off")
levels = [("Cell", "muscle cell"), ("Tissue", "muscle tissue"), ("Organ", "stomach"),
          ("Organ system", "digestive\nsystem"), ("Body", "human being")]
xs = [0.9, 2.95, 5.0, 7.05, 9.1]
for (name, ex), x in zip(levels, xs):
    ax.text(x, 2.4, name, ha="center", va="center", fontsize=8.2, color=INK,
            bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=ACCENT, lw=1.1))
    ax.text(x, 1.15, ex, ha="center", va="center", fontsize=7.6, color=MUTED)
for a, b in zip(xs[:-1], xs[1:]):
    ax.annotate("", xy=(b - 0.85, 2.4), xytext=(a + 0.85, 2.4),
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1))
fig.tight_layout()
```

**Example from the textbook.** Muscle fibres (cells) form **muscular tissue**.
Muscular tissue lies in the middle layer of the food pipe, stomach and
intestine. Its rhythmic contraction and relaxation (peristalsis) pushes food
along. **Glandular tissue** in the inner wall of the stomach and intestine
secretes digestive enzymes. These tissues together make the organs of the
digestive system, and the system digests food for the whole body. So cells,
tissues, organs and systems depend on one another; if the cells fail, the organ
and the body fail.

| Organ system | Main organs | Job |
|---|---|---|
| Digestive | mouth, food pipe, stomach, intestines, liver | digests and absorbs food |
| Respiratory | nose, trachea, lungs | takes in O₂, gives out CO₂ |
| Circulatory | heart, blood vessels, blood | carries food, oxygen and wastes |
| Excretory | kidneys, ureters, urinary bladder | removes urea and extra salts |
| Nervous | brain, spinal cord, nerves | controls and coordinates the body |
| Skeletal and muscular | bones, muscles | support, protection, movement |
| Reproductive | testes / ovaries and related organs | produces young ones |

## 3.3 Classification of living beings

Living beings differ in habitat, nutrition, reproduction and body structure,
but they also share features. A bat flies and a rabbit runs, but both give
birth to young and feed them milk, so both are placed in the class **Mammalia**.

::: definition Classification
**Classification** is the grouping of living beings into groups and subgroups
on the basis of their similarities and differences. It makes the study of the
huge number of organisms easy and systematic, and shows the trend of evolution.
:::

### 3.3.1 Two-kingdom system

Proposed by the Swedish biologist **Carolus Linnaeus** in **1753**. All organisms
were put into two kingdoms, **Plantae** and **Animalia**, on the basis of
nutrition, movement, growth and reproduction. Organisms that move, take ready-made
food (heterotrophic) and stop growing after some time are animals; those that do
not move, make their own food (autotrophic) and grow throughout life are plants.

**Merits:** the first scientific system; simple; plants and animals are easily
distinguished.
**Drawbacks:** (1) fungi, which cannot photosynthesise, were put with plants;
(2) prokaryotic bacteria and eukaryotic algae were put in the same kingdom;
(3) unicellular and multicellular organisms were not separated; (4) organisms
like lichens and *Euglena* (which has features of both) had no proper place.

### 3.3.2 Five-kingdom system

Proposed by the American ecologist **R. H. Whittaker** in **1969**. **Basis:**
type of cell (prokaryotic or eukaryotic), body organisation (unicellular or
multicellular), mode of nutrition (autotrophic or heterotrophic), role in the
ecosystem (producer, consumer or decomposer) and phylogenetic (evolutionary)
relationship.

```figure caption="The five kingdoms of R. H. Whittaker (1969), arranged from simple to complex."
fig, ax = plt.subplots(figsize=(5.1, 2.7))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5.2)
ax.axis("off")
ax.text(5.0, 4.7, "Living beings", ha="center", va="center", fontsize=8.6, color=INK,
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=INK, lw=1.1))
kings = [("Monera", "prokaryotic,\nunicellular", "bacteria"),
         ("Protista", "eukaryotic,\nunicellular", "amoeba"),
         ("Fungi", "no chlorophyll,\nabsorb food", "mushroom"),
         ("Plantae", "make own food\n(chlorophyll)", "fern, rice"),
         ("Animalia", "multicellular,\neat food", "frog, cow")]
xs = [1.0, 3.0, 5.0, 7.0, 9.0]
for (k, d, e), x in zip(kings, xs):
    ax.plot([5.0, x], [4.4, 3.65], color=GRID, lw=1)
    ax.text(x, 3.35, k, ha="center", va="center", fontsize=8.2, color=ACCENT,
            bbox=dict(boxstyle="round,pad=0.28", fc="white", ec=ACCENT, lw=1))
    ax.text(x, 2.15, d, ha="center", va="center", fontsize=7.2, color=INK)
    ax.text(x, 0.95, e, ha="center", va="center", fontsize=7.2, color=MUTED, style="italic")
fig.tight_layout()
```

| Kingdom | Main features | Examples |
|---|---|---|
| Monera | unicellular prokaryotes (no true nucleus) | bacteria, cyanobacteria, *Mycoplasma* |
| Protista | unicellular eukaryotes | *Amoeba*, *Paramecium*, *Euglena*, *Plasmodium*, *Chlamydomonas* |
| Fungi (Mycota) | eukaryotes with cell wall, no chlorophyll; saprophytic or parasitic; digest food outside the body | mushroom, yeast, *Mucor*, *Penicillium*, yarsagumba |
| Plantae | multicellular, green, autotrophic (producers) | moss, fern, pine, mustard, sunflower |
| Animalia | multicellular eukaryotic consumers, no cell wall | sponge, earthworm, insect, fish, human |

**Features:** unicellular and multicellular organisms are separated; prokaryotes
and eukaryotes are separated; autotrophs (Plantae) and heterotrophs (Animalia,
Fungi) are separated; organisms are arranged from least developed to more
developed, showing the trend of evolution.

| Two-kingdom system | Five-kingdom system |
|---|---|
| Linnaeus, 1753 | Whittaker, 1969 |
| two kingdoms: Plantae, Animalia | five kingdoms: Monera, Protista, Fungi, Plantae, Animalia |
| based on nutrition, movement, growth | based on cell type, body organisation, nutrition, ecological role, evolution |
| prokaryotes and eukaryotes mixed | separated |
| fungi and bacteria placed with plants | given their own kingdoms |

### 3.3.3 The vertebrate classes

Animals with a backbone are **vertebrates**. They are divided into five classes.

| Class | Body covering | Breathing | Young | Examples |
|---|---|---|---|---|
| Pisces (fish) | scales, fins | gills | eggs in water | rohu, trout |
| Amphibia | moist skin, no scales | gills when young; lungs and skin as adult | eggs in water | frog, toad |
| Reptilia | dry scaly skin | lungs | shelled eggs on land | lizard, snake, tortoise |
| Aves (birds) | feathers, beak | lungs | hard-shelled eggs | sparrow, danfe, pigeon |
| Mammalia | hair or fur, mammary glands | lungs | most give birth; feed milk | cow, bat, whale, human |

::: caution A whale is not a fish
A whale lives in water and has fins, but it has hair, breathes with lungs and
feeds its young with milk, so it is a mammal. Classification follows body
structure, not the place where an animal lives.
:::

## 3.4 Effects of microorganisms

**Microorganisms** (germs or microbes) are living beings too small to be seen with
the naked eye. They live in air, water, soil, uncovered food, dirt, and in and on
living and dead bodies. A broken egg left open becomes rotten and smelly because
of them. The study of microorganisms is **microbiology**.

**(A) Virus.** The smallest germs, which can infect plants, animals, bacteria and
fungi. A virus has **no cell** (acellular), so it belongs to no kingdom. Its body
is only nucleic acid (DNA or RNA) inside a protein coat (**capsid**), sometimes
with an envelope. Outside a host it behaves like a non-living thing (no eating,
breathing or growth); inside a living cell it multiplies, damaging the cell. So it
is called a **link between living and non-living** and an **obligate parasite**.
Examples: rhinovirus (cold), coronavirus (SARS-CoV-2 causes COVID-19), tobacco
mosaic virus, bacteriophage.

**(B) Bacteria.** Unicellular prokaryotes (kingdom Monera); round, rod-shaped or
spiral. A tough outer **capsule** lets some survive very hot or cold places. Most
are saprophytic **decomposers**; some make their own food; some are parasites
that cause disease. Examples: *Rhizobium*, *Azotobacter*, *Salmonella*,
cyanobacteria.

| Bacteria | Virus |
|---|---|
| a true cell (prokaryotic) | no cell; nucleic acid in a protein coat |
| living in all conditions; has metabolism | behaves as living only inside a host cell |
| can live freely, many are useful | always a parasite inside a cell |
| larger; seen with a light microscope | much smaller; needs an electron microscope |
| killed by antibiotics | not killed by antibiotics |

**(C) Amoeba.** A unicellular eukaryote (Protista) of water and moist soil. It has
no fixed shape; it moves and catches food with **pseudopodia** (false feet).
*Entamoeba histolytica* in dirty water causes **amoebic dysentery**.

**(D) Fungi.** Eukaryotes with a cell wall but no chlorophyll (kingdom Mycota).
Most are **saprophytes** living on dead and decaying matter; some are parasites.
The body is made of fine threads called **hyphae**, forming a **mycelium**.
Examples: *Mucor*, mushroom, yeast, *Penicillium*, yarsagumba (*Cordyceps*),
*Puccinia* (rust of wheat).

```photo id="sci8/bread-mould" caption="Mould growing on bread. It is a fungus: it has no chlorophyll and absorbs food from the bread through its thread-like hyphae." width="58"
key 1 Sporangium, which holds the spores
key 2 Mycelium of thread-like hyphae
```

### 3.4.1 Useful (positive) effects

1. *Amoeba proteus* feeds on bacteria, so it helps control them.
2. Decomposer bacteria (e.g. *Nitrosomonas*, *Nitrobacter*, *Clostridium*) break
   dead bodies and wastes into simple minerals, making the soil fertile and
   keeping the ecosystem in balance.
3. *Rhizobium* in the root nodules of legumes (pea, bean, gram) fixes
   atmospheric nitrogen, increasing soil fertility.
4. *Lactobacillus* turns milk into curd; *Streptococcus lactis* is used for cheese.
5. Bacteria and fungi are used to make antibiotics (penicillin from
   *Penicillium*), vaccines, insulin and vitamins.
6. **Yeast** ferments sugars into alcohol and acids (**fermentation**); it is used
   in bread, *jaand*, pickles and *gundruk*.
7. Bacteriophages kill bacteria and can be used against some bacterial
   infections and in water treatment.
8. Viruses are used in genetic engineering to transfer genes.

### 3.4.2 Harmful (negative) effects

1. They cause diseases in people, animals and crops, and reduce farm, fish, silk
   and honey production.
2. They spoil food and produce poisons, causing **food poisoning**.
3. They infect wounds and pimples; if the toxin enters the blood it can cause
   **sepsis**, which may be fatal.
4. They spoil stored grains and vegetables, causing loss to farmers.
5. Decomposing waste at dumping sites gives a foul smell and pollutes the air.

| Group | Diseases in humans | Plant diseases |
|---|---|---|
| Virus | COVID-19, common cold, AIDS, measles | tobacco mosaic |
| Bacteria | typhoid, tuberculosis, cholera, pneumonia | blight of rice, citrus canker |
| Protozoa | amoebic dysentery, malaria, giardiasis | — |
| Fungi | ringworm, athlete's foot | rust of wheat, root rot |

::: definition Food poisoning
**Food poisoning** is illness caused by eating food contaminated by microbes such
as *Clostridium*, *Salmonella*, norovirus or *Giardia* or by their toxins.
Symptoms: diarrhoea, vomiting, fever, dehydration, headache. *Prevention:* eat
fresh, well-cooked food; keep food covered; wash hands and utensils; never eat
stale or bad-smelling food.
:::

::: example Why does milk turn sour faster in summer?
**Reason.** *Lactobacillus* in milk changes milk sugar (lactose) into **lactic
acid**, which tastes sour and curdles the protein. Bacteria multiply faster in
warmth, so in summer the milk sours in a few hours.

**Conclusion.** Boil milk (kills most bacteria), cover it (stops new ones) and keep
it cool (slows growth). The same action of bacteria is used on purpose to make curd.
:::

## 3.5 Protection of food from microorganisms; vaccination

**Food preservation** is protecting food from microorganisms and keeping its
nutritional value so that it can be used for a long time. Microbes need
**moisture**, **warmth** and **air**; every method removes one of these.

| Method | How it is done | Why microbes cannot grow | Nepali examples |
|---|---|---|---|
| **Dry preservation** | drying in sun, oven or dryer at about 20–30 °C until very little moisture is left | no water for the microbes | grains, *sukuti* (dry meat), dry fish, *gundruk*, dry fruits |
| **Wet preservation** | washing or boiling the food, then dipping it in strong salt solution, lemon juice, vinegar or mustard oil in an airtight jar | salt, acid and oil stop microbes; airtight lid keeps spores out | lemon, chilli, radish and bamboo-shoot (*tama*) pickles |
| **Cold preservation** | keeping food at low temperature (about −18 °C to 4.4 °C) in a fridge or cold store | microbes become inactive or die | fruits and vegetables in cold stores; potatoes and ginger in covered pits |

::: caution Fungus in pickles
Fungus grows in a pickle when the vegetables were not dried properly, a wet spoon
was used, too little salt or oil was added, or the lid was not airtight. Dry the
vegetables well, use enough oil and salt, keep the jar airtight, and always use a
clean, dry spoon.
:::

**Vaccination.** A **vaccine** contains dead or weakened germs (or a part of them).
When it is given, the body makes **antibodies** without suffering the disease, so
later the real germ is destroyed quickly. This protection is called
**immunity**. Nepal's national immunisation programme gives children free
vaccines such as BCG (tuberculosis), polio, measles–rubella and others. Clean
water, hand-washing, covering food and controlling mosquitoes prevent the
diseases for which there is no vaccine.

## Chapter summary

- The **cell** is the structural and functional unit of life (Hooke, 1665).
- Parts: covering (cell wall + membrane), cytoplasm, cell components
  (organelles + inclusions), nucleus.
- Mitochondria = power house (ATP); chloroplast = photosynthesis; ribosome =
  protein factory; ER = endoskeleton; Golgi = secretion; lysosome = suicidal
  bag; nucleus = brain of the cell; human cells have 23 pairs of chromosomes.
- Plant cells have a cell wall, plastids and a large vacuole; animal cells do not.
- **Cell → tissue → organ → organ system → body.**
- Two-kingdom system: Linnaeus, 1753. Five-kingdom system: Whittaker, 1969 —
  Monera, Protista, Fungi, Plantae, Animalia.
- Virus = link between living and non-living; bacteria, amoeba and fungi have
  useful and harmful effects.
- Food preservation: dry, wet and cold methods remove moisture, add salt/acid/oil
  or lower the temperature. Vaccines give immunity.

## Practice questions

**Group A — Multiple choice (1 mark each)** *(Textbook exercises.)*

1. The branch of science that deals with the study of the cell is <span class="marks">[1]</span>
   (a) histology (b) cytology (c) cytogenetics (d) anatomy
2. In which form is the energy produced in a cell stored before it is given to the organelles? <span class="marks">[1]</span>
   (a) DNA (b) RNA (c) RBC (d) ATP
3. A common feature of the nuclear membrane and the cell membrane is that they <span class="marks">[1]</span>
   (a) help in transport (b) are made of pectin (c) are non-elastic (d) pass on heredity
4. Which function is done by both plant and animal cells? <span class="marks">[1]</span>
   (a) photosynthesis (b) cellular respiration (c) transpiration (d) guttation
5. What would happen if a cell had no cell membrane? <span class="marks">[1]</span>
   (a) organelles would be lost (b) the cell would die (c) only metabolism would stop (d) only the nucleus would be lost
6. Which function of the nucleus helps the growth of the body? <span class="marks">[1]</span>
   (a) making protein (b) transport (c) taking part in cell division (d) controlling all functions
7. Who proposed the two-kingdom system? <span class="marks">[1]</span>
   (a) Whittaker (b) Haeckel (c) Linnaeus (d) Aristotle
8. In the five-kingdom system, protozoans belong to <span class="marks">[1]</span>
   (a) Monera (b) Protista (c) Mycota (d) Animalia
9. Bacteria are called decomposers because they <span class="marks">[1]</span>
   (a) cause disease (b) infect wounds (c) live in extreme places (d) decay dead bodies and excreta
10. Which virus causes COVID-19? <span class="marks">[1]</span>
   (a) SARS-CoV-1 (b) SARS-CoV-2 (c) flu virus (d) rhinovirus
11. The main thing to be followed while preserving food is <span class="marks">[1]</span>
   (a) to prevent germs (b) drying well (c) keeping cold (d) adding salt
12. A feature of the five-kingdom system is that organisms are <span class="marks">[1]</span>
   (a) arranged in phylogenetic order (b) classified only by nutrition (c) classified by chlorophyll and growth (d) classified by movement
13. To preserve fresh, wet *gundruk*, it should be <span class="marks">[1]</span>
   (a) dried extremely in the sun (b) dried in the shade (c) dried leaving only the required small moisture (d) kept wet in an airtight bottle

::: note Answers to Group A
**1.** (b) — cytology. **2.** (d) — ATP (adenosine triphosphate). **3.** (a) — both control the passage of substances. **4.** (b) — every living cell respires. **5.** (b) — without the membrane nothing can be controlled or held in, so the cell dies. **6.** (c) — growth needs new cells. **7.** (c) — Linnaeus, 1753. **8.** (b) — Protista. **9.** (d). **10.** (b). **11.** (a) — every method aims to keep microbes out or inactive. **12.** (a) — from least developed to most developed. **13.** (c) — dried until only very little moisture is left, so microbes cannot grow but the food keeps its quality.
:::

**Group B — Short answer (2 marks each)**

1. Differentiate: (a) cytoplasm and nucleoplasm (b) chloroplast and chromoplast (c) cell wall and cell membrane (d) cell organelles and cell inclusions. <span class="marks">[4]</span>
2. Give reasons: (a) Ribosomes are called protein factories. (b) The cell wall gives a fixed shape to plant cells. (c) Metabolism occurs in the cytoplasm. (d) The cell is the basic unit of life. (e) Cells, tissues and organs must be coordinated for life processes. <span class="marks">[5]</span>
3. Where are mitochondria found in a cell? Write their functions. <span class="marks">[2]</span>
4. Which organelle digests itself, and why? <span class="marks">[2]</span>
5. Write the role of the Golgi body and the vacuole. <span class="marks">[2]</span>
6. Why is the nucleus called the brain of the cell? What happens if a cell has no nucleus? <span class="marks">[2]</span>
7. Differentiate between bacteria and virus. <span class="marks">[2]</span>
8. Give reasons: (a) A virus is called an infectious particle, not an organism. (b) We should not eat stale, smelly food. (c) The five-kingdom system gives a proper place to almost all organisms. (d) Fruits do not spoil if dried well. <span class="marks">[4]</span>
9. What is food poisoning? Write its causes and prevention. <span class="marks">[2]</span>
10. How is amoeba useful to people? <span class="marks">[2]</span>

::: note Answers to Group B
**1.** (a) Cytoplasm is the semi-liquid between the cell membrane and nucleus, holding organelles; nucleoplasm is the liquid inside the nucleus, holding the nucleolus and chromatin. (b) Chloroplast is a green plastid with chlorophyll that makes food; chromoplast is a coloured (non-green) plastid that colours flowers and fruits for pollination and dispersal. (c) See the table in 3.1.3: wall is non-living, tough, freely permeable, only in plants/fungi/bacteria; membrane is living, thin, semi-permeable, in all cells. (d) Organelles are living parts with a special job (mitochondria, ribosome); inclusions are non-living substances in the cytoplasm (water droplets, salt crystals, stored food, wastes).
**2.** (a) They join amino acids to make proteins. (b) It is tough, rigid and non-living and surrounds the membrane like a box. (c) The cytoplasm holds the enzymes, raw materials and organelles where the chemical reactions occur. (d) Every organism is made of cells and every life process takes place in cells. (e) Each life process needs many cells working as tissues, tissues working as organs and organs working as a system; if one level fails, the process stops.
**3.** In the cytoplasm of both plant and animal cells. Functions: oxidise glucose with oxygen to release energy stored as ATP (power house); contain DNA that passes on some hereditary characters.
**4.** The lysosome. It is full of digestive enzymes; when the enzyme level becomes very high, or the cell is old or damaged, the membrane breaks and the enzymes digest the cell itself — so it is called the suicidal bag.
**5.** Golgi body: secretes mucus, saliva, sweat and tears; sorts and packs proteins; helps form the new membrane or cell plate in division. Vacuole: stores cell sap, balances water and salts, and collects wastes before they are removed.
**6.** It controls and coordinates all activities of the cell and carries the hereditary material. Without a nucleus the cell cannot divide or control its work, and soon dies (e.g. mature red blood cells live only about 120 days).
**7.** See the bacteria–virus table in 3.4.
**8.** (a) It has no cell and no metabolism, and it shows life only inside a host cell. (b) Microbes have grown in it and made toxins, causing food poisoning. (c) It separates prokaryotes from eukaryotes, unicellular from multicellular, and gives fungi their own kingdom. (d) Microbes need water to grow; dried fruit has too little.
**9.** Illness from eating food spoiled by microbes or their toxins. Causes: stale, uncovered or undercooked food; dirty hands or utensils; germs like *Salmonella*, *Clostridium*, norovirus. Prevention: eat fresh, well-cooked, covered food; wash hands; keep food cold; avoid smelly food.
**10.** *Amoeba proteus* eats bacteria, so it is used to control bacteria (e.g. in cleaning waste water).
:::

**Group C — Long answer (4 marks each)**

1. Draw a labelled diagram of a plant cell and an animal cell, and complete a Venn diagram comparing them. <span class="marks">[4]</span>
2. Write the functions of the three kinds of plastids in a plant cell. What would happen to a plant with no chloroplasts? <span class="marks">[4]</span>
3. Write the merits and drawbacks of the two-kingdom system, and explain how the five-kingdom system corrected them. <span class="marks">[4]</span>
4. What are the methods of food preservation? Describe one, and write the importance of food preservation. Why does fungus grow in a pickle jar, and how can it be stopped? <span class="marks">[4]</span>
5. What is a microorganism? Give one example from each group, write four advantages of microorganisms, and name two diseases caused by each group. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** Draw as in the figure in 3.1.3. *Plant only:* cell wall, plastids, large central vacuole. *Animal only:* irregular shape, small vacuoles, central nucleus. *Both:* cell membrane, cytoplasm, nucleus, mitochondria, ribosomes, ER, Golgi body.
**2.** Chloroplast: makes food by photosynthesis, gives green colour, helps make fatty acids and amino acids. Chromoplast: gives colour to flowers and fruits to attract insects and birds for pollination and seed dispersal. Leucoplast: stores starch, protein and fat. Without chloroplasts the plant could not make food, so it would not grow and would die; animals that depend on it would also suffer.
**3.** Merits: first scientific system; simple; easy to tell plants from animals. Drawbacks: fungi put with plants; prokaryotic bacteria and eukaryotic algae put together; unicellular and multicellular not separated; lichens and *Euglena* had no place. Correction: Whittaker's five-kingdom system put prokaryotes in Monera, unicellular eukaryotes in Protista, fungi in their own kingdom Fungi, and kept only green multicellular plants in Plantae and multicellular consumers in Animalia.
**4.** Dry, wet and cold preservation (table in 3.5). *Wet preservation:* the food is washed or boiled, dried, then kept in strong salt solution, lemon juice, vinegar or mustard oil in an airtight jar; e.g. lemon pickle. *Importance:* food lasts longer, nutrients are kept, seasonal food is available all year, loss to farmers is reduced and food poisoning is prevented. Fungus grows when moisture or air enters (wet vegetables, wet spoon, loose lid, too little oil or salt); prevent it by drying well, using enough oil and salt, an airtight lid and a dry spoon.
**5.** Microorganisms are living beings too small to see without a microscope. Examples: virus — coronavirus; bacteria — *Rhizobium*; protozoa — *Amoeba*; fungi — yeast; algae — *Chlamydomonas*. Advantages: decomposition and soil fertility; nitrogen fixation; curd and cheese; antibiotics and vaccines; fermentation (bread, *jaand*). Diseases: virus — COVID-19, common cold; bacteria — typhoid, tuberculosis; protozoa — malaria, amoebic dysentery; fungi — ringworm, athlete's foot.
:::
