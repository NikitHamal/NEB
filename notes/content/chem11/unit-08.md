---
subject: Chemistry
grade: 11
unit: 8
title: Chemical equilibrium
hours: 3
area: General and Physical Chemistry
---

Most reactions do not go to completion. Long before all the reactants are used
up, the products begin turning back into reactants, and the two opposing changes
settle down to the same speed. Nothing appears to happen after that, yet both
reactions are still running. This balanced, unfinished state is **chemical
equilibrium**, and it decides how much ammonia a Haber plant can make and how
much sulphur trioxide a contact plant can make.

::: key What the examiner asks from this unit
Numerically, only two things come up: writing $K_c$ from a balanced equation and
converting between $K_p$ and $K_c$. Theoretically, expect "state the law of mass
action", "give four characteristics of dynamic equilibrium" and "apply Le
Chatelier's principle to the Haber process". Le Chatelier numericals are **not**
required.
:::

## 8.1 Physical and chemical equilibrium

A **reversible change** is one that can go in both directions under the same
conditions; it is written with a double half-arrow, ⇌. When the two opposing
changes go at the same rate in a closed system, the system is in **equilibrium**.

**Physical equilibrium** involves only a change of physical state — no new
substance is formed.

| Physical equilibrium | Example | Condition |
|---|---|---|
| Solid ⇌ Liquid | H₂O(s) ⇌ H₂O(l) | melting point, 0 °C at 1 atm |
| Liquid ⇌ Vapour | H₂O(l) ⇌ H₂O(g) | any closed vessel; fixes the vapour pressure |
| Solid ⇌ Vapour | I₂(s) ⇌ I₂(g) | sublimation, as in camphor or naphthalene |
| Solute ⇌ Solution | sugar(s) ⇌ sugar(aq) | a saturated solution |
| Gas ⇌ Solution | CO₂(g) ⇌ CO₂(aq) | a sealed bottle of soda |

**Chemical equilibrium** involves a chemical reaction, so new substances are
formed. Examples:

- N₂(g) + 3H₂(g) ⇌ 2NH₃(g)
- 2SO₂(g) + O₂(g) ⇌ 2SO₃(g)
- H₂(g) + I₂(g) ⇌ 2HI(g)
- CH₃COOH(l) + C₂H₅OH(l) ⇌ CH₃COOC₂H₅(l) + H₂O(l)
- CaCO₃(s) ⇌ CaO(s) + CO₂(g)  (in a closed vessel)

## 8.2 Dynamic nature of chemical equilibrium

At the start of a reaction only reactants are present, so the forward rate is
large and the backward rate is zero. As reactants are consumed the forward rate
falls; as products accumulate the backward rate rises. Sooner or later the two
rates become equal.

```figure caption="Forward and backward rates for H₂ + I₂ ⇌ 2HI, obtained by integrating the rate equations. Equilibrium is the instant the two rates become equal — after that both reactions continue, but at the same speed."
import numpy as np, matplotlib.pyplot as plt
kf, kr = 0.64, 0.01
dt, n = 0.002, 7000
H = np.zeros(n); I = np.zeros(n); HI = np.zeros(n)
H[0] = I[0] = 1.0
for i in range(n-1):
    r_f = kf*H[i]*I[i]; r_b = kr*HI[i]**2
    d = (r_f - r_b)*dt
    H[i+1] = H[i] - d; I[i+1] = I[i] - d; HI[i+1] = HI[i] + 2*d
t = np.arange(n)*dt
rf = kf*H*I; rb = kr*HI**2
fig, ax = plt.subplots(figsize=(4.7,2.8))
ax.plot(t, rf, color=SERIES[0], lw=1.9, label='forward rate  kf[H₂][I₂]')
ax.plot(t, rb, color=SERIES[1], lw=1.9, label='backward rate  kr[HI]²')
ax.axhline(0.0256, color=MUTED, lw=.9, ls=':')
ax.annotate('rates become equal:\nequilibrium', xy=(9.5, 0.0256), xytext=(6.4, 0.26),
            fontsize=8.4, color=INK, ha='center',
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.0, mutation_scale=9))
ax.set_xlabel('time  (arbitrary units)'); ax.set_ylabel('rate  (mol L⁻¹ s⁻¹)')
ax.set_xlim(0, 14); ax.set_ylim(0, 0.70)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.5); ax.legend()
```

