---
subject: Chemistry
grade: 11
unit: 11
title: Bio-inorganic Chemistry
hours: 3
area: Inorganic Chemistry
---

Life is usually taught as the chemistry of carbon, but no cell could work on
carbon alone. Roughly a quarter of all known enzymes need a metal ion to
function, oxygen is carried through your blood on an iron atom, and the electrical
signal running along a nerve is nothing but sodium and potassium ions moving
across a membrane. **Bio-inorganic chemistry** is the study of the role that
metal ions and other inorganic species play in living systems — and of what goes
wrong when the wrong metal, or too much of the right one, gets in.

::: key What the examiner asks from this unit
This is a short, high-yield unit. Learn (i) the macro/micro nutrient boundary and
which elements fall on each side; (ii) one biological function for each of the
ten metals named in the syllabus; (iii) the stoichiometry of the two pumps
(3 Na⁺ out, 2 K⁺ in per ATP; 2 Na⁺ in per glucose); (iv) the disease caused by
each toxic metal and the reason it is toxic.
:::

## 11.1 Introduction

Bio-inorganic chemistry sits between inorganic chemistry and biochemistry. It
asks three questions:

1. **Which** inorganic elements does an organism need, and how much of each?
2. **What** does each one actually do — is it a structural part, a charge
   carrier, or a catalyst?
3. **Why** are some metals poisonous, and how can the poisoning be reversed?

Only about 25 of the 118 elements are essential to the human body, and just 11 of
them make up 99.9% of its mass. An element is called **essential** if its removal
from the diet causes a definite deficiency disorder that is cured when the
element — and only that element — is put back.

Nature has picked its elements for good chemical reasons. Sodium and potassium
are used for electrical work because their ions are soluble, do not form strong
complexes, and move fast. Iron, copper, cobalt and manganese are used for
catalysis because they have *variable oxidation states* and can accept or donate
electrons. Zinc, which has only one oxidation state and no colour, is used where
a strong but redox-inert Lewis acid is required. Calcium, abundant and giving
very insoluble salts, is used for structure.

## 11.2 Micro and macro nutrients

Nutrients are classified by the **quantity** the body requires, not by their
importance — a deficiency of a micronutrient can be just as fatal as one of a
macronutrient.

::: definition Macronutrients and micronutrients
**Macronutrients** are elements required in relatively large quantities, more
than about 100 mg per day, each making up more than 0.01% of the body mass.
**Micronutrients (trace elements)** are required in quantities less than about
100 mg per day and make up less than 0.01% of the body mass.
:::

| | Elements | Approximate share of body mass |
|---|---|---|
| Major macronutrients | O, C, H, N | 96.2% |
| Mineral macronutrients | Ca, P, K, S, Na, Cl, Mg | 3.7% |
| Micronutrients (trace) | Fe, Zn, Cu, Mn, I, F, Se, Cr, Co, Mo, Ni, V | about 0.01% |

```figure caption="Elemental composition of the adult human body by mass. The dashed line at 0.01% is the conventional boundary between macronutrients and micronutrients; note the logarithmic scale."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.1,2.9))
el   = ['O','C','H','N','Ca','P','K','S','Na','Cl','Mg','Fe','Zn','Cu','I','Se','Cr','Co']
pct  = [65, 18.5, 9.5, 3.2, 1.5, 1.0, 0.40, 0.30, 0.20, 0.20, 0.10,
        6.0e-3, 3.3e-3, 1.0e-4, 2.0e-5, 1.9e-5, 2.4e-6, 2.1e-6]
cols = [ACCENT]*11 + ['#d9534f']*7
ax.bar(np.arange(len(el)), pct, color=cols, width=0.68)
ax.set_yscale('log')
ax.set_xticks(np.arange(len(el))); ax.set_xticklabels(el, fontsize=8.0)
ax.set_ylabel('share of body mass / %')
ax.set_ylim(5e-7, 4e2)
ax.axhline(1e-2, color=MUTED, lw=1.0, ls=(0,(4,3)))
ax.text(17.4, 1.6e-2, '0.01%', fontsize=7.6, color=MUTED, ha='right', va='bottom')
ax.text(5.0, 1.2e2, 'macronutrients', fontsize=8.4, color=ACCENT, ha='center')
ax.text(14.3, 1.2e2, 'micronutrients', fontsize=8.4, color='#d9534f', ha='center')
ax.spines[['top','right']].set_visible(False)
ax.grid(True, axis='y', alpha=0.5)
```

