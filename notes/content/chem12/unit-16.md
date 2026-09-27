---
subject: Chemistry
grade: 12
unit: 16
title: Amines
hours: 7
area: Organic Chemistry
---

Amines are the organic descendants of ammonia: replace one, two or three of the
hydrogens of NH₃ by alkyl or aryl groups and you get a primary, secondary or
tertiary amine. The nitrogen keeps its lone pair throughout, and almost the whole
chapter — basicity, salt formation, alkylation, acylation, diazotisation — is that
one lone pair doing chemistry. Amines are also the largest single family of
biologically active molecules: adrenaline, nicotine, quinine and most of the
drugs in a Nepali pharmacy are amines.

::: key What the examiner wants from this unit
Four high-value items: the **comparative basicity** of 1°, 2°, 3° amines and of
aniline (with reasons); **distinguishing 1°, 2° and 3° amines** by the nitrous
acid and carbylamine tests; **Hoffmann's separation** of an amine mixture; and the
reactions of **aniline** — diazotisation, coupling, and why nitration needs the
amino group protected first.
:::

## 16.1 Aliphatic amines: introduction, nomenclature, classification, isomerism

::: definition Amine
An amine is a compound derived from ammonia by replacing one or more hydrogen
atoms by alkyl or aryl groups. It is **primary (1°)**, **secondary (2°)** or
**tertiary (3°)** according to whether one, two or three hydrogens have been
replaced — that is, by the number of carbon atoms attached to nitrogen.
:::

```figure caption="Classification of amines by the number of carbon atoms on nitrogen. The lone pair (shown as two dots) survives in all three classes and is lost only in the quaternary salt."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.2,2.6))

def bond(p, q, shrink=0.24):
    p = np.array(p, float); q = np.array(q, float)
    d = q - p; L = np.hypot(*d); u = d / L
    a = p + u*shrink; b = q - u*shrink
    ax.plot([a[0], b[0]], [a[1], b[1]], color=INK, lw=1.5, solid_capstyle='round')

def amine(x, subs, lone=True, charge='', title='', formula='', eg=''):
    N = (x, 0.35)
    ax.text(*N, 'N', ha='center', va='center', fontsize=11.5, color=INK)
    pos = {'l': (x-0.85, 0.35), 'ur': (x+0.72, 1.02),
           'dr': (x+0.72, -0.32), 'd': (x, -0.58), 'u': (x, 1.28)}
    for key, lab in subs.items():
        p = pos[key]
        bond(N, p)
        c = SERIES[0] if lab.startswith('R') else MUTED
        ax.text(p[0], p[1], lab, ha='center', va='center', fontsize=10.5, color=c)
    if lone:
        ax.plot([x-0.10, x+0.10], [N[1]+0.36, N[1]+0.36], ls='none',
                marker='o', ms=2.6, color='#A8271F')
    if charge:
        ax.text(x+0.26, N[1]+0.30, charge, fontsize=10, color='#A8271F')
    ax.text(x, -1.15, title, ha='center', fontsize=9.2, color=INK, fontweight='bold')
    ax.text(x, -1.52, formula, ha='center', fontsize=8.8, color=INK)
    ax.text(x, -1.88, eg, ha='center', fontsize=8.2, color=MUTED)

amine(0.0, {'l':'R','ur':'H','dr':'H'}, title='primary (1°)',
      formula='R–NH₂', eg='CH₃NH₂')
amine(2.7, {'l':'R','ur':"R'",'dr':'H'}, title='secondary (2°)',
      formula='R₂NH', eg='(CH₃)₂NH')
amine(5.4, {'l':'R','ur':"R'",'dr':"R''"}, title='tertiary (3°)',
      formula='R₃N', eg='(CH₃)₃N')
amine(8.1, {'l':'R','ur':'R','dr':'R','d':'R'}, lone=False, charge='+',
      title='quaternary salt', formula='R₄N⁺X⁻', eg='(CH₃)₄N⁺I⁻')
ax.set_xlim(-1.3, 9.4); ax.set_ylim(-2.2, 1.7)
ax.set_aspect('equal'); ax.axis('off')
```

In the IUPAC system an amine is named as an **alkanamine**: drop the *-e* of the
alkane and add *-amine*. Groups on the nitrogen itself are prefixed with **N-**.

| Formula | IUPAC name | Common name | Class |
|---|---|---|---|
| CH₃NH₂ | methanamine | methylamine | 1° |
| CH₃CH₂CH₂NH₂ | propan-1-amine | n-propylamine | 1° |
| (CH₃)₂CHNH₂ | propan-2-amine | isopropylamine | 1° |
| CH₃NHCH₂CH₃ | N-methylethanamine | ethylmethylamine | 2° |
| (CH₃)₃N | N,N-dimethylmethanamine | trimethylamine | 3° |
| C₆H₅NH₂ | benzenamine | aniline | 1° (aromatic) |
| (CH₃)₄N⁺I⁻ | tetramethylammonium iodide | — | quaternary |

Amines show **chain**, **position** and **functional (metameric)** isomerism, and
those with a chiral carbon also show optical isomerism. C₃H₉N has exactly four
isomers, spread over all three classes:

| Isomer | Name | Class |
|---|---|---|
| CH₃CH₂CH₂NH₂ | propan-1-amine | 1° |
| (CH₃)₂CHNH₂ | propan-2-amine | 1° |
| CH₃CH₂NHCH₃ | N-methylethanamine | 2° |
| (CH₃)₃N | N,N-dimethylmethanamine | 3° |

## 16.2 Separation of 1°, 2° and 3° amines by Hoffmann's method

Ammonolysis of a haloalkane gives all three amines at once, so a method of
separating them is needed. **Hoffmann's method** uses **diethyl oxalate**,
(COOC₂H₅)₂, which reacts differently with each class.

(COOC₂H₅)₂ + 2RNH₂ → (CONHR)₂ + 2C₂H₅OH   (a **solid** dialkyl oxamide)

(COOC₂H₅)₂ + R₂NH → C₂H₅OOC–CO–NR₂ + C₂H₅OH   (a **liquid** oxamic ester)

R₃N + (COOC₂H₅)₂ → no reaction (no hydrogen on nitrogen)

The three are then separated physically and the original amines recovered by
hydrolysis with alkali:

(CONHR)₂ + 2NaOH → 2RNH₂ + (COONa)₂

```figure caption="Hoffmann's separation of a mixture of 1°, 2° and 3° amines using diethyl oxalate."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,3.3))
ax.set_xlim(0,10); ax.set_ylim(1.8,10.2); ax.axis('off')

def box(x, y, w, h, txt, fc='none', ec=INK, fs=8.0, bold=False):
    ax.add_patch(plt.Rectangle((x, y), w, h, fc=fc, ec=ec, lw=1.0))
    ax.text(x+w/2, y+h/2, txt, ha='center', va='center', fontsize=fs,
            color=INK, fontweight='bold' if bold else 'normal')

def arrow(p, q, c=MUTED):
    ax.annotate('', xy=q, xytext=p,
                arrowprops=dict(arrowstyle='-|>', color=c, lw=1.3, mutation_scale=11))

box(2.6, 9.0, 4.8, 1.0, 'mixture of 1°, 2°, 3° amines', bold=True, fs=8.6)
arrow((5.0, 9.0), (5.0, 8.35))
ax.text(5.25, 8.66, 'warm with diethyl oxalate (COOC₂H₅)₂',
        fontsize=7.4, color=MUTED, ha='left', va='center')
ax.plot([1.55, 8.45], [8.3, 8.3], color=MUTED, lw=1.2)
for x in (1.55, 5.0, 8.45):
    arrow((x, 8.3), (x, 7.65))
box(0.1, 6.1, 2.9, 1.5, 'solid oxamide\n(CONHR)₂\n(filter off)', fc='#eef4fa', fs=7.8)
box(3.55, 6.1, 2.9, 1.5, 'liquid ester\nC₂H₅OOC·CO·NR₂', fc='#eef7f0', fs=7.8)
box(7.0, 6.1, 2.9, 1.5, 'no reaction:\n3° amine R₃N\ndistils over', fc='#fbf1ee', fs=7.8)
for x, lab in ((1.55, 'NaOH'), (5.0, 'NaOH'), (8.45, 'already free')):
    arrow((x, 6.1), (x, 4.6))
    ax.text(x+0.18, 5.35, lab, fontsize=7.4, color=MUTED, ha='left', va='center')
box(0.1, 3.5, 2.9, 1.0, '1° amine  RNH₂', bold=True, fs=8.4)
box(3.55, 3.5, 2.9, 1.0, '2° amine  R₂NH', bold=True, fs=8.4)
box(7.0, 3.5, 2.9, 1.0, '3° amine  R₃N', bold=True, fs=8.4)
ax.text(5.0, 2.7, 'hydrolysis of the oxamide and the ester regenerates the amines',
        ha='center', fontsize=7.4, color=MUTED)
```

## 16.3 Preparation of primary amines

| Route | Reagents | Equation | Carbon change |
|---|---|---|---|
| From haloalkane (ammonolysis) | excess NH₃(alc.), 373 K, sealed tube | C₂H₅Br + 2NH₃ → C₂H₅NH₂ + NH₄Br | same |
| From nitrile (reduction) | Na + C₂H₅OH (Mendius), or LiAlH₄, or H₂/Ni | CH₃CN + 4[H] → CH₃CH₂NH₂ | **one more** C |
| From nitroalkane (reduction) | Sn/HCl or H₂/Ni | CH₃NO₂ + 6[H] → CH₃NH₂ + 2H₂O | same |
| From amide (reduction) | LiAlH₄ | CH₃CONH₂ + 4[H] → CH₃CH₂NH₂ + H₂O | same |
| From amide (Hofmann bromamide) | Br₂ + 4NaOH | CH₃CONH₂ + Br₂ + 4NaOH → CH₃NH₂ + Na₂CO₃ + 2NaBr + 2H₂O | **one fewer** C |

::: caution Ammonolysis never gives a pure product
The amine formed in C₂H₅Br + NH₃ is itself a nucleophile, so it attacks more
haloalkane: the product is a mixture of 1°, 2°, 3° amine **and** the quaternary
salt. A **large excess of ammonia** is used to push the first step and suppress
the rest. If a question asks for a *pure* primary amine, choose the Hofmann
bromamide reaction or reduction of a nitrile or nitro compound instead.
:::