::: definition Chemical equilibrium
Chemical equilibrium is the state of a reversible reaction in a closed system at
which the rate of the forward reaction becomes equal to the rate of the backward
reaction, so that the concentrations of reactants and products no longer change
with time.
:::

Equilibrium is **dynamic**, not static. Its characteristics are:

1. It is reached only in a **closed system** at constant temperature.
2. The forward and backward reactions **never stop**; they merely go at equal
   rates. Isotopic labelling proves this — label the iodine as I-131 in
   2HI and the label soon appears in I₂.
3. All observable properties (concentration, colour, pressure, density) become
   **constant** with time.
4. The same equilibrium state can be reached **from either direction** — from
   pure reactants or from pure products — provided the temperature and total
   composition are the same.
5. A **catalyst** does not change the position of equilibrium; it only makes the
   system reach it faster, because it speeds up both reactions equally.

```figure caption="The same equilibrium reached from both sides. Solid lines start from 1 M H₂ + 1 M I₂; dashed lines start from 2 M HI. Both end at [HI] = 1.6 M and [H₂] = [I₂] = 0.2 M."
import numpy as np, matplotlib.pyplot as plt
kf, kr = 0.64, 0.01
def run(h0, hi0, n=6000, dt=0.002):
    H = np.zeros(n); HI = np.zeros(n)
    H[0] = h0; HI[0] = hi0
    for i in range(n-1):
        d = (kf*H[i]*H[i] - kr*HI[i]**2)*dt
        H[i+1] = H[i] - d; HI[i+1] = HI[i] + 2*d
    return np.arange(n)*dt, H, HI
t, H1, HI1 = run(1.0, 0.0)
_, H2, HI2 = run(0.0, 2.0)
fig, ax = plt.subplots(figsize=(4.7,2.8))
ax.plot(t, HI1, color=SERIES[0], lw=1.9, label='[HI]')
ax.plot(t, H1,  color=SERIES[2], lw=1.9, label='[H₂] = [I₂]')
ax.plot(t, HI2, color=SERIES[0], lw=1.5, ls='--')
ax.plot(t, H2,  color=SERIES[2], lw=1.5, ls='--')
ax.axhline(1.6, color=MUTED, lw=.8, ls=':')
ax.axhline(0.2, color=MUTED, lw=.8, ls=':')
ax.text(9.4, 1.66, '1.6 M', fontsize=8.2, color=MUTED)
ax.text(9.4, 0.26, '0.2 M', fontsize=8.2, color=MUTED)
ax.set_xlabel('time  (arbitrary units)'); ax.set_ylabel('concentration  (mol L⁻¹)')
ax.set_xlim(0, 12); ax.set_ylim(0, 2.1)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.5); ax.legend(loc='center right')
```

## 8.3 Law of mass action

::: definition Law of mass action (Guldberg and Waage, 1864)
At a given temperature, the rate of a chemical reaction is directly proportional
to the product of the molar concentrations of the reactants, each raised to the
power equal to its coefficient in the balanced chemical equation.
:::

The molar concentration of a substance is called its **active mass**, written in
square brackets: $[A]$ in mol L⁻¹. For the general reversible reaction

aA + bB ⇌ cC + dD

the law of mass action gives the two rates as

$$ r_f = k_f[A]^{a}[B]^{b}, \qquad r_b = k_r[C]^{c}[D]^{d} $$

::: caution "Active mass" is not mass
Active mass means **molar concentration** (mol L⁻¹), not the mass in grams. For a
pure solid or a pure liquid the concentration is fixed by its density, so its
active mass is taken as **1** and it is left out of the equilibrium expression.
:::

## 8.4 Expression for equilibrium constant and its importance

At equilibrium the two rates are equal, $r_f = r_b$:

$$ k_f[A]^{a}[B]^{b} = k_r[C]^{c}[D]^{d} $$

$$ \frac{k_f}{k_r} = \frac{[C]^{c}[D]^{d}}{[A]^{a}[B]^{b}} = K_c $$

$K_c$ is the **equilibrium constant in terms of concentration**. If all species
are gases we may use partial pressures instead:

$$ K_p = \frac{p_C^{c}\,p_D^{d}}{p_A^{a}\,p_B^{b}} $$

The units of $K_c$ are $(\text{mol L}^{-1})^{\Delta n}$ and of $K_p$ are
$(\text{atm})^{\Delta n}$, where $\Delta n = (c+d) - (a+b)$ is the change in the
number of **gaseous** moles. When $\Delta n = 0$ both are dimensionless.

| Reaction | $K_c$ expression | $\Delta n$ | Units of $K_c$ |
|---|---|---|---|
| H₂ + I₂ ⇌ 2HI | [HI]²/([H₂][I₂]) | 0 | none |
| N₂ + 3H₂ ⇌ 2NH₃ | [NH₃]²/([N₂][H₂]³) | −2 | mol⁻² L² |
| PCl₅ ⇌ PCl₃ + Cl₂ | [PCl₃][Cl₂]/[PCl₅] | +1 | mol L⁻¹ |
| 2SO₂ + O₂ ⇌ 2SO₃ | [SO₃]²/([SO₂]²[O₂]) | −1 | mol⁻¹ L |
| CaCO₃(s) ⇌ CaO(s) + CO₂(g) | [CO₂] | +1 | mol L⁻¹ |

**Importance of the equilibrium constant**

1. **Extent of reaction.** A large $K$ (say $>10^{3}$) means the equilibrium
   mixture is almost all products; a small $K$ ($<10^{-3}$) means the reaction
   hardly proceeds. $K \approx 1$ means comparable amounts of both.
2. **Direction of reaction.** Compute the **reaction quotient** $Q$ using the
   same expression but with the *actual* concentrations. If $Q < K$ the reaction
   moves forward; if $Q > K$ it moves backward; if $Q = K$ it is already at
   equilibrium.
3. **Calculation of equilibrium concentrations** and of the yield of a product.
4. $K$ depends **only on temperature** — not on pressure, volume, initial
   concentrations or the presence of a catalyst.
5. Reversing a reaction replaces $K$ by $1/K$; multiplying the equation through
   by $n$ replaces $K$ by $K^{n}$.

::: example Worked example 8.1 — $K_c$ from an ICE table
**Problem.** One mole of H₂ and one mole of I₂ are heated in a closed 10 L flask
at $450\ ^{\circ}\text{C}$. At equilibrium 1.6 mol of HI is present. Calculate
$K_c$.

**Solution.** Let $x$ mol of H₂ react. Build an ICE (Initial–Change–Equilibrium)
table in **moles** first.

| | H₂ | I₂ | 2HI |
|---|---|---|---|
| **I**nitial (mol) | 1 | 1 | 0 |
| **C**hange (mol) | −x | −x | +2x |
| **E**quilibrium (mol) | 1 − x | 1 − x | 2x |

Given $2x = 1.6$, so $x = 0.8$. Equilibrium amounts are H₂ = 0.2 mol,
I₂ = 0.2 mol, HI = 1.6 mol. Divide by the volume (10 L) to get concentrations:

$$ [H_2] = [I_2] = 0.02\ \text{mol L}^{-1}, \qquad [HI] = 0.16\ \text{mol L}^{-1} $$

$$ K_c = \frac{[HI]^{2}}{[H_2][I_2]} = \frac{(0.16)^{2}}{(0.02)(0.02)} = \frac{0.0256}{0.0004} = 64 $$

$K_c = 64$, with no units because $\Delta n = 0$.
:::

::: example Worked example 8.2 — working backwards from $K_c$
**Problem.** For H₂ + I₂ ⇌ 2HI, $K_c = 64$ at $450\ ^{\circ}\text{C}$. If 1 mol
of H₂ and 1 mol of I₂ are placed in a 1 L vessel at this temperature, find the
equilibrium concentration of HI.