For **plants** the same division is used but the list differs slightly.
Macronutrients: C, H, O, N, P, K, Ca, Mg, S. Micronutrients: Fe, Mn, Zn, Cu, B,
Mo, Cl, Ni. This is why the fertiliser bags sold in Nepal are labelled with an
N : P : K ratio — those are the three macronutrients that Terai soils run short
of first.

::: caution "Trace" does not mean "optional"
Cobalt makes up about two parts per billion of the body, yet without it vitamin
B₁₂ cannot be made and the person develops pernicious anaemia. Iodine is needed
at roughly 150 μg per day, yet its absence causes goitre — the reason salt sold
in Nepal is iodised by law.
:::

## 11.3 Importance of metal ions in biological systems

| Metal | Ion(s) | Where it is found | What it does |
|---|---|---|---|
| Sodium | Na⁺ | chief **extracellular** cation (about 145 mM outside, 12 mM inside the cell) | osmotic and fluid balance, blood pressure, transmission of the nerve impulse, drives the uptake of glucose and amino acids |
| Potassium | K⁺ | chief **intracellular** cation (about 140 mM inside, 4 mM outside) | maintains the resting membrane potential, activates enzymes such as pyruvate kinase, controls heart rhythm |
| Magnesium | Mg²⁺ | chlorophyll; bound to ATP; ribosomes | the central atom of chlorophyll, so all photosynthesis depends on it; every kinase works on Mg–ATP, not free ATP; stabilises DNA and ribosomes |
| Calcium | Ca²⁺ | bone and teeth as hydroxyapatite Ca₅(PO₄)₃OH; blood plasma | skeletal structure; blood clotting; muscle contraction; acts as a second messenger in cell signalling |
| Iron | Fe²⁺/Fe³⁺ | haemoglobin, myoglobin, cytochromes, catalase, ferritin | carries O₂ in blood and stores it in muscle; transfers electrons in the respiratory chain; destroys H₂O₂ (catalase) |
| Copper | Cu⁺/Cu²⁺ | cytochrome c oxidase, superoxide dismutase, tyrosinase, plastocyanin, haemocyanin | the terminal step of respiration; removal of the superoxide radical; melanin formation; O₂ transport in molluscs and crabs (blue blood) |
| Zinc | Zn²⁺ | carbonic anhydrase, carboxypeptidase, alcohol dehydrogenase, zinc-finger proteins, insulin crystals | a redox-inert Lewis acid in over 300 enzymes; carbonic anhydrase speeds up CO₂ + H₂O ⇌ H⁺ + HCO₃⁻ about a million-fold; zinc fingers grip DNA |
| Nickel | Ni²⁺ | urease, hydrogenase | urease hydrolyses urea, NH₂CONH₂ + H₂O → 2NH₃ + CO₂; urease was the first enzyme ever crystallised |
| Cobalt | Co³⁺ | vitamin B₁₂ (cyanocobalamin), held in a corrin ring | formation of red blood cells and of the myelin sheath; its absence causes pernicious anaemia |
| Chromium | Cr³⁺ | glucose tolerance factor | helps insulin bind to its receptor, so it assists glucose uptake. Note that Cr(VI), as in chromate, is toxic and carcinogenic |

### Iron and the haem group

Haemoglobin is the best-studied bio-inorganic molecule. It is a protein of molar
mass about 64 500 g mol⁻¹ built from four subunits, each holding one flat
**haem** group. In each haem an Fe²⁺ ion sits at the centre of a **porphyrin
ring**, bonded to the four nitrogen atoms of the ring. A fifth position below the
plane is occupied by a nitrogen atom of a histidine residue of the protein, and
the sixth position above the plane is left free — that is where the O₂ molecule
binds, reversibly:

Hb + 4O₂ ⇌ Hb(O₂)₄

The binding must be *reversible*: O₂ is picked up in the lungs, where its partial
pressure is high, and released in the tissues, where it is low. Carbon monoxide
is poisonous precisely because it binds to the same site about 250 times more
strongly and does **not** let go, so the haemoglobin is taken out of service.
Note that the iron stays as Fe²⁺ throughout; if it is oxidised to Fe³⁺ the
product (methaemoglobin) cannot carry oxygen at all.

```figure caption="The haem group. Fe²⁺ is held by the four nitrogen atoms of the porphyrin ring, by a histidine nitrogen below the plane, and binds O₂ reversibly at the sixth site above the plane."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,3.1))

# porphyrin ring drawn in perspective as a rhombus
N = [(-1.55,0.0),(0.0,0.62),(1.55,0.0),(0.0,-0.62)]
ring = np.array(N + [N[0]])
ax.plot(ring[:,0], ring[:,1], color=MUTED, lw=1.3, ls='-')
# the four bridging methine carbons bulge the ring outwards
for (x1,y1),(x2,y2) in zip(N, N[1:]+N[:1]):
    mx, my = (x1+x2)/2, (y1+y2)/2
    ax.plot([mx*1.22],[my*1.22], marker='o', ms=3.0, color=MUTED)
    ax.plot([x1, mx*1.22, x2],[y1, my*1.22, y2], color=MUTED, lw=1.3)

# Fe centre and equatorial bonds
for (x,y) in N:
    ax.plot([0,x],[0,y], color=INK, lw=1.4)
    ax.plot([x],[y], marker='o', ms=9.5, color='#ffffff', zorder=3)
    ax.text(x, y, 'N', fontsize=8.6, color='#1d6fb8', ha='center', va='center', zorder=4)
ax.plot([0],[0], marker='o', ms=20, color='#b8860b', zorder=3)
ax.text(0,0,'Fe²⁺', fontsize=8.4, color='#ffffff', ha='center', va='center',
        zorder=4, fontweight='bold')

# axial ligands
ax.plot([0,0.0],[0,1.62], color=INK, lw=1.4, ls=(0,(3,2)))
ax.plot([0],[1.62], marker='o', ms=8, color='#d9534f', zorder=3)
ax.text(0.16,1.68,'O₂  (binds reversibly)', fontsize=8.0, color='#d9534f',
        ha='left', va='center')
ax.plot([0,0.0],[0,-1.62], color=INK, lw=1.4, ls=(0,(3,2)))
ax.plot([0],[-1.62], marker='o', ms=8.5, color='#2e8b57', zorder=3)
ax.text(0.16,-1.70,'N of histidine (globin chain)', fontsize=8.0, color='#2e8b57',
        ha='left', va='center')

ax.text(-2.55,0.90,'porphyrin\nring', fontsize=8.0, color=MUTED, ha='center',
        va='center', linespacing=1.3)
ax.annotate('', xy=(-1.30,0.52), xytext=(-2.30,0.75),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.0, mutation_scale=9))
ax.text(0.0,-2.28,'Hb + 4O₂  ⇌  Hb(O₂)₄', fontsize=8.6, color=INK, ha='center')

ax.set_xlim(-3.3,3.3); ax.set_ylim(-2.55,2.25); ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 11.1
**Problem.** Haemoglobin has a molar mass of 64 500 g mol⁻¹ and contains four
atoms of iron per molecule. (a) Calculate the percentage of iron in haemoglobin.
(b) An adult carries about 750 g of haemoglobin. What mass of iron is that?
(Fe = 55.85)

**Solution.**

(a) Mass of iron in one mole of haemoglobin $= 4 \times 55.85 = 223.4\ \text{g}$.

$$ \%\,\text{Fe} = \frac{223.4}{64\,500}\times 100 = 0.346\% $$

(b) $m(\text{Fe}) = 750 \times \dfrac{0.346}{100} = 2.60\ \text{g}$

That is about two-thirds of the roughly 4 g of iron in the whole body — which is
why blood loss so quickly causes iron-deficiency anaemia.
:::

## 11.4 Ion pumps

A cell membrane is a lipid bilayer, and ions cannot cross it on their own. The
concentrations of Na⁺ and K⁺ inside a cell are very different from those outside,
and the difference is *not* an equilibrium — it is maintained continuously by
protein machines called **pumps**, at a cost of energy.

::: definition Active and passive transport
**Passive transport** moves a species *down* its concentration gradient and needs
no energy. **Active transport** moves a species *against* its gradient and must
be paid for: **primary** active transport is paid directly with ATP; **secondary**
active transport is paid indirectly, using a gradient that some other pump has
already built.
:::

### The sodium–potassium pump

The Na⁺/K⁺-ATPase is an enzyme spanning the membrane of every animal cell. In
each cycle it hydrolyses one molecule of ATP and uses the energy to push
**three Na⁺ ions out** of the cell and pull **two K⁺ ions in**:

3Na⁺(inside) + 2K⁺(outside) + ATP + H₂O → 3Na⁺(outside) + 2K⁺(inside) + ADP + Pi

Both ions move *against* their gradients, so this is primary active transport.
Because three positive charges leave for every two that enter, the pump is
**electrogenic**: it leaves the inside of the cell negative with respect to the
outside, and this resting potential of about −70 mV is what a nerve impulse
discharges and restores. The pump is the largest single consumer of energy in the
body at rest — roughly a quarter of all the ATP you make, and more than half of
it in nerve cells.

### The sodium–glucose pump

Glucose in the gut is often *less* concentrated than the glucose already inside
the intestinal cell, so it cannot simply diffuse in. The **sodium–glucose linked
transporter (SGLT1)** in the lining of the small intestine solves the problem by
letting two Na⁺ ions fall down their steep gradient into the cell and using that
energy to drag one glucose molecule in with them:

2Na⁺(outside) + glucose(outside) → 2Na⁺(inside) + glucose(inside)

No ATP is consumed here directly — but the Na⁺ gradient that drives it was built
by the Na⁺/K⁺-ATPase, so this is **secondary** active transport (a *symport*,
because both species move the same way).

This piece of chemistry saves lives. Oral rehydration solution — the *jeevan jal*
packet sold in every Nepali pharmacy — is a mixture of glucose and sodium
chloride in water. In diarrhoeal disease the gut has stopped absorbing salt by
its usual route, but SGLT1 still works, so giving glucose *together with* salt
lets the sodium be absorbed, and water follows the sodium by osmosis. Salt alone,
or sugar alone, does far less.

```figure caption="The two pumps. Left: the Na⁺/K⁺-ATPase expels 3 Na⁺ and takes in 2 K⁺ for each ATP hydrolysed. Right: SGLT1 lets 2 Na⁺ fall down that gradient and carries one glucose molecule in with them."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle
fig, ax = plt.subplots(figsize=(5.1,3.0))

