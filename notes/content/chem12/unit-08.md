---
subject: Chemistry
grade: 12
unit: 8
title: Haloalkanes
hours: 8
area: Organic Chemistry
---

Replace one hydrogen of an alkane by a halogen and the molecule stops being
inert. The halogen pulls electron density away from the carbon it is attached
to, leaving that carbon electron-poor and open to attack by anything carrying a
lone pair. That single polarised bond, C–X, is the doorway from hydrocarbons
into alcohols, amines, nitriles, ethers and almost everything else in the rest
of this book. Haloalkanes are therefore studied less for themselves than as the
central junction of organic synthesis.

::: key The one idea behind the whole unit
In R–X the carbon carries a partial positive charge (Cδ⁺–Xδ⁻), so the halogen
leaves as X⁻ and a **nucleophile** takes its place. Every reaction in Section
8.5 is the same reaction with a different nucleophile. The only question the
examiner can really ask is *which nucleophile, and by which mechanism —
S<sub>N</sub>1 or S<sub>N</sub>2?*
:::

## 8.1 Introduction; nomenclature, isomerism and classification of monohaloalkanes

A **haloalkane** (alkyl halide) is an alkane in which one or more hydrogen atoms
have been replaced by halogen atoms. A **monohaloalkane** contains just one
halogen and has the general formula **CₙH₂ₙ₊₁X**, written R–X.

**Nomenclature.** In the IUPAC system the halogen is named as a prefix —
*fluoro-, chloro-, bromo-, iodo-* — on the longest chain that contains the
halogenated carbon, numbered so that the substituents get the lowest locants.
The older common name is simply "alkyl halide".

| Structure | IUPAC name | Common name |
|---|---|---|
| CH₃Cl | chloromethane | methyl chloride |
| CH₃CH₂Br | bromoethane | ethyl bromide |
| CH₃CH₂CH₂I | 1-iodopropane | *n*-propyl iodide |
| (CH₃)₂CHCl | 2-chloropropane | isopropyl chloride |
| (CH₃)₃CBr | 2-bromo-2-methylpropane | *tert*-butyl bromide |
| CH₃CH(CH₃)CH₂Cl | 1-chloro-2-methylpropane | isobutyl chloride |

**Classification.** Monohaloalkanes are classified by the nature of the carbon
carrying the halogen:

| Class | Halogen-bearing carbon is joined to | Example |
|---|---|---|
| **Primary (1°)** | one (or no) other carbon | CH₃CH₂CH₂Br |
| **Secondary (2°)** | two other carbons | (CH₃)₂CHBr |
| **Tertiary (3°)** | three other carbons | (CH₃)₃CBr |

This classification is not bookkeeping — it decides the mechanism. Primary
halides react by S<sub>N</sub>2, tertiary halides by S<sub>N</sub>1.

**Isomerism.** Monohaloalkanes show three kinds of isomerism:

1. **Chain isomerism** — different carbon skeletons, e.g. 1-bromobutane and
   1-bromo-2-methylpropane.
2. **Position isomerism** — the same skeleton with the halogen on a different
   carbon, e.g. 1-bromobutane and 2-bromobutane.
3. **Optical isomerism** — when the halogen-bearing carbon has four different
   groups, e.g. 2-bromobutane, which exists as a pair of non-superimposable
   mirror images.

C₄H₉Br has exactly **four** structural isomers, and they are worth knowing by
heart because examiners ask for them year after year.

```figure caption="The four structural isomers of C₄H₉Br. Skeletal lines are carbon–carbon bonds; every unlabelled vertex and every line end is a carbon carrying enough hydrogens to make four bonds. The first two are chain isomers of each other, as are the last two; the pairs 1-/2-bromobutane and 1-/2-bromo-2-methylpropane are position isomers. Only 2-bromobutane has four different groups on the halogen-bearing carbon, so only it is optically active."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.2, 3.2))

def bond(p, q, c=INK, lw=1.5):
    ax.plot([p[0], q[0]], [p[1], q[1]], color=c, lw=lw,
            solid_capstyle='round', zorder=2)

def lab(p, s, c=INK, fs=9.0):
    ax.text(p[0], p[1], s, ha='center', va='center', fontsize=fs, color=c,
            bbox=dict(fc='white', ec='none', pad=0.9), zorder=3)

def zig(x0, y0, n, up=True, d=0.46, h=0.30):
    return [(x0 + i * d, y0 + (h if (i % 2 == 0) == up else 0)) for i in range(n)]

def chain(pts):
    for a, b in zip(pts, pts[1:]):
        bond(a, b)

# 1-bromobutane : Br + four carbons
p = zig(0.15, 2.45, 5)
chain(p)
lab(p[0], 'Br', SERIES[1])
ax.text(1.05, 1.58, '1-bromobutane  (1°)', fontsize=8.0, color=INK, ha='center')

# 2-bromobutane : four carbons, Br on C2
q = zig(3.05, 2.45, 4)
chain(q)
bond(q[1], (q[1][0], q[1][1] - 0.46))
lab((q[1][0], q[1][1] - 0.50), 'Br', SERIES[1])
ax.text(3.95, 1.58, '2-bromobutane  (2°)', fontsize=8.0, color=INK, ha='center')
ax.text(3.95, 1.26, 'chiral — optically active', fontsize=7.2, color=SERIES[4],
        ha='center')

# 1-bromo-2-methylpropane : Br + three chain carbons + a methyl branch on C2
r = zig(0.15, 0.55, 4)
chain(r)
bond(r[2], (r[2][0], r[2][1] - 0.46))
lab(r[0], 'Br', SERIES[1])
ax.text(0.95, -0.28, '1-bromo-2-methylpropane  (1°)', fontsize=8.0, color=INK,
        ha='center')

# 2-bromo-2-methylpropane : central C carrying three methyls and Br
c0 = (3.85, 0.62)
for dx, dy in [(-0.46, -0.30), (0.46, -0.30), (0.0, 0.50)]:
    bond(c0, (c0[0] + dx, c0[1] + dy))
bond(c0, (c0[0] + 0.66, c0[1] + 0.18))
lab((c0[0] + 0.78, c0[1] + 0.22), 'Br', SERIES[1])
ax.text(3.95, -0.28, '2-bromo-2-methylpropane  (3°)', fontsize=8.0, color=INK,
        ha='center')

ax.set_xlim(-0.45, 5.75); ax.set_ylim(-0.62, 3.20)
ax.set_aspect('equal'); ax.axis('off')
```
## 8.2 Preparation from alkanes, alkenes and alcohols

### From alkanes — free radical halogenation

In the presence of ultraviolet light or at 573–773 K, an alkane reacts with
chlorine or bromine by a free radical chain mechanism:

CH₄ + Cl₂ --UV light--> CH₃Cl + HCl

| Step | Reaction |
|---|---|
| Initiation | Cl₂ --hv--> 2Cl• |
| Propagation | CH₄ + Cl• → CH₃• + HCl ; CH₃• + Cl₂ → CH₃Cl + Cl• |
| Termination | CH₃• + Cl• → CH₃Cl ; 2Cl• → Cl₂ ; 2CH₃• → C₂H₆ |

The method is cheap but a poor laboratory preparation: the chloromethane formed
is itself attacked, giving CH₂Cl₂, CHCl₃ and CCl₄, and a higher alkane gives a
mixture of position isomers as well. Reactivity of the halogens falls
F₂ > Cl₂ > Br₂ > I₂; fluorination is explosive and iodination is reversible, so
only chlorination and bromination are useful. Iodination can be forced by adding
an oxidising agent (HIO₃ or conc. HNO₃) to destroy the HI as it forms.

### From alkenes

**Addition of hydrogen halide — Markovnikov's rule.** The hydrogen adds to the
doubly bonded carbon that already carries **more** hydrogens:

CH₃CH=CH₂ + HBr → CH₃CHBrCH₃ (2-bromopropane, major)

The reason is the stability of the intermediate carbocation: the secondary
cation CH₃C⁺HCH₃ is more stable than the primary CH₃CH₂C⁺H₂.

