---
subject: Integrated Health Sciences I
grade: BSc Nursing Year 1
unit: 1
title: Cell, Tissues, Homeostasis and Body Chemistry
hours: 30
area: BSN 1 · Integrated Health Sciences I · Unit 1
---

Every disease a nurse treats begins as a failure inside cells, tissues or the fluid around them. This unit builds the base for the whole programme: how cells are organised, how substances cross the membrane, how the four primary tissues look under the microscope, how the body keeps its internal environment steady, and how the bicarbonate buffer holds blood pH at 7.40.

::: key What this unit gives you
- The cell, its organelles and membrane transport, with tonicity of IV fluids calculated for the bedside.
- Real micrographs of epithelium, cartilage and the three muscle types, labelled.
- Homeostasis and negative feedback, the resting membrane potential and cell-division arithmetic.
- The Henderson-Hasselbalch equation worked for normal and acidotic blood.
- Eight points on nursing care of a patient on IV fluids, and model answers with a full NANDA-I care plan.
:::

## 1.1 Levels of organisation and homeostasis

The body is built in levels: **chemical, cell, tissue, organ, organ system and organism**. Homeostasis is the maintenance of a relatively constant internal environment (temperature 37 °C, pH 7.35-7.45, glucose 4-6 mmol/L, plasma sodium 135-145 mmol/L). Most control is by **negative feedback**: a change is detected by a *receptor*, compared with a set point in a *control centre* (usually the brain), and corrected by an *effector* that reverses the change. **Positive feedback** amplifies a change until an end event, as in labour (oxytocin and uterine contractions rise together until the baby is born) and blood clotting.

```svgfig label="1.1" caption="Negative feedback loop, shown for body temperature. Heat raises the temperature, the hypothalamus detects it and sweating and skin vasodilation bring it back to 37 °C."
f = Fig(760, 266)
f.box(290, 12, 180, 46, "1 Stimulus\nTemperature rises above 37 °C", fill=ROSE, stroke=RED, size=11)
f.box(540, 100, 190, 54, "2 Receptor\nThermoreceptors in skin\nand hypothalamus", fill=BLUE, stroke=NAVY, size=10.5)
f.box(285, 100, 190, 54, "3 Control centre\nHypothalamus compares\nwith the set point", fill=SAND, stroke=AMBER, size=10.5)
f.box(30, 100, 190, 54, "4 Effector\nSweat glands work, skin\nvessels dilate", fill=MINT, stroke=TEAL, size=10.5)
f.box(285, 190, 190, 46, "5 Response\nHeat lost, temperature falls", fill=MINT, stroke=TEAL, size=11)
f.arrow([(470, 35), (635, 35), (635, 100)], color=RED, sw=2)
f.arrow([(540, 127), (475, 127)], color=NAVY, sw=2)
f.arrow([(285, 127), (220, 127)], color=AMBER, sw=2)
f.arrow([(125, 154), (125, 213), (285, 213)], color=TEAL, sw=2)
f.arrow([(475, 213), (690, 213), (690, 80), (690, 60)], color=TEAL, sw=2, dash=True)
f.text(745, 254, "dashed: negative feedback, the response switches the stimulus off", size=10.5, color=TEAL, bold=True, anchor="end")
```

## 1.2 The cell and its organelles

The cell is the structural and functional unit of life. A human cell has a **plasma membrane** (phospholipid bilayer with cholesterol and proteins), **cytoplasm**, and organelles: the **nucleus** (DNA, 46 chromosomes), **rough endoplasmic reticulum** (ribosomes make protein), **smooth ER** (lipids, detoxification), **Golgi apparatus** (packs and exports), **mitochondria** (ATP by oxidative phosphorylation), **lysosomes** (digestive enzymes) and the **cytoskeleton**. Cells with a heavy energy demand, such as heart muscle, are packed with mitochondria.

