---
subject: Question Bank
grade: 12
unit: 10
title: "Biology: Model Question Sets and Predicted Questions"
hours: 0
area: Biology
---

This chapter does three things. First it **reads the paper**: how the 75 marks are built and which unit carried how many marks in the board papers that could be obtained. Second, it gives **two complete model papers** set exactly to the board's grid — Botany 37 marks, Zoology 38 marks — each with a full solution in the wording and depth of a full-mark answer. Third, it lists **over forty ranked predicted questions**, each with the reason for the ranking and a short model answer. Sit each paper in three hours without opening the solutions; mark yourself strictly by the brackets.

::: key The grid in one line
**Section I Botany 37 = MCQ 5×1 + short 4×4 + long 2×8. Section II Zoology 38 = MCQ 6×1 + short 4×4 + long 2×8.** Total 75. The paper has four "OR" choices: one Botany short (Q7 or Q8), Botany Q11, Zoology Q19 (once Q18) and Zoology Q23. Botany and Zoology are answered in separate sections of the same answer sheet, Botany first. The MCQs (Q1–5 and Q12–17) are handed out 30 minutes after the start.
:::

::: caution What the data are, and what they are not
The pattern analysis below rests on **four full papers**: the 2079 board paper (set N), the official 2079 model question, the 2081 board paper (set W) and the 2082 board paper (set M), plus the MCQs of 2080 (Botany) and 2081 (set V). The 2080 paper could not be obtained in full. Four papers are a small sample: they show the board's *habits*; they do not guarantee the next paper. Every predicted question says why it is on the list, and none is a leak. The curriculum publishes no mark grid by unit, so the unit weights below are **measured from those papers** and compared with the teaching hours in the syllabus.
:::

## 10.1 Reading the paper: marks, minutes and order of attack

| Part | Questions | Marks | Minutes at 2.4 per mark |
|---|---|---|---|
| Section I Botany, Group A | Q1–5, MCQ | 5 | 6 |
| Section I Botany, Group B | Q6–9, four shorts | 16 | 38 |
| Section I Botany, Group C | Q10–11, two longs | 16 | 38 |
| Section II Zoology, Group A | Q12–17, MCQ | 6 | 7 |
| Section II Zoology, Group B | Q18–21, four shorts | 16 | 38 |
| Section II Zoology, Group C | Q22–23, two longs | 16 | 38 |
| Reading, choosing the ORs, checking | | | 15 |

1. **Choose the ORs in the first ten minutes.** Four OR choices means you always have a question you know better. Write the choice on the question paper.
2. **Draw first.** Every long question that says "with diagram" has a separate 2–3 marks for the diagram. Draw it at half a page, label with straight lines, and write the heading.
3. **Write to the brackets.** [1+3] means 1 mark for the definition and 3 for the explanation; give the definition its own first line.
4. **Do not leave MCQs blank.** There is no negative marking; rewrite the correct option (the letter and the words).
5. **Keep the 15-minute reserve** for the diagram labels and for any question you marked with a cross.

## 10.2 Pattern analysis

### 10.2.1 Marks by unit in each paper

The table gives the marks each syllabus unit carried in the four papers (MCQ + short + long; for a question with an OR the first alternative was counted). Botany adds to 37 and Zoology to 38 in every paper.

| Unit | 2079 | model 2079 | 2081 | 2082 | Mean | Expected next |
|---|---|---|---|---|---|---|
| 1 Plant Anatomy | 5 | 5 | 5 | 5 | 5.0 | 5 |
| 2 Plant Physiology | 13 | 10 | 10 | 10 | 10.8 | 10–11 |
| 3 Genetics | 9 | 13 | 13 | 13 | 12.0 | 12–13 |
| 4 Embryology | 5 | 1 (+4 unassigned) | 5 | 5 | 4.0 | 4–5 |
| 5 Biotechnology | 5 | 4 | 4 | 4 | 4.3 | 4 |
| **Botany total** | 37 | 37 | 37 | 37 | | 37 |
| 6 Animal Tissues | 5 | 5 | 5 | 5 | 5.0 | 5 |
| 7 Developmental Biology | 5 | 5 | 5 | 5 | 5.0 | 5 |
| 8 Human Biology | 18 | 15 | 16 | 17 | 16.5 | 16–17 |
| 9 Population and Health Disorders | 2 | 4 | 4 | 2 | 3.0 | 2–4 |
| 10 Applied Biology | 8 | 9 | 8 | 9 | 8.5 | 8–9 |
| **Zoology total** | 38 | 38 | 38 | 38 | | 38 |

In the model paper Botany Q7 was a figure question whose diagram could not be seen; its 4 marks are shown as unassigned. **Two things stand out.** First, the allocation is remarkably steady: units 1, 6 and 7 carried exactly 5 marks in every paper. Second, **Human Biology alone carries about 16–17 of the 38 Zoology marks (about 44 %)**, which is almost exactly its share of the Zoology teaching hours (28 of 64 hours), and Genetics plus Plant Physiology carry about 23 of the 37 Botany marks (62 %) against 41 of 64 hours.

```figure caption="Marks carried by each unit in the four papers read (dots: 2079, model 2079, 2081, 2082) and the mean (bar; blue = Botany, green = Zoology). Units 1, 6 and 7 never moved; Genetics, Physiology, Human Biology and Applied Biology carry the paper."
import numpy as np, matplotlib.pyplot as plt
units = ['1 Anatomy', '2 Physiology', '3 Genetics', '4 Embryology', '5 Biotech.', '6 Tissues', '7 Dev. Biol.', '8 Human Biol.', '9 Health', '10 Applied']
data = [[5,5,5,5],[13,10,10,10],[9,13,13,13],[5,1,5,5],[5,4,4,4],[5,5,5,5],[5,5,5,5],[18,15,16,17],[2,4,4,2],[8,9,8,9]]
fig, ax = plt.subplots(figsize=(4.7, 3.3))
y = np.arange(len(units))[::-1]
m = [np.mean(d) for d in data]
bot = ['#9ec1d9']*5 + ['#c9d8a8']*5
ax.barh(y, m, color=bot, edgecolor='none', height=0.62)
for yi, d in zip(y, data):
    ax.scatter(d, [yi]*4, s=11, color=INK, zorder=3)
for yi, mm in zip(y, m):
    ax.text(19.6, yi, '%.1f' % (mm + 1e-9), va='center', ha='right', fontsize=6.6, color=INK)
ax.set_yticks(y); ax.set_yticklabels(units, fontsize=6.8)
ax.set_xlim(0, 20); ax.set_xlabel('marks carried', fontsize=7.2); ax.tick_params(axis='x', labelsize=6.8)
ax.spines[['top', 'right']].set_visible(False); ax.grid(axis='x', color=GRID, lw=0.5)
```

### 10.2.2 The long questions: the board's rotation

| Paper | Botany Q10 | Botany Q11 (OR) | Zoology Q22 | Zoology Q23 (OR) |
|---|---|---|---|---|
| 2079 | Mutation (OR *Drosophila*) — Genetics | Hill reaction — Physiology | Cholera — Applied | Alimentary canal (OR SA node, blood group) — Human Biology |
| model 2079 | EMP pathway — Physiology | Replication (OR crossing over) — Genetics | Typhoid — Applied | Digestion (OR CO₂ transport) — Human Biology |
| 2081 | Dark reaction — Physiology | DNA structure (OR chromosomal mutation) — Genetics | Typhoid — Applied | Male reproductive system (OR eye) — Human Biology |
| 2082 | Photophosphorylation — Physiology | Colour blindness (OR replication) — Genetics | Tuberculosis — Applied | Female reproductive system (OR nephron) — Human Biology |

The rotation is almost mechanical. **Botany has one Physiology long and one Genetics long in every paper** (4 of 4). **Zoology Q22 is a bacterial disease every time** (4 of 4: cholera, typhoid, typhoid, tuberculosis) and **Q23 is a labelled organ system every time** (4 of 4). No long question has yet come from Plant Anatomy, Embryology, Biotechnology, Animal Tissues, Developmental Biology or Population and Health. The four units that carry the long questions are therefore **Plant Physiology, Genetics, Human Biology and Applied Biology**, and inside them the topics *not yet set as a long question* are the best guess for the next paper.

### 10.2.3 Topics that repeat

| Topic | Times seen | Where |
|---|---|---|
| DNA replication | 2 (model 2079, 2082 OR) | long |
| Crossing over and linkage | 2 (model 2079 OR, 2082 short) | long OR, short |
| Typhoid | 2 | long, Q22 |
| Porogamy (micropyle) | 2 (2080, 2082) | MCQ |
| Plant tissues: meristem, permanent tissue, vascular bundle | 5 (Q6 in all four papers + the model MCQ) | short and MCQ |
| Parthenogenesis vs parthenocarpy | 2 (model 2079, 2081) | MCQ |
| Point mutation, frame shift, monosomy, sickle-cell | 4 (model 2079, 2081, 2082, 2079 long) | MCQ and long |
| Sex-linked inheritance (*Drosophila*, colour blindness) | 3 (2079 OR, 2080 MCQ, 2082 long) | MCQ and long |
| Osmosis / turgor / plasmolysis | 5 (MCQs 2079, 2080, 2081 W, 2081 V; short OR 2082) | MCQ and short |
| Transplants and immunity | 3 (2079, model 2079 OR, 2082) | MCQ and short |
| Smoking, drugs, kidney disorders | every paper has one Q21 | short |
| Areolar / adipose / cartilage | 3 (2079, model 2079 ×2) | MCQ and short |

### 10.2.4 Question types and what the marker wants

- **MCQ** (11 marks): Botany MCQs rotate over Anatomy, Physiology, Genetics, Embryology and Biotechnology, one each; Zoology MCQs cover Tissues, Development, Human Biology (two or three), Health and Applied Biology. Since 2081 the stems are short *application* stories.
- **Figure questions** (Q7, Q19, Q20, Q23): "study the given figure", label A–D, give a function. Practise the eye, ear, pituitary, nephron, embryo sac, pollen grain and grafting until you can name four parts without thinking.
- **Opinion questions** (Q9, Q21): "justify", "plan", "in your view". Give two concrete points and one reason each.

## 10.3 Model question paper I

::: note Model Question Paper I — Biology (Sub. Code 2021)
**NEB-XII Model Set I.** Time: 3 hrs. Full marks: 75. Candidates are required to give their answers in their own words as far as practicable. The figures in the margin indicate full marks. Attempt all the questions. Complete Section I (Botany) first and then Section II (Zoology); answer each section separately in the same answer sheet.
:::

