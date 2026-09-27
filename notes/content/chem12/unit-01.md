---
subject: Chemistry
grade: 12
unit: 1
title: Volumetric Analysis
hours: 8
area: General and Physical Chemistry
---

Quantitative analysis answers one question: **how much** of something is present.
This unit teaches the volume-measuring route to that answer. You take a solution
of accurately known concentration, run it into a measured volume of the unknown
until the reaction is exactly complete, read the burette, and turn that reading
into a mass or a percentage. Everything after this — the arithmetic of equivalents,
the concentration units, the choice of indicator — exists only to make that one
reading trustworthy.

::: key What the examiner asks from this unit
Two marks-rich things appear almost every year: an **equivalent-weight / n-factor**
question (very often KMnO₄ in different media), and a **titration numerical**
solved with $N_1V_1 = N_2V_2$. Learn to write the n-factor of any species in five
seconds and the numericals become one-line problems.
:::

## 1.1 Introduction to gravimetric analysis, volumetric analysis and equivalent weight

Analytical chemistry splits into two halves. **Qualitative analysis** asks *what*
is present; **quantitative analysis** asks *how much*. Classical quantitative
analysis then splits again, according to what you actually measure on the bench.

::: definition Gravimetric and volumetric analysis
**Gravimetric analysis** is the quantitative estimation of a substance by
measuring the **mass** of a pure, stable compound of known composition into which
the substance has been converted.

**Volumetric analysis** (also called **titrimetric analysis**) is the quantitative
estimation of a substance by measuring the **volume** of a solution of known
concentration that reacts exactly with it.
:::

In a gravimetric estimation of sulphate, for example, the sulphate is precipitated
as barium sulphate, and the precipitate is filtered, washed, ignited and weighed:

BaCl₂ + Na₂SO₄ → BaSO₄↓ + 2NaCl

From the mass of BaSO₄ (molar mass 233) the mass of SO₄²⁻ (96) follows by simple
proportion. Chloride is estimated the same way as AgCl, and iron as Fe₂O₃.

| Feature | Gravimetric analysis | Volumetric analysis |
|---|---|---|
| Quantity measured | Mass of a precipitate | Volume of a standard solution |
| Chief apparatus | Analytical balance, crucible, furnace | Burette, pipette, volumetric flask |
| Speed | Slow (hours to days) | Fast (minutes) |
| Accuracy | Very high (to 0.01 mg) | High (to about 0.1 %) |
| Indicator needed | No | Usually yes |
| Suits | Small numbers of very accurate results | Routine repeated analysis |

Volumetric work needs a common currency in which "exactly enough" can be
expressed. That currency is the **equivalent**.

::: definition Equivalent weight
The **equivalent weight** (E) of a substance is the number of parts by mass of it
that combine with or displace 1.008 parts by mass of hydrogen, 8 parts of oxygen,
or 35.5 parts of chlorine.

Expressed as a mass in grams it is called one **gram equivalent**. In modern
language,

$$ E = \frac{\text{molar mass}}{n\text{-factor}} $$

where the n-factor is the number of "reacting units" the species supplies per
formula unit.
:::

Equivalent weight is a pure number (a relative mass), so it has no unit; the gram
equivalent has the unit g.