```svgfig label="1.2" caption="A typical animal cell with its main organelles, drawn in section."
f = Fig(760, 340)
f.circle(380, 160, 150, fill="#fff7ed", stroke=AMBER, sw=3)
f.circle(350, 150, 52, fill="#dbeafe", stroke=NAVY, sw=2)
f.circle(350, 150, 14, fill=NAVY, stroke=NAVY)
f.box(430, 90, 70, 22, "", fill="#bbf7d0", stroke=TEAL, r=11); f.box(445, 120, 60, 20, "", fill="#bbf7d0", stroke=TEAL, r=10)
f.poly([(290, 220), (350, 215), (360, 232), (292, 240)], fill="#fde68a", stroke=AMBER)
f.poly([(300, 250), (360, 245), (368, 262), (302, 268)], fill="#fde68a", stroke=AMBER)
f.circle(440, 215, 12, fill="#fecaca", stroke=RED); f.circle(262, 108, 10, fill="#e9d5ff", stroke="#6b21a8")
for pts in [(452, 160), (470, 190), (300, 80)]: f.circle(pts[0], pts[1], 3, fill=NAVY, stroke=NAVY)
L = [("Nucleus with nucleolus", 350, 150, 190, 60, "l"), ("Mitochondrion", 465, 100, 580, 60, "r"),
     ("Golgi apparatus", 300, 232, 190, 300, "l"), ("Lysosome", 440, 215, 580, 270, "r"), ("Vesicle", 262, 108, 190, 20, "l"), ("Ribosomes", 470, 190, 580, 190, "r")]
for n, x, y, tx, ty, s in L:
    f.arrow([(tx + (-6 if s == "r" else 6), ty), (x + (16 if s == "r" else -22), y)], color=SLATE, sw=1)
    f.text(tx, ty, n, size=11.5, color=NAVY, bold=True, anchor="start" if s == "r" else "end")
f.text(380, 330, "The thick outer ring is the plasma membrane (phospholipid bilayer)", size=11, color=AMBER, bold=True)
```

### Membrane transport

- **Simple diffusion:** movement down a concentration gradient (O₂, CO₂). **Facilitated diffusion:** carrier proteins, still downhill (glucose through GLUT).
- **Osmosis:** water moves across a semipermeable membrane from low to high solute concentration.
- **Active transport:** energy (ATP) moves solute uphill; the **Na⁺/K⁺-ATPase** pumps 3 Na⁺ out and 2 K⁺ in and uses a third of the cell's energy.
- **Endocytosis and exocytosis:** bulk transport in vesicles (phagocytosis of bacteria by neutrophils).

**Tonicity of IV fluids.** Osmolarity is the number of particles per litre. Normal saline is 0.9% NaCl: 9 g/L ÷ 58.44 g/mol = **154 mmol/L**, and since NaCl gives two particles, **308 mOsm/L**, close to plasma (about 290). A 5% dextrose bag holds 50 g/L ÷ 180.16 = **278 mOsm/L** in the bag, but the glucose is metabolised and the water that remains is hypotonic. Red cells in isotonic fluid stay normal, in hypertonic fluid shrink (crenation) and in hypotonic fluid swell and burst (haemolysis).

```svgfig label="1.3" caption="Red cell in three fluids. Isotonic saline (0.9%) keeps the shape, hypertonic fluid draws water out and the cell shrinks, hypotonic fluid lets water in and the cell swells."
f = Fig(760, 220)
for cx, name, col, r, lab in [(130, "Hypertonic (3% NaCl)", AMBER, 34, "Crenated, shrunk"), (380, "Isotonic (0.9% NaCl)", TEAL, 48, "Normal biconcave disc"), (630, "Hypotonic (0.45% NaCl)", RED, 62, "Swollen, may lyse")]:
    f.box(cx - 105, 8, 210, 160, "", fill="#f8fafc", stroke="#cbd5e1", r=10)
    f.circle(cx, 88, r, fill="#fecaca", stroke=col, sw=3)
    f.circle(cx, 88, max(r - 28, 6), fill="#fee2e2", stroke="#fca5a5", sw=1) if r < 60 else None
    f.text(cx, 190, name, size=12, color=col, bold=True); f.text(cx, 208, lab, size=11, color=SLATE)
f.arrow([(235, 88), (190, 88)], color=AMBER, sw=2)
f.arrow([(525, 88), (570, 88)], color=RED, sw=2)
```

## 1.3 Membrane potential and cell division

At rest the inside of a nerve or muscle cell is negative. Potassium leaks out through open channels until the electrical pull back balances the concentration pull out. The **Nernst equation** at 37 °C is E = 61.5 × log₁₀([K⁺]out ÷ [K⁺]in). With K⁺ 5 mmol/L outside and 150 inside: 61.5 × log(5/150) = **-90.8 mV**, close to the real resting potential (−70 to −90 mV). A raised plasma potassium (hyperkalaemia) makes the cell less negative, so heart muscle becomes irritable, which is why potassium is never pushed rapidly by IV bolus.