**Section I: Botany**

**Group A — Rewrite the correct option of each question. 5 × 1 = 5**

1. Which one of the following is a function of the endodermis of the root? <span class="marks">[1]</span>
   (a) photosynthesis (b) regulating the movement of water and minerals into the stele (c) secondary growth of the root (d) conduction of food
2. In a C4 plant, which enzyme first fixes atmospheric CO₂ in the mesophyll cells? <span class="marks">[1]</span>
   (a) RuBisCO (b) PEP carboxylase (c) ATP synthase (d) pyruvate kinase
3. The F₂ phenotypic ratio of a dihybrid cross with complete dominance is <span class="marks">[1]</span>
   (a) 3 : 1 (b) 1 : 2 : 1 (c) 9 : 3 : 3 : 1 (d) 1 : 1 : 1 : 1
4. A pollen grain with a thick exine of sporopollenin is produced in the <span class="marks">[1]</span>
   (a) ovule (b) anther (c) stigma (d) style
5. Virus-free plantlets can be obtained by culturing <span class="marks">[1]</span>
   (a) leaf segments (b) root tips only (c) shoot-apex meristem (d) mature pollen

**Group B — Short answer questions. 4 × 4 = 16**

6. Differentiate between xylem and phloem on the basis of cell types, living or dead condition, material conducted and direction of conduction. <span class="marks">[4]</span>
7. Study the given figure of a vascular bundle and answer the questions. <span class="marks">[1+2+1]</span>
   (i) Identify the type of vascular bundle in the figure. (ii) Name the parts A to D. (iii) State the function of part B.
8. State Mendel's law of segregation and explain it with a monohybrid cross up to F₂. <span class="marks">[1+3]</span>
   **OR** Describe four physiological effects of auxin in plants. <span class="marks">[4]</span>
9. Explain how Bt cotton is produced and discuss two benefits and two concerns of its use. <span class="marks">[2+2]</span>

```figure caption="Question diagram for Paper I, Question 7: transverse section of a vascular bundle. Letters only, no names — as on the real paper."
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle, Rectangle, FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.2, 3.4)); ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 8.4)
ax.add_patch(FancyBboxPatch((1.4, 0.8), 4.8, 6.9, boxstyle='round,pad=0.05,rounding_size=1.5', fc='#fbf4e4', ec=INK, lw=1.1))
ax.add_patch(Ellipse((3.8, 6.85), 3.7, 1.0, fc='#c9a45a', ec=INK, lw=0.7))
for i, x in enumerate([2.5, 3.1, 3.7, 4.3, 4.9]):
    ax.add_patch(Circle((x, 5.65 + (0.15 if i % 2 else 0)), 0.3, fc='#f3d98a', ec=INK, lw=0.6))
for x in [2.75, 3.4, 4.05, 4.7]:
    ax.add_patch(Circle((x, 5.0), 0.17, fc='#f7e8b0', ec=INK, lw=0.5))
ax.add_patch(Rectangle((1.9, 4.05), 3.8, 0.45, fc='#9ec1a0', ec=INK, lw=0.7))
for x in [2.3, 2.75, 3.2, 3.65, 4.1, 4.55, 5.0, 5.4]:
    ax.plot([x, x], [4.05, 4.5], color=INK, lw=0.5)
for x, y in [(2.7, 3.15), (4.8, 3.15)]:
    ax.add_patch(Circle((x, y), 0.55, fc='#3b5a8c', ec=INK, lw=0.7)); ax.add_patch(Circle((x, y), 0.3, fc='white', ec=INK, lw=0.4))
ax.add_patch(Circle((3.75, 2.4), 0.45, fc='#3b5a8c', ec=INK, lw=0.7)); ax.add_patch(Circle((3.75, 2.4), 0.25, fc='white', ec=INK, lw=0.4))
for x, y in [(3.1, 1.55), (3.75, 1.45), (4.4, 1.55)]:
    ax.add_patch(Circle((x, y), 0.2, fc='#3b5a8c', ec=INK, lw=0.6)); ax.add_patch(Circle((x, y), 0.09, fc='white', ec='none'))
for L, (x, y), (tx, ty) in [('A', (4.9, 5.85), (8.0, 6.3)), ('B', (5.4, 4.3), (8.0, 4.3)), ('C', (5.2, 3.3), (8.0, 3.1)), ('D', (4.4, 1.55), (8.0, 1.5))]:
    ax.annotate('', xy=(x, y), xytext=(tx-0.25, ty), arrowprops=dict(arrowstyle='-', color=INK, lw=0.8))
    ax.text(tx, ty, L, ha='left', va='center', fontsize=11, fontweight='bold', color=INK)
ax.text(3.8, 0.2, 'towards the pith', ha='center', fontsize=6.6, color=MUTED)
```

**Group C — Long answer questions. 2 × 8 = 16**

10. Describe the Krebs cycle. How many NADH, FADH₂ and ATP molecules are formed from one molecule of glucose in the link reaction and the Krebs cycle? <span class="marks">[1+5+2]</span>
11. State and explain Mendel's law of independent assortment with the help of a dihybrid cross. Show the F₂ phenotypic and genotypic ratios. <span class="marks">[1+5+2]</span>
    **OR** "Genes are expressed as proteins." Explain the processes of transcription and translation with necessary diagrams. <span class="marks">[2+3+3]</span>

**Section II: Zoology**

**Group A — Rewrite the correct option of each question. 6 × 1 = 6**

12. Which cells of the blood produce antibodies? <span class="marks">[1]</span>
    (a) neutrophils (b) plasma cells (c) eosinophils (d) platelets
13. The hormone that lowers the blood glucose level is <span class="marks">[1]</span>
    (a) glucagon (b) adrenaline (c) insulin (d) cortisol
14. Fertilisation in the human female normally takes place in the <span class="marks">[1]</span>
    (a) uterus (b) ampulla of the fallopian tube (c) cervix (d) ovary
15. Ultrafiltration of blood takes place in the <span class="marks">[1]</span>
    (a) proximal convoluted tubule (b) loop of Henle (c) glomerulus and Bowman's capsule (d) collecting duct
16. Deficiency of vitamin A causes <span class="marks">[1]</span>
    (a) scurvy (b) night blindness (c) rickets (d) beri-beri
17. Which of the following diseases is caused by a protozoan? <span class="marks">[1]</span>
    (a) typhoid (b) tuberculosis (c) malaria (d) cholera

**Group B — Short answer questions. 4 × 4 = 16**

18. Differentiate between bone and cartilage on the basis of matrix, cells, blood supply and location. <span class="marks">[4]</span>
19. Study the given figure of a neuron and answer the questions. <span class="marks">[1+1+2]</span>
    (i) Name the parts A and B. (ii) What is the direction of the nerve impulse in a neuron? (iii) Explain the role of part D and part C in the transmission of the impulse.
    **OR** Describe gastrulation in the frog. <span class="marks">[4]</span>
20. Explain how the hormones insulin and glucagon regulate the blood glucose level. Name one disorder of their imbalance. <span class="marks">[3+1]</span>
21. What is AIDS? Describe how HIV spreads and how it can be prevented. <span class="marks">[1+1.5+1.5]</span>

```figure caption="Question diagram for Paper I, Question 19: a neuron. Letters only."
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse
import numpy as np
fig, ax = plt.subplots(figsize=(4.6, 2.6)); ax.axis('off'); ax.set_xlim(0, 12); ax.set_ylim(0, 6.6)
ax.add_patch(Circle((2.5, 3.3), 1.05, fc='#f3d7b6', ec=INK, lw=1.0)); ax.add_patch(Circle((2.5, 3.3), 0.42, fc='#7a6aa8', ec=INK, lw=0.6))
for a, l in [(150, 1.6), (110, 1.7), (200, 1.5), (250, 1.4), (70, 1.3)]:
    r = np.deg2rad(a); x0, y0 = 2.5 + 1.0*np.cos(r), 3.3 + 1.0*np.sin(r)
    ax.plot([x0, 2.5 + (1.0 + l)*np.cos(r)], [y0, 3.3 + (1.0 + l)*np.sin(r)], color=INK, lw=1.3)
    xe, ye = 2.5 + (1.0 + l)*np.cos(r), 3.3 + (1.0 + l)*np.sin(r)
    ax.plot([xe, xe + 0.3*np.cos(r + 0.5)], [ye, ye + 0.3*np.sin(r + 0.5)], color=INK, lw=1.0); ax.plot([xe, xe + 0.3*np.cos(r - 0.5)], [ye, ye + 0.3*np.sin(r - 0.5)], color=INK, lw=1.0)
ax.plot([3.55, 10.0], [3.3, 3.3], color=INK, lw=1.4)
for x in [4.3, 5.75, 7.2, 8.65]:
    ax.add_patch(Ellipse((x, 3.3), 1.2, 0.62, fc='#f3e6b0', ec=INK, lw=0.8))
for yy in [3.9, 3.3, 2.7]:
    ax.plot([10.0, 10.9], [3.3, yy], color=INK, lw=1.0); ax.add_patch(Circle((11.05, yy), 0.17, fc='white', ec=INK, lw=0.9))
for L, (x, y), (tx, ty) in [('A', (0.94, 4.2), (0.7, 5.75)), ('B', (2.2, 4.1), (2.1, 5.75)), ('C', (6.4, 3.3), (6.4, 1.3)), ('D', (11.05, 3.9), (11.3, 5.6))]:
    ax.annotate('', xy=(x, y), xytext=(tx, ty-0.25 if ty > 3.3 else ty+0.25), arrowprops=dict(arrowstyle='-', color=INK, lw=0.8))
    ax.text(tx, ty, L, ha='center', va='center', fontsize=11, fontweight='bold', color=INK)
```

**Group C — Long answer questions. 2 × 8 = 16**

22. Name the causative agent of malaria. Describe its life cycle in man and in the mosquito. Mention the symptoms and control measures. <span class="marks">[1+3+2+2]</span>
23. Draw a labelled diagram of the human heart in longitudinal section and describe the double circulation of blood. <span class="marks">[3+3+2]</span>
    **OR** Draw a labelled neuron. Explain how a nerve impulse is generated and conducted along an axon. <span class="marks">[2+3+3]</span>

## 10.4 Solutions to Model Question Paper I

