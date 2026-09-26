---
subject: Biology
grade: 11
unit: 7
title: Evolutionary Biology
hours: 15
area: Zoology
---

Evolution is the one idea that makes the whole of biology hang together. Every
animal you meet in the next unit is a modified version of something older. This
unit asks three questions in order: how did life begin, what is the *evidence*
that species have changed, and by what *mechanism* did they change? It ends with
our own case, the descent of *Homo sapiens* from a Miocene ape.

::: key What the examiner asks from this unit
Four things recur almost every year: a **difference table** (Lamarckism vs
Darwinism, homologous vs analogous organs, types of isolation); a **labelled
series** (the horse, or the hominid line with dates and cranial capacities); a
short **explain-with-example** question on one evidence of evolution; and a
**Hardy–Weinberg calculation**, the only numerical question in the unit and the
easiest four marks in the paper.
:::

## 7.1 Life and its Origin

The Earth formed about 4.6 billion years ago; the oldest undisputed fossils,
cyanobacterial mats preserved as stromatolites, are about 3.5 billion years old.
Somewhere in that billion years, non-living chemistry became living chemistry.

### Theories that do not work

**Special creation** holds that all forms of life were made at once and have not
changed. It makes no testable prediction and is contradicted by the different
faunas of different rock layers. **Spontaneous generation (abiogenesis)** held
that life arises repeatedly from non-living matter — maggots from rotting meat.
Three experiments killed it.

| Worker | Experiment | Conclusion |
|---|---|---|
| Redi (1668) | meat in open, sealed and gauze-covered jars | maggots only where flies can lay eggs |
| Spallanzani (1767) | boiled broth in sealed flasks stayed sterile | microbes come from the air |
| Pasteur (1864) | broth in a **swan-necked flask** stayed sterile until the neck was broken | air could enter, dust could not — **biogenesis** |

**Biogenesis** — *omne vivum ex vivo* — is therefore the rule now, but it cannot
explain the *first* life, and **panspermia** (life arrived as spores from space)
only moves the problem elsewhere. The surviving explanation is chemical evolution.

### Chemical evolution — the Oparin–Haldane theory

A. I. Oparin (1924) and J. B. S. Haldane (1929) proposed independently that life
arose by slow chemical change under conditions that no longer exist. The
primitive atmosphere was **reducing and had no free oxygen** — methane (CH₄),
ammonia (NH₃), hydrogen (H₂) and water vapour — with ultraviolet light, lightning
and volcanic heat as energy sources and no ozone layer to block the UV.

::: definition Chemical evolution
The origin of life on Earth by a graded series of chemical steps, from simple
inorganic molecules to self-replicating organic systems, under the physical
conditions of the primitive Earth.
:::

1. Inorganic gases → **monomers** (amino acids, sugars, nitrogen bases, fatty
   acids) accumulating in the warm sea — Haldane's **"hot dilute soup"**.
2. Monomers → **polymers**: proteins, polysaccharides, nucleic acids.
3. Polymers aggregated into membrane-bounded droplets — Oparin's **coacervates**,
   Fox's **microspheres** — the first **protobionts**.
4. A self-copying nucleic acid appeared (the **RNA world**), giving heredity and
   the first true **cell**, an **anaerobic heterotroph** feeding on the soup.
5. As the soup ran out, **chemo-** and then **photoautotrophs** evolved.
   Photosynthesis released O₂, which built the ozone layer and ended chemical
   evolution for ever.
6. Free O₂ allowed **aerobic respiration** and so the larger eukaryotes and
   multicellular life.

### The Miller–Urey experiment (1953)

Stanley Miller and Harold Urey tested step 1 in a sealed glass apparatus. A flask
of boiling water fed vapour to an upper chamber charged with CH₄, NH₃ and H₂;
tungsten electrodes sparked for a week at about 800 °C; a condenser returned the
products to a U-trap. The trap collected **amino acids** — glycine, alanine,
aspartic acid — with urea, simple sugars and fatty acids.

::: caution Miller and Urey did not make life
They made the **monomers** of life from inorganic gases, and nothing more — no
protein, no nucleic acid, no cell. "Miller and Urey created life in the
laboratory" is a standard wrong answer.
:::

::: memory The primitive atmosphere
**"I made polythene pipes"** — the gases were **methane, ammonia, hydrogen** and
water vapour, with **no free oxygen**. Writing "oxygen" collapses the whole
answer: oxygen would have destroyed the organic molecules as fast as they formed.
:::

### The geological time scale

Geologists divide Earth history into eras, periods and epochs, with boundaries
drawn where the fossil fauna changes sharply — often at a mass extinction.
Learning the sequence is worth marks: almost every fossil you must name belongs
to a named period.

```figure caption="The geological time scale with the first appearance of major groups. Within each era the periods are drawn to scale, but the four eras are not to the same scale — the Precambrian alone lasted about 4,000 million years, seven times the whole of the rest."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

fig, ax = plt.subplots(figsize=(5.2, 4.6))

ERA_C = {"Precambrian": "#ccd5df", "Palaeozoic": "#bfd8c6",
         "Mesozoic": "#e6d7b2", "Cenozoic": "#e8c6c4"}
DATA = [
 ("Precambrian", 2.00, [("Precambrian\n(4600-541)", 4059,
   "3500 Mya  first prokaryotes (cyanobacteria)\n2400 Mya  free oxygen builds up\n"
   "1500 Mya  first eukaryotes\n 600 Mya  first soft-bodied animals")]),
 ("Palaeozoic", 2.50, [
   ("Cambrian (541-485)", 56, "Cambrian explosion: all major\ninvertebrate phyla; trilobites"),
   ("Ordovician (485-444)", 41, "First jawless fishes (Agnatha)"),
   ("Silurian (444-419)", 25, "First land plants; arthropods on land"),
   ("Devonian (419-359)", 60, "Age of Fishes; first amphibians"),
   ("Carboniferous (359-299)", 60, "Coal-forming forests; first reptiles"),
   ("Permian (299-252)", 47, "Reptiles radiate; largest mass extinction")]),
 ("Mesozoic", 2.05, [
   ("Triassic (252-201)", 51, "First dinosaurs; first mammals"),
   ("Jurassic (201-145)", 56, "Age of Reptiles; first birds"),
   ("Cretaceous (145-66)", 79, "Flowering plants spread; dinosaurs\nextinct at 66 Mya")]),
 ("Cenozoic", 2.45, [
   ("Palaeogene (66-23)", 43, "Age of Mammals begins; Eohippus;\nearly primates"),
   ("Neogene (23-2.6)", 20.4, "Miocene apes: Dryopithecus,\nRamapithecus (Siwaliks)"),
   ("Quaternary (2.6-0)", 2.6, "Ice ages; Homo habilis to Homo sapiens")]),
]

X0, X1 = 0.015, 0.085
P0, P1 = 0.100, 0.215
NAMEX, EVX = 0.235, 0.545

y = 0.10
bars = []
for era, eh, plist in DATA:
    ax.add_patch(Rectangle((X0, y), X1 - X0, eh, facecolor=ERA_C[era],
                           edgecolor=INK, lw=0.8))
    ax.text((X0 + X1) / 2, y + eh / 2, era, rotation=90, ha="center", va="center",
            fontsize=7.4, color=INK, fontweight="bold")
    tot = sum(d for _, d, _ in plist)
    py = y
    for lab, dur, ev in plist:
        h = eh * dur / tot
        ax.add_patch(Rectangle((P0, py), P1 - P0, h, facecolor=ERA_C[era],
                               edgecolor=INK, lw=0.6, alpha=0.75))
        bars.append((lab, py + h / 2, ev))
        py += h
    y += eh
TOP = y

last, prevh = -9.0, 0.0
for lab, mid, ev in bars:
    nl = max(lab.count("\n"), ev.count("\n")) + 1
    h = 0.172 * nl
    ly = max(mid, last + prevh / 2 + h / 2 + 0.07)
    last, prevh = ly, h
    ax.text(NAMEX, ly, lab, ha="left", va="center", fontsize=6.6, color=INK)
    ax.plot([P1 + 0.004, NAMEX - 0.010], [mid, ly], color=MUTED, lw=0.6)
    ax.text(EVX, ly, ev, ha="left", va="center", fontsize=6.3, color=MUTED)

zy = 0.10 + 2.00
zx = np.linspace(X0 - 0.008, P1 + 0.008, 13)
zz = zy + 0.032 * np.array([1, -1] * 7)[:13]
ax.plot(zx, zz, color="#ffffff", lw=2.4, zorder=5)
ax.plot(zx, zz, color=INK, lw=0.8, zorder=6)

for xx, tt, ha in [((X0 + X1) / 2, "Era", "center"), (NAMEX, "Period  (Mya)", "left"),
                   (EVX, "First appearance of major groups", "left")]:
    ax.text(xx, TOP + 0.14, tt, ha=ha, va="bottom", fontsize=7.2,
            color=INK, fontweight="bold")
ax.text(X0, -0.08, "oldest at the bottom; the wavy line marks a change of scale",
        fontsize=5.9, color=MUTED, va="top")
ax.set_xlim(0, 1.03); ax.set_ylim(-0.34, TOP + 0.50)
ax.axis("off")
```

## 7.2 Evidences of evolution

Darwin could not show evolution happening, so he built his case the way a lawyer
does — from converging independent lines of evidence.

### Evidence from morphology and anatomy

Compare the forelimb of a man, a whale, a bat and a horse. The jobs could hardly
differ more — grasping, swimming, flying, running — yet the bones are the *same
bones in the same order*: humerus, radius and ulna, carpals, metacarpals and
phalanges. Only their relative lengths differ. Such organs are **homologous**: one
ancestral pentadactyl limb remodelled for four ways of life, which is **divergent
evolution**. A bird's wing and an insect's wing are the opposite case: both fly,
but one is a bony forelimb with feathers and the other a double fold of cuticle
with no bones. These are **analogous** — unrelated lines meeting the same problem
the same way, or **convergent evolution**.

| Feature | Homologous organs | Analogous organs |
|---|---|---|
| Basic structure and embryonic origin | same | different |
| Function | different | same |
| Ancestry | common ancestor | unrelated ancestors |
| Process shown | divergent evolution | convergent evolution |
| Animal example | forelimbs of man, whale, bat, horse | wing of bird and wing of insect |
| Plant example | thorn of *Bougainvillea*, tendril of *Cucurbita* | sweet potato (root tuber), potato (stem tuber) |
| Meaning | proves common descent | proves adaptation, **not** relationship |

