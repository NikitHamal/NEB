---
subject: Chemistry
grade: 12
unit: 2
title: Ionic Equilibrium
hours: 10
area: General and Physical Chemistry
---

Water is never just water. In every aqueous solution a set of reversible ionic
reactions sits at equilibrium — the water splitting into H⁺ and OH⁻, a weak acid
half-ionised, a sparingly soluble salt dissolving as fast as it re-precipitates.
This unit gives you the equilibrium constants that describe those processes
($K_w$, $K_a$, $K_b$, $K_{sp}$, $K_h$) and the arithmetic — almost all of it
logarithms — that turns them into a pH or a solubility. It is the longest unit in
the physical-chemistry area and the most heavily examined.

::: key What the examiner asks from this unit
Expect one definition question (Bronsted or Lewis, conjugate pairs), one
**numerical** on pH / $K_a$ / buffers / $K_{sp}$, and very often a question on
choosing an indicator or on salt hydrolysis. Learn the five master formulas in
§2.8, §2.12 and §2.15 and most of the marks are already yours.
:::

## 2.1 Limitation of Arrhenius concept

Svante Arrhenius (1887) defined an **acid** as a substance that gives H⁺ ions in
aqueous solution and a **base** as one that gives OH⁻ ions. The definition works —
HCl → H⁺ + Cl⁻ and NaOH → Na⁺ + OH⁻ — but it fails in five ways that the board
asks about directly.

1. **It is restricted to water.** Acid-base behaviour in liquid ammonia, in
   benzene or in the gas phase is outside it. NH₃(g) + HCl(g) → NH₄Cl(s) is clearly
   a neutralisation, yet no water and no OH⁻ are involved.
2. **Free H⁺ does not exist in solution.** A bare proton is only about 10⁻¹⁵ m
   across and would have an enormous charge density; in water it is always
   hydrated as the hydronium ion, H₃O⁺.
3. **It cannot explain acids without hydrogen.** CO₂, SO₂, AlCl₃ and BF₃ all
   behave as acids, yet none of them contains an ionisable H.
4. **It cannot explain bases without OH.** NH₃, Na₂CO₃, CH₃NH₂ and NaHCO₃ all
   turn red litmus blue although no OH group is present in the formula.
5. **It ignores the role of the solvent.** Dry HCl gas does not turn dry blue
   litmus red, and HCl in benzene is not acidic at all. The solvent is an active
   partner, not a spectator.

## 2.2 Bronsted-Lowry definition; conjugate acid-base pairs

::: definition Bronsted-Lowry acid and base
An **acid** is a substance that can **donate a proton** (H⁺); a **base** is a
substance that can **accept a proton**. An acid-base reaction is simply the
transfer of a proton from the acid to the base.
:::

Because a proton must be given *to* something, every Bronsted acid-base reaction
has two acids and two bases:

CH₃COOH + H₂O ⇌ H₃O⁺ + CH₃COO⁻

Here CH₃COOH gives a proton to H₂O in the forward direction, and H₃O⁺ gives a
proton back to CH₃COO⁻ in the reverse direction.

::: definition Conjugate acid-base pair
A **conjugate acid-base pair** is a pair of species that differ by **one proton**.
The species left after an acid has lost its proton is its **conjugate base**; the
species formed when a base gains a proton is its **conjugate acid**.
:::

| Acid | Its conjugate base | Base | Its conjugate acid |
|---|---|---|---|
| HCl | Cl⁻ | H₂O | H₃O⁺ |
| CH₃COOH | CH₃COO⁻ | NH₃ | NH₄⁺ |
| H₂SO₄ | HSO₄⁻ | OH⁻ | H₂O |
| HSO₄⁻ | SO₄²⁻ | CO₃²⁻ | HCO₃⁻ |
| H₂CO₃ | HCO₃⁻ | HCO₃⁻ | H₂CO₃ |
| NH₄⁺ | NH₃ | CH₃COO⁻ | CH₃COOH |
| H₃O⁺ | H₂O | H₂PO₄⁻ | H₃PO₄ |

Species such as H₂O, HCO₃⁻, HSO₄⁻ and H₂PO₄⁻ appear in **both** columns: they can
donate a proton to a stronger base and accept one from a stronger acid. They are
called **amphiprotic** (or amphoteric) species.

H₂O + H₂O ⇌ H₃O⁺ + OH⁻

::: caution A conjugate base is not always a base you would recognise
Cl⁻ is the conjugate base of HCl, but a solution of NaCl is neutral. The reason is
that HCl is a very strong acid, so its conjugate base Cl⁻ is *extremely* weak — so
weak that it takes no measurable proportion of protons back from water. "Conjugate
base" describes a relationship, not a strength.
:::

The Bronsted definition still has a limitation of its own: it needs a **proton**.
Reactions such as BF₃ + NH₃ → F₃B←NH₃, which show every chemical feature of
neutralisation, lie outside it.

## 2.3 Relative strength of acids and bases

The strength of a Bronsted acid is the **extent** to which it transfers its proton
to water. For a weak acid HA,

HA + H₂O ⇌ H₃O⁺ + A⁻

$$ K_a = \frac{[\text{H}_3\text{O}^{+}][\text{A}^{-}]}{[\text{HA}]} $$

A larger $K_a$ (smaller $pK_a$) means a stronger acid. The same logic with $K_b$
measures base strength.

::: key Stronger acid, weaker conjugate base
The stronger an acid, the weaker its conjugate base, and vice versa. Quantitatively
$K_a \times K_b = K_w$ for any conjugate pair, so $pK_a + pK_b = 14$ at 25 °C.
:::

| Acid | $K_a$ (25 °C) | $pK_a$ | Conjugate base | $K_b$ of that base |
|---|---|---|---|---|
| HCl | very large | < 0 | Cl⁻ | negligible |
| HSO₄⁻ | $1.2\times10^{-2}$ | 1.92 | SO₄²⁻ | $8.3\times10^{-13}$ |
| HF | $6.8\times10^{-4}$ | 3.17 | F⁻ | $1.5\times10^{-11}$ |
| HCOOH | $1.8\times10^{-4}$ | 3.75 | HCOO⁻ | $5.6\times10^{-11}$ |
| CH₃COOH | $1.8\times10^{-5}$ | 4.74 | CH₃COO⁻ | $5.6\times10^{-10}$ |
| H₂CO₃ | $4.5\times10^{-7}$ | 6.35 | HCO₃⁻ | $2.2\times10^{-8}$ |
| NH₄⁺ | $5.6\times10^{-10}$ | 9.25 | NH₃ | $1.8\times10^{-5}$ |
| HCN | $4.9\times10^{-10}$ | 9.31 | CN⁻ | $2.0\times10^{-5}$ |

If two weak acids of the same concentration $C$ are compared, then since
$\alpha = \sqrt{K_a/C}$ (next section),

$$ \frac{\text{strength of acid 1}}{\text{strength of acid 2}}
= \frac{\alpha_1}{\alpha_2} = \sqrt{\frac{K_{a1}}{K_{a2}}} $$

So acetic acid ($1.8\times10^{-5}$) is about 192 times stronger than hydrocyanic
acid at the same concentration, because
$\sqrt{1.8\times10^{-5}/4.9\times10^{-10}} = \sqrt{3.67\times10^{4}} = 192$.

**Levelling effect.** HCl, HBr, HI, HNO₃ and HClO₄ all appear equally strong in
water, because each of them transfers its proton to water completely; the
strongest acid that can exist in water is H₃O⁺ itself. Water is said to *level*
them. To rank them you must use a weaker base as solvent, such as glacial acetic
acid, which shows the true order HClO₄ > HI > HBr > HCl > HNO₃.

## 2.4 Lewis definition

::: definition Lewis acid and base
A **Lewis acid** is any species that can **accept a lone pair of electrons**; a
**Lewis base** is any species that can **donate a lone pair**. Neutralisation is
the formation of a coordinate (dative) bond between them.
:::

BF₃ + :NH₃ → F₃B←NH₃

