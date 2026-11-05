---
subject: Chemistry
grade: CEE
unit: 8
title: Volumetric Analysis
hours: 1
area: Physical Chemistry
---

Volumetric analysis is the branch of the paper where chemistry becomes a measurement: a
solution of known strength is run from a burette into a measured volume of the unknown
until the reaction is just complete. It carries about **one question** (our estimate from
the MEC topic list), and that question is nearly always arithmetic — an equivalent weight,
a conversion between two concentration units, or a titration volume from
$N_1V_1 = N_2V_2$. The definitions are few; the marks are lost on units, on the n-factor
of the reagent, and on the difference between molality and molarity.

::: key What the paper asks from this chapter
- Equivalent weight $E = M/n$, where the n-factor is the basicity of an acid, the acidity of a base, the total charge of the cation of a salt, or the number of electrons gained or lost by an oxidant or reductant.
- **KMnO₄ has three n-factors**: 5 in acidic medium (to Mn²⁺), 3 in neutral (to MnO₂), 1 in strongly alkaline (to MnO₄²⁻). K₂Cr₂O₇ is always 6.
- Molarity = mol solute per litre of **solution**; molality = mol solute per kg of **solvent**; normality = molarity × n-factor.
- The one conversion that needs the density: $M = \dfrac{10 \times \%\text{w/w} \times d}{M_B}$.
- ppm = mg per kg (≈ mg L⁻¹ in dilute water), ppb = μg per kg; mole fraction = $n_i/\sum n$.
- Dilution: $M_1V_1 = M_2V_2$ — the number of moles does not change.
- A **primary standard** is pure, stable, non-hygroscopic and of high molar mass (oxalic acid, Na₂CO₃, KHP, borax, K₂Cr₂O₇); NaOH, HCl, KMnO₄ and Na₂S₂O₃ are **secondary** and must be standardised.
- Law of equivalence: $N_1V_1 = N_2V_2$; equivalents $= NV(\text{L}) = \text{mass}/E$. In a back titration the excess is subtracted.
:::

## 8.1 Equivalent weight and every concentration unit

### What a titration is

::: definition Volumetric analysis
**Volumetric analysis** is the quantitative determination of the concentration of a
solution by measuring the volume of another solution of known concentration that reacts
with it completely.
:::

| Term | Meaning |
|---|---|
| titrant | the solution of known concentration, run from the burette |
| analyte (titrand) | the solution being measured, pipetted into the conical flask |
| standard solution | a solution whose concentration is accurately known |
| equivalence point | the point at which the reactants have combined in the exact stoichiometric ratio |
| end point | the point at which the indicator changes colour — the *observed* approximation to the equivalence point |
| titration error | the difference between the end point and the equivalence point |

The whole method rests on one measurement: the **volume** delivered. Everything else is a
conversion from that volume to an amount of substance.

### Equivalent weight and the n-factor

::: definition Equivalent weight
The **equivalent weight** $E$ of a substance is the mass of it that supplies, consumes or
is associated with **one mole of H⁺, one mole of OH⁻ or one mole of electrons** in the
reaction concerned.
$$ E = \frac{M}{n} $$
where $M$ is the molar mass and $n$ is the **n-factor** (the number of equivalents per
mole).
:::

The n-factor is not a property of the substance alone — it is a property of the substance
**in a particular reaction**. That is why KMnO₄ has three different equivalent weights.

| Substance | Reaction role | n-factor | $E$ (g eq⁻¹) |
|---|---|---|---|
| HCl | acid (basicity 1) | 1 | 36.5 |
| CH₃COOH | acid (basicity 1) | 1 | 60 |
| H₂SO₄ | acid (basicity 2) | 2 | 49 |
| H₃PO₄ | acid (basicity 3) | 3 | 32.7 |
| NaOH | base (acidity 1) | 1 | 40 |
| Ca(OH)₂ | base (acidity 2) | 2 | 37 |
| Na₂CO₃ | salt, 2 H⁺ accepted | 2 | 53 |
| NaHCO₃ | salt, 1 H⁺ accepted | 1 | 84 |
| KMnO₄ (acidic) | Mn⁷⁺ → Mn²⁺, 5 e⁻ | 5 | 31.6 |
| KMnO₄ (neutral) | Mn⁷⁺ → Mn⁴⁺, 3 e⁻ | 3 | 52.7 |
| KMnO₄ (alkaline) | Mn⁷⁺ → Mn⁶⁺, 1 e⁻ | 1 | 158 |
| K₂Cr₂O₇ (acidic) | 2 Cr⁶⁺ → 2 Cr³⁺, 6 e⁻ | 6 | 49 |
| FeSO₄ | Fe²⁺ → Fe³⁺, 1 e⁻ | 1 | 152 |
| H₂C₂O₄·2H₂O | C₂O₄²⁻ → 2CO₂, 2 e⁻ | 2 | 63 |
| Na₂S₂O₃ | 2S₂O₃²⁻ → S₄O₆²⁻, 2 e⁻ for two | 1 | 158 |
| I₂ | I₂ → 2I⁻, 2 e⁻ | 2 | 127 |

::: caution The n-factor traps
- **H₃PO₄** is tribasic, so $E = 98/3 = 32.7$ when all three hydrogens are replaced. In a
  reaction that replaces only one, $E = 98$; only two, $E = 49$. Read what the equation does.
- **Na₂CO₃** with HCl to the **methyl orange** end point (all the way to CO₂) has $n = 2$
  and $E = 53$. To the **phenolphthalein** end point it stops at NaHCO₃ and $n = 1$,
  $E = 106$.
- **Na₂S₂O₃** has $n = 1$, not 2, because the two sulphur atoms in one formula unit lose
  one electron each between them.
- **Oxalic acid** as the dihydrate has $M = 126$, so $E = 63$; the anhydrous acid gives 45.
:::

::: example Equivalent weight from an equation
**Problem.** Find the equivalent weight of KMnO₄ when it oxidises oxalate in acid:
2KMnO₄ + 5H₂C₂O₄ + 3H₂SO₄ → K₂SO₄ + 2MnSO₄ + 10CO₂ + 8H₂O. (K = 39, Mn = 55, O = 16)

