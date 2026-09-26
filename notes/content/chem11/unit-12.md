---
subject: Chemistry
grade: 11
unit: 12
title: Basic Concept of Organic Chemistry
hours: 6
area: Organic Chemistry
---

More than twenty million compounds are known to chemistry, and over ninety per
cent of them are compounds of a single element — carbon. This unit is the door
into that enormous subject. It explains what makes carbon special, how its
compounds are sorted into families, how chemists draw and name them, and how the
crude oil pumped out of the ground is turned into the petrol and diesel that
reach the pumps in Nepal. Nothing here is difficult, but everything here is used
again in every organic chapter that follows.

::: key What the examiner asks from this unit
Learn to *draw* before you learn to talk. You must be able to convert between a
molecular formula, a condensed formula and a bond-line structure; write the IUPAC
name of any compound of up to six carbons; count and name the isomers of a given
formula; and define octane number and cetane number precisely. Those four skills
cover almost every question ever set on this unit.
:::

## 12.1 Introduction to organic chemistry and organic compounds

Until the early nineteenth century, chemists divided substances into *mineral*
compounds, obtained from rocks, and *organic* compounds, obtained only from
living things. Berzelius argued in 1807 that organic compounds could be made only
inside a plant or animal, under the influence of a mysterious **vital force**.

That idea was destroyed in 1828 by **Friedrich Wöhler**, who heated the purely
inorganic salt ammonium cyanate and obtained urea — a substance until then found
only in urine:

NH₄CNO --Δ--> NH₂CONH₂ (urea)

Kolbe synthesised acetic acid in 1845 and Berthelot made methane in 1856, and the
vital force theory was finished.

::: definition Organic chemistry
**Organic chemistry** is the branch of chemistry that deals with hydrocarbons and
their derivatives. An **organic compound** is a compound of carbon, other than
the oxides of carbon, carbonates and bicarbonates, cyanides, carbides and a few
other simple carbon compounds that are traditionally treated as inorganic.
:::

Note that the modern definition says nothing about living organisms. Petrol,
polythene, aspirin, DDT and nylon are all organic and none of them comes from a
living cell.

## 12.2 Reasons for separate study of organic compounds

Organic chemistry is studied as a separate branch for practical reasons, not
because carbon obeys different laws.

1. **Sheer number.** Over 20 million organic compounds are known against roughly
   half a million inorganic ones, and the list grows every day.
2. **Isomerism.** One molecular formula may stand for many different compounds.
   C₄H₁₀O alone represents seven substances. Nothing comparable happens in
   inorganic chemistry, so a *structural* formula, not a molecular formula, is
   needed to identify an organic compound.
3. **Distinct physical properties.** Organic compounds are almost all covalent,
   so they melt and boil at low temperatures, are usually insoluble in water but
   soluble in organic solvents, and do not conduct electricity.
4. **Distinct chemical behaviour.** Their reactions are *molecular* rather than
   ionic: they are slow, often reversible, need heat or a catalyst, and give side
   products. Inorganic ionic reactions are practically instantaneous.
5. **Reactions are governed by the functional group,** so millions of compounds
   can be handled in a few dozen families with a common set of reaction
   mechanisms.
6. **A separate nomenclature** (the IUPAC system) had to be built for them.
7. **Vast importance:** food, fuels, medicines, plastics, dyes, soaps, pesticides
   and the molecules of life itself are all organic.

| Property | Organic compounds | Inorganic compounds |
|---|---|---|
| Bonding | mostly covalent | mostly ionic |
| Melting and boiling point | low | generally high |
| Solubility | in organic solvents | usually in water |
| Electrical conductivity | non-conductors | conduct when fused or in solution |
| Rate of reaction | slow, needs catalyst or heat | fast, often instantaneous |
| Combustibility | usually inflammable | usually non-inflammable |
| Isomerism | very common | rare |
| Thermal stability | low; char on strong heating | generally high |

## 12.3 Tetra-covalency and catenation properties of carbon

### Tetra-covalency

Carbon is element number 6, with the ground-state configuration
1s² 2s² 2p_x¹ 2p_y¹. That gives only **two** unpaired electrons, so carbon ought
to be divalent — yet methane is CH₄, not CH₂.

The explanation is **promotion**. One of the paired 2s electrons is promoted to
the empty 2p_z orbital:

ground state 1s² 2s² 2p_x¹ 2p_y¹ → excited state 1s² 2s¹ 2p_x¹ 2p_y¹ 2p_z¹

This costs about 406 kJ mol⁻¹, but the two extra C–H bonds formed release far
more (about 2 × 413 kJ mol⁻¹), so the excited state is worth reaching. The four
singly occupied orbitals then mix to give four equivalent **sp³ hybrid
orbitals** pointing to the corners of a regular tetrahedron, with a bond angle of
**109°28′** (109.5°).

Why *covalency* rather than ionic bonding? Carbon would have to lose four
electrons to become C⁴⁺ (the sum of the first four ionisation energies is huge)
or gain four to become C⁴⁻ (impossible to force four electrons onto so small an
atom). Sharing is the only option, so carbon is always **tetracovalent** in its
stable compounds.

### Catenation

::: definition Catenation
**Catenation** is the ability of an element to link its own atoms together into
long chains, branched chains and rings through covalent bonds.
:::

Carbon catenates better than any other element. The reason is the strength of the
carbon–carbon bond, which in turn comes from carbon's small size: the two nuclei
can approach closely and overlap their orbitals effectively.

| Bond | C–C | Si–Si | N–N | O–O | S–S |
|---|---|---|---|---|---|
| Bond energy / kJ mol⁻¹ | 348 | 222 | 163 | 146 | 266 |

Two further points complete the picture. First, the C–H bond (413 kJ mol⁻¹) is
strong and non-polar, so a hydrocarbon chain is wrapped in a protective, chemically
inert skin — silicon chains, by contrast, are attacked at once by water. Second,
carbon also forms strong multiple bonds (C=C 614 kJ mol⁻¹, C≡C 839 kJ mol⁻¹),
which no other catenating element does well. Together these give open chains,
branched chains, rings of any size, and double and triple bonds — hence the
millions of compounds.