# membrane
ax.add_patch(Rectangle((0.0,2.15),10.0,1.30, fc='#e8d9b5', ec='none'))
ax.plot([0,10],[2.15,2.15], color=MUTED, lw=1.0)
ax.plot([0,10],[3.45,3.45], color=MUTED, lw=1.0)
for x in np.arange(0.18, 10.0, 0.30):
    ax.plot([x],[3.32], marker='o', ms=3.2, color='#c8a951')
    ax.plot([x],[2.28], marker='o', ms=3.2, color='#c8a951')
ax.text(5.0,4.78,'outside the cell:  Na⁺ 145 mM,  K⁺ 4 mM', fontsize=7.8,
        color=MUTED, ha='center')
ax.text(9.92,1.30,'inside the cell:  Na⁺ 12 mM,  K⁺ 140 mM', fontsize=7.8,
        color=MUTED, ha='right')

# two transport proteins
for x0, col, name in ((1.55,'#1d6fb8','Na⁺/K⁺-ATPase'), (6.15,'#2e8b57','SGLT1')):
    ax.add_patch(FancyBboxPatch((x0,2.05),2.3,1.50, boxstyle='round,pad=0.04,rounding_size=0.25',
                                fc=col, alpha=0.20, ec=col, lw=1.3))
    ax.text(x0+1.15, 2.80, name, fontsize=8.0, color=col, ha='center', va='center',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.88, pad=1.6), zorder=5)

