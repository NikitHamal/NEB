---
subject: Chemistry
grade: 12
unit: 20
title: Paper and Pulp
hours: 3
area: Applied Chemistry
---

Every page of this book began as a tree, a stalk of *babiyo* grass or an old
newspaper. Paper is a thin mat of **cellulose fibres** felted together from a
water suspension; making it is essentially one chemical problem — how to strip
away the **lignin** that glues the fibres together in a plant, without destroying
the cellulose itself. This unit follows that problem from the forest to the reel.

::: key What the examiner wants from this unit
Name the raw materials and the two kinds of pulping; describe the **stages**
(pulping → washing and screening → bleaching → beating and sizing → sheet
formation → drying and calendering); draw the **flow sheet**; and list the
properties by which paper quality is judged. The recovery of chemicals in the
Kraft process is the favourite extra-mark question.
:::

## 20.1 Introduction

::: definition Paper and pulp
**Pulp** is a fibrous mass of cellulose obtained by breaking down plant material
mechanically or chemically. **Paper** is the sheet formed when a dilute water
suspension of pulp is drained on a wire screen, pressed and dried, so that the
fibres bond to one another through hydrogen bonds between their –OH groups.
:::

The fibre is **cellulose**, (C₆H₁₀O₅)ₙ, a linear polymer of β-glucose units with
n running into the thousands. Along with it, plant cell walls contain:

| Component | Nature | Wanted in paper? |
|---|---|---|
| Cellulose, 40–50 % | long β-1,4-glucose chains; strong, white, insoluble | **yes** — it is the fibre |
| Hemicellulose, 20–30 % | short branched sugar polymers | partly — helps fibres bond |
| Lignin, 18–30 % | cross-linked aromatic polymer, brown, binds fibres | **no** — it is stiff and yellows in light |
| Extractives, 2–8 % | resins, fats, tannins | no — they make pitch spots |

```figure caption="Composition of some papermaking raw materials (oven-dry basis). Non-wood fibres such as straw and babiyo grass carry far less lignin, so they can be pulped under milder conditions."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.9))
mats = ['softwood\n(pine)', 'hardwood\n(sal, poplar)', 'bamboo', 'wheat straw\n/ babiyo', 'waste\npaper']
cell = [42, 45, 45, 40, 78]
hemi = [27, 30, 20, 28, 12]
lign = [28, 21, 25, 17, 6]
extr = [3, 4, 10, 15, 4]
b = np.zeros(len(mats))
for vals, lab, c in [(cell, 'cellulose', SERIES[0]), (hemi, 'hemicellulose', SERIES[2]),
                     (lign, 'lignin', SERIES[3]), (extr, 'extractives, ash', MUTED)]:
    ax.bar(mats, vals, bottom=b, label=lab, color=c, width=0.6)
    b = b + np.array(vals)
ax.set_ylabel('percentage by mass')
ax.set_ylim(0, 100)
ax.legend(fontsize=6.8, ncol=4, frameon=False, loc='lower center',
          bbox_to_anchor=(0.5, 1.0), handlelength=1.1, columnspacing=1.1)
ax.tick_params(axis='x', labelsize=7.2)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, axis='y', alpha=.4)
```

Paper was invented in China by Ts'ai Lun in about **105 AD** from rags and bark,
and Nepal has its own old tradition: **lokta** paper, hand-made from the inner
bark of the Himalayan *Daphne bholua* shrub, has carried scriptures and *lal
purja* land certificates for centuries because it resists insects and lasts for
generations.

## 20.2 Raw materials and their sources

| Class | Examples | Source |
|---|---|---|
| **Softwood** (long fibre, 3–5 mm) | pine, fir, spruce | conifer plantations; gives strength |
| **Hardwood** (short fibre, 1–2 mm) | sal, poplar, eucalyptus, birch | forests; gives smoothness and bulk |
| **Non-wood fibre** | *babiyo* (sabai) grass, rice and wheat straw, bagasse, jute, bamboo, kans grass | Terai farms and river banks — the main Nepali source |
| **Bast fibre** | lokta bark, rags, cotton linters | Himalayan shrubs, textile waste |
| **Recycled fibre** | waste paper, cartons | urban waste — now over half of world furnish |
| **Chemicals** | NaOH, Na₂S, Na₂SO₄, lime, Cl₂/ClO₂, H₂O₂ | imported in Nepal |
| **Fillers and sizes** | china clay, CaCO₃, TiO₂, talc, rosin, alum, starch | mineral suppliers |