```figure caption="The three pieces of glassware volumetric analysis stands on. Only the burette and the pipette are calibrated to deliver; the volumetric flask is calibrated to contain."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, Ellipse
fig, ax = plt.subplots(figsize=(5.1,3.9))

# ---------------- burette with conical flask beneath ----------------
xb = 0.60
ax.add_patch(Rectangle((xb-0.20, 3.05), 0.40, 5.45, fill=False, ec=INK, lw=1.3))
ax.add_patch(Rectangle((xb-0.20, 3.05), 0.40, 3.55, fc=ACCENT, alpha=0.18, ec='none'))
for i, y in enumerate(np.arange(3.25, 8.45, 0.26)):
    L = 0.11 if i % 4 else 0.20
    ax.plot([xb+0.20-L, xb+0.20], [y, y], color=MUTED, lw=0.7)
ax.plot([xb-0.20, xb+0.20], [6.60, 6.60], color=SERIES[1], lw=1.5)
ax.add_patch(Circle((xb, 2.86), 0.17, fc='white', ec=INK, lw=1.2, zorder=4))
ax.plot([xb-0.32, xb+0.32], [2.86, 2.86], color=INK, lw=1.5, zorder=5)
ax.add_patch(Polygon([[xb-0.08,2.68],[xb+0.08,2.68],[xb+0.025,2.05],[xb-0.025,2.05]],
                     closed=True, fill=False, ec=INK, lw=1.1))
for yd in (1.90, 1.72):
    ax.add_patch(Circle((xb, yd), 0.045, fc=ACCENT, ec='none', alpha=0.8))
ax.add_patch(Polygon([[xb-0.17,1.55],[xb+0.17,1.55],[xb+0.17,1.24],
                      [xb+0.95,0.16],[xb-0.95,0.16],[xb-0.17,1.24]],
                     closed=True, fill=False, ec=INK, lw=1.3))
ax.add_patch(Polygon([[xb+0.60,0.71],[xb+0.95,0.16],[xb-0.95,0.16],[xb-0.60,0.71]],
                     closed=True, fc=SERIES[4], alpha=0.18, ec='none'))
ax.text(xb, -0.50, 'burette and\nconical flask', ha='center', va='top',
        fontsize=8.6, color=INK)
ax.annotate('50 cm³ burette,\n0.1 cm³ divisions', xy=(xb-0.22, 8.30),
            xytext=(-5.05, 8.30), ha='left', va='center', fontsize=7.9, color=INK,
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.9, mutation_scale=9))
ax.annotate('bottom of the\nmeniscus is read', xy=(xb-0.22, 6.60),
            xytext=(-5.05, 6.10), ha='left', va='center', fontsize=7.9,
            color=SERIES[1],
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=0.9, mutation_scale=9))
ax.annotate('stopcock', xy=(xb-0.34, 2.86),
            xytext=(-2.10, 2.40), ha='left', va='center', fontsize=7.9, color=INK,
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.9, mutation_scale=9))

# ---------------- pipette ----------------
xp = 4.25
ax.add_patch(Rectangle((xp-0.075, 4.55), 0.15, 3.95, fill=False, ec=INK, lw=1.2))
ax.add_patch(Ellipse((xp, 3.45), 0.80, 2.3, fc=SERIES[2], alpha=0.20, ec=INK, lw=1.3))
ax.add_patch(Polygon([[xp-0.075,2.35],[xp+0.075,2.35],[xp+0.03,0.90],[xp-0.03,0.90]],
                     closed=True, fill=False, ec=INK, lw=1.2))
ax.plot([xp-0.16, xp+0.16], [7.30, 7.30], color=SERIES[1], lw=1.5)
ax.annotate('one graduation\nmark only', xy=(xp+0.18, 7.30), xytext=(xp+0.42, 8.15),
            ha='left', va='center', fontsize=7.9, color=SERIES[1],
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=0.9, mutation_scale=9))
ax.text(xp, -0.50, '25 cm³\npipette', ha='center', va='top', fontsize=8.6, color=INK)

# ---------------- volumetric (measuring) flask ----------------
xv = 8.60
ax.add_patch(Circle((xv, 2.55), 1.30, fc=ACCENT, alpha=0.15, ec=INK, lw=1.3))
for s in (-1, 1):
    ax.plot([xv + s*0.115, xv + s*0.115], [3.72, 8.00], color=INK, lw=1.2, zorder=3)
ax.plot([xv-0.115, xv+0.115], [8.00, 8.00], color=INK, lw=1.2, zorder=3)
ax.add_patch(Rectangle((xv-0.115, 3.72), 0.23, 2.83, fc=ACCENT, alpha=0.15,
                       ec='none', zorder=2))
ax.plot([xv-0.22, xv+0.22], [6.55, 6.55], color=SERIES[1], lw=1.5, zorder=5)
ax.annotate('calibration mark:\nholds one volume only', xy=(xv+0.24, 6.55),
            xytext=(xv+0.55, 7.75), ha='left', va='center', fontsize=7.9,
            color=SERIES[1],
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=0.9, mutation_scale=9))
ax.text(xv, -0.50, '250 cm³\nvolumetric flask', ha='center', va='top',
        fontsize=8.6, color=INK)

ax.set_xlim(-5.3, 15.2); ax.set_ylim(-1.9, 9.2)
ax.set_aspect('equal'); ax.axis('off')
```

## 1.2 Relationship between equivalent weight, atomic weight and valency

One atom of hydrogen has valency 1 and a relative atomic mass of 1.008, so by
definition one equivalent of hydrogen is 1.008. Now take an element X of atomic
weight A and valency v. One atom of X combines with v atoms of hydrogen, so A
parts of X combine with $1.008v$ parts of hydrogen. Therefore the mass of X that
combines with 1.008 parts of hydrogen is $A/v$:

$$ \text{equivalent weight} = \frac{\text{atomic weight}}{\text{valency}} $$

Rearranged, this gives the two forms the board also asks for:

$$ \text{atomic weight} = \text{equivalent weight} \times \text{valency},
\qquad \text{valency} = \frac{\text{atomic weight}}{\text{equivalent weight}} $$

| Element | Atomic weight | Valency | Equivalent weight |
|---|---|---|---|
| H | 1.008 | 1 | 1.008 |
| O | 16 | 2 | 8 |
| Cl | 35.5 | 1 | 35.5 |
| Mg | 24 | 2 | 12 |
| Al | 27 | 3 | 9 |
| Ca | 40 | 2 | 20 |
| Fe (ferrous) | 56 | 2 | 28 |
| Fe (ferric) | 56 | 3 | 18.67 |

::: caution Equivalent weight is not a fixed property
Iron has **two** equivalent weights because it shows two valencies, and KMnO₄ has
**three** because it is reduced to a different product in acidic, neutral and
strongly alkaline media. Always ask "in *which* reaction?" before quoting an
equivalent weight. Atomic weight and molar mass are fixed; equivalent weight is
not.
:::

## 1.3 Equivalent weight of compounds: acid, base, salt, oxidizing and reducing agents

For a compound, replace "valency" by the **n-factor** — the number of reacting
units the formula unit supplies. What counts as a unit depends on the class of
compound.

| Class | n-factor is | $E$ = |
|---|---|---|
| Acid | basicity = number of replaceable H⁺ | molar mass / basicity |
| Base | acidity = number of replaceable OH⁻ | molar mass / acidity |
| Salt | total positive (or negative) charge per formula unit | molar mass / total charge |
| Oxidising agent | number of electrons **gained** per formula unit | molar mass / electrons gained |
| Reducing agent | number of electrons **lost** per formula unit | molar mass / electrons lost |

Worked values you should know by heart:

| Substance | Molar mass | n-factor | Equivalent weight |
|---|---|---|---|
| HCl | 36.5 | 1 | 36.5 |
| H₂SO₄ | 98 | 2 | 49 |
| H₃PO₄ (full neutralisation) | 98 | 3 | 32.67 |
| NaOH | 40 | 1 | 40 |
| Ca(OH)₂ | 74 | 2 | 37 |
| Na₂CO₃ | 106 | 2 | 53 |
| CaCO₃ | 100 | 2 | 50 |
| Al₂(SO₄)₃ | 342 | 6 | 57 |
| K₂Cr₂O₇ (acid medium) | 294 | 6 | 49 |
| H₂C₂O₄·2H₂O (as reductant) | 126 | 2 | 63 |
| FeSO₄·7H₂O (as reductant) | 278 | 1 | 278 |
| Mohr's salt FeSO₄·(NH₄)₂SO₄·6H₂O | 392 | 1 | 392 |
| Na₂S₂O₃·5H₂O (with I₂) | 248 | 1 | 248 |
| I₂ (as oxidant) | 254 | 2 | 127 |

