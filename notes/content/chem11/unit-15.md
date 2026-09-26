---
subject: Chemistry
grade: 11
unit: 15
title: Aromatic Hydrocarbons
hours: 6
area: Organic Chemistry
---

The hydrocarbons of Unit 14 behaved exactly as their bonds predicted: a double
bond added, a triple bond added twice, a single bond was hard to touch. Benzene,
C₆H₆, breaks that pattern completely. On paper it looks like a ring with three
double bonds, so it should decolourise bromine water instantly and burn through
its unsaturation in every test. It does neither. It refuses to add, it prefers
to **substitute**, and it releases far less energy on hydrogenation than three
double bonds ought to. That stubbornness has a name — **aromaticity** — and this
unit is about where it comes from and what it does to the chemistry.

::: key What the examiner asks from this unit
Four things come up almost every year: Hückel's rule applied to a given ring,
the evidence for and against the Kekulé structure, the mechanism of one
electrophilic substitution (usually nitration), and the o/p versus m orientation
rules with a reason. Learn the four Friedel–Crafts-type reactions as a block —
reagent, catalyst, electrophile, product — because they are usually asked as a
single five-mark question.
:::

## 15.1 Introduction and characteristics of aromatic compounds

The word *aromatic* is a historical accident. The first members of the class —
benzaldehyde from almonds, vanillin from vanilla pods, oil of wintergreen — were
isolated because they smelled pleasant, and the name stuck long before anyone
understood the bonding. Today the smell is irrelevant; the word means a ring
system with a closed loop of delocalised π electrons and the unusual stability
that comes with it.

Organic compounds are therefore sorted into three families:

| Class | Description | Example |
|---|---|---|
| Aliphatic | Open chain, or a ring without a delocalised π loop | hexane, cyclohexane |
| Alicyclic | Cyclic but behaving like the corresponding aliphatic compound | cyclohexene |
| Aromatic | Contains a benzene ring or another Hückel π system | benzene, toluene, naphthalene, pyridine |

Aromatic compounds that contain a benzene ring are called **benzenoid**
(benzene, naphthalene, anthracene); those that are aromatic without one are
**non-benzenoid** (tropylium ion, azulene, furan).

### The characteristics that define the class

1. **Cyclic, planar and fully conjugated.** Every ring atom is sp² hybridised
   and carries one unhybridised p orbital perpendicular to the ring plane, so
   the loop of overlap is unbroken.
2. **(4n + 2) π electrons** in that loop — Hückel's rule, the subject of the
   next section.
3. **Unusually stable.** Benzene's measured heat of hydrogenation is about
   152 kJ mol⁻¹ less than the calculation for three isolated double bonds. That
   deficit is the **resonance energy** (delocalisation energy).
4. **Substitution, not addition, is the normal reaction.** Addition would
   destroy the delocalised loop, so an aromatic ring gives up a hydrogen instead
   of opening a double bond. Addition happens only under forcing conditions.
5. **Equal carbon–carbon bond lengths.** All six C—C bonds in benzene are
   139 pm — between a single bond (154 pm) and a double bond (134 pm).
6. **High carbon content**, so aromatic compounds burn with a **sooty, luminous
   flame** — a quick laboratory clue.
7. **Resistant to oxidation.** The ring survives hot KMnO₄; in an alkylbenzene
   the side chain is oxidised instead, leaving the ring intact.

::: definition Aromaticity
A cyclic, planar, fully conjugated system containing (4n + 2) delocalised π
electrons, where n = 0, 1, 2, 3, …, is **aromatic**. It is more stable than the
corresponding open-chain conjugated system by its resonance energy.
:::

## 15.2 Huckel's rule of aromaticity

Erich Hückel showed in 1931 that the stability of a monocyclic conjugated ring
depends on how many π electrons it holds. The rule has three conditions and a
count, and **all four must be satisfied**.

1. The molecule must be **cyclic**.
2. It must be **planar**, so the p orbitals are parallel.
3. Every atom of the ring must be able to contribute a p orbital, i.e. the
   conjugation must be **complete and uninterrupted**.
4. The number of delocalised π electrons must equal **4n + 2** where
   n = 0, 1, 2, 3, … — that is 2, 6, 10, 14, …

A ring that meets the first three conditions but holds **4n** π electrons
(4, 8, 12, …) is **antiaromatic** — it is *less* stable than the open chain, and
molecules usually escape that fate by buckling out of the plane. A ring that
fails a structural condition is simply **non-aromatic**.

```figure caption="Hückel's rule at work. Counting π electrons in the ring settles all three cases: 4n electrons destabilise, 4n+2 stabilise, and a ring that cannot stay flat is simply out of the competition."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 4, figsize=(5.2,2.4))

def poly(ax, n, r=1.0, rot=90, col=INK, lw=1.5):
    ang = np.radians(rot) + np.arange(n)*2*np.pi/n
    x, y = r*np.cos(ang), r*np.sin(ang)
    for i in range(n):
        j = (i+1) % n
        ax.plot([x[i], x[j]], [y[i], y[j]], color=col, lw=lw, zorder=2)
    return x, y

def dbond(ax, x, y, i, j, f=0.76, t=0.18, col=INK, lw=1.3):
    ix0, iy0 = x[i]*f, y[i]*f
    ix1, iy1 = x[j]*f, y[j]*f
    dx, dy = ix1-ix0, iy1-iy0
    ax.plot([ix0+dx*t, ix1-dx*t], [iy0+dy*t, iy1-dy*t], color=col, lw=lw)

def frame(ax, title, col):
    ax.set_title(title, fontsize=6.9, color=col, pad=5, linespacing=1.45)
    ax.set_xlim(-1.55, 1.55); ax.set_ylim(-1.45, 1.45)
    ax.set_aspect('equal'); ax.axis('off')

x, y = poly(axes[0], 4, 0.95, rot=45)
dbond(axes[0], x, y, 0, 1); dbond(axes[0], x, y, 2, 3)
frame(axes[0], 'cyclobutadiene\n4 π  (4n)\nANTIAROMATIC', '#d9534f')

x, y = poly(axes[1], 6, 1.05)
axes[1].add_patch(plt.Circle((0, 0), 0.62, fill=False, ec=ACCENT, lw=1.4))
frame(axes[1], 'benzene\n6 π  (4n+2, n=1)\nAROMATIC', '#2e8b57')

x, y = poly(axes[2], 5, 1.02)
axes[2].add_patch(plt.Circle((0, 0), 0.58, fill=False, ec=ACCENT, lw=1.4))
axes[2].text(0, 0, '−', fontsize=12, color=ACCENT, ha='center', va='center')
frame(axes[2], 'cyclopentadienyl anion\n6 π  (4n+2)\nAROMATIC', '#2e8b57')

x, y = poly(axes[3], 8, 1.05, rot=67.5)
for i in (0, 2, 4, 6):
    dbond(axes[3], x, y, i, i+1, f=0.80)
frame(axes[3], 'cyclooctatetraene\n8 π, tub-shaped\nNON-AROMATIC', MUTED)
fig.tight_layout()
```

