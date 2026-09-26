---
subject: Chemistry
grade: 12
unit: 12
title: Ethers
hours: 2
area: Organic Chemistry
---

An ether is an oxygen atom with an alkyl or aryl group on each side, R–O–R′. The
same formula CₙH₂ₙ₊₂O also belongs to the alcohols, so every ether is a
functional isomer of an alcohol — yet the two behave nothing alike. An ether has
no O–H bond, so it cannot hydrogen-bond to itself, cannot react with sodium and
is chemically very unreactive. That inertness is exactly why ethoxyethane became
the chemist's favourite solvent and the first surgical anaesthetic.

::: key A two-hour unit with three sure marks
Expect (i) **Williamson's synthesis**, including why it must be planned the right
way round; (ii) why an ether boils about 80 °C **below** its isomeric alcohol;
and (iii) the action of **HI** on ethoxyethane and on anisole. Everything else
in this unit is supporting detail.
:::

## 12.1 Introduction; nomenclature, classification and isomerism

The general formula of a saturated ether is **CₙH₂ₙ₊₂O**, the same as that of a
saturated monohydric alcohol. Ethers fall into two classes:

- **Simple (symmetrical) ethers**, R–O–R, with the same group on both sides —
  ethoxyethane, C₂H₅OC₂H₅.
- **Mixed (unsymmetrical) ethers**, R–O–R′ — methoxyethane, CH₃OC₂H₅; and
  methoxybenzene, C₆H₅OCH₃, which is an aromatic mixed ether.

**Nomenclature.** In the IUPAC system the **smaller** group plus the oxygen is
named as an **alkoxy** substituent on the larger parent chain: *alkoxyalkane*.
The common system simply names both groups followed by the word *ether*.

| Structure | IUPAC name | Common name |
|---|---|---|
| CH₃OCH₃ | methoxymethane | dimethyl ether |
| CH₃OC₂H₅ | methoxyethane | ethyl methyl ether |
| C₂H₅OC₂H₅ | ethoxyethane | diethyl ether ("ether") |
| CH₃OCH₂CH₂CH₃ | 1-methoxypropane | methyl *n*-propyl ether |
| CH₃OCH(CH₃)₂ | 2-methoxypropane | methyl isopropyl ether |
| (CH₃)₃COCH₃ | 2-methoxy-2-methylpropane | MTBE, *tert*-butyl methyl ether |
| C₆H₅OCH₃ | methoxybenzene | anisole |
| C₆H₅OC₆H₅ | phenoxybenzene | diphenyl ether |

**Isomerism.** Ethers show three kinds:

- **Metamerism** — the same formula, the same functional group, but a different
  *distribution of carbon atoms* on the two sides of the oxygen. C₄H₁₀O gives
  CH₃–O–C₃H₇ and C₂H₅–O–C₂H₅; these are metamers.
- **Chain isomerism** — within one alkyl group: 1-methoxypropane and
  2-methoxypropane.
- **Functional isomerism** — with the alcohols. C₂H₆O is either ethanol or
  methoxymethane; C₄H₁₀O has **four alcohols and three ethers**, seven isomers
  in all.

## 12.2 Preparation of aliphatic and aromatic ethers by Williamson's synthesis

Williamson's synthesis is the general method: a **sodium alkoxide or phenoxide**
(the nucleophile) is warmed with a **haloalkane** in dry conditions.

C₂H₅ONa + C₂H₅I → C₂H₅OC₂H₅ + NaI

C₆H₅ONa + CH₃I → C₆H₅OCH₃ + NaI   (anisole)

The mechanism is **SN₂**: the alkoxide oxygen attacks the carbon carrying the
halogen from the side opposite to it, and the halide leaves at the same moment.
That single fact decides how the reaction must be planned.

