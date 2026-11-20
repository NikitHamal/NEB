---
subject: Science and Technology
grade: 10
unit: 16
title: Gases
hours: 0
area: Science and Technology
---

Two gases play an outsized role in industry, agriculture and the Earth's atmosphere: **carbon dioxide ($\text{CO}_2$)**, an acidic oxide essential for photosynthesis, fire extinguishers and carbonated drinks, and **ammonia ($\text{NH}_3$)**, a pungent basic gas manufactured by **Haber's process** to produce nitrogenous fertilisers such as urea. This chapter covers the **laboratory preparation, collection, drying, tests, physical and chemical properties, and uses of $\text{CO}_2$ and $\text{NH}_3$**, together with the **greenhouse effect** and **acid rain**.

::: key What SEE asks from this chapter
Expect 4-mark diagram-based questions on the **laboratory preparation of $\text{CO}_2$** ($\text{CaCO}_3 + \text{dil. HCl}$, upward displacement of air) and **laboratory preparation of $\text{NH}_3$** ($2\text{NH}_4\text{Cl} + \text{Ca(OH)}_2 \xrightarrow{\Delta}$, inclined hard-glass test tube, quicklime $\text{CaO}$ drying tower, downward displacement of air), the **fountain experiment**, **Haber's process** ($450\text{–}500\ ^\circ\text{C}$, $200\text{–}900\ \text{atm}$, $\text{Fe}$ catalyst and $\text{Mo}$ promoter), **lime-water reactions** (short time vs long time), **burning magnesium in $\text{CO}_2$**, and 2-mark reasons on **greenhouse gases** and **acid rain**.
:::

## 16.1 Carbon dioxide gas: laboratory preparation, properties and uses

### Introduction and occurrence of Carbon Dioxide ($\text{CO}_2$)

- **Molecular formula:** $\text{CO}_2$ · **Relative molecular mass:** $12 + 2 \times 16 = 44$ · **Nature:** Acidic oxide.
- **Occurrence:** Present in atmospheric air at about $0.03\%$ (around $0.04\%$ today) by volume. Released during respiration, fermentation, combustion of carbon fuels, volcanic eruptions, and thermal decomposition of limestone ($\text{CaCO}_3 \xrightarrow{\Delta} \text{CaO} + \text{CO}_2 \uparrow$). Discovered by Van Helmont (1630) and studied by Joseph Black (1755).

### Laboratory preparation of Carbon Dioxide ($\text{CO}_2$)

- **Principle:** In the laboratory, carbon dioxide gas is prepared at room temperature by reacting **marble chips or limestone (calcium carbonate, $\text{CaCO}_3$)** with **dilute hydrochloric acid ($\text{HCl}$)**:

$$\text{CaCO}_3 + 2\text{HCl (dil.)} \longrightarrow \text{CaCl}_2 + \text{H}_2\text{O} + \text{CO}_2 \uparrow$$

```photo id="sci10/limestone" caption="Limestone (calcium carbonate, CaCO₃) is the mineral used as marble chips in the laboratory preparation of carbon dioxide and as raw material in lime kilns." width="58"
```

- **Apparatus and procedure:**
  1. Place a few pieces of marble chips ($\text{CaCO}_3$) inside a **Woulfe's bottle** (or flat-bottomed flask) fitted with a **thistle funnel** and a **delivery tube** through airtight corks.
  2. Ensure the **lower end of the thistle funnel dips below the acid level** (so generated $\text{CO}_2$ cannot escape out through the funnel) and the **end of the delivery tube stays well above the acid level**.
  3. Pour dilute $\text{HCl}$ through the thistle funnel until the marble chips are submerged. Effervescence begins immediately without heating.
  4. Collect the gas in an **upright gas jar by the upward displacement of air** because $\text{CO}_2$ is about **$1.5$ times heavier than air** and settles at the bottom of the jar, pushing lighter air upwards. (It is not collected over water because $\text{CO}_2$ dissolves in water to form carbonic acid.)
  5. If dry $\text{CO}_2$ is needed, pass the gas through concentrated $\text{H}_2\text{SO}_4$ or anhydrous $\text{CaCl}_2$ (never through quicklime $\text{CaO}$, which reacts with acidic $\text{CO}_2$).

::: caution Why dilute H₂SO₄ is NOT used with marble chips
Dilute sulphuric acid ($\text{H}_2\text{SO}_4$) is not used with $\text{CaCO}_3$ because the reaction forms **insoluble calcium sulphate ($\text{CaSO}_4$)**, which coats the surface of the marble chips as an impervious layer and **stops the reaction** after a few moments:
$\text{CaCO}_3 + \text{H}_2\text{SO}_4 \rightarrow \text{CaSO}_4 \downarrow + \text{H}_2\text{O} + \text{CO}_2 \uparrow$.
:::

