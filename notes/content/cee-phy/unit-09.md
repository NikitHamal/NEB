---
subject: Physics
grade: CEE
unit: 9
title: Thermal Expansion and Quantity of Heat
hours: 2
area: Heat and Thermodynamics
---

Heat and Thermodynamics carries **7 of the 50 Physics questions** (official MEC
weightage), and we estimate about **2** of them come from this chapter. The marks
here are almost all numerical or definitional: a coefficient of expansion and its
relation to the other two, a liquid that overflows a vessel, a mixture that settles
at a final temperature, an ice–water–steam sum, or a clock that loses seconds on a
hot day. Every one of them is a one-line formula *provided* the phase bookkeeping is
done in the right order. That order is what this chapter teaches.

::: key What the paper asks from this chapter
- $\Delta L = L\alpha\Delta T$, $\Delta A = A\beta\Delta T$, $\Delta V = V\gamma\Delta T$, with $\beta = 2\alpha$ and $\gamma = 3\alpha$.
- A hole in a heated plate **grows**; a clamped rod develops stress $Y\alpha\Delta T$; a pendulum clock loses time $\frac{1}{2}\alpha\Delta\theta$ per unit time.
- Real and apparent expansion: $\gamma_r = \gamma_a + \gamma_v$ (real = apparent + vessel); the level in a vessel first dips, then rises.
- $Q = mc\Delta T$, $Q = C\Delta T$, and the method of mixtures $m_1c_1(\theta_1-\theta) = (m_2c_2 + Wc_w)(\theta-\theta_2)$.
- Water equivalent $W = m_c c_c / c_w$; ignoring it makes the answer wrong in a predictable direction.
- $Q = mL$; $L_f = 3.36\times10^5\ \text{J kg}^{-1}$, $L_v = 2.26\times10^6\ \text{J kg}^{-1}$; temperature stays constant during a phase change.
- Newton's law of cooling: rate of loss of heat $\propto$ excess temperature, so cooling is exponential.
- The triple point of water: 273.16 K at 611 Pa, the only state where ice, water and vapour coexist.
:::

## 9.1 Linear, superficial and cubical expansion and their relation

Almost every substance expands when heated at constant pressure. The atoms vibrate
about fixed mean positions; the vibration is **not symmetric** about the mean
position — the repulsive side of the potential is steeper than the attractive side —
so the average separation grows as the amplitude grows. Nothing in the solid is
pushed apart by a "force of heat"; the spacing simply increases.

### The three coefficients

::: definition Coefficients of expansion
For a rise in temperature $\Delta T$:

- **Linear:** $\alpha = \dfrac{1}{L}\dfrac{\Delta L}{\Delta T}$ — fractional increase in length per kelvin.
- **Superficial:** $\beta = \dfrac{1}{A}\dfrac{\Delta A}{\Delta T}$ — fractional increase in area per kelvin.
- **Cubical (volume):** $\gamma = \dfrac{1}{V}\dfrac{\Delta V}{\Delta T}$ — fractional increase in volume per kelvin.
:::

All three have SI unit **K⁻¹** (numerically the same as °C⁻¹, because a temperature
*difference* is the same on both scales). They are properties of the material, not
of the size or shape of the body: a long rod and a short rod of copper have the same
α.

| Quantity | Symbol | Formula | Unit |
|---|---|---|---|
| Change in length | $\Delta L$ | $L\alpha\Delta T$ | m |
| Change in area | $\Delta A$ | $A\beta\Delta T$ | m² |
| Change in volume | $\Delta V$ | $V\gamma\Delta T$ | m³ |
| New length | $L'$ | $L(1+\alpha\Delta T)$ | m |

Typical values at room temperature (K⁻¹):

| Material | $\alpha$ | Material | $\alpha$ |
|---|---|---|---|
| Quartz (fused) | $0.4\times10^{-6}$ | Copper | $1.7\times10^{-5}$ |
| Invar | $1.2\times10^{-6}$ | Brass | $1.9\times10^{-5}$ |
| Glass | $8\times10^{-6}$ | Aluminium | $2.4\times10^{-5}$ |
| Steel, iron | $1.2\times10^{-5}$ | Lead | $2.9\times10^{-5}$ |

Two things to read off this table. Invar was invented for pendulum rods and tape
measures precisely because its α is ten times smaller than steel's. And **liquids
and gases expand far more than solids**: for mercury $\gamma = 1.8\times10^{-4}$ K⁻¹,
for water about $2.1\times10^{-4}$ K⁻¹, for air at constant pressure
$\gamma = 1/273 \approx 3.7\times10^{-3}$ K⁻¹. A gas is some twenty times more
expansive than a liquid and a few hundred times more than a solid.

### Why β = 2α and γ = 3α

::: derivation β = 2α and γ = 3α
**Starting point.** A cube of side $L$ is heated through $\Delta T$; every side grows
by the same fraction $\alpha\Delta T$. We want the coefficients of area and volume.

**Setting up.** $L' = L(1+\alpha\Delta T)$, area $A = L^2$, volume $V = L^3$.

**Step 1 — square the new side.** $A' = L'^2 = L^2(1+\alpha\Delta T)^2
= A(1 + 2\alpha\Delta T + \alpha^2\Delta T^2)$.

**Step 2 — throw away the squared term.** For a metal, $\alpha\Delta T$ is about
$10^{-5}\times50 = 5\times10^{-4}$; its square is $2.5\times10^{-7}$, a thousandth
of the linear term. Keeping only the first power,
$A' = A(1 + 2\alpha\Delta T)$, so $\Delta A = A(2\alpha)\Delta T$.

**Step 3 — compare with the definition.** $\Delta A = A\beta\Delta T$, hence
$\beta = 2\alpha$.

**Step 4 — cube the new side.** $V' = L'^3 = V(1+\alpha\Delta T)^3
= V(1 + 3\alpha\Delta T + 3\alpha^2\Delta T^2 + \alpha^3\Delta T^3)$, and again only
the first power survives: $\Delta V = V(3\alpha)\Delta T$, hence $\gamma = 3\alpha$.

**Result.** $\beta = 2\alpha$ and $\gamma = 3\alpha$.

**What it means.** The three coefficients are not independent: measure one and you
have all three. The conditions are that the solid is **isotropic** (the same α in
every direction — true for a metal, false for wood or a crystal) and that
$\alpha\Delta T \ll 1$.
:::

::: caution The classic wrong pair
Area uses $2\alpha$, volume uses $3\alpha$. Students who write $\gamma = 3\alpha$
for an area, or $\beta = \frac{3}{2}\alpha$, lose the mark every time. Fix the
picture in your head: length is one dimension, area two, volume three.
:::

The relation holds for **any** linear dimension of the body, including a hole. A
plate with a circular hole is, geometrically, the same as a plate with a disc of the
same material filling the hole — so on heating the disc grows and the hole grows
with it. The hole does **not** close up. This single fact is asked in some form in
almost every paper.

### Bimetallic strip

Two different metals — usually brass and iron — are riveted or welded along their
whole length. Brass has the larger α (about $1.9\times10^{-5}$ against
$1.2\times10^{-5}$ K⁻¹).

```figure caption="A bimetallic strip. On heating, brass lengthens more than iron, so the strip curves with brass on the outer (convex) side. On cooling it curves the other way, with brass on the inner side."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.9))
BRASS, IRON = '#B8860B', '#4A5568'
xs = np.linspace(0, 1, 200)
for x0, amp, tag in [(0.15, 0.0, 'room\ntemperature'), (2.65, 0.42, 'heated'), (5.15, -0.42, 'cooled')]:
    yc = amp*np.sin(np.pi*xs)
    ax.plot(x0+1.55*xs, 2.55+yc+0.055, color=BRASS, lw=6, solid_capstyle='butt', zorder=3)
    ax.plot(x0+1.55*xs, 2.55+yc-0.055, color=IRON, lw=6, solid_capstyle='butt', zorder=3)
    ax.text(x0+0.78, 1.28, tag, ha='center', va='center', fontsize=8.5, color=INK)
ax.annotate('brass', xy=(0.62,2.62), xytext=(0.30,3.45), fontsize=8.5, color=INK,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
ax.annotate('iron', xy=(0.62,2.44), xytext=(0.30,1.85), fontsize=8.5, color=INK,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
ax.text(2.65+0.78, 3.42, 'brass outside', ha='center', fontsize=8.5, color=BRASS)
ax.text(5.15+0.78, 3.30, 'brass inside', ha='center', fontsize=8.5, color=BRASS)
ax.set_xlim(0,7.2); ax.set_ylim(0.7,3.85); ax.axis('off')
```

