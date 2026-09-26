---
subject: Chemistry
grade: 11
unit: 7
title: States of Matter
hours: 8
area: General and Physical Chemistry
---

Matter exists in three ordinary states — gas, liquid and solid — and the only
real difference between them is how strongly the particles hold each other
against their own thermal motion. In a gas the motion wins completely; in a
solid the attraction wins completely; a liquid sits between the two. This unit
builds a quantitative model of the gaseous state first, because gases obey
simple laws, and then works down through liquids to solids.

::: key What the examiner asks from this unit
Three things repeat every year: (i) a derivation or statement of the kinetic gas
equation and the gas laws deduced from it, (ii) a numerical on the combined gas
equation, Dalton's law, Graham's law or $PV = nRT$, and (iii) short
definitions — vapour pressure, surface tension, efflorescence, unit cell. Learn
the definitions word-perfect; they are free marks.
:::

## 7.1 Gaseous state: kinetic theory of gas and postulates

The **kinetic molecular theory** explains the behaviour of gases from the motion
of their molecules. It rests on the following postulates.

1. A gas consists of a very large number of extremely small particles
   (molecules). Their own volume is negligible compared with the volume of the
   container, so a gas is mostly empty space.
2. The molecules are in constant, rapid, **random** motion in all directions.
3. The molecules collide with one another and with the walls of the container.
   All collisions are **perfectly elastic** — no kinetic energy is lost.
4. There is **no force of attraction or repulsion** between the molecules.
5. The **pressure** of a gas is the result of the continuous bombardment of the
   molecules on the walls of the container.
6. The **average kinetic energy** of the molecules is directly proportional to
   the absolute temperature, and at a given temperature it is the same for all
   gases, whatever their nature.
7. The effect of gravity on molecular motion is negligible.

From these postulates one can show (the derivation is not required at Grade 11)
that for $N$ molecules each of mass $m$ in a volume $V$,

$$ PV = \frac{1}{3}mNc^{2} $$

where $c$ is the **root-mean-square speed**, $c = \sqrt{\overline{c^{2}}}$. This
is the **kinetic gas equation**. Since the total kinetic energy of the $N$
molecules is $E = \frac{1}{2}mNc^{2}$, the equation can be written
$PV = \frac{2}{3}E$.

::: derivation The root-mean-square speed
For one mole, $mN = M$ (the molar mass) and $PV = RT$. Substituting in the
kinetic gas equation,

$$ RT = \frac{1}{3}Mc^{2} \;\Longrightarrow\; c_{rms} = \sqrt{\frac{3RT}{M}} $$

Because $M = \rho V_m$ and $PV_m = RT$, the same result may be written in terms
of density as $c_{rms} = \sqrt{3P/\rho}$. Also, from $PV = \frac{2}{3}E$ and
$PV = RT$, the kinetic energy of one mole is

$$ E = \frac{3}{2}RT $$

so the average kinetic energy **per molecule** is $\frac{3}{2}kT$, where
$k = R/N_A = 1.38\times10^{-23}\ \text{J K}^{-1}$ is the Boltzmann constant. Note
that $E$ depends only on $T$ — this is postulate 6, now proved.
:::

Not all molecules move at the same speed. The fraction of molecules having a
given speed is given by the **Maxwell–Boltzmann distribution**, which broadens
and flattens as the temperature rises.

```figure caption="Maxwell–Boltzmann speed distribution for nitrogen. Raising the temperature shifts the peak to higher speed and flattens the curve; the area under each curve is the same."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.9))
R = 8.314; M = 0.028
v = np.linspace(0, 1800, 700)
for T, c in [(300, SERIES[0]), (600, SERIES[1]), (1200, SERIES[2])]:
    f = 4*np.pi*(M/(2*np.pi*R*T))**1.5 * v**2 * np.exp(-M*v**2/(2*R*T))
    ax.plot(v, f*1e3, color=c, lw=1.8, label=f'{T} K')
    vmp = np.sqrt(2*R*T/M)
    ax.plot([vmp],[np.interp(vmp, v, f*1e3)], 'o', color=c, ms=4)
ax.set_xlabel('molecular speed  (m s⁻¹)')
ax.set_ylabel('fraction per unit speed  (×10⁻³)')
ax.set_xlim(0,1800)
ax.set_ylim(0, 2.45)
ax.annotate('most probable\nspeed', xy=(422, 1.99), xytext=(520, 2.22),
            fontsize=8.2, color=INK, ha='left', va='top',
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.0, mutation_scale=9))
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.5); ax.legend(title='temperature')
```

Three speeds are quoted for a gas, always in the same order:

| Speed | Expression | Meaning |
|---|---|---|
| Most probable, $c_{mp}$ | $\sqrt{2RT/M}$ | speed of the largest number of molecules |
| Average, $c_{av}$ | $\sqrt{8RT/\pi M}$ | arithmetic mean of all speeds |
| Root mean square, $c_{rms}$ | $\sqrt{3RT/M}$ | used in the kinetic gas equation |

Their ratio is $c_{mp} : c_{av} : c_{rms} = 1 : 1.128 : 1.224$.

## 7.2 Gas laws

**Boyle's law (1662).** At constant temperature, the volume of a fixed mass of
gas is inversely proportional to its pressure.

$$ V \propto \frac{1}{P} \quad (T, n \text{ constant}) \;\Longrightarrow\; P_1V_1 = P_2V_2 $$

A graph of $P$ against $V$ is a rectangular hyperbola (an *isotherm*); a graph of
$P$ against $1/V$ is a straight line through the origin.

