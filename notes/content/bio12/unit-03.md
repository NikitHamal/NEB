---
subject: Biology
grade: 12
unit: 3
title: Genetics
hours: 21
area: Botany
---

Genetics is the study of heredity and variation — how a *Pisum sativum* plant in
Mendel's monastery garden passes "tallness" to its offspring, and why the
offspring are never quite identical to the parents. This unit works from the
molecule upwards. First we ask what the hereditary material actually *is* and
how it copies and expresses itself. Then we follow Mendel's crosses and the
rules they yield, the exceptions to those rules, and what happens when genes
travel together on one chromosome or when the material itself is damaged.

::: key What the examiner asks from this unit
Genetics carries the most marks of any Botany unit (21 hours). Four things come
almost every year: a **labelled DNA / replication / translation diagram**; a
**worked cross** — you must draw the Punnett square, not just quote the ratio; a
**difference table** (DNA vs RNA, linkage vs crossing over, mitosis vs meiosis,
autopolyploidy vs allopolyploidy); and a **numerical or pedigree problem**. Show
parental genotypes, gametes, the square, and the ratio. Marks are given for each
of those four steps, so never jump straight to the answer.
:::

## 3.1 Genetic Materials

### Discovery of the genetic material

By 1900 it was clear that chromosomes carry heredity, but chromosomes contain
both protein and DNA, and protein — with its twenty different amino acids —
looked like the better candidate. Four experiments settled it.

**Griffith (1928) — transformation.** Frederick Griffith worked with
*Streptococcus pneumoniae*, which occurs in two strains: the **S strain**
(smooth, capsulated, virulent) and the **R strain** (rough, non-capsulated,
avirulent). Mice injected with live S bacteria died; live R bacteria, or
heat-killed S bacteria alone, were harmless. But a mixture of heat-killed S and
live R killed the mice, and live S bacteria were recovered from their bodies.
Some "transforming principle" had passed from the dead S cells into the living R
cells and changed them permanently.

**Avery, MacLeod and McCarty (1944).** They repeated Griffith's experiment in a
test tube and destroyed each class of molecule in turn. Protease and RNase did
not stop transformation; **DNase did**. The transforming principle was DNA.

**Hershey and Chase (1952).** They grew bacteriophage T2 in medium containing
radioactive ³²P (which labels DNA, because only DNA has phosphorus) or ³⁵S
(which labels protein, because only protein has sulphur). Phages were allowed to
infect *Escherichia coli*, the empty phage coats were stripped off in a blender
and the cells spun down. The ³²P was found **inside** the bacteria and in the
next generation of phages; the ³⁵S stayed outside. Only DNA entered the host, so
DNA is the genetic material.

**Fraenkel-Conrat and Singer (1957).** In tobacco mosaic virus, which has no
DNA, reconstituted viruses always produced the type of the **RNA** donor, not the
protein donor. So in some viruses **RNA is the genetic material**.

::: memory Why DNA and not protein
A genetic material must (i) replicate accurately, (ii) be chemically and
structurally stable, (iii) carry information, and (iv) allow slow change
(mutation) so that evolution is possible. DNA satisfies all four. RNA has a
reactive 2′-OH group and is far less stable, which is why RNA is used only as a
short-lived messenger in cellular organisms.
:::

### Chemical structure of DNA

DNA is a polymer of **nucleotides**. Each nucleotide has three parts: a
**phosphate group**, a **pentose sugar** (deoxyribose in DNA) and a
**nitrogenous base**. A base joined to a sugar alone is a **nucleoside**; add the
phosphate and it becomes a **nucleotide**.

The bases are of two kinds. **Purines** — adenine (A) and guanine (G) — have a
double ring (a six-membered ring fused to a five-membered ring). **Pyrimidines** —
cytosine (C), thymine (T) in DNA and uracil (U) in RNA — have a single
six-membered ring.

```figure caption="(a) A DNA nucleotide. (b) Complementary base pairing: A pairs with T by two hydrogen bonds, G with C by three. The two backbones run in opposite directions."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
fig, axs = plt.subplots(1, 2, figsize=(5.2, 2.9),
                        gridspec_kw=dict(width_ratios=[1.0, 1.5], wspace=0.05))
SUG="#f6e2c8"; SUGE="#9a7330"; PHO="#dfe9f2"; PHOE="#2c5f96"
PUR="#d9c6e6"; PURE="#6a4a78"; PYR="#cfe3d4"; PYRE="#2e8b57"

def reg(n, cx, cy, r, rot=0.0):
    a = np.radians(rot) + np.arange(n)*2*np.pi/n
    return np.c_[cx + r*np.cos(a), cy + r*np.sin(a)]

def purine(ax, cx, cy, r=0.40, ang=150.0, fc=PUR, ec=PURE):
    hexv = reg(6, 0, 0, r, ang)
    th = np.radians(30+ang); c5 = np.array([1.554*r*np.cos(th), 1.554*r*np.sin(th)])
    penv = reg(5, c5[0], c5[1], 0.8507*r, 30+ang)
    for v in (hexv, penv):
        ax.add_patch(Polygon(v + np.array([cx, cy]), closed=True, fc=fc, ec=ec,
                             lw=1.2, zorder=4))

def pyrim(ax, cx, cy, r=0.40, fc=PYR, ec=PYRE):
    ax.add_patch(Polygon(reg(6, cx, cy, r, 0), closed=True, fc=fc, ec=ec,
                         lw=1.2, zorder=4))

# ---------------- (a) one nucleotide ----------------
ax = axs[0]
ax.add_patch(Circle((0.55, 1.95), 0.26, fc=PHO, ec=PHOE, lw=1.2, zorder=4))
ax.text(0.55, 1.95, 'P', ha='center', va='center', fontsize=8.5, color=PHOE, zorder=5)
ax.plot([0.55, 0.55], [1.69, 1.42], color=INK, lw=1.1, zorder=3)
ax.add_patch(Polygon(reg(5, 1.00, 1.05, 0.42, 90), closed=True, fc=SUG, ec=SUGE,
                     lw=1.2, zorder=4))
ax.text(1.00, 1.03, 'sugar', ha='center', va='center', fontsize=6.2, color=SUGE, zorder=5)
ax.plot([1.42, 1.72], [1.05, 1.05], color=INK, lw=1.1, zorder=3)
pyrim(ax, 2.10, 1.05, 0.38)
ax.text(2.10, 1.05, 'base', ha='center', va='center', fontsize=6.2, color=PYRE, zorder=5)
ax.text(0.55, 2.42, 'phosphate', ha='center', fontsize=6.6, color=PHOE)
ax.text(0.98, 0.40, 'deoxyribose', ha='center', fontsize=6.6, color=SUGE)
ax.text(2.12, 0.40, 'nitrogenous\nbase', ha='center', fontsize=6.6, color=PYRE,
        linespacing=1.2)
ax.text(0.62, 1.44, "5′ C", fontsize=6.0, color=INK, ha='left', va='bottom')
ax.text(1.05, 0.66, "3′ OH", fontsize=6.0, color=INK, ha='left', va='top')
ax.plot([1.02, 1.02], [0.65, 0.78], color=INK, lw=0.8)
ax.set_title('(a) nucleotide', fontsize=7.6, pad=2)
ax.set_xlim(0.0, 2.8); ax.set_ylim(0.15, 2.62); ax.set_aspect('equal'); ax.axis('off')

# ---------------- (b) the two base pairs ----------------
ax = axs[1]
for y, (pu, py, nb, hb) in enumerate([(1.30, 0, 0, 0)]):
    pass
rows = [(2.05, 'A', 'T', 2), (0.72, 'G', 'C', 3)]
for y, pn, yn, nh in rows:
    purine(ax, 1.30, y, 0.40, ang=150)
    ax.text(1.30, y, pn, ha='center', va='center', fontsize=9, color=PURE, zorder=6)
    pyrim(ax, 2.72, y, 0.38)
    ax.text(2.72, y, yn, ha='center', va='center', fontsize=9, color=PYRE, zorder=6)
    for k in range(nh):
        yy = y + (k - (nh-1)/2)*0.17
        ax.plot([1.72, 2.34], [yy, yy], color='#a2453e', lw=1.0, ls=(0, (2, 2)),
                zorder=3)
    ax.text(2.03, y + (nh/2)*0.17 + 0.12, f'{nh} H-bonds', ha='center',
            fontsize=6.0, color='#a2453e')
    # sugars + backbone stubs
    ax.add_patch(Polygon(reg(5, 0.48, y, 0.27, 90), closed=True, fc=SUG, ec=SUGE,
                         lw=1.0, zorder=4))
    ax.add_patch(Polygon(reg(5, 3.56, y, 0.27, 90), closed=True, fc=SUG, ec=SUGE,
                         lw=1.0, zorder=4))
    ax.plot([0.75, 0.94], [y, y], color=INK, lw=1.0, zorder=3)
    ax.plot([3.10, 3.29], [y, y], color=INK, lw=1.0, zorder=3)
for x, c in ((0.16, PHOE), (3.88, PHOE)):
    ax.plot([x, x], [0.15, 2.62], color=c, lw=2.0, alpha=0.65, zorder=2)
    for yy in (2.05, 0.72):
        ax.plot([x, x+0.20 if x < 2 else x-0.20], [yy, yy], color=c, lw=1.0, zorder=2)
ax.annotate('', xy=(0.16, 2.72), xytext=(0.16, 2.30),
            arrowprops=dict(arrowstyle='-|>', color=PHOE, lw=1.4, mutation_scale=10))
ax.annotate('', xy=(3.88, 0.05), xytext=(3.88, 0.47),
            arrowprops=dict(arrowstyle='-|>', color=PHOE, lw=1.4, mutation_scale=10))
ax.text(0.16, 2.86, "5′→3′", ha='center', fontsize=6.4, color=PHOE)
ax.text(3.88, 2.86, "3′→5′", ha='center', fontsize=6.4, color=PHOE)
ax.text(2.02, 0.05, 'antiparallel sugar–phosphate backbones', ha='center',
        fontsize=6.4, color=MUTED)
ax.set_title('(b) base pairing', fontsize=7.6, pad=2)
ax.set_xlim(-0.05, 4.10); ax.set_ylim(-0.10, 3.05); ax.set_aspect('equal'); ax.axis('off')
```

Nucleotides are joined into a chain by **phosphodiester bonds**, which link the
3′ carbon of one sugar to the 5′ carbon of the next through a phosphate. Every
DNA strand therefore has a free phosphate at one end (the **5′ end**) and a free
hydroxyl at the other (the **3′ end**), and so has direction.

**Chargaff's rules (1950).** Erwin Chargaff analysed DNA from many species and
found that the amount of adenine always equals thymine and guanine always equals
cytosine:

$$ A = T, \qquad G = C, \qquad \frac{A+G}{T+C} = 1 $$

that is, purines = pyrimidines. The ratio $(A+T)/(G+C)$, however, differs from
species to species.

### The Watson–Crick double helix

Using Chargaff's data and the X-ray diffraction photographs of Rosalind Franklin
and Maurice Wilkins, **James Watson and Francis Crick proposed the double-helix
model in 1953** (Nobel Prize, 1962). Its features:

- Two polynucleotide chains are coiled round a common axis to form a
  **right-handed** helix.
- The chains are **antiparallel**: one runs 5′→3′, the other 3′→5′.
- Sugar–phosphate backbones lie **outside**; the bases project inwards,
  perpendicular to the axis.
- Bases pair by hydrogen bonds — **A with T (two bonds), G with C (three)**. A
  purine always pairs with a pyrimidine, so the width of the helix is constant.
- Diameter **2 nm**; one complete turn (pitch) is **3.4 nm** and contains **10
  base pairs**, so adjacent base pairs are **0.34 nm** apart.
- The coiling produces a wide **major groove** and a narrow **minor groove**,
  where regulatory proteins bind.
- The two strands are **complementary**: the sequence of one fixes the sequence
  of the other. This is the chemical basis of accurate copying.

```figure caption="B-DNA. The two strands are antiparallel and complementary; one complete turn is 3.4 nm long and holds 10 base pairs."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4, 4.3))
P = 3.4                                  # nm per turn
z = np.linspace(0.25, 7.35, 700)
x1 = np.sin(2*np.pi*z/P)
x2 = np.sin(2*np.pi*z/P + np.pi)
ax.plot(x1, z, color=ACCENT, lw=2.8, solid_capstyle='round', zorder=4)
ax.plot(x2, z, color='#b8860b', lw=2.8, solid_capstyle='round', zorder=4)
pairs = [('A','T'),('T','A'),('G','C'),('C','G'),('A','T'),('G','C'),('T','A'),
         ('C','G'),('G','C'),('A','T'),('T','A'),('C','G'),('A','T'),('G','C'),
         ('C','G'),('T','A'),('A','T'),('G','C'),('C','G'),('T','A'),('A','T')]
rungs = np.arange(0.34, 7.30, 0.34)
for k, zz in enumerate(rungs):
    a = np.sin(2*np.pi*zz/P); b = np.sin(2*np.pi*zz/P + np.pi)
    p, q = pairs[k % len(pairs)]
    nh = 3 if p in 'GC' else 2
    ax.plot([a, b], [zz, zz], color='#a2453e', lw=0.8,
            ls='-' if nh == 3 else (0, (1.7, 1.5)), alpha=0.85, zorder=3)
    if k % 3 == 1:
        ax.text(a*0.58, zz + 0.11, p, fontsize=5.8, color=INK, ha='center', zorder=5)
        ax.text(b*0.58, zz + 0.11, q, fontsize=5.8, color=INK, ha='center', zorder=5)
# strand polarity
ax.annotate('', xy=(x1[-1], 7.66), xytext=(x1[-1], 7.32),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.7, mutation_scale=11))
ax.annotate('', xy=(x2[0], -0.10), xytext=(x2[0], 0.24),
            arrowprops=dict(arrowstyle='-|>', color='#b8860b', lw=1.7, mutation_scale=11))
ax.text(x1[-1] + 0.10, 7.80, "3′", fontsize=8.5, color=ACCENT, ha='center')
ax.text(x2[-1] - 0.10, 7.80, "5′", fontsize=8.5, color='#b8860b', ha='center')
ax.text(x1[0] - 0.12, -0.52, "5′", fontsize=8.5, color=ACCENT, ha='center')
ax.text(x2[0] + 0.12, -0.52, "3′", fontsize=8.5, color='#b8860b', ha='center')
# diameter, measured where the projection is widest (z = 0.85)
ax.annotate('', xy=(-1.0, 0.85), xytext=(1.0, 0.85),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=1.0, mutation_scale=8))
ax.text(0.0, 0.40, '2 nm', fontsize=6.8, color=INK, ha='center', va='top')
# one turn
ax.annotate('', xy=(2.30, 2.55), xytext=(2.30, 5.95),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=1.0, mutation_scale=8))
ax.text(2.44, 4.25, 'one turn\n= 3.4 nm\n= 10 base pairs', fontsize=6.8, color=INK,
        va='center', linespacing=1.35)
def lab(t, tip, tx, ty, ha='left'):
    ax.annotate(t, xy=tip, xytext=(tx, ty), fontsize=6.8, color=INK, ha=ha,
                va='center', linespacing=1.3,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7, shrinkA=2, shrinkB=2))
lab('sugar–phosphate\nbackbone', (-0.93, 6.90), -2.30, 7.25, ha='right')
lab('base pair held by\nhydrogen bonds', (0.20, 5.62), -2.30, 5.75, ha='right')
lab('major groove (wide)', (0.0, 4.25), -2.30, 4.05, ha='right')
lab('minor groove (narrow)', (0.0, 2.55), -2.30, 2.35, ha='right')
lab('adjacent base pairs\n0.34 nm apart', (0.40, 6.28), 2.44, 6.90)
ax.set_xlim(-4.7, 4.5); ax.set_ylim(-1.05, 8.25); ax.axis('off')
```
::: caution Two hydrogen bonds or three?
A–T has **two** hydrogen bonds and G–C has **three**. DNA rich in G–C therefore
needs a higher temperature to melt (denature). Writing "A=T by three bonds"
loses a mark every time.
:::

