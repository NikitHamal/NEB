---
subject: Physics
grade: 11
unit: 13
title: Ideal gas
hours: 8
area: Heat and Thermodynamics
---

A gas is the simplest state of matter to model, because its molecules are so far
apart that for most of the time they do not feel one another at all. That single
simplification lets us start from Newton's laws applied to a swarm of tiny balls
and end up with the gas laws, with an exact meaning for temperature, and with a
prediction of the specific heat capacities of gases and solids. This unit is the
bridge between mechanics and heat, and it carries the longest derivation in the
Grade 11 course.

::: key What the examiner asks from this unit
Two things appear almost every year: the derivation of $p = \frac{1}{3}\rho
\overline{c^{2}}$ (an 8-mark Group C standard), and a numerical on root mean
square speed or on $C_p - C_v = R$. Learn the derivation as a sequence of
labelled steps — marks are given step by step.
:::

## 13.1 Ideal gas equation

Three experimental laws describe how a fixed mass of gas behaves.

| Law | Held constant | Statement | Form |
|---|---|---|---|
| Boyle's law | $T$ | volume varies inversely as pressure | $pV = $ constant |
| Charles's law | $p$ | volume varies directly as absolute temperature | $V/T = $ constant |
| Pressure (Gay-Lussac) law | $V$ | pressure varies directly as absolute temperature | $p/T = $ constant |

```figure caption="Left: Boyle's law isotherms for one mole. Right: Charles's law. Every line, extrapolated back, meets the temperature axis at $-273.15\ ^\circ$C."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(5.2, 2.5))
R = 8.314
a = axes[0]
V = np.linspace(0.008, 0.050, 300)
for T, col in [(200, '#1d6fb8'), (300, '#2e8b57'), (400, '#d9534f')]:
    a.plot(V*1000, R*T/V/1000, color=col, lw=1.7, label=f'{T} K')
a.set_xlabel('volume  $V$  (litre)'); a.set_ylabel('pressure  $p$  (kPa)')
a.set_xlim(0, 52); a.set_ylim(0, 450)
a.spines[['top','right']].set_visible(False); a.grid(True, alpha=.45)
a.legend(fontsize=7.8)
b = axes[1]
th = np.linspace(-300, 150, 200)
for p, col in [(150e3, '#1d6fb8'), (100e3, '#2e8b57'), (60e3, '#d9534f')]:
    Vv = R*(th+273.15)/p*1000
    ok = th >= 0
    b.plot(th[ok], Vv[ok], color=col, lw=1.7)
    b.plot(th[~ok], Vv[~ok], color=col, lw=1.0, ls='--')
b.axvline(-273.15, color=MUTED, lw=1.0, ls=':')
# the absolute-zero label is read off the line, not printed along it
b.annotate('$-273.15\\ ^\\circ$C', xy=(-273.15, 21), xytext=(-261, 30),
           ha='left', va='center', fontsize=8.0, color=MUTED,
           arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7, shrinkA=2, shrinkB=2))
b.set_xlabel('temperature  ($^\\circ$C)'); b.set_ylabel('volume  $V$  (litre)')
b.set_xlim(-300, 150); b.set_ylim(0, 40)
b.spines[['top','right']].set_visible(False); b.grid(True, alpha=.45)
fig.tight_layout()
```

Combining the three gives, for a fixed mass of gas,

$$ \frac{pV}{T} = \text{constant}, \qquad \text{so} \qquad
\frac{p_1V_1}{T_1} = \frac{p_2V_2}{T_2} $$

Avogadro's law fixes the constant: equal volumes of all gases at the same
temperature and pressure contain equal numbers of molecules. Hence for $n$ moles

$$ pV = nRT $$

where $R = 8.314\ \text{J mol}^{-1}\text{K}^{-1}$ is the **universal gas
constant**, the same for every gas. Writing $n = N/N_A$ for $N$ molecules gives
the molecular form $pV = NkT$, and writing $n = m/M$ gives $p = \rho RT/M$.

::: definition Ideal gas
An ideal gas is one that obeys $pV = nRT$ exactly at all pressures and
temperatures. A real gas approaches this behaviour at low pressure and at
temperatures well above its boiling point, where the molecules are far apart and
their own volume and mutual attraction can be ignored.
:::

::: caution Kelvin and consistent units
$T$ in $pV = nRT$ is always absolute temperature in kelvin, never °C. And if you
use $R = 8.314$, then $p$ must be in pascal and $V$ in cubic metres — mixing in
litres or kPa without converting is the standard way to lose a numerical mark.
:::

::: example Worked example 13.1
**Problem.** A weather balloon of volume $8.0\ \text{m}^3$ is released from
Kathmandu, where the pressure is 86 kPa and the temperature $27\ ^\circ$C. Find
its volume at a height where the pressure is 43 kPa and the temperature
$-33\ ^\circ$C. Assume the gas inside is ideal and none escapes.

**Solution.** Convert temperatures: $T_1 = 27+273 = 300$ K and
$T_2 = -33+273 = 240$ K. Since the mass is fixed,