::: example Applying Hückel's rule
**Classify each species as aromatic, antiaromatic or non-aromatic.**
(i) cyclopropenyl cation C₃H₃⁺  (ii) cyclopentadienyl cation C₅H₅⁺
(iii) tropylium (cycloheptatrienyl) cation C₇H₇⁺  (iv) cyclohexane
(v) naphthalene C₁₀H₈

**Method.** Check planar + cyclic + full conjugation first, then count only the
electrons **in the ring π system**. A positive carbon contributes an empty p
orbital (0 electrons); a negative carbon contributes a lone pair (2 electrons);
each C=C contributes 2.

(i) Three-membered ring, one C=C (2 π) and one C⁺ (empty p orbital) — cyclic,
planar, conjugated. π electrons = **2** = 4n + 2 with n = 0 → **aromatic**. This
is why the cyclopropenyl cation is surprisingly easy to make.

(ii) Five-membered ring, two C=C (4 π) and one C⁺ (0) — π electrons = **4** =
4n with n = 1 → **antiaromatic**, and indeed it is extremely unstable. Contrast
this with the *anion* in the figure, which has 6 π and is aromatic.

(iii) Seven-membered ring, three C=C (6 π) and one C⁺ (0) — π electrons =
**6** → **aromatic**. Tropylium bromide is an ionic, water-soluble solid, which
is remarkable for a hydrocarbon salt.

(iv) Cyclohexane has no p orbitals at all — condition 3 fails, so it is
**non-aromatic** (not antiaromatic).

(v) Naphthalene, two fused rings, five C=C → **10 π** = 4n + 2 with n = 2 →
**aromatic**. Hückel's rule was derived for monocyclic rings, so for fused
systems it is applied as a useful approximation rather than a proof.
:::

::: caution Count the ring electrons only
A lone pair counts **only if it sits in a p orbital that is part of the loop**.
In pyridine the nitrogen lone pair lies in an sp² orbital *in* the ring plane,
so it is not counted — pyridine has 6 π electrons from its three C=C/C=N bonds
and is aromatic. In pyrrole the nitrogen lone pair *is* in the p orbital, so it
joins the loop: 4 (from two C=C) + 2 = 6 π, again aromatic.
:::

## 15.3 Kekule structure of benzene

Benzene was isolated by Faraday in 1825 from compressed illuminating gas, and
its formula C₆H₆ was quickly established. That formula implies four degrees of
unsaturation, which for years nobody could draw. In 1865 **August Kekulé**
proposed a planar hexagonal ring of six carbons, each carrying one hydrogen,
with three alternating single and double bonds.

```figure caption="The Kekulé structures and what replaced them. The double-headed arrow is not an equilibrium: benzene is one substance whose π electrons are spread evenly, drawn as a hexagon with an inner circle."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(2, 1, figsize=(5.0,3.6),
                         gridspec_kw={'height_ratios': [1.25, 1.0]})

ax = axes[0]
ax.set_xlim(0, 10); ax.set_ylim(-2.0, 2.0)
ax.set_aspect('equal'); ax.axis('off')

def ring(ax, cx, cy, r=0.95, dbl=None, circle=False, col=INK):
    ang = np.arange(6)*np.pi/3 + np.pi/6
    x, y = cx + r*np.cos(ang), cy + r*np.sin(ang)
    for i in range(6):
        j = (i+1) % 6
        ax.plot([x[i], x[j]], [y[i], y[j]], color=col, lw=1.5, zorder=2)
    if circle:
        ax.add_patch(plt.Circle((cx, cy), r*0.58, fill=False, ec=ACCENT, lw=1.4))
    for (i, j) in (dbl or []):
        f, t = 0.76, 0.18
        ix0, iy0 = cx + (x[i]-cx)*f, cy + (y[i]-cy)*f
        ix1, iy1 = cx + (x[j]-cx)*f, cy + (y[j]-cy)*f
        dx, dy = ix1-ix0, iy1-iy0
        ax.plot([ix0+dx*t, ix1-dx*t], [iy0+dy*t, iy1-dy*t], color=col, lw=1.3)
    return x, y

ring(ax, 1.55, 0.05, dbl=[(0, 1), (2, 3), (4, 5)])
ring(ax, 5.00, 0.05, dbl=[(1, 2), (3, 4), (5, 0)])
ring(ax, 8.45, 0.05, circle=True)
for xa in (3.28, 6.73):
    ax.text(xa, 0.05, '↔', fontsize=15, color=MUTED, ha='center', va='center')
for xa, lab in ((1.55, 'Kekulé I'), (5.00, 'Kekulé II'),
                (8.45, 'resonance hybrid')):
    ax.text(xa, -1.55, lab, fontsize=7.4, color=INK, ha='center', va='center')

ax = axes[1]
ax.set_xlim(0, 10); ax.set_ylim(-1.6, 1.6)
ax.set_aspect('equal'); ax.axis('off')
from matplotlib.patches import Ellipse
xs = np.linspace(2.6, 7.4, 6)
ax.plot([2.3, 7.7], [0, 0], color=INK, lw=1.6)
for xc in xs:
    ax.plot(xc, 0, marker='o', ms=3.4, color=INK, zorder=3)
    for yc in (0.50, -0.50):
        ax.add_patch(Ellipse((xc, yc), 0.40, 0.66, fill=False, ec=MUTED,
                             lw=0.8, ls=(0, (2, 2))))
for yc in (0.62, -0.62):
    ax.add_patch(Ellipse((5.0, yc), 6.0, 0.88, fill=False, ec=ACCENT, lw=1.3))
ax.text(5.0, -1.34, 'the six parallel p orbitals overlap sideways, giving one π '
        'cloud above\nand one below the ring — the electrons belong to all six '
        'carbons', fontsize=7.0, color=MUTED, ha='center', va='center',
        linespacing=1.5)
fig.tight_layout()
```

### What the Kekulé structure explains

- The formula C₆H₆ and the fact that benzene adds exactly **three** molecules of
  hydrogen to give cyclohexane.
- Only **one** monosubstituted product, C₆H₅X, is ever obtained — all six
  hydrogens are equivalent, which a symmetrical ring accounts for.
- Complete ozonolysis of benzene gives **three** molecules of glyoxal, exactly
  as three C=C bonds require:

C₆H₆ + 3O₃ → benzene triozonide, then triozonide + 3H₂O --Zn--> 3 OHC—CHO

### What it fails to explain

- Benzene does **not** decolourise bromine water or Baeyer's reagent, although
  it is drawn with three double bonds.
- Its heat of hydrogenation is far too small (see §15.4).
- The C—C bond lengths are all **139 pm**, not alternating 134 and 154 pm.
- Kekulé's own structure predicts **two** different ortho-disubstituted
  products (one with a double bond between the substituted carbons and one
  without). Only one is ever isolated.

Kekulé tried to rescue the theory with his **oscillation hypothesis** — the two
arrangements interconvert so fast that no experiment can catch them apart. The
modern answer is better and simpler: benzene is not either structure. It is a
single substance, the **resonance hybrid**, in which the six π electrons are
delocalised over the whole ring.

::: memory Why the circle is drawn
Hexagon + inner circle = six carbons, six hydrogens (understood), and six π
electrons belonging to nobody in particular. Use the Kekulé form when you need
to *push arrows* in a mechanism, and the circle form everywhere else.
:::

## 15.4 Resonance and isomerism

### Resonance and resonance energy

Benzene is a resonance hybrid of the two Kekulé structures. Resonance lowers the
energy, and the size of that lowering can be measured by **hydrogenation**.

| Compound | C=C bonds | ΔH of hydrogenation (kJ mol⁻¹) |
|---|---|---|
| Cyclohexene | 1 | −120 |
| Cyclohexa-1,3-diene | 2 | −232 (expected −240) |
| Hypothetical "cyclohexatriene" | 3 | −360 (calculated, 3 × −120) |
| **Benzene (measured)** | — | **−208** |

```figure caption="Resonance energy of benzene from heats of hydrogenation. Every compound falls to the same product, cyclohexane, so the vertical gaps compare the starting materials directly. Benzene sits 152 kJ mol⁻¹ lower than three isolated double bonds would."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,3.0))
ax.set_xlim(0, 10); ax.set_ylim(-70, 430)
ax.axis('off')

def level(x0, x1, e, lab, col, lw=2.0):
    ax.plot([x0, x1], [e, e], color=col, lw=lw, solid_capstyle='butt')
    ax.text((x0+x1)/2, e + 16, lab, fontsize=7.0, color=col, ha='center',
            va='bottom', linespacing=1.4)

ax.plot([0.4, 9.6], [0, 0], color=MUTED, lw=1.6, solid_capstyle='butt')
ax.text(5.0, -22, 'cyclohexane  (the common product, taken as zero)',
        fontsize=7.0, color=MUTED, ha='center', va='top')
level(0.9, 2.6, 120, 'cyclohexene\n−120', '#2e8b57')
level(3.2, 4.9, 232, 'cyclohexa-1,3-diene\n−232', '#b8860b')
level(5.5, 8.4, 360, '"cyclohexatriene"\ncalculated −360', '#d9534f')
level(5.5, 9.2, 208, '', ACCENT)
ax.text(5.5, 192, 'benzene, measured −208', fontsize=7.0, color=ACCENT,
        ha='left', va='top')

ax.annotate('', xy=(8.75, 360), xytext=(8.75, 208),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=1.2,
                            mutation_scale=9))
ax.text(8.58, 284, 'resonance energy\n152 kJ mol⁻¹', fontsize=7.2, color=INK,
        ha='right', va='center', linespacing=1.45)
ax.annotate('', xy=(1.75, 8), xytext=(1.75, 114),
            arrowprops=dict(arrowstyle='-|>', color='#2e8b57', lw=1.0,
                            mutation_scale=8))
ax.annotate('', xy=(6.9, 8), xytext=(6.9, 202),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.0,
                            mutation_scale=8))
ax.text(0.4, 412, 'energy →', fontsize=7.0, color=MUTED, ha='left', va='center')
fig.tight_layout()
```

The gap of **152 kJ mol⁻¹** between the calculated and measured values is the
**resonance energy** of benzene. It is a stability *credit*: to make benzene
react by addition you must first pay that credit back, which is why benzene is
so reluctant to add and so willing to substitute.

::: key Rules for resonance structures
The contributing structures differ **only in the position of electrons** — the
nuclei never move. Each must have the same number of unpaired electrons and the
same overall charge. The real molecule is the hybrid, and it is **more stable
than the most stable single contributor**. A resonance hybrid is not a mixture
and not an equilibrium.
:::

### Isomerism in benzene derivatives

Because all six positions are equivalent, benzene gives exactly **one**
monosubstituted product C₆H₅X. Put a second substituent on and the picture
changes: three positional isomers become possible.

| Isomer | Positions | Prefix | Example, C₆H₄Cl₂ |
|---|---|---|---|
| ortho (o-) | 1, 2 — adjacent | o- | 1,2-dichlorobenzene |
| meta (m-) | 1, 3 — one carbon apart | m- | 1,3-dichlorobenzene |
| para (p-) | 1, 4 — opposite | p- | 1,4-dichlorobenzene |

```figure caption="The three disubstituted isomers. The hexagon has only three distinct relationships between two positions, which is why a disubstituted benzene has exactly three isomers, not six."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 3, figsize=(5.2,2.3))

def sring(ax, marks, title, lab='Cl'):
    ang = np.arange(6)*np.pi/3 + np.pi/6
    x, y = np.cos(ang), np.sin(ang)
    for i in range(6):
        j = (i+1) % 6
        ax.plot([x[i], x[j]], [y[i], y[j]], color=INK, lw=1.5)
    ax.add_patch(plt.Circle((0, 0), 0.50, fill=False, ec=ACCENT, lw=1.3))
    for k, idx in enumerate(marks):
        ax.plot([x[idx]*1.02, x[idx]*1.30], [y[idx]*1.02, y[idx]*1.30],
                color=INK, lw=1.3)
        ax.text(x[idx]*1.62, y[idx]*1.62, lab, fontsize=8.6, color='#d9534f',
                ha='center', va='center')
    for idx, num in zip(marks, ('1', '2')):
        ax.text(x[idx]*0.80, y[idx]*0.80, num, fontsize=6.6, color=MUTED,
                ha='center', va='center')
    ax.set_title(title, fontsize=7.6, color=INK, pad=6, linespacing=1.45)
    ax.set_xlim(-2.05, 2.05); ax.set_ylim(-1.95, 1.95)
    ax.set_aspect('equal'); ax.axis('off')

sring(axes[0], [1, 2], 'ortho  (1,2)\n1,2-dichlorobenzene')
sring(axes[1], [1, 3], 'meta  (1,3)\n1,3-dichlorobenzene')
sring(axes[2], [1, 4], 'para  (1,4)\n1,4-dichlorobenzene')
fig.tight_layout()
```

