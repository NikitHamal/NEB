---
subject: Biology
grade: 11
unit: 3
title: Introductory Microbiology
hours: 5
area: Botany
---

Microbiology is the study of organisms too small to see with the naked eye. Two
groups dominate this unit: the **bacteria** of kingdom Monera, which are true
cells but have no nucleus, and the **viruses**, which are not cells at all. They
matter out of all proportion to their size — they fix the nitrogen in a lentil
field in Bara, set curd in a Kathmandu kitchen, rot the jute in a Jhapa retting
pit, and cause cholera, typhoid and COVID-19. The unit ends with what happens
when we deliberately re-engineer them: biotechnology.

::: key What the examiner asks from this unit
Three items recur almost every year: a **labelled diagram** of a bacterial cell
or of a bacteriophage; a **difference table** (Gram-positive vs Gram-negative,
bacteria vs virus, virus living vs non-living); and a **list-with-examples**
answer on economic importance or on applications of biotechnology. Learn the
scientific names — an unnamed example earns no mark.
:::

## 3.1 Monera

Monera is one of the five kingdoms of Whittaker's 1969 classification and holds
**all prokaryotes** — organisms whose cells have no nuclear envelope and no
membrane-bound organelles. In the modern three-domain scheme the kingdom splits
into two domains, Archaea and Bacteria, while all other life forms one domain,
Eukarya.

::: definition Monera
Monera is the kingdom of unicellular, prokaryotic organisms whose genetic
material is a single naked circular DNA molecule lying free in the cytoplasm,
whose cell wall (when present) contains peptidoglycan, and whose ribosomes are
of the 70S type.
:::

### General characters

- Unicellular and prokaryotic; size usually **0.2–2 μm** wide and 1–10 μm long.
  *Mycoplasma* (0.1–0.3 μm) is the smallest known living cell.
- No nuclear membrane, nucleolus, mitochondrion, plastid, ER, Golgi body,
  lysosome or true vacuole.
- Genetic material: one circular, double-stranded DNA molecule (the **nucleoid**)
  with no histone proteins, often plus small circular **plasmids**.
- Ribosomes are **70S** (a 50S and a 30S subunit).
- Cell wall of **peptidoglycan** (murein) — a mesh of N-acetylglucosamine and
  N-acetylmuramic acid chains cross-linked by short peptides.
- Reproduction is asexual by **binary fission**; true meiosis and gametes are
  absent, but DNA can be exchanged by transformation, conjugation and
  transduction.
- They are the most widely distributed organisms on Earth — in soil, air, water,
  hot springs, snow, and inside other organisms.

### Shape and arrangement

Bacteria are classified into four basic shapes. Because the daughter cells often
stay stuck together after fission, each shape gives a set of characteristic
**arrangements**, and the arrangement is part of the name.

```figure caption="Basic shapes of bacteria (top row) and the arrangements produced when daughter cells stay together after binary fission."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.0, 3.4))

BLUE = '#cfe3f3'; GREEN = '#d8ead8'; SAND = '#f6ecd8'

def coc(x, y, r=0.30, fc=BLUE):
    ax.add_patch(Circle((x, y), r, fc=fc, ec=INK, lw=0.85, zorder=3))

def rod(x, y, w=0.95, h=0.40, fc=GREEN):
    ax.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h,
                 boxstyle=f'round,pad=0,rounding_size={h/2:.3f}',
                 fc=fc, ec=INK, lw=0.85, zorder=3))

def title(x, y, s):
    ax.text(x, y, s, fontsize=6.0, ha='center', va='top', color=INK)

# ---- row 1 : the four basic shapes ----
y1 = 9.4
coc(1.3, y1, 0.36)
title(1.3, y1-0.75, 'coccus\n(spherical)')
rod(4.0, y1, w=1.05, h=0.44)
title(4.0, y1-0.75, 'bacillus\n(rod)')
t = np.linspace(-0.35, np.pi+0.35, 150)
ax.plot(6.7 + 0.55*np.cos(t), y1 + 0.55*np.sin(t) - 0.12, color='#b8860b', lw=3.4,
        solid_capstyle='round', zorder=3)
title(6.7, y1-0.75, 'vibrio\n(comma)')
s = np.linspace(0, 1, 220)
ax.plot(8.6 + 1.5*s, y1 + 0.45*np.sin(2*np.pi*1.5*s), color='#6a5acd', lw=3.0,
        solid_capstyle='round', zorder=3)
title(9.35, y1-0.75, 'spirillum\n(rigid spiral)')
ax.plot(11.5 + 1.7*s, y1 + 0.36*np.sin(2*np.pi*3.2*s), color='#d9534f', lw=2.2,
        solid_capstyle='round', zorder=3)
title(12.35, y1-0.75, 'spirochaete\n(flexible spiral)')

# ---- row 2 : arrangements of cocci ----
y2 = 5.9
coc(0.95, y2); coc(1.62, y2)
title(1.28, y2-0.95, 'diplococcus')
for k in range(4):
    coc(3.55 + 0.62*k, y2)
title(4.48, y2-0.95, 'streptococcus')
for dx, dy in [(0,0),(0.52,0.24),(0.27,-0.46),(0.75,-0.32),(-0.20,-0.42),(0.48,0.68)]:
    coc(7.30+dx, y2+dy, 0.27)
title(7.60, y2-1.20, 'staphylococcus')
for dx in (0, 0.58):
    for dy in (0, 0.58):
        coc(9.95+dx, y2-0.29+dy, 0.28)
title(10.24, y2-1.20, 'tetrad')
for dx in (0, 0.56):
    for dy in (0, 0.56):
        coc(12.05+dx+0.22, y2-0.16+dy, 0.26, fc=SAND)
for dx in (0, 0.56):
    for dy in (0, 0.56):
        coc(12.05+dx, y2-0.38+dy, 0.26)
title(12.45, y2-1.20, 'sarcina\n(packet of 8)')

# ---- row 3 : arrangements of bacilli ----
y3 = 2.2
rod(1.28, y3+0.30, w=1.05, h=0.34); rod(1.28, y3-0.30, w=1.05, h=0.34)
title(1.28, y3-0.95, 'diplobacillus')
for k in range(4):
    rod(4.48, y3+0.72-0.48*k, w=1.20, h=0.32)
title(4.48, y3-1.20, 'streptobacillus')
ax.add_patch(FancyBboxPatch((7.60, y3-0.17), 5.20, 0.34,
             boxstyle='round,pad=0,rounding_size=0.17', fc=SAND, ec=INK, lw=0.85))
for xx in np.arange(8.25, 12.8, 0.68):
    ax.plot([xx, xx], [y3-0.17, y3+0.17], color=MUTED, lw=0.7)
title(10.20, y3-0.45, 'filamentous trichome (e.g. Oscillatoria)')

ax.text(0.1, 11.1, 'The arrangement is part of the name:   diplo- = pair,   strepto- = chain,   staphylo- = cluster',
        fontsize=6.2, ha='left', va='center', color=MUTED)
ax.set_xlim(-0.1, 13.6); ax.set_ylim(0.3, 11.6)
ax.set_aspect('equal'); ax.axis('off')
```
### Structure of a bacterial cell

