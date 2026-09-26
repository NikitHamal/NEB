---
subject: Chemistry
grade: 12
unit: 15
title: Nitro Compounds
hours: 3
area: Organic Chemistry
---

A nitro compound carries the group –NO₂ bonded to carbon through **nitrogen**.
That one detail separates a nitroalkane, R–NO₂, from an alkyl nitrite, R–O–N=O,
which has the same molecular formula but is joined through oxygen. Nitro
compounds matter for two reasons: they are the standard doorway to amines (and
therefore to dyes and drugs), and the nitro group is the textbook example of a
strongly **deactivating, meta-directing** substituent on a benzene ring.

::: key What the examiner wants from this unit
Three things come up almost every year: **reduction of nitrobenzene in different
media** (the four-product table — learn it cold), **why nitrobenzene is
meta-directing and less reactive than benzene**, and the preparation of
nitroalkanes from haloalkanes with silver nitrite versus sodium nitrite.
:::

## 15.1 Nitroalkanes: introduction, nomenclature, isomerism

::: definition Nitroalkane
A nitroalkane is a compound obtained by replacing one hydrogen atom of an alkane
by a nitro group, –NO₂. General formula: **CₙH₂ₙ₊₁NO₂**, i.e. R–NO₂.
:::

In the nitro group the nitrogen is positively charged and one oxygen negatively
charged, but the two N–O bonds are found experimentally to be **identical**
(both 122 pm). The group is a resonance hybrid, and the negative charge is shared
equally by the two oxygens.

```figure caption="The nitro group is a resonance hybrid: the two canonical forms are equivalent, so both N–O bonds are identical and each oxygen carries a half negative charge."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.3))

def bond(p, q, n=1, shrink=0.26, dashed=False, lw=1.5):
    p = np.array(p, float); q = np.array(q, float)
    d = q - p; L = np.hypot(*d); u = d / L
    perp = np.array([-u[1], u[0]])
    a = p + u*shrink; b = q - u*shrink
    offs = [0.0] if n == 1 else [0.06, -0.06]
    for k, o in enumerate(offs):
        ls = '--' if (dashed and k == 1) else '-'
        ax.plot([a[0]+perp[0]*o, b[0]+perp[0]*o],
                [a[1]+perp[1]*o, b[1]+perp[1]*o],
                color=INK, lw=lw, ls=ls, solid_capstyle='round')

def unit(x, up, dn, qN, qU, qD, dash=False):
    R  = (x, 0.0); N = (x+0.95, 0.0)
    OU = (x+1.85, 0.62); OD = (x+1.85, -0.62)
    bond(R, N); bond(N, OU, up, dashed=dash); bond(N, OD, dn, dashed=dash)
    ax.text(*R, 'R', ha='center', va='center', fontsize=11, color=MUTED)
    ax.text(*N, 'N', ha='center', va='center', fontsize=11, color=INK)
    ax.text(*OU, 'O', ha='center', va='center', fontsize=11, color=INK)
    ax.text(*OD, 'O', ha='center', va='center', fontsize=11, color=INK)
    ax.text(N[0]+0.17, N[1]+0.24, qN, fontsize=9.5, color='#A8271F')
    ax.text(OU[0]+0.20, OU[1]+0.16, qU, fontsize=9.5, color='#A8271F')
    ax.text(OD[0]+0.20, OD[1]+0.16, qD, fontsize=9.5, color='#A8271F')

unit(0.0, 2, 1, '+', '', '−')
ax.text(2.55, 0.0, '↔', ha='center', va='center', fontsize=15, color=MUTED)
unit(3.1, 1, 2, '+', '−', '')
ax.text(5.65, 0.0, '≡', ha='center', va='center', fontsize=14, color=MUTED)
unit(6.2, 2, 2, '+', 'δ−', 'δ−', dash=True)
ax.set_xlim(-0.6, 8.9); ax.set_ylim(-1.35, 1.35)
ax.set_aspect('equal'); ax.axis('off')
```

Naming is simple: name the parent alkane, number the chain so the nitro group
gets the lowest number, and put *nitro-* as a prefix. Nitroalkanes are classified
as primary (1°), secondary (2°) or tertiary (3°) by the number of hydrogen atoms
on the carbon **bearing** the nitro group.