**Solution.** Manganese goes from +7 in MnO₄⁻ to +2 in Mn²⁺, a gain of 5 electrons per
formula unit, so $n = 5$. $M = 39 + 55 + 64 = 158$, hence $E = 158/5 = 31.6$ g eq⁻¹.
The same reaction shows oxalate losing 2 electrons per H₂C₂O₄, so its $E = 90/2 = 45$.
:::

### The concentration units

| Unit | Definition | Formula |
|---|---|---|
| % w/w | mass of solute per 100 g of **solution** | $\dfrac{m_{\text{solute}}}{m_{\text{solution}}}\times 100$ |
| % w/v | mass of solute per 100 mL of solution | $\dfrac{m_{\text{solute}}\text{ (g)}}{V\text{ (mL)}}\times 100$ |
| g L⁻¹ | mass of solute per litre of solution | $m/V$ |
| **Molarity** $M$ | moles of solute per litre of **solution** | $\dfrac{n}{V(\text{L})}$ |
| **Molality** $m$ | moles of solute per kilogram of **solvent** | $\dfrac{n}{m_{\text{solvent}}(\text{kg})}$ |
| **Normality** $N$ | equivalents of solute per litre of solution | $\dfrac{\text{eq}}{V(\text{L})} = M \times n\text{-factor}$ |
| **Formality** $F$ | formula masses per litre of solution | $\dfrac{\text{formula mass}}{\text{L}}$ |
| ppm | parts per million by mass | $\dfrac{m_{\text{solute}}}{m_{\text{solution}}}\times 10^{6}$ ≈ mg kg⁻¹ |
| ppb | parts per billion by mass | $\dfrac{m_{\text{solute}}}{m_{\text{solution}}}\times 10^{9}$ = μg kg⁻¹ |
| mole fraction $x$ | moles of one component ÷ total moles | $\dfrac{n_i}{n_1+n_2+\dots}$ |

**Molarity from percentage and density.** This is the conversion the paper actually asks,
and it needs the density because a percentage is by mass while molarity is by volume:

::: derivation $M = \dfrac{10 \times \%\text{w/w} \times d}{M_B}$
**Setting up.** Take exactly 100 g of solution. It contains $p$ grams of solute
($p$ = the percentage) and has density $d$ g mL⁻¹.

**Step 1 — the volume of 100 g.** $V = \dfrac{100}{d}$ mL $= \dfrac{0.1}{d}$ L.

**Step 2 — the moles of solute.** $n = \dfrac{p}{M_B}$.

**Step 3 — divide.**
$$ M = \frac{n}{V} = \frac{p/M_B}{0.1/d} = \frac{10\,p\,d}{M_B} $$

**Result.** $M = \dfrac{10 \times \%\text{w/w} \times d}{M_B}$ with $d$ in g mL⁻¹.

**What it means.** A percentage tells you nothing about molarity until you know how heavy
the solution is. The factor 10 comes from 1000 mL ÷ 100 g.
:::

::: example 98 % sulphuric acid
**Problem.** Concentrated sulphuric acid is 98 % w/w H₂SO₄ and has density 1.84 g mL⁻¹.
Find its molarity and normality. ($M_{\text{H}_2\text{SO}_4} = 98$)

**Solution.** $M = \dfrac{10 \times 98 \times 1.84}{98} = 18.4$ mol L⁻¹.
Sulphuric acid has two replaceable hydrogens, so $N = 2 \times 18.4 = 36.8$ N.
This is why concentrated H₂SO₄ is described as "18 M" in the laboratory.
:::

::: example Molality of a glucose solution
**Problem.** A 10 % w/w aqueous glucose solution contains 10 g of glucose (M = 180) in
90 g of water. Find its molality.

**Solution.** $n = 10/180 = 0.0556$ mol; solvent = 90 g = 0.090 kg.
$m = 0.0556/0.090 = 0.617$ mol kg⁻¹.
Note that the denominator is the mass of **water**, not the mass of the solution (100 g).
Using 0.100 kg gives 0.556, the classic wrong option.
:::

::: example ppm, ppb and mole fraction
**Problem.** (a) 0.020 g of Ca²⁺ is dissolved in 1.00 kg of water. Express this in ppm.
(b) A sample contains 5 μg of arsenic per kg. Express this in ppb. (c) 36 g of water is
mixed with 46 g of ethanol. Find the mole fraction of ethanol.

**Solution.** (a) $0.020\ \text{g} = 20$ mg in 1.00 kg, so **20 ppm**.
(b) 5 μg kg⁻¹ = **5 ppb** (1 ppb = 1 μg kg⁻¹).
(c) Water: 36/18 = 2 mol; ethanol: 46/46 = 1 mol; total 3 mol.
$x_{\text{ethanol}} = 1/3 = 0.333$. The mole fractions of all components add to 1.
:::

::: caution Molarity, molality and normality — the three confusions
- **Molarity is per litre of solution; molality is per kilogram of solvent.** Molarity
  changes when the solution is warmed (the volume expands); molality does not, which is why
  colligative-property work uses molality.
- **Normality is molarity times the n-factor**, so the same solution can be 0.1 M and
  0.5 N (KMnO₄ in acid). Never write "0.1 N KMnO₄" and then use 0.1 as the molarity.
- **ppm is a mass ratio**, so it equals mg L⁻¹ only for dilute aqueous solutions, where
  1 L weighs about 1 kg. For a concentrated or non-aqueous solution the two differ.
:::

```figure caption="The concentration ladder of this chapter: percentage to molarity needs the density, and molarity to normality needs the n-factor. Molality and the mass ratios (ppm, ppb) sit off the ladder."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.0,3.0))
def box(x, y, w, h, txt, fc='#dce8f4', fs=9.4):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.012,rounding_size=0.025',
                                fc=fc, ec=MUTED, lw=0.9))
    ax.text(x+w/2, y+h/2, txt, ha='center', va='center', fontsize=fs, color=INK)
box(0.22, 0.74, 0.34, 0.16, '% w/w')
box(0.22, 0.42, 0.34, 0.16, 'MOLARITY  M')
box(0.22, 0.10, 0.34, 0.16, 'NORMALITY  N')
for y0 in (0.735, 0.415):
    ax.annotate('', xy=(0.39, y0-0.145), xytext=(0.39, y0),
                arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.4, mutation_scale=11))
ax.text(0.41, 0.665, '× 10 d / M_B', fontsize=8.6, color=ACCENT, va='center')
ax.text(0.41, 0.345, '× n-factor', fontsize=8.6, color=ACCENT, va='center')
ax.text(0.63, 0.50, 'molality  m\nmol per kg\nof solvent', fontsize=8.4, color=MUTED, va='center')
ax.text(0.63, 0.14, 'ppm, ppb and\nmole fraction are\nseparate ratios', fontsize=8.4, color=MUTED, va='center')
ax.set_xlim(0, 1); ax.set_ylim(0.05, 0.98); ax.axis('off')
```