On heating, the brass side becomes longer than the iron side, so the strip can only
stay joined by bending into an arc in which the brass is on the **outside** (the
longer path). On cooling the brass contracts more, so it ends up on the **inside**.
The strip therefore bends *towards* the metal with the smaller α when heated.

Uses: the **thermostat** in an electric iron, a geyser or a refrigerator (the strip
curls, breaks a contact, the heater switches off, and it straightens again when the
temperature falls); the **bimetallic thermometer**; and temperature compensation in
watches.

### Thermal stress

If a rod is clamped at both ends, it cannot expand, and the "lost" expansion appears
as an elastic strain:

$$ \text{strain} = \frac{\Delta L}{L} = \alpha\Delta T, \qquad
\sigma = Y\,\alpha\Delta T, \qquad F = YA\,\alpha\Delta T $$

where $Y$ is Young's modulus. The stress is **compressive** on heating (the rod
would have grown, so it is squeezed) and **tensile** on cooling. This is why
concrete roads are laid in slabs with tar-filled gaps, why railway rails are welded
with expansion joints, and why a glass tumbler cracks when boiling water is poured
into it: the inner surface tries to expand against a cold, unyielding outer surface.

::: example Worked example 9.1 — the gap in a rail
**Problem.** Steel rails 20 m long are laid at 15 °C. What gap must be left between
consecutive rails so that they just touch at 55 °C? ($\alpha = 1.2\times10^{-5}$ K⁻¹.)

**Solution.** $\Delta T = 40$ K, so
$\Delta L = L\alpha\Delta T = 20\times1.2\times10^{-5}\times40 = 9.6\times10^{-3}$ m
$= 9.6$ mm. So a gap of about 1 cm — the growth of one rail — is left at each
joint, which is why a train crossing a joint sets up the familiar clickety-click.
:::

::: example Worked example 9.2 — a clock on a hot day
**Problem.** A pendulum clock keeps correct time at 20 °C. Its rod is steel
($\alpha = 2\times10^{-5}$ K⁻¹). How much time does it lose in one day at 35 °C?

**Solution.** The period is $T_p = 2\pi\sqrt{L/g}$, so
$\frac{\Delta T_p}{T_p} = \frac{1}{2}\frac{\Delta L}{L} = \frac{1}{2}\alpha\Delta\theta$.
With $\Delta\theta = 15$ K, the fractional change is
$\frac{1}{2}(2\times10^{-5})(15) = 1.5\times10^{-4}$.
In a day the clock runs slow by $1.5\times10^{-4}\times86400 = 12.96$ s ≈ **13 s**.

The pendulum is *longer*, so each swing takes *longer*, so the clock **loses** time.
A cooling rod would make it gain.
:::

::: tip Two one-line checks
For a heated body, ask "does the *fractional* change look like $10^{-4}$?" —
$\alpha\Delta T$ for a metal and a 50 K rise is about $6\times10^{-4}$, i.e. 0.06 %.
If your answer is a few per cent, you have used the wrong coefficient or the wrong
power of ten. For a clock, remember the factor $\frac{1}{2}$: the period depends on
$\sqrt{L}$, not on $L$.
:::

## 9.2 Real and apparent expansion of liquids

A liquid has no fixed shape, so it has **only one** coefficient — the cubical one,
$\gamma$. (Writing "the linear expansion of water" is meaningless.) Its expansion is
measured by watching the level in a narrow stem, and that is where the trouble
starts: **the vessel is expanding too**, so the scale you read against is itself
growing.

### Apparent and real expansion

::: definition Apparent and real expansion
- **Real (absolute) expansion** is the true increase in the liquid's own volume.
- **Apparent expansion** is the increase measured *relative to the vessel*, i.e. the
  extra volume the liquid seems to gain as read on the vessel's own graduations.

The liquid that overflows a brim-full vessel is the **apparent** expansion; the real
expansion is larger, because the vessel's capacity also grew and swallowed part of it.
:::

Let the vessel be filled to the brim at the lower temperature, with volume $V$ and
coefficient $\gamma_v$; let the liquid's real coefficient be $\gamma_r$.

Vessel capacity at the higher temperature: $V_v = V(1+\gamma_v\Delta T)$.
Liquid volume at the higher temperature: $V_l = V(1+\gamma_r\Delta T)$.

The liquid that overflows is the difference:

$$ V_l - V_v = V(\gamma_r - \gamma_v)\Delta T $$

But the overflow is, by definition, the *apparent* expansion $V\gamma_a\Delta T$.
Comparing the two:

$$ \gamma_a = \gamma_r - \gamma_v \qquad\Longrightarrow\qquad
\gamma_r = \gamma_a + \gamma_v $$

So the **real coefficient is always larger than the apparent one**, and the gap is
exactly the expansion of the vessel. For a glass vessel $\gamma_v = 3\alpha_{glass}
\approx 2.4\times10^{-5}$ K⁻¹, which is small beside mercury's
$1.8\times10^{-4}$ but not negligible — it is about 13 % of it.

| Liquid in a glass vessel | $\gamma_r$ (K⁻¹) | $\gamma_a = \gamma_r - \gamma_v$ (K⁻¹) |
|---|---|---|
| Mercury | $1.82\times10^{-4}$ | $1.58\times10^{-4}$ |
| Water (around 20 °C) | $2.1\times10^{-4}$ | $1.86\times10^{-4}$ |
| Alcohol | $1.1\times10^{-3}$ | $1.08\times10^{-3}$ |
| Paraffin | $9.0\times10^{-4}$ | $8.8\times10^{-4}$ |

::: example Worked example 9.3 — overflow from a flask
**Problem.** A glass flask is completely filled with 500 cm³ of a liquid at 20 °C.
On heating to 70 °C, 4.0 cm³ overflows. If $\gamma_v = 2.4\times10^{-5}$ K⁻¹, find
the apparent and the real coefficients of the liquid.

**Solution.** $\Delta T = 50$ K and
$\gamma_a = \dfrac{\Delta V}{V\Delta T} = \dfrac{4.0}{500\times50}
= 1.6\times10^{-4}$ K⁻¹.
Then $\gamma_r = \gamma_a + \gamma_v = 1.6\times10^{-4} + 0.24\times10^{-4}
= 1.84\times10^{-4}$ K⁻¹.
The 4 cm³ that spilled understates the liquid's real growth by 0.24 × 10⁻⁴ × 500 ×
50 = 0.6 cm³, which the flask absorbed by growing.
:::

::: caution Sign and direction
$\gamma_r = \gamma_a + \gamma_v$, never $\gamma_a - \gamma_v$. If a question gives
the *real* coefficient and asks for the overflow, subtract: the overflow is
$V(\gamma_r - \gamma_v)\Delta T$. Reading the relation the wrong way round is the
single commonest error in this topic.
:::

### Why the level first falls, then rises

Warm a flask of coloured water gently and watch the top of the liquid in the stem.
It **dips** slightly, then climbs steadily past its starting mark.

The reason is a race between two expansions that start at the same moment but do not
have the same size. The glass in contact with the warming liquid heats up first and
quickly, so the flask's capacity grows early. The liquid as a whole is a poor
conductor and warms slowly, so for the first few seconds its own expansion is still
tiny. Capacity up, liquid not yet up → level down. Once the bulk liquid warms, its
much larger $\gamma$ takes over and the level rises.

```figure caption="Height of the liquid in the stem as a flask is warmed slowly. The level dips while the glass is expanding faster than the liquid, then rises once the liquid's much larger expansivity dominates."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9,2.85))
t = np.linspace(0, 10, 400)
h = 100 + 0.06*t**2 - 1.15*(1-np.exp(-1.1*t))
ax.plot(t, h, color=ACCENT, lw=2.0, zorder=3)
imin = t[np.argmin(h)]
ax.plot([imin],[h.min()], 'o', color=ACCENT, ms=5, zorder=4)
ax.axhline(100, color=MUTED, lw=0.9, ls=(0,(4,3)))
ax.annotate('level dips: the\nvessel grows first', xy=(imin, h.min()-0.04), xytext=(0.25, 98.85),
            fontsize=8.5, color=INK, va='center', ha='left',
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.8, mutation_scale=8))
ax.annotate('liquid expansion\ntakes over', xy=(4.9, 100.5), xytext=(4.35, 102.6),
            fontsize=8.5, color=INK, va='center', ha='left',
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.8, mutation_scale=8))
ax.text(6.3, 99.72, 'starting level', fontsize=8.5, color=MUTED, va='center', ha='left')
ax.set_xlabel('time after warming begins  (arbitrary units)')
ax.set_ylabel('level in stem  (mm)')
ax.set_xlim(0,10); ax.set_ylim(98.4,104.6)
ax.set_yticks([99,100,101,102,103,104])
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.5)
```