```figure caption="Boyle's law for one mole of gas at 273 K. Left: $P$ against $V$ is a hyperbola. Right: $P$ against $1/V$ is a straight line through the origin."
import numpy as np, matplotlib.pyplot as plt
fig, axs = plt.subplots(1, 2, figsize=(5.1,2.5))
V = np.linspace(2, 25, 300); k = 22.4
P = k/V
axs[0].plot(V, P, color=ACCENT, lw=1.9)
axs[0].set_xlabel('volume  V  (L)'); axs[0].set_ylabel('pressure  P  (atm)')
axs[0].set_xlim(0,26); axs[0].set_ylim(0,12)
axs[1].plot(1/V, P, color=SERIES[1], lw=1.9)
axs[1].set_xlabel('1/V  (L⁻¹)'); axs[1].set_ylabel('pressure  P  (atm)')
axs[1].set_xlim(0,0.52); axs[1].set_ylim(0,12)
for a in axs:
    a.spines[['top','right']].set_visible(False)
    a.grid(True, alpha=.5)
fig.tight_layout()
```

**Charles' law (1787).** At constant pressure, the volume of a fixed mass of gas
is directly proportional to its absolute temperature.

$$ V \propto T \quad (P, n \text{ constant}) \;\Longrightarrow\; \frac{V_1}{T_1} = \frac{V_2}{T_2} $$

In the Celsius form, $V_t = V_0\left(1 + \dfrac{t}{273.15}\right)$. Every
$V$–$t$ line, whatever the pressure, extrapolates back to zero volume at
$-273.15\ ^{\circ}\text{C}$. That temperature is **absolute zero**, the zero of
the Kelvin scale.

```figure caption="Charles' law isobars for 1 mol of gas. All lines meet the temperature axis at $-273.15\\ ^{\\circ}$C, which defines absolute zero. Dashed parts are extrapolations — no gas exists there."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.9))
t_real = np.linspace(-100, 200, 200)
t_ext  = np.linspace(-273.15, -100, 120)
for P, c in [(0.5, SERIES[0]), (1.0, SERIES[1]), (2.0, SERIES[2])]:
    Vr = 0.0821*(t_real+273.15)/P
    Ve = 0.0821*(t_ext+273.15)/P
    ax.plot(t_real, Vr, color=c, lw=1.8, label=f'{P} atm')
    ax.plot(t_ext, Ve, color=c, lw=1.2, ls='--', alpha=.8)
ax.axvline(-273.15, color=MUTED, lw=.9, ls=':')
ax.annotate('−273.15 °C', xy=(-273.15, 0), xytext=(-262, 34),
            fontsize=8.4, color=INK)
ax.set_xlabel('temperature  (°C)'); ax.set_ylabel('volume  (L)')
ax.set_xlim(-300, 210); ax.set_ylim(0, 40)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.5); ax.legend(title='pressure')
```

**Gay-Lussac's (pressure) law.** At constant volume, $P \propto T$, so
$P_1/T_1 = P_2/T_2$.

**Avogadro's law (1811).** Equal volumes of all gases, under the same conditions
of temperature and pressure, contain an equal number of molecules. Hence at
constant $T$ and $P$, $V \propto n$. One mole of any gas occupies
$22.4\ \text{L}$ at STP ($0\ ^{\circ}\text{C}$, 1 atm).

**Combined gas equation.** Putting Boyle's and Charles' laws together for a fixed
mass of gas,

$$ \frac{P_1V_1}{T_1} = \frac{P_2V_2}{T_2} $$

::: example Worked example 7.1 — combined gas equation
**Problem.** A gas occupies $300\ \text{cm}^3$ at $27\ ^{\circ}\text{C}$ and
$380\ \text{mm Hg}$. What volume will it occupy at STP?

**Solution.** Convert temperatures to kelvin first.

$T_1 = 27 + 273 = 300\ \text{K}$, $P_1 = 380\ \text{mm}$, $V_1 = 300\ \text{cm}^3$;
$T_2 = 273\ \text{K}$, $P_2 = 760\ \text{mm}$.

$$ V_2 = \frac{P_1V_1T_2}{T_1P_2} = \frac{380 \times 300 \times 273}{300 \times 760} $$

$$ V_2 = \frac{31122000}{228000} = 136.5\ \text{cm}^{3} $$

The volume falls, as expected: the pressure has doubled while the temperature
has only dropped slightly.
:::

**Dalton's law of partial pressures.** The total pressure of a mixture of gases
that do not react is the sum of the partial pressures of the component gases:

$$ P_{total} = p_1 + p_2 + p_3 + \cdots $$

The partial pressure of a component is the pressure it would exert if it alone
occupied the whole volume. In terms of mole fraction $x_i$,

$$ p_i = x_i \, P_{total} $$

The commonest use is correcting for water vapour when a gas is collected over
water: $p_{dry\ gas} = P_{atm} - p_{water\ vapour}$ (the *aqueous tension*).

**Graham's law of diffusion (1833).** At constant temperature and pressure, the
rate of diffusion (or effusion) of a gas is inversely proportional to the square
root of its density, and therefore of its molar mass:

$$ r \propto \frac{1}{\sqrt{d}} \;\Longrightarrow\; \frac{r_1}{r_2} = \sqrt{\frac{d_2}{d_1}} = \sqrt{\frac{M_2}{M_1}} $$

::: caution Rate is not volume
Graham's law compares **rates**, not volumes. If different volumes diffuse in
different times you must first form $r = V/t$ for each gas. Writing
$V_1/V_2 = \sqrt{M_2/M_1}$ when the times differ is the standard lost mark.
:::