$$ \frac{p_1V_1}{T_1} = \frac{p_2V_2}{T_2}
\;\Longrightarrow\; V_2 = V_1\times\frac{p_1}{p_2}\times\frac{T_2}{T_1} $$

$$ V_2 = 8.0\times\frac{86}{43}\times\frac{240}{300}
= 8.0\times2.0\times0.80 = 12.8\ \text{m}^{3} $$

The pressure drop alone would have doubled the volume; the fall in temperature
pulls it back to 1.6 times the original.
:::

## 13.2 Molecular properties of matter

All matter is made of molecules that are in ceaseless motion and that attract
one another when a little way apart but repel strongly when pushed very close
together. The separation $r_0$ at which the force is zero — about
$3\times10^{-10}$ m — is the normal spacing in a solid.

| Property | Solid | Liquid | Gas |
|---|---|---|---|
| Molecular spacing | $\approx r_0$ | slightly more than $r_0$ | $\approx 10 r_0$ |
| Intermolecular force | strong | moderate | negligible |
| Motion | vibration about fixed sites | vibration plus slow drift | free, rapid, random |
| Shape / volume | both fixed | volume fixed, shape not | neither fixed |

```figure caption="Force between two molecules. It is strongly repulsive when they are pushed closer than $r_0$ and weakly attractive beyond it."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6, 2.7))
sig = 3.0/2**(1/6)
r = np.linspace(2.55, 8.0, 500)
F = 24*(2*(sig/r)**12 - (sig/r)**6)/r
ax.plot(r, F, color=ACCENT, lw=1.9)
ax.axhline(0, color=INK, lw=0.9)
ax.plot([3.0], [0.0], 'o', color='#d9534f', ms=5.5, zorder=5)
ax.annotate('$r_0 \\approx 3\\times10^{-10}$ m', (3.0, 0), textcoords='offset points',
            xytext=(12, 14), fontsize=8.4, color='#d9534f',
            arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.0, mutation_scale=9))
# the repulsive branch is too steep to hold a label, so it is called out
ax.annotate('repulsion', xy=(2.78, 4.0), xytext=(3.15, 6.3), ha='left',
            va='center', fontsize=8.6, color=MUTED,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7, shrinkA=3, shrinkB=2))
ax.annotate('attraction', (4.6, -1.35), fontsize=8.6, color=MUTED)
ax.annotate('solid', (3.0, -3.4), fontsize=8.2, color='#2e8b57', ha='center')
ax.annotate('gas', (7.0, -3.4), fontsize=8.2, color='#2e8b57', ha='center')
ax.set_xlabel('separation  $r$  ($10^{-10}$ m)')
ax.set_ylabel('force  $F$  (arbitrary units)')
ax.set_xlim(2.55, 8.0); ax.set_ylim(-4.0, 8.0)
ax.set_yticks([])
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.4, axis='x')
```

Two numbers are worth memorising. The **Avogadro constant**
$N_A = 6.022\times10^{23}\ \text{mol}^{-1}$ is the number of molecules in one
mole, and one mole of any gas occupies $22.4$ litres at STP (273.15 K,
101.325 kPa). The mass of a single molecule is $m = M/N_A$, where $M$ is the
molar mass in kilograms per mole.

Molecules are not visible, but their motion is. In 1827 Robert Brown saw pollen
grains suspended in water jiggling in a random zig-zag that never stopped. This
**Brownian motion** is caused by the unbalanced bombardment of the grain by the
surrounding molecules, and the smaller the grain and the higher the temperature,
the more violent the dance — direct evidence that molecules are real and are
always moving.

The **mean free path** is the average distance a molecule travels between
collisions,

$$ \lambda = \frac{1}{\sqrt{2}\,\pi d^{2} n} $$

where $d$ is the molecular diameter and $n$ the number of molecules per unit
volume. For air at room conditions $\lambda \approx 10^{-7}$ m — about 300
molecular diameters, which is why a gas molecule suffers some $10^{9}$ collisions
every second yet still spends nearly all its time moving freely.

## 13.3 Kinetic-molecular model of an ideal gas

::: memory The six assumptions
1. A gas consists of a very large number of **identical** molecules in
   continuous **random** motion.
2. The total volume of the molecules is **negligible** compared with the volume
   of the container.
3. Intermolecular forces are **negligible** except during a collision.
4. Collisions with each other and with the walls are **perfectly elastic**, so
   kinetic energy is conserved.
5. The duration of a collision is negligible compared with the time between
   collisions.
6. Between collisions a molecule moves in a **straight line** with constant
   velocity, obeying Newton's laws.
:::

Two consequences of the model give physical meaning to the two quantities in the
gas equation. **Pressure** is the average force per unit area produced by the
continual bombardment of the walls by molecules. **Temperature** turns out to be
a direct measure of the average kinetic energy of the molecules — a result we
shall prove in §13.5.

Because the motion is random, no direction is preferred. If $u$, $v$, $w$ are
the velocity components of a molecule and $c^2 = u^2+v^2+w^2$, then averaged
over all the molecules

