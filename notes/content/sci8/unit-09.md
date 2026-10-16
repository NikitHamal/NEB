---
subject: Science and Technology
grade: 8
unit: 9
title: Matter
hours: 0
area: Science and Technology
---

Everything around you that has mass and takes up space is **matter**: the air
you breathe, the water you drink, the salt in the kitchen, the iron in the
plough. Matter is made of very small particles, and almost everything strange
about it — why a gas fills a room, why salt disappears in water, why a nail
rusts and a candle burns — comes from what those particles are doing.

::: key What this unit asks of you
You should be able to describe the three states of matter with the particle
idea, distinguish element, compound and mixture with examples, tell a physical
from a chemical change, explain solution, solute and solvent and what
"saturated" means, describe four methods of separating mixtures, classify
substances as acid, base or neutral using indicators and the pH scale, and
compare metals with non-metals.
:::

## 9.1 States of matter and the particle idea

Matter exists in three common states. What separates them is not what the
particles are but how they are arranged and how freely they move.

```figure caption="The same particles in three states. In a solid they are packed and only vibrate; in a liquid they slide over one another; in a gas they are far apart and move fast in every direction."
fig, ax = plt.subplots(figsize=(5.1, 2.6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5.4)
ax.axis("off")
import numpy as np
rng = np.random.default_rng(7)
names = ["Solid", "Liquid", "Gas"]
for k, name in enumerate(names):
    x0 = 0.6 + k * 3.2
    ax.add_patch(plt.Rectangle((x0, 1.4), 2.6, 2.4, fill=False, ec=GRID, lw=1.1))
    ax.text(x0 + 1.3, 4.25, name, ha="center", fontsize=7.6, color=INK)
    if k == 0:
        for i in range(5):
            for j in range(4):
                ax.add_patch(plt.Circle((x0 + 0.35 + i * 0.46, 1.75 + j * 0.5), 0.17,
                                        color=ACCENT, alpha=0.85))
    elif k == 1:
        pts = rng.uniform([x0 + 0.3, 1.7], [x0 + 2.3, 3.4], size=(14, 2))
        for px, py in pts:
            ax.add_patch(plt.Circle((px, py), 0.17, color=SERIES[1], alpha=0.85))
    else:
        pts = rng.uniform([x0 + 0.25, 1.6], [x0 + 2.35, 3.6], size=(7, 2))
        for px, py in pts:
            ax.add_patch(plt.Circle((px, py), 0.14, color=SERIES[2], alpha=0.85))
ax.text(2.0, 0.85, "fixed shape\\nfixed volume", ha="center", fontsize=6.2, color=INK)
ax.text(5.2, 0.85, "no fixed shape,\\nfixed volume", ha="center", fontsize=6.2, color=INK)
ax.text(8.4, 0.85, "no fixed shape,\\nno fixed volume", ha="center", fontsize=6.2, color=INK)
ax.text(5.0, 0.1, "heating gives the particles more energy: solid to liquid to gas",
        ha="center", fontsize=6.5, color=MUTED)
fig.tight_layout()
```

| | Solid | Liquid | Gas |
|---|---|---|---|
| Arrangement | closely packed, regular | close but irregular | far apart, random |
| Movement | vibrate in place | slide past one another | move fast in all directions |
| Shape | fixed | takes the shape of the container | fills the whole container |
| Volume | fixed | fixed | not fixed |
| Compressibility | almost none | very little | easily compressed |
| Diffusion | very slow | slow | fast |

**Change of state.** Melting (solid to liquid), freezing (liquid to solid),
evaporation and boiling (liquid to gas), condensation (gas to liquid) and
sublimation (solid straight to gas, as camphor and iodine do). During melting
and boiling the temperature stays constant even though heat is being supplied,
because the energy is being used to pull the particles apart rather than to
raise the temperature.

::: caution Evaporation and boiling are not the same
Evaporation happens at **any** temperature, only from the surface, and it cools
the remaining liquid — which is why water in a *gagri* stays cool and why you
feel cold when you come out of a bath. Boiling happens at one fixed temperature
for a given pressure (100 °C for water at sea level), throughout the liquid, with
bubbles. In the hills, water boils below 100 °C because the atmospheric pressure
is lower, which is why dal takes longer to cook in Jumla.
:::

## 9.2 Element, compound and mixture

