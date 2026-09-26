---
subject: Biology
grade: 12
unit: 7
title: Developmental Biology
hours: 6
area: Zoology
---

Developmental biology asks how a single cell becomes an animal. The answer has
two halves. First **gametogenesis** makes the haploid sperm and egg, halving the
chromosome number so that fertilisation can restore it. Then the zygote divides,
rearranges itself into three germ layers, and those layers build every organ.
The frog, which spawns in every paddy field in Nepal during the monsoon, is the
standard animal for studying this because its eggs are large, transparent enough
to follow, and develop outside the mother.

::: key What the examiner asks from this unit
Two diagrams carry most of the marks: the **flow chart of spermatogenesis and
oogenesis with the chromosome number written at every stage**, and the
**sequence zygote → cleavage → blastula → gastrula** drawn in section. Add the
**germ-layer derivative table** and you have covered almost every question set
on this unit in the last ten years.
:::

## 7.1 Gametogenesis

::: definition Gametogenesis
Gametogenesis is the process by which diploid primordial germ cells in the gonad
are converted into haploid gametes. It is called **spermatogenesis** in the
testis and **oogenesis** in the ovary.
:::

Both processes pass through the same three phases.

1. **Multiplication phase.** Primordial germ cells in the germinal epithelium
   divide repeatedly by **mitosis** to give many spermatogonia or oogonia. All
   are diploid ($2n$).
2. **Growth phase.** One gonium enlarges and becomes a **primary spermatocyte**
   or **primary oocyte**, still $2n$. The growth is slight in the male but
   enormous in the female, because the oocyte stores yolk, RNA and organelles
   for the embryo.
3. **Maturation phase.** Two meiotic divisions halve the chromosome number.
   Meiosis I is reductional ($2n \to n$); meiosis II is equational.

In the male a fourth phase follows: **spermiogenesis**, in which the round
spermatid is remodelled into a motile sperm. Nothing corresponding happens in
the female.

```figure caption="Spermatogenesis and oogenesis compared, with the chromosome number of the frog ($2n = 26$) at every stage. One primary spermatocyte yields four sperms; one primary oocyte yields one ovum and three polar bodies."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon, FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.2, 4.6))
CYT = "#e7eff7"; EDGE = "#2c5f96"; NUC = "#41638a"; YLK = "#f2e3b0"; PB = "#d9c2e0"
ax.set_xlim(-6.6, 6.6); ax.set_ylim(-2.0, 10.8); ax.axis('off')
LX, RX = -3.75, 3.55

def cell(x, y, r, fc=CYT, nr=0.36):
    ax.add_patch(Circle((x, y), r, fc=fc, ec=EDGE, lw=1.0, zorder=4))
    ax.add_patch(Circle((x, y), r*nr, fc=NUC, ec='none', zorder=5))

def cap(x, y, t, fs=5.3):
    ax.text(x, y, t, ha='center', va='top', fontsize=fs, color=MUTED,
            linespacing=1.2, zorder=6)

def arr(x0, y0, x1, y1):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.9,
                                mutation_scale=8))

def phase(y, t):
    ax.add_patch(FancyBboxPatch((-1.32, y - 0.40), 2.64, 0.80,
                                boxstyle="round,pad=0,rounding_size=0.18",
                                fc="#eef2f6", ec="#c3ccd6", lw=0.7, zorder=3))
    ax.text(0, y, t, ha='center', va='center', fontsize=5.6, color=INK,
            linespacing=1.15, zorder=5)

ax.text(LX, 10.30, 'SPERMATOGENESIS  (testis)', ha='center', fontsize=6.5, color=INK)
ax.text(RX, 10.30, 'OOGENESIS  (ovary)', ha='center', fontsize=6.5, color=INK)

# ---- R1 multiplication ----
cell(LX, 9.15, 0.40); cap(LX, 8.62, 'spermatogonium  (2n = 26)')
cell(RX, 9.15, 0.40); cap(RX, 8.62, 'oogonium  (2n = 26)')
phase(9.15, 'Multiplication\n(mitosis)')
arr(LX, 8.28, LX, 7.75); arr(RX, 8.28, RX, 7.82)

# ---- R2 growth ----
cell(LX, 7.15, 0.55); cap(LX, 6.50, 'primary spermatocyte  (2n = 26)')
ax.add_patch(Circle((RX, 6.95), 0.80, fc=YLK, ec=EDGE, lw=1.0, zorder=4))
ax.add_patch(Circle((RX, 6.95), 0.29, fc=NUC, ec='none', zorder=5))
cap(RX, 6.05, 'primary oocyte  (2n = 26),\nyolk now stored')
phase(7.05, 'Growth')
arr(LX, 6.18, LX, 5.62); arr(RX, 5.48, RX, 4.92)

# ---- R3 meiosis I ----
for x in (LX - 0.95, LX + 0.95):
    cell(x, 5.10, 0.44)
cap(LX, 4.52, 'two secondary spermatocytes\n(n = 13 each)')
ax.add_patch(Circle((RX, 4.10), 0.72, fc=YLK, ec=EDGE, lw=1.0, zorder=4))
ax.add_patch(Circle((RX, 4.10), 0.26, fc=NUC, ec='none', zorder=5))
ax.add_patch(Circle((4.66, 4.66), 0.20, fc=PB, ec=EDGE, lw=0.8, zorder=5))
ax.annotate('first polar\nbody  n = 13', xy=(4.86, 4.66), xytext=(5.72, 4.90),
            fontsize=5.0, color=MUTED, ha='center', va='center', linespacing=1.2,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
cap(RX, 3.30, 'secondary oocyte  (n = 13)')
phase(4.60, 'Maturation:\nmeiosis I')
for x in (LX - 0.95, LX + 0.95):
    arr(x, 4.08, x - 0.55, 3.45); arr(x, 4.08, x + 0.55, 3.45)
arr(RX, 2.98, RX, 2.45)

# ---- R4 meiosis II ----
for x in (LX - 1.65, LX - 0.55, LX + 0.55, LX + 1.65):
    cell(x, 3.00, 0.34)
cap(LX, 2.50, 'four spermatids  (n = 13 each)')
ax.add_patch(Circle((RX, 1.72, ), 0.68, fc=YLK, ec=EDGE, lw=1.0, zorder=4))
ax.add_patch(Circle((RX, 1.72), 0.25, fc=NUC, ec='none', zorder=5))
ax.add_patch(Circle((4.52, 2.24), 0.18, fc=PB, ec=EDGE, lw=0.8, zorder=5))
ax.annotate('second polar\nbody  n = 13', xy=(4.70, 2.24), xytext=(5.66, 2.36),
            fontsize=5.0, color=MUTED, ha='center', va='center', linespacing=1.2,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
cap(RX, 0.95, 'ootid  (n = 13)')
phase(1.90, 'Maturation:\nmeiosis II')
arr(LX, 2.18, LX, 1.72); arr(RX, 0.62, RX, 0.14)

# ---- R5 differentiation ----
def sperm(x, y, s=1.0):
    ax.add_patch(Ellipse((x, y), 0.30*s, 0.22*s, fc=NUC, ec='none', zorder=5))
    t = np.linspace(0, 1, 60)
    ax.plot(x - 0.15*s - 0.72*s*t, y + 0.11*s*np.sin(10*t), color=EDGE,
            lw=0.9, zorder=4)

for x in (LX - 1.65, LX - 0.55, LX + 0.55, LX + 1.65):
    sperm(x, 1.22)
cap(LX, 0.80, 'four functional spermatozoa')
ax.add_patch(Circle((RX, -0.62), 0.72, fc=YLK, ec=EDGE, lw=1.0, zorder=4))
ax.add_patch(Circle((RX, -0.62), 0.26, fc=NUC, ec='none', zorder=5))
ax.add_patch(Circle((RX, -0.62), 0.86, fc='none', ec=EDGE, lw=0.7,
                    ls=(0, (3, 2)), zorder=4))
for px, py in [(4.72, 0.02), (5.24, 0.46), (4.60, 0.62)]:
    ax.add_patch(Circle((px, py), 0.17, fc=PB, ec=EDGE, lw=0.7, zorder=5))
ax.text(5.74, -0.62, 'three polar\nbodies —\nall degenerate', ha='center',
        va='center', fontsize=5.0, color=MUTED, linespacing=1.25)
cap(RX, -1.44, 'one functional ovum')
phase(-0.62, 'Differentiation\n(spermiogenesis)')
ax.text(0, -1.62, 'no equivalent stage\nin the female', ha='center', va='center',
        fontsize=5.2, color=MUTED, linespacing=1.2)
```
| Feature | Spermatogenesis | Oogenesis |
|---|---|---|
| Site | seminiferous tubules of the testis | ovary |
| Begins at | puberty, and continues for life | in the foetus; arrested, resumed at puberty |
| Growth phase | slight | enormous — yolk is stored |
| Cytokinesis in meiosis | equal | unequal — polar bodies are tiny |
| Products per primary cell | 4 functional sperms | 1 functional ovum + 3 polar bodies |
| Extra phase | spermiogenesis | none |
| Product | small, motile, almost no cytoplasm | large, non-motile, full of cytoplasm and yolk |
| Completion of meiosis II | before release | only after the sperm enters |