**Peroxide (Kharasch) effect.** In the presence of benzoyl peroxide the addition
of **HBr only** goes the other way, because the mechanism becomes free radical:

CH₃CH=CH₂ + HBr --peroxide--> CH₃CH₂CH₂Br (1-bromopropane)

HCl and HI show no peroxide effect — the H–Cl bond is too strong to break
homolytically and the C–I bond is too weak to survive.

Reactivity of the hydrogen halides towards an alkene is HI > HBr > HCl > HF.

### From alcohols — the standard laboratory route

This is the method to quote unless a question says otherwise, because it gives
one product in good yield.

| Reagent | Equation | Note |
|---|---|---|
| Conc. HCl + anhyd. ZnCl₂ | C₂H₅OH + HCl → C₂H₅Cl + H₂O | ZnCl₂ is a catalyst; the mixture is **Lucas reagent** |
| NaBr + conc. H₂SO₄ | C₂H₅OH + HBr → C₂H₅Br + H₂O | HBr generated in situ |
| Red P + I₂ | 3C₂H₅OH + PI₃ → 3C₂H₅I + H₃PO₃ | PI₃ made in the flask |
| PCl₃ | 3C₂H₅OH + PCl₃ → 3C₂H₅Cl + H₃PO₃ | |
| PCl₅ | C₂H₅OH + PCl₅ → C₂H₅Cl + POCl₃ + HCl | |
| **SOCl₂** | C₂H₅OH + SOCl₂ → C₂H₅Cl + SO₂↑ + HCl↑ | **Darzen's process** — best of all |

Thionyl chloride is preferred because both by-products are gases that simply
escape, leaving pure haloalkane with nothing to separate.

The ease of replacement of –OH follows the order **3° > 2° > 1°**, which is the
basis of the **Lucas test**: a tertiary alcohol gives an oily turbidity at once,
a secondary alcohol in about five minutes, and a primary alcohol only on
heating.

**Halogen exchange.** Two named reactions convert one haloalkane into another:

- **Finkelstein reaction:** R–Cl + NaI --dry acetone--> R–I + NaCl↓
  (NaCl is insoluble in acetone, so it precipitates and drives the equilibrium.)
- **Swarts reaction:** CH₃Br + AgF → CH₃F + AgBr (also with Hg₂F₂ or SbF₃);
  this is how fluoroalkanes and freons are made.

## 8.3 Physical properties

Haloalkanes are colourless liquids (the first few members are gases) with a
sweetish smell.

| Property | Trend | Reason |
|---|---|---|
| Boiling point, same alkyl group | RI > RBr > RCl > RF | heavier, more polarisable halogen → stronger van der Waals forces |
| Boiling point, same halogen | rises with chain length | larger surface area of contact |
| Effect of branching | branched isomer boils **lower** | a branched molecule is more spherical, so less surface contact |
| Density | RI > RBr > RCl; bromides and iodides sink in water | heavy halogen atom |
| Solubility | insoluble in water, soluble in benzene, ether, alcohol | cannot make hydrogen bonds strong enough to break water's own |
| Dipole moment | CH₃Cl (1.86 D) > CH₃F (1.85) > CH₃Br (1.79) > CH₃I (1.64) | product of charge separation and bond length |

The last row is a favourite short question. Fluorine is the most electronegative
atom, yet CH₃F does **not** have the largest dipole moment, because the C–F bond
is so short that the charges are not far enough apart.

```figure caption="Left: boiling points of the 1-haloalkanes. Each series rises steadily with chain length, and for any given chain the order is always iodide above bromide above chloride above fluoride, because the heavier halogen is more polarisable and gives stronger van der Waals attraction. Right: branching lowers the boiling point — the four isomers of C₄H₉Br boil over a range of nearly 30 °C, the most branched boiling lowest."
import numpy as np, matplotlib.pyplot as plt
n = np.array([1, 2, 3, 4, 5])
data = {'R–F': [-78.4, -37.7, -2.5, 32.5, 62.8],
        'R–Cl': [-24.2, 12.3, 46.6, 78.4, 107.8],
        'R–Br': [3.6, 38.4, 71.0, 101.6, 129.6],
        'R–I': [42.4, 72.3, 102.5, 130.5, 157.0]}
fig, axes = plt.subplots(1, 2, figsize=(5.2, 2.8))
ax = axes[0]
for (k, v), c, mk in zip(data.items(), [SERIES[4], SERIES[0], SERIES[2], SERIES[1]],
                         ['^', 's', 'o', 'D']):
    ax.plot(n, v, mk + '-', color=c, ms=4.0, label=k)
ax.axhline(0, color=MUTED, lw=0.8, ls=':')
ax.set_xlabel('carbon atoms in the chain')
ax.set_ylabel('boiling point (°C)')
ax.set_xticks(n); ax.set_ylim(-100, 185)
ax.legend(ncol=2, fontsize=7.4, columnspacing=1.0, loc='upper left')
ax.spines[['top', 'right']].set_visible(False); ax.grid(alpha=0.4)
ax = axes[1]
iso = ['n-butyl (1°)', 'isobutyl (1°)', 'sec-butyl (2°)', 'tert-butyl (3°)']
bp = [101.6, 91.7, 91.2, 73.3]
ax.bar(range(4), bp, color=[SERIES[2], SERIES[2], SERIES[3], SERIES[1]], width=0.6)
for i, v in enumerate(bp):
    ax.text(i, v + 2.5, f'{v}', ha='center', fontsize=7.2, color=INK)
ax.set_xticks(range(4))
ax.set_xticklabels(iso, fontsize=6.6, rotation=28, ha='right')
ax.set_ylabel('boiling point of C₄H₉Br (°C)', fontsize=8.0)
ax.set_ylim(0, 122)
ax.spines[['top', 'right']].set_visible(False); ax.grid(axis='y', alpha=0.4)
fig.subplots_adjust(wspace=0.40, bottom=0.30)
```
## 8.4 Chemical properties; substitution reactions S<sub>N</sub>1 and S<sub>N</sub>2

Because the halogen is more electronegative than carbon, the C–X bond is
polarised Cδ⁺–Xδ⁻. A **nucleophile** (an electron-rich species: OH⁻, CN⁻, NH₃,
RO⁻, RS⁻, NO₂⁻) attacks the positive carbon and the halide leaves as X⁻ with
the bonding pair. The result is **nucleophilic substitution**, written
S<sub>N</sub>.

The C–X bond gets weaker and longer down the group, so the leaving group leaves
more easily:

| Bond | C–F | C–Cl | C–Br | C–I |
|---|---|---|---|---|
| Bond length (pm) | 139 | 178 | 193 | 214 |
| Bond enthalpy (kJ mol⁻¹) | 452 | 351 | 293 | 234 |
| Reactivity in substitution | least | | | **greatest** |

**Order of reactivity: R–I > R–Br > R–Cl > R–F.** Iodide is the best leaving
group because the C–I bond is the weakest, even though iodine is the least
electronegative halogen.

### The S<sub>N</sub>2 mechanism

S<sub>N</sub>2 means *substitution, nucleophilic, bimolecular*. It happens in
**one step**: the nucleophile attacks the carbon from the side exactly opposite
to the leaving group (**backside attack**) while the halide is still leaving. At
the half-way point the carbon is joined to five things in a **transition state**
in which the three unchanged groups lie in a plane.

$$ \text{rate} = k\,[\text{R--X}]\,[\text{Nu}^-] $$

Because the nucleophile comes in from the back, the other three groups are
pushed through the plane like an umbrella turning inside out in the wind. The
product therefore has the **opposite configuration** from the reactant. This is
**Walden inversion**, and it is the proof that the mechanism is S<sub>N</sub>2.

