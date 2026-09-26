---
subject: Chemistry
grade: 12
unit: 3
title: Chemical Kinetics
hours: 7
area: General and Physical Chemistry
---

Thermodynamics tells you **whether** a reaction can happen. It says nothing about
**how long** it will take. The conversion of diamond into graphite releases energy
and is perfectly spontaneous, yet a diamond ring survives a lifetime unchanged.
Petrol and air sitting in a fuel tank are thermodynamically doomed, but nothing
happens until a spark arrives. Chemical kinetics supplies the missing half of the
story: the rate of a reaction, the concentration terms that control it, and the
energy barrier that a collision must clear.

::: key What the examiner asks from this unit
One MCQ on order versus molecularity or on the units of $k$; one 5-mark numerical
on a first-order reaction, a half-life or the Arrhenius equation; and very often a
drawing question — the energy-profile diagram with and without a catalyst, or the
Maxwell-Boltzmann curve at two temperatures. The two equations you must be able to
write from memory are $k = \frac{2.303}{t}\log\frac{[A]_0}{[A]}$ and
$\log\frac{k_2}{k_1} = \frac{E_a}{2.303R}\left(\frac{T_2-T_1}{T_1T_2}\right)$.
:::

## 3.1 Introduction

**Chemical kinetics** is the branch of chemistry that deals with the *rate* of a
chemical reaction, the *factors* that affect that rate, and the *mechanism* — the
sequence of elementary steps — by which reactants become products.

By speed, reactions fall into three broad classes.

| Class | Time scale | Examples |
|---|---|---|
| Very fast (ionic) | 10⁻¹² – 10⁻³ s | AgNO₃ + NaCl → AgCl↓ + NaNO₃; HCl + NaOH → NaCl + H₂O |
| Very slow | months to millions of years | rusting of iron, 4Fe + 3O₂ → 2Fe₂O₃; chemical weathering of limestone in the Mahabharat hills; formation of coal |
| Moderate (measurable) | minutes to hours | 2H₂O₂ → 2H₂O + O₂; hydrolysis of an ester; inversion of cane sugar |

Only the middle class is convenient to study in the laboratory. Very fast ionic
reactions need special relaxation techniques; very slow ones show no measurable
change during a practical class.

Why the subject matters: it fixes the residence time of a reactor in the Hetauda
cement works, the expiry date printed on a strip of paracetamol, the rate at which
food spoils in the Terai heat, and how long the chlorine added to a Kathmandu water
tank stays effective.

## 3.2 Rate of reactions: average and instantaneous

::: definition Rate of reaction
The **rate of a reaction** is the change in the concentration of a reactant or a
product per unit time. For the reaction R → P,

$$ \text{average rate} = -\frac{\Delta[\text{R}]}{\Delta t}
= +\frac{\Delta[\text{P}]}{\Delta t} $$

The minus sign makes the rate a positive quantity, because $\Delta[\text{R}]$ is
itself negative. The SI unit is mol L⁻¹ s⁻¹ (for gases, atm s⁻¹ is also used).
:::

The average rate is the *slope of the chord* joining two points on the
concentration-time curve. It is a blunt instrument: a reactant is used up fastest
at the start and slowest at the end, so an average taken over a long interval
describes neither.

The **instantaneous rate** is the rate at one particular moment — the limit of the
average rate as the interval shrinks to zero:

$$ r_{\text{inst}} = \lim_{\Delta t \to 0}
\left(-\frac{\Delta[\text{R}]}{\Delta t}\right) = -\frac{d[\text{R}]}{dt} $$

Graphically it is the *slope of the tangent* drawn to the curve at that instant.
The instantaneous rate at $t = 0$ is called the **initial rate**, and it is the
quantity used to find the rate law, because at $t = 0$ the concentrations are
exactly what you made them and no product has yet accumulated.

```figure caption="Concentration against time for R → P. The dashed chord gives the average rate over 0–40 s; the solid tangent at $t = 40$ s gives the instantaneous rate at that moment. The chord is steeper than the tangent because the reaction was faster earlier."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,3.0))
k = 0.02; C0 = 1.00
t = np.linspace(0, 100, 400)
R = C0*np.exp(-k*t); P = C0 - R
ax.plot(t, R, color=ACCENT, lw=2.0)
ax.plot(t, P, color=SERIES[2], lw=2.0)
t1, t2 = 0.0, 40.0
R1, R2 = C0*np.exp(-k*t1), C0*np.exp(-k*t2)
ax.plot([t1, t2], [R1, R2], color=SERIES[1], lw=1.3, ls=(0,(5,2)))
ax.plot([t1, t2], [R1, R2], 'o', color=SERIES[1], ms=4)
slope = -k*R2
tl = np.array([12.0, 78.0])
ax.plot(tl, R2 + slope*(tl - t2), color=INK, lw=1.3)
ax.plot([t2], [R2], 'o', color=INK, ms=4.5)
ax.annotate('average rate\n= slope of chord', xy=(20, 0.70), xytext=(27, 0.88),
            fontsize=7.6, color=SERIES[1], ha='left',
            arrowprops=dict(arrowstyle='->', color=SERIES[1], lw=0.9))
ax.annotate('instantaneous rate\n= slope of tangent', xy=(57, 0.315),
            xytext=(45, 0.47), fontsize=7.6, color=INK, ha='left',
            arrowprops=dict(arrowstyle='->', color=INK, lw=0.9))
ax.text(99, 0.22, 'reactant [R]', fontsize=8.2, color=ACCENT, ha='right')
ax.text(99, 0.72, 'product [P]', fontsize=8.2, color=SERIES[2], ha='right')
ax.set_xlabel('time  t  (s)')
ax.set_ylabel('concentration  (mol L⁻¹)')
ax.set_xlim(0, 100); ax.set_ylim(0, 1.15)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=0.35)
```

### Rate of reaction versus rate of change of a single species

For a reaction with unequal coefficients the species disappear and appear at
different numerical rates. For

$$ a\text{A} + b\text{B} \longrightarrow c\text{C} + d\text{D} $$

the single quantity called *the rate of reaction* is

$$ r = -\frac{1}{a}\frac{d[\text{A}]}{dt} = -\frac{1}{b}\frac{d[\text{B}]}{dt}
= +\frac{1}{c}\frac{d[\text{C}]}{dt} = +\frac{1}{d}\frac{d[\text{D}]}{dt} $$

::: caution A very common slip
For N₂ + 3H₂ → 2NH₃, hydrogen disappears three times as fast as nitrogen and
ammonia appears twice as fast as nitrogen is used up. Divide by the coefficient
before you equate anything. Writing $-d[\text{H}_2]/dt = +d[\text{NH}_3]/dt$ is
wrong by a factor of 1.5.
:::

::: example Worked example 3.1 — average rate and the rates of individual species
**Problem.** In the reaction 2N₂O₅ → 4NO₂ + O₂, the concentration of N₂O₅ falls
from 0.50 mol L⁻¹ to 0.40 mol L⁻¹ in 100 s. Calculate (a) the average rate of
disappearance of N₂O₅, (b) the average rate of the reaction, and (c) the rates of
formation of NO₂ and of O₂.

**Solution.**

(a) $-\dfrac{\Delta[\text{N}_2\text{O}_5]}{\Delta t} = \dfrac{0.50 - 0.40}{100} = 1.0\times10^{-3}$ mol L⁻¹ s⁻¹.

(b) Divide by the coefficient of N₂O₅, which is 2:

$$ r = -\frac{1}{2}\frac{\Delta[\text{N}_2\text{O}_5]}{\Delta t}
= \frac{1.0\times10^{-3}}{2} = 5.0\times10^{-4}\ \text{mol L}^{-1}\text{s}^{-1} $$