::: caution The maths of meiosis is not symmetrical
Both sexes carry out exactly two meiotic divisions, so both produce four haploid
nuclei from one primary cell. The difference is the **cytoplasm**: in oogenesis
all of it goes to one cell, and the other three nuclei are pinched off as polar
bodies with almost no cytoplasm. Polar bodies cannot be fertilised and soon
degenerate.
:::

::: example Worked example 7.1 — chromosomes and DNA through meiosis
**Problem.** The frog *Rana tigrina* has $2n = 26$. For a primary spermatocyte
about to begin meiosis, state (a) the number of chromosomes and the number of
chromatids at the start of prophase I, (b) the number of chromosomes and
chromatids in each secondary spermatocyte, and (c) in each spermatid. (d) If the
nucleus of a spermatogonium contains $6.0\ \text{pg}$ of DNA in G₁, how much DNA
is in one sperm nucleus?

**Solution.**

(a) DNA has already been replicated in the S phase, so there are still
**26 chromosomes**, but each has two chromatids:

$$ 26 \times 2 = 52\ \text{chromatids} $$

(b) Meiosis I separates the homologous pairs. Each secondary spermatocyte gets
**13 chromosomes**, each still two-chromatid, so $13 \times 2 = 26$ chromatids.

(c) Meiosis II separates the sister chromatids, so each spermatid has
**13 chromosomes of one chromatid each** — 13 chromatids.

(d) A sperm is haploid and unreplicated, so it carries half the G₁ amount:

$$ \frac{6.0\ \text{pg}}{2} = 3.0\ \text{pg} $$

Fertilisation adds the egg's $3.0\ \text{pg}$ and restores the zygote to
$6.0\ \text{pg}$ and to $2n = 26$.
:::

::: example Worked example 7.2 — how many gametes?
**Problem.** A frog's testis contains 500 primary spermatocytes and its ovary
600 primary oocytes, all of which complete gametogenesis. (a) How many sperms
and how many ova are formed? (b) How many polar bodies? (c) What percentage of
the haploid nuclei produced in the ovary can actually be fertilised?

**Solution.**

(a) Each primary spermatocyte gives 4 sperms:

$$ 500 \times 4 = 2000\ \text{spermatozoa} $$

Each primary oocyte gives only 1 ovum:

$$ 600 \times 1 = 600\ \text{ova} $$

(b) Each primary oocyte also gives 3 polar bodies:

$$ 600 \times 3 = 1800\ \text{polar bodies} $$

(c) Each oocyte produces 4 haploid nuclei in all, of which 1 is usable:

$$ \frac{1}{4}\times 100 = 25\% $$

The male converts 100% of his meiotic products into gametes, the female only
25% — but each of her gametes is stocked with the food and machinery for the
first days of development.
:::

### The gametes themselves

```figure caption="A mature spermatozoon and a mature frog ovum, drawn in section. Note the scale: the egg is about a thousand times the volume of the sperm."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon, Wedge
fig, axes = plt.subplots(1, 2, figsize=(5.2, 3.2), gridspec_kw=dict(wspace=0.05))
EDGE = "#2c5f96"; NUC = "#2b3440"; ACR = "#cfe0d2"; MIT = "#f7dfc8"; MITE = "#b5832f"
ANIM = "#4a4a55"; VEG = "#f2e3b0"; JEL = "#dfe9f3"
WB = dict(fc='white', ec='none', pad=0.4)

# ---------------- (a) spermatozoon ----------------
ax = axes[0]
ax.set_xlim(-1.0, 13.0); ax.set_ylim(-5.4, 5.4); ax.axis('off')
ax.add_patch(Wedge((2.0, 0), 1.85, 90, 270, width=0.55, fc=ACR, ec=EDGE, lw=0.9, zorder=5))
ax.add_patch(Ellipse((2.3, 0), 3.4, 3.4, fc="#8e96a5", ec=EDGE, lw=0.9, zorder=4))
ax.add_patch(Ellipse((2.45, 0), 2.6, 2.6, fc=NUC, ec='none', zorder=5))
ax.add_patch(Polygon([[4.0, 0.62], [5.0, 0.55], [5.0, -0.55], [4.0, -0.62]],
                     closed=True, fc="#c3ccd6", ec=EDGE, lw=0.8, zorder=4))
for x in (4.25, 4.75):
    ax.add_patch(Ellipse((x, 0), 0.22, 0.75, fc=EDGE, ec='none', zorder=6))
ax.add_patch(Polygon([[5.0, 0.55], [7.6, 0.45], [7.6, -0.45], [5.0, -0.55]],
                     closed=True, fc=MIT, ec=EDGE, lw=0.8, zorder=4))
t = np.linspace(0, 1, 200)
ax.plot(5.0 + 2.6*t, 0.40*np.sin(15*t), color=MITE, lw=1.4, zorder=6)
ax.plot([5.0, 12.4], [0, 0], color=EDGE, lw=0.8, zorder=3)
tt = np.linspace(0, 1, 300)
ax.plot(7.6 + 4.8*tt, 0.95*np.sin(7.5*tt)*(0.35 + 0.65*tt), color=EDGE,
        lw=1.3, zorder=4)
for t2, xy, xt in [('acrosome', (1.25, 1.15), (0.5, 4.5)),
                   ('nucleus (n)', (2.45, -0.9), (2.2, -4.3)),
                   ('centrioles', (4.5, 0.55), (5.2, 4.5)),
                   ('mitochondrial spiral', (6.3, 0.42), (7.8, -4.3)),
                   ('axial filament', (9.2, -0.55), (10.4, 4.5))]:
    ax.annotate(t2, xy=xy, xytext=xt, fontsize=6.0, color=MUTED, ha='center',
                bbox=WB, zorder=10,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.65))
for x0, x1, t2 in [(0.15, 4.05, 'head'), (4.05, 5.05, 'neck'),
                   (5.05, 7.65, 'middle\npiece'), (7.65, 12.5, 'tail')]:
    ax.annotate('', xy=(x0, 2.45), xytext=(x1, 2.45),
                arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=0.7, mutation_scale=6))
    ax.text((x0 + x1)/2, 2.62, t2, ha='center', va='bottom', fontsize=6.0,
            color=INK, linespacing=1.1)
ax.text(6.0, -5.2, '(a) spermatozoon', ha='center', fontsize=7.0, color=INK)

# ---------------- (b) frog ovum ----------------
ax = axes[1]
ax.set_xlim(-6.5, 6.5); ax.set_ylim(-5.4, 5.6); ax.set_aspect('equal'); ax.axis('off')
for r, a in [(3.75, 0.30), (3.42, 0.45), (3.14, 0.60)]:
    ax.add_patch(Circle((0, 0.35), r, fc=JEL, ec="#9db6cc", lw=0.8, alpha=a, zorder=2))
ax.add_patch(Circle((0, 0.35), 2.85, fc=VEG, ec=EDGE, lw=1.1, zorder=3))
ax.add_patch(Wedge((0, 0.35), 2.85, 18, 162, fc=ANIM, ec=EDGE, lw=1.1, zorder=4))
ax.add_patch(Circle((0, 1.85), 0.44, fc="#e7eff7", ec=EDGE, lw=0.9, zorder=6))
ax.add_patch(Circle((0, 1.85), 0.17, fc="#2c5f96", ec='none', zorder=7))
rng = np.random.default_rng(4)
for _ in range(44):
    a = np.pi + np.pi*rng.random(); q = 2.60*np.sqrt(rng.random())
    px, py = q*np.cos(a), 0.35 + q*np.sin(a)
    ax.add_patch(Circle((px, py), 0.12 + 0.08*rng.random(), fc="#d9c37a",
                        ec='none', zorder=5))
ax.plot([0, 0], [-3.0, 3.7], color=MUTED, lw=0.7, ls=(0, (3, 2)), zorder=8)
for t2, xy, xt in [('jelly coats', (2.42, 2.55), (4.35, 4.55)),
                   ('vitelline membrane', (-2.05, 2.05), (-4.35, 4.35)),
                   ('animal pole:\npigmented', (-1.75, 1.25), (-4.75, 1.15)),
                   ('nucleus', (0.38, 2.00), (2.55, 3.85)),
                   ('vegetal pole:\nyolk granules', (1.45, -1.35), (4.55, -2.30))]:
    ax.annotate(t2, xy=xy, xytext=xt, fontsize=6.0, color=MUTED, ha='center',
                linespacing=1.2, bbox=WB, zorder=10,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.65))
ax.text(0, -5.2, '(b) mature frog ovum', ha='center', fontsize=7.0, color=INK)
```
The frog's egg is **mesolecithal** (a moderate amount of yolk) and
**telolecithal** (the yolk is pushed to one pole). Its dark, pigmented
**animal pole** holds the nucleus and most of the cytoplasm; the pale
**vegetal pole** holds the yolk. Egg types are classified on exactly these two
features — how much yolk, and where it lies.

| Type (amount of yolk) | Distribution | Diameter | Example |
|---|---|---|---|
| Alecithal | no yolk | ~0.1 mm | eutherian mammals, human |
| Microlecithal | little, evenly spread (isolecithal) | 0.1–0.2 mm | *Amphioxus*, sea urchin |
| Mesolecithal | moderate, at one pole (telolecithal) | 1.5–2.0 mm | **frog**, lungfish |
| Macrolecithal | very large, at one pole (telolecithal) | 25–30 mm | hen, reptiles, birds |
| Centrolecithal | yolk in the centre | ~0.5 mm | insects, other arthropods |

## 7.2 Development of frog

