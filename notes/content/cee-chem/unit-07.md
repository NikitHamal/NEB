---
subject: Chemistry
grade: CEE
unit: 7
title: Chemical and Ionic Equilibrium
hours: 2
area: Physical Chemistry
---

Equilibrium is the chapter that joins the arithmetic of Unit 1 to the acid–base and
solubility work of the rest of the paper. It carries about **two questions** (our estimate
from the MEC topic list), and they come in four shapes: a Kc or Kp calculation from
equilibrium concentrations, a "which way does it shift" question on Le Chatelier, a pH or
pKa one-liner, and a buffer, hydrolysis or Ksp judgement. Almost every question is decided
by one of two sentences — *the equilibrium constant changes only with temperature* and
*compare the ionic product with Ksp* — so learn those two properly and the rest is
arithmetic.

::: key What the paper asks from this chapter
- Equilibrium is **dynamic**: at equilibrium the forward and reverse rates are equal and the concentrations stay constant, but both reactions continue.
- $K_c$ and $K_p$ from the balanced equation, products over reactants, each raised to its coefficient; **pure solids and pure liquids never appear** in the expression.
- $K_p = K_c(RT)^{\Delta n}$, with $\Delta n$ = (moles of gaseous products) − (moles of gaseous reactants). $\Delta n = 0$ makes $K_p = K_c$, and both are then dimensionless.
- $Q$ vs $K$: $Q < K$ shifts forward, $Q > K$ shifts backward, $Q = K$ is equilibrium.
- Le Chatelier: concentration, pressure (only if $\Delta n \neq 0$) and temperature; a **catalyst never shifts** an equilibrium and never changes $K$.
- Definitions: Arrhenius (H⁺/OH⁻), Brønsted–Lowry (proton donor/acceptor, conjugate pairs), Lewis (electron-pair acceptor/donor); Ostwald's dilution law $\alpha = \sqrt{K_a/C}$.
- $K_w = 10^{-14}$ at 25 °C, $\text{pH} + \text{pOH} = 14$, $\text{p}K_a + \text{p}K_b = 14$; the log arithmetic for pH without a calculator.
- Buffer: $\text{pH} = \text{p}K_a + \log\frac{[\text{salt}]}{[\text{acid}]}$; the four salt types and which gives pH < 7, = 7, > 7.
- $K_{sp}$: precipitation starts when the ionic product exceeds $K_{sp}$; for AB, $s = \sqrt{K_{sp}}$, for AB₂, $K_{sp} = 4s^3$.
:::

## 7.1 Physical and chemical equilibrium; law of mass action; Kc, Kp and Q

### Reversible reactions and dynamic equilibrium

A **reversible reaction** can go in both directions under the same conditions; it is
written with a double arrow, ⇌. Nothing is ever "finished": as soon as products appear
they begin to react back. A **irreversible** reaction, written with a single arrow, runs
to completion — Ag⁺ + Cl⁻ → AgCl(s) in a test tube, or the burning of methane.

::: definition Dynamic equilibrium
A system is at **dynamic equilibrium** when the rate of the forward reaction equals the
rate of the reverse reaction, so that the concentrations of all species remain constant
with time, although both reactions are still taking place.
:::

Three ideas in that sentence carry marks. **Equal rates**, not equal concentrations.
**Constant concentrations**, not zero rates. **Closed system** — if a product escapes, as
CO₂ does from an open flask of limestone, the reverse reaction cannot keep up and the
"equilibrium" is never reached.

| Feature | What it means |
|---|---|
| Rates | $r_{\text{forward}} = r_{\text{reverse}}$ (not zero) |
| Concentrations | constant in time, but generally **not** equal to each other |
| Starting point | the same equilibrium position is reached whether you start from reactants or from products |
| Catalyst | equilibrium is reached **faster**, at the same position |
| Nature | dynamic, not static — measurable by isotopic labelling (H₂ + D₂ ⇌ 2HD) |

```figure caption="Approach to equilibrium for a reaction whose forward and reverse rates become equal. The rates converge; after that point the concentrations no longer change, although both reactions continue."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.9))
t = np.linspace(0, 8, 400)
A = 0.5*(1 + np.exp(-1.8*t))      # fraction as A, starts at 1, ends at 0.5
B = 1 - A
ax.plot(t, A, color=ACCENT, lw=2.1, label='forward rate  $k_f[A]$')
ax.plot(t, B, color=SERIES[1], lw=2.1, label='reverse rate  $k_r[B]$')
ax.axhline(0.5, color=MUTED, lw=0.9, ls=':')
ax.annotate('rates equal here:\nequilibrium reached', xy=(2.6, 0.5), xytext=(3.3, 0.78),
            fontsize=8.8, color=INK,
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.9, mutation_scale=9))
ax.text(6.9, 0.42, 'concentrations\nnow constant', ha='right', va='top', fontsize=8.6, color=MUTED)
ax.set_xlabel('time')
ax.set_ylabel('rate (arbitrary units)')
ax.set_xlim(0, 8); ax.set_ylim(0, 1.08)
ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=0.45)
ax.legend(loc='center right', fontsize=8.4, frameon=False)
```

The **law of chemical equilibrium** follows: at a fixed temperature, for

$$ aA + bB \rightleftharpoons cC + dD $$

the ratio $\frac{[C]^c[D]^d}{[A]^a[B]^b}$ is constant at equilibrium. That constant is
$K_c$, the **equilibrium constant in terms of concentration**.

### The law of mass action

::: definition Law of mass action (Guldberg and Waage, 1864)
The rate of a chemical reaction is proportional to the product of the **active masses**
(molar concentrations) of the reactants, each raised to the power of its stoichiometric
coefficient.
:::

Applied to the forward and reverse reactions separately and then equated at equilibrium,
the law gives the equilibrium constant:

$$ K_c = \frac{[C]^c[D]^d}{[A]^a[B]^b} \qquad K_p = \frac{p_C^{\,c}\,p_D^{\,d}}{p_A^{\,a}\,p_B^{\,b}} $$

where square brackets mean mol L⁻¹ and $p$ means partial pressure (usually in atm).
$K_p$ is used for gas reactions because partial pressures are what a pressure change
actually alters.

| Rule for writing any $K$ | Example |
|---|---|
| products on top, reactants below | N₂ + 3H₂ ⇌ 2NH₃ gives $K_c = \frac{[\text{NH}_3]^2}{[\text{N}_2][\text{H}_2]^3}$ |
| each concentration raised to its coefficient | the 3 on H₂ becomes a cube, not a factor of 3 |
| omit pure solids and pure liquids | CaCO₃(s) ⇌ CaO(s) + CO₂(g) gives $K_p = p_{\text{CO}_2}$ only |
| omit the solvent in a dilute solution | water is left out of the esterification constant |
| the reverse reaction has $1/K$ | if $K = 49$ for H₂ + I₂ ⇌ 2HI, then $K = 1/49$ for 2HI ⇌ H₂ + I₂ |
| doubling the equation squares $K$ | 2H₂ + 2I₂ ⇌ 4HI has $K = 49^2 = 2401$ |

::: caution Why solids and liquids are left out
The "concentration" of a pure solid or a pure liquid is its density divided by its molar
mass — a fixed number at a given temperature. It is constant, so it is folded into $K$.
That is why a heap of CaCO₃ and a heap of CaO of any size give the same $K_p$: only
$p_{\text{CO}_2}$ appears. Writing $[\text{CaCO}_3]$ in the expression is one of the most
common wrong options in the paper.
:::

### The relation between Kp and Kc

::: derivation $K_p = K_c(RT)^{\Delta n}$
We start from the ideal-gas law and substitute $p = (n/V)RT = cRT$ for every gas.

**Setting up.** For $aA + bB \rightleftharpoons cC + dD$, all species gaseous, let
$\Delta n = (c + d) - (a + b)$, counting gases only.

**Step 1 — replace each partial pressure.** $p_C = [C]RT$, and likewise for the others.

**Step 2 — substitute into $K_p$.**
$$ K_p = \frac{([C]RT)^c([D]RT)^d}{([A]RT)^a([B]RT)^b} $$

**Step 3 — collect the powers of $RT$.**
$$ K_p = \frac{[C]^c[D]^d}{[A]^a[B]^b} \times (RT)^{(c+d)-(a+b)} $$

**Step 4 — recognise $K_c$.**
$$ K_p = K_c(RT)^{\Delta n} $$

**Result.** $K_p = K_c(RT)^{\Delta n}$, with $R = 0.0821\ \text{L atm mol}^{-1}\text{K}^{-1}$
when pressures are in atm, and $T$ in kelvin.

**What it means.** The two constants differ only by the pressure–concentration conversion
for the *change* in the number of gas molecules. If the reaction produces as many gas
molecules as it consumes, $\Delta n = 0$, $(RT)^0 = 1$, and $K_p = K_c$ exactly.
:::

| Reaction | $\Delta n$ | $K_p$ in terms of $K_c$ | Units of $K_c$ | Units of $K_p$ |
|---|---|---|---|---|
| N₂ + 3H₂ ⇌ 2NH₃ | 2 − 4 = −2 | $K_c(RT)^{-2}$ | L² mol⁻² | atm⁻² |
| PCl₅ ⇌ PCl₃ + Cl₂ | 2 − 1 = +1 | $K_c(RT)$ | mol L⁻¹ | atm |
| H₂ + I₂ ⇌ 2HI | 2 − 2 = 0 | $K_c$ | none | none |
| N₂O₄ ⇌ 2NO₂ | +1 | $K_c(RT)$ | mol L⁻¹ | atm |
| CaCO₃(s) ⇌ CaO(s) + CO₂(g) | 1 − 0 = +1 | $K_c(RT)$ | mol L⁻¹ | atm |