**Vestigial organs** are reduced, functionless remnants of organs that worked in
an ancestor. Man has about 90: the **vermiform appendix** (a functional caecum in
herbivores), the **coccyx** (four fused tail vertebrae), the **plica semilunaris**
(a full third eyelid in frogs and birds), the **auricular muscles** that let a
horse swivel its ear, body hair and the wisdom teeth. A designer would not fit a
useless organ; an ancestor that used it explains it at once.

```figure caption="The three anatomical evidences. (a) Homologous forelimbs — the same bones (colour-coded) remodelled for grasping, swimming and flying. (b) Analogous wings — a bony forelimb and a chitinous fold of body wall, doing the same job. (c) Some of the vestigial organs of man."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon, Rectangle

fig, ax = plt.subplots(figsize=(5.2, 3.73))
ax.set_xlim(0, 15.2); ax.set_ylim(0, 10.9)
ax.set_aspect("equal"); ax.axis("off")

C_H, C_R, C_C, C_D = SERIES[0], SERIES[2], SERIES[3], SERIES[1]

def limb(x, y, Lh, Lr, dig, spread, memb=False, outline=False):
    ax.plot([x, x + Lh], [y, y], color=C_H, lw=4.6,
            solid_capstyle="round", zorder=4)
    for s in (+1, -1):
        ax.plot([x + Lh, x + Lh + Lr], [y + 0.05 * s, y + 0.17 * s],
                color=C_R, lw=2.2, solid_capstyle="round", zorder=4)
    xc = x + Lh + Lr
    for dx, dy in [(0.04, 0.09), (0.22, -0.05), (0.40, 0.07)]:
        ax.add_patch(Circle((xc + dx, y + dy), 0.115, facecolor=C_C,
                            edgecolor="none", zorder=5))
    xc += 0.50
    tips = []
    for L, a in zip(dig, np.linspace(spread, -spread, len(dig))):
        r = np.radians(a)
        tx, ty = xc + L * np.cos(r), y + 0.04 + L * np.sin(r)
        ax.plot([xc, tx], [y + 0.04, ty], color=C_D, lw=1.5,
                solid_capstyle="round", zorder=4)
        tips.append((tx, ty))
    if memb:
        ax.add_patch(Polygon([(x + Lh * 0.45, y - 0.05)] + tips, closed=True,
                             facecolor=C_D, alpha=0.14, edgecolor=C_D,
                             lw=0.7, zorder=1))
    if outline:
        ax.add_patch(Polygon([(x - 0.18, y + 0.30), (x - 0.18, y - 0.30)] + tips,
                             closed=True, facecolor=MUTED, alpha=0.14,
                             edgecolor=MUTED, lw=0.7, zorder=1))
    return tips

# ---------------- (a) homologous ----------------
limb(0.18, 9.05, 1.35, 1.25, [0.72, 0.90, 0.98, 0.90, 0.74], 33)
ax.text(0.18, 9.86, "human arm  (grasping)", fontsize=6.6, color=INK)
limb(0.18, 6.50, 0.85, 0.75, [1.05, 1.20, 1.25, 1.20, 1.02], 13, outline=True)
ax.text(0.18, 7.32, "whale flipper  (swimming)", fontsize=6.6, color=INK)
limb(0.18, 3.90, 1.15, 1.35, [0.50, 1.65, 1.90, 1.80, 1.55], 33, memb=True)
ax.text(0.18, 5.34, "bat wing  (flying)", fontsize=6.6, color=INK)

for k, (c, t) in enumerate([(C_H, "humerus"), (C_R, "radius + ulna"),
                            (C_C, "carpals"), (C_D, "digits (5)")]):
    yy = 2.10 - 0.56 * k
    ax.plot([0.28, 0.86], [yy, yy], color=c, lw=3.4, solid_capstyle="round")
    ax.text(1.02, yy, t, fontsize=6.4, color=MUTED, va="center")

# ---------------- (b) analogous ----------------
def scale(pts, sx, sy, ox, oy):
    return [(ox + px * sx, oy + py * sy) for px, py in pts]

bird = [(0.05, 0.00), (0.42, 0.30), (0.95, 0.22), (1.00, 0.04),
        (0.62, -0.10), (0.20, -0.13)]
BP = scale(bird, 2.25, 2.25, 5.78, 7.60)
ax.add_patch(Polygon(BP, closed=True, facecolor=SERIES[0], alpha=0.20,
                     edgecolor=SERIES[0], lw=1.0))
for f in np.linspace(0.18, 0.92, 7):
    x0 = 5.78 + 2.25 * (0.20 + 0.42 * f)
    ax.plot([x0, x0 + 0.12], [7.60 - 2.25 * (0.13 - 0.03 * f),
                              7.60 - 2.25 * (0.13 - 0.03 * f) - 0.34],
            color=SERIES[0], lw=0.7)
bx, by = 5.95, 7.66
ax.plot([bx, bx + 0.56], [by, by + 0.14], color=C_H, lw=3.0,
        solid_capstyle="round", zorder=4)
ax.plot([bx + 0.56, bx + 1.12], [by + 0.14, by + 0.10], color=C_R, lw=2.0,
        solid_capstyle="round", zorder=4)
ax.plot([bx + 1.12, bx + 1.72], [by + 0.10, by + 0.24], color=C_D, lw=1.3,
        solid_capstyle="round", zorder=4)
ax.text(5.72, 9.86, "bird wing", fontsize=6.8, color=INK, fontweight="bold")
ax.text(5.72, 9.40, "bones inside, skin\nand feathers outside",
        fontsize=6.1, color=MUTED, va="top")

ins = [(0.06, 0.00), (0.34, 0.26), (0.86, 0.20), (1.00, 0.02),
       (0.50, -0.14), (0.16, -0.10)]
IP = scale(ins, 2.25, 2.25, 5.82, 3.40)
ax.add_patch(Polygon(IP, closed=True, facecolor=SERIES[4], alpha=0.18,
                     edgecolor=SERIES[4], lw=1.0))
for f, L in [(0.10, 0.92), (0.26, 0.74), (0.42, 0.56)]:
    ax.plot([5.82 + 0.20, 5.82 + 2.25 * (0.20 + L * 0.80)],
            [3.40 + 0.04, 3.40 + 2.25 * (0.02 + f * 0.55)],
            color=SERIES[4], lw=0.7)
ax.text(5.72, 5.30, "insect wing", fontsize=6.8, color=INK, fontweight="bold")
ax.text(5.72, 4.84, "no bones at all:\na fold of cuticle",
        fontsize=6.1, color=MUTED, va="top")
ax.text(6.92, 6.26, "both fly: same\nfunction, very\ndifferent structure",
        fontsize=6.0, color=SERIES[1], ha="center", va="center")

# ---------------- (c) vestigial ----------------
cx, gy = 11.90, 0.72
ax.add_patch(Circle((cx, 8.78), 0.62, facecolor="#eef1f5",
                    edgecolor=INK, lw=0.9, zorder=3))
ax.add_patch(Ellipse((cx + 0.60, 8.74), 0.26, 0.40, facecolor="#eef1f5",
                     edgecolor=INK, lw=0.9, zorder=2))
ax.add_patch(Circle((cx - 0.22, 8.88), 0.11, facecolor="#ffffff",
                    edgecolor=INK, lw=0.7, zorder=4))
ax.add_patch(Circle((cx - 0.22, 8.88), 0.045, facecolor=INK,
                    edgecolor="none", zorder=5))
ax.add_patch(Rectangle((cx - 0.16, 8.02), 0.32, 0.22, facecolor="#eef1f5",
                       edgecolor=INK, lw=0.9, zorder=2))
ax.add_patch(Polygon([(cx - 0.68, 8.08), (cx + 0.68, 8.08), (cx + 0.82, 6.40),
                      (cx + 0.60, 4.32), (cx - 0.60, 4.32), (cx - 0.82, 6.40)],
                     closed=True, facecolor="#eef1f5", edgecolor=INK,
                     lw=0.9, zorder=2))
for s in (-1, 1):
    ax.plot([cx + s * 0.66, cx + s * 1.02, cx + s * 0.94],
            [7.94, 6.20, 4.64], color=INK, lw=2.2,
            solid_capstyle="round", zorder=1)
    ax.plot([cx + s * 0.34, cx + s * 0.42, cx + s * 0.38],
            [4.34, 2.10, gy + 0.16], color=INK, lw=2.6,
            solid_capstyle="round", zorder=1)
    ax.add_patch(Ellipse((cx + s * 0.50, gy + 0.10), 0.40, 0.18,
                         facecolor=INK, edgecolor="none", zorder=1))
ax.add_patch(Ellipse((cx + 0.34, 5.18), 0.30, 0.52, angle=28,
                     facecolor=SERIES[1], edgecolor=INK, lw=0.7, zorder=4))
ax.add_patch(Ellipse((cx, 4.46), 0.22, 0.40, facecolor=SERIES[4],
                     edgecolor=INK, lw=0.7, zorder=4))
for hy in (6.05, 5.72, 5.39, 5.06):
    ax.plot([cx + 1.00, cx + 1.22], [hy, hy + 0.12], color=MUTED, lw=0.7)

AR = dict(arrowstyle="-", color=MUTED, lw=0.7, shrinkA=1, shrinkB=1)
for txt, tx, ty, ha, px, py in [
        ("nictitating\nmembrane", 10.80, 9.40, "right", cx - 0.30, 8.90),
        ("coccyx\n(tail bones)", 10.80, 4.34, "right", cx - 0.09, 4.46),
        ("auricular\nmuscles", 13.32, 9.10, "left", cx + 0.70, 8.80),
        ("vermiform\nappendix", 13.32, 6.20, "left", cx + 0.46, 5.26),
        ("body hair", 13.32, 4.60, "left", cx + 1.18, 5.16)]:
    ax.annotate(txt, xy=(px, py), xytext=(tx, ty), fontsize=6.1, color=MUTED,
                ha=ha, va="center", arrowprops=AR)

for xs in (5.50, 8.30):
    ax.plot([xs, xs], [0.30, 10.10], color=GRID, lw=0.8)
for xt, tt in [(2.60, "(a) homologous"), (6.90, "(b) analogous"),
               (11.78, "(c) vestigial")]:
    ax.text(xt, 10.42, tt, fontsize=7.6, color=INK,
            fontweight="bold", ha="center", va="center")
```

### Evidence from embryology

**Von Baer's law**: the general characters of a large group appear in the embryo
before the special characters of the species. Early embryos of a fish, a chick and
a human can be confused — each has **pharyngeal (gill) slits**, a **notochord**, a
two-chambered heart and a **post-anal tail** — and the later the differences
appear, the closer the relationship. Haeckel's stronger **theory of
recapitulation** ("ontogeny repeats phylogeny", the embryo passing through the
*adult* stages of its ancestors) is **wrong**. What is true is that related embryos
inherit the same early developmental programme, so useless leftovers persist: gill
slits in a human, teeth in a baleen-whale foetus, a tail at six weeks.