```figure caption="Left: the four sp³ bonds of carbon point to the corners of a tetrahedron, bond angle 109°28′. Right: single-bond energies — the C–C bond is far stronger than the corresponding bond of any other second- or third-row element, which is why carbon alone catenates freely."
import numpy as np, matplotlib.pyplot as plt
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.1,2.7),
                               gridspec_kw={'width_ratios':[1.05,1.0]})

# ---- left: tetrahedral methane ----
th, ph = np.radians(28.0), np.radians(16.0)
def proj(v):
    X, Y, Z = v
    x = X*np.cos(th) - Y*np.sin(th)
    d = X*np.sin(th) + Y*np.cos(th)
    return (x, Z*np.cos(ph) - d*np.sin(ph)), d
V3 = [(1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1)]
P = []
for v in V3:
    (x, y), d = proj(v)
    P.append((0.95*x, 0.95*y, d))
back = max(range(4), key=lambda k: P[k][2])
C = (0.0, 0.0)
for a in range(4):
    for b in range(a+1, 4):
        dashed = (a == back or b == back)
        ax1.plot([P[a][0], P[b][0]], [P[a][1], P[b][1]], color=GRID,
                 lw=1.0, ls=((0,(2,2)) if dashed else '-'))
for k, (x, y, d) in enumerate(P):
    ax1.plot([C[0], x], [C[1], y], color=INK, lw=1.7,
             ls=((0,(2,2)) if k == back else '-'), zorder=2)
for k, (x, y, d) in enumerate(P):
    ax1.plot([x], [y], marker='o', ms=12, color='#ffffff', zorder=3)
    ax1.text(x, y, 'H', fontsize=8.8, color=ACCENT, ha='center',
             va='center', zorder=4)
ax1.plot([C[0]], [C[1]], marker='o', ms=14, color=INK, zorder=5)
ax1.text(C[0], C[1], 'C', fontsize=8.8, color='#ffffff', ha='center',
         va='center', zorder=6, fontweight='bold')
ang = sorted((np.degrees(np.arctan2(y, x)) % 360.0, k)
             for k, (x, y, d) in enumerate(P))
best = None
for m in range(4):
    a1, k1 = ang[m]; a2, k2 = ang[(m+1) % 4]
    gap = (a2 - a1) % 360.0
    if k1 == back or k2 == back:
        continue
    if best is None or abs(gap - 109.5) < abs(best[2] - 109.5):
        best = (a1, a2, gap)
a1, a2, gap = best
arc = np.radians(np.linspace(a1, a1 + gap, 60))
ax1.plot(0.46*np.cos(arc), 0.46*np.sin(arc), color='#d9534f', lw=1.1, zorder=7)
am = np.radians(a1 + gap/2.0)
ax1.text(0.74*np.cos(am), 0.74*np.sin(am), '109°28′', fontsize=8.0,
         color='#d9534f', ha='center', va='center', zorder=8,
         bbox=dict(boxstyle='round,pad=0.12', fc='white', ec='none'))
ax1.set_xlim(-1.45, 1.45); ax1.set_ylim(-1.30, 1.50)
ax1.set_aspect('equal'); ax1.axis('off')

# ---- right: single bond energies ----
lab = ['C–C','S–S','Si–Si','N–N','O–O']
val = [348, 266, 222, 163, 146]
cols = ['#1d6fb8'] + [MUTED]*4
ax2.barh(np.arange(len(lab))[::-1], val, color=cols, height=0.62)
for i, (l, v) in enumerate(zip(lab, val)):
    ax2.text(v+10, len(lab)-1-i, str(v), va='center', fontsize=7.8, color=INK)
ax2.set_yticks(np.arange(len(lab))[::-1]); ax2.set_yticklabels(lab, fontsize=8.2)
ax2.set_xlabel('bond energy / kJ mol⁻¹', fontsize=8.2)
ax2.set_xlim(0, 430)
ax2.spines[['top','right']].set_visible(False)
ax2.grid(True, axis='x', alpha=0.45)
fig.tight_layout()
```

## 12.4 Classification of organic compounds

Organic compounds are classified twice over: once by the **shape of the carbon
skeleton**, and once by the **functional group** they carry.

```figure caption="Classification of organic compounds by the shape of the carbon skeleton."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,4.2))

def box(x, y, text, col=INK, fs=7.4, w=1.05):
    ax.text(x, y, text, fontsize=fs, color=col, ha='center', va='center',
            linespacing=1.25,
            bbox=dict(boxstyle='round,pad=0.30', facecolor='#f4f6f9',
                      edgecolor=col, linewidth=0.9))

def link(x1, y1, x2, y2):
    ax.plot([x1, x1, x2, x2], [y1, (y1+y2)/2, (y1+y2)/2, y2],
            color=MUTED, lw=1.0, solid_joinstyle='miter')

box(5.0, 9.4, 'ORGANIC COMPOUNDS', col=ACCENT, fs=8.2)
link(5.0, 9.05, 1.75, 8.05); link(5.0, 9.05, 6.70, 8.05)
box(1.75, 7.70, 'Acyclic\n(open chain, aliphatic)')
box(6.70, 7.70, 'Cyclic\n(closed chain)')

link(1.75, 7.35, 1.75, 6.45)
box(1.75, 6.10, 'propane,\npropene,\n2-methylbutane', col=MUTED, fs=7.0)

link(6.70, 7.35, 4.55, 6.15); link(6.70, 7.35, 8.85, 6.15)
box(4.55, 5.80, 'Homocyclic\n(carbocyclic)')
box(8.85, 5.80, 'Heterocyclic')
link(8.85, 5.45, 8.85, 4.60)
box(8.85, 4.25, 'furan,\npyridine,\nthiophene', col=MUTED, fs=7.0)

link(4.55, 5.45, 2.80, 4.30); link(4.55, 5.45, 6.30, 4.30)
box(2.80, 3.95, 'Alicyclic')
box(6.30, 3.95, 'Aromatic')
link(2.80, 3.60, 2.80, 2.85)
box(2.80, 2.50, 'cyclohexane,\ncyclopropane', col=MUTED, fs=7.0)

link(6.30, 3.60, 5.25, 2.45); link(6.30, 3.60, 8.40, 2.45)
box(5.25, 2.10, 'Benzenoid')
box(8.40, 2.10, 'Non-benzenoid')
link(5.25, 1.75, 5.25, 1.00); link(8.40, 1.75, 8.40, 1.00)
box(5.25, 0.65, 'benzene,\nnaphthalene', col=MUTED, fs=7.0)
box(8.40, 0.65, 'azulene,\ntropolone', col=MUTED, fs=7.0)

ax.set_xlim(0.0,10.6); ax.set_ylim(0.0,10.0); ax.axis('off')
```

- **Acyclic (open-chain or aliphatic) compounds** have carbon chains with two free
  ends. The chain may be straight (n-pentane) or branched (2-methylbutane).
- **Cyclic (closed-chain or ring) compounds** have at least one ring.
  - **Homocyclic (carbocyclic)** rings are built of carbon only. If the ring
    behaves like an open chain it is **alicyclic** (cyclohexane); if it has the
    special stability and substitution chemistry of benzene it is **aromatic**.
    Aromatic compounds that contain a benzene ring are **benzenoid** (benzene,
    naphthalene, phenol); the few that are aromatic without one are
    **non-benzenoid** (azulene, tropolone).
  - **Heterocyclic** rings contain at least one atom other than carbon — a
    *hetero atom*, usually O, N or S (furan, pyrrole, thiophene, pyridine).

## 12.5 Alkyl groups, functional groups and homologous series

### Alkyl groups

Remove one hydrogen atom from an alkane CₙH₂ₙ₊₂ and the fragment that is left,
CₙH₂ₙ₊₁, is an **alkyl group**, written R–. Alkyl groups never exist on their
own; they are the building blocks from which names are made.