### Dilution

Diluting a solution adds solvent but not solute, so the number of moles is unchanged:

$$ M_1V_1 = M_2V_2 \qquad N_1V_1 = N_2V_2 $$

::: example Diluting an acid
**Problem.** What volume of 2.0 M HCl is needed to prepare 500 mL of 0.10 M HCl?

**Solution.** $V_1 = \dfrac{M_2V_2}{M_1} = \dfrac{0.10 \times 500}{2.0} = 25$ mL.
Measure 25 mL of the concentrated acid into a 500 mL volumetric flask and make up to the
mark with water. (Acid into water, never water into acid.)
:::

## 8.2 Primary and secondary standards; the law of equivalence

### Primary and secondary standards

::: definition Primary standard
A **primary standard** is a substance pure enough and stable enough to be weighed
directly and dissolved to give a solution of accurately known concentration, without
standardising it against anything else.
:::

| Quality of a primary standard | Why it matters |
|---|---|
| very high purity (99.9 % or better) | the mass weighed is the mass of the substance |
| stable in air — not hygroscopic, not efflorescent, not oxidised | the mass does not drift while you weigh it |
| high molar mass | a weighing error of 1 mg is a smaller fraction of a larger mass |
| readily soluble in water | it must dissolve completely and quickly |
| reacts rapidly and stoichiometrically | a sharp end point, a known equation |
| non-toxic and reasonably cheap | it is used in every laboratory |

| Primary standards | Used to standardise |
|---|---|
| oxalic acid H₂C₂O₄·2H₂O | NaOH, KMnO₄ |
| anhydrous sodium carbonate Na₂CO₃ | HCl, H₂SO₄ |
| potassium hydrogen phthalate (KHP) | NaOH |
| borax Na₂B₄O₇·10H₂O | HCl |
| potassium dichromate K₂Cr₂O₇ | Na₂S₂O₃, Fe²⁺ solutions |
| sodium chloride NaCl | AgNO₃ |
| pure zinc or copper | EDTA, iodine |
| Mohr's salt FeSO₄·(NH₄)₂SO₄·6H₂O | KMnO₄, K₂Cr₂O₇ |

::: definition Secondary standard
A **secondary standard** is a solution whose concentration is found by titrating it
against a primary standard. Its own solute is not pure or stable enough to be weighed
directly.
:::

| Secondary standard | Why it cannot be a primary standard |
|---|---|
| NaOH, KOH | hygroscopic; absorb CO₂ from the air, so the effective concentration drifts |
| HCl, H₂SO₄ | HCl is volatile; both absorb water and their strength varies |
| KMnO₄ | decomposes slowly, oxidises water and traces of organic matter; light-sensitive |
| Na₂S₂O₃ | decomposes in acid and is attacked by CO₂ and bacteria; concentration falls with time |
| I₂ | volatile and slightly soluble in water; solutions change strength on standing |

::: caution "Pure" is not the same as "primary"
Analytical-grade NaOH is sold as pure pellets, yet it still cannot be a primary standard,
because it takes water and CO₂ out of the air the moment the bottle is opened. Purity at
the factory and stability on the balance are different requirements, and the paper tests
the second one.
:::

### The law of equivalence and the normality equation

::: definition Law of equivalence
At the equivalence point, the number of equivalents of the titrant equals the number of
equivalents of the analyte:
$$ N_1V_1 = N_2V_2 $$
where $N$ is normality in eq L⁻¹ and $V$ is volume in the same unit on both sides.
:::

Equivalents can be counted in three ways, and all three must agree:

$$ \text{equivalents} = N \times V(\text{L}) = \frac{\text{mass}}{E} = n\text{-factor} \times \text{moles} $$

That identity is what makes normality so convenient: it removes the coefficients from the
calculation. Twenty millilitres of 0.1 N acid neutralises exactly twenty millilitres of
0.1 N base, whatever the acid and whatever the base, because "equivalent" already means
"capable of reacting with one mole of the other partner".

```photo id="chem12/volflask" caption="A 500 cm³ volumetric flask: the single mark on the narrow neck is the volume it is calibrated to contain." width="32"
```


::: example Acid against base, by both routes
**Problem.** 25.0 mL of 0.100 M Na₂CO₃ is titrated with 0.200 M HCl to the methyl orange
end point. Find the volume of acid used.

**Solution — normality route.** Na₂CO₃ has $n = 2$, so $N = 0.200$ N. HCl has $n = 1$, so
$N = 0.200$ N. Then $N_1V_1 = N_2V_2$ gives $0.200 \times 25.0 = 0.200 \times V_2$, so
$V_2 = 25.0$ mL.

**Solution — mole route.** Na₂CO₃ + 2HCl → 2NaCl + H₂O + CO₂. Moles of Na₂CO₃ =
$0.100 \times 0.0250 = 2.50 \times 10^{-3}$ mol; HCl needed = $5.00 \times 10^{-3}$ mol;
$V = 5.00 \times 10^{-3}/0.200 = 0.0250$ L = 25.0 mL. Both routes agree.
:::

::: example A redox titration
**Problem.** 25.0 mL of a solution of oxalic acid is exactly decolourised by 20.0 mL of
0.0200 M KMnO₄ in acidic medium. Find the normality and the strength of the oxalic acid
in g L⁻¹. ($E_{\text{oxalic}} = 63$)

**Solution.** KMnO₄ in acid has $n = 5$, so $N = 0.0200 \times 5 = 0.100$ N.
$N_1V_1 = N_2V_2$: $N_{\text{oxalic}} \times 25.0 = 0.100 \times 20.0$, so
$N_{\text{oxalic}} = 0.0800$ N.
Strength $= N \times E = 0.0800 \times 63 = 5.04$ g L⁻¹.
:::

