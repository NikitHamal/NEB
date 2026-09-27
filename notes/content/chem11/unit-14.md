---
subject: Chemistry
grade: 11
unit: 14
title: Hydrocarbons
hours: 8
area: Organic Chemistry
---

A **hydrocarbon** contains carbon and hydrogen only. Everything else in organic
chemistry is a hydrocarbon with something bolted onto it, which is why this unit
comes first among the families. Three families are studied: **alkanes**
(CₙH₂ₙ₊₂, all single bonds, saturated), **alkenes** (CₙH₂ₙ, one C=C) and
**alkynes** (CₙH₂ₙ₋₂, one C≡C). The plan is always the same — how each is made,
how each reacts, and how you tell them apart in a test tube.

::: key What the examiner asks from this unit
Every NEB paper takes preparations and properties straight from this list, so
learn each reaction as *reactant + reagent + condition → product*. The three
that appear almost every year are Markovnikov's rule with the peroxide effect,
Kolbe's electrolysis, and the pair of tests that separate ethene from ethyne.
Write the conditions above the arrow — a reaction without its catalyst and
temperature loses half its mark.
:::

```figure caption="Bonding in the first member of each family. As the bond order rises the carbon–carbon bond gets shorter and stronger, the s character of the hybrid orbitals rises, and the molecule flattens and then straightens."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 3, figsize=(5.2,2.6))

def frame(ax, title, sub):
    ax.set_title(title, fontsize=8.6, color=INK, pad=5)
    ax.text(0.0, -1.42, sub, fontsize=6.8, color=MUTED, ha='center',
            va='center', linespacing=1.45)
    ax.set_xlim(-1.55, 1.55); ax.set_ylim(-1.80, 1.30)
    ax.set_aspect('equal'); ax.axis('off')

def carbon(ax, x, y):
    ax.text(x, y, 'C', fontsize=11, color=INK, ha='center', va='center',
            zorder=3, bbox=dict(boxstyle='circle,pad=0.10', fc='white', ec='none'))

def hyd(ax, x0, y0, x1, y1):
    ax.plot([x0, x1], [y0, y1], color=INK, lw=1.4, zorder=1)
    ax.text(x1*1.12, y1*1.12 if abs(y1) > 0.01 else y1, 'H', fontsize=8.6,
            color=ACCENT, ha='center', va='center', zorder=2)

# ---- ethane ----
ax = axes[0]
carbon(ax, -0.42, 0); carbon(ax, 0.42, 0)
ax.plot([-0.26, 0.26], [0, 0], color=INK, lw=1.6)
for (cx, s) in ((-0.42, -1), (0.42, 1)):
    for ang in (55, -55):
        a = np.radians(ang)
        ax.plot([cx, cx + s*0.62*abs(np.cos(a))], [0, 0.62*np.sin(a)],
                color=INK, lw=1.4)
        ax.text(cx + s*0.78*abs(np.cos(a)), 0.78*np.sin(a), 'H', fontsize=8.6,
                color=ACCENT, ha='center', va='center')
    ax.plot([cx, cx + s*0.66], [0, 0], color=INK, lw=1.4)
    ax.text(cx + s*0.84, 0, 'H', fontsize=8.6, color=ACCENT, ha='center',
            va='center')
frame(ax, 'ethane  C₂H₆',
      'sp³, tetrahedral\nC—C 154 pm,  109.5°\n348 kJ mol⁻¹,  25 % s')

# ---- ethene ----
ax = axes[1]
carbon(ax, -0.42, 0); carbon(ax, 0.42, 0)
for dy in (0.075, -0.075):
    ax.plot([-0.26, 0.26], [dy, dy], color='#d9534f', lw=1.6)
for (cx, s) in ((-0.42, -1), (0.42, 1)):
    for ang in (60, -60):
        a = np.radians(ang)
        ax.plot([cx, cx + s*0.62*abs(np.cos(a))], [0, 0.62*np.sin(a)],
                color=INK, lw=1.4)
        ax.text(cx + s*0.80*abs(np.cos(a)), 0.80*np.sin(a), 'H', fontsize=8.6,
                color=ACCENT, ha='center', va='center')
frame(ax, 'ethene  C₂H₄',
      'sp², planar\nC=C 134 pm,  120°\n614 kJ mol⁻¹,  33 % s')

# ---- ethyne ----
ax = axes[2]
carbon(ax, -0.32, 0); carbon(ax, 0.32, 0)
for dy in (0.10, 0.0, -0.10):
    ax.plot([-0.17, 0.17], [dy, dy], color='#2e8b57', lw=1.5)
ax.plot([-0.48, -0.95], [0, 0], color=INK, lw=1.4)
ax.plot([0.48, 0.95], [0, 0], color=INK, lw=1.4)
ax.text(-1.14, 0, 'H', fontsize=8.6, color=ACCENT, ha='center', va='center')
ax.text(1.14, 0, 'H', fontsize=8.6, color=ACCENT, ha='center', va='center')
ax.annotate('', xy=(0.95, 0.42), xytext=(-0.95, 0.42),
            arrowprops=dict(arrowstyle='<->', color=MUTED, lw=0.9,
                            mutation_scale=8))
ax.text(0.0, 0.60, '180°  linear', fontsize=7.0, color=MUTED, ha='center')
frame(ax, 'ethyne  C₂H₂',
      'sp, linear\nC≡C 120 pm,  180°\n839 kJ mol⁻¹,  50 % s')
fig.tight_layout()
```

## 14.1 Alkanes: preparation from haloalkanes (reduction and Wurtz reaction), decarboxylation, catalytic hydrogenation of alkene and alkyne

Alkanes are also called **paraffins** (Latin *parum affinis*, "little affinity")
because they are so unreactive. Four laboratory preparations are on the syllabus.

### (a) Reduction of haloalkanes

Nascent hydrogen, generated in the flask by zinc and acid, replaces the halogen
by hydrogen. The alkane keeps the same number of carbons as the halide.

CH₃CH₂Cl + H₂ --Zn/HCl--> CH₃CH₃ + HCl

CH₃CH₂I + HI --red P, 423 K--> CH₃CH₃ + I₂

Zinc and ethanoic acid, zinc–copper couple in ethanol, or lithium aluminium
hydride LiAlH₄ in dry ether all do the same job. The order of ease is
R—I > R—Br > R—Cl, because the C—I bond is the weakest.

### (b) Wurtz reaction

Two molecules of haloalkane are coupled by metallic sodium in dry ether. The
alkane produced has **twice** the number of carbons of the halide.

2CH₃CH₂Br + 2Na --dry ether--> CH₃CH₂CH₂CH₃ + 2NaBr

::: caution Three limits of the Wurtz reaction
1. It cannot make **methane**, and it cannot make any alkane with an **odd**
   number of carbon atoms from a single halide.
2. With two *different* halides R—X and R′—X you get a mixture of three
   alkanes, R—R, R′—R′ and R—R′, which is hard to separate.
3. The ether must be **dry**: sodium reacts violently with water.
:::

### (c) Decarboxylation (soda-lime method)

The sodium salt of a carboxylic acid is heated with **soda lime** (NaOH + CaO,
in the ratio 3:1). Carbon dioxide leaves as carbonate, so the alkane has **one
carbon fewer** than the acid.

CH₃COONa + NaOH --CaO, Δ--> CH₄ + Na₂CO₃

CH₃CH₂COONa + NaOH --CaO, Δ--> CH₃CH₃ + Na₂CO₃

Calcium oxide is added to keep the very hygroscopic sodium hydroxide dry and to
stop it attacking the glass.

