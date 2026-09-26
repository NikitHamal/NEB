---
subject: Chemistry
grade: 12
unit: 11
title: Phenols
hours: 4
area: Organic Chemistry
---

A phenol has its –OH group attached **directly to the benzene ring**. That single
difference from an alcohol changes everything. The oxygen lone pair is drawn into
the ring, so the O–H bond becomes markedly more polar and phenol behaves as a
genuine, if weak, acid — it dissolves in sodium hydroxide, which no alcohol does.
The same lone-pair donation floods the ring with electron density, so phenol
undergoes electrophilic substitution far faster than benzene and always at the
ortho and para positions.

::: key The two questions to keep answering
Almost everything in this unit is one of two questions: **"why is phenol acidic
when ethanol is not?"** (answer: resonance stabilisation of the phenoxide ion)
and **"why does the ring react so fast, and where?"** (answer: the same lone
pair, delivered to positions 2, 4 and 6). Learn to draw the resonance structures
— examiners award marks for the diagrams, not the words.
:::

## 11.1 Introduction and nomenclature

Phenols are compounds of general formula Ar–OH. A **monohydric** phenol has one
–OH on the ring, a **dihydric** phenol two, and so on. Phenol itself, C₆H₅OH, was
called *carbolic acid* by Lister, who used it as the first surgical antiseptic.

Do **not** confuse a phenol with an aromatic alcohol: in benzyl alcohol,
C₆H₅CH₂OH, the –OH sits on a side-chain carbon, not on the ring, so it behaves
like an ordinary primary alcohol and gives no colour with FeCl₃.

| Structure | IUPAC name | Common name |
|---|---|---|
| C₆H₅OH | phenol | carbolic acid |
| 2-CH₃C₆H₄OH | 2-methylphenol | *o*-cresol |
| 4-CH₃C₆H₄OH | 4-methylphenol | *p*-cresol |
| 1,2-C₆H₄(OH)₂ | benzene-1,2-diol | catechol |
| 1,3-C₆H₄(OH)₂ | benzene-1,3-diol | resorcinol |
| 1,4-C₆H₄(OH)₂ | benzene-1,4-diol | quinol (hydroquinone) |
| 1,2,3-C₆H₃(OH)₃ | benzene-1,2,3-triol | pyrogallol |
| 2,4,6-(O₂N)₃C₆H₂OH | 2,4,6-trinitrophenol | picric acid |
| C₁₀H₇OH | naphthalen-1-ol | α-naphthol |

## 11.2 Preparation from chlorobenzene, diazonium salt, benzene sulphonic acid

**(a) From chlorobenzene — Dow's process.** Chlorobenzene is very unreactive, so
forcing conditions are needed: 10 % aqueous NaOH at 300 °C and about 150 atm.

C₆H₅Cl + 2NaOH --300 °C, 150 atm--> C₆H₅ONa + NaCl + H₂O

C₆H₅ONa + HCl → C₆H₅OH + NaCl

**(b) From benzene diazonium chloride.** Aniline is diazotised at 0–5 °C and the
diazonium salt solution is then simply warmed above 5 °C with dilute acid:

C₆H₅NH₂ + HNO₂ + HCl --0–5 °C--> C₆H₅N₂Cl + 2H₂O

C₆H₅N₂Cl + H₂O --warm, >5 °C--> C₆H₅OH + N₂↑ + HCl

This is the laboratory method: mild, and the nitrogen simply bubbles away.

**(c) From benzene sulphonic acid — alkali fusion.** The sodium salt is fused
with solid sodium hydroxide at 300–350 °C:

C₆H₅SO₃H + NaOH → C₆H₅SO₃Na + H₂O

C₆H₅SO₃Na + 2NaOH --fuse, 300–350 °C--> C₆H₅ONa + Na₂SO₃ + H₂O

C₆H₅ONa + HCl → C₆H₅OH + NaCl

::: caution Acidify at the end, or you get the salt
All three routes stop at **sodium phenoxide**, which is a water-soluble salt, not
phenol. The final acidification step — with HCl, dilute H₂SO₄ or even by passing
CO₂ — is worth a mark and is regularly forgotten.
:::

## 11.3 Physical properties

- Colourless, needle-shaped **crystalline solid**, m.p. 40.9 °C, b.p. 181.8 °C.
  On standing in air and light it slowly oxidises and turns **pink to red**.
- Characteristic sharp "carbolic" smell; **corrosive and poisonous** — it raises
  painful blisters on skin, so it is handled with gloves.
- **Sparingly soluble** in cold water (about 8.3 g per 100 g at 20 °C) because the
  large hydrocarbon ring is water-repelling, but freely soluble in ethanol,
  ether and benzene. Above 66 °C phenol and water mix in all proportions.
- Its boiling point is very high for its molar mass (94 g mol⁻¹) because the
  molecules are linked by **intermolecular hydrogen bonds**, just as in alcohols.
- Phenol dissolves readily in aqueous NaOH (forming sodium phenoxide) — a
  physical observation that is really a chemical test.

## 11.4 Acidic nature: comparison with alcohol and water

Phenol ionises slightly in water:

C₆H₅OH + H₂O ⇌ C₆H₅O⁻ + H₃O⁺,  $K_a = 1.0\times10^{-10}$,  $\mathrm{p}K_a = 10.0$

Two effects work together.

**(i) The phenoxide ion is resonance-stabilised.** Its negative charge is not
stuck on oxygen; it is delocalised over the two ortho and one para carbon atoms.
Spreading charge lowers energy, so the conjugate base is unusually stable and the
equilibrium above lies further right than for an alcohol. In an alkoxide ion,
CH₃CH₂O⁻, no such delocalisation is possible — and the electron-releasing (+I)
ethyl group actually pushes more charge onto the oxygen, making the ion *less*
stable still.

**(ii) The O–H bond in phenol is already polarised.** In phenol itself the oxygen
lone pair is fed into the ring, giving oxygen a partial positive charge. Oxygen
therefore pulls harder on the shared pair of the O–H bond, and the proton leaves
more easily.