| | Element | Compound | Mixture |
|---|---|---|---|
| Made of | one kind of atom only | two or more elements chemically joined | two or more substances not chemically joined |
| Can it be split? | not by chemical means | yes, into its elements | yes, by physical means |
| Composition | fixed (it is one substance) | fixed by mass | variable |
| Properties | its own | quite different from its elements | each part keeps its own properties |
| Examples | iron, oxygen, gold, hydrogen | water, salt, carbon dioxide, sugar | air, sea water, brass, soil, milk |

**Atom** is the smallest particle of an element that can take part in a chemical
reaction. **Molecule** is the smallest particle of a substance that can exist
freely; it may contain one atom (as in helium) or several (H₂O has three).
Copper, hydrogen and oxygen are written as symbols; water is H₂O and carbon
dioxide is CO₂.

```photo id="sci10/litmus" caption="Litmus paper tests. Blue turns red in acid; red turns blue in a base." width="64"
```

## 9.3 Physical and chemical change

| | Physical change | Chemical change |
|---|---|---|
| What happens | only the state, shape or size changes | a new substance with new properties is formed |
| Is it reversible? | usually yes | usually no |
| Energy | small amounts taken in or given out | usually a large amount given out or taken in |
| Examples | melting ice, dissolving sugar, breaking glass, magnetising iron | burning paper, rusting iron, souring milk, cooking rice, digestion |

::: tip The two-question test
**(1)** Is the substance after the change still the same substance — does it
still taste, look and behave the same? **(2)** Can I get the original back by a
simple physical method such as cooling, filtering or evaporating? If both
answers are yes, the change was physical.
:::

## 9.4 Solution

A **solution** is a mixture in which one substance is dissolved evenly in
another. The substance that dissolves is the **solute**; the one it dissolves in
is the **solvent**. In salt water, salt is the solute and water the solvent.

- A solution in which no more solute can be dissolved at that temperature is
  **saturated**. If more solute is added it sinks to the bottom.
- If a saturated solution is warmed it can usually dissolve more; on cooling,
  the extra solute comes out as crystals. This is how crystallisation purifies
  a substance.
- **Solubility** is the amount of a solute, in grams, that will dissolve in
  100 g of solvent at a given temperature.
- In a **suspension**, the solid particles are big enough to settle; in a
  **colloidal** mixture such as milk they do not settle but the mixture is not
  clear.

| Factor | Effect on how fast a solid dissolves |
|---|---|
| Temperature | warming speeds it up |
| Stirring | speeds it up |
| Size of particles | powder dissolves faster than lumps |
| Amount already dissolved | less will dissolve once saturated |

## 9.5 Separation of mixtures

Mixtures can be separated because their components differ in some physical
property — size, boiling point, solubility, magnetism or density.

| Method | Separates | Example |
|---|---|---|
| Hand picking | large visible pieces | stones from rice |
| Winnowing | lighter husk from heavier grain | paddy from husk |
| Sieving | different sizes of particle | flour from bran |
| Filtration | an insoluble solid from a liquid | sand from water, tea from tea leaves |
| Evaporation | a dissolved solid from its solvent | salt from salt water |
| Distillation | a liquid from a solution, keeping both | pure water from salt water |
| Sublimation | a substance that sublimes | camphor from sand |
| Crystallisation | a dissolved solid as pure crystals | sugar, alum, copper sulphate |
| Magnetic separation | iron from a mixture | iron filings from sulphur |
| Sedimentation and decantation | a heavy solid from a liquid | muddy water, after standing |
| Centrifuging | very fine suspended particles | cream from milk |
| Chromatography | dissolved colours | the dyes in a marker pen or in ink |