```figure caption="Laboratory setups compared: (a) preparation of carbon dioxide (CaCO₃ + dil. HCl at room temperature, collected in an upright jar by upward displacement of air) and (b) preparation of ammonia (heating NH₄Cl + Ca(OH)₂ in a slightly inclined hard-glass tube, dried through a quicklime CaO tower and collected in an inverted jar by downward displacement of air)."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, FancyBboxPatch
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.2, 2.85))
ax1.set_xlim(0, 6); ax1.set_ylim(0, 5.2); ax1.axis("off")
ax1.set_title("(a) Lab preparation of CO₂", fontsize=8.2, fontweight="bold", color=INK)
ax1.add_patch(FancyBboxPatch((0.5, 0.5), 1.8, 1.9, boxstyle="round,pad=0.04,rounding_size=0.2", fc="#eaf2fb", ec=INK, lw=1.2))
ax1.add_patch(Rectangle((0.55, 0.55), 1.7, 0.75, fc="#b9d7f2", ec="none"))
ax1.text(1.4, 0.3, "CaCO₃ + dil. HCl", ha="center", fontsize=6.8, color=INK)
ax1.plot([1.0, 1.0], [0.75, 4.1], color=INK, lw=1.3)
ax1.add_patch(Polygon([[0.7, 4.5], [1.3, 4.5], [1.0, 4.1]], fc="#eaf2fb", ec=INK, lw=1.1))
ax1.text(1.0, 4.7, "Thistle funnel", ha="center", fontsize=6.6, color=INK)
ax1.plot([1.8, 1.8, 4.3, 4.3], [2.1, 3.3, 3.3, 0.8], color=INK, lw=1.3)
ax1.add_patch(Rectangle((3.8, 0.5), 1.1, 2.2, fc="#f6f8ff", ec=INK, lw=1.2))
ax1.text(4.35, 1.3, "CO₂\n(upright\ngas jar)", ha="center", fontsize=6.8, color=ACCENT, fontweight="bold")
ax1.text(4.35, 0.15, "Upward displacement of air", ha="center", fontsize=6.5, color=MUTED)

ax2.set_xlim(0, 6.6); ax2.set_ylim(0, 5.2); ax2.axis("off")
ax2.set_title("(b) Lab preparation of NH₃", fontsize=8.2, fontweight="bold", color=INK)
ax2.add_patch(Polygon([[0.4, 2.4], [2.4, 1.9], [2.5, 2.3], [0.5, 2.8]], fc="#fff3cd", ec=INK, lw=1.2))
ax2.text(1.4, 2.95, "NH₄Cl + Ca(OH)₂", ha="center", fontsize=6.6, color=INK)
ax2.add_patch(Polygon([[0.8, 1.2], [1.1, 1.2], [0.95, 1.9]], fc=SERIES[1], ec="none"))
ax2.text(0.95, 0.85, "Heat", ha="center", fontsize=6.6, color=SERIES[1])
ax2.plot([2.45, 3.8], [2.05, 1.5], color=INK, lw=1.3)
ax2.add_patch(Rectangle((3.5, 1.4), 1.0, 1.5, fc="#e8f4ea", ec=INK, lw=1.1))
ax2.text(4.0, 2.15, "CaO\n(lime\ntower)", ha="center", va="center", fontsize=6.4, color=INK)
ax2.plot([4.0, 4.0, 5.5, 5.5], [2.9, 3.2, 3.2, 4.4], color=INK, lw=1.3)
ax2.add_patch(Rectangle((5.0, 2.7), 1.1, 2.0, fc="#f6f8ff", ec=INK, lw=1.2))
ax2.text(5.55, 3.9, "NH₃\n(inverted\njar)", ha="center", fontsize=6.8, color=ACCENT, fontweight="bold")
ax2.text(4.7, 0.15, "Downward displacement of air", ha="center", fontsize=6.5, color=MUTED)
fig.tight_layout()
```

### Tests for Carbon Dioxide

1. **Moist blue litmus test:** Introducing moist blue litmus paper into the gas jar turns it **faint red**, showing $\text{CO}_2$ is an acidic gas.
2. **Burning splinter test:** A burning matchstick or splinter inserted into the mouth of the jar is **extinguished immediately**.
3. **Lime-water test:** Passing the gas through clear lime water ($\text{Ca(OH)}_2$) for a short time turns it **milky white** due to insoluble calcium carbonate ($\text{CaCO}_3$).

### Physical and Chemical Properties of Carbon Dioxide

- **Physical properties:** (1) Colourless and odourless gas with a faint acidic/sour taste; (2) about **$1.5$ times heavier than air**; (3) slightly soluble in water at ordinary pressure, and highly soluble under high pressure (forming **soda water / carbonated soft drinks**); (4) neither combustible nor a supporter of combustion; (5) when cooled below $-78\ ^\circ\text{C}$ under pressure, it solidifies directly into white solid $\text{CO}_2$ called **dry ice**.
- **Chemical properties:**
  1. **Dissolution in water:** Dissolves in water to form weak **carbonic acid**: $\text{CO}_2 + \text{H}_2\text{O} \rightleftharpoons \text{H}_2\text{CO}_3$.
  2. **Reaction with lime water (for a short time vs for a long time — very important for SEE):**
     - *Short time:* Turns lime water **milky** due to insoluble calcium carbonate:
       $$\text{Ca(OH)}_2 + \text{CO}_2 \longrightarrow \text{CaCO}_3 \downarrow \text{(milky white)} + \text{H}_2\text{O}$$
     - *Long time (excess $\text{CO}_2$):* The milkiness **disappears (becomes colourless)** because insoluble $\text{CaCO}_3$ converts into **soluble calcium bicarbonate**:
       $$\text{CaCO}_3 + \text{H}_2\text{O} + \text{CO}_2 \text{ (excess)} \longrightarrow \text{Ca(HCO}_3)_2 \text{ (soluble)}$$
  3. **Reaction with alkalis:** Neutralises caustic alkalis to form carbonates: $2\text{KOH} + \text{CO}_2 \rightarrow \text{K}_2\text{CO}_3 + \text{H}_2\text{O}$ and $2\text{NaOH} + \text{CO}_2 \rightarrow \text{Na}_2\text{CO}_3 + \text{H}_2\text{O}$.
  4. **Reaction with burning magnesium ribbon:** Although $\text{CO}_2$ extinguishes ordinary fires, a **burning magnesium ribbon continues to burn in $\text{CO}_2$** because intense heat splits $\text{CO}_2$ and magnesium strips oxygen from it, forming **white magnesium oxide ($\text{MgO}$)** powder and **black carbon ($\text{C}$)** specks on the tube wall:
     $$2\text{Mg} + \text{CO}_2 \xrightarrow{\Delta} 2\text{MgO (white)} + \text{C (black)}$$
  5. **Reaction with red-hot coke at $900\ ^\circ\text{C}$:** Reduced to poisonous carbon monoxide gas: $\text{CO}_2 + \text{C} \xrightarrow{900\ ^\circ\text{C}} 2\text{CO}$.
  6. **Photosynthesis in green plants:** Green plants combine $\text{CO}_2$ and water in the presence of sunlight and chlorophyll to synthesise glucose:
     $$6\text{CO}_2 + 6\text{H}_2\text{O} \xrightarrow[\text{chlorophyll}]{\text{sunlight}} \text{C}_6\text{H}_{12}\text{O}_6 + 6\text{O}_2 \uparrow$$
  7. **Reaction with ammonia (manufacture of urea):** At about $1500\ ^\circ\text{C}$ (or $180\text{–}200\ ^\circ\text{C}$ under high pressure), $\text{CO}_2$ reacts with $\text{NH}_3$ to produce **urea** fertiliser:
     $$2\text{NH}_3 + \text{CO}_2 \xrightarrow{\Delta,\ \text{pressure}} \text{NH}_2\text{CONH}_2 \text{ (urea)} + \text{H}_2\text{O}$$

