---
subject: Science and Technology
grade: 10
unit: 9
title: Heat
hours: 0
area: Science and Technology
---

Heat is the form of energy that makes things hot. It cooks our dal-bhat, melts the snow on the Himalayas, makes the rails of a railway line expand in summer, and keeps us warm in a woollen jacket. In this unit you learn how solids, liquids and gases expand when heated, how much heat a substance needs to warm up, how heat is hidden when ice melts or water boils, and the three ways in which heat travels from place to place.

::: key What SEE asks from this unit
Definitions (heat, temperature, linear expansivity, specific heat capacity, latent heat), the formulae $Q = mc\Delta T$ and $Q = mL$, the principle of calorimetry (heat lost = heat gained), the anomalous expansion of water, the three modes of heat transfer with daily-life applications, and numericals.
:::

**Heat and temperature.**

**Heat** is the form of energy that flows from a hot body to a cold body because of a temperature difference. Its SI unit is the **joule (J)**. Another unit is the calorie: $1\ \text{cal} = 4.2\ \text{J}$.

**Temperature** tells how hot or cold a body is. It decides the direction of heat flow: heat always flows from the body at higher temperature to the body at lower temperature. It is measured in kelvin (K) or degree Celsius (°C).

| Heat | Temperature |
|---|---|
| A form of energy | A measure of hotness or coldness |
| Measured in joule | Measured in °C or kelvin |
| Measured by a calorimeter | Measured by a thermometer |
| Depends on mass, material and temperature change | Does not depend on mass |

A bucket of water at 40 °C has more heat than a cup of water at 40 °C, though both have the same temperature.

Temperature scales: $T(\text{K}) = t(°\text{C}) + 273$. Water freezes at 0 °C (273 K) and boils at 100 °C (373 K). A liquid-in-glass thermometer uses the expansion of mercury or alcohol with a fixed lower point (0 °C) and upper point (100 °C), divided into 100 equal parts.

## 9.1 Thermal expansion

::: definition Thermal expansion
The increase in the size (length, area or volume) of a substance when it is heated is called thermal expansion.
:::

When a solid is heated, its atoms vibrate more strongly and push each other slightly farther apart. So the whole body expands. When cooled, it contracts.

### Expansion of solids

A solid can expand in length (linear), in area (superficial) and in volume (cubical). For a rod, the change in length is

- directly proportional to the original length $L_0$,
- directly proportional to the rise in temperature $\Delta T$,
- different for different materials.

$$ \Delta L = \alpha\, L_0\, \Delta T \qquad\text{so}\qquad L = L_0\,(1 + \alpha\,\Delta T) $$

The constant $\alpha$ is the **coefficient of linear expansion**: the increase in length per unit original length per degree rise in temperature. Its unit is °C⁻¹ or K⁻¹.

| Material | $\alpha$ (per °C) |
|---|---|
| Steel / iron | $1.2\times10^{-5}$ |
| Copper | $1.7\times10^{-5}$ |
| Aluminium | $2.3\times10^{-5}$ |
| Brass | $1.9\times10^{-5}$ |
| Glass (ordinary) | $0.9\times10^{-5}$ |
| Invar (Fe-Ni alloy) | $0.1\times10^{-5}$ |

::: example Expansion of a rail
**Problem.** A steel rail is 30 m long at 10 °C. By how much does it expand when the temperature rises to 50 °C? ($\alpha = 1.2\times10^{-5}\ °\text{C}^{-1}$.)

**Solution.** $\Delta T = 50 - 10 = 40$ °C.

$\Delta L = \alpha L_0 \Delta T = 1.2\times10^{-5} \times 30 \times 40 = 1.44\times10^{-2}$ m $= 1.44$ cm.

This is why small gaps are left between rails. Without gaps the rails would bend (buckle).
:::

### Applications and nuisances of expansion of solids

- Gaps are left between railway rails, and between slabs of a concrete bridge or road.
- One end of a long iron bridge rests on rollers so that it can expand freely.
- Telephone and power lines are hung loosely; in summer they sag more and in winter they are tighter.
- A tight metal lid of a glass jar can be loosened by dipping it in hot water, since the metal expands more than the glass.
- An iron rim is heated before being fitted on a wooden cart wheel; on cooling it contracts and grips tightly.
- Riveting of steel plates is done with red-hot rivets.
- **Bimetallic strip.** Two strips of different metals (brass and iron) are riveted together. On heating, brass expands more than iron, so the strip bends with the brass on the outside of the curve. It is used in electric irons, heaters and fire alarms as a thermostat: when the temperature gets too high the strip bends and breaks the circuit.

