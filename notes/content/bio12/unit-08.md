---
subject: Biology
grade: 12
unit: 8
title: Human Biology
hours: 28
area: Zoology
---

Twenty-eight hours — more than a fifth of the whole Grade 12 course — are given
to one animal, *Homo sapiens*. The reason is not vanity. The human body is the
one animal whose physiology you will use every day: when a doctor reads your
blood pressure, when a patient in Bharatpur is put on dialysis, when an
adolescent is taught about the menstrual cycle. This unit works organ system by
organ system. For each one, learn three things in order: the **parts** (gross
anatomy, with a labelled diagram you can reproduce in ten minutes), the
**mechanism** (what each part physically does), and the **numbers** (the normal
values, because a value is what tells a clinician that something is wrong).

::: key What the examiner asks from this unit
Because it is the largest unit, Section II almost always draws one of its two
8-mark long questions from here, plus two or three of its four 4-mark short
questions. Long questions are nearly always "describe the structure of X with a
labelled diagram and explain its working" — so the diagram is half the marks.
Practise drawing the heart, the nephron, the brain and the reproductive systems
until you can label them from memory.
:::

## 8.1 Digestive system

Food as we eat it is made of polymers — starch, protein, triglyceride — whose
molecules are far too large to cross a cell membrane. **Digestion** is the
controlled hydrolysis of those polymers into absorbable monomers, and the
digestive system is a 9-metre tube with glands attached that does the job in
stages.

The human digestive system has two parts: the **alimentary canal** (a continuous
tube from mouth to anus, about 8–10 m long in an adult) and the **associated
digestive glands** (salivary glands, liver with gall bladder, and pancreas),
which lie outside the tube and pour their secretions into it through ducts.

### The alimentary canal

```figure caption="The human alimentary canal with its associated glands (anterior view; the liver is drawn semi-transparent so the stomach behind it is visible)."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Ellipse
from matplotlib.path import Path
from matplotlib.patches import PathPatch

fig, ax = plt.subplots(figsize=(5.0, 4.6))
WALL = "#c98a5e"; LUM = "#f6e2cf"; LIV = "#a4563f"; GLAND = "#d9b36b"
PANC = "#e0c083"; GB = "#7fa86a"

def tube(pts, w=7.4, z=3, c=WALL, l=LUM):
    x, y = np.array(pts).T
    ax.plot(x, y, color=c, lw=w, solid_capstyle='round', zorder=z)
    ax.plot(x, y, color=l, lw=w*0.55, solid_capstyle='round', zorder=z+0.1)

def blob(verts, codes, fc, ec="#8a5a3a", lw=1.0, z=3, alpha=1.0):
    p = PathPatch(Path(verts, codes), fc=fc, ec=ec, lw=lw, zorder=z, alpha=alpha)
    ax.add_patch(p); return p

def lab(txt, tip, tx, ty, ha='left', fs=6.2, c=INK):
    ax.annotate(txt, xy=tip, xytext=(tx, ty), fontsize=fs, color=c, ha=ha,
                va='center', zorder=20,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.65,
                                shrinkA=1.5, shrinkB=1.0))

# ---- head: buccal cavity, tongue, pharynx ----
ax.add_patch(Ellipse((0.0, 9.42), 1.5, 0.78, fc=LUM, ec="#8a5a3a", lw=1.0, zorder=3))
ax.plot([-0.62, 0.55], [9.30, 9.30], color=WALL, lw=2.4, zorder=4,
        solid_capstyle='round')          # tongue
for k in range(7):                        # upper teeth
    ax.plot([-0.62+0.19*k]*2, [9.66, 9.55], color="#f4f1e8", lw=2.0, zorder=5)
tube([(0.0, 9.05), (0.02, 8.80)], w=7.0, z=2)   # pharynx

# ---- oesophagus ----
tube([(0.02, 8.86), (0.06, 8.40), (0.14, 7.95), (0.22, 7.58)], w=5.8, z=2)

# ---- liver (4 lobes, wedge) drawn semi-transparent ----
lv = [(-2.15, 7.30), (-2.00, 8.02), (-1.20, 8.32), (-0.30, 8.28),
      (0.28, 8.02), (0.30, 7.44), (-0.40, 7.02), (-1.30, 6.92), (-2.15, 7.30)]
ax.add_patch(Polygon(lv, closed=True, fc=LIV, ec="#6f3628", lw=1.1,
                     zorder=6, alpha=0.62))
ax.plot([-1.02, -0.92], [8.30, 6.96], color="#6f3628", lw=0.8, zorder=6.1,
        alpha=0.8)                        # falciform ligament
# gall bladder + bile duct
ax.add_patch(Ellipse((-0.78, 6.80), 0.40, 0.26, angle=-20, fc=GB,
                     ec="#4e6b41", lw=0.9, zorder=7))
ax.plot([-0.66, -0.40, -0.30], [6.72, 6.52, 6.20], color="#4e6b41", lw=1.0, zorder=7)

# ---- stomach ----
st = [(0.20, 7.56), (0.58, 7.96), (1.04, 7.90), (1.34, 7.48),
      (1.40, 6.92), (1.20, 6.46), (0.82, 6.26), (0.50, 6.28),
      (0.40, 6.54), (0.46, 6.90), (0.52, 7.18), (0.44, 7.42),
      (0.24, 7.48), (0.20, 7.56)]
ax.add_patch(Polygon(st, closed=True, fc=LUM, ec="#8a5a3a", lw=1.2, zorder=4))
for k in range(5):                        # rugae
    ax.plot([0.62+0.15*k, 0.76+0.15*k], [7.62-0.08*k, 7.36-0.08*k],
            color="#c98a5e", lw=0.6, zorder=4.1)
tube([(0.50, 6.28), (0.24, 6.22), (0.02, 6.20)], w=5.4, z=4)   # pylorus

# ---- duodenum (C-loop) ----
tube([(0.02, 6.20), (-0.44, 6.22), (-0.62, 5.92), (-0.58, 5.54),
      (-0.28, 5.34), (0.14, 5.40), (0.44, 5.62)], w=5.4, z=4)
# ---- pancreas ----
pn = [(-0.32, 5.62), (-0.10, 5.86), (0.42, 6.02), (0.95, 6.16),
      (1.18, 6.22), (1.20, 6.06), (0.80, 5.92), (0.30, 5.74),
      (-0.14, 5.50), (-0.32, 5.62)]
ax.add_patch(Polygon(pn, closed=True, fc=PANC, ec="#a8842f", lw=1.0, zorder=5))
ax.plot([-0.24, 0.30, 0.80], [5.70, 5.86, 6.02], color="#a8842f", lw=0.6, zorder=5.1)

# ---- large intestine frame ----
tube([(-2.10, 1.95), (-2.10, 3.40), (-2.10, 4.86)], w=9.0, z=2.5)   # ascending
tube([(-2.10, 4.92), (-1.60, 5.06), (-0.80, 4.84), (0.0, 4.74),
      (0.90, 4.86), (1.62, 5.06), (2.10, 4.92)], w=9.0, z=2.5)      # transverse
tube([(2.10, 4.86), (2.10, 3.40), (2.10, 1.95)], w=9.0, z=2.5)      # descending
tube([(2.10, 1.98), (1.90, 1.40), (1.20, 1.18), (0.55, 1.30),
      (0.30, 1.08)], w=7.6, z=2.5)                                   # sigmoid
for yy in np.arange(2.25, 4.80, 0.42):                               # haustra
    for sx in (-2.10, 2.10):
        ax.plot([sx-0.155, sx+0.155], [yy, yy], color="#b3784f", lw=0.7, zorder=3.4)
for xx in np.arange(-1.60, 1.90, 0.46):
    yy = np.interp(xx, [-2.10, -1.60, -0.80, 0.0, 0.90, 1.62, 2.10],
                   [4.92, 5.06, 4.84, 4.74, 4.86, 5.06, 4.92])
    ax.plot([xx, xx], [yy-0.155, yy+0.155], color="#b3784f", lw=0.7, zorder=3.4)
tube([(0.26, 1.10), (0.22, 0.58)], w=8.4, z=2.5)                     # rectum
ax.add_patch(Ellipse((0.22, 0.44), 0.30, 0.13, fc="#8a5a3a", ec="#6f3628",
                     lw=0.8, zorder=3))
# caecum + appendix
ax.add_patch(Ellipse((-2.10, 1.76), 0.46, 0.56, fc=LUM, ec="#8a5a3a",
                     lw=1.1, zorder=3))
ax.plot([-1.98, -1.80, -1.86], [1.54, 1.28, 1.04], color=WALL, lw=2.0,
        zorder=3, solid_capstyle='round')

# ---- small intestine coil ----
ysr = [4.35, 3.85, 3.35, 2.85, 2.35]; r = 0.25; XL, XR = -1.28, 1.28
X, Y = [], []
for k, y in enumerate(ysr):
    a, b = (XR, XL) if k % 2 == 0 else (XL, XR)
    X += list(np.linspace(a, b, 40)); Y += [y]*40
    if k < len(ysr)-1:
        yc = (y + ysr[k+1])/2
        th = (np.linspace(np.pi/2, 1.5*np.pi, 26) if k % 2 == 0
              else np.linspace(np.pi/2, -np.pi/2, 26))
        X += list(b + r*np.cos(th)); Y += list(yc + r*np.sin(th))
tube([(0.44, 5.62), (0.90, 5.30), (1.22, 4.80), (1.28, 4.42)], w=5.4, z=3)
tube(list(zip(X, Y)), w=5.4, z=3)
tube([(-1.28, 2.35), (-1.70, 2.08), (-1.92, 1.88)], w=5.4, z=3)

# ---- salivary glands ----
for (cx, cy, w_, h_, an, nm) in [(-1.02, 9.62, 0.52, 0.38, 20, 'parotid'),
                                 (-0.86, 9.06, 0.44, 0.28, -10, 'submandibular'),
                                 (-0.28, 9.12, 0.30, 0.20, 0, 'sublingual')]:
    ax.add_patch(Ellipse((cx, cy), w_, h_, angle=an, fc=GLAND,
                         ec="#9a7a2c", lw=0.9, zorder=5))
ax.plot([-0.80, -0.50], [9.55, 9.42], color="#9a7a2c", lw=0.7, zorder=5)

# ---- labels: left column ----
lab("parotid gland", (-1.24, 9.68), -2.55, 9.95, ha='right')
lab("submandibular gland", (-1.06, 9.02), -2.55, 9.42, ha='right')
lab("sublingual gland", (-0.40, 9.06), -2.55, 8.88, ha='right')
lab("liver (4 lobes)", (-1.70, 7.90), -2.60, 8.24, ha='right')
lab("gall bladder", (-0.96, 6.78), -2.60, 7.44, ha='right')
lab("bile duct", (-0.36, 6.34), -2.60, 6.88, ha='right')
lab("duodenum\n(C-shaped)", (-0.62, 5.72), -2.62, 6.18, ha='right')
lab("hepatic flexure", (-2.08, 4.86), -2.70, 5.40, ha='right')
lab("ascending colon", (-2.14, 3.60), -2.70, 3.92, ha='right')
lab("ileo-caecal valve", (-1.88, 1.92), -2.70, 2.60, ha='right')
lab("caecum", (-2.22, 1.72), -2.70, 1.92, ha='right')
lab("vermiform appendix", (-1.86, 1.10), -2.70, 1.30, ha='right')

# ---- labels: right column ----
lab("buccal cavity\n(teeth + tongue)", (0.60, 9.44), 2.30, 9.92)
lab("pharynx", (0.06, 8.86), 2.30, 9.20)
lab("oesophagus (≈25 cm)", (0.16, 8.10), 2.30, 8.52)
lab("cardiac sphincter", (0.24, 7.52), 2.42, 7.92)
lab("stomach (1–1.5 L)", (1.20, 7.10), 2.60, 7.30)
lab("pyloric sphincter", (0.22, 6.22), 2.60, 6.72)
lab("pancreas", (0.90, 6.06), 2.62, 6.16)
lab("transverse colon", (0.46, 4.80), 2.62, 5.50)
lab("jejunum", (1.30, 4.10), 2.62, 4.70)
lab("descending colon", (2.16, 3.70), 2.66, 3.96)
lab("ileum (≈3.5 m)", (0.90, 2.62), 2.66, 2.98)
lab("sigmoid colon", (1.30, 1.18), 2.66, 1.80)
lab("rectum", (0.34, 0.86), 2.66, 1.06)
lab("anus", (0.36, 0.44), 2.66, 0.44)

ax.set_xlim(-5.55, 5.55); ax.set_ylim(0.05, 10.25)
ax.set_aspect('equal'); ax.axis('off')
```

The canal is regionally specialised:

- **Buccal cavity** — mechanical breakdown by the teeth, lubrication and partial
  starch digestion by saliva, and rolling of the food into a **bolus** by the
  tongue. Swallowing (deglutition) pushes the bolus into the pharynx; the
  epiglottis closes the glottis so food does not enter the trachea.
- **Oesophagus** — a muscular tube about 25 cm long. It secretes no enzyme; it
  moves the bolus by **peristalsis**, a travelling wave in which the circular
  muscle behind the bolus contracts and that in front relaxes.
- **Stomach** — a J-shaped bag of capacity 1–1.5 L with three regions
  (*cardiac*, *fundus*, *pyloric*) and three muscle layers (an extra oblique
  layer for churning). Gastric glands in its mucosa contain **mucous cells**
  (mucus + bicarbonate), **parietal (oxyntic) cells** (HCl and intrinsic factor)
  and **peptic (chief/zymogen) cells** (pepsinogen, and prorennin in infants).
  The bolus becomes acidic semi-fluid **chyme**, released in spurts through the
  pyloric sphincter.
- **Small intestine** — about 6 m long, the main site of both digestion and
  absorption, in three parts: the C-shaped **duodenum** (receives bile and
  pancreatic juice), the coiled **jejunum**, and the longest part, the **ileum**.
- **Large intestine** — about 1.5 m: **caecum** with the **vermiform appendix**
  (a vestigial organ in humans, housing symbiotic bacteria), **colon**
  (ascending, transverse, descending, sigmoid) and **rectum**. No enzymes are
  secreted here; it absorbs water, some minerals and vitamins (K and some B
  vitamins made by gut bacteria) and forms faeces.

::: memory Order of the canal — say it once, in order
Mouth → pharynx → oesophagus → stomach → duodenum → jejunum → ileum → caecum →
colon (ascending, transverse, descending, sigmoid) → rectum → anus.
Three sphincters guard it: **cardiac** (oesophagus–stomach), **pyloric**
(stomach–duodenum) and **anal**.
:::

### Teeth and the dental formula

Human teeth are **thecodont** (each root fixed in a bony socket),
**dicyphodont** (two sets in a lifetime — 20 deciduous or milk teeth, replaced by
32 permanent teeth) and **heterodont** (four different types with different
jobs).

```figure caption="(a) Vertical section of a human molar. (b) One side of the adult jaws, giving the permanent dental formula $2\left(\frac{2\,1\,2\,3}{2\,1\,2\,3}\right) = 32$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, FancyBboxPatch

fig, axes = plt.subplots(1, 2, figsize=(5.2, 4.0),
                         gridspec_kw=dict(width_ratios=[1.0, 1.18]))
EN = "#f7f4ea"; DEN = "#e3c58f"; PUL = "#d9737a"; CEM = "#a87f45"
BONE = "#ece3d4"; GUM = "#d9948f"

def lab(ax, txt, tip, tx, ty, ha='left', fs=6.2):
    ax.annotate(txt, xy=tip, xytext=(tx, ty), fontsize=fs, color=INK, ha=ha,
                va='center', zorder=20,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.65,
                                shrinkA=1.5, shrinkB=1.0))

# ================= (a) molar in vertical section =================
ax = axes[0]
ax.add_patch(Rectangle((-1.15, 0.10), 2.30, 2.05, fc=BONE, ec="#b79b6d",
                       lw=0.9, zorder=1))
for s_ in (1, -1):
    ax.add_patch(Polygon([(s_*1.15, 2.15), (s_*0.80, 2.15), (s_*0.70, 2.58),
                          (s_*1.15, 2.66)], closed=True, fc=GUM,
                         ec="#b06c68", lw=0.8, zorder=2))
DENT = [(-0.82, 2.40), (-0.92, 3.18), (-0.56, 3.76), (0.0, 3.88), (0.56, 3.76),
        (0.92, 3.18), (0.82, 2.40), (0.66, 1.62), (0.50, 0.76), (0.34, 0.78),
        (0.24, 1.50), (0.0, 2.00), (-0.24, 1.50), (-0.34, 0.78), (-0.50, 0.76),
        (-0.66, 1.62), (-0.82, 2.40)]
ax.add_patch(Polygon(DENT, closed=True, fc=DEN, ec="#a8824c", lw=1.0, zorder=3))
ax.add_patch(Polygon([(-0.82, 2.46), (-0.94, 3.20), (-0.57, 3.82), (0.0, 3.95),
                      (0.57, 3.82), (0.94, 3.20), (0.82, 2.46), (0.70, 2.48),
                      (0.80, 3.12), (0.50, 3.62), (0.0, 3.74), (-0.50, 3.62),
                      (-0.80, 3.12), (-0.70, 2.48)],
                     closed=True, fc=EN, ec="#9a9484", lw=0.9, zorder=4))
for s_ in (1, -1):
    ax.plot([s_*0.82, s_*0.66, s_*0.50], [2.40, 1.62, 0.78], color=CEM,
            lw=2.6, zorder=3.4, solid_capstyle='round')
    ax.plot([s_*0.90, s_*0.74, s_*0.58], [2.42, 1.62, 0.70], color="#c2708a",
            lw=1.0, ls=(0, (1.6, 1.4)), zorder=3.2)
ax.add_patch(Polygon([(-0.48, 3.02), (0.0, 3.40), (0.48, 3.02), (0.50, 2.34),
                      (0.505, 1.60), (0.46, 0.92), (0.40, 0.94), (0.385, 1.62),
                      (0.20, 2.40), (-0.20, 2.40), (-0.385, 1.62),
                      (-0.40, 0.94), (-0.46, 0.92), (-0.505, 1.60),
                      (-0.50, 2.34)],
                     closed=True, fc=PUL, ec="#a8494f", lw=0.8, zorder=5))
for s_ in (1, -1):
    ax.plot([s_*0.43, s_*0.43], [0.93, 0.66], color="#a8271f", lw=1.1, zorder=6)
ax.plot([-0.06, 0.06], [3.24, 3.24], color="#f7c9cc", lw=0.8, zorder=6)

lab(ax, "enamel", (-0.88, 3.34), -1.22, 4.34, ha='right')
lab(ax, "crown", (-0.40, 3.86), -1.22, 3.82, ha='right')
lab(ax, "neck", (-0.84, 2.44), -1.22, 3.10, ha='right')
lab(ax, "gum (gingiva)", (-1.02, 2.40), -1.30, 2.52, ha='right')
lab(ax, "alveolar bone", (-1.10, 1.70), -1.30, 1.84, ha='right')
lab(ax, "periodontal\nligament", (-0.70, 1.20), -1.30, 1.00, ha='right')
lab(ax, "root", (-0.42, 0.90), -1.30, 0.32, ha='right')
lab(ax, "dentine", (0.74, 3.30), 1.14, 4.34)
lab(ax, "pulp cavity", (0.34, 2.96), 1.14, 3.70)
lab(ax, "cementum", (0.80, 2.34), 1.14, 2.96)
lab(ax, "root canal", (0.45, 1.60), 1.14, 1.90)
lab(ax, "nerve + blood\nvessels", (0.44, 0.76), 1.14, 0.86)
ax.text(0, 4.86, "(a) molar, V.S.", ha='center', fontsize=7.4, color=INK)
ax.set_xlim(-2.55, 2.45); ax.set_ylim(-0.05, 5.05)
ax.set_aspect('equal'); ax.axis('off')

# ================= (b) permanent dentition, one side =================
ax = axes[1]
groups = [("incisors", "I", 2, 0.34, 0.64, "#1d6fb8"),
          ("canine", "C", 1, 0.30, 0.78, "#d9534f"),
          ("premolars", "PM", 2, 0.44, 0.54, "#2e8b57"),
          ("molars", "M", 3, 0.58, 0.50, "#b8860b")]
def draw_row(y0, up=True):
    x = 0.0
    for nm, sym, n, wdt, ht, c in groups:
        for k in range(n):
            yy = y0 + (0 if up else -ht)
            ax.add_patch(FancyBboxPatch((x, yy), wdt, ht,
                         boxstyle="round,pad=0.012,rounding_size=0.10",
                         fc=EN, ec=c, lw=1.25, zorder=3))
            x += wdt + 0.10
        x += 0.34
    return x - 0.34
xe = draw_row(0.30, up=True)
draw_row(-0.30, up=False)
for sgn in (1, -1):
    ax.plot([-0.10, xe + 0.02], [sgn*0.26, sgn*0.26], color=GUM, lw=3.4,
            zorder=1, solid_capstyle='round')
ax.plot([-0.26, -0.26], [-1.75, 1.95], color=MUTED, lw=0.8, ls=(0, (3, 2)))
ax.text(-0.34, -1.55, "midline", fontsize=6.0, color=MUTED, ha='right',
        rotation=90, va='bottom')
ax.text(xe + 0.30, 0.66, "upper jaw", fontsize=6.4, color=MUTED, ha='left')
ax.text(xe + 0.30, -0.66, "lower jaw", fontsize=6.4, color=MUTED, ha='left')
x = 0.0
for i, (nm, sym, n, wdt, ht, c) in enumerate(groups):
    span = n*wdt + (n-1)*0.10
    yb = 1.10 if i % 2 == 0 else 1.66
    ax.annotate('', xy=(x, yb), xytext=(x+span, yb),
                arrowprops=dict(arrowstyle='|-|', color=c, lw=0.9,
                                mutation_scale=2.0))
    ax.text(x+span/2, yb+0.06, f"{nm}\n{sym} = {n}", fontsize=6.3, color=c,
            ha='center', va='bottom', linespacing=1.25)
    x += span + 0.10 + 0.34
ax.text(xe/2, -1.30, "one half-jaw:  2  1  2  3  =  8 teeth\n"
        "both jaws, both sides:  4 × 8  =  32", fontsize=6.6, color=INK,
        ha='center', va='center')
ax.text(xe/2, 2.58, "(b) permanent teeth, one side", ha='center',
        fontsize=7.4, color=INK)
ax.set_xlim(-1.05, xe+1.05); ax.set_ylim(-2.05, 2.80); ax.axis('off')
fig.subplots_adjust(wspace=0.04)
```

The **permanent dental formula**, written for one half of the upper jaw over one
half of the lower jaw and doubled, is

$$ 2\left(\frac{I\,2 \;\; C\,1 \;\; PM\,2 \;\; M\,3}{I\,2 \;\; C\,1 \;\; PM\,2 \;\; M\,3}\right) = 32 $$

and the **deciduous (milk) dental formula**, which has no premolars, is

$$ 2\left(\frac{I\,2 \;\; C\,1 \;\; M\,2}{I\,2 \;\; C\,1 \;\; M\,2}\right) = 20 $$

Incisors cut, canines tear, premolars and molars crush and grind. The last
molars ("wisdom teeth") erupt at 17–25 years.

::: caution Read a dental formula the right way round
The formula counts **one half of each jaw only** — that is why it is multiplied
by 2. Writing $\frac{2123}{2123} = 32$ without the 2 outside is a marked error,
and so is calling the milk formula "2(2 1 2 2)": milk teeth have **no premolars**,
so it is 2 1 0 2, written simply as I2 C1 M2.
:::

### Digestive glands, enzymes and chemical digestion

Three sets of glands supply the tube. **Salivary glands** (three pairs: parotid,
submandibular, sublingual) secrete about 1–1.5 L of saliva a day, pH 6.8,
containing salivary amylase, lysozyme and mucin. The **liver**, the largest gland
of the body (1.2–1.5 kg), secretes **bile**, stored and concentrated in the gall
bladder. Bile contains **no enzyme**: its bile salts (sodium glycocholate and
taurocholate) **emulsify** fat — they break large fat droplets into a fine
suspension, hugely increasing the surface available to lipase — and its
bicarbonate neutralises the acid chyme. The **pancreas** is a heterocrine gland;
its exocrine part secretes pancreatic juice, the most complete digestive juice of
all, containing enzymes for every class of food.

| Enzyme | Source (juice) | Substrate | Product | Optimum pH |
|---|---|---|---|---|
| Salivary amylase (ptyalin) | salivary glands (saliva) | starch, glycogen | maltose + dextrins | 6.8 |
| Pepsin (from pepsinogen) | peptic cells (gastric juice) | proteins | peptones, proteoses | 1.5–2.0 |
| Rennin (infants only) | peptic cells (gastric juice) | casein of milk | paracasein (curd) | 3.5 |
| Gastric lipase | gastric glands | emulsified fat | fatty acids + glycerol | 4–5 |
| Pancreatic amylase | pancreas (pancreatic juice) | starch, dextrins | maltose | 7.1 |
| Trypsin (from trypsinogen) | pancreas | proteins, peptones | dipeptides, peptides | 7.8–8.0 |
| Chymotrypsin | pancreas | proteins, peptones | peptides | 8.0 |
| Carboxypeptidase | pancreas | peptides (C-terminal) | amino acids | 7.2 |
| Pancreatic lipase (steapsin) | pancreas | emulsified triglycerides | fatty acids + monoglycerides | 8.0 |
| Nucleases (DNase, RNase) | pancreas | DNA, RNA | nucleotides | 7.0 |
| Enterokinase | intestinal glands | trypsinogen | trypsin (activation) | 8.0 |
| Maltase | brush border | maltose | glucose + glucose | 6.1–6.8 |
| Sucrase (invertase) | brush border | sucrose | glucose + fructose | 6.2 |
| Lactase | brush border | lactose | glucose + galactose | 6.0 |
| Dipeptidase, aminopeptidase | brush border | dipeptides, peptides | amino acids | 8.0 |

Note the logic of the table. Proteolytic enzymes are secreted as **inactive
zymogens** (pepsinogen, trypsinogen, chymotrypsinogen) so that they cannot digest
the gland that makes them; pepsinogen is activated by HCl, trypsinogen by
**enterokinase** from the intestinal mucosa, and trypsin then activates all the
rest. Note also the pH jump: pepsin needs pH 2, every intestinal enzyme needs pH
about 8, which is why bile and pancreatic bicarbonate must neutralise the chyme
first.

::: key The end products of digestion
Carbohydrates → **monosaccharides** (glucose, fructose, galactose).
Proteins → **amino acids**. Fats → **fatty acids + glycerol/monoglycerides**.
Nucleic acids → nucleosides and nitrogenous bases. Only these cross the
intestinal epithelium.
:::

### Absorption: the villus

Absorption is the passage of the end products from the lumen into the blood or
lymph. It happens almost entirely in the small intestine, whose surface is
amplified three times over — by circular folds, by finger-like **villi**
(0.5–1.5 mm long, 20–40 per mm²), and by **microvilli** on each epithelial cell
forming the **brush border**. The total absorptive area reaches about 200 m²,
roughly a badminton court packed inside your abdomen.

