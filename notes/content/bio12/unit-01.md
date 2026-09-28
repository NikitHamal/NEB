---
subject: Biology
grade: 12
unit: 1
title: Plant Anatomy
hours: 8
area: Botany
---

Anatomy is what you see when you cut a plant open. A stem looks like a green rod
from outside; under a microscope it turns out to be a precisely arranged
community of cells, some alive and thin-walled, some dead and reinforced, some
hollowed out into pipes. This unit teaches you to read a transverse section —
to look at a slide and say, in a few seconds, *dicot root* or *monocot stem*,
and to justify the answer from what is on the slide.

::: key What the examiner asks from this unit
Four things, again and again. (1) Classify a tissue and give its wall structure
and function. (2) Identify a transverse section and list the *diagnostic*
differences — not every difference, the ones that decide it. (3) Draw a labelled
TS of a dicot or monocot root, stem or leaf. (4) Describe secondary growth of a
dicot stem in order: cambial ring, secondary xylem and phloem, annual rings,
cork cambium, bark. Nearly every long question in this unit is a comparison or
a sequence, so learn it as a table or as a numbered chain, never as loose prose.
:::

## 1.1 Concept of tissues

A single-celled *Chlamydomonas* does everything with one cell: it photosynthesises,
absorbs, moves and reproduces. A *Ficus* tree cannot. It is too large for
diffusion to supply its interior, too heavy to stand without reinforcement, and
too long-lived to leave repair to chance. Its answer is **division of labour**:
groups of cells specialise, and each group does one job well.

::: definition Tissue
A **tissue** is a group of cells of common origin that are structurally similar
and work together to perform a particular function. The study of tissues is
**histology**; the study of the internal structure of plants is **plant
anatomy**. Nehemiah Grew and Marcello Malpighi, working independently in the
1670s, founded the subject; Grew is usually called the *father of plant
anatomy*.
:::

Tissues are classified on two quite different bases, and candidates lose marks
by mixing them up.

**By the dividing power of the cells** — this gives **meristematic** tissue
(cells that retain the power to divide) and **permanent** tissue (cells that
have lost it). This is the classification §1.2 develops.

**By the number of cell types present** — a **simple tissue** is made of only
one kind of cell (parenchyma, collenchyma, sclerenchyma); a **complex tissue**
is made of more than one kind of cell working as a unit (xylem, phloem).

```figure caption="Classification of plant tissues. The first split is by dividing power — meristematic or permanent; permanent tissue is then split again by the number of cell types it contains, into simple and complex."
fig, ax = plt.subplots(figsize=(5.1, 3.4))
ax.set_xlim(0, 13.6); ax.set_ylim(0, 7.0); ax.axis('off')

def box(x, y, w, h, s, fc, ec, fs=7.0, weight='normal'):
    ax.add_patch(matplotlib.patches.FancyBboxPatch(
        (x - w/2, y - h/2), w, h, boxstyle="round,pad=0.07",
        fc=fc, ec=ec, lw=0.9, zorder=3))
    ax.text(x, y, s, ha='center', va='center', fontsize=fs,
            color=INK, zorder=4, linespacing=1.25, fontweight=weight)

def elbow(x1, y1, x2, y2):
    ax.plot([x1, x1, x2, x2], [y1, (y1+y2)/2, (y1+y2)/2, y2],
            color=MUTED, lw=0.8, zorder=1)

MER = "#dfe9f2"; MERE = "#2c5f96"
PER = "#e6f0e4"; PERE = "#2e8b57"

box(6.4, 6.55, 3.2, 0.60, "PLANT TISSUE", "#f2f3f5", MUTED, 8.0, '600')
elbow(6.4, 6.25, 2.9, 5.55); elbow(6.4, 6.25, 9.9, 5.55)

box(2.9, 5.22, 3.4, 0.66, "Meristematic\n(cells still divide)", MER, MERE, 7.2, '600')
box(9.9, 5.22, 3.4, 0.66, "Permanent\n(division lost)", PER, PERE, 7.2, '600')

elbow(2.9, 4.89, 1.05, 4.00); elbow(2.9, 4.89, 2.90, 4.00); elbow(2.9, 4.89, 4.75, 4.00)
box(1.05, 3.66, 1.80, 0.68, "Apical\nshoot and\nroot tips", MER, MERE, 6.2)
box(2.90, 3.66, 1.72, 0.68, "Intercalary\nat nodes,\ngrasses", MER, MERE, 6.2)
box(4.75, 3.66, 1.72, 0.68, "Lateral\nvascular and\ncork cambia", MER, MERE, 6.2)

elbow(9.9, 4.89, 7.55, 4.00); elbow(9.9, 4.89, 11.55, 4.00)
box(7.55, 3.66, 2.10, 0.62, "Simple\none cell type", PER, PERE, 6.6)
box(11.55, 3.66, 2.10, 0.62, "Complex\nmany cell types", PER, PERE, 6.6)

# vertical spines with short stubs -> children listed down the page
def spine(sx, top, ys, bx, bw, labels):
    ax.plot([sx, sx], [top, ys[-1]], color=MUTED, lw=0.8, zorder=1)
    for y, s in zip(ys, labels):
        ax.plot([sx, bx - bw/2], [y, y], color=MUTED, lw=0.8, zorder=1)
        box(bx, y, bw, 0.54, s, "#ffffff", PERE, 6.5)

ax.plot([7.55, 6.70], [3.35, 3.35], color=MUTED, lw=0.8, zorder=1)
ax.plot([6.70, 6.70], [3.35, 2.62], color=MUTED, lw=0.8, zorder=1)
spine(6.70, 2.62, [2.62, 1.78, 0.94], 8.10, 2.50,
      ["Parenchyma", "Collenchyma", "Sclerenchyma"])

ax.plot([11.55, 10.80], [3.35, 3.35], color=MUTED, lw=0.8, zorder=1)
ax.plot([10.80, 10.80], [3.35, 2.62], color=MUTED, lw=0.8, zorder=1)
spine(10.80, 2.62, [2.62, 1.78], 12.05, 1.90, ["Xylem", "Phloem"])
ax.text(12.05, 0.94, "(conducting\ntissues)", fontsize=6.2, ha='center',
        va='center', color=MUTED, linespacing=1.3)
fig.tight_layout()
```

### The three tissue systems

Cut any organ across and the tissues fall into three concentric zones. This is
Sachs' **tissue system** classification, and it is the fastest way to organise a
labelled diagram.

| Tissue system | Tissues in it | Where | Main job |
|---|---|---|---|
| **Epidermal (dermal)** | epidermis, cuticle, stomata, trichomes, root hairs | outermost single layer | protection, control of water loss and gas exchange |
| **Ground (fundamental)** | cortex, endodermis, pericycle, pith, medullary rays, mesophyll | everything between epidermis and vascular tissue | photosynthesis, storage, support |
| **Vascular (conducting)** | xylem, phloem, cambium | in bundles or a ring | long-distance transport of water and food |

::: tip The examiner is looking for
When you are asked to "describe the internal structure" of any organ, walk
inwards in that order — epidermis, then ground tissue, then vascular tissue,
then centre. You will never leave a layer out, and the answer reads like a
section rather than a list.
:::

## 1.2 Meristems and permanent tissues

### Meristematic tissue

::: definition Meristem
A **meristem** (Greek *meristos*, divisible) is a tissue of immature cells that
retain the power of continuous division. Every permanent tissue in a plant was
once meristematic. Because meristems are retained throughout life, a plant can
keep growing for as long as it lives — **open** or **indeterminate** growth,
which animals do not have.
:::

**Characteristics of meristematic cells.** They are small, isodiametric and
tightly packed, with **no intercellular spaces**. The wall is thin and made of
cellulose. The cytoplasm is dense and the nucleus large and conspicuous.
Vacuoles are absent or very small. Ergastic substances (starch, crystals) and
plastids are absent or present only as proplastids. Metabolic rate is high.

Meristems are classified three ways. Read each classification as answering a
different question.

**(a) By origin — where the meristem came from.**

- **Promeristem** (primordial meristem): the few cells at the very tip of a root
  or shoot from which all other meristems arise.
- **Primary meristem**: derived directly from the promeristem, present from the
  embryonic stage, and responsible for the **primary body** of the plant.
- **Secondary meristem**: arises later from permanent tissue that has
  **redifferentiated** and regained the power to divide — vascular cambium in the
  interfascicular region, cork cambium, wound cambium.

**(b) By position — where the meristem sits.**

- **Apical meristem**: at the tips of root and shoot. Causes **primary growth**,
  that is, increase in length.
- **Intercalary meristem**: a piece of apical meristem left behind between
  permanent tissues, typically at the base of an internode or leaf sheath. It is
  the reason a grass lawn regrows after mowing and a bamboo culm elongates so
  fast. Found in grasses, *Equisetum*, and in mint.
- **Lateral meristem**: cylinders running the length of the axis — the
  **vascular cambium** and the **cork cambium (phellogen)**. Cause **secondary
  growth**, that is, increase in girth.

**(c) By function — Haberlandt's classification of the apical meristem.** The
apical meristem is already sorted into three zones, each destined for one tissue
system:

| Primary meristem | Gives rise to |
|---|---|
| **Protoderm** (dermatogen) | epidermis |
| **Procambium** (plerome, in part) | primary xylem, primary phloem, vascular cambium |
| **Ground meristem** (periblem + part of plerome) | cortex, endodermis, pericycle, pith, medullary rays |