**Solution.** With $V = 1\ \text{L}$, moles and concentrations are numerically
equal.

| | H₂ | I₂ | 2HI |
|---|---|---|---|
| **I**nitial (M) | 1 | 1 | 0 |
| **C**hange (M) | −x | −x | +2x |
| **E**quilibrium (M) | 1 − x | 1 − x | 2x |

$$ K_c = \frac{(2x)^{2}}{(1-x)(1-x)} = \frac{4x^{2}}{(1-x)^{2}} = 64 $$

Both sides are perfect squares, so take the square root — this avoids the
quadratic:

$$ \frac{2x}{1-x} = 8 \;\Longrightarrow\; 2x = 8 - 8x \;\Longrightarrow\; 10x = 8 $$

So $x = 0.8$ and $[HI] = 2x = 1.6\ \text{mol L}^{-1}$, with
$[H_2] = [I_2] = 0.2\ \text{mol L}^{-1}$ — the same mixture as in Example 8.1,
as it must be.
:::

## 8.5 Relationship between $K_p$ and $K_c$

For an ideal gas, $PV = nRT$, so the partial pressure of a gas is related to its
molar concentration by

$$ p_A = \frac{n_A}{V}RT = [A]\,RT $$

Substituting this for every species in the expression for $K_p$:

$$ K_p = \frac{([C]RT)^{c}([D]RT)^{d}}{([A]RT)^{a}([B]RT)^{b}}
 = \frac{[C]^{c}[D]^{d}}{[A]^{a}[B]^{b}} \times (RT)^{(c+d)-(a+b)} $$

$$ \boxed{K_p = K_c (RT)^{\Delta n}} \qquad \Delta n = n_{products(g)} - n_{reactants(g)} $$

Three cases follow at once:

| $\Delta n$ | Relation | Example |
|---|---|---|
| $\Delta n = 0$ | $K_p = K_c$ | H₂ + I₂ ⇌ 2HI |
| $\Delta n > 0$ | $K_p > K_c$ | PCl₅ ⇌ PCl₃ + Cl₂ |
| $\Delta n < 0$ | $K_p < K_c$ | N₂ + 3H₂ ⇌ 2NH₃ |

::: caution Match R to the units of pressure
If $K_p$ is wanted in atm, use $R = 0.0821\ \text{L atm K}^{-1}\text{mol}^{-1}$
and concentrations in mol L⁻¹. Using $R = 8.314$ with atmospheres is the most
common error in this calculation. And $T$ is always in **kelvin**.
:::

::: example Worked example 8.3 — degree of dissociation, $K_c$ and $K_p$
**Problem.** 2 mol of PCl₅ were heated in a closed 2 L vessel at
$250\ ^{\circ}\text{C}$. At equilibrium PCl₅ was found to be 40 % dissociated.
Calculate $K_c$ and $K_p$.

**Solution.** Moles dissociated $= 0.40 \times 2 = 0.8\ \text{mol}$.

| | PCl₅ | PCl₃ | Cl₂ |
|---|---|---|---|
| **I**nitial (mol) | 2 | 0 | 0 |
| **C**hange (mol) | −0.8 | +0.8 | +0.8 |
| **E**quilibrium (mol) | 1.2 | 0.8 | 0.8 |

Dividing by $V = 2\ \text{L}$:

$$ [PCl_5] = 0.6, \quad [PCl_3] = 0.4, \quad [Cl_2] = 0.4\ \text{mol L}^{-1} $$

$$ K_c = \frac{[PCl_3][Cl_2]}{[PCl_5]} = \frac{(0.4)(0.4)}{0.6} = \frac{0.16}{0.6} = 0.267\ \text{mol L}^{-1} $$

Here $\Delta n = 2 - 1 = +1$ and $T = 250 + 273 = 523\ \text{K}$, so

$$ K_p = K_c(RT)^{1} = 0.267 \times 0.0821 \times 523 = 11.5\ \text{atm} $$
:::