Counting quickly: for **trisubstituted** benzene C₆H₃X₃ there are again three
isomers — 1,2,3 (vicinal), 1,2,4 (asymmetrical) and 1,3,5 (symmetrical). For
C₆H₄XY, with two *different* groups, there are still three (o, m, p).

## 15.5 Preparation of benzene from decarboxylation of sodium benzoate, phenol, and ethyne

| Method | Reagents and conditions | Equation |
|---|---|---|
| Decarboxylation of sodium benzoate | Soda lime (NaOH + CaO), heat | C₆H₅COONa + NaOH --CaO, Δ--> C₆H₆ + Na₂CO₃ |
| Reduction of phenol | Zinc dust, distil | C₆H₅OH + Zn --Δ--> C₆H₆ + ZnO |
| Cyclic polymerisation of ethyne | Red-hot iron or quartz tube, 873 K | 3C₂H₂ --Fe tube, 873 K--> C₆H₆ |
| Hydrolysis of benzenesulphonic acid | Superheated steam, 423 K | C₆H₅SO₃H + H₂O --Δ--> C₆H₆ + H₂SO₄ |
| Industrial source | Fractional distillation of coal tar (353–443 K cut) | — |

**Decarboxylation.** Heating the sodium salt of any carboxylic acid with soda
lime removes the —COONa group as carbonate and puts a hydrogen in its place.
Soda lime is used rather than NaOH alone because it is a free-flowing solid that
does not attack glass at the temperature needed.

**Reduction of phenol.** Zinc dust strips the oxygen out of phenol; the zinc is
oxidised to ZnO. This is the standard laboratory route when phenol is on hand.

**From ethyne.** Three molecules of ethyne polymerise on the surface of a
red-hot iron tube. This is the reaction that first showed benzene could be built
from a two-carbon unit, and it is a favourite examination question because it
links Units 14 and 15.

::: caution Balance the decarboxylation properly
Students commonly write C₆H₅COONa + NaOH → C₆H₆ + CO₂. Count the sodiums: the
left has two, the right has none. The carbon leaves as **sodium carbonate**,
Na₂CO₃, not as carbon dioxide.
:::

## 15.6 Physical properties of benzene

| Property | Value or description |
|---|---|
| State and appearance | Colourless, mobile liquid |
| Odour | Characteristic sweet aromatic smell |
| Boiling point | 353 K (80 °C) |
| Melting point | 278.5 K (5.5 °C) — freezes on a cold day |
| Density | 0.879 g cm⁻³ at 293 K, so it floats on water |
| Solubility | Insoluble in water; miscible with ether, alcohol, CCl₄, and itself an excellent solvent for fats, resins, rubber and iodine |
| Combustion | Burns with a **sooty, luminous flame** (92.3 % carbon by mass) |
| Toxicity | Highly toxic; prolonged exposure to the vapour causes leukaemia — benzene is a proven **carcinogen** and is no longer used as a school solvent |
| Other | Non-polar (zero dipole moment, from its symmetry); forms a low-boiling azeotrope with water at 342 K |

The zero dipole moment is itself evidence for the regular hexagonal structure:
the six identical C—H bond moments cancel exactly in pairs only if the ring is a
regular planar hexagon.

## 15.7 Chemical properties: addition (hydrogen, halogen); electrophilic substitution and orientation of benzene derivatives (o, m, p); nitration; sulphonation; halogenation; Friedel-Crafts reaction (alkylation and acylation); combustion; uses

### Addition reactions

Addition destroys the aromatic sextet, so it needs forcing conditions — high
pressure with a catalyst, or ultraviolet light.

**Hydrogenation.** C₆H₆ + 3H₂ --Ni, 473–573 K--> C₆H₁₂ (cyclohexane)

**Halogenation (addition).** In bright sunlight, and with **no** halogen
carrier present, chlorine adds by a free-radical route:

C₆H₆ + 3Cl₂ --UV light--> C₆H₆Cl₆

The product, benzene hexachloride (BHC, gammexane or lindane), was once a
widely used insecticide and is now banned in most countries for its
persistence. Note the contrast that examiners love: **sunlight gives addition,
a Lewis-acid catalyst in the dark gives substitution.**

### The mechanism of electrophilic substitution

Every ring substitution of benzene — nitration, sulphonation, halogenation,
alkylation, acylation — follows the same three steps.

1. **Generate the electrophile.** A reagent plus a catalyst produces a strongly
   electron-poor species, E⁺.
2. **Attack by the π cloud.** Two of the six delocalised electrons attack E⁺,
   giving a positively charged, non-aromatic intermediate called the **arenium
   ion** (or σ-complex, or carbocation intermediate). This step is slow — it is
   the rate-determining step, because aromaticity is temporarily lost.
3. **Lose a proton.** A base removes H⁺ from the sp³ carbon, the electron pair
   falls back into the ring, and **aromaticity is restored**. This step is fast
   and it is the reason substitution beats addition: the alternative, adding a
   nucleophile to the arenium ion, would leave the ring permanently
   non-aromatic.