### RNA and its types

RNA differs from DNA in the sugar (ribose), one base (uracil replaces thymine)
and usually in being single-stranded.

| Feature | DNA | RNA |
|---|---|---|
| Sugar | deoxyribose (no 2′-OH) | ribose (2′-OH present) |
| Bases | A, G, C, **T** | A, G, C, **U** |
| Strands | double, helical | mostly single |
| Occurrence | nucleus, mitochondria, plastids | nucleus and cytoplasm |
| Amount in a cell | constant | varies with protein synthesis |
| Stability | very stable | unstable, short-lived |
| Chargaff's rule | obeyed (A=T, G=C) | not obeyed |
| Function | stores genetic information | expresses it (and is genetic material in some viruses) |
| Hydrolysed by | DNase | RNase |

Three classes of RNA take part in protein synthesis:

- **mRNA (messenger RNA, ~3–5%)** carries the copy of the gene from nucleus to
  ribosome. Its bases are read in threes as **codons**.
- **tRNA (transfer RNA, ~15%)** is the adapter. It is the smallest RNA
  (~75–90 nucleotides), folds into a **clover-leaf** shape with an **anticodon
  loop** at one end and the amino-acid attachment site (the sequence –CCA) at its
  3′ end. There is at least one tRNA for each of the 20 amino acids.
- **rRNA (ribosomal RNA, ~80%)** combines with protein to build the ribosome and
  has catalytic (ribozyme) activity — the peptide bond itself is made by rRNA.

### DNA replication

Replication is **semi-conservative**: the two strands separate and each acts as a
template, so every daughter molecule has one old (parental) and one new strand.
This was proved by **Meselson and Stahl (1958)**, who grew *E. coli* for many
generations in medium containing heavy ¹⁵N, then transferred it to ordinary ¹⁴N.
After one generation all the DNA was of intermediate density (hybrid); after two
generations half was hybrid and half was light. Neither the conservative nor the
dispersive model predicts this pattern.

Replication begins at a fixed sequence called the **origin of replication** and
proceeds at a Y-shaped **replication fork**. The chief enzymes are:

| Enzyme | Function |
|---|---|
| Helicase | unwinds the double helix, breaking hydrogen bonds |
| Topoisomerase (gyrase) | relieves the supercoiling ahead of the fork |
| SSB proteins | hold the separated strands apart |
| Primase | lays down a short RNA primer with a free 3′-OH |
| DNA polymerase III | adds deoxyribonucleotides 5′→3′; main elongating enzyme |
| DNA polymerase I | removes the RNA primer and fills the gap with DNA |
| DNA ligase | seals the nicks by forming phosphodiester bonds |

Because DNA polymerase can add nucleotides **only to a free 3′-OH end**, it can
synthesise only in the 5′→3′ direction. On the strand whose template runs 3′→5′
towards the fork, synthesis is smooth and continuous — the **leading strand**. On
the other template the enzyme must work away from the fork, so it makes short
pieces of 1000–2000 nucleotides called **Okazaki fragments** which are later
joined by ligase — the **lagging strand**. Replication is therefore
**semi-discontinuous**.

```figure caption="A replication fork. Synthesis is continuous on the leading strand and discontinuous — as Okazaki fragments — on the lagging strand."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
fig, ax = plt.subplots(figsize=(5.2, 3.2))
OLD = MUTED; NEW = ACCENT; PRI = "#d9534f"
def arm(sign):
    t = np.linspace(0, 1, 160)
    return -1.2 + 4.6*t, sign*(0.24 + 1.40*t**1.5)
# parental duplex, still wound (right of the fork is the un-opened part? no: left)
ax.plot([-4.8, -1.25], [0.24, 0.24], color=OLD, lw=2.6, solid_capstyle='round', zorder=4)
ax.plot([-4.8, -1.25], [-0.24, -0.24], color=OLD, lw=2.6, solid_capstyle='round', zorder=4)
for xx in np.arange(-4.7, -1.28, 0.27):
    ax.plot([xx, xx], [-0.24, 0.24], color=GRID, lw=0.9, zorder=3)
xt, yt = arm(+1); xb, yb = arm(-1)
ax.plot(xt, yt, color=OLD, lw=2.6, solid_capstyle='round', zorder=4)
ax.plot(xb, yb, color=OLD, lw=2.6, solid_capstyle='round', zorder=4)
ax.add_patch(Ellipse((-1.18, 0.0), 0.86, 1.05, fc="#cfe3d4", ec="#2e8b57", lw=1.3, zorder=6))
ax.text(-1.18, 0.0, 'H', ha='center', va='center', fontsize=8.5, color="#2e8b57", zorder=7)
ax.annotate('', xy=(-2.55, 0.0), xytext=(-1.75, 0.0),
            arrowprops=dict(arrowstyle='-|>', color="#2e8b57", lw=1.5, mutation_scale=11), zorder=7)
# ---- leading strand: one continuous piece running back towards the fork ----
xl = np.linspace(3.30, -0.45, 160)
yl = (0.24 + 1.40*((xl + 1.2)/4.6)**1.5) - 0.38
ax.plot(xl[:-6], yl[:-6], color=NEW, lw=2.4, solid_capstyle='round', zorder=5)
ax.plot(xl[:10], yl[:10], color=PRI, lw=2.8, solid_capstyle='round', zorder=6)
ax.annotate('', xy=(xl[-1], yl[-1]), xytext=(xl[-7], yl[-7]),
            arrowprops=dict(arrowstyle='-|>', color=NEW, lw=1.8, mutation_scale=12), zorder=6)
ax.text(3.46, yl[0] + 0.06, "5′", fontsize=7, color=NEW)
ax.text(-0.42, yl[-1] - 0.34, "3′", fontsize=7, color=NEW)
# ---- lagging strand: three Okazaki fragments, each made 5′ -> 3′ ----
for a, b in [(-0.30, 1.05), (1.25, 2.45), (2.62, 3.72)]:
    xs = np.linspace(a, b, 80)
    ys = -(0.24 + 1.40*((xs + 1.2)/4.6)**1.5) + 0.38
    ax.plot(xs[10:-5], ys[10:-5], color=NEW, lw=2.4, solid_capstyle='round', zorder=5)
    ax.plot(xs[:11], ys[:11], color=PRI, lw=2.8, solid_capstyle='round', zorder=6)
    ax.annotate('', xy=(xs[-1], ys[-1]), xytext=(xs[-6], ys[-6]),
                arrowprops=dict(arrowstyle='-|>', color=NEW, lw=1.6, mutation_scale=10), zorder=6)
def lab(t, tip, tx, ty, ha='center', col=INK, fs=6.8):
    ax.annotate(t, xy=tip, xytext=(tx, ty), fontsize=fs, color=col, ha=ha, va='center',
                linespacing=1.3,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7, shrinkA=2, shrinkB=2))
lab('parental DNA', (-3.5, 0.0), -3.9, 1.20)
lab('helicase; the fork\nmoves this way', (-1.18, -0.55), -2.35, -1.75)
lab('leading strand —\ncontinuous', (1.55, 0.88), 0.85, 2.10, col=NEW)
lab('lagging strand — Okazaki\nfragments, later joined by ligase', (1.85, -1.02), 0.45, -2.20, col=NEW)
lab('RNA primer', (2.75, -1.42), 3.75, -2.20, col=PRI)
ax.text(3.95, 1.72, "3′", fontsize=7.5, color=OLD); ax.text(3.95, -1.78, "5′", fontsize=7.5, color=OLD)
ax.text(-5.0, 0.24, "5′", fontsize=7.5, color=OLD, ha='right', va='center')
ax.text(-5.0, -0.24, "3′", fontsize=7.5, color=OLD, ha='right', va='center')
ax.set_xlim(-5.6, 4.9); ax.set_ylim(-2.65, 2.55); ax.axis('off')
```
::: caution Direction of synthesis
The new strand is **always** built 5′→3′; the *template* is read 3′→5′. Saying
"the lagging strand is made 3′→5′" is wrong — each Okazaki fragment is itself
made 5′→3′; it is only the *overall growth* of the lagging strand that runs away
from the fork.
:::

### From gene to protein — the central dogma

Crick's **central dogma (1958)** states the flow of information:

DNA --replication--> DNA --transcription--> RNA --translation--> protein

In retroviruses such as HIV the flow is partly reversed: **reverse
transcriptase** copies RNA back into DNA (Temin and Baltimore, 1970).

**Transcription** is the copying of one strand of a gene into RNA. Only one
strand, the **template (antisense) strand**, is copied; the other, the **coding
(sense) strand**, has the same sequence as the mRNA except that T replaces U.
**RNA polymerase** binds the **promoter**, unwinds a short stretch, and adds
ribonucleotides 5′→3′ until it meets the **terminator**. In eukaryotes the first
transcript (hnRNA) is then processed: a 5′ cap is added, a poly-A tail is added
at the 3′ end, and the non-coding **introns** are cut out while the coding
**exons** are joined — **splicing**.

| | Replication | Transcription |
|---|---|---|
| Product | two DNA molecules | one RNA molecule |
| Template used | both strands | one strand only |
| Enzyme | DNA polymerase | RNA polymerase |
| Primer | RNA primer needed | not needed |
| Raw material | deoxyribonucleotides | ribonucleotides |
| Base inserted opposite A | T | U |
| Extent | the whole genome | one gene or operon |
| Occurs in | S phase of the cell cycle | as and when a product is needed |

**The genetic code.** The message is read in non-overlapping groups of three
bases called **codons**. With four bases there are $4^{3} = 64$ codons — 61
**sense** codons that specify amino acids and 3 **stop** (nonsense) codons, UAA,
UAG and UGA. **AUG** is both the start codon and the codon for methionine. The
code was cracked by Nirenberg and Matthaei (poly-U gave polyphenylalanine),
Khorana and Holley.

Its properties: it is **triplet**, **non-overlapping**, **comma-less** (read
continuously from a fixed starting point), **degenerate** (most amino acids have
more than one codon — only methionine and tryptophan have a single codon),
**unambiguous** (one codon never codes for two amino acids) and almost
**universal** (the same in *Escherichia coli*, in rice and in humans, with minor
exceptions in mitochondria).

```figure caption="The standard genetic code. Read the first base from the left column, the second along the top and the third from the right column. Stop codons are shaded."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.2, 4.3))
B = ['U', 'C', 'A', 'G']
code = {
 'UUU':'Phe','UUC':'Phe','UUA':'Leu','UUG':'Leu','CUU':'Leu','CUC':'Leu','CUA':'Leu','CUG':'Leu',
 'AUU':'Ile','AUC':'Ile','AUA':'Ile','AUG':'Met','GUU':'Val','GUC':'Val','GUA':'Val','GUG':'Val',
 'UCU':'Ser','UCC':'Ser','UCA':'Ser','UCG':'Ser','CCU':'Pro','CCC':'Pro','CCA':'Pro','CCG':'Pro',
 'ACU':'Thr','ACC':'Thr','ACA':'Thr','ACG':'Thr','GCU':'Ala','GCC':'Ala','GCA':'Ala','GCG':'Ala',
 'UAU':'Tyr','UAC':'Tyr','UAA':'STOP','UAG':'STOP','CAU':'His','CAC':'His','CAA':'Gln','CAG':'Gln',
 'AAU':'Asn','AAC':'Asn','AAA':'Lys','AAG':'Lys','GAU':'Asp','GAC':'Asp','GAA':'Glu','GAG':'Glu',
 'UGU':'Cys','UGC':'Cys','UGA':'STOP','UGG':'Trp','CGU':'Arg','CGC':'Arg','CGA':'Arg','CGG':'Arg',
 'AGU':'Ser','AGC':'Ser','AGA':'Arg','AGG':'Arg','GGU':'Gly','GGC':'Gly','GGA':'Gly','GGG':'Gly'}
CW, RH = 1.0, 0.30
for i, b1 in enumerate(B):
    for j, b2 in enumerate(B):
        for k, b3 in enumerate(B):
            x = j*CW; y = -(i*4 + k)*RH
            cod = b1 + b2 + b3
            aa = code[cod]
            stop = (aa == 'STOP'); start = (cod == 'AUG')
            fc = '#f3d6d3' if stop else ('#d6e8d8' if start else
                 ('#eef2f7' if (i + j) % 2 == 0 else '#ffffff'))
            ax.add_patch(Rectangle((x, y - RH), CW, RH, fc=fc, ec='#c3cad4', lw=0.5))
            ax.text(x + 0.06, y - RH/2, cod, fontsize=5.6, color=MUTED, va='center')
            ax.text(x + CW - 0.06, y - RH/2, aa, fontsize=5.8, color=INK, va='center',
                    ha='right', fontweight='bold' if (stop or start) else 'normal')
    ax.add_patch(Rectangle((-0.42, -(i*4 + 4)*RH), 0.42, 4*RH, fc='#dfe9f2',
                           ec='#c3cad4', lw=0.5))
    ax.text(-0.21, -(i*4 + 2)*RH, b1, fontsize=9, ha='center', va='center', color=INK)
    for k, b3 in enumerate(B):
        ax.text(4*CW + 0.20, -(i*4 + k)*RH - RH/2, b3, fontsize=7, ha='center',
                va='center', color=INK)
for j, b2 in enumerate(B):
    ax.add_patch(Rectangle((j*CW, 0), CW, 0.30, fc='#dfe9f2', ec='#c3cad4', lw=0.5))
    ax.text(j*CW + CW/2, 0.15, b2, fontsize=9, ha='center', va='center', color=INK)
ax.text(-0.21, 0.15, '1st', fontsize=6.4, ha='center', va='center', color=MUTED)
ax.text(4*CW + 0.20, 0.15, '3rd', fontsize=6.4, ha='center', va='center', color=MUTED)
ax.text(2.0, 0.48, 'second base', fontsize=7.2, ha='center', color=MUTED)
ax.text(-0.21, -5.05, 'AUG = start (Met)   ·   UAA, UAG, UGA = stop',
        fontsize=6.6, ha='left', color=INK)
ax.set_xlim(-0.55, 4.6); ax.set_ylim(-5.25, 0.62); ax.axis('off')
```

**Translation** builds the polypeptide on the ribosome (70S in prokaryotes,
80S in eukaryotes) in four steps:

1. **Activation.** Each amino acid is joined to its own tRNA by an
   aminoacyl-tRNA synthetase, using ATP, giving aminoacyl-tRNA.