Somatic cells divide by **mitosis** (prophase, metaphase, anaphase, telophase) into two identical diploid cells, so after n divisions one cell becomes 2ⁿ: **32** cells after 5 divisions and **1024** after 10. Gametes form by **meiosis**, which halves the chromosomes from 46 to 23. Uncontrolled mitosis is cancer.

## 1.4 The four primary tissues under the microscope

Tissues are groups of similar cells with a common function: **epithelial** (covering and lining), **connective** (support and binding, includes blood, bone, cartilage and fat), **muscle** (contraction) and **nervous** (conduction).

```photogrid label="1.4" cols="2" ratio="1.25" caption="Epithelium. (a) Real H&E micrograph of simple columnar epithelium lining a gland; nuclei sit at the base of tall cells. (b) The three shapes of epithelial cell and where each is found."
@ photo id="nur1/columnar" cap="Simple columnar epithelium (H&E)"
fit 1.25
focus 0.55 0.2
mark 0.50 0.82 "1"
mark 0.30 0.30 "2"
key 1 (a) Tall columnar cells in a single layer; surface at the top
key 2 (a) Connective tissue (lamina propria) beneath the lining
@ svg cap="Epithelial cell shapes"
f = Fig(330, 270)
f.box(10, 20, 100, 8, "", fill="#fbcfe8", stroke=RED, r=2); f.box(120, 14, 24, 26, "", fill="#fbcfe8", stroke=RED, r=2); f.box(150, 14, 24, 26, "", fill="#fbcfe8", stroke=RED, r=2)
f.text(60, 52, "Squamous", size=11, color=NAVY, bold=True); f.text(60, 66, "lung alveoli, vessels", size=10, color=SLATE)
for i in range(4): f.box(10 + i * 40, 110, 36, 36, "", fill="#bfdbfe", stroke=NAVY, r=3); f.circle(28 + i * 40, 128, 6, fill=NAVY, stroke=NAVY)
f.text(90, 168, "Cuboidal: kidney tubule, glands", size=11, color=NAVY, bold=True)
for i in range(6): f.box(10 + i * 26, 190, 22, 52, "", fill="#bbf7d0", stroke=TEAL, r=3); f.circle(21 + i * 26, 230, 5, fill=TEAL, stroke=TEAL)
f.text(90, 262, "Columnar: gut, uterus", size=11, color=TEAL, bold=True)
```

```photogrid label="1.5" cols="3" ratio="1.0" caption="The three muscle types. (a) Skeletal muscle: long unbranched cross-striated fibres. (b) Cardiac muscle: branched, striated, one central nucleus. (c) Smooth muscle: spindle cells, no striations. Only skeletal is voluntary."
@ photo id="nur1/skeletal" cap="Skeletal muscle"
fit 1.0
focus 0.5 0.5
mark 0.30 0.55 "1"
key 1 (a) Fine cross-striations (A and I bands) along each fibre
@ photo id="nur1/cardiac" cap="Cardiac muscle"
fit 1.0
focus 0.5 0.5
mark 0.45 0.60 "1"
key 1 (b) Central dark nuclei in branching striated fibres
@ photo id="nur1/smooth" cap="Smooth muscle"
fit 1.0
focus 0.5 0.5
mark 0.50 0.50 "1"
key 1 (c) Spindle cells with small cigar-shaped nuclei
```

```photogrid label="1.6" cols="2" ratio="1.1" caption="Connective tissue. (a) Hyaline cartilage under the microscope: chondrocytes sit in lacunae within a glassy matrix. It covers joint surfaces, and forms the nasal septum and tracheal rings. (b) Plan of the tissue families."
@ photo id="nur1/cartilage" cap="Hyaline cartilage"
fit 1.1
focus 0.5 0.5
mark 0.50 0.55 "1"
key 1 (a) Chondrocytes in lacunae within the matrix
@ svg cap="Connective tissue family"
f = Fig(330, 260)
f.box(95, 8, 140, 34, "Connective tissue", fill=BLUE, stroke=NAVY, bold=True, size=11)
f.line(165, 42, 165, 70, color=SLATE, sw=1.4)
f.box(4, 70, 322, 180, "", fill=SOFT, stroke="#cbd5e1", r=10)
for i, (t_, c) in enumerate([("Loose\n(areolar)", TEAL), ("Dense\n(tendon)", TEAL), ("Cartilage\n(hyaline)", AMBER), ("Bone", AMBER), ("Blood", RED), ("Adipose", SLATE)]):
    x = 14 + (i % 3) * 104; y = 86 + (i // 3) * 80
    f.box(x, y, 94, 62, t_, fill="#ffffff", stroke=c, size=10.5, color=c, bold=True)
```