```figure caption="Nitration of benzene, the standard example of electrophilic aromatic substitution. The slow step is the attack on NO₂⁺, which costs the ring its aromaticity; losing H⁺ is fast because it gives the aromatic sextet back."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
fig, axes = plt.subplots(1, 3, figsize=(5.2,2.6))

def hexa(ax, r=0.92):
    ang = np.arange(6)*np.pi/3 + np.pi/6
    x, y = r*np.cos(ang), r*np.sin(ang)
    for i in range(6):
        j = (i+1) % 6
        ax.plot([x[i], x[j]], [y[i], y[j]], color=INK, lw=1.5, zorder=2)
    return x, y

def inner(ax, x, y, i, j, f=0.76, t=0.18):
    ix0, iy0 = x[i]*f, y[i]*f
    ix1, iy1 = x[j]*f, y[j]*f
    dx, dy = ix1-ix0, iy1-iy0
    ax.plot([ix0+dx*t, ix1-dx*t], [iy0+dy*t, iy1-dy*t], color=INK, lw=1.3)

def frame(ax, title):
    ax.set_title(title, fontsize=7.2, color=INK, pad=5)
    ax.set_xlim(-1.75, 1.75); ax.set_ylim(-1.60, 2.30)
    ax.set_aspect('equal'); ax.axis('off')

ax = axes[0]
hexa(ax)
ax.add_patch(plt.Circle((0, 0), 0.54, fill=False, ec=ACCENT, lw=1.3))
ax.text(0.10, 1.90, 'NO₂⁺', fontsize=9.6, color='#d9534f', ha='center',
        va='center')
ax.add_patch(FancyArrowPatch((0.42, 0.42), (-0.05, 1.58),
                             connectionstyle='arc3,rad=0.42', color='#d9534f',
                             arrowstyle='-|>', mutation_scale=9, lw=1.2))
ax.text(0, -1.40, 'slow, aromaticity lost', fontsize=6.8, color=MUTED,
        ha='center', va='center')
frame(ax, '(a) π cloud attacks NO₂⁺')

ax = axes[1]
x, y = hexa(ax)
inner(ax, x, y, 2, 3); inner(ax, x, y, 5, 0)
ax.plot([x[1], x[1]-0.52], [y[1], y[1]+0.42], color=INK, lw=1.3)
ax.plot([x[1], x[1]+0.52], [y[1], y[1]+0.42], color=INK, lw=1.3)
ax.text(x[1]-0.80, y[1]+0.62, 'H', fontsize=8.6, color=INK, ha='center',
        va='center')
ax.text(x[1]+0.90, y[1]+0.62, 'NO₂', fontsize=8.6, color='#d9534f',
        ha='center', va='center')
ax.text(x[4]*0.58, y[4]*0.58, '+', fontsize=11, color=ACCENT, ha='center',
        va='center')
for idx in (0, 2):
    ax.text(x[idx]*1.48, y[idx]*1.48, 'δ+', fontsize=7.0, color=ACCENT,
            ha='center', va='center')
ax.text(0, -1.40, 'charge on 3 carbons (o, o, p)', fontsize=6.8, color=MUTED,
        ha='center', va='center')
frame(ax, '(b) arenium ion')

ax = axes[2]
x, y = hexa(ax)
ax.add_patch(plt.Circle((0, 0), 0.54, fill=False, ec=ACCENT, lw=1.3))
ax.plot([x[1], x[1]], [y[1], y[1]+0.44], color=INK, lw=1.3)
ax.text(0.42, 1.80, 'NO₂', fontsize=9.0, color='#d9534f', ha='center',
        va='center')
ax.text(-1.72, 1.30, '− H⁺, removed\nby HSO₄⁻', fontsize=6.8, color='#2e8b57',
        ha='left', va='center', linespacing=1.4)
ax.text(0, -1.40, 'fast, aromaticity restored', fontsize=6.8, color='#2e8b57',
        ha='center', va='center')
frame(ax, '(c) nitrobenzene')
fig.tight_layout()
```

### Nitration

C₆H₆ + HNO₃ (conc.) --conc. H₂SO₄, 330 K--> C₆H₅NO₂ + H₂O

The mixture of concentrated nitric and sulphuric acids is the **nitrating
mixture**. Sulphuric acid, being the stronger acid, protonates nitric acid and
strips water from it to release the electrophile, the **nitronium ion**:

HNO₃ + 2H₂SO₄ ⇌ NO₂⁺ + H₃O⁺ + 2HSO₄⁻

Above about 330 K a second nitro group enters, and because —NO₂ is
meta-directing the product is **1,3-dinitrobenzene**.

### Sulphonation

C₆H₆ + H₂SO₄ (fuming) --Δ--> C₆H₅SO₃H + H₂O

Fuming sulphuric acid (oleum) is used because the electrophile is **sulphur
trioxide**, SO₃, whose sulphur carries a large partial positive charge:

2H₂SO₄ ⇌ SO₃ + H₃O⁺ + HSO₄⁻

Sulphonation is the one electrophilic substitution that is readily
**reversible** — boiling benzenesulphonic acid with superheated steam gives
benzene back, which is the preparation listed in §15.5.

### Halogenation (substitution)

C₆H₆ + Cl₂ --anhydrous AlCl₃, dark--> C₆H₅Cl + HCl

C₆H₆ + Br₂ --anhydrous FeBr₃, dark--> C₆H₅Br + HBr

The Lewis acid is called a **halogen carrier**. It polarises the halogen
molecule and pulls one atom off as the electrophile:

Cl₂ + AlCl₃ → Cl⁺ + AlCl₄⁻

Iodination needs an oxidising agent (HIO₃ or HNO₃) to remove the HI as it forms,
because the reaction is reversible; fluorination is far too violent to control.

### Friedel–Crafts reactions

Both are run in the dark with **anhydrous aluminium chloride**; the smallest
trace of moisture destroys the catalyst.

**Alkylation** puts an alkyl group on the ring:

C₆H₆ + CH₃Cl --anhyd. AlCl₃--> C₆H₅CH₃ + HCl  (toluene)

CH₃Cl + AlCl₃ → CH₃⁺ + AlCl₄⁻

**Acylation** puts an acyl group on the ring:

C₆H₆ + CH₃COCl --anhyd. AlCl₃--> C₆H₅COCH₃ + HCl  (acetophenone)

CH₃COCl + AlCl₃ → CH₃CO⁺ + AlCl₄⁻

| Reaction | Reagent | Catalyst | Electrophile | Product |
|---|---|---|---|---|
| Nitration | conc. HNO₃ | conc. H₂SO₄, 330 K | NO₂⁺ | nitrobenzene |
| Sulphonation | fuming H₂SO₄ | — (SO₃ in oleum) | SO₃ | benzenesulphonic acid |
| Chlorination | Cl₂ | anhyd. AlCl₃, dark | Cl⁺ | chlorobenzene |
| Bromination | Br₂ | anhyd. FeBr₃, dark | Br⁺ | bromobenzene |
| Alkylation | CH₃Cl | anhyd. AlCl₃ | CH₃⁺ | toluene |
| Acylation | CH₃COCl | anhyd. AlCl₃ | CH₃CO⁺ | acetophenone |

::: caution Two limits of Friedel–Crafts alkylation
The alkyl group it installs is electron-releasing, so the product is *more*
reactive than benzene and **polyalkylation** is hard to avoid. Worse, the
carbocation can rearrange: benzene with 1-chloropropane gives mostly
**isopropylbenzene (cumene)**, not propylbenzene, because CH₃CH₂CH₂⁺ shifts a
hydride to become the more stable (CH₃)₂CH⁺. Acylation has neither problem —
the acylium ion is resonance-stabilised and does not rearrange, and the ketone
product is deactivated. This is why the standard way to make an alkylbenzene is
to acylate first and then reduce.
:::

### Combustion

2C₆H₆ + 15O₂ → 12CO₂ + 6H₂O   ΔH = −3268 kJ mol⁻¹ per mole of benzene

In a limited supply of air the high carbon content shows itself as the
characteristic sooty flame. Controlled catalytic oxidation gives a useful
industrial product:

2C₆H₆ + 9O₂ --V₂O₅, 723 K--> 2C₄H₂O₃ + 4CO₂ + 4H₂O  (maleic anhydride)

### Orientation of benzene derivatives

