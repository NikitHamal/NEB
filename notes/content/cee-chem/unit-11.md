---
subject: Chemistry
grade: CEE
unit: 11
title: Chemical Thermodynamics
hours: 1
area: Physical Chemistry
---

Thermodynamics answers a different question from kinetics: not *how fast*, but *will it
happen at all, and how much heat is involved*. The paper carries about **one question**
from this chapter (our estimate from the MEC topic list). It is usually a Hess's-law
addition, a $\Delta G = \Delta H - T\Delta S$ sign decision, or a definition question
about the enthalpy of formation, combustion or neutralisation. The marks are lost on
three things: a sign convention applied inconsistently, a non-zero enthalpy of formation
for an element, and the belief that "spontaneous" means "fast".

::: key What the paper asks from this chapter
- System and surroundings; open, closed and isolated systems; state functions ($U$, $H$, $S$, $G$) against path functions ($q$, $w$); intensive against extensive.
- First law in the IUPAC convention: $\Delta U = q + w$, with $q$ positive when heat enters the system and $w$ positive when work is done **on** it; $w = -P\Delta V$.
- $H = U + PV$; $\Delta H = q_p$ and $\Delta U = q_v$; $\Delta H = \Delta U + \Delta n_g RT$.
- $\Delta H_f^\circ$ of an element in its **standard state is zero**; $\Delta H^\circ_{\text{rxn}} = \sum \Delta H_f^\circ(\text{products}) - \sum \Delta H_f^\circ(\text{reactants})$.
- Laplace's law: $\Delta H$ reverses sign when a reaction is reversed. Hess's law: $\Delta H$ is independent of the path, so equations may be added and subtracted.
- Second law: $\Delta S_{\text{universe}} > 0$ for a spontaneous change. Entropy rises from solid to liquid to gas.
- $\Delta G = \Delta H - T\Delta S$; $\Delta G < 0$ spontaneous, $= 0$ equilibrium, $> 0$ non-spontaneous. The four sign cases decide the temperature behaviour.
- $\Delta G^\circ = -RT \ln K$; negative $\Delta G^\circ$ means $K > 1$.
:::

## 11.1 Systems and surroundings; state functions; internal energy; intensive and extensive properties; the first law and enthalpy

### System, surroundings and the three types of system

::: definition System and surroundings
The **system** is the part of the universe under study; the **surroundings** are
everything else; the **boundary** separates them and may be real (a beaker wall) or
imaginary.
:::

| Type | Exchanges matter? | Exchanges energy? | Example |
|---|---|---|---|
| **Open** | yes | yes | water boiling in an open pan; a living cell |
| **Closed** | no | yes | a sealed flask being heated; a piston-cylinder with no leak |
| **Isolated** | no | no | a thermos flask; a bomb calorimeter (approximately) |

An isolated system is the only one for which $\Delta U = 0$ always, because neither heat
nor work can cross the boundary.

### State functions and path functions

::: definition State function
A **state function** is a property whose value depends only on the present state of the
system — its pressure, volume, temperature and composition — and **not** on how that
state was reached. Its change between two states is $\Delta X = X_{\text{final}} - X_{\text{initial}}$
and is the same for every route.
:::

| State functions | Path functions |
|---|---|
| internal energy $U$, enthalpy $H$, entropy $S$, free energy $G$ | heat $q$, work $w$ |
| pressure $P$, volume $V$, temperature $T$, amount $n$ | — |
| A change depends only on the end points | A value depends on the route taken |

Because $U$ is a state function, $\Delta U$ for a change from A to B is fixed. But $q$
and $w$ are not: one route may exchange a lot of heat and little work, another the
reverse. Only their **sum** is fixed, which is exactly what the first law says.

```figure caption="Two routes from A to B on a $P$–$V$ diagram. The area under each path is the work done, so the work — and therefore the heat — differs between the routes, although $\Delta U$ is the same for both."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.7, 2.9))
V = np.linspace(2, 4, 200)
ax.plot(V, 8/V, color=ACCENT, lw=2.0, label='path 1: smooth expansion')
ax.plot([2, 2, 4], [4, 2, 2], color=SERIES[1], lw=2.0, ls='--', label='path 2: cool, then expand')
ax.fill_between([2, 2, 4], [0, 2, 2], [0, 2, 2], color=SERIES[1], alpha=0.0)
ax.plot([2], [4], 'o', color=INK, ms=5, zorder=5)
ax.plot([4], [2], 'o', color=INK, ms=5, zorder=5)
ax.text(1.86, 4.12, 'A', fontsize=9.5, color=INK)
ax.text(4.06, 2.02, 'B', fontsize=9.5, color=INK)
ax.set_xlabel('volume (L)'); ax.set_ylabel('pressure (atm)')
ax.set_xlim(1.5, 4.8); ax.set_ylim(0, 4.9)
ax.spines[['top', 'right']].set_visible(False)
ax.grid(True, alpha=0.45)
ax.legend(loc='upper right', fontsize=8.0)
```

### Intensive and extensive properties

::: definition Intensive and extensive
An **extensive** property depends on the amount of substance present — mass, volume,
internal energy, enthalpy, entropy, free energy. An **intensive** property does not —
temperature, pressure, density, molar volume, concentration, molar enthalpy, $E^\circ$.
:::

Doubling the amount doubles every extensive property but leaves every intensive one
unchanged. This is the same idea that makes $E^\circ$ of an electrode independent of how
the half-reaction is written (Unit 10), and it is why $\Delta H$ is quoted **per mole**.

| Extensive | Intensive |
|---|---|
| mass, volume, $n$ | density, molar volume |
| $U$, $H$, $S$, $G$, $C$ (heat capacity) | $T$, $P$, molar heat capacity |
| $\Delta H$ of a stated amount | $\Delta H_f^\circ$ per mole |

### Internal energy and the first law

The **internal energy** $U$ is the total energy of the system — kinetic energy of its
molecules plus the potential energy of their interactions. Its absolute value cannot be
measured; only $\Delta U$ can.

::: definition The first law of thermodynamics
Energy can be converted from one form to another but can neither be created nor
destroyed. For a closed system:
$$ \Delta U = q + w $$
where $q$ is the heat supplied **to** the system and $w$ the work done **on** the system.
Both are positive when energy enters the system. This is the IUPAC convention and it is
the one used throughout this book.
:::

For expansion against a constant external pressure, the work done **on** the system is

$$ w = -P_{\text{ext}}\Delta V $$

so an expanding gas ($\Delta V > 0$) has $w < 0$: it loses energy by doing work. A
compressed gas has $w > 0$.