```figure caption="A single intestinal villus. Sugars and amino acids leave in the blood capillaries; fats leave as chylomicrons in the lacteal."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Ellipse
from matplotlib.path import Path
from matplotlib.patches import PathPatch

fig, ax = plt.subplots(figsize=(4.8, 4.0))
EPI = "#f3ddc4"; EDGE = "#a8824c"; LAC = "#e8e2b0"; CORE = "#fbf3e6"

# villus outline: two side walls joined by a dome
ys = np.linspace(0, 3.4, 260)
w = 0.52 + 0.0*ys
w = np.where(ys > 2.9, 0.52*np.sqrt(np.clip(1-((ys-2.9)/0.52)**2, 0, 1)), 0.52)
w = np.maximum(w, 0.02)
pts = np.vstack([np.c_[w, ys], np.c_[-w[::-1], ys[::-1]]])
ax.add_patch(Polygon(pts, closed=True, fc=EPI, ec=EDGE, lw=1.3, zorder=3))
# lamina propria (inner core)
wi = np.maximum(w - 0.16, 0.01)
ax.add_patch(Polygon(np.vstack([np.c_[wi, ys], np.c_[-wi[::-1], ys[::-1]]]),
                     closed=True, fc=CORE, ec=EDGE, lw=0.7, zorder=4))
# columnar epithelial cell boundaries + microvilli brush border
for t in np.linspace(0.05, 0.995, 34):
    i = int(t*259); xx, yy = w[i], ys[i]
    for s in (1, -1):
        nx, ny = 1.0, 0.0
        if yy > 2.9:
            a = np.arctan2(yy-2.9, xx); nx, ny = np.cos(a), np.sin(a)
        ax.plot([s*(xx-0.16*nx), s*xx], [yy-0.16*ny, yy], color=EDGE,
                lw=0.45, zorder=5)
        ax.plot([s*xx, s*(xx+0.085*nx)], [yy, yy+0.085*ny], color="#8a6a45",
                lw=0.8, zorder=5)
# lacteal (central lymph vessel)
ax.add_patch(Polygon([(-0.11, 0.10), (-0.11, 2.85), (0.0, 3.05), (0.11, 2.85),
                      (0.11, 0.10)], closed=True, fc=LAC, ec="#a89a2c",
                     lw=0.9, zorder=6))
for k in range(4):
    ax.add_patch(Circle((-0.04+0.05*(k % 2), 0.6+0.55*k), 0.045, fc="#c9b83c",
                        ec='none', zorder=7))
# capillary network round the lacteal
th = np.linspace(0, 1, 200)
for s in (1, -1):
    xx = s*(0.30 + 0.085*np.sin(9.0*np.pi*th))
    yy = 0.12 + 3.0*th
    yy = np.where(yy > 2.8, 2.8 + (yy-2.8)*0.55, yy)
    ax.plot(xx*np.clip((3.3-yy)/0.7, 0, 1)**0.25, yy, color="#1d6fb8" if s > 0
            else "#c0392b", lw=1.5, zorder=6)
ax.annotate('', xy=(-0.30, 0.02), xytext=(-0.30, -0.42),
            arrowprops=dict(arrowstyle='-|>', color="#c0392b", lw=1.3,
                            mutation_scale=8), zorder=8)
ax.annotate('', xy=(0.30, -0.42), xytext=(0.30, 0.02),
            arrowprops=dict(arrowstyle='-|>', color="#1d6fb8", lw=1.3,
                            mutation_scale=8), zorder=8)
# smooth muscle strand + crypt of Lieberkuhn
ax.plot([0.0, 0.0], [0.05, 0.9], color="#b07a9a", lw=1.0, ls=(0, (2, 1.6)), zorder=5)
ax.add_patch(Polygon([(0.80, 0.02), (0.80, -0.55), (0.98, -0.72), (1.16, -0.55),
                      (1.16, 0.02)], closed=True, fc=EPI, ec=EDGE, lw=1.0, zorder=3))
ax.plot([0.60, 0.72], [0.02, 0.02], color=EDGE, lw=1.0, zorder=3)
ax.plot([-1.30, 1.40], [0.02, 0.02], color=EDGE, lw=1.1, zorder=2)

# absorbed molecules arriving at the surface
for (x0, y0, c, t) in [(-0.95, 2.55, "#1d6fb8", "glucose"),
                       (-0.95, 2.05, "#2e8b57", "amino\nacids"),
                       (0.95, 2.55, "#b8860b", "fatty acids +\nmonoglycerides"),
                       (0.95, 1.95, "#6a5acd", "glycerol")]:
    sg = 1 if x0 > 0 else -1
    ax.annotate('', xy=(sg*0.60, y0), xytext=(x0*1.05, y0),
                arrowprops=dict(arrowstyle='-|>', color=c, lw=1.1,
                                mutation_scale=8), zorder=8)
    ax.text(x0*1.12, y0, t, fontsize=6.2, color=c,
            ha='right' if sg < 0 else 'left', va='center')

def lab(txt, tip, tx, ty, ha='left', fs=6.2):
    ax.annotate(txt, xy=tip, xytext=(tx, ty), fontsize=fs, color=INK, ha=ha,
                va='center', zorder=20,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.65,
                                shrinkA=1.5, shrinkB=1.0))
lab("microvilli\n(brush border)", (0.10, 3.30), 0.95, 3.62)
lab("columnar\nepithelium", (-0.46, 2.85), -1.05, 3.45, ha='right')
lab("lacteal\n(lymph vessel)", (0.06, 1.85), -1.05, 1.35, ha='right')
lab("blood capillary\nnetwork", (0.33, 1.30), 1.05, 1.20)
lab("chylomicrons", (0.0, 1.15), -1.08, 0.72, ha='right')
lab("crypt of Lieberkühn\n(intestinal gland)", (1.06, -0.40), 1.10, -0.28)
lab("to hepatic portal vein", (0.30, -0.36), 0.62, -0.92)
lab("from mesenteric artery", (-0.30, -0.36), -0.62, -0.92, ha='right')
ax.text(0, 4.02, "villus, L.S.", ha='center', fontsize=7.4, color=INK)
ax.set_xlim(-2.35, 2.35); ax.set_ylim(-1.15, 4.20)
ax.set_aspect('equal'); ax.axis('off')
```

Glucose, galactose and amino acids are absorbed by **active transport** (against
their gradient, using ATP and a Na⁺ co-transporter) into the blood capillaries,
and travel by the **hepatic portal vein to the liver** before entering the
general circulation. Fructose and some amino acids move by **facilitated
diffusion**; water, most fatty acids, glycerol and fat-soluble vitamins by
**simple diffusion**. Fatty acids and monoglycerides are re-esterified inside the
epithelial cell, coated with protein to form **chylomicrons**, and enter the
**lacteal**; lymph carries them through the thoracic duct into the left
subclavian vein — bypassing the liver. Assimilation, the use of absorbed
nutrients by cells, completes the process; undigested cellulose (roughage) and
bacteria form the faeces, egested by the **defaecation reflex**.

## 8.2 Respiratory System

Every cell of the body oxidises glucose to make ATP, and every cell produces
CO₂. Breathing (**external respiration**) is only the transport half of the job —
moving O₂ from the air to the blood and CO₂ the other way. Cellular respiration,
the chemistry, happens in the mitochondria.

### The respiratory tract

Air passes through a **conducting portion**, which warms, moistens and filters it
but takes no part in exchange, and a **respiratory portion**, where exchange
occurs.

```figure caption="The human respiratory tract, with a magnified alveolar sac. The capillary enters blue (deoxygenated, from the pulmonary artery) and leaves red (oxygenated, to the pulmonary vein)."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Ellipse, PathPatch
from matplotlib.path import Path

fig, ax = plt.subplots(figsize=(5.2, 4.4))
LUNG = "#f0c9c4"; LEDGE = "#b06c68"; CART = "#dfe9f2"; TUBE = "#c9d9e6"
ALV = "#fbeeea"

def bez(pts, fc, ec, lw=1.2, z=3, ls='-'):
    """pts[0] = start; the rest must come in groups of 3, last point = pts[0]."""
    assert (len(pts) - 1) % 3 == 0, len(pts)
    codes = [Path.MOVETO] + [Path.CURVE4]*(len(pts)-1)
    p = PathPatch(Path(pts, codes), fc=fc, ec=ec, lw=lw, zorder=z, ls=ls)
    ax.add_patch(p); return p

def lab(txt, tip, tx, ty, ha='left', fs=6.2, c=INK):
    ax.annotate(txt, xy=tip, xytext=(tx, ty), fontsize=fs, color=c, ha=ha,
                va='center', zorder=25,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.65,
                                shrinkA=1.5, shrinkB=1.0))

# ---------------- lungs ----------------
R = [(-1.05, 7.62),
     (-1.90, 7.55), (-2.45, 6.60), (-2.55, 5.40),
     (-2.62, 4.10), (-2.35, 2.95), (-1.90, 2.72),
     (-1.40, 2.48), (-0.85, 2.75), (-0.62, 3.40),
     (-0.45, 4.10), (-0.50, 5.40), (-0.55, 6.20),
     (-0.60, 6.90), (-0.75, 7.55), (-1.05, 7.62)]
L = [(1.05, 7.62),
     (1.90, 7.55), (2.45, 6.60), (2.55, 5.40),
     (2.62, 4.10), (2.35, 2.95), (1.90, 2.72),
     (1.45, 2.50), (1.00, 2.80), (0.85, 3.50),
     (0.78, 4.10), (1.30, 4.55), (1.18, 5.05),
     (1.06, 5.55), (0.62, 5.85), (0.58, 6.30),
     (0.55, 6.90), (0.75, 7.55), (1.05, 7.62)]
def scaled(pts, k, cx, cy):
    return [(cx + (x-cx)*k, cy + (y-cy)*k) for x, y in pts]
bez(scaled(R, 1.06, -1.5, 5.1), 'none', "#8a6a9a", lw=0.9, z=1, ls=(0, (3, 2)))
bez(scaled(L, 1.06, 1.5, 5.1), 'none', "#8a6a9a", lw=0.9, z=1, ls=(0, (3, 2)))
bez(R, LUNG, LEDGE, z=2)
bez(L, LUNG, LEDGE, z=2)
ax.plot([-2.50, -1.30, -0.58], [5.90, 4.90, 4.10], color=LEDGE, lw=0.9, zorder=3)
ax.plot([-2.20, -1.40, -0.55], [6.60, 6.30, 5.90], color=LEDGE, lw=0.9, zorder=3)
ax.plot([2.50, 1.60, 0.95], [5.90, 4.80, 3.95], color=LEDGE, lw=0.9, zorder=3)

# ---------------- nasal cavity, pharynx, larynx, trachea ----------------
ax.add_patch(Polygon([(-1.25, 9.20), (-1.45, 9.70), (-0.90, 10.02),
                      (0.05, 10.05), (0.35, 9.72), (0.32, 9.18)],
                     closed=True, fc="#f7e2d8", ec="#b08070", lw=1.0, zorder=3))
for k in range(3):
    ax.plot([-1.20 + 0.03*k, -0.70], [9.36 + 0.21*k, 9.42 + 0.21*k],
            color="#b08070", lw=1.4, zorder=4, solid_capstyle='round')
ax.add_patch(Polygon([(-0.30, 9.18), (0.32, 9.18), (0.30, 8.72), (-0.28, 8.72)],
                     closed=True, fc=TUBE, ec="#7f96a8", lw=1.0, zorder=3))
ax.add_patch(Polygon([(-0.30, 8.72), (0.30, 8.72), (0.26, 8.18), (-0.26, 8.18)],
                     closed=True, fc=CART, ec="#7f96a8", lw=1.1, zorder=3))
ax.plot([-0.26, 0.26], [8.50, 8.50], color="#7f96a8", lw=0.8, zorder=4)
ax.add_patch(Polygon([(-0.22, 8.18), (0.22, 8.18), (0.22, 6.70), (-0.22, 6.70)],
                     closed=True, fc=TUBE, ec="#7f96a8", lw=1.0, zorder=3))
for y in np.arange(6.85, 8.16, 0.20):
    ax.plot([-0.22, 0.22], [y, y], color="#7f96a8", lw=2.0, zorder=4,
            solid_capstyle='butt')
ax.plot([-0.08, -0.55, -1.05], [6.72, 6.42, 6.18], color="#7f96a8", lw=4.4,
        zorder=5, solid_capstyle='round')
ax.plot([0.08, 0.68, 1.18], [6.72, 6.30, 6.05], color="#7f96a8", lw=3.6,
        zorder=5, solid_capstyle='round')

def branch(x, y, ang, L0, w, depth):
    if depth == 0:
        ax.add_patch(Circle((x, y), 0.075, fc="#e7b8b2", ec=LEDGE, lw=0.5, zorder=6))
        return
    for da in (-30, 26):
        a = np.radians(ang + da)
        x2, y2 = x + L0*np.cos(a), y + L0*np.sin(a)
        ax.plot([x, x2], [y, y2], color="#7f96a8", lw=max(w, 0.7), zorder=5.5,
                solid_capstyle='round')
        branch(x2, y2, ang + da, L0*0.72, w*0.68, depth-1)
branch(-1.05, 6.18, -105, 0.68, 3.0, 4)
branch(1.18, 6.05, -75, 0.66, 2.6, 4)

# pleura + diaphragm
th = np.linspace(0, np.pi, 200)
ax.plot(2.95*np.cos(th), 2.40 + 0.58*np.sin(th), color="#8a5a9a", lw=2.4,
        zorder=2, solid_capstyle='round')
ax.plot([-2.95, 2.95], [2.40, 2.40], color="#8a5a9a", lw=0.8, ls=(0, (3, 2)),
        zorder=1)
ax.annotate('', xy=(0.55, 2.10), xytext=(0.55, 2.86),
            arrowprops=dict(arrowstyle='-|>', color="#8a5a9a", lw=1.2,
                            mutation_scale=8), zorder=6)
ax.text(0.78, 1.98, "contracts and flattens\n→ thoracic volume rises",
        fontsize=5.9, color="#8a5a9a", va='center')

# ---------------- inset: alveolar sac ----------------
CX, CY, RR = 4.85, 6.85, 1.62
ax.add_patch(Circle((CX, CY), RR, fc="#fdf7f4", ec=MUTED, lw=1.0, zorder=8))
ax.plot([1.55, CX-RR*0.92], [5.05, CY-RR*0.60], color=MUTED, lw=0.6,
        ls=(0, (3, 2)), zorder=7)
ax.plot([1.70, CX-RR*0.52], [5.60, CY+RR*0.82], color=MUTED, lw=0.6,
        ls=(0, (3, 2)), zorder=7)
ax.plot([CX-1.45, CX-0.90, CX-0.45], [CY-1.00, CY-0.62, CY-0.30],
        color="#7f96a8", lw=3.2, zorder=9, solid_capstyle='round')
for dx, dy, rad in [(-0.10, 0.62, 0.44), (0.60, 0.50, 0.40), (0.92, -0.16, 0.38),
                    (0.30, -0.62, 0.40), (-0.42, -0.30, 0.36), (0.30, 0.02, 0.34)]:
    ax.add_patch(Circle((CX+dx, CY+dy), rad, fc=ALV, ec="#c08a84", lw=1.0,
                        zorder=9.5))
t = np.linspace(0, 1, 300)
cxx = CX - 1.05 + 2.15*t
cyy = CY + 0.95 - 1.55*t + 0.30*np.sin(10.5*np.pi*t)
ax.plot(cxx, cyy, color="#b03a3a", lw=2.0, zorder=10)
ax.plot(cxx[:120], cyy[:120], color="#4a67b8", lw=2.0, zorder=10)
ax.annotate('', xy=(CX+0.02, CY+0.44), xytext=(CX-0.34, CY+0.06),
            arrowprops=dict(arrowstyle='-|>', color="#b03a3a", lw=1.3,
                            mutation_scale=8), zorder=11)
ax.annotate('', xy=(CX+0.50, CY-0.38), xytext=(CX+0.20, CY-0.04),
            arrowprops=dict(arrowstyle='-|>', color="#4a67b8", lw=1.3,
                            mutation_scale=8), zorder=11)
ax.text(CX-0.60, CY+0.40, "O₂", fontsize=7.2, color="#b03a3a", ha='center')
ax.text(CX+0.80, CY-0.56, "CO₂", fontsize=7.2, color="#4a67b8", ha='center')

lab("nasal cavity\n(conchae)", (-1.05, 9.62), -3.30, 9.90, ha='right')
lab("pharynx", (-0.28, 8.95), -3.30, 9.08, ha='right')
lab("larynx (voice box)\n+ epiglottis", (-0.28, 8.46), -3.30, 8.35, ha='right')
lab("trachea, with\nC-shaped cartilage", (-0.22, 7.50), -3.30, 7.35, ha='right')
lab("primary bronchus", (-0.70, 6.34), -3.30, 6.42, ha='right')
lab("right lung — 3 lobes", (-2.28, 5.40), -3.30, 5.55, ha='right')
lab("bronchiole", (-1.55, 4.55), -3.30, 4.55, ha='right')
lab("pleural membranes", (-2.72, 3.55), -3.30, 3.55, ha='right')
lab("diaphragm", (-1.90, 2.82), -3.30, 2.70, ha='right')
lab("left lung — 2 lobes,\nwith a cardiac notch", (1.55, 7.05), 1.25, 9.85)
lab("terminal\nbronchiole", (CX-1.22, CY-0.84), CX-1.72, CY-1.88, ha='center')
lab("alveolar sac: ≈300 million\nalveoli, total area ≈ 70 m²",
    (CX+0.66, CY+0.88), CX+0.30, CY+2.25, ha='center')
lab("capillary network", (cxx[265], cyy[265]), CX+1.80, CY-1.30, ha='left')
ax.text(CX+0.55, CY-3.05, "alveolar air:  pO₂ 104,  pCO₂ 40 mmHg\n"
        "blood arriving:  pO₂ 40,  pCO₂ 45 mmHg", fontsize=6.0, color=INK,
        ha='center', va='center')

ax.set_xlim(-6.60, 7.60); ax.set_ylim(1.70, 10.70)
ax.set_aspect('equal'); ax.axis('off')
```

The **conducting portion** is: external nares → nasal chambers (lined by ciliated
mucous epithelium; the turbinate bones or conchae make the air swirl so that dust
sticks) → pharynx → larynx → trachea → two primary bronchi → secondary and
tertiary bronchi → bronchioles → terminal bronchioles. The trachea is held open
by about 16–20 **C-shaped rings of hyaline cartilage**, incomplete at the back so
that a swallowed bolus can bulge into the space.

The **respiratory portion** begins at the respiratory bronchioles and ends in the
**alveoli** — some 300 million thin-walled sacs giving a total surface of about
70 m². The **respiratory membrane** across which gases diffuse is astonishingly
thin (less than 1 μm) and has only three layers: the squamous alveolar
epithelium, a fused basement membrane, and the capillary endothelium.

::: key Why the lung is built this way
Fick's law says diffusion rate ∝ (surface area × pressure difference) ÷ thickness.
The lung maximises all three: 70 m² of area, a steep pO₂ gradient maintained by
ventilation and by blood flow, and a membrane under 1 μm thick.
:::

### Mechanism of breathing

Breathing is entirely a pressure story, governed by Boyle's law: increase the
volume of the thoracic cavity and the pressure inside falls below atmospheric, so
air rushes in.

- **Inspiration (active).** The **diaphragm** contracts and flattens (increasing
  the vertical axis of the thorax); the **external intercostal muscles** contract
  and pull the ribs up and out (increasing the antero-posterior axis). Thoracic
  volume rises, intrapulmonary pressure falls about 1–3 mmHg below atmospheric,
  and roughly 500 ml of air enters.
- **Expiration (normally passive).** The diaphragm and external intercostals
  relax; the elastic recoil of the lungs and chest wall reduces the volume and
  raises intrapulmonary pressure 1–3 mmHg above atmospheric, driving air out.
  Forced expiration adds the internal intercostals and abdominal muscles.

A normal adult breathes 12–16 times a minute. Breathing is controlled by the
**respiratory rhythm centre** in the medulla oblongata, moderated by the
**pneumotaxic centre** in the pons, and by chemoreceptors near the aorta and
carotid arteries that respond chiefly to a **rise in CO₂ and H⁺** — not to a fall
in O₂.

### Lung volumes and capacities

A **spirometer** records the volume of air moved. A *volume* is a single
measurement; a *capacity* is the sum of two or more volumes.

```figure caption="A spirometer trace: three quiet breaths, then one maximal inspiration followed by a maximal expiration. Volumes are drawn in colour, capacities (sums of volumes) to the right."
import numpy as np, matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(5.2, 3.4))
RV, ERV, TV, IRV = 1200, 1100, 500, 3000
FRC = RV + ERV            # 2300 — lung volume at the end of a quiet expiration
TOP = FRC + TV            # 2800 — at the end of a quiet inspiration
TLC = FRC + TV + IRV      # 5800

def smooth(x):
    return 0.5 - 0.5*np.cos(np.pi*np.clip(x, 0, 1))

def quiet(tt):
    return (FRC + TOP)/2 - (TV/2)*np.cos(2*np.pi*tt/2.4)

t = np.linspace(0, 22.5, 4000)
v = np.empty_like(t)
m = t <= 7.2;                    v[m] = quiet(t[m])
m = (t > 7.2) & (t <= 10.0);     v[m] = FRC + (TLC-FRC)*smooth((t[m]-7.2)/2.8)
m = (t > 10.0) & (t <= 10.6);    v[m] = TLC
m = (t > 10.6) & (t <= 13.4);    v[m] = TLC + (RV-TLC)*smooth((t[m]-10.6)/2.8)
m = (t > 13.4) & (t <= 14.0);    v[m] = RV
m = (t > 14.0) & (t <= 14.9);    v[m] = RV + (FRC-RV)*smooth((t[m]-14.0)/0.9)
m = t > 14.9;                    v[m] = quiet(t[m]-14.9)
ax.plot(t, v, color=ACCENT, lw=1.7, zorder=5)
ax.fill_between([0, 22.6], 0, RV, color=MUTED, alpha=0.13, zorder=1)
for y in (RV, FRC, TOP, TLC):
    ax.axhline(y, color=MUTED, lw=0.8, ls=(0, (3, 2)), zorder=2)
ax.text(22.4, RV/2, "residual volume  RV = 1200", fontsize=6.3, color=MUTED,
        ha='right', va='center')

def span(x, y0, y1, txt, c, ty=None, fs=6.4):
    ax.annotate('', xy=(x, y0), xytext=(x, y1),
                arrowprops=dict(arrowstyle='<|-|>', color=c, lw=1.1,
                                mutation_scale=7), zorder=6)
    if txt:
        ax.text(x + 0.28, (y0+y1)/2 if ty is None else ty, txt, fontsize=fs,
                color=c, va='center', ha='left', linespacing=1.2)

span(3.55, FRC, TOP, "", SERIES[2])
ax.annotate("TV 500", xy=(3.55, 2550), xytext=(1.85, 4250), fontsize=6.4,
            color=SERIES[2], ha='center', va='center', zorder=7,
            arrowprops=dict(arrowstyle='-', color=SERIES[2], lw=0.7,
                            shrinkA=2, shrinkB=2))
span(5.55, TOP, TLC, "IRV 3000", SERIES[3])
span(1.15, 0, FRC, "FRC\n2300", SERIES[0], ty=780)
span(15.60, FRC, TLC, "IC 3500", "#8a5a9a")
span(17.40, RV, FRC, "ERV\n1100", SERIES[1])
span(19.30, RV, TLC, "VC 4600", SERIES[4])
span(21.20, 0, TLC, "TLC\n5800", SERIES[5], ty=4400)
ax.text(10.3, TLC + 300, "maximal inspiration → maximal expiration",
        fontsize=6.4, color=INK, ha='center')
ax.set_xlabel('time (s)'); ax.set_ylabel('volume of air in the lungs (ml)')
ax.set_xlim(0, 22.6); ax.set_ylim(0, 6500)
ax.set_yticks([0, 1200, 2300, 2800, 5800])
ax.set_xticks([0, 5, 10, 15, 20])
ax.spines[['top', 'right']].set_visible(False)
ax.grid(True, axis='y', alpha=0.4)
```

| Volume / capacity | Symbol | Definition | Normal value |
|---|---|---|---|
| Tidal volume | TV | air breathed in or out in one quiet breath | 500 ml |
| Inspiratory reserve volume | IRV | extra air taken in by a forced inspiration | 2500–3000 ml |
| Expiratory reserve volume | ERV | extra air expelled by a forced expiration | 1000–1100 ml |
| Residual volume | RV | air left after the most forceful expiration | 1100–1200 ml |
| Inspiratory capacity | IC | TV + IRV | 3500 ml |
| Expiratory capacity | EC | TV + ERV | 1600 ml |
| Functional residual capacity | FRC | ERV + RV | 2300 ml |
| Vital capacity | VC | TV + IRV + ERV (max out after max in) | 4600 ml |
| Total lung capacity | TLC | VC + RV | 5800 ml |

::: caution Residual volume cannot be measured by a spirometer
RV is the air you can never blow out, so a spirometer never sees it. It is found
indirectly (helium dilution or nitrogen wash-out). Consequently TLC and FRC,
which contain RV, also cannot be read straight off a spirometer trace.
:::

::: example Worked example 8.1 — pulmonary and alveolar ventilation
**Problem.** A student breathes 15 times per minute with a tidal volume of
500 ml. The anatomical dead space is 150 ml. Calculate (a) the pulmonary
ventilation rate and (b) the alveolar ventilation rate. (c) If she instead takes
shallow breaths of 250 ml at 30 per minute, what happens to each?

**Solution.**

(a) Pulmonary ventilation $= TV \times$ breathing rate

$$ = 500 \times 15 = 7500\ \text{ml min}^{-1} = 7.5\ \text{L min}^{-1} $$

(b) Only the air beyond the dead space reaches the alveoli:

$$ V_A = (TV - V_D)\times f = (500-150)\times 15 = 350 \times 15 = 5250\ \text{ml min}^{-1} $$

(c) Pulmonary ventilation $= 250\times30 = 7500\ \text{ml min}^{-1}$ — **unchanged**.
But alveolar ventilation $= (250-150)\times 30 = 100\times30 = 3000\ \text{ml min}^{-1}$,
a fall of 43 %.

**Conclusion.** Deep slow breathing ventilates the alveoli far better than rapid
shallow breathing, even when the total air moved is identical. This is why
panting is an inefficient way to get oxygen.
:::

### Transport of gases

| Gas | Partial pressure (mmHg) | Atmospheric air | Alveoli | Deoxygenated blood | Oxygenated blood | Tissues |
|---|---|---|---|---|---|---|
| O₂ | pO₂ | 159 | 104 | 40 | 95 | 40 |
| CO₂ | pCO₂ | 0.3 | 40 | 45 | 40 | 45 |

Gases move only down these gradients, by simple diffusion. **Oxygen** is carried
almost entirely (97 %) by **haemoglobin** as oxyhaemoglobin, only 3 % dissolved
in plasma. One haemoglobin molecule binds four O₂ molecules, and the
**oxygen dissociation curve** is sigmoid. A fall in pH, a rise in pCO₂ and a rise
in temperature shift the curve to the right — the **Bohr effect** — so that
haemoglobin unloads more oxygen exactly in the tissues that are working hardest.