```figure caption="Williamson's synthesis. The alkoxide oxygen attacks the back of the carbon that carries the halogen, so the halide must be methyl or primary. Choosing the wrong partner gives an alkene or nothing at all."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
fig, axes = plt.subplots(3, 1, figsize=(5.2,3.4))
GRN = '#2e8b57'; RED = '#d9534f'
ANG = np.radians(np.array([90.,150.,210.,270.,330.,30.]))

def setup(ax):
    ax.axis('off'); ax.set_aspect('equal')
    ax.set_xlim(0, 10.6); ax.set_ylim(0, 2.0)

def arrow(ax, x1, x2, y, top, bot):
    ax.annotate('', xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.2,
                                mutation_scale=11))
    ax.text((x1+x2)/2, y+0.26, top, ha='center', va='center', fontsize=6.6,
            color=MUTED)
    ax.text((x1+x2)/2, y-0.28, bot, ha='center', va='center', fontsize=6.6,
            color=MUTED)

def ring(ax, cx, cy, r=0.40):
    V = np.c_[cx + r*np.cos(ANG), cy + r*np.sin(ANG)]
    for a, b in [(0,1),(1,2),(2,3),(3,4),(4,5),(5,0)]:
        ax.plot([V[a,0],V[b,0]], [V[a,1],V[b,1]], color=INK, lw=1.2,
                solid_capstyle='round')
    ax.add_patch(plt.Circle((cx,cy), r*0.56, fill=False, ec=INK, lw=1.0))
    return V

# ---------- panel 1 : aliphatic ----------
ax = axes[0]; setup(ax)
ax.text(0.10, 1.66, 'aliphatic ether', fontsize=7.4, color=ACCENT,
        fontweight='bold', va='center')
ax.text(1.20, 1.02, 'CH₃CH₂—O⁻ Na⁺', fontsize=9.4, color=ACCENT, ha='center',
        va='center')
ax.text(2.72, 1.02, '+', fontsize=9.4, color=INK, ha='center', va='center')
ax.text(4.00, 1.02, 'CH₃CH₂—I', fontsize=9.4, color=INK, ha='center', va='center')
arrow(ax, 5.10, 6.30, 1.02, 'dry, warm', '− NaI')
ax.text(8.30, 1.02, 'CH₃CH₂—O—CH₂CH₃', fontsize=9.4, color=GRN, ha='center',
        va='center')
ax.add_patch(FancyArrowPatch((1.58, 0.74), (4.05, 0.74),
                             connectionstyle='arc3,rad=0.40',
                             arrowstyle='-|>', mutation_scale=9, color=ACCENT,
                             lw=1.1, ls=(0,(2.4,1.8))))
ax.text(4.30, 0.18, 'the O⁻ attacks the back of the C—I carbon   (SN₂)',
        fontsize=6.8, color=ACCENT, ha='left', va='center')

# ---------- panel 2 : aromatic ----------
ax = axes[1]; setup(ax)
ax.text(0.10, 1.70, 'aromatic ether', fontsize=7.4, color=ACCENT,
        fontweight='bold', va='center')
V = ring(ax, 1.05, 1.00)
ax.plot([V[5,0], V[5,0]+0.30], [V[5,1], V[5,1]+0.18], color=INK, lw=1.2)
ax.text(1.98, 1.26, 'O⁻ Na⁺', fontsize=8.8, color=ACCENT, ha='left', va='center')
ax.text(3.28, 1.00, '+', fontsize=9.4, color=INK, ha='center', va='center')
ax.text(4.25, 1.00, 'CH₃—I', fontsize=9.4, color=INK, ha='center', va='center')
arrow(ax, 5.15, 6.35, 1.00, 'dry, warm', '− NaI')
V2 = ring(ax, 7.25, 1.00)
ax.plot([V2[5,0], V2[5,0]+0.30], [V2[5,1], V2[5,1]+0.18], color=INK, lw=1.2)
ax.text(8.15, 1.26, 'O—CH₃', fontsize=8.8, color=GRN, ha='left', va='center')
ax.text(8.75, 0.42, 'anisole', fontsize=7.0, color=GRN, ha='center', va='center')
ax.text(1.30, 0.28, 'the RING supplies the alkoxide, never the halide',
        fontsize=6.6, color=MUTED, ha='left', va='center')

# ---------- panel 3 : the two wrong pairings ----------
ax = axes[2]; setup(ax)
ax.text(0.10, 1.78, 'planned the wrong way round', fontsize=7.4, color=RED,
        fontweight='bold', va='center')
def cross(x, y):
    ax.plot([x-0.15, x+0.15], [y-0.15, y+0.15], color=RED, lw=1.6)
    ax.plot([x-0.15, x+0.15], [y+0.15, y-0.15], color=RED, lw=1.6)
ax.text(0.10, 1.12, 'CH₃O⁻ Na⁺  +  C₆H₅—Cl', fontsize=8.4, color=INK,
        ha='left', va='center')
ax.annotate('', xy=(5.30, 1.12), xytext=(4.45, 1.12),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.1,
                            mutation_scale=10))
cross(4.88, 1.12)
ax.text(5.62, 1.12, 'no reaction: haloarenes do not do SN₂',
        fontsize=6.8, color=RED, ha='left', va='center')
ax.text(0.10, 0.42, 'CH₃O⁻ Na⁺  +  (CH₃)₃C—Br', fontsize=8.4, color=INK,
        ha='left', va='center')
ax.annotate('', xy=(5.30, 0.42), xytext=(4.45, 0.42),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.1,
                            mutation_scale=10))
cross(4.88, 0.42)
ax.text(5.62, 0.42, 'E2 elimination gives (CH₃)₂C=CH₂, not an ether',
        fontsize=6.8, color=RED, ha='left', va='center')
fig.tight_layout()
```