### Back titration

A **back titration** is used when the reaction is slow, when the analyte is insoluble, or
when the end point is hard to see. A measured **excess** of a standard reagent is added,
the mixture is left to react completely, and the unreacted excess is then titrated:

$$ \text{equivalents used by the sample} = N_1V_1 - N_2V_2 $$

where $N_1V_1$ refers to the excess reagent added and $N_2V_2$ to the unreacted part.

```figure caption="The three steps of a back titration. The sample never has to be titrated directly: the excess of reagent is what the burette measures."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.0,2.6))
def box(x, y, w, txt, fc):
    ax.add_patch(FancyBboxPatch((x, y), w, 0.26, boxstyle='round,pad=0.015,rounding_size=0.03',
                                fc=fc, ec=MUTED, lw=0.9))
    ax.text(x+w/2, y+0.13, txt, ha='center', va='center', fontsize=8.6, color=INK)
box(0.01, 0.62, 0.30, 'sample\n+ measured excess\nof standard reagent', '#dce8f4')
box(0.345, 0.62, 0.30, 'react completely\n(sample is used up,\nreagent is left over)', '#f2f4f7')
box(0.68, 0.62, 0.30, 'titrate the excess\nwith a second\nstandard solution', '#f2f4f7')
box(0.345, 0.10, 0.30, 'equivalents used\n= N₁V₁ − N₂V₂', '#f7ecd9')
for x0, x1 in [(0.315, 0.340), (0.650, 0.675)]:
    ax.annotate('', xy=(x1, 0.75), xytext=(x0, 0.75),
                arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.3, mutation_scale=10))
ax.annotate('', xy=(0.495, 0.37), xytext=(0.495, 0.60),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.1, mutation_scale=9))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
```

::: example Back titration of impure limestone
**Problem.** 1.20 g of impure CaCO₃ is dissolved in 50.0 mL of 0.500 N HCl. The excess
acid needs 20.0 mL of 0.250 N NaOH for neutralisation. Find the percentage of CaCO₃ in
the sample. (Ca = 40, C = 12, O = 16; $E_{\text{CaCO}_3} = 50$)

**Solution.** Equivalents of HCl taken $= 0.500 \times 0.0500 = 0.0250$.
Equivalents of HCl left $= 0.250 \times 0.0200 = 0.00500$.
Equivalents used by the carbonate $= 0.0250 - 0.00500 = 0.0200$.
Mass of CaCO₃ $= 0.0200 \times 50 = 1.00$ g.
Percentage $= \dfrac{1.00}{1.20} \times 100 = 83.3$ %.
Check the arithmetic the other way: 0.0200 eq of CaCO₃ is 0.0100 mol, and
0.0100 × 100 = 1.00 g. Both routes agree because $E = M/2 = 50$.
:::

### Choosing the indicator

The indicator must change colour within the steep part of the titration curve, so that the
end point falls as close as possible to the equivalence point.

| Titration | pH at equivalence | Indicator |
|---|---|---|
| strong acid + strong base | 7 | phenolphthalein (8.3–10.0) or methyl orange (3.1–4.4) |
| weak acid + strong base | above 7 (about 8.7) | **phenolphthalein** only |
| strong acid + weak base | below 7 (about 5.1) | **methyl orange** only |
| weak acid + weak base | near 7, no sharp jump | none is satisfactory |
| KMnO₄ against a reductant | — | **self-indicating** (purple to colourless) |
| iodine against thiosulphate | — | starch (blue-black to colourless) |

```figure caption="Titration curves for 25.0 mL of 0.10 M acid against 0.10 M NaOH. The shaded bands are the transition ranges of methyl orange and phenolphthalein; an indicator is suitable only if its band lies on the steep part of the curve."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9,3.0))
V = np.linspace(0, 50, 1200)
Va, Ca, Cb = 25.0, 0.10, 0.10
def strong(V):
    tot = (Va+V)/1000.0
    cH = (Va*Ca/1000 - V*Cb/1000)/tot
    out = []
    for c in cH:
        if c > 1e-7:
            out.append(-np.log10(c))
        else:
            out.append(14 + np.log10(max(-c, 1e-14)))
    return np.array(out)
def weak(V):
    Ka = 1.8e-5
    out = []
    for v in V:
        nHA0 = Va*Ca/1000
        nOH = v*Cb/1000
        tot = (Va+v)/1000.0
        if nOH <= 1e-12:
            c = nHA0/tot
            h = (-Ka + np.sqrt(Ka**2 + 4*Ka*c))/2
            out.append(-np.log10(h))
        elif nOH < nHA0:
            nA = nOH; nHA = nHA0-nOH
            h = Ka*nHA/nA
            out.append(-np.log10(h))
        else:
            excess = (nOH-nHA0)/tot
            Kb = 1e-14/Ka
            oh = (-Kb + np.sqrt(Kb**2 + 4*Kb*excess))/2
            out.append(14 + np.log10(oh))
    return np.array(out)
ax.axhspan(3.1, 4.4, color='#f6d5c8', alpha=0.55, zorder=0)
ax.axhspan(8.3, 10.0, color='#cfe3f5', alpha=0.6, zorder=0)
ax.plot(V, strong(V), color=ACCENT, lw=2.0, label='strong acid')
ax.plot(V, weak(V), color=SERIES[1], lw=2.0, label='weak acid')
ax.axvline(25, color=MUTED, lw=0.9, ls=':')
ax.text(2, 4.7, 'methyl orange', fontsize=8.2, color='#9c4a2f')
ax.text(2, 9.6, 'phenolphthalein', fontsize=8.2, color='#2c5f86')
ax.text(26.2, 1.4, '25 mL', fontsize=8.2, color=MUTED)
ax.set_xlabel('volume of 0.10 M NaOH added (mL)')
ax.set_ylabel('pH')
ax.set_xlim(0, 50); ax.set_ylim(0, 14)
ax.set_yticks([0, 2, 4, 6, 8, 10, 12, 14])
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=0.4)
ax.legend(loc='lower right', fontsize=8.4, frameon=False)
```

::: caution Practical points that come up as one-liners
- The burette is rinsed with the **titrant**, the pipette with the **solution it will
  deliver**; rinsing with water would dilute the solution.