### (d) Catalytic hydrogenation (Sabatier–Senderens reduction)

An alkene or alkyne takes up hydrogen over a finely divided metal catalyst.

CH₂=CH₂ + H₂ --Ni, 523–573 K--> CH₃CH₃

CH≡CH + 2H₂ --Ni, 523–573 K--> CH₃CH₃

Nickel needs 250–300 °C; platinum or palladium work at room temperature. This is
the reaction used industrially to turn liquid vegetable oils into *vanaspati* ghee.

| Method | Reagent and condition | Carbon count | Note |
|---|---|---|---|
| Reduction of R—X | Zn/HCl, or Zn + CH₃COOH, or LiAlH₄ | unchanged | ease R—I > R—Br > R—Cl |
| Wurtz reaction | 2R—X + 2Na, dry ether | doubled | symmetrical alkanes only |
| Decarboxylation | RCOONa + NaOH/CaO, Δ | one fewer | good for CH₄ from CH₃COONa |
| Hydrogenation | H₂, Ni at 523–573 K (or Pt/Pd, 298 K) | unchanged | used for vanaspati ghee |
| Kolbe's electrolysis | conc. aq. RCOONa, electrolysis | doubled, minus 2 | Section 14.9 |

## 14.2 Alkanes chemical properties: substitution (halogenation, nitration, sulphonation); oxidation of ethane

Alkanes have only strong, non-polar σ bonds, so they are attacked neither by
electrophiles nor by nucleophiles. Their characteristic reaction is
**free-radical substitution**, which needs heat or ultraviolet light to get
started.

### Halogenation

CH₄ + Cl₂ --hν / 573 K--> CH₃Cl + HCl

CH₃Cl + Cl₂ --hν--> CH₂Cl₂ + HCl → CHCl₃ → CCl₄

The reaction does not stop at the first product: with excess chlorine all four
hydrogens are replaced in turn. Reactivity of the halogens falls sharply,
F₂ > Cl₂ > Br₂ > I₂. Fluorination is explosive and iodination is reversible
(HI reduces the product back), so iodination needs an oxidising agent such as
HIO₃ or HNO₃ to destroy the HI as it forms.

```figure caption="Free-radical chlorination of methane. Light splits Cl₂ homolytically; the two propagation steps then regenerate the chlorine atom, so one photon can convert thousands of methane molecules. The chain ends only when two radicals meet."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.1,3.3))
ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 6.6)

def band(y, h, label, col):
    ax.add_patch(plt.Rectangle((0.15, y-h/2), 9.7, h, facecolor='none',
                               edgecolor=col, lw=1.0, zorder=0))
    ax.text(0.45, y + h/2 - 0.30, label, fontsize=7.4, color=col,
            ha='left', va='center', fontweight='bold')

# ---- initiation ----
band(5.55, 1.65, 'Step 1  initiation', '#d9534f')
ax.text(1.45, 5.10, 'Cl', fontsize=11, color=INK, ha='center', va='center')
ax.text(2.35, 5.10, 'Cl', fontsize=11, color=INK, ha='center', va='center')
ax.plot([1.70, 2.10], [5.10, 5.10], color=INK, lw=1.5)
ax.plot([1.82, 1.98], [5.22, 5.22], marker='o', ms=3.0, ls='none',
        color='#d9534f')
ax.add_patch(FancyArrowPatch((1.86, 5.34), (1.50, 5.55),
                             connectionstyle='arc3,rad=0.42', arrowstyle='->',
                             mutation_scale=10, lw=1.2, color='#d9534f'))
ax.add_patch(FancyArrowPatch((1.94, 5.34), (2.30, 5.55),
                             connectionstyle='arc3,rad=-0.42', arrowstyle='->',
                             mutation_scale=10, lw=1.2, color='#d9534f'))
ax.annotate('', xy=(3.60, 5.10), xytext=(2.85, 5.10),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.1,
                            mutation_scale=10))
ax.text(3.22, 5.30, 'hν', fontsize=7.6, color=MUTED, ha='center')
ax.text(4.30, 5.10, '2 Cl•', fontsize=10.5, color='#d9534f', ha='center',
        va='center')
ax.text(7.55, 5.10, 'the fish-hook arrow moves ONE electron',
        fontsize=6.9, color=MUTED, ha='center', va='center')

# ---- propagation ----
band(3.35, 2.10, 'Step 2  propagation  (chain-carrying)', '#1d6fb8')
ax.text(5.0, 3.30, 'CH₄  +  Cl•   →   •CH₃  +  HCl', fontsize=10.2, color=INK,
        ha='center', va='center')
ax.text(5.0, 2.62, '•CH₃  +  Cl₂   →   CH₃Cl  +  Cl•', fontsize=10.2, color=INK,
        ha='center', va='center')
ax.text(5.0, 2.06, 'the Cl• made in the second step starts the first step again',
        fontsize=6.9, color='#1d6fb8', ha='center', va='center')

# ---- termination ----
band(1.10, 1.55, 'Step 3  termination', '#2e8b57')
ax.text(5.0, 0.92, 'Cl• + Cl• → Cl₂      •CH₃ + Cl• → CH₃Cl      '
        '•CH₃ + •CH₃ → C₂H₆', fontsize=8.8, color=INK, ha='center', va='center')
ax.text(5.0, 0.42, 'the trace of ethane found in the product proves the '
        'mechanism is radical', fontsize=6.9, color=MUTED, ha='center',
        va='center')
fig.tight_layout()
```

### Nitration

In the **vapour phase** at 673–773 K an alkane reacts with nitric acid vapour.
The reaction is also free-radical, and it gives a mixture, because C—C bonds
break as well.

CH₄ + HNO₃ --673–773 K--> CH₃NO₂ + H₂O

CH₃CH₃ + HNO₃ --673 K--> CH₃CH₂NO₂ + H₂O

### Sulphonation

An alkane heated with **oleum** (fuming sulphuric acid, H₂SO₄ + SO₃) gives a
sulphonic acid. Only alkanes from hexane upwards, and especially those with a
tertiary hydrogen, react at a useful rate:

CH₃(CH₂)₄CH₃ + HO—SO₃H --oleum, Δ--> CH₃(CH₂)₄CH₂—SO₃H + H₂O

Methane, ethane and propane do **not** sulphonate — a favourite one-mark point.

### Oxidation of ethane

| Condition | Equation | Product |
|---|---|---|
| Excess O₂, ignite | 2C₂H₆ + 7O₂ → 4CO₂ + 6H₂O | complete combustion, ΔH negative |
| O₂, Cu tube, 473 K, 100 atm | 2C₂H₆ + O₂ → 2CH₃CH₂OH | ethanol |
| O₂, Mo₂O₃ catalyst | C₂H₆ + O₂ → CH₃CHO + H₂O | ethanal |
| O₂, manganese(II) ethanoate, Δ | 2C₂H₆ + 3O₂ → 2CH₃COOH + 2H₂O | ethanoic acid |

Combustion is the reason alkanes matter economically: LPG (a mixture of propane
and butane) is the commonest cooking fuel in Nepali kitchens. The complete
combustion of butane is

2C₄H₁₀ + 13O₂ → 8CO₂ + 10H₂O

With a limited air supply the products are carbon monoxide and soot instead,
which is why a badly ventilated kitchen is dangerous.

## 14.3 Alkenes: preparation by dehydration of alcohol, dehydrohalogenation, catalytic hydrogenation of alkyne

Alkenes, or **olefins**, are made by **elimination** — pulling two groups off
adjacent carbons so that a π bond can form.

### (a) Dehydration of alcohols