### The three equivalent weights of potassium permanganate

KMnO₄ (molar mass 158) is reduced to a different manganese species in each medium,
so it gains a different number of electrons:

| Medium | Half reaction | Electrons gained | $E$ |
|---|---|---|---|
| Acidic (dil. H₂SO₄) | MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O | 5 | 158/5 = 31.6 |
| Neutral or faintly alkaline | MnO₄⁻ + 2H₂O + 3e⁻ → MnO₂ + 4OH⁻ | 3 | 158/3 = 52.67 |
| Strongly alkaline | MnO₄⁻ + e⁻ → MnO₄²⁻ | 1 | 158/1 = 158 |

Each half reaction is balanced in both mass and charge — check the acidic one:
charge on the left is $(-1) + 8(+1) + 5(-1) = +2$, and on the right $+2$.

::: example Worked example 1.1 — equivalent weights
**Problem.** Calculate the equivalent weight of (a) H₃PO₄ when it reacts with NaOH
to give Na₂HPO₄, (b) K₂Cr₂O₇ acting as an oxidising agent in acidic medium, and
(c) Na₂CO₃ in its reaction with dilute HCl.

**Solution.**

(a) 2NaOH + H₃PO₄ → Na₂HPO₄ + 2H₂O. Only **two** of the three hydrogens are
replaced, so the effective basicity is 2, not 3.

$$ E = \frac{98}{2} = 49 $$

(b) The reduction half reaction is Cr₂O₇²⁻ + 14H⁺ + 6e⁻ → 2Cr³⁺ + 7H₂O. Charge
check: left $(-2) + 14 - 6 = +6$; right $2 \times (+3) = +6$. Six electrons are
gained, so the n-factor is 6:

$$ E = \frac{294}{6} = 49 $$

(c) Na₂CO₃ + 2HCl → 2NaCl + H₂O + CO₂. One formula unit neutralises two H⁺, so
the n-factor is 2 (this also equals the total positive charge, $2 \times 1$, on the
two sodium ions):

$$ E = \frac{106}{2} = 53 $$
:::

## 1.4 Concentration units: percentage, g/L, molarity, molality, normality, formality, ppm and ppb

Concentration is the amount of solute in a stated amount of solvent or solution.
Which unit you choose depends on what you can measure.

| Unit | Symbol | Definition | Usual unit |
|---|---|---|---|
| Percentage by mass | % w/w | mass of solute per 100 g of **solution** | — |
| Percentage by mass/volume | % w/v | mass (g) of solute per 100 cm³ of solution | — |
| Percentage by volume | % v/v | volume of solute per 100 cm³ of solution | — |
| Strength | S | mass (g) of solute per litre of solution | g L⁻¹ |
| Molarity | M | moles of solute per litre of solution | mol L⁻¹ |
| Molality | m | moles of solute per kilogram of **solvent** | mol kg⁻¹ |
| Normality | N | gram equivalents of solute per litre of solution | eq L⁻¹ |
| Formality | F | formula masses of solute per litre of solution | mol L⁻¹ |
| Parts per million | ppm | parts of solute per 10⁶ parts of solution | — |
| Parts per billion | ppb | parts of solute per 10⁹ parts of solution | — |

The working formulas:

$$ M = \frac{w \times 1000}{M_w \times V_{\text{(cm}^3)}}, \qquad
N = \frac{w \times 1000}{E \times V_{\text{(cm}^3)}}, \qquad
S = N \times E = M \times M_w $$

$$ N = M \times n\text{-factor}, \qquad
\text{ppm} = \frac{\text{mass of solute}}{\text{mass of solution}} \times 10^{6} $$

If a concentrated reagent bottle gives the percentage by mass $p$ and the density
$d$ (in g cm⁻³), then one litre of it weighs $1000d$ g and contains $10pd$ g of
solute, so

$$ M = \frac{10\,p\,d}{M_w}, \qquad m = \frac{1000\,M}{1000\,d - M\,M_w} $$

::: tip Which units change with temperature?
Molarity, normality, formality and any "per volume" unit **change with
temperature**, because the volume of the solution expands on heating. Molality,
percentage by mass and mole fraction involve only masses, so they are
**temperature independent**. This is a favourite one-mark question.
:::

**Formality** is used for ionic solids, which contain no discrete molecules. A
solution made by dissolving 58.5 g of NaCl in water and making it up to one litre
is 1 F, because "one mole of NaCl molecules" does not exist in the solution — only
Na⁺ and Cl⁻ ions.

**ppm and ppb** are for very dilute solutions, and for dilute aqueous solutions
(density ≈ 1 g cm⁻³) 1 ppm is the same as 1 mg L⁻¹ and 1 ppb the same as 1 μg L⁻¹.
The national standard for arsenic in drinking water in Nepal is 50 ppb, i.e.
0.05 mg of arsenic per litre — a limit set because many Terai tube-wells exceed the
10 ppb WHO guideline.

::: example Worked example 1.2 — preparing a standard solution
**Problem.** What mass of anhydrous sodium carbonate is required to prepare
250 cm³ of 0.1 N Na₂CO₃ solution?

**Solution.** Equivalent weight of Na₂CO₃ = 106/2 = 53.

Gram equivalents required = $N \times V_{\text{(L)}} = 0.1 \times 0.250 = 0.025$ eq.

