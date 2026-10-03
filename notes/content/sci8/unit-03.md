---
subject: Science and Technology
grade: 8
title: Living Beings and Their Structure
unit: 3
hours: 0
area: Science and Technology
---

Every living thing, from the moss on a wall to the blue whale, is built from
cells. Some living things are a single cell and nothing else; a human being is
about thirty trillion cells arranged into tissues, organs and systems. This
unit looks at the cell first, then at how cells build a body, then at how
biologists sort the millions of living things into groups, and finally at the
microorganisms you cannot see — the ones that make curd and the ones that make
you ill.

::: key What this unit asks of you
You should be able to draw and label a plant cell and an animal cell and state
the function of each organelle, explain how cells form tissues, organs and organ
systems, name the five kingdoms and the classes of vertebrates with one example
each, and describe the useful and the harmful effects of microorganisms.
:::

## 3.1 The cell

The **cell** is the smallest living unit of a body. Robert Hooke saw the first
cells in 1665 in a slice of cork and gave them the name *cellulae*, meaning
little rooms. The statement that all living things are made of cells, and that
every cell comes from an existing cell, is called the **cell theory**.

### 3.1.1 Parts of a cell and their work

```figure caption="A plant cell and an animal cell side by side. The plant cell has a thick cell wall, a large central vacuole and chloroplasts; the animal cell has none of them and its vacuoles are small."
fig, ax = plt.subplots(figsize=(5.0, 2.9))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5.8)
ax.axis("off")
ax.add_patch(plt.Rectangle((0.5, 0.9), 3.9, 4.1, fc="#dbe8d2", ec=INK, lw=1.6))
ax.text(2.45, 5.25, "Plant cell", ha="center", fontsize=7.6, color=INK)
ax.add_patch(plt.Circle((6.9, 2.95), 2.05, fc="#f5e2dc", ec=INK, lw=1.6))
ax.text(6.9, 5.25, "Animal cell", ha="center", fontsize=7.6, color=INK)
ax.add_patch(plt.Circle((2.45, 2.6), 0.42, fc=ACCENT, alpha=0.55))
ax.text(2.45, 3.6, "nucleus", ha="center", fontsize=6.2, color=INK)
ax.add_patch(plt.Rectangle((0.95, 1.25), 1.0, 1.2, fc="white", ec=ACCENT, lw=1.0))
ax.text(1.45, 1.85, "vacuole", ha="center", va="center", fontsize=5.9, color=ACCENT)
for cx, cy in [(3.3, 1.5), (3.7, 2.9), (2.0, 4.1)]:
    ax.add_patch(plt.Circle((cx, cy), 0.2, fc=SERIES[2], alpha=0.8))
ax.text(3.85, 4.35, "chloroplast", ha="center", fontsize=6.2, color=SERIES[2])
ax.text(1.0, 0.45, "cell wall + cell membrane", ha="left", fontsize=6.2, color=MUTED)
ax.add_patch(plt.Circle((6.9, 3.1), 0.42, fc=ACCENT, alpha=0.55))
ax.text(6.9, 4.1, "nucleus", ha="center", fontsize=6.2, color=INK)
for cx, cy in [(6.1, 2.2), (7.7, 2.4)]:
    ax.add_patch(plt.Circle((cx, cy), 0.22, fc="white", ec=ACCENT, lw=1.0))
ax.text(8.65, 1.9, "small\\nvacuoles", ha="center", fontsize=6.0, color=ACCENT)
ax.text(6.9, 0.45, "cell membrane only", ha="center", fontsize=6.2, color=MUTED)
ax.text(5.0, 0.02, "both cells contain cytoplasm and mitochondria", ha="center",
        fontsize=6.3, color=MUTED)
fig.tight_layout()
```

