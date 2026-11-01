---
subject: Botany
grade: CEE
unit: 12
title: Photosynthesis and Respiration
hours: 3
area: Plant Physiology
---

The two great energy pathways share this chapter and its **3 of the 40
Botany questions**. The paper's habits here are predictable: it asks where
each step happens (thylakoid vs stroma, cytoplasm vs mitochondrion), the
first products and CO₂ acceptors of the **C3, C4 and CAM** pathways, the
book-keeping of **ATP, NADH and CO₂** through the Calvin cycle and through
glycolysis–Krebs–electron transport, and the **respiratory quotient** for
different substrates. Learn the numbers in the tables below and the
chapter converts directly into marks.

::: key What the paper asks from this chapter
- **Pigments** — chlorophyll *a* (primary, Mg centre) vs accessory *b*, carotenes, xanthophylls; absorption peaks in blue and red.
- **Light reactions** — PS II = P680 (acts first), PS I = P700; Z-scheme water → NADP⁺; photolysis at the oxygen-evolving complex (Mn₄CaO₅) releases O₂ **from water** into the lumen; non-cyclic makes ATP + NADPH + O₂; cyclic (PS I only) makes ATP alone, topping the ratio to 3 ATP : 2 NADPH.
- **Calvin cycle (C3)** — stroma; RuBP + CO₂ by RuBisCO → 2 × 3-PGA (first stable product); per CO₂: 3 ATP + 2 NADPH; per glucose: **18 ATP + 12 NADPH**.
- **C4 (Hatch–Slack)** — PEP carboxylase in mesophyll → oxaloacetate (4C) → malate → CO₂ released in bundle sheath (Kranz anatomy); spatial separation; 5 ATP per CO₂; maize, sugarcane.
- **Photorespiration** — RuBisCO oxygenase; chloroplast–peroxisome–mitochondrion; loses 1 CO₂ per 2 oxygenations; worse when hot and stomata shut.
- **Factors** — Blackman's law of limiting factors; light and CO₂ compensation points; airborne CO₂ is now about 0.043%, not 0.03%.
- **Bacterial photosynthesis** — bacteriochlorophyll, H₂S as donor, **no O₂ evolved**.
- **Respiration** — glycolysis (cytoplasm; net 2 ATP + 2 NADH → 2 pyruvate); link reaction (→ 2 acetyl-CoA + 2 CO₂ + 2 NADH); Krebs (matrix; per glucose 6 NADH + 2 FADH₂ + 2 ATP + 4 CO₂); ETS on cristae, O₂ the terminal acceptor, chemiosmosis (Mitchell).
- **Totals and RQ** — modern yield 30–32 ATP per glucose (classical 38); fermentation nets 2 ATP (all from glycolysis); RQ: carbohydrate 1.0, fat 0.7, protein 0.82, organic acids higher than 1; Pasteur effect.
:::

## 12.1 Photosynthetic pigments; photosystems I and II; the light reactions

Photosynthesis reduces CO₂ to carbohydrate with water as the electron
donor:

6 CO₂ + 12 H₂O → C₆H₁₂O₆ + 6 O₂ + 6 H₂O

Twelve waters stand on the left because **all the released oxygen comes
from water, not from CO₂** — predicted by van Niel from bacterial
photosynthesis and proved with the heavy isotope ¹⁸O (Ruben and
co-workers, 1941). The organelle is the chloroplast: pigments and electron
carriers sit in the **thylakoid membranes** (stacked into **grana**,
joined by **stroma lamellae**), protons are pumped into the **lumen**, and
the carbon-fixing enzymes float in the **stroma**. Hold the rule: **light
reaction in the thylakoid, dark reaction in the stroma**.

Of the pigments, only **chlorophyll *a*** — blue-green, with a
**magnesium atom at the centre of its porphyrin ring** — can turn light
into chemical energy: it is the **primary pigment**. **Chlorophyll *b*,
carotenes (orange) and xanthophylls (yellow)** are **accessory pigments**:
they harvest wavelengths chlorophyll *a* misses, pass the energy on, and
(the carotenoids) protect against photo-oxidation. Chlorophyll absorbs
strongly in the **blue and red** and reflects green — hence green leaves,
and hence the action spectrum peaking in red and blue light.

Light is gathered by two antenna systems, each funnelling energy into a
special pair of chlorophyll *a* molecules: **photosystem II, reaction
centre P680** (absorbance peak 680 nm, mostly in grana) and **photosystem
I, P700** (700 nm, mostly in stroma lamellae). Both are chlorophyll *a*;
the numbers are wavelengths. Despite the names, **PS II acts first** —
it was only discovered second.

In **non-cyclic photophosphorylation** electrons flow one way from water
to NADP⁺ along the **Z-scheme**: light excites P680, which feeds electrons
through pheophytin, the plastoquinone pool, the **cytochrome b₆f complex**
and **plastocyanin** to PS I; light excites P700, which feeds them through
**ferredoxin** to **NADP⁺, forming NADPH**. The hole left in P680 is so
oxidising (+1.2 V) that the **oxygen-evolving complex** (Mn₄CaO₅, needing
Cl⁻) on the **lumen** side of PS II can strip electrons from water —
**photolysis**:

2 H₂O → O₂ + 4 H⁺ + 4 e⁻

Those protons, plus more pumped by cytochrome b₆f, build the lumen
gradient whose discharge through **ATP synthase** makes ATP —
chemiosmosis. Net products: **ATP + NADPH + O₂**.