| Lewis acids (electron-pair acceptors) | Lewis bases (electron-pair donors) |
|---|---|
| Molecules with an incomplete octet: BF₃, AlCl₃, BeCl₂ | Molecules with a lone pair: NH₃, H₂O, R–OH, R–NH₂, R₂S |
| Simple cations: H⁺, Ag⁺, Cu²⁺, Fe³⁺ | Anions: OH⁻, Cl⁻, CN⁻, F⁻ |
| Molecules with expandable octets: SiF₄, PF₅, SF₄ | Molecules with π electrons: C₂H₄, C₆H₆ |
| Molecules with a multiple bond to an electronegative atom: CO₂, SO₃, SO₂ | Carbanions and alkoxides |

Ag⁺ + 2NH₃ → [Ag(NH₃)₂]⁺ and Cu²⁺ + 4NH₃ → [Cu(NH₃)₄]²⁺ are Lewis
neutralisations; this is why complex formation belongs in the same chapter of
ideas as acidity.

| | Arrhenius | Bronsted-Lowry | Lewis |
|---|---|---|---|
| Acid | gives H⁺ in water | proton donor | electron-pair acceptor |
| Base | gives OH⁻ in water | proton acceptor | electron-pair donor |
| Solvent | must be water | any solvent, or none | any solvent, or none |
| Scope | narrowest | wider | widest |
| Weakness | no non-aqueous acids/bases | cannot handle BF₃, AlCl₃ | too wide; says nothing about relative strength; protonic acids such as HCl are not strictly Lewis acids |

## 2.5 Ionization of weak electrolyte (Ostwald's dilution law)

A weak electrolyte is only partly ionised, and the un-ionised molecules are in
equilibrium with the ions.

::: derivation Ostwald's dilution law
Let one mole of a weak binary electrolyte AB be dissolved in $V$ litres, so its
concentration is $C = 1/V$, and let $\alpha$ be its degree of ionisation at
equilibrium.

| | AB | ⇌ | A⁺ | + | B⁻ |
|---|---|---|---|---|---|
| initial | $C$ | | 0 | | 0 |
| at equilibrium | $C(1-\alpha)$ | | $C\alpha$ | | $C\alpha$ |

Applying the law of mass action,

$$ K = \frac{[\text{A}^{+}][\text{B}^{-}]}{[\text{AB}]}
= \frac{C\alpha \cdot C\alpha}{C(1-\alpha)} = \frac{C\alpha^{2}}{1-\alpha} $$

For a weak electrolyte $\alpha \ll 1$, so $1 - \alpha \approx 1$ and

$$ K \approx C\alpha^{2} \;\Longrightarrow\;
\alpha = \sqrt{\frac{K}{C}} = \sqrt{KV} $$
:::

::: key Ostwald's dilution law in words
The degree of ionisation of a weak electrolyte is **inversely proportional to the
square root of its concentration**, i.e. directly proportional to the square root
of the dilution. Diluting a weak acid one hundred times increases its degree of
ionisation ten times.
:::

```figure caption="Ostwald's dilution law. The degree of ionisation of a weak acid rises steeply on dilution and approaches 100 % at infinite dilution; a stronger acid (larger $K_a$) lies higher at every concentration."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9,2.9))
C = np.logspace(-7, 0, 500)
data = [(6.8e-4, 'HF   (Ka = 6.8 × 10⁻⁴)', SERIES[1]),
        (1.8e-5, 'CH₃COOH   (Ka = 1.8 × 10⁻⁵)', ACCENT),
        (4.9e-10, 'HCN   (Ka = 4.9 × 10⁻¹⁰)', SERIES[2])]
for Ka, lab, col in data:
    a = (-Ka + np.sqrt(Ka**2 + 4*Ka*C))/(2*C)
    ax.plot(C, 100*a, color=col, lw=1.8, label=lab)
ax.set_xscale('log'); ax.set_yscale('log')
ax.set_xlabel('concentration  C  (mol L⁻¹)   —   dilution increases ←')
ax.set_ylabel('degree of ionisation (%)')
ax.set_xlim(1e-7, 1); ax.set_ylim(1e-3, 200)
ax.axhline(100, color=MUTED, lw=0.8, ls=':')
ax.text(1.4e-7, 118, 'complete ionisation', fontsize=7.6, color=MUTED)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=0.4, which='major')
ax.legend(loc='lower left', fontsize=7.6)
```

The law works well for weak electrolytes but **fails completely for strong
electrolytes** such as NaCl or HCl, which are fully ionised in the solid state
already; for them the observed "degree of ionisation" changes with concentration
only because of interionic attraction, not because of any equilibrium.

## 2.6 Ionic product of water (Kw)

Pure water conducts electricity very slightly, so it must ionise to a small
extent:

H₂O + H₂O ⇌ H₃O⁺ + OH⁻, usually written H₂O ⇌ H⁺ + OH⁻

$$ K = \frac{[\text{H}^{+}][\text{OH}^{-}]}{[\text{H}_2\text{O}]} $$

Because only about two water molecules in 10⁹ are ionised, $[\text{H}_2\text{O}]$
is effectively constant (55.5 mol L⁻¹), and it is absorbed into the constant:

$$ K_w = K[\text{H}_2\text{O}] = [\text{H}^{+}][\text{OH}^{-}] $$

::: definition Ionic product of water
The **ionic product of water**, $K_w$, is the product of the molar concentrations
of hydrogen ions and hydroxide ions in water or in any aqueous solution at a given
temperature. At 25 °C, $K_w = 1.0\times10^{-14}\ \text{mol}^{2}\ \text{L}^{-2}$,
and in pure water $[\text{H}^{+}] = [\text{OH}^{-}] = 1.0\times10^{-7}$ mol L⁻¹.
:::

Taking negative logarithms of $K_w = [\text{H}^{+}][\text{OH}^{-}]$,

$$ pK_w = pH + pOH = 14 \quad \text{(at 25 }^{\circ}\text{C)} $$

Ionisation of water is endothermic, so by Le Chatelier's principle $K_w$ rises
with temperature:

| Temperature | $K_w$ | $pK_w$ | pH of pure water |
|---|---|---|---|
| 0 °C | $0.11\times10^{-14}$ | 14.94 | 7.47 |
| 25 °C | $1.00\times10^{-14}$ | 14.00 | 7.00 |
| 50 °C | $5.48\times10^{-14}$ | 13.26 | 6.63 |
| 100 °C | $51.3\times10^{-14}$ | 12.29 | 6.14 |

::: caution "Neutral means pH 7" is only true at 25 °C
Water at 100 °C has pH 6.14 and is still **neutral**, because
$[\text{H}^{+}] = [\text{OH}^{-}]$ there. Neutrality means the two concentrations
are equal, not that the pH is 7.
:::

## 2.7 Dissociation constant of acid and base (Ka and Kb); concept of pKa and pKb

For the weak acid HA and the weak base BOH:

$$ K_a = \frac{[\text{H}^{+}][\text{A}^{-}]}{[\text{HA}]}, \qquad
K_b = \frac{[\text{B}^{+}][\text{OH}^{-}]}{[\text{BOH}]} $$

$K_a$ and $K_b$ are true equilibrium constants: they depend on temperature but
**not** on concentration. Combining with Ostwald's law, $K_a = C\alpha^{2}$.

Because these constants span many powers of ten, they are quoted
logarithmically:

$$ pK_a = -\log K_a, \qquad pK_b = -\log K_b $$

A **small** $pK_a$ means a **strong** acid. Acetic acid, $K_a = 1.8\times10^{-5}$,
has $pK_a = 4.74$.

::: derivation The relation $K_a \times K_b = K_w$ for a conjugate pair
Take the pair CH₃COOH / CH₃COO⁻:

CH₃COOH ⇌ H⁺ + CH₃COO⁻ with $K_a = \dfrac{[\text{H}^{+}][\text{CH}_3\text{COO}^{-}]}{[\text{CH}_3\text{COOH}]}$

CH₃COO⁻ + H₂O ⇌ CH₃COOH + OH⁻ with $K_b = \dfrac{[\text{CH}_3\text{COOH}][\text{OH}^{-}]}{[\text{CH}_3\text{COO}^{-}]}$

Multiplying the two expressions, every concentration except those of H⁺ and OH⁻
cancels:

$$ K_a \times K_b = [\text{H}^{+}][\text{OH}^{-}] = K_w $$

and taking logarithms, $pK_a + pK_b = pK_w = 14$ at 25 °C.
:::

