---
subject: Zoology
grade: CEE
unit: 3
title: Animal Tissues and Histology
hours: 4
area: Evolution and Diversity
---

Animal Tissues and Histology carries **4 of the 40 Zoology questions**. The
syllabus asks for the four primary tissues — epithelial, connective, muscular
and nervous — with their **structure, location and function**, so almost every
question is "which tissue lines/supports/forms this organ" or "which cell or
fibre does this job". The marks sit in the epithelium table, the three
cartilages and bone, the blood cells with their numbers, the three kinds of
muscle with the sarcomere, and the parts of a neuron.

::: key What the paper asks from this chapter
- **Epithelia**: name and location of each type — squamous (alveoli, blood vessels), cuboidal (kidney tubules, thyroid), columnar (stomach, intestine), ciliated (oviduct, bronchioles), pseudostratified (trachea), stratified squamous (skin, oesophagus), transitional (urinary bladder).
- **Glands**: exocrine, endocrine and heterocrine; merocrine, apocrine and holocrine secretion.
- **Connective tissue** cells (fibroblast, macrophage, mast cell, plasma cell, adipocyte) and fibres (collagen, elastic, reticular); tendon versus ligament.
- **Cartilage** (hyaline, elastic, fibrocartilage) versus **bone** (ossein, hydroxyapatite, Haversian system, osteoblast/osteoclast).
- **Blood** as fluid connective tissue: plasma, RBC, the five WBCs in their percentages, platelets.
- **Skeletal, smooth and cardiac muscle**: shape, nuclei, striations, intercalated discs, control; the sarcomere bands in contraction.
- **Neuron** structure (Nissl granules, axon, myelin, nodes of Ranvier), neuron types and neuroglia.
:::

## 3.1 Epithelial, connective, muscular and nervous tissues: structure, location and function

A **tissue** is a group of similar cells, with their intercellular substance,
that has a common origin and performs a common function. **Histology** is the
study of tissues. Animals have four primary tissues.

| Tissue | Germ layer | Cells and matrix | Main job | Examples |
|---|---|---|---|---|
| **Epithelial** | all three | cells packed close, **almost no matrix**, on a basement membrane | covering, lining, protection, secretion, absorption | epidermis, lining of gut, glands |
| **Connective** | mesoderm | few cells scattered in **abundant matrix** with fibres | binding, support, transport, storage, defence | areolar tissue, tendon, cartilage, bone, blood |
| **Muscular** | mesoderm (mostly) | elongated contractile **muscle fibres** | movement, contraction | skeletal, smooth, cardiac muscle |
| **Nervous** | ectoderm | **neurons** and **neuroglia** | receive, conduct and transmit impulses; coordination | brain, spinal cord, nerves |

### Epithelial tissue

**Epithelium** is a sheet of closely packed cells with negligible
intercellular matrix, resting on a non-cellular **basement membrane**, that
covers the body surface and lines its cavities, ducts and tubes.

```photo id="bio12/squamous-epithelium" caption="(a) Simple squamous epithelium in surface view (silver-stained whole mount, ×100): thin, flat, polygonal cells fit edge to edge like paving stones, and the silver outlines each boundary." width="66"
```


- It arises from **all three germ layers** — epidermis (ectoderm), gut lining (endoderm), lining of blood vessels and kidney tubules (mesoderm).
- **Avascular**: no blood vessels enter it; nutrients diffuse from capillaries of the connective tissue below.
- Cells are polar (free apical and basal surfaces) and joined by **cell junctions**: **tight junctions** (stop leakage between cells), **adhering junctions / desmosomes** (cement neighbouring cells), **gap junctions** (cytoplasmic channels for ions and small molecules).
- High **power of regeneration**; free surfaces may bear **microvilli** (absorption), **cilia** (movement) or **stereocilia** (long immotile microvilli, as in the epididymis).
- The lining of blood vessels and the heart is called **endothelium**; of the body cavities (pleura, peritoneum, pericardium) **mesothelium**.

| Epithelium | Structure | Location | Function |
|---|---|---|---|
| **Simple squamous** (pavement) | one layer of thin, flat, polygonal cells with a central flattened nucleus | **alveoli of lungs**, walls of **blood capillaries** and vessels (endothelium), **Bowman's capsule**, thin loop of Henle, serous membranes | diffusion, filtration |
| **Simple cuboidal** | one layer of cube-shaped cells, round central nucleus | **kidney tubules** (PCT with a **brush border** of microvilli), **thyroid follicles**, ducts of glands, surface of the ovary (germinal epithelium) | secretion, absorption |
| **Simple columnar** | tall cells, oval nucleus near the base; often with microvilli and **goblet cells** | lining of **stomach**, **small intestine** (brush border), gall bladder | secretion, absorption |
| **Ciliated columnar** | columnar cells with cilia | **fallopian tubes (oviducts)**, small bronchioles, uterus, central canal of spinal cord | moves ova, mucus or fluid in one direction |
| **Pseudostratified ciliated columnar** | one layer, but cells of different heights with nuclei at different levels, so it *looks* layered; all cells touch the basement membrane; goblet cells | **trachea**, **bronchi**, nasal passages | traps dust in mucus, cilia sweep it up |
| **Stratified squamous keratinised** | many layers; only the basal (germinative) layer divides; surface cells dead, filled with **keratin** | **epidermis of skin** | waterproof, resists wear |
| **Stratified squamous non-keratinised** | many layers, surface cells living and moist | **buccal cavity**, pharynx, **oesophagus**, **vagina**, cornea | resists abrasion |
| **Stratified cuboidal** | two or more layers of cuboidal cells | ducts of **sweat glands**, salivary and mammary ducts | protection, secretion |
| **Stratified columnar** | several layers, columnar at the surface | part of the male urethra, conjunctiva, large ducts | protection |
| **Transitional** (urothelium) | 4–6 layers; large dome-shaped (umbrella) surface cells that flatten when the organ is stretched | **urinary bladder**, **ureters**, renal pelvis | stretches without tearing |

