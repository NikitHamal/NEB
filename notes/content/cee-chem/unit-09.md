---
subject: Chemistry
grade: CEE
unit: 9
title: Chemical Kinetics
hours: 1
area: Physical Chemistry
---

Stoichiometry tells you what a reaction produces; kinetics tells you how fast it gets
there. The paper carries about **one question** from this chapter (our estimate from the
MEC topic list), and it is nearly always one of three things: a definition that turns on
the difference between order and molecularity, a one-line calculation with $t_{1/2}$ or
the integrated rate law, or a statement about catalysts and collision theory that is
true except for one wrong word. Almost every mark here is lost to a sign, a unit or a
half-life taken as proportional to concentration.

::: key What the paper asks from this chapter
- Rate of reaction is a **positive** quantity: for a reactant, rate $= -\frac{1}{a}\frac{d[A]}{dt}$; average rate uses a finite interval, instantaneous rate the tangent.
- Rate law is **experimental**; order $= m+n$ can be zero, fractional or negative. Molecularity is theoretical and always a whole number.
- Units of $k$: order 0 → mol L⁻¹ s⁻¹; order 1 → s⁻¹; order 2 → L mol⁻¹ s⁻¹; order $n$ → mol$^{1-n}$ L$^{n-1}$ s⁻¹.
- Zero order: $[A] = [A]_0 - kt$, $t_{1/2} = [A]_0/2k$. First order: $\ln([A]_0/[A]) = kt$, $t_{1/2} = 0.693/k$ — **independent of $[A]_0$**.
- A straight line of $\ln[A]$ against $t$ proves first order; its slope is $-k$.
- Collision theory: only collisions with energy ≥ threshold energy **and** the right orientation react; the activated complex sits at the top of the barrier.
- Arrhenius: $k = Ae^{-E_a/RT}$; a 10 °C rise roughly doubles the rate because the fraction of molecules above $E_a$ roughly doubles.
- A catalyst lowers $E_a$ for both directions equally: it changes the **rate**, never $\Delta H$, $\Delta G$ or $K$.
:::

## 9.1 Rate of reaction, rate expressions, the rate constant and its units; order and molecularity

### Rate of reaction: average and instantaneous

::: definition Rate of reaction
The **rate of reaction** is the change in concentration of a reactant or product per
unit time. Because concentrations are measured in mol L⁻¹ and time in seconds, the unit
is **mol L⁻¹ s⁻¹** (also written mol dm⁻³ s⁻¹ or M s⁻¹).
:::

For a reactant the concentration **falls**, so $\Delta[R]$ is negative. Rate must be
positive, hence the minus sign:

$$ \text{rate} = -\frac{\Delta[\text{R}]}{\Delta t} $$

For a product the concentration rises and no sign is needed. For the general equation
$aA + bB \rightarrow cC + dD$ all four species must give the **same** number for the
rate, so each is divided by its own coefficient:

$$ \text{rate} = -\frac{1}{a}\frac{d[A]}{dt} = -\frac{1}{b}\frac{d[B]}{dt} = \frac{1}{c}\frac{d[C]}{dt} = \frac{1}{d}\frac{d[D]}{dt} $$

| Reaction | Rate expression |
|---|---|
| 2N₂O₅ → 4NO₂ + O₂ | $-\frac{1}{2}\frac{d[\text{N}_2\text{O}_5]}{dt} = \frac{1}{4}\frac{d[\text{NO}_2]}{dt} = \frac{d[\text{O}_2]}{dt}$ |
| H₂ + I₂ → 2HI | $-\frac{d[\text{H}_2]}{dt} = \frac{1}{2}\frac{d[\text{HI}]}{dt}$ |
| 2HI → H₂ + I₂ | $-\frac{1}{2}\frac{d[\text{HI}]}{dt} = \frac{d[\text{H}_2]}{dt}$ |
| N₂ + 3H₂ → 2NH₃ | $-\frac{d[\text{N}_2]}{dt} = -\frac{1}{3}\frac{d[\text{H}_2]}{dt} = \frac{1}{2}\frac{d[\text{NH}_3]}{dt}$ |

**Average rate** is measured over a finite interval, $\Delta[R]/\Delta t$, and is read
from the slope of the chord joining two points on the concentration–time curve.
**Instantaneous rate** is the limit as $\Delta t \rightarrow 0$ and is the slope of the
**tangent** at that instant. Because the reactant is consumed fastest at the start, the
average rate over the first interval is always larger than the instantaneous rate at
the end of it.

::: caution Two mistakes that cost marks every year
- **The sign.** "Rate of disappearance of N₂O₅" is a positive number; "rate of change of
  [N₂O₅]" is negative. If an option is negative and the stem says "rate of
  disappearance", it is wrong.
- **The coefficient.** For 2N₂O₅ → 4NO₂ + O₂ the rate of formation of NO₂ is **four
  times** the rate of reaction, and the rate of disappearance of N₂O₅ is **twice** it.
  Do not report $d[\text{NO}_2]/dt$ as "the rate".
:::

::: example Rate from one measured species
**Problem.** In the decomposition 2N₂O₅ → 4NO₂ + O₂ the concentration of O₂ rises at
$2.0 \times 10^{-3}$ mol L⁻¹ s⁻¹. Find the rate of reaction and the rate of
disappearance of N₂O₅.

**Solution.** O₂ has coefficient 1, so it reports the rate directly:
rate $= d[\text{O}_2]/dt = \mathbf{2.0 \times 10^{-3}}$ mol L⁻¹ s⁻¹.
N₂O₅ has coefficient 2 and is consumed, so
$-d[\text{N}_2\text{O}_5]/dt = 2 \times \text{rate} = \mathbf{4.0 \times 10^{-3}}$ mol L⁻¹ s⁻¹.
:::

### Rate law and the rate constant

::: definition Rate law and rate constant
The **rate law** (rate expression) is an equation that relates the rate of a reaction
to the concentrations of the reactants, with the exponents found **by experiment**:
$\text{rate} = k[A]^m[B]^n$. The constant $k$ is the **rate constant** (specific reaction
rate): the rate when every concentration in the law is 1 mol L⁻¹.
:::

$k$ does **not** change as the reaction proceeds, and it does not depend on the
concentrations. It does depend on temperature, on the presence of a catalyst, and on the
nature of the reactants and the solvent.

The units of $k$ are whatever makes rate $= k \times$ (concentration)$^n$ come out in
mol L⁻¹ s⁻¹. For overall order $n$:

$$ \text{unit of } k = \text{mol}^{1-n}\,\text{L}^{n-1}\,\text{s}^{-1} $$

| Overall order | Rate law | Unit of $k$ |
|---|---|---|
| 0 | rate $= k$ | mol L⁻¹ s⁻¹ |
| 1 | rate $= k[A]$ | s⁻¹ |
| 2 | rate $= k[A]^2$ or $k[A][B]$ | L mol⁻¹ s⁻¹ |
| 3 | rate $= k[A]^2[B]$ | L² mol⁻² s⁻¹ |
| $n$ | rate $= k[A]^n$ | mol$^{1-n}$ L$^{n-1}$ s⁻¹ |