Once one group is on the ring it decides **where the next one goes** and
**how fast** the reaction runs. The group changes the electron density at the
ortho, meta and para positions through its inductive and resonance effects
(Unit 13), and the incoming electrophile goes wherever the electron density —
and the stability of the resulting arenium ion — is greatest.

```figure caption="Orientation explained by electron density. A +R group pumps electron density into the ortho and para positions, so the electrophile goes there; a −R group drains those same positions, leaving meta as the least unfavourable site."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
fig, axes = plt.subplots(1, 2, figsize=(5.0,2.6))

def scene(ax, group, gcol, marks, mcol, msym, hits, title, note):
    ang = np.arange(6)*np.pi/3 + np.pi/6
    x, y = np.cos(ang), np.sin(ang)
    for i in range(6):
        j = (i+1) % 6
        ax.plot([x[i], x[j]], [y[i], y[j]], color=INK, lw=1.5)
    ax.add_patch(plt.Circle((0, 0), 0.56, fill=False, ec=ACCENT, lw=1.3))
    ax.plot([x[1], x[1]], [y[1], y[1]+0.40], color=INK, lw=1.3)
    ax.text(0, 1.72, group, fontsize=9.2, color=gcol, ha='center', va='center')
    for idx in marks:
        ax.text(x[idx]*1.54, y[idx]*1.54, msym, fontsize=8.0, color=mcol,
                ha='center', va='center')
    for idx in hits:
        ax.text(x[idx]*1.60, y[idx]*1.60, 'E⁺', fontsize=8.0, color='#2e8b57',
                ha='center', va='center')
    ax.add_patch(FancyArrowPatch((-0.16, 1.48), (-0.62, 0.68),
                                 connectionstyle='arc3,rad=0.34', color=gcol,
                                 arrowstyle='-|>', mutation_scale=8, lw=1.1))
    ax.text(0, -2.10, note, fontsize=6.8, color=MUTED, ha='center',
            va='top', linespacing=1.45)
    ax.set_title(title, fontsize=7.4, color=INK, pad=5)
    ax.set_xlim(-2.05, 2.05); ax.set_ylim(-2.85, 2.15)
    ax.set_aspect('equal'); ax.axis('off')

scene(axes[0], '—OH', '#2e8b57', [0, 2, 4], '#d9534f', 'δ−', [],
      'phenol:  +R group',
      'density raised at the marked o and p carbons\n→ o,p-directing and '
      'activating')
scene(axes[1], '—NO₂', '#d9534f', [0, 2, 4], ACCENT, 'δ+', [3, 5],
      'nitrobenzene:  −R group',
      'o and p drained, so E⁺ goes to meta\n→ m-directing and deactivating')
fig.tight_layout()
```

| Type | Groups | Effect on rate | Directs to |
|---|---|---|---|
| Activating, o,p-directing | —OH, —O⁻, —OR, —NH₂, —NHR, —NR₂, —NHCOCH₃, —R (alkyl), —C₆H₅ | faster than benzene | ortho + para |
| Deactivating, o,p-directing | —F, —Cl, —Br, —I | slower than benzene | ortho + para |
| Deactivating, m-directing | —NO₂, —CN, —CHO, —COR, —COOH, —COOR, —SO₃H, —CCl₃, —N⁺R₃ | slower than benzene | meta |

The halogens are the exception that always appears in the examination. A
halogen has a strong **−I** effect, which drains the whole ring and makes the
reaction slow; but it also has a weak **+R** effect through its lone pairs,
which feeds density back specifically to the ortho and para positions. Rate is
governed by the stronger effect (−I, so deactivating); orientation is governed
by the position-selective effect (+R, so o,p-directing).

::: memory Sorting a substituent in two seconds
If the atom joined to the ring carries a **lone pair** (O, N, halogen) the group
is **o,p-directing**. If that atom carries a **double or triple bond to a more
electronegative atom**, or a **full positive charge** (—NO₂, —CHO, —COOH, —CN,
—SO₃H, —N⁺R₃), the group is **m-directing**. Alkyl and aryl groups are
o,p-directing by +I and hyperconjugation.
:::

Ortho and para products are formed together, and they are separated by their
physical properties — the para isomer is usually the more symmetrical, higher
melting solid, while the ortho isomer, which can hydrogen bond internally, is
often a lower boiling liquid. Bulky groups push the mixture towards para.

### Uses of benzene and its derivatives

- Solvent for fats, waxes, resins, rubber and iodine (now heavily restricted on
  health grounds).
- Feedstock for **styrene** (→ polystyrene), **phenol** via cumene, **aniline**
  via nitrobenzene, and **cyclohexane** (→ nylon-6,6).
- Manufacture of dyes, drugs (aspirin, paracetamol), explosives (TNT from
  toluene) and detergents (alkylbenzenesulphonates).
- Formerly added to petrol as an anti-knock agent; replaced because of its
  toxicity.

::: example Predicting orientation and the product
**Predict the major monosubstitution product, and say whether the reaction is
faster or slower than for benzene.**
(i) nitration of toluene  (ii) nitration of nitrobenzene
(iii) bromination of chlorobenzene  (iv) nitration of benzoic acid

**Method.** Identify the group already on the ring, classify it from the table,
then apply the direction and the rate separately.

(i) —CH₃ is an **activating, o,p-director** (+I and hyperconjugation).
Nitration is therefore **faster** than for benzene and gives a mixture of
**2-nitrotoluene (o)** and **4-nitrotoluene (p)**, with only a trace of the meta
isomer. Conditions: conc. HNO₃ + conc. H₂SO₄ at 303–313 K — deliberately cooler
than for benzene, because toluene reacts more readily.

(ii) —NO₂ is a **strongly deactivating m-director**. Nitration is **much
slower** and needs fuming HNO₃ with conc. H₂SO₄ at about 373 K. The product is
**1,3-dinitrobenzene**.

(iii) —Cl deactivates by −I but directs by +R, so the reaction is **slower**
than for benzene yet still gives **1-chloro-2-bromobenzene** and
**1-chloro-4-bromobenzene**.

(iv) —COOH has a carbon doubly bonded to oxygen, so it is **deactivating and
m-directing**: the product is **3-nitrobenzoic acid**, formed slowly.
:::

::: example Resonance energy from thermochemical data
**The heat of hydrogenation of cyclohexene is −119.6 kJ mol⁻¹ and that of
benzene is −208.4 kJ mol⁻¹. Calculate the resonance energy of benzene. What
would the resonance energy be if benzene's measured value were −240 kJ mol⁻¹
instead?**

**Step 1 — the model compound.** Every hydrogenation ends at the same product,
cyclohexane, so the heats can be compared directly. One isolated C=C releases
119.6 kJ mol⁻¹ on hydrogenation.