| Alkane | Alkyl group | Formula | Symbol |
|---|---|---|---|
| Methane CH₄ | methyl | CH₃– | Me |
| Ethane C₂H₆ | ethyl | CH₃CH₂– | Et |
| Propane C₃H₈ | n-propyl | CH₃CH₂CH₂– | n-Pr |
| Propane C₃H₈ | isopropyl (propan-2-yl) | (CH₃)₂CH– | i-Pr |
| Butane C₄H₁₀ | n-butyl | CH₃CH₂CH₂CH₂– | n-Bu |
| Butane C₄H₁₀ | sec-butyl | CH₃CH₂CH(CH₃)– | s-Bu |
| 2-Methylpropane | isobutyl | (CH₃)₂CHCH₂– | i-Bu |
| 2-Methylpropane | tert-butyl | (CH₃)₃C– | t-Bu |

A carbon atom is called **primary (1°)**, **secondary (2°)** or **tertiary (3°)**
according to whether it is attached to one, two or three other carbon atoms. This
classification runs right through organic chemistry, so learn it now.

### Functional groups

::: definition Functional group
A **functional group** is an atom or group of atoms in a molecule that determines
its characteristic chemical properties. The rest of the molecule, the
hydrocarbon part, is largely a spectator.
:::

| Class | Functional group | General formula | IUPAC prefix | IUPAC suffix |
|---|---|---|---|---|
| Alkene | >C=C< | CₙH₂ₙ | — | -ene |
| Alkyne | –C≡C– | CₙH₂ₙ₋₂ | — | -yne |
| Haloalkane | –X (F, Cl, Br, I) | R–X | halo- | — |
| Alcohol | –OH | R–OH | hydroxy- | -ol |
| Ether | –O– | R–O–R′ | alkoxy- | — |
| Aldehyde | –CHO | R–CHO | oxo- / formyl- | -al |
| Ketone | >C=O | R–CO–R′ | oxo- | -one |
| Carboxylic acid | –COOH | R–COOH | carboxy- | -oic acid |
| Ester | –COO– | R–COOR′ | alkoxycarbonyl- | -oate |
| Acid chloride | –COCl | R–COCl | — | -oyl chloride |
| Amide | –CONH₂ | R–CONH₂ | carbamoyl- | -amide |
| Amine | –NH₂ | R–NH₂ | amino- | -amine |
| Nitrile (cyanide) | –C≡N | R–CN | cyano- | -nitrile |
| Nitro | –NO₂ | R–NO₂ | nitro- | — |

### Homologous series

::: definition Homologous series
A **homologous series** is a family of organic compounds having the same
functional group, in which each member differs from the next by one –CH₂– unit
and which can all be represented by one general formula.
:::

Characteristics of a homologous series:

1. All members have the **same general formula** (alkanes CₙH₂ₙ₊₂, alcohols
   CₙH₂ₙ₊₁OH).
2. Successive members differ by a **–CH₂– group**, that is by **14 atomic mass
   units**.
3. All members contain the **same functional group** and therefore show
   essentially the **same chemical properties**.
4. They can all be made by the **same general methods**.
5. Physical properties (melting point, boiling point, density) change
   **gradually and regularly** with molecular mass, so the properties of an
   unknown member can be predicted by interpolation.

| n | Alkane (CₙH₂ₙ₊₂) | Molar mass | Boiling point / °C |
|---|---|---|---|
| 1 | CH₄ methane | 16 | −162 |
| 2 | C₂H₆ ethane | 30 | −89 |
| 3 | C₃H₈ propane | 44 | −42 |
| 4 | C₄H₁₀ butane | 58 | −0.5 |
| 5 | C₅H₁₂ pentane | 72 | 36 |
| 6 | C₆H₁₄ hexane | 86 | 69 |

The molar mass rises by exactly 14 each time and the boiling point rises steadily
— that regularity is the whole point of a homologous series.

### IUPAC nomenclature

The International Union of Pure and Applied Chemistry name of a compound is built
from five parts, always written in this order and joined into a single word:

**Secondary prefix + Primary prefix + Word root + Primary suffix + Secondary suffix**

| Part | What it gives | Example |
|---|---|---|
| Word root | number of carbons in the parent chain | meth (1), eth (2), prop (3), but (4), pent (5), hex (6) |
| Primary suffix | saturation | -ane, -ene, -yne |
| Secondary suffix | the principal functional group | -ol, -al, -one, -oic acid |
| Primary prefix | cyclo-, for a ring | cyclohexane |
| Secondary prefix | substituents | methyl-, chloro-, nitro- |

**The rules, in the order you apply them.**

1. **Find the parent chain** — the longest continuous chain of carbon atoms that
   contains the principal functional group. If two chains are equally long, choose
   the one with more substituents.
2. **Number the chain** from the end that gives the **lowest locant to the
   principal functional group**. If there is none, give the lowest locant to the
   multiple bond; failing that, to the substituents (the *lowest set of locants*
   rule).
3. **Name the substituents** as prefixes with their locants, and list them in
   **alphabetical order**. The multiplying prefixes di-, tri-, tetra- are *not*
   counted when alphabetising (di**m**ethyl files under "m").
4. **Punctuate**: numbers are separated from words by hyphens and from each other
   by commas. There are no spaces inside the name, except before "acid".
5. When the same substituent occurs more than once, use di-, tri-, tetra- and
   repeat the locant for each: 2,2-dimethylpropane, not 2-dimethylpropane.

When a molecule has more than one functional group, only the senior one becomes
the suffix; the rest become prefixes. The order of seniority is

–COOH > –SO₃H > –COOR > –COCl > –CONH₂ > –CN > –CHO > >C=O > –OH > –NH₂ >
>C=C< > –C≡C–

while –OR (alkoxy), –X (halo) and –NO₂ (nitro) are **always** prefixes, never
suffixes.

::: memory The order of the parts of a name
Say it as a sentence: "**S**ome **P**eople **W**ant **P**lain **S**imple names" —
**S**econdary prefix, **P**rimary prefix, **W**ord root, **P**rimary suffix,
**S**econdary suffix. Build every name in that order and you cannot put a piece
in the wrong place.
:::

::: example Worked example 12.1 — IUPAC naming
**Problem.** Give the IUPAC name of each compound.
(a) (CH₃)₂CH–CH₂–CH(CH₃)–CH₃
(b) CH₃–CH₂–CH(OH)–CH₂–CH₃
(c) CH₃–CH=CH–CH₂–CHO
(d) CH₃–CH(CH₃)–CH₂–COOH

**Solution.**

(a) Written out in full the molecule is CH₃–CH(CH₃)–CH₂–CH(CH₃)–CH₃. The longest
chain has **five** carbons, so the word root is *pent* and, being saturated, the
primary suffix is *-ane*. There are two methyl substituents. Numbering from the
left gives locants {2, 4}; from the right it also gives {2, 4}, so either end
serves. Name: **2,4-dimethylpentane**.

(b) The parent chain has five carbons and the principal functional group is –OH,
so the name ends in *-ol*. Numbering from either end puts the OH on carbon 3.
Name: **pentan-3-ol**.

(c) The –CHO group must be carbon 1, so number from the right: C1 is CHO, C2 is
CH₂, and the double bond lies between C3 and C4. Word root *pent*, primary suffix
*-ene* with locant 3, secondary suffix *-al*. Name: **pent-3-enal**.

(d) The –COOH carbon is always C1, so the chain is C1 (COOH), C2 (CH₂),
C3 (CH with a methyl), C4 (CH₃) — four carbons, with a methyl group on C3.
Name: **3-methylbutanoic acid**.
:::