A rule of thumb: about **2.2 tonnes of oven-dry wood** yield one tonne of bleached
chemical pulp, because roughly half of the wood substance is dissolved away.

## 20.3 Stages in production of paper

**(a) Preparation of the wood.** Logs are debarked, chipped to pieces about
20 mm × 20 mm × 4 mm and screened, so that the cooking liquor can penetrate
quickly and evenly.

**(b) Pulping.** The chips are broken down into individual fibres.

| | Mechanical pulping | Chemical pulping |
|---|---|---|
| How | logs ground against a wet revolving stone, or chips refined between discs | chips cooked with chemicals in a digester |
| Lignin | left in the pulp | dissolved out |
| Yield | 90–95 % | 45–55 % |
| Fibre strength | low (fibres are cut) | high |
| Colour stability | poor — newsprint yellows | good |
| Used for | newsprint, cheap magazine paper | printing, writing, packaging paper |

The important chemical route is the **sulphate or Kraft process** (*Kraft* is
German for "strength"). Chips are cooked with **white liquor** — a solution of
sodium hydroxide and sodium sulphide — at about **170 °C** and 7–8 atm for 2–4
hours. The alkali breaks the ether links of lignin and the HS⁻ ion attacks it
further, so the lignin dissolves as soluble sodium salts, leaving the cellulose
fibres intact. The spent liquor, now dark brown, is called **black liquor**.

The older **sulphite process** cooks the chips instead with calcium or magnesium
bisulphite solution containing free SO₂, which converts lignin into soluble
lignosulphonic acids:

2SO₂ + CaCO₃ + H₂O → Ca(HSO₃)₂ + CO₂↑

It gives a paler pulp that is easier to bleach, but a weaker one, and its waste
liquor is hard to recover; most mills have moved to the Kraft process.

::: key Chemical recovery — why the Kraft process is economic
Black liquor is concentrated in multiple-effect evaporators to about 65 % solids
and burnt in a **recovery furnace**. Its organic matter provides all the steam the
mill needs, while the sodium salts collect as a molten smelt of Na₂CO₃ and Na₂S:

Na₂SO₄ + 2C → Na₂S + 2CO₂↑

The smelt is dissolved to give **green liquor** and then **causticised** with
slaked lime to regenerate the cooking alkali:

Na₂CO₃ + Ca(OH)₂ → 2NaOH + CaCO₃↓

The calcium carbonate "lime mud" is filtered off and reburnt in a lime kiln, so
the lime is recycled too:

CaCO₃ --Δ--> CaO + CO₂↑   and   CaO + H₂O → Ca(OH)₂

More than 95 % of the chemicals go round this loop again.
:::

**(c) Washing and screening.** The pulp is washed free of black liquor on rotary
vacuum washers and screened to remove knots, uncooked chips, sand and grit.

**(d) Bleaching.** Unbleached Kraft pulp is brown (it is the paper of cement
sacks). The residual lignin is removed in stages with oxygen, chlorine dioxide and
hydrogen peroxide. Chlorine dioxide is generated on site because it cannot be
stored:

2NaClO₃ + 4HCl → 2ClO₂↑ + Cl₂↑ + 2NaCl + 2H₂O

::: caution Elemental chlorine is no longer used
Bleaching with Cl₂ gas chlorinates the lignin and produces **dioxins** and other
organochlorine poisons in the effluent. Modern mills are **ECF** (elemental
chlorine free, using ClO₂) or **TCF** (totally chlorine free, using O₂, O₃ and
H₂O₂). Do not write "bleaching with bleaching powder" as a modern method.
:::

**(e) Beating (refining) and stock preparation.** The wet pulp is passed between
rotating bars, which fray and swell the fibre walls so that more –OH groups are
exposed and the fibres bond better. Then additives go in:

| Additive | Purpose |
|---|---|
| Rosin soap + alum, Al₂(SO₄)₃ | **sizing** — deposits aluminium resinate on the fibres so ink does not spread |
| China clay, CaCO₃, TiO₂, talc | **loading** — fills the gaps, giving opacity, whiteness and smoothness |
| Starch, cellulose gums | dry strength |
| Dyes, optical brighteners | colour, whiteness |