**Carbon dioxide** is carried in three ways: about **70 % as bicarbonate**
(HCO₃⁻) in the plasma, after the reaction CO₂ + H₂O ⇌ H₂CO₃ ⇌ H⁺ + HCO₃⁻ inside
the red cell, catalysed by **carbonic anhydrase**; about **20–25 % as
carbamino-haemoglobin** bound to the globin part; and about **7 % dissolved** in
plasma.

::: example Worked example 8.2 — oxygen carrying capacity of blood
**Problem.** A healthy man has 15 g of haemoglobin per 100 ml of blood, and 1 g
of haemoglobin combines with 1.34 ml of O₂ at full saturation. His total blood
volume is 5 L. Find (a) the oxygen capacity of 100 ml of blood, (b) the total O₂
carried by haemoglobin in his body, and (c) the O₂ delivered to the tissues each
minute if 5 ml of O₂ leaves every 100 ml of blood and cardiac output is
5 L min⁻¹.

**Solution.**

(a) $1.34 \times 15 = 20.1\ \text{ml of O}_2$ per 100 ml of blood — the familiar
"20 volumes per cent".

(b) $5000\ \text{ml} \div 100 = 50$ units of 100 ml, so

$$ 50 \times 20.1 = 1005\ \text{ml} \approx 1.0\ \text{L of O}_2 $$

(c) Oxygen delivery $=$ cardiac output $\times$ arterio-venous O₂ difference

$$ = 5000\ \text{ml min}^{-1} \times \frac{5\ \text{ml}}{100\ \text{ml}} = 250\ \text{ml min}^{-1} $$

which matches the resting oxygen consumption of an adult, about 250 ml min⁻¹.
:::

Disorders of this system are common in Nepal's brick-kiln and city air: **asthma**
(bronchiolar spasm and inflammation), **emphysema** (alveolar walls destroyed by
smoking, so surface area collapses), **bronchitis**, **pneumonia** and
**occupational silicosis/asbestosis**.

## 8.3 Circulatory System

A human being is too large for diffusion alone. Oxygen would take years to
diffuse from the lung to the toe. The circulatory system solves this by bulk
flow: a pump, a closed network of tubes, and a fluid — **blood** — that carries
everything.

### Blood

Blood is a fluid connective tissue. An adult has about 5–6 L, which is 6–8 % of
body weight. Centrifuged, it separates into a straw-coloured **plasma** (55 %)
and **formed elements** (45 %); the packed-cell fraction is the **haematocrit**.

| Component | Share / count | Key features | Main function |
|---|---|---|---|
| Plasma | 55 % of blood | 90–92 % water; 6–8 % proteins (albumin, globulins, fibrinogen); salts, glucose, urea, hormones | transport medium; osmotic balance; clotting; immunity |
| Erythrocytes (RBC) | 5.0–5.5 million mm⁻³ | biconcave discs, 7 μm, **no nucleus** in mammals, life 120 days, made in red bone marrow, destroyed in spleen ("graveyard of RBC") | carry O₂ and some CO₂ as haemoglobin (12–16 g dl⁻¹) |
| Leucocytes (WBC) | 6000–8000 mm⁻³ | nucleated, colourless; **granulocytes**: neutrophil 60–65 %, eosinophil 2–3 %, basophil 0.5–1 %; **agranulocytes**: lymphocyte 20–25 %, monocyte 6–8 % | defence — phagocytosis, antibodies, allergy, inflammation |
| Thrombocytes (platelets) | 1.5–3.5 lakh mm⁻³ | cell fragments from megakaryocytes, no nucleus, life 5–9 days | release thromboplastin; start blood clotting |

**Clotting.** Injury exposes tissue and platelets release **thromboplastin**,
which with Ca²⁺ converts **prothrombin → thrombin**; thrombin converts the
soluble plasma protein **fibrinogen → fibrin**, whose threads trap blood cells
and form the clot. Vitamin K is needed by the liver to make prothrombin.

**Blood groups.** The ABO system depends on **antigens (agglutinogens)** on the
RBC surface and **antibodies (agglutinins)** in the plasma. Mixing an antigen
with its matching antibody makes the cells clump (**agglutination**), which can
kill the recipient.

| Group | Antigen on RBC | Antibody in plasma | Can donate to | Can receive from |
|---|---|---|---|---|
| A | A | anti-B (b) | A, AB | A, O |
| B | B | anti-A (a) | B, AB | B, O |
| AB | A and B | none | AB only | A, B, AB, O — **universal recipient** |
| O | none | anti-A and anti-B | A, B, AB, O — **universal donor** | O only |

The **Rh factor** is a separate antigen (D antigen) present in about 95 % of
Nepali people (Rh⁺). An Rh⁻ mother carrying an Rh⁺ foetus may be sensitised at
the first delivery and her anti-Rh antibodies can destroy the red cells of a
later Rh⁺ foetus — **erythroblastosis foetalis**, prevented by giving the mother
anti-Rh (anti-D) immunoglobulin within 72 hours of delivery.

::: caution "Universal donor" has limits
O⁻ blood has no A, B or D antigen, so it is safest in an emergency. But O plasma
carries **both** anti-A and anti-B antibodies, so only small volumes (packed
cells) are safe. Modern practice is always to cross-match.
:::

### Structure of the human heart

The heart is a hollow muscular organ the size of a closed fist (about 300 g),
lying in the thoracic cavity between the lungs, tilted so its apex points down
and to the left. It is enclosed in a double **pericardium** with pericardial
fluid between the layers, and its wall has three coats: outer **epicardium**,
thick middle **myocardium** of cardiac muscle, and inner **endocardium**.

```figure caption="Longitudinal (frontal) section of the human heart. Blue = deoxygenated blood, red = oxygenated. Note the left ventricular wall, about three times thicker than the right."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Ellipse, PathPatch
from matplotlib.path import Path

fig, ax = plt.subplots(figsize=(5.2, 4.6))
MUS = "#c98275"; MED = "#8a4a40"; BLUE = "#9fc0e0"; RED = "#eeb0a6"
VBLUE = "#4a67b8"; VRED = "#b03a3a"

def bez(pts, fc, ec, lw=1.2, z=3):
    assert (len(pts)-1) % 3 == 0, len(pts)
    ax.add_patch(PathPatch(Path(pts, [Path.MOVETO]+[Path.CURVE4]*(len(pts)-1)),
                           fc=fc, ec=ec, lw=lw, zorder=z))

def vessel(pts, c, w=7.0, z=5.5):
    x, y = np.array(pts).T
    ax.plot(x, y, color=MED, lw=w+1.6, solid_capstyle='round', zorder=z)
    ax.plot(x, y, color=c, lw=w, solid_capstyle='round', zorder=z+0.1)

def lab(txt, tip, tx, ty, ha='left', fs=6.2, c=INK):
    ax.annotate(txt, xy=tip, xytext=(tx, ty), fontsize=fs, color=c, ha=ha,
                va='center', zorder=30,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.65,
                                shrinkA=1.5, shrinkB=1.0))

# ---- great vessels (drawn first, behind the heart mass) ----
vessel([(0.55, 3.82), (0.46, 5.20), (0.30, 6.45), (-0.30, 7.32),
        (-1.35, 7.55), (-2.15, 7.00), (-2.48, 6.10), (-2.55, 4.90),
        (-2.58, 4.05)], "#d96a5a", w=7.4, z=5.5)          # aorta + arch
for bx in (-0.20, -0.70, -1.25):
    vessel([(bx, 7.34), (bx-0.05, 8.35)], "#d96a5a", w=4.0, z=5.3)
vessel([(-0.44, 3.80), (-0.34, 5.10), (-0.14, 5.90)], BLUE, w=6.6, z=5.6)
vessel([(-0.14, 5.90), (-0.95, 6.16), (-1.92, 6.28)], BLUE, w=5.4, z=5.6)
vessel([(-0.14, 5.90), (0.70, 6.20), (1.72, 6.32)], BLUE, w=5.4, z=5.6)
vessel([(-1.55, 6.95), (-1.52, 5.90), (-1.50, 5.05)], BLUE, w=6.2, z=5.6)
vessel([(-3.30, 2.05), (-2.85, 3.05), (-2.05, 3.92)], BLUE, w=6.2, z=5.6)
for (ys, ye) in [(5.45, 5.02), (4.20, 4.38)]:
    vessel([(3.20, ys), (2.55, (ys+ye)/2), (1.92, ye)], "#d96a5a", w=5.0, z=5.6)

# ---- heart muscle mass ----
OUT = [(-2.30, 5.30),
       (-2.55, 4.20), (-2.45, 2.70), (-1.70, 1.70),
       (-1.05, 0.90), (0.10, 0.20), (0.95, 0.45),
       (1.75, 0.68), (2.35, 2.20), (2.35, 3.70),
       (2.35, 4.75), (2.10, 5.50), (1.50, 5.60),
       (0.50, 5.78), (-1.40, 5.75), (-2.30, 5.30)]
bez(OUT, MUS, MED, lw=1.3, z=5)

RA = [(-2.02, 4.10), (-2.02, 4.90), (-1.65, 5.24), (-1.00, 5.28),
      (-0.78, 4.95), (-0.76, 4.05), (-1.00, 3.72), (-1.60, 3.68)]
LA = [(0.78, 4.10), (0.80, 4.95), (1.10, 5.26), (1.70, 5.22),
      (2.00, 4.88), (2.02, 4.05), (1.70, 3.70), (1.05, 3.68)]
RV = [(-1.78, 2.95), (-1.70, 3.35), (-0.28, 3.38), (-0.25, 1.85),
      (-0.62, 1.32), (-1.20, 1.50), (-1.62, 2.30)]
LV = [(0.38, 3.30), (1.24, 3.24), (1.40, 2.50), (1.20, 1.66),
      (0.92, 1.24), (0.64, 1.58), (0.40, 2.36)]
for poly, c in [(RA, BLUE), (LA, RED), (RV, BLUE), (LV, RED)]:
    ax.add_patch(Polygon(poly, closed=True, fc=c, ec=MED, lw=1.0, zorder=7))

# ---- valves ----
def av_valve(x0, x1, ytop, ybot, c):
    for xa, xb in [(x0, (x0+x1)/2), ((x0+x1)/2, x1)]:
        ax.add_patch(Polygon([(xa, ytop), (xb, ytop), ((xa+xb)/2, ybot)],
                             closed=True, fc="#fdf4ef", ec=MED, lw=0.9, zorder=8))
        for k in (0.25, 0.75):
            ax.plot([(xa+xb)/2, xa + (xb-xa)*k], [ybot, ybot-0.42],
                    color=MED, lw=0.5, zorder=8)
    ax.plot([x0+0.10, x1-0.10], [ybot-0.48, ybot-0.48], color="#a8625a",
            lw=3.0, zorder=8, solid_capstyle='round')
av_valve(-1.42, -0.34, 3.40, 2.78, MED)     # tricuspid
av_valve(0.42, 1.28, 3.34, 2.76, MED)       # bicuspid (mitral)
for (cx, cy) in [(-0.44, 3.70), (0.55, 3.76)]:
    for s in (-1, 1):
        u = np.linspace(0, 1, 40)
        xs = cx + s*0.21*u
        ax.plot(xs, cy - 0.17*np.sin(np.pi*u), color=MED, lw=1.2, zorder=9.2,
                solid_capstyle='round')
    ax.plot([cx-0.23, cx+0.23], [cy+0.02, cy+0.02], color=MED, lw=0.8,
            zorder=9.2)

# ---- flow arrows ----
def flow(p0, p1, c, z=12, lw=1.5):
    ax.annotate('', xy=p1, xytext=p0, zorder=z,
                arrowprops=dict(arrowstyle='-|>', color=c, lw=lw,
                                mutation_scale=9))
flow((-1.52, 5.85), (-1.50, 5.10), VBLUE)
flow((-2.62, 3.20), (-2.10, 3.82), VBLUE)
flow((-1.30, 4.20), (-1.05, 3.30), VBLUE)
flow((-1.10, 2.30), (-0.52, 3.55), VBLUE)
flow((-0.36, 4.70), (-0.24, 5.60), VBLUE)
flow((2.55, 4.80), (2.05, 4.55), VRED)
flow((1.42, 4.35), (1.12, 3.40), VRED)
flow((0.95, 2.40), (0.50, 3.44), VRED)
flow((0.46, 4.60), (0.36, 5.80), VRED)

# ---- labels ----
lab("aorta (to the body)", (-0.32, 7.36), -3.15, 8.25, ha='right')
lab("carotid / subclavian\nbranches", (-0.72, 8.15), 0.20, 8.42)
lab("superior vena cava", (-1.55, 6.70), -3.15, 7.15, ha='right')
lab("right pulmonary artery", (-1.55, 6.20), -3.15, 6.40, ha='right')
lab("right atrium", (-1.60, 4.70), -3.15, 5.05, ha='right')
lab("tricuspid valve\n(3 cusps)", (-0.95, 3.10), -3.15, 3.55, ha='right')
lab("right ventricle\n(thin wall)", (-1.05, 2.30), -3.15, 2.55, ha='right')
lab("inferior vena cava", (-2.95, 2.60), -3.15, 1.55, ha='right')
lab("pulmonary trunk", (-0.26, 5.45), 0.75, 6.95)
lab("left pulmonary artery", (1.30, 6.24), 2.15, 7.35)
lab("pulmonary veins (4)", (2.75, 5.30), 3.35, 6.35)
lab("left atrium", (1.45, 4.55), 3.35, 5.45)
lab("bicuspid (mitral) valve", (0.86, 3.05), 3.35, 4.20)
lab("semilunar valves", (0.52, 3.72), 3.35, 3.30)
lab("left ventricle —\nwall ≈ 3× thicker", (1.05, 2.10), 3.35, 2.30)
lab("interventricular\nseptum", (0.06, 2.20), 3.35, 1.20)
lab("apex of the heart", (0.95, 0.48), 3.35, 0.35)
lab("chordae tendineae\n+ papillary muscle", (-0.88, 2.40), -1.60, 0.45, ha='center')

ax.set_xlim(-6.20, 6.20); ax.set_ylim(-0.10, 8.90)
ax.set_aspect('equal'); ax.axis('off')
```

**Four chambers.** Two thin-walled **atria** (auricles) receive blood; two
thick-walled **ventricles** pump it. The **interatrial septum** and
**interventricular septum** separate the right (deoxygenated) side from the left
(oxygenated) side, so the two never mix. The left ventricle has a wall about
three times thicker than the right because it must push blood around the whole
body, not just to the lungs.

**Four valves**, all of which open only one way so that blood cannot flow back:

| Valve | Position | Cusps | Closes at |
|---|---|---|---|
| Tricuspid | right atrium → right ventricle | 3 | start of ventricular systole (1st sound) |
| Bicuspid (mitral) | left atrium → left ventricle | 2 | start of ventricular systole (1st sound) |
| Pulmonary semilunar | right ventricle → pulmonary trunk | 3 pocket-like | end of ventricular systole (2nd sound) |
| Aortic semilunar | left ventricle → aorta | 3 pocket-like | end of ventricular systole (2nd sound) |

The cusps of the AV valves are anchored by tendinous cords, the **chordae
tendineae**, to **papillary muscles** on the ventricle wall — they act like the
strings of a parachute, stopping the cusps from turning inside-out when the
ventricle contracts.

### Double circulation

```figure caption="Double circulation. Blood passes through the heart twice in one complete circuit: once in the pulmonary circuit and once in the systemic circuit."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

fig, ax = plt.subplots(figsize=(5.0, 3.4))
VB = "#4a67b8"; VR = "#b03a3a"

def box(x, y, w, h, txt, fc, ec, fs=7.0):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle="round,pad=0.02,rounding_size=0.10",
                 fc=fc, ec=ec, lw=1.1, zorder=3))
    ax.text(x+w/2, y+h/2, txt, fontsize=fs, color=INK, ha='center',
            va='center', zorder=4, linespacing=1.25)

box(1.05, 3.05, 1.90, 0.66, "LUNGS\ncapillaries of alveoli", "#eef4fb", "#4a67b8", 6.6)
box(1.05, 0.05, 1.90, 0.66, "BODY TISSUES\nsystemic capillaries", "#fdf1ee", "#b03a3a", 6.6)
box(0.30, 1.35, 1.35, 1.10, "RIGHT\nheart", "#cfdff0", "#4a67b8")
box(2.35, 1.35, 1.35, 1.10, "LEFT\nheart", "#f6cdc5", "#b03a3a")
ax.add_patch(Rectangle((0.22, 1.27), 3.56, 1.26, fill=False, ec=MUTED,
                       lw=0.9, ls=(0, (3, 2)), zorder=2))
ax.text(2.0, 2.66, "HEART", fontsize=7.4, color=INK, ha='center')

def arrow(p0, p1, c, rad=0.0, lw=1.8):
    ax.annotate('', xy=p1, xytext=p0, zorder=5,
                arrowprops=dict(arrowstyle='-|>', color=c, lw=lw,
                                mutation_scale=11,
                                connectionstyle=f"arc3,rad={rad}"))

arrow((0.98, 2.45), (1.35, 3.03), VB, rad=-0.25)
arrow((2.65, 3.03), (3.02, 2.47), VR, rad=-0.25)
arrow((3.02, 1.33), (2.65, 0.73), VR, rad=-0.25)
arrow((1.35, 0.73), (0.98, 1.33), VB, rad=-0.25)
ax.plot([2.00, 2.00], [1.32, 2.48], color=MUTED, lw=3.0, zorder=4,
        solid_capstyle='round')
ax.text(2.00, 1.14, "septum", fontsize=6.0, color=MUTED, ha='center',
        va='top', zorder=9)

ax.text(0.28, 2.95, "pulmonary\nartery\n(deoxygenated)", fontsize=6.2,
        color=VB, ha='center', va='center')
ax.text(3.74, 2.95, "pulmonary\nveins\n(oxygenated)", fontsize=6.2,
        color=VR, ha='center', va='center')
ax.text(3.76, 0.82, "aorta\n(oxygenated)", fontsize=6.2, color=VR,
        ha='center', va='center')
ax.text(0.26, 0.82, "venae cavae\n(deoxygenated)", fontsize=6.2, color=VB,
        ha='center', va='center')
ax.text(2.0, 3.92, "PULMONARY CIRCUIT  —  right ventricle → lungs → left atrium",
        fontsize=6.6, color=VB, ha='center')
ax.text(2.0, -0.32, "SYSTEMIC CIRCUIT  —  left ventricle → body → right atrium",
        fontsize=6.6, color=VR, ha='center')
ax.set_xlim(-1.30, 5.30); ax.set_ylim(-0.60, 4.15)
ax.set_aspect('equal'); ax.axis('off')
```

Because the blood passes through the heart **twice** in one complete circuit —
once as it goes to the lungs and once as it goes to the body — the human
circulation is called **double circulation**. It is also **closed** (blood stays
inside vessels) and **complete** (oxygenated and deoxygenated blood never mix).

Two special routes matter:

- **Coronary circulation** — the heart muscle cannot use the blood inside its
  own chambers. Coronary arteries branch from the base of the aorta to supply
  the myocardium; their blockage causes a heart attack.
- **Hepatic portal system** — blood from the stomach, intestine, pancreas and
  spleen goes first to the **liver** by the hepatic portal vein, so that absorbed
  food is processed and toxins removed before reaching the rest of the body. A
  *portal vein* is any vein that starts in capillaries and ends in capillaries.

| Feature | Artery | Vein | Capillary |
|---|---|---|---|
| Direction | away from heart | towards heart | between the two |
| Wall | thick, elastic, muscular | thinner, less elastic | one cell thick (endothelium only) |
| Lumen | narrow | wide | very narrow (7–8 μm) |
| Valves | absent (except at the heart) | present, prevent backflow | absent |
| Blood | oxygenated (except pulmonary artery) | deoxygenated (except pulmonary vein) | — |
| Pressure | high (~120/80 mmHg) | low (~10 mmHg) | falls 35 → 15 mmHg |

### The cardiac cycle

Cardiac muscle is **myogenic**: the beat starts inside the heart itself. The
**sino-atrial (SA) node**, a patch of modified cardiac muscle in the wall of the
right atrium near the opening of the superior vena cava, fires 70–75 times a
minute and is therefore the **pacemaker**. The impulse spreads over both atria to
the **atrio-ventricular (AV) node**, is delayed there by about 0.1 s (letting the
atria empty), then travels down the **bundle of His**, its two branches, and the
**Purkinje fibres** into the ventricle walls.

One cardiac cycle at 72 beats per minute lasts **0.8 s**:

| Phase | Duration | What happens |
|---|---|---|
| Atrial systole | 0.1 s | atria contract, pushing the last ~30 % of blood into the ventricles; AV valves open |
| Ventricular systole | 0.3 s | ventricles contract; AV valves shut (**"lubb"**, 1st sound); pressure rises; semilunar valves open and about 70 ml is ejected |
| Joint diastole | 0.4 s | all chambers relax; semilunar valves shut (**"dupp"**, 2nd sound); ventricles fill passively |

```figure caption="The cardiac cycle at 72 beats per minute: pressures in the aorta, left ventricle and left atrium, with left-ventricular volume below. AV = atrio-ventricular valve, SL = semilunar valve."
import numpy as np, matplotlib.pyplot as plt

fig, (ax, ax2) = plt.subplots(2, 1, figsize=(5.2, 3.4), sharex=True,
                              gridspec_kw=dict(height_ratios=[2.1, 1.0],
                                               hspace=0.10))
t = np.linspace(0, 0.8, 1600)

def pw(t, pts):
    """smooth piecewise curve through (time, value) knots"""
    tk = np.array([p[0] for p in pts]); vk = np.array([p[1] for p in pts])
    out = np.interp(t, tk, vk)
    for i in range(len(tk)-1):
        m = (t >= tk[i]) & (t <= tk[i+1])
        u = (t[m]-tk[i])/(tk[i+1]-tk[i])
        out[m] = vk[i] + (vk[i+1]-vk[i])*(0.5-0.5*np.cos(np.pi*u))
    return out

LV = pw(t, [(0.0, 5), (0.06, 9), (0.10, 7), (0.13, 45), (0.155, 82),
            (0.20, 115), (0.26, 120), (0.33, 100), (0.36, 60), (0.40, 12),
            (0.44, 3), (0.55, 4), (0.70, 5), (0.80, 6)])
AO = pw(t, [(0.0, 84), (0.10, 81), (0.155, 80), (0.20, 112), (0.26, 120),
            (0.33, 100), (0.355, 96), (0.375, 101), (0.44, 96), (0.60, 90),
            (0.80, 84)])
AT = pw(t, [(0.0, 5), (0.05, 11), (0.10, 6), (0.17, 9), (0.24, 5),
            (0.34, 3), (0.46, 10), (0.55, 7), (0.70, 5), (0.80, 5)])
VOL = pw(t, [(0.0, 110), (0.09, 130), (0.13, 130), (0.155, 130), (0.22, 100),
             (0.30, 66), (0.345, 60), (0.40, 60), (0.46, 78), (0.55, 98),
             (0.70, 108), (0.80, 110)])

ax.plot(t, AO, color=SERIES[1], lw=1.6, label='aorta')
ax.plot(t, LV, color=ACCENT, lw=1.7, label='left ventricle')
ax.plot(t, AT, color=SERIES[2], lw=1.3, label='left atrium')
for x in (0.10, 0.155, 0.335, 0.40):
    for a in (ax, ax2):
        a.axvline(x, color=MUTED, lw=0.7, ls=(0, (3, 2)), zorder=1)
ax.set_ylabel('pressure (mmHg)')
ax.set_ylim(-6, 200); ax.set_xlim(0, 0.8)
ax.legend(loc='center right', bbox_to_anchor=(1.005, 0.30), ncol=1,
          fontsize=6.4, handlelength=1.4, labelspacing=0.35)
for xx, txt in [(0.05, 'atrial\nsystole'), (0.128, 'IVC'),
                (0.245, 'ejection'), (0.368, 'IVR'), (0.655, 'ventricular filling')]:
    ax.text(xx, 184, txt, fontsize=5.9, color=MUTED, ha='center', va='center')
ax.annotate('AV valves shut\n(1st sound "lubb")', xy=(0.107, 24),
            xytext=(0.185, 44), fontsize=6.0, color=INK, ha='left',
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.7,
                            mutation_scale=7))
ax.annotate('SL valves shut\n(2nd sound "dupp")\ndicrotic notch', xy=(0.358, 97),
            xytext=(0.50, 162), fontsize=6.0, color=INK, ha='center', va='top',
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.7,
                            mutation_scale=7))
ax.annotate('SL valves open', xy=(0.158, 81), xytext=(0.006, 132),
            fontsize=6.0, color=INK, ha='left',
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.7,
                            mutation_scale=7))
ax.spines[['top', 'right']].set_visible(False)
ax.grid(True, axis='y', alpha=0.35)

ax2.plot(t, VOL, color=SERIES[4], lw=1.6)
ax2.axhline(130, color=MUTED, lw=0.7, ls=':')
ax2.axhline(60, color=MUTED, lw=0.7, ls=':')
ax2.text(0.79, 134, 'EDV 130 ml', fontsize=6.0, color=MUTED, ha='right')
ax2.text(0.79, 46, 'ESV 60 ml', fontsize=6.0, color=MUTED, ha='right')
ax2.annotate('', xy=(0.432, 60), xytext=(0.432, 130),
             arrowprops=dict(arrowstyle='<|-|>', color=SERIES[4], lw=1.0,
                             mutation_scale=7))
ax2.text(0.452, 108, 'stroke volume 70 ml', fontsize=6.1, color=SERIES[4],
         va='center')
ax2.set_ylabel('LV volume\n(ml)', fontsize=7.6)
ax2.set_xlabel('time (s)')
ax2.set_ylim(30, 158); ax2.set_yticks([60, 100, 130])
ax2.spines[['top', 'right']].set_visible(False)
ax2.grid(True, axis='y', alpha=0.35)
```

::: example Worked example 8.3 — cardiac output
**Problem.** A patient at the Shahid Gangalal Heart Centre has a heart rate of
72 beats per minute, an end-diastolic volume of 130 ml and an end-systolic volume
of 60 ml. Find (a) the stroke volume, (b) the cardiac output, (c) the ejection
fraction, and (d) the cardiac output when exercise raises the heart rate to
150 min⁻¹ and the stroke volume to 110 ml.

**Solution.**

(a) $SV = EDV - ESV = 130 - 60 = 70\ \text{ml}$

(b) $CO = SV \times HR = 70 \times 72 = 5040\ \text{ml min}^{-1} \approx 5.0\ \text{L min}^{-1}$

(c) Ejection fraction $= \dfrac{SV}{EDV}\times 100 = \dfrac{70}{130}\times100 = 53.8\ \%$
(normal is 55–70 %; below 40 % indicates heart failure).

(d) $CO = 110 \times 150 = 16\,500\ \text{ml min}^{-1} = 16.5\ \text{L min}^{-1}$ —
more than **three times** the resting value. This extra flow is the whole point
of a trained heart.
:::