| Part | Present in | Function |
|---|---|---|
| Cell wall | plant cells only | gives shape and strength; made of cellulose |
| Cell membrane | both | controls what enters and leaves the cell |
| Cytoplasm | both | the jelly in which the other parts float and reactions happen |
| Nucleus | both | contains the chromosomes; controls all the cell's activities |
| Mitochondria | both | release energy from food; the cell's power house |
| Vacuole | both | stores water and dissolved substances; large and central in plants |
| Chloroplast | plant cells only | contains chlorophyll and makes food by photosynthesis |
| Ribosome | both | builds proteins |
| Plastid | plant cells only | stores starch, oil or colour |

::: definition Cell
A **cell** is the smallest structural and functional unit of a living being,
capable of carrying out all the processes of life.
:::

```photo id="sci8/cheek-cells" caption="Human cheek cells under a light microscope. The dark oval in each cell is the nucleus, and the pale ring around it is cytoplasm." width="70"
key 1 Nucleus
key 2 Cytoplasm
key 3 Cell membrane
```
::: caution Three mistakes students make in cell diagrams
**(1)** Drawing the cell wall and the cell membrane as one line in a plant cell.
Draw the wall as a thick outer line and the membrane as a thin line just inside
it. **(2)** Putting chloroplasts in an animal cell — they belong to plants only.
**(3)** Forgetting the label lines: a diagram with the names but no lines to the
parts earns no marks.
:::

## 3.2 From cell to organ system

Cells of the same kind, doing the same job, join to form a **tissue**. Two or
more tissues working together form an **organ**. Organs that work together on
the same job form an **organ system**, and the systems together make the whole
body.

```figure caption="The five levels of organisation in the human body. Each level is built from the one below it, and the whole body works only when all the levels do."
fig, ax = plt.subplots(figsize=(5.0, 2.6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5.4)
ax.axis("off")
levels = [("Cell", 1.0, "muscle cell"), ("Tissue", 3.0, "muscle tissue"),
          ("Organ", 5.0, "stomach"), ("Organ system", 7.0, "digestive system"),
          ("Body", 9.0, "the whole human")]
for name, x, ex in levels:
    ax.text(x, 3.5, name, ha="center", va="center", fontsize=7.0, color=INK,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=ACCENT, lw=1.0))
    ax.text(x, 2.55, ex, ha="center", va="center", fontsize=6.1, color=MUTED)
    if x < 9.0:
        ax.annotate("", xy=(x + 1.3, 3.5), xytext=(x + 0.6, 3.5),
                    arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1))
ax.text(5.0, 1.3, "A group of cells that does the same job is a tissue;", ha="center",
        fontsize=6.6, color=INK)
ax.text(5.0, 0.72, "a group of tissues that does the same job is an organ.",
        ha="center", fontsize=6.6, color=INK)
fig.tight_layout()
```

| Organ system | Main organs | Job |
|---|---|---|
| Digestive | mouth, oesophagus, stomach, small and large intestine, liver | breaks food down and absorbs it |
| Respiratory | nose, trachea, bronchi, lungs | takes in oxygen and gives out carbon dioxide |
| Circulatory | heart, blood, blood vessels | carries food, oxygen and waste around the body |
| Excretory | kidneys, ureters, bladder, skin | removes waste such as urea and extra salts |
| Nervous | brain, spinal cord, nerves | senses and controls everything |
| Skeletal and muscular | bones and muscles | support, movement and protection |
| Reproductive | testes, ovaries and related organs | produces the young ones |

::: tip Learn the levels as a sentence
**Cells make tissues, tissues make organs, organs make systems, systems make
the body.** Say that sentence once before every answer about organisation, and
you will never put an organ under a tissue in the wrong order.
:::

## 3.3 Classification of living beings

There are millions of kinds of living being on the earth. Classification means
sorting them into groups according to their shared features, so that each kind
has one name and one place.

The broadest grouping used today is the **five-kingdom system** proposed by
R. H. Whittaker in 1969.

