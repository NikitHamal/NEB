---
subject: Biology
grade: 12
unit: 6
title: Animal Tissues
hours: 8
area: Zoology
---

A tissue is a group of similar cells, together with their intercellular material,
that share a common origin and do one job. The multicellular animal body is built
from only four of them — epithelial, connective, muscular and nervous. Every organ
you meet in the Human Biology unit, from the stomach wall to the eyeball, is these
four tissues stacked in different proportions. Learn the four properly now and the
rest of Zoology becomes description rather than memorisation.

::: key What the examiner asks from this unit
Three things, every year. A **labelled diagram** of a named tissue as it looks
under the microscope — the neuron, the T.S. of bone, the three muscle types.
A **difference table** — tendon vs ligament, cartilage vs bone, striated vs
cardiac vs smooth muscle. And a **"where is it found and why"** question, which
wants structure linked to function, not a list. Practise drawing; a correct
diagram with six labels is often the whole four marks.
:::

## 6.1 Epithelial tissue

::: definition Epithelial tissue
Epithelium is a sheet of closely packed cells, with almost no intercellular
matrix, resting on a non-cellular **basement membrane**, which covers the free
surfaces of the body and lines its cavities, ducts and tubes.
:::

Epithelium is the only tissue that arises from all three germ layers: the
epidermis of the skin and the lining of the mouth and anus are ectodermal, the
lining of the gut and its glands endodermal, and the lining of blood vessels,
kidney tubules and coelom mesodermal.

Its general characters follow from its job of forming a boundary:

- Cells are packed tightly and joined by **cell junctions** (tight junctions,
  desmosomes), so the sheet is continuous and leak-proof.
- Intercellular matrix is negligible.
- The sheet has **polarity** — a free (apical) surface and a basal surface
  cemented to the basement membrane, a thin glycoprotein layer secreted partly
  by the epithelium and partly by the connective tissue below.
- It is **avascular**. No blood vessel enters an epithelium; food and oxygen
  diffuse in from the capillaries of the connective tissue beneath.
- It has a very high **power of regeneration**, because it is the layer that
  gets worn away.

Epithelia are classified first by the number of cell layers, then by the shape
of the cells at the free surface.

```photo id="bio12/squamous-epithelium" caption="(a) Simple squamous epithelium in surface view (silver-stained whole mount, ×100): thin, flat, polygonal cells fit edge to edge like paving stones, and the silver outlines each boundary." width="66"
```

```photo id="bio12/cuboidal-epithelium" caption="(b) Simple cuboidal epithelium lining kidney tubules (×100): each tube is a single layer of cube-shaped cells with a round central nucleus around an open lumen." width="66"
mark 0.775 0.65 "1"
mark 0.30 0.50 "2"
key 1 Lumen of the tubule
key 2 Cuboidal cell with a central, round nucleus
```

```photo id="bio12/columnar-epithelium" caption="(c) Simple columnar epithelium with goblet cells (×400): tall cells with basal oval nuclei line the lumen; the pale rounded cells between them are mucus-filled goblet cells." width="66"
```
### Compound (stratified) epithelium

When the epithelium must resist wear, it becomes many cells thick. Only the
deepest layer — the **germinative** or Malpighian layer — touches the basement
membrane and divides; its daughter cells are pushed upwards, flatten, die and
are shed. In the epidermis of the skin the dying cells fill with the protein
**keratin**, giving a dry, waterproof, *keratinised* stratified squamous
epithelium. In the mouth, oesophagus and vagina the surface stays moist and the
epithelium is *non-keratinised*.

**Transitional epithelium** (urothelium) lines the ureter and urinary bladder.
It has no true stratum corneum, and its cells slide over one another so the
sheet can stretch: relaxed it looks 4–5 cells thick with dome-shaped surface
cells, distended it looks 2–3 cells thick and flat.

```photo id="bio12/transitional-epithelium" caption="Transitional epithelium of the urinary bladder (×100). Several layers of cells with large, rounded surface cells that flatten when the bladder is stretched, which is why the organ can fill without tearing." width="70"
mark 0.70 0.70 "1"
mark 0.95 0.40 "2"
key 1 Transitional epithelium — many cell layers, surface cells large and dome-shaped
key 2 Connective tissue (lamina propria) beneath the epithelium
```
### Glandular epithelium

When epithelial cells specialise for secretion they sink into the connective
tissue below and form a **gland**. A single cell doing this is a unicellular
gland — the **goblet cell** of the gut and trachea. Many cells doing it together
make a multicellular gland, tubular if the secretory part is a tube (intestinal
crypts, sweat glands) or alveolar/acinar if it is a flask (salivary, sebaceous).

Glands are grouped by where the secretion goes — **exocrine** glands release
through a duct, **endocrine** glands have no duct and pour hormones into the
blood — and by how the cell releases it.

| Mode | How the cell secretes | Example |
|---|---|---|
| Merocrine | by exocytosis; the cell stays intact | salivary gland, pancreas |
| Apocrine | apical part of the cell pinches off with the secretion | mammary gland |
| Holocrine | the whole cell disintegrates and becomes the secretion | sebaceous gland |