::: example Worked example 8.4 — converting $K_c$ to $K_p$ for ammonia
**Problem.** For N₂(g) + 3H₂(g) ⇌ 2NH₃(g), $K_c = 0.50\ \text{mol}^{-2}\text{L}^{2}$
at $400\ ^{\circ}\text{C}$. Calculate $K_p$.

**Solution.** $\Delta n = 2 - (1+3) = -2$ and $T = 400 + 273 = 673\ \text{K}$.

$$ RT = 0.0821 \times 673 = 55.25\ \text{L atm mol}^{-1} $$

$$ K_p = K_c(RT)^{-2} = \frac{0.50}{(55.25)^{2}} = \frac{0.50}{3052.6} $$

$$ K_p = 1.64\times10^{-4}\ \text{atm}^{-2} $$

$K_p < K_c$, as expected for $\Delta n < 0$.
:::

## 8.6 Le Chatelier's Principle

::: definition Le Chatelier's Principle (1884)
If a system at equilibrium is disturbed by a change in concentration, pressure or
temperature, the equilibrium shifts in the direction that tends to **oppose** or
undo the effect of the change.
:::

| Change applied | Direction of shift | Reason |
|---|---|---|
| Increase concentration of a reactant | forward | system consumes the added reactant |
| Remove a product as it forms | forward | system replaces what was removed |
| Increase total pressure (decrease volume) | towards the side with **fewer** gaseous moles | that reduces the pressure again |
| Decrease pressure | towards the side with **more** gaseous moles | — |
| Increase temperature | in the **endothermic** direction | that absorbs the added heat |
| Decrease temperature | in the **exothermic** direction | — |
| Add a catalyst | **no shift** | both rates are speeded up equally |
| Add an inert gas at constant **volume** | **no shift** | partial pressures are unchanged |

Only a change of temperature changes the **value** of $K$. Concentration and
pressure changes move the position of equilibrium but leave $K$ the same.

**Application 1 — Haber process.**
N₂(g) + 3H₂(g) ⇌ 2NH₃(g);  ΔH = −92.4 kJ mol⁻¹

Since $\Delta n = -2$, a **high pressure** (about 200 atm) pushes the equilibrium
towards ammonia. Since the forward reaction is exothermic, a **low temperature**
would give a better yield — but at low temperature the reaction is far too slow,
so a compromise **optimum temperature** of about 450–500 °C is used, with a
finely divided **iron catalyst** promoted by molybdenum. Ammonia is condensed out
continuously, which pulls the equilibrium further forward.

```figure caption="Equilibrium percentage of NH₃ in the Haber process, computed from the literature values of $K_p$. High pressure and low temperature both raise the yield — exactly as Le Chatelier's principle predicts."
import numpy as np, matplotlib.pyplot as plt
def pct(Kp, P):
    # 1 mol N2 + 3 mol H2 -> 2x mol NH3; solve Kp = 4x^2(4-2x)^2 / (27(1-x)^4 P^2)
    lo, hi = 1e-9, 1-1e-9
    for _ in range(200):
        x = 0.5*(lo+hi)
        f = 4*x**2*(4-2*x)**2/(27*(1-x)**4*P**2)
        if f < Kp: lo = x
        else: hi = x
    x = 0.5*(lo+hi)
    return 100*2*x/(4-2*x)
P = np.linspace(10, 400, 300)
fig, ax = plt.subplots(figsize=(4.7,2.8))
for i, (T, Kp) in enumerate([(300, 4.34e-3), (400, 1.64e-4), (500, 1.45e-5)]):
    y = [pct(Kp, p) for p in P]
    ax.plot(P, y, color=SERIES[i], lw=1.9, label=f'{T} °C')
ax.set_xlabel('total pressure  (atm)')
ax.set_ylabel('NH₃ at equilibrium  (% by volume)')
ax.set_xlim(0, 400); ax.set_ylim(0, 80)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.5); ax.legend(title='temperature')
```

**Application 2 — Contact process.**
2SO₂(g) + O₂(g) ⇌ 2SO₃(g);  ΔH = −196 kJ mol⁻¹