::: note Answer key — Group A (Botany 1–5, Zoology 12–17)
**1.** (b) — the root endodermis, through its Casparian strips and living cells, decides what enters the stele. Option (d) belongs to phloem, and the starch-storing endodermis is the stem's.
**2.** (b) — PEP carboxylase in the mesophyll fixes CO₂ as oxaloacetate; RuBisCO works later in the bundle sheath. Choosing RuBisCO is the C3 reflex.
**3.** (c) — 9 : 3 : 3 : 1. Option (a) is the monohybrid ratio.
**4.** (b) — pollen grains form in the anther, from microspore mother cells.
**5.** (c) — the shoot-apex meristem is free of virus; leaf pieces and roots carry it.
**12.** (b) — plasma cells (differentiated B lymphocytes) make antibodies; eosinophils and neutrophils are phagocytes or parasite-killers.
**13.** (c) — insulin (β cells) lowers blood glucose; glucagon raises it.
**14.** (b) — fertilisation occurs in the ampulla; implantation, not fertilisation, is in the uterus.
**15.** (c) — pressure filtration through the glomerular capillaries and Bowman's capsule; the PCT reabsorbs.
**16.** (b) — vitamin A is needed for rhodopsin; scurvy is vitamin C, rickets vitamin D, beri-beri vitamin B₁.
**17.** (c) — malaria is caused by *Plasmodium*, a protozoan; the other three are bacterial.
:::

::: note Solutions — Section I Botany, Group B (6–9)
**6.**

| Basis | Xylem | Phloem |
|---|---|---|
| Cell types | tracheids, vessels, xylem fibres, xylem parenchyma | sieve tubes, companion cells, phloem fibres, phloem parenchyma |
| Living or dead | mostly dead (only the parenchyma lives); walls lignified | mostly living (phloem fibres are dead); walls of cellulose |
| Material conducted | water and dissolved minerals | prepared food (sucrose) and hormones |
| Direction | upward only (root → leaf) | up and down (source → sink) |

**7.** (i) An **open collateral** vascular bundle, as in a dicot stem: xylem and phloem lie on the same radius, with a strip of cambium between them. [1]
(ii) **A** = phloem (sieve tubes and companion cells); **B** = cambium; **C** = metaxylem (large vessels); **D** = protoxylem (small vessels, towards the pith: the xylem is endarch). [2]
(iii) **B, the cambium,** is a meristem; it divides to cut secondary xylem inward and secondary phloem outward, so the stem grows in girth. [1]

**8.** **Law [1].** The two alleles of a gene separate (segregate) when gametes form, so each gamete receives only one allele of the pair; the two alleles meet again at random at fertilisation.
**Monohybrid cross [3].** Pure tall (TT) × pure dwarf (tt) → all F₁ tall (Tt). F₁ self-crossed: gametes T and t from each parent.

| | T | t |
|---|---|---|
| **T** | TT tall | Tt tall |
| **t** | Tt tall | tt dwarf |

F₂: 3 tall : 1 dwarf (phenotypic); 1 TT : 2 Tt : 1 tt (genotypic). The recessive trait reappears unchanged in one quarter of the F₂, which shows that the alleles did not blend but separated.
**OR — effects of auxin [4].** (i) *Cell elongation* in the stem, so shoots grow and bend towards light (phototropism). (ii) *Apical dominance*: the shoot tip suppresses the lateral buds. (iii) *Root initiation* on cuttings (IBA, NAA). (iv) *Parthenocarpy* and prevention of fruit drop; 2,4-D is a selective weed-killer of broad-leaved weeds.

**9.** **Production [2].** The *cry* gene of *Bacillus thuringiensis*, which codes for an insecticidal Cry protein, is cut out with a restriction enzyme and inserted in the **Ti plasmid** of *Agrobacterium tumefaciens*. Cotton cells or explants are infected; the cells that took up the gene are selected on antibiotic medium and **regenerated into plants by tissue culture**, then tested in the field. In the bollworm's alkaline gut the protoxin is activated, binds to the gut wall and kills the larva.
**Benefits [1] and concerns [1].** *Benefits:* less insecticide spraying, lower cost and less poisoning of farmers, higher yield. *Concerns:* pests may evolve resistance, non-target insects may be harmed, genes may flow to wild relatives, and the seed is patented and costly.
:::

::: note Solutions — Section I Botany, Group C (10–11)
**10.** **Krebs cycle [1 + 5].** Sir Hans Krebs described it in 1937. It occurs in the **mitochondrial matrix** and is a cycle because oxaloacetate is regenerated. Each **pyruvate** from glycolysis first enters the link reaction: pyruvate + NAD⁺ + CoA → acetyl CoA + CO₂ + NADH.
(1) Acetyl CoA (2C) + oxaloacetate (4C) → **citrate** (6C) (citrate synthase). (2) Citrate → isocitrate (aconitase). (3) Isocitrate → **α-ketoglutarate** (5C) + CO₂ + **NADH**. (4) α-Ketoglutarate → **succinyl CoA** (4C) + CO₂ + **NADH**. (5) Succinyl CoA → succinate + **GTP** (→ ATP), substrate-level phosphorylation. (6) Succinate → fumarate + **FADH₂**. (7) Fumarate → malate. (8) Malate → **oxaloacetate** + **NADH**.
One turn: 2 CO₂, 3 NADH, 1 FADH₂, 1 ATP (GTP).
**Yield per glucose [2].**

| Stage | NADH | FADH₂ | ATP | CO₂ |
|---|---|---|---|---|
| Link reaction (2 pyruvate) | 2 | 0 | 0 | 2 |
| Krebs cycle (2 turns) | 6 | 2 | 2 | 4 |
| **Total** | **8** | **2** | **2** | **6** |

In the electron transport system the 8 NADH and 2 FADH₂ give about 20 + 3 = 23 ATP (2.5 and 1.5 ATP each); adding 2 ATP gives about 25 ATP from these two stages, and with glycolysis the total is 30–32 ATP per glucose (36–38 in older books).

**11.** **Law [1].** When two or more pairs of contrasting characters are followed together, the alleles of each gene assort independently into the gametes, so the inheritance of one character does not affect that of another.
**Dihybrid cross [5].** Pure round yellow seeds (RRYY) × pure wrinkled green (rryy) → F₁ all round yellow (RrYy). The F₁ makes **four kinds of gametes in equal numbers**: RY, Ry, rY, ry. Selfing the F₁ (4 × 4 = 16 combinations):

| | RY | Ry | rY | ry |
|---|---|---|---|---|
| **RY** | RRYY round yellow | RRYy round yellow | RrYY round yellow | RrYy round yellow |
| **Ry** | RRYy round yellow | RRyy round green | RrYy round yellow | Rryy round green |
| **rY** | RrYY round yellow | RrYy round yellow | rrYY wrinkled yellow | rrYy wrinkled yellow |
| **ry** | RrYy round yellow | Rryy round green | rrYy wrinkled yellow | rryy wrinkled green |

**Ratios [2].** Phenotypic: 9 round yellow : 3 round green : 3 wrinkled yellow : 1 wrinkled green. Genotypic: 1 RRYY : 2 RRYy : 2 RrYY : 4 RrYy : 1 RRyy : 2 Rryy : 1 rrYY : 2 rrYy : 1 rryy (nine genotypes). Two new combinations — round green and wrinkled yellow — appear, which shows that the two characters were inherited independently.
**OR — transcription and translation [2+3+3].** *Gene expression* is the flow DNA → mRNA → protein.
*Transcription (in the nucleus):* RNA polymerase binds the promoter, the DNA opens, and the **template strand** (3′→5′) is copied into a complementary mRNA 5′→3′ (A–U, T–A, G–C, C–G) until the terminator; in eukaryotes the primary transcript is spliced (introns out), capped and given a poly-A tail.
*Translation (on ribosomes in the cytoplasm):* the small ribosomal subunit binds mRNA at the **AUG start codon**; the initiator tRNA (Met) pairs with it; each further codon is matched by a tRNA whose **anticodon** is complementary and which carries the right amino acid; peptide bonds join the amino acids (elongation) as the ribosome moves along the mRNA; a **stop codon** (UAA, UAG, UGA) makes the ribosome release the protein.
*Diagrams [3].* (a) DNA, RNA polymerase and the mRNA strand; (b) ribosome with mRNA, tRNA and the growing polypeptide.
:::

::: note Solutions — Section II Zoology, Group B (18–21)
**18.**

| Basis | Bone | Cartilage |
|---|---|---|
| Matrix | hard, of calcium phosphate and collagen | firm but flexible, of chondroitin sulphate and collagen |
| Cells | osteocytes in lacunae, linked by canaliculi | chondrocytes in lacunae (singly or in groups) |
| Blood supply | rich: blood vessels run in the Haversian canals | none (avascular); fed by diffusion from the perichondrium |
| Location | skeleton: limbs, skull, vertebrae | nose, ear pinna, trachea, ends of long bones, intervertebral discs |

**19.** (i) **A** = dendrites; **B** = cell body (cyton) with the nucleus. [1] (ii) The impulse travels in one direction only: dendrite → cell body → axon → axon terminal. [1] (iii) **C** is the **axon** (here a myelinated one): it conducts the impulse away from the cell body as an action potential; the **myelin sheath with nodes of Ranvier** makes the impulse jump from node to node (saltatory conduction), which is faster. **D** is the **synaptic knob (axon terminal)**: it holds vesicles of neurotransmitter (acetylcholine), which it releases into the synaptic cleft when the impulse arrives, so that the impulse passes to the next neuron or to a muscle. [2]
**OR — gastrulation in the frog [4].** After blastulation the **dorsal lip of the blastopore** appears near the grey crescent. Cells of the animal hemisphere spread over the surface (epiboly) and roll inward over the lip (invagination and involution), forming the **archenteron**, which enlarges as the blastocoel shrinks. The large yolky cells left in the blastopore form the **yolk plug**. By the end, ectoderm outside, endoderm lining the archenteron and mesoderm between them are formed.

**20.** Both hormones come from the islets of Langerhans of the pancreas; they work as opposites in a negative feedback loop. **Insulin [1.5].** When blood glucose rises after a meal, the **β cells** release insulin; it makes muscle and fat cells take in glucose and makes the liver convert glucose to **glycogen** (glycogenesis), so blood glucose falls. **Glucagon [1.5].** When blood glucose falls, the **α cells** release glucagon; it makes the liver break glycogen to glucose (glycogenolysis) and make new glucose from amino acids (gluconeogenesis), so blood glucose rises. **Disorder [1].** Too little insulin, or cells that do not respond to it, causes **diabetes mellitus** (high blood sugar, glucose in urine, thirst, weight loss); too much insulin causes **hypoglycaemia** (shaking, sweating, fainting).