```figure caption="Glandular epithelium: a unicellular goblet cell and the two commonest multicellular forms."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon, Circle
fig, axes = plt.subplots(1, 3, figsize=(5.2, 3.0),
                         gridspec_kw=dict(wspace=0.07))
CELL = "#e7eff7"; EDGE = "#2c5f96"; NUC = "#41638a"; BM = "#b5832f"; MUC = "#cfe0d2"
WB = dict(fc='white', ec='none', pad=0.5)

def lab(ax, t, s):
    ax.text(0.5, -0.42, t, ha='center', fontsize=6.9, color=INK)
    ax.text(0.5, -0.62, s, ha='center', fontsize=5.9, color=MUTED)

for ax in axes:
    ax.set_xlim(0, 1); ax.set_ylim(-0.74, 1.46); ax.axis('off')

# (a) unicellular goblet cell, enlarged
ax = axes[0]
ax.plot([0.08, 0.92], [0.06, 0.06], color=BM, lw=2.0, zorder=2)
for x0 in (0.10, 0.24, 0.64, 0.78):
    ax.add_patch(Polygon([[x0, 0.06], [x0+0.12, 0.06], [x0+0.12, 0.72], [x0, 0.72]],
                         closed=True, fc=CELL, ec=EDGE, lw=0.85, zorder=3))
    ax.add_patch(Ellipse((x0+0.06, 0.26), 0.058, 0.15, fc=NUC, ec='none', zorder=4))
t = np.linspace(0, 1, 70)
cx = 0.50
left = cx - 0.135*(0.18 + 0.82*t**0.75); right = cx + 0.135*(0.18 + 0.82*t**0.75)
y = 0.06 + 0.66*t
ax.add_patch(Polygon(np.vstack([np.c_[left, y], np.c_[right[::-1], y[::-1]]]),
                     closed=True, fc=MUC, ec=EDGE, lw=1.0, zorder=3))
ax.add_patch(Ellipse((cx, 0.19), 0.058, 0.13, fc=NUC, ec='none', zorder=4))
for dy, r in ((0.86, 0.036), (0.99, 0.026), (1.10, 0.018)):
    ax.add_patch(Ellipse((cx, dy), r*1.4, r*2.6, fc=MUC, ec=EDGE, lw=0.5, zorder=4))
ax.annotate('mucus', xy=(cx+0.035, 0.94), xytext=(0.84, 1.16),
            fontsize=5.7, color=MUTED, ha='center', bbox=WB,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.annotate('nucleus pushed\nto the base', xy=(cx-0.03, 0.19), xytext=(0.22, 1.10),
            fontsize=5.5, color=MUTED, ha='center', linespacing=1.2, bbox=WB,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
lab(ax, '(a) unicellular gland', 'goblet cell')

# (b) simple tubular gland
ax = axes[1]
ax.plot([0.03, 0.97], [1.02, 1.02], color=BM, lw=2.0, zorder=2)
for x0 in (0.04, 0.17, 0.70, 0.83):
    ax.add_patch(Polygon([[x0, 1.02], [x0+0.12, 1.02], [x0+0.12, 1.30], [x0, 1.30]],
                         closed=True, fc=CELL, ec=EDGE, lw=0.85, zorder=3))
for s in (-1, 1):
    ax.add_patch(Polygon([[0.50+s*0.075, 1.02], [0.50+s*0.075, 0.14],
                          [0.50+s*0.150, 0.14], [0.50+s*0.150, 1.02]],
                         closed=True, fc=CELL, ec=EDGE, lw=0.9, zorder=3))
    for yy in np.linspace(0.22, 0.92, 6):
        ax.plot([0.50+s*0.075, 0.50+s*0.150], [yy, yy], color=EDGE, lw=0.5, zorder=4)
        ax.add_patch(Ellipse((0.50+s*0.1125, yy+0.070), 0.030, 0.062,
                             fc=NUC, ec='none', zorder=5))
ax.add_patch(Polygon([[0.350, 0.14], [0.650, 0.14], [0.650, 0.05], [0.350, 0.05]],
                     closed=True, fc=CELL, ec=EDGE, lw=0.9, zorder=3))
ax.annotate('', xy=(0.50, 1.36), xytext=(0.50, 0.28),
            arrowprops=dict(arrowstyle='-|>', color='#c0392b', lw=1.1, mutation_scale=9))
ax.annotate('secretory cells', xy=(0.395, 0.55), xytext=(0.50, -0.14),
            fontsize=5.6, color=MUTED, ha='center', bbox=WB,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.text(0.50, 1.42, 'secretion out', ha='center', fontsize=5.6, color='#c0392b')
lab(ax, '(b) simple tubular', 'intestinal crypt, sweat gland')

# (c) simple alveolar gland
ax = axes[2]
ax.plot([0.03, 0.97], [1.02, 1.02], color=BM, lw=2.0, zorder=2)
for x0 in (0.04, 0.17, 0.70, 0.83):
    ax.add_patch(Polygon([[x0, 1.02], [x0+0.12, 1.02], [x0+0.12, 1.30], [x0, 1.30]],
                         closed=True, fc=CELL, ec=EDGE, lw=0.85, zorder=3))
for s in (-1, 1):
    ax.add_patch(Polygon([[0.50+s*0.048, 1.02], [0.50+s*0.048, 0.62],
                          [0.50+s*0.108, 0.62], [0.50+s*0.108, 1.02]],
                         closed=True, fc=CELL, ec=EDGE, lw=0.9, zorder=3))
ax.add_patch(Ellipse((0.50, 0.36), 0.54, 0.54, fc="#f2f7fb", ec=EDGE, lw=1.0, zorder=3))
ax.add_patch(Ellipse((0.50, 0.36), 0.30, 0.30, fc="#ffffff", ec=EDGE, lw=0.7, zorder=4))
for a in np.linspace(0, 2*np.pi, 13)[:-1]:
    ax.add_patch(Ellipse((0.50 + 0.210*np.cos(a), 0.36 + 0.210*np.sin(a)),
                         0.040, 0.040, fc=NUC, ec='none', zorder=5))
ax.annotate('', xy=(0.50, 1.36), xytext=(0.50, 0.70),
            arrowprops=dict(arrowstyle='-|>', color='#c0392b', lw=1.1, mutation_scale=9))
ax.annotate('duct', xy=(0.455, 0.84), xytext=(0.20, 0.92), fontsize=5.7,
            color=MUTED, ha='center', bbox=WB,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.text(0.50, 0.36, 'lumen', fontsize=5.4, color=MUTED, ha='center', va='center')
ax.annotate('flask of secretory cells', xy=(0.74, 0.20), xytext=(0.50, -0.14),
            fontsize=5.6, color=MUTED, ha='center', bbox=WB,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
lab(ax, '(c) simple alveolar', 'sebaceous, salivary gland')
```
| Type | Shape at free surface | Chief location | Main function |
|---|---|---|---|
| Simple squamous | flat, tile-like, central bulge | alveoli, Bowman's capsule, endothelium of vessels | diffusion, filtration |
| Simple cuboidal | cube, round central nucleus | kidney tubules, thyroid follicles, gland ducts | absorption, secretion |
| Simple columnar | tall, nucleus near the base | stomach, small intestine, gall bladder | secretion, absorption |
| Ciliated columnar | tall, with cilia | oviduct, bronchioles, ventricles of brain | moves mucus, ovum, CSF |
| Pseudostratified | tall and short cells, nuclei at two levels | trachea, nasal cavity, male urethra | protection, mucus movement |
| Stratified squamous | many layers, flat and dead at the top | epidermis, oesophagus, vagina, cornea | protection against wear |
| Transitional | 2–5 layers, cells slide | ureter, urinary bladder | allows stretching |
| Glandular | secretory, sunk into the tissue | gut lining, all glands | secretion |