Again $\Delta n = -1$ and the forward reaction is exothermic, so high pressure
and low temperature favour SO₃. In practice the equilibrium yield is already
above 95 % at 1–2 atm, so high pressure is not worth its cost; the plant runs at
400–450 °C over a **V₂O₅** catalyst with an excess of air (Le Chatelier applied
to concentration).

**Application 3 — physical equilibrium.** Ice ⇌ water is accompanied by a
*decrease* in volume, so increasing the pressure melts ice. This is why a wire
loaded at both ends cuts slowly through a block of ice — the phenomenon of
regelation.

## Chapter summary

- Chemical equilibrium is the state of a reversible reaction in a closed system
  where the forward and backward rates are equal. It is **dynamic**, reachable
  from either side, and unaffected in position by a catalyst.
- Law of mass action: rate ∝ product of active masses (molar concentrations),
  each raised to its stoichiometric coefficient.
- For aA + bB ⇌ cC + dD, $K_c = \dfrac{[C]^{c}[D]^{d}}{[A]^{a}[B]^{b}}$ and
  $K_p = \dfrac{p_C^{c}p_D^{d}}{p_A^{a}p_B^{b}}$; pure solids and pure liquids
  are omitted.
- $K_p = K_c(RT)^{\Delta n}$ with $\Delta n$ the change in gaseous moles; $K_p = K_c$
  when $\Delta n = 0$.
- $K$ measures the extent of reaction and depends **only on temperature**;
  comparing the reaction quotient $Q$ with $K$ predicts the direction of change.
- Le Chatelier: a disturbed equilibrium shifts so as to oppose the disturbance.
  High pressure favours the side with fewer gas moles; a temperature rise favours
  the endothermic direction.
- Haber: N₂ + 3H₂ ⇌ 2NH₃, ΔH = −92.4 kJ mol⁻¹, run at ≈200 atm and 450–500 °C
  over promoted iron. Contact: 2SO₂ + O₂ ⇌ 2SO₃, ΔH = −196 kJ mol⁻¹, at
  400–450 °C over V₂O₅.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. For the reaction N₂(g) + 3H₂(g) ⇌ 2NH₃(g), the relation between $K_p$ and $K_c$ is <span class="marks">[1]</span>
   (a) $K_p = K_c$ (b) $K_p = K_c RT$ (c) $K_p = K_c(RT)^{-2}$ (d) $K_p = K_c(RT)^{2}$
2. Which of the following will **not** change the position of an equilibrium? <span class="marks">[1]</span>
   (a) adding a catalyst (b) changing the temperature
   (c) changing the pressure when $\Delta n \ne 0$ (d) removing a product
3. The value of the equilibrium constant depends on <span class="marks">[1]</span>
   (a) initial concentrations (b) pressure (c) temperature (d) the catalyst used
4. In the reaction CaCO₃(s) ⇌ CaO(s) + CO₂(g), the equilibrium constant $K_c$ is <span class="marks">[1]</span>
   (a) [CaO][CO₂]/[CaCO₃] (b) [CO₂] (c) 1/[CO₂] (d) [CaO][CO₂]
5. If $Q > K_c$ for a reacting mixture, the reaction will <span class="marks">[1]</span>
   (a) go forward (b) go backward (c) already be at equilibrium (d) stop completely

::: note Answers to Group A
**1.** (c) — $\Delta n = 2 - 4 = -2$.
**2.** (a) — a catalyst speeds up both directions equally.
**3.** (c) — $K$ is a function of temperature alone.
**4.** (b) — pure solids have constant active mass and are omitted.
**5.** (b) — there is too much product, so the reverse reaction dominates until $Q$ falls to $K_c$.
:::

**Group B — Short answer (5 marks each)**

1. State the law of mass action and use it to derive the expression for the
   equilibrium constant $K_c$ of the reaction aA + bB ⇌ cC + dD. <span class="marks">[5]</span>
