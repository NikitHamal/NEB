---
subject: Biology
grade: 11
unit: 8
title: Faunal Diversity
hours: 34
area: Zoology
---

Between one and two million kinds of animal have been named, and the true number
alive today is probably several times larger. Faced with that flood a zoologist
sorts, but not arbitrarily: animals are grouped by *shared inherited
architecture* — how many germ layers built the embryo, whether there is a body
cavity, whether the body is segmented. Answer those few structural questions and
almost any animal can be placed. This unit works through the sorting scheme,
then slows down for three animals you will meet on the laboratory bench: the
ciliate *Paramecium*, the earthworm *Pheretima posthuma* and the frog
*Rana tigrina*.

::: key
**What this unit asks of you.** (i) Place a protist in its group from its
locomotory organelle. (ii) Give the diagnostic characters and examples of the
nine animal phyla, justifying each from level of organisation, symmetry, germ
layers and coelom. (iii) Describe, with labelled diagrams, *Paramecium* and the
organ systems of the earthworm and the frog. Diagrams carry a large share of
the marks — practise drawing them, not just reading them.
:::

## 8.1 Protista

Protista is the kingdom Whittaker (1969) created for the eukaryotes that are
neither plants, animals nor fungi. They share only a negative character — they
are what is left when the three higher kingdoms are removed — so Protista is a
**paraphyletic** "rag-bag" kingdom; the CDC syllabus uses this five-kingdom
treatment.

**General characters.** (i) Eukaryotic and mostly unicellular, so the level of
organisation is **protoplasmic** — one cell does everything. (ii) Aquatic or in
damp places, including a host's body fluids. (iii) Nutrition varied:
holophytic (*Euglena*), holozoic (*Amoeba*, *Paramecium*), saprophytic or
parasitic (*Plasmodium*). *Euglena*, both holophytic and saprophytic,
fits neither Plantae nor Animalia. (iv) Locomotion by
pseudopodia, flagella or cilia, or absent (Sporozoa). (v) Osmoregulation by
contractile vacuoles; respiration and excretion by diffusion. (vi) Reproduction
by fission, budding, syngamy or conjugation, with resistant **cysts**.

### Classification of Protista

Protista is conventionally divided on nutrition into plant-like protists,
animal-like protists (Protozoa) and fungus-like protists.

| Assemblage | Group | Key features | Examples |
|---|---|---|---|
| Plant-like | Chrysophyta (diatoms) | two-piece silica frustule; deposits form diatomite | *Navicula*, *Cyclotella* |
| Plant-like | Dinoflagellata | two flagella in grooves; cellulose plates; cause red tides | *Gonyaulax*, *Noctiluca* |
| Plant-like | Euglenophyta | pellicle instead of a wall; chlorophyll a and b; eyespot | *Euglena* |
| Animal-like | Protozoa | holozoic or parasitic; no cell wall | *Amoeba*, *Paramecium* |
| Fungus-like | Slime moulds | feeding plasmodium; spores in fruiting bodies | *Physarum* |

Within the Protozoa the classical division uses the **organelle of locomotion**.

| Class | Locomotory organelle | Habit | Examples and importance |
|---|---|---|---|
| Rhizopoda (Sarcodina) | pseudopodia | free-living or parasitic | *Amoeba proteus*; *Entamoeba histolytica* (amoebic dysentery); *Elphidium* |
| Mastigophora (Flagellata) | flagella | free-living or parasitic | *Euglena*; *Trypanosoma* (sleeping sickness); *Leishmania donovani* (kala-azar); *Giardia* |
| Sporozoa | none in the adult | all parasitic; spore-forming | *Plasmodium vivax*, *P. falciparum* (malaria); *Monocystis* |
| Ciliata | many short cilia | macro- and micronucleus present | *Paramecium*, *Vorticella*; *Balantidium coli* |

::: caution
Do not write "Protozoa is a phylum of Kingdom Animalia". In the five-kingdom
system used by the CDC syllabus, protozoans are **protists**; Protozoa is an
assemblage within Protista, and Animalia begins with the sponges.
:::

### *Paramecium caudatum*: structure

*Paramecium* is the standard ciliate type study — common in any pond or hay
infusion and large enough (170–330 μm) to see under a school microscope. Its
shape is constant, like a slipper: blunt in front, pointed behind, the posterior
end carrying a tuft of longer **caudal cilia** — the *caudatum* of the name.

```figure caption="*Paramecium caudatum*, ventral view."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Ellipse
fig, ax = plt.subplots(figsize=(5.2, 3.4))

ECTO = "#dfe9f2"; ENDO = "#eef3f8"; EDGE = "#2c5f96"
NUC = "#c9b6d8"; NUCE = "#6a4a78"
VAC = "#cfe3d4"; VACE = "#2e8b57"
FOOD = "#f2e3c4"; FOODE = "#9a7330"

# ---------------- body outline: slipper shape ----------------
x = np.linspace(-3.90, 3.90, 800)
u = (x + 3.90)/7.80
wt = 1.30*np.clip(np.sin(np.pi*u**0.72)**0.62, 0, 1)*(1 - 0.30*u**3)
wb = 1.22*np.clip(np.sin(np.pi*u**0.70)**0.60, 0, 1)*(1 - 0.34*u**3)
# oral groove: a shallow depression on the ventral (lower) surface
wb = wb - 0.46*np.exp(-((x + 0.15)/1.05)**2)*np.clip(wb/1.0, 0, 1)
top = wt; bot = -wb
ax.add_patch(Polygon(np.vstack([np.c_[x, top], np.c_[x[::-1], bot[::-1]]]),
                     closed=True, fc=ECTO, ec=EDGE, lw=1.4, zorder=3))
# endoplasm boundary
ax.add_patch(Polygon(np.vstack([np.c_[x, top*0.82], np.c_[x[::-1], bot[::-1]*0.80]]),
                     closed=True, fc=ENDO, ec="#9fb6cc", lw=0.8, zorder=4))

# ---------------- cilia round the whole pellicle ----------------
def normal(xs, arr, sign):
    i = np.argmin(np.abs(x - xs))
    i0, i1 = max(i - 3, 0), min(i + 3, len(x) - 1)
    dx = x[i1] - x[i0]; dy = arr[i1] - arr[i0]
    n = np.hypot(dx, dy)
    return (dy/n*sign*-1, dx/n*sign)

for xs in np.arange(-3.80, 3.86, 0.145):
    for arr, sg in ((top, 1), (bot, -1)):
        i = np.argmin(np.abs(x - xs))
        nx, ny = normal(xs, arr, sg)
        ax.plot([xs, xs + nx*0.30], [arr[i], arr[i] + ny*0.30], color=EDGE,
                lw=0.55, zorder=2, solid_capstyle='round')
# longer caudal cilia
for k in np.linspace(-0.55, 0.55, 7):
    ax.plot([3.86, 4.42], [k*0.30, k*0.70], color=EDGE, lw=0.6, zorder=2,
            solid_capstyle='round')

# ---------------- trichocysts in the ectoplasm ----------------
for xs in np.arange(-3.40, 3.50, 0.29):
    for arr, sg in ((top, 1), (bot, -1)):
        i = np.argmin(np.abs(x - xs))
        nx, ny = normal(xs, arr, sg)
        x0, y0 = xs - nx*0.06, arr[i] - ny*0.06
        ax.plot([x0, x0 - nx*0.22], [y0, y0 - ny*0.22], color="#a2453e",
                lw=0.85, zorder=5, solid_capstyle='round')

# ---------------- oral apparatus ----------------
ax.plot(x[(x > -1.55) & (x < 1.05)], bot[(x > -1.55) & (x < 1.05)],
        color=EDGE, lw=1.8, zorder=6)
vest = np.array([[0.36, -0.62], [0.86, -0.30], [1.02, 0.06], [0.72, 0.16],
                 [0.46, -0.12], [0.16, -0.50]])
ax.add_patch(Polygon(vest, closed=True, fc="#f6e2c8", ec=EDGE, lw=1.1, zorder=7))
ax.plot([0.98, 1.34, 1.52], [0.04, 0.26, 0.60], color=EDGE, lw=1.3, zorder=7,
        solid_capstyle='round')
# cytopyge
ax.plot([1.74, 1.98], [-0.72, -0.86], color="#a2453e", lw=1.8, zorder=7,
        solid_capstyle='round')

# ---------------- nuclei ----------------
ax.add_patch(Ellipse((-0.10, 0.34), 1.30, 0.86, angle=-12, fc=NUC, ec=NUCE,
                     lw=1.2, zorder=8))
ax.add_patch(Circle((0.52, 0.66), 0.20, fc="#8e6fa8", ec=NUCE, lw=1.0, zorder=9))

# ---------------- contractile vacuoles with radiating canals ----------------
for cx in (-2.35, 2.30):
    for a in np.linspace(0, 2*np.pi, 9)[:-1]:
        ax.plot([cx + 0.24*np.cos(a), cx + 0.62*np.cos(a)],
                [0.42 + 0.24*np.sin(a), 0.42 + 0.62*np.sin(a)],
                color=VACE, lw=0.9, zorder=7, solid_capstyle='round')
    ax.add_patch(Circle((cx, 0.42), 0.26, fc=VAC, ec=VACE, lw=1.1, zorder=8))

# ---------------- food vacuoles circulating (cyclosis) ----------------
fv = [(1.62, 0.90), (0.90, -0.62), (-0.90, -0.70), (-2.00, -0.34),
      (-2.55, 0.62), (-1.30, 0.86), (2.55, -0.40), (1.10, 1.02)]
for k, (cx, cy) in enumerate(fv):
    ax.add_patch(Circle((cx, cy), 0.17 + 0.03*(k % 3), fc=FOOD, ec=FOODE,
                        lw=0.9, zorder=8))
th = np.linspace(0.35, 5.95, 200)
ax.plot(2.05*np.cos(th) - 0.10, 0.92*np.sin(th) + 0.10, color=MUTED, lw=0.7,
        ls=(0, (4, 3)), zorder=6)
ax.annotate('', xy=(1.55, 0.82), xytext=(1.05, 0.96), zorder=6,
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.8,
                            mutation_scale=7))

# ---------------- labels ----------------
def lab(txt, tip, tx, ty, ha='center', fs=6.1):
    ax.annotate(txt, xy=tip, xytext=(tx, ty), fontsize=fs, color=INK, ha=ha,
                va='center', zorder=16, linespacing=1.25,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.75,
                                shrinkA=1.4, shrinkB=1.0))

lab("cilia in longitudinal rows", (-3.10, 1.12), -3.40, 2.42)
lab("pellicle", (-1.95, 1.22), -1.05, 1.92)
lab("trichocyst", (-0.62, 1.02), 0.05, 2.42)
lab("micronucleus", (0.58, 0.78), 1.45, 1.92)
lab("posterior contractile\nvacuole with canals", (2.55, 0.86), 3.70, 2.38)
lab("longer caudal cilia", (4.30, 0.42), 5.15, 1.30, ha='left')
lab("anterior end", (-3.86, 0.10), -5.15, 1.30, ha='right')
lab("anterior contractile\nvacuole", (-2.60, 0.72), -5.15, 0.22, ha='right')
lab("ectoplasm", (-3.28, -0.72), -5.15, -0.86, ha='right')
lab("endoplasm", (-2.85, -0.52), -5.15, -1.72, ha='right')
lab("macronucleus", (-0.34, 0.16), -2.40, -1.62)
lab("vestibule", (0.55, -0.42), 0.35, -1.62)
lab("food vacuole", (2.55, -0.40), 3.25, -1.62)
lab("oral groove\n(peristome)", (-0.75, -0.72), -1.45, -2.36)
lab("cytostome and\ncytopharynx", (1.30, 0.24), 1.28, -2.36)
lab("cytopyge (cell anus)", (1.86, -0.79), 4.35, -2.40)

ax.text(0.00, 2.92, "$\\it{Paramecium\\ caudatum}$ — ventral view",
        ha='center', fontsize=7.0, color=INK)
ax.set_xlim(-7.10, 7.10); ax.set_ylim(-2.90, 3.10)
ax.set_aspect('equal'); ax.axis('off')
```

A thin, firm, elastic **pellicle** fixes the cell's shape; it is sculptured into
hexagons with one cilium through the centre of each, so the cilia lie in neat
longitudinal rows. Beneath it lie a clear outer **ectoplasm** and a granular
inner **endoplasm**. Spindle-shaped **trichocysts** in the ectoplasm discharge a
sticky thread for anchorage and defence.

A distinctive feature is **nuclear dimorphism**. *P. caudatum* has one large,
kidney-shaped, polyploid **macronucleus** controlling all vegetative work, and
one small diploid **micronucleus** in a depression of it, the genetic reserve
used in sexual reproduction. (*P. aurelia* has two micronuclei — a favourite
one-mark trap.)

On the ventral surface a shallow **oral groove** (peristome) runs obliquely
back to about mid-body, deepening into a **vestibule**, then the **cytostome**
and a short **cytopharynx**; a **cytopyge** (cell anus) lies just behind it.

### *Paramecium*: locomotion, nutrition and osmoregulation

**Locomotion.** Each cilium makes a stiff *effective stroke* backwards and to
the right, then a limp *recovery stroke*; successive cilia start a fraction of a
beat later, so a wave travels along the body. This **metachronal rhythm** drives
the animal forward at about 1500 μm per second while the oblique stroke rotates
it, so the path is a wide spiral. Meeting an obstacle the cilia reverse, the
animal backs off, swings its front end round and tries again — the **avoiding
reaction**.

**Nutrition** is holozoic filter feeding. Longer cilia in the oral groove drive
water carrying bacteria into the vestibule; at the base of the cytopharynx the
food collects in a **food vacuole** which pinches off and circulates by
cyclosis. Digestion is **intracellular** in two phases — the vacuole first turns
acidic (about pH 4), killing the bacteria, then alkaline as proteases, amylases
and lipases are added. Products diffuse into the cytoplasm; the residue leaves
at the cytopyge.

**Osmoregulation.** Pond water is hypotonic, so water enters continuously. Two
**contractile vacuoles**, anterior and posterior, each fed by radiating canals,
collect it and discharge through a temporary pore, contracting alternately every
10–20 seconds. Their job is water balance, not excretion: ammonia and carbon
dioxide diffuse out across the body surface and oxygen diffuses in.

### *Paramecium*: reproduction

```figure caption="*Paramecium*: binary fission (left) and conjugation (right)."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Ellipse
fig, ax = plt.subplots(figsize=(5.2, 3.3))
BODY = "#f3e3cc"; EDGE = "#8a6a45"; MAC = "#c9b7d8"; MIC = "#7c5fa0"

def cell(cx, cy, s=1.0, waist=0.0, rot=0.0):
    u = np.linspace(-1, 1, 220)
    w = 0.42*np.sqrt(np.clip(1 - u**2, 0, 1))*(1 - 0.22*u)
    if waist:
        w = w*(1 - waist*np.exp(-(u/0.20)**2))
    pts = np.vstack([np.c_[u, w], np.c_[u[::-1], -w[::-1]]])*s
    th = np.radians(rot)
    R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    pts = pts @ R.T + np.array([cx, cy])
    ax.add_patch(Polygon(pts, closed=True, fc=BODY, ec=EDGE, lw=1.2, zorder=4))
    d = np.roll(pts, -1, 0) - np.roll(pts, 1, 0)
    L = np.hypot(d[:, 0], d[:, 1]); L[L == 0] = 1
    nx, ny = d[:, 1]/L, -d[:, 0]/L
    a = 0.5*np.sum(pts[:, 0]*np.roll(pts[:, 1], -1) - np.roll(pts[:, 0], -1)*pts[:, 1])
    if a < 0:
        nx, ny = -nx, -ny
    for i in range(0, len(pts), 15):
        ax.plot([pts[i, 0], pts[i, 0] + nx[i]*0.12*s],
                [pts[i, 1], pts[i, 1] + ny[i]*0.12*s],
                color=EDGE, lw=0.6, zorder=3, solid_capstyle='round')

def mac(cx, cy, w=0.60, h=0.28):
    ax.add_patch(Ellipse((cx, cy), w, h, fc=MAC, ec=INK, lw=0.8, zorder=6))

def mic(cx, cy, r=0.075):
    ax.add_patch(Circle((cx, cy), r, fc=MIC, ec=INK, lw=0.7, zorder=7))

def arrow(x0, x1, y):
    ax.annotate('', xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.2, mutation_scale=9))

# ---------- (a) transverse binary fission ----------
Y = 1.95
cell(-3.65, Y, 1.15); mac(-3.65, Y + 0.07, 0.62, 0.30); mic(-3.28, Y + 0.02)
ax.text(-3.65, Y - 1.15, "parent cell", ha='center', fontsize=6.4, color=MUTED)

arrow(-2.50, -1.70, Y)

cell(-0.55, Y, 1.15, waist=0.55)
mac(-0.95, Y + 0.05, 0.50, 0.26); mac(-0.15, Y + 0.05, 0.50, 0.26)
mic(-0.74, Y - 0.10); mic(-0.36, Y - 0.10)
ax.text(-0.55, Y - 1.15, "nuclei divide; a transverse\nconstriction appears",
        ha='center', fontsize=6.4, color=MUTED)

arrow(0.62, 1.32, Y)

for cx in (2.25, 3.95):
    cell(cx, Y, 0.85); mac(cx, Y + 0.05, 0.46, 0.24); mic(cx + 0.28, Y)
ax.text(3.10, Y - 1.15, "two daughter cells", ha='center', fontsize=6.4, color=MUTED)
ax.text(-5.30, Y + 1.00, "(a)  Transverse binary fission  —  asexual",
        ha='left', fontsize=7.5, color=INK)

# ---------- (b) conjugation ----------
Yb = -1.62
cell(-3.20, Yb + 0.50, 1.15, rot=6)
cell(-3.20, Yb - 0.50, 1.15, rot=-6)
ax.plot([-2.95, -2.35], [Yb + 0.02, Yb + 0.02], color=BODY, lw=6.0, zorder=5)
ax.plot([-2.95, -2.35], [Yb + 0.26, Yb + 0.26], color=EDGE, lw=0.8, zorder=6)
ax.plot([-2.95, -2.35], [Yb - 0.22, Yb - 0.22], color=EDGE, lw=0.8, zorder=6)
mac(-3.78, Yb + 0.62, 0.52, 0.24); mac(-3.78, Yb - 0.62, 0.52, 0.24)
for xx in (-2.82, -2.48):
    mic(xx, Yb + 0.38); mic(xx, Yb - 0.38)
ax.annotate('', xy=(-2.50, Yb - 0.28), xytext=(-2.80, Yb + 0.28),
            arrowprops=dict(arrowstyle='-|>', color="#a2453e", lw=1.0,
                            mutation_scale=8, connectionstyle="arc3,rad=0.4"), zorder=9)
ax.annotate('', xy=(-2.80, Yb + 0.28), xytext=(-2.50, Yb - 0.28),
            arrowprops=dict(arrowstyle='-|>', color="#a2453e", lw=1.0,
                            mutation_scale=8, connectionstyle="arc3,rad=0.4"), zorder=9)

def lb(txt, tip, tx, ty):
    ax.annotate(txt, xy=tip, xytext=(tx, ty), fontsize=6.2, color=INK, ha='left',
                va='center', zorder=10,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.75,
                                shrinkA=1.5, shrinkB=1.0))
lb("cytoplasmic bridge at the\nunited oral grooves", (-2.62, Yb + 0.02), -1.70, Yb + 0.92)
lb("migratory micronuclei are\nexchanged between partners", (-2.45, Yb + 0.15), -1.70, Yb - 0.12)
lb("macronucleus breaks down\nand disappears", (-3.78, Yb - 0.62), -1.70, Yb - 1.05)
ax.text(-5.30, Yb + 1.36, "(b)  Conjugation  —  sexual (exchange of micronuclei)",
        ha='left', fontsize=7.5, color=INK)

ax.set_xlim(-5.40, 5.40); ax.set_ylim(-3.45, 3.45)
ax.set_aspect('equal'); ax.axis('off')
```

**Transverse binary fission** is the asexual method and occurs two or three
times a day in good conditions. The micronucleus divides mitotically and the
macronucleus amitotically; a new oral groove and contractile vacuoles form; and
a transverse constriction separates an anterior *proter* from a posterior
*opisthe*. Note the plane — fission is **transverse** in *Paramecium* but
longitudinal in *Euglena*.

**Conjugation** is the sexual process. It does not increase numbers — two
conjugants give two ex-conjugants — but it reshuffles genes and rejuvenates a
clone that has divided asexually too long. Two individuals of different mating
types unite by their oral surfaces. In each the macronucleus disintegrates and
the micronucleus divides meiotically into four haploid nuclei, three of which
degenerate; the survivor divides mitotically into a large stationary and a small
migratory pronucleus. The migratory nuclei are exchanged across the cytoplasmic
bridge, and each fuses with the partner's stationary nucleus to give a diploid
**synkaryon**; the ex-conjugants separate and rebuild one macronucleus and one
micronucleus each. **Endomixis** and **autogamy** are similar reorganisations
without a partner.

::: example
**Working out the real size of a protist.** A drawing of *Paramecium* is 60 mm
long and is labelled "×250". What is the animal's actual length in micrometres?

Magnification is the image size divided by the object size,

$$ M = \frac{\text{size of image}}{\text{size of object}} \;\Rightarrow\; L = \frac{60\ \text{mm}}{250} = 0.24\ \text{mm} $$

and $0.24\ \text{mm} \times 1000 = 240\ \mu\text{m}$, comfortably inside the
170–330 μm range for *P. caudatum*. Two traps: magnification has no units, and
you must multiply millimetres by 1000 to get micrometres, not divide.
:::

::: derivation
**Why being small suits a protist.** For a spherical cell of radius $r$,

$$ S = 4\pi r^{2}, \qquad V = \tfrac{4}{3}\pi r^{3} $$

so that, dividing and cancelling every constant,

$$ \frac{S}{V} = \frac{4\pi r^{2}}{\tfrac{4}{3}\pi r^{3}} = \frac{3}{r} $$

The exchange surface available per unit of living substance is inversely
proportional to the radius. This one result explains why a protist needs no
lungs, no blood and no kidneys, and why anything much larger must invent them.
:::

::: example
**Putting numbers on it.** Compare a spherical protist of radius 50 μm with a
frog treated as a sphere of radius 3.0 cm.

Protist: $r = 5.0 \times 10^{-5}\ \text{m}$, so
$S/V = 3/(5.0 \times 10^{-5}) = 6.0 \times 10^{4}\ \text{m}^{-1}$.

Frog: $r = 3.0 \times 10^{-2}\ \text{m}$, so
$S/V = 3/(3.0 \times 10^{-2}) = 1.0 \times 10^{2}\ \text{m}^{-1}$.

The protist has 600 times as much exchange surface per unit volume, and no
point in it is more than 50 μm from the outside — well within the reach of
diffusion. The frog, with one six-hundredth of the relative surface, must have
lungs, a vascular skin, a heart and a closed circulation to do the same job.
:::

### Importance of protists

Protists matter out of all proportion to their size. They cause malaria
(*Plasmodium*, carried by female *Anopheles*), amoebic dysentery, giardiasis,
sleeping sickness and kala-azar, the last endemic in Nepal's eastern Terai.
Diatoms and dinoflagellates are the dominant phytoplankton of the oceans, and
ciliates graze bacteria in soil and in sewage-sludge tanks. Foraminiferan shells
and diatom frustules accumulate as chalk and **diatomite**, and flagellates such
as *Trichonympha* digest cellulose in the gut of termites.

## 8.2 Animalia

Kingdom Animalia contains the multicellular, eukaryotic, heterotrophic organisms
whose cells lack a cell wall and plastids. Animals share collagen and cell
junctions binding the cells; a diploid adult developed from a zygote through
blastula and gastrula stages; glycogen as the store; movement at some stage; and
nervous and muscular tissue, which no other kingdom has. About 35 phyla are
recognised; the syllabus asks for nine, sorted on four structural questions.

### Levels of organisation

| Level | What it means | Found in |
|---|---|---|
| Protoplasmic | one cell performs all functions using organelles | Protista |
| Cellular | cells loosely aggregated with some division of labour, no true tissues | Porifera |
| Cell–tissue | similar cells organised into definite tissues, e.g. the nerve net | Coelenterata |
| Tissue–organ | tissues combine into organs, but organ systems are incomplete | Platyhelminthes |
| Organ–system | organs grouped into systems, each with one job | Nemathelminthes to Chordata |

### Body plan

1. **Cell-aggregate plan.** A loose colony of cells round a central cavity with
   no mouth and no gut; water carrying food enters through pores and leaves by
   an osculum, and each cell feeds itself. Sponges only.