$$ \overline{u^{2}} = \overline{v^{2}} = \overline{w^{2}}
= \tfrac{1}{3}\overline{c^{2}} $$

## 13.4 Derivation of pressure exerted by gas

```figure caption="A molecule of mass $m$ rebounding elastically from the shaded face of a cube of side $l$. Only the $x$-component of its velocity is reversed."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle
fig, ax = plt.subplots(figsize=(4.4, 2.9))
s, d = 3.4, 1.15
f = [(0,0), (s,0), (s,s), (0,s)]
ax.add_patch(Polygon(f, closed=True, facecolor='#eef2f7', ec=INK, lw=1.3))
ax.add_patch(Polygon([(s,0),(s+d,d),(s+d,s+d),(s,s)], closed=True,
                     facecolor='#dfe6ee', ec=INK, lw=1.3, alpha=0.95))
ax.add_patch(Polygon([(0,s),(s,s),(s+d,s+d),(d,s+d)], closed=True,
                     facecolor='#e8edf3', ec=INK, lw=1.3, alpha=0.95))
ax.add_patch(Polygon([(s,0),(s+d,d),(s+d,s+d),(s,s)], closed=True,
                     facecolor='#d9534f', ec=INK, lw=1.3, alpha=0.25))
# incoming and rebound velocities are drawn on slightly separated lines so
# neither arrow is hidden under the other
ax.plot([1.0], [1.75], 'o', color=ACCENT, ms=7, zorder=5)
ax.annotate('', xy=(s-0.08, 1.75), xytext=(1.15, 1.75),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.6, mutation_scale=11))
ax.annotate('', xy=(1.75, 1.25), xytext=(s-0.1, 1.25),
            arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.6, mutation_scale=11))
ax.annotate('$+u$', (2.25, 2.00), fontsize=9.5, color=ACCENT)
ax.annotate('$-u$', (2.25, 1.00), va='top', fontsize=9.5, color='#d9534f')
ax.annotate('', xy=(s, -0.35), xytext=(0, -0.35),
            arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=1.0, mutation_scale=8))
ax.annotate('$l$', (s/2, -0.85), fontsize=10, color=MUTED, ha='center')
ax.annotate('face of area $l^{2}$', (s+d+0.15, (s+d)/2), fontsize=8.5, color='#d9534f')
ax.annotate('momentum change\nper impact $= 2mu$', (0.0, 4.80), va='bottom',
            fontsize=8.4, color=INK)
ax.set_xlim(-0.6, 8.2); ax.set_ylim(-1.3, 6.1); ax.axis('off')
```
::: derivation Pressure of an ideal gas, $p = \frac{1}{3}\rho\,\overline{c^{2}}$
We start from one molecule bouncing off one wall, and reach the pressure of the whole gas.
The plan is: momentum given in one hit $\to$ how often the hits come $\to$ force from one
molecule $\to$ force from all of them $\to$ pressure.

**Setting up.** A cube of side $l$ contains $N$ molecules, each of mass $m$. Take one
molecule with velocity components $u$, $v$, $w$ along the three axes, and watch the face
perpendicular to the $x$-axis.

**Step 1 — velocity after the bounce.** The collision is perfectly elastic and the wall is
smooth, so only the $x$-component is reversed:

$$ u \longrightarrow -u $$

**Step 2 — the molecule's change in momentum.** Momentum after minus momentum before:

$$ \Delta p_{molecule} = (-mu) - (mu) = -2mu $$

**Step 3 — the momentum given to the wall.** By Newton's third law, whatever the molecule
loses the wall gains:

$$ \Delta p_{wall} = 2mu $$

**Step 4 — how far the molecule travels before it hits this same face again.** It must cross
to the opposite face and come back:

$$ \text{distance} = 2l $$

**Step 5 — the time between two hits on this face.** Only the $x$-motion matters for
reaching this face, and $u$ does not change in size:

$$ \Delta t = \frac{2l}{u} $$

**Step 6 — the average force from this one molecule.** Newton's second law in momentum form
says force is rate of change of momentum:

$$ f = \frac{\Delta p_{wall}}{\Delta t} = \frac{2mu}{2l/u} $$

**Step 7 — simplify that fraction.** Dividing by $2l/u$ is the same as multiplying by
$u/2l$:

$$ f = 2mu \times \frac{u}{2l} = \frac{mu^{2}}{l} $$

**Step 8 — add up over all $N$ molecules.** Let their $x$-components be
$u_1, u_2, \ldots, u_N$. Forces on the same wall in the same direction simply add:

$$ F = \frac{m}{l}\left(u_1^{2} + u_2^{2} + \cdots + u_N^{2}\right) $$

**Step 9 — write the sum using a mean.** By definition the mean of the squares is
$\overline{u^{2}} = \dfrac{u_1^{2}+\cdots+u_N^{2}}{N}$, so the sum equals
$N\overline{u^{2}}$:

$$ F = \frac{mN\overline{u^{2}}}{l} $$

**Step 10 — turn force into pressure.** The face has area $l^{2}$:

$$ p = \frac{F}{l^{2}} = \frac{mN\overline{u^{2}}}{l \times l^{2}}
= \frac{mN\overline{u^{2}}}{l^{3}} $$

**Step 11 — replace $l^{3}$ by the volume $V$ of the cube:**

$$ p = \frac{mN\overline{u^{2}}}{V} $$

**Step 12 — bring in the other two directions.** For any one molecule, Pythagoras in three
dimensions gives $c^{2} = u^{2} + v^{2} + w^{2}$. Taking means over all molecules:

$$ \overline{c^{2}} = \overline{u^{2}} + \overline{v^{2}} + \overline{w^{2}} $$

**Step 13 — use the randomness of the motion.** No direction is special, so on average the
molecules move as much along $x$ as along $y$ or $z$:

$$ \overline{u^{2}} = \overline{v^{2}} = \overline{w^{2}} $$

**Step 14 — combine Steps 12 and 13.** The right-hand side of Step 12 becomes three equal
terms:

$$ \overline{c^{2}} = 3\,\overline{u^{2}}
\qquad \Longrightarrow \qquad \overline{u^{2}} = \tfrac{1}{3}\overline{c^{2}} $$

**Step 15 — substitute into Step 11:**

$$ p = \frac{1}{3}\cdot\frac{mN}{V}\cdot\overline{c^{2}} $$

**Step 16 — recognise the density.** The total mass of the gas is $mN$, so $mN/V$ is the
density $\rho$:

$$ p = \tfrac{1}{3}\rho\,\overline{c^{2}} $$

**Result.**

$$ p = \frac{1}{3}\rho\,\overline{c^{2}}
\qquad \text{or, multiplying by } V, \qquad
pV = \frac{1}{3}mN\overline{c^{2}} $$

**What it means.** Pressure is nothing more than the drumming of molecular impacts. It rises
if the molecules are heavier, if there are more of them in the same space, or — most
strongly — if they move faster, since the speed enters **squared**.

**Conditions used.** Collisions are perfectly elastic; molecules have negligible volume and
no forces between them except during collisions; motion is completely random (Step 13); and
the container walls are smooth and rigid. The cube is only for convenience — the result holds
for a vessel of any shape.
:::

::: tip The examiner is looking for
1. Momentum change per impact $= 2mu$, justified by Newton's third law.
2. Time between impacts $= 2l/u$, with the distance $2l$ explained.
3. Force from one molecule $= mu^{2}/l$ using $F = \Delta p/\Delta t$.
4. Summation over $N$ molecules and the introduction of $\overline{u^{2}}$.
5. Division by area $l^{2}$ and the substitution $V = l^{3}$.
6. The randomness argument giving $\overline{u^{2}} = \frac{1}{3}\overline{c^{2}}$ —
   **this step alone often carries a mark.**
7. The final statement, plus the list of assumptions.
:::

::: caution $\overline{c^{2}}$ is a mean of squares, not the square of a mean
For molecules of speeds 1, 2 and 3 units the mean speed is 2 but
$\overline{c^{2}} = (1+4+9)/3 = 4.67$, whose square root is 2.16. The rms speed
is always a little larger than the mean speed; never square the average.
:::

## 13.5 Average translational kinetic energy of gas molecule

::: derivation Average translational kinetic energy $\overline{E} = \frac{3}{2}kT$
We start from the kinetic-theory result for $pV$ and the ideal gas equation, and reach the
statement that temperature *is* molecular kinetic energy.

**Step 1 — the kinetic theory result from section 13.4:**

$$ pV = \tfrac{1}{3}mN\overline{c^{2}} $$

**Step 2 — reshape the right side so that a kinetic energy appears.** We want
$\frac{1}{2}m\overline{c^{2}}$ inside, so write $\frac{1}{3} = \frac{2}{3}\times\frac{1}{2}$:

$$ pV = \tfrac{2}{3}N\left(\tfrac{1}{2}m\overline{c^{2}}\right) $$

**Step 3 — name the bracket.** $\frac{1}{2}m\overline{c^{2}}$ is the average translational
kinetic energy of one molecule; call it $\overline{E}$:

$$ pV = \tfrac{2}{3}N\overline{E} $$

**Step 4 — bring in the experimental gas law.** For $N$ molecules, $pV = NkT$ where $k$ is
the Boltzmann constant:

$$ NkT = \tfrac{2}{3}N\overline{E} $$

**Step 5 — cancel $N$ from both sides:**

$$ kT = \tfrac{2}{3}\overline{E} $$

**Step 6 — multiply both sides by $\frac{3}{2}$:**

$$ \overline{E} = \tfrac{3}{2}kT $$

**Result.**

$$ \overline{E} = \tfrac{1}{2}m\overline{c^{2}} = \tfrac{3}{2}kT $$

**What it means.** The right-hand side contains no $m$, no $p$ and no $V$ — only the
temperature. So at the same temperature a hydrogen molecule and a carbon-dioxide molecule
have the **same** average kinetic energy; the heavy one simply moves more slowly. This is
what absolute temperature really measures.

