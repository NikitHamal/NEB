---
subject: Science and Technology
grade: 10
unit: 17
title: Metal and Non-metals
hours: 0
area: Science and Technology
---

Most of the things you see around you are made from metals or from non-metals: the iron of a bridge, the copper wire in a switch board, the aluminium of a pressure cooker, the carbon in a pencil and the oxygen you breathe. Nepal has rich deposits of limestone, iron ore, copper and magnetite, but the metals must be separated from their ores before they can be used. In this chapter you will compare metals with non-metals, learn why some metals react violently and others hardly react, see how metals are extracted from ores, and find out why iron rusts and how to stop it.

::: key What the SEE paper asks from this chapter
Expect: differences between metals and non-metals (2 to 4 marks); the reactivity series and a reaction that uses it, such as displacement (2 marks); the extraction steps for a metal such as iron or aluminium (4 marks); and the causes and prevention of corrosion (2 to 4 marks).
:::

## 17.1 Physical and chemical properties

### Physical properties

| Property | Metals | Non-metals |
|---|---|---|
| Appearance | shiny (lustrous) | dull (except iodine, graphite, diamond) |
| Hardness | usually hard (Na, K are soft) | usually soft (diamond is the hardest known natural substance) |
| State at room temperature | solid (except mercury, a liquid) | solid, liquid (bromine) or gas |
| Malleability and ductility | malleable (beaten into sheets) and ductile (drawn into wires) | brittle, break when hammered |
| Conduction of heat and electricity | good conductors (silver and copper best) | poor conductors (graphite conducts electricity) |
| Sound | sonorous (ring when struck) | not sonorous |
| Density, melting and boiling points | usually high | usually low |
| Examples | Fe, Cu, Al, Zn, Au, Ag | C, S, P, O₂, N₂, Br₂ |

### Chemical properties

#### 1. Reaction with oxygen

Metals form **basic oxides**; non-metals form **acidic oxides**.

| Reaction | Nature of oxide |
|---|---|
| 4Na + O₂ → 2Na₂O | basic (Na₂O + H₂O → 2NaOH) |
| 2Mg + O₂ → 2MgO | basic |
| 2Cu + O₂ --Δ--> 2CuO | basic |
| C + O₂ → CO₂ | acidic (CO₂ + H₂O ⇌ H₂CO₃) |
| S + O₂ → SO₂ | acidic (SO₂ + H₂O → H₂SO₃) |

Some oxides show both properties and are **amphoteric**, such as aluminium oxide (Al₂O₃) and zinc oxide (ZnO). They react with both acids and bases.

#### 2. Reaction with water

| Metal | Reaction |
|---|---|
| Potassium, sodium | violent with cold water: 2Na + 2H₂O → 2NaOH + H₂ ↑ (heat released) |
| Calcium | steadily with cold water: Ca + 2H₂O → Ca(OH)₂ + H₂ ↑ |
| Magnesium | slow with cold water; fast with hot water: Mg + 2H₂O → Mg(OH)₂ + H₂ ↑ |
| Aluminium, zinc, iron | react only with steam: 3Fe + 4H₂O(steam) ⇌ Fe₃O₄ + 4H₂ |
| Copper, silver, gold | do not react with water |

Sodium and potassium are stored under **kerosene** to keep them away from air and moisture.

#### 3. Reaction with acids

Metals above hydrogen in the reactivity series release hydrogen from dilute acids:

Mg + 2HCl → MgCl₂ + H₂ ↑

Zn + H₂SO₄ → ZnSO₄ + H₂ ↑

Copper, silver and gold do not react with dilute HCl or dilute H₂SO₄. Non-metals do not react with dilute acids.

#### 4. Reaction with salt solutions (displacement)

A more reactive metal displaces a less reactive one from its salt solution:

Zn + CuSO₄ → ZnSO₄ + Cu

Cu + 2AgNO₃ → Cu(NO₃)₂ + 2Ag

#### 5. Formation of ions and compounds