## 2.8 pH value: pH of strong and weak acids; pH of strong and weak bases

Hydrogen-ion concentrations run from about 10 to 10⁻¹⁵ mol L⁻¹. Sørensen (1909)
replaced them by a logarithmic scale.

::: definition pH
The **pH** of a solution is the negative logarithm to base 10 of its hydrogen-ion
concentration in mol L⁻¹:

$$ pH = -\log_{10}[\text{H}^{+}], \qquad [\text{H}^{+}] = 10^{-pH} $$

Similarly $pOH = -\log_{10}[\text{OH}^{-}]$, and $pH + pOH = 14$ at 25 °C.
:::

```figure caption="The pH scale at 25 °C. Each unit is a tenfold change in $[\text{H}^{+}]$, so lemon juice is about ten thousand times more acidic than milk."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
fig, ax = plt.subplots(figsize=(5.2,2.7))
cmap = LinearSegmentedColormap.from_list(
    'ph', [SERIES[1], '#e0a95f', '#e6e9ee', '#7fb2d8', ACCENT])
grad = np.linspace(0, 1, 700).reshape(1, -1)
ax.imshow(grad, extent=[0, 14, 0.0, 0.85], aspect='auto', cmap=cmap, zorder=1)
ax.add_patch(plt.Rectangle((0, 0.0), 14, 0.85, fill=False, ec=INK, lw=0.9, zorder=3))
for p in range(15):
    ax.plot([p, p], [0.0, 0.14], color=INK, lw=0.8, zorder=4)
    ax.text(p, -0.12, str(p), ha='center', va='top', fontsize=7.8, color=INK)
    ax.text(p, 1.00, str(14 - p), ha='center', va='bottom', fontsize=7.2, color=MUTED)
ax.text(-0.55, 0.42, 'pH', ha='right', va='center', fontsize=9, color=INK)
ax.text(-0.55, 1.06, 'pOH', ha='right', va='center', fontsize=8, color=MUTED)
ax.plot([7, 7], [0.0, 0.85], color=INK, lw=1.4, zorder=5)
for x0, x1, lab in [(0, 7, 'ACIDIC'), (7, 14, 'ALKALINE')]:
    ax.text((x0 + x1)/2, 1.52, lab, ha='center', fontsize=8.4, color=INK)
ax.text(7, 1.52, 'neutral', ha='center', fontsize=7.6, color=INK,
        bbox=dict(fc='white', ec='none', pad=1.2))
items = [(1.5, 'gastric juice', 0), (2.4, 'lemon juice', 1), (3.0, 'vinegar', 2),
         (5.6, 'rain water', 0), (6.6, 'milk', 1), (7.4, 'blood', 2),
         (8.3, 'baking soda', 0), (10.5, 'milk of magnesia', 1),
         (12.4, 'lime water', 2)]
for px, lab, row in items:
    y = [-0.62, -1.22, -1.82][row]
    ax.plot([px, px], [-0.02, y + 0.09], color=MUTED, lw=0.7, ls=':')
    ax.text(px, y, lab, ha='center', va='top', fontsize=7.3, color=INK)
ax.set_xlim(-2.1, 14.9); ax.set_ylim(-2.5, 1.95)
ax.axis('off')
```

**Strong acid.** A strong monobasic acid is completely ionised, so
$[\text{H}^{+}] = C$ and

$$ pH = -\log C $$

For a dibasic strong acid such as H₂SO₄, $[\text{H}^{+}] = 2C$.

**Weak acid.** Only a fraction $\alpha$ ionises, and $[\text{H}^{+}] = C\alpha$.
Substituting $\alpha = \sqrt{K_a/C}$,

$$ [\text{H}^{+}] = C\sqrt{\frac{K_a}{C}} = \sqrt{K_aC}
\;\Longrightarrow\; pH = \tfrac{1}{2}\left(pK_a - \log C\right) $$

**Strong base.** $[\text{OH}^{-}] = C \times$ (acidity), $pOH = -\log[\text{OH}^{-}]$
and $pH = 14 - pOH$.

**Weak base.** $[\text{OH}^{-}] = \sqrt{K_bC}$, so

$$ pOH = \tfrac{1}{2}\left(pK_b - \log C\right), \qquad pH = 14 - pOH $$

::: caution pH is not confined to 0–14
A 2 M solution of HCl has $[\text{H}^{+}] = 2$, so $pH = -\log 2 = -0.30$; a 5 M
NaOH solution has pH 14.7. The 0–14 range is only the region in which both ion
concentrations are below 1 mol L⁻¹. Also remember that $[\text{H}^{+}]$ must be in
**mol L⁻¹** — a favourite trap is to give the data in g L⁻¹.
:::

::: example Worked example 2.1 — strong acids and bases
**Problem.** Calculate the pH of (a) 0.005 M Ca(OH)₂, and (b) the solution formed
when 100 cm³ of 0.10 M HCl is mixed with 100 cm³ of 0.05 M NaOH.

**Solution.**

(a) Ca(OH)₂ → Ca²⁺ + 2OH⁻ is fully ionised, so
$[\text{OH}^{-}] = 2 \times 0.005 = 0.01\ \text{mol L}^{-1}$.

$$ pOH = -\log(1.0\times10^{-2}) = 2, \qquad pH = 14 - 2 = 12 $$

(b) Millimoles of H⁺ $= 0.10 \times 100 = 10.0$; millimoles of OH⁻
$= 0.05 \times 100 = 5.0$. The acid is in excess by 5.0 mmol, in a total volume of
200 cm³:

$$ [\text{H}^{+}] = \frac{5.0}{200} = 0.025\ \text{mol L}^{-1} $$

$$ pH = -\log(2.5\times10^{-2}) = 2 - \log 2.5 = 2 - 0.398 = 1.60 $$
:::

::: example Worked example 2.2 — a weak acid
**Problem.** Calculate the pH, the degree of ionisation and the concentration of
CH₃COO⁻ in 0.10 M acetic acid. $K_a = 1.8\times10^{-5}$.

**Solution.**

$$ [\text{H}^{+}] = \sqrt{K_aC} = \sqrt{1.8\times10^{-5} \times 0.10}
= \sqrt{1.8\times10^{-6}} = 1.34\times10^{-3}\ \text{mol L}^{-1} $$

$$ pH = -\log(1.34\times10^{-3}) = 3 - 0.127 = 2.87 $$

$$ \alpha = \sqrt{\frac{K_a}{C}} = \sqrt{\frac{1.8\times10^{-5}}{0.10}}
= 1.34\times10^{-2} = 1.34\ \% $$

Since each ionised molecule gives one acetate ion,
$[\text{CH}_3\text{COO}^{-}] = [\text{H}^{+}] = 1.34\times10^{-3}$ mol L⁻¹, and
the assumption $\alpha \ll 1$ is justified.
:::