The common Nepali frog *Rana tigrina* (now *Hoplobatrachus tigerinus*) breeds
in the monsoon. The male clasps the female in **amplexus**; she sheds 2,500–3,000
eggs into the water and he sheds sperm over them at once, so fertilisation is
**external**. The eggs float in a mass of swollen jelly that protects them and
absorbs heat from the sun.

### Fertilisation

```figure caption="Fertilisation in the frog. The grey crescent appears opposite the point of sperm entry and marks the future dorsal side of the tadpole."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Wedge, Polygon
fig, axes = plt.subplots(1, 3, figsize=(5.2, 3.2), gridspec_kw=dict(wspace=0.06))
EDGE = "#2c5f96"; ANIM = "#4a4a55"; VEG = "#f2e3b0"; GREY = "#a9b0bb"; PN = "#2b3440"
WB = dict(fc='white', ec='none', pad=0.4)
R = 2.7; CY = 0.30

def egg(ax, crescent=False):
    ax.add_patch(Circle((0, CY), R, fc=VEG, ec=EDGE, lw=1.1, zorder=3))
    ax.add_patch(Wedge((0, CY), R, 15, 165, fc=ANIM, ec=EDGE, lw=1.1, zorder=4))
    if crescent:
        ax.add_patch(Wedge((0, CY), R, 158, 205, width=0.66, fc=GREY,
                           ec=EDGE, lw=0.8, zorder=5))

def sperm(ax, x, y, ang, s=0.85, col=None):
    col = col or PN
    r = np.radians(ang)
    ax.add_patch(Ellipse((x, y), 0.40*s, 0.24*s, angle=ang, fc=col, ec='none', zorder=6))
    t = np.linspace(0, 1, 50)
    px = x - (0.20*s + 1.05*s*t)*np.cos(r) - 0.15*s*np.sin(11*t)*np.sin(r)
    py = y - (0.20*s + 1.05*s*t)*np.sin(r) + 0.15*s*np.sin(11*t)*np.cos(r)
    ax.plot(px, py, color=col, lw=0.8, zorder=6)

for ax in axes:
    ax.set_xlim(-5.0, 5.0); ax.set_ylim(-6.5, 6.0)
    ax.set_aspect('equal'); ax.axis('off')

# ---------------- (a) sperm entry ----------------
ax = axes[0]
egg(ax)
for a in (18, 42, 66, 88):
    ax_r = np.radians(a)
    sperm(ax, 3.55*np.cos(ax_r), CY + 3.55*np.sin(ax_r), a + 180, col=EDGE)
sr = np.radians(62)
sperm(ax, (R - 0.22)*np.cos(sr), CY + (R - 0.22)*np.sin(sr), 242, col="#e7eff7")
ax.annotate('point of\nsperm entry', xy=(1.05, CY + 2.25), xytext=(-2.95, 4.55),
            fontsize=5.8, color=MUTED, ha='center', va='center', linespacing=1.2,
            bbox=WB, arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.text(0, -3.35, 'only one sperm\nenters (monospermy)', ha='center', va='top',
        fontsize=5.8, color=MUTED, linespacing=1.2)
ax.text(0, -6.1, '(a) sperm entry', ha='center', va='bottom', fontsize=6.8, color=INK)

# ---------------- (b) grey crescent ----------------
ax = axes[1]
ax.add_patch(Circle((0, CY), R + 0.62, fc='none', ec=EDGE, lw=1.0,
                    ls=(0, (4, 2)), zorder=6))
egg(ax, crescent=True)
ax.annotate('fertilisation\nmembrane', xy=(2.35, CY + 2.35), xytext=(3.05, 4.85),
            fontsize=5.8, color=MUTED, ha='center', va='center', linespacing=1.2,
            bbox=WB, arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.annotate('grey crescent =\nfuture dorsal side', xy=(-2.45, CY + 0.72),
            xytext=(0.0, -3.95), fontsize=5.8, color=MUTED, ha='center', va='center',
            linespacing=1.2, bbox=WB,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.text(0, -6.1, '(b) grey crescent forms', ha='center', va='bottom',
        fontsize=6.8, color=INK)

# ---------------- (c) pronuclei fuse ----------------
ax = axes[2]
egg(ax, crescent=True)
ax.add_patch(Circle((-0.58, CY + 1.05), 0.52, fc="#dfe9f3", ec=EDGE, lw=0.9, zorder=7))
ax.add_patch(Circle((0.58, CY + 1.05), 0.52, fc="#f6ddd6", ec="#a8433c", lw=0.9, zorder=7))
ax.annotate('', xy=(0.04, CY + 1.05), xytext=(-0.80, CY + 1.05),
            arrowprops=dict(arrowstyle='-|>', color='#c0392b', lw=0.9, mutation_scale=7))
ax.annotate('', xy=(-0.04, CY + 1.05), xytext=(0.80, CY + 1.05),
            arrowprops=dict(arrowstyle='-|>', color='#c0392b', lw=0.9, mutation_scale=7))
ax.annotate('female\npronucleus\nn = 13', xy=(-1.02, CY + 1.42), xytext=(-3.20, 4.20),
            fontsize=5.6, color=MUTED, ha='center', va='center', linespacing=1.25,
            bbox=WB, arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.annotate('male\npronucleus\nn = 13', xy=(1.02, CY + 1.42), xytext=(3.20, 4.20),
            fontsize=5.6, color=MUTED, ha='center', va='center', linespacing=1.25,
            bbox=WB, arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.text(0, -3.35, 'zygote:  2n = 26', ha='center', va='top', fontsize=6.2, color=INK)
ax.text(0, -6.1, '(c) fusion of pronuclei', ha='center', va='bottom',
        fontsize=6.8, color=INK)
```
The moment a sperm touches the vitelline membrane, the egg reacts. Cortical
granules burst and the vitelline membrane lifts away from the surface as the
**fertilisation membrane**, which no second sperm can cross — so fertilisation
is **monospermic**. The pigmented cortex then rotates about 30° towards the
point of entry, uncovering a pale crescent of cytoplasm on the *opposite* side:
the **grey crescent**. This is the single most important landmark in the egg,
because it becomes the dorsal lip of the blastopore and so fixes the dorsal
surface and the whole body axis. Finally the male pronucleus ($n = 13$) fuses
with the female pronucleus ($n = 13$) to make a diploid zygote ($2n = 26$) —
**amphimixis**.

### Cleavage

::: definition Cleavage
Cleavage is the rapid series of mitotic divisions that converts the zygote into
a many-celled blastula. There is **no growth phase** between divisions, so the
cells, called **blastomeres**, get smaller at every step while the embryo as a
whole stays the same size.
:::

The amount and position of yolk decide how an egg cleaves, because yolk resists
the cleavage furrow.

```figure caption="Types of cleavage. Yolk (pale) obstructs the furrow, so the more yolk an egg has, the less completely it divides."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, Polygon, Ellipse
fig, axes = plt.subplots(1, 4, figsize=(5.2, 2.9), gridspec_kw=dict(wspace=0.05))
EDGE = "#2c5f96"; CYTO = "#dfe9f3"; VEG = "#f2e3b0"; ANIM = "#b9c6d6"
for ax in axes:
    ax.set_xlim(-1.5, 1.5); ax.set_ylim(-2.95, 1.55)
    ax.set_aspect('equal'); ax.axis('off')

def segment(ax, R, a0, a1, fc):
    th = np.linspace(np.radians(a1), np.radians(a0), 70)
    ax.add_patch(Polygon(np.column_stack([R*np.cos(th), R*np.sin(th)]),
                         closed=True, fc=fc, ec=EDGE, lw=1.0, zorder=4))

def lab(ax, t, s):
    ax.text(0, -1.22, t, ha='center', va='top', fontsize=6.2, color=INK,
            linespacing=1.2)
    ax.text(0, -2.05, s, ha='center', va='top', fontsize=5.3, color=MUTED,
            linespacing=1.25)

# (a) holoblastic equal
ax = axes[0]
ax.add_patch(Circle((0, 0), 1.05, fc=CYTO, ec=EDGE, lw=1.0))
ax.plot([0, 0], [-1.05, 1.05], color=EDGE, lw=1.0)
ax.plot([-1.05, 1.05], [0, 0], color=EDGE, lw=1.0)
lab(ax, '(a) holoblastic\nequal', 'microlecithal —\n$Amphioxus$')

# (b) holoblastic unequal
ax = axes[1]
ax.add_patch(Circle((0, 0), 1.05, fc=VEG, ec=EDGE, lw=1.0))
ax.add_patch(Wedge((0, 0), 1.05, 22, 158, fc=ANIM, ec=EDGE, lw=1.0))
ax.plot([0, 0], [-1.05, 1.05], color=EDGE, lw=1.0)
ax.plot([-0.97, 0.97], [0.40, 0.40], color=EDGE, lw=1.0)
ax.text(0.55, 0.68, 'micro', ha='center', fontsize=4.6, color=INK)
ax.text(0.56, -0.62, 'macro', ha='center', fontsize=4.6, color=INK)
lab(ax, '(b) holoblastic\nunequal', 'mesolecithal —\nfrog')

# (c) meroblastic discoidal
ax = axes[2]
ax.add_patch(Circle((0, 0), 1.05, fc=VEG, ec=EDGE, lw=1.0))
segment(ax, 1.05, 34, 146, "#9fb6cf")
for x in (-0.38, 0.0, 0.38):
    ax.plot([x, x], [0.60, 1.02], color=EDGE, lw=0.9, zorder=5)
ax.annotate('blastodisc', xy=(-0.19, 0.78), xytext=(0, 1.42), fontsize=5.0,
            color=MUTED, ha='center',
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.text(0, -0.55, 'yolk', ha='center', fontsize=5.0, color=INK)
lab(ax, '(c) meroblastic\ndiscoidal', 'macrolecithal —\nhen, reptile')

# (d) superficial
ax = axes[3]
ax.add_patch(Circle((0, 0), 1.05, fc=ANIM, ec=EDGE, lw=1.0))
ax.add_patch(Circle((0, 0), 0.62, fc=VEG, ec=EDGE, lw=1.0))
for a in np.linspace(0, 2*np.pi, 15)[:-1]:
    ax.plot([0.62*np.cos(a), 1.05*np.cos(a)], [0.62*np.sin(a), 1.05*np.sin(a)],
            color=EDGE, lw=0.8)
ax.text(0, -0.08, 'yolk', ha='center', fontsize=5.0, color=INK)
lab(ax, '(d) superficial', 'centrolecithal —\ninsects')
```
In the frog the cleavage is **holoblastic** (the furrow cuts right through) but
**unequal** (the yolky vegetal cells end up larger).