::: caution "Pseudostratified" is not "stratified"
A pseudostratified epithelium is **one cell layer thick**. Every cell reaches
the basement membrane, but the cells are of different heights, so their nuclei
sit at different levels and the sheet only *looks* layered. A stratified
epithelium has real layers and only the deepest touches the basement membrane.
:::

::: example Worked example 6.1 — magnification and real cell size
**Problem.** In a photomicrograph of the lining of the small intestine taken at
a magnification of $\times 1000$, one columnar cell measures $40\ \text{mm}$
from base to free surface and $8\ \text{mm}$ across. (a) Find its real height
and width in micrometres. (b) How many such cells lie side by side along
$1\ \text{mm}$ of the intestinal lining?

**Solution.** Magnification is defined as

$$ M = \frac{\text{image size}}{\text{actual size}} \;\Rightarrow\;
\text{actual size} = \frac{\text{image size}}{M} $$

(a) Height:

$$ \frac{40\ \text{mm}}{1000} = 0.040\ \text{mm} = 0.040 \times 1000\ \mu\text{m}
 = 40\ \mu\text{m} $$

Width: $8/1000 = 0.008\ \text{mm} = 8\ \mu\text{m}$. (Recall $1\ \text{mm} = 1000\ \mu\text{m}$.)

(b) Each cell is $8\ \mu\text{m}$ wide and $1\ \text{mm} = 1000\ \mu\text{m}$, so

$$ n = \frac{1000\ \mu\text{m}}{8\ \mu\text{m}} = 125\ \text{cells} $$

A cell $40\ \mu\text{m}$ tall and only $8\ \mu\text{m}$ wide is five times taller
than it is broad — that is exactly what "columnar" means.
:::

## 6.2 Connective tissue

::: definition Connective tissue
Connective tissue is a mesodermal tissue in which relatively few cells lie
scattered in an abundant **intercellular matrix** of fibres and ground
substance. It binds, supports, packs, transports and defends.
:::

Connective tissue is the mirror image of epithelium: there the cells crowd
together and the matrix is negligible, here the matrix does the work and the
cells are far apart. Its properties are the properties of its matrix. Three
kinds of fibre are woven into it:

- **White collagen fibres** — thick, wavy, non-branching bundles of the protein
  collagen. Very strong, inelastic. Boiling turns them into gelatin.
- **Yellow elastic fibres** — thinner, straight, branching fibres of elastin.
  They stretch to about 1.5 times their length and snap back.
- **Reticular fibres** — fine branching collagen, forming the mesh of lymph
  nodes, spleen and bone marrow.

The commonest cells are the **fibroblast** (spindle-shaped; makes the fibres and
ground substance), the **macrophage** or histiocyte (amoeboid; engulfs bacteria
and debris), the **mast cell** (granular; secretes heparin, which stops blood
clotting inside vessels, and histamine, which causes inflammation and allergy),
the **plasma cell** (secretes antibodies) and the **adipocyte** (stores fat).

| Group | Types | Distinguishing feature | Chief function |
|---|---|---|---|
| Loose connective | areolar, adipose, reticular | soft, cells many, matrix loose | packing, fat store, framework |
| Dense connective | tendon, ligament (regular); dermis (irregular) | fibres crowded and ordered | transmits or resists pull |
| Skeletal (supporting) | cartilage, bone | matrix solid | support, protection, movement |
| Fluid (vascular) | blood, lymph | matrix is liquid plasma | transport, defence |

### Loose connective tissue

**Areolar tissue** is the universal packing material — under the skin, between
muscles, around nerves, blood vessels and organs. Its loose, jelly-like matrix
lets tissue fluid and white blood cells move freely, which is why it is also the
main site of inflammation.

**Adipose tissue** is areolar tissue in which fat-storing cells have multiplied.
Each adipocyte is almost filled by a single fat droplet, so the cytoplasm is a
thin rim and the nucleus is squashed against one side — the "signet-ring"
appearance. It stores energy, insulates against cold and cushions the kidneys,
eyeballs and soles of the feet.

```photo id="bio12/areolar" caption="(a) Areolar (loose) connective tissue, spread preparation (×400): a loose meshwork of fibres with scattered cells in a soft ground substance." width="66"
mark 0.50 0.50 "1"
mark 0.30 0.74 "2"
mark 0.60 0.28 "3"
key 1 Collagen fibres — thick, pink, wavy bundles
key 2 Elastic fibres — thin, dark, branching and straight
key 3 Fibroblast nucleus
```