```figure caption="Where the meristems are. Apical meristems at the root and shoot tips add length, intercalary meristems at the base of internodes and leaf sheaths add length after the apex has been removed, and lateral meristems add girth."
fig, ax = plt.subplots(figsize=(4.6, 4.0))
ax.set_xlim(0, 10); ax.set_ylim(0, 9.4); ax.axis('off')
GRN = "#cfe3d4"; GRNE = "#2e8b57"; BRN = "#e8dcc6"; BRNE = "#9a7330"

# stem axis
ax.add_patch(matplotlib.patches.Rectangle((4.35, 3.1), 1.3, 4.9, fc="#eef4ee",
                                          ec=GRNE, lw=1.0, zorder=2))
# root axis
ax.add_patch(matplotlib.patches.Rectangle((4.45, 0.9), 1.1, 2.2, fc="#f5efe2",
                                          ec=BRNE, lw=1.0, zorder=2))
ax.add_patch(matplotlib.patches.Polygon([[4.45, 0.9], [5.55, 0.9], [5.0, 0.35]],
                                        closed=True, fc="#f5efe2", ec=BRNE, lw=1.0, zorder=2))
ax.text(5.0, 3.05, "soil line", fontsize=6.4, color=MUTED, ha='center', va='center',
        bbox=dict(fc="white", ec="none", pad=0.8), zorder=5)
ax.plot([2.6, 7.4], [3.1, 3.1], color=MUTED, lw=0.7, ls=(0, (4, 3)), zorder=1)

# leaves
for yy, s in ((6.5, 1), (6.5, -1), (5.1, 1), (5.1, -1)):
    ax.add_patch(matplotlib.patches.Ellipse((5.0 + s*1.55, yy + 0.25), 2.2, 0.72,
                 angle=s*16, fc=GRN, ec=GRNE, lw=0.8, zorder=1))

# apical meristems (shoot + root) as accent caps
ax.add_patch(matplotlib.patches.Circle((5.0, 8.05), 0.42, fc=ACCENT, ec='white',
                                       lw=0.8, zorder=4))
ax.add_patch(matplotlib.patches.Circle((5.0, 0.62), 0.30, fc=ACCENT, ec='white',
                                       lw=0.8, zorder=4))
# intercalary
for yy in (5.85, 4.35):
    ax.add_patch(matplotlib.patches.Rectangle((4.35, yy), 1.3, 0.30, fc="#d9534f",
                                              ec='white', lw=0.6, zorder=4))
# lateral (cambium) strips
for xx in (4.52, 5.30):
    ax.add_patch(matplotlib.patches.Rectangle((xx, 3.35), 0.18, 4.45, fc="#b8860b",
                                              ec='none', zorder=4))

def lab(t, tip, tx, ty, col):
    ax.annotate(t, xy=tip, xytext=(tx, ty), fontsize=7.2, color=col,
                ha='center', va='center', zorder=6,
                bbox=dict(fc="white", ec=col, lw=0.7, boxstyle="round,pad=0.24"),
                arrowprops=dict(arrowstyle='-', color=col, lw=0.8,
                                shrinkA=3, shrinkB=2))

lab("Apical meristem\n(shoot tip)", (5.0, 8.32), 7.9, 8.85, ACCENT)
lab("Apical meristem\n(root tip)", (5.0, 0.62), 7.9, 1.05, ACCENT)
lab("Intercalary\nmeristem", (4.35, 5.98), 1.7, 6.55, "#d9534f")
lab("Lateral meristem\n(cambium)", (5.39, 4.05), 1.9, 3.55, "#b8860b")
ax.text(5.0, 9.15, "Where the meristems are", fontsize=8.4, ha='center',
        va='center', color=INK, fontweight='600')
fig.tight_layout()
```

::: caution
"Apical meristem increases length, lateral meristem increases girth" is true but
incomplete as an answer. The examiner wants the *consequence*: apical meristem
produces the **primary body** (primary growth), lateral meristem produces the
**secondary body** (secondary growth). Monocots have apical and intercalary
meristems but, with rare exceptions such as *Dracaena* and *Yucca*, no normal
vascular cambium — which is exactly why a maize stem never thickens into a trunk.
:::

### Permanent tissue

Permanent cells have **differentiated**: they have taken a fixed shape, wall and
function, and have lost the power to divide. Most are dead at maturity or become
so. Two useful words:

::: definition Differentiation, dedifferentiation, redifferentiation
**Differentiation** — a meristematic cell matures into a permanent cell.
**Dedifferentiation** — a permanent cell regains the power to divide (this is how
interfascicular cambium and cork cambium form). **Redifferentiation** — the
products of a dedifferentiated cell mature again into permanent tissue.
:::

#### Simple permanent tissues

```figure caption="The three simple permanent tissues, in transverse section. The difference is entirely in the wall: thin cellulose in parenchyma, unevenly thickened with pectin at the corners in collenchyma, uniformly lignified in sclerenchyma — and only the first two are alive."
fig, ax = plt.subplots(figsize=(5.1, 2.8))
ax.set_xlim(0, 15.6); ax.set_ylim(0, 8.4); ax.axis('off')
CYT = "#f3ead9"; WALL = "#8a6d3b"

def cellgrid(ox, fc, ec, lw=0.9):
    cells = []
    for i in range(3):
        for j in range(2):
            x, y = ox + i*1.50, 2.55 + j*1.90
            ax.add_patch(matplotlib.patches.FancyBboxPatch(
                (x, y), 1.50, 1.90, boxstyle="round,pad=0.0,rounding_size=0.22",
                fc=fc, ec=ec, lw=lw, zorder=2))
            cells.append((x + 0.75, y + 0.95))
    return cells

# --- parenchyma: thin walls, rounded cells, intercellular spaces at the joins
ox = 0.35
cells = cellgrid(ox, CYT, WALL)
for (x, y) in cells:
    ax.add_patch(matplotlib.patches.Circle((x - 0.36, y + 0.42), 0.20,
                                           fc="#6a4a78", ec='none', zorder=3))
for vx in (ox + 1.50, ox + 3.00):
    ax.add_patch(matplotlib.patches.Circle((vx, 4.45), 0.24, fc="white",
                                           ec=WALL, lw=0.7, zorder=4))
ax.annotate("intercellular space", xy=(ox + 1.50, 4.72), xytext=(ox + 2.25, 7.75),
            fontsize=6.3, color=MUTED, ha='center', va='center',
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7, shrinkA=3, shrinkB=3))
ax.text(ox + 2.25, 1.60, "Parenchyma", fontsize=7.8, ha='center', color=INK,
        fontweight='600')
ax.text(ox + 2.25, 0.85, "thin cellulose wall,", fontsize=6.3, ha='center', color=MUTED)
ax.text(ox + 2.25, 0.25, "living, stores food", fontsize=6.3, ha='center', color=MUTED)

# --- collenchyma: cellulose piled up at the shared corners only
ox = 5.65
cellgrid(ox, CYT, WALL)
for i in range(4):
    for j in range(3):
        ax.add_patch(matplotlib.patches.Circle((ox + i*1.50, 2.55 + j*1.90), 0.34,
                                               fc=WALL, ec='none', zorder=4))
ax.annotate("thickening at the corners", xy=(ox + 1.50, 4.45 + 0.34),
            xytext=(ox + 2.25, 7.75), fontsize=6.3, color=MUTED, ha='center',
            va='center',
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7, shrinkA=3, shrinkB=3))
ax.text(ox + 2.25, 1.60, "Collenchyma", fontsize=7.8, ha='center', color=INK,
        fontweight='600')
ax.text(ox + 2.25, 0.85, "pectin-rich, unevenly", fontsize=6.3, ha='center', color=MUTED)
ax.text(ox + 2.25, 0.25, "thickened, living", fontsize=6.3, ha='center', color=MUTED)

# --- sclerenchyma: uniformly lignified wall, narrow lumen, dead
ox = 10.95
cells = cellgrid(ox, WALL, "#5c4522")
for (x, y) in cells:
    ax.add_patch(matplotlib.patches.Circle((x, y), 0.34, fc="white",
                                           ec="#5c4522", lw=0.6, zorder=4))
ax.annotate("narrow lumen, no protoplast", xy=(ox + 2.25, 5.45 + 0.34),
            xytext=(ox + 2.25, 7.75), fontsize=6.3, color=MUTED, ha='center',
            va='center',
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7, shrinkA=3, shrinkB=3))
ax.text(ox + 2.25, 1.60, "Sclerenchyma", fontsize=7.8, ha='center', color=INK,
        fontweight='600')
ax.text(ox + 2.25, 0.85, "uniformly lignified,", fontsize=6.3, ha='center', color=MUTED)
ax.text(ox + 2.25, 0.25, "dead, rigid", fontsize=6.3, ha='center', color=MUTED)
fig.tight_layout()
```

**Parenchyma** is the least specialised and most abundant tissue — the "packing"
of the plant, and the tissue from which all others evolved. Cells are living,
thin-walled, isodiametric or oval, with conspicuous intercellular spaces. It
fills the cortex, pith, medullary rays and mesophyll. Functions: storage of food
and water, and, because the cells stay alive and thin-walled, it is the seat of
most metabolism. It retains some power to divide, which is why parenchyma can
dedifferentiate into cambium and why a cutting can regenerate. Modifications:

- **Chlorenchyma** — parenchyma with chloroplasts; photosynthetic. The mesophyll
  of a leaf is chlorenchyma.
- **Aerenchyma** — parenchyma with very large air cavities; gives buoyancy and
  supplies oxygen to submerged parts. Characteristic of hydrophytes such as
  *Hydrilla*, *Nymphaea* and the rice root.
- **Prosenchyma** — elongated, pointed parenchyma giving some mechanical support.
- **Idioblasts** — isolated parenchyma cells storing oil, tannin or crystals.

**Collenchyma** is living mechanical tissue. The cells are elongated with
**unevenly thickened** walls of cellulose, hemicellulose and a large amount of
**pectin**, which is what makes it flexible rather than brittle. Intercellular
spaces are usually absent. It occurs just below the epidermis in young dicot
stems, in the petiole, and in the ridges of a *Cucurbita* or *Helianthus* stem —
never in monocots and rarely in roots. Because the wall is not lignified, the
cell can still stretch, so collenchyma supports an organ that is *still
growing*. By the thickening pattern:

- **Angular** collenchyma — thickened at the corners where several cells meet
  (*Datura*, *Solanum*).
- **Lamellar (plate)** collenchyma — thickened on the tangential walls only
  (*Helianthus* stem).
- **Lacunar (tubular)** collenchyma — thickened around intercellular spaces
  (*Cucurbita*, *Ambrosia*).