```figure caption="Types of epithelium in vertical section. Every type rests on a basement membrane (brown line). In pseudostratified epithelium every cell touches the membrane although the nuclei lie at different levels; in transitional epithelium the large surface cells flatten when the bladder fills."
import numpy as np
from matplotlib.patches import Rectangle, Ellipse, Polygon, FancyBboxPatch
fig, axes = plt.subplots(2, 3, figsize=(5.2, 3.7))
CELL, EDGE, NUC, BM = "#e7eff7", "#2c5f96", "#41638a", "#a0703a"
def base(ax):
    ax.set_xlim(0, 6); ax.set_ylim(-1.35, 3.4); ax.axis("off")
    ax.plot([0.15, 5.85], [0.45, 0.45], color=BM, lw=2.2, solid_capstyle="butt")
def cell(ax, x, y, w, h, fc=CELL):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=EDGE, lw=0.8))
def nuc(ax, x, y, w, h):
    ax.add_patch(Ellipse((x, y), w, h, fc=NUC, ec="none"))
def title(ax, a, b):
    ax.text(3.0, -0.25, a, ha="center", va="top", fontsize=6.9, color=INK)
    ax.text(3.0, -0.85, b, ha="center", va="top", fontsize=6.4, color=MUTED)
A = axes.ravel()
# (a) simple squamous
base(A[0])
for i in range(4):
    cell(A[0], 0.2 + 1.4 * i, 0.47, 1.4, 0.32)
    nuc(A[0], 0.9 + 1.4 * i, 0.70, 0.62, 0.22)
title(A[0], "simple squamous", "alveoli, capillaries")
# (b) simple cuboidal
base(A[1])
for i in range(5):
    cell(A[1], 0.25 + 1.1 * i, 0.47, 1.1, 1.1)
    nuc(A[1], 0.8 + 1.1 * i, 1.02, 0.46, 0.46)
title(A[1], "simple cuboidal", "kidney tubules, thyroid")
# (c) simple columnar with brush border
base(A[2])
for i in range(6):
    x = 0.25 + 0.92 * i
    cell(A[2], x, 0.47, 0.92, 2.2)
    nuc(A[2], x + 0.46, 1.0, 0.42, 0.62)
    for k in range(5):
        xx = x + 0.12 + 0.17 * k
        A[2].plot([xx, xx], [2.67, 2.95], color=EDGE, lw=0.7)
title(A[2], "simple columnar (brush border)", "stomach, intestine")
# (d) pseudostratified ciliated with a goblet cell
base(A[3])
xs = [0.25, 1.15, 2.05, 2.95, 3.85, 4.75]
for i, x in enumerate(xs):
    if i == 2:
        A[3].add_patch(Polygon([[x + 0.25, 0.47], [x + 0.65, 0.47], [x + 0.75, 1.5],
                                [x + 0.9, 2.67], [x, 2.67], [x + 0.15, 1.5]],
                               closed=True, fc=CELL, ec=EDGE, lw=0.8))
        A[3].add_patch(Ellipse((x + 0.45, 2.05), 0.7, 1.05, fc="#cfe3d4", ec="#2e8b57", lw=0.7))
        nuc(A[3], x + 0.45, 0.95, 0.3, 0.42)
        continue
    cell(A[3], x, 0.47, 0.9, 2.2)
    nuc(A[3], x + 0.45, [1.0, 1.75, 0, 1.35, 2.0, 1.1][i], 0.36, 0.5)
    for k in range(5):
        xx = x + 0.12 + 0.16 * k
        A[3].plot([xx, xx + 0.05], [2.67, 3.15], color=EDGE, lw=0.7)
A[3].text(2.5, 3.35, "goblet cell", ha="center", va="bottom", fontsize=6.4, color="#2e8b57")
title(A[3], "pseudostratified ciliated", "trachea, bronchi")
# (e) stratified squamous
base(A[4])
for i in range(7):
    cell(A[4], 0.25 + 0.8 * i, 0.47, 0.8, 0.75)
    nuc(A[4], 0.65 + 0.8 * i, 0.85, 0.34, 0.4)
for i in range(5):
    cell(A[4], 0.25 + 1.12 * i, 1.22, 1.12, 0.6)
    nuc(A[4], 0.81 + 1.12 * i, 1.52, 0.4, 0.3)
for i in range(4):
    cell(A[4], 0.25 + 1.4 * i, 1.82, 1.4, 0.32)
    nuc(A[4], 0.95 + 1.4 * i, 1.98, 0.5, 0.14)
for i in range(3):
    cell(A[4], 0.25 + 1.87 * i, 2.14, 1.87, 0.2, fc="#f3ecdd")
title(A[4], "stratified squamous", "skin, oesophagus")
# (f) transitional
base(A[5])
for i in range(6):
    cell(A[5], 0.25 + 0.92 * i, 0.47, 0.92, 0.7)
    nuc(A[5], 0.71 + 0.92 * i, 0.82, 0.36, 0.36)
for i in range(4):
    cell(A[5], 0.25 + 1.375 * i, 1.17, 1.375, 0.75)
    nuc(A[5], 0.94 + 1.375 * i, 1.55, 0.42, 0.36)
for i in range(3):
    x0 = 0.25 + 1.833 * i
    th = np.linspace(0, np.pi, 40)
    xsd = x0 + 0.9165 + 0.9165 * np.cos(th)
    ysd = 1.92 + 0.62 * np.sin(th)
    A[5].add_patch(Polygon(np.c_[xsd, ysd], closed=True, fc=CELL, ec=EDGE, lw=0.8))
    nuc(A[5], x0 + 0.92, 2.2, 0.44, 0.34)
title(A[5], "transitional", "urinary bladder, ureter")
fig.subplots_adjust(wspace=0.08, hspace=0.30, left=0.01, right=0.99, top=0.98, bottom=0.03)
```

**Glandular epithelium.** Epithelial cells specialised for secretion form
**glands**. A **unicellular gland** is the mucus-secreting **goblet cell** of the
intestine and respiratory tract. Multicellular glands are classified three ways.

| Basis | Type | Example |
|---|---|---|
| Where the secretion goes | **exocrine** — through a duct | salivary, sweat, sebaceous, gastric, mammary glands |
| | **endocrine** — ductless, into the blood (hormones) | thyroid, pituitary, adrenal |
| | **heterocrine (mixed)** — both | **pancreas** (enzymes + insulin), gonads |
| Mode of secretion | **merocrine (eccrine)** — secretion leaves by exocytosis, cell intact | salivary glands, pancreas, most sweat glands |
| | **apocrine** — the apical part of the cell pinches off with the secretion | **mammary glands**, sweat glands of the armpit |
| | **holocrine** — the whole cell breaks down to form the secretion | **sebaceous glands** |
| Shape | simple tubular / coiled tubular / branched tubular | intestinal crypts / **sweat glands** / gastric glands |
| | simple branched alveolar | **sebaceous glands** |
| | compound tubulo-alveolar | salivary glands, pancreas, mammary glands |

### Connective tissue

Connective tissues are the most abundant and widespread tissues. They arise from
the **mesoderm**, have **few cells in a large amount of matrix**, are usually
**vascular** (cartilage is the exception) and bind, support, protect, store and
transport.

```photo id="bio12/areolar" caption="(a) Areolar (loose) connective tissue, spread preparation (×400): a loose meshwork of fibres with scattered cells in a soft ground substance." width="66"
mark 0.50 0.50 "1"
mark 0.30 0.74 "2"
mark 0.60 0.28 "3"
key 1 Collagen fibres — thick, pink, wavy bundles
key 2 Elastic fibres — thin, dark, branching and straight
key 3 Fibroblast nucleus
```


```photo id="bio12/columnar-epithelium" caption="(c) Simple columnar epithelium with goblet cells (×400): tall cells with basal oval nuclei line the lumen; the pale rounded cells between them are mucus-filled goblet cells." width="66"
```


**The fibres**

| Fibre | Protein | Appearance | Property | Where |
|---|---|---|---|---|
| **White (collagen)** | **collagen** — the commonest protein of the body | wavy unbranched bundles | great tensile strength, little stretch; boiled → gelatin | tendons, dermis, bone, cartilage |
| **Yellow (elastic)** | **elastin** | single, branched fibres | stretch and recoil | ligaments, walls of arteries, lungs, pinna |
| **Reticular** | **reticulin** (a fine collagen) | delicate branched network | supporting framework (stroma) | lymph nodes, spleen, liver, bone marrow |

**The cells of loose connective tissue**

| Cell | Job |
|---|---|
| **Fibroblast** | the commonest cell; secretes fibres and matrix |
| **Macrophage (histiocyte)** | phagocytosis — engulfs microbes and debris |
| **Mast cell** | secretes **heparin** (anticoagulant), **histamine** (dilates vessels; allergy) and serotonin |
| **Plasma cell** | derived from B lymphocytes; secretes **antibodies** |
| **Adipocyte (fat cell)** | stores fat in one large droplet; nucleus pushed to the edge (signet-ring cell) |
| Melanocyte, lymphocyte | pigment; immunity |

**Classification of connective tissue**