| Formula | IUPAC name | Class | α-hydrogens |
|---|---|---|---|
| CH₃NO₂ | nitromethane | 1° | 3 |
| CH₃CH₂NO₂ | nitroethane | 1° | 2 |
| CH₃CH₂CH₂NO₂ | 1-nitropropane | 1° | 2 |
| (CH₃)₂CHNO₂ | 2-nitropropane | 2° | 1 |
| (CH₃)₃CNO₂ | 2-methyl-2-nitropropane | 3° | 0 |

Nitroalkanes show four kinds of isomerism:

| Type | Example pair |
|---|---|
| Chain isomerism | 1-nitrobutane and 1-nitro-2-methylpropane (C₄H₉NO₂) |
| Position isomerism | 1-nitropropane and 2-nitropropane (C₃H₇NO₂) |
| Functional isomerism (metamerism) | nitroethane CH₃CH₂NO₂ and ethyl nitrite CH₃CH₂–O–N=O (C₂H₅NO₂) |
| Tautomerism | the nitro form and the *aci* form, possible only when α-H is present |

The **nitro–aci tautomerism** is worth writing out, because everything acidic
about nitroalkanes follows from it:

CH₃–NO₂ ⇌ CH₂=N(OH)→O   (nitro form ⇌ aci form)

Because the aci form is an –OH group, 1° and 2° nitroalkanes are weak acids and
dissolve in aqueous NaOH; 3° nitroalkanes, having no α-H, do not.

| Nitroalkane | pKa | Dissolves in NaOH? |
|---|---|---|
| Nitromethane | 10.2 | yes |
| Nitroethane | 8.6 | yes |
| 2-Nitropropane | 7.7 | yes |
| 2-Methyl-2-nitropropane | — (no α-H) | no |

## 15.2 Preparation of nitroalkanes, physical properties and reduction

