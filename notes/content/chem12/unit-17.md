---
subject: Chemistry
grade: 12
unit: 17
title: Organometallic Compounds
hours: 2
area: Organic Chemistry
---

An organometallic compound contains a **direct metal–carbon bond**. That single
requirement is what makes these compounds so useful: in almost every other organic
molecule carbon is the electron-poor end of its bonds, but a metal is less
electronegative than carbon, so here the carbon is electron-**rich** and behaves
as a carbanion. A compound that supplies a nucleophilic carbon lets you join two
carbon skeletons together, and that is how most alcohols, acids and ketones are
built in the laboratory.

::: key What the examiner wants from this unit
One question dominates: **how a Grignard reagent is prepared and what it gives
with each reagent** — especially the aldehyde/ketone route to 1°, 2° and 3°
alcohols and the CO₂ route to carboxylic acids. Learn the reactivity order
RLi > RMgX > R₂Cd and be able to explain it from electronegativity.
:::

## 17.1 Introduction, general formula and examples

::: definition Organometallic compound
An organometallic compound is one in which at least one carbon atom of an organic
group is bonded **directly** to a metal atom, C–M.
:::

By this definition sodium ethoxide C₂H₅–O–Na and sodium ethanoate CH₃COONa are
**not** organometallic, because the metal is joined to oxygen, not to carbon.
Ethylmagnesium bromide C₂H₅–Mg–Br is.

| Class | General formula | Examples | Made from |
|---|---|---|---|
| Organolithium | R–Li | CH₃Li (methyllithium), C₄H₉Li (n-butyllithium), C₆H₅Li | R–X + 2Li → R–Li + LiX, in dry ether or hexane |
| Organomagnesium (Grignard) | R–Mg–X | CH₃MgI, C₂H₅MgBr, C₆H₅MgBr | R–X + Mg, dry ether |
| Organocopper (Gilman reagent) | R₂CuLi | (CH₃)₂CuLi, lithium dimethylcuprate | 2RLi + CuI → R₂CuLi + LiI |
| Organocadmium | R₂Cd | (CH₃)₂Cd, (C₂H₅)₂Cd | 2RMgX + CdCl₂ → R₂Cd + MgCl₂ + MgX₂ |

The three non-Grignard classes exist because chemists need **different levels of
reactivity**:

- **Organolithiums** are the most reactive. They add even to crowded ketones and
  can pull a proton off a benzene ring. They catch fire in air, so they are
  handled in an inert atmosphere.
- **Organocuprates** are the most *selective*. They couple with haloalkanes
  (R₂CuLi + R'X → R–R', the Corey–House synthesis) yet leave an ester or a nitrile
  in the same molecule untouched.
- **Organocadmiums** are the least reactive. They convert an acid chloride into a
  **ketone and stop there**, whereas a Grignard reagent would attack the ketone
  again and give a tertiary alcohol:

CH₃COCl + (CH₃)₂Cd → CH₃COCH₃ + CH₃CdCl

## 17.2 Nature of the metal–carbon bond

Carbon has a Pauling electronegativity of 2.55, and every metal here is lower. The
shared pair is therefore pulled towards **carbon**, giving the polarity

Cδ⁻ — Mδ⁺

The larger the electronegativity difference, the more ionic the bond, the more
carbanion-like the carbon, and the more reactive the reagent.

```figure caption="Ionic character of the carbon–metal bond, from the Pauling relation % ionic $= 100\\left[1-e^{-0.25(\\Delta\\chi)^2}\\right]$. Reactivity of the reagent follows the same order."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9,2.9))
metals = ['C–Li', 'C–Mg', 'C–Zn', 'C–Cd', 'C–Cu', 'C–Hg', 'C–Pb']
chi    = [0.98, 1.31, 1.65, 1.69, 1.90, 2.00, 2.33]
d      = np.array([2.55 - x for x in chi])
ionic  = 100*(1 - np.exp(-0.25*d**2))
cols   = [SERIES[1], SERIES[0], MUTED, SERIES[2], SERIES[3], MUTED, MUTED]
ax.bar(metals, ionic, color=cols, width=0.62)
for m, v, dd in zip(metals, ionic, d):
    ax.text(m, v+1.2, f'{v:.0f}%', ha='center', fontsize=7.8, color=INK)
ax.set_ylabel('ionic character of the C–M bond (%)')
ax.set_ylim(0, 56)
ax.annotate('more reactive, more carbanion-like', xy=(0.05, 0.86),
            xycoords='axes fraction', fontsize=7.8, color=MUTED)
ax.annotate('', xy=(0.04, 0.80), xytext=(0.52, 0.80), xycoords='axes fraction',
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.2, mutation_scale=11))
ax.spines[['top','right']].set_visible(False)
ax.grid(True, axis='y', alpha=.45)
```