::: memory Getting the unit of $k$ without memorising five rows
Take the rate law, put the unit mol L⁻¹ s⁻¹ on the left and the concentration units on
the right, and solve. For rate $= k[A]^2$:
mol L⁻¹ s⁻¹ = (unit of $k$) × (mol L⁻¹)², so unit of $k$ = L mol⁻¹ s⁻¹.
For a first-order reaction the same trick gives s⁻¹, which is why a first-order $k$ is
sometimes called the **frequency** of reaction.
:::

### Order and molecularity — the pair examiners love to confuse

::: definition Order and molecularity
The **order** of a reaction with respect to a reactant is the power to which its
concentration is raised in the experimentally determined rate law; the **overall order**
is the sum of these powers. The **molecularity** of a reaction is the number of
molecules (atoms or ions) that collide in a single elementary step to bring about the
reaction.
:::

| | Order | Molecularity |
|---|---|---|
| How obtained | experiment (rate law) | from the mechanism (theory) |
| Value | 0, 1, 2, 3, or a fraction; can be negative | always a positive whole number, 1, 2 or 3 |
| Applies to | the reaction as a whole | one elementary step only |
| Depends on concentration | no | no |
| Can change with conditions | yes — a reaction can change order as concentration changes | no |
| Relation | order = molecularity **only** for a single-step reaction | |

**Where they differ — learn these three.**

| Reaction | Molecularity | Experimental order | Why |
|---|---|---|---|
| H₂ + Cl₂ → 2HCl | 2 | 1.5, rate $= k[\text{H}_2][\text{Cl}_2]^{1/2}$ | chain mechanism; the Cl₂ step is not the only slow one |
| 2NH₃ → N₂ + 3H₂ on hot tungsten | 2 | 0 | the surface is saturated, so pressure no longer matters |
| C₁₂H₂₂O₁₁ + H₂O → C₆H₁₂O₆ + C₆H₁₂O₆ | 2 | 1 (pseudo-first-order) | water is in such large excess that its concentration hardly changes |

::: caution Order is NOT read off the balanced equation
A balanced equation is a book-keeping statement about atoms, not a description of the
slow step. The decomposition 2N₂O₅ → 4NO₂ + O₂ is **first order**, not second; the
oxidation 2NO + O₂ → 2NO₂ is third order; and H₂ + Cl₂ → 2HCl is of order **1.5**.
Any option that says "the order is the sum of the coefficients in the balanced
equation" is wrong, and it is the most popular distractor in this chapter.
:::

### Finding the order from initial rates

Hold all concentrations but one constant and see how the rate responds.

| Experiment | [A] (M) | [B] (M) | Initial rate (mol L⁻¹ s⁻¹) |
|---|---|---|---|
| 1 | 0.10 | 0.10 | $2.0 \times 10^{-3}$ |
| 2 | 0.20 | 0.10 | $4.0 \times 10^{-3}$ |
| 3 | 0.10 | 0.20 | $8.0 \times 10^{-3}$ |

Experiments 1 → 2: [A] doubles, rate doubles, so the order in A is 1.
Experiments 1 → 3: [B] doubles, rate becomes four times larger, so the order in B is 2.
Overall order $= 1 + 2 = 3$, rate $= k[A][B]^2$.

::: example Order, rate law and rate constant from a table
**Problem.** Use the table above. Find the rate law, the overall order and $k$.

**Solution.** Order in A: $\frac{4.0}{2.0} = 2 = 2^m$, so $m = 1$. Order in B:
$\frac{8.0}{2.0} = 4 = 2^n$, so $n = 2$. Rate $= k[A][B]^2$, overall order 3.
From experiment 1:
$k = \frac{2.0 \times 10^{-3}}{(0.10)(0.10)^2} = \frac{2.0 \times 10^{-3}}{1.0 \times 10^{-3}} = \mathbf{2.0}$ L² mol⁻² s⁻¹.
The unit follows the overall order 3: mol$^{1-3}$ L$^{3-1}$ s⁻¹ = L² mol⁻² s⁻¹.
:::

::: tip Two-second check on any order question
Ask: "can this number be a molecularity?" If an option offers a fractional or zero
order as a **molecularity**, eliminate it at once. If it offers "order = molecularity"
as a general rule, eliminate it too — that is true only for a one-step reaction.
:::

## 9.2 Integrated rate laws and half-lives of zero- and first-order reactions

A rate law is a differential equation. Integrating it gives concentration as a function
of time, which is what a question actually asks for.

### Zero order

Here the rate does not depend on concentration at all, which happens when a surface or
a catalyst is saturated, or in some photochemical reactions.

$$ \text{rate} = -\frac{d[A]}{dt} = k[A]^0 = k $$

Separating and integrating from $[A]_0$ at $t = 0$ to $[A]$ at $t$:

$$ [A] = [A]_0 - kt $$

This is the equation of a straight line: a plot of $[A]$ against $t$ has **slope $-k$**
and intercept $[A]_0$. The concentration falls by the same amount in every equal
interval of time, so the reaction finishes in a finite time, $t_{\text{complete}} =
[A]_0/k$.

**Half-life.** Put $[A] = [A]_0/2$:

$$ \frac{[A]_0}{2} = [A]_0 - kt_{1/2} \quad\Longrightarrow\quad t_{1/2} = \frac{[A]_0}{2k} $$

So for a zero-order reaction the half-life is **directly proportional** to the starting
concentration: start with twice as much and the first half takes twice as long. Each
successive half-life is shorter than the one before.

### First order

$$ \text{rate} = -\frac{d[A]}{dt} = k[A] $$

::: derivation The integrated rate law of a first-order reaction
We start from the rate law and want $[A]$ as a function of time.

**Step 1 — separate the variables.** Divide both sides by $[A]$ and multiply by $dt$:
$\frac{d[A]}{[A]} = -k\,dt$.

**Step 2 — integrate** between $t = 0$ (when $[A] = [A]_0$) and time $t$:
$\int_{[A]_0}^{[A]} \frac{d[A]}{[A]} = -k\int_0^t dt$.

**Step 3 — evaluate.** $\ln[A] - \ln[A]_0 = -kt$, that is
$\ln\frac{[A]}{[A]_0} = -kt$, or equivalently $\ln\frac{[A]_0}{[A]} = kt$.

**Step 4 — convert to base 10**, because CEE data are usually given as logarithms to
base 10: $\ln x = 2.303\log x$, so $k = \frac{2.303}{t}\log\frac{[A]_0}{[A]}$.

**Step 5 — exponentiate** for the working form: $[A] = [A]_0e^{-kt}$.