$$ w = \text{eq} \times E = 0.025 \times 53 = 1.325\ \text{g} $$

So 1.325 g is weighed accurately, dissolved in distilled water, and the solution
is made up to the 250 cm³ mark of a volumetric flask.
:::

::: example Worked example 1.3 — from a reagent-bottle label
**Problem.** A bottle of concentrated sulphuric acid is labelled "98 % by mass,
density 1.84 g cm⁻³". Calculate its molarity, normality and molality.

**Solution.** Molar mass of H₂SO₄ = 98 g mol⁻¹, $E = 49$.

$$ M = \frac{10\,p\,d}{M_w} = \frac{10 \times 98 \times 1.84}{98} = 18.4\ \text{mol L}^{-1} $$

$$ N = M \times n = 18.4 \times 2 = 36.8\ \text{eq L}^{-1} $$

For molality, take 100 g of the acid: it contains 98 g (= 1 mol) of H₂SO₄ and only
2 g (= 0.002 kg) of water.

$$ m = \frac{1.0\ \text{mol}}{0.002\ \text{kg}} = 500\ \text{mol kg}^{-1} $$

The huge molality is not a mistake — concentrated sulphuric acid is nearly pure
solute, so there is very little solvent to divide by.
:::

## 1.5 Primary and secondary standard substances

A titration is only as good as the solution whose concentration you claim to know.

::: definition Primary and secondary standards
A **primary standard** is a substance of such high purity and stability that a
standard solution can be prepared simply by weighing it accurately and dissolving
it in a known volume of solvent.

A **secondary standard** is a substance whose solution cannot be standardised by
direct weighing; its concentration must be found by titrating it against a primary
standard.
:::

A primary standard must satisfy all of the following:

1. Available in a state of high purity (99.9 % or better).
2. Stable in air — it must not absorb moisture (hygroscopic), lose water of
   crystallisation (efflorescent), or absorb CO₂.
3. Highly soluble in water, and the solution must be stable on storing.
4. A **high equivalent weight**, so that the weighing error is a small fraction of
   the mass taken.
5. It must react rapidly, completely and in one definite way (stoichiometrically).

| Primary standards | Secondary standards |
|---|---|
| Oxalic acid, H₂C₂O₄·2H₂O | Hydrochloric acid, HCl |
| Anhydrous sodium carbonate, Na₂CO₃ | Sodium hydroxide, NaOH |
| Potassium dichromate, K₂Cr₂O₇ | Potassium permanganate, KMnO₄ |
| Potassium hydrogen phthalate | Sodium thiosulphate, Na₂S₂O₃·5H₂O |
| Silver nitrate, AgNO₃; sodium chloride, NaCl | Iodine solution |

Why the right-hand column fails: NaOH is deliquescent and absorbs CO₂ from the
air, so the pellets you weigh are part Na₂CO₃ and part water. Concentrated HCl
gives off fumes, so its concentration drifts. KMnO₄ is always slightly
contaminated with MnO₂ and is slowly reduced by traces of organic matter in the
water, so it is standardised freshly against oxalic acid.

## 1.6 Law of equivalence and normality equation

::: key Law of equivalence
In any chemical reaction, substances react in the ratio of their **equivalents**.
One gram equivalent of an acid exactly neutralises one gram equivalent of a base;
one gram equivalent of an oxidising agent exactly oxidises one gram equivalent of
a reducing agent — whatever the mole ratio in the balanced equation.
:::

::: derivation The normality equation
Let a volume $V_1$ (cm³) of a solution of normality $N_1$ exactly react with a
volume $V_2$ of normality $N_2$. Since normality is gram equivalents per litre,
the number of **milliequivalents** in a volume $V$ cm³ of normality $N$ is

$$ \text{meq} = N \times V_{\text{(cm}^3)} $$

By the law of equivalence the two must be equal at the end point, so

$$ N_1V_1 = N_2V_2 $$

Writing $N = M \times n$ for each solution gives the equivalent **molarity
equation**

$$ n_1M_1V_1 = n_2M_2V_2 $$

and putting $N_1 = N_2$ for the same solute before and after adding water gives
the **dilution formula** $M_1V_1 = M_2V_2$.
:::

::: caution $N_1V_1 = N_2V_2$ works only in normalities
The equation $N_1V_1 = N_2V_2$ needs **no** balanced equation and **no**
stoichiometric coefficients — that is its whole advantage. But if you substitute
molarities into it you will be wrong whenever the n-factors differ. For molarity
you must use $n_1M_1V_1 = n_2M_2V_2$. Mixing the two is the single commonest error
in this unit.
:::

::: example Worked example 1.4 — dilution
**Problem.** Commercial hydrochloric acid is 11.6 N. What volume of it is needed
to prepare 500 cm³ of 0.1 N HCl?

**Solution.** The number of equivalents does not change on dilution, so

$$ N_1V_1 = N_2V_2 \;\Rightarrow\; 11.6 \times V_1 = 0.1 \times 500 $$

$$ V_1 = \frac{50}{11.6} = 4.31\ \text{cm}^3 $$

Measure 4.31 cm³ of the concentrated acid, add it **to** about 200 cm³ of water
(never water to acid), then make up to 500 cm³.
:::

## 1.7 Titration and its types: acid-base titration, redox titration

::: definition Titration
**Titration** is the process of determining the concentration of a solution by
adding to a measured volume of it, from a burette, just enough of a standard
solution for the reaction to be exactly complete.
:::

The vocabulary is examined on its own:

| Term | Meaning |
|---|---|
| Titrant | the standard solution in the burette |
| Titrate / analyte | the solution of unknown concentration in the flask |
| Aliquot | the measured portion of analyte delivered by the pipette |
| Equivalence point | the point at which chemically equivalent amounts have reacted |
| End point | the point at which the indicator changes colour — the *observed* equivalence point |
| Titration error | the (small) difference between end point and equivalence point |
| Concordant readings | two or more burette readings agreeing within 0.1 cm³ |

