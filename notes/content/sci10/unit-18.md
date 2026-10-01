---
subject: Science and Technology
grade: 10
unit: 18
title: Hydrocarbon and its Compounds
hours: 0
area: Science and Technology
---

LPG in your kitchen, petrol in a motorbike, the wax of a candle, the plastic of a bucket, vinegar in a pickle and the alcohol in a hand sanitiser are all compounds of **carbon**. Carbon forms more compounds than all other elements together, because its atoms join to each other in long chains and rings. The study of these compounds is called **organic chemistry**. This chapter starts with the simplest organic compounds, the hydrocarbons, and then moves to two families that you meet in daily life: alcohols and carboxylic acids.

::: key What the SEE paper asks from this chapter
Expect: the general formula and the first members of alkanes, alkenes and alkynes (1 to 2 marks); drawing the structural formula of a given compound (2 marks); the chemical tests that tell an alkane from an alkene (2 marks); the preparation, properties and uses of ethanol and ethanoic acid (4 marks).
:::

## 18.1 Alkanes, alkenes and alkynes

### Why carbon forms so many compounds

- **Tetravalency.** Carbon has 4 valence electrons (2, 4) and forms **four covalent bonds**.
- **Catenation.** Carbon atoms join to each other in long chains, branched chains and rings.
- It forms **single, double and triple** bonds.

A **hydrocarbon** is a compound made only of carbon and hydrogen. Hydrocarbons are of two types:

- **Saturated** hydrocarbons contain only single bonds (alkanes).
- **Unsaturated** hydrocarbons contain at least one double or triple bond (alkenes and alkynes).

### Alkanes (paraffins)

Alkanes have only C–C and C–H single bonds. The general formula is

$$ \text{C}_n\text{H}_{2n+2} $$

| n | Name | Molecular formula | Condensed formula | State at room temperature |
|---|---|---|---|---|
| 1 | Methane | CH₄ | CH₄ | gas |
| 2 | Ethane | C₂H₆ | CH₃CH₃ | gas |
| 3 | Propane | C₃H₈ | CH₃CH₂CH₃ | gas |
| 4 | Butane | C₄H₁₀ | CH₃CH₂CH₂CH₃ | gas |
| 5 | Pentane | C₅H₁₂ | CH₃(CH₂)₃CH₃ | liquid |
| 6 | Hexane | C₆H₁₄ | CH₃(CH₂)₄CH₃ | liquid |

Names of the first four are historical (meth-, eth-, prop-, but-). From five onward the Greek number is used (pent-, hex-, hept-, oct-, non-, dec-). All alkane names end in **-ane**.

```figure caption="Structural formulas of methane, ethene and ethyne. Carbon forms four bonds in every case: single, double and triple."
fig, ax = plt.subplots(figsize=(5.0,2.6))
def txt(x,y,s,**k): ax.text(x,y,s,ha='center',va='center',fontsize=10,color=INK,weight='bold',**k)
def ln(x1,y1,x2,y2): ax.plot([x1,x2],[y1,y2],color=INK,lw=1.6)
txt(1.5,1.5,'C'); txt(1.5,2.7,'H'); txt(1.5,0.3,'H'); txt(0.3,1.5,'H'); txt(2.7,1.5,'H')
ln(1.5,1.7,1.5,2.5); ln(1.5,1.3,1.5,0.5); ln(1.7,1.5,2.5,1.5); ln(0.5,1.5,1.3,1.5)
ax.text(1.5,-0.5,'methane CH₄',ha='center',fontsize=8,color=INK)
txt(5.4,1.5,'C'); txt(6.8,1.5,'C'); txt(4.6,2.5,'H'); txt(4.6,0.5,'H'); txt(7.6,2.5,'H'); txt(7.6,0.5,'H')
ln(5.6,1.58,6.6,1.58); ln(5.6,1.42,6.6,1.42)
ln(5.25,1.68,4.8,2.3); ln(5.25,1.32,4.8,0.7); ln(6.95,1.68,7.4,2.3); ln(6.95,1.32,7.4,0.7)
ax.text(6.1,-0.5,'ethene C₂H₄',ha='center',fontsize=8,color=INK)
txt(9.6,1.5,'H'); txt(10.9,1.5,'C'); txt(12.3,1.5,'C'); txt(13.6,1.5,'H')
ln(9.8,1.5,10.7,1.5); ln(11.1,1.62,12.1,1.62); ln(11.1,1.5,12.1,1.5); ln(11.1,1.38,12.1,1.38); ln(12.5,1.5,13.4,1.5)
ax.text(11.6,-0.5,'ethyne C₂H₂',ha='center',fontsize=8,color=INK)
ax.set_xlim(-0.5,14.2); ax.set_ylim(-0.9,3.2); ax.set_aspect('equal'); ax.axis('off')
```