::: caution Number from the functional group, not from the left
The commonest mistake in this topic is numbering the chain from whichever end you
happened to draw first. Always locate the principal functional group, give it the
lowest possible number, and only then worry about the substituents. "4-methylbutan-4-ol"
is not merely wrong, it is impossible — butane has only four carbons and the
correct name is butan-1-ol with the methyl included in the chain.
:::

## 12.6 Structural formula, contracted formula and bond line structural formula

A **molecular formula** (C₄H₁₀O) tells you only how many atoms there are. Because
of isomerism that is not enough, so organic chemists use three ways of showing how
the atoms are joined.

| Representation | What is shown | Example: butan-2-ol |
|---|---|---|
| Complete (displayed) structural formula | every atom and every bond drawn as a line | see the figure below |
| Condensed (contracted) formula | atoms written in order, bonds mostly omitted; branches in brackets | CH₃CH(OH)CH₂CH₃ |
| Bond-line (skeletal) structural formula | only the carbon skeleton as a zig-zag; carbons and their hydrogens are not written | see the figure below |

**Rules for a bond-line structure.** Each line is a bond. Every vertex and every
free line end is a **carbon** atom. The hydrogens attached to carbon are **not**
drawn — you work out how many there are from the fact that carbon is tetravalent.
All atoms other than carbon and hydrogen (O, N, Cl, and any H attached to them)
*are* written in.

```figure caption="The same molecule, butan-2-ol, drawn three ways. In the bond-line structure every vertex and line end is a carbon, and the hydrogens on carbon are understood."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(3, 1, figsize=(4.8,4.3),
                         gridspec_kw={'height_ratios':[1.55,0.55,1.05]})
for a in axes:
    a.axis('off')

# ---------- (a) complete structural formula ----------
ax = axes[0]
Cx = [0.0, 1.5, 3.0, 4.5]
for x in Cx:
    ax.text(x, 0.0, 'C', fontsize=9.5, color=INK, ha='center', va='center',
            bbox=dict(boxstyle='circle,pad=0.12', fc='white', ec='none'))
for x1, x2 in zip(Cx, Cx[1:]):
    ax.plot([x1+0.24, x2-0.24],[0,0], color=INK, lw=1.3)

def H(x, y, x0, y0):
    ax.plot([x0, x],[y0, y], color=INK, lw=1.3, zorder=1)
    ax.text(x, y, 'H', fontsize=9.0, color=ACCENT, ha='center', va='center',
            bbox=dict(boxstyle='circle,pad=0.10', fc='white', ec='none'), zorder=2)

H(-1.20, 0.00, -0.24, 0.0)
H( 0.00, 1.05, 0.0, 0.24); H( 0.00,-1.05, 0.0,-0.24)
H( 1.50,-1.05, 1.5,-0.24)
H( 3.00, 1.05, 3.0, 0.24); H( 3.00,-1.05, 3.0,-0.24)
H( 4.50, 1.05, 4.5, 0.24); H( 4.50,-1.05, 4.5,-0.24); H(5.70, 0.00, 4.74, 0.0)
# the OH group on C2
ax.plot([1.5,1.5],[0.24,0.86], color=INK, lw=1.3)
ax.text(1.5, 1.05, 'O', fontsize=9.5, color='#d9534f', ha='center', va='center',
        bbox=dict(boxstyle='circle,pad=0.12', fc='white', ec='none'))
ax.plot([0.66,1.26],[1.05,1.05], color=INK, lw=1.3)
ax.text(0.47, 1.05, 'H', fontsize=9.0, color=ACCENT, ha='center', va='center')
ax.text(-2.55, 0.0, '(a) complete\nstructural', fontsize=8.0, color=MUTED,
        ha='center', va='center', linespacing=1.3)
ax.set_xlim(-3.6, 6.4); ax.set_ylim(-1.55, 1.55)

# ---------- (b) condensed formula ----------
ax = axes[1]
ax.text(1.4, 0.0, 'CH₃—CH(OH)—CH₂—CH₃', fontsize=11.0, color=INK,
        ha='center', va='center')
ax.text(-2.55, 0.0, '(b) condensed', fontsize=8.0, color=MUTED, ha='center',
        va='center')
ax.set_xlim(-3.6, 6.4); ax.set_ylim(-0.6, 0.6)

# ---------- (c) bond-line formula ----------
ax = axes[2]
V = [(0.0,0.0), (0.80,0.46), (1.60,0.0), (2.40,0.46)]
for a_, b_ in zip(V, V[1:]):
    ax.plot([a_[0],b_[0]],[a_[1],b_[1]], color=INK, lw=1.7)
ax.plot([0.80,0.80],[0.46,1.30], color=INK, lw=1.7)
ax.text(0.80, 1.50, 'OH', fontsize=10.0, color='#d9534f', ha='center', va='center')
for i, (x,y) in enumerate(V, 1):
    ax.plot([x],[y], marker='o', ms=3.4, color=MUTED)
    ax.text(x, y-0.30, f'C{i}', fontsize=7.4, color=MUTED, ha='center', va='center')
ax.text(-1.85, 0.55, '(c) bond-line', fontsize=8.0, color=MUTED,
        ha='center', va='center')
ax.text(4.55, 0.55, 'C₄H₁₀O\nbutan-2-ol', fontsize=8.4, color=INK,
        ha='center', va='center', linespacing=1.3)
ax.set_xlim(-2.75, 5.90); ax.set_ylim(-0.60, 1.95)
fig.tight_layout()
```

### Isomerism

::: definition Isomerism
**Isomers** are two or more compounds that have the same molecular formula but
different structures, and therefore different properties. The phenomenon is
called **isomerism**.
:::

Isomerism splits into two branches:

- **Structural (constitutional) isomerism** — the atoms are joined in a different
  order. Sub-types: chain, position, functional, metamerism and tautomerism.
- **Stereoisomerism** — the atoms are joined in the same order but arranged
  differently in space. Sub-types: geometrical (cis–trans) and optical (d and l).

| Type | Difference between the isomers | Example (same molecular formula) |
|---|---|---|
| Chain | length or branching of the carbon skeleton | C₄H₁₀: butane and 2-methylpropane |
| Position | position of the functional group or multiple bond | C₃H₇OH: propan-1-ol and propan-2-ol |
| Functional | a different functional group altogether | C₂H₆O: ethanol and methoxymethane |
| Metamerism | different alkyl groups on either side of a divalent atom | C₄H₁₀O: ethoxyethane and methoxypropane |
| Tautomerism | a hydrogen atom migrates, giving two forms in equilibrium | CH₃COCH₃ ⇌ CH₃C(OH)=CH₂ (keto–enol) |
| Geometrical | arrangement about a C=C that cannot rotate | cis- and trans-but-2-ene |
| Optical | mirror-image arrangements about a chiral carbon | d- and l-lactic acid |