2. **Initiation.** The small ribosomal subunit binds the mRNA and moves to the
   AUG start codon; the initiator tRNA (carrying formyl-methionine in bacteria)
   pairs with it; the large subunit joins, placing this tRNA in the **P site**.
3. **Elongation.** The next aminoacyl-tRNA enters the **A site**, its anticodon
   pairing with the codon. **Peptidyl transferase** (an rRNA ribozyme) forms the
   peptide bond, and the ribosome **translocates** one codon along the mRNA; the
   empty tRNA leaves from the E site.
4. **Termination.** When a stop codon reaches the A site no tRNA fits; a release
   factor binds, the polypeptide is freed and the ribosome dissociates.

Several ribosomes usually translate one mRNA at once, forming a **polysome**.

```figure caption="Gene expression. (a) Transcription: RNA polymerase copies the template strand into mRNA. (b) Translation: tRNA anticodons read the codons on the ribosome."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle, FancyBboxPatch, Circle, Polygon
fig, axs = plt.subplots(2, 1, figsize=(5.2, 4.5),
                        gridspec_kw=dict(height_ratios=[1.0, 1.3], hspace=0.30))
# ================= (a) transcription =================
ax = axs[0]
DNA = MUTED
# RNA polymerase drawn behind the DNA
ax.add_patch(FancyBboxPatch((-1.55, -0.95), 3.35, 2.55, boxstyle='round,pad=0.12',
                            fc='#dfe9f2', ec=ACCENT, lw=1.2, alpha=0.75, zorder=2))
ax.text(0.12, 1.28, 'RNA polymerase', ha='center', fontsize=6.6, color=ACCENT, zorder=3)
# coding (sense) strand on top, template (antisense) below; bubble in the middle
xl = np.linspace(-4.6, -1.05, 60); xr = np.linspace(1.35, 4.6, 60)
for xs in (xl, xr):
    ax.plot(xs, 0.0*xs + 0.60, color=DNA, lw=2.5, solid_capstyle='round', zorder=5)
    ax.plot(xs, 0.0*xs + 0.00, color=DNA, lw=2.5, solid_capstyle='round', zorder=5)
    for xx in np.arange(xs[0] + 0.10, xs[-1], 0.29):
        ax.plot([xx, xx], [0.0, 0.60], color=GRID, lw=0.9, zorder=4)
tb = np.linspace(0, np.pi, 80)
ax.plot(-1.05 + 2.40*(1 - np.cos(tb))/2, 0.60 + 0.42*np.sin(tb), color=DNA, lw=2.5, zorder=5)
ax.plot(-1.05 + 2.40*(1 - np.cos(tb))/2, 0.00 - 0.42*np.sin(tb), color=DNA, lw=2.5, zorder=5)
# nascent mRNA: 3′ growing end inside the bubble, 5′ end trailing to the left
xm = np.linspace(0.95, -4.15, 120)
ym = -0.42 - 0.78*((0.95 - xm)/5.10)**1.3
ax.plot(xm, ym, color='#d9534f', lw=2.3, solid_capstyle='round', zorder=6)
for k, c in enumerate('ACGGUA'):
    xx = 0.72 - k*0.62
    yy = -0.42 - 0.78*((0.95 - xx)/5.10)**1.3
    ax.text(xx, yy - 0.26, c, fontsize=6.2, color='#d9534f', ha='center', zorder=6)
ax.text(-4.35, ym[-1] - 0.18, "5′", fontsize=6.8, color='#d9534f', ha='right')
ax.text(1.24, -0.70, "3′", fontsize=6.8, color='#d9534f', ha='left')
ax.text(-2.10, -1.52, 'mRNA', fontsize=6.6, color='#d9534f', ha='center')
ax.text(-4.75, 0.60, "5′", fontsize=6.8, color=DNA, ha='right', va='center')
ax.text(-4.75, 0.00, "3′", fontsize=6.8, color=DNA, ha='right', va='center')
ax.text(4.75, 0.60, "3′", fontsize=6.8, color=DNA, ha='left', va='center')
ax.text(4.75, 0.00, "5′", fontsize=6.8, color=DNA, ha='left', va='center')
ax.text(-3.05, 1.02, 'coding (sense) strand', fontsize=6.2, color=DNA, ha='center')
ax.text(-3.05, -0.44, 'template (antisense) strand', fontsize=6.2, color=DNA, ha='center')
ax.annotate('', xy=(3.60, 1.32), xytext=(2.10, 1.32),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.3, mutation_scale=11))
ax.text(2.85, 1.52, 'polymerase moves', fontsize=6.2, color=INK, ha='center')
ax.set_title('(a) transcription', fontsize=7.8, pad=0, loc='left')
ax.set_xlim(-5.7, 5.3); ax.set_ylim(-1.95, 1.85); ax.axis('off')

# ================= (b) translation =================
ax = axs[1]
codons = ['AUG', 'GCU', 'UCA', 'GGU', 'CAU', 'UAA']
W, X0 = 1.30, -4.30
cen = [X0 + k*W + W/2 for k in range(6)]
# ribosome subunits, drawn behind
ax.add_patch(Ellipse((-1.70, 1.02), 4.70, 1.80, fc='#cfe3d4', ec='#2e8b57',
                     lw=1.3, alpha=0.85, zorder=2))
ax.add_patch(Ellipse((-1.70, -0.60), 4.40, 0.92, fc='#e3f0e6', ec='#2e8b57',
                     lw=1.3, alpha=0.95, zorder=2))
ax.text(0.80, 1.22, 'large subunit', fontsize=6.4, color='#2e8b57', ha='left')
ax.text(0.72, -0.98, 'small subunit', fontsize=6.4, color='#2e8b57', ha='left')
for k, c in enumerate(codons):
    x = X0 + k*W
    ax.add_patch(Rectangle((x, -0.20), W, 0.40, fc='#fdf3e0' if k % 2 else '#f6e2c8',
                           ec='#9a7330', lw=0.9, zorder=6))
    ax.text(x + W/2, 0.0, c, ha='center', va='center', fontsize=6.8, color=INK, zorder=7)
ax.text(X0 - 0.14, 0.0, "5′", fontsize=6.8, color=MUTED, ha='right', va='center')
ax.text(X0 + 6*W + 0.14, 0.0, "3′", fontsize=6.8, color=MUTED, ha='left', va='center')
ax.text(1.62, -0.52, 'mRNA', fontsize=6.4, color='#9a7330', ha='center')
def trna(x, anti, aa, col, chain=None):
    ax.add_patch(Polygon([[x-0.36, 0.52], [x+0.36, 0.52], [x+0.24, 1.42], [x-0.24, 1.42]],
                         closed=True, fc='#ffffff', ec=col, lw=1.2, zorder=8))
    ax.add_patch(Rectangle((x-0.36, 0.22), 0.72, 0.30, fc='#ffffff', ec=col, lw=1.2, zorder=8))
    ax.text(x, 0.37, anti, ha='center', va='center', fontsize=6.0, color=col, zorder=9)
    for i in range(3):
        ax.plot([x - 0.22 + i*0.22]*2, [0.20, 0.24], color='#a2453e', lw=0.8, zorder=9)
    names = chain or [aa]
    for i, nm in enumerate(names):
        cx = x - i*0.62; cy = 1.66 + i*0.34
        ax.add_patch(Circle((cx, cy), 0.235, fc=col, ec=col, lw=0.8, alpha=0.60, zorder=9))
        ax.text(cx, cy, nm, ha='center', va='center', fontsize=5.4, color='#ffffff', zorder=10)
        if i:
            ax.plot([cx + 0.20, cx + 0.42], [cy - 0.10, cy - 0.24], color=INK, lw=1.0, zorder=9)
trna(cen[1], 'CGA', 'Ala', '#1d6fb8', chain=['Ala', 'Met'])
trna(cen[2], 'AGU', 'Ser', '#6a5acd')
for lbl, c in (('E', cen[0]), ('P', cen[1]), ('A', cen[2])):
    ax.text(c, -1.30, lbl + ' site', fontsize=6.4, color=INK, ha='center')
ax.annotate('', xy=(cen[2] - 0.22, 1.66), xytext=(cen[1] + 0.22, 1.66),
            arrowprops=dict(arrowstyle='-|>', color='#a2453e', lw=1.3, mutation_scale=9), zorder=11)
ax.annotate('peptide bond forms', xy=((cen[1] + cen[2])/2, 1.80), xytext=(0.10, 2.18),
            fontsize=6.2, color='#a2453e', ha='left', va='center',
            arrowprops=dict(arrowstyle='-', color='#a2453e', lw=0.7, shrinkA=2, shrinkB=2))
ax.annotate('growing polypeptide chain', xy=(cen[1] - 0.62, 2.22), xytext=(-5.55, 2.42),
            fontsize=6.2, color=INK, ha='left', va='center',
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7, shrinkA=2, shrinkB=2))
ax.annotate('anticodon', xy=(cen[1] - 0.30, 0.33), xytext=(-4.30, 0.95), fontsize=6.2,
            color=INK, ha='left', va='center',
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7, shrinkA=2, shrinkB=2))
ax.annotate('', xy=(2.95, 0.72), xytext=(1.75, 0.72),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.3, mutation_scale=11))
ax.text(2.35, 0.96, "ribosome moves 5′→3′", fontsize=6.2, color=INK, ha='center')
ax.text(cen[5], -1.30, 'stop codon', fontsize=6.2, color='#d9534f', ha='center')
ax.set_title('(b) translation', fontsize=7.8, pad=0, loc='left')
ax.set_xlim(-5.7, 5.3); ax.set_ylim(-1.60, 2.80); ax.axis('off')
```
### The gene

A **gene** is a segment of DNA that carries the information for one polypeptide
or one functional RNA. In the classical (Mendelian) sense it is the unit of
inheritance occupying a fixed position, the **locus**, on a chromosome;
alternative forms of a gene at the same locus are **alleles**. In molecular terms
the unit of function is the **cistron**, the smallest unit of mutation the
**muton** and of recombination the **recon**. Eukaryotic genes are usually
**split genes** — coding exons interrupted by non-coding introns.

## 3.2 Mendelian genetics

### Mendel and his material

Gregor Johann Mendel (1822–1884), an Austrian monk, worked on the garden pea
*Pisum sativum* between 1856 and 1863 and published *Experiments in Plant
Hybridisation* in 1866. His results were ignored until 1900, when de Vries,
Correns and Tschermak rediscovered them independently. He succeeded where others
had failed because of four decisions:

- He chose **one pair of contrasting characters at a time**, instead of
  comparing whole plants.
- He used **pure (true-breeding) lines**, obtained by self-pollinating for
  several generations before starting.
- He **counted** the offspring and treated the counts mathematically.
- He followed the cross for **more than one generation** (F₁, F₂, F₃).

*Pisum sativum* itself was a lucky choice: it is naturally **self-pollinating**
(the keel encloses the stamens and stigma), so pure lines are easy to keep; it
can be cross-pollinated by hand after emasculation; it has a short life cycle and
many seeds per plant; and it showed seven clear-cut pairs of characters.

| Character | Dominant | Recessive |
|---|---|---|
| Stem height | tall | dwarf |
| Flower position | axial | terminal |
| Flower colour | violet | white |
| Pod shape | inflated | constricted |
| Pod colour | green | yellow |
| Seed shape | round | wrinkled |
| Cotyledon colour | yellow | green |

::: definition The words you must use correctly
**Gene** — a unit of inheritance, a DNA segment at a fixed **locus**.
**Allele** — one of the alternative forms of a gene (T and t).
**Dominant** — the allele expressed in the heterozygote; **recessive** — the one
masked in it. **Homozygous** (TT, tt) — both alleles alike; **heterozygous** (Tt)
— alleles different. **Genotype** — the genetic constitution; **phenotype** — the
appearance. **Monohybrid cross** — a cross following one character;
**dihybrid** — two. **Back cross** — F₁ crossed with either parent; **test
cross** — F₁ crossed with the *homozygous recessive* parent.
:::

### Monohybrid cross and the first two laws

Mendel crossed a pure tall plant (TT) with a pure dwarf (tt). All the F₁ were
tall. When these F₁ plants were self-pollinated, the F₂ contained tall and dwarf
plants in the ratio **3 : 1** (Mendel counted 787 tall : 277 dwarf, a ratio of
2.84 : 1). The dwarf character had not been destroyed in F₁; it had only been
hidden.

```figure caption="Monohybrid cross in *Pisum sativum*. The F₂ phenotypic ratio is 3 tall : 1 dwarf and the genotypic ratio 1 TT : 2 Tt : 1 tt."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Ellipse, FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.0, 4.4))
TALLC = "#2e8b57"; DW = "#b8860b"
def plant(x, y, h, col, lab):
    ax.plot([x, x], [y, y + h], color=col, lw=1.6, solid_capstyle='round', zorder=4)
    for i, f in enumerate(np.linspace(0.32, 0.86, 3 if h > 0.7 else 2)):
        s = 1 if i % 2 else -1
        ax.add_patch(Ellipse((x + s*0.17, y + h*f), 0.30, 0.13, angle=s*22,
                             fc=col, ec=col, lw=0.6, alpha=0.55, zorder=3))
    ax.add_patch(Circle((x, y + h + 0.06), 0.085, fc='#d9c6e6', ec='#6a4a78',
                        lw=0.8, zorder=5))
    ax.text(x, y - 0.20, lab, ha='center', fontsize=7.2, color=INK)
# ---- P generation ----
ax.text(-3.45, 4.38, 'P', fontsize=8.5, color=MUTED, ha='center')
plant(-1.55, 4.05, 1.05, TALLC, 'TT  (tall)')
ax.text(-0.35, 4.55, '×', fontsize=11, color=INK, ha='center', va='center')
plant(0.85, 4.05, 0.40, DW, 'tt  (dwarf)')
# ---- gametes ----
for x, g, c in ((-1.55, 'T', TALLC), (0.85, 't', DW)):
    ax.annotate('', xy=(x, 3.12), xytext=(x, 3.72),
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.0, mutation_scale=9))
    ax.add_patch(Circle((x, 2.92), 0.20, fc='#eef2f7', ec=c, lw=1.1))
    ax.text(x, 2.92, g, ha='center', va='center', fontsize=8, color=c)
ax.text(-3.45, 2.92, 'gametes', fontsize=7.6, color=MUTED, ha='center')
# ---- F1 ----
ax.annotate('', xy=(-0.45, 2.22), xytext=(-1.45, 2.74),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.0, mutation_scale=9))
ax.annotate('', xy=(-0.25, 2.22), xytext=(0.75, 2.74),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.0, mutation_scale=9))
ax.text(-3.45, 1.92, 'F$_1$', fontsize=8.5, color=MUTED, ha='center')
plant(-0.35, 1.55, 1.00, TALLC, 'Tt  (all tall)')
ax.text(1.35, 2.05, 'self-\npollinated', fontsize=6.8, color=MUTED, ha='left',
        va='center', linespacing=1.3)
ax.annotate('', xy=(1.30, 2.05), xytext=(0.45, 2.05),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.0, mutation_scale=9))
# ---- F2 Punnett ----
C = 0.82; X0, Y0 = -1.15, -1.32
gam = ['T', 't']
cells = [['TT', 'Tt'], ['Tt', 'tt']]
for j, g in enumerate(gam):
    ax.add_patch(Rectangle((X0 + j*C, Y0 + 2*C), C, 0.42, fc='#dfe9f2', ec='#aab0ba', lw=0.8))
    ax.text(X0 + j*C + C/2, Y0 + 2*C + 0.21, g, ha='center', va='center', fontsize=9, color=INK)
    ax.add_patch(Rectangle((X0 - 0.42, Y0 + (1-j)*C), 0.42, C, fc='#dfe9f2', ec='#aab0ba', lw=0.8))
    ax.text(X0 - 0.21, Y0 + (1-j)*C + C/2, g, ha='center', va='center', fontsize=9, color=INK)
for i in range(2):
    for j in range(2):
        gt = cells[i][j]
        fc = '#cfe3d4' if 'T' in gt else '#f6e2c8'
        ax.add_patch(Rectangle((X0 + j*C, Y0 + (1-i)*C), C, C, fc=fc, ec='#8f96a3', lw=0.9))
        ax.text(X0 + j*C + C/2, Y0 + (1-i)*C + C/2 + 0.10, gt, ha='center', va='center',
                fontsize=9.5, color=INK)
        ax.text(X0 + j*C + C/2, Y0 + (1-i)*C + C/2 - 0.20, 'tall' if 'T' in gt else 'dwarf',
                ha='center', va='center', fontsize=6.2,
                color=TALLC if 'T' in gt else DW)
ax.text(X0 + C, Y0 + 2*C + 0.62, 'male gametes', ha='center', fontsize=7, color=MUTED)
ax.text(X0 - 0.62, Y0 + C, 'female\ngametes', ha='center', va='center', fontsize=7,
        color=MUTED, rotation=90, linespacing=1.2)
ax.text(-3.45, Y0 + C, 'F$_2$', fontsize=8.5, color=MUTED, ha='center', va='center')
ax.text(1.05, Y0 + 1.22, 'Genotypic ratio', fontsize=7.4, color=INK, ha='left')
ax.text(1.05, Y0 + 0.92, '1 TT : 2 Tt : 1 tt', fontsize=7.8, color=ACCENT, ha='left')
ax.text(1.05, Y0 + 0.46, 'Phenotypic ratio', fontsize=7.4, color=INK, ha='left')
ax.text(1.05, Y0 + 0.16, '3 tall : 1 dwarf', fontsize=7.8, color=ACCENT, ha='left')
ax.set_xlim(-3.95, 4.15); ax.set_ylim(-1.85, 5.55); ax.axis('off')
```