```figure caption="The Z-scheme of non-cyclic electron flow. The vertical axis is redox potential: the two light-driven jumps lift electrons from water all the way up to NADPH, and ATP is tapped on the downhill stretch between the photosystems."
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.2, 3.4))
pts = [(0.07, 0.82, 'H2O'), (0.18, 0.82, 'P680'), (0.18, -0.80, 'P680*'),
       (0.32, -0.05, 'PQ'), (0.46, 0.30, 'cyt b6f'), (0.60, 0.42, 'P700'),
       (0.60, -1.25, 'P700*'), (0.76, -0.40, 'Fd'), (0.93, -0.32, 'NADP+')]
xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
for a, b in zip(range(len(pts)-1), range(1, len(pts))):
    light = (a, b) in ((1, 2), (5, 6))
    ax.annotate('', xy=(xs[b], ys[b]), xytext=(xs[a], ys[a]),
                arrowprops=dict(arrowstyle='-|>', color='#e8a33d' if light else MUTED,
                                lw=1.8 if light else 1.1, shrinkA=10, shrinkB=10))
for x, y, lab in pts:
    ax.text(x, y, lab, fontsize=6.7, ha='center', va='center', color=INK,
            bbox=dict(fc='white', ec=MUTED, lw=0.6, boxstyle='round,pad=0.24'))
ax.text(0.155, 0.02, 'light\n680 nm', fontsize=6.4, color='#c0392b', ha='right', va='center')
ax.text(0.578, -0.42, 'light\n700 nm', fontsize=6.4, color='#c0392b', ha='right', va='center')
ax.text(0.07, 0.55, 'O2 out', fontsize=6.4, color='#2e8b57', ha='center')
ax.text(0.93, -0.08, 'NADPH', fontsize=6.7, color='#2e8b57', ha='center')
ax.text(0.39, 0.68, 'ATP made on this\nproton-pumping stretch', fontsize=6.3, color='#2e8b57', ha='center')
ax.set_ylim(1.12, -1.58); ax.set_xlim(-0.02, 1.02)
ax.set_ylabel('redox potential (volts)', fontsize=7.2)
ax.set_yticks([0.8, 0.4, 0.0, -0.4, -0.8, -1.2])
ax.tick_params(axis='y', labelsize=6.6)
ax.set_xticks([]); ax.grid(axis='y', lw=0.5, alpha=0.6); ax.set_axisbelow(True)
for s in ('top', 'right', 'bottom'):
    ax.spines[s].set_visible(False)
fig.tight_layout()
```

In **cyclic photophosphorylation** PS I works alone: its electron returns
from ferredoxin to the plastoquinone pool and round again, pumping
protons but splitting no water — **ATP only, no NADPH, no O₂**. Its
purpose is exact: the Calvin cycle needs ATP and NADPH in the ratio
**3 : 2**, linear flow supplies about 1.28, and cyclic flow makes up the
shortfall.

| | Non-cyclic | Cyclic |
|---|---|---|
| Photosystems | PS II and PS I | PS I only |
| Path | open: water → NADP⁺ | closed loop |
| Products | ATP + NADPH + O₂ | ATP only |
| Photolysis | yes | no |
| Main site | grana | stroma lamellae |


```figure caption="Respiration in four stages: glycolysis splits glucose to pyruvate in the cytosol for 2 ATP, the link reaction forms acetyl-CoA with CO₂ out, the Krebs cycle turns in the matrix loading NADH and FADH₂, and the electron transport chain on the cristae spends them against oxygen for the bulk of the ATP."
flow([("glycolysis", "glucose splits\nto pyruvate"),
      ("link reaction", "acetyl-CoA forms,\nCO₂ out"),
      ("Krebs cycle", "matrix turns,\nNADH, FADH₂"),
      ("ETC", "O₂ accepts,\n~30 ATP made")], figsize=(5.2, 2.15))
```

::: example The two ledgers the paper audits
**Problem.** How many ATP and NADPH does the Calvin cycle spend to make one
glucose? What is the RQ of tripalmitin (C₅₁H₉₈O₆ + 72.5 O₂ → 51 CO₂ + 49
H₂O)? And the modern ATP total per glucose respired?
**Solution.** Per CO₂ fixed the cycle spends 3 ATP + 2 NADPH; ×6 = **18 ATP
and 12 NADPH per glucose**. RQ = 51 ÷ 72.5 ≈ **0.7** — the fat signature,
hydrogen-rich fuel demanding extra oxygen. Respiration's ledger: 4
substrate-level ATP (2 glycolysis, 2 GTP) plus ~10 NADH × 2.5 and ~2 FADH₂ ×
1.5 ≈ 25 + 3 = 28 oxidative → **30–32 ATP per glucose**, against the 2 ATP of
fermentation: oxygen is worth fifteen-fold.
:::
## 12.2 Calvin cycle (C3), Hatch–Slack pathway (C4) and photorespiration; factors; bacterial photosynthesis

The **Calvin cycle** (Calvin, Benson, Bassham; Nobel 1961) runs in the
**stroma**, light-independent but not nocturnal — it stops within minutes
in the dark for want of ATP and NADPH.

1. **Carboxylation.** The 5C acceptor **ribulose-1,5-bisphosphate
   (RuBP)** takes CO₂, catalysed by **RuBisCO** (the most abundant
   protein on Earth, and a slow one). The 6C intermediate splits into two
   **3-phosphoglycerate (3-PGA, 3C)** — the first stable product, hence
   "C3 plants".