```figure caption="The three chain isomers of C₅H₁₂ in bond-line notation. Branching lowers the boiling point because the molecules pack less closely and their van der Waals contact area is smaller."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 3, figsize=(5.1,2.3))

def draw(ax, bonds, dots, title, sub):
    for (x1,y1),(x2,y2) in bonds:
        ax.plot([x1,x2],[y1,y2], color=INK, lw=1.8)
    for (x,y) in dots:
        ax.plot([x],[y], marker='o', ms=3.2, color=MUTED)
    ax.set_title(title, fontsize=8.0, color=INK, pad=5)
    ax.text(0.5, -0.20, sub, fontsize=7.6, color=MUTED, ha='center',
            va='center', transform=ax.transAxes)
    ax.set_xlim(-0.35, 3.15); ax.set_ylim(-0.55, 1.65)
    ax.set_aspect('equal'); ax.axis('off')

# n-pentane
V = [(0,0),(0.7,0.42),(1.4,0),(2.1,0.42),(2.8,0)]
draw(axes[0], list(zip(V, V[1:])), V, 'pentane', 'b.p. 36 °C')

# 2-methylbutane
V = [(0.2,0),(0.9,0.42),(1.6,0),(2.3,0.42)]
b = list(zip(V, V[1:])) + [((0.9,0.42),(0.9,1.26))]
draw(axes[1], b, V + [(0.9,1.26)], '2-methylbutane', 'b.p. 28 °C')

# 2,2-dimethylpropane
c = (1.3,0.42)
ends = [(0.6,0.0),(2.0,0.0),(1.3,1.26),(1.3,-0.42)]
draw(axes[2], [(c,e) for e in ends], [c]+ends, '2,2-dimethylpropane', 'b.p. 9.5 °C')
fig.tight_layout()
```

Geometrical isomerism appears whenever a double bond carries two *different*
groups on each of its carbons. The C=C bond cannot rotate — rotation would break
the π bond — so the two arrangements are separate, isolable compounds.

```figure caption="Geometrical isomers of but-2-ene. In the cis form the two methyl groups are on the same side and the bond dipoles add; in the trans form they are on opposite sides and the dipoles cancel."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(4.8,2.4))

def alkene(ax, top_left, bot_left, top_right, bot_right, title, sub):
    C1, C2 = (0.0,0.0), (1.10,0.0)
    ax.plot([C1[0]+0.18, C2[0]-0.18],[ 0.07, 0.07], color=INK, lw=1.7)
    ax.plot([C1[0]+0.18, C2[0]-0.18],[-0.07,-0.07], color=INK, lw=1.7)
    ax.text(C1[0], C1[1], 'C', fontsize=9.5, color=INK, ha='center', va='center')
    ax.text(C2[0], C2[1], 'C', fontsize=9.5, color=INK, ha='center', va='center')
    pos = {'tl':(-0.72, 0.72), 'bl':(-0.72,-0.72),
           'tr':(1.82, 0.72),  'br':(1.82,-0.72)}
    anch = {'tl':C1, 'bl':C1, 'tr':C2, 'br':C2}
    for k, lab in (('tl',top_left), ('bl',bot_left), ('tr',top_right), ('br',bot_right)):
        x, y = pos[k]; x0, y0 = anch[k]
        ax.plot([x0 + 0.20*np.sign(x-x0), x - 0.16*np.sign(x-x0)],
                [y0 + 0.16*np.sign(y-y0), y - 0.14*np.sign(y-y0)], color=INK, lw=1.5)
        col = '#d9534f' if lab == 'CH₃' else ACCENT
        ax.text(x, y, lab, fontsize=9.0, color=col, ha='center', va='center')
    ax.set_title(title, fontsize=8.4, color=INK, pad=4)
    ax.text(0.55, -1.32, sub, fontsize=7.6, color=MUTED, ha='center', va='center')
    ax.set_xlim(-1.45, 2.55); ax.set_ylim(-1.60, 1.15)
    ax.set_aspect('equal'); ax.axis('off')

alkene(axes[0], 'CH₃', 'H', 'CH₃', 'H', 'cis-but-2-ene',
       'polar,  b.p. 3.7 °C')
alkene(axes[1], 'CH₃', 'H', 'H', 'CH₃', 'trans-but-2-ene',
       'non-polar,  b.p. 0.9 °C')
fig.tight_layout()
```

::: example Worked example 12.2 — counting and naming isomers
**Problem.** (a) Draw and name the three chain isomers of C₅H₁₂. (b) How many
isomers have the molecular formula C₄H₁₀O? Name them and say what kind of
isomerism relates them.

**Solution.**

(a) A five-carbon skeleton can be arranged in only three ways:

1. an unbranched chain of five — CH₃CH₂CH₂CH₂CH₃, **pentane**;
2. a chain of four with one methyl on C2 — (CH₃)₂CHCH₂CH₃, **2-methylbutane**;
3. a chain of three with two methyls on C2 — C(CH₃)₄, **2,2-dimethylpropane**.

A methyl on C3 of butane would just be 2-methylbutane drawn backwards, and a
methyl on C1 would lengthen the chain to pentane, so there is no fourth isomer.

(b) C₄H₁₀O is saturated and has one oxygen, so it can be either an **alcohol** or
an **ether**.

*Alcohols*, C₄H₉OH — the butyl group has four isomeric forms:
butan-1-ol, butan-2-ol, 2-methylpropan-1-ol and 2-methylpropan-2-ol. **4 isomers.**

*Ethers*, R–O–R′ where the two alkyl groups together hold four carbons:
methoxypropane (CH₃–O–C₃H₇), 2-methoxypropane (CH₃–O–CH(CH₃)₂) and ethoxyethane
(C₂H₅–O–C₂H₅). **3 isomers.**

**Total = 7 isomers.** Within the alcohols the relationship is chain or position
isomerism; within the ethers, ethoxyethane and methoxypropane are **metamers**;
any alcohol compared with any ether is a pair of **functional isomers**.
:::

::: example Worked example 12.3
**Problem.** An organic compound contains 85.7% carbon and 14.3% hydrogen by
mass, and its vapour density is 21. Find its empirical and molecular formulae,
and draw the isomers it can have. (C = 12, H = 1)

**Solution.**

| Element | % by mass | ÷ atomic mass | simplest ratio |
|---|---|---|---|
| C | 85.7 | 85.7 ÷ 12 = 7.14 | 7.14 ÷ 7.14 = 1 |
| H | 14.3 | 14.3 ÷ 1 = 14.3 | 14.3 ÷ 7.14 = 2 |

The empirical formula is **CH₂**, of empirical formula mass 12 + 2 = 14.

Molecular mass = 2 × vapour density = 2 × 21 = 42, so

$$ n = \frac{42}{14} = 3 \quad\Rightarrow\quad \text{molecular formula } = \text{C}_3\text{H}_6 $$

C₃H₆ has one degree of unsaturation, which it can satisfy either with a double
bond or with a ring. The two isomers are therefore **propene**, CH₃–CH=CH₂ (an
open-chain alkene) and **cyclopropane**, a three-membered ring. They have the
same molecular formula but different functional character, so they are
**functional (ring–chain) isomers**.
:::

## 12.7 Cracking and reforming; quality of gasoline; octane number; cetane number; gasoline additive

Crude petroleum is separated by fractional distillation into fractions, of which
**gasoline (petrol)**, boiling between about 40 °C and 200 °C and containing
C₅ to C₁₂ hydrocarbons, is the most valuable. Crude oil yields only about 20% of
this fraction directly, while the market wants far more — and the straight-run
petrol that does come off is of poor quality. Two processes fix both problems.