A titration is repeated until two concordant readings are obtained, and the mean
of the concordant readings is used in the calculation. The first, rough titration
is discarded.

```figure caption="Reading a burette. The eye must be level with the bottom of the meniscus; a high or low eye introduces a parallax error of a few tenths of a cm³."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Ellipse, Circle
fig, ax = plt.subplots(figsize=(5.0,2.9))

# zoomed burette stem: 20.0 at y=3.6, 21.0 at y=1.6  (0.1 cm³ = 0.2 units)
ax.add_patch(Rectangle((0.0, 0.15), 1.30, 4.05, fill=False, ec=INK, lw=1.4))
ymen = 2.60
xm = np.linspace(0.02, 1.28, 80)
men = ymen + 0.17*((xm - 0.65)/0.63)**2
ax.fill_between(xm, 0.17, men, color=ACCENT, alpha=0.17)
ax.plot(xm, men, color=SERIES[0], lw=1.8)
for i in range(11):
    y = 3.6 - i*0.2
    if i % 5 == 0:
        ax.plot([0.0, 0.55], [y, y], color=INK, lw=1.0)
        ax.text(-0.13, y, f'{20.0 + i*0.1:.1f}', ha='right', va='center',
                fontsize=8.2, color=INK)
    else:
        ax.plot([0.0, 0.30], [y, y], color=MUTED, lw=0.8)

# sight line and reading
ax.plot([1.32, 2.70], [ymen, ymen], color=SERIES[1], lw=1.1, ls='--')
ax.text(1.40, ymen + 0.52, 'reading =\n20.5 cm³', fontsize=8.3, color=SERIES[1],
        va='center')

# three eye positions
eyes = [(3.95, 'eye too high  → reads low', MUTED, (0,(3,2))),
        (2.60, 'eye level  → correct', SERIES[2], '-'),
        (1.25, 'eye too low  → reads high', MUTED, (0,(3,2)))]
for y, lab, col, ls in eyes:
    ax.add_patch(Ellipse((4.55, y), 0.62, 0.30, fc='white', ec=col, lw=1.1, zorder=3))
    ax.add_patch(Circle((4.55, y), 0.085, fc=col, ec='none', zorder=4))
    ax.annotate('', xy=(2.80, ymen), xytext=(4.22, y),
                arrowprops=dict(arrowstyle='-|>', color=col, lw=1.2,
                                mutation_scale=10, linestyle=ls))
    ax.text(5.00, y, lab, va='center', fontsize=8.0, color=col)

ax.set_xlim(-1.0, 9.6); ax.set_ylim(-0.25, 4.55)
ax.axis('off')
```

### Types of titration

| Type | Reaction used | Typical example | Indicator |
|---|---|---|---|
| Acid-base (neutralisation) | H⁺ + OH⁻ → H₂O | NaOH vs HCl | phenolphthalein, methyl orange |
| Redox | electron transfer | KMnO₄ vs FeSO₄ | self-indicating |
| Precipitation | formation of an insoluble salt | AgNO₃ vs NaCl | potassium chromate (Mohr) |
| Complexometric | formation of a complex ion | EDTA vs Ca²⁺, Mg²⁺ | Eriochrome black T |
| Iodometric / iodimetric | I₂ ⇌ 2I⁻ | Na₂S₂O₃ vs liberated I₂ | starch (blue-black) |

### Acid-base titration

The four possible combinations behave differently near the equivalence point, and
this decides the indicator (developed fully in Unit 2):

| Acid vs base | pH at equivalence | Suitable indicator |
|---|---|---|
| Strong acid vs strong base | 7 | methyl orange **or** phenolphthalein |
| Weak acid vs strong base | > 7 | phenolphthalein |
| Strong acid vs weak base | < 7 | methyl orange |
| Weak acid vs weak base | ≈ 7, no sharp jump | none reliable — use a pH meter |

```figure caption="Titration of $25.0$ cm³ of $0.1$ M HCl with $0.1$ M NaOH. The pH leaps through more than six units on the addition of one drop, so both indicator ranges (shaded) lie inside the jump and either indicator may be used."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,3.1))
Kw = 1e-14; Va, Ca, Cb = 25.0, 0.1, 0.1
Vb = np.linspace(0, 50, 2000)
exc = (Ca*Va - Cb*Vb)/(Va + Vb)
h = (exc + np.sqrt(exc**2 + 4*Kw))/2
pH = -np.log10(h)
ax.axhspan(3.1, 4.4, color=SERIES[3], alpha=0.18, zorder=0)
ax.axhspan(8.3, 10.0, color=SERIES[4], alpha=0.18, zorder=0)
ax.text(1.2, 3.75, 'methyl orange  3.1 – 4.4', fontsize=7.6, color=INK, va='center')
ax.text(1.2, 9.15, 'phenolphthalein  8.3 – 10.0', fontsize=7.6, color=INK, va='center')
ax.plot(Vb, pH, color=ACCENT, lw=2.1, zorder=3)
ax.plot([25], [7], 'o', color=SERIES[1], ms=6.5, zorder=4)
ax.annotate('equivalence point\n25.0 cm³, pH = 7', (25, 7),
            textcoords='offset points', xytext=(14, -30), fontsize=8.0,
            color=SERIES[1],
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.0, mutation_scale=10))
ax.set_xlabel('volume of 0.1 M NaOH added  (cm³)')
ax.set_ylabel('pH of the flask')
ax.set_xlim(0, 50); ax.set_ylim(0, 14); ax.set_yticks(range(0, 15, 2))
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=0.45)
```

Sodium carbonate is a special case worth knowing, because it is neutralised in two
stages and therefore has **two** end points:

Na₂CO₃ + HCl → NaHCO₃ + NaCl  (first stage, pH ≈ 8.3, phenolphthalein)

NaHCO₃ + HCl → NaCl + H₂O + CO₂  (second stage, pH ≈ 4.0, methyl orange)

Phenolphthalein therefore measures **half** the carbonate and methyl orange
measures **all** of it. This is the basis of the double-indicator method used to
analyse mixtures of NaOH, Na₂CO₃ and NaHCO₃.

```figure caption="Titration of $25.0$ cm³ of $0.05$ M Na₂CO₃ with $0.1$ M HCl, computed from the acid dissociation constants of carbonic acid. Two end points appear, one inside each indicator range."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,3.1))
K1, K2, Kw = 4.45e-7, 4.69e-11, 1.0e-14
V0, C0, Ma = 25.0, 0.05, 0.10

def charge(h, va):
    tot = V0 + va
    Na = 2*C0*V0/tot; Cl = Ma*va/tot; CT = C0*V0/tot
    D = h*h + K1*h + K1*K2
    return Na + h - Cl - Kw/h - CT*(K1*h/D + 2*K1*K2/D)

Va = np.linspace(0.0, 40.0, 900)
pH = np.empty_like(Va)
for i, v in enumerate(Va):
    lo, hi = -14.0, 0.0
    for _ in range(90):
        mid = 0.5*(lo + hi)
        if charge(10.0**mid, v) < 0: lo = mid
        else: hi = mid
    pH[i] = -0.5*(lo + hi)

ax.axhspan(3.1, 4.4, color=SERIES[3], alpha=0.18, zorder=0)
ax.axhspan(8.3, 10.0, color=SERIES[4], alpha=0.18, zorder=0)
ax.text(27.0, 3.72, 'methyl orange', fontsize=7.6, color=INK, va='center')
ax.text(27.0, 9.18, 'phenolphthalein', fontsize=7.6, color=INK, va='center')
ax.plot(Va, pH, color=ACCENT, lw=2.1, zorder=3)
for v, lab in [(12.5, 'first end point\n12.5 cm³'), (25.0, 'second end point\n25.0 cm³')]:
    j = np.argmin(abs(Va - v))
    ax.plot([v], [pH[j]], 'o', color=SERIES[1], ms=6, zorder=4)
    ax.annotate(lab, (v, pH[j]), textcoords='offset points', xytext=(-56, -26),
                fontsize=7.8, color=SERIES[1],
                arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.0,
                                mutation_scale=9))
ax.set_xlabel('volume of 0.1 M HCl added  (cm³)')
ax.set_ylabel('pH of the flask')
ax.set_xlim(0, 40); ax.set_ylim(2, 12); ax.set_yticks(range(2, 13, 2))
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=0.45)
```

::: example Worked example 1.5 — acid-base titration
**Problem.** 25.0 cm³ of a sodium carbonate solution required 22.5 cm³ of
0.1 N hydrochloric acid for complete neutralisation using methyl orange.
Calculate the normality and the strength (in g L⁻¹) of the sodium carbonate
solution, and the mass of Na₂CO₃ in 250 cm³ of it.

**Solution.** Using the normality equation with acid = 1, base = 2:

$$ N_2 = \frac{N_1V_1}{V_2} = \frac{0.1 \times 22.5}{25.0} = 0.09\ \text{N} $$

Equivalent weight of Na₂CO₃ = 53, so

$$ S = N \times E = 0.09 \times 53 = 4.77\ \text{g L}^{-1} $$

In 250 cm³ (= 0.250 L) the mass is $4.77 \times 0.250 = 1.19\ \text{g}$.
:::

### Redox titration

Here the titrant oxidises or reduces the analyte, and the n-factor is the number
of electrons transferred. The two classic Nepali-syllabus systems are:

**Permanganometry.** KMnO₄ in dilute sulphuric acid titrated against oxalic acid
or a ferrous salt. KMnO₄ is **self-indicating**: the purple MnO₄⁻ is decolourised
as long as reductant remains, and the first permanent pale-pink tinge is the end
point.

2KMnO₄ + 5H₂C₂O₄ + 3H₂SO₄ → K₂SO₄ + 2MnSO₄ + 10CO₂ + 8H₂O

2KMnO₄ + 10FeSO₄ + 8H₂SO₄ → K₂SO₄ + 2MnSO₄ + 5Fe₂(SO₄)₃ + 8H₂O

**Dichrometry.** K₂Cr₂O₇ is a primary standard and its solution keeps
indefinitely, but it is not self-indicating; an external or internal redox
indicator (diphenylamine) is used.

K₂Cr₂O₇ + 6FeSO₄ + 7H₂SO₄ → K₂SO₄ + Cr₂(SO₄)₃ + 3Fe₂(SO₄)₃ + 7H₂O

::: caution Only dilute H₂SO₄ may be used to acidify a permanganate titration
Hydrochloric acid is itself oxidised by KMnO₄ (2MnO₄⁻ + 16H⁺ + 10Cl⁻ →
2Mn²⁺ + 5Cl₂ + 8H₂O), so extra permanganate is consumed and the result comes out
too high. Nitric acid is an oxidising agent and would oxidise the Fe²⁺ itself.
Oxalic acid titrations must also be warmed to 60–70 °C, because the reaction is
slow in the cold.
:::

::: example Worked example 1.6 — permanganate vs oxalic acid
**Problem.** 20.0 cm³ of 0.1 N KMnO₄ solution was required to oxidise 25.0 cm³ of
an oxalic acid solution in hot dilute H₂SO₄. Calculate the normality, molarity and
strength of the oxalic acid solution, given that the acid is the dihydrate
H₂C₂O₄·2H₂O.

**Solution.** By the law of equivalence,