| Bond | Δ(electronegativity) | Ionic character | Consequence |
|---|---|---|---|
| C–Li | 1.57 | ≈ 46 % | nearly a free carbanion; violently reactive |
| C–Mg | 1.24 | ≈ 32 % | strongly polar covalent; the working compromise |
| C–Cd | 0.86 | ≈ 17 % | mildly polar; attacks only acid chlorides |
| C–Pb | 0.22 | ≈ 1 % | essentially covalent and unreactive (tetraethyllead) |

::: key Why organometallics react at all
The reactive site is the **carbon**, not the metal. Because it carries a partial
negative charge, it attacks any electron-poor centre — the carbon of a C=O group,
the carbon of CO₂, or the hydrogen of any O–H, N–H or S–H bond.
:::

## 17.3 Grignard reagent: preparation from haloalkane and haloarene

::: definition Grignard reagent
An alkyl- or aryl-magnesium halide, R–Mg–X, made by the action of magnesium on a
haloalkane or haloarene in **dry ether**. Victor Grignard received the 1912 Nobel
Prize for it.
:::

CH₃CH₂Br + Mg --dry (C₂H₅)₂O--> CH₃CH₂MgBr   (ethylmagnesium bromide)

C₆H₅Br + Mg --dry ether--> C₆H₅MgBr   (phenylmagnesium bromide)

```figure caption="Formation of a Grignard reagent. Magnesium inserts into the C–X bond; two ether molecules donate lone pairs to the magnesium and keep the reagent in solution."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.6))
ax.set_xlim(0, 9.4); ax.set_ylim(-1.95, 1.75); ax.axis('off')

def bond(p, q, shrink=0.30, c=INK, lw=1.5, ls='-'):
    p = np.array(p, float); q = np.array(q, float)
    u = (q-p)/np.hypot(*(q-p))
    a = p + u*shrink; b = q - u*shrink
    ax.plot([a[0], b[0]], [a[1], b[1]], color=c, lw=lw, ls=ls, solid_capstyle='round')

# left: haloalkane + Mg
ax.text(0.35, 0.0, 'R', fontsize=11, ha='center', va='center', color=SERIES[0])
ax.text(1.35, 0.0, 'X', fontsize=11, ha='center', va='center', color=INK)
bond((0.35,0), (1.35,0))
ax.text(2.25, 0.0, '+', fontsize=11, ha='center', va='center', color=MUTED)
ax.text(3.05, 0.0, 'Mg', fontsize=11, ha='center', va='center', color='#A8271F')
ax.annotate('', xy=(5.2, 0.0), xytext=(3.75, 0.0),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.4, mutation_scale=12))
ax.text(4.5, 0.22, 'dry ether', fontsize=7.8, color=MUTED, ha='center')
ax.text(4.5, -0.42, 'trace I₂', fontsize=7.8, color=MUTED, ha='center')
# right: R-Mg-X with two ether donors
R = (5.9, 0.0); M = (7.2, 0.0); X = (8.5, 0.0)
ax.text(*R, 'R', fontsize=11, ha='center', va='center', color=SERIES[0])
ax.text(*M, 'Mg', fontsize=11, ha='center', va='center', color='#A8271F')
ax.text(*X, 'X', fontsize=11, ha='center', va='center', color=INK)
bond(R, M); bond(M, X)
ax.text(7.2, 1.30, '(C₂H₅)₂O', fontsize=8.6, ha='center', va='center', color=SERIES[2])
ax.text(7.2, -1.30, '(C₂H₅)₂O', fontsize=8.6, ha='center', va='center', color=SERIES[2])
bond((7.2, 1.30), M, shrink=0.34, c=SERIES[2], lw=1.1, ls=(0,(3,2)))
bond((7.2,-1.30), M, shrink=0.34, c=SERIES[2], lw=1.1, ls=(0,(3,2)))
ax.text(5.9, -0.75, 'δ−', fontsize=8.5, color='#A8271F', ha='center')
ax.text(7.62, 0.26, 'δ+', fontsize=8.5, color='#A8271F', ha='center')
ax.text(7.2, -1.62, 'ether-solvated Grignard reagent', fontsize=7.6,
        color=MUTED, ha='center')
```