#### Properties of alkanes

- **Physical:** colourless; insoluble in water, soluble in organic solvents; boiling point rises with size; lighter than water.
- **Chemical:** fairly unreactive because all bonds are single and strong.

| Reaction | Equation |
|---|---|
| Combustion (burning in excess air) | CH₄ + 2O₂ → CO₂ + 2H₂O + heat |
| Combustion of propane (LPG) | C₃H₈ + 5O₂ → 3CO₂ + 4H₂O |
| Substitution (with chlorine in sunlight) | CH₄ + Cl₂ --sunlight--> CH₃Cl + HCl |

In **substitution**, one hydrogen atom is replaced by another atom or group.

**Uses.** Methane (biogas, natural gas) for cooking; propane and butane (LPG); petrol, kerosene and diesel as fuel; paraffin wax in candles; bitumen on roads.

::: tip Biogas in Nepal
Biogas plants in Nepali villages produce **methane** (about 60 %) from cattle dung and kitchen waste by anaerobic decay. It burns with a clean blue flame and replaces firewood.
:::

### Alkenes (olefins)

Alkenes have **one C=C double bond**. General formula:

$$ \text{C}_n\text{H}_{2n} \qquad (n \ge 2) $$

| n | Name | Formula | Structure |
|---|---|---|---|
| 2 | Ethene (ethylene) | C₂H₄ | CH₂=CH₂ |
| 3 | Propene | C₃H₆ | CH₃CH=CH₂ |
| 4 | Butene | C₄H₈ | CH₃CH₂CH=CH₂ |

Names end in **-ene**.

**Laboratory preparation of ethene.** Ethanol is heated with excess concentrated sulphuric acid (a dehydrating agent) at 170 °C.

CH₃CH₂OH --conc. H₂SO₄, 170 °C--> CH₂=CH₂ + H₂O

**Properties.** Colourless gas with a faint sweet smell; slightly soluble in water. Alkenes are **reactive** because the double bond can break open.

| Reaction | Equation |
|---|---|
| Combustion | C₂H₄ + 3O₂ → 2CO₂ + 2H₂O (burns with a smoky flame) |
| **Addition** of hydrogen (Ni catalyst, 200 °C) | CH₂=CH₂ + H₂ → CH₃CH₃ |
| Addition of bromine | CH₂=CH₂ + Br₂ → CH₂Br–CH₂Br |
| Addition of HCl | CH₂=CH₂ + HCl → CH₃CH₂Cl |
| **Polymerisation** | n CH₂=CH₂ → –(CH₂–CH₂)ₙ– (polythene) |

**Uses.** Making polythene, ripening of fruits, making ethanol, and in welding and cutting as a fuel gas.

### Alkynes

Alkynes have **one C≡C triple bond**. General formula:

$$ \text{C}_n\text{H}_{2n-2} \qquad (n \ge 2) $$

| n | Name | Formula | Structure |
|---|---|---|---|
| 2 | Ethyne (acetylene) | C₂H₂ | HC≡CH |
| 3 | Propyne | C₃H₄ | CH₃C≡CH |
| 4 | Butyne | C₄H₆ | CH₃CH₂C≡CH |

Names end in **-yne**.

**Laboratory preparation of ethyne.** Calcium carbide reacts with cold water:

CaC₂ + 2H₂O → C₂H₂ ↑ + Ca(OH)₂