| Division | Plane | Result |
|---|---|---|
| First (about 1 hour after fertilisation) | vertical (meridional), through both poles, bisecting the grey crescent | 2 equal blastomeres |
| Second | vertical, at right angles to the first | 4 equal blastomeres |
| Third | horizontal (latitudinal), **above** the equator | 4 small micromeres + 4 large macromeres |
| Fourth | two vertical furrows | 16 cells |
| Fifth | two horizontal furrows | 32 cells, then a solid **morula** |

```figure caption="Cleavage in the frog, seen from the side with the animal pole uppermost. The third furrow is horizontal and lies above the equator, so the micromeres are smaller than the macromeres."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, Polygon
fig, axes = plt.subplots(1, 5, figsize=(5.2, 2.5), gridspec_kw=dict(wspace=0.04))
EDGE = "#2c5f96"; ANIM = "#6c7180"; VEG = "#f2e3b0"
R = 1.05

def base(ax):
    ax.set_xlim(-1.45, 1.45); ax.set_ylim(-2.35, 1.35)
    ax.set_aspect('equal'); ax.axis('off')
    ax.add_patch(Circle((0, 0), R, fc=VEG, ec=EDGE, lw=1.0, zorder=3))
    ax.add_patch(Wedge((0, 0), R, 18, 162, fc=ANIM, ec=EDGE, lw=1.0, zorder=4))

def lab(ax, t, s=''):
    ax.text(0, -1.28, t, ha='center', va='top', fontsize=6.3, color=INK)
    if s:
        ax.text(0, -1.63, s, ha='center', va='top', fontsize=5.2, color=MUTED,
                linespacing=1.25)

def vline(ax, x=0.0):
    y = np.sqrt(max(R**2 - x**2, 0))
    ax.plot([x, x], [-y, y], color=EDGE, lw=1.0, zorder=6)

def hline(ax, y):
    x = np.sqrt(max(R**2 - y**2, 0))
    ax.plot([-x, x], [y, y], color=EDGE, lw=1.0, zorder=6)

def frontplane(ax, w=0.46):
    """Second (vertical) furrow at 90 deg, seen as the near half of a plane."""
    t = np.linspace(-np.pi/2, np.pi/2, 60)
    ax.plot(w*np.cos(t), R*np.sin(t), color=EDGE, lw=1.0, zorder=6)

ax = axes[0]; base(ax); vline(ax, 0.0)
lab(ax, '2-cell', 'first furrow:\nvertical')

ax = axes[1]; base(ax); vline(ax, 0.0); frontplane(ax)
lab(ax, '4-cell', 'second furrow:\nvertical, at 90°')

ax = axes[2]; base(ax); vline(ax, 0.0); frontplane(ax); hline(ax, 0.40)
lab(ax, '8-cell', '4 micromeres +\n4 macromeres')

ax = axes[3]; base(ax)
vline(ax, -0.52); vline(ax, 0.0); vline(ax, 0.52); hline(ax, 0.40)
lab(ax, '16-cell', 'two more\nvertical furrows')

ax = axes[4]; base(ax)
vline(ax, -0.52); vline(ax, 0.0); vline(ax, 0.52)
hline(ax, 0.66); hline(ax, 0.40); hline(ax, -0.34)
lab(ax, 'morula', 'solid ball of\nblastomeres')
```
::: example Worked example 7.3 — cell number and cell size during cleavage
**Problem.** A frog's egg is a sphere of diameter $1.8\ \text{mm}$. Assume the
first seven cleavages are synchronous and that the embryo does not change in
total volume. (a) How many blastomeres are present after the 7th cleavage?
(b) What is the average diameter of one blastomere then? (c) Explain why the
answer to (b) shows that cleavage is division without growth.

**Solution.**

(a) Each cleavage doubles the number of cells, so after $n$ cleavages there are
$2^{n}$ cells:

$$ 2^{7} = 128\ \text{blastomeres} $$

(b) The total volume is unchanged, so each blastomere has $1/128$ of the
original volume. For spheres, volume $\propto d^{3}$, so

$$ \frac{d_{\text{cell}}}{d_{\text{egg}}} = \left(\frac{1}{128}\right)^{1/3}
= \frac{1}{5.04} $$
$$ d_{\text{cell}} = \frac{1.8\ \text{mm}}{5.04} = 0.357\ \text{mm}
\approx 0.36\ \text{mm} $$

(c) The number of cells has gone up 128-fold but the embryo is still
$1.8\ \text{mm}$ across, so no new material has been made — the same cytoplasm
has simply been partitioned into smaller boxes. The nucleus-to-cytoplasm ratio
rises towards the normal value of a body cell, which is the point of cleavage.
:::

### Blastula

```figure caption="V.S. of the frog blastula (coeloblastula). The blastocoel is eccentric — pushed into the animal half by the bulky yolk-laden macromeres."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, Polygon, Ellipse
fig, ax = plt.subplots(figsize=(5.0, 3.2))
EDGE = "#2c5f96"; ANIM = "#8e94a3"; VEG = "#f2e3b0"; CAV = "#ffffff"
WB = dict(fc='white', ec='none', pad=0.5)
ax.set_xlim(-8.2, 8.2); ax.set_ylim(-4.6, 4.9); ax.set_aspect('equal'); ax.axis('off')

R = 3.6
ax.add_patch(Circle((0, 0), R, fc="#f8f4e6", ec=EDGE, lw=1.2, zorder=3))
# micromere roof (animal hemisphere, small cells in two layers)
for rr, n, off in [(R - 0.32, 26, 0.0), (R - 0.92, 20, 0.08)]:
    for a in np.linspace(np.radians(8), np.radians(172), n):
        ax.add_patch(Ellipse((rr*np.cos(a + off), rr*np.sin(a + off)), 0.52, 0.40,
                             angle=np.degrees(a), fc=ANIM, ec=EDGE, lw=0.7, zorder=5))
# macromere floor (large yolky cells)
rng = np.random.default_rng(6)
for a, q in [(200, 0.74), (225, 0.80), (250, 0.72), (275, 0.78), (300, 0.74),
             (325, 0.80), (215, 0.40), (245, 0.36), (280, 0.34), (315, 0.40),
             (185, 0.76), (340, 0.76)]:
    r = np.radians(a)
    ax.add_patch(Circle((R*q*np.cos(r), R*q*np.sin(r)), 0.60, fc=VEG,
                        ec=EDGE, lw=0.8, zorder=5))
# blastocoel
ax.add_patch(Ellipse((0, 1.05), 4.0, 2.05, fc=CAV, ec=EDGE, lw=1.0, zorder=6))
ax.text(0, 1.05, 'blastocoel', ha='center', va='center', fontsize=6.4, color=INK,
        zorder=7)
for t, xy, xt in [('animal pole:\nsmall micromeres, 2 layers', (-2.4, 2.65), (-5.8, 4.1)),
                  ('vegetal pole:\nlarge yolky macromeres', (1.6, -2.6), (5.4, -3.6)),
                  ('roof of the blastocoel', (1.2, 2.65), (5.6, 3.6)),
                  ('floor of the blastocoel', (-1.25, 0.10), (-5.6, -2.9))]:
    ax.annotate(t, xy=xy, xytext=xt, fontsize=6.1, color=MUTED, ha='center',
                linespacing=1.2, bbox=WB, zorder=10,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.65))
ax.annotate('', xy=(0, R + 0.75), xytext=(0, -R - 0.75),
            arrowprops=dict(arrowstyle='<->', color=MUTED, lw=0.7, mutation_scale=6))
ax.text(0.30, R + 0.95, 'animal–vegetal axis', ha='center', fontsize=5.8, color=MUTED)
```

By about the 32-cell stage a fluid-filled cavity, the **blastocoel**, appears
among the blastomeres. The embryo is now a hollow ball — a **coeloblastula**.
Because the vegetal macromeres are swollen with yolk, the cavity is not central
but pushed up into the animal half; it is **eccentric**. Its roof is two layers
of small micromeres, its floor a thick mass of macromeres.

### Gastrulation