```figure caption="Resonance in phenol and in the phenoxide ion. In phenol the lone pair delocalises away from oxygen, leaving it δ+ and weakening the O–H bond; in the phenoxide ion the negative charge is spread over three ring carbons, which is why the conjugate base — and therefore phenol's acidity — is so much greater than an alkoxide's."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9,4.5))
ax.axis('off'); ax.set_aspect('equal')
OX = '#d9534f'; NEG = '#1d6fb8'
R = 0.46
ANG = np.radians(np.array([90.,150.,210.,270.,330.,30.]))

def charge(x, y, sign, col):
    ax.add_patch(plt.Circle((x, y), 0.115, fill=False, ec=col, lw=0.9, zorder=4))
    ax.text(x, y + 0.005, sign, color=col, fontsize=7.6, ha='center',
            va='center', zorder=5)

def struct(cx, cy, dbl, exo, ocharge, neg, oh=False):
    V = np.c_[cx + R*np.cos(ANG), cy + R*np.sin(ANG)]
    C = np.array([cx, cy])
    for a, b in [(0,1),(1,2),(2,3),(3,4),(4,5),(5,0)]:
        p, q = V[a], V[b]
        ax.plot([p[0],q[0]], [p[1],q[1]], color=INK, lw=1.25,
                solid_capstyle='round', zorder=2)
        if (a, b) in dbl:
            d = q - p; L = np.hypot(*d); n = np.array([-d[1], d[0]])/L
            if np.dot((p+q)/2 + n - C, n) > np.dot((p+q)/2 - C, n) * 0 + 0:
                pass
            if np.hypot(*((p+q)/2 + n*0.1 - C)) > np.hypot(*((p+q)/2 - C)):
                n = -n
            s, t = 0.10, 0.17
            ax.plot([p[0]+n[0]*s + d[0]*t, q[0]+n[0]*s - d[0]*t],
                    [p[1]+n[1]*s + d[1]*t, q[1]+n[1]*s - d[1]*t],
                    color=INK, lw=1.25, zorder=2)
    top = V[0]
    if exo:
        for s in (-0.050, 0.050):
            ax.plot([top[0]+s, top[0]+s], [top[1]+0.03, top[1]+0.30],
                    color=INK, lw=1.25, zorder=2)
    else:
        ax.plot([top[0], top[0]], [top[1]+0.03, top[1]+0.30],
                color=INK, lw=1.25, zorder=2)
    ax.text(top[0], top[1]+0.46, 'O', color=OX, fontsize=10.5, ha='center',
            va='center', fontweight='bold', zorder=3)
    if oh:
        ax.plot([top[0]+0.13, top[0]+0.23], [top[1]+0.46, top[1]+0.46],
                color=INK, lw=1.15, zorder=3)
        ax.text(top[0]+0.36, top[1]+0.46, 'H', color=INK, fontsize=8.8,
                ha='center', va='center', zorder=3)
    if ocharge:
        charge(top[0] + (0.50 if oh else 0.24), top[1]+0.62, ocharge, OX)
    if neg is not None:
        p = V[neg]; u = (p - C)/np.hypot(*(p - C))
        charge(p[0] + u[0]*0.27, p[1] + u[1]*0.27, '−', NEG)

def arrow(x, y):
    ax.annotate('', xy=(x+0.21, y), xytext=(x-0.21, y),
                arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=1.0,
                                mutation_scale=8))

KEK = [(0,1),(2,3),(4,5)]
XS = [0.78, 2.14, 3.50, 4.86]
Y1, Y2 = 1.70, -1.24

# row 1 : phenol
struct(XS[0], Y1, KEK, False, None, None, oh=True)
struct(XS[1], Y1, [(2,3),(4,5)], True, '+', 1, oh=True)
struct(XS[2], Y1, [(1,2),(4,5)], True, '+', 3, oh=True)
struct(XS[3], Y1, [(1,2),(3,4)], True, '+', 5, oh=True)
# row 2 : phenoxide
struct(XS[0], Y2, KEK, False, '−', None)
struct(XS[1], Y2, [(2,3),(4,5)], True, None, 1)
struct(XS[2], Y2, [(1,2),(4,5)], True, None, 3)
struct(XS[3], Y2, [(1,2),(3,4)], True, None, 5)
for x in [(XS[0]+XS[1])/2, (XS[1]+XS[2])/2, (XS[2]+XS[3])/2]:
    arrow(x, Y1); arrow(x, Y2)

ax.text(2.82, 3.18, 'PHENOL  —  oxygen becomes δ+,  so the O–H bond weakens',
        ha='center', va='center', fontsize=8.0, color=OX, fontweight='bold')
ax.text(2.82, 0.28,
        'PHENOXIDE ION  —  the charge is shared by C-2, C-4 and C-6',
        ha='center', va='center', fontsize=8.0, color=NEG, fontweight='bold')
ax.text(2.82, -2.44,
        'No such delocalisation is possible in CH₃CH₂O⁻, where the charge stays\n'
        'on one oxygen — so ethanol (pKa 15.9) is a far weaker acid than phenol (10.0).',
        ha='center', va='center', fontsize=7.0, color=MUTED, linespacing=1.45,
        bbox=dict(boxstyle='round,pad=0.40', fc='#fdf6ec', ec='#b8860b', lw=0.9))
ax.set_xlim(0.10, 5.54); ax.set_ylim(-2.90, 3.48)
fig.tight_layout()
```

**How strong is "acidic"?** Phenol is a much stronger acid than water or ethanol,
but much weaker than a carboxylic acid — and, decisively, weaker than carbonic
acid.

