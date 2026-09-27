---
subject: Chemistry
grade: 12
unit: 4
title: Thermodynamics
hours: 8
area: General and Physical Chemistry
---

Every chemical change moves energy about. Burning a cylinder of LPG in a
Kathmandu kitchen releases heat; dissolving ammonium nitrate in water makes the
beaker go cold. Thermodynamics is the book-keeping that tells us **how much**
energy moves, in which direction, and — most usefully — whether a reaction will
happen at all without being pushed. Three quantities do all the work: enthalpy
$H$, entropy $S$ and Gibbs free energy $G$.

::: key What the examiner wants from this unit
Four things, nearly every year: the first law with a sign-convention numerical,
a **Hess's law** calculation (often a Born–Haber cycle), the criterion
$\Delta G = \Delta H - T\Delta S$ applied to decide spontaneity, and
$\Delta G^{\circ} = -RT\ln K$. Learn the signs and you have the marks.
:::

## 4.1 Introduction; energy in chemical reactions

**Thermodynamics** is the study of energy changes accompanying physical and
chemical processes. It deals only with bulk, measurable properties — pressure,
volume, temperature, heat — and it says nothing about *how fast* a change occurs
(that is kinetics, Unit 3) or about individual molecules.

The part of the universe under study is the **system**; everything else is the
**surroundings**. The imaginary boundary between them decides what can cross it.

| Type of system | Exchanges matter? | Exchanges energy? | Example |
|---|---|---|---|
| Open | yes | yes | tea cooling in an open cup |
| Closed | no | yes | reaction in a sealed glass bulb |
| Isolated | no | no | hot water in a perfect thermos flask |

Any property that depends only on the present state of the system, and not on
the route taken to reach it, is a **state function**: $p$, $V$, $T$, $U$, $H$,
$S$, $G$. Heat $q$ and work $w$ are **path functions** — their values depend on
how the change was carried out.

| Process | Held constant | Condition |
|---|---|---|
| Isothermal | temperature | $\Delta T = 0$ |
| Isobaric | pressure | $\Delta p = 0$ |
| Isochoric | volume | $\Delta V = 0$, so $w = 0$ |
| Adiabatic | no heat exchange | $q = 0$ |
| Cyclic | system returns to start | $\Delta U = 0$, $\Delta H = 0$ |

**Where the energy comes from.** A reaction is bond-breaking followed by
bond-making. Breaking a bond always *costs* energy; making a bond always
*releases* it. The net enthalpy change is the difference:

$$ \Delta H = \sum (\text{bond enthalpies broken}) - \sum (\text{bond enthalpies formed}) $$

For H₂ + Cl₂ → 2HCl, the bonds broken are one H–H (436 kJ mol⁻¹) and one Cl–Cl
(242 kJ mol⁻¹); two H–Cl bonds are formed (431 kJ mol⁻¹ each):

$$ \Delta H = (436 + 242) - (2 \times 431) = 678 - 862 = -184\ \text{kJ mol}^{-1} $$

The negative sign means the products hold less energy than the reactants, so
184 kJ escapes into the surroundings for every mole of H₂ consumed. The measured
value is −184.6 kJ mol⁻¹.

## 4.2 Internal energy

::: definition Internal energy
The **internal energy** $U$ of a system is the total of all forms of energy
stored inside it — translational, rotational and vibrational energy of its
molecules, plus electronic and nuclear energy and the energy of intermolecular
attraction. It is a state function and an extensive property.
:::

Absolute values of $U$ cannot be measured, but *changes* can:

$$ \Delta U = U_{\text{final}} - U_{\text{initial}} = U_{2} - U_{1} $$

If the volume is kept constant no mechanical work is possible, so all the heat
supplied goes into raising the internal energy:

$$ q_{v} = \Delta U $$

This is why $\Delta U$ of combustion is measured in a **bomb calorimeter**, a
sealed steel vessel of fixed volume.

::: caution "Internal energy" is not "heat"
A system *contains* internal energy; it does not contain heat. Heat is energy in
transit across the boundary. Saying "the heat of the system is 200 J" is wrong;
"the system absorbed 200 J of heat" is right.
:::

## 4.3 First law of thermodynamics

::: definition First law of thermodynamics
Energy can neither be created nor destroyed, although it may be converted from
one form to another. Equivalently: the energy of an isolated system is constant.
For any process,

$$ \Delta U = q + w $$
:::

Everything depends on getting the signs right. The modern (IUPAC) convention is
written from the system's point of view:

| Quantity | Positive when | Negative when |
|---|---|---|
| $q$ | heat is **absorbed by** the system | heat is **released by** the system |
| $w$ | work is done **on** the system (compression) | work is done **by** the system (expansion) |

The only work a chemist normally meets is **pressure–volume work**. If a gas
expands by $\Delta V$ against a constant external pressure $p_{ext}$, the system
pushes the surroundings back, so it loses energy:

::: derivation Expression for pressure–volume work
Let the gas be in a cylinder of cross-sectional area $A$ fitted with a
frictionless piston, with a constant external pressure $p_{ext}$ pressing down.
The force on the piston is $F = p_{ext}A$. If the piston moves out a distance
$\Delta l$, the work done **by** the system is $F\Delta l = p_{ext}A\Delta l$.
But $A\Delta l = \Delta V$, the increase in volume. Since work done *by* the
system is negative in our convention,

$$ w = -p_{ext}\,\Delta V $$

Substituting in the first law gives the working form