Metals lose electrons to form **positive ions** (Na → Na⁺ + e⁻); non-metals gain electrons to form **negative ions** (Cl + e⁻ → Cl⁻). The oppositely charged ions attract to form **ionic compounds** such as NaCl. These compounds are hard, brittle crystals with high melting points that conduct electricity when molten or dissolved in water.

### Metals and non-metals compared in chemical behaviour

| Property | Metals | Non-metals |
|---|---|---|
| Electrons in the outer shell | usually 1 to 3 | usually 4 to 7 |
| Behaviour | lose electrons (electropositive) | gain electrons (electronegative) |
| Oxides | basic | acidic |
| Reaction with dilute acid | release H₂ (if reactive enough) | no reaction |
| Chloride | ionic solid | covalent (liquid or gas) |

### Alloys

An **alloy** is a homogeneous mixture of a metal with other metals or non-metals. Alloys are made to give hardness, strength or resistance to rusting.

| Alloy | Composition | Use |
|---|---|---|
| Brass | Cu + Zn | utensils, musical instruments, taps |
| Bronze | Cu + Sn | statues, bells, medals (Kathmandu valley temple bells) |
| Steel | Fe + C (up to 2 %) | bridges, machines |
| Stainless steel | Fe + Cr + Ni + C | kitchen utensils, surgical instruments |
| Duralumin | Al + Cu + Mg + Mn | aircraft parts |
| Solder | Pb + Sn | joining wires |

## 17.2 Reactivity series

### What is the reactivity series?

The **reactivity series** is a list of metals arranged in the order of decreasing reactivity (their tendency to lose electrons and form positive ions).

::: memory Reactivity series
K, Na, Ca, Mg, Al, Zn, Fe, Pb, (H), Cu, Hg, Ag, Au. A common aid is "Please Stop Calling Me A Careless Zebra Instead Try Learning How Copper Saves Gold" (K, Na, Ca, Mg, Al, C, Zn, Fe, Sn, Pb, H, Cu, Ag, Au).
:::

```figure caption="The reactivity series. Reactivity falls from top to bottom; hydrogen is included for comparison. Metals above hydrogen displace it from dilute acids."
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(4.6,3.4))
metals = ['K','Na','Ca','Mg','Al','Zn','Fe','Pb','H','Cu','Hg','Ag','Au']
notes = ['most reactive; stored under kerosene','violent with cold water','reacts with cold water','burns with a bright flame','protective oxide layer','reacts with steam','rusts in moist air','reacts slowly with acids','(reference, not a metal)','no reaction with dilute acid','liquid metal','used in jewellery and coins','least reactive; found free']
n = len(metals)
for i,m in enumerate(metals):
    f = 0.95 - 0.8*i/(n-1)
    col = (0.15+0.0*f, 0.35+0.35*(1-f), 0.80*f+0.2) if m != 'H' else (0.9,0.9,0.9)
    ax.add_patch(Rectangle((0, n-1-i), 1.0, 0.86, fc=col, ec='white'))
    ax.text(0.5, n-1-i+0.43, m, ha='center', va='center', fontsize=8, color='white' if m!='H' else INK, weight='bold')
    ax.text(1.15, n-1-i+0.43, notes[i], va='center', fontsize=7, color=INK)
ax.annotate('', xy=(-0.55, 0.2), xytext=(-0.55, n-0.3), arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.2))
ax.text(-0.75, n/2, 'decreasing reactivity', rotation=90, va='center', ha='center', fontsize=7.5, color=INK)
ax.set_xlim(-1.0, 5.2); ax.set_ylim(-0.2, n+0.1); ax.axis('off')
```

### Uses of the series

1. It **predicts displacement**: a metal displaces any metal below it from its salt solution.
2. It **predicts reaction with acids**: only metals above hydrogen give hydrogen.
3. It **chooses the method of extraction**: metals high in the series need electrolysis; those in the middle are reduced with carbon; those at the bottom are found free or obtained by heating the ore.