::: caution Which partner is which?
For a mixed ether there are always two ways of splitting it, and only one of them
works. Always make the **bulky** group the alkoxide and the **methyl or primary**
group the halide. To prepare 2-methoxy-2-methylpropane, use
(CH₃)₃CONa + CH₃I — **not** CH₃ONa + (CH₃)₃CBr, which would give
2-methylpropene by elimination. For anisole, use C₆H₅ONa + CH₃I — **not**
CH₃ONa + C₆H₅Cl, because the C–Cl bond of a haloarene has partial double-bond
character and is inert to SN₂.
:::

Ethers can also be made by the **dehydration of alcohols**, as in Unit 10:

2C₂H₅OH --conc. H₂SO₄, 140 °C--> C₂H₅OC₂H₅ + H₂O

This is cheap and is used industrially, but it works only for **simple** ethers —
a mixture of two alcohols would give all three possible products.

## 12.3 Physical properties

- Methoxymethane and methoxyethane are gases at room temperature; the rest of the
  lower ethers are **colourless, volatile, very inflammable liquids** with a
  sweet smell.
- Ethoxyethane boils at **34.6 °C** and has density 0.713 g cm⁻³ and dipole
  moment 1.15 D. The C–O–C angle is **111.7°** — wider than the 104.5° of water,
  because the two bulky ethyl groups repel each other.
- The boiling point is **far below that of the isomeric alcohol** (ethoxyethane
  34.6 °C against butan-1-ol 117.7 °C) because an ether has no O–H hydrogen and
  so cannot hydrogen-bond to another ether molecule. It boils at almost exactly
  the temperature of pentane (36.1 °C), the alkane of similar mass.
- Yet ethers are **as soluble in water as the alcohols** (6.5 g per 100 cm³,
  against 7.9 g for butan-1-ol), because the oxygen still has lone pairs and can
  *accept* a hydrogen bond from a water molecule even though it cannot donate one.
- The vapour is much denser than air, spreads along the bench and forms explosive
  mixtures — never use a naked flame near ether.

```figure caption="Ethoxyethane is a bent, polar molecule. The oxygen is sp³ hybridised with two lone pairs; the bulky ethyl groups open the C–O–C angle to 111.7°, wider than the H–O–H angle of water."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Arc
fig, ax = plt.subplots(figsize=(5.0,2.4))
ax.axis('off'); ax.set_aspect('equal')
OX = '#d9534f'
th = np.radians(111.7/2.0)
L = 0.95
C1 = np.array([-L*np.sin(th), -L*np.cos(th)])
C2 = np.array([ L*np.sin(th), -L*np.cos(th)])
for C in (C1, C2):
    u = C/np.hypot(*C)
    ax.plot([u[0]*0.20, C[0]-u[0]*0.22], [u[1]*0.20, C[1]-u[1]*0.22],
            color=INK, lw=1.7, solid_capstyle='round')
ax.text(0, 0, 'O', color=OX, fontsize=13.0, ha='center', va='center',
        fontweight='bold')
ax.text(C1[0]-0.06, C1[1]-0.12, 'CH₂', color=INK, fontsize=9.4, ha='center',
        va='center')
ax.text(C2[0]+0.06, C2[1]-0.12, 'CH₂', color=INK, fontsize=9.4, ha='center',
        va='center')
E1 = C1 + np.array([-0.78, 0.36]); E2 = C2 + np.array([0.78, 0.36])
ax.plot([C1[0]-0.26, E1[0]+0.20], [C1[1]+0.06, E1[1]-0.06], color=INK, lw=1.7,
        solid_capstyle='round')
ax.plot([C2[0]+0.26, E2[0]-0.20], [C2[1]+0.06, E2[1]-0.06], color=INK, lw=1.7,
        solid_capstyle='round')
ax.text(E1[0]-0.16, E1[1]+0.06, 'CH₃', color=INK, fontsize=9.4, ha='center',
        va='center')
ax.text(E2[0]+0.16, E2[1]+0.06, 'CH₃', color=INK, fontsize=9.4, ha='center',
        va='center')
for dx in (-0.15, 0.15):
    ax.plot([dx-0.05, dx+0.05], [0.34, 0.34], color=OX, lw=0, marker='o', ms=2.4)
ax.text(0.0, 0.60, 'two lone pairs', color=OX, fontsize=7.2, ha='center',
        va='center')
ax.add_patch(Arc((0,0), 0.98, 0.98, angle=0,
                 theta1=270-111.7/2, theta2=270+111.7/2, color=MUTED, lw=1.0))
ax.text(0.0, -0.76, '111.7°', color=MUTED, fontsize=8.0, ha='center', va='center')
ax.annotate('', xy=(2.15, 0.30), xytext=(2.15, -0.42),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.3,
                            mutation_scale=10))
ax.text(2.32, -0.06, 'net dipole\nμ = 1.15 D', color=ACCENT, fontsize=7.2,
        ha='left', va='center', linespacing=1.45)
ax.text(0.30, -1.32,
        'H—O—H   104.5°          CH₃—O—H   108.5°          '
        'C₂H₅—O—C₂H₅   111.7°\nthe bulkier the groups, the wider the angle',
        color=INK, fontsize=7.2, ha='center', va='center', linespacing=2.0,
        bbox=dict(boxstyle='round,pad=0.42', fc='#f4f8fb', ec=GRID, lw=0.9))
ax.set_xlim(-2.95, 4.35); ax.set_ylim(-1.98, 1.02)
fig.tight_layout()
```

