---
subject: Question Bank
grade: 12
unit: 8
title: "Biology: Unit-wise Objective Question Bank"
hours: 0
area: Biology
---

Group A of the Grade 12 Biology paper is eleven one-mark multiple-choice questions: five in Section I (Botany) and six in Section II (Zoology). They are handed out thirty minutes after the paper starts, so the eleven marks are the quickest marks in the paper, and they are also the marks that punish half-knowledge most, because every wrong option is written to match a real misconception. This chapter takes the **ten syllabus units in curriculum order**. Each unit opens with a table of the facts the examiners keep returning to, sets a block of multiple-choice questions, and closes with a key in which every answer has a one-line reason and, where an option is a trap, says what the trap is.

::: key What Group A really tests
Four things, nearly always: (1) a **definition** in one word (*porogamy*, *isograft*, *frame shift*); (2) a **sequence** (heart-beat path, urine path, steps of gametogenesis, ossicles); (3) an **application** dressed as a story ("if the oxyntic cells stopped working…"); (4) a **one-step calculation** such as a DPD or a genetic probability. Since 2081 the board has moved towards case-style stems; the facts tables below are there so that the stem is the only thing that is new to you.
:::

::: caution Where the year tags come from, and why only some questions carry one
A tag such as **(NEB 2079)** appears only on a question that the authors of this book actually saw in that paper — the wording was read from the printed paper or its scan. Sets differ: the board printed several question-paper sets each year (2079 set *N*, 2081 sets *V* and *W*, 2082 set *M*), and a tag names the year, not the set. **(NEB model 2079)** is the official board model question. **(NEB 2082, recast)** means the concept and the keyed answer were seen but the exact wording was not, so the stem has been rewritten. Everything with no tag is original, written for this book. No question is claimed to be a leak, and nothing here predicts an exam: it shows what the board has asked.
:::

::: tip How the paper is laid out
Botany carries 37 marks and Zoology 38 (Botany: MCQ 5 + four 4-mark shorts + two 8-mark longs = 37; Zoology: MCQ 6 + four 4-mark shorts + two 8-mark longs = 38). Questions 1–5 are Botany MCQs and 12–17 are Zoology MCQs; shorts are 6–9 and 18–21; longs are 10–11 and 22–23. In both sections one short and one long carry an **OR**. The curriculum publishes no unit-wise mark grid for Grade 12 Biology, so the number of MCQs set per unit below follows the teaching hours and the topics the real papers have used (see the pattern analysis in the last chapter of this part).
:::

## 8.1 Plant Anatomy

| High-yield fact | What to remember |
|---|---|
| Meristems, by position | **Apical** (length), **intercalary** (grasses, base of internode), **lateral** (girth: vascular cambium, cork cambium) |
| Meristematic vs permanent | meristematic cells keep the power of division; permanent cells have lost it |
| Simple permanent tissue | **parenchyma** (living, thin wall; chlorenchyma, aerenchyma, storage), **collenchyma** (living, corners thickened with cellulose + pectin), **sclerenchyma** (dead, lignified: fibres, sclereids) |
| Complex permanent tissue | **xylem** — tracheids, vessels, fibres, parenchyma; **phloem** — sieve tubes, companion cells, parenchyma, fibres |
| Living elements | xylem parenchyma (only living part of xylem); all of phloem except phloem fibres |
| Bundle types | collateral (open in dicot stem, closed in monocot stem), bicollateral (Cucurbita), concentric (amphivasal / amphicribral), radial (roots) |
| Root | dicot: 2–6 xylem arms, small pith, exarch; monocot: more than 6 (polyarch), large pith; endodermis with **Casparian strips** of suberin; passage cells opposite protoxylem |
| Stem | dicot: bundles in a **ring**, open, endarch, medullary rays; monocot: **scattered**, closed, sclerenchymatous hypodermis, no cambium |
| Leaf | dorsiventral (dicot): palisade above, spongy below; isobilateral (monocot): mesophyll undifferentiated, **bulliform cells**; C4 leaf: **Kranz** anatomy |
| Secondary growth | vascular cambium → secondary xylem (inside, more) and secondary phloem (outside); phellogen → phellem (cork) outside, phelloderm inside; **periderm** = all three |
| Wood | sapwood conducts; **heartwood** is dead, plugged with tyloses, tannin and resin; one annual ring = spring wood + autumn wood |

```figure caption="Types of vascular bundle. Dark = xylem, light = phloem, dashed line = cambium. Only the first is open (it has cambium), which is why a dicot stem can grow in girth and a monocot stem cannot."
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Rectangle, Wedge
fig, axes = plt.subplots(1, 5, figsize=(4.9, 2.3))
DK, LT = '#3b5a8c', '#f0c987'
def setup(ax, t):
    ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.3); ax.set_aspect('equal'); ax.axis('off')
    ax.text(0, -1.55, t, ha='center', va='top', fontsize=6.3, color=INK, linespacing=1.15)
ax = axes[0]; setup(ax, 'Collateral\nopen')
ax.add_patch(Ellipse((0, -0.5), 1.7, 0.95, fc=DK, ec=INK, lw=0.6))
ax.add_patch(Ellipse((0, 0.6), 1.7, 0.95, fc=LT, ec=INK, lw=0.6))
ax.plot([-0.85, 0.85], [0.05, 0.05], ls='--', color=INK, lw=0.9)
ax.text(0, 1.22, 'phloem', ha='center', fontsize=5.6, color=INK)
ax = axes[1]; setup(ax, 'Collateral\nclosed')
ax.add_patch(Ellipse((0, -0.5), 1.7, 0.95, fc=DK, ec=INK, lw=0.6))
ax.add_patch(Ellipse((0, 0.6), 1.7, 0.95, fc=LT, ec=INK, lw=0.6))
ax.text(0, 1.22, 'phloem', ha='center', fontsize=5.6, color=INK)
ax = axes[2]; setup(ax, 'Bicollateral')
ax.add_patch(Ellipse((0, 0.95), 1.6, 0.6, fc=LT, ec=INK, lw=0.6))
ax.add_patch(Ellipse((0, 0), 1.6, 0.8, fc=DK, ec=INK, lw=0.6))
ax.add_patch(Ellipse((0, -0.95), 1.6, 0.6, fc=LT, ec=INK, lw=0.6))
ax.plot([-0.8, 0.8], [0.45, 0.45], ls='--', color=INK, lw=0.8)
ax.plot([-0.8, 0.8], [-0.45, -0.45], ls='--', color=INK, lw=0.8)
ax = axes[3]; setup(ax, 'Concentric\namphivasal')
ax.add_patch(Circle((0, 0), 1.05, fc=DK, ec=INK, lw=0.6))
ax.add_patch(Circle((0, 0), 0.55, fc=LT, ec=INK, lw=0.6))
ax = axes[4]; setup(ax, 'Concentric\namphicribral')
ax.add_patch(Circle((0, 0), 1.05, fc=LT, ec=INK, lw=0.6))
ax.add_patch(Circle((0, 0), 0.55, fc=DK, ec=INK, lw=0.6))
fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.17, wspace=0.05)
```

```photo id="qbank/sunflower-stem" caption="Transverse section of a young sunflower (*Helianthus annuus*) stem, ×100. The vascular bundles stand in one ring around a large pith and are open (they contain cambium). This is the standard picture behind 'scattered or ring?' questions." width="62"
mark 0.045 0.53 "1"
mark 0.44 0.935 "2"
mark 0.786 0.47 "3"
mark 0.48 0.53 "4"
key 1 Epidermis
key 2 Cortex
key 3 Open vascular bundle (xylem stained red-violet)
key 4 Pith
```

1. What basis would you apply to distinguish a meristematic tissue from a permanent tissue? <span class="marks">[1]</span> (NEB model 2079)
   (a) supporting the plant (b) providing food (c) activating cell division (d) losing the ability of cell division
2. Which parenchyma makes aquatic plants light and helps them to float? <span class="marks">[1]</span> (NEB 2079)
   (a) prosenchyma (b) assimilatory parenchyma (c) aerenchyma (d) stellate parenchyma
3. What is the role of the endodermis in the roots of a plant? <span class="marks">[1]</span> (NEB 2080)
   (a) to store excess water and starch (b) to facilitate gas exchange for respiration (c) to regulate the movement of water and minerals into the root (d) to provide structural support
4. What is the name of the lateral meristem responsible for secondary growth in stems? <span class="marks">[1]</span> (NEB 2081)
   (a) apical meristem (b) vascular cambium (c) cork cambium (d) periderm
5. A botanist observes scattered vascular bundles throughout the ground tissue of a stem. What is the most appropriate conclusion? <span class="marks">[1]</span> (NEB 2082)
   (a) the plant is a monocot (b) the plant undergoes secondary growth (c) the plant has an open vascular bundle (d) the plant is a dicot
6. Which tissue is dead at maturity and has a heavily lignified wall? <span class="marks">[1]</span>
   (a) parenchyma (b) collenchyma (c) sclerenchyma (d) chlorenchyma
7. The extra thickening of collenchyma is deposited mainly at the corners of the cell and consists of <span class="marks">[1]</span>
   (a) lignin (b) cellulose and pectin (c) suberin (d) cutin
8. The only living component of xylem is <span class="marks">[1]</span>
   (a) tracheid (b) vessel (c) xylem parenchyma (d) xylem fibre
9. A sieve tube element has no nucleus. It stays alive because of the help of <span class="marks">[1]</span>
   (a) guard cell (b) companion cell (c) bulliform cell (d) passage cell
10. The vascular bundles of a dicot stem are <span class="marks">[1]</span>
    (a) closed collateral (b) open collateral (c) radial (d) concentric
11. In a transverse section of a root the pith is large and there are eight xylem bundles. The root belongs to <span class="marks">[1]</span>
    (a) a dicot (b) a monocot (c) a gymnosperm (d) a secondary-thickened dicot
12. Casparian strips are bands of <span class="marks">[1]</span>
    (a) lignin on the outer wall of the epidermis (b) suberin on the radial and transverse walls of endodermal cells (c) cutin on the cortex (d) pectin on the pericycle
13. Passage cells of the endodermis are found opposite the <span class="marks">[1]</span>
    (a) protophloem (b) protoxylem (c) metaxylem (d) pith
14. Large thin-walled cells that help a grass leaf to roll inwards in dry weather are <span class="marks">[1]</span>
    (a) bulliform cells (b) guard cells (c) subsidiary cells (d) palisade cells
15. The phellogen cuts off phellem towards the ______ and phelloderm towards the ______. <span class="marks">[1]</span>
    (a) inside; outside (b) outside; inside (c) outside; outside (d) inside; inside
16. Heartwood differs from sapwood because it <span class="marks">[1]</span>
    (a) carries water upward (b) is lighter in colour (c) is dead, plugged with tyloses, tannin and resin, and gives only support (d) lies just below the bark
17. Which leaf has mesophyll that is not differentiated into palisade and spongy tissue? <span class="marks">[1]</span>
    (a) dorsiventral leaf of a dicot (b) isobilateral leaf of a monocot (c) the leaf of *Ligustrum* (d) the leaf of a mango

::: note Answers — 8.1
**1.** (c) — meristematic cells are the ones that *activate* cell division; option (d) describes a permanent cell, the very opposite.
**2.** (c) — aerenchyma has large air spaces. Stellate parenchyma is a kind of aerenchyma with star-shaped cells (banana petiole), but the general tissue that gives buoyancy is aerenchyma. Assimilatory parenchyma (chlorenchyma) is for photosynthesis.
**3.** (c) — endodermal cells with Casparian strips force water to pass through the living protoplast, so the endodermis controls what enters the stele. Option (a) is the *starch sheath* of a stem, a different endodermis.
**4.** (b) — the vascular cambium adds secondary xylem and phloem. Cork cambium is also a lateral meristem, but it makes periderm, not the vascular tissue that the word "stem growth" usually means; apical meristem gives primary growth only.
**5.** (a) — scattered bundles in undifferentiated ground tissue are the signature of a monocot stem. Option (c) is the opposite: monocot bundles are *closed*.
**6.** (c) — sclerenchyma cells are dead and lignified. Collenchyma is living, parenchyma is living.
**7.** (b) — cellulose with pectin, not lignin; lignin belongs to sclerenchyma and xylem.
**8.** (c) — xylem parenchyma stores food and is alive; tracheids, vessels and fibres are dead at maturity.
**9.** (b) — the companion cell, sister cell of the sieve element, supplies ATP and proteins. Bulliform and passage cells are in leaf and endodermis.
**10.** (b) — a cambium strip lies between xylem and phloem, so the bundle is open. Option (a) is monocot stem; radial bundles are in roots.
**11.** (b) — more than six xylem bundles (polyarch) and a large pith are monocot-root features. A dicot root has two to six arms and little or no pith.
**12.** (b) — suberin on radial and transverse walls; option (a) puts it on the epidermis, which is wrong.
**13.** (b) — passage cells sit opposite the protoxylem so that water can reach the xylem arms. Students often say "phloem" because they think of food, but passage cells serve inward water flow.
**14.** (a) — bulliform (motor) cells lose turgor and the leaf rolls. Guard cells open and close stomata, palisade cells photosynthesise.
**15.** (b) — phellem (cork) is cut outwards; phelloderm (secondary cortex) is cut inwards. Reversing them is the usual error.
**16.** (c) — heartwood is non-conducting. Option (d) describes sapwood, which is the living conducting region beneath the bark.
**17.** (b) — isobilateral leaves of monocots have similar mesophyll on both sides. *Ligustrum* (privet) is a dicot with a dorsiventral leaf.
:::