**Sclerenchyma** is dead mechanical tissue. The wall is thick, uniformly
**lignified** and pierced by **simple pits**; the lumen is narrow and the
protoplast disappears at maturity. It gives rigidity, hardness and tensile
strength. Two forms:

- **Fibres** — very long, narrow cells with pointed ends, occurring in bundles.
  Commercially these are the bast fibres: jute (*Corchorus*), flax (*Linum*),
  hemp (*Cannabis*), and in Nepal **allo** or Himalayan nettle (*Girardinia
  diversifolia*), whose phloem fibres are woven in Sankhuwasabha and Bajhang.
- **Sclereids (stone cells)** — short, irregular, extremely thick-walled cells.
  The grit in a guava or pear fruit, the shell of a walnut, the hard seed coat of
  a pulse, and the stiff core of a tea leaf are all sclereids. Types include
  brachysclereids, macrosclereids, osteosclereids, astrosclereids and
  trichosclereids.

::: caution
Do not write "sclerenchyma is found only in old organs". It is found wherever
finished, non-stretching strength is needed — including the hypodermis of a
young monocot stem and the bundle caps of a young dicot stem. The reliable
distinction is *collenchyma supports a growing organ and is alive;
sclerenchyma supports a mature organ and is dead*.
:::

#### Complex permanent tissues

**Xylem** conducts water and dissolved minerals **upwards** from root to leaf,
and gives mechanical strength. It has four elements:

| Element | Living? | Structure | Function |
|---|---|---|---|
| **Tracheids** | dead | elongated, tapering, lignified, with **bordered pits**; end walls not perforated | conduction (in all vascular plants; the *only* element in gymnosperms) and support |
| **Vessels (trachea)** | dead | short, wide tubes placed end to end with **perforated end walls**, forming a continuous pipe | efficient conduction; characteristic of angiosperms |
| **Xylem fibres (wood fibres)** | dead | sclerenchymatous, thick-walled, narrow lumen | mechanical support |
| **Xylem parenchyma** | living | thin-walled, may store starch or tannin | storage and radial (lateral) conduction |

**Phloem** conducts prepared food — mainly sucrose — from source to sink, and
unlike xylem the flow can be **in either direction**. Its four elements:

| Element | Living? | Structure | Function |
|---|---|---|---|
| **Sieve tube elements** | living but **enucleate** | cylindrical cells joined end to end by perforated **sieve plates**; cytoplasm peripheral | translocation of food |
| **Companion cells** | living | narrow, dense cytoplasm, prominent nucleus, connected to the sieve tube by plasmodesmata | control the sieve tube, whose own nucleus is gone; load sugar |
| **Phloem fibres (bast fibres)** | dead | sclerenchymatous | support; the only *hard* element of phloem |
| **Phloem parenchyma** | living | thin-walled | storage of food, resin and latex |

```figure caption="Elements of the two complex tissues. Xylem conducts through dead cells with lignified walls: tracheids with bordered pits and vessels joined end to end into an open pipe. Phloem conducts through living sieve tubes that have lost their nucleus and are kept working by the companion cell beside them."
fig, ax = plt.subplots(figsize=(5.1, 3.1))
ax.set_xlim(0, 13.0); ax.set_ylim(0, 9.6); ax.axis('off')
W = "#8a6d3b"; L = "#f3ead9"; PH = "#dff0e4"; PHE = "#2e8b57"

# tracheid
ax.add_patch(matplotlib.patches.Polygon(
    [[1.0,7.9],[1.9,8.6],[2.8,7.9],[2.8,2.2],[1.9,1.5],[1.0,2.2]],
    closed=True, fc=L, ec=W, lw=1.1))
for y in (3.2, 4.2, 5.2, 6.2, 7.0):
    for x in (1.0, 2.8):
        ax.add_patch(matplotlib.patches.Ellipse((x, y), 0.34, 0.52, fc="white", ec=W, lw=0.8))
ax.text(1.9, 0.85, "Tracheid", fontsize=7.4, ha='center', fontweight='600', color=INK)
ax.text(1.9, 0.20, "bordered pits", fontsize=6.2, ha='center', color=MUTED)

# vessel: three members stacked, perforated plates
for (yb, yt) in ((2.0, 4.3), (4.5, 6.8), (7.0, 8.9)):
    ax.add_patch(matplotlib.patches.Rectangle((4.3, yb), 1.9, yt-yb, fc=L, ec=W, lw=1.1))
for y in (4.4, 6.9):
    ax.plot([4.3, 6.2], [y, y], color=W, lw=1.4)
    for x in (4.65, 5.05, 5.45, 5.85):
        ax.plot([x, x], [y-0.16, y+0.16], color="white", lw=1.8, solid_capstyle='butt')
ax.annotate("perforated\nend wall", xy=(6.2, 6.9), xytext=(8.2, 8.95), fontsize=6.4,
            color=MUTED, ha='center', va='center',
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7, shrinkA=2, shrinkB=2))
ax.text(5.25, 0.85, "Vessel", fontsize=7.4, ha='center', fontweight='600', color=INK)
ax.text(5.25, 0.20, "open pipe", fontsize=6.2, ha='center', color=MUTED)

# sieve tube + companion cell
for (yb, yt) in ((2.0, 4.8), (4.8, 7.6)):
    ax.add_patch(matplotlib.patches.Rectangle((9.3, yb), 1.6, yt-yb, fc=PH, ec=PHE, lw=1.1))
    ax.add_patch(matplotlib.patches.Rectangle((10.95, yb+0.15), 0.72, yt-yb-0.3,
                                              fc="#cbe3d3", ec=PHE, lw=0.9))
    ax.add_patch(matplotlib.patches.Circle((11.31, (yb+yt)/2), 0.22, fc="#6a4a78", ec='none'))
for y in (4.8,):
    ax.plot([9.3, 10.9], [y, y], color=PHE, lw=1.4)
    for x in (9.6, 9.95, 10.3, 10.65):
        ax.plot([x, x], [y-0.15, y+0.15], color="white", lw=1.8, solid_capstyle='butt')
ax.annotate("sieve plate", xy=(9.8, 4.8), xytext=(8.3, 3.05), fontsize=6.4, color=MUTED,
            ha='center', va='center',
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7, shrinkA=2, shrinkB=2))
ax.annotate("companion\ncell", xy=(11.31, 6.4), xytext=(11.9, 8.55), fontsize=6.4,
            color=MUTED, ha='center', va='center',
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7, shrinkA=2, shrinkB=2))
ax.text(10.4, 0.85, "Sieve tube", fontsize=7.4, ha='center', fontweight='600', color=INK)
ax.text(10.4, 0.20, "living, no nucleus", fontsize=6.2, ha='center', color=MUTED)
fig.tight_layout()
```

**Protoxylem and metaxylem.** Xylem formed first, while the organ is still
elongating, is **protoxylem**; its vessels are narrow with annular or spiral
lignification so they can be stretched. Xylem formed later is **metaxylem**,
with wider vessels and scalariform, reticulate or pitted thickening. Where the
protoxylem lies relative to the centre of the organ is a diagnostic feature:

- **Exarch** — protoxylem towards the periphery, metaxylem towards the centre.
  Found in **roots**.
- **Endarch** — protoxylem towards the centre, metaxylem towards the periphery.
  Found in **stems**.

::: memory
**"Roots are EXtroverts, stems are ENDoverts."** Ex-arch in the root, end-arch in
the stem. One word in an answer on root anatomy that most candidates forget.
:::

**Special (secretory) tissues** are sometimes counted as a third category:
**laticiferous tissue** (latex vessels of *Euphorbia*, *Calotropis*, *Ficus* and
the rubber plant *Hevea*) and **glandular tissue** (nectaries, oil glands of
*Citrus* peel, resin canals of *Pinus*, digestive glands of *Drosera*).

## 1.3 Anatomy of dicot and monocot root

Cut a young root across, a few centimetres behind the tip, and you get the
**primary structure**. Work inwards.

**Epiblema (rhizodermis).** The outermost layer, a single row of thin-walled
cells with **no cuticle and no stomata** — a root must absorb water, so it cannot
afford to waterproof itself. Some cells extend into unicellular **root hairs**,
which is why the layer is also called the **piliferous layer**.

**Cortex.** A broad zone of thin-walled parenchyma with conspicuous
intercellular spaces, storing starch. There is no chlorenchyma and, normally, no
collenchyma.

**Endodermis.** The innermost layer of the cortex, a single ring of barrel-shaped
cells fitted together without spaces. Their radial and tangential walls carry a
band of suberin and lignin, the **Casparian strip**, which is impermeable to
water. Water therefore cannot slip past the endodermis through the wall; it is
forced through the living protoplast, and the root gains control over what
enters the stele. Opposite the protoxylem groups, a few endodermal cells remain
thin-walled — these are the **passage cells** or transfusion cells, and water
crosses there.

**Pericycle.** A single layer (occasionally more) of parenchyma just inside the
endodermis. It is the most important layer to name, because **lateral roots
arise from the pericycle** — they are **endogenous**, arising deep inside the
parent root, whereas branches of a stem arise **exogenously** from the surface.
In a dicot the pericycle also gives rise to a part of the vascular cambium and to
the cork cambium.

**Vascular tissue.** Xylem and phloem lie in **separate, alternating, radial
strips** on different radii. This **radial** arrangement is the single most
reliable sign that you are looking at a root. The xylem is **exarch**.

::: key The one-line test
Xylem and phloem on the **same radius** with cambium between them means **stem**.
Xylem and phloem on **alternate radii** means **root**. Decide that first; then
count the xylem groups to decide dicot or monocot.
:::