(c) $\dfrac{\Delta[\text{NO}_2]}{\Delta t} = 4r = 4 \times 5.0\times10^{-4} = 2.0\times10^{-3}$ mol L⁻¹ s⁻¹ and
$\dfrac{\Delta[\text{O}_2]}{\Delta t} = 1 \times r = 5.0\times10^{-4}$ mol L⁻¹ s⁻¹.

Check the arithmetic against the stoichiometry: NO₂ appears four times as fast as
O₂, and 2.0×10⁻³ is indeed four times 5.0×10⁻⁴.
:::

## 3.3 Rate law and its expressions

::: definition Rate law
The **rate law** (or rate equation) is the experimentally determined expression
that relates the rate of a reaction to the concentrations of the reactants, each
raised to some power. For A + B → products,

$$ r = k[\text{A}]^{x}[\text{B}]^{y} $$

where $x$ and $y$ are found by experiment and $k$ is the rate constant.
:::

The powers $x$ and $y$ **cannot be read off the balanced equation**. They must be
measured. The table below makes the point; in every row the balanced equation would
predict something different from what is observed.

| Reaction | Balanced equation suggests | Observed rate law | Overall order |
|---|---|---|---|
| 2N₂O₅ → 4NO₂ + O₂ | $[\text{N}_2\text{O}_5]^2$ | $r = k[\text{N}_2\text{O}_5]$ | 1 |
| H₂ + I₂ → 2HI | $[\text{H}_2][\text{I}_2]$ | $r = k[\text{H}_2][\text{I}_2]$ | 2 |
| 2NO₂ + F₂ → 2NO₂F | $[\text{NO}_2]^2[\text{F}_2]$ | $r = k[\text{NO}_2][\text{F}_2]$ | 2 |
| CHCl₃ + Cl₂ → CCl₄ + HCl | $[\text{CHCl}_3][\text{Cl}_2]$ | $r = k[\text{CHCl}_3][\text{Cl}_2]^{1/2}$ | 1.5 |
| 2H₂O₂ → 2H₂O + O₂ | $[\text{H}_2\text{O}_2]^2$ | $r = k[\text{H}_2\text{O}_2]$ | 1 |

The reason is mechanism. A balanced equation is only a bookkeeping statement of
what goes in and what comes out; the rate is fixed by the **slowest step** of the
sequence, and only the species in that step appear in the rate law.

### Finding the rate law: the initial-rate method

Run the reaction several times, changing one concentration at a time, and measure
the initial rate each time.

- If doubling [A] doubles the rate, the order in A is 1 ($2^1 = 2$).
- If doubling [A] quadruples the rate, the order in A is 2 ($2^2 = 4$).
- If doubling [A] leaves the rate unchanged, the order in A is 0 ($2^0 = 1$).

::: example Worked example 3.2 — order from initial-rate data
**Problem.** For the reaction A + 2B → C the following initial rates were measured
at 298 K.

| Experiment | [A] / mol L⁻¹ | [B] / mol L⁻¹ | initial rate / mol L⁻¹ s⁻¹ |
|---|---|---|---|
| 1 | 0.10 | 0.10 | 2.0 × 10⁻³ |
| 2 | 0.20 | 0.10 | 4.0 × 10⁻³ |
| 3 | 0.10 | 0.20 | 8.0 × 10⁻³ |

Find the order with respect to each reactant, the overall order, the rate law and
the value of $k$ with its units.

**Solution.**

Let $r = k[\text{A}]^{x}[\text{B}]^{y}$.

*Experiments 1 and 2* ([B] constant): [A] is doubled and the rate doubles, so
$2^{x} = 2$ and $x = 1$.

*Experiments 1 and 3* ([A] constant): [B] is doubled and the rate becomes four
times larger, so $2^{y} = 4$ and $y = 2$.

Hence the rate law is $r = k[\text{A}][\text{B}]^{2}$ and the overall order is
$1 + 2 = 3$ — even though the coefficient of A in the equation is 1 and of B is 2,
which would have predicted order 3 by coincidence but the wrong *individual*
orders.

From experiment 1,

$$ k = \frac{r}{[\text{A}][\text{B}]^{2}}
= \frac{2.0\times10^{-3}}{(0.10)(0.10)^{2}}
= \frac{2.0\times10^{-3}}{1.0\times10^{-3}}
= 2.0\ \text{L}^{2}\text{mol}^{-2}\text{s}^{-1} $$

The units are those of a third-order rate constant, which confirms the order.
:::

## 3.4 Rate constant, its unit and significance

::: definition Rate constant
For $r = k[\text{A}]^{x}[\text{B}]^{y}$, the **rate constant** $k$ is the rate of
the reaction when the concentration of every reactant is unity. It is therefore
also called the **specific reaction rate**.
:::

### Units of the rate constant

Rearranging the rate law, $k = r/[\,]^{n}$ where $n$ is the overall order. With
$r$ in mol L⁻¹ s⁻¹ and concentration in mol L⁻¹,

$$ [k] = \frac{\text{mol L}^{-1}\text{s}^{-1}}{(\text{mol L}^{-1})^{n}}
= (\text{mol L}^{-1})^{1-n}\,\text{s}^{-1} $$

| Overall order $n$ | Units of $k$ |
|---|---|
| 0 | mol L⁻¹ s⁻¹ |
| 1 | s⁻¹ |
| 2 | L mol⁻¹ s⁻¹ (= mol⁻¹ L s⁻¹) |
| 3 | L² mol⁻² s⁻¹ |
| $\tfrac{1}{2}$ | mol$^{1/2}$ L$^{-1/2}$ s⁻¹ |

::: memory Reading the order off the units
Count the power of "mol" in the units of $k$ and subtract it from 1. If $k$ is in
L mol⁻¹ s⁻¹ the power of mol is $-1$, so $n = 1-(-1) = 2$: second order. Notice
that a first-order $k$ is the only one whose units contain no concentration at
all, which is why a first-order rate constant can be quoted in s⁻¹, min⁻¹ or
year⁻¹ without any reference to volume.
:::

### Significance of $k$

1. It is a **measure of the intrinsic speed** of a reaction, free of the accident
   of how concentrated the solution happens to be. Two reactions can be compared
   only through their rate constants, never through their rates.
2. It is **independent of concentration** but **depends on temperature** — roughly
   doubling for every 10 K rise — and on the presence of a catalyst.
3. A **large $k$ means a fast reaction.** For the same order, the reaction with the
   larger $k$ goes faster at any given concentration.
4. Its **units reveal the overall order**, as in the box above.
5. It is characteristic of a particular reaction at a particular temperature, so
   it is tabulated in data books and used to calculate rates, half-lives and
   activation energies.

::: example Worked example 3.3 — using the units of $k$
**Problem.** The rate constant of a reaction is $3.0\times10^{-2}$ L mol⁻¹ s⁻¹.
(a) What is the order of the reaction? (b) Write its rate law for a single
reactant A. (c) Calculate the rate when [A] = 0.20 mol L⁻¹, and (d) state what
happens to that rate if [A] is trebled.

**Solution.**

(a) The units contain mol⁻¹, so $1-n = -1$ and $n = 2$: the reaction is
**second order**.

(b) $r = k[\text{A}]^{2}$.

(c) $r = 3.0\times10^{-2} \times (0.20)^{2} = 3.0\times10^{-2}\times0.040 = 1.2\times10^{-3}$ mol L⁻¹ s⁻¹.