**Conditions used.** The gas is ideal, and only *translational* energy is counted (rotation
and vibration are extra, and are why $C_v$ differs between gases).
:::

::: derivation Root mean square speed $c_{rms} = \sqrt{3RT/M}$
We start from the same two equations, but written for **one mole**, and reach a formula for
molecular speed.

**Step 1 — take one mole.** Then $N = N_A$, and the total mass $mN_A$ is the molar mass $M$:

$$ pV = \tfrac{1}{3}M\overline{c^{2}} $$

**Step 2 — write the gas equation for one mole:**

$$ pV = RT $$

**Step 3 — set the two expressions for $pV$ equal:**

$$ \tfrac{1}{3}M\overline{c^{2}} = RT $$

**Step 4 — multiply both sides by 3:**

$$ M\overline{c^{2}} = 3RT $$

**Step 5 — divide both sides by $M$:**

$$ \overline{c^{2}} = \frac{3RT}{M} $$

**Step 6 — take the square root.** The root of the mean of the squares is, by definition, the
**rms speed**:

$$ c_{rms} = \sqrt{\frac{3RT}{M}} $$

**Result.** Two other forms follow at once, by using $p = \frac{1}{3}\rho\overline{c^{2}}$
and by dividing $R/M$ by Avogadro's number:

$$ c_{rms} = \sqrt{\frac{3RT}{M}} = \sqrt{\frac{3kT}{m}} = \sqrt{\frac{3p}{\rho}} $$

**What it means.** $c_{rms} \propto \sqrt{T}$, so to double the molecular speed you must
**quadruple** the absolute temperature. And $c_{rms} \propto 1/\sqrt{M}$, which is why light
gases such as hydrogen and helium leak out of a balloon — and out of a planet's
atmosphere — faster than heavy ones.

**Conditions used.** Ideal-gas behaviour; $T$ in kelvin and $M$ in kg mol⁻¹.
:::

::: key Temperature is molecular kinetic energy
The average translational kinetic energy of a gas molecule depends **only** on
the absolute temperature — not on the pressure, the volume or the kind of gas.
Heavy molecules simply move more slowly. For one mole the total translational
kinetic energy is $\frac{3}{2}RT$, and at $T = 0$ it would vanish, which is the
kinetic-theory meaning of absolute zero.
:::

::: example Worked example 13.2
**Problem.** Find the average translational kinetic energy of one molecule of
any gas at $27\ ^\circ$C, and the total translational kinetic energy of one mole
at the same temperature. Take $k = 1.38\times10^{-23}\ \text{J K}^{-1}$ and
$R = 8.314\ \text{J mol}^{-1}\text{K}^{-1}$.

**Solution.** $T = 300$ K. For one molecule,

$$ \overline{E} = \tfrac{3}{2}kT = 1.5\times1.38\times10^{-23}\times300
= 6.21\times10^{-21}\ \text{J} $$

For one mole,

$$ E = \tfrac{3}{2}RT = 1.5\times8.314\times300 = 3.74\times10^{3}\ \text{J} $$

That is about 3.7 kJ per mole — the same for helium, nitrogen or carbon dioxide
at this temperature.
:::

## 13.6 Boltzmann constant; root mean square speed

::: definition Boltzmann constant
The Boltzmann constant is the gas constant per molecule:
$$ k = \frac{R}{N_A} = \frac{8.314}{6.022\times10^{23}}
= 1.38\times10^{-23}\ \text{J K}^{-1} $$
It converts absolute temperature into energy per molecule.
:::

The **root mean square speed** is the square root of the mean of the squares of
the molecular speeds. It was derived step by step in section 13.5:

$$ c_{rms} = \sqrt{\overline{c^{2}}} = \sqrt{\frac{3RT}{M}}
= \sqrt{\frac{3kT}{m}} = \sqrt{\frac{3p}{\rho}} $$

Use the first form when you know the temperature and the molar mass, and the
last when you know the pressure and density. Two conclusions follow at once:
$c_{rms} \propto \sqrt{T}$, so to double the rms speed you must **quadruple** the
absolute temperature; and $c_{rms} \propto 1/\sqrt{M}$ at a given temperature, so
hydrogen molecules move four times as fast as oxygen molecules.

```figure caption="Maxwell distribution of molecular speeds for oxygen. Raising the temperature flattens and broadens the curve and shifts it to higher speeds."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9, 2.8))
kB = 1.381e-23; m = 0.032/6.022e23
v = np.linspace(1, 2000, 800)
for T, col in [(300, '#1d6fb8'), (900, '#d9534f')]:
    f = 4*np.pi*(m/(2*np.pi*kB*T))**1.5 * v**2 * np.exp(-m*v**2/(2*kB*T))
    ax.plot(v, f*1000, color=col, lw=1.8, label=f'{T} K')
T = 300.0
vmp = np.sqrt(2*kB*T/m); vav = np.sqrt(8*kB*T/(np.pi*m)); vrms = np.sqrt(3*kB*T/m)
# the three speeds differ by under 90 m/s, so the markers are carried above
# the peak and the labels fanned left / up / right to keep them apart
marks = [(vmp, '$v_{mp}$', 2.22, 2.32, 'right', vmp - 8),
         (vav, r'$\bar{v}$', 2.46, 2.56, 'center', vav),
         (vrms, '$c_{rms}$', 2.22, 2.32, 'left', vrms + 8)]
for x, lab, top, ly, ha, lx in marks:
    ax.vlines(x, 0, top, color=MUTED, lw=0.9, ls=':')
    ax.annotate(lab, (lx, ly), fontsize=8.6, color=MUTED, ha=ha, va='center')
ax.set_xlabel('molecular speed  $v$  (m s$^{-1}$)')
ax.set_ylabel('fraction per unit speed  ($10^{-3}$ s m$^{-1}$)')
ax.set_xlim(0, 2000); ax.set_ylim(0, 2.78)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.45)
ax.legend(fontsize=8.2)
```

