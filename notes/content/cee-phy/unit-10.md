---
subject: Physics
grade: CEE
unit: 10
title: Ideal Gas and Thermodynamics
hours: 3
area: Heat and Thermodynamics
---

This is the heaviest chapter in the Heat area: **3 of the 50 Physics questions**
come from it.
Three kinds of question are set. The **gas law** — a state change, a density, an rms
speed, a ratio of speeds. The **first law** — the four processes, the work done, and
the molar heat capacities. And the **second law** — engine efficiency, refrigerator
COP, and why no engine can be perfect. Almost every mark here comes from getting the
**sign convention** right once and then applying one table.

::: key What the paper asks from this chapter
- $PV = nRT = NkT$; every other form ($P = \rho RT/M$, $P_1V_1/T_1 = P_2V_2/T_2$), and $R = N_Ak = 8.31$ J mol⁻¹ K⁻¹.
- Kinetic theory: $P = \frac{1}{3}\rho c_{rms}^2$; $c_{rms} = \sqrt{3RT/M} = \sqrt{3kT/m}$; average translational KE $= \frac{3}{2}kT$ per molecule.
- Degrees of freedom: 3, 5, 6 for monatomic, diatomic, polyatomic; $C_v = \frac{f}{2}R$, $C_p = C_v + R$, $\gamma = 1 + 2/f$.
- First law $Q = \Delta U + W$, with $W$ the work done **by** the gas; $\Delta U = nC_v\Delta T$ in every process.
- The four processes: $W$, $Q$, $\Delta U$ and the molar heat capacity of each; isothermal $W = nRT\ln(V_2/V_1)$; adiabatic $PV^\gamma = $ const.
- Second law: no engine turns all its heat into work; $\eta = 1 - Q_2/Q_1 \le 1 - T_2/T_1$; refrigerator COP $= Q_2/W$.
- Entropy never decreases in an isolated system; $\Delta S = Q/T$ for a reversible change.
:::

## 10.1 Ideal-gas equation; kinetic theory: pressure, rms speed and energy of molecules

### The ideal gas

A real gas at low pressure and moderate temperature behaves almost like an **ideal
gas**. The model makes five assumptions:

1. A gas is a large number of identical molecules in random motion.
2. The molecules are **point-like** — their own volume is negligible beside the
   volume of the container.
3. **No intermolecular forces** except during a collision (so there is no potential
   energy of interaction).
4. Collisions with each other and with the walls are **perfectly elastic** — kinetic
   energy is conserved.
5. Between collisions the molecules move in straight lines, and the collision time is
   negligible beside the time between collisions.

Assumption 3 is the important one: with no potential energy, the **internal energy
of an ideal gas is entirely kinetic, and depends only on temperature**.

### The gas laws and the equation of state

