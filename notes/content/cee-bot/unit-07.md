---
subject: Botany
grade: CEE
unit: 7
title: Cell Biology and Cell Division
hours: 5
area: Cell Biology
---

Cell Biology and Cell Division is the **heaviest unit in the Botany paper — 5 of the
40 questions** — and the most predictable. One question usually comes from the cell
theory or the prokaryote/eukaryote comparison, two or three from organelle structure and
function, and one or two from the cell cycle and the differences between mitosis and
meiosis. The numbers are what examiners love: 70S and 80S, 9+2, 46 and 23, 2C and 4C.
Learn the tables and count chromosomes carefully; this unit is where careless students
lose marks they knew.

::: key What the paper asks from this chapter
- **Cell theory and its exceptions** — Schleiden, Schwann, Virchow; viruses are acellular, coenocytic hyphae are multinucleate without cross walls.
- **Prokaryote versus eukaryote** — 70S versus 80S ribosomes, nucleoid versus nucleus, peptidoglycan versus cellulose, binary fission versus mitosis.
- **Organelle structure and function** — cristae, grana, cisternae, cis and trans faces, hydrolytic enzymes, the nucleolus, the nuclear pore.
- **The wall in three layers** — middle lamella (calcium pectate), primary wall, secondary wall (lignin).
- **Chromosome vocabulary** — chromatid, centromere, telomere, nucleosome (DNA + histone octamer).
- **9+2** — the microtubule arrangement of eukaryotic cilia and flagella; bacterial flagella are flagellin and have no 9+2.
- **The cell cycle** — G1, S, G2, M, G0; DNA replicates in S; checkpoints at G1/S and G2/M.
- **Mitosis versus meiosis** — one division versus two, 2n → 2n versus 2n → 4 × n, cell plate versus cleavage furrow, and the chromosome and DNA counts at each stage.
:::

## 7.1 Prokaryotic and eukaryotic cells; the cell theory

### How the cell was discovered, and the cell theory

| Year | Person | Contribution |
|---|---|---|
| 1665 | **Robert Hooke** | saw the empty "cells" (dead cork cell walls) and coined the word *cell* |
| 1674 | **Antonie van Leeuwenhoek** | first saw living cells — bacteria and protozoa in pond water |
| 1831 | **Robert Brown** | discovered the **nucleus** in orchid cells |
| 1838 | **Matthias Schleiden** | all **plants** are made of cells |
| 1839 | **Theodor Schwann** | all **animals** are made of cells; proposed the cell theory with Schleiden |
| 1855 | **Rudolf Virchow** | ***omnis cellula e cellula*** — every cell arises from a pre-existing cell |
| 1931 | **Ernst Ruska** | built the electron microscope, which made organelles visible |

The **cell theory** in its modern form says four things: the cell is the **structural and
functional unit** of all living organisms; all organisms are made of **one or more
cells**; new cells arise **only by division of existing cells**; and all cells are
chemically similar, containing DNA, RNA, protein and a plasma membrane.

```photo id="bio11/microscope" caption="A binocular compound light microscope. The first instrument a Grade 11 biology student must be able to name part by part — most practical examinations begin here." width="68"
crop 0.04 0.02 0.96 0.99
mark 0.30 0.93 "1"
mark 0.52 0.79 "2"
mark 0.47 0.665 "3"
mark 0.40 0.575 "4"
mark 0.33 0.485 "5"
mark 0.46 0.385 "6"
mark 0.80 0.345 "7"
mark 0.78 0.60 "8"
mark 0.55 0.10 "9"
key 1 eyepiece (ocular lens)
key 2 body tube and head
key 3 revolving nosepiece
key 4 objective lenses
key 5 stage with clips
key 6 condenser and iris diaphragm
key 7 coarse and fine focus knobs
key 8 arm
key 9 base with illuminator
```


**Exceptions.** The theory has three standard exceptions:

1. **Viruses, viroids and prions** are **acellular** — they have no cell, no cytoplasm and no ribosomes, and cannot reproduce outside a host.
2. **Coenocytic (aseptate) structures** — the hyphae of *Mucor* and *Rhizopus* are a single continuous mass of cytoplasm with **many nuclei and no cross walls**; the latex vessels of plants and striated muscle fibres are also multinucleate. One "cell" holds many nuclei.
3. **Prokaryotes** have no membrane-bound nucleus or organelles, so the classical statement "every cell has a nucleus" does not apply to them — though they are still cells.

### Prokaryotic and eukaryotic cells compared

| Feature | Prokaryotic cell | Eukaryotic cell |
|---|---|---|
| Typical size | 1–10 μm | 10–100 μm |
| **Nucleus** | **absent**; DNA lies in a **nucleoid** | **present**, with a double nuclear envelope and pores |
| DNA | circular, naked (no histone proteins in bacteria), one main chromosome | linear, bound to histones, many chromosomes |
| Extra DNA | **plasmids** | only inside mitochondria and chloroplasts |
| **Ribosomes** | **70S** (50S + 30S) | **80S** (60S + 40S) in the cytoplasm; 70S in mitochondria and chloroplasts |
| Membrane-bound organelles | **none** — no mitochondria, ER, Golgi, lysosome, chloroplast | present |
| Respiratory enzymes | on the **plasma membrane** and its infoldings (mesosomes) | on the inner mitochondrial membrane |
| **Cell wall** | **peptidoglycan** (murein); absent in *Mycoplasma* | **cellulose** in plants, **chitin** in fungi, absent in animals |
| Cell division | **binary fission** (amitosis), no spindle | **mitosis** and **meiosis**, with a spindle |
| **Flagella** | **flagellin**, single fibril, no 9+2, rotates | **tubulin**, 9+2 axoneme, bends |
| Other surface structures | pili, fimbriae, capsule | cilia, microvilli, glycocalyx |
| Cytoskeleton | poorly developed | microtubules, microfilaments, intermediate filaments |
| Examples | bacteria, cyanobacteria, mycoplasma, archaea | protists, fungi, plants, animals |

```figure caption="(a) A prokaryotic cell: no nucleus, circular DNA in a nucleoid, 70S ribosomes, and a flagellum of flagellin. (b) A eukaryotic cell: a true nucleus, membrane-bound organelles and a cell wall."
fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.9), gridspec_kw={"width_ratios": [1, 1.12]})
def lab(ax, xy, txy, s, c=INK, ha="left"):
    ax.annotate(s, xy=xy, xytext=txy, fontsize=8.2, color=c, ha=ha, va="center",
                arrowprops=dict(arrowstyle="-", color="#7a8494", lw=0.8, shrinkA=1, shrinkB=0))
ax = axs[0]; ax.set_xlim(0, 10); ax.set_ylim(0, 8); ax.axis("off"); ax.set_aspect("equal")
ax.add_patch(matplotlib.patches.FancyBboxPatch((1.2, 3.0), 6.4, 2.6, boxstyle="round,pad=0,rounding_size=1.2", fc="#f3efe2", ec="#3b7d3b", lw=2.4))
ax.add_patch(matplotlib.patches.FancyBboxPatch((1.0, 2.8), 6.8, 3.0, boxstyle="round,pad=0,rounding_size=1.3", fc="none", ec="#8fbf8f", lw=0.9))
t = np.linspace(0, 6.3, 120)
ax.plot(3.2 + 1.5 * np.cos(t) * (0.6 + 0.12 * np.sin(5 * t)), 4.3 + 0.7 * np.sin(t) * (0.6 + 0.12 * np.cos(4 * t)), color="#4a4f5c", lw=1.5)
ax.add_patch(Circle((5.9, 4.9), 0.35, fc="none", ec="#6a5acd", lw=1.3))
for x, y in [(5.0, 3.6), (5.6, 3.9), (6.4, 3.5), (4.6, 5.0), (6.8, 4.3), (4.2, 3.5)]: ax.add_patch(Circle((x, y), 0.14, fc="#c0392b", ec="none"))
xs = np.linspace(7.6, 9.8, 60); ax.plot(xs, 4.3 + 0.35 * np.sin((xs - 7.6) * 3.4), color="#7a5230", lw=1.8)
lab(ax, (3.2, 4.6), (2.2, 7.3), "nucleoid (circular DNA)")
lab(ax, (5.9, 5.2), (6.1, 7.0), "plasmid", "#6a5acd")
lab(ax, (5.0, 3.6), (4.3, 1.6), "70S ribosomes", "#c0392b")
lab(ax, (1.1, 3.6), (0.1, 0.35), "cell wall + membrane", "#3b7d3b")
lab(ax, (9.2, 4.55), (7.5, 2.0), "flagellum", "#7a5230")
ax.text(4.5, -0.9, "(a) prokaryote", ha="center", fontsize=9, fontweight="bold")
ax = axs[1]; ax.set_xlim(0, 11); ax.set_ylim(0, 8); ax.axis("off"); ax.set_aspect("equal")
ax.add_patch(Ellipse((5.2, 4.2), 9.6, 6.6, fc="#eef6ec", ec="#2f7d3b", lw=2.4))
ax.add_patch(Ellipse((5.2, 4.2), 9.1, 6.1, fc="none", ec="#8fbf8f", lw=0.9))
ax.add_patch(Circle((4.4, 4.7), 1.35, fc="#cfe0f2", ec="#1d6fb8", lw=1.8)); ax.add_patch(Circle((4.1, 4.9), 0.42, fc="#1d4f8a", ec="none"))
ax.add_patch(Ellipse((7.6, 5.5), 1.9, 0.85, angle=25, fc="#e9a38b", ec="#b0472c", lw=1.3))
for dx in (-0.5, -0.1, 0.3, 0.7): ax.plot([7.6 + dx * 0.9 - 0.15, 7.6 + dx * 0.9 + 0.15], [5.3 + dx * 0.4, 5.6 + dx * 0.4], color="#b0472c", lw=0.9)
ax.add_patch(Ellipse((6.8, 2.5), 2.6, 1.0, angle=-15, fc="#9fd09b", ec="#2f7d3b", lw=1.3))
for dx in (-0.8, -0.3, 0.2, 0.7): ax.plot([6.8 + dx - 0.2, 6.8 + dx + 0.2], [2.5 - dx * 0.25 + 0.0, 2.5 - dx * 0.25 + 0.0], color="#2f7d3b", lw=1.6)
ax.add_patch(Ellipse((2.6, 2.6), 2.4, 1.7, fc="#e7ecf5", ec="#8a96a8", lw=1.1))
lab(ax, (4.0, 5.9), (1.0, 7.5), "nucleus", "#1d6fb8")
lab(ax, (4.1, 4.9), (0.2, 1.7), "nucleolus", "#1d4f8a")
lab(ax, (7.9, 5.9), (6.0, 7.75), "mitochondrion", "#b0472c")
lab(ax, (7.6, 2.1), (8.6, 0.9), "chloroplast", "#2f7d3b")
lab(ax, (2.6, 2.6), (4.6, 0.3), "vacuole", "#5b6472")
lab(ax, (9.5, 5.6), (9.4, 6.9), "cell wall", "#2f7d3b")
ax.text(5.2, -0.9, "(b) eukaryote (plant cell)", ha="center", fontsize=9, fontweight="bold")
fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.08, wspace=0.03)
```