```figure caption="Acid strengths on the $\mathrm{p}K_a$ scale — the smaller the $\mathrm{p}K_a$, the stronger the acid. Phenol sits between water and carbonic acid, which is exactly why it dissolves in NaOH but gives no CO₂ with NaHCO₃."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.9))
names = ['ethanol\nC₂H₅OH', 'water\nH₂O', 'phenol\nC₆H₅OH',
         'carbonic acid\nH₂CO₃  (pKa₁)', 'acetic acid\nCH₃COOH']
pka   = [15.9, 15.7, 10.0, 6.35, 4.76]
cols  = ['#5b6472', '#5b6472', '#d9534f', '#2e8b57', '#2e8b57']
y = np.arange(len(names))
ax.barh(y, pka, color=cols, height=0.62, zorder=3)
for yi, v, t in zip(y, pka, ['15.9', '15.7', '10.0', '6.35', '4.76']):
    ax.text(v + 0.35, yi, t, va='center', fontsize=8.2, color=INK, zorder=4)
ax.set_yticks(y); ax.set_yticklabels(names, fontsize=7.4)
ax.invert_yaxis()
ax.set_xlabel('p$K_a$  at 25 °C        (smaller p$K_a$ = stronger acid)')
ax.set_xlim(0, 18.6)
ax.axvline(10.0, color='#d9534f', lw=0.9, ls=':', zorder=1)
ax.text(10.25, -0.62, 'phenol', fontsize=7.2, color='#d9534f', va='center')
ax.spines[['top','right','left']].set_visible(False)
ax.tick_params(axis='y', length=0)
ax.grid(True, axis='x', alpha=.45, zorder=0)
fig.tight_layout()
```

The consequences are examined every year:

| Reagent | Phenol | Ethanol | Carboxylic acid |
|---|---|---|---|
| Na metal | H₂ evolved | H₂ evolved | H₂ evolved |
| NaOH(aq) | **dissolves**, gives C₆H₅ONa | no reaction | dissolves |
| NaHCO₃(aq) | **no CO₂** | no reaction | **CO₂ effervescence** |
| Litmus | very faintly red | neutral | red |

So NaOH separates phenol from an alcohol, and NaHCO₃ separates a carboxylic acid
from phenol.

C₆H₅OH + NaOH → C₆H₅ONa + H₂O

**Effect of substituents.** Electron-withdrawing groups drain charge from the
phenoxide ion and strengthen the acid; electron-releasing groups weaken it:

picric acid (0.38) > *p*-nitrophenol (7.15) > phenol (10.0) > *p*-cresol (10.26)

::: example Worked example 11.1
**Problem.** The dissociation constant of phenol is $K_a = 1.0\times10^{-10}$ at
25 °C. Calculate the pH and the degree of ionisation of a 0.01 M aqueous
solution of phenol.

**Solution.** For a weak monobasic acid of concentration $C$,

$$ [\text{H}^{+}] = \sqrt{K_a\,C} $$

$$ [\text{H}^{+}] = \sqrt{(1.0\times10^{-10})(1.0\times10^{-2})}
 = \sqrt{1.0\times10^{-12}} = 1.0\times10^{-6}\ \text{mol dm}^{-3} $$

$$ \mathrm{pH} = -\log[\text{H}^{+}] = 6.0 $$

Degree of ionisation, by Ostwald's dilution law,

$$ \alpha = \sqrt{\frac{K_a}{C}} = \sqrt{\frac{1.0\times10^{-10}}{1.0\times10^{-2}}}
 = 1.0\times10^{-4} = 0.01\ \% $$

Only one molecule in ten thousand is ionised — phenol is acidic, but only just.
:::

::: example Worked example 11.2
**Problem.** Phenol dissolves completely in aqueous NaOH but gives no
effervescence with NaHCO₃. Justify this using
$K_a(\text{C}_6\text{H}_5\text{OH}) = 1.0\times10^{-10}$,
$K_{a1}(\text{H}_2\text{CO}_3) = 4.5\times10^{-7}$ and
$K_w = 1.0\times10^{-14}$.

**Solution.**

*With NaOH.* C₆H₅OH + OH⁻ ⇌ C₆H₅O⁻ + H₂O, for which

$$ K = \frac{K_a}{K_w} = \frac{1.0\times10^{-10}}{1.0\times10^{-14}} = 1.0\times10^{4} $$

$K \gg 1$, so the reaction goes essentially to completion and the phenol
dissolves as sodium phenoxide.

*With NaHCO₃.* C₆H₅OH + HCO₃⁻ ⇌ C₆H₅O⁻ + H₂CO₃, for which

$$ K = \frac{K_a(\text{C}_6\text{H}_5\text{OH})}{K_{a1}(\text{H}_2\text{CO}_3)}
 = \frac{1.0\times10^{-10}}{4.5\times10^{-7}} = 2.2\times10^{-4} $$

$K \ll 1$, so almost no reaction occurs: no H₂CO₃ is formed and therefore no CO₂
is released. Phenol is a **weaker acid than carbonic acid**, so it cannot
displace CO₂ from a bicarbonate — which is the standard way of telling phenol
from benzoic acid.
:::

## 11.5 Action with NH₃, Zn, Na, benzene diazonium chloride, phthalic anhydride

**(a) With ammonia** (replacement of –OH by –NH₂, over anhydrous ZnCl₂ at 300 °C):

C₆H₅OH + NH₃ --anhyd. ZnCl₂, 300 °C--> C₆H₅NH₂ + H₂O   (aniline)

**(b) With zinc dust** (reduction; removal of the oxygen):

C₆H₅OH + Zn --distil--> C₆H₆ + ZnO

**(c) With sodium metal** (the acidic O–H hydrogen is displaced):

2C₆H₅OH + 2Na → 2C₆H₅ONa + H₂↑

**(d) With benzene diazonium chloride** — a **coupling reaction** in cold
alkaline solution at 0–5 °C. The diazonium ion is a weak electrophile, so it can
attack only a strongly activated ring, and it goes to the **para** position:

C₆H₅N₂Cl + C₆H₅OH --NaOH(aq), 0–5 °C--> C₆H₅–N=N–C₆H₄–OH + HCl

The product, *p*-hydroxyazobenzene, is an **orange dye**; this is the basis of
the whole azo-dye industry.