**21.** **AIDS [1].** Acquired immunodeficiency syndrome, caused by **HIV**, an RNA retrovirus that destroys CD4 helper T cells. **Spread [1.5].** Unprotected sexual intercourse; transfusion of infected blood or use of shared needles and razors; from an infected mother to her baby during pregnancy, birth or breast-feeding. It does not spread by touch, mosquito bite, food or shared toilets. **Prevention [1.5].** Faithfulness and condom use; screened blood only; single-use syringes; antiretroviral drugs for infected mothers; education and counselling.
:::

::: note Solutions — Section II Zoology, Group C (22–23)
**22.** **Causative agent [1].** *Plasmodium* (*P. vivax* and *P. falciparum* are the important species), a protozoan carried by the female *Anopheles*.
**Life cycle [3].** *In man:* sporozoites injected by the mosquito go to the liver and multiply (schizogony); the merozoites enter red cells and multiply again, and the cells burst every 48 hours, releasing toxin and more merozoites; some become gametocytes. *In the mosquito:* the mosquito takes up gametocytes with the blood; male and female gametes fuse in its gut; the zygote (ookinete) forms an oocyst on the gut wall, which releases sporozoites into the salivary glands.
**Symptoms [2].** Periodic chills, high fever and sweating; headache and vomiting; anaemia and enlarged spleen; cerebral malaria in severe *falciparum* infection.
**Control [2].** Destroy breeding places (drain stagnant water), indoor residual spraying, larvicides and larvivorous fish; insecticide-treated bed nets and repellents; rapid diagnosis and treatment with artemisinin-based drugs.

**23.** **Diagram [3].** Draw the heart in longitudinal section and label: right atrium, left atrium, right ventricle, left ventricle, tricuspid valve, bicuspid (mitral) valve, semilunar valves, superior and inferior vena cava, pulmonary artery, pulmonary veins, aorta, interventricular septum. (Use the figure below as a model.)

```figure caption="Longitudinal section of the human heart (Paper I, question 23): blue = deoxygenated, red = oxygenated blood."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Ellipse, PathPatch
from matplotlib.path import Path

fig, ax = plt.subplots(figsize=(5.2, 4.6))
MUS = "#c98275"; MED = "#8a4a40"; BLUE = "#9fc0e0"; RED = "#eeb0a6"
VBLUE = "#4a67b8"; VRED = "#b03a3a"

def bez(pts, fc, ec, lw=1.2, z=3):
    assert (len(pts)-1) % 3 == 0, len(pts)
    ax.add_patch(PathPatch(Path(pts, [Path.MOVETO]+[Path.CURVE4]*(len(pts)-1)),
                           fc=fc, ec=ec, lw=lw, zorder=z))

def vessel(pts, c, w=7.0, z=5.5):
    x, y = np.array(pts).T
    ax.plot(x, y, color=MED, lw=w+1.6, solid_capstyle='round', zorder=z)
    ax.plot(x, y, color=c, lw=w, solid_capstyle='round', zorder=z+0.1)

def lab(txt, tip, tx, ty, ha='left', fs=6.2, c=INK):
    ax.annotate(txt, xy=tip, xytext=(tx, ty), fontsize=fs, color=c, ha=ha,
                va='center', zorder=30,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.65,
                                shrinkA=1.5, shrinkB=1.0))

# ---- great vessels (drawn first, behind the heart mass) ----
vessel([(0.55, 3.82), (0.46, 5.20), (0.30, 6.45), (-0.30, 7.32),
        (-1.35, 7.55), (-2.15, 7.00), (-2.48, 6.10), (-2.55, 4.90),
        (-2.58, 4.05)], "#d96a5a", w=7.4, z=5.5)          # aorta + arch
for bx in (-0.20, -0.70, -1.25):
    vessel([(bx, 7.34), (bx-0.05, 8.35)], "#d96a5a", w=4.0, z=5.3)
vessel([(-0.44, 3.80), (-0.34, 5.10), (-0.14, 5.90)], BLUE, w=6.6, z=5.6)
vessel([(-0.14, 5.90), (-0.95, 6.16), (-1.92, 6.28)], BLUE, w=5.4, z=5.6)
vessel([(-0.14, 5.90), (0.70, 6.20), (1.72, 6.32)], BLUE, w=5.4, z=5.6)
vessel([(-1.55, 6.95), (-1.52, 5.90), (-1.50, 5.05)], BLUE, w=6.2, z=5.6)
vessel([(-3.30, 2.05), (-2.85, 3.05), (-2.05, 3.92)], BLUE, w=6.2, z=5.6)
for (ys, ye) in [(5.45, 5.02), (4.20, 4.38)]:
    vessel([(3.20, ys), (2.55, (ys+ye)/2), (1.92, ye)], "#d96a5a", w=5.0, z=5.6)

# ---- heart muscle mass ----
OUT = [(-2.30, 5.30),
       (-2.55, 4.20), (-2.45, 2.70), (-1.70, 1.70),
       (-1.05, 0.90), (0.10, 0.20), (0.95, 0.45),
       (1.75, 0.68), (2.35, 2.20), (2.35, 3.70),
       (2.35, 4.75), (2.10, 5.50), (1.50, 5.60),
       (0.50, 5.78), (-1.40, 5.75), (-2.30, 5.30)]
bez(OUT, MUS, MED, lw=1.3, z=5)

RA = [(-2.02, 4.10), (-2.02, 4.90), (-1.65, 5.24), (-1.00, 5.28),
      (-0.78, 4.95), (-0.76, 4.05), (-1.00, 3.72), (-1.60, 3.68)]
LA = [(0.78, 4.10), (0.80, 4.95), (1.10, 5.26), (1.70, 5.22),
      (2.00, 4.88), (2.02, 4.05), (1.70, 3.70), (1.05, 3.68)]
RV = [(-1.78, 2.95), (-1.70, 3.35), (-0.28, 3.38), (-0.25, 1.85),
      (-0.62, 1.32), (-1.20, 1.50), (-1.62, 2.30)]
LV = [(0.38, 3.30), (1.24, 3.24), (1.40, 2.50), (1.20, 1.66),
      (0.92, 1.24), (0.64, 1.58), (0.40, 2.36)]
for poly, c in [(RA, BLUE), (LA, RED), (RV, BLUE), (LV, RED)]:
    ax.add_patch(Polygon(poly, closed=True, fc=c, ec=MED, lw=1.0, zorder=7))

# ---- valves ----
def av_valve(x0, x1, ytop, ybot, c):
    for xa, xb in [(x0, (x0+x1)/2), ((x0+x1)/2, x1)]:
        ax.add_patch(Polygon([(xa, ytop), (xb, ytop), ((xa+xb)/2, ybot)],
                             closed=True, fc="#fdf4ef", ec=MED, lw=0.9, zorder=8))
        for k in (0.25, 0.75):
            ax.plot([(xa+xb)/2, xa + (xb-xa)*k], [ybot, ybot-0.42],
                    color=MED, lw=0.5, zorder=8)
    ax.plot([x0+0.10, x1-0.10], [ybot-0.48, ybot-0.48], color="#a8625a",
            lw=3.0, zorder=8, solid_capstyle='round')
av_valve(-1.42, -0.34, 3.40, 2.78, MED)     # tricuspid
av_valve(0.42, 1.28, 3.34, 2.76, MED)       # bicuspid (mitral)
for (cx, cy) in [(-0.44, 3.70), (0.55, 3.76)]:
    for s in (-1, 1):
        u = np.linspace(0, 1, 40)
        xs = cx + s*0.21*u
        ax.plot(xs, cy - 0.17*np.sin(np.pi*u), color=MED, lw=1.2, zorder=9.2,
                solid_capstyle='round')
    ax.plot([cx-0.23, cx+0.23], [cy+0.02, cy+0.02], color=MED, lw=0.8,
            zorder=9.2)

# ---- flow arrows ----
def flow(p0, p1, c, z=12, lw=1.5):
    ax.annotate('', xy=p1, xytext=p0, zorder=z,
                arrowprops=dict(arrowstyle='-|>', color=c, lw=lw,
                                mutation_scale=9))
flow((-1.52, 5.85), (-1.50, 5.10), VBLUE)
flow((-2.62, 3.20), (-2.10, 3.82), VBLUE)
flow((-1.30, 4.20), (-1.05, 3.30), VBLUE)
flow((-1.10, 2.30), (-0.52, 3.55), VBLUE)
flow((-0.36, 4.70), (-0.24, 5.60), VBLUE)
flow((2.55, 4.80), (2.05, 4.55), VRED)
flow((1.42, 4.35), (1.12, 3.40), VRED)
flow((0.95, 2.40), (0.50, 3.44), VRED)
flow((0.46, 4.60), (0.36, 5.80), VRED)

# ---- labels ----
lab("aorta (to the body)", (-0.32, 7.36), -3.15, 8.25, ha='right')
lab("carotid / subclavian\nbranches", (-0.72, 8.15), 0.20, 8.42)
lab("superior vena cava", (-1.55, 6.70), -3.15, 7.15, ha='right')
lab("right pulmonary artery", (-1.55, 6.20), -3.15, 6.40, ha='right')
lab("right atrium", (-1.60, 4.70), -3.15, 5.05, ha='right')
lab("tricuspid valve\n(3 cusps)", (-0.95, 3.10), -3.15, 3.55, ha='right')
lab("right ventricle\n(thin wall)", (-1.05, 2.30), -3.15, 2.55, ha='right')
lab("inferior vena cava", (-2.95, 2.60), -3.15, 1.55, ha='right')
lab("pulmonary trunk", (-0.26, 5.45), 0.75, 6.95)
lab("left pulmonary artery", (1.30, 6.24), 2.15, 7.35)
lab("pulmonary veins (4)", (2.75, 5.30), 3.35, 6.35)
lab("left atrium", (1.45, 4.55), 3.35, 5.45)
lab("bicuspid (mitral) valve", (0.86, 3.05), 3.35, 4.20)
lab("semilunar valves", (0.52, 3.72), 3.35, 3.30)
lab("left ventricle —\nwall ≈ 3× thicker", (1.05, 2.10), 3.35, 2.30)
lab("interventricular\nseptum", (0.06, 2.20), 3.35, 1.20)
lab("apex of the heart", (0.95, 0.48), 3.35, 0.35)
lab("chordae tendineae\n+ papillary muscle", (-0.88, 2.40), -1.60, 0.45, ha='center')

ax.set_xlim(-6.20, 6.20); ax.set_ylim(-0.10, 8.90)
ax.set_aspect('equal'); ax.axis('off')
```