The speeds are spread over a wide range described by the **Maxwell
distribution**. Three speeds are quoted from it: the most probable speed
$v_{mp} = \sqrt{2kT/m}$, the mean speed $\bar{v} = \sqrt{8kT/\pi m}$ and the rms
speed $c_{rms} = \sqrt{3kT/m}$, always in that increasing order, in the ratio
$1 : 1.128 : 1.225$.

::: example Worked example 13.3
**Problem.** Calculate the rms speed of oxygen molecules at $27\ ^\circ$C
($M = 32\ \text{g mol}^{-1}$). At what temperature will hydrogen molecules
($M = 2\ \text{g mol}^{-1}$) have this same rms speed?

**Solution.** With $T = 300$ K and $M = 0.032\ \text{kg mol}^{-1}$,

$$ c_{rms} = \sqrt{\frac{3RT}{M}} = \sqrt{\frac{3\times8.314\times300}{0.032}}
= \sqrt{2.338\times10^{5}} = 484\ \text{m s}^{-1} $$

For equal rms speeds, $3RT_H/M_H = 3RT_O/M_O$, so $T$ is proportional to $M$:

$$ T_H = T_O\times\frac{M_H}{M_O} = 300\times\frac{2}{32} = 18.8\ \text{K} $$

Hydrogen must be cooled almost to liquid-helium temperatures to slow it down to
the speed oxygen has at room temperature.
:::

## 13.7 Heat capacities: gases and solids

A gas has two molar heat capacities, because it can be heated in two different
ways.

::: definition Molar heat capacities
$C_v$ is the heat needed to raise the temperature of one mole by 1 K at constant
**volume**; $C_p$ is the heat needed for the same rise at constant
**pressure**. Both are in J mol⁻¹ K⁻¹.
:::

$C_p$ is always the larger. At constant volume the gas cannot expand, so all the
heat goes into internal energy. At constant pressure the gas must also push back
the surroundings, and the extra heat supplies that work.

::: derivation Mayer's relation, $C_p - C_v = R$
We start from the same small temperature rise $dT$ given to one mole of gas in two different
ways, and reach the relation between the two molar heat capacities.

**Setting up.** Take exactly one mole. Heat it once at constant volume and once at constant
pressure, in both cases raising its temperature by the same small amount $dT$. The internal
energy of an ideal gas depends only on its temperature, so the *same* $dT$ always produces
the *same* change $dU$, whichever path we take. That single fact is the key to the whole
derivation.

**Step 1 — heat it at constant volume.** By the definition of $C_v$, the heat needed is

$$ dQ_v = C_v\,dT $$

**Step 2 — no work is done at constant volume.** Work is $p\,dV$, and $dV = 0$ because the
gas cannot expand. So by the first law, $dQ = dU + p\,dV$ reduces to

$$ dU = C_v\,dT $$

**Step 3 — now heat it at constant pressure.** By the definition of $C_p$:

$$ dQ_p = C_p\,dT $$

**Step 4 — apply the first law to this second path.** Now the gas *does* expand, pushing
back the surroundings:

$$ C_p\,dT = dU + p\,dV $$

**Step 5 — replace $dU$ using Step 2.** This is the step licensed by the "setting up"
remark: the same $dT$ means the same $dU$:

$$ C_p\,dT = C_v\,dT + p\,dV $$

**Step 6 — find $p\,dV$ from the gas law.** For one mole, $pV = RT$. Differentiating both
sides with $p$ held constant:

$$ p\,dV = R\,dT $$

**Step 7 — substitute this into Step 5:**

$$ C_p\,dT = C_v\,dT + R\,dT $$

**Step 8 — divide every term by $dT$:**

$$ C_p = C_v + R $$

**Step 9 — rearrange:**

$$ C_p - C_v = R $$

**Result.**

$$ C_p - C_v = R $$

**What it means.** $C_p$ is always the larger of the two, because heating at constant
pressure has to pay for the expansion work as well as the temperature rise. The extra amount
is exactly $R$ — the same for every ideal gas, monatomic or diatomic, because the work done
in expanding depends only on the gas law and not on the molecule's structure.