The gas is collected over water. It is colourless, with a garlic-like smell when impure (from traces of phosphine).

| Reaction | Equation |
|---|---|
| Combustion | 2C₂H₂ + 5O₂ → 4CO₂ + 2H₂O (very sooty flame, very hot) |
| Addition of H₂ (Ni) | C₂H₂ + 2H₂ → C₂H₆ |
| Addition of Br₂ | C₂H₂ + 2Br₂ → CHBr₂–CHBr₂ |

**Uses.** Oxy-acetylene flame for welding and cutting metals (about 3000 °C); making plastics and ethanoic acid; old miners' lamps.

### Tests to separate alkanes from alkenes and alkynes

| Test | Alkane | Alkene / alkyne |
|---|---|---|
| **Bromine water** (red-brown) | stays red-brown | decolourised |
| **Baeyer's reagent** (cold dilute alkaline KMnO₄, pink-purple) | no change | purple colour disappears |
| Flame | clear or blue, little smoke | yellow, smoky (more in alkyne) |

::: caution Saturated or unsaturated?
"Saturated" does **not** mean "contains water". It means all carbon atoms are bonded to the maximum possible number of other atoms (only single bonds). Unsaturated compounds can still add atoms across a double or triple bond.
:::

## 18.2 Homologous series

::: definition Homologous series
A **homologous series** is a family of organic compounds that have the same functional group, the same general formula, similar chemical properties, and in which the successive members differ by a **–CH₂–** group (14 mass units).
:::

### Characteristics

1. All members can be represented by one general formula (alkanes C$_n$H$_{2n+2}$).
2. Successive members differ by CH₂ (relative molecular mass 14).
3. Chemical properties are similar, because they have the same functional group.
4. Physical properties change gradually: melting and boiling points rise with the molecular mass.
5. They can be made by similar methods.

```figure caption="Boiling points of the first eight alkanes. The gradual rise with the number of carbon atoms is a property of the homologous series."
n = np.arange(1, 9)
bp = [-162, -89, -42, -1, 36, 69, 98, 126]
names = ['CH₄','C₂H₆','C₃H₈','C₄H₁₀','C₅H₁₂','C₆H₁₄','C₇H₁₆','C₈H₁₈']
fig, ax = plt.subplots(figsize=(4.6,2.8))
ax.plot(n, bp, marker='o', color=ACCENT, lw=1.8, ms=4)
ax.axhline(25, color=GRID, ls='--', lw=0.8); ax.text(1.0, 32, 'room temperature (25 °C)', fontsize=6.8, color=MUTED)
for x,y,s in zip(n,bp,names): ax.text(x, y+(-22 if x<5 else 12), s, ha='center', fontsize=6, color=INK, rotation=0)
ax.set_xlabel('number of carbon atoms', fontsize=8, color=INK); ax.set_ylabel('boiling point (°C)', fontsize=8, color=INK)
ax.spines[['top','right']].set_visible(False); ax.grid(color=GRID, lw=0.4); ax.tick_params(labelsize=7)
ax.set_ylim(-200, 170)
fig.tight_layout()
```

### Functional group

A **functional group** is the atom or group of atoms that decides the chemical properties of a compound.

| Homologous series | Functional group | General formula | First member |
|---|---|---|---|
| Alkane | none (C–C) | CₙH₂ₙ₊₂ | methane |
| Alkene | C=C | CₙH₂ₙ | ethene |
| Alkyne | C≡C | CₙH₂ₙ₋₂ | ethyne |
| Alcohol | –OH (hydroxyl) | CₙH₂ₙ₊₁OH | methanol |
| Carboxylic acid | –COOH (carboxyl) | CₙH₂ₙ₊₁COOH | methanoic acid |

::: example Molecular formula from the general formula
**Problem.** Write the molecular formula of the alkane, alkene and alkyne having 5 carbon atoms.

**Solution.** n = 5. Alkane: 2 × 5 + 2 = 12 hydrogen atoms, **C₅H₁₂** (pentane). Alkene: 2 × 5 = 10, **C₅H₁₀** (pentene). Alkyne: 2 × 5 − 2 = 8, **C₅H₈** (pentyne).
:::