An alcohol loses water over concentrated sulphuric acid at 443 K, or over
alumina at 623 K.

CH₃CH₂OH --conc. H₂SO₄, 443 K--> CH₂=CH₂ + H₂O

The ease of dehydration follows carbocation stability: **3° > 2° > 1°**. A
tertiary alcohol dehydrates with 20 % H₂SO₄ at 358 K, a primary one needs 95 %
acid at 443 K.

### (b) Dehydrohalogenation

A haloalkane loses HX when warmed with **alcoholic** potassium hydroxide.

CH₃CH₂Br + KOH (alcoholic) --Δ--> CH₂=CH₂ + KBr + H₂O

::: caution Alcoholic KOH, not aqueous
*Alcoholic* KOH gives **elimination** and an alkene; *aqueous* KOH gives
**substitution** and an alcohol. The same reagent, a different solvent, a
completely different product. Write the word "alcoholic" every time.
:::

When more than one alkene is possible, **Saytzeff's rule** decides:

::: definition Saytzeff's (Zaitsev's) rule
In a dehydrohalogenation or dehydration, the hydrogen is removed from the
carbon carrying the **fewest hydrogen atoms**, so the major product is the
**more substituted** — and therefore more stable — alkene.
:::

CH₃CH₂CHBrCH₃ + KOH (alc.) → CH₃CH=CHCH₃ (but-2-ene, 81 %) + CH₂=CHCH₂CH₃
(but-1-ene, 19 %)

The ease of elimination is again 3° > 2° > 1°, and R—I > R—Br > R—Cl.

### (c) Catalytic hydrogenation of an alkyne

Adding only one molecule of hydrogen stops at the alkene, provided the catalyst
is poisoned so that it cannot go further.

CH≡CH + H₂ --Lindlar's catalyst--> CH₂=CH₂

**Lindlar's catalyst** is palladium deposited on calcium carbonate and partly
deactivated with quinoline or lead ethanoate. Both hydrogens arrive on the same
face of the triple bond, so an internal alkyne gives the **cis** alkene. Sodium
in liquid ammonia at 195 K does the opposite and gives the **trans** alkene.

## 14.4 Alkenes chemical properties: addition with HX (Markovnikov's rule and peroxide effect), H₂O, O₃, H₂SO₄

The π bond of an alkene is a loose, exposed cloud of electrons above and below
the C=C axis. It is therefore a **nucleophile**, and the characteristic reaction
of an alkene is **electrophilic addition**.

### Addition of hydrogen halides

CH₂=CH₂ + HBr → CH₃CH₂Br

Reactivity falls in the order HI > HBr > HCl, which is the order of decreasing
acid strength — the easier the H—X bond gives up H⁺, the faster the addition.

With an **unsymmetrical** alkene there are two possible products, and only one
of them forms in quantity.

::: definition Markovnikov's rule
When an unsymmetrical reagent HX adds to an unsymmetrical alkene, the
**hydrogen attaches itself to the doubly bonded carbon that already carries the
greater number of hydrogen atoms**, and the halogen goes to the other carbon.
:::

CH₃CH=CH₂ + HBr → CH₃CHBrCH₃  (2-bromopropane, major)

```figure caption="Electrophilic addition of HBr to propene. The π electrons attack H, and the proton lands on C1 because that route gives the more stable secondary carbocation. Br⁻ then adds to the positive carbon, so the bromine ends up on C2 — which is exactly what Markovnikov's rule states."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
fig, axes = plt.subplots(1, 3, figsize=(5.2,2.5))
for a in axes:
    a.axis('off'); a.set_xlim(-0.55, 2.85); a.set_ylim(-1.35, 1.55)

def curly(ax, p0, p1, rad, col):
    ax.add_patch(FancyArrowPatch(p0, p1, connectionstyle=f'arc3,rad={rad}',
                                 arrowstyle='-|>', mutation_scale=11, lw=1.25,
                                 color=col, shrinkA=1, shrinkB=1))

# ---- (a) attack of the pi bond on H ----
ax = axes[0]
ax.text(0.05, 0.0, 'CH₃', fontsize=9.6, color=INK, ha='center', va='center')
ax.text(0.95, 0.0, 'CH', fontsize=9.6, color=INK, ha='center', va='center')
ax.text(1.92, 0.0, 'CH₂', fontsize=9.6, color=INK, ha='center', va='center')
ax.plot([0.34, 0.72], [0, 0], color=INK, lw=1.5)
for dy in (0.075, -0.075):
    ax.plot([1.20, 1.62], [dy, dy], color='#d9534f', lw=1.5)
ax.text(1.12, 1.05, 'H', fontsize=9.6, color=ACCENT, ha='center', va='center')
ax.text(1.62, 1.05, 'Br', fontsize=9.6, color=ACCENT, ha='center', va='center')
ax.plot([1.26, 1.46], [1.05, 1.05], color=INK, lw=1.4)
curly(ax, (1.41, 0.22), (1.14, 0.86), 0.40, '#d9534f')
curly(ax, (1.38, 1.18), (1.66, 1.26), -0.55, ACCENT)
ax.set_title('(a) π electrons attack H', fontsize=7.6, color=INK, pad=4)
ax.text(1.15, -1.05, 'propene  +  H—Br', fontsize=7.0, color=MUTED,
        ha='center', va='center')

# ---- (b) the carbocation ----
ax = axes[1]
ax.text(0.20, 0.0, 'CH₃', fontsize=9.6, color=INK, ha='center', va='center')
ax.text(1.12, 0.0, 'CH', fontsize=9.6, color=ACCENT, ha='center', va='center')
ax.text(1.44, 0.24, '+', fontsize=10, color=ACCENT, ha='center', va='center')
ax.text(2.20, 0.0, 'CH₃', fontsize=9.6, color=INK, ha='center', va='center')
ax.plot([0.50, 0.90], [0, 0], color=INK, lw=1.5)
ax.plot([1.38, 1.88], [0, 0], color=INK, lw=1.5)
ax.text(1.12, -1.00, 'Br⁻', fontsize=10.0, color='#2e8b57', ha='center',
        va='center')
curly(ax, (1.12, -0.80), (1.18, -0.22), -0.42, '#2e8b57')
ax.set_title('(b) 2° carbocation', fontsize=7.6, color=INK, pad=4)
ax.text(1.15, 1.20, 'secondary, not primary:\n(CH₃)₂CH⁺  >  CH₃CH₂CH₂⁺',
        fontsize=6.6, color=MUTED, ha='center', va='center', linespacing=1.4)

# ---- (c) product ----
ax = axes[2]
ax.text(1.15, 0.28, 'CH₃—CHBr—CH₃', fontsize=10.2, color=INK, ha='center',
        va='center')
ax.text(1.15, -0.42, '2-bromopropane', fontsize=8.0, color='#2e8b57',
        ha='center', va='center')
ax.text(1.15, -0.92, 'Markovnikov product', fontsize=7.0, color=MUTED,
        ha='center', va='center')
ax.set_title('(c) Br⁻ adds to C2', fontsize=7.6, color=INK, pad=4)
fig.tight_layout()
```

The rule is not a rule at all but a consequence of carbocation stability: the
proton adds so as to give the **more stable carbocation**, and a secondary
cation beats a primary one because two +I alkyl groups spread its charge
(Section 13.7).

### Peroxide effect (Kharasch effect)

In the presence of benzoyl peroxide or simply of air-formed peroxides, the
addition of **HBr** goes the other way round:

CH₃CH=CH₂ + HBr --(C₆H₅CO)₂O₂--> CH₃CH₂CH₂Br  (1-bromopropane)