```figure caption="Two separating methods. In filtration the insoluble solid stays on the paper and the clear liquid passes through; in distillation the solution is boiled so that the solvent leaves as vapour and is collected back as pure liquid."
fig, ax = plt.subplots(figsize=(5.0, 2.8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis("off")
ax.add_patch(plt.Polygon([[0.8, 3.9], [1.0, 1.6], [2.6, 1.6], [2.8, 3.9]],
                         fill=False, ec=INK, lw=1.3))
ax.plot([0.8, 2.8], [2.9, 2.9], color=SERIES[1], lw=1.6)
ax.add_patch(plt.Polygon([[0.85, 2.85], [1.15, 1.65], [2.45, 1.65], [2.75, 2.85]],
                         fc=ACCENT, alpha=0.2, ec="none"))
ax.text(1.8, 4.25, "funnel + filter paper", ha="center", fontsize=6.4, color=INK)
ax.text(1.8, 1.0, "filtrate collected", ha="center", fontsize=6.2, color=ACCENT)
ax.text(1.8, 0.35, "filtration", ha="center", fontsize=6.8, color=INK)
ax.add_patch(plt.Polygon([[6.0, 3.6], [6.2, 1.6], [7.6, 1.6], [7.8, 3.6]],
                         fill=False, ec=INK, lw=1.3))
ax.add_patch(plt.Polygon([[6.05, 2.3], [6.15, 1.65], [7.65, 1.65], [7.75, 2.3]],
                         fc=ACCENT, alpha=0.2, ec="none"))
ax.plot([6.9, 6.9], [3.6, 4.8], color=INK, lw=1.2)
ax.plot([6.9, 9.0], [4.8, 4.8], color=INK, lw=1.2)
ax.plot([9.0, 9.0], [4.8, 3.4], color=INK, lw=1.2)
ax.add_patch(plt.Polygon([[8.4, 3.4], [8.6, 2.0], [9.4, 2.0], [9.6, 3.4]],
                         fill=False, ec=SERIES[2], lw=1.2))
ax.text(8.6, 1.5, "pure solvent", ha="center", fontsize=6.2, color=SERIES[2])
ax.text(7.5, 5.15, "condenser", ha="center", fontsize=6.3, color=INK)
ax.text(6.9, 0.35, "distillation", ha="center", fontsize=6.8, color=INK)
fig.tight_layout()
```

```photo id="sci10/malachite" caption="Malachite, a copper ore. Minerals are naturally occurring compounds, not mixtures." width="58"
```

## 9.6 Acids, bases and salts

**Acids** taste sour, turn blue litmus red and react with metals to give
hydrogen. **Bases** taste bitter and feel soapy; a base that dissolves in water
is an **alkali**. Alkalis turn red litmus blue. When an acid reacts with a base
they neutralise each other and form a **salt** and water:

$$\text{HCl}+\text{NaOH}\rightarrow\text{NaCl}+\text{H}_2\text{O}$$

| Indicator | In acid | In base (alkali) |
|---|---|---|
| Blue litmus | turns red | stays blue |
| Red litmus | stays red | turns blue |
| Methyl orange | red | yellow |
| Phenolphthalein | colourless | pink |
| Turmeric paper | unchanged | turns red |

The **pH scale** runs from 0 to 14. Below 7 is acidic, 7 is neutral and above 7
is basic.

```figure caption="The pH scale with everyday Nepali examples. Every step is a tenfold change in acidity, so a solution of pH 4 is ten times more acidic than one of pH 5."
fig, ax = plt.subplots(figsize=(5.1, 2.5))
ax.set_xlim(0, 14)
ax.set_ylim(0, 4)
ax.axis("off")
for i in range(14):
    c = plt.cm.RdYlGn_r(i / 13.0)
    ax.add_patch(plt.Rectangle((i, 1.7), 1.0, 0.8, color=c, alpha=0.75, ec="white", lw=0.6))
    ax.text(i + 0.5, 2.1, str(i + 1), ha="center", va="center", fontsize=6.3, color=INK)
ax.text(1.5, 3.4, "acidic", ha="center", fontsize=7.0, color="#b00020")
ax.text(7.0, 3.4, "neutral", ha="center", fontsize=7.0, color=INK)
ax.text(12.5, 3.4, "basic", ha="center", fontsize=7.0, color="#2f7d32")
notes = [(0.5, "lemon 2"), (2.5, "vinegar 3"), (5.0, "rain 6"), (7.5, "water 7"),
         (9.5, "soap 9"), (12.0, "lime 12")]
for x, t in notes:
    ax.text(x, 1.25, t, ha="center", fontsize=6.2, color=INK)
ax.text(7.0, 0.45, "litmus and pH paper tell you which side of 7 a substance lies on",
        ha="center", fontsize=6.4, color=MUTED)
fig.tight_layout()
```

::: caution Acid into water, never water into acid
Mixing a strong acid with water gives out a great deal of heat. If you pour
water into concentrated acid, the first few drops boil instantly and can spit
acid out of the vessel. Always pour the acid slowly down the side of a vessel of
water, stirring, and wear goggles.
:::

## 9.7 Metals and non-metals

| Property | Metals | Non-metals |
|---|---|---|
| Appearance | shiny (lustrous) | usually dull |
| Conductivity | good conductors of heat and electricity | poor, except graphite |
| Malleability and ductility | can be beaten into sheets and drawn into wires | brittle; not ductile |
| State at room temperature | mostly solid (mercury is liquid) | solid, liquid or gas |
| Sound | sonorous | not sonorous |
| Oxides | basic (metal oxide + water gives a base) | acidic or neutral |
| Examples | iron, copper, aluminium, zinc, gold | sulphur, carbon, oxygen, nitrogen, iodine |