**(e) With phthalic anhydride** (two molecules of phenol, conc. H₂SO₄, heat):

C₆H₄(CO)₂O + 2C₆H₅OH --conc. H₂SO₄--> phenolphthalein + H₂O

Phenolphthalein, C₂₀H₁₄O₄, is the familiar titration indicator: colourless in
acid, pink in alkali.

## 11.6 Acylation, Kolbe's reaction, Reimer-Tiemann reaction

**Acylation.** Phenol is a poor nucleophile, so an acid chloride or anhydride is
used, usually with a base (pyridine or NaOH) to mop up the acid formed:

C₆H₅OH + CH₃COCl → CH₃COOC₆H₅ + HCl   (phenyl ethanoate)

C₆H₅OH + (CH₃CO)₂O → CH₃COOC₆H₅ + CH₃COOH

Heating phenyl ethanoate with anhydrous AlCl₃ shifts the acetyl group onto the
ring itself, giving *o*- and *p*-hydroxyacetophenone — the **Fries
rearrangement**.

**Kolbe's reaction (Kolbe–Schmitt).** Dry sodium phenoxide absorbs carbon dioxide
under pressure. CO₂ is the electrophile and attacks the ortho position:

C₆H₅ONa + CO₂ --125 °C, 4–7 atm--> 2-(HO)C₆H₄COONa

2-(HO)C₆H₄COONa + HCl → 2-(HO)C₆H₄COOH + NaCl   (salicylic acid)

Salicylic acid is then acetylated to give **aspirin**:

2-(HO)C₆H₄COOH + (CH₃CO)₂O → 2-(CH₃COO)C₆H₄COOH + CH₃COOH

**Reimer–Tiemann reaction.** Phenol warmed with chloroform and aqueous NaOH at
60–70 °C, followed by acidification, gives **salicylaldehyde**
(2-hydroxybenzaldehyde). The true electrophile is **dichlorocarbene**, :CCl₂,
generated from chloroform by the alkali:

CHCl₃ + NaOH → :CCl₂ + NaCl + H₂O

C₆H₅OH + CHCl₃ + 3NaOH --60–70 °C--> 2-(HO)C₆H₄CHO + 3NaCl + 2H₂O

If carbon tetrachloride is used in place of chloroform the product is salicylic
acid instead:

C₆H₅OH + CCl₄ + 5NaOH → 2-(HO)C₆H₄COONa + 4NaCl + 3H₂O

::: caution Both Kolbe and Reimer–Tiemann need the phenoxide, not phenol
The attacking species (CO₂ or :CCl₂) is a **weak** electrophile. Only the
phenoxide ion, C₆H₅O⁻, is activated enough to react with it. That is why both
reactions are carried out in **alkali** — leave out the NaOH and nothing happens.
:::

## 11.7 Electrophilic substitution: nitration, sulphonation, bromination, Friedel-Crafts alkylation

Because the –OH group donates its lone pair into the ring, phenol is far more
reactive than benzene and substitution occurs at C-2, C-4 and C-6.

```figure caption="Why phenol substitutes at positions 2, 4 and 6. The oxygen lone pair is delocalised into the ring, building up negative charge on the two ortho carbons and the para carbon, so an electrophile E⁺ attacks there and never at C-3 or C-5."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
fig, ax = plt.subplots(figsize=(4.8,3.4))
ax.axis('off'); ax.set_aspect('equal')
OX = '#d9534f'; NEG = '#1d6fb8'
R = 1.02
ANG = np.radians(np.array([90.,150.,210.,270.,330.,30.]))
V = np.c_[R*np.cos(ANG), R*np.sin(ANG)]
for a, b in [(0,1),(1,2),(2,3),(3,4),(4,5),(5,0)]:
    ax.plot([V[a,0],V[b,0]], [V[a,1],V[b,1]], color=INK, lw=1.6,
            solid_capstyle='round', zorder=2)
ax.add_patch(plt.Circle((0,0), 0.50, fill=False, ec=INK, lw=1.2, zorder=2))
OY = V[0,1] + 0.52
ax.plot([0,0],[V[0,1]+0.04, V[0,1]+0.36], color=INK, lw=1.6, zorder=2)
ax.text(0, OY, 'O', color=OX, fontsize=12.0, ha='center', va='center',
        fontweight='bold', zorder=3)
ax.plot([0.15, 0.27],[OY, OY], color=INK, lw=1.4, zorder=2)
ax.text(0.41, OY, 'H', color=INK, fontsize=10.0, ha='center', va='center', zorder=3)
for dy in (0.11, -0.11):
    ax.plot([-0.25], [OY+dy], marker='o', ms=2.3, color=OX, zorder=3)
# two curved arrows: the lone pair delocalises towards both ortho carbons
for tgt, rad, x0 in [(1, 0.50, -0.34), (5, -0.50, 0.34)]:
    u = V[tgt]/np.hypot(*V[tgt])
    ax.add_patch(FancyArrowPatch((x0, OY-0.16),
                                 (V[tgt,0]+u[0]*0.20, V[tgt,1]+u[1]*0.20),
                                 connectionstyle=f'arc3,rad={rad}',
                                 arrowstyle='-|>', mutation_scale=10,
                                 color=OX, lw=1.1, ls=(0,(2.6,1.8)), zorder=4))
num = ['1', '2\northo', '3', '4\npara', '5', '6\northo']
for i, t in enumerate(num):
    u = V[i]/np.hypot(*V[i])
    if i == 0:
        ax.text(0.30, V[0,1]-0.16, t, fontsize=7.6, color=MUTED,
                ha='left', va='center')
    else:
        ax.text(V[i,0]+u[0]*0.36, V[i,1]+u[1]*0.36, t, fontsize=7.6,
                color=MUTED, ha='center', va='center', linespacing=1.35)
for i in (1, 3, 5):
    u = V[i]/np.hypot(*V[i])
    ax.text(u[0]*0.75, u[1]*0.75, 'δ−', color=NEG, fontsize=9.0,
            ha='center', va='center', fontweight='bold', zorder=4)
ax.annotate('E⁺ attacks the three\nδ− carbons: 2, 4 and 6',
            xy=(V[3,0]+0.04, V[3,1]-0.06), xytext=(2.28, -1.62),
            fontsize=7.6, color=NEG, ha='center', va='center', linespacing=1.45,
            arrowprops=dict(arrowstyle='-|>', color=NEG, lw=1.0, mutation_scale=9))
ax.text(-2.30, 1.42, '–OH is strongly\nactivating and\no,p-directing',
        fontsize=7.8, color=OX, ha='center', va='center', linespacing=1.5,
        bbox=dict(boxstyle='round,pad=0.38', fc='#fdeeee', ec=OX, lw=0.9))
ax.text(0.05, -2.30, 'C-3 and C-5 get no extra charge, so the meta product is not formed',
        fontsize=7.0, color=MUTED, ha='center', va='center')
ax.set_xlim(-3.45, 3.60); ax.set_ylim(-2.60, 2.30)
fig.tight_layout()
```