### Electrocardiogram (ECG)

The electrical changes that sweep the heart can be picked up from the skin. The
standard trace of one beat has three deflections.

```figure caption="(a) The conducting system of the heart. (b) A normal ECG: P = atrial depolarisation, QRS = ventricular depolarisation, T = ventricular repolarisation."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, PathPatch
from matplotlib.path import Path

fig, (axA, axB) = plt.subplots(1, 2, figsize=(5.2, 2.9),
                               gridspec_kw=dict(width_ratios=[0.78, 1.32]))

# ---------- (a) conducting system ----------
ax = axA
OUT = [(-1.15, 2.62),
       (-1.28, 2.05), (-1.22, 1.32), (-0.85, 0.82),
       (-0.52, 0.42), (0.05, 0.05), (0.48, 0.18),
       (0.88, 0.30), (1.18, 1.08), (1.18, 1.82),
       (1.18, 2.35), (1.05, 2.72), (0.75, 2.78),
       (0.25, 2.88), (-0.70, 2.86), (-1.15, 2.62)]
ax.add_patch(PathPatch(Path(OUT, [Path.MOVETO]+[Path.CURVE4]*15),
                       fc="#f3ded9", ec="#a8625a", lw=1.1, zorder=2))
ax.plot([-0.02, 0.05, 0.10], [2.70, 1.50, 0.40], color="#a8625a", lw=0.9, zorder=3)
ax.plot([-1.20, 1.16], [1.72, 1.72], color="#a8625a", lw=0.9, zorder=3)
# SA node, AV node, bundle, Purkinje
ax.add_patch(Circle((-0.72, 2.46), 0.115, fc="#b8860b", ec=INK, lw=0.6, zorder=6))
ax.add_patch(Circle((-0.08, 1.80), 0.095, fc="#b8860b", ec=INK, lw=0.6, zorder=6))
ax.plot([-0.06, 0.03, 0.06], [1.72, 1.30, 0.95], color="#b8860b", lw=1.6, zorder=5)
for s in (-1, 1):
    xs = [0.06, 0.06+s*0.16, 0.06+s*0.42, 0.06+s*0.66]
    ys = [0.95, 0.74, 0.50, 0.62]
    ax.plot(xs, ys, color="#b8860b", lw=1.3, zorder=5)
    for k in range(3):
        ax.plot([xs[-1], xs[-1]+s*0.12], [ys[-1]+0.22*k, ys[-1]+0.40+0.22*k],
                color="#b8860b", lw=0.8, zorder=5)
for r in (0.20, 0.36, 0.52):
    th = np.linspace(-0.9*np.pi, 0.5*np.pi, 60)
    ax.plot(-0.72 + r*np.cos(th), 2.46 + r*0.75*np.sin(th), color="#b8860b",
            lw=0.5, ls=(0, (2, 2)), zorder=4)
def la(txt, tip, tx, ty, ha='left'):
    ax.annotate(txt, xy=tip, xytext=(tx, ty), fontsize=6.0, color=INK, ha=ha,
                va='center', zorder=9,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6,
                                shrinkA=1.5, shrinkB=1.0))
la("SA node\n(pacemaker)", (-0.84, 2.50), -1.45, 3.25, ha='center')
la("AV node", (-0.18, 1.86), -1.55, 1.95, ha='right')
la("bundle of His", (0.04, 1.20), 1.45, 1.55)
la("Purkinje\nfibres", (0.62, 0.72), 1.55, 0.35)
ax.text(0.0, 3.62, "(a) conducting system", ha='center', fontsize=7.2, color=INK)
ax.set_xlim(-2.75, 2.75); ax.set_ylim(-0.15, 3.85)
ax.set_aspect('equal'); ax.axis('off')

# ---------- (b) ECG trace ----------
ax = axB
t = np.linspace(0, 1.75, 3000)
def g(c, w, a):
    return a*np.exp(-0.5*((t - c)/w)**2)
def beat(t0):
    return (g(t0+0.10, 0.028, 0.16) - g(t0+0.215, 0.009, 0.09)
            + g(t0+0.242, 0.011, 1.00) - g(t0+0.272, 0.012, 0.22)
            + g(t0+0.42, 0.045, 0.30))
v = beat(0.0) + beat(0.8)
ax.plot(t, v, color=ACCENT, lw=1.5, zorder=4)
ax.axhline(0, color=MUTED, lw=0.7, zorder=2)
for x, y, s, dy, ha in [(0.10, 0.17, 'P', 0.13, 'center'),
                        (0.196, -0.10, 'Q', -0.13, 'right'),
                        (0.242, 1.01, 'R', 0.10, 'center'),
                        (0.300, -0.24, 'S', -0.13, 'left'),
                        (0.42, 0.31, 'T', 0.13, 'center')]:
    ax.text(x, y+dy, s, fontsize=8.0, color=INK, ha=ha,
            va='bottom' if dy > 0 else 'top', fontweight='bold')
ax.annotate('', xy=(0.058, -0.42), xytext=(0.215, -0.42),
            arrowprops=dict(arrowstyle='<|-|>', color=SERIES[2], lw=0.9,
                            mutation_scale=6))
ax.text(0.136, -0.55, 'P–R 0.16 s', fontsize=6.0, color=SERIES[2], ha='center')
ax.annotate('', xy=(0.212, -0.72), xytext=(0.285, -0.72),
            arrowprops=dict(arrowstyle='<|-|>', color=SERIES[3], lw=0.9,
                            mutation_scale=6))
ax.text(0.40, -0.72, 'QRS 0.08 s', fontsize=6.0, color=SERIES[3], ha='left',
        va='center')
ax.annotate('', xy=(0.242, 1.32), xytext=(1.042, 1.32),
            arrowprops=dict(arrowstyle='<|-|>', color=SERIES[4], lw=0.9,
                            mutation_scale=6))
ax.text(0.64, 1.39, 'R–R = 0.8 s  →  heart rate 75 min⁻¹', fontsize=6.2,
        color=SERIES[4], ha='center')
ax.set_xlim(-0.03, 1.60); ax.set_ylim(-0.95, 1.68)
ax.set_xlabel('time (s)', fontsize=7.6)
ax.set_yticks([]); ax.set_xticks([0, 0.4, 0.8, 1.2, 1.6])
ax.spines[['top', 'right', 'left']].set_visible(False)
ax.set_title("(b) normal electrocardiogram", fontsize=7.2, color=INK, pad=4)
```

| Wave | Electrical event | Mechanical event that follows |
|---|---|---|
| **P** | depolarisation of the atria | atrial systole |
| **QRS complex** | depolarisation of the ventricles (atrial repolarisation is hidden inside it) | ventricular systole begins |
| **T** | repolarisation of the ventricles | ventricular systole ends |

Counting the **R–R interval** gives the heart rate directly: heart rate = 60 ÷
(R–R in seconds). A raised ST segment, an absent P wave or a widened QRS each
point to a specific disease, which is why the ECG is the first test done in a
suspected heart attack.

**Blood pressure** is the force blood exerts on the artery wall, measured with a
sphygmomanometer over the brachial artery and written systolic/diastolic. Normal
adult value is **120/80 mmHg**; persistently above 140/90 mmHg is
**hypertension**, a leading cause of stroke and kidney failure in Nepal.

::: caution Cardiac output is *not* the heart rate
Cardiac output has units of volume per time (L min⁻¹), not beats per minute. An
athlete has a *low* resting heart rate (50 min⁻¹) but a *normal* cardiac output,
because the stroke volume is large. Always write $CO = SV \times HR$.
:::

## 8.4 Excretory System

Every reaction in the body leaves waste. Deamination of surplus amino acids in
the liver produces **ammonia** (NH₃), which is extremely toxic and very soluble;
the liver at once converts it to **urea** through the ornithine cycle. Because
humans excrete nitrogen mainly as urea, we are **ureotelic**. Bony fish, which
have unlimited water, excrete ammonia directly (**ammonotelic**); birds, reptiles
and insects, which must save water, excrete almost insoluble uric acid
(**uricotelic**).

| Organ | Substance excreted |
|---|---|
| Kidneys | urea, uric acid, creatinine, excess water, salts, drugs |
| Lungs | CO₂ and water vapour |
| Skin (sweat glands) | water, NaCl, traces of urea and lactic acid |
| Liver | bile pigments (bilirubin, biliverdin), cholesterol, excess metals |
| Large intestine | excess Ca²⁺, Fe²⁺ (this is *egestion* for undigested food) |

### The urinary system and the kidney

```figure caption="(a) The human urinary system, anterior view. (b) Longitudinal section of a kidney."
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Circle, Polygon, Ellipse

fig, (axA, axB) = plt.subplots(1, 2, figsize=(5.2, 3.4),
                               gridspec_kw=dict(width_ratios=[1.0, 1.28],
                                                wspace=0.06))
CORT = "#f1d8d1"; MED = "#d79a90"; EDGE = "#9d5a52"
RED = "#c0392b"; BLU = "#1d6fb8"; PEL = "#fbf3de"

def bean(cx, cy, sx, sy, mirror=False):
    P = [(0.00, 1.00),
         (-0.62, 0.98), (-0.98, 0.52), (-0.98, 0.00),
         (-0.98, -0.52), (-0.62, -0.98), (0.00, -1.00),
         (0.46, -1.00), (0.74, -0.66), (0.56, -0.33),
         (0.36, -0.10), (0.36, 0.10), (0.56, 0.33),
         (0.74, 0.66), (0.46, 1.00), (0.00, 1.00)]
    m = -1.0 if mirror else 1.0
    return [(cx + m*x*sx, cy + y*sy) for x, y in P]

def kid(ax, cx, cy, sx, sy, mirror=False, fc=CORT, lw=1.1, z=3):
    pts = bean(cx, cy, sx, sy, mirror)
    ax.add_patch(PathPatch(Path(pts, [Path.MOVETO]+[Path.CURVE4]*15),
                           fc=fc, ec=EDGE, lw=lw, zorder=z))

def tube(ax, pts, w=5.0, c=EDGE, l="#fdf7ef", z=4):
    x, y = np.array(pts).T
    ax.plot(x, y, color=c, lw=w, solid_capstyle='round', zorder=z)
    ax.plot(x, y, color=l, lw=w*0.5, solid_capstyle='round', zorder=z+0.1)

# ============================ (a) urinary system
ax = axA
def la(txt, tip, tx, ty, ha='left', fs=5.9):
    ax.annotate(txt, xy=tip, xytext=(tx, ty), fontsize=fs, color=INK, ha=ha,
                va='center', zorder=15,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6,
                                shrinkA=1.5, shrinkB=1.0))
ax.plot([0.34, 0.34], [1.55, 6.30], color=RED, lw=3.4, zorder=2,
        solid_capstyle='round')
ax.plot([-0.34, -0.34], [1.55, 6.30], color=BLU, lw=3.4, zorder=2,
        solid_capstyle='round')
kid(ax, -1.62, 4.05, 0.72, 1.00, mirror=False)
kid(ax, 1.62, 4.35, 0.72, 1.00, mirror=True)
for s, cy in ((-1, 5.20), (1, 5.50)):
    ax.add_patch(Polygon([(s*1.62, cy+0.40), (s*1.62-0.52, cy-0.14),
                          (s*1.62+0.52, cy-0.14)], closed=True,
                         fc="#e9d9a8", ec="#a08a3c", lw=0.9, zorder=4))
ax.plot([0.34, -1.24], [4.30, 4.16], color=RED, lw=2.2, zorder=3)
ax.plot([-0.34, -1.24], [3.88, 3.92], color=BLU, lw=2.2, zorder=3)
ax.plot([0.34, 1.24], [4.62, 4.46], color=RED, lw=2.2, zorder=3)
ax.plot([-0.34, 1.24], [4.16, 4.22], color=BLU, lw=2.2, zorder=3)
tube(ax, [(-1.26, 3.82), (-1.26, 3.05), (-1.00, 2.30), (-0.70, 1.72)], w=4.2)
tube(ax, [(1.26, 4.12), (1.26, 3.15), (1.00, 2.30), (0.70, 1.72)], w=4.2)
BL = [(0.00, 1.86),
      (0.62, 1.84), (1.05, 1.42), (1.05, 0.92),
      (1.05, 0.34), (0.58, 0.02), (0.00, 0.02),
      (-0.58, 0.02), (-1.05, 0.34), (-1.05, 0.92),
      (-1.05, 1.42), (-0.62, 1.84), (0.00, 1.86)]
ax.add_patch(PathPatch(Path(BL, [Path.MOVETO]+[Path.CURVE4]*12),
                       fc="#f8e7c8", ec="#a8823c", lw=1.1, zorder=3))
tube(ax, [(0.0, 0.18), (0.0, -0.70)], w=4.6)
la("adrenal gland", (-1.62, 5.08), -2.20, 6.30, ha='center')
la("kidney", (-2.20, 3.80), -2.60, 4.95, ha='center')
la("renal artery", (0.80, 4.54), 2.50, 6.30, ha='center')
la("renal vein", (0.55, 4.18), 2.62, 4.25, ha='center')
la("ureter", (1.14, 2.90), 2.38, 3.05, ha='center')
la("urinary\nbladder", (0.90, 1.24), 2.30, 1.55, ha='center')
la("urethra", (0.0, -0.45), 1.55, -0.60, ha='center')
la("abdominal aorta", (0.34, 6.10), 1.05, 6.95, ha='center')
la("inferior\nvena cava", (-0.34, 2.45), -1.95, 1.95, ha='center')
ax.text(-0.2, 7.85, "(a) urinary system", ha='center', fontsize=7.2, color=INK)
ax.set_xlim(-3.45, 3.45); ax.set_ylim(-1.30, 8.20)
ax.set_aspect('equal'); ax.axis('off')

# ============================ (b) kidney L.S.
ax = axB
def lb(txt, tip, tx, ty, ha='left', fs=5.9):
    ax.annotate(txt, xy=tip, xytext=(tx, ty), fontsize=fs, color=INK, ha=ha,
                va='center', zorder=15,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6,
                                shrinkA=1.5, shrinkB=1.0))
kid(ax, 0, 0, 2.55, 3.25, fc=CORT, lw=1.3, z=3)
PYR = [(2.10, 2.72, 1.52, -0.90), (1.05, 1.78, 0.52, -1.48),
       (0.00, 0.64, -0.64, -1.66), (-1.05, -0.52, -1.78, -1.48),
       (-2.10, -1.52, -2.72, -0.90)]
for ay, by1, by2, bx in PYR:
    ax.add_patch(Polygon([(0.36, ay), (bx, by1), (bx, by2)], closed=True,
                         fc=MED, ec=EDGE, lw=0.8, zorder=4))
PELV = [(0.22, 2.55), (0.22, -2.55), (0.95, -0.52), (1.62, -0.40),
        (1.62, 0.40), (0.95, 0.52)]
ax.add_patch(Polygon(PELV, closed=True, fc=PEL, ec="#a8823c", lw=1.0, zorder=5))
for ay, *_ in PYR:
    ax.add_patch(Ellipse((0.30, ay), 0.34, 0.46, fc=PEL, ec="#a8823c",
                         lw=0.7, zorder=6))
ax.plot([1.55, 3.25], [0.05, 0.05], color="#a8823c", lw=4.4, zorder=5,
        solid_capstyle='round')
ax.plot([1.55, 3.25], [0.05, 0.05], color=PEL, lw=2.2, zorder=5.1,
        solid_capstyle='round')
ax.plot([1.18, 3.25], [0.78, 1.95], color=RED, lw=3.0, zorder=6,
        solid_capstyle='round')
ax.plot([1.18, 3.25], [-0.72, -1.95], color=BLU, lw=3.0, zorder=6,
        solid_capstyle='round')
lb("fibrous capsule", (-2.00, -2.05), -3.85, -3.45, ha='center')
lb("cortex", (-2.10, 0.55), -4.05, 1.35, ha='center')
lb("medulla\n(renal pyramid)", (-0.90, -0.10), -3.95, -0.60, ha='center')
lb("renal column", (-1.15, -1.02), -4.00, -2.45, ha='center')
lb("renal papilla\n+ minor calyx", (0.30, -1.05), 2.55, -3.05, ha='center')
lb("renal pelvis", (0.70, 1.55), 3.25, 3.30, ha='center')
lb("renal artery", (2.30, 1.35), 4.35, 2.20, ha='left', fs=5.9)
lb("renal vein", (2.30, -1.35), 4.35, -1.15, ha='left', fs=5.9)
lb("ureter", (2.85, 0.05), 4.35, 0.45, ha='left', fs=5.9)
ax.text(0.0, 4.35, "(b) kidney in L.S.", ha='center', fontsize=7.2, color=INK)
ax.set_xlim(-4.95, 6.35); ax.set_ylim(-4.05, 4.75)
ax.set_aspect('equal'); ax.axis('off')
```

Each kidney is a dark-red bean about 11 cm × 6 cm × 3 cm weighing roughly 150 g,
lying against the back wall of the abdomen at the level of the last thoracic and
first three lumbar vertebrae. The right kidney sits slightly lower because the
liver is above it. A section shows, from outside in:

- **Fibrous capsule** — tough protective coat.
- **Cortex** — the outer granular zone containing all the renal corpuscles.
- **Medulla** — 8–18 striated **renal pyramids**; each pyramid ends in a
  **renal papilla**. Cortical tissue dipping between pyramids forms the
  **renal columns of Bertini**.
- **Pelvis** — the funnel that collects urine. Each papilla drains into a
  **minor calyx**; minor calyces join into 2–3 **major calyces**, and these into
  the pelvis, which narrows into the **ureter**.

### The nephron

```figure caption="A nephron and its blood supply. Osmolarity of the medullary fluid rises from 300 to 1200 mOsm L$^{-1}$ — the counter-current gradient that lets us make concentrated urine."
from matplotlib.patches import Wedge, Circle, Rectangle

fig, ax = plt.subplots(figsize=(5.2, 4.5))
TUB = "#8a6a3a"; LUM = "#fdf6e6"; RED = "#c0392b"; BLU = "#1d6fb8"
GRN = "#2e8b57"; ORG = "#c97b1d"; FIL = "#4a67b8"

ax.add_patch(Rectangle((-6.90, 0.0), 12.80, 4.50, fc="#f7e7e3", ec='none', zorder=0))
ax.add_patch(Rectangle((-6.90, -7.00), 12.80, 7.00, fc="#e9cfc8", ec='none', zorder=0))
ax.plot([-6.90, 5.90], [0, 0], color=MUTED, lw=0.8, ls=(0, (4, 3)), zorder=1)
ax.text(-6.80, 4.35, "CORTEX", fontsize=6.4, color="#8a5a52", ha='left')
ax.text(-6.80, -6.80, "MEDULLA", fontsize=6.4, color="#8a5a52", ha='left')

def tube(pts, w=6.0, c=TUB, l=LUM, z=5):
    x, y = np.array(pts).T
    ax.plot(x, y, color=c, lw=w, solid_capstyle='round', zorder=z)
    ax.plot(x, y, color=l, lw=w*0.48, solid_capstyle='round', zorder=z+0.1)

def wavy(x0, x1, y0, y1, n, amp, npts=300):
    t = np.linspace(0, 1, npts)
    return list(zip(x0 + (x1-x0)*t, y0 + (y1-y0)*t + amp*np.sin(2*np.pi*n*t)))

GX, GY = -4.60, 2.60
ax.add_patch(Wedge((GX, GY), 0.90, 46, 314, width=0.18, fc="#e7ecf5",
                   ec="#4a67b8", lw=1.0, zorder=4))
for k in range(6):
    a = k*np.pi/3.0
    ax.add_patch(Circle((GX + 0.21*np.cos(a), GY + 0.21*np.sin(a)), 0.33,
                        fill=False, ec=RED, lw=1.0, zorder=6))
ax.plot([-6.55, -5.65, -5.10], [3.62, 3.22, 2.96], color=RED, lw=2.6,
        zorder=3, solid_capstyle='round')
ax.plot([-4.18, -3.58, -3.12], [3.30, 3.62, 3.28], color=RED, lw=1.5,
        zorder=3, solid_capstyle='round')

tube(wavy(-3.78, -2.55, 2.50, 2.12, 1.5, 0.42))
DES, ASC = -2.25, -0.75
tube([(-2.55, 2.12), (-2.35, 1.55), (DES, 0.80), (DES, -5.05)])
tube([(DES, -5.05), (DES + 0.10, -5.62), (ASC - 0.10, -5.62), (ASC, -5.05)])
tube([(ASC, -5.05), (ASC, 0.80), (ASC + 0.13, 1.60), (ASC + 0.27, 2.08)])
tube(wavy(-0.40, 1.20, 2.12, 2.42, 1.5, 0.38))
tube([(1.20, 2.42), (1.55, 1.80), (1.80, 0.60), (1.92, -5.40), (1.80, -6.10)],
     w=8.0)
ax.annotate('', xy=(1.82, -6.62), xytext=(1.81, -6.15), zorder=6,
            arrowprops=dict(arrowstyle='-|>', color=TUB, lw=1.0,
                            mutation_scale=8))

vr = np.linspace(0, 1, 220)
ax.plot(0.28 + 0.10*np.sin(2*np.pi*3*vr), 0.45 - 5.25*vr, color=RED, lw=1.0,
        alpha=0.85, zorder=2)
ax.plot(1.05 + 0.10*np.sin(2*np.pi*3*vr), -4.80 + 5.25*vr, color=BLU, lw=1.0,
        alpha=0.85, zorder=2)
ax.plot([0.28, 1.05], [-4.80, -4.80], color=BLU, lw=1.0, alpha=0.85, zorder=2)

def lab(txt, tip, tx, ty, ha='left', fs=6.0, c=INK):
    ax.annotate(txt, xy=tip, xytext=(tx, ty), fontsize=fs, color=c, ha=ha,
                va='center', zorder=20,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.65,
                                shrinkA=2.0, shrinkB=1.0))

lab("afferent arteriole", (-6.02, 3.40), -6.80, 4.10, c=RED)
lab("efferent arteriole", (-3.52, 3.62), -3.98, 3.98, c=RED)
lab("proximal convoluted tubule (PCT)", (-3.15, 2.88), -1.72, 4.30)
lab("glomerulus", (-4.95, 2.34), -6.88, 2.14, fs=5.9, c=RED)
lab("Bowman's\ncapsule", (-5.22, 2.06), -6.80, 1.35)
lab("distal convoluted\ntubule (DCT)", (0.72, 2.62), 2.35, 3.45)
lab("collecting duct", (1.88, -1.05), 2.75, -0.35)
lab("vasa recta", (1.08, -4.05), 2.75, -4.05, c=BLU)
ax.text(-2.95, -2.40, "descending limb — water permeable", fontsize=5.8,
        color=INK, rotation=90, ha='center', va='center', zorder=20)
ax.text(-1.50, -2.40, "ascending limb — pumps out Na⁺, Cl⁻", fontsize=5.8,
        color=INK, rotation=90, ha='center', va='center', zorder=20)
ax.text(-1.50, -6.25, "loop of Henle", fontsize=6.4, color=INK, ha='center')
ax.text(2.35, -6.35, "urine → minor calyx", fontsize=6.0, color=TUB, ha='left')

def step(n, txt, tip, tx, ty, col, ha='left'):
    ax.annotate(f"{n}. {txt}", xy=tip, xytext=(tx, ty), fontsize=6.1,
                color=col, ha=ha, va='center', zorder=21,
                arrowprops=dict(arrowstyle='-|>', color=col, lw=0.9,
                                mutation_scale=7, shrinkA=2.0, shrinkB=1.0))

step(1, "ultrafiltration", (-4.86, 1.88), -6.80, 0.90, FIL)
step(2, "selective reabsorption\n(70–80 % of the filtrate)", (-3.30, 2.06),
     -2.50, 0.42, ORG, ha='right')
step(3, "tubular secretion\n(H⁺, K⁺, NH₃, drugs)", (0.48, 2.18), 2.35, 1.55, GRN)
step(4, "water reabsorption\nunder ADH", (1.98, -2.72), 2.75, -2.15, ORG)

for y, v in ((-0.55, "300"), (-2.20, "600"), (-3.85, "900"),
             (-5.55, "1200 mOsm L⁻¹")):
    ax.text(-6.35, y, v, fontsize=5.8, color="#8a5a52", ha='left')
ax.annotate('', xy=(-6.55, -5.80), xytext=(-6.55, -0.30), zorder=3,
            arrowprops=dict(arrowstyle='-|>', color="#8a5a52", lw=0.9,
                            mutation_scale=7))

ax.set_xlim(-6.90, 5.90); ax.set_ylim(-7.00, 4.50)
ax.set_aspect('equal'); ax.axis('off')
```

The **nephron** is the structural and functional unit of the kidney; each kidney
has about **1 million** of them. A nephron has two parts:

1. **Malpighian body (renal corpuscle)** — the **glomerulus**, a knot of about
   50 capillaries, cupped inside the double-walled **Bowman's capsule**.
2. **Renal tubule** — proximal convoluted tubule (PCT) → loop of Henle
   (descending + ascending limb) → distal convoluted tubule (DCT) → collecting
   duct.

About 85 % are **cortical nephrons**, with short loops that barely enter the
medulla. The remaining 15 % are **juxtamedullary nephrons**, whose long loops
plunge deep into the medulla; these are the ones that make concentrated urine.

The blood supply is unusual. The **afferent arteriole** entering the glomerulus
is **wider** than the **efferent arteriole** leaving it. Blood therefore piles up
inside the glomerulus and the pressure there stays high — this is what drives
filtration. The efferent arteriole then breaks up again into **peritubular
capillaries** around the PCT and DCT, and into the hairpin **vasa recta** around
the loop of Henle. Two capillary beds in series like this make a **portal
system** (the renal portal system of the kidney).

### Urine formation

**Step 1 — Ultrafiltration.** Blood pressure in the glomerulus forces water and
all small solutes through three layers (capillary endothelium → basement
membrane → podocytes of the capsule) into the capsular space. Blood cells and
plasma proteins are too big and stay behind. The driving force is the **net
filtration pressure**:

$$ \text{NFP} = P_{gc} - P_{cs} - \pi_{gc} = 55 - 15 - 30 = 10\ \text{mmHg} $$

where $P_{gc}$ is glomerular capillary hydrostatic pressure, $P_{cs}$ the
hydrostatic pressure of the fluid already in the capsule and $\pi_{gc}$ the
colloid osmotic (oncotic) pressure of the plasma proteins. The **glomerular
filtration rate (GFR)** in a healthy adult is **125 ml min⁻¹**, that is about
**180 litres per day** of filtrate — yet only 1–1.5 L leaves as urine, so
**about 99 % is reabsorbed**.

**Step 2 — Selective reabsorption.** Useful substances are taken back into the
peritubular blood.

| Region | Reabsorbed | Mechanism |
|---|---|---|
| **PCT** (70–80 % of filtrate) | all glucose and amino acids, 70 % Na⁺ and water, HCO₃⁻ | active transport + osmosis; microvilli give a huge surface |
| **Descending limb** | water only | osmosis into the hypertonic medulla |
| **Ascending limb** | Na⁺, Cl⁻ (pumped out); **impermeable to water** | active transport |
| **DCT** | Na⁺ (under aldosterone), water (under ADH) | selective, hormone-controlled |
| **Collecting duct** | water (under ADH), urea | osmosis |