::: example Worked example 7.2 — Graham's law
**Problem.** $120\ \text{cm}^3$ of a gas diffuses through a porous plug in
$20\ \text{s}$, while $180\ \text{cm}^3$ of oxygen diffuses through the same plug
in $15\ \text{s}$ under identical conditions. Calculate the molar mass of the gas.

**Solution.** Form the rates first.

$$ r_{gas} = \frac{120}{20} = 6\ \text{cm}^3\text{s}^{-1}, \qquad
r_{O_2} = \frac{180}{15} = 12\ \text{cm}^3\text{s}^{-1} $$

By Graham's law,

$$ \frac{r_{gas}}{r_{O_2}} = \sqrt{\frac{M_{O_2}}{M_{gas}}}
\;\Longrightarrow\; \frac{6}{12} = \sqrt{\frac{32}{M_{gas}}} $$

Squaring, $\dfrac{1}{4} = \dfrac{32}{M_{gas}}$, so
$M_{gas} = 128\ \text{g mol}^{-1}$. (Hydrogen iodide, HI, has a molar mass of
127.9 — the gas is almost certainly HI.)
:::

## 7.3 Ideal gas and ideal gas equation; universal gas constant and its significance

An **ideal gas** is a hypothetical gas that obeys Boyle's law, Charles' law and
Avogadro's law exactly at all temperatures and pressures. Its molecules have no
volume of their own and exert no attractive force on one another. No real gas is
ideal, but real gases approach ideal behaviour at **low pressure and high
temperature**.

Combining the three laws for $n$ moles gives the **ideal gas equation**:

$$ V \propto \frac{nT}{P} \;\Longrightarrow\; PV = nRT $$

Since $n = w/M$ (mass over molar mass), two very useful working forms follow:

$$ PV = \frac{w}{M}RT, \qquad M = \frac{\rho RT}{P} \quad \text{where } \rho = w/V $$

$R$ is the **universal (molar) gas constant** — universal because its value is
the same for every gas.

| Units of $P$ and $V$ | Value of $R$ |
|---|---|
| Pa, m³ (SI) | $8.314\ \text{J K}^{-1}\text{mol}^{-1}$ |
| atm, litre | $0.0821\ \text{L atm K}^{-1}\text{mol}^{-1}$ |
| mm Hg, litre | $62.4\ \text{L mm Hg K}^{-1}\text{mol}^{-1}$ |
| calorie (energy) | $1.987 \approx 2\ \text{cal K}^{-1}\text{mol}^{-1}$ |

**Significance of $R$.** $R = PV/nT$, and pressure × volume has the dimensions of
energy (force per area × volume = force × distance). So $R$ is an *energy per
mole per kelvin*. Physically, $R$ is the **work done by one mole of an ideal gas
when its temperature is raised by one kelvin at constant pressure**.

::: example Worked example 7.3 — molar mass from the ideal gas equation
**Problem.** $0.30\ \text{g}$ of a volatile liquid, on complete vaporisation,
occupies $100\ \text{cm}^3$ at $27\ ^{\circ}\text{C}$ and $1\ \text{atm}$.
Calculate its molar mass. ($R = 0.0821\ \text{L atm K}^{-1}\text{mol}^{-1}$)

**Solution.** Work in litres and kelvin: $V = 0.100\ \text{L}$, $T = 300\ \text{K}$.

$$ n = \frac{PV}{RT} = \frac{1 \times 0.100}{0.0821 \times 300} = \frac{0.100}{24.63} = 4.06\times10^{-3}\ \text{mol} $$

$$ M = \frac{w}{n} = \frac{0.30}{4.06\times10^{-3}} = 73.9 \approx 74\ \text{g mol}^{-1} $$

A molar mass of 74 fits butan-1-ol, C₄H₉OH.
:::

## 7.4 Deviation of real gas from ideality

Real gases obey $PV = nRT$ only approximately. The deviation is measured by the
**compressibility factor**

$$ Z = \frac{PV}{nRT} $$

For an ideal gas $Z = 1$ at every pressure. For real gases:

- At **low pressure**, $Z < 1$ for most gases — the gas is *more* compressible
  than ideal, because intermolecular attractions pull the molecules together.
- At **high pressure**, $Z > 1$ for all gases — the gas is *less* compressible
  than ideal, because the molecules' own volume can no longer be ignored and
  short-range repulsion dominates.
- Hydrogen and helium have $Z > 1$ at all pressures at room temperature: their
  attractive forces are too weak to matter.

```figure caption="Compressibility factor $Z$ against pressure at 320 K, computed from the van der Waals equation. The dotted line $Z = 1$ is the ideal gas."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.9))
R, T = 0.0821, 320.0
gases = [('H₂', 0.244, 0.0266), ('N₂', 1.39, 0.0391),
         ('CH₄', 2.25, 0.0428), ('CO₂', 3.59, 0.0427)]
Vm = np.logspace(np.log10(0.06), np.log10(80), 8000)[::-1]
for i, (name, a, b) in enumerate(gases):
    P = R*T/(Vm-b) - a/Vm**2
    Z = P*Vm/(R*T)
    drop = np.where(np.diff(P) <= 0)[0]          # cut the unphysical vdW loop
    stop = drop[0]+1 if len(drop) else len(P)
    P, Z = P[:stop], Z[:stop]
    m = (P > 0) & (P <= 600)
    ax.plot(P[m], Z[m], color=SERIES[i], lw=1.8, label=name)
ax.axhline(1.0, color=MUTED, lw=1.0, ls=':')
ax.annotate('ideal gas', xy=(500, 1.0), xytext=(430, 0.70), fontsize=8.2,
            color=MUTED)
ax.set_xlabel('pressure  P  (atm)'); ax.set_ylabel('Z = PV/nRT')
ax.set_xlim(0, 600); ax.set_ylim(0, 2.0)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.5); ax.legend(ncol=4, columnspacing=1.0, loc='upper left')
```