```photo id="bio12/adipose" caption="(b) Adipose tissue (×100). The fat droplet fills each cell and pushes the cytoplasm and nucleus into a thin rim at the edge, so the cells look empty in a stained section." width="66"
mark 0.13 0.22 "1"
mark 0.60 0.55 "2"
key 1 Nucleus pushed to one side by the fat droplet
key 2 Adipocyte — the droplet-filled space
```
### Dense connective tissue

In dense tissue the fibres are packed so tightly that the cells are squeezed
into rows between them. When the fibres all run one way the tissue is *regular*
and resists pull along a single line — the tendon and the ligament. When they
run in all directions it is *irregular* and resists pull from any direction —
the dermis of the skin and the capsules of organs.

```photo id="bio12/tendon" caption="Dense regular connective tissue of a tendon (×400): parallel, wavy bundles of collagen with a few flattened fibroblast nuclei squeezed between them, which gives great strength along one direction. A ligament has the same build with branching yellow elastic fibres among the collagen." width="76"
```

| Feature | Tendon | Ligament |
|---|---|---|
| Chief fibre | white collagen | yellow elastic |
| Arrangement | straight, parallel bundles | branching, interlacing |
| Elasticity | almost none — inextensible | elastic, stretches and recoils |
| Colour when fresh | glistening white | yellowish |
| Cells | fibroblasts in rows between bundles | fibroblasts scattered |
| Connects | muscle to bone | bone to bone at a joint |
| Blood supply | poor, so it heals slowly | poor |

### Cartilage

Cartilage is a solid but flexible skeletal tissue. Its cells, the
**chondrocytes**, sit singly or in twos inside fluid-filled spaces called
**lacunae**, embedded in a firm matrix of the protein **chondrin**. The whole
mass is wrapped in a fibrous sheath, the **perichondrium**, from which it grows
and through which it is fed — because cartilage itself has no blood vessels.

| Type | Matrix contains | Where found |
|---|---|---|
| Hyaline | chondrin only; clear, bluish, glassy | tracheal rings, nose tip, articular surfaces, embryonic skeleton |
| Elastic | a network of yellow elastic fibres | pinna of ear, epiglottis, eustachian tube |
| Fibrous (white) | dense bundles of collagen | intervertebral discs, pubic symphysis |
| Calcified | calcium salts deposited in the matrix | head of the humerus, suprascapula of frog |

```photo id="qbank/hyaline-cartilage" caption="(a) Hyaline cartilage (×100): chondrocytes sit singly or in small groups in lacunae in a smooth, glassy matrix." width="66"
```

```photo id="bio12/elastic-cartilage" caption="(b) Elastic cartilage (×100): the matrix is full of dark-stained elastic fibres, giving flexibility (external ear, epiglottis)." width="66"
mark 0.62 0.70 "1"
mark 0.50 0.37 "2"
key 1 Chondrocyte in a lacuna
key 2 Perichondrium — the fibrous covering of the cartilage
```

```photo id="bio12/fibrocartilage" caption="(c) Fibrocartilage (×100): dense bundles of collagen run in rows through the matrix, resisting compression (intervertebral discs, pubic symphysis)." width="66"
```

### Bone

Bone is the hardest connective tissue. Its matrix, **ossein**, is about one-third
organic protein — which gives toughness — and two-thirds inorganic salts, mainly
calcium phosphate with some calcium carbonate, which give hardness. Bone cells,
the **osteocytes**, lie in lacunae and keep in touch with one another and with
the blood supply through hair-fine channels, the **canaliculi**.

In the compact bone of a mammal, this material is organised into cylinders. Each
cylinder, an **osteon** or **Haversian system**, is a central **Haversian canal**
carrying a blood capillary, a lymph vessel and a nerve, surrounded by 4–20
concentric **lamellae** of matrix with rings of lacunae between them. Haversian
canals run lengthwise along the bone and are linked sideways by **Volkmann's
canals**. The whole bone is sheathed in the **periosteum**.

```photo id="bio12/compact-bone" caption="T.S. of compact bone (ground section, ×100): concentric lamellae surround each central canal to form an osteon (Haversian system). The right-hand copy is the same section with its parts named; every osteocyte sits in a lacuna and reaches the canal through its canaliculi." width="92"
crop 0.46 0.0 1.0 1.0
```
| Feature | Cartilage | Bone |
|---|---|---|
| Matrix | chondrin (protein), soft and flexible | ossein + calcium salts, hard and rigid |
| Cells | chondrocytes, 1–4 per lacuna | osteocytes, 1 per lacuna |
| Canaliculi | absent | present, linking lacunae |
| Blood supply | absent (avascular) | rich, through Haversian canals |
| Covering | perichondrium | periosteum |
| Growth | interstitial and appositional | appositional only |

::: caution Cartilage heals slowly — and frog bone has no Haversian systems
Because cartilage has no blood vessels, its cells are fed only by diffusion
through the matrix from the perichondrium. That is why a torn knee cartilage
heals far more slowly than a broken bone. Second point, often asked: well-formed
Haversian systems are a feature of **mammalian** compact bone. The bone of the
frog and other lower vertebrates is nourished by diffusion and **lacks Haversian
canals**.
:::

### Fluid connective tissue

Blood is a connective tissue whose matrix is liquid. About 55% of it by volume
is **plasma** — 90–92% water, with plasma proteins (albumin, globulin,
fibrinogen), glucose, salts, hormones and wastes — and about 45% is the
**formed elements**.

