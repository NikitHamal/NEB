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

```figure caption="Simple epithelia in vertical section, as seen under the microscope. All cells touch the basement membrane (gold)."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon
fig, axes = plt.subplots(2, 3, figsize=(5.2, 3.4),
                         gridspec_kw=dict(wspace=0.05, hspace=0.62))
CELL = "#e7eff7"; EDGE = "#2c5f96"; NUC = "#41638a"; BM = "#b5832f"; MUC = "#cfe0d2"
AR = 2.2                      # y-units per x-unit, so nuclei look round
WB = dict(fc='white', ec='none', pad=0.5)

def bm(ax, x0=0.03, x1=0.97):
    ax.plot([x0, x1], [0, 0], color=BM, lw=2.2, solid_capstyle='butt', zorder=2)

def rect(ax, x0, w, h, ny=0.50, nw=0.46):
    ax.add_patch(Polygon([[x0, 0], [x0+w, 0], [x0+w, h], [x0, h]], closed=True,
                         fc=CELL, ec=EDGE, lw=0.9, zorder=3))
    nx = w*nw
    ax.add_patch(Ellipse((x0+w/2, h*ny), nx, min(nx*AR, h*0.46),
                         fc=NUC, ec='none', zorder=4))

def cilia(ax, x0, w, h, n=6):
    for x in np.linspace(x0+0.010, x0+w-0.010, n):
        ax.plot([x, x+0.008], [h, h+0.13], color=EDGE, lw=0.7, zorder=5)

def lab(ax, t, s):
    ax.text(0.5, -0.66, t, ha='center', fontsize=6.9, color=INK)
    ax.text(0.5, -0.88, s, ha='center', fontsize=5.9, color=MUTED)

for ax in axes.ravel():
    ax.set_xlim(0, 1); ax.set_ylim(-1.04, 1.14); ax.axis('off')

# (a) simple squamous
ax = axes[0, 0]; bm(ax)
for i in range(4):
    x0 = 0.03 + i*0.235; w = 0.235
    t = np.linspace(0, 1, 70)
    top = 0.12 + 0.30*np.exp(-((t-0.5)/0.17)**2)
    pts = np.vstack([[[x0, 0]], np.c_[x0 + w*t, top], [[x0+w, 0]]])
    ax.add_patch(Polygon(pts, closed=True, fc=CELL, ec=EDGE, lw=0.9, zorder=3))
    ax.add_patch(Ellipse((x0+w/2, 0.21), 0.080, 0.17, fc=NUC, ec='none', zorder=4))
ax.annotate('flat, tile-like cell', xy=(0.62, 0.32), xytext=(0.52, 0.92),
            fontsize=5.7, color=MUTED, ha='center', bbox=WB,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.annotate('basement membrane', xy=(0.20, 0.0), xytext=(0.52, -0.24),
            fontsize=5.5, color=BM, ha='center', bbox=WB,
            arrowprops=dict(arrowstyle='-', color=BM, lw=0.6))
lab(ax, '(a) simple squamous', "alveoli, Bowman's capsule")

# (b) simple cuboidal
ax = axes[0, 1]; bm(ax)
for i in range(5):
    rect(ax, 0.03 + i*0.188, 0.188, 0.36, ny=0.50, nw=0.50)
lab(ax, '(b) simple cuboidal', 'kidney tubule, thyroid')

# (c) simple columnar
ax = axes[0, 2]; bm(ax)
for i in range(6):
    rect(ax, 0.03 + i*0.157, 0.157, 0.80, ny=0.24, nw=0.52)
ax.annotate('oval nucleus\nnear the base', xy=(0.42, 0.19), xytext=(0.52, -0.42),
            fontsize=5.5, color=MUTED, ha='center', linespacing=1.2, bbox=WB,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
lab(ax, '(c) simple columnar', 'stomach, intestine')

# (d) ciliated columnar
ax = axes[1, 0]; bm(ax)
for i in range(6):
    x0 = 0.03 + i*0.157
    rect(ax, x0, 0.157, 0.74, ny=0.24, nw=0.52)
    cilia(ax, x0, 0.157, 0.74)
ax.annotate('cilia', xy=(0.42, 0.85), xytext=(0.74, 1.02), fontsize=5.8,
            color=MUTED, bbox=WB,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
lab(ax, '(d) ciliated columnar', 'oviduct, bronchiole')

# (e) pseudostratified
ax = axes[1, 1]; bm(ax)
hs = [0.80, 0.40, 0.80, 0.44, 0.80, 0.38]
for i, h in enumerate(hs):
    x0 = 0.03 + i*0.157
    ax.add_patch(Polygon([[x0, 0], [x0+0.157, 0], [x0+0.157, h], [x0, h]],
                         closed=True, fc=CELL, ec=EDGE, lw=0.9, zorder=3))
    ny = 0.66 if h > 0.6 else 0.50
    ax.add_patch(Ellipse((x0+0.0785, h*ny), 0.082, 0.175, fc=NUC, ec='none', zorder=4))
    if h > 0.6:
        cilia(ax, x0, 0.157, h, 5)
ax.annotate('nuclei at two levels,\nbut one cell layer', xy=(0.34, 0.22),
            xytext=(0.52, -0.42), fontsize=5.5, color=MUTED, ha='center',
            linespacing=1.2, bbox=WB,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
lab(ax, '(e) pseudostratified', 'trachea, nasal cavity')

# (f) glandular with goblet cells
ax = axes[1, 2]; bm(ax)
for i in range(6):
    x0 = 0.03 + i*0.157
    if i in (1, 4):
        t = np.linspace(0, 1, 60)
        wl = x0 + 0.0785 - 0.076*(0.22 + 0.78*t**0.75)
        wr = x0 + 0.0785 + 0.076*(0.22 + 0.78*t**0.75)
        y = 0.76*t
        ax.add_patch(Polygon(np.vstack([np.c_[wl, y], np.c_[wr[::-1], y[::-1]]]),
                             closed=True, fc=MUC, ec=EDGE, lw=0.9, zorder=3))
        ax.add_patch(Ellipse((x0+0.0785, 0.14), 0.060, 0.14, fc=NUC, ec='none', zorder=4))
        for dy, r in ((0.88, 0.028), (0.99, 0.019)):
            ax.add_patch(Ellipse((x0+0.0785, dy), r*1.5, r*3.0, fc=MUC,
                                 ec=EDGE, lw=0.5, zorder=4))
    else:
        rect(ax, x0, 0.157, 0.76, ny=0.24, nw=0.52)
ax.annotate('goblet cell\nsheds mucus', xy=(0.20, 0.52), xytext=(0.54, -0.42),
            fontsize=5.5, color=MUTED, ha='center', linespacing=1.2, bbox=WB,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
lab(ax, '(f) glandular', 'gut lining, trachea')
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

```figure caption="Compound epithelia. Transitional epithelium is drawn relaxed and stretched to show why the bladder can fill without tearing."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon
fig, axes = plt.subplots(1, 3, figsize=(5.2, 3.0),
                         gridspec_kw=dict(wspace=0.07))