```figure caption="The five kingdoms. The system sorts living things first by the kind of cell, then by how they obtain food, and then by how their body is organised."
fig, ax = plt.subplots(figsize=(5.1, 3.0))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6.6)
ax.axis("off")
ax.text(5.0, 6.1, "Living beings", ha="center", fontsize=8.0, color=INK,
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=INK, lw=1.2))
kings = [("Monera", "bacteria\\nno true nucleus", 1.0),
         ("Protista", "Amoeba, Paramecium\\nsingle celled", 3.0),
         ("Fungi", "mushroom, mould\\ncell wall, no chlorophyll", 5.0),
         ("Plantae", "green plants\\nmake their own food", 7.0),
         ("Animalia", "animals\\ntake ready-made food", 9.0)]
for name, note, x in kings:
    ax.plot([5.0, x], [5.75, 4.5], color=GRID, lw=0.9)
    ax.text(x, 4.05, name, ha="center", va="center", fontsize=7.0, color=ACCENT,
            bbox=dict(boxstyle="round,pad=0.28", fc="white", ec=ACCENT, lw=1.0))
    ax.text(x, 2.9, note, ha="center", va="center", fontsize=5.9, color=INK)
ax.text(5.0, 1.35, "Monera and Protista have no organised tissue;", ha="center",
        fontsize=6.4, color=MUTED)
ax.text(5.0, 0.8, "Fungi absorb their food, plants make it, animals eat it.",
        ha="center", fontsize=6.4, color=MUTED)
fig.tight_layout()
```

| Kingdom | Kind of cell | How it feeds | Examples |
|---|---|---|---|
| Monera | no true nucleus (prokaryotic) | absorbs or makes its own food | bacteria, cyanobacteria |
| Protista | true nucleus, one cell | absorbs, or moves and engulfs | Amoeba, Paramecium, Euglena, algae |
| Fungi | true nucleus, cell wall | absorbs dissolved food from dead matter | mushroom, yeast, mould |
| Plantae | true nucleus, cell wall, chlorophyll | makes food by photosynthesis | moss, fern, pine, bamboo, rice |
| Animalia | true nucleus, no cell wall | eats ready-made food | earthworm, fish, frog, cow, human |

### 3.3.1 The vertebrates

The kingdom Animalia is very large, so it is divided further. Animals with a
backbone are **vertebrates**; those without are invertebrates (insects,
molluscs and worms). The vertebrates are divided into five classes.

| Class | Skin and covering | Breathing | Reproduces by | Example |
|---|---|---|---|---|
| Pisces (fish) | wet scales | gills | laying eggs in water | rohu, trout |
| Amphibia | moist, no scales | gills when young, lungs and skin as adult | eggs in water | frog, toad |
| Reptilia | dry scaly | lungs | eggs with a leathery shell on land | snake, lizard, tortoise |
| Aves (birds) | feathers | lungs | hard-shelled eggs | sparrow, danphe, duck |
| Mammalia | hair or fur | lungs | gives birth to live young and feeds milk | cow, bat, whale, human |

::: caution A whale is not a fish
A whale lives in water and has fins, so students often put it with the fish.
But it has hair, it breathes air through lungs and it feeds its young with
milk. Classification follows structure, not the place where the animal lives.
:::

## 3.4 Effects of microorganisms

**Microorganisms** are living beings so small that they cannot be seen with the
naked eye; a microscope is needed. They are found in the five kingdoms, but the
ones that matter most in daily life are bacteria, fungi, protozoa and some
algae.

```photo id="sci8/paramecium" caption="Paramecium, a single-celled animal of the kingdom Protista, seen through a microscope. The beating hair-like cilia around it push it through the water." width="62"
key 1 Cilia, used for movement
key 2 Food vacuole
key 3 Contractile vacuole, which removes extra water
```
### 3.4.1 Useful microorganisms

| Microorganism | What it does for us |
|---|---|
| Bacteria (Lactobacillus) | turns milk into curd and *mohi* |
| Yeast (a fungus) | makes dough rise for bread; ferments *jaand* and wine |
| Bacteria in the soil | fix nitrogen and decompose dead matter into humus |
| Bacteria in the intestine | help digestion and make some vitamins |
| Fungi (Penicillium) | the source of the antibiotic penicillin |
| Algae | make oxygen in water and food for fish |
| Bacteria in sewage treatment | clean waste water |