| Formed element | Normal count (per mm³) | Structure | Function |
|---|---|---|---|
| Erythrocyte (RBC) | 4.5–5.5 million | biconcave disc, 7–8 μm, no nucleus in mammals | carries O₂ and CO₂ as oxyhaemoglobin and carbaminohaemoglobin |
| Neutrophil | 4000–11000 WBC in total; 60–65% of them | 3–5 lobed nucleus, fine granules | phagocytosis of bacteria |
| Eosinophil | 2–3% of WBC | bilobed nucleus, coarse granules | allergy and parasite defence |
| Basophil | 0.5–1% of WBC | lobed nucleus, large dark granules | secretes heparin and histamine |
| Lymphocyte | 20–25% of WBC | large round nucleus, thin cytoplasm | antibodies and cell-mediated immunity |
| Monocyte | 6–8% of WBC | kidney-shaped nucleus, largest WBC | becomes a macrophage in tissues |
| Thrombocyte (platelet) | 150,000–400,000 | cell fragment, no nucleus | blood clotting |

```photo id="qbank/blood-leukocytes" caption="Human blood smear (×400). The many small pink discs without nuclei are red blood cells; the few cells with a dark-stained nucleus are white blood cells. Compare the proportions — red cells outnumber white cells roughly 700 to 1." width="70"
mark 0.55 0.62 "1"
mark 0.42 0.45 "2"
mark 0.84 0.27 "3"
key 1 Erythrocyte (red blood cell) — biconcave, no nucleus in mammals
key 2 Leucocyte (white blood cell) — nucleus stains dark
key 3 Another leucocyte, with a lobed nucleus
```
::: example Worked example 6.2 — counting red cells with a haemocytometer
**Problem.** Blood is diluted 1 : 200 and loaded into a Neubauer counting
chamber. The central ruled square is $1\ \text{mm} \times 1\ \text{mm}$, divided
into 400 small squares, and the depth under the cover-slip is $0.1\ \text{mm}$.
A student counts 500 red cells in 80 small squares. Find the RBC count per mm³
and say whether the person is anaemic.

**Solution.** Area of one small square:

$$ A = \frac{1\ \text{mm}^{2}}{400} = 2.5 \times 10^{-3}\ \text{mm}^{2} $$

Volume of blood over 80 small squares:

$$ V = 80 \times (2.5 \times 10^{-3}\ \text{mm}^{2}) \times 0.1\ \text{mm}
= 0.02\ \text{mm}^{3} $$

Cells per mm³ of the **diluted** blood:

$$ \frac{500}{0.02} = 25\,000\ \text{per mm}^{3} $$

Multiplying by the dilution factor 200 to get back to whole blood:

$$ 25\,000 \times 200 = 5\,000\,000 = 5 \times 10^{6}\ \text{per mm}^{3} $$

Five million per mm³ lies in the normal range of 4.5–5.5 million, so the person
is **not anaemic**.
:::

## 6.3 Muscular tissue

::: definition Muscular tissue
Muscular tissue is a mesodermal tissue made of elongated cells, the **muscle
fibres**, whose cytoplasm is packed with the contractile protein filaments
**actin** and **myosin**, so that the cell can shorten and generate force.
:::

A muscle fibre has its own vocabulary: the cell membrane is the **sarcolemma**,
the cytoplasm the **sarcoplasm**, the endoplasmic reticulum the **sarcoplasmic
reticulum** (it stores the Ca²⁺ that triggers contraction), and the contractile
threads running the length of the fibre are the **myofibrils**. About 40% of the
body mass of an adult is muscle, in three kinds.

```photo id="bio12/skeletal-muscle" caption="(a) Skeletal muscle in longitudinal section (×400): long, unbranched, cross-striated fibres, each with many nuclei at the edge." width="66"
mark 0.10 0.40 "1"
mark 0.25 0.55 "2"
key 1 Cross-striations (alternating A and I bands)
key 2 One of the many peripheral nuclei of a single fibre
```

```photo id="bio12/cardiac-discs2" caption="(b) Cardiac muscle (iron haematoxylin, ×400): short, striated, branching fibres joined end to end — each with one central nucleus — form a continuous network." width="66"
```

```photo id="bio12/smooth-muscle" caption="(c) Smooth muscle (×400): spindle-shaped, unstriated cells, each with a single central nucleus, lie in overlapping bundles." width="66"
```
| Feature | Striated (skeletal) | Cardiac | Smooth (unstriated) |
|---|---|---|---|
| Shape of fibre | long, cylindrical, unbranched | cylindrical, **branched** | spindle-shaped (fusiform) |
| Striations | present, prominent | present, faint | absent |
| Nuclei | many, at the periphery | one (rarely two), central | one, central |
| Intercalated discs | absent | **present** | absent |
| Control | voluntary | involuntary | involuntary |
| Speed and fatigue | fast, powerful, tires quickly | moderate, rhythmic, never tires | slow, sustained, tires slowly |
| Location | attached to bones, tongue, diaphragm | wall of the heart only | gut, uterus, blood vessels, iris, bronchi |

### The sarcomere

Under high power, a myofibril shows repeating light and dark bands. The dark
**A band** (anisotropic) is the length of the thick myosin filaments; the light
**I band** (isotropic) contains only thin actin filaments and is bisected by a
dark **Z line**. The **H zone** in the middle of the A band contains myosin
only, and is crossed by the **M line**.

::: definition Sarcomere
A sarcomere is the segment of a myofibril between two successive Z lines. It is
the **functional (contractile) unit** of striated muscle. At rest it is about
2.0–2.5 μm long.
:::

```photo id="bio12/sarcomere-tem" caption="Electron micrograph of a skeletal-muscle fibre in longitudinal section. The dark Z lines mark the ends of each sarcomere; between them the darker A band and paler I band alternate regularly, which is what gives the fibre its striped look under the light microscope." width="80"
```