(d) Rate $\propto [\text{A}]^{2}$, so trebling [A] multiplies the rate by
$3^{2} = 9$; the new rate is $1.08\times10^{-2}$ mol L⁻¹ s⁻¹. The rate constant
itself does not change.
:::

## 3.5 Order and molecularity

::: definition Order and molecularity
The **order** of a reaction is the sum of the powers of the concentration terms in
the experimentally determined rate law. The **molecularity** of a reaction is the
number of reactant species (atoms, ions or molecules) that take part in a single
elementary step, as written in the balanced equation for that step.
:::

| | Order | Molecularity |
|---|---|---|
| How obtained | experimentally, from the rate law | theoretically, by counting species in an elementary step |
| Possible values | 0, 1, 2, 3, and fractional values | 1, 2, 3 only — whole numbers |
| Can it be zero? | yes (photochemical and surface reactions) | no |
| Applies to | overall reaction or an elementary step | an elementary step only |
| Effect of conditions | can change (pseudo-order in excess solvent) | fixed |

For an **elementary** reaction — one that happens in a single step — order and
molecularity are equal. They differ for **complex** reactions, which proceed in
several steps.

**Fractional order.** The observed law
$r = k[\text{CHCl}_3][\text{Cl}_2]^{1/2}$ gives order 1.5. No molecule can be
"half" present in a collision; the half-power is the fingerprint of a chain
mechanism in which Cl₂ ⇌ 2Cl· supplies the reacting atom.

**Zero order.** In the decomposition of ammonia on a hot tungsten surface,
2NH₃ → N₂ + 3H₂, the metal is saturated with adsorbed NH₃, so adding more ammonia
cannot speed anything up: $r = k$. The photochemical combination
H₂ + Cl₂ → 2HCl is zero order in both gases because the rate is set by the
intensity of the light.

**Pseudo-order (pseudo-unimolecular) reactions.** Hydrolysis of cane sugar,

C₁₂H₂₂O₁₁ + H₂O → C₆H₁₂O₆ + C₆H₁₂O₆,

is bimolecular, and the true rate law is
$r = k'[\text{C}_{12}\text{H}_{22}\text{O}_{11}][\text{H}_2\text{O}]$. But water is
the solvent and is present in vast excess, so $[\text{H}_2\text{O}]$ hardly changes
and is absorbed into the constant: $r = k[\text{C}_{12}\text{H}_{22}\text{O}_{11}]$.
The reaction is second order in reality and **first order in behaviour** — a
pseudo-first-order reaction. The acid hydrolysis of an ester,
CH₃COOC₂H₅ + H₂O → CH₃COOH + C₂H₅OH, is the other standard example.

```figure caption="Rate against reactant concentration for zero-, first- and second-order reactions. A zero-order rate is a horizontal line, a first-order rate is a straight line through the origin of slope $k$, and a second-order rate is a parabola."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.8))
C = np.linspace(0, 1.0, 300)
ax.plot(C, 0.40*np.ones_like(C), color=SERIES[2], lw=2.0,
        label='zero order:  r = k')
ax.plot(C, 0.80*C, color=ACCENT, lw=2.0, label='first order:  r = k[A]')
ax.plot(C, 0.90*C**2, color=SERIES[1], lw=2.0, ls=(0,(5,2)),
        label='second order:  r = k[A]²')
ax.set_xlabel('[A]   (mol L⁻¹)')
ax.set_ylabel('rate   (mol L⁻¹ s⁻¹)')
ax.set_xlim(0, 1.0); ax.set_ylim(0, 0.95)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=0.35)
ax.legend(loc='upper left', fontsize=7.8)
```

## 3.6 Integrated rate equation for zero and first order reaction

The rate law is a *differential* equation. Integrating it gives a relation between
concentration and time that can be tested directly against experimental data.

::: derivation Zero-order integrated rate equation
For A → products with $r = k[\text{A}]^{0} = k$,

$$ -\frac{d[\text{A}]}{dt} = k \quad\Longrightarrow\quad -d[\text{A}] = k\,dt $$

Integrate from $[\text{A}]_0$ at $t = 0$ to $[\text{A}]$ at time $t$:

$$ -\int_{[\text{A}]_0}^{[\text{A}]} d[\text{A}] = k\int_{0}^{t} dt
\quad\Longrightarrow\quad [\text{A}]_0 - [\text{A}] = kt $$

$$ \boxed{[\text{A}] = [\text{A}]_0 - kt} \qquad
k = \frac{[\text{A}]_0 - [\text{A}]}{t} $$

A plot of $[\text{A}]$ against $t$ is therefore a **straight line** of slope $-k$
and intercept $[\text{A}]_0$. The reactant is used up at a steady rate and vanishes
completely at $t = [\text{A}]_0/k$.
:::

::: derivation First-order integrated rate equation
For A → products with $r = k[\text{A}]$,

$$ -\frac{d[\text{A}]}{dt} = k[\text{A}] \quad\Longrightarrow\quad
-\frac{d[\text{A}]}{[\text{A}]} = k\,dt $$

Integrating between the same limits,

$$ -\int_{[\text{A}]_0}^{[\text{A}]}\frac{d[\text{A}]}{[\text{A}]}
= k\int_{0}^{t} dt \quad\Longrightarrow\quad
\ln\frac{[\text{A}]_0}{[\text{A}]} = kt $$

$$ \boxed{k = \frac{1}{t}\ln\frac{[\text{A}]_0}{[\text{A}]}
= \frac{2.303}{t}\log\frac{[\text{A}]_0}{[\text{A}]}} $$

Two other useful forms follow at once:

$$ \ln[\text{A}] = \ln[\text{A}]_0 - kt, \qquad
[\text{A}] = [\text{A}]_0\,e^{-kt} $$

So $\ln[\text{A}]$ (or $\log[\text{A}]$) against $t$ is a straight line — of slope
$-k$ in the natural-log form and $-k/2.303$ in the base-10 form. A first-order
reaction never truly finishes; the concentration decays exponentially towards zero.
:::

::: tip Whatever is proportional to concentration will do
Because only the *ratio* $[\text{A}]_0/[\text{A}]$ appears, any quantity
proportional to the amount left can be substituted — the volume of KMnO₄ needed to
titrate the residual H₂O₂, the pressure of a gas, the angle of optical rotation, or
the mass of an undecayed radioactive sample. Units cancel in the ratio, so no
conversion to mol L⁻¹ is needed.
:::

```figure caption="Left: concentration against time for a zero-order and a first-order reaction with the same starting concentration. Right: the corresponding linear tests. A zero-order reaction is linear in $[A]$; a first-order reaction is linear in $\ln[A]$, with slope $-k$."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(5.2,2.7))
k0, k1, C0 = 0.020, 0.030, 1.00
t0 = np.linspace(0, 50, 200); t1 = np.linspace(0, 100, 300)
ax = axes[0]
ax.plot(t0, C0 - k0*t0, color=SERIES[2], lw=2.0, label='zero order')
ax.plot(t1, C0*np.exp(-k1*t1), color=ACCENT, lw=2.0, label='first order')
ax.set_xlabel('t  (s)'); ax.set_ylabel('[A]  (mol L⁻¹)')
ax.set_xlim(0, 100); ax.set_ylim(0, 1.08)
ax.legend(loc='upper right', fontsize=7.2)
ax = axes[1]
ax.plot(t1, np.log(C0) - k1*t1, color=ACCENT, lw=2.0)
ax.set_xlabel('t  (s)'); ax.set_ylabel('ln [A]')
ax.set_xlim(0, 100); ax.set_ylim(-3.2, 0.4)
ax.annotate('slope = −k', xy=(60, np.log(C0) - k1*60), xytext=(22, -2.6),
            fontsize=7.8, color=INK,
            arrowprops=dict(arrowstyle='->', color=INK, lw=0.9))
for a in axes:
    a.spines[['top','right']].set_visible(False)
    a.grid(True, alpha=0.35)
fig.tight_layout()
```