```photogrid label="7.2" cols="2" ratio="1.2" caption="What a cell looks like at each magnification. (a) A compound light microscope with its eyepiece (10x) and rotating objectives. (b) Total magnification is eyepiece times objective, so the 4x, 10x and 40x objectives give 40, 100 and 400 times. With a field number of 18 mm the width of the field is 18/objective: 4.50 mm, 1.80 mm and 0.45 mm. A cell that fills one twentieth of the field at 400x is therefore about 22.5 micrometres across, which is why plant cells (10 to 100 micrometres) are visible but a bacterium (1 to 5 micrometres) is only a dot."
@ photo id="bio11/microscope" cap="A compound microscope"
fit 1.2
focus 0.5 0.5
@ svg cap="Field of view at 40x, 100x and 400x (field number 18 mm)"
fn, eye = 18.0, 10
objs = (4, 10, 40)
tot = [eye * o for o in objs]
fov = [fn / o for o in objs]
cell = fov[2] / 20 * 1000
assert tot == [40, 100, 400] and abs(fov[2] - 0.45) < 1e-12 and abs(cell - 22.5) < 1e-9
facts = dict(m1=tot[0], m2=tot[1], m3=tot[2], d1="%.2f" % fov[0], d2="%.2f" % fov[1], d3="%.2f" % fov[2], cell="%.1f" % cell)
f = Fig(300, 236)
f.text(150, 12, "Field of view (circle diameter to scale)", size=10.5, color=NAVY, bold=True)
sc = 160 / fov[0]
for d, t, col in zip(fov, tot, (NAVY, TEAL, RED)):
    f.circle(110, 108, d * sc / 2, fill="none", stroke=col, sw=2)
f.text(110, 44, "40x: 4.50 mm", size=10.5, color=NAVY, bold=True)
f.line(133, 90, 200, 66, color=TEAL)
f.text(204, 66, "100x: 1.80 mm", size=10.5, color=TEAL, bold=True, anchor="start", vmid=True)
f.line(110, 108, 200, 108, color=RED)
f.text(204, 108, "400x: 0.45 mm", size=10.5, color=RED, bold=True, anchor="start", vmid=True)
f.text(150, 206, "one cell = 1/20 of field = 22.5 um", size=10.5, color=NAVY, bold=True)
```

## 7.2 The cell wall, the membrane and the organelles

### The cell wall

Only plants, fungi and bacteria have a wall; animal cells do not. A plant cell wall has
**three parts**, laid down in this order:

| Layer | Position | Composition | Property |
|---|---|---|---|
| **Middle lamella** | outermost boundary between two neighbouring cells, formed **first** at cytokinesis | **calcium pectate** (and magnesium pectate) | cements the cells together; digested by pectinase when fruit softens |
| **Primary wall** | between the middle lamella and the plasma membrane | cellulose microfibrils in a matrix of hemicellulose, pectin and glycoprotein | thin, elastic, allows the cell to grow |
| **Secondary wall** | deposited inside the primary wall after growth stops | cellulose plus **lignin** (in xylem and sclerenchyma) | thick, rigid, three sub-layers (S1, S2, S3); gives strength and waterproofing |

**Plasmodesmata** are fine cytoplasmic channels that pass through the wall and connect
the cytoplasm of adjacent cells. The wall's functions are support, protection, a limit
to water uptake (which is why a plant cell does not burst in pure water), and transport
through the plasmodesmata. Bacterial walls are **peptidoglycan**, fungal walls
**chitin** — a fact the paper tests every year.

### The plasma membrane

The membrane is a **phospholipid bilayer** about 7.5 nm thick. The phosphate heads face
outwards into water; the fatty-acid tails face inwards, away from it. Proteins float in
or through this bilayer, and cholesterol sits between the phospholipid tails. Because
the proteins move about in a fluid lipid sea, **Singer and Nicolson (1972)** called it
the **fluid-mosaic model**.

| Component | Role |
|---|---|
| **Phospholipid** | forms the bilayer; the barrier to water-soluble substances |
| **Integral (intrinsic) protein** | spans the bilayer; forms channels, pumps and carriers |
| **Peripheral (extrinsic) protein** | sits on one surface; enzymes, receptors, anchors |
| **Glycoprotein and glycolipid** | carbohydrate chains on the outer surface — cell recognition, ABO antigens, receptors |
| **Cholesterol** | keeps the membrane fluid at low temperature and stable at high temperature |

The membrane is **selectively permeable**: small non-polar molecules (O₂, CO₂) cross by
simple diffusion, water by osmosis through channels called aquaporins, and ions and
sugars through pumps and carriers, often against the gradient using ATP.

| Transport | Direction | Energy needed | Example |
|---|---|---|---|
| **Simple diffusion** | down the concentration gradient | none | O₂ and CO₂ across the bilayer |
| **Osmosis** | water moves down its water potential | none | water through aquaporins |
| **Facilitated diffusion** | down the gradient, through a carrier or channel | none | glucose into a red blood cell |
| **Active transport** | **against** the gradient, through a pump | **ATP** | Na⁺/K⁺ pump; mineral uptake by root hairs |
| **Endocytosis / exocytosis** | bulk movement in vesicles | ATP | phagocytosis by white cells; secretion of enzymes |