```figure caption="The S(N)2 mechanism, shown for (S)-2-bromobutane with hydroxide ion. One step, no intermediate. The curly arrows show the movement of electron pairs: the lone pair on the hydroxide forms the new bond while the C–Br bonding pair leaves with the bromine. In the transition state (square brackets, double dagger) the carbon is joined to five groups and the three spectator groups lie in a plane. As the reaction finishes they swing past that plane, so the product has the inverted configuration — Walden inversion."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Polygon
fig, ax = plt.subplots(figsize=(5.2, 3.0))

def bond(p, q, c=INK, lw=1.4, ls='-'):
    ax.plot([p[0], q[0]], [p[1], q[1]], color=c, lw=lw, ls=ls,
            solid_capstyle='round', zorder=2)

def lab(p, s, c=INK, fs=8.2):
    ax.text(p[0], p[1], s, ha='center', va='center', fontsize=fs, color=c,
            bbox=dict(fc='white', ec='none', pad=0.5), zorder=4)

def wedge(p, q, c=INK, w=0.10):
    p = np.array(p, float); q = np.array(q, float)
    d = q - p; nv = np.array([-d[1], d[0]]) / np.hypot(*d)
    ax.add_patch(Polygon([p, q + nv * w, q - nv * w], closed=True, fc=c, ec=c,
                         zorder=2))

def hashed(p, q, c=INK, n=5, w=0.11):
    p = np.array(p, float); q = np.array(q, float)
    d = q - p; nv = np.array([-d[1], d[0]]) / np.hypot(*d)
    for i in range(1, n + 1):
        t = i / (n + 0.4); m = p + d * t; hw = w * t
        ax.plot([m[0] - nv[0] * hw, m[0] + nv[0] * hw],
                [m[1] - nv[1] * hw, m[1] + nv[1] * hw], color=c, lw=1.2, zorder=2)

def centre(cx, cy, back_left):
    # CH₃ points up, H points down, C₂H₅ marks the face the ethyl group sits on
    bond((cx, cy), (cx, cy + 0.60)); lab((cx, cy + 0.80), 'CH₃')
    bond((cx, cy), (cx, cy - 0.60)); lab((cx, cy - 0.78), 'H')
    if back_left:
        hashed((cx, cy), (cx - 0.44, cy - 0.46)); lab((cx - 0.72, cy - 0.64), 'C₂H₅')
    else:
        wedge((cx, cy), (cx + 0.44, cy - 0.46)); lab((cx + 0.74, cy - 0.64), 'C₂H₅')
    lab((cx, cy), 'C')

# --- stage 1: hydroxide attacks the face opposite to Br
c1 = 1.55
centre(c1, 0, True)
bond((c1 + 0.22, 0), (c1 + 1.05, 0))
lab((c1 + 1.28, 0), 'Br', SERIES[1])
lab((0.18, 0), 'HO⁻', SERIES[2])
ax.add_patch(FancyArrowPatch((0.48, 0.10), (c1 - 0.28, 0.06), arrowstyle='-|>',
                             color=SERIES[2], lw=1.2, mutation_scale=9,
                             connectionstyle='arc3,rad=-0.34', zorder=5))
ax.add_patch(FancyArrowPatch((c1 + 0.66, 0.14), (c1 + 1.30, 0.44), arrowstyle='-|>',
                             color=SERIES[1], lw=1.2, mutation_scale=9,
                             connectionstyle='arc3,rad=-0.55', zorder=5))
ax.text(c1 - 0.1, -1.48, 'backside attack', fontsize=7.6, color=SERIES[2],
        ha='center')

# --- stage 2: the single transition state
cx = 5.70
def bracket(x, y0, y1, side):
    ax.plot([x, x], [y0, y1], color=INK, lw=1.2, zorder=3)
    ax.plot([x, x + 0.18 * side], [y0, y0], color=INK, lw=1.2, zorder=3)
    ax.plot([x, x + 0.18 * side], [y1, y1], color=INK, lw=1.2, zorder=3)
bracket(3.98, -1.02, 1.18, +1)
bracket(7.44, -1.02, 1.18, -1)
ax.text(7.62, 1.20, '‡', fontsize=11, color=INK, ha='center', va='center')
bond((cx, 0), (cx, 0.60)); lab((cx, 0.80), 'CH₃')
bond((cx, 0), (cx, -0.60)); lab((cx, -0.78), 'H')
bond((cx, 0), (cx + 0.44, -0.46)); lab((cx + 0.74, -0.64), 'C₂H₅')
lab((cx, 0), 'C')
bond((cx - 1.18, 0), (cx - 0.22, 0), c=MUTED, ls=(0, (3, 2)))
bond((cx + 0.22, 0), (cx + 1.18, 0), c=MUTED, ls=(0, (3, 2)))
lab((cx - 1.45, 0), 'HO', SERIES[2])
lab((cx + 1.45, 0), 'Br', SERIES[1])
ax.text(cx - 1.45, 0.40, 'δ⁻', fontsize=8.0, color=SERIES[2], ha='center')
ax.text(cx + 1.45, 0.40, 'δ⁻', fontsize=8.0, color=SERIES[1], ha='center')
ax.text(cx, -1.44, 'transition state\n(five groups on C)', fontsize=7.6,
        color=MUTED, ha='center', va='top', linespacing=1.4)

# --- stage 3: product with the umbrella turned inside out
c3 = 9.80
centre(c3, 0, False)
bond((c3 - 0.22, 0), (c3 - 1.00, 0))
lab((c3 - 1.28, 0), 'HO', SERIES[2])
ax.text(c3 - 0.1, -1.48, 'configuration inverted', fontsize=7.6,
        color=SERIES[4], ha='center')

for x0, x1 in [(3.22, 3.78), (7.86, 8.42)]:
    ax.add_patch(FancyArrowPatch((x0, 0), (x1, 0), arrowstyle='-|>',
                                 color=INK, lw=1.3, mutation_scale=11))
ax.set_xlim(-0.25, 10.95); ax.set_ylim(-2.05, 1.55)
ax.set_aspect('equal'); ax.axis('off')
```
### The S<sub>N</sub>1 mechanism

S<sub>N</sub>1 means *substitution, nucleophilic, unimolecular*. It happens in
**two steps**:

- **Step 1 (slow, rate-determining).** The C–X bond breaks heterolytically on
  its own, giving a flat, sp²-hybridised **carbocation** and X⁻.
- **Step 2 (fast).** The nucleophile attacks the carbocation.

$$ \text{rate} = k\,[\text{R--X}] $$

The nucleophile does not appear in the rate law at all, because it joins the
reaction only after the slow step is over. Doubling the hydroxide concentration
does not change the rate — the single most quotable difference between the two
mechanisms.

The carbocation is **planar**, so the nucleophile can attack either face with
equal ease. A single enantiomer of the halide therefore gives a **50 : 50
mixture of both product enantiomers** — a racemic mixture. This is
**racemisation**.