**Step 3 — Tubular secretion.** The tubule cells actively add H⁺, K⁺, NH₃,
creatinine and many drugs (penicillin, aspirin) from the blood into the filtrate.
Secretion of H⁺ and NH₃ is how the kidney keeps blood pH near 7.4.

::: key Counter-current multiplier
The ascending limb pumps Na⁺ and Cl⁻ out but will not let water follow. Salt
therefore piles up in the medullary interstitium while the descending limb loses
water into it. Because the two limbs run **in opposite directions** side by side,
a small difference at each level is *multiplied* along the loop, building a
gradient from **300 mOsm L⁻¹** at the cortex to **1200 mOsm L⁻¹** at the papilla.
The **vasa recta** run counter-current too, so they remove reabsorbed water
without washing the salt away. The collecting duct then passes through this
gradient, and water leaves it by osmosis — which is how urine four times more
concentrated than blood can be produced.
:::

::: example Worked example 8.4 — GFR and filtration fraction
**Problem.** Renal blood flow is 1200 ml min⁻¹ and the haematocrit is 45 %. If
the glomerular filtration rate is 125 ml min⁻¹, find (i) the renal plasma flow,
(ii) the filtration fraction, and (iii) the volume filtered in 24 hours.

**Solution.**
(i) Plasma is the non-cell fraction, so plasma = (100 − 45) % = 55 % of blood.

$$ \text{RPF} = 1200 \times 0.55 = 660\ \text{ml min}^{-1} $$

(ii) The filtration fraction is the part of that plasma which actually filters:

$$ FF = \frac{GFR}{RPF} = \frac{125}{660} = 0.189 \approx 19\ \% $$

(iii) Volume filtered per day:

$$ V = 125\ \text{ml min}^{-1} \times 60 \times 24 = 180\,000\ \text{ml} = 180\ \text{L} $$

About one-fifth of the plasma entering the glomerulus is filtered; the other
four-fifths carries the plasma proteins on into the efferent arteriole. Of the
180 L filtered, roughly 178.5 L is reabsorbed and about **1.5 L** is voided.
:::

### Control of kidney function, and disorders

- **ADH (vasopressin)** from the posterior pituitary makes the DCT and
  collecting duct permeable to water. Dehydration → more ADH → less, more
  concentrated urine. No ADH → **diabetes insipidus**, up to 20 L of dilute
  urine a day.
- **Renin–angiotensin–aldosterone system.** A fall in blood pressure is sensed
  by the **juxtaglomerular apparatus** (JGA), where the afferent arteriole
  touches the DCT. It releases **renin** → angiotensin II → vasoconstriction and
  release of **aldosterone** from the adrenal cortex → Na⁺ and water reabsorption
  in the DCT → blood pressure restored.
- **ANF (atrial natriuretic factor)** from a stretched atrial wall does the
  opposite: it causes vasodilation and salt loss, lowering blood pressure.

**Micturition.** Urine trickles down the ureters by peristalsis and is stored in
the urinary bladder. Stretch receptors fire when about 300–400 ml has collected;
the reflex centre in the sacral spinal cord relaxes the internal sphincter while
the detrusor muscle contracts. The external sphincter is under voluntary control,
which is why micturition can be delayed.

Normal urine is pale yellow (from **urochrome**), slightly acidic (pH ≈ 6),
95 % water, with about 2 % urea, 0.05 % uric acid and 0.075 % creatinine, plus
salts. Glucose, protein, blood cells or ketone bodies in urine are always
abnormal.

| Disorder | Cause | Sign |
|---|---|---|
| Uraemia | kidney failure; urea retained in blood | blood urea ≫ 40 mg/dl |
| Renal calculi (stones) | crystals of calcium oxalate/uric acid in the pelvis | severe loin pain, blood in urine |
| Glomerulonephritis | inflammation of the glomeruli after infection | protein and blood in urine |
| Diabetes mellitus | insulin deficiency | glucose in urine (glycosuria) |
| Diabetes insipidus | lack of ADH | huge volume of dilute urine |

Kidney failure is treated by **haemodialysis** — blood is pumped past a
semi-permeable cellophane membrane bathed in dialysing fluid that has the same
composition as normal plasma *except* that it contains **no urea**, so urea
diffuses out down its concentration gradient while glucose and salts stay in.
The permanent cure is **renal transplantation**, for which tissue matching is
essential.

::: caution Filtration is not the same as reabsorption
A common exam error is to say "the kidney filters 1.5 L a day". The kidney
*filters* 180 L a day and *reabsorbs* 178.5 L of it. Also, glucose is normally
100 % reabsorbed in the PCT; it appears in urine only when the plasma glucose
exceeds the **renal threshold of about 180 mg/dl** and the carriers saturate.
:::

## 8.5 Nervous system

The nervous system is the body's *fast* control system: it works in milliseconds,
by electrical impulses along fixed wires, and its effects stop as soon as the
impulse stops. It is divided into the **central nervous system (CNS)** — brain
and spinal cord — and the **peripheral nervous system (PNS)** — **12 pairs of
cranial nerves** and **31 pairs of spinal nerves**. The PNS in turn has a
**somatic** (voluntary, skeletal muscle) division and an **autonomic**
(involuntary) division, which is itself split into the **sympathetic**
("fight or flight", thoraco-lumbar, noradrenaline) and the **parasympathetic**
("rest and digest", cranio-sacral, acetylcholine) systems.

### The neuron

```figure caption="A myelinated motor neuron. The impulse always travels dendrite → cell body → axon → synaptic knob."
from matplotlib.patches import Circle, Ellipse, Polygon

fig, ax = plt.subplots(figsize=(5.2, 2.9))
MEM = "#8a6a3a"; CYT = "#fdf0d8"; MYE = "#cfe0f2"; MYE_E = "#4a67b8"
NUC = "#e4c37a"

SX, SY = -4.55, 0.0
th = np.linspace(0, 2*np.pi, 200)
rr = 0.80 + 0.07*np.sin(5*th)
ax.fill(SX + rr*np.cos(th), SY + rr*np.sin(th)*1.02, fc=CYT, ec=MEM,
        lw=1.2, zorder=4)
ax.add_patch(Circle((SX - 0.10, SY + 0.05), 0.30, fc=NUC, ec=MEM, lw=0.9,
                    zorder=5))
ax.add_patch(Circle((SX - 0.10, SY + 0.05), 0.10, fc=MEM, ec='none', zorder=6))
for k in range(9):
    ax.add_patch(Circle((SX + 0.30*np.cos(k), SY + 0.42*np.sin(k*2.1)), 0.055,
                        fc="#c08a4a", ec='none', zorder=5))

DEN = [(140, 1.9), (168, 2.1), (196, 1.9), (110, 1.5), (226, 1.5)]
for a_deg, L in DEN:
    a = np.radians(a_deg)
    x0, y0 = SX + 0.72*np.cos(a), SY + 0.72*np.sin(a)
    x1, y1 = SX + L*np.cos(a), SY + L*np.sin(a)
    ax.plot([x0, x1], [y0, y1], color=MEM, lw=2.4, solid_capstyle='round',
            zorder=3)
    for s in (-1, 1):
        b = a + s*0.42
        ax.plot([x1, x1 + 0.52*np.cos(b)], [y1, y1 + 0.52*np.sin(b)],
                color=MEM, lw=1.4, solid_capstyle='round', zorder=3)

ax.plot([-3.78, 4.20], [0, 0], color=MEM, lw=4.6, solid_capstyle='round',
        zorder=3)
ax.plot([-3.78, 4.20], [0, 0], color=CYT, lw=2.0, solid_capstyle='round',
        zorder=3.1)
for cx in (-2.55, -1.05, 0.45, 1.95, 3.45):
    ax.add_patch(Ellipse((cx, 0), 1.20, 0.74, fc=MYE, ec=MYE_E, lw=1.0,
                         zorder=4))
    ax.add_patch(Circle((cx + 0.30, 0.22), 0.075, fc=MYE_E, ec='none', zorder=5))

for s, dy in ((1, 0.9), (0, 0.0), (-1, -0.9)):
    ax.plot([4.20, 4.85, 5.35], [0, dy*0.6, dy], color=MEM, lw=1.8,
            solid_capstyle='round', zorder=3)
    ax.add_patch(Circle((5.45, dy), 0.16, fc="#d9a05b", ec=MEM, lw=0.9,
                        zorder=5))

ax.annotate('', xy=(2.10, -1.55), xytext=(-2.60, -1.55), zorder=6,
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.2,
                            mutation_scale=10))
ax.text(-0.25, -1.85, "direction of nerve impulse", fontsize=6.2, color=ACCENT,
        ha='center')

def lab(txt, tip, tx, ty, ha='left', fs=6.1):
    ax.annotate(txt, xy=tip, xytext=(tx, ty), fontsize=fs, color=INK, ha=ha,
                va='center', zorder=20,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.65,
                                shrinkA=2.0, shrinkB=1.0))

lab("dendrites", (-6.05, 0.95), -6.40, 2.30, ha='left')
lab("cell body (cyton)", (-4.35, -0.72), -5.90, -1.95, ha='left')
lab("nucleus", (-4.65, 0.05), -4.30, 2.35, ha='center')
lab("Nissl granules", (-4.25, 0.40), -2.90, 2.75, ha='center')
lab("axon hillock", (-3.70, -0.20), -2.85, -1.10, ha='center')
lab("myelin sheath", (-1.05, 0.36), -0.60, 2.35, ha='center')
lab("node of Ranvier", (0.45 + 0.75, 0.0), 1.90, -1.05, ha='center')
lab("Schwann cell\nnucleus", (2.25, 0.22), 2.60, 2.45, ha='center')
lab("axon", (3.45, -0.36), 4.30, -1.85, ha='center')
lab("synaptic knobs", (5.52, 0.95), 5.05, 2.35, ha='center')
ax.set_xlim(-6.90, 6.90); ax.set_ylim(-3.20, 3.20)
ax.set_aspect('equal'); ax.axis('off')
```

A **neuron** never divides after birth. Its **cell body (cyton)** contains the
nucleus and dark-staining **Nissl granules** (rough ER) that make the
neurotransmitter; **dendrites** carry impulses *towards* the cell body; the
single **axon** carries them *away*. In myelinated neurons, **Schwann cells**
wrap the axon in an insulating fatty **myelin sheath**, broken every ~1 mm at a
**node of Ranvier**. Depending on their job, neurons are **sensory (afferent)**,
**motor (efferent)** or **interneurons (relay)**.

### The nerve impulse

```figure caption="An action potential recorded from a single axon. Resting potential $-70$ mV, threshold $-55$ mV, peak about $+35$ mV."
fig, ax = plt.subplots(figsize=(5.2, 3.3))

def pw(t, pts):
    tk = np.array([p[0] for p in pts]); vk = np.array([p[1] for p in pts])
    out = np.interp(t, tk, vk)
    for i in range(len(tk)-1):
        m = (t >= tk[i]) & (t <= tk[i+1])
        u = (t[m]-tk[i])/(tk[i+1]-tk[i])
        out[m] = vk[i] + (vk[i+1]-vk[i])*(0.5-0.5*np.cos(np.pi*u))
    return out

t = np.linspace(-0.5, 6.0, 2000)
V = pw(t, [(-0.5, -70), (0.45, -70), (0.80, -55), (1.10, -25), (1.40, 12),
           (1.68, 35), (2.05, 8), (2.45, -32), (2.95, -74), (3.45, -80),
           (4.60, -74), (6.00, -70)])
ax.plot(t, V, color=ACCENT, lw=1.9, zorder=5)
for y, ls in ((-70, ':'), (-55, ':'), (0, '-')):
    ax.axhline(y, color=MUTED if y else GRID, lw=0.8, ls=ls, zorder=1)

ax.text(-0.42, -64, "resting potential  −70 mV", fontsize=6.1, color=MUTED,
        ha='left')
ax.text(-0.42, -49, "threshold  −55 mV", fontsize=6.1, color=MUTED, ha='left')
ax.text(1.62, 44, "+35 mV", fontsize=6.2, color=INK, ha='center')

ax.annotate('', xy=(0.55, -71), xytext=(0.55, -92), zorder=6,
            arrowprops=dict(arrowstyle='-|>', color=SERIES[2], lw=1.1,
                            mutation_scale=8))
ax.text(0.55, -96, "stimulus", fontsize=6.1, color=SERIES[2], ha='center',
        va='top')

def note(txt, tip, tx, ty, ha='left'):
    ax.annotate(txt, xy=tip, xytext=(tx, ty), fontsize=6.1, color=INK, ha=ha,
                va='center', zorder=20,
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.7,
                                mutation_scale=7, shrinkA=2.0, shrinkB=1.5))

note("depolarisation\nNa⁺ gates open, Na⁺ rushes in", (1.22, -8), -0.42, 22)
note("repolarisation\nK⁺ gates open, K⁺ leaves", (2.28, -18), 3.05, 26)
note("hyperpolarisation\n(K⁺ gates close slowly)", (3.50, -80), 4.35, -40)
note("Na⁺/K⁺ pump (3 Na⁺ out : 2 K⁺ in)\nre-establishes the resting state",
     (5.30, -71), 5.95, -95, ha='right')

ax.plot([1.00, 2.60], [-112, -112], color=SERIES[1], lw=2.6,
        solid_capstyle='butt', zorder=4)
ax.plot([2.60, 4.60], [-112, -112], color=SERIES[3], lw=2.6,
        solid_capstyle='butt', zorder=4)
ax.text(1.80, -119, "absolute refractory ≈1 ms", fontsize=5.8,
        color=SERIES[1], ha='center', va='top')
ax.text(3.60, -119, "relative refractory", fontsize=5.8, color=SERIES[3],
        ha='center', va='top')

ax.set_xlim(-0.5, 6.0); ax.set_ylim(-132, 60)
ax.set_xlabel("time (ms)"); ax.set_ylabel("membrane potential (mV)")
ax.set_yticks([-70, -55, 0, 35])
ax.spines[['top', 'right']].set_visible(False)
ax.spines['bottom'].set_position(('data', -132))
ax.grid(False)
```

At rest the axon membrane is **polarised**: the Na⁺/K⁺ pump throws out 3 Na⁺ for
every 2 K⁺ it takes in, and the membrane leaks K⁺ freely but Na⁺ hardly at all,
so the inside is about **−70 mV** with respect to the outside. A stimulus that
depolarises a patch to the **threshold of −55 mV** throws open the voltage-gated
Na⁺ channels; Na⁺ floods in and the potential shoots to about **+35 mV**
(**depolarisation**). The Na⁺ gates then shut and K⁺ gates open, so K⁺ leaves
and the inside becomes negative again (**repolarisation**), briefly overshooting
to about −80 mV (**hyperpolarisation**). During the **absolute refractory
period** of roughly 1 ms no second impulse is possible at all — this is what
fixes the maximum firing frequency and makes the impulse travel one way only.

::: key All-or-none law
A stimulus below threshold produces no impulse; any stimulus at or above
threshold produces an action potential of **exactly the same size**. A stronger
stimulus does not give a bigger impulse — it gives **more impulses per second**
and recruits more neurons. That is how the brain codes intensity.
:::

In an unmyelinated axon the impulse creeps along at **0.5–2 m s⁻¹**. In a
myelinated axon current can only enter at the nodes of Ranvier, so the impulse
leaps from node to node — **saltatory conduction** — reaching **100–120 m s⁻¹**
in the thickest human fibres, and using far less ATP.

At a **synapse** the impulse cannot jump the 20 nm cleft electrically. Ca²⁺
entering the knob makes vesicles fuse with the pre-synaptic membrane and release
a **neurotransmitter** (acetylcholine at the neuromuscular junction, also
noradrenaline, dopamine, GABA, serotonin). It diffuses across, binds receptors
on the post-synaptic membrane and starts a new impulse; the enzyme
**cholinesterase** then destroys it so the synapse resets. Because vesicles are
only on one side, a synapse conducts in **one direction only**.

::: example Worked example 8.5 — nerve conduction velocity
**Problem.** A nerve is stimulated at the elbow and again at the wrist of a
patient in Bharatpur. The muscle responds 4.0 ms after the wrist stimulus and
9.5 ms after the elbow stimulus. The two stimulating points are 33 cm apart.
Find the conduction velocity of the nerve, and say whether the fibre is
myelinated.

**Solution.** The delay at the neuromuscular junction is the same for both
stimuli, so subtracting removes it:

$$ \Delta t = 9.5 - 4.0 = 5.5\ \text{ms} = 5.5 \times 10^{-3}\ \text{s} $$

$$ s = 33\ \text{cm} = 0.33\ \text{m} $$

$$ v = \frac{s}{\Delta t} = \frac{0.33}{5.5 \times 10^{-3}} = 60\ \text{m s}^{-1} $$

60 m s⁻¹ is far above the 0.5–2 m s⁻¹ of unmyelinated fibres, so this is a
**myelinated** fibre conducting saltatorily. (Values below about 40 m s⁻¹ in a
motor nerve suggest demyelination.)
:::

### The brain

```figure caption="The human brain in longitudinal (sagittal) section. Anterior is to the left."
from matplotlib.patches import Ellipse, Circle, Polygon, FancyBboxPatch

fig, ax = plt.subplots(figsize=(5.2, 3.4))
CB = "#f2ddd8"; CBE = "#a8625a"; IN = "#e8c9a4"; INE = "#9c7440"
CER = "#e6cfe4"; CERE = "#8a5f86"; STEM = "#f6e3c4"

th = np.linspace(0, 2*np.pi, 600)
rr = 1 + 0.030*np.sin(13*th)
ax.fill(-0.80 + 4.25*rr*np.cos(th), 1.20 + 2.45*rr*np.sin(th),
        fc=CB, ec=CBE, lw=1.2, zorder=2)
for k in range(7):
    a0 = 0.28 + k*0.82
    aa = np.linspace(a0, a0 + 0.30, 30)
    ax.plot(-0.80 + 4.25*0.90*np.cos(aa), 1.20 + 2.45*0.90*np.sin(aa),
            color=CBE, lw=0.6, alpha=0.7, zorder=3)

cc = np.linspace(0, 1, 120)
ccx = -2.70 + 4.60*cc
ccy = 0.52 + 1.15*np.sin(np.pi*cc)
ax.plot(ccx, ccy, color=INE, lw=7.5, solid_capstyle='round', zorder=4)
ax.plot(ccx, ccy, color="#fbf1d8", lw=5.5, solid_capstyle='round', zorder=4.1)

ax.add_patch(Ellipse((-0.15, -0.05), 1.75, 1.00, angle=-8, fc=IN, ec=INE,
                     lw=1.0, zorder=5))
ax.add_patch(Ellipse((-1.15, -0.85), 1.10, 0.58, angle=-16, fc="#dcb894",
                     ec=INE, lw=1.0, zorder=5))
ax.plot([-1.45, -1.62], [-1.08, -1.52], color=INE, lw=1.6, zorder=5)
ax.add_patch(Ellipse((-1.72, -1.78), 0.66, 0.52, fc="#e9d09a", ec=INE,
                     lw=1.0, zorder=5))
ax.add_patch(Circle((1.02, 0.28), 0.17, fc="#c9a24a", ec=INE, lw=0.8, zorder=6))

STEMPTS = [(0.62, 0.02), (1.28, -0.62), (1.55, -1.30), (1.70, -2.10),
           (1.92, -3.10), (2.05, -4.05)]
xs, ys = np.array(STEMPTS).T
ax.plot(xs, ys, color=INE, lw=11.0, solid_capstyle='round', zorder=4)
ax.plot(xs, ys, color=STEM, lw=9.0, solid_capstyle='round', zorder=4.1)
ax.add_patch(Ellipse((1.62, -1.62), 1.55, 1.05, angle=-20, fc="#f0d6a8",
                     ec=INE, lw=1.0, zorder=5))

ax.add_patch(Ellipse((3.85, -1.45), 3.10, 2.15, angle=-12, fc=CER, ec=CERE,
                     lw=1.1, zorder=3))
for k in range(8):
    a = -0.25 + k*0.42
    ax.plot([3.85 + 0.35*np.cos(a), 3.85 + 1.48*np.cos(a)],
            [-1.45 + 0.28*np.sin(a), -1.45 + 1.02*np.sin(a)],
            color=CERE, lw=0.6, alpha=0.8, zorder=4)

def lab(txt, tip, tx, ty, ha='left', fs=6.1):
    ax.annotate(txt, xy=tip, xytext=(tx, ty), fontsize=fs, color=INK, ha=ha,
                va='center', zorder=20,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.65,
                                shrinkA=2.0, shrinkB=1.0))

lab("cerebrum\n(cerebral cortex,\ngyri and sulci)", (-3.30, 2.70), -7.20, 3.05)
lab("corpus callosum", (-1.40, 1.44), -7.20, 1.25)
lab("thalamus", (-0.55, 0.05), -7.20, 0.05)
lab("hypothalamus", (-1.30, -0.92), -7.20, -1.05)
lab("pituitary gland", (-1.95, -1.90), -7.20, -2.30)
lab("pineal body", (1.06, 0.42), -1.62, -3.62, ha='center')
lab("mid-brain", (1.18, -0.72), 0.15, -3.35, ha='center')
lab("pons Varolii", (1.72, -1.72), 2.55, -3.35, ha='center')
lab("medulla oblongata", (1.95, -3.05), 5.55, -2.95, ha='left')
lab("spinal cord", (2.05, -3.95), 5.55, -3.95, ha='left')
lab("cerebellum", (4.45, -1.05), 5.55, -0.35, ha='left')
ax.text(-6.10, 3.95, "ANTERIOR", fontsize=6.0, color=MUTED, ha='center')
ax.text(5.90, 3.95, "POSTERIOR", fontsize=6.0, color=MUTED, ha='center')
ax.set_xlim(-7.40, 7.40); ax.set_ylim(-4.55, 4.35)
ax.set_aspect('equal'); ax.axis('off')
```

The brain weighs about 1.35 kg, floats in **cerebrospinal fluid** and is wrapped
in three **meninges** (dura, arachnoid, pia mater). Its parts:

| Part | Position | Main functions |
|---|---|---|
| **Cerebrum** (2 hemispheres) | forebrain, largest part | intelligence, memory, speech, will, all voluntary action; sensory perception |
| **Corpus callosum** | between the hemispheres | band of nerve fibres joining left and right |
| **Thalamus** | forebrain floor | relay station for all sensory impulses except smell |
| **Hypothalamus** | below the thalamus | temperature, hunger, thirst, sleep, emotion; controls the pituitary |
| **Mid-brain** | brainstem | reflex centres for sight and hearing (pupil, head-turning) |
| **Cerebellum** | hindbrain, behind | balance, posture, coordination of muscle action |
| **Pons Varolii** | hindbrain | bridge between the two halves of the cerebellum; helps control breathing |
| **Medulla oblongata** | lowest, joins spinal cord | **involuntary vital centres**: heartbeat, breathing, blood pressure, swallowing, vomiting |

The **spinal cord** runs from the medulla to the first lumbar vertebra inside the
vertebral column. In section, its **grey matter** (cell bodies) is central and
butterfly-shaped, while the **white matter** (myelinated tracts) is outside —
the opposite arrangement to the brain.

### The reflex arc

```figure caption="A spinal reflex arc (withdrawal of the hand). The impulse reaches the effector without waiting for the brain."
from matplotlib.patches import Ellipse, Circle, Polygon

fig, ax = plt.subplots(figsize=(5.2, 3.2))
CORD = "#f4f1ea"; GREY = "#cfc4b4"; EDG = "#7e7264"
SN = "#1d6fb8"; MN = "#c0392b"; RN = "#2e8b57"

CX, CY, S = -3.30, 0.0, 1.35
ax.add_patch(Ellipse((CX, CY), 3.55, 4.45, fc=CORD, ec=EDG, lw=1.2, zorder=2))
BF = [(-0.30, 1.50), (-0.55, 0.70), (-0.95, 0.10), (-1.20, -0.75),
      (-0.75, -1.18), (-0.35, -0.55), (-0.15, -0.10), (0.15, -0.10),
      (0.35, -0.55), (0.75, -1.18), (1.20, -0.75), (0.95, 0.10),
      (0.55, 0.70), (0.30, 1.50), (0.12, 1.45), (0.12, 0.22),
      (-0.12, 0.22), (-0.12, 1.45)]
ax.add_patch(Polygon([(CX + x*S, CY + y*S) for x, y in BF], closed=True,
                     fc=GREY, ec=EDG, lw=1.0, zorder=3))
ax.add_patch(Circle((CX, CY + 0.22), 0.09, fc='white', ec=EDG, lw=0.7, zorder=4))

ax.plot([4.10, 6.10], [2.35, 2.35], color="#c79a72", lw=3.2, zorder=3,
        solid_capstyle='round')
ax.plot([4.10, 6.10], [2.62, 2.62], color="#e7cdb4", lw=3.2, zorder=3,
        solid_capstyle='round')
for k in range(5):
    ax.plot([4.45 + 0.35*k, 4.30 + 0.35*k], [2.72, 3.10], color="#b8860b",
            lw=0.8, zorder=4)
ax.text(5.10, 3.30, "heat / pin", fontsize=6.1, color="#b8860b", ha='center')

ax.add_patch(Ellipse((4.30, -2.15), 2.90, 1.05, angle=-8, fc="#f0c9c2",
                     ec="#a8625a", lw=1.1, zorder=3))
for k in range(5):
    ax.plot([3.20 + 0.55*k, 3.35 + 0.55*k], [-2.55, -1.72], color="#a8625a",
            lw=0.6, alpha=0.8, zorder=4)

SENS = [(4.05, 2.28), (2.10, 2.05), (0.60, 1.95)]
ax.plot(*np.array(SENS).T, color=SN, lw=1.8, zorder=5, solid_capstyle='round')
ax.add_patch(Circle((0.35, 1.92), 0.30, fc="#cfe0f2", ec=SN, lw=1.1, zorder=6))
ax.plot([0.10, -1.10, -2.10, -3.32], [1.88, 1.72, 1.42, 1.14], color=SN,
        lw=1.8, zorder=5, solid_capstyle='round')
ax.add_patch(Circle((CX - 0.22, CY + 1.05), 0.22, fc="#d9f0e0", ec=RN, lw=1.0,
                    zorder=6))
ax.plot([CX - 0.30, CX - 0.55, CX - 0.62], [0.86, 0.20, -0.62], color=RN,
        lw=1.6, zorder=5, solid_capstyle='round')
ax.add_patch(Circle((CX - 0.62, CY - 0.88), 0.26, fc="#f6cdc5", ec=MN, lw=1.1,
                    zorder=6))
ax.plot([CX - 0.40, -2.30, -0.60, 1.40, 3.05], [-1.02, -1.35, -1.75, -2.05, -2.18],
        color=MN, lw=1.8, zorder=5, solid_capstyle='round')

def arr(p0, p1, c):
    ax.annotate('', xy=p1, xytext=p0, zorder=8,
                arrowprops=dict(arrowstyle='-|>', color=c, lw=1.4,
                                mutation_scale=9))
arr((3.10, 2.24), (2.60, 2.18), SN)
arr((-1.05, 1.71), (-1.55, 1.56), SN)
arr((CX - 0.52, 0.05), (CX - 0.58, -0.35), RN)
arr((-1.00, -1.68), (-0.45, -1.78), MN)
ax.annotate('', xy=(CX, 2.72), xytext=(CX, 2.05), zorder=8,
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.1,
                            mutation_scale=8))
ax.text(CX, 2.84, "ascending tract\n→ brain (pain is\nfelt a moment later)",
        fontsize=5.9, color=MUTED, ha='center', va='bottom')

def lab(txt, tip, tx, ty, ha='left', fs=6.0, c=INK):
    ax.annotate(txt, xy=tip, xytext=(tx, ty), fontsize=fs, color=c, ha=ha,
                va='center', zorder=20,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.65,
                                shrinkA=2.0, shrinkB=1.0))

lab("receptor in skin", (4.35, 2.30), 6.75, 1.70, ha='right')
lab("sensory (afferent)\nneuron", (2.40, 2.12), 2.05, 0.95, ha='center', c=SN)
lab("dorsal root ganglion", (0.30, 2.22), -0.40, 3.25, ha='center')
lab("white matter", (CX - 1.55, 0.55), -7.05, 1.95, ha='left')
lab("grey matter", (CX - 1.05, -0.75), -7.05, 0.90, ha='left')
lab("central canal", (CX, 0.30), -7.05, -0.15, ha='left')
lab("relay neuron", (CX - 0.44, 1.05), -7.05, -1.20, ha='left', c=RN)
lab("motor (efferent)\nneuron", (CX - 0.62, -0.88), -7.05, -2.55, ha='left', c=MN)
lab("effector — flexor muscle\ncontracts, hand withdraws", (4.00, -2.60),
    2.55, -3.35, ha='center')
ax.set_xlim(-7.15, 6.85); ax.set_ylim(-3.80, 4.00)
ax.set_aspect('equal'); ax.axis('off')
```