```photo id="sci10/mg-burning" caption="Magnesium burns with a dazzling white flame, intense enough to continue burning even inside carbon dioxide gas, leaving white MgO ash and black carbon." width="52"
```

```photo id="sci10/co2-extinguisher" caption="A carbon dioxide fire extinguisher. Heavy, non-combustible CO₂ forms a blanket over the fire and cuts off the oxygen supply." width="46"
```

### Uses of Carbon Dioxide

1. Used in **fire extinguishers** (soda-acid and compressed $\text{CO}_2$ cylinders) because it is heavier than air and does not support combustion.
2. Dissolved under high pressure in **aerated soft drinks, soda water and beer** to give a sharp, fizzy taste.
3. Solid $\text{CO}_2$ (**dry ice**) is used as a refrigerant to preserve meat, fish, ice cream and vaccines without wetting them (it sublimes directly to gas).
4. Used by green plants for **photosynthesis** and in **carbogen** ($95\%\ \text{O}_2 + 5\%\ \text{CO}_2$) to stimulate breathing in pneumonia or carbon-monoxide poisoning patients.
5. Used industrially to manufacture **urea ($\text{NH}_2\text{CONH}_2$)**, **washing soda ($\text{Na}_2\text{CO}_3$)** and **baking soda ($\text{NaHCO}_3$)** by the Solvay process.

## 16.2 Ammonia gas: laboratory preparation, Haber's process, properties and uses

### Introduction to Ammonia ($\text{NH}_3$)

- **Molecular formula:** $\text{NH}_3$ · **Relative molecular mass:** $14 + 3 \times 1 = 17$ · **Nature:** Basic (alkaline) gas.
- Formed in nature by bacterial decay of nitrogenous organic matter (such as urea in urine: $\text{NH}_2\text{CONH}_2 + \text{H}_2\text{O} \rightarrow 2\text{NH}_3 + \text{CO}_2$), which gives public urinals their sharp smell. First prepared in pure form by Joseph Priestley (1774) and named *alkaline air*.

### Laboratory preparation of Ammonia ($\text{NH}_3$)

- **Principle:** In the laboratory, ammonia gas is prepared by heating a finely ground mixture of **ammonium chloride ($\text{NH}_4\text{Cl}$)** and **slaked lime / calcium hydroxide ($\text{Ca(OH)}_2$)** in the ratio **$2 : 1$** in a hard-glass test tube:

$$2\text{NH}_4\text{Cl} + \text{Ca(OH)}_2 \xrightarrow{\Delta} \text{CaCl}_2 + 2\text{H}_2\text{O} + 2\text{NH}_3 \uparrow$$

- **Important precautions and reasons in the setup (frequently asked in SEE):**
  1. **Why the hard-glass test tube is clamped slightly inclined downwards towards its mouth:** Water vapour produced during the reaction condenses near the cooler mouth of the tube; tilting the mouth slightly downwards prevents condensed water droplets from trickling back onto the hot glass bottom and **cracking the test tube**.
  2. **Why the gas is passed through a lime tower packed with quicklime ($\text{CaO}$):** To absorb moisture and **dry the ammonia gas**. Acidic drying agents like conc. $\text{H}_2\text{SO}_4$ or $\text{P}_2\text{O}_5$ and anhydrous $\text{CaCl}_2$ **cannot** be used because basic ammonia reacts with them ($2\text{NH}_3 + \text{H}_2\text{SO}_4 \rightarrow (\text{NH}_4)_2\text{SO}_4$ and $\text{CaCl}_2 + 8\text{NH}_3 \rightarrow \text{CaCl}_2\cdot 8\text{NH}_3$).
  3. **Why ammonia is collected in an inverted gas jar by the downward displacement of air:** Ammonia is **lighter than air** (vapour density $8.5$ vs air $14.4$) and **extremely soluble in water** ($1$ volume of water dissolves about $700\text{–}1300$ volumes of $\text{NH}_3$ at room temperature), so it cannot be collected over water.

### Industrial manufacture of Ammonia: Haber's Process

On an industrial scale, ammonia is manufactured by **Haber's synthetic process** by directly combining pure, dry **nitrogen ($\text{N}_2$)** and **hydrogen ($\text{H}_2$)** in the volume ratio **$1 : 3$**:

$$\text{N}_2\text{(g)} + 3\text{H}_2\text{(g)} \underset{450\text{–}500\ ^\circ\text{C},\ 200\text{–}900\ \text{atm}}{\stackrel{\text{Fe catalyst + Mo promoter}}{\rightleftharpoons}} 2\text{NH}_3\text{(g)} + \text{Heat}$$

- **Essential conditions for maximum yield in Haber's process:**
  1. **Temperature:** Optimum temperature of **$450\ ^\circ\text{C}$ to $500\ ^\circ\text{C}$** (the reaction is exothermic, so too high a temperature decomposes $\text{NH}_3$, while too low a temperature makes the reaction too slow).
  2. **Pressure:** High pressure of **$200\ \text{atm}$ to $900\ \text{atm}$** (typically $200\text{–}250\ \text{atm}$), because $4$ volumes of reactants ($\text{1 vol N}_2 + \text{3 vol H}_2$) contract to $2$ volumes of $\text{NH}_3$.
  3. **Catalyst and promoter:** Finely divided **iron ($\text{Fe}$)** as positive catalyst and **molybdenum ($\text{Mo}$)** (or $\text{K}_2\text{O}/\text{Al}_2\text{O}_3$) as **promoter** to increase the efficiency of the iron catalyst.

### Tests for Ammonia Gas

1. **Moist red litmus test:** Turns moist **red litmus paper blue**, confirming $\text{NH}_3$ is a basic gas.
2. **Hydrochloric acid rod test:** Bringing a glass rod dipped in **concentrated $\text{HCl}$** near the mouth of the jar produces **dense white fumes of solid ammonium chloride ($\text{NH}_4\text{Cl}$)**:
   $$\text{NH}_3 + \text{HCl (conc.)} \longrightarrow \text{NH}_4\text{Cl (dense white fumes)}$$
3. **Nessler's reagent test:** Passing ammonia through alkaline potassium mercuric iodide (**Nessler's reagent**) gives a **brown precipitate**.

### Physical Properties of Ammonia and the Fountain Experiment

- **Physical properties:** (1) Colourless gas with a **strong, pungent (choking) smell** that brings tears to the eyes; (2) **lighter than air**; (3) **extremely soluble in water**; (4) neither combustible in air nor a supporter of combustion (though it burns in pure oxygen with a greenish-yellow flame); (5) easily liquefied under pressure or by cooling to $-33.4\ ^\circ\text{C}$.
- **Fountain experiment (proving extreme solubility and basic nature of $\text{NH}_3$):**
  A dry round-bottomed flask filled with $\text{NH}_3$ gas is inverted over a trough containing water and a few drops of **phenolphthalein indicator** (colourless in neutral water) or red litmus solution. When a few drops of water are squeezed into the flask from a dropper, all the $\text{NH}_3$ in the flask dissolves instantly in those drops, creating a **partial vacuum (very low pressure)** inside the flask. Atmospheric pressure outside pushes the trough water rapidly up the jet tube, forming a **pink fountain** (with phenolphthalein) or **blue fountain** (with red litmus) inside the flask.

```figure caption="The ammonia fountain experiment. When a few drops of water from the dropper dissolve the ammonia gas inside the inverted flask, internal pressure drops sharply and atmospheric pressure forces the indicator solution up the jet tube as a pink/blue fountain."
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
fig, ax = plt.subplots(figsize=(4.4, 2.9))
ax.set_xlim(0, 8); ax.set_ylim(0, 6); ax.axis("off")
ax.add_patch(Circle((4.0, 4.3), 1.25, fc="#fde8ef", ec=INK, lw=1.2))
ax.add_patch(Rectangle((3.72, 2.5), 0.56, 0.7, fc="white", ec=INK, lw=1.2))
ax.add_patch(Rectangle((3.68, 2.35), 0.64, 0.2, fc=MUTED, ec=INK, lw=1.0))
ax.add_patch(Rectangle((2.3, 0.35), 3.4, 1.35, fc="#f6f8ff", ec=INK, lw=1.2))
ax.add_patch(Rectangle((2.35, 0.4), 3.3, 0.95, fc="#cfe2ff", ec="none"))
ax.plot([4.0, 4.0], [0.6, 4.0], color=INK, lw=1.5)
for ang, r in [(-0.4, 0.7), (-0.2, 0.9), (0, 1.0), (0.2, 0.9), (0.4, 0.7)]:
    ax.plot([4.0, 4.0+r*ang], [4.0, 4.0+r*0.85], color="#d63384", lw=1.4)
ax.plot([3.82, 3.82], [1.9, 2.85], color=INK, lw=1.2)
ax.add_patch(Circle((3.82, 1.8), 0.14, fc=MUTED, ec=INK, lw=0.9))
ax.text(4.0, 5.15, "Pink fountain\n(NH₃ + phenolphthalein)", ha="center", fontsize=7.2, color="#b01e68", fontweight="bold")
ax.text(6.4, 4.3, "Inverted flask\n(partial vacuum)", ha="center", fontsize=7.2, color=INK)
ax.text(1.7, 2.0, "Dropper\n(water)", ha="center", fontsize=7.0, color=INK)
ax.text(6.5, 0.9, "Water + phenolphthalein\n(pushed by atm. pressure)", ha="center", fontsize=6.9, color=INK)
fig.tight_layout()
```

### Chemical Properties and Uses of Ammonia

1. **Reaction with water:** Dissolves in water to form a weak alkali, **ammonium hydroxide ($\text{NH}_4\text{OH}$)**:
   $$\text{NH}_3 + \text{H}_2\text{O} \rightleftharpoons \text{NH}_4\text{OH} \rightleftharpoons \text{NH}_4^+ + \text{OH}^-$$