```figure caption="A bimetallic strip. Brass expands more than iron, so on heating the strip bends toward the iron side. At the right, the bending strip breaks a thermostat contact."
import numpy as np, matplotlib.pyplot as plt
fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.0, 2.4))
for ax in (a1, a2):
    ax.set_xlim(0, 10); ax.set_ylim(-3.5, 3.5); ax.axis('off')
a1.set_title('Cold: straight', fontsize=9, color=INK)
a1.fill_between([1, 9], [0, 0], [0.5, 0.5], color='#C9A227', ec=INK)
a1.fill_between([1, 9], [-0.5, -0.5], [0, 0], color='#8E8E93', ec=INK)
a1.text(5, 1.0, 'brass', ha='center', fontsize=8.5, color=INK)
a1.text(5, -1.4, 'iron', ha='center', fontsize=8.5, color=INK)
a2.set_title('Hot: bends', fontsize=9, color=INK)
x = np.linspace(1, 9, 60)
yc = -0.04*(x-1)*(9-x)*(-1)
yc = -0.05*(x-1)**2
a2.fill_between(x, yc, yc+0.5, color='#C9A227', ec=INK)
a2.fill_between(x, yc-0.5, yc, color='#8E8E93', ec=INK)
a2.set_ylim(-4.6, 2.6)
a2.text(4.5, 1.0, 'brass (outer, longer)', ha='center', fontsize=8.5, color=INK)
a2.text(3.0, -1.9, 'iron', ha='center', fontsize=8.5, color=INK)
fig.tight_layout()
```

### Expansion of liquids

Liquids expand much more than solids for the same rise in temperature. They have no shape of their own, so we study only their **volume expansion**. This is the principle of the thermometer: mercury in the bulb expands and rises in the thin tube.

A liquid in a container is heated: at first, the level of the liquid in the container falls slightly (because the container expands first), and then rises (the liquid expands more than the container). The **real expansion** of a liquid is its apparent expansion plus the expansion of the container.

### Anomalous expansion of water

Most liquids expand steadily on heating. Water behaves in a special way between 0 °C and 4 °C. When water at 0 °C is heated, it **contracts** until it reaches 4 °C, and above 4 °C it expands as usual. So water has its **minimum volume and maximum density at 4 °C** (density 1000 kg m⁻³).

```figure caption="Density of water near its freezing point. The density is greatest at 4 degrees C. (Values are approximate and the vertical scale is greatly magnified.)"
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4, 2.7))
T = np.linspace(0, 10, 100)
rho = 999.97*(1 - 7.0e-6*(T-4)**2)
ax.plot(T, rho, color=ACCENT, lw=2)
ax.plot([4], [999.97], 'o', color='#A8271F', ms=5)
ax.annotate('maximum at 4 C', (4, 999.97), xytext=(5.3, 999.935), fontsize=8.5, color=INK,
            arrowprops=dict(arrowstyle='-', color=MUTED))
ax.set_xlabel('temperature (C)'); ax.set_ylabel('density (kg/m3)')
ax.set_ylim(999.65, 1000.02)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.5)
fig.tight_layout()
```

**Importance in nature.** In a cold country, the top water of a lake cools first. Water at 4 °C is densest, so it sinks to the bottom, and warmer water rises. When the whole lake is at 4 °C and the surface cools further to 0 °C, the colder water is lighter, stays on top and freezes into a layer of ice. Ice is a poor conductor of heat, so the water below stays liquid at about 4 °C. Fish and other aquatic animals survive under the ice in winter. If water behaved like other liquids, whole lakes would freeze from the bottom up, killing the life in them.

### Expansion of gases