```figure caption="The seven isomers of C₄H₁₀O. The four alcohols can hydrogen-bond to each other and boil high; the three ethers cannot, and boil close to pentane, the alkane of almost the same molar mass."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,3.0))
names = ['butan-1-ol', '2-methylpropan-1-ol', 'butan-2-ol',
         '2-methylpropan-2-ol', '1-methoxypropane', 'ethoxyethane',
         '2-methoxypropane']
bp    = [117.7, 107.9, 99.5, 82.4, 38.8, 34.6, 30.8]
kind  = ['alcohol']*4 + ['ether']*3
cols  = [ACCENT if k == 'alcohol' else '#2e8b57' for k in kind]
y = np.arange(len(names))
ax.barh(y, bp, color=cols, height=0.66, zorder=3)
for yi, v in zip(y, bp):
    off = 2.0 if v > 60 else 7.0
    ax.text(v + off, yi, f'{v:.1f}', va='center', fontsize=7.6, color=INK,
            zorder=6,
            bbox=dict(fc='white', ec='none', pad=0.9) if v < 60 else None)
ax.set_yticks(y); ax.set_yticklabels(names, fontsize=7.6)
ax.invert_yaxis()
ax.axvline(36.1, color='#b8860b', lw=1.1, ls='--', zorder=5)
ax.text(37.6, 6.45, 'pentane  36.1 °C', fontsize=7.0, color='#b8860b',
        va='center')
ax.text(122, 1.5, 'hydrogen\nbonded', fontsize=7.4, color=ACCENT, va='center',
        ha='left', linespacing=1.4)
ax.text(122, 5.0, 'no O—H:\nno hydrogen\nbonding', fontsize=7.4, color='#2e8b57',
        va='center', ha='left', linespacing=1.4)
ax.set_xlabel('boiling point  (°C)')
ax.set_xlim(0, 152)
ax.spines[['top','right','left']].set_visible(False)
ax.tick_params(axis='y', length=0)
ax.grid(True, axis='x', alpha=.45, zorder=0)
fig.tight_layout()
```

## 12.4 Chemical properties of ethoxyethane: action with HI, conc. HCl, conc. H₂SO₄, air and Cl₂

Ethers are remarkably unreactive: they are not attacked by alkalis, by sodium
metal or by ordinary oxidising and reducing agents. The oxygen lone pairs do,
however, make an ether a weak **Lewis base**, and that is where most of its
chemistry starts. The oxygen is first protonated (or coordinated), and the C–O
bond is then broken by the nucleophile.

**(a) With hydrogen iodide.** The amount and temperature decide the product:

C₂H₅OC₂H₅ + HI (cold) → C₂H₅OH + C₂H₅I

C₂H₅OC₂H₅ + 2HI (hot, excess) → 2C₂H₅I + H₂O

Reactivity of the halogen acids is HI > HBr > HCl, following the nucleophilic
strength of the halide ion. With an **aromatic** ether the iodide can attack only
the sp³ carbon of the alkyl group, so the aryl–oxygen bond survives:

C₆H₅OCH₃ + HI → C₆H₅OH + CH₃I

**(b) With concentrated HCl.** In the cold the ether merely dissolves, forming an
**oxonium salt** — the clearest demonstration of its basic character:

C₂H₅OC₂H₅ + HCl (cold, conc.) → [(C₂H₅)₂OH]⁺Cl⁻

Heated under pressure the C–O bonds are broken:

C₂H₅OC₂H₅ + 2HCl --heat, pressure--> 2C₂H₅Cl + H₂O

**(c) With concentrated H₂SO₄.** Again, cold gives the oxonium salt; hot gives
cleavage to ethyl hydrogen sulphate:

C₂H₅OC₂H₅ + H₂SO₄ (cold) → [(C₂H₅)₂OH]⁺HSO₄⁻

C₂H₅OC₂H₅ + 2H₂SO₄ --heat--> 2C₂H₅HSO₄ + H₂O

**(d) With air — peroxide formation.** On long standing in air and light, ether
slowly takes up oxygen at the carbon next to the oxygen:

C₂H₅OC₂H₅ + O₂ --air, light, slow--> CH₃CH(OOH)OC₂H₅

