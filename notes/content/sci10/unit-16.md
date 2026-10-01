---
subject: Science and Technology
grade: 10
unit: 16
title: Gases
hours: 0
area: Science and Technology
---

We live at the bottom of an ocean of air. We cannot see most gases, yet they fill balloons, drive the engine of a bus, make soda fizzy and keep us alive. This chapter explains how gas particles behave, how the volume of a gas changes with pressure and temperature (the laws of Boyle and Charles), and how three important gases (hydrogen, oxygen and carbon dioxide) are made in the laboratory and used in daily life.

::: key What the SEE paper asks from this chapter
Expect: a statement of Boyle's or Charles' law (2 marks); a numerical on either law (4 marks, converting °C to kelvin is the main trap); the laboratory preparation of H₂, O₂ or CO₂ with equation and test (4 marks); and the uses of these gases (2 marks).
:::

## 16.1 Properties of gases

### The three states of matter

| Property | Solid | Liquid | Gas |
|---|---|---|---|
| Shape | fixed | takes shape of container | takes shape of container |
| Volume | fixed | fixed | fills the whole container |
| Particle spacing | very close | close | very far apart |
| Compressibility | almost none | very little | high |
| Particle motion | vibrate in place | slide past each other | move freely and fast |

### General properties of gases

- Gases have **no fixed shape and no fixed volume**. They fill every part of the container.
- Gases are **highly compressible**. Cooking gas (LPG) is squeezed into a small cylinder as a liquid.
- Gases **diffuse** quickly. The smell of cooking spreads through a house because the particles mix with air.
- Gases **exert pressure** on the walls of the container because their particles continually hit the walls.
- Gases have **low density** compared with solids and liquids.
- Gases **expand** on heating.

### Kinetic theory of gases (simple form)

1. A gas is made of tiny particles that are very far apart; most of the volume is empty space.
2. The particles move randomly and in straight lines at high speed.
3. They collide with each other and with the walls of the container. The collisions with the wall cause **pressure**.
4. The average kinetic energy of the particles increases with temperature.

### The three quantities that describe a gas

| Quantity | Symbol | Unit |
|---|---|---|
| Pressure | P | pascal (Pa); also atm, mm of Hg. 1 atm = 101 325 Pa = 760 mm Hg |
| Volume | V | m³, litre (L), cm³. 1 L = 1000 cm³ |
| Temperature | T | kelvin (K) |

Gas calculations must use the **absolute (Kelvin) temperature**:

$$ T(\text{K}) = t(^\circ\text{C}) + 273 $$

At 0 K (−273 °C), called **absolute zero**, the movement of particles would stop. It is the lowest possible temperature.

Standard temperature and pressure (**STP**) means 0 °C (273 K) and 1 atm (760 mm Hg).

## 16.2 Boyle's and Charles' laws

### Boyle's law

::: definition Boyle's law
At a constant temperature, the volume of a fixed mass of gas is **inversely proportional** to its pressure.
:::

$$ V \propto \frac{1}{P} \quad \Rightarrow \quad PV = \text{constant} \quad \Rightarrow \quad P_1V_1 = P_2V_2 $$

If the pressure is doubled, the volume is halved. This is why a bicycle pump gets harder to push as the air is compressed, and why air bubbles from a diver grow bigger as they rise (the pressure falls).

**Experimental idea.** Air is trapped in a closed tube above mercury (or oil). Extra pressure is applied and the volume is read each time. The product $P \times V$ is found to remain the same.

| P (atm) | V (L) | P × V |
|---|---|---|
| 1 | 12 | 12 |
| 2 | 6 | 12 |
| 3 | 4 | 12 |
| 4 | 3 | 12 |

### Charles' law

::: definition Charles' law
At a constant pressure, the volume of a fixed mass of gas is **directly proportional to its absolute (kelvin) temperature**.
:::

$$ V \propto T \quad \Rightarrow \quad \frac{V}{T} = \text{constant} \quad \Rightarrow \quad \frac{V_1}{T_1} = \frac{V_2}{T_2} $$