6C₁₉H₂₉COONa + Al₂(SO₄)₃ → 2(C₁₉H₂₉COO)₃Al + 3Na₂SO₄

**(f) Sheet formation on the paper machine.** A very dilute stock, about **0.5 %
fibre in water**, flows from the headbox onto a moving endless wire mesh. Water
drains through the wire and is sucked away, leaving a wet web of about 20 % solids;
press rolls squeeze it to 40 %; steam-heated drying cylinders take it to 94–95 %;
calender rolls press it smooth and the sheet is wound on a reel and slit.

```figure caption="The Fourdrinier paper machine. The figures along the top show how the dryness of the web rises from 0.5 % at the headbox to about 95 % at the reel."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.2,2.9))
ax.set_xlim(0, 13.6); ax.set_ylim(1.1, 7.1); ax.axis('off')
WEB = 4.15

def roll(x, y, r, fc):
    ax.add_patch(Circle((x, y), r, fc=fc, ec=INK, lw=1.0))

ax.plot([1.9, 12.6], [WEB, WEB], color=MUTED, lw=0.8, ls=':')
ax.add_patch(FancyBboxPatch((0.25, 3.5), 1.5, 1.4, boxstyle='round,pad=0.08',
                            fc='#dbe8f6', ec=INK, lw=1.0))
ax.text(1.0, 4.2, 'head\nbox', ha='center', va='center', fontsize=7.2, color=INK)

# wire section
ax.plot([1.85, 5.0], [WEB, WEB], color=INK, lw=1.7)
for x in (2.05, 3.45, 4.85):
    roll(x, WEB-0.26, 0.24, 'white')
ax.text(3.45, 4.75, 'wire (mesh)', ha='center', fontsize=7.2, color=INK)
for x in (2.5, 3.2, 3.9, 4.6):
    ax.annotate('', xy=(x, 3.05), xytext=(x, 3.75),
                arrowprops=dict(arrowstyle='-|>', color=SERIES[0], lw=0.9,
                                mutation_scale=8))
ax.text(3.55, 2.75, 'water drained and sucked away', ha='center', fontsize=7.0,
        color=SERIES[0])

for x in (5.75, 6.65):
    roll(x, WEB+0.36, 0.33, '#eef2f7'); roll(x, WEB-0.36, 0.33, '#eef2f7')
ax.text(6.2, 2.35, 'press\nrolls', ha='center', va='top', fontsize=7.2, color=INK)

for x in (7.9, 8.9, 9.9):
    roll(x, WEB+0.45, 0.42, '#f7ded4'); roll(x+0.5, WEB-0.45, 0.42, '#f7ded4')
ax.text(9.15, 2.35, 'drying\ncylinders', ha='center', va='top', fontsize=7.2,
        color=INK)

roll(11.45, WEB+0.32, 0.29, '#e8f2ea'); roll(11.45, WEB-0.32, 0.29, '#e8f2ea')
ax.text(11.45, 2.35, 'calender', ha='center', va='top', fontsize=7.2, color=INK)
roll(12.75, WEB+0.15, 0.62, '#f2f4f7')
ax.text(12.75, 2.35, 'reel', ha='center', va='top', fontsize=7.2, color=INK)

ax.annotate('', xy=(13.2, 5.95), xytext=(1.9, 5.95),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.0, mutation_scale=10))
ax.text(0.25, 6.45, 'dryness', ha='left', fontsize=7.4, color=MUTED)
for x, t in [(2.6, '0.5 %'), (6.2, '20 %'), (9.4, '40 %'), (12.7, '95 %')]:
    ax.text(x, 6.45, t, ha='center', fontsize=7.4, color='#A8271F')
```

## 20.4 Flow sheet for paper production