### Cracking

::: definition Cracking
**Cracking** is the process of breaking down larger hydrocarbon molecules of high
boiling point into smaller, more useful molecules of lower boiling point.
:::

C₁₆H₃₄ --Δ--> C₈H₁₈ + C₈H₁₆

C₁₂H₂₆ --Δ--> C₆H₁₄ + C₆H₁₂

| | Thermal cracking | Catalytic cracking |
|---|---|---|
| Conditions | 750–900 K, 10–70 atm, no catalyst | 700–800 K, 1–2 atm |
| Catalyst | none | zeolite or silica–alumina |
| Intermediate | free radicals | carbocations |
| Main products | straight-chain alkanes and alkenes | branched alkanes, cycloalkanes, aromatics |
| Quality of petrol | moderate | high, because branched products resist knocking |

### Reforming

::: definition Reforming
**Reforming** is the rearrangement of hydrocarbon molecules into isomeric or
cyclic forms of nearly the same molecular mass, in order to improve the quality
of the petrol. The number of carbon atoms is essentially unchanged.
:::

Three kinds of change occur together over a platinum-on-alumina catalyst at about
770 K and 10–20 atm — the process is called *platforming*:

- **Isomerisation:** n-hexane → 2,2-dimethylbutane
- **Cyclisation:** C₆H₁₄ → C₆H₁₂ (cyclohexane) + H₂
- **Aromatisation:** C₆H₁₄ → C₆H₆ (benzene) + 4H₂, and
  C₇H₁₆ → C₇H₈ (toluene) + 4H₂

Cracking makes *more* petrol; reforming makes *better* petrol.

### Knocking, octane number and cetane number

In a petrol engine the fuel–air mixture should burn smoothly only when the spark
plug fires. If part of the mixture ignites on its own beforehand, the engine
produces a sharp metallic rattle, loses power and eventually damages itself. This
premature explosion is called **knocking** or *pinking*.

Knocking depends on structure. Straight-chain alkanes knock badly; branched
alkanes, cycloalkanes and aromatics knock very little:

n-alkane > cycloalkane > alkene > branched alkane > aromatic hydrocarbon

::: definition Octane number
The **octane number** of a petrol is the percentage by volume of iso-octane
(2,2,4-trimethylpentane) in a mixture of iso-octane and n-heptane that has the
same knocking characteristics as the fuel being tested. Iso-octane is given the
value 100 and n-heptane the value 0.
:::

So a petrol of octane number 91 knocks exactly like a blend of 91 parts
iso-octane with 9 parts n-heptane. The higher the octane number, the better the
antiknock quality and the higher the compression ratio the engine may use.

::: definition Cetane number
The **cetane number** of a diesel is the percentage by volume of cetane
(n-hexadecane, C₁₆H₃₄) in a mixture of cetane and α-methylnaphthalene that has
the same ignition delay as the diesel being tested. Cetane is given the value
100 and α-methylnaphthalene the value 0.
:::

::: caution A good petrol is a bad diesel
The two scales run in **opposite** directions. A petrol engine ignites its fuel
with a spark and wants a fuel that resists spontaneous ignition — so branched and
aromatic hydrocarbons, high octane number. A diesel engine ignites its fuel by
compression alone and wants a fuel that ignites *easily* — so straight-chain
alkanes, high cetane number. Good diesel has a cetane number of 45–55.
:::

### Gasoline additives

A **gasoline additive** is a substance added in small quantity to petrol to
improve its performance, chiefly its antiknock quality.

| Additive | Formula / nature | Purpose |
|---|---|---|
| Tetraethyl lead, TEL (now banned) | Pb(C₂H₅)₄ | raised the octane number by about 10 units at 0.5 mL per litre |
| Ethylene dibromide (scavenger, used with TEL) | C₂H₄Br₂ | converted lead residues to volatile PbBr₂ so they left with the exhaust |
| MTBE | methyl tert-butyl ether | oxygenate; raises octane number and helps complete combustion |
| Ethanol | C₂H₅OH | renewable oxygenate, octane number about 108 |
| Aromatics | benzene, toluene, xylene | high octane blending components |
| Detergents and antioxidants | organic amines, phenols | keep injectors clean, prevent gum formation |

Tetraethyl lead was outstandingly effective and outstandingly poisonous: it filled
city air with lead compounds and destroyed the catalytic converters fitted to
modern exhausts. Nepal, like the rest of South Asia, phased out leaded petrol
around the turn of the century, and the fuel sold today by Nepal Oil Corporation
is unleaded, its octane number raised by reforming and by oxygenates instead.

::: example Worked example 12.4
**Problem.** (a) A sample of petrol knocks exactly as badly as a mixture of
87 mL of iso-octane and 13 mL of n-heptane. State its octane number.
(b) A refinery blends 60 L of a stream of octane number 95 with 40 L of a stream
of octane number 80. Assuming the octane numbers blend linearly by volume, find
the octane number of the product. (c) The product must reach 91 before it can be
sold. Is the blend acceptable?

**Solution.**

(a) By definition the octane number is the percentage by volume of iso-octane in
the matching reference mixture:

$$ \text{ON} = \frac{87}{87+13}\times 100 = 87 $$

(b) Taking a volume-weighted mean,

$$ \text{ON} = \frac{60(95) + 40(80)}{60+40} = \frac{5700 + 3200}{100} = 89 $$

(c) 89 is below the required 91, so the blend fails. The refinery must either add
a higher-octane stream or increase the severity of the reforming step. For
example, replacing 20 L of the 80-octane stream with 20 L of the 95-octane stream
would give $\dfrac{80(95) + 20(80)}{100} = 92$, which passes.
:::

## 12.8 Bond fission and electronic effects — a bridge to Unit 13

Everything after this unit is about *how* organic reactions happen. Two ideas
underlie all of it: how a bond breaks, and how electron density is pushed about
inside a molecule that has not yet reacted.

### Homolytic and heterolytic fission

| | Homolytic fission | Heterolytic fission |
|---|---|---|
| How the pair splits | one electron to each atom | both electrons to one atom |
| Products | two **free radicals**, A• and B• | two **ions**, A⁺ and B:⁻ |
| Arrow used | half-headed "fish-hook" arrow | full curved arrow |
| Favoured by | high temperature, UV light, peroxides, non-polar solvents | polar bonds and polar solvents |
| Example | Cl₂ --hν--> 2Cl• | CH₃–Br → CH₃⁺ + Br⁻ |