2. **Blind-sac plan.** One cavity with a single opening serving as mouth *and*
   anus, so feeding is discontinuous. Coelenterata and Platyhelminthes.
3. **Tube-within-a-tube plan.** A complete gut runs from mouth to anus inside
   the body-wall tube, so food passes one way through specialised regions and
   feeding, digestion and egestion go on at once. Nemathelminthes onwards — the
   plan of every higher animal.

### Symmetry

```figure caption="Body symmetry: asymmetrical, radial and bilateral."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Ellipse
fig, axes = plt.subplots(1, 3, figsize=(5.2, 2.6))
BODY = "#e3ecf4"; EDGE = "#2c5f96"; PL = "#c0392b"
YT_, YS_ = -2.22, -2.66
rng = np.random.default_rng(11)

# ================= (a) asymmetrical: Amoeba =================
ax = axes[0]
th = np.linspace(0, 2*np.pi, 500)
r = 0.86*(1.00 + 0.26*np.sin(3*th + 0.7) + 0.20*np.sin(5*th + 2.1)
          + 0.13*np.sin(7*th + 4.0) + 0.09*np.sin(2*th))
ax.add_patch(Polygon(np.c_[r*np.cos(th), r*np.sin(th) + 0.10], closed=True,
                     fc=BODY, ec=EDGE, lw=1.2, zorder=3))
ax.add_patch(Ellipse((0.16, 0.18), 0.40, 0.30, angle=20, fc="#b9c6d6", ec=EDGE,
                     lw=0.8, zorder=4))
for _ in range(9):
    a = 2*np.pi*rng.random(); rr = 0.58*np.sqrt(rng.random())
    ax.add_patch(Circle((rr*np.cos(a), rr*np.sin(a) + 0.10), 0.055,
                        fc="#9fb2c6", ec='none', zorder=4))
for a in (0.5, 2.0, 3.6, 5.2):
    ax.plot([-1.40*np.cos(a), 1.40*np.cos(a)],
            [-1.40*np.sin(a) + 0.10, 1.40*np.sin(a) + 0.10],
            color=PL, lw=0.8, ls=(0, (3, 2)), zorder=5)
ax.annotate("no plane cuts it\ninto equal halves", xy=(0.62, -0.60),
            xytext=(0.10, -1.62), fontsize=5.7, color=PL, ha='center',
            va='center', linespacing=1.3,
            bbox=dict(fc='white', ec='none', pad=0.6),
            arrowprops=dict(arrowstyle='-', color=PL, lw=0.7))
ax.text(0, YT_, "(a)  asymmetrical", ha='center', fontsize=6.8, color=INK)
ax.text(0, YS_, "$\\it{Amoeba}$, most sponges", ha='center', fontsize=5.9,
        color=MUTED)

# ================= (b) radial: Hydra seen from above =================
ax = axes[1]
for a in np.linspace(0, np.pi, 7)[:-1]:
    ax.plot([-1.44*np.cos(a), 1.44*np.cos(a)], [-1.44*np.sin(a), 1.44*np.sin(a)],
            color=PL, lw=0.8, ls=(0, (3, 2)), zorder=6)
ax.add_patch(Circle((0, 0), 0.80, fc=BODY, ec=EDGE, lw=1.2, zorder=3))
ax.add_patch(Circle((0, 0), 0.26, fc="#f6e2c8", ec=EDGE, lw=1.0, zorder=5))
for a in np.linspace(0, 2*np.pi, 9)[:-1]:
    t = np.linspace(0, 1, 40)
    rr = 0.80 + 0.52*t; aa = a + 0.30*t**2
    ax.plot(rr*np.cos(aa), rr*np.sin(aa), color=EDGE, lw=1.1, zorder=4,
            solid_capstyle='round')
ax.annotate("mouth", xy=(0.13, 0.13), xytext=(0.98, 1.16), fontsize=5.8,
            color=INK, ha='center', zorder=10,
            bbox=dict(fc='white', ec='none', pad=0.6),
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7))
ax.text(0.0, -1.70, "any plane through the\naxis gives equal halves",
        ha='center', va='center', fontsize=5.7, color=PL, linespacing=1.3,
        zorder=10, bbox=dict(fc='white', ec='none', pad=0.6))
ax.text(0, YT_, "(b)  radial", ha='center', fontsize=6.8, color=INK)
ax.text(0, YS_, "$\\it{Hydra}$, jellyfish", ha='center', fontsize=5.9, color=MUTED)

# ================= (c) bilateral: frog seen from above =================
ax = axes[2]
DY = 0.34
ax.plot([0, 0], [-1.40 + DY, 1.52 + DY], color=PL, lw=0.9, ls=(0, (3, 2)),
        zorder=7)
yk = [1.15, 0.92, 0.70, 0.26, -0.26, -0.78, -1.08]
wk = [0.26, 0.40, 0.46, 0.50, 0.46, 0.30, 0.14]
y = np.linspace(yk[-1], yk[0], 300); w = np.interp(y, yk[::-1], wk[::-1])
ax.add_patch(Polygon(np.vstack([np.c_[w, y + DY], np.c_[-w[::-1], y[::-1] + DY]]),
                     closed=True, fc=BODY, ec=EDGE, lw=1.2, zorder=3))
for s in (1, -1):
    ax.add_patch(Circle((s*0.17, 1.04 + DY), 0.095, fc="#f6e2c8", ec=EDGE,
                        lw=0.8, zorder=5))
    ax.plot([s*0.42, s*0.80, s*0.64], [0.62 + DY, 0.34 + DY, 0.02 + DY],
            color=EDGE, lw=1.1, zorder=2, solid_capstyle='round')
    for d in (-0.14, 0.0, 0.14):
        ax.plot([s*0.64, s*0.88], [0.02 + DY, -0.10 + d + DY], color=EDGE,
                lw=0.7, zorder=2)
    ax.plot([s*0.38, s*0.86, s*0.62], [-0.58 + DY, -0.90 + DY, -1.38 + DY],
            color=EDGE, lw=1.2, zorder=2, solid_capstyle='round')
    for d in (-0.20, -0.05, 0.10, 0.25):
        ax.plot([s*0.62, s*0.92], [-1.38 + DY, -1.58 + d*0.6 + DY], color=EDGE,
                lw=0.7, zorder=2)
ax.text(0.0, 1.76, "mid-sagittal plane", ha='center', fontsize=5.7, color=PL)
ax.text(0, YT_, "(c)  bilateral", ha='center', fontsize=6.8, color=INK)
ax.text(0, YS_, "frog, insects, human", ha='center', fontsize=5.9, color=MUTED)

for ax in axes:
    ax.set_xlim(-1.60, 1.60); ax.set_ylim(-2.96, 1.92)
    ax.set_aspect('equal'); ax.axis('off')
```

- **Asymmetrical:** no plane divides the body into equal halves — *Amoeba*, most
  sponges.
- **Radial:** any plane through the central axis gives equal halves, so the
  animal meets its world equally on all sides; typical of sessile or drifting
  animals such as *Hydra*. In adult echinoderms it is **pentamerous** radial
  symmetry, built on five rays.
- **Bilateral:** one mid-sagittal plane gives mirror-image right and left
  halves. This goes with directed forward movement and therefore with
  **cephalisation**, the gathering of sense organs, ganglia and mouth at the
  leading end to form a head.

### Germ layers and the coelom

**Diploblastic** animals build the body from ectoderm and endoderm with a
non-cellular jelly (mesogloea) between — Porifera and Coelenterata.
**Triploblastic** animals insert mesoderm between the two, and mesoderm is what
makes muscle, blood, skeleton, kidneys and gonads possible.

The **coelom** is a fluid-filled cavity lying *within the mesoderm* and lined
throughout by mesodermal peritoneum. It frees the gut to move independently of
the body wall, works as a hydrostatic skeleton and transport medium, and gives
organs and gametes room to enlarge.

```figure caption="Coelom types in transverse section."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Patch
fig, axes = plt.subplots(1, 3, figsize=(5.2, 3.0))

ECT, ECTE = "#cfe0ee", "#2c5f96"        # ectoderm
MES, MESE = "#f2d7d4", "#a2453e"        # mesoderm
END, ENDE = "#f2e3c4", "#9a7330"        # endoderm

def lab(ax, txt, tip, tx, ty, ha='center', fs=5.6):
    ax.annotate(txt, xy=tip, xytext=(tx, ty), fontsize=fs, color=INK, ha=ha,
                va='center', zorder=14, linespacing=1.25,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7,
                                shrinkA=1.2, shrinkB=1.0))

def panel(ax, kind, title, sub):
    R = 0.98
    ax.add_patch(Circle((0, 0), R, fc=ECT, ec=ECTE, lw=1.3, zorder=2))
    ax.add_patch(Circle((0, 0), R - 0.10, fc=MES, ec=MESE, lw=1.0, zorder=3))
    if kind == "a":
        rng = np.random.default_rng(3)
        for _ in range(170):
            rr = (R - 0.14)*np.sqrt(rng.random()); th = 2*np.pi*rng.random()
            if rr < 0.38:
                continue
            ax.plot([rr*np.cos(th)], [rr*np.sin(th)], marker='o', ms=1.4,
                    color=MESE, alpha=0.6, zorder=4)
    else:
        ax.add_patch(Circle((0, 0), R - 0.22, fc="white", ec=MESE, lw=0.9,
                            zorder=4))
    if kind == "c":
        ax.add_patch(Circle((0, 0), 0.42, fc=MES, ec=MESE, lw=1.0, zorder=5))
        for s in (1, -1):
            ax.plot([0, 0], [s*0.42, s*(R - 0.10)], color=MESE, lw=1.0, zorder=5)
    ax.add_patch(Circle((0, 0), 0.30, fc=END, ec=ENDE, lw=1.1, zorder=6))
    ax.text(0, -1.56, title, ha='center', va='top', fontsize=6.8, color=INK)
    ax.text(0, -1.96, sub, ha='center', va='top', fontsize=5.8, color=MUTED,
            linespacing=1.3)
    ax.set_xlim(-1.62, 1.62); ax.set_ylim(-2.78, 1.88)
    ax.set_aspect('equal'); ax.axis('off')

# ---------------- (a) acoelomate ----------------
ax = axes[0]
panel(ax, "a", "(a)  acoelomate",
      "no cavity; mesodermal\nparenchyma fills the space\n$\\it{Planaria}$, $\\it{Taenia}$")
lab(ax, "body wall", (-0.70, 0.68), -1.58, 1.62, ha='left')
lab(ax, "gut (endoderm)", (0.21, 0.21), 1.58, 1.62, ha='right')
lab(ax, "parenchyma (mesoderm)", (0.62, -0.56), 0.00, -1.26)

# ---------------- (b) pseudocoelomate ----------------
ax = axes[1]
panel(ax, "b", "(b)  pseudocoelomate",
      "cavity is a persistent\nblastocoel, unlined round the gut\n$\\it{Ascaris}$, rotifers")
lab(ax, "mesoderm on the\nbody-wall side only", (-0.88, 0.32), -1.58, 1.52,
    ha='left')
lab(ax, "pseudocoel", (0.06, 0.60), 1.58, 1.18, ha='right')
lab(ax, "gut with no peritoneum", (0.22, -0.24), 0.00, -1.26)

# ---------------- (c) coelomate ----------------
ax = axes[2]
panel(ax, "c", "(c)  coelomate",
      "true coelom inside mesoderm,\nlined by peritoneum throughout\nearthworm, frog")
lab(ax, "somatic\nperitoneum", (-0.84, 0.38), -1.58, 1.52, ha='left')
lab(ax, "coelom", (0.00, 0.64), 1.58, 1.62, ha='right')
lab(ax, "visceral peritoneum", (0.34, -0.30), 0.58, -1.26)
lab(ax, "mesentery", (0.00, -0.66), -1.20, -1.26)

leg = [Patch(fc=ECT, ec=ECTE, label="ectoderm"),
       Patch(fc=MES, ec=MESE, label="mesoderm"),
       Patch(fc=END, ec=ENDE, label="endoderm")]
fig.legend(handles=leg, loc='lower center', ncol=3, fontsize=6.0, frameon=False,
           handlelength=1.1, handleheight=0.9, columnspacing=1.8,
           handletextpad=0.5, bbox_to_anchor=(0.5, 0.015))
```

| Condition | Cavity | Lining | Example |
|---|---|---|---|
| Acoelomate | none; gut and body wall packed with mesodermal parenchyma | — | *Planaria*, *Taenia* |
| Pseudocoelomate | present, but a persistent blastocoel | mesoderm outside only, not round the gut | *Ascaris*, rotifers |
| Coelomate | a true coelom | peritoneum on both body wall and gut | earthworm, cockroach, frog |

Coelomates divide further by the fate of the blastopore. In **protostomes**
(Annelida, Arthropoda, Mollusca) it becomes the mouth and the coelom is a split
in solid mesoderm (**schizocoely**); in **deuterostomes** (Echinodermata,
Chordata) it becomes the anus and the coelom buds from the archenteron
(**enterocoely**).

### Segmentation and the basis of classification

**Metameric segmentation** divides the body along its long axis into similar
units, each repeating the same organs — nephridia, ganglia, vessels, muscle
blocks — as in Annelida, Arthropoda and Chordata. A tapeworm's "segments" are
budded reproductive sacs, not true metameres: **pseudometamerism**.

```figure caption="Classification of Kingdom Animalia into nine phyla."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.2, 4.5))

SPAN = 28.0
SX = 5.0/SPAN                                   # inches per x-unit
GAP = 0.55

BLU, BLE = "#cfe0ee", "#2c5f96"
GRN, GRE = "#cfe3d4", "#2e8b57"
TAN, TAE = "#f2e3c4", "#9a7330"
PNK, PNE = "#f2d7d4", "#a2453e"

def _plain(t):
    return t.replace("$\\it{", "").replace("}$", "")

def width(txt, fs):
    n = max(len(_plain(l)) for l in txt.split("\n"))
    return n*(0.70*fs/72.0)/SX*1.36 + 0.34

def pack(items, y, centre=0.0):
    """items: list of dicts with txt, fc, ec, fs, h. Returns list of centres."""
    ws = [width(it["txt"], it["fs"]) for it in items]
    total = sum(ws) + GAP*(len(ws) - 1)
    x = centre - total/2
    cs = []
    for it, w in zip(items, ws):
        cx = x + w/2
        ax.add_patch(FancyBboxPatch((x, y - it["h"]/2), w, it["h"],
                                    boxstyle="round,pad=0.02,rounding_size=0.12",
                                    fc=it["fc"], ec=it["ec"], lw=0.95, zorder=5))
        ax.text(cx, y, it["txt"], ha='center', va='center', fontsize=it["fs"],
                color=INK, zorder=6, linespacing=1.3)
        cs.append(cx); x += w + GAP
    return cs

def elbow(x0, y0, x1, y1, ym):
    ax.plot([x0, x0, x1, x1], [y0, ym, ym, y1], color=MUTED, lw=0.8, zorder=3)

def P(txt, fs=5.1, h=0.88):   return dict(txt=txt, fc=GRN, ec=GRE, fs=fs, h=h)
def B(txt, fs=5.3, h=0.80):   return dict(txt=txt, fc=BLU, ec=BLE, fs=fs, h=h)
def T(txt, fs=5.1, h=0.58):   return dict(txt=txt, fc=TAN, ec=TAE, fs=fs, h=h)
def K(txt, fs=5.3, h=0.68):   return dict(txt=txt, fc=PNK, ec=PNE, fs=fs, h=h)

Y5, Y4, Y3, Y2, Y1, Y0 = 1.55, 3.70, 5.35, 6.95, 8.50, 9.95

# ---------- row 5: the coelomate phyla ----------
r5 = pack([P("ANNELIDA\n$\\it{Pheretima}$"), P("ARTHROPODA\n$\\it{Periplaneta}$"),
           P("MOLLUSCA\n$\\it{Pila}$"), P("ECHINO-\nDERMATA\n$\\it{Asterias}$", h=1.22),
           P("CHORDATA\n$\\it{Rana}$")], Y5, centre=1.0)

# ---------- row 4 ----------
r4 = pack([P("PLATY-\nHELMINTHES\n$\\it{Taenia}$", h=1.22),
           P("NEMATHEL-\nMINTHES\n$\\it{Ascaris}$", h=1.22),
           K("protostomia\nmouth first"), K("deuterostomia\nanus first")],
          Y4, centre=-0.8)
for c in r5[:3]:
    elbow(r4[2], Y4 - 0.34, c, Y5 + 0.61, 2.62)
elbow(r4[3], Y4 - 0.34, r5[3], Y5 + 0.61, 2.62)
elbow(r4[3], Y4 - 0.34, r5[4], Y5 + 0.44, 2.62)

# ---------- row 3: coelom ----------
r3 = pack([T("acoelomate"), T("pseudocoelomate"), T("coelomate"),
           P("COELENTERATA\n$\\it{Hydra}$")], Y3, centre=0.6)
elbow(r3[0], Y3 - 0.29, r4[0], Y4 + 0.61, 4.62)
elbow(r3[1], Y3 - 0.29, r4[1], Y4 + 0.61, 4.62)
elbow(r3[2], Y3 - 0.29, r4[2], Y4 + 0.34, 4.62)
elbow(r3[2], Y3 - 0.29, r4[3], Y4 + 0.34, 4.62)

# ---------- row 2: germ layers ----------
r2 = pack([B("triploblastic\nbilateral"), B("diploblastic\nradial"),
           P("PORIFERA\n$\\it{Sycon}$")], Y2, centre=1.4)
for c in r3[:3]:
    elbow(r2[0], Y2 - 0.40, c, Y3 + 0.29, 6.16)
elbow(r2[1], Y2 - 0.40, r3[3], Y3 + 0.44, 6.16)

# ---------- row 1: level of organisation ----------
r1 = pack([B("tissue level and above", h=0.62), B("cellular level\n(no true tissues)")],
          Y1, centre=1.0)
elbow(r1[0], Y1 - 0.31, r2[0], Y2 + 0.40, 7.75)
elbow(r1[0], Y1 - 0.31, r2[1], Y2 + 0.40, 7.75)
elbow(r1[1], Y1 - 0.40, r2[2], Y2 + 0.44, 7.75)

# ---------- root ----------
root = pack([dict(txt="KINGDOM ANIMALIA", fc="#e3e8ee", ec=INK, fs=6.9, h=0.70)],
            Y0, centre=1.0)
elbow(root[0], Y0 - 0.35, r1[0], Y1 + 0.31, 9.25)
elbow(root[0], Y0 - 0.35, r1[1], Y1 + 0.40, 9.25)

# ---------- row captions ----------
XL = 1.0 - SPAN/2 + 0.10
for yy, t in [(Y1, "level of\norganisation"), (Y2, "germ layers\nand symmetry"),
              (Y3, "coelom"), (Y5, "phyla")]:
    ax.text(XL, yy, t, fontsize=5.0, color=MUTED, ha='left', va='center',
            style='italic', linespacing=1.3)
for yy in (9.25, 7.75, 6.16, 4.62, 2.62):
    ax.plot([XL - 0.05, 1.0 + SPAN/2 - 0.10], [yy, yy], color=GRID, lw=0.6,
            ls=(0, (4, 4)), zorder=1)

ax.set_xlim(1.0 - SPAN/2, 1.0 + SPAN/2); ax.set_ylim(0.75, 10.55)
ax.axis('off')
```

The nine phyla follow in the traditional order of increasing complexity.

### 1. Phylum Porifera

The sponges — the simplest animals, at the **cellular** level of organisation.

- Aquatic, mostly marine, **sessile** as adults; asymmetrical or radial.
- **Diploblastic**: an outer pinacoderm, an inner choanoderm, and a gelatinous
  mesenchyme between them containing amoebocytes and skeletal cells.
- The body wall is pierced by microscopic **ostia**; water drawn through them
  enters the **spongocoel** and leaves by one large **osculum**. This one-way
  **canal system**, driven by flagella, brings food and oxygen and removes
  waste; its grades are **ascon** (*Leucosolenia*), **sycon** (*Sycon*) and
  **leucon** (*Spongilla*).
- **Choanocytes** (collar cells) line the canals, each straining bacteria with a
  collar of microvilli round a flagellum; digestion is **intracellular**.
- Support from an endoskeleton of calcareous or siliceous **spicules** or of the
  protein **spongin**. There is no mouth, gut, nervous system, muscle or organ.
- Reproduction asexual by budding, fragmentation and **gemmules**, and sexual —
  usually hermaphrodite, with a free-swimming larva. Regeneration is
  extraordinary.