Two laws follow.

::: definition Mendel's first two laws
**Law of dominance.** When two contrasting alleles are brought together in a
hybrid, only one — the dominant — is expressed; the other, the recessive,
remains unexpressed but unchanged.

**Law of segregation (law of purity of gametes).** The two alleles of a pair
separate from each other during gamete formation, so that every gamete receives
only one of them. A gamete is never hybrid.
:::

The cytological basis is **anaphase I of meiosis**, when the two homologous
chromosomes carrying T and t move to opposite poles.

::: example Worked example 3.1 — monohybrid numbers
**Problem.** A pure tall pea plant is crossed with a dwarf one. The F₁ plants
are self-pollinated and give 1,200 F₂ plants. (a) How many are expected to be
tall and how many dwarf? (b) How many of the tall plants breed true? (c) If one
tall F₂ plant is picked at random, what is the probability that it is
heterozygous?

**Solution.**

P: TT × tt → F₁ all **Tt** (tall). F₁ selfed: Tt × tt is *not* the cross — it is
Tt × Tt, giving the genotypic ratio 1 TT : 2 Tt : 1 tt.

(a) Phenotypes are 3 tall : 1 dwarf, so

$$ \text{tall} = \frac{3}{4}\times 1200 = 900, \qquad \text{dwarf} = \frac{1}{4}\times 1200 = 300 $$

(b) True-breeding tall plants are TT, which is 1/4 of the F₂:

$$ TT = \frac{1}{4}\times 1200 = 300 $$

(c) Among the 900 tall plants, 300 are TT and 600 are Tt, so

$$ P(\text{heterozygous} \mid \text{tall}) = \frac{600}{900} = \frac{2}{3} $$
:::

### Test cross and back cross

A tall plant may be TT or Tt, and the two look identical. The genotype is
revealed by a **test cross** — crossing the individual with the homozygous
recessive (dwarf). If the plant is TT, every offspring is tall; if it is Tt, the
offspring are 1 tall : 1 dwarf. The test cross therefore **converts a hidden
genotype into a visible ratio**, and the F₁ ratio is a direct copy of the gamete
ratio of the unknown parent.

```figure caption="Test cross. The offspring ratio directly reveals whether the tall parent was homozygous or heterozygous."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, axs = plt.subplots(1, 2, figsize=(5.2, 2.8), gridspec_kw=dict(wspace=0.30))
TALLC = "#2e8b57"; DW = "#b8860b"
def cross(ax, title, top, side, cells, ratio):
    C = 0.90
    n = len(side)
    for j, g in enumerate(top):
        ax.add_patch(Rectangle((j*C, n*C), C, 0.44, fc='#dfe9f2', ec='#aab0ba', lw=0.8))
        ax.text(j*C + C/2, n*C + 0.22, g, ha='center', va='center', fontsize=9, color=INK)
    for i, g in enumerate(side):
        ax.add_patch(Rectangle((-0.44, (len(side)-1-i)*C), 0.44, C, fc='#dfe9f2',
                               ec='#aab0ba', lw=0.8))
        ax.text(-0.22, (len(side)-1-i)*C + C/2, g, ha='center', va='center',
                fontsize=9, color=INK)
    for i in range(len(side)):
        for j in range(len(top)):
            gt = cells[i][j]
            fc = '#cfe3d4' if 'T' in gt else '#f6e2c8'
            ax.add_patch(Rectangle((j*C, (len(side)-1-i)*C), C, C, fc=fc,
                                   ec='#8f96a3', lw=0.9))
            ax.text(j*C + C/2, (len(side)-1-i)*C + C/2 + 0.11, gt, ha='center',
                    va='center', fontsize=9.5, color=INK)
            ax.text(j*C + C/2, (len(side)-1-i)*C + C/2 - 0.20,
                    'tall' if 'T' in gt else 'dwarf', ha='center', va='center',
                    fontsize=6.2, color=TALLC if 'T' in gt else DW)
    ax.set_title(title, fontsize=7.8, pad=3)
    ax.text(C*len(top)/2, -0.38, ratio, ha='center', fontsize=7.6, color=ACCENT)
    ax.set_xlim(-0.70, C*len(top) + 0.30)
    ax.set_ylim(-0.62, len(side)*C + 0.72)
    ax.set_aspect('equal'); ax.axis('off')
cross(axs[0], '(a)  TT  ×  tt', ['T', 'T'], ['t', 't'],
      [['Tt', 'Tt'], ['Tt', 'Tt']], 'all tall  —  parent was TT')
cross(axs[1], '(b)  Tt  ×  tt', ['T', 't'], ['t', 't'],
      [['Tt', 'tt'], ['Tt', 'tt']], '1 tall : 1 dwarf  —  parent was Tt')
```

::: caution Test cross is not the same as back cross
Every test cross is a back cross, but not every back cross is a test cross. A
back cross uses **either** parent; a test cross uses only the **homozygous
recessive** parent. If the question says "test cross", the second parent must be
the recessive one.
:::

::: example Worked example 3.2 — reading a test cross
**Problem.** A pea plant with violet flowers, whose genotype is unknown, is test
crossed. Out of 80 offspring, 38 have violet flowers and 42 have white flowers.
(a) What was the genotype of the violet parent? (b) What proportion of gametes
of that parent carried the recessive allele?

**Solution.** Let V = violet (dominant), v = white. The tester is vv.

The offspring are close to 1 violet : 1 white. If the parent had been VV, every
offspring would have received a V and all would be violet. A 1 : 1 ratio can
only come from a parent producing two kinds of gametes in equal numbers, so the
parent was **Vv**.

$$ Vv \times vv \;\longrightarrow\; \tfrac{1}{2}\,Vv\ (\text{violet}) \;+\; \tfrac{1}{2}\,vv\ (\text{white}) $$

(b) Half the gametes carried v, i.e. **50 %**. The observed 38 : 42 is a normal
sampling deviation from the expected 40 : 40.
:::

### Dihybrid cross and independent assortment

Mendel next followed two characters at once. He crossed a pure round-yellow
seeded plant (RRYY) with a pure wrinkled-green one (rryy). All F₁ seeds were
round and yellow (RrYy). Selfing the F₁ gave four phenotypes in the ratio
**9 round yellow : 3 round green : 3 wrinkled yellow : 1 wrinkled green**.

A double heterozygote RrYy makes $2^{2} = 4$ kinds of gamete — RY, Ry, rY and ry
— in equal numbers, because the R/r pair segregates independently of the Y/y
pair. Combining four kinds of male gamete with four kinds of female gamete gives
the 16 boxes of the Punnett square.

```figure caption="Dihybrid cross. The 16 boxes give the F₂ ratio 9 round yellow : 3 round green : 3 wrinkled yellow : 1 wrinkled green."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.0, 4.4))
gam = ['RY', 'Ry', 'rY', 'ry']
COL = {'RY': '#cfe3d4', 'Ry': '#e6ddc2', 'rY': '#dfe9f2', 'ry': '#f1d9d6'}
def pheno(g):
    R = 'R' in g; Y = 'Y' in g
    return ('round yellow' if Y else 'round green') if R else \
           ('wrinkled yellow' if Y else 'wrinkled green')
FILL = {'round yellow': '#cfe3d4', 'round green': '#e6ddc2',
        'wrinkled yellow': '#dfe9f2', 'wrinkled green': '#f1d9d6'}
C = 1.02
for j, g in enumerate(gam):
    ax.add_patch(Rectangle((j*C, 4*C), C, 0.50, fc='#dfe9f2', ec='#aab0ba', lw=0.8))
    ax.text(j*C + C/2, 4*C + 0.25, g, ha='center', va='center', fontsize=8.5, color=INK)
    ax.add_patch(Rectangle((-0.50, (3-j)*C), 0.50, C, fc='#dfe9f2', ec='#aab0ba', lw=0.8))
    ax.text(-0.25, (3-j)*C + C/2, g, ha='center', va='center', fontsize=8.5, color=INK)
count = {}
for i, gi in enumerate(gam):
    for j, gj in enumerate(gam):
        gt = ''.join(sorted(gi[0] + gj[0], key=str.lower)) + \
             ''.join(sorted(gi[1] + gj[1], key=str.lower))
        ph = pheno(gt); count[ph] = count.get(ph, 0) + 1
        ax.add_patch(Rectangle((j*C, (3-i)*C), C, C, fc=FILL[ph], ec='#8f96a3', lw=0.9))
        ax.text(j*C + C/2, (3-i)*C + C/2, gt, ha='center', va='center',
                fontsize=8.6, color=INK)
ax.text(2*C, 4*C + 0.74, 'gametes of the male parent  (RrYy)', ha='center',
        fontsize=7.2, color=MUTED)
ax.text(-0.80, 2*C, 'gametes of the female parent  (RrYy)', va='center',
        ha='center', fontsize=7.2, color=MUTED, rotation=90)
order = ['round yellow', 'round green', 'wrinkled yellow', 'wrinkled green']
for k, ph in enumerate(order):
    y = -0.42 - k*0.34
    ax.add_patch(Rectangle((0.10, y - 0.11), 0.26, 0.22, fc=FILL[ph],
                           ec='#8f96a3', lw=0.8))
    ax.text(0.48, y, f'{count[ph]}  {ph}', fontsize=7.4, color=INK, va='center')
ax.text(3.32, -0.72, '9 : 3 : 3 : 1', fontsize=10.5, color=ACCENT, ha='center')
ax.text(3.32, -1.20, 'each character alone\nstill gives 3 : 1', fontsize=6.8,
        color=MUTED, ha='center', linespacing=1.3)
ax.set_xlim(-1.05, 4*C + 0.25); ax.set_ylim(-1.75, 4*C + 0.95)
ax.set_aspect('equal'); ax.axis('off')
```

::: definition Mendel's third law
**Law of independent assortment.** When two pairs of contrasting characters are
followed together, the members of one pair assort into the gametes independently
of the members of the other pair. Consequently, every possible combination of
alleles appears in the gametes with equal frequency.
:::

Notice that each character taken separately still shows 3 : 1 — in the 16 boxes
there are 12 round : 4 wrinkled and 12 yellow : 4 green. The 9 : 3 : 3 : 1 ratio
is simply $(3:1)\times(3:1)$. This is the **product rule**: the probability of
two independent events happening together is the product of their separate
probabilities.

| Number of heterozygous pairs, $n$ | Kinds of gamete | F₂ phenotypes | F₂ genotypes | Size of Punnett square |
|---|---|---|---|---|
| 1 | 2 | 2 | 3 | 4 |
| 2 | 4 | 4 | 9 | 16 |
| 3 | 8 | 8 | 27 | 64 |
| $n$ | $2^{n}$ | $2^{n}$ | $3^{n}$ | $4^{n}$ |

::: example Worked example 3.3 — dihybrid numbers
**Problem.** In *Pisum sativum*, round (R) is dominant to wrinkled (r) and
yellow (Y) to green (y). A plant of genotype RrYy is self-pollinated and
produces 1,600 seeds. Find (a) the number of seeds in each of the four
phenotypic classes, (b) the number of seeds of genotype RrYy, and (c) the
probability that a randomly chosen round yellow seed is homozygous for both
genes.

**Solution.** RrYy × RrYy gives 9 : 3 : 3 : 1 out of 16.

(a) Multiply each fraction by 1600:

$$ \frac{9}{16}\times1600 = 900\ \text{round yellow}, \qquad \frac{3}{16}\times1600 = 300\ \text{round green} $$
$$ \frac{3}{16}\times1600 = 300\ \text{wrinkled yellow}, \qquad \frac{1}{16}\times1600 = 100\ \text{wrinkled green} $$

(b) For one gene, Rr × Rr gives Rr with probability 1/2; likewise Yy. By the
product rule,

$$ P(RrYy) = \tfrac{1}{2}\times\tfrac{1}{2} = \tfrac{1}{4}, \qquad
0.25 \times 1600 = 400\ \text{seeds} $$

(c) Round yellow seeds are 9 of the 16 boxes; only one of those boxes is RRYY.
So

$$ P(RRYY \mid \text{round yellow}) = \frac{1}{9} $$
:::

### Testing a ratio: the chi-square test

Real counts never match the expected ratio exactly. The **chi-square ($\chi^2$)
goodness-of-fit test** decides whether the difference is small enough to be due
to chance.

$$ \chi^{2} = \sum \frac{(O - E)^{2}}{E} $$

where $O$ is the observed number and $E$ the expected number in each class.
The **degrees of freedom** are $df = n - 1$, where $n$ is the number of classes.
Compare the calculated value with the critical value at the 5 % level:

| $df$ | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Critical $\chi^{2}$ at $p = 0.05$ | 3.841 | 5.991 | 7.815 | 9.488 | 11.070 |

If calculated $\chi^{2}$ **is less than** the critical value, the deviation is
not significant and the hypothesis (the expected ratio) is accepted.