$$ N_{\text{acid}} = \frac{N_{\text{KMnO}_4} V_{\text{KMnO}_4}}{V_{\text{acid}}}
= \frac{0.1 \times 20.0}{25.0} = 0.08\ \text{N} $$

Oxalic acid loses 2 electrons per molecule (C₂O₄²⁻ → 2CO₂ + 2e⁻), so its n-factor
is 2 and $E = 126/2 = 63$:

$$ M = \frac{N}{n} = \frac{0.08}{2} = 0.04\ \text{mol L}^{-1} $$

$$ S = N \times E = 0.08 \times 63 = 5.04\ \text{g L}^{-1} $$
:::

::: example Worked example 1.7 — standardising KMnO₄ against Mohr's salt
**Problem.** 3.92 g of pure Mohr's salt, FeSO₄·(NH₄)₂SO₄·6H₂O (molar mass 392),
was dissolved in dilute H₂SO₄ and the solution made up to 250 cm³. 25.0 cm³ of
this solution required 20.0 cm³ of KMnO₄ solution for oxidation. Find the
normality of the KMnO₄ solution and the mass of KMnO₄ in one litre of it.

**Solution.** Mohr's salt supplies one Fe²⁺ per formula unit and Fe²⁺ loses one
electron, so its n-factor is 1 and $E = 392$.

Equivalents of Mohr's salt taken $= 3.92/392 = 0.0100$ eq in 250 cm³.