The deviation arises because two of the postulates are false for a real gas:
molecules **do** attract one another, and they **do** occupy volume. Van der
Waals corrected the ideal gas equation for both:

$$ \left(P + \frac{an^{2}}{V^{2}}\right)(V - nb) = nRT $$

- $an^{2}/V^{2}$ is the **pressure correction**. A molecule about to strike the
  wall is pulled back by its neighbours, so the observed pressure is less than
  the ideal one. The constant $a$ measures the strength of attraction; its unit
  is atm L² mol⁻².
- $nb$ is the **volume correction** (the *excluded volume*). The space actually
  available to the molecules is less than $V$. The constant $b$ is about four
  times the actual volume of one mole of molecules; its unit is L mol⁻¹.

Gases that are easily liquefied (CO₂, NH₃, SO₂) have large $a$; permanent gases
(H₂, He, N₂) have small $a$. The temperature at which a real gas obeys Boyle's
law over an appreciable range of pressure is its **Boyle temperature**,
$T_B = a/Rb$.

## 7.5 Liquid state

### Evaporation and condensation

**Evaporation** is the escape of molecules from the *surface* of a liquid into
the vapour phase, and it happens at *all* temperatures. Only the fastest surface
molecules have enough energy to break free, so the molecules left behind have a
lower average kinetic energy — which is why **evaporation causes cooling**. It
is an endothermic, surface phenomenon. It is faster when the temperature is
higher, the surface area is larger, the air is dry and moving, and the
intermolecular forces are weak.

**Condensation** is the reverse: vapour molecules returning to the liquid. In a
closed vessel the two rates soon become equal and a dynamic equilibrium is
reached.

### Vapour pressure and boiling point

::: definition Vapour pressure
The **vapour pressure** of a liquid is the pressure exerted by its vapour when
the vapour is in dynamic equilibrium with the liquid at a given temperature.
:::

Vapour pressure increases rapidly with temperature and is larger for liquids with
weaker intermolecular forces (ether > ethanol > water > mercury). It does **not**
depend on the surface area of the liquid or on the amount of liquid present.

::: definition Boiling point
The **boiling point** of a liquid is the temperature at which its vapour pressure
becomes equal to the external (atmospheric) pressure. When the external pressure
is 1 atm (760 mm Hg) it is called the *normal boiling point*.
:::

This explains a familiar Nepali experience. In Kathmandu, about 1,350 m above sea
level, atmospheric pressure is roughly 86 kPa instead of 101 kPa, so water boils
near $95\ ^{\circ}\text{C}$ and rice takes longer to cook. Higher up, at Namche
Bazaar (3,440 m), water boils at about $89\ ^{\circ}\text{C}$. A pressure cooker
solves the problem by raising the pressure above the liquid, which raises the
boiling point to about $120\ ^{\circ}\text{C}$.

### Surface tension and viscosity

A molecule inside a liquid is pulled equally in all directions, but a molecule at
the surface is pulled only sideways and inwards. The surface therefore behaves
like a stretched elastic skin.

::: definition Surface tension
**Surface tension** ($\gamma$) is the force acting at right angles to a line of
unit length drawn on the surface of a liquid. Its SI unit is N m⁻¹ (equivalently
J m⁻², energy per unit surface area).
:::

Surface tension explains why raindrops and mercury droplets are spherical (a
sphere has the least surface area for a given volume), why a needle can float on
water, why water rises in a narrow capillary, and why insects can walk on a
pond. It **decreases** as temperature rises (molecular motion weakens the
attractions) and falls sharply when a detergent or soap is added — which is why
soapy water wets cloth and cleans it.

::: definition Viscosity
**Viscosity** is the resistance offered by a liquid to its own flow, caused by
internal friction between adjacent layers. The coefficient of viscosity $\eta$
has the SI unit N s m⁻² (pascal second); the CGS unit is the poise
($1\ \text{P} = 0.1\ \text{Pa s}$).
:::

Viscosity increases with stronger intermolecular forces and with larger, more
tangled molecules — glycerol and honey are far more viscous than water, and
water is more viscous than petrol. Unlike gases, the viscosity of a liquid
**decreases** as the temperature rises, which is why engine oil thins in summer.

## 7.6 Liquid crystals and their applications

Some organic substances with long, rod-shaped molecules do not melt directly
from a solid to a normal liquid. Between the two they pass through a cloudy
intermediate state that **flows like a liquid but keeps some of the molecular
order of a crystal**. This state is called the **liquid crystal** or *mesophase*.
It was discovered in 1888 by Friedrich Reinitzer in cholesteryl benzoate, which
melts at $145\ ^{\circ}\text{C}$ to a turbid liquid and becomes a clear liquid
only at $179\ ^{\circ}\text{C}$.