| Change | $\Delta V$ | $w$ | Meaning |
|---|---|---|---|
| Gas expands | positive | negative | system does work on the surroundings |
| Gas compressed | negative | positive | surroundings do work on the system |
| $\Delta V = 0$ | zero | 0 | no pressure–volume work |

::: caution Two conventions — read the stem
Some older textbooks write $\Delta U = q - w$ and count work done **by** the system as
positive. The physics is identical; only the book-keeping differs. If a question names
the convention, follow it. If it does not, use IUPAC ($\Delta U = q + w$) and remember
that an expanding gas has **negative** work. Never mix the two within one calculation —
that is where the "sign error" distractors come from.
:::

::: example First law with both signs
**Problem.** A gas absorbs 500 J of heat and does 200 J of work on the surroundings. Find
$\Delta U$. Then find $\Delta U$ if the same gas absorbs 500 J and has 200 J of work done
on it.

**Solution.** IUPAC: $q = +500$ J. Work done **by** the system is negative: $w = -200$ J.
$\Delta U = 500 + (-200) = \mathbf{+300}$ J — the gas warms.
Second case: $w = +200$ J, so $\Delta U = 500 + 200 = \mathbf{+700}$ J.
:::

::: example Work of expansion in joules
**Problem.** A gas expands from 2.0 L to 4.0 L against a constant pressure of 1.0 atm.
Find the work done on the system in joules (1 L atm = 101.3 J).

**Solution.** $\Delta V = +2.0$ L.
$w = -P\Delta V = -(1.0)(2.0) = -2.0$ L atm
$= -2.0 \times 101.3 = \mathbf{-203}$ J.
The negative sign says the system lost energy as work; the surroundings gained it.
:::

### Enthalpy

Most reactions in a laboratory are carried out in open vessels, at constant **pressure**,
not constant volume. The heat exchanged then is not $\Delta U$, because the system also
does work pushing back the atmosphere. Thermodynamics therefore defines a new state
function:

$$ H = U + PV $$

::: definition Enthalpy
**Enthalpy** $H$ is the heat content of a system at constant pressure, defined as
$H = U + PV$. At constant pressure the heat exchanged equals the change in enthalpy,
$q_p = \Delta H$; at constant volume, $q_v = \Delta U$.
:::

For a change at constant pressure, $\Delta H = \Delta U + P\Delta V$. For reactions
involving gases, $P\Delta V = \Delta n_g RT$, where $\Delta n_g$ is the change in the
number of moles of **gas**:

$$ \Delta H = \Delta U + \Delta n_g RT $$

- If $\Delta n_g = 0$, $\Delta H = \Delta U$ (e.g. H₂ + I₂ → 2HI).
- If $\Delta n_g < 0$ (gas consumed), $\Delta H < \Delta U$ — the reaction is more
  exothermic at constant pressure.
- If $\Delta n_g > 0$ (gas produced), $\Delta H > \Delta U$.

| Sign | $\Delta H$ | Heat | Example |
|---|---|---|---|
| Exothermic | negative | released to the surroundings | combustion, neutralisation, condensation |
| Endothermic | positive | absorbed from the surroundings | melting, boiling, decomposition of CaCO₃ |

::: example Converting ΔU to ΔH
**Problem.** For N₂(g) + 3H₂(g) → 2NH₃(g), $\Delta U = -87.4$ kJ mol⁻¹ at 298 K. Find
$\Delta H$ ($R = 8.314$ J mol⁻¹ K⁻¹).

**Solution.** $\Delta n_g = 2 - (1 + 3) = -2$.
$\Delta n_g RT = (-2)(8.314)(298) = -4955$ J = $-4.96$ kJ.
$\Delta H = -87.4 + (-4.96) = \mathbf{-92.4}$ kJ mol⁻¹.
The reaction releases slightly more heat at constant pressure, because the surroundings
do work on the system as four moles of gas collapse into two.
:::

## 11.2 Enthalpies of reaction, formation, combustion, neutralisation, solution, fusion and vaporisation; Laplace's and Hess's laws

### Enthalpy of reaction

The **enthalpy of reaction** $\Delta H_r$ is the heat change when the reaction takes place
as written, with the coefficients interpreted as moles. It is found from formation
enthalpies:

$$ \Delta H^\circ_{\text{rxn}} = \sum \Delta H_f^\circ(\text{products}) - \sum \Delta H_f^\circ(\text{reactants}) $$

The logic: every compound is imagined broken into its elements (cost = $-\Delta H_f^\circ$),
and the elements are reassembled into the products (gain = $+\Delta H_f^\circ$).

### Enthalpy of formation

::: definition Standard enthalpy of formation
The **standard enthalpy of formation** $\Delta H_f^\circ$ is the enthalpy change when **one
mole** of a compound is formed from its elements in their **standard states** at 298 K and
1 bar. By definition it is **zero for an element in its standard state**.
:::

| Substance | $\Delta H_f^\circ$ (kJ mol⁻¹) | Note |
|---|---|---|
| C(graphite), O₂(g), H₂(g), N₂(g), Br₂(l), I₂(s), Na(s) | 0 | standard states |
| C(diamond) | +1.9 | not the standard state of carbon |
| O₃(g) | +142 | not the standard state of oxygen |
| CH₄(g) | −74.8 | |
| CO(g) | −110.5 | |
| CO₂(g) | −393.5 | |
| H₂O(l) | −285.8 | |
| H₂O(g) | −241.8 | the difference is the enthalpy of vaporisation |
| NH₃(g) | −46.1 | |
| C₂H₅OH(l) | −277.7 | |

::: caution Zero, but only for the standard state
$\Delta H_f^\circ$ is zero for graphite, not diamond; for O₂ gas, not ozone; for rhombic
sulphur, not monoclinic; for white phosphorus is **not** zero (red phosphorus is the
standard state). An option that says "the enthalpy of formation of every element is zero"
is wrong — it is zero only in the **most stable form at 298 K and 1 bar**.
:::

### The other enthalpies, one by one

| Enthalpy | Definition (all per mole) | Sign and typical value |
|---|---|---|
| **Combustion** $\Delta H_c^\circ$ | one mole of substance burnt completely in excess O₂ | always negative for fuels; CH₄ −890.3 kJ mol⁻¹ |
| **Neutralisation** $\Delta H_n^\circ$ | one mole of H⁺ from an acid neutralised by OH⁻ from a base | −57.1 kJ mol⁻¹ for strong acid + strong base |
| **Solution** $\Delta H_{\text{sol}}^\circ$ | one mole of substance dissolved in enough solvent that further dilution gives no heat change | NaOH −44.5; NH₄NO₃ +25.7 (endothermic, the cold pack) |
| **Fusion** $\Delta H_{\text{fus}}^\circ$ | one mole of solid melted at its melting point | always positive; ice +6.01 kJ mol⁻¹ |
| **Vaporisation** $\Delta H_{\text{vap}}^\circ$ | one mole of liquid boiled at its boiling point | always positive; water +40.7 kJ mol⁻¹ |
| **Sublimation** $\Delta H_{\text{sub}}^\circ$ | one mole of solid converted directly to vapour | positive; equals $\Delta H_{\text{fus}} + \Delta H_{\text{vap}}$ |