| Reaction | Reagent and conditions | Product |
|---|---|---|
| **Nitration** | 20 % dilute HNO₃, 25 °C | *o*-nitrophenol + *p*-nitrophenol |
| | conc. HNO₃ + conc. H₂SO₄ | 2,4,6-trinitrophenol (**picric acid**) |
| **Sulphonation** | conc. H₂SO₄, 25 °C | *o*-phenolsulphonic acid (mainly) |
| | conc. H₂SO₄, 100 °C | *p*-phenolsulphonic acid (mainly) |
| **Bromination** | Br₂ in CS₂ or CHCl₃, 0 °C | *p*-bromophenol (mainly) |
| | **bromine water**, excess | 2,4,6-tribromophenol, **white precipitate** |
| **Friedel–Crafts alkylation** | CH₃Cl, anhydrous AlCl₃ | *o*- and *p*-cresol |

The important equations are

C₆H₅OH + 3HNO₃ --conc. H₂SO₄--> C₆H₂(NO₂)₃OH + 3H₂O

C₆H₅OH + H₂SO₄ ⇌ HO–C₆H₄–SO₃H + H₂O

C₆H₅OH + 3Br₂ --water--> C₆H₂Br₃OH↓ + 3HBr

C₆H₅OH + CH₃Cl --anhyd. AlCl₃--> CH₃–C₆H₄–OH + HCl

The two nitrophenols are separated by **steam distillation**: only the ortho
isomer distils over, because its –OH and –NO₂ groups are close enough to form an
*intramolecular* hydrogen bond (chelation), leaving no O–H free to bond to
neighbouring molecules. The para isomer, whose groups are too far apart, forms
*intermolecular* hydrogen bonds instead, associates into larger units and stays
behind.

```figure caption="Separation of the nitrophenols by steam distillation. Intramolecular hydrogen bonding (chelation) in the ortho isomer leaves no O–H free to link one molecule to the next, so it is volatile; the para isomer is held together by intermolecular hydrogen bonds and stays behind."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(5.2,3.4))
OX = '#d9534f'; GRN = '#2e8b57'
ANG = np.radians(np.array([90.,150.,210.,270.,330.,30.]))
def ring(ax, cx, cy, r=0.60):
    V = np.c_[cx + r*np.cos(ANG), cy + r*np.sin(ANG)]
    for a, b in [(0,1),(1,2),(2,3),(3,4),(4,5),(5,0)]:
        ax.plot([V[a,0],V[b,0]], [V[a,1],V[b,1]], color=INK, lw=1.4,
                solid_capstyle='round')
    ax.add_patch(plt.Circle((cx,cy), r*0.56, fill=False, ec=INK, lw=1.1))
    return V

# ---- ortho : intramolecular ----
ax = axes[0]; ax.axis('off'); ax.set_aspect('equal')
V = ring(ax, 0.0, 0.0)
ax.plot([V[0,0], -0.12],[V[0,1]+0.02, V[0,1]+0.36], color=INK, lw=1.4)
ax.text(-0.22, V[0,1]+0.54, 'O', color=OX, fontsize=10.8, ha='center',
        va='center', fontweight='bold')
ax.plot([-0.08, 0.04],[V[0,1]+0.54, V[0,1]+0.54], color=INK, lw=1.3)
ax.text(0.17, V[0,1]+0.54, 'H', color=INK, fontsize=9.4, ha='center', va='center')
ax.plot([V[5,0], V[5,0]+0.34],[V[5,1]+0.02, V[5,1]+0.28], color=INK, lw=1.4)
NX, NY = V[5,0]+0.52, V[5,1]+0.42
ax.text(NX, NY, 'N', color=GRN, fontsize=10.8, ha='center', va='center',
        fontweight='bold')
for s in (-0.05, 0.05):
    ax.plot([NX+0.30+s, NX+0.52+s],[NY-0.10, NY-0.28], color=INK, lw=1.2)
ax.text(NX+0.70, NY-0.40, 'O', color=OX, fontsize=9.8, ha='center',
        va='center', fontweight='bold')
ax.plot([NX-0.10, NX-0.26],[NY+0.20, NY+0.44], color=INK, lw=1.3)
ax.text(NX-0.38, NY+0.60, 'O', color=OX, fontsize=9.8, ha='center',
        va='center', fontweight='bold')
ax.plot([0.33, NX-0.50],[V[0,1]+0.62, NY+0.54], color=OX, lw=1.4, ls=(0,(2.2,1.8)))
ax.set_title('2-nitrophenol  (ortho)', fontsize=8.6, color=INK, pad=4)
ax.text(0.28, -1.62,
        'INTRAmolecular H-bond\n(chelation, a 6-membered ring)\n'
        '→ no link to the next molecule\n→ volatile, steam-distils over',
        fontsize=7.2, color=OX, ha='center', va='center', linespacing=1.55)
ax.set_xlim(-1.55, 2.45); ax.set_ylim(-2.55, 2.10)

# ---- para : intermolecular ----
ax = axes[1]; ax.axis('off'); ax.set_aspect('equal')
for cy in (1.34, -1.62):
    V = ring(ax, 0.0, cy)
    ax.plot([V[0,0], -0.10],[V[0,1]+0.02, V[0,1]+0.34], color=INK, lw=1.4)
    ax.text(-0.20, V[0,1]+0.52, 'O', color=OX, fontsize=10.2, ha='center',
            va='center', fontweight='bold')
    ax.plot([-0.06, 0.06],[V[0,1]+0.52, V[0,1]+0.52], color=INK, lw=1.3)
    ax.text(0.20, V[0,1]+0.52, 'H', color=INK, fontsize=9.2, ha='center',
            va='center')
    ax.plot([V[3,0], V[3,0]],[V[3,1]-0.02, V[3,1]-0.30], color=INK, lw=1.4)
    ax.text(V[3,0], V[3,1]-0.50, 'NO₂', color=GRN, fontsize=9.4, ha='center',
            va='center', fontweight='bold')
# hydrogen bond: NO2 oxygen of the upper molecule to the O-H of the lower one
ax.plot([0.22, 0.22],[1.34-0.60-0.62, -1.62+0.60+0.66], color=OX, lw=1.4,
        ls=(0,(2.2,1.8)))
ax.text(0.0, 2.72, '⋮', fontsize=11, color=MUTED, ha='center', va='center')
ax.text(0.0, -3.06, '⋮', fontsize=11, color=MUTED, ha='center', va='center')
ax.set_title('4-nitrophenol  (para)', fontsize=8.6, color=INK, pad=4)
ax.text(2.30, -0.15, 'INTERmolecular\nH-bonds join the\nmolecules into\nchains\n'
        '→ associated,\n→ much less volatile',
        fontsize=7.2, color=OX, ha='center', va='center', linespacing=1.55)
ax.set_xlim(-1.35, 3.85); ax.set_ylim(-3.35, 3.05)
fig.tight_layout()
```

