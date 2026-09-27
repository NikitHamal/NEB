---
subject: Chemistry
grade: 12
unit: 7
title: Studies of Heavy Metals
hours: 15
area: Inorganic Chemistry
---

Copper, zinc, mercury, iron and silver are the five metals the NEB course calls
**heavy metals** — dense metals whose chemistry has been worked out over
centuries of smelting. This is the longest unit in the book, but it is also the
most repetitive: every metal is handled in the same four moves. Where is it
found and how is it won from its ore? How does it behave with air, acids,
alkalis and other metal ions? What are its two or three examinable compounds?
What is it used for? Learn the pattern once and the five metals become five
copies of one template.

::: key What the examiner actually asks
Extraction questions carry the most marks: the **ore and its formula**, the
**furnace or process name**, and the **balanced equation for the key reduction
step**. Then come the "action of X on Y" one-liners, and finally the named
compounds — blue vitriol, white vitriol, calomel, corrosive sublimate, silver
nitrate. Every one of these is a table in this chapter. Memorise the tables.
:::

The whole unit is governed by one number per metal: its **standard reduction
potential**. A metal above hydrogen displaces hydrogen from dilute acid; a metal
below it does not, and must instead be dissolved by an *oxidising* acid such as
nitric acid. That single rule explains why zinc and iron fizz in dilute
hydrochloric acid while copper, mercury and silver sit there unchanged.

```figure caption="Standard reduction potentials of the five metals of this unit. Zinc and iron lie below hydrogen on this scale, so they displace hydrogen from dilute acids; copper, mercury and silver lie above it and need an oxidising acid such as nitric acid. The same ordering fixes every displacement reaction in the chapter."

import numpy as np, matplotlib.pyplot as plt
names = ['Zn²⁺/Zn', 'Fe²⁺/Fe', '2H⁺/H₂', 'Cu²⁺/Cu', 'Hg₂²⁺/Hg', 'Ag⁺/Ag']
vals  = [-0.76, -0.44, 0.00, 0.34, 0.79, 0.80]
cols = [SERIES[2], SERIES[2], MUTED, SERIES[1], SERIES[1], SERIES[1]]
y = np.arange(len(names))[::-1]
fig, ax = plt.subplots(figsize=(5.0, 2.8))
ax.barh(y, vals, color=cols, height=0.55)
for yy, v in zip(y, vals):
    lab = ' 0.00' if v == 0 else f'{v:+.2f}'
    ax.text(v + (0.035 if v >= 0 else -0.035), yy, lab,
            va='center', ha='left' if v >= 0 else 'right', fontsize=7.8, color=INK)
ax.axvline(0, color=INK, lw=1.0)
ax.set_yticks(y); ax.set_yticklabels(names, fontsize=8.2)
ax.set_xlabel('standard reduction potential  E° / V')
ax.set_xlim(-1.05, 1.05); ax.set_ylim(-0.6, 6.1)
ax.text(-0.98, 5.6, 'displace H₂ from dilute acid', fontsize=7.6, color=SERIES[2])
ax.text(0.98, 5.6, 'need an oxidising acid', fontsize=7.6, color=SERIES[1], ha='right')
ax.spines[['top', 'right', 'left']].set_visible(False)
ax.grid(axis='x', alpha=0.45)
```
## 7.1 Copper

Copper is the oldest worked metal: the Kathmandu Valley's repoussé work, the
gilded roofs of Pashupatinath and the water vessels of every Newari household
are copper or its alloys. Nepal has small copper showings at Wapsa in
Solukhumbu and in the Bhotkhola area, but none is mined industrially, so the
metal is imported.

### Occurrence and extraction from copper pyrite

| Ore | Formula | Type | Remark |
|---|---|---|---|
| Copper pyrite (chalcopyrite) | CuFeS₂ | sulphide | **the chief ore**, ~76% of world supply |
| Copper glance | Cu₂S | sulphide | rich but scarce |
| Cuprite (ruby copper) | Cu₂O | oxide | red |
| Malachite | CuCO₃·Cu(OH)₂ | carbonate | green |
| Azurite | 2CuCO₃·Cu(OH)₂ | carbonate | blue |

Copper pyrite carries only 2–3% copper, so the ore must be enriched before any
chemistry is done. The full route has five stages.

**1. Crushing and concentration by froth flotation.** The powdered ore is
stirred in water containing pine oil and a little sodium ethyl xanthate, and air
is blown through. The sulphide particles are wetted by the oil, stick to the
air bubbles and rise as a froth; the earthy gangue (silica, clay) is wetted by
water and sinks. Froth flotation is used because the ore is a **sulphide** —
sulphides are preferentially wetted by oil.

**2. Roasting.** The concentrate is heated in a current of air in a
reverberatory furnace at about 1070 K, below the melting point of the charge.
Moisture is driven off, volatile arsenic and antimony oxides escape, and the
sulphur burns:

- S + O₂ → SO₂
- 2CuFeS₂ + O₂ → Cu₂S + 2FeS + SO₂
- 2FeS + 3O₂ → 2FeO + 2SO₂
- 2Cu₂S + 3O₂ → 2Cu₂O + 2SO₂

Roasting is deliberately **incomplete**: enough Cu₂S must survive to reduce the
Cu₂O later.

**3. Smelting.** The roasted mass, mixed with coke and silica (sand), is smelted
in a small water-jacketed blast furnace. Silica is the **flux**; it removes iron
as a fusible slag:

- FeO + SiO₂ → FeSiO₃ (fusible slag, tapped off)
- Cu₂O + FeS → Cu₂S + FeO

The molten product that collects below the slag is **copper matte**, a mixture
of Cu₂S and FeS containing about 45% copper.

**4. Bessemerisation.** The matte is transferred to a Bessemer converter lined
with silica (an acidic lining, because the impurity FeO is basic). A hot air
blast is forced through the tuyères:

- 2FeS + 3O₂ → 2FeO + 2SO₂ , then FeO + SiO₂ → FeSiO₃ (slag)
- 2Cu₂S + 3O₂ → 2Cu₂O + 2SO₂
- **2Cu₂O + Cu₂S → 6Cu + SO₂↑**

The last equation is the heart of the process and is called **auto-reduction**
or **self-reduction**: the ore reduces itself, with no external reducing agent.
The copper obtained is 98% pure and is called **blister copper**, because the
escaping SO₂ leaves blisters on its solidified surface.

**5. Refining.** Two methods are used in succession.

*Poling.* Molten blister copper is stirred with poles of green (unseasoned)
wood. The hydrocarbons released reduce any dissolved Cu₂O back to copper, and
the layer of charcoal on top stops re-oxidation.

*Electrolytic refining.* This gives 99.95% copper — the purity needed for
electrical wiring.

| Part of the cell | What it is |
|---|---|
| Anode | thick plate of impure blister copper |
| Cathode | thin sheet of pure copper |
| Electrolyte | 15% CuSO₄ solution acidified with dilute H₂SO₄ |
| At the anode | Cu → Cu²⁺ + 2e⁻ (the anode dissolves) |
| At the cathode | Cu²⁺ + 2e⁻ → Cu (pure copper deposits) |
| Anode mud | Ag, Au, Pt — too noble to dissolve; falls below the anode |
| Left in solution | Zn²⁺, Fe²⁺ — too active to be deposited |

```figure caption="Electrolytic refining of copper. Impurities split three ways: noble metals fall as anode mud, active metals stay dissolved as ions, and only copper crosses to the cathode. The anode mud is valuable enough that many refineries recover their running costs from the silver and gold in it."

import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
fig, ax = plt.subplots(figsize=(4.8, 3.2))
ax.add_patch(Rectangle((0.5, 0.4), 7.0, 3.4, fc='none', ec=INK, lw=1.6))
ax.add_patch(Rectangle((0.55, 0.45), 6.9, 2.9, fc=ACCENT, alpha=0.10, ec='none'))
ax.add_patch(Rectangle((1.8, 0.7), 0.42, 3.3, fc=MUTED, ec=INK, lw=1.2))
ax.add_patch(Rectangle((5.7, 0.7), 0.18, 3.3, fc=SERIES[3], ec=INK, lw=1.2))
ax.text(2.0, 4.12, 'anode\nimpure Cu', ha='center', va='bottom', fontsize=8.0, color=INK)
ax.text(5.8, 4.12, 'cathode\npure Cu', ha='center', va='bottom', fontsize=8.0, color=INK)
ax.text(4.0, 3.02, 'CuSO₄(aq) + dil. H₂SO₄', ha='center', fontsize=8.2, color=INK)
ax.add_patch(FancyArrowPatch((2.6, 2.3), (5.3, 2.3), arrowstyle='-|>',
                             color=SERIES[1], lw=1.4, mutation_scale=11))
ax.text(3.95, 2.45, 'Cu²⁺', ha='center', fontsize=8.6, color=SERIES[1])
ax.text(2.35, 1.6, 'Cu → Cu²⁺ + 2e⁻', fontsize=7.8, color=INK)
ax.text(4.35, 1.1, 'Cu²⁺ + 2e⁻ → Cu', fontsize=7.8, color=INK)
ax.plot([2.0, 2.0, 3.35], [5.15, 5.75, 5.75], color=INK, lw=1.2)
ax.plot([4.1, 5.79, 5.79], [5.75, 5.75, 5.15], color=INK, lw=1.2)
ax.plot([3.45, 3.45], [5.5, 6.0], color=INK, lw=1.6)
ax.plot([3.75, 3.75], [5.62, 5.88], color=INK, lw=2.8)
ax.text(3.6, 6.15, 'DC supply, 0.2–0.5 V', ha='center', fontsize=7.8, color=MUTED)
rs = np.random.RandomState(3)
ax.plot(np.linspace(1.75, 2.35, 22), 0.56 + 0.04*rs.rand(22), '.',
        color=SERIES[4], ms=4)
ax.annotate('anode mud\n(Ag, Au, Pt)', (2.05, 0.56), textcoords='offset points',
            xytext=(-20, -30), fontsize=7.6, color=SERIES[4], ha='center',
            arrowprops=dict(arrowstyle='-|>', color=SERIES[4], lw=1.0, mutation_scale=8))
ax.text(6.85, 1.9, 'Zn²⁺, Fe²⁺\nstay in\nsolution', fontsize=7.4, color=MUTED, ha='center')
ax.set_xlim(0, 8.3); ax.set_ylim(-0.75, 6.5); ax.axis('off')
```
### Properties of copper