**(a) From haloalkanes (Victor Meyer's method).** A haloalkane refluxed with
**silver nitrite** in ethanol gives the nitroalkane as the main product:

CH₃CH₂Br + AgNO₂ → CH₃CH₂NO₂ + AgBr↓

::: caution AgNO₂ versus NaNO₂ — the nitrite ion has two ends
The nitrite ion is ambident: it can attack through N (giving R–NO₂) or through O
(giving R–O–N=O). With **AgNO₂** the covalent character of the Ag–O bond leaves
nitrogen free, so the **nitroalkane** dominates. With ionic **NaNO₂ or KNO₂** in
ethanol the **alkyl nitrite** dominates. Writing "R–X + NaNO₂ → R–NO₂" in an
answer loses the mark. (In the polar aprotic solvent DMF, NaNO₂ does give mainly
the nitroalkane — the Kornblum modification.)
:::

Reactivity for the substitution follows 1° > 2° > 3°, and iodides react fastest.

**(b) From alkanes (vapour-phase nitration).** Industrially, an alkane and
nitric acid vapour are passed together at 400–450 °C:

CH₄ + HNO₃ --400–450 °C--> CH₃NO₂ + H₂O

The reaction is a free-radical chain, so with higher alkanes a mixture of all
possible mononitro products (plus C–C cleavage products) is obtained. Nitromethane,
nitroethane and the two nitropropanes are all made commercially this way from
propane.

**Physical properties.**

- Nitromethane and its homologues are colourless, pleasant-smelling liquids
  (they turn yellow on standing in light).
- The nitro group is strongly polar — nitromethane has a dipole moment of
  3.46 D — so the molecules attract one another by strong dipole–dipole forces
  and boil much higher than their molecular mass suggests.
- They are only sparingly soluble in water (no O–H or N–H to donate a hydrogen
  bond) but are excellent solvents themselves, and are **denser than water**
  (nitromethane 1.14 g cm⁻³).
- 1° and 2° nitroalkanes are weakly acidic (see the pKa table above); all
  nitroalkanes are toxic.

| Compound | M (g mol⁻¹) | Dipole moment (D) | Boiling point (°C) |
|---|---|---|---|
| Butane, C₄H₁₀ | 58 | 0 | −0.5 |
| Propanone, CH₃COCH₃ | 58 | 2.9 | 56 |
| Nitromethane, CH₃NO₂ | 61 | 3.46 | 101 |
| Nitroethane, C₂H₅NO₂ | 75 | 3.2 | 114 |

**Reduction.** Complete reduction gives a primary amine — the most useful
reaction of the whole class:

CH₃CH₂NO₂ + 6[H] --Sn/HCl--> CH₃CH₂NH₂ + 2H₂O

Controlled (partial) reduction with zinc dust and aqueous ammonium chloride stops
at the N-alkylhydroxylamine:

CH₃CH₂NO₂ + 4[H] --Zn/NH₄Cl--> CH₃CH₂NHOH + H₂O

| Reagent | Electrons supplied | Product |
|---|---|---|
| Sn/HCl, Fe/HCl, H₂ + Ni, LiAlH₄ | 6[H] | primary amine, R–NH₂ |
| Zn dust + NH₄Cl(aq), neutral | 4[H] | N-alkylhydroxylamine, R–NHOH |

::: example Worked example 15.1 — distinguishing 1°, 2° and 3° nitroalkanes
**Problem.** Three bottles contain 1-nitropropane, 2-nitropropane and
2-methyl-2-nitropropane. How would you identify each using nitrous acid?

**Solution.** Treat each with HNO₂ (NaNO₂ + dilute HCl, cold) and then add NaOH.

| Nitroalkane | Intermediate formed | Observation |
|---|---|---|
| 1-Nitropropane (1°, 2 α-H) | nitrolic acid, C₂H₅C(NO₂)=N–OH | **blood-red** solution with NaOH |
| 2-Nitropropane (2°, 1 α-H) | pseudonitrole, (CH₃)₂C(NO₂)NO | **blue** colour |
| 2-Methyl-2-nitropropane (3°, no α-H) | no reaction | remains **colourless** |

The test works because HNO₂ attacks the α-carbon. A 1° nitroalkane still has one
α-H left after attack and can tautomerise to the coloured nitrolic acid salt; a 2°
one has none left and stays as the blue pseudonitrole; a 3° one has no α-H to
attack in the first place.
:::

## 15.3 Nitrobenzene: preparation from benzene, physical properties

Benzene is nitrated by a **nitrating mixture** — 1 : 1 concentrated nitric acid
and concentrated sulphuric acid — at a carefully held 50–60 °C:

C₆H₆ + HNO₃ --conc. H₂SO₄, 50–60 °C--> C₆H₅NO₂ + H₂O

The sulphuric acid is not a spectator. It protonates nitric acid and pulls out
water, generating the actual electrophile, the **nitronium ion**:

HNO₃ + 2H₂SO₄ → NO₂⁺ + H₃O⁺ + 2HSO₄⁻

The NO₂⁺ then attacks the benzene ring in the usual two steps (attack giving an
arenium ion, then loss of H⁺). Above about 60 °C the product itself is nitrated
further to m-dinitrobenzene, which is why the temperature must be controlled with
a water bath.

**Physical properties of nitrobenzene.** A pale yellow oily liquid smelling of
bitter almonds; m.p. 5.7 °C, b.p. 211 °C, density 1.20 g cm⁻³; insoluble in
water but miscible with ethanol, ether and benzene; **steam-volatile**; and
highly poisonous — it is absorbed through the skin and converts haemoglobin to
methaemoglobin.

## 15.4 Reduction of nitrobenzene in different media

Nitrobenzene is the classic substrate whose reduction product depends entirely on
the **medium**. This is the single most examined table in the unit.

```figure caption="Reduction of nitrobenzene: the product is decided by the medium, not by the reducing metal."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,3.2))
ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off')
rows = [
    (8.8, 'Sn/HCl or Fe/HCl   (acidic)',      'C₆H₅NH₂\naniline',                 SERIES[0]),
    (6.4, 'Zn dust + NH₄Cl   (neutral)',  'C₆H₅NHOH\nN-phenylhydroxylamine',  SERIES[2]),
    (4.0, 'Zn dust + NaOH   (alkaline)',      'C₆H₅NH–NHC₆H₅\nhydrazobenzene',    SERIES[3]),
    (1.6, 'electrolysis in conc. H₂SO₄',      'p-H₂N–C₆H₄–OH\np-aminophenol',     SERIES[1]),
]
ax.text(0.1, 5.2, 'C₆H₅NO₂', fontsize=11.5, color=INK, ha='left', va='center',
        fontweight='bold')
ax.plot([2.3, 2.3], [rows[-1][0], rows[0][0]], color=MUTED, lw=1.1)
ax.plot([1.95, 2.3], [5.2, 5.2], color=MUTED, lw=1.1)
for y, reagent, prod, c in rows:
    ax.annotate('', xy=(6.0, y), xytext=(2.3, y),
                arrowprops=dict(arrowstyle='-|>', color=c, lw=1.5, mutation_scale=12))
    ax.text(4.15, y+0.22, reagent, fontsize=7.6, color=c, ha='center', va='bottom')
    ax.text(6.3, y, prod, fontsize=8.4, color=INK, ha='left', va='center')
```


| Medium | Reagent | Product | Equation |
|---|---|---|---|
| Acidic | Sn + conc. HCl, or Fe + HCl, or H₂/Ni | aniline | C₆H₅NO₂ + 6[H] → C₆H₅NH₂ + 2H₂O |
| Neutral | Zn dust + NH₄Cl(aq) | N-phenylhydroxylamine | C₆H₅NO₂ + 4[H] → C₆H₅NHOH + H₂O |
| Weakly alkaline | Na₃AsO₃ (sodium arsenite) | azoxybenzene | 2C₆H₅NO₂ + 6[H] → C₆H₅N(O)=NC₆H₅ + 3H₂O |
| Alkaline (mild) | LiAlH₄, or Zn + NaOH (limited) | azobenzene | 2C₆H₅NO₂ + 8[H] → C₆H₅N=NC₆H₅ + 4H₂O |
| Strongly alkaline | Zn dust + NaOH (excess) | hydrazobenzene | 2C₆H₅NO₂ + 10[H] → C₆H₅NHNHC₆H₅ + 4H₂O |
| Electrolytic, conc. H₂SO₄ | cathodic H, then rearrangement | p-aminophenol | C₆H₅NO₂ + 4[H] → p-H₂NC₆H₄OH + H₂O |
| Selective (for dinitro) | (NH₄)₂S or NH₄SH | m-nitroaniline | m-C₆H₄(NO₂)₂ + 3H₂S → m-NO₂C₆H₄NH₂ + 3S↓ + 2H₂O |

The industrial route to aniline uses iron filings and a little HCl (the Béchamp
reduction), and the whole equation balances neatly:

4C₆H₅NO₂ + 9Fe + 4H₂O → 4C₆H₅NH₂ + 3Fe₃O₄

::: tip How to remember the medium–product pattern
Acidic → the **most** reduced single-ring product (aniline). Neutral → stops
**halfway** (–NHOH). Alkaline → two rings **couple** (azoxy → azo → hydrazo, in
order of increasing reduction). Electrolytic in strong acid → the –NHOH
rearranges onto the ring, giving **p-aminophenol** (this is the industrial route
to paracetamol).
:::

::: example Worked example 15.2 — mass calculation on nitration and reduction
**Problem.** 39.0 g of benzene is nitrated with a 75 % yield, and all the
nitrobenzene formed is reduced by Sn/HCl with an 80 % yield. Calculate the mass
of aniline obtained. (C = 12, H = 1, N = 14, O = 16)

**Solution.**

Moles of benzene = 39.0 / 78 = 0.500 mol.

Step 1, nitration (1 : 1 stoichiometry): moles of nitrobenzene
= 0.500 × 0.75 = 0.375 mol. (Mass = 0.375 × 123 = 46.1 g.)

Step 2, reduction (1 : 1 stoichiometry): moles of aniline
= 0.375 × 0.80 = 0.300 mol.

Molar mass of aniline C₆H₅NH₂ = 6(12) + 7(1) + 14 = 93 g mol⁻¹.

Mass of aniline = 0.300 × 93 = **27.9 g**.
:::

## 15.5 Electrophilic substitution in nitrobenzene

The nitro group withdraws electrons both inductively (−I, nitrogen is positive)
and by resonance (−R, it pulls π electron density out of the ring). The ring is
therefore **electron-poor and strongly deactivated**: nitrobenzene is nitrated
about 10⁷ times more slowly than benzene itself, and Friedel–Crafts alkylation or
acylation fails completely on it.

```figure caption="Relative rate of nitration (benzene = 1) on a logarithmic scale. Electron-releasing groups activate the ring; –NO₂ deactivates it by about seven orders of magnitude."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.8))
names = ['C₆H₅NO₂', 'C₆H₅Cl', 'C₆H₆', 'C₆H₅CH₃', 'C₆H₅OH']
rates = [6e-8, 3.3e-2, 1.0, 25.0, 1.0e3]
cols  = [SERIES[1], SERIES[3], MUTED, SERIES[2], SERIES[0]]
ax.barh(names, rates, color=cols, height=0.6)
ax.set_xscale('log')
ax.set_xlim(1e-8, 1e5)
ax.set_xlabel('relative rate of nitration  (benzene = 1)')
ax.axvline(1.0, color=INK, lw=0.9, ls=':')
for n, r in zip(names, rates):
    ax.text(r*1.9, n, f'{r:g}', va='center', fontsize=7.8, color=INK)
ax.spines[['top','right','left']].set_visible(False)
ax.grid(True, axis='x', alpha=.45)
```

The group is also **meta-directing**. Attack at the *ortho* or *para* position
would put the positive charge of the intermediate arenium ion on the carbon that
already carries the positively charged nitrogen — an intolerable arrangement.
Only *meta* attack avoids this, so the meta product forms.

| Reaction | Conditions | Product |
|---|---|---|
| Nitration | conc. HNO₃ + conc. H₂SO₄, 95–100 °C | m-dinitrobenzene |
| Sulphonation | fuming H₂SO₄ (SO₃ + H₂SO₄), ~100 °C | m-nitrobenzenesulphonic acid |
| Bromination | Br₂ + anhydrous FeBr₃, ~100 °C | m-bromonitrobenzene |

C₆H₅NO₂ + HNO₃ --conc. H₂SO₄, 100 °C--> m-C₆H₄(NO₂)₂ + H₂O

C₆H₅NO₂ + H₂SO₄ --SO₃, 100 °C--> m-NO₂–C₆H₄–SO₃H + H₂O

C₆H₅NO₂ + Br₂ --FeBr₃, 100 °C--> m-NO₂–C₆H₄–Br + HBr

::: caution Harsher conditions, not different ones
The three reactions are the same electrophilic substitutions as for benzene, but
every one needs a **higher temperature and a stronger catalyst**, because the ring
is deactivated. Compare: benzene brominates at room temperature with FeBr₃;
nitrobenzene needs 100 °C.
:::

::: example Worked example 15.3 — a synthesis by ordering the steps
**Problem.** Starting from benzene, how would you prepare (a) m-nitroaniline and
(b) p-nitroaniline? Explain why the order of steps differs.

**Solution.**

(a) **m-Nitroaniline.** Nitrate twice, then reduce one group selectively.

C₆H₆ --HNO₃/H₂SO₄, 55 °C--> C₆H₅NO₂ --HNO₃/H₂SO₄, 100 °C--> m-C₆H₄(NO₂)₂

then m-C₆H₄(NO₂)₂ + 3H₂S --(NH₄)₂S--> m-NO₂C₆H₄NH₂ + 3S↓ + 2H₂O

Both nitro groups are meta-directing, so the second nitration necessarily gives
the 1,3-isomer; ammonium sulphide is mild enough to reduce only one of them.

(b) **p-Nitroaniline.** Here the amino group must be introduced **first**,
because –NH₂ is ortho/para-directing:

C₆H₅NO₂ --Sn/HCl--> C₆H₅NH₂ --(CH₃CO)₂O--> C₆H₅NHCOCH₃
--HNO₃/H₂SO₄--> p-NO₂C₆H₄NHCOCH₃ --H₃O⁺, hydrolysis--> p-NO₂C₆H₄NH₂

The acetyl group is needed because free aniline is protonated by the nitrating
mixture to –NH₃⁺, which is meta-directing, and is also oxidised by nitric acid.

**Why the order differs:** the directing effect of the group already on the ring
fixes where the next one goes. Put –NO₂ on first for a meta product, –NH₂ (as its
amide) on first for a para product.
:::

## 15.6 Uses of nitro compounds

| Compound | Use |
|---|---|
| Nitromethane, nitroethane | solvents for cellulose acetate, resins, waxes and paints; fuel for model and drag-racing engines |
| Nitroalkanes generally | starting materials for amines, hydroxylamines and, on chlorination, chloropicrin CCl₃NO₂ (a soil fumigant) |
| Nitrobenzene | about 97 % goes to make **aniline**, and hence azo dyes, rubber chemicals and drugs; also a solvent, a mild oxidising agent (Skraup quinoline synthesis) and "oil of mirbane", the almond scent of cheap soaps and shoe polish |
| p-Aminophenol (from nitrobenzene) | manufacture of **paracetamol** |
| 2,4,6-Trinitrotoluene (TNT) | high explosive; melts at 80 °C, so it can be poured into shells |
| 2,4,6-Trinitrophenol (picric acid) | explosive, yellow dye, and an antiseptic for burns |
| Nitroglycerine | the explosive in dynamite; in tiny doses a **vasodilator** for angina |
| Aromatic nitro drugs | chloramphenicol, nitrofurantoin and metronidazole — the last is prescribed widely in Nepal for giardiasis and amoebic dysentery |
| Nitro musks | fixatives in cheap perfumes |

## Chapter summary

- Nitroalkanes are R–NO₂ (CₙH₂ₙ₊₁NO₂); the nitro group is a resonance hybrid with
  two identical N–O bonds. Alkyl nitrites R–O–N=O are their functional isomers.
- Nitroalkanes show chain, position, functional and nitro–aci tautomeric
  isomerism. Only 1° and 2° (α-H present) are acidic and dissolve in NaOH.
- Preparation: R–X + AgNO₂ → R–NO₂ (with NaNO₂ you get the nitrite instead);
  CH₄ + HNO₃ at 400–450 °C → CH₃NO₂ + H₂O.
- Reduction: 6[H] gives R–NH₂; 4[H] with Zn/NH₄Cl stops at R–NHOH.
- Nitrobenzene: C₆H₆ + HNO₃ (conc. H₂SO₄, 50–60 °C) → C₆H₅NO₂ + H₂O, electrophile
  NO₂⁺. Pale yellow oil, b.p. 211 °C, bitter-almond smell, poisonous.
- Reduction of nitrobenzene: acidic → aniline; neutral → phenylhydroxylamine;
  alkaline → azoxy, azo, hydrazobenzene; electrolytic in conc. H₂SO₄ →
  p-aminophenol; (NH₄)₂S reduces only one group of a dinitro compound.
- –NO₂ is −I and −R, so it deactivates the ring (≈10⁷ times slower nitration) and
  is **meta-directing**: nitration, sulphonation and bromination all give the
  m-product, and Friedel–Crafts fails.
- Uses: aniline and dye manufacture, paracetamol, solvents, TNT, picric acid,
  nitroglycerine, metronidazole.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The functional isomer of nitroethane is <span class="marks">[1]</span>
   (a) nitromethane (b) ethyl nitrite (c) 2-nitropropane (d) ethanamine
2. Reduction of nitrobenzene with zinc dust and aqueous ammonium chloride gives <span class="marks">[1]</span>
   (a) aniline (b) azobenzene (c) N-phenylhydroxylamine (d) p-aminophenol
3. Nitration of nitrobenzene gives mainly <span class="marks">[1]</span>
   (a) o-dinitrobenzene (b) m-dinitrobenzene (c) p-dinitrobenzene (d) 1,3,5-trinitrobenzene
4. Which nitroalkane gives **no** colour with nitrous acid? <span class="marks">[1]</span>
   (a) nitromethane (b) nitroethane (c) 2-nitropropane (d) 2-methyl-2-nitropropane
5. The electrophile in the nitration of benzene is <span class="marks">[1]</span>
   (a) NO₂⁻ (b) NO₂⁺ (c) HNO₃ (d) NO⁺

::: note Answers to Group A
**1.** (b) — both are C₂H₅NO₂, but the nitrite is joined through oxygen.
**2.** (c) — a neutral medium stops the reduction at 4[H].
**3.** (b) — –NO₂ is meta-directing.
**4.** (d) — it is tertiary and has no α-hydrogen to attack.
**5.** (b) — the nitronium ion, generated by H₂SO₄ from HNO₃.
:::

**Group B — Short answer (5 marks each)**

1. What happens when a haloalkane is treated with (i) silver nitrite and (ii)
   sodium nitrite in ethanol? Explain the difference. <span class="marks">[5]</span>
2. Nitromethane boils at 101 °C while butane, of almost the same molecular mass,
   boils at −0.5 °C. Account for this, and explain why nitromethane is still only
   sparingly soluble in water. <span class="marks">[5]</span>
3. How is nitrobenzene prepared from benzene? Give the equation, the conditions,
   and the role of concentrated sulphuric acid. <span class="marks">[5]</span>
4. Explain, with reasons, why nitrobenzene undergoes electrophilic substitution
   more slowly than benzene and gives the meta product. <span class="marks">[5]</span>
5. 24.6 g of nitrobenzene is completely reduced by Sn/HCl. Calculate the mass of
   aniline formed if the yield is 90 %. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** AgNO₂ gives mainly the **nitroalkane** (CH₃CH₂Br + AgNO₂ → CH₃CH₂NO₂ + AgBr),
because the Ag–O bond is largely covalent and leaves the nitrogen lone pair as the
better nucleophilic site. NaNO₂ is ionic, the nitrite ion attacks through oxygen,
and the **alkyl nitrite** CH₃CH₂–O–N=O is the main product. The nitrite ion is
*ambident* — it has two nucleophilic sites.

**2.** Nitromethane has a very large dipole moment (3.46 D), so dipole–dipole
attraction between molecules is strong and a lot of energy is needed to separate
them; butane is non-polar and held only by weak London forces. Nitromethane can
*accept* hydrogen bonds from water but has no O–H or N–H of its own to donate, and
its hydrocarbon part is hydrophobic, so it cannot fit into water's hydrogen-bonded
network — hence low solubility.

**3.** C₆H₆ + HNO₃ --conc. H₂SO₄, 50–60 °C--> C₆H₅NO₂ + H₂O. Conditions: 1 : 1
nitrating mixture, water bath at 50–60 °C, reflux. H₂SO₄ protonates nitric acid
and removes water to generate the electrophile:
HNO₃ + 2H₂SO₄ → NO₂⁺ + H₃O⁺ + 2HSO₄⁻. Above 60 °C, m-dinitrobenzene is formed.

**4.** The –NO₂ group is electron-withdrawing both inductively (the N carries a
positive charge) and by resonance (it delocalises ring π electrons onto its
oxygens). The ring therefore has less electron density available for an
electrophile, and the arenium-ion intermediate is destabilised — nitration is
about 10⁷ times slower than for benzene. For *ortho* and *para* attack one
canonical form of the intermediate places the positive charge on the ring carbon
bearing the positive nitrogen, which is strongly destabilising; *meta* attack
never does, so the meta isomer is formed.

**5.** Moles of C₆H₅NO₂ = 24.6 / 123 = 0.200 mol. The reaction is 1 : 1, so
theoretical aniline = 0.200 mol = 0.200 × 93 = 18.6 g.
Actual mass = 18.6 × 0.90 = **16.74 g**.
:::

**Group C — Long answer (8 marks each)**

1. (a) Describe the reduction of nitrobenzene in acidic, neutral, strongly
   alkaline and electrolytic (conc. H₂SO₄) media, giving the product and a
   balanced equation in each case. <span class="marks">[5]</span>
   (b) How are 1°, 2° and 3° nitroalkanes distinguished by the nitrous acid
   test? <span class="marks">[3]</span>
2. (a) Starting from benzene, show how m-nitroaniline and p-nitroaniline are
   prepared, explaining why the order of the steps must differ. <span class="marks">[5]</span>
   (b) 78 g of benzene is nitrated (70 % yield) and the product is reduced to
   aniline (85 % yield). Find the mass of aniline obtained. <span class="marks">[3]</span>

::: note Answers to Group C
**1.** (a) Use the table in §15.4: acidic (Sn/HCl) → aniline,
C₆H₅NO₂ + 6[H] → C₆H₅NH₂ + 2H₂O; neutral (Zn/NH₄Cl) → N-phenylhydroxylamine,
C₆H₅NO₂ + 4[H] → C₆H₅NHOH + H₂O; strongly alkaline (Zn/NaOH excess) →
hydrazobenzene, 2C₆H₅NO₂ + 10[H] → C₆H₅NHNHC₆H₅ + 4H₂O; electrolytic in conc.
H₂SO₄ → p-aminophenol, C₆H₅NO₂ + 4[H] → p-H₂NC₆H₄OH + H₂O (the –NHOH formed first
rearranges in strong acid).
(b) 1° → blood-red nitrolic acid salt with NaOH; 2° → blue pseudonitrole;
3° → no reaction (no α-hydrogen). See Worked example 15.1.

**2.** (a) As in Worked example 15.3: nitrate twice then reduce with (NH₄)₂S for
the meta isomer; for the para isomer reduce first, protect the –NH₂ as
acetanilide, nitrate, then hydrolyse.
(b) Moles of benzene = 78 / 78 = 1.00 mol. Nitrobenzene = 1.00 × 0.70 = 0.70 mol.
Aniline = 0.70 × 0.85 = 0.595 mol = 0.595 × 93 = **55.3 g**.
:::