Metals are used where strength or conductivity is needed. An **alloy** is a
mixture of a metal with another element, made to improve a property: brass is
copper and zinc, bronze is copper and tin, steel is iron with a little carbon,
stainless steel adds chromium, and solder is tin and lead. Alloys are usually
harder and more resistant to corrosion than the pure metal.

::: example Worked classification
**Problem.** Classify each of the following as an element, a compound or a
mixture, and say whether each is a metal or a non-metal where that applies:
(a) brass (b) water (c) graphite (d) air (e) copper.

**Solution.**
(a) Brass — a **mixture** of copper and zinc; it contains metals but brass
itself is not an element.
(b) Water — a **compound** of hydrogen and oxygen, H₂O; both are non-metals.
(c) Graphite — an **element**, a form of carbon, and a **non-metal** (the
exception that conducts electricity).
(d) Air — a **mixture** of nitrogen, oxygen, carbon dioxide, water vapour and
other gases.
(e) Copper — an **element** and a **metal**.

**The reasoning.** If the substance has one kind of atom, it is an element; if
two or more elements are chemically joined in a fixed ratio, it is a compound;
if the parts can be separated by a physical method, it is a mixture.
:::

::: example A crystallisation calculation
**Problem.** 40 g of a saturated solution of salt in water contains 8 g of
salt. Find the solubility of salt in water at that temperature.

**Solution.** The mass of water in the solution is
$40-8=32$ g. The solubility is the mass of salt that dissolves in 100 g of
water:

$$\text{solubility}=\frac{8}{32}\times100=25\ \text{g per 100 g of water}$$

**Answer.** 25 g per 100 g of water at that temperature.

**Check.** $32\times\frac{25}{100}=8$ g of salt in 32 g of water ✓, and
$8+32=40$ g of solution ✓.
:::

## Chapter summary

- Matter is anything with mass that occupies space; it is made of particles.
- **Solid**: fixed shape and volume, particles vibrate in place. **Liquid**:
  fixed volume, takes the shape of the container. **Gas**: neither fixed, easily
  compressed, diffuses fast.
- Changes of state: melting, freezing, evaporation, boiling, condensation,
  sublimation; temperature stays constant during melting and boiling.
- **Element** = one kind of atom; **compound** = elements chemically combined in
  a fixed ratio; **mixture** = substances not chemically combined.
- A **physical** change alters only state, shape or size and is usually
  reversible; a **chemical** change forms a new substance and is usually not.
- In a solution the **solute** dissolves in the **solvent**; a **saturated**
  solution holds as much solute as it can at that temperature.
- Mixtures are separated by hand picking, winnowing, sieving, filtration,
  evaporation, distillation, sublimation, crystallisation, magnetic separation
  and chromatography.
- Acids turn blue litmus red, bases turn red litmus blue; acid plus base gives
  a salt and water; the pH scale runs from 0 to 14.
- Metals are lustrous, malleable, ductile, sonorous and good conductors;
  non-metals are not, except graphite. Alloys are mixtures made to improve a
  property.

## Practice questions

**Group A — Objective (1 mark each)**

1. Which state of matter is easily compressible?
   <span class="marks">[1]</span>
   (a) solid (b) liquid (c) gas (d) none
2. Which of these is a compound? <span class="marks">[1]</span>
   (a) air (b) brass (c) water (d) sea water
3. Rusting of iron is a <span class="marks">[1]</span>
   (a) physical change (b) chemical change (c) change of state (d) reversible
   change
4. In salt water, the solvent is <span class="marks">[1]</span>
   (a) salt (b) water (c) both (d) neither
5. Which method separates a dissolved solid from its solvent, keeping the
   solvent? <span class="marks">[1]</span>
   (a) filtration (b) sieving (c) distillation (d) decantation
6. A solution of pH 3 is <span class="marks">[1]</span>
   (a) acidic (b) neutral (c) basic (d) alkaline

::: note Answers to Group A
**1.** (c) — the particles of a gas are far apart.
**2.** (c) — water is H₂O, a compound of hydrogen and oxygen.
**3.** (b) — a new substance, rust, is formed and the change is not easily
reversed.
**4.** (b) — water is the medium; salt is the solute.
**5.** (c) — distillation gives back pure solvent; evaporation would lose it.
**6.** (a) — pH below 7 is acidic.
:::