Copper is a soft, reddish-brown, ductile metal of density 8.95 g cm⁻³ and
melting point 1083 °C. It is the second best conductor of electricity after
silver.

| Reagent | Conditions | Reaction |
|---|---|---|
| Dry air | room temperature | no action |
| Moist air + CO₂ | long exposure | 2Cu + O₂ + CO₂ + H₂O → CuCO₃·Cu(OH)₂ (green patina) |
| Air | red heat, below 1370 K | 2Cu + O₂ → 2CuO (black) |
| Air | above 1370 K | 4Cu + O₂ → 2Cu₂O (red) |
| Dilute HCl / dilute H₂SO₄ | — | **no reaction** (Cu is below H in the series) |
| Hot conc. H₂SO₄ | — | Cu + 2H₂SO₄ → CuSO₄ + SO₂↑ + 2H₂O |
| Dilute HNO₃ | cold | 3Cu + 8HNO₃ → 3Cu(NO₃)₂ + 2NO↑ + 4H₂O |
| Conc. HNO₃ | — | Cu + 4HNO₃ → Cu(NO₃)₂ + 2NO₂↑ + 2H₂O |
| Conc. HCl | hot, air present | 2Cu + 4HCl + O₂ → 2CuCl₂ + 2H₂O |
| Cl₂ | heated | Cu + Cl₂ → CuCl₂ |

**Action with aqueous ammonia.** Copper is slowly dissolved by ammonia solution
**in the presence of air**, giving the deep blue tetraamminecopper(II) ion:

2Cu + 8NH₃ + O₂ + 2H₂O → 2[Cu(NH₃)₄](OH)₂

This deep blue solution is **Schweitzer's reagent**. It dissolves cellulose, and
squirting that solution into dilute acid regenerates the cellulose as a fibre —
this is how rayon (artificial silk) was first made.

**Action with metal ions (displacement).** Copper displaces from solution any
metal that lies below it in the electrochemical series, and is itself displaced
by any metal above it:

- Cu + 2AgNO₃ → Cu(NO₃)₂ + 2Ag (silver tree; the solution turns blue)
- Cu + Hg(NO₃)₂ → Cu(NO₃)₂ + Hg
- **Cu + 2FeCl₃ → CuCl₂ + 2FeCl₂**

The last reaction looks like an exception — iron is *above* copper, yet Fe³⁺
oxidises copper. It is not an exception: the relevant couple is Fe³⁺/Fe²⁺
(E° = +0.77 V), not Fe²⁺/Fe. It is used industrially to etch copper printed
circuit boards.

::: caution Displacement compares the right two couples
"Iron is more reactive than copper, so copper cannot react with an iron salt"
is a trap. Copper *does* react with Fe³⁺ because the Fe³⁺/Fe²⁺ couple sits
above Cu²⁺/Cu. Always name the **couple**, never just the element.
:::

### Uses of copper

1. Electrical wiring, cables, busbars and motor windings — second only to silver
   in conductivity but far cheaper.
2. Utensils, boilers, calorimeters and distillation vessels (high thermal
   conductivity, not attacked by water).
3. Alloys: **brass** (Cu + Zn), **bronze** (Cu + Sn), **gun metal**
   (Cu + Sn + Zn), **German silver** (Cu + Zn + Ni), **coinage alloys**.
4. Electroplating and electrotyping; roofing sheets, temple ornament and
   repoussé work.
5. Copper salts as fungicides (Bordeaux mixture) and in electroplating baths.

### Chemistry of blue vitriol, CuSO₄·5H₂O

Blue vitriol, *nilathotha* in Nepali, is copper(II) sulphate pentahydrate.

**Preparation.** On the laboratory scale, dissolve copper(II) oxide or carbonate
in warm dilute sulphuric acid and crystallise:

CuO + H₂SO₄ → CuSO₄ + H₂O

Industrially, scrap copper is heated with dilute sulphuric acid while air is
blown through:

2Cu + 2H₂SO₄ + O₂ → 2CuSO₄ + 2H₂O

**Structure.** The crystal is not "copper sulphate with five loose waters". Four
water molecules are bonded to the copper ion in a square plane and the fifth is
held by hydrogen bonds to the sulphate, so the formula is better written
**[Cu(H₂O)₄]SO₄·H₂O**.

**Action of heat.** The water is lost in three well-separated stages:

| Temperature | Change | Colour |
|---|---|---|
| 100 °C | CuSO₄·5H₂O → CuSO₄·H₂O + 4H₂O | blue → pale blue |
| 230 °C | CuSO₄·H₂O → CuSO₄ + H₂O | pale blue → **white** |
| 720 °C | CuSO₄ → CuO + SO₃ | white → black |

Anhydrous copper sulphate is white and turns blue with water, which is the
standard laboratory **test for water**.

```figure caption="Thermal dehydration of one mole of blue vitriol. Each step is a sharp, separate loss, which is why the pentahydrate is written [Cu(H₂O)₄]SO₄·H₂O — the fifth water, hydrogen-bonded to the sulphate, is the one that needs 230 °C to leave."
import numpy as np, matplotlib.pyplot as plt
T = np.array([25, 100, 100, 230, 230, 720, 720, 900])
M = np.array([249.5, 249.5, 177.5, 177.5, 159.5, 159.5, 79.5, 79.5])
fig, ax = plt.subplots(figsize=(5.0, 2.9))
ax.plot(T, M, color=ACCENT, lw=2.0)
ax.fill_between(T, 0, M, color=ACCENT, alpha=0.08)
labs = [(60, 249.5, 'CuSO₄·5H₂O\n249.5 g, blue'),
        (165, 177.5, 'CuSO₄·H₂O\n177.5 g'),
        (470, 159.5, 'CuSO₄\n159.5 g, white'),
        (810, 79.5, 'CuO\n79.5 g, black')]
for x, y, s in labs:
    ax.annotate(s, (x, y), textcoords='offset points', xytext=(0, 9),
                ha='center', fontsize=7.4, color=INK)
for x, s in [(100, '−4H₂O'), (230, '−H₂O'), (720, '−SO₃')]:
    ax.annotate(s, (x, 0), textcoords='offset points', xytext=(0, 6),
                ha='center', fontsize=7.6, color=SERIES[1])
    ax.axvline(x, color=SERIES[1], lw=0.8, ls=':')
ax.set_xlabel('temperature (°C)'); ax.set_ylabel('mass of residue (g per mole)')
ax.set_xlim(0, 940); ax.set_ylim(0, 300)
ax.spines[['top', 'right']].set_visible(False); ax.grid(alpha=0.4)
```

**Reactions of the solution.** These are the reactions of the hydrated Cu²⁺ ion
and are examined every year.

| Reagent | Observation | Equation |
|---|---|---|
| NaOH(aq) | blue gelatinous precipitate | CuSO₄ + 2NaOH → Cu(OH)₂↓ + Na₂SO₄ |
| NH₃(aq), a little | pale blue precipitate | CuSO₄ + 2NH₄OH → Cu(OH)₂↓ + (NH₄)₂SO₄ |
| NH₃(aq), excess | precipitate dissolves, **deep blue** | Cu(OH)₂ + 4NH₃ → [Cu(NH₃)₄](OH)₂ |
| H₂S | black precipitate | CuSO₄ + H₂S → CuS↓ + H₂SO₄ |
| KI | white precipitate + brown iodine | 2CuSO₄ + 4KI → Cu₂I₂↓ + 2K₂SO₄ + I₂ |
| KCN, excess | cyanogen gas evolved | 2CuSO₄ + 4KCN → Cu₂(CN)₂↓ + 2K₂SO₄ + C₂N₂↑ |
| Fe or Zn | red-brown copper deposits | Fe + CuSO₄ → FeSO₄ + Cu |

Note the last two rows carefully: iodide and cyanide both **reduce** copper(II)
to copper(I). Cu²⁺ does not give CuI₂ or Cu(CN)₂; those compounds decompose at
once.

**Uses of blue vitriol.** Bordeaux mixture (CuSO₄ + slaked lime) sprayed against
blight and mildew on potato, tomato and grape; electroplating and electrolytic
refining baths; Fehling's solution and Benedict's solution for reducing sugars;
a mordant in calico printing; an algicide in drinking-water tanks; a laboratory
test for water.

### Red oxide and black oxide of copper

| | Red oxide | Black oxide |
|---|---|---|
| Name | copper(I) oxide, cuprous oxide | copper(II) oxide, cupric oxide |
| Formula | **Cu₂O** | **CuO** |
| Colour | red | black |
| Nature | basic, covalent character | basic |
| Made by | reduction of Fehling's solution by a reducing sugar; or 4Cu + O₂ → 2Cu₂O above 1370 K | 2Cu + O₂ → 2CuO at red heat; or Cu(NO₃)₂ heated |
| Uses | red ("ruby") glass and glazes; **antifouling paint** for ships' hulls; copper oxide rectifiers; as a fungicide for seed dressing | pigment for blue and green glass and ceramics; **oxidising agent in the combustion analysis of organic compounds**; making rayon and other copper salts; desulphurising petroleum |

::: example Worked example 7.1
**Problem.** A sample of ore contains 20.0% copper pyrite, CuFeS₂, by mass.
Calculate the mass of copper that can be recovered from 1.00 tonne of this ore
if the overall recovery of the plant is 90%.
(Cu = 63.5, Fe = 56, S = 32)