::: caution The units question
The unit of $K_c$ is $(\text{mol L}^{-1})^{\Delta n}$ and of $K_p$ is $(\text{atm})^{\Delta n}$.
So for N₂ + 3H₂ ⇌ 2NH₃, $\Delta n = -2$ and the unit is
$(\text{mol L}^{-1})^{-2} = \text{L}^2\text{mol}^{-2}$. When $\Delta n = 0$ the constant is
**dimensionless** — a favourite one-mark question. A "unitless" answer is wrong for
PCl₅ ⇌ PCl₃ + Cl₂ and right for H₂ + I₂ ⇌ 2HI.
:::

::: example Kc from equilibrium concentrations, then Kp
**Problem.** At 500 K, 1.0 mol of N₂ and 3.0 mol of H₂ are sealed in a 1.0 L vessel. At
equilibrium the vessel contains 1.0 mol N₂, 2.0 mol H₂ and 4.0 mol NH₃. Find $K_c$ and
$K_p$ ($R = 0.0821$ L atm mol⁻¹ K⁻¹).

**Solution.** All volumes are 1.0 L, so moles = concentrations.
$K_c = \dfrac{[\text{NH}_3]^2}{[\text{N}_2][\text{H}_2]^3} = \dfrac{4.0^2}{1.0 \times 2.0^3}
= \dfrac{16}{8} = 2.0$, unit L² mol⁻².
$\Delta n = 2 - 4 = -2$, so $K_p = K_c(RT)^{-2} = 2.0 \times (0.0821 \times 500)^{-2}
= 2.0 \times (41.05)^{-2} = 1.19 \times 10^{-3}$ atm⁻².
:::

### The reaction quotient Q and the direction of shift

$Q$ is the same fraction as $K$ but built from concentrations **at any moment**, not
necessarily at equilibrium. Comparing the two tells you which way the reaction must go.

| Comparison | Meaning | What happens |
|---|---|---|
| $Q < K$ | too little product, too much reactant | reaction goes **forward** (to the right) |
| $Q > K$ | too much product | reaction goes **backward** (to the left) |
| $Q = K$ | the ratio already has the equilibrium value | the system is at equilibrium |

::: example Deciding the direction from Q
**Problem.** For H₂ + I₂ ⇌ 2HI, $K_c = 49$ at 700 K. A mixture contains
[H₂] = 1.0, [I₂] = 1.0 and [HI] = 2.0 mol L⁻¹. Which way does the reaction go?

**Solution.** $Q = \dfrac{[\text{HI}]^2}{[\text{H}_2][\text{I}_2]} = \dfrac{2.0^2}{1.0 \times 1.0} = 4.0$.
$Q < K$ (4 < 49), so the reaction proceeds **forward**, making more HI until $Q$ rises to 49.
:::

### What does and does not change K

$K$ is a **constant at a given temperature** and nothing else. This one sentence answers
a large share of the objective questions on the chapter.

| Change | Effect on $K$ | Effect on the position |
|---|---|---|
| temperature | **changes** (increases for endothermic, decreases for exothermic) | shifts |
| adding or removing a reactant or product | none | shifts to restore $Q = K$ |
| changing pressure or volume | none | shifts only if $\Delta n \neq 0$ |
| adding a catalyst | **none** | none — equilibrium arrives sooner |
| adding an inert gas at constant volume | none | none |
| changing the surface area of a solid | none | none |

::: tip Reading a "K changes?" question
Underline the word *constant*. If the only change is concentration, pressure, volume,
catalyst or surface area, $K$ does not move — only the position does. Temperature is the
sole entry in the left-hand column that changes $K$.
:::

## 7.2 Le Chatelier's principle and its applications

::: definition Le Chatelier's principle (1884)
If a system at equilibrium is disturbed by a change in concentration, pressure or
temperature, the system shifts in the direction that tends to **oppose** the change and
so establishes a new equilibrium.
:::

| Disturbance | Shift | Reason |
|---|---|---|
| add a reactant | forward | uses up the added substance |
| remove a product | forward | replaces what was taken away |
| add a product | backward | removes the added product |
| increase pressure (reduce volume) | towards the side with **fewer gas molecules** | fewer molecules occupy less space |
| decrease pressure | towards **more gas molecules** | |
| increase temperature | in the **endothermic** direction | absorbs the extra heat |
| decrease temperature | in the **exothermic** direction | releases heat |
| add catalyst | **no shift** | forward and reverse rates rise equally |

Two cases where students lose the mark:

- **$\Delta n = 0$.** In H₂ + I₂ ⇌ 2HI there are two gas molecules on each side, so
  squeezing the mixture changes both partial pressures equally and the position does not
  move at all. Pressure has *no* effect.
- **Inert gas.** Added at **constant volume**, it does not change any partial pressure and
  there is no shift. Added at **constant pressure** the vessel must expand, every partial
  pressure falls, and the equilibrium shifts towards the side with **more** gas molecules
  — exactly as if the pressure had been lowered.

```figure caption="A disturbance in the N₂O₄ ⇌ 2NO₂ equilibrium. Extra NO₂ is injected at the dashed line: its concentration jumps at once, then part of it dimerises until the original value of $K_c$ is restored."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9,2.9))
t1 = np.linspace(0, 5, 200); t2 = np.linspace(5, 12, 300)
# before injection: equilibrium N2O4 = 0.60, NO2 = 0.80 (Kc = 0.64/0.60)
n2o4_a = 0.60 - 0.40*np.exp(-0.9*t1)
no2_a  = 0.80 + 0.80*np.exp(-0.9*t1)
ax.plot(t1, n2o4_a, color=ACCENT, lw=2.0)
ax.plot(t1, no2_a, color=SERIES[1], lw=2.0)
# after injection: NO2 jumps to 1.20, then relaxes to 0.896; N2O4 0.60 -> 0.752
n2o4_b = 0.752 - 0.152*np.exp(-1.1*(t2-5))
no2_b  = 0.896 + 0.304*np.exp(-1.1*(t2-5))
ax.plot(t2, n2o4_b, color=ACCENT, lw=2.0)
ax.plot(t2, no2_b, color=SERIES[1], lw=2.0)
ax.plot([5,5], [0.0, 1.28], color=MUTED, lw=1.0, ls='--')
ax.annotate('NO₂ added', xy=(5, 1.22), xytext=(5.4, 1.30), fontsize=8.8, color=INK)
ax.text(0.3, 0.66, 'N₂O₄', color=ACCENT, fontsize=9.2)
ax.text(0.3, 0.86, 'NO₂', color=SERIES[1], fontsize=9.2)
ax.annotate('new equilibrium:\nKc is the same', xy=(9.6, 0.90), xytext=(6.2, 0.34),
            fontsize=8.6, color=MUTED,
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.8, mutation_scale=9))
ax.set_xlabel('time')
ax.set_ylabel('concentration (mol L⁻¹)')
ax.set_xlim(0, 12); ax.set_ylim(0, 1.4)
ax.set_xticks([0, 2, 4, 6, 8, 10, 12])
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=0.45)
```

### The Haber process

$$ \text{N}_2(g) + 3\text{H}_2(g) \rightleftharpoons 2\text{NH}_3(g) \qquad \Delta H = -92\ \text{kJ mol}^{-1} $$

| Factor | Effect on yield of NH₃ | What the industry does |
|---|---|---|
| pressure | 4 mol gas → 2 mol gas, so **high pressure** favours NH₃ | about 200 atm |
| temperature | exothermic, so **low temperature** favours NH₃ | about 700 K (430 °C) |
| catalyst | no effect on yield, large effect on rate | iron with K₂O and Al₂O₃ promoters |
| removal of NH₃ | shifts forward | cool and condense the ammonia, recycle the rest |

**Why a compromise temperature?** At 300 K the equilibrium yield at 200 atm is very high
but the reaction is so slow that the plant would produce almost nothing. At 900 K the rate
is excellent but the equilibrium has moved back towards nitrogen and hydrogen. The
catalyst only works efficiently above about 650 K. The operating temperature of about
700 K is therefore the point where a *usable* rate and a *worthwhile* yield meet — a
compromise, not an optimum of either quantity alone. Increasing the pressure shifts the
equilibrium the right way and also raises the collision rate, which is why pressure is
pushed as high as the plant's steel allows.

```figure caption="Why the Haber process uses a compromise temperature. The equilibrium amount of ammonia falls as the temperature rises, while the rate climbs steeply. The shaded band is the practical window, near 700 K at about 200 atm."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9,3.0))
T = np.linspace(450, 1000, 300)
# equilibrium mole % NH3: van't Hoff from K(298) = 5.9e5 atm^-2, dH = -92 kJ/mol, P = 200 atm
lnK = np.log(5.9e5) + (92000/8.314)*(1/T - 1/298.15)
K = np.exp(lnK)
P = 200.0
eps = np.linspace(1e-6, 0.9999, 6000)
nN, nH, nA = 1-eps, 3-3*eps, 2*eps
tot = 4-2*eps
Kp_curve = ((nA/tot)*P)**2 / (((nN/tot)*P) * ((nH/tot)*P)**3)
yield_pct = []
for kk in K:
    i = np.argmin(np.abs(Kp_curve - kk))
    yield_pct.append(100*nA[i]/tot[i])
yield_pct = np.array(yield_pct)
rate = 100*np.exp(-2454*(1/T - 1/1000.0))
ax.plot(T, yield_pct, color=ACCENT, lw=2.2, label='equilibrium NH₃ (per cent)')
ax.plot(T, rate, color=SERIES[1], lw=1.9, ls='--', label='relative rate of reaction')
ax.axvspan(660, 760, color='#f0d9c8', alpha=0.7, zorder=0)
ax.text(710, 102, 'compromise\n≈ 700 K', ha='center', va='top', fontsize=8.8, color=INK)
ax.set_xlabel('temperature (K)')
ax.set_ylabel('per cent / relative units')
ax.set_xlim(450, 1000); ax.set_ylim(0, 105)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=0.45)
ax.legend(loc='lower left', fontsize=8.2, frameon=False)
```