```figure caption="The fluid-mosaic model of the plasma membrane. The phospholipid bilayer has hydrophilic heads outside and hydrophobic tails inside; integral and peripheral proteins float in it, cholesterol stiffens it, and carbohydrate chains on the outer surface mark the cell."
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.0, 2.9))
for i in range(26):
    x = 0.03 + i * 0.037
    ax.add_patch(Circle((x, 0.62), 0.015, facecolor="#2C6E9B", edgecolor="none"))
    ax.add_patch(Circle((x, 0.38), 0.015, facecolor="#2C6E9B", edgecolor="none"))
    ax.plot([x - 0.006, x - 0.006], [0.605, 0.455], color="#C97B2E", lw=0.9)
    ax.plot([x + 0.006, x + 0.006], [0.605, 0.455], color="#C97B2E", lw=0.9)
    ax.plot([x - 0.006, x - 0.006], [0.395, 0.545], color="#C97B2E", lw=0.9)
    ax.plot([x + 0.006, x + 0.006], [0.395, 0.545], color="#C97B2E", lw=0.9)
ax.add_patch(FancyBboxPatch((0.27, 0.30), 0.10, 0.40, boxstyle="round,pad=0.004,rounding_size=0.03",
                            facecolor="#3F7D3A", edgecolor="none"))
ax.add_patch(FancyBboxPatch((0.50, 0.28), 0.10, 0.09, boxstyle="round,pad=0.004,rounding_size=0.03",
                            facecolor="#7A5C3E", edgecolor="none"))
for k in range(3):
    ax.plot([0.70, 0.735], [0.46 + 0.045 * k, 0.46 + 0.045 * k], color="#8E5AA8", lw=1.8)
for k in range(4):
    ax.add_patch(Circle((0.32 + 0.010 * np.cos(k * 1.6), 0.72 + 0.035 * k), 0.014,
                        facecolor="#B5482F", edgecolor="none"))
ax.text(0.04, 0.665, "hydrophilic head", fontsize=6.9, ha="left", color="#2C6E9B")
ax.text(0.04, 0.29, "hydrophobic tails", fontsize=6.9, ha="left", color="#C97B2E")
ax.text(0.32, 0.235, "integral protein", fontsize=6.9, ha="center", color="#3F7D3A")
ax.text(0.55, 0.205, "peripheral protein", fontsize=6.9, ha="center", color="#7A5C3E")
ax.text(0.20, 0.88, "glycoprotein", fontsize=6.9, ha="center", color="#B5482F")
ax.plot([0.26, 0.31], [0.855, 0.815], color=MUTED, lw=0.7)
ax.text(0.79, 0.68, "cholesterol", fontsize=6.9, ha="left", color="#8E5AA8")
ax.plot([0.785, 0.74], [0.665, 0.585], color=MUTED, lw=0.7)
ax.set_xlim(0, 1); ax.set_ylim(0.15, 0.95)
ax.axis("off")
```

### Mitochondria

A mitochondrion is 0.5–1 μm wide and 2–8 μm long, bounded by **two membranes**. The
outer membrane is smooth; the inner one is folded into finger-like **cristae** that
project into the jelly-like **matrix**. On the inner membrane sit the **F₁ particles
(oxysomes)**, which carry the enzymes of the electron transport chain and ATP synthase.
The matrix holds the enzymes of the Krebs cycle, **circular DNA**, **70S ribosomes** and
phosphate granules.

```photo id="bio11/mito-tem" caption="Two mitochondria in a mammalian lung cell (TEM). Each is bounded by a double membrane; the inner membrane is thrown into cristae. Scale bar 50 nm." width="70"
crop 0 0.1 1 1
```


Because a mitochondrion has its own DNA and ribosomes it is called **semi-autonomous**:
it makes some of its own proteins but depends on nuclear genes for the rest, and it
divides on its own. Mitochondrial DNA is inherited **from the mother** in humans. The
mitochondrion is the **powerhouse** — the site of aerobic respiration and oxidative
phosphorylation. Cells that do heavy work (heart muscle, flight muscle, the tapetum of
an anther) are packed with them.

### Chloroplasts

A chloroplast is a lens-shaped organelle 5–10 μm long, also bounded by **two
membranes**. Inside is the **stroma**, a protein-rich fluid holding the enzymes of the
Calvin cycle, starch grains, circular DNA and **70S ribosomes**. From the stroma, flat
membranous sacs called **thylakoids** arise; where they are stacked like coins they form
a **granum**, and the unstacked thylakoids that join one granum to the next are the
**intergranal (stroma) lamellae**. The chlorophyll and the photosystems sit **in the
thylakoid membrane**, not in the stroma — a favourite trap. Algal chloroplasts carry a
protein body, the **pyrenoid**, around which starch is laid down.

```photo id="bio11/chloroplast-tem" caption="Part of a chloroplast in a leaf cell of *Anemone* (TEM): stacks of thylakoids (grana) joined by stroma lamellae, inside the double envelope. Scale bar 500 nm." width="70"
```


| Part | Function |
|---|---|
| **Thylakoid membrane** | light reactions — photosystems I and II, chlorophyll, electron transport |
| **Grana** | stacks of thylakoids; increase the surface area for light capture |
| **Stroma** | Calvin cycle (dark reaction); DNA and 70S ribosomes |
| **Starch grain** | the storage product of photosynthesis |

### Endoplasmic reticulum

The ER is a network of membrane-bound tubules and flattened sacs (**cisternae**)
continuous with the outer nuclear membrane.

- **Rough ER** carries **ribosomes** on its surface and is the site of **protein synthesis** and transport — abundant in cells that secrete enzymes (pancreas, salivary gland).
- **Smooth ER** has no ribosomes. It makes **lipids and steroids**, detoxifies drugs and poisons (liver), stores **Ca²⁺** (sarcoplasmic reticulum of muscle) and carries out glycogen breakdown.

### Golgi body

The Golgi body (Golgi apparatus, dictyosome in plants) is a stack of flattened,
curved cisternae with swollen margins. It has two faces: the **cis (forming) face**
receives vesicles from the ER, and the **trans (maturing) face** releases vesicles
towards the membrane. Its jobs are to **modify, sort, package and secrete** — adding
sugar chains to proteins (glycosylation), forming **lysosomes**, producing **cell-wall
material**, and in plant cells laying down the **cell plate** at cytokinesis.

### Lysosomes

A lysosome is a **single-membrane** vesicle, formed from the Golgi, filled with about
40 **hydrolytic (acid hydrolase) enzymes** — protease, lipase, nuclease, phosphatase —
that work best at **pH ≈ 5**. They digest material taken in by the cell (heterophagy)
and worn-out organelles of the cell itself (autophagy). If the lysosome membrane
ruptures, its enzymes digest the cell's own contents; Christian de Duve, who discovered
them, therefore called lysosomes the **"suicidal bags"** of the cell. They are common in
animal cells and in fungi; in mature plant cells the large central **vacuole** does much
of the same work.

### Ribosomes

A ribosome is a tiny granule of **rRNA and protein**, with no membrane, first seen by
George Palade. It is the **site of protein synthesis**. The prokaryotic ribosome is
**70S**, made of a 50S and a 30S subunit; the eukaryotic cytoplasmic ribosome is
**80S**, made of 60S and 40S subunits. Mitochondria and chloroplasts contain **70S**
ribosomes — evidence for their bacterial origin. Several ribosomes translating one mRNA
form a **polysome**.

### Nucleus

The nucleus is bounded by a **double membrane, the nuclear envelope**, perforated by
**nuclear pores** that let RNA and proteins pass between nucleus and cytoplasm. Inside
are the **nucleoplasm**, the **chromatin** (DNA with histones) and one or more
**nucleoli**. The **nucleolus** is not an organelle with a membrane; it is the site
where **rRNA is made and ribosomal subunits are assembled**. The nucleus holds the
genetic material and controls the cell's activities.

### Chromosomes

During division the chromatin condenses into **chromosomes**. A chromosome that has
replicated has two identical **chromatids** joined at the **centromere**, a narrow
region (the primary constriction) that carries the **kinetochore** to which spindle
fibres attach. The ends of each chromatid are **telomeres**, which protect the DNA from
being degraded or fused. Some chromosomes have a **satellite** beyond a secondary
constriction.

The DNA itself is wrapped twice round an **octamer of histones** — two molecules each
of H2A, H2B, H3 and H4 — with about **147 base pairs** per turn, forming a
**nucleosome**; the string of nucleosomes is coiled further to make the visible
chromosome.

| By centromere position | Shape |
|---|---|
| **Metacentric** | centromere in the middle; two equal arms |
| **Submetacentric** | centromere slightly off-centre |
| **Acrocentric** | centromere near one end |
| **Telocentric** | centromere at the very end |

### Cilia and flagella

Eukaryotic cilia and flagella have the same internal structure: a core, the **axoneme**,
of nine pairs of microtubules arranged in a ring around a central pair — the **9+2
arrangement**. The pairs are linked by **dynein** arms, which slide the microtubules past
one another using **ATP**, so the structure bends. At the base is a **basal body** with a
**9+0** arrangement, identical to a centriole. Cilia are short and numerous; flagella are
long and few (the sperm tail, *Chlamydomonas*).

A **bacterial flagellum** is completely different: a single fibril of the protein
**flagellin**, with no 9+2 and no membrane, that **rotates** like a propeller driven by
a proton gradient. Do not mix the two.