The peroxide is non-volatile, so it concentrates in the flask when ether is
distilled and **explodes** near dryness. Peroxides are detected by shaking with
acidified KI solution (iodine is liberated, giving a blue colour with starch) or
with FeSO₄ and KSCN (blood-red). They are prevented by storing ether in dark
bottles over a piece of sodium wire or reduced iron, and by never distilling
ether to dryness.

**(e) With chlorine.** Substitution of the α-hydrogens, and the extent depends on
the light:

C₂H₅OC₂H₅ + 2Cl₂ --in the dark--> CH₃CHCl–O–CHClCH₃ + 2HCl

C₂H₅OC₂H₅ + 10Cl₂ --bright sunlight--> C₂Cl₅OC₂Cl₅ + 10HCl

::: caution Anisole plus HI gives phenol, never iodobenzene
Cleavage of an ether by HI always breaks the bond to the carbon that can accept a
backside SN₂ attack. In anisole only the methyl carbon is sp³ hybridised, so the
products are **phenol and iodomethane**. Writing "iodobenzene and methanol" is
the standard error here.
:::

## 12.5 Uses

- **Solvent.** Ethoxyethane dissolves fats, oils, waxes, resins, gums,
  nitrocellulose and alkaloids, and is used for extracting organic compounds from
  aqueous solutions ("ether extraction") because it is inert and boils off easily.
- **Grignard reagents** are prepared and used in dry ether; the ether oxygen
  donates its lone pairs to the magnesium and keeps R–Mg–X in solution.
- **Anaesthetic.** Ethoxyethane was the first general anaesthetic (1846) and is
  still listed as an essential medicine, though its flammability means safer
  agents are now preferred.
- **Refrigerant** and as a starting fluid for diesel engines in cold weather.
- **Smokeless powder** (cordite) is made using an ether–alcohol mixture.
- **MTBE**, 2-methoxy-2-methylpropane, is blended into petrol as a lead-free
  anti-knock agent in place of tetraethyl lead.

::: example Worked example 12.1
**Problem.** Write the structures and IUPAC names of all the isomeric **ethers**
of molecular formula C₅H₁₂O, and state which pairs are metamers.

**Solution.** The oxygen must carry five carbons in total, split between the two
sides as 1 + 4 or 2 + 3.

*Split 1 + 4 — methoxybutanes* (CH₃–O–C₄H₉); the butyl group has four
arrangements:

1. CH₃OCH₂CH₂CH₂CH₃ — 1-methoxybutane
2. CH₃OCH(CH₃)CH₂CH₃ — 2-methoxybutane
3. CH₃OCH₂CH(CH₃)₂ — 1-methoxy-2-methylpropane
4. CH₃OC(CH₃)₃ — 2-methoxy-2-methylpropane

*Split 2 + 3 — ethoxypropanes* (C₂H₅–O–C₃H₇):

5. C₂H₅OCH₂CH₂CH₃ — 1-ethoxypropane
6. C₂H₅OCH(CH₃)₂ — 2-ethoxypropane

There are therefore **six** isomeric ethers. Any methoxybutane paired with any
ethoxypropane is a pair of **metamers**, because the carbon atoms are distributed
differently about the oxygen (1 + 4 against 2 + 3). Within each group — for
example 1-methoxybutane and 2-methoxybutane — the isomerism is **chain** or
**position** isomerism, not metamerism.
:::

::: example Worked example 12.2
**Problem.** 6.8 g of sodium ethoxide is warmed with excess iodoethane.
Calculate the mass and the volume of ethoxyethane obtained if the yield is 75 %.
(Density of ethoxyethane = 0.713 g cm⁻³; Na = 23, C = 12, H = 1, O = 16)

**Solution.** C₂H₅ONa + C₂H₅I → C₂H₅OC₂H₅ + NaI

Molar mass of C₂H₅ONa $= 24 + 5 + 16 + 23 = 68\ \text{g mol}^{-1}$, so

$$ n(\text{C}_2\text{H}_5\text{ONa}) = \frac{6.8}{68} = 0.10\ \text{mol} $$

The iodoethane is in excess, so the alkoxide is the limiting reagent and the
theoretical yield of ether is 0.10 mol. Molar mass of C₄H₁₀O
$= 48 + 10 + 16 = 74\ \text{g mol}^{-1}$, so the theoretical mass is
$0.10 \times 74 = 7.4\ \text{g}$.

At 75 % yield,

$$ m = 0.75 \times 7.4 = 5.55\ \text{g}, \qquad
V = \frac{m}{\rho} = \frac{5.55}{0.713} = 7.78\ \text{cm}^{3} $$
:::