$$ \Delta U = q - p_{ext}\,\Delta V $$

For a constant-volume change $\Delta V = 0$, so $w=0$ and $\Delta U = q_{v}$.
:::

::: example Worked example 4.1
**Problem.** Two moles of an ideal gas expand from 10.0 L to 25.0 L against a
constant external pressure of 1.50 atm. During the expansion the gas absorbs
3.50 kJ of heat. Calculate the work done and the change in internal energy.
(1 L atm = 101.3 J.)

**Solution.** The volume change is $\Delta V = 25.0 - 10.0 = 15.0$ L, and the
expansion is against a constant pressure, so

$$ w = -p_{ext}\Delta V = -(1.50\ \text{atm})(15.0\ \text{L}) = -22.5\ \text{L atm} $$

Converting, $w = -22.5 \times 101.3 = -2279\ \text{J} = -2.28\ \text{kJ}$. The
sign is negative because the gas did work on the surroundings.

Heat is absorbed, so $q = +3.50$ kJ. By the first law,

$$ \Delta U = q + w = 3.50 + (-2.28) = +1.22\ \text{kJ} $$

The internal energy rises by 1.22 kJ: of the 3.50 kJ taken in, 2.28 kJ was spent
pushing back the atmosphere and only 1.22 kJ was stored.
:::

## 4.4 Enthalpy and enthalpy changes (endothermic and exothermic)

Most reactions in a laboratory are run in open vessels, at the constant pressure
of the atmosphere, not at constant volume. The state function suited to constant
pressure is **enthalpy**:

$$ H = U + pV $$

::: derivation $\Delta H$ is the heat absorbed at constant pressure
At constant pressure, $\Delta H = \Delta U + p\Delta V$. From the first law with
only $p$–$V$ work, $\Delta U = q_{p} - p\Delta V$. Adding,

$$ \Delta H = (q_{p} - p\Delta V) + p\Delta V = q_{p} $$

So the enthalpy change of a reaction is simply the heat exchanged at constant
pressure — which is exactly what a calorimeter open to the air measures.
:::

For reactions involving gases, $p\Delta V = \Delta n_{g}RT$ where
$\Delta n_{g}$ is the change in the number of moles of **gas**, so

$$ \Delta H = \Delta U + \Delta n_{g}RT $$

A reaction is **exothermic** if it gives heat out ($\Delta H$ negative,
products below reactants on an enthalpy diagram) and **endothermic** if it takes
heat in ($\Delta H$ positive, products above reactants).

```figure caption="Enthalpy level diagrams. Left: an exothermic reaction, $\Delta H < 0$. Right: an endothermic reaction, $\Delta H > 0$. The vertical axis is enthalpy; only the difference is measurable."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(5.2, 3.1))
RED = '#A8271F'; GRN = '#0B6A62'

def panel(ax, hr, hp, col, title, dlab, eq1, eq2):
    ax.hlines(hr, 0.10, 0.44, color=INK, lw=2.0)
    ax.hlines(hp, 0.56, 0.92, color=INK, lw=2.0)
    ax.plot([0.44, 0.56], [hr, hp], color=MUTED, lw=0.9, ls=':')
    ax.annotate('', xy=(0.50, hp), xytext=(0.50, hr),
                arrowprops=dict(arrowstyle='-|>', color=col, lw=1.8, mutation_scale=13))
    ax.text(0.545, (hr + hp) / 2, dlab, color=col, fontsize=8.6, va='center')
    ax.text(0.27, hr + 0.035, 'reactants', ha='center', fontsize=8.4, color=INK)
    ax.text(0.74, hp + 0.035, 'products', ha='center', fontsize=8.4, color=INK)
    ax.text(0.5, 1.18, eq1, ha='center', fontsize=7.4, color=MUTED)
    ax.text(0.5, 1.07, eq2, ha='center', fontsize=7.4, color=MUTED)
    ax.set_title(title, fontsize=9.6, pad=6)
    ax.set_xlim(0.02, 1.02); ax.set_ylim(0.0, 1.30)
    ax.set_xticks([]); ax.set_yticks([])
    ax.spines[['top', 'right', 'bottom']].set_visible(False)

panel(axes[0], 0.80, 0.16, RED, 'Exothermic', 'ΔH negative\n(heat given out)',
      'CH₄ + 2O₂ → CO₂ + 2H₂O', 'ΔH = −890 kJ mol⁻¹')
panel(axes[1], 0.16, 0.80, GRN, 'Endothermic', 'ΔH positive\n(heat taken in)',
      'CaCO₃ → CaO + CO₂', 'ΔH = +178 kJ mol⁻¹')
axes[0].set_ylabel('enthalpy  $H$')
fig.subplots_adjust(wspace=0.30)
```
::: caution The sign is part of the answer
"ΔH = 890 kJ for the combustion of methane" is wrong and loses the mark. Heat is
*released*, so $\Delta H = -890\ \text{kJ mol}^{-1}$. Equally, an exothermic
reaction has a *negative* $\Delta H$ but makes the thermometer reading *rise* —
the two signs are opposite because the thermometer is in the surroundings.
:::

::: example Worked example 4.2
**Problem.** For the combustion of methane,
CH₄(g) + 2O₂(g) → CO₂(g) + 2H₂O(l), $\Delta H^{\circ} = -890.3$ kJ mol⁻¹ at
298 K. Calculate $\Delta U^{\circ}$. ($R = 8.314$ J K⁻¹ mol⁻¹.)

