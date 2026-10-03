---
subject: Science and Technology
grade: 10
unit: 8
title: Pressure
hours: 0
area: Science and Technology
---

Why does a sharp knife cut better than a blunt one? Why do your ears hurt when you dive deep into a pond? How can a small mechanic's jack lift a heavy truck? Why does a steel ship float but a steel nail sink? All of these are answered by one idea: **pressure**. In this unit you will study pressure in solids, liquids and gases, the laws of Pascal and Archimedes, the pressure of the air around us, and the conditions for floating and sinking.

::: key What SEE asks from this unit
Definitions (pressure, Pascal's law, atmospheric pressure, Archimedes' principle, density, relative density), formulae $P = F/A$ and $P = h\rho g$, the working of a hydraulic machine, the law of floatation, and numericals on each. Many "Why …?" reasoning questions come from this unit.
:::

## 8.1 Pressure in solids, liquids and gases

### Thrust and pressure

The force acting at right angles (perpendicular) to a surface is called **thrust**. Its unit is the newton. When you stand, your weight is the thrust on the ground.

The same thrust can have very different effects depending on the area it acts on. A girl in high-heeled shoes sinks into soft soil but the same girl in flat shoes does not. A drawing pin has a sharp point and a broad head: the point gets a large effect from a small force.

::: definition Pressure
Pressure is the thrust (perpendicular force) acting per unit area of a surface.
:::

$$ P = \frac{F}{A} $$

The SI unit of pressure is the **pascal (Pa)**, where $1\ \text{Pa} = 1\ \text{N m}^{-2}$. Larger units: $1\ \text{kPa} = 1000$ Pa. 

- For the same force, pressure is **greater** when the area is **smaller**.
- For the same area, pressure is **greater** when the force is **greater**.

### Pressure in solids: applications

| To increase pressure (reduce the area) | To decrease pressure (increase the area) |
|---|---|
| Knives, axes, blades are sharpened | Tractors and trucks have wide tyres |
| Nails, needles and pins have pointed tips | Railway lines rest on broad wooden or concrete sleepers |
| A khukuri has a keen edge | Heavy buildings have wide foundations |
| Spikes in athletic shoes | Camels have broad flat feet for walking on sand; skis and snowshoes spread weight on snow |
| Chisels for stone | School bags have wide straps |

::: example Pressure of a person on the ground
**Problem.** A man of mass 60 kg stands on the ground. The area of contact of each shoe is 150 cm². Find the pressure on the ground (a) when he stands on both feet and (b) when he stands on one foot. Take $g = 9.8$ m s⁻².

**Solution.** Weight $= mg = 60 \times 9.8 = 588$ N. This is the thrust.

Area of one shoe $= 150\ \text{cm}^2 = 150 \times 10^{-4} = 0.015\ \text{m}^2$.

(a) Both feet: $A = 2 \times 0.015 = 0.03\ \text{m}^2$. $P = \dfrac{588}{0.03} = 19\,600$ Pa.

(b) One foot: $A = 0.015\ \text{m}^2$. $P = \dfrac{588}{0.015} = 39\,200$ Pa.

Standing on one foot doubles the pressure because the area is halved.
:::

::: caution Convert the area first
Many students divide the force in N by an area in cm². The SI unit needs m². Remember $1\ \text{cm}^2 = 10^{-4}\ \text{m}^2$ and $1\ \text{m}^2 = 10\,000\ \text{cm}^2$.
:::

### Pressure in liquids

A liquid has weight, so it presses on the bottom and on the walls of its container. Important facts:

1. A liquid exerts pressure on the bottom and on all the walls of the container.
2. Pressure at a point acts equally in all directions.
3. Pressure increases with depth. That is why the wall of a dam is thicker at the bottom, and why the water from the lowest hole of a bottle shoots out the farthest.
4. At the same depth in the same liquid, pressure is the same everywhere (it does not depend on the shape of the vessel).
5. Pressure depends on the density of the liquid: for the same depth, a denser liquid (like mercury) gives more pressure.

::: derivation Pressure at a depth $h$ in a liquid
We find the pressure at the bottom of a column of liquid from the weight of the column.

**Setting up.** Imagine a vertical column of liquid of height $h$ and base area $A$. The liquid has density $\rho$.

**Step 1 — volume of the column.**

$$ V = A\,h $$

**Step 2 — mass of the column.** Mass = density × volume:

$$ m = \rho V = \rho A h $$