A second, quite different cause of a dip is **anomalous expansion**: between 0 °C and
4 °C water *contracts* as it warms, so its level genuinely falls.

### Anomalous expansion of water

Water is not a normal liquid. From 0 °C to 4 °C it **contracts**; above 4 °C it
expands in the ordinary way. Its density therefore peaks at 4 °C:

```figure caption="Density of water against temperature. The maximum at 4 °C is the anomalous region: warming from 0 °C to 4 °C makes water contract."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.85))
T = np.array([0,2,4,6,8,10,15,20,25,30,40])
rho = np.array([999.84,999.94,999.97,999.94,999.85,999.70,999.10,998.21,997.05,995.65,992.22])
ax.plot(T, rho, color=ACCENT, lw=2.0, zorder=3)
ax.plot([4],[999.97], 'o', color=ACCENT, ms=5, zorder=4)
ax.annotate('maximum density at 4 °C', xy=(4.35,999.99), xytext=(7.0,1000.95),
            fontsize=8.5, color=INK, va='center', ha='left',
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.8, mutation_scale=8))
ax.axvline(4, color=GRID, lw=0.9)
ax.set_xlabel('temperature  (°C)'); ax.set_ylabel('density  (kg m⁻³)')
ax.set_xlim(0,40); ax.set_ylim(991,1001.8)
ax.set_xticks([0,4,10,20,30,40])
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.5)
```

Consequences you can be asked to explain:

- **Ice floats**, because ice (917 kg m⁻³) is less dense than water.
- A pond **freezes from the top down**. The surface water cools to 4 °C and sinks;
  below 4 °C it is lighter and stays on top, where it freezes. The 4 °C water at the
  bottom lets fish survive the winter.
- Water in a **closed pipe bursts** when it freezes: the 8 % expansion is resisted by
  the pipe, and the pressure rise is enormous.

**Density falls as the temperature rises.** From $V = V_0(1+\gamma\Delta T)$ and
$\rho = m/V$,

$$ \rho = \frac{\rho_0}{1+\gamma\Delta T} \approx \rho_0(1-\gamma\Delta T) $$

so a rise of $\Delta T$ lowers the density by the fraction $\gamma\Delta T$. A body's
**relative density** falls on heating, and a solid floats a little deeper in hot
water than in cold.

## 9.3 Heat capacity, specific heat capacity and the method of mixtures

### The three quantities

::: definition Heat capacity and specific heat capacity
**Heat capacity** $C$ of a body is the heat needed to raise its temperature by 1 K:
$C = Q/\Delta T$, unit J K⁻¹. It depends on the *amount* of material.

**Specific heat capacity** $c$ is the heat needed to raise **1 kg** of the substance
by 1 K: $c = \dfrac{Q}{m\Delta T}$, unit J kg⁻¹ K⁻¹. It is a property of the
*material* only.

**Molar heat capacity** is the heat needed to raise 1 mol by 1 K, unit
J mol⁻¹ K⁻¹.
:::

So $Q = mc\Delta T = C\Delta T$, and $C = mc$. A 2 kg block of copper has twice the
heat capacity of a 1 kg block, but the same specific heat capacity.

| Substance | $c$ (J kg⁻¹ K⁻¹) | Substance | $c$ (J kg⁻¹ K⁻¹) |
|---|---|---|---|
| Water | 4200 | Brass | 380 |
| Ice | 2100 | Copper | 390 |
| Steam | 2010 | Iron, steel | 480 |
| Kerosene | 2100 | Aluminium | 900 |
| Mercury | 140 | Lead | 130 |

**Water's specific heat is unusually large** — about ten times that of copper. That
one number explains why water is used as a coolant in vehicle radiators, why a
hot-water bottle stays warm for hours, why coastal climates are milder than inland
ones, and why a kettle of water takes so long to boil. It is also why water is the
standard calorimetric liquid: a given mass of water changes temperature slowly, so a
mixture experiment is easy to time.

### Water equivalent

A calorimeter is a metal cup, and it takes heat too. Rather than carry its mass and
specific heat through every calculation, we convert it into the mass of **water**
that would take the same heat for the same temperature rise:

$$ W = \frac{m_c c_c}{c_w} \quad\text{(in kg)} \qquad\Longrightarrow\qquad
\text{heat capacity of calorimeter} = Wc_w $$

A copper calorimeter of mass 0.10 kg and $c = 390$ J kg⁻¹ K⁻¹ has water equivalent
$W = 0.10\times390/4200 = 0.0093$ kg = 9.3 g. Its heat capacity is
$9.3\times10^{-3}\times4200 = 39$ J K⁻¹.

### The method of mixtures

::: key Principle of calorimetry
In an isolated system, **heat lost by the hot bodies = heat gained by the cold
bodies**. No heat is created or destroyed; it only moves.
:::

Put a hot solid of mass $m_1$, specific heat $c_1$, at temperature $\theta_1$ into
water of mass $m_2$ at $\theta_2$, inside a calorimeter of water equivalent $W$. If
the final temperature is $\theta$ (with $\theta_2 < \theta < \theta_1$):

$$ m_1c_1(\theta_1-\theta) = (m_2c_w + Wc_w)(\theta-\theta_2) $$

Every bracket is **positive**: a hot body *falls* from $\theta_1$ to $\theta$, so its
change is $\theta_1-\theta$; a cold body *rises* from $\theta_2$ to $\theta$, so its
change is $\theta-\theta_2$. Writing the two brackets the same way round is the
source of most sign errors in this topic.

::: example Worked example 9.4 — finding a specific heat
**Problem.** A 0.10 kg block of metal at 100 °C is dropped into 0.20 kg of water at
20 °C in a calorimeter of water equivalent 0.02 kg. The final temperature is 25 °C.
Find the specific heat of the metal. ($c_w = 4200$ J kg⁻¹ K⁻¹.)

**Solution.** Heat gained by the water and calorimeter:
$(0.20 + 0.02)\times4200\times(25-20) = 0.22\times4200\times5 = 4620$ J.
Heat lost by the metal: $0.10\times c\times(100-25) = 7.5c$.
Equating: $7.5c = 4620$, so $c = 616$ J kg⁻¹ K⁻¹ ≈ $6.2\times10^2$ J kg⁻¹ K⁻¹.

If the calorimeter had been ignored, the heat gained would have been taken as
$0.20\times4200\times5 = 4200$ J and the answer would have come out as 560 J kg⁻¹ K⁻¹
— 9 % too low. That is the size of the error a 20 g water equivalent makes.
:::

::: caution Three ways a mixture answer goes wrong
1. **Ignoring the calorimeter.** Its water equivalent must be added to the water
   mass. Leaving it out always makes the hot body's specific heat come out **too
   low** (too little heat is credited to the cold side).
2. **Sign flip.** Use $(\theta_1-\theta)$ for the hot side and $(\theta-\theta_2)$
   for the cold side. A negative answer means you reversed one of them.
3. **Stopping at 0 °C.** If ice is involved, check first whether *all* the ice can
   melt with the heat available. If it cannot, the final temperature is 0 °C with
   some ice left, and the water term must not be used at all.
:::

### Newton's law of cooling

::: definition Newton's law of cooling
The rate at which a body loses heat to its surroundings is directly proportional to
the **excess of its temperature over the surroundings**, provided that excess is
small and the surroundings are at a constant temperature:

$$ \frac{dQ}{dt} = k(\theta-\theta_s) $$
:::

Since $dQ = -mc\,d\theta$ for the body, the same law can be written as a statement
about the **rate of fall of temperature**:

$$ \frac{d\theta}{dt} = -K(\theta-\theta_s), \qquad K = \frac{k}{mc} $$

Integrating from $\theta_0$ at $t = 0$:

$$ \theta - \theta_s = (\theta_0-\theta_s)\,e^{-Kt} $$

so the excess temperature decays exponentially. Three consequences the paper uses:

- **The hotter body cools faster.** At 90 °C in a 25 °C room the body loses heat five
  times as fast as at 38 °C. This is why a cup of tea is drinkable in ten minutes but
  takes an hour to come down to room temperature.
- **A plot of $\ln(\theta-\theta_s)$ against $t$ is a straight line** of slope $-K$.
  That is the standard experimental verification of the law.
- **The law is only a small-excess approximation** to Stefan's law. For a body much
  hotter than its surroundings, radiation loss grows as $T^4$ and Newton's law fails.

::: example Worked example 9.5 — cooling coffee in Kathmandu
**Problem.** A cup of coffee at 90 °C is left in a room at 25 °C. It cools to 70 °C
in 5 minutes. How long will it take to reach 50 °C?