::: example Worked example 3.4 — a first-order reaction
**Problem.** A first-order reaction is 25 % complete in 40 minutes. Calculate
(a) the rate constant, (b) the time needed for the reaction to be 75 % complete.

**Solution.**

(a) Take $[\text{A}]_0 = 100$. If 25 % has reacted, $[\text{A}] = 75$.

$$ k = \frac{2.303}{t}\log\frac{[\text{A}]_0}{[\text{A}]}
= \frac{2.303}{40}\log\frac{100}{75} = 0.057575 \times \log 1.3333 $$

$\log 1.3333 = 0.1249$, so $k = 0.057575 \times 0.1249 = 7.19\times10^{-3}\ \text{min}^{-1}$.

(b) For 75 % completion, $[\text{A}] = 25$:

$$ t = \frac{2.303}{k}\log\frac{100}{25}
= \frac{2.303}{7.19\times10^{-3}}\times \log 4
= 320.3 \times 0.6021 = 193\ \text{min} $$

Note the structure of the answer: 75 % completion leaves one quarter, which is two
successive halvings, so $t = 2t_{1/2}$ — and indeed
$t_{1/2} = 0.693/k = 96.4$ min gives $2t_{1/2} = 193$ min. Use this as a check.
:::

::: example Worked example 3.5 — a zero-order reaction
**Problem.** The decomposition of NH₃ on a hot tungsten wire is zero order with
$k = 2.0\times10^{-2}$ mol L⁻¹ s⁻¹. If the initial concentration of NH₃ is
0.50 mol L⁻¹, find (a) the concentration left after 10 s, (b) the time for the
concentration to fall to half its initial value, and (c) the time for the ammonia
to disappear completely.

**Solution.**

(a) $[\text{A}] = [\text{A}]_0 - kt = 0.50 - (2.0\times10^{-2})(10) = 0.50 - 0.20 = 0.30$ mol L⁻¹.

(b) $t_{1/2} = \dfrac{[\text{A}]_0}{2k} = \dfrac{0.50}{2 \times 2.0\times10^{-2}} = \dfrac{0.50}{0.040} = 12.5\ \text{s}$.

(c) Complete reaction means $[\text{A}] = 0$, so
$t = \dfrac{[\text{A}]_0}{k} = \dfrac{0.50}{2.0\times10^{-2}} = 25\ \text{s}$,
which is exactly $2t_{1/2}$. A zero-order reaction, unlike a first-order one, does
come to a definite end.
:::

## 3.7 Half-life of zero and first order reactions

::: definition Half-life
The **half-life** $t_{1/2}$ of a reaction is the time in which the concentration of
a reactant falls to one half of its initial value.
:::

::: derivation Half-life expressions
**Zero order.** Put $[\text{A}] = [\text{A}]_0/2$ in $[\text{A}] = [\text{A}]_0 - kt$:

$$ \frac{[\text{A}]_0}{2} = [\text{A}]_0 - kt_{1/2}
\quad\Longrightarrow\quad
\boxed{t_{1/2} = \frac{[\text{A}]_0}{2k}} $$

The half-life is **directly proportional to the initial concentration**.

**First order.** Put $[\text{A}] = [\text{A}]_0/2$ in
$k = \frac{2.303}{t}\log\frac{[\text{A}]_0}{[\text{A}]}$:

$$ k = \frac{2.303}{t_{1/2}}\log 2 = \frac{2.303 \times 0.3010}{t_{1/2}}
= \frac{0.693}{t_{1/2}} $$

$$ \boxed{t_{1/2} = \frac{0.693}{k} = \frac{\ln 2}{k}} $$

The half-life is **independent of the initial concentration** — the single most
useful fact in this chapter.
:::

Because each half-life removes half of whatever is left, the fraction of reactant
surviving after $n$ half-lives is $(1/2)^{n}$:

| Half-lives elapsed | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| Fraction left | 1 | 1/2 | 1/4 | 1/8 | 1/16 | 1/32 |
| Per cent completed | 0 | 50 | 75 | 87.5 | 93.75 | 96.875 |

::: memory Two shortcuts worth memorising
$t_{99\%} = 6.64\,t_{1/2}$ and $t_{99.9\%} \approx 10\,t_{1/2}$ for a first-order
reaction, because $t = \frac{2.303}{k}\log 100 = \frac{2 \times 2.303}{k}$ and
$\frac{3 \times 2.303}{k}$ respectively, while $t_{1/2} = 0.693/k$.
:::

::: example Worked example 3.6 — half-life arithmetic
**Problem.** The half-life of the first-order decomposition of N₂O₅ at a certain
temperature is 20 minutes. (a) What fraction of the sample remains after one hour?
(b) If 4.0 g of N₂O₅ was taken, what mass has decomposed in one hour?
(c) Calculate the rate constant.

**Solution.**

(a) One hour is 60 min, which is $60/20 = 3$ half-lives, so the fraction left is
$(1/2)^{3} = 1/8 = 0.125$, i.e. **12.5 %**.

(b) Mass left $= 4.0 \times 1/8 = 0.50$ g, so the mass decomposed is
$4.0 - 0.50 = 3.5$ g.

(c) $k = \dfrac{0.693}{t_{1/2}} = \dfrac{0.693}{20} = 3.47\times10^{-2}\ \text{min}^{-1}$ ( $= 5.78\times10^{-4}$ s⁻¹ ).
:::

## 3.8 Collision theory; activation energy and activated complex

Collision theory pictures a reaction as the outcome of collisions between reactant
molecules. Its three statements are:

1. Molecules must **collide** before they can react.
2. Only a small fraction of collisions are **effective**: the colliding molecules
   must carry at least a certain minimum energy.
3. The molecules must also collide with the **correct orientation** of the
   reacting bonds.

For a bimolecular gas reaction the number of collisions per unit volume per second,
the collision frequency $Z$, is enormous — of the order of 10³⁰ L⁻¹ s⁻¹ at room
temperature and ordinary pressures. If every collision worked, all gas reactions
would be over in microseconds. They are not, so

$$ r = Z \times P \times e^{-E_a/RT} $$

where $e^{-E_a/RT}$ is the fraction of collisions with energy at least $E_a$ and
$P$ is the **steric** (orientation) factor, a number between 0 and 1.

::: definition Activation energy and activated complex
The **activation energy** $E_a$ is the minimum extra energy, over and above the
average energy of the reactant molecules, that colliding molecules must possess
for the collision to lead to products. Its unit is kJ mol⁻¹.

The **activated complex** (or transition state) is the short-lived, unstable
arrangement of atoms at the top of the energy barrier, in which the old bonds are
partly broken and the new bonds are partly formed. It cannot be isolated.
:::

For the gas-phase reaction H₂ + I₂ → 2HI the activated complex is a four-centre
arrangement often written [H⋯H⋯I⋯I]‡, in which both the H—H and the I—I bonds are
stretched and two H—I bonds are forming.

::: key Threshold energy and activation energy
$E_{\text{threshold}} = E_{\text{average of reactants}} + E_a$. The threshold
energy is the *absolute* energy a collision must reach; the activation energy is
the *extra* energy needed, measured from the reactant level. A small $E_a$ means a
fast reaction; a large $E_a$ means a slow one.
:::