| Group | Tissue | Structure | Location |
|---|---|---|---|
| **Loose (proper)** | **Areolar** | loose mesh of collagen and elastic fibres, all the cell types, semi-fluid matrix | under the skin, round blood vessels, nerves and muscles, in mesenteries — "packing tissue" |
| | **Adipose** | fat cells packed together; **white fat** (one droplet) and **brown fat** (many droplets, many mitochondria — makes heat) | subcutaneous layer, round kidneys, heart, mesentery, yellow bone marrow; brown fat in newborns and hibernating mammals |
| | **Reticular** | reticular fibres with reticular cells | lymph nodes, spleen, bone marrow |
| **Dense** | **Dense regular** | fibres in parallel bundles | **tendons** (white collagen; join **muscle to bone**, inelastic); **ligaments** (with yellow elastic fibres; join **bone to bone**, slightly elastic) |
| | **Dense irregular** | collagen fibres in all directions | **dermis** of skin, capsules of organs, periosteum, perichondrium |
| **Supporting (skeletal)** | **Cartilage** | **chondrocytes** in **lacunae** in a firm matrix of **chondrin** (chondroitin sulphate); covered by **perichondrium**; **avascular** | see the cartilage table |
| | **Bone** | **osteocytes** in lacunae in a hard matrix of **ossein** (collagen) and calcium salts | skeleton |
| **Fluid** | **Blood** | cells in fluid **plasma** | blood vessels |
| | **Lymph** | plasma-like fluid with lymphocytes, no RBCs or platelets | lymph vessels |

**Cartilage**

| Type | Matrix | Location |
|---|---|---|
| **Hyaline** — the commonest, glassy, bluish-white | homogeneous; fine collagen fibres invisible | **articular ends of long bones**, **costal cartilages** of ribs, rings of the **trachea** and bronchi, **larynx**, nasal septum; the embryonic skeleton |
| **Elastic** (yellow) | many **yellow elastic fibres** | **pinna (external ear)**, **epiglottis**, Eustachian tube |
| **White fibrocartilage** | dense bundles of **collagen fibres** — the strongest | **intervertebral discs**, **pubic symphysis**, menisci of the knee |
| Calcified | hyaline cartilage hardened by calcium salts | suprascapula of the frog; heads of the humerus and femur of the frog |

**Bone** is the hardest connective tissue. Its matrix is about **two-thirds
inorganic** — mainly **calcium phosphate as hydroxyapatite** with some calcium
carbonate — and **one-third organic**, chiefly the protein **ossein**. Acid
dissolves the salts and leaves a flexible bone; burning removes the ossein and
leaves a brittle one.

- **Osteoblasts** form bone; when trapped in their own matrix they become **osteocytes**, which sit in **lacunae** and reach each other through fine **canaliculi**. **Osteoclasts** resorb bone.
- **Compact bone** (shafts of long bones) of mammals is built of **Haversian systems (osteons)**: a central **Haversian canal** carrying blood vessels and nerves, surrounded by concentric **lamellae** of matrix with lacunae between them. Transverse **Volkmann's canals** link neighbouring Haversian canals. Outside is the **periosteum**, inside the **endosteum**.
- **Spongy (cancellous) bone** (ends of long bones, flat bones) is a lattice of **trabeculae** with **red bone marrow** (makes blood cells) in the spaces; the marrow cavity of the shaft holds **yellow (fatty) marrow** in adults.

```photo id="bio12/compact-bone" caption="T.S. of compact bone (ground section, ×100), labelled: concentric lamellae round each central (Haversian) canal form an osteon; each osteocyte sits in a lacuna and reaches the canal through canaliculi." width="64"
crop 0.46 0.0 1.0 1.0
```