The two amide routes are worth contrasting because they change the carbon
skeleton in opposite directions: LiAlH₄ reduction of ethanamide keeps both carbons
and gives ethylamine, whereas Hofmann bromamide degradation of the same ethanamide
loses a carbon as carbonate and gives **methylamine**.

## 16.4 Physical properties, basicity and comparative basic nature

**Physical properties.** Methylamine, dimethylamine and trimethylamine are gases;
the next members are liquids with a strong fishy, ammoniacal smell (the smell of
stale fish is largely trimethylamine). 1° and 2° amines have N–H bonds and
associate by hydrogen bonding, but 3° amines have none — so for the same molecular
mass the boiling point falls in the order **1° > 2° > 3°**.

| Compound (C₃H₉N, M = 59) | Class | N–H bonds | b.p. (°C) |
|---|---|---|---|
| Propan-1-amine | 1° | 2 | 48 |
| N-Methylethanamine | 2° | 1 | 37 |
| Trimethylamine | 3° | 0 | 3 |
| Propan-1-ol (for comparison, M = 60) | — | — | 97 |

All amines can accept hydrogen bonds from water, so the lower members are freely
water-soluble; solubility falls as the hydrocarbon chain grows. Amines boil lower
than alcohols of similar mass because N is less electronegative than O, so the
N···H–N hydrogen bond is weaker than O···H–O.

**Basicity.** The lone pair accepts a proton, so an amine is both a Brønsted and
a Lewis base:

RNH₂ + H₂O ⇌ RNH₃⁺ + OH⁻

$$ K_b = \frac{[\mathrm{RNH_3^+}][\mathrm{OH^-}]}{[\mathrm{RNH_2}]}, \qquad pK_b = -\log K_b $$

A **larger** $K_b$ — and therefore a **smaller** $pK_b$ — means a stronger base.
For a conjugate pair, $pK_a + pK_b = 14$ at 25 °C.

```figure caption="Measured $pK_b$ values at 25 °C. A smaller $pK_b$ means a stronger base, so the bars grow to the right as basicity falls."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9,3.0))
names = ['(CH₃)₂NH', 'CH₃NH₂', '(CH₃)₃N', 'NH₃',
         'p-CH₃C₆H₄NH₂', 'C₆H₅NH₂', 'p-NO₂C₆H₄NH₂']
pkb   = [3.27, 3.36, 4.19, 4.75, 8.92, 9.38, 13.0]
cols  = [SERIES[0]]*3 + [MUTED] + [SERIES[1]]*3
ax.barh(range(len(names)), pkb, color=cols, height=0.62)
ax.set_yticks(range(len(names))); ax.set_yticklabels(names, fontsize=8.2)
ax.invert_yaxis()
ax.set_xlabel('$pK_b$   (smaller = stronger base)')
ax.set_xlim(0, 14.5)
for i, v in enumerate(pkb):
    ax.text(v+0.25, i, f'{v}', va='center', fontsize=7.8, color=INK)
ax.axvline(4.75, color=INK, lw=0.9, ls=':')
ax.text(4.9, 6.35, 'ammonia', fontsize=7.4, color=MUTED)
ax.spines[['top','right','left']].set_visible(False)
ax.grid(True, axis='x', alpha=.45)
```

Three effects compete:

1. **+I effect of alkyl groups** pushes electron density onto nitrogen, making the
   lone pair more available. On this count alone, 3° > 2° > 1° > NH₃.
2. **Solvation of the cation.** The more N–H bonds the cation has, the more
   hydrogen bonds it makes with water, and the more stable it is. Here
   1° > 2° > 3°.
3. **Steric hindrance.** Three bulky groups crowd the nitrogen in a 3° amine and
   block both the incoming proton and the solvating water molecules.

In water the compromise gives, for the methyl series,

**(CH₃)₂NH > CH₃NH₂ > (CH₃)₃N > NH₃**

and for the ethyl series (C₂H₅ is a better electron donor than CH₃),

**(C₂H₅)₂NH > (C₂H₅)₃N > C₂H₅NH₂ > NH₃**

::: tip The gas-phase check
In the gas phase there is no water, so solvation cannot interfere and the order is
the pure inductive one: 3° > 2° > 1° > NH₃. Quoting this shows the examiner you
know *why* trimethylamine is out of place in water — it is a solvation effect, not
an electronic one.
:::

::: example Worked example 16.1 — pH of an amine solution
**Problem.** Calculate the pH of a 0.10 mol dm⁻³ solution of methylamine.
$K_b = 4.4\times 10^{-4}$.

**Solution.** For a weak base, CH₃NH₂ + H₂O ⇌ CH₃NH₃⁺ + OH⁻, with $c \gg K_b$:

$$ [\mathrm{OH^-}] = \sqrt{K_b\,c} = \sqrt{4.4\times10^{-4}\times 0.10} = \sqrt{4.4\times10^{-5}} $$

$$ [\mathrm{OH^-}] = 6.63\times10^{-3}\ \mathrm{mol\ dm^{-3}} $$

$$ pOH = -\log(6.63\times10^{-3}) = 2.18 \quad\Rightarrow\quad pH = 14 - 2.18 = 11.82 $$

The solution is strongly basic, as expected for a base about 25 times stronger
than ammonia.
:::

## 16.5 Reactions of primary amines