**Why neutralisation is always about −57 kJ.** A strong acid and a strong base are fully
ionised, so whatever the acid and base, the reaction is the same:

$$ H^+(aq) + OH^-(aq) \rightarrow H_2O(l) \qquad \Delta H = -57.1\ \text{kJ mol}^{-1} $$

A **weak** acid or base gives a smaller (less negative) value, because some of the energy
released is used up in ionising the weak electrolyte. This is a favourite distractor: the
value is −57.1 for strong–strong only.

**Enthalpy of solution** is the sum of two terms: the **lattice enthalpy** (energy needed
to break the crystal apart, endothermic) and the **hydration enthalpy** (energy released
when the ions are surrounded by water, exothermic). When hydration wins, dissolution is
exothermic (NaOH); when the lattice wins, it is endothermic (NH₄NO₃, KNO₃).

```figure caption="The enthalpy ladder for one substance. Melting and boiling are both endothermic; sublimation is the sum of the two steps, which is why $\Delta H_{\text{sub}} = \Delta H_{\text{fus}} + \Delta H_{\text{vap}}$. The vertical scale is schematic."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8, 3.0))
ax.set_xlim(0, 10); ax.set_ylim(-1.2, 7.6); ax.axis('off')
for y0, txt in [(0.2, 'solid'), (2.1, 'liquid'), (5.6, 'gas')]:
    ax.plot([1.0, 8.4], [y0, y0], color=INK, lw=1.8)
    ax.text(1.1, y0 + 0.26, txt, fontsize=9, color=INK, va='bottom')
ax.annotate('', xy=(2.6, 2.1), xytext=(2.6, 0.2),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.4))
ax.text(2.85, 1.15, 'ΔH_fus = +6.01', fontsize=8.4, color=ACCENT, va='center')
ax.annotate('', xy=(4.2, 5.6), xytext=(4.2, 2.1),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.4))
ax.text(4.45, 3.85, 'ΔH_vap = +40.7', fontsize=8.4, color=SERIES[1], va='center')
ax.annotate('', xy=(7.3, 5.6), xytext=(7.3, 0.2),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[2], lw=1.4))
ax.text(7.05, 2.9, 'ΔH_sub\n= +46.7', fontsize=8.4, color=SERIES[2], va='center', ha='right')
ax.text(0.2, 7.1, 'all values in kJ mol⁻¹', fontsize=8.0, color=MUTED)
```

### Laplace's law

::: definition Laplace's law
The enthalpy change of a reaction is equal in magnitude and **opposite in sign** to that
of the reverse reaction: $\Delta H_{\text{forward}} = -\Delta H_{\text{backward}}$.
:::

So if the formation of water releases 285.8 kJ per mole, the decomposition of one mole of
liquid water into its elements absorbs exactly 285.8 kJ. Nothing is lost in the round
trip, because enthalpy is a state function.

### Hess's law

::: definition Hess's law of constant heat summation
The total enthalpy change of a chemical reaction is the same whether the reaction takes
place in **one step or in several steps**, provided the initial and final states are the
same. $\Delta H$ is independent of the path.
:::

Hess's law is not a new law: it follows directly from the first law, because $H$ is a state
function and $\Delta H$ depends only on the end points.

**The three operations** that solve every Hess problem:

1. **Add** two equations and their $\Delta H$ values add.
2. **Reverse** an equation and the sign of $\Delta H$ flips (Laplace's law).
3. **Multiply** an equation by a number and $\Delta H$ is multiplied by the same number.

```figure caption="Hess's law for the formation of carbon monoxide. The direct route from the elements to CO₂ releases 393.5 kJ; the two-step route releases 110.5 + 283.0 kJ. Because enthalpy is a state function the two totals must agree, which is how the otherwise unmeasurable formation of CO is found."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9, 3.1))
ax.set_xlim(0, 11); ax.set_ylim(-470, 90); ax.axis('off')
ax.plot([2.2, 8.8], [0, 0], color=INK, lw=1.8)
ax.plot([2.2, 6.6], [-110.5, -110.5], color=INK, lw=1.8)
ax.plot([2.2, 8.8], [-393.5, -393.5], color=INK, lw=1.8)
ax.text(5.5, 22, 'C(s) + O₂(g)', fontsize=8.8, color=INK, ha='center')
ax.text(4.9, -172, 'CO(g) + ½O₂(g)', fontsize=8.8, color=INK, ha='center')
ax.text(5.5, -371, 'CO₂(g)', fontsize=8.8, color=INK, ha='center')
ax.annotate('', xy=(3.0, -110.5), xytext=(3.0, 0),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.4))
ax.text(3.15, -52, '−110.5', fontsize=8.2, color=ACCENT, va='center')
ax.annotate('', xy=(3.0, -393.5), xytext=(3.0, -110.5),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.4))
ax.text(3.15, -250, '−283.0', fontsize=8.2, color=ACCENT, va='center')
ax.annotate('', xy=(7.7, -393.5), xytext=(7.7, 0),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.4))
ax.text(7.9, -200, '−393.5\ndirect', fontsize=8.2, color=SERIES[1], va='center')
ax.text(0.2, -440, 'enthalpy / kJ mol⁻¹', fontsize=8.0, color=MUTED)
```

::: example Hess's law in three equations
**Problem.** Find $\Delta H$ for C(s) + ½O₂(g) → CO(g), given
(i) C(s) + O₂(g) → CO₂(g), $\Delta H = -393.5$ kJ
(ii) CO(g) + ½O₂(g) → CO₂(g), $\Delta H = -283.0$ kJ.

**Solution.** The target has CO on the right and only ½O₂ used, so take (i) **minus** (ii):
(i) gives CO₂ on the right; (ii) reversed puts CO₂ on the left and CO on the right with
$\Delta H = +283.0$ kJ. Adding:

C(s) + O₂(g) + CO₂(g) → CO₂(g) + CO(g) + ½O₂(g)

Cancel CO₂ and ½O₂ from both sides:
C(s) + ½O₂(g) → CO(g)
$\Delta H = -393.5 + 283.0 = \mathbf{-110.5}$ kJ mol⁻¹.
:::

::: example Hess's law from formation enthalpies
**Problem.** Find $\Delta H^\circ$ for CH₄(g) + 2O₂(g) → CO₂(g) + 2H₂O(l), using
$\Delta H_f^\circ$: CH₄ −74.8, CO₂ −393.5, H₂O(l) −285.8 kJ mol⁻¹.

**Solution.**
$\Delta H^\circ = [(-393.5) + 2(-285.8)] - [(-74.8) + 2(0)]$
$= (-393.5 - 571.6) + 74.8 = -965.1 + 74.8 = \mathbf{-890.3}$ kJ mol⁻¹.
The two zeros are the O₂, an element in its standard state. Forgetting them, or forgetting
the coefficient 2 on water, are the two classic errors.
:::

::: example Hess's law round a three-equation cycle
**Problem.** Find $\Delta H_f^\circ$ of ethyne, 2C(s) + H₂(g) → C₂H₂(g), from
(i) C₂H₂(g) + 5/2O₂(g) → 2CO₂(g) + H₂O(l), $\Delta H = -1299.5$ kJ
(ii) C(s) + O₂(g) → CO₂(g), $\Delta H = -393.5$ kJ
(iii) H₂(g) + ½O₂(g) → H₂O(l), $\Delta H = -285.8$ kJ.

**Solution.** The target has C₂H₂ on the **right**, so (i) must be **reversed**
($\Delta H = +1299.5$). It also needs 2C on the left, so (ii) is **doubled**
($\Delta H = -787.0$). Hydrogen appears once, so (iii) is used as it stands.

Adding the three adjusted equations:

2C(s) + 2O₂(g) + H₂(g) + ½O₂(g) + 2CO₂(g) + H₂O(l) → 2CO₂(g) + H₂O(l) + C₂H₂(g) + 5/2O₂(g)

Cancel 2CO₂, H₂O(l) and 5/2O₂ from both sides (2 + ½ = 5/2 on the left):

2C(s) + H₂(g) → C₂H₂(g)

$\Delta H = (+1299.5) + (-787.0) + (-285.8) = \mathbf{+226.7}$ kJ mol⁻¹.

The positive sign is the point: ethyne is **endothermic** with respect to its elements,
which is why it is unstable, burns with a very hot flame and can decompose explosively.
A negative answer here would mean an arithmetic slip in the reversal.
:::

::: tip Hess problems in an MCQ
Do not balance anything you are not asked to balance. Look at where the target substance
appears, decide "same side or opposite side", and add or subtract. If the target has a
coefficient of 2, double the whole equation **and** its $\Delta H$. Then check the sign
with common sense: forming CO from elements must release heat, so the answer is negative.
:::

## 11.3 Spontaneity, entropy and the second law; Gibbs free energy and its relation to the equilibrium constant

### Spontaneity

A **spontaneous** process is one that has a natural tendency to occur once started, without
outside help: a ball rolling downhill, iron rusting, gas expanding into a vacuum, ice
melting above 0 °C. Spontaneous does **not** mean fast — the conversion of diamond to
graphite is spontaneous and takes longer than the age of the Earth.

Two driving forces decide spontaneity: the tendency to reach **lower energy** (exothermic,
$\Delta H < 0$) and the tendency to reach **greater disorder** (entropy increase,
$\Delta S > 0$). Neither alone is sufficient.

### Entropy and the second law

::: definition Entropy
**Entropy** $S$ is a measure of the disorder or randomness of a system — the number of
ways its energy and particles can be arranged. Its unit is **J K⁻¹ mol⁻¹**. For a
reversible change at constant temperature, $\Delta S = q_{\text{rev}}/T$.
:::

| Change | $\Delta S$ | Reason |
|---|---|---|
| Solid → liquid → gas | positive | particles become freer |
| Gas produced in a reaction | positive | moles of gas increase |
| Gas consumed | negative | moles of gas decrease |
| Mixing two gases | positive | more arrangements |
| Cooling a substance | negative | less thermal disorder |

The **third law** fixes the zero: the entropy of a perfectly ordered crystal at 0 K is
zero. That is why absolute entropies can be tabulated, while only changes in $U$ and $H$
can be measured.

::: definition The second law of thermodynamics
For any spontaneous change, the total entropy of the universe increases:
$$ \Delta S_{\text{universe}} = \Delta S_{\text{system}} + \Delta S_{\text{surroundings}} > 0 $$
For a reversible change it is zero; a negative total is impossible.
:::

The entropy of the system alone may fall — freezing water is spontaneous below 0 °C even
though $\Delta S_{\text{system}} < 0$ — because the heat released raises the entropy of
the surroundings by more:

$$ \Delta S_{\text{surroundings}} = -\frac{\Delta H}{T} $$

So a reaction is spontaneous when $\Delta S_{\text{system}} - \Delta H/T > 0$, which
multiplied by $-T$ gives the Gibbs criterion below.

### Gibbs free energy

::: definition Gibbs free energy
$G = H - TS$. At constant temperature and pressure the change is
$$ \Delta G = \Delta H - T\Delta S $$
A process is **spontaneous** when $\Delta G < 0$, at **equilibrium** when $\Delta G = 0$,
and **non-spontaneous** when $\Delta G > 0$.
:::

$\Delta G$ combines the two driving forces into one number: $\Delta H$ is the heat term and
$-T\Delta S$ the disorder term, weighted by the temperature.

| $\Delta H$ | $\Delta S$ | $\Delta G = \Delta H - T\Delta S$ | Spontaneous? | Example |
|---|---|---|---|---|
| − | + | always negative | at **all** temperatures | combustion of a fuel |
| − | − | negative at low $T$, positive at high $T$ | at **low** $T$ | freezing of water below 0 °C |
| + | + | positive at low $T$, negative at high $T$ | at **high** $T$ | melting of ice; CaCO₃ decomposition |
| + | − | always positive | **never** | 3O₂ → 2O₃ under ordinary conditions |

The switch-over temperature, where $\Delta G = 0$, is

$$ T = \frac{\Delta H}{\Delta S} $$

```figure caption="$\Delta G$ against temperature for the four sign combinations. A positive $\Delta H$ with a positive $\Delta S$ starts non-spontaneous and becomes spontaneous above $\Delta H/\Delta S$; the opposite pair does the reverse. The dots mark the switch-over temperatures, 333 K and 500 K."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9, 3.0))
T = np.linspace(0, 600, 200)
cases = [(-50, 0.06, SERIES[0], 'ΔH<0, ΔS>0'),
         (-50, -0.15, SERIES[1], 'ΔH<0, ΔS<0'),
         (50, 0.10, SERIES[2], 'ΔH>0, ΔS>0'),
         (50, -0.10, SERIES[3], 'ΔH>0, ΔS<0')]
offsets = [-11, 10, -14, 10]
for (dh, ds, col, lab), dy in zip(cases, offsets):
    g = dh - T*ds
    ax.plot(T, g, color=col, lw=1.9)
    ax.text(562, dh - 562*ds + dy, lab, fontsize=7.8, color=col, ha='right')
ax.axhline(0, color=INK, lw=0.9)
ax.plot([333, 500], [0, 0], 'o', color=INK, ms=4, zorder=5)
ax.set_xlabel('temperature (K)'); ax.set_ylabel('ΔG (kJ mol⁻¹)')
ax.set_xlim(0, 600); ax.set_ylim(-110, 130)
ax.spines[['top', 'right']].set_visible(False)
ax.grid(True, alpha=0.45)
```

::: caution ΔG < 0 means spontaneous, not fast
A negative $\Delta G$ says the reaction **can** go, not that it **will go quickly**.
Diamond → graphite has $\Delta G < 0$ and does not happen measurably; the conversion of
sugar to CO₂ and water has $\Delta G < 0$ and needs a flame or an enzyme. Kinetics
(Unit 9) decides the speed, thermodynamics the direction. An option that equates
"spontaneous" with "fast" or with "exothermic" is the commonest wrong key in this chapter.
:::

::: example Finding the temperature at which a reaction turns
**Problem.** For a reaction $\Delta H = +50$ kJ mol⁻¹ and $\Delta S = +100$ J K⁻¹ mol⁻¹.
At what temperature does it become spontaneous?

**Solution.** Spontaneous needs $\Delta G < 0$, so $T\Delta S > \Delta H$:
$T > \frac{50\,000}{100} = \mathbf{500}$ K (227 °C).
Above 500 K the disorder term outweighs the heat term. Below it, the reaction is
non-spontaneous.
:::

### Free energy and the equilibrium constant

At equilibrium $\Delta G = 0$ and the reaction quotient equals $K$. Combining this with
$\Delta G = \Delta G^\circ + RT\ln Q$ gives the bridge between thermodynamics and
equilibrium:

$$ \Delta G^\circ = -RT\ln K = -2.303RT\log K $$

| $\Delta G^\circ$ | $K$ | Meaning |
|---|---|---|
| negative | $K > 1$ | products favoured at equilibrium |
| zero | $K = 1$ | reactants and products comparable |
| positive | $K < 1$ | reactants favoured at equilibrium |

Note that $K$ depends only on temperature, so $\Delta G^\circ$ must be quoted at a stated
temperature. A catalyst changes neither.

::: example Equilibrium constant from ΔG°
**Problem.** A reaction has $\Delta G^\circ = -20$ kJ mol⁻¹ at 298 K. Find $K$
($R = 8.314$ J mol⁻¹ K⁻¹).

**Solution.** $\ln K = -\frac{\Delta G^\circ}{RT} = \frac{20\,000}{(8.314)(298)} = 8.07$.
$K = e^{8.07} \approx \mathbf{3.2 \times 10^3}$.
A large $K$, as expected from a strongly negative $\Delta G^\circ$: every 5.7 kJ mol⁻¹ of
$\Delta G^\circ$ changes $K$ by a factor of ten at room temperature.
:::

::: example ΔG at a temperature other than 298 K
**Problem.** For N₂(g) + 3H₂(g) → 2NH₃(g), $\Delta H^\circ = -92.4$ kJ mol⁻¹ and
$\Delta S^\circ = -198$ J K⁻¹ mol⁻¹. Find $\Delta G^\circ$ at 298 K and at 700 K.

**Solution.** At 298 K:
$\Delta G^\circ = -92.4 - (298)(-0.198) = -92.4 + 59.0 = \mathbf{-33.4}$ kJ mol⁻¹
(spontaneous).
At 700 K:
$\Delta G^\circ = -92.4 - (700)(-0.198) = -92.4 + 138.6 = \mathbf{+46.2}$ kJ mol⁻¹
(non-spontaneous at standard pressure).
This is exactly why the Haber process is run at about 700 K only with a pressure of
200 atm: the high pressure makes $Q$ small, so the actual $\Delta G$ stays negative even
though $\Delta G^\circ$ has changed sign. Temperature helps the rate and hurts the yield;
pressure rescues the yield.
:::

## Formula and fact sheet

| Quantity | Relation | Note |
|---|---|---|
| First law (IUPAC) | $\Delta U = q + w$ | $q$ in, $w$ on the system: both positive |
| Pressure–volume work | $w = -P_{\text{ext}}\Delta V$ | expansion gives $w < 0$ |
| Enthalpy | $H = U + PV$ | $\Delta H = q_p$, $\Delta U = q_v$ |
| Enthalpy from internal energy | $\Delta H = \Delta U + \Delta n_g RT$ | $\Delta n_g$ counts gas moles only |
| Reaction enthalpy | $\Delta H^\circ_{\text{rxn}} = \sum \Delta H_f^\circ(\text{products}) - \sum \Delta H_f^\circ(\text{reactants})$ | elements in standard state = 0 |
| Laplace's law | $\Delta H_{\text{forward}} = -\Delta H_{\text{backward}}$ | reversing flips the sign |
| Hess's law | $\Delta H$ is independent of the path | add, reverse, multiply |
| Entropy change | $\Delta S = q_{\text{rev}}/T$ | J K⁻¹ mol⁻¹ |
| Entropy of surroundings | $\Delta S_{\text{surr}} = -\Delta H/T$ | at constant $T$, $P$ |
| Second law | $\Delta S_{\text{universe}} > 0$ | spontaneous |
| Gibbs free energy | $\Delta G = \Delta H - T\Delta S$ | $<0$ spontaneous, $0$ equilibrium |
| Switch-over temperature | $T = \Delta H/\Delta S$ | where $\Delta G = 0$ |
| Free energy and $K$ | $\Delta G^\circ = -RT\ln K$ | negative $\Delta G^\circ$ → $K > 1$ |
| Sublimation | $\Delta H_{\text{sub}} = \Delta H_{\text{fus}} + \Delta H_{\text{vap}}$ | |

Numbers to carry in: $\Delta H_f^\circ$ — CH₄ −74.8, CO −110.5, CO₂ −393.5, H₂O(l) −285.8,
H₂O(g) −241.8, NH₃ −46.1 kJ mol⁻¹. $\Delta H_{\text{fus}}$ ice +6.01;
$\Delta H_{\text{vap}}$ water +40.7; $\Delta H_{\text{neut}}$ (strong–strong) −57.1;
$\Delta H_c$ methane −890.3 kJ mol⁻¹. $\Delta S^\circ$ — H₂ 130.7, O₂ 205.1, N₂ 191.6,
NH₃ 192.5, H₂O(g) 188.7, H₂O(l) 69.9 J K⁻¹ mol⁻¹. 1 L atm = 101.3 J.

| Sign of $\Delta H$ | Sign of $\Delta S$ | Spontaneous |
|---|---|---|
| − | + | at all temperatures |
| − | − | at low temperature |
| + | + | at high temperature |
| + | − | never |

## Chapter summary

- A system is open, closed or isolated; only an isolated system has $\Delta U = 0$ always. $U$, $H$, $S$ and $G$ are state functions; $q$ and $w$ are path functions whose sum alone is fixed.
- Extensive properties scale with amount (mass, $U$, $H$, $S$, $G$); intensive ones do not ($T$, $P$, density, molar enthalpy).
- First law (IUPAC): $\Delta U = q + w$, with $q$ positive into the system and $w = -P\Delta V$ positive when work is done on it. An expanding gas has negative work.
- $H = U + PV$; $\Delta H = q_p$ at constant pressure and $\Delta U = q_v$ at constant volume; $\Delta H = \Delta U + \Delta n_g RT$.
- $\Delta H_f^\circ$ is zero only for an element in its standard state; $\Delta H^\circ_{\text{rxn}}$ is products minus reactants.
- Combustion is always exothermic; neutralisation of a strong acid by a strong base is −57.1 kJ mol⁻¹; fusion and vaporisation are always endothermic, and $\Delta H_{\text{sub}} = \Delta H_{\text{fus}} + \Delta H_{\text{vap}}$.
- Laplace's law: reversing a reaction reverses the sign of $\Delta H$. Hess's law: $\Delta H$ is path-independent, so equations can be added, reversed and multiplied.
- Second law: $\Delta S_{\text{universe}} > 0$ for a spontaneous change; $\Delta S_{\text{surr}} = -\Delta H/T$, so an exothermic reaction can be spontaneous even when its own entropy falls.
- $\Delta G = \Delta H - T\Delta S$: negative spontaneous, zero equilibrium, positive non-spontaneous; $T = \Delta H/\Delta S$ is the switch-over temperature; spontaneous never means fast.
- $\Delta G^\circ = -RT\ln K$: a negative $\Delta G^\circ$ gives $K > 1$; $K$ depends only on temperature.

## Practice questions

**Set A — Recall (25 questions)**

1. A system that exchanges both matter and energy with its surroundings is
   (a) closed (b) isolated (c) open (d) adiabatic
2. Which of the following is a state function?
   (a) work (b) enthalpy (c) heat (d) heat and work together
3. Which property is intensive?
   (a) mass (b) volume (c) internal energy (d) temperature
4. The first law of thermodynamics is a statement of the conservation of
   (a) energy (b) mass (c) momentum (d) charge
5. According to the IUPAC sign convention, the first law is written
   (a) $\Delta U = q - w$ (b) $\Delta U = q + w$ (c) $\Delta U = w - q$ (d) $\Delta U = qw$
6. A reaction with a negative $\Delta H$ is
   (a) endothermic (b) isothermal (c) adiabatic (d) exothermic
7. The enthalpy of formation of an element in its standard state is
   (a) always negative (b) always positive (c) zero (d) equal to its atomic mass
8. Hess's law follows directly from
   (a) the first law of thermodynamics (b) the second law (c) the third law (d) Le Chatelier's principle
9. Laplace's law states that
   (a) $\Delta H$ forward equals $\Delta H$ backward (b) $\Delta H$ forward is the negative of $\Delta H$ backward (c) $\Delta H$ is always negative (d) $\Delta H$ depends on the path
10. The enthalpy of neutralisation of a strong acid by a strong base is about
   (a) −890 kJ mol⁻¹ (b) −285.8 kJ mol⁻¹ (c) +57.1 kJ mol⁻¹ (d) −57.1 kJ mol⁻¹
11. The unit of entropy is
   (a) J K⁻¹ mol⁻¹ (b) J mol⁻¹ (c) kJ mol⁻¹ (d) J K mol⁻¹
12. For a spontaneous process the second law requires that
   (a) $\Delta S$ of the system is negative (b) $\Delta S$ of the surroundings is zero (c) $\Delta S$ of the universe is positive (d) $\Delta H$ is negative
13. Gibbs free energy is defined as
   (a) $G = H + TS$ (b) $G = H - TS$ (c) $G = U - TS$ (d) $G = H/T - S$
14. A process is spontaneous when
   (a) $\Delta G > 0$ (b) $\Delta G = 0$ (c) $\Delta H < 0$ always (d) $\Delta G < 0$
15. The standard free energy change is related to the equilibrium constant by
   (a) $\Delta G^\circ = -RT\ln K$ (b) $\Delta G^\circ = RT\ln K$ (c) $\Delta G^\circ = -RT/K$ (d) $\Delta G^\circ = -\ln K/RT$
16. The enthalpy change when one mole of a substance is completely burnt in oxygen is the enthalpy of
   (a) formation (b) solution (c) combustion (d) neutralisation
17. The enthalpy of fusion of ice at 0 °C is about
   (a) 40.7 kJ mol⁻¹ (b) 22.0 kJ mol⁻¹ (c) 2.26 kJ mol⁻¹ (d) 6.01 kJ mol⁻¹
18. For an isolated system
   (a) $q = 0$ but $w$ is not zero (b) $\Delta U = 0$ (c) $\Delta H$ is always zero (d) $\Delta S = 0$
19. For a reaction involving gases
   (a) $\Delta H = \Delta U + \Delta n_gRT$ (b) $\Delta H = \Delta U - \Delta n_gRT$ (c) $\Delta U = \Delta H + \Delta n_gRT$ (d) $\Delta H = \Delta U/RT$
20. Which change has a positive entropy change?
   (a) 2H₂(g) + O₂(g) → 2H₂O(l) (b) N₂(g) + 3H₂(g) → 2NH₃(g) (c) CaCO₃(s) → CaO(s) + CO₂(g) (d) H₂O(g) → H₂O(l)
21. The standard enthalpy of combustion of methane is
   (a) −74.8 kJ mol⁻¹ (b) −890.3 kJ mol⁻¹ (c) −393.5 kJ mol⁻¹ (d) −285.8 kJ mol⁻¹
22. At constant volume, the heat exchanged equals
   (a) $\Delta H$ (b) $\Delta G$ (c) $\Delta S$ (d) $\Delta U$
23. The dissolution of ammonium nitrate in water is
   (a) thermally neutral (b) strongly exothermic (c) endothermic (d) equal to its enthalpy of fusion
24. Which of these is an extensive property?
   (a) mass (b) temperature (c) density (d) molar volume
25. At equilibrium, $\Delta G$ for the system is
   (a) negative (b) positive (c) $-RT$ (d) zero

::: note Answers and explanations — Set A
**1.** (c) — Open systems exchange both. A closed system exchanges only energy; an isolated system exchanges neither.
**2.** (b) — Enthalpy depends only on the state. Heat and work depend on the path and are not state functions.
**3.** (d) — Temperature does not depend on how much substance is present. Mass, volume and internal energy all do.
**4.** (a) — Energy is conserved; the first law is the law of conservation of energy written for a thermodynamic system.
**5.** (b) — IUPAC counts heat into the system and work done on the system as positive, so $\Delta U = q + w$.
**6.** (d) — A negative $\Delta H$ means heat leaves the system: exothermic.
**7.** (c) — Zero, but only in the standard state. Diamond and ozone have non-zero values.
**8.** (a) — Enthalpy is a state function, so $\Delta H$ is path-independent; that is the first law applied to $H$.
**9.** (b) — Reversing a reaction reverses the sign of the heat change, because the initial and final states are swapped.
**10.** (d) — −57.1 kJ mol⁻¹ for a strong acid and a strong base; weaker electrolytes give less negative values.
**11.** (a) — Entropy is energy per kelvin per mole; $\Delta S = q_{\text{rev}}/T$.
**12.** (c) — The total entropy of the universe must increase; the system's own entropy may fall if the surroundings gain more.
**13.** (b) — $G = H - TS$; the $-TS$ term carries the entropy contribution.
**14.** (d) — Negative $\Delta G$ is the criterion at constant temperature and pressure.
**15.** (a) — $\Delta G^\circ = -RT\ln K$; it is the bridge between thermodynamics and equilibrium.
**16.** (c) — Combustion, and it is always exothermic for a fuel.
**17.** (d) — 6.01 kJ mol⁻¹. 40.7 is the enthalpy of vaporisation; 2.26 is per gram, not per mole.
**18.** (b) — Neither heat nor work can cross the boundary, so the internal energy cannot change.
**19.** (a) — $\Delta H = \Delta U + P\Delta V$ and $P\Delta V = \Delta n_gRT$ for ideal gases.
**20.** (c) — A solid produces a gas, so disorder rises. The other three consume gas or condense it.
**21.** (b) — −890.3 kJ mol⁻¹. −74.8 is the enthalpy of formation of methane, −393.5 that of CO₂.
**22.** (d) — No pressure–volume work is possible at constant volume, so all the heat appears as $\Delta U$.
**23.** (c) — The lattice energy outweighs the hydration energy, so the solution cools: the cold pack.
**24.** (a) — Mass scales with amount. Temperature, density and molar volume are intensive.
**25.** (d) — At equilibrium there is no further driving force, so $\Delta G = 0$.
:::

**Set B — Understanding (15 questions)**

1. An ideal gas expands isothermally, so $\Delta U = 0$. This means
   (a) no heat is exchanged (b) the heat absorbed equals the work done by the gas (c) no work is done (d) the enthalpy change is also zero
2. For H₂(g) + I₂(g) → 2HI(g), $\Delta H = \Delta U$ because
   (a) the reaction is exothermic (b) no catalyst is used (c) the temperature is constant (d) $\Delta n_g = 0$
3. A reaction has $\Delta H > 0$ and $\Delta S > 0$. It is spontaneous
   (a) at high temperature (b) at all temperatures (c) at no temperature (d) only at low temperature
4. The enthalpy of formation of CO cannot be measured directly by burning carbon in a limited supply of oxygen because
   (a) CO is a gas (b) graphite is an allotrope (c) some CO₂ always forms as well (d) the reaction is endothermic
5. When a thermochemical equation is reversed, its $\Delta H$
   (a) stays the same (b) changes sign (c) doubles (d) becomes zero
6. Which statement about a catalyst is correct in thermodynamics?
   (a) It does not change $\Delta H$ or $\Delta G$ (b) It makes $\Delta G$ more negative (c) It raises the equilibrium constant (d) It lowers $\Delta H$
7. For a reaction with $\Delta G = 0$, the system is
   (a) far from equilibrium (b) spontaneous (c) non-spontaneous (d) at equilibrium
8. For the combustion of methane, $\Delta H$ is more negative than $\Delta U$ because
   (a) water is formed as a liquid (b) the reaction is exothermic (c) $\Delta n_g$ is negative (d) $\Delta n_g$ is positive
9. The entropy of a perfect crystal at 0 K is
   (a) maximum (b) zero (c) negative (d) infinite
10. For an exothermic reaction at constant pressure, the heat released is
   (a) $-\Delta H$ (b) $\Delta U$ (c) $-\Delta G$ (d) $T\Delta S$
11. Which reaction has a negative entropy change?
   (a) CaCO₃(s) → CaO(s) + CO₂(g) (b) I₂(s) → I₂(g) (c) 2H₂(g) + O₂(g) → 2H₂O(l) (d) NH₄Cl(s) → NH₃(g) + HCl(g)
12. A reaction has $\Delta G^\circ = -20$ kJ mol⁻¹ at 298 K. Its equilibrium constant is about
   (a) 1 (b) 0.1 (c) $3.2 \times 10^{-4}$ (d) $3.2 \times 10^{3}$
13. For N₂(g) + 3H₂(g) → 2NH₃(g), $\Delta S$ is negative mainly because
   (a) four moles of gas become two (b) the reaction is exothermic (c) a catalyst is used (d) ammonia is a gas
14. Which pair of signs makes a reaction spontaneous at every temperature?
   (a) $\Delta H > 0$, $\Delta S < 0$ (b) $\Delta H < 0$, $\Delta S > 0$ (c) $\Delta H > 0$, $\Delta S > 0$ (d) $\Delta H < 0$, $\Delta S < 0$
15. The enthalpy of sublimation of a solid equals
   (a) $\Delta H_{\text{fus}} - \Delta H_{\text{vap}}$ (b) $\Delta H_{\text{fus}} \times \Delta H_{\text{vap}}$ (c) $\Delta H_{\text{fus}} + \Delta H_{\text{vap}}$ (d) $\Delta H_{\text{vap}} - \Delta H_{\text{fus}}$

::: note Answers and explanations — Set B
**1.** (b) — With $\Delta U = 0$, the first law gives $q = -w$: all the heat absorbed is converted into work done by the gas.
**2.** (d) — $\Delta n_g = 2 - 2 = 0$, so $P\Delta V = 0$ and $\Delta H = \Delta U$.
**3.** (a) — $\Delta G = \Delta H - T\Delta S$; with both positive, $-T\Delta S$ eventually outweighs $\Delta H$, so the reaction turns spontaneous above $T = \Delta H/\Delta S$.
**4.** (c) — Carbon burnt in limited oxygen gives a mixture of CO and CO₂, so the heat change cannot be attributed to one product; Hess's law is used instead.
**5.** (b) — Laplace's law: the reverse reaction has the same magnitude of $\Delta H$ with the opposite sign.
**6.** (a) — A catalyst changes only the activation energy and the rate; $\Delta H$, $\Delta G$ and $K$ are untouched.
**7.** (d) — $\Delta G = 0$ is the equilibrium condition; there is no net driving force in either direction.
**8.** (c) — CH₄ + 2O₂ → CO₂ + 2H₂O(l) has $\Delta n_g = 1 - 3 = -2$, so $\Delta H = \Delta U - 2RT$, which is more negative.
**9.** (b) — Third law: a perfectly ordered crystal at absolute zero has zero entropy.
**10.** (a) — At constant pressure $q_p = \Delta H$, so the heat released is $-\Delta H$ when $\Delta H$ is negative.
**11.** (c) — Three moles of gas become a liquid, so disorder falls. The other three produce gas.
**12.** (d) — $\ln K = 20\,000/(8.314 \times 298) = 8.07$, so $K = e^{8.07} \approx 3.2 \times 10^3$.
**13.** (a) — Entropy falls when the number of gas molecules falls; the reaction is also exothermic, but that affects $\Delta H$, not $\Delta S$.
**14.** (b) — An exothermic reaction that also increases disorder is spontaneous at every temperature.
**15.** (c) — Sublimation is melting followed by boiling, and enthalpy is a state function, so the two steps add.
:::

**Set C — Application (10 questions)**

1. A gas expands from 2.0 L to 4.0 L against a constant 1.0 atm. The work done on the system is (1 L atm = 101.3 J)
   (a) +203 J (b) −405 J (c) −203 J (d) +405 J
2. A system absorbs 500 J of heat and does 200 J of work. Its $\Delta U$ is
   (a) +300 J (b) +700 J (c) −300 J (d) −700 J
3. For N₂(g) + 3H₂(g) → 2NH₃(g), $\Delta U = -87.4$ kJ mol⁻¹ at 298 K. $\Delta H$ is about
   (a) −82.4 kJ mol⁻¹ (b) −92.4 kJ mol⁻¹ (c) −87.4 kJ mol⁻¹ (d) −97.4 kJ mol⁻¹
4. Given $\Delta H_f^\circ$(CO₂) = −393.5 and $\Delta H_f^\circ$(CO) = −110.5 kJ mol⁻¹, the enthalpy of combustion of CO is
   (a) −504.0 kJ mol⁻¹ (b) −110.5 kJ mol⁻¹ (c) +283.0 kJ mol⁻¹ (d) −283.0 kJ mol⁻¹
5. From C(s) + O₂(g) → CO₂(g), $\Delta H = -393.5$ kJ, and CO(g) + ½O₂(g) → CO₂(g), $\Delta H = -283.0$ kJ, the enthalpy of formation of CO is
   (a) −110.5 kJ mol⁻¹ (b) −676.5 kJ mol⁻¹ (c) +110.5 kJ mol⁻¹ (d) −283.0 kJ mol⁻¹
6. A reaction has $\Delta H = +50$ kJ mol⁻¹ and $\Delta S = +100$ J K⁻¹ mol⁻¹. It becomes spontaneous above
   (a) 50 K (b) 200 K (c) 500 K (d) 5000 K
7. $\Delta H_{\text{vap}}$ of water is 40.7 kJ mol⁻¹ at 373 K. $\Delta S_{\text{vap}}$ is about
   (a) 40.7 J K⁻¹ mol⁻¹ (b) 109 J K⁻¹ mol⁻¹ (c) 0.109 J K⁻¹ mol⁻¹ (d) 15.2 J K⁻¹ mol⁻¹
8. The enthalpy of combustion of methane is −890.3 kJ mol⁻¹. The heat released when 3.2 g of methane burns completely is (CH₄ = 16)
   (a) 890.3 kJ (b) 44.5 kJ (c) 89.0 kJ (d) 178.1 kJ
9. For N₂ + 3H₂ → 2NH₃, $\Delta H^\circ = -92.4$ kJ mol⁻¹ and $\Delta S^\circ = -198$ J K⁻¹ mol⁻¹. $\Delta G^\circ$ at 298 K is about
   (a) −33.4 kJ mol⁻¹ (b) +33.4 kJ mol⁻¹ (c) −151.4 kJ mol⁻¹ (d) −59.0 kJ mol⁻¹
10. For the reaction in the previous question, $\Delta G^\circ$ becomes zero at about
   (a) 214 K (b) 298 K (c) 467 K (d) 1000 K

::: note Answers and explanations — Set C
**1.** (c) — $w = -P\Delta V = -(1.0)(2.0)$ L atm = $-2.0 \times 101.3 = -203$ J. Option (a) drops the sign; (b) doubles the volume change.
**2.** (a) — $q = +500$ J and $w = -200$ J (work done by the system), so $\Delta U = +300$ J. Option (b) treats the work as done on the system.
**3.** (b) — $\Delta n_g = -2$, so $\Delta H = -87.4 + (-2)(8.314)(298)/1000 = -87.4 - 4.96 = -92.4$ kJ mol⁻¹. Option (a) adds the term instead of subtracting it.
**4.** (d) — CO + ½O₂ → CO₂: $\Delta H = \Delta H_f$(CO₂) − $\Delta H_f$(CO) = $-393.5 - (-110.5) = -283.0$ kJ mol⁻¹. Option (c) reverses the sign; (a) adds the two.
**5.** (a) — Take the first equation and subtract the second: $-393.5 - (-283.0) = -110.5$ kJ mol⁻¹. Option (b) adds them instead of subtracting.
**6.** (c) — Spontaneous needs $T\Delta S > \Delta H$, so $T > 50\,000/100 = 500$ K. Option (a) forgets to convert kJ to J.
**7.** (b) — $\Delta S = \Delta H/T = 40\,700/373 = 109$ J K⁻¹ mol⁻¹. Option (a) forgets the division by $T$; (d) divides by the wrong temperature.
**8.** (d) — $n = 3.2/16 = 0.20$ mol, so heat $= 0.20 \times 890.3 = 178.1$ kJ. Option (a) is per mole; (b) is a quarter of a mole.
**9.** (a) — $\Delta G^\circ = -92.4 - (298)(-0.198) = -92.4 + 59.0 = -33.4$ kJ mol⁻¹. Option (c) subtracts the entropy term as well.
**10.** (c) — Set $\Delta G^\circ = 0$: $T = \Delta H/\Delta S = 92\,400/198 = 467$ K. Option (a) inverts the ratio.
:::