```figure caption="Flow sheet for paper by the Kraft (sulphate) process. The right-hand column is the chemical recovery cycle that regenerates the white liquor."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.2,4.4))
ax.set_xlim(0, 15.8); ax.set_ylim(0, 22.3); ax.axis('off')

def box(cx, y, txt, fc='#f2f5f9', w=5.6, h=1.75, fs=7.6, bold=False):
    ax.add_patch(FancyBboxPatch((cx-w/2, y), w, h, boxstyle='round,pad=0.10',
                                fc=fc, ec=INK, lw=1.0))
    ax.text(cx, y+h/2, txt, ha='center', va='center', fontsize=fs, color=INK,
            fontweight='bold' if bold else 'normal')

def arr(x1, y1, x2, y2, c=MUTED, lw=1.25):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='-|>', color=c, lw=lw, mutation_scale=10))

def path(pts, c=MUTED, lw=1.2):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    ax.plot(xs[:-1], ys[:-1], color=c, lw=lw, solid_capstyle='round')
    arr(xs[-2], ys[-2], xs[-1], ys[-1], c=c, lw=lw)

L, R = 3.4, 11.0
box(L, 20.1, 'wood / babiyo grass → chips', fc='#e8eff8', bold=True, fs=7.4)
arr(L, 20.1, L, 18.95)
box(L, 17.2, 'digester, 170 °C\nchips + white liquor', fc='#f7ded4')
arr(L, 17.2, L, 16.05)
box(L, 14.3, 'blow tank, washing\nand screening')
arr(L, 14.3, L, 13.15)
box(L, 11.4, 'bleaching\n(O₂, ClO₂, H₂O₂)', fc='#eef7ee')
arr(L, 11.4, L, 10.25)
box(L, 8.5, 'beating + sizing\n(rosin, alum, clay)')
arr(L, 8.5, L, 7.35)
box(L, 5.6, 'paper machine:\nwire, press, dryers')
arr(L, 5.6, L, 4.45)
box(L, 2.7, 'calendering and reeling\n→  PAPER', fc='#e8eff8', bold=True)

box(R, 17.2, 'multiple-effect\nevaporators', w=4.8)
box(R, 14.3, 'recovery furnace\nNa₂SO₄ + 2C → Na₂S + 2CO₂', w=6.3, fs=6.8)
box(R, 11.4, 'dissolving tank\n→  green liquor', w=4.8)
box(R, 8.5, 'causticiser\nNa₂CO₃ + Ca(OH)₂ → 2NaOH + CaCO₃', w=6.9, fs=6.2)
box(R, 5.6, 'lime kiln\nCaCO₃ → CaO + CO₂', w=4.8, fs=7.0)
arr(R, 17.2, R, 16.05); arr(R, 14.3, R, 13.15); arr(R, 11.4, R, 10.25)

# black liquor: washing  ->  evaporators
path([(6.2, 15.2), (7.4, 15.2), (7.4, 18.1), (8.55, 18.1)], c=SERIES[3])
ax.text(7.55, 16.5, 'black\nliquor', fontsize=6.8, color=SERIES[3], ha='left')
# lime sub-loop
arr(10.1, 8.5, 10.1, 7.4, c=MUTED, lw=1.1)
ax.text(9.95, 7.78, 'lime mud', fontsize=6.6, color=MUTED, ha='right', va='center')
arr(12.0, 7.4, 12.0, 8.5, c=SERIES[2], lw=1.1)
ax.text(12.15, 7.78, 'CaO → Ca(OH)₂', fontsize=6.6, color=SERIES[2],
        ha='left', va='center')
# white liquor return: causticiser -> digester
path([(14.45, 9.4), (15.3, 9.4), (15.3, 19.6), (7.0, 19.6), (7.0, 18.1),
      (6.3, 18.1)], c=SERIES[2], lw=1.3)
ax.text(10.6, 19.75, 'white liquor  NaOH + Na₂S', fontsize=7.0,
        color=SERIES[2], ha='center', va='bottom')
```

::: example Worked example 20.1 — pulp yield
**Problem.** A digester is charged with 5.0 tonnes of oven-dry wood containing
45 % cellulose, 26 % hemicellulose, 25 % lignin and 4 % extractives. Cooking
dissolves all the lignin and extractives and half of the hemicellulose.
Calculate the pulp yield.

**Solution.**

Cellulose retained = 0.45 × 5000 = 2250 kg
Hemicellulose retained = ½ × 0.26 × 5000 = 650 kg
Lignin and extractives retained = 0

Mass of pulp = 2250 + 650 = 2900 kg

$$ \text{yield} = \frac{2900}{5000} \times 100 = 58\ \% $$

The yield of a real Kraft cook is 45–50 %, lower than this, because some cellulose
is also degraded by the hot alkali. Mechanical pulping keeps everything and so
gives 90–95 %.
:::