### Cell inclusions

**Cell inclusions** are non-living materials in the cytoplasm — they are not organelles
and have no membrane of their own:

| Inclusion | Where |
|---|---|
| Starch grains | plant cells (storage) |
| Oil droplets and fat globules | seeds, adipose cells |
| Glycogen granules | liver and muscle |
| **Calcium oxalate crystals** (raphides) | *Colocasia*, *Opuntia*, many plant cells |
| Pigment granules | melanin in skin, anthocyanin in vacuoles |
| Vacuoles with cell sap, resins, gums, latex | plant cells |
| Secretory granules | gland cells |

### Plant cells and animal cells compared

| Feature | Plant cell | Animal cell |
|---|---|---|
| **Cell wall** | present, of cellulose | **absent** |
| Shape | fixed, often angular | variable, rounded |
| **Chloroplast** | present in green parts | **absent** |
| **Vacuole** | one large central vacuole with sap | small and many, or none |
| **Centriole** | absent in higher plants | present |
| **Cytokinesis** | **cell plate** | **cleavage furrow** |
| Stored food | starch | glycogen |
| Lysosomes | few; the vacuole does much of the work | many |
| Cell junctions | **plasmodesmata** through the wall | gap junctions, desmosomes |

::: caution Organelle traps
- **Chlorophyll is in the thylakoid membrane**, not in the stroma; the stroma holds the Calvin-cycle enzymes.
- **The nucleolus makes rRNA, not DNA** — DNA is made in the nucleoplasm during S phase.
- **Lysosomes are single-membraned; mitochondria and chloroplasts are double-membraned.**
- **70S ribosomes** occur in prokaryotes, mitochondria and chloroplasts; **80S** only in the eukaryotic cytoplasm.
- A plant cell has **no centriole** in higher plants, yet still forms a spindle — spindle fibres in plants are made without centrioles.
:::

## 7.3 The cell cycle; amitosis, mitosis and meiosis

### The cell cycle

The **cell cycle** is the sequence of events by which a cell duplicates its contents
and divides into two. It has two main phases:

| Phase | What happens | Share of a typical 24 h animal cell |
|---|---|---|
| **Interphase** | the cell grows and copies its DNA; no visible chromosomes | about 23 h |
| — **G₁** | cell grows, makes proteins and organelles; the **G₁/S checkpoint** decides whether to divide | about 11 h |
| — **S** | **DNA replication**; each chromosome becomes two chromatids; histones are made | about 8 h |
| — **G₂** | further growth, spindle proteins made; the **G₂/M checkpoint** checks the copied DNA | about 4 h |
| **M phase** | mitosis (karyokinesis) followed by cytokinesis | about 1 h |

A cell that leaves the cycle and stops dividing — a mature neuron, a muscle fibre —
enters **G₀**, a resting state from which it may never return. The checkpoints are
controlled by **cyclins and cyclin-dependent kinases (CDKs)**; if DNA is damaged at the
G₁/S checkpoint the cell arrests and repairs it, or kills itself (apoptosis). Loss of
checkpoint control is a step towards cancer.

```figure caption="The cell cycle, read clockwise. Interphase (G₁, S, G₂) takes up most of the cycle; DNA is copied only in S. The G₁/S and G₂/M checkpoints decide whether the cell may go on, and a cell that leaves the cycle enters G₀."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.5, 3.3))
ax.set_aspect("equal"); ax.axis("off")
ax.set_xlim(-1.40, 1.40); ax.set_ylim(-1.40, 1.30)
segs = [("G₁", 15, 165, "#3F7D3A"), ("S", -95, 15, "#C97B2E"),
        ("G₂", -165, -95, "#7A5C3E"), ("M", 165, 195, "#B5482F")]
for lab, a0, a1, col in segs:
    ax.add_patch(plt.matplotlib.patches.Wedge((0, 0), 1.0, a0, a1, width=0.34,
                                              facecolor=col, edgecolor="white", lw=1.4, alpha=0.92))
    mid = np.deg2rad((a0 + a1) / 2)
    ax.text(0.83 * np.cos(mid), 0.83 * np.sin(mid), lab, ha="center", va="center",
            fontsize=8.6, color="white", fontweight="bold")
ax.text(0, 0.09, "cell", ha="center", va="center", fontsize=7.6, color=INK)
ax.text(0, -0.09, "cycle", ha="center", va="center", fontsize=7.6, color=INK)
for ang, lab in [(15, "G₁/S"), (195, "G₂/M")]:
    r = np.deg2rad(ang)
    ax.plot([1.05 * np.cos(r)], [1.05 * np.sin(r)], marker="o", ms=3.4, color=INK)
    ax.text(1.20 * np.cos(r), 1.20 * np.sin(r), lab, fontsize=6.9, ha="center", va="center", color=INK)
r = np.deg2rad(-38)
ax.annotate("", xy=(1.02 * np.cos(r - 0.10), 1.02 * np.sin(r - 0.10)),
            xytext=(1.02 * np.cos(r + 0.10), 1.02 * np.sin(r + 0.10)),
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2, mutation_scale=11))
ax.annotate("", xy=(-1.08, 1.02), xytext=(-0.80, 0.76),
            arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.1, mutation_scale=8))
ax.text(-1.18, 1.10, "G₀", fontsize=8.0, ha="center", color=MUTED)
ax.text(0, -1.32, "a cell that stops dividing leaves the cycle into G₀", fontsize=6.8,
        ha="center", color=MUTED)
```

### Amitosis

**Amitosis** (direct division) is division of the nucleus **without** spindle formation
and without condensation of chromosomes: the nucleus simply constricts and divides into
two. It occurs in bacteria (binary fission), in some yeasts and protozoa, and in
damaged or ageing cells. It produces no variation and is not a substitute for mitosis
in the cells of higher organisms.

### Mitosis

Mitosis is the division of a nucleus into **two genetically identical daughter nuclei**
with the same chromosome number. It is one continuous process, described in four stages:

| Stage | What happens |
|---|---|
| **Prophase** | chromatin condenses into visible chromosomes (each with two chromatids); the **nucleolus disappears**; spindle fibres begin to form from the poles; the nuclear envelope breaks down at the end of prophase |
| **Metaphase** | chromosomes line up at the **equator (metaphase plate)**; spindle fibres from opposite poles attach to the **kinetochore** of each centromere |
| **Anaphase** | the **centromeres split**; the two chromatids of each chromosome are pulled to opposite poles, centromere first — so each pole receives one complete set |
| **Telophase** | chromosomes reach the poles and decondense; the **nuclear envelope re-forms**; the **nucleolus reappears**; the spindle disappears |

**Cytokinesis** follows. In an **animal cell** the membrane invaginates as a **cleavage
furrow** (a contractile ring of actin and myosin) and pinches the cell in two. In a
**plant cell** the rigid wall prevents pinching, so vesicles from the **Golgi** line up
at the equator and fuse to form a **cell plate**, which becomes the **middle lamella**
and then the new walls.

```figure caption="Mitosis in a strip: interphase, prophase, metaphase, anaphase, telophase and cytokinesis. The chromosome number stays the same throughout; only the sister chromatids are separated."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse
fig, axs = plt.subplots(1, 6, figsize=(5.2, 2.5), gridspec_kw=dict(wspace=0.04))
titles = ["Interphase", "Prophase", "Metaphase", "Anaphase", "Telophase", "Cytokinesis"]
for k, ax in enumerate(axs):
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off"); ax.set_aspect("equal")
    ax.add_patch(Ellipse((0.5, 0.60), 0.88, 0.62, facecolor="#F4F1E4", edgecolor="#8A8F98", lw=1.0))
    ax.text(0.5, 0.16, titles[k], fontsize=6.9, ha="center", va="center", color=INK)
    if k == 0:
        ax.add_patch(Circle((0.5, 0.60), 0.19, facecolor="#DCE6EE", edgecolor="#2C6E9B", lw=0.9))
        t = np.linspace(0, 6.2, 90)
        ax.plot(0.5 + 0.13 * np.sin(t), 0.60 + 0.13 * np.cos(t), color="#2C6E9B", lw=0.9)
    elif k == 1:
        ax.add_patch(Circle((0.5, 0.60), 0.19, facecolor="none", edgecolor="#2C6E9B", lw=0.8, ls=":"))
        for dx in (-0.10, -0.03, 0.04, 0.11):
            ax.plot([0.5 + dx, 0.5 + dx + 0.015], [0.47, 0.73], color="#B5482F", lw=2.4)
    elif k == 2:
        ax.plot([0.24, 0.76], [0.60, 0.60], color="#8A8F98", lw=0.7, ls=":")
        for dx in (-0.15, -0.05, 0.05, 0.15):
            ax.plot([0.5 + dx, 0.5 + dx], [0.52, 0.68], color="#B5482F", lw=3.0)
    elif k == 3:
        for dx in (-0.15, -0.05, 0.05, 0.15):
            ax.plot([0.5 + dx], [0.44], marker="o", ms=4.4, color="#B5482F")
            ax.plot([0.5 + dx], [0.76], marker="o", ms=4.4, color="#B5482F")
    elif k == 4:
        ax.add_patch(Circle((0.34, 0.60), 0.15, facecolor="#DCE6EE", edgecolor="#2C6E9B", lw=0.9))
        ax.add_patch(Circle((0.66, 0.60), 0.15, facecolor="#DCE6EE", edgecolor="#2C6E9B", lw=0.9))
    else:
        ax.add_patch(Circle((0.30, 0.60), 0.14, facecolor="#DCE6EE", edgecolor="#2C6E9B", lw=0.9))
        ax.add_patch(Circle((0.70, 0.60), 0.14, facecolor="#DCE6EE", edgecolor="#2C6E9B", lw=0.9))
        ax.plot([0.50, 0.50], [0.29, 0.91], color="#3F7D3A", lw=1.8)
```