**Group B — Short answer (2 marks each)**

1. Give two differences between a solid and a gas, using the particle idea.
   <span class="marks">[2]</span>
2. Distinguish between a compound and a mixture with one example of each.
   <span class="marks">[2]</span>
3. What is a saturated solution? How can more solute be dissolved in it?
   <span class="marks">[2]</span>
4. Write any four differences between metals and non-metals.
   <span class="marks">[2]</span>

::: note Answers to Group B
**1.** In a solid the particles are closely packed and only vibrate about fixed
positions, so a solid has a fixed shape and volume and cannot be compressed; in
a gas the particles are far apart and move quickly in all directions, so a gas
has neither fixed shape nor fixed volume, fills its container, diffuses quickly
and can be compressed easily.
**2.** A compound is formed when two or more elements combine chemically in a
fixed ratio, and its properties differ from those of its elements — water, H₂O.
A mixture contains two or more substances that are not chemically combined, in
any proportion, and each part keeps its own properties — air, or brass.
**3.** A saturated solution is one that contains as much solute as it can
dissolve at that temperature; adding more solute leaves it undissolved at the
bottom. More can be dissolved by warming the solution, by adding more solvent,
or by grinding the solute finer and stirring.
**4.** Any four of: metals are lustrous, non-metals are dull; metals conduct
heat and electricity, non-metals generally do not (graphite excepted); metals
are malleable and ductile, non-metals are brittle; metals are usually sonorous;
metals are mostly solids at room temperature while non-metals may be solid,
liquid or gas; metal oxides are basic while non-metal oxides are acidic or
neutral.
:::

**Group C — Long answer (4 marks each)**

1. Describe with diagrams how you would separate a mixture of salt, sand and
   iron filings into its three parts. Name each method and say what property it
   uses. <span class="marks">[4]</span>
2. Explain, with examples, three differences between a physical change and a
   chemical change. Classify the burning of a candle as both: which part of it
   is physical and which is chemical? <span class="marks">[4]</span>

::: note Answers to Group C
**1.** **Step 1 — magnetic separation.** Draw a bar magnet through the mixture,
preferably wrapped in paper; the iron filings stick to it and are the first part
separated. Property used: iron is attracted by a magnet while sand and salt are
not. **Step 2 — dissolving and filtration.** Add water and stir; the salt
dissolves and the sand does not. Fold filter paper in a funnel, pour the mixture
in, and the sand stays on the paper while the salt solution passes through.
Property used: salt is soluble in water and sand is not, and the sand particles
are too large to pass through the paper. **Step 3 — evaporation or
crystallisation.** Heat the filtrate gently in a dish until the water has
evaporated and salt crystals are left. Property used: salt has a much higher
boiling point than water and does not evaporate with it.
**2.** **Three differences.** (i) In a physical change no new substance is
formed — melting ice gives water — while in a chemical change a new substance
with new properties is formed, as when iron rusts to give rust. (ii) A physical
change is usually reversible: water can be frozen back to ice. A chemical change
is usually not: rust cannot easily be turned back into iron. (iii) A physical
change involves small energy changes and no change in chemical composition; a
chemical change involves a large energy change and a change in composition.
**The candle.** The melting of the wax near the flame is **physical** — the wax
changes from solid to liquid and back as it cools, and no new substance is
formed. The burning of the wax vapour is **chemical** — it combines with oxygen
to give carbon dioxide, water vapour, soot and heat, and the wax cannot be
recovered.
:::

## Objective practice

**Choose the correct answer.** <span class="marks">[5×1=5]</span>

**1.** An atom with 11 protons and 12 neutrons has a mass number of
   (a) 11 (b) 12 (c) 23 (d) 1
**2.** Which of these is a compound?
   (a) air (b) water (c) brass (d) soil
**3.** A solution of pH 3 is
   (a) strongly basic (b) weakly basic (c) acidic (d) neutral
**4.** Sublimation is the change from
   (a) solid to liquid (b) liquid to gas (c) solid directly to gas (d) gas to liquid
**5.** Common salt is recovered from sea water by
   (a) filtration (b) evaporation (c) decantation (d) magnetic separation

::: note Objective practice — answers
**1.** (c) — $11 + 12 = 23$. **2.** (b) — a fixed 2:1 ratio, chemically bonded. **3.** (c) — pH below 7 is acidic. **4.** (c) — as in camphor. **5.** (b) — the water evaporates and leaves the salt.
:::