**Conditions used.** One mole of an **ideal** gas, and internal energy a function of
temperature alone. For a mass of $n$ moles the relation becomes $C_p - C_v = nR$ if $C$ means
total heat capacity; per unit mass it becomes $c_p - c_v = R/M$.
:::

::: tip The examiner is looking for
1. Both processes applied to the **same** $dT$ and the same one mole.
2. $dU = C_v\,dT$, with the reason "no work is done at constant volume".
3. The first law written as $dQ = dU + p\,dV$ for the constant-pressure path.
4. $p\,dV = R\,dT$ obtained by differentiating $pV = RT$ at constant $p$.
5. The cancellation of $dT$ and the final statement $C_p - C_v = R$.
:::

The ratio $\gamma = C_p/C_v$ identifies the kind of molecule, because the
internal energy depends on how many independent ways a molecule can store
energy.

| Gas | $C_v$ | $C_p$ | $\gamma = C_p/C_v$ | Example |
|---|---|---|---|---|
| Monatomic | $\frac{3}{2}R = 12.5$ | $\frac{5}{2}R = 20.8$ | 1.67 | He, Ne, Ar |
| Diatomic | $\frac{5}{2}R = 20.8$ | $\frac{7}{2}R = 29.1$ | 1.40 | H₂, O₂, N₂ |

(Values in J mol⁻¹ K⁻¹.) A monatomic molecule is a single point and can only
move in three directions, so its energy is entirely translational,
$U = \frac{3}{2}RT$ per mole, giving $C_v = \frac{3}{2}R$. A diatomic molecule is
a dumbbell that can also rotate about two axes, storing $\frac{1}{2}RT$ more per
mole in each, so $U = \frac{5}{2}RT$ and $C_v = \frac{5}{2}R$.

**Solids.** In a solid the atoms cannot travel; they vibrate about fixed sites.
Each atom vibrating in three dimensions stores $3kT$ of energy on average — half
kinetic and half potential in each of the three directions — so one mole stores
$U = 3RT$ and the molar heat capacity is

$$ C = 3R \approx 25\ \text{J mol}^{-1}\text{K}^{-1} $$

This is the **law of Dulong and Petit**: all simple solids have about the same
molar heat capacity. It works well: for copper ($M = 63.5\ \text{g mol}^{-1}$)
it predicts $c = 3R/M = 24.9/0.0635 = 392\ \text{J kg}^{-1}\text{K}^{-1}$,
against a measured 385. It fails badly at low temperatures, where every solid's
heat capacity falls towards zero — a purely quantum effect that classical
physics cannot explain.

::: example Worked example 13.4
**Problem.** For a certain gas $C_p = 29.1$ and
$C_v = 20.8\ \text{J mol}^{-1}\text{K}^{-1}$. (a) Find $R$ and $\gamma$ and say
whether the gas is monatomic or diatomic. (b) How much heat is needed to raise
the temperature of 2.0 mol of this gas by 50 K at constant pressure, and how
much at constant volume? (c) Account for the difference.

**Solution.** (a) $R = C_p - C_v = 29.1 - 20.8 = 8.3\ \text{J mol}^{-1}
\text{K}^{-1}$, and $\gamma = 29.1/20.8 = 1.40$, so the gas is **diatomic**.

(b) At constant pressure:

$$ Q_p = nC_p\Delta T = 2.0\times29.1\times50 = 2910\ \text{J} $$

At constant volume:

$$ Q_v = nC_v\Delta T = 2.0\times20.8\times50 = 2080\ \text{J} $$

(c) The difference is $2910-2080 = 830$ J. This is exactly the work done by the
gas in expanding at constant pressure:

$$ W = p\Delta V = nR\Delta T = 2.0\times8.3\times50 = 830\ \text{J} $$
:::

## Chapter summary

- Gas laws combine into the ideal gas equation $pV = nRT = NkT$, with
  $R = 8.314\ \text{J mol}^{-1}\text{K}^{-1}$ and $T$ in kelvin.
- Kinetic theory assumes many identical molecules of negligible volume in random
  motion, with no forces except during elastic collisions.
- Pressure of an ideal gas: $p = \frac{1}{3}\rho\overline{c^{2}}$, equivalently
  $pV = \frac{1}{3}mN\overline{c^{2}}$.
- Average translational kinetic energy per molecule is
  $\overline{E} = \frac{1}{2}m\overline{c^{2}} = \frac{3}{2}kT$, and per mole
  $\frac{3}{2}RT$ — independent of the nature of the gas.
- Boltzmann constant $k = R/N_A = 1.38\times10^{-23}\ \text{J K}^{-1}$.
- Root mean square speed $c_{rms} = \sqrt{3RT/M} = \sqrt{3kT/m} =
  \sqrt{3p/\rho}$, so $c_{rms}\propto\sqrt{T}$ and $c_{rms}\propto 1/\sqrt{M}$.
- Mayer's relation $C_p - C_v = R$; $\gamma = 1.67$ for monatomic and $1.40$ for
  diatomic gases.
