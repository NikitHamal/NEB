---
subject: Chemistry
grade: 12
unit: 10
title: Alcohols
hours: 7
area: Organic Chemistry
---

An alcohol is a hydrocarbon in which one hydrogen has been replaced by a hydroxyl
group, –OH. That one small change transforms the molecule: alkanes are gases and
oily liquids that dissolve in nothing, while the first few alcohols are
water-miscible liquids that boil far above their parent alkanes, react with
sodium, and can be oxidised in steps all the way to carboxylic acids. Almost
every other oxygen-containing family in Grade 12 — ethers, aldehydes, ketones,
acids, esters — can be reached from an alcohol, so this unit is the hub of the
organic course.

::: key What the examiners ask
Three things carry most of the marks: (i) **distinguishing** 1°, 2° and 3°
alcohols — Victor Meyer's method, Lucas test, oxidation behaviour; (ii) the
**reagent → product** table of chemical properties, written as balanced
equations with conditions; (iii) short numericals on fermentation yield and on
gas volumes. Learn the conditions, not just the arrows: `170 °C` and `140 °C`
with the same acid give completely different products.
:::

## 10.1 Introduction; nomenclature, isomerism and classification of monohydric alcohol

An alcohol containing **one** –OH group is **monohydric**, two is **dihydric**
(ethane-1,2-diol, glycol), three is **trihydric** (propane-1,2,3-triol,
glycerol). The general formula of a saturated monohydric alcohol is
**CₙH₂ₙ₊₁OH**, i.e. CₙH₂ₙ₊₂O. The carbon that carries the –OH is called the
**carbinol carbon**.

**Classification.** Count how many carbon atoms are attached to the carbinol
carbon: one gives a **primary (1°)** alcohol, two a **secondary (2°)** alcohol,
three a **tertiary (3°)** alcohol. (Methanol, CH₃OH, has none and is counted as
primary.)

```figure caption="The three classes of monohydric alcohol. Classification depends only on the number of carbon atoms attached to the carbinol carbon, never on the total number of carbons."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 3, figsize=(5.2,3.2))
GRP = '#2e8b57'
spec = [
 ('primary  (1°)', '#1d6fb8',
  [('H', MUTED), ('H', MUTED), ('R', GRP)], 'R–CH₂–OH',
  'CH₃CH₂OH\nethanol', '1 carbon attached'),
 ('secondary  (2°)', '#b8860b',
  [('R', GRP), ("R'", GRP), ('H', MUTED)], 'R₂CH–OH',
  '(CH₃)₂CHOH\npropan-2-ol', '2 carbons attached'),
 ('tertiary  (3°)', '#d9534f',
  [('R', GRP), ("R'", GRP), ("R''", GRP)], 'R₃C–OH',
  '(CH₃)₃COH\n2-methylpropan-2-ol', '3 carbons attached'),
]
pos = [(-1.02, 0.0), (1.02, 0.0), (0.0, -1.02)]
bnd = [((-0.24,0.0),(-0.74,0.0)), ((0.24,0.0),(0.74,0.0)), ((0.0,-0.24),(0.0,-0.74))]
for ax, (title, tc, subs, gen, ex, note) in zip(axes, spec):
    ax.axis('off'); ax.set_aspect('equal')
    ax.set_xlim(-2.0, 2.0); ax.set_ylim(-3.45, 2.05)
    ax.text(0, 1.88, title, color=tc, fontsize=9.6, ha='center', va='center',
            fontweight='bold')
    ax.plot([0,0],[0.24,0.80], color=INK, lw=1.7, solid_capstyle='round')
    ax.text(0, 1.06, 'OH', color=ACCENT, fontsize=11.5, ha='center', va='center',
            fontweight='bold')
    ax.text(0, 0, 'C', color=INK, fontsize=11.5, ha='center', va='center')
    for (lab, col), (x, y), (p, q) in zip(subs, pos, bnd):
        ax.plot([p[0],q[0]],[p[1],q[1]], color=INK, lw=1.7, solid_capstyle='round')
        ax.text(x, y, lab, color=col, fontsize=11.0, ha='center', va='center')
    ax.text(0, -1.68, note, color=MUTED, fontsize=7.4, ha='center', va='center')
    ax.text(0, -2.22, gen, color=INK, fontsize=10.2, ha='center', va='center')
    ax.plot([-1.25,1.25],[-2.58,-2.58], color=GRID, lw=1.0)
    ax.text(0, -3.02, ex, color=tc, fontsize=7.8, ha='center', va='center',
            linespacing=1.45)
fig.tight_layout()
```

**Nomenclature.** In IUPAC names the suffix **-ol** replaces the final *-e* of
the parent alkane, and the position of the –OH gets the lowest possible locant.
The –OH outranks alkyl groups and C=C when numbering.

| Structure | IUPAC name | Common name | Class |
|---|---|---|---|
| CH₃OH | methanol | methyl alcohol | 1° |
| CH₃CH₂OH | ethanol | ethyl alcohol | 1° |
| CH₃CH₂CH₂OH | propan-1-ol | *n*-propyl alcohol | 1° |
| (CH₃)₂CHOH | propan-2-ol | isopropyl alcohol | 2° |
| CH₃CH₂CH₂CH₂OH | butan-1-ol | *n*-butyl alcohol | 1° |
| CH₃CH₂CH(OH)CH₃ | butan-2-ol | *sec*-butyl alcohol | 2° |
| (CH₃)₂CHCH₂OH | 2-methylpropan-1-ol | isobutyl alcohol | 1° |
| (CH₃)₃COH | 2-methylpropan-2-ol | *tert*-butyl alcohol | 3° |
| CH₂=CHCH₂OH | prop-2-en-1-ol | allyl alcohol | 1° |
| C₆H₅CH₂OH | phenylmethanol | benzyl alcohol | 1° |

**Isomerism.** Monohydric alcohols show four kinds:

- **Chain isomerism** — butan-1-ol and 2-methylpropan-1-ol (C₄H₁₀O).
- **Position isomerism** — butan-1-ol and butan-2-ol (–OH moved along the same chain).
- **Functional isomerism** — an alcohol and an ether of the same formula, e.g.
  C₂H₆O is either ethanol or methoxymethane.
- **Optical isomerism** — butan-2-ol has four different groups on C-2, so it is
  chiral and exists as two enantiomers.