```figure caption="The two ways a covalent bond can break. A fish-hook (half-headed) arrow moves one electron and gives free radicals; a full curved arrow moves an electron pair and gives ions."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(5.1,2.4))

def base(ax, title):
    ax.text(0.0, 0.0, 'A', fontsize=11, color=INK, ha='center', va='center')
    ax.text(1.4, 0.0, 'B', fontsize=11, color=INK, ha='center', va='center')
    ax.plot([0.24,1.16],[0,0], color=INK, lw=1.5)
    ax.plot([0.60],[0.10], marker='o', ms=3.0, color='#d9534f')
    ax.plot([0.80],[0.10], marker='o', ms=3.0, color='#d9534f')
    ax.set_title(title, fontsize=8.6, color=INK, pad=6)
    ax.set_xlim(-0.75, 4.35); ax.set_ylim(-1.35, 1.25)
    ax.axis('off')

# --- homolytic ---
ax = axes[0]
base(ax, 'homolytic fission')
ax.annotate('', xy=(0.12,0.34), xytext=(0.62,0.24),
            arrowprops=dict(arrowstyle='->', color='#d9534f', lw=1.3,
                            connectionstyle='arc3,rad=0.45', mutation_scale=11))
ax.annotate('', xy=(1.30,0.34), xytext=(0.80,0.24),
            arrowprops=dict(arrowstyle='->', color='#d9534f', lw=1.3,
                            connectionstyle='arc3,rad=-0.45', mutation_scale=11))
ax.annotate('', xy=(2.55,0.0), xytext=(1.95,0.0),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.3, mutation_scale=11))
ax.text(3.45, 0.0, 'A•  +  B•', fontsize=10.5, color=INK, ha='center', va='center')
ax.text(1.80, -0.92, 'free radicals:  Cl₂ --hν--> 2Cl•', fontsize=7.8,
        color=MUTED, ha='center')

# --- heterolytic ---
ax = axes[1]
base(ax, 'heterolytic fission')
ax.annotate('', xy=(1.40,0.22), xytext=(0.70,0.22),
            arrowprops=dict(arrowstyle='-|>', color='#1d6fb8', lw=1.5,
                            connectionstyle='arc3,rad=-0.55', mutation_scale=12))
ax.annotate('', xy=(2.55,0.0), xytext=(1.95,0.0),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.3, mutation_scale=11))
ax.text(3.45, 0.0, 'A⁺  +  B:⁻', fontsize=10.5, color=INK, ha='center', va='center')
ax.text(1.80, -0.92, 'ions:  CH₃—Br → CH₃⁺ + Br⁻', fontsize=7.8,
        color=MUTED, ha='center')
fig.tight_layout()
```

Heterolysis produces the two reactive carbon species you will meet constantly:

- A **carbocation** has a positively charged carbon with only six electrons. It
  is sp² hybridised and planar. Stability: 3° > 2° > 1° > CH₃⁺.
- A **carbanion** has a negatively charged carbon carrying a lone pair. It is sp³
  hybridised and pyramidal. Stability runs the other way: CH₃⁻ > 1° > 2° > 3°.

### Electrophiles and nucleophiles

| | Electrophile | Nucleophile |
|---|---|---|
| Meaning | "electron loving" | "nucleus loving" |
| Electronically | electron **deficient**, accepts an electron pair (a Lewis acid) | electron **rich**, donates an electron pair (a Lewis base) |
| Charge | positive or neutral | negative or neutral |
| Examples | H⁺, Cl⁺, Br⁺, NO₂⁺, R⁺, BF₃, AlCl₃, SO₃, the carbon of >C=O | OH⁻, CN⁻, Cl⁻, RO⁻, NH₃, H₂O, ROH, RNH₂, alkenes |

A **free radical** is the third species: neutral, with one unpaired electron,
paramagnetic and extremely reactive. Stability: 3° > 2° > 1° > CH₃•.

### Inductive, resonance and hyperconjugative effects

**Inductive effect (I).** When an atom more electronegative than carbon is
attached to a chain, the σ electrons of the C–X bond are pulled towards it, and
the polarisation is relayed along the chain with rapidly decreasing strength — it
is negligible beyond the third carbon. It is a **permanent** effect.

- **–I groups** withdraw electrons:
  –NO₂ > –CN > –COOH > –F > –Cl > –Br > –I > –OCH₃ > –C₆H₅
- **+I groups** release electrons (taking H as the standard):
  –C(CH₃)₃ > –CH(CH₃)₂ > –CH₂CH₃ > –CH₃

The classic demonstration is acid strength. Chlorine is –I, so it drains electron
density from the –COO⁻ ion and stabilises it, making the acid stronger:

| Acid | CH₃COOH | ClCH₂COOH | Cl₂CHCOOH | Cl₃CCOOH |
|---|---|---|---|---|
| pKa | 4.76 | 2.86 | 1.29 | 0.66 |
| Strength | weakest | → | → | strongest |

**Resonance (mesomeric) effect (R or M).** In a conjugated system, π electrons or
a lone pair are delocalised over several atoms. Unlike the inductive effect it is
transmitted through the whole conjugated system without dying away, and it is
usually the stronger of the two.

- **+R groups** push a lone pair into the system: –OH, –OR, –NH₂, –NHR, –X
- **–R groups** pull π electrons out of it: –NO₂, –CN, –CHO, –COR, –COOH, –SO₃H

**Hyperconjugation.** The σ electrons of a C–H bond on the carbon *next to* an
sp² centre can also delocalise into the empty or π orbital. It is sometimes called
"no-bond resonance" or the Baker–Nathan effect. Its strength depends simply on the
number of α-hydrogens available, which is why

(CH₃)₃C⁺ (9 α-H) > (CH₃)₂CH⁺ (6 α-H) > CH₃CH₂⁺ (3 α-H) > CH₃⁺ (0 α-H)

and why the same order of stability appears again for free radicals and for
substituted alkenes.

## Chapter summary

- Organic chemistry is the chemistry of hydrocarbons and their derivatives. The
  vital force theory died when Wöhler made urea from ammonium cyanate in 1828,
  NH₄CNO --Δ--> NH₂CONH₂.
- Organic compounds are studied separately because of their number, their
  isomerism, their covalent character, their slow molecular reactions and their
  functional-group chemistry.
- Carbon is **tetracovalent**: promotion of a 2s electron gives four unpaired
  electrons, four sp³ hybrid orbitals and a tetrahedral angle of 109°28′.
  **Catenation** is possible because the C–C bond (348 kJ mol⁻¹) is far stronger
  than Si–Si, N–N or O–O.
- Compounds are classified as acyclic, or cyclic — homocyclic (alicyclic or
  aromatic, benzenoid or non-benzenoid) and heterocyclic.
- An alkyl group is CₙH₂ₙ₊₁; a functional group decides chemical behaviour; a
  **homologous series** has one general formula, a constant difference of –CH₂–
  (14 u), identical chemical properties and a regular gradation of physical
  properties.
- An IUPAC name is built as secondary prefix + primary prefix + word root +
  primary suffix + secondary suffix, numbering the parent chain so that the
  principal functional group gets the lowest locant.
- Structures are written in three ways: complete structural, condensed and
  bond-line, where every vertex and line end is a carbon and hydrogens on carbon
  are omitted.
- **Isomers** share a molecular formula but differ in structure: chain, position,
  functional, metamerism and tautomerism (structural); geometrical and optical
  (stereo). C₅H₁₂ has 3 isomers, C₄H₁₀O has 7.
- **Cracking** breaks big molecules into smaller ones and makes more petrol;
  **reforming** rearranges molecules into branched and aromatic forms and makes
  better petrol.
- **Octane number** = % by volume of iso-octane in the iso-octane/n-heptane blend
  that knocks equally; **cetane number** = % by volume of cetane in the
  cetane/α-methylnaphthalene blend with the same ignition delay. High octane and
  high cetane are opposite requirements.