::: example Will the reaction happen?
**Problem.** Will iron displace copper from copper sulphate solution? Will copper displace zinc from zinc sulphate solution? Write the equation where a reaction occurs.

**Solution.** Iron is above copper in the series, so it is more reactive and **will** displace copper: Fe + CuSO₄ → FeSO₄ + Cu. Copper is below zinc, so it is less reactive and **will not** displace zinc: no reaction.
:::

::: example Predicting the order
**Problem.** X displaces Y from the solution of Y's salt. Y displaces Z. Arrange X, Y, Z in decreasing order of reactivity.

**Solution.** X is more reactive than Y, and Y is more reactive than Z. The order is **X > Y > Z**.
:::

## 17.3 Extraction of metals

### Minerals and ores

- A **mineral** is a natural substance in the earth's crust that contains a metal in the form of its compounds.
- An **ore** is a mineral from which the metal can be extracted **conveniently and profitably**.
- **Gangue** (matrix) is the sand, soil and rock impurity mixed with the ore.
- **Metallurgy** is the whole process of extracting a metal from its ore and refining it.

```photo id="sci10/iron-ore" caption="A piece of iron ore (hematite and limonite) with a ruler for scale. Iron is extracted from ores like this." width="56"
```

```photo id="sci10/bauxite" caption="Bauxite, the ore from which aluminium is extracted." width="56"
```

| Metal | Chief ore | Formula |
|---|---|---|
| Iron | haematite | Fe₂O₃ |
| | magnetite | Fe₃O₄ |
| Aluminium | bauxite | Al₂O₃·2H₂O |
| Copper | copper pyrite | CuFeS₂ |
| | copper glance | Cu₂S |
| Zinc | zinc blende | ZnS |
| Sodium | rock salt | NaCl |
| Lead | galena | PbS |

```photo id="sci10/malachite" caption="Malachite, a green ore of copper (copper carbonate)." width="56"
```

All ores are minerals, but not all minerals are ores. Clay contains aluminium, but it is not an ore of aluminium because extraction from it is not profitable.

### Steps in metallurgy

1. **Crushing and grinding** the ore to powder.
2. **Concentration (dressing)** to remove gangue: hand picking, gravity separation (washing), magnetic separation (for magnetite), froth flotation (for sulphide ores).
3. **Conversion to oxide:** *calcination* (heating a carbonate or hydrated ore in limited or no air, CaCO₃ → CaO + CO₂) or *roasting* (heating a sulphide ore in excess air, 2ZnS + 3O₂ → 2ZnO + 2SO₂).
4. **Reduction** of the oxide to the metal by carbon, carbon monoxide, aluminium or electrolysis.
5. **Refining (purification)** of the crude metal, for example electrolytic refining of copper.

### Extraction according to reactivity

| Position in series | Method | Example |
|---|---|---|
| K, Na, Ca, Mg, Al | **electrolysis** of the molten compound | 2Al₂O₃ → 4Al + 3O₂ |
| Zn, Fe, Pb, Sn | **reduction** of the oxide with carbon or CO | Fe₂O₃ + 3CO → 2Fe + 3CO₂ |
| Hg (cinnabar, HgS) | **heating** the ore (roasting) | 2HgS + 3O₂ → 2HgO + 2SO₂; 2HgO → 2Hg + O₂ |
| Ag, Au, Pt | found **free (native)** in nature | washing away the sand |

### Extraction of iron (blast furnace)

Iron is extracted in a tall steel furnace lined with fire-bricks. The charge of **haematite (Fe₂O₃), coke (carbon) and limestone (CaCO₃)** is fed from the top. A blast of hot air is blown from near the bottom.

| Zone | Reaction |
|---|---|
| Bottom (about 1500 °C) | coke burns: C + O₂ → CO₂ (heat released) |
| Middle | CO₂ + C → 2CO (carbon monoxide, the reducing agent) |
| Upper-middle (about 700 °C) | reduction: Fe₂O₃ + 3CO → 2Fe + 3CO₂ |
| Flux action | limestone decomposes: CaCO₃ → CaO + CO₂; then CaO + SiO₂ → CaSiO₃ (slag) |