2. **Reaction with acids:** Reacts with acids ($\text{HCl}$, $\text{H}_2\text{SO}_4$, $\text{HNO}_3$) without forming water to produce **ammonium salts**:
   $$\text{NH}_3 + \text{HCl} \longrightarrow \text{NH}_4\text{Cl}, \qquad 2\text{NH}_3 + \text{H}_2\text{SO}_4 \longrightarrow (\text{NH}_4)_2\text{SO}_4$$
   $$\text{NH}_3 + \text{HNO}_3 \longrightarrow \text{NH}_4\text{NO}_3$$
3. **Reaction with carbon dioxide (formation of urea):** At $1500\ ^\circ\text{C}$ (or $180\text{–}200\ ^\circ\text{C}$ under pressure), forms **urea**:
   $$2\text{NH}_3 + \text{CO}_2 \xrightarrow{\Delta,\ \text{pressure}} \text{NH}_2\text{CONH}_2 + \text{H}_2\text{O}$$
4. **Reaction with oxygen (combustion and Ostwald catalytic oxidation):**
   - In pure oxygen, burns with a greenish-yellow flame: $4\text{NH}_3 + 3\text{O}_2 \xrightarrow{\Delta} 2\text{N}_2 + 6\text{H}_2\text{O}$.
   - Passed over heated **platinum ($\text{Pt}$) gauze at $800\ ^\circ\text{C}$**, it oxidises to nitric oxide ($\text{NO}$), the key step of **Ostwald's process** for making nitric acid ($\text{HNO}_3$): $4\text{NH}_3 + 5\text{O}_2 \xrightarrow{\text{Pt},\ 800\ ^\circ\text{C}} 4\text{NO} + 6\text{H}_2\text{O}$.
5. **Reaction with molten sodium:** Passing dry $\text{NH}_3$ over heated sodium at $300\ ^\circ\text{C}$ forms sodamide and hydrogen: $2\text{Na} + 2\text{NH}_3 \xrightarrow{300\ ^\circ\text{C}} 2\text{NaNH}_2 + \text{H}_2 \uparrow$.

- **Uses of Ammonia:** (1) Manufacture of nitrogenous chemical fertilisers (**urea, ammonium sulphate, ammonium nitrate, ammonium phosphate**); (2) manufacture of **nitric acid ($\text{HNO}_3$)** by Ostwald's process and **washing soda** by Solvay's process; (3) liquid ammonia is used as a **refrigerant** in cold-storage and ice factories because it has a high latent heat of vaporisation; (4) aqueous ammonia (**liquor ammonia**) cleans grease, oil stains and window glass; (5) used in making **blueprints** of maps and in manufacturing rayon, nylon, plastics and dyes.

## 16.3 Greenhouse effect and acid rain

### Greenhouse Effect

- **Artificial greenhouse:** A glass or transparent plastic house ("cold frame") used to grow off-season vegetables and flowers. Short-wavelength solar radiation enters through the roof, warms the soil and plants inside, and the re-radiated **long-wavelength infrared heat waves** cannot escape back out, keeping the interior warm.
- **Natural and enhanced greenhouse effect:** The Earth's atmosphere acts as a natural blanket. **Greenhouse gases** — **carbon dioxide ($\text{CO}_2$)**, **methane ($\text{CH}_4$)**, **water vapour ($\text{H}_2\text{O}$)**, **nitrous oxide ($\text{N}_2\text{O}$)**, **ozone ($\text{O}_3$)** and **chlorofluorocarbons ($\text{CFCs}$)** — trap outgoing infrared heat and keep the Earth habitable at an average of about $15\ ^\circ\text{C}$. However, excessive burning of fossil fuels and deforestation have raised greenhouse-gas levels, causing **global warming**, melting of Himalayan snow and glaciers, glacial lake outburst floods (GLOFs), rising sea levels and extreme weather.

### Acid Rain

::: definition Acid Rain
When atmospheric pollutants such as **sulphur dioxide ($\text{SO}_2$)**, **sulphur trioxide ($\text{SO}_3$)**, **oxides of nitrogen ($\text{NO}_x$)** and **carbon dioxide ($\text{CO}_2$)** emitted from factories, brick kilns and vehicles dissolve in rainwater, they form **sulphuric acid ($\text{H}_2\text{SO}_4$)**, **sulphurous acid ($\text{H}_2\text{SO}_3$)**, **nitric acid ($\text{HNO}_3$)** and **carbonic acid ($\text{H}_2\text{CO}_3$)**, lowering the pH of rainwater below $5.6$ (typically $3\text{–}5$). This acidic precipitation is called **acid rain**.
:::

- **Chemical equations of acid rain formation:**
  - $\text{SO}_2 + \text{H}_2\text{O} \longrightarrow \text{H}_2\text{SO}_3$ (sulphurous acid)
  - $2\text{SO}_2 + \text{O}_2 \longrightarrow 2\text{SO}_3$ and $\text{SO}_3 + \text{H}_2\text{O} \longrightarrow \text{H}_2\text{SO}_4$ (sulphuric acid)
  - $2\text{NO}_2 + \text{H}_2\text{O} \longrightarrow \text{HNO}_3$ (nitric acid) $+ \text{HNO}_2$ (nitrous acid)
  - $\text{CO}_2 + \text{H}_2\text{O} \rightleftharpoons \text{H}_2\text{CO}_3$ (carbonic acid)
- **Harmful effects:** (1) Corrodes marble, limestone monuments and temples ("stone leprosy"): $\text{CaCO}_3 + \text{H}_2\text{SO}_4 \rightarrow \text{CaSO}_4 + \text{H}_2\text{O} + \text{CO}_2$; (2) increases soil acidity and reduces crop fertility; (3) acidifies lakes and rivers, killing fish and aquatic life; (4) bleaches leaves and stunts forest growth; (5) causes skin and eye irritation.
- **Control measures:** Replace fossil fuels with clean hydroelectricity, solar and electric vehicles; install catalytic converters and desulphurisation scrubbers in factories; afforestation.