**Solution.** Excess temperatures: initially $90-25 = 65$ K, after 5 min
$70-25 = 45$ K. From the exponential law,
$45 = 65e^{-5K}$, so $K = \frac{1}{5}\ln(65/45) = 0.0734$ min⁻¹.
For 50 °C the excess is 25 K:
$25 = 65e^{-Kt}$, so $t = \frac{\ln(65/25)}{0.0734} = \frac{0.9555}{0.0734}
= 13$ min.

The first 20 K took 5 min; the next 20 K takes 8 min — the cooling slows as the
excess shrinks. Any answer that gives equal times for equal temperature drops has
used a linear law by mistake.
:::

**Cooling correction.** In a real mixture experiment the calorimeter loses heat to
the room while the mixture settles. Newton's law supplies the fix: plot the
temperature against time, and extrapolate the cooling curve backwards to the instant
of mixing. The corrected final temperature is slightly higher than the highest
reading, and the corrected initial rate is read from the same graph. This is why the
experiment is stirred quickly, started close to room temperature, and finished fast.

## 9.4 Latent heat of fusion and vaporization; the triple point

### Latent heat

While ice melts at 0 °C, its temperature does not rise, however hard you heat it.
The heat is doing something else: it is pulling the molecules out of the rigid
lattice and into the liquid. The energy goes into **potential** energy of the
molecules, not into their kinetic energy — and temperature is a measure of the
average kinetic energy. Only when the last crystal has melted does the thermometer
start to climb again.

::: definition Specific latent heat
The **specific latent heat** $L$ of a substance is the heat needed to change 1 kg of
it from one phase to another **at constant temperature**:

$$ Q = mL \qquad L = \frac{Q}{m}\ \text{(J kg}^{-1}\text{)} $$

- **Latent heat of fusion** $L_f$: solid → liquid (melting), or liquid → solid
  (freezing, same value released).
- **Latent heat of vaporization** $L_v$: liquid → vapour (boiling or evaporating), or
  vapour → liquid (condensing, same value released).
:::

| Change | Substance | Specific latent heat |
|---|---|---|
| Fusion (melting) | Ice at 0 °C | $3.36\times10^5$ J kg⁻¹ (80 cal g⁻¹) |
| Vaporization | Water at 100 °C | $2.26\times10^6$ J kg⁻¹ (540 cal g⁻¹) |
| Sublimation | Ice → vapour at 0 °C | $2.83\times10^6$ J kg⁻¹ |

Note how large $L_v$ is: boiling 1 g of water takes about 5.4 times as much heat as
heating it from 0 °C to 100 °C. That is why steam is such an effective heating
medium, and why a burn from steam is far worse than a burn from boiling water: the
steam first gives up 2260 J g⁻¹ of latent heat as it condenses on the skin, and only
then does the resulting 100 °C water cool.

**Evaporation versus boiling.** Evaporation happens at *any* temperature, from the
surface only, and cools the remaining liquid (the fastest molecules leave). Boiling
happens at one fixed temperature for a given pressure, throughout the liquid, when
the saturated vapour pressure equals the external pressure. That is why water boils
at about 95 °C in Kathmandu (air pressure ≈ 0.88 atm) and at 71 °C on the summit of
Sagarmatha — and why a pressure cooker, by raising the pressure, raises the boiling
point and cooks dal faster.

### The heating curve

```figure caption="Heat needed to take 1 g of ice from −20 °C to steam at 120 °C. Each plateau is a latent heat: 336 J g⁻¹ for melting and 2260 J g⁻¹ for boiling, during which heat is supplied but the temperature does not change."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.95))
Q = [0,42,42,378,378,798,798,3058,3058,3098]
T = [-20,0,0,0,0,100,100,100,100,120]
ax.plot(Q, T, color=ACCENT, lw=2.0, zorder=3)
ax.axhline(0, color=GRID, lw=0.8)
ax.annotate('melting', xy=(210,1.5), xytext=(210,26), ha='center', va='bottom', fontsize=8.5,
            color=INK, arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.8, mutation_scale=8))
ax.annotate('boiling', xy=(1900,101.5), xytext=(1900,111), ha='center', va='bottom',
            fontsize=8.5, color=INK,
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.8, mutation_scale=8))
ax.text(55, -13, 'ice warms', fontsize=8.5, color=MUTED)
ax.text(720, 18, 'water warms', fontsize=8.5, color=MUTED)
ax.text(3045, 106, 'steam', fontsize=8.5, color=MUTED, ha='right', va='bottom')
ax.set_xlabel('heat supplied to 1 g  (J)'); ax.set_ylabel('temperature  (°C)')
ax.set_xlim(0,3150); ax.set_ylim(-32,135)
ax.set_yticks([-20,0,50,100])
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.5)
```

The curve is the whole of calorimetry in one picture. To find the heat to take a mass
$m$ from one point to another, add up the straight sloped pieces ($mc\Delta T$) and
the flat pieces ($mL$) that lie between them.

### Doing the phase bookkeeping

An ice problem is not one equation but a **decision tree**. Work in this order and
never skip step 2:

1. **Heat available.** How much heat would the warm bodies release if they cooled to
   0 °C? (Include the calorimeter.)
2. **Heat needed to melt all the ice.** $Q = mL_f$. Compare it with step 1.
   - If step 1 < step 2, the final temperature is **0 °C** and some ice survives.
     The answer is "0 °C, with $m_{left} = m - Q_1/L_f$ of ice remaining".
   - If step 1 > step 2, all the ice melts; go on.
3. **Leftover heat.** Subtract the melting heat from the available heat. Use the
   remainder to warm the *whole* final mass — original water plus calorimeter plus
   melted ice — and solve for $\Delta T$.

::: example Worked example 9.6 — ice into water, with the calorimeter
**Problem.** 20 g of ice at 0 °C is dropped into 180 g of water at 30 °C in a
calorimeter of water equivalent 20 g. Find the final temperature.
($c_w = 4200$ J kg⁻¹ K⁻¹, $L_f = 3.36\times10^5$ J kg⁻¹.)

**Solution.**
*Step 1 — heat available if everything cools to 0 °C.* The water plus the
calorimeter behave as 200 g of water:
$Q_1 = 0.200\times4200\times30 = 25\,200$ J.

*Step 2 — heat to melt all the ice.*
$Q_2 = 0.020\times3.36\times10^5 = 6720$ J. Since $6720 < 25\,200$, **all the ice
melts** and the mixture ends above 0 °C.

*Step 3 — warm the final mixture.* Leftover heat
$= 25\,200 - 6720 = 18\,480$ J. The final mass that must be warmed is
$180 + 20 + 20 = 220$ g (original water, calorimeter equivalent, melted ice), so
$\Delta T = \dfrac{18\,480}{0.220\times4200} = \dfrac{18\,480}{924} = 20$ K.

**Answer.** The final temperature is **20 °C**.

Check the balance the other way: the water cools 30 → 20 °C, releasing
$0.200\times4200\times10 = 8400$ J; the ice absorbs $6720$ J to melt and
$0.020\times4200\times20 = 1680$ J to warm to 20 °C, total $8400$ J. It balances.
:::

::: example Worked example 9.7 — ice at −10 °C to steam at 100 °C
**Problem.** How much heat is needed to convert 10 g of ice at −10 °C into steam at
100 °C? ($c_{ice} = 2100$, $c_w = 4200$, $L_f = 3.36\times10^5$,
$L_v = 2.26\times10^6$, all SI.)

**Solution.** Four separate stages, in order:

| Stage | Process | Heat (J) |
|---|---|---|
| 1 | warm the ice −10 → 0 °C | $0.010\times2100\times10 = 210$ |
| 2 | melt the ice at 0 °C | $0.010\times3.36\times10^5 = 3360$ |
| 3 | warm the water 0 → 100 °C | $0.010\times4200\times100 = 4200$ |
| 4 | boil the water at 100 °C | $0.010\times2.26\times10^6 = 22\,600$ |
| | **total** | **30 370 J ≈ 3.04 × 10⁴ J** |

Stage 4 alone is three-quarters of the total. The heat is **not** one $mc\Delta T$:
each stage uses its own specific heat or its own latent heat, and the total is a sum
of four numbers.
:::

::: caution "Steam at 100 °C" is not "water at 100 °C"
A gram of steam at 100 °C contains 2260 J more than a gram of water at 100 °C. Every
statement about "which is hotter" must be about **temperature**; every statement
about "which contains more heat" must count the latent heat. The two are different
questions, and the paper asks both.
:::

### The triple point

::: definition Triple point
The **triple point** of a substance is the unique temperature and pressure at which
its solid, liquid and vapour phases coexist in equilibrium. For water it is

