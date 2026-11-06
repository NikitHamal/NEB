---
subject: Chemistry
grade: 11
unit: 1
title: Foundation and Fundamentals
hours: 2
area: General and Physical Chemistry
---

Everything you can touch, breathe or drink is matter, and chemistry is the
science of what matter is made of and how it changes. This short opening unit
fixes the vocabulary and the counting rules that the other sixteen units will
use without further comment: atom, molecule, radical, atomic mass unit,
empirical formula, molecular formula. Get these exactly right now and the
stoichiometry in Unit 2 becomes arithmetic instead of guesswork.

::: key What the examiner asks from this unit
Two things, almost every year: a definition (atom vs molecule, empirical vs
molecular formula, atomic mass unit) and a **percentage composition** numerical.
Both are full-mark questions if you show the molar mass working.
:::

## 1.1 General introduction of chemistry

::: definition Chemistry
Chemistry is the branch of science that deals with the **composition,
structure, properties and transformations** of matter, and with the energy
changes that accompany those transformations.
:::

Matter is anything that has mass and occupies space. Chemistry studies matter
at the level of its particles — atoms, molecules and ions — and explains bulk
behaviour (why iron rusts, why ice floats, why a lemon tastes sour) in terms of
what those particles do.

The subject grew out of **alchemy**, the medieval search for a way to turn base
metals into gold. It became a quantitative science when Antoine Lavoisier
(1743–1794) began weighing his reactants and products and stated the law of
conservation of mass; he is called the father of modern chemistry. John Dalton's
atomic theory (1808) then gave the weighings a particle explanation, and the
modern subject follows from there.

| Branch | Deals with |
|---|---|
| Physical chemistry | Principles and laws governing chemical change — energy, rates, equilibrium, structure |
| Inorganic chemistry | Elements and their compounds other than hydrocarbons and their derivatives |
| Organic chemistry | Compounds of carbon: hydrocarbons and their derivatives |
| Analytical chemistry | Detection (qualitative) and estimation (quantitative) of substances |
| Biochemistry | Chemical processes inside living organisms |
| Industrial / applied chemistry | Manufacture of chemicals on a commercial scale |
| Nuclear chemistry | Changes in the nucleus: radioactivity, fission, fusion |
| Environmental chemistry | Chemical species in air, water and soil, and pollution |

## 1.2 Importance and scope of chemistry

Chemistry is called the *central science* because physics, biology, geology,
agriculture, medicine and engineering all borrow from it.

| Field | What chemistry contributes |
|---|---|
| Agriculture | Fertilizers (urea, DAP, potash), pesticides, soil-pH correction with lime |
| Medicine | Drug synthesis — antibiotics, analgesics, vaccines, anaesthetics |
| Industry | Cement, glass, paper, soap and detergents, paints, plastics, textiles |
| Energy | Petroleum refining, LPG, biogas, batteries, solar-cell materials |
| Food | Preservatives, iodisation of salt, vitamins, food testing for adulteration |
| Environment | Water purification, monitoring of SO₂ and CO₂, ozone-layer studies |
| Materials | Alloys, semiconductors, ceramics, nano-materials, polymers |

In Nepal the scope is very concrete. Cement plants at Udayapur and Hetauda
convert limestone (CaCO₃) into clinker; iodised salt distributed by the
Salt Trading Corporation has removed goitre from most hill districts; arsenic
test kits in the Terai screen tube-well water; and the country imports several
hundred thousand tonnes of urea and DAP every year, so knowing the nitrogen
content of a fertilizer bag is a genuinely useful piece of chemistry.

## 1.3 Basic concepts

### Atoms and molecules

::: definition Atom and molecule
An **atom** is the smallest particle of an element that takes part in a chemical
reaction. It may or may not be able to exist independently.
A **molecule** is the smallest particle of an element or compound that can exist
independently and shows all the properties of that substance.
:::

The number of atoms present in one molecule of a substance is its **atomicity**.

| Atomicity | Meaning | Examples |
|---|---|---|
| Monoatomic | 1 atom per molecule | He, Ne, Ar, Na (vapour) |
| Diatomic | 2 atoms | H₂, O₂, N₂, Cl₂, HCl, CO |
| Triatomic | 3 atoms | O₃, H₂O, CO₂ |
| Tetra-atomic | 4 atoms | NH₃, P₄ |
| Polyatomic | many atoms | S₈, C₆H₁₂O₆ |