C₄H₁₀O therefore has **four** alcohols (butan-1-ol, butan-2-ol,
2-methylpropan-1-ol, 2-methylpropan-2-ol) and **three** ethers.

## 10.2 Distinction of 1, 2, 3 alcohols by Victor Meyer's Method

Victor Meyer's method converts the alcohol into a nitroalkane in three steps and
then exploits the fact that only α-hydrogens (hydrogens on the carbon bearing
–NO₂) react with nitrous acid.

**Step 1 — iodination.** R–OH + HI --red P--> R–I + H₂O

**Step 2 — nitration of the iodide.** R–I + AgNO₂ → R–NO₂ + AgI↓

**Step 3 — action of nitrous acid, then alkali.** HNO₂ (from NaNO₂ + dil. HCl)
attacks an α-hydrogen. The number of α-hydrogens decides the colour:

```figure caption="Victor Meyer's method. The colour at the last step is decided by the number of α-hydrogen atoms on the nitro carbon: two give a nitrolic acid (red salt), one gives a pseudonitrole (blue), none gives no reaction."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.1,4.4))
ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0.3,10.5)

def box(x, y, w, h, txt, fc, ec, fs=7.0, tc=None, weight=None):
    ax.add_patch(plt.Rectangle((x-w/2, y-h/2), w, h, facecolor=fc,
                               edgecolor=ec, lw=1.0, zorder=1))
    ax.text(x, y, txt, ha='center', va='center', fontsize=fs,
            color=tc or INK, zorder=2, linespacing=1.40, fontweight=weight or 'normal')

def down(x, y1, y2, lab=None):
    ax.annotate('', xy=(x, y2), xytext=(x, y1),
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.1,
                                mutation_scale=10))
    if lab:
        ax.text(x+0.13, (y1+y2)/2, lab, fontsize=6.5, color=MUTED,
                ha='left', va='center')

box(5.0, 10.05, 3.4, 0.62, 'alcohol   R–OH', '#eef3f9', ACCENT, 8.4, ACCENT)
down(5.0, 9.72, 9.28, 'HI / red P')
box(5.0, 8.95, 3.4, 0.62, 'iodoalkane   R–I', '#eef3f9', ACCENT, 8.4)
down(5.0, 8.62, 8.18, 'AgNO₂,  − AgI')
box(5.0, 7.85, 3.4, 0.62, 'nitroalkane   R–NO₂', '#eef3f9', ACCENT, 8.4)
ax.text(5.0, 7.30, 'HNO₂  (NaNO₂ + dil. HCl),  then excess NaOH',
        ha='center', va='center', fontsize=6.9, color=MUTED)

xs = (1.72, 5.0, 8.28)
cols = ['#d9534f', '#1d6fb8', '#5b6472']
heads = ['1°   R–CH₂–NO₂', '2°   R₂CH–NO₂', '3°   R₃C–NO₂']
alpha = ['2 α-hydrogens', '1 α-hydrogen', 'no α-hydrogen']
prod = ['nitrolic acid\nR–C(NO₂)=N–OH',
        'pseudonitrole\nR₂C(NO₂)(N=O)',
        'no reaction\nwith HNO₂']
res  = ['BLOOD RED\nsolution with NaOH',
        'BLUE\nsolution',
        'COLOURLESS\n(stays colourless)']
swat = ['#c0392b', '#2354a8', '#f2f4f7']
tcol = ['white', 'white', MUTED]
for x, c, hd, al, pr, rs, sw, tc in zip(xs, cols, heads, alpha, prod, res, swat, tcol):
    ax.annotate('', xy=(x, 6.58), xytext=(5.0, 7.08),
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.0,
                                mutation_scale=9))
    box(x, 6.22, 2.95, 0.62, hd, 'white', c, 7.6, c, 'bold')
    ax.text(x, 5.62, al, ha='center', va='center', fontsize=6.8, color=MUTED)
    down(x, 5.30, 4.82)
    box(x, 4.28, 2.95, 1.02, pr, '#fbfbfc', GRID, 6.8)
    down(x, 3.74, 3.26)
    box(x, 2.62, 2.95, 1.22, rs, sw, c, 7.4, tc, 'bold')

ax.text(5.0, 1.10,
        'Only 1° and 2° nitroalkanes have a hydrogen on the nitro carbon for HNO₂ to\n'
        'replace, so only they give a coloured product. The 3° alcohol is identified\n'
        'by the absence of any colour.',
        ha='center', va='center', fontsize=6.9, color=MUTED, linespacing=1.45,
        bbox=dict(boxstyle='round,pad=0.42', fc='#fdf6ec', ec='#b8860b', lw=0.9))
fig.tight_layout()
```

The **Lucas test** is the quicker bench alternative. Lucas reagent is
concentrated HCl saturated with anhydrous ZnCl₂. It works because the reaction
is SN1: the faster the carbocation forms, the faster the insoluble chloride
appears as turbidity.

| Test | Reagent and conditions | 1° alcohol | 2° alcohol | 3° alcohol |
|---|---|---|---|---|
| **Victor Meyer** | HI/red P → AgNO₂ → HNO₂ → NaOH | blood **red** | **blue** | **colourless** |
| **Lucas** | conc. HCl + anhyd. ZnCl₂, 25 °C | no turbidity (needs heating) | turbidity in about 5 min | turbidity **at once** |
| **Oxidation** | acidified K₂Cr₂O₇ | aldehyde, then carboxylic acid | ketone only | no reaction (mild) |
| **Catalytic dehydrogenation** | Cu, 300 °C | aldehyde + H₂ | ketone + H₂ | alkene + H₂O |
| **Esterification rate** | CH₃COOH / conc. H₂SO₄ | fastest | medium | slowest |

::: caution Victor Meyer colours are easy to swap
The red colour belongs to the **1°** alcohol (two α-hydrogens, nitrolic acid) and
the blue to the **2°** alcohol (one α-hydrogen, pseudonitrole). A common error is
to write "3° gives red". A 3° alcohol gives **no colour at all** — that absence
is the test.
:::

## 10.3 Preparation from haloalkane, primary amines and esters

**(a) From haloalkanes — hydrolysis.** Boiling with aqueous KOH (or moist Ag₂O)
replaces halogen by –OH:

CH₃CH₂Br + KOH(aq) → CH₃CH₂OH + KBr

Primary halides react by SN2, tertiary by SN1. With alcoholic KOH the same halide
would give an alkene instead, so the **aqueous** solvent must be stated.