$$ T_3 = 273.16\ \text{K} = 0.01\ ^\circ\text{C}, \qquad
P_3 = 611\ \text{Pa} \approx 4.58\ \text{mm of mercury} $$

At any other pressure only two phases can be in equilibrium at a given temperature
(ice and water at 0 °C and 1 atm, for example).
:::

Why the paper cares about it:

- It is a **single, reproducible fixed point** — one temperature *and* one pressure —
  so it is far better as a thermometer calibration than the melting point, which
  depends on pressure. The kelvin was defined from the triple point of water from
  1954 until the 2019 redefinition of the SI.
- **Melting point ≠ triple point.** Ice melts at 273.15 K (0.00 °C) under 1 atm, but
  at 273.16 K under 611 Pa. The two differ by 0.01 K because the melting point
  depends on pressure.
- The triple point pressure is below atmospheric, so **ice does not sublime at
  1 atm**; it melts. Sublimation of ice is common in the dry, thin air of the
  high Himalayas, where the vapour pressure is very low.

The same idea applies to carbon dioxide, whose triple point is at 5.1 atm — above
atmospheric pressure. That is why "dry ice" does not melt at room pressure: it
sublimes straight to gas.

```photogrid label="9.1" cols="2" ratio="1.2" caption="Linear expansion and the bimetallic strip. (a) A bimetallic strip bends when heated because its two metals expand by different amounts. (b) The change in length is dL = alpha L dT. For strips 1.000 m long and a rise of 100 K, brass (alpha = 19 x 10^-6 per K) grows 1.9 mm, aluminium (23 x 10^-6) 2.3 mm and steel (12 x 10^-6) 1.2 mm. Bonded brass and steel differ by 0.7 mm over this length, so the strip curves with the brass on the outside of the bend. The expansion is a straight line in dT, which is the reason thermostats and fire alarms can be set by temperature."
@ photo id="ioephy/bimetal" cap="A bimetallic strip from an overload relay: two metals bonded together"
fit 1.2
focus 0.5 0.5
@ svg cap="Expansion of 1 m strips for a 100 K rise"
al = {"brass": 19e-6, "aluminium": 23e-6, "steel": 12e-6}
dL = {k: a * 1.0 * 100 * 1000 for k, a in al.items()}
assert abs(dL["brass"] - 1.9) < 1e-9 and abs(dL["aluminium"] - 2.3) < 1e-9 and abs(dL["steel"] - 1.2) < 1e-9
d = dL["brass"] - dL["steel"]; assert abs(d - 0.7) < 1e-9
facts = dict(b="%.1f" % dL["brass"], al="%.1f" % dL["aluminium"], s="%.1f" % dL["steel"], d="%.1f" % d)
f = Fig(300, 236)
f.text(150, 14, "dL = alpha L dT  (L = 1 m, dT = 100 K)", size=10.5, color=NAVY, bold=True)
cols = {"brass": (SAND, AMBER), "aluminium": (BLUE, NAVY), "steel": (MINT, TEAL)}
for i, (k, v) in enumerate(dL.items()):
    y = 28 + i * 34
    f.text(8, y + 12, k, size=10.5, color=SLATE, bold=True, anchor="start", vmid=True)
    f.box(78, y, v * 70, 24, "", fill=cols[k][0], stroke=cols[k][1], r=3); f.text(78 + v * 70 + 6, y + 12, "%.1f mm" % v, size=10.5, color=cols[k][1], bold=True, anchor="start", vmid=True)
f.text(150, 140, "bimetal: brass minus steel = %.1f mm in 1 m" % d, size=10.5, color=RED, bold=True)
X = lambda T: 40 + T * 2.2; Y = lambda dl: 206 - dl * 20
f.line(X(0), Y(0), 270, Y(0), color=SLATE, sw=1.2)
for k in ("brass", "steel"):
    f.line(X(0), Y(0), X(100), Y(al[k] * 1e5), color=cols[k][1], sw=2.2)
f.text(X(100) + 4, Y(1.9) - 4, "brass", size=10.5, color=AMBER, bold=True, anchor="start"); f.text(X(100) + 4, Y(1.2) + 12, "steel", size=10.5, color=TEAL, bold=True, anchor="start")
f.text(X(50), 224, "dT (K): the line is straight", size=10.5, color=SLATE)
```

```photogrid label="9.2" cols="2" ratio="1.2" caption="Latent heat is hidden energy. (a) Steam from a kettle is invisible until it cools and condenses into the white mist we see. (b) The cell compares 10 g of water at 100 degrees C with 10 g of steam at the same temperature, both cooling to skin temperature, 37 degrees C. The water gives out m c dT = 2.63 kJ, but the steam first condenses, giving out m L = 22.6 kJ with the latent heat of vaporisation 2260 kJ/kg, and then cools, so it delivers 25.23 kJ in all, 9.6 times more. This is why a steam burn is far more serious than a burn from boiling water, and why steam is an efficient heating fluid in industry."
@ photo id="ceephy3/kettle" cap="Steam rising from a kettle"
fit 1.2
focus 0.5 0.45
@ svg cap="Why steam burns worse than boiling water"
m, c, Lv = 10.0, 4.18, 2260.0
rows = [("water 60 C", m * c * (60 - 37) / 1000), ("water 100 C", m * c * (100 - 37) / 1000),
        ("steam condenses", m * Lv / 1000), ("steam to 37 C", (m * Lv + m * c * 63) / 1000)]
assert round(rows[1][1], 2) == 2.63 and round(rows[3][1], 2) == 25.23
ratio = rows[3][1] / rows[1][1]
f = Fig(300, 236)
f.text(150, 12, "Heat given to skin by 10 g, kJ", size=10.5, color=NAVY, bold=True)
hbars(f, rows, vmax=27, fmt="%.2f", x0=94, y0=30, bw=130, gap=30,
      colors=[(BLUE, NAVY), (SAND, AMBER), (ROSE, RED), (ROSE, RED)])
f.text(150, 158, "cooling to skin temperature 37 C", size=10, color=SLATE, bold=True)
f.text(150, 180, "water: Q = m c dT = %.2f kJ" % rows[1][1], size=10.5, color=NAVY, bold=True)
f.text(150, 200, "steam: Q = m L + m c dT = %.2f kJ" % rows[3][1], size=10.5, color=NAVY, bold=True)
f.text(150, 218, "steam delivers %.1f times more heat" % ratio, size=10.5, color=RED, bold=True)
facts = dict(w=rows[1][1], s=rows[3][1], r=ratio, lat=rows[2][1])
```

## Formula and fact sheet

| Topic | Formula or fact |
|---|---|
| Linear expansion | $\Delta L = L\alpha\Delta T$; $L' = L(1+\alpha\Delta T)$ |
| Area, volume | $\Delta A = A\beta\Delta T$, $\Delta V = V\gamma\Delta T$ |
| The relation | $\beta = 2\alpha$, $\gamma = 3\alpha$ (isotropic solid, $\alpha\Delta T\ll1$) |
| Units | all three in K⁻¹; α (solids) ~10⁻⁵, γ (liquids) ~10⁻⁴, γ (gases) ~10⁻³ |
| Hole in a plate | grows on heating, exactly as a disc of the same material would |
| Bimetallic strip | bends with the **larger-α** metal on the outside when heated; towards the smaller-α metal |
| Thermal stress | $\sigma = Y\alpha\Delta T$ (compressive on heating), $F = YA\alpha\Delta T$ |
| Pendulum clock | $\dfrac{\Delta T_p}{T_p} = \dfrac{1}{2}\alpha\Delta\theta$; loses time when hot |
| Time lost per day | $\dfrac{1}{2}\alpha\Delta\theta\times86400$ s |
| Real vs apparent | $\gamma_r = \gamma_a + \gamma_v$, with $\gamma_v = 3\alpha_{vessel}$ |
| Overflow | $\Delta V = V(\gamma_r - \gamma_v)\Delta T$ |
| Density on heating | $\rho = \rho_0(1+\gamma\Delta T)^{-1}\approx\rho_0(1-\gamma\Delta T)$ |
| Water anomaly | maximum density 1000 kg m⁻³ at 4 °C; ice 917 kg m⁻³ |
| Heat capacity | $C = Q/\Delta T$ (J K⁻¹); $C = mc$ |
| Specific heat | $Q = mc\Delta T$ (J kg⁻¹ K⁻¹) |
| Water equivalent | $W = m_cc_c/c_w$; heat capacity of calorimeter $= Wc_w$ |
| Method of mixtures | $m_1c_1(\theta_1-\theta) = (m_2c_w + Wc_w)(\theta-\theta_2)$ |
| Latent heat | $Q = mL$ (J kg⁻¹); $L_f = 3.36\times10^5$, $L_v = 2.26\times10^6$ J kg⁻¹ |
| Sublimation | $L_{sub}\approx L_f + L_v$ (with $L_v$ at 0 °C) $= 2.83\times10^6$ J kg⁻¹ |
| Newton's cooling | $\dfrac{dQ}{dt} = k(\theta-\theta_s)$; $\theta-\theta_s = (\theta_0-\theta_s)e^{-Kt}$ |
| Cooling check | $\ln(\theta-\theta_s)$ vs $t$ is a straight line of slope $-K$ |
| Triple point of water | 273.16 K (0.01 °C), 611 Pa (4.58 mm Hg); all three phases coexist |
| Useful constants | 1 cal = 4.2 J; $c_w = 4200$, $c_{ice} = 2100$, $c_{steam} = 2010$ J kg⁻¹ K⁻¹ |