```figure caption="The S(N)1 mechanism, shown for a tertiary halide. Step 1 is slow: the C–Br bond breaks by itself and the carbon becomes flat and sp2-hybridised, with an empty p orbital (the two open lobes). Step 2 is fast: hydroxide attacks that empty orbital. Because the two lobes are identical, attack is equally likely from above and from below, and the product is a 50:50 racemic mixture."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Ellipse
fig, ax = plt.subplots(figsize=(5.2, 3.2))

def bond(p, q, c=INK, lw=1.4, ls='-'):
    ax.plot([p[0], q[0]], [p[1], q[1]], color=c, lw=lw, ls=ls,
            solid_capstyle='round', zorder=3)

def lab(p, s, c=INK, fs=8.4):
    ax.text(p[0], p[1], s, ha='center', va='center', fontsize=fs, color=c,
            bbox=dict(fc='white', ec='none', pad=0.6), zorder=5)

# --- step 1: the halide
c1 = (1.30, 0.0)
for dx, dy, s in [(-0.52, 0.46, 'CH₃'), (-0.52, -0.46, 'CH₃'), (0.0, -0.66, 'CH₃')]:
    bond(c1, (c1[0] + dx, c1[1] + dy))
    lab((c1[0] + dx * 1.42, c1[1] + dy * 1.42), s)
lab(c1, 'C')
bond(c1, (c1[0] + 0.92, c1[1] + 0.62))
lab((c1[0] + 1.14, c1[1] + 0.78), 'Br', SERIES[1])
ax.add_patch(FancyArrowPatch((1.86, 0.44), (2.62, 1.02), arrowstyle='-|>',
                             color=SERIES[1], lw=1.2, mutation_scale=9,
                             connectionstyle='arc3,rad=-0.55', zorder=6))
ax.text(1.25, -1.98, 'tertiary halide', fontsize=7.6, color=MUTED, ha='center')

# --- step 2: planar carbocation
c2 = (5.55, 0.0)
ax.add_patch(Ellipse((c2[0], c2[1] + 0.72), 0.52, 1.10, fc=ACCENT, alpha=0.16,
                     ec=ACCENT, lw=1.0, zorder=1))
ax.add_patch(Ellipse((c2[0], c2[1] - 0.72), 0.52, 1.10, fc=ACCENT, alpha=0.16,
                     ec=ACCENT, lw=1.0, zorder=1))
for ang, s in [(150, 'CH₃'), (210, 'CH₃'), (0, 'CH₃')]:
    r = np.radians(ang)
    bond(c2, (c2[0] + 0.62 * np.cos(r), c2[1] + 0.62 * np.sin(r)))
    lab((c2[0] + 0.94 * np.cos(r), c2[1] + 0.94 * np.sin(r)), s)
lab(c2, 'C')
ax.text(c2[0] + 0.30, c2[1] + 0.30, '+', fontsize=11, color=SERIES[1])
ax.text(c2[0] + 0.02, c2[1] + 1.62, 'empty p orbital', fontsize=7.2,
        color=ACCENT, ha='center')
lab((c2[0] - 1.45, c2[1] + 1.05), 'HO⁻', SERIES[2])
lab((c2[0] - 1.45, c2[1] - 1.05), 'HO⁻', SERIES[2])
ax.add_patch(FancyArrowPatch((c2[0] - 1.10, c2[1] + 0.98), (c2[0] - 0.16, c2[1] + 0.72),
                             arrowstyle='-|>', color=SERIES[2], lw=1.2,
                             mutation_scale=9, connectionstyle='arc3,rad=0.30', zorder=6))
ax.add_patch(FancyArrowPatch((c2[0] - 1.10, c2[1] - 0.98), (c2[0] - 0.16, c2[1] - 0.72),
                             arrowstyle='-|>', color=SERIES[2], lw=1.2,
                             mutation_scale=9, connectionstyle='arc3,rad=-0.30', zorder=6))
ax.text(c2[0], -1.98, 'planar carbocation (sp²)', fontsize=7.6, color=MUTED, ha='center')

# --- step 3: racemic products
for cy, tag in [(1.10, 'attack from above'), (-0.95, 'attack from below')]:
    c3 = (9.70, cy)
    for dx, dy in [(-0.50, 0.34), (-0.50, -0.34), (0.0, -0.52)]:
        bond(c3, (c3[0] + dx, c3[1] + dy))
    lab(c3, 'C')
    bond(c3, (c3[0] + 0.72, cy + 0.34))
    lab((c3[0] + 0.98, cy + 0.42), 'OH', SERIES[2])
    ax.text(c3[0] + 0.05, cy + 0.95, tag, fontsize=6.8, color=MUTED, ha='center')
ax.text(9.9, -1.98, '50 : 50 racemic mixture', fontsize=7.6, color=SERIES[4], ha='center')

ax.add_patch(FancyArrowPatch((2.95, 0), (4.15, 0), arrowstyle='-|>',
                             color=INK, lw=1.3, mutation_scale=11))
ax.text(3.55, 0.20, 'slow', fontsize=7.4, color=INK, ha='center')
ax.text(3.55, -0.42, '−Br⁻', fontsize=7.4, color=SERIES[1], ha='center')
ax.add_patch(FancyArrowPatch((7.35, 0), (8.55, 0), arrowstyle='-|>',
                             color=INK, lw=1.3, mutation_scale=11))
ax.text(7.95, 0.20, 'fast', fontsize=7.4, color=INK, ha='center')
ax.set_xlim(-0.25, 11.3); ax.set_ylim(-2.35, 2.35)
ax.set_aspect('equal'); ax.axis('off')
```

### Energy profiles and the choice of mechanism

The two mechanisms look completely different on an energy profile. S<sub>N</sub>2
has **one** hump — one transition state, no intermediate. S<sub>N</sub>1 has
**two** humps with a **well** between them: the well is the carbocation, a real
(if short-lived) species that can be detected.

```figure caption="Reaction energy profiles. The S(N)2 profile has a single maximum, so there is one transition state and no intermediate; the S(N)1 profile has two maxima separated by a minimum, and that minimum is the carbocation intermediate. The first S(N)1 hump is the taller one, so step 1 is the rate-determining step and only R–X appears in the rate law."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

def path(xs, ys, n=500):
    X = np.linspace(xs[0], xs[-1], n); Y = np.zeros_like(X)
    for i in range(len(xs) - 1):
        m = (X >= xs[i]) & (X <= xs[i + 1])
        t = (X[m] - xs[i]) / (xs[i + 1] - xs[i])
        Y[m] = ys[i] + (ys[i + 1] - ys[i]) * (1 - np.cos(np.pi * t)) / 2
    return X, Y

fig, axes = plt.subplots(1, 2, figsize=(5.2, 2.9))

ax = axes[0]
X, Y = path([0, 1, 5, 9, 10], [0, 0, 11, -4, -4])
ax.plot(X, Y, color=ACCENT, lw=2.0)
ax.annotate('transition state\n(5 groups on C)', (5, 11), textcoords='offset points',
            xytext=(0, 6), ha='center', fontsize=6.8, color=INK)
ax.add_patch(FancyArrowPatch((2.1, 0), (2.1, 11), arrowstyle='<|-|>',
                             color=SERIES[1], lw=1.0, mutation_scale=7))
ax.text(1.15, 5.6, '$E_a$', fontsize=8.6, color=SERIES[1], va='center')
ax.text(0.3, -2.6, 'R–X + Nu⁻', fontsize=7.2, color=MUTED)
ax.text(9.6, -6.6, 'R–Nu\n+ X⁻', fontsize=7.2, color=MUTED, ha='right')
ax.set_title('S$_N$2  — one step', fontsize=9.0)
ax.set_ylim(-9, 19)

ax = axes[1]
X, Y = path([0, 1, 3, 5, 7, 9, 10], [0, 0, 16, 7, 11, -4, -4])
ax.plot(X, Y, color=SERIES[1], lw=2.0)
ax.annotate('TS 1', (3, 16), textcoords='offset points', xytext=(0, 5),
            ha='center', fontsize=7.0, color=INK)
ax.annotate('TS 2', (7, 11), textcoords='offset points', xytext=(6, 5),
            ha='center', fontsize=7.0, color=INK)
ax.annotate('carbocation\nintermediate', (5, 7), textcoords='offset points',
            xytext=(0, -24), ha='center', fontsize=6.8, color=SERIES[4],
            arrowprops=dict(arrowstyle='-|>', color=SERIES[4], lw=0.9, mutation_scale=7))
ax.add_patch(FancyArrowPatch((1.55, 0), (1.55, 16), arrowstyle='<|-|>',
                             color=SERIES[0], lw=1.0, mutation_scale=7))
ax.text(0.45, 8.0, '$E_a$', fontsize=8.6, color=SERIES[0], va='center')
ax.text(5.0, 21.5, 'step 1 is rate-determining', fontsize=6.8,
        color=SERIES[0], va='center', ha='center')
ax.text(0.3, -2.6, 'R–X', fontsize=7.2, color=MUTED)
ax.text(9.6, -6.6, 'R–Nu\n+ X⁻', fontsize=7.2, color=MUTED, ha='right')
ax.set_title('S$_N$1  — two steps', fontsize=9.0)
ax.set_ylim(-9, 24)

for ax in axes:
    ax.set_xlabel('reaction coordinate', fontsize=8.0)
    ax.set_ylabel('potential energy', fontsize=8.0)
    ax.set_xticks([]); ax.set_yticks([])
    ax.spines[['top', 'right']].set_visible(False)
fig.subplots_adjust(wspace=0.28)
```