::: example Worked example 2.3 — a weak base (Ostwald's law)
**Problem.** Calculate the degree of ionisation, the hydroxide-ion concentration
and the pH of 0.020 M ammonium hydroxide. $K_b = 1.8\times10^{-5}$.

**Solution.**

$$ \alpha = \sqrt{\frac{K_b}{C}} = \sqrt{\frac{1.8\times10^{-5}}{0.020}}
= \sqrt{9.0\times10^{-4}} = 0.030 = 3.0\ \% $$

$$ [\text{OH}^{-}] = C\alpha = 0.020 \times 0.030 = 6.0\times10^{-4}\ \text{mol L}^{-1} $$

$$ pOH = -\log(6.0\times10^{-4}) = 4 - 0.778 = 3.22 $$

$$ pH = 14 - 3.22 = 10.78 $$
:::

## 2.9 Solubility and solubility product principle

::: definition Solubility and solubility product
The **solubility** (S) of a salt is the number of moles of it that dissolve in one
litre of solvent to give a saturated solution at a stated temperature.

The **solubility product** ($K_{sp}$) of a sparingly soluble salt is the product
of the molar concentrations of its ions in a **saturated** solution, each raised
to the power of its coefficient in the dissociation equation.
:::

In a saturated solution of AgCl an equilibrium exists between the undissolved
solid and its ions:

AgCl(s) ⇌ Ag⁺(aq) + Cl⁻(aq)

$$ K = \frac{[\text{Ag}^{+}][\text{Cl}^{-}]}{[\text{AgCl(s)}]} $$

The concentration of a pure solid is constant, so it is absorbed into the
constant, giving $K_{sp} = [\text{Ag}^{+}][\text{Cl}^{-}]$.

::: derivation General relation between $K_{sp}$ and solubility
For a salt $\text{A}_x\text{B}_y$ of solubility $S$ mol L⁻¹,

A$_x$B$_y$(s) ⇌ $x$A$^{y+}$ + $y$B$^{x-}$

At saturation $[\text{A}^{y+}] = xS$ and $[\text{B}^{x-}] = yS$, so

$$ K_{sp} = (xS)^{x}(yS)^{y} = x^{x}y^{y}S^{(x+y)} $$
:::

| Salt type | Example | $K_{sp}$ in terms of $S$ | $S$ in terms of $K_{sp}$ |
|---|---|---|---|
| AB | AgCl, BaSO₄ | $S^{2}$ | $\sqrt{K_{sp}}$ |
| AB₂ or A₂B | PbI₂, Ag₂CrO₄ | $4S^{3}$ | $\left(K_{sp}/4\right)^{1/3}$ |
| AB₃ | Fe(OH)₃ | $27S^{4}$ | $\left(K_{sp}/27\right)^{1/4}$ |
| A₃B₂ | Ca₃(PO₄)₂ | $108S^{5}$ | $\left(K_{sp}/108\right)^{1/5}$ |

$K_{sp}$ depends only on temperature. Solubility, by contrast, depends on what
else is in the solution — which is the subject of the next two sections.

::: example Worked example 2.4 — $K_{sp}$ from solubility, and back
**Problem.** (a) The solubility of silver chloride in water at 25 °C is
$1.93\times10^{-3}$ g L⁻¹. Calculate its solubility product
(molar mass of AgCl = 143.5). (b) The solubility of silver chromate, Ag₂CrO₄, is
$6.5\times10^{-5}$ mol L⁻¹. Calculate its $K_{sp}$.

**Solution.**

(a) Molar solubility:

$$ S = \frac{1.93\times10^{-3}}{143.5} = 1.345\times10^{-5}\ \text{mol L}^{-1} $$

AgCl(s) ⇌ Ag⁺ + Cl⁻, so $[\text{Ag}^{+}] = [\text{Cl}^{-}] = S$ and

$$ K_{sp} = S^{2} = (1.345\times10^{-5})^{2} = 1.81\times10^{-10} $$

(b) Ag₂CrO₄(s) ⇌ 2Ag⁺ + CrO₄²⁻, so $[\text{Ag}^{+}] = 2S$ and
$[\text{CrO}_4^{2-}] = S$:

$$ K_{sp} = (2S)^{2}(S) = 4S^{3} = 4(6.5\times10^{-5})^{3}
= 4 \times 2.746\times10^{-13} = 1.10\times10^{-12} $$
:::

## 2.10 Common ion effect

::: definition Common ion effect
The **common ion effect** is the suppression of the ionisation of a weak
electrolyte (or of the solubility of a sparingly soluble salt) caused by the
addition of a strong electrolyte that supplies an ion **common** to the
equilibrium.
:::

It is Le Chatelier's principle applied to an ionic equilibrium. Add acetate ions
to acetic acid and the equilibrium

CH₃COOH ⇌ CH₃COO⁻ + H⁺

shifts to the left, so $[\text{H}^{+}]$ falls and the pH rises — even though more
"acid material" has been added. In the same way NH₄Cl suppresses the ionisation of
NH₄OH, and HCl suppresses that of H₂S.

| System | Added common ion | Effect |
|---|---|---|
| CH₃COOH + CH₃COONa | CH₃COO⁻ | ionisation of the acid suppressed; pH rises |
| NH₄OH + NH₄Cl | NH₄⁺ | ionisation of the base suppressed; [OH⁻] falls |
| H₂S + HCl | H⁺ | [S²⁻] falls sharply — basis of Group II analysis |
| AgCl + NaCl | Cl⁻ | solubility of AgCl falls |
| Saturated NaCl + HCl gas | Cl⁻ | pure NaCl crystallises out (salt purification) |

```figure caption="Common ion effect on the solubility of silver chloride. Adding only $0.01$ mol L⁻¹ of chloride ion depresses the solubility about 750-fold."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9,2.9))
Ksp = 1.8e-10
C = np.logspace(-8, -1, 500)
S = (-C + np.sqrt(C**2 + 4*Ksp))/2
S0 = np.sqrt(Ksp)
ax.plot(C, S, color=ACCENT, lw=2.0)
ax.axhline(S0, color=SERIES[1], lw=1.1, ls='--')
ax.text(1.3e-8, S0*1.35, 'solubility in pure water,  1.34 × 10⁻⁵ mol L⁻¹',
        fontsize=7.6, color=SERIES[1])
ax.plot([1e-2], [Ksp/1e-2], 'o', color=SERIES[1], ms=6, zorder=4)
ax.annotate('in 0.01 M NaCl:\n1.8 × 10⁻⁸ mol L⁻¹', (1e-2, Ksp/1e-2),
            textcoords='offset points', xytext=(-104, 16), fontsize=7.8,
            color=SERIES[1],
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.0,
                            mutation_scale=9))
ax.set_xscale('log'); ax.set_yscale('log')
ax.set_xlabel('concentration of added Cl⁻  (mol L⁻¹)')
ax.set_ylabel('solubility of AgCl  (mol L⁻¹)')
ax.set_xlim(1e-8, 1e-1); ax.set_ylim(1e-9, 1e-4)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=0.4)
```

::: example Worked example 2.5 — common ion effect on solubility
**Problem.** $K_{sp}$ of AgCl is $1.8\times10^{-10}$. Calculate its solubility
(a) in pure water and (b) in 0.010 M sodium chloride solution.

**Solution.**

(a) $S = \sqrt{K_{sp}} = \sqrt{1.8\times10^{-10}} = 1.34\times10^{-5}$ mol L⁻¹.

(b) Let the solubility now be $S'$. Then $[\text{Ag}^{+}] = S'$, while the
chloride comes almost entirely from the NaCl:
$[\text{Cl}^{-}] = 0.010 + S' \approx 0.010$ (because $S'$ will be tiny).

$$ K_{sp} = S' \times 0.010 \;\Longrightarrow\;
S' = \frac{1.8\times10^{-10}}{0.010} = 1.8\times10^{-8}\ \text{mol L}^{-1} $$

The solubility has fallen by a factor of about 745, since
$1.34\times10^{-5}/1.8\times10^{-8} = 745$. This is why a precipitate is always
washed with a dilute solution of a common ion rather than with pure water.
:::

## 2.11 Application of solubility product principle and common ion effect in precipitation reactions

Write $Q$ (the **ionic product**) for the product of the ion concentrations at any
moment, calculated exactly like $K_{sp}$ but for a solution that need not be
saturated. Then:

| Condition | Meaning |
|---|---|
| $Q < K_{sp}$ | unsaturated — no precipitate; more solid will dissolve |
| $Q = K_{sp}$ | exactly saturated — solid and solution in equilibrium |
| $Q > K_{sp}$ | supersaturated — precipitation occurs until $Q$ falls to $K_{sp}$ |

**Qualitative analysis.** The whole group separation scheme rests on these two
ideas.

- **Group II** (Cu²⁺, Pb²⁺, Cd²⁺, Bi³⁺, …) is precipitated as sulphides by
  passing H₂S in the presence of **dilute HCl**. The H⁺ from HCl is a common ion
  for H₂S ⇌ 2H⁺ + S²⁻, so it pushes that equilibrium far to the left and keeps
  $[\text{S}^{2-}]$ extremely low. Only the sulphides with the very smallest
  $K_{sp}$ (CuS, PbS, CdS) then satisfy $Q > K_{sp}$; ZnS, MnS and NiS do not
  precipitate.
- **Group III A** (Fe³⁺, Al³⁺, Cr³⁺) is precipitated as hydroxides by NH₄OH in
  the presence of **NH₄Cl**. The NH₄⁺ common ion suppresses the ionisation of
  NH₄OH, keeping $[\text{OH}^{-}]$ low, so only the hydroxides of very low
  $K_{sp}$ come down and Mg(OH)₂ stays in solution.