::: example Worked example 20.2 — regenerating the cooking liquor
**Problem.** How much slaked lime is needed to causticise green liquor so as to
regenerate 1000 kg of NaOH, and what mass of lime mud is produced?
(Na = 23, O = 16, H = 1, C = 12, Ca = 40)

**Solution.** Na₂CO₃ + Ca(OH)₂ → 2NaOH + CaCO₃↓

M(NaOH) = 40, so moles of NaOH = 1000/40 = 25 kmol.

From the equation, Ca(OH)₂ needed = 25/2 = 12.5 kmol.

M[Ca(OH)₂] = 40 + 2(16+1) = 74, so mass = 12.5 × 74 = **925 kg**.

CaCO₃ formed = 12.5 kmol × 100 = **1250 kg** of lime mud.

Burning this mud in the lime kiln gives back
12.5 × 56 = 700 kg of CaO, which is slaked and used again — the loop closes.
:::

## 20.5 Quality of paper

Paper is sold and specified by measurable properties, not by appearance alone.

| Property | Meaning and unit | Typical value |
|---|---|---|
| **Grammage (GSM)** | mass per unit area, g m⁻² | newsprint 45, photocopy 70–80, card 200+ |
| Caliper | thickness, μm | 100 μm for 80 gsm |
| Bulk | caliper ÷ grammage, cm³ g⁻¹ | 1.2–1.5 |
| Brightness | % of blue light reflected | newsprint 58, copier paper 90+ |
| Opacity | % of light stopped; raised by TiO₂ and clay | > 90 % for printing paper |
| Tensile, burst and tear strength | resistance to pulling, bursting, tearing | high in long-fibre Kraft |
| Sizing (Cobb value) | water absorbed in 60 s, g m⁻² | low for writing paper |
| Ash content | % of mineral filler left on ignition | 5–20 % |
| pH | acid-free paper has pH 7–9 | archival paper is alkaline |
| Smoothness and finish | calendered, machine or glazed | — |

::: caution Acid sizing makes paper crumble
Rosin–alum sizing leaves the sheet slightly acidic (pH 4.5–5.5). Over decades the
acid hydrolyses the cellulose chains and the paper turns brown and brittle — the
reason old books fall apart. Documents meant to last are made on **acid-free**
paper sized with synthetic sizes and filled with CaCO₃, which buffers the sheet to
pH 7–9. Nepali lokta paper, made with an alkaline ash cook and no alum, survives
for centuries for the same reason.
:::

::: example Worked example 20.3 — grammage
**Problem.** A sheet of A4 paper measures 210 mm × 297 mm and the paper is
80 g m⁻². Find (a) the mass of one sheet, (b) the mass of a ream of 500 sheets,
and (c) the number of sheets that can be cut from 1 tonne of such paper.

**Solution.**

(a) Area = 0.210 × 0.297 = 0.06237 m²
mass = 80 × 0.06237 = **4.99 g ≈ 5.0 g**

(b) Ream = 500 × 4.99 = 2495 g = **2.50 kg**

(c) Number of sheets = 1 000 000 g ÷ 4.99 g = **2.0 × 10⁵ sheets**, that is about
400 reams per tonne.
:::

### Paper and pulp in Nepal

Nepal's one large integrated mill, **Bhrikuti Pulp and Paper** at Gaindakot in
Nawalparasi, was built in the mid-1980s with Chinese assistance and used *babiyo*
(sabai) grass and paddy straw rather than wood. It supplied much of the country's
paper, was privatised in 1992 and closed in 2011, and Nepal now imports most of
its paper from India, China and Indonesia. The mills still working are small ones
that recycle waste paper, together with several hundred cottage units in the hill
districts producing **lokta** paper for notebooks, gift wrap and export. The
attraction of Nepal's non-wood fibres is clear from the composition chart: less
lignin means a milder cook, less chemical and less effluent — but they are bulky,
seasonal and low in ash-free fibre, which is why a mill must sit close to its
fields.

## Chapter summary

- Paper is a mat of cellulose fibres, (C₆H₁₀O₅)ₙ, bonded by hydrogen bonds;
  pulping is the removal of lignin, which is brown, stiff and light-sensitive.
- Wood is roughly 45 % cellulose, 25 % hemicellulose and 25 % lignin; non-wood
  fibres such as babiyo grass and straw contain much less lignin.