**Solution.** Count gas moles only — liquid water does not count.

Gaseous reactants: 1 (CH₄) + 2 (O₂) = 3 mol. Gaseous products: 1 (CO₂) = 1 mol.

$$ \Delta n_{g} = 1 - 3 = -2 $$

From $\Delta H = \Delta U + \Delta n_{g}RT$,

$$ \Delta U = \Delta H - \Delta n_{g}RT = -890.3 - (-2)(8.314\times10^{-3})(298) $$
$$ \Delta U = -890.3 + 4.96 = -885.3\ \text{kJ mol}^{-1} $$

Because the gas volume shrinks, the atmosphere does work *on* the system, so
less energy escapes as heat than the internal energy drop would suggest.
:::

## 4.5 Enthalpy of reaction, solution, formation, combustion

The **standard state** of a substance is its most stable form at 1 bar pressure
and the stated temperature (usually 298 K). A standard enthalpy change carries
the superscript circle, $\Delta H^{\circ}$.

| Name | Definition | Example |
|---|---|---|
| Enthalpy of reaction $\Delta H_{r}$ | Heat change when the molar amounts in the balanced equation react completely | N₂ + 3H₂ → 2NH₃, $\Delta H^{\circ} = -92.2$ kJ |
| Enthalpy of formation $\Delta H_{f}$ | Heat change when **one mole** of a compound is formed from its elements in their standard states | C(s) + 2H₂(g) → CH₄(g), $\Delta H_{f}^{\circ} = -74.8$ kJ mol⁻¹ |
| Enthalpy of combustion $\Delta H_{c}$ | Heat change when **one mole** of a substance burns completely in excess oxygen | C₂H₅OH(l) + 3O₂ → 2CO₂ + 3H₂O(l), $\Delta H_{c}^{\circ} = -1367$ kJ mol⁻¹ |
| Enthalpy of solution $\Delta H_{sol}$ | Heat change when one mole of a solute dissolves in so much solvent that further dilution causes no further heat change | NH₄Cl(s) + water → NH₄⁺(aq) + Cl⁻(aq), $\Delta H_{sol} = +15.1$ kJ mol⁻¹ |
| Enthalpy of neutralisation | Heat change when one gram-equivalent of acid is neutralised by a base in dilute solution | H⁺(aq) + OH⁻(aq) → H₂O(l), $\Delta H = -57.1$ kJ |

Two consequences worth remembering. First, $\Delta H_{f}^{\circ}$ of any
**element in its standard state is zero** — O₂(g), C(graphite), Br₂(l) all have
$\Delta H_{f}^{\circ} = 0$. Second, once a table of formation enthalpies exists,
any reaction enthalpy follows from

$$ \Delta H_{r}^{\circ} = \sum \Delta H_{f}^{\circ}(\text{products}) - \sum \Delta H_{f}^{\circ}(\text{reactants}) $$

Enthalpy of solution is itself the sum of two opposing terms: the **lattice
enthalpy** (energy needed to pull the ionic lattice apart, always positive) and
the **hydration enthalpy** of the separated ions (always negative). NH₄Cl
dissolves endothermically because its lattice enthalpy slightly outweighs
hydration — which is why an instant cold pack works.

## 4.6 Laws of thermochemistry: Laplace law and Hess's law

::: definition Lavoisier–Laplace law
The enthalpy change of a reaction is equal in magnitude but opposite in sign to
the enthalpy change of the reverse reaction.
:::

For example, if C(s) + O₂(g) → CO₂(g) has $\Delta H = -393.5$ kJ mol⁻¹, then
CO₂(g) → C(s) + O₂(g) has $\Delta H = +393.5$ kJ mol⁻¹. The law is just a
restatement of the first law: if it were not true you could run the forward and
backward reactions in a loop and manufacture energy from nothing.

::: definition Hess's law of constant heat summation
The total enthalpy change of a reaction is the same whether the reaction takes
place in one step or in several steps, provided the initial and final states are
the same.
:::

Hess's law follows because $H$ is a **state function**: $\Delta H$ depends only
on the endpoints, never the route. So around any closed cycle the enthalpy
changes sum to zero, and an unmeasurable $\Delta H$ can be found from measurable
ones.

```figure caption="A Hess's law cycle for the oxidation of carbon. The direct route ($\Delta H_1$) and the two-step route through CO ($\Delta H_2 + \Delta H_3$) must give the same total, so $\Delta H_1 = \Delta H_2 + \Delta H_3$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0, 3.1))
RED = '#A8271F'; GRN = '#0B6A62'
lv = {'a': 0.0, 'b': -110.5, 'c': -393.5}
ax.hlines(lv['a'], 0.05, 0.95, color=INK, lw=2.0)
ax.hlines(lv['b'], 1.30, 2.20, color=INK, lw=2.0)
ax.hlines(lv['c'], 2.55, 3.45, color=INK, lw=2.0)
ax.text(0.50, lv['a'] + 16, 'C(s) + O₂(g)', ha='center', fontsize=8.8, color=INK)
ax.text(1.75, lv['b'] + 16, 'CO(g) + ½O₂(g)', ha='center', fontsize=8.8, color=INK)
ax.text(3.00, lv['c'] + 16, 'CO₂(g)', ha='center', fontsize=8.8, color=INK)
ax.annotate('', xy=(1.30, lv['b']), xytext=(0.95, lv['a']),
            arrowprops=dict(arrowstyle='-|>', color=GRN, lw=1.7, mutation_scale=12))
ax.annotate('', xy=(2.55, lv['c']), xytext=(2.20, lv['b']),
            arrowprops=dict(arrowstyle='-|>', color=GRN, lw=1.7, mutation_scale=12))
ax.text(1.33, -132, 'ΔH₂ = −110.5', color=GRN, fontsize=8.4, va='top')
ax.text(2.50, -262, 'ΔH₃ = −283.0', color=GRN, fontsize=8.4, va='top')
ax.annotate('', xy=(0.50, lv['c']), xytext=(0.50, lv['a']),
            arrowprops=dict(arrowstyle='-|>', color=RED, lw=2.0, mutation_scale=13))
ax.text(0.60, -215, 'direct route\nΔH₁ = −393.5', color=RED, fontsize=8.4, va='center')
ax.set_xlim(0, 3.75); ax.set_ylim(-450, 80)
ax.set_ylabel('enthalpy  $H$  (kJ mol$^{-1}$)')
ax.set_xticks([])
ax.spines[['top', 'right', 'bottom']].set_visible(False)
ax.grid(axis='y', alpha=0.45)
```
::: example Worked example 4.3
**Problem.** Calculate the standard enthalpy of formation of methane from:

(i) C(s) + O₂(g) → CO₂(g), $\Delta H^{\circ} = -393.5$ kJ mol⁻¹
(ii) H₂(g) + ½O₂(g) → H₂O(l), $\Delta H^{\circ} = -285.8$ kJ mol⁻¹
(iii) CH₄(g) + 2O₂(g) → CO₂(g) + 2H₂O(l), $\Delta H^{\circ} = -890.3$ kJ mol⁻¹

**Solution.** The target equation is C(s) + 2H₂(g) → CH₄(g).

Take (i) as written, add 2 × (ii), and **subtract** (iii) — which means reversing
it and changing its sign, by the Lavoisier–Laplace law:

C(s) + O₂ → CO₂ ............... $-393.5$
2H₂ + O₂ → 2H₂O(l) ........... $2(-285.8) = -571.6$
CO₂ + 2H₂O(l) → CH₄ + 2O₂ ..... $+890.3$

Adding the three equations, CO₂ cancels, 2H₂O cancels, and of the oxygen
$1 + 1 - 2 = 0$ mol remain. What is left is exactly C(s) + 2H₂ → CH₄. Hence

$$ \Delta H_{f}^{\circ}(\text{CH}_4) = -393.5 - 571.6 + 890.3 = -74.8\ \text{kJ mol}^{-1} $$

The accepted value is −74.8 kJ mol⁻¹, a quantity that cannot be measured
directly because carbon and hydrogen do not combine cleanly to give methane.
:::

### The Born–Haber cycle

The most important application of Hess's law in inorganic chemistry is the
**Born–Haber cycle**, which finds the **lattice enthalpy** of an ionic solid —
the enthalpy change when one mole of the crystal is formed from its gaseous ions.
Lattice enthalpy cannot be measured directly; every other step in the cycle can.

```figure caption="Born–Haber cycle for sodium chloride as a Hess's law cycle. Both routes from Na(s) + ½Cl₂(g) to NaCl(s) must have the same total enthalpy change, which fixes the lattice enthalpy $U$ at −787 kJ mol$^{-1}$. All values in kJ mol$^{-1}$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.2, 3.3))
RED = '#A8271F'; GRN = '#0B6A62'
ax.set_xlim(0, 10); ax.set_ylim(0.1, 6.3); ax.axis('off')

def node(x, y, txt):
    ax.text(x, y, txt, ha='center', va='center', fontsize=8.8, color=INK)

A = (2.30, 5.40); B = (2.30, 3.35); C = (2.30, 1.10); D = (7.40, 1.10)
node(*A, 'Na(s) + ½Cl₂(g)')
node(*B, 'Na(g) + Cl(g)')
node(*C, 'Na⁺(g) + Cl⁻(g)')
node(*D, 'NaCl(s)')

# left column: the five atomising / ionising steps
ax.annotate('', xy=(2.30, 3.70), xytext=(2.30, 5.05),
            arrowprops=dict(arrowstyle='-|>', color=GRN, lw=1.7, mutation_scale=12))
ax.text(2.62, 4.60, 'sublimation  +108', fontsize=8.0, color=GRN)
ax.text(2.62, 4.18, '½ dissociation  +121', fontsize=8.0, color=GRN)
ax.annotate('', xy=(2.30, 1.45), xytext=(2.30, 3.00),
            arrowprops=dict(arrowstyle='-|>', color=GRN, lw=1.7, mutation_scale=12))
ax.text(2.62, 2.50, 'ionisation  +496', fontsize=8.0, color=GRN)
ax.text(2.62, 2.08, 'electron affinity  −349', fontsize=8.0, color=GRN)

# bottom: lattice enthalpy
ax.annotate('', xy=(6.85, 1.10), xytext=(3.55, 1.10),
            arrowprops=dict(arrowstyle='-|>', color=RED, lw=1.9, mutation_scale=12))
ax.text(5.20, 1.36, 'lattice enthalpy  U = −787', ha='center', fontsize=8.4, color=RED)

# the direct formation route, drawn as an elbow along the outside
ax.plot([3.55, 8.95], [5.40, 5.40], color=ACCENT, lw=1.9)
ax.plot([8.95, 8.95], [5.40, 1.10], color=ACCENT, lw=1.9)
ax.annotate('', xy=(7.95, 1.10), xytext=(8.95, 1.10),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.9, mutation_scale=12))
ax.text(6.15, 5.66, 'direct formation   ΔH$_f$ = −411', ha='center',
        fontsize=8.4, color=ACCENT)

ax.text(0.05, 0.32, 'Hess:  ΔH$_f$ = (+108) + (+121) + (+496) + (−349) + U',
        fontsize=8.2, color=INK, ha='left')
```
::: example Worked example 4.4
**Problem.** Use the Born–Haber cycle to calculate the lattice enthalpy of NaCl
from: enthalpy of formation of NaCl(s) = −411 kJ mol⁻¹; enthalpy of sublimation
of Na = +108 kJ mol⁻¹; first ionisation energy of Na = +496 kJ mol⁻¹; bond
dissociation enthalpy of Cl₂ = +242 kJ mol⁻¹; electron affinity of Cl = −349
kJ mol⁻¹.