```figure caption="Ultrastructure of a rod-shaped bacterium. Compare it with the eukaryotic cell of Unit 1: there is no nuclear envelope and no membrane-bound organelle of any kind."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Ellipse, Arc
fig, ax = plt.subplots(figsize=(5.0, 3.2))

for inset, fc, ec in [(0.00, '#e8eef6', MUTED), (0.32, '#f6ecd8', INK), (0.56, '#ffffff', INK)]:
    h = 3.5 - 2*inset
    ax.add_patch(FancyBboxPatch((2.6+inset, 3.0+inset), 8.0-2*inset, h,
                 boxstyle=f'round,pad=0,rounding_size={h/2:.3f}',
                 fc=fc, ec=ec, lw=1.0, zorder=1))

# nucleoid : one tangled circular DNA molecule
t = np.linspace(0, 2*np.pi, 800)
ax.plot(7.0 + 1.55*np.sin(2*t) + 0.28*np.sin(5*t), 4.75 + 0.55*np.sin(3*t),
        color='#1d6fb8', lw=1.3, zorder=3)
ax.add_patch(Ellipse((9.75, 3.95), 0.80, 0.52, fc='none', ec='#d9534f', lw=1.3, zorder=3))
rng = np.random.default_rng(11)
ax.plot(rng.uniform(4.1, 10.1, 34), rng.uniform(3.6, 5.9, 34), 'o', ms=1.8,
        color=MUTED, zorder=2)
ax.add_patch(Arc((3.55, 4.75), 0.80, 1.30, theta1=-90, theta2=90, ec=INK, lw=1.0, zorder=4))
ax.add_patch(Circle((5.5, 3.78), 0.30, fc='#e5d4ef', ec=INK, lw=0.8, zorder=3))
xf = np.linspace(0, 2.15, 240)
ax.plot(0.30 + xf, 4.75 + 0.33*np.sin(2*np.pi*xf/0.92), color=INK, lw=1.2, zorder=3)
for xx in (7.9, 8.6, 9.3, 10.0):
    ax.plot([xx, xx], [6.54, 7.20], color=INK, lw=0.8)

def lab(s, xy, xytext, ha='center'):
    ax.annotate(s, xy=xy, xytext=xytext, fontsize=6.2, ha=ha, va='center', color=INK,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6, shrinkA=1, shrinkB=1))

lab('capsule (slime layer)', (4.6, 6.50), (2.6, 9.30))
lab('cell wall (peptidoglycan)', (6.1, 6.34), (6.9, 8.35))
lab('plasma membrane', (7.6, 6.10), (11.9, 9.30), ha='right')
lab('pili', (8.6, 7.20), (10.1, 8.15), ha='left')
lab('mesosome', (3.92, 5.35), (1.1, 7.10), ha='left')
lab('flagellum', (1.00, 4.92), (0.2, 6.15), ha='left')
lab('nucleoid: one circular,\nnaked DNA molecule', (7.1, 4.45), (5.7, 1.30))
lab('70S ribosomes', (4.7, 3.80), (2.0, 1.85))
lab('plasmid', (9.75, 3.70), (9.9, 1.85))
lab('storage granule', (5.5, 3.48), (8.6, 0.85), ha='center')
ax.text(0.2, 0.85, 'length ≈ 2 μm', fontsize=6.3, color=MUTED, ha='left')
ax.set_xlim(-0.1, 12.6); ax.set_ylim(0.2, 10.0)
ax.set_aspect('equal'); ax.axis('off')
```
| Part | Structure | Function |
|---|---|---|
| Capsule / slime layer | outer mucilaginous polysaccharide sheath | protection, sticking to surfaces, resists drying and phagocytosis |
| Cell wall | rigid peptidoglycan mesh, 10–80 nm thick | shape, protection, resists osmotic bursting |
| Plasma membrane | lipoprotein bilayer, no cholesterol | selective transport, respiratory enzymes |
| Mesosome | infolding of the plasma membrane | increases surface area for respiration; helps in DNA replication |
| Nucleoid | one naked circular double-stranded DNA | carries all essential genes |
| Plasmid | small extra circular DNA | carries resistance, fertility and toxin genes; used as a **vector** in gene cloning |
| Ribosome | 70S (50S + 30S), free in cytoplasm | protein synthesis |
| Flagellum | flagellin fibre with basal body and hook | locomotion |
| Pili (fimbriae) | short hollow protein tubes | attachment; sex pili transfer DNA in conjugation |
| Inclusions | glycogen, PHB, volutin, gas vacuoles | food and gas storage |

::: memory Flagellar arrangements
**A-M-A-L-C-P** — **A**trichous (none), **M**onotrichous (one, at one end),
**A**mphitrichous (one at each end), **L**ophotrichous (a tuft at one end),
**C**ephalotrichous (a tuft at both ends), **P**eritrichous (all over the body,
as in *Escherichia coli*).
:::