### Relative masses and the atomic mass unit

An atom of oxygen weighs about 2.66 × 10⁻²³ g. Numbers like this are useless in
the laboratory, so chemists compare masses instead of quoting them. The agreed
standard is the carbon-12 atom.

::: definition Atomic mass unit (amu or u)
One atomic mass unit is **one-twelfth of the mass of one atom of carbon-12**.
1 u = 1.66054 × 10⁻²⁴ g = 1.66054 × 10⁻²⁷ kg.
:::

```figure caption="The carbon-12 standard: one $^{12}$C atom has a mass of $1.9926\times10^{-23}$ g, and one-twelfth of it — the shaded wedge — defines 1 u."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4,3.0))
sizes = [1]*12
explode = [0.16] + [0.0]*11
cols = [SERIES[1]] + ['#e8edf3']*11
w, _ = ax.pie(sizes, explode=explode, colors=cols, startangle=90,
              wedgeprops=dict(edgecolor=MUTED, linewidth=0.8))
ax.text(0, -1.42, 'one atom of carbon-12   =   12 u   =   1.9926 × 10⁻²³ g',
        ha='center', fontsize=9.2, color=INK)
ax.annotate('1 u = 1.66054 × 10⁻²⁴ g', xy=(0.62, 0.95), xytext=(1.15, 1.35),
            fontsize=9.2, color=SERIES[1], ha='center',
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.2, mutation_scale=11))
ax.set_xlim(-1.7, 1.9); ax.set_ylim(-1.7, 1.7)
ax.set_aspect('equal'); ax.axis('off')
```

**Relative atomic mass** of an element is the number of times one atom of that
element is heavier than one-twelfth of a carbon-12 atom. It is a pure ratio, so
it has **no unit**. Expressed in u it is called the atomic mass.

$$ \text{relative atomic mass} = \frac{\text{mass of one atom of the element}}{\frac{1}{12}\times\text{mass of one } ^{12}\text{C atom}} $$

**Relative molecular mass** is defined in the same way for a molecule, and is
obtained simply by adding the atomic masses of all the atoms in the formula. For
ionic compounds, which have no discrete molecules, the same sum is called the
**formula mass**.

::: example Worked example 1.1
**Problem.** Calculate the relative molecular mass of H₂SO₄ and the actual mass
of one molecule of it in grams. (H = 1, S = 32, O = 16)

**Solution.** Adding the atomic masses,

$$ M = 2(1) + 32 + 4(16) = 2 + 32 + 64 = 98 $$

So the relative molecular mass is 98 (no unit); the molecular mass is 98 u.
Since 1 u = 1.66054 × 10⁻²⁴ g,

$$ m = 98 \times 1.66054\times10^{-24}\ \text{g} = 1.627\times10^{-22}\ \text{g} $$
:::

### Radicals

::: definition Radical
A radical is an atom or a group of atoms carrying a net electrical charge which
behaves as a **single unit** in a chemical reaction. Positively charged radicals
are basic radicals (cations); negatively charged ones are acid radicals (anions).
:::

| Valency | Basic radicals (cations) | Acid radicals (anions) |
|---|---|---|
| 1 | Na⁺, K⁺, NH₄⁺, Ag⁺ | Cl⁻, NO₃⁻, OH⁻, HCO₃⁻ |
| 2 | Mg²⁺, Ca²⁺, Fe²⁺, Cu²⁺, Zn²⁺ | SO₄²⁻, CO₃²⁻, O²⁻, S²⁻ |
| 3 | Al³⁺, Fe³⁺ | PO₄³⁻, N³⁻ |

A formula is written by criss-crossing the valencies and reducing: Al³⁺ with
SO₄²⁻ gives Al₂(SO₄)₃; Ca²⁺ with PO₄³⁻ gives Ca₃(PO₄)₂.

### Molecular formula and empirical formula

::: definition The two formulae
The **molecular formula** shows the *actual* number of atoms of each element in
one molecule. The **empirical formula** shows the *simplest whole-number ratio*
of the atoms present.
:::