::: example Worked example 3.4 — chi-square test of a 9:3:3:1 ratio
**Problem.** Mendel's F₂ from a dihybrid cross gave 315 round yellow, 108 round
green, 101 wrinkled yellow and 32 wrinkled green seeds, a total of 556. Test
whether these agree with a 9 : 3 : 3 : 1 ratio.

**Solution.** Expected numbers are $\frac{9}{16}, \frac{3}{16}, \frac{3}{16},
\frac{1}{16}$ of 556:

$$ E_1 = \frac{9\times556}{16} = 312.75, \quad E_2 = E_3 = \frac{3\times556}{16} = 104.25,
\quad E_4 = \frac{556}{16} = 34.75 $$

| Class | $O$ | $E$ | $O-E$ | $(O-E)^2/E$ |
|---|---|---|---|---|
| Round yellow | 315 | 312.75 | +2.25 | 0.016 |
| Round green | 108 | 104.25 | +3.75 | 0.135 |
| Wrinkled yellow | 101 | 104.25 | −3.25 | 0.101 |
| Wrinkled green | 32 | 34.75 | −2.75 | 0.218 |
| **Total** | **556** | **556** | 0 | **0.470** |

$$ \chi^{2} = 0.016 + 0.135 + 0.101 + 0.218 = 0.470 $$

There are 4 classes, so $df = 4 - 1 = 3$ and the critical value at $p = 0.05$ is
**7.815**. Since $0.470 < 7.815$, the deviation is not significant: the data
**agree with the 9 : 3 : 3 : 1 ratio**.
:::

::: caution Chi-square uses numbers, never percentages
$O$ and $E$ must be actual counts of individuals. Feeding percentages or
fractions into the formula gives a meaningless answer. Also, $E$ is calculated
from the *same* total as $O$ — the two columns must add to the same number.
:::

### Deviations from Mendelism

**Incomplete dominance.** Neither allele is fully dominant, and the heterozygote
is intermediate. In the four o'clock plant *Mirabilis jalapa* (and in
*Antirrhinum majus*, the snapdragon), red (RR) × white (rr) gives **pink** (Rr).
Selfing the F₁ gives 1 red : 2 pink : 1 white — the phenotypic ratio is now the
**same as the genotypic ratio**, 1 : 2 : 1.

**Codominance.** Both alleles are fully expressed in the heterozygote, side by
side, without blending. In cattle, red (C^R^C^R^) × white (C^W^C^W^) gives
**roan** — a coat with red hairs and white hairs mixed, not pink hairs. In humans
the I^A^I^B^ genotype gives blood group AB, with **both** A and B antigens on
the red cells.

```figure caption="(a) Incomplete dominance in *Mirabilis jalapa*: the F₂ ratio is 1 : 2 : 1. (b) Codominance in cattle: the roan coat carries both kinds of hair."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
fig, axs = plt.subplots(1, 2, figsize=(5.2, 3.2), gridspec_kw=dict(wspace=0.22,
                        width_ratios=[1.25, 1.0]))
RED = "#c0392b"; WHT = "#f4f4f2"; PNK = "#e79aa0"
# ---------- (a) incomplete dominance ----------
ax = axs[0]
def flower(x, y, r, fc, lab, sub):
    for a in np.linspace(0, 2*np.pi, 6)[:-1]:
        ax.add_patch(Circle((x + r*0.78*np.cos(a), y + r*0.78*np.sin(a)), r*0.58,
                            fc=fc, ec='#7a4b4b', lw=0.8, zorder=3))
    ax.add_patch(Circle((x, y), r*0.38, fc='#e8c95a', ec='#7a4b4b', lw=0.7, zorder=4))
    ax.text(x, y - r*2.05, lab, ha='center', fontsize=7.2, color=INK)
    ax.text(x, y - r*2.68, sub, ha='center', fontsize=6.4, color=MUTED)
flower(0.75, 4.35, 0.36, RED, 'RR', 'red')
ax.text(2.05, 4.35, '×', fontsize=11, ha='center', va='center', color=INK)
flower(3.35, 4.35, 0.36, WHT, 'rr', 'white')
ax.annotate('', xy=(2.05, 3.05), xytext=(2.05, 3.45),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.0, mutation_scale=9))
flower(2.05, 2.70, 0.36, PNK, 'Rr', 'F$_1$ all pink')
ax.text(3.15, 2.70, 'selfed', fontsize=6.6, color=MUTED, ha='left', va='center')
C = 0.80; X0, Y0 = 1.00, -0.42
for j, g in enumerate(['R', 'r']):
    ax.add_patch(Rectangle((X0 + j*C, Y0 + 2*C), C, 0.34, fc='#dfe9f2', ec='#aab0ba', lw=0.8))
    ax.text(X0 + j*C + C/2, Y0 + 2*C + 0.17, g, ha='center', va='center', fontsize=8.5)
    ax.add_patch(Rectangle((X0 - 0.34, Y0 + (1-j)*C), 0.34, C, fc='#dfe9f2', ec='#aab0ba', lw=0.8))
    ax.text(X0 - 0.17, Y0 + (1-j)*C + C/2, g, ha='center', va='center', fontsize=8.5)
cells = [['RR', 'Rr'], ['Rr', 'rr']]
for i in range(2):
    for j in range(2):
        gt = cells[i][j]
        fc = RED if gt == 'RR' else (WHT if gt == 'rr' else PNK)
        ax.add_patch(Rectangle((X0 + j*C, Y0 + (1-i)*C), C, C, fc=fc, ec='#8f96a3', lw=0.9))
        ax.text(X0 + j*C + C/2, Y0 + (1-i)*C + C/2, gt, ha='center', va='center',
                fontsize=9, color='white' if gt == 'RR' else INK)
ax.text(X0 + C, Y0 - 0.34, '1 red : 2 pink : 1 white', ha='center', fontsize=7.4, color=ACCENT)
ax.set_title('(a) incomplete dominance', fontsize=7.8, pad=2)
ax.set_xlim(0.10, 4.25); ax.set_ylim(-1.15, 5.15); ax.set_aspect('equal'); ax.axis('off')
# ---------- (b) codominance ----------
ax = axs[1]
def coat(x, y, kind):
    ax.add_patch(Circle((x, y), 0.62, fc='#ffffff', ec=MUTED, lw=1.0, zorder=2))
    rng = np.random.default_rng(7)
    pts = []
    while len(pts) < 90:
        p = rng.uniform(-0.58, 0.58, 2)
        if p[0]**2 + p[1]**2 < 0.33: pts.append(p)
    for k, p in enumerate(pts):
        if kind == 'red': c = RED
        elif kind == 'white': c = '#c9ccd2'
        else: c = RED if k % 2 else '#c9ccd2'
        ax.plot([x + p[0]], [y + p[1]], marker='o', ms=2.3, color=c, zorder=3)
coat(0.80, 3.55, 'red');   ax.text(0.80, 2.34, '$C^{R}C^{R}$\nred', ha='center',
                                   fontsize=7.0, color=INK, linespacing=1.3)
ax.text(1.95, 3.55, '×', fontsize=11, ha='center', va='center', color=INK)
coat(3.10, 3.55, 'white'); ax.text(3.10, 2.34, '$C^{W}C^{W}$\nwhite', ha='center',
                                   fontsize=7.0, color=INK, linespacing=1.3)
ax.annotate('', xy=(1.95, 1.95), xytext=(1.95, 2.45),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.0, mutation_scale=9))
coat(1.95, 1.30, 'roan');  ax.text(1.95, 0.10, '$C^{R}C^{W}$\nroan', ha='center',
                                   fontsize=7.0, color=INK, linespacing=1.3)
ax.text(1.95, -0.72, 'both kinds of hair\nappear — no blending', ha='center',
        fontsize=6.6, color=MUTED, linespacing=1.3)
ax.set_title('(b) codominance', fontsize=7.8, pad=2)
ax.set_xlim(0.05, 3.90); ax.set_ylim(-1.30, 4.55); ax.set_aspect('equal'); ax.axis('off')
```

**Multiple alleles.** A gene may have more than two alleles in the population,
although any one diploid individual carries only two of them. The standard
example is the human **ABO blood group**, controlled by the gene *I* with three
alleles: I^A^, I^B^ and i. I^A^ and I^B^ are codominant with each other and both
are dominant over i.

```figure caption="Inheritance of the ABO blood groups. A cross between group A and group B heterozygotes can give all four groups."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, axs = plt.subplots(1, 2, figsize=(5.2, 2.9),
                        gridspec_kw=dict(width_ratios=[1.30, 1.0], wspace=0.16))
# ---------- table ----------
ax = axs[0]
rows = [['Genotype', 'Group', 'Antigen', 'Antibody'],
        ['$I^{A}I^{A}$, $I^{A}i$', 'A', 'A', 'anti-B'],
        ['$I^{B}I^{B}$, $I^{B}i$', 'B', 'B', 'anti-A'],
        ['$I^{A}I^{B}$', 'AB', 'A and B', 'none'],
        ['$ii$', 'O', 'none', 'anti-A, anti-B']]
w = [1.30, 0.62, 0.86, 1.22]; h = 0.46
for r, row in enumerate(rows):
    x = 0.0
    for c, cell in enumerate(row):
        fc = '#dfe9f2' if r == 0 else ('#f7f9fb' if r % 2 else '#ffffff')
        ax.add_patch(Rectangle((x, -r*h), w[c], h, fc=fc, ec='#aab0ba', lw=0.7))
        ax.text(x + w[c]/2, -r*h + h/2, cell, ha='center', va='center',
                fontsize=6.3 if r else 6.8, color=INK)
        x += w[c]
ax.text(sum(w)/2, 0.66, 'ABO blood groups', ha='center', fontsize=7.6, color=INK)
ax.text(0.0, -5*h + 0.10, 'three alleles: $I^{A}$, $I^{B}$, $i$   ·   $I^{A}$ and $I^{B}$'
        ' are codominant,\nboth dominant over $i$', fontsize=6.4, color=MUTED,
        ha='left', va='top', linespacing=1.4)
ax.set_xlim(-0.12, sum(w) + 0.12); ax.set_ylim(-5*h - 0.65, 0.95); ax.axis('off')
# ---------- Punnett ----------
ax = axs[1]
top = ['$I^{A}$', '$i$']; side = ['$I^{B}$', '$i$']
cells = [['$I^{A}I^{B}$', '$I^{B}i$'], ['$I^{A}i$', '$ii$']]
phen = [['AB', 'B'], ['A', 'O']]
FILL = {'A': '#cfe3d4', 'B': '#dfe9f2', 'AB': '#e6ddc2', 'O': '#f1d9d6'}
C = 1.00
for j, g in enumerate(top):
    ax.add_patch(Rectangle((j*C, 2*C), C, 0.40, fc='#eef2f7', ec='#aab0ba', lw=0.8))
    ax.text(j*C + C/2, 2*C + 0.20, g, ha='center', va='center', fontsize=8)
for i, g in enumerate(side):
    ax.add_patch(Rectangle((-0.40, (1-i)*C), 0.40, C, fc='#eef2f7', ec='#aab0ba', lw=0.8))
    ax.text(-0.20, (1-i)*C + C/2, g, ha='center', va='center', fontsize=8)
for i in range(2):
    for j in range(2):
        ax.add_patch(Rectangle((j*C, (1-i)*C), C, C, fc=FILL[phen[i][j]],
                               ec='#8f96a3', lw=0.9))
        ax.text(j*C + C/2, (1-i)*C + C/2 + 0.14, cells[i][j], ha='center',
                va='center', fontsize=8)
        ax.text(j*C + C/2, (1-i)*C + C/2 - 0.22, 'group ' + phen[i][j],
                ha='center', va='center', fontsize=6.2, color=MUTED)
ax.text(C, 2*C + 0.66, 'father  $I^{A}i$  (A)', ha='center', fontsize=7.0, color=INK)
ax.text(-0.72, C, 'mother  $I^{B}i$  (B)', va='center', ha='center', fontsize=7.0,
        color=INK, rotation=90)
ax.text(C, -0.40, '1 AB : 1 A : 1 B : 1 O', ha='center', fontsize=7.4, color=ACCENT)
ax.set_xlim(-0.95, 2*C + 0.15); ax.set_ylim(-0.70, 2*C + 0.90)
ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 3.5 — blood groups and parentage
**Problem.** A woman of blood group O gives birth to a child of blood group B.
She names a man of blood group AB as the father, but he denies it and points to
another man of group O. (a) Can the AB man be the father? (b) Can the O man be
the father? (c) If a group A man (heterozygous) marries a group B woman
(heterozygous), what is the chance that their first child is group O?

**Solution.**

(a) Mother is group O = **ii**, so she can give only **i**. The child is group B,
which must be I^B^I^B^ or I^B^i. Since one allele came from the mother and it was
i, the child must be **I^B^i**, and the I^B^ came from the father. The AB man is
I^A^I^B^ and *can* donate I^B^. **Yes — he could be the father.**

(b) A group O man is ii and can donate only i. A child of ii × ii is always ii,
i.e. group O. **No — the group O man cannot be the father.**

(c) I^A^i × I^B^i gives four equally likely genotypes: I^A^I^B^ (AB), I^A^i (A),
I^B^i (B) and ii (O). So

$$ P(\text{group O}) = \frac{1}{4} = 25\ \% $$
:::

::: caution Blood groups prove exclusion, not paternity
A blood-group test can show that a man **cannot** be the father. It can never
prove that he **is**, because millions of other men share the same group. Write
"could be" and "cannot be", never "is".
:::

**Lethal genes.** Some alleles kill the homozygote. In maize and in snapdragon,
chlorophyll-deficient seedlings die, so a cross between two heterozygous green
plants gives 3 green : 1 white, but the white ones die and the surviving ratio
becomes **2 green : 1 white-carrier green**, i.e. a modified 2 : 1 ratio.

### Sex determination

Sex is decided by a special pair of chromosomes, the **sex chromosomes** or
**allosomes**; the rest are **autosomes**. Humans have 22 pairs of autosomes plus
one pair of sex chromosomes (44 + XX in the female, 44 + XY in the male).

| Type | Female | Male | Examples |
|---|---|---|---|
| XX–XY | XX (homogametic) | XY (heterogametic) | humans, *Drosophila*, *Melandrium album* |
| XX–XO | XX | XO (one X, no Y) | grasshopper, cockroach, *Dioscorea* |
| ZZ–ZW | ZW (heterogametic) | ZZ | birds, butterflies, some fish |
| Haplo-diploid | diploid (fertilised egg) | haploid (unfertilised egg) | honey bee, ant, wasp |

```figure caption="Sex determination of the XX–XY type. The father's sperm decides the sex of the child; the expected ratio is 1 girl : 1 boy."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
fig, ax = plt.subplots(figsize=(4.6, 2.9))
PINK = "#f1d9d6"; BLUE = "#dfe9f2"
ax.text(-1.55, 3.05, 'mother  44 + XX', fontsize=7.6, color=INK, ha='center')
ax.text(1.55, 3.05, 'father  44 + XY', fontsize=7.6, color=INK, ha='center')
ax.text(0.0, 3.05, '×', fontsize=11, color=INK, ha='center')
for x, gs, c in ((-1.55, ['X', 'X'], '#c0392b'), (1.55, ['X', 'Y'], ACCENT)):
    for k, g in enumerate(gs):
        cx = x + (k - 0.5)*0.72
        ax.annotate('', xy=(cx, 2.30), xytext=(x, 2.78),
                    arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.9, mutation_scale=8))
        ax.add_patch(Circle((cx, 2.08), 0.21, fc='#f7f9fb', ec=c, lw=1.1))
        ax.text(cx, 2.08, g, ha='center', va='center', fontsize=8.5, color=c)