The molten iron sinks to the bottom, with the lighter molten slag floating on it. Both are tapped off separately. The iron from the furnace is **pig iron** (impure, 3 to 5 % carbon); it is converted into **steel** by removing excess carbon.

```figure caption="Blast furnace for iron: raw materials enter at the top, hot air enters near the bottom, and molten iron and slag are tapped at the base."
from matplotlib.patches import Polygon
fig, ax = plt.subplots(figsize=(4.6,3.6))
body = Polygon([[1.2,0.8],[3.8,0.8],[4.5,3.3],[3.4,5.0],[1.6,5.0],[0.5,3.3]], fc='#f1e4d8', ec=INK, lw=1.5)
ax.add_patch(body)
ax.add_patch(Polygon([[1.2,0.8],[3.8,0.8],[3.95,1.6],[1.05,1.6]], fc='#e57a2c', ec='none', alpha=0.85))
ax.add_patch(Polygon([[1.6,5.0],[3.4,5.0],[3.7,5.4],[1.3,5.4]], fc='white', ec=INK, lw=1.2))
ax.annotate('charge: haematite,\ncoke, limestone', xy=(3.6,5.4), xytext=(5.0,5.7), fontsize=7, color=INK, va='center', arrowprops=dict(arrowstyle='->', color=INK, lw=0.9))
ax.annotate('waste gases (CO, CO₂, N₂)', xy=(3.5,5.0), xytext=(5.0,4.9), fontsize=7, color=INK, va='center', arrowprops=dict(arrowstyle='->', color=INK, lw=0.9))
ax.text(2.5,4.0,'Fe₂O₃ + 3CO → 2Fe + 3CO₂\n(about 700 °C)', ha='center', va='center', fontsize=5.8, color=INK)
ax.text(2.5,2.9,'CO₂ + C → 2CO', ha='center', va='center', fontsize=6.6, color=INK)
ax.text(2.5,2.15,'C + O₂ → CO₂\n(about 1500 °C)', ha='center', va='center', fontsize=5.8, color=INK)
ax.text(2.5,1.2,'molten iron + slag', ha='center', va='center', fontsize=6.6, color='white', weight='bold')
ax.annotate('hot air blast', xy=(1.1,1.9), xytext=(-1.0,2.3), fontsize=7, color=INK, va='center', arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.6))
ax.annotate('hot air blast', xy=(3.9,1.9), xytext=(5.0,2.3), fontsize=7, color=INK, va='center', arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.6))
ax.annotate('molten slag (tapped)', xy=(3.9,1.0), xytext=(5.0,1.0), fontsize=7, color=INK, va='center', arrowprops=dict(arrowstyle='->', color=INK, lw=0.9))
ax.annotate('molten iron (tapped)', xy=(1.2,0.85), xytext=(-1.0,0.4), fontsize=7, color=INK, va='center', arrowprops=dict(arrowstyle='->', color=INK, lw=0.9))
ax.set_xlim(-1.2, 7.4); ax.set_ylim(0, 6.2); ax.axis('off')
```

### Extraction of aluminium (Hall-Heroult electrolysis)

Bauxite is purified to pure alumina (Al₂O₃). Alumina has a very high melting point (2050 °C), so it is dissolved in molten **cryolite** (Na₃AlF₆) at about 950 °C, which lowers the melting point and improves conduction. The mixture is electrolysed in a steel tank lined with carbon (the cathode) using carbon anodes.

- At the cathode: Al³⁺ + 3e⁻ → Al (molten aluminium collects at the bottom)
- At the anode: 2O²⁻ → O₂ + 4e⁻; the oxygen burns away the carbon anodes (CO₂ forms), so the anodes need replacing.

Overall: 2Al₂O₃ → 4Al + 3O₂

### Uses of some metals