### The contact process

$$ 2\text{SO}_2(g) + \text{O}_2(g) \rightleftharpoons 2\text{SO}_3(g) \qquad \Delta H = -197\ \text{kJ mol}^{-1} $$

Three gas molecules become two, and the reaction is exothermic, so **high pressure and low
temperature** both favour SO₃. Again the rate sets the limit: the plant runs at about
**720 K (450 °C)** and 1–2 atm over a **V₂O₅** catalyst, with the SO₃ absorbed in
concentrated H₂SO₄ as it forms so that it cannot react back. The yield is about 98 %.

<div style="break-before:page"></div>

### The Ostwald process

$$ 4\text{NH}_3(g) + 5\text{O}_2(g) \rightleftharpoons 4\text{NO}(g) + 6\text{H}_2\text{O}(g) \qquad \Delta H = -905\ \text{kJ mol}^{-1} $$

Here 9 gas molecules become 10, so a rise in pressure shifts the equilibrium *backwards* —
pressure is **not** a lever for yield in this step. It is still run at about 9 atm because
the higher pressure raises the collision rate and the throughput, and because the
equilibrium lies so far to the right at 800–900 K that the yield is nearly complete. The
real difficulty is **selectivity**: too high a temperature decomposes NH₃ and carries the
oxidation on to N₂. Hence a platinum–rhodium gauze at about **800 K**, a contact time of
about a millisecond, and rapid cooling of the gases.

::: caution Catalyst, yield and K
A catalyst lowers the activation energy of *both* directions by the same amount. It
therefore does not change $\Delta H$, does not change $K$, and does not change the
equilibrium yield — it only shortens the time needed to reach it. Every option that says
"the catalyst increases the yield of ammonia" is wrong for that reason.
:::

::: example Using Le Chatelier on a real equilibrium
**Problem.** For 2SO₂ + O₂ ⇌ 2SO₃, ΔH = −197 kJ, state the effect on the amount of SO₃ of
(a) raising the temperature, (b) compressing the mixture, (c) adding V₂O₅, (d) removing SO₃.

**Solution.** (a) The forward reaction is exothermic, so heat is a product; raising the
temperature shifts the equilibrium **backward** and SO₃ **falls**. (b) 3 mol gas → 2 mol
gas, so compression shifts **forward** and SO₃ **rises**. (c) No effect on the amount —
equilibrium is reached sooner only. (d) Removing a product shifts the equilibrium
**forward**, so more SO₃ forms (and the yield of the step rises).
:::
## 7.3 Arrhenius, Brønsted–Lowry and Lewis acids and bases; Ostwald's dilution law

### The three definitions

| Theory | Acid | Base | Example that only this theory explains |
|---|---|---|---|
| **Arrhenius** (1884) | gives H⁺ ions in water | gives OH⁻ ions in water | HCl and NaOH in water |
| **Brønsted–Lowry** (1923) | **proton (H⁺) donor** | **proton acceptor** | NH₃ is a base although it contains no OH |
| **Lewis** (1923) | **electron-pair acceptor** | **electron-pair donor** | BF₃ + NH₃, with no proton transferred at all |

Each theory widens the one before. Arrhenius cannot call NH₃ a base (it has no OH
group) and cannot handle reactions in solvents other than water. Brønsted–Lowry handles
NH₃ and all proton transfers, but cannot explain why BF₃ and AlCl₃ behave as acids.
Lewis covers those, at the cost of calling every cation and every electron-pair-deficient
molecule an acid.

::: definition Brønsted–Lowry acid and base
An **acid** is a species that donates a proton; a **base** is a species that accepts a
proton. Every acid has a **conjugate base**, formed by losing one H⁺, and every base has
a **conjugate acid**, formed by gaining one H⁺.
:::

| Acid | Conjugate base | Base | Conjugate acid |
|---|---|---|---|
| HCl | Cl⁻ | NH₃ | NH₄⁺ |
| CH₃COOH | CH₃COO⁻ | OH⁻ | H₂O |
| H₂O | OH⁻ | H₂O | H₃O⁺ |
| HCO₃⁻ | CO₃²⁻ | HCO₃⁻ | H₂CO₃ |
| NH₄⁺ | NH₃ | CH₃COO⁻ | CH₃COOH |
| HSO₄⁻ | SO₄²⁻ | HSO₄⁻ | H₂SO₄ |

A species that can both donate and accept a proton is **amphiprotic** — water, HCO₃⁻,
HSO₄⁻, H₂PO₄⁻ and the amino acids are the standard examples. Notice in the table that
water appears twice: it is the base when it accepts a proton from HCl, and the acid when
it donates one to NH₃.

The stronger the acid, the weaker its conjugate base. HCl is a strong acid, so Cl⁻ is a
negligible base (which is why NaCl solutions are neutral); CH₃COOH is weak, so CH₃COO⁻ is
a real base (which is why sodium acetate solutions are alkaline).

### Strong and weak electrolytes

::: definition Degree of dissociation
The **degree of dissociation** $\alpha$ is the fraction of the dissolved molecules that
have split into ions: $\alpha = \dfrac{\text{moles dissociated}}{\text{moles dissolved}}$.
A **strong** electrolyte is almost completely dissociated ($\alpha \approx 1$); a **weak**
electrolyte is only slightly dissociated ($\alpha \ll 1$).
:::

| | Strong electrolyte | Weak electrolyte |
|---|---|---|
| $\alpha$ | close to 1 (0.9–1) | small (0.01–0.1) |
| Arrow | single → | double ⇌ |
| Examples (acids) | HCl, HBr, HI, HNO₃, H₂SO₄, HClO₄ | CH₃COOH, H₂CO₃, HCN, H₃PO₄, HF |
| Examples (bases) | NaOH, KOH, Ca(OH)₂, Ba(OH)₂ | NH₃, amines, Mg(OH)₂ |
| Examples (salts) | NaCl, KNO₃, NH₄Cl (all soluble salts) | — (salts are strong electrolytes) |
| Conductivity | high | low, but rises on dilution |

### Ostwald's dilution law

::: derivation Ostwald's dilution law
We start from the equilibrium of a weak monobasic acid and the definition of $\alpha$.

**Setting up.** Let $C$ mol L⁻¹ of HA be dissolved; a fraction $\alpha$ dissociates.
$$ \text{HA} \rightleftharpoons \text{H}^+ + \text{A}^- $$

**Step 1 — concentrations at equilibrium.** HA left $= C(1-\alpha)$;
$[\text{H}^+] = [\text{A}^-] = C\alpha$.

**Step 2 — write $K_a$.**
$$ K_a = \frac{[\text{H}^+][\text{A}^-]}{[\text{HA}]} = \frac{(C\alpha)(C\alpha)}{C(1-\alpha)} = \frac{C\alpha^2}{1-\alpha} $$

**Step 3 — use the weakness.** For a weak electrolyte $\alpha \ll 1$, so $1-\alpha \approx 1$:
$$ K_a = C\alpha^2 \quad\Longrightarrow\quad \alpha = \sqrt{\frac{K_a}{C}} $$

**Result.** $\alpha = \sqrt{K_a/C}$ for a weak acid, and $\alpha = \sqrt{K_b/C}$ for a weak
base. The law holds only for weak binary electrolytes in dilute solution; it fails for
strong electrolytes, where $\alpha$ is near 1 and $1-\alpha$ cannot be dropped.

**What it means.** $\alpha$ is **inversely proportional to the square root of the
concentration**: diluting a weak acid increases the fraction dissociated.
:::

::: caution Dilution raises α but lowers [H⁺]
These two statements look contradictory and examiners exploit the confusion. As $C$ falls,
$\alpha = \sqrt{K_a/C}$ **rises**, but the actual hydrogen-ion concentration
$[\text{H}^+] = C\alpha = \sqrt{K_aC}$ **falls**, because $C$ falls faster than $\alpha$
rises. So a dilute weak acid is *more dissociated* and *less acidic* at the same time.
For acetic acid, $K_a = 1.8 \times 10^{-5}$: at 0.1 M, $\alpha = 1.3\%$ and
$[\text{H}^+] = 1.3 \times 10^{-3}$ M; at 0.001 M, $\alpha = 13.4\%$ but
$[\text{H}^+] = 1.3 \times 10^{-4}$ M — ten times weaker.
:::

::: example Degree of dissociation and Ka
**Problem.** A 0.10 M solution of a weak monobasic acid has pH 2.87. Find $\alpha$ and $K_a$.

**Solution.** $[\text{H}^+] = 10^{-2.87} = 1.35 \times 10^{-3}$ M.
$\alpha = [\text{H}^+]/C = 1.35 \times 10^{-3}/0.10 = 1.35 \times 10^{-2}$ (1.35 %).
$K_a = C\alpha^2 = 0.10 \times (1.35 \times 10^{-2})^2 = 1.8 \times 10^{-5}$.
(Check with the shortcut: $\alpha = \sqrt{1.8\times10^{-5}/0.1} = 1.34\%$.)
:::

## 7.4 Ionic product of water, pH, pOH, pKa, pKb; common-ion effect; solubility product