**(b) From primary amines.** A primary aliphatic amine treated with nitrous acid
(NaNO₂ + dilute HCl, 0–5 °C) gives an unstable diazonium salt that loses nitrogen
at once:

CH₃CH₂NH₂ + HNO₂ → CH₃CH₂OH + N₂↑ + H₂O

Brisk effervescence of nitrogen is also the standard **test for a 1° amine**.

**(c) From esters — hydrolysis.** Acid hydrolysis is reversible; alkaline
hydrolysis (saponification) goes to completion because the acid is removed as its
salt:

CH₃COOC₂H₅ + H₂O ⇌ (dil. H₂SO₄) CH₃COOH + C₂H₅OH

CH₃COOC₂H₅ + NaOH → CH₃COONa + C₂H₅OH

Reduction of an ester with LiAlH₄ (or Na/C₂H₅OH, the Bouveault–Blanc reduction)
gives **two** alcohols — the alcohol part plus a 1° alcohol from the acyl part:

CH₃COOC₂H₅ + 4[H] → CH₃CH₂OH + C₂H₅OH

## 10.4 Industrial preparation: oxo process, hydroboration-oxidation of ethene, fermentation of sugar

**(a) Oxo process (hydroformylation).** An alkene, carbon monoxide and hydrogen
are passed over dicobalt octacarbonyl at about 150 °C and 100 atm. The aldehyde
formed is then hydrogenated to a **primary** alcohol:

CH₂=CH₂ + CO + H₂ --Co₂(CO)₈, 150 °C, 100 atm--> CH₃CH₂CHO

CH₃CH₂CHO + H₂ --Ni, 140 °C--> CH₃CH₂CH₂OH  (propan-1-ol)

Note that the chain grows by one carbon: ethene gives propan-1-ol, not ethanol.

**(b) Hydroboration–oxidation of ethene.** Diborane adds across the double bond,
and the trialkylborane is then oxidised by alkaline hydrogen peroxide:

3CH₂=CH₂ + BH₃ --dry ether--> (CH₃CH₂)₃B

(CH₃CH₂)₃B + 3H₂O₂ --NaOH(aq)--> 3CH₃CH₂OH + H₃BO₃

Boron attaches to the carbon carrying **more** hydrogen, so with an unsymmetrical
alkene the product is **anti-Markovnikov**: propene gives propan-1-ol, whereas
acid-catalysed hydration of propene gives propan-2-ol. With ethene both routes
give ethanol, which is why the syllabus names ethene here.

**(c) Fermentation of sugar.** Starch from maize, rice or millet is first broken
down, then glucose is fermented at 25–30 °C in the absence of air:

2(C₆H₁₀O₅)ₙ + nH₂O --diastase--> nC₁₂H₂₂O₁₁  (starch → maltose)

C₁₂H₂₂O₁₁ + H₂O --maltase--> 2C₆H₁₂O₆  (maltose → glucose)

C₆H₁₂O₆ --zymase--> 2C₂H₅OH + 2CO₂↑  (glucose → ethanol)

For cane sugar the first enzyme is **invertase**:
C₁₂H₂₂O₁₁ + H₂O --invertase--> C₆H₁₂O₆ + C₆H₁₂O₆ (glucose + fructose).

Fermentation stops near 14 % alcohol because zymase is destroyed by its own
product, so the dilute "wash" must be concentrated by fractional distillation.
This is exactly how *jaand* and *chhyang* are made from millet and rice in the
Nepali hills, and *raksi* is the distillate from the same wash.

::: example Worked example 10.1
**Problem.** 90 g of glucose is fermented completely by zymase. Calculate
(a) the mass of ethanol formed, (b) its volume, given that the density of ethanol
is 0.789 g cm⁻³, and (c) the volume of CO₂ liberated at STP. If only 38.0 g of
ethanol is actually recovered, what is the percentage yield?
(C = 12, H = 1, O = 16)

**Solution.** C₆H₁₂O₆ --zymase--> 2C₂H₅OH + 2CO₂

Molar mass of glucose $= 6(12) + 12(1) + 6(16) = 180\ \text{g mol}^{-1}$, so

$$ n(\text{glucose}) = \frac{90}{180} = 0.50\ \text{mol} $$

(a) 1 mol glucose gives 2 mol ethanol, so $n(\text{ethanol}) = 1.00\ \text{mol}$.
Molar mass of C₂H₅OH $= 46\ \text{g mol}^{-1}$, hence mass $= 46\ \text{g}$.

(b) $V = m/\rho = 46/0.789 = 58.3\ \text{cm}^{3}$.

(c) $n(\text{CO}_2) = 1.00\ \text{mol}$, and 1 mol of any gas occupies
$22.4\ \text{dm}^{3}$ at STP, so $V = 22.4\ \text{dm}^{3}$.

Percentage yield $= \dfrac{38.0}{46.0}\times 100 = 82.6\ \%$.
:::

## 10.5 Common terms: absolute alcohol, power alcohol, denatured alcohol, rectified spirit, alcoholic beverage

| Term | What it is | How it is made / why |
|---|---|---|
| **Rectified spirit** | 95.6 % ethanol + 4.4 % water by mass | the constant-boiling **azeotrope** (b.p. 78.15 °C) obtained by fractional distillation of the fermented wash; further distillation cannot concentrate it |
| **Absolute alcohol** | 100 % ethanol | rectified spirit is refluxed with quicklime (CaO) for several hours and then distilled; CaO takes up the water as Ca(OH)₂. Azeotropic distillation with benzene is the industrial route |
| **Denatured alcohol** (methylated spirit) | ethanol made undrinkable | about 5 % methanol with pyridine, a trace of CuSO₄ (blue colour) and petroleum are added, so industrial alcohol escapes the heavy excise duty on drink |
| **Power alcohol** | petrol containing 20–25 % ethanol | used as a motor fuel; benzene or ether is added as a co-solvent to stop the ethanol separating out in cold weather. It raises the octane number and saves imported petrol |
| **Alcoholic beverage** | a drink whose intoxicant is ethanol | *undistilled* by fermentation only — beer 4–8 %, wine 10–14 %, *chhyang*; *distilled* — whisky, rum, *raksi*, 30–45 %. Strength is also quoted as **proof spirit** |

::: caution Absolute alcohol cannot be made by distilling harder
Because ethanol and water form an azeotrope at 95.6 %, the vapour has the same
composition as the liquid. No amount of extra fractionation gets past 95.6 % — a
**chemical** drying agent (CaO) or an added third component (benzene) is
essential. Anhydrous CaCl₂ must *not* be used; it forms a compound with ethanol.
:::