**Result.** $\ln\frac{[A]_0}{[A]} = kt$, $[A] = [A]_0e^{-kt}$,
$k = \frac{2.303}{t}\log\frac{[A]_0}{[A]}$.

**What it means.** A plot of $\ln[A]$ against $t$ is a straight line of slope $-k$; the
concentration itself decays exponentially, so it never quite reaches zero. The law
assumes the reaction is first order throughout and that temperature is constant.
:::

**Half-life.** Put $[A] = [A]_0/2$:

$$ kt_{1/2} = \ln 2 = 0.693 \quad\Longrightarrow\quad t_{1/2} = \frac{0.693}{k} $$

The initial concentration has cancelled out. **The half-life of a first-order reaction
is independent of the starting concentration** — this single sentence is the most
examined idea in the chapter. After $n$ half-lives the fraction left is $(1/2)^n$:

| Half-lives elapsed | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Fraction left | 1/2 | 1/4 | 1/8 | 1/16 | 1/32 |
| Percentage left | 50 % | 25 % | 12.5 % | 6.25 % | 3.13 % |

```figure caption="Concentration against time. A zero-order reaction (a) loses the same amount in every equal interval and reaches zero at a definite time; a first-order reaction (b) halves in every equal interval and never reaches zero."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(5.1, 2.6))
ax = axes[0]
t0 = np.linspace(0, 50, 300)
ax.plot(t0, np.clip(0.10 - 0.002*t0, 0, None), color=ACCENT, lw=1.9)
ax.plot([25], [0.05], 'o', color=ACCENT, ms=5, zorder=4)
ax.annotate('t½ = 25 s', xy=(25, 0.05), xytext=(27, 0.077), fontsize=8, color=INK,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
ax.set_title('(a) zero order', fontsize=9, loc='left')
ax.set_xlabel('time (s)'); ax.set_ylabel('[A] (mol L⁻¹)')
ax.set_xlim(0, 50); ax.set_ylim(0, 0.115)
ax.set_xticks([0, 10, 20, 30, 40, 50])
ax.spines[['top', 'right']].set_visible(False)
ax.grid(True, alpha=0.45)
ax = axes[1]
t1 = np.linspace(0, 40, 300)
ax.plot(t1, 0.10*np.exp(-0.0693*t1), color=SERIES[1], lw=1.9)
for tt, yy in [(10, 0.05), (20, 0.025), (30, 0.0125)]:
    ax.plot([tt], [yy], 'o', color=SERIES[1], ms=4.5, zorder=4)
    ax.plot([tt, tt], [0, yy], ls=':', lw=0.9, color=MUTED)
ax.text(21.5, 0.079, 'each 10 min\nhalves [A]', fontsize=8, color=INK)
ax.set_title('(b) first order', fontsize=9, loc='left')
ax.set_xlabel('time (min)'); ax.set_ylabel('[A] (mol L⁻¹)')
ax.set_xlim(0, 40); ax.set_ylim(0, 0.115)
ax.set_xticks([0, 10, 20, 30, 40])
ax.spines[['top', 'right']].set_visible(False)
ax.grid(True, alpha=0.45)
fig.tight_layout()
```

### The graphical test — which plot is straight?

This table answers most graph questions in the paper.

| Order | Plot that is a straight line | Slope | Intercept | Half-life |
|---|---|---|---|---|
| 0 | $[A]$ vs $t$ | $-k$ | $[A]_0$ | $[A]_0/2k$, ∝ $[A]_0$ |
| 1 | $\ln[A]$ vs $t$ | $-k$ | $\ln[A]_0$ | $0.693/k$, independent of $[A]_0$ |
| 2 | $1/[A]$ vs $t$ | $+k$ | $1/[A]_0$ | $1/(k[A]_0)$ |

```figure caption="Two first-order reactions with different starting concentrations. The lines are parallel, so both have the same slope $-k$ and the same half-life: after 10 min each concentration has fallen to half its own starting value."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8, 2.8))
t = np.linspace(0, 40, 200)
k = 0.0693
for A0, col, lab in [(0.10, ACCENT, '[A]₀ = 0.10 M'), (0.05, SERIES[1], '[A]₀ = 0.05 M')]:
    ax.plot(t, np.log(A0) - k*t, color=col, lw=1.9, label=lab)
    ax.plot([10], [np.log(A0/2)], 'o', color=col, ms=5, zorder=4)
ax.axvline(10, color=MUTED, ls=':', lw=1.0)
ax.text(11.5, -5.55, 'after 10 min both\nhave halved', fontsize=8.2, color=INK)
ax.set_xlabel('time (min)'); ax.set_ylabel('ln [A]')
ax.set_xlim(0, 40); ax.set_ylim(-6.1, -1.8)
ax.set_yticks([-2, -3, -4, -5, -6])
ax.legend(loc='upper right', fontsize=8.2)
ax.spines[['top', 'right']].set_visible(False)
ax.grid(True, alpha=0.45)
```

### Worked calculations

::: example First order: rate constant from two concentrations
**Problem.** The concentration in a first-order reaction falls from 0.80 M to 0.10 M in
400 s. Find $k$ and $t_{1/2}$.

**Solution.** $\frac{[A]_0}{[A]} = \frac{0.80}{0.10} = 8$, so
$k = \frac{2.303}{400}\log 8 = \frac{2.303 \times 0.903}{400} = \mathbf{5.2 \times 10^{-3}}$ s⁻¹.
Then $t_{1/2} = \frac{0.693}{5.2 \times 10^{-3}} = \mathbf{133}$ s.
Short cut: 0.80 → 0.10 is three halvings, so $t_{1/2} = 400/3 = 133$ s.
:::

::: example Zero order: half-life and completion time
**Problem.** A zero-order reaction has $[A]_0 = 0.10$ M and $k = 2.0 \times 10^{-3}$
mol L⁻¹ s⁻¹. Find $t_{1/2}$ and the time for complete reaction.

**Solution.** $t_{1/2} = \frac{[A]_0}{2k} = \frac{0.10}{2(2.0 \times 10^{-3})} = \mathbf{25}$ s.
Complete reaction means $[A] = 0$: $t = \frac{[A]_0}{k} = \frac{0.10}{2.0 \times 10^{-3}} = \mathbf{50}$ s.
The second half takes 25 s — the same as the first, because the rate never changes.
:::

::: caution Half-life traps
- **First order:** $t_{1/2}$ does not depend on $[A]_0$. An option saying "the half-life
  doubles when the initial concentration is doubled" is right only for zero order.
- **Zero order:** $t_{1/2}$ doubles when $[A]_0$ doubles, and the **second** half-life is
  *shorter* (it is half of the first) — unlike first order, where every half-life is equal.
- **"75 % complete" is two half-lives, not one and a half.** 100 → 50 → 25 means 75 %
  has gone in $2t_{1/2}$.
- **A first-order reaction never reaches 100 %.** Any option with "completes at
  $t = \ldots$" for first order is wrong.
:::