### The ionic product of water

Water dissociates very slightly:

$$ \text{H}_2\text{O} \rightleftharpoons \text{H}^+ + \text{OH}^- $$

$$ K_w = [\text{H}^+][\text{OH}^-] = 1.0 \times 10^{-14} \ \text{at 25 °C} $$

$K_w$ is the **ionic product of water**. Because dissociation absorbs heat, $K_w$
**increases with temperature** — about $5.5 \times 10^{-13}$ at 100 °C. Pure water is
always electrically neutral, so $[\text{H}^+] = [\text{OH}^-] = 10^{-7}$ M at 25 °C and
pH 7. At 100 °C neutral water has pH ≈ 6.13: **pH 7 means neutral only at 25 °C.**

### pH, pOH, pKa and pKb

$$ \text{pH} = -\log[\text{H}^+] \qquad \text{pOH} = -\log[\text{OH}^-] \qquad \text{pH} + \text{pOH} = 14\ (25\ ^\circ\text{C}) $$

$$ \text{p}K_a = -\log K_a \qquad \text{p}K_b = -\log K_b \qquad \text{p}K_a + \text{p}K_b = 14\ \text{for a conjugate pair} $$

| Solution | $[\text{H}^+]$ | pH | Working |
|---|---|---|---|
| 0.01 M HCl | $10^{-2}$ | 2.00 | strong acid, fully ionised |
| 0.01 M NaOH | $10^{-12}$ | 12.00 | pOH = 2, so pH = 14 − 2 |
| $2 \times 10^{-3}$ M HCl | $2 \times 10^{-3}$ | 2.70 | 3 − log 2 = 3 − 0.30 |
| $5 \times 10^{-5}$ M HCl | $5 \times 10^{-5}$ | 4.30 | 5 − log 5 = 5 − 0.70 |
| 0.1 M CH₃COOH | $1.34 \times 10^{-3}$ | 2.87 | $\tfrac{1}{2}(\text{p}K_a - \log C)$ |
| 0.1 M NH₃ | $1.34 \times 10^{-3}$ (OH⁻) | 11.13 | pOH = 2.87, pH = 14 − 2.87 |

::: tip Log arithmetic without a calculator
Learn four logarithms and you can do every pH question in the paper by hand:
$\log 2 = 0.30$, $\log 3 = 0.48$, $\log 5 = 0.70$, $\log 7 = 0.85$.
To take a pH, write the concentration as (a number between 1 and 10) × 10⁻ⁿ: the pH is
$n - \log(\text{that number})$. So $[\text{H}^+] = 4 \times 10^{-4}$ gives
pH = 4 − 0.60 = 3.40. Going the other way, pH 5.3 means $[\text{H}^+] = 10^{-5.3}
= 10^{-6} \times 10^{0.7} = 5 \times 10^{-6}$ M. For a weak acid use
$\text{pH} = \tfrac{1}{2}(\text{p}K_a - \log C)$; for its salt,
$\text{pH} = 7 + \tfrac{1}{2}(\text{p}K_a + \log C)$.
:::

```figure caption="The pH scale is logarithmic: one pH unit is a tenfold change in hydrogen-ion concentration. Values above 7 are basic only at 25 °C."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
fig, ax = plt.subplots(figsize=(5.0,2.8))
cmap = LinearSegmentedColormap.from_list('ph', ['#b03a2e','#e67e22','#f4d03f','#27ae60','#2e86c1','#6c3483'])
ax.imshow(np.linspace(0,1,600).reshape(1,-1), extent=[0,14,0,1], aspect='auto', cmap=cmap, zorder=1)
ax.set_xlim(-0.4, 14.4); ax.set_ylim(-1.3, 3.3)
ax.set_yticks([])
ax.set_xticks(range(0,15))
ax.set_xlabel('pH')
for s in ax.spines.values():
    s.set_visible(False)
ax.text(3.0, -0.55, 'acidic', ha='center', fontsize=9.2, color=INK)
ax.text(7.0, -0.55, 'neutral', ha='center', fontsize=9.2, color=INK)
ax.text(11.0, -0.55, 'basic', ha='center', fontsize=9.2, color=INK)
for xph, xtxt, y, txt in [(2.3, 2.3, 1.35, 'lemon  2.3'), (6.5, 5.0, 2.45, 'milk  6.5'),
                          (7.4, 8.8, 2.45, 'blood  7.4'), (10.0, 10.0, 1.35, 'soap  10')]:
    ax.plot([xph, xtxt], [1.05, y - 0.06], color=MUTED, lw=0.8)
    ax.text(xtxt, y, txt, ha='center', va='bottom', fontsize=8.8, color=INK)
ax.text(-0.3, 3.1, 'one unit = tenfold change in [H⁺]', fontsize=8.4, color=MUTED)
```

### The common-ion effect

::: definition Common-ion effect
The **common-ion effect** is the suppression of the ionisation of a weak electrolyte by
the addition of a strong electrolyte that supplies one of the same ions.
:::

Add sodium acetate to acetic acid. The acetate ion is already the product of the acid's
ionisation, so by Le Chatelier the equilibrium is driven back to the left:

$$ \text{CH}_3\text{COOH} \rightleftharpoons \text{CH}_3\text{COO}^- + \text{H}^+ $$

The result: $\alpha$ falls, $[\text{H}^+]$ falls, and the pH **rises**. The same idea
lowers the solubility of a sparingly soluble salt in a solution containing one of its
ions, and it is the reason a buffer works.

::: example Common ion, by the Ka expression
**Problem.** Find the pH of a solution that is 0.10 M in CH₃COOH and 0.10 M in CH₃COONa
($K_a = 1.8 \times 10^{-5}$).

**Solution.** The salt is fully ionised, so $[\text{CH}_3\text{COO}^-] \approx 0.10$ M.
Let $x = [\text{H}^+]$. Then $K_a = \dfrac{x(0.10 + x)}{0.10 - x} \approx \dfrac{x \times 0.10}{0.10}$,
so $x = K_a = 1.8 \times 10^{-5}$ M and pH = 4.74.
Compare pure 0.10 M acetic acid: pH 2.87. The common ion has raised the pH by nearly two
units — the acid is now only 0.018 % ionised.
:::

### Solubility product and precipitation

For a sparingly soluble salt in contact with its saturated solution,

$$ \text{AgCl}(s) \rightleftharpoons \text{Ag}^+ + \text{Cl}^- \qquad K_{sp} = [\text{Ag}^+][\text{Cl}^-] $$

::: definition Solubility product
The **solubility product** $K_{sp}$ is the product of the molar concentrations of the ions
in a **saturated** solution, each raised to the power of its coefficient in the
dissociation equation, at a given temperature. It is an equilibrium constant, so it
depends only on temperature.
:::

| Salt | Dissociation | $K_{sp}$ expression | $K_{sp}$ at 25 °C |
|---|---|---|---|
| AgCl | AgCl(s) ⇌ Ag⁺ + Cl⁻ | $[\text{Ag}^+][\text{Cl}^-]$ | $1.8 \times 10^{-10}$ |
| AgBr | AgBr(s) ⇌ Ag⁺ + Br⁻ | $[\text{Ag}^+][\text{Br}^-]$ | $5.0 \times 10^{-13}$ |
| AgI | AgI(s) ⇌ Ag⁺ + I⁻ | $[\text{Ag}^+][\text{I}^-]$ | $8.3 \times 10^{-17}$ |
| BaSO₄ | BaSO₄(s) ⇌ Ba²⁺ + SO₄²⁻ | $[\text{Ba}^{2+}][\text{SO}_4^{2-}]$ | $1.1 \times 10^{-10}$ |
| PbCl₂ | PbCl₂(s) ⇌ Pb²⁺ + 2Cl⁻ | $[\text{Pb}^{2+}][\text{Cl}^-]^2$ | $1.6 \times 10^{-5}$ |
| CaF₂ | CaF₂(s) ⇌ Ca²⁺ + 2F⁻ | $[\text{Ca}^{2+}][\text{F}^-]^2$ | $4.0 \times 10^{-11}$ |

**The ionic product test.** Calculate the ionic product $Q_{sp}$ exactly as you would
$K_{sp}$, but from the concentrations actually present:

| | Meaning | Result |
|---|---|---|
| $Q_{sp} < K_{sp}$ | unsaturated | no precipitate; more solid would dissolve |
| $Q_{sp} = K_{sp}$ | saturated | at the point of precipitation |
| $Q_{sp} > K_{sp}$ | supersaturated | **precipitate forms** until $Q_{sp}$ falls to $K_{sp}$ |

**Solubility from $K_{sp}$.** Let the solubility be $s$ mol L⁻¹.

| Type | Example | $K_{sp}$ | Solubility |
|---|---|---|---|
| AB | AgCl | $s^2$ | $s = \sqrt{K_{sp}}$ |
| AB₂ or A₂B | PbCl₂, Ag₂CrO₄ | $4s^3$ | $s = \sqrt[3]{K_{sp}/4}$ |
| AB₃ | Fe(OH)₃ | $27s^4$ | $s = \sqrt[4]{K_{sp}/27}$ |

::: example Solubility of AgCl, and the common-ion effect on it
**Problem.** $K_{sp}(\text{AgCl}) = 1.8 \times 10^{-10}$. Find its solubility in (a) pure
water and (b) 0.010 M NaCl. ($M_{\text{AgCl}} = 143.5$)