ax.text(-3.05, 2.08, 'gametes', fontsize=7.2, color=MUTED, ha='center', va='center')
C = 0.94; X0, Y0 = -0.95, -0.55
top = ['X', 'Y']; side = ['X', 'X']
cells = [['XX', 'XY'], ['XX', 'XY']]
for j, g in enumerate(top):
    ax.add_patch(Rectangle((X0 + j*C, Y0 + 2*C), C, 0.38, fc=BLUE, ec='#aab0ba', lw=0.8))
    ax.text(X0 + j*C + C/2, Y0 + 2*C + 0.19, g, ha='center', va='center', fontsize=8.5)
for i, g in enumerate(side):
    ax.add_patch(Rectangle((X0 - 0.38, Y0 + (1-i)*C), 0.38, C, fc=PINK, ec='#aab0ba', lw=0.8))
    ax.text(X0 - 0.19, Y0 + (1-i)*C + C/2, g, ha='center', va='center', fontsize=8.5)
for i in range(2):
    for j in range(2):
        gt = cells[i][j]
        fc = PINK if gt == 'XX' else BLUE
        ax.add_patch(Rectangle((X0 + j*C, Y0 + (1-i)*C), C, C, fc=fc, ec='#8f96a3', lw=0.9))
        ax.text(X0 + j*C + C/2, Y0 + (1-i)*C + C/2 + 0.13, '44 + ' + gt, ha='center',
                va='center', fontsize=7.6, color=INK)
        ax.text(X0 + j*C + C/2, Y0 + (1-i)*C + C/2 - 0.20,
                'girl' if gt == 'XX' else 'boy', ha='center', va='center',
                fontsize=6.6, color='#c0392b' if gt == 'XX' else ACCENT)
ax.text(X0 + C, Y0 + 2*C + 0.62, 'sperm', ha='center', fontsize=7.2, color=MUTED)
ax.text(X0 - 0.66, Y0 + C, 'ova', va='center', ha='center', fontsize=7.2,
        color=MUTED, rotation=90)
ax.text(X0 + C, Y0 - 0.38, '1 girl : 1 boy', ha='center', fontsize=8, color=ACCENT)
ax.set_xlim(-3.55, 3.25); ax.set_ylim(-1.15, 3.45); ax.axis('off')
```

Because the mother can give only an X, **the sex of the child is decided by the
father's sperm**. Blaming the mother for the sex of a baby, still common in parts
of Nepal, has no biological basis.

### Sex-linked inheritance

Genes on the X chromosome, other than in the tiny region it shares with Y, have
**no partner allele in the male**. A male is therefore **hemizygous**: a single
recessive allele on his one X is enough to show the character. This is why
**red–green colour blindness** and **haemophilia** are far commoner in men.

The pattern is called **criss-cross inheritance**: an affected father passes the
allele to all his daughters (who become carriers) but to none of his sons; a
carrier mother passes it to half her sons, who are affected.

::: example Worked example 3.6 — a sex-linked probability
**Problem.** A woman with normal colour vision, whose father was colour blind,
marries a man with normal colour vision. Using X^C^ for the normal allele and
X^c^ for the colour-blind allele, find (a) the genotypes of the parents,
(b) the expected proportion of colour-blind children, and (c) the probability
that their first son is colour blind.

**Solution.**

(a) Her father was X^c^Y. A father gives his only X to every daughter, so she
received X^c^ from him and X^C^ from her mother. She is a **carrier, X^C^X^c^**.
Her husband has normal vision, so he is **X^C^Y**.

(b) The cross X^C^X^c^ × X^C^Y gives four equally likely offspring:

| | X^C^ (from father) | Y (from father) |
|---|---|---|
| **X^C^** | X^C^X^C^ normal girl | X^C^Y normal boy |
| **X^c^** | X^C^X^c^ carrier girl | X^c^Y colour-blind boy |

One of the four is colour blind, so

$$ P(\text{colour blind child}) = \tfrac{1}{4} = 25\ \% $$

All the daughters see normally, though half of them are carriers.

(c) Among sons only, half are X^c^Y:

$$ P(\text{colour blind} \mid \text{son}) = \tfrac{1}{2} = 50\ \% $$
:::

### Pedigree analysis

A **pedigree** is a family tree drawn with standard symbols. It is the geneticist's
substitute for a controlled cross in humans, where crosses cannot be arranged.

```figure caption="Pedigree analysis. (a) The standard symbols. (b) An autosomal recessive trait — it skips generations and affects both sexes. (c) An X-linked recessive trait — only males are affected, through carrier mothers."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Wedge
fig = plt.figure(figsize=(5.2, 4.6))
gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.85], hspace=0.20, wspace=0.14)
axk = fig.add_subplot(gs[0, :]); axa = fig.add_subplot(gs[1, 0]); axb = fig.add_subplot(gs[1, 1])
S = 0.30                                   # half-size of a symbol
def male(ax, x, y, fill='none', z=5):
    ax.add_patch(Rectangle((x-S, y-S), 2*S, 2*S, fc='#ffffff', ec=INK, lw=1.1, zorder=z))
    if fill == 'full':
        ax.add_patch(Rectangle((x-S, y-S), 2*S, 2*S, fc=INK, ec=INK, lw=1.1, zorder=z+1))
    elif fill == 'carrier':
        ax.add_patch(Rectangle((x-S, y-S), S, 2*S, fc=INK, ec='none', zorder=z+1))
        ax.add_patch(Rectangle((x-S, y-S), 2*S, 2*S, fc='none', ec=INK, lw=1.1, zorder=z+2))
    elif fill == 'dot':
        ax.add_patch(Circle((x, y), S*0.30, fc=INK, ec=INK, zorder=z+1))
def female(ax, x, y, fill='none', z=5):
    ax.add_patch(Circle((x, y), S, fc='#ffffff', ec=INK, lw=1.1, zorder=z))
    if fill == 'full':
        ax.add_patch(Circle((x, y), S, fc=INK, ec=INK, lw=1.1, zorder=z+1))
    elif fill == 'carrier':
        ax.add_patch(Wedge((x, y), S, 90, 270, fc=INK, ec='none', zorder=z+1))
        ax.add_patch(Circle((x, y), S, fc='none', ec=INK, lw=1.1, zorder=z+2))
    elif fill == 'dot':
        ax.add_patch(Circle((x, y), S*0.30, fc=INK, ec=INK, zorder=z+1))
def marry(ax, x1, x2, y, cons=False):
    ax.plot([x1+S, x2-S], [y, y], color=INK, lw=1.0, zorder=3)
    if cons:
        ax.plot([x1+S, x2-S], [y-0.09, y-0.09], color=INK, lw=1.0, zorder=3)
def sibs(ax, xs, ytop, ykid, dropx=None):
    xm = (min(xs)+max(xs))/2 if dropx is None else dropx
    ax.plot([xm, xm], [ytop, ytop-0.34], color=INK, lw=1.0, zorder=3)
    ax.plot([min(xs), max(xs)], [ytop-0.34, ytop-0.34], color=INK, lw=1.0, zorder=3)
    for x in xs:
        ax.plot([x, x], [ytop-0.34, ykid+S], color=INK, lw=1.0, zorder=3)
# ---------------- (a) key ----------------
ax = axk
items = [('male', lambda x, y: male(ax, x, y)),
         ('female', lambda x, y: female(ax, x, y)),
         ('affected\nmale', lambda x, y: male(ax, x, y, 'full')),
         ('affected\nfemale', lambda x, y: female(ax, x, y, 'full')),
         ('carrier\nfemale', lambda x, y: female(ax, x, y, 'carrier')),
         ('deceased', lambda x, y: (male(ax, x, y),
              ax.plot([x-S*1.3, x+S*1.3], [y-S*1.3, y+S*1.3], color=INK, lw=1.0, zorder=9)))]
for k, (lab, fn) in enumerate(items):
    x = 0.55 + k*1.28; fn(x, 0.72)
    ax.text(x, 0.06, lab, ha='center', va='top', fontsize=6.2, color=INK, linespacing=1.25)
x = 0.55 + 6*1.28
male(ax, x - 0.30, 0.72); female(ax, x + 0.62, 0.72); marry(ax, x - 0.30, x + 0.62, 0.72)
ax.text(x + 0.16, 0.06, 'mating/\nmarriage line', ha='center', va='top', fontsize=6.2,
        color=INK, linespacing=1.25)
xa = 0.55 + 7.7*1.28
male(ax, xa, 0.72)
ax.annotate('', xy=(xa-S-0.04, 0.72-S-0.04), xytext=(xa-S-0.46, 0.72-S-0.42),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.0, mutation_scale=9))
ax.text(xa, 0.06, 'proband\n(arrow)', ha='center', va='top', fontsize=6.2, color=INK,
        linespacing=1.25)
ax.set_title('(a) standard pedigree symbols', fontsize=7.8, pad=2, loc='left')
ax.set_xlim(-0.35, 11.1); ax.set_ylim(-0.85, 1.35); ax.set_aspect('equal'); ax.axis('off')
# ---------------- (b) autosomal recessive ----------------
ax = axa
y1, y2, y3 = 2.60, 1.35, 0.10
male(ax, 0.9, y1); female(ax, 2.7, y1); marry(ax, 0.9, 2.7, y1)
ax.text(0.30, y1, 'I', fontsize=7, color=MUTED, ha='right', va='center')
sibs(ax, [0.7, 1.8, 2.9], y1, y2)
male(ax, 0.7, y2); female(ax, 1.8, y2, 'full'); male(ax, 2.9, y2)
female(ax, 4.0, y2); marry(ax, 2.9, 4.0, y2)
ax.text(0.30, y2, 'II', fontsize=7, color=MUTED, ha='right', va='center')
sibs(ax, [2.8, 3.7, 4.6], y2, y3, dropx=3.45)
male(ax, 2.8, y3, 'full'); female(ax, 3.7, y3); male(ax, 4.6, y3)
ax.text(0.30, y3, 'III', fontsize=7, color=MUTED, ha='right', va='center')
ax.text(2.6, -0.85, 'affected girl in II from\nunaffected parents;\nboth sexes affected',
        fontsize=6.4, color=MUTED, ha='center', va='top', linespacing=1.35)
ax.set_title('(b) autosomal recessive', fontsize=7.8, pad=2, loc='left')
ax.set_xlim(0.0, 5.3); ax.set_ylim(-1.75, 3.25); ax.set_aspect('equal'); ax.axis('off')
# ---------------- (c) X-linked recessive ----------------
ax = axb
male(ax, 0.9, y1); female(ax, 2.7, y1, 'carrier'); marry(ax, 0.9, 2.7, y1)
ax.text(0.30, y1, 'I', fontsize=7, color=MUTED, ha='right', va='center')
sibs(ax, [0.7, 1.8, 2.9], y1, y2)
male(ax, 0.7, y2, 'full'); male(ax, 1.8, y2); female(ax, 2.9, y2, 'carrier')
male(ax, 4.0, y2); marry(ax, 2.9, 4.0, y2)
sibs(ax, [3.0, 3.9], y2, y3, dropx=3.45)
male(ax, 3.0, y3, 'full'); female(ax, 3.9, y3, 'carrier')
ax.text(0.30, y2, 'II', fontsize=7, color=MUTED, ha='right', va='center')
ax.text(0.30, y3, 'III', fontsize=7, color=MUTED, ha='right', va='center')
ax.text(2.6, -0.85, 'only males affected;\npassed on by carrier\nmothers (criss-cross)',
        fontsize=6.4, color=MUTED, ha='center', va='top', linespacing=1.35)
ax.set_title('(c) X-linked recessive', fontsize=7.8, pad=2, loc='left')
ax.set_xlim(0.0, 5.3); ax.set_ylim(-1.75, 3.25); ax.set_aspect('equal'); ax.axis('off')
```

Reading a pedigree follows four questions, in this order:

1. **Does the trait appear in every generation?** If yes, suspect **dominant**;
   if it skips a generation, suspect **recessive**.
2. **Do two unaffected parents have an affected child?** If yes, the trait is
   certainly **recessive** and the parents are carriers.
3. **Are both sexes affected equally?** If yes, the gene is **autosomal**; if
   almost all the affected are male, suspect **X-linked**.
4. **Does an affected father pass it to every daughter but no son?** That is
   the signature of an **X-linked** gene.

::: example Worked example 3.7 — analysing a pedigree
**Problem.** In figure (b) above, an unaffected couple in generation I have an
affected daughter (II-2). Their unaffected son (II-3) marries an unrelated
unaffected woman and they have an affected son (III-1). (a) Is the gene dominant
or recessive, autosomal or sex-linked? (b) Give the genotypes of the couple in
generation I. (c) If the couple II-3 × II-4 have another child, what is the
probability that it is affected?

**Solution.** Let the alleles be A (normal) and a (affected).

(a) Two unaffected parents in generation I produced an **affected daughter**.
A trait that is absent in the parents but present in the child must be
**recessive**. It cannot be X-linked recessive, because an X-linked recessive
daughter would need an affected father (she gets one X from him), and her father
is normal. So the gene is **autosomal recessive**.

(b) Each parent in generation I is unaffected but has passed an a allele to
II-2, who is aa. Both must therefore be heterozygous: **Aa × Aa**.

(c) II-3 is unaffected and comes from Aa × Aa, so he is Aa with probability 2/3
and AA with probability 1/3. His wife II-4 must also be a carrier, because their
son III-1 is aa — so she is **Aa** for certain, and II-3 must in fact also be
**Aa** (he gave an a to III-1). For a known Aa × Aa couple,

$$ P(\text{affected child}) = \tfrac{1}{4} = 25\ \% $$
:::

## 3.3 Linkage and crossing over

### Linkage

Mendel's third law works only for genes on **different** chromosomes. Each
chromosome carries hundreds of genes, and genes on the same chromosome travel
together into the same gamete. This tendency is **linkage**.

The first evidence came from **Bateson and Punnett (1906)** working on the sweet
pea *Lathyrus odoratus*. They crossed a purple-flowered, long-pollen plant
(PPLL) with a red-flowered, round-pollen plant (ppll). The F₁ were all purple
long, as expected, but the F₂ did not fit 9 : 3 : 3 : 1:

| F₂ class | Observed | Expected on 9:3:3:1 |
|---|---|---|
| Purple, long | 284 | 214.3 |
| Purple, round | 21 | 71.4 |
| Red, long | 21 | 71.4 |
| Red, round | 55 | 23.8 |
| **Total** | **381** | **381** |

The two **parental** combinations were far commoner than expected and the two
**new** combinations far rarer. Bateson and Punnett explained this with the
**coupling and repulsion hypothesis**: alleles that entered the cross together
tend to stay together (coupling, or *cis*), while those that entered apart tend
to stay apart (repulsion, or *trans*).

**T. H. Morgan (1910)**, working on *Drosophila melanogaster*, showed that
coupling and repulsion are simply two arrangements of the same phenomenon, and
gave it the name **linkage**. He proposed that linked genes lie on the same
chromosome and that the strength of linkage depends on the **distance** between
them: the closer two genes are, the more tightly they are linked.

::: definition Linkage
Linkage is the tendency of two or more genes located on the same chromosome to
be inherited together into the same gamete, so that they do not assort
independently. A group of all the genes on one chromosome forms a **linkage
group**, and the number of linkage groups in an organism equals its **haploid
chromosome number**.
:::

| Organism | 2n | Linkage groups (n) |
|---|---|---|
| *Pisum sativum* | 14 | 7 |
| *Zea mays* | 20 | 10 |
| *Drosophila melanogaster* | 8 | 4 |
| *Homo sapiens* | 46 | 23 |

Linkage is of two kinds. In **complete linkage** the linked genes are always
inherited together and no new combination appears; it is rare, and is seen in
the male *Drosophila* and the female silkworm *Bombyx mori*, where crossing over
does not occur. In **incomplete linkage** a few new combinations do appear,
because crossing over separates the genes in a small proportion of meioses. Most
linkage is of this second type.

### Crossing over

::: definition Crossing over
Crossing over is the mutual exchange of corresponding segments between
**non-sister chromatids** of a pair of homologous chromosomes. It takes place in
the **pachytene stage of prophase I of meiosis**, at points called **chiasmata**,
and produces new (recombinant) combinations of linked genes.
:::

The steps are: **synapsis** (pairing of homologues to form a bivalent in
zygotene) → **duplication** (each homologue is already two chromatids, so the
bivalent is a tetrad) → **chiasma formation** and breakage of two non-sister
chromatids at exactly corresponding points (pachytene) → **reunion** of the
broken pieces with the opposite chromatid, catalysed by endonuclease and ligase
→ **terminalisation** of the chiasmata in diplotene and diakinesis. The
**chiasmatype theory** of Janssens (1909) states that a chiasma is the visible
result of a crossover that has already happened.

```figure caption="Crossing over between two non-sister chromatids of a bivalent. Two chromatids stay parental (AB, ab) and two become recombinant (Ab, aB)."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle
fig, axs = plt.subplots(1, 2, figsize=(5.2, 3.4), gridspec_kw=dict(width_ratios=[1.0, 1.25],
                        wspace=0.16))