```photo id="sci10/urea" caption="Granules of urea (NH₂CONH₂), the most widely used nitrogenous fertiliser in Nepal, manufactured industrially by reacting ammonia (NH₃) with carbon dioxide (CO₂) under high temperature and pressure." width="54"
```

### Comparison between Carbon Dioxide ($\text{CO}_2$) and Ammonia ($\text{NH}_3$)

| Basis | Carbon Dioxide ($\text{CO}_2$) | Ammonia ($\text{NH}_3$) |
|---|---|---|
| **Chemical nature** | Acidic gas (turns moist blue litmus red) | Basic / alkaline gas (turns moist red litmus blue) |
| **Odour** | Odourless | Strong, pungent choking smell |
| **Density vs air** | About $1.5$ times **heavier** than air (mol. mass $44$) | **Lighter** than air (mol. mass $17$) |
| **Lab reactants** | Marble chips ($\text{CaCO}_3$) + dilute $\text{HCl}$ at room temperature | Ammonium chloride ($\text{NH}_4\text{Cl}$) + slaked lime ($\text{Ca(OH)}_2$) heated ($2:1$) |
| **Drying agent** | Conc. $\text{H}_2\text{SO}_4$ or anhydrous $\text{CaCl}_2$ | Quicklime ($\text{CaO}$) in a lime tower |
| **Collection method** | **Upward displacement of air** in an upright jar | **Downward displacement of air** in an inverted jar |
| **Confirmatory test** | Turns clear lime water milky white | Gives dense white fumes of $\text{NH}_4\text{Cl}$ with a rod dipped in conc. $\text{HCl}$ |

::: example Stoichiometry of CO₂ laboratory preparation
**Problem.** What mass of pure calcium carbonate ($\text{CaCO}_3$) is required to produce $22\ \text{g}$ of carbon dioxide gas on complete reaction with dilute $\text{HCl}$? ($\text{Ca} = 40,\ \text{C} = 12,\ \text{O} = 16$)

**Solution.** From the balanced equation $\text{CaCO}_3 + 2\text{HCl} \rightarrow \text{CaCl}_2 + \text{H}_2\text{O} + \text{CO}_2 \uparrow$, the molar mass of $\text{CaCO}_3 = 40 + 12 + 48 = 100\ \text{g}$ and the molar mass of $\text{CO}_2 = 12 + 32 = 44\ \text{g}$.
Since $44\ \text{g}$ of $\text{CO}_2$ is produced by $100\ \text{g}$ of $\text{CaCO}_3$, the mass required for $22\ \text{g}$ of $\text{CO}_2$ is:
$$m = \frac{100}{44} \times 22 = 50\ \text{g of CaCO}_3$$
:::

::: example Lime-water reactions (Short time vs Long time)
**Problem.** A colourless gas 'A' prepared from marble chips and dilute $\text{HCl}$ is passed through lime water for a short time to form a white precipitate 'B', and on passing excess 'A' for a long time, a clear solution 'C' is formed. Identify 'A', 'B' and 'C' with balanced equations.

**Solution.** 'A' is **carbon dioxide ($\text{CO}_2$)**, 'B' is **calcium carbonate ($\text{CaCO}_3$)**, and 'C' is **calcium bicarbonate ($\text{Ca(HCO}_3)_2$)**:
$$\text{Ca(OH)}_2 + \text{CO}_2\text{ (A)} \longrightarrow \text{CaCO}_3 \downarrow\text{ (B)} + \text{H}_2\text{O}$$
$$\text{CaCO}_3\text{ (B)} + \text{H}_2\text{O} + \text{CO}_2\text{ (excess)} \longrightarrow \text{Ca(HCO}_3)_2\text{ (C)}$$
:::

::: example Haber's process volume ratio and mass calculation
**Problem.** In Haber's process, how many grams of ammonia ($\text{NH}_3$) are produced when $28\ \text{g}$ of nitrogen ($\text{N}_2$) reacts completely with hydrogen ($\text{H}_2$)? ($\text{N} = 14,\ \text{H} = 1$)

**Solution.** From $\text{N}_2 + 3\text{H}_2 \rightleftharpoons 2\text{NH}_3$, $1\ \text{mole of N}_2\ (28\ \text{g})$ reacts with $3\ \text{moles of H}_2\ (6\ \text{g})$ to form $2\ \text{moles of NH}_3$:
$$m(\text{NH}_3) = 2 \times 17\ \text{g} = 34\ \text{g}$$
Therefore, $28\ \text{g}$ of nitrogen produces **$34\ \text{g}$ of ammonia**.
:::

## Chapter summary