**Solution.** Break the formation of NaCl(s) into five steps that add up to it:

| Step | Process | $\Delta H$ / kJ mol⁻¹ |
|---|---|---|
| 1 | Na(s) → Na(g) | +108 |
| 2 | ½Cl₂(g) → Cl(g) | $\tfrac{1}{2}(242) = +121$ |
| 3 | Na(g) → Na⁺(g) + e⁻ | +496 |
| 4 | Cl(g) + e⁻ → Cl⁻(g) | −349 |
| 5 | Na⁺(g) + Cl⁻(g) → NaCl(s) | $U = ?$ |

By Hess's law the five steps must total $\Delta H_{f}^{\circ}$:

$$ \Delta H_{f}^{\circ} = 108 + 121 + 496 + (-349) + U $$
$$ -411 = 376 + U \;\Longrightarrow\; U = -411 - 376 = -787\ \text{kJ mol}^{-1} $$

So 787 kJ is released when one mole of gaseous Na⁺ and Cl⁻ ions collapses into
the crystal — a very large number, which is why NaCl melts at 801 °C.
:::

::: tip Half a bond enthalpy, not a whole one
The formation equation is Na(s) + ½Cl₂(g) → NaCl(s), so only **half** the Cl–Cl
bond is broken. Forgetting the factor of ½ is the single commonest Born–Haber
error and shifts the answer by 121 kJ.
:::

## 4.7 Entropy and spontaneity

A **spontaneous** process is one that occurs on its own, without continuous
outside help: ice melting in a glass at room temperature, iron rusting, a gas
filling a vacuum. Exothermicity alone does not explain spontaneity — ice melts
spontaneously above 0 °C even though melting is endothermic. A second driving
force is at work: the tendency towards **disorder**.

::: definition Entropy
**Entropy** $S$ is a measure of the randomness or disorder of a system. It is a
state function. For a change carried out reversibly at constant temperature $T$,

$$ \Delta S = \frac{q_{rev}}{T} $$

Its SI unit is J K⁻¹ mol⁻¹.
:::

Entropy increases when disorder increases:

- **Phase changes:** $S_{\text{solid}} < S_{\text{liquid}} \ll S_{\text{gas}}$.
- **Number of gas molecules:** CaCO₃(s) → CaO(s) + CO₂(g) creates a gas, so
  $\Delta S > 0$. N₂ + 3H₂ → 2NH₃ destroys two moles of gas, so $\Delta S < 0$.
- **Dissolving** an ionic solid and **mixing** are entropy-increasing.
- **Heating** anything raises its entropy.

For a phase change at its transition temperature the process is reversible, so
$\Delta S = \Delta H / T$. For the melting of ice,
$\Delta S_{fus} = 6010 / 273 = 22.0$ J K⁻¹ mol⁻¹; for the boiling of water,
$\Delta S_{vap} = 40700 / 373 = 109.1$ J K⁻¹ mol⁻¹. Boiling disorders far more,
as expected.

The **third law of thermodynamics** completes the picture: the entropy of a
perfectly crystalline substance at absolute zero is zero. That gives entropy an
absolute scale, which is why tables list $S^{\circ}$ itself, not just
$\Delta S^{\circ}$.

## 4.8 Second law of thermodynamics

The first law says energy is conserved; it does not say which direction a change
will go. The second law supplies the direction.

::: key The second law, three equivalent statements
1. **Entropy statement.** In any spontaneous (irreversible) process the total
   entropy of the universe increases: $\Delta S_{total} > 0$. For a reversible
   process $\Delta S_{total} = 0$. It never decreases.
2. **Clausius statement.** Heat cannot flow of its own accord from a colder body
   to a hotter body.
3. **Kelvin–Planck statement.** It is impossible to construct a machine that,
   working in a cycle, converts heat completely into work without rejecting some
   heat to a colder reservoir.
:::

Writing the universe as system plus surroundings,

$$ \Delta S_{total} = \Delta S_{system} + \Delta S_{surroundings} > 0 \quad (\text{spontaneous}) $$

Note that $\Delta S_{system}$ alone may be negative — water freezing in a
Mustang winter becomes more ordered — provided the surroundings gain more entropy
than the system loses.

## 4.9 Gibbs free energy and prediction of spontaneity

Testing $\Delta S_{total}$ means measuring the surroundings, which is awkward.
J. W. Gibbs removed the need by defining a function of the **system only**:

$$ G = H - TS \qquad\text{so, at constant } T,\qquad \Delta G = \Delta H - T\Delta S $$