- **Group IV** sulphides (ZnS, MnS, CoS, NiS) are then precipitated by H₂S in
  **alkaline** medium, where $[\text{S}^{2-}]$ is much higher.

**Purification of common salt.** Saturated brine made from crude salt is treated
with HCl gas. The large excess of the common ion Cl⁻ makes
$Q = [\text{Na}^{+}][\text{Cl}^{-}]$ exceed $K_{sp}$ for NaCl, and pure sodium
chloride crystallises out while the more soluble impurities (MgCl₂, CaCl₂) stay in
solution.

**Salting out of soap.** Adding solid NaCl to the soap solution after
saponification raises $[\text{Na}^{+}]$, exceeds the solubility product of sodium
stearate, and the soap separates as a curd.

::: example Worked example 2.6 — will a precipitate form?
**Problem.** Equal volumes of 0.0020 M BaCl₂ and 0.0020 M Na₂SO₄ are mixed. Will
barium sulphate precipitate? $K_{sp}(\text{BaSO}_4) = 1.1\times10^{-10}$.

**Solution.** On mixing equal volumes each concentration is halved:

$$ [\text{Ba}^{2+}] = [\text{SO}_4^{2-}] = \frac{0.0020}{2} = 1.0\times10^{-3}\ \text{mol L}^{-1} $$

$$ Q = [\text{Ba}^{2+}][\text{SO}_4^{2-}] = (1.0\times10^{-3})^{2} = 1.0\times10^{-6} $$

Since $Q = 1.0\times10^{-6}$ is very much greater than
$K_{sp} = 1.1\times10^{-10}$, the solution is supersaturated and BaSO₄ **will**
precipitate. Precipitation continues until the ion product falls to
$1.1\times10^{-10}$.
:::

## 2.12 Buffer solution and its application

::: definition Buffer solution
A **buffer solution** is one that resists a change in its pH when a small amount
of a strong acid or a strong base is added to it, or when it is diluted.
:::

| Type | Made from | Example | pH |
|---|---|---|---|
| Acidic buffer | weak acid + its salt with a strong base | CH₃COOH + CH₃COONa | < 7 |
| Basic buffer | weak base + its salt with a strong acid | NH₄OH + NH₄Cl | > 7 |
| Salt-only buffer | salt of a weak acid and a weak base | CH₃COONH₄ | ≈ 7 |

::: derivation Henderson–Hasselbalch equation
For an acidic buffer, the weak acid is only slightly ionised and the salt is
completely ionised:

HA ⇌ H⁺ + A⁻  and NaA → Na⁺ + A⁻

$$ K_a = \frac{[\text{H}^{+}][\text{A}^{-}]}{[\text{HA}]} $$

The common ion A⁻ from the salt pushes the acid equilibrium far to the left, so
$[\text{HA}] \approx$ the concentration of acid taken, and $[\text{A}^{-}] \approx$
the concentration of salt taken. Hence

$$ [\text{H}^{+}] = K_a \frac{[\text{acid}]}{[\text{salt}]} $$

Taking negative logarithms,

$$ pH = pK_a + \log\frac{[\text{salt}]}{[\text{acid}]} $$

For a basic buffer the same argument gives

$$ pOH = pK_b + \log\frac{[\text{salt}]}{[\text{base}]}, \qquad pH = 14 - pOH $$
:::

**How a buffer works.** Take CH₃COOH + CH₃COONa. The mixture contains a large
reserve of un-ionised acid and a large reserve of acetate ions.

- Add H⁺: it is mopped up by the acetate reserve, CH₃COO⁻ + H⁺ → CH₃COOH. A weak,
  barely ionised acid replaces the strong acid, so the pH hardly moves.
- Add OH⁻: it is neutralised by the acid reserve, CH₃COOH + OH⁻ → CH₃COO⁻ + H₂O.

Only the **ratio** [salt]/[acid] changes, and pH depends on its logarithm, so a
large change in the ratio gives a small change in pH.

```figure caption="Buffer action. Small additions of strong acid or alkali move the buffer pH by less than $0.1$ unit, while the same addition to pure water swings it by five units. Beyond about $0.08$ mol the reserve is used up and the buffer fails."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,3.0))
Ka, Kw, CT = 1.8e-5, 1.0e-14, 0.20
x = np.linspace(-0.095, 0.095, 600)   # + = mol NaOH added, - = mol HCl added

def buffer_pH(v):
    Na = 0.10 + max(v, 0.0); Cl = max(-v, 0.0)
    lo, hi = -14.0, 0.0
    for _ in range(90):
        mid = 0.5*(lo + hi); h = 10.0**mid
        f = Na + h - Cl - Kw/h - CT*Ka/(Ka + h)
        if f < 0: lo = mid
        else: hi = mid
    return -0.5*(lo + hi)

pHb = np.array([buffer_pH(v) for v in x])
exc = -x
pHw = -np.log10((exc + np.sqrt(exc**2 + 4*Kw))/2)
ax.plot(x, pHw, color=MUTED, lw=1.7, ls='--', label='pure water')
ax.plot(x, pHb, color=ACCENT, lw=2.1,
        label='buffer (0.10 M acid + 0.10 M salt)')
ax.axvline(0, color=GRID, lw=0.9)
for v, lab, off in [(-0.010, 'add 0.01 mol HCl:\npH 4.74 → 4.66', (-46, -30)),
                    (0.010, 'add 0.01 mol NaOH:\npH 4.74 → 4.83', (6, 30))]:
    yv = buffer_pH(v)
    ax.plot([v], [yv], 'o', color=SERIES[1], ms=5, zorder=5)
    ax.annotate(lab, (v, yv), textcoords='offset points', xytext=off,
                fontsize=7.4, color=SERIES[1], ha='center',
                arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=0.9,
                                mutation_scale=8))
ax.set_xlabel('acid added ←   mol of strong acid or alkali per litre   → alkali added')
ax.set_ylabel('pH')
ax.set_xlim(-0.095, 0.095); ax.set_ylim(0, 14); ax.set_yticks(range(0, 15, 2))
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=0.4)
ax.legend(loc='upper left', fontsize=7.4)
```

::: key Buffer capacity
A buffer works best when $[\text{salt}] = [\text{acid}]$, because then
$pH = pK_a$ and the ratio can move furthest in either direction. In practice a
buffer is useful only over the range $pH = pK_a \pm 1$. Choose the weak acid whose
$pK_a$ is closest to the pH you want.
:::

**Applications of buffers.**

- **Blood** is buffered at pH 7.4 by H₂CO₃/HCO₃⁻ (with phosphate and protein
  buffers). A drift of 0.4 pH unit either way is fatal.
- Intracellular fluid is buffered by H₂PO₄⁻/HPO₄²⁻ at about pH 7.2.
- **Agriculture**: soil must be buffered near pH 6–7; acidic hill soils in Nepal
  are limed to raise and hold the pH.
- **Industry**: electroplating baths, fermentation of beer and curd, dyeing of
  textiles, sugar refining and paper manufacture all need fixed pH.
- **Pharmacy**: eye drops and injections are buffered to the pH of body fluid to
  avoid irritation.
- **Analysis**: complexometric EDTA titrations are run in an NH₄Cl/NH₄OH buffer
  at pH 10.

::: example Worked example 2.7 — preparing a buffer and testing it
**Problem.** (a) What mass of sodium acetate (molar mass 82) must be dissolved in
1.00 L of 0.10 M acetic acid to give a buffer of pH 5.00?
($K_a = 1.8\times10^{-5}$.) (b) Show that adding 0.010 mol of HCl to 1.00 L of a
buffer that is 0.10 M in acetic acid and 0.10 M in sodium acetate changes the pH
by less than 0.1 unit.

**Solution.**

(a) $pK_a = -\log(1.8\times10^{-5}) = 5 - \log 1.8 = 5 - 0.255 = 4.74$.

$$ pH = pK_a + \log\frac{[\text{salt}]}{[\text{acid}]}
\;\Longrightarrow\; 5.00 = 4.74 + \log\frac{[\text{salt}]}{0.10} $$

$$ \log\frac{[\text{salt}]}{0.10} = 0.26 \;\Longrightarrow\;
\frac{[\text{salt}]}{0.10} = 10^{0.26} = 1.80 $$