Charles found that for every 1 °C rise, the volume of a gas increases by 1/273 of its volume at 0 °C. A balloon left in the hot sun swells; one put in a fridge shrinks.

```figure caption="Boyle's law (left): V against P is a curve, V against 1/P is a straight line. Charles' law (right): V against T (kelvin) is a straight line through the origin."
fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.0,2.5))
P = np.linspace(0.8, 4.2, 100)
a1.plot(P, 12/P, color=ACCENT, lw=2)
a1.set_xlabel('P (atm)', fontsize=7.5, color=INK); a1.set_ylabel('V (L)', fontsize=7.5, color=INK)
a1.set_title('Boyle: T constant', fontsize=8, color=INK)
a1.text(2.4, 9, 'PV = constant', fontsize=7, color=MUTED)
T = np.linspace(0, 400, 50)
a2.plot(T, 0.05*T, color=SERIES[1], lw=2)
a2.set_xlabel('T (K)', fontsize=7.5, color=INK); a2.set_ylabel('V (L)', fontsize=7.5, color=INK)
a2.set_title('Charles: P constant', fontsize=8, color=INK)
a2.text(120, 17.5, 'V/T = constant', fontsize=7, color=MUTED)
a2.set_xlim(0, 420); a2.set_ylim(0, 22)
for a in (a1,a2):
    a.spines[['top','right']].set_visible(False); a.grid(color=GRID, lw=0.4); a.tick_params(labelsize=7)
fig.tight_layout()
```

::: caution Always convert to kelvin
In Charles' law, never put °C into the formula. If $V_1 = 300$ cm³ at 27 °C, then $T_1 = 27 + 273 = 300$ K. A gas at 0 °C does not have zero volume.
:::

::: example Boyle's law numerical
**Problem.** A gas occupies 600 cm³ at a pressure of 1 atm. What volume will it occupy at 3 atm if the temperature is constant?

**Solution.** $P_1V_1 = P_2V_2$, so $1 \times 600 = 3 \times V_2$. Therefore $V_2 = 600/3 = $ **200 cm³**.
:::

::: example Charles' law numerical
**Problem.** A balloon holds 2.0 L of air at 27 °C. It is placed in a water bath at 87 °C. Find the new volume at constant pressure.

**Solution.** $T_1 = 27 + 273 = 300$ K and $T_2 = 87 + 273 = 360$ K. $\dfrac{V_1}{T_1} = \dfrac{V_2}{T_2}$ gives $V_2 = \dfrac{2.0 \times 360}{300} = $ **2.4 L**.
:::

::: example Pressure of a compressed gas
**Problem.** 4 litres of hydrogen at a pressure of 750 mm Hg is compressed at constant temperature to 1.5 litres. Find the new pressure.

**Solution.** $P_1V_1 = P_2V_2$: $750 \times 4 = P_2 \times 1.5$, so $P_2 = 3000/1.5 = $ **2000 mm Hg**.
:::

::: example Volume at a lower temperature
**Problem.** A gas has a volume of 546 cm³ at 273 °C. At what temperature (in °C) will its volume be 273 cm³ at constant pressure?

**Solution.** $T_1 = 273 + 273 = 546$ K. $\dfrac{546}{546} = \dfrac{273}{T_2}$, so $T_2 = 273$ K. In °C: $273 - 273 = $ **0 °C**.
:::

### Combined gas equation

When pressure, volume and temperature all change, the two laws are joined:

$$ \frac{P_1V_1}{T_1} = \frac{P_2V_2}{T_2} $$

::: example Combined gas equation
**Problem.** A gas has volume 500 cm³ at 27 °C and 700 mm Hg. Find its volume at STP (0 °C, 760 mm Hg).

**Solution.** $T_1 = 300$ K, $T_2 = 273$ K. $V_2 = \dfrac{P_1V_1T_2}{T_1P_2} = \dfrac{700 \times 500 \times 273}{300 \times 760}$. The numerator is $700 \times 500 = 350000$; $350000 \times 273 = 95\,550\,000$. The denominator is $300 \times 760 = 228\,000$. $V_2 = 95\,550\,000 / 228\,000 = $ **419 cm³** (approximately).
:::