## 11.8 Test of phenol (FeCl₃ test, aqueous bromine test, Libermann test); uses

| Test | Reagent and conditions | Observation with phenol | With ethanol |
|---|---|---|---|
| **Ferric chloride test** | a few drops of **neutral** FeCl₃ | **violet / blue-violet** colour | no colour |
| **Aqueous bromine test** | excess bromine water | **white precipitate** of 2,4,6-tribromophenol; bromine decolourised | no reaction |
| **Libermann's nitroso test** | solid NaNO₂ + conc. H₂SO₄, warm; dilute with water; then excess NaOH | deep **blue-green** solution → **red** on dilution → **blue-green** again with excess alkali | negative |
| **NaOH solubility** | 10 % NaOH(aq) | **dissolves** as sodium phenoxide | does not react |
| **Phthalein test** | phthalic anhydride + conc. H₂SO₄, then NaOH | **pink** colour (phenolphthalein) | negative |

The ferric chloride colour comes from a violet complex ion:

6C₆H₅OH + FeCl₃ → [Fe(OC₆H₅)₆]³⁻ + 3Cl⁻ + 6H⁺

::: caution The FeCl₃ must be neutral
Ferric chloride solution is normally acidic through hydrolysis, and an acidic
solution suppresses the ionisation of phenol so the colour fails to develop. The
reagent is neutralised first. Also note that some phenols (for example
*p*-nitrophenol) give a weak or no colour, so a negative FeCl₃ test alone is not
proof that phenol is absent.
:::

**Uses of phenol**

- Manufacture of **bakelite** (phenol + methanal), the first synthetic plastic.
- **Antiseptics and disinfectants** — carbolic soap, and the cresols in Lysol and
  creosote used to preserve railway sleepers and electric poles.
- **Drugs**: salicylic acid → aspirin; also paracetamol and phenacetin; methyl
  salicylate is oil of wintergreen, used in pain balms.
- **Picric acid**, a yellow dye and a powerful explosive.
- **Azo dyes**, by coupling with diazonium salts.
- **Phenolphthalein**, the acid–base indicator used in NaOH titrations.
- Starting material for **nylon-6,6** (via cyclohexanol) and for epoxy resins.

::: example Worked example 11.3
**Problem.** 0.94 g of phenol is shaken with excess bromine water until
precipitation is complete. Calculate (a) the mass of 2,4,6-tribromophenol formed
and (b) the mass of bromine consumed. (C = 12, H = 1, O = 16, Br = 79.9)

**Solution.** C₆H₅OH + 3Br₂ → C₆H₂Br₃OH↓ + 3HBr

Molar mass of phenol $= 6(12) + 6(1) + 16 = 94\ \text{g mol}^{-1}$, so

$$ n(\text{phenol}) = \frac{0.94}{94} = 0.010\ \text{mol} $$

(a) 1 mol phenol gives 1 mol of tribromophenol, whose molar mass is

$$ M = 6(12) + 3(1) + 3(79.9) + 16 = 72 + 3 + 239.7 + 16 = 330.7\ \text{g mol}^{-1} $$

$$ m = 0.010 \times 330.7 = 3.31\ \text{g} $$

(b) 3 mol of Br₂ are needed per mol of phenol:

$$ n(\text{Br}_2) = 3 \times 0.010 = 0.030\ \text{mol}, \qquad
m = 0.030 \times 159.8 = 4.79\ \text{g} $$
:::

::: example Worked example 11.4
**Problem.** An organic compound **P**, C₇H₈O, is insoluble in water and in
NaHCO₃ but dissolves in NaOH. It gives a violet colour with neutral FeCl₃ and a
white precipitate with bromine water. On treatment with CHCl₃ and NaOH followed
by acidification it gives an aldehyde **Q**. Identify **P** and **Q**.

**Solution.**