```photo id="sci8/bread-mould" caption="Rhizopus, the mould that grows on bread and over-ripe fruit. It is a fungus: it has no chlorophyll, so it feeds by absorbing dissolved food from the bread." width="62"
key 1 Sporangium, which holds the spores
key 2 Spores
key 3 Mycelium, the thread-like feeding part
```
### 3.4.2 Harmful microorganisms and protection from them

Harmful microorganisms are called **pathogens**. They cause diseases in people,
animals and crops, and they spoil food.

| Disease | Caused by | Spreads through |
|---|---|---|
| Typhoid | bacteria | contaminated water and food |
| Cholera | bacteria | contaminated water |
| Tuberculosis | bacteria | droplets in the air when a patient coughs |
| Common cold, influenza | virus | droplets and touch |
| Dysentery (amoebiasis) | protozoan | contaminated water and food |
| Ringworm | fungus | skin contact and shared clothes |
| Malaria | protozoan | the bite of an infected mosquito |
| Damping off of seedlings | fungus | soil |

**Ways to protect yourself.**

1. Drink boiled or filtered water.
2. Wash hands with soap before eating and after using the toilet.
3. Cover the mouth and nose when coughing or sneezing.
4. Keep food covered; do not eat food that is old or smells wrong.
5. Keep the house and the surroundings clean; do not let water stand in
   old tyres, pots and drains, because mosquitoes breed there.
6. Get the vaccination that the health post offers — measles, BCG, polio and
   others. A vaccine teaches the body to defend itself before the germ arrives.

```photo id="sci8/onion-root" caption="Cells of an onion root tip, stained to show the nucleus. The cells near the tip are dividing, which is why a root tip is used to study cell division." width="80"
key 1 Nucleus
key 2 Dividing cell
key 3 Root tip tissue
```
::: example Worked reasoning: why does milk turn sour in summer?
**Observation.** Fresh milk kept in an open glass turns sour in a few hours in
Asar, but stays good for most of a day in winter.

**Reason.** Milk contains *Lactobacillus* bacteria. They feed on the sugar in
milk (lactose) and change it into lactic acid. The more acid produced, the
sourer the taste, and the acid also makes the milk protein curdle. Bacteria
multiply faster in warmth, so in hot weather the same number of bacteria doubles
every twenty minutes or so and the milk turns sour quickly.

**Practical conclusion.** Boil the milk and keep it covered in a cool place, or
use a refrigerator. Boiling kills most of the bacteria; covering keeps new ones
from falling in. The same reaction is used on purpose to make curd and *mohi*
from milk.
:::

## Chapter summary

- The **cell** is the smallest living unit; the cell theory says all living
  things are made of cells and every cell comes from a cell.
- Plant cells have a cell wall, chloroplasts and a large central vacuole; animal
  cells do not.
- The nucleus controls the cell, mitochondria release energy, chloroplasts make
  food, the membrane controls entry and exit.
- **Cell → tissue → organ → organ system → body.**
- The **five kingdoms** are Monera, Protista, Fungi, Plantae and Animalia,
  sorted mainly by cell type and the way they feed.
- The five vertebrate classes are Pisces, Amphibia, Reptilia, Aves and
  Mammalia; classification follows structure, not habitat.
- Microorganisms are useful (curd, bread, nitrogen fixing, antibiotics, sewage
  treatment) and harmful (typhoid, cholera, ringworm, food spoilage).
- Boiled water, soap, covered food, clean surroundings and vaccination are the
  five practical defences against disease.

## Practice questions

**Group A — Objective (1 mark each)**

1. The part of the cell that controls its activities is the
   <span class="marks">[1]</span>
   (a) cytoplasm (b) nucleus (c) vacuole (d) cell membrane
2. Which of these is present in a plant cell but not in an animal cell?
   <span class="marks">[1]</span>
   (a) nucleus (b) mitochondrion (c) chloroplast (d) cytoplasm
3. A group of similar cells doing the same work is called a
   <span class="marks">[1]</span>
   (a) tissue (b) organ (c) system (d) organism