**Step 2 — the calculated value for three isolated double bonds.**

ΔH(calculated) = 3 × (−119.6) = **−358.8 kJ mol⁻¹**

**Step 3 — compare with experiment.**

Resonance energy = ΔH(calculated) − ΔH(measured)
= (−358.8) − (−208.4) = **−150.4**, i.e. a stabilisation of **150.4 kJ mol⁻¹**

Benzene lies 150.4 kJ mol⁻¹ *below* where three separate double bonds would put
it, and that is the energy penalty any reaction must pay before it can break the
ring's delocalisation.

**Step 4 — the hypothetical case.** If benzene released 240 kJ mol⁻¹ the
resonance energy would be 358.8 − 240 = **118.8 kJ mol⁻¹**: still aromatic, but
noticeably less stabilised. The general point is that **the smaller the measured
heat of hydrogenation, the larger the resonance energy** — the molecule has
already "spent" some of its unsaturation on delocalisation.
:::

::: example A two-step synthesis with a yield calculation
**(a) Starting from benzene, prepare 1,3-dinitrobenzene, giving reagents and
conditions. (b) 39 g of benzene is nitrated and 49.2 g of nitrobenzene is
isolated. Calculate the percentage yield.**

**(a)** The first nitro group must go on before the second, because —NO₂ is the
group that directs the second one to the meta position.

Step 1: C₆H₆ + HNO₃ --conc. H₂SO₄, 330 K--> C₆H₅NO₂ + H₂O

Step 2: C₆H₅NO₂ + HNO₃ --fuming H₂SO₄, 373 K--> 1,3-C₆H₄(NO₂)₂ + H₂O

The harsher conditions in step 2 are needed because the ring has been
deactivated by the first nitro group. Note that the route **cannot** be
reversed: you cannot make 1,2- or 1,4-dinitrobenzene this way at all.

**(b)** Molar mass of benzene = (6 × 12) + (6 × 1) = **78 g mol⁻¹**
Molar mass of nitrobenzene C₆H₅NO₂ = 72 + 5 + 14 + 32 = **123 g mol⁻¹**

Moles of benzene = 39 / 78 = **0.50 mol**

The equation is 1 : 1, so the theoretical yield of nitrobenzene is
0.50 mol = 0.50 × 123 = **61.5 g**.

Percentage yield = (49.2 / 61.5) × 100 = **80 %**
:::

## Chapter summary

- **Aromatic** means cyclic, planar, fully conjugated and holding (4n + 2)
  delocalised π electrons. 4n electrons in the same geometry means
  **antiaromatic**; a broken conjugation or a non-planar ring means
  **non-aromatic**.
- Kekulé's alternating-bond hexagon explains the formula, the single
  monosubstituted product and the three molecules of glyoxal from ozonolysis,
  but not the equal 139 pm bond lengths, the refusal to add bromine, or the low
  heat of hydrogenation.
- Benzene is a **resonance hybrid** of the two Kekulé forms, stabilised by a
  **resonance energy of about 150 kJ mol⁻¹**.
- Benzene is made by decarboxylating sodium benzoate with soda lime, reducing
  phenol with zinc dust, or passing ethyne through a red-hot tube.
- The typical reaction is **electrophilic substitution** in three steps:
  generate E⁺, slow attack by the π cloud to give the **arenium ion**, fast loss
  of H⁺ to restore aromaticity.
- Nitration (NO₂⁺), sulphonation (SO₃), halogenation (X⁺ with a halogen
  carrier), Friedel–Crafts alkylation (R⁺) and acylation (RCO⁺) all share that
  mechanism.
- Addition needs forcing conditions: 3H₂/Ni gives cyclohexane, 3Cl₂ in sunlight
  gives benzene hexachloride.
- Groups with a **lone pair on the attached atom** are o,p-directing; groups
  with a **multiple bond to an electronegative atom or a positive charge** are
  m-directing. Halogens deactivate but still direct o,p.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Benzene does not decolourise bromine water because <span class="marks">[1]</span>
   (a) it is a liquid (b) its π electrons are delocalised and the ring is stabilised (c) bromine is insoluble in it (d) it has no hydrogen
2. Which species is antiaromatic? <span class="marks">[1]</span>
   (a) benzene (b) cyclopentadienyl anion (c) cyclobutadiene (d) tropylium cation
3. The electrophile in the nitration of benzene is <span class="marks">[1]</span>
   (a) HNO₃ (b) NO₂⁻ (c) NO₂⁺ (d) NO⁺
4. All six carbon–carbon bond lengths in benzene are <span class="marks">[1]</span>
   (a) 154 pm (b) 139 pm (c) 134 pm (d) 120 pm
5. Benzene is obtained when ethyne is passed through <span class="marks">[1]</span>
   (a) cold dilute KMnO₄ (b) a red-hot iron tube at 873 K (c) ammoniacal AgNO₃ (d) conc. H₂SO₄
6. Which group is meta-directing? <span class="marks">[1]</span>
   (a) —OH (b) —CH₃ (c) —Cl (d) —COOH
7. Friedel–Crafts reactions cannot be carried out in the presence of <span class="marks">[1]</span>
   (a) anhydrous AlCl₃ (b) moisture (c) an acyl chloride (d) benzene
8. The number of isomers of dichlorobenzene, C₆H₄Cl₂, is <span class="marks">[1]</span>
   (a) 2 (b) 3 (c) 4 (d) 6
9. Chlorine reacts with benzene in bright sunlight to give <span class="marks">[1]</span>
   (a) chlorobenzene (b) benzene hexachloride (c) o-dichlorobenzene (d) no reaction

::: note Answers to Group A
**1.** (b) — addition would destroy the aromatic sextet, and the resonance
energy makes that unfavourable.
**2.** (c) — 4 π electrons, i.e. 4n with n = 1.
**3.** (c) — the nitronium ion, generated by H₂SO₄ acting on HNO₃.
**4.** (b) — intermediate between a single and a double bond, as delocalisation
requires.
**5.** (b) — cyclic polymerisation, 3C₂H₂ → C₆H₆.
**6.** (d) — the carbon of —COOH is doubly bonded to oxygen, so the group is
−R and deactivating.
**7.** (b) — water destroys the anhydrous AlCl₃ catalyst.
**8.** (b) — ortho, meta and para only.
**9.** (b) — sunlight with no halogen carrier gives free-radical addition,
C₆H₆Cl₆.
:::

**Group B — Short answer (5 marks each)**

1. State Hückel's rule and its conditions. Apply it to cyclobutadiene, benzene,
   the cyclopentadienyl anion and cyclooctatetraene. <span class="marks">[5]</span>