- The conical flask is rinsed with water only — a few drops of water in the flask do not
  change the number of moles present.
- Air bubbles in the burette tip must be removed before the initial reading; a bubble that
  escapes during the titration makes the volume read too high.
- Read the burette at the **bottom of the meniscus**, with the eye level with the reading.
- The last drop is added dropwise, and the flask is swirled after each addition.
:::

```photogrid label="8.1" cols="2" ratio="1.2" caption="One drop changes the pH by six units. (a) A burette delivers titrant slowly until the indicator changes. (b) For 25.0 mL of 0.100 M HCl and 0.100 M NaOH the pH is 1.00 at the start, 3.70 at 24.9 mL, exactly 7.00 at 25.0 mL and 10.30 at 25.1 mL. A 0.2 mL range crosses 6.6 pH units, so methyl orange (3.1 to 4.4) and phenolphthalein (8.3 to 10) both change colour within one drop of the true end-point at 25.0 mL, and either indicator can be used for a strong acid and a strong base."
@ photo id="chem12/titration" cap="A burette in a clamp: the volume of titrant is read to 0.05 mL"
fit 1.2
focus 0.5 0.5
@ svg cap="Titration curve: 25.0 mL of 0.100 M HCl with 0.100 M NaOH"
Ca, Va, Cb = 0.100, 25.0, 0.100
def pH(Vb):
    n = Ca * Va - Cb * Vb; V = Va + Vb
    if abs(n) < 1e-9: return 7.0
    return -math.log10(n / V) if n > 0 else 14 + math.log10(-n / V)
p0, p1, p2 = pH(0), pH(24.9), pH(25.1)
assert abs(p0 - 1.0) < 1e-9 and abs(p1 - 3.70) < 0.01 and abs(p2 - 10.30) < 0.01 and pH(25.0) == 7.0
facts = dict(p0="%.2f" % p0, p1="%.2f" % p1, p2="%.2f" % p2, jump="%.1f" % (p2 - p1), veq="%.1f" % (Ca * Va / Cb))
f = Fig(300, 236)
f.text(150, 14, "pH against volume of NaOH added", size=10.5, color=NAVY, bold=True)
X = lambda v: 40 + v * 4.8; Y = lambda p: 160 - p * 9.2
f.box(X(0), Y(10), X(50) - X(0), Y(8.3) - Y(10), fill=SAND, stroke=SAND, r=0, sw=0)
f.line(X(0), Y(0), 285, Y(0), color=SLATE, sw=1.4); f.line(X(0), Y(0), X(0), 34, color=SOFT, sw=1.2)
pts = [(X(v), Y(pH(v))) for v in [i * 0.5 for i in range(0, 100)] + [24.9, 25.0, 25.1] if True]
pts.sort()
for (a, b), (c, d) in zip(pts, pts[1:]): f.line(a, b, c, d, color=NAVY, sw=2.6)
f.circle(X(25), Y(7), 4, fill=AMBER, stroke=AMBER)
f.text(X(25) + 8, Y(7) + 14, "end-point 25.0 mL, pH 7", size=10.5, color=AMBER, bold=True, anchor="start")
for v in (0, 25, 50): f.text(X(v), Y(0) + 13, "%d" % v, size=10.5, color=SLATE)
for p in (2, 7, 12): f.text(35, Y(p), "%d" % p, size=10.5, color=SLATE, anchor="end", vmid=True)
f.text(150, 190, "24.9 mL: pH %.2f; 25.1 mL: pH %.2f" % (p1, p2), size=10.5, color=NAVY, bold=True)
f.text(150, 208, "0.2 mL spans %.1f pH units" % (p2 - p1), size=10.5, color=NAVY, bold=True)
f.text(150, 226, "shaded band: phenolphthalein, pH 8.3 to 10", size=10.5, color=SLATE)
```

```photogrid label="8.2" cols="2" ratio="1.2" caption="Making a primary standard. (a) A volumetric flask is graduated to hold exactly 500 mL at 20 degrees C, so the concentration of the solution made in it is known from the mass dissolved. (b) The cell computes mass = M x V x C for 0.1000 M: sodium carbonate needs 5.30 g, oxalic acid dihydrate 6.30 g, potassium dichromate 14.71 g and borax 19.07 g. A primary standard is weighed directly, so it must be pure, stable and of high molar mass. With a balance good to 0.2 mg the weighing error is 0.0038 per cent for sodium carbonate and only 0.0010 per cent for borax, which is why a larger molar mass makes a better primary standard."
@ photo id="ceechem2/flask" cap="A 500 mL volumetric flask"
fit 1.2
focus 0.5 0.55
@ svg cap="Mass of primary standard for 500 mL of 0.1000 M"
V, C = 0.5, 0.1
data = [("Na2CO3", 105.99), ("H2C2O4.2H2O", 126.07), ("borax", 381.37), ("K2Cr2O7", 294.19)]
rows = [(n, M * V * C) for n, M in data]
assert round(rows[0][1], 2) == 5.30 and round(rows[1][1], 2) == 6.30 and round(rows[3][1], 2) == 14.71
err = [0.0002 / m * 100 for _, m in rows]
f = Fig(300, 236)
f.text(150, 12, "Grams for 500 mL of 0.1000 M", size=10.5, color=NAVY, bold=True)
hbars(f, rows, vmax=20, fmt="%.2f g", x0=86, y0=32, bw=130, gap=30)
f.text(150, 166, "relative error of a 0.2 mg balance:", size=10, color=SLATE, bold=True)
f.text(150, 186, "Na2CO3 %.4f%%, borax %.4f%%" % (err[0], err[2]), size=10.5, color=NAVY, bold=True)
f.text(150, 206, "a heavier molar mass means a bigger weighing", size=10, color=SLATE, bold=True)
f.text(150, 222, "and a smaller weighing error", size=10, color=SLATE, bold=True)
facts = dict(na=rows[0][1], ox=rows[1][1], bx=rows[2][1], cr=rows[3][1], e1=err[0], e2=err[2])
```

## Formula and fact sheet