| Law | Held constant | Statement |
|---|---|---|
| Boyle's | $T$ | $PV = $ constant |
| Charles's | $P$ | $V/T = $ constant |
| Pressure (Gay-Lussac's) | $V$ | $P/T = $ constant |
| Avogadro's | $P$, $T$ | $V \propto n$ |

Combining them gives the **ideal-gas equation**:

$$ PV = nRT = NkT = \frac{m}{M}RT, \qquad P = \frac{\rho RT}{M} $$

| Symbol | Meaning | Value |
|---|---|---|
| $R$ | universal gas constant | $8.31$ J mol⁻¹ K⁻¹ |
| $k$ | Boltzmann constant | $1.38\times10^{-23}$ J K⁻¹ |
| $N_A$ | Avogadro number | $6.02\times10^{23}$ mol⁻¹ |
| $n$ | number of moles, $m/M$ | mol |

and $R = N_Ak$, $k = R/N_A$. Since $n = m/M$, the density of a gas is

$$ \rho = \frac{PM}{RT} $$

so at a fixed pressure and temperature **a denser gas is a heavier gas** — carbon
dioxide sinks, hydrogen rises. For a fixed mass of gas, $PV/T$ is constant:

$$ \frac{P_1V_1}{T_1} = \frac{P_2V_2}{T_2} $$

One mole of any ideal gas occupies **22.4 L at STP** (273 K, 1 atm) and 22.7 L at
1 bar. **Temperatures in the gas equation must be in kelvin** — every time.

**Dalton's law of partial pressures:** in a mixture of non-reacting gases, the total
pressure is the sum of the pressures each gas would exert alone:
$P = P_1 + P_2 + \dots$ For each gas $P_iV = n_iRT$, so the mole fraction fixes the
share of the pressure.

::: example Worked example 10.1 — how many molecules in a breath
**Problem.** A balloon contains 2.0 g of helium ($M = 4.0$ g mol⁻¹) at 27 °C and a
pressure of $1.0\times10^5$ Pa. Find the volume and the number of molecules.
($R = 8.31$ J mol⁻¹ K⁻¹.)

**Solution.** $n = 2.0/4.0 = 0.50$ mol and $T = 300$ K, so
$V = \dfrac{nRT}{P} = \dfrac{0.50\times8.31\times300}{1.0\times10^5}
= 1.25\times10^{-2}$ m³ $= 12.5$ L.
The number of molecules is $N = nN_A = 0.50\times6.02\times10^{23}
= 3.01\times10^{23}$.

Note that the *identity* of the gas enters only through $M$; at the same $P$, $V$
and $T$, every gas has the same number of molecules (Avogadro).
:::

### Kinetic theory: where the pressure comes from

Pressure is the average force per unit area from molecules hammering the walls. Each
molecule of mass $m$ and velocity component $v_x$ hits a wall, rebounds with $-v_x$,
and delivers momentum $2mv_x$. The derivation is short and worth following once.

::: derivation Pressure of an ideal gas, P = ⅓ρc²
**Starting point.** $N$ molecules of mass $m$ in a cubical box of side $L$; we want
the pressure on one wall.

**Setting up.** Take one molecule moving with velocity component $v_x$ towards the
wall. It rebounds elastically, so its momentum change is $2mv_x$.

**Step 1 — how often it hits that wall.** It must travel $2L$ (there and back), so
the time between hits is $2L/v_x$, and the number of hits per second is $v_x/2L$.

**Step 2 — force from one molecule.** Force = momentum change × hits per second
$= 2mv_x\cdot\dfrac{v_x}{2L} = \dfrac{mv_x^2}{L}$.

**Step 3 — add all molecules.** The total force on the wall is
$\dfrac{m}{L}\sum v_x^2$, and the pressure is force/area with area $L^2$:
$P = \dfrac{m}{L^3}\sum v_x^2 = \dfrac{mN}{V}\overline{v_x^2}$.

**Step 4 — use isotropy.** The motion is random in direction, so
$\overline{v_x^2} = \overline{v_y^2} = \overline{v_z^2}$, and
$c^2 = v_x^2+v_y^2+v_z^2$ gives $\overline{v_x^2} = \frac{1}{3}\overline{c^2}$.

**Result.**
$$ P = \frac{1}{3}\frac{mN}{V}\overline{c^2} = \frac{1}{3}\rho c_{rms}^2 $$

**What it means.** Pressure is the kinetic energy density of the molecules, times
$\frac{2}{3}$. The conditions are the five ideal-gas assumptions; the result is
exact for them, and a good approximation for real gases at low pressure.
:::

::: caution rms, mean and most probable are three different speeds
$c_{rms} = \sqrt{\overline{c^2}}$ is **not** the average speed. For the Maxwell
distribution
$$ c_{mp} = \sqrt{\frac{2RT}{M}}, \qquad
c_{avg} = \sqrt{\frac{8RT}{\pi M}}, \qquad
c_{rms} = \sqrt{\frac{3RT}{M}} $$
in the ratio $1.41 : 1.60 : 1.73$. Only $c_{rms}$ appears in $P = \frac{1}{3}\rho
c_{rms}^2$. A question that says "average speed" wants $c_{avg}$; one that says "rms"
wants $c_{rms}$.
:::

### rms speed and kinetic energy

Squaring $c_{rms} = \sqrt{3RT/M}$ and combining it with $PV = nRT$:

$$ c_{rms} = \sqrt{\frac{3RT}{M}} = \sqrt{\frac{3kT}{m}} = \sqrt{\frac{3P}{\rho}} $$

Three consequences, each of which is a standard question:

- **At the same temperature, lighter molecules move faster**: $c_{rms}\propto
  1/\sqrt{M}$. Hydrogen ($M = 2$) moves four times as fast as oxygen ($M = 32$).
  This is why hydrogen and helium escape the Earth's atmosphere and nitrogen and
  oxygen do not.
- **$c_{rms}\propto\sqrt{T}$**: to double the rms speed you must **quadruple** the
  absolute temperature.
- **Average kinetic energy** of one molecule is $\frac{1}{2}m\overline{c^2}
  = \frac{3}{2}kT$, independent of the gas. For one mole it is $\frac{3}{2}RT$, and
  for $n$ moles the total translational kinetic energy is $\frac{3}{2}nRT
  = \frac{3}{2}PV$.

```figure caption="Maxwell–Boltzmann distribution of molecular speeds at 300 K and 600 K for nitrogen. Raising the temperature flattens and widens the curve: the most probable speed and the rms speed both move to the right."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9,2.85))
M, R = 0.028, 8.314
v = np.linspace(0, 1500, 500)
def f(T):
    a = M/(2*np.pi*R*T)
    return 4*np.pi*(a**1.5)*v**2*np.exp(-M*v**2/(2*R*T))*1e3
for T, c, lab, ty in [(300, ACCENT, '300 K', 2.62), (600, SERIES[2], '600 K', 1.72)]:
    ax.plot(v, f(T), color=c, lw=2.0, zorder=3)
    vr = np.sqrt(3*R*T/M)
    ax.plot([vr,vr],[0, f(T)[np.argmin(abs(v-vr))]], color=c, lw=0.9, ls=(0,(3,3)))
    ax.text(vr-25, ty, lab, color=c, fontsize=8.5, va='center', ha='center')
ax.text(40, 2.32, 'dashed lines: rms speed', fontsize=8, color=MUTED, va='center')
ax.set_xlabel('molecular speed  (m s⁻¹)')
ax.set_ylabel('fraction per unit speed  (10⁻³ s m⁻¹)')
ax.set_xlim(0,1500); ax.set_ylim(0,2.85)
ax.set_xticks([0,500,1000,1500])
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.5)
```

### Degrees of freedom and molar heat capacities

A **degree of freedom** is one independent way a molecule can store energy. By the
**law of equipartition**, each degree of freedom carries $\frac{1}{2}kT$ per molecule
on average.

| Gas | Example | Degrees of freedom $f$ | $C_v$ | $C_p$ | $\gamma$ |
|---|---|---|---|---|---|
| Monatomic | He, Ne, Ar | 3 (all translational) | $\frac{3}{2}R = 12.5$ | $\frac{5}{2}R = 20.8$ | 1.67 |
| Diatomic | H₂, O₂, N₂ | 5 (3 + 2 rotational) | $\frac{5}{2}R = 20.8$ | $\frac{7}{2}R = 29.1$ | 1.40 |
| Polyatomic | NH₃, CH₄ | 6 (3 + 3 rotational) | $3R = 24.9$ | $4R = 33.3$ | 1.33 |

(Units J mol⁻¹ K⁻¹.) A diatomic molecule has two rotational axes because rotation
about the bond axis carries almost no energy. At high temperature the bond can also
vibrate, adding two more degrees of freedom and lowering γ towards 1.29 — not needed
for the paper, but it explains why γ is not exactly 1.40 for real air.

$$ C_v = \frac{f}{2}R, \qquad C_p = C_v + R = \left(\frac{f}{2}+1\right)R, \qquad
\gamma = \frac{C_p}{C_v} = 1 + \frac{2}{f} $$

::: memory γ in three numbers
$f = 3 \Rightarrow \gamma = 1.67$; $f = 5 \Rightarrow \gamma = 1.40$;
$f = 6 \Rightarrow \gamma = 1.33$. Monatomic is the *biggest* γ, polyatomic the
smallest — because more ways to store energy means more heat needed for the same
temperature rise, so $C_v$ is larger and the ratio $C_p/C_v$ smaller.
:::

::: example Worked example 10.2 — two gases at the same temperature
**Problem.** At 300 K, compare the rms speeds and the average kinetic energies of
hydrogen ($M = 2$ g mol⁻¹) and oxygen ($M = 32$ g mol⁻¹).

**Solution.** $c_{rms} = \sqrt{3RT/M}$, so
$\dfrac{c_{H_2}}{c_{O_2}} = \sqrt{\dfrac{32}{2}} = 4$.
Hydrogen molecules move four times as fast.
The average kinetic energy is $\frac{3}{2}kT$ for **both**, because it depends only
on $T$: $\frac{3}{2}(1.38\times10^{-23})(300) = 6.2\times10^{-21}$ J each. A heavier
molecule is slower but carries more mass, and the two effects cancel exactly.
:::

## 10.2 First law of thermodynamics: isothermal, adiabatic, isochoric and isobaric processes; molar heat capacities

### The first law and the sign convention

The first law is conservation of energy written for a gas:

::: key First law of thermodynamics
$$ Q = \Delta U + W $$

$Q$ = heat **supplied to** the gas; $\Delta U$ = rise in its internal energy;
$W$ = work done **by** the gas on its surroundings.
:::

This is the convention used throughout this book, and the one in the NEB syllabus.
Learn it as a sentence: *heat in = rise in internal energy + work out*. Equivalently
$\Delta U = Q - W$.

::: caution Two conventions, one answer
Some books write $\Delta U = Q + W$ with $W$ the work done **on** the gas. The
physics is identical; only the sign of $W$ differs. In an MCQ, decide from the
wording: "work done **by** the gas" is positive when the gas expands. If a question
says "work done on the gas is 100 J", then $W = -100$ J in our convention, so
$\Delta U = Q + 100$.
:::

For an ideal gas, $U$ depends only on $T$, so **in every process whatsoever**

$$ \Delta U = nC_v\Delta T $$

This is the single most useful line in the chapter: it holds for isothermal,
adiabatic, isobaric, isochoric and any crooked path on the $P$–$V$ diagram.

### Work done by a gas

Work is force × displacement, and for a piston of area $A$ pushed through $dx$ the
force is $PA$, so $dW = PA\,dx = P\,dV$:

$$ W = \int_{V_1}^{V_2} P\,dV $$

On a $P$–$V$ diagram this is the **area under the curve**. Work is positive when the
volume increases (expansion) and negative when it decreases (compression). For a
**closed cycle**, the net work is the area enclosed by the loop — positive if the
cycle runs clockwise.

### The four processes

| Process | Held constant | Condition | Work $W$ by gas | $\Delta U$ | $Q$ | Molar heat capacity |
|---|---|---|---|---|---|---|
| Isothermal | $T$ | $PV = $ const | $nRT\ln\frac{V_2}{V_1}$ | 0 | $=W$ | infinite |
| Adiabatic | no heat flow | $PV^\gamma = $ const | $nC_v(T_1-T_2)$ | $nC_v\Delta T$ | 0 | zero |
| Isochoric | $V$ | $W = 0$ | 0 | $nC_v\Delta T$ | $nC_v\Delta T$ | $C_v$ |
| Isobaric | $P$ | $W = P\Delta V$ | $nR\Delta T$ | $nC_v\Delta T$ | $nC_p\Delta T$ | $C_p$ |

Read the table as four answers to one question: *where does the heat go?* At
constant volume it all becomes internal energy. At constant pressure some of it leaks
away as work, so **more heat is needed for the same temperature rise** — that is
exactly why $C_p > C_v$.

```figure caption="The four processes starting from the same state A. Isobaric runs horizontally, isochoric vertically, isothermal is the curve PV = constant, and adiabatic is the steeper curve PV^γ = constant."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.95))
V = np.linspace(1, 3.1, 200)
ax.plot(V, 4/V, color=ACCENT, lw=2.0, label='isothermal')
ax.plot(V, 4/V**1.4, color='#A8271F', lw=2.0, label='adiabatic')
ax.plot([1,3.1],[4,4], color=SERIES[1], lw=2.0, label='isobaric')
ax.plot([1,1],[4,1.0], color=SERIES[3], lw=2.0, label='isochoric')
ax.plot([1],[4], 'o', color=INK, ms=4.5, zorder=5)
ax.text(1.08, 4.22, 'A', fontsize=9, color=INK)
ax.text(2.55, 3.35, 'isobaric', color=SERIES[1], fontsize=8.5, ha='right')
ax.text(1.72, 2.62, 'isothermal', color=ACCENT, fontsize=8.5, ha='left')
ax.text(2.42, 0.72, 'adiabatic', color='#A8271F', fontsize=8.5, ha='left')
ax.text(0.86, 1.55, 'isochoric', color=SERIES[3], fontsize=8.5, rotation=90,
        ha='right', va='center')
ax.set_xlabel('volume  V  (L)'); ax.set_ylabel('pressure  P  (atm)')
ax.set_xlim(0.55,3.6); ax.set_ylim(0.2,4.75)
ax.set_xticks([1,2,3]); ax.set_yticks([1,2,3,4])
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.5)
```

### Isothermal process

Temperature constant, so $\Delta U = 0$ and the first law gives $Q = W$. Since
$P = nRT/V$,

$$ W = \int_{V_1}^{V_2}\frac{nRT}{V}\,dV = nRT\ln\frac{V_2}{V_1}
= nRT\ln\frac{P_1}{P_2} $$

The process must be **slow**, so that heat can flow in or out and keep the
temperature equal to the surroundings throughout. The molar heat capacity of an
isothermal process is formally infinite: heat flows but $\Delta T = 0$.

### Adiabatic process

No heat enters or leaves ($Q = 0$), so $\Delta U = -W$: the gas does work at the
expense of its own internal energy. From $Q = 0$ and $\Delta U = nC_v\Delta T$,

$$ W = -\Delta U = nC_v(T_1-T_2) = \frac{P_1V_1-P_2V_2}{\gamma-1} $$

Combining $PV = nRT$ with $dU + P\,dV = 0$ gives the **adiabatic relations**

$$ PV^\gamma = \text{constant}, \qquad TV^{\gamma-1} = \text{constant}, \qquad
T^\gamma P^{1-\gamma} = \text{constant} $$

::: derivation The adiabatic relation PV^γ = constant
**Starting point.** In an adiabatic process $Q = 0$, so the first law reads
$dU + P\,dV = 0$. We want the relation between $P$ and $V$.

**Step 1 — write $dU$.** For an ideal gas $dU = nC_v\,dT$.

**Step 2 — get $dT$ from the gas law.** Differentiating $PV = nRT$ at constant $n$:
$P\,dV + V\,dP = nR\,dT$, so $n\,dT = (P\,dV + V\,dP)/R$.

**Step 3 — substitute into the first law.**
$\dfrac{C_v}{R}(P\,dV + V\,dP) + P\,dV = 0$.

**Step 4 — clear the fraction and collect.** Multiplying by $R$:
$C_vP\,dV + C_vV\,dP + RP\,dV = 0$, that is
$(C_v+R)P\,dV + C_vV\,dP = 0$. Since $C_v + R = C_p$,
$C_pP\,dV + C_vV\,dP = 0$.

**Step 5 — divide by $C_vPV$.** $\gamma\dfrac{dV}{V} + \dfrac{dP}{P} = 0$.

**Step 6 — integrate.** $\gamma\ln V + \ln P = $ constant, i.e.
$\ln(PV^\gamma) = $ constant.

**Result.** $PV^\gamma = $ constant.

**Conditions.** An ideal gas with constant γ, taken through a **reversible**
(quasi-static) adiabatic process. For a real, fast compression the relation is only
approximate.
:::

An adiabatic **expansion** therefore cools the gas (rising air cools and forms cloud
over the Annapurnas), and an adiabatic **compression** heats it (a bicycle pump warms
up; a diesel engine ignites its fuel with no spark at all).

::: caution Adiabatic is not isothermal
Both can be "fast" or "slow", but they differ in one physical fact: in an adiabatic
process **no heat crosses the boundary**, so the temperature must change. Students
who write $T_1 = T_2$ in an adiabatic expansion lose every mark in the question.
:::

### Adiabatic versus isothermal curves

Both curves fall as $V$ increases, but the adiabatic one falls faster. Differentiate
$PV = $ const: the isothermal slope is $-P/V$. Differentiate $PV^\gamma = $ const: the
adiabatic slope is $-\gamma P/V$. Since $\gamma > 1$, the adiabatic curve is
**steeper by a factor γ** — the two curves cross at the starting point, with the
adiabatic below the isothermal for an expansion and above it for a compression.

### Mayer's relation and the molar heat capacities

::: derivation Cp − Cv = R
**Starting point.** Heat the same $n$ moles of gas through the same $\Delta T$, once
at constant volume and once at constant pressure, and compare the heat needed.

**Step 1 — constant volume.** No work is done ($W = 0$), so all the heat becomes
internal energy:
$Q_v = \Delta U = nC_v\Delta T$.

**Step 2 — constant pressure.** The gas expands and does work
$W = P\Delta V = nR\Delta T$ (using $PV = nRT$ at constant $P$). The same internal
energy change is needed, so
$Q_p = \Delta U + W = nC_v\Delta T + nR\Delta T$.

**Step 3 — compare.** By definition $Q_p = nC_p\Delta T$, so
$nC_p\Delta T = nC_v\Delta T + nR\Delta T$.

**Result.**
$$ C_p - C_v = R, \qquad \gamma = \frac{C_p}{C_v} = 1 + \frac{2}{f} $$

**What it means.** The extra heat at constant pressure pays for the work of
expansion. Because $R > 0$, $C_p$ is always larger than $C_v$ — and the difference is
the same $R$ for every ideal gas, monatomic or not.
:::

The **molar heat capacity of a process** in general is $C = C_v + \dfrac{R}{1-x}$ for
a path $PV^x = $ constant; the table above is the four values worth memorising:
$C_v$ (isochoric), $C_p$ (isobaric), $\infty$ (isothermal), 0 (adiabatic).

::: example Worked example 10.3 — isothermal expansion
**Problem.** 2.0 mol of an ideal gas expands isothermally at 300 K from 10 L to
20 L. Find the work done, the heat supplied and the change in internal energy.

**Solution.** $\Delta U = 0$ (isothermal), so $Q = W$.
$W = nRT\ln\dfrac{V_2}{V_1} = 2\times8.31\times300\times\ln 2
= 4986\times0.693 = 3.46\times10^3$ J.
So $W = Q = 3.46$ kJ and $\Delta U = 0$.

The gas absorbed 3.46 kJ of heat and turned **all** of it into work. That is allowed
for an isothermal process — but only because the gas is not a cyclic engine: it has
expanded once and cannot repeat without being compressed back.
:::

::: example Worked example 10.4 — adiabatic expansion
**Problem.** 1.0 mol of monatomic gas ($\gamma = 1.67$) expands adiabatically from
300 K to 200 K. Find the work done by the gas and the drop in internal energy.

**Solution.** $Q = 0$, so $W = -\Delta U = nC_v(T_1-T_2)$ with
$C_v = \frac{3}{2}R = 12.5$ J mol⁻¹ K⁻¹.
$W = 1.0\times12.5\times100 = 1.25\times10^3$ J.
The internal energy falls by the same 1.25 kJ — the gas paid for the work out of its
own thermal energy, which is why it cooled.
:::

### Cyclic processes

A cyclic process returns the gas to its starting state, so $\Delta U = 0$ over the
cycle and $Q_{net} = W_{net}$ = the area enclosed on the $P$–$V$ diagram. This is
exactly how a heat engine works, and it is where the second law enters.

## 10.3 Second law of thermodynamics: internal-combustion engines, refrigerators and entropy

### The second law

The first law forbids nothing that actually happens: it would happily allow a cup of
tea to heat itself by cooling the room, or an engine to turn the whole of its heat
into work. The second law says which of those energy-conserving processes actually
occur.

::: definition The second law
**Kelvin–Planck statement.** No cyclic engine can convert **all** the heat it absorbs
from a single reservoir into work; some heat must be rejected to a colder sink.

**Clausius statement.** Heat cannot flow **by itself** from a colder body to a hotter
one; work must be done to make it happen.
:::

The two statements are equivalent: an engine that violated one could be used to
violate the other. Both are statements about **direction** — energy conservation
alone does not fix the direction of a process, and the second law does.

### Heat engines

A heat engine takes heat $Q_1$ from a hot reservoir at $T_1$, converts part of it
into work $W$, and rejects the rest $Q_2$ to a cold sink at $T_2$. By the first law
over a cycle, $W = Q_1 - Q_2$. The **efficiency** is

$$ \eta = \frac{W}{Q_1} = \frac{Q_1-Q_2}{Q_1} = 1 - \frac{Q_2}{Q_1} $$

The **Carnot engine** is the best possible engine between two temperatures: it uses
two isothermal and two adiabatic steps, all reversible. For it $Q_2/Q_1 = T_2/T_1$,
so

$$ \eta_{Carnot} = 1 - \frac{T_2}{T_1} $$

```figure caption="The Carnot cycle on a P–V diagram: isothermal expansion at T₁, adiabatic expansion, isothermal compression at T₂, adiabatic compression back to the start. The shaded area is the net work done in one cycle."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9,2.9))
g = 5/3
VA, PA, VB, PB = 1.0, 6.0, 2.0, 3.0
r = (600/300)**(1/(g-1))
VC, VD = VB*r, VA*r
PC, PD = PB*(VB/VC)**g, PA*(VA/VD)**g
vAB = np.linspace(VA, VB, 60); pAB = PA*VA/vAB
vBC = np.linspace(VB, VC, 60); pBC = PB*(VB/vBC)**g
vCD = np.linspace(VC, VD, 60); pCD = PC*VC/vCD
vDA = np.linspace(VD, VA, 60); pDA = PD*(VD/vDA)**g
V = np.concatenate([vAB, vBC, vCD, vDA]); P = np.concatenate([pAB, pBC, pCD, pDA])
ax.fill(V, P, color=ACCENT, alpha=0.14, lw=0)
ax.plot(vAB, pAB, color=ACCENT, lw=2.0)
ax.plot(vBC, pBC, color='#A8271F', lw=2.0)
ax.plot(vCD, pCD, color=ACCENT, lw=2.0)
ax.plot(vDA, pDA, color='#A8271F', lw=2.0)
for vv, pp, nm, dx, dy in [(VA,PA,'A',-0.16,0.28),(VB,PB,'B',-0.10,0.28),
                           (VC,PC,'C',0.12,-0.30),(VD,PD,'D',0.05,0.30)]:
    ax.plot([vv],[pp],'o', color=INK, ms=4, zorder=5)
    ax.text(vv+dx, pp+dy, nm, fontsize=9, color=INK)
ax.text(1.30, 5.55, 'T₁ = 600 K', color=ACCENT, fontsize=8.5, ha='left')
ax.text(3.30, 0.30, 'T₂ = 300 K', color=ACCENT, fontsize=8.5, ha='left')
ax.annotate('W = area', xy=(2.55, 1.55), xytext=(3.55, 2.55), fontsize=8.5, color=INK,
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.8, mutation_scale=8))
ax.set_xlabel('volume  V  (arbitrary units)'); ax.set_ylabel('pressure  P  (arbitrary units)')
ax.set_xlim(0.4,6.4); ax.set_ylim(0.05,6.9)
ax.set_xticks([1,2,3,4,5,6]); ax.set_yticks([1,2,3,4,5,6])
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.5)
```

::: caution Use kelvin in the efficiency
$\eta = 1 - T_2/T_1$ needs **absolute** temperatures. An engine working between
27 °C and 127 °C has $T_1 = 400$ K and $T_2 = 300$ K, so $\eta = 1 - 300/400 = 25\%$,
**not** $1 - 27/127 = 79\%$. The wrong calculation always gives a number that looks
impressive and is impossible — a useful check in itself.
:::

::: example Worked example 10.5 — engine between two reservoirs
**Problem.** A Carnot engine works between 500 K and 300 K and absorbs 1000 J per
cycle from the hot reservoir. Find its efficiency, the work done and the heat
rejected.

**Solution.** $\eta = 1 - \dfrac{300}{500} = 0.40 = 40\%$.
$W = \eta Q_1 = 0.40\times1000 = 400$ J.
$Q_2 = Q_1 - W = 600$ J.

No engine operating between these two temperatures can beat 40 %; a real engine with
friction and heat losses will be well below it.
:::

### Refrigerators and heat pumps

A refrigerator is a heat engine run backwards: work $W$ is supplied to pump heat
$Q_2$ out of the cold space and reject $Q_1 = Q_2 + W$ to the warm room. Its
performance is measured by the **coefficient of performance**

$$ \text{COP} = \frac{Q_2}{W} = \frac{Q_2}{Q_1-Q_2}
\qquad\Longrightarrow\qquad \text{(Carnot)}\quad \frac{T_2}{T_1-T_2} $$

A heat pump is the same machine used the other way round: what you want is $Q_1$,
the heat delivered to the warm space, so its COP is $Q_1/W = T_1/(T_1-T_2)$, which
is exactly **COP$_{fridge}$ + 1**. That is why a heat pump can deliver more heat than
the electrical energy it consumes — it is moving heat, not making it.

```figure caption="Energy bookkeeping for a heat engine (left) and a refrigerator (right). Both obey the first law; they differ in which arrow is the desired output."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.1,2.9))
def block(x, y, w, h, txt):
    ax.add_patch(plt.Rectangle((x-w/2, y-h/2), w, h, fc='white', ec=INK, lw=1.0, zorder=3))
    ax.text(x, y, txt, ha='center', va='center', fontsize=8.5, color=INK, zorder=4)
def arrow(x1, y1, x2, y2, txt, tx, ty, col=INK):
    ax.annotate('', xy=(x2,y2), xytext=(x1,y1),
                arrowprops=dict(arrowstyle='-|>', color=col, lw=1.3, mutation_scale=10))
    ax.text(tx, ty, txt, fontsize=8.5, color=col, ha='center', va='center')
block(1.35, 1.75, 1.05, 0.62, 'engine')
arrow(1.35, 2.75, 1.35, 2.10, 'Q₁', 1.62, 2.45)
arrow(1.90, 1.75, 2.55, 1.75, 'W', 2.22, 1.98)
arrow(1.35, 1.42, 1.35, 0.80, 'Q₂', 1.62, 1.10)
ax.text(1.35, 3.02, 'hot  T₁', fontsize=8, color=MUTED, ha='center')
ax.text(1.35, 0.60, 'cold  T₂', fontsize=8, color=MUTED, ha='center')
block(3.95, 1.75, 1.25, 0.62, 'refrigerator')
arrow(3.95, 0.80, 3.95, 1.42, 'Q₂', 4.22, 1.10)
arrow(5.25, 1.75, 4.62, 1.75, 'W', 4.95, 1.98)
arrow(3.95, 2.10, 3.95, 2.75, 'Q₁', 4.22, 2.45)
ax.text(3.95, 3.02, 'room  T₁', fontsize=8, color=MUTED, ha='center')
ax.text(3.95, 0.60, 'food  T₂', fontsize=8, color=MUTED, ha='center')
ax.set_xlim(0.55,5.6); ax.set_ylim(0.35,3.25); ax.axis('off')
```

::: example Worked example 10.6 — the kitchen refrigerator
**Problem.** A refrigerator keeps its compartment at 250 K and rejects heat to a
kitchen at 300 K. What is the best possible COP, and how much heat can it remove per
joule of electrical work?

**Solution.** $\text{COP} = \dfrac{T_2}{T_1-T_2} = \dfrac{250}{50} = 5$.
With 1 J of work it removes up to 5 J from the food and delivers 6 J to the kitchen.
This is why a refrigerator is a *heat pump* for the room: leave the door open and the
room warms, because the 6 J rejected exceeds the 1 J consumed.
:::

### Internal-combustion engines

An internal-combustion engine burns fuel **inside** the cylinder, so the hot gas
itself is the working substance. The four-stroke cycle:

| Stroke | What happens | Valves |
|---|---|---|
| Induction (suction) | Piston moves down, air–fuel mixture is drawn in | inlet open |
| Compression | Piston moves up, mixture compressed adiabatically and heated | both closed |
| Power (expansion) | Spark ignites the mixture; hot gas pushes the piston down | both closed |
| Exhaust | Piston moves up, burnt gas pushed out | exhaust open |

The petrol engine approximates the **Otto cycle** (two adiabatic and two isochoric
steps), whose ideal efficiency is

$$ \eta_{Otto} = 1 - \frac{1}{r^{\gamma-1}} $$

where $r = V_1/V_2$ is the compression ratio. Higher compression means higher
efficiency, which is why a diesel engine (compression ratio 15–20, fuel ignited by
the heat of compression alone) is more efficient than a petrol engine (ratio 8–10).
Real efficiencies are 25–30 % for petrol and 35–40 % for diesel — far below the
Carnot limit, because of friction, heat lost through the cylinder walls, incomplete
combustion and the energy carried away by the exhaust.

### Entropy

::: definition Entropy
Entropy $S$ is a measure of the **disorder** of a system. For a reversible change at
temperature $T$,
$$ \Delta S = \frac{Q}{T} \qquad (\text{unit J K}^{-1}) $$
and Boltzmann's form is $S = k\ln W$, where $W$ is the number of microscopic ways the
state can be arranged.
:::

The second law in its entropy form: **the entropy of an isolated system never
decreases.** For a reversible process $\Delta S = 0$; for every real (irreversible)
process $\Delta S > 0$. Heat flowing from a hot body to a cold one increases the
total entropy; the reverse would decrease it and never happens by itself. An engine
cannot be perfect because the heat it must reject carries entropy away, and that
entropy has to go somewhere.

| Statement | What it forbids |
|---|---|
| Kelvin–Planck | an engine with $\eta = 1$ |
| Clausius | a refrigerator with no work input |
| Entropy | any spontaneous process that lowers the entropy of an isolated system |

```photogrid label="10.1" cols="2" ratio="1.2" caption="Hot air is lighter air. (a) The burner raises the temperature of the air in the envelope, which stays open at the bottom so its pressure stays at atmospheric. (b) For an envelope of 2,800 m^3 in air at 20 C (density 1.204 kg/m^3) the ideal-gas law gives density in proportion to 1/T. At 100 C the inside density is 0.946 kg/m^3 and the lift is (rho_out - rho_in) V = 723 kg of payload. The envelope holds 116,406 mol of cold air but only 91,449 mol when hot, so 24,956 mol leave through the mouth."
@ photo id="ceephy/burner" cap="A hot-air balloon burner warms the air inside the envelope"
fit 1.2
focus 0.5 0.5
@ svg cap="Lift of a 2,800 cubic metre balloon against air temperature"
V = 2800.0; P = 101325.0; R = 8.314; T0 = 293.15; rho0 = 1.204
rho = lambda T: rho0 * T0 / T
lift = lambda Tc: (rho0 - rho(Tc + 273.15)) * V
n_out = P * V / (R * T0); n_in = P * V / (R * 373.15)
assert 720 < lift(100) < 725 and abs(n_out - 116_400) < 400 and n_out > n_in
facts = dict(rin="%.3f" % rho(373.15), lift="%.0f" % lift(100), nout="{:,.0f}".format(n_out), nin="{:,.0f}".format(n_in), esc="{:,.0f}".format(n_out - n_in))
f = Fig(300, 236)
f.text(150, 14, "Lift (kg) = (rho out - rho in) V", size=10.5, color=NAVY, bold=True)
X = lambda T: 44 + (T - 20) * 2.2; Y = lambda m: 160 - m * 0.13
f.line(X(20), Y(0), 280, Y(0), color=SLATE, sw=1.4); f.line(X(20), Y(0), X(20), 34, color=SOFT, sw=1.2)
pts = [(X(T), Y(lift(T))) for T in range(20, 121, 4)]
for (a, b), (c, d) in zip(pts, pts[1:]): f.line(a, b, c, d, color=AMBER, sw=2.6)
f.line(X(100), Y(0), X(100), Y(lift(100)), color=TEAL, sw=1.2, dash=True)
f.circle(X(100), Y(lift(100)), 4, fill=TEAL, stroke=TEAL)
f.text(X(100) - 8, Y(lift(100)) - 10, "%.0f kg" % lift(100), size=10.5, color=TEAL, bold=True, anchor="end")
for T in (20, 60, 100): f.text(X(T), Y(0) + 13, "%d C" % T, size=10.5, color=SLATE)
for m in (250, 500, 750): f.text(38, Y(m), "%d" % m, size=10.5, color=SLATE, anchor="end", vmid=True)
f.text(150, 192, "inside density %.3f vs 1.204 kg/m^3" % rho(373.15), size=10.5, color=NAVY, bold=True)
f.text(150, 210, "cold %.0f mol, hot %.0f mol" % (n_out, n_in), size=10.5, color=NAVY, bold=True)
f.text(150, 228, "%.0f mol escape: n = PV / RT" % (n_out - n_in), size=10.5, color=NAVY, bold=True)
```

```photogrid label="10.2" cols="2" ratio="1.2" caption="The colder the box, the more the work. (a) The compressor is the heart of a refrigeration plant: it compresses the vapour of the refrigerant, which then condenses and gives heat to the surroundings. (b) The coefficient of performance of an ideal (Carnot) refrigerator is Tc / (Th - Tc). With the kitchen at 30 degrees C the ideal COP is 10.66 for a refrigerator at 4 degrees C, but only 5.32 for a freezer at -18 degrees C. To take 1000 kJ out of the freezer the ideal machine needs 188 kJ of work, and a real machine with a COP of 2.5 needs 400 kJ. The heat rejected at the back is always the heat removed plus the work done."
@ photo id="ceephy3/compressor" cap="The reciprocating compressor of a refrigeration plant"
fit 1.2
focus 0.5 0.5
@ svg cap="Coefficient of performance of a refrigerator"
Th = 303.15
rows = []
for tc in (10, 4, -5, -18):
    T = tc + 273.15
    rows.append(("%d C" % tc, T / (Th - T)))
assert round(rows[1][1], 2) == 10.66 and round(rows[3][1], 2) == 5.32
W_ideal = 1000 / rows[3][1]
W_real = 1000 / 2.5
f = Fig(300, 236)
f.text(150, 12, "Carnot COP, kitchen at 30 C", size=10.5, color=NAVY, bold=True)
hbars(f, rows, vmax=15, fmt="%.2f", x0=52, y0=30, bw=170, gap=30,
      colors=[(BLUE, NAVY), (MINT, TEAL), (SAND, AMBER), (ROSE, RED)])
f.text(150, 158, "inside temperature shown; COP = Tc / (Th - Tc)", size=10, color=SLATE, bold=True)
f.text(150, 180, "removing 1000 kJ from a -18 C freezer:", size=10.5, color=NAVY, bold=True)
f.text(150, 200, "ideal work %.0f kJ, real (COP 2.5) %.0f kJ" % (W_ideal, W_real), size=10.5, color=NAVY, bold=True)
f.text(150, 218, "colder inside means more work per joule", size=10, color=SLATE, bold=True)
facts = dict(c4=rows[1][1], c18=rows[3][1], wi=W_ideal, wr=W_real)
```

## Formula and fact sheet

| Topic | Formula or fact |
|---|---|
| Ideal gas | $PV = nRT = NkT$; $R = 8.31$ J mol⁻¹ K⁻¹, $k = 1.38\times10^{-23}$ J K⁻¹ |
| Other forms | $P = \rho RT/M$; $\rho = PM/RT$; $P_1V_1/T_1 = P_2V_2/T_2$ |
| Constants | $R = N_Ak$; $N_A = 6.02\times10^{23}$; 1 mol = 22.4 L at STP |
| Kinetic pressure | $P = \frac{1}{3}\rho c_{rms}^2 = \frac{1}{3}\frac{mN}{V}\overline{c^2}$ |
| Speeds | $c_{rms} = \sqrt{3RT/M} = \sqrt{3kT/m} = \sqrt{3P/\rho}$; $c_{avg} = \sqrt{8RT/\pi M}$; $c_{mp} = \sqrt{2RT/M}$ |
| Speed ratio | $c_{mp} : c_{avg} : c_{rms} = 1.41 : 1.60 : 1.73$ |
| Kinetic energy | $\frac{3}{2}kT$ per molecule; $\frac{3}{2}RT$ per mole; total $\frac{3}{2}nRT = \frac{3}{2}PV$ |
| Degrees of freedom | monatomic 3, diatomic 5, polyatomic 6 |
| Heat capacities | $C_v = \frac{f}{2}R$; $C_p = C_v + R$; $\gamma = 1 + 2/f$ |
| γ values | 1.67 (monatomic), 1.40 (diatomic), 1.33 (polyatomic) |
| First law | $Q = \Delta U + W$; $W$ = work **by** the gas; $\Delta U = nC_v\Delta T$ always |
| Work | $W = \int P\,dV$ = area under the $P$–$V$ curve |
| Isothermal | $\Delta U = 0$, $Q = W = nRT\ln(V_2/V_1)$, $PV = $ const, $C = \infty$ |
| Adiabatic | $Q = 0$, $W = nC_v(T_1-T_2) = \frac{P_1V_1-P_2V_2}{\gamma-1}$, $PV^\gamma = $ const, $C = 0$ |
| Isochoric | $W = 0$, $Q = \Delta U = nC_v\Delta T$, $C = C_v$ |
| Isobaric | $W = nR\Delta T$, $Q = nC_p\Delta T$, $C = C_p$ |
| Slopes on $P$–$V$ | isothermal $-P/V$; adiabatic $-\gamma P/V$ (steeper by γ) |
| Cycle | $\Delta U = 0$, $Q_{net} = W_{net}$ = enclosed area |
| Engine | $\eta = W/Q_1 = 1 - Q_2/Q_1$; Carnot $\eta = 1 - T_2/T_1$ (kelvin) |
| Refrigerator | COP $= Q_2/W = T_2/(T_1-T_2)$; heat pump COP $= T_1/(T_1-T_2)$ |
| Otto cycle | $\eta = 1 - 1/r^{\gamma-1}$ |
| Entropy | $\Delta S = Q/T$ (reversible); $\Delta S \ge 0$ for an isolated system; $S = k\ln W$ |

## Chapter summary

- $PV = nRT = NkT$; $R = N_Ak$; $P = \rho RT/M$. Temperature must be in kelvin, and
  one mole of any gas occupies 22.4 L at STP.
- Kinetic theory gives $P = \frac{1}{3}\rho c_{rms}^2$, hence
  $c_{rms} = \sqrt{3RT/M}$: at the same temperature the lighter gas is faster, and
  doubling $c_{rms}$ needs four times the absolute temperature.
- Average translational kinetic energy is $\frac{3}{2}kT$ per molecule whatever the
  gas; the internal energy of an ideal gas depends only on $T$.
- Degrees of freedom 3, 5, 6 give $C_v = \frac{f}{2}R$, $C_p = C_v + R$ and γ = 1.67,
  1.40, 1.33. $C_p > C_v$ because the extra heat at constant pressure does work.
- First law: $Q = \Delta U + W$ with $W$ done **by** the gas; $\Delta U = nC_v\Delta T$
  in every process.
- Isothermal: $\Delta U = 0$, $Q = W = nRT\ln(V_2/V_1)$. Adiabatic: $Q = 0$,
  $W = -\Delta U$, $PV^\gamma$ constant, and the curve is γ times steeper.
  Isochoric: $W = 0$, all the heat goes to internal energy. Isobaric:
  $W = nR\Delta T$, $Q = nC_p\Delta T$.
- A cycle has $\Delta U = 0$, so $Q_{net} = W_{net}$ = the area enclosed.
- $\eta = 1 - Q_2/Q_1 \le 1 - T_2/T_1$, with kelvin temperatures; a real engine is
  always below the Carnot value.
- A refrigerator moves heat with COP $= Q_2/W = T_2/(T_1-T_2)$; run with the door open
  it warms the room.
- The entropy of an isolated system never decreases; that is the second law in one
  line.

## Practice questions

**Set A — Recall (28 questions)**

1. For $n$ moles of an ideal gas the equation of state is
   (a) $PV = nRT^2$ (b) $PV = nRT$ (c) $P/V = nRT$ (d) $PV = nR/T$
2. The value of the universal gas constant R is
   (a) 8.31 J mol⁻¹ K⁻¹ (b) 1.38 × 10⁻²³ J K⁻¹ (c) 6.02 × 10²³ mol⁻¹ (d) 4.18 J cal⁻¹
3. The volume occupied by 1 mole of an ideal gas at STP is about
   (a) 11.2 L (b) 24.0 L (c) 2.24 L (d) 22.4 L
4. The pressure of an ideal gas of density ρ is
   (a) $\rho c_{rms}^2$ (b) $\frac{1}{2}\rho c_{rms}^2$ (c) $\frac{1}{3}\rho c_{rms}^2$ (d) $3\rho c_{rms}^2$
5. The rms speed of molecules of molar mass M at temperature T is
   (a) $\sqrt{2RT/M}$ (b) $\sqrt{3RT/M}$ (c) $\sqrt{RT/M}$ (d) $3RT/M$
6. The average translational kinetic energy of one gas molecule is
   (a) kT (b) ½kT (c) (5/2)kT (d) (3/2)kT
7. The number of degrees of freedom of a monatomic gas molecule is
   (a) 3 (b) 5 (c) 6 (d) 2
8. At ordinary temperature a diatomic gas molecule has
   (a) 2 (b) 3 (c) 5 (d) 7 degrees of freedom
9. For a monatomic ideal gas, γ = Cp/Cv is
   (a) 1.40 (b) 1.67 (c) 1.33 (d) 1.00
10. For a diatomic ideal gas at room temperature, γ is about
   (a) 1.40 (b) 1.67 (c) 1.33 (d) 1.20
11. Mayer's relation for an ideal gas is
   (a) Cp + Cv = R (b) Cp/Cv = R (c) Cp − Cv = γ (d) Cp − Cv = R
12. Taking Q as heat supplied to the gas and W as work done by it, the first law is
   (a) Q = W − ΔU (b) ΔU = Q + W (c) Q = ΔU + W (d) W = Q + ΔU
13. For an ideal gas taken through an isothermal process
   (a) Q = 0 (b) ΔU = 0 (c) W = 0 (d) ΔU = Q
14. In an adiabatic process
   (a) Q = 0 (b) W = 0 (c) ΔU = 0 (d) P is constant
15. In an isochoric process the work done by the gas is
   (a) PΔV (b) nRT ln(V₂/V₁) (c) nCpΔT (d) zero
16. In an isobaric process the work done by the gas is
   (a) zero (b) nCvΔT (c) PΔV (d) nCpΔT
17. The work done by n moles of gas in a reversible isothermal expansion from V₁ to V₂ is
   (a) nCv(T₂ − T₁) (b) nRT ln(V₂/V₁) (c) P(V₂ − V₁) (d) nR(T₂ − T₁)
18. For a reversible adiabatic process in an ideal gas
   (a) PV^γ = constant (b) PV = constant (c) P/V = constant (d) PV^(1/γ) = constant
19. The Kelvin–Planck statement of the second law says that no engine can
   (a) absorb heat from a hot body (b) reject heat to a cold body (c) work in cycles (d) convert all the heat absorbed into work
20. The efficiency of a Carnot engine working between T₁ and T₂ is
   (a) 1 − T₁/T₂ (b) T₂/T₁ (c) 1 − T₂/T₁ (d) (T₁ − T₂)/T₂
21. The coefficient of performance of a refrigerator is
   (a) W/Q₁ (b) Q₂/W (c) W/Q₂ (d) Q₁/W
22. The SI unit of entropy is
   (a) J K⁻¹ (b) J (c) J kg⁻¹ K⁻¹ (d) W K⁻¹
23. The entropy change in a reversible adiabatic process is
   (a) positive (b) negative (c) infinite (d) zero
24. The universal gas constant R is equal to
   (a) N_A/k (b) k/N_A (c) N_Ak (d) N_A + k
25. The SI unit of molar heat capacity is
   (a) J K⁻¹ (b) J mol⁻¹ K⁻¹ (c) J kg⁻¹ K⁻¹ (d) mol K⁻¹
26. For an ideal gas the internal energy depends only on its
   (a) temperature (b) pressure (c) volume (d) density
27. An ideal gas expands into a vacuum inside a thermally insulated container. Its temperature
   (a) rises (b) falls (c) falls to zero (d) stays the same
28. A petrol engine works on the
   (a) Carnot cycle (b) diesel cycle (c) Otto cycle (d) Rankine cycle

::: note Answers and explanations — Set A
**1.** (b) — the equation of state is PV = nRT. Option (a) has T squared, and (d) divides by T instead of multiplying.
**2.** (a) — R = 8.31 J mol⁻¹ K⁻¹. Option (b) is Boltzmann's constant and (c) is Avogadro's number.
**3.** (d) — at 273 K and 1 atm, V = RT/P = 8.31 × 273/1.01 × 10⁵ = 22.4 × 10⁻³ m³ = 22.4 L.
**4.** (c) — from kinetic theory P = ⅓ρc²ᵣₘₛ. The factor ⅓ comes from the three directions of motion.
**5.** (b) — c_rms = √(3RT/M). Option (a) is the most probable speed and (c) is missing the 3.
**6.** (d) — three translational degrees of freedom at ½kT each. Option (c) would be the total energy including rotation.
**7.** (a) — a point atom can move in three independent directions only.
**8.** (c) — three translational plus two rotational; rotation about the bond carries no energy.
**9.** (b) — f = 3 gives γ = 1 + 2/3 = 1.67. Option (a) is the diatomic value.
**10.** (a) — f = 5 gives γ = 1 + 2/5 = 1.40, which is why air is treated as γ = 1.4.
**11.** (d) — Cp − Cv = R; the difference is the work done in expanding at constant pressure.
**12.** (c) — heat in = rise in internal energy + work out.
**13.** (b) — the temperature does not change, and for an ideal gas U depends only on T, so ΔU = 0.
**14.** (a) — "adiabatic" means no heat crosses the boundary. W is not zero unless the volume is fixed.
**15.** (d) — W = PΔV and ΔV = 0 at constant volume.
**16.** (c) — at constant pressure the work is PΔV = nRΔT.
**17.** (b) — integrating P = nRT/V over the volume gives nRT ln(V₂/V₁).
**18.** (a) — PV^γ = constant; the exponent is γ, greater than 1, so the curve is steeper than an isotherm.
**19.** (d) — a cyclic engine must reject some heat to a sink; 100 % conversion is forbidden.
**20.** (c) — η = 1 − T₂/T₁ with absolute temperatures. Option (a) has the ratio upside down.
**21.** (b) — COP is what you get (heat removed) divided by what you pay (work).
**22.** (a) — entropy is heat divided by temperature, J/K.
**23.** (d) — Q = 0, so ΔS = Q/T = 0. A reversible adiabatic process is isentropic.
**24.** (c) — R = N_Ak, the gas constant per mole is Avogadro's number times the constant per molecule.
**25.** (b) — heat per mole per kelvin.
**26.** (a) — with no intermolecular potential energy, U is purely kinetic and therefore depends only on T.
**27.** (d) — Q = 0 (insulated) and W = 0 (expanding against nothing), so ΔU = 0 and T is unchanged.
**28.** (c) — the Otto cycle: two adiabatic and two isochoric steps.
:::

**Set B — Understanding (17 questions)**

1. Hydrogen (M = 2) and oxygen (M = 32) are at the same temperature. The rms speed of hydrogen molecules is
   (a) 16 times that of oxygen (b) one quarter of that of oxygen (c) 4 times that of oxygen (d) the same as that of oxygen
2. A gas is heated at constant pressure. The heat supplied is used to
   (a) raise the internal energy only (b) do work only (c) raise the temperature only (d) raise the internal energy and do work of expansion
3. On a P–V diagram the adiabatic curve through a point is steeper than the isothermal curve because
   (a) the adiabatic process is always slower (b) the pressure falls faster when no heat enters to keep T constant (c) the temperature rises during an adiabatic expansion (d) γ is less than 1
4. Cp is greater than Cv because at constant pressure
   (a) the gas does work as it expands (b) the temperature rises faster (c) no heat is supplied (d) the gas becomes denser
5. A gas is compressed adiabatically. Its temperature
   (a) falls, because Q = 0 (b) stays the same (c) rises, because the work done on it raises its internal energy (d) falls, because the volume decreases
6. An ideal gas undergoes free expansion into a vacuum. Which is correct?
   (a) Q > 0 and W > 0 (b) Q = 0, W = 0 and ΔU = 0 (c) Q = 0 and W > 0 (d) ΔU > 0
7. The efficiency of a real heat engine is always less than the Carnot efficiency because
   (a) the second law forbids engines altogether (b) a Carnot cycle cannot be drawn (c) heat cannot be rejected to a sink (d) of friction, heat losses and irreversible processes
8. A refrigerator is run with its door open in a closed, insulated room. The room
   (a) warms up (b) cools down (c) stays at the same temperature (d) cools first, then warms
9. For any process in an isolated system, the entropy
   (a) always decreases (b) stays constant (c) never decreases (d) becomes zero
10. No heat engine can have an efficiency of 100 % because
   (a) fuels burn incompletely (b) it would have to reject no heat at all (c) friction can never be removed (d) the working substance would freeze
11. The same gas is heated through the same ΔT, once at constant volume and once at constant pressure. The heat needed is
   (a) greater at constant pressure (b) greater at constant volume (c) the same in both cases (d) zero at constant pressure
12. The rms speed of gas molecules becomes double when the absolute temperature is
   (a) doubled (b) halved (c) made eight times (d) made four times
13. The average translational kinetic energy of gas molecules depends on
   (a) the gas and its pressure (b) only the absolute temperature (c) only the volume (d) the molar mass of the gas
14. A gas is heated at constant volume. All the heat supplied
   (a) does work of expansion (b) is lost to the surroundings (c) raises the internal energy (d) is converted into entropy
15. In a cyclic process the net heat supplied to the gas equals
   (a) the net work done by it (b) the change in its internal energy (c) zero in every case (d) the heat rejected
16. In an isobaric expansion of an ideal gas, the fraction of the heat supplied that appears as work is
   (a) 1 (b) 1/γ (c) γ (d) (γ − 1)/γ
17. Heat flows by itself from a hot body to a cold one. The reverse transfer
   (a) never happens in any device (b) happens only if work is done on the system (c) happens if the temperature difference is small (d) happens in an isolated system

::: note Answers and explanations — Set B
**1.** (c) — c_rms ∝ 1/√M, so the ratio is √(32/2) = 4. Option (a) is the ratio of the molar masses, not of the speeds.
**2.** (d) — at constant pressure the gas expands, so some heat becomes work and the rest raises U; Q = nCpΔT accounts for both.
**3.** (b) — the isothermal slope is −P/V and the adiabatic slope is −γP/V; with γ > 1 the adiabatic falls faster.
**4.** (a) — the extra heat Cp − Cv = R per mole is exactly the work of expansion PΔV = RΔT.
**5.** (c) — Q = 0, so ΔU = −W; compressing means W < 0, hence ΔU > 0 and T rises. This is how a diesel engine ignites its fuel.
**6.** (b) — no heat crosses the insulated wall and the gas pushes against nothing, so W = 0; ΔU = 0 and T is unchanged.
**7.** (d) — the Carnot efficiency is the reversible limit; friction, heat leaks and finite-time operation all cost real engines.
**8.** (a) — the refrigerator delivers Q₁ = Q₂ + W to the room, and Q₁ exceeds the electrical work W, so the room gains net energy.
**9.** (c) — the second law: ΔS ≥ 0 for an isolated system, with equality only for reversible processes.
**10.** (b) — η = 1 − Q₂/Q₁ = 1 needs Q₂ = 0, i.e. no heat rejected, which the Kelvin–Planck statement forbids.
**11.** (a) — Cp > Cv, because at constant pressure part of the heat becomes work of expansion.
**12.** (d) — c_rms ∝ √T, so doubling the speed needs T multiplied by 4.
**13.** (b) — ½m c²_rms = (3/2)kT, which contains T and nothing else.
**14.** (c) — no expansion means W = 0, so Q = ΔU entirely.
**15.** (a) — ΔU = 0 over a complete cycle, so Q = W; the work is the area enclosed by the loop.
**16.** (d) — W/Q = nRΔT/(nCpΔT) = R/Cp = (γ − 1)/γ, which is 0.4 for a monatomic gas.
**17.** (b) — that is the Clausius statement: a refrigerator must be driven by work.
:::

**Set C — Application (11 questions)**

1. 2.0 mol of an ideal gas expands isothermally at 300 K from 10 L to 20 L. The work done is
   (a) 1.73 kJ (b) 3.46 kJ (c) 4.99 kJ (d) 6.93 kJ
2. The rms speed of oxygen molecules (M = 32 g mol⁻¹) at 300 K is about
   (a) 279 m s⁻¹ (b) 394 m s⁻¹ (c) 483 m s⁻¹ (d) 683 m s⁻¹
3. The average translational kinetic energy of a gas molecule at 300 K is
   (a) 6.2 × 10⁻²¹ J (b) 4.1 × 10⁻²¹ J (c) 2.1 × 10⁻²¹ J (d) 1.2 × 10⁻²⁰ J
4. 1.0 mol of monatomic gas expands adiabatically from 300 K to 200 K. The work done by the gas is
   (a) 2.08 kJ (b) 0.83 kJ (c) 1.66 kJ (d) 1.25 kJ
5. A Carnot engine works between 500 K and 300 K. Its efficiency is
   (a) 20 % (b) 60 % (c) 40 % (d) 80 %
6. A Carnot engine works between 127 °C and 27 °C. Its efficiency is
   (a) 25 % (b) 40 % (c) 21 % (d) 79 %
7. A refrigerator works between 250 K and 300 K. Its maximum coefficient of performance is
   (a) 0.2 (b) 5 (c) 6 (d) 1.2
8. An engine takes 800 J from its hot reservoir and delivers 200 J of work per cycle. The heat rejected per cycle is
   (a) 200 J (b) 400 J (c) 600 J (d) 1000 J
9. A fixed mass of gas at 27 °C is heated at constant volume until its pressure doubles. Its new temperature is
   (a) 327 °C (b) 54 °C (c) 600 °C (d) 150 °C
10. The heat needed to raise the temperature of 2.0 mol of a diatomic gas by 20 K at constant pressure is
   (a) 832 J (b) 1.16 kJ (c) 333 J (d) 2.32 kJ
11. 2.0 mol of an ideal gas is heated through 100 K at constant pressure. The work done by the gas is
   (a) 0.83 kJ (b) 2.08 kJ (c) 1.16 kJ (d) 1.66 kJ

::: note Answers and explanations — Set C
**1.** (b) — W = nRT ln(V₂/V₁) = 2 × 8.31 × 300 × ln 2 = 4986 × 0.693 = 3.46 kJ. Option (d) uses ln 4 by mistake.
**2.** (c) — c_rms = √(3RT/M) = √(3 × 8.31 × 300/0.032) = √(2.34 × 10⁵) = 483 m s⁻¹. Option (b) is the most probable speed √(2RT/M).
**3.** (a) — (3/2)kT = 1.5 × 1.38 × 10⁻²³ × 300 = 6.2 × 10⁻²¹ J. Option (b) is kT, which omits the 3/2.
**4.** (d) — Q = 0, so W = nCv(T₁ − T₂) = 1 × 12.5 × 100 = 1.25 kJ. Option (a) wrongly uses Cp.
**5.** (c) — η = 1 − 300/500 = 0.40. Option (b) is Q₂/Q₁ = T₂/T₁, the fraction *rejected*, not the efficiency.
**6.** (a) — convert first: T₁ = 400 K, T₂ = 300 K, so η = 1 − 300/400 = 25 %. Option (d) is the °C blunder, 1 − 27/127; option (c) is the ratio 27/127 itself.
**7.** (b) — COP = T₂/(T₁ − T₂) = 250/50 = 5. Option (c) is the heat pump COP, which is one larger.
**8.** (c) — Q₂ = Q₁ − W = 800 − 200 = 600 J. The efficiency is 25 %, but the question asks for the heat rejected.
**9.** (a) — at constant V, P ∝ T, so T doubles from 300 K to 600 K, which is 327 °C. Option (b) doubles the Celsius reading instead.
**10.** (b) — Q = nCpΔT = 2 × 29.1 × 20 = 1.16 kJ. Option (a) uses Cv, which would be right only at constant volume; (c) is only the work nRΔT; (d) doubles ΔT.
**11.** (d) — W = PΔV = nRΔT = 2 × 8.31 × 100 = 1.66 kJ. Option (b) is the heat nCpΔT, (c) is nCvΔT, and (a) is nRΔT for 1 mol.
:::

**Group D — Model answers for long questions (10 marks each, for deeper revision)**

1. Derive the pressure exerted by an ideal gas on the basis of kinetic theory and find the rms speed and the mean kinetic energy per molecule. <span class="marks">[10]</span>
2. State the first and second laws of thermodynamics, explain the thermodynamic processes and the Carnot engine, and solve a numerical. <span class="marks">[10]</span>

```photogrid label="10.H" cols="2" ratio="1.4" caption="Gases and engines. (a) The fire piston compresses air so quickly (adiabatically) that its temperature rises enough to ignite tinder. (b) An air compressor does work on gas, raising its pressure and temperature."
@ photo id="phy12b/firepiston" cap="(a) Fire piston"
fit 1.4
focus 0.5 0.5
@ photo id="ceephy3/compressor" cap="(b) Air compressor"
fit 1.4
focus 0.5 0.5
```

### Model answer D1: kinetic theory of gases (10 marks)

**Introduction.** The kinetic theory explains the large-scale properties of a gas from the motion of its molecules.

**Assumptions.** A gas consists of a very large number of identical, tiny molecules in random motion. The collisions are perfectly elastic, there is no force between molecules except during a collision, the volume of the molecules is negligible, and the time of collision is negligible compared with the time between collisions.

**Derivation.** Take $N$ molecules of mass $m$ in a cubical box of side $L$. A molecule moving with velocity component $v_x$ hits a wall and rebounds, so the change of momentum is $2mv_x$. It hits the same wall every $2L/v_x$ seconds, so the force it produces is $mv_x^2/L$. For all molecules, $F = \dfrac{m}{L}\sum v_x^2 = \dfrac{Nm\overline{v_x^2}}{L}$. By symmetry $\overline{v_x^2} = \tfrac13\overline{c^2}$, so the pressure is

$$ P = \frac{F}{L^2} = \frac13\frac{Nm\,\overline{c^2}}{V} = \frac13\rho\,\overline{c^2} $$

**Consequences.**

1. Comparing with $PV = nRT$ ($PV = NkT$): $\tfrac13Nm\overline{c^2} = NkT$.
2. **Mean kinetic energy per molecule** $= \tfrac12m\overline{c^2} = \tfrac32kT$, which depends only on temperature. Temperature is a measure of the average translational kinetic energy.
3. **rms speed** $c_{rms} = \sqrt{\dfrac{3kT}{m}} = \sqrt{\dfrac{3RT}{M}} = \sqrt{\dfrac{3P}{\rho}}$.
4. **Law of equipartition.** Each degree of freedom has energy $\tfrac12kT$ per molecule. A gas with $f$ degrees of freedom has $U = \tfrac f2nRT$.
5. Boyle's, Charles', Avogadro's and Dalton's laws all follow from $P = \tfrac13\rho\overline{c^2}$.

| Gas | $M\ (\text{g mol}^{-1})$ | $c_{rms}$ at $300\ \text{K}$ |
|---|---|---|
| Hydrogen | 2 | $1934\ \text{m s}^{-1}$ |
| Oxygen | 32 | $484\ \text{m s}^{-1}$ |

**Numerical.** For oxygen, $c_{rms} = \sqrt{3(8.314)(300)/0.032} = 484\ \text{m s}^{-1}$. Hydrogen at the same temperature is four times faster. The mean kinetic energy per molecule is $\tfrac32(1.38\times10^{-23})(300) = 6.2\times10^{-21}\ \text{J}$ for both gases.

**Conclusion.** $P = \tfrac13\rho\overline{c^2}$, and absolute temperature is proportional to the mean kinetic energy of the molecules.

### Model answer D2: laws of thermodynamics and the Carnot engine (10 marks)

**Introduction.** Thermodynamics studies how heat is converted to work. The **zeroth law** says that two bodies in thermal equilibrium with a third are in equilibrium with each other, which defines temperature.

**First law.** Heat supplied equals the increase in internal energy plus the work done by the system: $Q = \Delta U + W$. It is the law of conservation of energy.

**Processes.**

| Process | Condition | Result |
|---|---|---|
| Isothermal | $T$ constant, $\Delta U = 0$ | $Q = W = nRT\ln\dfrac{V_2}{V_1}$, $PV$ constant |
| Isobaric | $P$ constant | $W = P\Delta V$ |
| Isochoric | $V$ constant | $W = 0$, $Q = \Delta U = nC_v\Delta T$ |
| Adiabatic | $Q = 0$ | $PV^{\gamma}$ constant, $W = \dfrac{nR(T_1 - T_2)}{\gamma - 1}$ |

Also $C_p - C_v = R$ and $\gamma = C_p/C_v$ ($1.67$ for monatomic and $1.4$ for diatomic gases).

**Second law.** *Kelvin-Planck:* no engine can convert all the heat taken from a single source into work. *Clausius:* heat cannot flow from a cold body to a hot body without external work. So efficiency is always below 100%.

**Carnot engine.** It works between a source at $T_1$ and a sink at $T_2$ in four reversible steps: isothermal expansion, adiabatic expansion, isothermal compression and adiabatic compression. Its efficiency is $\eta = 1 - \dfrac{T_2}{T_1}$, the maximum possible. A refrigerator has the coefficient of performance $\dfrac{T_2}{T_1 - T_2}$.

**Numerical.** A Carnot engine works between $500\ \text{K}$ and $300\ \text{K}$ and takes $1000\ \text{J}$ from the source. Then $\eta = 1 - 300/500 = 40\%$, the work is $400\ \text{J}$ and the heat rejected is $600\ \text{J}$. For one mole of an ideal gas doubling its volume isothermally at $300\ \text{K}$, $W = 8.314\times300\times\ln2 = 1729\ \text{J}$ and $\Delta U = 0$.

**Conclusion.** The first law is about the energy balance and the second law about its direction. Carnot's efficiency $1 - T_2/T_1$ is the upper limit for any engine.