**Solution.** (a) $s = \sqrt{1.8 \times 10^{-10}} = 1.34 \times 10^{-5}$ mol L⁻¹, which is
$1.34 \times 10^{-5} \times 143.5 = 1.9 \times 10^{-3}$ g L⁻¹.
(b) Now $[\text{Cl}^-] = 0.010$ M, so $[\text{Ag}^+] = K_{sp}/0.010 = 1.8 \times 10^{-8}$ M.
The solubility has fallen by a factor of about 750. This is the common-ion effect applied
to a solubility equilibrium, and it is why AgCl is washed with dilute HCl, not water.
:::

::: example Will a precipitate form?
**Problem.** Equal volumes of 0.020 M AgNO₃ and 0.020 M NaCl are mixed. Will AgCl
precipitate? ($K_{sp} = 1.8 \times 10^{-10}$)

**Solution.** Mixing doubles the total volume, so each concentration is halved:
$[\text{Ag}^+] = [\text{Cl}^-] = 0.010$ M.
$Q_{sp} = 0.010 \times 0.010 = 1.0 \times 10^{-4}$.
$Q_{sp} \gg K_{sp}$ ($10^{-4}$ against $10^{-10}$), so **yes**, AgCl precipitates at once.
:::

::: caution Three Ksp traps
1. **$K_{sp}$ has no units in the expression but the concentrations are molar.** Do not
   add the concentrations; multiply them, with each raised to its coefficient.
2. **$K_{sp}$ is not solubility.** For salts of different types, the bigger $K_{sp}$ does
   not always mean the more soluble salt — compare $s$, not $K_{sp}$.
3. **A precipitate needs $Q_{sp} > K_{sp}$**, not $Q_{sp} = K_{sp}$ and certainly not
   "$K_{sp}$ is exceeded by the mass added". Calculate the concentrations *after* mixing,
   which means after any dilution.
:::

## 7.5 Acidic and basic buffers; types of salts and their hydrolysis

### Buffer solutions

::: definition Buffer
A **buffer solution** is a solution that resists a change in pH when a small amount of
acid or base is added, or when it is diluted. An **acidic buffer** contains a weak acid
and its salt with a strong base; a **basic buffer** contains a weak base and its salt with
a strong acid.
:::

| | Acidic buffer | Basic buffer |
|---|---|---|
| Contains | weak acid + its salt (CH₃COOH + CH₃COONa) | weak base + its salt (NH₃ + NH₄Cl) |
| pH | below 7 (about $\text{p}K_a$) | above 7 (about $14 - \text{p}K_b$) |
| Added H⁺ is consumed by | CH₃COO⁻ | NH₃ |
| Added OH⁻ is consumed by | CH₃COOH | NH₄⁺ |
| Henderson form | $\text{pH} = \text{p}K_a + \log\dfrac{[\text{salt}]}{[\text{acid}]}$ | $\text{pOH} = \text{p}K_b + \log\dfrac{[\text{salt}]}{[\text{base}]}$ |

**How it works.** In an acetic acid–acetate buffer both components are present in large
amount. Added H⁺ is taken up by the acetate ion, added OH⁻ is taken up by the acid, and
neither survives to change the pH much. The ratio [salt]/[acid] barely moves, so the pH
barely moves.

::: derivation Henderson–Hasselbalch equation
**Setting up.** A weak acid HA at concentration $c_a$ with its salt NaA at $c_s$. The salt
is fully ionised, so $[\text{A}^-] \approx c_s$; the acid is only slightly ionised, so
$[\text{HA}] \approx c_a$.

**Step 1 — start from $K_a$.**
$$ K_a = \frac{[\text{H}^+][\text{A}^-]}{[\text{HA}]} $$

**Step 2 — solve for $[\text{H}^+]$.**
$$ [\text{H}^+] = K_a\frac{[\text{HA}]}{[\text{A}^-]} = K_a\frac{c_a}{c_s} $$

**Step 3 — take negative logarithms of both sides.**
$$ -\log[\text{H}^+] = -\log K_a - \log\frac{c_a}{c_s} $$

**Step 4 — use the definitions and flip the ratio.**
$$ \text{pH} = \text{p}K_a + \log\frac{c_s}{c_a} $$

**Result.** $\text{pH} = \text{p}K_a + \log\dfrac{[\text{salt}]}{[\text{acid}]}$.

**What it means.** The pH is fixed by the **ratio**, not by the absolute concentrations,
which is why dilution does not change the pH of a buffer much. When
$[\text{salt}] = [\text{acid}]$, pH = pKa — the point of maximum buffer capacity.
:::

::: example pH of an acetic acid–acetate buffer
**Problem.** A buffer is 0.10 M in CH₃COOH and 0.20 M in CH₃COONa; pKa = 4.74. Find its pH,
and the pH after 0.01 mol of HCl is added to 1.0 L of it.

**Solution.** pH $= 4.74 + \log(0.20/0.10) = 4.74 + 0.30 = 5.04$.
After adding 0.01 mol HCl, the acid rises to 0.11 M and the salt falls to 0.19 M:
pH $= 4.74 + \log(0.19/0.11) = 4.74 + 0.24 = 4.98$. The pH has moved by only 0.06 unit;
the same amount of HCl in 1.0 L of pure water would take pH from 7 to 2.
:::

Blood is buffered at pH 7.35–7.45 by the H₂CO₃/HCO₃⁻ pair (and by haemoglobin and
phosphate); a deviation of 0.4 unit is life-threatening. Buffer capacity is greatest when
the ratio is 1 : 1 and falls as the ratio moves away from it.

### Salt hydrolysis — the four types

A salt of a weak acid or weak base reacts with water; this is **hydrolysis**. Which ion
hydrolyses decides whether the solution is acidic, basic or neutral.

| Salt type | Example | Ion that hydrolyses | Solution | pH formula |
|---|---|---|---|---|
| strong acid + strong base | NaCl, KNO₃, Na₂SO₄ | neither | **neutral**, pH 7 | pH = 7 |
| weak acid + strong base | CH₃COONa, Na₂CO₃, KCN | the anion (A⁻) | **basic**, pH > 7 | $\text{pH} = 7 + \tfrac{1}{2}(\text{p}K_a + \log C)$ |
| strong acid + weak base | NH₄Cl, (NH₄)₂SO₄ | the cation (BH⁺) | **acidic**, pH < 7 | $\text{pH} = 7 - \tfrac{1}{2}(\text{p}K_b + \log C)$ |
| weak acid + weak base | CH₃COONH₄, NH₄CN | both ions | depends on $K_a$ vs $K_b$ | $\text{pH} = 7 + \tfrac{1}{2}(\text{p}K_a - \text{p}K_b)$ |

**Why each behaves as it does.**

- **NaCl.** Na⁺ is the conjugate acid of NaOH (a strong base) and Cl⁻ is the conjugate
  base of HCl (a strong acid). Neither is strong enough to take or give a proton to water,
  so nothing hydrolyses and the pH stays 7.
- **CH₃COONa.** The acetate ion is the conjugate base of a *weak* acid, so it does take a
  proton from water:
  $$ \text{CH}_3\text{COO}^- + \text{H}_2\text{O} \rightleftharpoons \text{CH}_3\text{COOH} + \text{OH}^- $$
  OH⁻ is left over, so the solution is **basic**. The hydrolysis constant is
  $K_h = K_w/K_a$.
- **NH₄Cl.** The ammonium ion is the conjugate acid of a weak base and donates a proton to
  water:
  $$ \text{NH}_4^+ + \text{H}_2\text{O} \rightleftharpoons \text{NH}_3 + \text{H}_3\text{O}^+ $$
  H₃O⁺ is produced, so the solution is **acidic**, with $K_h = K_w/K_b$.
- **CH₃COONH₄.** Both ions hydrolyse. Because $K_a(\text{CH}_3\text{COOH}) \approx
  K_b(\text{NH}_3) \approx 1.8 \times 10^{-5}$, the two effects cancel and the pH is 7.00 —
  and, unusually, **independent of concentration**.

::: example pH of a salt of a weak acid
**Problem.** Find the pH of 0.10 M CH₃COONa ($K_a = 1.8 \times 10^{-5}$, so pKa = 4.74).

**Solution.** pH $= 7 + \tfrac{1}{2}(\text{p}K_a + \log C) = 7 + \tfrac{1}{2}(4.74 - 1.00)
= 7 + 1.87 = 8.87$.
Check the logic: the salt of a weak acid is basic, and 8.87 is basic but not strongly so.
:::

::: example pH of a salt of a weak base
**Problem.** Find the pH of 0.10 M NH₄Cl ($K_b$ for NH₃ $= 1.8 \times 10^{-5}$).

**Solution.** pH $= 7 - \tfrac{1}{2}(\text{p}K_b + \log C) = 7 - \tfrac{1}{2}(4.74 - 1.00)
= 7 - 1.87 = 5.13$. Acidic, as expected for the salt of a weak base.
:::

::: caution The hydrolysis traps
- **pH 7 does not mean "no hydrolysis".** It means the two hydrolyses happen to cancel
  (CH₃COONH₄) or that neither ion hydrolyses (NaCl). Read the question.
- **A salt of a weak acid is basic, not acidic.** Students reverse this because the word
  "acid" appears. Anchor it: the anion of a weak acid is a base (it takes H⁺ back).
- **The pH of a weak acid–weak base salt does not depend on concentration**, because the
  $C$ cancels between the two hydrolysis expressions. Every formula with $\log C$ in it
  must contain a $\log C$ term that is genuinely there.
- **Hydrolysis increases on dilution and on heating** (both are endothermic in the
  forward direction for these salts), so a dilute or warm salt solution is further from
  pH 7.
:::