**Double circulation [3].** Blood passes through the heart twice in one complete circuit. *Systemic circulation:* left ventricle → aorta → arteries → capillaries of the body (oxygen given up) → veins → superior and inferior **vena cava** → right atrium. *Pulmonary circulation:* right atrium → (tricuspid valve) → right ventricle → **pulmonary artery** (deoxygenated blood) → lungs (oxygen taken up) → **pulmonary veins** → left atrium → (bicuspid valve) → left ventricle.
**Significance [2].** The oxygenated and deoxygenated blood never mix, so the tissues get fully oxygenated blood; the body circuit can keep a high pressure while the lung circuit has a low pressure; this suits warm-blooded animals that need much energy.
**OR — neuron and nerve impulse [2+3+3].** *Neuron [2].* Cell body (cyton) with nucleus and Nissl granules; dendrites that receive; a long axon, wrapped in a myelin sheath from Schwann cells with gaps called nodes of Ranvier; ends in synaptic knobs. *Generation [3].* At rest the membrane is polarised at about **−70 mV** (more Na⁺ outside, more K⁺ inside, kept by the Na⁺–K⁺ pump). A stimulus opens Na⁺ channels; Na⁺ rushes in and the inside becomes positive (**depolarisation**, about +35 mV): the action potential. Then K⁺ channels open, K⁺ leaves and the membrane returns to −70 mV (**repolarisation**). *Conduction [3].* The action potential depolarises the next patch of membrane, so it travels as a wave; in a myelinated axon it jumps from node to node (**saltatory conduction**), reaching up to 100 m s⁻¹. It follows the all-or-none law. At the synapse the impulse is carried by neurotransmitter.
:::

## 10.5 Model question paper II

::: note Model Question Paper II — Biology (Sub. Code 2021)
**NEB-XII Model Set II.** Time: 3 hrs. Full marks: 75. Candidates are required to give their answers in their own words as far as practicable. The figures in the margin indicate full marks. Attempt all the questions. Complete Section I (Botany) first and then Section II (Zoology).
:::

**Section I: Botany**

**Group A — Rewrite the correct option of each question. 5 × 1 = 5**

1. Which of the following is a lateral (secondary) meristem? <span class="marks">[1]</span>
   (a) shoot apex (b) root apex (c) cork cambium (d) intercalary meristem
2. Which plant hormone promotes closure of stomata during water stress? <span class="marks">[1]</span>
   (a) auxin (b) gibberellin (c) abscisic acid (d) cytokinin
3. Replacement of one purine by another purine in DNA is called <span class="marks">[1]</span>
   (a) transversion (b) transition (c) frame shift (d) deletion
4. The triploid primary endosperm nucleus is formed when one male gamete fuses with <span class="marks">[1]</span>
   (a) the egg (b) a synergid (c) the two polar nuclei (d) an antipodal cell
5. The biofertiliser that lives in the root nodules of pulses and fixes nitrogen is <span class="marks">[1]</span>
   (a) *Rhizobium* (b) *Azotobacter* (c) *Trichoderma* (d) *Bacillus thuringiensis*

**Group B — Short answer questions. 4 × 4 = 16**

6. Write four differences between a dicot leaf and a monocot leaf. <span class="marks">[4]</span>
7. Study the given figure of a flower part and answer the questions. <span class="marks">[1+2+1]</span>
   (i) Identify the figure. (ii) Name the parts A to D. (iii) What is the function of part B, and what does part D become after fertilisation?
8. Explain the cohesion–tension theory of the ascent of sap and give one evidence in its support. <span class="marks">[3+1]</span>
   **OR** Describe any two functions each of gibberellins and cytokinins in plants. <span class="marks">[4]</span>
9. Explain the use of biofertilisers and green manure in sustainable agriculture, with two examples of each. <span class="marks">[2+2]</span>

**Group C — Long answer questions. 2 × 8 = 16**

10. Describe the C4 pathway of photosynthesis (Hatch–Slack pathway) with the help of the Kranz anatomy of the leaf. Why are C4 plants more efficient in hot, dry climates? <span class="marks">[1+5+2]</span>
11. What is linkage? Describe Morgan's experiment on linkage in *Drosophila* and explain how crossing over breaks linkage. Mention the significance of crossing over. <span class="marks">[1+4+1+2]</span>
    **OR** Describe the different types of RNA and their roles in protein synthesis. <span class="marks">[2+6]</span>

**Section II: Zoology**

**Group A — Rewrite the correct option of each question. 6 × 1 = 6**

12. Intercalated discs are found in <span class="marks">[1]</span>
    (a) skeletal muscle (b) smooth muscle (c) cardiac muscle (d) striated voluntary muscle
13. In human oogenesis the secondary oocyte is arrested at <span class="marks">[1]</span>
    (a) prophase I (b) metaphase II (c) anaphase II (d) telophase I
14. The pH of the human gastric juice is about <span class="marks">[1]</span>
    (a) 1.5–2.0 (b) 4.5–5.0 (c) 6.8 (d) 8.0
15. The hormone that maintains the endometrium and the pregnancy is <span class="marks">[1]</span>
    (a) FSH (b) progesterone (c) LH (d) thyroxine
16. Which of the following is a depressant drug? <span class="marks">[1]</span>
    (a) caffeine (b) nicotine (c) alcohol (d) cocaine
17. The vaccine that protects against tuberculosis is <span class="marks">[1]</span>
    (a) OPV (b) DPT (c) BCG (d) MMR

**Group B — Short answer questions. 4 × 4 = 16**

18. Write four differences between epithelial tissue and connective tissue. <span class="marks">[4]</span>
19. Study the given figure of a human spermatozoon and answer the questions. <span class="marks">[1+1+2]</span>
    (i) Name the parts A and B. (ii) What is the role of part C? (iii) Why is part D important in fertilisation?
    **OR** Explain the metamorphosis of a frog tadpole into an adult frog and the role of thyroxine. <span class="marks">[2+2]</span>
20. Explain how the human eye focuses on near and distant objects. Name one defect of vision with its correction. <span class="marks">[3+1]</span>
21. What is family planning? Name four methods of contraception and give one merit or demerit of each. <span class="marks">[1+3]</span>

```figure caption="Question diagram for Paper II, Question 7: longitudinal section of a pistil. Letters only."
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle, Rectangle
fig, ax = plt.subplots(figsize=(4.0, 3.6)); ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 9.4)
ax.add_patch(Ellipse((4.0, 2.6), 4.6, 4.2, fc='#dff2d9', ec=INK, lw=1.2))
ax.add_patch(Ellipse((4.0, 2.6), 3.7, 3.3, fc='#fdf6e3', ec=INK, lw=0.7))
for x, y in [(3.0, 2.0), (4.0, 1.5), (5.0, 2.0), (3.2, 3.4), (4.8, 3.4)]:
    ax.add_patch(Ellipse((x, y), 0.75, 0.55, fc='#ffd9a8', ec=INK, lw=0.7)); ax.add_patch(Circle((x, y), 0.14, fc='#8a6cc1', ec='none'))
ax.add_patch(Rectangle((3.75, 4.6), 0.5, 2.6, fc='#b7d99a', ec=INK, lw=0.9))
ax.add_patch(Ellipse((4.0, 7.65), 2.0, 0.9, fc='#e9c46a', ec=INK, lw=0.9))
for dx in [-0.7, -0.35, 0, 0.35, 0.7]: ax.plot([4.0+dx, 4.0+dx], [7.8, 8.2], color=INK, lw=0.8)
for L, (x, y), (tx, ty) in [('A', (4.7, 7.85), (8.2, 8.3)), ('B', (4.25, 6.0), (8.2, 6.2)), ('C', (6.2, 3.4), (8.2, 3.9)), ('D', (5.0, 2.0), (8.2, 1.6))]:
    ax.annotate('', xy=(x, y), xytext=(tx-0.25, ty), arrowprops=dict(arrowstyle='-', color=INK, lw=0.8))
    ax.text(tx, ty, L, ha='left', va='center', fontsize=11, fontweight='bold', color=INK)
```

```figure caption="Question diagram for Paper II, Question 19: a mature human spermatozoon. Letters only."
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle, Rectangle
import numpy as np
fig, ax = plt.subplots(figsize=(4.6, 2.3)); ax.axis('off'); ax.set_xlim(0, 13); ax.set_ylim(0, 5.4)
ax.add_patch(Ellipse((2.0, 2.4), 2.6, 1.6, fc='#c9b8e6', ec=INK, lw=1.0))
ax.add_patch(Ellipse((1.2, 2.4), 1.1, 1.45, fc='#e7d9a8', ec=INK, lw=0.8))
ax.add_patch(Rectangle((3.25, 2.2), 0.45, 0.4, fc='#9ec1a0', ec=INK, lw=0.7))
ax.add_patch(Rectangle((3.7, 2.2), 2.1, 0.4, fc='#d9a0a0', ec=INK, lw=0.7))
for x in np.arange(3.9, 5.75, 0.3): ax.plot([x, x], [2.2, 2.6], color=INK, lw=0.5)
xs = np.linspace(5.8, 12.4, 100); ax.plot(xs, 2.4 + 0.12*np.sin((xs-5.8)*2.4), color=INK, lw=1.4)
for L, (x, y), (tx, ty) in [('A', (1.0, 3.0), (0.8, 4.6)), ('B', (2.3, 3.0), (3.0, 4.6)), ('C', (4.7, 2.6), (5.0, 4.2)), ('D', (9.0, 2.45), (9.0, 0.8))]:
    ax.annotate('', xy=(x, y if ty > 2.4 else y-0.05), xytext=(tx, ty-0.25 if ty > 2.4 else ty+0.25), arrowprops=dict(arrowstyle='-', color=INK, lw=0.8))
    ax.text(tx, ty, L, ha='center', va='center', fontsize=11, fontweight='bold', color=INK)
```

**Group C — Long answer questions. 2 × 8 = 16**

22. Name the causative agent of hepatitis B. Explain its mode of transmission and symptoms. Mention the preventive measures and the serious complications of the disease. <span class="marks">[1+2+2+2+1]</span>
23. Draw a labelled diagram of the human ear. Explain how sound is heard. What is the role of the semicircular canals? <span class="marks">[3+3+2]</span>
    **OR** Describe urine formation in the nephron: ultrafiltration, selective reabsorption and tubular secretion. State the role of ADH. <span class="marks">[2+4+2]</span>