| Quantity | Relation |
|---|---|
| Equivalent weight | $E = M/n$; equivalents $= \text{mass}/E$ |
| n-factor: acid | basicity (replaceable H⁺): HCl 1, H₂SO₄ 2, H₃PO₄ 3 |
| n-factor: base | acidity (OH⁻): NaOH 1, Ca(OH)₂ 2, Al(OH)₃ 3 |
| n-factor: salt | total charge on the cation: NaCl 1, Na₂CO₃ 2, Al₂(SO₄)₃ 6 |
| n-factor: redox | electrons gained or lost per formula unit |
| KMnO₄ | 5 (acid, Mn²⁺), 3 (neutral, MnO₂), 1 (alkaline, MnO₄²⁻) |
| K₂Cr₂O₇ | 6 in acid (2Cr³⁺); $E = 49$ |
| Molarity | $M = n/V(\text{L})$; $M = \dfrac{10 \times \%\text{w/w} \times d}{M_B}$ |
| Molality | $m = n/\text{kg solvent}$ |
| Normality | $N = M \times n\text{-factor}$ |
| Formality | formula masses per litre; used for ionic solids such as NaCl |
| ppm / ppb | mg kg⁻¹ / μg kg⁻¹ (≈ mg L⁻¹ for dilute aqueous) |
| Mole fraction | $x_i = n_i/\sum n$; $\sum x_i = 1$ |
| Dilution | $M_1V_1 = M_2V_2$; $N_1V_1 = N_2V_2$ |
| Law of equivalence | $N_1V_1 = N_2V_2$ at the equivalence point |
| Back titration | equivalents of sample $= N_1V_1 - N_2V_2$ |
| Strength | g L⁻¹ $= N \times E$ |

| Indicator | pH range | Colour change | Use |
|---|---|---|---|
| methyl orange | 3.1–4.4 | red to yellow | strong acid + weak base |
| methyl red | 4.4–6.2 | red to yellow | strong acid + weak base |
| bromothymol blue | 6.0–7.6 | yellow to blue | strong acid + strong base |
| phenolphthalein | 8.3–10.0 | colourless to pink | weak acid + strong base |
| starch | — | blue-black to colourless | iodometric titrations |
| KMnO₄ itself | — | purple to colourless | permanganate titrations |

Primary standards: oxalic acid, Na₂CO₃, KHP, borax, K₂Cr₂O₇, NaCl, pure Zn/Cu, Mohr's
salt. Secondary standards: NaOH, KOH, HCl, H₂SO₄, KMnO₄, Na₂S₂O₃, I₂.

## Chapter summary

- Volumetric analysis measures the volume of a standard solution needed to react completely with a measured volume of analyte; the end point is the indicator's approximation to the equivalence point.
- Equivalent weight $E = M/n$; the n-factor is the basicity of an acid, the acidity of a base, the cation charge of a salt, or the electron change of an oxidant or reductant.
- KMnO₄ has three equivalent weights because it is reduced to Mn²⁺ (n = 5), MnO₂ (n = 3) or MnO₄²⁻ (n = 1); K₂Cr₂O₇ is always n = 6.
- Molarity is per litre of solution and changes with temperature; molality is per kilogram of solvent and does not. Normality = molarity × n-factor.
- $M = 10 \times \%\text{w/w} \times d / M_B$ is the only conversion that needs the density; ppm and ppb are mass ratios, and mole fractions sum to 1.
- Dilution conserves moles: $M_1V_1 = M_2V_2$.
- A primary standard is pure, stable, non-hygroscopic, soluble, fast-reacting and of high molar mass; NaOH, HCl, KMnO₄, Na₂S₂O₃ and I₂ are secondary standards and must be standardised.
- At the equivalence point $N_1V_1 = N_2V_2$, and equivalents can be counted as $NV$, mass/$E$, or n-factor × moles.
- In a back titration the equivalents used by the sample are the excess added minus the excess titrated back.
- Choose the indicator whose transition range lies on the steep part of the curve: phenolphthalein for weak acid + strong base, methyl orange for strong acid + weak base.

## Practice questions

**Set A — Recall (23 questions)**

1. The equivalent weight of an acid is its molar mass divided by
   (a) its basicity (b) its acidity (c) the number of oxygen atoms (d) the number of moles
2. The equivalent weight of H₂SO₄ (M = 98) is
   (a) 98 (b) 24.5 (c) 49 (d) 32.7
3. The n-factor of K₂Cr₂O₇ in acidic medium is
   (a) 3 (b) 6 (c) 2 (d) 7
4. The equivalent weight of KMnO₄ in acidic medium (M = 158) is
   (a) 158 (b) 52.7 (c) 79 (d) 31.6
5. The equivalent weight of anhydrous Na₂CO₃ (M = 106) is
   (a) 106 (b) 53 (c) 35.3 (d) 26.5
6. Molarity is the number of moles of solute per
   (a) litre of solution (b) kilogram of solvent (c) litre of solvent (d) kilogram of solution
7. Molality is expressed in
   (a) mol L⁻¹ (b) mol kg⁻¹ (c) eq L⁻¹ (d) g L⁻¹
8. Normality is equal to molarity multiplied by
   (a) molar mass (b) density (c) the n-factor (d) volume in litres
9. One part per million is the same as
   (a) 1 g per kg (b) 1 mg per g (c) 1 μg per kg (d) 1 mg per kg
10. The sum of the mole fractions of all the components of a solution is
   (a) 1 (b) 100 (c) 0 (d) equal to the molarity
11. Formality is normally used for
   (a) weak acids (b) gases (c) ionic solids that do not exist as molecules (d) non-electrolytes
12. Which substance is a primary standard?
   (a) NaOH (b) oxalic acid (c) HCl (d) KMnO₄
13. Which substance is NOT a primary standard?
   (a) NaOH (b) Na₂CO₃ (c) potassium hydrogen phthalate (d) borax
14. The law of equivalence is written as
   (a) $M_1V_1 = M_2V_2$ (b) $N_1V_2 = N_2V_1$ (c) $N_1 = N_2$ (d) $N_1V_1 = N_2V_2$
15. The indicator used for a strong acid–weak base titration is
   (a) phenolphthalein (b) methyl orange (c) starch (d) litmus
16. The indicator used for a weak acid–strong base titration is
   (a) methyl orange (b) starch (c) phenolphthalein (d) methyl red