```figure caption="Comparative embryology. At the earliest stage the three embryos are nearly indistinguishable and all three show pharyngeal gill slits and a post-anal tail; species characters appear only later. This is von Baer's law, not Haeckel's recapitulation."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Ellipse

fig, ax = plt.subplots(figsize=(5.2, 4.0))
ax.set_xlim(0, 15.6); ax.set_ylim(0, 12.0)
ax.set_aspect("equal"); ax.axis("off")
BODY = "#eef1f5"

def embryo(cx, cy, L, B, wid, headr, tail, gills, limbs=(),
           beak=False, caudal=False):
    N = 200
    u = np.linspace(0, 1, N)
    th = np.radians(18.0 + B * u)
    sx = np.cumsum(np.cos(th)) * L / N
    sy = np.cumsum(np.sin(th)) * L / N
    w = wid * ((1 - u) ** 0.80 * 0.92 + 0.08)
    nx, ny = -np.sin(th), np.cos(th)          # left of travel = dorsal
    up = np.c_[sx + nx * w, sy + ny * w]
    dn = np.c_[sx - nx * w, sy - ny * w]
    allp = np.vstack([up, dn])
    ox = cx - 0.5 * (allp[:, 0].min() + allp[:, 0].max())
    oy = cy - 0.5 * (allp[:, 1].min() + allp[:, 1].max())
    sx += ox; sy += oy
    ax.add_patch(Polygon(np.vstack([np.c_[sx + nx * w, sy + ny * w],
                                    np.c_[sx - nx * w, sy - ny * w][::-1]]),
                         closed=True, facecolor=BODY, edgecolor=INK,
                         lw=0.9, zorder=3))
    hx = sx[0] - np.cos(th[0]) * headr * 0.55
    hy = sy[0] - np.sin(th[0]) * headr * 0.55
    ax.add_patch(Circle((hx, hy), headr, facecolor=BODY, edgecolor=INK,
                        lw=0.9, zorder=4))
    ax.add_patch(Circle((hx - 0.34 * headr, hy + 0.20 * headr), 0.25 * headr,
                        facecolor=INK, edgecolor="none", zorder=5))
    if beak:
        ax.add_patch(Polygon([(hx - 0.92 * headr, hy + 0.16 * headr),
                              (hx - 1.95 * headr, hy - 0.16 * headr),
                              (hx - 0.86 * headr, hy - 0.50 * headr)],
                             closed=True, facecolor=SERIES[3], edgecolor=INK,
                             lw=0.7, zorder=5))
    for j in range(gills):
        i = 14 + j * 11
        ax.plot([sx[i] - nx[i] * w[i] * 1.0, sx[i] + nx[i] * w[i] * 1.0],
                [sy[i] - ny[i] * w[i] * 1.0, sy[i] + ny[i] * w[i] * 1.0],
                color=SERIES[1], lw=1.5, solid_capstyle="round", zorder=6)
    tx = sx[-1] + np.cos(th[-1]) * tail
    ty = sy[-1] + np.sin(th[-1]) * tail
    ax.plot([sx[-1], tx], [sy[-1], ty], color=INK, lw=1.7,
            solid_capstyle="round", zorder=3)
    if caudal:
        d = np.array([np.cos(th[-1]), np.sin(th[-1])])
        p = np.array([-d[1], d[0]])
        ax.add_patch(Polygon([(tx, ty), (tx + (d * 0.52 + p * 0.46)[0],
                                         ty + (d * 0.52 + p * 0.46)[1]),
                              (tx + d[0] * 0.30, ty + d[1] * 0.30),
                              (tx + (d * 0.52 - p * 0.44)[0],
                               ty + (d * 0.52 - p * 0.44)[1])],
                             closed=True, facecolor=BODY, edgecolor=INK,
                             lw=0.8, zorder=2))
    for frac, d1, d2, bend in limbs:
        i = int(frac * (N - 1))
        a = np.arctan2(-ny[i], -nx[i])
        p1 = (sx[i] - nx[i] * w[i] * 0.85, sy[i] - ny[i] * w[i] * 0.85)
        p2 = (p1[0] + d1 * np.cos(a), p1[1] + d1 * np.sin(a))
        a2 = a + np.radians(bend)
        p3 = (p2[0] + d2 * np.cos(a2), p2[1] + d2 * np.sin(a2))
        ax.plot([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], color=INK,
                lw=2.0 if d2 else 3.2, solid_capstyle="round", zorder=2)
        if d2:
            ax.add_patch(Ellipse(p3, 0.30, 0.18,
                                 angle=np.degrees(a2), facecolor=INK,
                                 edgecolor="none", zorder=2))

COLX = [3.95, 7.45, 10.90]
ROWY = [9.05, 5.65, 2.25]
NAMES = ["fish\n(Labeo)", "chick\n(Gallus)", "human\n(Homo)"]
NOTES = ["gill slits (red) and a\ntail in every early\nembryo",
         "the middle stages are\nstill hard to tell\napart",
         "only at the end do fin,\nbeak, wing and hand\nappear"]
BUD = (0.13, 0.0, 0)

for x, t in zip(COLX, ["early", "middle", "late"]):
    ax.text(x, 11.55, t, fontsize=7.6, color=INK, fontweight="bold", ha="center")
for i, y in enumerate(ROWY):
    ax.text(0.10, y, NAMES[i], fontsize=7.2, color=INK, va="center")
    ax.text(13.00, y, NOTES[i], fontsize=6.2, color=MUTED, va="center")
    ax.plot([1.60, 15.5], [y + 1.70, y + 1.70], color=GRID, lw=0.7)
ax.plot([1.60, 15.5], [ROWY[2] - 1.70, ROWY[2] - 1.70], color=GRID, lw=0.7)
ax.plot([12.72, 12.72], [0.55, 10.75], color=GRID, lw=0.7)

y = ROWY[0]
embryo(COLX[0], y, 2.70, -195, 0.40, 0.46, 0.26, 4)
embryo(COLX[1], y, 2.70, -135, 0.38, 0.44, 0.48, 4)
embryo(COLX[2] - 0.60, y, 2.85, -36, 0.32, 0.36, 0.38, 3, caudal=True,
       limbs=[(0.46, 0.32, 0.0, 0), (0.74, 0.28, 0.0, 0)])
y = ROWY[1]
embryo(COLX[0], y, 2.70, -195, 0.40, 0.46, 0.24, 4)
embryo(COLX[1], y, 2.70, -140, 0.38, 0.46, 0.40, 4, limbs=[(0.40,) + BUD, (0.70,) + BUD])
embryo(COLX[2] + 0.10, y, 2.45, -96, 0.38, 0.48, 0.36, 0, beak=True,
       limbs=[(0.40, 0.40, 0.32, -60), (0.72, 0.38, 0.30, 62)])
y = ROWY[2]
embryo(COLX[0], y, 2.70, -195, 0.40, 0.48, 0.22, 4)
embryo(COLX[1], y, 2.70, -145, 0.38, 0.50, 0.34, 3, limbs=[(0.40,) + BUD, (0.70,) + BUD])
embryo(COLX[2], y, 2.30, -104, 0.42, 0.62, 0.09, 0,
       limbs=[(0.38, 0.40, 0.30, -58), (0.72, 0.42, 0.34, 58)])
```

### Evidence from palaeontology (fossils)

A **fossil** is any preserved trace of a past organism, and fossils are the only
*direct* evidence of evolution, being the extinct organisms themselves. Age is read
from the **law of superposition** (the lower stratum of undisturbed sedimentary
rock is older) and measured by **radiometric dating** — carbon-14 below about
50,000 years, uranium–lead and potassium–argon for older rocks.
Fossils occur in a definite **sequence** — invertebrates, fish, amphibians,
reptiles, then birds and mammals — **none out of order**. Some are **connecting
links**, carrying characters of two groups.

| Organism | Links | Mixed characters |
|---|---|---|
| *Archaeopteryx* (Jurassic) | reptiles ↔ birds | feathers, wings, beak; but teeth, clawed digits, long bony tail |
| *Seymouria* (Permian) | amphibians ↔ reptiles | amphibian skull; reptilian limb girdles |
| Lungfish (*Protopterus*) | fish ↔ amphibians | gills **and** lungs; fins with bones |
| *Peripatus* | annelids ↔ arthropods | annelid body wall; arthropod tracheae |
| Platypus (*Ornithorhynchus*) | reptiles ↔ mammals | lays eggs, cloaca; but hair and milk |

A **living fossil** is a species almost unchanged from its fossil ancestors —
*Latimeria*, *Limulus*, *Sphenodon*, *Ginkgo biloba*, *Cycas*. The best-documented
lineage is the **horse**, worked out by Marsh and Osborn from an almost unbroken
North American series.