## 10.6 Solutions to Model Question Paper II

::: note Answer key — Group A (Botany 1–5, Zoology 12–17)
**1.** (c) — cork cambium is a lateral meristem. Shoot and root apices are apical, and the intercalary meristem is in grass internodes.
**2.** (c) — abscisic acid, the stress hormone, closes stomata. Gibberellin and cytokinin tend to keep them open.
**3.** (b) — a transition is purine→purine or pyrimidine→pyrimidine; a transversion swaps the classes (option a).
**4.** (c) — one male gamete + two polar nuclei = 3n endosperm nucleus; the other male gamete fuses with the egg.
**5.** (a) — *Rhizobium* forms root nodules on legumes; *Azotobacter* is free-living.
**12.** (c) — intercalated discs join cardiac muscle cells.
**13.** (b) — the secondary oocyte is arrested at metaphase II until a sperm enters.
**14.** (a) — HCl gives a pH of about 1.5–2.0. The value 6.8 is saliva.
**15.** (b) — progesterone of the corpus luteum, later of the placenta.
**16.** (c) — alcohol depresses the central nervous system; caffeine, nicotine and cocaine are stimulants.
**17.** (c) — BCG; OPV is polio, DPT is diphtheria, pertussis and tetanus.
:::

::: note Solutions — Section I Botany, Group B (6–9)
**6.**

| Dicot leaf | Monocot leaf |
|---|---|
| Dorsiventral: upper and lower surfaces differ | Isobilateral: both surfaces alike |
| Mesophyll differentiated into palisade and spongy parenchyma | Mesophyll not differentiated |
| Stomata mostly on the lower surface; guard cells kidney-shaped | Stomata on both surfaces; guard cells dumb-bell-shaped |
| Reticulate venation; no bulliform cells | Parallel venation; bulliform cells on the upper epidermis |

**7.** (i) **Longitudinal section of a carpel (pistil)**. (ii) **A** = stigma; **B** = style; **C** = ovary (wall); **D** = ovule. (iii) **The style** is the tube through which the pollen tube grows down to the ovary; **the ovule D becomes the seed** after fertilisation (and the ovary becomes the fruit).

**8.** **Cohesion–tension theory [3].** Proposed by Dixon and Joly (1894). Water is lost by transpiration from the leaf mesophyll, creating a tension (negative pressure) in the leaf xylem. Because water molecules **cohere** to each other (hydrogen bonds) and **adhere** to the xylem walls, the water column, unbroken from leaf to root, is pulled up as a continuous stream; the tension can reach many atmospheres, enough for the tallest trees. **Evidence [1].** The diameter of a tree trunk shrinks slightly by day, when transpiration is at its highest, showing that the xylem is under tension; a cut stem pulls in air or coloured water.
**OR [4].** *Gibberellins:* (i) stretch the internodes (bolting) and make dwarf plants tall; (ii) break seed and bud dormancy and promote germination of cereals (barley malting); (iii) produce seedless, larger grapes. *Cytokinins:* (i) promote cell division (with auxin) and shoot formation in tissue culture; (ii) delay leaf senescence; (iii) break apical dominance. (Any two of each.)

**9.** **Biofertilisers [1] and green manure [1], with examples [2].** A biofertiliser is a living microorganism that increases soil fertility or the nutrient supply of a plant: *Rhizobium* for legumes, *Azotobacter* for cereals, *Azolla* with *Anabaena* for rice fields, phosphate-solubilising bacteria. Green manure is a crop grown and **ploughed into the soil while still green** to add organic matter and nitrogen: *Sesbania* (dhaincha), *Crotalaria* (sunhemp). **Sustainability.** They replace costly imported chemical fertiliser, improve soil structure and water holding capacity, avoid soil and water pollution, and keep the soil microbes alive.
:::

::: note Solutions — Section I Botany, Group C (10–11)
**10.** **Introduction [1].** The C4 pathway, worked out by Hatch and Slack (1966), is a carbon-concentrating mechanism in plants such as maize and sugarcane.
**Kranz anatomy.** The leaf shows two types of photosynthetic cells: **mesophyll cells** and, round every vein, a ring of large **bundle-sheath cells** with big chloroplasts — the **Kranz** ("wreath") arrangement.
**Pathway [5].**
1. *In the mesophyll.* CO₂ enters as bicarbonate; **PEP carboxylase** joins it to **phosphoenolpyruvate (PEP, 3C)** to form **oxaloacetate (OAA, 4C)**, the first stable product. PEP carboxylase has no affinity for O₂.
2. OAA is converted to **malate** (or aspartate), which moves through plasmodesmata into the **bundle sheath**.
3. *In the bundle sheath.* Malate is **decarboxylated**: CO₂ is released at a high concentration and pyruvate (3C) is left.
4. The CO₂ enters the normal **Calvin cycle**: RuBisCO fixes it, because the local CO₂ is so high that RuBisCO acts as a carboxylase and **photorespiration is almost suppressed**.
5. Pyruvate returns to the mesophyll, where **pyruvate phosphate dikinase** (using 2 ATP equivalents) regenerates PEP.
**Efficiency [2].** In hot, dry air the stomata partly close, the leaf CO₂ falls and O₂ rises, which makes RuBisCO in C3 plants waste carbon in photorespiration. The C4 plant pumps CO₂ into the bundle sheath, so it keeps photosynthesising at a high temperature (30–45 °C) with stomata closed, loses less water per gram of dry matter and has a higher yield, though at an extra cost of 2 ATP per CO₂.

**11.** **Linkage [1].** The tendency of genes that lie on the same chromosome to be inherited together.
**Morgan's experiment [4].** Morgan crossed a grey-bodied, long-winged fly (b⁺b⁺ vg⁺vg⁺) with a black-bodied, vestigial-winged fly (bb vgvg); the F₁ were all grey and long. He test-crossed an F₁ female with a black vestigial male (bb vgvg) and expected 1 : 1 : 1 : 1 if the genes assorted independently. He got 965 grey long : 944 black vestigial : 206 grey vestigial : 185 black long. **Parental types were 83 %** and **recombinants 17 %**, so the genes were linked on the same chromosome; the few recombinants showed that linkage is incomplete.
**How crossing over breaks linkage [1].** In prophase I of meiosis in the heterozygous female, non-sister chromatids of the homologues exchange segments at pachytene; the gametes Bvg and bVg⁺ carry new combinations, so the grey vestigial and black long flies appear. No crossing over occurs in male *Drosophila*, which is why a female is used.
**Significance [2].** It produces variation, it makes **gene maps** possible (1 % recombination = 1 map unit), and it lets breeders combine useful genes.
**OR — types of RNA [2+6].** RNA is a single-stranded polymer of ribonucleotides containing ribose and uracil; it is made on a DNA template by transcription.
*mRNA (messenger)* — about 5 % of cellular RNA; copies the gene; each three bases form a codon; it carries the message to the ribosome. *tRNA (transfer)* — clover-leaf, 75–90 nucleotides, with an **anticodon** loop and an amino-acid attachment site at the 3′ end; it reads the codon and brings the matching amino acid. *rRNA (ribosomal)* — the commonest RNA (~80 %); with proteins it forms the two ribosomal subunits, the site of translation, and catalyses peptide-bond formation.
*In protein synthesis:* mRNA is made in the nucleus and moves to the cytoplasm; the ribosome (rRNA) binds it at AUG; tRNAs bring amino acids in the order the codons dictate; the ribosome joins them by peptide bonds until a stop codon ends the chain. *Minor types:* snRNA (splicing) and miRNA (gene regulation).
:::

::: note Solutions — Section II Zoology, Group B (18–21)
**18.**

| Epithelial tissue | Connective tissue |
|---|---|
| Cells closely packed with very little matrix | Cells scattered in a large amount of matrix |
| Forms coverings and linings of organs and glands | Binds, supports and connects other tissues |
| Rests on a basement membrane; no blood vessels | Usually has blood vessels (except cartilage) |
| Types: squamous, cuboidal, columnar, stratified | Types: areolar, adipose, tendon, cartilage, bone, blood |

**19.** (i) **A** = acrosome (cap of the head); **B** = nucleus (inside the head), containing the haploid set of chromosomes. [1] (ii) **C, the middle piece,** contains the mitochondria in a spiral; it supplies the ATP for movement of the tail. [1] (iii) **D, the tail,** is a flagellum whose lashing movement propels the sperm up the female tract to the egg; without it the sperm could not reach the egg (the acrosome enzymes, hyaluronidase and acrosin, then let the head penetrate it).
**OR — metamorphosis [2+2].** The tadpole hatches with external gills, a tail and a herbivorous gut. Changes: hind limbs appear, then forelimbs; the tail is resorbed by its cells' lysosomes; gills are replaced by lungs; the long coiled gut shortens as the diet changes to carnivorous; the skin thickens and the lateral line disappears; the heart changes from two to three chambers. **Thyroxine** from the thyroid (stimulated by TSH) triggers and coordinates the changes; without iodine or the gland, the tadpole grows but never metamorphoses, and injecting thyroxine speeds it up.

**20.** The eye focuses by changing the **curvature of the lens (accommodation)**, controlled by the ciliary muscle and the suspensory ligaments.
*Distant object [1.5].* The ciliary muscle relaxes, the suspensory ligaments tighten and pull the lens flat; its focal length rises, so parallel rays focus on the retina. *Near object [1.5].* The ciliary muscle contracts, the ligaments slacken, the lens becomes thicker and rounder (shorter focal length), so diverging rays from a near object focus on the retina; the pupil also constricts.
*Defect [1].* **Myopia** (short sight): the eyeball is too long, so distant objects focus in front of the retina; corrected with **concave** lenses. (Hypermetropia is corrected with convex lenses.)

**21.** **Family planning [1].** Planning the number and spacing of children by voluntary use of contraception to protect the health of mother and child and to control population. **Methods [3].**

| Method | Type | Merit / demerit |
|---|---|---|
| Condom | barrier | also protects against STIs and HIV; may tear |
| Oral contraceptive pill | hormonal | very effective when taken daily; may cause nausea or clots |
| Copper-T (IUD) | intra-uterine | works 5–10 years; needs a trained health worker for insertion |
| Vasectomy / tubectomy | surgical, permanent | almost 100 % effective; hard to reverse |
:::

