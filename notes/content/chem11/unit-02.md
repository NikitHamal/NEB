---
subject: Chemistry
grade: 11
unit: 2
title: Stoichiometry
hours: 8
area: General and Physical Chemistry
---

Stoichiometry is the arithmetic of chemistry: given a balanced equation, how much
of one substance reacts with, or produces, how much of another. It rests on a
single idea — atoms are neither created nor destroyed, only rearranged — and on a
single counting unit, the **mole**. This is the longest unit in the physical
chemistry area and the one that carries most of the numerical marks in the board
paper, so every step here is worth practising until it is automatic.

::: key The one habit that makes stoichiometry easy
Never go straight from grams of A to grams of B. Always travel
**mass → moles → (mole ratio from the balanced equation) → moles → mass**.
The mole ratio is the only place where the chemistry enters; everything else is
division and multiplication.
:::

## 2.1 Dalton's atomic theory and its postulates

John Dalton (1808) explained the mass laws by assuming matter is made of
indivisible particles. His postulates are:

1. All matter is made up of extremely small, indivisible particles called **atoms**.
2. Atoms can neither be created nor destroyed in a chemical reaction.
3. Atoms of the same element are identical in mass, size and all other properties.
4. Atoms of different elements differ in mass, size and properties.
5. Atoms combine in **small whole-number ratios** to form compound atoms (molecules).
6. The relative number and kind of atoms in a given compound are fixed.

| Postulate | Law it explains | Modern status |
|---|---|---|
| Atoms are indivisible | Conservation of mass | **Wrong** — atoms contain e⁻, p⁺, n |
| Atoms are neither created nor destroyed | Conservation of mass | Valid for chemical change; fails in nuclear reactions |
| Atoms of one element are identical in mass | Definite proportions | **Wrong** — isotopes (¹H, ²H, ³H) differ in mass |
| Atoms combine in small whole-number ratios | Multiple proportions | Valid for simple compounds; fails for polymers and non-stoichiometric solids such as Fe₀.₉₅O |

::: caution Dalton's theory is not "disproved"
Examiners want both sides. The theory is *superseded*, not useless: its
book-keeping (atoms conserved, combining in fixed ratios) is still exactly how we
balance equations. Only the claims about indivisibility and identical masses have
failed.
:::

## 2.2 Laws of stoichiometry

| Law | Statement | Example |
|---|---|---|
| Conservation of mass (Lavoisier, 1789) | Matter is neither created nor destroyed in a chemical reaction; total mass of reactants = total mass of products | 2H₂ + O₂ → 2H₂O : 4 g + 32 g = 36 g |
| Definite (constant) proportions (Proust, 1799) | A pure compound always contains the same elements combined in the same fixed ratio by mass, whatever its source | H₂O from a Kathmandu tap or from a lab always has H : O = 1 : 8 by mass |
| Multiple proportions (Dalton, 1803) | When two elements form more than one compound, the masses of one element combining with a fixed mass of the other are in a simple whole-number ratio | Cu₂O and CuO: O per 63.5 g Cu = 8 g and 16 g, ratio 1 : 2 |
| Reciprocal proportions (Richter, 1792) | The masses of two elements that combine separately with a fixed mass of a third element are either in the same ratio, or a simple multiple of it, as when they combine together | H and O each combine with S; H : O in H₂S and SO₂ relate simply to H : O in H₂O |
| Gaseous volumes (Gay-Lussac, 1808) | Gases react, and the gaseous products form, in volumes that bear a simple whole-number ratio to one another at the same temperature and pressure | 2 vol H₂ + 1 vol O₂ → 2 vol steam |