**Solution.** First the percentage of copper in the pure mineral:

$$ M(\text{CuFeS}_2) = 63.5 + 56 + 2(32) = 183.5\ \text{g mol}^{-1} $$

$$ \%\,\text{Cu} = \frac{63.5}{183.5}\times 100 = 34.60\% $$

Copper as a fraction of the **ore** is $0.200 \times 34.60\% = 6.92\%$.

Mass of copper in 1.00 tonne = 1000 kg:

$$ m = 1000 \times 0.0692 = 69.2\ \text{kg} $$

At 90% recovery, $m = 0.90 \times 69.2 = 62.3\ \text{kg}$ of copper.
:::

::: example Worked example 7.2
**Problem.** 24.95 g of blue vitriol is heated first to 100 °C, then to 230 °C.
Calculate the mass of the residue at each stage and the total mass of water
lost. (Cu = 63.5, S = 32, O = 16, H = 1)

**Solution.** $M(\text{CuSO}_4\cdot 5\text{H}_2\text{O}) = 63.5+32+64+90 = 249.5\ \text{g mol}^{-1}$, so

$$ n = \frac{24.95}{249.5} = 0.100\ \text{mol} $$

At 100 °C four moles of water leave per mole of salt:

$$ m(\text{H}_2\text{O}) = 0.100 \times 4 \times 18 = 7.2\ \text{g} $$

so the residue CuSO₄·H₂O weighs $24.95 - 7.2 = 17.75\ \text{g}$.

At 230 °C the fifth water leaves: a further $0.100 \times 18 = 1.8\ \text{g}$,
giving white anhydrous CuSO₄ of mass $17.75 - 1.8 = 15.95\ \text{g}$
(check: $0.100 \times 159.5 = 15.95\ \text{g}$ ✔).

Total water lost $= 7.2 + 1.8 = 9.0\ \text{g}$.
:::

## 7.2 Zinc

Zinc is the metal that protects other metals. In Nepal it matters twice over:
the Ganesh Himal lead–zinc deposit in Dhading is the country's best-known metal
prospect, and galvanised (*jasta*) roofing sheet is the standard roof of the
hills.

### Occurrence and extraction from zinc blende

| Ore | Formula | Remark |
|---|---|---|
| Zinc blende (sphalerite) | **ZnS** | chief ore |
| Calamine (smithsonite) | ZnCO₃ | carbonate ore |
| Zincite | ZnO | red, rare |
| Willemite | Zn₂SiO₄ | silicate |

**1. Concentration by froth flotation** — again a sulphide ore, again pine oil
and air. Blende often carries galena (PbS), so a depressant is used to float the
two sulphides separately.

**2. Roasting.** The concentrate is roasted at about 1200 K in a free supply of
air in a fluidised-bed roaster:

2ZnS + 3O₂ → 2ZnO + 2SO₂↑

(A carbonate ore is **calcined** instead: ZnCO₃ → ZnO + CO₂.) The SO₂ is not
wasted — it is fed to a contact-process plant to make sulphuric acid.

**3. Reduction (smelting).** The zinc oxide is mixed with powdered coke and
heated to 1673 K in fireclay retorts:

**ZnO + C → Zn + CO↑**

At this temperature zinc is a **vapour** (b.p. 907 °C), so it distils over and
is condensed. This is the crucial difference from iron smelting, and the reason
zinc was isolated so late in history: cool the vapour in air and it simply burns
back to ZnO. The condensed metal, 97–98% pure, is called **spelter**, and the
fine powder that condenses first is **zinc dust**.

**4. Refining.** Three options: *liquation* (melting on a sloping hearth so that
zinc runs off and less fusible iron stays behind), *fractional distillation*,
and *electrolytic refining* using ZnSO₄ + H₂SO₄ as electrolyte with aluminium
cathodes, which gives 99.95% zinc.

::: caution Roast, then reduce — never reduce a sulphide directly
Carbon will not reduce ZnS. Every sulphide ore in this chapter is first
converted to the **oxide** by roasting, because carbon reduces oxides but has
no affinity for sulphur. Copper is the one apparent exception, and there the
reducing agent is not carbon but the ore's own sulphide (auto-reduction).
:::

### Properties of zinc

Zinc is a bluish-white metal, brittle at room temperature, malleable between
100 °C and 150 °C, and brittle again above 200 °C — so zinc sheet is always
rolled hot.