## 1.5 Body fluids, pH and the bicarbonate buffer

Water forms about 60% of adult body weight: two-thirds **intracellular** and one-third **extracellular** (plasma and interstitial fluid). Blood pH is held at 7.35-7.45 by buffers, the lungs (CO₂) and the kidneys (H⁺ and HCO₃⁻). The main extracellular buffer is bicarbonate: CO₂ + H₂O ⇌ H₂CO₃ ⇌ H⁺ + HCO₃⁻. The **Henderson-Hasselbalch equation** is pH = 6.1 + log₁₀ [HCO₃⁻ ÷ (0.03 × PaCO₂)].

- **Normal:** HCO₃⁻ 24 mmol/L and PaCO₂ 40 mmHg give a ratio of 24 ÷ 1.2 = **20.0** to 1, so pH = 6.1 + log 20 = **7.40**.
- **Metabolic acidosis (diarrhoea, DKA):** HCO₃⁻ falls to 12 and the lungs blow off CO₂ to 25 mmHg: 12 ÷ 0.75 = 16, pH = **7.30**. The deep fast breathing (Kussmaul) is compensation.
- Dilution check: to make 500 mL of 0.9% saline from a 10% stock, take 500 × 0.9 ÷ 10 = **45 mL** of stock and add water to 500 mL (C₁V₁ = C₂V₂).

```svgfig label="1.4" caption="Acid-base balance: the bicarbonate buffer equation and its two controllers. The lungs adjust CO₂ in minutes, the kidneys adjust HCO₃⁻ in days."
f = Fig(760, 210)
f.box(30, 20, 130, 50, "CO₂ + H₂O\n(from metabolism)", fill=SAND, stroke=AMBER, size=11)
f.box(220, 20, 110, 50, "H₂CO₃\ncarbonic acid", fill=BLUE, stroke=NAVY, size=11)
f.box(390, 20, 150, 50, "H⁺ + HCO₃⁻\nacid + base", fill=ROSE, stroke=RED, size=11)
f.arrow([(160, 45), (220, 45)], color=SLATE, sw=2, both=True); f.arrow([(330, 45), (390, 45)], color=SLATE, sw=2, both=True)
f.box(30, 130, 250, 56, "Lungs: breathing rate and depth\nchange PaCO₂ in minutes", fill=MINT, stroke=TEAL, size=11)
f.box(420, 130, 300, 56, "Kidneys: excrete H⁺, regenerate HCO₃⁻\ntake hours to days", fill=MINT, stroke=TEAL, size=11)
f.arrow([(95, 130), (95, 70)], color=TEAL, sw=2); f.arrow([(560, 130), (500, 70)], color=TEAL, sw=2)
f.box(580, 20, 150, 50, "pH = 6.1 + log\nHCO₃⁻ ÷ 0.03 PaCO₂", fill=SOFT, stroke=NAVY, size=10.5, bold=True)
```

```python
import math
nacl = 9 / 58.44 * 1000 * 2
dex = 50 / 180.16 * 1000
ph = 6.1 + math.log10(24 / (0.03 * 40))
e_k = 61.5 * math.log10(5 / 150)
print("NaCl mOsm/L", round(nacl))
print("Dextrose mOsm/L", round(dex))
print("pH", f"{ph:.2f}")
print("E_K mV", round(e_k, 1))
```

```text
NaCl mOsm/L 308
Dextrose mOsm/L 278
pH 7.40
E_K mV -90.8
```

## 1.6 Nursing care of a patient on IV fluids: eight points