::: derivation The Gibbs criterion from the second law
At constant temperature and pressure the heat a reaction gives to its
surroundings is $-\Delta H_{sys}$, delivered reversibly at $T$, so

$$ \Delta S_{surr} = -\frac{\Delta H_{sys}}{T} $$

The second law requires $\Delta S_{total} > 0$ for a spontaneous change:

$$ \Delta S_{sys} - \frac{\Delta H_{sys}}{T} > 0 $$

Multiplying through by $-T$ (which reverses the inequality),

$$ \Delta H_{sys} - T\Delta S_{sys} < 0 $$

The left-hand side is defined as $\Delta G$. Hence a process at constant $T$ and
$p$ is spontaneous if and only if $\Delta G < 0$.
:::

| $\Delta H$ | $\Delta S$ | $\Delta G = \Delta H - T\Delta S$ | Spontaneous? |
|---|---|---|---|
| − | + | always negative | Yes, at **all** temperatures |
| − | − | negative at low $T$ | Only **below** $T = \Delta H/\Delta S$ |
| + | + | negative at high $T$ | Only **above** $T = \Delta H/\Delta S$ |
| + | − | always positive | **Never** |

$\Delta G$ also has a mechanical meaning: $-\Delta G$ is the maximum useful
(non-expansion) work obtainable from the change. At equilibrium
$\Delta G = 0$ and no further work can be extracted.

```figure caption="$\Delta G = \Delta H - T\Delta S$ is a straight line against temperature with slope $-\Delta S$ and intercept $\Delta H$. A reaction is spontaneous wherever its line lies below the dashed $\Delta G = 0$ axis."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0, 3.1))
T = np.linspace(0, 1000, 300)
cases = [(-100.0,  0.100, 'ΔH < 0, ΔS > 0 : spontaneous at all T', SERIES[2]),
         ( -60.0, -0.150, 'ΔH < 0, ΔS < 0 : only below 400 K', SERIES[0]),
         (  60.0,  0.100, 'ΔH > 0, ΔS > 0 : only above 600 K', SERIES[3]),
         (  80.0, -0.050, 'ΔH > 0, ΔS < 0 : never spontaneous', SERIES[1])]
for dH, dS, lab, c in cases:
    ax.plot(T, dH - T * dS, color=c, lw=1.8, label=lab)
ax.axhline(0, color=INK, lw=1.0, ls='--')
ax.plot([400, 600], [0, 0], 'o', color=INK, ms=4.5, zorder=5)
ax.text(418, 40, '400 K', fontsize=8.0, color=SERIES[0])
ax.text(612, -38, '600 K', fontsize=8.0, color=SERIES[3])
ax.text(40, -92, 'spontaneous region  (ΔG < 0)', fontsize=8.0, color=MUTED)
ax.set_xlabel('temperature  $T$  (K)')
ax.set_ylabel('$\\Delta G$  (kJ mol$^{-1}$)')
ax.set_xlim(0, 1000); ax.set_ylim(-230, 235)
ax.spines[['top', 'right']].set_visible(False)
ax.grid(alpha=0.45)
ax.legend(loc='upper center', fontsize=7.4, ncol=1, handlelength=1.6,
          labelspacing=0.28)
```
::: example Worked example 4.5
**Problem.** For the decomposition of limestone, CaCO₃(s) → CaO(s) + CO₂(g),
$\Delta H^{\circ} = +178.3$ kJ mol⁻¹ and $\Delta S^{\circ} = +160.6$
J K⁻¹ mol⁻¹. (a) Is the reaction spontaneous at 298 K? (b) Above what
temperature does it become spontaneous?

**Solution.**

(a) Convert the entropy to kJ: $\Delta S^{\circ} = 0.1606$ kJ K⁻¹ mol⁻¹.

$$ \Delta G^{\circ} = \Delta H^{\circ} - T\Delta S^{\circ} = 178.3 - (298)(0.1606) $$
$$ \Delta G^{\circ} = 178.3 - 47.9 = +130.4\ \text{kJ mol}^{-1} $$

$\Delta G^{\circ}$ is positive, so limestone does **not** decompose at room
temperature — fortunate, since Nepal's buildings are full of it.

(b) The changeover is where $\Delta G^{\circ} = 0$:

$$ T = \frac{\Delta H^{\circ}}{\Delta S^{\circ}} = \frac{178.3}{0.1606} = 1110\ \text{K} \;(837\ ^{\circ}\text{C}) $$

Above about 1110 K the $T\Delta S$ term wins and decomposition becomes
spontaneous. This is exactly why a cement kiln is run near 1400 °C.
:::

::: caution $\Delta G < 0$ does not mean "fast"
Thermodynamics predicts only *possibility*, not *speed*. The conversion of
diamond to graphite has $\Delta G^{\circ} = -2.9$ kJ mol⁻¹ and so is
spontaneous, yet a diamond lasts millions of years because the activation energy
is enormous. Spontaneous means "needs no help", not "happens quickly".
:::

## 4.10 Relationship between $\Delta G$ and equilibrium constant

For a reaction not at standard concentrations, the free energy change is

$$ \Delta G = \Delta G^{\circ} + RT\ln Q $$

where $Q$ is the reaction quotient — the same expression as the equilibrium
constant but with the actual, not equilibrium, concentrations. As the reaction
proceeds, $Q$ changes and $\Delta G$ rises towards zero.