| Reagent | Product | Remark |
|---|---|---|
| CHCl₃ + alcoholic KOH, warm | alkyl isocyanide (carbylamine), R–NC | RNH₂ + CHCl₃ + 3KOH → RNC + 3KCl + 3H₂O — **only 1° amines**, foul smell |
| conc. HCl | alkylammonium chloride, RNH₃⁺Cl⁻ | shows basic character; NaOH regenerates the amine |
| R'–X (alkylation) | 2° → 3° amine → quaternary salt | exhaustive alkylation; the amine is the nucleophile |
| R'COCl or (R'CO)₂O (acylation) | N-substituted amide, R–NHCOR' | CH₃NH₂ + CH₃COCl → CH₃NHCOCH₃ + HCl; pyridine removes the HCl |
| HNO₂ (NaNO₂ + HCl, 0–5 °C) | alcohol + N₂↑ | RNH₂ + HNO₂ → ROH + N₂↑ + H₂O — brisk effervescence |

The carbylamine (Hofmann isocyanide) reaction is the quickest test for a primary
amine — the isocyanide has an extremely unpleasant smell and neither 2° nor 3°
amines give it:

CH₃NH₂ + CHCl₃ + 3KOH → CH₃NC + 3KCl + 3H₂O

Acylation converts a strongly basic, easily oxidised –NH₂ into a mild, stable
amide. That is why acylation is used as a **protecting group** (see §16.10).

## 16.6 Test of 1°, 2° and 3° amines

Nitrous acid, made *in situ* from NaNO₂ and dilute HCl at 0–5 °C, gives a
different result with each class.

| Amine | Reaction with HNO₂ | Observation |
|---|---|---|
| 1° aliphatic | RNH₂ + HNO₂ → ROH + N₂↑ + H₂O | **brisk effervescence** of N₂, no gas left in the tube |
| 2° | R₂NH + HNO₂ → R₂N–NO + H₂O | **yellow oily** N-nitrosoamine separates |
| 3° aliphatic | R₃N + HNO₂ → [R₃NH]⁺NO₂⁻ | clear solution only — a salt, no gas, no oil |
| 1° aromatic (aniline), 0–5 °C | C₆H₅NH₂ + NaNO₂ + 2HCl → C₆H₅N₂⁺Cl⁻ + NaCl + 2H₂O | clear solution; adding alkaline 2-naphthol gives an **orange-red dye** |

A second, cleaner test is **Hinsberg's test** with benzenesulphonyl chloride,
C₆H₅SO₂Cl, followed by aqueous NaOH.

```figure caption="Hinsberg's test. The product from a 1° amine still has an acidic N–H and dissolves in NaOH; the product from a 2° amine has none and stays as a precipitate; a 3° amine does not react at all."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.1,3.0))
ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off')
ax.text(0.1, 9.4, 'amine + C₆H₅SO₂Cl,  then aqueous NaOH', fontsize=9.0,
        color=INK, fontweight='bold')
rows = [(7.4, '1°  RNH₂',  'C₆H₅SO₂NHR',  'acidic N–H left',
         'clear solution\n(dissolves in NaOH)', SERIES[0]),
        (4.6, '2°  R₂NH',  'C₆H₅SO₂NR₂',  'no N–H left',
         'white precipitate\n(insoluble in NaOH)', SERIES[2]),
        (1.8, '3°  R₃N',   'no reaction',  'no N–H to replace',
         'amine layer only,\nno product', SERIES[1])]
for y, lab, prod, why, obs, c in rows:
    ax.text(0.1, y, lab, fontsize=9.2, color=INK, va='center', fontweight='bold')
    ax.annotate('', xy=(3.9, y), xytext=(1.6, y),
                arrowprops=dict(arrowstyle='-|>', color=c, lw=1.4, mutation_scale=11))
    ax.text(4.0, y, prod, fontsize=8.6, color=c, va='center')
    ax.text(4.0, y-0.72, why, fontsize=7.4, color=MUTED, va='center', style='italic')
    ax.add_patch(plt.Rectangle((6.9, y-0.85), 3.0, 1.7, fc='none', ec=c, lw=1.0))
    ax.text(8.4, y, obs, fontsize=7.6, color=INK, ha='center', va='center')
```

::: example Worked example 16.2 — identifying three unlabelled amines
**Problem.** Bottles P, Q and R contain propan-1-amine, N-methylethanamine and
trimethylamine in some order. On treatment with NaNO₂ + dilute HCl at 5 °C, P
gives a yellow oil, Q effervesces briskly and R gives only a clear solution.
Identify P, Q and R and confirm Q by a second test.

**Solution.**

- Brisk effervescence of N₂ means a **1° aliphatic amine**, so
  **Q = propan-1-amine**, CH₃CH₂CH₂NH₂
  (CH₃CH₂CH₂NH₂ + HNO₂ → CH₃CH₂CH₂OH + N₂↑ + H₂O).
- A yellow oily layer is an N-nitrosoamine, so **P = N-methylethanamine**
  (CH₃NHC₂H₅ + HNO₂ → CH₃N(NO)C₂H₅ + H₂O).
- Only a salt is formed with the 3° amine, so **R = trimethylamine**
  ((CH₃)₃N + HNO₂ → [(CH₃)₃NH]⁺NO₂⁻).