The peroxide provides radicals, so the mechanism becomes free-radical instead of
ionic. Br• adds first, and it adds to the terminal carbon because that gives the
more stable **secondary free radical**. The result looks like anti-Markovnikov
addition.

::: caution The peroxide effect works only with HBr
With HCl the H—Cl bond is too strong for Cl• to be produced easily, and with HI
the H—I bond is so weak that the iodine atoms simply recombine. Only HBr sits in
the window where both chain steps are exothermic. So peroxides change the
product of HBr addition and of nothing else.
:::

```figure caption="The same alkene and the same reagent give opposite products according to whether peroxide is present. The ionic route builds the more stable carbocation; the radical route builds the more stable free radical, and the two put the bromine on opposite carbons."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,3.0))
ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 6.0)

def route(y, cond, inter, prod, name, col):
    ax.text(1.15, y, 'CH₃—CH=CH₂\n+  HBr', fontsize=8.8, color=INK,
            ha='center', va='center', linespacing=1.5)
    ax.annotate('', xy=(4.95, y), xytext=(2.55, y),
                arrowprops=dict(arrowstyle='-|>', color=col, lw=1.3,
                                mutation_scale=11))
    ax.text(3.75, y + 0.34, cond, fontsize=7.0, color=col,
            ha='center', va='bottom')
    ax.text(3.75, y - 0.36, inter, fontsize=6.7, color=MUTED,
            ha='center', va='top')
    ax.text(6.45, y, prod, fontsize=9.4, color=INK, ha='center', va='center')
    ax.text(8.25, y, name, fontsize=7.4, color=col, ha='left', va='center',
            linespacing=1.4)

route(4.35, 'no peroxide (ionic)',
      'via CH₃—CH⁺—CH₃\n2° carbocation', 'CH₃—CHBr—CH₃',
      '2-bromopropane\nMarkovnikov', ACCENT)
route(1.55, 'benzoyl peroxide',
      'via CH₃—•CH—CH₂Br\n2° free radical', 'CH₃—CH₂—CH₂Br',
      '1-bromopropane\nanti-Markovnikov', '#d9534f')
ax.plot([0.3, 9.7], [2.95, 2.95], color=GRID, lw=0.9)
fig.tight_layout()
```

### Addition of water (hydration)

Water adds across the double bond in the presence of an acid catalyst, and the
addition follows Markovnikov's rule.

CH₂=CH₂ + H₂O --H₃PO₄, 573 K, 60 atm--> CH₃CH₂OH

CH₃CH=CH₂ + H₂O --dil. H₂SO₄--> CH₃CH(OH)CH₃  (propan-2-ol)

### Addition of sulphuric acid

Cold concentrated sulphuric acid adds to give an **alkyl hydrogen sulphate**,
which on boiling with water hydrolyses to the alcohol. The two steps together
are the industrial *indirect hydration* of alkenes.

CH₂=CH₂ + H₂SO₄ (cold, conc.) → CH₃CH₂—OSO₃H  (ethyl hydrogen sulphate)

CH₃CH₂—OSO₃H + H₂O --Δ--> CH₃CH₂OH + H₂SO₄

With propene, Markovnikov's rule puts the —OSO₃H on C2, so the alcohol obtained
is propan-2-ol, not propan-1-ol.

### Ozonolysis

Ozone adds across the double bond to give an unstable **ozonide**, which is
then split by zinc dust and water. The zinc is essential — it destroys the
hydrogen peroxide that would otherwise oxidise the products further.

```figure caption="Ozonolysis of but-2-ene. The five-membered ozonide breaks exactly where the double bond was, so counting the carbonyl compounds tells you where the double bond used to be."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.1,2.5))
ax.axis('off'); ax.set_xlim(-0.4, 11.0); ax.set_ylim(-1.7, 1.9)

# ---- alkene ----
ax.text(0.00, 0.0, 'CH₃', fontsize=9.2, color=INK, ha='center', va='center')
ax.text(0.85, 0.0, 'CH', fontsize=9.2, color=INK, ha='center', va='center')
ax.text(1.70, 0.0, 'CH', fontsize=9.2, color=INK, ha='center', va='center')
ax.text(2.55, 0.0, 'CH₃', fontsize=9.2, color=INK, ha='center', va='center')
ax.plot([0.28, 0.62], [0, 0], color=INK, lw=1.4)
ax.plot([1.93, 2.27], [0, 0], color=INK, lw=1.4)
for dy in (0.075, -0.075):
    ax.plot([1.10, 1.45], [dy, dy], color='#d9534f', lw=1.5)
ax.text(1.28, -1.05, 'but-2-ene', fontsize=7.2, color=MUTED, ha='center')

ax.annotate('', xy=(4.15, 0.0), xytext=(3.05, 0.0),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.2,
                            mutation_scale=11))
ax.text(3.60, 0.30, 'O₃', fontsize=8.0, color='#1d6fb8', ha='center')
ax.text(3.60, -0.42, 'CCl₄,\n250 K', fontsize=6.4, color=MUTED, ha='center',
        linespacing=1.3)

# ---- ozonide ring ----
cx, cy, r = 5.55, 0.05, 0.62
labels = ['O', 'O', 'C', 'O', 'C']
cols = ['#1d6fb8', '#1d6fb8', INK, '#1d6fb8', INK]
angs = np.radians([90, 162, 234, 306, 18])
xs, ys = cx + r*np.cos(angs), cy + r*np.sin(angs)
for i in range(5):
    j = (i + 1) % 5
    ax.plot([xs[i], xs[j]], [ys[i], ys[j]], color=INK, lw=1.4, zorder=1)
for x, y, lab, c in zip(xs, ys, labels, cols):
    ax.text(x, y, lab, fontsize=8.8, color=c, ha='center', va='center',
            zorder=3, bbox=dict(boxstyle='circle,pad=0.10', fc='white',
                                ec='none'))
ax.plot([xs[2], xs[2]-0.30], [ys[2], ys[2]-0.52], color=INK, lw=1.3)
ax.text(xs[2]-0.52, ys[2]-0.72, 'CH₃', fontsize=7.6, color=INK, ha='center')
ax.plot([xs[4], xs[4]+0.30], [ys[4], ys[4]+0.52], color=INK, lw=1.3)
ax.text(xs[4]+0.55, ys[4]+0.70, 'CH₃', fontsize=7.6, color=INK, ha='center')
ax.text(cx, -1.35, 'ozonide (unstable)', fontsize=7.2, color=MUTED,
        ha='center')

ax.annotate('', xy=(8.20, 0.0), xytext=(7.05, 0.0),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.2,
                            mutation_scale=11))
ax.text(7.62, 0.30, 'Zn / H₂O', fontsize=7.6, color='#2e8b57', ha='center')

ax.text(9.55, 0.28, '2 CH₃CHO', fontsize=10.2, color=INK, ha='center',
        va='center')
ax.text(9.55, -0.36, 'ethanal', fontsize=7.4, color='#2e8b57', ha='center',
        va='center')
fig.tight_layout()
```

CH₃CH=CHCH₃ --(i) O₃  (ii) Zn/H₂O--> 2CH₃CHO

CH₂=CH₂ --(i) O₃  (ii) Zn/H₂O--> 2HCHO

CH₃CH=CH₂ --(i) O₃  (ii) Zn/H₂O--> CH₃CHO + HCHO

Because each doubly bonded carbon becomes a carbonyl carbon, ozonolysis is the
classical method for **locating a double bond**: identify the two carbonyl
compounds and join them back together at the oxygen atoms.