## 9.3 Collision theory, activation and threshold energy, the activated complex; factors affecting rate; catalysis

### Collision theory

Molecules in a gas collide about $10^{10}$ times per second, yet most reactions are
slow. Collision theory explains the gap with two filters:

$$ \text{rate} \propto Z \times f $$

where $Z$ is the **collision frequency** (collisions per unit volume per second) and
$f$ is the **fraction of collisions that are effective**. A collision produces reaction
only if (i) the molecules together carry energy at least equal to the **threshold
energy**, and (ii) they are **correctly oriented** at the moment of impact.

- Raising the **concentration** raises $Z$: more molecules in the same volume, more
  collisions, faster reaction.
- Raising the **temperature** raises both the average speed (so $Z$ rises slightly) and,
  far more importantly, $f$ (which rises steeply). The temperature effect is therefore
  much larger than the concentration effect.
- A **catalyst** raises $f$ by providing a route with a lower energy demand.

### Threshold energy, activation energy and the activated complex

::: definition Threshold energy, activation energy and activated complex
The **threshold energy** is the minimum total energy that colliding molecules must
possess if they are to react. The **activation energy** $E_a$ is the extra energy the
reactants must gain above their average energy to reach the threshold:
$E_a = E_{\text{threshold}} - E_{\text{reactants}}$. The **activated complex**
(transition state) is the short-lived, unstable, high-energy arrangement of atoms at the
top of the energy barrier; it is not an intermediate and cannot be isolated.
:::

```figure caption="Energy profile of an exothermic reaction with and without a catalyst. The catalyst lowers the barrier but leaves the energies of the reactants and products — and therefore $\Delta H$ — unchanged."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0, 2.9))
x = np.linspace(0, 10, 600)
s = 1/(1 + np.exp(-(x - 5)/0.5))
g = np.exp(-((x - 5)/0.55)**2)
uncat = 40 - 20*s + 60*g
cat = 40 - 20*s + 30*g
ax.plot(x, uncat, color=ACCENT, lw=2.0, label='without catalyst')
ax.plot(x, cat, color=SERIES[1], lw=2.0, ls='--', label='with catalyst')
ax.plot([1.6, 5.0], [60, 60], ls=':', lw=0.9, color=SERIES[1])
ax.plot([3.2, 5.0], [90, 90], ls=':', lw=0.9, color=ACCENT)
ax.annotate('', xy=(3.2, 90), xytext=(3.2, 40),
            arrowprops=dict(arrowstyle='<->', color=ACCENT, lw=1.1))
ax.annotate('', xy=(1.6, 60), xytext=(1.6, 40),
            arrowprops=dict(arrowstyle='<->', color=SERIES[1], lw=1.1))
ax.annotate('', xy=(8.7, 20), xytext=(8.7, 40),
            arrowprops=dict(arrowstyle='<->', color=INK, lw=1.1))
ax.text(3.05, 72, 'Ea', fontsize=9, color=ACCENT, ha='right')
ax.text(1.45, 54, "Ea′", fontsize=9, color=SERIES[1], ha='right')
ax.text(8.55, 30, 'ΔH < 0', fontsize=8.6, color=INK, ha='right', va='center')
ax.text(5.0, 94, 'activated complex', fontsize=8.4, color=INK, ha='center')
ax.text(0.15, 31.0, 'reactants', fontsize=8.4, color=MUTED)
ax.text(9.0, 14, 'products', fontsize=8.4, color=MUTED, ha='right')
ax.set_xlabel('reaction coordinate'); ax.set_ylabel('potential energy')
ax.set_xlim(0, 10); ax.set_ylim(8, 102)
ax.set_xticks([]); ax.set_yticks([])
ax.spines[['top', 'right']].set_visible(False)
ax.legend(loc='upper left', fontsize=8.2, bbox_to_anchor=(0.0, 1.0))
```

For a single-step reaction the enthalpy change is the difference of the two barriers:

$$ \Delta H = E_{a(\text{forward})} - E_{a(\text{backward})} $$

For an **exothermic** reaction $E_{a(\text{backward})} > E_{a(\text{forward})}$; for an
endothermic one the reverse. A catalyst lowers both barriers by the same amount, so
$\Delta H$ is untouched and the equilibrium constant cannot change — only the speed with
which equilibrium is reached.

### Temperature and the Arrhenius equation

$$ k = Ae^{-E_a/RT} $$

$A$ is the **frequency factor** (roughly the collision frequency with the right
orientation), $E_a$ the activation energy in J mol⁻¹, $R = 8.314$ J mol⁻¹ K⁻¹ and $T$ the
absolute temperature. Taking logarithms:

$$ \ln k = \ln A - \frac{E_a}{RT} $$

so a plot of $\ln k$ against $1/T$ is a straight line of slope $-E_a/R$. Comparing two
temperatures eliminates $A$:

$$ \log\frac{k_2}{k_1} = \frac{E_a}{2.303R}\left(\frac{1}{T_1} - \frac{1}{T_2}\right) $$

Because $E_a$ sits in the exponent, a small rise in $T$ produces a large rise in $k$.
The empirical **temperature coefficient** is $k$ at $(T + 10)$ divided by $k$ at $T$;
for most reactions near room temperature it lies between **2 and 3**, which is the
familiar rule that *a 10 °C rise roughly doubles the rate*.

```figure caption="Maxwell–Boltzmann distribution of molecular energies at two temperatures. Only molecules to the right of the $E_a$ line can react; warming the gas flattens the curve and thickens its tail, so a far larger fraction of molecules can react."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9, 2.8))
v = np.linspace(0, 1500, 600)
def mb(T):
    a = 0.032/(2*8.314*T)
    f = v**2*np.exp(-a*v**2)
    return f/f.max()
ax.plot(v, mb(300), color=ACCENT, lw=1.9, label='300 K')
ax.plot(v, mb(500), color=SERIES[1], lw=1.9, label='500 K')
ax.fill_between(v, 0, mb(500), where=(v >= 950), color=SERIES[1], alpha=0.30)
ax.fill_between(v, 0, mb(300), where=(v >= 950), color=ACCENT, alpha=0.55)
ax.axvline(950, color=MUTED, ls='--', lw=1.0)
ax.text(935, 0.60, 'Ea', fontsize=8.6, color=INK, ha='right')
ax.text(1005, 0.40, 'reacting\nmolecules', fontsize=8.2, color=INK)
ax.set_xlabel('molecular speed (m s⁻¹)'); ax.set_ylabel('fraction of molecules')
ax.set_xlim(0, 1500); ax.set_ylim(0, 1.05)
ax.set_yticks([])
ax.spines[['top', 'right']].set_visible(False)
ax.legend(loc='upper right', fontsize=8.2)
```

::: example Arrhenius in one line
**Problem.** A reaction has $E_a = 50$ kJ mol⁻¹. By what factor does $k$ increase when
the temperature rises from 300 K to 310 K? ($R = 8.314$ J mol⁻¹ K⁻¹)