Gram's stain (Christian Gram, 1884) divides bacteria into two great groups, and
the difference is a difference of wall chemistry.

```figure caption="The two wall patterns revealed by Gram's stain, drawn in section with the outside of the cell upwards. The Gram-negative wall has little peptidoglycan but adds an outer membrane of lipopolysaccharide."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.0, 2.6))

def band(x, y, w, h, fc, ec=INK):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=0.8, zorder=3))

def right(x, y, s, color=INK):
    ax.annotate(s, xy=(x, y), xytext=(x + 0.35, y), fontsize=6.3,
                ha='left', va='center', color=color,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))

# ---------------- Gram-positive ----------------
band(0.6, 1.0, 2.2, 0.55, '#cfe3f3')
band(0.6, 1.55, 2.2, 2.55, '#8fc08f')
ax.text(1.7, 2.82, 'thick peptidoglycan\n20–80 nm\n+ teichoic acid',
        fontsize=6.3, ha='center', va='center', color=INK, zorder=4)
ax.text(1.7, 1.27, 'plasma membrane', fontsize=5.6, ha='center', va='center',
        color=INK, zorder=4)
ax.text(1.7, 5.45, 'GRAM-POSITIVE', fontsize=7.4, ha='center', color=INK)
ax.text(1.7, 4.50, 'crystal violet retained\n→  stains VIOLET',
        fontsize=6.3, ha='center', va='center', color='#6a5acd')
ax.text(1.7, 0.40, 'Bacillus subtilis,\nStaphylococcus aureus',
        fontsize=6.0, ha='center', color=MUTED, style='italic')

# ---------------- Gram-negative ----------------
band(6.0, 1.0, 2.2, 0.55, '#cfe3f3')
band(6.0, 1.55, 2.2, 0.45, '#8fc08f')
band(6.0, 2.00, 2.2, 0.75, '#ffffff')
band(6.0, 2.75, 2.2, 0.60, '#f2c9a0')
right(8.2, 1.27, 'plasma membrane')
right(8.2, 1.77, 'thin peptidoglycan, 2–7 nm')
right(8.2, 2.38, 'periplasmic space')
right(8.2, 3.05, 'outer membrane of\nlipopolysaccharide')
ax.text(7.1, 5.45, 'GRAM-NEGATIVE', fontsize=7.4, ha='center', color=INK)
ax.text(7.1, 4.50, 'decolourised, then counterstained\n→  stains PINK',
        fontsize=6.3, ha='center', va='center', color='#d9534f')
ax.text(7.1, 0.40, 'Escherichia coli,\nVibrio cholerae',
        fontsize=6.0, ha='center', color=MUTED, style='italic')

ax.annotate('', xy=(4.15, 4.15), xytext=(4.15, 1.0),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=0.9, mutation_scale=9))
ax.text(4.30, 2.6, 'outside\nof cell', fontsize=6.0, ha='left', va='center', color=INK)
ax.set_xlim(0.0, 12.9); ax.set_ylim(-0.35, 5.9)
ax.axis('off')
```

| Feature | Gram-positive | Gram-negative |
|---|---|---|
| Colour after staining | violet / purple | pink / red |
| Peptidoglycan | thick, 20–80 nm, 40–90 % of wall | thin, 2–7 nm, 5–20 % of wall |
| Teichoic acid | present | absent |
| Outer membrane, lipopolysaccharide | absent | present |
| Periplasmic space | absent or very narrow | well developed |
| Sensitivity to penicillin | high | comparatively low |
| Examples | *Bacillus subtilis*, *Staphylococcus aureus*, *Clostridium tetani* | *Escherichia coli*, *Vibrio cholerae*, *Salmonella typhi*, *Rhizobium leguminosarum* |

### Nutrition

| Mode | Energy / carbon source | Examples |
|---|---|---|
| Photoautotrophic | sunlight; CO₂ fixed | cyanobacteria (*Nostoc*), purple sulphur bacteria (*Chromatium*), green sulphur bacteria (*Chlorobium*) |
| Chemoautotrophic | oxidation of inorganic substances | *Nitrosomonas* (NH₃ → NO₂⁻), *Nitrobacter* (NO₂⁻ → NO₃⁻), *Thiobacillus* (S → SO₄²⁻) |
| Saprophytic | dead organic matter | *Bacillus*, most soil bacteria — the chief decomposers |
| Parasitic | living host, causes harm | *Mycobacterium tuberculosis*, *Xanthomonas oryzae* |
| Symbiotic | living host, mutual benefit | *Rhizobium leguminosarum* in the root nodules of legumes |

### Reproduction

1. **Binary fission** (amitosis) is the normal method. The DNA replicates, the
   cell elongates, a transverse septum grows inwards and the cell splits into two
   identical daughter cells. Under ideal conditions *E. coli* divides every
   **20 minutes**.
2. **Endospore formation** is *not* reproduction — it is survival. *Bacillus* and
   *Clostridium* lay down a thick, almost dehydrated spore inside the cell that
   can survive boiling, drought and disinfectants for years, then germinate into
   a single vegetative cell.
3. **Genetic recombination** substitutes for sex. There are three routes:
   **transformation** — naked DNA is taken up from the medium (Griffith, 1928);
   **conjugation** — DNA passes through a sex pilus from a donor to a recipient
   (Lederberg and Tatum, 1946); **transduction** — DNA is carried from one cell to
   another by a bacteriophage (Zinder and Lederberg, 1952).

::: caution Binary fission is not mitosis
There is no spindle, no centromere and no nuclear envelope to break down, so
binary fission is **amitosis**. Writing "prophase" or "metaphase" in a binary
fission answer loses the mark.
:::

### The growth of a bacterial population

Because one cell becomes two at each division, a bacterial population grows
**geometrically**. If $N_0$ cells grow for time $t$ with a generation time $g$,
the number of generations is $n = t/g$ and