## 10.6 Physical properties

- **State and smell.** C₁–C₁₁ straight-chain alcohols are colourless liquids with
  a mild spirituous smell; C₁₂ and above are waxy, odourless solids.
- **Boiling point.** Far higher than the alkane, haloalkane or ether of
  comparable molar mass, because alcohol molecules are linked by **intermolecular
  hydrogen bonds** (about 20 kJ mol⁻¹ each). Vaporising an alcohol means breaking
  this network as well as overcoming van der Waals forces.
- **Effect of branching.** Among isomers the boiling point *falls* with
  branching, because a compact molecule has less surface contact: butan-1-ol
  117.7 °C > butan-2-ol 99.5 °C > 2-methylpropan-2-ol 82.4 °C.
- **Solubility.** Methanol, ethanol and propan-1-ol are miscible with water in
  all proportions; solubility then falls sharply as the water-repelling alkyl
  chain grows and the hydrogen-bonding –OH becomes a smaller part of the
  molecule. Butan-1-ol dissolves 7.9 g per 100 g of water; decan-1-ol is
  practically insoluble.
- **Density.** Less than water (ethanol 0.789 g cm⁻³) but much greater than the
  parent alkane.
- **Neutral to litmus.** Alcohols are extremely weak acids
  ($\mathrm{p}K_a \approx 16$–18) and do not turn blue litmus red.

```figure caption="Hydrogen bonding in liquid ethanol. The hydroxyl hydrogen carries a partial positive charge and is attracted to a lone pair on the oxygen of the next molecule, linking the molecules into chains."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,4.3))
ax.axis('off'); ax.set_xlim(-1.62, 3.58); ax.set_ylim(-4.25, 1.30)
ax.set_aspect('equal')
OX = '#d9534f'
step = 1.55
for k in range(3):
    y = -step*k
    # O-H bond
    ax.plot([0,0],[y+0.20, y+0.50], color=INK, lw=1.7, solid_capstyle='round')
    ax.text(0, y, 'O', color=OX, fontsize=12.0, ha='center', va='center',
            fontweight='bold')
    ax.text(0, y+0.68, 'H', color=INK, fontsize=10.5, ha='center', va='center')
    # lone pairs on O (left side)
    for dy in (0.13, -0.13):
        ax.plot([-0.26,-0.20],[y+dy, y+dy], color=OX, lw=0, marker='o', ms=1.9)
    ax.text(-0.52, y+0.30, 'δ−', color=OX, fontsize=7.6, ha='center', va='center')
    ax.text(0.30, y+0.76, 'δ+', color=ACCENT, fontsize=7.6, ha='center', va='center')
    # ethyl chain: O -> CH2 -> CH3
    ax.plot([0.26, 0.86],[y-0.10, y-0.44], color=INK, lw=1.7, solid_capstyle='round')
    ax.text(1.12, y-0.52, 'CH₂', color=INK, fontsize=9.2, ha='center', va='center')
    ax.plot([1.42, 2.00],[y-0.44, y-0.10], color=INK, lw=1.7, solid_capstyle='round')
    ax.text(2.30, y-0.02, 'CH₃', color=INK, fontsize=9.2, ha='center', va='center')
    # hydrogen bond up to previous O
    if k > 0:
        ax.plot([0,0],[y+0.82, y+step-0.20], color=OX, lw=1.4, ls=(0,(2.2,2.0)))
ax.annotate('hydrogen\nbond', xy=(0.0, -0.50),
            xytext=(-1.55, -0.50), fontsize=7.4, color=OX, ha='left',
            va='center', linespacing=1.4,
            arrowprops=dict(arrowstyle='-|>', color=OX, lw=1.0, mutation_scale=9,
                            shrinkA=3, shrinkB=2))
ax.text(1.05, 0.98, 'one ethanol molecule,  CH₃CH₂OH', color=MUTED,
        fontsize=7.4, ha='center', va='center')
ax.text(1.05, -4.02, 'solid line = covalent bond      dotted line = hydrogen bond,\n'
        'about 20 kJ mol⁻¹ — one twentieth of the O–H covalent bond',
        color=MUTED, fontsize=6.8, ha='center', va='center', linespacing=1.4)
fig.tight_layout()
```

```figure caption="Boiling points of straight-chain 1-alkanols and of the alkanes of almost the same molar mass. Hydrogen bonding lifts every alcohol roughly 100–150 °C above its alkane partner; ethoxyethane, which cannot hydrogen-bond to itself, sits with the alkanes."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,3.1))
alc_M  = [32.04, 46.07, 60.10, 74.12, 88.15]
alc_bp = [64.7, 78.3, 97.2, 117.7, 138.0]
alc_nm = ['methanol','ethanol','propan-1-ol','butan-1-ol','pentan-1-ol']
alk_M  = [30.07, 44.10, 58.12, 72.15, 86.18]
alk_bp = [-88.6, -42.1, -0.5, 36.1, 68.7]
alk_nm = ['ethane','propane','butane','pentane','hexane']
ax.plot(alc_M, alc_bp, 'o-', color=ACCENT, ms=5.0, lw=1.8, label='1-alkanol')
ax.plot(alk_M, alk_bp, 's--', color='#5b6472', ms=4.6, lw=1.6, label='alkane')
ax.plot([74.12], [34.6], 'D', color='#2e8b57', ms=6.5, zorder=5)
for M, b, n in zip(alc_M, alc_bp, alc_nm):
    ax.annotate(n, (M, b), textcoords='offset points', xytext=(0,9),
                ha='center', fontsize=6.6, color=ACCENT)
for M, b, n, off in zip(alk_M, alk_bp, alk_nm,
                        [(0,-13),(0,-13),(0,-13),(-26,-4),(6,-13)]):
    ax.annotate(n, (M, b), textcoords='offset points', xytext=off,
                ha='center', fontsize=6.6, color=MUTED)
ax.annotate('', xy=(46.07, 78.3), xytext=(46.07, -42.1),
            arrowprops=dict(arrowstyle='<|-|>', color='#d9534f', lw=1.1,
                            mutation_scale=9))
ax.text(47.6, 18.0, 'ΔT ≈ 120 °C', fontsize=7.4, color='#d9534f')
ax.annotate('ethoxyethane\n(no H-bonding)', xy=(74.12, 34.6),
            xytext=(78.5, -42), fontsize=6.8, color='#2e8b57', ha='center',
            linespacing=1.4,
            arrowprops=dict(arrowstyle='-|>', color='#2e8b57', lw=1.0,
                            mutation_scale=8))
ax.axhline(0, color=GRID, lw=0.9)
ax.set_xlabel('molar mass  (g mol⁻¹)')
ax.set_ylabel('boiling point  (°C)')
ax.set_xlim(24, 96); ax.set_ylim(-110, 175)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.45)
ax.legend(loc='upper left', fontsize=7.6)
fig.tight_layout()
```