17. The number of equivalents of a solute is equal to
   (a) $N \times V$ in litres (b) $M \times V$ in litres (c) mass × $E$ (d) $N/V$
18. The equivalent weight of oxalic acid dihydrate (M = 126) is
   (a) 126 (b) 45 (c) 90 (d) 63
19. The point at which the indicator changes colour in a titration is called the
   (a) equivalence point (b) end point (c) neutral point (d) stoichiometric point
20. Potassium permanganate needs no external indicator because it is
   (a) colourless (b) yellow (c) purple and turns colourless (d) white
21. A primary standard should have
   (a) a high molar mass (b) low solubility (c) a low molar mass (d) high volatility
22. The burette should be rinsed with
   (a) distilled water (b) the analyte solution (c) the indicator (d) the titrant
23. 1 M H₂SO₄ is the same as
   (a) 0.5 N (b) 2 N (c) 1 N (d) 4 N

::: note Answers and explanations — Set A
**1.** (a) — An acid's n-factor is its basicity, the number of replaceable H⁺ per molecule. For a base it would be the acidity, the number of OH⁻.
**2.** (c) — Sulphuric acid is dibasic, so $E = 98/2 = 49$. Option (a) forgets the n-factor and (d) is the value for H₃PO₄.
**3.** (b) — Two chromium atoms go from +6 to +3, so 2 × 3 = 6 electrons are gained per formula unit. Option (a) counts only one chromium atom.
**4.** (d) — Mn goes from +7 to +2, so $n = 5$ and $E = 158/5 = 31.6$. Option (b) is the value in neutral medium (n = 3).
**5.** (b) — The carbonate ion takes two protons, so $n = 2$ and $E = 106/2 = 53$. Option (a) uses n = 1, which is right only for NaHCO₃.
**6.** (a) — Molarity is moles per litre of **solution**, not of solvent. The volume includes the solute.
**7.** (b) — Molality is moles of solute per kilogram of **solvent**, so its unit is mol kg⁻¹ and it does not change with temperature.
**8.** (c) — $N = M \times n$-factor. The n-factor is 1 for HCl, 2 for H₂SO₄ and 5 for KMnO₄ in acid.
**9.** (d) — ppm is 1 mg per kg (or per litre of dilute aqueous solution). Option (c) is one part per billion.
**10.** (a) — Mole fractions are fractions of the total number of moles, so they must add up to exactly 1.
**11.** (c) — Formality counts formula masses per litre and is used for ionic solids such as NaCl, which contain no discrete molecules.
**12.** (b) — Oxalic acid is pure, stable and non-hygroscopic. NaOH absorbs CO₂ and water, HCl is volatile and KMnO₄ decomposes.
**13.** (a) — NaOH is hygroscopic and absorbs CO₂ from the air, so its concentration drifts. The other three are standard primary standards.
**14.** (d) — At the equivalence point the equivalents of the two reactants are equal: $N_1V_1 = N_2V_2$. Option (a) is true only for a 1 : 1 reaction in molar terms.
**15.** (b) — The salt of a weak base is acidic at equivalence (pH about 5), so the indicator must change in the acid region: methyl orange.
**16.** (c) — The salt of a weak acid is basic at equivalence (pH about 8.7), so phenolphthalein, which changes at 8.3–10.0, is the right choice.
**17.** (a) — Equivalents $= N \times V$ in litres. Option (b) gives moles, not equivalents.
**18.** (d) — Oxalate loses two electrons, so $n = 2$ and $E = 126/2 = 63$. Option (b) is the anhydrous value, 90/2.
**19.** (b) — The end point is what you observe; the equivalence point is the true stoichiometric point. The small difference between them is the titration error.
**20.** (c) — The purple permanganate ion is reduced to almost colourless Mn²⁺, so the first permanent pink tint marks the end point.
**21.** (a) — A high molar mass makes the weighing error a smaller fraction of the mass taken. Low solubility and volatility would both be disqualifying.
**22.** (d) — Rinsing with the titrant removes water that would otherwise dilute it. Rinsing with water would make the delivered concentration lower than stated.
**23.** (b) — Sulphuric acid has two replaceable protons, so $N = 2M = 2$ N. Option (c) is the value for a monobasic acid.
:::

**Set B — Understanding (14 questions)**

1. KMnO₄ has different equivalent weights in acidic, neutral and alkaline media because
   (a) its n-factor depends on the electrons gained (b) its molar mass changes (c) the temperature changes (d) it decomposes
2. NaOH cannot be used as a primary standard because it
   (a) is insoluble in water (b) has a low molar mass (c) is a strong base (d) absorbs water and CO₂ from the air
3. Molality is preferred to molarity in colligative-property work because molality
   (a) is easier to measure (b) does not change with temperature (c) uses a smaller mass of solute (d) is always numerically smaller
4. 0.1 M H₂SO₄ is 0.2 N because
   (a) its molar mass is 98 (b) it is a strong acid (c) it has two replaceable H⁺ per molecule (d) it contains two oxygen atoms
5. When a solution is diluted with water, the number of moles of solute
   (a) stays the same (b) increases (c) decreases (d) doubles
6. Phenolphthalein is unsuitable for a strong acid–weak base titration because the pH at equivalence is
   (a) above 10 (b) exactly 7 (c) below 3 (d) below its colour-change range
7. A primary standard should have a high molar mass so that
   (a) it dissolves faster (b) it reacts faster (c) a weighing error is a small fraction of the mass (d) it is cheaper
8. A back titration is used when
   (a) the reaction is very fast (b) the analyte is insoluble or the reaction is slow (c) no indicator is available (d) the titrant is a primary standard
9. The difference between the end point and the equivalence point is called the
   (a) titration error (b) indicator constant (c) percentage purity (d) buffer error
10. No external indicator is needed in a permanganate titration because
   (a) the analyte is already coloured (b) the end point is a precipitate (c) KMnO₄ is its own indicator (d) the pH changes sharply
11. Which solution has the greater normality: 0.1 M H₂SO₄ or 0.1 M HCl?
   (a) HCl (b) both are equal (c) it depends on the volume (d) H₂SO₄, which has two replaceable protons
12. A concentration of 1 ppm in water means
   (a) 1 g per litre (b) 1 mg per kg (c) 1 μg per kg (d) 1 mol per litre