**Significance of mitosis:** it keeps the chromosome number constant (2n → 2n); it
produces genetically identical cells, so it is the basis of **growth**, **repair and
replacement** of tissues (skin, gut lining, blood cells), **asexual reproduction**
(binary fission, budding, cuttings) and the **vegetative propagation** of plants.

### Meiosis

**Meiosis** is a reduction division: one diploid cell gives **four haploid cells** after
**two divisions** with only **one** round of DNA replication.

| Stage | What happens |
|---|---|
| **Prophase I** (longest) | **Leptotene** — chromosomes become visible as threads. **Zygotene** — homologous chromosomes pair up (**synapsis**) and form a **bivalent** held by the synaptonemal complex. **Pachytene** — **crossing over** between non-sister chromatids; segments are exchanged. **Diplotene** — the homologues begin to separate and the points of exchange are seen as **chiasmata**. **Diakinesis** — chromosomes condense fully, the envelope breaks down, the spindle forms. |
| **Metaphase I** | bivalents line up at the equator; the two homologues of each pair face opposite poles |
| **Anaphase I** | the **homologues separate** and move to opposite poles; **centromeres do not divide** |
| **Telophase I** | two haploid cells form (each chromosome still has two chromatids) |
| **Meiosis II** | like mitosis: **sister chromatids separate**; centromeres divide; four haploid cells result |

```figure caption="Meiosis. Crossing over in prophase I exchanges segments between non-sister chromatids of a bivalent, and the two divisions take one diploid cell to four haploid cells."
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.1, 2.9), gridspec_kw=dict(wspace=0.10))
for ax in (ax1, ax2):
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off"); ax.set_aspect("equal")
ax1.add_patch(Ellipse((0.5, 0.52), 0.90, 0.76, facecolor="#F4F1E4", edgecolor="#8A8F98", lw=1.0))
ax1.plot([0.16, 0.46], [0.64, 0.64], color="#B5482F", lw=3.0)
ax1.plot([0.46, 0.84], [0.64, 0.64], color="#2C6E9B", lw=3.0)
ax1.plot([0.16, 0.46], [0.40, 0.40], color="#2C6E9B", lw=3.0)
ax1.plot([0.46, 0.84], [0.40, 0.40], color="#B5482F", lw=3.0)
ax1.plot([0.44, 0.56], [0.64, 0.40], color=INK, lw=1.1)
ax1.plot([0.56, 0.44], [0.64, 0.40], color=INK, lw=1.1)
ax1.text(0.50, 0.80, "crossing over", fontsize=7.2, ha="center", color=INK)
ax1.text(0.50, 0.26, "chiasma", fontsize=7.0, ha="center", color=INK)
ax1.plot([0.50, 0.50], [0.30, 0.37], color=MUTED, lw=0.7)
ax1.text(0.50, 0.06, "(a) prophase I", fontsize=7.4, ha="center", color=INK)
ax2.add_patch(Ellipse((0.5, 0.88), 0.30, 0.12, facecolor="#DCE6EE", edgecolor="#2C6E9B", lw=1.0))
ax2.text(0.5, 0.88, "2n", fontsize=7.6, ha="center", va="center", color="#2C6E9B")
for x in (0.28, 0.72):
    ax2.annotate("", xy=(x, 0.685), xytext=(0.5 + (x - 0.5) * 0.40, 0.815),
                 arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.0, mutation_scale=7))
    ax2.add_patch(Ellipse((x, 0.62), 0.26, 0.13, facecolor="#E8F0E4", edgecolor="#3F7D3A", lw=1.0))
    ax2.text(x, 0.62, "n", fontsize=7.4, ha="center", va="center", color="#3F7D3A")
ax2.text(0.50, 0.755, "meiosis I", fontsize=6.6, ha="center", va="center", color=MUTED,
         bbox=dict(fc="white", ec="none", pad=1.0))
for x, x0 in [(0.16, 0.28), (0.40, 0.28), (0.60, 0.72), (0.84, 0.72)]:
    ax2.annotate("", xy=(x, 0.395), xytext=(x0 + (x - x0) * 0.35, 0.545),
                 arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.0, mutation_scale=7))
    ax2.add_patch(Circle((x, 0.32), 0.085, facecolor="#C97B2E", edgecolor="none", alpha=0.9))
    ax2.text(x, 0.32, "n", fontsize=7.0, ha="center", va="center", color="white")
ax2.text(0.50, 0.465, "meiosis II", fontsize=6.6, ha="center", va="center", color=MUTED,
         bbox=dict(fc="white", ec="none", pad=1.0))
ax2.text(0.50, 0.13, "(b) four haploid cells", fontsize=7.2, ha="center", color=INK)
```

**Significance of meiosis:** it **halves the chromosome number**, so that fertilisation
restores the diploid number and the species number stays constant across generations; it
produces **variation** through crossing over and independent assortment, which is the raw
material of evolution; and it shuffles alleles so that no two gametes are alike.

**The two sources of variation.** **Crossing over** (pachytene of prophase I) exchanges
segments between **non-sister chromatids of homologous chromosomes**, producing
recombinant chromatids. **Independent assortment** (metaphase I) is the random
orientation of each bivalent: with $n$ pairs, a gamete can receive $2^n$ different
combinations of maternal and paternal chromosomes — $2^{23}$, over eight million, in a
human.

::: example Problem. A cell has 2n = 8. Give the number of chromosomes, chromatids and DNA molecules at metaphase of mitosis, at metaphase I and at metaphase II.
**Solution.** After S phase the DNA is doubled but the chromosome number is not.
**Mitosis metaphase:** 8 chromosomes, 16 chromatids, 16 DNA molecules.
**Metaphase I:** 8 chromosomes (4 bivalents), 16 chromatids, 16 DNA molecules.
**Metaphase II:** 4 chromosomes, 8 chromatids, 8 DNA molecules — meiosis I has already
halved the chromosome number.
:::

::: example Problem. A human cell has 2n = 46 and a G₁ DNA content of 2C. Give the chromosome number and DNA content at G₁, after S phase, at anaphase of mitosis, after meiosis I and in a sperm.
**Solution.** G₁: **46 chromosomes, 2C**. After S: **46 chromosomes, 4C** — the DNA has
doubled but the centromeres have not. Anaphase of mitosis: **92 chromosomes, 4C**,
because every centromere has split. After meiosis I: **23 chromosomes, 2C** — the
number is halved but each chromosome still has two chromatids. Sperm: **23 chromosomes,
1C**. The rule is: count centromeres for chromosomes, count DNA molecules for C.
:::

### Mitosis and meiosis compared

| Feature | Mitosis | Meiosis |
|---|---|---|
| Divisions | **one** | **two**, one after the other |
| DNA replication | once | once |
| Products | **2** cells | **4** cells |
| Chromosome number of products | **same** as parent (2n → 2n) | **half** (2n → n) |
| Pairing of homologues (synapsis) | does not occur | occurs in prophase I |
| **Crossing over** | **absent** | **present** (pachytene) |
| Chiasmata | absent | present |
| Metaphase | single chromosomes at the equator | **bivalents** at the equator in meiosis I |
| Anaphase | **centromeres divide**, chromatids separate | meiosis I: **homologues separate, centromeres do not divide**; meiosis II: chromatids separate |
| Genetic result | daughter cells identical to parent | daughter cells genetically different |
| Where | all somatic cells, meristems | reproductive organs: anther, ovule, testis, ovary |
| Role | growth, repair, asexual reproduction | gamete formation, variation, evolution |