```figure caption="Molecular arrangement in the solid, the two common thermotropic mesophases and the ordinary liquid. Order is lost step by step as the temperature rises."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.1,2.5))
rng = np.random.default_rng(7)
def rod(x, y, ang, c):
    L = 0.23
    dx, dy = L*np.cos(ang), L*np.sin(ang)
    ax.plot([x-dx, x+dx], [y-dy, y+dy], color=c, lw=2.0, solid_capstyle='round')
panels = ['Crystalline solid', 'Smectic', 'Nematic', 'Isotropic liquid']
for p in range(4):
    x0 = p*2.6
    for r in range(4):
        for cnum in range(4):
            if p == 0:
                x, y, ang = x0+0.28+cnum*0.52, 0.45+r*0.62, np.pi/2
            elif p == 1:
                x = x0+0.28+cnum*0.52 + rng.uniform(-0.06,0.06)
                y = 0.45+r*0.62
                ang = np.pi/2 + rng.uniform(-0.16,0.16)
            elif p == 2:
                x = x0+0.28+cnum*0.52 + rng.uniform(-0.14,0.14)
                y = 0.45+r*0.62 + rng.uniform(-0.22,0.22)
                ang = np.pi/2 + rng.uniform(-0.38,0.38)
            else:
                x = x0+0.28+rng.uniform(0,1.7); y = 0.35+rng.uniform(0,2.4)
                ang = rng.uniform(0, np.pi)
            rod(x, y, ang, SERIES[p])
    ax.text(x0+1.05, -0.28, panels[p], ha='center', fontsize=8.6, color=INK)
ax.annotate('', xy=(10.3,3.35), xytext=(0.1,3.35),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.1, mutation_scale=11))
ax.text(5.2, 3.48, 'increasing temperature  →  decreasing order',
        ha='center', fontsize=8.4, color=MUTED)
ax.set_xlim(-0.2, 10.5); ax.set_ylim(-0.7, 3.8)
ax.axis('off')
```

**Types of liquid crystals**

| Class | Driven by | Sub-types and description |
|---|---|---|
| Thermotropic | temperature | **Nematic** — molecules parallel but not in layers; **Smectic** — parallel *and* arranged in layers; **Cholesteric** (chiral nematic) — layers whose direction twists from layer to layer, giving bright colours |
| Lyotropic | concentration in a solvent | soap and detergent solutions, cell membranes, phospholipid bilayers |

**Applications**

- **Liquid crystal displays (LCDs)** in calculators, digital watches, laptops,
  mobile phones and televisions. A small voltage twists the nematic molecules and
  changes how they transmit polarised light, so a segment turns dark.
- **Thermometers and temperature strips.** Cholesteric liquid crystals reflect a
  colour that depends on temperature — used in forehead thermometers, aquarium
  strips and mood rings.
- **Medical diagnosis.** A liquid-crystal film on the skin maps surface
  temperature and can reveal tumours or blocked veins, which are warmer.
- **Non-destructive testing.** Films placed on electronic circuit boards or
  pipes reveal hot spots and cracks.
- Optical shutters, pressure sensors and some drug-delivery systems.

## 7.7 Solid state: types of solids; amorphous and crystalline solids

In a solid the particles occupy fixed mean positions and can only vibrate, so a
solid has a definite shape and volume and is nearly incompressible. Solids are of
two kinds.

| Property | Crystalline solid | Amorphous solid |
|---|---|---|
| Arrangement of particles | long-range regular order | only short-range order |
| Melting point | sharp, definite | melts over a range; softens gradually |
| Geometry | definite geometrical shape, plane faces | irregular shape |
| Heat of fusion | definite | not definite |
| Cutting | clean cleavage along planes | irregular breakage |
| Physical properties | **anisotropic** (vary with direction) | **isotropic** (same in all directions) |
| Nature | true solids | pseudo-solids / supercooled liquids |
| Examples | NaCl, diamond, quartz, ice, sugar | glass, rubber, plastic, fused silica, coal tar |

Crystalline solids are further classified by the kind of particle at the lattice
points and the force holding them together.

| Type | Particles | Binding force | Examples | Typical properties |
|---|---|---|---|---|
| Ionic | cations and anions | strong electrostatic | NaCl, KNO₃, ZnS | hard, brittle, high m.p., conduct when molten or aqueous |
| Covalent (network) | atoms | covalent bonds throughout | diamond, SiO₂, SiC | extremely hard, very high m.p., non-conducting (graphite is the exception) |
| Molecular | molecules | van der Waals or H-bonds | I₂, dry ice (CO₂), ice, S₈ | soft, low m.p., volatile, insulators |
| Metallic | metal ions in a sea of electrons | metallic bond | Cu, Fe, Na, Al | malleable, ductile, lustrous, good conductors |

## 7.8 Efflorescent, deliquescent and hygroscopic solids

| Term | Behaviour in air | Result | Examples |
|---|---|---|---|
| **Efflorescent** | *loses* its water of crystallization to the atmosphere | crystal becomes dull and powdery | Na₂CO₃·10H₂O, Na₂SO₄·10H₂O, FeSO₄·7H₂O, MgSO₄·7H₂O |
| **Deliquescent** | *absorbs* so much moisture that it dissolves in it | solid turns into a solution | CaCl₂, NaOH, KOH, MgCl₂, FeCl₃, ZnCl₂ |
| **Hygroscopic** | *absorbs* moisture but does **not** dissolve in it | solid stays solid, merely damp | CaO (quicklime), silica gel, anhydrous CuSO₄, P₄O₁₀, conc. H₂SO₄ (a liquid) |

Efflorescence happens when the vapour pressure of the hydrate is *greater* than
the partial pressure of water vapour in the air; deliquescence happens when the
saturated solution of the salt has a vapour pressure *lower* than that of the
air. Deliquescent and hygroscopic substances are used as **drying agents**
(desiccators, drying towers) — anhydrous CaCl₂ for most gases, quicklime for
ammonia, concentrated H₂SO₄ for acidic and neutral gases.

::: caution Deliquescent versus hygroscopic
Both absorb water. The difference is what happens next: a **deliquescent** solid
*dissolves* in the water it absorbs and ends up as a puddle of solution; a
**hygroscopic** solid only becomes damp. Every deliquescent substance is
hygroscopic, but not every hygroscopic substance is deliquescent.
:::

## 7.9 Crystallization and crystal growth; water of crystallization