```photo id="bio12/dicot-root-ts" caption="Transverse section of a young dicot root (*Ranunculus*), ×100. The boxed stele is tiny compared with the cortex — that proportion is itself diagnostic of a dicot root." width="96"
mark 0.048 0.620 "1"
mark 0.330 0.600 "2"
mark 0.700 0.572 "3"
mark 0.710 0.503 "4"
box 0.646 0.366 0.170 0.238
key 1 Epiblema (piliferous layer) — one cell thick, no cuticle, bears root hairs
key 2 Cortex — a wide zone of thin-walled parenchyma packed with starch grains
key 3 Endodermis — innermost cortical layer, its walls carrying Casparian strips
key 4 Xylem of the stele — exarch, here tetrarch; the box outlines the whole stele
```
**Dicot root.** The number of xylem groups is small — usually **two to six**
(diarch, triarch, tetrarch, pentarch, hexarch). *Ranunculus* is commonly
tetrarch. The centre of the stele is occupied by xylem, so the **pith is absent
or very small**. Conjunctive tissue, the parenchyma lying between the xylem and
phloem strips, later becomes part of the cambium. Because a dicot root has a
cambium in waiting, it is capable of **secondary growth**.

**Monocot root.** The same ground plan, but the numbers change. The xylem groups
are many — **more than six**, often twenty or more, so the root is
**polyarch**. The bundles are pushed out into a ring near the periphery, and the
centre is filled by a **large, well-developed pith** of parenchyma. Conjunctive
tissue is often sclerenchymatous. There is **no cambium**, so a monocot root
shows **no secondary growth**.

```photo id="bio12/monocot-root-ts" caption="Transverse section of a monocot root (*Zea mays*), ×40. The vascular bundles form a ring enclosing a large central pith." width="74"
crop 0.235 0.205 0.580 0.785
mark 0.102 0.348 "1"
mark 0.186 0.500 "2"
mark 0.640 0.565 "3"
mark 0.520 0.455 "4"
key 1 Epidermis, with the remains of root hairs
key 2 Cortex — wide and parenchymatous, as in a dicot root
key 3 Ring of many alternating xylem and phloem groups (polyarch)
key 4 Large central pith — the feature a dicot root does not have
```
```figure caption="Transverse section of a dicot and a monocot root. Read the number of xylem arms first: two to six in a dicot, many in a monocot. The dicot has little or no pith and will later form cambium; the monocot has a large pith and never does."
fig, ax = plt.subplots(figsize=(5.1, 3.1))
ax.set_xlim(0, 13.4); ax.set_ylim(0, 8.8); ax.axis('off')
CORT = "#eef2e8"; CORTE = "#7d8a6b"
XY = "#d9534f"; PHL = "#2e8b57"; PITH = "#f6e7cf"; END = "#b8860b"

for (x, c, lab, ec) in ((2.35, XY, "xylem", 'none'), (5.15, PHL, "phloem", 'none'),
                        (8.05, PITH, "pith", MUTED),
                        (10.35, "white", "endodermis", END)):
    ax.add_patch(matplotlib.patches.Rectangle((x, 8.10), 0.42, 0.30, fc=c, ec=ec, lw=0.8))
    ax.text(x + 0.56, 8.25, lab, fontsize=6.8, va='center', color=INK)

def root(cx, cy, R, n, pith, title, sub):
    ax.add_patch(matplotlib.patches.Circle((cx, cy), R, fc=CORT, ec=CORTE, lw=1.1))
    ax.add_patch(matplotlib.patches.Circle((cx, cy), R*0.955, fc='none', ec=CORTE, lw=0.6))
    rs = R*0.46
    ax.add_patch(matplotlib.patches.Circle((cx, cy), rs, fc="white", ec=END, lw=1.3))
    if pith:
        ax.add_patch(matplotlib.patches.Circle((cx, cy), rs*0.56, fc=PITH, ec='none'))
    for k in range(n):
        a = 2*np.pi*k/n + np.pi/2
        ax.add_patch(matplotlib.patches.Ellipse(
            (cx + rs*0.76*np.cos(a), cy + rs*0.76*np.sin(a)), rs*0.30, rs*0.44,
            angle=np.rad2deg(a)-90, fc=XY, ec='none'))
        b = a + np.pi/n
        ax.add_patch(matplotlib.patches.Ellipse(
            (cx + rs*0.74*np.cos(b), cy + rs*0.74*np.sin(b)), rs*0.24, rs*0.34,
            angle=np.rad2deg(b)-90, fc=PHL, ec='none'))
    if not pith:
        for k in range(n):
            a = 2*np.pi*k/n + np.pi/2
            ax.add_patch(matplotlib.patches.Ellipse(
                (cx + rs*0.38*np.cos(a), cy + rs*0.38*np.sin(a)), rs*0.26, rs*0.60,
                angle=np.rad2deg(a)-90, fc=XY, ec='none'))
        ax.add_patch(matplotlib.patches.Circle((cx, cy), rs*0.17, fc=XY, ec='none'))
    ax.text(cx, cy - R - 0.68, title, fontsize=8.0, ha='center', color=INK, fontweight='600')
    ax.text(cx, cy - R - 1.28, sub, fontsize=6.5, ha='center', color=MUTED)

root(3.1, 4.55, 2.55, 4, False, "Dicot root",
     "tetrarch • no pith • cambium forms later")
root(10.3, 4.55, 2.55, 12, True, "Monocot root",
     "polyarch • large pith • no cambium")
ax.text(6.7, 4.55, "xylem and\nphloem on\nalternate\nradii:\nRADIAL", fontsize=6.4,
        ha='center', va='center', color=ACCENT, linespacing=1.45)
fig.tight_layout()
```

| Feature | **Dicot root** | **Monocot root** |
|---|---|---|
| Xylem groups | 2–6 (di- to hexarch) | many, more than 6 (polyarch) |
| Pith | absent or very small | large and well developed |
| Conjunctive tissue | parenchymatous | usually sclerenchymatous |
| Cambium | develops later from conjunctive tissue and pericycle | absent |
| Secondary growth | present | absent |
| Cortex | comparatively narrow | comparatively wide |
| Example | *Helianthus*, *Cicer*, *Ranunculus* | *Zea mays*, *Oryza*, *Allium* |

Everything above the double line in that table is shared: both have epiblema
with root hairs, both have endodermis with Casparian strips and passage cells,
both have a pericycle, both have radial bundles, and in both the xylem is
exarch.

## 1.4 Anatomy of dicot and monocot stem

A stem is built for support, conduction and often photosynthesis, and its
anatomy shows it.

### Dicot stem (*Helianthus*, sunflower)

**Epidermis** — one layer, with a **cuticle**, a few **stomata** and often
multicellular **trichomes**. Unlike the root, the stem is above ground and must
limit water loss.

**Hypodermis** — several layers of **collenchyma**, often thickest under the
ridges of the stem. This is what makes a young sunflower stem ridged and
flexible.

**General cortex** — chlorenchyma outside, ordinary parenchyma inside; resin
canals occur in *Helianthus*.

**Endodermis** — the innermost cortical layer, loaded with starch grains, so it
is called the **starch sheath**. A Casparian strip is not usually visible.

**Pericycle** — semilunar patches of sclerenchyma sitting like caps on the outer
face of each vascular bundle, alternating with parenchyma. These **bundle caps**
are a strong diagnostic feature.

**Vascular bundles** — arranged in a **single ring**, limited in number, all of
the same size, and wedge-shaped. Each bundle is **conjoint** (xylem and phloem
in one bundle), **collateral** (phloem outside, xylem inside, on the same
radius), and **open** (a strip of cambium lies between them). The xylem is
**endarch**.

**Pith and medullary rays** — a large central parenchymatous pith, with strips of
parenchyma running radially between adjacent bundles. Those strips are the
**medullary (pith) rays**, and the part of them lying between the bundles is where
the **interfascicular cambium** will appear.

```photo id="bio12/dicot-stem-ts" caption="Transverse section of a young dicot stem (*Helianthus*), ×40. The vascular bundles lie in a single ring around a wide pith." width="72"
crop 0.215 0.020 0.775 1.000
mark 0.438 0.934 "1"
mark 0.241 0.902 "2"
mark 0.598 0.884 "3"
mark 0.598 0.820 "4"
mark 0.473 0.444 "5"
key 1 Epidermis, drawn out into ridges and carrying a cuticle
key 2 Hypodermis of collenchyma, thickest under each ridge, then a narrow cortex
key 3 Sclerenchymatous cap (pericyclic fibres) standing over each bundle
key 4 Vascular bundle — conjoint, collateral and open; the wide cells are metaxylem
key 5 Pith of parenchyma; medullary rays run out between the bundles
```
### Monocot stem (*Zea mays*, maize)

The differences are large enough that the two sections are never confused once
you know them.

**Epidermis** — one layer with a thick cuticle; stomata present.

**Hypodermis** — **sclerenchyma**, not collenchyma, two to three layers thick.
A maize stem is stiff rather than flexible.

**Ground tissue** — there is no differentiation into cortex, endodermis,
pericycle and pith. The whole mass inside the hypodermis is one continuous
**parenchymatous ground tissue**.

**Vascular bundles** — **scattered** throughout the ground tissue (an
**atactostele**), numerous, and of **unequal size**: the bundles near the
periphery are small and crowded, those towards the centre are large and widely
spaced. Each bundle is **conjoint, collateral and closed** — there is **no
cambium**, so a monocot stem cannot grow in girth in the ordinary way. The xylem
is **endarch**.

**Bundle sheath** — each bundle is surrounded by a sheath of sclerenchyma.
Inside, the xylem is arranged in a characteristic **"Y" or "V" shape**: two large
pitted metaxylem vessels form the arms, protoxylem lies below them, and the
lowest protoxylem vessel disintegrates to leave a water-filled cavity, the
**lysigenous cavity** or protoxylem lacuna. Phloem lies above, consisting of
sieve tubes and companion cells only — **phloem parenchyma is absent** in a
monocot stem.