Confirmation of Q: warm with chloroform and alcoholic KOH. Only the primary amine
gives the vile-smelling carbylamine,
CH₃CH₂CH₂NH₂ + CHCl₃ + 3KOH → CH₃CH₂CH₂NC + 3KCl + 3H₂O.
Alternatively, Hinsberg's test on Q gives a sulphonamide that **dissolves** in
NaOH, while P's does not.
:::

## 16.7 Aniline: preparation from nitrobenzene and phenol; physical properties

**From nitrobenzene** (the industrial and laboratory route) — reduce in an acidic
medium:

C₆H₅NO₂ + 6[H] --Sn/conc. HCl--> C₆H₅NH₂ + 2H₂O

Using cheaper iron filings with a little HCl (the Béchamp reduction):

4C₆H₅NO₂ + 9Fe + 4H₂O → 4C₆H₅NH₂ + 3Fe₃O₄

**From phenol** — heat with ammonia over a zinc chloride (or alumina) catalyst at
about 300–350 °C under pressure:

C₆H₅OH + NH₃ --ZnCl₂, 300 °C--> C₆H₅NH₂ + H₂O

**Physical properties.** Pure aniline is a colourless oily liquid, but it darkens
to reddish-brown on standing because air oxidises it. It has a characteristic
unpleasant smell, b.p. 184 °C, m.p. −6 °C, density 1.02 g cm⁻³. It is only
slightly soluble in water (about 3.6 g per 100 g at 25 °C) but miscible with
ethanol, ether and benzene, is steam-volatile, and is **poisonous** — it is
absorbed through the skin and causes methaemoglobinaemia.

## 16.8 Basicity of aniline compared with aliphatic amines and ammonia

Aniline ($pK_b = 9.38$) is about **a million times weaker** a base than
methylamine ($pK_b = 3.36$) and much weaker than ammonia ($pK_b = 4.75$). Two
reasons, both about availability of the lone pair:

1. **Resonance.** The nitrogen lone pair is conjugated with the benzene ring and
   is delocalised over the *ortho* and *para* carbons. A delocalised pair is not
   free to bond a proton. In an aliphatic amine there is no such delocalisation.
2. **Loss of resonance energy on protonation.** In the anilinium ion C₆H₅NH₃⁺ the
   lone pair is tied up in the N–H bond, so the delocalisation is destroyed and
   the ion is *less* stabilised relative to the free base. The equilibrium
   therefore lies to the left.

A third, smaller contribution: the nitrogen of aniline is close to sp², and the
greater s-character holds the lone pair nearer the nucleus.

Substituents on the ring shift the value predictably — electron-releasing groups
raise basicity, electron-withdrawing groups lower it:

| Base | $pK_b$ | Comment |
|---|---|---|
| (CH₃)₂NH | 3.27 | strongest here; two +I groups |
| CH₃NH₂ | 3.36 | +I effect, no resonance |
| NH₃ | 4.75 | reference |
| p-Toluidine, p-CH₃C₆H₄NH₂ | 8.92 | –CH₃ releases electrons |
| Aniline | 9.38 | lone pair delocalised into ring |
| p-Nitroaniline | 13.0 | –NO₂ withdraws strongly; almost neutral |

Overall: **aliphatic amine > ammonia > aniline > diphenylamine > triphenylamine.**

## 16.9 Alkylation, acylation, diazotisation, carbylamine and coupling

| Reaction | Reagents and conditions | Product |
|---|---|---|
| Alkylation | CH₃I, then more CH₃I | C₆H₅NHCH₃ (N-methylaniline) → C₆H₅N(CH₃)₂ → quaternary salt |
| Acylation | (CH₃CO)₂O or CH₃COCl / pyridine | C₆H₅NHCOCH₃, **acetanilide** (m.p. 114 °C) + CH₃COOH |
| Benzoylation | C₆H₅COCl + NaOH (Schotten–Baumann) | C₆H₅NHCOC₆H₅, benzanilide |
| Diazotisation | NaNO₂ + 2HCl, 0–5 °C | C₆H₅N₂⁺Cl⁻, benzenediazonium chloride |
| Carbylamine | CHCl₃ + alcoholic KOH | C₆H₅NC, phenyl isocyanide (foul smell) |
| Coupling | C₆H₅N₂⁺Cl⁻ + phenol, NaOH, pH 9–10 | p-HO–C₆H₄–N=N–C₆H₅, an orange azo dye |
| Coupling | C₆H₅N₂⁺Cl⁻ + aniline, weakly acidic | p-H₂N–C₆H₄–N=N–C₆H₅, aniline yellow |

Written out, the two reactions that carry the most marks are:

C₆H₅NH₂ + NaNO₂ + 2HCl --0–5 °C--> C₆H₅N₂⁺Cl⁻ + NaCl + 2H₂O

C₆H₅N₂⁺Cl⁻ + C₆H₅OH --NaOH, 0–5 °C--> p-HO–C₆H₄–N=N–C₆H₅ + HCl

::: caution Keep the ice bath on
Benzenediazonium chloride decomposes above about 5 °C:
C₆H₅N₂⁺Cl⁻ + H₂O → C₆H₅OH + N₂↑ + HCl. Every diazotisation and every coupling
must be written **at 0–5 °C**; omitting the temperature is the commonest lost mark
in this unit. Coupling with a phenol needs *weak alkali*, coupling with an amine
needs *weak acid* — the diazonium ion is a feeble electrophile and needs an
activated ring.
:::