$$ [\text{salt}] = 0.180\ \text{mol L}^{-1}
\;\Longrightarrow\; w = 0.180 \times 82 = 14.8\ \text{g} $$

(b) Before addition, [salt] = [acid] = 0.10, so $pH = pK_a = 4.74$.

The added H⁺ converts 0.010 mol of acetate into acetic acid, so
[salt] = 0.090 and [acid] = 0.110:

$$ pH = 4.74 + \log\frac{0.090}{0.110} = 4.74 + \log 0.818 = 4.74 - 0.087 = 4.66 $$

The change is 0.08 pH unit. The same 0.010 mol of HCl added to a litre of pure
water would take the pH from 7 to $-\log(0.010) = 2$ — a change of five units.
:::

## 2.13 Indicators and selection of indicators in acid-base titration

::: definition Acid-base indicator
An **acid-base indicator** is a weak organic acid or base whose un-ionised form
has a different colour from its ionised form, so that the colour of the solution
signals its pH.
:::

**Ostwald's theory.** Let the indicator be a weak acid HIn:

HIn ⇌ H⁺ + In⁻  (colour A) → (colour B)

$$ K_{In} = \frac{[\text{H}^{+}][\text{In}^{-}]}{[\text{HIn}]}
\;\Longrightarrow\; pH = pK_{In} + \log\frac{[\text{In}^{-}]}{[\text{HIn}]} $$

The eye sees colour A alone when [HIn] is about ten times [In⁻], and colour B
alone when the ratio is reversed. Putting the ratio equal to $1/10$ and $10/1$
gives the **working range** of the indicator:

$$ pH = pK_{In} \pm 1 $$

In an acidic solution the high $[\text{H}^{+}]$ pushes the equilibrium left, so
phenolphthalein (whose ionised form is pink) is colourless in acid; in alkali the
H⁺ is removed and the pink In⁻ appears.

| Indicator | Range (pH) | Colour in acid | Colour in alkali |
|---|---|---|---|
| Methyl orange | 3.1 – 4.4 | red | yellow |
| Methyl red | 4.2 – 6.3 | red | yellow |
| Litmus | 5.0 – 8.0 | red | blue |
| Bromothymol blue | 6.0 – 7.6 | yellow | blue |
| Phenol red | 6.8 – 8.4 | yellow | red |
| Phenolphthalein | 8.3 – 10.0 | colourless | pink |
| Thymolphthalein | 9.3 – 10.5 | colourless | blue |

::: key The rule for selecting an indicator
Choose an indicator whose **working range lies wholly within the steep, nearly
vertical portion** of the titration curve — the part where one drop of titrant
changes the pH by several units. If the range lies outside that jump, the colour
changes too early or too late and the titration is worthless.
:::

```figure caption="Titration curves for $25.0$ cm³ of $0.1$ M acid in the flask. The curves coincide wherever the pH is fixed by excess strong acid or strong base. Only the strong-strong curve crosses both shaded ranges; a weak acid needs phenolphthalein and a weak base needs methyl orange."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.2,3.2))
Kw = 1.0e-14
V0, C0, Ct = 25.0, 0.10, 0.10
Ka_ac = 1.8e-5          # acetic acid
Ka_nh4 = Kw/1.8e-5      # ammonium ion

def solve(fn, v):
    lo, hi = -14.0, 0.0
    for _ in range(90):
        mid = 0.5*(lo + hi)
        if fn(10.0**mid, v) < 0: lo = mid
        else: hi = mid
    return -0.5*(lo + hi)

def f_ss(h, v):                      # HCl in flask, NaOH from burette
    tot = V0 + v
    return Ct*v/tot + h - C0*V0/tot - Kw/h

def f_ws(h, v):                      # CH3COOH in flask, NaOH from burette
    tot = V0 + v
    CT = C0*V0/tot
    return Ct*v/tot + h - Kw/h - CT*Ka_ac/(Ka_ac + h)

def f_sw(h, v):                      # HCl in flask, NH3 from burette
    tot = V0 + v
    NT = Ct*v/tot
    return NT*h/(h + Ka_nh4) + h - C0*V0/tot - Kw/h

V = np.linspace(0.0, 50.0, 500)
ax.axhspan(3.1, 4.4, color=SERIES[3], alpha=0.18, zorder=0)
ax.axhspan(8.3, 10.0, color=SERIES[4], alpha=0.18, zorder=0)
ax.text(30.0, 3.72, 'methyl orange', fontsize=7.4, color=INK, va='center')
ax.text(2.5, 9.18, 'phenolphthalein', fontsize=7.4, color=INK, va='center')
styles = [(f_ss, 'strong acid – strong base  (eq. pH 7.0)', ACCENT, '-', 2.6, 2),
          (f_ws, 'weak acid – strong base  (eq. pH 8.7)', SERIES[1], (0,(5,2)), 1.7, 3),
          (f_sw, 'strong acid – weak base  (eq. pH 5.3)', SERIES[2], (0,(1.4,1.6)), 1.9, 4)]
for fn, lab, col, ls, lw, z in styles:
    ax.plot(V, [solve(fn, v) for v in V], color=col, lw=lw, ls=ls, label=lab,
            zorder=z)
ax.plot([25, 25], [0, 11.4], color=MUTED, lw=0.8, ls=':', zorder=1)
ax.text(25.4, 0.5, 'equivalence\nvolume', fontsize=7.4, color=MUTED)
ax.set_xlabel('volume of 0.1 M base added  (cm³)')
ax.set_ylabel('pH')
ax.set_xlim(0, 50); ax.set_ylim(0, 14); ax.set_yticks(range(0, 15, 2))
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=0.4)
ax.legend(loc='upper left', fontsize=7.2)
```

| Titration | pH at equivalence | Why | Indicator |
|---|---|---|---|
| Strong acid vs strong base | 7 | salt not hydrolysed | methyl orange or phenolphthalein |
| Weak acid vs strong base | > 7 (≈ 8.7) | anionic hydrolysis | **phenolphthalein** |
| Strong acid vs weak base | < 7 (≈ 5.3) | cationic hydrolysis | **methyl orange** |
| Weak acid vs weak base | ≈ 7 | both ions hydrolysed | no sharp jump — no indicator works; use a pH meter |

## 2.14 Types of salts: acidic, basic, simple, complex

A salt is the product of the reaction of an acid with a base. Salts are classified
in two independent ways.

**By composition:**

| Class | Formed by | Examples |
|---|---|---|
| Normal (neutral) salt | complete replacement of all H⁺ of the acid | NaCl, Na₂SO₄, K₃PO₄ |
| Acid salt | partial replacement of the replaceable H⁺ | NaHSO₄, NaHCO₃, NaH₂PO₄ |
| Basic salt | partial replacement of the OH⁻ of a polyacidic base | Pb(OH)Cl, Zn(OH)Cl, Mg(OH)Cl |
| Double salt | two simple salts crystallised together | Mohr's salt FeSO₄·(NH₄)₂SO₄·6H₂O; potash alum K₂SO₄·Al₂(SO₄)₃·24H₂O |
| Mixed salt | one acid with two different bases, or one base with two acids | CaOCl₂ (bleaching powder), NaKSO₄ |
| Complex salt | contains a complex ion that survives in solution | K₄[Fe(CN)₆], [Cu(NH₃)₄]SO₄, K₃[Fe(CN)₆] |

::: key Double salt versus complex salt
A **double salt** exists only in the solid state: dissolve Mohr's salt and the
solution gives all the tests of Fe²⁺, NH₄⁺ and SO₄²⁻. A **complex salt** keeps its
complex ion in solution: dissolve K₄[Fe(CN)₆] and you get K⁺ and
[Fe(CN)₆]⁴⁻ — the solution gives **no** test for Fe²⁺ or CN⁻.
:::

**By the pH of their solution** (the result of hydrolysis, §2.15):

| Salt of | Nature of solution | Example |
|---|---|---|
| Strong acid + strong base | neutral, pH = 7 | NaCl, KNO₃, Na₂SO₄ |
| Weak acid + strong base | basic, pH > 7 | CH₃COONa, Na₂CO₃, KCN |
| Strong acid + weak base | acidic, pH < 7 | NH₄Cl, CuSO₄, FeCl₃ |
| Weak acid + weak base | depends on $K_a$ vs $K_b$ | CH₃COONH₄ (≈ 7) |