- Raw materials: softwood (long fibre, strength), hardwood (short fibre,
  smoothness), non-wood fibre, rags and lokta bark, and recycled waste paper.
- Mechanical pulping gives 90–95 % yield but weak, yellowing pulp; chemical
  pulping gives 45–55 % yield of strong, stable fibre.
- Kraft (sulphate) process: cook chips with white liquor (NaOH + Na₂S) at 170 °C
  for 2–4 h; the sulphite process uses Ca(HSO₃)₂ with free SO₂.
- Chemical recovery: burn black liquor (Na₂SO₄ + 2C → Na₂S + 2CO₂↑), dissolve the
  smelt to green liquor, causticise it
  (Na₂CO₃ + Ca(OH)₂ → 2NaOH + CaCO₃↓) and reburn the lime mud
  (CaCO₃ → CaO + CO₂↑; CaO + H₂O → Ca(OH)₂).
- Stages: chipping → pulping → washing and screening → bleaching (ECF with ClO₂,
  not Cl₂) → beating, sizing with rosin + alum and loading with clay → sheet
  formation on the Fourdrinier wire → pressing, drying, calendering, reeling.
- Quality is measured by grammage (g m⁻²), caliper, brightness, opacity, tensile,
  burst and tear strength, sizing, ash content and pH; acid-free paper lasts
  longest.
- Bhrikuti Pulp and Paper, Gaindakot, worked on babiyo grass and straw from the
  mid-1980s until 2011; Nepal's living paper tradition is hand-made lokta paper.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The chief chemical constituent of paper is <span class="marks">[1]</span>
   (a) lignin (b) cellulose (c) starch (d) hemicellulose
2. The white liquor used in the Kraft process contains <span class="marks">[1]</span>
   (a) NaOH and Na₂S (b) Ca(HSO₃)₂ and SO₂ (c) NaOCl and NaOH (d) NaClO₃ and HCl
3. Lignin must be removed from pulp mainly because it <span class="marks">[1]</span>
   (a) is too expensive (b) dissolves the cellulose
   (c) is brown and makes the paper yellow in light (d) prevents drying
4. Causticisation of green liquor is represented by <span class="marks">[1]</span>
   (a) CaCO₃ → CaO + CO₂ (b) Na₂CO₃ + Ca(OH)₂ → 2NaOH + CaCO₃
   (c) Na₂SO₄ + 2C → Na₂S + 2CO₂ (d) 2SO₂ + CaCO₃ + H₂O → Ca(HSO₃)₂ + CO₂
5. Rosin and alum are added to pulp for <span class="marks">[1]</span>
   (a) bleaching (b) loading (c) sizing (d) drying
6. The grammage of ordinary photocopy paper is about <span class="marks">[1]</span>
   (a) 10 g m⁻² (b) 45 g m⁻² (c) 80 g m⁻² (d) 300 g m⁻²

::: note Answers to Group A
**1.** (b) — the fibre itself is cellulose.
**2.** (a) — sodium hydroxide with sodium sulphide.
**3.** (c) — residual lignin oxidises in light and yellows the sheet.
**4.** (b) — lime converts carbonate back to hydroxide.
**5.** (c) — aluminium resinate stops ink spreading.
**6.** (c) — 70–80 g m⁻² is the usual office grade.
:::

**Group B — Short answer (5 marks each)**

1. What are pulp and paper? Name the raw materials used for papermaking in Nepal
   and state one advantage of non-wood fibre. <span class="marks">[5]</span>
2. Compare mechanical and chemical pulping under yield, strength, colour stability
   and use. <span class="marks">[5]</span>
3. Describe the Kraft process, giving the composition of white liquor, the cooking
   conditions and the equations of chemical recovery. <span class="marks">[5]</span>
4. What is the purpose of (i) bleaching, (ii) beating, (iii) sizing and
   (iv) loading? Name one chemical used in each. <span class="marks">[5]</span>
5. List six properties by which the quality of paper is judged and explain why
   acid-free paper lasts longer. <span class="marks">[5]</span>
6. 4.0 tonnes of oven-dry straw contains 40 % cellulose, 28 % hemicellulose and
   17 % lignin. If cooking removes all the lignin and one-quarter of the
   hemicellulose, calculate the mass of pulp and the percentage yield. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Pulp is the fibrous cellulose mass got by breaking plant material down