Azo coupling is the chemistry behind most synthetic textile dyes, and the
–N=N– chromophore is why they are coloured at all.

## 16.10 Electrophilic substitution in aniline; uses

The –NH₂ group is strongly activating and *ortho*/*para*-directing, so aniline
reacts far faster than benzene. Two complications follow:

- In the strongly acidic nitrating mixture, aniline is protonated to the
  anilinium ion, –NH₃⁺, which is **meta-directing**. Direct nitration therefore
  gives a poor mixture containing roughly half m-nitroaniline.
- Nitric acid also **oxidises** aniline to tarry products.

The answer is to protect the nitrogen by acetylation first.

| Reaction | Conditions | Product |
|---|---|---|
| Nitration (direct) | conc. HNO₃ + H₂SO₄ | mixture: o-, p- and about 47 % m-nitroaniline |
| Nitration (correct route) | acetylate → HNO₃/H₂SO₄ at 288 K → hydrolyse | **p-nitroaniline** |
| Sulphonation | conc. H₂SO₄, then bake at 180–200 °C | **sulphanilic acid**, p-H₂N–C₆H₄–SO₃H (a zwitterion) |
| Bromination | Br₂ in water, room temperature | **2,4,6-tribromoaniline**, white precipitate, at once |
| Bromination (monosubstitution) | acetylate → Br₂/CH₃COOH → hydrolyse | p-bromoaniline |

C₆H₅NH₂ + 3Br₂ → 2,4,6-C₆H₂Br₃(NH₂) + 3HBr

**Uses of aniline and amines.** Aniline is the feedstock for azo dyes (aniline
yellow, methyl orange, indigo), for **sulpha drugs** via sulphanilic acid, for
paracetamol, for rubber vulcanisation accelerators and antioxidants, for
polyurethane precursors, and in black printing ink and shoe polish. Aliphatic
amines are used as solvents, as corrosion inhibitors in boiler water, in making
nylon-6,6 (hexamethylenediamine), quaternary ammonium salts as cationic detergents
and disinfectants, and as intermediates for almost every synthetic drug.

::: example Worked example 16.3 — Hofmann bromamide numerical
**Problem.** 11.8 g of ethanamide (acetamide) is treated with bromine and sodium
hydroxide. Calculate the mass of amine obtained if the yield is 80 %. Name the
amine. (C = 12, H = 1, N = 14, O = 16, Br = 80)

**Solution.** The reaction removes one carbon:

CH₃CONH₂ + Br₂ + 4NaOH → CH₃NH₂ + Na₂CO₃ + 2NaBr + 2H₂O

Molar mass of CH₃CONH₂ = 2(12) + 5(1) + 14 + 16 = 59 g mol⁻¹.

Moles of ethanamide = 11.8 / 59 = 0.200 mol.

Stoichiometry is 1 : 1, so theoretical methylamine = 0.200 mol.
Molar mass of CH₃NH₂ = 12 + 5 + 14 = 31 g mol⁻¹, so theoretical mass
= 0.200 × 31 = 6.20 g.

Actual mass = 6.20 × 0.80 = **4.96 g of methylamine** (a primary amine with one
carbon fewer than the amide).
:::

::: example Worked example 16.4 — why the order of steps matters
**Problem.** Explain, with equations, why p-nitroaniline cannot be made by
nitrating aniline directly, and give a workable four-step synthesis from
nitrobenzene.

**Solution.** In the nitrating mixture, aniline is first protonated:

C₆H₅NH₂ + H₂SO₄ → C₆H₅NH₃⁺ + HSO₄⁻

The anilinium ion has no lone pair on nitrogen; –NH₃⁺ is electron-withdrawing and
**meta-directing**, so a large fraction of m-nitroaniline is formed, and HNO₃ also
oxidises part of the aniline to tar.

Workable route:

1. C₆H₅NO₂ + 6[H] --Sn/HCl--> C₆H₅NH₂ + 2H₂O
2. C₆H₅NH₂ + (CH₃CO)₂O → C₆H₅NHCOCH₃ + CH₃COOH  (protect the nitrogen)
3. C₆H₅NHCOCH₃ + HNO₃ --H₂SO₄, 288 K--> p-NO₂–C₆H₄–NHCOCH₃ + H₂O
4. p-NO₂–C₆H₄–NHCOCH₃ + H₂O --H⁺, heat--> p-NO₂–C₆H₄–NH₂ + CH₃COOH

The acetyl group is only weakly basic, so it is not protonated; it keeps the
directing effect *ortho/para* while reducing the activation enough to stop
polysubstitution and oxidation.
:::

## Chapter summary

- Amines are 1° (RNH₂), 2° (R₂NH) or 3° (R₃N) by the number of carbons on
  nitrogen; IUPAC names them alkanamines, with N- prefixes for groups on nitrogen.
  C₃H₉N has four isomers covering all three classes.
- Hoffmann's method separates a mixture with diethyl oxalate: 1° → solid oxamide,
  2° → liquid oxamic ester, 3° → no reaction; alkaline hydrolysis returns each
  amine.
- Primary amines: C₂H₅Br + 2NH₃ → C₂H₅NH₂ + NH₄Br; CH₃CN + 4[H] → CH₃CH₂NH₂
  (one more C); CH₃NO₂ + 6[H] → CH₃NH₂ + 2H₂O; CH₃CONH₂ + Br₂ + 4NaOH →
  CH₃NH₂ + Na₂CO₃ + 2NaBr + 2H₂O (one fewer C).
- Boiling point 1° > 2° > 3° at equal mass (hydrogen bonding); amines boil below
  alcohols of similar mass.
- $K_b = [\mathrm{RNH_3^+}][\mathrm{OH^-}]/[\mathrm{RNH_2}]$, and smaller $pK_b$
  means stronger base. In water: (CH₃)₂NH > CH₃NH₂ > (CH₃)₃N > NH₃; in the gas
  phase 3° > 2° > 1° > NH₃.
- Aniline ($pK_b = 9.38$) is a far weaker base than ammonia because its lone pair
  is delocalised into the ring and that stabilisation is lost on protonation.
- Distinguishing tests: HNO₂ gives N₂ effervescence (1°), a yellow nitrosoamine
  oil (2°) or just a salt (3°); CHCl₃ + alcoholic KOH gives the foul carbylamine
  only with 1°; Hinsberg's sulphonamide dissolves in NaOH only for 1°.
- Diazotisation at 0–5 °C: C₆H₅NH₂ + NaNO₂ + 2HCl → C₆H₅N₂⁺Cl⁻ + NaCl + 2H₂O;
  the diazonium salt couples with phenol (weak alkali) or aniline (weak acid) to
  give azo dyes.
- Aniline gives 2,4,6-tribromoaniline at once with bromine water, sulphanilic acid
  on baking with H₂SO₄, and needs acetyl protection before nitration to give
  p-nitroaniline.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The number of structural isomers of C₃H₉N is <span class="marks">[1]</span>
   (a) 2 (b) 3 (c) 4 (d) 5
2. Which one gives brisk effervescence of nitrogen with nitrous acid at 5 °C? <span class="marks">[1]</span>
   (a) (CH₃)₃N (b) CH₃NHCH₃ (c) CH₃CH₂NH₂ (d) C₆H₅N(CH₃)₂
3. The correct order of basic strength **in aqueous solution** is <span class="marks">[1]</span>
   (a) (CH₃)₃N > (CH₃)₂NH > CH₃NH₂ > NH₃
   (b) (CH₃)₂NH > CH₃NH₂ > (CH₃)₃N > NH₃
   (c) NH₃ > CH₃NH₂ > (CH₃)₂NH > (CH₃)₃N
   (d) CH₃NH₂ > (CH₃)₂NH > NH₃ > (CH₃)₃N
4. Aniline is a weaker base than ammonia because <span class="marks">[1]</span>
   (a) it is a liquid (b) its lone pair is delocalised into the ring
   (c) it is aromatic (d) nitrogen is sp³ hybridised
5. Benzenediazonium chloride is prepared at 0–5 °C because <span class="marks">[1]</span>
   (a) the reaction is exothermic (b) it decomposes to phenol and N₂ above 5 °C
   (c) aniline freezes (d) HCl evaporates
6. The Hinsberg product of a secondary amine is <span class="marks">[1]</span>
   (a) soluble in NaOH (b) insoluble in NaOH (c) a gas (d) not formed

::: note Answers to Group A
**1.** (c) — two 1° amines, one 2° and one 3°.
**2.** (c) — only a 1° aliphatic amine gives an unstable diazonium salt that
releases N₂.
**3.** (b) — the compromise between +I effect, cation solvation and steric
hindrance.
**4.** (b) — delocalisation removes the lone pair from service, and the anilinium
ion loses that resonance energy.
**5.** (b) — C₆H₅N₂⁺Cl⁻ + H₂O → C₆H₅OH + N₂↑ + HCl.
**6.** (b) — C₆H₅SO₂NR₂ has no acidic N–H, so it cannot form a sodium salt.
:::

**Group B — Short answer (5 marks each)**

1. Classify amines with one example each, and write the four structural isomers of
   C₃H₉N with their IUPAC names. <span class="marks">[5]</span>
2. Describe Hoffmann's method for separating a mixture of 1°, 2° and 3° amines,
   with equations. <span class="marks">[5]</span>
3. Arrange CH₃NH₂, (CH₃)₂NH, (CH₃)₃N and NH₃ in order of basic strength in water
   and justify the order. Why does the order change in the gas phase? <span class="marks">[5]</span>
4. How will you distinguish between propan-1-amine, N-methylethanamine and
   trimethylamine? Give reagents, equations and observations. <span class="marks">[5]</span>
5. Calculate the pH of a 0.050 mol dm⁻³ solution of ethylamine
   ($K_b = 5.0\times10^{-4}$). <span class="marks">[5]</span>
6. What is diazotisation? Give the equation and explain the coupling reaction of
   benzenediazonium chloride with phenol. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** See §16.1: 1° R–NH₂ (CH₃NH₂), 2° R₂NH ((CH₃)₂NH), 3° R₃N ((CH₃)₃N).
Isomers of C₃H₉N: propan-1-amine, propan-2-amine (both 1°), N-methylethanamine
(2°), N,N-dimethylmethanamine (3°).

**2.** Warm the mixture with diethyl oxalate. 1° → solid oxamide,
(COOC₂H₅)₂ + 2RNH₂ → (CONHR)₂ + 2C₂H₅OH; 2° → liquid oxamic ester,
(COOC₂H₅)₂ + R₂NH → C₂H₅OOC·CO·NR₂ + C₂H₅OH; 3° does not react and distils over
unchanged. Filter the solid from the liquid, then hydrolyse each with NaOH:
(CONHR)₂ + 2NaOH → 2RNH₂ + (COONa)₂.

**3.** In water: (CH₃)₂NH > CH₃NH₂ > (CH₃)₃N > NH₃. Alkyl groups release electrons
(+I), so replacing H by CH₃ increases the electron density on nitrogen; but each
replacement also removes one N–H from the cation, reducing hydrogen-bonded
solvation, and three methyl groups sterically crowd the nitrogen. Two methyls give
the best balance. In the gas phase there is no solvent, so only the +I effect
operates and the order becomes (CH₃)₃N > (CH₃)₂NH > CH₃NH₂ > NH₃.

**4.** Use NaNO₂ + dilute HCl at 0–5 °C. Propan-1-amine: brisk N₂,
C₃H₇NH₂ + HNO₂ → C₃H₇OH + N₂↑ + H₂O. N-Methylethanamine: yellow oil,
CH₃NHC₂H₅ + HNO₂ → CH₃N(NO)C₂H₅ + H₂O. Trimethylamine: clear solution of
[(CH₃)₃NH]⁺NO₂⁻ only. Confirm the first with the carbylamine test,
C₃H₇NH₂ + CHCl₃ + 3KOH → C₃H₇NC + 3KCl + 3H₂O.

**5.** $[\mathrm{OH^-}] = \sqrt{K_bc} = \sqrt{5.0\times10^{-4}\times0.050}
= \sqrt{2.5\times10^{-5}} = 5.0\times10^{-3}$ mol dm⁻³.
So $pOH = 2.30$ and **pH = 11.70**.

**6.** Diazotisation is the conversion of a primary aromatic amine into a diazonium
salt with nitrous acid at 0–5 °C:
C₆H₅NH₂ + NaNO₂ + 2HCl → C₆H₅N₂⁺Cl⁻ + NaCl + 2H₂O. The diazonium ion is a weak
electrophile, so it attacks only a strongly activated ring. With phenol in weak
alkali (pH 9–10, which generates the more reactive phenoxide) it substitutes at
the para position:
C₆H₅N₂⁺Cl⁻ + C₆H₅OH → p-HO–C₆H₄–N=N–C₆H₅ + HCl, an orange azo dye.
:::

**Group C — Long answer (8 marks each)**

1. (a) How is aniline prepared from nitrobenzene and from phenol? Give equations
   and conditions. <span class="marks">[3]</span>
   (b) Compare the basicity of aniline with that of methylamine and ammonia, with
   reasons. <span class="marks">[3]</span>
   (c) Why does bromine water give 2,4,6-tribromoaniline immediately, whereas
   p-bromoaniline needs a three-step route? <span class="marks">[2]</span>
2. (a) Give the reactions of a primary amine with chloroform and alcoholic KOH,
   with an acid chloride, with an alkyl halide and with nitrous acid. <span class="marks">[4]</span>
   (b) 8.85 g of ethanamide is subjected to the Hofmann bromamide reaction with a
   70 % yield. Name the product and calculate its mass. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** (a) C₆H₅NO₂ + 6[H] --Sn/conc. HCl--> C₆H₅NH₂ + 2H₂O (industrially
4C₆H₅NO₂ + 9Fe + 4H₂O → 4C₆H₅NH₂ + 3Fe₃O₄); and
C₆H₅OH + NH₃ --ZnCl₂, 300 °C, pressure--> C₆H₅NH₂ + H₂O.
(b) Basicity CH₃NH₂ ($pK_b$ 3.36) > NH₃ (4.75) > C₆H₅NH₂ (9.38). Methylamine is
strengthened by the +I effect of CH₃; aniline is weakened because the lone pair is
delocalised into the ring and because the anilinium ion loses that resonance
stabilisation on protonation.
(c) –NH₂ is so strongly activating that all three free *ortho/para* positions
react at once with bromine water, giving the tribromo compound. Acetylation
moderates the activation (and the bulky group blocks the ortho positions), so
bromination then stops at the para position; hydrolysis afterwards frees the
amine.

**2.** (a) Carbylamine: RNH₂ + CHCl₃ + 3KOH → RNC + 3KCl + 3H₂O.
Acylation: CH₃NH₂ + CH₃COCl → CH₃NHCOCH₃ + HCl.
Alkylation: CH₃NH₂ + CH₃I → (CH₃)₂NH·HI, continuing to (CH₃)₃N and (CH₃)₄N⁺I⁻.
Nitrous acid: RNH₂ + HNO₂ → ROH + N₂↑ + H₂O.
(b) Moles of CH₃CONH₂ = 8.85 / 59 = 0.150 mol. The product is **methylamine**,
CH₃NH₂ (M = 31). Theoretical mass = 0.150 × 31 = 4.65 g; at 70 % yield,
mass = 4.65 × 0.70 = **3.26 g**.
:::