## 8.2 Plant Physiology

| High-yield fact | What to remember |
|---|---|
| Water potential | DPD (suction pressure) = OP − TP; water moves to the cell with the **larger DPD** (lower water potential). Turgid cell: TP = OP, DPD = 0, WP = 0. Flaccid: TP = 0, DPD = OP |
| Plasmolysis | protoplast shrinks from the wall in a hypertonic solution (exosmosis); reversible as deplasmolysis |
| Transpiration | ~90 % stomatal, ~10 % cuticular, <1 % lenticular; drives the ascent of sap by **cohesion–tension** (Dixon and Joly) |
| Guttation | liquid water from **hydathodes** at night, pushed by root pressure |
| Stomatal opening | light → K⁺ and malate enter guard cells → water enters → guard cells turgid → pore opens; ABA closes stomata |
| Photosynthesis | light reaction in **grana**; Calvin cycle in **stroma**; O₂ comes from **water** (Hill reaction; ¹⁸O experiments of Ruben and Kamen) |
| Photosystems | PS II reaction centre **P680**, PS I **P700**; non-cyclic: ATP + NADPH + O₂; cyclic: ATP only |
| Calvin cycle | RuBisCO fixes CO₂ on RuBP → 3-PGA (3C); per CO₂: 3 ATP + 2 NADPH; per glucose: 18 ATP + 12 NADPH |
| C4 and CAM | C4: PEP carboxylase, first product oxaloacetate (4C), **Kranz anatomy** (maize, sugarcane); CAM: stomata open at night (*Opuntia*, pineapple) |
| Respiration | glycolysis (EMP) in cytoplasm: net **2 ATP**, 2 NADH, 2 pyruvate; Krebs cycle in matrix; ETS on the inner mitochondrial membrane; classical 36–38 ATP, modern 30–32 |
| RQ | carbohydrate 1.0, fat ≈ 0.7, protein ≈ 0.8, organic acids > 1 |
| Hormones | **auxin** (apical dominance, rooting, parthenocarpy), **gibberellin** (bolting, internode elongation, bakanae), **cytokinin** (division, delays senescence), **ABA** (stress, dormancy, stomatal closure), **ethylene** (ripening) |
| Growth and movement | sigmoid growth curve: lag, log, stationary; tropisms are directional, nastic movements are not (*Mimosa* is seismonastic); vernalisation = cold induction of flowering |

```figure caption="The two-cell osmosis problem (NEB 2079, set N). Cell P: OP 15 atm, TP 10 atm, so DPD = 5 atm. Cell Q: OP 12 atm, TP 6 atm, so DPD = 6 atm. Water moves toward the larger DPD, from P to Q. The printed diagram in that paper showed TP = 10 atm for Q while the text said 6 atm; with 10 atm the DPD of Q would be 2 and the flow would reverse, so use the stated data of the text, which is the one that matches option (a)."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
fig, ax = plt.subplots(figsize=(4.7, 2.5)); ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 5.4)
for x0, name, op, tp in [(0.6, 'Cell P', 15, 10), (5.4, 'Cell Q', 12, 6)]:
    ax.add_patch(FancyBboxPatch((x0, 1.6), 3.9, 2.5, boxstyle='round,pad=0.05,rounding_size=0.6', fc='#eaf1fb', ec=INK, lw=1.1))
    ax.text(x0+1.95, 4.45, name, ha='center', fontsize=9, color=INK, fontweight='bold')
    ax.text(x0+1.95, 3.45, 'OP = %d atm' % op, ha='center', fontsize=8.2, color=INK)
    ax.text(x0+1.95, 2.85, 'TP = %d atm' % tp, ha='center', fontsize=8.2, color=INK)
    ax.text(x0+1.95, 2.0, 'DPD = %d atm' % (op-tp), ha='center', fontsize=8.6, color=ACCENT, fontweight='bold')
ax.annotate('', xy=(6.3, 0.95), xytext=(3.7, 0.95), arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=2.2, mutation_scale=16))
ax.text(5.0, 0.3, 'net water movement: P → Q', ha='center', fontsize=8, color=INK)
ax.text(5.0, 5.15, 'semi-permeable membrane between the cells', ha='center', fontsize=7, color=MUTED)
ax.plot([5.0, 5.0], [1.55, 4.15], color=MUTED, lw=1.0, ls=':')
```

1. Two cells P and Q lie in contact, separated by a semi-permeable membrane. The osmotic pressure of P is 15 atm and of Q is 12 atm; the turgor pressure of P is 10 atm and of Q is 6 atm. In which direction will water move? <span class="marks">[1]</span> (NEB 2079)
   (a) from P to Q (b) from Q to P (c) no movement of water (d) either way
2. Which one is the condition of a fully turgid cell? <span class="marks">[1]</span> (NEB 2080, options recast)
   (a) TP = 0 (b) WP = 0 (c) DPD = OP (d) OP = 0
3. Which one of the following parts is not responsible for transpiration in plants? <span class="marks">[1]</span> (NEB model 2079)
   (a) root (b) stem (c) leaves (d) all aerial parts
4. Which structure of a plant is primarily responsible for regulating transpiration? <span class="marks">[1]</span> (NEB 2082)
   (a) xylem (b) stomata (c) root hairs (d) phloem
5. A cell has an osmotic pressure of 12 atm and a turgor pressure of 8 atm. Its DPD is <span class="marks">[1]</span>
   (a) 20 atm (b) 4 atm (c) 12 atm (d) 96 atm
6. The cohesion–tension theory of the ascent of sap was proposed by <span class="marks">[1]</span>
   (a) Dixon and Joly (b) Münch (c) Went (d) Calvin and Benson
7. Loss of liquid water from leaf margins through hydathodes at night is <span class="marks">[1]</span>
   (a) transpiration (b) guttation (c) bleeding of a cut stem (d) imbibition
8. Stomata open in the morning because <span class="marks">[1]</span>
   (a) K⁺ leave the guard cells (b) K⁺ enter the guard cells, water follows and they become turgid (c) abscisic acid accumulates (d) starch is formed in guard cells
9. A plant cell is placed in a 10 % NaCl solution. The cell will <span class="marks">[1]</span>
   (a) swell and burst (b) become plasmolysed (c) become fully turgid (d) show no change
10. Some C4 plants show the diagnostic feature of Kranz anatomy. Which of these plants has it? <span class="marks">[1]</span> (NEB model 2079)
    (a) wheat (b) maize (c) barley (d) oats
11. The oxygen released in photosynthesis comes from <span class="marks">[1]</span>
    (a) carbon dioxide (b) glucose (c) water (d) RuBP
12. The reaction-centre chlorophyll *a* of photosystem I is <span class="marks">[1]</span>
    (a) P680 (b) P700 (c) P430 (d) P870
13. Cyclic photophosphorylation produces <span class="marks">[1]</span>
    (a) ATP, NADPH and O₂ (b) ATP only (c) NADPH only (d) O₂ and NADPH
14. The first stable product of carbon fixation in the Calvin cycle of a C3 plant is <span class="marks">[1]</span>
    (a) oxaloacetic acid (b) 3-phosphoglyceric acid (c) ribulose bisphosphate (d) pyruvic acid
15. For the fixation of one molecule of CO₂ in the Calvin cycle the plant needs <span class="marks">[1]</span>
    (a) 2 ATP and 3 NADPH (b) 3 ATP and 2 NADPH (c) 1 ATP and 1 NADPH (d) 6 ATP and 6 NADPH
16. In a C4 plant the enzyme that first fixes CO₂ in the mesophyll cell is <span class="marks">[1]</span>
    (a) RuBisCO (b) PEP carboxylase (c) pyruvate kinase (d) hexokinase
17. Stomata open only at night in <span class="marks">[1]</span>
    (a) maize (b) sugarcane (c) *Opuntia* (d) wheat
18. The net gain of ATP from glycolysis of one glucose molecule is <span class="marks">[1]</span>
    (a) 2 (b) 4 (c) 8 (d) 36
19. One glucose molecule, through two turns of the Krebs cycle, gives <span class="marks">[1]</span>
    (a) 2 NADH, 6 FADH₂, 2 ATP (b) 6 NADH, 2 FADH₂, 2 ATP (c) 8 NADH, 0 FADH₂, 4 ATP (d) 4 NADH, 4 FADH₂, 0 ATP
20. The electron transport system of a plant cell is located in the <span class="marks">[1]</span>
    (a) mitochondrial matrix (b) cytoplasm (c) inner mitochondrial membrane (d) outer mitochondrial membrane
21. If a plant is placed in a sealed bell jar with limited oxygen, what happens to its energy production over time? <span class="marks">[1]</span> (NEB 2082)
    (a) ATP increases because glycolysis rises (b) it relies on anaerobic respiration and makes less ATP (c) the citric acid cycle speeds up (d) the electron transport chain continues normally
22. The respiratory quotient when fat is the respiratory substrate is about <span class="marks">[1]</span>
    (a) 1.0 (b) 0.7 (c) 1.3 (d) zero
23. The end products of alcoholic fermentation in yeast are <span class="marks">[1]</span>
    (a) lactic acid and ATP (b) ethanol and CO₂ (c) pyruvate and water (d) acetyl CoA and NADH
24. Removal of the shoot tip makes the lateral buds sprout because the source of the inhibitor is removed. The inhibiting hormone is <span class="marks">[1]</span>
    (a) auxin (b) cytokinin (c) ethylene (d) gibberellin
25. What causes cell elongation in the internodal regions of plants? <span class="marks">[1]</span> (NEB 2081)
    (a) indole acetic acid (b) gibberellins (c) abscisic acid (d) cytokinins
26. The hormone that delays senescence of leaves and promotes cell division is <span class="marks">[1]</span>
    (a) abscisic acid (b) ethylene (c) cytokinin (d) auxin only
27. The gaseous hormone that hastens fruit ripening is <span class="marks">[1]</span>
    (a) ethylene (b) auxin (c) gibberellin (d) zeatin
28. The "foolish seedling" (bakanae) disease of rice led to the discovery of <span class="marks">[1]</span>
    (a) auxin (b) gibberellin (c) cytokinin (d) abscisic acid
29. The folding of the leaflets of *Mimosa pudica* on touch is an example of <span class="marks">[1]</span>
    (a) phototropism (b) seismonastic movement (c) geotropism (d) hydrotropism
30. The promotion of flowering by a period of low temperature is called <span class="marks">[1]</span>
    (a) photoperiodism (b) vernalisation (c) stratification (d) scarification

::: note Answers — 8.2
**1.** (a) — DPD of P = 15 − 10 = 5 atm, of Q = 12 − 6 = 6 atm. Water moves towards the larger DPD, so P → Q. Option (c) is the trap of comparing only the osmotic pressures or only the turgor pressures: P is larger in both, which gives a false "P is stronger" instinct. It is the *difference* that matters.
**2.** (b) — in a turgid cell TP = OP, so DPD = OP − TP = 0 and water potential is 0. Option (c) is a *flaccid* cell.
**3.** (a) — transpiration is loss from aerial parts; roots absorb water. Option (d) is true of transpiration, not its opposite.
**4.** (b) — guard cells change the pore size. Xylem and phloem only conduct.
**5.** (b) — DPD = OP − TP = 12 − 8 = 4 atm. Option (a) adds instead of subtracting.
**6.** (a) — Dixon and Joly (1894). Münch proposed the pressure-flow hypothesis for phloem; Went is auxin.
**7.** (b) — guttation is from hydathodes and needs root pressure. Bleeding is from a cut stem.
**8.** (b) — in light, K⁺ and malate accumulate, the guard cells take in water and bulge, pulling the stoma open. Option (c) is the closing signal.
**9.** (b) — the outside solution is hypertonic, water leaves, the protoplast shrinks away from the wall: plasmolysis. Bursting (a) is what animal cells do in hypotonic water.
**10.** (b) — maize is a C4 plant with a wreath (Kranz) of bundle-sheath cells. Wheat, barley and oats are C3 grasses, a favourite distractor set.
**11.** (c) — photolysis of water (Hill reaction; ¹⁸O in water appears in O₂). Students pick CO₂ because it is the gas that is "used".
**12.** (b) — P700 for PS I, P680 for PS II. P870 is bacterial.
**13.** (b) — electrons return to PS I, so there is no NADPH and, with no photolysis, no O₂.
**14.** (b) — 3-PGA (a 3-carbon acid). OAA is the first product in C4 plants; RuBP is the acceptor.
**15.** (b) — 3 ATP + 2 NADPH per CO₂, so 18 ATP and 12 NADPH for one glucose.
**16.** (b) — PEP carboxylase, which has no affinity for O₂, fixes HCO₃⁻ into oxaloacetate; RuBisCO works later, in the bundle sheath.
**17.** (c) — CAM plants open stomata at night to save water. Maize, sugarcane and wheat open them by day.
**18.** (a) — 4 ATP made, 2 spent: net 2. Option (b) is the gross yield.
**19.** (b) — one turn gives 3 NADH, 1 FADH₂ and 1 ATP/GTP; two turns double it. Option (a) swaps the two carriers.
**20.** (c) — the matrix holds the Krebs cycle; the ETS sits in the folded inner membrane.
**21.** (b) — with little O₂ the plant switches to fermentation, which yields only 2 ATP per glucose. Option (c) is wrong because the Krebs cycle also depends on O₂ through NAD⁺ regeneration.
**22.** (b) — fats are so oxygen-poor that more O₂ is used than CO₂ released (about 0.7). The value 1.0 is for carbohydrate.
**23.** (b) — pyruvate → acetaldehyde + CO₂ → ethanol. Lactic acid is the end product in muscle.
**24.** (a) — auxin from the apical bud suppresses lateral buds (apical dominance); cytokinin does the opposite.
**25.** (b) — gibberellins stretch internodes (bolting). Auxin also elongates cells, but the question keys the internodal response to gibberellin.
**26.** (c) — cytokinin. "Auxin only" cannot be right because auxin alone does not divide cells in culture.
**27.** (a) — ethylene is the only gaseous plant hormone. Option (d) zeatin is a cytokinin.
**28.** (b) — *Gibberella fujikuroi* secretes gibberellin; the infected rice grows tall and weak.
**29.** (b) — a touch-induced movement not directed by the stimulus is a nastic movement, here seismonastic. A tropism would bend *toward* the stimulus.
**30.** (b) — vernalisation; stratification and scarification are seed-dormancy treatments.
:::