::: example Worked example 12.3
**Problem.** 7.4 g of ethoxyethane is heated with an excess of hydroiodic acid.
Calculate the mass of iodoethane and of water formed. What would the products be,
and in what masses, if only 0.10 mol of **cold** HI were used?
(I = 126.9)

**Solution.**

$$ n(\text{C}_4\text{H}_{10}\text{O}) = \frac{7.4}{74} = 0.10\ \text{mol} $$

*Hot, excess HI.* C₂H₅OC₂H₅ + 2HI → 2C₂H₅I + H₂O

$n(\text{C}_2\text{H}_5\text{I}) = 2 \times 0.10 = 0.20\ \text{mol}$ and its molar
mass is $24 + 5 + 126.9 = 155.9\ \text{g mol}^{-1}$, so

$$ m(\text{C}_2\text{H}_5\text{I}) = 0.20 \times 155.9 = 31.2\ \text{g} $$

$n(\text{H}_2\text{O}) = 0.10\ \text{mol}$, so $m = 0.10 \times 18 = 1.8\ \text{g}$.

*Cold, 1 mol of HI per mol of ether.* C₂H₅OC₂H₅ + HI → C₂H₅OH + C₂H₅I

Now one mole of each product is formed per mole of ether:
$m(\text{C}_2\text{H}_5\text{OH}) = 0.10 \times 46 = 4.6\ \text{g}$ and
$m(\text{C}_2\text{H}_5\text{I}) = 0.10 \times 155.9 = 15.6\ \text{g}$.
:::

::: example Worked example 12.4
**Problem.** 10.8 g of anisole is refluxed with excess hydroiodic acid. Name and
calculate the mass of each organic product, and explain why iodobenzene is
**not** formed.

**Solution.** C₆H₅OCH₃ + HI → C₆H₅OH + CH₃I

Molar mass of anisole, C₇H₈O $= 84 + 8 + 16 = 108\ \text{g mol}^{-1}$, so

$$ n = \frac{10.8}{108} = 0.10\ \text{mol} $$

One mole of anisole gives one mole of each product.

Phenol, C₆H₅OH, $M = 94\ \text{g mol}^{-1}$:
$m = 0.10 \times 94 = 9.4\ \text{g}$.

Iodomethane, CH₃I, $M = 12 + 3 + 126.9 = 141.9\ \text{g mol}^{-1}$:
$m = 0.10 \times 141.9 = 14.2\ \text{g}$.

**Why not iodobenzene?** The iodide ion must attack the carbon from the side
opposite the leaving oxygen (SN₂). The methyl carbon is sp³ and open to such an
attack, but the ring carbon is sp² and its bond to oxygen has partial
double-bond character from delocalisation; a benzene ring also blocks backside
approach. So the CH₃–O bond breaks and the C₆H₅–O bond does not.
:::

## Chapter summary

- An ether is R–O–R′, formula CₙH₂ₙ₊₂O — a **functional isomer of an alcohol**.
  Simple ethers have identical groups, mixed ethers different ones.
- IUPAC names are **alkoxyalkanes**, the smaller group becoming the alkoxy
  substituent: C₂H₅OC₂H₅ is ethoxyethane, C₆H₅OCH₃ is methoxybenzene (anisole).
- Ethers show **metamerism** (different sharing of carbons about the oxygen),
  chain isomerism and functional isomerism with alcohols. C₄H₁₀O has 3 ethers
  and 4 alcohols.
- **Williamson's synthesis**: R–ONa + R′–X → R–O–R′ + NaX, an SN₂ reaction. The
  halide must be **methyl or primary**; a 3° halide gives an alkene and a
  haloarene gives nothing. For anisole use C₆H₅ONa + CH₃I.
- No O–H means no self-hydrogen-bonding, so ethoxyethane boils at 34.6 °C,
  about 83 °C below butan-1-ol and close to pentane. It is still water-soluble,
  because oxygen can **accept** a hydrogen bond from water.
- The oxygen lone pairs make ethers weak **Lewis bases**: cold conc. HCl or
  H₂SO₄ gives oxonium salts; hot acid cleaves both C–O bonds.
- HI cold gives alcohol + iodoalkane; hot excess HI gives 2 iodoalkane + water;
  anisole gives **phenol + iodomethane**.
- Ether left in air forms an explosive **peroxide**, CH₃CH(OOH)OC₂H₅ — store over
  sodium wire in dark bottles and never distil to dryness. Chlorine substitutes
  the α-hydrogens in the dark and every hydrogen in sunlight.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The IUPAC name of C₂H₅OCH₃ is <span class="marks">[1]</span>
   (a) ethoxymethane (b) methoxyethane (c) ethyl methyl ether (d) methoxymethane
2. CH₃OC₃H₇ and C₂H₅OC₂H₅ are <span class="marks">[1]</span>
   (a) chain isomers (b) position isomers (c) metamers (d) functional isomers