| Metal | Uses |
|---|---|
| Iron | machines, buildings, vehicles (as steel) |
| Aluminium | cooking vessels, foil, aircraft, power cables |
| Copper | electric wires, coins, utensils |
| Zinc | galvanising iron, dry cells |
| Gold, silver | ornaments, coins, electronics |

## 17.4 Corrosion

**Corrosion** is the slow destruction of a metal by the action of air, moisture or chemicals in its surroundings.

```photo id="sci10/rust" caption="Rust on iron: the reddish-brown flaky layer forms when iron is in contact with moist air." width="70"
```

| Metal | Corrosion product |
|---|---|
| Iron | **rust**, reddish-brown Fe₂O₃·xH₂O |
| Copper | green coating of basic copper carbonate |
| Silver | black silver sulphide, Ag₂S (tarnishing) |
| Aluminium | thin, tough Al₂O₃ layer that **protects** the metal underneath |

### Rusting of iron

Rusting needs **both oxygen (air) and water (moisture)**. Experiment: three test tubes with nails: (A) nail in water open to air: rusts; (B) nail in boiled (air-free) water with a layer of oil: no rust; (C) nail in dry air with anhydrous calcium chloride: no rust. Only tube A has both air and water.

Overall: 4Fe + 3O₂ + 2xH₂O → 2Fe₂O₃·xH₂O (rust)

Rust is flaky and falls off, exposing new iron, so rusting goes on until the whole piece is eaten away. Salt water, acid rain and a warm humid climate speed up rusting.

### Prevention of corrosion

| Method | How it works |
|---|---|
| Painting, oiling or greasing | keeps air and water from the metal (gates, machines, bicycle chains) |
| **Galvanisation** | coating iron with a thin layer of zinc (roofing sheets, buckets); zinc protects even if scratched, because zinc is more reactive and corrodes first |
| Electroplating | coating with a thin layer of nickel, chromium, tin or silver |
| Alloying | stainless steel (Fe + Cr + Ni) does not rust |
| Tin plating | tin cans for food |
| Sacrificial protection | blocks of Mg or Zn bolted on the hull of ships |

::: caution Rusting is not "burning"
Students often say that iron rusts because it reacts with oxygen alone. Dry air does not rust iron. **Water must be present as well.** And aluminium forms an oxide layer too, but that layer is a **protective** coat, not a flaky one.
:::

::: example Mass of iron from ore
**Problem.** Fe₂O₃ + 3CO → 2Fe + 3CO₂. How much iron is obtained from 160 kg of Fe₂O₃? (Fe = 56, O = 16.)

**Solution.** Molar mass of Fe₂O₃ = 2 × 56 + 3 × 16 = 112 + 48 = 160. Two atoms of Fe weigh 2 × 56 = 112. So 160 kg of Fe₂O₃ gives **112 kg** of iron.
:::

::: example Percentage of metal in an ore
**Problem.** Find the percentage of aluminium in alumina, Al₂O₃. (Al = 27, O = 16.)

**Solution.** Molar mass of Al₂O₃ = 2 × 27 + 3 × 16 = 54 + 48 = 102. Percentage of Al = (54 / 102) × 100 = **52.9 %**.
:::

## Chapter summary

- Metals are lustrous, malleable, ductile and conduct heat and electricity; non-metals are dull, brittle and poor conductors (graphite and diamond are exceptions).
- Metal oxides are basic; non-metal oxides are acidic; Al₂O₃ and ZnO are amphoteric.
- Reactivity series: K, Na, Ca, Mg, Al, Zn, Fe, Pb, H, Cu, Hg, Ag, Au. A more reactive metal displaces a less reactive one; only metals above H liberate H₂ from dilute acids.
- Ores of Fe: haematite and magnetite; Al: bauxite; Cu: copper pyrite.
- Steps: crushing, concentration, calcination/roasting, reduction, refining. Reactive metals are extracted by electrolysis; middle metals by carbon reduction.
- Iron is made in a blast furnace from haematite, coke and limestone; Al is extracted by electrolysis of alumina in cryolite.
- Rusting needs oxygen and water; prevent it by painting, galvanising, plating and alloying.