## 8.3 Genetics

| High-yield fact | What to remember |
|---|---|
| Genetic material | Griffith (transformation), Avery–MacLeod–McCarty (DNA is the transforming principle), **Hershey–Chase** (³²P labels DNA, ³⁵S labels protein; DNA enters the bacterium) |
| DNA structure | Watson and Crick 1953; antiparallel; A=T (2 H-bonds), G≡C (3 H-bonds); B-DNA: 10 bp per turn, pitch **3.4 nm**, diameter 2 nm; Chargaff: A = T and G = C |
| Replication | **semi-conservative** (Meselson–Stahl, ¹⁵N/¹⁴N); helicase, SSB, primase, DNA polymerase III, polymerase I, **ligase**; leading strand continuous, lagging strand in **Okazaki** fragments |
| Code | 64 codons, 61 sense + 3 stop (UAA, UAG, UGA); start AUG; degenerate, universal, non-overlapping, commaless |
| Expression | transcription (RNA polymerase, nucleus) → mRNA → translation (ribosome, tRNA anticodon reads codon) |
| Mendel | monohybrid F₂ 3 : 1 (genotype 1 : 2 : 1); test cross 1 : 1; dihybrid 9 : 3 : 3 : 1 with 9 genotypes and 4 phenotypes |
| Post-Mendelian | incomplete dominance 1 : 2 : 1 (*Mirabilis jalapa*); codominance (roan cattle, AB group); multiple alleles I^A, I^B, i |
| Sex-linkage | colour blindness and haemophilia are X-linked recessive; **criss-cross** inheritance (father → daughter → grandson); *Drosophila* white eye (Morgan) |
| Linkage and crossing over | linked genes inherited together; crossing over between non-sister chromatids at **pachytene**; 1 % recombination = 1 map unit |
| Gene mutation | point: substitution (transition purine↔purine, transversion purine↔pyrimidine); **frame shift** by insertion or deletion of a base; sickle-cell anaemia is a point mutation (Glu → Val) |
| Chromosomal | deletion, duplication, inversion, translocation; aneuploidy: monosomy 2n − 1, trisomy 2n + 1; Down = trisomy 21, Turner = 45, X, Klinefelter = 47, XXY |
| Polyploidy | extra whole sets; induced by **colchicine**; triticale (wheat × rye) is an allopolyploid |

```figure caption="Complete dominance against incomplete dominance. The genotypic ratio is 1 : 2 : 1 in both, but the phenotypic ratio is 3 : 1 when R is dominant and 1 : 2 : 1 when neither allele dominates (*Mirabilis jalapa*, four o'clock plant)."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, axes = plt.subplots(1, 2, figsize=(4.8, 2.55))
col = {'RR': '#d94b4b', 'Rr': '#d94b4b', 'rr': '#f3f3f3'}
col2 = {'RR': '#d94b4b', 'Rr': '#f0a3b6', 'rr': '#f3f3f3'}
for ax, cm, title, foot in [(axes[0], col, 'Complete dominance', '3 red : 1 white'), (axes[1], col2, 'Incomplete dominance', '1 red : 2 pink : 1 white')]:
    ax.set_xlim(-0.2, 3.3); ax.set_ylim(0.3, 3.35); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title(title, fontsize=7.6, color=INK, pad=2)
    ax.text(1.5, 3.05, 'Rr × Rr', ha='center', fontsize=7, color=MUTED)
    gam = ['R', 'r']
    for j, g in enumerate(gam):
        ax.text(1.1 + 1.0*j, 2.45, g, ha='center', va='center', fontsize=8, color=INK)
        ax.text(0.45, 1.6 - 1.0*j + 0.0, g, ha='center', va='center', fontsize=8, color=INK)
    for i in range(2):
        for j in range(2):
            gt = ''.join(sorted(gam[i] + gam[j]))
            gt = 'RR' if gt == 'RR' else ('rr' if gt == 'rr' else 'Rr')
            ax.add_patch(Rectangle((0.6 + 1.0*j, 1.1 - 1.0*i + 0.0), 1.0, 1.0, fc=cm[gt], ec=INK, lw=0.8))
            ax.text(1.1 + 1.0*j, 1.6 - 1.0*i, gt, ha='center', va='center', fontsize=8, color=INK if gt != 'RR' else 'white')
    ax.text(1.6, 0.68, foot, ha='center', fontsize=7.2, color=INK, fontweight='bold')
fig.subplots_adjust(left=0.01, right=0.99, top=0.93, bottom=0.03, wspace=0.05)
```

1. In a monohybrid cross of two heterozygous parents (Rr × Rr), what genotypes are expected among the offspring? <span class="marks">[1]</span> (NEB 2079; option (a) was misprinted in the paper and is corrected here)
   (a) 1 RR : 2 Rr : 1 rr (b) 1 rr : 3 RR (c) 3 Rr : 1 rr (d) all Rr
2. Which type of mutation is caused by the addition or deletion of a single nitrogenous base? <span class="marks">[1]</span> (NEB model 2079)
   (a) transition (b) transversion (c) frame shift (d) substitution
3. Two pea plants with red flowers, genotypes unknown, are crossed and give red and white flowers in the ratio 3 : 1. What are the genotypes of the parents? <span class="marks">[1]</span> (NEB 2080, ratio recast as 3 : 1)
   (a) both homozygous (b) one homozygous, one heterozygous (c) both heterozygous (d) both hemizygous
4. Marriage of a man of normal vision with a colour-blind woman will produce <span class="marks">[1]</span> (NEB 2080)
   (a) normal sons and normal daughters (b) colour-blind sons and carrier daughters (c) colour-blind sons and colour-blind daughters (d) normal sons and carrier daughters
5. A heterozygous individual AaBb is crossed with another AaBb. What is the probability that an offspring shows the recessive phenotype for both traits? <span class="marks">[1]</span> (NEB 2081)
   (a) 1/4 (b) 1/8 (c) 1/16 (d) 1/32
6. Which genotype represents monosomy, a type of aneuploidy? <span class="marks">[1]</span> (NEB 2081)
   (a) 2n − 2 (b) 2n − 1 (c) 2n + 1 (d) 2n + 1 + 1
7. Which of the following genetic disorders is caused by a point mutation? <span class="marks">[1]</span> (NEB 2082)
   (a) Down's syndrome (b) Turner's syndrome (c) sickle-cell anaemia (d) Klinefelter's syndrome
8. In the Hershey–Chase experiment the DNA of the bacteriophage was labelled with <span class="marks">[1]</span>
   (a) ³⁵S (b) ³²P (c) ¹⁴C (d) ¹⁵N
9. A DNA sample contains 30 % adenine. The percentage of guanine is <span class="marks">[1]</span>
   (a) 20 (b) 30 (c) 40 (d) 70
10. The number of hydrogen bonds between guanine and cytosine is <span class="marks">[1]</span>
    (a) 1 (b) 2 (c) 3 (d) 4
11. One complete turn of B-DNA is <span class="marks">[1]</span>
    (a) 0.34 nm with 1 bp (b) 3.4 nm with 10 bp (c) 34 nm with 100 bp (d) 2 nm with 10 bp
12. *E. coli* grown for many generations in ¹⁵N medium is shifted to ¹⁴N medium. After two generations of division the DNA is <span class="marks">[1]</span>
    (a) all heavy (b) all hybrid (c) half hybrid and half light (d) all light
13. Short fragments formed on the lagging strand are joined by <span class="marks">[1]</span>
    (a) helicase (b) primase (c) DNA ligase (d) RNA polymerase
14. Which of these is a stop codon? <span class="marks">[1]</span>
    (a) AUG (b) UGA (c) UGG (d) UUU
15. If the codon on the mRNA is GCA, the anticodon of the tRNA is <span class="marks">[1]</span>
    (a) CGU (b) CGT (c) GCA (d) UGC
16. The enzyme that synthesises mRNA from a DNA template is <span class="marks">[1]</span>
    (a) DNA polymerase (b) RNA polymerase (c) reverse transcriptase (d) ligase
17. The testcross of a tall plant (T?) with a dwarf plant gives 1 tall : 1 dwarf. The tall parent was <span class="marks">[1]</span>
    (a) TT (b) Tt (c) tt (d) cannot be known
18. The F₂ phenotypic ratio in a cross between red (RR) and white (rr) four o'clock plants is <span class="marks">[1]</span>
    (a) 3 : 1 (b) 1 : 2 : 1 (c) 9 : 3 : 3 : 1 (d) 1 : 1
19. A man of blood group A and a woman of blood group B have a child of group O. The genotypes of the parents must be <span class="marks">[1]</span>
    (a) I^A I^A and I^B I^B (b) I^A i and I^B i (c) I^A I^A and I^B i (d) I^A i and I^B I^B
20. The grandson of a colour-blind man can receive the gene only through <span class="marks">[1]</span>
    (a) his father (b) his carrier mother, who got it from the colour-blind man (c) his grandmother's brother (d) an autosome
21. *Drosophila melanogaster* was chosen for genetic studies mainly because it <span class="marks">[1]</span>
    (a) has a long life cycle (b) has a short life cycle, few chromosomes and many progeny (c) is a plant (d) has no sex chromosomes
22. Crossing over takes place at the ______ stage of meiosis I. <span class="marks">[1]</span>
    (a) leptotene (b) zygotene (c) pachytene (d) diakinesis
23. If the frequency of crossing over between genes A and B is 8 %, the distance between them is <span class="marks">[1]</span>
    (a) 8 map units (b) 0.8 map units (c) 92 map units (d) 16 map units
24. Two genes are closely linked. The frequency of recombination between them will be <span class="marks">[1]</span>
    (a) high (b) low (c) 50 % always (d) 100 %
25. The chromosome number of a person with Down's syndrome is <span class="marks">[1]</span>
    (a) 45 (b) 46 (c) 47 (d) 48
26. A woman with 45 chromosomes and the sex-chromosome constitution XO has <span class="marks">[1]</span>
    (a) Klinefelter's syndrome (b) Turner's syndrome (c) Down's syndrome (d) Patau's syndrome
27. Polyploidy in plants is induced artificially by <span class="marks">[1]</span>
    (a) colchicine (b) ethylene (c) gibberellin (d) ethidium bromide
28. Triticale, a man-made cereal, is <span class="marks">[1]</span>
    (a) an autotriploid (b) an allopolyploid of wheat and rye (c) a transgenic plant (d) a haploid

::: note Answers — 8.3
**1.** (a) — Rr × Rr gives 1 RR : 2 Rr : 1 rr. The printed option was a typo for RR; note the answer is a *genotypic* 1 : 2 : 1, not the phenotypic 3 : 1, and (c) mixes the two.
**2.** (c) — inserting or deleting one base shifts every codon after it. Transition and transversion only *replace* a base.
**3.** (c) — Rr × Rr gives 3 red : 1 white. Two homozygotes (a) or one of each (b) would give no white offspring at all.
**4.** (b) — X^cX^c × X^CY: every son gets the mother's X^c and is colour-blind; every daughter gets X^C from the father and X^c from the mother, so she is a carrier. Option (d) swaps the sexes.
**5.** (c) — probability of aa = 1/4 and of bb = 1/4, so (1/4)(1/4) = 1/16. Option (a) counts only one trait.
**6.** (b) — monosomy is 2n − 1. 2n − 2 is nullisomy, 2n + 1 trisomy, 2n + 1 + 1 double trisomy.
**7.** (c) — sickle-cell anaemia is one base change (GAG → GTG), Glu → Val. Down, Turner and Klinefelter are chromosome-number changes.
**8.** (b) — phosphorus is in DNA; sulphur is in protein, so ³⁵S labels the protein coat. Choosing ³⁵S is the classic slip.
**9.** (a) — A = T = 30 %, so G + C = 40 %, G = 20 %.
**10.** (c) — G≡C has three, A=T has two.
**11.** (b) — 10 bp × 0.34 nm = 3.4 nm; (d) is the *diameter*.
**12.** (c) — the first generation is all hybrid (¹⁵N/¹⁴N); the second is half hybrid and half light. Semi-conservative replication never gives all-heavy after a shift.
**13.** (c) — DNA ligase seals the nicks between Okazaki fragments. Primase makes the primers; helicase unwinds.
**14.** (b) — the stop codons are UAA, UAG, UGA. AUG is the start codon and also codes Met; UGG is Trp.
**15.** (a) — the anticodon pairs with the codon: G–C, C–G, A–U gives CGU. Option (b) contains T, which tRNA does not have.
**16.** (b) — transcription uses RNA polymerase; reverse transcriptase makes DNA from RNA.
**17.** (b) — a 1 : 1 testcross ratio shows a heterozygous parent; TT would give all tall.
**18.** (b) — incomplete dominance gives 1 red : 2 pink : 1 white. The figure shows it beside complete dominance.
**19.** (b) — the O child has two *i* alleles, one from each parent, so both parents are heterozygous.
**20.** (b) — the colour-blind man gives his X only to his daughters; she passes it to her son (criss-cross). Option (a) is wrong because a father gives his son a Y.
**21.** (b) — 2n = 8, a life cycle of about 10–14 days, and hundreds of offspring per mating.
**22.** (c) — crossing over happens at pachytene; chiasmata become visible at diplotene. Students choose diplotene because they *see* the chiasma then.
**23.** (a) — 1 % recombination = 1 map unit.
**24.** (b) — closer genes are crossed over less often.
**25.** (c) — trisomy 21 gives 47 chromosomes. 45 is Turner.
**26.** (b) — 45, X is Turner; Klinefelter is 47, XXY.
**27.** (a) — colchicine blocks spindle formation, so chromosomes double without division.
**28.** (b) — triticale is wheat (*Triticum*) × rye (*Secale*), doubled with colchicine.
:::