**Solution.**
$\log\frac{k_2}{k_1} = \frac{50000}{2.303 \times 8.314}\left(\frac{1}{300} - \frac{1}{310}\right)
= 2612 \times (1.075 \times 10^{-4}) = 0.281$.
$\frac{k_2}{k_1} = 10^{0.281} = \mathbf{1.9}$, i.e. the rate roughly doubles — the 10 °C
rule, now derived rather than memorised.
:::

::: caution What temperature does *not* do
A rise in temperature does **not** lower the activation energy. The barrier stays where
it is; what changes is how many molecules have enough energy to clear it. An option
saying "heating lowers $E_a$" is a standard wrong key. Only a **catalyst** lowers $E_a$.
:::

### The other factors that change the rate

| Factor | Effect | Reason |
|---|---|---|
| Concentration of reactants | rate rises | more molecules per unit volume, so more collisions per second |
| Pressure (gases) | rate rises with pressure | same as raising concentration |
| Surface area (solids) | rate rises with finer division | reaction happens at the surface only |
| Temperature | rate rises steeply | larger fraction of molecules above $E_a$ |
| Catalyst | rate rises | alternative path with lower $E_a$ |
| Nature of the reactants | ionic and radical reactions are fast; covalent bond-breaking is slow | bond strength and number of bonds to break |
| Light | starts photochemical reactions | photons supply the activation energy (H₂ + Cl₂, photography, photosynthesis) |
| Solvent | can change the rate greatly | polarity and solvation stabilise or destabilise the activated complex |

### Catalysis: homogeneous, heterogeneous and enzyme

::: definition Catalyst
A **catalyst** is a substance that increases the rate of a reaction without itself being
consumed, by providing an alternative reaction path of lower activation energy. It is
recovered chemically unchanged in mass and composition at the end of the reaction.
:::

| Type | Phase | How it works | Examples |
|---|---|---|---|
| **Homogeneous** | same phase as the reactants (usually all gas or all liquid) | forms a short-lived intermediate with a reactant, which then decomposes | NO in the lead-chamber process (SO₂ + O₂); H⁺ in the hydrolysis of an ester; Cl• in the destruction of ozone; I⁻ in the decomposition of H₂O₂ |
| **Heterogeneous** | different phase — usually a solid with gaseous or liquid reactants | reactants are **adsorbed** on the surface, which weakens their bonds and holds them in the right orientation | Fe in the Haber process; V₂O₅ in the contact process; Pt in the oxidation of SO₂ and in catalytic converters; Ni in the hydrogenation of oils; MnO₂ in the decomposition of KClO₃ |
| **Enzyme** | biological, in living cells | a protein with an active site of fixed shape; the substrate fits like a key in a lock, so the enzyme is **highly specific** | zymase (glucose → ethanol); invertase (sucrose → glucose + fructose); urease (urea → NH₃ + CO₂); pepsin and trypsin (proteins); catalase (H₂O₂) |

**Characteristics of a catalyst — the list examiners pick from.**

1. It increases the rate of the forward and the backward reaction **equally**, so it
   shortens the time to reach equilibrium but does not shift the position of equilibrium
   or change $K$, $\Delta H$ or $\Delta G$.
2. It is needed in only a **small amount** and is regenerated, so its mass and
   composition are unchanged at the end.
3. It is **highly specific**: MnO₂ works for KClO₃ but not for every decomposition.
4. It works by **lowering the activation energy**, not by supplying energy.
5. A finely divided catalyst is more effective — greater surface area.
6. A **promoter** increases a catalyst's activity (Mo promotes Fe in the Haber process);
   a **poison** (catalyst poison) destroys it (arsenic poisons the Pt catalyst in the
   contact process; lead poisons the Pt in a catalytic converter).
7. A **negative catalyst** or inhibitor slows a reaction (glycerol in hydrogen peroxide;
   tetraethyl lead in petrol).
8. In **autocatalysis** a product catalyses its own reaction (Mn²⁺ in the
   permanganate–oxalate titration).
9. A catalyst **cannot make a thermodynamically forbidden reaction happen**; it only
   speeds a reaction that is already possible.
10. Enzymes are destroyed by high temperature and by extremes of pH — they are
    **denatured**, which is why the body has an optimum temperature near 37 °C.

::: memory The three "cannot"s of a catalyst
A catalyst **cannot** change $\Delta H$, **cannot** change the equilibrium constant, and
**cannot** start a reaction that is thermodynamically impossible. If an option claims
any of these, it is the distractor.
:::

## Formula and fact sheet

| Quantity | Relation | Unit |
|---|---|---|
| Rate of reaction | $-\frac{1}{a}\frac{d[A]}{dt} = \frac{1}{c}\frac{d[C]}{dt}$ | mol L⁻¹ s⁻¹ |
| Average rate | $-\Delta[R]/\Delta t$ over a finite interval | mol L⁻¹ s⁻¹ |
| Instantaneous rate | slope of the tangent to the concentration–time curve | mol L⁻¹ s⁻¹ |
| Rate law | rate $= k[A]^m[B]^n$; order $= m+n$ | — |
| Unit of $k$ | mol$^{1-n}$ L$^{n-1}$ s⁻¹ | see table |
| Zero order | $[A] = [A]_0 - kt$; $t_{1/2} = [A]_0/2k$; $t_{\text{complete}} = [A]_0/k$ | — |
| First order | $\ln\frac{[A]_0}{[A]} = kt$; $k = \frac{2.303}{t}\log\frac{[A]_0}{[A]}$ | s⁻¹ |
| First-order half-life | $t_{1/2} = 0.693/k$ | s |
| Fraction left after $n$ half-lives | $(1/2)^n$ | — |
| Second order | $\frac{1}{[A]} = \frac{1}{[A]_0} + kt$; $t_{1/2} = \frac{1}{k[A]_0}$ | L mol⁻¹ s⁻¹ |
| Arrhenius | $k = Ae^{-E_a/RT}$; $\ln k = \ln A - E_a/RT$ | — |
| Two temperatures | $\log\frac{k_2}{k_1} = \frac{E_a}{2.303R}\left(\frac{1}{T_1} - \frac{1}{T_2}\right)$ | — |
| Temperature coefficient | $k_{T+10}/k_T \approx 2$ to $3$ | — |
| Enthalpy from barriers | $\Delta H = E_{a(\text{f})} - E_{a(\text{b})}$ | J mol⁻¹ |

| Straight-line test | $y$-axis | Slope | Intercept |
|---|---|---|---|
| Zero order | $[A]$ | $-k$ | $[A]_0$ |
| First order | $\ln[A]$ | $-k$ | $\ln[A]_0$ |
| Second order | $1/[A]$ | $+k$ | $1/[A]_0$ |
| Arrhenius | $\ln k$ | $-E_a/R$ | $\ln A$ |