```figure caption="Evolution of the horse from *Eohippus* to *Equus*: size increases about five-fold, the fore-foot loses toes from four to one, and the cheek tooth changes from a low-crowned browsing tooth to a tall cement-covered grazing tooth."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon, Rectangle

fig, ax = plt.subplots(figsize=(5.2, 4.4))
ax.set_xlim(-0.15, 11.60); ax.set_ylim(0.10, 10.04)
ax.set_aspect("equal"); ax.axis("off")
HC, HD = "#e3e8ee", "#5b6472"

OUT = [(1.22, 0.94), (1.28, 1.02), (1.20, 1.14), (1.08, 1.20), (0.96, 1.20),
       (0.78, 1.10), (0.62, 1.02), (0.36, 0.98), (0.04, 0.97), (-0.28, 0.99),
       (-0.46, 0.94), (-0.54, 0.78), (-0.50, 0.62), (-0.36, 0.54),
       (-0.06, 0.50), (0.26, 0.50), (0.50, 0.56), (0.60, 0.70),
       (0.72, 0.86), (0.88, 0.96), (1.02, 1.00), (1.14, 0.90)]

def horse(x, yg, s):
    for lx, dx in ((-0.40, -0.05), (-0.30, -0.02), (0.38, 0.03), (0.48, 0.06)):
        ax.plot([x + lx * s, x + (lx + dx) * s], [yg + 0.58 * s, yg],
                color=HD, lw=0.7 + 1.25 * s, solid_capstyle="round", zorder=2)
    ax.plot([x - 0.50 * s, x - 0.70 * s], [yg + 0.88 * s, yg + 0.34 * s],
            color=HD, lw=0.5 + 0.8 * s, solid_capstyle="round", zorder=2)
    ax.add_patch(Polygon([(x + px * s, yg + py * s) for px, py in OUT],
                         closed=True, facecolor=HC, edgecolor=INK,
                         lw=0.8, zorder=3))
    for ex in (0.99, 1.06):
        ax.plot([x + ex * s, x + (ex - 0.02) * s],
                [yg + 1.19 * s, yg + 1.30 * s], color=INK, lw=0.8, zorder=4)
    ax.add_patch(Ellipse((x + 1.09 * s, yg + 1.09 * s), 0.07 * s, 0.06 * s,
                         facecolor=INK, edgecolor="none", zorder=5))

def foot(x, yb, spec, splints=0):
    H = 1.15
    for dx, top, bot, lw in spec:
        x0, x1 = x + dx, x + dx * 1.40
        ax.plot([x0, x1], [yb + H * top, yb + H * bot], color="#d8dde4",
                lw=lw + 1.8, solid_capstyle="round", zorder=2)
        ax.plot([x0, x1], [yb + H * top, yb + H * bot], color=INK,
                lw=0.5, alpha=0.5, zorder=3)
        if bot == 0:
            ax.add_patch(Ellipse((x1, yb), 0.17 + 0.026 * lw, 0.13,
                                 facecolor=SERIES[3] if abs(dx) < 0.02 else "#c3c9d2",
                                 edgecolor=INK, lw=0.6, zorder=4))
    for k in range(splints):
        dx = (-0.19, 0.19)[k]
        ax.plot([x + dx, x + dx * 1.9], [yb + H * 0.92, yb + H * 0.40],
                color=MUTED, lw=1.0, ls=(0, (2, 1.6)), zorder=2)

F4 = [(-0.30, 0.62, 0, 2.4), (-0.10, 0.92, 0, 3.4),
      (0.10, 1.00, 0, 4.0), (0.30, 0.66, 0, 2.6)]
F3 = [(-0.26, 0.72, 0, 2.8), (0.0, 1.00, 0, 4.4), (0.26, 0.72, 0, 2.8)]
F3M = [(-0.26, 0.64, 0.30, 2.0), (0.0, 1.00, 0, 5.2), (0.26, 0.64, 0.30, 2.0)]
F1 = [(0.0, 1.00, 0, 6.2)]

def tooth(x, yb, crown, col):
    ax.add_patch(Rectangle((x - 0.24, yb), 0.48, crown, facecolor=col,
                           edgecolor=INK, lw=0.8, zorder=3))
    for k in (1, 2, 3):
        ax.plot([x - 0.24 + 0.12 * k] * 2, [yb + 0.04, yb + crown - 0.04],
                color=INK, lw=0.4, alpha=0.4, zorder=4)
    for rx in (x - 0.13, x + 0.13):
        ax.add_patch(Polygon([(rx - 0.10, yb), (rx + 0.10, yb), (rx, yb - 0.52)],
                             closed=True, facecolor="#eceff3", edgecolor=INK,
                             lw=0.7, zorder=3))

ROW = dict(name=9.80, epoch=9.44, ground=6.20, hlab=5.88,
           foot=3.95, flab=3.70, tooth=2.05, tlab=1.35)
COL = [2.55, 4.40, 6.25, 8.10, 9.95]
GEN = [("$\\it{Eohippus}$", "Eocene\n55 Mya", 0.30, F4, 0, 0.30,
        "4 toes\n(front)", "low crown\nbrowser"),
       ("$\\it{Mesohippus}$", "Oligocene\n35 Mya", 0.60, F3, 0, 0.42,
        "3 toes,\nall touch", "low crown\nbrowser"),
       ("$\\it{Merychippus}$", "Miocene\n20 Mya", 1.00, F3M, 0, 0.72,
        "3 toes, only\nmiddle used", "high crown\ngrazer"),
       ("$\\it{Pliohippus}$", "Pliocene\n5 Mya", 1.20, F1, 2, 0.85,
        "1 toe +\n2 splints", "high crown\ngrazer"),
       ("$\\it{Equus}$", "Pleistocene\nto now", 1.60, F1, 0, 1.00,
        "1 toe\n(hoof)", "high crown\ngrazer")]

for x, (nm, ep, ht, fs, sp, cr, fl, tl) in zip(COL, GEN):
    ax.text(x, ROW["name"], nm, fontsize=7.0, color=INK, ha="center",
            va="center", fontweight="bold")
    ax.text(x, ROW["epoch"], ep, fontsize=6.2, color=MUTED, ha="center", va="top")
    horse(x, ROW["ground"], ht * 0.68)
    ax.text(x, ROW["hlab"], f"{ht:g} m tall",
            fontsize=6.3, color=MUTED, ha="center", va="top")
    foot(x, ROW["foot"], fs, sp)
    ax.text(x, ROW["flab"], fl, fontsize=6.2, color=MUTED, ha="center", va="top")
    tooth(x, ROW["tooth"], cr, SERIES[0] if cr < 0.5 else SERIES[2])
    ax.text(x, ROW["tlab"], tl, fontsize=6.2, color=MUTED, ha="center", va="top")

ax.plot([COL[0] - 0.95, COL[-1] + 1.35], [ROW["ground"], ROW["ground"]],
        color=GRID, lw=0.9)
for yy, lab in [(7.05, "the animal\n(to scale)"), (4.55, "fore-foot"),
                (2.55, "cheek tooth")]:
    ax.text(0.00, yy, lab, fontsize=6.8, color=INK, va="center", ha="left")
for yy in (8.78, 5.46, 3.16):
    ax.plot([-0.05, 11.45], [yy, yy], color=GRID, lw=0.7)
```

The **trends** are: increase in body size; lengthening of limbs, head and neck;
reduction of the toes from four to one with the weight on the enlarged third digit;
increase in tooth-crown height with cement filling the folds; and enlargement of
the brain. All follow from one change — Miocene forest gave way to grassland, so a
small hiding browser became a large running grazer, and grass silica wore teeth
down fast enough to make tall crowns pay.

### Evidence from biogeography

Animal distribution fits history, not climate. Australia has been isolated since
the Mesozoic, so almost all its mammals are **marsupials**, radiated into grazers
(kangaroo), burrowers (wombat), gliders (flying phalanger) and carnivores
(Tasmanian wolf) — a marsupial version of each placental mammal elsewhere, with no
placentals to compete. Darwin's decisive observation came from the **Galápagos
Islands** in 1835: 13 finch species found nowhere else, all close relatives of one
South American ground finch but differing chiefly in the **beak**, each beak
matching a different food. One immigrant population spread to different islands and
foods and diverged — **adaptive radiation**.

```figure caption="Darwin's finches of the Galápagos. One immigrant seed-eating ancestor radiated into 13 species differing mainly in beak size and shape, each beak matching a different food."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, FancyBboxPatch

fig, ax = plt.subplots(figsize=(5.2, 4.4))

def finch(ax, x, y, L, D, curve=0.0, chisel=False, col=SERIES[0]):
    """Head + beak. L = beak length, D = beak depth."""
    ax.add_patch(Circle((x, y), 0.46, facecolor="#e7ebf1", edgecolor=INK, lw=0.9))
    ax.add_patch(Circle((x - 0.13, y + 0.17), 0.075, facecolor=INK, edgecolor="none"))
    tipy = y + 0.04 - curve
    up = [(x - 0.40, y + 0.20), (x - 0.40 - L * 0.55, y + 0.16 - curve * 0.45),
          (x - 0.40 - L, tipy)]
    lo = [(x - 0.40 - L * 0.92, tipy - 0.03), (x - 0.40 - L * 0.45, y - D * 0.85),
          (x - 0.40, y - D)]
    ax.add_patch(Polygon(up + lo, closed=True, facecolor=col, edgecolor=INK, lw=0.8))
    ax.plot([x - 0.40, x - 0.40 - L * 0.9], [y + 0.02, tipy + 0.01],
            color=INK, lw=0.5, alpha=0.6)
    if chisel:
        ax.plot([x - 0.40 - L - 0.04, x - 0.40 - L - 0.46],
                [tipy - 0.02, tipy + 0.26], color="#7a5c2e", lw=1.7,
                solid_capstyle="round")
        ax.text(x - 0.40 - L - 0.52, tipy + 0.34, "cactus\nspine",
                fontsize=5.6, color="#7a5c2e", ha="center")

CELLS = [
 (1.55, 6.95, "Geospiza\\ magnirostris", "large ground finch", "big, hard seeds",
  0.62, 0.62, 0.0, False),
 (4.10, 6.95, "Geospiza\\ fortis", "medium ground finch", "medium seeds",
  0.55, 0.42, 0.0, False),
 (6.65, 6.95, "Geospiza\\ fuliginosa", "small ground finch", "small soft seeds",
  0.44, 0.26, 0.0, False),
 (9.20, 6.95, "Geospiza\\ scandens", "cactus finch", "cactus flowers, nectar",
  1.05, 0.20, 0.16, False),
 (1.55, 2.55, "Platyspiza\\ crassirostris", "vegetarian tree finch", "buds, leaves, fruit",
  0.50, 0.55, 0.22, False),
 (4.10, 2.55, "Camarhynchus\\ pallidus", "woodpecker finch", "insects under bark",
  0.86, 0.26, 0.0, True),
 (6.65, 2.55, "Certhidea\\ olivacea", "warbler finch", "small insects",
  0.72, 0.12, 0.04, False),
]
for x, y, sci, com, diet, L, D, cu, ch in CELLS:
    finch(ax, x + 0.45, y, L, D, cu, ch, col=SERIES[0] if y > 5 else SERIES[2])
    ax.text(x, y - 1.05, "$\\it{" + sci + "}$", ha="center", fontsize=6.6, color=INK)
    ax.text(x, y - 1.45, com, ha="center", fontsize=6.2, color=INK)
    ax.text(x, y - 1.82, diet, ha="center", fontsize=6.0, color=MUTED, style="italic")

ax.add_patch(FancyBboxPatch((7.98, 1.28), 2.56, 2.25, boxstyle="round,pad=0.10",
                            facecolor="#f2f5f8", edgecolor=MUTED, lw=0.8))
ax.text(9.26, 2.40,
        "ONE seed-eating\nancestor from\nmainland S. America\n\n→ 13 species\n"
        "on 1 island group\n\nadaptive radiation",
        ha="center", va="center", fontsize=6.2, color=INK)
ax.text(5.6, 8.85, "Beak shape tracks the food each species eats", ha="center",
        fontsize=7.2, color=INK, fontweight="bold")
ax.set_xlim(0.1, 11.0); ax.set_ylim(0.5, 9.3)
ax.set_aspect("equal"); ax.axis("off")
```