| Reagent | Reaction |
|---|---|
| Moist air | 2Zn + O₂ + CO₂ + H₂O → ZnCO₃·Zn(OH)₂ (protective film) |
| Air, strong heating | 2Zn + O₂ → 2ZnO (burns with a bluish-white flame; the white ZnO smoke is **philosopher's wool**) |
| Dilute HCl | Zn + 2HCl → ZnCl₂ + H₂↑ |
| Dilute H₂SO₄ | Zn + H₂SO₄ → ZnSO₄ + H₂↑ |
| Hot conc. H₂SO₄ | Zn + 2H₂SO₄ → ZnSO₄ + SO₂↑ + 2H₂O |
| Very dilute HNO₃, cold | 4Zn + 10HNO₃ → 4Zn(NO₃)₂ + NH₄NO₃ + 3H₂O |
| Dilute HNO₃ | 3Zn + 8HNO₃ → 3Zn(NO₃)₂ + 2NO↑ + 4H₂O |
| Conc. HNO₃ | Zn + 4HNO₃ → Zn(NO₃)₂ + 2NO₂↑ + 2H₂O |
| Hot NaOH(aq) | Zn + 2NaOH → Na₂ZnO₂ + H₂↑ (sodium zincate) |
| Steam, red heat | Zn + H₂O → ZnO + H₂↑ |

The reaction with alkali is written more accurately as

Zn + 2NaOH + 2H₂O → Na₂[Zn(OH)₄] + H₂↑

Because zinc dissolves in **both** acid and alkali with evolution of hydrogen,
it is **amphoteric** — the single most-asked fact about the metal.

**Displacement.** Zinc lies well below hydrogen (E° = −0.76 V), so it displaces
almost every common metal from solution:

- Zn + CuSO₄ → ZnSO₄ + Cu
- Zn + FeSO₄ → ZnSO₄ + Fe
- Zn + 2AgNO₃ → Zn(NO₃)₂ + 2Ag
- 2Na[Ag(CN)₂] + Zn → Na₂[Zn(CN)₄] + 2Ag (used in the silver cyanide process)

In alkaline solution zinc is such a strong reducing agent that it reduces
nitrates all the way to ammonia — the basis of a test for the nitrate ion:

4Zn + 7NaOH + NaNO₃ → 4Na₂ZnO₂ + NH₃↑ + 2H₂O

### Uses of zinc

1. **Galvanising** iron sheet, pipe, nails and wire — the largest single use.
2. Alloys: brass, German silver, bronze solders and die-casting alloys.
3. The negative electrode (the can) of the dry Leclanché cell.
4. **Zinc dust** as a reducing agent in the laboratory and in industry; zinc
   amalgam in Clemmensen reduction.
5. **Sacrificial anodes** on ships' hulls, buried pipelines and water heaters.
6. Zinc oxide in white paint, rubber compounding, cosmetics and calamine lotion;
   zinc sulphate as a micronutrient fertiliser on zinc-deficient paddy soils.

### Chemistry of white vitriol, ZnSO₄·7H₂O

**Preparation.** Dissolve zinc, zinc oxide or zinc carbonate in dilute sulphuric
acid and crystallise the solution **below 30 °C**:

- Zn + H₂SO₄ → ZnSO₄ + H₂↑
- ZnO + H₂SO₄ → ZnSO₄ + H₂O

Above 30 °C the hexahydrate crystallises instead, and above 70 °C the
monohydrate, so temperature control matters.

**Action of heat.**

| Temperature | Change |
|---|---|
| 100 °C | ZnSO₄·7H₂O → ZnSO₄·H₂O + 6H₂O |
| 450 °C | ZnSO₄·H₂O → ZnSO₄ + H₂O |
| red heat | 2ZnSO₄ → 2ZnO + 2SO₂↑ + O₂↑ |

**Reactions in solution.**

| Reagent | Observation | Equation |
|---|---|---|
| NaOH, a little | white precipitate | ZnSO₄ + 2NaOH → Zn(OH)₂↓ + Na₂SO₄ |
| NaOH, excess | precipitate **dissolves** | Zn(OH)₂ + 2NaOH → Na₂[Zn(OH)₄] |
| NH₃, a little | white precipitate | ZnSO₄ + 2NH₄OH → Zn(OH)₂↓ + (NH₄)₂SO₄ |
| NH₃, excess | dissolves, colourless | Zn(OH)₂ + 4NH₃ → [Zn(NH₃)₄](OH)₂ |
| H₂S in alkaline medium | white precipitate | ZnSO₄ + H₂S → ZnS↓ + H₂SO₄ |
| BaCl₂ | white precipitate, acid-insoluble | ZnSO₄ + BaCl₂ → BaSO₄↓ + ZnCl₂ |
| K₄[Fe(CN)₆] | white precipitate | 2ZnSO₄ + K₄[Fe(CN)₆] → Zn₂[Fe(CN)₆]↓ + 2K₂SO₄ |

The white Zn(OH)₂ that dissolves in **excess** alkali is the standard way of
telling zinc from other white-precipitate cations: aluminium behaves similarly
with NaOH but not with excess ammonia, while magnesium dissolves in neither.

**Uses of white vitriol.** Making **lithopone** (ZnS + BaSO₄), a brilliant white
pigment that does not blacken in polluted air as white lead does; as an eye
lotion and mild astringent antiseptic; a mordant in dyeing and calico printing;
electrolyte in zinc electroplating; a wood preservative; and a zinc fertiliser.

::: example Worked example 7.3
**Problem.** 194.8 g of pure zinc blende is roasted completely, and the zinc
oxide formed is then reduced by coke. Calculate (a) the volume of SO₂ produced
at STP and (b) the mass of zinc obtained, assuming both steps go to completion.
(Zn = 65.4, S = 32, molar volume at STP = 22.4 L mol⁻¹)

**Solution.** $M(\text{ZnS}) = 65.4 + 32 = 97.4\ \text{g mol}^{-1}$, so

$$ n(\text{ZnS}) = \frac{194.8}{97.4} = 2.00\ \text{mol} $$

(a) From 2ZnS + 3O₂ → 2ZnO + 2SO₂, the mole ratio ZnS : SO₂ is 1 : 1, so
$n(\text{SO}_2) = 2.00\ \text{mol}$ and

$$ V = 2.00 \times 22.4 = 44.8\ \text{L at STP} $$

(b) From ZnO + C → Zn + CO, the ratio ZnO : Zn is also 1 : 1, so
$n(\text{Zn}) = 2.00\ \text{mol}$ and

$$ m = 2.00 \times 65.4 = 130.8\ \text{g of zinc} $$
:::

## 7.3 Mercury

Mercury is the only metal that is liquid at room temperature, and the only one
on this list that is a cumulative poison. Its vapour damages the nervous system,
which is why mercury thermometers and sphygmomanometers are being withdrawn
from Nepali hospitals under the Minamata Convention.

### Occurrence and extraction from cinnabar

| Ore | Formula | Colour |
|---|---|---|
| **Cinnabar** | **HgS** | bright red — the chief ore |
| Calomel (horn quicksilver) | Hg₂Cl₂ | white |
| Livingstonite | HgSb₄S₈ | grey |

**1. Concentration.** The crushed ore is concentrated by froth flotation.

**2. Roasting — and that is the whole extraction.** Cinnabar is roasted in a
current of air at 700–800 K in a shaft or rotary furnace:

**HgS + O₂ → Hg + SO₂↑**

No reducing agent is needed. Mercury(II) oxide is so unstable that even if it
forms first it decomposes at once:

2HgS + 3O₂ → 2HgO + 2SO₂ , then 2HgO → 2Hg + O₂

This makes mercury the easiest metal in the syllabus to extract: it is the only
one whose oxide falls apart on heating, which is precisely how Priestley and
Lavoisier discovered oxygen.

**3. Condensation.** The mercury vapour (b.p. 357 °C) is led through a long
series of water-cooled earthenware condensers and collects as liquid metal.

**4. Purification.** Two steps:

- The crude metal is allowed to fall as a fine spray down a tall column of
  dilute nitric acid. Base metals (Zn, Pb, Sn, Cu) dissolve; mercury, being
  noble, does not. Any mercury that does dissolve is recovered by shaking with
  more mercury.
- The washed metal is **distilled under reduced pressure**. Laboratory-grade
  mercury is "triple-distilled", 99.999% pure.

### Properties of mercury

| Property | Value |
|---|---|
| Melting point | −38.9 °C |
| Boiling point | 356.6 °C |
| Density | 13.6 g cm⁻³ |
| Electrical conductivity | moderate |
| Thermal conductivity | poor |

Mercury has a high surface tension, so it does not wet glass and forms convex
menisci; it expands almost uniformly between 0 °C and 100 °C, which is why it
was the standard thermometric liquid.

| Reagent | Reaction |
|---|---|
| Dry or moist air, cold | no action (it keeps its mirror surface) |
| Air at about 350 °C | 2Hg + O₂ → 2HgO (red) |
| The same oxide above 400 °C | 2HgO → 2Hg + O₂↑ |
| Dilute HCl, dilute H₂SO₄ | **no reaction** |
| Hot conc. H₂SO₄, excess acid | Hg + 2H₂SO₄ → HgSO₄ + SO₂↑ + 2H₂O |
| Hot conc. H₂SO₄, excess mercury | 2Hg + 2H₂SO₄ → Hg₂SO₄ + SO₂↑ + 2H₂O |
| Cold dilute HNO₃, excess mercury | 6Hg + 8HNO₃ → 3Hg₂(NO₃)₂ + 2NO↑ + 4H₂O |
| Hot conc. HNO₃, excess acid | Hg + 4HNO₃ → Hg(NO₃)₂ + 2NO₂↑ + 2H₂O |
| Cl₂, excess | Hg + Cl₂ → HgCl₂ |
| Cl₂, limited | 2Hg + Cl₂ → Hg₂Cl₂ |
| Sulphur, rubbed together | Hg + S → HgS (black) |

::: key Excess of which reagent decides the oxidation state
With mercury, **excess metal gives the mercurous (Hg₂²⁺) salt and excess acid
or halogen gives the mercuric (Hg²⁺) salt**. Two answers to the same question
are both right; the condition in the question tells you which. The Hg₂²⁺ ion
always contains an Hg–Hg bond, so it is never written as Hg⁺.
:::

Mercury dissolves most metals to give **amalgams** — sodium amalgam and zinc
amalgam are common reducing agents, and dental amalgam is Ag–Sn–Hg. Iron and
platinum do **not** amalgamate, which is why mercury is stored and transported
in iron bottles. Powdered sulphur is sprinkled on a spilt mercury bead because
the solid black sulphide formed is not volatile and can be swept up safely.

### Chemistry of calomel, Hg₂Cl₂

Calomel is mercury(I) chloride, a white insoluble powder.

**Preparation.**

- By precipitation: Hg₂(NO₃)₂ + 2NaCl → Hg₂Cl₂↓ + 2NaNO₃
- By grinding corrosive sublimate with mercury: HgCl₂ + Hg → Hg₂Cl₂
- By reduction with tin(II) chloride: 2HgCl₂ + SnCl₂ → Hg₂Cl₂↓ + SnCl₄

**Properties.** It is a white solid, insoluble in water, tasteless and
non-poisonous (unlike the mercuric compound), and it sublimes at about 400 °C.

*Action of ammonia* — the identifying test:

**Hg₂Cl₂ + 2NH₃ → Hg(NH₂)Cl↓ + Hg↓ + NH₄Cl**

The finely divided free mercury turns the white solid **black**. The name
calomel comes from the Greek *kalos melas*, "beautiful black", for exactly this
reaction.

*Action of excess potassium iodide* — disproportionation again:

Hg₂Cl₂ + 2KI → HgI₂ + Hg↓ + 2KCl

**Uses.** The **calomel electrode** — a standard secondary reference electrode
in every pH meter (E° = +0.28 V for the saturated form); formerly a purgative
in medicine; in fungicides and in sweet-mercury preparations.

### Chemistry of corrosive sublimate, HgCl₂

Corrosive sublimate is mercury(II) chloride — a violent poison, as the name
warns.

**Preparation.**

- Direct: Hg + Cl₂ → HgCl₂ (excess chlorine, about 300 °C)
- Industrial: mercury(II) sulphate is heated with sodium chloride, and the
  product sublimes off:

HgSO₄ + 2NaCl → HgCl₂↑ + Na₂SO₄

A little manganese dioxide is added to oxidise any mercurous salt to the
mercuric state.

**Properties.** A white crystalline solid, sparingly soluble in water, very
soluble in alcohol and ether. In solution it is **largely un-ionised** — it is
essentially a covalent molecule, Cl–Hg–Cl — so a fresh solution gives only a
faint test for chloride ion with silver nitrate. It sublimes readily on heating.

| Reagent | Observation | Equation |
|---|---|---|
| NaOH | yellow precipitate | HgCl₂ + 2NaOH → HgO↓ + 2NaCl + H₂O |
| NH₃ | white precipitate (the 'infusible white precipitate') | HgCl₂ + 2NH₃ → Hg(NH₂)Cl↓ + NH₄Cl |
| SnCl₂, limited | white precipitate of calomel | 2HgCl₂ + SnCl₂ → Hg₂Cl₂↓ + SnCl₄ |
| SnCl₂, excess | grey-black free mercury | Hg₂Cl₂ + SnCl₂ → 2Hg↓ + SnCl₄ |
| KI, limited | scarlet precipitate | HgCl₂ + 2KI → HgI₂↓ + 2KCl |
| KI, excess | precipitate dissolves | HgI₂ + 2KI → K₂[HgI₄] |

The last row makes **Nessler's reagent** (alkaline K₂[HgI₄]), the standard test
for ammonia and ammonium salts — it gives a brown precipitate with NH₄⁺, and is
used to check drinking water and effluent in Nepali laboratories.

The two-stage reaction with tin(II) chloride is the classic distinction: a white
precipitate turning grey on adding more SnCl₂ proves a **mercuric** salt.

**Uses.** Antiseptic and disinfectant in 1 : 1000 solution; preserving timber
and anatomical specimens; making Nessler's reagent and calomel; catalyst
(with HgSO₄) for the hydration of ethyne to ethanal; seed dressing; and as a
laboratory reagent.

::: caution Calomel and corrosive sublimate are opposites in almost every way
Calomel Hg₂Cl₂ is insoluble, tasteless and non-poisonous; corrosive sublimate
HgCl₂ is soluble, sharply metallic-tasting and lethal. Ammonia blackens the
first and gives a persistent **white** precipitate with the second. Do not swap
their formulae — Hg₂Cl₂ has the Hg–Hg bond.
:::

## 7.4 Iron

Iron is the working metal of the modern world and the central atom of
haemoglobin. Nepal's Dhaubadi deposit in Nawalparasi, together with older
showings at Phulchoki (Lalitpur) and Thoshe (Ramechhap), is the basis of the
country's first planned iron and steel plant.

### Occurrence and extraction

| Ore | Formula | % Fe | Remark |
|---|---|---|---|
| **Haematite** | **Fe₂O₃** | 70 | red, chief ore |
| Magnetite | Fe₃O₄ | 72 | magnetic, richest |
| Siderite (spathic ore) | FeCO₃ | 48 | carbonate |
| Limonite | Fe₂O₃·3H₂O | 60 | hydrated, brown |
| Iron pyrite | FeS₂ | 47 | "fool's gold"; used for H₂SO₄, **not** for iron |

Iron pyrite is never used to make iron: the sulphur it leaves behind makes the
metal red-short, i.e. brittle when hot.

**1. Concentration.** Gravity separation (washing) for haematite; magnetic
separation for magnetite.

**2. Calcination and roasting.** Heating in a reverberatory furnace drives off
moisture and CO₂, burns away sulphur and arsenic as their oxides, and oxidises
FeO to Fe₂O₃, leaving the ore porous.

**3. Smelting in the blast furnace.** The charge is roasted ore, coke and
limestone in roughly the mass ratio 8 : 4 : 1, fed in at the top through a
cup-and-cone arrangement. A blast of air preheated to about 1000 K enters near
the bottom through **tuyères**. Four zones do four different jobs.

| Zone | Temperature | Chemistry |
|---|---|---|
| Combustion (bottom) | 1900 K | C + O₂ → CO₂ (exothermic); CO₂ + C → 2CO (endothermic) |
| Fusion | 1500 K | FeO + C → Fe + CO; spongy iron melts and dissolves carbon |
| Slag formation | 1200 K | CaCO₃ → CaO + CO₂; **CaO + SiO₂ → CaSiO₃** (slag) |
| Reduction (top) | 700–900 K | 3Fe₂O₃ + CO → 2Fe₃O₄ + CO₂; Fe₃O₄ + CO → 3FeO + CO₂; **FeO + CO → Fe + CO₂** |

Molten iron collects at the hearth and the lighter slag floats on it; both are
tapped separately. The product is **pig iron**, about 4% carbon, plus Si, Mn, P
and S. Remelting pig iron with scrap and coke in a cupola furnace gives **cast
iron**.

```figure caption="The blast furnace. The charge falls while the gases rise, so each zone meets the charge at the temperature that suits its reaction: reduction by carbon monoxide at the cool top, slag formation in the middle, and combustion at the tuyeres. Note that limestone is a flux, not a fuel — it converts the silica gangue into a fusible slag that floats on the molten iron."

import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.0, 4.5))
pts = [(2.0, -0.55), (2.0, 1.2), (1.35, 2.6), (1.35, 7.4), (1.9, 8.6),
       (4.1, 8.6), (4.65, 7.4), (4.65, 2.6), (4.0, 1.2), (4.0, -0.55)]
shell = Polygon(pts, closed=True, fc='none', ec=INK, lw=1.8, zorder=4)
clipper = Polygon(pts, closed=True, fc='none', ec='none')
ax.add_patch(clipper); ax.add_patch(shell)
bands = [(6.6, 8.6, '#e6ecf5', 'Zone of reduction', '700–900 K',
          '3Fe₂O₃ + CO → 2Fe₃O₄ + CO₂\nFe₃O₄ + CO → 3FeO + CO₂\nFeO + CO → Fe + CO₂'),
         (4.4, 6.6, '#efe9da', 'Zone of slag formation', '1200 K',
          'CaCO₃ → CaO + CO₂\nCaO + SiO₂ → CaSiO₃'),
         (2.4, 4.4, '#f6e1d9', 'Zone of fusion', '1500 K',
          'FeO + C → Fe + CO\nspongy iron melts, dissolves C'),
         (0.45, 2.4, '#f0cdbd', 'Zone of combustion', '1900 K',
          'C + O₂ → CO₂\nCO₂ + C → 2CO')]
for y0, y1, c, title, temp, eqs in bands:
    r = Rectangle((1.2, y0), 3.6, y1 - y0, fc=c, ec='none', zorder=1)
    ax.add_patch(r); r.set_clip_path(clipper)
    ax.plot([1.35, 4.65], [y1, y1], color=MUTED, lw=0.7, ls=':', zorder=3)
    yc = (y0 + y1) / 2
    ax.text(5.05, yc + 0.60, title, fontsize=8.0, color=INK, va='center')
    ax.text(5.05, yc + 0.20, temp, fontsize=7.6, color=SERIES[1], va='center')
    ax.text(5.05, yc - 0.42, eqs, fontsize=6.6, color=MUTED, va='center')
for y0, y1, c, lab in [(0.0, 0.45, '#c9b9a0', 'slag (CaSiO₃)'),
                       (-0.55, 0.0, '#8f8f97', 'molten pig iron (~4% C)')]:
    r = Rectangle((1.2, y0), 3.6, y1 - y0, fc=c, ec='none', zorder=1)
    ax.add_patch(r); r.set_clip_path(clipper)
ax.plot([2.0, 4.0], [0.0, 0.0], color=INK, lw=0.9, zorder=5)
ax.text(5.05, 0.22, 'slag  (CaSiO₃)', fontsize=7.4, color=INK, va='center')
ax.text(5.05, -0.33, 'molten pig iron (~4% C)', fontsize=7.4, color=INK, va='center')
ax.text(3.0, 9.55, 'charge:  ore : coke : limestone = 8 : 4 : 1',
        ha='center', fontsize=7.8, color=INK)
ax.add_patch(FancyArrowPatch((3.0, 9.35), (3.0, 8.72), arrowstyle='-|>',
                             color=INK, lw=1.3, mutation_scale=10))
ax.add_patch(FancyArrowPatch((1.5, 8.0), (0.55, 8.0), arrowstyle='-|>',
                             color=MUTED, lw=1.2, mutation_scale=9))
ax.text(0.05, 8.72, 'waste gas\n(CO, CO₂, N₂)', fontsize=7.2, color=MUTED,
        ha='left', va='bottom')
ax.add_patch(FancyArrowPatch((0.75, 0.75), (1.95, 0.75), arrowstyle='-|>',
                             color=SERIES[1], lw=1.4, mutation_scale=10))
ax.text(0.05, 0.55, 'hot air\nblast\n(1000 K)', fontsize=7.2,
        color=SERIES[1], ha='left', va='top')
ax.set_xlim(0.0, 9.3); ax.set_ylim(-1.5, 9.9); ax.axis('off')
```
### Properties and uses of iron

Pure iron is a lustrous, silvery-white, soft metal of density 7.86 g cm⁻³ and
melting point 1535 °C. It is strongly **ferromagnetic**.

| Reagent | Reaction |
|---|---|
| Dry air | no action |
| Moist air | rusting: hydrated Fe₂O₃·xH₂O |
| Air, strongly heated | 3Fe + 2O₂ → Fe₃O₄ |
| Steam, red heat (reversible) | 3Fe + 4H₂O ⇌ Fe₃O₄ + 4H₂ |
| Dilute HCl | Fe + 2HCl → FeCl₂ + H₂↑ |
| Dilute H₂SO₄ | Fe + H₂SO₄ → FeSO₄ + H₂↑ |
| Hot conc. H₂SO₄ | 2Fe + 6H₂SO₄ → Fe₂(SO₄)₃ + 3SO₂↑ + 6H₂O |
| Very dilute cold HNO₃ | 4Fe + 10HNO₃ → 4Fe(NO₃)₂ + NH₄NO₃ + 3H₂O |
| Conc. HNO₃ | **passivity** — a thin film of Fe₃O₄ stops all further attack |
| Cl₂, heated | 2Fe + 3Cl₂ → 2FeCl₃ |
| NaOH(aq) | no action — iron is not amphoteric |
| CuSO₄(aq) | Fe + CuSO₄ → FeSO₄ + Cu |

Note that dilute acids give **iron(II)**, while chlorine and hot concentrated
sulphuric acid give **iron(III)**: the halogen and the hot acid are the stronger
oxidising agents.

| Variety | Carbon | Properties and uses |
|---|---|---|
| Pig iron / cast iron | 2.5–4.5% | hard, brittle, cannot be forged; drain pipes, manhole covers, engine blocks, stoves |
| Wrought iron | below 0.25% | softest and purest, malleable, weldable; chains, hooks, ornamental gates, electromagnet cores |
| Steel | 0.25–1.5% | hard **and** tough, can be tempered; rods, girders, rails, tools, vehicles |

Iron is also essential biologically: an adult carries about 4 g, most of it in
the haem groups of haemoglobin, and iron-deficiency anaemia is Nepal's commonest
nutritional disorder.

### Manufacture of steel by the Basic Oxygen Method

Steel is iron with its carbon content cut to between 0.25% and 1.5%, and with
silicon, manganese, phosphorus and sulphur removed. The **Basic Oxygen Process**
(the LD or Linz–Donawitz process) now makes most of the world's steel.

- **Vessel.** A pear-shaped converter lined with a **basic** refractory
  (calcined dolomite, CaO·MgO) — basic because the impurity oxides SiO₂ and
  P₂O₅ that must be absorbed are acidic.
- **Charge.** Molten pig iron from the blast furnace, up to 30% scrap steel, and
  a measured amount of quicklime (CaO) as flux.
- **Blow.** A water-cooled lance is lowered to within a metre of the melt and
  99.5% pure oxygen is blown at about 10 atm for 20 minutes. No fuel is needed:
  the oxidation of the impurities supplies all the heat.

| Impurity | Oxidation | Fate of the oxide |
|---|---|---|
| Carbon | 2C + O₂ → 2CO↑ | burns off at the mouth as a flame |
| Silicon | Si + O₂ → SiO₂ | SiO₂ + CaO → CaSiO₃ (slag) |
| Manganese | 2Mn + O₂ → 2MnO | MnO + SiO₂ → MnSiO₃ (slag) |
| Phosphorus | 4P + 5O₂ → 2P₂O₅ | P₂O₅ + 3CaO → Ca₃(PO₄)₂ (slag, sold as fertiliser) |
| Sulphur | S + O₂ → SO₂↑ | escapes as gas |

When the carbon has fallen to the required level the blow is stopped and
calculated amounts of ferro-manganese or other alloying metals are added. One
charge of 300 tonnes takes about 40 minutes.

### Manufacture of steel by the Open Hearth Process

The **Open Hearth** or Siemens–Martin process is older and slower but gives far
better control of composition.

- **Vessel.** A shallow, saucer-shaped hearth of large surface area, lined with
  dolomite (basic hearth, for high-phosphorus pig iron) or silica (acid hearth,
  for low-phosphorus pig iron).
- **Heating.** Producer gas and preheated air are burnt over the surface of the
  charge. The hot waste gases pass through brick **regenerators**, which store
  the heat and give it back to the incoming air — the Siemens regenerative
  principle, which is what makes 1600 °C possible on an open hearth.
- **Oxidising agent.** Not an oxygen blast but **haematite added to the charge**.
  The iron(III) oxide burns out the impurities:

| Impurity | Reaction |
|---|---|
| Carbon | Fe₂O₃ + 3C → 2Fe + 3CO↑ |
| Silicon | 2Fe₂O₃ + 3Si → 4Fe + 3SiO₂ |
| Manganese | Fe₂O₃ + 3Mn → 2Fe + 3MnO |
| Phosphorus | 5Fe₂O₃ + 6P → 10Fe + 3P₂O₅ |

Lime is added as flux, and the SiO₂ and P₂O₅ pass into the slag as before. A
charge takes 8–10 hours, and because it is slow the operator can draw samples,
analyse them and adjust the melt — which is why alloy and tool steels are still
made this way.

| | Basic Oxygen Process | Open Hearth Process |
|---|---|---|
| Oxidant | pure O₂ blown through a lance | Fe₂O₃ (haematite) in the charge |
| Fuel | none needed | producer gas + regenerators |
| Time per charge | 20–40 min | 8–10 h |
| Control of composition | limited | excellent — samples can be taken |
| Nitrogen pick-up | very low (no air blown) | low |
| Typical product | plain carbon steel in bulk | alloy, tool and special steels |

**Heat treatment** finishes the job: *annealing* (heat, then cool very slowly)
softens steel and removes internal stress; *quenching* (heat, then plunge into
oil or water) makes it glass-hard but brittle; *tempering* (reheat the quenched
steel gently) restores toughness; *case hardening* gives a hard skin on a tough
core.

### Corrosion of iron and its prevention

**Rusting is an electrochemical process**, not simple oxidation. It needs
**both water and oxygen** — iron does not rust in dry air, nor under
air-free boiled water.

A single drop of water on an iron surface sets up a miniature galvanic cell. The
centre of the drop, starved of oxygen, becomes the **anode**; the rim, where
oxygen dissolves freely, becomes the **cathode**.

At the anode (oxidation): 2Fe → 2Fe²⁺ + 4e⁻

At the cathode (reduction): O₂ + 4H⁺ + 4e⁻ → 2H₂O

Overall: 2Fe + O₂ + 4H⁺ → 2Fe²⁺ + 2H₂O

The H⁺ comes from carbonic acid, since rainwater always carries dissolved CO₂.
The Fe²⁺ then diffuses out to the oxygen-rich rim and is oxidised further:

4Fe²⁺ + O₂ + 4H₂O → 2Fe₂O₃ + 8H⁺ , then Fe₂O₃ + xH₂O → **Fe₂O₃·xH₂O** (rust)

Rust is flaky and porous, so it does not protect the metal underneath — unlike
the oxide film on aluminium — and corrosion continues right through the object.

```figure caption="Rusting under a drop of water. The oxygen-starved centre of the drop becomes the anode and the oxygen-rich rim becomes the cathode; electrons travel through the metal itself. Rust therefore deposits in a ring at the edge of the drop, not where the metal is actually being eaten away."

import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.0, 3.2))
ax.add_patch(Rectangle((0.0, -1.0), 10.0, 1.0, fc='#b9bec7', ec=INK, lw=1.3))
ax.text(0.3, -0.85, 'iron', fontsize=8.2, color=INK, va='bottom')
th = np.linspace(0, np.pi, 240)
xd, yd = 5.0 + 3.1*np.cos(th), 1.30*np.sin(th)
ax.plot(xd, yd, color=ACCENT, lw=1.6)
ax.fill_between(xd, 0, yd, color=ACCENT, alpha=0.11)
ax.text(5.0, 1.92, 'water drop (dissolved O₂ and CO₂)',
        ha='center', fontsize=7.8, color=ACCENT)
ax.plot([4.55, 5.45], [0, 0], color=SERIES[1], lw=3.6, solid_capstyle='butt')
ax.text(5.0, 0.92, 'ANODE  (oxygen-poor)', ha='center', fontsize=7.5, color=SERIES[1])
ax.text(5.0, 0.58, '2Fe → 2Fe²⁺ + 4e⁻', ha='center', fontsize=7.6, color=INK)
for x in (2.35, 7.65):
    ax.plot([x - 0.55, x + 0.55], [0, 0], color=SERIES[2], lw=3.6, solid_capstyle='butt')
ax.annotate('CATHODE (oxygen-rich)\nO₂ + 4H⁺ + 4e⁻ → 2H₂O', (2.35, 0.05),
            textcoords='offset points', xytext=(-26, 52), fontsize=7.4,
            color=SERIES[2], ha='left',
            arrowprops=dict(arrowstyle='-|>', color=SERIES[2], lw=1.0, mutation_scale=8))
ax.annotate('rust ring\nFe₂O₃·xH₂O', (7.9, 0.05), textcoords='offset points',
            xytext=(22, 52), fontsize=7.4, color='#8a4a22', ha='left',
            arrowprops=dict(arrowstyle='-|>', color='#8a4a22', lw=1.0, mutation_scale=8))
for a, b in [((4.5, -0.3), (2.6, -0.3)), ((5.5, -0.3), (7.4, -0.3))]:
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle='-|>', color=SERIES[4], lw=1.3,
                                 mutation_scale=9, connectionstyle='arc3,rad=0.25'))
ax.text(3.55, -0.78, 'e⁻ through the metal', fontsize=7.4, color=SERIES[4], ha='center')
ax.text(6.45, -0.78, 'e⁻', fontsize=7.8, color=SERIES[4], ha='center')
ax.set_xlim(-0.3, 10.9); ax.set_ylim(-1.3, 2.8); ax.axis('off')
```
**Factors that speed up rusting:** presence of moisture and oxygen; dissolved
CO₂, acids and especially **salts** (sea air, road salt) because they raise the
conductivity of the electrolyte; contact with a less reactive metal; impurities
and strains in the metal; and rough or scratched surfaces.

**Prevention.**

| Method | How it works | Example |
|---|---|---|
| Barrier coating | keeps out air and water | paint, grease, oil, enamel, plastic |
| **Galvanising** | zinc coat; zinc is more electropositive, so it corrodes first even if the coat is scratched | roofing sheet, buckets, nails |
| Tinning | tin coat, purely a barrier | food cans |
| Electroplating | Cr, Ni or Cu deposited electrolytically | taps, cycle parts |
| **Cathodic (sacrificial) protection** | blocks of Mg or Zn wired to the iron corrode instead | ship hulls, buried pipelines, water tanks |
| Alloying | the alloy carries its own passive film | stainless steel: Fe + 18% Cr + 8% Ni |
| Passivation | a chemically grown oxide or phosphate film | phosphating of car bodies before painting |

::: caution Galvanising protects a scratch; tinning does not
Both coatings work while they are unbroken. Scratch a galvanised sheet and the
zinc, being **more** electropositive than iron, still corrodes first and the
iron is safe. Scratch a tinned can and the iron, being **more** electropositive
than tin, becomes the anode — so a scratched tin can rusts *faster* than plain
iron. This comparison is a standard 2-mark question.
:::

::: example Worked example 7.4
**Problem.** A basic oxygen converter is charged with 100 tonnes of pig iron
containing 4.0% carbon, which must be brought down to 0.4% carbon. Calculate the
volume of oxygen at STP needed to remove this carbon, assuming it is all
oxidised to carbon monoxide. (C = 12, molar volume at STP = 22.4 L mol⁻¹)

**Solution.** Carbon to be removed:

$$ m(\text{C}) = 100\ \text{t}\times(0.040 - 0.004) = 3.6\ \text{t} = 3.6\times 10^{6}\ \text{g} $$

$$ n(\text{C}) = \frac{3.6\times10^{6}}{12} = 3.0\times10^{5}\ \text{mol} $$

From 2C + O₂ → 2CO, one mole of O₂ is needed for every two moles of carbon:

$$ n(\text{O}_2) = \tfrac{1}{2}\times 3.0\times10^{5} = 1.5\times10^{5}\ \text{mol} $$

$$ V = 1.5\times10^{5}\times 22.4 = 3.36\times10^{6}\ \text{L} = 3360\ \text{m}^{3} $$
:::

## 7.5 Silver

Silver is the best conductor of heat and electricity of all metals, and the
metal of Nepali jewellery, ritual vessels and the old *mohar* coinage. Almost
all of it today comes as a by-product of lead, zinc and copper refining rather
than from a silver mine.

### Occurrence and extraction by the cyanide process

| Ore | Formula |
|---|---|
| Native silver | Ag |
| **Argentite (silver glance)** | **Ag₂S** |
| Horn silver | AgCl |
| Ruby silver (pyrargyrite) | Ag₃SbS₃ |
| Anode mud of copper refining | mixed Ag, Au, Pt |

The **cyanide process** (the MacArthur–Forrest process) extracts silver from
argentite in three steps.

**1. Concentration** of the crushed ore by froth flotation.

**2. Leaching with sodium cyanide.** The concentrate is stirred with a dilute
(0.1–0.5%) solution of sodium cyanide while air is blown through:

**Ag₂S + 4NaCN ⇌ 2Na[Ag(CN)₂] + Na₂S**

The reaction is reversible and would stop early, so the sodium sulphide is
continuously destroyed by the air blast:

2Na₂S + 2O₂ + H₂O → Na₂S₂O₃ + 2NaOH

Removing a product pulls the equilibrium to the right — Le Chatelier's principle
doing real industrial work. The silver is now in solution as the soluble
complex **sodium dicyanoargentate(I)**.

**3. Precipitation with zinc.** Scrap zinc dust is added to the filtered
solution. Zinc is more electropositive than silver, so it displaces it:

**2Na[Ag(CN)₂] + Zn → Na₂[Zn(CN)₄] + 2Ag↓**

**4. Refining.** The spongy silver is purified electrolytically by the **Moebius
process**: a plate of impure silver is the anode, a sheet of pure silver the
cathode, and the electrolyte is silver nitrate acidified with 1% nitric acid.
Pure silver falls as crystals into a canvas bag hung beneath the anode; gold and
platinum stay in the anode mud. The product is 99.9% pure.

::: key Why cyanide, of all things
Cyanide is used because Ag⁺ forms an exceptionally stable complex with CN⁻.
Complex formation lowers the concentration of free Ag⁺ so far that even an
insoluble sulphide is forced into solution. The same trick is used for gold.
The price is a lethally toxic effluent, which is why cyanide leaching is tightly
regulated.
:::

Silver is a white, lustrous, very malleable and ductile metal (m.p. 961 °C,
density 10.5 g cm⁻³). It is unaffected by air and water, but is **tarnished
black by hydrogen sulphide** in polluted air:

4Ag + 2H₂S + O₂ → 2Ag₂S + 2H₂O

It does not react with dilute hydrochloric or sulphuric acid, but dissolves in
nitric acid and in hot concentrated sulphuric acid.

### Preparation and uses of silver nitrate

Silver nitrate, AgNO₃, is called **lunar caustic** — *luna* was the alchemists'
name for silver, and the solid cauterises skin.

**Preparation.** Dissolve pure silver in nitric acid and evaporate:

3Ag + 4HNO₃(dilute) → 3AgNO₃ + NO↑ + 2H₂O

Ag + 2HNO₃(conc.) → AgNO₃ + NO₂↑ + H₂O

If the silver contained copper, the crystals are heated to about 450 °C: the
copper nitrate decomposes to black insoluble CuO while silver nitrate is
unaffected, and the salt is then extracted with water.

**Properties.**

| Reagent | Observation | Equation |
|---|---|---|
| Heat, 450 °C then higher | melts, then decomposes | 2AgNO₃ → 2Ag + 2NO₂↑ + O₂↑ |
| NaOH | brown precipitate (not the hydroxide) | 2AgNO₃ + 2NaOH → Ag₂O↓ + 2NaNO₃ + H₂O |
| NH₃, excess | colourless solution — **Tollens' reagent** | Ag₂O + 4NH₃ + H₂O → 2[Ag(NH₃)₂]OH |
| NaCl | white curdy precipitate | AgNO₃ + NaCl → AgCl↓ + NaNO₃ |
| KBr | pale yellow precipitate | AgNO₃ + KBr → AgBr↓ + KNO₃ |
| KI | yellow precipitate | AgNO₃ + KI → AgI↓ + KNO₃ |
| K₂CrO₄ | brick-red precipitate | 2AgNO₃ + K₂CrO₄ → Ag₂CrO₄↓ + 2KNO₃ |
| Organic matter / skin | black stain of finely divided silver | reduction of Ag⁺ to Ag |

**Uses.** Making the silver halides for photographic film and paper; indelible
marking ink and hair dye; **Tollens' reagent** for the silver-mirror test on
aldehydes; the standard reagent for detecting halide ions; argentometric
titration (Mohr's and Volhard's methods); silver plating; and as a caustic and
antiseptic in medicine.

### Preparation and uses of silver chloride

Silver chloride, AgCl, occurs naturally as **horn silver**.

**Preparation.** By adding any soluble chloride to a silver nitrate solution:

AgNO₃ + NaCl → AgCl↓ + NaNO₃

or by dissolving silver oxide in hydrochloric acid: Ag₂O + 2HCl → 2AgCl + H₂O.

**Properties.** A white **curdy** precipitate, insoluble in water and in dilute
nitric acid, which fuses at 455 °C to a horn-like mass. Its three examinable
reactions are all dissolutions, and all three are complex formation:

| Reagent | Result |
|---|---|
| NH₃(aq) | AgCl + 2NH₃ → [Ag(NH₃)₂]Cl (dissolves; AgBr dissolves only partly, AgI not at all) |
| Na₂S₂O₃ ("hypo") | AgCl + 2Na₂S₂O₃ → Na₃[Ag(S₂O₃)₂] + NaCl — this is photographic **fixing** |
| KCN | AgCl + 2KCN → K[Ag(CN)₂] + KCl |

Exposed to light it slowly turns violet then grey as it decomposes:

2AgCl --light--> 2Ag + Cl₂↑

This photosensitivity is the whole basis of film photography, and of
photochromic (self-darkening) spectacle lenses.

**Uses.** Photography and photochromic glass; the **Ag/AgCl reference
electrode**, the electrode inside most pH probes and ECG pads; preparing pure
silver; and as an antiseptic in some dressings.

::: example Worked example 7.5
**Problem.** In the cyanide process, a leach solution contains 0.500 mol of
sodium dicyanoargentate(I), Na[Ag(CN)₂]. Calculate (a) the minimum mass of zinc
dust required to precipitate all the silver, and (b) the mass of silver
obtained. (Zn = 65.4, Ag = 108)

**Solution.** The equation is

2Na[Ag(CN)₂] + Zn → Na₂[Zn(CN)₄] + 2Ag

(a) The ratio of complex to zinc is 2 : 1, so

$$ n(\text{Zn}) = \frac{0.500}{2} = 0.250\ \text{mol},\qquad
m = 0.250\times65.4 = 16.35\ \text{g} $$

(b) The ratio of complex to silver is 1 : 1, so $n(\text{Ag}) = 0.500\ \text{mol}$ and

$$ m = 0.500 \times 108 = 54.0\ \text{g of silver} $$
:::

### Tests for the five metal ions at a glance

| Ion | With NaOH | With excess NaOH | With NH₃(aq), excess | Other test |
|---|---|---|---|---|
| Cu²⁺ | blue precipitate | insoluble | **deep blue** solution | black CuS with H₂S |
| Zn²⁺ | white precipitate | **dissolves** (zincate) | dissolves, colourless | white ZnS in alkaline medium |
| Hg²⁺ | yellow HgO | insoluble | white Hg(NH₂)Cl | SnCl₂: white → grey |
| Fe²⁺ | dirty green precipitate | insoluble | dirty green | K₃[Fe(CN)₆] gives deep blue |
| Fe³⁺ | reddish-brown precipitate | insoluble | reddish-brown | KSCN gives blood-red |
| Ag⁺ | brown Ag₂O | insoluble | dissolves (Tollens') | white AgCl, soluble in NH₃ |

## Chapter summary

- **Copper** comes from copper pyrite, CuFeS₂: froth flotation → roasting →
  smelting with silica (FeSiO₃ slag, Cu₂S + FeS matte) → bessemerisation, where
  **2Cu₂O + Cu₂S → 6Cu + SO₂** gives blister copper by auto-reduction → poling
  and electrolytic refining (anode mud holds Ag, Au, Pt).
- Copper is unattacked by dilute HCl or H₂SO₄ but dissolves in HNO₃ and in hot
  conc. H₂SO₄; with aqueous ammonia and air it gives deep blue
  [Cu(NH₃)₄](OH)₂, Schweitzer's reagent. Blue vitriol is
  [Cu(H₂O)₄]SO₄·H₂O, white when anhydrous. Cu₂O is the red oxide, CuO the black.
- **Zinc** comes from zinc blende, ZnS: flotation → roasting (2ZnS + 3O₂ →
  2ZnO + 2SO₂) → reduction with coke (**ZnO + C → Zn + CO**), the zinc distilling
  off as vapour. Zinc is **amphoteric**: it gives H₂ with both dilute acid and
  hot alkali. White vitriol is ZnSO₄·7H₂O.
- **Mercury** comes from cinnabar, HgS, by roasting alone: **HgS + O₂ → Hg +
  SO₂**, because HgO decomposes on heating. Excess mercury gives mercurous
  (Hg₂²⁺) salts, excess acid or halogen gives mercuric (Hg²⁺) salts.
  Calomel Hg₂Cl₂ is white, insoluble, harmless and **blackened by ammonia**;
  corrosive sublimate HgCl₂ is soluble, covalent and poisonous, and gives a
  white precipitate with ammonia and a scarlet one with KI that dissolves in
  excess KI to Nessler's reagent.
- **Iron** comes from haematite Fe₂O₃ in the blast furnace, the key step being
  **FeO + CO → Fe + CO₂**, with limestone as flux giving CaSiO₃ slag; the
  product is pig iron with ~4% C. Conc. HNO₃ makes iron **passive**.
- Steel: the **Basic Oxygen Process** burns the impurities out with a lance of
  pure O₂ in 20 minutes, no fuel; the **Open Hearth Process** uses haematite as
  the oxidant and regenerative heating over 8–10 hours, with much better control
  of composition.
- **Rusting** is electrochemical and needs water *and* oxygen: anode
  2Fe → 2Fe²⁺ + 4e⁻, cathode O₂ + 4H⁺ + 4e⁻ → 2H₂O, product Fe₂O₃·xH₂O.
  Galvanising protects even when scratched; tinning does not.
- **Silver** is extracted by the cyanide process:
  Ag₂S + 4NaCN ⇌ 2Na[Ag(CN)₂] + Na₂S, then
  2Na[Ag(CN)₂] + Zn → Na₂[Zn(CN)₄] + 2Ag, then Moebius electrolytic refining.
  AgNO₃ is lunar caustic; AgCl is a white curdy precipitate soluble in ammonia
  and in hypo, and darkens in light.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The chief ore of copper is <span class="marks">[1]</span>
   (a) cuprite (b) malachite (c) copper pyrite (d) copper glance
2. In the bessemerisation of copper matte, copper is finally obtained by <span class="marks">[1]</span>
   (a) reduction with coke (b) reduction with carbon monoxide (c) auto-reduction (d) electrolysis
3. The metal extracted by roasting its ore alone, with no reducing agent, is <span class="marks">[1]</span>
   (a) zinc (b) mercury (c) iron (d) copper
4. Which of the following dissolves in both dilute hydrochloric acid and hot sodium hydroxide solution? <span class="marks">[1]</span>
   (a) Cu (b) Ag (c) Zn (d) Hg
5. Concentrated nitric acid has no visible action on iron because <span class="marks">[1]</span>
   (a) iron is a noble metal (b) a protective film of Fe₃O₄ is formed (c) iron is amphoteric (d) the acid is too concentrated to ionise
6. Ammonia solution turns calomel black because it forms <span class="marks">[1]</span>
   (a) HgO (b) HgS (c) finely divided mercury (d) Hg(NH₃)₂Cl₂
7. In the cyanide process the silver is finally precipitated by <span class="marks">[1]</span>
   (a) copper (b) zinc (c) iron (d) sodium
8. Anhydrous copper sulphate is <span class="marks">[1]</span>
   (a) blue (b) green (c) white (d) black
9. The flux used in the blast furnace extraction of iron is <span class="marks">[1]</span>
   (a) silica (b) limestone (c) coke (d) dolomite

::: note Answers to Group A
**1.** (c) — copper pyrite, CuFeS₂, supplies about three-quarters of the world's copper.

**2.** (c) — 2Cu₂O + Cu₂S → 6Cu + SO₂; the ore reduces itself.

**3.** (b) — HgS + O₂ → Hg + SO₂, because HgO decomposes on heating.

**4.** (c) — zinc is amphoteric and gives H₂ with acid and with alkali.

**5.** (b) — passivity; the film is coherent and stops further attack.

**6.** (c) — Hg₂Cl₂ + 2NH₃ → Hg(NH₂)Cl + **Hg** + NH₄Cl.

**7.** (b) — zinc is more electropositive: 2Na[Ag(CN)₂] + Zn → Na₂[Zn(CN)₄] + 2Ag.

**8.** (c) — white, and it turns blue with water; this is the test for water.

**9.** (b) — limestone gives CaO, which removes the silica gangue as CaSiO₃.
:::

**Group B — Short answer (5 marks each)**

1. Describe the extraction of copper from copper pyrite up to the stage of
   blister copper. Give balanced equations for roasting, smelting and
   bessemerisation, and state the role of silica. <span class="marks">[5]</span>
2. How is zinc extracted from zinc blende? Why must the ore be roasted before
   reduction, and why is the zinc obtained as a vapour? <span class="marks">[5]</span>
3. What happens when (a) copper is left in moist air containing CO₂,
   (b) copper is warmed with aqueous ammonia in the presence of air,
   (c) copper is added to iron(III) chloride solution? Give equations. <span class="marks">[5]</span>
4. Explain, with equations, the action of heat on blue vitriol. Why is the
   formula of the pentahydrate better written [Cu(H₂O)₄]SO₄·H₂O? <span class="marks">[5]</span>
5. Distinguish between calomel and corrosive sublimate under four headings, and
   give one chemical test that separates them. <span class="marks">[5]</span>
6. 24.95 g of blue vitriol is heated to 230 °C. Calculate the mass of the
   residue and the volume of water vapour released at STP.
   (Cu = 63.5, S = 32, O = 16, H = 1) <span class="marks">[5]</span>
7. Explain the electrochemical theory of rusting. Why does a scratched
   galvanised sheet still resist rust while a scratched tinned can does
   not? <span class="marks">[5]</span>

::: note Answers to Group B
**2.** Concentration by froth flotation; roasting 2ZnS + 3O₂ → 2ZnO + 2SO₂;
reduction ZnO + C → Zn + CO at 1673 K in fireclay retorts; refining by
liquation, distillation or electrolysis. Carbon has no affinity for sulphur and
cannot reduce ZnS, so the sulphide must first become the oxide. Zinc boils at
907 °C, well below the 1400 °C of the retort, so it leaves as vapour and is
condensed out of contact with air — otherwise it would re-oxidise to ZnO.

**5.**

| | Calomel Hg₂Cl₂ | Corrosive sublimate HgCl₂ |
|---|---|---|
| Oxidation state | Hg(I), with an Hg–Hg bond | Hg(II) |
| Solubility in water | insoluble | soluble |
| Toxicity | non-poisonous | violent poison |
| With NH₃ | turns **black** (free Hg) | **white** precipitate Hg(NH₂)Cl |

Test: add ammonia solution. Blackening proves calomel.

**6.** $n = 24.95/249.5 = 0.100\ \text{mol}$. Heating to 230 °C removes all five
waters, so the residue is anhydrous CuSO₄:

$$ m = 0.100 \times 159.5 = 15.95\ \text{g} $$

Water released $= 0.100\times5 = 0.500\ \text{mol}$, so at STP

$$ V = 0.500 \times 22.4 = 11.2\ \text{L} $$

**7.** A water film containing dissolved O₂ and CO₂ makes the iron surface a
galvanic cell. Oxygen-poor areas are anodic, 2Fe → 2Fe²⁺ + 4e⁻; oxygen-rich
areas are cathodic, O₂ + 4H⁺ + 4e⁻ → 2H₂O. The Fe²⁺ is oxidised further,
4Fe²⁺ + O₂ + 4H₂O → 2Fe₂O₃ + 8H⁺, and the oxide hydrates to rust Fe₂O₃·xH₂O.
Zinc (E° = −0.76 V) is more electropositive than iron (−0.44 V), so at a scratch
the zinc becomes the anode and corrodes *instead of* the iron — sacrificial
protection. Tin (−0.14 V) is **less** electropositive than iron, so at a scratch
the iron becomes the anode of a small cell and corrodes faster than it would on
its own.
:::

**Group C — Long answer (8 marks each)**

1. (a) Describe the manufacture of steel by the Basic Oxygen Process, with the
   equations for the removal of carbon, silicon and phosphorus, and state the
   function of the lime. <span class="marks">[5]</span>
   (b) Compare the Basic Oxygen Process with the Open Hearth Process under
   three headings. <span class="marks">[3]</span>
2. (a) Describe the extraction of silver from argentite by the cyanide process,
   with equations, and explain why air is blown through the leach
   solution. <span class="marks">[5]</span>
   (b) How is silver chloride prepared? Give its action with aqueous ammonia,
   with sodium thiosulphate and with light. <span class="marks">[3]</span>
3. An ore contains 25.0% copper pyrite by mass. Calculate (a) the percentage of
   copper in pure CuFeS₂, (b) the mass of copper in 2.00 tonnes of the ore, and
   (c) the mass of blister copper (98% pure) that this would give at 85%
   recovery. (Cu = 63.5, Fe = 56, S = 32) <span class="marks">[8]</span>

::: note Answers to Group C
**1.(a)** A pear-shaped converter lined with basic dolomite is charged with
molten pig iron, up to 30% scrap and quicklime. A water-cooled lance blows
99.5% oxygen at ~10 atm for about 20 minutes; the heat of oxidation of the
impurities keeps the charge molten, so no fuel is burnt.
2C + O₂ → 2CO↑ (burns off at the mouth); Si + O₂ → SiO₂;
4P + 5O₂ → 2P₂O₅. The lime is a **basic flux** that absorbs these acidic
oxides: SiO₂ + CaO → CaSiO₃ and P₂O₅ + 3CaO → Ca₃(PO₄)₂, both of which float
off as slag. Alloying metals such as ferro-manganese are added at the end.

**1.(b)** Oxidant: pure O₂ blown in, versus haematite added to the charge.
Time: 20–40 minutes, versus 8–10 hours. Control: limited, versus excellent —
the open hearth can be sampled and corrected, so it is preferred for alloy and
tool steels.

**2.(a)** Flotation concentrates the argentite. Leaching with 0.1–0.5% NaCN in
a current of air gives the soluble complex,
Ag₂S + 4NaCN ⇌ 2Na[Ag(CN)₂] + Na₂S. The reaction is reversible; the air
oxidises the sodium sulphide away, 2Na₂S + 2O₂ + H₂O → Na₂S₂O₃ + 2NaOH, so by
Le Chatelier's principle the equilibrium is driven to the right. The filtered
solution is treated with zinc dust,
2Na[Ag(CN)₂] + Zn → Na₂[Zn(CN)₄] + 2Ag↓, and the spongy silver is refined
electrolytically (Moebius process) with an impure silver anode, a pure silver
cathode and AgNO₃ + 1% HNO₃ as electrolyte.

**2.(b)** AgNO₃ + NaCl → AgCl↓ + NaNO₃, a white curdy precipitate.
With ammonia it dissolves: AgCl + 2NH₃ → [Ag(NH₃)₂]Cl. With hypo it dissolves:
AgCl + 2Na₂S₂O₃ → Na₃[Ag(S₂O₃)₂] + NaCl (photographic fixing). In light it
darkens: 2AgCl → 2Ag + Cl₂.

**3.** (a) $M(\text{CuFeS}_2) = 63.5+56+64 = 183.5$, so

$$ \%\,\text{Cu} = \frac{63.5}{183.5}\times100 = 34.60\% $$

(b) Copper in the ore $= 0.250\times34.60\% = 8.65\%$, so in 2000 kg

$$ m = 2000\times0.0865 = 173\ \text{kg} $$

(c) Copper actually recovered $= 0.85\times173 = 147.1\ \text{kg}$. Since
blister copper is only 98% copper, the mass of blister copper is

$$ m = \frac{147.1}{0.98} = 150.1\ \text{kg} \approx 150\ \text{kg} $$
:::