::: note Solutions — Section II Zoology, Group C (22–23)
**22.** **Causative agent [1].** Hepatitis B virus (HBV), a **DNA** virus of the family Hepadnaviridae.
**Transmission [2].** **Blood and body fluids**: transfusion of infected blood, sharing of needles and razors, unprotected sexual intercourse, and from an infected **mother to her baby** at birth. It does **not** spread by food and water (that is hepatitis A and E).
**Symptoms [2].** After an incubation of 1–6 months: loss of appetite, nausea, fatigue, fever and joint pain, **jaundice** (yellow skin and eyes), dark urine, pale stools and right-side abdominal pain.
**Prevention [2].** **Hepatitis B vaccine** (in Nepal given in the pentavalent vaccine to infants); screening of donated blood; single-use needles and syringes; safe sex; vaccination of newborns of infected mothers; health workers must be vaccinated.
**Complications [1].** **Chronic hepatitis, cirrhosis of the liver and liver cancer** (hepatocellular carcinoma).

**23.** **Diagram [3].** Draw the outer ear (pinna, auditory canal, tympanic membrane), the middle ear (malleus, incus, stapes, oval window, round window, Eustachian tube) and the inner ear (cochlea, vestibule with utriculus and sacculus, three semicircular canals, auditory nerve). Use the ear figure given in section 9.8 as the model.
**Hearing [3].** Sound waves are collected by the **pinna** and travel down the **auditory canal** to the **tympanic membrane (eardrum)**, which vibrates. The vibrations are passed and amplified by the three **ossicles** — malleus, incus and stapes — to the **oval window**. They set the **perilymph** of the cochlea moving; waves in the fluid move the **basilar membrane**, and the **hair cells of the organ of Corti** bend against the tectorial membrane and fire impulses in the **auditory nerve** to the **temporal lobe** of the cerebrum, where the sound is perceived. The round window bulges to relieve the pressure; the **Eustachian tube** equalises the air pressure on both sides of the eardrum.
**Semicircular canals [2].** Three canals in three planes at right angles, each with an ampulla and a crista with hair cells. When the head rotates, the endolymph lags, bends the hair cells and sends impulses through the vestibular nerve to the cerebellum, which adjusts posture: they sense **rotation and dynamic balance**; the utriculus and sacculus sense static balance and linear movement.
**OR — urine formation [2+4+2].** *Ultrafiltration [2]:* in the **glomerulus** the blood pressure (about 70 mm Hg, high because the afferent arteriole is wider than the efferent) forces water, glucose, amino acids, salts and urea through the capillary wall, the basement membrane and the podocytes into Bowman's capsule; proteins and cells stay. About 125 mL a minute (180 L a day) of **glomerular filtrate** is formed. *Selective reabsorption [4]:* in the **PCT** all the glucose and amino acids, most Na⁺, K⁺, HCO₃⁻ and about 65 % of the water are returned to the blood by active and passive transport; the **loop of Henle** builds a concentration gradient (descending limb loses water, ascending limb pumps out salt); the **DCT and collecting duct** reabsorb more water under ADH. About 99 % of the filtrate is reclaimed. *Tubular secretion:* the DCT secretes H⁺, K⁺, NH₃ and drugs into the tubule, controlling the blood pH and ion balance. The remaining fluid is **urine** (about 1.5 litres a day). *ADH [2]:* antidiuretic hormone from the posterior pituitary makes the DCT and collecting duct permeable to water; when the body is short of water more ADH is released and small volumes of concentrated urine result; when there is plenty, less ADH gives copious dilute urine. Too little ADH causes diabetes insipidus.
:::

## 10.7 Ranked predicted questions for the coming exam

How the ranking works. **A** = the unit is certain (it has carried marks in all four papers) **and** the topic has not yet been set in the slot where the board habitually asks it; **B** = the topic has appeared only as an OR, a short or an MCQ and has not been the main long question; **C** = plausible but the unit has been set less regularly. Within each grade the order follows the *gap* (how long the topic has been absent) and the *unit weight* from 10.2. Every entry gives the reason and a compact model answer; where a fuller answer exists earlier in this part, it is pointed to. **No entry is a forecast of the real paper.**

### Botany — long questions (8 marks)

1. **(A) Describe the Krebs cycle and the electron transport system; state the ATP yield of aerobic respiration.** *Why:* a Physiology long appeared in all four papers; glycolysis (model 2079) and three photosynthesis topics have been set, respiration beyond glycolysis has not. *Answer:* link reaction in the matrix (pyruvate → acetyl CoA + CO₂ + NADH); cycle: acetyl CoA + oxaloacetate → citrate → … → oxaloacetate, giving per turn 3 NADH, 1 FADH₂, 1 ATP, 2 CO₂; ETS on the inner mitochondrial membrane (complexes I–IV, O₂ the final acceptor, chemiosmosis, ATP synthase); total 30–32 ATP (36–38 classical). Full answer: Model Paper I, Q10.
2. **(A) C4 pathway and Kranz anatomy; compare C3 and C4.** *Why:* the same reason; Kranz anatomy was an MCQ in the model 2079 paper (maize) and C4 has never been a long question. *Answer:* PEP carboxylase in mesophyll → oxaloacetate → malate → bundle sheath → CO₂ released → Calvin cycle; pyruvate returns, PEP regenerated by 2 ATP; no photorespiration. Full answer: Model Paper II, Q10.
3. **(A) State and explain Mendel's laws of inheritance using monohybrid and dihybrid crosses.** *Why:* Genetics supplied one long in every paper, but Mendelian genetics (6 teaching hours) has never been the long question; the replication/mutation/sex-linkage topics have used the slot. *Answer:* law of dominance, segregation (3 : 1, 1 : 2 : 1), independent assortment (9 : 3 : 3 : 1); test cross 1 : 1. Full answer: Model Paper I, Q8 and Q11.
4. **(A) Explain transcription, the genetic code and translation (protein synthesis).** *Why:* replication, mutation and structure have had their turn; gene expression has not (it appears only as an OR in Model Paper I). *Answer:* RNA polymerase copies the template strand to mRNA; 64 codons, 61 sense, 3 stop, AUG start; ribosome + tRNA anticodons + peptide bonds; stop codon releases the chain. Full answer: Model Paper I, Q11 (OR).
5. **(B) Describe secondary growth in a dicot stem with diagrams.** *Why:* Anatomy has carried 5 marks in every paper but never a long question; secondary growth is the most "longable" topic. *Answer:* fascicular + interfascicular cambium → ring; secondary xylem inside, phloem outside; cork cambium → phellem, phelloderm; annual rings; lenticels. Full answer: 9.1 Q7.
6. **(B) Mechanism of stomatal opening and closing; factors affecting transpiration.** *Why:* every Physiology long so far was photosynthesis or respiration; water relations (4 hours) have only produced shorts. *Answer:* in light K⁺ and malate enter guard cells, water follows, the thin-walled dorsal wall bulges and the pore opens; ABA closes it; factors: light, temperature, humidity, wind, soil water, leaf area.
7. **(B) Describe the development of the male gametophyte and the structure of the pollen grain.** *Why:* the 2081 short on the pollen grain suggests the board is now drawing from Embryology. *Answer:* anther with four microsporangia → microspore mother cells (2n) → meiosis → tetrad → microspores (n) → mitosis → vegetative and generative cells; exine, intine, germ pores; the generative cell divides into two male gametes.
8. **(B) Describe the development of the embryo sac and double fertilisation.** *Why:* never asked as a long question. *Answer:* functional megaspore → 3 mitoses → 7 cells, 8 nuclei; pollen tube through micropyle; syngamy + triple fusion. Full answer: 9.4 Q6, and 9.4 Q4.
9. **(C) Describe plant tissue culture and its applications.** *Why:* Biotechnology has produced a short in every paper, never a long. *Answer:* explant → sterile MS medium → callus → shoot and root → hardening; uses. Full answer: 9.5 Q6.
10. **(C) Explain genetic engineering: steps of recombinant DNA technology and its applications.** *Why:* the Q9 shorts on GMOs (2082) and biotechnology (model 2079) lead to it. *Answer:* isolate gene, cut with restriction enzyme, ligate into a vector, transform host, select, express; Bt cotton, Golden Rice, insulin.

### Zoology — long questions (8 marks)

11. **(A) Malaria: causative agent, life cycle, symptoms, control.** *Why:* Q22 was a bacterial disease in all four papers; the next most-examined diseases of the syllabus are malaria, AIDS and hepatitis. *Answer:* *Plasmodium*, female *Anopheles*; schizogony in liver and red cells, gametocytes, sporogony in the mosquito; periodic fever; nets, spraying, artemisinin. Full answer: 9.9 Q6 and Model Paper I, Q22.
12. **(A) Typhoid (again).** *Why:* the only disease set twice (model 2079, 2081); the board has repeated a disease within two years. *Answer:* *Salmonella* Typhi; faeco-oral route; step-ladder fever, rose spots; safe water, vaccine, Widal test. Full answer: 9.10 Q7.
13. **(A) Cholera, tuberculosis (repeat) or AIDS.** *Why:* cholera (2079) and TB (2082) were each asked once; AIDS has been an MCQ or short, never the long. *Answer:* see 9.10 Q8 and Q9 and 9.9 Q5. For AIDS: HIV, retrovirus, CD4 T-cell destruction, sexual contact, blood, mother to child, ELISA test, ART, prevention.
14. **(A) Structure of the human heart and double circulation; cardiac cycle.** *Why:* Q23 is a labelled organ system every time; digestive, reproductive, excretory and (as OR) circulation via the SA node have been set, but the heart's structure has not. *Answer:* four chambers, valves, vessels; double circulation; cardiac cycle of 0.8 s (atrial systole 0.1, ventricular systole 0.3, diastole 0.4). Full answer: Model Paper I, Q23.
15. **(A) Neuron, nerve impulse and synapse; reflex arc.** *Why:* the nervous system (3 hours) has not produced a long; the neuron was only a short figure. *Answer:* structure of a neuron; resting potential −70 mV, depolarisation, repolarisation; saltatory conduction; synapse with neurotransmitter; reflex arc receptor → sensory neuron → spinal cord → motor neuron → effector. Full answer: Model Paper I, Q23 (OR).
16. **(B) Endocrine glands: pituitary, thyroid and their disorders.** *Why:* Endocrinology is the biggest sub-unit of Human Biology (9 hours) and so far supplied only shorts and MCQs. *Answer:* hypothalamus–pituitary axis; anterior lobe: GH, TSH, ACTH, FSH, LH, prolactin; posterior lobe: oxytocin, ADH; thyroid: thyroxine, calcitonin; disorders: gigantism, acromegaly, dwarfism, goitre, cretinism, myxoedema, Graves', diabetes insipidus.
17. **(B) The menstrual cycle with its hormonal control.** *Why:* the female reproductive system was the 2082 long; the cycle is its natural sequel and has never been set. *Answer:* 28 days; menstrual phase days 1–5, follicular/proliferative phase to day 13 (FSH, oestrogen), ovulation on day 14 (LH surge), luteal/secretory phase (corpus luteum, progesterone); if no fertilisation, falling progesterone causes menstruation.
18. **(B) The structure of the ear and the mechanism of hearing; or the brain.** *Why:* the ear was a 2082 short and the eye was 2079 and 2081 OR, so a sense organ long is due. *Answer:* Model Paper II, Q23 (ear); for the brain: forebrain (cerebrum with four lobes, thalamus, hypothalamus), midbrain, hindbrain (cerebellum, pons, medulla).
19. **(C) Mechanism of breathing, lung volumes and transport of oxygen.** *Why:* only the CO₂ transport OR has been set from respiration. *Answer:* inspiration by diaphragm and external intercostals, expiration passive; TV 500 mL, IRV 3000, ERV 1100, RV 1200, VC 4600; oxygen carried as oxyhaemoglobin, dissociation curve, Bohr effect.