CELL = "#e7eff7"; EDGE = "#2c5f96"; NUC = "#41638a"; BM = "#b5832f"; KER = "#efe2c6"
WB = dict(fc='white', ec='none', pad=0.5)

def bm(ax, x0=0.03, x1=0.97):
    ax.plot([x0, x1], [0, 0], color=BM, lw=2.2, solid_capstyle='butt', zorder=2)

def cell(ax, cx, cy, w, h, fc=CELL, nw=0.40):
    ax.add_patch(Ellipse((cx, cy), w, h, fc=fc, ec=EDGE, lw=0.85, zorder=3))
    ax.add_patch(Ellipse((cx, cy), w*nw, min(h*0.46, w*nw*1.25), fc=NUC,
                         ec='none', zorder=4))

def lab(ax, t, s):
    ax.text(0.5, -0.52, t, ha='center', fontsize=6.9, color=INK)
    ax.text(0.5, -0.74, s, ha='center', fontsize=5.9, color=MUTED)

for ax in axes:
    ax.set_xlim(0, 1); ax.set_ylim(-0.88, 1.62); ax.axis('off')

# (a) stratified squamous, keratinised
ax = axes[0]; bm(ax)
for i in range(7):
    cell(ax, 0.08 + i*0.14, 0.14, 0.135, 0.26)
for i in range(6):
    cell(ax, 0.15 + i*0.14, 0.40, 0.150, 0.22)
for i in range(6):
    cell(ax, 0.12 + i*0.14, 0.60, 0.165, 0.16)
for i in range(5):
    cell(ax, 0.17 + i*0.16, 0.76, 0.185, 0.11)
for y in (0.86, 0.95, 1.04):
    ax.add_patch(Polygon([[0.05, y], [0.95, y], [0.95, y+0.062], [0.05, y+0.062]],
                         closed=True, fc=KER, ec=EDGE, lw=0.6, zorder=3))