They are connected by one integer $n$:

$$ \text{molecular formula} = n \times (\text{empirical formula}), \qquad
n = \frac{\text{molecular mass}}{\text{empirical formula mass}} $$

| Compound | Molecular formula | Empirical formula | $n$ |
|---|---|---|---|
| Water | H₂O | H₂O | 1 |
| Hydrogen peroxide | H₂O₂ | HO | 2 |
| Benzene | C₆H₆ | CH | 6 |
| Ethyne | C₂H₂ | CH | 2 |
| Glucose | C₆H₁₂O₆ | CH₂O | 6 |
| Acetic acid | C₂H₄O₂ | CH₂O | 2 |

```figure caption="One empirical formula can belong to many compounds; only the molecular mass fixes $n$."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.0,2.6))
def box(x, y, w, h, txt, fc, tc=INK, fs=9.3):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.035,rounding_size=0.06',
                                fc=fc, ec=MUTED, lw=0.9))
    ax.text(x+w/2, y+h/2, txt, ha='center', va='center', fontsize=fs, color=tc)
box(0.02, 0.38, 0.26, 0.26, 'CH₂O\nempirical unit\nmass 30', '#dce8f4')
items = [('n = 1\nCH₂O\nmethanal, 30', 0.72),
         ('n = 2\nC₂H₄O₂\nacetic acid, 60', 0.38),
         ('n = 6\nC₆H₁₂O₆\nglucose, 180', 0.04)]
for txt, y in items:
    box(0.58, y, 0.40, 0.24, txt, '#f2f4f7')
    ax.annotate('', xy=(0.57, y+0.12), xytext=(0.29, 0.51),
                arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.3, mutation_scale=11))
ax.text(0.43, 0.94, 'multiply by n', ha='center', fontsize=8.8, color=ACCENT)
ax.set_xlim(0,1.02); ax.set_ylim(0,1.02); ax.axis('off')
```

::: caution Empirical formula is not "the small formula"
The empirical formula of ethane (C₂H₆) is CH₃, not CH — you divide by the HCF of
the subscripts, which is 2, not by whatever makes the numbers smallest. And for
many compounds (water, ammonia, methane) the two formulae are identical.
:::

## 1.4 Percentage composition from molecular formula

The **percentage composition** of a compound is the mass of each element present
in 100 g of the compound. From the molecular formula:

$$ \%\ \text{of element X} = \frac{(\text{atomic mass of X})\times(\text{number of X atoms})}{\text{molecular mass of the compound}}\times 100 $$

The percentages of all elements must add up to 100 (allow ±0.1 for rounding) —
that is your free check on the arithmetic.

::: example Worked example 1.2
**Problem.** Find the percentage composition of urea, CO(NH₂)₂.
(C = 12, O = 16, N = 14, H = 1)

**Solution.** Molecular mass:

$$ M = 12 + 16 + 2(14) + 4(1) = 12 + 16 + 28 + 4 = 60 $$

| Element | Mass in 1 mol | Percentage |
|---|---|---|
| C | 12 | (12/60) × 100 = 20.00 % |
| O | 16 | (16/60) × 100 = 26.67 % |
| N | 28 | (28/60) × 100 = 46.67 % |
| H | 4 | (4/60) × 100 = 6.66 % |

Total = 100.00 %. Urea is the richest solid nitrogen fertilizer in common use.
:::

```figure caption="Nitrogen content of common fertilizers, calculated from their formulae. Urea carries more than twice the nitrogen of ammonium sulphate per kilogram."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.8))
names = ['Urea\nCO(NH₂)₂', 'Ammonium\nnitrate\nNH₄NO₃', 'DAP\n(NH₄)₂HPO₄',
         'Ammonium\nsulphate\n(NH₄)₂SO₄', 'Potassium\nnitrate\nKNO₃']
pct = [46.67, 35.00, 21.21, 21.21, 13.86]
bars = ax.bar(np.arange(5), pct, width=0.62,
              color=[SERIES[0], SERIES[0], MUTED, MUTED, MUTED])
bars[0].set_color(SERIES[1])
for i, v in enumerate(pct):
    ax.text(i, v+1.0, f'{v:.1f}%', ha='center', fontsize=8.6, color=INK)
ax.set_xticks(np.arange(5)); ax.set_xticklabels(names, fontsize=7.6)
ax.set_ylabel('nitrogen by mass (%)'); ax.set_ylim(0, 54)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, axis='y', alpha=0.5)
```