**Crystallization** is the process of obtaining pure crystals of a solid from its
hot saturated solution (or from a melt). It is the standard laboratory method of
purifying a solid, and the industrial method of making sugar, common salt, alum
and copper sulphate. The steps are:

1. Dissolve the impure solid in the **minimum amount of hot solvent** to make a
   saturated solution.
2. **Filter hot** to remove insoluble impurities.
3. **Cool slowly**. The solution becomes supersaturated and crystals separate;
   soluble impurities remain in the mother liquor.
4. Filter the crystals, wash with a little cold solvent and dry between filter
   papers.

**Crystal growth** happens in two stages. First **nucleation**: a few particles
come together to form a tiny nucleus. Then **growth**: further particles deposit
on the faces of the nucleus in a regular pattern. Slow cooling and an
undisturbed solution give a few large, well-formed crystals; rapid cooling or
stirring gives many small ones. Dropping in a tiny **seed crystal** starts the
process where nucleation is slow.

::: definition Water of crystallization
The **water of crystallization** is the definite number of water molecules
chemically combined with one formula unit of a substance in its crystalline
state. It gives the crystal its shape and often its colour; on heating it is
driven off and the crystal crumbles.
:::

CuSO₄·5H₂O --Δ--> CuSO₄ + 5H₂O  (blue crystals → white powder)

| Common name | Formula | Water molecules |
|---|---|---|
| Blue vitriol | CuSO₄·5H₂O | 5 |
| Green vitriol | FeSO₄·7H₂O | 7 |
| White vitriol | ZnSO₄·7H₂O | 7 |
| Washing soda | Na₂CO₃·10H₂O | 10 |
| Glauber's salt | Na₂SO₄·10H₂O | 10 |
| Gypsum | CaSO₄·2H₂O | 2 |
| Epsom salt | MgSO₄·7H₂O | 7 |
| Borax | Na₂B₄O₇·10H₂O | 10 |
| Mohr's salt | FeSO₄·(NH₄)₂SO₄·6H₂O | 6 |
| Potash alum | K₂SO₄·Al₂(SO₄)₃·24H₂O | 24 |

::: example Worked example 7.4 — finding the water of crystallization
**Problem.** A hydrated salt MgSO₄·xH₂O loses $51.2\ \%$ of its mass when heated
to constant weight. Find $x$. (Mg = 24, S = 32, O = 16, H = 1)

**Solution.** Formula mass of anhydrous MgSO₄ $= 24 + 32 + 4(16) = 120$.
Formula mass of the hydrate $= 120 + 18x$. The mass lost is the water, so

$$ \frac{18x}{120 + 18x} \times 100 = 51.2 $$

$$ 1800x = 51.2(120) + 51.2(18x) = 6144 + 921.6x $$

$$ 878.4x = 6144 \;\Longrightarrow\; x = 6.99 \approx 7 $$

The salt is MgSO₄·7H₂O, Epsom salt. **Check:** $18(7)/246 = 51.2\ \%$. ✔
:::

## 7.10 Introduction to unit crystal lattice and unit cell

::: definition Crystal lattice and unit cell
A **crystal (space) lattice** is the regular three-dimensional arrangement of
points in space that represents the positions of the constituent particles of a
crystal. A **unit cell** is the smallest repeating portion of the lattice which,
when repeated in three dimensions, generates the whole crystal.
:::

A unit cell is described by six **cell parameters**: the three edge lengths
$a$, $b$, $c$ and the three angles $\alpha$ (between $b$ and $c$), $\beta$
(between $a$ and $c$) and $\gamma$ (between $a$ and $b$). Different combinations
give exactly **seven crystal systems**, which in turn give 14 Bravais lattices.

| Crystal system | Edges | Angles | Example |
|---|---|---|---|
| Cubic | $a=b=c$ | $\alpha=\beta=\gamma=90^{\circ}$ | NaCl, Cu, diamond |
| Tetragonal | $a=b\ne c$ | $\alpha=\beta=\gamma=90^{\circ}$ | SnO₂, white tin |
| Orthorhombic | $a\ne b\ne c$ | $\alpha=\beta=\gamma=90^{\circ}$ | rhombic sulphur, KNO₃ |
| Monoclinic | $a\ne b\ne c$ | $\alpha=\gamma=90^{\circ},\ \beta\ne90^{\circ}$ | monoclinic sulphur, Na₂SO₄·10H₂O |
| Triclinic | $a\ne b\ne c$ | all $\ne 90^{\circ}$ | CuSO₄·5H₂O, K₂Cr₂O₇ |
| Hexagonal | $a=b\ne c$ | $\alpha=\beta=90^{\circ},\ \gamma=120^{\circ}$ | graphite, ZnO |
| Rhombohedral | $a=b=c$ | $\alpha=\beta=\gamma\ne90^{\circ}$ | calcite, cinnabar |

Within the cubic system there are three important unit cells.