::: derivation $\Delta G^{\circ} = -RT\ln K$
At equilibrium two things are true at once: the reaction has no further tendency
to move, so $\Delta G = 0$; and the quotient has reached its equilibrium value,
$Q = K$. Substituting both into the relation above,

$$ 0 = \Delta G^{\circ} + RT\ln K \;\Longrightarrow\; \Delta G^{\circ} = -RT\ln K = -2.303\,RT\log K $$
:::

| $\Delta G^{\circ}$ | $K$ | Position of equilibrium |
|---|---|---|
| negative | $K > 1$ | products favoured |
| zero | $K = 1$ | neither favoured |
| positive | $K < 1$ | reactants favoured |

::: example Worked example 4.6
**Problem.** At 298 K the equilibrium constant for N₂O₄(g) ⇌ 2NO₂(g) is
$K_{p} = 0.145$. Calculate $\Delta G^{\circ}$ for the dissociation.
($R = 8.314$ J K⁻¹ mol⁻¹.)

**Solution.** Use $\Delta G^{\circ} = -2.303\,RT\log K$.

$$ 2.303\,RT = 2.303 \times 8.314 \times 298 = 5706\ \text{J mol}^{-1} $$
$$ \log K = \log(0.145) = -0.8386 $$
$$ \Delta G^{\circ} = -(5706)(-0.8386) = +4785\ \text{J mol}^{-1} = +4.79\ \text{kJ mol}^{-1} $$

$\Delta G^{\circ}$ is positive and $K < 1$, so at 298 K and standard pressures
the dinitrogen tetroxide side is favoured — consistent with the fact that
N₂O₄ dissociation needs warming to go appreciably to the right.
:::

## Chapter summary

- A **system** exchanges matter and/or energy with its **surroundings**. $U$,
  $H$, $S$, $G$, $p$, $V$, $T$ are state functions; $q$ and $w$ are not.
- **First law:** $\Delta U = q + w$ with $w = -p_{ext}\Delta V$. At constant
  volume $q_{v} = \Delta U$; at constant pressure $q_{p} = \Delta H$.
- $H = U + pV$, so $\Delta H = \Delta U + \Delta n_{g}RT$ for gas reactions.
  $\Delta H < 0$ exothermic, $\Delta H > 0$ endothermic.
- $\Delta H_{r}^{\circ} = \sum\Delta H_{f}^{\circ}(\text{products}) - \sum\Delta H_{f}^{\circ}(\text{reactants})$,
  and $\Delta H_{f}^{\circ}$ of an element in its standard state is zero.
- **Lavoisier–Laplace:** reversing a reaction reverses the sign of $\Delta H$.
  **Hess's law:** $\Delta H$ is route-independent — the basis of the Born–Haber
  cycle, which gives lattice enthalpy (−787 kJ mol⁻¹ for NaCl).
- **Entropy** $S$ measures disorder, $\Delta S = q_{rev}/T$ in J K⁻¹ mol⁻¹;
  $S$ rises solid → liquid → gas.
- **Second law:** $\Delta S_{total} = \Delta S_{sys} + \Delta S_{surr} > 0$ for
  every spontaneous change.
- **Gibbs:** $\Delta G = \Delta H - T\Delta S$; spontaneous if $\Delta G < 0$,
  at equilibrium if $\Delta G = 0$; crossover at $T = \Delta H/\Delta S$.
- $\Delta G = \Delta G^{\circ} + RT\ln Q$ and
  $\Delta G^{\circ} = -RT\ln K = -2.303\,RT\log K$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Which of the following is **not** a state function? <span class="marks">[1]</span>
   (a) internal energy (b) enthalpy (c) work (d) entropy
2. For the isothermal expansion of an ideal gas, $\Delta U$ is <span class="marks">[1]</span>
   (a) positive (b) negative (c) zero (d) equal to $w$
3. For N₂(g) + 3H₂(g) → 2NH₃(g), the value of $\Delta H - \Delta U$ is <span class="marks">[1]</span>
   (a) $+2RT$ (b) $-2RT$ (c) $+RT$ (d) zero
4. A reaction is spontaneous at all temperatures when <span class="marks">[1]</span>
   (a) $\Delta H < 0, \Delta S < 0$ (b) $\Delta H > 0, \Delta S > 0$
   (c) $\Delta H < 0, \Delta S > 0$ (d) $\Delta H > 0, \Delta S < 0$
5. If $\Delta G^{\circ} = 0$ for a reaction at temperature $T$, then $K$ equals <span class="marks">[1]</span>
   (a) 0 (b) 1 (c) infinity (d) $e$
6. The entropy of a perfectly crystalline solid at 0 K is <span class="marks">[1]</span>
   (a) zero (b) positive (c) negative (d) infinite

::: note Answers to Group A
**1.** (c) — work depends on the path taken, not just on the endpoints.

**2.** (c) — $U$ of an ideal gas depends only on $T$, and $T$ is constant.

**3.** (b) — $\Delta n_{g} = 2 - 4 = -2$, and $\Delta H - \Delta U = \Delta n_{g}RT$.

**4.** (c) — then $-T\Delta S$ is negative too, so $\Delta G$ is negative at every $T$.

**5.** (b) — $\Delta G^{\circ} = -RT\ln K$, so $\ln K = 0$ and $K = 1$.

**6.** (a) — third law of thermodynamics: perfect order means zero disorder.
:::

**Group B — Short answer (5 marks each)**

1. Define internal energy. State the first law of thermodynamics and derive the
   expression $w = -p_{ext}\Delta V$ for the work done in an isobaric expansion. <span class="marks">[5]</span>