## Chapter summary

- $\Delta L = L\alpha\Delta T$, $\Delta A = A\beta\Delta T$, $\Delta V = V\gamma\Delta T$,
  with $\beta = 2\alpha$ and $\gamma = 3\alpha$ for an isotropic solid. Area takes
  $2\alpha$, volume takes $3\alpha$ — never the other way round.
- A hole or a cavity in a heated plate grows by the same fraction as the metal
  itself; nothing shrinks on heating except water below 4 °C.
- A clamped rod develops $\sigma = Y\alpha\Delta T$, compressive on heating. A
  pendulum clock runs slow when hot, losing $\frac{1}{2}\alpha\Delta\theta$ of its
  time.
- A liquid's real expansion exceeds its apparent expansion by the vessel's:
  $\gamma_r = \gamma_a + \gamma_v$. The level in a warmed vessel first dips (the
  glass grows first) and then rises.
- Water is densest at 4 °C; that is why ice floats, ponds freeze from the top, and
  pipes burst in a hard frost.
- $Q = mc\Delta T$ raises temperature; $Q = mL$ changes phase at constant
  temperature. Never use both for the same stage.
- The calorimeter's water equivalent $W = m_cc_c/c_w$ must be added to the water
  mass. Ignoring it makes the hot body's specific heat come out too low.
- In an ice problem, first compare the heat available with $mL_f$. If the ice cannot
  all melt, the final temperature is 0 °C with ice left over.
- Newton's law of cooling gives exponential cooling; equal temperature drops take
  longer and longer, and the hotter body cools faster.
- The triple point of water is 273.16 K at 611 Pa — the one state where ice, water
  and vapour coexist, and the reason the melting point (273.15 K at 1 atm) is not
  the same number.

## Practice questions

**Set A — Recall (23 questions)**

1. For an isotropic solid, the coefficient of cubical expansion γ is related to the coefficient of linear expansion α by
   (a) γ = α (b) γ = 2α (c) γ = 3α (d) γ = α/3
2. The SI unit of the coefficient of linear expansion is
   (a) m (b) m K⁻¹ (c) J K⁻¹ (d) K⁻¹
3. A circular hole is cut in a metal plate. When the plate is heated, the diameter of the hole
   (a) decreases (b) increases (c) stays the same (d) increases only if the hole is at the centre
4. A bimetallic strip of brass and iron is heated. Brass has the larger α. The strip bends with
   (a) brass on the outer (convex) side (b) iron on the outer side (c) brass on the inner side (d) no bending, since both expand
5. Water has its maximum density at
   (a) 0 °C (b) 2 °C (c) 10 °C (d) 4 °C
6. The SI unit of specific heat capacity is
   (a) J K⁻¹ (b) J kg⁻¹ (c) J kg⁻¹ K⁻¹ (d) kg J⁻¹ K⁻¹
7. The water equivalent of a calorimeter is
   (a) the mass of water with the same heat capacity as the calorimeter (b) the mass of the calorimeter (c) the heat capacity of the calorimeter (d) the mass of water in the calorimeter
8. The specific latent heat of fusion of ice is
   (a) 2.26 × 10⁶ J kg⁻¹ (b) 3.36 × 10⁵ J kg⁻¹ (c) 4.2 × 10³ J kg⁻¹ (d) 3.36 × 10⁴ J kg⁻¹
9. The specific latent heat of vaporization of water at 100 °C is about
   (a) 3.36 × 10⁵ J kg⁻¹ (b) 2.26 × 10⁵ J kg⁻¹ (c) 4.2 × 10³ J kg⁻¹ (d) 2.26 × 10⁶ J kg⁻¹
10. The triple point of water is at
   (a) 273.15 K and 1 atm (b) 273.16 K and 611 Pa (c) 373.15 K and 1 atm (d) 273.16 K and 1 atm
11. At the triple point of a substance
   (a) only the solid and liquid phases coexist (b) only the liquid and vapour phases coexist (c) all three phases coexist in equilibrium (d) the substance has no latent heat
12. If γₐ is the apparent expansivity of a liquid and γᵥ that of its vessel, the real expansivity is
   (a) γₐ + γᵥ (b) γₐ − γᵥ (c) γₐγᵥ (d) γᵥ − γₐ
13. For the same rise in temperature, the cubical expansion is greatest in
   (a) solids (b) liquids (c) gases (d) all the same
14. Newton's law of cooling states that the rate of loss of heat by a body is proportional to
   (a) its absolute temperature (b) the fourth power of its absolute temperature (c) the square of the excess temperature (d) its excess temperature over the surroundings
15. The dimensional formula of the coefficient of linear expansion is
   (a) [K⁻¹] (b) [K] (c) [L K⁻¹] (d) [L⁻¹ K⁻¹]
16. The heat capacity of a body is the heat needed to
   (a) raise unit mass through 1 K (b) raise its temperature by 1 K (c) melt it completely (d) raise it from 0 °C to 100 °C
17. When a liquid in a glass vessel is warmed gently, the level first falls and then rises because
   (a) the liquid contracts at first (b) the liquid evaporates (c) glass has a larger γ than the liquid (d) the vessel expands at first, before the liquid's expansion overtakes it
18. The coefficient of superficial expansion β equals
   (a) α (b) 2α (c) 3α (d) α/2
19. A rod of length L and coefficient α is heated through ΔT. Its increase in length is
   (a) LαΔT (b) Lα/ΔT (c) 2LαΔT (d) 3LαΔT
20. A rod is clamped at both ends and then heated. The stress developed in it is
   (a) zero, because it cannot expand (b) tensile, of magnitude YαΔT (c) compressive, of magnitude YαΔT (d) YΔT/α
21. The principle of calorimetry states that
   (a) the final temperature is the mean of the initial temperatures (b) heat lost by the hot body equals heat gained by the cold body if none escapes (c) the total heat of the system is zero (d) heat flows from the colder to the hotter body
22. Which of the following substances has the highest specific heat capacity?
   (a) copper (b) mercury (c) iron (d) water
23. Two bodies of the same mass need the same heat for the same temperature rise when they have the same
   (a) density (b) volume (c) specific heat capacity (d) thermal conductivity

::: note Answers and explanations — Set A
**1.** (c) — length is one dimension, area two, volume three, so the coefficients go as 1 : 2 : 3. Option (b) is the area coefficient.
**2.** (d) — α is a fractional change of length per kelvin, so the metre cancels and K⁻¹ is left.
**3.** (b) — every linear dimension of the plate grows by the fraction αΔT, and the hole is one of them. A hole behaves like a disc of the same metal.
**4.** (a) — brass lengthens more, so it must form the longer (outer) arc. The strip curves towards the metal with the smaller α.
**5.** (d) — between 0 °C and 4 °C water contracts, and above 4 °C it expands; the turning point is the density maximum.
**6.** (c) — heat per unit mass per kelvin: J/(kg K).
**7.** (a) — the water equivalent is a *mass of water* whose heat capacity equals the calorimeter's. Option (c) is the heat capacity itself, in J K⁻¹.
**8.** (b) — 80 cal g⁻¹ × 4.2 = 336 J g⁻¹ = 3.36 × 10⁵ J kg⁻¹. The 10⁶ value in (a) is the latent heat of vaporization.
**9.** (d) — 540 cal g⁻¹ × 4.2 ≈ 2.26 × 10⁶ J kg⁻¹, about seven times the latent heat of fusion.
**10.** (b) — 273.16 K at 611 Pa. Option (a) is the ordinary melting point at 1 atm.
**11.** (c) — that is the definition: solid, liquid and vapour in equilibrium at one temperature and pressure.
**12.** (a) — the vessel's growth hides part of the liquid's growth, so the real coefficient is the larger one.
**13.** (c) — gases have γ ≈ 3.7 × 10⁻³ K⁻¹, some twenty times a liquid's and a few hundred times a solid's.
**14.** (d) — the driving difference is the body's temperature minus the surroundings'. Option (b) is Stefan's law, which Newton's law approximates for small excess.
**15.** (a) — (1/L)(ΔL/ΔT) = [L]/[L][K] = [K⁻¹].
**16.** (b) — heat capacity is per kelvin for the whole body; per unit mass is the specific heat, option (a).
**17.** (d) — the glass in contact with the warm liquid heats first and its capacity grows before the bulk liquid has expanded much.
**18.** (b) — area is two-dimensional, so β = 2α. Option (c) belongs to volume.
**19.** (a) — the definition of α rearranged: ΔL = LαΔT.
**20.** (c) — the rod would have grown, so it is compressed; the strain αΔT multiplied by Y gives the stress.
**21.** (b) — conservation of energy for an isolated system. The final temperature is a weighted mean, not a simple mean, unless the masses and specific heats are equal.
**22.** (d) — water's 4200 J kg⁻¹ K⁻¹ is about ten times copper's and thirty times mercury's.
**23.** (c) — Q = mcΔT, so equal m, ΔT and Q requires equal c.
:::