2. **Reduction.** Each 3-PGA is phosphorylated by **1 ATP** and reduced
   by **1 NADPH** to **glyceraldehyde-3-phosphate (G3P)**.
3. **Regeneration.** Most G3P is reshuffled (costing 1 more ATP per CO₂)
   to rebuild RuBP; the surplus leaves to make sugars.

Book-keeping: **per CO₂, 3 ATP + 2 NADPH**; six turns give one glucose
at **18 ATP + 12 NADPH**, twelve G3P of which two exit and ten recycle.

**Photorespiration.** RuBisCO is also an *oxygenase*: in air it sometimes
fixes O₂ instead of CO₂, yielding one 3-PGA and one useless
2-phosphoglycolate. Salvaging it tours three organelles — **chloroplast
→ peroxisome → mitochondrion** — burns ATP and **releases one CO₂ for
every two oxygenations**, with no ATP gain. It worsens as temperature
rises and as closed stomata let internal CO₂ fall.

**C4 photosynthesis (Hatch and Slack, 1966)** defeats photorespiration by
concentrating CO₂ around RuBisCO, separating the two carboxylations
**in space**. C4 leaves show **Kranz anatomy**: chloroplast-rich
**bundle-sheath** cells wreathing the veins, ringed by mesophyll. In the
**mesophyll**, **PEP carboxylase** (no oxygenase activity, high affinity)
fixes bicarbonate onto PEP to give **oxaloacetate (4C)** — the first
stable product — which is reduced to **malate** and shipped to the bundle
sheath. There malate is decarboxylated, flooding RuBisCO with CO₂ at
10–20 times atmospheric levels, and the Calvin cycle runs almost free of
oxygenation; pyruvate returns to regenerate PEP at a cost of **two extra
ATP equivalents per CO₂ (5 ATP + 2 NADPH total)**. Maize, sugarcane,
sorghum and finger millet (kodo) are Nepal's C4 crops; rice and wheat are
C3. **CAM plants** (pineapple, *Aloe vera*, *Opuntia*) achieve the same
separation **in time**: stomata open at night, PEP carboxylase stores
malic acid in the vacuole, and by day, behind closed stomata, the acid is
decarboxylated for the Calvin cycle.

| | C3 | C4 | CAM |
|---|---|---|---|
| First stable product | 3-PGA (3C) | oxaloacetate (4C) | oxaloacetate (4C) |
| First CO₂ acceptor/enzyme | RuBP / RuBisCO | PEP / PEP carboxylase | PEP / PEP carboxylase |
| Separation | none | spatial (Kranz) | temporal (night/day) |
| Photorespiration | high | greatly suppressed | greatly suppressed |
| CO₂ compensation point | 40–100 ppm | 3–10 ppm | very low |
| ATP per CO₂ | 3 | 5 | 5–6 |
| Stomata open | day | day | night |

**Bacterial photosynthesis** (purple and green sulphur bacteria) uses
**bacteriochlorophyll**, one photosystem, and donors such as **H₂S**
instead of water — so it deposits sulphur and **evolves no oxygen**
(anoxygenic). Comparing it with plant photosynthesis is what led van Niel
to locate the oxygen's source in water.

**Factors.** **Blackman's law of limiting factors (1905)**: the rate is
set by whichever factor is nearest its minimum. The **light compensation
point** is where photosynthesis exactly balances respiration (no net gas
exchange); the **CO₂ compensation point** is the equivalent CO₂ level
(40–100 ppm in C3, only 3–10 in C4). CO₂ in air is now about **427 ppm
(0.043%)** and is usually the field's limiting factor; red and blue light
are most effective; temperature governs through enzyme kinetics (rate
roughly doubling per 10 °C to an optimum, then crashing); water shortage
acts by closing stomata.

## 12.3 Aerobic and anaerobic respiration: glycolysis, oxidative decarboxylation, Krebs cycle, electron transport and oxidative phosphorylation; factors

Respiration releases the energy of food in controlled packets, trapping
much of it in ATP:

C₆H₁₂O₆ + 6 O₂ → 6 CO₂ + 6 H₂O + energy (ΔG ≈ −2870 kJ mol⁻¹)

**1. Glycolysis** (Embden–Meyerhof–Parnas pathway) runs in the
**cytoplasm** of every cell, with or without oxygen. Glucose is
phosphorylated twice — **2 ATP invested**, at hexokinase and at the
rate-limiting **phosphofructokinase** — then split into two triose
phosphates, each oxidised (making **NADH**) and each yielding 2 ATP by
**substrate-level phosphorylation**. Net: **2 ATP + 2 NADH + 2 pyruvate
(3C)** per glucose. No CO₂ yet.

**2. Link reaction (oxidative decarboxylation).** In the **mitochondrial
matrix** the pyruvate dehydrogenase complex converts each pyruvate (3C)
to **acetyl-CoA (2C) + CO₂ + NADH**: per glucose, **2 CO₂ + 2 NADH**.
It is irreversible, which is why fat cannot be turned back into sugar by
reversing it.

**3. Krebs cycle** (citric acid/TCA cycle, Krebs 1937), also in the
matrix. Acetyl-CoA (2C) joins oxaloacetate (4C) → **citrate (6C)** →
α-ketoglutarate (5C) → succinyl-CoA (4C) → succinate → fumarate → malate
→ oxaloacetate again. **Per turn: 3 NADH + 1 FADH₂ + 1 ATP + 2 CO₂**;
per glucose (two turns): **6 NADH + 2 FADH₂ + 2 ATP + 4 CO₂**. Note that
all six glucose carbons have now left as CO₂ and no O₂ has been used.