```figure caption="Maxwell-Boltzmann distribution of molecular energies. Raising the temperature from $T_1$ to $T_2$ flattens and broadens the curve; the shaded tail beyond $E_a$ — the fraction of molecules able to react — grows far more than the temperature does."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.9))
E = np.linspace(0, 60, 700)
def f(E, T):
    y = np.sqrt(E)*np.exp(-E/T)
    return y/np.trapezoid(y, E)
Ea = 22.0
y1, y2 = f(E, 5.0), f(E, 9.0)
ax.plot(E, y1, color=ACCENT, lw=2.0, label='T₁  (lower temperature)')
ax.plot(E, y2, color=SERIES[1], lw=2.0, label='T₂  (higher, T₂ > T₁)')
m = E >= Ea
ax.fill_between(E[m], 0, y2[m], color=SERIES[1], alpha=0.35, lw=0)
ax.fill_between(E[m], 0, y1[m], color=ACCENT, alpha=0.55, lw=0)
ax.axvline(Ea, color=INK, lw=1.1, ls=(0,(4,2)))
ax.text(Ea - 0.9, 0.083, 'Eₐ', fontsize=9.5, color=INK, ha='right')
ax.annotate('molecules with E ≥ Eₐ\n(shaded): these react',
            xy=(27.5, 0.008), xytext=(29, 0.050),
            fontsize=7.6, color=INK,
            arrowprops=dict(arrowstyle='->', color=INK, lw=0.9))
ax.set_xlabel('kinetic energy  E')
ax.set_ylabel('fraction of molecules')
ax.set_xlim(0, 45); ax.set_ylim(0, 0.145)
ax.set_yticks([])
ax.spines[['top','right','left']].set_visible(False)
ax.legend(loc='upper right', fontsize=7.8)
```

## 3.9 Factors affecting rate: concentration, temperature (Arrhenius equation), catalyst (energy profile diagram)

### (a) Nature and physical state of the reactants

Ionic reactions in solution are almost instantaneous because no covalent bond has
to break; reactions that require the breaking of strong bonds are slow. Powdered
CaCO₃ dissolves in dilute HCl far faster than a marble chip of the same mass,
because the surface area exposed is much larger. This is why lump limestone is
crushed before being fed to a lime kiln.

### (b) Concentration (and pressure for gases)

Increasing the concentration increases the number of molecules per unit volume,
hence the collision frequency, hence the rate. Quantitatively the effect is fixed
by the order: for $r = k[\text{A}]^{2}$ doubling [A] quadruples the rate, whereas
for a zero-order reaction it changes nothing. For gaseous reactants, increasing the
pressure has the same effect as increasing the concentration.

### (c) Temperature — the Arrhenius equation

A rise of 10 K near room temperature typically **doubles or trebles** the rate. The
ratio $k_{T+10}/k_{T}$ is called the **temperature coefficient** and usually lies
between 2 and 3. The reason is not the small increase in collision frequency
(collision frequency goes only as $\sqrt{T}$, about 1.6 % for 10 K near 300 K) but
the sharp growth of the high-energy tail of the Maxwell-Boltzmann curve.

::: derivation The Arrhenius equation and its useful two-temperature form
Arrhenius (1889) found that rate constants obey

$$ k = A\,e^{-E_a/RT} $$

where $A$ is the **frequency (pre-exponential) factor**, with the same units as
$k$, $E_a$ the activation energy, $R = 8.314$ J K⁻¹ mol⁻¹ and $T$ the absolute
temperature. Taking natural logarithms,

$$ \ln k = \ln A - \frac{E_a}{RT}, \qquad
\log k = \log A - \frac{E_a}{2.303\,RT} $$

A graph of $\ln k$ against $1/T$ is a straight line of slope $-E_a/R$ and intercept
$\ln A$; this is how $E_a$ is measured.

Writing the equation at two temperatures and subtracting,

$$ \log k_2 - \log k_1 = -\frac{E_a}{2.303R}\left(\frac{1}{T_2}-\frac{1}{T_1}\right) $$

$$ \boxed{\log\frac{k_2}{k_1}
= \frac{E_a}{2.303\,R}\left(\frac{T_2 - T_1}{T_1T_2}\right)} $$
:::

```figure caption="Arrhenius plot for the gas-phase decomposition of HI. The points are experimental rate constants; the slope of the line is $-E_a/R$, giving $E_a \approx 104$ kJ mol$^{-1}$, and the intercept at $1/T = 0$ gives $\ln A$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9,2.9))
R = 8.314; Ea = 104000.0; A = 4.0e13
T = np.array([700.0, 730.0, 760.0, 790.0, 820.0])
invT = 1.0/T
lnk = np.log(A) - Ea/(R*T)
xl = np.linspace(1.18e-3, 1.47e-3, 50)
ax.plot(xl*1e3, np.log(A) - Ea/(R)*xl, color=ACCENT, lw=1.6)
ax.plot(invT*1e3, lnk, 'o', color=SERIES[1], ms=5.5, zorder=5)
ax.plot([invT[0]*1e3, invT[3]*1e3], [lnk[3], lnk[3]], color=MUTED, lw=0.9, ls=':')
ax.plot([invT[0]*1e3, invT[0]*1e3], [lnk[3], lnk[0]], color=MUTED, lw=0.9, ls=':')
ax.text(1.347, 15.56, 'Δ(1/T)', fontsize=7.4, color=MUTED, ha='center')
ax.text(1.421, 14.45, 'Δ ln k', fontsize=7.4, color=MUTED, ha='center', rotation=90)
ax.text(1.245, 14.05, 'slope = −Eₐ/R\n= −1.25 × 10⁴ K', fontsize=8.0, color=INK)
ax.set_xlabel('10³ / T   (K⁻¹)')
ax.set_ylabel('ln k')
ax.set_xlim(1.18, 1.47); ax.set_ylim(13.0, 16.6)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=0.35)
```

::: example Worked example 3.7 — activation energy from a doubling of rate
**Problem.** The rate constant of a reaction doubles when the temperature is raised
from 300 K to 310 K. Calculate the activation energy.
($R = 8.314$ J K⁻¹ mol⁻¹, $\log 2 = 0.3010$.)

**Solution.**

$$ \log\frac{k_2}{k_1}
= \frac{E_a}{2.303R}\left(\frac{T_2-T_1}{T_1T_2}\right) $$

with $k_2/k_1 = 2$, $T_1 = 300$ K, $T_2 = 310$ K:

$$ 0.3010 = \frac{E_a}{2.303 \times 8.314}
\times \frac{10}{300 \times 310}
= \frac{E_a \times 10}{19.147 \times 93000} $$

$$ E_a = \frac{0.3010 \times 19.147 \times 93000}{10}
= \frac{0.3010 \times 1{,}780{,}671}{10} = 53{,}604\ \text{J mol}^{-1} $$

$$ E_a \approx 53.6\ \text{kJ mol}^{-1} $$

This is the classic result: an activation energy of about 50 kJ mol⁻¹ is what makes
a reaction roughly twice as fast for every 10 K near room temperature.
:::

::: example Worked example 3.8 — $E_a$ and $A$ from two rate constants
**Problem.** For a first-order reaction $k = 2.0\times10^{-5}$ s⁻¹ at 300 K and
$8.0\times10^{-5}$ s⁻¹ at 320 K. Calculate the activation energy and the
frequency factor. ($\log 4 = 0.6021$.)

**Solution.**

$$ \log\frac{8.0\times10^{-5}}{2.0\times10^{-5}} = \log 4 = 0.6021 $$

$$ 0.6021 = \frac{E_a}{2.303 \times 8.314}\times\frac{320-300}{300 \times 320}
= \frac{E_a \times 20}{19.147 \times 96000} $$