3. Anisole on refluxing with excess HI gives <span class="marks">[1]</span>
   (a) iodobenzene + methanol (b) phenol + iodomethane
   (c) benzene + iodomethane (d) phenol + methanol
4. Ethoxyethane boils at 34.6 °C while butan-1-ol boils at 117.7 °C because <span class="marks">[1]</span>
   (a) the ether has a smaller molar mass (b) the ether cannot form intermolecular
   hydrogen bonds (c) the ether is non-polar (d) the alcohol is ionic
5. The best pair of reagents for preparing 2-methoxy-2-methylpropane is <span class="marks">[1]</span>
   (a) CH₃ONa + (CH₃)₃CBr (b) (CH₃)₃CONa + CH₃I
   (c) CH₃OH + (CH₃)₃COH (d) CH₃Br + (CH₃)₃CBr
6. Diethyl ether stored for a long time in a half-empty bottle becomes dangerous
   because it forms <span class="marks">[1]</span>
   (a) ethanol (b) ethanal (c) a peroxide (d) an oxonium salt

::: note Answers to Group A
**1.** (b) — the **smaller** group (CH₃) becomes the methoxy substituent on the larger (ethane) chain.
**2.** (c) — same functional group, same formula, but the carbons are shared 1 + 3 against 2 + 2 about the oxygen.
**3.** (b) — only the sp³ methyl carbon can undergo SN₂, so the aryl–O bond survives.
**4.** (b) — an ether has no O–H hydrogen to donate, so its molecules are held together only by weak dipole and van der Waals forces.
**5.** (b) — the bulky group must be the alkoxide; (a) would give 2-methylpropene by elimination.
**6.** (c) — slow autoxidation gives CH₃CH(OOH)OC₂H₅, which explodes when the ether is distilled to dryness.
:::

**Group B — Short answer (5 marks each)**

1. What is Williamson's synthesis? Show how it is used to prepare ethoxyethane
   and anisole, and explain why CH₃ONa + C₆H₅Cl cannot be used. <span class="marks">[5]</span>
2. Explain why ethoxyethane (b.p. 34.6 °C) boils far below butan-1-ol
   (b.p. 117.7 °C) although both are C₄H₁₀O, yet the two are about equally
   soluble in water. <span class="marks">[5]</span>
3. What happens when ethoxyethane is treated with (a) cold HI, (b) hot excess HI,
   (c) cold conc. H₂SO₄, (d) chlorine in the dark, (e) air over a long period?
   Give equations. <span class="marks">[5]</span>
4. Write all the isomers of C₄H₁₀O with their IUPAC names, and state the type of
   isomerism shown by (i) ethoxyethane and butan-1-ol, (ii) ethoxyethane and
   1-methoxypropane. <span class="marks">[5]</span>
5. 14.8 g of ethoxyethane is heated with excess HI. Calculate the mass of
   iodoethane formed and the volume of HI required at STP. (I = 126.9) <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Williamson's synthesis is the SN₂ reaction of a sodium alkoxide or
phenoxide with a methyl or primary haloalkane:
C₂H₅ONa + C₂H₅I → C₂H₅OC₂H₅ + NaI, and
C₆H₅ONa + CH₃I → C₆H₅OCH₃ + NaI. CH₃ONa + C₆H₅Cl fails because the C–Cl bond in
a haloarene has partial double-bond character (the chlorine lone pair is
delocalised into the ring), the ring carbon is sp², and the benzene ring blocks
the backside approach that SN₂ requires.

**2.** Butan-1-ol has an O–H hydrogen, so its molecules are joined by
intermolecular hydrogen bonds that must be broken before it boils; ethoxyethane
has no O–H and is held only by dipole and van der Waals forces, so it boils about
83 °C lower — close to pentane (36.1 °C). Solubility is a different question:
water supplies the hydrogen, and the ether oxygen *accepts* the hydrogen bond, so
both compounds hydrogen-bond to **water** about equally well (6.5 g and 7.9 g per
100 cm³).

**3.** (a) C₂H₅OC₂H₅ + HI → C₂H₅OH + C₂H₅I.
(b) C₂H₅OC₂H₅ + 2HI → 2C₂H₅I + H₂O.
(c) It dissolves, forming the oxonium salt [(C₂H₅)₂OH]⁺HSO₄⁻ — the ether is
acting as a Lewis base.
(d) C₂H₅OC₂H₅ + 2Cl₂ → CH₃CHCl–O–CHClCH₃ + 2HCl (the two α-hydrogens are
replaced).
(e) Slow autoxidation: C₂H₅OC₂H₅ + O₂ → CH₃CH(OOH)OC₂H₅, an explosive peroxide.