**4. Electron transport and oxidative phosphorylation.** The 10 NADH and
2 FADH₂ are cashed at the **inner mitochondrial membrane (cristae)**:
Complex I → ubiquinone → Complex III → cytochrome *c* → Complex IV →
**oxygen, the terminal electron acceptor**, which with protons forms
water. FADH₂ enters at **Complex II**, bypassing I — which is why it
yields less. Complexes I, III and IV pump protons (10 H⁺ per NADH, 6 per
FADH₂), and their return through **ATP synthase** drives ATP formation —
**Peter Mitchell's chemiosmotic hypothesis** (Nobel 1978). With about 4
H⁺ spent per ATP, an NADH is worth **2.5 ATP** and an FADH₂ **1.5**,
giving the modern total of **30–32 ATP per glucose** (the shuttle used by
the two cytoplasmic NADH decides between 30 and 32). The classical
figure of **38 ATP** assumed 3 per NADH and 2 per FADH₂; if a question
specifies those ratios, use them.

```figure caption="The four stages of aerobic respiration of one glucose. All the carbon escapes as CO2 before any oxygen is consumed; nearly all the ATP is minted at the end, on the cristae."
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
fig, ax = plt.subplots(figsize=(4.9, 4.2))
Rect = mpatches.Rectangle
rows = [
    ('GLYCOLYSIS', 'cytoplasm', 'glucose (6C) to 2 pyruvate (3C)', 'net 2 ATP + 2 NADH', '#1d6fb8'),
    ('LINK REACTION', 'mitochondrial matrix', '2 pyruvate to 2 acetyl-CoA (2C)', '2 CO2 + 2 NADH', '#6a5acd'),
    ('KREBS CYCLE', 'mitochondrial matrix', '2 acetyl-CoA oxidised completely', '4 CO2 + 6 NADH + 2 FADH2 + 2 ATP', '#2e8b57'),
    ('ELECTRON TRANSPORT', 'inner mitochondrial membrane', '10 NADH + 2 FADH2 + O2 to water', 'about 26-28 ATP', '#c0392b'),
]
h = 0.200
for i, (name, where, what, out, col) in enumerate(rows):
    y = 0.985 - (i + 1)*h - i*0.022
    ax.add_patch(Rect((0.02, y), 0.96, h, fc='white', ec=col, lw=1.5))
    ax.text(0.05, y + h - 0.046, name, fontsize=7.0, color=col, va='top')
    ax.text(0.95, y + h - 0.046, where, fontsize=6.2, color=MUTED, ha='right', va='top')
    ax.text(0.05, y + h - 0.108, what, fontsize=6.7, color=INK, va='top')
    ax.text(0.05, y + 0.022, out, fontsize=6.7, color=col, va='bottom')
    if i < 3:
        ax.annotate('', xy=(0.50, y - 0.026), xytext=(0.50, y), arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.4))
ax.text(0.50, 0.045, 'TOTAL: about 30-32 ATP per glucose', fontsize=7.5, color=INK, ha='center',
        bbox=dict(fc='#f2f5f9', ec=INK, lw=1.0, boxstyle='round,pad=0.34'))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
fig.tight_layout()
```

**Anaerobic respiration (fermentation).** Without oxygen the chain
stalls and NADH piles up; fermentation exists to **regenerate NAD⁺** so
glycolysis can continue. **Alcoholic fermentation** (yeast, flooded
roots): pyruvate → acetaldehyde (pyruvate decarboxylase) → **ethanol +
CO₂**. **Lactic acid fermentation** (muscle, *Lactobacillus*): pyruvate
→ lactate, **no CO₂**. Fermentation itself makes **zero ATP** — the
whole anaerobic yield is glycolysis's **2 ATP**, about 8% of the
aerobic prize, which is why switching on oxygen sharply cuts glucose
consumption (the **Pasteur effect**).

**Respiratory quotient.** RQ = CO₂ evolved ÷ O₂ consumed (Ganong's
respirometer), and it betrays the substrate: **carbohydrates 1.0**,
**fats ≈ 0.7** (oxygen-poor, so they gulp external O₂), **proteins ≈
0.82**, **organic acids higher than 1** (malic 1.33, oxalic 4.0 —
already oxygen-rich), fermenting tissue undefined (no O₂ taken up).

::: example Worked example — costs and quotients
**Problem.** (a) How many ATP and NADPH does the Calvin cycle spend to
export one net G3P? (b) Germinating seeds in a respirometer evolve
45 cm³ of CO₂ while taking up 50 cm³ of O₂. Find the RQ and comment.

**Solution.** (a) A net G3P contains 3 carbons, so three turns fix 3 CO₂.
At 3 ATP + 2 NADPH per CO₂:

$$ 3 \times 3 = 9\ \text{ATP}, \qquad 3 \times 2 = 6\ \text{NADPH} $$

(One glucose, two G3P, doubles this to 18 ATP + 12 NADPH.)

(b) $$ \text{RQ} = \frac{45}{50} = 0.9 $$

Below 1 but above the fat value of 0.7: the seeds are respiring a
**mixture** — largely fat or protein with some carbohydrate — as oily
seeds (mustard, castor) do while converting their stores.
:::