::: definition Gastrulation
Gastrulation is the set of coordinated cell movements that converts the
one-layered blastula into a three-layered **gastrula** with an **archenteron**
(the primitive gut) opening to the outside at the **blastopore**.
:::

Nothing new is made during gastrulation — cells simply move to where they will
be needed. Two movements do the work.

- **Epiboly.** The small animal micromeres divide fast and spread downwards as a
  sheet over the vegetal region, like a sock being pulled on. They become
  **ectoderm**.
- **Emboly.** Cells at the margin roll inwards over the lip of the blastopore
  (**involution**) and move forward inside. They become **mesoderm** and
  **endoderm**.

```figure caption="Gastrulation in the frog, in vertical section. The blastocoel is squeezed out as the archenteron grows; the vegetal cells left in the blastopore form the yolk plug."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Wedge, Polygon
fig, axes = plt.subplots(1, 3, figsize=(5.2, 3.1), gridspec_kw=dict(wspace=0.05))
EDGE = "#2c5f96"; ECTO = "#7ba4cd"; MESO = "#cf8b84"; ENDO = "#ecd9a0"
BODY = "#f7f0dc"; CAV = "#ffffff"
WB = dict(fc='white', ec='none', pad=0.35)
R = 2.45

def comma(ax, a0, a1, r0, r1, w0, w1, n=90):
    """Archenteron: a tapering channel running inward along an arc."""
    t = np.linspace(0, 1, n)
    ang = np.radians(a0 + (a1 - a0)*t)
    rad = r0 + (r1 - r0)*t
    w = w0 + (w1 - w0)*np.sin(np.pi*t)**0.6
    up = np.column_stack([(rad + w)*np.cos(ang), (rad + w)*np.sin(ang)])
    dn = np.column_stack([(rad - w)*np.cos(ang), (rad - w)*np.sin(ang)])
    ax.add_patch(Polygon(np.vstack([up, dn[::-1]]), closed=True, fc=CAV,
                         ec=EDGE, lw=0.9, zorder=8))

for ax in axes:
    ax.set_xlim(-3.6, 3.6); ax.set_ylim(-4.9, 3.9)
    ax.set_aspect('equal'); ax.axis('off')

def shell(ax, meso=False):
    ax.add_patch(Circle((0, 0), R, fc=BODY, ec=EDGE, lw=1.1, zorder=3))
    if meso:
        ax.add_patch(Wedge((0, 0), R - 0.16, 0, 360, width=0.22, fc=MESO,
                           ec='none', zorder=4))
    ax.add_patch(Wedge((0, 0), R, 0, 360, width=0.16, fc=ECTO, ec='none', zorder=5))
    ax.add_patch(Circle((0, 0), R, fc='none', ec=EDGE, lw=1.1, zorder=6))

def plug(ax, r=0.40):
    a = np.radians(202)
    ax.add_patch(Circle(((R - 0.10)*np.cos(a), (R - 0.10)*np.sin(a)), r,
                        fc=ENDO, ec=EDGE, lw=0.9, zorder=9))

def foot(ax, t):
    ax.text(0, -4.80, t, ha='center', va='bottom', fontsize=6.6, color=INK)

# ---------------- (a) early gastrula ----------------
ax = axes[0]
shell(ax)
ax.add_patch(Ellipse((0, 0.52), 3.10, 1.92, fc=CAV, ec=EDGE, lw=0.9, zorder=7))
ax.text(0, 0.52, 'blastocoel', ha='center', va='center', fontsize=5.6,
        color=INK, zorder=9)
comma(ax, 204, 186, R + 0.02, 1.62, 0.07, 0.13)
for a in (138, 158, 178):
    ax.annotate('', xy=(2.92*np.cos(np.radians(a - 20)), 2.92*np.sin(np.radians(a - 20))),
                xytext=(2.92*np.cos(np.radians(a)), 2.92*np.sin(np.radians(a))),
                arrowprops=dict(arrowstyle='-|>', color='#2e7d5b', lw=0.9,
                                mutation_scale=7, connectionstyle='arc3,rad=0.28'))
ax.annotate('epiboly', xy=(-2.72, 1.32), xytext=(-1.55, 3.35), fontsize=5.8,
            color='#2e7d5b', ha='center', bbox=WB, zorder=10,
            arrowprops=dict(arrowstyle='-', color='#2e7d5b', lw=0.6))
ax.annotate('dorsal lip of\nthe blastopore', xy=(-2.28, -0.92), xytext=(0.0, -3.70),
            fontsize=5.8, color=MUTED, ha='center', va='center', linespacing=1.2,
            bbox=WB, zorder=10, arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
foot(ax, '(a) early gastrula')

# ---------------- (b) mid gastrula ----------------
ax = axes[1]
shell(ax, meso=True)
comma(ax, 208, 74, R + 0.02, 1.22, 0.10, 0.40)
ax.add_patch(Ellipse((1.48, 0.42), 1.34, 0.94, fc=CAV, ec=EDGE, lw=0.9, zorder=7))
ax.text(1.48, 0.42, 'blastocoel', ha='center', va='center', fontsize=5.0,
        color=INK, zorder=9)
plug(ax, 0.42)
ax.annotate('archenteron', xy=(-0.62, 1.72), xytext=(-1.05, 3.35), fontsize=5.8,
            color=MUTED, ha='center', bbox=WB, zorder=11,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.annotate('yolk plug', xy=(-2.32, -1.18), xytext=(-0.90, -3.70), fontsize=5.8,
            color=MUTED, ha='center', bbox=WB, zorder=11,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.annotate('involution\n(emboly)', xy=(-2.50, -0.55), xytext=(1.95, -3.70),
            fontsize=5.8, color='#2e7d5b', ha='center', va='center', linespacing=1.2,
            bbox=WB, zorder=11,
            arrowprops=dict(arrowstyle='-', color='#2e7d5b', lw=0.6))
foot(ax, '(b) mid gastrula')

# ---------------- (c) late gastrula ----------------
ax = axes[2]
shell(ax, meso=True)
comma(ax, 208, 58, R + 0.02, 1.00, 0.13, 0.70)
plug(ax, 0.32)
ax.text(1.10, -0.85, 'endoderm', ha='center', fontsize=5.4, color=INK, zorder=10)
ax.annotate('ectoderm', xy=(1.92, 1.50), xytext=(2.35, 3.35), fontsize=5.8,
            color=MUTED, ha='center', bbox=WB, zorder=11,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.annotate('mesoderm', xy=(-1.48, 1.78), xytext=(-2.15, 3.35), fontsize=5.8,
            color=MUTED, ha='center', bbox=WB, zorder=11,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.annotate('archenteron', xy=(0.55, 1.22), xytext=(2.05, -3.70), fontsize=5.8,
            color=MUTED, ha='center', bbox=WB, zorder=11,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.annotate('yolk plug in the\ncircular blastopore', xy=(-2.36, -1.06),
            xytext=(-1.20, -3.70), fontsize=5.8, color=MUTED, ha='center',
            va='center', linespacing=1.2, bbox=WB, zorder=11,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
foot(ax, '(c) late gastrula')
```
The sequence is easy to remember if you follow the blastopore. A crescentic
groove appears just below the grey crescent — its upper edge is the **dorsal
lip**. Cells stream over it, so an inward pocket, the **archenteron**, grows
towards the animal pole and pushes the blastocoel aside until it disappears.
Lateral and then ventral lips form, so the blastopore becomes a complete ring
with a knob of pale yolky endoderm, the **yolk plug**, sticking out of it. At the
end the embryo has three layers: ectoderm outside, endoderm lining the
archenteron, and mesoderm squeezed between them.

::: key Spemann's organiser
The dorsal lip of the blastopore is the **primary organiser**. Hans Spemann and
Hilde Mangold showed in 1924 that grafting a dorsal lip from one newt gastrula
onto the belly of another makes the host grow a complete second embryo. The
dorsal lip comes from the grey crescent — which is why the grey crescent decides
the body axis.
:::

::: caution In the frog the blastopore becomes the anus
The frog is a **deuterostome** ("second mouth"): the blastopore of the gastrula
becomes the **anus**, and the mouth breaks through later at the opposite end.
Students routinely write the reverse. The blastopore becomes the mouth only in
protostomes such as earthworms and insects.
:::

### Neurulation and the three germ layers