## 10.7 Chemical properties

Alcohols react at three places: the **O–H** bond (as a very weak acid), the
**C–O** bond (the –OH is replaced), and the **α C–H** bond (oxidation and
dehydrogenation).

### (a) Replacement of –OH by halogen

| Reagent | Equation (with ethanol) | Note |
|---|---|---|
| HX | C₂H₅OH + HCl --anhyd. ZnCl₂--> C₂H₅Cl + H₂O | Groves' process; reactivity HI > HBr > HCl and 3° > 2° > 1° |
| PX₃ | 3C₂H₅OH + PBr₃ → 3C₂H₅Br + H₃PO₃ | PBr₃ and PI₃ are made *in situ* from red P + Br₂ / I₂ |
| PCl₅ | C₂H₅OH + PCl₅ → C₂H₅Cl + POCl₃ + HCl | also a **test for –OH**: vigorous HCl fumes |
| SOCl₂ | C₂H₅OH + SOCl₂ --pyridine--> C₂H₅Cl + SO₂↑ + HCl↑ | **Darzen's method** — the best, because both by-products are gases and escape, leaving pure chloroalkane |

### (b) Action of reactive metals

The hydroxyl hydrogen is displaced as hydrogen gas:

2C₂H₅OH + 2Na → 2C₂H₅ONa + H₂↑   (sodium ethoxide)

6C₂H₅OH + 2Al → 2(C₂H₅O)₃Al + 3H₂↑   (aluminium ethoxide)

The reaction is far less vigorous than sodium with water, showing that alcohols
are weaker acids than water. Reactivity falls **1° > 2° > 3°**, because each
extra electron-releasing alkyl group pushes charge onto the oxygen of the
alkoxide ion and destabilises it.

### (c) Dehydration

The product depends entirely on the **temperature**:

C₂H₅OH --conc. H₂SO₄, 170 °C--> CH₂=CH₂ + H₂O   (intramolecular, gives an alkene)

2C₂H₅OH --conc. H₂SO₄, 140 °C--> C₂H₅OC₂H₅ + H₂O   (intermolecular, gives an ether)

Alumina at 350 °C does the same job without the charring caused by sulphuric
acid. Ease of dehydration is **3° > 2° > 1°**, and where two alkenes are
possible, **Saytzeff's rule** applies — the more substituted (more stable) alkene
predominates. So butan-2-ol gives mainly but-2-ene, not but-1-ene.

### (d) Oxidation of 1°, 2° and 3° alcohols

```figure caption="Oxidation and catalytic dehydrogenation of the three classes of alcohol. A 2° alcohol stops at the ketone because the carbinol carbon has no second hydrogen to lose; a 3° alcohol has none at all, so it dehydrates instead."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.2,3.3))
ax.axis('off'); ax.set_xlim(0,10.6); ax.set_ylim(0.55,6.45)

def box(x, y, w, txt, fc, ec, fs=7.2, tc=None, h=0.78, weight='normal'):
    ax.add_patch(plt.Rectangle((x-w/2, y-h/2), w, h, facecolor=fc,
                               edgecolor=ec, lw=1.0, zorder=1))
    ax.text(x, y, txt, ha='center', va='center', fontsize=fs, color=tc or INK,
            zorder=2, linespacing=1.35, fontweight=weight)

def right(x1, x2, y, top, bot=None, col=None):
    col = col or MUTED
    ax.annotate('', xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle='-|>', color=col, lw=1.1,
                                mutation_scale=10))
    ax.text((x1+x2)/2, y+0.30, top, ha='center', va='center', fontsize=6.4,
            color=col)
    if bot:
        ax.text((x1+x2)/2, y-0.32, bot, ha='center', va='center', fontsize=6.4,
                color=col)

rows = [
 (5.55, '#1d6fb8', '1°   R–CH₂–OH', 'CH₃CH₂OH',
  'aldehyde\nR–CHO', 'carboxylic acid\nR–COOH'),
 (3.45, '#b8860b', '2°   R₂CH–OH', '(CH₃)₂CHOH',
  'ketone\nR₂C=O', 'no further\noxidation'),
]
for y, c, hd, ex, p1, p2 in rows:
    box(1.35, y, 2.45, hd, 'white', c, 7.6, c, 0.80, 'bold')
    ax.text(1.35, y-0.62, ex, ha='center', va='center', fontsize=6.4, color=MUTED)
    right(2.62, 4.35, y, 'K₂Cr₂O₇ / H⁺', 'or Cu, 300 °C', c)
    box(5.30, y, 1.85, p1, '#f4f8fb', c, 7.2, INK, 0.90)
    if 'no further' in p2:
        right(6.28, 7.95, y, '[O]', None, GRID)
        box(9.00, y, 2.05, p2, '#f7f7f9', GRID, 7.0, MUTED, 0.90)
    else:
        right(6.28, 7.95, y, '[O]', None, c)
        box(9.00, y, 2.05, p2, '#f4f8fb', c, 7.2, INK, 0.90)

y = 1.35
c = '#d9534f'
box(1.35, y, 2.45, '3°   R₃C–OH', 'white', c, 7.6, c, 0.80, 'bold')
ax.text(1.35, y-0.62, '(CH₃)₃COH', ha='center', va='center', fontsize=6.4, color=MUTED)
right(2.62, 4.35, y, 'K₂Cr₂O₇ / H⁺', 'or Cu, 300 °C', c)
box(5.30, y, 1.85, 'NO oxidation\n(Cu gives alkene)', '#fdeeee', c, 7.0, INK, 0.90)
right(6.28, 7.95, y, 'hot conc. [O]', None, c)
box(9.00, y, 2.05, 'C–C cleavage:\nketone + acid', '#fdeeee', c, 7.0, INK, 0.90)

ax.text(5.3, 6.20, 'the carbinol carbon must carry an H atom to be oxidised',
        ha='center', va='center', fontsize=7.0, color=MUTED, style='italic')
fig.tight_layout()
```