## 8.4 Embryology

| High-yield fact | What to remember |
|---|---|
| Vegetative propagation | natural: runners, rhizomes, tubers, bulbs, leaf buds (*Bryophyllum*); artificial: cutting, **layering** (simple/soil layering keeps the branch attached to the parent), grafting (stock + scion), budding |
| Apomixis and relatives | **parthenogenesis** = embryo from an unfertilised egg; **parthenocarpy** = fruit without fertilisation (seedless banana, grape) |
| Pollination | autogamy, geitonogamy (same plant), xenogamy (different plants); wind-pollinated flowers: light dry pollen, feathery stigma |
| Pollen grain | exine of **sporopollenin**; generative cell → 2 male gametes; vegetative (tube) cell; formed in microsporangia from microspore mother cells; **tapetum** nourishes |
| Embryo sac (Polygonum type) | 7 cells, 8 nuclei: egg apparatus (egg + 2 synergids) at the micropylar end, 3 antipodals at the chalazal end, central cell with 2 polar nuclei |
| Entry of pollen tube | porogamy (through micropyle, commonest), chalazogamy (*Casuarina*), mesogamy (through integument) |
| Double fertilisation | Nawaschin (1898): syngamy gives 2n zygote; triple fusion gives **3n primary endosperm nucleus** |
| After fertilisation | synergids and antipodals degenerate; ovule → seed, ovary → fruit, integument → seed coat |
| Embryo | dicot: radicle, plumule, hypocotyl, 2 cotyledons, suspensor; monocot: **scutellum** (one cotyledon), coleoptile, coleorhiza |
| Endosperm | nuclear (coconut water), cellular, helobial; 3n tissue that feeds the embryo |

```figure caption="Mature embryo sac of an angiosperm (Polygonum type): seven cells, eight nuclei. The micropyle, where the pollen tube enters, is at the top."
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle
fig, ax = plt.subplots(figsize=(4.3, 3.6)); ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 10.6)
ax.add_patch(Ellipse((4.0, 5.3), 5.0, 9.4, fc='#fdf6e3', ec=INK, lw=1.3))
ax.add_patch(Ellipse((3.2, 8.7), 1.25, 1.35, fc='#fff3c4', ec=INK, lw=0.9))
ax.add_patch(Ellipse((4.85, 8.7), 1.25, 1.35, fc='#fff3c4', ec=INK, lw=0.9))
ax.add_patch(Ellipse((4.0, 7.4), 1.55, 1.3, fc='#ffd7d7', ec=INK, lw=0.9))
for x, y in [(3.2, 8.75), (4.85, 8.75), (4.0, 7.4)]:
    ax.add_patch(Circle((x, y), 0.26, fc='#5a6fa8', ec=INK, lw=0.6))
ax.add_patch(Ellipse((4.0, 5.3), 3.0, 2.2, fc='#e9f3ff', ec=INK, lw=0.8))
ax.add_patch(Circle((3.45, 5.3), 0.32, fc='#5a6fa8', ec=INK, lw=0.6)); ax.add_patch(Circle((4.55, 5.3), 0.32, fc='#5a6fa8', ec=INK, lw=0.6))
for x in [2.75, 4.0, 5.25]:
    ax.add_patch(Ellipse((x, 1.75), 1.15, 1.15, fc='#dff2d9', ec=INK, lw=0.9)); ax.add_patch(Circle((x, 1.75), 0.24, fc='#5a6fa8', ec=INK, lw=0.6))
for txt, xy, tx in [('synergids', (3.2, 8.95), (7.6, 9.4)), ('egg cell', (4.0, 7.6), (7.6, 7.9)),
                    ('polar nuclei', (4.55, 5.35), (7.6, 5.9)), ('central cell', (5.3, 4.6), (7.6, 4.6)),
                    ('antipodal cells', (5.25, 1.85), (7.6, 1.85)), ('embryo sac wall', (6.45, 3.4), (7.6, 3.2))]:
    ax.annotate(txt, xy=xy, xytext=tx, fontsize=7.4, color=INK, va='center', arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7, shrinkA=1, shrinkB=1))
ax.text(4.0, 0.25, 'chalazal end', ha='center', fontsize=7, color=MUTED)
ax.text(1.0, 10.15, 'micropylar end', ha='center', fontsize=7, color=MUTED)
```

1. Which of the following cells of an embryo sac degenerate after fertilisation? <span class="marks">[1]</span> (NEB 2079)
   (a) synergids and the primary endosperm cell (b) synergids and antipodal cells (c) antipodal cells and the primary endosperm cell (d) the egg and antipodal cells
2. What is the development of an embryo from an unfertilised egg called? <span class="marks">[1]</span> (NEB model 2079)
   (a) parthenocarpy (b) parthenogenesis (c) polyembryony (d) polycarpy
3. In porogamy, through which structure does the pollen tube enter the ovule? <span class="marks">[1]</span> (NEB 2080; turned round in NEB 2082)
   (a) chalazal end (b) integument (c) micropyle (d) ovary wall
4. What is the development of a fruit without fertilisation called? <span class="marks">[1]</span> (NEB 2081)
   (a) parthenocarpy (b) apomixis (c) polyspory (d) parthenogenesis
5. Which type of artificial vegetative propagation induces roots on a branch while it is still attached to the parent plant, and suits plants with soft branches lying near the soil? <span class="marks">[1]</span> (NEB 2081)
   (a) air layering (b) grafting (c) soil layering (d) cutting
6. The number of cells and nuclei in a mature Polygonum-type embryo sac are <span class="marks">[1]</span>
   (a) 8 cells, 7 nuclei (b) 7 cells, 8 nuclei (c) 8 cells, 8 nuclei (d) 7 cells, 7 nuclei
7. Triple fusion in an angiosperm forms <span class="marks">[1]</span>
   (a) the zygote (b) a 3n primary endosperm nucleus (c) the embryo (d) the suspensor
8. Double fertilisation in angiosperms was discovered by <span class="marks">[1]</span>
   (a) Strasburger (b) Nawaschin (c) Hofmeister (d) Mendel
9. The hard outer layer of the pollen grain, resistant to acid, alkali and heat, is made of <span class="marks">[1]</span>
   (a) cellulose (b) pectin (c) sporopollenin (d) callose
10. The nutritive layer of the anther wall that supplies food to developing pollen grains is the <span class="marks">[1]</span>
    (a) epidermis (b) endothecium (c) middle layer (d) tapetum
11. Pollen grains from the anther of a flower reach the stigma of another flower of the same plant. This is <span class="marks">[1]</span>
    (a) autogamy (b) geitonogamy (c) xenogamy (d) cleistogamy
12. Which feature is typical of a wind-pollinated flower? <span class="marks">[1]</span>
    (a) large coloured petals and nectar (b) light dry pollen and feathery stigma (c) sticky heavy pollen (d) sweet scent
13. The single cotyledon of a monocot embryo is called <span class="marks">[1]</span>
    (a) coleoptile (b) scutellum (c) coleorhiza (d) plumule
14. The free-nuclear endosperm is seen in <span class="marks">[1]</span>
    (a) coconut (b) pea (c) wheat grain after maturity (d) orchid
15. In the dicot embryo the portion between the plumule and the radicle is the <span class="marks">[1]</span>
    (a) epicotyl only (b) hypocotyl (c) suspensor (d) scutellum
16. The ovule develops into a ______ and the ovary into a ______. <span class="marks">[1]</span>
    (a) fruit; seed (b) seed; fruit (c) embryo; endosperm (d) seed coat; pericarp only

::: note Answers — 8.4
**1.** (b) — synergids and antipodals have done their job and disappear; the primary endosperm cell *divides* to form endosperm. Option (a) is the trap: the endosperm cell is the busiest cell after fertilisation.
**2.** (b) — parthenogenesis is about the *egg*; parthenocarpy (a) is about the *fruit*. The two words differ by one syllable and exam setters exploit it.
**3.** (c) — micropylar entry is porogamy. In 2082 the question was reversed: "which term describes entry through the micropyle" with options mesogamy, chalazogamy, syngamy, porogamy.
**4.** (a) — seedless banana and grape are parthenocarpic. Parthenogenesis (d) is an egg developing without fertilisation.
**5.** (c) — in simple (soil) layering the branch is bent into the soil while still attached and roots then form. Air layering works on upright branches, and grafting and cutting detach the piece at once.
**6.** (b) — seven cells but eight nuclei because the central cell carries two polar nuclei.
**7.** (b) — one sperm nucleus + two polar nuclei = 3n. The zygote (a) comes from syngamy.
**8.** (b) — Nawaschin (1898, *Fritillaria* and *Lilium*), confirmed by Guignard. Strasburger described the embryo sac and fertilisation, not the double event.
**9.** (c) — sporopollenin, one of the most resistant organic materials. Callose is found around microspore mother cells and in pollen tubes.
**10.** (d) — the tapetum; the endothecium helps dehiscence.
**11.** (b) — the flowers are on the *same plant*, so it is geitonogamy; it is genetically autogamy but ecologically cross-pollination. Xenogamy needs two plants.
**12.** (b) — wind-pollinated flowers are small, dull and produce huge amounts of light dry pollen. Colour, scent and sticky pollen are insect-pollination features.
**13.** (b) — scutellum; coleoptile and coleorhiza are protective sheaths of the plumule and radicle.
**14.** (a) — coconut water is free-nuclear endosperm; the white kernel is the later cellular stage.
**15.** (b) — the hypocotyl lies below the cotyledons and ends in the radicle; the epicotyl lies above them.
**16.** (b) — ovule → seed, ovary → fruit. Reversed, it is the commonest slip.
:::

## 8.5 Biotechnology

| High-yield fact | What to remember |
|---|---|
| Totipotency | every living plant cell can, in principle, regenerate a whole plant (Haberlandt) |
| Culture medium | **MS (Murashige–Skoog)** medium with sucrose, vitamins and growth regulators; high auxin : cytokinin → roots; high cytokinin : auxin → shoots; balanced → **callus** |
| Kinds of culture | meristem (virus-free plants), embryo culture (rescues embryos that would die), anther culture (haploids), protoplast fusion (somatic hybrids) |
| Micropropagation | clonal multiplication from small explants in aseptic conditions; used for orchids, banana, potato; useful for rare plants |
| Breeding | selection, introduction, **hybridisation** (F₁ shows heterosis, hybrid vigour), mutation breeding, polyploidy |
| Disease resistance | breeding for resistance, meristem culture for virus-free stock, transgenics (Bt) |
| Bio-inputs | green manure (*Sesbania*, *Crotalaria*), biofertiliser (*Rhizobium*, *Azotobacter*, *Azolla* + *Anabaena*), biopesticide (*Bacillus thuringiensis*, *Trichoderma*, NPV) |
| Genetic engineering | restriction enzymes cut, ligase joins, vectors carry (plasmid, *Agrobacterium* Ti plasmid); GMOs: Bt cotton, Golden Rice |
| Food | **food security** = access to enough food at all times; **food safety** = food free of hazards such as toxins and pathogens |

```photo id="qbank/plant-callus" caption="A callus growing on Murashige–Skoog medium. Callus is an undifferentiated mass of parenchyma-like cells; change the auxin : cytokinin ratio and it will form roots or shoots." width="64"
crop 0.08 0.02 0.92 0.42
mark 0.38 0.50 "1"
mark 0.80 0.80 "2"
key 1 Callus (undifferentiated cell mass)
key 2 Culture medium in the glass vessel
```

1. In an economically important plant species embryo mortality is very high. Which method would you suggest to check the mortality? <span class="marks">[1]</span> (NEB 2079)
   (a) micropropagation (b) polyploid mutation (c) embryo culture (d) meristem culture
2. Who proposed the concept of totipotency of plant cells? <span class="marks">[1]</span>
   (a) Haberlandt (b) Skoog (c) Steward (d) Murashige
3. A high concentration of cytokinin relative to auxin in the medium promotes <span class="marks">[1]</span>
   (a) root formation (b) shoot formation (c) only callus (d) cell death