- **Carbon dioxide ($\text{CO}_2$, mol. mass $44$):** Prepared in the lab at room temperature from marble chips and dilute $\text{HCl}$: $\text{CaCO}_3 + 2\text{HCl} \rightarrow \text{CaCl}_2 + \text{H}_2\text{O} + \text{CO}_2 \uparrow$. Collected in an upright jar by **upward displacement of air** ($1.5\times$ heavier than air, soluble in water).
- **Key reactions of $\text{CO}_2$:** Dissolves in water to form $\text{H}_2\text{CO}_3$; turns lime water milky ($\text{CaCO}_3 \downarrow$) on short passing and colourless ($\text{Ca(HCO}_3)_2$) in excess; burning $\text{Mg}$ continues to burn in $\text{CO}_2$ ($2\text{Mg} + \text{CO}_2 \rightarrow 2\text{MgO} + \text{C}$); reacts with $\text{NH}_3$ under heat and pressure to form **urea ($\text{NH}_2\text{CONH}_2$)**.
- **Ammonia ($\text{NH}_3$, mol. mass $17$):** Prepared in the lab by heating $\text{NH}_4\text{Cl}$ and $\text{Ca(OH)}_2$ ($2:1$): $2\text{NH}_4\text{Cl} + \text{Ca(OH)}_2 \xrightarrow{\Delta} \text{CaCl}_2 + 2\text{H}_2\text{O} + 2\text{NH}_3 \uparrow$. Dried through a **quicklime ($\text{CaO}$) tower** and collected in an inverted jar by **downward displacement of air** (lighter than air and extremely soluble in water).
- **Haber's process:** $\text{N}_2 + 3\text{H}_2 \rightleftharpoons 2\text{NH}_3 + \text{Heat}$ at **$450\text{–}500\ ^\circ\text{C}$**, **$200\text{–}900\ \text{atm}$**, with **$\text{Fe}$ catalyst** and **$\text{Mo}$ promoter**.
- **Tests for $\text{NH}_3$:** Turns moist red litmus blue; forms dense white fumes of $\text{NH}_4\text{Cl}$ with conc. $\text{HCl}$; turns Nessler's reagent brown. The **fountain experiment** demonstrates its extreme solubility in water and alkaline nature.
- **Greenhouse gases** ($\text{CO}_2, \text{CH}_4, \text{N}_2\text{O}, \text{CFCs}, \text{H}_2\text{O}$) trap infrared heat; excess emissions cause global warming. **Acid rain** ($\text{H}_2\text{SO}_4, \text{H}_2\text{SO}_3, \text{HNO}_3$ from $\text{SO}_2$ and $\text{NO}_x$) corrodes monuments and acidifies soil and water.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. By which method is carbon dioxide gas collected in the laboratory? <span class="marks">[1]</span>
   (a) downward displacement of water (b) downward displacement of air (c) upward displacement of air (d) upward displacement of water
2. Which compounds are formed in sequence when carbon dioxide is passed through lime water first for a short time and then for a long time? <span class="marks">[1]</span>
   (a) $\text{Ca(HCO}_3)_2$ then $\text{CaCO}_3$ (b) $\text{CaCO}_3$ then $\text{Ca(HCO}_3)_2$ (c) $\text{CaO}$ then $\text{CaCO}_3$ (d) $\text{CaCl}_2$ then $\text{CaCO}_3$
3. Which drying agent is used in the lime tower during the laboratory preparation of ammonia gas? <span class="marks">[1]</span>
   (a) conc. $\text{H}_2\text{SO}_4$ (b) anhydrous $\text{CaCl}_2$ (c) quicklime ($\text{CaO}$) (d) $\text{P}_2\text{O}_5$
4. In Haber's process for manufacturing ammonia, what are the roles of iron ($\text{Fe}$) and molybdenum ($\text{Mo}$)? <span class="marks">[1]</span>
   (a) both are reactants (b) Fe is promoter and Mo is catalyst (c) Fe is catalyst and Mo is promoter (d) both are drying agents
5. Which chemical fertiliser is formed when ammonia reacts with carbon dioxide at high temperature and pressure? <span class="marks">[1]</span>
   (a) ammonium sulphate (b) ammonium chloride (c) urea (d) calcium cyanamide
6. Which gas is primarily responsible for forming sulphuric acid in acid rain? <span class="marks">[1]</span>
   (a) $\text{NH}_3$ (b) $\text{CH}_4$ (c) $\text{SO}_2$ (d) $\text{H}_2$

::: note Answers to Group A
**1.** (c) — $\text{CO}_2$ is heavier than air and soluble in water, so it settles at the bottom of an upright jar by upward displacement of air.
**2.** (b) — insoluble $\text{CaCO}_3$ (milky) forms first, followed by soluble $\text{Ca(HCO}_3)_2$ (colourless) on passing excess $\text{CO}_2$.
**3.** (c) — basic quicklime ($\text{CaO}$) dries basic $\text{NH}_3$ without reacting with it; acidic drying agents react with $\text{NH}_3$.
**4.** (c) — finely divided iron ($\text{Fe}$) acts as positive catalyst and molybdenum ($\text{Mo}$) acts as promoter.
**5.** (c) — $2\text{NH}_3 + \text{CO}_2 \rightarrow \text{NH}_2\text{CONH}_2\text{ (urea)} + \text{H}_2\text{O}$.
**6.** (c) — $\text{SO}_2$ oxidises to $\text{SO}_3$ and reacts with rainwater to form $\text{H}_2\text{SO}_4$.
:::

**Group B — Short answer (2 marks each)**