**Conditions that matter.**

- The ether must be **absolutely dry** and the apparatus moisture-free; the Mg
  turnings are cleaned to expose fresh metal and a crystal of iodine is added to
  start the reaction.
- The ether is not just a solvent: the oxygen lone pairs **coordinate** to the
  magnesium, satisfying its electron demand and keeping the reagent dissolved.
  Tetrahydrofuran (THF) does the job even better.
- Reactivity of the halide: **R–I > R–Br > R–Cl**, and alkyl > aryl.
- **Haloarenes** are far less reactive because the C–X bond has partial double-bond
  character. Bromobenzene and iodobenzene work in ether, but **chlorobenzene will
  not react in ether at all** — it needs THF at reflux (66 °C).

::: caution The reagent destroys itself with water
Any compound with an active hydrogen — water, alcohol, acid, amine, even a
terminal alkyne — protonates the carbanion carbon and the reagent is gone:
CH₃MgI + H₂O → CH₄↑ + Mg(OH)I. This is why the whole preparation is done under
anhydrous conditions, and why you never wash a Grignard mixture with water until
the reaction you wanted is finished.
:::

## 17.4 Reactions of the Grignard reagent

Every reaction follows the same pattern: the δ− carbon attacks an electron-poor
carbon (or hydrogen), giving a magnesium salt, which is then **hydrolysed with
dilute acid** to release the organic product.

```figure caption="The Grignard reaction map. In every case the nucleophilic carbon adds first and dilute acid is used in a second step."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.1,3.4))
ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off')
rows = [
    (9.1, 'H₂O',                    'R–H  alkane',                 SERIES[3]),
    (7.8, 'HCHO,  then H₃O⁺',       'R–CH₂OH  1° alcohol',         SERIES[0]),
    (6.5, "R'CHO,  then H₃O⁺",      "R'CH(OH)R  2° alcohol",       SERIES[0]),
    (5.2, "R'COR'',  then H₃O⁺",    'tertiary alcohol  3°',        SERIES[0]),
    (3.9, 'CO₂ (dry ice), H₃O⁺',    'R–COOH  carboxylic acid',     SERIES[2]),
    (2.6, 'HCN,  then H₃O⁺',        'R–CHO  aldehyde',             SERIES[1]),
    (1.3, "R'CN,  then H₃O⁺",       "R–CO–R'  ketone",             SERIES[1]),
]
ax.text(0.1, 5.2, 'R–Mg–X', fontsize=11, color=INK, ha='left', va='center',
        fontweight='bold')
ax.plot([2.0, 2.0], [rows[-1][0], rows[0][0]], color=MUTED, lw=1.1)
ax.plot([1.72, 2.0], [5.2, 5.2], color=MUTED, lw=1.1)
for y, reagent, prod, c in rows:
    ax.annotate('', xy=(5.2, y), xytext=(2.0, y),
                arrowprops=dict(arrowstyle='-|>', color=c, lw=1.4, mutation_scale=11))
    ax.text(3.6, y+0.14, reagent, fontsize=7.6, color=c, ha='center', va='bottom')
    ax.text(5.45, y, prod, fontsize=8.2, color=INK, ha='left', va='center')
```