ax.annotate('dead keratinised\nsquames shed here', xy=(0.72, 1.07),
            xytext=(0.50, 1.46), fontsize=5.5, color=MUTED, ha='center',
            linespacing=1.2, bbox=WB,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.annotate('germinative layer\n(the only dividing layer)', xy=(0.15, 0.06),
            xytext=(0.50, -0.30), fontsize=5.5, color=MUTED, ha='center',
            linespacing=1.2, bbox=WB,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
lab(ax, '(a) stratified squamous', 'epidermis of skin')

# (b) transitional, relaxed
ax = axes[1]; bm(ax)
for i in range(7):
    cell(ax, 0.08 + i*0.142, 0.15, 0.135, 0.27)
for i in range(6):
    cell(ax, 0.15 + i*0.142, 0.45, 0.155, 0.29)
for i in range(5):
    cell(ax, 0.19 + i*0.155, 0.76, 0.185, 0.30)
ax.annotate('dome-shaped\nsurface cells', xy=(0.50, 0.90), xytext=(0.50, 1.42),
            fontsize=5.5, color=MUTED, ha='center', linespacing=1.2, bbox=WB,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.text(0.50, -0.30, 'about 5 cells thick', ha='center', fontsize=5.5, color=MUTED)
lab(ax, '(b) transitional, relaxed', 'empty bladder')

# (c) transitional, stretched
ax = axes[2]; bm(ax)
for i in range(11):
    cell(ax, 0.055 + i*0.090, 0.10, 0.088, 0.18, nw=0.38)
for i in range(10):
    cell(ax, 0.10 + i*0.090, 0.28, 0.098, 0.15, nw=0.38)
ax.annotate('cells slide over\none another', xy=(0.50, 0.36), xytext=(0.50, 0.84),
            fontsize=5.5, color=MUTED, ha='center', linespacing=1.2, bbox=WB,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.annotate('', xy=(0.98, -0.16), xytext=(0.66, -0.16),
            arrowprops=dict(arrowstyle='-|>', color='#c0392b', lw=1.0, mutation_scale=8))
ax.annotate('', xy=(0.02, -0.16), xytext=(0.34, -0.16),
            arrowprops=dict(arrowstyle='-|>', color='#c0392b', lw=1.0, mutation_scale=8))
ax.text(0.50, -0.17, 'stretch', ha='center', va='center', fontsize=5.5, color='#c0392b')
lab(ax, '(c) transitional, stretched', 'full bladder')
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

```figure caption="Areolar tissue and adipose tissue. In adipose tissue the fat droplet fills the cell and pushes the nucleus to one side."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon, Circle
fig, axes = plt.subplots(1, 2, figsize=(5.2, 3.0), gridspec_kw=dict(wspace=0.06))
MTX = "#f5f2ec"; COLL = "#7f8b99"; ELA = "#c8a02e"; EDGE = "#2c5f96"
CYT = "#e7eff7"; NUC = "#41638a"; FAT = "#fbf3d8"
WB = dict(fc='white', ec='none', pad=0.5)
rng = np.random.default_rng(7)

for ax in axes:
    ax.set_xlim(0, 10); ax.set_ylim(-3.5, 8.9); ax.axis('off')
    ax.add_patch(Polygon([[0.2, 0.2], [9.8, 0.2], [9.8, 7.8], [0.2, 7.8]],
                         closed=True, fc=MTX, ec='none', zorder=1))

# ---------------- (a) areolar ----------------
ax = axes[0]
x = np.linspace(0.3, 9.7, 300)
for y0, amp, ph in [(1.2, 0.45, 0.2), (2.9, 0.55, 1.4), (4.6, 0.40, 2.6),
                    (6.4, 0.50, 0.8), (7.3, 0.35, 3.3)]:
    ax.plot(x, y0 + amp*np.sin(1.5*x + ph) + 0.18*np.sin(4.1*x + ph),
            color=COLL, lw=2.3, alpha=0.85, zorder=2, solid_capstyle='round')
for x0, y0, x1, y1 in [(0.4, 7.6, 9.6, 0.6), (0.5, 0.6, 9.5, 7.4),
                       (3.2, 7.7, 5.0, 0.4), (7.0, 0.4, 8.2, 7.6)]:
    ax.plot([x0, x1], [y0, y1], color=ELA, lw=1.0, zorder=2)
    ax.plot([0.55*x0+0.45*x1, 0.55*x0+0.45*x1 + 1.3],
            [0.55*y0+0.45*y1, 0.55*y0+0.45*y1 - 0.9], color=ELA, lw=0.8, zorder=2)
# fibroblast
ax.add_patch(Polygon([[1.2, 5.6], [2.2, 6.4], [3.6, 6.2], [2.6, 5.3], [1.6, 5.1]],
                     closed=True, fc=CYT, ec=EDGE, lw=0.9, zorder=4))
ax.add_patch(Ellipse((2.3, 5.85), 0.62, 0.46, angle=15, fc=NUC, ec='none', zorder=5))
# macrophage
ax.add_patch(Polygon([[6.2, 5.4], [7.0, 6.5], [8.2, 6.3], [8.6, 5.3], [7.6, 4.6],
                      [6.6, 4.7]], closed=True, fc=CYT, ec=EDGE, lw=0.9, zorder=4))
ax.add_patch(Ellipse((7.4, 5.6), 0.72, 0.52, angle=-20, fc=NUC, ec='none', zorder=5))
for _ in range(7):
    a = 2*np.pi*rng.random(); r = 0.7*np.sqrt(rng.random())
    ax.add_patch(Circle((7.4 + r*np.cos(a), 5.5 + 0.7*r*np.sin(a)), 0.09,
                        fc="#9fb2c6", ec='none', zorder=5))
# mast cell
ax.add_patch(Circle((2.6, 2.2), 0.78, fc=CYT, ec=EDGE, lw=0.9, zorder=4))
for _ in range(16):
    a = 2*np.pi*rng.random(); r = 0.66*np.sqrt(rng.random())
    ax.add_patch(Circle((2.6 + r*np.cos(a), 2.2 + r*np.sin(a)), 0.10,
                        fc="#8e6bb0", ec='none', zorder=5))
ax.add_patch(Ellipse((2.6, 2.2), 0.50, 0.44, fc=NUC, ec='none', zorder=6))
# plasma cell
ax.add_patch(Ellipse((6.6, 2.0), 1.35, 1.00, angle=-12, fc=CYT, ec=EDGE, lw=0.9, zorder=4))
ax.add_patch(Ellipse((6.25, 2.05), 0.62, 0.58, fc=NUC, ec='none', zorder=5))
for t, xy, xt in [('fibroblast', (2.3, 6.3), (1.9, 8.6)),
                  ('macrophage', (7.5, 6.4), (7.6, 8.6)),
                  ('mast cell', (2.6, 1.45), (1.3, -1.0)),
                  ('plasma cell', (6.6, 1.35), (8.6, -1.0)),
                  ('white collagen fibre', (5.1, 4.9), (5.0, -1.0)),
                  ('yellow elastic fibre', (7.9, 5.4), (5.0, -2.3))]:
    ax.annotate(t, xy=xy, xytext=xt, fontsize=5.8, color=MUTED, ha='center',
                bbox=WB, arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.text(5.0, -3.35, '(a) areolar tissue', ha='center', fontsize=7.0, color=INK)

# ---------------- (b) adipose ----------------
ax = axes[1]
centres = [(2.0, 6.55), (5.0, 6.85), (7.9, 6.45), (1.7, 3.30), (4.7, 3.45),
           (7.8, 3.20), (2.4, 0.95), (5.4, 0.85), (8.2, 0.85)]
for cx, cy in centres:
    ax.add_patch(Circle((cx, cy), 1.24, fc=CYT, ec=EDGE, lw=1.0, zorder=3))
    ax.add_patch(Circle((cx, cy), 1.04, fc=FAT, ec=EDGE, lw=0.7, zorder=4))
    ax.add_patch(Ellipse((cx - 0.88, cy - 0.56), 0.62, 0.34, angle=32,
                         fc=NUC, ec='none', zorder=5))
ax.plot([0.3, 9.7], [4.98, 4.98], color="#c0392b", lw=1.6, alpha=0.75, zorder=2)
ax.plot([0.3, 9.7], [4.72, 4.72], color="#c0392b", lw=1.6, alpha=0.75, zorder=2)
for t, xy, xt in [('single large fat droplet', (5.0, 7.3), (5.0, 8.7)),
                  ('nucleus flattened\nagainst the cell rim', (3.85, 2.88), (2.2, -1.9)),
                  ('capillary', (8.8, 4.85), (8.0, -1.6))]:
    ax.annotate(t, xy=xy, xytext=xt, fontsize=5.8, color=MUTED, ha='center',
                linespacing=1.2, bbox=WB,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.text(5.0, -3.35, '(b) adipose tissue', ha='center', fontsize=7.0, color=INK)
```
### Dense connective tissue

In dense tissue the fibres are packed so tightly that the cells are squeezed
into rows between them. When the fibres all run one way the tissue is *regular*
and resists pull along a single line — the tendon and the ligament. When they
run in all directions it is *irregular* and resists pull from any direction —
the dermis of the skin and the capsules of organs.

```figure caption="Dense regular connective tissue: a tendon is built of straight white collagen bundles, a ligament of branching yellow elastic fibres."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon
fig, axes = plt.subplots(1, 2, figsize=(5.2, 2.9), gridspec_kw=dict(wspace=0.06))
MTX = "#f5f2ec"; COLL = "#8d99a8"; ELA = "#c8a02e"; NUC = "#41638a"
WB = dict(fc='white', ec='none', pad=0.5)

for ax in axes:
    ax.set_xlim(0, 10); ax.set_ylim(-2.4, 8.4); ax.axis('off')
    ax.add_patch(Polygon([[0.2, 0.2], [9.8, 0.2], [9.8, 7.8], [0.2, 7.8]],
                         closed=True, fc=MTX, ec='none', zorder=1))

# (a) tendon
ax = axes[0]
x = np.linspace(0.3, 9.7, 400)
rows = [0.85, 2.35, 3.85, 5.35, 6.85]
for k, y0 in enumerate(rows):
    for d in (-0.20, 0.0, 0.20, 0.40):
        ax.plot(x, y0 + d + 0.085*np.sin(2.6*x + k), color=COLL, lw=1.5,
                alpha=0.9, zorder=2)
for k, y0 in enumerate(rows[:-1]):
    for cx in (1.5, 3.5, 5.5, 7.5, 9.0):
        ax.add_patch(Ellipse((cx + 0.3*k % 1.0, y0 + 0.78), 0.80, 0.26,
                             fc=NUC, ec='none', zorder=4))
ax.annotate('parallel bundles of\nwhite collagen fibres', xy=(6.0, 5.55),
            xytext=(5.0, 9.0), fontsize=5.9, color=MUTED, ha='center',
            linespacing=1.2, bbox=WB,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.annotate('rows of fibroblast nuclei', xy=(3.5, 4.63), xytext=(5.0, -1.2),
            fontsize=5.9, color=MUTED, ha='center', bbox=WB,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.text(5.0, -2.3, '(a) tendon  (muscle → bone)', ha='center', fontsize=7.0, color=INK)

# (b) ligament
ax = axes[1]
x = np.linspace(0.3, 9.7, 400)
for k, y0 in enumerate([1.0, 2.5, 4.0, 5.5, 7.0]):
    ax.plot(x, y0 + 0.30*np.sin(1.1*x + 0.9*k), color=ELA, lw=1.7, zorder=2)
for x0, y0, dy in [(2.0, 1.15, 1.2), (4.4, 2.7, 1.2), (6.6, 4.2, 1.2),
                   (3.1, 5.7, 1.1), (7.6, 5.7, 1.1), (1.4, 4.2, 1.1)]:
    ax.plot([x0, x0 + 1.5], [y0, y0 + dy], color=ELA, lw=1.2, zorder=2)
    ax.plot([x0, x0 + 1.3], [y0, y0 - 0.9], color=ELA, lw=1.0, zorder=2)
for cx, cy in [(2.6, 1.9), (5.3, 3.4), (7.4, 2.2), (3.9, 6.4), (8.2, 6.6), (1.5, 6.3)]:
    ax.add_patch(Ellipse((cx, cy), 0.80, 0.30, angle=12, fc=NUC, ec='none', zorder=4))
ax.annotate('branching yellow\nelastic fibres', xy=(5.9, 4.9), xytext=(5.0, 9.0),
            fontsize=5.9, color=MUTED, ha='center', linespacing=1.2, bbox=WB,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.annotate('fibroblasts scattered,\nnot in rows', xy=(5.3, 3.4), xytext=(5.0, -1.3),
            fontsize=5.9, color=MUTED, ha='center', linespacing=1.2, bbox=WB,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.text(5.0, -2.3, '(b) ligament  (bone → bone)', ha='center', fontsize=7.0, color=INK)
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

```figure caption="The three common types of cartilage. Chondrocytes lie in lacunae; what changes between types is the fibre content of the matrix."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon, Circle
fig, axes = plt.subplots(1, 3, figsize=(5.2, 3.0), gridspec_kw=dict(wspace=0.06))
EDGE = "#2c5f96"; NUC = "#41638a"; CYT = "#dfe9f3"
WB = dict(fc='white', ec='none', pad=0.5)
rng = np.random.default_rng(3)

def lacuna(ax, cx, cy, pair=False, r=0.62):
    dx = (r*0.55) if pair else 0.0
    ax.add_patch(Ellipse((cx, cy), 2.0*r + (1.1*dx), 1.55*r, fc="#ffffff",
                         ec=EDGE, lw=0.8, zorder=4))
    for s in ((-1, 1) if pair else (0,)):
        ax.add_patch(Circle((cx + s*dx*0.85, cy), r*0.52, fc=CYT, ec=EDGE,
                            lw=0.7, zorder=5))
        ax.add_patch(Circle((cx + s*dx*0.85, cy), r*0.24, fc=NUC, ec='none', zorder=6))

def frame(ax, mc):
    ax.set_xlim(0, 10); ax.set_ylim(-2.6, 9.0); ax.axis('off')
    ax.add_patch(Polygon([[0.2, 0.2], [9.8, 0.2], [9.8, 7.4], [0.2, 7.4]],
                         closed=True, fc=mc, ec='none', zorder=1))

# (a) hyaline
ax = axes[0]; frame(ax, "#e2eef2")
ax.add_patch(Polygon([[0.2, 7.4], [9.8, 7.4], [9.8, 8.2], [0.2, 8.2]],
                     closed=True, fc="#e6ddcb", ec=EDGE, lw=0.8, zorder=2))
for cx in (1.4, 3.4, 5.4, 7.4, 9.0):
    ax.add_patch(Ellipse((cx, 7.80), 0.85, 0.25, fc=NUC, ec='none', zorder=3))
for cx, cy, pr in [(2.4, 5.6, True), (6.6, 6.0, False), (1.9, 3.2, False),
                   (5.2, 3.4, True), (8.4, 3.0, False), (3.4, 1.2, False),
                   (7.2, 1.3, True)]:
    lacuna(ax, cx, cy, pr)
ax.annotate('perichondrium', xy=(5.0, 7.85), xytext=(5.0, 8.85), fontsize=5.9,
            color=MUTED, ha='center', bbox=WB,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.annotate('two chondrocytes\nin one lacuna', xy=(2.9, 5.6), xytext=(5.0, -1.2),
            fontsize=5.7, color=MUTED, ha='center', linespacing=1.2, bbox=WB,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.text(5.0, -2.45, '(a) hyaline', ha='center', fontsize=7.0, color=INK)

# (b) elastic
ax = axes[1]; frame(ax, "#f4efdc")
x = np.linspace(0.3, 9.7, 300)
for k in range(9):
    ax.plot(x, 0.6 + 0.78*k + 0.32*np.sin(1.4*x + 0.8*k), color="#c8a02e",
            lw=0.9, alpha=0.9, zorder=2)
for _ in range(14):
    x0 = 0.5 + 9.0*rng.random(); y0 = 0.5 + 6.5*rng.random()
    ax.plot([x0, x0 + 1.1], [y0, y0 + 1.5*(rng.random() - 0.5)],
            color="#c8a02e", lw=0.8, zorder=2)
for cx, cy, pr in [(2.2, 5.9, False), (6.4, 6.2, True), (1.8, 3.0, True),
                   (5.4, 3.3, False), (8.5, 2.8, False), (3.2, 1.0, False),
                   (7.6, 1.1, False)]:
    lacuna(ax, cx, cy, pr)
ax.annotate('network of yellow\nelastic fibres', xy=(4.0, 6.7), xytext=(5.0, 8.55),
            fontsize=5.7, color=MUTED, ha='center', linespacing=1.2, bbox=WB,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.annotate('lacuna', xy=(5.4, 3.3), xytext=(5.0, -1.2), fontsize=5.9,
            color=MUTED, ha='center', bbox=WB,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.text(5.0, -2.45, '(b) elastic', ha='center', fontsize=7.0, color=INK)

# (c) fibrous
ax = axes[2]; frame(ax, "#eeeae4")
x = np.linspace(0.3, 9.7, 300)
for k in range(7):
    y0 = 0.7 + 1.05*k
    for d in (-0.13, 0.0, 0.13):
        ax.plot(x, y0 + d + 0.10*np.sin(2.2*x + k), color="#8d99a8", lw=1.5,
                alpha=0.9, zorder=2)
for cx, cy, pr in [(2.4, 6.05, False), (6.8, 6.05, False), (4.4, 4.95, True),
                   (1.9, 3.85, False), (7.6, 3.85, False), (3.6, 1.75, False),
                   (8.0, 1.75, False)]:
    lacuna(ax, cx, cy, pr, r=0.52)
ax.annotate('dense collagen\nbundles', xy=(5.6, 6.9), xytext=(5.0, 8.55),
            fontsize=5.7, color=MUTED, ha='center', linespacing=1.2, bbox=WB,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.annotate('chondrocyte', xy=(3.6, 1.75), xytext=(5.0, -1.2), fontsize=5.9,
            color=MUTED, ha='center', bbox=WB,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.text(5.0, -2.45, '(c) fibrous', ha='center', fontsize=7.0, color=INK)
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

```figure caption="T.S. of mammalian compact bone showing two Haversian systems (osteons). Every osteocyte reaches the central canal through its canaliculi."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle, Polygon
fig, ax = plt.subplots(figsize=(5.0, 4.4))
BONE = "#f1e9da"; EDGE = "#6b5b3e"; NUC = "#41638a"
WB = dict(fc='white', ec='none', pad=0.5)

ax.set_xlim(-4.0, 4.0); ax.set_ylim(-3.75, 4.35)
ax.set_aspect('equal'); ax.axis('off')
ax.add_patch(Polygon([[-3.9, -2.55], [3.9, -2.55], [3.9, 2.45], [-3.9, 2.45]],
                     closed=True, fc=BONE, ec='none', zorder=1))
# periosteum
ax.add_patch(Polygon([[-3.9, 2.45], [3.9, 2.45], [3.9, 2.90], [-3.9, 2.90]],
                     closed=True, fc="#e6ddcb", ec=EDGE, lw=0.9, zorder=2))
for cx in np.arange(-3.5, 3.8, 0.9):
    ax.add_patch(Ellipse((cx, 2.68), 0.42, 0.11, fc=NUC, ec='none', zorder=3))

def osteon(ax, cx, cy, nring=3, r0=0.44, dr=0.40):
    for k in range(nring, 0, -1):
        ax.add_patch(Circle((cx, cy), r0 + dr*k, fc="#e9dfc8" if k % 2 else BONE,
                            ec=EDGE, lw=0.8, zorder=3))
    for k in range(nring):
        rr = r0 + dr*(k + 0.5)
        n = 7 + 2*k
        for a in np.linspace(0, 2*np.pi, n, endpoint=False) + 0.28*k:
            lx, ly = cx + rr*np.cos(a), cy + rr*np.sin(a)
            for s in (-1, 1):
                ax.plot([lx + s*0.055*np.cos(a), lx + s*0.21*np.cos(a)],
                        [ly + s*0.055*np.sin(a), ly + s*0.21*np.sin(a)],
                        color=EDGE, lw=0.45, zorder=4)
            ax.add_patch(Ellipse((lx, ly), 0.22, 0.105, angle=np.degrees(a) + 90,
                                 fc="#ffffff", ec=EDGE, lw=0.6, zorder=5))
            ax.add_patch(Ellipse((lx, ly), 0.135, 0.062, angle=np.degrees(a) + 90,
                                 fc=NUC, ec='none', zorder=6))
    ax.add_patch(Circle((cx, cy), r0, fc="#ffffff", ec=EDGE, lw=1.2, zorder=7))
    ax.add_patch(Circle((cx, cy + 0.11), 0.175, fc="#d9736c", ec="#a8433c",
                        lw=0.6, zorder=8))
    ax.add_patch(Circle((cx - 0.15, cy - 0.17), 0.090, fc="#a9c7e2",
                        ec=ACCENT, lw=0.5, zorder=8))
    ax.add_patch(Circle((cx + 0.16, cy - 0.18), 0.075, fc="#c8a02e",
                        ec=EDGE, lw=0.5, zorder=8))

L, R = (-1.90, 0.25), (1.95, -0.25)
osteon(ax, *L)
osteon(ax, *R)

# Volkmann's canal: transverse channel joining the two Haversian canals
vx = np.array([L[0], R[0]]); vy = np.array([L[1], R[1]])
ax.plot(vx, vy + 0.11, color=EDGE, lw=0.9, zorder=9)
ax.plot(vx, vy - 0.11, color=EDGE, lw=0.9, zorder=9)
ax.fill_between(vx, vy - 0.11, vy + 0.11, color="#ffffff", zorder=8.5)
ax.plot(vx, vy, color="#d9736c", lw=1.3, zorder=9)

for t, xy, xt in [
        ('periosteum', (-2.6, 2.68), (-2.85, 3.62)),
        ('one osteon\n(Haversian system)', (-1.90, 1.90), (-0.35, 3.62)),
        ('Haversian canal:\nblood vessel, lymph\nvessel and nerve', (2.06, -0.10), (2.95, 3.45)),
        ('concentric lamellae', (-3.36, 0.42), (-2.45, -2.45)),
        ('lacuna with osteocyte', (2.62, 0.62), (2.10, -2.45)),
        ('canaliculi', (-1.55, -1.28), (-1.30, -3.25)),
        ("Volkmann's canal", (0.10, 0.02), (1.80, -3.25))]:
    ax.annotate(t, xy=xy, xytext=xt, fontsize=6.3, color=MUTED, ha='center',
                linespacing=1.25, bbox=WB, zorder=12,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7))
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

```figure caption="The formed elements of mammalian blood, drawn to the same scale. The mammalian red cell has no nucleus; that of the frog and bird does."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle, Polygon
fig, ax = plt.subplots(figsize=(5.2, 3.2))
RBC = "#e2999a"; RBCD = "#b3595c"; PALE = "#efe3ef"; EDG = "#7d6f8c"
GN = "#8e6bb0"; GR = "#cc6b52"; GB = "#4a3a6b"
ax.set_xlim(0, 24); ax.set_ylim(-4.6, 7.2); ax.set_aspect('equal'); ax.axis('off')

def cap(x, y, t, s=''):
    ax.text(x, y, t, ha='center', fontsize=6.3, color=INK)
    if s:
        ax.text(x, y - 0.85, s, ha='center', fontsize=5.5, color=MUTED)

# --- top row: RBC surface, RBC section, platelets
ax.add_patch(Circle((2.6, 4.2), 1.55, fc=RBC, ec=RBCD, lw=0.9))
ax.add_patch(Circle((2.6, 4.2), 0.80, fc="#f0c6c6", ec=RBCD, lw=0.6))
cap(2.6, 1.95, 'RBC, surface view', 'pale, thin centre')

th = np.linspace(0, 2*np.pi, 300)
xx = 1.55*np.cos(th)
yy = 0.62*np.sin(th)*(0.34 + 0.66*np.abs(np.cos(th)))
ax.add_patch(Polygon(np.c_[8.4 + xx, 4.2 + yy], closed=True, fc=RBC, ec=RBCD, lw=0.9))
ax.annotate('', xy=(8.4, 3.62), xytext=(8.4, 4.78),
            arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=0.7, mutation_scale=6))
ax.text(10.35, 4.2, '≈ 2 μm', fontsize=5.6, color=MUTED, va='center')
ax.annotate('', xy=(6.85, 5.55), xytext=(9.95, 5.55),
            arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=0.7, mutation_scale=6))
ax.text(8.4, 5.85, '7–8 μm', fontsize=5.6, color=MUTED, ha='center')
cap(8.4, 1.95, 'RBC, side view', 'biconcave, no nucleus')

for dx, dy, r in [(0, 0, 0.52), (1.25, 0.35, 0.42), (0.75, -0.85, 0.46),
                  (2.15, -0.55, 0.38)]:
    a = np.linspace(0, 2*np.pi, 9)
    rr = r*(1 + 0.22*np.sin(3*a + dx))
    ax.add_patch(Polygon(np.c_[15.6 + dx + rr*np.cos(a), 4.3 + dy + rr*np.sin(a)],
                         closed=True, fc="#c8a9c8", ec=EDG, lw=0.7))
cap(16.4, 1.95, 'platelets', 'cell fragments')

ax.add_patch(Polygon([[19.6, 2.6], [23.6, 2.6], [23.6, 6.2], [19.6, 6.2]],
                     closed=True, fc="#f6efd9", ec="#c8b98c", lw=0.9))
ax.text(21.6, 4.9, 'plasma', ha='center', fontsize=6.3, color=INK)
ax.text(21.6, 4.0, '55% of blood\n90–92% water', ha='center', fontsize=5.5,
        color=MUTED, linespacing=1.25)
cap(21.6, 1.95, 'liquid matrix', '')

# --- bottom row: five WBCs
rng = np.random.default_rng(5)

def granules(cx, cy, n, r, col, rad=1.55):
    for _ in range(n):
        a = 2*np.pi*rng.random(); q = rad*0.82*np.sqrt(rng.random())
        ax.add_patch(Circle((cx + q*np.cos(a), cy + q*np.sin(a)), r, fc=col,
                            ec='none', alpha=0.9, zorder=4))

# neutrophil
cx, cy = 2.6, -1.5
ax.add_patch(Circle((cx, cy), 1.65, fc=PALE, ec=EDG, lw=0.9, zorder=2))
granules(cx, cy, 26, 0.10, "#b9a7c8")
for dx, dy, w, h, an in [(-0.85, 0.35, 0.95, 0.70, 20), (0.15, 0.75, 0.85, 0.65, -10),
                         (0.80, -0.25, 0.90, 0.70, 35), (-0.25, -0.80, 0.85, 0.62, -20)]:
    ax.add_patch(Ellipse((cx + dx, cy + dy), w, h, angle=an, fc=GN, ec='none', zorder=5))
ax.plot([cx - 0.5, cx + 0.05, cx + 0.5, cx - 0.1], [cy + 0.5, cy + 0.6, cy + 0.2, cy - 0.5],
        color=GN, lw=1.6, zorder=5)
cap(2.6, -3.7, 'neutrophil', '60–65% of WBC')

# eosinophil
cx = 7.4
ax.add_patch(Circle((cx, cy), 1.65, fc=PALE, ec=EDG, lw=0.9, zorder=2))
granules(cx, cy, 20, 0.20, GR)
for dx in (-0.75, 0.75):
    ax.add_patch(Ellipse((cx + dx, cy + 0.25), 1.05, 0.85, fc=GN, ec='none', zorder=5))
ax.plot([cx - 0.5, cx + 0.5], [cy + 0.25, cy + 0.25], color=GN, lw=1.8, zorder=5)
cap(7.4, -3.7, 'eosinophil', '2–3% of WBC')

# basophil
cx = 12.1
ax.add_patch(Circle((cx, cy), 1.65, fc=PALE, ec=EDG, lw=0.9, zorder=2))
ax.add_patch(Ellipse((cx - 0.55, cy + 0.30), 1.10, 0.90, angle=25, fc=GN, ec='none', zorder=4))
ax.add_patch(Ellipse((cx + 0.55, cy - 0.20), 1.05, 0.85, angle=25, fc=GN, ec='none', zorder=4))
granules(cx, cy, 16, 0.26, GB)
cap(12.1, -3.7, 'basophil', 'under 1% of WBC')

# lymphocyte
cx = 16.8
ax.add_patch(Circle((cx, cy), 1.45, fc=PALE, ec=EDG, lw=0.9, zorder=2))
ax.add_patch(Circle((cx - 0.06, cy + 0.06), 1.16, fc=GN, ec='none', zorder=4))
cap(16.8, -3.7, 'lymphocyte', '20–25% of WBC')

# monocyte
cx = 21.5
ax.add_patch(Circle((cx, cy), 1.85, fc=PALE, ec=EDG, lw=0.9, zorder=2))
a = np.linspace(-1.05*np.pi, 0.35*np.pi, 90)
inner = np.c_[cx + 1.20*np.cos(a), cy + 1.20*np.sin(a)]
outer = np.c_[cx + 0.42*np.cos(a[::-1]) + 0.55, cy + 0.42*np.sin(a[::-1]) - 0.15]
ax.add_patch(Polygon(np.vstack([inner, outer]), closed=True, fc=GN, ec='none', zorder=4))
cap(21.5, -3.7, 'monocyte', 'largest WBC')
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

```figure caption="The three types of muscle. Look for three things in an exam diagram: striations, the shape of the fibre, and the number and position of the nuclei."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon, FancyBboxPatch
fig, axes = plt.subplots(1, 3, figsize=(5.2, 3.2), gridspec_kw=dict(wspace=0.06))
MUS = "#f0d8cf"; MED = "#c9705c"; DARK = "#9c4a38"; NUC = "#41638a"
WB = dict(fc='white', ec='none', pad=0.5)

def lab(ax, t, s):
    ax.text(5.0, -3.05, t, ha='center', fontsize=7.0, color=INK)
    ax.text(5.0, -3.55, s, ha='center', va='top', fontsize=5.8, color=MUTED, linespacing=1.25)

for ax in axes:
    ax.set_xlim(0, 10); ax.set_ylim(-5.4, 8.4); ax.axis('off')

def stripe(ax, x0, x1, y0, y1, step=0.30):
    for x in np.arange(x0 + step, x1, step):
        ax.plot([x, x], [y0, y1], color=MED, lw=1.5, alpha=0.75, zorder=4)

# ---------------- (a) striated / skeletal ----------------
ax = axes[0]
for y0, y1 in [(5.0, 7.4), (2.0, 4.4)]:
    ax.add_patch(FancyBboxPatch((0.5, y0), 9.0, y1 - y0,
                                boxstyle="round,pad=0,rounding_size=0.55",
                                fc=MUS, ec=DARK, lw=1.0, zorder=3))
    stripe(ax, 0.6, 9.4, y0 + 0.10, y1 - 0.10)
    for cx in (1.8, 4.3, 6.9, 8.6):
        ax.add_patch(Ellipse((cx, y1 - 0.38), 1.00, 0.44, fc=NUC, ec='none', zorder=5))
    for cx in (3.0, 5.6, 7.8):
        ax.add_patch(Ellipse((cx, y0 + 0.38), 1.00, 0.44, fc=NUC, ec='none', zorder=5))
ax.annotate('many nuclei, pushed to\nthe edge of the fibre', xy=(4.3, 7.02),
            xytext=(5.0, 9.6), fontsize=5.8, color=MUTED, ha='center',
            linespacing=1.2, bbox=WB,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.annotate('light and dark\ncross striations', xy=(6.2, 3.2), xytext=(5.0, -1.5),
            fontsize=5.8, color=MUTED, ha='center', linespacing=1.2, bbox=WB,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
lab(ax, '(a) striated (skeletal)', 'long, cylindrical, unbranched\nvoluntary — biceps, tongue')

# ---------------- (b) cardiac ----------------
ax = axes[1]
trunk = [(0.5, 6.4, 9.5, 6.4), (0.5, 2.6, 9.5, 2.6)]
for y in (6.4, 2.6):
    ax.add_patch(FancyBboxPatch((0.5, y - 1.05), 9.0, 2.10,
                                boxstyle="round,pad=0,rounding_size=0.45",
                                fc=MUS, ec=DARK, lw=1.0, zorder=3))
    stripe(ax, 0.6, 9.4, y - 0.95, y + 0.95)
# branch joining the two fibres
ax.add_patch(Polygon([[3.5, 5.45], [5.0, 5.45], [5.6, 3.55], [4.1, 3.55]],
                     closed=True, fc=MUS, ec=DARK, lw=1.0, zorder=3))
stripe(ax, 3.8, 5.3, 3.70, 5.30, step=0.34)
for x, y in [(2.2, 6.4), (6.2, 6.4), (8.8, 6.4), (1.6, 2.6), (5.2, 2.6), (8.4, 2.6)]:
    ax.add_patch(Ellipse((x, y), 0.95, 0.80, fc=NUC, ec='none', zorder=5))
for x, y in [(4.0, 6.4), (7.6, 6.4), (3.2, 2.6), (7.0, 2.6)]:
    ax.plot([x, x + 0.34, x + 0.34, x + 0.68], [y - 1.05, y - 1.05, y + 1.05, y + 1.05],
            color=DARK, lw=2.2, zorder=6, solid_capstyle='butt')
ax.annotate('intercalated disc', xy=(4.17, 7.2), xytext=(5.0, 9.6), fontsize=5.8,
            color=MUTED, ha='center', bbox=WB,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.annotate('fibres branch and rejoin', xy=(4.9, 4.5), xytext=(5.0, -1.5),
            fontsize=5.8, color=MUTED, ha='center', bbox=WB,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.annotate('one central nucleus', xy=(6.2, 6.4), xytext=(6.4, 0.6), fontsize=5.8,
            color=MUTED, ha='center', bbox=WB,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
lab(ax, '(b) cardiac', 'branched, striated, involuntary\nheart wall only — never tires')

# ---------------- (c) smooth / unstriated ----------------
ax = axes[2]
def spindle(ax, cx, cy, L, W, ang=0.0):
    t = np.linspace(0, 2*np.pi, 200)
    x = (L/2)*np.cos(t); y = (W/2)*np.sin(t)*np.abs(np.cos(t))**0.45
    r = np.radians(ang)
    X = cx + x*np.cos(r) - y*np.sin(r); Y = cy + x*np.sin(r) + y*np.cos(r)
    ax.add_patch(Polygon(np.c_[X, Y], closed=True, fc=MUS, ec=DARK, lw=1.0, zorder=3))
    ax.add_patch(Ellipse((cx, cy), L*0.20, W*0.42, angle=ang, fc=NUC, ec='none', zorder=5))
for cx, cy, L, W, a in [(4.6, 7.3, 8.2, 1.5, -4), (5.4, 5.6, 8.6, 1.6, 5),
                        (4.4, 3.9, 8.0, 1.5, -6), (5.6, 2.2, 8.4, 1.6, 4),
                        (4.8, 0.5, 8.0, 1.5, -3)]:
    spindle(ax, cx, cy, L, W, a)
ax.annotate('spindle-shaped cell,\ntapering at both ends', xy=(8.4, 5.3),
            xytext=(5.0, 9.6), fontsize=5.8, color=MUTED, ha='center',
            linespacing=1.2, bbox=WB,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.annotate('no striations; one central,\ncigar-shaped nucleus', xy=(4.4, 3.9),
            xytext=(5.0, -1.7), fontsize=5.8, color=MUTED, ha='center',
            linespacing=1.2, bbox=WB,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
lab(ax, '(c) smooth (unstriated)', 'involuntary — gut, uterus,\nblood vessels, iris')
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

```figure caption="A myelinated motor neuron and an enlarged view of a synapse. The impulse travels dendrite → cyton → axon → synaptic knob, and never the other way."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon, Circle, FancyBboxPatch
fig, axes = plt.subplots(2, 1, figsize=(5.2, 4.6),
                         gridspec_kw=dict(height_ratios=[1.35, 1.0], hspace=0.06))
CYT = "#e7eff7"; EDGE = "#2c5f96"; NUC = "#41638a"; MYE = "#f2e0bf"; MYEE = "#c09a44"
WB = dict(fc='white', ec='none', pad=0.5)

# ================= upper: whole neuron =================
ax = axes[0]
ax.set_xlim(0, 26); ax.set_ylim(-4.6, 6.4); ax.axis('off')
cx, cy = 4.6, 0.6
th = np.linspace(0, 2*np.pi, 400)
r = 2.05*(1 + 0.12*np.sin(5*th + 0.6) + 0.07*np.sin(3*th))
ax.add_patch(Polygon(np.c_[cx + r*np.cos(th), cy + r*np.sin(th)], closed=True,
                     fc=CYT, ec=EDGE, lw=1.1, zorder=4))
ax.add_patch(Circle((cx - 0.15, cy + 0.15), 0.90, fc="#ffffff", ec=EDGE, lw=0.9, zorder=5))
ax.add_patch(Circle((cx - 0.15, cy + 0.15), 0.34, fc=NUC, ec='none', zorder=6))
rng = np.random.default_rng(12)
for _ in range(22):
    a = 2*np.pi*rng.random(); q = 1.85*np.sqrt(rng.random())
    px, py = cx + q*np.cos(a), cy + q*np.sin(a)
    if (px - cx + 0.15)**2 + (py - cy - 0.15)**2 > 1.25:
        ax.add_patch(Ellipse((px, py), 0.34, 0.22, angle=30*rng.random(),
                             fc="#8fa8c4", ec='none', zorder=5))
# dendrites
for ang, L in [(150, 3.4), (185, 3.8), (215, 3.2), (120, 2.9), (245, 2.7)]:
    a = np.radians(ang)
    x0, y0 = cx + 1.9*np.cos(a), cy + 1.9*np.sin(a)
    x1, y1 = cx + (1.9 + L)*np.cos(a), cy + (1.9 + L)*np.sin(a)
    ax.plot([x0, x1], [y0, y1], color=EDGE, lw=1.6, zorder=3, solid_capstyle='round')
    for d in (-28, 28):
        b = np.radians(ang + d)
        ax.plot([x1, x1 + 1.5*np.cos(b)], [y1, y1 + 1.5*np.sin(b)],
                color=EDGE, lw=1.0, zorder=3, solid_capstyle='round')
# axon hillock + axon
ax.add_patch(Polygon([[cx + 1.5, cy + 1.15], [cx + 3.3, cy + 0.42],
                      [cx + 3.3, cy - 0.42], [cx + 1.5, cy - 1.15]],
                     closed=True, fc=CYT, ec=EDGE, lw=1.0, zorder=4))
AX0, AX1 = cx + 3.3, 22.2
ax.plot([AX0, AX1], [cy, cy], color=EDGE, lw=1.7, zorder=3)
seg = [(8.2, 11.0), (11.6, 14.4), (15.0, 17.8), (18.4, 21.2)]
for a, b in seg:
    ax.add_patch(FancyBboxPatch((a, cy - 1.02), b - a, 2.04,
                                boxstyle="round,pad=0,rounding_size=0.5",
                                fc=MYE, ec=MYEE, lw=1.0, zorder=5))
    ax.add_patch(Ellipse(((a + b)/2 + 0.9, cy + 0.66), 0.85, 0.42,
                         fc=NUC, ec='none', zorder=6))
# telodendria with synaptic knobs
for dy in (-1.9, 0.0, 1.9):
    ax.plot([AX1, 24.0], [cy, cy + dy], color=EDGE, lw=1.2, zorder=3,
            solid_capstyle='round')
    ax.add_patch(Circle((24.3, cy + dy), 0.52, fc="#d9c2e0", ec="#7d5c93",
                        lw=0.9, zorder=5))
ax.annotate('', xy=(13.0, cy + 2.9), xytext=(7.0, cy + 2.9),
            arrowprops=dict(arrowstyle='-|>', color='#c0392b', lw=1.2, mutation_scale=10))
ax.text(10.0, cy + 3.35, 'direction of impulse', ha='center', fontsize=6.4, color='#c0392b')
for t, xy, xt in [
        ('dendrites', (1.0, 2.6), (1.4, 5.6)),
        ('nucleus', (cx - 0.15, cy + 0.15), (5.4, 5.6)),
        ('Nissl granules', (cx + 1.0, cy - 1.3), (2.6, -3.9)),
        ('axon hillock', (cx + 2.4, cy - 0.75), (7.4, -3.9)),
        ('node of Ranvier', (11.3, cy - 0.15), (12.2, -3.9)),
        ('myelin sheath', (12.8, cy + 1.05), (13.6, 4.6)),
        ('Schwann cell nucleus', (16.6, cy + 0.66), (19.4, 4.6)),
        ('synaptic knobs', (24.3, cy + 1.9), (21.0, -3.9))]:
    ax.annotate(t, xy=xy, xytext=xt, fontsize=6.2, color=MUTED, ha='center',
                bbox=WB, zorder=10,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.65))

# ================= lower: synapse =================
ax = axes[1]
ax.set_xlim(0, 26); ax.set_ylim(-4.7, 5.4); ax.axis('off')
# presynaptic knob
t = np.linspace(0, 2*np.pi, 300)
kx = 9.0 + 4.6*np.cos(t); ky = 2.4 + 2.5*np.sin(t)
ax.add_patch(Polygon(np.c_[kx, ky], closed=True, fc="#e7dff0", ec="#7d5c93",
                     lw=1.1, zorder=3))
ax.add_patch(Polygon([[2.0, 1.55], [5.2, 1.55], [5.2, 3.25], [2.0, 3.25]],
                     closed=True, fc="#e7dff0", ec="#7d5c93", lw=1.1, zorder=3))
rng = np.random.default_rng(21)
for _ in range(16):
    a = 2*np.pi*rng.random(); q = np.sqrt(rng.random())
    vx, vy = 9.0 + 3.4*q*np.cos(a), 2.4 + 1.8*q*np.sin(a)
    ax.add_patch(Circle((vx, vy), 0.40, fc="#ffffff", ec="#7d5c93", lw=0.7, zorder=4))
    ax.add_patch(Circle((vx, vy), 0.16, fc="#7d5c93", ec='none', zorder=5))
for mx, my, an in [(6.6, 3.5, 20), (11.6, 3.3, -15), (10.2, 1.0, 10)]:
    ax.add_patch(Ellipse((mx, my), 2.1, 0.95, angle=an, fc="#f7dfc8",
                         ec="#b5832f", lw=0.8, zorder=5))
    ax.plot([mx - 0.7, mx - 0.3, mx + 0.1, mx + 0.5],
            [my + 0.22, my - 0.22, my + 0.22, my - 0.22], color="#b5832f",
            lw=0.6, zorder=6)
# cleft and postsynaptic membrane
ax.plot([4.4, 13.6], [-0.15, -0.15], color="#7d5c93", lw=1.6, zorder=6)
ax.add_patch(Polygon([[1.6, -2.6], [24.4, -2.6], [24.4, -1.05], [1.6, -1.05]],
                     closed=True, fc="#dbe9dc", ec="#3f7a52", lw=1.1, zorder=3))
for x in np.arange(3.0, 23.0, 1.7):
    ax.add_patch(Polygon([[x, -1.05], [x + 0.75, -1.05], [x + 0.55, -0.45],
                          [x + 0.20, -0.45]], closed=True, fc="#8dc0a0",
                         ec="#3f7a52", lw=0.7, zorder=5))
for x in (5.2, 7.6, 10.0, 12.4):
    ax.add_patch(Circle((x + 0.3, -0.62), 0.22, fc="#7d5c93", ec='none', zorder=6))
    ax.annotate('', xy=(x + 0.3, -0.48), xytext=(x + 0.3, 0.55),
                arrowprops=dict(arrowstyle='-|>', color="#7d5c93", lw=0.8,
                                mutation_scale=7))
for t2, xy, xt in [
        ('axon of the\nfirst neuron', (3.0, 2.4), (3.0, 4.8)),
        ('synaptic vesicles with\nneurotransmitter', (9.6, 2.9), (11.2, 4.8)),
        ('mitochondrion', (11.9, 3.4), (18.4, 4.0)),
        ('synaptic cleft (≈ 20 nm)', (14.6, -0.55), (19.6, 1.9)),
        ('receptor proteins', (18.4, -0.75), (18.8, -3.5)),
        ('membrane of the\nnext neuron', (6.0, -1.9), (6.4, -4.2))]:
    ax.annotate(t2, xy=xy, xytext=xt, fontsize=6.2, color=MUTED, ha='center',
                linespacing=1.2, bbox=WB, zorder=10,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.65))
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