::: example Worked example 1.3
**Problem.** A 50 kg bag of ammonium sulphate, (NH₄)₂SO₄, is spread on a paddy
field in Chitwan. What mass of nitrogen does it supply?

**Solution.** Formula mass:

$$ M = 2(14 + 4) + 32 + 4(16) = 36 + 32 + 64 = 132 $$

Nitrogen present in one formula unit = 2 × 14 = 28.

$$ \%\ \text{N} = \frac{28}{132}\times100 = 21.21\ \% $$

$$ \text{mass of N} = \frac{21.21}{100}\times 50\ \text{kg} = 10.6\ \text{kg} $$

The same 50 kg as urea would supply 0.4667 × 50 = 23.3 kg of nitrogen.
:::

::: example Worked example 1.4
**Problem.** Calculate the percentage of water of crystallisation in blue
vitriol, CuSO₄·5H₂O. (Cu = 63.5, S = 32, O = 16, H = 1)

**Solution.** Mass of the anhydrous part: 63.5 + 32 + 4(16) = 159.5.
Mass of five water molecules: 5 × 18 = 90. Total M = 249.5.

$$ \%\ \text{H}_2\text{O} = \frac{90}{249.5}\times100 = 36.07\ \% $$

So heating 100 g of blue vitriol to dryness leaves 63.93 g of white anhydrous
CuSO₄ and drives off 36.07 g of water.
:::

::: tip Saving time in the exam
Write the molar-mass sum as one line of arithmetic and **then** divide. Students
who compute each percentage from scratch make four chances for an error instead
of one. Always finish by adding the percentages to check they give 100.
:::

```photogrid label="1.P" cols="2" ratio="1.27" caption="Percentage composition is the mass of each element in 100 g of a compound, found as (atomic mass x number of atoms) / molar mass x 100. (a) Hydrated copper sulphate crystals. (b) For CuSO4.5H2O the molar mass is 249.68 g/mol and copper makes up 25.45 %, while in the anhydrous salt (M = 159.61) it makes up 39.82 %. The difference is the water of crystallisation, 36.08 % of the crystal, which leaves as steam on heating and turns the blue crystals into white powder. The same arithmetic lets an analyst check the purity of a fertiliser or a drug against its label."
@ photo id="chem12/cuso4" cap="Blue crystals of hydrated copper sulphate"
fit 1.27
focus 0.5 0.5
@ svg cap="Percentage composition of CuSO4.5H2O and CuSO4"
Cu, S, O, H = 63.55, 32.06, 15.999, 1.008
M_an = Cu + S + 4 * O
M_hy = M_an + 5 * (2 * H + O)
hy = dict(Cu=Cu / M_hy * 100, S=S / M_hy * 100, O=(4 * O + 5 * O) / M_hy * 100, H=10 * H / M_hy * 100)
an = dict(Cu=Cu / M_an * 100, S=S / M_an * 100, O=4 * O / M_an * 100, H=0.0)
assert abs(sum(hy.values()) - 100) < 1e-9 and abs(sum(an.values()) - 100) < 1e-9
water = 5 * (2 * H + O) / M_hy * 100
assert abs(M_hy - 249.68) < 0.02 and abs(water - 36.08) < 0.05
cols = dict(Cu=RED, S=AMBER, O=NAVY, H=TEAL)
f = Fig(300, 236)
f.text(150, 14, "Mass percentage of each element", size=10.5, color=NAVY, bold=True)
for row, (title, d, y) in enumerate([("CuSO4.5H2O  M = %.2f" % M_hy, hy, 30), ("CuSO4  M = %.2f" % M_an, an, 100)]):
    f.text(20, y, title, size=10.5, bold=True, anchor="start")
    x = 20
    for k in ("Cu", "S", "O", "H"):
        w = d[k] * 2.6
        if w > 0:
            f.box(x, y + 8, w, 26, k if w > 20 else "", fill=cols[k], stroke=cols[k], color="#ffffff", size=10.5, bold=True, r=0)
        x += w
    f.text(20, y + 52, "  ".join("%s %.1f" % (k, d[k]) for k in ("Cu", "S", "O", "H") if d[k] > 0), size=10, color=SLATE, anchor="start")
f.text(150, 182, "water of crystallisation = %.2f %%" % water, size=10.5, color=NAVY, bold=True)
f.text(150, 198, "heating drives off 90.08 g per 249.68 g", size=10.5, color=RED, bold=True)
f.text(150, 214, "(blue crystals turn white anhydrous powder)", size=10.5, color=SLATE)
facts = dict(Mh="%.2f" % M_hy, Ma="%.2f" % M_an, cu="%.2f" % hy["Cu"], w="%.2f" % water, cua="%.2f" % an["Cu"])
```