Orders and units to memorise: 0 → mol L⁻¹ s⁻¹; 1 → s⁻¹; 2 → L mol⁻¹ s⁻¹; 3 → L² mol⁻² s⁻¹.
Order–molecularity gaps: H₂ + Cl₂ → 2HCl (order 1.5, molecularity 2); 2NH₃ on tungsten
(order 0, molecularity 2); ester hydrolysis in excess water (pseudo-first-order,
molecularity 2).

## Chapter summary

- Rate is positive: for a reactant rate $= -(1/a)d[R]/dt$; the coefficient of every species must be included. Average rate is a chord, instantaneous rate a tangent.
- The rate law is experimental; order is the sum of the exponents and may be 0, fractional or negative, while molecularity is a theoretical whole number for one step.
- Units of $k$: mol L⁻¹ s⁻¹ (0), s⁻¹ (1), L mol⁻¹ s⁻¹ (2), L² mol⁻² s⁻¹ (3).
- Zero order: $[A] = [A]_0 - kt$, $t_{1/2} = [A]_0/2k$ (doubles when $[A]_0$ doubles), and the reaction finishes at $[A]_0/k$.
- First order: $\ln([A]_0/[A]) = kt$, $[A] = [A]_0e^{-kt}$, $t_{1/2} = 0.693/k$ — **independent of $[A]_0$**; $n$ half-lives leave $(1/2)^n$.
- A straight $\ln[A]$–$t$ plot (slope $-k$) is the test for first order; a straight $[A]$–$t$ plot is the test for zero order.
- Collision theory: rate depends on collision frequency and on the fraction of collisions with energy ≥ threshold energy and correct orientation; the activated complex is the top of the barrier.
- $k = Ae^{-E_a/RT}$; a 10 °C rise roughly doubles the rate; the barrier itself does not fall with temperature.
- A catalyst lowers $E_a$ for both directions, speeds the approach to equilibrium, and changes neither $\Delta H$, $\Delta G$ nor $K$; enzymes are specific biological catalysts with an optimum pH and temperature.

## Practice questions

**Set A — Recall (25 questions)**

1. The rate of disappearance of a reactant is written with a negative sign because
   (a) reactants are always solids (b) the stoichiometric coefficient of a reactant is negative (c) the reactant concentration falls, so $d[R]/dt$ is negative (d) the rate constant of a reactant is negative
2. The SI unit of the rate of a chemical reaction is
   (a) mol L⁻¹ s⁻¹ (b) mol L⁻¹ (c) s⁻¹ (d) L mol⁻¹ s⁻¹
3. For 2N₂O₅ → 4NO₂ + O₂ the rate of reaction is equal to
   (a) $-d[\text{N}_2\text{O}_5]/dt$ (b) $-2d[\text{N}_2\text{O}_5]/dt$ (c) $+\frac{1}{2}d[\text{N}_2\text{O}_5]/dt$ (d) $-\frac{1}{2}d[\text{N}_2\text{O}_5]/dt$
4. The unit of the rate constant of a first-order reaction is
   (a) mol L⁻¹ s⁻¹ (b) s⁻¹ (c) L mol⁻¹ s⁻¹ (d) mol⁻¹ L s⁻¹
5. The unit of $k$ for a zero-order reaction is
   (a) mol L⁻¹ s⁻¹ (b) s⁻¹ (c) L mol⁻¹ s⁻¹ (d) L² mol⁻² s⁻¹
6. The order of a reaction is
   (a) the number of molecules in the balanced equation (b) always equal to the molecularity (c) the sum of the concentration powers in the experimental rate law (d) the number of steps in the mechanism
7. The molecularity of a reaction
   (a) may be zero (b) may be fractional (c) is found by experiment (d) is always a whole number
8. The half-life of a first-order reaction is
   (a) directly proportional to $[A]_0$ (b) independent of $[A]_0$ (c) inversely proportional to $[A]_0$ (d) proportional to $[A]_0^2$
9. The integrated rate equation of a zero-order reaction is
   (a) $[A] = [A]_0e^{-kt}$ (b) $1/[A] = 1/[A]_0 + kt$ (c) $\ln[A] = \ln[A]_0 + kt$ (d) $[A] = [A]_0 - kt$
10. For a first-order reaction, a graph of $\ln[A]$ against time is
   (a) a straight line of slope $-k$ (b) a straight line of slope $+k$ (c) a straight line of slope $-k/2.303$ (d) a curve
11. For a zero-order reaction, a graph of $[A]$ against time is a straight line whose slope is
   (a) $+k$ (b) $-2.303k$ (c) $-k$ (d) $k/2.303$
12. For a first-order reaction, $t_{1/2}$ is equal to
   (a) $0.693k$ (b) $0.693/k$ (c) $k/0.693$ (d) $1/k$
13. According to collision theory, colliding molecules react only if they
   (a) have equal masses (b) collide exactly head-on (c) are in the gaseous state (d) have at least the threshold energy and a favourable orientation
14. The minimum energy that colliding molecules must possess in order to react is called the
   (a) activation energy (b) internal energy (c) bond energy (d) lattice energy
15. The short-lived, high-energy arrangement of atoms at the top of the energy barrier is the
   (a) intermediate (b) activated complex (c) free radical (d) catalyst
16. A catalyst increases the rate of a reaction by
   (a) raising the activation energy (b) changing the enthalpy of reaction (c) providing an alternative path of lower activation energy (d) increasing the equilibrium constant
17. The catalyst used in the Haber process is
   (a) iron (b) V₂O₅ (c) platinum (d) nickel
18. A catalyst present in a different phase from the reactants is described as
   (a) homogeneous (b) an enzyme (c) an autocatalyst (d) heterogeneous
19. Enzymes are
   (a) inorganic catalysts (b) inhibitors of biological reactions (c) highly specific biological catalysts (d) homogeneous gas-phase catalysts
20. The temperature coefficient of a reaction compares the rate constants at two temperatures differing by
   (a) 1 K (b) 10 K (c) 100 K (d) 273 K
21. The Arrhenius equation is
   (a) $k = Ae^{-E_a/RT}$ (b) $k = Ae^{E_a/RT}$ (c) $k = Ae^{-RT/E_a}$ (d) $k = A + e^{-E_a/RT}$
22. A reaction whose rate does not depend on the concentration of the reactant is of
   (a) first order (b) second order (c) zero order (d) fractional order
23. The unit of the rate constant of a second-order reaction is
   (a) s⁻¹ (b) L mol⁻¹ s⁻¹ (c) mol L⁻¹ s⁻¹ (d) L² mol⁻² s⁻¹
24. For H₂ + Cl₂ → 2HCl the rate law is rate $= k[\text{H}_2][\text{Cl}_2]^{1/2}$. The overall order is
   (a) 1 (b) 2 (c) 3 (d) 1.5
25. The hydrolysis of an ester in a large excess of water is an example of a
   (a) zero-order reaction (b) pseudo-first-order reaction (c) second-order reaction (d) third-order reaction