Gases expand far more than solids and liquids. All gases expand by the same fraction for the same rise in temperature. At constant pressure, the volume of a gas increases by $\tfrac{1}{273}$ of its volume at 0 °C for every 1 °C rise (Charles' law, studied in the unit on gases). A balloon left in the hot sun may burst for this reason, and a hot-air balloon rises because heated air expands, becomes less dense, and floats.

::: caution Water contracts, ice expands
Between 0 °C and 4 °C water contracts on heating. But when water freezes into ice at 0 °C, it **expands** (about 9 %), so ice is less dense than water and floats. A sealed water bottle or pipe left in a freezer can burst for this reason.
:::

## 9.2 Specific heat capacity

Put a pan of water and a pan of the same mass of oil on identical stoves. The oil gets hot far faster. Different materials need different amounts of heat to rise by the same temperature.

### Heat capacity

::: definition Heat capacity
The heat capacity of a body is the amount of heat required to raise its temperature by 1 °C (or 1 K). Unit: J °C⁻¹ or J K⁻¹.
:::

Heat capacity depends on the mass and the material of the body.

### Specific heat capacity

::: definition Specific heat capacity
The specific heat capacity of a substance is the amount of heat required to raise the temperature of 1 kg of the substance by 1 °C (or 1 K). Unit: J kg⁻¹ °C⁻¹ (or J kg⁻¹ K⁻¹).
:::

If a mass $m$ of a substance with specific heat capacity $c$ is heated through a temperature change $\Delta T$, the heat absorbed (or given out) is

$$ Q = mc\,\Delta T = mc\,(T_2 - T_1) $$

Heat capacity $= mc$.

| Substance | $c$ (J kg⁻¹ °C⁻¹) |
|---|---|
| Water | 4200 |
| Ice | 2100 |
| Steam | 2000 |
| Aluminium | 900 |
| Iron | 450 |
| Copper | 390 |
| Lead | 130 |
| Mercury | 140 |

Water has a very high specific heat capacity. This has useful consequences:

- Water is used to cool car engines and as the hot-water bottle filler: it carries a lot of heat for a small rise in temperature.
- **Sea breeze.** In the day, land warms faster than the sea (lower $c$), so the air above the land rises and cooler air from the sea blows inland. At night the land cools faster and the wind blows from land to sea.
- Coastal areas have a milder climate than places far inland, since the sea warms and cools slowly.

::: example Heating water
**Problem.** How much heat is needed to raise the temperature of 2 kg of water from 20 °C to 70 °C? ($c = 4200$ J kg⁻¹ °C⁻¹.)

**Solution.** $Q = mc\Delta T = 2 \times 4200 \times (70-20) = 2 \times 4200 \times 50 = 420\,000$ J $= 420$ kJ.
:::

::: example Time taken by a heater
**Problem.** An electric heater of power 2000 W is used to heat 10 kg of water from 20 °C to 40 °C. How long does it take? Assume no heat is lost.

**Solution.** Heat needed $Q = 10 \times 4200 \times 20 = 840\,000$ J.

Heat given per second $= 2000$ J. Time $t = \dfrac{Q}{P} = \dfrac{840\,000}{2000} = 420$ s $= 7$ minutes.
:::

### Principle of calorimetry (method of mixtures)

When a hot body is mixed with a cold body in an insulated container and no heat is lost to the surroundings,

$$ \text{heat lost by the hot body} = \text{heat gained by the cold body} $$

This is based on the law of conservation of energy. The final temperature lies between the two initial temperatures.

::: example Mixing hot and cold water
**Problem.** 200 g of water at 80 °C is mixed with 300 g of water at 20 °C. Find the final temperature of the mixture.

**Solution.** Let the final temperature be $T$. Both are water, so $c$ cancels.

Heat lost $= 0.2 \times c \times (80 - T)$; heat gained $= 0.3 \times c \times (T - 20)$.

$0.2(80 - T) = 0.3(T - 20)$

$16 - 0.2T = 0.3T - 6$

$22 = 0.5T$, so $T = 44$ °C.
:::

::: example Specific heat of a metal
**Problem.** A 0.5 kg metal piece heated to 100 °C is dropped into 1 kg of water at 20 °C. The final temperature is 25 °C. Find the specific heat capacity of the metal (neglect heat taken by the container).

**Solution.** Heat lost by metal $= 0.5 \times c \times (100 - 25) = 37.5\,c$.

Heat gained by water $= 1 \times 4200 \times (25 - 20) = 21\,000$ J.

Equate: $37.5\,c = 21\,000$, so $c = 560$ J kg⁻¹ °C⁻¹.
:::

## 9.3 Latent heat

When ice at 0 °C is heated, its temperature does not rise while it melts. When water boils at 100 °C, the temperature stays at 100 °C until all the water has turned to steam. The heat supplied during a change of state does not raise the temperature; it breaks the attractions between molecules. It is hidden, so it is called **latent heat** ("latent" means hidden).

::: definition Specific latent heat
The specific latent heat of a substance is the amount of heat required to change 1 kg of the substance from one state to another at constant temperature.
:::

$$ Q = mL $$

- **Specific latent heat of fusion** ($L_f$): heat needed to change 1 kg of solid to liquid at its melting point. For ice, $L_f = 3.36\times10^{5}$ J kg⁻¹ (336 kJ kg⁻¹).
- **Specific latent heat of vaporisation** ($L_v$): heat needed to change 1 kg of liquid to vapour at its boiling point. For water, $L_v = 2.26\times10^{6}$ J kg⁻¹ (2260 kJ kg⁻¹).

The same heat is given out when the changes are reversed (freezing, condensation).

```figure caption="Heating curve for 0.1 kg of ice at -10 degrees C changed to steam at 100 degrees C. The flat parts are melting and boiling, where heat goes into latent heat and the temperature does not rise."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8, 2.8))
Q = [0, 2.1, 35.7, 77.7, 303.7, 307.7]
T = [-10, 0, 0, 100, 100, 120]
ax.plot(Q, T, color=ACCENT, lw=2, marker='o', ms=3.5)
ax.set_xlabel('heat supplied (kJ)'); ax.set_ylabel('temperature (C)')
ax.text(5, 8, 'ice', fontsize=8.5, color=INK)
ax.text(10, -9, 'melting (ice + water)', fontsize=8.5, color=INK)
ax.text(88, 30, 'water heats up', fontsize=8.5, color=INK, rotation=0)
ax.text(135, 108, 'boiling (water + steam)', fontsize=8.5, color=INK)
ax.set_ylim(-20, 135)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.5)
fig.tight_layout()
```

Why steam burns more than boiling water: steam at 100 °C carries the extra latent heat (2.26 MJ per kg) which it gives out when it condenses on the skin, in addition to the heat from cooling.

Daily-life uses: cooling a drink with ice (ice absorbs 336 kJ per kg while melting), the cooling effect of sweat evaporating from the skin, a refrigerator working by evaporation of a refrigerant, and steam used to heat or sterilise.

::: example Melting ice
**Problem.** How much heat is required to change 500 g of ice at 0 °C into water at 0 °C? ($L_f = 3.36\times10^5$ J kg⁻¹.)

**Solution.** $Q = mL_f = 0.5 \times 3.36\times10^5 = 1.68\times10^5$ J $= 168$ kJ.
:::

::: example From ice to steam
**Problem.** Find the total heat needed to change 100 g of ice at 0 °C into steam at 100 °C. ($c_w = 4200$ J kg⁻¹ °C⁻¹, $L_f = 3.36\times10^5$ J kg⁻¹, $L_v = 2.26\times10^6$ J kg⁻¹.)

**Solution.** Mass $= 0.1$ kg.

Step 1, melt the ice: $Q_1 = 0.1 \times 3.36\times10^5 = 33\,600$ J.

Step 2, warm water from 0 °C to 100 °C: $Q_2 = 0.1 \times 4200 \times 100 = 42\,000$ J.

Step 3, boil the water: $Q_3 = 0.1 \times 2.26\times10^6 = 226\,000$ J.

Total $Q = 33\,600 + 42\,000 + 226\,000 = 301\,600$ J $\approx 3.02\times10^5$ J.
:::

## 9.4 Heat transfer

Heat moves from one place to another in three ways: conduction, convection and radiation.

### Conduction

::: definition Conduction
Conduction is the transfer of heat through a solid from the hotter part to the colder part, from molecule to molecule, without the movement of the molecules from their places.
:::

When one end of an iron rod is held in a flame, the other end soon becomes hot. The molecules at the hot end vibrate more and pass their energy to the neighbouring molecules.

- **Good conductors** (metals: silver, copper, aluminium, iron) allow heat to pass easily. Cooking utensils are made of metal.
- **Bad conductors** or insulators (wood, plastic, air, wool, glass, water) do not. Handles of pans are wood or plastic; woollen clothes trap air and keep us warm; double walls and cork keep a house warm.
- Metals feel colder than wood in winter because they conduct heat away from the hand faster.
- Liquids and gases are poor conductors.

### Convection

::: definition Convection
Convection is the transfer of heat in liquids and gases by the actual movement of the heated particles of the fluid from one place to another.
:::

When a fluid is heated from below, the lower part expands, becomes less dense and rises. The cooler, denser fluid from above sinks to take its place. This circular flow is called a **convection current**.

- **Heating water in a beaker** with a crystal of potassium permanganate at the bottom shows the coloured streams rising in the middle and falling on the sides.
- **Sea and land breezes** and monsoon winds are large-scale convection currents.
- A room heater is placed near the floor and a ventilator near the roof: warm air rises and goes out, fresh air comes in.
- A chimney draws smoke up. A refrigerator's freezer is placed at the top so that cold air sinks and cools the whole.
- Hot-air balloons and the formation of clouds depend on convection.

### Radiation

::: definition Radiation
Radiation is the transfer of heat from a hot body to the surroundings in the form of electromagnetic waves (infrared), without needing any material medium.
:::

The heat of the Sun reaches the Earth through the empty space. A person sitting near a fire feels warm even though air is a poor conductor and the hot air rises. Radiation travels at the speed of light, 3×10⁸ m s⁻¹.

| Surface | Absorbs heat | Emits heat | Reflects heat |
|---|---|---|---|
| Dull black | Good | Good | Poor |
| Bright white / shiny | Poor | Poor | Good |

Applications: we wear white or light clothes in summer; solar cookers and solar water heaters have black absorbing surfaces; the radiator of a car is painted black to lose heat quickly; kettles and fire-fighters' suits are shiny.

| | Conduction | Convection | Radiation |
|---|---|---|---|
| Medium needed | Solid | Liquid or gas | None |
| How heat moves | Vibration passes along | Particles move | Electromagnetic waves |
| Speed | Slow | Slow | Very fast (speed of light) |
| Example | Iron rod heated at one end | Sea breeze | Sunlight reaching the Earth |

### The thermos (vacuum) flask

A thermos flask keeps hot things hot and cold things cold by reducing all three methods of heat transfer.

```figure caption="Section of a thermos flask. The vacuum between the double glass walls stops conduction and convection; the silvered surfaces reduce radiation."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(4.4, 3.2))
ax.set_xlim(0, 11); ax.set_ylim(0, 8.2); ax.axis('off')
ax.add_patch(Rectangle((2.5, 1.0), 3.4, 6.0, fc='white', ec=INK, lw=2.2))
ax.add_patch(Rectangle((3.1, 1.6), 2.2, 5.4, fc='white', ec=INK, lw=2.2))
ax.add_patch(Rectangle((3.15, 1.65), 2.1, 3.4, fc='#FFD9A8', ec='none'))
ax.add_patch(Rectangle((2.5, 0.4), 3.4, 0.6, fc='#BBBBBB', ec=INK))
ax.add_patch(Rectangle((3.3, 7.0), 1.8, 0.7, fc='#8B6B3E', ec=INK))
ax.text(4.2, 3.3, 'hot\nliquid', ha='center', fontsize=8.5, color=INK)
ax.annotate('vacuum', (2.8, 4.5), xytext=(6.7, 5.7), fontsize=8.5, color=INK, arrowprops=dict(arrowstyle='-', color=MUTED))
ax.annotate('silvered walls', (3.1, 3.0), xytext=(6.7, 3.6), fontsize=8.5, color=INK, arrowprops=dict(arrowstyle='-', color=MUTED))
ax.annotate('cork stopper', (5.1, 7.35), xytext=(6.7, 7.4), fontsize=8.5, color=INK, arrowprops=dict(arrowstyle='-', color=MUTED))
ax.annotate('cork support', (4.2, 0.7), xytext=(6.7, 1.0), fontsize=8.5, color=INK, arrowprops=dict(arrowstyle='-', color=MUTED))
```

| Part | Job |
|---|---|
| Double-walled glass with vacuum between | No conduction or convection across the gap |
| Silvered (shiny) walls | Reflects radiation back inside and reduces radiation loss |
| Cork stopper and support | Cork is a bad conductor, so little heat escapes through them |

::: caution Heat does not "rise"
Hot air rises, but heat is not a thing that rises. Heat moves from hot to cold in every direction by conduction and radiation. Only in fluids does the hot material itself move upward in convection.
:::

## Chapter summary

- Heat is energy (joule); temperature tells hotness. Heat flows from higher to lower temperature. $T(\text{K}) = t(°\text{C}) + 273$.
- Linear expansion: $\Delta L = \alpha L_0 \Delta T$. Bimetallic strips, rail gaps and tyre-fitting use expansion.
- Water contracts from 0 °C to 4 °C and has maximum density at 4 °C; this saves aquatic life in frozen lakes.
- Specific heat capacity $c$: heat to raise 1 kg by 1 °C; $Q = mc\Delta T$ (water $c = 4200$ J kg⁻¹ °C⁻¹). Heat lost = heat gained in mixing.
- Latent heat: $Q = mL$ with no change in temperature. $L_f$(ice) $= 3.36\times10^5$ J kg⁻¹, $L_v$(water) $= 2.26\times10^6$ J kg⁻¹.
- Conduction (solids, particles vibrate), convection (fluids, particles move), radiation (waves, no medium needed).
- Dull black surfaces absorb and emit heat well; shiny surfaces reflect heat. A thermos flask reduces all three modes.

## Practice questions

**Group A — Objective (1 mark each)**

1. At which temperature does water have the maximum density? <span class="marks">[1]</span>
   (a) 0 °C (b) 4 °C (c) 10 °C (d) 100 °C
2. The SI unit of specific heat capacity is <span class="marks">[1]</span>
   (a) J kg⁻¹ (b) J °C⁻¹ (c) J kg⁻¹ K⁻¹ (d) W
3. Heat from the Sun reaches the Earth by <span class="marks">[1]</span>
   (a) conduction (b) convection (c) radiation (d) all of these
4. During melting of ice at 0 °C, the temperature of the ice-water mixture <span class="marks">[1]</span>
   (a) rises (b) falls (c) remains constant (d) becomes 4 °C
5. Convection takes place in <span class="marks">[1]</span>
   (a) solids only (b) vacuum (c) liquids and gases (d) metals

::: note Answers to Group A
**1.** (b) — water's density is greatest at 4 °C.
**2.** (c) — $c = Q/(m\Delta T)$.
**3.** (c) — only radiation can cross empty space.
**4.** (c) — heat goes into latent heat, not into raising temperature.
**5.** (c) — fluids can flow and carry heat.
:::

**Group B — Short answer (2 marks each)**

1. Define specific heat capacity and state its SI unit. <span class="marks">[2]</span>
2. Why are gaps left between railway rails? <span class="marks">[2]</span>
3. Why does the sea breeze blow during the day? <span class="marks">[2]</span>
4. Why do we wear white clothes in summer? <span class="marks">[2]</span>
5. Why does a steam burn hurt more than a burn from boiling water at the same temperature? <span class="marks">[2]</span>

::: note Answers to Group B
**1.** It is the heat needed to raise the temperature of 1 kg of a substance by 1 °C (or 1 K). Unit: J kg⁻¹ K⁻¹.
**2.** Rails expand in hot weather. Gaps give room to expand freely; otherwise they would bend and damage the track.
**3.** Land has a lower specific heat capacity, so it gets hot faster than the sea. Air over the land rises and cool air from the sea moves in to take its place.
**4.** White surfaces reflect most of the heat and absorb little, so we stay cooler.
**5.** Steam at 100 °C gives out its latent heat of vaporisation (2.26×10⁶ J kg⁻¹) when it condenses on the skin, in addition to the heat from cooling, so it supplies much more heat.
:::

**Group C — Long answer (4 marks each)**

1. Explain the anomalous expansion of water and state its importance for aquatic life. <span class="marks">[4]</span>
2. How much heat is required to raise the temperature of 3 kg of copper from 25 °C to 75 °C? ($c = 390$ J kg⁻¹ °C⁻¹.) <span class="marks">[4]</span>
3. 400 g of water at 90 °C is added to 600 g of water at 30 °C. Find the final temperature. <span class="marks">[4]</span>
4. Calculate the heat needed to convert 2 kg of ice at 0 °C into water at 30 °C. ($L_f = 3.36\times10^5$ J kg⁻¹, $c_w = 4200$ J kg⁻¹ °C⁻¹.) <span class="marks">[4]</span>
5. Compare conduction, convection and radiation with an example of each. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** On heating from 0 °C to 4 °C water contracts; above 4 °C it expands. So its density is maximum at 4 °C. In a cold lake, 4 °C water sinks to the bottom and colder water stays on top and freezes. The ice layer insulates the water below, which stays at about 4 °C, so fish survive.
**2.** $Q = mc\Delta T = 3 \times 390 \times 50 = 58\,500$ J.
**3.** $0.4(90 - T) = 0.6(T - 30)$; $36 - 0.4T = 0.6T - 18$; $54 = T$. So $T = 54$ °C.
**4.** $Q_1 = mL_f = 2 \times 3.36\times10^5 = 6.72\times10^5$ J. $Q_2 = 2 \times 4200 \times 30 = 2.52\times10^5$ J. Total $= 9.24\times10^5$ J.
**5.** Use the comparison table: conduction in solids (iron rod), convection in fluids (sea breeze, boiling water), radiation without a medium (sunlight).
:::