```photo id="bio12/monocot-stem-ts" caption="Transverse section of a monocot stem (*Zea mays*), ×40. The bundles are scattered through a continuous ground tissue — small and crowded near the surface, large and widely spaced towards the centre." width="96"
mark 0.440 0.920 "1"
mark 0.305 0.858 "2"
mark 0.330 0.470 "3"
mark 0.430 0.645 "4"
key 1 Epidermis with a thick cuticle, underlain by a sclerenchymatous hypodermis
key 2 Small, crowded peripheral bundles
key 3 Large, widely spaced central bundle — conjoint, collateral and closed
key 4 Continuous parenchymatous ground tissue (no cortex, endodermis or pith)
```
```figure caption="Transverse section of a dicot and a monocot stem. In the dicot the bundles are open — they contain cambium — and stand in one ring around a pith. In the monocot they are closed and scattered through the ground tissue, with no pith and no secondary growth."
fig, ax = plt.subplots(figsize=(5.1, 3.1))
ax.set_xlim(0, 13.4); ax.set_ylim(0, 8.8); ax.axis('off')
GT = "#f3f1e6"; XY = "#d9534f"; PHL = "#2e8b57"
PITH = "#f6e7cf"; CAM = "#b8860b"; COL = "#cfe3d4"

for (x, c, lab) in ((2.45, XY, "xylem"), (5.25, PHL, "phloem"),
                    (8.15, CAM, "cambium"), (11.05, COL, "collenchyma")):
    ax.add_patch(matplotlib.patches.Rectangle((x, 8.10), 0.42, 0.30, fc=c, ec='none'))
    ax.text(x + 0.56, 8.25, lab, fontsize=6.8, va='center', color=INK)

cy, R = 4.55, 2.55
cx = 3.1
ax.add_patch(matplotlib.patches.Circle((cx, cy), R, fc=COL, ec="#7d8a6b", lw=1.1))
ax.add_patch(matplotlib.patches.Circle((cx, cy), R*0.86, fc=GT, ec='none'))
ax.add_patch(matplotlib.patches.Circle((cx, cy), R*0.50, fc=PITH, ec='none'))
for k in range(8):
    a = 2*np.pi*k/8 + np.pi/2
    ang = np.rad2deg(a) - 90
    ax.add_patch(matplotlib.patches.Ellipse((cx+R*0.575*np.cos(a), cy+R*0.575*np.sin(a)),
                 R*0.30, R*0.19, angle=ang, fc=XY, ec='none'))
    ax.add_patch(matplotlib.patches.Ellipse((cx+R*0.665*np.cos(a), cy+R*0.665*np.sin(a)),
                 R*0.30, R*0.05, angle=ang, fc=CAM, ec='none'))
    ax.add_patch(matplotlib.patches.Ellipse((cx+R*0.755*np.cos(a), cy+R*0.755*np.sin(a)),
                 R*0.26, R*0.145, angle=ang, fc=PHL, ec='none'))
ax.text(cx, cy - R - 0.68, "Dicot stem", fontsize=8.0, ha='center', color=INK,
        fontweight='600')
ax.text(cx, cy - R - 1.28, "one ring • open bundles • pith", fontsize=6.5,
        ha='center', color=MUTED)

cx2 = 10.3
ax.add_patch(matplotlib.patches.Circle((cx2, cy), R, fc="#e8e2cc", ec="#9a8f6b", lw=1.1))
ax.add_patch(matplotlib.patches.Circle((cx2, cy), R*0.90, fc=GT, ec='none'))
spots = []
for (ring, count, rad, off) in ((0.80, 14, 0.145, 0.0), (0.57, 9, 0.185, 0.21),
                                (0.32, 5, 0.215, 0.5), (0.0, 1, 0.215, 0.0)):
    for k in range(count):
        a = 2*np.pi*k/count + off
        spots.append((cx2 + R*ring*np.cos(a), cy + R*ring*np.sin(a), R*rad))
for (x, y, r) in spots:
    ax.add_patch(matplotlib.patches.Circle((x, y), r, fc="#f8f4e4", ec="#9a8f6b", lw=0.7))
    ax.add_patch(matplotlib.patches.Circle((x, y - r*0.20), r*0.46, fc=XY, ec='none'))
    ax.add_patch(matplotlib.patches.Circle((x, y + r*0.42), r*0.30, fc=PHL, ec='none'))
ax.text(cx2, cy - R - 0.68, "Monocot stem", fontsize=8.0, ha='center', color=INK,
        fontweight='600')
ax.text(cx2, cy - R - 1.28, "scattered • closed bundles • no pith", fontsize=6.5,
        ha='center', color=MUTED)

ax.text(6.7, 4.55, "phloem out,\nxylem in,\nsame radius:\nCOLLATERAL", fontsize=6.4,
        ha='center', va='center', color=ACCENT, linespacing=1.45)
fig.tight_layout()
```

| Feature | **Dicot stem** | **Monocot stem** |
|---|---|---|
| Hypodermis | collenchymatous | sclerenchymatous |
| Ground tissue | differentiated into cortex, endodermis, pericycle, pith | undifferentiated, continuous |
| Bundle arrangement | a single ring (eustele) | scattered (atactostele) |
| Bundle number and size | few, all alike | many, unequal — small outside, large inside |
| Bundle type | conjoint, collateral, **open** | conjoint, collateral, **closed** |
| Bundle sheath | absent (bundle caps of pericyclic sclerenchyma instead) | present, sclerenchymatous |
| Phloem parenchyma | present | absent |
| Water-containing cavity | absent | present (lysigenous cavity) |
| Medullary rays | present | absent |
| Secondary growth | present | absent |

### Types of vascular bundle — the vocabulary

You will be asked to *name* a bundle, not merely describe it.

- **Radial** — xylem and phloem on different radii, alternating. Roots.
- **Conjoint** — xylem and phloem in the same bundle. Stems and leaves.
  - **Collateral** — phloem on the outer side only (most stems).
  - **Bicollateral** — phloem on *both* the outer and inner sides of the xylem.
    Family Cucurbitaceae (*Cucurbita*, *Luffa*), and *Solanum*.
- **Concentric** — one tissue completely surrounds the other.
  - **Amphivasal (leptocentric)** — xylem surrounds phloem. *Dracaena*, *Yucca*.
  - **Amphicribral (hadrocentric)** — phloem surrounds xylem. Ferns, and the
    bundles in some fruits.
- **Open** — cambium present between xylem and phloem, secondary growth possible.
- **Closed** — no cambium, no secondary growth.

::: memory
**Amphi-VAS-al = VAS**cular tissue, i.e. **xylem**, on the outside.
**Amphi-CRIB-ral** — *cribrum* is Latin for a sieve, so **sieve tubes
(phloem)** on the outside. Two marks that hinge on one syllable.
:::

## 1.5 Anatomy of dicot and monocot leaf

A typical dicot leaf is held horizontally, so its upper surface gets far more
light than its lower. Its anatomy is correspondingly two-faced, or
**dorsiventral**. A typical monocot leaf such as grass or maize stands more or
less vertically, so both surfaces are lit equally, and its anatomy is alike on
both sides — **isobilateral**.

### Dorsiventral (dicot) leaf

**Upper epidermis** — a single layer with a thick **cuticle** and very few or no
stomata. **Lower epidermis** — a thinner cuticle and **many stomata**. A leaf
with stomata mainly on the lower surface is **hypostomatic**, which reduces
water loss because the lower surface is cooler and shaded.

**Mesophyll** — the chlorenchyma between the two epidermes, and here it is
**differentiated into two zones**:

- **Palisade parenchyma** — one to three layers of elongated, closely packed
  cylindrical cells just below the upper epidermis, standing on end with their
  long axes at right angles to the surface, and packed with chloroplasts. Most
  photosynthesis happens here.
- **Spongy parenchyma** — loosely arranged, irregular cells below the palisade,
  with large intercellular spaces continuous with the **substomatal cavity**.
  Fewer chloroplasts; this is the tissue that handles gas exchange.

**Vascular bundles** — the veins. Each is conjoint, collateral and closed, with
**xylem towards the upper (adaxial) side and phloem towards the lower (abaxial)
side** — a point worth stating, because it follows directly from the leaf being
a flattened extension of the stem. Larger veins have a **bundle sheath** of
parenchyma, and the midrib bundle sits in a ridge of collenchyma and parenchyma.
Venation is **reticulate**.

```photo id="bio12/dicot-leaf-ts" caption="Transverse section of a dorsiventral dicot leaf (*Ligustrum*, privet), ×100. Palisade cells stand on end directly under the upper epidermis; the spongy mesophyll below is full of air spaces." width="96"
mark 0.300 0.895 "1"
mark 0.300 0.775 "2"
mark 0.280 0.520 "3"
mark 0.298 0.245 "4"
mark 0.500 0.455 "5"
key 1 Upper epidermis with a thick cuticle and few or no stomata
key 2 Palisade parenchyma — elongated cells on end, holding most of the chloroplasts
key 3 Spongy mesophyll — loose cells with large air spaces for gas exchange
key 4 Lower epidermis — thinner cuticle, most of the stomata
key 5 Midrib vascular bundle — xylem above, phloem below
```
### Isobilateral (monocot) leaf

**Epidermis on both surfaces** — both cuticularised, both bearing **stomata in
roughly equal numbers** (the leaf is **amphistomatic**). The guard cells are
**dumb-bell shaped**, not kidney-shaped as in a dicot. In the upper epidermis of
grasses, groups of large, thin-walled, highly vacuolated **bulliform (motor)
cells** occur at intervals; when the plant loses water these lose turgor and the
leaf rolls inwards, cutting transpiration. You can see this in a maize field on
a hot Terai afternoon.

**Mesophyll** — **not differentiated**. There is no palisade and no spongy zone;
the whole mesophyll is uniform chlorenchyma with small intercellular spaces.

**Vascular bundles** — arranged in a **parallel row**, of unequal size (large
bundles alternating with small), each surrounded by a **sclerenchymatous bundle
sheath** which often extends as a **girder** to both epidermes. Venation is
**parallel**.