### Botany — short questions (4 marks)

20. **(A) Differentiate between xylem and phloem.** *Why:* Q6 has been a tissue question in all four papers; complex tissues were set in 2082 only as "simple vs complex". *Answer:* Model Paper I, Q6.
21. **(A) Differentiate between collenchyma and sclerenchyma; write two functions of each.** *Why:* same slot; the third simple tissue has not been set alone. *Answer:* collenchyma living, corners thickened with cellulose and pectin, support young stems and petioles; sclerenchyma dead, lignified, fibres and sclereids, strength to mature parts.
22. **(A) Write four differences between a dicot root and a monocot root (or stem).** *Why:* the bundle/root/stem comparison is the standard Q6 or figure question. *Answer:* 9.1 Q5–Q6.
23. **(A) Explain Mendel's law of segregation with a monohybrid cross, or define test cross and back cross.** *Why:* Q8 has been an incomplete dominance, linkage or polyploidy question; segregation and test cross are the core not yet set as a short. *Answer:* Model Paper I, Q8.
24. **(B) How is sex determined in humans? Why is the father responsible for the sex of a child?** *Why:* the sex-linked questions (2079, 2080, 2082) rest on this basis. *Answer:* 22 pairs of autosomes + XX in female, XY in male; all eggs carry X; half the sperm carry X, half Y; X-sperm → girl, Y-sperm → boy; 1 : 1.
25. **(B) ABO blood groups as an example of multiple alleles and codominance.** *Why:* multiple alleles are in the syllabus and not yet asked beyond the blood-group MCQ pattern. *Answer:* alleles I^A, I^B, i; I^A = I^B codominant, both dominant over i; genotypes and phenotypes of the four groups; O child needs two *i* alleles.
26. **(B) Explain double fertilisation and its significance.** *Why:* one of the most basic Embryology topics and never set. *Answer:* 9.4 Q4.
27. **(B) Describe types of pollination and the adaptations of wind-pollinated and insect-pollinated flowers.** *Why:* pollination has been absent from the papers since the 2079 MCQ pattern. *Answer:* autogamy, geitonogamy, xenogamy; anemophily and entomophily adaptations; 9.4 Q5.
28. **(B) Describe the role of any two hormones: auxin, gibberellin, cytokinin, ABA, ethylene.** *Why:* plant hormones appear only in MCQs (2081, 2082 set). *Answer:* Model Paper I, Q8 (OR) and Model Paper II, Q8 (OR).
29. **(C) Distinguish between C3 and C4 plants, or explain photorespiration.** *Why:* the MCQ on Kranz anatomy suggests C4 is in the board's question bank. *Answer:* 9.2 Q5.
30. **(C) Explain the role of biofertilisers, biopesticides and green manure in sustainable agriculture.** *Why:* Q9 has drawn on the applications of biotechnology each year. *Answer:* Model Paper II, Q9; 9.5 Q5.

### Zoology — short questions (4 marks)

31. **(A) Write the differences between bone and cartilage (or between tendon and ligament).** *Why:* Q18 or Q20 is a tissue comparison in every paper; areolar/adipose (model 2079), muscle (2081) and epithelia (2079, 2082) are done; bone and cartilage have not been set. *Answer:* Model Paper I, Q18.
32. **(A) Describe the structure of a neuron with a labelled diagram (nervous tissue).** *Why:* nervous tissue is the fourth tissue of the unit and has not been asked. *Answer:* cyton (nucleus, Nissl granules), dendrites, axon, myelin sheath, nodes of Ranvier, axon terminal; impulse one way.
33. **(A) Explain cleavage and morula formation in the frog.** *Why:* the frog-stage short has covered blastulation (model 2079), coelom (2081) and neurulation (2082); cleavage and gastrulation are still open. *Answer:* cleavage is rapid mitosis without growth: 1st and 2nd vertical, 3rd horizontal above the equator, giving micromeres and macromeres; holoblastic unequal; morula of 32–64 cells. Gastrulation: Model Paper I, Q19 (OR).
34. **(A) Describe spermatogenesis with a labelled diagram.** *Why:* oogenesis was asked in 2079 and a sperm is a typical figure question. *Answer:* spermatogonia → primary spermatocyte → secondary spermatocytes → spermatids → spermatozoa (spermiogenesis); Sertoli cells; four sperm per primary spermatocyte. Diagram: 9.7, compared figure.
35. **(A) Write a plan or opinion on a health problem: alcohol, tobacco, drug abuse, adolescent health, HIV stigma or diabetes.** *Why:* Q21 has been a health-and-society short in every paper. *Answer:* 9.9 Q1–Q2 for the method: causes, effects, two activities by students, two by the school.
36. **(B) What is immunity? Describe vaccines and the types of immunity.** *Why:* immunity was an OR in model 2079 and appears in MCQs. *Answer:* 9.9 Q3; vaccines contain weakened or killed pathogens or their antigens and give artificial active immunity (BCG, polio, DPT).
37. **(B) Family planning: methods of contraception with merits.** *Why:* "family planning" was an MCQ answer in 2079 and population control is in the syllabus. *Answer:* Model Paper II, Q21.
38. **(B) Describe the eye and accommodation, or vision defects.** *Why:* the eye was a short in 2079 and a long OR in 2081. *Answer:* Model Paper II, Q20.
39. **(B) Explain the functions of the liver, or the role of the pancreas, in digestion.** *Why:* digestion is a repeated long; the glands are its natural short. *Answer:* liver: bile, glycogen storage, urea, detoxification; pancreas: amylase, trypsin, lipase, bicarbonate, insulin and glucagon.
40. **(B) Explain the functions of the kidney, dialysis and kidney transplant.** *Why:* renal disorders were Q21 in 2079 and 2082. *Answer:* functions: excretion, osmoregulation, pH, blood pressure, erythropoietin; dialysis (haemodialysis) removes urea when kidneys fail; transplant replaces them; donor must match blood group and tissue type.
41. **(C) Write about apiculture, sericulture or vermicomposting: method and economic importance.** *Why:* Q19 OR has been poultry (2081) and fish (2082); the other applied-zoology topics are next. *Answer:* 9.10 Q3–Q5.
42. **(C) Explain the causes and effects of hormonal disorders: goitre, diabetes mellitus, gigantism.** *Why:* the endocrine unit is weighty and the 2081 pituitary short ended with "birth hormone". *Answer:* goitre: iodine deficiency, swollen thyroid; diabetes mellitus: insulin deficiency; gigantism: excess GH in childhood.

### MCQ hot-list (Group A)

| Topic likely to be tested | Why it is on the list | The fact to know |
|---|---|---|
| Meristem / permanent tissue / tissue functions | Botany MCQ 4 (model 2079, 2082 similar) | meristem divides; cambium gives secondary xylem and phloem |
| Osmosis, DPD, turgor, plasmolysis, stomata | 5 MCQs in 4 papers | DPD = OP − TP; turgid cell WP = 0 |
| Point mutation, frame shift, monosomy, trisomy, sickle cell | one every paper | monosomy 2n − 1; sickle cell is a point mutation |
| Sex-linked cross outcomes | 2080 | colour-blind woman × normal man → blind sons, carrier daughters |
| Double fertilisation, porogamy, parthenogenesis vs parthenocarpy | 4 MCQs in 4 papers | 3n endosperm; micropyle entry |
| Cartilage, adipose, phagocytes, muscle | one tissue MCQ every paper | cartilage avascular; neutrophils and monocytes phagocytose |
| Frog development sequence; gametogenesis steps | one every paper | morula → blastula → gastrula; spermiogenesis = spermatid → sperm |
| Heart-beat path, urine path, digestive enzymes order, brain lobes, hormones | 2–3 Human Biology MCQs every paper | SA → AV → His → Purkinje; pelvis → ureter → bladder → urethra |
| Transplants, family planning, immigration | 2079, 2082 | isograft = identical twins; immigration = entry |
| Bacterial vs viral vs fungal diseases | model 2079, 2082 | TB, typhoid, cholera are bacterial; candidiasis is fungal |

## Chapter summary

- **Grid:** Botany 37 = 5 + 16 + 16; Zoology 38 = 6 + 16 + 16; four ORs (one Botany short, Botany Q11, Zoology Q19, Zoology Q23). MCQs come after 30 minutes. Budget 2.4 minutes per mark and keep 15 minutes in hand.
- **Unit weights in four papers:** Anatomy, Tissues and Developmental Biology exactly 5 each every time; Physiology about 11, Genetics about 12, Biotechnology 4, Embryology 4–5; Human Biology 16–17, Applied Biology 8–9, Health 2–4.
- **Rotation of the long questions:** Botany Q10/Q11 = one Physiology + one Genetics (4 of 4); Zoology Q22 = a bacterial disease (4 of 4); Zoology Q23 = a labelled organ system (4 of 4).
- **Not yet asked as a long question:** Krebs cycle/ETS, C4, Mendel's laws, protein synthesis (Botany); malaria/AIDS/hepatitis, heart, neuron, endocrine glands, menstrual cycle, ear (Zoology).
- **Tag honesty:** year tags in this part record only what was read in the papers; predictions are built from frequency and gap, not from any leak.