### Evidence from taxonomy, biochemistry and artificial selection

Only common descent explains why living things can be arranged in nested groups
at all. Biochemistry says the same at the molecular level: **all** organisms use
nucleic acid as the genetic material, the **same genetic code**, ATP and largely
the same 20 amino acids — and the *degree* of similarity measures relationship.
Cytochrome *c* differs from the human protein by 1 amino acid in the rhesus
monkey, about 12 in the horse and about 45 in yeast; human and chimpanzee DNA are
98–99 % identical.

Artificial selection makes the argument practical: if man can change a species in
centuries, nature can do it in millions of years. From the one wild species
*Brassica oleracea* breeders produced cabbage, cauliflower, kohlrabi, Brussels
sprouts, broccoli and kale, and all dogs descend from the wolf.

### Evolution happening now: industrial melanism

The peppered moth *Biston betularia* rests by day on tree trunks in England in two
forms — speckled grey **typica** and black **carbonaria**. Before industrialisation
the trunks were pale with lichen and *carbonaria* was almost unknown, first
recorded in Manchester in 1848. Soot killed the lichens and blackened the bark, and
within fifty years about 98 % of Manchester moths were black. Birds ate whichever
form they could see, as Kettlewell proved by mark–release–recapture in 1955. After
Britain's **Clean Air Act of 1956** the lichens returned and the melanic form
collapsed again — the same allele favoured and then disfavoured within 150 years.

```figure caption="Industrial melanism in *Biston betularia*. (a) Kettlewell's 1955 mark–recapture percentages — each form survives better where it is camouflaged. (b) The rise and fall of the melanic form, tracking soot and then the Clean Air Act of 1956."
import numpy as np, matplotlib.pyplot as plt

fig, axs = plt.subplots(1, 2, figsize=(5.2, 2.8), gridspec_kw=dict(wspace=0.42))

a = axs[0]
x = np.arange(2); w = 0.34
typ = [13.0, 12.5]; car = [27.5, 6.3]
a.bar(x - w / 2, typ, w, color="#b9c2cd", edgecolor=INK, lw=0.7, label="typica (pale)")
a.bar(x + w / 2, car, w, color="#2b2f36", edgecolor=INK, lw=0.7, label="carbonaria (black)")
for xi, v in zip(x - w / 2, typ):
    a.text(xi, v + 0.9, f"{v}%", ha="center", fontsize=6.4, color=INK)
for xi, v in zip(x + w / 2, car):
    a.text(xi, v + 0.9, f"{v}%", ha="center", fontsize=6.4, color=INK)
a.set_xticks(x)
a.set_xticklabels(["Birmingham\n(sooty bark)", "Dorset\n(lichened bark)"], fontsize=7.0)
a.set_ylabel("moths recaptured (%)", fontsize=7.6)
a.set_ylim(0, 34)
a.legend(fontsize=6.3, loc="upper right")
a.spines[["top", "right"]].set_visible(False)
a.grid(True, axis="y", alpha=0.45)
a.set_title("(a) Kettlewell, 1955", fontsize=7.6, pad=3)

b = axs[1]
yr = np.array([1848, 1870, 1895, 1930, 1960, 1970, 1980, 1989, 1996, 2003])
fr = np.array([1, 55, 98, 96, 93, 85, 62, 29.6, 15, 6])
b.plot(yr, fr, "-o", color="#2b2f36", ms=3.2, lw=1.6)
b.axvline(1956, color=SERIES[1], lw=1.1, ls=(0, (3, 2)))
b.annotate("Clean Air\nAct 1956", xy=(1956, 46), xytext=(1962, 36),
           fontsize=6.3, color=SERIES[1],
           arrowprops=dict(arrowstyle="-|>", color=SERIES[1], lw=0.8, mutation_scale=8))
b.annotate("first black moth\nManchester 1848", xy=(1848, 1), xytext=(1852, 20),
           fontsize=6.3, color=MUTED,
           arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.8, mutation_scale=8))
b.set_xlabel("year", fontsize=7.6)
b.set_ylabel("melanic form (%)", fontsize=7.6)
b.set_xlim(1840, 2012); b.set_ylim(0, 108)
b.spines[["top", "right"]].set_visible(False)
b.grid(True, alpha=0.45)
b.set_title("(b) rise and fall of carbonaria", fontsize=7.6, pad=3)
```

The same process runs around us: *Staphylococcus* resistant to penicillin,
*Anopheles* resistant to DDT in the Terai, *Plasmodium falciparum* resistant to
chloroquine. Each time a rare pre-existing resistant variant was the only one to
survive the new chemical, and so left all the offspring.

::: caution The drug does not create the resistance
Bacteria do not "become" resistant because an antibiotic is present. The
resistant mutant already existed by chance; the antibiotic merely removes its
competitors. Saying the drug induced the mutation is Lamarckism, and it loses
marks.
:::

## 7.3 Theories of evolution

By 1859 everyone agreed that species had changed. The argument was about *how*.
Three answers were given in turn; the third is the one now accepted.

### Lamarckism — inheritance of acquired characters

Jean Baptiste **Lamarck** (*Philosophie Zoologique*, 1809) rested his theory on
four propositions: (i) a changed **environment** creates new needs; (ii) an organ
**used** more enlarges and one **not used** degenerates; (iii) characters
**acquired** in life are **inherited**; (iv) such changes accumulate into a new
species. His examples are still quoted — the **giraffe** stretching its neck for
high foliage, **snakes** losing limbs by creeping, webbed feet in **ducks**, the
blind cave salamander *Proteus*, the reduced wings of **ostrich** and **kiwi**.

The first two propositions are true; the third is false, and everything depends on
it. August **Weismann** cut the tails off mice for five generations (901 mice) and
every litter was born with a normal tail. His **germplasm theory** explains why:
the body is somatoplasm, the gametes germplasm, and only germplasm is transmitted —
a change in the body cannot write itself back into the DNA of the gametes.

### Darwinism — natural selection

Charles **Darwin** sailed as naturalist on HMS *Beagle* (1831–36), read Malthus
on population growth, and published *On the Origin of Species* on 24 November
1859 — after **Alfred Russel Wallace** reached the same theory independently and
the two read a joint paper in 1858. The argument has six steps.

1. **Prodigality of reproduction.** Every organism produces far more offspring than
   can survive — a pair of elephants would leave 19 million descendants in 750
   years — yet populations stay roughly constant.
2. **Struggle for existence.** Therefore most offspring die: **intraspecific**
   (severest, since needs are identical), **interspecific** and **environmental**.
3. **Variation.** No two individuals of a species are exactly alike.
4. **Natural selection.** Individuals whose variations fit the environment better
   survive and reproduce more — "survival of the fittest", where *fittest* means
   best able to leave offspring, not strongest.
5. **Inheritance of useful variations** by the survivors.
6. **Origin of species** by accumulation of these changes in different directions
   in different places.

::: key Lamarck's giraffe and Darwin's giraffe
**Lamarck:** every giraffe stretched its neck and passed the stretch on — the
environment *created* the character. **Darwin:** giraffes with longer necks
already existed by chance variation, fed better and left more offspring — the
environment only *selected* among characters already there. That difference is
the whole of this unit.
:::

Darwin knew nothing of Mendel, so he could not explain **how variations arise** nor
separate inherited from acquired ones; he could not account for
**over-specialisation** (the antlers of the Irish elk); and a rare favourable
variation seemed likely to be diluted by intercrossing (the **swamping effect**).

### Mutation theory (Hugo de Vries, 1901)

Working on the evening primrose *Oenothera lamarckiana*, de Vries found individuals
that differed sharply from the parents, bred true at once and had not arisen
gradually. He called these **mutations** and argued that evolution proceeds by
large, sudden, discontinuous, heritable changes which are **random and
pre-adaptive** — they occur before, and independently of, any need for them.
Mutation is indeed the ultimate source of the variation Darwin lacked, but most
mutations are harmful and mutation alone has no direction.

### Neo-Darwinism — the modern synthesis

Neo-Darwinism is Darwin's selection combined with Mendelian genetics, mutation
theory and population mathematics, built in the 1930s and 40s by Fisher, Haldane,
Wright, Dobzhansky, Huxley and Mayr.

::: definition Evolution, in the Neo-Darwinian sense
Evolution is a **change in the allele (gene) frequencies of a population** across
generations. The **population**, not the individual, is the unit of evolution: an
individual cannot evolve, only be selected.
:::

| Factor | What it does | Direction |
|---|---|---|
| **Mutation** | creates new alleles | random |
| **Recombination** | reshuffles existing alleles | random |
| **Genetic drift** | random change of frequency in small populations | random |
| **Gene flow** | moves alleles between populations | random |
| **Natural selection** | sorts variants by reproductive success | **the only directional one** |
| **Isolation** | stops gene pools re-mixing | fixes divergence |

| Point of comparison | Lamarckism (1809) | Darwinism (1859) | Neo-Darwinism (1940s) |
|---|---|---|---|
| Source of variation | environment, new needs | not explained | mutation, recombination |
| Nature of variation | acquired, directed | small, continuous, random | random, genetic |
| Role of environment | creates the character | selects among characters | selects among characters |
| Acquired characters inherited? | yes — central claim | no | no |
| Unit of evolution | the individual | the individual | the **population** |
| Mechanism | use and disuse | natural selection | selection, drift, gene flow, isolation |
| Present status | rejected | accepted but incomplete | accepted |

### Types of natural selection

Selection acts on a continuously varying character — height, seed size, beak depth
— and reshapes its distribution in one of three ways.