## Chapter summary

- Chemistry studies the composition, structure, properties and transformations of
  matter; its main branches are physical, inorganic, organic, analytical,
  biochemistry, industrial, nuclear and environmental.
- An atom is the smallest particle of an element taking part in a reaction; a
  molecule is the smallest particle able to exist independently.
- 1 atomic mass unit = 1/12 of the mass of one ¹²C atom = 1.66054 × 10⁻²⁴ g.
- Relative atomic and molecular masses are ratios and carry no unit; molecular
  mass is the sum of the atomic masses in the formula.
- A radical is a charged atom or group of atoms that acts as one unit; formulae
  are built by criss-crossing valencies.
- Molecular formula = $n$ × empirical formula, with
  $n = \text{molecular mass} / \text{empirical formula mass}$.
- Percentage of X = (atomic mass of X × number of X atoms) / molecular mass × 100;
  all percentages must total 100.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. One atomic mass unit is equal to <span class="marks">[1]</span>
   (a) mass of one ¹²C atom (b) 1/12 of the mass of one ¹²C atom
   (c) mass of one hydrogen atom (d) 1/16 of the mass of one oxygen atom
2. The empirical formula of hydrogen peroxide (H₂O₂) is <span class="marks">[1]</span>
   (a) H₂O₂ (b) HO (c) H₂O (d) HO₂
3. The percentage of nitrogen in ammonium nitrate, NH₄NO₃, is <span class="marks">[1]</span>
   (a) 17.5 % (b) 21.2 % (c) 35.0 % (d) 46.7 %
4. Which of the following is a triatomic molecule? <span class="marks">[1]</span>
   (a) He (b) Cl₂ (c) O₃ (d) P₄
5. Relative atomic mass has the unit <span class="marks">[1]</span>
   (a) gram (b) amu (c) kg mol⁻¹ (d) no unit

::: note Answers to Group A
**1.** (b) — that is the definition of the amu on the carbon-12 scale.
**2.** (b) — divide both subscripts by the HCF 2.
**3.** (c) — M = 80 and 2 N atoms give 28, so 28/80 × 100 = 35.0 %.
**4.** (c) — ozone has three atoms per molecule.
**5.** (d) — it is a ratio of two masses, so the units cancel.
:::

**Group B — Short answer (5 marks each)**

1. Define atom, molecule and radical, giving one example of each. Why can an atom
   of oxygen not exist freely while a molecule of oxygen can? <span class="marks">[5]</span>
2. What is meant by atomic mass unit? Calculate the mass in grams of one molecule
   of carbon dioxide. <span class="marks">[5]</span>
3. Distinguish between empirical formula and molecular formula with two examples
   each. A compound has the empirical formula CH₂ and molecular mass 56; find its
   molecular formula. <span class="marks">[5]</span>
4. Calculate the percentage composition of calcium carbonate, CaCO₃, and hence the
   mass of calcium oxide obtainable from 1 tonne of pure limestone.
   (Ca = 40, C = 12, O = 16) <span class="marks">[5]</span>

::: note Answers to Group B
**2.** 1 u = 1/12 of the mass of a ¹²C atom = 1.66054 × 10⁻²⁴ g. For CO₂,
M = 12 + 32 = 44, so one molecule has mass 44 × 1.66054 × 10⁻²⁴ g
= 7.31 × 10⁻²³ g.