mechanically or chemically; paper is the sheet formed when dilute pulp is drained
on a wire, pressed and dried. Nepali raw materials: babiyo (sabai) grass, rice and
wheat straw, bagasse, bamboo, lokta bark and waste paper. Non-wood fibre contains
much less lignin, so it needs a milder cook, less chemical and less energy.

**2.** See the table in §20.3: mechanical 90–95 % yield, weak short fibres, yellows
in light, used for newsprint; chemical 45–55 % yield, strong fibres, colour-stable,
used for printing, writing and packaging paper.

**3.** Chips are cooked with white liquor (NaOH + Na₂S) at about 170 °C and 7–8 atm
for 2–4 hours; lignin dissolves, leaving cellulose. Recovery:
Na₂SO₄ + 2C → Na₂S + 2CO₂↑ in the furnace;
Na₂CO₃ + Ca(OH)₂ → 2NaOH + CaCO₃↓ in the causticiser;
CaCO₃ --Δ--> CaO + CO₂↑ and CaO + H₂O → Ca(OH)₂ in the lime kiln.

**4.** (i) Bleaching removes residual lignin and whitens the pulp — ClO₂ or H₂O₂.
(ii) Beating frays and swells the fibres so they bond — mechanical, no chemical.
(iii) Sizing makes the sheet resist ink spread — rosin with alum, Al₂(SO₄)₃.
(iv) Loading fills the gaps for opacity and smoothness — china clay, CaCO₃ or TiO₂.

**5.** Grammage, caliper, brightness, opacity, strength (tensile, burst, tear),
sizing or Cobb value, ash content, pH, smoothness. Acid-free paper (pH 7–9) is not
slowly hydrolysed at its glycosidic links, so the cellulose chains keep their
length and the sheet does not become brown and brittle.

**6.** Cellulose retained = 0.40 × 4000 = 1600 kg.
Hemicellulose retained = ¾ × 0.28 × 4000 = 840 kg. Lignin retained = 0.
Pulp = 1600 + 840 = **2440 kg**; yield = 2440/4000 × 100 = **61 %**.
:::

**Group C — Long answer (8 marks each)**

1. Describe the manufacture of paper from wood by the Kraft process with a
   flow-sheet diagram, giving the stages from chipping to reeling and the
   equations of chemical recovery. <span class="marks">[8]</span>
2. (a) What is meant by the grammage of paper? A reel of paper 1.2 m wide and
   4000 m long weighs 336 kg. Find its grammage. <span class="marks">[4]</span>
   (b) Explain how bleaching is carried out in a modern mill and why elemental
   chlorine has been abandoned. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** Logs are debarked and chipped; the chips are cooked in a digester with
white liquor (NaOH + Na₂S) at 170 °C for 2–4 h, which dissolves the lignin; the
pulp is blown, washed and screened; it is bleached with O₂, ClO₂ and H₂O₂; beaten,
sized with rosin–alum and loaded with china clay; formed into a web on the
Fourdrinier wire from a 0.5 % suspension; pressed, dried on steam cylinders,
calendered, reeled and cut. The black liquor is evaporated and burnt
(Na₂SO₄ + 2C → Na₂S + 2CO₂↑), the smelt dissolved to green liquor and causticised
(Na₂CO₃ + Ca(OH)₂ → 2NaOH + CaCO₃↓), and the lime mud reburnt
(CaCO₃ → CaO + CO₂↑; CaO + H₂O → Ca(OH)₂). Draw the flow sheet of §20.4.

**2.** (a) Grammage is the mass of one square metre of the paper, in g m⁻².
Area = 1.2 × 4000 = 4800 m²; mass = 336 kg = 336 000 g.
Grammage = 336 000 / 4800 = **70 g m⁻²**.
(b) Bleaching is done in stages: an oxygen stage removes about half the residual
lignin cheaply, then chlorine dioxide (made on site by
2NaClO₃ + 4HCl → 2ClO₂↑ + Cl₂↑ + 2NaCl + 2H₂O) oxidises the rest, with alkaline
extraction and hydrogen peroxide stages between. Elemental chlorine was abandoned
because it chlorinates lignin to dioxins and other toxic, persistent
organochlorines that pass into the river; ECF and TCF sequences avoid them.
:::