| Feature | Cartilage | Bone |
|---|---|---|
| Matrix | **chondrin**, soft and flexible | **ossein + calcium salts**, hard and rigid |
| Blood vessels | **absent** (nourished by diffusion from the perichondrium) | present (Haversian and Volkmann's canals) |
| Cells | chondrocytes, 1–4 per lacuna | osteocytes, 1 per lacuna |
| Canaliculi | absent | present |
| Growth | from inside and from the surface | from the surface (and at growth plates) |
| Marrow | absent | present |

**Blood** is a **fluid connective tissue**: about **55 % plasma** and **45 %
formed elements**. Plasma is 90–92 % water and 6–8 % proteins — **albumin**
(osmotic pressure), **globulins** (antibodies, transport) and **fibrinogen**
(clotting) — with glucose, amino acids, salts, hormones and urea.

```photo id="bio12/adipose" caption="(b) Adipose tissue (×100). The fat droplet fills each cell and pushes the cytoplasm and nucleus into a thin rim at the edge, so the cells look empty in a stained section." width="66"
mark 0.13 0.22 "1"
mark 0.60 0.55 "2"
key 1 Nucleus pushed to one side by the fat droplet
key 2 Adipocyte — the droplet-filled space
```


| Element | Number per mm³ | Structure | Life span | Job |
|---|---|---|---|---|
| **RBC (erythrocyte)** | **5–5.5 million** (men), about 4.5 million (women) | **biconcave, no nucleus** in mammals, about 7.5 μm; full of **haemoglobin** (12–16 g per 100 mL blood); made in red bone marrow | **120 days**; destroyed in the **spleen** (the "graveyard of RBCs") and liver | carry O₂ and some CO₂ |
| **WBC (leucocyte)** | **6000–8000** | nucleated, colourless, amoeboid; can squeeze out of capillaries (**diapedesis**) | days | defence |
| **Platelets (thrombocytes)** | **1.5–3.5 lakh** | non-nucleated **fragments of megakaryocytes** of bone marrow | about a week | **blood clotting** |

| WBC | Type | % of WBCs | Nucleus | Job |
|---|---|---|---|---|
| **Neutrophil** | granulocyte | **60–65** (most abundant) | **3–5 lobes** | **phagocytosis** of bacteria; first to arrive; pus is dead neutrophils |
| **Eosinophil (acidophil)** | granulocyte | **2–3** | **bilobed** | allergy and **parasitic worm** infections (rises in both) |
| **Basophil** | granulocyte | **0.5–1** (fewest) | S-shaped or lobed | releases **histamine, heparin** and serotonin (inflammation) |
| **Lymphocyte** | agranulocyte | **20–25** | large round nucleus filling the cell | **immunity**: B cells (antibodies), T cells |
| **Monocyte** | agranulocyte | **6–8** | **kidney- (bean-) shaped**; the **largest WBC** | phagocytosis; becomes a **macrophage** in tissues |

::: memory WBCs in falling order of number
**"Never Let Monkeys Eat Bananas"** — Neutrophils (60–65 %) > Lymphocytes
(20–25 %) > Monocytes (6–8 %) > Eosinophils (2–3 %) > Basophils (0.5–1 %).
:::

### Muscular tissue

Muscle is made of long, contractile **muscle fibres** (cells) whose cytoplasm
(**sarcoplasm**) is packed with **myofibrils** of the proteins **actin** (thin
filaments) and **myosin** (thick filaments). The cell membrane is the
**sarcolemma**; the endoplasmic reticulum, which stores Ca²⁺, is the
**sarcoplasmic reticulum**. Muscles are mesodermal, except the muscles of the
**iris** and the myoepithelial cells of glands, which are ectodermal.

```photo id="bio12/skeletal-muscle" caption="(a) Skeletal muscle in longitudinal section (×400): long, unbranched, cross-striated fibres, each with many nuclei at the edge." width="66"
mark 0.10 0.40 "1"
mark 0.25 0.55 "2"
key 1 Cross-striations (alternating A and I bands)
key 2 One of the many peripheral nuclei of a single fibre
```


| Feature | **Skeletal** (striated, voluntary) | **Smooth** (unstriated, involuntary, visceral) | **Cardiac** |
|---|---|---|---|
| Shape | long, **cylindrical, unbranched** | **spindle-shaped**, unbranched | cylindrical, **branched** |
| Nuclei | **many**, at the **periphery** (a syncytium) | **one**, central | one (sometimes two), central |
| Striations | prominent light and dark bands | **absent** | present, fainter |
| Intercalated discs | absent | absent | **present** (gap junctions and desmosomes) |
| Control | **voluntary** (somatic nerves) | involuntary (autonomic) | involuntary; **myogenic** — beats on its own |
| Contraction | fast, powerful, **fatigues** quickly | slow, sustained, **no fatigue** | rhythmic, **never fatigues** |
| Location | limbs, body wall, **tongue**, pharynx, **diaphragm**, attached to bones by tendons | walls of **alimentary canal**, blood vessels, urinary bladder, uterus, **iris**, ciliary body, **arrector pili** | **wall of the heart** (myocardium) |

```figure caption="Above: the three kinds of muscle fibre. Below: one sarcomere, the unit of contraction, from one Z line to the next. In contraction the thin actin filaments slide in over the myosin, so the I band and H zone shorten while the A band keeps its length."
import numpy as np
from matplotlib.patches import Rectangle, Ellipse, Polygon
fig = plt.figure(figsize=(5.2, 3.5))
gs = fig.add_gridspec(2, 3, height_ratios=[1.0, 0.85], hspace=0.12, wspace=0.10,
                      left=0.02, right=0.98, top=0.99, bottom=0.02)
FIB, EDGE, NUC = "#f4dcd6", "#a2453e", "#41638a"
# skeletal
ax = fig.add_subplot(gs[0, 0]); ax.set_xlim(0, 6); ax.set_ylim(-1.3, 3.2); ax.axis("off")
for y0 in (0.3, 1.75):
    ax.add_patch(Rectangle((0.2, y0), 5.6, 1.1, fc=FIB, ec=EDGE, lw=0.8))
    for x in np.arange(0.35, 5.8, 0.3):
        ax.add_patch(Rectangle((x, y0 + 0.02), 0.13, 1.06, fc="#c98b80", ec="none"))
    for x in (1.0, 2.9, 4.7):
        ax.add_patch(Ellipse((x, y0 + 0.98), 0.55, 0.16, fc=NUC, ec="none", zorder=3))
    ax.add_patch(Ellipse((2.0, y0 + 0.12), 0.55, 0.16, fc=NUC, ec="none", zorder=3))
ax.text(3, -0.1, "skeletal", ha="center", va="top", fontsize=7.0, color=INK)
ax.text(3, -0.7, "striated, many peripheral nuclei", ha="center", va="top", fontsize=6.4, color=MUTED)
# smooth
ax = fig.add_subplot(gs[0, 1]); ax.set_xlim(0, 6); ax.set_ylim(-1.3, 3.2); ax.axis("off")
for (x0, y0) in [(0.2, 0.5), (1.6, 1.25), (0.9, 2.0), (2.6, 0.55), (3.1, 2.05)]:
    ax.add_patch(Polygon([[x0, y0], [x0 + 1.4, y0 + 0.28], [x0 + 2.8, y0],
                          [x0 + 1.4, y0 - 0.28]], closed=True, fc=FIB, ec=EDGE, lw=0.8))
    ax.add_patch(Ellipse((x0 + 1.4, y0), 0.7, 0.14, fc=NUC, ec="none"))
ax.text(3, -0.1, "smooth", ha="center", va="top", fontsize=7.0, color=INK)
ax.text(3, -0.7, "spindle cells, no striations", ha="center", va="top", fontsize=6.4, color=MUTED)
# cardiac
ax = fig.add_subplot(gs[0, 2]); ax.set_xlim(0, 6); ax.set_ylim(-1.3, 3.2); ax.axis("off")
ax.add_patch(Rectangle((0.2, 0.3), 5.6, 0.8, fc=FIB, ec=EDGE, lw=0.8))
ax.add_patch(Rectangle((0.2, 1.95), 5.6, 0.8, fc=FIB, ec=EDGE, lw=0.8))
ax.add_patch(Polygon([[2.3, 1.1], [2.95, 1.1], [3.85, 1.95], [3.2, 1.95]], closed=True,
                     fc=FIB, ec=EDGE, lw=0.8))
for y0 in (0.3, 1.95):
    for x in np.arange(0.4, 5.8, 0.36):
        ax.plot([x, x], [y0 + 0.05, y0 + 0.75], color="#d7a79e", lw=0.8)
for x, y0 in [(1.7, 0.3), (4.4, 0.3), (1.3, 1.95), (4.9, 1.95)]:
    ax.plot([x, x], [y0, y0 + 0.8], color=INK, lw=2.2)
for x, y in [(0.95, 0.7), (3.1, 0.7), (5.15, 0.7), (2.4, 2.35), (4.0, 2.35)]:
    ax.add_patch(Ellipse((x, y), 0.42, 0.26, fc=NUC, ec="none", zorder=3))
ax.text(3, -0.1, "cardiac", ha="center", va="top", fontsize=7.0, color=INK)
ax.text(3, -0.7, "branched; intercalated discs", ha="center", va="top", fontsize=6.4, color=MUTED)
# sarcomere
ax = fig.add_subplot(gs[1, :]); ax.set_xlim(-0.6, 10.6); ax.set_ylim(-1.95, 1.85); ax.axis("off")
for x in (0, 10):
    ax.plot([x, x], [-0.95, 0.95], color=INK, lw=2.4)
for y in (-0.6, -0.2, 0.2, 0.6):
    ax.plot([0, 4.1], [y, y], color=SERIES[0], lw=1.0)
    ax.plot([5.9, 10], [y, y], color=SERIES[0], lw=1.0)
for y in (-0.4, 0.0, 0.4):
    ax.plot([2.6, 7.4], [y, y], color=SERIES[1], lw=3.4, solid_capstyle="butt")
ax.plot([5, 5], [-0.75, 0.75], color=MUTED, lw=1.0, ls=(0, (2, 1.5)))
def brace(x0, x1, y, text, up=True):
    d = 0.18 if up else -0.18
    ax.plot([x0, x0, x1, x1], [y - d, y, y, y - d], color=MUTED, lw=0.8)
    ax.text((x0 + x1) / 2, y + (0.12 if up else -0.12), text, ha="center",
            va="bottom" if up else "top", fontsize=6.8, color=INK)
brace(2.6, 7.4, 1.25, "A band (dark) = thick myosin filaments (red) — length constant")
brace(4.1, 5.9, -1.2, "H zone", up=False)
brace(0, 2.6, -1.2, "half I band", up=False)
brace(7.4, 10, -1.2, "half I band", up=False)
ax.text(0, 1.05, "Z line", ha="center", va="bottom", fontsize=6.8, color=INK)
ax.text(10, 1.05, "Z line", ha="center", va="bottom", fontsize=6.8, color=INK)
ax.text(5, -0.83, "M line", ha="center", va="top", fontsize=6.4, color=MUTED)
ax.text(1.3, 0.75, "actin (thin)", ha="center", va="bottom", fontsize=6.6, color=SERIES[0])
ax.text(8.75, 0.75, "actin (thin)", ha="center", va="bottom", fontsize=6.6, color=SERIES[0])
```

**The sarcomere** is the functional unit of a myofibril — the segment between
two **Z lines** (Krause's membranes).

| Band | Contains | Name | In contraction |
|---|---|---|---|
| **A band** | myosin (with overlapping actin at its ends) | anisotropic, **dark** | **length unchanged** |
| **I band** | actin only | isotropic, **light**; bisected by the Z line | **shortens** |
| **H zone** | myosin only, centre of the A band | Hensen's zone; bisected by the **M line** | **shortens / disappears** |
| Sarcomere | Z line to Z line (about 2–3 μm at rest) | — | **shortens** |

**Sliding filament theory (Huxley and Hanson, 1954).** A nerve impulse
releases **Ca²⁺** from the sarcoplasmic reticulum; Ca²⁺ binds **troponin**, which
shifts **tropomyosin** off the binding sites on actin; the **myosin heads**
(ATPase) form **cross-bridges**, swing and pull the actin towards the M line.
**ATP** is needed to detach each cross-bridge — after death ATP runs out and
the muscles lock (**rigor mortis**). The filaments themselves do not shorten.

```photo id="bio12/cardiac-discs2" caption="(b) Cardiac muscle (iron haematoxylin, ×400): short, striated, branching fibres joined end to end — each with one central nucleus — form a continuous network." width="66"
```


| Red (slow, type I) fibres | White (fast, type II) fibres |
|---|---|
| much **myoglobin**, many mitochondria, rich blood supply | little myoglobin, few mitochondria |
| aerobic, slow, sustained contraction, resist fatigue | anaerobic (lactic acid), fast, brief, fatigue quickly |
| back muscles, flight muscles of birds | eye muscles, breast muscles of the domestic fowl |

### Nervous tissue

Nervous tissue is **ectodermal** and consists of **neurons**, the structural and
functional units that conduct impulses, and **neuroglia**, which support them.

```photo id="bio12/neuron-motor" caption="A multipolar motor neuron in a spinal-cord smear (×100). The cell body with its large nucleus gives off several branching dendrites; the small dark dots around it are the nuclei of supporting neuroglial cells. The impulse travels dendrite → cyton → axon → synaptic knob, and never the other way." width="86"
mark 0.45 0.58 "1"
mark 0.28 0.47 "2"
mark 0.70 0.81 "3"
key 1 Cell body (cyton) with its nucleus
key 2 Dendrite — branching, carries impulses towards the cell body
key 3 Nucleus of a neuroglial cell
```


**The neuron**

- **Cyton (cell body, perikaryon)** — a large nucleus with a prominent nucleolus; cytoplasm with **Nissl granules** (clumps of **rough ER with ribosomes**: protein synthesis) and **neurofibrils**. Mature neurons have **no functional centrioles** and do not divide.
- **Dendrites** — short, branched processes that carry impulses **towards** the cyton; they contain Nissl granules.
- **Axon** — usually one long process carrying impulses **away from** the cyton; it arises from the **axon hillock** (no Nissl granules), and ends in branches with **synaptic knobs** full of neurotransmitter vesicles.
- **Myelin sheath** — a fatty (lipoprotein) wrapping formed by **Schwann cells** in the PNS and **oligodendrocytes** in the CNS; the outer sheath of the Schwann cell is the **neurilemma**. Gaps in the myelin are the **nodes of Ranvier**, where the impulse jumps (**saltatory conduction**, up to about 120 m s⁻¹).

```figure caption="A myelinated motor neuron. Dendrites bring impulses to the cyton; the axon carries them away to the synaptic knobs. Myelin formed by Schwann cells is interrupted at the nodes of Ranvier, where the impulse jumps."
import numpy as np
from matplotlib.patches import Circle, Polygon, FancyBboxPatch, Ellipse
fig, ax = plt.subplots(figsize=(5.2, 2.6))
ax.set_xlim(-0.4, 13.2); ax.set_ylim(-2.6, 3.0); ax.set_aspect("equal"); ax.axis("off")
BODY, EDGE = "#f2e3c4", "#9a7330"
th = np.linspace(0, 2 * np.pi, 9)[:-1]
pts = [[1.6 + 1.05 * np.cos(t) * (1 + 0.12 * (k % 2)), 0.2 + 0.95 * np.sin(t) * (1 + 0.12 * (k % 2))]
       for k, t in enumerate(th)]
ax.add_patch(Polygon(pts, closed=True, fc=BODY, ec=EDGE, lw=1.0, zorder=3))
for t in th:
    x0, y0 = 1.6 + 1.0 * np.cos(t), 0.2 + 0.9 * np.sin(t)
    if abs(np.cos(t)) > 0.95 and np.cos(t) > 0:
        continue
    x1, y1 = 1.6 + 1.9 * np.cos(t), 0.2 + 1.8 * np.sin(t)
    ax.plot([x0, x1], [y0, y1], color=EDGE, lw=1.2, zorder=2)
    for s in (-0.45, 0.45):
        ax.plot([x1, x1 + 0.55 * np.cos(t + s)], [y1, y1 + 0.55 * np.sin(t + s)],
                color=EDGE, lw=0.8, zorder=2)
ax.add_patch(Circle((1.5, 0.2), 0.38, fc="#cfe0ee", ec=SERIES[0], lw=0.9, zorder=4))
ax.add_patch(Circle((1.5, 0.2), 0.11, fc=SERIES[0], ec="none", zorder=5))
rng = np.random.default_rng(4)
for _ in range(22):
    r, a = 0.5 + 0.35 * rng.random(), 2 * np.pi * rng.random()
    ax.plot(1.6 + r * np.cos(a), 0.2 + r * 0.9 * np.sin(a), "o", ms=1.6, color="#6b4f2a", zorder=4)
ax.add_patch(Polygon([[2.62, 0.45], [3.2, 0.12], [3.2, 0.28], [2.62, -0.05]], closed=True,
                     fc=BODY, ec=EDGE, lw=0.8, zorder=3))
ax.plot([3.2, 11.0], [0.2, 0.2], color=EDGE, lw=1.4, zorder=2)
for x in np.arange(3.6, 10.6, 1.45):
    ax.add_patch(FancyBboxPatch((x, -0.05), 1.15, 0.5, boxstyle="round,pad=0,rounding_size=0.22",
                                fc="#e7eff7", ec=SERIES[0], lw=0.9, zorder=3))
    ax.add_patch(Ellipse((x + 0.58, 0.48), 0.32, 0.13, fc=SERIES[0], ec="none", zorder=4))
for a in (-0.6, -0.2, 0.2, 0.6):
    x1, y1 = 11.0 + 0.9 * np.cos(a), 0.2 + 0.9 * np.sin(a)
    ax.plot([11.0, x1], [0.2, y1], color=EDGE, lw=1.0)
    ax.add_patch(Circle((x1 + 0.1 * np.cos(a), y1 + 0.1 * np.sin(a)), 0.13, fc=EDGE, ec="none"))
fs = 6.8
def lab(t, xy, xyt, ha="center"):
    ax.annotate(t, xy=xy, xytext=xyt, fontsize=fs, color=INK, ha=ha, va="center",
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7))
lab("dendrites", (0.15, 1.55), (0.3, 2.65))
lab("cyton with\nNissl granules", (2.05, 0.75), (3.1, 2.3))
lab("nucleus", (1.45, 0.05), (1.0, -2.05))
lab("axon hillock", (2.95, 0.15), (3.0, -1.55))
lab("Schwann cell\n(myelin sheath)", (5.65, 0.45), (5.8, 2.3))
lab("node of Ranvier", (6.42, 0.2), (7.0, -1.55))
lab("Schwann cell\nnucleus", (8.48, 0.53), (9.0, 2.3))
lab("synaptic knobs", (11.85, -0.3), (11.6, -1.55))
ax.annotate("", xy=(10.4, -0.75), xytext=(4.0, -0.75),
            arrowprops=dict(arrowstyle="-|>", color=SERIES[1], lw=1.1))
ax.text(5.2, -1.0, "impulse", fontsize=6.6, color=SERIES[1], ha="center", va="top")
```

| Neuron type | Processes | Where |
|---|---|---|
| **Unipolar** | one | early embryo; invertebrates |
| **Pseudounipolar** | one process that splits into two | **sensory neurons of the dorsal root ganglia** |
| **Bipolar** | one axon + one dendrite | **retina**, olfactory epithelium, inner ear |
| **Multipolar** | one axon + many dendrites (the commonest) | **motor neurons**, brain and spinal cord |

By function neurons are **sensory (afferent)**, **motor (efferent)** or
**interneurons (association neurons)**. **Myelinated** fibres form the **white
matter** and the cranial and spinal nerves; **non-myelinated** fibres occur in
the **grey matter** and the autonomic nervous system. A **nerve** is a bundle of
nerve fibres wrapped in connective tissue (endoneurium, perineurium,
epineurium).

```photo id="bio12/smooth-muscle" caption="(c) Smooth muscle (×400): spindle-shaped, unstriated cells, each with a single central nucleus, lie in overlapping bundles." width="66"
```


**Neuroglia** — non-conducting supporting cells that make up about half the
volume of nervous tissue and, unlike neurons, can still divide.

| Glial cell | Job |
|---|---|
| **Astrocytes** | star-shaped; support neurons, form the **blood–brain barrier**, regulate ions |
| **Oligodendrocytes** | form **myelin in the CNS** |
| **Schwann cells** | form **myelin in the PNS** and the neurilemma |
| **Microglia** | **phagocytic** scavengers of the CNS (of mesodermal origin) |
| **Ependymal cells** | line the brain ventricles and central canal; help make **CSF** |

::: caution Six traps from this chapter
1. The **trachea** is lined by **pseudostratified** ciliated columnar epithelium, not stratified.
2. The **oesophagus** and **vagina** have **non-keratinised** stratified squamous epithelium; only the skin is keratinised.
3. **Tendon** = muscle to bone (white, collagen, inelastic); **ligament** = bone to bone (yellow, elastic).
4. **Pinna and epiglottis** are **elastic** cartilage; **intervertebral discs** are **fibrocartilage**; the ends of long bones are **hyaline**.
5. In contraction the **A band does not change**; the I band and H zone shorten.
6. **Monocytes** are the largest WBCs, **neutrophils** the most numerous, **basophils** the fewest; **eosinophils** rise in allergy and worm infection.
:::

::: tip Answering "which tissue" questions
Decide first whether the organ needs to **diffuse** (squamous), **secrete or
absorb** (cuboidal/columnar), **move something along** (ciliated), **resist wear**
(stratified) or **stretch** (transitional). The location follows from the job.
:::

::: example Matching epithelial linings to physiological roles
**Problem.** Which specific epithelium lines (a) Bowman's capsule and pulmonary alveoli, (b) the proximal convoluted tubule (PCT) of the nephron, (c) the fallopian tube and bronchioles, and (d) the urinary bladder?

**Solution.** (a) **Simple squamous** (thin diffusion barrier); (b) **brush-bordered simple cuboidal** (microvilli maximise reabsorption); (c) **ciliated columnar/cuboidal** (propels ovum or mucus); (d) **transitional epithelium / urothelium** (stretches without tearing).
:::

::: example Sarcomere band changes during skeletal-muscle contraction
**Problem.** When a skeletal muscle fibre contracts under the sliding-filament mechanism, state what happens to the length of (a) the A-band, (b) the I-band, (c) the H-zone, and (d) the sarcomere (Z-to-Z distance).

**Solution.** Thick (myosin) and thin (actin) filaments do not shorten; actin slides into the A-band. Therefore **(a) the A-band stays constant**, while **(b) the I-band, (c) the H-zone, and (d) the sarcomere all shorten**.
:::

::: example Distinguishing compact bone, hyaline cartilage and tendon
**Problem.** Histological slide X shows concentric lamellae around Haversian canals connected by Volkmann's canals; slide Y shows chondrocytes in fluid-filled lacunae (2–4 per capsule) in an avascular basophilic matrix without Haversian systems. Identify X and Y.

**Solution.** Haversian systems (osteons) are the hallmark of **mammalian compact bone** (X); avascular matrix with chondrocyte cell nests (isogenous groups) lacking Haversian canals is **hyaline cartilage** (Y).
:::

## Formula and fact sheet

| Item | Value or name |
|---|---|
| Basement membrane, no matrix, avascular | epithelium |
| Endothelium / mesothelium | lining of blood vessels / of body cavities |
| Brush border | PCT of kidney (cuboidal), small intestine (columnar) |
| Stereocilia | epididymis, vas deferens |
| Goblet cell | unicellular mucous gland |
| Heterocrine gland | pancreas, gonads |
| Holocrine / apocrine / merocrine | sebaceous / mammary / salivary, pancreas |
| Commonest cell of areolar tissue | fibroblast |
| Heparin and histamine | mast cells (and basophils) |
| Antibodies | plasma cells (from B lymphocytes) |
| Brown fat | thermogenesis — newborns, hibernating animals |
| Collagen / elastin / reticulin | white / yellow / reticular fibres |
| Tendon / ligament | muscle to bone / bone to bone |
| Cartilage matrix / bone matrix protein | chondrin / ossein |
| Bone salt | calcium phosphate as hydroxyapatite (about 2/3 of the matrix) |
| Bone-forming / bone-resorbing cells | osteoblasts / osteoclasts |
| Haversian and Volkmann's canals | compact bone of mammals |
| Blood | 55 % plasma, 45 % cells; plasma 90–92 % water, 6–8 % protein |
| RBC | 5–5.5 million/mm³; biconcave, no nucleus; 120 days; spleen = graveyard |
| WBC | 6000–8000/mm³ — N 60–65, L 20–25, M 6–8, E 2–3, B 0.5–1 % |
| Platelets | 1.5–3.5 lakh/mm³; megakaryocyte fragments; clotting |
| Haemoglobin | 12–16 g per 100 mL |
| Skeletal muscle | striated, voluntary, multinucleate, unbranched |
| Smooth muscle | unstriated, involuntary, uninucleate, spindle-shaped |
| Cardiac muscle | striated, involuntary, branched, intercalated discs, myogenic |
| Sarcomere | Z to Z; A band constant; I band and H zone shorten |
| Ca²⁺ store / Ca²⁺ receptor | sarcoplasmic reticulum / troponin |
| Nissl granules | rough ER + ribosomes in cyton and dendrites; absent from the axon hillock |
| Myelin | Schwann cells (PNS), oligodendrocytes (CNS) |
| Saltatory conduction | nodes of Ranvier |
| Bipolar / pseudounipolar / multipolar | retina / dorsal root ganglion / motor neurons |
| Blood–brain barrier / phagocytic glia | astrocytes / microglia |

## Chapter summary

- A tissue is a group of similar cells with a common origin and function; the four primary tissues are epithelial, connective, muscular and nervous.
- **Epithelium** rests on a basement membrane, has almost no matrix, is avascular and arises from all three germ layers; it is named by layers and cell shape — squamous (alveoli, capillaries), cuboidal (kidney tubules, thyroid), columnar (stomach, intestine), ciliated (oviduct), pseudostratified (trachea), stratified squamous (skin, oesophagus), transitional (urinary bladder).
- Glands are exocrine, endocrine or heterocrine (pancreas), and secrete in merocrine (salivary), apocrine (mammary) or holocrine (sebaceous) fashion.
- **Connective tissue** has few cells (fibroblasts, macrophages, mast cells, plasma cells, fat cells) in abundant matrix with collagen, elastic and reticular fibres: areolar, adipose, tendon, ligament, cartilage, bone, blood and lymph.
- **Cartilage** is avascular with chondrin matrix — hyaline (joints, trachea), elastic (pinna, epiglottis), fibrocartilage (intervertebral discs); **bone** has ossein and hydroxyapatite, osteocytes in lacunae and Haversian systems.
- **Blood**: 55 % plasma; RBCs (5 million/mm³, 120 days, no nucleus), WBCs (6000–8000/mm³; neutrophils most, basophils fewest, monocytes largest) and platelets (clotting).
- **Muscle**: skeletal (striated, voluntary, multinucleate), smooth (spindle, involuntary) and cardiac (branched, intercalated discs, myogenic); in contraction actin slides over myosin, the A band stays constant and the I band and H zone shorten.
- **Nervous tissue**: neurons (cyton with Nissl granules, dendrites, axon, myelin from Schwann cells or oligodendrocytes, nodes of Ranvier) and neuroglia (astrocytes, oligodendrocytes, Schwann cells, microglia, ependymal cells).

## Practice questions

**Set A — Recall (25 questions)**

1. The inner lining of blood vessels (endothelium) is made of
   (a) simple cuboidal epithelium (b) simple columnar epithelium (c) simple squamous epithelium (d) transitional epithelium
2. The urinary bladder is lined by
   (a) transitional epithelium (b) keratinised stratified squamous epithelium (c) simple columnar epithelium (d) pseudostratified epithelium
3. The trachea is lined by
   (a) simple squamous epithelium (b) stratified squamous epithelium (c) simple cuboidal epithelium (d) pseudostratified ciliated columnar epithelium
4. Cuboidal epithelium with a brush border of microvilli lines the
   (a) trachea (b) proximal convoluted tubule (c) urinary bladder (d) epidermis
5. Sebaceous glands secrete by the
   (a) merocrine mode (b) apocrine mode (c) holocrine mode (d) endocrine mode
6. Mammary glands are an example of
   (a) apocrine glands (b) holocrine glands (c) endocrine glands (d) unicellular glands
7. The most abundant cell of areolar connective tissue is the
   (a) mast cell (b) macrophage (c) plasma cell (d) fibroblast
8. Heparin and histamine are secreted in connective tissue by
   (a) fibroblasts (b) mast cells (c) plasma cells (d) adipocytes
9. A tendon connects
   (a) muscle to bone (b) bone to bone (c) muscle to muscle (d) bone to cartilage
10. The pinna and the epiglottis are supported by
   (a) hyaline cartilage (b) white fibrocartilage (c) elastic cartilage (d) calcified cartilage
11. The intervertebral discs are made of
   (a) hyaline cartilage (b) white fibrocartilage (c) elastic cartilage (d) spongy bone
12. Haversian canals are found in
   (a) hyaline cartilage (b) elastic cartilage (c) red bone marrow (d) compact bone of mammals
13. Bone-forming cells are called
   (a) osteoblasts (b) osteoclasts (c) chondroblasts (d) fibroblasts
14. The protein of the bone matrix is
   (a) chondrin (b) keratin (c) ossein (d) elastin
15. The most numerous white blood cells in human blood are
   (a) lymphocytes (b) monocytes (c) eosinophils (d) neutrophils
16. The largest white blood cell is the
   (a) lymphocyte (b) monocyte (c) basophil (d) neutrophil
17. Antibodies are secreted by
   (a) mast cells (b) macrophages (c) plasma cells (d) erythrocytes
18. The average life span of a human red blood cell is
   (a) 120 days (b) 12 days (c) 60 days (d) 7 days
19. Intercalated discs are found in
   (a) skeletal muscle (b) smooth muscle (c) tendons (d) cardiac muscle
20. Smooth muscle is found in the
   (a) biceps (b) wall of the intestine (c) heart (d) tongue
21. The functional unit of a myofibril is the
   (a) sarcomere (b) sarcolemma (c) sarcoplasm (d) sarcoplasmic reticulum
22. The myelin sheath of peripheral nerve fibres is formed by
   (a) oligodendrocytes (b) astrocytes (c) Schwann cells (d) microglia
23. Nissl granules of a neuron are made of
   (a) mitochondria (b) lysosomes (c) Golgi bodies (d) rough ER with ribosomes
24. Bipolar neurons are found in the
   (a) motor nerves of the spinal cord (b) retina (c) dorsal root ganglia (d) cerebral cortex
25. The gaps between successive segments of the myelin sheath are
   (a) Nissl bodies (b) axon hillocks (c) nodes of Ranvier (d) synaptic clefts

::: note Answers and explanations — Set A
**1.** (c) — thin, flat cells allow exchange across capillary walls; cuboidal and columnar epithelia are too thick.
**2.** (a) — transitional epithelium stretches as the bladder fills; keratinised epithelium is confined to the skin.
**3.** (d) — the "respiratory epithelium": cells of different heights with cilia and goblet cells, all on one basement membrane.
**4.** (b) — PCT cells reabsorb most of the filtrate across a brush border. The trachea is ciliated, the bladder transitional.
**5.** (c) — the whole sebaceous cell breaks down to form sebum.
**6.** (a) — the tip of the secreting cell pinches off with the milk fat; sebaceous glands are holocrine.
**7.** (d) — fibroblasts secrete the fibres and matrix and outnumber every other cell type.
**8.** (b) — mast cells (like basophils) release heparin (anticoagulant) and histamine (inflammation).
**9.** (a) — tendons of dense white collagen fibres join muscle to bone; ligaments join bone to bone.
**10.** (c) — elastic fibres let the pinna and epiglottis bend and spring back.
**11.** (b) — collagen bundles make fibrocartilage the strongest cartilage, fit for the discs and pubic symphysis.
**12.** (d) — each Haversian system (osteon) of compact bone has a central canal with blood vessels; cartilage is avascular.
**13.** (a) — osteoblasts build bone; osteoclasts resorb it.
**14.** (c) — ossein (collagen) is the organic part of bone matrix; chondrin belongs to cartilage.
**15.** (d) — neutrophils are 60–65 % of WBCs; lymphocytes come second at 20–25 %.
**16.** (b) — the monocyte, with a kidney-shaped nucleus, becomes a tissue macrophage.
**17.** (c) — plasma cells are activated B lymphocytes.
**18.** (a) — about 120 days; worn-out RBCs are removed in the spleen and liver.
**19.** (d) — intercalated discs with gap junctions let the heart's fibres contract as one unit.
**20.** (b) — the gut wall's smooth muscle produces peristalsis; biceps and tongue are skeletal, the heart cardiac.
**21.** (a) — the sarcomere, from one Z line to the next, is the unit that shortens.
**22.** (c) — Schwann cells in the PNS; oligodendrocytes myelinate CNS fibres.
**23.** (d) — Nissl granules are rough ER studded with ribosomes, making proteins for the long axon.
**24.** (b) — retinal bipolar cells link the rods and cones with ganglion cells.
**25.** (c) — the nodes of Ranvier, where the impulse jumps in saltatory conduction.
:::

**Set B — Understanding (15 questions)**

1. Epithelial cells receive their oxygen and nutrients
   (a) from capillaries running between the cells (b) by diffusion from vessels in the connective tissue below (c) from lymph vessels within the epithelium (d) from the air directly
2. Transitional epithelium suits the urinary bladder because
   (a) its cells secrete mucus (b) it is keratinised (c) it absorbs urine (d) its cells change shape and flatten when the bladder stretches
3. Which pair is correctly matched?
   (a) ciliated columnar — fallopian tube (b) keratinised stratified squamous — oesophagus (c) simple squamous — PCT (d) transitional — trachea
4. Which statement is true of cartilage but NOT of bone?
   (a) its matrix contains hydroxyapatite (b) it has Haversian canals (c) it is avascular and fed by diffusion (d) its cells lie in lacunae
5. During contraction of a skeletal muscle, which part of the sarcomere keeps its length?
   (a) I band (b) A band (c) H zone (d) the whole sarcomere
6. Cardiac muscle works throughout life without fatigue mainly because it
   (a) is under voluntary control (b) lacks myofibrils (c) has no nuclei (d) has many mitochondria and a rich blood supply
7. Red muscle fibres differ from white muscle fibres in having
   (a) more myoglobin and mitochondria (b) fewer mitochondria (c) faster but brief contraction (d) a poorer blood supply
8. Myelinated fibres conduct impulses faster than non-myelinated fibres of the same diameter because
   (a) they have more Nissl granules (b) myelin itself carries the current (c) the impulse jumps from node to node (d) they lack a neurilemma
9. Blood is classed as a connective tissue because it
   (a) contains haemoglobin (b) is mesodermal, with cells in a fluid matrix (c) flows in vessels (d) has no fibres at all
10. Brown adipose tissue is abundant in newborn babies and hibernating mammals because it
   (a) stores water (b) secretes insulin (c) forms antibodies (d) produces heat by oxidising fat
11. The phagocytic cells of the central nervous system are the
   (a) microglia (b) astrocytes (c) oligodendrocytes (d) ependymal cells
12. Basophils resemble mast cells in that both
   (a) make antibodies (b) carry oxygen (c) release histamine and heparin (d) form myelin
13. Ligaments are more elastic than tendons because they contain more
   (a) collagen fibres (b) yellow elastic fibres (c) cartilage (d) calcium salts
14. Mature neurons cannot be replaced by division because they
   (a) lack nuclei (b) lack Nissl granules (c) lack mitochondria (d) have no functional centrioles
15. Platelets are
   (a) fragments of megakaryocytes (b) nucleated cells from the spleen (c) a kind of lymphocyte (d) RBCs without haemoglobin

::: note Answers and explanations — Set B
**1.** (b) — epithelium is avascular; everything diffuses across the basement membrane from the connective tissue capillaries.
**2.** (d) — the dome-shaped surface cells flatten and slide, so the lining stretches without tearing.
**3.** (a) — cilia sweep the ovum along the oviduct. The oesophagus is non-keratinised, the PCT cuboidal, the trachea pseudostratified.
**4.** (c) — cartilage has no blood vessels; both tissues have cells in lacunae (d), and (a), (b) are bone only.
**5.** (b) — the A band is the length of the myosin filaments, which do not shorten; actin slides in, so the I band and H zone narrow.
**6.** (d) — abundant mitochondria and coronary blood keep cardiac muscle aerobic, and its long refractory period forces rest between beats. It is involuntary (a).
**7.** (a) — myoglobin stores O₂ and many mitochondria give aerobic, sustained contraction.
**8.** (c) — myelin insulates; ion exchange happens only at the nodes, so the impulse jumps (saltatory conduction).
**9.** (b) — like all connective tissues it arises from mesoderm and has cells in an abundant matrix (plasma); fibrinogen forms fibres on clotting.
**10.** (d) — brown fat cells have many mitochondria that release the energy of fat as heat (non-shivering thermogenesis).
**11.** (a) — microglia are the brain's macrophages, derived from mesoderm.
**12.** (c) — both have granules of histamine and heparin and act in inflammation and allergy.
**13.** (b) — ligaments carry elastic fibres and allow joint movement; tendons are almost pure collagen.
**14.** (d) — neurons are permanently out of the cell cycle; textbooks give the lack of functional centrioles as the reason.
**15.** (a) — megakaryocytes of the bone marrow break into platelets, which have no nucleus.
:::

**Set C — Application (10 questions)**

1. A slide shows long, unbranched, cylindrical fibres with many peripheral nuclei and cross-striations. It was most probably taken from the
   (a) heart (b) tongue (c) stomach wall (d) iris
2. A section shows cells in lacunae in a clear, glassy matrix with no visible fibres, surrounded by perichondrium. It was most probably taken from the
   (a) pinna (b) intervertebral disc (c) epiglottis (d) tracheal rings
3. A sarcomere 2.4 μm long has an A band of 1.6 μm. If it shortens to 2.0 μm, the total length of I band in the sarcomere becomes
   (a) 0.4 μm (b) 0.8 μm (c) 0.2 μm (d) 1.2 μm
4. In a count of 200 WBCs a technician finds 124 neutrophils, 50 lymphocytes, 14 monocytes, 10 eosinophils and 2 basophils. The count suggests
   (a) bacterial infection (b) viral infection (c) allergy or worm infection (d) leukaemia
5. A person has 5 litres of blood with 5 million RBCs per mm³. If each RBC lives 120 days, about how many RBCs must be made each day?
   (a) 2 × 10⁹ (b) 2 × 10¹¹ (c) 2 × 10¹³ (d) 4 × 10⁷
6. A tissue from the pubic symphysis has chondrocytes in lacunae and dense bundles of collagen fibres in its matrix. It is
   (a) hyaline cartilage (b) elastic cartilage (c) compact bone (d) white fibrocartilage
7. A drug that blocks the release of Ca²⁺ from the sarcoplasmic reticulum would
   (a) prevent skeletal muscle contraction (b) speed up contraction (c) cause rigor mortis (d) affect only smooth muscle
8. Muscles become stiff a few hours after death because
   (a) actin and myosin filaments shorten (b) calcium is removed from the muscle (c) no ATP is left to detach the myosin cross-bridges (d) the sarcolemma dissolves
9. A drug destroys the cell bodies of neurons lying in the dorsal root ganglia. The neurons affected are
   (a) multipolar motor neurons (b) pseudounipolar sensory neurons (c) bipolar interneurons (d) multipolar autonomic neurons
10. A tissue has spindle-shaped cells, each with one central nucleus and no striations. Which activity depends on it?
   (a) movement of the limbs (b) the heartbeat (c) blinking of the eyelids (d) peristalsis of the intestine

::: note Answers and explanations — Set C
**1.** (b) — these are skeletal fibres; the tongue is skeletal muscle, while the heart is cardiac and the stomach wall and iris smooth.
**2.** (d) — a glassy matrix without visible fibres is hyaline cartilage, as in the C-shaped tracheal rings. Pinna and epiglottis are elastic, the disc fibrocartilage.
**3.** (a) — the A band stays 1.6 μm, so I band = sarcomere − A band = 2.0 − 1.6 = 0.4 μm (it was 0.8 μm before).
**4.** (c) — eosinophils are 10/200 = 5 %, above the normal 2–3 %; neutrophils (62 %), lymphocytes (25 %), monocytes (7 %) and basophils (1 %) are normal.
**5.** (b) — 5 L = 5 × 10⁶ mm³, so total RBCs = 5 × 10⁶ × 5 × 10⁶ = 2.5 × 10¹³; ÷ 120 ≈ 2 × 10¹¹ per day.
**6.** (d) — collagen bundles in a cartilage matrix mean white fibrocartilage, the tissue of the pubic symphysis and intervertebral discs.
**7.** (a) — without Ca²⁺ troponin keeps the binding sites covered and no cross-bridges form; rigor (c) needs a lack of ATP, not of Ca²⁺.
**8.** (c) — rigor mortis: cross-bridges stay locked to actin because ATP is needed to release them; the filaments themselves never shorten (a).
**9.** (b) — the dorsal root ganglia hold the cell bodies of pseudounipolar sensory neurons; motor cell bodies lie in the grey matter of the cord.
**10.** (d) — smooth muscle drives peristalsis; limbs and eyelids use skeletal muscle and the heartbeat is cardiac.
:::