4. Virus-free plants are obtained by culturing <span class="marks">[1]</span>
   (a) leaf segments (b) anthers (c) shoot-tip meristem (d) roots
5. Haploid plants are produced in the laboratory by <span class="marks">[1]</span>
   (a) anther culture (b) embryo culture (c) meristem culture (d) root culture
6. Somatic hybrids are produced by the fusion of <span class="marks">[1]</span>
   (a) pollen and egg (b) two protoplasts from different species (c) two pollen grains (d) two gametes of the same plant
7. The first generation of a cross between two pure lines often grows better than both parents. This is called <span class="marks">[1]</span>
   (a) inbreeding depression (b) heterosis (c) apomixis (d) polyploidy
8. The *cry* gene in Bt cotton comes from <span class="marks">[1]</span>
   (a) *Agrobacterium tumefaciens* (b) *Bacillus thuringiensis* (c) *Rhizobium* (d) *E. coli*
9. A common vector used to introduce a foreign gene into a dicot plant is <span class="marks">[1]</span>
   (a) the Ti plasmid of *Agrobacterium* (b) the bacteriophage λ only (c) a retrovirus (d) a cosmid of yeast
10. The enzyme that cuts DNA at specific base sequences is <span class="marks">[1]</span>
    (a) ligase (b) restriction endonuclease (c) DNA polymerase (d) helicase
11. Which of the following is used as a green manure crop in Nepal? <span class="marks">[1]</span>
    (a) *Sesbania* (b) wheat (c) maize (d) mustard
12. *Azolla* is used as a biofertiliser because it lives with a nitrogen-fixing <span class="marks">[1]</span>
    (a) *Rhizobium* (b) *Anabaena* (c) *Azotobacter* (d) *Nostoc* only
13. Golden Rice was developed to overcome the deficiency of <span class="marks">[1]</span>
    (a) vitamin A (b) iron (c) iodine (d) vitamin C
14. Food that is free from toxins and disease-causing organisms is a matter of <span class="marks">[1]</span>
    (a) food security (b) food safety (c) food sovereignty (d) food processing

::: note Answers — 8.5
**1.** (c) — embryo culture rescues weak or aborting embryos by growing them on medium. Meristem culture (d) gives virus-free plants, a different aim.
**2.** (a) — Gottlieb Haberlandt (1902). Skoog and Miller found kinetin; Murashige and Skoog gave the medium.
**3.** (b) — high cytokinin : auxin → shoots; the reverse → roots; a balance → callus. Reversing the ratio is the usual error.
**4.** (c) — the apical meristem is usually free of virus because it has no vascular connection.
**5.** (a) — anther (or pollen) culture gives haploids, which doubling then turns into homozygous diploids.
**6.** (b) — protoplast fusion bypasses sexual barriers (pomato). Fusion of gametes is ordinary fertilisation.
**7.** (b) — heterosis or hybrid vigour; inbreeding depression is the opposite.
**8.** (b) — the *cry* gene codes Cry protein, toxic to bollworm. *Agrobacterium* supplies the vector, which is why (a) tempts.
**9.** (a) — the Ti plasmid transfers T-DNA into dicot cells.
**10.** (b) — restriction endonuclease; ligase joins, it does not cut.
**11.** (a) — *Sesbania* (dhaincha) is ploughed in while green; wheat and maize are grain crops.
**12.** (b) — *Azolla* fixes nitrogen through *Anabaena azollae*. *Rhizobium* lives in legume nodules.
**13.** (a) — Golden Rice makes β-carotene, the precursor of vitamin A.
**14.** (b) — safety is about hazards; security (a) is about availability and access.
:::

## 8.6 Animal Tissues