**Factors affecting respiration.** **Oxygen**: below a few percent the
rate falls and fermentation takes over. **Temperature**: rate roughly
doubles per 10 °C (Q₁₀ ≈ 2) up to about 35–40 °C, then enzyme damage
cuts it. **Water**: dry seeds respire almost imperceptibly (why grain
stores safely), and imbibition switches respiration on. **CO₂**: high
concentrations depress respiration — exploited in controlled-atmosphere
fruit storage. Light acts only indirectly, through temperature and
photosynthate supply.


::: example Worked example — the ATP account for one glucose (modern values)
Count carefully, stage by stage, per glucose molecule:

- **Glycolysis** (cytoplasm): 4 ATP made by substrate-level phosphorylation, 2 spent → **net 2 ATP**, plus 2 NADH in the cytoplasm (worth about 1.5–2.5 ATP each depending on the shuttle used).
- **Oxidative decarboxylation** (per glucose: two pyruvates) → 2 mitochondrial NADH.
- **Krebs cycle** (two turns) → 2 ATP (GTP) directly, 6 NADH, 2 FADH₂.
- Electron transport at roughly 2.5 ATP per mitochondrial NADH and 1.5 per FADH₂ gives a grand total of **about 30–32 ATP** — the modern figure. (Older books quote 36–38 using 3 and 2 ATP per NADH/FADH₂; if an MCQ lists 38 as an option, the paper is using the traditional accounting.)

The robust facts are the *net numbers per stage* — learn those, and either total can be reconstructed.
:::

::: caution Trap — O₂ comes from water, not from CO₂
Isotope experiments settled it: the oxygen released in photosynthesis comes from **splitting water (photolysis) at photosystem II**, not from carbon dioxide. Pairs with a second swap: **cyclic** photophosphorylation makes **ATP only** (PS I alone, no NADPH, no O₂), while **non-cyclic** flow (PS II + PS I) makes ATP + NADPH + O₂.
:::



```figure caption="The two metabolisms in four drawers: the light reactions that split water and mint ATP and NADPH, the Calvin cycle that spends them on CO₂, the C₄ shuttle that supercharges RuBisCO, and the fermentations that keep glycolysis alive without oxygen."
cards([
    ("Light reactions", "thylakoid: PSII P680, PSI P700\nwater split: O₂ out\nATP + NADPH made"),
    ("Calvin cycle", "stroma: RuBisCO on RuBP\nPGA → G3P → sugar\n18 ATP, 12 NADPH / glucose"),
    ("C₄ shuttle", "PEP carboxylase in mesophyll\nmalate to bundle sheath\nKranz: no photorespiration"),
    ("Fermentation", "yeast: ethanol + CO₂\nmuscle: lactate\n2 ATP only, NAD⁺ recycled"),
], cols=2, figsize=(6.2, 3.0))
```

::: caution
Four pairs the paper swaps: the evolved **O₂ comes from water, not CO₂**
(¹⁸O labelling settled it); **PSII acts first in the chain though named
second** — numbering follows discovery, electrons follow energy; the
**Calvin cycle sits in the stroma**, not on the thylakoid, and needs light
only via ATP and NADPH; and **photorespiration consumes, it does not
produce** — CO₂ out, ATP spent, no sugar, which is exactly why C₄ exists.
:::

## Formula and fact sheet

- **Sites**: light reactions thylakoid (grana/lamellae), O₂ from water (¹⁸O proof); Calvin stroma; glycolysis cytoplasm; link + Krebs matrix; ETS cristae.
- **Photosystems**: PS II P680 acts first, PS I P700; order H₂O → PS II → PQ → cyt b₆f → plastocyanin → PS I → ferredoxin → NADP⁺.
- **Products**: non-cyclic ATP + NADPH + O₂; cyclic ATP only (ratio repair to 3 : 2).
- **Calvin**: RuBP acceptor, RuBisCO, first product 3-PGA; 3 ATP + 2 NADPH per CO₂; **18 ATP + 12 NADPH per glucose**.
- **C4**: PEP/PEP carboxylase → OAA → malate → bundle sheath (Kranz); 5 ATP per CO₂; compensation 3–10 ppm. **CAM**: same chemistry by night, stomata shut by day.
- **Photorespiration**: RuBisCO oxygenase; chloroplast–peroxisome–mitochondrion; 1 CO₂ lost per 2 oxygenations; hot + closed stomata worsens it.
- **Bacterial photosynthesis**: bacteriochlorophyll, H₂S donor, no O₂.
- **Respiration tallies per glucose**: glycolysis net 2 ATP + 2 NADH; link 2 NADH + 2 CO₂; Krebs 6 NADH + 2 FADH₂ + 2 ATP + 4 CO₂; carriers total 10 NADH + 2 FADH₂.
- **Yields**: NADH ≈ 2.5 ATP, FADH₂ ≈ 1.5 → **30–32 per glucose** (classical 3/2 gives 38); fermentation 2 (glycolysis only, regenerates NAD⁺).
- **RQ**: glucose 1.0, fat 0.7, protein 0.82, malic acid 1.33, oxalic 4.0; measured by Ganong's respirometer.
- **People**: van Niel and Ruben (O₂ from water), Calvin (cycle), Hatch and Slack (C4), Krebs (cycle), Mitchell (chemiosmosis), Blackman (limiting factors).

### Rapid-revision tables and high-yield facts