| | S<sub>N</sub>1 | S<sub>N</sub>2 |
|---|---|---|
| Molecularity of slow step | 1 (only R–X) | 2 (R–X and Nu⁻) |
| Steps | two | one |
| Rate law | rate = $k[\text{RX}]$ | rate = $k[\text{RX}][\text{Nu}^-]$ |
| Intermediate | **carbocation** | none — only a transition state |
| Stereochemistry | racemisation | **inversion** (Walden) |
| Favoured by | 3° > 2° > 1° halide | CH₃X > 1° > 2° > 3° |
| Nucleophile | weak, low concentration | strong, high concentration |
| Solvent | polar **protic** (water, ethanol) | polar **aprotic** (acetone, DMSO) |
| Rearrangement | possible (carbocation can shift) | never |

::: caution The two reactivity orders are opposite — do not mix them up
For S<sub>N</sub>1 the order is 3° > 2° > 1° because a tertiary carbocation is
the most stable (three alkyl groups push electron density in). For
S<sub>N</sub>2 the order is exactly reversed, CH₃X > 1° > 2° > 3°, because the
three bulky groups on a tertiary carbon physically block the backside attack —
**steric hindrance**. The only order that stays the same for both is the
leaving group: R–I > R–Br > R–Cl > R–F.
:::

::: example Worked example 8.1
**Problem.** The hydrolysis of bromomethane by hydroxide ion in aqueous acetone
has rate $2.0\times10^{-4}\ \text{mol L}^{-1}\text{s}^{-1}$ when
$[\text{CH}_3\text{Br}] = 0.10\ \text{M}$ and $[\text{OH}^-] = 0.10\ \text{M}$.
(a) Find the rate constant. (b) What is the rate if the hydroxide concentration
alone is doubled? (c) What would the answer to (b) be for
2-bromo-2-methylpropane, and why?

**Solution.** (a) Bromomethane is a primary (in fact methyl) halide, so the
mechanism is S<sub>N</sub>2 and the rate law is second order overall:

$$ \text{rate} = k[\text{CH}_3\text{Br}][\text{OH}^-] $$

$$ k = \frac{2.0\times10^{-4}}{0.10\times0.10} = 2.0\times10^{-2}\ \text{L mol}^{-1}\text{s}^{-1} $$

(b) The rate is first order in hydroxide, so doubling $[\text{OH}^-]$ doubles the
rate:

$$ \text{rate} = 2.0\times10^{-2}\times0.10\times0.20 = 4.0\times10^{-4}\ \text{mol L}^{-1}\text{s}^{-1} $$

(c) 2-Bromo-2-methylpropane is tertiary, so it reacts by S<sub>N</sub>1 with
rate $=k[\text{RBr}]$. Hydroxide takes no part in the slow step, so doubling
$[\text{OH}^-]$ leaves the rate **unchanged**.
:::

## 8.5 Formation of alcohol, nitrile, amine, ether, thioether, carbylamine, nitrite and nitroalkane

Every reaction below is nucleophilic substitution. Learn the table as one
reaction with eight different nucleophiles.

| Reagent and conditions | Nucleophile | Product | Class |
|---|---|---|---|
| KOH or NaOH, **aqueous**, warm | OH⁻ | C₂H₅OH | alcohol |
| moist Ag₂O | OH⁻ | C₂H₅OH | alcohol |
| **KCN**, alcoholic | ⁻C≡N (through **carbon**) | CH₃CH₂CN, propanenitrile | nitrile |
| **AgCN**, alcoholic | ⁻N≡C (through **nitrogen**) | CH₃CH₂NC, ethyl isocyanide | carbylamine (isocyanide) |
| NH₃, alcoholic, excess, sealed tube | NH₃ | C₂H₅NH₂ | primary amine |
| **R'ONa**, dry (Williamson) | R'O⁻ | C₂H₅OC₂H₅ | ether |
| **R'SNa** or KSH | R'S⁻ / HS⁻ | C₂H₅SC₂H₅ / C₂H₅SH | thioether / thiol |
| **KNO₂**, aqueous alcohol | O–N=O (through **oxygen**) | C₂H₅–O–N=O | alkyl nitrite |
| **AgNO₂**, alcoholic | ⁻NO₂ (through **nitrogen**) | C₂H₅NO₂ | nitroalkane |

Written out with equations:

- C₂H₅Br + KOH(aq) → C₂H₅OH + KBr
- C₂H₅Br + KCN → C₂H₅CN + KBr
- C₂H₅Br + AgCN → C₂H₅NC + AgBr
- C₂H₅Br + 2NH₃ → C₂H₅NH₂ + NH₄Br
- C₂H₅Br + C₂H₅ONa → C₂H₅OC₂H₅ + NaBr
- C₂H₅Br + C₂H₅SNa → C₂H₅SC₂H₅ + NaBr
- C₂H₅Br + KNO₂ → C₂H₅ONO + KBr
- C₂H₅Br + AgNO₂ → C₂H₅NO₂ + AgBr

::: key The silver salt rule — this is examined every single year
KCN and KNO₂ are **ionic**, so the anion attacks through the atom that carries
the negative charge most freely (C of CN⁻, O of NO₂⁻), giving the **nitrile**
and the **alkyl nitrite**. AgCN and AgNO₂ are largely **covalent**, so the
carbon and the oxygen are tied up in the bond to silver and the attack must
happen through the **nitrogen**, giving the **isocyanide** and the
**nitroalkane**. Potassium → C or O; silver → N.
:::

The ammonolysis reaction does not stop at the primary amine: the amine produced
is itself a nucleophile, so a mixture of primary, secondary and tertiary amines
and finally the quaternary ammonium salt is obtained. A large excess of ammonia
favours the primary amine.

## 8.6 Elimination reaction; reduction; the Wurtz reaction

### Dehydrohalogenation and Saytzeff's rule

Heated with **alcoholic** potassium hydroxide, a haloalkane loses HX and becomes
an alkene. The base takes a hydrogen from the carbon **next to** the one
carrying the halogen (the β-carbon), so the reaction is called **β-elimination**:

CH₃CH₂Br + KOH(alc.) --Δ--> CH₂=CH₂ + KBr + H₂O

::: caution Aqueous KOH and alcoholic KOH give different products
The same reagent, two different solvents, two different answers. In **water**
the hydroxide acts as a **nucleophile** and you get the alcohol (substitution).
In **alcohol** it acts as a **base**, pulling off a β-hydrogen, and you get the
alkene (elimination). Losing a mark here is the most avoidable mistake in the
whole unit.
:::

When the halide has two different β-carbons, two alkenes are possible.
**Saytzeff's (Zaitsev's) rule** says the major product is the **more
substituted** alkene — the one with more alkyl groups attached to the doubly
bonded carbons — because it is the more stable.