```figure caption="One sarcomere, the unit between two Z lines. During contraction the filaments do not shorten — the actin slides over the myosin, so the I band and H zone narrow while the A band stays the same length."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.2, 3.0))
ACT = "#3f7fb8"; MYO = "#a8433c"; ZL = "#2b3440"
ax.set_xlim(-1.3, 11.3); ax.set_ylim(-4.0, 4.0); ax.axis('off')

# shaded A band
ax.add_patch(Polygon([[2.5, -1.55], [7.5, -1.55], [7.5, 1.55], [2.5, 1.55]],
                     closed=True, fc="#f3e2e0", ec='none', zorder=1))
rows = [-1.15, -0.45, 0.45, 1.15]
# thin actin filaments from each Z line
for y in rows:
    ax.plot([0.0, 4.35], [y, y], color=ACT, lw=2.0, zorder=3, solid_capstyle='butt')
    ax.plot([5.65, 10.0], [y, y], color=ACT, lw=2.0, zorder=3, solid_capstyle='butt')
# thick myosin filaments with cross-bridges
for y in (-0.80, 0.80):
    ax.plot([2.5, 7.5], [y, y], color=MYO, lw=4.2, zorder=4, solid_capstyle='butt')
    for x in np.arange(2.75, 7.5, 0.55):
        if abs(x - 5.0) > 0.75:
            s = -1 if y > 0 else 1
            ax.plot([x, x + 0.18], [y, y + s*0.34], color=MYO, lw=1.0, zorder=5)
# Z lines and M line
for x in (0.0, 10.0):
    ax.plot([x, x], [-1.75, 1.75], color=ZL, lw=3.0, zorder=6, solid_capstyle='butt')
ax.plot([5.0, 5.0], [-1.25, 1.25], color=ZL, lw=1.6, ls=(0, (2, 1.6)), zorder=6)

def span(y, x0, x1, t, col=INK, fs=7.0, up=True):
    ax.annotate('', xy=(x0, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle='<|-|>', color=col, lw=0.9, mutation_scale=7))
    ax.text((x0 + x1)/2, y + (0.24 if up else -0.62), t, ha='center',
            fontsize=fs, color=col)

span(2.95, 0.0, 10.0, 'sarcomere  (Z line to Z line,  $\\approx 2.5\\ \\mu$m)')
span(-2.25, 2.5, 7.5, 'A band (dark) — myosin present', up=False)
span(-2.25, 0.0, 2.5, 'half I band', up=False)
span(-2.25, 7.5, 10.0, 'half I band', up=False)
span(2.10, 4.35, 5.65, 'H zone', up=True)
ax.text(0.0, 2.02, 'Z line', ha='center', fontsize=6.6, color=ZL)
ax.text(10.0, 2.02, 'Z line', ha='center', fontsize=6.6, color=ZL)
ax.text(5.0, 1.62, 'M line', ha='center', fontsize=6.6, color=ZL)
ax.text(1.05, 0.02, 'actin\n(thin)', ha='center', va='center', fontsize=6.3,
        color=ACT, linespacing=1.2)
ax.text(6.55, 0.02, 'myosin\n(thick)', ha='center', va='center', fontsize=6.3,
        color=MYO, linespacing=1.2)
ax.text(5.0, -3.60, 'I band and H zone shorten on contraction; the A band does not',
        ha='center', fontsize=6.3, color=MUTED)
```
::: example Worked example 6.3 — how far does a muscle shorten?
**Problem.** A myofibril in the biceps is $2.4\ \text{cm}$ long and its
sarcomeres are each $2.4\ \mu\text{m}$ long at rest. (a) How many sarcomeres
lie end to end along it? (b) If every sarcomere shortens to $1.8\ \mu\text{m}$
during a full contraction, what is the new length of the myofibril and the
percentage shortening?

**Solution.**

(a) Convert to the same unit: $2.4\ \text{cm} = 24\ \text{mm} = 24\,000\ \mu\text{m}$.

$$ n = \frac{24\,000\ \mu\text{m}}{2.4\ \mu\text{m}} = 10\,000\ \text{sarcomeres} $$

(b) New length $= 10\,000 \times 1.8\ \mu\text{m} = 18\,000\ \mu\text{m} = 1.8\ \text{cm}$.

$$ \text{shortening} = \frac{2.4 - 1.8}{2.4}\times 100 = 25\% $$

Each sarcomere shortens by only $0.6\ \mu\text{m}$, but because 10,000 of them
are joined in series the whole fibril shortens by $0.6\ \text{cm}$. That is how
a change too small to see adds up to a visible movement.
:::

## 6.4 Nervous tissue

Nervous tissue is ectodermal and is built from two kinds of cell: the
**neurons**, which carry the messages, and the **neuroglia**, about ten times
more numerous, which support, insulate, feed and defend them. Neurons are
excitable — they respond to a stimulus by generating an electrical impulse — and
conductive — they pass that impulse on. Mature neurons have lost the power to
divide, which is why nerve damage is often permanent.

A typical motor neuron has three parts:

1. **Cyton (cell body or perikaryon)** — contains the nucleus, and granular
   patches of rough endoplasmic reticulum with ribosomes called **Nissl
   granules**, which make the neuron's proteins. It has no centriole.
2. **Dendrites** — many short, branched, tapering processes that carry impulses
   **towards** the cyton. They also contain Nissl granules.
3. **Axon** — a single long process arising from the cone-shaped **axon hillock**
   that carries the impulse **away** from the cyton. It has no Nissl granules.
   It ends in fine branches, the **telodendria**, each tipped by a **synaptic
   knob**.