```figure caption="Neurulation in transverse section. The notochord induces the ectoderm above it to fold into the neural tube; the mesoderm splits into somites and lateral plate."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon
fig, axes = plt.subplots(1, 3, figsize=(5.2, 2.7), gridspec_kw=dict(wspace=0.05))
EDGE = "#2c5f96"; ECTO = "#a9c6e2"; NEUR = "#3d6ea8"; MESO = "#cf8b84"
ENDO = "#ecd9a0"; NOTO = "#a8433c"; CAV = "#ffffff"
WB = dict(fc='white', ec='none', pad=0.35)
A, B = 2.35, 1.55                      # body half-width, half-height

def outline(ax):
    ax.add_patch(Ellipse((0, 0), 2*A, 2*B, fc=ECTO, ec=EDGE, lw=1.0, zorder=3))
    ax.add_patch(Ellipse((0, -0.34), 3.30, 1.72, fc=ENDO, ec=EDGE, lw=0.9, zorder=4))
    ax.add_patch(Ellipse((0, -0.34), 2.00, 0.86, fc=CAV, ec=EDGE, lw=0.8, zorder=5))
    ax.add_patch(Circle((0, 0.62), 0.24, fc=NOTO, ec=EDGE, lw=0.8, zorder=6))
    for sx in (-1, 1):
        ax.add_patch(Ellipse((sx*1.02, 0.52), 0.95, 0.42, fc=MESO, ec=EDGE,
                             lw=0.8, zorder=6))

def cap(x):
    """Point on the body outline at abscissa x."""
    return B*np.sqrt(max(1 - (x/A)**2, 0))

for ax in axes:
    ax.set_xlim(-3.1, 3.1); ax.set_ylim(-2.9, 2.85)
    ax.set_aspect('equal'); ax.axis('off')

# ---------- (a) neural plate ----------
ax = axes[0]
outline(ax)
xs = np.linspace(-1.05, 1.05, 40)
up = np.column_stack([xs, [cap(x) for x in xs]])
dn = np.column_stack([xs, [cap(x) - 0.30 for x in xs]])
ax.add_patch(Polygon(np.vstack([up, dn[::-1]]), closed=True, fc=NEUR, ec=EDGE,
                     lw=0.8, zorder=7))
ax.annotate('neural plate', xy=(-0.55, 1.28), xytext=(-1.45, 2.45), fontsize=5.6,
            color=MUTED, ha='center', bbox=WB, zorder=10,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.annotate('notochord', xy=(0.26, 0.62), xytext=(2.05, 2.45), fontsize=5.6,
            color=MUTED, ha='center', bbox=WB, zorder=10,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.annotate('archenteron', xy=(0.60, -0.34), xytext=(0.90, -2.20), fontsize=5.6,
            color=MUTED, ha='center', bbox=WB, zorder=10,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.text(0, -2.80, '(a) neural plate', ha='center', va='bottom', fontsize=6.6, color=INK)

# ---------- (b) neural groove and folds ----------
ax = axes[1]
outline(ax)
for s in (-1, 1):
    ax.add_patch(Polygon([[s*1.12, cap(1.12)], [s*0.86, 1.92], [s*0.28, 1.18],
                          [s*0.20, 0.90], [s*0.62, 0.88], [s*0.92, cap(0.92) - 0.28]],
                         closed=True, fc=NEUR, ec=EDGE, lw=0.8, zorder=7))
ax.annotate('neural fold', xy=(-0.86, 1.80), xytext=(-1.90, 2.45), fontsize=5.6,
            color=MUTED, ha='center', bbox=WB, zorder=10,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.annotate('neural groove', xy=(0.05, 1.32), xytext=(1.70, 2.45), fontsize=5.6,
            color=MUTED, ha='center', bbox=WB, zorder=10,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.annotate('mesoderm', xy=(-1.30, 0.52), xytext=(-1.95, -2.20), fontsize=5.6,
            color=MUTED, ha='center', bbox=WB, zorder=10,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.text(0, -2.80, '(b) neural groove', ha='center', va='bottom', fontsize=6.6, color=INK)

# ---------- (c) neural tube ----------
ax = axes[2]
outline(ax)
ax.add_patch(Ellipse((0, 1.06), 0.88, 0.70, fc=NEUR, ec=EDGE, lw=0.9, zorder=7))
ax.add_patch(Ellipse((0, 1.06), 0.36, 0.30, fc=CAV, ec=EDGE, lw=0.7, zorder=8))
for s in (-1, 1):
    ax.add_patch(Circle((s*0.62, 1.42), 0.14, fc="#6a5acd", ec=EDGE, lw=0.7, zorder=8))
ax.annotate('neural tube\n(with neurocoel)', xy=(-0.44, 1.06), xytext=(-1.75, 2.42),
            fontsize=5.4, color=MUTED, ha='center', va='center', linespacing=1.2,
            bbox=WB, zorder=10, arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.annotate('neural crest', xy=(0.70, 1.50), xytext=(1.95, 2.42), fontsize=5.4,
            color=MUTED, ha='center', bbox=WB, zorder=10,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.annotate('somite', xy=(1.10, 0.52), xytext=(2.10, -2.20), fontsize=5.4,
            color=MUTED, ha='center', bbox=WB, zorder=10,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.annotate('endoderm', xy=(-1.20, -0.55), xytext=(-1.85, -2.20), fontsize=5.4,
            color=MUTED, ha='center', bbox=WB, zorder=10,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.text(0, -2.80, '(c) neural tube', ha='center', va='bottom', fontsize=6.6, color=INK)
```

The roof of the archenteron rolls off as a solid rod, the **notochord**. It
induces the ectoderm directly above it to thicken into a **neural plate**. The
edges of the plate rise as **neural folds**, the middle sinks as a **neural
groove**, and the folds meet and fuse to make the hollow **neural tube** — the
future brain and spinal cord. Cells left at the join form the **neural crest**.
Meanwhile the mesoderm on each side splits into an upper **epimere** (somites →
muscles and vertebrae), a middle **mesomere** (→ kidney) and a lower
**hypomere**, whose cavity is the **coelom**.

| Germ layer | What it becomes |
|---|---|
| **Ectoderm** | epidermis and its glands; whole nervous system (brain, spinal cord, nerves); retina and lens of the eye; receptor cells of sense organs; lining of mouth and anus; enamel of teeth; adrenal medulla |
| **Mesoderm** | all three muscle types; bone and cartilage; dermis; notochord; blood, lymph, heart and blood vessels; kidneys and their ducts; gonads; peritoneum lining the coelom |
| **Endoderm** | epithelial lining of the alimentary canal (except mouth and anus); liver and pancreas; lining of the trachea, bronchi and lungs; thyroid, parathyroid and thymus; lining of the urinary bladder and the Eustachian tube |

::: memory Which layer made it?
**"Outside, inside, in between."** Anything on the outside or made of nerve is
**ectoderm**. Anything lining a tube that opens into the gut is **endoderm**.
Everything in between — muscle, bone, blood, kidney — is **mesoderm**.
:::

### Hatching and metamorphosis

```figure caption="Life history of the frog. The tadpole is a herbivore with gills and a tail; metamorphosis rebuilds it as a carnivore with lungs and legs."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon, Wedge
fig, axes = plt.subplots(1, 5, figsize=(5.2, 2.4), gridspec_kw=dict(wspace=0.04))
EDGE = "#2c5f96"; BODY = "#7f8798"; FIN = "#cfdcea"; VEG = "#f2e3b0"
for ax in axes:
    ax.set_xlim(-2.4, 2.4); ax.set_ylim(-3.05, 1.85)
    ax.set_aspect('equal'); ax.axis('off')

def lab(ax, t, s):
    ax.text(0, -1.30, t, ha='center', va='top', fontsize=6.0, color=INK)
    ax.text(0, -1.92, s, ha='center', va='top', fontsize=5.0, color=MUTED,
            linespacing=1.25)

def tadpole(ax, bw=1.25, bh=0.85, tl=1.85, fin=0.42, bx=-0.55):
    t = np.linspace(0, 1, 60)
    tipx = bx + bw/2 + tl
    xs = bx + bw/2 + tl*t
    hw = fin*np.sin(np.pi*t**0.8) + 0.10*(1 - t)
    ax.add_patch(Polygon(np.vstack([np.column_stack([xs, hw]),
                                    np.column_stack([xs[::-1], -hw[::-1]])]),
                         closed=True, fc=FIN, ec=EDGE, lw=0.7, zorder=3))
    ax.plot([bx + bw/2, tipx], [0, 0], color=EDGE, lw=1.6, zorder=4)
    ax.add_patch(Ellipse((bx, 0), bw, bh, fc=BODY, ec=EDGE, lw=0.9, zorder=5))
    ax.add_patch(Circle((bx - bw*0.26, bh*0.16), 0.10, fc='white', ec=EDGE,
                        lw=0.6, zorder=6))

# (1) fertilised egg in jelly
ax = axes[0]
ax.add_patch(Circle((0, 0), 1.18, fc="#dfe9f3", ec="#9db6cc", lw=0.8, alpha=0.55, zorder=2))
ax.add_patch(Circle((0, 0), 0.72, fc=VEG, ec=EDGE, lw=1.0, zorder=3))
ax.add_patch(Wedge((0, 0), 0.72, 15, 165, fc="#4a4a55", ec=EDGE, lw=1.0, zorder=4))
lab(ax, 'egg in jelly', 'fertilised;\nhatches in ~6 days')

# (2) early tadpole with external gills + sucker
ax = axes[1]
tadpole(ax, 1.05, 0.72, 1.70, 0.34, -0.60)
for k, a in enumerate((118, 92, 66)):
    r = np.radians(a)
    x0, y0 = -0.60 + 0.50*np.cos(r), 0.34*np.sin(r)
    tt = np.linspace(0, 1, 20)
    ax.plot(x0 + 0.42*tt*np.cos(r), y0 + 0.42*tt*np.sin(r) + 0.07*np.sin(9*tt),
            color="#c0392b", lw=0.9, zorder=7)
ax.add_patch(Ellipse((-1.12, -0.22), 0.22, 0.14, fc='white', ec=EDGE, lw=0.7, zorder=7))
ax.text(0, 1.30, 'external gills', ha='center', fontsize=5.0, color='#c0392b')
lab(ax, 'early tadpole', 'external gills,\nadhesive sucker')

# (3) tadpole with operculum
ax = axes[2]
tadpole(ax, 1.25, 0.85, 1.85, 0.42, -0.55)
ax.add_patch(Wedge((-0.55, 0), 0.62, 200, 160, width=0.10, fc='none',
                   ec="#a8433c", lw=1.0, zorder=7))
ax.plot([-0.98], [-0.20], marker='o', ms=2.2, color="#a8433c", zorder=8)
ax.text(0, 1.30, 'operculum + spiracle', ha='center', fontsize=5.0, color='#a8433c')
lab(ax, 'gilled tadpole', 'internal gills,\nherbivore, long gut')

# (4) tadpole with limbs
ax = axes[3]
tadpole(ax, 1.25, 0.85, 1.55, 0.36, -0.55)
for s in (-1, 1):
    ax.add_patch(Polygon([[0.16, s*0.16], [0.72, s*0.62], [1.02, s*0.46]],
                         closed=False, fc='none', ec=EDGE, lw=1.3, zorder=8))
    ax.plot([0.72, 1.02], [s*0.62, s*0.46], color=EDGE, lw=1.3, zorder=8)
    ax.add_patch(Polygon([[-1.02, s*0.12], [-1.38, s*0.50], [-1.16, s*0.66]],
                         closed=False, fc='none', ec=EDGE, lw=1.1, zorder=8))
ax.text(0, 1.30, 'lungs develop', ha='center', fontsize=5.0, color=MUTED)
lab(ax, 'limbed tadpole', 'hind limbs first,\nthen forelimbs')

# (5) froglet / adult
ax = axes[4]
ax.add_patch(Ellipse((0, 0), 1.75, 1.00, fc="#5f8f63", ec=EDGE, lw=1.0, zorder=5))
ax.add_patch(Ellipse((-0.98, 0.10), 0.72, 0.62, fc="#5f8f63", ec=EDGE, lw=1.0, zorder=6))
ax.add_patch(Circle((-1.12, 0.30), 0.12, fc='white', ec=EDGE, lw=0.6, zorder=7))
for s in (-1, 1):
    ax.plot([0.55, 1.15, 0.80], [s*0.28, s*0.78, s*0.95], color=EDGE, lw=1.3, zorder=7)
    ax.plot([-0.55, -0.95], [s*0.30, s*0.72], color=EDGE, lw=1.1, zorder=7)
ax.text(0, 1.30, 'tail resorbed', ha='center', fontsize=5.0, color=MUTED)
lab(ax, 'froglet → adult', 'carnivore, short gut,\nlungs and skin')
```