C1 = "#1d6fb8"; C2 = "#d9534f"
def gene(ax, x, y, letter, col):
    ax.add_patch(Circle((x, y), 0.155, fc='#ffffff', ec=col, lw=1.2, zorder=6))
    ax.text(x, y, letter, ha='center', va='center', fontsize=7.6, color=INK, zorder=7)
def cent(ax, x, y):
    ax.add_patch(Circle((x, y), 0.105, fc='#ffffff', ec=INK, lw=1.0, zorder=7))
# ---------------- (a) bivalent with one chiasma ----------------
ax = axs[0]
xs = [0.30, 0.66, 1.44, 1.80]
TOP, BOT, CH1, CH2 = 3.00, 0.00, 1.70, 1.34
ax.plot([xs[0]]*2, [BOT, TOP], color=C1, lw=5.0, solid_capstyle='round', zorder=4)
ax.plot([xs[3]]*2, [BOT, TOP], color=C2, lw=5.0, solid_capstyle='round', zorder=4)
ax.plot([xs[1], xs[1], xs[2], xs[2]], [TOP, CH1, CH2, BOT], color=C1, lw=5.0,
        solid_capstyle='round', solid_joinstyle='round', zorder=5)
ax.plot([xs[2], xs[2], xs[1], xs[1]], [TOP, CH1, CH2, BOT], color=C2, lw=5.0,
        solid_capstyle='round', solid_joinstyle='round', zorder=5)
for x in xs:
    cent(ax, x, 2.30)
gene(ax, xs[0], 2.76, 'A', C1); gene(ax, xs[1], 2.76, 'A', C1)
gene(ax, xs[2], 2.76, 'a', C2); gene(ax, xs[3], 2.76, 'a', C2)
for x, l, c in ((xs[0], 'B', C1), (xs[1], 'B', C1), (xs[2], 'b', C2), (xs[3], 'b', C2)):
    gene(ax, x, 0.40, l, c)
ax.annotate('chiasma', xy=(1.05, 1.52), xytext=(2.30, 1.52), fontsize=7.0, color=INK,
            ha='left', va='center',
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.9, mutation_scale=9))
ax.annotate('centromere', xy=(xs[3] + 0.10, 2.30), xytext=(2.30, 2.44), fontsize=7.0,
            color=INK, ha='left', va='center',
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.9, mutation_scale=9))
ax.text(0.48, 3.28, 'paternal', fontsize=7.0, color=C1, ha='center')
ax.text(1.62, 3.28, 'maternal', fontsize=7.0, color=C2, ha='center')
ax.set_title('(a) pachytene: a bivalent', fontsize=7.8, pad=4, loc='left')
ax.set_xlim(-0.20, 3.40); ax.set_ylim(-0.75, 3.62); ax.axis('off')
# ---------------- (b) the four chromatids produced ----------------
ax = axs[1]
combos = [('A', 'B', C1, C1, 'parental'), ('A', 'b', C1, C2, 'recombinant'),
          ('a', 'B', C2, C1, 'recombinant'), ('a', 'b', C2, C2, 'parental')]
for k, (t, b, ct, cb, kind) in enumerate(combos):
    x = 0.45 + k*0.96
    ax.plot([x, x], [1.54, 3.00], color=ct, lw=5.0, solid_capstyle='round', zorder=4)
    ax.plot([x, x], [0.00, 1.46], color=cb, lw=5.0, solid_capstyle='round', zorder=4)
    cent(ax, x, 1.50)
    gene(ax, x, 2.40, t, ct)
    gene(ax, x, 0.50, b, cb)
    ax.text(x, -0.30, t + b, ha='center', fontsize=8.4, color=INK)
    ax.text(x, -0.62, kind, ha='center', fontsize=5.7, color=MUTED)
ax.text(1.89, 3.28, 'the four chromatids of the tetrad', fontsize=7.0, color=MUTED,
        ha='center')
ax.set_title('(b) after crossing over', fontsize=7.8, pad=4, loc='left')
ax.set_xlim(-0.05, 3.85); ax.set_ylim(-0.75, 3.62); ax.axis('off')
```
**Kinds of crossing over.** A **single** crossover involves one chiasma between
two chromatids; a **double** crossover has two chiasmata in the same pair; and a
**multiple** crossover has more than two. Double crossovers between two genes
restore the parental combination and so make genes look closer together than
they are.

**Factors affecting the frequency of crossing over:**

- **Distance between the genes** — the chief factor; the farther apart, the more
  often a chiasma falls between them.
- **Sex** — absent in male *Drosophila* and female *Bombyx mori*; generally
  higher in the female.
- **Age** — frequency falls in older organisms.
- **Temperature** — very high and very low temperatures increase it.
- **Radiation and chemicals** — X-rays and some chemicals raise it.
- **Distance from the centromere** — crossing over is rare very close to the
  centromere.

### Gene mapping

Because the chance of a chiasma falling between two genes is proportional to the
distance between them, the **recombination frequency** measures that distance:

$$ \text{RF} = \frac{\text{number of recombinant offspring}}{\text{total offspring}} \times 100\ \% $$

Sturtevant (1913) defined **one map unit (1 centiMorgan, cM) = 1 % recombination**,
and used recombination frequencies to draw the first **genetic map**, showing
that genes lie in a fixed linear order on the chromosome. The maximum observable
recombination frequency is 50 %, which is the same result as independent
assortment; genes more than 50 cM apart therefore appear unlinked.

::: example Worked example 3.8 — recombination frequency and map distance
**Problem.** In *Zea mays*, coloured aleurone (C) is dominant to colourless (c),
and full endosperm (Sh) to shrunken (sh). A plant heterozygous for both genes was
test crossed with a colourless, shrunken plant. The offspring were:

coloured full 4032, coloured shrunken 149, colourless full 152, colourless
shrunken 4035.

(a) Are the genes linked? (b) Find the recombination frequency and the map
distance. (c) Write the genotype of the heterozygous parent.

**Solution.**

(a) A test cross of a double heterozygote on unlinked genes would give
1 : 1 : 1 : 1. Here two classes are huge and two are tiny, so the genes are
**linked**.

(b) Total offspring $= 4032 + 149 + 152 + 4035 = 8368$. The two rare classes are
the recombinants, $149 + 152 = 301$:

$$ \text{RF} = \frac{301}{8368}\times 100 = 3.60\ \% $$

So the two genes are **3.6 map units (3.6 cM) apart**.

(c) The parental (commonest) classes are coloured-full and colourless-shrunken,
so C travelled with Sh and c with sh. The heterozygote was in the **coupling
(*cis*) arrangement**, written **C Sh / c sh**.
:::

::: caution Recombinants are the rare classes, not the recessive ones
In a linkage test cross, identify the recombinants by **frequency**, not by
appearance. The two *smallest* classes are always the recombinants, whatever
phenotypes they happen to show.
:::

| | Linkage | Crossing over |
|---|---|---|
| Effect on genes | keeps linked genes together | separates linked genes |
| Result | parental combinations | recombinant (new) combinations |
| Frequency | high for close genes | low for close genes |
| Stage | acts throughout meiosis | pachytene of prophase I |
| Relation to distance | decreases with distance | increases with distance |
| Evolutionary value | keeps useful combinations intact | creates variation |

## 3.4 Mutation and polyploidy

### Mutation

::: definition Mutation
A mutation is a sudden, random, heritable change in the genetic material of an
organism that is not caused by segregation or recombination. The term was coined
by **Hugo de Vries (1901)** from his work on the evening primrose *Oenothera
lamarckiana*.
:::

Mutations are **sudden** (they appear in one step, not gradually), **random**
(they cannot be directed towards a need), **heritable** if they occur in
germ cells, **recurrent**, usually **recessive** and usually **harmful**,
because any random change in a finely tuned system is more likely to damage it
than improve it. They are also **rare** — typically 1 in 10⁵ to 10⁶ gametes per
gene per generation.

Mutations are classified in three ways:

| Basis | Types |
|---|---|
| Cell involved | **somatic** (body cells; not inherited, e.g. a bud sport) and **germinal** (gametes; inherited) |
| Origin | **spontaneous** (natural, from replication errors) and **induced** (by a mutagen) |
| Extent | **gene (point) mutation** and **chromosomal mutation** |

**Gene or point mutations** change one or a few base pairs.

- **Substitution** — one base pair is replaced by another. A **transition**
  replaces a purine by a purine (or pyrimidine by pyrimidine); a
  **transversion** replaces a purine by a pyrimidine or the reverse.
  A substitution may be **silent** (the codon still codes for the same amino
  acid, because the code is degenerate), **missense** (a different amino acid) or
  **nonsense** (a stop codon appears and the chain is cut short).
- **Frameshift** — insertion or deletion of bases in a number that is **not a
  multiple of three**. Every codon after the change is misread, so the whole
  protein downstream is wrong. Frameshifts are far more damaging than
  substitutions.

The classic example of a missense mutation is **sickle-cell anaemia**: a single
substitution GAG → GTG in the gene for the β-chain of haemoglobin puts **valine
in place of glutamic acid** at the sixth amino acid, and the altered haemoglobin
makes the red cells sickle-shaped when oxygen is low.

**Chromosomal mutations (aberrations)** change chromosome structure or number.
The four structural changes are shown below.

```figure caption="Structural chromosomal aberrations. The normal chromosome carries the gene order A B C D E F."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.0, 3.4))
PAL = {'A': '#cfe3d4', 'B': '#dfe9f2', 'C': '#f6e2c8', 'D': '#e6d6ea',
       'E': '#f1d9d6', 'F': '#dde7d8', 'M': '#fdf0c2', 'N': '#ffe0b5'}
W, H = 0.40, 0.32
def chrom(x, y, letters, label=None, col=None):
    for k, L in enumerate(letters):
        ax.add_patch(Rectangle((x + k*W, y), W, H, fc=PAL.get(L, '#eeeeee'),
                               ec=INK, lw=0.8))
        ax.text(x + k*W + W/2, y + H/2, L, ha='center', va='center',
                fontsize=7.4, color=INK)
    if label:
        ax.text(x - 0.16, y + H/2, label, ha='right', va='center', fontsize=6.8,
                color=col or MUTED)
rows = [
    ('Deletion', ['A','B','C','D','E','F'], ['A','B','E','F'], 'segment C D is lost'),
    ('Duplication', ['A','B','C','D','E','F'], ['A','B','C','C','D','E','F'],
     'segment C is repeated'),
    ('Inversion', ['A','B','C','D','E','F'], ['A','B','D','C','E','F'],
     'segment C D is turned round'),
]
y = 3.30
for name, norm, mut, note in rows:
    ax.text(-0.10, y + 0.66, name, fontsize=7.8, color=INK, ha='left', va='bottom')
    chrom(0.55, y + 0.28, norm, 'normal')
    chrom(0.55, y - 0.18, mut, 'changed', col=ACCENT)
    ax.annotate('', xy=(0.42, y - 0.02), xytext=(0.42, y + 0.34),
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.9, mutation_scale=8))
    ax.text(3.62, y + 0.08, note, fontsize=6.6, color=MUTED, ha='left', va='center')
    y -= 1.26
ax.text(-0.10, y + 0.66, 'Translocation', fontsize=7.8, color=INK, ha='left', va='bottom')
chrom(0.55, y + 0.28, ['A','B','C','D'], 'normal')
chrom(2.45, y + 0.28, ['M','N'])
chrom(0.55, y - 0.18, ['A','B','N'], 'changed', col=ACCENT)
chrom(2.05, y - 0.18, ['M','C','D'])
ax.annotate('', xy=(0.42, y - 0.02), xytext=(0.42, y + 0.34),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.9, mutation_scale=8))
ax.text(3.62, y + 0.08, 'segments swapped between\ntwo non-homologous chromosomes',
        fontsize=6.6, color=MUTED, ha='left', va='center', linespacing=1.35)