1. **Check the right fluid.** Read the label against the order for name, strength, volume and expiry. Isotonic saline and Ringer's lactate expand the circulation, while 5% dextrose is mostly free water. Giving the wrong class of fluid can shift water into or out of cells.
2. **Calculate and set the rate.** Work out drops per minute from volume, time and the set's drop factor, and recheck after every position change. A rate that is too fast overloads the heart, and one too slow delays correction. Never "catch up" a lost volume without an order.
3. **Inspect the cannula site.** Look for redness, swelling, pain and a palpable cord at each shift. These are early signs of phlebitis or infiltration. Resite at once and record the visual infusion phlebitis score.
4. **Watch for fluid overload.** Crackles, rising respiratory rate, raised JVP, oedema and weight gain after infusion mean the circulation is overfilled. Raise the head of the bed, slow the drip and call the doctor. Elderly and cardiac patients are most at risk.
5. **Watch for dehydration signals.** Dry mucosa, thirst, falling urine below 0.5 mL/kg/h, tachycardia and a falling BP show the fluid is not enough. Record input and output every shift. Weigh daily when the stay is long.
6. **Monitor electrolytes.** Check ordered sodium and potassium results and report abnormal values. Hypotonic fluid can lower sodium and cause confusion, while potassium given too fast can stop the heart. Never add potassium to a running bag without an order and a label.
7. **Keep it sterile.** Wash hands, clean the port with 70% alcohol and label the bag and the set with date and time. Change sets as per hospital policy (usually 72-96 hours). This prevents bloodstream infection.
8. **Teach and document.** Tell the patient not to adjust the clamp, to keep the arm free and to call for pain or swelling. Record the type, volume, rate, site and response, and sign. A missing entry means the care was not done in the eyes of the law and the Nepal Nursing Council.

## Formula and fact sheet

- Normal saline 0.9% = 9 g/L = 154 mmol/L = 308 mOsm/L; 5% dextrose = 50 g/L = 278 mOsm/L before metabolism.
- Nernst (37 °C): E = 61.5 × log([ion]out ÷ [ion]in); for K⁺ 5/150 it is -90.8 mV.
- Cells after n divisions = 2ⁿ. pH = 6.1 + log [HCO₃⁻ ÷ (0.03 × PaCO₂)]; normal ratio 20 : 1 gives 7.40.
- C₁V₁ = C₂V₂. Total body water about 60% of body weight, two-thirds intracellular.

## Chapter summary

- Homeostasis works by negative feedback: receptor, control centre, effector, response.
- Membrane transport is passive (diffusion, osmosis) or active (Na⁺/K⁺ pump, vesicles); tonicity decides whether a cell swells or shrinks.
- The four tissues have recognisable microscopic patterns: lined cells, matrix with cells, striated or smooth fibres, neurons.
- Blood pH 7.35-7.45 depends on a 20 : 1 bicarbonate to carbonic acid ratio, controlled by lungs and kidneys.
- Safe IV fluid care is the right fluid, the right rate, a watched site and watched electrolytes.

## Practice

**MCQs (with reasons)**

1. Which tissue is seen as branched cells with central nuclei and cross-striations? (a) skeletal muscle (b) cardiac muscle (c) smooth muscle (d) simple columnar epithelium.
2. A red cell placed in 0.45% NaCl will: (a) shrink (b) stay unchanged (c) swell and may burst (d) divide.
3. The Na⁺/K⁺-ATPase moves: (a) 2 Na⁺ in and 3 K⁺ out (b) 3 Na⁺ out and 2 K⁺ in (c) 3 Na⁺ in and 2 K⁺ out (d) water only.
4. With HCO₃⁻ 24 mmol/L and PaCO₂ 40 mmHg, the pH is: (a) 7.20 (b) 7.30 (c) 7.40 (d) 7.60.
5. After 5 successive mitotic divisions one cell gives: (a) 10 cells (b) 16 cells (c) 25 cells (d) 32 cells.

::: note Answers and rationales
**1. (b).** Cardiac fibres branch and have one central nucleus; skeletal fibres are unbranched with peripheral nuclei, and smooth muscle shows no striations.
**2. (c).** 0.45% saline is hypotonic, so water enters the cell by osmosis. Shrinking (a) occurs in hypertonic fluid.
**3. (b).** The pump uses ATP to remove 3 Na⁺ and bring in 2 K⁺, keeping the inside negative. The other options reverse the direction.
**4. (c).** pH = 6.1 + log 20 = 7.40. Values of 7.20 or 7.30 are acidotic.
**5. (d).** Divisions double the number each time, 2⁵ = 32. Option (c) wrongly squares 5.
:::

**Short answer (3 marks): Differentiate isotonic, hypotonic and hypertonic solutions with an example each.** An isotonic solution has the same osmolarity as plasma (about 290 mOsm/L), for example 0.9% NaCl at 308 mOsm/L, and causes no net water shift. A hypotonic solution has lower osmolarity (0.45% NaCl) and water moves into cells, which swell. A hypertonic solution has higher osmolarity (3% NaCl) and water leaves cells, which shrink. The choice of IV fluid depends on whether the patient needs volume or cell hydration.