The tadpole hatches about six days after fertilisation. At first it has **external
gills**, an **adhesive sucker** and no mouth, and lives on its remaining yolk. A
mouth with horny jaws then opens; the tadpole becomes a **herbivore** with a long
coiled intestine, and a fold of skin, the **operculum**, grows back over
**internal gills**, leaving one opening, the **spiracle**, on the left side.
Hind limbs appear first, then forelimbs; lungs replace the gills; and the tail
and gills are digested away by lysosomal enzymes. The gut shortens as the animal
turns **carnivore**. From egg to froglet takes about two to three months.

```figure caption="Hormonal control of metamorphosis. Thyroxine drives the change; without iodine the tadpole never becomes a frog."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.6, 2.9))
ax.set_xlim(0, 10); ax.set_ylim(0, 10.4); ax.axis('off')
BOX = "#eef2f6"; BE = "#c3ccd6"

def box(x, y, w, h, t, fc=BOX, fs=6.2):
    ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h,
                                boxstyle="round,pad=0,rounding_size=0.22",
                                fc=fc, ec=BE, lw=0.8, zorder=4))
    ax.text(x, y, t, ha='center', va='center', fontsize=fs, color=INK,
            linespacing=1.2, zorder=5)

def arrow(y0, y1, lab, col=ACCENT):
    ax.annotate('', xy=(3.9, y1), xytext=(3.9, y0),
                arrowprops=dict(arrowstyle='-|>', color=col, lw=1.1, mutation_scale=9))
    ax.text(4.25, (y0 + y1)/2, lab, ha='left', va='center', fontsize=5.8, color=col)

box(3.9, 9.5, 5.0, 1.15, 'Hypothalamus')
arrow(8.93, 8.07, 'TRH')
box(3.9, 7.5, 5.0, 1.15, 'Anterior pituitary')
arrow(6.93, 6.07, 'TSH')
box(3.9, 5.5, 5.0, 1.15, 'Thyroid gland')
arrow(4.93, 4.07, 'thyroxine  (T₄, T₃)')
box(3.9, 3.5, 5.0, 1.15, 'Tadpole tissues')
ax.annotate('', xy=(3.9, 2.07), xytext=(3.9, 2.93),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.1, mutation_scale=9))
box(3.9, 1.5, 6.4, 1.45,
    'METAMORPHOSIS\ntail resorbed, limbs grow, gut shortens', fc="#e3efe6", fs=6.0)
ax.annotate('iodine from\nthe water', xy=(6.45, 5.5), xytext=(8.6, 6.9),
            fontsize=5.8, color='#8a6d1f', ha='center', va='center', linespacing=1.2,
            arrowprops=dict(arrowstyle='-|>', color='#8a6d1f', lw=0.9, mutation_scale=7))
ax.annotate('no iodine or no thyroid\n→ permanent giant tadpole', xy=(6.45, 3.9),
            xytext=(8.4, 2.6), fontsize=5.8, color='#a8433c', ha='center',
            va='center', linespacing=1.2,
            arrowprops=dict(arrowstyle='-', color='#a8433c', lw=0.7))
ax.annotate('prolactin\nopposes', xy=(3.72, 4.50), xytext=(1.05, 4.50),
            fontsize=5.6, color='#6a5acd', ha='center', va='center', linespacing=1.2,
            arrowprops=dict(arrowstyle='-[,widthB=0.22', color='#6a5acd', lw=0.9))
```

Metamorphosis is driven by **thyroxine** from the thyroid gland, which needs
**iodine** to be made, and the thyroid is in turn driven by **TSH** from the
anterior pituitary. Feed thyroxine to a young tadpole and it turns into a
minute frog far too early. Remove the thyroid, or keep the tadpole in
iodine-free water, and it simply grows into a giant tadpole that never
metamorphoses.

::: example Worked example 7.4 — why a frog lays thousands of eggs
**Problem.** A female *Rana tigrina* lays 2,800 eggs in one season. 85% are
fertilised, 60% of the fertilised eggs hatch into tadpoles, and only 3% of those
tadpoles survive to become adult frogs. (a) How many adults are produced?
(b) What percentage of the eggs laid reaches adulthood? (c) On average, how many
adults does one breeding pair leave, and what does this tell you about the size
of the frog population from year to year?

**Solution.**

(a) Work through the chain step by step:

$$ \text{fertilised} = 2800 \times 0.85 = 2380 $$
$$ \text{tadpoles} = 2380 \times 0.60 = 1428 $$
$$ \text{adults} = 1428 \times 0.03 = 42.84 \approx 43\ \text{frogs} $$

(b) $$ \frac{42.84}{2800} \times 100 = 1.53\% $$

(c) One pair leaves about 43 adults, but only 2 are needed to replace the
parents. The population would explode if every egg had this success rate, so in
practice predation, drying of the pond and disease cut the survivors down to
roughly 2 per pair. **External fertilisation with no parental care can only work
if the number of eggs is enormous** — exactly the opposite of the mammalian
strategy, where one or two young get heavy protection.
:::

## Chapter summary

- Gametogenesis has three phases — multiplication (mitosis), growth, and
  maturation (two meiotic divisions); spermatogenesis adds a fourth,
  spermiogenesis.
- One primary spermatocyte gives **4 sperms**; one primary oocyte gives
  **1 ovum + 3 polar bodies**. Both divide meiotically twice; only the cytoplasm
  is shared unequally.
- In the frog $2n = 26$, so every gamete carries $n = 13$ and the zygote is
  restored to $2n = 26$.
- The frog's egg is **mesolecithal** and **telolecithal**: dark animal pole with
  the nucleus, pale vegetal pole with the yolk.
- Fertilisation is external and monospermic; the fertilisation membrane blocks
  extra sperms, and the **grey crescent** appears opposite the point of entry and
  fixes the dorsal side.
- Cleavage is **holoblastic but unequal**: furrows 1 and 2 vertical, furrow 3
  horizontal above the equator giving 4 micromeres and 4 macromeres. After $n$
  cleavages there are $2^{n}$ blastomeres and the embryo has not grown.
- The **coeloblastula** has an eccentric blastocoel with a micromere roof and a
  macromere floor.
- Gastrulation uses **epiboly** and **emboly**; the archenteron replaces the
  blastocoel, the yolk plug fills the circular blastopore, and three germ layers
  appear. The dorsal lip is **Spemann's organiser**, and the blastopore becomes
  the **anus**.
- Ectoderm → skin and nervous system; mesoderm → muscle, bone, blood, kidney;
  endoderm → gut lining, liver, pancreas, lungs.
- Metamorphosis of the tadpole is controlled by **thyroxine**, which requires
  iodine and is stimulated by TSH.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The number of functional gametes formed from one primary oocyte is <span class="marks">[1]</span>
   (a) one (b) two (c) three (d) four
2. The grey crescent of the frog's egg appears <span class="marks">[1]</span>
   (a) at the point of sperm entry (b) opposite the point of sperm entry
   (c) at the vegetal pole (d) around the whole equator