```figure caption="Saytzeff elimination from 2-bromobutane. Hydroxide can remove a hydrogen from C1 or from C3. Removing it from C3 gives but-2-ene, which has two alkyl groups on the double bond and is the more stable, more substituted alkene; it is the major product. Removing it from C1 gives the less substituted but-1-ene, the minor product."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.0, 3.0))

def bond(p, q, c=INK, lw=1.5):
    ax.plot([p[0], q[0]], [p[1], q[1]], color=c, lw=lw,
            solid_capstyle='round', zorder=2)

def lab(p, s, c=INK, fs=8.6):
    ax.text(p[0], p[1], s, ha='center', va='center', fontsize=fs, color=c,
            bbox=dict(fc='white', ec='none', pad=0.8), zorder=4)

def dbl(p, q, c=INK):
    d = np.array(q) - np.array(p); L = np.hypot(*d); nv = np.array([-d[1], d[0]]) / L * 0.075
    bond(np.array(p) + nv, np.array(q) + nv, c)
    bond(np.array(p) - nv, np.array(q) - nv, c)

# reactant: 2-bromobutane
pts = [(0.15, 0.30), (0.62, 0.0), (1.09, 0.30), (1.56, 0.0)]
for a, b in zip(pts, pts[1:]):
    bond(a, b)
bond(pts[1], (pts[1][0], pts[1][1] - 0.46))
lab((pts[1][0], pts[1][1] - 0.52), 'Br', SERIES[1])
for p, t, c in [(pts[0], '1', SERIES[0]), (pts[1], '2', MUTED),
                (pts[2], '3', SERIES[2]), (pts[3], '4', MUTED)]:
    ax.text(p[0], p[1] + 0.22, t, fontsize=7.0, color=c, ha='center')
ax.text(0.85, -1.05, '2-bromobutane', fontsize=8.0, color=INK, ha='center')
ax.text(0.85, -1.38, 'alc. KOH, Δ', fontsize=7.4, color=MUTED, ha='center')

# arrows to products
ax.add_patch(FancyArrowPatch((2.05, 0.15), (3.05, 1.15), arrowstyle='-|>',
                             color=SERIES[2], lw=1.4, mutation_scale=11))
ax.add_patch(FancyArrowPatch((2.05, -0.10), (3.05, -1.05), arrowstyle='-|>',
                             color=SERIES[0], lw=1.4, mutation_scale=11))
ax.text(2.30, 0.92, '−H from C3', fontsize=7.2, color=SERIES[2], rotation=42)
ax.text(2.30, -1.02, '−H from C1', fontsize=7.2, color=SERIES[0], rotation=-42)

# major product: but-2-ene
q = [(3.35, 1.35), (3.82, 1.05), (4.29, 1.35), (4.76, 1.05)]
bond(q[0], q[1]); dbl(q[1], q[2]); bond(q[2], q[3])
ax.text(4.05, 0.62, 'but-2-ene  —  MAJOR (≈80%)', fontsize=8.0,
        color=SERIES[2], ha='center')
ax.text(4.05, 0.32, 'two alkyl groups on the C=C', fontsize=7.0,
        color=MUTED, ha='center')

# minor product: but-1-ene
r = [(3.35, -1.05), (3.82, -1.35), (4.29, -1.05), (4.76, -1.35)]
dbl(r[0], r[1]); bond(r[1], r[2]); bond(r[2], r[3])
ax.text(4.05, -1.78, 'but-1-ene  —  minor (≈20%)', fontsize=8.0,
        color=SERIES[0], ha='center')
ax.text(4.05, -2.06, 'one alkyl group on the C=C', fontsize=7.0,
        color=MUTED, ha='center')

ax.set_xlim(-0.25, 5.65); ax.set_ylim(-2.35, 1.85)
ax.set_aspect('equal'); ax.axis('off')
```

The ease of dehydrohalogenation is **3° > 2° > 1°**, and for the same alkyl
group R–I > R–Br > R–Cl.

### Reduction

Reduction replaces the halogen by hydrogen and gives back the parent alkane:

C₂H₅Br + 2[H] --Zn/HCl--> C₂H₆ + HBr

Suitable reducing agents are Zn + HCl, Zn–Cu couple in ethanol, LiAlH₄ in dry
ether, and H₂ over a nickel catalyst.

### The Wurtz reaction

Two molecules of haloalkane are joined by metallic sodium in dry ether:

2C₂H₅Br + 2Na --dry ether--> C₄H₁₀ + 2NaBr