$$ N = N_0 \times 2^{n}, \qquad n = \frac{\log N - \log N_0}{\log 2} $$

::: example Worked example 3.1
**Problem.** A culture starts with $1 \times 10^{3}$ cells of *Escherichia coli*
whose generation time is 20 minutes. How many cells are present after 3 hours of
exponential growth?

**Solution.** Time available $t = 3 \times 60 = 180$ minutes, so

$$ n = \frac{t}{g} = \frac{180}{20} = 9 \ \text{generations} $$

$$ N = N_0 \times 2^{n} = 1\times10^{3} \times 2^{9} = 1\times10^{3} \times 512 = 5.12 \times 10^{5}\ \text{cells} $$
:::

::: example Worked example 3.2
**Problem.** A bacterial population rises from $5 \times 10^{3}$ to
$3.2 \times 10^{5}$ cells in 2 hours. Find the number of generations and the
generation time.

**Solution.** The growth factor is

$$ \frac{N}{N_0} = \frac{3.2\times10^{5}}{5\times10^{3}} = 64 = 2^{6} $$

so $n = 6$ generations. Then

$$ g = \frac{t}{n} = \frac{120\ \text{min}}{6} = 20\ \text{minutes} $$
:::

::: example Worked example 3.3
**Problem.** A milk sample is diluted $10^{-5}$ times. $0.1\ \text{mL}$ of the
dilution is spread on nutrient agar and gives 148 colonies. Calculate the number
of colony-forming units (CFU) per millilitre of the original milk.

**Solution.** Each colony arose from one cell, so

$$ \text{CFU mL}^{-1} = \frac{\text{colonies}}{\text{volume plated} \times \text{dilution}}
 = \frac{148}{0.1 \times 10^{-5}} $$

$$ = 148 \times 10^{6} = 1.48 \times 10^{8}\ \text{CFU mL}^{-1} $$

The milk is heavily contaminated: the acceptable limit for pasteurised milk is
about $10^{5}\ \text{CFU mL}^{-1}$.
:::

### Classification of Monera

| Group | Wall | Distinguishing feature | Examples |
|---|---|---|---|
| Archaebacteria | no peptidoglycan; branched lipids with ether links | live in extreme habitats; oldest known prokaryotes | *Methanobacterium* (methanogen, in biogas and in cattle rumen), *Halobacterium* (salt lakes), *Sulfolobus* (hot acid springs) |
| Eubacteria — true bacteria | peptidoglycan | the ordinary heterotrophic and chemoautotrophic bacteria | *Escherichia coli*, *Bacillus*, *Rhizobium*, *Vibrio cholerae* |
| Eubacteria — cyanobacteria | peptidoglycan | oxygen-releasing photosynthesis with chlorophyll *a* | *Nostoc*, *Anabaena*, *Oscillatoria*, *Spirulina* |
| Mycoplasma (PPLO) | **no cell wall** | smallest living cells, pleomorphic; "jokers of the plant kingdom" | *Mycoplasma gallisepticum*; cause of little leaf of brinjal |

**Cyanobacteria** (blue-green algae) deserve special mention. They are
prokaryotic but photosynthesise like plants, using chlorophyll *a* together with
the blue pigment c-phycocyanin and the red c-phycoerythrin. Filamentous forms
such as *Nostoc* and *Anabaena* have thick-walled colourless cells called
**heterocysts** in which atmospheric nitrogen is fixed; this is why *Anabaena
azollae*, living inside the water fern *Azolla*, is used as a biofertiliser in
rice fields. When nutrient-rich water warms up, cyanobacteria multiply into a
foul-smelling **water bloom** that deoxygenates the water and kills fish.

### Economic importance of bacteria

| Useful role | Organism | Product or effect |
|---|---|---|
| Nitrogen fixation | *Rhizobium leguminosarum*, *Azotobacter*, *Anabaena* | converts N₂ into ammonia; raises soil fertility |
| Nitrification | *Nitrosomonas*, *Nitrobacter* | ammonia → nitrite → nitrate, the form roots absorb |
| Dairy | *Lactobacillus*, *Streptococcus lactis* | curd, cheese, *dahi* and *mohi* |
| Vinegar | *Acetobacter aceti* | ethanol → acetic acid |
| Antibiotics | *Streptomyces griseus*, *S. venezuelae*, *Bacillus subtilis* | streptomycin, chloramphenicol, subtilin |
| Retting | *Clostridium*, *Pseudomonas* | frees jute, flax and hemp fibres from the stem |
| Biogas | *Methanobacterium* | methane from cow dung — over 400,000 domestic plants in Nepal |
| Sewage treatment | mixed saprophytes | breaks organic waste into harmless minerals |
| Vitamins, amino acids | *Pseudomonas denitrificans*, *Corynebacterium glutamicum* | vitamin B₁₂, glutamic acid |

| Harmful effect | Disease | Causal bacterium |
|---|---|---|
| Human | cholera | *Vibrio cholerae* |
| Human | typhoid | *Salmonella typhi* |
| Human | tuberculosis | *Mycobacterium tuberculosis* |
| Human | tetanus | *Clostridium tetani* |
| Plant | bacterial blight of rice | *Xanthomonas oryzae* |
| Plant | citrus canker | *Xanthomonas citri* |
| Plant | crown gall | *Agrobacterium tumefaciens* |
| Other | food spoilage, denitrification, milk souring | many saprophytes |

## 3.2 Virus

The word *virus* is Latin for poison. In 1892 the Russian scientist **D. J.
Iwanowski** showed that the sap of a tobacco plant with mosaic disease stayed
infectious after being passed through a filter fine enough to stop all bacteria.
In 1898 **M. W. Beijerinck** named the agent *contagium vivum fluidum* — a living
infectious fluid. In 1935 **W. M. Stanley** crystallised tobacco mosaic virus and
proved it was nucleoprotein, for which he received the Nobel Prize in 1946.