A **reflex action** is a rapid, automatic, involuntary response to a stimulus.
The path the impulse takes is the **reflex arc**, and it has five parts:

**receptor → sensory neuron → CNS (relay neuron) → motor neuron → effector**

Touching a hot *tawa* takes the impulse from the skin receptor along the sensory
neuron (whose cell body sits in the **dorsal root ganglion**) into the dorsal
horn of the spinal cord, across a relay neuron, out along the motor neuron
through the ventral root, to the flexor muscle — all in about 20 ms. A branch
also runs up the ascending tract to the brain, which is why you *feel* the pain
only after your hand has already moved. **Inborn (unconditioned)** reflexes such
as blinking, sneezing and the knee jerk are present from birth;
**conditioned reflexes**, like Pavlov's dogs salivating at a bell, are learnt and
need the cerebral cortex.

::: caution A reflex is not "brainless", but it is "brain-free"
The brain is informed, but it is not consulted. Marks are lost for writing that
the impulse "goes to the brain and comes back" — in a **spinal reflex** the
decision is taken in the spinal cord. Note too that the **knee jerk** is
*monosynaptic*: there is no relay neuron, the sensory neuron synapses directly
with the motor neuron.
:::

## 8.6 Sense organs

The five sense organs are the **eye** (photoreceptor), **ear** (phono- and
statoreceptor), **nose** (olfactoreceptor), **tongue** (gustatoreceptor) and
**skin** (thermo-, tango- and algesireceptor).

### The eye

```figure caption="Horizontal section of the human eye. Light passes cornea → aqueous humour → pupil → lens → vitreous humour → retina, where it forms a real, inverted, diminished image."
from matplotlib.patches import Circle, Wedge, Ellipse, Polygon, PathPatch
from matplotlib.path import Path

fig, ax = plt.subplots(figsize=(5.2, 3.4))
SCLE = "#7c766a"; CHO = "#a8504a"; RET = "#e0b075"
AQ = "#e6f2fb"; VIT = "#f0f7fc"; LENS = "#cfe4f5"

R = 2.60
ax.add_patch(Circle((0, 0), R, fc=VIT, ec=SCLE, lw=1.5, zorder=2))
ax.add_patch(Wedge((0, 0), R - 0.03, -66, 66, width=0.17, fc=CHO, ec='none',
                   zorder=3))
ax.add_patch(Wedge((0, 0), R - 0.20, -66, 66, width=0.17, fc=RET, ec='none',
                   zorder=3))

CO = [(-1.90, 1.77),
      (-2.52, 1.42), (-2.98, 0.78), (-2.98, 0.00),
      (-2.98, -0.78), (-2.52, -1.42), (-1.90, -1.77)]
ax.add_patch(PathPatch(Path(CO, [Path.MOVETO] + [Path.CURVE4]*6), fc=AQ,
                       ec="#4a8fc0", lw=1.8, zorder=5))

ax.add_patch(Ellipse((-0.72, 0), 0.98, 2.50, fc=LENS, ec="#4a67b8", lw=1.3,
                     zorder=6))
for s_ in (1, -1):
    ax.add_patch(Polygon([(-1.86, s_*1.74), (-1.28, s_*1.44), (-1.74, s_*1.16)],
                         closed=True, fc="#d4b06a", ec="#8a6a3a", lw=0.8,
                         zorder=7))
    ax.add_patch(Polygon([(-1.36, s_*1.38), (-1.52, s_*1.40), (-1.52, s_*0.50),
                          (-1.36, s_*0.48)], closed=True, fc="#6f7fa8",
                         ec="#3d4a6b", lw=0.8, zorder=7))
    for k in range(3):
        ax.plot([-1.26, -0.78], [s_*(1.40 - 0.07*k), s_*(1.26 - 0.10*k)],
                color="#8a6a3a", lw=0.7, zorder=7)

for y in (-1.05, -0.52, 0.0, 0.52, 1.05):
    ax.plot([-5.30, -3.05], [y, y*0.88], color="#f2c14e", lw=0.9, zorder=1)
ax.annotate('', xy=(-2.05, 0), xytext=(-5.30, 0), zorder=8,
            arrowprops=dict(arrowstyle='-|>', color="#d4a017", lw=1.5,
                            mutation_scale=10))
ax.text(-4.20, 0.30, "light", fontsize=6.2, color="#a8770c", ha='center')

ax.add_patch(Ellipse((2.24, -0.78), 0.26, 0.46, angle=-16, fc="#f6eecf",
                     ec="#8a6a3a", lw=0.9, zorder=7))
ax.plot([2.42, 4.05], [-0.88, -1.62], color="#c9b98d", lw=7.0, zorder=4.8,
        solid_capstyle='round')
ax.plot([2.42, 4.05], [-0.88, -1.62], color="#f2e6c8", lw=5.0, zorder=4.9,
        solid_capstyle='round')
ax.add_patch(Circle((2.32, 0.42), 0.15, fc="#8a3a3a", ec='none', zorder=7))

def lab(txt, tip, tx, ty, ha='left', fs=6.0):
    ax.annotate(txt, xy=tip, xytext=(tx, ty), fontsize=fs, color=INK, ha=ha,
                va='center', zorder=20,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.65,
                                shrinkA=2.0, shrinkB=1.0))

lab("cornea", (-2.86, 0.92), -4.30, 2.55, ha='center')
lab("aqueous humour", (-2.10, -0.95), -4.05, -2.55, ha='center')
lab("pupil", (-1.46, 0.00), -1.55, 3.55, ha='center')
lab("iris", (-1.44, -0.95), -1.35, -3.45, ha='center')
lab("ciliary body", (-1.62, 1.48), 0.55, 3.55, ha='center')
lab("suspensory\nligament", (-1.02, 1.32), 2.75, 3.25, ha='center')
lab("lens", (-0.72, -0.30), 0.55, -3.45, ha='center')
lab("vitreous humour", (1.05, 0.95), 2.75, -3.45, ha='center')
lab("sclera", (2.32, 1.18), 4.70, 2.85, ha='left')
lab("choroid", (2.20, 1.42), 4.70, 2.05, ha='left')
lab("retina", (2.00, 1.68), 4.70, 1.25, ha='left')
lab("yellow spot\n(fovea centralis)", (2.32, 0.42), 4.70, 0.25, ha='left')
lab("blind spot\n(optic disc)", (2.30, -0.78), 4.95, -1.35, ha='left')
lab("optic nerve", (3.70, -1.46), 4.95, -2.85, ha='left')
ax.set_xlim(-6.30, 7.10); ax.set_ylim(-4.15, 4.15)
ax.set_aspect('equal'); ax.axis('off')
```


The eyeball has three coats — the tough **sclera** outside (transparent in
front as the **cornea**), the pigmented, blood-rich **choroid**, and the
light-sensitive **retina**. The retina carries about **120 million rods**
(pigment **rhodopsin**; dim light, black-and-white vision) and about **6–7
million cones** (pigment **iodopsin**; bright light, colour). Cones are packed
most densely at the **yellow spot (fovea centralis)**, which gives the sharpest
image; where the optic nerve leaves there are no receptors at all, giving the
**blind spot**. The lens is held by suspensory ligaments from the **ciliary
body**; when the ciliary muscle contracts the ligaments slacken and the elastic
lens becomes more convex, focusing near objects — this is **accommodation**.
Vitamin A deficiency destroys rhodopsin and causes **night blindness**, a real
public-health problem in the Terai.

Common defects of the eye follow from the geometry. In **myopia (short sight)**
the eyeball is too long, so the image of a distant object falls *in front of* the
retina; a **concave (diverging) lens** corrects it. In **hypermetropia (long
sight)** the eyeball is too short and the image would fall *behind* the retina; a
**convex (converging) lens** corrects it. **Presbyopia** is the stiffening of the
lens with age, **astigmatism** is an unevenly curved cornea, and a **cataract**
is a lens that has gone opaque — treated by replacing it with an artificial one.

### The ear

```figure caption="The human ear: outer, middle and inner divisions. The cochlea hears; the semicircular canals and vestibule give balance."
from matplotlib.patches import Ellipse, Circle, Polygon, PathPatch
from matplotlib.path import Path

fig, ax = plt.subplots(figsize=(5.2, 3.4))
BN = "#ece3d4"; BNE = "#a79878"; TUB = "#8a6a3a"; LUM = "#fdf6e6"
OSS = "#e0c88a"; OSE = "#8a6a3a"; NRV = "#c9a24a"

PIN = [(-4.45, 1.85),
       (-5.45, 2.05), (-6.35, 1.35), (-6.30, 0.30),
       (-6.25, -0.70), (-5.55, -1.55), (-4.85, -1.60),
       (-4.35, -1.64), (-4.20, -0.55), (-4.45, 1.85)]
ax.add_patch(PathPatch(Path(PIN, [Path.MOVETO] + [Path.CURVE4]*9),
                       fc="#f6ded6", ec="#a8625a", lw=1.2, zorder=3))
ax.add_patch(PathPatch(Path([(-4.75, 1.15), (-5.35, 1.15), (-5.65, 0.35),
                             (-5.15, -0.45)],
                            [Path.MOVETO] + [Path.CURVE4]*3),
                       fc='none', ec="#a8625a", lw=0.8, zorder=4))

def tube(pts, w=7.0, c=TUB, l=LUM, z=4):
    x, y = np.array(pts).T
    ax.plot(x, y, color=c, lw=w, solid_capstyle='round', zorder=z)
    ax.plot(x, y, color=l, lw=w*0.55, solid_capstyle='round', zorder=z+0.1)

tube([(-4.55, 0.35), (-3.20, 0.25), (-1.95, 0.10)], w=13.0)
ax.plot([-1.85, -1.55], [0.95, -0.85], color="#4a8fc0", lw=2.2, zorder=6,
        solid_capstyle='round')

ax.add_patch(Polygon([(-1.72, 0.42), (-1.10, 1.05), (-0.92, 0.82),
                      (-1.62, 0.20)], closed=True, fc=OSS, ec=OSE, lw=0.9,
                     zorder=6))
ax.add_patch(Polygon([(-1.05, 1.02), (-0.30, 0.96), (-0.28, 0.68),
                      (-0.95, 0.76)], closed=True, fc=OSS, ec=OSE, lw=0.9,
                     zorder=6))
ax.add_patch(Polygon([(-0.32, 0.92), (0.38, 0.62), (0.38, 0.28),
                      (-0.30, 0.66)], closed=True, fc=OSS, ec=OSE, lw=0.9,
                     zorder=6))
ax.plot([0.42, 0.42], [0.66, 0.24], color="#4a8fc0", lw=2.0, zorder=6)
ax.plot([0.42, 0.42], [-0.35, -0.72], color="#4a8fc0", lw=2.0, zorder=6)

ax.add_patch(Ellipse((1.05, 0.30), 1.05, 1.25, angle=-14, fc="#dce8f5",
                     ec="#4a67b8", lw=1.1, zorder=5))
for cx, cy, w, h, an in ((2.05, 2.05, 1.85, 1.15, 8), (1.55, 1.75, 1.15, 1.95, 28),
                         (2.85, 1.65, 1.25, 1.85, -32)):
    ax.add_patch(Ellipse((cx, cy), w, h, angle=an, fill=False, ec="#4a67b8",
                         lw=2.4, zorder=4))
ax.add_patch(Circle((1.32, 1.02), 0.17, fc="#dce8f5", ec="#4a67b8", lw=0.9,
                    zorder=6))

th = np.linspace(0, 2.7*2*np.pi, 700)
rr = 1.18*(1 - th/(3.05*2*np.pi))
cxc, cyc = 3.05, -1.35
ax.plot(cxc + rr*np.cos(th + np.pi), cyc + rr*np.sin(th + np.pi),
        color=TUB, lw=5.0, solid_capstyle='round', zorder=4)
ax.plot(cxc + rr*np.cos(th + np.pi), cyc + rr*np.sin(th + np.pi),
        color="#f6e6c0", lw=2.6, solid_capstyle='round', zorder=4.1)
ax.plot([1.30, 1.87], [-0.25, -1.30], color=TUB, lw=5.0, zorder=4,
        solid_capstyle='round')
ax.plot([1.30, 1.87], [-0.25, -1.30], color="#f6e6c0", lw=2.6, zorder=4.1,
        solid_capstyle='round')

ax.plot([2.60, 3.80, 4.95], [-2.42, -2.92, -3.05], color=NRV, lw=3.2, zorder=3,
        solid_capstyle='round')
tube([(0.95, -0.55), (0.10, -1.65), (-0.95, -2.75), (-1.85, -3.10)], w=7.0)

for x in (-1.98, 0.72):
    ax.plot([x, x], [-3.55, 3.15], color=MUTED, lw=0.7, ls=(0, (4, 3)), zorder=1)
ax.text(-4.00, 3.35, "OUTER EAR", fontsize=6.2, color=MUTED, ha='center')
ax.text(-0.65, 3.35, "MIDDLE EAR", fontsize=6.2, color=MUTED, ha='center')
ax.text(3.00, 3.35, "INNER EAR", fontsize=6.2, color=MUTED, ha='center')

def lab(txt, tip, tx, ty, ha='left', fs=6.0):
    ax.annotate(txt, xy=tip, xytext=(tx, ty), fontsize=fs, color=INK, ha=ha,
                va='center', zorder=20,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.65,
                                shrinkA=2.0, shrinkB=1.0))

lab("pinna", (-5.85, 1.05), -6.90, 2.35, ha='left')
lab("auditory canal", (-3.40, 0.25), -6.90, -1.45, ha='left')
lab("tympanic membrane\n(ear drum)", (-1.72, -0.55), -5.15, -2.85, ha='center')
lab("malleus", (-1.35, 0.72), -2.55, 2.15, ha='center')
lab("incus", (-0.65, 0.88), -1.05, 2.60, ha='center')
lab("stapes", (0.05, 0.62), 0.35, 2.15, ha='center')
lab("oval window", (0.45, 0.45), 1.95, -0.05, ha='left', fs=5.9)
lab("round window", (0.40, -0.58), -0.20, -1.25, ha='right', fs=5.9)
lab("Eustachian tube\n→ pharynx", (-1.05, -2.62), -2.30, -3.95, ha='center')
lab("semicircular\ncanals", (2.62, 2.55), 4.85, 2.60, ha='left')
lab("vestibule (utriculus\n+ sacculus)", (1.15, 0.72), 4.85, 1.30, ha='left')
lab("cochlea", (3.05, -0.55), 4.85, -0.35, ha='left')
lab("auditory nerve\n→ brain", (4.20, -2.98), 4.85, -1.95, ha='left')
ax.set_xlim(-7.05, 7.05); ax.set_ylim(-4.35, 3.75)
ax.set_aspect('equal'); ax.axis('off')
```

Sound waves collected by the **pinna** travel down the auditory canal and
vibrate the **tympanic membrane**. The three ear ossicles —
**malleus → incus → stapes**, the smallest bones in the body — act as levers
that amplify the vibration about 20 times and pass it through the **oval
window** into the fluid of the **cochlea**. Inside the cochlea, the **organ of
Corti** on the basilar membrane carries hair cells that convert the fluid wave
into impulses, which the auditory nerve carries to the temporal lobe. The
**round window** lets the fluid move; the **Eustachian tube** connects the middle
ear to the pharynx and equalises air pressure on the two sides of the ear drum
(which is why the ears "pop" on the drive up to Muktinath). The three
**semicircular canals**, set in three planes at right angles, detect rotation
(dynamic balance), while the **utriculus** and **sacculus** with their otoliths
detect the position of the head (static balance). Humans hear
**20 Hz to 20 000 Hz**.

| Sense organ | Receptor | Stimulus detected |
|---|---|---|
| Eye | rods and cones of the retina | light (photoreceptor) |
| Ear | organ of Corti; cristae and maculae | sound; rotation and gravity |
| Nose | olfactory epithelium | chemicals in air (smell) |
| Tongue | taste buds (sweet, sour, salt, bitter, umami) | chemicals in solution |
| Skin | Meissner, Pacinian, Krause, Ruffini, free nerve endings | touch, pressure, cold, heat, pain |

## 8.7 Endocrinology

The endocrine system is the body's *slow but far-reaching* control system.
**Endocrine (ductless) glands** pour their secretion, a **hormone**, straight
into the blood, which carries it to distant **target organs** that have matching
receptors. Hormones are needed in minute amounts, are not stored in the target,
and are destroyed after use — so they must be secreted continuously.

| Feature | Nervous system | Endocrine system |
|---|---|---|
| Message carried by | electrical impulse along a neuron | chemical hormone in blood |
| Route | fixed "wire" to one target | whole bloodstream, any cell with the receptor |
| Speed of response | milliseconds | seconds to hours |
| Duration of effect | very brief | long, sometimes lifelong (growth) |
| Control of | muscles and glands | metabolism, growth, reproduction |
| Feedback | reflex arc | negative feedback loops |

Chemically, hormones are of three kinds: **peptides/proteins** (insulin, GH,
ADH), **steroids** (cortisol, aldosterone, testosterone, oestrogen — made from
cholesterol) and **amino-acid derivatives** (thyroxine, adrenaline). Because
steroids are lipid-soluble they pass straight through the cell membrane and act
on the genes; peptide hormones cannot, so they bind a surface receptor and work
through a **second messenger** such as cyclic AMP.

```figure caption="The main endocrine glands of the human body. Hypophysis = pituitary."
from matplotlib.patches import Ellipse, Circle, Polygon, PathPatch, FancyBboxPatch
from matplotlib.path import Path

fig, ax = plt.subplots(figsize=(5.2, 4.4))
SKIN = "#f7ece2"; SKE = "#b9a191"; GL = "#e2b24a"; GLE = "#8a6a20"

BODY = [(0.00, 9.45),
        (0.62, 9.45), (1.00, 8.95), (0.96, 8.42),
        (0.92, 7.95), (0.70, 7.72), (1.30, 7.55),
        (2.20, 7.32), (2.45, 6.85), (2.48, 6.05),
        (2.52, 5.05), (2.62, 4.35), (2.72, 3.85),
        (2.80, 3.45), (2.35, 3.38), (2.20, 3.80),
        (2.00, 4.55), (1.86, 5.10), (1.80, 5.55),
        (1.74, 6.00), (1.86, 4.20), (1.70, 3.10),
        (1.58, 2.10), (1.55, 1.00), (1.35, 0.05),
        (1.05, -0.60), (0.55, -0.55), (0.42, 0.20),
        (0.30, 0.95), (0.25, 1.65), (0.00, 2.30),
        (-0.25, 1.65), (-0.30, 0.95), (-0.42, 0.20),
        (-0.55, -0.55), (-1.05, -0.60), (-1.35, 0.05),
        (-1.55, 1.00), (-1.58, 2.10), (-1.70, 3.10),
        (-1.86, 4.20), (-1.74, 6.00), (-1.80, 5.55),
        (-1.86, 5.10), (-2.00, 4.55), (-2.20, 3.80),
        (-2.35, 3.38), (-2.80, 3.45), (-2.72, 3.85),
        (-2.62, 4.35), (-2.52, 5.05), (-2.48, 6.05),
        (-2.45, 6.85), (-2.20, 7.32), (-1.30, 7.55),
        (-0.70, 7.72), (-0.92, 7.95), (-0.96, 8.42),
        (-1.00, 8.95), (-0.62, 9.45), (0.00, 9.45)]
ax.add_patch(PathPatch(Path(BODY, [Path.MOVETO] + [Path.CURVE4]*60),
                       fc=SKIN, ec=SKE, lw=1.1, zorder=2))

def gland(x, y, w, h, angle=0):
    ax.add_patch(Ellipse((x, y), w, h, angle=angle, fc=GL, ec=GLE, lw=0.9,
                         zorder=5))

gland(0.00, 8.92, 0.34, 0.26)
gland(0.00, 8.55, 0.30, 0.22)
for s in (-1, 1):
    ax.add_patch(Polygon([(s*0.10, 7.92), (s*0.52, 8.10), (s*0.46, 7.55),
                          (s*0.12, 7.62)], closed=True, fc=GL, ec=GLE,
                         lw=0.9, zorder=5))
    ax.add_patch(Circle((s*0.34, 7.80), 0.055, fc="#8a3a1a", ec='none', zorder=6))
gland(0.00, 6.85, 0.95, 1.05)
for s in (-1, 1):
    ax.add_patch(Polygon([(s*0.30, 5.62), (s*1.05, 5.72), (s*1.00, 5.30),
                          (s*0.32, 5.30)], closed=True, fc=GL, ec=GLE,
                         lw=0.9, zorder=5))
gland(0.55, 4.72, 1.70, 0.70, angle=-12)
for s in (-1, 1):
    gland(s*0.92, 3.02, 0.50, 0.40)
gland(0.00, 2.74, 1.05, 0.62)
for s in (-1, 1):
    ax.add_patch(Circle((s*0.34, 2.02), 0.20, fc=GL, ec=GLE, lw=0.9, zorder=5))

def lab(txt, tip, tx, ty, ha='left', fs=6.1):
    ax.annotate(txt, xy=tip, xytext=(tx, ty), fontsize=fs, color=INK, ha=ha,
                va='center', zorder=20,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.65,
                                shrinkA=2.0, shrinkB=1.0))

lab("pineal body", (-0.16, 8.93), -1.30, 9.55, ha='right')
lab("hypophysis (pituitary)", (-0.15, 8.55), -1.30, 8.45, ha='right')
lab("thyroid + parathyroids", (-0.48, 7.82), -1.70, 7.40, ha='right')
lab("thymus", (-0.46, 6.92), -2.65, 6.55, ha='right')
lab("adrenal glands", (-0.98, 5.52), -2.70, 5.35, ha='right')
lab("pancreas\n(islets of Langerhans)", (-0.28, 4.62), -2.95, 4.15, ha='right')
lab("ovaries (female)", (-1.14, 3.05), -2.10, 3.30, ha='right')
lab("uterus", (-0.52, 2.74), -1.95, 2.45, ha='right')
lab("testes (male)", (-0.52, 2.02), -1.85, 1.60, ha='right')
ax.text(3.15, 8.95, "Every gland shown\nhere is ductless: it\nsecretes straight\ninto the blood.",
        fontsize=6.0, color=MUTED, ha='left', va='top', linespacing=1.4)
ax.set_xlim(-6.95, 6.65); ax.set_ylim(-1.10, 10.15)
ax.set_aspect('equal'); ax.axis('off')
```

### Hypothalamus and the hypophysis (pituitary gland)

The **hypophysis** or pituitary is a pea-sized gland, about 0.5 g, hanging by a stalk (the *infundibulum*) from the floor of the hypothalamus and resting in the **sella turcica**, a hollow in the sphenoid bone. It has two parts of completely different origin:

- The **adenohypophysis** (anterior lobe) develops from **Rathke's pouch**, an upgrowth of the embryonic mouth roof. It is true glandular tissue and makes its own hormones.
- The **neurohypophysis** (posterior lobe) is a downgrowth of the brain. It makes nothing: it only **stores and releases** two hormones manufactured in the hypothalamus.

The hypothalamus controls the anterior lobe chemically, through a private blood route called the **hypothalamo-hypophyseal portal system** — capillaries in the hypothalamus drain into veins that break up into capillaries again in the anterior lobe. Hypothalamic neurons pour **releasing hormones** (GnRH, TRH, CRH, GHRH) and **inhibiting hormones** (somatostatin, PIH) into this portal blood in nanogram amounts, and the anterior lobe responds. The posterior lobe is controlled *neurally* instead: the hormones **ADH** and **oxytocin** are made in the supraoptic and paraventricular nuclei of the hypothalamus and travel down the axons themselves.