def up(x, lab, col):
    ax.annotate('', xy=(x,4.05), xytext=(x,1.55),
                arrowprops=dict(arrowstyle='-|>', color=col, lw=1.6, mutation_scale=12))
    ax.text(x, 4.16, lab, fontsize=8.2, color=col, ha='center', va='bottom')
def down(x, lab, col, y=1.30):
    ax.annotate('', xy=(x,1.55), xytext=(x,4.05),
                arrowprops=dict(arrowstyle='-|>', color=col, lw=1.6, mutation_scale=12))
    ax.text(x, 4.16, lab, fontsize=8.2, color=col, ha='center', va='bottom')

up(1.95, '3 Na⁺', '#d9534f')
down(3.45, '2 K⁺', '#1d6fb8')
down(6.55, '2 Na⁺', '#d9534f')
down(7.95, 'glucose', '#2e8b57')

# ATP label
ax.annotate('', xy=(2.70,1.95), xytext=(2.70,1.05),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.2, mutation_scale=10))
ax.text(2.70,0.92,'ATP → ADP + Pi', fontsize=7.8, color=INK, ha='center', va='top')
ax.text(7.25,0.92,'no ATP used directly:\ndriven by the Na⁺ gradient', fontsize=7.6,
        color=INK, ha='center', va='top', linespacing=1.3)