- A bond breaks **homolytically** (fish-hook arrows, free radicals) or
  **heterolytically** (full curved arrow, ions). Electrophiles accept an electron
  pair, nucleophiles donate one. The **inductive** effect dies out along a chain,
  the **resonance** effect travels through a conjugated system, and
  **hyperconjugation** grows with the number of α-hydrogens.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The bond angle in methane is <span class="marks">[1]</span>
   (a) 90° (b) 104°31′ (c) 109°28′ (d) 120°
2. The number of structural isomers of C₅H₁₂ is <span class="marks">[1]</span>
   (a) 2 (b) 3 (c) 4 (d) 5
3. The IUPAC name of (CH₃)₃C–OH is <span class="marks">[1]</span>
   (a) butan-1-ol (b) butan-2-ol (c) 2-methylpropan-1-ol (d) 2-methylpropan-2-ol
4. Octane number 100 is assigned to <span class="marks">[1]</span>
   (a) n-heptane (b) n-octane (c) 2,2,4-trimethylpentane (d) cetane
5. Homolytic fission of a covalent bond produces <span class="marks">[1]</span>
   (a) a carbocation (b) a carbanion (c) free radicals (d) an electrophile and a nucleophile
6. Which of the following shows the +I effect? <span class="marks">[1]</span>
   (a) –NO₂ (b) –CN (c) –COOH (d) –C(CH₃)₃
7. Ethanol and methoxymethane are an example of <span class="marks">[1]</span>
   (a) chain isomerism (b) position isomerism (c) functional isomerism (d) tautomerism

::: note Answers to Group A
**1.** (c) — four equivalent sp³ orbitals directed to the corners of a regular tetrahedron.
**2.** (b) — pentane, 2-methylbutane and 2,2-dimethylpropane.
**3.** (d) — the longest chain is three carbons with a methyl and the OH both on C2.
**4.** (c) — iso-octane, 2,2,4-trimethylpentane, is the 100 mark; n-heptane is 0.
**5.** (c) — each atom keeps one electron of the shared pair.
**6.** (d) — alkyl groups release electrons; –NO₂, –CN and –COOH are all –I.
**7.** (c) — same formula C₂H₆O but different functional groups, alcohol and ether.
:::

**Group B — Short answer (5 marks each)**

1. Why is organic chemistry studied as a separate branch of chemistry? Give any five reasons. <span class="marks">[5]</span>
2. Explain the tetra-covalency of carbon on the basis of its electronic configuration, and state why carbon catenates better than silicon. <span class="marks">[5]</span>
3. Define a homologous series and give its five characteristics, illustrating with the first four alkanes. <span class="marks">[5]</span>
4. Write the IUPAC names of: (i) (CH₃)₂CHCH₂CH₃ (ii) CH₃CH₂CH(OH)CH₃ (iii) CH₃CH₂CHO (iv) CH₃CH(CH₃)COOH (v) CH₃CH₂C≡CH <span class="marks">[5]</span>
5. Draw the structures of all the isomers of C₄H₉Cl and name them. <span class="marks">[5]</span>
6. Distinguish between cracking and reforming. Write one equation for each. <span class="marks">[5]</span>
7. Define octane number and cetane number. Why does a high octane number make a poor diesel? <span class="marks">[5]</span>
8. Distinguish between homolytic and heterolytic fission with one example of each, and define an electrophile and a nucleophile. <span class="marks">[5]</span>

::: note Answers to Group B
**4.** (i) 2-methylbutane (ii) butan-2-ol (iii) propanal (iv) 2-methylpropanoic acid
(v) but-1-yne.

**5.** Four isomers: 1-chlorobutane CH₃CH₂CH₂CH₂Cl; 2-chlorobutane
CH₃CH₂CHClCH₃; 1-chloro-2-methylpropane (CH₃)₂CHCH₂Cl; 2-chloro-2-methylpropane
(CH₃)₃CCl. The first pair and the second pair are position isomers of each other,
and the two skeletons are chain isomers.

**6.** Cracking breaks large molecules into smaller ones and so increases the
*quantity* of petrol: C₁₆H₃₄ → C₈H₁₈ + C₈H₁₆. Reforming rearranges molecules of
about the same size into branched or aromatic forms and so increases the
*quality*: C₆H₁₄ → C₆H₆ + 4H₂. Cracking uses 750–900 K, or a zeolite catalyst at
700–800 K; reforming uses Pt/Al₂O₃ at about 770 K and 10–20 atm.

**7.** Definitions as in Section 12.7. A petrol engine needs a fuel that will
*not* ignite before the spark, so it needs branched and aromatic molecules; a
diesel engine ignites its fuel by compression and needs one that ignites as
readily as possible, so it needs straight-chain alkanes. The two requirements are
opposite, so a high-octane fuel necessarily has a low cetane number.
:::

**Group C — Long answer (8 marks each)**

1. (a) Classify organic compounds on the basis of the carbon skeleton, giving one
   example of each class. <span class="marks">[4]</span>
   (b) Define isomerism and classify it. Draw and name all seven isomers of
   C₄H₁₀O, stating the type of isomerism in each case. <span class="marks">[4]</span>
2. (a) State the rules of IUPAC nomenclature and use them to name
   CH₃–CH(CH₃)–CH₂–CH(OH)–CH₃ and CH₃–CH=CH–COOH. <span class="marks">[4]</span>
   (b) An organic compound contains 92.3% carbon and 7.7% hydrogen and has a
   vapour density of 13. Find its molecular formula. A petrol made largely from
   this kind of compound is blended, 75 L of octane number 96 with 25 L of octane
   number 84; find the octane number of the blend. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** (a) See the classification figure in Section 12.4 — acyclic (propane);
cyclic → homocyclic → alicyclic (cyclohexane); homocyclic → aromatic → benzenoid
(benzene) and non-benzenoid (azulene); heterocyclic (pyridine).
(b) See Worked example 12.2: four alcohols (butan-1-ol, butan-2-ol,
2-methylpropan-1-ol, 2-methylpropan-2-ol) and three ethers (methoxypropane,
2-methoxypropane, ethoxyethane). Alcohol against alcohol is chain or position
isomerism; ether against ether is metamerism; alcohol against ether is functional
isomerism.

**2.** (a) Rules as in Section 12.5. For CH₃–CH(CH₃)–CH₂–CH(OH)–CH₃ the parent
chain is five carbons and the OH must get the lowest locant, so number from the
right: the OH is on C2 and the methyl on C4 — **4-methylpentan-2-ol**. For
CH₃–CH=CH–COOH the –COOH carbon is C1, the chain has four carbons and the double
bond lies between C2 and C3 — **but-2-enoic acid**.

(b) C: 92.3 ÷ 12 = 7.69; H: 7.7 ÷ 1 = 7.7; ratio 1 : 1, so the empirical formula
is CH with empirical mass 13. Molecular mass = 2 × 13 = 26, so
$n = 26/13 = 2$ and the molecular formula is **C₂H₂** (ethyne).
Blend: $\text{ON} = \dfrac{75(96) + 25(84)}{100} = \dfrac{7200 + 2100}{100} = 93$.
:::