| Quantity | Value |
|---|---|
| Chl a peaks | ~430 nm and ~662 nm |
| PSII / PSI | P680 / P700 |
| O₂ source | water (photolysis) |
| Calvin per glucose | 6 CO₂, 18 ATP, 12 NADPH |
| C₄ first enzyme | PEP carboxylase (mesophyll) |
| Photorespiration organs | chloroplast, peroxisome, mitochondrion |
| Glycolysis | cytosol; net 2 ATP + 2 NADH |
| Krebs per turn | 3 NADH, 1 FADH₂, 1 GTP, 2 CO₂ |
| Terminal acceptor | O₂ → H₂O |
| Total aerobic | ~30–32 ATP; fermentation 2 ATP |
| RQ | carbs 1, fats ≈ 0.7, proteins ≈ 0.8–0.9 |
| Bacterial photosynthesis | H₂S donor, no O₂ |

## Chapter summary

- Chlorophyll *a* (Mg-centred) alone converts light energy; accessory pigments widen the catch and protect the reaction centres P680 (PS II, acting first) and P700 (PS I).
- The Z-scheme drags electrons from water (photolysis at the Mn₄CaO₅ complex, O₂ and protons into the lumen) to NADP⁺, minting ATP chemiosmotically on the way; cyclic flow around PS I adds ATP only, balancing the 3 : 2 budget.
- The stromal Calvin cycle carboxylates RuBP via RuBisCO into 3-PGA and, at 3 ATP + 2 NADPH per CO₂, builds glucose for 18 ATP + 12 NADPH.
- Photorespiration — RuBisCO fixing O₂ — wastes carbon through a three-organelle salvage loop; C4 plants suppress it spatially (Kranz anatomy, PEP carboxylase pump, 5 ATP per CO₂) and CAM plants temporally.
- Blackman's limiting-factor law and the two compensation points govern how light, CO₂ (now 0.043%), temperature and water set the photosynthetic rate; bacteria photosynthesise with H₂S and release no O₂.
- Glycolysis (cytoplasm) nets 2 ATP + 2 NADH; the link reaction and Krebs cycle (matrix) strip the six carbons out as CO₂, loading 10 NADH and 2 FADH₂ in all.
- The cristae electron-transport chain, ending at oxygen, converts those carriers into most of the modern 30–32 ATP per glucose (38 classically).
- Without oxygen, fermentation merely regenerates NAD⁺ for glycolysis's 2 ATP (Pasteur effect), and the RQ — 1.0, 0.7, 0.82, above 1 — reports the substrate being burned.

## Practice questions

**Set A — Recall (25 questions)**

1. The only pigment that can convert light energy into chemical energy is
   (a) chlorophyll *b* (b) carotene (c) chlorophyll *a* (d) xanthophyll
2. The metallic atom at the centre of the chlorophyll molecule is
   (a) iron (b) magnesium (c) copper (d) manganese
3. The reaction centre of photosystem II is
   (a) P680 (b) P700 (c) P720 (d) P650
4. The oxygen released in photosynthesis comes from
   (a) water (b) carbon dioxide (c) chlorophyll (d) glucose
5. Water is split (photolysed) at the oxygen-evolving complex associated with
   (a) photosystem I in the stroma (b) the Calvin cycle (c) photosystem II on the lumen side (d) ATP synthase
6. The products of non-cyclic photophosphorylation are
   (a) ATP, NADPH and O₂ (b) ATP only (c) NADPH only (d) glucose and O₂
7. Cyclic photophosphorylation involves
   (a) both photosystems (b) photosystem II only (c) neither photosystem (d) photosystem I only
8. In non-cyclic electron flow, the final electron acceptor is
   (a) oxygen (b) NADP⁺ (c) ferredoxin (d) plastoquinone
9. The first stable product of the Calvin cycle is
   (a) 3-phosphoglycerate (3-PGA) (b) oxaloacetate (c) glucose (d) RuBP
10. The CO₂ acceptor in a C3 plant is
   (a) phosphoenolpyruvate (b) malate (c) ribulose-1,5-bisphosphate (RuBP) (d) pyruvate
11. The enzyme that fixes CO₂ in the Calvin cycle is
   (a) PEP carboxylase (b) hexokinase (c) ATP synthase (d) RuBisCO
12. The first stable product of the C4 pathway is
   (a) 3-PGA (b) oxaloacetate (c) malate (d) aspartate
13. Kranz anatomy is the diagnostic leaf structure of
   (a) C3 plants (b) CAM plants (c) C4 plants (d) hydrophytes
14. The three organelles involved in photorespiration are the
   (a) nucleus, ribosome and Golgi body (b) chloroplast, vacuole and lysosome (c) chloroplast, nucleus and mitochondrion (d) chloroplast, peroxisome and mitochondrion
15. The law of limiting factors in photosynthesis was given by
   (a) Blackman (b) Calvin (c) Dixon (d) Krebs
16. Photosynthetic sulphur bacteria differ from green plants in that they
   (a) release more oxygen (b) use chlorophyll *a* (c) fix nitrogen (d) use H₂S as electron donor and evolve no oxygen
17. Glycolysis takes place in the
   (a) mitochondrial matrix (b) cytoplasm (c) chloroplast stroma (d) nucleus
18. The net gain of ATP from glycolysis of one glucose is
   (a) 4 (b) 8 (c) 2 (d) 0
19. The link reaction converts pyruvate into
   (a) citrate (b) lactate (c) acetyl-CoA (d) oxaloacetate
20. The Krebs cycle operates in the
   (a) cytoplasm (b) cristae (c) chloroplast (d) mitochondrial matrix
21. The number of NADH molecules produced per turn of the Krebs cycle is
   (a) one (b) three (c) two (d) four
22. The terminal electron acceptor in aerobic respiration is
   (a) NAD⁺ (b) oxygen (c) cytochrome *c* (d) carbon dioxide