```figure caption="The three cubic unit cells. Corner atoms are shared between 8 cells, face atoms between 2, and the body-centre atom belongs to one cell alone."
import numpy as np, matplotlib.pyplot as plt
fig, axs = plt.subplots(1, 3, figsize=(5.1,2.2))
def proj(p):
    x, y, z = p
    return x + 0.40*z, y + 0.34*z
corners = [(x,y,z) for x in (0,1) for y in (0,1) for z in (0,1)]
edges = [(p,q) for i,p in enumerate(corners) for q in corners[i+1:]
         if sum(abs(np.array(p)-np.array(q))) == 1]
titles = ['Simple cubic\nZ = 1', 'Body-centred\nZ = 2', 'Face-centred\nZ = 4']
extra = [[], [(0.5,0.5,0.5)],
         [(0.5,0.5,0),(0.5,0.5,1),(0.5,0,0.5),(0.5,1,0.5),(0,0.5,0.5),(1,0.5,0.5)]]
for k, ax in enumerate(axs):
    for p,q in edges:
        X = [proj(p)[0], proj(q)[0]]; Y = [proj(p)[1], proj(q)[1]]
        ax.plot(X, Y, color=MUTED, lw=0.9, zorder=1)
    for p in corners:
        X, Y = proj(p)
        ax.plot([X],[Y],'o', color=ACCENT, ms=8, zorder=3)
    for p in extra[k]:
        X, Y = proj(p)
        ax.plot([X],[Y],'o', color=SERIES[1], ms=8, zorder=4)
    ax.set_title(titles[k], fontsize=8.6)
    ax.set_xlim(-0.25, 1.65); ax.set_ylim(-0.25, 1.6)
    ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout()
```

A particle sitting on a corner, edge or face is shared with neighbouring cells,
so only a fraction of it belongs to the cell being counted.

| Position of particle | Shared between | Contribution to one cell |
|---|---|---|
| Corner | 8 cells | 1/8 |
| Edge | 4 cells | 1/4 |
| Face centre | 2 cells | 1/2 |
| Body centre | 1 cell | 1 |

Hence the number of particles per unit cell, $Z$:

- **Simple (primitive) cubic:** $8 \times \tfrac{1}{8} = 1$
- **Body-centred cubic (bcc):** $8 \times \tfrac{1}{8} + 1 = 2$
- **Face-centred cubic (fcc):** $8 \times \tfrac{1}{8} + 6 \times \tfrac{1}{2} = 4$
- **End-centred:** $8 \times \tfrac{1}{8} + 2 \times \tfrac{1}{2} = 2$

::: example Worked example 7.5 — from the unit cell to density
**Problem.** Copper crystallises in a face-centred cubic lattice with edge length
$a = 3.61\times10^{-8}\ \text{cm}$. Calculate the number of atoms per unit cell
and the density of copper. (Cu $= 63.5\ \text{g mol}^{-1}$,
$N_A = 6.022\times10^{23}$)

**Solution.** For fcc, $Z = 8\left(\tfrac{1}{8}\right) + 6\left(\tfrac{1}{2}\right) = 1 + 3 = 4$ atoms.

Volume of the unit cell:

$$ a^{3} = (3.61\times10^{-8})^{3} = 4.705\times10^{-23}\ \text{cm}^{3} $$

Mass of the unit cell $= Z \times$ (mass of one atom) $= ZM/N_A$:

$$ \rho = \frac{ZM}{a^{3}N_A} = \frac{4 \times 63.5}{4.705\times10^{-23} \times 6.022\times10^{23}} $$

$$ \rho = \frac{254}{28.34} = 8.96\ \text{g cm}^{-3} $$

This matches the measured density of copper, which confirms the fcc structure.
:::

## Chapter summary

- Kinetic gas equation: $PV = \frac{1}{3}mNc^{2}$, giving
  $c_{rms} = \sqrt{3RT/M} = \sqrt{3P/\rho}$ and kinetic energy per mole
  $E = \frac{3}{2}RT$.
- Gas laws: Boyle $P_1V_1 = P_2V_2$; Charles $V_1/T_1 = V_2/T_2$; combined
  $P_1V_1/T_1 = P_2V_2/T_2$; Dalton $P = \sum p_i$ with $p_i = x_iP$; Graham
  $r_1/r_2 = \sqrt{M_2/M_1}$.
- Ideal gas equation $PV = nRT = (w/M)RT$, so $M = \rho RT/P$;
  $R = 8.314\ \text{J K}^{-1}\text{mol}^{-1} = 0.0821\ \text{L atm K}^{-1}\text{mol}^{-1}$,
  the work done by one mole per kelvin at constant pressure.
- Real gases deviate because molecules attract and occupy volume:
  $Z = PV/nRT \ne 1$, and $\left(P + an^{2}/V^{2}\right)(V-nb) = nRT$.
- Vapour pressure rises with temperature; a liquid boils when its vapour
  pressure equals the external pressure. Surface tension ($\gamma$, N m⁻¹) and
  viscosity ($\eta$, Pa s) both fall as temperature rises.
- Liquid crystals are mesophases: thermotropic (nematic, smectic, cholesteric)
  and lyotropic; used in LCDs, thermometers and medical thermography.
- Crystalline solids are anisotropic with sharp melting points; amorphous solids
  are isotropic pseudo-solids. Efflorescent solids lose water, deliquescent
  solids dissolve in absorbed water, hygroscopic solids merely absorb it.
- A unit cell is the smallest repeating unit of a crystal lattice; corner
  contributes 1/8, face 1/2, body 1, giving $Z = 1$ (sc), 2 (bcc), 4 (fcc), and
  $\rho = ZM/a^{3}N_A$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. At constant temperature, the graph of pressure against $1/V$ for a fixed mass of gas is <span class="marks">[1]</span>
   (a) a hyperbola (b) a straight line through the origin (c) a parabola (d) a horizontal line
2. The value of the universal gas constant in SI units is <span class="marks">[1]</span>
   (a) 0.0821 (b) 1.987 (c) 8.314 (d) 62.4
3. Which of the following is a deliquescent substance? <span class="marks">[1]</span>
   (a) Na₂CO₃·10H₂O (b) CaCl₂ (c) CaO (d) CuSO₄·5H₂O
4. The number of atoms per unit cell in a face-centred cubic lattice is <span class="marks">[1]</span>
   (a) 1 (b) 2 (c) 4 (d) 8