ax.set_xlim(-0.1,10.1); ax.set_ylim(0.15,5.05); ax.axis('off')
```

::: example Worked example 11.2
**Problem.** A resting nerve cell hydrolyses ATP on its Na⁺/K⁺ pump at the rate
of $2.0\times10^{-9}$ mol per second. Calculate the number of Na⁺ ions expelled
and of K⁺ ions taken in every second.
($N_A = 6.022\times10^{23}\ \text{mol}^{-1}$)

**Solution.** The pump moves 3 Na⁺ out and 2 K⁺ in per ATP, so

$$ n(\text{Na}^{+}) = 3 \times 2.0\times10^{-9} = 6.0\times10^{-9}\ \text{mol s}^{-1} $$
$$ N(\text{Na}^{+}) = 6.0\times10^{-9} \times 6.022\times10^{23} = 3.6\times10^{15}\ \text{ions s}^{-1} $$

For potassium,

$$ n(\text{K}^{+}) = 2 \times 2.0\times10^{-9} = 4.0\times10^{-9}\ \text{mol s}^{-1} $$
$$ N(\text{K}^{+}) = 4.0\times10^{-9} \times 6.022\times10^{23} = 2.4\times10^{15}\ \text{ions s}^{-1} $$

Since 3 positive charges leave for every 2 that enter, there is a net export of
$1.2\times10^{15}$ positive charges per second — the cell interior stays negative.
:::

::: example Worked example 11.3
**Problem.** A person's daily food contains 5.85 g of sodium chloride. Calculate
the amount (in moles) and the mass of Na⁺ taken in, and compare it with the WHO
recommendation of less than 2.0 g of sodium per day. (Na = 23, Cl = 35.5)

**Solution.** Molar mass of NaCl $= 23 + 35.5 = 58.5\ \text{g mol}^{-1}$.

$$ n(\text{NaCl}) = \frac{5.85}{58.5} = 0.100\ \text{mol} $$

One mole of NaCl gives one mole of Na⁺, so $n(\text{Na}^{+}) = 0.100\ \text{mol}$ and

$$ m(\text{Na}^{+}) = 0.100 \times 23 = 2.3\ \text{g} $$

This is already 15% above the WHO limit, and it comes from the table salt alone —
before counting the sodium in pickles, instant noodles and dried meat.
:::

## 11.5 Metal toxicity

A metal becomes toxic when it does one of three things: it binds to the
**–SH (thiol) groups** of enzymes and shuts them down; it **replaces** the proper
metal in a protein with one of the wrong size or charge; or it catalyses the
formation of **free radicals** that attack the cell. Non-essential heavy metals
are dangerous at any level; essential ones are dangerous only in excess.

| Metal | Main sources | How it poisons | Effect / disease |
|---|---|---|---|
| Iron | overdose of iron tablets; repeated blood transfusion; the genetic disorder haemochromatosis | free Fe²⁺ generates the hydroxyl radical by the Fenton reaction, Fe²⁺ + H₂O₂ → Fe³⁺ + OH⁻ + •OH | liver cirrhosis, damage to heart and pancreas; acute poisoning of children |
| Arsenic | contaminated tube-well water; pesticides; some coal | As(III) binds the –SH groups of enzymes such as pyruvate dehydrogenase; arsenate AsO₄³⁻ mimics phosphate and uncouples ATP synthesis | melanosis and keratosis of palms and soles, black-foot disease, cancer of skin, lung and bladder |
| Mercury | methylmercury in large fish; broken thermometers and CFL tubes; gold amalgamation | Hg²⁺ and CH₃Hg⁺ bind thiol groups; methylmercury crosses the blood–brain and placental barriers | **Minamata disease** — numbness, loss of speech, vision and hearing, birth defects |
| Lead | old lead paint, lead pipes, battery recycling, some cosmetics and spices | Pb²⁺ inhibits δ-aminolaevulinic acid dehydratase and ferrochelatase, blocking haem synthesis; it also mimics Ca²⁺ and is stored in bone | anaemia, abdominal colic, kidney damage, and irreversible loss of IQ in children |
| Cadmium | nickel–cadmium batteries, cigarette smoke, rice grown on contaminated soil, electroplating | Cd²⁺ displaces Zn²⁺ from enzymes, whose active site then no longer fits; damages the kidney tubule | **itai-itai disease** — kidney failure, softening of bone (osteomalacia) and repeated fractures |

Arsenic is not a distant problem in Nepal. Tube-wells in several Terai districts,
Nawalparasi worst among them, draw water from sediments that release arsenic. The
WHO guideline is 0.01 mg L⁻¹ (10 ppb), while the Nepal interim national standard
is 0.05 mg L⁻¹ (50 ppb); wells are painted red or green after testing.

**Treatment.** Heavy-metal poisoning is treated by **chelation therapy** — giving
a ligand that wraps around the metal ion and forms a stable, water-soluble
complex that the kidney can excrete.

| Poison | Chelating antidote |
|---|---|
| Lead | calcium disodium EDTA, succimer (DMSA) |
| Arsenic, mercury | BAL (dimercaprol, a dithiol) |
| Iron | desferrioxamine |
| Copper (Wilson's disease) | D-penicillamine |

::: example Worked example 11.4
**Problem.** A tube-well sample from the Terai contains 0.15 mg L⁻¹ of arsenic.
(a) Express this concentration in parts per billion. (b) By what factor does it
exceed the WHO guideline of 0.01 mg L⁻¹? (c) If a farmer drinks 4.0 L of this
water a day, what mass of arsenic does he take in over one year of 365 days?

**Solution.**

(a) 1 mg L⁻¹ is 1 part per million, since 1 L of water has a mass of about
$10^{6}$ mg. Therefore

$$ 0.15\ \text{mg L}^{-1} = 0.15\ \text{ppm} = 150\ \text{ppb} $$

(b) $\dfrac{0.15}{0.01} = 15$, so the water is **15 times** the WHO guideline
(and 3 times the Nepal interim standard of 0.05 mg L⁻¹).

(c) Daily intake $= 0.15 \times 4.0 = 0.60\ \text{mg}$. Over a year,

$$ m = 0.60 \times 365 = 219\ \text{mg} \approx 0.22\ \text{g} $$
:::

::: caution Toxicity is about dose, not about the element
Iron, copper, zinc, chromium and cobalt are all *essential* and all *toxic*. What
matters is the dose: too little iron gives anaemia, too much gives liver
cirrhosis. Only the non-essential heavy metals — lead, cadmium, mercury,
arsenic — have no safe biological role at all.
:::

## Chapter summary

- Bio-inorganic chemistry studies the role of inorganic elements, especially
  metal ions, in living systems. About 25 elements are essential to humans;
  11 of them make up 99.9% of body mass.
- **Macronutrients** are needed in more than about 100 mg per day and make up
  more than 0.01% of body mass (O, C, H, N, Ca, P, K, S, Na, Cl, Mg);
  **micronutrients** are needed in smaller amounts (Fe, Zn, Cu, Mn, I, F, Se,
  Cr, Co, Mo, Ni).
- Na⁺ is the main extracellular and K⁺ the main intracellular cation; Mg²⁺ is
  the centre of chlorophyll and the partner of ATP; Ca²⁺ builds bone as
  Ca₅(PO₄)₃OH and triggers clotting and muscle contraction.
- Fe²⁺ in the porphyrin ring of haem carries O₂ (Hb + 4O₂ ⇌ Hb(O₂)₄) and Fe in
  cytochromes transfers electrons; Cu works in cytochrome c oxidase and
  haemocyanin; Zn²⁺ is the Lewis acid of carbonic anhydrase; Ni²⁺ is in urease;
  Co³⁺ is in vitamin B₁₂; Cr³⁺ helps insulin act.
- The **Na⁺/K⁺-ATPase** is primary active transport: 3 Na⁺ out and 2 K⁺ in per
  ATP, which makes it electrogenic and maintains the −70 mV resting potential.
- **SGLT1** is secondary active transport: 2 Na⁺ enter down their gradient and
  bring one glucose molecule with them. This is the chemistry behind oral
  rehydration solution.
- Toxic metals act by binding –SH groups, by replacing the correct metal ion, or
  by generating free radicals (Fenton reaction for iron). Mercury causes Minamata
  disease, cadmium causes itai-itai disease, lead blocks haem synthesis, arsenic
  inactivates thiol enzymes.
- Poisoning is treated by **chelation therapy**: EDTA for lead, BAL for arsenic
  and mercury, desferrioxamine for iron, penicillamine for copper.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The metal ion present at the centre of the chlorophyll molecule is <span class="marks">[1]</span>
   (a) Fe²⁺ (b) Mg²⁺ (c) Ca²⁺ (d) Co³⁺
2. In one cycle the sodium–potassium pump transports <span class="marks">[1]</span>
   (a) 2 Na⁺ out and 3 K⁺ in (b) 3 Na⁺ out and 2 K⁺ in
   (c) 3 Na⁺ in and 2 K⁺ out (d) 1 Na⁺ out and 1 K⁺ in
3. The metal present in vitamin B₁₂ is <span class="marks">[1]</span>
   (a) Ni (b) Zn (c) Co (d) Cr
4. Itai-itai disease is caused by poisoning with <span class="marks">[1]</span>
   (a) mercury (b) lead (c) cadmium (d) arsenic
5. Which enzyme requires Zn²⁺ at its active site? <span class="marks">[1]</span>
   (a) urease (b) catalase (c) carbonic anhydrase (d) cytochrome c oxidase
6. The antidote used in lead poisoning is <span class="marks">[1]</span>
   (a) desferrioxamine (b) calcium disodium EDTA (c) glucose (d) sodium thiosulphate

::: note Answers to Group A
**1.** (b) — chlorophyll is a magnesium porphyrin; haemoglobin is the iron one.
**2.** (b) — three positive charges out for two in, which is why the pump is electrogenic.
**3.** (c) — cobalt sits in the corrin ring of cyanocobalamin.
**4.** (c) — cadmium damages the kidney tubule and softens bone.
**5.** (c) — Zn²⁺ is the Lewis acid that activates water in carbonic anhydrase.
**6.** (b) — EDTA chelates Pb²⁺ into a soluble complex that is excreted.
:::

**Group B — Short answer (5 marks each)**

1. Distinguish between macronutrients and micronutrients with three examples of each. Why is a micronutrient deficiency still dangerous? <span class="marks">[5]</span>
2. Describe the structure of the haem group and explain how haemoglobin carries oxygen. Why is carbon monoxide poisonous? <span class="marks">[5]</span>
3. Explain the working of the sodium–potassium pump. Why is it called an electrogenic pump? <span class="marks">[5]</span>
4. What is the sodium–glucose pump? Explain how it accounts for the composition of oral rehydration solution. <span class="marks">[5]</span>
5. State the biological role of any five of the following: Mg, Ca, Fe, Cu, Zn, Ni, Co. <span class="marks">[5]</span>
6. Haemoglobin (molar mass 64 500 g mol⁻¹) contains four iron atoms per molecule. Calculate the percentage of iron in it and the mass of haemoglobin that would contain 1.00 g of iron. (Fe = 55.85) <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Macronutrients are needed in more than about 100 mg per day and exceed 0.01%
of body mass — for example Ca, P, K. Micronutrients are needed in less than about
100 mg per day — for example Fe, Zn, I. A micronutrient deficiency is still
dangerous because the trace metal is usually at the *active site* of an enzyme, so
a few milligrams missing stop a whole reaction: no cobalt means no vitamin B₁₂ and
pernicious anaemia; no iodine means goitre.

**3.** See Section 11.4. Per molecule of ATP hydrolysed, 3 Na⁺ are pushed out and
2 K⁺ are pulled in, both against their concentration gradients (primary active
transport). It is electrogenic because three positive charges leave for every two
that enter, so a net positive charge is exported and the interior of the cell is
left about 70 mV negative with respect to the outside.

**6.** Iron in one mole of haemoglobin $= 4 \times 55.85 = 223.4\ \text{g}$, so
%Fe $= (223.4/64\,500)\times100 = 0.346\%$. If 100 g of haemoglobin holds 0.346 g
of iron, then the mass holding 1.00 g is
$100 \times (1.00/0.346) = 289\ \text{g}$ of haemoglobin.
:::

**Group C — Long answer (8 marks each)**

1. (a) What is bio-inorganic chemistry? Classify the elements of the human body
   into macronutrients and micronutrients, giving the approximate boundary
   between them. <span class="marks">[3]</span>
   (b) Tabulate the biological importance of Na, K, Mg, Ca and Fe, giving one
   specific molecule or process for each. <span class="marks">[5]</span>
2. (a) Explain, with equations where possible, why arsenic, mercury, lead and
   cadmium are toxic, naming the disease associated with each. <span class="marks">[5]</span>
   (b) A tube-well in Nawalparasi yields water containing 0.20 mg L⁻¹ of arsenic.
   Express this in ppb, state by what factor it exceeds the Nepal interim
   standard of 0.05 mg L⁻¹, and calculate the mass of arsenic consumed in 30 days
   by a person drinking 3.0 L per day. <span class="marks">[3]</span>

::: note Answers to Group C
**1.** (a) Outline as in Sections 11.1 and 11.2: the boundary is about 100 mg per
day, or 0.01% of body mass. (b) Use the table in Section 11.3 — Na⁺ extracellular
osmotic balance and nerve impulse; K⁺ intracellular, resting potential and
pyruvate kinase; Mg²⁺ chlorophyll and Mg–ATP; Ca²⁺ hydroxyapatite in bone,
clotting and muscle contraction; Fe haemoglobin, myoglobin and the cytochromes.

**2.** (a) Arsenic(III) binds the –SH groups of enzymes and arsenate mimics
phosphate, giving melanosis, keratosis and cancers. Mercury, especially
methylmercury, binds thiols and crosses into the brain — Minamata disease. Lead
inhibits ALA dehydratase and ferrochelatase so haem cannot be made (anaemia) and
replaces Ca²⁺ in bone. Cadmium displaces Zn²⁺ from enzymes and destroys the kidney
tubule — itai-itai disease.
(b) 0.20 mg L⁻¹ = 0.20 ppm = **200 ppb**; that is $0.20/0.05 = $ **4 times** the
Nepal interim standard. Daily intake $= 0.20 \times 3.0 = 0.60\ \text{mg}$, so in
30 days $m = 0.60 \times 30 = 18\ \text{mg}$.
:::