::: definition Virus
A virus is an ultramicroscopic, obligate intracellular parasite consisting of a
single kind of nucleic acid (DNA **or** RNA, never both) enclosed in a protein
coat called a capsid; it has no cytoplasm, no ribosomes and no metabolism of its
own, and can multiply only inside a living host cell.
:::

### Living and non-living characters

| Living characters | Non-living characters |
|---|---|
| Contain nucleic acid, the genetic material | Can be crystallised and stored like a chemical |
| Multiply, giving thousands of copies | No respiration, no growth, no excretion |
| Show heredity and mutation | No cytoplasm, membrane, ribosome or enzyme system of their own |
| Are host- and tissue-specific | Inert outside the host — cannot multiply in a culture medium |
| Respond to heat, formalin and radiation | Obey the law of mass action, like a chemical |

Viruses are therefore said to be **on the borderline between the living and the
non-living**: living inside the host, a chemical outside it.

### Structure

```figure caption="Structure of the T4 bacteriophage (a tailed DNA virus of *E. coli*) and of tobacco mosaic virus (a helical RNA virus). Sizes are approximate."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Circle, FancyBboxPatch, Ellipse
fig, (axA, axB) = plt.subplots(1, 2, figsize=(5.2, 3.2),
                               gridspec_kw=dict(width_ratios=[1.0, 1.05], wspace=0.05))

# ============ (a) T4 bacteriophage ============
hx, hy = 5.0, 12.4
a = np.radians(np.arange(90, 450, 60))
head = np.c_[hx + 1.85*np.cos(a), hy + 2.30*np.sin(a)]
axA.add_patch(Polygon(head, closed=True, fc='#cfe3f3', ec=INK, lw=1.1, zorder=2))
t = np.linspace(0, 6*np.pi, 400)
axA.plot(hx + 0.95*np.sin(t*0.9)*np.cos(t*0.25), hy + 1.55*np.sin(t*0.31),
         color='#1d6fb8', lw=1.0, zorder=3)
axA.add_patch(Rectangle((hx-1.05, hy-2.85), 2.10, 0.52, fc='#f6ecd8', ec=INK, lw=1.0, zorder=3))
axA.add_patch(Rectangle((hx-0.80, hy-7.45), 1.60, 4.60, fc='#d8ead8', ec=INK, lw=1.0, zorder=2))
for k in range(1, 9):
    yy = hy - 2.85 - 0.51*k
    axA.plot([hx-0.80, hx+0.80], [yy, yy], color=MUTED, lw=0.6, zorder=3)
axA.add_patch(Rectangle((hx-0.22, hy-7.45), 0.44, 4.60, fc='#ffffff', ec=INK, lw=0.8, zorder=4))
axA.add_patch(Rectangle((hx-1.30, hy-8.05), 2.60, 0.60, fc='#f2c9a0', ec=INK, lw=1.0, zorder=3))
for dx in (-1.05, -0.35, 0.35, 1.05):
    axA.plot([hx+dx, hx+dx*1.15], [hy-8.05, hy-8.70], color=INK, lw=0.9, zorder=3)
for sgn in (-1, 1):
    xf = np.array([hx+sgn*1.30, hx+sgn*2.25, hx+sgn*2.55])
    yf = np.array([hy-7.85, hy-8.60, hy-9.70])
    axA.plot(xf, yf, color=INK, lw=1.0, zorder=3)

def labA(s, xy, xytext, ha='left'):
    axA.annotate(s, xy=xy, xytext=xytext, fontsize=6.0, ha=ha, va='center', color=INK,
                 arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6, shrinkA=1, shrinkB=1))

labA('head (capsid):\nicosahedral,\n95 × 65 nm', (hx+1.55, hy+1.30), (hx+2.25, hy+1.85))
labA('double-stranded DNA', (hx+0.60, hy+0.10), (hx+2.25, hy-0.35))
labA('collar', (hx+1.05, hy-2.60), (hx+2.25, hy-2.40))
labA('contractile tail sheath', (hx+0.80, hy-4.60), (hx+2.25, hy-4.40))
labA('hollow tail core', (hx+0.22, hy-6.30), (hx+2.25, hy-6.30))
labA('base plate', (hx+1.30, hy-7.75), (hx+2.25, hy-7.95))
labA('tail fibres and spikes\n(attach to host wall)', (hx+2.40, hy-9.35), (hx+1.10, hy-10.60))
axA.text(0.2, 17.0, '(a)  T4 bacteriophage', fontsize=6.8, color=INK)
axA.text(0.2, 0.9, 'total length ≈ 200 nm', fontsize=6.2, color=MUTED)
axA.set_xlim(0.0, 10.4); axA.set_ylim(0.2, 17.6)
axA.set_aspect('equal'); axA.axis('off')

# ============ (b) Tobacco mosaic virus ============
cx = 4.6
for k in range(11):
    y0 = 2.6 + 1.02*k
    axB.add_patch(Ellipse((cx, y0), 5.6, 0.86, fc='#d8ead8', ec=INK, lw=0.8, zorder=2))
    for j in range(8):
        th = np.linspace(0, np.pi, 30)
        axB.plot(cx - 2.5 + 0.72*j + 0.26*np.cos(th), y0 + 0.30*np.sin(th),
                 color=MUTED, lw=0.5, zorder=3)
yy = np.linspace(2.4, 13.0, 500)
axB.plot(cx + 1.05*np.sin(2*np.pi*(yy-2.4)/2.05), yy, color='#d9534f', lw=1.4, zorder=5)
axB.add_patch(Ellipse((cx, 13.62), 5.6, 0.86, fc='#f6ecd8', ec=INK, lw=0.9, zorder=6))

def labB(s, xy, xytext, ha='left'):
    axB.annotate(s, xy=xy, xytext=xytext, fontsize=6.0, ha=ha, va='center', color=INK,
                 arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6, shrinkA=1, shrinkB=1))

labB('capsomeres: 2130 identical\nprotein subunits in a helix', (cx+2.55, 11.7), (cx-4.3, 15.2))
labB('single-stranded RNA,\n≈ 6400 nucleotides,\ncoiled inside the helix', (cx+0.95, 7.6), (cx+3.0, 7.2))
labB('16⅓ subunits per turn', (cx+2.35, 4.3), (cx+3.0, 3.7))
axB.annotate('', xy=(cx-3.35, 2.6), xytext=(cx-3.35, 13.62),
             arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=0.8, mutation_scale=6))
axB.text(cx-3.55, 8.1, '300 nm', fontsize=6.2, rotation=90, ha='right', va='center', color=INK)
axB.annotate('', xy=(cx-2.8, 1.55), xytext=(cx+2.8, 1.55),
             arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=0.8, mutation_scale=6))
axB.text(cx, 1.0, 'diameter 18 nm', fontsize=6.2, ha='center', color=INK)
axB.text(-3.3, 17.0, '(b)  tobacco mosaic virus', fontsize=6.8, color=INK)
axB.set_xlim(-3.4, 11.0); axB.set_ylim(0.2, 17.6)
axB.set_aspect('equal'); axB.axis('off')
```