## 16.3 Preparation of hydrogen, oxygen and carbon dioxide

### Hydrogen (H₂)

**Laboratory preparation.** Granulated zinc is placed in a flask with a thistle funnel and a delivery tube. Dilute sulphuric acid (or hydrochloric acid) is added through the funnel. Hydrogen is collected by the **downward displacement of water**.

Zn + H₂SO₄ → ZnSO₄ + H₂ ↑

Zn + 2HCl → ZnCl₂ + H₂ ↑

| Property | Hydrogen |
|---|---|
| Physical | colourless, odourless, tasteless; lightest gas; slightly soluble in water |
| Chemical | burns with a pale blue flame to form water: 2H₂ + O₂ → 2H₂O; a neutral gas |
| Test | a burning splinter put at the mouth of the test tube gives a **"pop" sound** |

**Uses.** Fuel (rocket fuel, fuel cells); manufacture of ammonia (for fertiliser) and margarine (hardening of vegetable oil); filling balloons (earlier); oxy-hydrogen flame for welding.

::: caution Safety
Hydrogen forms an explosive mixture with air. Always test the gas for purity with a small flame before lighting the gas jet, and keep flames away from the generator.
:::

### Oxygen (O₂)

**Laboratory preparation.** Heat potassium chlorate (KClO₃) mixed with manganese dioxide (MnO₂, catalyst) in a hard glass test tube. Oxygen is collected by **downward displacement of water** (it is slightly soluble in water).

2KClO₃ --MnO₂, Δ--> 2KCl + 3O₂ ↑

Another method, without strong heating: add MnO₂ to hydrogen peroxide solution.

2H₂O₂ --MnO₂--> 2H₂O + O₂ ↑

| Property | Oxygen |
|---|---|
| Physical | colourless, odourless, tasteless, slightly soluble in water, slightly heavier than air; about 21 % of air |
| Chemical | supports burning but does not burn itself; reacts with metals and non-metals to form oxides: 2Mg + O₂ → 2MgO, C + O₂ → CO₂, S + O₂ → SO₂ |
| Test | a glowing splinter **relights** in the gas |

**Uses.** Respiration (in hospitals, mountain climbing, deep-sea diving); burning of fuels; oxy-acetylene welding and cutting; rocket fuel and steel making.

### Carbon dioxide (CO₂)

**Laboratory preparation.** Marble chips (calcium carbonate) are put in a flask and dilute hydrochloric acid is added through the thistle funnel. CO₂ is collected by **upward displacement of air** because it is heavier than air and fairly soluble in water.

CaCO₃ + 2HCl → CaCl₂ + H₂O + CO₂ ↑

Dilute H₂SO₄ is not used, because the calcium sulphate formed coats the marble and stops the reaction.