3. The third cleavage furrow in the frog's egg is <span class="marks">[1]</span>
   (a) vertical and through both poles (b) vertical at right angles to the first
   (c) horizontal, above the equator (d) horizontal, below the equator
4. The blastocoel of the frog's blastula is eccentric because <span class="marks">[1]</span>
   (a) the egg is alecithal (b) the macromeres are packed with yolk
   (c) cleavage is meroblastic (d) the blastopore has already formed
5. The dorsal lip of the blastopore is called the primary organiser because it <span class="marks">[1]</span>
   (a) forms the yolk plug (b) induces the neural plate
   (c) becomes the mouth (d) secretes thyroxine
6. Which of the following is **not** a derivative of mesoderm? <span class="marks">[1]</span>
   (a) kidney (b) heart (c) liver (d) skeletal muscle
7. A tadpole kept in iodine-free water will <span class="marks">[1]</span>
   (a) metamorphose early (b) remain a tadpole and keep growing
   (c) die within a week (d) develop lungs but no limbs
8. An egg with a moderate amount of yolk collected at one pole is <span class="marks">[1]</span>
   (a) alecithal (b) centrolecithal (c) mesolecithal and telolecithal
   (d) macrolecithal and isolecithal

::: note Answers to Group A
**1.** (a) — the other three haploid nuclei are shed as polar bodies.
**2.** (b) — the cortex rotates towards the entry point, uncovering pale cytoplasm on the far side.
**3.** (c) — it lies above the equator, so the micromeres are smaller than the macromeres.
**4.** (b) — the bulky yolky macromeres push the cavity into the animal half.
**5.** (b) — Spemann and Mangold's graft induced a complete secondary embryo.
**6.** (c) — the liver is endodermal; kidney, heart and muscle are mesodermal.
**7.** (b) — no iodine means no thyroxine, so it becomes a permanent giant tadpole.
**8.** (c) — that is exactly the frog's egg.
:::

**Group B — Short answer questions (4 marks each)**

1. Define gametogenesis. With the help of a flow chart, compare spermatogenesis
   and oogenesis in any four respects. <span class="marks">[4]</span>
2. A frog has $2n = 26$. Trace the chromosome number through one primary
   spermatocyte, one secondary spermatocyte, one spermatid and the zygote, and
   state how many sperms 250 primary spermatocytes will produce. <span class="marks">[4]</span>
3. What is the grey crescent? Explain why it is important in the development of
   the frog. <span class="marks">[4]</span>
4. Describe the cleavage of the frog's egg up to the 8-cell stage, mentioning
   the plane of each furrow. Why is it called holoblastic unequal cleavage? <span class="marks">[4]</span>
5. Distinguish between epiboly and emboly. Name the three germ layers formed at
   the end of gastrulation and give one derivative of each. <span class="marks">[4]</span>
6. Write short notes on the role of thyroxine in the metamorphosis of the frog. <span class="marks">[4]</span>

::: note Answers to Group B
**1.** Gametogenesis is the formation of haploid gametes from diploid germ cells
in the gonad. Flow chart: gonium ($2n$) → mitosis → primary gametocyte ($2n$) →
meiosis I → secondary gametocyte(s) ($n$) → meiosis II → 4 spermatids / 1 ootid
+ 3 polar bodies. Four differences: site (testis / ovary); growth phase (slight /
enormous with yolk); cytokinesis (equal / unequal); yield (4 sperms / 1 ovum +
3 polar bodies). A fifth mark-worthy point is the extra phase of spermiogenesis
in the male.

**2.** Primary spermatocyte $= 26$ chromosomes (52 chromatids, since DNA is
replicated). Secondary spermatocyte $= 13$ chromosomes (26 chromatids).
Spermatid $= 13$ chromosomes (13 chromatids). Zygote $= 13 + 13 = 26$
chromosomes. Sperms from 250 primary spermatocytes:
$250 \times 4 = \mathbf{1000}$ sperms.

**3.** The grey crescent is the crescent-shaped, lightly pigmented area that
appears on the surface of the fertilised frog's egg opposite the point of sperm
entry, formed when the pigmented cortex rotates about 30° towards the entry
point. Importance: (i) it marks the future **dorsal** side; (ii) the first
cleavage furrow passes through it and divides it equally, so each of the first
two blastomeres can form a complete embryo; (iii) the dorsal lip of the
blastopore — Spemann's organiser — develops from it, so it fixes the body axis.

**4.** First furrow — vertical (meridional), passing through both poles and
bisecting the grey crescent → 2 equal blastomeres. Second furrow — vertical, at
right angles to the first → 4 equal blastomeres. Third furrow — horizontal
(latitudinal) but **above** the equator → 4 small micromeres at the animal pole
and 4 large macromeres at the vegetal pole. It is *holoblastic* because the
furrow cuts completely through the egg, and *unequal* because the yolk at the
vegetal pole slows the furrow, so the resulting blastomeres are of different
sizes.

**5.** **Epiboly** is the downward spreading of the small, rapidly dividing
animal micromeres as a sheet over the vegetal cells; they become ectoderm.
**Emboly** is the inward movement of marginal cells over the lip of the
blastopore by involution and invagination; they become mesoderm and endoderm.
Germ layers and one derivative each: ectoderm → brain and spinal cord (or
epidermis); mesoderm → skeletal muscle (or kidney, blood); endoderm → lining of
the alimentary canal (or liver, lungs).

**6.** Thyroxine (T₄, converted to the more active T₃) is secreted by the
tadpole's thyroid gland under the control of TSH from the anterior pituitary,
and its synthesis requires iodine absorbed from the water. It triggers the whole
of metamorphosis: resorption of the tail and gills by lysosomal enzymes, growth
of hind and then fore limbs, replacement of gills by lungs, shortening of the
intestine as the animal changes from herbivore to carnivore, and development of
eyelids. Feeding thyroxine to a young tadpole causes precocious metamorphosis
into a tiny frog; removing the thyroid or withholding iodine gives a permanent
giant tadpole. Prolactin acts against thyroxine and keeps the larva larval.
:::

**Group C — Long answer questions (8 marks each)**

1. Describe the process of gametogenesis in animals. Draw a labelled flow chart
   of spermatogenesis and oogenesis showing the chromosome number at each stage,
   and tabulate any four differences between the two processes. <span class="marks">[8]</span>
2. Describe the development of the frog from the fertilised egg up to the
   formation of the gastrula. Draw labelled diagrams of the blastula and the
   late gastrula, and state the fate of each germ layer. <span class="marks">[8]</span>

::: note Answers to Group C
**1.** *Outline.* (i) Define gametogenesis; name the two types and their sites.
(ii) Multiplication phase — repeated mitosis of primordial germ cells giving
spermatogonia / oogonia, all $2n$. (iii) Growth phase — one gonium enlarges into
a primary spermatocyte or primary oocyte, still $2n$; in the female this involves
massive storage of yolk, RNA and organelles, which is why the oocyte may be a
thousand times the volume of a spermatocyte. (iv) Maturation phase — meiosis I is
reductional ($2n \to n$) and meiosis II is equational; in the male cytokinesis is
equal, giving 2 secondary spermatocytes and then 4 spermatids, while in the
female it is grossly unequal, giving a secondary oocyte plus a first polar body,
then an ootid plus a second polar body. (v) Spermiogenesis — the spermatid loses
cytoplasm, the Golgi body forms the acrosome, the nucleus condenses into the
head, the centrioles form the neck, mitochondria form the spiral of the middle
piece and the distal centriole grows the axial filament of the tail. (vi) Flow
chart as in Figure 1, with $2n = 26$ down to $n = 13$ marked at every stage.
(vii) Four differences from the table in §7.1 — site, growth phase, cytokinesis,
number and nature of the products. Conclude with the functional reason: the sperm
is specialised to travel, the ovum to feed the embryo.

**2.** *Outline.* (i) **Fertilisation** — external, in water, during amplexus;
monospermic; cortical reaction lifts the fertilisation membrane; the pigmented
cortex rotates and the grey crescent appears opposite the entry point; male and
female pronuclei ($n = 13$ each) fuse to give a zygote with $2n = 26$.
(ii) **Cleavage** — holoblastic and unequal: first and second furrows vertical
and at right angles giving 4 equal blastomeres, third furrow horizontal above the
equator giving 4 micromeres and 4 macromeres, then 16, 32 and a solid morula. No
growth occurs, so the blastomeres get steadily smaller.
(iii) **Blastulation** — a fluid-filled blastocoel appears and, being pushed up
by the yolk-laden macromeres, lies eccentrically in the animal half; the roof is
two layers of micromeres, the floor a mass of macromeres. Draw and label as in
Figure 6.
(iv) **Gastrulation** — epiboly carries micromeres downward; emboly carries
marginal cells inward over the dorsal lip; the archenteron grows as the
blastocoel shrinks and vanishes; lateral and ventral lips complete a circular
blastopore plugged by the yolk plug. Draw and label as in Figure 7(c), showing
ectoderm, mesoderm, endoderm, archenteron, blastopore and yolk plug.
(v) **Fate of the germ layers** — ectoderm gives the epidermis and the entire
nervous system; mesoderm gives muscles, skeleton, dermis, blood, heart, kidneys
and gonads; endoderm gives the lining of the gut and its glands (liver,
pancreas) and of the respiratory tract. Mention that the dorsal lip is Spemann's
organiser and that in this deuterostome the blastopore becomes the anus.
:::