*Step 1.* Soluble in NaOH but not NaHCO₃ ⇒ **P** is a phenol, not a carboxylic
acid (a carboxylic acid would give CO₂ with NaHCO₃).
*Step 2.* Violet with FeCl₃ and a white precipitate with Br₂ water confirm a
phenolic –OH on the ring.
*Step 3.* C₇H₈O = C₆H₄(CH₃)(OH), a **cresol**. Since the Reimer–Tiemann reaction
works, a free ortho position is needed; the standard NEB answer is
**4-methylphenol (*p*-cresol)**, which has both ortho positions free.
*Step 4.* Reimer–Tiemann puts a –CHO group ortho to the –OH:

CH₃C₆H₄OH + CHCl₃ + 3NaOH → 2-hydroxy-5-methylbenzaldehyde + 3NaCl + 2H₂O

So **P** is *p*-cresol and **Q** is 2-hydroxy-5-methylbenzaldehyde,
C₈H₈O₂ (molar mass 136).
:::

## Chapter summary

- A phenol has –OH bonded **directly to the ring**; benzyl alcohol has it on a
  side chain and behaves as a 1° alcohol.
- Preparations: chlorobenzene + NaOH at 300 °C/150 atm (Dow); warming
  C₆H₅N₂Cl with water; fusion of C₆H₅SO₃Na with NaOH. Every route ends in
  sodium phenoxide and must be **acidified**.
- Phenol is a colourless solid, m.p. 41 °C, sparingly soluble in water, corrosive,
  and turns pink in air.
- Acidity: $K_a = 1.0\times10^{-10}$, $\mathrm{p}K_a = 10.0$ — stronger than water
  (15.7) and ethanol (15.9) but weaker than carbonic acid (6.35). Hence it
  **dissolves in NaOH but gives no CO₂ with NaHCO₃**. The cause is resonance
  stabilisation of the phenoxide ion over C-2, C-4 and C-6.
- With NH₃ over ZnCl₂ at 300 °C → aniline; with Zn dust → benzene; with Na → sodium
  phenoxide + H₂; with C₆H₅N₂Cl in cold alkali → *p*-hydroxyazobenzene (orange
  dye); with phthalic anhydride → phenolphthalein.
- Kolbe: C₆H₅ONa + CO₂ at 125 °C/4–7 atm → sodium salicylate → salicylic acid →
  aspirin. Reimer–Tiemann: CHCl₃ + NaOH (via :CCl₂) → salicylaldehyde; CCl₄
  gives salicylic acid.
- Electrophilic substitution is fast and **o,p-directed**: dilute HNO₃ → o- and
  p-nitrophenol (separated by steam distillation, ortho is chelated); conc.
  HNO₃/H₂SO₄ → picric acid; bromine water → white 2,4,6-tribromophenol.
- Tests: **violet** with neutral FeCl₃; **white precipitate** with bromine water;
  Libermann's test gives blue-green → red on dilution → blue-green with alkali.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Phenol dissolves in aqueous NaOH but not in aqueous NaHCO₃ because <span class="marks">[1]</span>
   (a) it is a stronger acid than carbonic acid (b) it is a weaker acid than
   carbonic acid (c) it is not acidic at all (d) it is insoluble in water
2. The white precipitate formed when phenol is shaken with excess bromine water is <span class="marks">[1]</span>
   (a) *p*-bromophenol (b) *o*-bromophenol (c) 2,4,6-tribromophenol (d) bromobenzene
3. Sodium phenoxide heated with CO₂ at 125 °C and 4–7 atm gives, after
   acidification, <span class="marks">[1]</span>
   (a) benzoic acid (b) salicylic acid (c) salicylaldehyde (d) picric acid
4. The electrophile in the Reimer–Tiemann reaction is <span class="marks">[1]</span>
   (a) CHCl₃ (b) CCl₃⁻ (c) :CCl₂ (d) Cl⁺
5. Which one gives a violet colour with neutral ferric chloride? <span class="marks">[1]</span>
   (a) ethanol (b) benzyl alcohol (c) phenol (d) chlorobenzene
6. Phenol is *more* acidic than ethanol mainly because <span class="marks">[1]</span>
   (a) it is a solid (b) the phenoxide ion is resonance stabilised
   (c) it contains a benzene ring (d) it has a higher molar mass

::: note Answers to Group A
**1.** (b) — with $\mathrm{p}K_a$ 10.0 against 6.35, phenol cannot displace CO₂ from a bicarbonate.
**2.** (c) — in water all three activated positions (2, 4 and 6) are brominated.
**3.** (b) — Kolbe–Schmitt reaction; CO₂ attacks the ortho position.
**4.** (c) — dichlorocarbene, generated from CHCl₃ by the alkali.
**5.** (c) — only a phenolic –OH forms the violet iron(III) complex.
**6.** (b) — the negative charge is delocalised over C-2, C-4 and C-6, which is impossible in an alkoxide ion.
:::

**Group B — Short answer (5 marks each)**

1. Explain, with resonance structures, why phenol is a stronger acid than ethanol
   but a weaker acid than acetic acid. <span class="marks">[5]</span>
2. How is phenol prepared from (a) chlorobenzene, (b) benzene diazonium chloride
   and (c) benzene sulphonic acid? Give equations and conditions. <span class="marks">[5]</span>
3. What is the Reimer–Tiemann reaction? Give the mechanism outline, the equation
   and the product obtained when CCl₄ is used in place of CHCl₃. <span class="marks">[5]</span>
4. How would you distinguish between phenol, ethanol and benzoic acid using
   simple chemical tests? <span class="marks">[5]</span>
5. Calculate the pH of a 0.001 M solution of phenol,
   $K_a = 1.0\times10^{-10}$, and state whether the solution would turn blue
   litmus red. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** In the phenoxide ion the negative charge is delocalised over the oxygen and