Every virus has two essential parts. The **capsid** is the protein coat, built of
identical subunits called **capsomeres**; it protects the nucleic acid and decides
which host cell the virus can attach to. The **genome** is one molecule (or a few
pieces) of DNA or RNA, single- or double-stranded. Some animal viruses add an
outer **envelope** of host membrane carrying viral spikes — influenza virus, HIV
and SARS-CoV-2 are enveloped. Capsid plus genome is a **nucleocapsid**; one
complete infective particle is a **virion**.

Notice a pleasing piece of arithmetic in TMV: three RNA nucleotides are bound by
each protein subunit, so $6400/3 \approx 2133$ — very close to the 2130
capsomeres actually counted.

| Basis | Types | Examples |
|---|---|---|
| Host | plant viruses, animal viruses, bacteriophages, mycophages | TMV; rabies virus; T4 phage |
| Nucleic acid | dsDNA, ssDNA, dsRNA, ssRNA | T4 phage; φX174; wound tumour virus; TMV, HIV |
| Shape | rod (TMV), spherical/polyhedral (poliovirus), tadpole (phage), brick (variola), bullet (rabies) | — |
| Envelope | naked (TMV, poliovirus) or enveloped (influenza, HIV) | — |

::: caution DNA or RNA — never both
A virus carries **one** kind of nucleic acid. Most plant viruses are RNA viruses
and most bacteriophages are DNA viruses. Retroviruses such as HIV are RNA
viruses that copy their RNA into DNA using **reverse transcriptase**; this does
not make them "DNA and RNA viruses".
:::

### Multiplication — the lytic cycle

```figure caption="The lytic cycle of a bacteriophage. The dashed branch shows the lysogenic alternative, in which the phage DNA integrates into the host chromosome as a prophage and is copied silently for many generations."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.0, 3.4))

def box(xc, yc, w, h, s, fc, ec, fs=6.0):
    ax.add_patch(FancyBboxPatch((xc-w/2, yc-h/2), w, h,
                 boxstyle='round,pad=0,rounding_size=0.18',
                 fc=fc, ec=ec, lw=0.95, zorder=3))
    ax.text(xc, yc, s, fontsize=fs, ha='center', va='center', color=INK, zorder=4)

stages = [
 '1.  ADSORPTION — tail fibres attach to\nspecific receptors on the host cell wall',
 '2.  PENETRATION — sheath contracts, the core\npierces the wall, DNA is injected; coat stays outside',
 '3.  BIOSYNTHESIS — host DNA is hydrolysed;\nphage DNA and capsid proteins are made',
 '4.  MATURATION — parts self-assemble\ninto complete new virions',
 '5.  LYSIS — endolysin bursts the cell and\n100–200 phages are released',
]
XC, W, H = 5.6, 6.6, 1.35
ys = [8.7, 6.85, 5.0, 3.15, 1.3]
for s, y in zip(stages, ys):
    box(XC, y, W, H, s, '#eef3f8', ACCENT)
for y in ys[:-1]:
    ax.annotate('', xy=(XC, y-1.175+0.02), xytext=(XC, y-H/2-0.02),
                arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.3, mutation_scale=10))

# recycling path back to stage 1, routed clear of the boxes
ax.plot([XC-W/2, 1.15], [ys[-1], ys[-1]], color=ACCENT, lw=1.2, zorder=2)
ax.plot([1.15, 1.15], [ys[-1], ys[0]], color=ACCENT, lw=1.2, zorder=2)
ax.annotate('', xy=(XC-W/2, ys[0]), xytext=(1.15, ys[0]),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.2, mutation_scale=10))
ax.text(0.80, 5.0, 'released phages infect fresh cells', fontsize=5.9,
        rotation=90, ha='center', va='center', color=MUTED)

# lysogenic branch
box(12.2, 6.0, 4.8, 2.9,
    'LYSOGENIC CYCLE\n\nthe injected DNA instead\nintegrates into the host\nchromosome as a PROPHAGE\nand is copied silently with it;\nthe host cell is not killed',
    '#fdf3e6', '#b8860b', fs=6.0)
ax.annotate('', xy=(9.75, 6.6), xytext=(8.95, 6.85),
            arrowprops=dict(arrowstyle='-|>', color='#b8860b', lw=1.2,
                            ls=(0, (3, 2)), mutation_scale=10))
ax.annotate('', xy=(8.95, 5.0), xytext=(9.75, 4.9),
            arrowprops=dict(arrowstyle='-|>', color='#b8860b', lw=1.2,
                            ls=(0, (3, 2)), mutation_scale=10))
ax.text(12.2, 3.55, 'induction by UV light or chemicals\nreturns it to the lytic cycle',
        fontsize=5.9, ha='center', va='center', color='#b8860b')
ax.text(XC, 10.15, 'LYTIC CYCLE', fontsize=8.2, ha='center', color=INK)
ax.text(XC, 9.68, 'one complete cycle takes ≈ 25 min in E. coli at 37 °C',
        fontsize=6.0, ha='center', color=MUTED)
ax.set_xlim(0.2, 15.0); ax.set_ylim(0.3, 10.5)
ax.axis('off')
```
::: example Worked example 3.4
**Problem.** One T4 phage infects a single *E. coli* cell. Each lytic cycle takes
25 minutes and has a **burst size** of 200. Assuming every released phage at once
finds a fresh host, how many free phages exist after 75 minutes?