```figure caption="Laboratory preparation of hydrogen (left) by downward displacement of water, and carbon dioxide (right) by upward displacement of air."
from matplotlib.patches import Rectangle, Circle
fig, ax = plt.subplots(figsize=(5.0,3.0))
def flask(x0, label, solid):
    ax.add_patch(Circle((x0,1.2), 0.95, fc='#eaf2fb', ec=INK, lw=1.2, zorder=2))
    ax.add_patch(Rectangle((x0-0.2,2.0), 0.4, 1.3, fc='white', ec=INK, lw=1.2, zorder=1))
    ax.add_patch(Rectangle((x0-0.88,0.45), 1.76, 0.5, fc='#b9d7f2', ec='none', zorder=3))
    ax.text(x0, 0.2, solid, ha='center', fontsize=6.5, color=INK, zorder=4)
    ax.text(x0, 3.5, 'thistle funnel', fontsize=6.5, color=INK, ha='center')
    ax.text(x0+0.9, -0.7, label, ha='center', fontsize=7, color=INK, weight='bold')
flask(1.5, 'H₂SO₄ + zinc', 'zinc')
flask(7.0, 'HCl + marble chips', 'marble')
ax.plot([1.2,1.2,3.5],[2.7,2.9,2.9], color=INK, lw=1.3)
ax.plot([3.5,3.5],[2.9,0.5], color=INK, lw=1.3)
ax.add_patch(Rectangle((3.0,0.0), 1.2, 1.9, fc='#b9d7f2', ec=INK, lw=1.1, zorder=1))
ax.text(4.2, 3.3, 'gas jar full of water', ha='center', fontsize=6.3, color=INK)
ax.annotate('H₂ bubbles', xy=(3.5,0.9), xytext=(4.8,1.1), fontsize=6.6, color=INK, arrowprops=dict(arrowstyle='->', color=INK, lw=0.8))
ax.plot([6.7,6.7,8.6],[2.7,2.9,2.9], color=INK, lw=1.3)
ax.plot([8.6,8.6],[2.9,0.3], color=INK, lw=1.3)
ax.add_patch(Rectangle((8.2,0.0), 0.8, 1.9, fc='#f2f2f2', ec=INK, lw=1.1, zorder=1))
ax.text(9.3, 3.3, 'gas jar (upright)', ha='center', fontsize=6.3, color=INK)
ax.annotate('CO₂ settles\nat the bottom', xy=(8.6,0.4), xytext=(9.9,0.7), ha='left', fontsize=6.3, color=INK, arrowprops=dict(arrowstyle='->', color=INK, lw=0.8))
ax.set_xlim(-0.5, 11.5); ax.set_ylim(-1.0, 3.8); ax.set_aspect('equal'); ax.axis('off')
```

| Property | Carbon dioxide |
|---|---|
| Physical | colourless, faint sour taste, **heavier than air**, soluble in water (soda water) |
| Chemical | does not burn nor support burning; acidic oxide: CO₂ + H₂O ⇌ H₂CO₃ |
| Test | turns **lime water milky**: Ca(OH)₂ + CO₂ → CaCO₃ ↓ + H₂O; excess CO₂ clears it: CaCO₃ + H₂O + CO₂ → Ca(HCO₃)₂ |

**Uses.** Fire extinguishers (it smothers fire); soft drinks and soda water; dry ice (solid CO₂) for cooling and storing food; photosynthesis in plants; baking (with baking powder).

### Comparison of the three gases

| | Hydrogen | Oxygen | Carbon dioxide |
|---|---|---|---|
| Lab method | Zn + dil. H₂SO₄ | KClO₃ + MnO₂, heat | CaCO₃ + dil. HCl |
| Collection | downward displacement of water | downward displacement of water | upward displacement of air |
| Test | burning splinter, "pop" | glowing splinter relights | lime water turns milky |
| Burns? | burns | supports burning | extinguishes flame |
| Density vs air | lighter | slightly heavier | heavier |

::: tip Why the collection method differs
A gas that is **insoluble** in water is collected over water. A gas that is **heavier than air** and soluble is collected by **upward displacement of air** (the jar is kept upright). A gas lighter than air and soluble would be collected by downward displacement of air (the jar is inverted).
:::

::: example Volume of oxygen from a reaction
**Problem.** Heating 245 g of potassium chlorate gives 96 g of oxygen. Find the mass of potassium chloride formed, using the law of conservation of mass.

**Solution.** 2KClO₃ → 2KCl + 3O₂. Mass of reactant = 245 g. Mass of O₂ = 96 g. Mass of KCl = 245 − 96 = **149 g**.
:::

## Chapter summary

- Gas particles are far apart and move fast; gases have no fixed shape or volume, are compressible and exert pressure.
- Temperature in gas laws must be in kelvin: $T = t + 273$.
- **Boyle's law** (constant T): $P_1V_1 = P_2V_2$.
- **Charles' law** (constant P): $V_1/T_1 = V_2/T_2$.
- Combined: $\dfrac{P_1V_1}{T_1} = \dfrac{P_2V_2}{T_2}$; STP is 273 K and 760 mm Hg.
- H₂: Zn + dil. H₂SO₄; pop test. O₂: KClO₃ + MnO₂ heated; glowing splinter relights. CO₂: CaCO₃ + dil. HCl; lime water turns milky.
- Uses: H₂ as fuel and in ammonia; O₂ in respiration and welding; CO₂ in fire extinguishers and soft drinks.