Note that an *acid salt* is not the same thing as an *acidic salt*: NaHCO₃ is an
acid salt by composition but its solution is **alkaline**, because the carbonic
acid it comes from is much weaker than the base NaOH.

## 2.15 Hydrolysis of salts

::: definition Salt hydrolysis
**Hydrolysis** is the reaction of the cation or the anion of a dissolved salt with
water to produce the parent acid or base, making the solution acidic or alkaline.
It is the reverse of neutralisation.
:::

**Case 1 — salt of a strong acid and a strong base (NaCl).**

NaCl → Na⁺ + Cl⁻. Neither ion reacts with water: Na⁺ would give NaOH, a strong
base which is completely ionised again, and Cl⁻ would give HCl, likewise. There
is **no hydrolysis**; the solution is neutral, pH 7.

**Case 2 — salt of a weak acid and a strong base (CH₃COONa): anionic hydrolysis.**

CH₃COO⁻ + H₂O ⇌ CH₃COOH + OH⁻

The acetate ion takes a proton from water, leaving OH⁻ behind; the solution is
**alkaline**.

::: derivation pH of a salt of a weak acid and a strong base
Let $C$ be the concentration of the salt and $h$ its degree of hydrolysis.

| | CH₃COO⁻ | + H₂O ⇌ | CH₃COOH | + | OH⁻ |
|---|---|---|---|---|---|
| initial | $C$ | | 0 | | 0 |
| equilibrium | $C(1-h)$ | | $Ch$ | | $Ch$ |

$$ K_h = \frac{[\text{CH}_3\text{COOH}][\text{OH}^{-}]}{[\text{CH}_3\text{COO}^{-}]}
= \frac{Ch^{2}}{1-h} \approx Ch^{2} $$

Multiplying numerator and denominator of $K_h$ by $[\text{H}^{+}]$ and recognising
$K_a$ and $K_w$,

$$ K_h = \frac{K_w}{K_a}, \qquad h = \sqrt{\frac{K_h}{C}} = \sqrt{\frac{K_w}{K_aC}} $$

Since $[\text{OH}^{-}] = Ch = \sqrt{K_hC} = \sqrt{K_wC/K_a}$, taking logarithms
gives

$$ pH = 7 + \tfrac{1}{2}pK_a + \tfrac{1}{2}\log C $$
:::

**Case 3 — salt of a strong acid and a weak base (NH₄Cl): cationic hydrolysis.**

NH₄⁺ + H₂O ⇌ NH₄OH + H⁺

The solution is **acidic**. By exactly the same argument,

$$ K_h = \frac{K_w}{K_b}, \qquad h = \sqrt{\frac{K_w}{K_bC}}, \qquad
pH = 7 - \tfrac{1}{2}pK_b - \tfrac{1}{2}\log C $$

**Case 4 — salt of a weak acid and a weak base (CH₃COONH₄).** Both ions hydrolyse
and

$$ K_h = \frac{K_w}{K_aK_b}, \qquad h = \sqrt{\frac{K_w}{K_aK_b}}, \qquad
pH = 7 + \tfrac{1}{2}pK_a - \tfrac{1}{2}pK_b $$

Notice that here the degree of hydrolysis and the pH are **independent of
concentration** — a favourite one-mark point. Dilution does not change the pH of
an ammonium acetate solution.

| Salt of | Ion hydrolysed | $K_h$ | Nature |
|---|---|---|---|
| SA + SB | none | — | neutral |
| WA + SB | anion | $K_w/K_a$ | alkaline |
| SA + WB | cation | $K_w/K_b$ | acidic |
| WA + WB | both | $K_w/(K_aK_b)$ | depends on $K_a$ vs $K_b$ |

::: example Worked example 2.8 — hydrolysis of sodium acetate
**Problem.** Calculate the hydrolysis constant, the degree of hydrolysis and the
pH of a 0.10 M solution of sodium acetate at 25 °C.
$K_a(\text{CH}_3\text{COOH}) = 1.8\times10^{-5}$, $K_w = 1.0\times10^{-14}$.

**Solution.**

$$ K_h = \frac{K_w}{K_a} = \frac{1.0\times10^{-14}}{1.8\times10^{-5}}
= 5.56\times10^{-10} $$

$$ h = \sqrt{\frac{K_h}{C}} = \sqrt{\frac{5.56\times10^{-10}}{0.10}}
= \sqrt{5.56\times10^{-9}} = 7.45\times10^{-5} $$

so only about 0.0075 % of the acetate is hydrolysed.

$$ [\text{OH}^{-}] = Ch = 0.10 \times 7.45\times10^{-5} = 7.45\times10^{-6}\ \text{mol L}^{-1} $$

$$ pOH = -\log(7.45\times10^{-6}) = 6 - 0.872 = 5.13, \qquad pH = 14 - 5.13 = 8.87 $$

The standard formula gives the same result:
$pH = 7 + \frac{1}{2}(4.74) + \frac{1}{2}(-1) = 7 + 2.37 - 0.50 = 8.87$.
:::

## Chapter summary

- Arrhenius acids/bases work only in water; Bronsted-Lowry defines acid = proton
  donor, base = proton acceptor, giving conjugate pairs that differ by one H⁺;
  Lewis defines acid = electron-pair acceptor, base = electron-pair donor.
- For a conjugate pair $K_a \times K_b = K_w$ and $pK_a + pK_b = 14$; the stronger
  the acid, the weaker its conjugate base.
- Ostwald's dilution law: $K = C\alpha^{2}/(1-\alpha) \approx C\alpha^{2}$, so
  $\alpha = \sqrt{K/C} = \sqrt{KV}$. It fails for strong electrolytes.
- $K_w = [\text{H}^{+}][\text{OH}^{-}] = 1.0\times10^{-14}$ at 25 °C;
  $pH + pOH = 14$. $K_w$ rises with temperature, so neutral pH falls below 7 on
  heating.
- pH master formulas: strong acid $pH = -\log C$; weak acid
  $pH = \frac{1}{2}(pK_a - \log C)$; strong base $pH = 14 + \log C$; weak base
  $pOH = \frac{1}{2}(pK_b - \log C)$.
- $K_{sp} = x^{x}y^{y}S^{(x+y)}$ for A$_x$B$_y$. Precipitation occurs when the
  ionic product $Q > K_{sp}$; the common ion effect lowers solubility and
  suppresses the ionisation of weak electrolytes.
- Buffers: $pH = pK_a + \log([\text{salt}]/[\text{acid}])$ and
  $pOH = pK_b + \log([\text{salt}]/[\text{base}])$; capacity is greatest at
  $pH = pK_a$ and useful over $pK_a \pm 1$.
- Choose an indicator whose range lies inside the vertical part of the titration
  curve: phenolphthalein (8.3–10.0) for weak acid vs strong base, methyl orange
  (3.1–4.4) for strong acid vs weak base, either for strong vs strong.
- Hydrolysis: WA+SB gives $pH = 7 + \frac{1}{2}pK_a + \frac{1}{2}\log C$
  (alkaline); SA+WB gives $pH = 7 - \frac{1}{2}pK_b - \frac{1}{2}\log C$ (acidic);
  WA+WB gives $pH = 7 + \frac{1}{2}pK_a - \frac{1}{2}pK_b$, independent of
  concentration.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The conjugate base of HSO₄⁻ is <span class="marks">[1]</span>
   (a) H₂SO₄ (b) SO₄²⁻ (c) H₂O (d) OH⁻
2. Which of the following is a Lewis acid but **not** a Bronsted acid? <span class="marks">[1]</span>
   (a) HCl (b) NH₄⁺ (c) BF₃ (d) CH₃COOH
3. The pH of a 0.001 M solution of NaOH at 25 °C is <span class="marks">[1]</span>
   (a) 3 (b) 7 (c) 11 (d) 14
4. On dilution, the degree of ionisation of a weak electrolyte <span class="marks">[1]</span>
   (a) decreases (b) increases (c) remains the same (d) becomes zero
5. An aqueous solution of ammonium chloride is <span class="marks">[1]</span>
   (a) neutral (b) acidic (c) alkaline (d) amphoteric