| High-yield fact | What to remember |
|---|---|
| Simple epithelia | squamous (alveoli, blood vessels, Bowman's capsule; "pavement"), cuboidal (thyroid follicle, PCT with brush border), columnar (stomach, intestine; with goblet cells), ciliated columnar (trachea, oviduct), pseudostratified |
| Compound epithelia | stratified squamous keratinised (epidermis), **non-keratinised** (vagina, oesophagus, mouth), transitional (bladder, ureter) |
| Areolar tissue | loose; fibroblasts, **mast cells** (histamine, heparin), macrophages; packing tissue under skin |
| Dense connective | **tendon** joins muscle to bone; **ligament** joins bone to bone |
| Adipose tissue | fat globules; storage, insulation, cushion |
| Cartilage | hyaline (nose, trachea, articular ends), elastic (pinna, epiglottis), fibrocartilage (intervertebral disc); matrix chondroitin sulphate; **no blood supply** (avascular) |
| Bone | osteocytes in lacunae, matrix of calcium phosphate + collagen, Haversian canals with blood vessels |
| Blood | plasma 55 %; RBC, WBC (granulocytes: neutrophil, eosinophil, basophil; agranulocytes: lymphocyte, monocyte), platelets; **phagocytes**: neutrophils and monocytes |
| Muscle | skeletal (striated, voluntary, multinucleate); cardiac (striated, involuntary, branched, **intercalated discs**); smooth (unstriated, involuntary, spindle) |
| Nervous tissue | neuron = cell body + dendrites + axon; myelin sheath from Schwann cells; neuroglia support |

```photo id="qbank/blood-leukocytes" caption="A human blood smear (haematoxylin–eosin, ×400). The pink discs are red blood cells, which have no nucleus. The few cells with dark-purple nuclei are leucocytes (white cells): one has a small round dense nucleus (a lymphocyte) and three have a nucleus cut into lobes — neutrophils, the commonest phagocytic white cell. Platelets are the tiny fragments between the red cells." width="90"
call 0.60 0.50 0.462 0.385 "neutrophil (lobed nucleus)"
call 0.74 0.40 0.888 0.245 "neutrophil"
call 0.55 0.08 0.392 0.172 "neutrophil"
call 0.80 0.08 0.677 0.155 "another leucocyte"
call 0.64 0.78 0.81 0.575 "red blood cell"
call 0.27 0.52 0.337 0.355 "lymphocyte"
```

1. Which of the following tissues possesses fat globules? <span class="marks">[1]</span> (NEB 2079)
   (a) areolar tissue (b) adipose tissue (c) blood plasma (d) striped muscle
2. Which of the following tissues lacks a blood supply? <span class="marks">[1]</span> (NEB model 2079)
   (a) areolar (b) muscular (c) bone (d) cartilage
3. Which pair of white blood cells contains phagocytic cells? <span class="marks">[1]</span> (NEB 2081)
   (a) monocytes and eosinophils (b) monocytes and neutrophils (c) eosinophils and basophils (d) monocytes and lymphocytes
4. Which epithelium forms the inner lining of the vagina? <span class="marks">[1]</span> (NEB 2081)
   (a) columnar (b) cuboidal (c) stratified keratinised squamous (d) stratified non-keratinised squamous
5. Which cells of connective tissue produce histamine and heparin? <span class="marks">[1]</span> (NEB 2082, wording recast)
   (a) plasma cells (b) macrophages (c) fibroblasts (d) mast cells
6. Which epithelium lines the air sacs (alveoli) of the lung? <span class="marks">[1]</span>
   (a) simple cuboidal (b) simple squamous (c) simple columnar (d) transitional
7. The epithelium that can stretch when the urinary bladder is filled is <span class="marks">[1]</span>
   (a) transitional (b) simple squamous (c) simple cuboidal (d) ciliated columnar
8. Tendon and ligament are both <span class="marks">[1]</span>
   (a) dense regular connective tissue (b) adipose tissue (c) loose connective tissue (d) fibrocartilage
9. A ligament connects <span class="marks">[1]</span>
   (a) muscle to bone (b) bone to bone (c) muscle to muscle (d) skin to muscle
10. The cartilage in the external ear (pinna) is <span class="marks">[1]</span>
    (a) hyaline (b) elastic (c) fibrocartilage (d) calcified
11. The cells of bone that lie in lacunae are <span class="marks">[1]</span>
    (a) osteoblasts only (b) osteocytes (c) chondrocytes (d) fibroblasts
12. Muscle fibres that are striated and branched and join end to end through intercalated discs are <span class="marks">[1]</span>
    (a) skeletal (b) cardiac (c) smooth (d) visceral
13. Which muscle is involuntary and non-striated? <span class="marks">[1]</span>
    (a) biceps (b) heart muscle (c) muscle of the intestinal wall (d) tongue muscle
14. The fatty insulating sheath around an axon in peripheral nerves is formed by <span class="marks">[1]</span>
    (a) oligodendrocytes (b) Schwann cells (c) astrocytes (d) microglia
15. The type of cell that makes up about 99 % of the formed elements of blood is <span class="marks">[1]</span>
    (a) RBC (b) WBC (c) platelets (d) plasma cell
16. Squamous epithelium is also called pavement epithelium because <span class="marks">[1]</span>
    (a) it is found on roads (b) its flat cells fit edge to edge like paving stones (c) its cells are cube shaped (d) it is ciliated

::: note Answers — 8.6
**1.** (b) — adipose tissue stores fat globules. Areolar tissue (a) is the commoner distractor because it is also loose and sits beside fat.
**2.** (d) — cartilage is avascular and is fed by diffusion from the perichondrium. Bone (c) has Haversian canals full of vessels.
**3.** (b) — neutrophils and monocytes (which become macrophages) are the professional phagocytes; eosinophils are weakly phagocytic, lymphocytes are not.
**4.** (d) — the vagina is a moist internal passage, so its stratified squamous epithelium is *non-keratinised*. Keratinised squamous (c) is the epidermis.
**5.** (d) — mast cell granules hold histamine and heparin. Plasma cells make antibodies.
**6.** (b) — a single flat layer keeps the diffusion distance small. Cuboidal lines kidney tubules.
**7.** (a) — transitional epithelium lets the cells slide over one another.
**8.** (a) — both are dense regular connective tissue rich in collagen; they differ in what they join. Fibrocartilage (d) is found in the disc.
**9.** (b) — ligament is bone to bone; tendon is muscle to bone (option a).
**10.** (b) — elastic cartilage springs back; hyaline is at the articular ends and trachea.
**11.** (b) — osteocytes sit in lacunae. Osteoblasts make matrix and become osteocytes; chondrocytes belong to cartilage.
**12.** (b) — cardiac muscle. Skeletal fibres are long, unbranched and multinucleate.
**13.** (c) — smooth muscle of the gut. Heart muscle (b) is involuntary but striated, the classic half-right answer.
**14.** (b) — Schwann cells in the peripheral nervous system; oligodendrocytes do the same in the central nervous system.
**15.** (a) — red cells outnumber white cells by about 600 : 1.
**16.** (b) — flat cells, tightly joined, resemble a paved floor. The word has nothing to do with a pavement outside.
:::

## 8.7 Developmental Biology

| High-yield fact | What to remember |
|---|---|
| Gametogenesis | three phases: **multiplication → growth → maturation** |
| Spermatogenesis | seminiferous tubules: spermatogonium → primary spermatocyte (2n) → 2 secondary spermatocytes (n) → 4 spermatids → **spermiogenesis** → 4 spermatozoa; Sertoli cells nourish |
| Oogenesis | in the ovary: oogonium → primary oocyte (arrested in prophase I) → secondary oocyte (arrested in metaphase II) + first polar body → ovum + second polar body **after fertilisation**; one ovum, three polar bodies |
| Frog egg | mesolecithal, telolecithal; dark animal pole, yolky vegetal pole; grey crescent |
| Frog development | fertilisation → **cleavage** (holoblastic, unequal) → morula → blastula (blastocoel) → gastrula (blastopore, archenteron) → neurula → tadpole → metamorphosis (thyroxine) |
| Germ layers | ectoderm (skin, nervous system), mesoderm (muscle, notochord, **coelom**), endoderm (gut lining) |
| Fertilisation in frog | external, in water |

```figure caption="Stages of early frog development, drawn as sections. Animal pole up. The blastocoel is pushed toward the animal pole by the yolky vegetal cells; during gastrulation cells roll in at the blastopore and the archenteron grows; in the neurula the ectoderm folds into the neural tube above the notochord."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Wedge, Rectangle
fig, axes = plt.subplots(1, 5, figsize=(4.9, 2.3))
for ax in axes:
    ax.set_xlim(-1.35, 1.35); ax.set_ylim(-1.35, 1.35); ax.set_aspect('equal'); ax.axis('off')
ttl = ['8-cell stage', 'Morula', 'Blastula', 'Gastrula', 'Neurula']
for ax, t in zip(axes, ttl): ax.text(0, -1.3, t, ha='center', va='top', fontsize=6.4, color=INK)
AN, VG = '#b9d3a0', '#f4e3a1'
ax = axes[0]
ax.add_patch(Circle((0, 0), 1.0, fc=VG, ec=INK, lw=0.9)); ax.add_patch(Wedge((0, 0), 1.0, 0, 180, fc=AN, ec=INK, lw=0.9))
ax.plot([-1, 1], [0, 0], color=INK, lw=0.9); ax.plot([0, 0], [0.0, 1.0], color=INK, lw=0.8); ax.plot([0, 0], [-1.0, 0.0], color=INK, lw=0.8)
ax = axes[1]
ax.add_patch(Circle((0, 0), 1.0, fc=VG, ec=INK, lw=0.9)); ax.add_patch(Wedge((0, 0), 1.0, 10, 170, fc=AN, ec=INK, lw=0.6))
for yy in np.arange(-0.72, 0.8, 0.29):
    for xx in np.arange(-0.78, 0.8, 0.29):
        x2 = xx + (0.145 if int(round((yy + 0.72) / 0.29)) % 2 else 0)
        if x2*x2 + yy*yy < 0.74**2:
            ax.add_patch(Circle((x2, yy), 0.125, fc='none', ec=INK, lw=0.45))
ax = axes[2]
ax.add_patch(Circle((0, 0), 1.0, fc=VG, ec=INK, lw=0.9)); ax.add_patch(Wedge((0, 0), 1.0, 10, 170, fc=AN, ec=INK, lw=0.6))
ax.add_patch(Ellipse((0, 0.33), 1.1, 0.62, fc='white', ec=INK, lw=0.8))
ax.annotate('blastocoel', (0, 0.35), (0, 1.22), fontsize=5.6, ha='center', color=INK, arrowprops=dict(arrowstyle='-', lw=0.5, color=MUTED))
ax = axes[3]
ax.add_patch(Circle((0, 0), 1.0, fc=AN, ec=INK, lw=0.9)); ax.add_patch(Wedge((0, 0), 1.0, 180, 360, fc=VG, ec=INK, lw=0.6))
ax.add_patch(Ellipse((0.0, 0.0), 1.25, 0.46, angle=38, fc='white', ec=INK, lw=0.8))
ax.add_patch(Circle((0.95, -0.35), 0.17, fc=VG, ec=INK, lw=0.6))
ax.annotate('archenteron', (-0.15, 0.0), (-1.0, 1.25), fontsize=5.6, ha='center', color=INK, arrowprops=dict(arrowstyle='-', lw=0.5, color=MUTED))
ax.annotate('yolk plug', (0.95, -0.35), (1.0, -1.05), fontsize=5.2, ha='center', color=INK, arrowprops=dict(arrowstyle='-', lw=0.5, color=MUTED))
ax = axes[4]
ax.add_patch(Ellipse((0, 0), 2.1, 1.85, fc='#f3c6a8', ec=INK, lw=0.9))
ax.add_patch(Ellipse((0, -0.08), 1.35, 0.85, fc=VG, ec=INK, lw=0.6))
ax.add_patch(Circle((0, 0.55), 0.22, fc='white', ec=INK, lw=0.8)); ax.add_patch(Circle((0, 0.22), 0.11, fc='#c79a6d', ec=INK, lw=0.6))
ax.annotate('neural tube', (0, 0.6), (0, 1.3), fontsize=5.6, ha='center', color=INK, arrowprops=dict(arrowstyle='-', lw=0.5, color=MUTED))
ax.annotate('notochord', (0.1, 0.22), (1.0, 0.95), fontsize=5.2, ha='center', color=INK, arrowprops=dict(arrowstyle='-', lw=0.5, color=MUTED))
fig.subplots_adjust(left=0.005, right=0.995, top=0.80, bottom=0.12, wspace=0.03)
```

1. What are the sequential steps involved in gametogenesis? <span class="marks">[1]</span> (NEB 2079)
   (a) multiplication, growth, maturation (b) multiplication, maturation, growth (c) growth, multiplication, maturation (d) maturation, growth, multiplication
2. In the frog, the coelom is derived from which embryonic layer? <span class="marks">[1]</span> (NEB model 2079)
   (a) ectoderm (b) mesoderm (c) endoderm (d) mesogloea
3. What happens during spermiogenesis in spermatogenesis? <span class="marks">[1]</span> (NEB 2081)
   (a) primary spermatocytes form from spermatogonia (b) secondary spermatocytes form from primary spermatocytes (c) spermatids form from secondary spermatocytes (d) spermatozoa form from spermatids
4. Which is the correct sequence of embryonic development in a frog? <span class="marks">[1]</span> (NEB 2081)
   (a) morula, blastula, gastrula (b) blastula, morula, gastrula (c) morula, gastrula, blastula (d) blastula, gastrula, morula
5. Immediately after fertilisation, a frog zygote undergoes <span class="marks">[1]</span> (NEB 2082, wording recast)
   (a) gastrulation (b) neurulation (c) cleavage (d) metamorphosis
6. One primary spermatocyte gives rise to <span class="marks">[1]</span>
   (a) one sperm (b) two sperms (c) four sperms (d) eight sperms
7. One primary oocyte finally gives rise to <span class="marks">[1]</span>
   (a) four ova (b) one ovum and three polar bodies (c) two ova and two polar bodies (d) one ovum only
8. In humans the secondary oocyte is arrested at <span class="marks">[1]</span>
   (a) prophase I (b) metaphase II (c) telophase II (d) anaphase I
9. The cleavage of a frog egg is holoblastic and unequal because <span class="marks">[1]</span>
   (a) the egg has no yolk (b) the yolk is concentrated in the vegetal half and slows division there (c) the egg is microlecithal (d) the egg is centrolecithal
10. The cavity of the blastula is called <span class="marks">[1]</span>
    (a) archenteron (b) blastocoel (c) coelom (d) gastrocoel
11. The cavity formed inside the embryo during gastrulation is the <span class="marks">[1]</span>
    (a) blastocoel (b) archenteron (c) neurocoel (d) pseudocoel
12. The nervous system of the frog develops from <span class="marks">[1]</span>
    (a) endoderm (b) mesoderm (c) ectoderm (d) notochord
13. Metamorphosis of a frog tadpole into an adult is controlled by <span class="marks">[1]</span>
    (a) insulin (b) thyroxine (c) oestrogen (d) adrenaline
14. Fertilisation in the frog is <span class="marks">[1]</span>
    (a) internal (b) external, in water (c) internal, in the oviduct (d) by budding

::: note Answers — 8.7
**1.** (a) — multiplication, growth, maturation. Option (c) puts growth first; it is tempting because in ordinary life "growth" precedes "maturity".
**2.** (b) — the coelom is a mesodermal cavity (it forms by a split in the mesoderm). Mesogloea (d) is a jelly layer of cnidarians, not a germ layer.
**3.** (d) — spermiogenesis is the conversion of a *spermatid* into a spermatozoon (no division). Options (a)–(c) are the division steps of the multiplication and maturation phases.
**4.** (a) — morula → blastula → gastrula. The blastula follows the morula because the cavity forms inside the solid ball.
**5.** (c) — cleavage is the first series of mitoses, without growth. Gastrulation comes several stages later.
**6.** (c) — meiosis I and II give four haploid spermatids, each becoming a sperm.
**7.** (b) — oogenesis is unequal: one large ovum and three small polar bodies.
**8.** (b) — the secondary oocyte stops at metaphase II and completes meiosis only after the sperm enters.
**9.** (b) — yolk slows the cleavage furrows, so vegetal cells are larger. Microlecithal (c) means little yolk.
**10.** (b) — blastocoel is the cavity of the blastula; archenteron belongs to the gastrula.
**11.** (b) — the archenteron becomes the gut. Students confuse it with the blastocoel, which it gradually replaces.
**12.** (c) — the neural plate, then the neural tube, arises from ectoderm; the notochord is mesodermal and induces it.
**13.** (b) — thyroxine from the thyroid; if the gland is removed, tadpoles remain tadpoles.
**14.** (b) — the male clasps the female (amplexus) and sperm are shed over the eggs in water.
:::

## 8.8 Human Biology

| High-yield fact | What to remember |
|---|---|
| Digestion | amylase (saliva, pH 6.8; pancreatic), **pepsin** (stomach; pepsinogen is activated by HCl from **oxyntic/parietal cells**), **rennin** (milk protein, infants), trypsin (activated by **enterokinase**), lipase, peptidases; bile emulsifies fat but is no enzyme; absorption: villus, fats via **lacteals** (chyle) |
| Breathing | diaphragm contracts → inspiration; vital capacity = TV + IRV + ERV; **respiratory centre in the medulla**; O₂ carried as oxyhaemoglobin (97 %); CO₂: ~70 % as bicarbonate (carbonic anhydrase in RBC), 20–25 % carbamino-Hb, 7 % dissolved |
| Heart | right: tricuspid; left: bicuspid (mitral); beat path **SA node → AV node → bundle of His → Purkinje fibres**; cardiac output = stroke volume × heart rate; SA node is the natural pacemaker |
| Blood groups | A, B, AB, O; O⁻ universal donor, AB⁺ universal recipient; Rh incompatibility |
| Excretion | nephron; filtration in glomerulus, reabsorption mostly in **PCT**, loop of Henle builds the gradient, **ADH** acts on DCT and collecting duct (lack → diabetes insipidus); urine path: renal pelvis → ureter → bladder → urethra |
| Nervous system | resting potential ≈ −70 mV; **cerebellum** = balance and coordination; **medulla** = respiration, heart rate; **hypothalamus** = temperature, hunger, thirst; reflex centre = spinal cord; **frontal lobe** = higher functions |
| Eye and ear | rods (dim light, rhodopsin from vitamin A), cones (colour); **blind spot** = no photoreceptors; ossicles **malleus → incus → stapes**; cochlea (hearing), semicircular canals (balance), Eustachian tube (pressure) |
| Endocrine | pituitary: GH, ADH, **oxytocin** (birth hormone); thyroid: thyroxine (goitre, myxoedema, cretinism, Graves'); parathyroid: PTH; adrenal: adrenaline, cortisol; **islets of Langerhans**: β cells insulin, α cells glucagon |
| Reproduction | testes lie in the scrotum (2–3 °C cooler); LH surge triggers ovulation (≈ day 14); corpus luteum secretes progesterone; fertilisation in the fallopian tube; amniocentesis samples amniotic fluid; IVF uses a surrogate who carries the pregnancy |

```figure caption="A nephron. 1 = filtration in the glomerulus; 2 = selective reabsorption, largest in the proximal tubule; 3 = tubular secretion and final adjustment in the distal tubule. Urine leaves by the collecting duct."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge
fig, ax = plt.subplots(figsize=(4.5, 4.0)); ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 10)
TC = '#2b6cb0'
ax.add_patch(Wedge((2.1, 8.3), 0.95, 35, 325, fc='#fde9e9', ec=TC, lw=1.4))
ax.add_patch(Circle((2.0, 8.3), 0.5, fc='#e05a5a', ec=INK, lw=0.6))
ax.plot([0.3, 1.45], [9.2, 8.7], color='#e05a5a', lw=1.6); ax.plot([0.3, 1.45], [7.4, 7.95], color='#e05a5a', lw=1.3)
t = np.linspace(0, 1, 120); x = 2.95 + 1.3*t; y = 8.0 - 0.6*t + 0.18*np.sin(t*26)
ax.plot(x, y, color=TC, lw=2.2)
ax.plot([4.25, 4.25], [7.35, 2.4], color=TC, lw=2.2)
th = np.linspace(np.pi, 2*np.pi, 40); ax.plot(4.85 + 0.6*np.cos(th), 2.4 + 0.6*np.sin(th), color=TC, lw=2.2)
ax.plot([5.45, 5.45], [2.4, 7.0], color=TC, lw=1.1)
t = np.linspace(0, 1, 100); ax.plot(5.45 + 1.15*t, 7.0 + 0.7*t + 0.15*np.sin(t*22), color=TC, lw=1.6)
ax.plot([6.6, 7.7], [7.75, 7.75], color=TC, lw=1.6)
ax.plot([7.7, 7.7], [8.4, 0.9], color=TC, lw=2.6)
ax.annotate('', xy=(7.7, 0.35), xytext=(7.7, 0.95), arrowprops=dict(arrowstyle='-|>', color=TC, lw=1.6))
ax.axhline(5.0, color=MUTED, lw=0.8, ls='--', xmin=0.02, xmax=0.98)
ax.text(0.15, 5.3, 'cortex', fontsize=7.5, color=MUTED); ax.text(0.15, 4.55, 'medulla', fontsize=7.5, color=MUTED)
for s, xy, tx, ty in [('Bowman\'s capsule\nand glomerulus', (2.5, 9.0), 0.1, 9.75), ('proximal convoluted tubule', (3.7, 7.75), 4.6, 9.8),
                      ('distal convoluted tubule', (6.3, 7.5), 6.6, 9.1), ('descending limb', (4.25, 4.6), 0.35, 3.3),
                      ('ascending limb', (5.45, 4.4), 6.0, 4.25), ('loop of Henle', (4.85, 1.8), 2.3, 1.1),
                      ('collecting duct', (7.7, 6.3), 8.25, 5.4), ('to renal pelvis', (7.7, 0.55), 8.15, 0.5)]:
    ax.annotate(s, xy=xy, xytext=(tx, ty), fontsize=6.6, color=INK, va='center', arrowprops=dict(arrowstyle='-', lw=0.6, color=MUTED, shrinkA=1, shrinkB=1))
for n, (bx, by) in [('1', (2.1, 6.85)), ('2', (3.45, 6.5)), ('3', (6.15, 6.65))]:
    ax.add_patch(Circle((bx, by), 0.27, fc=ACCENT, ec='none')); ax.text(bx, by-0.02, n, color='white', ha='center', va='center', fontsize=7.5, fontweight='bold')
```

1. Which enzyme is needed for the digestion of milk protein in human beings? <span class="marks">[1]</span> (NEB model 2079)
   (a) rennin (b) lactase (c) pepsin (d) sucrase
2. If the cerebellum of a person is injured, which physiological function is affected? <span class="marks">[1]</span> (NEB model 2079)
   (a) respiratory ability (b) body movement (c) memory function (d) smelling power
3. The vas deferens carries spermatozoa from the cauda epididymis to the ejaculatory duct. What happens if it is surgically disconnected? <span class="marks">[1]</span> (NEB model 2079)
   (a) sperms become non-motile (b) sperms lack nuclei (c) seminal fluid is without sperms (d) no spermatogenesis occurs
4. In the middle ear of a human being there are three ear ossicles. Which set is arranged in the correct sequence? <span class="marks">[1]</span> (NEB 2079)
   (a) malleus, incus, stapes (b) malleus, stapes, incus (c) cochlea, incus, malleus (d) malleus, incus, saccule
5. Pancreas is a gland with exocrine and endocrine functions; its exocrine part is the pancreatic acini. What is the endocrine part? <span class="marks">[1]</span> (NEB 2079)
   (a) zona glomerulosa (b) islets of Langerhans (c) zona reticularis (d) adenohypophysis
6. Show the correct path of origin and conduction of the heart beat in the human heart. <span class="marks">[1]</span> (NEB 2081)
   (a) AV node, SA node, bundle of His, Purkinje fibres (b) SA node, AV node, bundle of His, Purkinje fibres (c) SA node, AV node, Purkinje fibres, bundle of His (d) AV node, bundle of His, Purkinje fibres, SA node
7. Which enzymes are likely to act in order on soyabean sprouts eaten by a man as they move down the alimentary canal? <span class="marks">[1]</span> (NEB 2081)
   (a) pepsin, trypsin, peptidases (b) trypsin, peptidases, pepsin (c) pepsin, peptidases, trypsin (d) peptidases, pepsin, trypsin
8. What would happen if the frontal lobe of the cerebrum were accidentally damaged? <span class="marks">[1]</span> (NEB 2081)
   (a) loss of vision and hearing (b) impaired respiration and circulation (c) impaired water balance and hunger (d) loss of memory and learning
9. What is the primary role of a surrogate mother in the context of IVF? <span class="marks">[1]</span> (NEB 2081)
   (a) to ensure successful fertilisation (b) to provide emotional support to the biological mother (c) to carry the pregnancy to full term (d) to donate ova
10. What would happen if the oxyntic cells of the gastric glands became non-functional? <span class="marks">[1]</span> (NEB 2081)
    (a) lipase becomes more active (b) protein digestion does not take place (c) the pH of the stomach falls (d) pepsin is not secreted
11. Show the correct path for the flow of urine. <span class="marks">[1]</span> (NEB 2081)
    (a) renal pelvis, ureter, urinary bladder, urethra (b) renal pelvis, ureter, urethra, urinary bladder (c) renal pelvis, urinary bladder, urethra, ureter (d) renal pelvis, urethra, ureter, urinary bladder
12. A person has a puffy appearance, a moon face, low body temperature and intolerance to cold. What is he suffering from? <span class="marks">[1]</span> (NEB 2081)
    (a) Grave's disease (b) Conn's disease (c) myxoedema (d) Hashimoto's disease
13. What is the substance sampled during amniocentesis? <span class="marks">[1]</span> (NEB 2081)
    (a) placental cells (b) amniotic fluid (c) maternal blood (d) umbilical cord tissue
14. After digestion in the duodenum, the fat-rich milky fluid absorbed into the lacteals is called <span class="marks">[1]</span> (NEB 2082, wording recast)
    (a) bolus (b) chyme (c) lymph (d) chyle
15. The enzyme that activates trypsinogen to trypsin is <span class="marks">[1]</span>
    (a) enterokinase (b) pepsin (c) amylase (d) carboxypeptidase
16. The digestive juice that has **no** enzyme but is essential for fat digestion is <span class="marks">[1]</span>
    (a) gastric juice (b) bile (c) pancreatic juice (d) succus entericus
17. About 70 % of the carbon dioxide is carried in the blood as <span class="marks">[1]</span>
    (a) dissolved CO₂ (b) carbaminohaemoglobin (c) bicarbonate ions (d) carbonic acid in plasma
18. Vital capacity of the lungs is <span class="marks">[1]</span>
    (a) TV + IRV (b) TV + IRV + ERV (c) IRV + ERV + RV (d) TLC − TV
19. The valve between the left atrium and the left ventricle is the <span class="marks">[1]</span>
    (a) tricuspid valve (b) bicuspid (mitral) valve (c) semilunar valve (d) Eustachian valve
20. If the stroke volume is 70 mL and the heart beats 72 times per minute, the cardiac output is about <span class="marks">[1]</span>
    (a) 0.5 L min⁻¹ (b) 5.0 L min⁻¹ (c) 50 L min⁻¹ (d) 12 L min⁻¹
21. A person with blood group AB⁺ can receive blood from <span class="marks">[1]</span>
    (a) AB⁺ only (b) all ABO groups, either Rh type (c) O only (d) A and B only
22. Most of the selective reabsorption from the glomerular filtrate takes place in the <span class="marks">[1]</span>
    (a) Bowman's capsule (b) proximal convoluted tubule (c) distal convoluted tubule (d) collecting duct
23. If ADH is secreted insufficiently, the person passes <span class="marks">[1]</span>
    (a) a small volume of concentrated urine (b) a large volume of dilute urine (c) urine with glucose (d) no urine
24. The part of the brain that controls body temperature, hunger and thirst is the <span class="marks">[1]</span>
    (a) cerebellum (b) medulla oblongata (c) hypothalamus (d) thalamus
25. The blind spot of the eye is the region where <span class="marks">[1]</span>
    (a) the optic nerve leaves and there are no photoreceptors (b) only cones are present (c) only rods are present (d) the lens is attached
26. Organ of Corti, the receptor of hearing, is located in the <span class="marks">[1]</span>
    (a) semicircular canals (b) utriculus (c) cochlea (d) Eustachian tube
27. The hormone that is called the birth hormone because it causes uterine contractions is <span class="marks">[1]</span>
    (a) oxytocin (b) prolactin (c) relaxin only (d) vasopressin
28. Insulin is secreted by the ______ of the islets of Langerhans. <span class="marks">[1]</span>
    (a) α cells (b) β cells (c) δ cells (d) acinar cells
29. The release of a secondary oocyte from the Graafian follicle is triggered by a surge of <span class="marks">[1]</span>
    (a) FSH (b) LH (c) progesterone (d) oestrogen only
30. The testes lie outside the abdominal cavity in the scrotum because <span class="marks">[1]</span>
    (a) they are too large (b) spermatogenesis needs a temperature 2–3 °C lower than the body's core temperature (c) they need more oxygen (d) they secrete less testosterone inside
31. The hormone that maintains the endometrium during pregnancy and is secreted by the corpus luteum is <span class="marks">[1]</span>
    (a) oestrogen (b) progesterone (c) FSH (d) testosterone
32. Excess growth hormone in childhood causes <span class="marks">[1]</span>
    (a) acromegaly (b) gigantism (c) dwarfism (d) cretinism

::: note Answers — 8.8
**1.** (a) — rennin curdles casein in infants; lactase (b) digests the milk *sugar*, which is the trap. Pepsin also acts on protein but the classic milk-protein answer is rennin.
**2.** (b) — the cerebellum coordinates movement and balance. Respiration belongs to the medulla, memory to the cerebrum, smell to the olfactory bulb.
**3.** (c) — sperms are still made and still stored, so the semen carries none; the fluid from the seminal vesicles and prostate still comes. Option (d) is wrong because spermatogenesis goes on in the testis.
**4.** (a) — malleus, incus, stapes from the tympanum inward. The cochlea and saccule are not ossicles.
**5.** (b) — the islets of Langerhans make insulin and glucagon. Zona glomerulosa and zona reticularis are adrenal cortex layers, adenohypophysis is the anterior pituitary.
**6.** (b) — SA node (pacemaker) → AV node → bundle of His → Purkinje fibres.
**7.** (a) — pepsin (stomach) → trypsin (duodenum) → peptidases (intestinal brush border). Reversing the stomach and the intestine gives (b)–(d).
**8.** (d) — the frontal lobe handles thinking, planning and memory. Option (a) is the occipital and temporal lobes; (b) the medulla; (c) the hypothalamus.
**9.** (c) — a gestational surrogate carries the embryo to term. Donating ova is the role of an egg donor, and fertilisation happens in the laboratory.
**10.** (b) — oxyntic (parietal) cells make the HCl; without it pepsinogen is not converted to active pepsin and the acidity needed for protein digestion in the stomach is lost. Option (d) is the nearest distractor: the *chief* cells still release pepsinogen, so the real failure is activation, not secretion. The pH would rise, not fall (c), and lipase (a) works in the intestine.
**11.** (a) — pelvis → ureter → bladder → urethra. The bladder lies between the ureter and the urethra.
**12.** (c) — myxoedema is adult hypothyroidism: puffy face, cold intolerance, low metabolic rate. Graves' is hyperthyroidism. Hashimoto's is an autoimmune cause of hypothyroidism, but the puffy-face description is the textbook picture of myxoedema.
**13.** (b) — a needle takes amniotic fluid to test for chromosome and gene disorders. Placental cells are sampled in chorionic villus sampling.
**14.** (d) — chyle. Chyme is the acidic food mass leaving the stomach, bolus is the swallowed mass.
**15.** (a) — enterokinase of the intestinal mucosa. Pepsin acts in the stomach.
**16.** (b) — bile salts emulsify fat; bile has no digestive enzyme.
**17.** (c) — as HCO₃⁻, formed by carbonic anhydrase in the RBC. About 20–25 % is carbamino-haemoglobin.
**18.** (b) — TV + IRV + ERV. Option (c) contains the residual volume, which cannot be exhaled.
**19.** (b) — the left valve is bicuspid (mitral). Tricuspid is on the right.
**20.** (b) — 70 mL × 72 = 5040 mL ≈ 5 L min⁻¹.
**21.** (b) — AB⁺ is the universal recipient because it has no anti-A, anti-B or anti-D antibodies.
**22.** (b) — about two thirds of the filtrate is reabsorbed in the PCT.
**23.** (b) — too little ADH means too little water reabsorbed: diabetes insipidus. The word "diabetes" tempts students into choosing glucose in urine (c), but that is diabetes *mellitus*.
**24.** (c) — the hypothalamus is the thermostat and the centre of hunger and thirst.
**25.** (a) — the optic disc has no rods or cones. Option (b) describes the fovea centralis.
**26.** (c) — the organ of Corti sits on the basilar membrane of the cochlea. The semicircular canals sense rotation.
**27.** (a) — oxytocin. Vasopressin (ADH) is the other posterior pituitary hormone.
**28.** (b) — β cells make insulin; α cells make glucagon.
**29.** (b) — an LH surge ruptures the follicle. FSH grows the follicle.
**30.** (b) — sperm production needs about 2–3 °C below core temperature.
**31.** (b) — progesterone from the corpus luteum (later the placenta). Oestrogen builds the endometrium in the first half of the cycle.
**32.** (b) — excess GH in childhood gives gigantism; in an adult it gives acromegaly (a). Dwarfism is deficiency.
:::

## 8.9 Human Population and Health Disorders

| High-yield fact | What to remember |
|---|---|
| Population change | growth = (births − deaths) + (immigration − emigration); **immigration** = individuals entering, **emigration** = leaving |
| Demography | sex ratio = males per 100 females; dependency ratio = (under 15 + over 64) per 100 of working age; a pyramid with a broad base is an **expanding** population (Nepal's shape is moving from this towards a narrower base) |
| Checking growth | **family planning**, raising the age of marriage, education of girls, contraceptive choice; food supply does not control population |
| Transplants | **autograft** (same individual), **isograft** (genetically identical individuals, twins), **allograft** (same species), **xenograft** (different species); cornea is **avascular** and immune-privileged, so it is rarely rejected |
| Immunity | innate and acquired; active (own antibodies) vs passive (readymade, mother's milk, antiserum); vaccines give artificial active immunity |
| AIDS | HIV (an RNA retrovirus) kills **CD4 helper T cells**; spread by blood, sexual contact, mother to child |
| Malaria | *Plasmodium*; vector is the female *Anopheles*; dengue by *Aedes* |
| Substance abuse | nicotine (tobacco), alcohol (liver cirrhosis), opioids; peer pressure is a major cause in adolescents; prevention by awareness, refusal skills, rehabilitation |
| Deficiency diseases | kwashiorkor (protein), marasmus (protein + energy), goitre (iodine), night blindness (vitamin A) |

```figure caption="Two patterns of population growth. J-shaped growth is exponential and stops abruptly; S-shaped (logistic) growth levels off at the carrying capacity K set by food, space and disease."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4, 2.7))
t = np.linspace(0, 10, 200)
ax.plot(t, 0.3*np.exp(0.5*t), color='#c0392b', lw=2.0)
K = 60; ax.plot(t, K/(1 + 19*np.exp(-0.8*t)), color=ACCENT, lw=2.0)
ax.axhline(K, color=MUTED, lw=0.9, ls='--')
ax.set_xlim(0, 10); ax.set_ylim(0, 75)
ax.text(0.2, K + 2.2, 'carrying capacity (K)', fontsize=7, color=MUTED)
ax.text(5.7, 30, 'S-shaped (logistic)', fontsize=7.5, color=ACCENT, fontweight='bold'); ax.text(6.0, 14, 'J-shaped (exponential)', fontsize=7.5, color='#c0392b', fontweight='bold')
ax.set_xlabel('time'); ax.set_ylabel('population size'); ax.set_xticks([]); ax.set_yticks([])
ax.spines[['top', 'right']].set_visible(False)
```

1. When an organ transplantation occurs between two genetically identical individuals, what is the type of transplantation? <span class="marks">[1]</span> (NEB 2079)
   (a) autograft (b) allograft (c) heterograft (d) isograft
2. Overpopulation has adverse consequences in society. Which of the following can control it? <span class="marks">[1]</span> (NEB 2079)
   (a) early marriage (b) polygamy (c) family planning (d) food supply
3. Which organ transplant has the lowest risk of rejection because the tissue lacks blood vessels? <span class="marks">[1]</span> (NEB 2082, wording recast)
   (a) cornea (b) kidney (c) heart (d) liver
4. The movement of individuals into a population from outside, which increases its size, is <span class="marks">[1]</span> (NEB 2082, wording recast)
   (a) emigration (b) immigration (c) dispersion (d) natality
5. A population has 1000 individuals. In a year there are 40 births, 10 deaths, 5 immigrants and 15 emigrants. The net increase is <span class="marks">[1]</span>
   (a) 20 (b) 30 (c) 50 (d) 60
6. A population pyramid with a broad base and a narrow top represents <span class="marks">[1]</span>
   (a) a declining population (b) an expanding population (c) a stable population (d) a zero-growth population
7. The skin graft transferred from one part of the body of a burn patient to another part is an <span class="marks">[1]</span>
   (a) allograft (b) xenograft (c) autograft (d) isograft
8. HIV mainly destroys <span class="marks">[1]</span>
   (a) B lymphocytes (b) CD4 helper T cells (c) red blood cells (d) platelets
9. The vector of the malaria parasite is <span class="marks">[1]</span>
   (a) female *Anopheles* (b) male *Anopheles* (c) *Culex* (d) *Aedes aegypti*
10. The antibodies received by a baby through breast milk give <span class="marks">[1]</span>
    (a) natural active immunity (b) natural passive immunity (c) artificial active immunity (d) artificial passive immunity
11. Kwashiorkor is caused by the deficiency of <span class="marks">[1]</span>
    (a) protein (b) iodine (c) vitamin A (d) vitamin C
12. Which is the most common reason for adolescents to start smoking? <span class="marks">[1]</span>
    (a) hunger (b) peer pressure (c) poverty alone (d) doctor's advice

::: note Answers — 8.9
**1.** (d) — genetically identical individuals (identical twins) give an isograft. Autograft (a) is from the same individual, allograft (b) from the same species, heterograft (c) from another species.
**2.** (c) — family planning controls birth. Early marriage and polygamy raise births; food supply supports growth.
**3.** (a) — the cornea has no blood vessels and sits behind the immune system's surveillance; rejection is rare.
**4.** (b) — immigration increases and emigration decreases the population; natality is births only.
**5.** (a) — births − deaths = 30; immigration − emigration = −10; net = 30 + (−10) = 20. Option (b) forgets the net migration.
**6.** (b) — a broad base means many young people: an expanding population. A narrow base would be declining.
**7.** (c) — same individual, so an autograft; no immune rejection.
**8.** (b) — HIV binds CD4 on helper T cells; as they fall, infections take over.
**9.** (a) — the female *Anopheles* bites at night; the male feeds on plant juices. *Aedes* carries dengue.
**10.** (b) — antibodies come ready-made from the mother (natural) and the baby made none (passive).
**11.** (a) — protein deficiency with adequate energy gives oedema and a swollen belly; marasmus is protein and energy lack.
**12.** (b) — peer pressure; the question type also appears as a planning task (see the subjective chapter).
:::

## 8.10 Applied Biology

| High-yield fact | What to remember |
|---|---|
| Apiculture | *Apis cerana* (indigenous hive bee), *A. mellifera* (European), *A. dorsata* (rock bee), *A. florea*; caste: queen, workers (♀, 2n), drones (♂, haploid, from unfertilised eggs); royal jelly makes a queen |
| Sericulture | *Bombyx mori* feeds on mulberry; the larva spins a cocoon of **fibroin** held by **sericin**; the pupa is killed to reel unbroken silk |
| Pisciculture | indigenous fish of Nepal: **Asala** (snow trout), Sahar (mahseer), Katle; **composite culture**: catla (surface), rohu (column), mrigal (bottom) + common/grass/silver carp; **integrated fish farming** adds livestock or crops |
| Poultry | **layers** (eggs), **broilers** (meat), **pullet** (young hen not yet laying); Ranikhet (Newcastle) disease is viral |
| Dairy and others | Jersey, Holstein-Friesian, Murrah buffalo; vermicompost by *Eisenia fetida*; pearl made of **nacre** by oysters; lac from *Kerria lacca* |
| Bacterial diseases | typhoid (*Salmonella typhi*, Widal test, enteric fever), cholera (*Vibrio cholerae*, ORS), tuberculosis (*Mycobacterium tuberculosis*, BCG, DOTS) |
| Viral, protozoal | hepatitis A (faeco-oral), influenza, AIDS; malaria, amoebiasis; candidiasis is **fungal** |
| Microbiology at work | penicillin (*Penicillium*, Fleming 1928); vaccine (Jenner, smallpox); *Lactobacillus* makes curd; sewage treatment; biogas by methanogens |

1. Which one of the following sets contains bacterial diseases only? <span class="marks">[1]</span> (NEB model 2079)
   (a) hepatitis, influenza, cholera (b) cholera, typhoid, candidiasis (c) tuberculosis, typhoid, cholera (d) tuberculosis, cholera, candidiasis
2. Which pair of diseases is spread through contaminated food and water? <span class="marks">[1]</span> (NEB 2082, wording recast)
   (a) typhoid and cholera (b) tuberculosis and typhoid (c) cholera and candidiasis (d) typhoid and influenza
3. The indigenous honeybee of Nepal, kept in log and box hives, is <span class="marks">[1]</span>
   (a) *Apis mellifera* (b) *Apis cerana* (c) *Apis dorsata* (d) *Apis florea*
4. In a honeybee colony, drones develop from <span class="marks">[1]</span>
   (a) fertilised eggs (b) unfertilised eggs (c) larvae fed royal jelly (d) workers' eggs
5. A larva becomes a queen bee because it is fed throughout on <span class="marks">[1]</span>
   (a) bee bread (b) royal jelly (c) honey only (d) pollen only
6. The silkworm *Bombyx mori* is fed on the leaves of <span class="marks">[1]</span>
   (a) castor (b) mulberry (c) oak (d) peepal
7. The two proteins of the raw silk thread are <span class="marks">[1]</span>
   (a) keratin and collagen (b) fibroin and sericin (c) casein and albumin (d) myosin and actin
8. Silk is spun by the ______ of the silk moth. <span class="marks">[1]</span>
   (a) adult (b) larva (c) egg (d) pupa
9. Which of the following is an indigenous fish of Nepal? <span class="marks">[1]</span>
   (a) silver carp (b) grass carp (c) Asala (snow trout) (d) common carp
10. In composite fish culture catla, rohu and mrigal are stocked together because they <span class="marks">[1]</span>
    (a) eat each other (b) feed at different depths of the pond (c) breed at the same time (d) need different temperatures
11. A pullet is <span class="marks">[1]</span>
    (a) a male chick (b) a young female hen that has not started laying (c) an egg-laying hen (d) a hen reared for meat
12. Ranikhet disease of poultry is caused by a <span class="marks">[1]</span>
    (a) bacterium (b) virus (c) fungus (d) protozoan
13. The earthworm commonly used for vermicomposting is <span class="marks">[1]</span>
    (a) *Pheretima posthuma* (b) *Eisenia fetida* (c) *Lumbricus terrestris* only (d) *Hirudinaria*
14. Pearl is made up of <span class="marks">[1]</span>
    (a) calcium carbonate laid as nacre around an irritant in an oyster (b) silica (c) chitin (d) keratin
15. Lac is obtained from <span class="marks">[1]</span>
    (a) *Kerria lacca* (b) *Bombyx mori* (c) *Apis cerana* (d) *Laccifer* plants
16. The causative organism of typhoid is <span class="marks">[1]</span>
    (a) *Vibrio cholerae* (b) *Salmonella typhi* (c) *Mycobacterium tuberculosis* (d) *Plasmodium vivax*
17. The test used for the diagnosis of typhoid is <span class="marks">[1]</span>
    (a) Widal test (b) ELISA (c) Mantoux test (d) Schick test
18. The first line of treatment of dehydration in cholera is <span class="marks">[1]</span>
    (a) antibiotics only (b) oral rehydration solution (c) vaccination (d) blood transfusion
19. The vaccine given in infancy against tuberculosis is <span class="marks">[1]</span>
    (a) DPT (b) BCG (c) OPV (d) MMR
20. Hepatitis A virus spreads mainly through <span class="marks">[1]</span>
    (a) contaminated food and water (b) blood transfusion only (c) mosquito bite (d) droplets
21. The malaria parasite *Plasmodium* is a <span class="marks">[1]</span>
    (a) bacterium (b) virus (c) protozoan (d) fungus
22. Penicillin was discovered by Alexander Fleming from the mould <span class="marks">[1]</span>
    (a) *Aspergillus* (b) *Penicillium notatum* (c) *Rhizopus* (d) *Streptomyces*
23. The first vaccine in history was prepared against <span class="marks">[1]</span>
    (a) polio (b) smallpox (c) rabies (d) tetanus
24. Curd is formed from milk by the action of <span class="marks">[1]</span>
    (a) *Lactobacillus* (b) *Saccharomyces* (c) *Rhizobium* (d) *Penicillium*

::: note Answers — 8.10
**1.** (c) — tuberculosis, typhoid and cholera are all bacterial. Candidiasis is a fungal disease and hepatitis and influenza are viral, so every other option hides one wrong member.
**2.** (a) — typhoid and cholera spread by the faeco-oral route. Tuberculosis and influenza are airborne; candidiasis is fungal.
**3.** (b) — *Apis cerana* is the hive bee of Nepal's hills. *A. mellifera* is the introduced European bee.
**4.** (b) — drones are haploid, from unfertilised eggs (parthenogenesis); queen and workers are diploid.
**5.** (b) — royal jelly for the whole larval life makes a queen; workers get it only for the first days.
**6.** (b) — mulberry (*Morus*). Castor feeds the eri silkworm.
**7.** (b) — fibroin forms the thread and sericin glues it.
**8.** (b) — the larva (caterpillar) spins the cocoon before it pupates.
**9.** (c) — Asala is indigenous; silver, grass and common carp are exotic fishes introduced for culture.
**10.** (b) — catla is a surface feeder, rohu a column feeder, mrigal a bottom feeder, so they use the whole pond without competing.
**11.** (b) — a pullet is a young female fowl before egg laying; the word is not "egg-laying hen" (c).
**12.** (b) — Newcastle disease virus.
**13.** (b) — *Eisenia fetida* (red wiggler) is an epigeic composting worm. *Pheretima* is a burrower.
**14.** (a) — nacre (aragonite and conchiolin) around an irritant in the mantle.
**15.** (a) — the lac insect *Kerria lacca* secretes lac on twigs.
**16.** (b) — *Salmonella typhi*. *Vibrio cholerae* causes cholera.
**17.** (a) — Widal detects antibodies to *S. typhi* antigens; Mantoux is for TB.
**18.** (b) — ORS replaces water and salts; antibiotics are secondary.
**19.** (b) — BCG; DPT is for diphtheria, pertussis, tetanus.
**20.** (a) — faeco-oral; hepatitis B spreads through blood.
**21.** (c) — *Plasmodium* is a sporozoan protozoan.
**22.** (b) — *Penicillium notatum*, discovered in 1928.
**23.** (b) — Edward Jenner used cowpox against smallpox (1796).
**24.** (a) — *Lactobacillus* converts lactose to lactic acid; *Saccharomyces* is baker's yeast.
:::

## Chapter summary

- Group A is 5 Botany + 6 Zoology one-mark MCQs; every distractor is a real misconception, so learn the **contrast** (parthenogenesis vs parthenocarpy, isograft vs allograft, myxoedema vs Graves', immigration vs emigration).
- **Botany:** bundles are open collateral in a dicot stem and closed scattered in a monocot; endodermis regulates entry into the stele; DPD = OP − TP and water moves to the larger DPD; O₂ comes from water; net glycolysis is 2 ATP; auxin, GA, cytokinin, ABA, ethylene each have one signature effect.
- **Genetics:** Rr × Rr gives 1 : 2 : 1 genotypes; AaBb × AaBb gives 1/16 double recessive; frame shift by one-base indel; X-linked recessive traits skip from maternal grandfather to grandson; monosomy is 2n − 1; sickle-cell anaemia is a point mutation.
- **Embryology and biotechnology:** porogamy = micropyle; synergids and antipodals degenerate; triple fusion gives 3n endosperm; embryo culture saves aborting embryos; meristem culture gives virus-free plants.
- **Zoology:** cartilage has no blood supply; neutrophils and monocytes are phagocytic; spermiogenesis turns a spermatid into a sperm; morula → blastula → gastrula; heart beat SA → AV → His → Purkinje; urine path pelvis → ureter → bladder → urethra.
- **Health and applied biology:** typhoid, cholera and TB are bacterial; candidiasis is fungal; *Apis cerana*, *Bombyx mori*, Asala, *Eisenia fetida* are the names that recur.