With acidified potassium dichromate the full equation for the first step is

3CH₃CH₂OH + K₂Cr₂O₇ + 4H₂SO₄ → 3CH₃CHO + K₂SO₄ + Cr₂(SO₄)₃ + 7H₂O

and the orange dichromate turns green as Cr(VI) becomes Cr(III) — the colour
change used in a police breathalyser. Because the aldehyde (b.p. 21 °C) boils
well below the alcohol, it is distilled off as it forms; if left in the flask it
is oxidised on to ethanoic acid.

### (e) Catalytic dehydrogenation

Passing the vapour over copper at 300 °C removes **hydrogen** rather than adding
oxygen, which is why it distinguishes the three classes so cleanly:

CH₃CH₂OH --Cu, 300 °C--> CH₃CHO + H₂↑

(CH₃)₂CHOH --Cu, 300 °C--> CH₃COCH₃ + H₂↑

(CH₃)₃COH --Cu, 300 °C--> (CH₃)₂C=CH₂ + H₂O

### (f) Esterification

Warming an alcohol with a carboxylic acid and a little concentrated sulphuric
acid gives a sweet-smelling ester. The reaction is reversible, so the acid acts
both as catalyst and as dehydrating agent:

CH₃COOH + C₂H₅OH ⇌ (conc. H₂SO₄) CH₃COOC₂H₅ + H₂O

Isotopic labelling shows that the –OH of the **acid** is lost as water, not the
–OH of the alcohol. Rate falls 1° > 2° > 3° on steric grounds. With an acid
chloride or anhydride the reaction is fast and irreversible:

C₂H₅OH + CH₃COCl → CH₃COOC₂H₅ + HCl↑

### (g) Test of ethanol

| Test | Reagent and conditions | Observation with ethanol |
|---|---|---|
| **Iodoform test** | I₂ + NaOH (i.e. NaOI), warm to 60 °C | **yellow crystalline precipitate** of CHI₃ with a sharp antiseptic smell |
| **Ester test** | CH₃COOH + a few drops conc. H₂SO₄, warm | pleasant fruity smell of ethyl ethanoate |
| **Sodium test** | small piece of Na | steady effervescence of H₂; solid sodium ethoxide on evaporation |
| **Dichromate test** | acidified K₂Cr₂O₇, warm | orange → **green**; smell of ethanal, then vinegar |
| **FeCl₃ test** | neutral FeCl₃ | **no colour** — this is how ethanol is told apart from phenol |

The balanced iodoform equation is

CH₃CH₂OH + 4I₂ + 6NaOH → CHI₃↓ + 5NaI + HCOONa + 5H₂O

::: caution The iodoform test is not a test for "alcohol"
It is positive only for ethanol and for alcohols containing the
**CH₃–CH(OH)–** group (propan-2-ol, butan-2-ol) and for methyl ketones. Methanol,
propan-1-ol and 2-methylpropan-2-ol give a **negative** iodoform test.
:::

::: example Worked example 10.2
**Problem.** 9.2 g of absolute ethanol is treated with excess sodium metal.
Calculate (a) the volume of hydrogen liberated at STP and (b) the mass of sodium
ethoxide formed. (Na = 23)

**Solution.** 2C₂H₅OH + 2Na → 2C₂H₅ONa + H₂↑

Molar mass of ethanol $= 46\ \text{g mol}^{-1}$, so

$$ n(\text{C}_2\text{H}_5\text{OH}) = \frac{9.2}{46} = 0.20\ \text{mol} $$

(a) From the equation, 2 mol of ethanol give 1 mol of H₂:

$$ n(\text{H}_2) = \frac{0.20}{2} = 0.10\ \text{mol}, \qquad
V = 0.10 \times 22.4 = 2.24\ \text{dm}^{3}\ \text{at STP} $$

(b) $n(\text{C}_2\text{H}_5\text{ONa}) = 0.20\ \text{mol}$ and its molar mass is
$24 + 5 + 16 + 23 = 68\ \text{g mol}^{-1}$, so

$$ m = 0.20 \times 68 = 13.6\ \text{g} $$
:::

::: example Worked example 10.3
**Problem.** An alcohol **A** of molecular formula C₄H₁₀O gives turbidity with
Lucas reagent only after about five minutes, a **blue** colour in Victor Meyer's
test, and a yellow precipitate on warming with I₂ and NaOH. Oxidation of **A**
with acidified K₂Cr₂O₇ gives **B**, C₄H₈O, which does **not** reduce Fehling's
solution. Identify **A** and **B** and write the equations.

**Solution.**

*Step 1.* Turbidity after five minutes with Lucas reagent ⇒ **A is secondary**.
*Step 2.* A blue colour in Victor Meyer's test ⇒ the nitroalkane is 2° (one
α-hydrogen, pseudonitrole) ⇒ confirms **secondary**.
*Step 3.* The only secondary alcohol with formula C₄H₁₀O is **butan-2-ol**,
CH₃CH(OH)CH₂CH₃.
*Step 4.* It contains the CH₃–CH(OH)– group, so the positive iodoform test is
consistent.
*Step 5.* Oxidation of a 2° alcohol gives a **ketone**, which has the same number
of carbons and does not reduce Fehling's solution:

CH₃CH(OH)CH₂CH₃ + [O] --K₂Cr₂O₇/H₂SO₄--> CH₃COCH₂CH₃ + H₂O

So **A** is butan-2-ol and **B** is butanone (C₄H₈O, molar mass 72, as required).
The iodoform reaction is

CH₃CH(OH)CH₂CH₃ + 4I₂ + 6NaOH → CHI₃↓ + CH₃CH₂COONa + 5NaI + 5H₂O
:::

::: example Worked example 10.4
**Problem.** 4.6 g of ethanol is heated with excess concentrated sulphuric acid
at 170 °C. If the conversion to ethene is 80 %, what volume of ethene is
collected at STP? What volume would be collected if the same sample were heated
at 140 °C instead, assuming the same 80 % conversion?

**Solution.** At 170 °C: C₂H₅OH → CH₂=CH₂ + H₂O

$$ n(\text{C}_2\text{H}_5\text{OH}) = \frac{4.6}{46} = 0.10\ \text{mol} $$