::: note Answers and explanations — Set A
**1.** (c) — Concentration falls, so $d[R]/dt$ is negative; the minus sign makes the rate positive. Rate constants are always positive and coefficients are positive numbers.
**2.** (a) — Concentration per unit time, mol L⁻¹ ÷ s. Option (c) is the unit of a first-order $k$; (d) of a second-order $k$.
**3.** (d) — Every rate must agree, so each is divided by its coefficient; N₂O₅ has 2 and is consumed.
**4.** (b) — rate $= k[A]$ gives mol L⁻¹ s⁻¹ = $k$ × mol L⁻¹, so $k$ is in s⁻¹.
**5.** (a) — rate $= k$ for zero order, so $k$ carries the unit of rate itself.
**6.** (c) — Order is experimental. It equals the molecularity only for a single-step reaction.
**7.** (d) — Molecularity counts whole species colliding in one step, so it cannot be 0 or a fraction. Zero and fractional orders exist because order is empirical.
**8.** (b) — $t_{1/2} = 0.693/k$ contains no concentration term. Only for zero order is $t_{1/2}$ proportional to $[A]_0$.
**9.** (d) — Integrating $-d[A]/dt = k$ gives $[A] = [A]_0 - kt$. Option (a) is the first-order law, (b) the second-order law.
**10.** (a) — $\ln[A] = \ln[A]_0 - kt$; slope $-k$, intercept $\ln[A]_0$.
**11.** (c) — $[A] = [A]_0 - kt$; the slope is $-k$.
**12.** (b) — Putting $[A] = [A]_0/2$ in the integrated law gives $kt_{1/2} = \ln 2 = 0.693$.
**13.** (d) — Both conditions are needed: enough energy **and** the right geometry. Head-on collision alone is neither necessary nor sufficient.
**14.** (a) — The activation energy is the extra energy above the reactants' average energy needed to reach the threshold.
**15.** (b) — The activated complex is a transient arrangement at the peak; an intermediate sits in a valley between two steps.
**16.** (c) — A catalyst offers a new path of lower $E_a$. It cannot alter $\Delta H$ or $K$.
**17.** (a) — Iron with molybdenum as promoter. V₂O₅ is the contact process, Pt the oxidation of SO₂ and catalytic converters, Ni the hydrogenation of oils.
**18.** (d) — Different phase, e.g. solid Fe with gaseous N₂ and H₂. A homogeneous catalyst shares the phase of the reactants.
**19.** (c) — Enzymes are proteins with an active site of fixed shape, hence highly specific; they work best at an optimum pH and near 37 °C.
**20.** (b) — The temperature coefficient is $k_{T+10}/k_T$, usually about 2 to 3.
**21.** (a) — $k$ rises as $T$ rises, which requires the negative exponent $-E_a/RT$.
**22.** (c) — Rate $= k[A]^0 = k$, independent of concentration. This happens on a saturated catalyst surface.
**23.** (b) — mol L⁻¹ s⁻¹ = $k$(mol L⁻¹)², so $k$ is in L mol⁻¹ s⁻¹.
**24.** (d) — Order $= 1 + \frac{1}{2} = 1.5$. The balanced equation's coefficients (1 and 1) do not give the order.
**25.** (b) — Water is in such large excess that its concentration is effectively constant, so the observed order is 1 although two molecules are involved.
:::

**Set B — Understanding (15 questions)**

1. The order of a reaction can be fractional but its molecularity cannot, because molecularity
   (a) is measured at constant temperature (b) counts the actual species colliding in one elementary step (c) depends on the concentrations used (d) equals the number of product molecules
2. The decomposition of ammonia on a hot tungsten surface has a rate independent of ammonia pressure. The reaction is
   (a) first order (b) second order (c) of order 1.5 (d) zero order
3. The half-life of a first-order reaction is 20 min. The time for the concentration to fall to one-eighth of its initial value is
   (a) 60 min (b) 40 min (c) 80 min (d) 160 min
4. For a zero-order reaction, the time needed for complete reaction is
   (a) independent of $[A]_0$ (b) proportional to $1/[A]_0$ (c) proportional to $[A]_0$ (d) proportional to $[A]_0^2$
5. A catalyst does NOT change the
   (a) rate of the forward reaction (b) enthalpy change of the reaction (c) activation energy (d) rate of the reverse reaction
6. The rate of most reactions increases with temperature mainly because
   (a) a larger fraction of molecules has energy at least equal to $E_a$ (b) the activation energy falls (c) the molecules become smaller (d) the concentration of the reactants rises
7. For an exothermic reaction, the activation energy of the reverse reaction is
   (a) equal to that of the forward reaction (b) smaller than that of the forward reaction (c) zero (d) larger than that of the forward reaction
8. Two reactions have the same rate constant at 300 K but different activation energies. At 350 K the reaction with the larger $E_a$ has
   (a) the smaller rate constant (b) the same rate constant (c) the larger rate constant (d) a rate constant that cannot be compared
9. Which statement about the rate constant $k$ is correct?
   (a) It equals the rate when every reactant concentration is 1 mol L⁻¹ (b) It depends on the concentrations of the reactants (c) It has the same unit for every reaction (d) It increases steadily as the reaction proceeds
10. If the activation energy of a reaction is zero, the rate
   (a) is zero at every temperature (b) does not depend on temperature (c) doubles for every 10 K rise (d) falls as the temperature rises
11. A homogeneous catalyst is one that
   (a) is always a solid (b) is in a different phase from the reactants (c) is consumed during the reaction (d) is in the same phase as the reactants
12. Enzyme-catalysed reactions are characterised by
   (a) very high activation energies (b) a complete absence of specificity (c) maximum activity at an optimum pH and temperature (d) independence of temperature
13. The half-life of a first-order reaction is 10 min. The time needed for 99.9 % completion is about
   (a) 100 min (b) 30 min (c) 50 min (d) 1000 min
14. In an energy profile, the difference between the threshold energy and the average energy of the reactants is the
   (a) enthalpy of reaction (b) bond energy (c) activation energy (d) internal energy
15. The rate of a reaction between a gas and a solid is increased most by
   (a) using the solid in large lumps (b) grinding the solid to a fine powder (c) cooling the reaction mixture (d) adding an inert gas at constant volume