$$ E_a = \frac{0.6021 \times 19.147 \times 96000}{20}
= \frac{0.6021 \times 1{,}838{,}112}{20} = 55{,}336\ \text{J mol}^{-1}
\approx 55.3\ \text{kJ mol}^{-1} $$

For the frequency factor, use $\log k = \log A - \dfrac{E_a}{2.303RT}$ at 300 K:

$$ \frac{E_a}{2.303RT} = \frac{55{,}336}{19.147 \times 300}
= \frac{55{,}336}{5744} = 9.633 $$

$$ \log A = \log(2.0\times10^{-5}) + 9.633 = (-4.699) + 9.633 = 4.934 $$

$$ A = 10^{4.934} = 8.6\times10^{4}\ \text{s}^{-1} $$

$A$ carries the units of $k$, here s⁻¹, because the exponential term is
dimensionless.
:::

### (d) Catalyst — the energy profile diagram

A **catalyst** is a substance that alters the rate of a reaction without being
consumed, and provides an alternative path of **lower activation energy**. It does
this by forming an unstable intermediate with a reactant; when that intermediate
breaks down to give the product, the catalyst is regenerated.

Three consequences must be stated carefully, because the board asks about them.

- A catalyst lowers $E_a$ for the forward **and** the backward reaction **by the
  same amount**, so it speeds both up equally and **does not shift the position of
  equilibrium** — only the time taken to reach it.
- It does **not** change $\Delta H$, because $\Delta H$ depends only on the energies
  of the reactants and products, not on the path between them.
- It cannot make a thermodynamically impossible reaction happen.

```figure caption="Potential-energy profile for an exothermic reaction. The catalysed path (dashed) has a lower barrier $E_a'$ and therefore a much larger fraction of successful collisions, but the reactant and product levels — and hence $\Delta H$ — are unchanged."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.1,3.2))
x = np.linspace(0, 10, 600)
dH = -30.0
def prof(top):
    return dH/(1 + np.exp(-(x - 5.0)*1.6)) + top*np.exp(-((x - 5.0)**2)/1.9)
y1, y2 = prof(115.0), prof(70.0)
i1, i2 = int(np.argmax(y1)), int(np.argmax(y2))
p1, p2 = y1[i1], y2[i2]
ax.plot(x, y1, color=ACCENT, lw=2.1, label='uncatalysed')
ax.plot(x, y2, color=SERIES[1], lw=1.9, ls=(0,(5,2)), label='catalysed')
ax.axhline(0, color=MUTED, lw=0.8, ls=':')
ax.axhline(dH, color=MUTED, lw=0.8, ls=':')
ax.plot([3.55, x[i1]], [p1, p1], color=ACCENT, lw=0.8, ls=':')
ax.plot([x[i2], 6.55], [p2, p2], color=SERIES[1], lw=0.8, ls=':')
ax.annotate('', xy=(3.55, 0), xytext=(3.55, p1),
            arrowprops=dict(arrowstyle='<->', color=ACCENT, lw=1.0))
ax.text(3.40, p1/2, 'Eₐ', fontsize=10, color=ACCENT, ha='right', va='center')
ax.annotate('', xy=(6.55, 0), xytext=(6.55, p2),
            arrowprops=dict(arrowstyle='<->', color=SERIES[1], lw=1.0))
ax.text(6.72, p2/2, "Eₐ′", fontsize=10, color=SERIES[1], ha='left', va='center')
ax.annotate('', xy=(9.25, 0), xytext=(9.25, dH),
            arrowprops=dict(arrowstyle='<->', color=INK, lw=1.0))
ax.text(9.10, dH/2, 'ΔH', fontsize=9, color=INK, ha='right', va='center')
ax.plot([x[i1]], [p1], 'o', color=ACCENT, ms=5)
ax.text(x[i1], p1 + 7, 'activated complex', fontsize=7.8, color=INK, ha='center')
ax.text(0.30, 6, 'reactants', fontsize=8.2, color=INK)
ax.text(7.6, -42, 'products', fontsize=8.2, color=INK, ha='center')
ax.set_xlabel('reaction coordinate  (progress of reaction) →')
ax.set_ylabel('potential energy  (kJ mol⁻¹)')
ax.set_xlim(0, 10); ax.set_ylim(-52, 128)
ax.set_xticks([])
ax.spines[['top','right','bottom']].set_visible(False)
ax.legend(loc='upper left', fontsize=7.8)
```

### (e) Other factors

**Surface area** of a solid catalyst or reactant, **intensity of light** for
photochemical reactions such as H₂ + Cl₂ → 2HCl and photosynthesis, and the
**nature of the solvent** all affect the rate.

## 3.10 Catalysis and types: homogeneous, heterogeneous and enzyme catalysis

**Catalysis** is the process by which the rate of a reaction is changed by a
catalyst. A **positive catalyst** speeds the reaction up; a **negative catalyst**
(inhibitor) slows it down, as glycerol does for the decomposition of H₂O₂.

Two supporting terms:

- A **promoter** (activator) is a substance that has no catalytic power of its own
  but increases the activity of a catalyst — Mo with Fe in the Haber process.
- A **catalytic poison** destroys the activity of a catalyst — As₂O₃ poisons the
  V₂O₅ of the contact process, so the SO₂ must be purified first.

### (a) Homogeneous catalysis

The catalyst and the reactants are in the **same phase**.

| Reaction | Catalyst | Phase |
|---|---|---|
| 2SO₂ + O₂ → 2SO₃ (lead-chamber process) | NO(g) | all gases |
| CH₃COOC₂H₅ + H₂O → CH₃COOH + C₂H₅OH | H⁺(aq) from dilute HCl | all in solution |
| C₁₂H₂₂O₁₁ + H₂O → 2C₆H₁₂O₆ | H⁺(aq) | all in solution |
| 2H₂O₂ → 2H₂O + O₂ | I⁻(aq) | all in solution |

In the lead-chamber process the mechanism is easy to see: 2NO + O₂ → 2NO₂, then
NO₂ + SO₂ → SO₃ + NO. The NO is used in the first step and returned in the second,
so it does not appear in the overall equation.

### (b) Heterogeneous catalysis

The catalyst is in a **different phase** from the reactants — almost always a solid
catalysing gases or liquids. Reaction occurs on the surface: the reactants are
adsorbed on active centres, which weakens their bonds and holds them in a
favourable orientation; the product then desorbs.

| Reaction | Catalyst | Process |
|---|---|---|
| N₂ + 3H₂ ⇌ 2NH₃ | finely divided Fe with Mo promoter | Haber process |
| 2SO₂ + O₂ ⇌ 2SO₃ | V₂O₅ (solid) | contact process |
| 4NH₃ + 5O₂ → 4NO + 6H₂O | Pt gauze | Ostwald process |
| vegetable oil + H₂ → vanaspati ghee | Ni (solid) | oil hydrogenation |
| 2KClO₃ → 2KCl + 3O₂ | MnO₂ (solid) | laboratory oxygen |

The hydrogenation of mustard or soyabean oil over nickel to make the solid
vanaspati ghee sold in Nepali shops is the most familiar industrial example of
heterogeneous catalysis in the country.

### (c) Enzyme catalysis

**Enzymes** are protein molecules produced by living cells that catalyse
biochemical reactions; they are also called **biocatalysts**. A colloidal enzyme
molecule has a cavity of a definite shape — the **active site** — into which only a
substrate of matching shape fits, the "lock-and-key" picture.