::: caution The traps in cell division
1. **Meiosis II is equational, not reductional.** It separates sister chromatids exactly as mitosis does; the reduction happens in meiosis I.
2. **DNA content and chromosome number are not the same thing.** After S phase a human cell still has 46 chromosomes but 92 DNA molecules. At anaphase of mitosis the centromeres split, so the cell briefly has **92 chromosomes**.
3. **Plant cells make a cell plate, animal cells a cleavage furrow.** A question about "cytokinesis by a furrow" is about an animal cell.
4. **In anaphase I the centromeres do not divide** — the whole chromosome, with both chromatids, travels to the pole.
5. **Crossing over happens in pachytene**, but the **chiasmata** that show where it happened are seen in **diplotene**.
:::

::: example Counting mitotic and meiotic divisions to produce seeds
**Problem.** How many mitotic divisions are required to produce 64 cells from a single meristematic cell, and how many total meiotic divisions are required to form 100 wheat grains ($2n = 42$)?

**Solution.** Each mitotic division adds one cell to the count ($N - 1$ total mitoses, in $\log_2 64 = 6$ generations): **63 mitotic divisions**. For $n$ seeds in an angiosperm, 1 microspore mother cell makes 4 pollen grains ($n/4$ meioses) and 1 megaspore mother cell makes 1 functional egg ($n$ meioses), so $n + n/4 = \frac{5}{4}n = \frac{5}{4}(100) = \mathbf{125\text{ meiotic divisions}}$.
:::

```photogrid label="7.1" cols="2" ratio="1.2" caption="Counting cells to find how long each phase lasts. (a) A root-tip squash of onion: cells caught in mitosis show condensed chromosomes. (b) In a sample of 200 cells, 160 were in interphase and 40 in mitosis (prophase 24, metaphase 6, anaphase 4, telophase 6), so the mitotic index is 20 per cent. If the whole cycle takes 20 hours, the time spent in a phase is its fraction of cells times 20 h: interphase 16.0 h, prophase 2.4 h, metaphase 0.6 h, anaphase 0.4 h and telophase 0.6 h. Prophase is the longest stage of mitosis, which is why most dividing cells you find are in it."
@ photo id="bio11/onion-root" cap="Onion root tip cells in mitosis"
fit 1.2
focus 0.5 0.5
@ svg cap="Phase counts in 200 cells and the time each takes (20 h cycle)"
cnt = (("Interphase", 160), ("Prophase", 24), ("Metaphase", 6), ("Anaphase", 4), ("Telophase", 6))
tot = sum(n for _, n in cnt)
assert tot == 200
mi = 100 * (tot - 160) / tot
hrs = {k: n / tot * 20 for k, n in cnt}
assert abs(mi - 20) < 1e-9 and abs(hrs["Prophase"] - 2.4) < 1e-9 and abs(hrs["Interphase"] - 16) < 1e-9
facts = dict(mi="%.0f" % mi, ti="%.1f" % hrs["Interphase"], tp="%.1f" % hrs["Prophase"], tm="%.1f" % hrs["Metaphase"], ta="%.1f" % hrs["Anaphase"], tt="%.1f" % hrs["Telophase"])
f = Fig(300, 236)
f.text(150, 12, "Cells counted and hours per phase", size=10.5, color=NAVY, bold=True)
for i, (k, n) in enumerate(cnt):
    y = 30 + i * 30
    f.text(8, y + 10, k, size=10.5, color=SLATE, anchor="start", vmid=True)
    w = n / 160 * 78
    f.box(86, y, max(w, 3), 20, fill=MINT if i else BLUE, stroke=TEAL if i else NAVY, r=2)
    f.text(86 + max(w, 3) + 6, y + 10, "%d cells = %.1f h" % (n, hrs[k]), size=10.5, color=TEAL if i else NAVY, bold=True, anchor="start", vmid=True)
f.text(150, 196, "mitotic index = 40/200 = 20 per cent", size=10.5, color=NAVY, bold=True)
f.text(150, 214, "time = fraction of cells x 20 h", size=10.5, color=SLATE, bold=True)
```

## Formula and fact sheet

| Item | Fact |
|---|---|
| Cell discovered | Robert Hooke, 1665, in cork |
| First living cells | Leeuwenhoek, 1674 |
| Nucleus | Robert Brown, 1831 |
| Cell theory | Schleiden (1838, plants) + Schwann (1839, animals) |
| *Omnis cellula e cellula* | Virchow, 1855 |
| Exceptions | viruses, viroids, prions (acellular); coenocytic hyphae (*Mucor*); multinucleate muscle fibres |
| Prokaryote ribosome | **70S** = 50S + 30S |
| Eukaryote ribosome | **80S** = 60S + 40S; 70S in mitochondria and chloroplasts |
| Prokaryote wall / plant wall / fungal wall | peptidoglycan / cellulose / chitin |
| Cell wall layers | middle lamella (calcium pectate) → primary (cellulose) → secondary (cellulose + lignin) |
| Membrane model | fluid mosaic, Singer and Nicolson, 1972; bilayer about 7.5 nm |
| Mitochondrion | double membrane, cristae, matrix, own circular DNA, 70S ribosomes, F₁ particles; maternal inheritance |
| Chloroplast | double membrane, stroma, thylakoids, grana, intergranal lamellae, own DNA, 70S ribosomes; chlorophyll **in the thylakoid membrane** |
| Rough ER | ribosomes, protein synthesis and transport |
| Smooth ER | lipid and steroid synthesis, detoxification, Ca²⁺ store |
| Golgi | cis (forming) and trans (maturing) faces; secretion, glycosylation, lysosome and cell-plate formation |
| Lysosome | single membrane, acid hydrolases, pH ≈ 5; "suicidal bag" (de Duve) |
| Nucleolus | rRNA synthesis and ribosome assembly |
| Nucleosome | 147 bp DNA round a histone octamer (2 each of H2A, H2B, H3, H4) |
| Chromosome parts | chromatid, centromere (kinetochore), telomere, satellite |
| Chromosome types | metacentric, submetacentric, acrocentric, telocentric |
| 9+2 | eukaryotic cilia and flagella; basal body 9+0; dynein + ATP |
| Bacterial flagellum | flagellin, no 9+2, rotates |
| Bacterial surface | capsule, peptidoglycan wall, plasma membrane, mesosome, pili, flagellum |
| **Organelle membranes** | **double**: nucleus, mitochondrion, chloroplast; **single**: ER, Golgi, lysosome, vacuole, peroxisome; **none**: ribosome, centriole |
| Cell inclusions | starch, oil, glycogen, calcium oxalate crystals, pigments, vacuolar sap |
| Cell cycle | G₁ → S → G₂ → M; DNA replicates in **S**; G₀ = resting |
| Cell-cycle duration | human cell about 24 h: G₁ 11, S 8, G₂ 4, M 1 |
| Checkpoints | G₁/S (restriction point), G₂/M, spindle assembly; cyclins and CDKs |
| Mitosis stages | prophase, metaphase, anaphase, telophase |
| Cytokinesis | animal: cleavage furrow; plant: cell plate from Golgi vesicles |
| Meiosis prophase I | leptotene, zygotene (synapsis), pachytene (crossing over), diplotene (chiasmata), diakinesis |
| Meiosis products | 4 haploid cells from one diploid cell |
| Variation | crossing over (prophase I) + independent assortment (metaphase I), $2^n$ combinations |
| Amitosis | direct division, no spindle, no chromosome condensation; bacteria |
| Human numbers | somatic 46 (2n), gamete 23 (n) |

## Chapter summary

- The cell theory (Schleiden 1838, Schwann 1839, Virchow 1855) has exceptions: viruses are acellular and coenocytic hyphae are multinucleate without cross walls.
- Prokaryotes have no nucleus or membrane-bound organelles, 70S ribosomes, a peptidoglycan wall and binary fission; eukaryotes have a nucleus, 80S cytoplasmic ribosomes and mitosis.
- The plant wall is middle lamella (calcium pectate), primary wall (cellulose) and secondary wall (cellulose plus lignin); plasmodesmata connect neighbouring cells.
- The plasma membrane is a fluid mosaic of phospholipid bilayer and proteins (Singer and Nicolson, 1972), selectively permeable.
- Mitochondria (cristae) and chloroplasts (grana, thylakoids, stroma) are double-membraned and semi-autonomous, with their own DNA and 70S ribosomes; chlorophyll sits in the thylakoid membrane.
- Lysosomes are single-membraned bags of acid hydrolases — the "suicidal bags"; the Golgi packages and secretes and forms the cell plate.
- Chromatin is DNA wound round histone octamers into nucleosomes; a replicated chromosome has two chromatids joined at the centromere, with telomeres at the ends.
- Eukaryotic cilia and flagella are 9+2 microtubules moved by dynein and ATP; bacterial flagella are flagellin and rotate.
- The cell cycle is G₁, S, G₂, M with checkpoints; DNA replicates only in S, so chromosome number and DNA content must be counted separately.
- Mitosis gives two identical diploid cells (growth, repair); meiosis gives four haploid cells in two divisions, with crossing over in pachytene and independent assortment at metaphase I providing the variation.