```figure caption="Transverse section of a dorsiventral and an isobilateral leaf. The dicot leaf has palisade above and spongy mesophyll below, with most stomata on the lower surface; the monocot leaf has uniform mesophyll, stomata on both surfaces, and bulliform cells that roll the blade up in dry air."
fig, ax = plt.subplots(figsize=(5.1, 3.2))
ax.set_xlim(0, 13.0); ax.set_ylim(0, 9.4); ax.axis('off')
EPI = "#f2ecdc"; EPIE = "#9a8f6b"; PAL = "#7fb98a"; SPO = "#bfdcc4"
XY = "#d9534f"; PHL = "#2e8b57"; SCL = "#b8860b"

def epi(x0, x1, yb, h):
    n = int((x1 - x0) / 0.62)
    for i in range(n):
        ax.add_patch(matplotlib.patches.Rectangle((x0 + i*(x1-x0)/n, yb),
                     (x1-x0)/n, h, fc=EPI, ec=EPIE, lw=0.6))

# ---- dorsiventral
x0, x1 = 0.5, 6.0
epi(x0, x1, 6.6, 0.62)
for i in range(9):
    ax.add_patch(matplotlib.patches.Rectangle((x0+0.22+i*0.58, 4.85), 0.40, 1.68,
                 fc=PAL, ec="#4f8a5c", lw=0.6))
for (x, y, r) in [(1.1,4.1,0.36),(1.9,4.35,0.30),(2.7,4.05,0.34),(3.6,4.30,0.32),
                  (4.4,4.05,0.35),(5.2,4.32,0.30),(1.5,3.35,0.32),(2.4,3.25,0.35),
                  (3.3,3.45,0.30),(4.1,3.25,0.33),(5.0,3.40,0.31),(5.6,3.95,0.28)]:
    ax.add_patch(matplotlib.patches.Circle((x, y), r, fc=SPO, ec="#6ea87b", lw=0.6))
epi(x0, x1, 2.30, 0.62)
# midrib bundle
ax.add_patch(matplotlib.patches.Ellipse((3.25, 4.62), 1.25, 0.72, fc="#f8f4e4",
                                        ec=EPIE, lw=0.7))
ax.add_patch(matplotlib.patches.Ellipse((3.25, 4.78), 0.86, 0.26, fc=XY, ec='none'))
ax.add_patch(matplotlib.patches.Ellipse((3.25, 4.44), 0.70, 0.22, fc=PHL, ec='none'))
# stoma lower
ax.add_patch(matplotlib.patches.Rectangle((4.62, 2.30), 0.42, 0.62, fc="white", ec=EPIE, lw=0.6))
ax.annotate("stoma", xy=(4.83, 2.36), xytext=(5.75, 1.45), fontsize=6.3, color=MUTED,
            ha='center', arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7,
                                         shrinkA=2, shrinkB=2))
ax.text(3.25, 8.75, "Dorsiventral (dicot)", fontsize=8.0, ha='center', color=INK,
        fontweight='600')
ax.text(3.25, 8.15, "mesophyll in two distinct zones", fontsize=6.5, ha='center', color=MUTED)
ax.text(6.35, 5.70, "palisade", fontsize=6.4, color=INK, ha='left', va='center')
ax.plot([5.95, 6.28], [5.70, 5.70], color=MUTED, lw=0.7)
ax.text(6.35, 3.75, "spongy", fontsize=6.4, color=INK, ha='left', va='center')
ax.plot([5.95, 6.28], [3.80, 3.75], color=MUTED, lw=0.7)

# ---- isobilateral
x0, x1 = 7.4, 12.6
epi(x0, x1, 6.6, 0.62)
epi(x0, x1, 2.30, 0.62)
rng = np.random.default_rng(7)
for i in range(7):
    for j in range(5):
        xx = x0 + 0.42 + i*0.74 + (0.24 if j % 2 else 0)
        yy = 3.30 + j*0.78
        ax.add_patch(matplotlib.patches.Circle((xx, yy), 0.33, fc=SPO, ec="#6ea87b", lw=0.6))
for (bx, br) in ((8.7, 0.62), (10.4, 0.44), (11.9, 0.62)):
    ax.add_patch(matplotlib.patches.Ellipse((bx, 4.62), br*2.0, br*1.45, fc="#f8f4e4",
                 ec=SCL, lw=1.0))
    ax.add_patch(matplotlib.patches.Ellipse((bx, 4.78), br*1.35, br*0.50, fc=XY, ec='none'))
    ax.add_patch(matplotlib.patches.Ellipse((bx, 4.42), br*1.10, br*0.42, fc=PHL, ec='none'))
    ax.add_patch(matplotlib.patches.Rectangle((bx-br*0.30, 5.30), br*0.60, 1.30,
                 fc=SCL, ec='none', alpha=0.55))
    ax.add_patch(matplotlib.patches.Rectangle((bx-br*0.30, 2.92), br*0.60, 1.00,
                 fc=SCL, ec='none', alpha=0.55))
# bulliform cells
for i, xx in enumerate((9.55, 9.95, 10.35, 10.75)):
    ax.add_patch(matplotlib.patches.Circle((xx, 6.98), 0.30 - abs(i-1.5)*0.045,
                 fc="#dfe9f2", ec=ACCENT, lw=0.7, zorder=5))
ax.annotate("bulliform cells", xy=(10.15, 7.32), xytext=(10.15, 8.15), fontsize=6.3,
            color=ACCENT, ha='center',
            arrowprops=dict(arrowstyle='-', color=ACCENT, lw=0.7, shrinkA=2, shrinkB=2))
ax.annotate("sclerenchyma girder", xy=(11.9, 5.85), xytext=(11.4, 1.45), fontsize=6.3,
            color=MUTED, ha='center',
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7, shrinkA=2, shrinkB=2))
ax.text(10.0, 8.75, "Isobilateral (monocot)", fontsize=8.0, ha='center', color=INK,
        fontweight='600')
fig.tight_layout()
```

| Feature | **Dorsiventral (dicot) leaf** | **Isobilateral (monocot) leaf** |
|---|---|---|
| Orientation | horizontal | more or less vertical |
| Stomata | mostly on the lower surface (hypostomatic) | equal on both surfaces (amphistomatic) |
| Guard cells | kidney (bean) shaped | dumb-bell shaped |
| Mesophyll | differentiated into palisade and spongy | uniform, undifferentiated |
| Bulliform cells | absent | present in the upper epidermis |
| Bundle sheath | parenchymatous | sclerenchymatous, often with girders |
| Venation | reticulate | parallel |
| Example | *Mangifera*, *Helianthus*, *Ficus* | *Zea mays*, *Oryza*, *Cynodon* |

::: example Reading an unknown slide
**Problem.** You are given a stained transverse section. It shows a single-layered
epidermis with a thick cuticle on one side only, a hypodermis of cells thickened
at their corners, a ring of eight wedge-shaped bundles each with a strip of thin
cells between the xylem and phloem, and a wide central parenchyma. Identify the
organ and the class, giving your reasons.

**Solution.**
1. **Root or stem?** The xylem and phloem lie in the *same* bundle on the same
   radius, not alternating. Therefore it is a **stem**, not a root.
2. **Cuticle and corner-thickened hypodermis.** The cuticle confirms an aerial
   organ; corner thickening is **angular collenchyma**, which occurs in dicot
   stems and never in monocots.
3. **A ring of bundles, all of similar size.** Scattered unequal bundles would
   mean a monocot; one ring means a **dicot**.
4. **A strip of thin cells between xylem and phloem** is the **cambium**, so the
   bundle is **open** — again a dicot, and the stem is capable of secondary
   growth.
5. **Wide central parenchyma** is the **pith**, present in a dicot stem, absent
   in a monocot stem.

**Answer.** A transverse section of a **young dicot stem**, showing conjoint,
collateral, open vascular bundles in a single ring.
:::

## 1.6 Secondary growth of dicot stem

A sunflower stem a metre tall can stand on its primary tissues. A *Shorea robusta*
(sal) thirty metres tall cannot. As a woody plant adds height and leaves, the
primary body can neither support the load nor carry the water the crown demands,
so the plant adds **girth** — and the tissues that do that are the two **lateral
meristems**: the **vascular cambium** and the **cork cambium**.

::: definition Secondary growth
**Secondary growth** is the increase in the thickness (girth) of a plant axis
brought about by the activity of lateral meristems. It occurs in dicot and
gymnosperm stems and roots, and is normally absent in monocots and in leaves.
:::

### Step 1 — Formation of the complete cambial ring

Look again at the primary dicot stem. Inside each vascular bundle, between the
xylem and phloem, there is already a strip of cambium: the **fascicular
(intrafascicular) cambium**. Between the bundles there is only medullary-ray
parenchyma.

Now those ray cells lying **in line with** the fascicular strips
**dedifferentiate** and become meristematic. This newly formed meristem is the
**interfascicular cambium**. The two kinds join end to end, and the result is a
continuous **cambial ring** encircling the pith.

### Step 2 — Activity of the cambial ring

The ring is one cell thick, and its cells divide **tangentially** (by periclinal
divisions), cutting off daughter cells on both faces:

- cells cut off towards the **inside** mature into **secondary xylem** — the
  **wood**;
- cells cut off towards the **outside** mature into **secondary phloem** — the
  **bast**.

Far more xylem is produced than phloem, which is why a tree trunk is
overwhelmingly wood. The consequences follow in a fixed order, and the examiner
wants them in that order:

1. The ring is pushed steadily outwards as wood accumulates inside it.
2. The **primary phloem** is crushed and obliterated against the cortex; the
   **primary xylem** survives, squeezed against the pith at the centre.
3. Certain cambial cells stay parenchymatous and produce radial files of living
   cells running through the wood — the **secondary medullary rays** — which
   carry water and food radially and store starch.
4. The cortex and epidermis, which cannot stretch indefinitely, eventually
   rupture; the plant must make a new protective layer, which is Step 3.