4. Amoeba belongs to the kingdom <span class="marks">[1]</span>
   (a) Monera (b) Protista (c) Fungi (d) Animalia
5. A whale is classified as a mammal because it
   <span class="marks">[1]</span>
   (a) lives in water (b) has a large body (c) breathes through lungs and feeds
   milk (d) has fins
6. Which microorganism turns milk into curd? <span class="marks">[1]</span>
   (a) yeast (b) Lactobacillus (c) Plasmodium (d) Penicillium

::: note Answers to Group A
**1.** (b) — the nucleus holds the chromosomes and directs the cell.
**2.** (c) — chloroplasts carry chlorophyll, which animals never have.
**3.** (a) — same kind of cells, same work, is a tissue.
**4.** (b) — Amoeba is a single-celled organism with a true nucleus.
**5.** (c) — hair, lungs and milk are mammal features.
**6.** (b) — Lactobacillus turns lactose into lactic acid.
:::

**Group B — Short answer (2 marks each)**

1. Write the functions of any four parts of a plant cell.
   <span class="marks">[2]</span>
2. Distinguish between a tissue and an organ with one example each.
   <span class="marks">[2]</span>
3. Write the five kingdoms with one example of each.
   <span class="marks">[2]</span>
4. Name two useful and two harmful microorganisms, with the effect of each.
   <span class="marks">[2]</span>

::: note Answers to Group B
**1.** Any four: nucleus (controls all activities); chloroplast (makes food by
photosynthesis); cell wall (gives shape and support); vacuole (stores water and
dissolved substances); mitochondrion (releases energy); cell membrane (controls
what enters and leaves).
**2.** A tissue is a group of similar cells doing the same work — muscle tissue,
for example. An organ is a group of different tissues working together on one
job — the stomach, which has muscle tissue, glandular tissue and lining tissue.
**3.** Monera — bacteria; Protista — Amoeba or Paramecium; Fungi — mushroom,
yeast or mould; Plantae — bamboo, fern or pine; Animalia — earthworm, frog,
cow or human.
**4.** Useful: Lactobacillus, which makes curd; yeast, which makes dough rise
and is used in fermentation. Harmful: *Plasmodium*, which causes malaria, spread
by mosquitoes; the fungus that causes ringworm, spread by skin contact and
shared clothes.
:::

**Group C — Long answer (4 marks each)**

1. Draw a labelled diagram of a plant cell and an animal cell side by side, and
   write three differences between them. <span class="marks">[4]</span>
2. What are microorganisms? Describe any three uses of microorganisms in daily
   life and any three diseases they cause, with the way each disease spreads.
   <span class="marks">[4]</span>

::: note Answers to Group C
**1.** **Diagram.** Two large circles or rectangles, the plant cell a rectangle
with a thick double boundary (cell wall outside, cell membrane inside) and the
animal cell a circle with a single thin boundary. Label nucleus, cytoplasm,
cell membrane, cell wall, chloroplast and vacuole on the plant cell; nucleus,
cytoplasm and cell membrane on the animal cell. **Three differences.**
(i) A plant cell has a cell wall of cellulose; an animal cell has only a cell
membrane. (ii) A plant cell has chloroplasts and can make its own food; an
animal cell has none and must take ready-made food. (iii) A plant cell has one
large central vacuole; an animal cell has small scattered vacuoles.
**2.** **Microorganisms** are living beings too small to be seen with the naked
eye, visible only under a microscope. **Uses.** (i) *Lactobacillus* turns milk
into curd, *mohi* and cheese. (ii) Yeast makes bread dough rise by giving out
carbon dioxide, and is used in fermentation. (iii) Soil bacteria fix nitrogen
and decompose dead matter into humus, and *Penicillium* gives us the antibiotic
penicillin. **Diseases.** (i) Typhoid, a bacterial disease spread through
contaminated water and food. (ii) Ringworm, a fungal disease spread by skin
contact and shared clothes. (iii) Malaria, caused by a protozoan and spread by
the bite of an infected *Anopheles* mosquito. Protection: boiled water, soap,
covered food, clean surroundings and vaccination.
:::