**Medium answer (5 marks): Describe the cell membrane and the modes of transport across it (Figure 1.2).** The plasma membrane is a fluid mosaic of a phospholipid bilayer, cholesterol that gives stability, and proteins that act as channels, carriers, receptors and enzymes. It is selectively permeable. *Passive transport* needs no energy and includes simple diffusion (O₂, CO₂, lipid-soluble drugs), facilitated diffusion by carriers (glucose, GLUT4 under insulin) and osmosis of water through aquaporins. *Active transport* uses ATP to move solutes uphill, as in the Na⁺/K⁺-ATPase, which pumps 3 Na⁺ out and 2 K⁺ in and sets the resting potential, and secondary active transport such as the Na⁺-glucose co-transporter used in ORS. *Vesicular transport* moves large particles by endocytosis, phagocytosis and exocytosis. Clinical link: ORS works because glucose carries sodium and water across the gut wall even in diarrhoea.

**Long answer (10 marks): Mrs Sita Karki, 45, is admitted to the medical ward of a district hospital with 3 days of watery diarrhoea. She is drowsy and breathing deeply. Pulse 112/min, BP 90/60 mmHg, RR 28/min, dry tongue, skin pinch goes back slowly. ABG: pH 7.30, HCO₃⁻ 12 mmol/L, PaCO₂ 25 mmHg. Discuss the physiology and the nursing care with a care plan.**

*Introduction and physiology.* Diarrhoea loses water, sodium and bicarbonate-rich intestinal fluid. The Henderson-Hasselbalch equation confirms the ABG: pH = 6.1 + log [12 ÷ (0.03 × 25)] = 6.1 + log 16 = **7.30**, a metabolic acidosis with respiratory compensation (low PaCO₂ and Kussmaul breathing). Her MAP is (90 + 120) ÷ 3 = 70 mmHg, near the lower safe limit, and the fall in extracellular volume explains the tachycardia, dry mucosa and slow skin pinch. Priorities are volume restoration, correction of acidosis by treating the cause, safety and monitoring. Fluid is given as ordered (Ringer's lactate or normal saline); ORS is added as soon as she can drink, since glucose-linked sodium absorption continues in diarrhoea. Zinc is given as per the Nepal diarrhoea protocol.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "I am very thirsty and weak." **O:** 3 days of watery stool, P 112, BP 90/60, dry tongue, slow skin pinch, urine scanty. | **Deficient fluid volume** related to excessive stool loss, as evidenced by tachycardia, hypotension and dry mucous membranes. | **Fluid balance:** BP at least 100/60, pulse below 100, urine at least 0.5 mL/kg/h within 12 h. | 1. Start IV fluid as ordered and check the rate hourly; *restores circulating volume.* 2. Strict input-output chart; *detects balance and renal perfusion.* 3. Give ORS 200 mL after each loose stool once alert; *replaces losses by the gut route.* 4. Daily weight; *tracks fluid change.* | Vitals every 2 h, urine hourly; goal met when BP and urine reach target. |
| **O:** pH 7.30, HCO₃⁻ 12, RR 28 and deep, drowsy. | **Risk for electrolyte imbalance** related to diarrhoea and acidosis (potassium loss). | **Electrolyte balance:** K⁺ 3.5-5.0 mmol/L and pH above 7.35 within 24 h. | 1. Send ordered electrolytes and repeat ABG; *guides therapy.* 2. Monitor ECG and muscle weakness; *low potassium causes arrhythmia.* 3. Give potassium only diluted and slow; *rapid potassium stops the heart.* | Repeat ABG and K⁺ reviewed; breathing slows toward 16-20/min. |
| **O:** drowsy, perianal skin sore, soiled linen. | **Risk for infection** and **impaired skin integrity** related to faecal contamination. | **Skin integrity:** intact perianal skin; no spread of infection in 7 days. | 1. Hand hygiene and contact precautions; *oral-faecal spread.* 2. Barrier cream, change soiled linen; *protects skin.* 3. Teach handwashing and safe water; *prevents recurrence.* | Skin inspected each shift; family demonstrates handwashing. |

Health education: boil or filter drinking water, wash hands with soap after toilet, use ORS and zinc for every child or adult with diarrhoea, and return to hospital for blood in stool, persistent vomiting or drowsiness.

::: tip Exam tip
Whenever an ABG is given, write the equation, substitute the numbers and name both the primary disorder and the compensation. A pH value alone earns only half the marks.
:::