## Practice questions

**Group A — Objective questions (1 mark each)**

1. The gas used in fire extinguishers is <span class="marks">[1]</span>
   (a) hydrogen (b) oxygen (c) carbon dioxide (d) nitrogen
2. 27 °C in kelvin is <span class="marks">[1]</span>
   (a) 246 K (b) 273 K (c) 300 K (d) 327 K
3. Which gas gives a "pop" sound with a burning splinter? <span class="marks">[1]</span>
   (a) oxygen (b) hydrogen (c) CO₂ (d) nitrogen
4. Boyle's law is stated at constant <span class="marks">[1]</span>
   (a) volume (b) pressure (c) temperature (d) mass of gas
5. In the preparation of oxygen from KClO₃, MnO₂ acts as <span class="marks">[1]</span>
   (a) a reactant (b) a catalyst (c) a product (d) a drying agent
6. A gas is collected by upward displacement of air if it is <span class="marks">[1]</span>
   (a) lighter than air (b) heavier than air and soluble (c) insoluble in water (d) coloured

::: note Answers to Group A
**1.** (c) — CO₂ does not support burning and is heavier than air.
**2.** (c) — 27 + 273 = 300.
**3.** (b) — hydrogen burns with a pop.
**4.** (c) — temperature is constant.
**5.** (b) — it speeds up the reaction and is unchanged.
**6.** (b) — like CO₂.
:::

**Group B — Short answer (2 marks each)**

1. State Boyle's law and write its mathematical form. <span class="marks">[2]</span>
2. Why is the Kelvin scale used in Charles' law? <span class="marks">[2]</span>
3. How is lime water used to test CO₂? Write the equation. <span class="marks">[2]</span>
4. Why is dilute sulphuric acid not used to prepare CO₂ from marble? <span class="marks">[2]</span>
5. A gas of volume 300 cm³ at 1 atm is compressed to 2 atm at constant temperature. Find the new volume. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** At constant temperature, the volume of a fixed mass of gas is inversely proportional to its pressure; $P_1V_1 = P_2V_2$.
**2.** The volume of a gas is proportional to the absolute temperature; the Kelvin scale starts from absolute zero, so that V/T is a constant.
**3.** Passing CO₂ through lime water makes it milky: Ca(OH)₂ + CO₂ → CaCO₃ ↓ + H₂O.
**4.** Calcium sulphate is slightly soluble and forms a coat on the marble that stops the acid reaching it.
**5.** $V_2 = P_1V_1/P_2 = (1 \times 300)/2 = $ **150 cm³**.
:::

**Group C — Long answer (4 marks each)**

1. Describe the laboratory preparation of oxygen. Give the equation, one test and two uses. <span class="marks">[4]</span>
2. A gas occupies 250 cm³ at 17 °C. At what temperature will it occupy 300 cm³ at constant pressure? <span class="marks">[4]</span>
3. Describe the laboratory preparation of hydrogen with a labelled diagram, equation and test. <span class="marks">[4]</span>
4. 500 cm³ of a gas at 27 °C and 760 mm Hg is heated to 127 °C and the pressure changed to 1520 mm Hg. Find the final volume. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** Heat KClO₃ with MnO₂ in a hard glass tube; collect over water. 2KClO₃ → 2KCl + 3O₂ ↑. A glowing splinter relights. Uses: respiration support, welding.
**2.** $T_1 = 17 + 273 = 290$ K. $T_2 = V_2T_1/V_1 = 300 \times 290/250 = 348$ K. In °C: 348 − 273 = **75 °C**.
**3.** Zinc granules and dilute H₂SO₄ in a flask with thistle funnel; gas collected over water. Zn + H₂SO₄ → ZnSO₄ + H₂ ↑. Test: burning splinter gives a pop. (Draw the diagram as in the chapter.)
**4.** $T_1 = 300$ K, $T_2 = 400$ K. $V_2 = \dfrac{P_1V_1T_2}{T_1P_2} = \dfrac{760 \times 500 \times 400}{300 \times 1520} = $ **333.3 cm³**.
:::