::: note Answers and explanations — Set B
**1.** (b) — Molecularity is a count of particles in one step, so it is a whole number. Order is empirical and may be fractional because it reflects the mechanism, not a count.
**2.** (d) — A saturated surface cannot use more ammonia, so the rate stops responding to pressure: rate $= k[\text{NH}_3]^0$.
**3.** (a) — One-eighth is three halvings: $3 \times 20 = 60$ min. Option (b) is two half-lives (one-quarter left).
**4.** (c) — $t_{\text{complete}} = [A]_0/k$, so doubling $[A]_0$ doubles the time. For first order there is no finite completion time.
**5.** (b) — A catalyst lowers $E_a$ and so speeds both directions, but $\Delta H$ depends only on the reactants and products.
**6.** (a) — Heating does not lower the barrier; it shifts the Maxwell–Boltzmann curve so that a much larger fraction lies above $E_a$.
**7.** (d) — $\Delta H = E_{a(\text{f})} - E_{a(\text{b})}$ is negative for an exothermic reaction, so $E_{a(\text{b})}$ must be the larger.
**8.** (c) — $\ln k$ changes with temperature at the rate $E_a/RT^2$; the reaction with the larger $E_a$ is more temperature-sensitive, so it overtakes the other.
**9.** (a) — That is the definition of the specific rate constant. $k$ does not depend on concentration, and its unit changes with the order.
**10.** (b) — $k = Ae^{0} = A$, so $k$ is independent of $T$. This is the case for some radical recombinations.
**11.** (d) — Same phase, e.g. NO gas with SO₂ and O₂ gases, or H⁺(aq) in ester hydrolysis.
**12.** (c) — Enzymes are proteins: specific, and denatured by heat or by the wrong pH, so they show an optimum near body temperature.
**13.** (a) — 99.9 % gone leaves 0.1 % = $10^{-3}$, which is about 10 half-lives ($2^{10} = 1024$): $10 \times 10 = 100$ min.
**14.** (c) — $E_a = E_{\text{threshold}} - E_{\text{reactants}}$. The enthalpy change compares products with reactants, not the peak with the reactants.
**15.** (b) — Reaction occurs only at the surface, so finer division exposes far more surface. Cooling slows it; an inert gas at constant volume changes nothing.
:::

**Set C — Application (10 questions)**

1. In the decomposition 2N₂O₅ → 4NO₂ + O₂, oxygen is formed at $2.0 \times 10^{-3}$ mol L⁻¹ s⁻¹. The rate of disappearance of N₂O₅ is
   (a) $1.0 \times 10^{-3}$ (b) $2.0 \times 10^{-3}$ (c) $4.0 \times 10^{-3}$ (d) $8.0 \times 10^{-3}$ mol L⁻¹ s⁻¹
2. A first-order reaction has a half-life of 10 min. Its rate constant is
   (a) $6.93 \times 10^{-2}$ min⁻¹ (b) $6.93 \times 10^{-3}$ min⁻¹ (c) $1.44 \times 10^{-1}$ min⁻¹ (d) 0.693 min⁻¹
3. In a first-order reaction the concentration falls from 0.80 M to 0.10 M in 400 s. The rate constant is
   (a) $2.6 \times 10^{-3}$ s⁻¹ (b) $1.7 \times 10^{-3}$ s⁻¹ (c) $6.9 \times 10^{-3}$ s⁻¹ (d) $5.2 \times 10^{-3}$ s⁻¹
4. A zero-order reaction has $[A]_0 = 0.10$ M and $k = 2.0 \times 10^{-3}$ mol L⁻¹ s⁻¹. Its half-life is
   (a) 50 s (b) 25 s (c) 5.0 s (d) 100 s
5. For A + B → products, doubling [A] at fixed [B] doubles the rate, while doubling [B] at fixed [A] makes the rate four times larger. The rate law is
   (a) rate $= k[A][B]^2$ (b) rate $= k[A]^2[B]$ (c) rate $= k[A][B]$ (d) rate $= k[A]^2[B]^2$
6. For a reaction with rate $= k[A][B]^2$, the rate is $2.0 \times 10^{-3}$ mol L⁻¹ s⁻¹ when [A] = [B] = 0.10 M. The value of $k$ is
   (a) 0.20 (b) $2.0 \times 10^{-2}$ (c) 2.0 (d) 20, in L² mol⁻² s⁻¹
7. The rate constant of a reaction doubles when the temperature rises from 300 K to 310 K. Taking $R = 8.314$ J mol⁻¹ K⁻¹, $E_a$ is about
   (a) 50 kJ mol⁻¹ (b) 25 kJ mol⁻¹ (c) 200 kJ mol⁻¹ (d) 107 kJ mol⁻¹
8. A first-order reaction is 75 % complete in 60 min. Its half-life is
   (a) 30 min (b) 20 min (c) 45 min (d) 60 min
9. A zero-order reaction starts at 0.50 M with $k = 1.0 \times 10^{-2}$ mol L⁻¹ s⁻¹. The concentration after 20 s is
   (a) 0.10 M (b) 0.20 M (c) 0.30 M (d) 0.40 M
10. The half-life of a first-order reaction is 1.5 h. Its rate constant in s⁻¹ is
   (a) $4.6 \times 10^{-4}$ (b) $1.28 \times 10^{-4}$ (c) $1.28 \times 10^{-3}$ (d) $7.7 \times 10^{-3}$

::: note Answers and explanations — Set C
**1.** (c) — $-d[\text{N}_2\text{O}_5]/dt = 2 \times d[\text{O}_2]/dt = 4.0 \times 10^{-3}$. Option (b) forgets the coefficient 2.
**2.** (a) — $k = 0.693/10 = 6.93 \times 10^{-2}$ min⁻¹. Option (b) divides by 100; (d) forgets to divide at all.
**3.** (d) — $k = \frac{2.303}{400}\log 8 = \frac{2.303 \times 0.903}{400} = 5.2 \times 10^{-3}$ s⁻¹. Short cut: three halvings in 400 s, so $t_{1/2} = 133$ s and $k = 0.693/133$.
**4.** (b) — $t_{1/2} = [A]_0/2k = 0.10/(4.0 \times 10^{-3}) = 25$ s. Option (a) is the completion time, $[A]_0/k$.
**5.** (a) — Order in A is 1 (rate doubles), order in B is 2 (rate quadruples). Option (c) is the answer students give when they ignore the four-fold change.
**6.** (c) — $k = \frac{2.0 \times 10^{-3}}{(0.10)(0.10)^2} = 2.0$ L² mol⁻² s⁻¹. Option (a) uses $[A][B]$ instead of $[A][B]^2$.
**7.** (d) — $\log 2 = \frac{E_a}{2.303 \times 8.314}\left(\frac{1}{300} - \frac{1}{310}\right)$, so $E_a = \frac{0.301 \times 19.15}{1.075 \times 10^{-4}} \approx 1.07 \times 10^{5}$ J mol⁻¹.
**8.** (a) — 75 % complete means two half-lives (100 → 50 → 25), so $t_{1/2} = 30$ min. Option (c) wrongly halves 75.
**9.** (c) — $[A] = 0.50 - (1.0 \times 10^{-2})(20) = 0.30$ M. Option (a) subtracts 0.40, using twice the time.
**10.** (b) — 1.5 h = 5400 s, so $k = 0.693/5400 = 1.28 \times 10^{-4}$ s⁻¹. Option (a) is the same number with the wrong power of ten.
:::