::: example Molecular mass
**Problem.** Find the relative molecular mass of butane and show that it differs from propane by 14. (C = 12, H = 1.)

**Solution.** Butane C₄H₁₀: 4 × 12 + 10 × 1 = 48 + 10 = **58**. Propane C₃H₈: 3 × 12 + 8 = 36 + 8 = **44**. Difference = 58 − 44 = **14**, the mass of one CH₂.
:::

::: example Which hydrocarbon is the unknown?
**Problem.** A hydrocarbon has 4 carbon atoms and 6 hydrogen atoms. Is it an alkane, alkene or alkyne? Will it decolourise bromine water?

**Solution.** For n = 4: alkane has 10 H, alkene has 8 H, alkyne has 2 × 4 − 2 = 6 H. So C₄H₆ is an **alkyne** (unsaturated). It **will decolourise** bromine water.
:::

## 18.3 Alcohols

An **alcohol** is an organic compound in which one or more hydrogen atoms of an alkane is replaced by the hydroxyl group (–OH). General formula for the simple (monohydric) alcohols: **CₙH₂ₙ₊₁OH**. Names end in **-ol**.

| Name | Formula | Structure |
|---|---|---|
| Methanol (methyl alcohol) | CH₃OH | CH₃–OH |
| Ethanol (ethyl alcohol) | C₂H₅OH | CH₃CH₂–OH |
| Propanol | C₃H₇OH | CH₃CH₂CH₂–OH |

### Ethanol

**Preparation by fermentation.** Sugar from molasses, rice, millet or grapes is changed to ethanol by the enzymes in yeast (zymase). Local drinks of Nepal such as *jaand* and *raksi* are made by fermentation.

C₆H₁₂O₆ --zymase--> 2C₂H₅OH + 2CO₂ ↑

Other methods: hydration of ethene (C₂H₄ + H₂O → C₂H₅OH, steam, phosphoric acid catalyst, high pressure).

**Physical properties.** Colourless liquid with a pleasant smell and burning taste; boiling point 78 °C; mixes with water in all proportions; a good solvent.

**Chemical properties.**

| Reaction | Equation |
|---|---|
| Combustion | C₂H₅OH + 3O₂ → 2CO₂ + 3H₂O (burns with a blue, almost smokeless flame) |
| With sodium | 2C₂H₅OH + 2Na → 2C₂H₅ONa + H₂ ↑ (sodium ethoxide) |
| Oxidation (acidified K₂Cr₂O₇ or alkaline KMnO₄) | C₂H₅OH + 2[O] → CH₃COOH + H₂O |
| Dehydration (conc. H₂SO₄, 170 °C) | C₂H₅OH → C₂H₄ + H₂O |
| Esterification (with ethanoic acid) | CH₃COOH + C₂H₅OH ⇌ CH₃COOC₂H₅ + H₂O (conc. H₂SO₄) |

Ethanol does not change the colour of litmus (it is neutral).

**Uses.** Solvent for paints, perfumes and medicines; antiseptic and hand sanitiser (70 %); fuel (blended with petrol; gasohol); preparation of ethanoic acid and ether; alcoholic drinks.

::: caution Methanol is a poison
Methanol, or wood spirit, looks like ethanol but is poisonous: even a small amount can cause blindness or death. Adulterated local liquor containing methanol causes deaths every year. **Denatured spirit** is ethanol made unfit to drink by adding methanol and a blue dye.
:::

::: tip Rectified, absolute and denatured
Fermentation gives about 10 to 15 % ethanol. Distillation gives **rectified spirit** (about 95 %). Removing the last 5 % of water gives **absolute alcohol** (100 %).
:::

## 18.4 Carboxylic acids

A **carboxylic acid** is an organic compound containing the carboxyl group **–COOH**. General formula: **CₙH₂ₙ₊₁COOH** (or R–COOH). Names end in **-oic acid**.

| Name (common name) | Formula | Source |
|---|---|---|
| Methanoic acid (formic acid) | HCOOH | red ants, nettle sting (sisnu) |
| Ethanoic acid (acetic acid) | CH₃COOH | vinegar |
| Propanoic acid | C₂H₅COOH | preservative in bread |