| Reagent | Intermediate | Final product after H₃O⁺ |
|---|---|---|
| Water (or ROH, NH₃, RCOOH) | — | alkane R–H + Mg(OH)X |
| Methanal, HCHO | R–CH₂–OMgX | **primary** alcohol R–CH₂OH |
| Any other aldehyde, R'CHO | R'RCH–OMgX | **secondary** alcohol |
| Ketone, R'COR'' | R'R''RC–OMgX | **tertiary** alcohol |
| Carbon dioxide (solid CO₂) | R–COOMgX | carboxylic acid R–COOH (one C more) |
| Hydrogen cyanide, HCN | RCH=N–MgX | aldehyde R–CHO |
| Nitrile, R'CN | R'(R)C=N–MgX | ketone R–CO–R' |
| Ester, R'COOR'' (2 equivalents) | — | tertiary alcohol with **two identical** R groups |
| Acid chloride, R'COCl (1 equivalent, cold) | — | ketone R–CO–R'; excess RMgX gives the 3° alcohol |

Worked through with real formulae:

CH₃MgI + HCHO → CH₃CH₂OMgI --H₃O⁺--> CH₃CH₂OH + Mg(OH)I

CH₃MgI + CH₃CHO → (CH₃)₂CHOMgI --H₃O⁺--> (CH₃)₂CHOH  (propan-2-ol, 2°)

CH₃MgI + CH₃COCH₃ → (CH₃)₃COMgI --H₃O⁺--> (CH₃)₃COH  (2-methylpropan-2-ol, 3°)

C₂H₅MgBr + CO₂ → C₂H₅COOMgBr --H₃O⁺--> C₂H₅COOH  (propanoic acid)

CH₃COOC₂H₅ + 2CH₃MgI → (CH₃)₃COMgI + C₂H₅OMgI --H₃O⁺--> (CH₃)₃COH + C₂H₅OH

::: example Worked example 17.1 — choosing the right pair
**Problem.** Give **two** different Grignard routes to 2-methylbutan-2-ol,
CH₃CH₂C(CH₃)₂OH.

**Solution.** A tertiary alcohol comes from a ketone, so break one of the three
C–C bonds at the alcohol carbon. The piece you remove becomes the Grignard reagent
and what is left becomes the ketone.

Route 1 — break the ethyl group:

CH₃CH₂MgBr + CH₃COCH₃ → CH₃CH₂C(CH₃)₂OMgBr --H₃O⁺--> CH₃CH₂C(CH₃)₂OH

Route 2 — break a methyl group:

CH₃MgI + CH₃CH₂COCH₃ → CH₃CH₂C(CH₃)₂OMgI --H₃O⁺--> CH₃CH₂C(CH₃)₂OH

(Butan-2-one is the ketone in Route 2.) A third route uses an ester:
CH₃COOC₂H₅ would give 2-methylbutan-2-ol only if the two added groups were
identical, which here they are — 2 CH₃MgI on ethyl propanoate C₂H₅COOC₂H₅ gives
the same alcohol.
:::

::: example Worked example 17.2 — mass of a carboxylic acid
**Problem.** 10.9 g of bromoethane is converted into a Grignard reagent, which is
poured onto excess solid CO₂ and then hydrolysed. Calculate the mass of acid
obtained if the overall yield is 75 %. (C = 12, H = 1, O = 16, Br = 80)

**Solution.**

Molar mass of C₂H₅Br = 2(12) + 5(1) + 80 = 109 g mol⁻¹, so
moles = 10.9 / 109 = 0.100 mol.

The Grignard reagent is formed 1 : 1, and carbonation adds exactly one carbon:

C₂H₅MgBr + CO₂ → C₂H₅COOMgBr --H₃O⁺--> C₂H₅COOH

Product is propanoic acid, C₂H₅COOH, M = 3(12) + 6(1) + 2(16) = 74 g mol⁻¹.

Theoretical mass = 0.100 × 74 = 7.40 g. At 75 % yield,
mass = 7.40 × 0.75 = **5.55 g**.
:::

::: example Worked example 17.3 — Zerewitinoff active-hydrogen determination
**Problem.** 0.60 g of an organic compound liberates 224 cm³ of methane, measured
at STP, when treated with excess methylmagnesium iodide. How many active hydrogen
atoms does one molecule contain if its molar mass is 60 g mol⁻¹? Suggest a
structure.

**Solution.** Each active hydrogen releases one molecule of methane:

CH₃MgI + R–OH → CH₄↑ + R–OMgI

Moles of CH₄ = 0.224 / 22.4 = 0.0100 mol.