**Solution.** In 75 minutes there are $75/25 = 3$ complete cycles. Each phage
becomes 200, so

$$ N = 200^{3} = 8 \times 10^{6}\ \text{phages} $$

from a single starting particle — which is why a phage-infected culture clears
within an hour.
:::

Two even simpler infectious agents exist. A **viroid** (T. O. Diener, 1971) is a
short, naked circular RNA with *no protein coat* — potato spindle tuber viroid is
the type example. A **prion** (S. Prusiner) is an infectious *protein* with no
nucleic acid at all; prions cause scrapie in sheep, BSE ("mad cow disease") and
Creutzfeldt–Jakob disease in humans.

| Group | Disease | Virus |
|---|---|---|
| Plant | tobacco mosaic | TMV |
| Plant | bunchy top of banana | banana bunchy top virus |
| Plant | yellow vein mosaic of lady's finger | bhindi yellow vein mosaic virus |
| Human | poliomyelitis | poliovirus |
| Human | rabies | rabies (lyssa) virus |
| Human | AIDS | HIV, a retrovirus |
| Human | COVID-19 | SARS-CoV-2 |

## 3.3 Impacts of biotechnology in microbiology

::: definition Biotechnology
Biotechnology is the use of living organisms, their cells or their enzymes to
manufacture products and provide services useful to humans. Modern biotechnology
rests on **recombinant DNA technology** — transferring a chosen gene from one
organism into another so that the new host makes the desired product.
:::

Microorganisms are the ideal factories: they are small, they grow within hours on
cheap media, their genetics is simple, and a single plasmid can carry a foreign
gene into millions of cells. The key tools are:

- **Restriction endonucleases** — "molecular scissors" that cut DNA at a specific
  base sequence. *Eco*RI, from *E. coli*, leaves sticky ends.
- **DNA ligase** — the glue that seals the cut ends together.
- **Vectors** — carriers that take the gene into the host: plasmids (pBR322), the
  Ti plasmid of *Agrobacterium tumefaciens* for plants, and bacteriophage λ.
- **Host cells** — usually *Escherichia coli* or the yeast *Saccharomyces
  cerevisiae*.
- **Bioreactor (fermenter)** — a stirred, aerated, temperature-controlled vessel
  in which the engineered microbes are grown by the thousand litres.

::: memory The five steps of gene cloning
**I-C-I-T-S** — **I**solate the gene, **C**ut it out with a restriction enzyme,
**I**nsert it into a vector with ligase, **T**ransform the host cell, then
**S**elect the recombinants and scale up in a bioreactor.
:::

| Field | What microbial biotechnology delivers | Example |
|---|---|---|
| Medicine | human proteins made in bacteria | human insulin (Humulin, 1982) from *E. coli*; human growth hormone; interferon |
| Vaccines | safe subunit vaccines | hepatitis B vaccine made in yeast |
| Diagnostics | gene-based detection | PCR (K. Mullis, 1983) for tuberculosis and SARS-CoV-2; DNA fingerprinting |
| Agriculture | insect-resistant crops | *cry* genes from *Bacillus thuringiensis* in Bt cotton and Bt maize |
| Biofertiliser | living nitrogen fixers instead of urea | *Rhizobium* seed inoculum, *Azotobacter*, *Azolla*–*Anabaena* in paddy |
| Biopesticide | microbes that kill pests | *Bt* spore sprays; *Trichoderma* against soil fungi |
| Food | single-cell protein, fermented foods | *Spirulina* tablets; *gundruk*, *kinema*, curd |
| Energy | methane from waste | *Methanobacterium* in household biogas plants |
| Environment | bioremediation and bioleaching | *Pseudomonas putida* digests oil spills; *Thiobacillus ferrooxidans* extracts copper from low-grade ore |
| Industry | cheap enzymes | amylase and lipase in detergents; protease in leather tanning |

In Nepal the visible impacts are mainly agricultural and energy-related.
Government and NGO programmes have installed more than **400,000 household
biogas plants**, each replacing firewood with methane from cattle dung. The
Nepal Agricultural Research Council supplies *Rhizobium* inoculum for lentil,
chickpea and soybean; tissue-culture laboratories multiply disease-free banana,
potato and orchid plantlets; and the National Gene Bank at Khumaltar stores seed
of indigenous crop landraces.

Against these gains stand real concerns: the escape of genes from genetically
modified crops into wild relatives, the loss of local landraces when a single
engineered variety is planted everywhere, the possibility of engineered pathogens
being misused, patenting of genes taken from communities without their consent
(**biopiracy**), and the cost of the technology, which keeps it in the hands of a
few companies. Nepal regulates this work through its National Biosafety
Framework, based on the Cartagena Protocol on Biosafety.

::: tip Answering "impacts of biotechnology"
Marks are awarded for **named** examples paired with the **organism used**. Write
"human insulin produced in *Escherichia coli*", not "medicines are produced".
If the question says *impacts*, give both benefits and hazards — two or three of
each — or you forfeit half the marks.
:::

## Chapter summary

- Monera contains all prokaryotes: no nuclear envelope, no membrane-bound
  organelles, 70S ribosomes, a single naked circular DNA, and a peptidoglycan
  wall (absent in *Mycoplasma*, non-peptidoglycan in Archaebacteria).
- Bacterial shapes are coccus, bacillus, vibrio and spiral; the prefixes diplo-,
  strepto-, staphylo-, tetrad and sarcina name the arrangements.