```figure caption="Secondary growth in a dicot stem, in three steps. A complete cambial ring forms first, then it cuts secondary xylem to the inside and secondary phloem to the outside, and finally a cork cambium in the cortex lays down the periderm."
fig, ax = plt.subplots(figsize=(5.1, 3.0))
ax.set_xlim(0, 15.0); ax.set_ylim(0, 9.6); ax.axis('off')
PITH = "#f6e7cf"; CORT = "#e9efe4"; XY = "#d9534f"; XY2 = "#e9a19d"
PHL = "#2e8b57"; PHL2 = "#9ecdaf"; CAM = "#b8860b"; CORK = "#6b5334"

for (x, c, lab) in ((0.30, XY2, "secondary xylem"), (4.85, CAM, "cambium"),
                    (7.70, PHL2, "secondary phloem"), (12.35, CORK, "cork")):
    ax.add_patch(matplotlib.patches.Rectangle((x, 9.05), 0.40, 0.28, fc=c, ec='none'))
    ax.text(x + 0.52, 9.19, lab, fontsize=6.4, va='center', color=INK)

def panel(cx, stage, title, sub):
    R, cy = 2.25, 5.60
    ax.add_patch(matplotlib.patches.Circle((cx, cy), R, fc=CORT, ec="#7d8a6b", lw=1.0))
    if stage == 3:
        ax.add_patch(matplotlib.patches.Circle((cx, cy), R, fc='none', ec=CORK, lw=2.6))
    ax.add_patch(matplotlib.patches.Circle((cx, cy), R*0.44, fc=PITH, ec='none'))
    if stage >= 2:
        ax.add_patch(matplotlib.patches.Wedge((cx, cy), R*0.80, 0, 360,
                     width=R*0.30, fc=XY2, ec='none'))
        ax.add_patch(matplotlib.patches.Wedge((cx, cy), R*0.865, 0, 360,
                     width=R*0.065, fc=CAM, ec='none'))
        ax.add_patch(matplotlib.patches.Wedge((cx, cy), R*0.925, 0, 360,
                     width=R*0.060, fc=PHL2, ec='none'))
        for k in range(10):
            a = 2*np.pi*k/10 + 0.14
            ax.plot([cx + R*0.46*np.cos(a), cx + R*0.80*np.cos(a)],
                    [cy + R*0.46*np.sin(a), cy + R*0.80*np.sin(a)],
                    color="#c6b79a", lw=0.8)
    for k in range(6):
        a = 2*np.pi*k/6 + np.pi/2
        rr = R*0.58 if stage >= 2 else R*0.68
        ang = np.rad2deg(a) - 90
        ax.add_patch(matplotlib.patches.Ellipse(
            (cx + rr*0.88*np.cos(a), cy + rr*0.88*np.sin(a)),
            R*0.22, R*0.15, angle=ang, fc=XY, ec='none'))
        if stage == 1:
            ax.add_patch(matplotlib.patches.Ellipse(
                (cx + R*0.80*np.cos(a), cy + R*0.80*np.sin(a)), R*0.20, R*0.12,
                angle=ang, fc=PHL, ec='none'))
            ax.add_patch(matplotlib.patches.Ellipse(
                (cx + R*0.735*np.cos(a), cy + R*0.735*np.sin(a)), R*0.22, R*0.045,
                angle=ang, fc=CAM, ec='none'))
    if stage == 1:
        aa = np.linspace(np.pi/2, np.pi/2 + 2*np.pi, 300)
        ax.plot(cx + R*0.735*np.cos(aa), cy + R*0.735*np.sin(aa), color=CAM,
                lw=1.1, ls=(0, (2, 2)))
    ax.text(cx, 2.55, title, fontsize=7.4, ha='center', color=INK, fontweight='600')
    ax.text(cx, 1.30, sub, fontsize=6.2, ha='center', va='center', color=MUTED,
            linespacing=1.45)

panel(2.50, 1, "1. Cambial ring",
      "interfascicular cambium\n(dashed) joins the\nfascicular strips")
panel(7.50, 2, "2. Secondary tissues",
      "xylem laid down inside,\nphloem outside,\nrays between")
panel(12.50, 3, "3. Periderm",
      "cork cambium forms\nin the cortex;\nbark appears")
fig.tight_layout()
```

### Annual rings

In a place with a marked growing season, the cambium does not work at a constant
rate.

- In **spring**, water is plentiful and growth is rapid. The cambium cuts off
  xylem with **wide vessels and thin walls** — this is **spring wood** or **early
  wood**, and it looks **light** in colour and low in density.
- In **autumn** (and through a dry or cold season), activity slows. The xylem has
  **narrow vessels and thick walls** — **autumn wood** or **late wood**, which
  looks **dark** and dense.

One band of spring wood plus the following band of autumn wood is one **annual
ring** or **growth ring**, and it represents **one year's growth**. Counting the
rings on a cut stump therefore gives the age of the tree, a technique called
**dendrochronology**; the widths also record good and bad years, so rings are
used to reconstruct past climate.

```photo id="bio12/annual-rings" caption="Transverse section of a woody dicot stem (*Tilia*), ×40. Each annual ring is one band of wide-vesselled early wood followed by one band of dense late wood." width="96"
mark 0.040 0.600 "1"
mark 0.118 0.545 "2"
mark 0.300 0.520 "3"
mark 0.420 0.780 "4"
mark 0.715 0.500 "5"
mark 0.672 0.362 "6"
key 1 Bark — periderm and the crushed tissues outside it
key 2 Secondary phloem, laid down outside the cambial ring
key 3 Secondary xylem (wood); the darker concentric arcs are annual ring boundaries
key 4 Medullary rays — files of living cells running radially out from the pith
key 5 Pith
key 6 Primary xylem, crushed against the pith by the wood formed later
```
::: caution
Annual rings are only reliable where the seasons are sharply contrasted. In the
hot, wet Terai and in the tropics generally, the cambium may work almost all
year and the rings are faint or absent; a drought in mid-season can also produce
a **false annual ring**, and a very bad year can produce none at all. So write
"counting annual rings gives the age of a tree **in regions with a distinct
growing season**" — the qualification is worth the mark.
:::

### Heartwood and sapwood

As a trunk ages, the older wood at the centre stops conducting. Its parenchyma
dies, tannins, resins, gums and oils are deposited in the cells, and neighbouring
parenchyma cells balloon into the vessels through the pits as **tyloses**,
plugging them. The result is **heartwood (duramen)** — dark, hard, durable,
resistant to insects and decay, and purely mechanical in function. It is the
timber that is commercially valuable: sal, sisau (*Dalbergia sissoo*) and teak
are prized for their heartwood.

The outer, lighter, water-conducting zone is the **sapwood (alburnum)**. It
contains living parenchyma and functioning vessels and is the only part of the
wood that actually carries the transpiration stream.

### Step 3 — The cork cambium and bark

While the vascular cambium works inside, the outer tissues are being torn apart.
A second lateral meristem, the **cork cambium** or **phellogen**, arises by
dedifferentiation of cells in the hypodermis or outer cortex (in the root, from
the pericycle). It too divides tangentially:

- **outwards** it cuts off **phellem (cork)**, whose walls become impregnated
  with **suberin**; the cells die, and the layer is impermeable to water and
  gases;
- **inwards** it cuts off **phelloderm (secondary cortex)**, a living
  parenchymatous layer.

::: definition Periderm and bark
**Periderm** = phellogen + phellem + phelloderm, taken together.
**Bark** = *all* the tissues lying outside the vascular cambium, that is,
secondary phloem + periderm and whatever remains of the cortex and epidermis. A
bark formed early in the season and containing living secondary phloem is
**soft bark**; the dead, flaking outer bark of an old trunk is **rhytidome**. If
it comes away as a complete hollow cylinder it is **ring bark** (*Betula*,
birch); if in irregular flakes, **scale bark** (*Psidium*, guava).
:::

Cork would suffocate the stem if it were unbroken, so at certain points the
phellogen produces loosely arranged, rounded, thin-walled cells with large
intercellular spaces instead of compact cork. These break through the surface as
raised lens-shaped pores, the **lenticels**, and they are the route by which a
woody stem exchanges gases. Look at the trunk of a *Dalbergia* or a mango and you
can see them with the naked eye.

Cork's commercial value comes from exactly these properties — light, compressible,
impermeable, chemically inert. Bottle cork is the phellem of *Quercus suber*, the
cork oak.

::: example Ordering the events of secondary growth
**Problem.** Arrange the following in the order in which they occur in a dicot
stem, and state which meristem is responsible for each: formation of lenticels;
crushing of primary phloem; dedifferentiation of medullary ray cells; deposition
of tyloses; formation of secondary xylem.

**Solution.**
1. **Dedifferentiation of medullary ray cells** — ray parenchyma in line with the
   fascicular cambium becomes meristematic and forms the **interfascicular
   cambium**, completing the cambial ring. *Meristem: none yet — this is the
   event that creates one.*
2. **Formation of secondary xylem** — the completed **vascular cambium** cuts off
   xylem on its inner face. This begins immediately and continues for the life of
   the tree.
3. **Crushing of primary phloem** — as secondary xylem accumulates, the cambial
   ring is pushed outwards and the primary phloem, which lies outside it, is
   compressed and obliterated. *Vascular cambium.*
4. **Formation of lenticels** — the **cork cambium (phellogen)** arises in the
   cortex and, at intervals, produces loose complementary tissue that ruptures the
   epidermis. This must come after secondary growth has begun to stretch the
   cortex. *Cork cambium.*
5. **Deposition of tyloses** — only in old wood, when central xylem ceases to
   conduct and becomes heartwood. This is the last event of the five. *No
   meristem; it is a change in existing xylem parenchyma.*

**Answer.** 3 → 5 → 2 → 1 → 4 in the order the question lists them; that is:
dedifferentiation of ray cells, secondary xylem, crushing of primary phloem,
lenticels, tyloses.
:::

::: example Why a monocot cannot become a tree in the ordinary way
**Problem.** A coconut palm is twenty metres tall, yet its stem has no annual
rings and its diameter at the top is almost the same as at the base. Explain
anatomically, and say how a palm nevertheless achieves its girth.

**Solution.**
1. A monocot vascular bundle is **conjoint, collateral and closed** — there is no
   cambium between the xylem and phloem.
2. There is also no interfascicular region of the normal kind, because the
   bundles are **scattered** through undifferentiated ground tissue rather than
   arranged in a ring; there is no line of ray parenchyma along which an
   interfascicular cambium could form.
3. With no vascular cambium, no **secondary xylem** can be produced, so there is
   no wood and therefore no spring-wood/autumn-wood alternation and **no annual
   rings**.
4. The palm instead achieves its girth by **primary thickening**: a zone of
   meristem just below the shoot apex enlarges the stem to its final diameter
   *before* it elongates. This is why the trunk is a near-uniform cylinder — each
   segment was made at full width and then simply pushed up.