### Ethanoic acid (acetic acid)

**Preparation.** Oxidation of ethanol by acidified potassium dichromate:

CH₃CH₂OH + 2[O] → CH₃COOH + H₂O

Vinegar is made when bacteria (*Acetobacter*) oxidise dilute ethanol (as in fermented fruit juice or rice) with air. Vinegar contains 5 to 8 % ethanoic acid. Pure (100 %) ethanoic acid freezes at 16.6 °C into ice-like crystals and is called **glacial acetic acid**.

**Physical properties.** Colourless liquid with sharp pungent smell and sour taste; miscible with water; boiling point 118 °C.

**Chemical properties.** It is a **weak acid**.

| Reaction | Equation |
|---|---|
| With litmus | turns blue litmus red |
| With metals | 2CH₃COOH + Zn → (CH₃COO)₂Zn + H₂ ↑ |
| With carbonates / bicarbonates | 2CH₃COOH + Na₂CO₃ → 2CH₃COONa + H₂O + CO₂ ↑ ; CH₃COOH + NaHCO₃ → CH₃COONa + H₂O + CO₂ ↑ |
| With bases | CH₃COOH + NaOH → CH₃COONa + H₂O |
| With alcohols (esterification) | CH₃COOH + C₂H₅OH ⇌ CH₃COOC₂H₅ + H₂O |

The **brisk effervescence with sodium bicarbonate** is the test that separates a carboxylic acid from an alcohol (alcohols give no gas with NaHCO₃).

**Esterification.** The reaction of an alcohol with a carboxylic acid in the presence of a little conc. H₂SO₄ gives a sweet-smelling **ester** and water. Esters are used as perfumes, in artificial fruit flavours and as solvents.

**Uses.** Vinegar for food and pickles; making dyes, plastics, rayon and medicines; preparing esters; making cellulose acetate; as a solvent.

| | Ethanol | Ethanoic acid |
|---|---|---|
| Functional group | –OH | –COOH |
| Litmus | no effect | turns blue litmus red |
| NaHCO₃ | no reaction | CO₂ with brisk fizz |
| Smell | sweet, spirit-like | pungent, vinegar |
| Nature | neutral | weak acid |

::: example Balancing combustion
**Problem.** Balance the equation for the complete combustion of butane: C₄H₁₀ + O₂ → CO₂ + H₂O.

**Solution.** Carbon: 4 on the left, so 4CO₂. Hydrogen: 10, so 5H₂O. Oxygen needed on the right = 4 × 2 + 5 = 13, so O₂ = 13/2. Multiply all by 2: **2C₄H₁₀ + 13O₂ → 8CO₂ + 10H₂O**.
:::

::: example Percentage of carbon
**Problem.** Find the percentage of carbon in ethane, C₂H₆, and in ethene, C₂H₄. (C = 12, H = 1.)

**Solution.** Ethane: mass = 24 + 6 = 30; % C = 24/30 × 100 = **80 %**. Ethene: mass = 24 + 4 = 28; % C = 24/28 × 100 = **85.7 %**. The unsaturated compound has more carbon, so it burns with a smokier flame.
:::

## Chapter summary

- Carbon is tetravalent and shows catenation; hydrocarbons contain only C and H.
- Alkanes CₙH₂ₙ₊₂ (single bonds, substitution); alkenes CₙH₂ₙ (C=C, addition and polymerisation); alkynes CₙH₂ₙ₋₂ (C≡C, addition).
- Unsaturated hydrocarbons decolourise bromine water and Baeyer's reagent; alkanes do not.
- A homologous series has the same functional group and general formula, and members differ by –CH₂– (14 u).
- Alcohols CₙH₂ₙ₊₁OH (–OH): ethanol is made by fermentation of sugar; it reacts with Na to give H₂; oxidises to ethanoic acid; methanol is poisonous.
- Carboxylic acids CₙH₂ₙ₊₁COOH (–COOH): ethanoic acid (vinegar) is a weak acid, gives CO₂ with NaHCO₃, and forms esters with alcohols.