the two ortho and one para carbons (four contributing structures), so the
conjugate base is stabilised and the proton is lost more easily. In an ethoxide
ion the charge stays on one oxygen and the +I effect of the ethyl group
intensifies it, so ethanol ($\mathrm{p}K_a$ 15.9) is a much weaker acid. In the
acetate ion, however, the charge is shared **equally by two electronegative
oxygen atoms**, which is far more effective than spreading it onto carbon atoms —
so acetic acid ($\mathrm{p}K_a$ 4.76) is stronger than phenol (10.0).

**2.** (a) C₆H₅Cl + 2NaOH --300 °C, 150 atm--> C₆H₅ONa + NaCl + H₂O, then
C₆H₅ONa + HCl → C₆H₅OH + NaCl (Dow's process).
(b) C₆H₅N₂Cl + H₂O --warm above 5 °C--> C₆H₅OH + N₂↑ + HCl.
(c) C₆H₅SO₃Na + 2NaOH --fuse 300–350 °C--> C₆H₅ONa + Na₂SO₃ + H₂O, then acidify.

**3.** Phenol + CHCl₃ + aqueous NaOH at 60–70 °C, then acidification, gives
salicylaldehyde. The alkali removes a proton from chloroform to give CCl₃⁻ which
loses Cl⁻ to form **dichlorocarbene :CCl₂**, the electrophile. It attacks the
ortho position of the phenoxide ion; hydrolysis of the resulting –CHCl₂ group
gives –CHO. Overall:
C₆H₅OH + CHCl₃ + 3NaOH → 2-(HO)C₆H₄CHO + 3NaCl + 2H₂O.
With CCl₄ the product is salicylic acid:
C₆H₅OH + CCl₄ + 5NaOH → 2-(HO)C₆H₄COONa + 4NaCl + 3H₂O.

**4.** Add NaHCO₃ solution: only **benzoic acid** gives CO₂ effervescence. To the
remaining two add neutral FeCl₃: **phenol** gives a violet colour, ethanol none.
Confirm with bromine water (phenol → white precipitate) and with the iodoform
test (ethanol → yellow CHI₃).

**5.** $[\text{H}^{+}] = \sqrt{K_aC} = \sqrt{(1.0\times10^{-10})(1.0\times10^{-3})}
= \sqrt{1.0\times10^{-13}} = 3.16\times10^{-7}\ \text{mol dm}^{-3}$.
$\mathrm{pH} = -\log(3.16\times10^{-7}) = 6.5$. The solution is only very slightly
acidic — litmus (which changes around pH 5–8) would show at most a very faint
pink, so in practice phenol does **not** turn blue litmus properly red.
:::

**Group C — Long answer (8 marks each)**

1. (a) Account for the acidic character of phenol and compare it with that of
   water and ethanol, using resonance structures. <span class="marks">[4]</span>
   (b) Give equations for the action of phenol with ammonia, zinc dust, sodium
   metal, benzene diazonium chloride and phthalic anhydride. <span class="marks">[4]</span>
2. (a) Why is phenol more reactive than benzene towards electrophilic
   substitution, and why does substitution occur at the ortho and para
   positions? <span class="marks">[3]</span>
   (b) Write equations for the nitration, sulphonation, bromination and
   Friedel–Crafts alkylation of phenol, stating the conditions. <span class="marks">[3]</span>
   (c) 9.4 g of phenol is nitrated completely with excess conc. HNO₃/H₂SO₄.
   Calculate the mass of picric acid obtained if the yield is 70 %. <span class="marks">[2]</span>

::: note Answers to Group C
**1. (a)** Phenol ionises as C₆H₅OH ⇌ C₆H₅O⁻ + H⁺. The phenoxide ion has four
resonance structures spreading the negative charge onto C-2, C-4 and C-6, so it
is far more stable than the hydroxide or ethoxide ion in which the charge is
localised on one oxygen. In phenol itself the oxygen lone pair is delocalised
into the ring, leaving oxygen δ+ and weakening the O–H bond. Hence acidity runs
phenol (10.0) > water (15.7) > ethanol (15.9); the +I effect of the alkyl group
makes ethanol the weakest of the three.
**(b)** C₆H₅OH + NH₃ --ZnCl₂, 300 °C--> C₆H₅NH₂ + H₂O;
C₆H₅OH + Zn --distil--> C₆H₆ + ZnO;
2C₆H₅OH + 2Na → 2C₆H₅ONa + H₂↑;
C₆H₅N₂Cl + C₆H₅OH --NaOH, 0–5 °C--> C₆H₅N=N–C₆H₄–OH + HCl;
C₆H₄(CO)₂O + 2C₆H₅OH --conc. H₂SO₄--> phenolphthalein + H₂O.

**2. (a)** The oxygen lone pair is delocalised into the ring, so the ring carries
more electron density than benzene and attracts electrophiles more strongly
(–OH is strongly activating). The delocalisation places the extra negative charge
specifically on C-2, C-4 and C-6, so the electrophile attacks there; the
intermediate carbocation formed at those positions is also the only one that can
be stabilised by a structure in which every atom has a complete octet.
**(b)** C₆H₅OH + HNO₃(dil., 25 °C) → o- and p-O₂NC₆H₄OH + H₂O;
C₆H₅OH + 3HNO₃ --conc. H₂SO₄--> C₆H₂(NO₂)₃OH + 3H₂O;
C₆H₅OH + H₂SO₄ ⇌ HOC₆H₄SO₃H + H₂O (ortho at 25 °C, para at 100 °C);
C₆H₅OH + 3Br₂ (water) → C₆H₂Br₃OH↓ + 3HBr;
C₆H₅OH + CH₃Cl --anhyd. AlCl₃--> CH₃C₆H₄OH + HCl.
**(c)** $n(\text{phenol}) = 9.4/94 = 0.10\ \text{mol}$. One mole of phenol gives
one mole of picric acid, C₆H₂(NO₂)₃OH, of molar mass
$72 + 3 + 3(46) + 16 = 229\ \text{g mol}^{-1}$. Theoretical mass
$= 0.10 \times 229 = 22.9\ \text{g}$; at 70 % yield,
$m = 0.70 \times 22.9 = 16.0\ \text{g}$.
:::