5. A few monocots (*Dracaena*, *Yucca*, *Agave*) do show **anomalous secondary
   growth** from a cambium that arises outside the bundles in the ground tissue
   and produces whole new amphivasal bundles, not ordinary wood.

**Answer.** No vascular cambium, hence no secondary xylem and no annual rings;
girth comes from a primary thickening meristem, and the exceptions
(*Dracaena*, *Yucca*) use an anomalous cambium.
:::

### Secondary growth in the dicot root

The principle is the same but the ring has to be assembled differently, because
in a root the xylem and phloem are on alternating radii.

1. Conjunctive parenchyma lying **just inside each phloem strip** becomes
   meristematic. These arcs are the first pieces of cambium.
2. Cells of the **pericycle lying outside each protoxylem group** also
   dedifferentiate and join the arcs.
3. Because the arcs curve inside the phloem but bulge outwards at the protoxylem,
   the completed ring is at first **wavy** in outline.
4. The portions inside the phloem work faster, pushing outwards, and the ring soon
   becomes **circular**.
5. Thereafter it behaves exactly as in the stem: secondary xylem inside, secondary
   phloem outside, and a cork cambium — here arising from the **pericycle** —
   forms the periderm. The epiblema and cortex are shed.

## Chapter summary

- A **tissue** is a group of cells of common origin doing one job. Tissues are
  **meristematic** (still dividing) or **permanent** (differentiated), and
  **simple** (one cell type) or **complex** (several). The three **tissue
  systems** are epidermal, ground and vascular.
- **Meristems** are classified by origin (promeristem, primary, secondary), by
  position (**apical** → length, **intercalary** → grasses regrow, **lateral** →
  girth) and by function (protoderm → epidermis, procambium → vascular tissue,
  ground meristem → cortex and pith).
- Simple permanent tissues: **parenchyma** (living, thin-walled, storage;
  variants chlorenchyma, aerenchyma), **collenchyma** (living, pectin-rich,
  unevenly thickened, flexible support in growing dicot organs — angular,
  lamellar, lacunar), **sclerenchyma** (dead, lignified, rigid — fibres and
  sclereids).
- Complex tissues: **xylem** = tracheids + vessels + fibres + parenchyma
  (upward, one way); **phloem** = sieve tubes + companion cells + fibres +
  parenchyma (both ways). Protoxylem is **exarch in roots, endarch in stems**.
- **Root:** epiblema without cuticle, wide cortex, endodermis with Casparian
  strips and passage cells, pericycle giving **endogenous** lateral roots,
  **radial** bundles, exarch xylem. Dicot 2–6 xylem groups with little or no
  pith and later a cambium; monocot polyarch with a large pith and no cambium.
- **Stem:** cuticle and stomata, collenchymatous hypodermis (dicot) or
  sclerenchymatous (monocot), **conjoint collateral** bundles, endarch xylem.
  Dicot — one ring, **open**, pith and medullary rays present. Monocot —
  **scattered**, **closed**, sclerenchymatous bundle sheath, lysigenous cavity,
  no phloem parenchyma, no medullary rays.
- **Leaf:** dorsiventral (dicot) has palisade + spongy mesophyll, stomata mainly
  below, kidney-shaped guard cells, reticulate venation; isobilateral (monocot)
  has uniform mesophyll, stomata on both faces, dumb-bell guard cells,
  bulliform cells, sclerenchymatous sheaths and parallel venation.
- **Secondary growth of a dicot stem:** interfascicular cambium forms from
  medullary-ray cells and joins the fascicular cambium into a **cambial ring**;
  it cuts **secondary xylem inwards and secondary phloem outwards**, crushing the
  primary phloem. Spring wood + autumn wood = one **annual ring**. Old central
  wood becomes **heartwood** (tyloses, tannins); the conducting outer zone is
  **sapwood**.
- The **cork cambium (phellogen)** makes **phellem (cork, suberised) outwards and
  phelloderm inwards**; the three together are the **periderm**. **Bark** is
  everything outside the vascular cambium, and **lenticels** are its breathing
  pores.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Xylem and phloem lying on alternate radii is characteristic of <span class="marks">[1]</span>
   (a) a dicot stem (b) a monocot stem (c) a root (d) a dorsiventral leaf
2. The Casparian strip is found in the <span class="marks">[1]</span>
   (a) epiblema (b) pericycle (c) endodermis (d) conjunctive tissue
3. Bulliform cells occur in the <span class="marks">[1]</span>
   (a) upper epidermis of a grass leaf (b) lower epidermis of a dicot leaf (c) mesophyll of a maize leaf (d) hypodermis of a dicot stem
4. Interfascicular cambium is formed by the dedifferentiation of <span class="marks">[1]</span>
   (a) pericycle cells (b) medullary ray cells (c) endodermal cells (d) phloem parenchyma
5. A vascular bundle in which the phloem completely surrounds the xylem is called <span class="marks">[1]</span>
   (a) amphivasal (b) amphicribral (c) bicollateral (d) radial
6. Cork is impermeable to water because its walls are impregnated with <span class="marks">[1]</span>
   (a) lignin (b) cutin (c) suberin (d) pectin

::: note Answers to Group A
**1.** (c) — radial bundles are the defining feature of a root; stems and leaves have conjoint bundles.
**2.** (c) — the strip of suberin and lignin lies on the radial and tangential walls of the endodermis.
**3.** (a) — large thin-walled motor cells in the upper epidermis of grasses; they lose turgor and roll the leaf.
**4.** (b) — ray parenchyma lying in line with the fascicular strips becomes meristematic.
**5.** (b) — *cribrum* = sieve, so amphicribral means phloem outside. Amphivasal is the reverse.
**6.** (c) — suberin. Lignin stiffens sclerenchyma, cutin forms the cuticle, pectin softens collenchyma.
:::

**Group B — Short answer (4 marks each)**

1. Distinguish between collenchyma and sclerenchyma under four
   headings. <span class="marks">[4]</span>
2. Describe the structure and function of the endodermis and pericycle of a
   dicot root. <span class="marks">[4]</span>
3. What is an annual ring? Explain how spring wood and autumn wood differ, and
   state one limitation of using annual rings to age a tree in
   Nepal. <span class="marks">[4]</span>
4. Give four anatomical differences between a dorsiventral and an isobilateral
   leaf. <span class="marks">[4]</span>
5. Define bark. Distinguish between periderm and bark, and explain the function
   of lenticels. <span class="marks">[4]</span>
6. Name the four elements of xylem and state one function of
   each. <span class="marks">[4]</span>

::: note Answers to Group B
**1.** Table of four rows. *Cell state* — collenchyma living, sclerenchyma dead.
*Wall material* — cellulose, hemicellulose and pectin (collenchyma) versus
lignin (sclerenchyma). *Thickening* — uneven, at corners or on particular walls,
versus uniform and heavy with a narrow lumen. *Function and location* — flexible
support in a still-growing dicot organ (hypodermis, petiole) versus rigid
support in a mature organ (fibres, sclereids, bundle caps).

**3.** Definition, then the contrast: spring wood has wide, thin-walled vessels
and is light-coloured and less dense; autumn wood has narrow, thick-walled
vessels and is dark and dense. One of each = one year. **Limitation:** in the
Terai and the tropics the cambium may work almost continuously, so the rings are
faint or absent, and a mid-season drought can lay down a **false ring** —
so ring counts are reliable only where the growing season is sharply defined.

**6.** *Tracheids* — dead, tapering, bordered pits; conduction and support, and
the only conducting element in gymnosperms. *Vessels* — dead, wide tubes with
perforated end walls; efficient conduction, characteristic of angiosperms.
*Xylem fibres* — dead, sclerenchymatous; mechanical support. *Xylem parenchyma* —
living; storage of starch and tannin, and radial conduction.
:::

**Group C — Long answer (8 marks each)**

1. (a) Draw a labelled transverse section of a young dicot stem. <span class="marks">[4]</span>
   (b) Compare the dicot stem with a monocot stem under the headings hypodermis,
   ground tissue, arrangement of bundles, bundle type and capacity for secondary
   growth. <span class="marks">[4]</span>
2. (a) Describe, in order, the formation of the cambial ring and the production
   of secondary tissues in a dicot stem. <span class="marks">[5]</span>
   (b) Explain how the cork cambium arises and what it produces, and define
   periderm and bark. <span class="marks">[3]</span>
3. (a) Draw a labelled transverse section of a monocot root and state four
   features that distinguish it from a dicot root. <span class="marks">[5]</span>
   (b) Lateral roots are said to be endogenous while stem branches are exogenous.
   Explain what this means and why it matters. <span class="marks">[3]</span>

::: note Answer outline to Group C question 2
**(a)** Five stages, in this order and no other.
(i) The **fascicular (intrafascicular) cambium** already lies between the xylem
and phloem of each bundle.
(ii) Medullary-ray parenchyma **in line with** those strips **dedifferentiates**
to form the **interfascicular cambium**.
(iii) The two join into a continuous **cambial ring**, one cell thick.
(iv) The ring divides **tangentially**, cutting off **secondary xylem on its
inner face** and **secondary phloem on its outer face**, with far more xylem than
phloem. Some initials remain parenchymatous and produce **secondary medullary
rays**.
(v) The ring is pushed outwards; the **primary phloem is crushed** while the
primary xylem persists against the pith. With time the central wood becomes
**heartwood** and the outer wood remains conducting **sapwood**, and the
spring-wood/autumn-wood alternation shows as **annual rings**.

**(b)** The **cork cambium (phellogen)** arises by dedifferentiation of
hypodermal or outer cortical cells (in a root, from the pericycle), because the
epidermis and cortex cannot stretch to match the expanding stele and are
rupturing. It divides tangentially, cutting off **phellem (cork)** outwards —
suberised, dead, waterproof — and **phelloderm (secondary cortex)** inwards,
living parenchyma. **Periderm** = phellogen + phellem + phelloderm. **Bark** =
everything outside the vascular cambium, that is, the secondary phloem together
with the periderm and the crushed remains of cortex and epidermis. Gas exchange
continues through **lenticels**.
:::