```figure caption="Mass of oxygen combined with a given mass of copper in its two oxides. Each line is straight through the origin (definite proportions) and the slopes are in the ratio $1:2$ (multiple proportions)."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.9))
cu = np.linspace(0, 127, 60)
ax.plot(cu, cu*(16/127), color=SERIES[0], lw=1.9, label='Cu₂O   (8 g O per 63.5 g Cu)')
ax.plot(cu, cu*(16/63.5), color=SERIES[1], lw=1.9, label='CuO    (16 g O per 63.5 g Cu)')
ax.vlines(63.5, 0, 16, color=MUTED, lw=0.9, ls=':')
ax.plot([63.5],[8],'o',color=SERIES[0],ms=5)
ax.plot([63.5],[16],'o',color=SERIES[1],ms=5)
ax.annotate('8 g', (63.5,8), textcoords='offset points', xytext=(6,-9), fontsize=9, color=SERIES[0])
ax.annotate('16 g', (63.5,16), textcoords='offset points', xytext=(6,-2), fontsize=9, color=SERIES[1])
ax.set_xlabel('mass of copper (g)'); ax.set_ylabel('mass of oxygen combined (g)')
ax.set_xlim(0,135); ax.set_ylim(0,34)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=0.5)
ax.legend(loc='upper left', fontsize=8.0)
```

::: example Worked example 2.1
**Problem.** Copper forms two oxides. Sample A contains 88.8 % copper and sample B
contains 79.9 % copper by mass. Show that these figures obey the law of multiple
proportions.

**Solution.** Take 100 g of each sample.

| | Cu (g) | O (g) | O per 1 g of Cu |
|---|---|---|---|
| A | 88.8 | 11.2 | 11.2 / 88.8 = 0.126 |
| B | 79.9 | 20.1 | 20.1 / 79.9 = 0.252 |

Ratio of the oxygen masses for a fixed mass of copper

$$ = \frac{0.126}{0.252} = \frac{1}{2} $$

a simple whole-number ratio, so the law is obeyed. A is Cu₂O and B is CuO.
:::

## 2.3 Avogadro's law and its deductions

::: definition Avogadro's law
Equal volumes of all gases, measured at the same temperature and pressure,
contain an equal number of molecules.
:::

Avogadro's law rescued Gay-Lussac's volume ratios, which contradicted Dalton's
assumption that elementary gases were monoatomic. Writing hydrogen and oxygen as
H₂ and O₂ makes 2 volumes + 1 volume → 2 volumes come out exactly right:

2H₂ + O₂ → 2H₂O  (2 molecules + 1 molecule → 2 molecules)

### Deduction 1 — molecular mass and vapour density

::: derivation Molecular mass = 2 × vapour density
**Vapour density** (VD) is the ratio of the mass of a certain volume of a gas to
the mass of the same volume of hydrogen, both measured at the same temperature
and pressure.