- Dulong and Petit: the molar heat capacity of a simple solid is about
  $3R = 25\ \text{J mol}^{-1}\text{K}^{-1}$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. At constant temperature the pressure of a fixed mass of ideal gas is
   proportional to <span class="marks">[1]</span>
   (a) $V$ (b) $1/V$ (c) $V^2$ (d) $\sqrt{V}$
2. The rms speed of the molecules of an ideal gas is proportional to <span class="marks">[1]</span>
   (a) $T$ (b) $T^{2}$ (c) $\sqrt{T}$ (d) $1/T$
3. The average translational kinetic energy of a molecule at absolute
   temperature $T$ is <span class="marks">[1]</span>
   (a) $kT$ (b) $\frac{3}{2}kT$ (c) $\frac{3}{2}RT$ (d) $\frac{1}{2}kT$
4. For a diatomic gas the ratio $C_p/C_v$ is about <span class="marks">[1]</span>
   (a) 1.33 (b) 1.40 (c) 1.67 (d) 1.00
5. According to the law of Dulong and Petit, the molar heat capacity of a simple
   solid is about <span class="marks">[1]</span>
   (a) $R$ (b) $\frac{3}{2}R$ (c) $3R$ (d) $\frac{5}{2}R$

::: note Answers to Group A
**1.** (b) — Boyle's law, $pV$ constant.
**2.** (c) — $c_{rms} = \sqrt{3RT/M}$.
**3.** (b) — per **molecule**; $\frac{3}{2}RT$ would be per mole.
**4.** (b) — $C_p/C_v = 3.5R/2.5R = 1.40$.
**5.** (c) — $3R \approx 25\ \text{J mol}^{-1}\text{K}^{-1}$.
:::

**Group B — Short answer (5 marks each)**

1. State the assumptions of the kinetic molecular model of an ideal gas, and
   explain on this model what pressure and temperature mean. <span class="marks">[5]</span>
2. A closed cylinder contains 2.0 g of hydrogen ($M = 2.0\ \text{g mol}^{-1}$) at
   $27\ ^\circ$C. Find (i) the number of molecules present and (ii) the total
   translational kinetic energy of the gas. <span class="marks">[5]</span>
3. Define the Boltzmann constant and show that the average translational kinetic
   energy of a gas molecule is $\frac{3}{2}kT$. <span class="marks">[5]</span>
4. Derive Mayer's relation $C_p - C_v = R$ and hence find $\gamma$ for a
   monatomic gas. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** The six assumptions of §13.3. Pressure is the average force per unit area
from molecular bombardment of the walls; temperature is a direct measure of the
average translational kinetic energy of the molecules,
$\overline{E} = \frac{3}{2}kT$.

**2.** (i) $n = 2.0/2.0 = 1.0$ mol, so
$N = nN_A = 6.02\times10^{23}$ molecules.
(ii) $E = \frac{3}{2}nRT = 1.5\times1.0\times8.314\times300 = 3.74\times10^{3}$ J.

**3.** Define $k = R/N_A$. Then from kinetic theory
$pV = \frac{1}{3}mN\overline{c^{2}} = \frac{2}{3}N(\frac{1}{2}m\overline{c^{2}})$;
equating to $pV = NkT$ gives
$\frac{1}{2}m\overline{c^{2}} = \frac{3}{2}kT$.

**4.** Derivation as in §13.7. For a monatomic gas $C_v = \frac{3}{2}R$, so
$C_p = C_v + R = \frac{5}{2}R$ and
$\gamma = \frac{5}{2}R \div \frac{3}{2}R = 5/3 = 1.67$.
:::

**Group C — Long answer (8 marks each)**

1. (a) State the assumptions of the kinetic theory of gases and derive the
   expression $p = \frac{1}{3}\rho\overline{c^{2}}$ for the pressure of an ideal
   gas. <span class="marks">[6]</span>
   (b) Hence show that the average translational kinetic energy of a molecule is
   $\frac{3}{2}kT$. <span class="marks">[2]</span>
2. A vessel of volume $0.0249\ \text{m}^3$ contains oxygen at 300 K and a
   pressure of $1.0\times10^{5}\ \text{Pa}$. Taking $M = 32\ \text{g mol}^{-1}$,
   find (a) the number of moles, (b) the number of molecules, (c) the density of
   the gas and (d) the rms speed of its molecules. <span class="marks">[8]</span>

::: note Answers to Group C
**1.** Full derivation as set out in §13.4, Steps 1 to 6, followed by the
argument of §13.5.

**2.** (a) $n = pV/RT = (1.0\times10^{5}\times0.0249)/(8.314\times300)
= 2490/2494 = 1.00$ mol.

(b) $N = nN_A = 6.02\times10^{23}$ molecules.

(c) Mass $= nM = 1.00\times0.032 = 0.032$ kg, so
$\rho = 0.032/0.0249 = 1.29\ \text{kg m}^{-3}$.

(d) $c_{rms} = \sqrt{3p/\rho} = \sqrt{(3\times1.0\times10^{5})/1.29}
= \sqrt{2.33\times10^{5}} = 483\ \text{m s}^{-1}$.
(The same answer follows from $\sqrt{3RT/M}$, as it must.)
:::
