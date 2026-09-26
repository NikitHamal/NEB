---
subject: Chemistry
grade: 11
unit: 13
title: Fundamental Principles of Organic Chemistry
hours: 10
area: Organic Chemistry
---

Unit 12 taught you what organic compounds are. This unit teaches you the working
grammar of the subject: how to give every compound a name that no two chemists
can disagree about, how to prove by experiment which elements a compound
contains, how the same set of atoms can build several different substances, and
why some bonds break one way and some the other. Ten hours of the syllabus are
spent here because everything in Units 14 and 15 — and the whole of the Grade 12
organic course — is written in this language.

::: key What the examiner asks from this unit
Four skills carry almost every mark: (1) name any compound of up to six carbons
and go back from the name to the structure; (2) write the Lassaigne equations
with the colour of each product; (3) draw and classify isomers, including cis /
trans and d / l; and (4) use the inductive and resonance effects to *explain* an
order of acid strength or carbocation stability. Notice that the last one is
always "explain", never "state".
:::

## 13.1 IUPAC Nomenclature of Organic Compounds (up to chain having 6 carbon atoms)

Before 1892 every compound had a trivial name — acetic acid, glycerol, urea —
which told you nothing about its structure. The **IUPAC system** (International
Union of Pure and Applied Chemistry) builds a name out of pieces, so that the
name and the structure can always be converted into each other.

An IUPAC name has up to four parts:

**secondary prefix + word root + primary suffix + secondary suffix**

| Part | What it gives | Examples |
|---|---|---|
| Secondary prefix | substituents that are not the principal group | methyl-, ethyl-, chloro-, nitro-, hydroxy-, amino- |
| Word root | number of carbons in the principal chain | meth (1), eth (2), prop (3), but (4), pent (5), hex (6) |
| Primary suffix | saturation of the chain | -ane, -ene, -yne |
| Secondary suffix | the principal functional group | -ol, -al, -one, -oic acid, -amine |

```figure caption="How an IUPAC name is assembled. Each piece of the name answers one question about the structure, and the pieces are always written in this order."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(2, 1, figsize=(5.0,3.4),
                         gridspec_kw={'height_ratios':[1.25,1.0]})
for a in axes:
    a.axis('off')

ax = axes[0]
V = [(0.0,0.0),(0.8,0.46),(1.6,0.0),(2.4,0.46),(3.2,0.0),(4.0,0.46)]
for i in (0,1,3,4):
    (x1,y1),(x2,y2) = V[i], V[i+1]
    ax.plot([x1,x2],[y1,y2], color=INK, lw=1.8, solid_capstyle='round')
(x1,y1),(x2,y2) = V[2], V[3]
dx, dy = x2-x1, y2-y1
L = np.hypot(dx,dy); nx, ny = -dy/L, dx/L
for s in (0.075,-0.075):
    ax.plot([x1+nx*s, x2+nx*s],[y1+ny*s, y2+ny*s], color='#d9534f', lw=1.8)
ax.plot([0.8,0.8],[0.46,1.18], color=INK, lw=1.8)
ax.text(0.8, 1.40, 'OH', fontsize=10.5, color='#1d6fb8', ha='center', va='center')
ax.plot([3.2,3.2],[0.0,-0.72], color=INK, lw=1.8)
ax.text(3.2,-0.95, 'CH₃', fontsize=9.2, color='#2e8b57', ha='center', va='center')
offs = [(-0.05,-0.30),(-0.30,0.16),(-0.02,-0.30),(0.16,0.26),(0.34,-0.12),(0.14,0.26)]
for i,((x,y),(ox,oy)) in enumerate(zip(V, offs), 1):
    ax.plot([x],[y], marker='o', ms=3.2, color=MUTED)
    ax.text(x+ox, y+oy, str(i), fontsize=7.6, color=MUTED, ha='center', va='center')
ax.text(5.35, 0.30, 'C₇H₁₄O', fontsize=9.0, color=INK, ha='center', va='center')
ax.set_xlim(-0.9, 6.1); ax.set_ylim(-1.35, 1.75); ax.set_aspect('equal')

ax = axes[1]
ax.set_xlim(0,4); ax.set_ylim(0,1)
parts = [('5-methyl', '#2e8b57', 'secondary prefix\n(substituent + locant)'),
         ('hex',      INK,       'word root\n6 carbons in chain'),
         ('-3-en',    '#d9534f', 'primary suffix\nC=C between C3 and C4'),
         ('-2-ol',    '#1d6fb8', 'secondary suffix\nOH on C2')]
for xi,(txt,col,note) in zip([0.5,1.5,2.5,3.5], parts):
    ax.text(xi, 0.84, txt, fontsize=11.0, color=col, ha='center', va='center',
            fontweight='bold')
    ax.plot([xi,xi],[0.68,0.74], color=MUTED, lw=0.8)
    ax.text(xi, 0.50, note, fontsize=7.0, color=MUTED, ha='center', va='center',
            linespacing=1.35)
ax.plot([0.15,3.85],[0.29,0.29], color=GRID, lw=1.0)
ax.text(2.0, 0.11, '5-methylhex-3-en-2-ol', fontsize=12.5, color=INK,
        ha='center', va='center')
fig.tight_layout()
```

### The naming rules, in the order you apply them

1. **Find the principal chain.** It is the longest continuous chain of carbon
   atoms that contains the principal functional group, and then the greatest
   number of multiple bonds. If two chains are equally long, take the one with
   more substituents.
2. **Find the principal functional group.** If a molecule has more than one, only
   the senior one gets a suffix; the rest become prefixes. The seniority order is

   —COOH > —COOR (ester) > —COCl > —CONH₂ > —CN > —CHO > >C=O > —OH > —NH₂ >
   C=C > C≡C

3. **Number the chain** from the end that gives the **lowest locant to the
   principal functional group**. If there is no functional group, number to give
   the lowest locant to the multiple bond; if there is neither, number to give
   the lowest set of locants to the substituents (**first point of difference**
   rule).
4. **Name the substituents** and put them in **alphabetical order**, each with
   its locant. The multiplying prefixes di-, tri-, tetra- are *not* counted when
   alphabetising, so 4-ethyl-2-methylhexane has ethyl before methyl, and
   2,3-dimethylpentane files under "m".
5. **Assemble and elide.** Drop the final "e" of -ane/-ene/-yne when the next
   letter is a vowel: hexan-2-**ol** (not hexane-2-ol), but hexane-1,2-**diol**
   (the "e" survives before a consonant).

| Class | Group | Prefix | Suffix | Example (IUPAC name) |
|---|---|---|---|---|
| Carboxylic acid | —COOH | carboxy- | -oic acid | CH₃COOH ethanoic acid |
| Ester | —COOR | alkoxycarbonyl- | alkyl …oate | CH₃COOC₂H₅ ethyl ethanoate |
| Acid chloride | —COCl | chlorocarbonyl- | -oyl chloride | CH₃COCl ethanoyl chloride |
| Amide | —CONH₂ | carbamoyl- | -amide | CH₃CONH₂ ethanamide |
| Nitrile | —C≡N | cyano- | -nitrile | CH₃CN ethanenitrile |
| Aldehyde | —CHO | oxo- / formyl- | -al | CH₃CH₂CHO propanal |
| Ketone | >C=O | oxo- | -one | CH₃COCH₃ propanone |
| Alcohol | —OH | hydroxy- | -ol | C₂H₅OH ethanol |
| Amine | —NH₂ | amino- | -amine | CH₃NH₂ methanamine |
| Ether | —OR | alkoxy- | — | CH₃OC₂H₅ methoxyethane |
| Halide | —X | fluoro-, chloro-, bromo-, iodo- | — | CH₃Cl chloromethane |
| Nitro | —NO₂ | nitro- | — | CH₃NO₂ nitromethane |

The common alkyl groups up to C4 are worth memorising, because NEB questions
still quote the trivial names:

| Structure | IUPAC name | Trivial name |
|---|---|---|
| CH₃— | methyl | methyl |
| CH₃CH₂— | ethyl | ethyl |
| CH₃CH₂CH₂— | propyl | n-propyl |
| (CH₃)₂CH— | propan-2-yl | isopropyl |
| CH₃CH₂CH₂CH₂— | butyl | n-butyl |
| CH₃CH₂CH(CH₃)— | butan-2-yl | sec-butyl |
| (CH₃)₂CHCH₂— | 2-methylpropyl | isobutyl |
| (CH₃)₃C— | 2-methylpropan-2-yl | tert-butyl |