| Enzyme | Reaction catalysed | Source |
|---|---|---|
| Invertase | sucrose → glucose + fructose | yeast |
| Zymase | C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂ | yeast |
| Diastase (amylase) | starch → maltose | malt, saliva |
| Maltase | maltose → glucose | yeast |
| Urease | CO(NH₂)₂ + H₂O → 2NH₃ + CO₂ | soyabean |
| Pepsin | proteins → peptides | gastric juice |

Characteristics of enzyme catalysis: extremely high efficiency (one molecule can
transform millions of substrate molecules per minute), very high **specificity**
(urease attacks urea and nothing else), activity confined to a narrow optimum
temperature (typically 298–310 K, because higher temperatures denature the protein)
and a narrow optimum pH (usually 5–7), and sensitivity to inhibitors and
activators. The fermentation of rice in making *jaand* and *raksi* runs on the
enzymes of yeast, and the souring of milk into *dahi* on those of *Lactobacillus*.

::: caution Autocatalysis
In the permanganate-oxalic acid titration of Unit 1, the first few drops of KMnO₄
decolourise slowly and the rest almost instantly. The Mn²⁺ produced by the reaction
catalyses the reaction itself — **autocatalysis**. It is why that titration is
carried out warm, at about 60 °C, to get the first drops going.
:::

## Chapter summary

- Kinetics deals with rates, the factors affecting them and mechanism. Average rate
  is the slope of a chord, instantaneous rate the slope of the tangent, on a
  concentration-time graph; the unit is mol L⁻¹ s⁻¹.
- For $a$A + $b$B → $c$C + $d$D the rate of reaction is
  $-\frac{1}{a}\frac{d[\text{A}]}{dt} = \frac{1}{c}\frac{d[\text{C}]}{dt}$: always
  divide by the stoichiometric coefficient.
- The rate law $r = k[\text{A}]^{x}[\text{B}]^{y}$ is **experimental**; its powers
  need not match the coefficients in the balanced equation.
- $k$ is the specific reaction rate, has units
  $(\text{mol L}^{-1})^{1-n}\text{s}^{-1}$, is independent of concentration and
  increases with temperature.
- Order is experimental and may be zero or fractional; molecularity is theoretical
  and is a small whole number. They are equal only for elementary reactions.
  Reactions like ester hydrolysis are pseudo-first-order because the solvent is in
  excess.
- Zero order: $[\text{A}] = [\text{A}]_0 - kt$ and $t_{1/2} = [\text{A}]_0/2k$;
  the plot of $[\text{A}]$ against $t$ is linear.
- First order: $k = \frac{2.303}{t}\log\frac{[\text{A}]_0}{[\text{A}]}$ and
  $t_{1/2} = 0.693/k$, independent of the initial concentration; the plot of
  $\ln[\text{A}]$ against $t$ is linear with slope $-k$.
- Collision theory: $r = ZPe^{-E_a/RT}$. Only collisions with energy at least
  $E_a$ and the right orientation succeed; the activated complex sits at the top of
  the barrier.
- Arrhenius: $k = Ae^{-E_a/RT}$, so $\ln k$ against $1/T$ is linear with slope
  $-E_a/R$, and
  $\log\frac{k_2}{k_1} = \frac{E_a}{2.303R}\left(\frac{T_2-T_1}{T_1T_2}\right)$.
- A catalyst provides a path of lower $E_a$, lowers the barrier equally in both
  directions, and changes neither $\Delta H$ nor the equilibrium position.
  Catalysis is homogeneous (NO in the lead-chamber process), heterogeneous (Fe in
  the Haber process) or enzymatic (zymase in fermentation).

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The unit of the rate constant of a zero-order reaction is <span class="marks">[1]</span>
   (a) s⁻¹ (b) mol L⁻¹ s⁻¹ (c) L mol⁻¹ s⁻¹ (d) L² mol⁻² s⁻¹
2. For a first-order reaction the half-life is <span class="marks">[1]</span>
   (a) proportional to $[\text{A}]_0$ (b) inversely proportional to $[\text{A}]_0$
   (c) independent of $[\text{A}]_0$ (d) proportional to $[\text{A}]_0^{2}$
3. The observed rate law for 2N₂O₅ → 4NO₂ + O₂ is $r = k[\text{N}_2\text{O}_5]$.
   The overall order is <span class="marks">[1]</span>
   (a) 0 (b) 1 (c) 2 (d) 3
4. Which of the following quantities can **never** be fractional? <span class="marks">[1]</span>
   (a) order (b) molecularity (c) rate (d) rate constant
5. A catalyst increases the rate of a reaction because it <span class="marks">[1]</span>
   (a) increases the number of collisions (b) lowers the activation energy
   (c) makes $\Delta H$ more negative (d) shifts the equilibrium to the right
6. The hydrolysis of ethyl acetate in a large excess of water is <span class="marks">[1]</span>
   (a) zero order (b) pseudo-first order (c) second order (d) third order
7. If trebling the concentration of the single reactant makes the rate nine times
   larger, the order of the reaction is <span class="marks">[1]</span>
   (a) 1 (b) 2 (c) 3 (d) 1/2
8. In a plot of $\ln k$ against $1/T$ the slope is equal to <span class="marks">[1]</span>
   (a) $-E_a/R$ (b) $+E_a/R$ (c) $-E_a/2.303R$ (d) $\ln A$

::: note Answers to Group A
**1.** (b) — $k$ has units $(\text{mol L}^{-1})^{1-n}\text{s}^{-1}$; for $n = 0$ this is mol L⁻¹ s⁻¹.
**2.** (c) — $t_{1/2} = 0.693/k$ contains no concentration term.
**3.** (b) — the order is the power in the *experimental* rate law, not the coefficient.
**4.** (b) — molecularity counts whole molecules in one step, so it is 1, 2 or 3.
**5.** (b) — it offers an alternative path over a lower barrier; $\Delta H$ and $K$ are unaffected.
**6.** (b) — truly bimolecular, but $[\text{H}_2\text{O}]$ is constant, so it behaves as first order.
**7.** (b) — $3^{x} = 9$ gives $x = 2$.
**8.** (a) — from $\ln k = \ln A - E_a/RT$.
:::

**Group B — Short answer (5 marks each)**

1. Distinguish between the average rate and the instantaneous rate of a reaction.
   For 4NH₃ + 5O₂ → 4NO + 6H₂O, write the rate of reaction in terms of each
   species. If O₂ is consumed at $2.5\times10^{-3}$ mol L⁻¹ s⁻¹, at what rate is NO
   formed? <span class="marks">[5]</span>
2. A first-order reaction has a rate constant of $1.15\times10^{-3}$ s⁻¹. How long
   will 5.0 g of the reactant take to be reduced to 3.0 g? <span class="marks">[5]</span>
3. The half-life of a first-order reaction is 10 minutes. Calculate the rate
   constant and the time required for the reaction to be 90 % complete. <span class="marks">[5]</span>
4. For a zero-order reaction $k = 1.0\times10^{-2}$ mol L⁻¹ s⁻¹ and
   $[\text{A}]_0 = 0.40$ mol L⁻¹. Find the half-life and the time at which
   $[\text{A}] = 0.10$ mol L⁻¹. <span class="marks">[5]</span>
5. The rate constant of a reaction at 300 K is $4.5\times10^{-3}$ s⁻¹ and its
   activation energy is 60 kJ mol⁻¹. Calculate the rate constant at 320 K. <span class="marks">[5]</span>
6. Define catalysis. Distinguish between homogeneous and heterogeneous catalysis
   with one example of each, and state three characteristics of enzyme
   catalysis. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** The average rate is the concentration change divided by a finite time