2. Give three pieces of evidence that support the Kekulé structure of benzene
   and three that contradict it. <span class="marks">[5]</span>
3. What is resonance energy? How is the resonance energy of benzene obtained
   from heats of hydrogenation, and what does it explain about benzene's
   chemistry? <span class="marks">[5]</span>
4. How is benzene prepared from (i) sodium benzoate, (ii) phenol and
   (iii) ethyne? Give equations with conditions. <span class="marks">[5]</span>
5. Describe the mechanism of the nitration of benzene, naming the electrophile,
   the intermediate and the rate-determining step. <span class="marks">[5]</span>
6. What are Friedel–Crafts reactions? Write the alkylation and acylation of
   benzene with equations, and give two limitations of alkylation. <span class="marks">[5]</span>
7. Why is —NO₂ meta-directing while —OH is ortho–para directing? Explain in
   terms of the resonance effect. <span class="marks">[5]</span>
8. Chlorine is deactivating yet ortho–para directing. Explain this apparent
   contradiction. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** A cyclic, planar, fully conjugated ring with (4n + 2) delocalised π
electrons is aromatic. Cyclobutadiene 4 π = 4n, antiaromatic; benzene 6 π,
aromatic (n = 1); cyclopentadienyl anion 4 π from two C=C plus the lone pair =
6 π, aromatic; cyclooctatetraene 8 π = 4n and tub-shaped, therefore
non-aromatic.

**2.** *For*: it accounts for C₆H₆; benzene adds exactly 3H₂ to give
cyclohexane; ozonolysis gives three molecules of glyoxal; only one
monosubstituted product C₆H₅X exists. *Against*: benzene does not decolourise
bromine water or Baeyer's reagent; its heat of hydrogenation is 152 kJ mol⁻¹
too small; all six C—C bonds are 139 pm, not alternating; the structure predicts
two different ortho isomers but only one is found.

**3.** Resonance energy is the extra stability of the delocalised hybrid over
the most stable single contributing structure. ΔH for three isolated double
bonds = 3 × (−120) = −360 kJ mol⁻¹, while benzene measures −208 kJ mol⁻¹; the
difference, 152 kJ mol⁻¹, is the resonance energy. It explains why benzene
resists addition and prefers substitution, which restores the delocalised
system.

**5.** Step 1: HNO₃ + 2H₂SO₄ ⇌ NO₂⁺ + H₃O⁺ + 2HSO₄⁻. Step 2 (slow, rate
determining): the π cloud attacks NO₂⁺ to give the arenium ion (σ-complex), a
non-aromatic carbocation whose positive charge is delocalised over three
carbons. Step 3 (fast): HSO₄⁻ removes H⁺ from the sp³ carbon and aromaticity is
restored, giving C₆H₅NO₂.

**7.** In phenol the oxygen lone pair is delocalised into the ring (+R), and the
resonance structures put the negative charge specifically on the **ortho and
para** carbons, so the electrophile attacks there. In nitrobenzene the −NO₂
group withdraws density (−R), and the resonance structures put the **positive**
charge on the ortho and para carbons; the meta positions are least depleted, so
attack occurs there.

**8.** Chlorine exerts a strong −I effect, which withdraws density from the
whole ring and slows every electrophilic substitution — hence deactivating. It
also exerts a weak +R effect through its lone pairs, and that effect delivers
density **only** to the ortho and para positions. Rate is decided by the
stronger −I effect, orientation by the position-selective +R effect.
:::

**Group C — Long answer (8 marks each)**

1. (a) State Hückel's rule and explain, with reasons, why cyclobutadiene is
   antiaromatic, benzene is aromatic and cyclooctatetraene is non-aromatic. <span class="marks">[4]</span>
   (b) Discuss the Kekulé structure of benzene: what it explains, what it fails
   to explain, and how resonance resolves the difficulty. <span class="marks">[4]</span>
2. (a) Describe the general mechanism of electrophilic aromatic substitution,
   using nitration as the example. <span class="marks">[4]</span>
   (b) Write equations with reagents and conditions for the sulphonation,
   bromination, alkylation and acylation of benzene, naming the electrophile in
   each case. <span class="marks">[4]</span>
3. (a) Explain the terms *activating*, *deactivating*, *o,p-directing* and
   *m-directing*, giving two examples of each class. <span class="marks">[3]</span>
   (b) Predict the major product of (i) nitration of toluene, (ii) nitration of
   nitrobenzene, (iii) bromination of phenol. <span class="marks">[3]</span>
   (c) 7.8 g of benzene is completely burnt in oxygen. Calculate the volume of
   carbon dioxide produced at STP. <span class="marks">[2]</span>

::: note Answers to Group C
**1.** (a) Cyclobutadiene is planar, cyclic and conjugated but holds 4 π
electrons (4n), so it is destabilised relative to the open chain — antiaromatic.
Benzene holds 6 π (4n + 2 with n = 1) in a regular planar hexagon — aromatic.
Cyclooctatetraene has 8 π (4n) and escapes antiaromaticity by folding into a tub
shape; since it is no longer planar, its p orbitals cannot overlap all round the
ring and it behaves as an ordinary polyene — non-aromatic.

**2.** (b) Sulphonation: C₆H₆ + H₂SO₄ (fuming) --Δ--> C₆H₅SO₃H + H₂O,
electrophile SO₃. Bromination: C₆H₆ + Br₂ --anhyd. FeBr₃, dark--> C₆H₅Br + HBr,
electrophile Br⁺. Alkylation: C₆H₆ + CH₃Cl --anhyd. AlCl₃--> C₆H₅CH₃ + HCl,
electrophile CH₃⁺. Acylation: C₆H₆ + CH₃COCl --anhyd. AlCl₃--> C₆H₅COCH₃ + HCl,
electrophile CH₃CO⁺.

**3.** (b) (i) 2-nitrotoluene and 4-nitrotoluene — —CH₃ is activating and
o,p-directing. (ii) 1,3-dinitrobenzene — —NO₂ is deactivating and m-directing.
(iii) 2-bromophenol and 4-bromophenol with bromine in CS₂ at low temperature;
with **bromine water** the ring is so activated that 2,4,6-tribromophenol
precipitates as a white solid.

**3.** (c) The balanced equation is 2C₆H₆ + 15O₂ → 12CO₂ + 6H₂O.
Molar mass of benzene = 78 g mol⁻¹, so moles of benzene = 7.8 / 78 = 0.10 mol.
From the equation 2 mol of benzene gives 12 mol of CO₂, i.e. 1 mol gives 6 mol,
so moles of CO₂ = 6 × 0.10 = 0.60 mol.
Volume at STP = 0.60 × 22.4 = **13.44 dm³**.
:::