Moles of compound = 0.60 / 60 = 0.0100 mol.

Ratio = 0.0100 : 0.0100 = **1 active hydrogen per molecule**.

With M = 60 and one active H the compound could be ethanoic acid CH₃COOH or
propan-1-ol C₃H₇OH. Sodium hydrogen carbonate settles it: the acid gives brisk
CO₂ effervescence, the alcohol does not.
:::

## Chapter summary

- An organometallic compound has a direct C–M bond; C₂H₅ONa and CH₃COONa do not
  qualify.
- Classes: R–Li (organolithium), R–Mg–X (Grignard), R₂CuLi (Gilman cuprate),
  R₂Cd (organocadmium). Reactivity RLi > RMgX > R₂Cd; R₂Cd converts RCOCl into a
  ketone and stops there.
- Carbon (2.55) is more electronegative than every one of these metals, so the bond
  is Cδ⁻–Mδ⁺. Ionic character: C–Li ≈ 46 %, C–Mg ≈ 32 %, C–Cd ≈ 17 %. More ionic
  means more carbanion-like and more reactive.
- Preparation: R–X + Mg in dry ether → RMgX; reactivity R–I > R–Br > R–Cl.
  The ether coordinates to Mg. Chlorobenzene needs THF at reflux, not ether.
- Any active hydrogen kills the reagent: CH₃MgI + H₂O → CH₄↑ + Mg(OH)I
  (the basis of Zerewitinoff's method).
- Alcohols: HCHO → 1°, RCHO → 2°, ketone → 3°. CO₂ → carboxylic acid with one
  extra carbon. HCN → aldehyde, R'CN → ketone, ester (2 equiv.) → 3° alcohol with
  two identical groups, acid chloride → ketone then 3° alcohol.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Which is **not** an organometallic compound? <span class="marks">[1]</span>
   (a) C₂H₅MgBr (b) CH₃Li (c) C₂H₅ONa (d) (CH₃)₂Cd
2. A Grignard reagent reacts with methanal to give, after hydrolysis, a <span class="marks">[1]</span>
   (a) primary alcohol (b) secondary alcohol (c) tertiary alcohol (d) ketone
3. The C–M bond is most ionic in <span class="marks">[1]</span>
   (a) C–Pb (b) C–Cd (c) C–Mg (d) C–Li
4. Ethylmagnesium bromide poured on solid CO₂ and then hydrolysed gives <span class="marks">[1]</span>
   (a) ethanoic acid (b) propanoic acid (c) ethanol (d) propan-1-ol
5. Dry ether is used in preparing a Grignard reagent because <span class="marks">[1]</span>
   (a) it is cheap (b) its oxygen lone pairs coordinate to magnesium
   (c) it reacts with the halide (d) it oxidises magnesium

::: note Answers to Group A
**1.** (c) — sodium is bonded to oxygen, not to carbon.
**2.** (a) — HCHO supplies only one carbon substituent, so R–CH₂OH results.
**3.** (d) — lithium has the lowest electronegativity, Δχ = 1.57.
**4.** (b) — carbonation adds one carbon to the ethyl group.
**5.** (b) — coordination stabilises the magnesium and keeps RMgX in solution.
:::

**Group B — Short answer (5 marks each)**

1. Define an organometallic compound. Give the general formula and one example
   each of organolithium, organocopper and organocadmium compounds. <span class="marks">[5]</span>
2. Explain the nature of the carbon–metal bond and use it to account for the
   reactivity order RLi > RMgX > R₂Cd. <span class="marks">[5]</span>
3. How is ethylmagnesium bromide prepared? State three precautions and explain why
   chlorobenzene does not form a Grignard reagent in ether. <span class="marks">[5]</span>
4. How would you obtain (i) propan-1-ol, (ii) propan-2-ol and (iii)
   2-methylpropan-2-ol from a Grignard reagent? Give equations. <span class="marks">[5]</span>
5. 21.8 g of bromoethane is converted to its Grignard reagent and treated with
   excess methanal, then hydrolysed. Calculate the mass of alcohol formed at 80 %
   yield. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** See §17.1. R–Li (CH₃Li), R₂CuLi ((CH₃)₂CuLi), R₂Cd ((CH₃)₂Cd).

**2.** Carbon (χ = 2.55) is more electronegative than the metals, so the bonding
pair lies nearer carbon: Cδ⁻–Mδ⁺. The bigger the electronegativity difference the
more ionic the bond and the freer the carbanion. Δχ is 1.57 for C–Li (≈46 % ionic),
1.24 for C–Mg (≈32 %) and 0.86 for C–Cd (≈17 %), giving RLi > RMgX > R₂Cd.

**3.** C₂H₅Br + Mg --dry ether--> C₂H₅MgBr. Precautions: (i) all apparatus and the
ether must be perfectly dry, since water destroys the reagent; (ii) clean Mg
turnings and a crystal of iodine are used to start the reaction; (iii) the mixture
is kept away from air and moisture and gently refluxed. Chlorobenzene fails
because the C–Cl bond in a haloarene has partial double-bond character (resonance)
and is too strong to be attacked by Mg in ether; THF at 66 °C is needed instead.

**4.** (i) C₂H₅MgBr + HCHO → C₂H₅CH₂OMgBr --H₃O⁺--> CH₃CH₂CH₂OH (1°).
(ii) CH₃MgI + CH₃CHO → (CH₃)₂CHOMgI --H₃O⁺--> (CH₃)₂CHOH.
(iii) CH₃MgI + CH₃COCH₃ → (CH₃)₃COMgI --H₃O⁺--> (CH₃)₃COH.

**5.** Moles of C₂H₅Br = 21.8 / 109 = 0.200 mol. With HCHO the ethyl group gains
one carbon, so the product is propan-1-ol, C₃H₇OH, M = 60 g mol⁻¹. Theoretical
mass = 0.200 × 60 = 12.0 g; at 80 % yield, mass = **9.6 g**.
:::

**Group C — Long answer (8 marks each)**

1. (a) How is a Grignard reagent prepared from a haloalkane and from a haloarene?
   Give equations and conditions. <span class="marks">[3]</span>
   (b) Describe its reactions with water, carbon dioxide, an ester and a nitrile,
   giving the product in each case. <span class="marks">[5]</span>
2. (a) Show how 1°, 2° and 3° alcohols are prepared from Grignard reagents, using
   ethanal, methanal and propanone as the carbonyl compounds. <span class="marks">[5]</span>
   (b) 0.90 g of a compound of molar mass 90 g mol⁻¹ liberates 448 cm³ of methane
   at STP with excess CH₃MgI. How many active hydrogen atoms has it? <span class="marks">[3]</span>

::: note Answers to Group C
**1.** (a) CH₃CH₂Br + Mg --dry ether--> CH₃CH₂MgBr; C₆H₅Br + Mg --dry ether-->
C₆H₅MgBr. Absolutely anhydrous conditions, clean magnesium, a crystal of iodine to
initiate; chlorobenzene requires THF at 66 °C.
(b) Water: CH₃MgI + H₂O → CH₄↑ + Mg(OH)I (alkane). CO₂: C₂H₅MgBr + CO₂ →
C₂H₅COOMgBr, then H₃O⁺ gives propanoic acid. Ester: two equivalents add, giving a
tertiary alcohol with two identical groups, e.g.
CH₃COOC₂H₅ + 2CH₃MgI → (CH₃)₃COH after hydrolysis. Nitrile: addition to C≡N gives a
ketimine salt which hydrolyses to a ketone,
CH₃MgI + CH₃CN → CH₃C(=NMgI)CH₃ --H₃O⁺--> CH₃COCH₃.

**2.** (a) HCHO + CH₃MgI → ethanol (1°); CH₃CHO + CH₃MgI → propan-2-ol (2°);
CH₃COCH₃ + CH₃MgI → 2-methylpropan-2-ol (3°). Each requires acid hydrolysis of the
alkoxide intermediate R–OMgI.
(b) Moles of CH₄ = 0.448 / 22.4 = 0.0200 mol. Moles of compound = 0.90 / 90 =
0.0100 mol. Ratio 2 : 1, so the molecule has **2 active hydrogen atoms** —
consistent with lactic acid, CH₃CH(OH)COOH (M = 90), which has one –OH and one
–COOH hydrogen.
:::