```figure caption="The three types of natural selection acting on one continuously varying character. The dashed curve is the distribution before selection, the filled curve after it; the shaded tails are the individuals selected against."
import numpy as np, matplotlib.pyplot as plt

fig, axs = plt.subplots(1, 3, figsize=(5.2, 2.7), sharey=True,
                        gridspec_kw=dict(wspace=0.16))
x = np.linspace(-3.6, 3.6, 500)
def g(m, s): return np.exp(-0.5 * ((x - m) / s) ** 2) / (s * np.sqrt(2 * np.pi))
before = g(0, 1.0)

cases = [("stabilising", g(0, 0.50), [(-3.6, -1.15), (1.15, 3.6)],
          "both extremes removed,\nmean unchanged"),
         ("directional", g(1.15, 0.72), [(-3.6, -0.35)],
          "one extreme favoured,\nmean shifts"),
         ("disruptive", 0.5 * g(-1.35, 0.46) + 0.5 * g(1.35, 0.46), [(-0.55, 0.55)],
          "intermediates removed,\ncurve splits in two")]

for ax, (name, after, bands, note) in zip(axs, cases):
    ax.plot(x, before, color=MUTED, lw=1.2, ls=(0, (3, 2)), label="before")
    ax.fill_between(x, 0, after, color=ACCENT, alpha=0.22)
    ax.plot(x, after, color=ACCENT, lw=1.6, label="after")
    for lo, hi in bands:
        m = (x >= lo) & (x <= hi)
        ax.fill_between(x[m], 0, before[m], color=SERIES[1], alpha=0.32, lw=0)
    ax.axvline(0, color=GRID, lw=0.8)
    ax.set_title(name, fontsize=8.4, pad=2)
    ax.text(-3.45, 1.14, note, fontsize=6.3, color=MUTED, va="top")
    ax.set_xlabel("value of the character", fontsize=7.2)
    ax.set_xticks([]); ax.set_yticks([])
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_ylim(0, 1.20)
axs[0].set_ylabel("number of individuals", fontsize=7.4)
axs[1].annotate("", xy=(1.15, 0.60), xytext=(0.0, 0.60),
                arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.1, mutation_scale=9))
axs[2].text(3.4, 0.66, "shaded red = selected against", fontsize=6.0, color=SERIES[1],
            ha="right")
```

| Type | Which survive | Effect on the curve | Example |
|---|---|---|---|
| **Stabilising** | the intermediates | narrower, mean unchanged | human birth weight: 3–4 kg babies survive best |
| **Directional** | one extreme | mean shifts that way | industrial melanism; DDT resistance |
| **Disruptive** | both extremes | splits in two; can start speciation | seedcracker beaks: large crack hard seeds, small soft ones, intermediates neither |

### The Hardy–Weinberg principle

If evolution is a change in allele frequency, we need a baseline for what
frequencies do when nothing changes them. It was given independently in 1908 by
**G. H. Hardy** and **Wilhelm Weinberg**.

::: definition Hardy–Weinberg principle
In a large, randomly mating population the allele and genotype frequencies at a
locus remain **constant from generation to generation**, provided no mutation,
migration, selection or drift acts. Such a population is in **genetic
equilibrium**.
:::

Let $p$ be the frequency of the dominant allele $A$ and $q$ that of the recessive
$a$. These are the only alleles, so $p + q = 1$, and random mating is equivalent to
drawing two alleles at random from the gene pool, giving the terms of $(p+q)^2$:

$$ (p + q)^{2} = p^{2} + 2pq + q^{2} = 1 $$

with $p^{2}$ the frequency of $AA$, $2pq$ of $Aa$ and $q^{2}$ of $aa$.

::: derivation Why the frequencies do not drift
An $AA$ parent gives only $A$ gametes and an $Aa$ parent half $A$ gametes, so in
the next gamete pool

$$ p' = p^{2} + \tfrac{1}{2}(2pq) = p(p + q) = p, \qquad q' = q^{2} + pq = q $$

The frequencies come out **unchanged**, so the next generation is again
$p^2 : 2pq : q^2$. Equilibrium is reached after a **single** generation of random
mating and holds for ever unless a condition breaks.
:::

Each of the five conditions, when broken, names an agent of evolution: the
population is **very large** (else drift); mating is **random**; there is **no
mutation**, **no migration** and **no natural selection**.

::: key The real use of Hardy–Weinberg
No natural population meets all five conditions, so the principle is not a
description of nature but a **null hypothesis**. If observed genotype frequencies
differ significantly from $p^2 : 2pq : q^2$, a condition is being broken and **the
population is evolving**. That deviation is how evolution is measured.
:::

```figure caption="Hardy–Weinberg genotype frequencies as a function of the allele frequency $p$. Heterozygotes are commonest at $p = q = 0.5$, where $2pq = 0.5$. For a rare recessive allele the disorder is rare but carriers are not: at $q = 0.1$ there are 18 carriers for every affected individual."
import numpy as np, matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(4.9, 3.1))
p = np.linspace(0, 1, 400); q = 1 - p
ax.plot(p, p ** 2, color=SERIES[0], lw=1.8, label="$AA = p^2$")
ax.plot(p, 2 * p * q, color=SERIES[1], lw=1.8, label="$Aa = 2pq$")
ax.plot(p, q ** 2, color=SERIES[2], lw=1.8, label="$aa = q^2$")
ax.plot([0.5], [0.5], "o", color=SERIES[1], ms=5)
ax.annotate("max heterozygotes\n$2pq = 0.5$ at $p = q = 0.5$", xy=(0.5, 0.5),
            xytext=(0.50, 0.74), ha="center", fontsize=6.6, color=SERIES[1],
            arrowprops=dict(arrowstyle="-|>", color=SERIES[1], lw=0.9, mutation_scale=9))
ax.axvline(0.9, color=GRID, lw=0.9, ls=(0, (3, 2)))
ax.plot([0.9, 0.9], [0.01, 0.18], color=INK, lw=0.8)
ax.annotate("$q = 0.1$:  carriers $0.18$,\naffected only $0.01$", xy=(0.9, 0.10),
            xytext=(0.60, 0.26), fontsize=6.6, color=INK,
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.8, mutation_scale=8))
ax.set_xlabel("frequency of the dominant allele,  $p$")
ax.set_ylabel("genotype frequency")
ax.set_xlim(0, 1); ax.set_ylim(0, 1.02)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(True, alpha=0.45)
ax.legend(loc="upper center", ncol=3, fontsize=7.4, columnspacing=1.0)
```

::: example Worked example 7.1 — from the recessive phenotype to the whole population
**Problem.** Tasting PTC is dominant ($T$) over inability ($t$). Of 1000 students
in Pokhara, 160 are non-tasters. Assuming equilibrium, find both allele
frequencies and the expected number of each genotype.

**Solution.** Only the recessive homozygote is recognisable by phenotype.

$$ q^{2} = \frac{160}{1000} = 0.16 \;\Rightarrow\; q = 0.4, \qquad p = 0.6 $$

$$ p^{2} = 0.36, \qquad 2pq = 2(0.6)(0.4) = 0.48, \qquad q^{2} = 0.16 $$

Expected numbers $TT = 360$, $Tt = 480$, $tt = 160$ (sum 1000 ✓). So 84 % are
tasters, and more than half of those are heterozygous carriers.
:::

::: example Worked example 7.2 — hidden carriers of a rare disease
**Problem.** Albinism is autosomal recessive and affects 1 person in 10,000. Find
the allele frequency, the percentage of carriers and the number of carriers per
affected person.

**Solution.**

$$ q^{2} = \frac{1}{10000} = 0.0001 \;\Rightarrow\; q = 0.01, \qquad p = 0.99 $$

$$ 2pq = 2 \times 0.99 \times 0.01 = 0.0198 = 1.98\ \% $$

$$ \frac{2pq}{q^{2}} = \frac{0.0198}{0.0001} = 198 $$

So 1 person in 50 carries the allele unseen: **198 carriers per albino**. A
recessive allele can be common while the disorder stays rare, because almost every
copy is hidden in a heterozygote — which is why marriage between close relatives
raises the risk.
:::

::: example Worked example 7.3 — testing whether a population is in equilibrium
**Problem.** The MN blood group has two codominant alleles, so all three
genotypes are visible. Of 1000 people, 490 are MM, 420 MN and 90 NN. Is the
population in Hardy–Weinberg equilibrium?

**Solution.** Count alleles directly among the 2000 present:

$$ p(M) = \frac{2(490) + 420}{2000} = 0.7, \qquad q(N) = 0.3 $$

Expected: $MM = p^{2}N = 490$, $MN = 2pqN = 420$, $NN = q^{2}N = 90$ — identical to
the observed values, so the population **is** in equilibrium at this locus.
:::

::: caution Take the square root, and take it of the right thing
Two marks go here every year. (i) $q$ is the square root of the **frequency** of
the recessive phenotype, not of the *number* affected — divide by population size
first. (ii) The recessive phenotype equals $q^2$ only under complete dominance; if
the trait is codominant, count alleles directly as in example 7.3.
:::

### Genetic drift, founder effect and bottleneck

**Genetic drift** is random change in allele frequency caused by sampling error in
a small population. Toss a coin ten times and you may get seven heads; toss it ten
thousand times and you will not get 70 %. In a population of 20 an allele can be
lost or fixed by chance alone, useful or not — hence the first Hardy–Weinberg
condition. Two cases are named. In the **founder effect** a few colonists' small
sample of alleles becomes the gene pool of the new population, as in the Galápagos
finches. In the **bottleneck effect** a population is cut down by catastrophe and
recovers from the few survivors, permanently losing variation: Nepal's greater
one-horned rhinoceros fell below 100 animals in Chitwan in the late 1960s and has
recovered to about 750, but carries only the alleles those hundred happened to
have.

### Isolation and speciation

::: definition Species and speciation
A **species** is a group of actually or potentially interbreeding natural
populations, reproductively isolated from other such groups (Mayr). **Speciation**
is the origin of a new species; it requires gene flow between two populations to be
stopped, since interbreeding keeps merging their gene pools. **Isolation** is any
mechanism that prevents interbreeding.
:::

| Category | Mechanism | Example |
|---|---|---|
| **Geographical** | mountain, river, sea or desert separates them | the Himalaya; Galápagos channels |
| **Pre-zygotic** — ecological | different habitat, so they never meet | *Rana* of ponds and of streams |
| Pre-zygotic — temporal | different breeding season or time of day | two pines shedding pollen a month apart |
| Pre-zygotic — ethological | different courtship, song or pheromone | fireflies with different flash patterns |
| Pre-zygotic — mechanical | genitalia or flower structure do not fit | flowers with different pollinators |
| Pre-zygotic — gametic | sperm cannot fertilise the egg | many marine invertebrates |
| **Post-zygotic** — hybrid inviability | the hybrid zygote dies early | sheep × goat |
| Post-zygotic — hybrid sterility | the hybrid lives but cannot breed | the mule (horse × donkey) |
| Post-zygotic — hybrid breakdown | $F_1$ fertile but $F_2$ weak | some cotton crosses |

| | Allopatric speciation | Sympatric speciation |
|---|---|---|
| Populations are | geographically separated | in the same area |
| First barrier | geographical isolation | reproductive, from the start |
| Speed | usually slow | can be immediate |
| Typical cause | mountain uplift, river change, islands | polyploidy, host shift, disruptive selection |
| Example | Darwin's finches; Grand Canyon squirrels | polyploid wheat; apple maggot flies |
| Frequency | the common route in animals | common in plants |

The Himalaya is a working example: the range rose through the Miocene and
Pliocene, cutting one fauna into northern and southern halves and stacking
habitats from Terai to alpine desert within 150 km. Nepal's diversity for its
size — over 200 mammal species in 147,000 km² — is a result of that repeated
allopatric isolation.