ax.set_xlim(-0.35, 6.75); ax.set_ylim(y - 0.42, 4.30); ax.axis('off')
```
Changes in **number** are of two kinds. **Euploidy** is a change by whole sets
(n, 3n, 4n …). **Aneuploidy** is a change of one or a few individual
chromosomes:

| Aneuploid | Formula | Human example |
|---|---|---|
| Nullisomy | 2n − 2 | lethal in humans |
| Monosomy | 2n − 1 | Turner's syndrome, 45, XO |
| Trisomy | 2n + 1 | Down's syndrome, 47, trisomy-21; Klinefelter's, 47, XXY |
| Tetrasomy | 2n + 2 | rare |

Aneuploidy arises from **non-disjunction** — the failure of a homologous pair
(or of sister chromatids) to separate at anaphase, so that one gamete gets an
extra chromosome and the other gets none.

**Mutagens** are agents that raise the mutation rate: **physical** — X-rays,
gamma rays, UV light (which makes thymine dimers), high temperature;
**chemical** — mustard gas, nitrous acid, ethyl methane sulphonate (EMS), base
analogues such as 5-bromouracil, acridine dyes (which cause frameshifts), and
colchicine; **biological** — transposons and some viruses.

::: key Why mutation matters
Mutation is the **only original source of new alleles**. Recombination and
crossing over merely shuffle alleles that already exist; mutation creates them.
Without mutation there would be no raw material for natural selection and no
evolution. In agriculture, **mutation breeding** with gamma rays or EMS has
produced short-strawed, early-maturing and disease-resistant varieties of rice,
wheat and barley.
:::

### Polyploidy

::: definition Polyploidy
Polyploidy is the presence of more than two complete sets of chromosomes in a
cell or organism — triploid (3n), tetraploid (4n), hexaploid (6n) and so on. It
arises when the chromosomes duplicate but the cell fails to divide, or when
unreduced (2n) gametes fuse.
:::

It is common in flowering plants — roughly half of all angiosperm species are
polyploid — but rare in animals, where it upsets sex determination.

**Autopolyploidy** multiplies the chromosome set of a **single** species
(AA → AAAA). Examples: tetraploid potato *Solanum tuberosum* (2n = 4x = 48),
triploid banana (2n = 3x = 33) and triploid seedless watermelon, tetraploid
*Citrullus* and the giant forms of *Datura*.

**Allopolyploidy** (amphidiploidy) combines the chromosome sets of **two
different** species, usually after a sterile hybrid doubles its chromosomes
(AB → AABB). Examples: bread wheat *Triticum aestivum* (2n = 6x = 42),
*Gossypium hirsutum* (New World cotton), *Nicotiana tabacum*, *Brassica napus*,
*Triticale* (*Triticum* × *Secale cereale*, the first man-made cereal) and
*Raphanobrassica*, produced by Karpechenko in 1928 by crossing radish
*Raphanus sativus* with cabbage *Brassica oleracea*.

| | Autopolyploidy | Allopolyploidy |
|---|---|---|
| Source of sets | one species | two different species |
| Constitution | AAAA | AABB |
| Pairing at meiosis | multivalents form | normal bivalents |
| Fertility | often low | usually fertile |
| Examples | potato, banana, watermelon | *Triticum aestivum*, *Raphanobrassica*, *Triticale* |

Polyploidy is induced artificially with **colchicine**, an alkaloid from
*Colchicum autumnale*, which destroys the spindle so that the doubled
chromosomes stay in one nucleus. Its effects include the **gigas effect** —
larger cells, thicker leaves, bigger flowers and fruits — greater vigour and
more chemical content; and, in odd-numbered polyploids such as 3n, **sterility**,
because an odd number of sets cannot pair evenly at meiosis. That sterility is
useful: it is exactly why bananas and triploid watermelons are seedless.

::: caution Polyploidy is not aneuploidy
Polyploidy changes the number of **whole sets** (3n, 4n); aneuploidy changes the
number of **individual chromosomes** (2n + 1, 2n − 1). Down's syndrome is
aneuploidy, not polyploidy; bread wheat is polyploidy, not aneuploidy.
:::

## Chapter summary

- **DNA is the genetic material** — Griffith's transformation, Avery's enzyme
  test, and the Hershey–Chase ³²P/³⁵S experiment; in some viruses (TMV) it is
  RNA. Chargaff's rules: A = T, G = C, so A + G = T + C.
- **B-DNA** is a right-handed antiparallel double helix, diameter **2 nm**,
  pitch **3.4 nm**, **10 bp per turn**, rise **0.34 nm** per base pair; A=T has
  two hydrogen bonds, G≡C has three.
- **Replication is semi-conservative** (Meselson–Stahl): helicase opens the
  fork, primase lays an RNA primer, DNA polymerase III builds only 5′ → 3′, so
  one strand is **leading** (continuous) and one **lagging** (Okazaki fragments
  joined by ligase).
- **Central dogma**: DNA → (transcription) → mRNA → (translation) → protein. The
  code is a **triplet, degenerate, non-overlapping, comma-less and nearly
  universal** code of 64 codons; AUG starts, UAA, UAG and UGA stop.
- **Mendel's laws**: dominance, segregation (monohybrid 3 : 1 phenotypic,
  1 : 2 : 1 genotypic) and independent assortment (dihybrid **9 : 3 : 3 : 1**;
  test cross **1 : 1 : 1 : 1**). A heterozygote of n genes makes 2ⁿ kinds of
  gamete.
- **Chi-square** tests a ratio: $\chi^2 = \sum (O-E)^2/E$ with df = (classes − 1);
  if $\chi^2$ is **less** than the critical value (3.841 at df = 1, 7.815 at
  df = 3, p = 0.05) the deviation is due to chance and the ratio is accepted.
- **Deviations from Mendelism**: incomplete dominance (1 : 2 : 1, *Mirabilis
  jalapa*), codominance (roan cattle, AB blood), multiple alleles (I^A, I^B, i),
  lethal genes (2 : 1) and sex linkage.
- **Linkage** keeps genes on one chromosome together; **crossing over** at the
  chiasma in pachytene breaks that linkage. Recombination frequency
  $= (\text{recombinants}/\text{total}) \times 100\ \%$, and 1 % = **1 map unit
  (cM)**; the maximum useful value is 50 %.
- **Mutation** is the only source of new alleles: point mutations (substitution —
  transition or transversion; frameshift) and chromosomal mutations (deletion,
  duplication, inversion, translocation; aneuploidy 2n ± 1, euploidy).
  **Polyploidy** is auto- (AAAA, potato, banana) or allo- (AABB, *Triticum
  aestivum*, *Raphanobrassica*, *Triticale*) and is induced by colchicine.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Which nitrogenous base is present in RNA but not in DNA? <span class="marks">[1]</span>
   (a) adenine (b) thymine (c) uracil (d) cytosine
2. In the Watson–Crick model, one complete turn of the DNA helix measures <span class="marks">[1]</span>
   (a) 0.34 nm (b) 2 nm (c) 3.4 nm (d) 20 nm
3. The phenotypic ratio of a dihybrid **test cross** is <span class="marks">[1]</span>
   (a) 9 : 3 : 3 : 1 (b) 1 : 1 : 1 : 1 (c) 3 : 1 (d) 1 : 2 : 1
4. A man of blood group AB marries a woman of group O. Which group can **never** appear among their children? <span class="marks">[1]</span>
   (a) A (b) B (c) AB (d) A and B both
5. Crossing over takes place during <span class="marks">[1]</span>
   (a) leptotene (b) zygotene (c) pachytene (d) diplotene
6. *Raphanobrassica* is an example of <span class="marks">[1]</span>
   (a) autopolyploidy (b) allopolyploidy (c) monosomy (d) trisomy

::: note Answers to Group A
**1.** (c) — RNA has uracil in place of thymine.
**2.** (c) — the pitch is 3.4 nm; 0.34 nm is the rise per base pair and 2 nm the diameter.
**3.** (b) — the F₁ makes four kinds of gamete in equal numbers and the tester contributes only recessives.
**4.** (c) — the parents can only give I^A or I^B with i, so the children are A (I^A i) or B (I^B i).
**5.** (c) — chiasmata form and the segments are exchanged in pachytene of prophase I.
**6.** (b) — it combines the sets of two species, *Raphanus sativus* and *Brassica oleracea*.
:::

**Group B — Short answer (4 marks each)**

1. State Mendel's law of segregation and illustrate it with a monohybrid cross in pea up to the F₂ generation, giving both ratios. <span class="marks">[4]</span>
2. A pure tall pea plant with round seeds (TTRR) is crossed with a dwarf plant with wrinkled seeds (ttrr). Give the F₁, the gametes of the F₁, the F₂ phenotypic ratio, and the result of test crossing the F₁. <span class="marks">[4]</span>
3. Differentiate between DNA and RNA (any four points) and name the three types of RNA with one function each. <span class="marks">[4]</span>
4. Define linkage and crossing over. In a test cross of a double heterozygote, 1600 offspring were obtained of which 96 were recombinants. Calculate the recombination frequency and the map distance between the two genes. <span class="marks">[4]</span>
5. What is polyploidy? Differentiate between autopolyploidy and allopolyploidy with one example of each, and name the chemical used to induce polyploidy. <span class="marks">[4]</span>

::: note Answers to Group B
**1.** *Law of segregation:* the two alleles of a gene, which stay together in the
body cells of a heterozygote, **separate from each other without being altered**
during gamete formation, so that each gamete receives only one of them.
Cross TT (tall) × tt (dwarf) → F₁ all **Tt, tall**. Selfing the F₁ gives
gametes T and t from each parent, so the F₂ Punnett square gives
TT : Tt : Tt : tt. **Phenotypic ratio 3 tall : 1 dwarf; genotypic ratio
1 TT : 2 Tt : 1 tt.** The reappearance of pure dwarfs in the F₂ proves the
alleles were never blended.

**2.** F₁ = **TtRr**, all tall with round seeds. The F₁ makes 2² = **4 kinds of
gamete**: TR, Tr, tR, tr in equal numbers. Selfing gives the F₂ ratio
**9 tall round : 3 tall wrinkled : 3 dwarf round : 1 dwarf wrinkled**.
A test cross (TtRr × ttrr) gives **1 tall round : 1 tall wrinkled : 1 dwarf
round : 1 dwarf wrinkled**, i.e. 1 : 1 : 1 : 1, which directly reveals the four
gamete types of the F₁.

**3.**

| Feature | DNA | RNA |
|---|---|---|
| Sugar | deoxyribose | ribose |
| Bases | A, T, G, C | A, U, G, C |
| Strands | double (usually) | single (usually) |
| Site | nucleus, mitochondria, plastids | mostly cytoplasm |
| Amount | constant in a species | varies with protein synthesis |

**mRNA** carries the codon message from gene to ribosome; **tRNA** carries an
amino acid and reads the codon with its anticodon; **rRNA** builds the ribosome
and has peptidyl transferase activity.

**4.** *Linkage* is the tendency of genes on the same chromosome to be inherited
together. *Crossing over* is the exchange of corresponding segments between
non-sister chromatids of homologous chromosomes at the chiasma in pachytene,
producing recombinants.

$$ \text{RF} = \frac{96}{1600}\times 100 = 6\ \% $$

Since 1 % recombination = 1 map unit, the two genes lie **6 map units (6 cM)
apart**.

**5.** *Polyploidy* is the presence of more than two complete sets of chromosomes
in a cell. In **autopolyploidy** the extra sets come from the **same** species
(AAAA), pairing gives multivalents and fertility is often low — e.g. tetraploid
potato *Solanum tuberosum* (2n = 4x = 48) or triploid banana. In
**allopolyploidy** the sets come from **two different** species (AABB), pairing
is normal and the plant is fertile — e.g. bread wheat *Triticum aestivum*
(2n = 6x = 42) or *Raphanobrassica*. Polyploidy is induced by **colchicine**,
obtained from *Colchicum autumnale*, which prevents spindle formation.
:::

**Group C — Long answer (8 marks each)**

1. Describe the Watson–Crick model of DNA with a labelled diagram. Explain how
   DNA replicates semi-conservatively, naming the enzymes and explaining why one
   strand is made continuously and the other in fragments. <span class="marks">[8]</span>
2. What is sex-linked inheritance? Explain X-linked recessive inheritance by
   working out a cross between a carrier woman and a normal man for colour
   blindness, and state the criteria by which an X-linked recessive trait is
   recognised in a pedigree. <span class="marks">[8]</span>
3. In a dihybrid cross in pea, the F₂ generation of 160 plants consisted of 95
   tall round, 27 tall wrinkled, 30 dwarf round and 8 dwarf wrinkled. Test
   whether these results agree with the expected 9 : 3 : 3 : 1 ratio using the
   chi-square test, and explain what your conclusion means. <span class="marks">[8]</span>

::: note Answers to Group C
**1. Outline.** (i) DNA is a right-handed double helix of two antiparallel
polynucleotide chains, one running 5′ → 3′ and the other 3′ → 5′.
(ii) Each nucleotide = deoxyribose + phosphate + base; the sugar–phosphate
backbone lies outside, joined by 3′–5′ phosphodiester bonds, and the bases face
inward. (iii) Base pairing is complementary: A = T by two hydrogen bonds, G ≡ C
by three, which satisfies Chargaff's rules and keeps the diameter constant.
(iv) Dimensions: diameter 2 nm, pitch 3.4 nm, 10 base pairs per turn, rise
0.34 nm; major and minor grooves run along the outside. (v) **Replication** is
semi-conservative — each daughter molecule keeps one parental strand, proved by
Meselson and Stahl with ¹⁵N. (vi) Helicase unwinds the helix at the origin,
topoisomerase relieves the strain and single-strand binding proteins hold the
strands apart. (vii) Primase lays a short RNA primer; DNA polymerase III adds
nucleotides **only to a free 3′ end**, so synthesis is always 5′ → 3′.
(viii) Because the two templates are antiparallel, only one of them faces the
fork in the right direction: that new strand is the **leading strand** and grows
continuously, while the other is made backwards in short **Okazaki fragments**
(the **lagging strand**), whose primers are replaced by DNA polymerase I and
whose nicks are sealed by **DNA ligase**. Credit is given for a labelled diagram
of the fork.

**2. Outline.** (i) Genes carried on the sex chromosomes are **sex-linked**;
most lie on the non-homologous part of the X, so they are **X-linked**.
(ii) A male is **hemizygous** — he has only one X, so a single recessive allele
is expressed in him; a female must be homozygous recessive to show the trait.
(iii) Cross X^C X^c (carrier woman) × X^C Y (normal man). Her gametes are X^C and
X^c; his are X^C and Y. The offspring are **X^C X^C, X^C X^c, X^C Y, X^c Y** —
that is, among the daughters half are normal and half carriers, none affected;
among the sons half are normal and **half are colour blind**. Overall 1/4 of the
children, or 1/2 of the sons, are affected. (iv) The trait passes from carrier
mother to son and from affected father to all his daughters as carriers —
**criss-cross inheritance**. (v) Pedigree criteria for an X-linked recessive
trait: far more affected males than females; an affected male's parents are both
unaffected but his mother is a carrier; **no father-to-son transmission**; every
daughter of an affected male is a carrier; affected females appear only when an
affected father marries a carrier or affected mother. Examples: colour blindness,
haemophilia, Duchenne muscular dystrophy.

**3.** Total = 160. Expected numbers on 9 : 3 : 3 : 1 (total parts 16):

| Class | O | E | O − E | (O−E)²/E |
|---|---|---|---|---|
| Tall round | 95 | 90 | +5 | 0.278 |
| Tall wrinkled | 27 | 30 | −3 | 0.300 |
| Dwarf round | 30 | 30 | 0 | 0.000 |
| Dwarf wrinkled | 8 | 10 | −2 | 0.400 |
| **Total** | **160** | **160** | **0** | **0.978** |

E values: $160\times 9/16 = 90$, $160\times 3/16 = 30$, $160\times 3/16 = 30$,
$160\times 1/16 = 10$.

$$ \chi^2 = 0.278 + 0.300 + 0.000 + 0.400 = 0.978 $$

Degrees of freedom $= 4 - 1 = 3$; the critical value at p = 0.05 is **7.815**.
Since $0.978 < 7.815$, the deviation is **not significant**: it is within the
range expected from chance sampling alone. The **null hypothesis is accepted**,
so the data agree with a 9 : 3 : 3 : 1 ratio and the two genes are assorting
independently. Note that the test never proves the hypothesis true — it only
says the data give no reason to reject it.
:::