This is the standard way of climbing from a small alkane to one with **twice**
as many carbon atoms, so it can only make alkanes with an **even** number of
carbons from a single halide. If two different halides are used, three products
form (R–R, R–R' and R'–R') and separating them is a nuisance. Tertiary halides
give alkenes instead, by elimination.

::: example Worked example 8.2
**Problem.** 21.8 g of bromoethane is treated with excess sodium in dry ether.
Calculate the mass and the volume at STP of the alkane formed, assuming the
reaction is complete. (C = 12, H = 1, Br = 80)

**Solution.** The Wurtz reaction is

2C₂H₅Br + 2Na → C₄H₁₀ + 2NaBr

$M(\text{C}_2\text{H}_5\text{Br}) = 24 + 5 + 80 = 109\ \text{g mol}^{-1}$, so

$$ n(\text{C}_2\text{H}_5\text{Br}) = \frac{21.8}{109} = 0.200\ \text{mol} $$

Two moles of halide give one mole of butane, so
$n(\text{C}_4\text{H}_{10}) = 0.100\ \text{mol}$ and

$$ m = 0.100\times58 = 5.8\ \text{g},\qquad
V = 0.100\times22.4 = 2.24\ \text{L at STP} $$
:::

::: example Worked example 8.3
**Problem.** A monobromoalkane contains 58.4% bromine by mass. Find its
molecular formula, and name and classify all its structural isomers.
(C = 12, H = 1, Br = 80)

**Solution.** A monobromoalkane is CₙH₂ₙ₊₁Br, of molar mass

$$ M = 12n + (2n+1) + 80 = 14n + 81 $$

The mass fraction of bromine is

$$ \frac{80}{14n+81} = 0.584 \;\Longrightarrow\; 14n + 81 = \frac{80}{0.584} = 137.0 $$

$$ 14n = 56.0 \;\Longrightarrow\; n = 4 $$

The formula is **C₄H₉Br**, and its four isomers are

| Isomer | Name | Class |
|---|---|---|
| CH₃CH₂CH₂CH₂Br | 1-bromobutane | 1° |
| CH₃CH₂CHBrCH₃ | 2-bromobutane | 2° |
| (CH₃)₂CHCH₂Br | 1-bromo-2-methylpropane | 1° |
| (CH₃)₃CBr | 2-bromo-2-methylpropane | 3° |
:::

## 8.7 Preparation of trichloromethane from ethanol and propanone

Trichloromethane, CHCl₃, is the old anaesthetic **chloroform**. It is made
industrially and in the laboratory by the **haloform reaction**, in which
bleaching powder supplies both the chlorine and the alkali.

Bleaching powder in water provides the two reagents:

CaOCl₂ + H₂O → Ca(OH)₂ + Cl₂

### From ethanol — three steps

| Step | Reaction | What happens |
|---|---|---|
| 1. Oxidation | CH₃CH₂OH + Cl₂ → CH₃CHO + 2HCl | ethanol → ethanal |
| 2. Chlorination | CH₃CHO + 3Cl₂ → CCl₃CHO + 3HCl | ethanal → trichloroethanal (**chloral**) |
| 3. Hydrolysis | 2CCl₃CHO + Ca(OH)₂ → 2CHCl₃ + (HCOO)₂Ca | chloral → chloroform + calcium methanoate |

### From propanone — two steps

Propanone already has the carbonyl group, so no oxidation step is needed and the
yield is better. This is the preferred method.

| Step | Reaction |
|---|---|
| 1. Chlorination | CH₃COCH₃ + 3Cl₂ → CCl₃COCH₃ + 3HCl |
| 2. Hydrolysis | 2CCl₃COCH₃ + Ca(OH)₂ → 2CHCl₃ + (CH₃COO)₂Ca |

In both routes the crude chloroform distils over with steam, and is purified by
shaking with concentrated sulphuric acid, washing with dilute alkali and water,
drying over anhydrous calcium chloride and redistilling at 334 K.

::: memory Why propanone beats ethanol
Ethanol needs **three** steps (oxidation, chlorination, hydrolysis) because the
carbonyl group has to be made first. Propanone needs only **two** (chlorination,
hydrolysis). Same reagent — bleaching powder — same final step, one step fewer,
higher yield.
:::

## 8.8 Chemical properties of trichloromethane

Chloroform is a colourless, sweet-smelling, heavy liquid (density 1.49 g cm⁻³,
b.p. 61 °C), almost insoluble in water, non-inflammable, and a good solvent for
fats, oils, waxes, resins, rubber and iodine.

### Oxidation — the reason chloroform is kept in a dark bottle

In air and sunlight chloroform is slowly oxidised to **phosgene** (carbonyl
chloride), an extremely poisonous gas used as a war gas in 1915:

**2CHCl₃ + O₂ --light--> 2COCl₂ + 2HCl**

This is why chloroform is stored in **dark brown bottles filled to the brim**
(to keep out light and air) with about **1% ethanol** added. The ethanol
destroys any phosgene that does form, turning it into harmless diethyl
carbonate:

COCl₂ + 2C₂H₅OH → (C₂H₅O)₂CO + 2HCl

### Reduction

CHCl₃ + 2[H] --Zn/HCl--> CH₂Cl₂ + HCl

Zinc dust and water give dichloromethane; with excess reducing agent the
reduction goes all the way to methane, CHCl₃ + 6[H] → CH₄ + 3HCl.

### Action on silver powder

Heated with silver powder, chloroform loses all its chlorine and the two carbon
skeletons join, giving **ethyne**:

**2CHCl₃ + 6Ag → C₂H₂↑ + 6AgCl**

### Action with concentrated nitric acid

**CHCl₃ + HNO₃ → CCl₃NO₂ + H₂O**

The product, trichloronitromethane, is **chloropicrin** — a tear gas, and a soil
fumigant and insecticide.

### Action with propanone

In the presence of dilute potassium hydroxide, chloroform adds across the
carbonyl group of propanone:

**CHCl₃ + CH₃COCH₃ --dil. KOH--> (CH₃)₂C(OH)CCl₃**

The product, 1,1,1-trichloro-2-methylpropan-2-ol, is **chloretone**, once widely
used as a hypnotic and sedative.

### Action with aqueous alkali

Boiled with aqueous sodium hydroxide, chloroform is hydrolysed to a salt of
methanoic acid:

**CHCl₃ + 4NaOH → HCOONa + 3NaCl + 2H₂O**

### The carbylamine reaction

Warmed with a primary amine and alcoholic KOH, chloroform gives an isocyanide
with an appalling smell — the standard test for a **primary** amine:

C₆H₅NH₂ + CHCl₃ + 3KOH → C₆H₅NC + 3KCl + 3H₂O

| Reagent | Product | Name of product |
|---|---|---|
| O₂ + light | COCl₂ | phosgene |
| Zn/HCl | CH₂Cl₂ | dichloromethane |
| Ag powder, Δ | C₂H₂ | ethyne |
| conc. HNO₃ | CCl₃NO₂ | chloropicrin |
| propanone + dil. KOH | (CH₃)₂C(OH)CCl₃ | chloretone |
| NaOH(aq), boil | HCOONa | sodium methanoate |
| RNH₂ + alc. KOH | RNC | isocyanide (carbylamine test) |

**Uses of chloroform.** Solvent for fats, oils, rubber, resins and iodine;
manufacture of chloretone, chloropicrin and the refrigerant Freon-22
(CHCl₃ + 2HF --SbF₅--> CHClF₂ + 2HCl); a preservative for anatomical specimens;
and formerly a general anaesthetic, now abandoned because it damages the liver.

::: example Worked example 8.4
**Problem.** Chloroform is prepared from 9.20 g of ethanol by the bleaching
powder method. Calculate the theoretical mass of chloroform, and the actual mass
if the yield is 60%. (C = 12, H = 1, O = 16, Cl = 35.5)

**Solution.** Over the three steps one molecule of ethanol gives one molecule of
chloroform:

CH₃CH₂OH → CH₃CHO → CCl₃CHO → CHCl₃

$M(\text{C}_2\text{H}_5\text{OH}) = 46\ \text{g mol}^{-1}$, so

$$ n = \frac{9.20}{46} = 0.200\ \text{mol} $$

Therefore $n(\text{CHCl}_3) = 0.200\ \text{mol}$, and with
$M(\text{CHCl}_3) = 12 + 1 + 3(35.5) = 119.5\ \text{g mol}^{-1}$:

$$ m_{\text{theoretical}} = 0.200\times119.5 = 23.9\ \text{g} $$

$$ m_{\text{actual}} = 0.60\times23.9 = 14.3\ \text{g} $$
:::

## Chapter summary

- A monohaloalkane is CₙH₂ₙ₊₁X. It is 1°, 2° or 3° according to the number of
  carbons on the halogen-bearing carbon, and shows chain, position and (when
  that carbon has four different groups) optical isomerism. C₄H₉Br has four
  structural isomers.
- Preparation: free radical halogenation of alkanes (gives mixtures);
  Markovnikov addition of HX to alkenes, reversed for HBr by peroxides; and —
  best — alcohols with conc. HX/ZnCl₂, PCl₃, PCl₅ or **SOCl₂ (Darzen's
  process)**. Finkelstein (NaI/acetone) and Swarts (AgF) exchange halogens.
- Boiling point rises RF < RCl < RBr < RI and with chain length, and falls with
  branching. Dipole moments run CH₃Cl > CH₃F > CH₃Br > CH₃I.
- Reactivity in nucleophilic substitution is **R–I > R–Br > R–Cl > R–F**,
  because the C–X bond enthalpy falls in that order.
- **S<sub>N</sub>2:** one step, backside attack, rate = $k[\text{RX}][\text{Nu}^-]$,
  transition state with five groups on carbon, **inversion** of configuration,
  favoured by CH₃X > 1° > 2° > 3° and strong nucleophiles.
- **S<sub>N</sub>1:** two steps through a planar **carbocation**,
  rate = $k[\text{RX}]$, **racemisation**, favoured by 3° > 2° > 1°, weak
  nucleophiles and polar protic solvents. Its energy profile has two humps and
  an intermediate well; the S<sub>N</sub>2 profile has one hump and none.
- The eight nucleophiles: OH⁻ → alcohol; KCN → nitrile but AgCN → isocyanide;
  NH₃ → amine; R'ONa → ether (Williamson); R'SNa → thioether; KNO₂ → alkyl
  nitrite but AgNO₂ → nitroalkane. **Potassium attacks through C or O, silver
  through N.**
- **Aqueous** KOH substitutes (alcohol); **alcoholic** KOH eliminates (alkene),
  the more substituted alkene being the major product by **Saytzeff's rule**.
  Reduction gives the alkane; the **Wurtz reaction**
  (2RX + 2Na, dry ether) doubles the chain.
- Chloroform is made from ethanol (3 steps) or propanone (2 steps) with
  bleaching powder. It is oxidised in air and light to poisonous **phosgene**,
  so it is kept in dark bottles with 1% ethanol; with Ag it gives ethyne, with
  conc. HNO₃ chloropicrin, with propanone chloretone, and with aqueous NaOH
  sodium methanoate.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The number of structural isomers of C₄H₉Br is <span class="marks">[1]</span>
   (a) 2 (b) 3 (c) 4 (d) 5
2. Which haloalkane is most reactive towards nucleophilic substitution? <span class="marks">[1]</span>
   (a) CH₃CH₂F (b) CH₃CH₂Cl (c) CH₃CH₂Br (d) CH₃CH₂I
3. An S<sub>N</sub>2 reaction proceeds with <span class="marks">[1]</span>
   (a) retention of configuration (b) inversion of configuration (c) racemisation (d) no stereochemical change
4. The intermediate in an S<sub>N</sub>1 reaction is <span class="marks">[1]</span>
   (a) a carbanion (b) a free radical (c) a carbocation (d) a carbene
5. Bromoethane heated with alcoholic KOH gives <span class="marks">[1]</span>
   (a) ethanol (b) ethene (c) ethane (d) ethoxyethane
6. Bromoethane warmed with silver cyanide gives mainly <span class="marks">[1]</span>
   (a) propanenitrile (b) ethyl isocyanide (c) ethylamine (d) ethanol
7. Chloroform is stored in dark bottles because in light and air it forms <span class="marks">[1]</span>
   (a) chloropicrin (b) chloretone (c) phosgene (d) ethyne
8. The reagent that converts ethanol to chloroethane with only gaseous by-products is <span class="marks">[1]</span>
   (a) PCl₅ (b) PCl₃ (c) SOCl₂ (d) conc. HCl

::: note Answers to Group A
**1.** (c) — 1-bromobutane, 2-bromobutane, 1-bromo-2-methylpropane and 2-bromo-2-methylpropane.

**2.** (d) — the C–I bond is the weakest (234 kJ mol⁻¹), so iodide is the best leaving group.

**3.** (b) — backside attack turns the molecule inside out (Walden inversion).

**4.** (c) — the slow step is heterolysis of C–X to give a planar carbocation.

**5.** (b) — alcoholic KOH acts as a base and eliminates HBr.

**6.** (b) — AgCN is covalent, so attack is through nitrogen and an isocyanide is formed.

**7.** (c) — 2CHCl₃ + O₂ → 2COCl₂ + 2HCl.

**8.** (c) — Darzen's process; SO₂ and HCl both escape as gases.
:::

**Group B — Short answer (5 marks each)**

1. Define a haloalkane. Write the structures, IUPAC names and classification
   (1°, 2°, 3°) of all the isomers of C₄H₉Br, and state which one is optically
   active. <span class="marks">[5]</span>
2. How is bromoethane prepared from (a) ethene and (b) ethanol? Why is thionyl
   chloride the best reagent for making chloroethane from ethanol? <span class="marks">[5]</span>
3. Explain the S<sub>N</sub>2 mechanism with a suitable example. Why does it
   give inversion of configuration, and why is a tertiary halide unreactive by
   this route? <span class="marks">[5]</span>
4. Distinguish between S<sub>N</sub>1 and S<sub>N</sub>2 mechanisms under five
   headings. <span class="marks">[5]</span>
5. What happens when bromoethane is treated with (a) KCN, (b) AgCN,
   (c) AgNO₂, (d) KNO₂, (e) sodium ethoxide? Give equations and name the
   products. <span class="marks">[5]</span>
6. State Saytzeff's rule. Predict and explain the major product when
   2-bromobutane is heated with alcoholic KOH. <span class="marks">[5]</span>
7. 21.8 g of bromoethane is heated with sodium in dry ether. Name the reaction,
   write the equation, and calculate the volume of gas produced at
   STP. <span class="marks">[5]</span>
8. How is chloroform prepared from propanone? Why is this route preferred to the
   one starting from ethanol? <span class="marks">[5]</span>

::: note Answers to Group B
**2.** (a) Ethene + HBr → CH₃CH₂Br; the addition needs no peroxide because ethene
is symmetrical, so Markovnikov's rule does not arise. (b) Ethanol is warmed with
NaBr and conc. H₂SO₄, which generates HBr in the flask:
C₂H₅OH + HBr → C₂H₅Br + H₂O. Thionyl chloride is best for the chloride because
C₂H₅OH + SOCl₂ → C₂H₅Cl + SO₂↑ + HCl↑ — both by-products are gases and escape,
so the haloalkane is obtained pure with no separation step.

**4.**

| | S<sub>N</sub>1 | S<sub>N</sub>2 |
|---|---|---|
| Steps | two | one |
| Rate law | $k[\text{RX}]$ | $k[\text{RX}][\text{Nu}^-]$ |
| Intermediate | carbocation | none (transition state only) |
| Stereochemistry | racemisation | inversion |
| Favoured by | 3° halide, weak nucleophile, protic solvent | 1° halide, strong nucleophile, aprotic solvent |

**6.** Saytzeff's rule: in a dehydrohalogenation the alkene with the greater
number of alkyl groups on the doubly bonded carbons is the major product,
because alkyl groups release electrons into the double bond (hyperconjugation
and inductive effect) and stabilise it. 2-Bromobutane can lose a β-hydrogen
from C1 or C3. Loss from C3 gives **but-2-ene**, CH₃CH=CHCH₃, which is
disubstituted; loss from C1 gives but-1-ene, CH₂=CHCH₂CH₃, which is
monosubstituted. But-2-ene is therefore the major product (about 80%).

**7.** The **Wurtz reaction**: 2C₂H₅Br + 2Na → C₄H₁₀ + 2NaBr.
$n(\text{C}_2\text{H}_5\text{Br}) = 21.8/109 = 0.200\ \text{mol}$, so
$n(\text{C}_4\text{H}_{10}) = 0.100\ \text{mol}$ and

$$ V = 0.100 \times 22.4 = 2.24\ \text{L at STP} $$

**8.** Bleaching powder in water gives Ca(OH)₂ and Cl₂. Then
CH₃COCH₃ + 3Cl₂ → CCl₃COCH₃ + 3HCl, and
2CCl₃COCH₃ + Ca(OH)₂ → 2CHCl₃ + (CH₃COO)₂Ca. Propanone is preferred because it
already contains the carbonyl group, so the oxidation step needed with ethanol
is unnecessary: two steps instead of three, and a higher yield.
:::

**Group C — Long answer (8 marks each)**

1. (a) Describe the S<sub>N</sub>1 and S<sub>N</sub>2 mechanisms of hydrolysis
   of a haloalkane, using suitable examples, and draw the energy profile of
   each. <span class="marks">[5]</span>
   (b) Explain why 2-bromo-2-methylpropane hydrolyses by S<sub>N</sub>1 while
   bromomethane hydrolyses by S<sub>N</sub>2. <span class="marks">[3]</span>
2. (a) How is trichloromethane prepared from ethanol? Give all three
   equations. <span class="marks">[4]</span>
   (b) What happens when chloroform is treated with (i) air and sunlight,
   (ii) silver powder, (iii) conc. HNO₃, (iv) aqueous NaOH? Give
   equations. <span class="marks">[4]</span>
3. An organic compound **A**, C₃H₇Br, reacts with aqueous KOH to give **B**,
   and with alcoholic KOH to give **C**, C₃H₆. **A** with KCN gives **D**, and
   **A** with sodium in dry ether gives **E**, C₆H₁₄. Identify **A** to **E**,
   write all the equations, and state the mechanism by which **A** reacts with
   aqueous KOH if **A** is the 2-bromo isomer. <span class="marks">[8]</span>

::: note Answers to Group C
**1.(b)** In 2-bromo-2-methylpropane the halogen-bearing carbon carries three
methyl groups. They release electron density by the inductive effect and by
hyperconjugation, so the carbocation left behind when Br⁻ departs is strongly
stabilised, and the slow heterolysis of step 1 becomes easy — S<sub>N</sub>1.
The same three methyl groups also crowd the back of the carbon, so backside
attack is sterically blocked and S<sub>N</sub>2 is impossible. Bromomethane is
the opposite case: the CH₃⁺ cation would be very unstable, so S<sub>N</sub>1 is
ruled out, while the carbon is completely unhindered and the nucleophile can
reach it easily — S<sub>N</sub>2.

**2.(a)** CaOCl₂ + H₂O → Ca(OH)₂ + Cl₂;
CH₃CH₂OH + Cl₂ → CH₃CHO + 2HCl;
CH₃CHO + 3Cl₂ → CCl₃CHO + 3HCl;
2CCl₃CHO + Ca(OH)₂ → 2CHCl₃ + (HCOO)₂Ca.

**2.(b)** (i) 2CHCl₃ + O₂ → 2COCl₂ + 2HCl (phosgene).
(ii) 2CHCl₃ + 6Ag → C₂H₂ + 6AgCl (ethyne).
(iii) CHCl₃ + HNO₃ → CCl₃NO₂ + H₂O (chloropicrin).
(iv) CHCl₃ + 4NaOH → HCOONa + 3NaCl + 2H₂O (sodium methanoate).

**3.** **A** = C₃H₇Br (1-bromopropane or 2-bromopropane).
**B** = propan-1-ol or propan-2-ol, C₃H₇OH:
C₃H₇Br + KOH(aq) → C₃H₇OH + KBr.
**C** = propene, CH₃CH=CH₂:
C₃H₇Br + KOH(alc.) → CH₃CH=CH₂ + KBr + H₂O.
**D** = butanenitrile (or 2-methylpropanenitrile), C₃H₇CN:
C₃H₇Br + KCN → C₃H₇CN + KBr.
**E** = hexane, C₆H₁₄, by the Wurtz reaction:
2C₃H₇Br + 2Na → C₆H₁₄ + 2NaBr.

If **A** is 2-bromopropane it is a **secondary** halide. Secondary halides sit
on the borderline, but with a strong nucleophile such as concentrated aqueous
hydroxide the reaction is mainly **S<sub>N</sub>2**, giving propan-2-ol with
inversion at the chiral centre; in a highly ionising solvent with dilute
hydroxide it drifts towards S<sub>N</sub>1 and partial racemisation.
:::