Ethene formed $= 0.80 \times 0.10 = 0.080\ \text{mol}$, so

$$ V = 0.080 \times 22.4 = 1.79\ \text{dm}^{3}\ \text{at STP} $$

At 140 °C the reaction is **intermolecular**: 2C₂H₅OH → C₂H₅OC₂H₅ + H₂O. The
product is ethoxyethane, a liquid (b.p. 34.6 °C), so **no gas is collected**.
The amount of ether formed would be
$0.080/2 = 0.040\ \text{mol}$, i.e. $0.040 \times 74 = 2.96\ \text{g}$.

The point of the question is the condition: the same reagent at two temperatures
gives two different products.
:::

## Chapter summary

- A monohydric alcohol is CₙH₂ₙ₊₁OH; it is 1°, 2° or 3° according to the number
  of carbon atoms (1, 2 or 3) attached to the carbinol carbon.
- **Victor Meyer:** HI/red P → AgNO₂ → HNO₂/NaOH gives **red** (1°, nitrolic
  acid), **blue** (2°, pseudonitrole), **colourless** (3°).
  **Lucas:** turbidity at once (3°), in 5 min (2°), none cold (1°).
- Preparations: R–X + aq. KOH; R–NH₂ + HNO₂ → R–OH + N₂; hydrolysis of esters.
  Industrial: oxo process (alkene + CO + H₂ → aldehyde → 1° alcohol, one extra
  carbon), hydroboration–oxidation (anti-Markovnikov), fermentation
  (C₆H₁₂O₆ --zymase--> 2C₂H₅OH + 2CO₂).
- Rectified spirit = 95.6 % azeotrope; absolute alcohol = 100 %, made with CaO;
  denatured alcohol contains methanol and pyridine; power alcohol is
  petrol + 20–25 % ethanol.
- High boiling point and water solubility come from **intermolecular hydrogen
  bonding**; both fall as the alkyl chain grows, and boiling point falls with
  branching.