```photogrid label="7.1" cols="2" ratio="1.2" caption="Why buffers resist change. (a) Litmus paper only shows acid or base; a pH meter gives the number. (b) 0.100 M acetic acid (Ka = 1.8 x 10^-5) has [H+] = 1.33e-03 M, pH 2.88, and ionises 1.33 per cent. A buffer of 0.10 M acid and 0.10 M acetate has pH = pKa = 4.74. Adding 0.010 mol NaOH to 1 L of pure water jumps the pH from 7.00 to 12.00, but in the buffer it only moves to 4.83, a change of 0.09, because the acid HA neutralises the added OH- and the Henderson equation pH = pKa + log([A-] / [HA]) changes slowly."
@ photo id="sci10/litmus" cap="Litmus paper shows whether a solution is acidic or basic"
fit 1.2
focus 0.5 0.5
@ svg cap="pH before and after adding 0.010 mol of NaOH to 1 L"
Ka = 1.8e-5; c = 0.100
h = (-Ka + math.sqrt(Ka ** 2 + 4 * Ka * c)) / 2; ph = -math.log10(h); pct = h / c * 100
pka = -math.log10(Ka); pb2 = pka + math.log10(0.11 / 0.09); dpb = pb2 - pka
assert abs(ph - 2.876) < 0.002 and abs(pka - 4.745) < 0.001 and abs(pb2 - 4.832) < 0.002 and abs(14 + math.log10(0.010) - 12) < 1e-9
facts = dict(h="%.2e" % h, ph="%.2f" % ph, pct="%.2f" % pct, pka="%.2f" % pka, pb2="%.2f" % pb2, dpb="%.2f" % dpb)
f = Fig(300, 236)
f.text(150, 14, "pH before (box) and after (fill) 0.010 mol NaOH", size=10, color=NAVY, bold=True)
for i, (lab, p1, p2, col, fl) in enumerate((("pure water", 7.0, 12.0, RED, ROSE), ("acetate buffer", pka, pb2, TEAL, MINT))):
    y = 36 + i * 62
    f.text(14, y + 4, lab, size=10.5, color=SLATE, anchor="start")
    f.box(14, y + 10, p1 * 16, 16, fill="#ffffff", stroke=col, r=2, sw=1.4)
    f.box(14, y + 32, p2 * 16, 16, fill=fl, stroke=col, r=2, sw=1.4)
    f.text(14 + p1 * 16 + 5, y + 18, "%.2f" % p1, size=10.5, color=col, bold=True, anchor="start", vmid=True)
    f.text(14 + p2 * 16 + 5, y + 40, "%.2f" % p2, size=10.5, color=col, bold=True, anchor="start", vmid=True)
f.text(150, 170, "0.100 M acetic acid: pH %.2f (%.2f per cent ionised)" % (ph, pct), size=10, color=NAVY, bold=True)
f.text(150, 188, "water moves by 5.00, buffer by %.2f" % dpb, size=10.5, color=NAVY, bold=True)
f.text(150, 206, "pH = pKa + log([A-] / [HA])", size=10.5, color=NAVY, bold=True)
```

## Formula and fact sheet

| Quantity | Relation |
|---|---|
| Equilibrium constant | $K_c = \dfrac{[C]^c[D]^d}{[A]^a[B]^b}$; pure solids and liquids omitted |
| Pressure form | $K_p = \dfrac{p_C^c p_D^d}{p_A^a p_B^b}$ |
| Kp–Kc | $K_p = K_c(RT)^{\Delta n}$, $\Delta n$ = gas product moles − gas reactant moles |
| Reaction quotient | $Q$ from the same expression at any moment; $Q<K$ forward, $Q>K$ backward |
| Reverse / multiple | reverse reaction $1/K$; equation × n gives $K^n$; added equations multiply $K$ |
| Partial pressure | $p_i = x_iP_{\text{total}}$ |
| Ostwald dilution | $K_a = C\alpha^2/(1-\alpha) \approx C\alpha^2$; $\alpha = \sqrt{K_a/C}$ |
| Weak acid | $[\text{H}^+] = \sqrt{K_aC}$; $\text{pH} = \tfrac{1}{2}(\text{p}K_a - \log C)$ |
| Water | $K_w = [\text{H}^+][\text{OH}^-] = 10^{-14}$ at 25 °C; pH + pOH = 14 |
| Definitions | pH = −log[H⁺]; pOH = −log[OH⁻]; pKa = −log Ka; pKa + pKb = 14 |
| Common ion | $[\text{H}^+] = K_a\dfrac{[\text{acid}]}{[\text{salt}]}$ |
| Solubility product | $K_{sp} = [\text{Ag}^+][\text{Cl}^-]$; precipitate when $Q_{sp} > K_{sp}$ |
| Solubility | AB: $s=\sqrt{K_{sp}}$; AB₂: $K_{sp}=4s^3$; AB₃: $K_{sp}=27s^4$ |
| Buffer | $\text{pH} = \text{p}K_a + \log([\text{salt}]/[\text{acid}])$ |
| Salt pH | weak acid salt: $7+\tfrac{1}{2}(\text{p}K_a+\log C)$; weak base salt: $7-\tfrac{1}{2}(\text{p}K_b+\log C)$; both weak: $7+\tfrac{1}{2}(\text{p}K_a-\text{p}K_b)$ |
| Hydrolysis constant | $K_h = K_w/K_a$ (anion) or $K_w/K_b$ (cation); $h = \sqrt{K_h/C}$ |

| Equilibrium | $\Delta n$ | Shift with pressure | Shift with temperature |
|---|---|---|---|
| N₂ + 3H₂ ⇌ 2NH₃, ΔH = −92 kJ | −2 | right (high P) | left (high T) |
| 2SO₂ + O₂ ⇌ 2SO₃, ΔH = −197 kJ | −1 | right | left |
| 4NH₃ + 5O₂ ⇌ 4NO + 6H₂O, ΔH = −905 kJ | +1 | left (slightly) | left |
| H₂ + I₂ ⇌ 2HI, ΔH = −9.4 kJ | 0 | **no effect** | left (slightly) |
| N₂O₄ ⇌ 2NO₂, ΔH = +57 kJ | +1 | left | right (browns on heating) |
| CaCO₃ ⇌ CaO + CO₂, ΔH = +178 kJ | +1 | left | right |

Industrial conditions: **Haber** 700 K, 200 atm, Fe + K₂O/Al₂O₃; **contact** 720 K, 1–2 atm,
V₂O₅; **Ostwald** 800 K, 9 atm, Pt–Rh gauze. In each case the temperature is a compromise
between yield (low T) and rate (high T), and the catalyst changes only the rate.

Logs worth memorising: log 2 = 0.30, log 3 = 0.48, log 5 = 0.70, log 7 = 0.85.

## Chapter summary

- At dynamic equilibrium the forward and reverse rates are equal and concentrations are constant, but both reactions continue; a catalyst only shortens the time taken to get there.
- $K_c$ and $K_p$ take products over reactants with each concentration raised to its coefficient; pure solids and pure liquids are omitted because their concentrations are constant.
- $K_p = K_c(RT)^{\Delta n}$. When $\Delta n = 0$ the two are equal and both are dimensionless; when $\Delta n = -2$, $K_c$ carries L² mol⁻² and $K_p$ atm⁻².
- $Q$ is the same ratio at any moment: $Q < K$ shifts forward, $Q > K$ shifts backward. Only temperature changes $K$; pressure shifts the position only if $\Delta n \neq 0$.
- Le Chatelier: added reactant, removed product, higher pressure (towards fewer gas moles) and lower temperature (for an exothermic reaction) all push the equilibrium forward. Haber, contact and Ostwald each use a compromise temperature of roughly 700–800 K for rate, with pressure chosen from $\Delta n$.
- Arrhenius: H⁺/OH⁻ in water. Brønsted–Lowry: proton donor/acceptor, with conjugate pairs differing by one H⁺. Lewis: electron-pair acceptor/donor. Amphiprotic species (H₂O, HCO₃⁻) can act either way.
- Ostwald's dilution law gives $\alpha = \sqrt{K_a/C}$: dilution raises the fraction dissociated but lowers $[\text{H}^+] = \sqrt{K_aC}$.
- $K_w = 10^{-14}$ at 25 °C, pH + pOH = 14, pKa + pKb = 14. Neutral is pH 7 only at 25 °C.
- A buffer is a weak acid (or base) with its salt; $\text{pH} = \text{p}K_a + \log([\text{salt}]/[\text{acid}])$, and the pH depends on the ratio, not the concentrations.
- Salt hydrolysis: strong/strong neutral; weak acid/strong base basic; strong acid/weak base acidic; weak/weak decided by $K_a$ against $K_b$ and independent of concentration.
- $K_{sp}$ is an equilibrium constant: a precipitate forms when the ionic product after mixing exceeds it, and a common ion lowers the solubility.

## Practice questions

**Set A — Recall (26 questions)**

1. At equilibrium, a reversible reaction has
   (a) the forward reaction stopped (b) the reverse reaction stopped (c) both reactions proceeding at equal rates (d) all the reactants used up
2. For N₂ + 3H₂ ⇌ 2NH₃, the equilibrium constant $K_c$ is
   (a) [NH₃]²/([N₂][H₂]³) (b) [NH₃]/([N₂][H₂]) (c) [N₂][H₂]³/[NH₃]² (d) [NH₃]²/([N₂][H₂])
3. The unit of $K_c$ for H₂ + I₂ ⇌ 2HI is
   (a) mol L⁻¹ (b) L mol⁻¹ (c) mol² L⁻² (d) there is no unit
4. For PCl₅ ⇌ PCl₃ + Cl₂, the relation between $K_p$ and $K_c$ is
   (a) $K_p = K_c$ (b) $K_p = K_c(RT)$ (c) $K_p = K_c(RT)^2$ (d) $K_p = K_c/(RT)$