- Examples: *Sycon*, *Spongilla*, *Euspongia* (bath sponge), *Euplectella*
  (Venus' flower basket), *Hyalonema*.

```figure caption="L.S. of (a) the sponge *Sycon* and (b) *Hydra*."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle
fig, axes = plt.subplots(1, 2, figsize=(5.2, 3.4))
WALL = "#f0dfc4"; EDGE = "#8a6a45"; CAV = "#dcebf4"; ENDO = "#bcd9c2"

def sil(ax, ys, ws, fc, ec=EDGE, lw=1.2, z=2, close_top=False, top=None):
    y = np.linspace(ys[0], ys[-1], 250)
    w = np.interp(y, ys, ws)
    pts = np.vstack([np.c_[w, y], np.c_[-w[::-1], y[::-1]]])
    ax.add_patch(Polygon(pts, closed=True, fc=fc, ec=ec, lw=lw, zorder=z))
    return y, w

def lab(ax, txt, tip, tx, ty, ha='left', fs=6.1):
    ax.annotate(txt, xy=tip, xytext=(tx, ty), fontsize=fs, color=INK, ha=ha,
                va='center', zorder=12,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7,
                                shrinkA=1.5, shrinkB=1.0))

# ================= (a) Sycon, longitudinal section =================
ax = axes[0]
ys = [0.00, 0.25, 0.70, 1.40, 2.60, 3.30, 3.60]
wo = [0.16, 0.32, 0.62, 0.80, 0.82, 0.66, 0.58]
wi = [0.00, 0.00, 0.22, 0.34, 0.36, 0.30, 0.30]
sil(ax, ys, wo, WALL, z=2)
yy = np.linspace(0.55, 3.72, 200)
ww = np.interp(yy, ys, wi)
ax.add_patch(Polygon(np.vstack([np.c_[ww, yy], np.c_[-ww[::-1], yy[::-1]]]),
                     closed=True, fc=CAV, ec=EDGE, lw=0.9, zorder=3))
# radial canals + ostia with incurrent arrows
for yc in (1.00, 1.55, 2.10, 2.65):
    for s in (1, -1):
        a = np.interp(yc, ys, wo); b = np.interp(yc, ys, wi)
        ax.plot([s*b, s*a], [yc, yc], color=EDGE, lw=0.8, zorder=4)
        ax.annotate('', xy=(s*(a - 0.10), yc), xytext=(s*(a + 0.42), yc),
                    arrowprops=dict(arrowstyle='-|>', color="#1d6fb8", lw=0.9,
                                    mutation_scale=7), zorder=5)
# spicules on the surface and the oscular fringe
for yc in np.arange(0.8, 3.3, 0.30):
    for s in (1, -1):
        a = np.interp(yc, ys, wo)
        ax.plot([s*a, s*(a + 0.14)], [yc, yc + 0.10], color=MUTED, lw=1.0, zorder=4)
for k in range(9):
    xx = -0.30 + 0.075*k
    ax.plot([xx, xx*1.35], [3.72, 4.18], color=MUTED, lw=1.0, zorder=5)
ax.annotate('', xy=(0, 4.55), xytext=(0, 3.60),
            arrowprops=dict(arrowstyle='-|>', color="#1d6fb8", lw=1.3,
                            mutation_scale=9), zorder=6)
ax.plot([-0.55, 0.55], [-0.02, -0.02], color=EDGE, lw=2.0, zorder=1,
        solid_capstyle='round')

lab(ax, "osculum\n(excurrent opening)", (0.22, 3.68), 0.55, 4.62)
lab(ax, "oscular spicules", (-0.28, 3.98), -0.55, 4.55, ha='right')
lab(ax, "spongocoel\n(paragastric\ncavity)", (0.20, 2.40), 0.95, 2.00)
lab(ax, "ostium", (0.92, 2.65), 1.25, 3.28)
lab(ax, "radial canal\n(choanocytes)", (-0.55, 2.10), -1.00, 3.15, ha='right')
lab(ax, "body wall\n(2 layers)", (-0.72, 1.35), -1.05, 0.85, ha='right')
lab(ax, "base of attachment", (0.10, -0.02), 0.60, -0.62)
ax.text(0, 5.15, "(a)  $Sycon$  (Porifera), L.S.", ha='center', fontsize=7.4, color=INK)

# ================= (b) Hydra, longitudinal section =================
ax = axes[1]
ys = [0.00, 0.14, 0.40, 1.00, 2.10, 2.55, 2.80, 3.00]
w1 = [0.44, 0.26, 0.40, 0.48, 0.48, 0.42, 0.30, 0.10]
w2 = [0.34, 0.17, 0.31, 0.39, 0.39, 0.33, 0.22, 0.06]
w3 = [0.22, 0.06, 0.20, 0.28, 0.28, 0.23, 0.14, 0.02]
sil(ax, ys, w1, WALL, z=2)
sil(ax, ys, w2, ENDO, ec=EDGE, lw=0.7, z=3)
sil(ax, ys, w3, CAV, ec=EDGE, lw=0.7, z=4)
# whorl of tentacles round the base of the hypostome
for ang, x0 in [(118, -0.16), (142, -0.21), (166, -0.24),
                (62, 0.16), (38, 0.21), (14, 0.24)]:
    a = np.radians(ang); t = np.linspace(0, 1, 40); L = 1.25
    xs = x0 + L*t*np.cos(a)
    yt = 2.74 + L*t*np.sin(a) - 0.18*t**2
    ax.plot(xs, yt, color=EDGE, lw=2.6, zorder=1, solid_capstyle='round')
    ax.plot(xs, yt, color=WALL, lw=1.2, zorder=1, solid_capstyle='round')
    for tk in (0.28, 0.52, 0.76):
        i = int(tk*39)
        ax.add_patch(Circle((xs[i], yt[i]), 0.052, fc="#a2453e", ec='none', zorder=2))
ax.plot([-0.09, 0.09], [3.01, 3.01], color=EDGE, lw=1.5, zorder=6)
# bud growing out of the body wall
bys = [0.0, 0.10, 0.30, 0.50]; bw1 = [0.03, 0.17, 0.20, 0.13]
byy = np.linspace(0, 0.50, 60); bww = np.interp(byy, bys, bw1)
bud = np.vstack([np.c_[bww, byy], np.c_[-bww[::-1], byy[::-1]]])
ang = np.radians(-48)
R = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
bud = bud @ R.T + np.array([0.40, 1.15])
ax.add_patch(Polygon(bud, closed=True, fc=WALL, ec=EDGE, lw=1.0, zorder=5))
btip = np.array([0.50*np.sin(-ang), 0.50*np.cos(ang)]) + np.array([0.40, 1.15])
for da in (-26, 6, 36):
    a = np.radians(-42 + da)
    ax.plot([btip[0], btip[0] + 0.30*np.cos(a)], [btip[1], btip[1] + 0.30*np.sin(a)],
            color=EDGE, lw=1.1, zorder=5, solid_capstyle='round')
ax.plot([-0.50, 0.50], [-0.03, -0.03], color=EDGE, lw=2.2, zorder=1,
        solid_capstyle='round')

lab(ax, "tentacle", (0.82, 3.40), 1.30, 4.30)
lab(ax, "nematocyst\nbatteries", (-0.58, 3.38), -1.05, 4.25, ha='right')
lab(ax, "mouth on the\nhypostome", (0.05, 3.01), 0.75, 2.48)
lab(ax, "ectoderm", (-0.455, 1.85), -0.95, 2.35, ha='right')
lab(ax, "mesoglea", (-0.375, 1.55), -0.95, 1.80, ha='right')
lab(ax, "endoderm", (-0.31, 1.25), -0.95, 1.25, ha='right')
lab(ax, "coelenteron\n(gastrovascular\ncavity)", (0.10, 1.85), 0.62, 1.55)
lab(ax, "bud", (0.62, 0.92), 1.15, 0.58)
lab(ax, "basal disc", (-0.25, -0.03), -0.75, -0.62, ha='right')
ax.text(0, 5.15, "(b)  $Hydra$  (Coelenterata), L.S.", ha='center', fontsize=7.4,
        color=INK)

for ax in axes:
    ax.set_xlim(-2.7, 2.7); ax.set_ylim(-1.3, 5.4)
    ax.set_aspect('equal'); ax.axis('off')
fig.subplots_adjust(wspace=0.02)
```

### 2. Phylum Coelenterata (Cnidaria)

- Aquatic, mostly marine, a few fresh-water (*Hydra*); solitary or colonial.
- **Radially symmetrical, diploblastic**, at the **cell–tissue** level, with an
  acellular **mesogloea** between epidermis and gastrodermis.
- A single **coelenteron** (gastrovascular cavity) opens by a mouth ringed with
  tentacles; there is no anus, so the plan is **blind-sac**. Digestion is first
  extracellular in the cavity, then intracellular in the gastrodermis.
- The diagnostic character is the **cnidoblast**, a stinging cell holding a
  **nematocyst** — a coiled thread fired by the trigger-like cnidocil, used for
  capturing prey, defence and locomotion.
- **Polymorphism** is common: the sedentary **polyp** feeds, the free-swimming
  **medusa** reproduces sexually; in *Obelia* the two alternate
  (**metagenesis**).
- The nervous system is a diffuse **nerve net** with no brain; there are no
  respiratory, circulatory or excretory organs.
- Reproduction asexual by budding, sexual by gametes, with a ciliated
  **planula** larva.
- Examples: *Hydra*, *Obelia*, *Aurelia* (jellyfish), *Physalia* (Portuguese
  man-of-war), *Metridium* (sea anemone), *Corallium* (red coral).

### 3. Phylum Platyhelminthes

The flatworms — the first **triploblastic, bilaterally symmetrical** animals.

- Body dorsoventrally flattened and **acoelomate**, the space between the organs
  packed with mesodermal **parenchyma**; **tissue–organ** level; definite
  cephalisation.
- Free-living (*Planaria*) or, more often, **parasitic**, with **hooks and
  suckers**, a resistant tegument and reduced sense organs.
- The gut, when present, is **incomplete** — a mouth but no anus; in tapeworms
  it is absent and food is absorbed over the body surface.
- Excretion and osmoregulation by **protonephridia** ending in **flame cells**.
- Nervous system "ladder-like": paired cerebral ganglia, longitudinal cords and
  transverse commissures.
- Almost all **hermaphrodite**, with elaborate reproductive systems and life
  cycles running through several hosts and larvae (miracidium, sporocyst,
  redia, cercaria in *Fasciola*).
- Examples: *Planaria*, *Fasciola hepatica* (liver fluke), *Taenia solium* (pork
  tapeworm), *Schistosoma* (blood fluke), *Echinococcus*.

```figure caption="(a) *Planaria*; (b) *Ascaris lumbricoides*, both sexes."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Ellipse
fig, axes = plt.subplots(2, 1, figsize=(5.2, 3.8),
                         gridspec_kw=dict(hspace=0.16, height_ratios=[4.1, 5.7]))

BODY = "#f0e8d6"; EDGE = "#7d6244"; GUT = "#c98f62"; GUTE = "#8a5a33"
WORM = "#f0e2c2"; WEDGE = "#9a7330"

def lab(ax, txt, tip, tx, ty, ha='center', fs=5.9):
    ax.annotate(txt, xy=tip, xytext=(tx, ty), fontsize=fs, color=INK, ha=ha,
                va='center', zorder=16, linespacing=1.25,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.72,
                                shrinkA=1.3, shrinkB=1.0))

# ==================== (a) Planaria, dorsal view ====================
ax = axes[0]
xk = [-3.40, -3.26, -3.08, -2.92, -2.70, -2.35, -1.60, -0.60,  0.50,  1.60,
       2.40,  2.90]
wk = [ 0.07,  0.26,  0.52,  0.72,  0.52,  0.56,  0.64,  0.68,  0.62,  0.46,
       0.24,  0.04]
x = np.linspace(xk[0], xk[-1], 700)
w = np.interp(x, xk, wk)
ax.add_patch(Polygon(np.vstack([np.c_[x, w], np.c_[x[::-1], -w[::-1]]]),
                     closed=True, fc=BODY, ec=EDGE, lw=1.3, zorder=3))
for s in (1, -1):
    ax.add_patch(Circle((-2.80, s*0.17), 0.075, fc=INK, ec='none', zorder=7))
    ax.add_patch(Circle((-2.80, s*0.17), 0.145, fc='none', ec=EDGE, lw=0.8,
                        zorder=7))
def wid(xx):
    return np.interp(xx, xk, wk)

ax.plot([-2.64, -0.60], [0, 0], color=GUTE, lw=2.8, zorder=5,
        solid_capstyle='round')
for xx in (-2.42, -2.12, -1.82, -1.52, -1.22, -0.92):
    for s in (1, -1):
        ax.plot([xx, xx - 0.12, xx - 0.30], [0, s*wid(xx)*0.52, s*wid(xx)*0.80],
                color=GUTE, lw=1.5, zorder=5, solid_capstyle='round')
for s in (1, -1):
    ax.plot([0.16, 2.44], [s*0.24, s*0.24], color=GUTE, lw=2.2, zorder=5,
            solid_capstyle='round')
    ax.plot([-0.26, 0.16], [0, s*0.24], color=GUTE, lw=2.2, zorder=5)
    for xx in (0.42, 0.80, 1.18, 1.56, 1.94, 2.28):
        ax.plot([xx, xx - 0.10, xx - 0.26],
                [s*0.24, s*wid(xx)*0.66, s*wid(xx)*0.90],
                color=GUTE, lw=1.4, zorder=5, solid_capstyle='round')
ax.add_patch(Ellipse((-0.40, 0), 1.05, 0.34, fc="#f8efdd", ec=EDGE, lw=1.1,
                     zorder=6))
ax.add_patch(Ellipse((-0.40, 0), 0.86, 0.19, fc=GUT, ec=GUTE, lw=0.9, zorder=7))
ax.add_patch(Circle((0.02, 0), 0.075, fc="#a2453e", ec='none', zorder=8))
for s in (1, -1):
    ax.plot([-2.56, 2.38], [s*0.36]*2, color="#6a4a78", lw=0.75, zorder=4,
            ls=(0, (4, 2)))

lab(ax, "eyespots", (-2.80, 0.24), -4.35, 1.50)
lab(ax, "auricle", (-2.92, -0.66), -3.90, -1.50)
lab(ax, "three-branched intestine", (-1.60, 0.46), -1.15, 1.50)
lab(ax, "ventral nerve cords", (-1.30, -0.36), -1.30, -1.50)
lab(ax, "pharyngeal sheath", (-0.40, 0.17), 2.60, 1.50)
lab(ax, "muscular pharynx", (-0.40, -0.10), 2.05, -1.50)
lab(ax, "mouth (ventral)", (0.02, 0.06), 4.20, 1.50, ha='left')
lab(ax, "flat, acoelomate body", (1.90, -0.34), 4.25, -1.50, ha='left')
ax.text(-4.95, 1.90, "(a)  $\\it{Planaria}$ (Platyhelminthes), dorsal view",
        ha='left', va='center', fontsize=6.8, color=INK)
ax.set_xlim(-5.05, 6.45); ax.set_ylim(-2.00, 2.10)

# ==================== (b) Ascaris, male and female ====================
ax = axes[1]

def worm(cy, L, rad, curl=0.0):
    xx = np.linspace(-L/2, L/2, 600)
    r = rad*np.clip(1 - (np.abs(xx)/(L/2 + 0.36))**8, 0, 1)**0.30
    ys = cy + curl*np.clip((xx - L/2 + 1.45)/1.45, 0, 1)**2.2*1.10
    ax.add_patch(Polygon(np.vstack([np.c_[xx, ys + r],
                                    np.c_[xx[::-1], (ys - r)[::-1]]]),
                         closed=True, fc=WORM, ec=WEDGE, lw=1.3, zorder=3))
    return xx, ys, r

# ---- female (upper): longer, straight
xf, yf, rf = worm(0.95, 6.60, 0.34)
t = np.linspace(-2.85, 2.95, 400)
ax.plot(t, 0.95 + 0.20*np.sin(4.6*t), color="#c07d9a", lw=1.0, zorder=5)
ax.add_patch(Circle((-3.24, 0.95), 0.10, fc="#a2453e", ec=WEDGE, lw=0.8, zorder=6))
ax.add_patch(Circle((-1.05, 0.62), 0.09, fc="#2e6b4f", ec=WEDGE, lw=0.8, zorder=6))
ax.plot([3.22, 3.34], [0.88, 0.88], color="#a2453e", lw=1.5, zorder=6)

# ---- male (lower): shorter, tail hooked
xm, ym, rm = worm(-1.05, 5.60, 0.28, curl=-1.00)
ax.plot(xm + 0.0, ym + 0.17*np.sin(5.0*xm), color="#8fa8c4", lw=0.9, zorder=5)
ax.add_patch(Circle((-2.74, -1.05), 0.09, fc="#a2453e", ec=WEDGE, lw=0.8, zorder=6))
i = np.argmin(np.abs(xm - 2.45))
for dx in (0.06, -0.06):
    ax.plot([xm[i] + dx, xm[i] + dx + 0.30], [ym[i] - 0.14, ym[i] - 0.72],
            color="#6a4a78", lw=1.2, zorder=7, solid_capstyle='round')

lab(ax, "mouth with three lips", (-3.24, 1.06), -3.30, 2.10)
lab(ax, "female genital pore", (-1.05, 0.62), 0.20, 2.10)
lab(ax, "coiled gonad", (1.30, 1.08), 2.85, 2.10)
lab(ax, "anus", (3.28, 0.88), 4.50, 1.85, ha='left')
lab(ax, "thick cuticle", (0.20, -1.33), -3.30, -2.42)
lab(ax, "posterior end hooked ventrally,\nwith two penial spicules",
    (2.72, -1.86), 0.20, -2.42)
ax.text(-4.95, 2.58, "(b)  $\\it{Ascaris\\ lumbricoides}$ (Nemathelminthes): "
                     "sexes separate",
        ha='left', va='center', fontsize=6.8, color=INK)
ax.text(4.55, 0.95, "female", ha='left', va='center', fontsize=6.2, color=MUTED,
        style='italic')
ax.text(4.55, -1.05, "male", ha='left', va='center', fontsize=6.2, color=MUTED,
        style='italic')
ax.set_xlim(-5.05, 6.45); ax.set_ylim(-2.85, 2.85)

for a in axes:
    a.set_aspect('equal'); a.axis('off')
```

### 4. Phylum Nemathelminthes (Aschelminthes)

The roundworms.

- Body long, cylindrical, **unsegmented**, tapering at both ends, circular in
  section; triploblastic, bilateral, **pseudocoelomate**; **organ–system** level.
- Covered by a tough moulted **cuticle**; the body wall has **only longitudinal
  muscles**, so the worm can only thrash from side to side.
- The gut is **complete**, with mouth and anus — the first phylum with the
  tube-within-a-tube plan.
- No circulatory or respiratory organs; parasites respire anaerobically.
  Excretion by **renette cells** or by an H-shaped canal system.
- **Sexes separate**, with marked **sexual dimorphism**: the male *Ascaris* is
  shorter with a curved tail bearing penial setae, the female longer and
  straight.
- Examples: *Ascaris lumbricoides*, *Ancylostoma duodenale* (hookworm),
  *Wuchereria bancrofti* (filariasis), *Enterobius* (pinworm), *Trichinella*.

### 5. Phylum Annelida

The segmented worms — the first animals with a **true coelom**.

- Body **metamerically segmented** outside by annuli and inside by septa;
  bilateral, triploblastic.
- A true **schizocoelic coelom**, divided by septa into compartments of coelomic
  fluid that act as a **hydrostatic skeleton**.
- Locomotion by chitinous **setae** (earthworm), **parapodia** (*Nereis*) or
  suckers (leech), working against circular and longitudinal muscle layers.
- **Closed blood vascular system**; the respiratory pigment is dissolved in the
  plasma. Excretion by segmental **nephridia**; respiration through the moist
  skin or by gills.
- Nervous system: dorsal cerebral ganglia, circumpharyngeal connectives, and a
  double, ventral, solid, ganglionated nerve cord.
- Monoecious (earthworm, leech) or dioecious (*Nereis*); development direct, or
  through a **trochophore** larva in marine forms.
- Examples: *Pheretima posthuma*, *Lumbricus*, *Hirudinaria* (leech), *Nereis*
  (clam worm), *Aphrodite* (sea mouse).

### 6. Phylum Arthropoda

The largest phylum: about three of every four known animal species.

- Body segmented and divided into **head, thorax and abdomen** (or cephalothorax
  and abdomen); segmentation is **heteronomous**, different segments doing
  different jobs.
- The diagnostic character is **jointed appendages**, modified as antennae,
  mouthparts, walking legs, paddles and copulatory organs.
- A chitinous **exoskeleton** covers the body; because it cannot grow it is
  periodically shed — **moulting (ecdysis)**.
- The body cavity is a blood-filled **haemocoel** and circulation is **open**,
  the dorsal heart pumping haemolymph into sinuses; the true coelom survives
  only in the gonads and excretory organs.
- Respiration by gills, **book gills** (*Limulus*), **book lungs** (scorpion) or
  **tracheae** with spiracles (insects); excretion by **Malpighian tubules**
  (insects), green glands (prawn) or coxal glands (scorpion).
- **Compound eyes** of many ommatidia, plus ocelli, antennae and statocysts.
  Usually dioecious, fertilisation internal, development often with
  metamorphosis.
- Examples: *Periplaneta americana* (cockroach), *Apis indica* (honey bee),
  *Bombyx mori* (silkworm), *Palaemon* (prawn), *Palamnaeus* (scorpion),
  *Limulus*, *Scolopendra*, *Julus*.

```figure caption="(a) *Periplaneta*, (b) *Pila*, (c) *Asterias*."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Ellipse
fig, axes = plt.subplots(1, 3, figsize=(5.2, 3.0))
BODY = "#e6cfa8"; EDGE = "#7a5c3a"; SHELL = "#e8d3b0"; SEA = "#e4c9a0"

def lab(ax, txt, tip, tx, ty, ha='left', fs=5.7):
    ax.annotate(txt, xy=tip, xytext=(tx, ty), fontsize=fs, color=INK, ha=ha,
                va='center', zorder=14,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7,
                                shrinkA=1.2, shrinkB=1.0))

# ================= (a) Cockroach, dorsal view =================
ax = axes[0]
yk = [1.32, 1.12, 0.95, 0.55, 0.10, -0.60, -1.25, -1.55]
wk = [0.16, 0.30, 0.42, 0.50, 0.48, 0.42, 0.26, 0.10]
y = np.linspace(yk[-1], yk[0], 260); w = np.interp(y, yk[::-1], wk[::-1])
ax.add_patch(Polygon(np.vstack([np.c_[w, y], np.c_[-w[::-1], y[::-1]]]),
                     closed=True, fc=BODY, ec=EDGE, lw=1.2, zorder=3))
for yy in (-0.10, -0.40, -0.70, -1.00, -1.25):
    ww = np.interp(yy, yk[::-1], wk[::-1])
    ax.plot([-ww, ww], [yy, yy], color=EDGE, lw=0.6, zorder=4)
ax.add_patch(Ellipse((0, 0.80), 0.86, 0.52, fc="#d8bd91", ec=EDGE, lw=1.1, zorder=5))
ax.add_patch(Ellipse((0, 1.20), 0.38, 0.32, fc="#d8bd91", ec=EDGE, lw=1.1, zorder=5))
for s in (1, -1):
    ax.add_patch(Circle((s*0.12, 1.26), 0.05, fc=INK, ec='none', zorder=6))
    t = np.linspace(0, 1, 40)
    ax.plot(s*(0.10 + 0.55*t + 0.20*t**2), 1.32 + 1.10*t - 0.30*t**2,
            color=EDGE, lw=0.9, zorder=2)
    for yl, ln, dn in [(0.86, 0.46, 0.30), (0.62, 0.52, 0.42), (0.34, 0.58, 0.58)]:
        x0 = np.interp(yl, yk[::-1], wk[::-1])
        ax.plot([s*x0, s*(x0 + ln), s*(x0 + ln - 0.10)],
                [yl, yl - dn*0.35, yl - dn], color=EDGE, lw=1.0, zorder=2,
                solid_capstyle='round')
    ax.add_patch(Ellipse((s*0.22, -0.45), 0.34, 1.75, angle=s*5, fc='none',
                         ec=EDGE, lw=0.8, ls=(0, (3, 2)), zorder=6))
    ax.plot([s*0.08, s*0.26], [-1.55, -1.92], color=EDGE, lw=1.0, zorder=3,
            solid_capstyle='round')
lab(ax, "antenna", (0.55, 2.02), 1.00, 2.40)
lab(ax, "compound\neye", (0.14, 1.26), 0.72, 1.52)
lab(ax, "head", (-0.16, 1.22), -0.62, 1.78, ha='right')
lab(ax, "thorax", (-0.40, 0.80), -0.90, 1.10, ha='right')
lab(ax, "jointed\nlegs", (0.90, 0.30), 1.05, 0.72)
lab(ax, "wings", (0.38, -0.85), 0.92, -0.55)
lab(ax, "segmented\nabdomen", (-0.34, -0.70), -0.80, -1.10, ha='right')
lab(ax, "anal cercus", (0.24, -1.85), 0.60, -2.20)
ax.text(0, 3.05, "(a)  Cockroach", ha='center', fontsize=7.2, color=INK)
ax.text(0, 2.75, "Arthropoda", ha='center', fontsize=6.4, color=MUTED, style='italic')

# ================= (b) Pila, a gastropod mollusc =================
ax = axes[1]
th = np.linspace(0, 4.6*np.pi, 400)
r = 0.085*np.exp(0.205*th)
sx, sy = 0.30 + r*np.cos(th + 1.2), 0.70 + r*np.sin(th + 1.2)
for i in range(len(th) - 1):
    ax.plot(sx[i:i+2], sy[i:i+2], color=EDGE, lw=0.6 + 9.5*r[i]/r[-1], zorder=4,
            solid_capstyle='round')
for i in range(len(th) - 1):
    ax.plot(sx[i:i+2], sy[i:i+2], color=SHELL, lw=max(0.2, 8.0*r[i]/r[-1]), zorder=5,
            solid_capstyle='round')
foot = np.array([[-1.05, -0.20], [-1.30, -0.95], [-0.70, -1.45], [0.45, -1.42],
                 [1.00, -1.05], [0.90, -0.45], [0.10, -0.30]])
ax.add_patch(Polygon(foot, closed=True, fc=BODY, ec=EDGE, lw=1.2, zorder=3))
ax.add_patch(Ellipse((0.62, -0.92), 0.52, 0.40, angle=-15, fc="#c9ad80", ec=EDGE,
                     lw=1.0, zorder=6))
for s, yy in [(1, -0.30), (1, -0.55)]:
    pass
for dx, dy in [(-0.28, 0.42), (-0.52, 0.22)]:
    ax.plot([-1.05 + 0.0, -1.05 + dx*1.6], [-0.45, -0.45 + dy*1.6], color=EDGE,
            lw=1.1, zorder=4, solid_capstyle='round')
ax.add_patch(Circle((-1.12, -0.52), 0.075, fc=INK, ec='none', zorder=7))
lab(ax, "spirally\ncoiled shell", (0.95, 1.30), 1.05, 2.30)
lab(ax, "apex", (0.30, 0.70), 0.80, 0.50)
lab(ax, "tentacles", (-1.66, 0.12), -1.30, 1.15, ha='right')
lab(ax, "eye", (-1.12, -0.52), -1.60, -0.35, ha='right')
lab(ax, "muscular\nfoot", (-0.40, -1.20), -0.70, -1.85, ha='right')
lab(ax, "operculum", (0.70, -0.98), 1.00, -1.62)
ax.text(0, 3.05, "(b)  $Pila$", ha='center', fontsize=7.2, color=INK)
ax.text(0, 2.75, "Mollusca", ha='center', fontsize=6.4, color=MUTED, style='italic')

# ================= (c) Starfish, aboral view =================
ax = axes[2]
t = np.linspace(0, 2*np.pi, 800)
rr = 0.52 + 1.05*(0.5 + 0.5*np.cos(5*t))**1.8
ax.add_patch(Polygon(np.c_[rr*np.cos(t), rr*np.sin(t)], closed=True, fc=SEA,
                     ec=EDGE, lw=1.2, zorder=3))
ax.add_patch(Circle((0, 0), 0.52, fc='none', ec=EDGE, lw=0.8, ls=(0, (3, 2)),
                    zorder=4))
rng = np.random.default_rng(3)
for k in range(5):
    a = k*2*np.pi/5
    for f in np.linspace(0.30, 0.90, 7):
        rad = np.interp(a, t, rr)*f
        for off in (-0.13, 0.0, 0.13):
            ax.add_patch(Circle((rad*np.cos(a + off*(1 - f)),
                                 rad*np.sin(a + off*(1 - f))), 0.045,
                                fc="#b08a55", ec='none', zorder=5))
mad = 0.36*np.array([np.cos(np.pi/5 + 0.15), np.sin(np.pi/5 + 0.15)])
ax.add_patch(Circle(mad, 0.13, fc="#cf9b6a", ec=EDGE, lw=0.9, zorder=6))
ax.add_patch(Circle((0, 0), 0.10, fc=INK, ec='none', zorder=6))
lab(ax, "arm (ray)", (1.15, 0.30), 1.30, 1.15)
lab(ax, "central\ndisc", (-0.32, -0.26), -0.90, -1.15, ha='right')
lab(ax, "madre-\nporite", (mad[0] + 0.10, mad[1] + 0.08), 0.90, 1.80)
lab(ax, "spines", (0.72, -0.64), 1.15, -1.30)
ax.text(0, 3.05, "(c)  Starfish", ha='center', fontsize=7.2, color=INK)
ax.text(0, 2.75, "Echinodermata", ha='center', fontsize=6.4, color=MUTED,
        style='italic')

for ax in axes:
    ax.set_xlim(-2.15, 2.15); ax.set_ylim(-2.65, 3.25)
    ax.set_aspect('equal'); ax.axis('off')
fig.subplots_adjust(wspace=0.02)
```

### 7. Phylum Mollusca

The second largest phylum — snails, mussels, squids and their relatives.

- Body soft and **unsegmented**, with a **head**, a muscular ventral **foot**
  for creeping, burrowing or swimming, and a dorsal **visceral mass**.
- The visceral mass is covered by the **mantle**, a fleshy fold that secretes the
  calcareous **shell** and encloses the **mantle cavity** holding the gills.
- Most have a rasping **radula** armed with rows of chitinous teeth; it is
  absent in the filter-feeding bivalves.
- Respiration by feather-like **ctenidia**, or by a pulmonary sac in land
  snails. Circulation **open** except in cephalopods; the pigment is usually
  **haemocyanin**, blue when oxygenated.
- Excretion by metanephridia, the **organ of Bojanus**.
- Usually dioecious, with **trochophore** and **veliger** larvae. Cephalopods
  have the best nervous system and eyes of any invertebrate.
- Examples: *Pila globosa* (apple snail), *Lamellidens* (fresh-water mussel),
  *Sepia* (cuttlefish), *Loligo* (squid), *Octopus*, *Pinctada* (pearl
  oyster).

### 8. Phylum Echinodermata

- **Exclusively marine** and mostly bottom-dwelling; the name means
  "spiny-skinned".
- Adults show **pentamerous radial symmetry**, but the larva (bipinnaria,
  echinopluteus) is **bilaterally symmetrical** — which is why echinoderms are
  grouped with the bilateral deuterostomes, not with the coelenterates.
- Triploblastic and coelomate, the coelom formed by **enterocoely** and the
  blastopore becoming the anus.
- The endoskeleton is of calcareous **ossicles**, usually spiny.
- The unique character is the **water vascular (ambulacral) system**: sea water
  enters the sieve-like **madreporite**, runs down the stone canal to a ring
  canal and out along five radial canals to hundreds of **tube feet**, each
  worked hydraulically by an ampulla and used for locomotion, gripping prey and
  gas exchange.
- **No excretory organs**; the nervous system is a nerve ring with radial nerves
  and no brain. Sexes usually separate, fertilisation external; **regeneration
  and autotomy** are famous — one arm with part of the disc can rebuild a
  starfish.
- Examples: *Asterias* (starfish), *Echinus* (sea urchin), *Holothuria* (sea
  cucumber), *Antedon* (feather star), *Ophiura* (brittle star).

### 9. Phylum Chordata

```figure caption="A generalised chordate and the three subphyla."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Ellipse, Rectangle, FancyBboxPatch

BODY = "#f2e6d2"; EDGE = "#8a5a33"
NERVE = "#cfe0ee"; NEDGE = "#2c5f96"
NOTO = "#f2e3c4"; NOEDGE = "#9a7330"
GUTC = "#e8d3b4"; RED = "#a2453e"

fig = plt.figure(figsize=(5.2, 4.55))
gs = fig.add_gridspec(2, 3, height_ratios=[5.05, 3.55], hspace=0.10,
                      wspace=0.04)
axT = fig.add_subplot(gs[0, :])

# ============ (a) generalised chordate ============
ax = axT
xk = [-5.20, -4.90, -4.40, -3.60, -2.40, -1.00, 0.60, 2.00, 3.20, 4.10, 4.70]
wk = [0.06,  0.52,  0.80,  0.96,  1.04,  1.04, 0.94, 0.76, 0.54, 0.36, 0.26]
xb = np.linspace(xk[0], xk[-1], 500)
wb = np.interp(xb, xk, wk)
ax.add_patch(Polygon(np.vstack([np.c_[xb, wb], np.c_[xb[::-1], -wb[::-1]]]),
                     closed=True, fc=BODY, ec=EDGE, lw=1.2, zorder=2))
# caudal fin
ax.add_patch(Polygon([(4.62, 0.24), (5.55, 0.86), (5.20, 0.0),
                      (5.55, -0.86), (4.62, -0.24)],
                     closed=True, fc=BODY, ec=EDGE, lw=1.0, zorder=1))

# dorsal hollow nerve cord
xn = np.linspace(-4.75, 4.48, 300)
ax.fill_between(xn, 0.40, 0.62, color=NERVE, ec=NEDGE, lw=0.9, zorder=5)
ax.fill_between(xn, 0.475, 0.545, color="white", ec="none", zorder=6)
# anterior swelling (brain)
ax.add_patch(Ellipse((-4.60, 0.48), 0.60, 0.40, fc=NERVE, ec=NEDGE, lw=0.9,
                     zorder=7))

# notochord
ax.fill_between(np.linspace(-4.60, 4.48, 300), 0.06, 0.30, color=NOTO,
                ec=NOEDGE, lw=0.9, zorder=5)
for xx in np.arange(-4.40, 4.44, 0.26):
    ax.plot([xx, xx], [0.08, 0.28], color=NOEDGE, lw=0.4, alpha=0.55, zorder=6)

# pharynx with gill slits
ax.add_patch(Polygon([(-4.55, -0.10), (-1.95, -0.10), (-1.95, -0.86),
                      (-4.55, -0.86)], closed=True, fc=GUTC, ec=EDGE,
                     lw=1.0, zorder=5))
for xx in (-4.24, -3.86, -3.48, -3.10, -2.72, -2.34):
    ax.plot([xx, xx - 0.14], [-0.12, -0.84], color=RED, lw=1.7, zorder=7,
            solid_capstyle='round')
# gut and anus
ax.fill_between(np.linspace(-1.95, 2.35, 200), -0.62, -0.34, color=GUTC,
                ec=EDGE, lw=1.0, zorder=5)
ax.plot([2.35, 2.35], [-0.62, -0.90], color=EDGE, lw=1.0, zorder=5)
ax.add_patch(Circle((2.35, -0.93), 0.09, fc=RED, ec=EDGE, lw=0.7, zorder=8))
# mouth
ax.add_patch(Circle((-5.02, -0.18), 0.11, fc=RED, ec=EDGE, lw=0.7, zorder=8))
# ventral heart
ax.add_patch(Ellipse((-2.05, -1.02), 0.46, 0.30, fc="#e6b9b4", ec=RED,
                     lw=0.9, zorder=8))
# myotomes (segmented muscle blocks) behind the anus
for xx in np.arange(2.60, 4.55, 0.32):
    ww = np.interp(xx, xb, wb)
    ax.plot([xx, xx - 0.14], [ww - 0.03, -ww + 0.03], color=MUTED, lw=0.5,
            zorder=3)

# post-anal tail bracket
ax.annotate("", xy=(2.35, -1.62), xytext=(5.45, -1.62),
            arrowprops=dict(arrowstyle='<->', color=MUTED, lw=0.9))
ax.text(3.90, -1.80, "post-anal tail", fontsize=6.2, color=INK, ha='center',
        va='top')

def lab(txt, tip, tx, ty, ha='center', fs=6.2):
    ax.annotate(txt, xy=tip, xytext=(tx, ty), fontsize=fs, color=INK, ha=ha,
                va='center', zorder=15,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.75,
                                shrinkA=2.0, shrinkB=1.0))

lab("dorsal, hollow, tubular nerve cord", (-0.60, 0.51), -1.30, 1.95)
lab("notochord (elastic rod\nbelow the nerve cord)", (2.60, 0.18), 3.55, 1.90)
lab("brain", (-4.60, 0.62), -4.90, 1.42, ha='right')
lab("mouth", (-5.06, -0.18), -5.55, -0.95, ha='right')
lab("pharynx with paired\ngill slits", (-3.30, -0.50), -3.70, -1.85)
lab("ventral heart", (-2.05, -1.10), -1.20, -2.30)
lab("gut", (0.60, -0.48), 0.60, -1.30)
lab("anus", (2.35, -0.96), 1.55, -2.30)

ax.text(-5.85, 2.52, "(a)  the four fundamental chordate characters",
        fontsize=7.0, color=INK, va='top', ha='left')
ax.set_xlim(-5.95, 6.45); ax.set_ylim(-2.62, 2.62)
ax.set_aspect('equal'); ax.axis('off')

# ============ (b) the three subphyla ============
XL, XR, YB, YT = -2.70, 2.70, -3.15, 2.05

def panel(k):
    a = fig.add_subplot(gs[1, k])
    a.set_xlim(XL, XR); a.set_ylim(YB, YT)
    a.set_aspect('equal'); a.axis('off')
    return a

def caption(a, title, sub):
    a.text(0, -1.95, title, ha='center', va='top', fontsize=6.6, color=INK)
    a.text(0, -2.38, sub, ha='center', va='top', fontsize=5.7, color=MUTED,
           linespacing=1.3)

# --- Urochordata: an ascidian ---
a1 = panel(0)
S, DX, DY = 0.78, -0.62, -0.05
def T(p):
    return (p[0] * S + DX, p[1] * S + DY)
sac = [(-0.95, -1.30), (-1.15, -0.30), (-1.05, 0.55), (-0.70, 1.00),
       (-0.55, 1.35), (-0.20, 1.40), (-0.05, 1.00), (0.35, 1.25),
       (0.72, 1.18), (0.72, 0.72), (1.05, 0.30), (1.10, -0.55),
       (0.90, -1.30)]
a1.add_patch(Polygon([T(q) for q in sac], closed=True, fc=BODY, ec=EDGE,
                     lw=1.1, zorder=3))
a1.add_patch(Polygon([T(q) for q in [(-0.55, 1.35), (-0.20, 1.40),
                                     (-0.05, 1.00), (-0.52, 0.96)]],
                     closed=True, fc="#e6d2b0", ec=EDGE, lw=0.8, zorder=4))
a1.add_patch(Polygon([T(q) for q in [(0.35, 1.25), (0.72, 1.18),
                                     (0.72, 0.72), (0.36, 0.80)]],
                     closed=True, fc="#e6d2b0", ec=EDGE, lw=0.8, zorder=4))
# branchial basket with slits
a1.add_patch(Ellipse(T((-0.05, 0.10)), 1.35 * S, 1.25 * S, fc=GUTC, ec=EDGE,
                     lw=0.8, zorder=4))
for yy in (0.48, 0.24, 0.00, -0.24, -0.48):
    hw = 0.62 * np.sqrt(max(1 - (yy / 0.64) ** 2, 0.02))
    a1.plot([T((-0.05 - hw, yy))[0], T((-0.05 + hw, yy))[0]],
            [T((0, yy))[1]] * 2, color=RED, lw=0.9, zorder=5)
a1.plot([T((-1.45, 0))[0], T((1.40, 0))[0]], [T((0, -1.30))[1]] * 2,
        color=MUTED, lw=1.4, zorder=2)
a1.annotate("inhalant siphon", xy=T((-0.37, 1.34)), xytext=(-2.60, 1.72),
            fontsize=5.6, color=INK, ha='left', va='center',
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7))
a1.annotate("exhalant\nsiphon", xy=T((0.54, 1.20)), xytext=(1.55, 1.55),
            fontsize=5.6, color=INK, ha='center', va='center',
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7))
a1.annotate("pharynx with\ngill slits", xy=T((0.42, -0.30)), xytext=(1.55, -0.75),
            fontsize=5.6, color=INK, ha='center', va='center',
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7))
caption(a1, "Urochordata  ($\\it{Herdmania}$)",
        "notochord only in the\nlarval tail; adult sessile")

# --- Cephalochordata: Amphioxus ---
a2 = panel(1)
xk2 = [-2.15, -1.90, -1.30, -0.40, 0.60, 1.40, 1.95, 2.20]
wk2 = [0.03, 0.22, 0.34, 0.38, 0.35, 0.26, 0.14, 0.02]
x2 = np.linspace(xk2[0], xk2[-1], 300)
w2 = np.interp(x2, xk2, wk2)
a2.add_patch(Polygon(np.vstack([np.c_[x2, w2], np.c_[x2[::-1], -w2[::-1]]]),
                     closed=True, fc=BODY, ec=EDGE, lw=1.1, zorder=3))
a2.fill_between(np.linspace(-1.95, 2.10, 200), 0.03, 0.15, color=NOTO,
                ec=NOEDGE, lw=0.7, zorder=5)
a2.fill_between(np.linspace(-1.95, 2.10, 200), 0.17, 0.27, color=NERVE,
                ec=NEDGE, lw=0.7, zorder=5)
for xx in (-1.60, -1.35, -1.10, -0.85, -0.60, -0.35):
    a2.plot([xx, xx - 0.07], [-0.04, -0.28], color=RED, lw=0.9, zorder=6)
for xx in np.arange(-1.70, 2.00, 0.24):
    ww = np.interp(xx, x2, w2)
    a2.plot([xx, xx - 0.10], [ww - 0.02, -ww + 0.02], color=MUTED, lw=0.4,
            zorder=4)
a2.annotate("notochord runs the\nwhole body length",
            xy=(1.10, 0.09), xytext=(0.20, 1.55), fontsize=5.6, color=INK,
            ha='center', va='center',
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7))
a2.annotate("gill slits", xy=(-1.05, -0.22), xytext=(-1.75, -1.25),
            fontsize=5.6, color=INK, ha='center', va='center',
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7))
caption(a2, "Cephalochordata  ($\\it{Amphioxus}$)",
        "notochord persists head to\ntail throughout life")

# --- Vertebrata: a fish ---
a3 = panel(2)
xk3 = [-2.10, -1.85, -1.30, -0.40, 0.70, 1.45, 1.80]
wk3 = [0.10, 0.42, 0.62, 0.66, 0.46, 0.26, 0.16]
x3 = np.linspace(xk3[0], xk3[-1], 300)
w3 = np.interp(x3, xk3, wk3)
a3.add_patch(Polygon(np.vstack([np.c_[x3, w3], np.c_[x3[::-1], -w3[::-1]]]),
                     closed=True, fc=BODY, ec=EDGE, lw=1.1, zorder=3))
a3.add_patch(Polygon([(1.74, 0.14), (2.35, 0.62), (2.10, 0.0),
                      (2.35, -0.62), (1.74, -0.14)], closed=True, fc=BODY,
                     ec=EDGE, lw=0.9, zorder=2))
a3.add_patch(Polygon([(-0.55, 0.64), (0.25, 1.05), (0.45, 0.56)], closed=True,
                     fc=BODY, ec=EDGE, lw=0.8, zorder=2))
# vertebral column: a chain of blocks
for xx in np.arange(-1.62, 1.70, 0.27):
    a3.add_patch(FancyBboxPatch((xx - 0.10, 0.03), 0.20, 0.20,
                                boxstyle="round,pad=0.008,rounding_size=0.04",
                                fc=NOTO, ec=NOEDGE, lw=0.7, zorder=5))
a3.fill_between(np.linspace(-1.72, 1.80, 200), 0.26, 0.36, color=NERVE,
                ec=NEDGE, lw=0.7, zorder=5)
a3.add_patch(Ellipse((-1.72, 0.30), 0.52, 0.34, fc=NERVE, ec=NEDGE, lw=0.8,
                     zorder=6))
a3.plot([-1.55, -1.55], [-0.10, -0.52], color=RED, lw=1.1, zorder=6)
a3.annotate("brain in a\ncranium", xy=(-1.78, 0.44), xytext=(-1.55, 1.55),
            fontsize=5.6, color=INK, ha='center', va='center',
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7))
a3.annotate("vertebral column",
            xy=(0.70, 0.13), xytext=(0.55, -1.35), fontsize=5.6, color=INK,
            ha='center', va='center',
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7))
caption(a3, "Vertebrata  ($\\it{Labeo}$)",
        "notochord replaced by a\nbony or cartilaginous spine")

fig.text(0.012, 0.415, "(b)  the three subphyla of Chordata", fontsize=7.0,
         color=INK, ha='left', va='center')
```

Four characters define a chordate; all four need be present only at *some*
stage of the life cycle.

1. A **notochord** — a flexible rod of vacuolated cells in a fibrous sheath,
   below the nerve cord and above the gut; the first skeleton, and the
   stiffening the swimming muscles work against.
2. A **dorsal, hollow (tubular) nerve cord**, single and without ganglia — the
   exact opposite of the ventral, solid, double, ganglionated cord of annelids
   and arthropods. Its front end enlarges into the brain.
3. **Pharyngeal gill slits**, paired openings from pharynx to exterior, used for
   filter feeding in protochordates and respiration in fishes; in land
   vertebrates they appear only in the embryo.
4. A **post-anal tail**, a muscular extension behind the anus.

A chordate also has a **ventral heart**, closed circulation, an enterocoelic
coelom and bilateral symmetry at the organ–system grade.

| Subphylum | Notochord | Features | Examples |
|---|---|---|---|
| Urochordata | in the larval tail only, lost at metamorphosis | marine, sessile adult with a tunic; retrogressive metamorphosis | *Herdmania*, *Ascidia*, *Salpa* |
| Cephalochordata | head to tail, throughout life | marine, fish-like burrowing filter feeders; no head, no heart | *Branchiostoma* (amphioxus) |
| Vertebrata | replaced in the adult by a **vertebral column** | cranium enclosing the brain; paired appendages; chambered heart; kidneys | fishes, amphibians, reptiles, birds, mammals |

Vertebrata divides into Agnatha (jawless) and Gnathostomata (jawed).

| Class | Diagnostic features | Heart | Examples |
|---|---|---|---|
| Cyclostomata | no jaws, scales or paired fins; cartilaginous | two-chambered | *Petromyzon*, *Myxine* |
| Chondrichthyes | cartilaginous; placoid scales; no operculum | two-chambered | *Scoliodon*, *Torpedo* |
| Osteichthyes | bony; cycloid scales; operculum; air bladder | two-chambered | *Labeo*, *Hippocampus* |
| Amphibia | moist scaleless skin; gills then lungs | three-chambered | *Rana*, *Bufo* |
| Reptilia | dry skin with scales; shelled amniotic egg | three-chambered | *Calotes*, *Naja* |
| Aves | feathers; pneumatic bones; air sacs; warm-blooded | four-chambered | *Columba*, *Pavo* |
| Mammalia | hair; **mammary glands**; **diaphragm**; warm-blooded | four-chambered | *Homo*, *Panthera* |

Finally, the nine phyla side by side. "Distinguish between" questions are
answered from exactly these columns.

| Phylum | Symmetry | Germ layers | Coelom | Digestive tract | Circulation | Excretion | Example |
|---|---|---|---|---|---|---|---|
| Porifera | asymmetrical / radial | diploblastic | absent | absent (canal system) | absent | diffusion | *Sycon* |
| Coelenterata | radial | diploblastic | absent | blind sac | absent | diffusion | *Hydra* |
| Platyhelminthes | bilateral | triploblastic | acoelomate | incomplete or absent | absent | flame cells | *Taenia* |
| Nemathelminthes | bilateral | triploblastic | pseudocoelomate | complete | absent | renette cells | *Ascaris* |
| Annelida | bilateral | triploblastic | true (schizocoelic) | complete | closed | nephridia | *Pheretima* |
| Arthropoda | bilateral | triploblastic | haemocoel | complete | open | Malpighian tubules | *Periplaneta* |
| Mollusca | bilateral (often asymmetrical) | triploblastic | reduced true coelom | complete | open | organ of Bojanus | *Pila* |
| Echinodermata | radial adult, bilateral larva | triploblastic | true (enterocoelic) | complete | water vascular system | none | *Asterias* |
| Chordata | bilateral | triploblastic | true (enterocoelic) | complete | closed, ventral heart | kidneys | *Rana* |

## 8.3 Earthworm (*Pheretima posthuma*)

Darwin, who spent his last years studying earthworms, doubted "whether there
are many other animals which have played so important a part in the history of
the world". *Pheretima posthuma* is the common earthworm of the Nepalese plains
and the standard annelid type study.

### Habit and habitat

*Pheretima* lives in damp, humus-rich soil. It is **nocturnal**, **fossorial**
(it burrows by eating its way through the soil) and **detritivorous**, coming up
at night to feed on fallen leaves and deposit its castings. Heavy monsoon rain
floods the burrows and drives it out, because cutaneous respiration fails under
water; in the dry season it burrows deep and **aestivates**.

### External features

```figure caption="External features of *Pheretima posthuma*."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Ellipse
fig, ax = plt.subplots(figsize=(5.2, 2.9))
BODY = "#e8c9a6"; EDGE = "#8a5a33"; CLIT = "#c98f62"

# ---- body outline: long, tapering at both ends, slight swelling at clitellum
x = np.linspace(-4.55, 4.55, 700)
w = 0.40*np.clip(1 - (np.abs(x)/4.80)**5, 0, 1)**0.55
w = w*(1 + 0.16*np.exp(-((x + 1.55)/0.62)**2))
top, bot = w, -w
ax.add_patch(Polygon(np.vstack([np.c_[x, top], np.c_[x[::-1], bot[::-1]]]),
                     closed=True, fc=BODY, ec=EDGE, lw=1.25, zorder=3))

# ---- metameric segment grooves
for xs in np.arange(-4.30, 4.40, 0.185):
    ww = np.interp(xs, x, w)
    if ww < 0.05:
        continue
    yy = np.linspace(-ww, ww, 30)
    ax.plot(xs + 0.055*np.cos(0.5*np.pi*yy/ww), yy, color=EDGE, lw=0.45,
            zorder=4, alpha=0.75)

# ---- clitellum band (segments 14-16)
cl0, cl1 = -2.10, -1.00
m = (x >= cl0) & (x <= cl1)
ax.add_patch(Polygon(np.vstack([np.c_[x[m], top[m]], np.c_[x[m][::-1], bot[m][::-1]]]),
                     closed=True, fc=CLIT, ec=EDGE, lw=1.1, zorder=5))

# ---- prostomium and mouth (anterior, left)
ax.add_patch(Polygon([[-4.55, 0.06], [-4.95, 0.13], [-4.88, -0.05], [-4.55, -0.09]],
                     closed=True, fc=CLIT, ec=EDGE, lw=1.0, zorder=4))
ax.plot([-4.60, -4.42], [-0.10, -0.12], color="#a2453e", lw=1.6, zorder=6)
# ---- anus (posterior, right)
ax.plot([4.50, 4.58], [0.04, -0.04], color="#a2453e", lw=1.8, zorder=6)

# ---- setae: a complete ring in every segment (perichaetine arrangement)
for xs in np.arange(-4.05, 4.30, 0.185):
    ww = np.interp(xs, x, w)
    if ww < 0.09 or (cl0 - 0.05 < xs < cl1 + 0.05):
        continue
    for off in (0.16, 0.36, 0.56, 0.76, 0.94):
        for sg in (1, -1):
            ax.plot([xs, xs - 0.045], [sg*ww*off, sg*(ww*off + 0.15)],
                    color="#6a4522", lw=0.45, zorder=2, solid_capstyle='round')

# ---- external apertures
def pore(xx, yy, r=0.055, fc="#a2453e"):
    ax.add_patch(Circle((xx, yy), r, fc=fc, ec=EDGE, lw=0.6, zorder=7))

for xx in (-3.55, -3.37, -3.18, -2.99):          # spermathecal pores 5/6 - 8/9
    pore(xx, -0.22, 0.045, "#7c5fa0")
pore(-1.55, -0.30, 0.055, "#2e6b4f")             # female pore, segment 14
for s in (-1, 1):
    pore(-0.62, s*0.0 - 0.26 if s < 0 else -0.26, 0.0)  # placeholder (no draw)
for xx in (-0.72, -0.52):                        # male pores, segment 18
    pore(xx, -0.28, 0.055, "#1d6fb8")
for xs in np.arange(-3.9, 4.2, 0.37):            # nephridiopores
    ww = np.interp(xs, x, w)
    if ww < 0.10 or (cl0 - 0.05 < xs < cl1 + 0.05):
        continue
    ax.add_patch(Circle((xs, -ww*0.88), 0.022, fc=MUTED, ec='none', zorder=6))
for xs in np.arange(-2.6, 4.2, 0.55):            # mid-dorsal pores
    ww = np.interp(xs, x, w)
    ax.add_patch(Circle((xs, ww - 0.035), 0.022, fc=MUTED, ec='none', zorder=6))

# ---- labels
def lab(txt, tip, tx, ty, ha='center', fs=6.2):
    ax.annotate(txt, xy=tip, xytext=(tx, ty), fontsize=fs, color=INK, ha=ha,
                va='center', zorder=14,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.75,
                                shrinkA=1.5, shrinkB=1.0))

lab("prostomium", (-4.86, 0.10), -4.55, 1.68)
lab("peristomium (segment 1)", (-4.40, -0.12), -2.35, 1.14)
lab("clitellum (segments 14-16)", (-1.55, 0.44), -1.00, 1.68)
lab("dorsal pores", (1.15, 0.40), 1.30, 1.14)
lab("anus on last segment", (4.54, 0.00), 3.92, 1.68)
lab("spermathecal pores (4 pairs)", (-3.28, -0.24), -3.60, -1.24)
lab("female pore (segment 14)", (-1.55, -0.32), -2.20, -1.80)
lab("male pores (segment 18)", (-0.62, -0.30), 0.55, -1.24)
lab("setae: a complete ring of 80-120\nin every segment", (2.35, -0.52), 3.05, -1.86)
lab("nephridiopore", (3.98, -0.26), 4.35, -1.24)
ax.annotate('', xy=(-4.92, 0.74), xytext=(4.92, 0.74),
            arrowprops=dict(arrowstyle='<->', color="#2e6b4f", lw=0.8,
                            mutation_scale=8), zorder=8)
ax.text(-4.55, 0.93, "anterior", ha='center', fontsize=6.0, color="#2e6b4f")
ax.text(4.40, 0.93, "posterior", ha='center', fontsize=6.0, color="#2e6b4f")

ax.set_xlim(-5.70, 5.70); ax.set_ylim(-2.25, 2.05)
ax.set_aspect('equal'); ax.axis('off')
```

The body is long, narrow and cylindrical, about 150 mm long and 3–5 mm wide,
dark brown above from the pigment **porphyrin** and paler below. It is divided
into 100–140 ring-like **segments** (metameres) numbered from the front, with a
fine dark mid-dorsal line marking the dorsal blood vessel beneath the skin.

A small fleshy lobe, the **prostomium**, overhangs the mouth; it is not a
segment, and works as a sensory probe and a wedge for pushing soil apart. The
**peristomium** is segment 1 and bears the crescentic **mouth**; the last
segment carries the **anus**. Segments 14–16 are swollen into a glandular
reddish girdle, the **clitellum**, which secretes the mucus binding worms during
copulation and the albumen and **cocoon** in which the eggs develop.

**Setae** are small S-shaped chitinous bristles sunk in pits and moved by
protractor and retractor muscles. In *Pheretima* they are **perichaetine** — a
complete ring of 80 to 120 in every segment — and are absent only from the
first segment, the last segment and the clitellum. (*Lumbricus* has only eight
per segment in four pairs: the **lumbricine** arrangement.) The setae grip the
soil so that the muscles have something to pull against.

| Aperture | Number | Position |
|---|---|---|
| Mouth | 1 | anterior, on the peristomium (segment 1) |
| Anus | 1 | terminal, on the last segment |
| Female genital pore | 1 | mid-ventral, on segment 14 |
| Male genital pores | 1 pair | ventro-lateral, on segment 18 |
| Spermathecal pores | 4 pairs | ventro-lateral, in grooves 5/6, 6/7, 7/8 and 8/9 |
| Nephridiopores | very many | scattered over all segments except the first two |
| Dorsal pores | 1 per segment | mid-dorsal, from groove 12/13 backwards; they release coelomic fluid that keeps the skin moist |

### Body wall, coelom and locomotion

```figure caption="T.S. of *Pheretima posthuma*, intestinal region."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Wedge, Ellipse
fig, ax = plt.subplots(figsize=(4.6, 4.3))
EDGE = "#8a5a33"

# ---------- concentric layers of the body wall ----------
layers = [(2.00, "#efe3d2", "cuticle"),
          (1.945, "#e6cfae", "epidermis"),
          (1.855, "#d9b184", "circular muscle"),
          (1.690, "#c08a5a", "longitudinal muscle"),
          (1.505, "#f7f1e6", "parietal peritoneum")]
for r, c, _ in layers:
    ax.add_patch(Circle((0, 0), r, fc=c, ec=EDGE, lw=0.9, zorder=2))
ax.add_patch(Circle((0, 0), 1.478, fc="#fdfbf7", ec=EDGE, lw=0.8, zorder=3))
# fibre hatching in the longitudinal muscle layer
for a in np.arange(0, 2*np.pi, np.pi/34):
    ax.plot([1.520*np.cos(a), 1.680*np.cos(a)], [1.520*np.sin(a), 1.680*np.sin(a)],
            color="#8a5a33", lw=0.35, zorder=4, alpha=0.7)

# ---------- gut (intestine) ----------
ax.add_patch(Circle((0, -0.06), 0.95, fc="#b7c9a8", ec=EDGE, lw=0.9, zorder=5))
ax.add_patch(Circle((0, -0.06), 0.885, fc="#e2c49c", ec=EDGE, lw=0.8, zorder=6))
ax.add_patch(Circle((0, -0.06), 0.800, fc="#f6ecd9", ec=EDGE, lw=0.8, zorder=7))
# typhlosole: median dorsal infold of the intestinal wall
ty = np.array([[-0.20, 0.72], [-0.13, 0.20], [-0.05, 0.02], [0.0, -0.06],
               [0.05, 0.02], [0.13, 0.20], [0.20, 0.72]])
ax.add_patch(Polygon(ty, closed=True, fc="#e2c49c", ec=EDGE, lw=0.8, zorder=8))
# villi-like folds of the intestinal epithelium
for a in np.linspace(0, 2*np.pi, 44, endpoint=False):
    if abs(np.sin(a)) < 0.35 and np.cos(a) > 0:
        pass
    x0, y0 = 0.800*np.cos(a), -0.06 + 0.800*np.sin(a)
    if y0 > 0.30 and abs(x0) < 0.22:
        continue
    ax.plot([x0, 0.720*np.cos(a)], [y0, -0.06 + 0.720*np.sin(a)],
            color="#c9a271", lw=0.5, zorder=9)

# ---------- blood vessels and nerve cord ----------
ax.add_patch(Circle((0, 1.18), 0.135, fc="#c0392b", ec=INK, lw=0.7, zorder=10))
ax.add_patch(Circle((0, -1.14), 0.115, fc="#1d6fb8", ec=INK, lw=0.7, zorder=10))
ax.add_patch(Circle((0, -1.345), 0.115, fc="#e2c96a", ec=NDK if False else "#8a6a12",
                    lw=0.7, zorder=10))
ax.add_patch(Circle((0, -1.478), 0.075, fc="#1d6fb8", ec=INK, lw=0.6, zorder=11))

# ---------- setae in their setal sacs ----------
for a_deg in (248, 262, 278, 292):
    a = np.radians(a_deg)
    ax.add_patch(Ellipse((1.78*np.cos(a), 1.78*np.sin(a)), 0.20, 0.10,
                         angle=a_deg - 90, fc="#f7f1e6", ec=EDGE, lw=0.6, zorder=8))
    ax.plot([1.86*np.cos(a), 2.26*np.cos(a)], [1.86*np.sin(a), 2.26*np.sin(a)],
            color="#6a4522", lw=1.1, zorder=6, solid_capstyle='round')

# ---------- nephridia coiled in the coelom ----------
for s in (1, -1):
    u = np.linspace(0, 4.2*np.pi, 300)
    nx = s*(1.21 + 0.175*np.sin(u))
    ny = -0.52 + 0.072*u
    ax.plot(nx, ny, color="#7c5fa0", lw=0.95, zorder=9)
    ax.plot([s*1.21, s*1.52], [-0.52, -0.80], color="#7c5fa0", lw=0.8, zorder=9)

# ---------- chloragogen cells stippled on the gut surface ----------
rng = np.random.default_rng(7)
for a in np.linspace(0, 2*np.pi, 60, endpoint=False):
    r = 0.918 + 0.018*rng.standard_normal()
    ax.add_patch(Circle((r*np.cos(a), -0.06 + r*np.sin(a)), 0.030, fc="#6f8f5e",
                        ec='none', zorder=10))

def lab(txt, tip, tx, ty_, ha='center', fs=6.0):
    ax.annotate(txt, xy=tip, xytext=(tx, ty_), fontsize=fs, color=INK, ha=ha,
                va='center', zorder=16,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7,
                                shrinkA=1.2, shrinkB=1.0))

d = np.radians
lab("cuticle", (1.97*np.cos(d(72)), 1.97*np.sin(d(72))), 1.25, 2.95, ha='left')
lab("epidermis", (1.90*np.cos(d(52)), 1.90*np.sin(d(52))), 2.45, 2.35, ha='left')
lab("circular muscle", (1.77*np.cos(d(36)), 1.77*np.sin(d(36))), 2.60, 1.70, ha='left')
lab("longitudinal muscle", (1.60*np.cos(d(20)), 1.60*np.sin(d(20))), 2.60, 1.10,
    ha='left')
lab("coelomic cavity", (1.20*np.cos(d(6)), 1.20*np.sin(d(6))), 2.60, 0.50, ha='left')
lab("chloragogen cells", (0.92*np.cos(d(-24)), -0.06 + 0.92*np.sin(d(-24))),
    2.60, -0.12, ha='left')
lab("nephridium", (1.27, -0.35), 2.60, -0.72, ha='left')
lab("ventral blood vessel", (0.11, -1.16), 2.60, -1.35, ha='left')
lab("setae", (2.20*np.cos(d(292)), 2.20*np.sin(d(292))), 2.20, -2.55, ha='left')

lab("dorsal blood vessel", (-0.12, 1.20), -1.35, 2.95, ha='right')
lab("typhlosole", (-0.14, 0.45), -2.55, 2.30, ha='right')
lab("intestinal lumen", (-0.55, 0.42), -2.70, 1.68, ha='right')
lab("intestinal epithelium", (-0.80, -0.06), -2.70, 1.08, ha='right')
lab("parietal peritoneum", (-1.49*np.cos(d(14)), -1.49*np.sin(d(14))),
    -2.70, 0.48, ha='right')
lab("body wall muscles", (-1.60*np.cos(d(28)), -1.60*np.sin(d(28))), -2.70, -0.12,
    ha='right')
lab("ventral nerve cord", (-0.11, -1.35), -2.70, -1.35, ha='right')
lab("sub-neural vessel", (-0.05, -1.50), -2.20, -2.55, ha='right')

ax.set_xlim(-5.10, 5.10); ax.set_ylim(-3.15, 3.35)
ax.set_aspect('equal'); ax.axis('off')
```

From outside inwards the body wall has five layers: a thin non-cellular
**cuticle**; a single-layered **epidermis** of columnar supporting cells with
glandular, basal and sensory cells among them; a thin **circular muscle** layer;
a thick **longitudinal muscle** layer in bundles; and an inner **coelomic
epithelium**.

The **coelom** is a true schizocoelic cavity partitioned by intersegmental
**septa**. It holds a milky alkaline **coelomic fluid** with proteins, salts and
free **coelomocytes** — the worm's hydrostatic skeleton and transport medium
and, squeezed out through the dorsal pores, the source of the film of moisture
the skin needs.

**Locomotion** follows directly. The coelomic fluid is incompressible and the
septa stop it flowing far, so when the circular muscles of the front segments
contract those segments become long and thin and are pushed forward; their setae
anchor them, the longitudinal muscles contract, and the rest of the body is
drawn up. A wave of this alternate contraction travels backwards and the worm
creeps forward at about 25 cm a minute.

::: example
**How many setae does an earthworm carry?** A *Pheretima posthuma* has 120
segments. Setae are absent from segment 1, from the clitellum (14, 15, 16) and
from the last segment. Taking an average of 100 setae per setigerous segment,
estimate the total.

Setigerous segments $= 120 - 1 - 3 - 1 = 115$, so the total is

$$ N = 115 \times 100 = 1.15 \times 10^{4} $$

about eleven and a half thousand; the extremes of the range give 9200 and
13800, so "roughly ten thousand setae" is safe for any *Pheretima*. *Lumbricus*,
with 8 setae in each of about 115 segments, has only about 920 — the
perichaetine arrangement gives more than ten times as many anchor points.
:::

### Digestive system

```figure caption="Alimentary canal of *Pheretima posthuma*, L.S."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Ellipse
fig, ax = plt.subplots(figsize=(5.2, 3.0))
WALL = "#f0dfc4"; EDGE = "#8a5a33"; GUT = "#d8b489"; MUS = "#c08a5a"
INT = "#e2c49c"

# ---------- body wall in longitudinal section ----------
xb = np.linspace(-4.95, 4.85, 600)
wb = 0.60*np.clip(1 - (np.abs(xb + 0.05)/5.10)**6, 0, 1)**0.42
ax.add_patch(Polygon(np.vstack([np.c_[xb, wb], np.c_[xb[::-1], -wb[::-1]]]),
                     closed=True, fc=WALL, ec=EDGE, lw=1.25, zorder=2))

# ---------- alimentary canal ----------
xk = [-4.70, -4.42, -4.16, -4.06, -3.72, -3.42, -2.78, -2.66, -2.08, -1.96,
      -0.92, -0.80, 4.32, 4.62]
wk = [0.02, 0.10, 0.11, 0.25, 0.27, 0.11, 0.11, 0.26, 0.26, 0.15,
      0.17, 0.31, 0.28, 0.04]
xg = np.linspace(xk[0], xk[-1], 600)
wg = np.interp(xg, xk, wk)
ax.add_patch(Polygon(np.vstack([np.c_[xg, wg], np.c_[xg[::-1], -wg[::-1]]]),
                     closed=True, fc=GUT, ec=EDGE, lw=1.0, zorder=5))
# gizzard: thick muscular wall
mg = (xg >= -2.66) & (xg <= -2.08)
ax.add_patch(Polygon(np.vstack([np.c_[xg[mg], wg[mg]], np.c_[xg[mg][::-1], -wg[mg][::-1]]]),
                     closed=True, fc=MUS, ec=EDGE, lw=1.2, zorder=6))
ax.add_patch(Polygon(np.vstack([np.c_[xg[mg], wg[mg]*0.40],
                                np.c_[xg[mg][::-1], -wg[mg][::-1]*0.40]]),
                     closed=True, fc="#f4e6d2", ec=EDGE, lw=0.7, zorder=7))
# intestine shading + typhlosole (dorsal infold, from segment 26 backwards)
mi = xg >= -0.80
ax.add_patch(Polygon(np.vstack([np.c_[xg[mi], wg[mi]], np.c_[xg[mi][::-1], -wg[mi][::-1]]]),
                     closed=True, fc=INT, ec=EDGE, lw=1.0, zorder=5))
xt = np.linspace(0.30, 4.20, 240)
wt = np.interp(xt, xk, wk)
yt = wt - 0.075 - 0.030*np.sin(7.5*xt)
ax.fill_between(xt, wt - 0.012, yt, color="#c08a5a", ec=EDGE, lw=0.7, zorder=7)
# intestinal caeca: one pair at segment 26, directed forwards
for s in (1, -1):
    ca = np.array([[-0.05, s*0.28], [-0.30, s*0.52], [-0.72, s*0.58],
                   [-0.86, s*0.44], [-0.52, s*0.36], [-0.20, s*0.22]])
    ax.add_patch(Polygon(ca, closed=True, fc=INT, ec=EDGE, lw=0.9, zorder=8))
# calciferous glands in the wall of the stomach
for s in (1, -1):
    for cx in (-1.76, -1.48, -1.20, -0.98):
        ax.add_patch(Ellipse((cx, s*0.245), 0.20, 0.17, fc="#cfe0ee", ec=EDGE,
                             lw=0.7, zorder=7))
# pharyngeal (salivary) mass
ax.add_patch(Ellipse((-3.88, 0.40), 0.46, 0.22, fc="#cfe0ee", ec=EDGE, lw=0.7,
                     zorder=6))
# mouth and anus
ax.plot([-4.95, -4.68], [-0.04, -0.02], color="#a2453e", lw=1.8, zorder=8)
ax.plot([4.62, 4.84], [0.00, 0.00], color="#a2453e", lw=1.8, zorder=8)

# ---------- septa between successive segments ----------
for xs in np.arange(-4.30, 4.60, 0.31):
    ww = np.interp(xs, xb, wb); gg = np.interp(xs, xg, wg)
    if ww < 0.10:
        continue
    for s in (1, -1):
        if ww - 0.02 > gg + 0.02:
            ax.plot([xs, xs], [s*(gg + 0.02), s*(ww - 0.02)], color=MUTED,
                    lw=0.45, zorder=3)

# ---------- labels ----------
def lab(txt, tip, tx, ty, ha='center', fs=6.1):
    ax.annotate(txt, xy=tip, xytext=(tx, ty), fontsize=fs, color=INK, ha=ha,
                va='center', zorder=14,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.75,
                                shrinkA=1.5, shrinkB=1.0))

lab("buccal cavity (1-3)", (-4.30, 0.11), -4.55, 1.85)
lab("pharynx (4-5)", (-3.86, 0.44), -3.45, 1.18)
lab("gizzard (8-9)", (-2.36, 0.30), -1.75, 1.85)
lab("typhlosole", (2.20, 0.18), 1.10, 1.85)
lab("septum", (3.42, 0.44), 3.30, 1.85)
lab("anus", (4.76, 0.00), 4.75, 1.18)
lab("mouth", (-4.88, -0.04), -5.05, -1.30)
lab("oesophagus (5-7)", (-3.10, 0.13), -3.30, -1.30)
lab("stomach (9-14) with\ncalciferous glands", (-1.40, -0.30), -0.70, -1.32)
lab("intestine (15 to last segment)", (2.30, -0.28), 2.90, -1.30)
lab("intestinal caeca (26)", (-0.60, -0.52), 1.60, -1.98)

ax.set_xlim(-6.00, 6.00); ax.set_ylim(-2.50, 2.20)
ax.set_aspect('equal'); ax.axis('off')
```

The alimentary canal is a straight tube from mouth to anus — the
tube-within-a-tube plan at its clearest. Its regions and their segment numbers
must be memorised.

| Region | Segments | Structure and function |
|---|---|---|
| Mouth and buccal cavity | 1–3 | thin-walled and eversible; takes in soil and leaf fragments |
| Pharynx | 4–5 | muscular and bulbous; **pharyngeal (salivary) glands** secrete mucus and a proteolytic enzyme; acts as a suction pump |
| Oesophagus | 5–7 | short, narrow conducting tube |
| Gizzard | 8–9 | thick, highly muscular, cuticle-lined; **grinds** the food to a paste |
| Stomach | 9–14 | glandular; **calciferous glands** in its wall secrete calcium carbonate, which **neutralises the humic acid** of the soil |
| Intestine | 15 to the last segment | main site of digestion and absorption; bears the typhlosole and the caeca |
| Anus | last segment | egests the castings |

A pair of conical **intestinal caeca** arises at **segment 26** and projects
forwards over segments 22–25, secreting amylase. A **typhlosole**, a deep
glandular median infolding of the dorsal wall, runs from about segment 26 to
within 25 segments of the hind end; it increases the absorptive surface without
lengthening the gut — the trick the human ileum plays with villi.

Digestion is **extracellular**, using proteases, amylases, and cellulase and
chitinase largely of bacterial origin; the undigested soil leaves as **worm
castings**, richer in nitrogen, phosphorus, potassium and calcium than the soil
around them.

### Blood vascular system

```figure caption="Blood vascular system of *Pheretima posthuma*."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Ellipse, FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.2, 3.0))
RED = "#c0392b"; BLU = "#1d6fb8"; EDGE = "#8a5a33"; GUTC = "#efe0c8"

def sx(n):                      # x-coordinate of segment n
    return -4.30 + 0.40*(n - 1)

# ---------- body wall (schematic) and gut ----------
ax.add_patch(FancyBboxPatch((-4.80, -1.62), 9.60, 3.00,
                            boxstyle="round,pad=0.02,rounding_size=0.55",
                            fc="#fdfaf5", ec=MUTED, lw=0.9, ls=(0, (4, 3)),
                            zorder=1))
ax.add_patch(FancyBboxPatch((-4.55, -0.22), 9.10, 0.44,
                            boxstyle="round,pad=0.01,rounding_size=0.18",
                            fc=GUTC, ec=EDGE, lw=0.8, zorder=2))
ax.text(3.35, 0.00, "alimentary canal", ha='center', va='center', fontsize=5.7,
        color=MUTED, style='italic', zorder=3)

# ---------- longitudinal vessels ----------
# dorsal vessel: contractile, blood driven forwards (posterior to anterior)
ax.plot([-4.50, 4.50], [1.00, 1.00], color=RED, lw=3.0, zorder=6,
        solid_capstyle='round')
for xa in (3.9, 2.3, -1.4, -3.0):
    ax.annotate('', xy=(xa - 0.34, 1.00), xytext=(xa, 1.00),
                arrowprops=dict(arrowstyle='-|>', color="#7d1f14", lw=1.0,
                                mutation_scale=8), zorder=8)
# ventral vessel: distributing, blood carried backwards
ax.plot([-4.50, 4.50], [-0.82, -0.82], color=BLU, lw=2.6, zorder=6,
        solid_capstyle='round')
for xa in (-3.6, -2.0, 1.6, 3.0):
    ax.annotate('', xy=(xa + 0.34, -0.82), xytext=(xa, -0.82),
                arrowprops=dict(arrowstyle='-|>', color="#0f4a80", lw=1.0,
                                mutation_scale=8), zorder=8)
# ventral nerve cord and the sub-neural vessel lying beneath it
ax.plot([-4.20, 4.30], [-1.16, -1.16], color="#e2c96a", lw=2.4, zorder=5,
        solid_capstyle='round')
ax.plot([-4.20, 4.30], [-1.40, -1.40], color=BLU, lw=1.5, zorder=6,
        solid_capstyle='round')
# supra-oesophageal vessel (segments 9-13)
ax.plot([sx(9) - 0.18, sx(13) + 0.18], [0.46, 0.46], color="#8e2c20", lw=2.2,
        zorder=9, solid_capstyle='round')
# lateral oesophageal vessel
ax.plot([sx(3), sx(14)], [-0.46, -0.46], color="#3a86c8", lw=1.6, zorder=6,
        solid_capstyle='round')

# ---------- hearts ----------
t = np.linspace(0, 1, 60)
def heart(xc, ytop, ybot, col, amp=0.30, z=5):
    yy = ytop + (ybot - ytop)*t
    xx = xc + amp*np.sin(np.pi*t)
    ax.fill_betweenx(yy, 2*xc - xx, xx, color=col, alpha=0.95, zorder=z)
    ax.plot(xx, yy, color="#7d1f14", lw=0.8, zorder=z + 1)
    ax.plot(2*xc - xx, yy, color="#7d1f14", lw=0.8, zorder=z + 1)

for n in (7, 9):
    heart(sx(n), 1.00, -0.82, "#d9776c")
for n in (12, 13):
    heart(sx(n), 0.46, -0.82, "#a93226", amp=0.24, z=7)
    ax.plot([sx(n), sx(n)], [0.46, 1.00], color="#a93226", lw=1.5, zorder=6)

# ---------- segment scale ----------
for n in (1, 5, 7, 9, 12, 13, 15):
    ax.plot([sx(n), sx(n)], [1.52, 1.62], color=MUTED, lw=0.6, zorder=4)
    ax.text(sx(n), 1.78, str(n), ha='center', va='center', fontsize=5.6,
            color=MUTED)
ax.plot([sx(1), sx(15)], [1.52, 1.52], color=MUTED, lw=0.6, zorder=4)
ax.text(sx(15) + 0.30, 1.72, "segment no.", ha='left', va='center', fontsize=5.6,
        color=MUTED)
ax.text(-4.95, 1.72, "anterior", ha='right', va='center', fontsize=5.8,
        color="#2e6b4f")
ax.text(4.95, 1.72, "posterior", ha='left', va='center', fontsize=5.8,
        color="#2e6b4f")

def lab(txt, tip, tx, ty, ha='center', fs=6.1):
    ax.annotate(txt, xy=tip, xytext=(tx, ty), fontsize=fs, color=INK, ha=ha,
                va='center', zorder=14,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.75,
                                shrinkA=1.5, shrinkB=1.0))

lab("supra-oesophageal vessel (9-13)", (sx(11), 0.46), -3.10, 2.98)
lab("dorsal vessel (collecting)", (2.90, 1.00), 2.60, 2.98)
lab("lateral hearts (7, 9)", (sx(7) - 0.26, 0.30), -3.60, 2.36)
lab("latero-oesophageal hearts (12, 13)", (sx(13) + 0.22, -0.20), 1.60, 2.36)
lab("lateral oesophageal vessel", (sx(5), -0.46), -3.70, -2.28)
lab("ventral vessel (distributing)", (2.20, -0.82), 1.90, -2.28)
lab("ventral nerve cord", (-2.90, -1.16), -2.40, -2.90)
lab("sub-neural vessel", (1.10, -1.40), 1.80, -2.90)

ax.set_xlim(-6.30, 6.30); ax.set_ylim(-3.30, 3.30)
ax.set_aspect('equal'); ax.axis('off')
```

The system is **closed** — blood never leaves the vessels and never enters the
coelom. The blood is red because **haemoglobin is dissolved in the plasma**
rather than packed into cells, the reverse of the vertebrate arrangement; the
only blood cells are colourless, nucleated amoebocytes.

The main longitudinal vessels are the **dorsal vessel** above the gut, the chief
*collecting* vessel, contractile and valved, in which blood flows **forwards**;
the **ventral vessel** below the gut, the chief *distributing* vessel, in which
blood flows **backwards** and which supplies a pair of branches to every
segment; the **sub-neural vessel** below the nerve cord; and the
**supra-oesophageal** and paired **lateral oesophageal** vessels serving the
anterior gut.

| Hearts | Segments | Connection |
|---|---|---|
| Lateral hearts | 7 and 9 | dorsal vessel to ventral vessel |
| Latero-oesophageal hearts | 12 and 13 | dorsal and supra-oesophageal vessels to the ventral vessel |

All four pairs are contractile, valved and vertical. Blood collected from the
gut, body wall and nephridia enters the dorsal vessel, is driven forward, passes
down through the hearts into the ventral vessel and is distributed backwards.

### Respiratory system

There are no respiratory organs: respiration is entirely **cutaneous**. Oxygen
dissolves in the film of mucus and coelomic fluid on the cuticle, diffuses
through the thin epidermis into a dense subcuticular capillary network and binds
to the plasma haemoglobin; carbon dioxide leaves by the reverse route. All of it
depends on the skin staying wet — which is why the worm is nocturnal and
suffocates if its skin dries.

### Excretory system

Excretion is by thousands of **nephridia**. A typical nephridium is a coiled
tubule beginning in a ciliated funnel, the **nephrostome**, opening into the
coelom of the segment in front, then a narrow neck, a long twisted body and a
terminal duct. Three kinds occur, and the distinction between **exonephric**
and **enteronephric** types is characteristic of *Pheretima*.

| Type | Position | Opening |
|---|---|---|
| Septal nephridia | on both faces of the septa, from segment 15 backwards | into the intestine (enteronephric) |
| Integumentary nephridia | on the inner body wall from segment 3 back, most numerous in the clitellum | through nephridiopores (exonephric) |
| Pharyngeal nephridia | three paired tufts in segments 4, 5 and 6 | into the buccal cavity and pharynx (enteronephric) |

The waste is chiefly **ammonia and urea**: the worm is ammonotelic in wet soil
and shifts towards ureotelism as it dries. **Chloragogen cells** round the gut
and dorsal vessel store and excrete waste, like a vertebrate liver. Because the
septal and pharyngeal nephridia empty into the gut, much of their water is
reabsorbed.

### Nervous system and sense organs

```figure caption="Nervous system of *Pheretima posthuma*."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Ellipse
fig, ax = plt.subplots(figsize=(5.2, 2.7))
NRV = "#d4a017"; NDK = "#8a6a12"; PHA = "#f0dfc4"; EDGE = "#8a5a33"

# ---------- pharynx (shown only as a guide) ----------
ax.add_patch(Ellipse((-3.35, -0.02), 1.55, 1.05, fc=PHA, ec=EDGE, lw=0.9,
                     ls=(0, (4, 3)), zorder=2))
ax.text(-3.35, -0.02, "pharynx", ha='center', va='center', fontsize=5.8,
        color=MUTED, style='italic', zorder=3)

# ---------- cerebral ganglia (supra-pharyngeal, segment 3) ----------
for dx in (-0.17, 0.17):
    ax.add_patch(Ellipse((-3.40 + dx, 0.70), 0.34, 0.26, fc=NRV, ec=NDK, lw=0.9,
                         zorder=6))
# nerves running forwards to the prostomium and buccal chamber
for tipx, tipy in [(-4.95, 1.08), (-5.05, 0.74), (-4.95, 0.40)]:
    ax.plot([-3.60, -4.25, tipx], [0.70, 0.94, tipy], color=NRV, lw=1.1, zorder=5,
            solid_capstyle='round')

# ---------- circum-pharyngeal connectives ----------
t = np.linspace(0, 1, 60)
for a in (0.62, -0.62):
    ax.plot(-3.40 + a*np.sin(np.pi*t), 0.66 - 1.38*t, color=NRV, lw=1.6, zorder=5)

# ---------- sub-pharyngeal ganglion (segment 4) ----------
ax.add_patch(Ellipse((-3.40, -0.76), 0.62, 0.28, fc=NRV, ec=NDK, lw=1.0, zorder=6))

# ---------- ventral nerve cord with segmental ganglia ----------
ax.plot([-3.40, 4.55], [-0.76, -0.76], color=NRV, lw=2.4, zorder=5,
        solid_capstyle='round')
gx = np.arange(-2.60, 4.30, 0.78)
for x in gx:
    ax.add_patch(Ellipse((x, -0.76), 0.40, 0.22, fc=NRV, ec=NDK, lw=0.8, zorder=6))
    for s in (1, -1):
        for dx, dy in [(-0.10, 0.46), (0.10, 0.50), (0.28, 0.42)]:
            ax.plot([x + dx*0.4, x + dx], [-0.76, -0.76 + s*dy], color=NRV,
                    lw=0.8, zorder=4, solid_capstyle='round')
    ax.plot([x + 0.39, x + 0.39], [-0.66, -0.86], color=MUTED, lw=0.4, zorder=4)

def lab(txt, tip, tx, ty, ha='center', fs=6.1):
    ax.annotate(txt, xy=tip, xytext=(tx, ty), fontsize=fs, color=INK, ha=ha,
                va='center', zorder=14,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.75,
                                shrinkA=1.5, shrinkB=1.0))

lab("cerebral ganglia (the 'brain',\nsegment 3)", (-3.40, 0.84), -2.75, 2.05)
lab("nerves to prostomium\nand buccal chamber", (-4.70, 0.94), -5.30, 2.05, ha='right')
lab("circum-pharyngeal\nconnective", (-2.78, -0.05), -1.05, 0.62, ha='left')
lab("sub-pharyngeal ganglion\n(segment 4)", (-3.45, -0.92), -4.05, -1.80, ha='center')
lab("double, solid, ventral nerve\ncord (fused pair)", (1.05, -0.78), 0.90, -1.85)
lab("segmental ganglion", (2.20, -0.68), 2.55, 1.10, ha='center')
lab("three pairs of\nlateral nerves", (3.55, -0.30), 4.25, 0.92, ha='left')

ax.set_xlim(-6.60, 6.60); ax.set_ylim(-2.45, 2.45)
ax.set_aspect('equal'); ax.axis('off')
```

The **central nervous system** is a nerve ring round the pharynx plus a cord
below the gut. A pair of **cerebral ganglia** (the "brain") lies on the pharynx
in **segment 3**; two **circumpharyngeal connectives** pass round the pharynx to
the **sub-pharyngeal ganglia** in segment 4; and from these the **ventral nerve
cord** runs to the last segment. The cord is double but fused, **solid** and
**ventral**, with a swollen **ganglion in every segment** giving off three pairs
of lateral nerves — the exact opposite of the chordate plan, which is single,
hollow and dorsal. An autonomic plexus lies in the wall of the gut.

Sense organs are simple: **no eyes**, but **photoreceptor cells** in the
epidermis, crowded on the prostomium, so the worm withdraws from light, plus
tactile, chemical and thermal receptors.

### Reproductive system and development

*Pheretima* is **hermaphrodite (monoecious)** but **protandrous**, the sperm
maturing before the ova, so self-fertilisation is impossible and
**cross-fertilisation** is the rule.

**Male organs.** Two pairs of **testes** lie in segments 10 and 11 in
fluid-filled **testis sacs**. Immature sperm pass to two pairs of **seminal
vesicles** in segments 11 and 12 to mature, are collected by **spermiducal
funnels** into the **vasa deferentia**, and leave by the male genital pores on
segment 18. Two pairs of **prostate glands** in segments 16–21 secrete a fluid
that activates the sperm.

**Female organs.** A single pair of **ovaries** hangs from the septum in
**segment 13**. Ova are shed into the coelom, gathered by ciliated **oviducal
funnels** and carried by short oviducts that unite to open at the single
mid-ventral female genital pore on segment 14. Four pairs of **spermathecae** in
segments 6, 7, 8 and 9 store the partner's sperm.

**Copulation and development.** On a warm damp night two worms meet head to
tail, apply their ventral surfaces and are bound by a mucus sheath from the
clitella, each charging the other's spermathecae. Days later the clitellum
secretes a tough **cocoon** with a store of albumen; the worm wriggles backwards
out of it, and as the cocoon slides forward it picks up ova at segment 14 and
stored sperm at segments 6–9. **Fertilisation is therefore external, inside the
cocoon.** One to four young worms emerge after two or three weeks. Development
is **direct**.

::: caution
Two marks are regularly thrown away here. A hermaphrodite is not necessarily
self-fertilising: *Pheretima* is hermaphrodite **and** cross-fertilising. And
although sperm pass from body to body, fertilisation happens **outside** both
worms, in the cocoon — so write "external fertilisation", not "internal".
:::

### Economic importance

The burrows aerate and drain the soil, and a healthy field may hold over a
million worms per hectare. The castings are rich in available nitrogen,
phosphate, potash, calcium and humus, so the worm continuously manufactures
topsoil — Darwin's reason for calling it the farmer's friend. Farmed worms turn
kitchen and farm waste into **vermicompost**, now a small enterprise in Nepal's
hill districts, and worm meal is used as poultry and fish feed. Against this,
casts spoil lawns and earthworms host poultry parasites such as *Syngamus*.

## 8.4 Frog (*Rana tigrina*)

*Rana tigrina*, the Indian bull frog, is the commonest large frog of the
Nepalese Terai and the standard vertebrate type study. It leads two lives:
beginning as a gill-breathing herbivorous tadpole in water and ending as a
lung-breathing carnivore largely on land.

### Habit and habitat

The frog is **amphibious**, living in ponds, ditches and paddy fields;
**nocturnal**; **carnivorous**, taking insects, worms, snails and small fish;
and **poikilothermic**. Unable to regulate its temperature, it **hibernates**
in winter and **aestivates** in the hot dry season, buried in mud, living on
stored fat and respiring only through the skin. Its mottled olive-green back is
protective **camouflage**.

### External features

The body is divided into **head** and **trunk**; there is no neck and no tail in
the adult. The skin is smooth, moist, slimy and scaleless, loosely attached and
packed with mucous glands and blood capillaries — a respiratory organ as much as
a covering.

The head bears a blunt **snout**, a wide **mouth**, a pair of valved **external
nares**, two bulging **eyes** with a fixed upper eyelid, a movable lower eyelid
and a transparent **nictitating membrane** that covers the eye under water, and
behind each eye a circular **tympanum** flush with the skin — there is no
external ear. The **forelimbs** are short and four-digited; the **hindlimbs**
are long, muscular and five-toed with **webbed** feet for leaping and swimming.
The single **cloacal aperture** passes faeces, urine and gametes alike.

**Sexual dimorphism**: the male is smaller, has a larger tympanum, a pair of
**vocal sacs** at the angles of the jaws, and a rough dark **nuptial pad** on
the first digit of each forelimb for gripping the female in amplexus.

### Digestive system

```figure caption="Digestive system of *Rana tigrina*, liver displaced."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Ellipse
fig, ax = plt.subplots(figsize=(5.2, 3.7))
GUT = "#e8c9a6"; EDGE = "#8a5a33"; LIV = "#a4574f"; LIV2 = "#bd6d63"

def smooth(pts, k=9, n=400):
    p = np.asarray(pts, float)
    t = np.linspace(0, 1, len(p)); tf = np.linspace(0, 1, n)
    c = np.c_[np.interp(tf, t, p[:, 0]), np.interp(tf, t, p[:, 1])]
    ker = np.ones(k)/k
    for j in (0, 1):
        c[:, j] = np.convolve(np.pad(c[:, j], (k, k), mode='edge'), ker,
                              mode='same')[k:-k]
    return c

def tube(cline, ws, fc=GUT, ec=EDGE, lw=1.0, z=4):
    c = np.asarray(cline, float)
    t = np.gradient(c, axis=0)
    L = np.hypot(t[:, 0], t[:, 1]); L[L == 0] = 1
    nv = np.c_[-t[:, 1]/L, t[:, 0]/L]
    w = np.asarray(ws, float)[:, None]
    ax.add_patch(Polygon(np.vstack([c + nv*w, (c - nv*w)[::-1]]), closed=True,
                         fc=fc, ec=ec, lw=lw, zorder=z))

# ================= liver, three lobes =================
ax.add_patch(Polygon([[-1.05, 3.00], [-1.85, 3.15], [-2.55, 2.62], [-2.62, 1.95],
                      [-2.12, 1.48], [-1.55, 1.62], [-1.10, 2.10]], closed=True,
                     fc=LIV, ec="#6d332d", lw=1.0, zorder=3))
ax.add_patch(Polygon([[-1.00, 2.95], [-0.88, 2.28], [-1.10, 1.74], [-1.55, 1.60],
                      [-1.80, 2.02], [-1.62, 2.66]], closed=True, fc=LIV2,
                     ec="#6d332d", lw=1.0, zorder=4))
ax.add_patch(Polygon([[-2.10, 1.50], [-2.58, 1.14], [-2.28, 0.66], [-1.70, 0.78],
                      [-1.54, 1.24]], closed=True, fc=LIV, ec="#6d332d", lw=1.0,
                     zorder=3))
ax.add_patch(Ellipse((-1.62, 1.40), 0.32, 0.26, angle=-18, fc="#5f9e6a",
                     ec="#2f5f39", lw=0.9, zorder=6))
ax.plot([-1.48, -0.40], [1.34, 1.16], color="#5f9e6a", lw=1.0, zorder=7)

# ================= buccal cavity, tongue, oesophagus =================
ax.add_patch(Ellipse((0.28, 3.48), 1.95, 0.92, fc="#f3e0cd", ec=EDGE, lw=1.1,
                     zorder=5))
ax.add_patch(Polygon([[0.28, 3.82], [0.74, 3.58], [0.80, 3.22], [0.44, 3.10],
                      [0.28, 3.24], [0.12, 3.10], [-0.24, 3.22], [-0.18, 3.58]],
                     closed=True, fc="#e8a9a3", ec="#a2453e", lw=0.9, zorder=6))
for s in (1, -1):
    ax.add_patch(Circle((0.28 + s*0.70, 3.70), 0.10, fc="#cfe0ee", ec=EDGE,
                        lw=0.7, zorder=6))
oes = smooth([[0.18, 3.06], [0.20, 2.82], [0.22, 2.58]], k=5, n=60)
tube(oes, np.full(60, 0.15), z=6)

# ================= stomach =================
st = smooth([[0.22, 2.60], [0.52, 2.22], [0.74, 1.80], [0.78, 1.34],
             [0.62, 0.98], [0.32, 0.76]], k=21, n=220)
ws = np.interp(np.linspace(0, 1, 220), [0, 0.15, 0.40, 0.70, 0.90, 1.0],
               [0.16, 0.34, 0.44, 0.40, 0.24, 0.14])
tube(st, ws, fc="#dfb98f", lw=1.2, z=6)

# ================= duodenum =================
du = smooth([[0.30, 0.76], [-0.02, 0.92], [-0.22, 1.26], [-0.20, 1.62],
             [-0.08, 1.84]], k=15, n=150)
tube(du, np.full(150, 0.16), z=7)

# ================= ileum: long coiled loop =================
il = smooth([[-0.08, 1.86], [-0.42, 1.72], [-0.58, 1.38], [-0.44, 1.04],
             [0.10, 0.90], [0.76, 0.82], [1.02, 0.52], [0.82, 0.22],
             [0.10, 0.14], [-0.60, 0.06], [-0.90, -0.24], [-0.70, -0.54],
             [0.00, -0.62], [0.76, -0.68], [0.98, -0.98], [0.78, -1.28],
             [0.10, -1.36], [-0.46, -1.42], [-0.64, -1.70], [-0.36, -1.92],
             [0.02, -1.98]], k=11, n=560)
tube(il, np.full(560, 0.135), z=5)

# ================= rectum and cloaca =================
re = smooth([[0.04, -1.98], [0.06, -2.34], [0.06, -2.70]], k=5, n=80)
tube(re, np.linspace(0.26, 0.20, 80), fc="#dfb98f", lw=1.1, z=6)
ax.add_patch(Ellipse((0.06, -2.90), 0.44, 0.34, fc="#d7ab7e", ec=EDGE, lw=1.0,
                     zorder=7))
ax.plot([-0.04, 0.16], [-3.08, -3.08], color="#a2453e", lw=1.6, zorder=8)

# ================= pancreas and spleen =================
ax.add_patch(Polygon([[0.12, 1.02], [0.36, 1.26], [0.40, 1.60], [0.22, 1.68],
                      [0.10, 1.40], [0.02, 1.14]], closed=True, fc="#e8d08a",
                     ec="#9a8330", lw=0.9, zorder=8))
ax.add_patch(Circle((1.42, -0.42), 0.19, fc="#8e3b34", ec="#5b241f", lw=0.8,
                    zorder=8))
ax.plot([1.24, 0.98], [-0.48, -0.60], color="#8e3b34", lw=0.8, zorder=7)

def lab(txt, tip, tx, ty, ha='center', fs=6.1):
    ax.annotate(txt, xy=tip, xytext=(tx, ty), fontsize=fs, color=INK, ha=ha,
                va='center', zorder=16,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.75,
                                shrinkA=1.4, shrinkB=1.0))

lab("buccal cavity", (1.16, 3.42), 2.35, 3.90, ha='left')
lab("bilobed tongue", (0.66, 3.52), 2.35, 3.24, ha='left')
lab("oesophagus", (0.30, 2.66), 2.35, 2.58, ha='left')
lab("cardiac end of stomach", (0.68, 2.06), 2.35, 1.92, ha='left')
lab("pyloric end of stomach", (0.68, 1.00), 2.35, 1.26, ha='left')
lab("pancreas", (0.38, 1.44), 2.35, 0.60, ha='left')
lab("ileum (coiled small intestine)", (1.14, 0.52), 2.35, -0.06, ha='left')
lab("spleen", (1.60, -0.40), 2.35, -0.72, ha='left')
lab("rectum (large intestine)", (0.30, -2.36), 2.35, -1.38, ha='left')
lab("cloaca and cloacal aperture", (0.28, -2.94), 2.35, -2.04, ha='left')

lab("right lobe of liver", (-2.05, 2.70), -3.05, 3.60, ha='right')
lab("left lobe of liver", (-1.30, 2.40), -3.05, 2.94, ha='right')
lab("gall bladder", (-1.78, 1.44), -3.05, 2.28, ha='right')
lab("posterior lobe of liver", (-2.26, 1.00), -3.05, 1.62, ha='right')
lab("bile duct opening into\nthe duodenum", (-0.90, 1.24), -3.05, 0.80, ha='right')
lab("duodenum", (-0.36, 1.32), -3.05, 0.02, ha='right')
lab("pyloric sphincter", (0.36, 0.78), -3.05, -0.62, ha='right')
lab("mesentery slung\nbetween gut loops", (-0.80, -1.00), -3.05, -1.50, ha='right')

ax.set_xlim(-7.00, 7.00); ax.set_ylim(-4.40, 4.40)
ax.set_aspect('equal'); ax.axis('off')
```

The alimentary canal is short, as in all carnivores. The **buccal cavity** has a
row of fine **maxillary teeth** on the upper jaw and two patches of **vomerine
teeth** on the palate, the lower jaw being toothless; the teeth do not chew but
only stop struggling prey escaping. The **tongue** is large, sticky and bilobed,
attached at the *front* of the floor and free behind, so it can be flicked far
out to catch an insect and flicked back with it.

Behind the **pharynx** a short **oesophagus** leads to the **stomach**, a wide
muscular bag with cardiac and pyloric regions that begins protein digestion. The
**small intestine** follows: the short **duodenum** beside the stomach, then the
long coiled **ileum**, lined with villi, where digestion is completed and
absorption occurs. The wide **rectum** absorbs water and opens into the
**cloaca**.

Two glands discharge into the duodenum: the dark-red **liver**, with a right and
a bilobed left lobe and the green **gall bladder** between them, whose bile
emulsifies fats and neutralises the acid chyme; and the yellowish **pancreas**,
whose duct joins the bile duct to form the **common bile duct**.

### Respiratory system

```figure caption="Frog respiration: (a) the air path, (b) a lung."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Ellipse, FancyBboxPatch
fig, axes = plt.subplots(1, 2, figsize=(5.2, 3.0))
SKIN = "#cfd8a8"; EDGE = "#5f6b3a"; LUNG = "#e8a9a3"; LEDGE = "#a2453e"
BLU = "#1d6fb8"

def smooth(pts, k=9, n=400, closed=True):
    p = np.asarray(pts, float)
    if closed:
        p = np.vstack([p, p[:1]])
    t = np.linspace(0, 1, len(p)); tf = np.linspace(0, 1, n)
    c = np.c_[np.interp(tf, t, p[:, 0]), np.interp(tf, t, p[:, 1])]
    ker = np.ones(k)/k
    for j in (0, 1):
        pad = np.r_[c[-k:, j], c[:, j], c[:k, j]] if closed else \
              np.pad(c[:, j], (k, k), mode='edge')
        c[:, j] = np.convolve(pad, ker, mode='same')[k:-k]
    return c

def lab(ax, txt, tip, tx, ty, ha='center', fs=6.0):
    ax.annotate(txt, xy=tip, xytext=(tx, ty), fontsize=fs, color=INK, ha=ha,
                va='center', zorder=16,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7,
                                shrinkA=1.3, shrinkB=1.0))

# ============ (a) air path through the frog, seen from the side ============
ax = axes[0]
body = smooth([[-3.52, -0.06], [-3.38, 0.20], [-3.05, 0.42], [-2.70, 0.74],
               [-2.35, 0.86], [-2.05, 0.66], [-1.45, 0.78], [-0.50, 0.92],
               [0.60, 0.86], [1.55, 0.62], [2.15, 0.26], [2.30, -0.20],
               [1.90, -0.66], [0.85, -0.90], [-0.45, -0.94], [-1.70, -0.84],
               [-2.65, -0.56], [-3.30, -0.28]], k=9, n=500)
ax.add_patch(Polygon(body, closed=True, fc=SKIN, ec=EDGE, lw=1.2, zorder=2))
ax.add_patch(Ellipse((-2.48, 0.62), 0.46, 0.34, angle=12, fc="#e9edd4", ec=EDGE,
                     lw=0.9, zorder=8))
ax.add_patch(Circle((-2.52, 0.64), 0.09, fc=INK, ec='none', zorder=9))
ax.add_patch(Circle((-1.62, 0.16), 0.24, fc='none', ec=EDGE, lw=0.8, zorder=8))
ax.plot([-3.52, -3.10], [-0.06, -0.14], color="#a2453e", lw=1.4, zorder=8)
# buccal cavity
buc = smooth([[-3.15, 0.04], [-2.60, 0.24], [-1.85, 0.26], [-1.25, 0.12],
              [-1.20, -0.08], [-1.90, -0.18], [-2.70, -0.16]], k=11, n=300)
ax.add_patch(Polygon(buc, closed=True, fc="#f3e0cd", ec=EDGE, lw=0.9, zorder=4))
# external and internal nares
ax.add_patch(Circle((-3.36, 0.20), 0.075, fc="#fdfbf7", ec=EDGE, lw=0.8, zorder=6))
ax.add_patch(Circle((-2.86, 0.26), 0.065, fc="#fdfbf7", ec=EDGE, lw=0.8, zorder=6))
ax.plot([-3.32, -2.90], [0.24, 0.28], color=EDGE, lw=0.8, zorder=5)
# glottis and laryngo-tracheal chamber
ax.add_patch(Ellipse((-1.12, 0.00), 0.16, 0.20, fc="#f6d7b8", ec=LEDGE, lw=0.9,
                     zorder=7))
ax.add_patch(FancyBboxPatch((-1.02, -0.14), 0.42, 0.30,
                            boxstyle="round,pad=0.01,rounding_size=0.10",
                            fc="#e9c9a4", ec=EDGE, lw=0.9, zorder=6))
# bronchi and lungs
for s in (1, -1):
    ax.plot([-0.58, -0.22], [0.01 + s*0.02, s*0.30], color=EDGE, lw=1.8, zorder=5,
            solid_capstyle='round')
    ax.add_patch(Ellipse((0.52, s*0.38), 1.42, 0.62, angle=s*6, fc=LUNG, ec=LEDGE,
                         lw=1.1, zorder=6))
    for u in np.linspace(-0.55, 0.55, 7):
        ax.plot([0.52 + u, 0.52 + u*0.92],
                [s*0.38 - 0.20 - 0.04*abs(u), s*0.38 + 0.20 + 0.04*abs(u)],
                color=LEDGE, lw=0.4, zorder=7, alpha=0.7)
# air-flow arrows
ax.annotate('', xy=(-3.22, 0.22), xytext=(-4.10, 0.46),
            arrowprops=dict(arrowstyle='-|>', color=BLU, lw=1.2, mutation_scale=8),
            zorder=9)
ax.annotate('', xy=(-1.30, 0.06), xytext=(-2.55, 0.10),
            arrowprops=dict(arrowstyle='-|>', color=BLU, lw=1.1, mutation_scale=8),
            zorder=9)
ax.annotate('', xy=(-0.25, 0.30), xytext=(-0.70, 0.05),
            arrowprops=dict(arrowstyle='-|>', color=BLU, lw=1.1, mutation_scale=8),
            zorder=9)
# cutaneous exchange arrows across the moist skin
for xx in (-1.10, 0.10, 1.25):
    ax.annotate('', xy=(xx, -0.80), xytext=(xx + 0.10, -1.40),
                arrowprops=dict(arrowstyle='-|>', color="#2e8b57", lw=1.0,
                                mutation_scale=7), zorder=9)

lab(ax, "external naris", (-3.40, 0.20), -2.70, 2.20, ha='center')
lab(ax, "internal naris", (-2.86, 0.32), -0.35, 2.68, ha='center')
lab(ax, "buccal cavity", (-2.20, 0.16), -2.85, 1.55, ha='center')
lab(ax, "glottis", (-1.12, 0.10), -0.50, 1.55, ha='center')
lab(ax, "laryngo-tracheal\nchamber", (-0.70, -0.14), 1.60, 1.90, ha='center')
lab(ax, "lung (ovoid, sac-like)", (1.00, 0.62), 2.05, 0.60, ha='left')
lab(ax, "bronchus", (-0.40, 0.18), 1.35, -0.70, ha='left')
lab(ax, "O$_2$ and CO$_2$ exchanged\nacross the moist skin", (0.10, -1.20),
    0.50, -2.35, ha='center')
ax.text(-3.90, 2.98, "(a)  The path taken by air", ha='left', fontsize=7.2,
        color=INK)

# ============ (b) internal structure of one lung ============
ax = axes[1]
ax.add_patch(Ellipse((0.15, 0.10), 3.30, 2.30, fc="#f6dedb", ec=LEDGE, lw=1.3,
                     zorder=3))
ax.add_patch(Ellipse((0.15, 0.10), 3.02, 2.02, fc=LUNG, ec=LEDGE, lw=0.8, zorder=4))
# alveolar honeycomb
a, b = 1.42, 0.96
for iy, yy in enumerate(np.arange(-0.90, 0.95, 0.225)):
    for xx in np.arange(-1.42, 1.45, 0.26) + (0.13 if iy % 2 else 0.0):
        if ((xx - 0.15)/a)**2 + ((yy - 0.10)/b)**2 < 0.94:
            ax.add_patch(Circle((xx, yy), 0.095, fc="#fbeceb", ec=LEDGE, lw=0.5,
                                zorder=5))
# capillary network running over the septa
rng = np.random.default_rng(11)
for k in range(9):
    y0 = -0.85 + 0.215*k
    xs = np.linspace(-1.45, 1.70, 120)
    inside = ((xs - 0.15)/a)**2 + ((y0 - 0.10)/b)**2 < 0.90
    if inside.sum() < 5:
        continue
    ys = y0 + 0.055*np.sin(7.5*xs + k)
    ax.plot(xs[inside], ys[inside], color="#c0392b", lw=0.55, zorder=6, alpha=0.85)
# bronchus entering
ax.add_patch(Polygon([[-1.55, 0.22], [-2.35, 0.46], [-2.35, 0.12], [-1.55, -0.10]],
                     closed=True, fc="#e9c9a4", ec=EDGE, lw=1.0, zorder=6))

lab(ax, "bronchus", (-2.10, 0.30), -2.90, 1.55, ha='center')
lab(ax, "elastic, vascular\nlung wall", (-0.95, 1.05), -2.30, 2.40, ha='center')
lab(ax, "alveoli (air sacs) formed\nby internal septa", (0.55, 0.55), 1.70, 2.35,
    ha='center')
lab(ax, "dense network of\nblood capillaries", (0.90, -0.55), 1.90, -1.65, ha='center')
lab(ax, "internal septum", (-0.40, -0.80), -1.90, -1.65, ha='center')
ax.text(-3.90, 2.98, "(b)  Internal structure of a lung", ha='left', fontsize=7.2,
        color=INK)

for ax in axes:
    ax.set_xlim(-4.30, 4.30); ax.set_ylim(-3.00, 3.20)
    ax.set_aspect('equal'); ax.axis('off')
fig.subplots_adjust(wspace=0.02)
```

The frog breathes in **three** ways, and a full answer must name all three.

1. **Cutaneous**, through the moist, thin, vascular skin. It works in water and
   in air, costs no muscular effort, and is the *only* method available during
   hibernation and aestivation; over the year it accounts for most of the total
   gas exchange and for almost all carbon-dioxide loss.
2. **Buccopharyngeal**, across the moist lining of the buccal cavity, used at
   rest on land with the mouth shut and the throat visibly fluttering.
3. **Pulmonary**, through the lungs, when the frog is active. Air passes:
   external nares → nasal chambers → internal nares → buccal cavity →
   **glottis** → laryngo-tracheal chamber → bronchi → lungs.

The **lungs** are a pair of thin-walled, elastic, pink, ovoid sacs whose inner
surface is thrown into **septa** dividing it into **alveoli**, each covered by a
capillary network. With **no diaphragm and no movable ribs** the frog cannot
suck air in, so it uses a **buccal force pump**: with the glottis shut the
buccal floor is lowered and air drawn in through the nares; the nares close, the
glottis opens, and raising the buccal floor *forces* air into the lungs. Elastic
recoil drives expiration.

### Blood vascular system

```figure caption="The frog's heart and aortic arches, ventral view."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Ellipse
fig, ax = plt.subplots(figsize=(5.0, 3.8))
RED = "#c0392b"; BLU = "#1d6fb8"; VEN = "#a37ba8"; DK = "#6d332d"

def smooth(pts, k=9, n=300):
    p = np.asarray(pts, float); p = np.vstack([p, p[:1]])
    t = np.linspace(0, 1, len(p)); tf = np.linspace(0, 1, n)
    c = np.c_[np.interp(tf, t, p[:, 0]), np.interp(tf, t, p[:, 1])]
    ker = np.ones(k)/k
    for j in (0, 1):
        pad = np.r_[c[-k:, j], c[:, j], c[:k, j]]
        c[:, j] = np.convolve(pad, ker, mode='same')[k:-k]
    return c

def vessel(pts, col, lw=3.2, z=5):
    p = np.asarray(pts, float)
    ax.plot(p[:, 0], p[:, 1], color=col, lw=lw, zorder=z, solid_capstyle='round',
            solid_joinstyle='round')
    ax.plot(p[:, 0], p[:, 1], color=DK, lw=lw + 0.9, zorder=z - 1,
            solid_capstyle='round', solid_joinstyle='round')

# ---------- sinus venosus, lying on the dorsal surface ----------
ax.add_patch(Polygon([[0.90, 1.42], [2.30, 2.26], [2.55, 1.46], [1.62, 0.80]],
                     closed=True, fc="#c8dcee", ec=BLU, lw=1.0, ls=(0, (3, 2)),
                     zorder=3))

# ---------- great veins ----------
vessel([[3.45, 2.30], [2.60, 2.15], [1.90, 2.02]], "#7aa8d0", 3.0)
vessel([[3.50, 1.55], [2.70, 1.62], [2.00, 1.72]], "#7aa8d0", 3.0)
vessel([[3.45, 0.62], [2.75, 0.95], [2.05, 1.28]], "#7aa8d0", 3.0)
vessel([[-3.55, 1.20], [-2.60, 1.05], [-1.70, 0.86]], "#d98d85", 2.6)
vessel([[-3.55, 0.35], [-2.60, 0.58], [-1.70, 0.74]], "#d98d85", 2.6)

# ---------- atria ----------
ax.add_patch(Ellipse((-0.70, 0.66), 1.45, 1.32, angle=-8, fc="#d9877f", ec=DK,
                     lw=1.2, zorder=6))
ax.add_patch(Ellipse((0.78, 0.70), 1.62, 1.42, angle=8, fc="#93b6d8", ec=DK,
                     lw=1.2, zorder=6))
ax.plot([0.02, 0.06], [1.30, -0.05], color=DK, lw=0.9, zorder=8)

# ---------- ventricle ----------
ven = smooth([[-1.28, -0.10], [-1.26, -1.10], [-0.85, -2.10], [0.10, -2.92],
              [1.02, -2.05], [1.36, -1.05], [1.32, -0.10]], k=15, n=320)
ax.add_patch(Polygon(ven, closed=True, fc=VEN, ec=DK, lw=1.3, zorder=5))
for u in np.linspace(-0.75, 0.80, 6):
    ax.plot([u*1.20, 0.10 + u*0.34], [-0.30, -2.40], color="#8a6490", lw=0.5,
            zorder=6, alpha=0.8)

# ---------- truncus (conus) arteriosus and the aortic trunks ----------
vessel([[0.82, -0.55], [0.40, 0.10], [0.00, 0.80], [-0.30, 1.48]], "#c47b74", 4.6, z=9)
ax.plot([0.60, -0.14], [-0.18, 1.18], color="#8c4b44", lw=1.0, zorder=11,
        ls=(0, (3, 2)))
vessel([[-0.32, 1.52], [-1.05, 1.92], [-1.62, 2.18]], "#c47b74", 3.4, z=9)
vessel([[-0.28, 1.52], [0.45, 1.98], [1.00, 2.28]], "#c47b74", 3.4, z=9)

for base, tips, cols in [((-1.62, 2.18),
                          [(-2.30, 3.62), (-3.15, 2.92), (-3.30, 1.96)],
                          [RED, RED, BLU]),
                         ((1.00, 2.28),
                          [(1.50, 3.72), (2.35, 3.22), (2.90, 2.58)],
                          [RED, RED, BLU])]:
    for tip, col in zip(tips, cols):
        mid = ((base[0] + tip[0])/2 + 0.10*(tip[1] - base[1]),
               (base[1] + tip[1])/2)
        vessel([list(base), list(mid), list(tip)], col, 2.6, z=8)

def lab(txt, tip, tx, ty, ha='center', fs=6.0):
    ax.annotate(txt, xy=tip, xytext=(tx, ty), fontsize=fs, color=INK, ha=ha,
                va='center', zorder=18,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.75,
                                shrinkA=1.4, shrinkB=1.0))

lab("carotid arch\n(to the head)", (-2.42, 3.40), -3.60, 4.05, ha='right')
lab("systemic arch\n(to the body)", (-3.05, 2.88), -3.90, 3.00, ha='right')
lab("pulmocutaneous arch\n(to lungs and skin)", (-3.20, 2.00), -3.90, 1.95, ha='right')
lab("pulmonary veins\n(from the lungs)", (-3.10, 1.12), -3.90, 0.85, ha='right')
lab("left atrium", (-1.05, 0.55), -3.90, -0.15, ha='right')
lab("ventricle: single,\nthick and muscular", (-1.05, -1.25), -3.90, -1.55, ha='right')
lab("apex of the ventricle", (0.10, -2.84), -2.50, -3.05, ha='right')

lab("carotid arch", (1.42, 3.55), 3.35, 4.05, ha='left')
lab("systemic arch", (2.25, 3.10), 3.35, 3.40, ha='left')
lab("two precaval veins", (2.90, 2.24), 3.70, 2.70, ha='left')
lab("postcaval vein", (3.05, 0.82), 3.70, 0.85, ha='left')
lab("sinus venosus (on the\ndorsal surface)", (1.62, 1.55), 3.70, 1.75, ha='left')
lab("right atrium", (1.35, 0.55), 3.70, 0.05, ha='left')
lab("truncus arteriosus,\ncontaining the spiral valve", (0.52, -0.10), 3.70, -1.30,
    ha='left')

ax.text(0.10, -4.05, "ventral view; the atria are completely separated but the\n"
                     "ventricle is undivided, so blood is partly mixed",
        ha='center', fontsize=6.0, color=MUTED, style='italic')

ax.set_xlim(-7.30, 7.30); ax.set_ylim(-5.20, 5.30)
ax.set_aspect('equal'); ax.axis('off')
```

The system is closed, with a **three-chambered heart** — two atria and one
undivided ventricle — in a pericardial cavity, plus two accessory chambers: the
thin-walled **sinus venosus** on the dorsal surface, which receives the two
precaval veins and the postcaval vein and delivers to the right atrium, and the
**truncus arteriosus** leaving the ventricle, which contains a **spiral valve**.

Deoxygenated blood reaches the right atrium through the sinus venosus;
oxygenated blood from the lungs reaches the left atrium through the **pulmonary
veins**; both empty into the single ventricle. Complete mixing is avoided by the
muscular trabeculae of the ventricle and by the spiral valve, which steers the
most deoxygenated blood into the **pulmocutaneous arch** (to lungs and skin),
mixed blood into the **systemic arch** (to the body) and the best-oxygenated
blood into the **carotid arch** (to the brain). Mixing is reduced but not
abolished, so the frog's double circulation is **incomplete**.

```figure caption="Double but incomplete circulation in the frog."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse, Patch
fig, ax = plt.subplots(figsize=(5.2, 3.2))
RED = "#c0392b"; BLU = "#1d6fb8"; MIX = "#7d5a94"

def box(cx, cy, w, h, txt, fc, ec, fs=6.2, tc=INK, r=0.16, z=5):
    ax.add_patch(FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                                boxstyle=f"round,pad=0.02,rounding_size={r}",
                                fc=fc, ec=ec, lw=1.1, zorder=z))
    ax.text(cx, cy, txt, ha='center', va='center', fontsize=fs, color=tc,
            zorder=z + 1)

def arrow(p0, p1, col, rad=0.0, lw=1.6, z=6):
    ax.annotate('', xy=p1, xytext=p0, zorder=z,
                arrowprops=dict(arrowstyle='-|>', color=col, lw=lw,
                                mutation_scale=10,
                                connectionstyle=f"arc3,rad={rad}"))

# ---------------- heart outline ----------------
ax.add_patch(FancyBboxPatch((-2.05, -2.35), 4.10, 4.90,
                            boxstyle="round,pad=0.02,rounding_size=0.30",
                            fc="#fbf4f3", ec=MUTED, lw=0.9, ls=(0, (4, 3)),
                            zorder=2))
ax.text(0.00, 2.86, "HEART", ha='center', fontsize=6.8, color=MUTED,
        fontweight='bold')

box(0.60, 1.95, 1.90, 0.52, "sinus venosus", "#c8dcee", BLU, fs=6.0)
ax.add_patch(Ellipse((-0.88, 1.00), 1.55, 0.95, fc="#f0c6c1", ec=RED, lw=1.1,
                     zorder=5))
ax.text(-0.88, 1.00, "left\natrium", ha='center', va='center', fontsize=6.0,
        color=INK, zorder=6)
ax.add_patch(Ellipse((0.88, 1.00), 1.55, 0.95, fc="#c8dcee", ec=BLU, lw=1.1,
                     zorder=5))
ax.text(0.88, 1.00, "right\natrium", ha='center', va='center', fontsize=6.0,
        color=INK, zorder=6)
box(0.00, -0.45, 3.30, 1.05, "VENTRICLE (single)", "#d9cbe2", MIX, fs=6.2)
box(0.00, -1.75, 2.40, 0.58, "truncus arteriosus", "#d9cbe2", MIX, fs=6.0)

# ---------------- systemic and pulmonary circuits ----------------
box(-4.55, 0.00, 2.30, 1.10, "LUNGS\nand SKIN", "#cfe3d4", "#2e8b57", fs=6.4)
box(4.55, 0.00, 2.30, 1.10, "BODY\nTISSUES", "#f2e3c4", "#9a7330", fs=6.4)

arrow((4.55, 0.60), (1.62, 2.02), BLU, rad=-0.28)
arrow((0.60, 1.66), (0.88, 1.52), BLU, rad=0.0, lw=1.4)
arrow((0.88, 0.50), (0.62, 0.12), BLU, rad=0.0, lw=1.4)
arrow((-0.88, 0.50), (-0.62, 0.12), RED, rad=0.0, lw=1.4)
arrow((0.00, -1.00), (0.00, -1.42), MIX, rad=0.0, lw=1.6)
arrow((-1.24, -1.85), (-4.55, -0.62), BLU, rad=-0.26)
arrow((-4.55, 0.60), (-1.70, 1.05), RED, rad=-0.26)
arrow((1.24, -1.85), (4.55, -0.62), RED, rad=0.26)

ax.text(3.45, 2.52, "precaval and postcaval\nveins", ha='center', fontsize=5.9,
        color=BLU)
ax.text(-3.30, 2.18, "pulmonary veins", ha='center', fontsize=5.9, color=RED)
ax.text(-3.05, -2.62, "pulmocutaneous arch", ha='center', fontsize=5.9, color=BLU)
ax.text(3.05, -2.62, "carotid and systemic arches", ha='center', fontsize=5.9,
        color=RED)
ax.text(0.00, 3.52, "Pulmonary circuit (left)  and  systemic circuit (right):\n"
                    "blood passes through the heart twice in one complete round",
        ha='center', fontsize=6.2, color=INK)

leg = [Patch(fc="#f0c6c1", ec=RED, label="oxygenated blood"),
       Patch(fc="#c8dcee", ec=BLU, label="deoxygenated blood"),
       Patch(fc="#d9cbe2", ec=MIX, label="mixed blood")]
ax.legend(handles=leg, loc='lower center', bbox_to_anchor=(0.5, -0.03), ncol=3,
          fontsize=5.9, frameon=False, handlelength=1.1, handleheight=0.9,
          columnspacing=1.4, handletextpad=0.5)

ax.set_xlim(-6.30, 6.30); ax.set_ylim(-4.40, 4.30)
ax.set_aspect('equal'); ax.axis('off')
```

The blood has plasma and three kinds of corpuscle: **nucleated, oval, biconvex
red cells** (unlike a mammal's enucleate discs), white cells and spindle cells.
Both a **hepatic portal** and a **renal portal** system are present, and the
lymphatic system has contractile **lymph hearts**.

::: example
**How fast does the blood go round?** A frog's heart beats 50 times a minute and
ejects 0.20 mL at each beat; the total blood volume is 5.0 mL. How long does one
complete turnover take?

The cardiac output is the stroke volume times the rate,

$$ Q = 0.20\ \text{mL} \times 50\ \text{min}^{-1} = 10\ \text{mL min}^{-1} $$

and the turnover time is the blood volume divided by that output,

$$ t = \frac{V}{Q} = \frac{5.0}{10}\ \text{min} = 0.50\ \text{min} = 30\ \text{s} $$

Thirty seconds; a resting human takes about 60 s (5 L per minute against 5 L of
blood). The frog's small size and low metabolic rate let it manage with a
three-chambered heart; a bird or mammal running a warm body at ten times the
metabolic rate needs a four-chambered heart that keeps the two circuits
separate.
:::

### Excretory system and osmoregulation

```figure caption="Urinogenital system: (a) male, (b) female frog."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Ellipse, FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.2, 4.4))
KID = "#9c4a44"; KEDG = "#632b27"; FAT = "#e8cd72"; FEDG = "#9a8330"
TUB = "#e3d0b4"; TEDG = "#8a6a45"; OV = "#5a5f66"

def lab(txt, tip, tx, ty, ha='center', fs=6.0):
    ax.annotate(txt, xy=tip, xytext=(tx, ty), fontsize=fs, color=INK, ha=ha,
                va='center', zorder=20,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7,
                                shrinkA=1.3, shrinkB=1.0))

def base(XC):
    """Kidneys, adrenals, fat bodies, cloaca and bladder: common to both sexes."""
    for s in (1, -1):
        ax.add_patch(FancyBboxPatch((XC + s*0.62 - 0.30, -1.60), 0.60, 3.45,
                                    boxstyle="round,pad=0.01,rounding_size=0.26",
                                    fc=KID, ec=KEDG, lw=1.1, zorder=5))
        ax.add_patch(FancyBboxPatch((XC + s*0.62 - 0.10, -1.35), 0.20, 2.90,
                                    boxstyle="round,pad=0.01,rounding_size=0.09",
                                    fc="#e6c463", ec="#8a6a12", lw=0.7, zorder=6))
        for k, a in enumerate(np.linspace(58, 122, 5)):
            r = np.radians(a if s > 0 else 180 - a)
            ax.plot([XC + s*0.72, XC + s*0.72 + 1.15*np.cos(r)],
                    [2.00, 2.00 + 1.15*np.sin(r)], color=FAT, lw=3.4, zorder=4,
                    solid_capstyle='round')
            ax.plot([XC + s*0.72, XC + s*0.72 + 1.15*np.cos(r)],
                    [2.00, 2.00 + 1.15*np.sin(r)], color=FEDG, lw=0.5, zorder=5,
                    alpha=0.5)
        ax.plot([XC + s*0.62, XC + s*0.62, XC + s*0.16, XC],
                [-1.60, -2.35, -3.05, -3.30], color=TUB, lw=3.0, zorder=5,
                solid_capstyle='round', solid_joinstyle='round')
        ax.plot([XC + s*0.62, XC + s*0.62, XC + s*0.16, XC],
                [-1.60, -2.35, -3.05, -3.30], color=TEDG, lw=0.6, zorder=6,
                alpha=0.6)
    ax.add_patch(Ellipse((XC, -3.52), 0.80, 0.56, fc="#d7ab7e", ec=TEDG, lw=1.1,
                         zorder=8))
    for s in (1, -1):
        ax.add_patch(Ellipse((XC + s*0.44, -4.42), 0.86, 0.94, fc="#cfe0ee",
                             ec="#2c5f96", lw=1.0, zorder=7))
    ax.plot([XC, XC], [-3.78, -4.10], color="#2c5f96", lw=1.6, zorder=8)

# ===================== (a) male =====================
XM = -3.45
base(XM)
for s in (1, -1):
    ax.add_patch(Ellipse((XM + s*0.42, 0.78), 0.56, 0.92, angle=-s*8,
                         fc="#f0e2c2", ec=TEDG, lw=1.1, zorder=9))
    for yy in (1.05, 0.80, 0.55):
        ax.plot([XM + s*0.58, XM + s*0.76], [yy, yy + 0.06], color="#c9a271",
                lw=0.9, zorder=10)
    ax.add_patch(Ellipse((XM + s*0.62, -2.20), 0.40, 0.58, fc="#e9d6b4",
                         ec=TEDG, lw=0.9, zorder=7))
ax.text(XM, 5.05, "(a)  male", ha='center', fontsize=7.4, color=INK)

lab("fat bodies", (XM - 1.35, 2.70), -5.35, 4.20, ha='right')
lab("testis", (XM - 0.66, 0.90), -5.35, 3.30, ha='right')
lab("vasa efferentia", (XM - 0.70, 0.55), -5.35, 2.40, ha='right')
lab("kidney", (XM - 0.86, 0.20), -5.35, 1.50, ha='right')
lab("adrenal gland", (XM - 0.68, -0.60), -5.35, 0.60, ha='right')
lab("urinogenital duct", (XM - 0.66, -1.90), -5.35, -0.30, ha='right')
lab("seminal vesicle", (XM - 0.80, -2.20), -5.35, -1.25, ha='right')
lab("cloaca", (XM - 0.38, -3.52), -5.35, -2.25, ha='right')
lab("urinary bladder", (XM - 0.82, -4.45), -5.35, -3.35, ha='right')

# ===================== (b) female =====================
XF = 3.45
base(XF)
rng = np.random.default_rng(5)
for s in (1, -1):
    # ovary: a lobed mass packed with eggs
    lobe = []
    for a in np.linspace(0, 2*np.pi, 300):
        r = 0.86 + 0.20*np.sin(5*a) + 0.06*np.sin(9*a)
        lobe.append([XF + s*1.48 + r*np.cos(a)*0.78, 0.62 + r*np.sin(a)*1.20])
    ax.add_patch(Polygon(lobe, closed=True, fc="#c9c3b4", ec="#5f5a50", lw=1.0,
                         zorder=9))
    for k in range(26):
        rr = 0.82*np.sqrt(rng.random()); th = 2*np.pi*rng.random()
        ax.add_patch(Circle((XF + s*1.48 + 0.72*rr*np.cos(th),
                             0.62 + 1.10*rr*np.sin(th)), 0.085, fc=OV,
                            ec='none', zorder=10))
    # oviduct: long, much-coiled tube lateral to the kidney
    yy = np.linspace(-2.05, 2.55, 400)
    xx = XF + s*(1.05 + 0.20*np.sin(7.0*yy))
    ax.plot(xx, yy, color="#e8b9a8", lw=2.6, zorder=6, solid_capstyle='round')
    ax.plot(xx, yy, color="#a2453e", lw=0.5, zorder=7, alpha=0.6)
    ax.add_patch(Circle((XF + s*1.05, 2.62), 0.15, fc="#f3d9cf", ec="#a2453e",
                        lw=0.9, zorder=8))
    # ovisac: dilated posterior end opening into the cloaca
    ax.add_patch(Ellipse((XF + s*0.98, -2.35), 0.52, 0.72, fc="#f0cec2",
                         ec="#a2453e", lw=1.0, zorder=8))
    ax.plot([XF + s*0.98, XF + s*0.25], [-2.68, -3.30], color="#f0cec2", lw=2.4,
            zorder=6, solid_capstyle='round')
ax.text(XF, 5.05, "(b)  female", ha='center', fontsize=7.4, color=INK)

lab("fat bodies", (XF + 1.30, 2.75), 6.30, 4.20, ha='left')
lab("ostium of the oviduct", (XF + 1.18, 2.66), 6.30, 3.30, ha='left')
lab("ovary packed with eggs", (XF + 2.10, 0.80), 6.30, 2.40, ha='left')
lab("kidney", (XF + 0.80, 0.10), 6.30, 1.50, ha='left')
lab("coiled oviduct", (XF + 1.22, -0.60), 6.30, 0.60, ha='left')
lab("ureter", (XF + 0.66, -1.95), 6.30, -0.30, ha='left')
lab("ovisac", (XF + 1.22, -2.35), 6.30, -1.25, ha='left')
lab("cloaca", (XF + 0.38, -3.52), 6.30, -2.25, ha='left')
lab("urinary bladder", (XF + 0.84, -4.45), 6.30, -3.35, ha='left')

ax.set_xlim(-9.60, 11.20); ax.set_ylim(-6.20, 5.60)
ax.set_aspect('equal'); ax.axis('off')
```

A pair of dark-red, flattened **mesonephric kidneys** lies against the dorsal
body wall beside the vertebral column, each with a narrow yellow **adrenal
gland** along its ventral surface and built of many uriniferous tubules
beginning in Malpighian corpuscles.

Urine leaves by a **ureter** opening dorsally into the **cloaca**. In the
**male** the same duct also carries sperm and is therefore the **urinogenital
duct** — the reason the two systems are described together. A thin-walled
bilobed **urinary bladder** opens ventrally into the cloaca, not into the
ureters, so urine enters it from the cloaca and water can be reabsorbed on land.

The adult is **ureotelic**, excreting urea, far less toxic than ammonia and much
cheaper in water; the aquatic tadpole is **ammonotelic**. The switch at
metamorphosis is a neat case of excretion matching habitat.

### Nervous system and sense organs

```figure caption="Frog's brain: (a) dorsal, (b) ventral view."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Ellipse, FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.0, 4.2))
BR = "#e7d3b9"; BR2 = "#d9bd98"; BR3 = "#cfae86"; EDGE = "#7d6244"

def lab(txt, tip, tx, ty, ha='center', fs=6.0):
    ax.annotate(txt, xy=tip, xytext=(tx, ty), fontsize=fs, color=INK, ha=ha,
                va='center', zorder=18,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.75,
                                shrinkA=1.4, shrinkB=1.0))

def common(XC):
    """Parts that look the same from above and from below."""
    for s in (1, -1):
        ax.add_patch(Ellipse((XC + s*0.27, 3.08), 0.54, 0.66, fc=BR2, ec=EDGE,
                             lw=1.0, zorder=5))
        ax.add_patch(Ellipse((XC + s*0.36, 1.98), 0.76, 1.68, fc=BR, ec=EDGE,
                             lw=1.1, zorder=5))
    ax.add_patch(Polygon([[XC - 0.72, -0.88], [XC + 0.72, -0.88],
                          [XC + 0.36, -2.34], [XC - 0.36, -2.34]], closed=True,
                         fc=BR2, ec=EDGE, lw=1.1, zorder=5))
    ax.add_patch(FancyBboxPatch((XC - 0.20, -3.34), 0.40, 1.04,
                                boxstyle="round,pad=0.01,rounding_size=0.12",
                                fc=BR3, ec=EDGE, lw=1.0, zorder=4))

# ================= (a) dorsal view =================
XA = -2.85
common(XA)
ax.add_patch(Polygon([[XA - 0.56, 1.24], [XA + 0.56, 1.24], [XA + 0.50, 0.44],
                      [XA - 0.50, 0.44]], closed=True, fc=BR3, ec=EDGE, lw=1.0,
                     zorder=6))
ax.add_patch(Circle((XA, 0.94), 0.10, fc="#8e6fa8", ec=INK, lw=0.7, zorder=8))
for s in (1, -1):
    ax.add_patch(Ellipse((XA + s*0.44, 0.04), 0.84, 0.94, fc=BR2, ec=EDGE, lw=1.1,
                         zorder=7))
ax.add_patch(FancyBboxPatch((XA - 0.74, -0.86), 1.48, 0.30,
                            boxstyle="round,pad=0.01,rounding_size=0.12",
                            fc=BR3, ec=EDGE, lw=1.0, zorder=7))
ax.add_patch(Polygon([[XA, -1.02], [XA + 0.42, -1.55], [XA, -2.12],
                      [XA - 0.42, -1.55]], closed=True, fc="#f4ece0", ec=EDGE,
                     lw=0.8, ls=(0, (3, 2)), zorder=6))
ax.text(XA, 4.62, "(a)  dorsal view", ha='center', fontsize=7.2, color=INK)

lab("olfactory lobes", (XA - 0.48, 3.16), -4.60, 4.00, ha='right')
lab("cerebral hemispheres", (XA - 0.68, 2.20), -4.60, 3.10, ha='right')
lab("pineal body", (XA - 0.10, 0.98), -4.60, 2.20, ha='right')
lab("diencephalon", (XA - 0.52, 0.72), -4.60, 1.30, ha='right')
lab("optic lobes", (XA - 0.78, 0.04), -4.60, 0.40, ha='right')
lab("cerebellum", (XA - 0.70, -0.72), -4.60, -0.50, ha='right')
lab("fourth ventricle", (XA - 0.30, -1.55), -4.60, -1.40, ha='right')
lab("medulla oblongata", (XA - 0.62, -1.15), -4.60, -2.30, ha='right')
lab("spinal cord", (XA - 0.20, -2.95), -4.60, -3.20, ha='right')

# ================= (b) ventral view =================
XB = 2.85
common(XB)
ax.add_patch(Polygon([[XB - 0.56, 1.24], [XB + 0.56, 1.24], [XB + 0.50, 0.10],
                      [XB - 0.50, 0.10]], closed=True, fc=BR3, ec=EDGE, lw=1.0,
                     zorder=3))
for s in (1, -1):
    ax.add_patch(Ellipse((XB + s*0.50, -0.20), 0.80, 0.86, fc=BR2, ec=EDGE,
                         lw=1.0, zorder=4))
# optic chiasma
for s in (1, -1):
    ax.plot([XB - s*0.86, XB + s*0.50], [1.32, 0.66], color="#d8b25e",
            lw=2.6, zorder=7, solid_capstyle='round')
ax.add_patch(Circle((XB, 0.99), 0.13, fc="#d8b25e", ec="#8a6a12", lw=0.7, zorder=8))
# infundibulum and pituitary body
ax.add_patch(FancyBboxPatch((XB - 0.13, 0.18), 0.26, 0.40,
                            boxstyle="round,pad=0.01,rounding_size=0.08",
                            fc=BR3, ec=EDGE, lw=0.9, zorder=8))
ax.add_patch(Ellipse((XB, -0.08), 0.60, 0.44, fc="#c49fd0", ec="#6a4a78", lw=1.0,
                     zorder=9))
# stubs of cranial nerves leaving the medulla
for s in (1, -1):
    for yy, ln in [(-1.05, 0.52), (-1.42, 0.50), (-1.78, 0.46), (-2.12, 0.42)]:
        x0 = XB + s*np.interp(yy, [-2.34, -0.88], [0.36, 0.72])
        ax.plot([x0, x0 + s*ln], [yy, yy - 0.16], color="#d8b25e", lw=1.2,
                zorder=6, solid_capstyle='round')
ax.text(XB, 4.62, "(b)  ventral view", ha='center', fontsize=7.2, color=INK)

lab("olfactory lobes", (XB + 0.48, 3.16), 4.60, 4.00, ha='left')
lab("cerebral hemispheres", (XB + 0.68, 2.20), 4.60, 3.10, ha='left')
lab("optic nerve", (XB + 0.72, 0.84), 4.60, 2.20, ha='left')
lab("optic chiasma", (XB + 0.14, 1.02), 4.60, 1.30, ha='left')
lab("infundibulum", (XB + 0.14, 0.40), 4.60, 0.40, ha='left')
lab("pituitary body (hypophysis)", (XB + 0.30, -0.12), 4.60, -0.50, ha='left')
lab("optic lobe (seen from below)", (XB + 0.86, -0.32), 4.60, -1.40, ha='left')
lab("cranial nerves", (XB + 1.00, -1.55), 4.60, -2.30, ha='left')
lab("spinal cord", (XB + 0.20, -2.95), 4.60, -3.20, ha='left')

ax.set_xlim(-8.40, 8.40); ax.set_ylim(-5.10, 5.30)
ax.set_aspect('equal'); ax.axis('off')
```

The nervous system has a **central** part (brain and spinal cord), a
**peripheral** part (**10 pairs of cranial nerves** and 10 pairs of spinal
nerves) and an **autonomic** part. The brain lies in the cranium in two meninges
and has three regions.

- **Forebrain:** a pair of small **olfactory lobes**, a pair of elongated
  **cerebral hemispheres**, and the **diencephalon**, roofed by the **pineal
  body** and bearing on its floor the **optic chiasma**, the **infundibulum**
  and the **pituitary body**.
- **Midbrain:** a pair of large rounded **optic lobes**, the main visual
  centres — far more prominent than in a mammal, where sight has moved to the
  cortex.
- **Hindbrain:** a small transverse **cerebellum** for balance and coordination,
  small because the frog makes few complex movements; and the **medulla
  oblongata**, holding the centres for respiration, heartbeat and digestion,
  which narrows behind into the **spinal cord**.

Sense organs are well developed: eyes with a nictitating membrane; ears with a
tympanum, a middle ear containing the rod-like **columella**, and an internal
ear with semicircular canals; olfactory epithelium; taste buds; and skin
receptors. The tadpole also has a **lateral line system**, lost at
metamorphosis.

### Reproductive system and life history

The frog is **dioecious**, with external fertilisation and indirect development.

**Male.** A pair of pale-yellow oval **testes** is attached to the ventral
surface of the kidneys by the **mesorchium**. Ten to twelve **vasa efferentia**
carry sperm into the kidney, where they join **Bidder's canal** and then the
**urinogenital duct**; a dilation of the duct serves as a **seminal vesicle**.
Yellow finger-like **fat bodies** store food for the breeding season.

**Female.** A pair of large lobed **ovaries** lies near the kidneys, attached by
the **mesovarium** but *not* joined to them. Ova are shed into the coelom and
picked up by the funnel-shaped **ostium** of a long coiled **oviduct**, whose
hind end dilates into an **ovisac** opening separately into the cloaca. A mature
female sheds 2500 to 3000 eggs at a time.

**Breeding and development.** Breeding follows the first heavy monsoon rain.
The male grips the female behind the forelimbs with his nuptial pads —
**amplexus** — which stimulates her to shed her eggs into the water; he sheds
sperm over them at once, so **fertilisation is external**. The jelly-coated eggs
hatch in a few days into a **tadpole**, utterly unlike its parent: herbivorous,
with horny jaws, a long coiled gut, a finned tail, first external and then
internal **gills**, a **two-chambered** heart, a lateral line and no limbs.
**Metamorphosis**, controlled by **thyroxine**, converts it into a frog in about
two months. *Progressive* changes: hindlimbs then forelimbs, lungs, eyelids and
tympanum, a three-chambered heart, and a shortened gut. *Retrogressive*
changes: tail, gills, horny jaws and lateral line are digested away by lysosomal
enzymes.

::: caution
Amplexus is **not** copulation. The male never introduces sperm into the female;
he merely clasps her so that eggs and sperm are shed into the same small volume
of water at the same moment. Calling amplexus "internal fertilisation", or the
frog's development "direct", loses the mark.
:::

### Economic importance

Frogs eat enormous numbers of insects, including paddy pests and the mosquitoes
that carry malaria and dengue, and are among the best agents of **biological
pest control** in Nepalese farmland. Export as frog legs is now restricted,
because over-collection caused insect outbreaks and heavier pesticide use. They
remain a standard laboratory animal, and because their permeable skin absorbs
whatever is in the water they are sensitive **bio-indicators** of pollution.

## Chapter summary

- Protista holds the eukaryotes that are neither plant, animal nor fungus; the
  Protozoa are classified by locomotory organelle into Rhizopoda, Mastigophora,
  Sporozoa and Ciliata.
- *Paramecium caudatum* is a slipper-shaped ciliate with a pellicle,
  trichocysts, two contractile vacuoles, a macronucleus and a micronucleus; it
  swims by a metachronal wave, filter feeds, divides by transverse binary
  fission and reorganises its nuclei by conjugation.
- Animals are classified by level of organisation, body plan, symmetry, germ
  layers, coelom and segmentation: Porifera cellular, Coelenterata diploblastic
  and radial, Platyhelminthes acoelomate, Nemathelminthes pseudocoelomate,
  Annelida onwards truly coelomate. Chordata is defined by a notochord, a dorsal
  hollow nerve cord, pharyngeal gill slits and a post-anal tail.
- *Pheretima posthuma* has a clitellum on segments 14–16, perichaetine setae, a
  gizzard, calciferous glands, caeca at segment 26 and a typhlosole, four pairs
  of hearts in a closed circulation, three kinds of nephridia and a solid
  ventral nerve cord. It is hermaphrodite but cross-fertilising, with external
  fertilisation inside the cocoon.
- *Rana tigrina* breathes cutaneously, buccopharyngeally and through lungs
  worked by a buccal force pump; its three-chambered heart with a spiral valve
  gives a double but incomplete circulation. It is ureotelic, with mesonephric
  kidneys and a shared urinogenital duct in the male; fertilisation is external
  after amplexus, and thyroxine-driven metamorphosis reverses almost every
  larval character.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The locomotory organelle of an adult sporozoan is <span class="marks">[1]</span>
   (a) cilia (b) flagella (c) pseudopodia (d) none

2. *Paramecium caudatum* possesses <span class="marks">[1]</span>
   (a) one micronucleus (b) two micronuclei (c) many micronuclei (d) no micronucleus

3. Flame cells are the excretory structures of <span class="marks">[1]</span>
   (a) Annelida (b) Platyhelminthes (c) Mollusca (d) Echinodermata

4. The pseudocoelomate phylum among the following is <span class="marks">[1]</span>
   (a) Platyhelminthes (b) Nemathelminthes (c) Annelida (d) Arthropoda

5. The water vascular system with tube feet is characteristic of <span class="marks">[1]</span>
   (a) Mollusca (b) Arthropoda (c) Echinodermata (d) Chordata

6. In *Pheretima posthuma* the setae of one segment number about <span class="marks">[1]</span>
   (a) 4 (b) 8 (c) 80–120 (d) 800

7. The number of pairs of hearts in the earthworm is <span class="marks">[1]</span>
   (a) two (b) three (c) four (d) five

8. The spiral valve of the frog lies in the <span class="marks">[1]</span>
   (a) sinus venosus (b) truncus arteriosus (c) ventricle (d) left atrium

::: note Answers to Group A
**1.** (d) — adult sporozoans glide. **2.** (a) — *P. aurelia* has two.
**3.** (b) — flame cells terminate the protonephridia of flatworms. **4.** (b) —
the cavity of *Ascaris* is a persistent blastocoel, unlined on the gut side.
**5.** (c). **6.** (c) — *Pheretima* is perichaetine. **7.** (c) — lateral
hearts in 7 and 9, latero-oesophageal in 12 and 13. **8.** (b) — it steers blood
into the three aortic arches.
:::

**Group B — Short answer questions (4 marks each)**

1. Distinguish between acoelomate, pseudocoelomate and coelomate animals, giving
   one example of each. <span class="marks">[4]</span>

2. How does *Paramecium* keep its water content constant in pond water?
   <span class="marks">[4]</span>

3. State four diagnostic characters of phylum Arthropoda and name two examples.
   <span class="marks">[4]</span>

4. List the external apertures of *Pheretima posthuma* with their positions.
   <span class="marks">[4]</span>

5. Describe the three types of nephridia found in the earthworm.
   <span class="marks">[4]</span>

6. The earthworm is hermaphrodite, yet it cannot fertilise itself, and its
   fertilisation is external. Explain. <span class="marks">[4]</span>

7. Explain the three modes of respiration in the frog and state when each is
   used. <span class="marks">[4]</span>

8. Summarise the progressive and retrogressive changes that occur during the
   metamorphosis of a tadpole. <span class="marks">[4]</span>

::: note Answers to Group B
**1.** Acoelomate — no body cavity, the space packed with mesodermal parenchyma
(*Planaria*). Pseudocoelomate — a cavity present but a persistent blastocoel,
lined by mesoderm on the body-wall side only (*Ascaris*). Coelomate — a true
coelom within the mesoderm, lined by peritoneum on both body wall and gut
(*Pheretima*).

**2.** Pond water is hypotonic, so water enters by osmosis. Two contractile
vacuoles, each fed by radiating canals, collect it and discharge through a
temporary pore, contracting alternately every 10–20 s. Their role is
osmoregulation, not excretion: ammonia leaves by diffusion.

**3.** (i) Jointed appendages. (ii) A chitinous exoskeleton that is moulted
(ecdysis). (iii) A haemocoel with an open circulation. (iv) Segmented body,
typically head, thorax and abdomen, with compound eyes. Examples: *Periplaneta
americana*, *Palaemon*.

**4.** Mouth on the peristomium (segment 1); anus on the last segment; female
genital pore mid-ventral on segment 14; one pair of male genital pores on
segment 18; four pairs of spermathecal pores in grooves 5/6, 6/7, 7/8 and 8/9;
many nephridiopores; mid-dorsal pores from groove 12/13 backwards.

**5.** Septal nephridia, on both faces of the septa from segment 15 backwards,
open into the intestine (enteronephric). Integumentary nephridia, on the inner
body wall from segment 3 back and most numerous in the clitellum, open on the
skin (exonephric). Pharyngeal nephridia form three paired tufts in segments
4–6, lack nephrostomes and open into the buccal cavity and pharynx.

**6.** Both sets of gonads occur in one worm, but it is protandrous — sperm
mature before the ova of the same animal — so cross-fertilisation is
obligatory. During copulation each worm charges the other's spermathecae. Later
the clitellum secretes a cocoon; as the worm backs out, the cocoon collects ova
at segment 14 and stored sperm at segments 6–9, so the gametes meet inside the
cocoon, outside both parents.

**7.** Cutaneous respiration through the moist vascular skin works in water and
air, is the only method during hibernation and aestivation, and accounts for
most of the year's gas exchange. Buccopharyngeal respiration across the buccal
lining is used at rest on land. Pulmonary respiration serves the active animal,
air being driven in by a buccal force pump.

**8.** Progressive: hindlimbs then forelimbs; lungs replace gills; eyelids and a
tympanum appear; the heart becomes three-chambered; the gut shortens; excretion
shifts from ammonotelic to ureotelic. Retrogressive: tail, gills, horny jaws and
lateral line are digested away by lysosomal enzymes. Thyroxine triggers the
change, which takes about two months.
:::

**Group C — Long answer questions (8 marks each)**

1. Describe the structure of *Paramecium caudatum* with a labelled diagram, and
   explain how it obtains and digests its food. <span class="marks">[8]</span>

2. On what characters is Kingdom Animalia classified? Name the nine phyla in
   order of increasing complexity and give two diagnostic characters and one
   example of each. <span class="marks">[8]</span>

3. Describe the digestive system of *Pheretima posthuma* with a labelled
   diagram, and add a note on the typhlosole and the intestinal caeca.
   <span class="marks">[8]</span>

4. Describe the structure of the frog's heart with a labelled diagram, trace
   the course of blood through it, and explain why the frog's double
   circulation is said to be incomplete. <span class="marks">[8]</span>

::: note Answers to Group C
**1.** *Structure* — slipper-shaped ciliate, 170–330 μm; pellicle sculptured
into hexagons with one cilium each and longer caudal cilia behind; ectoplasm
with trichocysts; granular endoplasm; oral groove leading to vestibule,
cytostome and cytopharynx, with a cytopyge behind; two contractile vacuoles with
radiating canals; a vegetative macronucleus and a reproductive micronucleus.
Draw and label these. *Nutrition* — holozoic filter feeding: oral-groove cilia
sweep bacteria into the vestibule; a food vacuole forms at the base of the
cytopharynx and circulates by cyclosis; digestion is intracellular, the vacuole
first acidic (about pH 4) then alkaline as proteases, amylases and lipases act;
the residue is egested at the cytopyge.

**2.** *Characters used*: level of organisation; body plan; symmetry; germ
layers; coelom; segmentation and cephalisation. *Phyla*: Porifera — cellular
level, canal system with choanocytes and spicules (*Sycon*); Coelenterata —
radial, diploblastic, cnidoblasts, blind-sac gut (*Hydra*); Platyhelminthes —
flattened, acoelomate, flame cells (*Taenia*); Nemathelminthes — cylindrical,
pseudocoelomate, complete gut (*Ascaris*); Annelida — metameric segmentation,
true coelom, nephridia (*Pheretima*); Arthropoda — jointed appendages, chitinous
exoskeleton, haemocoel (*Periplaneta*); Mollusca — soft unsegmented body with
foot, mantle and shell, radula (*Pila*); Echinodermata — marine, pentamerous
radial adult, water vascular system (*Asterias*); Chordata — notochord, dorsal
hollow nerve cord, gill slits, post-anal tail (*Rana*).

**3.** A straight tube from mouth to anus: buccal cavity 1–3; pharynx 4–5, with
salivary glands secreting mucus and a protease, acting as a suction pump;
oesophagus 5–7; gizzard 8–9, thick, muscular and cuticle-lined, grinding the
food; stomach 9–14, whose calciferous glands neutralise the humic acid of the
soil; intestine from 15 to the last segment; terminal anus. Digestion is
extracellular and the residue leaves as castings. *Note* — the typhlosole is a
deep median infolding of the dorsal intestinal wall from about segment 26,
multiplying the absorptive surface without lengthening the gut; a pair of
conical caeca arises at segment 26, projects forward over segments 22–25 and
secretes amylase. A labelled longitudinal section is required.

**4.** *Structure* — three chambers (two atria, one undivided ventricle) in a
pericardium, plus the thin-walled sinus venosus dorsally, receiving the two
precaval and one postcaval veins, and the truncus arteriosus, which leaves the
ventricle, contains a spiral valve and divides into two aortic trunks giving
carotid, systemic and pulmocutaneous arches. *Course of blood* — deoxygenated
blood from the body enters the sinus venosus and right atrium; oxygenated blood
returns by the pulmonary veins to the left atrium; both empty into the single
ventricle, where trabeculae limit mixing; the spiral valve then directs the most
deoxygenated blood into the pulmocutaneous arch, mixed blood into the systemic
arch and the best-oxygenated blood into the carotid arch. *Why incomplete* —
blood passes through the heart twice in one circuit, so the circulation is
double, but with one ventricle the streams are not kept wholly apart and the
systemic arch carries mixed blood. Only birds and mammals, with a four-chambered
heart, separate them completely.
:::