**Set B — Understanding (15 questions)**

1. A pendulum clock keeps correct time at 20 °C. On a day when the temperature is 35 °C, the clock
   (a) gains time, because the pendulum shortens (b) loses time, because the pendulum lengthens (c) keeps correct time, because g is unchanged (d) loses time, because g decreases
2. Two rods of the same length are made of metals with α in the ratio 1 : 2. Heated through the same ΔT, the ratio of their increases in length is
   (a) 2 : 1 (b) 1 : 4 (c) 4 : 1 (d) 1 : 2
3. A cube is heated through ΔT. The fractional changes in its length, surface area and volume are in the ratio
   (a) 1 : 2 : 3 (b) 1 : 3 : 2 (c) 3 : 2 : 1 (d) 1 : 1 : 1
4. A bimetallic strip of brass and iron is cooled below room temperature. Compared with its behaviour on heating, it bends
   (a) the same way (b) the opposite way, with brass on the inner side (c) the opposite way, with brass on the outer side (d) not at all
5. The apparent expansion of a liquid in a vessel is found to be zero. This means that
   (a) the liquid and the vessel expand equally (b) the liquid does not expand (c) the vessel does not expand (d) the liquid contracts
6. Ice at 0 °C cools a drink better than the same mass of water at 0 °C because
   (a) ice is colder than water (b) ice has a lower specific heat (c) ice absorbs latent heat as it melts (d) ice has a higher density
7. Steam at 100 °C causes a worse burn than water at 100 °C because steam
   (a) is at a higher temperature (b) has a higher specific heat (c) releases latent heat when it condenses (d) is a gas and spreads faster
8. In a mixture experiment the water equivalent of the calorimeter is ignored. The specific heat calculated for the hot solid will be
   (a) too high (b) too low (c) unaffected (d) exactly zero
9. A solid is heated and its volume increases by 0.3 %. Its density
   (a) increases by 0.3 % (b) decreases by 0.3 % (c) decreases by 0.1 % (d) is unchanged
10. The rate of cooling of a hot body is greatest
   (a) when it is hottest (b) when it is near room temperature (c) at a steady rate throughout (d) only at the moment it reaches room temperature
11. The steel rod of a pendulum clock is replaced by an invar rod of the same length. The clock is now
   (a) almost unaffected by temperature changes (b) more affected by temperature changes (c) slower at every temperature (d) faster at every temperature
12. Two solid spheres of the same metal have radii in the ratio 1 : 2. Heated through the same ΔT, the ratio of the increases in their volumes is
   (a) 1 : 2 (b) 1 : 4 (c) 1 : 6 (d) 1 : 8
13. Water at 0 °C is warmed slowly. Its volume
   (a) increases steadily (b) decreases steadily (c) decreases until 4 °C, then increases (d) increases until 4 °C, then decreases
14. The temperature of a body does not change while it melts, although heat is supplied. The heat supplied
   (a) is lost to the surroundings (b) raises the kinetic energy of the molecules (c) is used only to expand the body (d) raises the potential energy of the molecules
15. Equal masses of water and kerosene (c = 2100 J kg⁻¹ K⁻¹) absorb equal amounts of heat. The rise in temperature of the kerosene is
   (a) half that of the water (b) twice that of the water (c) the same as that of the water (d) four times that of the water

::: note Answers and explanations — Set B
**1.** (b) — a longer pendulum has a longer period T = 2π√(L/g), so each swing takes more time and the clock falls behind. g does not change measurably with the weather.
**2.** (d) — ΔL = LαΔT with L and ΔT the same, so ΔL ∝ α: the ratio is 1 : 2.
**3.** (a) — ΔL/L = αΔT, ΔA/A = 2αΔT, ΔV/V = 3αΔT, so the fractional changes are in the ratio of the dimensions, 1 : 2 : 3.
**4.** (b) — on cooling, brass contracts more than iron, so brass becomes the shorter (inner) surface. The bend reverses direction.
**5.** (a) — γₐ = γᵣ − γᵥ = 0 means γᵣ = γᵥ. The liquid does expand; the vessel expands by exactly as much, so nothing seems to change.
**6.** (c) — melting takes 336 J g⁻¹ of latent heat from the drink before the ice water can warm at all. The temperature of both is 0 °C, so (a) is wrong.
**7.** (c) — condensing steam gives up 2260 J g⁻¹ before the 100 °C water even starts to cool. Both are at the same temperature.
**8.** (b) — the heat actually gained by the cold side is larger than m_w c_w Δθ; ignoring W makes the numerator too small, so c comes out too low.
**9.** (b) — ρ = m/V, so a fractional rise γΔT in volume gives the same fractional fall in density.
**10.** (a) — the rate is proportional to the excess temperature, which is largest at the start. That is why the cooling curve is steepest at the beginning.
**11.** (a) — invar's α is about 1.2 × 10⁻⁶ K⁻¹, ten times smaller than steel's, so the length hardly changes and the clock keeps time in all weathers.
**12.** (d) — volumes go as the cube of the radius, 1 : 8, and ΔV = VγΔT with the same γ and ΔT.
**13.** (c) — water contracts from 0 °C to 4 °C (the anomalous region) and expands above 4 °C, so the volume is least at 4 °C.
**14.** (d) — the heat breaks the bonds of the lattice, increasing the molecules' potential energy. The average kinetic energy, and therefore the temperature, stays the same.
**15.** (b) — Δθ = Q/(mc), so with Q and m equal, Δθ ∝ 1/c: kerosene's c is half of water's, so its rise is twice as large.
:::

**Set C — Application (9 questions)**

1. A steel rail is 1.0 m long at 20 °C (α = 1.2 × 10⁻⁵ K⁻¹). Its increase in length at 70 °C is
   (a) 0.6 mm (b) 0.06 mm (c) 6 mm (d) 0.3 mm
2. A pendulum clock with a steel rod (α = 2 × 10⁻⁵ K⁻¹) keeps correct time at 20 °C. The time it loses in a day at 35 °C is about
   (a) 26 s (b) 6.5 s (c) 1.3 s (d) 13 s
3. A glass vessel (γ = 2.4 × 10⁻⁵ K⁻¹) is filled with a liquid whose apparent expansivity is 1.6 × 10⁻⁴ K⁻¹. The real expansivity of the liquid is
   (a) 1.36 × 10⁻⁴ K⁻¹ (b) 1.6 × 10⁻⁴ K⁻¹ (c) 1.84 × 10⁻⁴ K⁻¹ (d) 4.0 × 10⁻⁵ K⁻¹
4. 100 g of water at 60 °C is mixed with 50 g of water at 20 °C in a calorimeter of water equivalent 10 g. The final temperature is
   (a) 40 °C (b) 45 °C (c) 46.7 °C (d) 50 °C
5. 20 g of ice at 0 °C is dropped into 100 g of water at 40 °C. Neglecting the calorimeter, the final temperature is ($L_f = 3.36\times10^5$ J kg⁻¹)
   (a) 0 °C (b) 10 °C (c) 20 °C (d) 24 °C
6. The heat needed to convert 10 g of ice at −10 °C into steam at 100 °C is ($c_{ice} = 2100$, $c_w = 4200$, $L_f = 3.36\times10^5$, $L_v = 2.26\times10^6$, all SI)
   (a) 7.8 × 10³ J (b) 3.04 × 10⁴ J (c) 2.6 × 10⁴ J (d) 3.0 × 10⁵ J