5. Which species is left out of the equilibrium constant expression?
   (a) gases (b) aqueous ions (c) pure solids (d) dissolved molecules
6. If the reaction quotient $Q$ is greater than $K$, the reaction
   (a) goes forward (b) goes backward (c) is at equilibrium (d) cannot proceed at all
7. A catalyst added to a system already at equilibrium
   (a) shifts it forward (b) shifts it backward (c) increases $K$ (d) does not change the position
8. The equilibrium constant of a reaction changes when
   (a) the pressure is changed (b) the temperature is changed (c) a catalyst is added (d) the volume is changed
9. An increase in pressure shifts an equilibrium towards
   (a) the side with more gas molecules (b) the endothermic side (c) no shift at all (d) the side with fewer gas molecules
10. The catalyst used in the Haber process is
   (a) V₂O₅ (b) platinum–rhodium (c) iron with promoters (d) nickel
11. The catalyst used in the contact process is
   (a) iron (b) V₂O₅ (c) platinum (d) nickel
12. The catalyst used in the Ostwald process is
   (a) V₂O₅ (b) iron (c) platinum–rhodium gauze (d) copper
13. According to Brønsted and Lowry, an acid is a
   (a) proton donor (b) proton acceptor (c) electron-pair donor (d) substance that gives OH⁻
14. The conjugate base of HCO₃⁻ is
   (a) H₂CO₃ (b) CO₂ (c) CO₃²⁻ (d) OH⁻
15. According to Lewis, an acid is an
   (a) electron-pair donor (b) electron-pair acceptor (c) proton donor (d) proton acceptor
16. Which species is amphiprotic?
   (a) HSO₄⁻ (b) SO₄²⁻ (c) HCl (d) NH₄⁺
17. The ionic product of water at 25 °C is
   (a) $1 \times 10^{-7}$ (b) $1 \times 10^{-14}$ (c) $1 \times 10^{-10}$ (d) 55.5
18. At 25 °C, pH + pOH is equal to
   (a) 0 (b) 7 (c) 1 (d) 14
19. For a conjugate acid–base pair at 25 °C, pKa + pKb is
   (a) 7 (b) 10 (c) 14 (d) 0
20. Ostwald's dilution law for a weak acid gives $\alpha$ equal to
   (a) $\sqrt{K_a/C}$ (b) $\sqrt{K_aC}$ (c) $K_a/C$ (d) $C/K_a$
21. The common-ion effect
   (a) increases ionisation (b) increases $K$ (c) has no effect on ionisation (d) suppresses the ionisation of a weak electrolyte
22. For PbCl₂, the solubility product is
   (a) [Pb²⁺][Cl⁻] (b) [Pb²⁺][Cl⁻]² (c) [Pb²⁺]²[Cl⁻] (d) [Pb²⁺][2Cl⁻]²
23. A mixture of CH₃COOH and CH₃COONa in water is
   (a) an acidic buffer (b) a basic buffer (c) a neutral solution (d) not a buffer at all
24. An aqueous solution of NH₄Cl is
   (a) basic (b) neutral (c) strongly basic (d) acidic
25. An aqueous solution of NaCl is
   (a) acidic (b) basic (c) neutral (d) acidic only when concentrated
26. The degree of dissociation of an electrolyte is
   (a) the fraction of dissolved molecules that ionise (b) the number of ions per molecule (c) the molar mass divided by the number of ions (d) the concentration of the solution

::: note Answers and explanations — Set A
**1.** (c) — Equilibrium is dynamic: both reactions continue at the same rate, so concentrations stay constant. Nothing has stopped and nothing is necessarily used up.
**2.** (a) — Products over reactants, each raised to its coefficient: [NH₃]² on top, [N₂] and [H₂]³ below. Option (c) is the expression for the reverse reaction.
**3.** (d) — $\Delta n = 2 - 2 = 0$, so the concentration units cancel and $K_c$ is dimensionless. Options (a) and (b) belong to reactions with $\Delta n = +1$ and $-1$.
**4.** (b) — $\Delta n = 2 - 1 = +1$, so $K_p = K_c(RT)^{+1}$. Option (a) would be right only if $\Delta n = 0$.
**5.** (c) — The concentration of a pure solid or pure liquid is constant (its density divided by molar mass) and is absorbed into $K$. Gases and aqueous species do appear.
**6.** (b) — $Q > K$ means there is too much product, so the reverse reaction runs until $Q$ falls to $K$. Option (a) is the case $Q < K$.
**7.** (d) — A catalyst lowers the activation energy of both directions equally, so equilibrium is reached sooner at exactly the same position. It does not change $K$.
**8.** (b) — $K$ depends only on temperature. Pressure, volume, concentration and catalyst change the position or the rate, never the value of $K$.
**9.** (d) — Raising the pressure favours the side with fewer gas molecules, because that side occupies less volume. If $\Delta n = 0$ there is no shift at all.
**10.** (c) — Iron with K₂O and Al₂O₃ promoters, at about 700 K and 200 atm. V₂O₅ is the contact process and Pt–Rh the Ostwald process.
**11.** (b) — Vanadium(V) oxide, V₂O₅, at about 720 K. Iron is the Haber catalyst and platinum–rhodium the Ostwald catalyst.
**12.** (c) — A platinum–rhodium gauze at about 800 K and 9 atm. It is expensive, so it is used as a fine gauze with a very short contact time.
**13.** (a) — A Brønsted–Lowry acid donates a proton and its conjugate base is what remains after the proton has gone. An electron-pair acceptor is the Lewis definition.
**14.** (c) — Remove one H⁺ from HCO₃⁻ and CO₃²⁻ remains. H₂CO₃ is the conjugate acid, formed by adding H⁺.
**15.** (b) — A Lewis acid accepts an electron pair, as BF₃ does from NH₃. This definition covers acids such as BF₃ and AlCl₃ that contain no hydrogen at all.
**16.** (a) — HSO₄⁻ can donate a proton (to give SO₄²⁻) or accept one (to give H₂SO₄). SO₄²⁻ and NH₄⁺ can only do one of the two.
**17.** (b) — $K_w = [\text{H}^+][\text{OH}^-] = 1 \times 10^{-14}$ at 25 °C. Option (a) is the concentration of each ion in pure water, not the product.
**18.** (d) — Since $K_w = 10^{-14}$, $-\log[\text{H}^+] - \log[\text{OH}^-] = 14$, so pH + pOH = 14 at 25 °C. At other temperatures the sum is pKw, not 14.
**19.** (c) — $K_aK_b = K_w$ for a conjugate pair, so taking logs gives pKa + pKb = pKw = 14 at 25 °C.
**20.** (a) — $K_a = C\alpha^2$ for a weak electrolyte, so $\alpha = \sqrt{K_a/C}$. Option (b) is the expression for $[\text{H}^+]$, not for $\alpha$.
**21.** (d) — Adding a common ion drives the ionisation equilibrium back towards the un-ionised molecule, so $\alpha$ and $[\text{H}^+]$ fall. $K$ itself is unchanged.
**22.** (b) — PbCl₂ gives one Pb²⁺ and two Cl⁻, so each concentration is raised to its coefficient: [Pb²⁺][Cl⁻]².
**23.** (a) — A weak acid with its salt is an acidic buffer, with pH ≈ pKa = 4.74. A basic buffer needs a weak base and its salt, such as NH₃ + NH₄Cl.
**24.** (d) — NH₄⁺ is the conjugate acid of the weak base NH₃, so it donates a proton to water and leaves H₃O⁺. The salt of a weak base is acidic.
**25.** (c) — Na⁺ and Cl⁻ are the conjugates of a strong base and a strong acid, so neither hydrolyses and the pH stays 7 at 25 °C.
**26.** (a) — $\alpha$ is the fraction of the dissolved molecules that have split into ions, so it lies between 0 and 1 (or 0 and 100 %). It is not the number of ions per formula unit.
:::

**Set B — Understanding (16 questions)**

1. For N₂ + 3H₂ ⇌ 2NH₃ at equilibrium, which change increases the amount of NH₃ **without** changing $K$?
   (a) raising the temperature (b) adding a catalyst (c) compressing the mixture (d) adding argon at constant volume
2. Argon is added to a gaseous equilibrium mixture at constant volume. The position of equilibrium
   (a) does not change (b) shifts forward (c) shifts backward (d) changes $K$
3. For H₂ + I₂ ⇌ 2HI, doubling the total pressure at constant temperature
   (a) shifts the equilibrium forward (b) shifts it backward (c) doubles $K$ (d) leaves the position unchanged
4. N₂O₄ ⇌ 2NO₂ is endothermic. On warming the mixture, it
   (a) becomes colourless (b) becomes a deeper brown (c) does not change colour (d) deposits a solid
5. On diluting a weak acid solution with water,
   (a) $\alpha$ falls and [H⁺] falls (b) $\alpha$ rises and [H⁺] rises (c) $\alpha$ rises and [H⁺] falls (d) both stay the same
6. Which 0.1 M aqueous solution has the highest pH at 25 °C?
   (a) HCl (b) CH₃COOH (c) NaCl (d) NaOH
7. In HCO₃⁻ + H₂O ⇌ H₂CO₃ + OH⁻, water acts as
   (a) an acid (b) a base (c) a salt (d) a catalyst
8. NH₃ is a Brønsted base but not an Arrhenius base because
   (a) it does not accept protons (b) its formula contains no OH group (c) it is a weak electrolyte (d) it reacts with acids