6. The indicator most suitable for the titration of acetic acid against sodium
   hydroxide is <span class="marks">[1]</span>
   (a) methyl orange (b) methyl red (c) phenolphthalein (d) any of them
7. If the solubility of a salt AB₂ is $S$ mol L⁻¹, its solubility product is <span class="marks">[1]</span>
   (a) $S^{2}$ (b) $2S^{3}$ (c) $4S^{3}$ (d) $S^{3}$

::: note Answers to Group A
**1.** (b) — removing one proton from HSO₄⁻ leaves SO₄²⁻.
**2.** (c) — BF₃ has no proton to donate but an empty p orbital to accept a lone pair.
**3.** (c) — $pOH = -\log 10^{-3} = 3$, so $pH = 14 - 3 = 11$.
**4.** (b) — Ostwald's law, $\alpha = \sqrt{K/C}$, and $C$ falls on dilution.
**5.** (b) — NH₄⁺ hydrolyses to give H⁺ (salt of strong acid + weak base).
**6.** (c) — the equivalence pH is about 8.7, inside the phenolphthalein range 8.3–10.0.
**7.** (c) — AB₂ ⇌ A²⁺ + 2B⁻, so $K_{sp} = (S)(2S)^{2} = 4S^{3}$.
:::

**Group B — Short answer (5 marks each)**

1. State the limitations of the Arrhenius concept of acids and bases, and show
   how the Bronsted-Lowry concept removes them. Identify the conjugate acid-base
   pairs in HCO₃⁻ + H₂O ⇌ H₂CO₃ + OH⁻. <span class="marks">[5]</span>
2. State and derive Ostwald's dilution law. Why does it fail for strong
   electrolytes? <span class="marks">[5]</span>
3. Calculate the pH and the degree of ionisation of a 0.020 M solution of a weak
   monobasic acid whose $K_a$ is $2.0\times10^{-5}$. <span class="marks">[5]</span>
4. What is a buffer solution? Derive the Henderson equation for an acidic buffer
   and calculate the pH of a solution that is 0.20 M in CH₃COOH and 0.10 M in
   CH₃COONa. ($pK_a = 4.74$) <span class="marks">[5]</span>
5. Define solubility product. The solubility of Mg(OH)₂ in water is
   $1.65\times10^{-4}$ mol L⁻¹. Calculate its solubility product. <span class="marks">[5]</span>
6. What is meant by hydrolysis of a salt? Explain, with equations, why an aqueous
   solution of sodium carbonate is alkaline while that of ferric chloride is
   acidic. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Limitations: restricted to water; free H⁺ cannot exist; cannot explain
acids without H (CO₂, BF₃) or bases without OH (NH₃); ignores the solvent. The
Bronsted definition needs only a proton transfer, so it works in any solvent and
classifies NH₃ as a base and NH₄⁺ as an acid. In the given equation the pairs are
HCO₃⁻ / H₂CO₃ (base / its conjugate acid) and H₂O / OH⁻ (acid / its conjugate
base).

**3.** Using $[\text{H}^{+}] = \sqrt{K_aC}$,

$$ [\text{H}^{+}] = \sqrt{2.0\times10^{-5}\times 0.020} = \sqrt{4.0\times10^{-7}} = 6.32\times10^{-4}\ \text{mol L}^{-1} $$

so $pH = 4 - \log 6.32 = 4 - 0.801 = 3.20$. And
$\alpha = \sqrt{K_a/C} = \sqrt{1.0\times10^{-3}} = 3.16\times10^{-2}$, i.e. 3.16 per cent.

**4.** $pH = pK_a + \log([\text{salt}]/[\text{acid}])$, so
$pH = 4.74 + \log(0.10/0.20) = 4.74 - 0.301 = 4.44$.

**5.** Mg(OH)₂ ⇌ Mg²⁺ + 2OH⁻, so $K_{sp} = (S)(2S)^{2} = 4S^{3}$ and
$K_{sp} = 4(1.65\times10^{-4})^{3} = 4 \times 4.49\times10^{-12} = 1.80\times10^{-11}$.

**6.** Hydrolysis is the reaction of the ions of a salt with water to regenerate
the parent acid or base. Na₂CO₃ is the salt of the weak acid H₂CO₃ and the strong
base NaOH, so the anion hydrolyses: CO₃²⁻ + H₂O ⇌ HCO₃⁻ + OH⁻, releasing OH⁻ and
making the solution alkaline. FeCl₃ is the salt of the strong acid HCl and the
weak base Fe(OH)₃, so the cation hydrolyses:
Fe³⁺ + 3H₂O ⇌ Fe(OH)₃ + 3H⁺, releasing H⁺ and making the solution acidic.
:::

**Group C — Long answer (8 marks each)**

1. (a) Define pH and derive the expression for the pH of a weak monobasic
   acid. <span class="marks">[3]</span>
   (b) Calculate the pH of 0.10 M ammonium hydroxide
   ($K_b = 1.8\times10^{-5}$), and the pH of the solution obtained when 0.10 mol
   of NH₄Cl is dissolved in 1.00 L of that ammonia solution. <span class="marks">[5]</span>
2. (a) What is the common ion effect? Explain how it and the solubility product
   principle are used to separate Group II from Group IV cations in qualitative
   analysis. <span class="marks">[4]</span>
   (b) The solubility product of AgCl is $1.8\times10^{-10}$. Calculate its
   solubility in pure water and in 0.10 M AgNO₃ solution. <span class="marks">[4]</span>
3. (a) State Ostwald's theory of indicators and derive the working range of an
   indicator. <span class="marks">[4]</span>
   (b) Sketch the titration curve for a weak acid against a strong base, mark the
   equivalence point, and justify the choice of phenolphthalein rather than
   methyl orange. <span class="marks">[4]</span>

::: note Answers to Group C
**1.(b)** For the ammonia alone,
$[\text{OH}^{-}] = \sqrt{K_bC} = \sqrt{1.8\times10^{-6}} = 1.34\times10^{-3}$
mol L⁻¹, so $pOH = 2.87$ and $pH = 11.13$.

Adding NH₄Cl creates a basic buffer with [base] = [salt] = 0.10 M:

$$ pOH = pK_b + \log\frac{[\text{salt}]}{[\text{base}]} = 4.74 + \log 1 = 4.74 $$

so $pH = 14 - 4.74 = 9.26$. The common ion NH₄⁺ has suppressed the ionisation of
the base and lowered the pH by nearly two units.

**2.(a)** The common ion effect is the suppression of the ionisation of a weak
electrolyte by adding a strong electrolyte with an ion in common. H₂S is a weak
acid; in the presence of dilute HCl the common ion H⁺ drives
H₂S ⇌ 2H⁺ + S²⁻ to the left, so $[\text{S}^{2-}]$ is very small. Only the Group II
sulphides, whose $K_{sp}$ values are extremely small, then reach
$Q > K_{sp}$ and precipitate. In Group IV the solution is made alkaline with
NH₄OH; the OH⁻ removes H⁺, $[\text{S}^{2-}]$ rises by many powers of ten, and the
more soluble sulphides ZnS, MnS, CoS and NiS now satisfy $Q > K_{sp}$.

**2.(b)** In pure water $S = \sqrt{K_{sp}} = 1.34\times10^{-5}$ mol L⁻¹.

In 0.10 M AgNO₃, $[\text{Ag}^{+}] \approx 0.10$, so

$$ S' = \frac{K_{sp}}{[\text{Ag}^{+}]} = \frac{1.8\times10^{-10}}{0.10}
= 1.8\times10^{-9}\ \text{mol L}^{-1} $$

about 7450 times smaller.

**3.(b)** The curve starts near pH 2.9, rises quickly, flattens into a buffer
region around $pH = pK_a = 4.74$ at half-neutralisation, then jumps steeply to the
equivalence point at pH ≈ 8.7 (alkaline because of anionic hydrolysis of the
acetate formed) and levels off near pH 12–13. The vertical portion runs only from
about pH 7 to pH 11. Phenolphthalein (8.3–10.0) lies inside that jump, so its
colour changes within one drop of the equivalence point. Methyl orange (3.1–4.4)
lies far below it, in the buffer region, and would change colour long before the
acid was neutralised.
:::