::: example Worked example 13.1 — naming four compounds
**Problem.** Give the IUPAC name of
(a) CH₃CH₂CH(CH₃)CH₂CH₂CH₃, (b) (CH₃)₂C=CHCH₂CH₃,
(c) CH₃CH(OH)CH₂CHO, (d) (CH₃)₂CHCH₂CH(CH₃)COOH.

**Solution.**

(a) The longest chain is six carbons, so the root is **hex** and there is no
functional group, so the suffix is **-ane**. One methyl branch. Numbering from
the left puts it on C3; from the right, on C4. Lowest locant wins:
**3-methylhexane**.

(b) The principal chain must contain the C=C. The longest such chain is
CH₃—C(CH₃)=CH—CH₂—CH₃, five carbons, so the root is **pent** and the suffix
**-ene**. Numbering from the left gives the double bond the locant 2 (it starts
at C2); from the right it would be 3. So the chain is pent-2-ene with a methyl
on C2: **2-methylpent-2-ene**.

(c) Two groups are present, —CHO and —OH. The aldehyde is senior, so it takes
the suffix and *must* be C1. The chain is four carbons: **butanal**. The OH sits
on C3 and becomes the prefix hydroxy-: **3-hydroxybutanal**.

(d) The —COOH carbon is C1. Reading back: C1 = COOH, C2 = CH(CH₃),
C3 = CH₂, C4 = CH(CH₃), C5 = CH₃. The chain is five carbons with methyls on
C2 and C4: **2,4-dimethylpentanoic acid** (C₇H₁₄O₂).
:::

::: caution Three naming traps that cost easy marks
1. The longest chain is not always the one drawn horizontally — count every
   branch as a possible continuation.
2. The carbon of —COOH, —CHO, —CN and —COCl is **part of the chain and is
   always C1**. Ethanoic acid is "eth", not "meth".
3. Once the principal functional group has fixed the numbering, you may not
   renumber to give a substituent a lower locant. 3-hydroxybutanal can never be
   called 2-hydroxybutanal.
:::

## 13.2 Qualitative analysis: detection of N, S and halogens by Lassaigne's test

In an organic compound nitrogen, sulphur and the halogens are joined by
**covalent** bonds, so the ordinary inorganic tests — which need free ions — give
nothing. **Lassaigne's test** solves this by first converting the covalent
element into an ionic sodium salt.