- Gram-positive walls have thick peptidoglycan and teichoic acid and stain
  violet; Gram-negative walls have thin peptidoglycan plus an outer
  lipopolysaccharide membrane and stain pink.
- Reproduction is binary fission (amitosis); endospores are for survival, not
  reproduction; DNA is exchanged by transformation, conjugation and transduction.
- Population growth is geometric: $N = N_0 \times 2^{n}$ with $n = t/g$.
- A virus is a nucleoprotein particle — one kind of nucleic acid in a capsid of
  capsomeres — that is inert outside its host and multiplies only inside it,
  by the lytic or the lysogenic cycle.
- T4 bacteriophage: icosahedral head of dsDNA, collar, contractile sheath, hollow
  core, base plate, tail fibres. TMV: helical rod 300 × 18 nm, 2130 capsomeres,
  ssRNA.
- Microbial biotechnology uses restriction enzymes, ligase, plasmid vectors and
  *E. coli* hosts to make insulin, vaccines, Bt crops, biofertilisers, biogas and
  bioremediation agents — with biosafety and biopiracy as the chief concerns.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The ribosome of a bacterial cell is of the type <span class="marks">[1]</span>
   (a) 80S (b) 70S (c) 60S (d) 55S
2. Which structure allows a bacterium to transfer DNA during conjugation? <span class="marks">[1]</span>
   (a) flagellum (b) capsule (c) sex pilus (d) mesosome
3. Nitrogen fixation in *Nostoc* takes place in the <span class="marks">[1]</span>
   (a) akinete (b) heterocyst (c) hormogone (d) gas vacuole
4. Tobacco mosaic virus contains <span class="marks">[1]</span>
   (a) double-stranded DNA (b) single-stranded DNA (c) double-stranded RNA (d) single-stranded RNA
5. An infectious agent made only of protein, with no nucleic acid, is a <span class="marks">[1]</span>
   (a) viroid (b) prion (c) prophage (d) mycoplasma
6. The enzyme used as "molecular scissors" in gene cloning is <span class="marks">[1]</span>
   (a) DNA ligase (b) DNA polymerase (c) restriction endonuclease (d) reverse transcriptase

::: note Answers to Group A
**1.** (b) — prokaryotic ribosomes are 70S (50S + 30S); 80S is eukaryotic.
**2.** (c) — the F or sex pilus forms the conjugation tube.
**3.** (b) — the thick-walled colourless heterocyst holds the nitrogenase.
**4.** (d) — TMV has a single-stranded RNA genome of about 6400 nucleotides.
**5.** (b) — a prion is a proteinaceous infectious particle.
**6.** (c) — restriction endonucleases cut DNA at specific recognition sequences.
:::

**Group B — Short answer (4 marks each)**

1. Draw a labelled diagram of a bacterial cell and state the function of the
   mesosome and of the plasmid. <span class="marks">[4]</span>
2. Differentiate between Gram-positive and Gram-negative bacteria (any four
   points, with one example of each). <span class="marks">[4]</span>
3. A culture of *Escherichia coli* containing $2 \times 10^{4}$ cells is grown for
   2 hours at 37 °C, where its generation time is 20 minutes. Calculate the final
   number of cells, and state how many generations occurred. <span class="marks">[4]</span>
4. Why is a virus said to lie on the borderline between living and non-living?
   Give two characters of each kind. <span class="marks">[4]</span>

::: note Answers to Group B
**1.** Diagram must show capsule, cell wall, plasma membrane, nucleoid, plasmid,
70S ribosomes, mesosome, flagellum and pili. The **mesosome** is an infolding of
the plasma membrane that increases the surface area for respiratory enzymes and
assists DNA replication and cell-wall formation. The **plasmid** is extra
circular DNA carrying non-essential genes such as antibiotic resistance; it
replicates independently and is used as a vector in genetic engineering.

**3.** Number of generations $n = t/g = 120/20 = 6$. Then

$$ N = N_0 \times 2^{n} = 2\times10^{4} \times 2^{6} = 2\times10^{4} \times 64 = 1.28 \times 10^{6}\ \text{cells} $$

So six generations occur and the population reaches $1.28 \times 10^{6}$ cells.

**4.** Living: they possess nucleic acid and so show heredity and mutation, and
they multiply to give thousands of progeny inside a host. Non-living: they can be
crystallised and stored like a chemical, and they have no cytoplasm, no
respiration and no enzyme system of their own, so they cannot grow on a
nutrient medium.
:::

**Group C — Long answer (8 marks each)**

1. (a) Draw a well-labelled diagram of the T4 bacteriophage. <span class="marks">[4]</span>
   (b) Describe the lytic cycle of a bacteriophage, and explain how it differs
   from the lysogenic cycle. <span class="marks">[4]</span>
2. Describe the economic importance of bacteria under the headings agriculture,
   industry, medicine and disease, giving the scientific name of the organism in
   each case. <span class="marks">[8]</span>

::: note Answer outline to Group C question 1
(a) Labels required: icosahedral head containing double-stranded DNA, collar,
contractile tail sheath, hollow tail core, base plate, tail spikes and six long
tail fibres; total length about 200 nm.

(b) **Lytic cycle** — (i) *adsorption*: tail fibres bind specific receptors on
the wall of *E. coli*; (ii) *penetration*: the sheath contracts, the core pierces
the wall and the DNA is injected while the empty coat (ghost) stays outside;
(iii) *biosynthesis (eclipse)*: host DNA is hydrolysed and the host machinery is
diverted to make phage DNA and capsid proteins; (iv) *maturation*: parts assemble
into complete virions; (v) *lysis*: endolysin dissolves the wall and 100–200
phages are released in about 25 minutes. The host always dies.

In the **lysogenic cycle** the injected DNA instead integrates into the bacterial
chromosome as a **prophage** and is replicated silently with the host DNA for
many generations; the host survives, and only when induced by ultraviolet light
or chemicals does the prophage excise itself and enter the lytic cycle.
Bacteriophage λ is the standard example.
:::