## 7.4 Human evolution

### Our place among the primates

Man is classified: **Animalia** → **Chordata** → **Mammalia** → Order **Primates**
→ Family **Hominidae** → ***Homo*** → ***Homo sapiens***. Three words are confused:
**hominoid** = apes plus man; **hominid** = great apes plus man; **hominin** = man
and his extinct bipedal ancestors.

With all primates we share grasping hands and feet with an **opposable thumb**,
nails instead of claws, forward-facing eyes giving **stereoscopic colour vision**,
a large brain for body size and prolonged parental care. What separates *man* from
the apes: habitual **bipedal** gait with an **S-shaped** vertebral column, broad
pelvis, **arched foot** and non-opposable big toe; the **foramen magnum** central
in the skull base, so the head balances on the column; **cranial capacity
1350–1450 cm³** with a vertical forehead and no brow ridge; a **chin**, small
canines and an evenly arched tooth row; and a precision grip, speech and learned
culture.

::: caution Man did not evolve from the monkey or the chimpanzee
Man and the modern apes are **cousins**, not parents and children: they share a
common Miocene ancestor and have been diverging ever since. "Man descended from
monkeys" is wrong and is penalised.
:::

```figure caption="Simplified phylogeny of the hominoids. Note that *Ramapithecus* (now referred to *Sivapithecus*) sits on the orangutan branch, not on ours; the hominin line runs *Australopithecus* → *H. habilis* → *H. erectus* → *H. sapiens*, with the Neanderthals as an extinct side branch. The time scale is expanded after 5 Mya."
import numpy as np, matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(5.2, 4.0))
ax.set_xlim(-1.40, 13.30); ax.set_ylim(-1.15, 10.15)
ax.axis("off")

def X(t):
    return (25 - t) * 0.225 if t >= 5 else 4.5 + (5 - t) * 1.10

TRUNK, LX = 6.40, 10.50
ax.plot([X(25), X(5)], [TRUNK, TRUNK], color=MUTED, lw=2.4,
        solid_capstyle="round")

for t, y, lab in [(16.0, 9.55, "gibbons"),
                  (8.0, 8.45, "orangutan\n(incl. $\\it{Sivapithecus}$)"),
                  (6.6, 7.55, "gorilla"), (6.0, 6.95, "chimpanzee")]:
    ax.plot([X(t), X(t)], [TRUNK, y], color=MUTED, lw=1.2)
    ax.plot([X(t), LX - 0.14], [y, y], color=MUTED, lw=1.2)
    ax.text(LX, y, lab, fontsize=6.6, color=MUTED, va="center")

def clade(xsplit, ysplit, y, t0, t1, lab, c, extinct=False):
    ax.plot([xsplit, xsplit], [ysplit, y], color=c, lw=1.5)
    ax.plot([xsplit, X(t0)], [y, y], color=c, lw=1.5)
    ax.plot([X(t0), X(t1)], [y, y], color=c, lw=3.4, solid_capstyle="butt")
    if extinct:
        ax.plot([X(t1)], [y], marker="x", ms=5.5, mew=1.7, color=c)
    ax.plot([X(t1) + 0.10, LX - 0.14], [y, y], color=c, lw=0.6,
            ls=(0, (1.6, 2.0)))
    ax.text(LX, y, lab, fontsize=6.6, color=c, va="center")

G, B, R, V = SERIES[2], SERIES[0], SERIES[1], SERIES[4]
clade(X(6.0), TRUNK, 5.30, 4.2, 2.0, "$\\it{Australopithecus}$", G)
clade(X(2.4), 5.30, 4.15, 2.4, 1.5, "$\\it{Homo\\ habilis}$", B)
clade(X(1.9), 4.15, 3.00, 1.9, 0.3, "$\\it{Homo\\ erectus}$", B)
clade(X(0.45), 3.00, 1.85, 0.45, 0.04, "$\\it{H.\\ neanderthalensis}$", R, True)
clade(X(0.32), 3.00, 0.70, 0.32, 0.0, "$\\it{Homo\\ sapiens}$", V)

for t in (25, 20, 15, 10, 5, 4, 3, 2, 1, 0):
    ax.plot([X(t), X(t)], [-0.42, -0.22], color=MUTED, lw=0.8)
    ax.text(X(t), -0.54, f"{t}", fontsize=6.4, color=MUTED, ha="center", va="top")
ax.plot([X(25), X(0)], [-0.22, -0.22], color=MUTED, lw=1.0)
ax.text(X(12.5), -1.06, "million years ago", fontsize=6.6, color=MUTED, ha="center")
ax.plot([X(5), X(5)], [-0.50, 9.95], color=GRID, lw=0.8, ls=(0, (3, 3)))
ax.text(X(5) + 0.12, 9.92, "time scale expands here", fontsize=6.0,
        color=MUTED, va="top")

ax.text(-1.35, TRUNK + 0.22,
        "common ancestor\nof the apes\n($\\it{Dryopithecus}$ group,\n25-15 Mya)",
        fontsize=6.4, color=INK, va="bottom", ha="left")
ax.annotate("hominin line:\nbipedal, big brain",
            xy=(X(6.0), 5.85), xytext=(1.00, 3.55), fontsize=6.4,
            color=G, ha="center", va="top",
            arrowprops=dict(arrowstyle="->", color=G, lw=0.8))
ax.text(LX + 1.95, 1.85, "×", fontsize=1, color="none")
```

### Dryopithecus and Ramapithecus — the Miocene apes

***Dryopithecus*** ("oak ape") lived about **22 to 9 Mya** in the forests of
Africa, Europe and Asia: limbs of about equal length, semi-erect with
knuckle-walking, a U-shaped jaw with large canines and roughly **400 cm³** of
brain. It is regarded as ancestral to the great apes and possibly to the African
ape–human line.

***Ramapithecus*** ("Rama's ape") matters in Nepal. The first jaws came from the
**Siwalik (Churia) Hills** in 1932, and the Nepali specimen — molars dated to about
**9.0–9.5 million years** — from **Tinau Khola, Palpa district**. It was smaller
than *Dryopithecus*, with thickly enamelled molars, reduced canines and a short
deep jaw: a ground-dwelling eater of hard seeds. For twenty years it was called our
first direct ancestor, but more complete specimens found in 1975–76 showed this was
a mistake; it is now referred to ***Sivapithecus*** and placed on the **orangutan**
branch. Learn it as the best-known Miocene ape of South Asia, not as our ancestor.

### Australopithecus — the first biped

***Australopithecus*** ("southern ape") lived in eastern and southern Africa from
about **4.2 to 2 Mya**. *A. africanus* was described by Raymond Dart in 1924 from
the **Taung** skull; *A. afarensis* is known from **"Lucy"**, a 40 %-complete
skeleton found at Hadar, Ethiopia, in 1974 and dated to **3.2 Mya**. The pelvis
and knee are decisive: it walked **upright on two legs** while its brain was still
ape-sized, only **400–500 cm³**, and the 3.6-million-year-old Laetoli footprints
show the stride directly. It stood 1.0–1.5 m, had large molars and heavy brow
ridges, and used broken stones but **made no tools**. Bipedalism came before the
brain, and freeing the hands made everything afterwards possible.

### Homo habilis, Homo erectus and the Neanderthals

***Homo habilis*** ("handy man", **2.4–1.5 Mya**) was found by Louis and Mary
Leakey at **Olduvai Gorge, Tanzania**, in 1960. Cranial capacity rose to
**650–800 cm³** and the jaws grew lighter, but the name carries its importance: it
is the first hominin that certainly **made stone tools**, the flaked pebble
choppers of the **Oldowan** industry.

***Homo erectus*** appeared about **1.9 Mya** and survived to roughly **300,000
years ago**, the longest run of any *Homo*. Cranial capacity **800–1100 cm³**
(average about 950), height 1.6–1.8 m, thick brow ridge, sloping forehead and
**no chin**. **Java man** (*Pithecanthropus erectus*, Dubois, 1891) and **Peking
man** (*Sinanthropus pekinensis*, 1927) are the same species under older names.
*H. erectus* was the first to **use fire**, to make the Acheulian **hand axe**, to
hunt large game cooperatively and to leave Africa.

***Homo neanderthalensis*** lived in Europe, the Near East and Central Asia from
about **400,000 to 40,000 years ago**, the first skull coming from the Neander
valley, Germany, in 1856. Cranial capacity **1300–1600 cm³** (average ~1450) was
*larger* than the modern average. They were short and heavily built, with a
receding forehead, heavy brow ridge and weak chin; they made fine **Mousterian**
flake tools, wore skins and **buried their dead** with grave goods, the first
evidence of ritual. They disappeared about 40,000 years ago after modern humans
reached Europe, leaving 1–2 % of their DNA in living non-African populations.

::: caution A bigger brain is not automatically a better brain
The Neanderthal average of about 1450 cm³ equals or exceeds the modern
1350–1450 cm³. Brain **organisation** — especially the frontal and temporal lobes
and the speech areas — matters more than bulk. Do not write that cranial capacity
rose steadily right to the present; it peaked and then fell slightly.
:::

### Homo sapiens

Anatomically modern ***Homo sapiens*** arose in **Africa about 300,000 years
ago** and spread worldwide from roughly 70,000 years ago. The best-known early
European population is **Cro-Magnon man**, **40,000 to 10,000 years ago**, about
1.8 m tall with a cranial capacity near **1600 cm³**, a vertical forehead, no brow
ridge and a well-marked chin; Cro-Magnons made blade and bone tools, sewed
clothing and painted Altamira and Lascaux. With *Homo sapiens sapiens*
(**1350–1450 cm³**) biological evolution was overtaken by **cultural
evolution**: agriculture from about 10,000 years ago, then writing and science.

| Stage | Age | Cranial capacity | Where found | Key advance |
|---|---|---|---|---|
| *Dryopithecus* | 22–9 Mya | ~400 cm³ | Africa, Europe, Asia | Miocene ape, semi-erect |
| *Ramapithecus* (*Sivapithecus*) | 14–9 Mya | ~400 cm³ | Siwaliks, Nepal and India | thick molars; orangutan branch |
| *Australopithecus* | 4.2–2 Mya | 400–500 cm³ | East and South Africa | **fully bipedal**, no tools |
| *Homo habilis* | 2.4–1.5 Mya | 650–800 cm³ | Olduvai Gorge, Tanzania | **first stone tools** (Oldowan) |
| *Homo erectus* | 1.9–0.3 Mya | 800–1100 cm³ | Java, China, Africa, Europe | **fire**, hand axes, left Africa |
| *Homo neanderthalensis* | 0.4–0.04 Mya | 1300–1600 cm³ | Europe, West and Central Asia | burial of the dead, Mousterian |
| *Homo sapiens* (Cro-Magnon) | 40,000–10,000 yr | ~1600 cm³ | Europe | cave art, blade tools |
| *Homo sapiens sapiens* | 300,000 yr – now | 1350–1450 cm³ | worldwide | agriculture, language, culture |