In a myelinated fibre the axon is wrapped in a fatty **myelin sheath** made by
**Schwann cells**, covered outside by the **neurilemma**. The sheath is
interrupted every millimetre or so at the **nodes of Ranvier**. The impulse
jumps from node to node — **saltatory conduction** — which is why a myelinated
fibre conducts up to a hundred times faster than a bare one.

```photo id="bio12/neuron-motor" caption="A multipolar motor neuron in a spinal-cord smear (×100). The cell body with its large nucleus gives off several branching dendrites; the small dark dots around it are the nuclei of supporting neuroglial cells. The impulse travels dendrite → cyton → axon → synaptic knob, and never the other way." width="86"
mark 0.45 0.58 "1"
mark 0.28 0.47 "2"
mark 0.70 0.81 "3"
key 1 Cell body (cyton) with its nucleus
key 2 Dendrite — branching, carries impulses towards the cell body
key 3 Nucleus of a neuroglial cell
```

```photo id="bio12/synapse" caption="An enlarged chemical synapse. Transmitter stored in synaptic vesicles is released at the active zone of the presynaptic terminal and binds receptors on the post-synaptic membrane." width="78"
```
::: memory The direction rule
**D**endrite = **D**elivers to the cell body. Axon carries **away**. At a synapse
the vesicles are always on the axon side, so transmission across a synapse is
strictly **one-way**.
:::

Neurons are named by the number of processes leaving the cyton — **unipolar**
(one process; in insect and embryonic nerve cells), **bipolar** (one axon and
one dendrite; retina, olfactory epithelium) and **multipolar** (one axon and
many dendrites; the commonest type, in the brain and spinal cord). By function
they are **sensory (afferent)**, **motor (efferent)** or **association
(interneurons)**.

The main neuroglia are **astrocytes** (anchor neurons to capillaries and help
form the blood–brain barrier), **oligodendrocytes** (make myelin inside the
brain and spinal cord), **microglia** (phagocytes of the nervous system) and
**ependymal cells** (line the brain ventricles and circulate cerebrospinal
fluid).

::: definition Synapse
A synapse is the functional junction between the synaptic knob of one neuron and
the dendrite or cyton of the next. The membranes do not touch; they are
separated by a **synaptic cleft** about 20 nm wide. The impulse crosses
chemically: it makes the knob release a **neurotransmitter** such as
acetylcholine, which diffuses across the cleft and excites the next membrane.
:::

::: example Worked example 6.4 — how long does a reflex take?
**Problem.** You step on a thorn in a Chitwan forest and pull your foot back.
The sensory path from the foot to the spinal cord is $0.90\ \text{m}$ and the
motor path back to the leg muscle is $0.80\ \text{m}$; both are myelinated
fibres conducting at $85\ \text{m s}^{-1}$. The reflex arc contains 2 synapses,
each causing a delay of $0.5\ \text{ms}$. (a) Find the total reflex time.
(b) How long would the same journey take along a non-myelinated fibre
conducting at $0.5\ \text{m s}^{-1}$?

**Solution.**

(a) Total length of nerve fibre $= 0.90 + 0.80 = 1.70\ \text{m}$.

$$ t_{\text{conduction}} = \frac{1.70\ \text{m}}{85\ \text{m s}^{-1}}
 = 0.020\ \text{s} = 20\ \text{ms} $$

Synaptic delay $= 2 \times 0.5 = 1.0\ \text{ms}$. Total reflex time

$$ t = 20 + 1 = 21\ \text{ms} = 0.021\ \text{s} $$

(b) Along a bare fibre:

$$ t = \frac{1.70\ \text{m}}{0.5\ \text{m s}^{-1}} = 3.4\ \text{s} $$

The myelin sheath makes the response about 160 times faster — quite literally
the difference between a scratch and a deep wound.
:::

::: caution Do not mix up the two sheaths
The **myelin sheath** is the fatty insulating layer produced by the Schwann
cell. The **neurilemma** is the thin outer living membrane of the Schwann cell
itself, *outside* the myelin. Non-myelinated fibres still have a neurilemma —
they simply lack myelin, and so have no nodes of Ranvier and conduct slowly.
:::

| Feature | Myelinated fibre | Non-myelinated fibre |
|---|---|---|
| Myelin sheath | present | absent |
| Nodes of Ranvier | present | absent |
| Conduction | saltatory, fast (up to about 120 m s⁻¹) | continuous, slow (about 0.5–2 m s⁻¹) |
| Found in | cranial and spinal nerves, white matter | autonomic nerves, grey matter |

## Chapter summary

- A tissue is a group of similar cells with a common origin doing one job; the
  four animal tissues are epithelial, connective, muscular and nervous.
- Epithelium: cells packed, matrix negligible, avascular, polar, on a basement
  membrane, high regeneration. Simple (squamous, cuboidal, columnar, ciliated,
  pseudostratified), compound (stratified squamous, transitional) or glandular.
- Connective tissue: few cells, abundant matrix of collagen, elastic and
  reticular fibres. Loose (areolar, adipose), dense (tendon = collagen,
  muscle→bone; ligament = elastin, bone→bone), skeletal (cartilage, bone) and
  fluid (blood, lymph).
- Cartilage: chondrocytes in lacunae in chondrin, avascular, covered by
  perichondrium. Bone: osteocytes in lacunae joined by canaliculi, matrix of
  ossein + calcium salts, organised into Haversian systems in mammals.
- Blood = 55% plasma + 45% formed elements. RBC 4.5–5.5 million per mm³,
  WBC 4000–11000 per mm³, platelets 150,000–400,000 per mm³.
- Muscle: striated (cylindrical, unbranched, many peripheral nuclei, voluntary),
  cardiac (branched, central nucleus, intercalated discs, involuntary, tireless),
  smooth (spindle, one central nucleus, no striations, involuntary).