23. The chemiosmotic hypothesis of ATP synthesis was proposed by
   (a) Krebs (b) Calvin (c) Peter Mitchell (d) Embden
24. The end products of alcoholic fermentation of glucose are
   (a) lactic acid only (b) ethanol only (c) CO₂ and water (d) ethanol and CO₂
25. The respiratory quotient (RQ) for glucose is
   (a) 1.0 (b) 0.7 (c) 0.82 (d) 1.33

::: note Answers and explanations — Set A
**1.** (c) — Chlorophyll *a* forms the reaction centres; the others only gather light and hand the energy over.
**2.** (b) — Mg²⁺ sits in the porphyrin ring; iron belongs to haem and cytochromes.
**3.** (a) — P680 and P700 name absorption maxima in nm; both centres are chlorophyll *a*.
**4.** (a) — Proved with ¹⁸O-labelled water by Ruben and co-workers (1941).
**5.** (c) — The Mn₄CaO₅ complex faces the lumen of PS II, so photolysis protons feed the ATP gradient.
**6.** (a) — Linear flow from water to NADP⁺ yields both currencies and oxygen.
**7.** (d) — Electrons cycle around PS I only: ATP without NADPH or O₂.
**8.** (b) — Ferredoxin–NADP⁺ reductase completes the Z-scheme by making NADPH.
**9.** (a) — The 6C addition product splits instantly into two 3-PGA — the "3" of C3.
**10.** (c) — The 5C RuBP is regenerated each turn to accept the next CO₂.
**11.** (d) — RuBisCO, the Earth's most abundant protein, carboxylates (and, unluckily, oxygenates) RuBP.
**12.** (b) — PEP carboxylase makes the 4C oxaloacetate first; malate is its reduced transport form.
**13.** (c) — The wreath of bundle-sheath cells around the veins houses the C4 Calvin cycle.
**14.** (d) — Phosphoglycolate salvage runs chloroplast → peroxisome → mitochondrion, leaking CO₂.
**15.** (a) — Blackman (1905): the scarcest factor sets the rate.
**16.** (d) — Anoxygenic photosynthesis with bacteriochlorophyll; sulphur is deposited instead of O₂ released.
**17.** (b) — Glycolysis is universal and cytoplasmic; only later stages enter the mitochondrion.
**18.** (c) — Four ATP made by substrate-level phosphorylation minus two invested = net 2.
**19.** (c) — Oxidative decarboxylation: 3C pyruvate → 2C acetyl-CoA + CO₂ + NADH.
**20.** (d) — The matrix holds the cycle; the cristae hold the electron transport chain.
**21.** (b) — Plus 1 FADH₂, 1 ATP and 2 CO₂ per turn.
**22.** (b) — Oxygen accepts the electrons and protons to form water; without it the chain stalls.
**23.** (c) — Peter Mitchell, Nobel Prize 1978; the same mechanism makes ATP in chloroplasts.
**24.** (d) — Glucose → 2 ethanol + 2 CO₂; lactic fermentation, by contrast, releases no CO₂.
**25.** (a) — Six CO₂ out for six O₂ in: RQ = 1.0 for carbohydrates.
:::

**Set B — Understanding (15 questions)**

1. Photosystem II acts before photosystem I in the Z-scheme; the numbering reflects
   (a) the order in which they were discovered, not the order of action (b) their sizes (c) their wavelength order (d) a printing error
2. The precise role of cyclic photophosphorylation is to
   (a) top up ATP to the 3 : 2 ratio the Calvin cycle needs (b) produce extra oxygen (c) fix CO₂ at night (d) replace PS II
3. Calling the Calvin cycle the "dark reaction" is misleading because it
   (a) occurs only at night (b) needs no enzymes (c) is unaffected by light in any way (d) is light-independent but soon stops in darkness without ATP and NADPH
4. C4 plants almost escape photorespiration because in their bundle sheath
   (a) RuBisCO is absent (b) oxygen is absent (c) the Calvin cycle is absent (d) CO₂ is concentrated 10–20 times around RuBisCO
5. CAM plants open their stomata at night mainly to
   (a) absorb dew (b) fix CO₂ when evaporative water loss is least (c) release oxygen (d) attract pollinators
6. Photorespiration increases on a hot afternoon when stomata close because inside the leaf
   (a) light intensity falls (b) CO₂ falls and O₂ rises, favouring RuBisCO's oxygenase activity (c) PEP carboxylase stops (d) chlorophyll breaks down
7. At the light compensation point, a leaf shows no net gas exchange because
   (a) photosynthesis has stopped (b) respiration has stopped (c) stomata are closed (d) photosynthesis exactly balances respiration
8. The essential purpose of fermentation is to
   (a) make ATP directly (b) produce alcohol for the cell (c) regenerate NAD⁺ so glycolysis can continue (d) release CO₂
9. FADH₂ yields fewer ATP than NADH in the electron transport chain because it
   (a) is made in the cytoplasm (b) enters at Complex II, bypassing the first proton-pumping complex (c) carries only one electron (d) cannot reach the membrane
10. Cyanide kills cells by blocking Complex IV, which directly causes
   (a) the electron transport chain to halt and ATP synthesis to stop (b) glycolysis to reverse (c) photolysis to stop (d) faster ATP production
11. The RQ of fats is less than 1 because fats are
   (a) rich in oxygen (b) oxygen-poor, so oxidising them needs much external O₂ (c) insoluble in water (d) stored only in seeds