::: memory Trends in human evolution, in the order they happened
1. **Erect posture and bipedalism** — S-shaped spine, broad pelvis, arched foot,
   non-opposable big toe. This came **first**, in *Australopithecus*.
2. **Freeing of the hands**, then the precision grip of an opposable thumb.
3. **Increase in cranial capacity**: 400 → 450 → 700 → 950 → 1450 cm³.
4. **Shortening of the jaws and face**, prognathous → orthognathous, canines
   reduced, a **chin** appears, brow ridges lost, forehead vertical.
5. **Forward shift of the foramen magnum** to the centre of the skull base.
6. **Tool making → fire → speech → agriculture**: culture replaces biology.
:::

## Chapter summary

- Life arose once, by **chemical evolution** under a reducing, oxygen-free
  atmosphere (Oparin 1924, Haldane 1929): gases → monomers → polymers →
  protobionts → anaerobic heterotroph → photoautotroph → aerobe. **Miller and Urey
  (1953)** obtained **amino acids**, not life. Pasteur's swan-necked flask had
  already established **biogenesis**.
- **Homologous** organs = same structure, different function → divergent evolution
  → common ancestry. **Analogous** = different structure, same function →
  convergent evolution → adaptation only. **Vestigial** organs are functionless
  remnants (appendix, coccyx, plica semilunaris, ear muscles). Early vertebrate
  embryos share gill slits, notochord and a post-anal tail (**von Baer's law**).
- Fossils are the only direct evidence and include connecting links —
  *Archaeopteryx*, lungfish, *Peripatus*, platypus, *Seymouria*. Horse series
  *Eohippus* → *Mesohippus* → *Merychippus* → *Pliohippus* → *Equus*: 0.3 → 1.6 m,
  toes 4 → 1, browsing → grazing teeth.
- **Lamarckism** (use, disuse, inheritance of acquired characters) was disproved by
  Weismann's germplasm theory. **Darwinism** = over-production → struggle →
  variation → natural selection → new species, but could not explain variation.
  **Neo-Darwinism** = mutation + recombination + selection + drift + gene flow +
  isolation, acting on a **population**.
- Selection is **stabilising**, **directional** or **disruptive**; industrial
  melanism in *Biston betularia* is directional selection recorded in real time.
- **Hardy–Weinberg**: $p + q = 1$ and $p^{2} + 2pq + q^{2} = 1$, with $p^2 = AA$,
  $2pq = Aa$, $q^2 = aa$; it needs a large, randomly mating population with no
  mutation, migration or selection, and deviation from it **is** evolution. For a
  recessive trait $q = \sqrt{q^{2}}$ from the phenotype frequency, and the
  carrier : affected ratio is $2p/q$. Speciation needs isolation — geographical,
  pre-zygotic or post-zygotic; **allopatric** dominates in animals, **sympatric**
  in plants.
- Human line: *Dryopithecus* (400 cm³) → *Australopithecus* (450 cm³, first biped)
  → *H. habilis* (650–800 cm³, first tools) → *H. erectus* (950 cm³, fire) →
  *H. neanderthalensis* (1450 cm³, burial) → *H. sapiens* (1350–1450 cm³).
  *Ramapithecus* of the Nepali Siwaliks belongs to the **orangutan** branch.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The theory of inheritance of acquired characters was proposed by <span class="marks">[1]</span>
   (a) Charles Darwin (b) J. B. Lamarck (c) Hugo de Vries (d) August Weismann
2. The wing of a bird and the wing of an insect are <span class="marks">[1]</span>
   (a) homologous organs (b) analogous organs (c) vestigial organs (d) atavistic organs
3. The connecting link between reptiles and birds is <span class="marks">[1]</span>
   (a) *Seymouria* (b) *Peripatus* (c) *Archaeopteryx* (d) *Ornithorhynchus*
4. In a population in Hardy–Weinberg equilibrium the frequency of the recessive
   allele is 0.2. The frequency of heterozygotes is <span class="marks">[1]</span>
   (a) 0.04 (b) 0.16 (c) 0.32 (d) 0.64
5. The first hominin to make stone tools was <span class="marks">[1]</span>
   (a) *Australopithecus* (b) *Homo habilis* (c) *Homo erectus* (d) *Ramapithecus*

::: note Answers to Group A
**1.** (b) — Lamarck, *Philosophie Zoologique*, 1809.
**2.** (b) — same function (flight), completely different structure and origin.
**3.** (c) — *Archaeopteryx*: feathers and wings, but reptilian teeth, claws and a long bony tail.
**4.** (c) — $q = 0.2$, $p = 0.8$, so $2pq = 2(0.8)(0.2) = 0.32$.
**5.** (b) — *Homo habilis*, the "handy man", made the Oldowan pebble tools.
:::

**Group B — Short answer (4 marks each)**

1. Differentiate between homologous and analogous organs, giving one animal and
   one plant example of each. <span class="marks">[4]</span>
2. Describe the Miller–Urey experiment and state precisely what it proved. <span class="marks">[4]</span>
3. In a population of 2000 people, 320 cannot roll the tongue, a recessive
   character. Assuming Hardy–Weinberg equilibrium, calculate both allele
   frequencies and the expected number of heterozygotes. <span class="marks">[4]</span>
4. What is industrial melanism, and how does it demonstrate natural selection? <span class="marks">[4]</span>
5. State the Hardy–Weinberg principle and the conditions under which a population
   stays in genetic equilibrium. <span class="marks">[4]</span>

::: note Answers to Group B
**1.** Homologous — same basic structure and embryonic origin, different function,
by divergent evolution from a common ancestor: forelimbs of man, whale, bat and
horse; thorn of *Bougainvillea* and tendril of *Cucurbita*. Analogous — different
structure and origin, same function, by convergent evolution: wing of a bird and of
an insect; sweet potato (root tuber) and potato (stem tuber). Homology proves
relationship, analogy only adaptation.

**2.** Sealed glass system: boiling water feeds vapour into a chamber charged with
CH₄, NH₃ and H₂, tungsten electrodes spark for a week at about 800 °C, a condenser
returns the products to a U-trap. Result: **amino acids** (glycine, alanine,
aspartic acid) with urea, sugars and fatty acids. It proved that the **monomers of
life form spontaneously from inorganic gases** — it did *not* produce a cell, a
protein or a nucleic acid.

**3.** $q^{2} = 320/2000 = 0.16$, so $q = 0.4$ and $p = 0.6$. Then
$2pq = 2(0.6)(0.4) = 0.48$, so heterozygotes $= 0.48 \times 2000 = 960$. (Check:
$p^2 \times 2000 = 720$ homozygous rollers; $720 + 960 + 320 = 2000$. ✓)

**4.** Industrial melanism is the rise in frequency of a dark form in a polluted
area. In *Biston betularia* the melanic *carbonaria* was almost unknown before
1848; soot killed the lichens and by 1895 about 98 % of Manchester moths were
black. Kettlewell's 1955 mark–recapture recovered 27.5 % of *carbonaria* against
13.0 % of *typica* in sooty Birmingham and the reverse in unpolluted Dorset: birds
ate whichever form was conspicuous. After the Clean Air Act of 1956 the melanic
form fell back. It is **directional** natural selection, because a pre-existing
heritable variation changed in frequency through differential survival in a
direction set by the environment.

**5.** In a large, randomly mating population the allele and genotype frequencies
at a locus stay constant across generations, with $p + q = 1$ and
$p^{2} + 2pq + q^{2} = 1$. Conditions: very large population, random mating, no
mutation, no migration, no natural selection. Breaking any one makes the population
evolve.
:::

**Group C — Long answer (8 marks each)**

1. Describe the evolution of the horse from *Eohippus* to *Equus* with the help of
   a labelled diagram, and state four evolutionary trends shown by the
   series. <span class="marks">[8]</span>
2. (a) State the postulates of Darwin's theory of natural selection. <span class="marks">[4]</span>
   (b) Explain the long neck of the giraffe first on Lamarck's theory and then on
   Darwin's, and say why only one explanation is accepted. <span class="marks">[4]</span>
3. Give an account of human evolution from *Dryopithecus* to *Homo sapiens
   sapiens* with the approximate age and cranial capacity of each stage, and list
   four trends shown by the series. <span class="marks">[8]</span>

::: note Answer outlines to Group C
**1.** Diagram as in the figure above. *Eohippus* (Eocene, 0.3 m, 4 toes in front
and 3 behind, low-crowned browsing teeth, forest) → *Mesohippus* (Oligocene, 0.6 m,
3 toes) → *Merychippus* (Miocene, 1.0 m, 3 toes with the weight on the enlarged
middle toe, first high-crowned grazing teeth with cement) → *Pliohippus* (Pliocene,
1.2 m, one functional toe with two splints) → *Equus* (Pleistocene to now,
1.5–1.6 m, single hoof). Trends: body size increases; toes reduce from four to one
with the weight on the third digit; crown height increases with cement in the
folds, browser → grazer; limbs, head and neck lengthen and the brain enlarges.
Cause: Miocene forest gave way to grassland, favouring speed and
abrasion-resistant teeth.

**2.** (a) Prodigality of reproduction; struggle for existence (intraspecific,
interspecific, environmental); variation; natural selection, or survival of the
fittest; inheritance of the useful variations; origin of new species by their
accumulation. (b) **Lamarck:** the short-necked ancestor stretched its neck for high
foliage, the stretch was acquired and passed on, and the offspring stretched
further — the environment *created* the long neck. **Darwin:** the population
already varied in neck length; when low foliage grew scarce the longer-necked
individuals fed better and left more offspring, so mean neck length rose each
generation — the environment only *selected* among existing variations. Darwin's
version is accepted because acquired somatic characters are not inherited
(Weismann), whereas heritable variation plus differential survival is directly
observed, as in industrial melanism.

**3.** Stages, ages and cranial capacities as in the table of section 7.4, in that
order, with the branching of the figure. Trends: erect posture and complete
bipedalism, which came *before* the large brain; progressive increase in cranial
capacity; shortening of the jaws and face with reduced canines, loss of the brow
ridges and appearance of a chin; forward shift of the foramen magnum with an
S-shaped spine, broad pelvis and arched foot; and tool making, fire and speech, so
that cultural evolution replaces biological.
:::