```figure caption="The hypothalamo-hypophyseal axis. Left: the two lobes and their two control routes. Right: negative feedback in the thyroid axis — the product switches off its own command."
from matplotlib.patches import Ellipse, FancyBboxPatch, FancyArrowPatch, PathPatch
from matplotlib.path import Path

fig, axs = plt.subplots(1, 2, figsize=(5.2, 3.0),
                        gridspec_kw=dict(width_ratios=[1.0, 0.92], wspace=0.10))
ANT = "#d98a3d"; POS = "#5b86c4"; HY = "#9c7bb8"

# ---------------- panel a : the gland ----------------
ax = axs[0]
ax.add_patch(FancyBboxPatch((-1.62, 2.05), 3.24, 0.98,
                            boxstyle="round,pad=0.08,rounding_size=0.26",
                            fc="#efe6f5", ec=HY, lw=1.1, zorder=2))
ax.text(0.00, 2.54, "HYPOTHALAMUS", fontsize=6.4, color=HY, ha='center',
        va='center', fontweight='bold', zorder=6)
ax.plot([-0.05, -0.05], [2.05, 1.40], color=MUTED, lw=2.6,
        solid_capstyle='round', zorder=3)
ax.add_patch(Ellipse((-0.95, 1.00), 1.90, 1.20, fc="#f6dcc2", ec=ANT, lw=1.1,
                     zorder=4))
ax.add_patch(Ellipse((1.00, 1.02), 1.80, 1.10, fc="#d9e4f4", ec=POS, lw=1.1,
                     zorder=4))
ax.text(-0.95, 1.00, "ANTERIOR\n(adeno-)", fontsize=5.0, color=ANT,
        ha='center', va='center', fontweight='bold', zorder=6, linespacing=1.3)
ax.text(1.00, 1.02, "POSTERIOR\n(neuro-)", fontsize=5.0, color=POS,
        ha='center', va='center', fontweight='bold', zorder=6, linespacing=1.3)

ax.annotate("", xy=(-1.15, 1.58), xytext=(-1.28, 2.02), zorder=7,
            arrowprops=dict(arrowstyle='-|>', color=ANT, lw=1.3,
                            mutation_scale=8))
ax.text(-2.02, 1.80, "portal\nblood", fontsize=5.9, color=ANT,
        ha='right', va='center', linespacing=1.35, zorder=6)
ax.annotate("", xy=(0.85, 1.55), xytext=(0.45, 2.02), zorder=7,
            arrowprops=dict(arrowstyle='-|>', color=POS, lw=1.3,
                            mutation_scale=8))
ax.text(1.98, 1.80, "down\naxons", fontsize=5.9, color=POS,
        ha='left', va='center', linespacing=1.35, zorder=6)

ax.text(-1.55, 0.24, "GH  TSH  ACTH\nFSH  LH  prolactin", fontsize=5.9,
        color=INK, ha='center', va='top', linespacing=1.4, zorder=6)
ax.text(1.55, 0.24, "ADH\noxytocin", fontsize=5.9, color=INK, ha='center',
        va='top', linespacing=1.4, zorder=6)
ax.annotate("", xy=(-1.30, 0.34), xytext=(-1.00, 0.42), zorder=5,
            arrowprops=dict(arrowstyle='-|>', color=ANT, lw=1.0,
                            mutation_scale=7))
ax.annotate("", xy=(1.40, 0.34), xytext=(1.05, 0.48), zorder=5,
            arrowprops=dict(arrowstyle='-|>', color=POS, lw=1.0,
                            mutation_scale=7))
ax.text(-0.18, 3.26, "(a) two lobes, two control routes", fontsize=6.3,
        color=MUTED, ha='center', va='bottom')
ax.set_xlim(-3.35, 3.00); ax.set_ylim(-0.75, 3.55)
ax.set_aspect('equal'); ax.axis('off')

# ---------------- panel b : negative feedback ----------------
ax = axs[1]
BOX = [(0.00, 3.30, "HYPOTHALAMUS", HY, "#efe6f5"),
       (0.00, 2.10, "ANTERIOR PITUITARY", ANT, "#f6dcc2"),
       (0.00, 0.90, "THYROID GLAND", "#2e8b57", "#dcefe3"),
       (0.00, -0.30, "T₃ / T₄ in blood", INK, "#eceff4")]
for x, y, t, c, f in BOX:
    ax.add_patch(FancyBboxPatch((x-1.28, y-0.28), 2.56, 0.56,
                                boxstyle="round,pad=0.05,rounding_size=0.14",
                                fc=f, ec=c, lw=1.0, zorder=4))
    ax.text(x, y, t, fontsize=6.0, color=c, ha='center', va='center',
            fontweight='bold', zorder=6)
for y0, y1, lb in ((3.30, 2.10, "TRH"), (2.10, 0.90, "TSH"),
                   (0.90, -0.30, "secretes")):
    ax.annotate("", xy=(0.00, y1+0.30), xytext=(0.00, y0-0.30), zorder=5,
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.2,
                                mutation_scale=8))
    ax.text(0.12, (y0+y1)/2, lb, fontsize=5.9, color=MUTED, ha='left',
            va='center', zorder=6)
for yt, dx in ((3.30, 2.05), (2.10, 1.72)):
    ax.add_patch(FancyArrowPatch((-1.30, -0.30), (-1.30, yt),
                                 connectionstyle=f"arc3,rad=0.40",
                                 arrowstyle='-|>', color="#d9534f", lw=1.1,
                                 mutation_scale=8, zorder=3))
ax.text(-2.62, 1.50, "NEGATIVE\nFEEDBACK\n(−)", fontsize=6.1, color="#d9534f",
        ha='center', va='center', fontweight='bold', linespacing=1.4, zorder=6)
ax.text(0.00, 4.02, "(b) the thyroid axis", fontsize=6.3, color=MUTED,
        ha='center', va='bottom')
ax.set_xlim(-3.45, 1.75); ax.set_ylim(-1.05, 4.35)
ax.set_aspect('equal'); ax.axis('off')
```

**Hormones of the anterior lobe.** Six, and NEB expects all six.

1. **Growth hormone (GH, somatotropin)** — promotes growth of the long bones and muscles, protein synthesis and fat breakdown. Hyposecretion in childhood gives **pituitary dwarfism** (small but normally proportioned, normal intelligence); hypersecretion in childhood gives **gigantism**; hypersecretion after the epiphyses have closed gives **acromegaly** — thickened jaw, hands and feet.
2. **Thyroid-stimulating hormone (TSH)** — drives the thyroid to make T₃ and T₄.
3. **Adrenocorticotropic hormone (ACTH)** — drives the adrenal *cortex* to make glucocorticoids.
4. **Follicle-stimulating hormone (FSH)** — ripens the Graafian follicle in the ovary; starts spermatogenesis in the testis.
5. **Luteinising hormone (LH)**, called **ICSH** in the male — triggers ovulation and forms the corpus luteum; stimulates Leydig cells to make testosterone.
6. **Prolactin (LTH)** — starts and maintains milk secretion after childbirth.

The **pars intermedia** secretes **melanocyte-stimulating hormone (MSH)**, which disperses melanin granules; in humans it is nearly vestigial. Because the anterior lobe controls the thyroid, adrenal cortex and gonads, it is traditionally called the **master gland** — although the hypothalamus is the real master above it.

**Hormones of the posterior lobe.** Both are small nonapeptides (9 amino acids).

- **ADH (vasopressin)** makes the DCT and collecting duct permeable to water, concentrating the urine (§8.4). Deficiency causes **diabetes insipidus**: 10–20 litres of dilute, tasteless urine a day and raging thirst.
- **Oxytocin** contracts the smooth muscle of the uterus during labour and causes **milk ejection** from the mammary glands. It is the textbook example of **positive feedback** — stretching of the cervix triggers oxytocin, which contracts the uterus, which stretches the cervix more, until the baby is delivered.

### Thyroid gland

The thyroid is the **largest purely endocrine gland**, about 25 g, made of two lobes on either side of the trachea joined across the front by a bridge, the **isthmus**. Its tissue is a mass of hollow **follicles** filled with a jelly called **colloid**, which stores the hormone bound to the protein **thyroglobulin** — the only endocrine gland that stockpiles its product outside its cells.

The follicle cells trap iodide from the blood and build **thyroxine (T₄, tetraiodothyronine)** and **triiodothyronine (T₃)**. T₃ is several times more active but is made in smaller amount. Their job is to set the **basal metabolic rate**: they raise oxygen consumption and heat production in almost every cell, speed up carbohydrate and fat oxidation, and are essential for normal growth and brain development in the infant. They are often called the *personality hormone* because a deficiency dulls mental activity. An adult needs about **150 µg of iodine a day**.

Scattered between the follicles are the **parafollicular (C) cells**, which secrete **calcitonin** — this *lowers* blood calcium by inhibiting the release of calcium from bone. It opposes parathormone.

::: caution Goitre is not one disease
A goitre is simply a swollen thyroid, and it happens in *both* directions. In **endemic (simple) goitre** there is too little dietary iodine, so T₄ cannot be made; T₄ never rises, TSH is never switched off by feedback, and the gland enlarges as it is flogged by TSH — the hormone level is *low*. In **Graves' disease (exophthalmic goitre)** the gland is enlarged *and* overactive, with a racing pulse, weight loss despite a good appetite and bulging eyeballs. Hill districts of Nepal were historically iodine-deficient, which is why salt is iodised.
:::