9. A buffer solution resists a change in pH because it
   (a) holds reserves of a weak acid and its conjugate base (b) contains a strong acid and a strong base (c) always has pH exactly 7 (d) does not ionise at all
10. A solution of sodium acetate is basic because
   (a) Na⁺ hydrolyses (b) the salt is insoluble (c) CH₃COO⁻ accepts a proton from water (d) CH₃COO⁻ donates a proton to water
11. Which pair of solutions, mixed, gives a buffer?
   (a) HCl + NaCl (b) NaOH + NaCl (c) HCl + NaOH in equal amounts (d) CH₃COOH + CH₃COONa
12. AgCl is much less soluble in 0.1 M NaCl than in pure water because
   (a) $K_{sp}$ increases (b) the common ion shifts the equilibrium left (c) NaCl reacts with AgCl (d) the temperature falls
13. A catalyst cannot change the equilibrium constant because it
   (a) lowers only the forward activation energy (b) is used up in the reaction (c) changes ΔH (d) lowers both activation energies equally
14. Ostwald's dilution law cannot be applied to strong electrolytes because
   (a) they are almost completely ionised (b) they do not dissolve (c) they have no $K_a$ at all (d) their $\alpha$ is zero
15. At 100 °C pure water has pH about 6.1. This shows that
   (a) water is acidic at 100 °C (b) water is basic at 100 °C (c) water is still neutral because [H⁺] = [OH⁻] (d) $K_w$ is smaller at 100 °C
16. Which 0.1 M salt solution is acidic at 25 °C?
   (a) NaCl (b) NH₄Cl (c) Na₂CO₃ (d) CH₃COONa

::: note Answers and explanations — Set B
**1.** (c) — Compression favours the side with fewer gas molecules (4 → 2), so more NH₃ forms while $K$ stays the same. Heating would shift an exothermic reaction backward, and a catalyst changes only the rate.
**2.** (a) — At constant volume the partial pressures of the reacting gases are unchanged, so $Q$ is unchanged and there is no shift. At constant *pressure* the added gas would expand the mixture and shift it towards more gas molecules.
**3.** (d) — $\Delta n = 0$, so both partial pressures are multiplied by the same factor and $Q$ still equals $K$. $K$ itself never depends on pressure.
**4.** (b) — Dissociation of N₂O₄ into NO₂ absorbs heat, so warming shifts the equilibrium to the right. NO₂ is the brown gas, so the colour deepens.
**5.** (c) — Dilution raises the fraction ionised ($\alpha = \sqrt{K_a/C}$) but lowers the concentration of ions, since $[\text{H}^+] = \sqrt{K_aC}$. More dissociated, less acidic.
**6.** (d) — NaOH is a strong base, so its pH is about 13. NaCl is neutral (7), acetic acid about 2.9 and HCl about 1.
**7.** (a) — Water donates a proton to HCO₃⁻ and becomes OH⁻, so water is the acid and HCO₃⁻ the base. In the reverse reaction their roles swap.
**8.** (b) — The Arrhenius definition requires a base to supply OH⁻ in water; NH₃ has no OH group and acts as a base only by accepting H⁺.
**9.** (a) — Both members of the pair are present in large amount: the acid neutralises added OH⁻ and the anion neutralises added H⁺, so the ratio, and with it the pH, hardly moves.
**10.** (c) — The acetate ion is the conjugate base of a weak acid, so it takes a proton from water and leaves OH⁻ behind. Na⁺ is the conjugate of a strong base and does not hydrolyse.
**11.** (d) — A weak acid with its salt is the definition of an acidic buffer. HCl + NaOH in equal amounts gives NaCl and water — a neutral salt, not a buffer.
**12.** (b) — Extra Cl⁻ pushes the dissolution equilibrium back towards the solid, so less AgCl dissolves. $K_{sp}$ is unchanged; only the position of the equilibrium moves.
**13.** (d) — It provides an alternative path of lower activation energy for both directions by the same amount, so the difference between the two rates, and hence $K$, is untouched.
**14.** (a) — The approximation $1-\alpha \approx 1$ fails when $\alpha$ is close to 1, which is exactly the case for a strong electrolyte.
**15.** (c) — At 100 °C $K_w$ is larger, about $5.5 \times 10^{-13}$, so neutral water has [H⁺] = [OH⁻] = 7.4 × 10⁻⁷ M and pH 6.13. Neutral does not mean pH 7 at every temperature.
**16.** (b) — NH₄⁺ is the conjugate acid of the weak base NH₃ and hydrolyses to give H₃O⁺. NaCl is neutral and the other two are basic.
:::

**Set C — Application (10 questions)**

1. For H₂ + I₂ ⇌ 2HI, the equilibrium concentrations are [H₂] = 0.50, [I₂] = 0.50 and [HI] = 2.0 mol L⁻¹. $K_c$ is
   (a) 4.0 (b) 8.0 (c) 16 (d) 32
2. For N₂ + 3H₂ ⇌ 2NH₃, $K_c = 4.0 \times 10^{-2}$ at 400 K. Taking $R = 0.0821$ L atm mol⁻¹ K⁻¹, $K_p$ is about
   (a) $3.7 \times 10^{-5}$ (b) $1.3$ (c) $4.3 \times 10^{1}$ (d) $3.7 \times 10^{-3}$
3. For 2SO₂ + O₂ ⇌ 2SO₃, $K_c = 278$. A mixture has [SO₂] = 0.20, [O₂] = 0.10 and [SO₃] = 0.40 mol L⁻¹. The reaction will
   (a) go backward (b) go forward (c) stay at equilibrium (d) stop completely
4. The pH of $2 \times 10^{-3}$ M HCl is
   (a) 2.00 (b) 2.30 (c) 3.00 (d) 2.70
5. The pH of 0.005 M NaOH at 25 °C is
   (a) 11.70 (b) 2.30 (c) 12.00 (d) 11.30
6. The pH of 0.01 M CH₃COOH ($K_a = 1.8 \times 10^{-5}$) is about
   (a) 2.00 (b) 2.87 (c) 3.37 (d) 4.74
7. The solubility of AgCl in pure water is ($K_{sp} = 1.8 \times 10^{-10}$)
   (a) $1.3 \times 10^{-5}$ mol L⁻¹ (b) $1.8 \times 10^{-10}$ mol L⁻¹ (c) $9.0 \times 10^{-6}$ mol L⁻¹ (d) $1.3 \times 10^{-3}$ mol L⁻¹
8. Equal volumes of 0.020 M AgNO₃ and 0.020 M NaCl are mixed. Taking $K_{sp}$(AgCl) $= 1.8 \times 10^{-10}$,
   (a) no precipitate forms because $Q < K_{sp}$ (b) a precipitate forms because $Q = K_{sp}$ (c) no precipitate forms because $Q = K_{sp}$ (d) a precipitate forms because $Q > K_{sp}$
9. A buffer is 0.10 M in CH₃COOH and 0.010 M in CH₃COONa (pKa = 4.74). Its pH is
   (a) 4.74 (b) 3.74 (c) 5.74 (d) 4.04
10. The pH of 0.10 M CH₃COONa solution is (pKa of CH₃COOH = 4.74)
   (a) 5.13 (b) 7.00 (c) 8.87 (d) 11.13

::: note Answers and explanations — Set C
**1.** (c) — $K_c = [\text{HI}]^2/([\text{H}_2][\text{I}_2]) = 2.0^2/(0.50 \times 0.50) = 4.0/0.25 = 16$. Option (a) forgets to square [HI] or to multiply the two denominators.
**2.** (a) — $\Delta n = 2 - 4 = -2$ and $RT = 0.0821 \times 400 = 32.84$. So $K_p = 0.040 \times (32.84)^{-2} = 0.040/1078 = 3.7 \times 10^{-5}$ atm⁻². Option (b) multiplies instead of dividing.
**3.** (b) — $Q = [\text{SO}_3]^2/([\text{SO}_2]^2[\text{O}_2]) = 0.16/(0.040 \times 0.10) = 40$, which is less than $K = 278$, so the forward reaction runs until $Q$ reaches 278.
**4.** (d) — pH $= -\log(2 \times 10^{-3}) = 3 - \log 2 = 3 - 0.30 = 2.70$. Option (a) ignores the factor 2 and option (c) rounds the wrong way.
**5.** (a) — pOH $= -\log(5 \times 10^{-3}) = 3 - 0.70 = 2.30$, so pH $= 14 - 2.30 = 11.70$. Option (b) is the pOH, not the pH.
**6.** (c) — pH $= \tfrac{1}{2}(\text{p}K_a - \log C) = \tfrac{1}{2}(4.74 + 2.00) = 3.37$. Option (b) is the value for 0.1 M, ten times stronger.
**7.** (a) — For a 1 : 1 salt $s = \sqrt{K_{sp}} = \sqrt{1.8 \times 10^{-10}} = 1.34 \times 10^{-5}$ mol L⁻¹. Option (b) is $K_{sp}$ itself, not the solubility.
**8.** (d) — After mixing, each concentration is halved to 0.010 M, so $Q = 1.0 \times 10^{-4}$, far above $1.8 \times 10^{-10}$. Precipitation continues until $Q$ falls to $K_{sp}$.
**9.** (b) — pH $= 4.74 + \log(0.010/0.10) = 4.74 - 1.00 = 3.74$. The salt is ten times more dilute than the acid, so the buffer is more acidic than pKa.
**10.** (c) — pH $= 7 + \tfrac{1}{2}(\text{p}K_a + \log C) = 7 + \tfrac{1}{2}(4.74 - 1.00) = 8.87$. Option (a) is the pH of the corresponding NH₄Cl-type salt, and (d) would need a much stronger base.
:::