**3.** Empirical formula mass of CH₂ = 12 + 2 = 14, so n = 56/14 = 4 and the
molecular formula is C₄H₈.

**4.** M(CaCO₃) = 40 + 12 + 48 = 100. %Ca = 40 %, %C = 12 %, %O = 48 %.
On heating, CaCO₃ → CaO + CO₂. Every 100 g of CaCO₃ gives 56 g of CaO, so
1 tonne (1000 kg) gives 560 kg of CaO.
:::

**Group C — Long answer (8 marks each)**

1. (a) Explain why chemistry is called the central science, listing four fields in
   which it is applied with one concrete example from Nepal in each. <span class="marks">[4]</span>
   (b) State the relation between empirical formula, molecular formula and
   molecular mass, and use it to show that acetic acid and glucose share an
   empirical formula. <span class="marks">[4]</span>
2. A farmer can buy either urea, CO(NH₂)₂, at Rs 1,000 per 50 kg bag or ammonium
   sulphate, (NH₄)₂SO₄, at Rs 600 per 50 kg bag. <span class="marks">[8]</span>
   (a) Calculate the percentage of nitrogen in each.
   (b) Calculate the mass of nitrogen in one bag of each.
   (c) Find the cost per kilogram of nitrogen for each and say which is cheaper.

::: note Answer to Group C question 2
(a) Urea: M = 60, N = 28, so %N = 28/60 × 100 = 46.67 %.
Ammonium sulphate: M = 132, N = 28, so %N = 28/132 × 100 = 21.21 %.

(b) Urea bag: 0.4667 × 50 = 23.33 kg of N.
Ammonium sulphate bag: 0.2121 × 50 = 10.61 kg of N.

(c) Urea: Rs 1000 / 23.33 kg = Rs 42.9 per kg of N.
Ammonium sulphate: Rs 600 / 10.61 kg = Rs 56.6 per kg of N.
Urea is the cheaper source of nitrogen, even though the bag costs more.
:::

**Group D — Model answers for long questions (10 marks each, for deeper revision)**

1. Explain the mole concept and Avogadro's number, and show how molar mass, molar volume and the number of particles are related, with numericals. <span class="marks">[10]</span>
2. How are the percentage composition, the empirical formula and the molecular formula of a compound determined? Explain limiting reagent and percentage yield with numericals. <span class="marks">[10]</span>

### Model answer D1: the mole concept and Avogadro's number (10 marks)

**Introduction.** Atoms and molecules are far too small to count or weigh one by one. Chemists therefore count them in large groups called **moles**, just as a shopkeeper in Kathmandu sells eggs by the dozen or by the crate.

**Definitions.**