| Thyroid disorder | Direction | Main features |
|---|---|---|
| Simple (endemic) goitre | Iodine lack, low T₄ | Swollen neck, sluggishness |
| **Cretinism** | Hyposecretion in infancy | Stunted growth, retarded mental development, protruding tongue |
| **Myxoedema (Gull's disease)** | Hyposecretion in adult | Puffy face, dry skin, slow pulse, low BMR, weight gain, feels cold |
| **Graves' disease** | Hypersecretion | High BMR, weight loss, rapid heart, tremor, exophthalmos |

### Parathyroid glands

Four small glands — about 0.05 g each — are embedded in pairs on the **back surface of the thyroid lobes**. They secrete **parathormone (PTH, Collip's hormone)**, the main regulator of blood calcium, which is normally held at **9–11 mg per 100 ml**. PTH raises blood Ca²⁺ in three ways: it activates osteoclasts so bone releases calcium; it increases calcium reabsorption (and phosphate excretion) in the kidney tubule; and it activates vitamin D, which increases calcium absorption from the intestine.

Hyposecretion drops blood calcium and causes **hypocalcaemic tetany** — sustained, painful spasms of the muscles of the hands, feet and larynx, which can be fatal. Hypersecretion strips calcium out of the skeleton, leaving bones soft and easily broken, and deposits it as kidney stones.

### Adrenal (suprarenal) glands

A pair of caps, one on the upper pole of each kidney, each about 5 g. Each is really **two glands in one**, with different embryonic origins:

**The cortex** (outer, mesodermal, essential for life) has three zones, from outside in:

| Zone | Hormone class | Example | Action |
|---|---|---|---|
| Zona glomerulosa | Mineralocorticoid | **Aldosterone** | Na⁺ and water reabsorbed, K⁺ excreted in DCT/collecting duct → raises blood volume and BP |
| Zona fasciculata | Glucocorticoid | **Cortisol** | Gluconeogenesis from protein and fat, raises blood glucose, anti-inflammatory, suppresses immunity |
| Zona reticularis | Sex corticoid | Androgens | Small amounts; pubic and axillary hair |

**The medulla** (inner, ectodermal, derived from neural crest — effectively a modified sympathetic ganglion) secretes **adrenaline (epinephrine)**, about 80 %, and **noradrenaline**, about 20 %. These are the **emergency hormones** of *fight, flight and fright*: heart rate and force rise, blood pressure rises, bronchioles and pupils dilate, blood is shunted from the gut and skin to the skeletal muscles, and glycogenolysis floods the blood with glucose. The medulla is not essential for life — the sympathetic nerves can do the same work.

| Adrenal disorder | Cause | Features |
|---|---|---|
| **Addison's disease** | Cortical hyposecretion | Bronze pigmentation of skin, low blood Na⁺ and BP, weakness, weight loss |
| **Cushing's syndrome** | Glucocorticoid hypersecretion | Moon face, buffalo hump, trunk obesity with thin limbs, high blood glucose |
| **Conn's syndrome** | Aldosterone hypersecretion | Na⁺ retention, K⁺ loss, high blood pressure |

### Islets of Langerhans (endocrine pancreas)

The pancreas is a **heterocrine (mixed) gland**: the acini are exocrine and pour pancreatic juice into the duodenum (§8.1), while about 1–2 % of its mass is scattered as one to two million ductless clumps, the **islets of Langerhans**.

| Islet cell | Share | Hormone | Effect on blood glucose |
|---|---|---|---|
| **β (beta)** | ~70 % | **Insulin** | **Lowers** it — glucose enters cells, glycogenesis in liver and muscle, lipogenesis |
| **α (alpha)** | ~20 % | **Glucagon** | **Raises** it — glycogenolysis and gluconeogenesis in the liver |
| δ (delta) | ~5 % | Somatostatin | Inhibits both of the above |
| F (PP) | ~2 % | Pancreatic polypeptide | Damps pancreatic secretion |

Insulin (Banting and Best, 1921) is a protein of **51 amino acids** in two chains joined by disulphide bridges. Fasting blood glucose is normally **70–110 mg per 100 ml**; insulin and glucagon are antagonists that hold it there.

**Diabetes mellitus** follows a lack of insulin or a failure of the tissues to respond to it. Blood glucose climbs past the renal threshold of 180 mg/100 ml, so glucose appears in the urine (**glycosuria**) and drags water with it osmotically. The classical signs are the *three P's*: **polyuria** (excessive urine), **polydipsia** (excessive thirst) and **polyphagia** (excessive hunger), with weight loss. Because glucose cannot be used, fat is burned instead and **ketone bodies** accumulate, giving acidosis. **Type 1 (IDDM)** is autoimmune destruction of β cells, begins young and needs injected insulin; **Type 2 (NIDDM)** is insulin resistance, begins in middle age and is linked to obesity and inactivity.

### Gonads, pineal body and thymus

- **Testis** — the **interstitial cells of Leydig**, stimulated by LH/ICSH, secrete **testosterone**: it drives spermatogenesis and the male secondary sexual characters (beard, deep voice, muscular build). Sertoli cells secrete **inhibin**, which feeds back to damp FSH.
- **Ovary** — the ripening **Graafian follicle** secretes **oestrogen** (female secondary sexual characters, repair of the uterine lining); the **corpus luteum** secretes **progesterone**, the "pregnancy hormone", which makes the endometrium secretory and holds a pregnancy; **relaxin** loosens the pubic symphysis at birth.
- **Pineal body (epiphysis cerebri)** — a tiny gland on the roof of the diencephalon secreting **melatonin**, which governs the daily (circadian) sleep–wake rhythm, pigmentation and the timing of puberty — it inhibits the gonads until puberty. Secretion is high in darkness.
- **Thymus** — behind the sternum; secretes **thymosin**, under which T-lymphocytes mature. It is large in the child and **atrophies after puberty**, which is why immunity weakens with age.

Some organs that are not glands also secrete hormones: the stomach (**gastrin**), the duodenum (**secretin**, **cholecystokinin**), the kidney (**erythropoietin**, which drives red-cell production) and the heart (**atrial natriuretic factor**, which lowers blood pressure).

| Gland | Hormone | Target | Principal effect |
|---|---|---|---|
| Hypothalamus | Releasing/inhibiting hormones | Anterior pituitary | Switch each pituitary hormone on or off |
| Anterior pituitary | GH | Bones, muscles | Growth, protein synthesis |
| | TSH | Thyroid | T₃/T₄ secretion |
| | ACTH | Adrenal cortex | Glucocorticoid secretion |
| | FSH | Ovary / testis | Follicle ripening; spermatogenesis |
| | LH (ICSH) | Ovary / testis | Ovulation, corpus luteum; testosterone |
| | Prolactin | Mammary gland | Milk secretion |
| Posterior pituitary | ADH | Kidney tubule | Water reabsorption |
| | Oxytocin | Uterus, mammary gland | Labour contractions, milk ejection |
| Thyroid | T₄ / T₃ | All cells | Raise BMR; growth and brain development |
| | Calcitonin | Bone | Lowers blood Ca²⁺ |
| Parathyroid | Parathormone | Bone, kidney, gut | Raises blood Ca²⁺ |
| Adrenal cortex | Aldosterone | Kidney tubule | Na⁺ retention, K⁺ loss, raises BP |
| | Cortisol | Liver, immune cells | Raises blood glucose, anti-inflammatory |
| Adrenal medulla | Adrenaline | Heart, vessels, liver | Emergency response, raises glucose and BP |
| Pancreas (β) | Insulin | Liver, muscle, fat | **Lowers** blood glucose |
| Pancreas (α) | Glucagon | Liver | **Raises** blood glucose |
| Testis | Testosterone | Whole body | Male secondary sexual characters |
| Ovary | Oestrogen | Whole body | Female secondary sexual characters |
| | Progesterone | Uterus | Maintains pregnancy |
| Pineal | Melatonin | Brain, gonads | Circadian rhythm, delays puberty |
| Thymus | Thymosin | T-lymphocytes | Maturation of T cells |

::: memory Two hormones that raise, one that lowers
Blood glucose is *raised* by glucagon, adrenaline, cortisol and GH, but *lowered* by **insulin alone**. That is why the loss of one hormone — insulin — causes a disease as serious as diabetes mellitus: there is no substitute for it.
:::

## 8.8 Reproductive System

Every other system in this chapter keeps *one* body alive. The reproductive system keeps the *species* alive, and it is the only system that is not needed for the individual's own survival. In humans reproduction is **sexual**, **viviparous** (the young develop inside the mother) and **dioecious** (the sexes are in separate individuals), with internal fertilisation.

```figure caption="The human reproductive systems in front view. (a) Male. (b) Female, with the uterus opened to show the cavity."
from matplotlib.patches import Ellipse, Circle, PathPatch, FancyBboxPatch, Arc
from matplotlib.path import Path

fig, axs = plt.subplots(1, 2, figsize=(5.2, 3.6),
                        gridspec_kw=dict(width_ratios=[1, 1], wspace=0.16))
ORG = "#f2ddc6"; OE = "#b08a5e"; GL = "#e2b24a"; GE = "#8a6a20"
TUB = "#9c7f63"; LUM = "#fdf4e8"; MUS = "#e8c3c3"; ME = "#b07878"

def tube(ax, pts, w=5.0, c=TUB, l=LUM, z=6):
    x, y = np.array(pts).T
    ax.plot(x, y, color=c, lw=w, solid_capstyle='round', zorder=z)
    ax.plot(x, y, color=l, lw=w*0.45, solid_capstyle='round', zorder=z+0.1)

def lab(ax, txt, tip, tx, ty, ha='left', fs=6.0):
    ax.annotate(txt, xy=tip, xytext=(tx, ty), fontsize=fs, color=INK, ha=ha,
                va='center', zorder=25,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.65,
                                shrinkA=2.0, shrinkB=1.0))

# ------------------------------------------------ (a) male
ax = axs[0]
ax.add_patch(Ellipse((0.00, 1.55), 4.70, 2.35, fc="#f7ece2", ec="#c9b09a",
                     lw=1.0, zorder=1))                      # scrotum
for s in (-1, 1):
    ax.add_patch(Ellipse((s*1.42, 1.58), 1.05, 1.30, fc=ORG, ec=OE, lw=1.0,
                         zorder=3))                          # testis
    ax.add_patch(Arc((s*1.42, 1.58), 1.62, 1.80, angle=0,
                     theta1=-78 if s > 0 else 102, theta2=78 if s > 0 else 258,
                     color="#7a6046", lw=2.4, zorder=4))     # epididymis
    tube(ax, [(s*2.05, 2.15), (s*1.86, 2.95), (s*1.48, 3.58),
              (s*0.92, 3.86), (s*0.40, 3.62)], w=4.2)        # vas deferens
    ax.add_patch(Ellipse((s*1.30, 4.32), 1.25, 0.52, angle=-s*32, fc=GL,
                         ec=GE, lw=0.9, zorder=5))           # seminal vesicle
    ax.add_patch(Circle((s*0.62, 2.88), 0.16, fc=GL, ec=GE, lw=0.8, zorder=7))
ax.add_patch(Ellipse((0.00, 5.10), 2.20, 1.55, fc="#dfe8f4", ec="#7a94b6",
                     lw=1.0, zorder=4))                      # bladder
ax.add_patch(Ellipse((0.00, 3.42), 1.30, 0.82, fc=GL, ec=GE, lw=1.0, zorder=6))
ax.add_patch(FancyBboxPatch((-0.40, -0.28), 0.80, 2.60,
                            boxstyle="round,pad=0.02,rounding_size=0.32",
                            fc=ORG, ec=OE, lw=1.0, zorder=8))  # penis
ax.add_patch(Ellipse((0.00, -0.26), 0.94, 0.58, fc="#e9cdb2", ec=OE, lw=1.0,
                     zorder=9))                              # glans
tube(ax, [(0.00, 4.30), (0.00, -0.36)], w=3.6, z=10)         # urethra

lab(ax, "urinary bladder", (-0.94, 5.42), -1.70, 6.20, ha='right')
lab(ax, "vas deferens", (-1.86, 3.05), -2.65, 4.15, ha='right')
lab(ax, "epididymis", (-2.18, 1.90), -2.75, 2.65, ha='right')
lab(ax, "testis", (-1.42, 1.30), -2.85, 1.55, ha='right')
lab(ax, "scrotum", (-2.05, 0.90), -2.85, 0.55, ha='right')
lab(ax, "seminal vesicle", (1.72, 4.55), 1.75, 5.70, ha='left')
lab(ax, "prostate", (0.58, 3.46), 1.75, 4.30, ha='left')
lab(ax, "Cowper's gland", (0.76, 2.88), 1.75, 3.05, ha='left')
lab(ax, "urethra", (0.00, 2.05), 1.55, 1.95, ha='left')
lab(ax, "penis", (0.40, 0.90), 1.55, 0.75, ha='left')
ax.text(-0.25, 6.62, "(a) male", fontsize=6.6, color=MUTED, ha='center',
        va='bottom', fontweight='bold')
ax.set_xlim(-5.45, 4.75); ax.set_ylim(-1.05, 7.05)
ax.set_aspect('equal'); ax.axis('off')

# ------------------------------------------------ (b) female
ax = axs[1]
UT = [(-0.95, 3.30), (-0.80, 3.76), (0.80, 3.76), (0.95, 3.30),
      (1.02, 2.90), (0.72, 2.25), (0.52, 1.80),
      (0.44, 1.62), (-0.44, 1.62), (-0.52, 1.80),
      (-0.72, 2.25), (-1.02, 2.90), (-0.95, 3.30)]
ax.add_patch(PathPatch(Path(UT, [Path.MOVETO] + [Path.CURVE4]*12),
                       fc=MUS, ec=ME, lw=1.1, zorder=4))
CAV = [(-0.58, 3.22), (-0.46, 3.54), (0.46, 3.54), (0.58, 3.22),
       (0.60, 2.86), (0.34, 2.28), (0.18, 1.92),
       (0.12, 1.80), (-0.12, 1.80), (-0.18, 1.92),
       (-0.34, 2.28), (-0.60, 2.86), (-0.58, 3.22)]
ax.add_patch(PathPatch(Path(CAV, [Path.MOVETO] + [Path.CURVE4]*12),
                       fc="#fbeeee", ec=ME, lw=0.7, zorder=5))
for s in (-1, 1):
    tube(ax, [(s*0.92, 3.50), (s*1.55, 3.92), (s*2.22, 3.74),
              (s*2.56, 3.12), (s*2.52, 2.74)], w=4.6, z=6)   # oviduct
    for k in range(5):                                        # fimbriae
        th = np.deg2rad(202 + k*34)
        ax.plot([s*2.52, s*2.52 + 0.48*np.cos(th)],
                [2.68, 2.68 + 0.48*np.sin(th)],
                color="#7a6046", lw=0.9, zorder=7, solid_capstyle='round')
    ax.add_patch(Ellipse((s*2.30, 1.90), 1.00, 0.68, angle=-s*12, fc=ORG,
                         ec=OE, lw=1.0, zorder=6))            # ovary
    for k in range(3):
        ax.add_patch(Circle((s*2.30 + (k-1)*0.26,
                             1.90 + (0.11 if k == 1 else -0.05)),
                            0.10, fc="#fdf4e8", ec=OE, lw=0.7, zorder=7))
ax.add_patch(FancyBboxPatch((-0.33, 0.98), 0.66, 0.62,
                            boxstyle="round,pad=0.02,rounding_size=0.10",
                            fc="#dcc4c4", ec=ME, lw=1.0, zorder=6))  # cervix
tube(ax, [(0.00, 1.06), (0.00, 0.08)], w=7.0, c=ME, l="#fbeeee", z=4)

lab(ax, "fallopian tube\n(oviduct)", (1.92, 3.88), 2.55, 5.05, ha='left')
lab(ax, "fimbriae", (2.88, 2.52), 3.40, 3.05, ha='left')
lab(ax, "ovary", (2.76, 1.78), 3.40, 1.90, ha='left')
lab(ax, "Graafian\nfollicles", (2.16, 1.98), 3.40, 0.95, ha='left')
lab(ax, "myometrium", (-0.88, 3.08), -1.70, 4.35, ha='right')
lab(ax, "endometrium", (-0.54, 2.86), -1.70, 3.45, ha='right')
lab(ax, "uterine cavity", (-0.22, 2.30), -1.95, 2.50, ha='right')
lab(ax, "cervix", (-0.35, 1.28), -1.70, 1.40, ha='right')
lab(ax, "vagina", (-0.14, 0.50), -1.70, 0.50, ha='right')
ax.text(0.20, 5.60, "(b) female", fontsize=6.6, color=MUTED, ha='center',
        va='bottom', fontweight='bold')
ax.set_xlim(-4.85, 5.35); ax.set_ylim(-1.05, 7.05)
ax.set_aspect('equal'); ax.axis('off')
```

### Male reproductive system

**Testes.** A pair of oval glands, about 4 × 2.5 cm, held outside the abdomen in the **scrotum** — a skin sac that keeps them **2–2.5 °C below body temperature**, because spermatogenesis fails at core temperature. Each testis is divided into about 250 lobules, and each lobule holds one to three tightly coiled **seminiferous tubules**, the site of sperm formation. Two kinds of cell line the tubule: **germinal cells**, which divide to make sperms, and tall **Sertoli (nurse) cells**, which nourish the developing sperms and secrete **inhibin**. In the connective tissue *between* the tubules lie the **interstitial cells of Leydig**, which make testosterone.

**Duct system.** Seminiferous tubules → **rete testis** → **vasa efferentia** → **epididymis** (a 6-metre coiled tube on the back of the testis where sperms mature and are stored) → **vas deferens** → **ejaculatory duct** → **urethra**, which passes through the penis and is a shared passage for urine and semen.

**Accessory glands.** The paired **seminal vesicles** contribute about 60 % of the semen, a fluid rich in **fructose** that fuels the sperm tail. The **prostate** adds a thin alkaline milky fluid, about 30 %, which neutralises the acidity of the vagina. The two **Cowper's (bulbourethral) glands** add a lubricating mucus. An ejaculation is **2–5 ml** of semen carrying roughly **200–300 million sperms**.

**The sperm** is about 60 µm long and has four parts: the **head**, mostly nucleus, capped by the enzyme-filled **acrosome** that dissolves a path through the egg coverings; the **neck**, with the centrioles; the **middle piece**, packed with a spiral of mitochondria that supply ATP; and the whip-like **tail** (flagellum) that drives it forward.

### Female reproductive system

**Ovaries.** A pair of almond-shaped glands, about 3 cm long, in the pelvic cavity. They are both **gamete-producing** and **endocrine**. A newborn girl already has about 1–2 million primary oocytes; only some 400 will ever be ovulated.

**Fallopian tubes (oviducts).** Two 10–12 cm tubes. The funnel-shaped **infundibulum** next to the ovary carries finger-like **fimbriae** that sweep the released egg in; the wide **ampulla** that follows is where **fertilisation normally happens**; the narrow **isthmus** opens into the uterus. Cilia and muscular waves move the egg along.

**Uterus (womb).** A hollow, pear-shaped muscular organ the size of a fist, with a **fundus**, **body** and a narrow neck, the **cervix**, opening into the **vagina**. Its wall has three coats: the outer **perimetrium**, the thick muscular **myometrium** that contracts at birth, and the inner glandular **endometrium**, which is rebuilt and shed every month and into which the embryo implants.

### The menstrual cycle

At **menarche** (about 11–14 years) a girl's reproductive tract begins a repeating **28-day cycle** which continues, except during pregnancy, until **menopause** at about 45–50. Day 1 of the cycle is the first day of bleeding.

```figure caption="The 28-day menstrual cycle: pituitary and ovarian hormones, the ovarian events they cause, and the resulting changes in the uterine lining."
fig, axs = plt.subplots(3, 1, figsize=(5.0, 3.4), sharex=True,
                        gridspec_kw=dict(height_ratios=[1.30, 0.62, 0.78],
                                         hspace=0.16))
t = np.linspace(0, 28, 601)

def bump(c, w, h):
    return h*np.exp(-0.5*((t-c)/w)**2)

FSH  = 26 + bump(3.5, 3.0, 26) + bump(13.6, 1.0, 30)
LH   = 16 + bump(13.8, 0.72, 96) + 0.9*t
OES  = 14 + bump(12.6, 2.1, 78) + bump(21.5, 4.0, 34)
PRO  = 6 + bump(21.5, 4.2, 82)

for ax in axs:
    ax.spines[['top', 'right']].set_visible(False)
for x in (5, 14, 28):
    for ax in axs:
        ax.axvline(x, color=GRID, lw=0.8, zorder=0)

ax = axs[0]
for y, lb, c, ls in ((FSH, "FSH", SERIES[0], '-'), (LH, "LH", SERIES[1], '-'),
                     (OES, "oestrogen", SERIES[2], '--'),
                     (PRO, "progesterone", SERIES[3], '--')):
    ax.plot(t, y, color=c, lw=1.5, ls=ls, zorder=3)
ax.text(10.4, 104, "LH surge", fontsize=6.2, color=SERIES[1], ha='right',
        va='center')
ax.annotate("", xy=(13.2, 108), xytext=(10.7, 104), zorder=4,
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=0.8,
                            mutation_scale=7))
ax.text(1.0, 96, "FSH", fontsize=6.4, color=SERIES[0], fontweight='bold')
ax.text(11.2, 66, "oestrogen", fontsize=6.4, color=SERIES[2], ha='right')
ax.text(23.6, 74, "progesterone", fontsize=6.4, color=SERIES[3], ha='center')
ax.set_ylabel("hormone level\n(relative)", fontsize=6.6, labelpad=1.5)
ax.set_ylim(0, 128); ax.set_yticks([])
ax.tick_params(left=False)

ax = axs[1]
from matplotlib.patches import Circle, Wedge
ax.set_ylim(-1.0, 1.0)
for i, (x, r, fc, ec) in enumerate(((2.0, 0.20, "#fdf4e8", "#b08a5e"),
                                    (6.0, 0.28, "#fdf4e8", "#b08a5e"),
                                    (10.0, 0.38, "#fdf4e8", "#b08a5e"),
                                    (13.4, 0.48, "#fdf4e8", "#b08a5e"))):
    ax.add_patch(Circle((x, 0.05), r, fc=fc, ec=ec, lw=0.9, zorder=3,
                        transform=ax.transData))
    ax.add_patch(Circle((x + r*0.34, 0.05 - r*0.30), r*0.30, fc="#e2b24a",
                        ec="#8a6a20", lw=0.6, zorder=4))
ax.add_patch(Circle((16.2, 0.05), 0.24, fc="#e2b24a", ec="#8a6a20", lw=0.8,
                    zorder=3))
ax.annotate("", xy=(15.6, 0.05), xytext=(14.3, 0.05), zorder=3,
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.9,
                            mutation_scale=7))
for x, r in ((19.5, 0.50), (23.0, 0.46), (26.3, 0.26)):
    ax.add_patch(Circle((x, 0.05), r, fc="#f6d9a8", ec="#b08a5e", lw=0.9,
                        zorder=3))
ax.text(6.0, -0.88, "follicle grows", fontsize=6.2, color=MUTED, ha='center')
ax.text(14.1, 0.80, "OVULATION", fontsize=6.3, color=SERIES[1], ha='center',
        fontweight='bold')
ax.text(21.0, -0.88, "corpus luteum → regresses", fontsize=6.2, color=MUTED,
        ha='center')
ax.set_ylabel("ovary", fontsize=6.6, labelpad=1.5)
ax.set_yticks([]); ax.tick_params(left=False)
ax.spines[['left', 'bottom']].set_visible(False)

ax = axs[2]
END = np.where(t <= 5, 3.4 - 0.52*t, 0.0)
END = np.where((t > 5) & (t <= 14), 0.8 + 0.42*(t-5), END)
END = np.where(t > 14, 4.58 + 1.05*(1-np.exp(-(t-14)/3.4)) - 0.10*np.maximum(t-25, 0)**2, END)
ax.fill_between(t, 0, END, color="#f0d3d3", zorder=2)
ax.plot(t, END, color=ME if 'ME' in dir() else "#b07878", lw=1.2, zorder=3)
ax.fill_between(t[t <= 5], 0, END[t <= 5], color="#d9534f", alpha=0.35, zorder=3)
ax.text(2.5, 1.9, "menses", fontsize=6.2, color="#a3302c", ha='center')
ax.text(9.8, 0.80, "proliferative phase", fontsize=6.2, color=MUTED,
        ha='center')
ax.text(20.5, 1.25, "secretory phase", fontsize=6.2, color=MUTED, ha='center')
ax.set_ylabel("uterine\nlining", fontsize=6.6, labelpad=1.5)
ax.set_ylim(0, 7.2); ax.set_yticks([]); ax.tick_params(left=False)
ax.spines['left'].set_visible(False)
ax.set_xlabel("day of cycle", fontsize=7.0, labelpad=1.5)
ax.set_xlim(0, 28); ax.set_xticks([1, 5, 10, 14, 20, 28])
ax.tick_params(labelsize=6.8)
```

The cycle has four phases, and each is driven by the hormones plotted in the figure.

| Phase | Days | Hormones | What happens |
|---|---|---|---|
| **Menstrual** | 1–5 | All four low | The corpus luteum of the last cycle has died, so progesterone collapses; the endometrium breaks down and is shed as **menstrual flow** (50–80 ml of blood, mucus and tissue) |
| **Proliferative (follicular)** | 6–13 | FSH ↑, then oestrogen ↑ | FSH ripens one **Graafian follicle**, which secretes oestrogen; the endometrium is rebuilt and thickens |
| **Ovulatory** | 14 | **LH surge** | High oestrogen triggers a sudden burst of LH; the follicle ruptures and the **secondary oocyte is released** |
| **Secretory (luteal)** | 15–28 | Progesterone ↑ | The empty follicle becomes the yellow **corpus luteum**, whose progesterone makes the endometrium thick, glandular and ready to receive an embryo |

If fertilisation does not occur, the corpus luteum degenerates into the **corpus albicans** by about day 26, progesterone falls, and menstruation begins again. If fertilisation *does* occur, the young embryo secretes **hCG (human chorionic gonadotropin)**, which keeps the corpus luteum alive — so progesterone stays high and there is no menstruation. This is exactly what a pregnancy test detects in urine.

::: caution The fertile window is not day 14 only
The oocyte survives only about **24 hours** after ovulation, but sperms can survive **3–5 days** in the female tract. The fertile period is therefore roughly days 10–17 of a 28-day cycle, not a single day. And the *luteal* phase is the fixed 14 days — it is the follicular phase that varies from woman to woman, which is why "day 14" is only an average.
:::

### Gametogenesis, fertilisation and gestation

**Gametogenesis** is meiotic, so each gamete is haploid (n = 23).

| | Spermatogenesis | Oogenesis |
|---|---|---|
| Site | Seminiferous tubules | Ovary |
| Begins | At puberty | In foetal life, completed after puberty |
| Product of one diploid cell | **4 functional sperms** | **1 ovum + 3 polar bodies** |
| Cytoplasm division | Equal | Unequal — the ovum keeps it all |
| Duration | About 64–74 days, continuous | One ovum per month, interrupted for years |
| Ends | At death (slows with age) | At menopause |

Meiosis in the female is halted twice: the primary oocyte stops in **prophase I** until ovulation, and the secondary oocyte stops in **metaphase II** and only finishes meiosis **if a sperm enters**.

**Fertilisation** takes place in the **ampulla** of the fallopian tube, normally within 24 hours of ovulation. The acrosome releases hyaluronidase and other enzymes that digest a path through the corona radiata and zona pellucida; the moment one sperm fuses with the oocyte membrane, the **cortical reaction** hardens the zona and blocks all other sperms (preventing polyspermy). The oocyte completes meiosis II, the two haploid nuclei fuse, and the diploid **zygote** is formed.

The zygote divides as it travels down the tube, becoming a solid **morula** and then a hollow **blastocyst**, which **implants** in the endometrium about **6–7 days** after fertilisation. The chorion of the embryo and the endometrium of the mother together build the **placenta**, across which oxygen and nutrients diffuse in and CO₂ and nitrogenous waste diffuse out — the two bloodstreams come close but never mix. The placenta is also a temporary endocrine gland, making hCG, oestrogen and progesterone.

**Gestation** lasts about **280 days (40 weeks)** counted from the first day of the last menstrual period. Birth (**parturition**) is triggered by a foetal–maternal hormone cascade in which **oxytocin** from the posterior pituitary contracts the myometrium in a positive-feedback loop. After delivery, **prolactin** starts milk secretion and oxytocin ejects it; the first milk, **colostrum**, is thin and yellowish and is rich in antibodies (IgA) that give the newborn passive immunity.

::: example How long can the ovaries keep going?
**Problem.** A girl reaches menarche at 13 and menopause at 49. If she ovulates once every 28 days and has two pregnancies, each removing 10 months of cycling, estimate the number of ova she releases in her lifetime. Compare this with the 1 million primary oocytes present at birth.

**Solution.**
Total reproductive span = 49 − 13 = 36 years = 36 × 365 = 13 140 days.
Time lost to pregnancy = 2 × 10 months = 20 months = 20 × 30 = 600 days.
Cycling time = 13 140 − 600 = 12 540 days.

$$ N = \frac{12\,540}{28} \approx 448 \text{ ova} $$

Fraction of the original stock used:

$$ \frac{448}{1\,000\,000} \times 100 \approx 0.045\,\% $$

Fewer than one oocyte in two thousand is ever ovulated; the rest degenerate by **atresia**. This is why a female is born with all the oocytes she will ever have, yet never runs short of them before menopause.
:::

## Chapter summary

- **Digestion** is chemical hydrolysis by enzymes, each with its own optimum pH: salivary amylase 6.8, pepsin 1.5–2.0, pancreatic and intestinal enzymes 7–8. Absorption happens in the ileum across **villi**, which raise the surface area to about 250 m².
- **Breathing** moves air; **respiration** releases energy. Tidal volume 500 ml, vital capacity 4500 ml, total lung capacity 5800 ml, residual volume 1200 ml. Pulmonary ventilation = tidal volume × breathing rate ≈ 500 × 12 = 6000 ml min⁻¹.
- Gas exchange is **pure diffusion** across the 0.5 µm alveolar wall over about 70 m² of surface. Oxygen travels as **oxyhaemoglobin** (1 g Hb carries 1.34 ml O₂); most CO₂ travels as **bicarbonate**.
- **Cardiac output** $= \text{stroke volume} \times \text{heart rate} = 70 \times 72 \approx 5000$ ml min⁻¹. The cardiac cycle lasts **0.8 s** (atrial systole 0.1 s, ventricular systole 0.3 s, joint diastole 0.4 s); normal BP is **120/80 mmHg**. The heart beats **myogenically**, from the SA node.
- **Urine formation** = ultrafiltration + selective reabsorption + tubular secretion. Net filtration pressure $= 55 - (15 + 30) = 10$ mmHg; **GFR = 125 ml min⁻¹ = 180 L day⁻¹**, of which more than 99 % is reabsorbed to leave 1–1.5 L of urine.
- A **nerve impulse** is a self-propagating reversal of membrane potential from **−70 mV** to **+35 mV**, restored by the Na⁺–K⁺ pump (3 Na⁺ out : 2 K⁺ in). Conduction is **saltatory** and up to 100 times faster in myelinated fibres. Conduction velocity = distance ÷ time.
- **Hormones** are chemical messengers carried in the blood: slow to start, long to act, controlled by **negative feedback** through the hypothalamo-hypophyseal axis. Insulin alone lowers blood glucose (normal 70–110 mg per 100 ml); glucagon, adrenaline, cortisol and GH raise it.
- The **menstrual cycle** is 28 days: menses 1–5, proliferative 6–13, ovulation at **14** on the LH surge, secretory 15–28 under progesterone from the corpus luteum. Fertilisation occurs in the **ampulla**; gestation is **280 days**.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The enzyme that works best at pH 1.5–2.0 is <span class="marks">[1]</span>
   (a) salivary amylase (b) pepsin (c) trypsin (d) intestinal lipase
2. Which lung volume **cannot** be measured with a spirometer? <span class="marks">[1]</span>
   (a) tidal volume (b) inspiratory reserve volume (c) vital capacity (d) residual volume
3. If the stroke volume is 80 ml and the heart rate is 75 beats per minute, the cardiac output is <span class="marks">[1]</span>
   (a) 4 L min⁻¹ (b) 5 L min⁻¹ (c) 6 L min⁻¹ (d) 7.5 L min⁻¹
4. Ultrafiltration of blood takes place in the <span class="marks">[1]</span>
   (a) proximal convoluted tubule (b) glomerulus and Bowman's capsule (c) loop of Henle (d) collecting duct
5. The resting membrane potential of a neuron is about <span class="marks">[1]</span>
   (a) +35 mV (b) −55 mV (c) −70 mV (d) −90 mV
6. The blind spot of the retina contains <span class="marks">[1]</span>
   (a) only rods (b) only cones (c) both rods and cones (d) neither rods nor cones
7. Hyposecretion of thyroxine in an infant causes <span class="marks">[1]</span>
   (a) myxoedema (b) cretinism (c) Graves' disease (d) tetany
8. In a normal 28-day cycle, fertilisation of the ovum usually occurs in the <span class="marks">[1]</span>
   (a) ovary (b) ampulla of the fallopian tube (c) uterus (d) cervix

::: note Answers to Group A
**1.** (b) — pepsin is the only enzyme of the strongly acidic gastric juice.
**2.** (d) — residual volume never leaves the lungs, so no spirometer can collect it.
**3.** (c) — $80 \times 75 = 6000$ ml min⁻¹ = 6 L min⁻¹.
**4.** (b) — the pressure difference across the glomerular capillaries drives filtration into Bowman's capsule.
**5.** (c) — −70 mV inside relative to outside; −55 mV is the threshold, not the resting value.
**6.** (d) — the optic disc is where the optic nerve leaves, so it has no photoreceptors at all.
**7.** (b) — in the infant it stunts body and brain growth (cretinism); the adult form is myxoedema.
**8.** (b) — the wide ampulla of the oviduct, within about 24 hours of ovulation.
:::

**Group B — Short answer (4 marks each)**

1. Draw a labelled diagram of an intestinal villus and explain **three** ways in which it is adapted for absorption. <span class="marks">[4]</span>
2. Distinguish between breathing and respiration. Define tidal volume and vital capacity, giving their normal values in an adult. <span class="marks">[4]</span>
3. An athlete breathes 20 times a minute with a tidal volume of 600 ml. The anatomical dead space is 150 ml. Calculate (i) the pulmonary ventilation and (ii) the alveolar ventilation, both in litres per minute. <span class="marks">[4]</span>
4. Describe the events of one cardiac cycle and give the duration of each of its three phases. <span class="marks">[4]</span>
5. In a patient the renal plasma flow is 600 ml min⁻¹ and the GFR is 120 ml min⁻¹. Calculate the filtration fraction. If 99 % of the filtrate is reabsorbed, what volume of urine is formed in 24 hours? <span class="marks">[4]</span>
6. What is a reflex action? Draw a labelled diagram of the reflex arc of the knee-jerk reflex. <span class="marks">[4]</span>
7. Two points on a nerve 12 cm apart are stimulated in turn; the muscle responds after 1.0 ms and 2.0 ms respectively. Calculate the conduction velocity in m s⁻¹ and state, with a reason, whether the fibre is myelinated. <span class="marks">[4]</span>
8. Name the disorders caused by the hyper- and hyposecretion of thyroxine and of growth hormone, and give one sign of each. <span class="marks">[4]</span>

::: note Answers to Group B
**1.** Diagram as in Figure 3. Adaptations: (i) each villus is 0.5–1 mm long and covered in microvilli, giving a brush border that raises the absorptive area to about 250 m²; (ii) the epithelium is one cell thick, so the diffusion path is very short; (iii) a dense blood capillary network carries glucose and amino acids away while a central **lacteal** carries fats, so the concentration gradient is never allowed to fall.

**2.** *Breathing* is the mechanical movement of air in and out of the lungs; *respiration* is the enzyme-controlled oxidation of food inside the cell to release ATP. Breathing is physical, involves no enzymes and happens in the lungs; respiration is chemical, needs enzymes and happens in every cell.
**Tidal volume** = volume of air breathed in or out in one quiet breath ≈ **500 ml**.
**Vital capacity** = maximum volume that can be expelled after the deepest possible inspiration = IRV + TV + ERV ≈ **4500 ml** (about 3500 ml in women).

**3.** (i) Pulmonary ventilation $= \text{TV} \times \text{rate} = 600 \times 20 = 12\,000$ ml min⁻¹ = **12 L min⁻¹**.
(ii) Only $600 - 150 = 450$ ml of each breath reaches the alveoli, so
alveolar ventilation $= 450 \times 20 = 9000$ ml min⁻¹ = **9 L min⁻¹**.
The 3 L min⁻¹ difference is air that merely fills the conducting airways and takes no part in gas exchange.

**4.** One cycle lasts **0.8 s** at 75 beats per minute.
*Atrial systole* (0.1 s): atria contract, pushing the last 30 % of blood through the open AV valves into the ventricles.
*Ventricular systole* (0.3 s): ventricles contract, AV valves shut (**first sound, "lubb"**), pressure rises isovolumetrically until the semilunar valves open and about 70 ml is ejected into the aorta and pulmonary trunk.
*Joint diastole* (0.4 s): ventricles relax, semilunar valves shut (**second sound, "dupp"**), AV valves open and the chambers refill passively.

**5.** Filtration fraction $= \dfrac{\text{GFR}}{\text{RPF}} \times 100 = \dfrac{120}{600} \times 100 = \mathbf{20\,\%}$.
Filtrate in 24 h $= 120 \times 60 \times 24 = 172\,800$ ml = 172.8 L.
Urine $= 1\,\%$ of this $= 0.01 \times 172.8 = \mathbf{1.73\ L\ day^{-1}}$, which is in the normal range of 1–1.5 L.

**6.** A **reflex action** is an immediate, involuntary, stereotyped response to a stimulus, carried out over a fixed nerve pathway without waiting for the brain's decision. Diagram as in Figure 15: stretch receptor in the quadriceps tendon → sensory (afferent) neuron → dorsal root ganglion → spinal cord grey matter → motor (efferent) neuron through the ventral root → quadriceps muscle (effector), which contracts and extends the leg. The knee-jerk is *monosynaptic* — there is no relay neuron.

**7.** The extra 12 cm of nerve added 1.0 ms to the latency, so
$$ v = \frac{\Delta s}{\Delta t} = \frac{0.12\ \text{m}}{1.0 \times 10^{-3}\ \text{s}} = \mathbf{120\ m\ s^{-1}} $$
This is far above the 0.5–2 m s⁻¹ of unmyelinated fibres, so the fibre **is myelinated**: the impulse jumps from node to node (saltatory conduction). Taking the difference between two stimulation points cancels out the synaptic and muscle delay, which is why two points are used rather than one.

**8.** *Thyroxine* — hypersecretion: **Graves' disease (exophthalmic goitre)**, sign = protruding eyeballs with rapid pulse and weight loss; hyposecretion: **myxoedema** in the adult, sign = puffy dry skin and low BMR, or **cretinism** in the infant, sign = stunted growth with mental retardation.
*Growth hormone* — hypersecretion before the epiphyses close: **gigantism**, sign = abnormal height; after they close: **acromegaly**, sign = enlarged jaw, hands and feet; hyposecretion in childhood: **pituitary dwarfism**, sign = very short stature with normal body proportions and normal intelligence.
:::

**Group C — Long answer (8 marks each)**

1. Draw a labelled diagram of the human heart in longitudinal section and describe the course of blood through the double circulation. A person has a stroke volume of 75 ml and a heart rate of 80 beats per minute; calculate the cardiac output, and find the cardiac reserve if the maximum output during exercise is 25 L min⁻¹. <span class="marks">[8]</span>
2. Describe the structure of a nephron with a labelled diagram and explain the three steps of urine formation. Why is glucose absent from the urine of a healthy person but present in an untreated diabetic? <span class="marks">[8]</span>
3. Describe the structure of a myelinated neuron. With the help of a graph of membrane potential against time, explain the origin and conduction of a nerve impulse, naming the value of the resting potential, the threshold and the peak. <span class="marks">[8]</span>
4. Describe the menstrual cycle of a human female under the headings *menstrual*, *proliferative*, *ovulatory* and *secretory* phases, and explain the hormonal control of each. What happens to the corpus luteum if fertilisation occurs? <span class="marks">[8]</span>

::: note Answers to Group C
**1.** Diagram as in Figures 6 and 7. *Structure:* four chambers — two thin-walled atria and two thick-walled ventricles, the left ventricle wall being about three times thicker because it pumps to the whole body. The right atrium and ventricle are separated by the **tricuspid valve**, the left pair by the **bicuspid (mitral) valve**; both are anchored by chordae tendineae to papillary muscles so they cannot turn inside out. **Semilunar valves** guard the openings of the pulmonary artery and the aorta. The interventricular septum prevents mixing.
*Double circulation:* blood passes through the heart **twice** in one complete round.
**Pulmonary circuit:** right atrium → tricuspid valve → right ventricle → pulmonary semilunar valve → pulmonary artery → lungs (CO₂ out, O₂ in) → pulmonary veins → left atrium.
**Systemic circuit:** left atrium → bicuspid valve → left ventricle → aortic semilunar valve → aorta → body tissues → venae cavae → right atrium.
The advantage is that oxygenated and deoxygenated blood never mix and full pressure can be delivered to the body without damaging the delicate lung capillaries.
*Calculation:* $\text{CO} = \text{SV} \times \text{HR} = 75 \times 80 = 6000$ ml min⁻¹ = **6 L min⁻¹**.
Cardiac reserve $= 25 - 6 = \mathbf{19\ L\ min^{-1}}$, i.e. the heart can raise its output roughly four-fold during exercise.

**2.** Diagram as in Figure 11. A nephron is the structural and functional unit of the kidney; there are about **1 million in each kidney**. It consists of a **Malpighian body** (glomerulus + Bowman's capsule) in the cortex, followed by the **proximal convoluted tubule**, the **loop of Henle** that dips into the medulla, the **distal convoluted tubule**, and the **collecting duct**.
*(i) Ultrafiltration.* Blood enters the glomerulus through a wide afferent arteriole and leaves by a narrower efferent one, so hydrostatic pressure is high. Net filtration pressure $= 55 - (15 + 30) = 10$ mmHg drives water and all small solutes into the capsule; blood cells and plasma proteins are held back. GFR = **125 ml min⁻¹ = 180 L day⁻¹**.
*(ii) Selective reabsorption.* The PCT returns 70–80 % of the filtrate — all the glucose and amino acids by active transport, Na⁺ actively and water osmotically. The loop of Henle builds the medullary salt gradient (300 → 1200 mOsm L⁻¹) by counter-current multiplication, and the DCT and collecting duct reabsorb the last water under **ADH**.
*(iii) Tubular secretion.* H⁺, K⁺, ammonia, creatinine and drugs are actively added from the blood into the DCT, which also regulates blood pH.
More than 99 % of the 180 L is reabsorbed, leaving 1–1.5 L of urine.
*Glucose:* in a healthy person the PCT carriers reabsorb all the filtered glucose, so none remains. In an untreated diabetic there is too little insulin, so blood glucose rises above the **renal threshold of 180 mg per 100 ml**; the carriers are saturated and the excess glucose passes on into the urine (glycosuria), dragging water with it osmotically and causing polyuria.

**3.** Diagram as in Figures 12 and 13. *Structure:* a **cyton (cell body)** containing the nucleus and Nissl granules; many short branched **dendrites** that receive impulses; and one long **axon** that carries the impulse away. The axon is wrapped in a fatty **myelin sheath** laid down by Schwann cells, interrupted every 1–2 mm at the **nodes of Ranvier**; it ends in synaptic knobs holding neurotransmitter vesicles.
*Resting state:* the Na⁺–K⁺ pump throws 3 Na⁺ out for every 2 K⁺ in, and the membrane leaks K⁺ outward, leaving the inside at **−70 mV** — polarised.
*Depolarisation:* a stimulus that brings the membrane to the **threshold of −55 mV** opens voltage-gated Na⁺ channels; Na⁺ floods in and the potential shoots up to about **+35 mV**. Below threshold nothing happens at all — the **all-or-none law**.
*Repolarisation:* Na⁺ channels close, K⁺ channels open and K⁺ leaves, restoring the negative inside, usually overshooting to about −80 mV (hyperpolarisation) before the pump restores the resting value.
*Refractory period:* for about 1 ms the membrane cannot be re-excited, which fixes the maximum firing rate and keeps the impulse travelling one way only.
*Conduction:* the local current from an active point depolarises the next point to threshold, so the impulse regenerates itself along the fibre without losing strength. In myelinated fibres only the nodes can depolarise, so the impulse **jumps** from node to node — **saltatory conduction**, up to 100–120 m s⁻¹ against 0.5–2 m s⁻¹ in unmyelinated fibres.

**4.** Graph as in Figure 21. The cycle averages 28 days, counted from the first day of bleeding.
*Menstrual phase (days 1–5).* The corpus luteum of the previous cycle has degenerated, so oestrogen and progesterone fall sharply. The endometrium can no longer be maintained; it breaks down and is shed with 50–80 ml of blood.
*Proliferative / follicular phase (days 6–13).* **FSH** from the anterior pituitary ripens one Graafian follicle, which secretes **oestrogen**. Oestrogen repairs and thickens the endometrium and restores its glands and blood vessels.
*Ovulatory phase (day 14).* The peak of oestrogen acts by **positive feedback** on the pituitary to produce a sudden **LH surge**. The follicle ruptures and the secondary oocyte is released into the fallopian tube.
*Secretory / luteal phase (days 15–28).* Under LH the ruptured follicle becomes the **corpus luteum**, which secretes **progesterone** (with some oestrogen). Progesterone makes the endometrium thick, soft, glandular and richly supplied with blood — ready for implantation — and inhibits FSH and LH so no new follicle develops.
*If fertilisation occurs*, the implanted embryo secretes **hCG**, which keeps the corpus luteum alive for about three months. Progesterone therefore stays high, the endometrium is not shed, menstruation stops and the pregnancy is maintained until the placenta takes over hormone production. If fertilisation does not occur, the corpus luteum degenerates into the **corpus albicans** around day 26, hormone levels collapse, and the next menstrual phase begins.
:::