## Practice questions

**Group A — Objective questions (1 mark each)**

1. The general formula of alkenes is <span class="marks">[1]</span>
   (a) CₙH₂ₙ₊₂ (b) CₙH₂ₙ (c) CₙH₂ₙ₋₂ (d) CₙHₙ
2. The functional group of alcohols is <span class="marks">[1]</span>
   (a) –COOH (b) –CHO (c) –OH (d) C=C
3. Which gas is produced when calcium carbide reacts with water? <span class="marks">[1]</span>
   (a) methane (b) ethene (c) ethyne (d) hydrogen
4. Vinegar contains <span class="marks">[1]</span>
   (a) formic acid (b) ethanoic acid (c) citric acid (d) lactic acid
5. Which compound will decolourise bromine water? <span class="marks">[1]</span>
   (a) C₂H₆ (b) CH₄ (c) C₂H₄ (d) C₃H₈
6. The next member after C₃H₈ in the alkane series is <span class="marks">[1]</span>
   (a) C₄H₈ (b) C₄H₁₀ (c) C₄H₁₂ (d) C₅H₁₂

::: note Answers to Group A
**1.** (b) — CₙH₂ₙ.
**2.** (c) — hydroxyl.
**3.** (c) — CaC₂ + 2H₂O → C₂H₂ + Ca(OH)₂.
**4.** (b) — 5 to 8 % acetic acid.
**5.** (c) — ethene is unsaturated.
**6.** (b) — add CH₂ to C₃H₈.
:::

**Group B — Short answer (2 marks each)**

1. What is a homologous series? Give two characteristics. <span class="marks">[2]</span>
2. Write the molecular formula and structural formula of ethyne. <span class="marks">[2]</span>
3. How would you distinguish ethane from ethene in the laboratory? <span class="marks">[2]</span>
4. Write the equation for the reaction of ethanoic acid with sodium bicarbonate. <span class="marks">[2]</span>
5. What is esterification? Write an equation. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** A family of organic compounds with the same functional group and general formula, in which successive members differ by CH₂. Characteristics: gradual change in physical properties; similar chemical properties.
**2.** C₂H₂; H–C≡C–H.
**3.** Shake each with bromine water: ethene decolourises it; ethane does not.
**4.** CH₃COOH + NaHCO₃ → CH₃COONa + H₂O + CO₂ ↑.
**5.** Reaction of an alcohol and a carboxylic acid in presence of conc. H₂SO₄ to give an ester and water: CH₃COOH + C₂H₅OH ⇌ CH₃COOC₂H₅ + H₂O.
:::

**Group C — Long answer (4 marks each)**

1. Write the preparation, two properties and two uses of ethanol. <span class="marks">[4]</span>
2. Compare alkanes, alkenes and alkynes in terms of general formula, bond type, example and type of reaction. <span class="marks">[4]</span>
3. Describe the laboratory preparation of ethyne and write two of its reactions. <span class="marks">[4]</span>
4. Write the formulae of the alkane, alkene and alkyne with 6 carbon atoms and calculate the molecular mass of the alkane (C = 12, H = 1). <span class="marks">[4]</span>

::: note Answers to Group C
**1.** Fermentation: C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂ with yeast. Properties: colourless liquid, miscible with water; reacts with sodium giving H₂; burns with a blue flame. Uses: solvent, sanitiser, fuel.
**2.** Alkanes CₙH₂ₙ₊₂, single bond, ethane, substitution. Alkenes CₙH₂ₙ, double bond, ethene, addition. Alkynes CₙH₂ₙ₋₂, triple bond, ethyne, addition.
**3.** CaC₂ + 2H₂O → C₂H₂ + Ca(OH)₂, gas collected over water. Reactions: 2C₂H₂ + 5O₂ → 4CO₂ + 2H₂O; C₂H₂ + 2H₂ → C₂H₆ (Ni).
**4.** Alkane C₆H₁₄, alkene C₆H₁₂, alkyne C₆H₁₀. Mass of C₆H₁₄ = 72 + 14 = **86**.
:::