interval — the slope of the chord; the instantaneous rate is the limit of that as
the interval tends to zero — the slope of the tangent. For the given reaction,

$$ r = -\frac{1}{4}\frac{d[\text{NH}_3]}{dt} = -\frac{1}{5}\frac{d[\text{O}_2]}{dt}
= +\frac{1}{4}\frac{d[\text{NO}]}{dt} = +\frac{1}{6}\frac{d[\text{H}_2\text{O}]}{dt} $$

So $r = \frac{1}{5}(2.5\times10^{-3}) = 5.0\times10^{-4}$ mol L⁻¹ s⁻¹ and
$\frac{d[\text{NO}]}{dt} = 4r = 2.0\times10^{-3}$ mol L⁻¹ s⁻¹.

**2.** Mass is proportional to concentration, so the ratio 5.0/3.0 may be used
directly:
$t = \frac{2.303}{1.15\times10^{-3}}\log\frac{5.0}{3.0} = 2002.6 \times 0.2218 = 444\ \text{s}$ (7 min 24 s).

**3.** $k = 0.693/10 = 6.93\times10^{-2}$ min⁻¹. For 90 % completion 10 % remains,
so $t = \frac{2.303}{6.93\times10^{-2}}\log 10 = 33.24 \times 1 = 33.2$ min.

**4.** $t_{1/2} = \frac{[\text{A}]_0}{2k} = \frac{0.40}{0.020} = 20\ \text{s}$. From
$[\text{A}] = [\text{A}]_0 - kt$,
$t = \frac{0.40-0.10}{1.0\times10^{-2}} = 30\ \text{s}$.

**5.** $\log\frac{k_2}{k_1} = \frac{60000}{2.303\times8.314} \times\frac{20}{300\times320} = 3133.1 \times 2.0833\times10^{-4} = 0.6528$, so
$k_2/k_1 = 4.50$ and
$k_2 = 4.50 \times 4.5\times10^{-3} = 2.02\times10^{-2}$ s⁻¹.

**6.** Catalysis is the change in the rate of a reaction brought about by a
substance (the catalyst) that is not consumed. In **homogeneous** catalysis the
catalyst is in the same phase as the reactants — NO(g) in
2SO₂ + O₂ → 2SO₃ in the lead-chamber process. In **heterogeneous** catalysis it is
in a different phase — solid Fe for N₂ + 3H₂ ⇌ 2NH₃ in the Haber process, where
reaction occurs on the adsorbing surface. Enzyme catalysis is (i) extremely
efficient, one molecule turning over millions of substrate molecules per minute,
(ii) highly specific, one enzyme for one substrate (urease acts only on urea), and
(iii) restricted to a narrow optimum temperature (about 298–310 K) and pH, because
the protein is denatured outside it.
:::

**Group C — Long answer (8 marks each)**

1. (a) Derive the integrated rate equation for a first-order reaction and show
   that its half-life is independent of the initial concentration. <span class="marks">[5]</span>
   (b) A first-order reaction is found to be 30 % decomposed in 40 minutes.
   Calculate its rate constant and half-life. <span class="marks">[3]</span>
2. (a) Distinguish between the order and the molecularity of a reaction, with one
   example of each of a zero-order and a fractional-order reaction. Explain what is
   meant by a pseudo-first-order reaction. <span class="marks">[4]</span>
   (b) The rate constant of a reaction is $2.0\times10^{-4}$ s⁻¹ at 500 K and
   $4.0\times10^{-3}$ s⁻¹ at 600 K. Calculate the activation energy. <span class="marks">[4]</span>
3. (a) State the postulates of collision theory. Define activation energy and
   activated complex, and use the Maxwell-Boltzmann distribution to explain why a
   10 K rise in temperature can double the rate. <span class="marks">[4]</span>
   (b) Draw the potential-energy profile for an exothermic reaction with and
   without a catalyst. If a catalyst lowers the activation energy from
   75 kJ mol⁻¹ to 50 kJ mol⁻¹, by what factor does the rate increase at
   300 K? <span class="marks">[4]</span>

::: note Answers to Group C
**1.(a)** See the derivation box in §3.6: from $-d[\text{A}]/dt = k[\text{A}]$,
separating variables and integrating gives
$k = \frac{2.303}{t}\log\frac{[\text{A}]_0}{[\text{A}]}$. Putting
$[\text{A}] = [\text{A}]_0/2$ makes the logarithm $\log 2 = 0.3010$, so
$t_{1/2} = 2.303 \times 0.3010/k = 0.693/k$. The initial concentration has
cancelled, so $t_{1/2}$ does not depend on it.

**1.(b)** 30 % decomposed leaves 70 %:

$$ k = \frac{2.303}{40}\log\frac{100}{70} = 0.057575 \times 0.1549
= 8.92\times10^{-3}\ \text{min}^{-1} $$

$$ t_{1/2} = \frac{0.693}{8.92\times10^{-3}} = 77.7\ \text{min} $$

**2.(a)** Order is the sum of the powers of the concentration terms in the
experimental rate law; it is found by experiment and may be 0, fractional or a
whole number. Molecularity is the number of species colliding in one elementary
step; it is deduced from the equation for that step and must be 1, 2 or 3.
Zero order: 2NH₃ → N₂ + 3H₂ on a hot tungsten surface, $r = k$. Fractional order:
CHCl₃ + Cl₂ → CCl₄ + HCl, $r = k[\text{CHCl}_3][\text{Cl}_2]^{1/2}$, order 1.5. A
pseudo-first-order reaction is one whose true order is higher but which behaves as
first order because one reactant — usually the solvent — is in such large excess
that its concentration is effectively constant, as in
CH₃COOC₂H₅ + H₂O → CH₃COOH + C₂H₅OH.

**2.(b)** $\log\frac{4.0\times10^{-3}}{2.0\times10^{-4}} = \log 20 = 1.3010$.

$$ 1.3010 = \frac{E_a}{2.303\times8.314}\times\frac{600-500}{500\times600}
= \frac{E_a \times 100}{19.147 \times 300000} $$

$$ E_a = \frac{1.3010 \times 19.147 \times 300000}{100}
= 74{,}733\ \text{J mol}^{-1} \approx 74.7\ \text{kJ mol}^{-1} $$

**3.(a)** Postulates: molecules must collide; only collisions carrying at least the
activation energy are effective; the colliding molecules must also be correctly
oriented, which is allowed for by the steric factor $P$ in $r = ZPe^{-E_a/RT}$.
Activation energy is the minimum extra energy above the average that colliding
molecules must have to react; the activated complex is the unstable
partly-bonded arrangement at the top of the barrier. On the Maxwell-Boltzmann
curve, raising the temperature by 10 K raises the collision frequency by less than
2 %, but the area of the tail beyond $E_a$ — the fraction of molecules with enough
energy — roughly doubles, because that fraction is $e^{-E_a/RT}$ and the exponent
is large. It is this exponential factor, not the collision frequency, that doubles
the rate.

**3.(b)** The diagram is the one in §3.9(d): the same reactant and product levels,
the same $\Delta H$, but a lower peak for the catalysed path. The rates are in the
ratio of the exponential factors:

$$ \frac{r_{\text{cat}}}{r_{\text{uncat}}}
= \frac{e^{-E_a'/RT}}{e^{-E_a/RT}} = e^{(E_a - E_a')/RT}
= e^{25000/(8.314 \times 300)} $$

$$ = e^{10.02} = 2.25\times10^{4} $$

The catalysed reaction is about twenty-two thousand times faster, even though
$\Delta H$ and the equilibrium constant are unchanged.
:::