## Practice questions

**Group A — Objective questions (1 mark each)**

1. The only liquid metal at room temperature is <span class="marks">[1]</span>
   (a) sodium (b) mercury (c) bromine (d) gallium
2. The most reactive metal among the following is <span class="marks">[1]</span>
   (a) Zn (b) Cu (c) Mg (d) Fe
3. The chief ore of aluminium is <span class="marks">[1]</span>
   (a) haematite (b) bauxite (c) galena (d) zinc blende
4. Galvanisation is the coating of iron with <span class="marks">[1]</span>
   (a) tin (b) copper (c) zinc (d) nickel
5. Which of the following metals does not react with dilute HCl? <span class="marks">[1]</span>
   (a) Mg (b) Zn (c) Cu (d) Fe
6. The slag in a blast furnace is <span class="marks">[1]</span>
   (a) CaCO₃ (b) CaSiO₃ (c) SiO₂ (d) CaO

::: note Answers to Group A
**1.** (b) — mercury.
**2.** (c) — Mg is highest.
**3.** (b) — bauxite, Al₂O₃·2H₂O.
**4.** (c) — zinc.
**5.** (c) — Cu is below hydrogen.
**6.** (b) — CaO + SiO₂ → CaSiO₃.
:::

**Group B — Short answer (2 marks each)**

1. Differentiate between a mineral and an ore. <span class="marks">[2]</span>
2. Why are sodium and potassium kept under kerosene? <span class="marks">[2]</span>
3. Write the balanced equation for the reaction of zinc with dilute sulphuric acid and name the gas formed. <span class="marks">[2]</span>
4. Why does aluminium not corrode easily even though it is reactive? <span class="marks">[2]</span>
5. Write two differences between metals and non-metals. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** A mineral is any natural substance that contains a metal compound; an ore is a mineral from which the metal can be extracted profitably.
**2.** They react violently with oxygen and moisture of the air; kerosene keeps them away from both.
**3.** Zn + H₂SO₄ → ZnSO₄ + H₂ ↑; hydrogen.
**4.** Aluminium forms a thin, strong layer of Al₂O₃ on its surface that protects the metal beneath.
**5.** Metals are good conductors, malleable and ductile; non-metals are poor conductors and brittle.
:::

**Group C — Long answer (4 marks each)**

1. Describe the extraction of iron from haematite in a blast furnace. Give the reactions. <span class="marks">[4]</span>
2. What is corrosion? Explain the conditions for rusting of iron and four methods of prevention. <span class="marks">[4]</span>
3. What is the reactivity series? Explain two of its uses with an example for each. <span class="marks">[4]</span>
4. Find the mass of aluminium obtainable from 204 kg of alumina (Al = 27, O = 16). <span class="marks">[4]</span>

::: note Answers to Group C
**1.** Charge: haematite, coke, limestone from the top; hot air from bottom. C + O₂ → CO₂; CO₂ + C → 2CO; Fe₂O₃ + 3CO → 2Fe + 3CO₂; CaCO₃ → CaO + CO₂; CaO + SiO₂ → CaSiO₃ (slag). Molten iron and slag are tapped from the bottom.
**2.** Corrosion: slow destruction of a metal by air, moisture or chemicals. Rusting needs oxygen and water together (nail experiment). Prevention: painting or oiling, galvanising with zinc, electroplating, alloying (stainless steel), sacrificial protection.
**3.** The reactivity series ranks metals by decreasing reactivity. (i) Displacement: Zn + CuSO₄ → ZnSO₄ + Cu. (ii) Reaction with acid: Mg and Zn give H₂ with dilute acids but Cu does not. (iii) It chooses the extraction method.
**4.** Molar mass of Al₂O₃ = 102; it contains 54 of aluminium. Mass of Al = (54 / 102) × 204 = 54 × 2 = **108 kg**.
:::