2. Give any five characteristics of dynamic chemical equilibrium. <span class="marks">[5]</span>
3. Derive the relationship $K_p = K_c(RT)^{\Delta n}$ and state when $K_p = K_c$. <span class="marks">[5]</span>
4. 1 mol of ethanoic acid and 1 mol of ethanol were mixed and allowed to reach
   equilibrium at 298 K. At equilibrium $2/3$ mol of ester had formed. Calculate
   $K_c$ for the esterification. <span class="marks">[5]</span>
5. For 2SO₂(g) + O₂(g) ⇌ 2SO₃(g), $K_c = 4.0\ \text{mol}^{-1}\text{L}$ at
   1000 K. Calculate $K_p$ at the same temperature. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Statement as in §8.3, then equate $k_f[A]^a[B]^b = k_r[C]^c[D]^d$ at
equilibrium and rearrange to $K_c = k_f/k_r = [C]^c[D]^d/([A]^a[B]^b)$.

**2.** Any five from §8.2: closed system; equal forward and backward rates;
reactions continue (dynamic); measurable properties constant; attainable from
either direction; catalyst does not shift it; $K$ fixed at a given temperature.

**3.** As derived in §8.5, using $p_i = [i]RT$. $K_p = K_c$ when $\Delta n = 0$.

**4.** CH₃COOH + C₂H₅OH ⇌ CH₃COOC₂H₅ + H₂O with $x = 2/3$.
Equilibrium amounts: acid $= 1/3$, alcohol $= 1/3$, ester $= 2/3$, water $= 2/3$.
Because $\Delta n = 0$, the volume $V$ cancels:

$$ K_c = \frac{(2/3)(2/3)}{(1/3)(1/3)} = \frac{4/9}{1/9} = 4 $$

**5.** $\Delta n = 2 - 3 = -1$, $T = 1000\ \text{K}$, $RT = 0.0821 \times 1000 = 82.1$.
$K_p = K_c(RT)^{-1} = 4.0/82.1 = 0.0487\ \text{atm}^{-1}$.
:::

**Group C — Long answer (8 marks each)**

1. (a) What is meant by dynamic chemical equilibrium? Distinguish it from
   physical equilibrium with one example of each. <span class="marks">[3]</span>
   (b) State Le Chatelier's principle and apply it to the manufacture of ammonia
   by the Haber process, justifying the pressure, the temperature and the use of
   a catalyst. <span class="marks">[5]</span>
2. (a) Derive $K_p = K_c(RT)^{\Delta n}$. <span class="marks">[3]</span>
   (b) 4 mol of PCl₅ were heated in a 4 L closed vessel at $250\ ^{\circ}\text{C}$.
   At equilibrium 50 % had dissociated into PCl₃ and Cl₂. Using an ICE table,
   calculate $K_c$ and $K_p$. <span class="marks">[5]</span>

::: note Answers to Group C
**1.** (a) See §8.1 and §8.2 — physical equilibrium involves only a change of
state (ice ⇌ water), chemical equilibrium forms new substances
(N₂ + 3H₂ ⇌ 2NH₃). (b) Statement of the principle, then: $\Delta n = -2$ so
high pressure (200 atm) increases the yield; the forward reaction is exothermic
(ΔH = −92.4 kJ mol⁻¹) so a low temperature increases the yield but lowers the
rate, hence the compromise at 450–500 °C; the iron catalyst does not change the
yield, only the time taken to reach it.

**2(b).** Dissociated $= 0.50 \times 4 = 2\ \text{mol}$.

| | PCl₅ | PCl₃ | Cl₂ |
|---|---|---|---|
| Initial (mol) | 4 | 0 | 0 |
| Change (mol) | −2 | +2 | +2 |
| Equilibrium (mol) | 2 | 2 | 2 |

Dividing by 4 L: $[PCl_5] = [PCl_3] = [Cl_2] = 0.5\ \text{mol L}^{-1}$.

$$ K_c = \frac{(0.5)(0.5)}{0.5} = 0.5\ \text{mol L}^{-1} $$

With $\Delta n = +1$ and $T = 523\ \text{K}$,
$K_p = 0.5 \times 0.0821 \times 523 = 21.5\ \text{atm}$.
:::