1. Give reason: Carbon dioxide gas can be collected in an open upright gas jar, whereas ammonia gas is collected in an inverted gas jar. <span class="marks">[2]</span>
2. Give reason: Dilute sulphuric acid is not used instead of dilute $\text{HCl}$ to prepare $\text{CO}_2$ from marble chips, and conc. $\text{H}_2\text{SO}_4$ is not used to dry ammonia gas. <span class="marks">[2]</span>
3. Why is the hard-glass test tube clamped slightly inclined downwards towards its mouth during the laboratory preparation of ammonia? <span class="marks">[2]</span>
4. What happens when a burning magnesium ribbon is inserted into a jar full of $\text{CO}_2$ gas? Write the balanced chemical equation. <span class="marks">[2]</span>
5. State the conditions (temperature, pressure, catalyst and promoter) required for manufacturing ammonia by Haber's process with the balanced equation. <span class="marks">[2]</span>
6. What is acid rain? Write any two harmful effects of acid rain on the environment. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $\text{CO}_2$ is about $1.5$ times heavier than air, so it sinks to the bottom of an upright jar by upward displacement of air. $\text{NH}_3$ is lighter than air and extremely soluble in water, so it rises to the top of an inverted jar by downward displacement of air.
**2.** Dilute $\text{H}_2\text{SO}_4$ reacts with marble ($\text{CaCO}_3$) to form insoluble $\text{CaSO}_4$, which coats the marble and stops the reaction. Conc. $\text{H}_2\text{SO}_4$ cannot dry basic $\text{NH}_3$ because it reacts with $\text{NH}_3$ to form ammonium sulphate: $2\text{NH}_3 + \text{H}_2\text{SO}_4 \rightarrow (\text{NH}_4)_2\text{SO}_4$.
**3.** Water vapour formed during heating condenses near the cooler mouth of the test tube; inclining the tube slightly downwards prevents the condensed water from flowing back onto the hot glass base and cracking the tube.
**4.** Due to intense heat, magnesium continues to burn in $\text{CO}_2$ by stripping oxygen from it, forming white magnesium oxide powder and black carbon specks: $2\text{Mg} + \text{CO}_2 \xrightarrow{\Delta} 2\text{MgO} + \text{C}$.
**5.** Equation: $\text{N}_2 + 3\text{H}_2 \rightleftharpoons 2\text{NH}_3 + \text{Heat}$. Conditions: temperature **$450\text{–}500\ ^\circ\text{C}$**, pressure **$200\text{–}900\ \text{atm}$**, **iron ($\text{Fe}$)** catalyst and **molybdenum ($\text{Mo}$)** promoter.
**6.** Rainwater that becomes acidic ($\text{pH} < 5.6$) when industrial gases like $\text{SO}_2$ and $\text{NO}_x$ dissolve in it to form $\text{H}_2\text{SO}_4$ and $\text{HNO}_3$ is called acid rain. Effects: (i) corrodes marble monuments and historical temples; (ii) increases soil and water acidity, harming crops and aquatic life.
:::

**Group C — Long answer (4 marks each)**

1. Describe the laboratory preparation of carbon dioxide gas with a neat labelled diagram and balanced chemical equation. Also write what happens when $\text{CO}_2$ is passed through lime water for a short time and for a long time. <span class="marks">[4]</span>
2. Describe the laboratory preparation of dry ammonia gas with a neat labelled diagram and balanced chemical equation. How do you confirm that the gas jar is full of ammonia? <span class="marks">[4]</span>
3. Explain the ammonia fountain experiment with a labelled diagram. What two properties of ammonia does this experiment prove? <span class="marks">[4]</span>
4. Write the balanced chemical equations for the reaction of ammonia with (i) water, (ii) hydrochloric acid, (iii) carbon dioxide under heat and pressure, and (iv) write any two industrial uses of ammonia. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** Draw the $\text{CO}_2$ Woulfe's bottle setup (Figure 1a). Marble chips ($\text{CaCO}_3$) react with dilute $\text{HCl}$ at room temperature: $\text{CaCO}_3 + 2\text{HCl} \rightarrow \text{CaCl}_2 + \text{H}_2\text{O} + \text{CO}_2 \uparrow$. Collected by upward displacement of air. With lime water for a short time, white precipitate of $\text{CaCO}_3$ makes it milky: $\text{Ca(OH)}_2 + \text{CO}_2 \rightarrow \text{CaCO}_3 \downarrow + \text{H}_2\text{O}$. For a long time, soluble $\text{Ca(HCO}_3)_2$ makes it colourless again: $\text{CaCO}_3 + \text{H}_2\text{O} + \text{CO}_2 \rightarrow \text{Ca(HCO}_3)_2$.
**2.** Draw the $\text{NH}_3$ setup with inclined hard-glass tube and $\text{CaO}$ lime tower (Figure 1b). Finely ground $\text{NH}_4\text{Cl}$ and $\text{Ca(OH)}_2$ ($2:1$) are heated: $2\text{NH}_4\text{Cl} + \text{Ca(OH)}_2 \xrightarrow{\Delta} \text{CaCl}_2 + 2\text{H}_2\text{O} + 2\text{NH}_3 \uparrow$. The gas is dried through $\text{CaO}$ and collected in an inverted jar by downward displacement of air. **Confirmation test:** Hold a moist red litmus paper (turns blue) or a glass rod dipped in conc. $\text{HCl}$ (gives dense white fumes of $\text{NH}_4\text{Cl}$) at the mouth of the inverted jar.
**3.** Draw the fountain experiment setup (Figure 2). When a few drops of water are squeezed from the dropper into the inverted $\text{NH}_3$-filled flask, ammonia dissolves rapidly in the water drops, creating a partial vacuum inside the flask. Atmospheric pressure pushes the water + phenolphthalein solution up the jet tube as a pink fountain. It proves two properties: (i) **ammonia is extremely soluble in water**, and (ii) **aqueous solution of ammonia is basic (alkaline)** in nature.
**4.** (i) $\text{NH}_3 + \text{H}_2\text{O} \rightleftharpoons \text{NH}_4\text{OH}$; (ii) $\text{NH}_3 + \text{HCl} \rightarrow \text{NH}_4\text{Cl}$; (iii) $2\text{NH}_3 + \text{CO}_2 \xrightarrow{1500\ ^\circ\text{C},\ \text{pressure}} \text{NH}_2\text{CONH}_2 + \text{H}_2\text{O}$; (iv) Uses: manufacture of chemical fertilisers (urea, ammonium sulphate) and manufacture of nitric acid ($\text{HNO}_3$) / refrigerant in cold storage.
:::