$$ N(\text{Mohr's salt}) = \frac{0.0100}{0.250} = 0.04\ \text{N} $$

Milliequivalents in the 25.0 cm³ aliquot $= 0.04 \times 25.0 = 1.00$ meq.

$$ N(\text{KMnO}_4) = \frac{1.00}{20.0} = 0.05\ \text{N} $$

In acidic medium $E(\text{KMnO}_4) = 158/5 = 31.6$, so the mass per litre is

$$ S = N \times E = 0.05 \times 31.6 = 1.58\ \text{g L}^{-1} $$
:::

## Chapter summary

- Gravimetric analysis weighs a precipitate; volumetric analysis measures the
  volume of a standard solution. Volumetric work is faster, gravimetric more
  accurate.
- $E = \text{molar mass}/n\text{-factor}$, and for an element
  $E = \text{atomic weight}/\text{valency}$. The n-factor is basicity for an acid,
  acidity for a base, total ionic charge for a salt, and electrons transferred for
  a redox reagent.
- KMnO₄ has three equivalent weights: 31.6 (acidic, 5e⁻), 52.67 (neutral, 3e⁻) and
  158 (strongly alkaline, 1e⁻).
- Key concentration relations: $M = w \times 1000/(M_w V_{\text{cm}^3})$,
  $N = M \times n$, $S = N \times E$, $M = 10pd/M_w$,
  $m = 1000M/(1000d - MM_w)$. Molality and percentage by mass do not change with
  temperature; molarity and normality do.
- A primary standard (oxalic acid, Na₂CO₃, K₂Cr₂O₇) is pure, stable and of high
  equivalent weight, so it can be weighed directly; a secondary standard (HCl,
  NaOH, KMnO₄, Na₂S₂O₃) must be titrated against one.
- Law of equivalence $\Rightarrow$ $N_1V_1 = N_2V_2$ (milliequivalents when $V$ is
  in cm³), or $n_1M_1V_1 = n_2M_2V_2$ in molarities.
- In a permanganate titration, acidify with **dilute H₂SO₄ only**; KMnO₄ is
  self-indicating, while K₂Cr₂O₇ needs an indicator but is itself a primary
  standard.
- Na₂CO₃ titrated with HCl gives two end points: phenolphthalein at the
  bicarbonate stage (half the carbonate) and methyl orange at complete
  neutralisation.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The equivalent weight of KMnO₄ in acidic medium is <span class="marks">[1]</span>
   (a) 158 (b) 79 (c) 52.67 (d) 31.6
2. Which of the following is a primary standard substance? <span class="marks">[1]</span>
   (a) NaOH (b) HCl (c) K₂Cr₂O₇ (d) KMnO₄
3. The concentration unit that does **not** change with temperature is <span class="marks">[1]</span>
   (a) molarity (b) normality (c) molality (d) formality
4. A 0.1 M solution of H₂SO₄ is the same as <span class="marks">[1]</span>
   (a) 0.05 N (b) 0.1 N (c) 0.2 N (d) 0.4 N
5. In the titration of oxalic acid against KMnO₄ the indicator used is <span class="marks">[1]</span>
   (a) phenolphthalein (b) methyl orange (c) starch (d) none — KMnO₄ is self-indicating
6. 1 ppm of fluoride in drinking water is the same as <span class="marks">[1]</span>
   (a) 1 g L⁻¹ (b) 1 mg L⁻¹ (c) 1 μg L⁻¹ (d) 1 mol L⁻¹

::: note Answers to Group A
**1.** (d) — MnO₄⁻ gains 5 electrons, so $E = 158/5 = 31.6$.
**2.** (c) — K₂Cr₂O₇ is pure, non-hygroscopic, stable and of high equivalent weight.
**3.** (c) — molality uses the **mass** of solvent, and mass does not expand on heating.
**4.** (c) — $N = M \times n = 0.1 \times 2 = 0.2$ N.
**5.** (d) — the purple permanganate colour itself marks the end point.
**6.** (b) — for dilute aqueous solutions the density is 1 g cm⁻³, so 1 part in 10⁶ = 1 mg per 1000 g ≈ 1 mg L⁻¹.
:::

**Group B — Short answer (5 marks each)**

1. Define equivalent weight. Calculate the equivalent weight of KMnO₄ in acidic,
   neutral and strongly alkaline media, writing the half reaction in each
   case. <span class="marks">[5]</span>
2. What mass of oxalic acid dihydrate is needed to prepare 500 cm³ of a 0.1 N
   solution? <span class="marks">[5]</span>
3. 25.0 cm³ of 0.1 N NaOH was exactly neutralised by 20.0 cm³ of sulphuric acid.
   Calculate the normality, molarity and strength in g L⁻¹ of the acid. <span class="marks">[5]</span>
4. Distinguish between a primary and a secondary standard substance. Give two
   examples of each and state why sodium hydroxide cannot be a primary
   standard. <span class="marks">[5]</span>
5. Concentrated nitric acid is 70 % by mass and has a density of 1.42 g cm⁻³.
   Calculate its molarity, and the volume of it needed to prepare 1.00 L of
   0.5 M HNO₃. <span class="marks">[5]</span>
6. Why is only dilute sulphuric acid used to acidify a potassium permanganate
   titration, and why must an oxalic acid titration be carried out hot? <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Acidic: MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O, $E = 158/5 = 31.6$. Neutral or
faintly alkaline: MnO₄⁻ + 2H₂O + 3e⁻ → MnO₂ + 4OH⁻, $E = 158/3 = 52.67$. Strongly
alkaline: MnO₄⁻ + e⁻ → MnO₄²⁻, $E = 158/1 = 158$.

**2.** $E(\text{H}_2\text{C}_2\text{O}_4\cdot 2\text{H}_2\text{O}) = 126/2 = 63$.
Equivalents needed $= 0.1 \times 0.500 = 0.05$, so
$w = 0.05 \times 63 = 3.15\ \text{g}$.

**3.** $N_{\text{acid}} = (0.1 \times 25.0)/20.0 = 0.125\ \text{N}$;
$M = N/n = 0.125/2 = 0.0625\ \text{M}$;
$S = N \times E = 0.125 \times 49 = 6.125\ \text{g L}^{-1}$.

**4.** A primary standard is pure, stable, highly soluble and of high equivalent
weight, so a standard solution follows from one accurate weighing (oxalic acid,
K₂Cr₂O₇). A secondary standard must be titrated against a primary standard
(HCl, KMnO₄). NaOH is deliquescent and absorbs CO₂ from the air to form Na₂CO₃,
so the mass weighed is not pure NaOH.

**5.** $M = 10pd/M_w = (10 \times 70 \times 1.42)/63 = 994/63 = 15.78\ \text{M}$.
For the dilution, $M_1V_1 = M_2V_2$:
$V_1 = (0.5 \times 1000)/15.78 = 31.7\ \text{cm}^3$.

**6.** HCl would itself be oxidised by permanganate
(2MnO₄⁻ + 16H⁺ + 10Cl⁻ → 2Mn²⁺ + 5Cl₂ + 8H₂O), consuming extra KMnO₄ and giving a
high result; HNO₃ is an oxidising agent and would oxidise the reductant in the
flask. Only dilute H₂SO₄ merely supplies H⁺. The oxalate–permanganate reaction is
very slow at room temperature (it is autocatalysed by the Mn²⁺ it produces), so the
flask is warmed to 60–70 °C to get a sharp end point.
:::

**Group C — Long answer (8 marks each)**

1. (a) State the law of equivalence and use it to derive the normality equation
   $N_1V_1 = N_2V_2$. <span class="marks">[3]</span>
   (b) 1.06 g of anhydrous sodium carbonate was dissolved in water and the
   solution made up to 250 cm³. 25.0 cm³ of this solution required 20.0 cm³ of
   hydrochloric acid for complete neutralisation. Calculate the normality of the
   acid and its strength in g L⁻¹. <span class="marks">[5]</span>
2. (a) What is a redox titration? Write the balanced equation for the titration of
   ferrous sulphate with potassium permanganate in acidic medium and give the
   n-factor of each reagent. <span class="marks">[3]</span>
   (b) 2.00 g of an impure sample of Mohr's salt was dissolved in dilute H₂SO₄ and
   made up to 250 cm³. 25.0 cm³ of this solution required 10.0 cm³ of 0.05 N
   KMnO₄. Calculate the percentage purity of the sample. <span class="marks">[5]</span>

::: note Answers to Group C
**1.(b)** $E(\text{Na}_2\text{CO}_3) = 106/2 = 53$, so the equivalents taken are
$1.06/53 = 0.0200$ eq in 250 cm³, i.e. 20.0 meq.

The 25.0 cm³ aliquot contains $20.0 \times (25.0/250) = 2.00$ meq. Therefore

$$ N(\text{HCl}) = \frac{2.00}{20.0} = 0.100\ \text{N} $$

and $S = N \times E = 0.100 \times 36.5 = 3.65\ \text{g L}^{-1}$.

**2.(a)** A redox titration is one in which the titrant and analyte react by
transfer of electrons, the end point being fixed by a redox indicator or by the
titrant's own colour.

2KMnO₄ + 10FeSO₄ + 8H₂SO₄ → K₂SO₄ + 2MnSO₄ + 5Fe₂(SO₄)₃ + 8H₂O

n-factor of KMnO₄ = 5 (MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O); n-factor of FeSO₄ = 1
(Fe²⁺ → Fe³⁺ + e⁻).

**2.(b)** Milliequivalents of KMnO₄ used $= 0.05 \times 10.0 = 0.500$ meq, so the
25.0 cm³ aliquot contained 0.500 meq of Mohr's salt.

In the full 250 cm³, meq $= 0.500 \times 10 = 5.00$ meq $= 5.00\times10^{-3}$ eq.

Since $E = 392$ (n-factor 1), the mass of pure Mohr's salt is

$$ w = 5.00\times10^{-3} \times 392 = 1.96\ \text{g} $$

$$ \text{purity} = \frac{1.96}{2.00} \times 100 = 98.0\ \% $$
:::