2. Define enthalpy of formation, enthalpy of combustion, enthalpy of solution and
   enthalpy of neutralisation, giving one thermochemical equation for each. <span class="marks">[5]</span>
3. State Hess's law. Given C(s) + O₂(g) → CO₂(g), $\Delta H = -393.5$ kJ mol⁻¹ and
   CO(g) + ½O₂(g) → CO₂(g), $\Delta H = -283.0$ kJ mol⁻¹, calculate the enthalpy of
   formation of carbon monoxide. <span class="marks">[5]</span>
4. For a certain reaction $\Delta H = 30.56$ kJ mol⁻¹ and $\Delta S = 66.0$
   J K⁻¹ mol⁻¹. Calculate $\Delta G$ at 300 K and find the temperature at which
   the reaction becomes spontaneous. <span class="marks">[5]</span>
5. Derive $\Delta G = \Delta H - T\Delta S$ from the second law, and use it to
   discuss the four possible sign combinations of $\Delta H$ and $\Delta S$. <span class="marks">[5]</span>
6. The equilibrium constant of a reaction at 298 K is $1.0\times10^{5}$.
   Calculate $\Delta G^{\circ}$ and comment on the position of equilibrium. <span class="marks">[5]</span>

::: note Answers to Group B
**3.** Hess's law: the enthalpy change is the same by whatever route the reaction
is carried out. The target is C(s) + ½O₂(g) → CO(g). Subtract the second equation
from the first (i.e. reverse the second and add):

C(s) + O₂ → CO₂ ..... $-393.5$; CO₂ → CO + ½O₂ ..... $+283.0$

$$ \Delta H_{f}^{\circ}(\text{CO}) = -393.5 + 283.0 = -110.5\ \text{kJ mol}^{-1} $$

**4.** With $\Delta S = 0.0660$ kJ K⁻¹ mol⁻¹,

$$ \Delta G_{300} = 30.56 - (300)(0.0660) = 30.56 - 19.80 = +10.76\ \text{kJ mol}^{-1} $$

so it is non-spontaneous at 300 K. Setting $\Delta G = 0$,
$T = 30.56/0.0660 = 463\ \text{K}$; above 463 K the reaction is spontaneous.

**6.** $\Delta G^{\circ} = -2.303RT\log K = -(2.303)(8.314)(298)\log(10^{5})
= -(5706)(5) = -28530\ \text{J mol}^{-1} = -28.53\ \text{kJ mol}^{-1}$.
Since $\Delta G^{\circ}$ is large and negative and $K \gg 1$, the equilibrium
lies far to the product side.
:::

**Group C — Long answer (8 marks each)**

1. (a) State Hess's law of constant heat summation and explain why it follows
   from enthalpy being a state function. <span class="marks">[3]</span>
   (b) Construct a Born–Haber cycle for potassium chloride and calculate its
   lattice enthalpy from: $\Delta H_{f}^{\circ}(\text{KCl}) = -437$ kJ mol⁻¹,
   enthalpy of sublimation of K = +89 kJ mol⁻¹, ionisation energy of K = +419
   kJ mol⁻¹, bond dissociation enthalpy of Cl₂ = +242 kJ mol⁻¹, electron affinity
   of Cl = −349 kJ mol⁻¹. Explain why the lattice enthalpy of NaCl is more
   negative than that of KCl. <span class="marks">[5]</span>
2. (a) State the second law of thermodynamics in two different ways and define
   entropy. Explain, using $\Delta S_{total}$, how water can freeze
   spontaneously in winter although freezing decreases the entropy of the water. <span class="marks">[4]</span>
   (b) The enthalpy of vaporisation of water at 373 K is 40.7 kJ mol⁻¹.
   Calculate $\Delta S_{vap}$, and hence $\Delta G$ for the vaporisation at
   373 K and at 383 K. Interpret both answers. <span class="marks">[4]</span>

::: note Answers to Group C
**1.(b)** The steps are: K(s) → K(g), +89; ½Cl₂(g) → Cl(g),
$\tfrac{1}{2}(242) = +121$; K(g) → K⁺(g) + e⁻, +419; Cl(g) + e⁻ → Cl⁻(g), −349;
K⁺(g) + Cl⁻(g) → KCl(s), $U$. By Hess's law

$$ -437 = 89 + 121 + 419 - 349 + U = 280 + U \;\Longrightarrow\; U = -717\ \text{kJ mol}^{-1} $$

Lattice enthalpy varies as $1/(r_{+} + r_{-})$. Na⁺ (102 pm) is smaller than
K⁺ (138 pm), so the ions in NaCl sit closer together, the electrostatic
attraction is stronger and the lattice enthalpy is more negative
(−787 against −717 kJ mol⁻¹).

**2.(b)** Vaporisation at the normal boiling point is a reversible change, so

$$ \Delta S_{vap} = \frac{\Delta H_{vap}}{T} = \frac{40700}{373} = 109.1\ \text{J K}^{-1}\text{mol}^{-1} $$

At 373 K: $\Delta G = 40700 - (373)(109.1) = 0$. Liquid and vapour are in
equilibrium — which is what "boiling point" means.

At 383 K: $\Delta G = 40700 - (383)(109.1) = 40700 - 41785 = -1085\ \text{J mol}^{-1}
= -1.09\ \text{kJ mol}^{-1}$, negative, so above 373 K vaporisation is
spontaneous and the liquid boils away.
:::