- –OH replaced by halogen using HX/ZnCl₂, PX₃, PCl₅ or SOCl₂ (Darzen's, cleanest).
  With Na: 2R–OH + 2Na → 2R–ONa + H₂↑, reactivity 1° > 2° > 3°.
- Dehydration with conc. H₂SO₄ gives the **alkene at 170 °C** and the **ether at
  140 °C**; ease 3° > 2° > 1°, orientation by Saytzeff's rule.
- Oxidation: 1° → aldehyde → acid; 2° → ketone only; 3° → no reaction. Cu at
  300 °C dehydrogenates 1° and 2° but dehydrates 3°.
- Ethanol is identified by the iodoform test (yellow CHI₃), the ester test and the
  orange → green dichromate change; it gives **no** colour with FeCl₃.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Which alcohol gives a blue colour in Victor Meyer's test? <span class="marks">[1]</span>
   (a) ethanol (b) propan-2-ol (c) 2-methylpropan-2-ol (d) methanol
2. The alcohol that gives turbidity immediately with Lucas reagent is <span class="marks">[1]</span>
   (a) butan-1-ol (b) butan-2-ol (c) 2-methylpropan-2-ol (d) propan-1-ol
3. Ethanol heated with concentrated H₂SO₄ at 140 °C gives mainly <span class="marks">[1]</span>
   (a) ethene (b) ethanal (c) ethoxyethane (d) ethyl hydrogen sulphate
4. The reagent used in Darzen's method for converting an alcohol into a
   chloroalkane is <span class="marks">[1]</span>
   (a) PCl₅ (b) SOCl₂ (c) conc. HCl + ZnCl₂ (d) Cl₂
5. Rectified spirit contains <span class="marks">[1]</span>
   (a) 100 % ethanol (b) 95.6 % ethanol (c) 84 % ethanol (d) ethanol + 5 % methanol
6. Which of the following does **not** give a positive iodoform test? <span class="marks">[1]</span>
   (a) ethanol (b) propan-2-ol (c) butan-2-ol (d) propan-1-ol

::: note Answers to Group A
**1.** (b) — propan-2-ol is 2°; its nitroalkane has one α-H and gives the blue pseudonitrole.
**2.** (c) — 3° alcohols form the carbocation fastest, so the insoluble chloride appears at once.
**3.** (c) — 140 °C favours intermolecular dehydration to the ether; 170 °C gives ethene.
**4.** (b) — SOCl₂; the by-products SO₂ and HCl are gases and escape, leaving a pure product.
**5.** (b) — it is the ethanol–water azeotrope, 95.6 % ethanol by mass.
**6.** (d) — propan-1-ol has no CH₃–CH(OH)– group, so it cannot give CHI₃.
:::

**Group B — Short answer (5 marks each)**

1. Describe Victor Meyer's method for distinguishing primary, secondary and
   tertiary alcohols, giving the equations and the colour obtained in each case. <span class="marks">[5]</span>
2. Explain why ethanol (b.p. 78 °C) boils about 120 °C higher than propane
   (b.p. −42 °C) although the two have almost the same molar mass, and why
   2-methylpropan-2-ol boils lower than butan-1-ol. <span class="marks">[5]</span>
3. 180 g of glucose is fermented by zymase. Calculate the mass and volume of
   absolute ethanol obtained (density 0.789 g cm⁻³) and the volume of CO₂ at STP,
   assuming the reaction is complete. <span class="marks">[5]</span>
4. What happens when (a) ethanol is warmed with I₂ and NaOH, (b) propan-2-ol
   vapour is passed over copper at 300 °C, (c) ethanol is treated with SOCl₂,
   (d) 2-methylpropan-2-ol is warmed with acidified K₂Cr₂O₇, (e) ethanol is
   warmed with ethanoic acid and conc. H₂SO₄? Write equations. <span class="marks">[5]</span>
5. Distinguish between rectified spirit, absolute alcohol, denatured alcohol and
   power alcohol. How is absolute alcohol obtained from rectified spirit? <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Outline: (i) R–OH + HI/red P → R–I; (ii) R–I + AgNO₂ → R–NO₂ + AgI;
(iii) R–NO₂ + HNO₂, then excess NaOH. 1° (two α-H) → nitrolic acid
R–C(NO₂)=N–OH → **blood-red** sodium salt; 2° (one α-H) → pseudonitrole
R₂C(NO₂)(N=O) → **blue**; 3° (no α-H) → no reaction → **colourless**.

**2.** Ethanol molecules are joined by intermolecular hydrogen bonds between the
δ+ hydroxyl hydrogen and a lone pair on the oxygen of the next molecule
(≈ 20 kJ mol⁻¹ each). Propane has only weak van der Waals forces, so much less
energy is needed to separate its molecules. 2-Methylpropan-2-ol is a compact,
nearly spherical molecule: the surface area of contact between molecules, and so
the van der Waals attraction, is smaller than in the extended chain of
butan-1-ol, and there is only one –OH in each case. Hence branching lowers the
boiling point (117.7 °C → 82.4 °C).

**3.** $n(\text{glucose}) = 180/180 = 1.00\ \text{mol}$.
C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂, so $n(\text{ethanol}) = 2.00\ \text{mol}$,
$m = 2.00 \times 46 = 92\ \text{g}$ and
$V = 92/0.789 = 116.6\ \text{cm}^{3}$.
$n(\text{CO}_2) = 2.00\ \text{mol}$, so
$V = 2.00 \times 22.4 = 44.8\ \text{dm}^{3}$ at STP.

**4.** (a) Yellow ppt of iodoform:
CH₃CH₂OH + 4I₂ + 6NaOH → CHI₃↓ + 5NaI + HCOONa + 5H₂O.
(b) Dehydrogenation to a ketone:
(CH₃)₂CHOH --Cu, 300 °C--> CH₃COCH₃ + H₂↑.
(c) C₂H₅OH + SOCl₂ → C₂H₅Cl + SO₂↑ + HCl↑.
(d) No reaction — the carbinol carbon of a 3° alcohol carries no hydrogen, so
mild oxidation is impossible (the dichromate stays orange).
(e) Esterification: CH₃COOH + C₂H₅OH ⇌ CH₃COOC₂H₅ + H₂O, a fruity-smelling ester.

**5.** Rectified spirit = 95.6 % ethanol + 4.4 % water (the azeotrope from
fractional distillation). Absolute alcohol = 100 % ethanol. Denatured alcohol =
ethanol + about 5 % methanol, pyridine and CuSO₄, made unfit to drink so as to
avoid excise duty. Power alcohol = petrol containing 20–25 % ethanol as a motor
fuel, with benzene as co-solvent. Absolute alcohol is obtained by refluxing
rectified spirit with quicklime (CaO) for 5–6 hours and then distilling; CaO
removes the water as Ca(OH)₂. Distillation alone cannot work, because the
95.6 % mixture is a constant-boiling azeotrope.
:::

**Group C — Long answer (8 marks each)**

1. (a) How is ethanol manufactured by the fermentation of starch? Give the
   enzymes and equations for each stage, and state why fermentation alone cannot
   give alcohol stronger than about 14 %. <span class="marks">[4]</span>
   (b) Describe the oxo process and the hydroboration–oxidation of ethene, and
   state one advantage of each over fermentation. <span class="marks">[4]</span>
2. (a) Write balanced equations for the action of ethanol with PCl₅, sodium
   metal, conc. H₂SO₄ at 170 °C and acidified K₂Cr₂O₇. <span class="marks">[4]</span>
   (b) An organic liquid **X**, C₃H₈O, does not give turbidity with Lucas reagent
   in the cold, gives a red colour in Victor Meyer's test, and on oxidation gives
   **Y** which turns blue litmus red. 6.0 g of **X** gives 1.12 dm³ of hydrogen
   at STP with excess sodium. Identify **X** and **Y**, verify the gas volume by
   calculation, and write all the equations. <span class="marks">[4]</span>

::: note Answers to Group C
**1. (a)** Starch is boiled with water and treated with malt:
2(C₆H₁₀O₅)ₙ + nH₂O --diastase--> nC₁₂H₂₂O₁₁; then
C₁₂H₂₂O₁₁ + H₂O --maltase--> 2C₆H₁₂O₆; then
C₆H₁₂O₆ --zymase--> 2C₂H₅OH + 2CO₂↑ at 25–30 °C in the absence of air.
Zymase is a protein and is destroyed (denatured) by ethanol above about 14 %, so
the fermentation stops itself; the wash must then be fractionally distilled to
95.6 % rectified spirit.
**(b)** Oxo process: CH₂=CH₂ + CO + H₂ --Co₂(CO)₈, 150 °C, 100 atm--> CH₃CH₂CHO,
then CH₃CH₂CHO + H₂ --Ni--> CH₃CH₂CH₂OH. Advantage: continuous, uses cheap
petrochemical feedstock, and lengthens the chain by one carbon.
Hydroboration–oxidation: 3CH₂=CH₂ + BH₃ → (C₂H₅)₃B, then
(C₂H₅)₃B + 3H₂O₂ --NaOH--> 3C₂H₅OH + H₃BO₃. Advantage: very high yield, no
rearrangement, and with unsymmetrical alkenes it gives the anti-Markovnikov
(1°) alcohol which acid hydration cannot.

**2. (a)** C₂H₅OH + PCl₅ → C₂H₅Cl + POCl₃ + HCl;
2C₂H₅OH + 2Na → 2C₂H₅ONa + H₂↑;
C₂H₅OH --conc. H₂SO₄, 170 °C--> CH₂=CH₂ + H₂O;
3CH₃CH₂OH + K₂Cr₂O₇ + 4H₂SO₄ → 3CH₃CHO + K₂SO₄ + Cr₂(SO₄)₃ + 7H₂O.

**(b)** No turbidity in the cold with Lucas reagent and a **red** Victor Meyer
colour both mean **X is primary**. C₃H₈O has only one primary straight-chain
alcohol, so **X = propan-1-ol**, CH₃CH₂CH₂OH. Oxidation gives
**Y = propanoic acid**, CH₃CH₂COOH, which turns blue litmus red.

Check the gas volume: molar mass of C₃H₈O is $60\ \text{g mol}^{-1}$, so
$n(X) = 6.0/60 = 0.10\ \text{mol}$. From
2C₃H₇OH + 2Na → 2C₃H₇ONa + H₂↑, $n(\text{H}_2) = 0.050\ \text{mol}$ and
$V = 0.050 \times 22.4 = 1.12\ \text{dm}^{3}$ — as stated.

Equations: 2CH₃CH₂CH₂OH + 2Na → 2CH₃CH₂CH₂ONa + H₂↑;
CH₃CH₂CH₂OH + [O] → CH₃CH₂CHO + H₂O; CH₃CH₂CHO + [O] → CH₃CH₂COOH.
:::