::: definition Sodium fusion (Lassaigne's) extract
A small piece of clean, dry sodium is heated in an ignition tube until it melts,
the organic compound is added, and the tube is heated to redness and then plunged
while hot into about 20 cm³ of distilled water in a china dish. The tube
shatters; the mixture is boiled and filtered. The clear, alkaline filtrate is the
**sodium fusion extract** or **Lassaigne's extract**.
:::

During the fusion sodium reduces the elements into ionic salts:

Na + C + N --fuse--> NaCN

2Na + S --fuse--> Na₂S

Na + X --fuse--> NaX   (X = Cl, Br, I)

If nitrogen **and** sulphur are both present and sodium is not in excess, they
combine instead as sodium thiocyanate:

Na + C + N + S --fuse--> NaSCN

```figure caption="Lassaigne's test. The fusion turns covalently bonded N, S and X into the ions CN⁻, S²⁻ and X⁻, which ordinary inorganic tests can then detect."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,4.4))
ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0.85,10.4)

def box(x, y, w, h, txt, fc, ec, fs=7.2, tc=None):
    ax.add_patch(plt.Rectangle((x-w/2, y-h/2), w, h, facecolor=fc,
                               edgecolor=ec, lw=1.0, zorder=1))
    ax.text(x, y, txt, ha='center', va='center', fontsize=fs,
            color=tc or INK, zorder=2, linespacing=1.40)

def down(x, y1, y2, lab=None, xl=0.12):
    ax.annotate('', xy=(x, y2), xytext=(x, y1),
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.1,
                                mutation_scale=10))
    if lab:
        ax.text(x+xl, (y1+y2)/2, lab, fontsize=6.6, color=MUTED,
                ha='left', va='center')

box(5.0, 9.85, 9.2, 0.90,
    'organic compound  +  metallic Na,  heated to redness in an ignition tube\n'
    'Na + C + N → NaCN      2Na + S → Na₂S      Na + X → NaX',
    '#eef3f9', ACCENT, 7.0)
down(5.0, 9.40, 8.92, 'plunge hot tube into water, boil, filter')
box(5.0, 8.50, 5.4, 0.72, 'sodium fusion (Lassaigne’s) extract',
    '#eef3f9', ACCENT, 7.6)

for x in (1.75, 5.0, 8.25):
    ax.annotate('', xy=(x, 7.35), xytext=(5.0, 8.14),
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.0,
                                mutation_scale=9,
                                connectionstyle='arc3,rad=0.0'))

cols = ['#2e8b57', '#b8860b', '#6a5acd']
heads = ['test for N', 'test for S', 'test for halogen']
reag = ['add fresh FeSO₄,\nboil, cool, then\nacidify with\ndil. H₂SO₄',
        '(i) sodium nitroprusside\n(ii) lead acetate +\n     CH₃COOH',
        'boil with dil. HNO₃\nto expel HCN and H₂S,\nthen add AgNO₃']
obs  = ['Prussian blue\nFe₄[Fe(CN)₆]₃',
        '(i) deep violet\n(ii) black ppt PbS',
        'white ppt → Cl\npale yellow → Br\nyellow ppt → I']
for x, c, hd, rg, ob in zip((1.75, 5.0, 8.25), cols, heads, reag, obs):
    box(x, 7.00, 2.85, 0.70, hd, 'white', c, 7.4, c)
    down(x, 6.65, 5.95)
    box(x, 5.20, 2.85, 1.50, rg, '#fbfbfc', GRID, 6.6)
    down(x, 4.45, 3.80)
    box(x, 3.10, 2.85, 1.40, ob, '#f4f8f4', c, 6.8)

ax.text(5.0, 1.75,
        'If N and S are both present the extract contains SCN⁻ instead:\n'
        'with FeCl₃ it gives a blood-red colour, Fe(SCN)₃, and no Prussian blue.',
        ha='center', va='center', fontsize=6.9, color=MUTED, linespacing=1.45,
        bbox=dict(boxstyle='round,pad=0.42', fc='#fdf6ec', ec='#b8860b', lw=0.9))
fig.tight_layout()
```

### Detection of nitrogen

The extract is boiled with freshly prepared iron(II) sulphate solution and then
acidified with dilute sulphuric acid. A **Prussian blue** colour or precipitate
confirms nitrogen.

6NaCN + FeSO₄ → Na₄[Fe(CN)₆] + Na₂SO₄

3Na₄[Fe(CN)₆] + 2Fe₂(SO₄)₃ → Fe₄[Fe(CN)₆]₃↓ + 6Na₂SO₄   (Prussian blue)

Some of the Fe²⁺ is oxidised to Fe³⁺ by air during the boiling; the acid then
dissolves the greenish iron hydroxides so that the blue colour can be seen.

### Detection of sulphur

Two independent tests are used.

1. **Sodium nitroprusside test.** A few drops of sodium nitroprusside give a deep
   violet or purple colour:

   Na₂S + Na₂[Fe(CN)₅NO] → Na₄[Fe(CN)₅NOS]   (violet)

2. **Lead acetate test.** Acidify with acetic acid and add lead acetate; a black
   precipitate of lead sulphide appears:

   Na₂S + (CH₃COO)₂Pb → PbS↓ + 2CH₃COONa   (black)

### Detection of nitrogen and sulphur together

If both are present as SCN⁻, adding iron(III) chloride gives a blood-red colour:

FeCl₃ + 3NaSCN → Fe(SCN)₃ + 3NaCl   (blood red)

Fusing with **excess** sodium destroys the thiocyanate (NaSCN + 2Na → NaCN +
Na₂S), after which the ordinary nitrogen and sulphur tests both work.

### Detection of halogens

The extract is first boiled with dilute nitric acid. This is essential: any
cyanide or sulphide left in solution would precipitate AgCN and Ag₂S and give a
false positive.

NaCN + HNO₃ → NaNO₃ + HCN↑

Na₂S + 2HNO₃ → 2NaNO₃ + H₂S↑

Silver nitrate solution is then added:

NaX + AgNO₃ → AgX↓ + NaNO₃

| Halogen | Precipitate | Colour | In excess NH₄OH |
|---|---|---|---|
| Chlorine | AgCl | white, curdy | completely soluble |
| Bromine | AgBr | pale yellow | sparingly soluble |
| Iodine | AgI | bright yellow | insoluble |

::: caution Where Lassaigne's test fails
The test does not work for **diazonium salts**, because they lose their nitrogen
as N₂ gas before the sodium can react with it. Also, the sodium must be *dry* and
freshly cut, the tube must be red hot, and the fusion mixture must be plunged in
while still hot — otherwise unreacted sodium survives and the extract is unsafe.
:::

For completeness: **carbon and hydrogen** are detected by heating the compound
with dry copper(II) oxide. The carbon dioxide turns lime water milky and the
water condensing on the cool part of the tube turns anhydrous copper sulphate
from white to blue.

## 13.3 Isomerism: definition and classification

::: definition Isomerism
**Isomers** are two or more different compounds that have the *same molecular
formula* but *different arrangements of atoms*, and therefore different physical
and/or chemical properties. The phenomenon is called **isomerism** (Greek *isos*,
equal; *meros*, part).
:::

Isomerism exists because carbon is tetravalent and catenates: for a given
formula there is usually more than one way to join the atoms up. The number of
possibilities rises very fast — C₄H₁₀ has 2 isomers, C₅H₁₂ has 3, C₆H₁₄ has 5,
C₁₀H₂₂ has 75 and C₂₀H₄₂ has 366 319.

```figure caption="The classification of isomerism. Structural isomers differ in the order in which the atoms are joined; stereoisomers are joined identically but arranged differently in space."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.1,3.1))
ax.axis('off'); ax.set_xlim(0,12); ax.set_ylim(0,7.4)

def node(x, y, w, h, txt, fc, ec, fs=7.0, tc=None):
    ax.add_patch(plt.Rectangle((x-w/2, y-h/2), w, h, facecolor=fc,
                               edgecolor=ec, lw=1.0, zorder=2))
    ax.text(x, y, txt, ha='center', va='center', fontsize=fs,
            color=tc or INK, zorder=3, linespacing=1.35)

def elbow(x0, y0, x1, y1, col):
    ym = (y0 + y1) / 2 + 0.22
    ax.plot([x0, x0], [y0, ym], color=col, lw=1.0, zorder=1)
    ax.plot([x0, x1], [ym, ym], color=col, lw=1.0, zorder=1)
    ax.annotate('', xy=(x1, y1), xytext=(x1, ym),
                arrowprops=dict(arrowstyle='-|>', color=col, lw=1.0,
                                mutation_scale=9), zorder=1)

node(6.0, 6.85, 3.0, 0.72, 'ISOMERISM', '#eef3f9', ACCENT, 8.4, ACCENT)
node(3.2, 5.20, 4.4, 0.78,
     'Structural (constitutional)\ndifferent order of bonding',
     '#f4f8f4', '#2e8b57', 6.9)
node(8.8, 5.20, 4.4, 0.78,
     'Stereoisomerism\nsame order, different in space',
     '#faf2f2', '#d9534f', 6.9)
elbow(6.0, 6.49, 3.2, 5.59, MUTED)
elbow(6.0, 6.49, 8.8, 5.59, MUTED)

left = [('Chain', 'butane /\n2-methylpropane'),
        ('Position', 'propan-1-ol /\npropan-2-ol'),
        ('Functional', 'ethanol /\nmethoxymethane'),
        ('Metamerism', 'ethoxyethane /\n1-methoxypropane'),
        ('Tautomerism', 'keto ⇌ enol')]
for i, (t, e) in enumerate(left):
    y = 3.95 - i*0.78
    node(2.1, y, 2.0, 0.62, t, 'white', '#2e8b57', 6.8, '#2e8b57')
    ax.text(3.30, y, e, fontsize=5.9, color=MUTED, ha='left', va='center',
            linespacing=1.3)
    ax.plot([0.95, 1.10], [y, y], color='#2e8b57', lw=1.0)
ax.plot([0.95, 0.95], [3.95, 0.83], color='#2e8b57', lw=1.0)
ax.plot([0.95, 0.95], [3.95, 4.81], color='#2e8b57', lw=1.0)
ax.plot([0.95, 3.20], [4.81, 4.81], color='#2e8b57', lw=1.0)

right = [('Geometrical', 'cis / trans\nbut-2-ene'),
         ('Optical', 'd / l\nlactic acid')]
for i, (t, e) in enumerate(right):
    y = 3.95 - i*0.78
    node(7.9, y, 2.0, 0.62, t, 'white', '#d9534f', 6.8, '#d9534f')
    ax.text(9.10, y, e, fontsize=5.9, color=MUTED, ha='left', va='center',
            linespacing=1.3)
    ax.plot([6.75, 6.90], [y, y], color='#d9534f', lw=1.0)
ax.plot([6.75, 6.75], [3.95, 3.17], color='#d9534f', lw=1.0)
ax.plot([6.75, 6.75], [3.95, 4.81], color='#d9534f', lw=1.0)
ax.plot([6.75, 8.80], [4.81, 4.81], color='#d9534f', lw=1.0)
fig.tight_layout()
```

## 13.4 Structural isomerism: chain, position, functional, metamerism and tautomerism

**Structural isomers** have the same molecular formula but a different
*connectivity* — the atoms are bonded to different partners. Five types are
examined.

### Chain isomerism

The isomers differ in the **length or branching of the carbon skeleton**. It
begins at C₄.

- C₄H₁₀: CH₃CH₂CH₂CH₃ (butane) and (CH₃)₃CH (2-methylpropane)
- C₅H₁₂: pentane, 2-methylbutane, 2,2-dimethylpropane
- C₆H₁₄: hexane, 2-methylpentane, 3-methylpentane, 2,2-dimethylbutane,
  2,3-dimethylbutane — five in all

### Position isomerism

The skeleton is the same; the **functional group or multiple bond sits on a
different carbon**.

- C₃H₈O: CH₃CH₂CH₂OH (propan-1-ol) and CH₃CH(OH)CH₃ (propan-2-ol)
- C₄H₈: CH₂=CHCH₂CH₃ (but-1-ene) and CH₃CH=CHCH₃ (but-2-ene)
- C₆H₄Cl₂: 1,2-, 1,3- and 1,4-dichlorobenzene

### Functional isomerism

The isomers contain **different functional groups altogether**, so they belong to
different families and behave completely differently.

| Formula | Isomer 1 | Isomer 2 |
|---|---|---|
| C₂H₆O | ethanol CH₃CH₂OH (liquid, b.p. 78 °C) | methoxymethane CH₃OCH₃ (gas, b.p. −24 °C) |
| C₃H₆O | propanal CH₃CH₂CHO | propanone CH₃COCH₃ |
| C₂H₄O₂ | ethanoic acid CH₃COOH | methyl methanoate HCOOCH₃ |
| C₃H₉N | propan-1-amine (1°) | N-methylethanamine (2°) |

### Metamerism

::: definition Metamerism
**Metamers** are isomers that contain the *same functional group* but *different
alkyl groups on either side of a polyvalent atom or group* such as —O—, —S—,
—CO— or —NH—.
:::

- C₄H₁₀O ethers: C₂H₅—O—C₂H₅ (ethoxyethane) and CH₃—O—C₃H₇ (1-methoxypropane)
- C₅H₁₀O ketones: CH₃—CO—C₃H₇ (pentan-2-one) and C₂H₅—CO—C₂H₅ (pentan-3-one)

Metamerism is really a special case of chain/position isomerism, but NEB lists it
separately, so learn the definition word for word.

### Tautomerism

::: definition Tautomerism
**Tautomers** are structural isomers that exist together in **dynamic
equilibrium** and interconvert by the migration of a hydrogen atom from one atom
to another, with a shift of the double bond.
:::

The common type is **keto–enol tautomerism**, which needs at least one hydrogen
on the carbon next to the carbonyl (an α-hydrogen):

CH₃—CO—CH₃ ⇌ CH₃—C(OH)=CH₂

(keto form) ⇌ (enol form)

At room temperature propanone is 99.99 % keto; ethyl acetoacetate,
CH₃COCH₂COOC₂H₅, is about 93 % keto and 7 % enol, because its enol is stabilised
by conjugation and an internal hydrogen bond. The keto form normally dominates
because the C=O bond (≈ 749 kJ mol⁻¹) is much stronger than the C=C bond
(≈ 614 kJ mol⁻¹).

::: caution Tautomers are not resonance structures
Resonance structures are *imaginary* forms of **one** substance and differ only
in where the electrons are drawn. Tautomers are **two real, separable
substances** and differ in where an *atom* (the hydrogen) actually is. Never
join tautomers with a double-headed resonance arrow — use the equilibrium
arrows ⇌.
:::

::: example Worked example 13.2 — counting and classifying isomers
**Problem.** Write all the structural isomers of C₄H₁₀O and state the type of
isomerism relating each pair you name.

**Solution.** C₄H₁₀O is saturated (degree of unsaturation zero) with one oxygen,
so it is either an **alcohol** or an **ether**.

*Alcohols* — put —OH on each distinct position of the two C₄ skeletons:

1. CH₃CH₂CH₂CH₂OH — butan-1-ol
2. CH₃CH₂CH(OH)CH₃ — butan-2-ol
3. (CH₃)₂CHCH₂OH — 2-methylpropan-1-ol
4. (CH₃)₃COH — 2-methylpropan-2-ol

*Ethers* — split the four carbons across the oxygen as 1 + 3 or 2 + 2:

5. CH₃—O—CH₂CH₂CH₃ — 1-methoxypropane
6. CH₃—O—CH(CH₃)₂ — 2-methoxypropane
7. CH₃CH₂—O—CH₂CH₃ — ethoxyethane

**Seven isomers.** Relationships: 1 and 2 are *position* isomers; 1 and 3 are
*chain* isomers; any alcohol and any ether are *functional* isomers; 5 and 7 are
*metamers*; 5 and 6 are *chain* isomers.
:::

## 13.5 Geometrical isomerism (cis and trans) and optical isomerism (d and l form)

Stereoisomers have the same connectivity. They differ only in the
three-dimensional arrangement of the atoms.

### Geometrical (cis–trans) isomerism

A C=C double bond cannot rotate: rotating it would mean breaking the π bond,
which costs about 250 kJ mol⁻¹. The groups on the two carbons are therefore
locked in place.

::: key Condition for geometrical isomerism
There must be **restricted rotation** (a C=C bond or a ring), **and each of the
two doubly bonded carbons must carry two different groups.** If either carbon
carries two identical groups, the two "arrangements" are the same molecule and
there is no geometrical isomerism.
:::

- but-2-ene CH₃CH=CHCH₃ — each carbon carries CH₃ and H → **yes**, cis and trans
- but-1-ene CH₂=CHCH₂CH₃ — C1 carries two H → **no**
- 2-methylbut-2-ene (CH₃)₂C=CHCH₃ — C2 carries two CH₃ → **no**

In the **cis** isomer the two like groups are on the same side of the double
bond; in the **trans** isomer they are on opposite sides.

| Property | cis isomer | trans isomer |
|---|---|---|
| Position of like groups | same side | opposite sides |
| Dipole moment | bond dipoles add — polar | dipoles cancel — zero or small |
| Boiling point | higher (stronger dipole–dipole forces) | lower |
| Melting point | lower (packs badly, less symmetric) | higher (packs well) |
| Stability | lower (the two groups crowd each other) | higher |
| Solubility in water | greater | smaller |

The standard NEB illustration is the pair of butenedioic acids. **Maleic acid**
(cis) melts at 130 °C, is very soluble in water and loses water on heating to
give maleic anhydride. **Fumaric acid** (trans) melts at 287 °C, is much less
soluble and forms no anhydride, because its two —COOH groups are too far apart
to reach each other.

### Optical isomerism

::: definition Optical isomerism
A substance is **optically active** if it rotates the plane of plane-polarised
light. Two isomers that are **non-superimposable mirror images** of each other
are called **enantiomers** or **optical isomers**; one rotates the plane to the
right (**dextrorotatory**, d or +) and the other by exactly the same angle to the
left (**laevorotatory**, l or −).
:::

The usual cause is a **chiral (asymmetric) carbon** — a carbon atom joined to
**four different** groups. Such a molecule has no plane of symmetry, so its
mirror image cannot be laid on top of it, just as a left hand cannot be laid on a
right hand.

```figure caption="The two enantiomers of lactic acid. The bold wedge points towards you and the hashed bond away from you. The two structures are mirror images that cannot be superimposed however they are turned."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(5.0,3.0))

def wedge(ax, x0, y0, x1, y1, col=INK, w=0.10):
    dx, dy = x1-x0, y1-y0
    L = np.hypot(dx, dy); nx, ny = -dy/L, dx/L
    ax.add_patch(plt.Polygon([[x0, y0], [x1+nx*w, y1+ny*w],
                              [x1-nx*w, y1-ny*w]], closed=True,
                             facecolor=col, edgecolor=col, lw=0.6, zorder=2))

def hashed(ax, x0, y0, x1, y1, col=INK, n=6):
    dx, dy = x1-x0, y1-y0
    L = np.hypot(dx, dy); nx, ny = -dy/L, dx/L
    for i in range(1, n+1):
        f = i/(n+0.4); w = 0.028 + 0.075*f
        cx, cy = x0+dx*f, y0+dy*f
        ax.plot([cx-nx*w, cx+nx*w], [cy-ny*w, cy+ny*w], color=col, lw=1.3,
                zorder=2)

def centre(ax, s, title):
    # bonds at 60, 150, 240, 330 degrees (s = +1 left panel, -1 mirrored panel)
    spec = [(60, 'COOH', '#d9534f', 'plain'),
            (150, 'H',   ACCENT,    'hash'),
            (240, 'CH₃', '#2e8b57', 'plain'),
            (330, 'OH',  ACCENT,    'wedge')]
    for deg, lab, col, kind in spec:
        a = np.radians(deg)
        x, y = s*np.cos(a), np.sin(a)
        x0, y0 = 0.22*x, 0.22*y
        x1, y1 = 0.88*x, 0.88*y
        if kind == 'plain':
            ax.plot([x0, x1], [y0, y1], color=INK, lw=1.6)
        elif kind == 'wedge':
            wedge(ax, x0, y0, x1, y1)
        else:
            hashed(ax, x0, y0, x1, y1)
        ax.text(1.16*x, 1.16*y, lab, fontsize=9.4, color=col,
                ha='center', va='center')
    ax.text(0, 0, 'C', fontsize=11, color=INK, ha='center', va='center', zorder=3)
    ax.set_title(title, fontsize=8.6, color=INK, pad=6)
    ax.set_xlim(-1.70, 1.70); ax.set_ylim(-1.50, 1.50)
    ax.set_aspect('equal'); ax.axis('off')

centre(axes[0], 1, 'd-(+)-lactic acid')
centre(axes[1], -1, 'l-(−)-lactic acid')
fig.subplots_adjust(wspace=0.05)
fig.text(0.5, 0.14, 'mirror', ha='center', fontsize=7.4, color=MUTED)
fig.add_artist(plt.Line2D([0.5, 0.5], [0.20, 0.92], color=MUTED, lw=1.0,
                          linestyle=(0, (4, 3))))
```

Key facts about enantiomers:

- They have **identical** melting point, boiling point, density, solubility and
  ordinary chemical reactivity. They differ only in the **direction** in which
  they rotate polarised light, and in how they react with other chiral things
  (enzymes, other enantiomers, polarised light).
- A **racemic mixture** is an equimolar (50:50) mixture of the d and l forms. It
  is written (±) or dl and is **optically inactive by external compensation** —
  the rotation of one half exactly cancels the other.
- A **meso** compound has chiral carbons but also an internal plane of symmetry,
  so it is optically inactive by **internal compensation**. Tartaric acid
  therefore exists in three forms: d, l and meso.
- A molecule with **n** different chiral carbons has at most $2^{n}$ optical
  isomers (van't Hoff's rule).

The rotation is measured in a **polarimeter** and reported as the specific
rotation

$$ [\alpha]_{D}^{25} = \frac{\alpha}{l \times c} $$

where $\alpha$ is the observed rotation in degrees, $l$ the length of the tube in
decimetres and $c$ the concentration in g cm⁻³.

::: caution d/l is not D/L
The lower-case **d** and **l** used by NEB describe only the *observed direction
of rotation* (+ and −), which must be measured. The capital **D** and **L** used
in biology describe the *configuration* drawn in a Fischer projection. A compound
can be D and laevorotatory at the same time — L-(+)-arabinose is the classic
example. Do not mix the two notations.
:::

::: example Worked example 13.3 — which isomers exist?
**Problem.** (a) Which of these show geometrical isomerism: pent-2-ene,
2-methylbut-1-ene, 1,2-dichloroethene, 1,1-dichloroethene? (b) How many optical
isomers does 2,3-dihydroxybutanoic acid, CH₃CH(OH)CH(OH)COOH, have?

**Solution.**

(a) Apply the test carbon by carbon.

- **pent-2-ene**, CH₃CH=CHCH₂CH₃: C2 carries CH₃ and H, C3 carries C₂H₅ and H —
  both different, so **yes** (cis and trans).
- **2-methylbut-1-ene**, CH₂=C(CH₃)CH₂CH₃: C1 carries two H — **no**.
- **1,2-dichloroethene**, ClCH=CHCl: each carbon carries Cl and H — **yes**.
- **1,1-dichloroethene**, Cl₂C=CH₂: C1 carries two Cl and C2 two H — **no**.

(b) Number the carbons: C1 = COOH, C2 = CH(OH), C3 = CH(OH), C4 = CH₃.

- C2 is bonded to —COOH, —OH, —H and —CH(OH)CH₃: four different groups → chiral.
- C3 is bonded to —CH₃, —OH, —H and —CH(OH)COOH: four different groups → chiral.

So $n = 2$ and the number of optical isomers is $2^{2} = 4$ — two pairs of
enantiomers. (There is no meso form here, because the two chiral carbons do not
carry the same set of groups.)
:::

## 13.6 Reaction Mechanism: homolytic and heterolytic fission

::: definition Reaction mechanism
A **reaction mechanism** is the detailed, step-by-step description of how
reactants become products: which bonds break, which form, in what order, and
what short-lived intermediates appear on the way.
:::

Every organic reaction starts by breaking a covalent bond, and a shared pair can
be split in only two ways.

### Homolytic fission (homolysis)

The two bonded atoms take **one electron each**. Each fragment keeps an unpaired
electron and is a **free radical**. The movement of a single electron is shown
by a half-headed "fish-hook" arrow.

Cl—Cl --hν--> Cl• + Cl•

CH₃—CH₃ --Δ, 500 °C--> CH₃• + CH₃•

Homolysis is favoured by high temperature, ultraviolet light, peroxide
initiators, non-polar bonds and non-polar solvents such as CCl₄. The reactions
it starts are called **free-radical reactions**; substitution in alkanes
(Section 14.2) is the standard example.

### Heterolytic fission (heterolysis)

**Both electrons go to one atom** — the more electronegative one. Two oppositely
charged ions result, and the movement of the electron *pair* is shown by a full
curved arrow.

CH₃—Br → CH₃⁺ + Br⁻   (carbocation)

CH₃—MgBr → CH₃⁻ + MgBr⁺   (carbanion)

Heterolysis is favoured by polar bonds, polar solvents (which solvate and
stabilise the ions) and the presence of a catalyst such as AlCl₃ that can pull
the leaving group away. It gives **ionic (polar) reactions**.

```figure caption="Top: the two ways a shared pair can break. A single-barbed arrow moves one electron, a full arrow moves a pair. Bottom: the shape of the three reactive intermediates, with the stability order below each one."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(2, 3, figsize=(5.1,4.0),
                         gridspec_kw={'height_ratios':[1.0, 1.25]})
for a in axes.ravel():
    a.axis('off')

def bond_scene(ax, title, sub, arrows, prod, col):
    ax.text(0.0, 0.0, 'A', fontsize=10.5, color=INK, ha='center', va='center')
    ax.text(1.15, 0.0, 'B', fontsize=10.5, color=INK, ha='center', va='center')
    ax.plot([0.22, 0.93], [0, 0], color=INK, lw=1.5)
    ax.plot([0.50], [0.10], marker='o', ms=2.8, color=col)
    ax.plot([0.66], [0.10], marker='o', ms=2.8, color=col)
    for (xy, xytext, rad, style) in arrows:
        ax.annotate('', xy=xy, xytext=xytext,
                    arrowprops=dict(arrowstyle=style, color=col, lw=1.25,
                                    connectionstyle=f'arc3,rad={rad}',
                                    mutation_scale=10))
    ax.annotate('', xy=(2.35, 0.0), xytext=(1.58, 0.0),
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.1,
                                mutation_scale=10))
    ax.text(3.20, 0.0, prod, fontsize=9.6, color=INK, ha='center', va='center')
    ax.set_title(title, fontsize=8.0, color=col, pad=4)
    ax.text(1.95, -0.95, sub, fontsize=6.6, color=MUTED, ha='center', va='center')
    ax.set_xlim(-0.55, 4.25); ax.set_ylim(-1.30, 0.95)

bond_scene(axes[0, 0], 'homolysis', 'Cl₂ --hν--> 2Cl•',
           [((0.05, 0.40), (0.52, 0.22), 0.45, '->'),
            ((1.10, 0.40), (0.64, 0.22), -0.45, '->')],
           'A•  +  B•', '#d9534f')
bond_scene(axes[0, 1], 'heterolysis (i)', 'CH₃—Br → CH₃⁺ + Br⁻',
           [((1.16, 0.26), (0.55, 0.24), -0.5, '-|>')],
           'A⁺  +  B⁻', ACCENT)
bond_scene(axes[0, 2], 'heterolysis (ii)', 'CH₃—MgBr → CH₃⁻ + MgBr⁺',
           [((-0.02, 0.26), (0.60, 0.24), 0.5, '-|>')],
           'A⁻  +  B⁺', '#2e8b57')

from matplotlib.patches import Ellipse

def trigonal(ax, label, charge, order, col, mode):
    if mode == 'pyramidal':
        ends = [(-0.86, -0.42), (0.86, -0.42), (0.0, -0.92)]
    else:                       # planar sp2, bonds at 0, 120, 240 degrees
        ends = [(np.cos(np.radians(d)), np.sin(np.radians(d)))
                for d in (0, 120, 240)]
    for (x, y) in ends:
        ax.plot([0, x*0.80], [0, y*0.80], color=INK, lw=1.5)
        ax.text(x*1.06, y*1.10, 'R', fontsize=8.4, color=MUTED,
                ha='center', va='center')
    if mode != 'pyramidal':     # the perpendicular p orbital, seen edge-on
        for yc in (0.60, -0.60):
            ax.add_patch(Ellipse((0, yc), 0.30, 0.66, fill=False, ec=col,
                                 lw=1.0, ls=(0, (2.5, 2))))
    ax.text(0, 0, 'C', fontsize=11, color=col, ha='center', va='center',
            zorder=4, bbox=dict(boxstyle='circle,pad=0.12', fc='white', ec='none'))
    if charge:
        ax.text(0.40, 0.34, charge, fontsize=11, color=col, ha='center',
                va='center')
    if mode == 'pyramidal':     # lone pair in the sp3 orbital
        ax.plot([-0.10, 0.10], [0.52, 0.52], marker='o', ms=3.2, ls='none',
                color=col)
    if mode == 'radical':       # one electron in the p orbital
        ax.plot([0.0], [0.60], marker='o', ms=3.6, color=col)
    ax.set_title(label, fontsize=7.8, color=col, pad=3)
    ax.text(0.0, -1.52, order, fontsize=6.5, color=MUTED, ha='center',
            va='center', linespacing=1.4)
    ax.set_xlim(-1.45, 1.45); ax.set_ylim(-1.90, 1.25)
    ax.set_aspect('equal')

trigonal(axes[1, 0], 'carbocation  sp², planar', '+',
         'empty p orbital, 6 e⁻\n3° > 2° > 1° > CH₃⁺', ACCENT, 'cation')
trigonal(axes[1, 1], 'carbanion  sp³, pyramidal', '−',
         'lone pair, 8 e⁻\nCH₃⁻ > 1° > 2° > 3°', '#2e8b57', 'pyramidal')
trigonal(axes[1, 2], 'free radical  sp², planar', '',
         'one unpaired e⁻, 7 e⁻\n3° > 2° > 1° > CH₃•', '#d9534f', 'radical')
fig.tight_layout()
```

| | Homolytic fission | Heterolytic fission |
|---|---|---|
| Sharing of the pair | one electron to each atom | both electrons to one atom |
| Arrow | half-headed (fish-hook) | full curved arrow |
| Products | two free radicals | a cation and an anion |
| Favoured by | UV light, heat, peroxides, non-polar solvent | polar bond, polar solvent, catalyst |
| Energy needed | bond dissociation energy | usually less, if the ions are solvated |
| Reaction type produced | free-radical reactions | ionic (electrophilic / nucleophilic) reactions |

## 13.7 Electrophiles, nucleophiles and free radicals

The species produced by fission are the **reaction intermediates**; the species
that attack them are the **reagents**. Organic reagents are sorted by what they
do with electrons.

::: definition Electrophile and nucleophile
An **electrophile** ("electron loving") is an electron-deficient species that
accepts a pair of electrons — a Lewis acid. A **nucleophile** ("nucleus loving")
is an electron-rich species that donates a pair of electrons — a Lewis base.
:::

| | Electrophile (E⁺ or E) | Nucleophile (Nu⁻ or Nu) |
|---|---|---|
| Electron demand | deficient — accepts a pair | rich — donates a pair |
| Lewis character | acid | base |
| Attacks | the electron-rich site (π bond, benzene ring, C of C=O) | the electron-poor site (C of C—X, C of C=O) |
| Charged examples | H⁺, Cl⁺, Br⁺, NO₂⁺, NO⁺, R⁺, R—C≡O⁺ | OH⁻, CN⁻, Cl⁻, Br⁻, RO⁻, CH₃COO⁻, HSO₃⁻, R⁻ |
| Neutral examples | BF₃, AlCl₃, FeCl₃, ZnCl₂, SO₃, carbene :CCl₂ | H₂O, NH₃, ROH, RNH₂, R₃P, alkenes, benzene |

Two points examiners like:

- Every **carbocation is an electrophile** and every **carbanion is a
  nucleophile**, but the reverse is not true — BF₃ is an electrophile with no
  charge at all.
- **Ambident nucleophiles** such as CN⁻ and NO₂⁻ have two donor atoms and can
  attack through either, which is why KCN gives nitriles while AgCN gives
  isocyanides.

A **free radical** is the third kind of reactive species: an atom or group with
an **unpaired electron**, electrically neutral, paramagnetic and extremely
reactive. It is neither an electrophile nor a nucleophile, although it is
electron deficient.

| Intermediate | Electrons on C | Hybridisation | Shape | Stability order |
|---|---|---|---|---|
| Carbocation R₃C⁺ | 6 | sp² | trigonal planar, 120° | 3° > 2° > 1° > CH₃⁺ |
| Carbanion R₃C⁻ | 8 (incl. lone pair) | sp³ | pyramidal, ≈107° | CH₃⁻ > 1° > 2° > 3° |
| Free radical R₃C• | 7 | sp² | planar (shallow pyramid) | 3° > 2° > 1° > CH₃• |

The reason for the carbocation order is that alkyl groups release electrons
(+I effect) and also share the C—H electrons of the neighbouring carbon with the
empty p orbital (**hyperconjugation**); the more alkyl groups, the more the
positive charge is spread out and the more stable the ion. For a carbanion the
charge is negative, so electron-releasing alkyl groups make it *worse*, and the
order reverses.

## 13.8 Inductive effect (+I and −I); Resonance effect (+R and −R)

Substituents change how a molecule reacts by pushing or pulling electron density.
Two permanent electronic effects are on the syllabus.

### Inductive effect

::: definition Inductive effect
The **inductive effect** is the permanent displacement of the electrons of a
**σ bond** towards the more electronegative of the two atoms, and its relay along
the chain of σ bonds with rapidly decreasing intensity.
:::

Hydrogen is taken as the reference, so an effect is measured relative to a C—H
bond.

- **−I groups** (electron-withdrawing) pull electrons away from the chain. In
  decreasing order of strength:

  —NO₂ > —CN > —SO₃H > —CHO > —COOH > —F > —Cl > —Br > —I > —OR > —OH > —C₆H₅

- **+I groups** (electron-releasing) push electrons towards the chain:

  —O⁻ > —COO⁻ > —C(CH₃)₃ > —CH(CH₃)₂ > —CH₂CH₃ > —CH₃ > —H

The effect **dies away quickly**: its strength falls to roughly one-third at each
successive carbon, so it is negligible beyond the third carbon from the
substituent. That is why 4-chlorobutanoic acid is barely stronger than butanoic
acid, while 2-chlorobutanoic acid is much stronger.

```figure caption="Left: the −I effect of chlorine drains electron density from the carboxylate ion and so strengthens the acid — each extra chlorine lowers pKa (a lower pKa means a stronger acid). Right: the +R effect of the −NH₂ group in aniline pushes its lone pair into the ring, building up negative charge at the ortho and para positions."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(5.2,2.9),
                         gridspec_kw={'width_ratios':[1.12, 1.0]})

ax = axes[0]
names = ['CH₃CH₂COOH', 'CH₃COOH', 'ClCH₂COOH', 'Cl₂CHCOOH', 'Cl₃CCOOH']
pka   = [4.87, 4.76, 2.87, 1.29, 0.66]
cols  = [MUTED, MUTED, '#1d6fb8', '#1d6fb8', '#1d6fb8']
y = np.arange(len(pka))[::-1]
ax.barh(y, pka, color=cols, height=0.62)
for yi, p in zip(y, pka):
    ax.text(p + 0.14, yi, f'{p:.2f}', va='center', fontsize=7.2, color=INK)
ax.set_yticks(y); ax.set_yticklabels(names, fontsize=7.2)
ax.set_xlabel('pK$_a$   (smaller = stronger acid)', fontsize=7.8)
ax.set_xlim(0, 6.1)
ax.spines[['top', 'right']].set_visible(False)
ax.tick_params(axis='x', labelsize=7.0)
ax.annotate('more Cl,\nstronger −I,\nstronger acid', xy=(0.80, 0.08),
            xytext=(2.70, 0.55), fontsize=6.8, color='#1d6fb8',
            ha='center', va='center', linespacing=1.4,
            arrowprops=dict(arrowstyle='-|>', color='#1d6fb8', lw=1.0,
                            mutation_scale=9, connectionstyle='arc3,rad=0.25'))
ax.set_title('inductive effect', fontsize=8.4, color=INK, pad=5)

ax = axes[1]
ax.axis('off')
r = 1.0
ang = np.arange(6)*np.pi/3 + np.pi/6
xs, ys = r*np.cos(ang), r*np.sin(ang)
for i in range(6):
    j = (i+1) % 6
    ax.plot([xs[i], xs[j]], [ys[i], ys[j]], color=INK, lw=1.7,
            solid_capstyle='round')
ax.add_patch(plt.Circle((0, 0), 0.58, fill=False, ec=INK, lw=1.5))
ax.plot([xs[1], xs[1]], [ys[1], ys[1]+0.62], color=INK, lw=1.7)
ax.text(xs[1], ys[1]+0.86, 'NH₂', fontsize=10.0, color='#2e8b57',
        ha='center', va='center')
ax.plot([-0.10, 0.10], [ys[1]+0.62, ys[1]+0.62], marker='o', ms=2.6,
        ls='none', color='#2e8b57')
for idx in (0, 2, 4):
    ax.text(xs[idx]*1.42, ys[idx]*1.42, 'δ−', fontsize=8.6, color='#d9534f',
            ha='center', va='center')
ax.annotate('', xy=(0.0, 0.62), xytext=(0.0, ys[1]+0.52),
            arrowprops=dict(arrowstyle='-|>', color='#2e8b57', lw=1.3,
                            mutation_scale=10,
                            connectionstyle='arc3,rad=0.35'))
ax.text(0, -1.92, 'aniline:  +R effect of —NH₂\no and p positions enriched',
        fontsize=6.9, color=MUTED, ha='center', va='center', linespacing=1.4)
ax.set_xlim(-2.1, 2.1); ax.set_ylim(-2.35, 2.55); ax.set_aspect('equal')
ax.set_title('resonance effect', fontsize=8.4, color=INK, pad=5)
fig.tight_layout()
```

**Application 1 — strength of carboxylic acids.** An acid is strong when its
conjugate base is stable. A −I group drains negative charge away from the
carboxylate ion and stabilises it, so the acid is stronger:

| Acid | CH₃CH₂COOH | CH₃COOH | HCOOH | ClCH₂COOH | Cl₂CHCOOH | Cl₃CCOOH |
|---|---|---|---|---|---|---|
| pKa | 4.87 | 4.76 | 3.75 | 2.87 | 1.29 | 0.66 |

Formic acid beats acetic acid because it has no +I methyl group at all. Among the
monohalo acids, the more electronegative halogen wins: FCH₂COOH (2.59) >
ClCH₂COOH (2.87) > BrCH₂COOH (2.90) > ICH₂COOH (3.17).

**Application 2 — carbocation stability.** Alkyl groups are +I, so they feed
electron density into the electron-poor carbon: (CH₃)₃C⁺ > (CH₃)₂CH⁺ > CH₃CH₂⁺ >
CH₃⁺. This single fact explains Markovnikov's rule in Unit 14.

### Resonance (mesomeric) effect

::: definition Resonance effect
The **resonance** or **mesomeric effect** is the permanent polarisation produced
in a conjugated system by the delocalisation of **π electrons or a lone pair**
through the system. It is written +R (or +M) when the group *donates* electrons
to the system and −R (or −M) when it *withdraws* them.
:::

- **+R groups** carry a lone pair on the atom attached to the conjugated system
  and push it in: —OH, —OR, —NH₂, —NHR, —NR₂, —NHCOR, —OCOR, —F, —Cl, —Br, —I.
- **−R groups** have a multiply bonded electronegative atom and pull electron
  density out: —NO₂, —CN, —CHO, —COR, —COOH, —COOR, —CONH₂, —SO₃H.

Two properties distinguish resonance from induction and are worth a mark each:

| | Inductive effect | Resonance effect |
|---|---|---|
| Electrons involved | σ electrons | π electrons or a lone pair |
| Needs conjugation? | no | yes — a planar, conjugated system |
| Range | dies out after 2–3 σ bonds | transmitted right along the conjugated chain |
| Charge produced | partial (δ+, δ−) | full formal charges in the contributing structures |
| Magnitude | weaker | stronger |

For resonance to be possible the contributing structures must have the **same
positions for all nuclei**, the **same number of unpaired electrons**, and the
system must be **planar and conjugated**. The real molecule is a single
**resonance hybrid** — never one structure "changing into" another — and it is
always more stable than the most stable contributing structure. That extra
stability is the **resonance energy** (152 kJ mol⁻¹ for benzene, Unit 15).

**Application — acidity of phenol versus ethanol.** Phenol (pKa 10.0) is far more
acidic than ethanol (pKa 15.9), because the phenoxide ion C₆H₅O⁻ spreads its
negative charge over the ortho and para carbons of the ring by resonance, while
the ethoxide ion has nowhere to put it.

**Application — basicity of aniline versus ammonia.** In aniline the nitrogen
lone pair is delocalised into the ring (+R). It is therefore less available for
protonation, which is why aniline (pKb 9.4) is a much weaker base than ammonia
(pKb 4.75) or methylamine (pKb 3.4).

::: example Worked example 13.4 — reasoning with electronic effects
**Problem.** (a) Arrange in increasing order of acid strength: CH₃COOH,
CH₃CH₂COOH, ClCH₂COOH, FCH₂COOH, Cl₃CCOOH. (b) Which carbocation is more stable,
CH₃CH₂CH₂⁺ or (CH₃)₂CH⁺, and why? (c) 4-nitrophenol is a stronger acid than
phenol. Explain.

**Solution.**

(a) Start from ethanoic acid. Adding a +I ethyl group in place of a methyl
weakens the acid; adding −I halogens strengthens it, more halogens and more
electronegative halogens giving more strengthening. So, weakest first:

CH₃CH₂COOH < CH₃COOH < ClCH₂COOH < FCH₂COOH < Cl₃CCOOH

(pKa 4.87, 4.76, 2.87, 2.59, 0.66 — the pKa values confirm the order.)

(b) (CH₃)₂CH⁺ is a **secondary** carbocation with two +I methyl groups feeding
electron density into the empty p orbital, plus six α C—H bonds available for
hyperconjugation. CH₃CH₂CH₂⁺ is **primary**, with only one alkyl group and two
α C—H bonds. The secondary cation is therefore more stable.

(c) Acidity depends on the stability of the anion. In the 4-nitrophenoxide ion
the —NO₂ group is both strongly −I and strongly −R; because it sits at the para
position it is conjugated with the oxygen, so the negative charge can be
delocalised right onto the nitro oxygens. The anion is much more stable than
plain phenoxide, so the acid is stronger (pKa 7.15 against 10.0).
:::

::: memory Six things to have at your fingertips
1. Root words: meth, eth, prop, but, pent, hex.
2. Seniority: acid > ester > amide > nitrile > aldehyde > ketone > alcohol >
   amine > ene > yne.
3. Lassaigne colours: Prussian blue (N), violet and black (S), blood red (N+S),
   white / pale yellow / yellow (Cl, Br, I).
4. Five structural isomerisms: **C**hain, **P**osition, **F**unctional,
   **M**etamerism, **T**automerism — "Can Piyush Find My Tiffin?"
5. Carbocation and radical stability: 3° > 2° > 1° > methyl. Carbanion: reverse.
6. −I strongest: NO₂; +I strongest among alkyls: tert-butyl.
:::

## Chapter summary

- An IUPAC name is *secondary prefix + word root + primary suffix + secondary
  suffix*. Choose the longest chain containing the senior functional group,
  number for the lowest locant to that group, list substituents alphabetically,
  and elide the final "e" before a vowel.
- Lassaigne's test fuses the compound with sodium to make NaCN, Na₂S and NaX.
  Nitrogen gives Prussian blue Fe₄[Fe(CN)₆]₃; sulphur gives a violet nitroprusside
  colour and a black PbS precipitate; halogens give AgCl (white), AgBr (pale
  yellow) or AgI (yellow) after the extract is boiled with dilute HNO₃.
- Isomers share a molecular formula. Structural isomerism = chain, position,
  functional, metamerism, tautomerism. Stereoisomerism = geometrical and optical.
- Geometrical isomerism needs restricted rotation **and** two different groups on
  each doubly bonded carbon. Trans is the more stable and higher-melting; cis is
  the more polar and higher-boiling.
- Optical isomerism needs a chiral carbon (four different groups). Enantiomers
  rotate polarised light equally and oppositely; a 50:50 racemic mixture and a
  meso form are both optically inactive; $n$ chiral centres give up to $2^{n}$
  isomers.
- Homolysis splits the pair one electron each and gives free radicals;
  heterolysis gives both electrons to one atom and produces a carbocation or a
  carbanion. Carbocations and radicals are sp² and planar, 3° > 2° > 1°;
  carbanions are sp³ and pyramidal, with the order reversed.
- Electrophiles accept an electron pair (Lewis acids); nucleophiles donate one
  (Lewis bases); free radicals have one unpaired electron.
- The inductive effect works through σ bonds, is short-range and gives partial
  charges; the resonance effect works through a conjugated π system, is
  long-range and gives full charges. Both are permanent, and together they
  explain acid strength, base strength and carbocation stability.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The IUPAC name of (CH₃)₂CHCH₂CH₂OH is <span class="marks">[1]</span>
   (a) 2-methylbutan-1-ol (b) 3-methylbutan-1-ol (c) 2-methylbutan-4-ol (d) pentan-1-ol
2. Prussian blue in Lassaigne's test confirms the presence of <span class="marks">[1]</span>
   (a) sulphur (b) nitrogen (c) chlorine (d) phosphorus
3. Before testing for halogens the sodium extract is boiled with dilute HNO₃ in order to <span class="marks">[1]</span>
   (a) oxidise the halide (b) remove cyanide and sulphide ions (c) neutralise the sodium
   (d) increase the solubility of AgX
4. Ethoxyethane and 1-methoxypropane are <span class="marks">[1]</span>
   (a) chain isomers (b) tautomers (c) metamers (d) functional isomers
5. Which compound shows geometrical isomerism? <span class="marks">[1]</span>
   (a) 1,1-dichloroethene (b) 2-methylprop-1-ene (c) pent-2-ene (d) propene
6. A racemic mixture is optically inactive because of <span class="marks">[1]</span>
   (a) internal compensation (b) external compensation (c) the absence of a chiral carbon
   (d) a plane of symmetry in each molecule
7. Heterolytic fission of a covalent bond gives <span class="marks">[1]</span>
   (a) two free radicals (b) a cation and an anion (c) two cations (d) two atoms
8. Which of the following is the strongest −I group? <span class="marks">[1]</span>
   (a) —CH₃ (b) —OH (c) —I (d) —NO₂
9. The number of optical isomers of a compound with three different chiral carbons is <span class="marks">[1]</span>
   (a) 3 (b) 4 (c) 6 (d) 8

::: note Answers to Group A
**1.** (b) — the longest chain is four carbons with OH on C1 and a methyl on C3.
**2.** (b) — the CN⁻ from fused nitrogen ends up as Fe₄[Fe(CN)₆]₃.
**3.** (b) — otherwise AgCN and Ag₂S precipitate and give a false positive.
**4.** (c) — same functional group (ether) but different alkyl groups on the oxygen.
**5.** (c) — in CH₃CH=CHC₂H₅ each doubly bonded carbon carries two different groups.
**6.** (b) — the d and l halves rotate the plane equally and oppositely and cancel.
**7.** (b) — both electrons go to the more electronegative atom.
**8.** (d) — the nitro group heads the −I series.
**9.** (d) — $2^{n}$ with $n = 3$ gives 8.
:::

**Group B — Short answer (5 marks each)**

1. State the rules of IUPAC nomenclature and use them to name
   (i) CH₃CH₂CH(CH₃)CH₂CH₃ (ii) (CH₃)₂C=CHCH₃ (iii) CH₃CH(OH)CH₂CH₂CHO
   (iv) CH₃CH₂COOCH₃ <span class="marks">[5]</span>
2. How is Lassaigne's extract prepared? Describe with equations how nitrogen and
   sulphur are detected in it. <span class="marks">[5]</span>
3. Define isomerism and classify it with one example of each type. <span class="marks">[5]</span>
4. What are the necessary conditions for geometrical isomerism? Draw the cis and
   trans forms of but-2-ene and give three ways in which their properties
   differ. <span class="marks">[5]</span>
5. What is a chiral carbon? Explain optical isomerism with lactic acid as an
   example, and distinguish between a racemic mixture and a meso compound. <span class="marks">[5]</span>
6. Distinguish between homolytic and heterolytic fission. Give the shape,
   hybridisation and stability order of a carbocation and a carbanion. <span class="marks">[5]</span>
7. Define the inductive effect. Explain why trichloroacetic acid is a much
   stronger acid than acetic acid, and why the effect of the chlorine in
   4-chlorobutanoic acid is almost negligible. <span class="marks">[5]</span>
8. Write the seven structural isomers of C₄H₁₀O, name them, and state the type of
   isomerism between (i) isomers 1 and 2 and (ii) an alcohol and an ether. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** (i) 3-methylpentane (ii) 2-methylbut-2-ene (iii) 4-hydroxypentanal
(iv) methyl propanoate. In (iii) the —CHO carbon is C1, the chain is five
carbons, and the OH becomes the prefix hydroxy-.

**2.** Extract: fuse the compound with clean sodium to redness, plunge the hot
tube into distilled water, boil and filter.
Nitrogen — boil with FeSO₄, acidify with dilute H₂SO₄:
6NaCN + FeSO₄ → Na₄[Fe(CN)₆] + Na₂SO₄, then
3Na₄[Fe(CN)₆] + 2Fe₂(SO₄)₃ → Fe₄[Fe(CN)₆]₃↓ + 6Na₂SO₄, Prussian blue.
Sulphur — Na₂S + Na₂[Fe(CN)₅NO] → Na₄[Fe(CN)₅NOS], violet; and
Na₂S + (CH₃COO)₂Pb → PbS↓ + 2CH₃COONa, black.

**4.** Conditions: restricted rotation about a C=C (or a ring) and two different
groups on each of the doubly bonded carbons. cis-but-2-ene has both methyls on
the same side (b.p. 3.7 °C, m.p. −139 °C, dipole moment 0.33 D);
trans-but-2-ene has them on opposite sides (b.p. 0.9 °C, m.p. −106 °C, dipole
moment 0). The trans form is more stable and melts higher; the cis form is more
polar and boils higher.

**7.** Definition as in Section 13.8. In Cl₃CCOOH three strongly −I chlorines
drain electron density from the carboxylate oxygen, spreading the negative
charge and stabilising the anion, so the acid ionises far more completely
(pKa 0.66 against 4.76). In 4-chlorobutanoic acid the chlorine is three carbons
away; the inductive effect falls to roughly one-third of its strength at each
carbon, so almost nothing reaches the —COOH group.

**8.** butan-1-ol, butan-2-ol, 2-methylpropan-1-ol, 2-methylpropan-2-ol,
1-methoxypropane, 2-methoxypropane, ethoxyethane. (i) butan-1-ol and butan-2-ol
are position isomers; (ii) any alcohol and any ether are functional isomers.
:::

**Group C — Long answer (8 marks each)**

1. (a) State the rules used to select and number the principal chain in IUPAC
   nomenclature, and give the seniority order of the common functional groups. <span class="marks">[4]</span>
   (b) Name: (i) CH₃CH(CH₃)CH₂CH(OH)CH₃ (ii) HOOC—CH₂—CH(CH₃)—COOH
   (iii) CH₃CH₂CH₂CHO (iv) (CH₃)₃CCl. <span class="marks">[4]</span>
2. (a) Define isomerism and classify it fully, giving one example of each of the
   seven types. <span class="marks">[4]</span>
   (b) What is optical isomerism? State the conditions for a compound to be
   optically active, define enantiomer, racemic mixture and meso compound, and
   work out how many optical isomers tartaric acid, HOOC—CH(OH)—CH(OH)—COOH,
   actually has. <span class="marks">[4]</span>
3. (a) Define the inductive effect and the resonance effect and give three points
   of difference between them. <span class="marks">[4]</span>
   (b) Using these effects, explain: (i) the order HCOOH > CH₃COOH >
   CH₃CH₂COOH in acid strength; (ii) why phenol is more acidic than ethanol;
   (iii) why aniline is a weaker base than ammonia. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** (b) (i) 4-methylpentan-2-ol — the chain is five carbons, the OH takes the
lower locant 2, so the methyl lands on C4. (ii) 2-methylbutanedioic acid — both
—COOH carbons are in the chain, giving a four-carbon diacid with a methyl on C2.
(iii) butanal. (iv) 2-chloro-2-methylpropane.

**2.** (b) A compound is optically active if it is chiral, i.e. its mirror image
is not superimposable on it; the usual cause is a carbon carrying four different
groups, and the molecule must have no plane or centre of symmetry. Enantiomers
are the two non-superimposable mirror images; a racemic mixture is a 50:50 blend
of them, inactive by external compensation; a meso compound contains chiral
carbons but has an internal plane of symmetry and is inactive by internal
compensation.
Tartaric acid has two chiral carbons, so $2^{2} = 4$ is the maximum — but the two
chiral carbons carry the *same* four groups, so one of the four is a meso form
and its mirror image is identical to it. Tartaric acid therefore has only
**three** forms: d, l and meso.

**3.** (b) (i) The methyl group in CH₃COOH is +I and pushes electron density onto
the carboxylate, destabilising the anion; the ethyl group in CH₃CH₂COOH is a
still stronger +I group. Formic acid has no alkyl group at all, so its anion is
the most stable and it is the strongest of the three.
(ii) In the phenoxide ion the negative charge is delocalised over the ortho and
para carbons of the ring by the −R effect of the ring, so the anion is strongly
resonance stabilised. The ethoxide ion has no such delocalisation, so ethanol
is a far weaker acid (pKa 10.0 against 15.9).
(iii) In aniline the nitrogen lone pair is conjugated with the ring (+R effect of
—NH₂) and is delocalised into it, so it is much less available to accept a
proton. In ammonia the lone pair is entirely localised on nitrogen. Hence
aniline (pKb 9.4) is a much weaker base than ammonia (pKb 4.75).
:::