**4.** Alcohols: butan-1-ol, butan-2-ol, 2-methylpropan-1-ol,
2-methylpropan-2-ol. Ethers: ethoxyethane, 1-methoxypropane, 2-methoxypropane —
seven isomers in all. (i) **Functional** isomerism (alcohol against ether).
(ii) **Metamerism** (2 + 2 against 1 + 3 carbons about the oxygen).

**5.** $n(\text{C}_4\text{H}_{10}\text{O}) = 14.8/74 = 0.20\ \text{mol}$.
C₂H₅OC₂H₅ + 2HI → 2C₂H₅I + H₂O, so
$n(\text{C}_2\text{H}_5\text{I}) = 0.40\ \text{mol}$ and
$m = 0.40 \times 155.9 = 62.4\ \text{g}$.
$n(\text{HI}) = 0.40\ \text{mol}$, so
$V = 0.40 \times 22.4 = 8.96\ \text{dm}^{3}$ at STP.
:::

**Group C — Long answer (8 marks each)**

1. (a) Define an ether and classify ethers with one example of each type.
   Explain metamerism using C₄H₁₀O. <span class="marks">[3]</span>
   (b) Describe Williamson's synthesis of an aliphatic and of an aromatic ether,
   give the mechanism in outline, and explain why the halide must be primary. <span class="marks">[3]</span>
   (c) How is ethoxyethane also obtained from ethanol? Why does this method fail
   for mixed ethers? <span class="marks">[2]</span>
2. (a) Give equations for the action of ethoxyethane with HI, conc. HCl,
   conc. H₂SO₄, air and Cl₂, stating the conditions in each case. <span class="marks">[5]</span>
   (b) 3.7 g of ethoxyethane is treated with just 0.050 mol of cold HI. Name the
   organic products and calculate the mass of each. <span class="marks">[3]</span>

::: note Answers to Group C
**1. (a)** An ether has an oxygen atom bonded to two carbon atoms, R–O–R′.
Simple (symmetrical): C₂H₅OC₂H₅. Mixed (unsymmetrical): CH₃OC₂H₅; aromatic
mixed: C₆H₅OCH₃. **Metamerism** is isomerism arising from a different
distribution of carbon atoms about the same functional group: for C₄H₁₀O,
C₂H₅–O–C₂H₅ (2 + 2) and CH₃–O–C₃H₇ (1 + 3) are metamers.
**(b)** C₂H₅ONa + C₂H₅I → C₂H₅OC₂H₅ + NaI;
C₆H₅ONa + CH₃I → C₆H₅OCH₃ + NaI. Mechanism: the alkoxide oxygen, a strong
nucleophile, attacks the carbon carrying the halogen from the side opposite the
C–X bond; the transition state has the oxygen and the halogen partially bonded on
opposite sides, and the halide leaves as the new C–O bond forms (SN₂). Because
the attack must come from behind the carbon, bulky groups block it: a 3° halide
reacts by elimination (E2) to give an alkene instead, so only methyl and primary
halides give good yields.
**(c)** 2C₂H₅OH --conc. H₂SO₄, 140 °C--> C₂H₅OC₂H₅ + H₂O. With a mixture of two
different alcohols, R–OH and R′–OH, all three ethers R–O–R, R–O–R′ and R′–O–R′
are formed together and are difficult to separate, so the method is useless for
mixed ethers.

**2. (a)** C₂H₅OC₂H₅ + HI (cold) → C₂H₅OH + C₂H₅I;
C₂H₅OC₂H₅ + 2HI (hot, excess) → 2C₂H₅I + H₂O;
C₂H₅OC₂H₅ + HCl (cold conc.) → [(C₂H₅)₂OH]⁺Cl⁻, and on heating under pressure
C₂H₅OC₂H₅ + 2HCl → 2C₂H₅Cl + H₂O;
C₂H₅OC₂H₅ + H₂SO₄ (cold) → [(C₂H₅)₂OH]⁺HSO₄⁻, and on heating
C₂H₅OC₂H₅ + 2H₂SO₄ → 2C₂H₅HSO₄ + H₂O;
C₂H₅OC₂H₅ + O₂ (air, light, slow) → CH₃CH(OOH)OC₂H₅;
C₂H₅OC₂H₅ + 2Cl₂ (dark) → CH₃CHCl–O–CHClCH₃ + 2HCl, and
C₂H₅OC₂H₅ + 10Cl₂ (sunlight) → C₂Cl₅OC₂Cl₅ + 10HCl.
**(b)** $n(\text{ether}) = 3.7/74 = 0.050\ \text{mol}$, and 0.050 mol of HI is
supplied, so the mole ratio is 1 : 1 and only one C–O bond is broken:
C₂H₅OC₂H₅ + HI → C₂H₅OH + C₂H₅I. The products are **ethanol**,
$m = 0.050 \times 46 = 2.3\ \text{g}$, and **iodoethane**,
$m = 0.050 \times 155.9 = 7.8\ \text{g}$.
:::