12. The Pasteur effect refers to the observation that supplying oxygen to fermenting yeast
   (a) increases alcohol production (b) kills the yeast (c) has no effect (d) greatly decreases glucose consumption
13. Cyclic electron flow is located chiefly in the stroma lamellae because these membranes are rich in
   (a) PS II (b) oxygen-evolving complexes (c) PS I (d) RuBisCO
14. Accessory pigments increase photosynthetic efficiency by
   (a) absorbing extra wavelengths and passing energy to chlorophyll *a* (b) replacing chlorophyll *a* in reaction centres (c) reflecting green light (d) fixing CO₂ themselves
15. Anaerobic respiration yields so little energy because the glucose is
   (a) fully oxidised (b) converted to water (c) only partly oxidised, most energy remaining in ethanol or lactate (d) stored as starch

::: note Answers and explanations — Set B
**1.** (a) — PS I was characterised first, though in the chain PS II feeds it.
**2.** (a) — Linear flow gives an ATP : NADPH ratio near 1.28; cyclic flow tops it up to the required 1.5.
**3.** (d) — No photon is used directly, but the substrates ATP and NADPH run out quickly in the dark.
**4.** (d) — The PEP-carboxylase pump swamps the oxygenase reaction by sheer CO₂ pressure.
**5.** (b) — Night air is cool and humid; CO₂ is banked as malic acid and spent behind closed stomata by day.
**6.** (b) — Trapped O₂ from photolysis plus dwindling CO₂ tips RuBisCO towards oxygenation.
**7.** (d) — CO₂ taken up in photosynthesis equals CO₂ released in respiration.
**8.** (c) — Reducing pyruvate re-oxidises NADH; the ATP all comes from glycolysis itself.
**9.** (b) — Skipping Complex I saves 4 of the 10 protons: about 1.5 ATP against NADH's 2.5.
**10.** (a) — With no electron flow to oxygen the proton gradient collapses and oxidative phosphorylation ends.
**11.** (b) — Tripalmitin gives 102 CO₂ per 145 O₂: RQ ≈ 0.7.
**12.** (d) — ATP and citrate from aerobic respiration inhibit phosphofructokinase, throttling glycolysis.
**13.** (c) — Stroma lamellae carry PS I and ATP synthase but little PS II.
**14.** (a) — Chlorophyll *b* and carotenoids broaden the absorbed spectrum; carotenoids also quench photo-damage.
**15.** (c) — Only about 8% of glucose's free energy is released; the rest stays in the incompletely oxidised product.
:::

**Set C — Application (10 questions)**

1. To synthesise one molecule of glucose, the Calvin cycle consumes
   (a) 12 ATP and 18 NADPH (b) 6 ATP and 6 NADPH (c) 18 ATP and 12 NADPH (d) 30 ATP and 12 NADPH
2. The number of turns of the Calvin cycle needed to export one net G3P is
   (a) one (b) six (c) three (d) twelve
3. Before the electron transport chain, complete breakdown of one glucose to CO₂ has produced NADH totalling
   (a) 10 (b) 6 (c) 8 (d) 4
4. Respiring seeds evolve 45 cm³ CO₂ and consume 50 cm³ O₂ in the same time. The RQ is
   (a) 1.0 (b) 0.9 (c) 0.7 (d) 1.1
5. Using the classical values of 3 ATP per NADH and 2 ATP per FADH₂, the total ATP from one glucose (prokaryote-style accounting) is
   (a) 32 (b) 38 (c) 30 (d) 40
6. The ATP cost of fixing one CO₂ in a C4 plant such as maize is
   (a) 5 ATP (b) 3 ATP (c) 2 ATP (d) 1 ATP
7. If 12 water molecules are photolysed at PS II, the number of O₂ molecules released is
   (a) 12 (b) 3 (c) 24 (d) 6
8. The number of CO₂ molecules released when one pyruvate passes through the link reaction and Krebs cycle is
   (a) three (b) one (c) two (d) six
9. Yeast fermenting one glucose molecule under anaerobic conditions nets
   (a) 8 ATP (b) 4 ATP (c) 0 ATP (d) 2 ATP
10. Six turns of the Calvin cycle produce G3P molecules numbering
   (a) 6, all exported (b) 12, of which 2 leave the cycle (c) 2 only (d) 18, of which 6 leave

::: note Answers and explanations — Set C
**1.** (c) — Six CO₂ at 3 ATP + 2 NADPH each: 18 ATP and 12 NADPH.
**2.** (c) — Three CO₂ fixed give six G3P, five of which regenerate RuBP and one leaves net.
**3.** (a) — 2 (glycolysis) + 2 (link) + 6 (Krebs) = 10 NADH, besides 2 FADH₂.
**4.** (b) — RQ $= 45/50 = 0.9$, a mixed fat/carbohydrate substrate.
**5.** (b) — $4\ \text{(substrate-level)} + 10 \times 3 + 2 \times 2 = 38$; modern P/O ratios give 30–32.
**6.** (a) — The Calvin cycle's 3 ATP plus 2 ATP-equivalents to regenerate PEP.
**7.** (d) — $2\,\text{H}_2\text{O} \to \text{O}_2 + 4\text{H}^+ + 4e^-$, so 12 waters give 6 O₂.
**8.** (a) — One at the link reaction and two in the Krebs cycle: all three pyruvate carbons.
**9.** (d) — Only glycolysis pays out; fermentation itself yields no ATP.
**10.** (b) — Twelve G3P form; ten rebuild the six RuBP and two combine towards one glucose.
:::