- The sarcomere, from Z line to Z line, is the contractile unit; on contraction
  the I band and H zone shorten but the A band does not.
- A neuron has a cyton with Nissl granules, dendrites carrying impulses in, and
  one axon carrying them out. Myelin plus nodes of Ranvier give saltatory
  conduction; the synapse transmits chemically and in one direction only.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The tissue that arises from all three germ layers is <span class="marks">[1]</span>
   (a) connective (b) epithelial (c) muscular (d) nervous

2. Transitional epithelium is characteristic of the <span class="marks">[1]</span>
   (a) trachea (b) small intestine (c) urinary bladder (d) oesophagus

3. Tendons are made chiefly of <span class="marks">[1]</span>
   (a) yellow elastic fibres (b) white collagen fibres (c) reticular fibres (d) chondrin

4. Which is **absent** in cartilage? <span class="marks">[1]</span>
   (a) lacunae (b) chondrocytes (c) blood vessels (d) perichondrium

5. Intercalated discs occur in <span class="marks">[1]</span>
   (a) skeletal muscle (b) cardiac muscle (c) smooth muscle (d) all three

6. During contraction of a sarcomere, the band whose length does **not** change is the <span class="marks">[1]</span>
   (a) I band (b) H zone (c) A band (d) Z line

7. Nissl granules are absent from the <span class="marks">[1]</span>
   (a) cyton (b) dendrite (c) axon (d) nucleus

8. Heparin and histamine are secreted by the <span class="marks">[1]</span>
   (a) fibroblast (b) mast cell (c) plasma cell (d) osteocyte

::: note Answers to Group A
**1.** (b) — epidermis is ectodermal, gut lining endodermal, endothelium mesodermal.
**2.** (c) — it must stretch as the bladder fills.
**3.** (b) — which is why a tendon is inextensible.
**4.** (c) — cartilage is avascular and is fed by diffusion from the perichondrium.
**5.** (b) — they are the junctions between adjacent cardiac fibres.
**6.** (c) — the A band equals the length of the myosin filament, which does not shorten.
**7.** (c) — the axon has no Nissl granules; this distinguishes it from a dendrite.
**8.** (b) — heparin prevents clotting inside vessels, histamine causes inflammation.
:::

**Group B — Short answer questions (4 marks each)**

1. Define epithelial tissue and give four general characters of it. <span class="marks">[4]</span>

2. Distinguish between a tendon and a ligament under four heads. <span class="marks">[4]</span>

3. Draw a labelled T.S. of a Haversian system and name any four parts.
   <span class="marks">[4]</span>

4. Give four differences between cardiac muscle and smooth muscle.
   <span class="marks">[4]</span>

5. In a haemocytometer count, blood is diluted 1 : 200, and 420 red cells are
   counted in 80 small squares, each of area $\frac{1}{400}\ \text{mm}^{2}$ under
   a depth of $0.1\ \text{mm}$. Calculate the RBC count per mm³ and comment.
   <span class="marks">[4]</span>

6. Why is cartilage slow to heal while bone heals comparatively fast?
   <span class="marks">[4]</span>

::: note Answers to Group B
**2.** Tendon — white collagen fibres, straight parallel bundles, inextensible,
joins muscle to bone. Ligament — yellow elastic fibres, branching, elastic,
joins bone to bone.

**4.** Cardiac: branched fibres, one central nucleus, intercalated discs
present, found only in the heart, never fatigues. Smooth: spindle-shaped
unbranched cells, one central nucleus, no discs, no striations, found in gut,
uterus and blood vessels.

**5.** Volume over 80 small squares
$= 80 \times \frac{1}{400}\ \text{mm}^{2} \times 0.1\ \text{mm} = 0.02\ \text{mm}^{3}$.
Diluted count $= 420/0.02 = 21\,000$ per mm³. Whole blood
$= 21\,000 \times 200 = 4\,200\,000 = 4.2$ million per mm³. This is **below** the
normal range of 4.5–5.5 million, so the person is mildly anaemic.

**6.** Cartilage is avascular: its chondrocytes receive food and oxygen only by
slow diffusion through the solid matrix from the perichondrium, and they divide
slowly. Bone is richly supplied with blood through the Haversian and Volkmann's
canals, and the periosteum contains osteoblasts that can lay down new matrix
quickly, so a fracture unites in weeks.
:::

**Group C — Long answer questions (8 marks each)**

1. (a) Classify epithelial tissue with one example and one location for each
   type. <span class="marks">[5]</span>
   (b) Draw a labelled diagram of pseudostratified ciliated columnar epithelium
   and explain why it is not a stratified epithelium. <span class="marks">[3]</span>

2. (a) Describe the structure of a myelinated motor neuron with a labelled
   diagram. <span class="marks">[5]</span>
   (b) What is a synapse? Explain how an impulse crosses it and why transmission
   is one-way. <span class="marks">[3]</span>

::: note Answer outline to Group C question 2
(a) Cyton with nucleus, Nissl granules and no centriole; several branched
dendrites conducting towards the cyton; a single axon arising at the axon
hillock, covered by myelin made by Schwann cells, with neurilemma outside and
nodes of Ranvier between successive Schwann cells; ending in telodendria tipped
by synaptic knobs. Award marks for the labelled diagram.

(b) A synapse is the junction between the synaptic knob of one neuron and the
dendrite or cyton of the next, separated by a cleft of about 20 nm. The arriving
impulse opens Ca²⁺ channels in the knob; synaptic vesicles fuse with the
presynaptic membrane and release acetylcholine, which diffuses across the cleft
and binds receptors on the postsynaptic membrane, starting a new impulse. The
enzyme cholinesterase then destroys the transmitter. Transmission is one-way
because vesicles and transmitter exist only on the presynaptic side and
receptors only on the postsynaptic side.
:::