**Step 3 — weight of the column.** This is the thrust on the base:

$$ F = mg = \rho A h g $$

**Step 4 — pressure = thrust ÷ area.**

$$ P = \frac{F}{A} = \frac{\rho A h g}{A} $$

**Result.**

$$ P = h\rho g $$

**What it means.** The pressure depends only on the depth $h$, the density $\rho$ of the liquid and $g$. It does not depend on the area of the base or on the shape of the vessel.

**Condition.** The liquid is at rest and its density is uniform. This is the pressure due to the liquid alone; the air above adds atmospheric pressure.
:::

::: tip The examiner is looking for
Volume $= Ah$, mass $= \rho Ah$, weight $= \rho Ahg$, then divide by $A$. Do not forget to say that $A$ cancels.
:::

```figure caption="Pressure of fresh water increases in a straight line with depth: P = h x 1000 x 9.8 (gauge pressure, atmosphere not included)."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4, 2.8))
h = np.linspace(0, 10, 50)
P = 1000*9.8*h/1000.0
ax.plot(P, h, color=ACCENT, lw=2)
ax.invert_yaxis()
ax.plot([98], [10], 'o', color='#A8271F', ms=4)
ax.annotate('10 m: 98 kPa', (98, 10), xytext=(35, 8.4), fontsize=8.5, color=INK,
            arrowprops=dict(arrowstyle='-', color=MUTED))
ax.set_xlabel('pressure due to water (kPa)'); ax.set_ylabel('depth h (m)')
ax.set_xlim(0, 110)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.5)
fig.tight_layout()
```

::: example Pressure under water
**Problem.** Find the pressure due to water at the bottom of a lake 20 m deep. Density of water is 1000 kg m⁻³ and $g = 10$ m s⁻². Also find the total pressure if atmospheric pressure is $1\times10^5$ Pa.

**Solution.** $P = h\rho g = 20 \times 1000 \times 10 = 2\times10^5$ Pa.

Total pressure $= 2\times10^5 + 1\times10^5 = 3\times10^5$ Pa.
:::

### Pressure in gases

A gas is made of molecules moving rapidly in all directions. They keep hitting the walls of the container. These countless tiny collisions produce a steady force on the walls, which gives the **gas pressure**. A gas fills its whole container and presses equally on all walls.