- **Mole:** the amount of a substance that contains as many elementary entities (atoms, molecules, ions or electrons) as there are atoms in exactly $12\ \text{g}$ of carbon-12.
- **Avogadro's number** ($N_A$): the number of entities in one mole, $N_A=6.022\times10^{23}\ \text{mol}^{-1}$.
- **Atomic mass unit (u):** $\tfrac1{12}$ of the mass of one carbon-12 atom, $1.66\times10^{-27}\ \text{kg}$.
- **Molar mass:** the mass of one mole in grams, numerically equal to the relative atomic or molecular mass (H₂O: $18\ \text{g mol}^{-1}$).
- **Molar volume:** one mole of any gas occupies $22.4\ \text{L}$ at STP ($0^{\circ}\text{C}$, $1\ \text{atm}$) and about $24\ \text{L}$ at room temperature (Avogadro's law).

**Relations between the quantities.**

$$ n=\frac{m}{M}=\frac{N}{N_A}=\frac{V_{\text{STP}}}{22.4\ \text{L}} $$

where $n$ is the number of moles, $m$ the mass, $M$ the molar mass, $N$ the number of particles and $V$ the volume of the gas.

**Concentration units.** **Molarity** $=\dfrac{\text{moles of solute}}{\text{litres of solution}}$, and **molality** $=\dfrac{\text{moles of solute}}{\text{kg of solvent}}$.

| Quantity | Symbol | Unit | Link to the mole |
|---|---|---|---|
| Mass | $m$ | g | $n=m/M$ |
| Particles | $N$ | none | $n=N/N_A$ |
| Gas volume | $V$ | L | $n=V/22.4$ at STP |
| Molarity | $M$ | mol L⁻¹ | $n=MV$ |

**Why the mole is important.**

1. It links the invisible atomic world to the weighable laboratory quantities.
2. Chemical equations are read in moles: $2\text{H}_2+\text{O}_2\rightarrow2\text{H}_2\text{O}$ means 2 mol of hydrogen react with 1 mol of oxygen.
3. It is the basis of all calculations on formulae, solutions and gases.

**Numericals.**

1. **Particles in a mass.** In $18\ \text{g}$ of water, $n=18/18=1\ \text{mol}$, so $N=6.022\times10^{23}$ molecules, and the number of atoms is $3\times6.022\times10^{23}=1.81\times10^{24}$.
2. **Volume of gas.** $11\ \text{g}$ of CO₂ ($M=44$) is $0.25\ \text{mol}$ and occupies $0.25\times22.4=5.6\ \text{L}$ at STP.
3. **Mass of one molecule.** One molecule of water has mass $\dfrac{18}{6.022\times10^{23}}=2.99\times10^{-23}\ \text{g}$.

**Conclusion.** The mole is the chemist's counting unit, connecting mass, number of particles and gas volume through the molar mass, Avogadro's number and the molar volume.

### Model answer D2: formulae, limiting reagent and percentage yield (10 marks)

**Introduction.** The composition of a compound is found by analysis and expressed by its formulae. Industrial chemists then use the mole ratios of the balanced equation to plan reactions.

**Percentage composition.** $\%\text{ of element}=\dfrac{\text{mass of the element in one mole}}{\text{molar mass}}\times100$. For calcium carbonate CaCO₃ ($M=100$): Ca $=40\%$, C $=12\%$, O $=48\%$.

**Empirical and molecular formula.**

1. The **empirical formula** gives the simplest whole-number ratio of atoms; the **molecular formula** gives the actual number of atoms in a molecule, $=(\text{empirical formula})_n$ with $n=\dfrac{\text{molar mass}}{\text{empirical formula mass}}$.
2. Steps: (a) write the percentage (or mass) of each element; (b) divide by the atomic mass to get moles; (c) divide all by the smallest to get the ratio; (d) multiply to remove fractions; (e) compare the molar mass to find $n$.

**Worked example.** A compound contains $40.0\%$ C, $6.67\%$ H and $53.3\%$ O, and its molar mass is $180$.

| Element | % | Moles | Ratio |
|---|---|---|---|
| C | 40.0 | $40.0/12=3.33$ | 1 |
| H | 6.67 | $6.67/1=6.67$ | 2 |
| O | 53.3 | $53.3/16=3.33$ | 1 |

The empirical formula is **CH₂O** (mass $30$), so $n=180/30=6$ and the molecular formula is **C₆H₁₂O₆** (glucose).

**Limiting reagent.** In a reaction, the reactant that is consumed first and decides how much product forms is the **limiting reagent**; the other reactant is in **excess**.

- *Example:* $5\ \text{g}$ of H₂ ($2.5\ \text{mol}$) reacts with $32\ \text{g}$ of O₂ ($1\ \text{mol}$) in $2\text{H}_2+\text{O}_2\rightarrow2\text{H}_2\text{O}$.
- $1\ \text{mol}$ of O₂ needs only $2\ \text{mol}$ of H₂, so **O₂ is limiting**, and water formed $=2\ \text{mol}=36\ \text{g}$.
- Hydrogen left over $=2.5-2=0.5\ \text{mol}=1\ \text{g}$.

**Percentage yield.**

$$ \%\text{ yield}=\frac{\text{actual yield}}{\text{theoretical yield}}\times100 $$

*Example:* heating $100\ \text{g}$ of CaCO₃ should give $56\ \text{g}$ of CaO (theoretical). If $50\ \text{g}$ is obtained, the yield is $\dfrac{50}{56}\times100=89.3\%$. Real yields are below $100\%$ because of side reactions, incomplete reaction and losses.

**Conclusion.** Percentage composition leads to the empirical formula, the molar mass gives the molecular formula, and the limiting reagent and percentage yield are the basis of industrial planning.