5. Amorphous solids are <span class="marks">[1]</span>
   (a) anisotropic with a sharp melting point (b) isotropic with a sharp melting point
   (c) anisotropic with no sharp melting point (d) isotropic with no sharp melting point

::: note Answers to Group A
**1.** (b) — Boyle's law gives $P = k(1/V)$, of the form $y = mx$.
**2.** (c) — $8.314\ \text{J K}^{-1}\text{mol}^{-1}$; 0.0821 is in L atm units.
**3.** (b) — CaCl₂ absorbs moisture and dissolves in it; CaO only becomes damp (hygroscopic).
**4.** (c) — $8(1/8) + 6(1/2) = 4$.
**5.** (d) — no long-range order, so properties are the same in all directions and they soften over a range.
:::

**Group B — Short answer (5 marks each)**

1. State the postulates of the kinetic molecular theory of gases and write the
   kinetic gas equation, explaining each term. <span class="marks">[5]</span>
2. Define vapour pressure and boiling point. Explain why water boils at about
   $95\ ^{\circ}\text{C}$ in Kathmandu but at $100\ ^{\circ}\text{C}$ in Biratnagar. <span class="marks">[5]</span>
3. A closed vessel contains 4 g of hydrogen and 64 g of oxygen at a total
   pressure of 1.5 atm. Calculate the partial pressure of each gas.
   (H = 1, O = 16) <span class="marks">[5]</span>
4. Distinguish between crystalline and amorphous solids, giving two examples of
   each. <span class="marks">[5]</span>
5. Calculate the volume occupied by 4.4 g of carbon dioxide at
   $27\ ^{\circ}\text{C}$ and 2 atm pressure.
   ($R = 0.0821\ \text{L atm K}^{-1}\text{mol}^{-1}$) <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Give the seven postulates of §7.1, then $PV = \frac{1}{3}mNc^{2}$, where
$P$ is pressure, $V$ volume, $m$ the mass of one molecule, $N$ the number of
molecules and $c$ the root-mean-square speed.

**2.** Definitions as in §7.5. Kathmandu (≈1,350 m) has a lower atmospheric
pressure (≈86 kPa) than Biratnagar (≈100 kPa, near sea level). A liquid boils
when its vapour pressure equals the external pressure, so in Kathmandu that
condition is reached at a lower temperature.

**3.** $n_{H_2} = 4/2 = 2\ \text{mol}$; $n_{O_2} = 64/32 = 2\ \text{mol}$; total
$= 4\ \text{mol}$. Mole fraction of each $= 2/4 = 0.5$. Hence
$p_{H_2} = 0.5 \times 1.5 = 0.75\ \text{atm}$ and
$p_{O_2} = 0.75\ \text{atm}$.

**4.** Use the comparison table of §7.7 — long-range order, sharp vs. ranged
melting point, anisotropy vs. isotropy, clean cleavage vs. irregular breakage.
Examples: NaCl and quartz (crystalline); glass and rubber (amorphous).

**5.** $n = 4.4/44 = 0.1\ \text{mol}$, $T = 300\ \text{K}$.
$V = nRT/P = (0.1 \times 0.0821 \times 300)/2 = 2.463/2 = 1.23\ \text{L}$.
:::

**Group C — Long answer (8 marks each)**

1. (a) State Boyle's law, Charles' law and Avogadro's law, and combine them to
   obtain the ideal gas equation $PV = nRT$. <span class="marks">[4]</span>
   (b) What is meant by the universal gas constant? Give its value in two sets of
   units and state its physical significance. <span class="marks">[2]</span>
   (c) 0.50 g of a gas occupies $280\ \text{cm}^3$ at STP. Calculate its molar
   mass. <span class="marks">[2]</span>
2. (a) Why do real gases deviate from ideal behaviour? Define the compressibility
   factor and sketch how it varies with pressure for H₂ and CO₂. <span class="marks">[4]</span>
   (b) Write the van der Waals equation for $n$ moles and explain the physical
   meaning and units of the constants $a$ and $b$. <span class="marks">[4]</span>
3. (a) Define crystal lattice and unit cell, and name the seven crystal
   systems. <span class="marks">[4]</span>
   (b) A metal of molar mass $56\ \text{g mol}^{-1}$ crystallises in a
   body-centred cubic lattice with $a = 2.87\times10^{-8}\ \text{cm}$. Calculate
   its density. <span class="marks">[4]</span>

::: note Answers to Group C
**1(c).** At STP one mole occupies $22400\ \text{cm}^3$. So
$n = 280/22400 = 0.0125\ \text{mol}$ and
$M = 0.50/0.0125 = 40\ \text{g mol}^{-1}$ (argon).

**2.** (a) Two postulates fail: real molecules attract one another and have a
finite volume. $Z = PV/nRT$; $Z = 1$ for an ideal gas. CO₂ dips well below 1 at
moderate pressure (strong attractions) and rises above 1 at high pressure; H₂
stays above 1 throughout at room temperature. See Figure 4.
(b) $\left(P + an^{2}/V^{2}\right)(V - nb) = nRT$; $a$ measures intermolecular
attraction (atm L² mol⁻²) and $b$ the excluded volume, about four times the true
molecular volume of one mole (L mol⁻¹).

**3(b).** For bcc, $Z = 2$. $a^{3} = (2.87\times10^{-8})^{3} = 2.364\times10^{-23}\ \text{cm}^{3}$.

$$ \rho = \frac{ZM}{a^{3}N_A} = \frac{2 \times 56}{2.364\times10^{-23} \times 6.022\times10^{23}} = \frac{112}{14.24} = 7.87\ \text{g cm}^{-3} $$

which is the density of iron.
:::