## Practice questions

**Set A — Recall (30 questions)**

1. The cell theory was proposed by
   (a) Hooke and Leeuwenhoek (b) Schleiden and Schwann (c) Virchow and Pasteur (d) Brown and Purkinje
2. "Omnis cellula e cellula" — every cell arises from a pre-existing cell — was stated by
   (a) Schwann (b) Schleiden (c) Hooke (d) Virchow
3. The cell was first discovered by
   (a) Robert Hooke in cork (b) Leeuwenhoek in pond water (c) Robert Brown in orchid (d) Schwann in cartilage
4. Which of the following is absent from a prokaryotic cell?
   (a) ribosomes (b) plasma membrane (c) membrane-bound nucleus (d) cell wall
5. The ribosomes of a prokaryotic cell are of the type
   (a) 80S (b) 60S (c) 40S (d) 70S
6. The genetic material of a bacterium lies in the
   (a) nucleoid (b) nucleus (c) mitochondrion (d) chloroplast
7. The middle lamella of a plant cell wall is made mainly of
   (a) cellulose (b) lignin (c) calcium pectate (d) chitin
8. The fluid-mosaic model of the plasma membrane was proposed by
   (a) Danielli and Davson (b) Singer and Nicolson (c) Robertson (d) Palade
9. The inner membrane of a mitochondrion is folded into
   (a) cristae (b) grana (c) thylakoids (d) cisternae
10. A stack of thylakoids in a chloroplast is called a
   (a) crista (b) stroma (c) cisterna (d) granum
11. Rough endoplasmic reticulum differs from smooth ER in bearing
   (a) DNA (b) ribosomes (c) chlorophyll (d) hydrolytic enzymes
12. The organelle that modifies, packages and secretes cell products is the
   (a) lysosome (b) ribosome (c) Golgi body (d) peroxisome
13. Lysosomes are called "suicidal bags" because they
   (a) contain DNA (b) make ATP (c) digest food (d) hold enzymes that can digest the cell's own contents
14. The 80S ribosome of a eukaryote is made of the subunits
   (a) 60S and 40S (b) 50S and 30S (c) 40S and 30S (d) 60S and 50S
15. The nucleolus is the site of
   (a) DNA replication (b) rRNA synthesis and ribosome assembly (c) ATP synthesis (d) protein digestion
16. In a nucleosome, DNA is wound around
   (a) a single histone (b) non-histone protein only (c) an octamer of histones (d) RNA
17. The region at which the two chromatids of a chromosome are joined is the
   (a) centromere (b) telomere (c) chiasma (d) satellite
18. The 9+2 arrangement of microtubules is found in
   (a) bacterial flagella (b) prokaryotic cilia (c) centrioles (d) eukaryotic cilia and flagella
19. Which of these is a non-living cell inclusion?
   (a) mitochondrion (b) ribosome (c) calcium oxalate crystal (d) Golgi body
20. The longest phase of the cell cycle is
   (a) M phase (b) interphase (c) anaphase (d) telophase
21. DNA replicates during
   (a) G₁ phase (b) G₂ phase (c) M phase (d) S phase
22. The stage of mitosis in which chromosomes line up at the equator is
   (a) metaphase (b) anaphase (c) prophase (d) telophase
23. In plant cells, cytokinesis takes place by formation of a
   (a) cleavage furrow (b) contractile ring (c) cell plate (d) chitin septum
24. Synapsis and crossing over occur in
   (a) mitosis (b) prophase I of meiosis (c) prophase II of meiosis (d) anaphase I
25. The chromosome number is halved during
   (a) meiosis I (b) meiosis II (c) mitosis (d) S phase
26. Meiosis II is called equational because it
   (a) halves the chromosome number (b) doubles the DNA (c) pairs the homologues (d) separates sister chromatids without changing the number
27. Direct division of the nucleus without spindle formation is
   (a) mitosis (b) amitosis (c) meiosis (d) endomitosis
28. Chiasmata are first clearly visible in
   (a) leptotene (b) zygotene (c) diplotene (d) diakinesis
29. Colchicine arrests a dividing cell at
   (a) prophase (b) anaphase (c) telophase (d) metaphase
30. A human somatic cell has 46 chromosomes. The number in a gamete is
   (a) 23 (b) 46 (c) 92 (d) 12

::: note Answers and explanations — Set A
**1.** (b) — Schleiden (plants, 1838) and Schwann (animals, 1839) gave the cell theory; Virchow added the third tenet later.
**2.** (d) — Virchow (1855) stated that new cells come only from existing cells. Schwann and Schleiden believed cells formed from a shapeless matrix.
**3.** (a) — Hooke saw the empty cell walls of cork in 1665 and named them cells; Leeuwenhoek first saw living cells nine years later.
**4.** (c) — Prokaryotes have no nuclear envelope; the DNA lies free in the nucleoid. They do have ribosomes, a membrane and usually a wall.
**5.** (d) — 70S (50S + 30S). 80S is the eukaryotic cytoplasmic ribosome.
**6.** (a) — The single circular chromosome lies in the nucleoid region, not in a nucleus. Plasmids are separate small circles.
**7.** (c) — Calcium pectate cements adjacent cells; pectinase digests it when fruit ripens and softens.
**8.** (b) — Singer and Nicolson (1972). Danielli and Davson had proposed the earlier sandwich model.
**9.** (a) — Cristae increase the area of the inner membrane, where the electron transport chain and ATP synthase sit.
**10.** (d) — A granum is a stack of thylakoids; the stroma is the fluid around them.
**11.** (b) — Rough ER carries ribosomes and makes protein; smooth ER makes lipid and steroid.
**12.** (c) — The Golgi modifies, sorts and packages; the lysosome only digests.
**13.** (d) — The hydrolytic enzymes, if released, digest the cell itself. The membrane normally keeps them safely inside.
**14.** (a) — 80S = 60S + 40S. The 50S + 30S pair makes the 70S ribosome of prokaryotes.
**15.** (b) — The nucleolus makes rRNA and assembles ribosomal subunits; DNA replication happens in the nucleoplasm.
**16.** (c) — About 147 bp of DNA wind round two each of H2A, H2B, H3 and H4.
**17.** (a) — The centromere carries the kinetochore for the spindle; the telomeres are the ends.
**18.** (d) — Nine doublets around a central pair, with dynein arms. Bacterial flagella are flagellin and have no 9+2.
**19.** (c) — Crystals are ergastic, non-living inclusions. Mitochondria, ribosomes and the Golgi are organelles.
**20.** (b) — Interphase takes about 23 h of a 24 h cycle; M phase about 1 h.
**21.** (d) — S phase is the synthesis phase; each chromosome becomes two chromatids.
**22.** (a) — At metaphase the chromosomes lie on the metaphase plate with spindle fibres attached to their kinetochores.
**23.** (c) — Golgi vesicles fuse at the equator to make a cell plate, which becomes the middle lamella.
**24.** (b) — Synapsis and crossing over are confined to prophase I; meiosis II has no pairing.
**25.** (a) — Homologues separate in anaphase I, so each daughter nucleus gets n chromosomes.
**26.** (d) — Meiosis II separates chromatids, like mitosis, and leaves the chromosome number unchanged.
**27.** (b) — Amitosis is direct division, seen in bacteria and some protozoa; no spindle or condensed chromosomes are involved.
**28.** (c) — Crossing over happens in pachytene but the chiasmata become visible as the homologues pull apart in diplotene.
**29.** (d) — Colchicine blocks spindle formation, so chromosomes cannot move to the poles and the cell arrests in metaphase — the basis of karyotyping.
**30.** (a) — Meiosis halves 46 to 23; fertilisation restores 46.
:::

**Set B — Understanding (18 questions)**

1. Viruses are an exception to the cell theory because they
   (a) have a nucleus (b) are prokaryotes (c) are acellular and have no cell (d) lack nucleic acid