7. A steel rod (Y = 2 × 10¹¹ Pa, α = 1.2 × 10⁻⁵ K⁻¹) is clamped at both ends and heated through 100 K. The stress set up is
   (a) 1.2 × 10⁸ Pa (b) 2.4 × 10⁶ Pa (c) 4.8 × 10⁸ Pa (d) 2.4 × 10⁸ Pa
8. A body cools from 60 °C to 50 °C in 10 minutes in surroundings at 25 °C. The time it takes to cool from 50 °C to 45 °C is about
   (a) 6.7 min (b) 5.0 min (c) 8.0 min (d) 10 min
9. The mass of ice at 0 °C needed to cool 200 g of water from 50 °C to 0 °C is ($L_f = 3.36\times10^5$ J kg⁻¹)
   (a) 100 g (b) 125 g (c) 150 g (d) 200 g

::: note Answers and explanations — Set C
**1.** (a) — ΔL = 1.0 × 1.2 × 10⁻⁵ × 50 = 6.0 × 10⁻⁴ m = 0.6 mm. Option (b) uses ΔT = 5 K.
**2.** (d) — fractional loss ½αΔθ = ½(2 × 10⁻⁵)(15) = 1.5 × 10⁻⁴; per day 1.5 × 10⁻⁴ × 86400 ≈ 13 s. Option (a) forgets the ½.
**3.** (c) — γᵣ = γₐ + γᵥ = 1.6 × 10⁻⁴ + 0.24 × 10⁻⁴ = 1.84 × 10⁻⁴ K⁻¹. Option (a) subtracts instead of adding.
**4.** (b) — (100 × 60 + 60 × 20)/(100 + 60) = 7200/160 = 45 °C. The 10 g water equivalent must be added to the cold water, not to the hot.
**5.** (c) — heat available = 0.100 × 4200 × 40 = 16 800 J; melting 20 g needs 6720 J, so all the ice melts. Remaining 10 080 J warms 120 g: Δθ = 10 080/(0.120 × 4200) = 20 K, final 20 °C.
**6.** (b) — 210 + 3360 + 4200 + 22 600 = 30 370 J ≈ 3.04 × 10⁴ J. Option (a) omits the boiling stage; (c) counts only the melting and boiling stages.
**7.** (d) — σ = YαΔT = 2 × 10¹¹ × 1.2 × 10⁻⁵ × 100 = 2.4 × 10⁸ Pa, compressive.
**8.** (a) — mean excess 30 K gives 10 K in 10 min; for the next 5 K the mean excess is 22.5 K, so the rate is 0.75 K min⁻¹ and the time is 5/0.75 ≈ 6.7 min. The exponential law gives 6.6 min.
**9.** (b) — heat to remove = 0.200 × 4200 × 50 = 42 000 J; m = 42 000/(3.36 × 10⁵) = 0.125 kg = 125 g.
:::

**Group D — Model answers for long questions (10 marks each, for deeper revision)**

1. Define the coefficients of linear, area and volume expansion, show that $\alpha:\beta:\gamma = 1:2:3$, and explain the anomalous expansion of water. <span class="marks">[10]</span>
2. State the principle of calorimetry, define specific and latent heats and solve a mixture problem with ice. <span class="marks">[10]</span>

```photogrid label="9.H" cols="2" ratio="1.4" caption="Heat and expansion. (a) A bimetallic strip bends when heated because the two metals expand by different amounts, which is how a thermostat switch works. (b) A calorimeter is a thermally insulated vessel used to measure heat exchanged by the principle of calorimetry."
@ photo id="ioephy/bimetal" cap="(a) Bimetallic strip"
fit 1.4
focus 0.5 0.5
@ photo id="ceechem2/calorimeter" cap="(b) Calorimeter"
fit 1.4
focus 0.5 0.5
```

### Model answer D1: thermal expansion of solids and liquids (10 marks)

**Introduction.** Most substances expand on heating because the molecules vibrate with greater amplitude and the average distance between them increases.

**Coefficients.** The coefficient of **linear** expansion is $\alpha = \dfrac{\Delta L}{L\,\Delta\theta}$, of **area** expansion $\beta = \dfrac{\Delta A}{A\,\Delta\theta}$, and of **volume** expansion $\gamma = \dfrac{\Delta V}{V\,\Delta\theta}$. The unit of each is K⁻¹ (or $^{\circ}\text{C}^{-1}$).

**Relation.** For a square plate of side $L$, the new side is $L(1 + \alpha\theta)$, so the new area is $L^2(1 + \alpha\theta)^2 \approx L^2(1 + 2\alpha\theta)$ and $\beta = 2\alpha$. For a cube the volume is $L^3(1 + 3\alpha\theta)$ and $\gamma = 3\alpha$. Hence $\alpha:\beta:\gamma = 1:2:3$.

**Liquids.** A liquid has two coefficients. The **apparent** expansion is what we see relative to the vessel, and the **real** expansion adds the expansion of the vessel: $\gamma_r = \gamma_a + \gamma_g$. The density changes as $\rho' = \rho/(1 + \gamma\theta)$.

**Anomalous expansion of water.** Between $0^{\circ}\text{C}$ and $4^{\circ}\text{C}$ water contracts when heated, so its density is maximum, $1000\ \text{kg m}^{-3}$, at $4^{\circ}\text{C}$. Above $4^{\circ}\text{C}$ it expands normally. In a lake in winter, the surface cools to $4^{\circ}\text{C}$ and sinks; then the surface water cools further and freezes first. Ice floats and insulates the water below, so fish survive.

| Material | $\alpha\ (\text{K}^{-1})$ |
|---|---|
| Steel | $1.2\times10^{-5}$ |
| Aluminium | $2.3\times10^{-5}$ |
| Glass (ordinary) | $0.9\times10^{-5}$ |
| Invar | $\approx 10^{-6}$ |

**Applications and effects.** Gaps in railway tracks and bridges, rivetting hot, fitting an iron tyre on a wheel, the bimetal thermostat and the compensated pendulum of a clock (invar), all use expansion.

**Numerical.** A steel rail $30\ \text{m}$ long at $20^{\circ}\text{C}$ is heated to $50^{\circ}\text{C}$: $\Delta L = 30\times1.2\times10^{-5}\times30 = 1.08\times10^{-2}\ \text{m} = 10.8\ \text{mm}$. If it could not expand, the thermal stress would be $Y\alpha\Delta\theta = 2\times10^{11}\times1.2\times10^{-5}\times30 = 7.2\times10^{7}\ \text{Pa}$.

**Conclusion.** $\gamma = 3\alpha$ for isotropic solids, and water's maximum density at $4^{\circ}\text{C}$ protects aquatic life.

### Model answer D2: calorimetry, specific heat and latent heat (10 marks)

**Introduction.** **Heat** is the energy that flows because of a temperature difference. Its SI unit is joule ($1\ \text{cal} = 4.2\ \text{J}$).

**Definitions.**

1. **Heat capacity** $C = Q/\Delta\theta$ (J K⁻¹).
2. **Specific heat capacity** $c = \dfrac{Q}{m\,\Delta\theta}$ (J kg⁻¹ K⁻¹). For water $c = 4200$, which is high, so water is a good coolant and the sea moderates the climate.
3. **Latent heat** $L = Q/m$ is the heat to change the state at constant temperature. For ice, $L_f = 3.36\times10^5\ \text{J kg}^{-1}$ and for steam, $L_v = 2.26\times10^6\ \text{J kg}^{-1}$.

**Principle of calorimetry.** If no heat is lost, the heat lost by the hot bodies equals the heat gained by the cold bodies. This follows from the conservation of energy.

| Process | Heat formula |
|---|---|
| Temperature change | $Q = mc\,\Delta\theta$ |
| Melting or freezing | $Q = mL_f$ |
| Boiling or condensing | $Q = mL_v$ |
| Water equivalent | $W = mc/c_{water}$ |

**Numerical.** $50\ \text{g}$ of ice at $0^{\circ}\text{C}$ is added to $200\ \text{g}$ of water at $40^{\circ}\text{C}$ in an insulated vessel. Heat needed to melt the ice $= 0.050\times3.36\times10^5 = 16\,800\ \text{J}$. Heat the water can give up in cooling to $0^{\circ}\text{C}$ $= 0.200\times4200\times40 = 33\,600\ \text{J}$, which is more, so all the ice melts. The remaining $16\,800\ \text{J}$ warms the total $250\ \text{g}$: $\Delta\theta = \dfrac{16\,800}{0.250\times4200} = 16^{\circ}\text{C}$. The final temperature is $16^{\circ}\text{C}$.

**Conclusion.** Calorimetry rests on energy conservation. During a change of state the temperature stays constant, because the heat is used to break molecular bonds.