- If the gas is heated, the molecules move faster and strike harder, so pressure rises (a car tyre is more firmly inflated after a long drive).
- If the same gas is squeezed into a smaller volume, the molecules hit the walls more often, so pressure rises (Boyle's law, studied in the unit on gases).

## 8.2 Pascal's law

::: definition Pascal's law
When pressure is applied to an enclosed fluid (liquid or gas) at rest, the pressure is transmitted equally and undiminished in all directions through the fluid and to the walls of the container.
:::

You can show this with a hollow glass sphere having holes all over it, filled with water and fitted with a piston. When the piston is pushed, water spurts out equally from all holes.

### The hydraulic machine

A hydraulic machine has two cylinders joined by a pipe and filled with a liquid (oil). They have pistons of different areas: a small piston of area $a$ and a large piston of area $A$.

```photo id="sci10/hydraulic-jack" caption="A hydraulic bottle jack of the kind used to lift a vehicle. A small force on the handle gives a large lifting force." width="50"
```

```figure caption="A hydraulic press. A small force f on the small piston (area a) gives a large force F on the large piston (area A), because the pressure is the same in the liquid."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(4.8, 3.0))
ax.set_xlim(0, 12); ax.set_ylim(0, 7.5); ax.axis('off')
ax.add_patch(Rectangle((1.0, 1.0), 1.4, 3.0, fc='#CFE0FF', ec=INK, lw=1.3))
ax.add_patch(Rectangle((6.0, 1.0), 4.4, 3.0, fc='#CFE0FF', ec=INK, lw=1.3))
ax.add_patch(Rectangle((2.4, 1.0), 3.6, 0.8, fc='#CFE0FF', ec=INK, lw=1.3))
ax.add_patch(Rectangle((1.0, 3.2), 1.4, 0.35, fc=INK, ec=INK))
ax.add_patch(Rectangle((6.0, 3.2), 4.4, 0.35, fc=INK, ec=INK))
ax.plot([1.7, 1.7], [3.55, 5.2], color=INK, lw=2)
ax.plot([8.2, 8.2], [3.55, 5.0], color=INK, lw=2)
ax.add_patch(Rectangle((6.8, 5.0), 2.8, 0.5, fc='#BBBBBB', ec=INK))
ax.annotate('', xy=(1.7, 4.3), xytext=(1.7, 6.4), arrowprops=dict(arrowstyle='->', color='#A8271F', lw=2))
ax.text(1.7, 6.7, 'small force f', ha='center', fontsize=8.5, color=INK)
ax.annotate('', xy=(8.2, 6.8), xytext=(8.2, 5.6), arrowprops=dict(arrowstyle='->', color='#A8271F', lw=2))
ax.text(8.2, 7.1, 'large force F (load)', ha='center', fontsize=8.5, color=INK)
ax.text(1.7, 0.45, 'area a', ha='center', fontsize=8.5, color=INK)
ax.text(8.2, 0.45, 'area A', ha='center', fontsize=8.5, color=INK)
ax.text(8.2, 2.3, 'oil', ha='center', fontsize=9, color=INK)
```

::: derivation The force multiplication of a hydraulic machine
We use Pascal's law to relate the two forces.

**Setting up.** A force $f$ is applied on the small piston of area $a$. The large piston has area $A$ and gives out a force $F$.

**Step 1 — pressure produced by the small piston.**

$$ P = \frac{f}{a} $$

**Step 2 — Pascal's law.** The same pressure is transmitted to the large piston:

$$ P = \frac{F}{A} $$

**Step 3 — equate the two.**

$$ \frac{f}{a} = \frac{F}{A} $$

**Result.**

$$ F = f \times \frac{A}{a} $$

**What it means.** The output force is larger than the input force by the ratio of the areas $A/a$. This ratio is the **mechanical advantage**.

**Condition.** The liquid cannot be compressed and there is no friction or leakage. No energy is gained: the small piston must move a long distance to move the large piston a short distance.
:::

::: example Hydraulic lift
**Problem.** In a hydraulic lift the small piston has an area of 5 cm² and the large piston has an area of 500 cm². What force must be applied to the small piston to lift a load of 10,000 N? What is the mechanical advantage?

**Solution.** $\dfrac{f}{a} = \dfrac{F}{A}$, so

$f = F\times\dfrac{a}{A} = 10\,000 \times \dfrac{5}{500} = 100$ N.

Mechanical advantage $= \dfrac{A}{a} = \dfrac{500}{5} = 100$. (We may keep both areas in cm² because only their ratio is used.)

The small piston moves 100 times farther than the load: to raise the load by 1 cm the small piston goes down 100 cm.
:::

Applications of Pascal's law: hydraulic jack, hydraulic press, hydraulic brakes of cars and motorbikes, dentist's and barber's chairs, excavators and heavy machines.

## 8.3 Atmospheric pressure

The Earth is surrounded by a blanket of air called the **atmosphere**, extending to hundreds of kilometres. Air has weight, so it presses on everything. The pressure due to the weight of the air is **atmospheric pressure**.

::: definition Atmospheric pressure
The force exerted by the weight of the column of air above a unit area of the Earth's surface is called atmospheric pressure.
:::

At sea level it is about

$$ 1\ \text{atm} = 76\ \text{cm of Hg} = 760\ \text{mm of Hg} = 1.013\times10^{5}\ \text{Pa} $$

We are not crushed because the fluids inside our body press outward with the same pressure.

### Proofs that the air exerts pressure

- A tumbler filled with water and covered with a card can be turned upside down; the card does not fall because the atmosphere pushes it up.
- A rubber sucker sticks to a smooth wall because the air outside pushes it on.
- When air is pumped out of a tin can, the can is crushed by the outside air.
- We can drink with a straw because, when we suck, the pressure inside the straw falls and the atmospheric pressure pushes the juice up.
- Two Magdeburg hemispheres from which the air is removed cannot be pulled apart easily.

### Barometer

A **barometer** measures atmospheric pressure. In the simple mercury barometer (Torricelli, 1643) a glass tube about 1 m long, closed at one end, is filled with mercury and turned upside down in a dish of mercury. The mercury falls until its column is about **76 cm** high above the level in the dish. Above the mercury is an empty space (Torricelli's vacuum).

```photo id="sci10/barometer" caption="A laboratory mercury barometer: the height of the mercury column in the glass tube balances the pressure of the atmosphere." width="40"
```

At the level of the dish, the pressure of the mercury column equals atmospheric pressure:

$$ P_{atm} = h\rho g = 0.76 \times 13600 \times 9.8 \approx 1.013\times10^{5}\ \text{Pa} $$

The height does not change if the tube is tilted or the tube is wider; only the vertical height matters. It changes with weather and with altitude. Mercury is used because it is very dense: a water barometer would need a tube about 10.3 m tall.

### Variation with altitude

Pressure falls as we climb because the column of air above becomes shorter, and the air becomes thinner. At the top of Sagarmatha (8,849 m) the pressure is only about one third of the sea-level value. This is why climbers carry oxygen cylinders, why water boils below 100 °C in the hills (about 95 °C in Kathmandu), and why a pressure cooker is helpful there.

Other uses and instruments: the **aneroid barometer** (a metal box, used as an altimeter in aircraft); weather forecasting (low pressure usually means rain or storms); a pressure cooker works by raising the pressure so that water boils at a higher temperature; a suction pump and a siphon.

::: example Height of the barometer column
**Problem.** At a certain place the atmospheric pressure is $9.0\times10^{4}$ Pa. Find the height of the mercury column. (Density of mercury $= 13600$ kg m⁻³, $g = 10$ m s⁻².)

**Solution.** $h = \dfrac{P}{\rho g} = \dfrac{9.0\times10^{4}}{13600 \times 10} = \dfrac{90000}{136000} = 0.66$ m $= 66$ cm.

The mercury stands lower than at sea level, so this place is higher up (like a hill town).
:::

## 8.4 Archimedes and floatation

### Density and relative density

**Density** is the mass per unit volume: $\rho = \dfrac{m}{V}$ (unit kg m⁻³). Pure water has density 1000 kg m⁻³ (1 g cm⁻³). **Relative density** (specific gravity) is the ratio of the density of a substance to the density of water. It has no unit.

| Substance | Density (kg m⁻³) |
|---|---|
| Air | 1.2 |
| Cork | 240 |
| Wood (typical) | 600 |
| Ice | 917 |
| Pure water | 1000 |
| Sea water | 1025 |
| Iron | 7870 |
| Mercury | 13600 |
| Gold | 19300 |

### Upthrust (buoyant force)

A piece of wood pushed under water jumps back up. The liquid pushes up on any body placed in it. This upward force is called **upthrust** or **buoyant force**. It exists because pressure increases with depth, so the push on the bottom of the object is greater than the push on its top.

### Archimedes' principle

::: definition Archimedes' principle
When a body is fully or partly immersed in a fluid, it experiences an upward force (upthrust) equal to the weight of the fluid displaced by it.
:::

$$ \text{Upthrust} = V_{displaced}\,\rho_{fluid}\, g $$

Experimental proof: a stone hangs from a spring balance and shows weight $W_1$ in air. When it is lowered into a overflow can of water, the balance shows a smaller reading $W_2$. The loss of weight $W_1 - W_2$ equals the weight of the water that overflows into a beaker.

Because of upthrust, the weight of a body in a liquid appears less: **apparent weight = real weight − upthrust**.

::: example Upthrust on a stone
**Problem.** A stone of volume 0.002 m³ and weight 50 N in air is fully immersed in water. Find the upthrust and the apparent weight. ($\rho_w = 1000$ kg m⁻³, $g = 10$ m s⁻².)

**Solution.** Volume of water displaced $= 0.002\ \text{m}^3$.

Upthrust $= V\rho g = 0.002 \times 1000 \times 10 = 20$ N.

Apparent weight $= 50 - 20 = 30$ N.
:::

### Floating and sinking

Compare the weight $W$ of the body with the upthrust $U$ when it is fully under the liquid.

| Condition | Result |
|---|---|
| $W > U$ (body denser than liquid) | The body **sinks** |
| $W = U$ (density equal) | It **floats fully submerged** at any depth |
| $W < U$ (body less dense than liquid) | It rises and **floats partly submerged** until the upthrust equals the weight |

```figure caption="Sinking, suspended and floating bodies. W is the weight, U the upthrust. A floating body has U = W."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, axs = plt.subplots(1, 3, figsize=(5.0, 2.7))
titles = ['Sinks (W > U)', 'Suspended (W = U)', 'Floats (U = W)']
ypos = [0.6, 2.8, 4.4]
for ax, t, y in zip(axs, titles, ypos):
    ax.set_xlim(0, 4); ax.set_ylim(0, 7); ax.axis('off')
    ax.add_patch(Rectangle((0.2, 0.2), 3.6, 4.8, fc='#CFE0FF', ec=INK, lw=1.2))
    ax.set_title(t, fontsize=8.5, color=INK)
    ax.add_patch(Rectangle((1.4, y), 1.2, 1.0, fc='#8B6B3E', ec=INK, lw=1.2))
for ax, y, wl, ul in zip(axs, ypos, [1.4, 0.9, 0.9], [0.7, 0.9, 0.9]):
    cy = y + 0.5
    ax.annotate('', xy=(1.9, cy - wl - 0.1), xytext=(1.9, cy - 0.1), arrowprops=dict(arrowstyle='->', color='#A8271F', lw=1.8))
    ax.annotate('', xy=(2.1, cy + ul + 0.1), xytext=(2.1, cy + 0.1), arrowprops=dict(arrowstyle='->', color='#1B6E3A', lw=1.8))
axs[0].text(1.0, 0.45, 'W', fontsize=8.5, color='#A8271F')
axs[0].text(2.8, 1.6, 'U', fontsize=8.5, color='#1B6E3A')
fig.tight_layout()
```

### Law of floatation

::: definition Law of floatation
A floating body displaces a weight of liquid equal to its own weight.
:::

For a floating body, upthrust = weight of the body. A body of density $\rho_b$ floating in a liquid of density $\rho_l$ has a fraction of its volume submerged given by

$$ \frac{V_{sub}}{V} = \frac{\rho_b}{\rho_l} $$

::: example Fraction of a block that is submerged
**Problem.** A wooden block of density 600 kg m⁻³ floats in water. What fraction of its volume is under water? What happens in a liquid of density 1200 kg m⁻³?

**Solution.** In water: $\dfrac{V_{sub}}{V} = \dfrac{600}{1000} = 0.6$, so 60 % of the block is under water.

In the denser liquid: $\dfrac{600}{1200} = 0.5$, so only half is submerged. The denser the liquid, the higher the block floats.
:::

### Applications of floatation

- **Ships.** Iron sinks but a ship floats. A ship is hollow and its hull is shaped to displace a large volume of water. The weight of the water displaced equals the weight of the ship. So the **average density** of the ship (including the air inside) is less than that of water.
- **Plimsoll line.** The marks on the side of a ship show how deep it may safely sink in different waters (fresh, salt, tropical). A ship sinks deeper in fresh water than in sea water, since fresh water is less dense.
- **Submarines.** Ballast tanks are filled with water to dive and emptied with compressed air to rise.
- **Hydrometer.** An instrument floating upright in a liquid whose depth of sinking tells us the liquid's density. A **lactometer** (milk) is a hydrometer used to check the purity of milk.
- **Balloons and airships.** Filled with hydrogen or helium (less dense than air), they float in the air since the upthrust of the air is larger than their weight.
- A swimmer floats more easily in the Dead Sea or in sea water than in a river.
- Fish adjust their **swim bladder** to change average density and depth.

::: caution Floating and heaviness
A body does not float because it is "light", it floats because its **average density is less than that of the liquid**. A huge iron ship floats while a small iron nail sinks.
:::

::: example Does it float?
**Problem.** A metal tray has mass 2 kg and when it is set afloat in water its volume of water displaced when just about to sink is 0.004 m³. Does it float? ($g = 10$ m s⁻².)

**Solution.** Weight of tray $= 2 \times 10 = 20$ N. The maximum upthrust it can get is $0.004 \times 1000 \times 10 = 40$ N, which is greater than 20 N, so it floats. It will sink only until 0.002 m³ is displaced (upthrust 20 N = weight).
:::

## Chapter summary

- Pressure = thrust ÷ area: $P = F/A$; unit pascal (1 Pa = 1 N m⁻²). Small area gives high pressure.
- Liquid pressure: $P = h\rho g$; it increases with depth and acts equally in all directions at a point.
- Pascal's law: pressure on an enclosed fluid is transmitted equally in all directions. Hydraulic machine: $F = f\,(A/a)$.
- Atmospheric pressure at sea level $= 76$ cm Hg $= 1.013\times10^5$ Pa; it decreases with altitude. A barometer measures it.
- Archimedes' principle: upthrust = weight of fluid displaced $= V\rho g$; apparent weight = weight − upthrust.
- A body sinks if $\rho_b > \rho_l$, floats if $\rho_b < \rho_l$; for a floating body, upthrust = weight.
- Ships float because their average density is less than water's; submarines, hydrometers and balloons use the same law.

## Practice questions

**Group A — Objective (1 mark each)**

1. The SI unit of pressure is <span class="marks">[1]</span>
   (a) newton (b) pascal (c) joule (d) watt
2. The pressure in a liquid at a given depth depends on <span class="marks">[1]</span>
   (a) the shape of the vessel (b) the area of the base (c) the density of the liquid (d) none of these
3. Hydraulic brakes work on <span class="marks">[1]</span>
   (a) Archimedes' principle (b) Pascal's law (c) Newton's third law (d) Boyle's law
4. A mercury barometer reads 76 cm. If the tube is tilted, the vertical height of the mercury will be <span class="marks">[1]</span>
   (a) more than 76 cm (b) less than 76 cm (c) 76 cm (d) zero
5. A body floats in a liquid when <span class="marks">[1]</span>
   (a) its density is more than the liquid (b) its density is less than the liquid (c) it is hollow (d) it is made of iron

::: note Answers to Group A
**1.** (b) — 1 Pa = 1 N m⁻².
**2.** (c) — $P = h\rho g$; shape and area do not matter.
**3.** (b) — pressure on the brake fluid is transmitted equally to all wheels.
**4.** (c) — only the vertical height matters; the length of the tube filled increases.
**5.** (b) — a body with lower density than the liquid floats.
:::

**Group B — Short answer (2 marks each)**

1. Why is the wall of a dam made thicker at the bottom? <span class="marks">[2]</span>
2. State Pascal's law. Write one application. <span class="marks">[2]</span>
3. Why does a nail have a pointed tip and a broad head? <span class="marks">[2]</span>
4. State Archimedes' principle. <span class="marks">[2]</span>
5. Why does the pressure of the atmosphere decrease with height? <span class="marks">[2]</span>

::: note Answers to Group B
**1.** Pressure in a liquid increases with depth ($P = h\rho g$). The water at the bottom pushes the wall hardest, so the wall must be thicker to withstand it.
**2.** Pressure applied to an enclosed fluid is transmitted equally and undiminished in all directions. Application: the hydraulic jack (or hydraulic brake).
**3.** The pointed tip has a very small area, so a small force gives a large pressure that helps it enter the wood. The broad head has a large area, so the pressure on the hand is small and does not hurt.
**4.** When a body is immersed fully or partly in a fluid, it experiences an upthrust equal to the weight of the fluid it displaces.
**5.** The column of air above becomes shorter and the air becomes thinner, so there is less weight of air above.
:::

**Group C — Long answer (4 marks each)**

1. A box weighing 400 N rests on a floor with a contact area of 0.5 m². Calculate the pressure it exerts. If it is turned to rest on a face of area 0.2 m², what is the new pressure? <span class="marks">[4]</span>
2. Derive the expression $P = h\rho g$ for the pressure at a depth in a liquid. <span class="marks">[4]</span>
3. The areas of the small and large pistons of a hydraulic press are 10 cm² and 1000 cm². A force of 50 N is applied to the small piston. Find (a) the force on the large piston and (b) the mechanical advantage. <span class="marks">[4]</span>
4. A solid cube of side 10 cm and mass 0.5 kg is placed in water. Will it float or sink? Find the upthrust when it floats. ($\rho_w = 1000$ kg m⁻³, $g = 10$ m s⁻².) <span class="marks">[4]</span>
5. A diver is 30 m below the surface of a lake. Find the pressure due to the water, and the total pressure if the atmospheric pressure is $1.0\times10^5$ Pa. ($g = 10$ m s⁻².) <span class="marks">[4]</span>

::: note Answers to Group C
**1.** $P_1 = 400/0.5 = 800$ Pa. $P_2 = 400/0.2 = 2000$ Pa. The pressure is larger on the smaller area.
**2.** See the derivation box: volume $Ah$, mass $\rho Ah$, weight $\rho Ahg$, divide by $A$ to get $P = h\rho g$.
**3.** (a) $F = f \times A/a = 50 \times 1000/10 = 5000$ N. (b) Mechanical advantage $= 1000/10 = 100$.
**4.** Volume $= (0.1)^3 = 0.001$ m³. Density $= 0.5/0.001 = 500$ kg m⁻³, which is less than 1000, so it **floats**. Upthrust = weight $= 0.5 \times 10 = 5$ N. Half the cube is under water.
**5.** $P = h\rho g = 30 \times 1000 \times 10 = 3.0\times10^5$ Pa. Total $= 3.0\times10^5 + 1.0\times10^5 = 4.0\times10^5$ Pa.
:::