::: example Worked example 14.1 — predicting addition products
**Problem.** Give the major organic product of each reaction, with a reason.
(a) but-1-ene + HCl
(b) but-1-ene + HBr in the presence of benzoyl peroxide
(c) 2-methylpropene + H₂O with dilute H₂SO₄
(d) an alkene X, C₅H₁₀, gives only propanone and ethanal on ozonolysis. What is X?

**Solution.**

(a) Markovnikov: the H goes to C1, which already has two hydrogens, so the Cl
goes to C2. Product **2-chlorobutane**, CH₃CH₂CHClCH₃. The route through the
secondary cation CH₃CH₂CH⁺CH₃ is preferred to the primary one.

(b) Peroxide effect, and the reagent is HBr, so the addition is
anti-Markovnikov: Br• adds to C1 giving the secondary radical
CH₃CH₂•CHCH₂Br... more simply, the bromine ends on the terminal carbon.
Product **1-bromobutane**, CH₃CH₂CH₂CH₂Br.

(c) (CH₃)₂C=CH₂ + H₂O: the H adds to the CH₂ carbon, the OH to the carbon
carrying the two methyls, because that gives a tertiary carbocation. Product
**2-methylpropan-2-ol**, (CH₃)₃COH.

(d) Reverse the ozonolysis. Write the two carbonyl compounds facing each other
and replace the two oxygens by a double bond:

(CH₃)₂C=O + O=CHCH₃ → (CH₃)₂C=CHCH₃

X is **2-methylbut-2-ene**, C₅H₁₀ — the formula checks: 5 C and 10 H.
:::

## 14.5 Alkynes: preparation from carbon and hydrogen, 1,2-dibromoethane, chloroform/iodoform

### (a) From the elements

An electric arc is struck between two carbon electrodes in an atmosphere of
hydrogen. This is the only common organic compound made straight from its
elements.

2C + H₂ --electric arc, 3000 °C--> C₂H₂

The mixture must be chilled at once, because ethyne is thermodynamically
unstable with respect to its elements (ΔH°f is **positive**, +227 kJ mol⁻¹) and
would decompose again if left hot.

### (b) From 1,2-dibromoethane

Two molecules of HBr are eliminated by alcoholic potassium hydroxide.

CH₂Br—CH₂Br + 2KOH (alc.) --Δ--> CH≡CH + 2KBr + 2H₂O

The first elimination is easy; the second is difficult, because a vinyl halide
is unreactive, so sodamide NaNH₂ at 423 K is often used for the second step:

CH₂Br—CH₂Br + KOH (alc.) → CH₂=CHBr + KBr + H₂O

CH₂=CHBr + NaNH₂ --Δ--> CH≡CH + NaBr + NH₃

### (c) From chloroform or iodoform

Heating trihalomethane with silver powder removes all six halogen atoms:

2CHCl₃ + 6Ag --Δ--> CH≡CH + 6AgCl

2CHI₃ + 6Ag --Δ--> CH≡CH + 6AgI

### (d) From calcium carbide — the industrial and laboratory route

Most ethyne actually used, including the gas in a gas-welding cylinder, comes
from calcium carbide and water:

CaO + 3C --2300 K, electric furnace--> CaC₂ + CO

CaC₂ + 2H₂O → C₂H₂↑ + Ca(OH)₂

## 14.6 Alkynes chemical properties: addition with H₂, HX, H₂O; acidic nature (sodium, ammoniacal AgNO₃, ammoniacal Cu₂Cl₂)

An alkyne has two π bonds, so it adds **two** molecules of most reagents, one
after the other.

### Addition of hydrogen

CH≡CH + H₂ --Ni, 473 K--> CH₂=CH₂ --H₂, Ni--> CH₃CH₃

### Addition of hydrogen halides

Markovnikov's rule applies at each stage, so both halogens end up on the **same**
carbon:

CH≡CH + HBr → CH₂=CHBr (bromoethene) --HBr--> CH₃CHBr₂ (1,1-dibromoethane)

CH≡CH + HCl --Hg²⁺, 470 K--> CH₂=CHCl (vinyl chloride, the monomer of PVC)

### Addition of water

Water adds only in the presence of mercury(II) sulphate in dilute sulphuric
acid. The first product is an **enol**, which tautomerises at once to the
carbonyl compound (Section 13.4).

CH≡CH + H₂O --40 % H₂SO₄, 1 % HgSO₄, 333 K--> [CH₂=CHOH] → CH₃CHO

CH₃C≡CH + H₂O --HgSO₄/H₂SO₄--> CH₃COCH₃ (propanone, by Markovnikov addition)

::: key Ethyne is the only alkyne that gives an aldehyde
Hydration of ethyne gives ethanal; hydration of every other alkyne gives a
**ketone**, because Markovnikov's rule puts the OH on the more substituted
carbon.
:::

### Acidic nature of terminal alkynes

The hydrogen on a triply bonded carbon is weakly acidic. The reason is
hybridisation: an sp carbon has **50 % s character**, so its electrons are held
much closer to the nucleus and it behaves as a more electronegative atom, which
makes the C—H bond more polar and the resulting carbanion more stable.

Acidity: HC≡CH  >  CH₂=CH₂  >  CH₃—CH₃
(pKa ≈ 25, 44, 50; s character 50 %, 33 %, 25 %)

Three reactions demonstrate it, and all three need a **terminal** ≡C—H:

1. **With sodium metal** at 473 K, hydrogen is displaced:

   2CH≡CH + 2Na → 2CH≡C—Na (monosodium acetylide) + H₂↑

   CH≡C—Na + Na --473 K--> Na—C≡C—Na (disodium acetylide) + ½H₂