Let each volume contain $n$ molecules (Avogadro's law).

$$ VD = \frac{n\times(\text{mass of 1 molecule of gas})}{n\times(\text{mass of 1 molecule of H}_2)} = \frac{\text{mass of 1 molecule of gas}}{\text{mass of 1 molecule of H}_2} $$

Multiplying numerator and denominator by 2 and using the fact that the molecular
mass of H₂ is 2,

$$ VD = \frac{2\times \text{mass of 1 molecule of gas}}{2\times\text{mass of 1 molecule of H}_2} = \frac{\text{molecular mass}}{2} $$

$$ \therefore\ \text{molecular mass} = 2 \times \text{vapour density} $$
:::

### Deduction 2 — molecular mass and volume of a gas

One mole of any gas occupies **22.4 litres at STP** (273 K, 1 atm). This volume is
called the **gram molecular volume**. Hence the molecular mass in grams of any gas
occupies 22.4 L at STP, and

$$ \text{molecular mass} = \frac{\text{mass of gas (g)}}{\text{volume at STP (L)}}\times 22.4 $$

### Deduction 3 — molecular mass and number of particles

The gram molecular mass of any substance contains the same number of molecules,
the **Avogadro number** $N_A = 6.022\times10^{23}\ \text{mol}^{-1}$.

::: example Worked example 2.2
**Problem.** 0.50 g of a gas occupies 280 cm³ at STP. Calculate (a) its molecular
mass and (b) its vapour density.

**Solution.** (a) 280 cm³ = 0.280 L.

$$ n = \frac{0.280}{22.4} = 0.0125\ \text{mol}, \qquad M = \frac{0.50}{0.0125} = 40\ \text{g mol}^{-1} $$

(b) $VD = M/2 = 40/2 = 20$. The gas is argon.
:::

## 2.4 Mole and its relation with mass, volume and number of particles

::: definition Mole
A mole is the amount of a substance that contains as many elementary entities
(atoms, molecules, ions or electrons) as there are atoms in exactly 12 g of
carbon-12, that is $6.022\times10^{23}$ entities.
:::

| Starting from | To get moles | From moles |
|---|---|---|
| Mass $w$ (g) | $n = w/M$ | $w = n\times M$ |
| Number of particles $N$ | $n = N/N_A$ | $N = n\times N_A$ |
| Volume of gas at STP $V$ (L) | $n = V/22.4$ | $V = n\times22.4$ |

```figure caption="The mole is the hub of every stoichiometric calculation. Convert into moles, use the equation, convert back out."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.0,3.2))
def box(x,y,w,h,txt,fc,fs=9.2):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.03,rounding_size=0.05',
                                fc=fc, ec=MUTED, lw=0.9))
    ax.text(x+w/2,y+h/2,txt,ha='center',va='center',fontsize=fs,color=INK)
box(0.36,0.42,0.28,0.18,'MOLE\nn','#dce8f4',10.2)
box(0.02,0.78,0.34,0.17,'MASS  w  (g)','#f2f4f7')
box(0.64,0.78,0.34,0.17,'PARTICLES  N','#f2f4f7')
box(0.33,0.04,0.34,0.17,'VOLUME at STP\nV (litre)','#f2f4f7')
def link(p,q,lab1,lab2,off1,off2):
    ax.annotate('',xy=q,xytext=p,arrowprops=dict(arrowstyle='<|-|>',color=ACCENT,
                 lw=1.3,mutation_scale=10))
    mx,my=(p[0]+q[0])/2,(p[1]+q[1])/2
    ax.annotate(lab1,(mx,my),textcoords='offset points',xytext=off1,fontsize=8.4,color=ACCENT)
    ax.annotate(lab2,(mx,my),textcoords='offset points',xytext=off2,fontsize=8.4,color=SERIES[1])
link((0.38,0.60),(0.24,0.78),'÷ M','× M',(-30,2),(-30,-11))
link((0.62,0.60),(0.77,0.78),'÷ Nᴀ','× Nᴀ',(6,2),(6,-11))
link((0.50,0.42),(0.50,0.21),'÷ 22.4','× 22.4',(6,4),(6,-10))
ax.text(0.03,0.30,'M = molar mass (g mol⁻¹)\nNᴀ = 6.022 × 10²³ mol⁻¹\n22.4 L = molar volume at STP',
        fontsize=8.3,color=MUTED,va='center')
ax.set_xlim(0,1.0); ax.set_ylim(0,1.0); ax.axis('off')
```

::: example Worked example 2.3
**Problem.** For 8.8 g of carbon dioxide at STP calculate (a) the number of moles,
(b) the number of molecules, (c) the number of oxygen atoms and (d) the volume
occupied. (C = 12, O = 16)

**Solution.** M(CO₂) = 12 + 2(16) = 44 g mol⁻¹.

(a) $n = 8.8/44 = 0.20\ \text{mol}$

(b) $N = 0.20 \times 6.022\times10^{23} = 1.204\times10^{23}$ molecules

(c) each molecule has 2 oxygen atoms, so
$N_O = 2 \times 1.204\times10^{23} = 2.409\times10^{23}$ atoms

(d) $V = 0.20 \times 22.4 = 4.48\ \text{L}$
:::

## 2.5 Calculations based on mole concept

A balanced equation is read in moles. For

CaCO₃ --Δ--> CaO + CO₂↑

the coefficients 1 : 1 : 1 mean 1 mol (100 g) of calcium carbonate gives 1 mol
(56 g) of calcium oxide and 1 mol (22.4 L at STP) of carbon dioxide.

::: tip Four steps, every time
1. Write and **balance** the equation.
2. Convert the given quantity to moles.
3. Multiply by the mole ratio taken from the coefficients.
4. Convert the answer back to the unit asked for (g, L or particles).
:::

::: example Worked example 2.4
**Problem.** 25 g of limestone from Udayapur, which is 80 % pure CaCO₃, is heated
strongly. Calculate the mass of quicklime formed and the volume of CO₂ liberated
at STP. (Ca = 40, C = 12, O = 16)

**Solution.** Mass of pure CaCO₃ = 80 % of 25 g = 20 g.

CaCO₃ --Δ--> CaO + CO₂↑

$$ n(\text{CaCO}_3) = \frac{20}{100} = 0.20\ \text{mol} $$

The mole ratio CaCO₃ : CaO : CO₂ is 1 : 1 : 1, so
$n(\text{CaO}) = n(\text{CO}_2) = 0.20$ mol.

$$ w(\text{CaO}) = 0.20 \times 56 = 11.2\ \text{g} $$
$$ V(\text{CO}_2) = 0.20 \times 22.4 = 4.48\ \text{L at STP} $$
:::

::: caution Purity and the mole ratio are different corrections
Apply the purity **before** converting to moles (it changes the mass you actually
have), and apply the percentage yield **after** the stoichiometry (it changes what
you actually collect). Mixing the two up is the commonest lost mark in this unit.
:::

## 2.6 Limiting reactant and excess reactant

When reactants are not mixed in exactly the ratio required by the equation, one
runs out first and stops the reaction.

::: definition Limiting and excess reactant
The **limiting reactant** is the reactant that is completely consumed and so
decides how much product can form. Any reactant left over when the limiting
reactant is used up is the **excess reactant**.
:::

To find it, divide the moles available of each reactant by its coefficient in the
balanced equation. The **smallest** quotient marks the limiting reactant.

```figure caption="For 28 g N₂ mixed with 9 g H₂, nitrogen is completely used up while 1.5 mol of hydrogen survives, so N₂ is the limiting reactant."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,2.8))
x = np.arange(2); w = 0.34
supplied = [1.0, 4.5]; needed = [1.0, 3.0]
ax.bar(x-w/2, supplied, w, color=SERIES[0], label='moles supplied')
ax.bar(x+w/2, needed,  w, color=SERIES[3], label='moles required')
for i,(s,nd) in enumerate(zip(supplied,needed)):
    ax.text(i-w/2, s+0.08, f'{s:.1f}', ha='center', fontsize=8.5, color=INK)
    ax.text(i+w/2, nd+0.08, f'{nd:.1f}', ha='center', fontsize=8.5, color=INK)
ax.annotate('', xy=(1.34, 3.0), xytext=(1.34, 4.5),
            arrowprops=dict(arrowstyle='<|-|>', color=SERIES[1], lw=1.2, mutation_scale=9))
ax.text(1.40, 3.75, '1.5 mol of H₂\nleft over', fontsize=8.4, color=SERIES[1], va='center')
ax.text(0, 1.55, 'LIMITING\nREACTANT', ha='center', fontsize=8.4, color=SERIES[1])
ax.set_xticks(x); ax.set_xticklabels(['N₂', 'H₂'])
ax.set_ylabel('amount (mol)'); ax.set_ylim(0, 5.4); ax.set_xlim(-0.55, 2.05)
ax.spines[['top','right']].set_visible(False); ax.grid(True, axis='y', alpha=0.5)
ax.legend(loc='upper left', fontsize=8.2)
```

::: example Worked example 2.5
**Problem.** 28 g of nitrogen is mixed with 9 g of hydrogen and passed over an
iron catalyst. Identify the limiting reactant, find the mass of ammonia formed and
the mass of the excess reactant left. (N = 14, H = 1)

**Solution.** The balanced equation is

N₂ + 3H₂ → 2NH₃

$$ n(\text{N}_2) = \frac{28}{28} = 1.0\ \text{mol}, \qquad n(\text{H}_2) = \frac{9}{2} = 4.5\ \text{mol} $$

Dividing by the coefficients: N₂ gives 1.0/1 = 1.0 and H₂ gives 4.5/3 = 1.5. The
smaller value belongs to **nitrogen**, so N₂ is limiting and H₂ is in excess.

Hydrogen used = 3 × 1.0 = 3.0 mol; hydrogen left = 4.5 − 3.0 = 1.5 mol,
i.e. 1.5 × 2 = **3 g of H₂**.

Ammonia formed = 2 × 1.0 = 2.0 mol = 2.0 × 17 = **34 g of NH₃**.

Check by mass: 28 g + 6 g reacted = 34 g of product, and 3 g of H₂ remains.
:::

## 2.7 Theoretical yield, experimental yield and percentage yield

Real reactions rarely give everything the equation promises: they may be
reversible, side reactions occur, or product is lost on filtering and drying.

| Term | Meaning |
|---|---|
| Theoretical yield | Maximum mass of product calculated from the balanced equation, assuming the limiting reactant is fully converted |
| Experimental (actual) yield | Mass of pure product actually obtained in the laboratory |
| Percentage yield | Actual yield expressed as a percentage of the theoretical yield |

$$ \%\ \text{yield} = \frac{\text{actual yield}}{\text{theoretical yield}}\times 100 $$

::: example Worked example 2.6
**Problem.** In the reaction of Worked example 2.5 only 27.2 g of ammonia is
collected. Calculate the percentage yield. If a plant needs 1.00 tonne of ammonia
per day at this yield, what mass of nitrogen must it supply?

**Solution.** Theoretical yield = 34 g.

$$ \%\ \text{yield} = \frac{27.2}{34}\times100 = 80\ \% $$

For 1.00 t = 1000 kg of actual NH₃, the theoretical yield needed is

$$ \frac{1000}{0.80} = 1250\ \text{kg of NH}_3 $$

From the equation 28 kg of N₂ gives 34 kg of NH₃, so

$$ w(\text{N}_2) = 1250 \times \frac{28}{34} = 1029\ \text{kg} \approx 1.03\ \text{t} $$
:::

## 2.8 Calculation of empirical and molecular formula from percentage composition

```figure caption="The fixed route from percentage composition to molecular formula."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.4,4.0))
steps = ['percentage of each element\n(take 100 g of compound)',
         'divide by atomic mass\n→ relative number of moles',
         'divide by the smallest value\n→ simplest mole ratio',
         'multiply to clear fractions\n→ EMPIRICAL FORMULA',
         'n = molecular mass ÷ EF mass',
         'MOLECULAR FORMULA = n × EF']
ys = [0.86, 0.70, 0.54, 0.38, 0.22, 0.06]
for i,(s,y) in enumerate(zip(steps,ys)):
    fc = '#dce8f4' if i in (3,5) else '#f2f4f7'
    ax.add_patch(FancyBboxPatch((0.06,y),0.88,0.115,
                 boxstyle='round,pad=0.02,rounding_size=0.04', fc=fc, ec=MUTED, lw=0.9))
    ax.text(0.50,y+0.058,s,ha='center',va='center',fontsize=8.9,color=INK)
    if i < len(ys)-1:
        ax.annotate('',xy=(0.50,ys[i+1]+0.118),xytext=(0.50,y-0.002),
                    arrowprops=dict(arrowstyle='-|>',color=ACCENT,lw=1.3,mutation_scale=11))
ax.set_xlim(0,1); ax.set_ylim(0.0,1.0); ax.axis('off')
```

::: example Worked example 2.7
**Problem.** An organic compound contains C 40.0 %, H 6.7 % and O 53.3 % by mass.
Its molecular mass is 180. Find its empirical and molecular formulae.

**Solution.**

| Element | % | ÷ atomic mass | ÷ smallest (3.33) | Whole number |
|---|---|---|---|---|
| C | 40.0 | 40.0/12 = 3.33 | 1.00 | 1 |
| H | 6.7 | 6.7/1 = 6.70 | 2.01 | 2 |
| O | 53.3 | 53.3/16 = 3.33 | 1.00 | 1 |

Empirical formula = **CH₂O**; empirical formula mass = 12 + 2 + 16 = 30.

$$ n = \frac{\text{molecular mass}}{\text{EF mass}} = \frac{180}{30} = 6 $$

$$ \text{molecular formula} = (\text{CH}_2\text{O})_6 = \text{C}_6\text{H}_{12}\text{O}_6 $$

which is glucose.
:::

::: caution Do not round 2.5 down to 2
If the simplest ratio comes out as 1 : 2.5 : 1, **multiply all of them by 2** to
get 2 : 5 : 2. Only round when the value is within about 0.1 of a whole number
(2.01 → 2 is fine; 2.5 → 2 destroys the answer).
:::

## Chapter summary

- Dalton's postulates: atoms are indivisible, conserved, identical within an
  element and combine in small whole-number ratios. Isotopes and subatomic
  particles have since disproved the first and third.
- The mass laws: conservation of mass, definite proportions, multiple proportions,
  reciprocal proportions, and Gay-Lussac's law of gaseous volumes.
- Avogadro's law: equal volumes of gases at the same T and P contain equal numbers
  of molecules. Deductions: molecular mass = 2 × vapour density; 1 mol of gas
  occupies 22.4 L at STP; 1 mol contains $N_A = 6.022\times10^{23}$ particles.
- Mole conversions: $n = w/M = N/N_A = V/22.4$ (V in litres, at STP).
- Stoichiometry route: mass → moles → mole ratio from the balanced equation →
  moles → mass or volume.
- The limiting reactant is the one with the smallest value of (moles ÷
  coefficient); it fixes the amount of product. The rest is excess.
- $\%\ \text{yield} = (\text{actual}/\text{theoretical})\times100$. Purity is
  applied to the reactant, yield to the product.
- Empirical formula: % → ÷ atomic mass → ÷ smallest → clear fractions;
  molecular formula = $n\times$ empirical formula with
  $n = \text{molecular mass}/\text{EF mass}$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The number of molecules in 11.2 L of any gas at STP is <span class="marks">[1]</span>
   (a) 6.022 × 10²³ (b) 3.011 × 10²³ (c) 1.204 × 10²⁴ (d) 12.044 × 10²³
2. The vapour density of a gas is 32. Its molecular mass is <span class="marks">[1]</span>
   (a) 16 (b) 32 (c) 64 (d) 128
3. In the reaction 2H₂ + O₂ → 2H₂O, 4 g of H₂ is mixed with 16 g of O₂.
   The limiting reactant is <span class="marks">[1]</span>
   (a) H₂ (b) O₂ (c) neither (d) both equally
4. Which law is explained by the existence of CO and CO₂? <span class="marks">[1]</span>
   (a) conservation of mass (b) definite proportions
   (c) multiple proportions (d) reciprocal proportions
5. The empirical formula of a compound is CH₂O and its molecular mass is 60.
   Its molecular formula is <span class="marks">[1]</span>
   (a) CH₂O (b) C₂H₄O₂ (c) C₃H₆O₃ (d) C₆H₁₂O₆

::: note Answers to Group A
**1.** (b) — 11.2 L is half a mole, so 0.5 × 6.022 × 10²³ = 3.011 × 10²³.
**2.** (c) — molecular mass = 2 × VD = 64.
**3.** (b) — n(H₂) = 2, n(O₂) = 0.5; dividing by coefficients gives 1.0 and 0.5,
so oxygen runs out first.
**4.** (c) — for a fixed 12 g of carbon, the oxygen masses are 16 g and 32 g,
a ratio of 1 : 2.
**5.** (b) — EF mass = 30, n = 60/30 = 2.
:::

**Group B — Short answer (5 marks each)**

1. State the postulates of Dalton's atomic theory and mention two of its
   limitations. <span class="marks">[5]</span>
2. State Avogadro's law and derive the relation: molecular mass = 2 × vapour
   density. <span class="marks">[5]</span>
3. Calculate the number of moles, molecules and atoms present in 3.4 g of ammonia
   gas, and the volume it occupies at STP. (N = 14, H = 1) <span class="marks">[5]</span>
4. 6.5 g of zinc is dropped into excess dilute hydrochloric acid. Calculate the
   volume of hydrogen liberated at STP and the mass of zinc chloride formed.
   (Zn = 65, Cl = 35.5) <span class="marks">[5]</span>
5. Define limiting reactant. 50 g of CaCO₃ is treated with 35 g of HCl. Which is
   the limiting reactant, and what mass of CO₂ is produced?
   (Ca = 40, C = 12, O = 16, H = 1, Cl = 35.5) <span class="marks">[5]</span>

::: note Answers to Group B
**3.** M(NH₃) = 17 g mol⁻¹, so n = 3.4/17 = 0.20 mol.
Molecules = 0.20 × 6.022 × 10²³ = 1.204 × 10²³.
Each NH₃ has 4 atoms, so atoms = 4 × 1.204 × 10²³ = 4.82 × 10²³.
Volume at STP = 0.20 × 22.4 = 4.48 L.

**4.** Zn + 2HCl → ZnCl₂ + H₂↑. n(Zn) = 6.5/65 = 0.10 mol.
Mole ratio Zn : H₂ : ZnCl₂ = 1 : 1 : 1, so n(H₂) = n(ZnCl₂) = 0.10 mol.
V(H₂) = 0.10 × 22.4 = 2.24 L at STP.
M(ZnCl₂) = 65 + 71 = 136, so mass = 0.10 × 136 = 13.6 g.

**5.** CaCO₃ + 2HCl → CaCl₂ + H₂O + CO₂↑.
n(CaCO₃) = 50/100 = 0.50 mol; n(HCl) = 35/36.5 = 0.959 mol.
Dividing by coefficients: 0.50/1 = 0.50 and 0.959/2 = 0.479, so **HCl is
limiting**. n(CO₂) = 0.959/2 = 0.479 mol, giving
0.479 × 44 = 21.1 g of CO₂ (equivalently 10.7 L at STP).
:::

**Group C — Long answer (8 marks each)**

1. (a) State the law of multiple proportions. Two oxides of nitrogen contain
   63.6 % and 46.7 % nitrogen by mass. Show that the data illustrate the law and
   identify the oxides. (N = 14, O = 16) <span class="marks">[5]</span>
   (b) Define theoretical yield and percentage yield, and explain two reasons why
   the actual yield of an industrial reaction is always less than the theoretical
   yield. <span class="marks">[3]</span>
2. A hydrocarbon contains 85.7 % carbon and 14.3 % hydrogen by mass. Its vapour
   density is 21. <span class="marks">[8]</span>
   (a) Determine its empirical formula.
   (b) Determine its molecular mass and molecular formula.
   (c) Calculate the volume of oxygen at STP required for the complete combustion
   of 4.2 g of this hydrocarbon.

::: note Answers to Group C
**1 (a).** In 100 g of the first oxide: N = 63.6 g, O = 36.4 g, so oxygen per
1 g of nitrogen = 36.4/63.6 = 0.572. In the second: N = 46.7 g, O = 53.3 g, giving
53.3/46.7 = 1.141. The ratio is 0.572 : 1.141 = 1 : 2, a simple whole-number
ratio, so the law holds. The first is N₂O (28 : 16) and the second is NO (14 : 16).

**1 (b).** Theoretical yield is the maximum product calculable from the balanced
equation for the limiting reactant; percentage yield is actual/theoretical × 100.
Actual yields fall short because many reactions are reversible and reach
equilibrium before completion, side reactions consume reactant, and product is
lost during filtration, transfer and purification.

**2.** (a) C: 85.7/12 = 7.14; H: 14.3/1 = 14.3. Dividing by 7.14 gives 1 : 2, so
the empirical formula is **CH₂** (EF mass 14).

(b) Molecular mass = 2 × VD = 2 × 21 = 42, so n = 42/14 = 3 and the molecular
formula is **C₃H₆** (propene).

(c) C₃H₆ + 4.5O₂ → 3CO₂ + 3H₂O, i.e. 2C₃H₆ + 9O₂ → 6CO₂ + 6H₂O.
n(C₃H₆) = 4.2/42 = 0.10 mol, so n(O₂) = 0.10 × 4.5 = 0.45 mol.
V(O₂) = 0.45 × 22.4 = **10.08 L at STP**.
:::