2. A coenocytic hypha of *Mucor* is an exception because it
   (a) is one mass of cytoplasm with many nuclei and no cross walls (b) has no nucleus (c) is a virus (d) has a cellulose wall
3. A plant cell placed in pure water does not burst because
   (a) it has no membrane (b) it has a contractile vacuole (c) it lacks a cell wall (d) the rigid wall resists the turgor pressure
4. Mitochondria and chloroplasts are called semi-autonomous because they
   (a) lack DNA (b) have their own DNA and 70S ribosomes but depend on nuclear genes (c) divide only with the nucleus (d) have 80S ribosomes
5. The lysosome membrane is important because it
   (a) keeps the hydrolytic enzymes away from the cytoplasm (b) makes ATP (c) synthesises protein (d) contains DNA
6. A cell that secretes large amounts of digestive enzyme would have many
   (a) chloroplasts (b) lysosomes (c) rough ER and Golgi bodies (d) cilia
7. The nuclear pore allows
   (a) free passage of ribosomes (b) exchange of RNA and proteins between nucleus and cytoplasm (c) ATP synthesis (d) DNA replication
8. During anaphase of mitosis, a human cell contains
   (a) 23 chromosomes (b) 46 chromosomes (c) 46 pairs of chromosomes (d) 92 chromosomes
9. Meiosis is important for evolution mainly because it
   (a) produces new gene combinations by crossing over and independent assortment (b) doubles the chromosome number (c) makes identical cells (d) repairs tissues
10. Mitosis in a haploid cell produces
   (a) haploid gametes only (b) diploid cells (c) two haploid cells identical to the parent (d) four haploid cells
11. Spindle fibres attach to a chromosome at the
   (a) telomere (b) satellite (c) chiasma (d) kinetochore of the centromere
12. In a cell with 2n = 8, the number of bivalents at metaphase I is
   (a) 8 (b) 4 (c) 16 (d) 2
13. A cell in G₀
   (a) has left the cycle and is not dividing (b) is in S phase (c) has no DNA (d) is undergoing meiosis
14. Colchicine-treated cells show a doubled chromosome number because colchicine
   (a) breaks the DNA (b) prevents DNA replication (c) prevents spindle formation, so the nucleus re-forms undivided (d) dissolves the cell wall
15. The significance of crossing over is that it
   (a) halves the chromosome number (b) exchanges segments between non-sister chromatids (c) separates sister chromatids (d) doubles the DNA
16. A plant cell differs from an animal cell at cytokinesis because the plant cell
   (a) has no spindle (b) divides by binary fission (c) forms a cleavage furrow (d) forms a cell plate from Golgi vesicles
17. The enzyme used to separate cells by digesting the middle lamella is
   (a) pectinase (b) cellulase (c) ligase (d) amylase
18. If the DNA content of a cell in G₁ is 2C, the content at metaphase of mitosis is
   (a) 2C (b) C (c) 4C (d) 8C

::: note Answers and explanations — Set B
**1.** (c) — Viruses have no cell, cytoplasm or ribosomes; they are obligate parasites and cannot reproduce alone.
**2.** (a) — The aseptate hypha is a continuous cytoplasm with many nuclei, so "one cell, one nucleus" fails.
**3.** (d) — The wall resists the pressure; an animal cell without a wall would swell and lyse.
**4.** (b) — They carry their own circular DNA and 70S ribosomes, yet most of their proteins are coded by nuclear genes.
**5.** (a) — The membrane isolates the acid hydrolases; if it leaks, the cell digests itself.
**6.** (c) — Secretory proteins are made on rough ER and packed by the Golgi. Chloroplasts and cilia have nothing to do with secretion.
**7.** (b) — mRNA leaves and ribosomal proteins enter through the pore; ribosomes are assembled in the cytoplasm, not exported whole.
**8.** (d) — The centromeres split, so 46 chromosomes become 92 daughter chromosomes before cytokinesis.
**9.** (a) — Crossing over and independent assortment generate new combinations; mitosis makes identical cells.
**10.** (c) — Mitosis conserves the number, so a haploid parent gives two haploid daughters.
**11.** (d) — The kinetochore, a protein plate on the centromere, is the attachment point.
**12.** (b) — Eight chromosomes make four homologous pairs, hence four bivalents.
**13.** (a) — G₀ is the resting state outside the cycle; the DNA is intact but not being replicated.
**14.** (c) — Without a spindle the chromosomes cannot separate, so the nuclear envelope re-forms around a doubled set.
**15.** (b) — Non-sister chromatids of homologous chromosomes exchange segments, producing recombinant chromatids.
**16.** (d) — Golgi vesicles line up at the equator and fuse into a cell plate; the animal cell pinches in.
**17.** (a) — Pectinase digests the calcium pectate of the middle lamella, releasing single cells — the basis of protoplast and tissue-culture work.
**18.** (c) — DNA doubles in S phase, so a 2C cell reaches 4C by metaphase, though the chromosome number is unchanged.
:::

**Set C — Application (12 questions)**

1. A human cell with 46 chromosomes completes meiosis. The number of cells and the chromosome number in each are
   (a) 2 and 46 (b) 4 and 23 (c) 4 and 46 (d) 2 and 23
2. A cell has 2n = 24. At anaphase of mitosis, the number of chromosomes in the cell is
   (a) 12 (b) 24 (c) 36 (d) 48
3. An organism has 2n = 6. Ignoring crossing over, how many different combinations of maternal and paternal chromosomes can a gamete receive?
   (a) 3 (b) 6 (c) 8 (d) 64
4. A cell in G₁ has 10 chromosomes and 10 DNA molecules. At metaphase I of meiosis it has
   (a) 10 chromosomes and 20 DNA molecules (b) 20 chromosomes and 20 DNA molecules (c) 10 chromosomes and 10 DNA molecules (d) 5 chromosomes and 10 DNA molecules
5. After meiosis I, each daughter of a 2n = 10 cell has
   (a) 10 chromosomes and 10 DNA molecules (b) 5 chromosomes and 5 DNA molecules (c) 10 chromosomes and 20 DNA molecules (d) 5 chromosomes and 10 DNA molecules
6. A drug blocks formation of the cell plate. Which cells are affected?
   (a) animal cells only (b) plant cells only (c) bacterial cells only (d) both plant and animal cells
7. An onion root-tip cell has 2n = 16. At anaphase of mitosis it contains
   (a) 8 chromosomes (b) 16 chromosomes (c) 32 chromosomes (d) 64 chromosomes
8. Two genes lie on different chromosomes. The gametes of a heterozygote AaBb are produced in the ratio
   (a) 1 : 1 : 1 : 1 (b) 3 : 1 (c) 9 : 3 : 3 : 1 (d) 1 : 2 : 1
9. A cell has 2n = 46. After meiosis II, the DNA content of each cell compared with G₁ is
   (a) the same (b) half (c) double (d) four times
10. A moss gametophyte has 12 chromosomes in each cell. The sporophyte cells have
   (a) 6 (b) 12 (c) 48 (d) 24
11. Crossing over occurs between two linked genes in 20 % of meioses. The recombination frequency is
   (a) 10 % (b) 20 % (c) 40 % (d) 5 %
12. A cell with 2n = 8 undergoes meiosis. The number of chromatids per cell at metaphase II is
   (a) 4 (b) 16 (c) 8 (d) 2

::: note Answers and explanations — Set C
**1.** (b) — Two divisions give four cells, and the chromosome number is halved to 23.
**2.** (d) — At anaphase the 24 centromeres split, giving 48 daughter chromosomes in the cell before cytokinesis.
**3.** (c) — $2^n$ with n = 3 gives 8 combinations.
**4.** (a) — After S phase the DNA is doubled (20 molecules) but the chromosome number is still 10; the 10 chromosomes form 5 bivalents.
**5.** (d) — Meiosis I halves the chromosome number to 5, but each chromosome still has two chromatids, so 10 DNA molecules.
**6.** (b) — Only walled cells build a cell plate; animal cells use a cleavage furrow.
**7.** (c) — The 16 centromeres split, so 32 daughter chromosomes are present at anaphase.
**8.** (a) — Independent assortment of two unlinked pairs gives four gamete types in equal numbers.
**9.** (b) — Meiosis halves the DNA: a 2C cell yields 1C gametes.
**10.** (d) — The sporophyte is diploid, so 2 × 12 = 24.
**11.** (a) — Each meiosis with a crossover yields 2 recombinant chromatids out of 4, so 20 % × ½ = 10 %.
**12.** (c) — After meiosis I each cell has 4 chromosomes, each with 2 chromatids: 8 chromatids at metaphase II.
:::