2. **With ammoniacal silver nitrate** (Tollens' reagent) — a **white** precipitate
   of silver acetylide:

   CH≡CH + 2[Ag(NH₃)₂]OH → Ag—C≡C—Ag↓ + 4NH₃ + 2H₂O

3. **With ammoniacal cuprous chloride** — a **red** precipitate of copper
   acetylide:

   CH≡CH + Cu₂Cl₂ + 2NH₄OH → Cu—C≡C—Cu↓ + 2NH₄Cl + 2H₂O

::: caution Acidic, but not an acid
Ethyne does **not** turn blue litmus red and does not react with NaOH or
Na₂CO₃ — it is a far weaker acid than water. "Acidic character" here means only
that it can lose a proton to a very strong base such as Na or NaNH₂. Also
remember that but-2-yne, CH₃C≡CCH₃, has no hydrogen on the triply bonded carbons
and gives **none** of these three reactions.
:::

## 14.7 Test of unsaturation (ethene and ethyne): bromine water test and Baeyer's test

Both tests work because the π bond is attacked and destroyed, taking the colour
of the reagent with it.

### Bromine water test

Bromine water is reddish-brown. An unsaturated hydrocarbon **decolourises** it
without any hydrogen bromide being given off:

CH₂=CH₂ + Br₂ → CH₂Br—CH₂Br (1,2-dibromoethane, colourless)

CH≡CH + 2Br₂ → CHBr₂—CHBr₂ (1,1,2,2-tetrabromoethane, colourless)

Note that ethyne needs **two** molecules of bromine and therefore decolourises
twice as much bromine water per mole.

### Baeyer's test

Baeyer's reagent is **cold dilute alkaline potassium permanganate**, which is
purple. An alkene turns it colourless and throws down a brown precipitate of
manganese dioxide:

CH₂=CH₂ + H₂O + [O] --cold dil. alk. KMnO₄--> CH₂OH—CH₂OH (ethane-1,2-diol)

CH≡CH + 4[O] --cold dil. alk. KMnO₄--> HOOC—COOH (oxalic acid)

```figure caption="Identifying an unknown gaseous hydrocarbon. The first test separates saturated from unsaturated; the second separates a terminal alkyne from an alkene, because only the terminal alkyne has an acidic hydrogen."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,3.6))
ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0.5, 9.2)

def box(x, y, w, h, txt, fc, ec, fs=7.1, tc=None):
    ax.add_patch(plt.Rectangle((x-w/2, y-h/2), w, h, facecolor=fc,
                               edgecolor=ec, lw=1.0, zorder=1))
    ax.text(x, y, txt, ha='center', va='center', fontsize=fs, color=tc or INK,
            zorder=2, linespacing=1.4)

def arrow(x0, y0, x1, y1, lab, col, side='right'):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='-|>', color=col, lw=1.1,
                                mutation_scale=10))
    ax.text((x0+x1)/2 + (0.28 if side == 'right' else -0.28), (y0+y1)/2,
            lab, fontsize=6.6, color=col,
            ha='left' if side == 'right' else 'right', va='center',
            linespacing=1.3)

box(5.0, 8.75, 6.6, 0.68, 'unknown gas:  CH₄,  C₂H₄  or  C₂H₂ ?',
    '#eef3f9', ACCENT, 7.6)
box(5.0, 7.30, 5.4, 0.70, 'shake with bromine water (reddish-brown)',
    'white', MUTED, 7.1)
ax.annotate('', xy=(5.0, 7.68), xytext=(5.0, 8.40),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.1,
                            mutation_scale=10))

arrow(4.20, 6.92, 2.20, 6.05, 'no change', '#b8860b', 'left')
ax.annotate('', xy=(7.80, 6.05), xytext=(5.80, 6.92),
            arrowprops=dict(arrowstyle='-|>', color='#2e8b57', lw=1.1,
                            mutation_scale=10))
ax.text(7.10, 6.62, 'decolourised\n(also Baeyer’s reagent)', fontsize=6.6,
        color='#2e8b57', ha='left', va='center', linespacing=1.3)

box(2.20, 5.70, 3.0, 0.70, 'saturated — alkane\nCH₄', '#fdf6ec', '#b8860b', 7.1)
box(7.80, 5.70, 3.2, 0.70, 'unsaturated\nC₂H₄ or C₂H₂', '#f4f8f4', '#2e8b57',
    7.1)
ax.annotate('', xy=(7.80, 4.62), xytext=(7.80, 5.35),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.1,
                            mutation_scale=10))
box(7.80, 4.25, 3.8, 0.74, 'pass into ammoniacal AgNO₃\n(or ammoniacal Cu₂Cl₂)',
    'white', MUTED, 7.0)

ax.annotate('', xy=(4.60, 2.95), xytext=(6.80, 3.88),
            arrowprops=dict(arrowstyle='-|>', color='#1d6fb8', lw=1.1,
                            mutation_scale=10))
ax.text(5.40, 3.42, 'no ppt', fontsize=6.6, color='#1d6fb8',
        ha='right', va='center')
ax.annotate('', xy=(9.10, 2.95), xytext=(8.70, 3.88),
            arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.1,
                            mutation_scale=10))
ax.text(8.45, 3.40, 'white ppt\n(red with Cu₂Cl₂)', fontsize=6.6,
        color='#d9534f', ha='right', va='center', linespacing=1.3)

box(3.60, 2.50, 3.2, 0.78, 'ETHENE  C₂H₄\nno acidic H', '#eef3f9', '#1d6fb8',
    7.4, '#1d6fb8')
box(8.00, 2.50, 3.2, 0.78, 'ETHYNE  C₂H₂\nAg₂C₂ or Cu₂C₂', '#faf2f2', '#d9534f',
    7.4, '#d9534f')
ax.text(5.0, 1.15, 'Baeyer’s reagent (cold dilute alkaline KMnO₄) is '
        'decolourised by both\nC₂H₄ and C₂H₂, so it proves unsaturation but '
        'cannot tell them apart.', fontsize=6.8, color=MUTED, ha='center',
        va='center', linespacing=1.45)
fig.tight_layout()
```

| Test | Reagent | Alkane | Alkene | Alkyne (terminal) |
|---|---|---|---|---|
| Bromine water | Br₂(aq), reddish-brown | no change | decolourised | decolourised (2 mol Br₂) |
| Baeyer's test | cold dil. alkaline KMnO₄, purple | no change | decolourised, brown MnO₂ | decolourised, brown MnO₂ |
| Ammoniacal AgNO₃ | [Ag(NH₃)₂]OH | no change | no change | **white** ppt Ag₂C₂ |
| Ammoniacal Cu₂Cl₂ | CuCl in NH₄OH | no change | no change | **red** ppt Cu₂C₂ |

## 14.8 Comparative physical properties of alkane, alkene and alkyne

| Property | Alkane | Alkene | Alkyne |
|---|---|---|---|
| General formula | CₙH₂ₙ₊₂ | CₙH₂ₙ | CₙH₂ₙ₋₂ |
| Hybridisation of C | sp³ | sp² | sp |
| Bond angle | 109.5° | 120° | 180° |
| C—C bond length | 154 pm | 134 pm | 120 pm |
| C—C bond enthalpy | 348 kJ mol⁻¹ | 614 kJ mol⁻¹ | 839 kJ mol⁻¹ |
| s character | 25 % | 33.3 % | 50 % |
| Physical state (C₁–C₄) | gas | gas | gas |
| Boiling point of the C₂ member | −88.6 °C | −103.7 °C | −84 °C (sublimes) |
| Density | less than water | less than water | less than water |
| Solubility | insoluble in water, soluble in benzene, ether, CCl₄ | same | slightly more soluble (weakly polar C—H) |
| Dipole moment | ≈ 0 | ≈ 0 (trans), small (cis) | ≈ 0 |
| Chemical character | inert; free-radical substitution | electrophilic addition | electrophilic addition + acidic H |
| Flame | blue, non-sooty | slightly luminous | bright, smoky (high C content) |

Within any one family the boiling point rises steadily with the number of
carbons, because the van der Waals attraction grows with molecular size, and
falls with branching, because a branched molecule is more nearly spherical and
its molecules touch over a smaller area.

::: example Worked example 14.2 — a combustion calculation
**Problem.** 2.8 g of ethene is burnt completely in oxygen. Calculate (a) the
volume of carbon dioxide produced at STP, and (b) the mass of oxygen consumed.
(C = 12, H = 1, O = 16; molar volume at STP = 22.4 dm³ mol⁻¹.)

**Solution.** The balanced equation is

C₂H₄ + 3O₂ → 2CO₂ + 2H₂O

Molar mass of ethene = 2(12) + 4(1) = 28 g mol⁻¹.

Moles of ethene = 2.8 / 28 = 0.10 mol.

(a) From the equation, 1 mol of C₂H₄ gives 2 mol of CO₂, so
moles of CO₂ = 2 × 0.10 = 0.20 mol.

Volume at STP = 0.20 × 22.4 = **4.48 dm³**.

(b) Moles of O₂ = 3 × 0.10 = 0.30 mol, so
mass = 0.30 × 32 = **9.6 g**.
:::

## 14.9 Kolbe's electrolysis method

::: definition Kolbe's electrolytic method
When a **concentrated aqueous solution of the sodium or potassium salt of a
carboxylic acid** is electrolysed, the carboxylate ion is discharged at the
anode, loses carbon dioxide and the resulting alkyl radicals couple to give an
**alkane with an even number of carbon atoms**.
:::

For sodium ethanoate the overall change is

2CH₃COONa + 2H₂O --electrolysis--> CH₃CH₃↑ + 2CO₂↑ + H₂↑ + 2NaOH

The mechanism, which NEB asks for in full, is:

**At the anode (oxidation).**

2CH₃COO⁻ → 2CH₃COO• + 2e⁻

2CH₃COO• → 2CH₃• + 2CO₂↑

CH₃• + CH₃• → CH₃CH₃

**At the cathode (reduction).**

2Na⁺ + 2e⁻ → 2Na

2Na + 2H₂O → 2NaOH + H₂↑

So ethane and carbon dioxide come off the anode and hydrogen off the cathode,
and the solution slowly turns alkaline.

::: key The carbon count rule
An acid RCOONa with **n** carbon atoms gives an alkane with **2(n − 1)** carbon
atoms. Sodium ethanoate (n = 2) gives ethane (2 C); sodium propanoate (n = 3)
gives butane (4 C). **Methane can never be made this way** — sodium methanoate
HCOONa would need n = 1, giving zero carbons, and in fact it gives hydrogen and
carbon dioxide only. Nor can any odd-carbon alkane be made from a single salt.
:::

2CH₃CH₂COONa + 2H₂O --electrolysis--> CH₃CH₂CH₂CH₃ + 2CO₂ + H₂ + 2NaOH

Electrolysing a **mixture** of two different salts gives three alkanes, exactly
as the Wurtz reaction does. A related use: the potassium salt of a dicarboxylic
acid ester gives long-chain diesters, which is how some polymer feedstocks are
made.

::: example Worked example 14.3 — identifying an unknown hydrocarbon
**Problem.** A gaseous hydrocarbon **A** has a vapour density of 27. It
decolourises bromine water and Baeyer's reagent, and gives a white precipitate
with ammoniacal silver nitrate. On treatment with dilute H₂SO₄ containing
HgSO₄ it gives a ketone **B**. Identify **A** and **B** and write the equations.

**Solution.**

*Step 1 — molecular formula.* Molar mass = 2 × vapour density = 2 × 27 =
54 g mol⁻¹.

For an alkyne CₙH₂ₙ₋₂: 12n + (2n − 2) = 54, so 14n = 56 and n = 4. The formula
is **C₄H₆**.

*Step 2 — which C₄H₆?* The white precipitate with ammoniacal AgNO₃ proves there
is a hydrogen on a triply bonded carbon, so A is **terminal**: A is
**but-1-yne**, CH₃CH₂C≡CH. (But-2-yne, CH₃C≡CCH₃, has no acidic hydrogen and
would give no precipitate.)

*Step 3 — the ketone.* Hydration follows Markovnikov's rule, so the OH goes to
C2:

CH₃CH₂C≡CH + H₂O --HgSO₄/H₂SO₄--> [CH₃CH₂C(OH)=CH₂] → CH₃CH₂COCH₃

B is **butan-2-one**, CH₃CH₂COCH₃.

*The other equations.*

CH₃CH₂C≡CH + 2Br₂ → CH₃CH₂CBr₂—CHBr₂

CH₃CH₂C≡CH + [Ag(NH₃)₂]OH → CH₃CH₂C≡C—Ag↓ + 2NH₃ + H₂O
:::

::: example Worked example 14.4 — a multi-step synthesis
**Problem.** Starting from calcium carbide only, and using any inorganic
reagents, show how you would prepare (a) ethanal, (b) ethane and (c) ethanoic
acid.

**Solution.**

*Step 0 — make ethyne.*

CaC₂ + 2H₂O → C₂H₂ + Ca(OH)₂

(a) **Ethanal** — hydrate the ethyne:

C₂H₂ + H₂O --40 % H₂SO₄, 1 % HgSO₄, 333 K--> CH₃CHO

(b) **Ethane** — hydrogenate twice over nickel:

C₂H₂ + 2H₂ --Ni, 523 K--> C₂H₆

(c) **Ethanoic acid** — oxidise the ethanal of part (a):

CH₃CHO + [O] --K₂Cr₂O₇/H₂SO₄--> CH₃COOH

A useful check: every carbon skeleton in the answer has exactly two carbons, as
it must, because no step joins or breaks a C—C bond.
:::

::: memory Reactions worth learning by heart
1. **Wurtz** doubles the carbons; **soda lime** removes one; **Kolbe** gives
   2(n − 1).
2. **Markovnikov**: "the rich get richer" — H goes to the carbon with more H.
3. **Peroxide effect: HBr only.**
4. **Lindlar** gives cis, **Na/liquid NH₃** gives trans.
5. **Ozonolysis** cuts the molecule exactly at the double bond.
6. **Ammoniacal AgNO₃ white, ammoniacal Cu₂Cl₂ red** — terminal alkynes only.
:::

## Chapter summary

- Alkanes are made by reducing haloalkanes (same carbon count), by the Wurtz
  reaction with Na in dry ether (double the carbons), by heating RCOONa with
  soda lime (one carbon fewer) and by hydrogenating alkenes or alkynes over Ni.
- Alkanes undergo free-radical substitution — halogenation (hν), vapour-phase
  nitration (673–773 K) and sulphonation with oleum — and are oxidised
  stepwise to alcohol, aldehyde, acid and finally CO₂ + H₂O.
- Alkenes are made by elimination: dehydration of alcohols (conc. H₂SO₄,
  443 K), dehydrohalogenation with alcoholic KOH, and partial hydrogenation of
  an alkyne over Lindlar's catalyst. Saytzeff's rule gives the more substituted
  alkene.
- Alkenes undergo electrophilic addition. HX follows Markovnikov's rule
  because the more stable carbocation forms; HBr with peroxide goes the other
  way. Hydration gives alcohols; H₂SO₄ gives alkyl hydrogen sulphates;
  ozonolysis followed by Zn/H₂O cleaves the molecule at the double bond.
- Alkynes come from C + H₂ in an electric arc, from 1,2-dibromoethane with
  alcoholic KOH, from CHCl₃ or CHI₃ with silver, and industrially from CaC₂ +
  H₂O. They add H₂, HX and H₂O (giving CH₃CHO from ethyne, ketones from all
  others).
- A terminal alkyne has an acidic hydrogen because sp carbon has 50 % s
  character: it gives H₂ with Na, a white Ag₂C₂ with ammoniacal AgNO₃ and a red
  Cu₂C₂ with ammoniacal Cu₂Cl₂.
- Bromine water and Baeyer's reagent are both decolourised by alkenes and
  alkynes but not alkanes; only ammoniacal AgNO₃ or Cu₂Cl₂ separates ethyne
  from ethene.
- Kolbe's electrolysis of concentrated aqueous RCOONa gives an alkane of
  2(n − 1) carbons at the anode along with CO₂, plus H₂ and NaOH at the cathode.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The Wurtz reaction of bromoethane gives <span class="marks">[1]</span>
   (a) ethane (b) propane (c) butane (d) ethene
2. Heating sodium propanoate with soda lime gives <span class="marks">[1]</span>
   (a) propane (b) ethane (c) methane (d) butane
3. Propene reacts with HBr in the presence of benzoyl peroxide to give mainly <span class="marks">[1]</span>
   (a) 2-bromopropane (b) 1-bromopropane (c) 1,2-dibromopropane (d) propan-2-ol
4. The catalyst used to stop the hydrogenation of an alkyne at the alkene stage is <span class="marks">[1]</span>
   (a) Raney nickel (b) Lindlar's catalyst (c) anhydrous AlCl₃ (d) HgSO₄
5. Ethyne can be distinguished from ethene by <span class="marks">[1]</span>
   (a) bromine water (b) Baeyer's reagent (c) ammoniacal AgNO₃ (d) burning it
6. Hydration of propyne with HgSO₄/H₂SO₄ gives <span class="marks">[1]</span>
   (a) propanal (b) propanone (c) propan-1-ol (d) propanoic acid
7. Kolbe's electrolysis of a concentrated solution of sodium ethanoate gives, at the anode, <span class="marks">[1]</span>
   (a) methane and CO₂ (b) ethane and CO₂ (c) ethene and H₂ (d) ethyne and O₂
8. Which one does **not** undergo sulphonation with oleum? <span class="marks">[1]</span>
   (a) hexane (b) heptane (c) 2-methylpropane (d) methane
9. The C—C bond length is shortest in <span class="marks">[1]</span>
   (a) ethane (b) ethene (c) ethyne (d) all are equal

::: note Answers to Group A
**1.** (c) — Wurtz coupling doubles the carbon count, 2 × C₂ = C₄.
**2.** (b) — decarboxylation removes one carbon from the three-carbon acid.
**3.** (b) — the peroxide effect makes the addition anti-Markovnikov.
**4.** (b) — Pd on CaCO₃ poisoned with quinoline.
**5.** (c) — only the terminal alkyne has an acidic H and gives a white Ag₂C₂ precipitate.
**6.** (b) — Markovnikov addition puts the OH on C2, and the enol tautomerises to the ketone.
**7.** (b) — 2CH₃COO⁻ → 2CH₃• + 2CO₂ + 2e⁻, and the methyl radicals couple.
**8.** (d) — the first three members, methane, ethane and propane, do not sulphonate.
**9.** (c) — 120 pm, against 134 pm for C=C and 154 pm for C—C.
:::

**Group B — Short answer (5 marks each)**

1. How is ethane prepared from (i) bromoethane by the Wurtz reaction,
   (ii) sodium propanoate, (iii) ethene and (iv) ethyne? Give equations with
   conditions. <span class="marks">[5]</span>
2. Describe the free-radical mechanism of the chlorination of methane, naming
   the three stages. Why is a trace of ethane always found in the product? <span class="marks">[5]</span>
3. State Markovnikov's rule and explain it on the basis of carbocation
   stability, using the addition of HBr to propene. <span class="marks">[5]</span>
4. What is the peroxide effect? Why is it shown by HBr but not by HCl or HI? <span class="marks">[5]</span>
5. What is ozonolysis? An alkene C₄H₈ gives only ethanal on ozonolysis.
   Identify it and write the equations. <span class="marks">[5]</span>
6. How would you distinguish between ethane, ethene and ethyne in the
   laboratory? Give the reagent, the observation and one equation in each case. <span class="marks">[5]</span>
7. Explain the acidic character of ethyne. Write the reactions with sodium,
   ammoniacal silver nitrate and ammoniacal cuprous chloride, giving the colour
   of each precipitate. <span class="marks">[5]</span>
8. What is Kolbe's electrolytic method? Write the anode and cathode reactions
   for a concentrated solution of sodium ethanoate, and state two limitations of
   the method. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** (i) 2CH₃Br + 2Na --dry ether--> C₂H₆ + 2NaBr (note bromomethane, not
bromoethane, is needed for ethane). (ii) CH₃CH₂COONa + NaOH --CaO, Δ--> C₂H₆ +
Na₂CO₃. (iii) C₂H₄ + H₂ --Ni, 523–573 K--> C₂H₆. (iv) C₂H₂ + 2H₂ --Ni--> C₂H₆.

**5.** Ozonolysis is the addition of ozone across a C=C to give an ozonide,
followed by cleavage with Zn/H₂O to give carbonyl compounds. If the only
product is ethanal, both halves of the molecule must be CH₃CH=, so the alkene
is **but-2-ene**:
CH₃CH=CHCH₃ + O₃ → ozonide, then ozonide + H₂O --Zn--> 2CH₃CHO.
(The isomer but-1-ene would give HCHO + CH₃CH₂CHO, and 2-methylpropene would
give HCHO + propanone.)

**6.** Bromine water: no change with ethane, decolourised by ethene and ethyne.
Ammoniacal AgNO₃: white precipitate with ethyne only,
C₂H₂ + 2[Ag(NH₃)₂]OH → Ag₂C₂↓ + 4NH₃ + 2H₂O. So no change to bromine water =
ethane; decolourises bromine water but gives no precipitate = ethene;
decolourises bromine water and gives a white precipitate = ethyne.

**8.** Definition as in Section 14.9.
Anode: 2CH₃COO⁻ → 2CH₃COO• + 2e⁻; 2CH₃COO• → 2CH₃• + 2CO₂; 2CH₃• → C₂H₆.
Cathode: 2Na⁺ + 2e⁻ → 2Na; 2Na + 2H₂O → 2NaOH + H₂.
Limitations: (i) only alkanes with an even number of carbons can be made, so
methane and propane are impossible; (ii) a mixture of two salts gives a mixture
of three alkanes; (iii) the solution must be concentrated, or oxygen is
discharged at the anode instead.
:::

**Group C — Long answer (8 marks each)**

1. (a) Describe, with equations and conditions, four laboratory methods of
   preparing an alkane. <span class="marks">[4]</span>
   (b) What happens when ethane is (i) chlorinated in sunlight, (ii) heated
   with nitric acid vapour at 673 K, (iii) oxidised with O₂ over a Cu tube at
   473 K and 100 atm, (iv) burnt in excess oxygen? <span class="marks">[4]</span>
2. (a) State Markovnikov's rule and the peroxide effect, and explain both in
   terms of the stability of the intermediate formed. <span class="marks">[4]</span>
   (b) Complete: (i) CH₃CH=CH₂ + H₂O/H⁺ → (ii) CH₂=CH₂ + conc. H₂SO₄ → , then
   + H₂O, Δ → (iii) 2-methylbut-2-ene + O₃, then Zn/H₂O → (iv) CH₃CH₂CHBrCH₃ +
   alc. KOH → <span class="marks">[4]</span>
3. (a) How is ethyne prepared from calcium carbide and from 1,2-dibromoethane?
   Give equations. <span class="marks">[3]</span>
   (b) Explain, with equations, the acidic nature of ethyne and the two
   precipitation tests based on it. <span class="marks">[3]</span>
   (c) 5.6 dm³ of ethyne at STP is burnt completely. Calculate the mass of
   carbon dioxide formed. <span class="marks">[2]</span>

::: note Answers to Group C
**2.** (b) (i) propan-2-ol, CH₃CH(OH)CH₃ — Markovnikov.
(ii) CH₂=CH₂ + H₂SO₄ → CH₃CH₂OSO₃H, and CH₃CH₂OSO₃H + H₂O --Δ--> C₂H₅OH +
H₂SO₄.
(iii) (CH₃)₂C=CHCH₃ gives propanone (CH₃)₂CO and ethanal CH₃CHO.
(iv) but-2-ene CH₃CH=CHCH₃ as the major product (Saytzeff) with but-1-ene as
the minor product.

**3.** (c) The balanced equation is 2C₂H₂ + 5O₂ → 4CO₂ + 2H₂O.
Moles of ethyne = 5.6 / 22.4 = 0.25 mol.
From the equation, 2 mol of C₂H₂ gives 4 mol of CO₂, i.e. 1 mol gives 2 mol,
so moles of CO₂ = 2 × 0.25 = 0.50 mol.
Mass of CO₂ = 0.50 × 44 = **22 g**.
:::