13. The pipette should be rinsed with
   (a) distilled water (b) the titrant (c) the solution it will deliver (d) the indicator
14. A few drops of distilled water left in the conical flask before the titration
   (a) do not change the number of moles of analyte (b) increase its concentration (c) change the end point (d) invalidate the titration

::: note Answers and explanations — Set B
**1.** (a) — The manganese is reduced to Mn²⁺ (5 e⁻), MnO₂ (3 e⁻) or MnO₄²⁻ (1 e⁻), so $E = 158/5$, $158/3$ or $158/1$. The molar mass never changes.
**2.** (d) — Pellets of NaOH take up water and CO₂, forming carbonate, so the mass weighed no longer corresponds to the stated amount of NaOH.
**3.** (b) — Molality uses a mass of solvent, which does not expand or contract with temperature; a molarity would change as the solution's volume changed.
**4.** (c) — Normality counts replaceable H⁺, and H₂SO₄ has two. The strength of the acid is irrelevant to the n-factor.
**5.** (a) — Dilution adds solvent only, so the moles of solute are conserved. That is exactly why $M_1V_1 = M_2V_2$.
**6.** (d) — The equivalence pH of about 5 lies below phenolphthalein's range of 8.3–10.0, so the indicator would change far too late.
**7.** (c) — A 1 mg error on a 2 g mass is 0.05 %; the same error on a 0.05 g mass is 2 %. A high molar mass makes the relative error small.
**8.** (b) — When the analyte dissolves slowly, reacts slowly, or gives no sharp end point, an excess of reagent is added and the remainder is titrated back.
**9.** (a) — This difference is the titration error. A good indicator keeps it small by changing on the steep part of the curve.
**10.** (c) — The purple colour of MnO₄⁻ disappears as it is reduced, so the first permanent pink colour is the end point.
**11.** (d) — $N = M \times n$-factor: 0.1 M H₂SO₄ is 0.2 N while 0.1 M HCl is 0.1 N. Normality does not depend on the volume taken.
**12.** (b) — One part per million is 1 mg kg⁻¹ (≈ 1 mg L⁻¹ for dilute aqueous solutions). Option (c) is 1 ppb.
**13.** (c) — The pipette must deliver exactly the solution it holds; rinsing with water would dilute it and rinsing with titrant would add extra reagent.
**14.** (a) — The water adds volume but no analyte, and the titration measures moles, not concentration in the flask. The end point is unchanged.
:::

**Set C — Application (9 questions)**

1. The molarity of 98 % w/w H₂SO₄ of density 1.84 g mL⁻¹ is
   (a) 9.2 M (b) 1.84 M (c) 18.4 M (d) 36.8 M
2. The normality of 0.05 M K₂Cr₂O₇ in acidic medium is
   (a) 0.30 N (b) 0.05 N (c) 0.10 N (d) 0.60 N
3. 25 mL of 2.0 M HCl is diluted to 500 mL. The new molarity is
   (a) 0.50 M (b) 0.05 M (c) 1.0 M (d) 0.10 M
4. The volume of 0.200 M HCl needed to neutralise 25.0 mL of 0.100 M Na₂CO₃ completely is
   (a) 12.5 mL (b) 25.0 mL (c) 50.0 mL (d) 5.0 mL
5. The mass of Na₂CO₃ needed to prepare 250 mL of 0.100 N solution is (Na = 23)
   (a) 1.325 g (b) 2.650 g (c) 0.662 g (d) 5.300 g
6. 1.20 g of impure CaCO₃ is dissolved in 50.0 mL of 0.500 N HCl; the excess acid needs 20.0 mL of 0.250 N NaOH. The percentage of CaCO₃ (E = 50) is
   (a) 20.0 % (b) 96.0 % (c) 66.7 % (d) 83.3 %
7. The molality of a 10 % w/w glucose solution (M = 180) is
   (a) 0.556 m (b) 1.00 m (c) 0.617 m (d) 0.100 m
8. 0.020 g of Ca²⁺ dissolved in 1.00 kg of water gives a concentration of
   (a) 2 ppm (b) 20 ppm (c) 200 ppm (d) 0.02 ppm
9. 0.200 g of impure NaOH needs 48.0 mL of 0.100 M HCl for neutralisation. The percentage purity of the NaOH is (Na = 23, O = 16, H = 1)
   (a) 48 % (b) 80 % (c) 96 % (d) 100 %

::: note Answers and explanations — Set C
**1.** (c) — $M = \dfrac{10 \times 98 \times 1.84}{98} = 18.4$ M. Option (d) is the normality, since H₂SO₄ has two replaceable protons.
**2.** (a) — $N = M \times 6 = 0.05 \times 6 = 0.30$ N. Option (c) wrongly uses n = 2, the n-factor of oxalic acid.
**3.** (d) — $M_2 = M_1V_1/V_2 = 2.0 \times 25/500 = 0.10$ M. Option (a) divides by 100 instead of 500.
**4.** (b) — $N(\text{Na}_2\text{CO}_3) = 0.200$ N and $N(\text{HCl}) = 0.200$ N, so $N_1V_1 = N_2V_2$ gives 25.0 mL. By moles: 0.00250 mol carbonate needs 0.00500 mol acid.
**5.** (a) — Equivalents $= 0.250 \times 0.100 = 0.0250$; mass $= 0.0250 \times 53 = 1.325$ g. Option (b) uses $E = 106$, i.e. n = 1.
**6.** (d) — Acid taken 0.0250 eq, acid left 0.00500 eq, so 0.0200 eq reacted with the carbonate; mass $= 0.0200 \times 50 = 1.00$ g, and $1.00/1.20 = 83.3$ %.
**7.** (c) — 10 g glucose is 0.0556 mol and the solvent is 90 g = 0.090 kg, so $m = 0.0556/0.090 = 0.617$. Option (a) divides by the 100 g of solution.
**8.** (b) — 0.020 g = 20 mg in 1.00 kg, so 20 ppm. Option (a) forgets to convert grams to milligrams.
**9.** (c) — Moles of HCl $= 0.0480 \times 0.100 = 0.00480$; mass of NaOH $= 0.00480 \times 40 = 0.192$ g; purity $= 0.192/0.200 = 96$ %.
:::
