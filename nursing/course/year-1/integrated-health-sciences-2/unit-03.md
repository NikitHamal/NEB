---
subject: Integrated Health Sciences II
grade: BSc Nursing Year 1
unit: 3
title: Renal System, Fluids, Electrolytes and Acid-Base
hours: 30
area: BSN 2-3 · Integrated Health Sciences II · Unit 3
---

The two kidneys filter about 180 litres of plasma a day and turn it into 1.5 litres of urine, while keeping water, sodium, potassium and pH steady. The nurse measures this work every shift as input-output, daily weight and creatinine, and runs IV fluids that must match it. This unit covers the nephron, urine formation and GFR, hormonal control of water and sodium, body fluid compartments, the main electrolyte disorders, acid-base interpretation and kidney failure care, including the dialysis services at the National Kidney Centre and TUTH.

::: key What this unit gives you
- A real kidney micrograph with a nephron schematic, and a three-up strip with the juxtaglomerular figure, a urine dipstick photograph and a fluid-compartment diagram.
- GFR (Cockcroft-Gault), filtration and reabsorption, body water, maintenance fluid (4-2-1 rule) and urine output targets, worked step by step.
- ADH, aldosterone and the RAAS as a control diagram; an electrolyte and an acid-base table with Winter's formula.
- Eight points on protecting the kidney, and model answers with a care plan for chronic kidney disease with hyperkalaemia.
:::

## 3.1 The nephron and urine formation

Each kidney has about one million **nephrons**. A nephron has a **renal corpuscle** (glomerulus, a tuft of capillaries, inside Bowman's capsule) and a tubule: **proximal convoluted tubule (PCT)**, **loop of Henle**, **distal convoluted tubule (DCT)** and the **collecting duct**. Urine forms in three steps: **filtration** in the glomerulus (water and small solutes, no cells or large protein), **reabsorption** along the tubule (the PCT takes back about 65% of water and sodium, all glucose and amino acids), and **secretion** of hydrogen, potassium and drugs. The normal glomerular filtration rate (GFR) is **125 mL/min**, which is 180 L a day; with 1.5 L of urine passed, **99.2%** of the filtrate is reabsorbed.

```photogrid label="3.1" cols="2" ratio="1.3" caption="The kidney at the microscope. (a) A real kidney section stained for CD10 (brown marks the proximal tubule brush border): round glomeruli sit among brown tubules. (b) The path of filtrate through the nephron with the main job of each segment."
@ photo id="nur2/kidney" cap="Kidney cortex, CD10 stain"
fit 1.3
focus 0.5 0.5
mark 0.30 0.65 "1"
mark 0.58 0.52 "2"
key 1 (a) Glomerulus: a round, pale tuft of capillaries (filtration)
key 2 (a) Brown proximal tubules: most reabsorption of water, sodium and glucose
@ svg cap="Nephron segments"
f = Fig(380, 300)
st = [("Glomerulus: filters 125 mL/min", BLUE, NAVY), ("PCT: 65% of Na⁺ and water, all glucose", MINT, TEAL), ("Loop of Henle: makes the salty medulla", SAND, AMBER), ("DCT: fine-tunes Na⁺, K⁺, Ca²⁺ (aldosterone)", MINT, TEAL), ("Collecting duct: water by ADH", BLUE, NAVY)]
for i, (t_, fc, sc) in enumerate(st):
    y = 8 + i * 58; f.box(10, y, 360, 40, t_, fill=fc, stroke=sc, size=10.5, bold=True)
    if i < 4: f.arrow([(190, y + 40), (190, y + 58)], color=SLATE, sw=2)
```

## 3.2 GFR, clearance and the hormones that control water and sodium

**Creatinine clearance** estimates the GFR in the ward. By the **Cockcroft-Gault** formula, CrCl = (140 − age) × weight (kg) ÷ (72 × serum creatinine in mg/dL), multiplied by 0.85 for women. A 60-year-old man of 70 kg with creatinine 1.4 mg/dL has a CrCl of **55.6 mL/min**; a 55-year-old woman of 55 kg with creatinine 1.1 has **50.2 mL/min** and a drug dose may need to be reduced. The general clearance formula is C = U × V ÷ P: with urine creatinine 120 mg/dL, urine flow 1 mL/min and plasma creatinine 1.0 mg/dL, the clearance is **120 mL/min**. CKD is staged by GFR: stage 3 is 30-59, stage 4 is 15-29 and stage 5 is below 15 mL/min.

Three hormones fine-tune the output. **ADH** (from the posterior pituitary) opens water channels in the collecting duct, so water is kept and urine is concentrated; it is released when plasma osmolality rises or blood volume falls. **Aldosterone** (adrenal cortex, driven by the RAAS) makes the DCT keep sodium and lose potassium. **Atrial natriuretic peptide** from the stretched atria does the reverse and causes sodium loss. Loop diuretics such as **furosemide** block sodium and chloride reabsorption in the loop of Henle, so urine volume rises.

```svgfig label="3.2" caption="Control of water and sodium. A fall in volume or a rise in osmolality triggers ADH and the RAAS; both act on the kidney to keep water and salt and return the volume to normal."
f = Fig(760, 210)
f.box(10, 70, 150, 56, "Low blood volume\nor high osmolality", fill=ROSE, stroke=RED, size=11, bold=True)
f.box(220, 20, 160, 50, "Posterior pituitary\nreleases ADH", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(220, 130, 160, 50, "Kidney: renin →\nangiotensin II →\naldosterone", fill=SAND, stroke=AMBER, size=10, bold=True)
f.box(440, 20, 150, 50, "Collecting duct\nkeeps water", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(440, 130, 150, 50, "DCT keeps Na⁺,\nwater follows", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(630, 70, 120, 56, "Volume and\nBP restored", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.arrow([(160, 90), (220, 45)], color=SLATE, sw=2); f.arrow([(160, 110), (220, 155)], color=SLATE, sw=2)
f.arrow([(380, 45), (440, 45)], color=SLATE, sw=2); f.arrow([(380, 155), (440, 155)], color=SLATE, sw=2)
f.arrow([(590, 45), (630, 85)], color=TEAL, sw=2); f.arrow([(590, 155), (630, 112)], color=TEAL, sw=2)
f.text(380, 198, "Diuretics, ACE inhibitors and spironolactone act on these steps", size=10.5, color=RED, bold=True)
```

## 3.3 Body fluids and electrolytes

Total body water (TBW) is 60% of body weight in an adult man. For a 60 kg person TBW is **36 L**: two-thirds is **intracellular fluid (ICF)**, 24 L, and one-third is **extracellular fluid (ECF)**, 12 L, which divides into **interstitial fluid** (9 L) and **plasma** (3 L). Babies are 75-80% water and the elderly about 50%, so infants dehydrate rapidly in diarrhoea. The main ECF cation is sodium and the main ICF cation is potassium, kept apart by the Na⁺/K⁺ pump.

```photogrid label="3.2" cols="3" ratio="0.95" caption="Reading the kidney's output. (a) The OpenStax figure of the juxtaglomerular apparatus: drawing and micrograph of the corpuscle. (b) A urine dipstick being read in a laboratory (the colour pads change with glucose, protein, blood, ketones and pH). (c) The fluid compartments of a 60 kg adult."
@ photo id="nur2/jga" cap="Juxtaglomerular apparatus"
fit 0.95
focus 0.35 0.5
mark 0.14 0.70 "1"
mark 0.82 0.60 "2"
key 1 (a) Macula densa and juxtaglomerular cells: they sense salt and release renin
key 2 (a) Glomerulus in the micrograph, with the proximal tubule beside it
@ photo id="nur2/urine" cap="Urine dipstick reading"
fit 0.95
focus 0.5 0.5
mark 0.62 0.72 "3"
mark 0.30 0.22 "4"
key 3 (b) The strip is dipped for 1-2 seconds and read at the stated time against the colour chart
key 4 (b) Gloves and a clean cup: a midstream specimen is tested within 1 hour
@ svg cap="Fluid compartments (60 kg)"
f = Fig(300, 300)
f.box(10, 10, 280, 50, "Total body water 36 L (60%)", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(10, 90, 150, 110, "ICF 24 L\n(two-thirds)\nK⁺, Mg²⁺,\nprotein, phosphate", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(170, 90, 120, 50, "Interstitial 9 L", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(170, 150, 120, 50, "Plasma 3 L", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.text(230, 80, "ECF 12 L: Na⁺, Cl⁻, HCO₃⁻", size=10, color=AMBER, bold=True)
f.text(150, 230, "Oedema: fluid shifts to the interstitium.", size=10, color=SLATE, bold=True)
f.text(150, 250, "Shock: plasma volume falls.", size=10, color=SLATE, bold=True)
f.arrow([(60, 60), (60, 90)], color=SLATE, sw=2); f.arrow([(230, 60), (230, 90)], color=SLATE, sw=2)
```

**Maintenance fluid** uses the **4-2-1 rule**: 4 mL/kg/h for the first 10 kg, 2 mL/kg/h for the next 10 kg, 1 mL/kg/h thereafter. An 18-kg child needs 4 × 10 + 2 × 8 = **56 mL/h**, and a 70-kg adult needs 40 + 20 + 50 = **110 mL/h**. The minimum acceptable urine output is **0.5 mL/kg/h**, so 35 mL/h for the 70-kg adult.

```python
age, wt, scr = 60, 70, 1.4
crcl = (140 - age) * wt / (72 * scr)
litres = 125 * 1440 / 1000
reab = (1 - 1.5 / litres) * 100
tbw = 0.6 * 60
child = 4 * 10 + 2 * 8
print(f"CrCl = {crcl:.1f} mL/min")
print(f"Filtrate = {litres:.1f} L/day; reabsorbed = {reab:.1f}%")
print(f"TBW {tbw:.1f} L: ICF {tbw * 2 / 3:.1f}, ECF {tbw / 3:.1f} (interstitial {tbw / 4:.1f}, plasma {tbw / 12:.1f})")
print(f"Maintenance 18 kg child = {child} mL/h")
```

```text
CrCl = 55.6 mL/min
Filtrate = 180.0 L/day; reabsorbed = 99.2%
TBW 36.0 L: ICF 24.0, ECF 12.0 (interstitial 9.0, plasma 3.0)
Maintenance 18 kg child = 56 mL/h
```

| Electrolyte | Normal (mmol/L) | Causes of abnormality | Main signs | Key nursing action |
|---|---|---|---|---|
| Sodium | 135-145 | Low: diuretics, SIADH, over-hydration. High: dehydration, diabetes insipidus | Low: confusion, seizures. High: thirst, irritability | Correct slowly, not more than 8-10 mmol/L in 24 h |
| Potassium | 3.5-5.0 | Low: vomiting, diarrhoea, furosemide. High: kidney failure, ACE inhibitors | Low: weakness, U waves. High: peaked T, wide QRS, arrest | Monitor ECG; never give IV potassium undiluted or fast |
| Calcium | 2.2-2.6 | Low: thyroidectomy, vitamin D lack. High: hyperparathyroidism | Low: tingling, tetany. High: stones, bone pain, constipation | Calcium gluconate for tetany; hydrate for high calcium |
| Magnesium | 0.7-1.0 | Low: alcohol, diuretics | Tremor, arrhythmia, seizures | Replace before potassium will correct |

## 3.4 Acid-base balance

Blood pH is held at 7.35-7.45 by buffers (bicarbonate), the lungs (change CO₂ in minutes) and the kidneys (change H⁺ and bicarbonate in days). Read an ABG in three steps: **pH** (acidosis or alkalosis), then **PaCO₂** (respiratory cause, normal 35-45) and **HCO₃** (metabolic cause, normal 22-26), then **compensation**. A patient with pH 7.28, PaCO₂ 30 and HCO₃ 14 has a **metabolic acidosis**; **Winter's formula** gives the expected PaCO₂ as 1.5 × 14 + 8 = **29 mmHg** (± 2), so the lungs are compensating correctly. If the measured CO₂ were 45, a second respiratory acidosis would be present.

| ABG pattern | pH | PaCO₂ | HCO₃ | Common cause |
|---|---|---|---|---|
| Respiratory acidosis | below 7.35 | above 45 | normal or high | COPD, opioids, sedation |
| Respiratory alkalosis | above 7.45 | below 35 | normal or low | Fever, panic, pain |
| Metabolic acidosis | below 7.35 | low | below 22 | DKA, renal failure, diarrhoea |
| Metabolic alkalosis | above 7.45 | high | above 26 | Vomiting, nasogastric loss |

## 3.5 Protecting the kidneys: health education in eight points

Chronic kidney disease (CKD) is silent until 70-80% of function is lost, and dialysis is costly for Nepali families even where the government supports it at the National Kidney Centre, TUTH, Bir and provincial hospitals. Prevention in the community by the nurse is the better answer.

1. **Control blood pressure.** High pressure damages the filtering capillaries and is the second cause of CKD. Keep BP below 130/80 mmHg for those with kidney disease and take the tablets daily. ACE inhibitors such as enalapril protect the kidney, but potassium and creatinine need a check after starting.
2. **Control blood sugar.** Diabetes is the commonest cause of kidney failure. Keep HbA1c near 7% and test the urine for albumin every year. Early treatment slows the damage.
3. **Drink enough water but not too much.** Drink 2-3 litres a day in hot weather and for field work unless a doctor restricts fluid. Pale yellow urine is a good guide. Dehydration lowers kidney blood flow and encourages stones.
4. **Avoid harmful medicines.** Painkillers such as diclofenac and ibuprofen, some herbal and Ayurvedic mixtures, and unchecked antibiotics injure the kidney tubules. Use them only when prescribed and for the shortest time. Pharmacy sales of strong painkillers without a prescription should be refused.
5. **Reduce salt.** Under 5 g a day lowers BP and oedema. Avoid pickles, instant noodles and dried fish. Check food labels for sodium.
6. **Treat infections early.** Burning urine, frequency and fever mean urinary tract infection, which can spread to the kidney. Women should wipe front to back and not delay passing urine. Complete the antibiotic course and report flank pain.
7. **Keep healthy habits.** Stop smoking, limit alcohol, keep BMI below 23 and exercise on most days. Obesity and tobacco raise the risk of CKD. Screen those with diabetes, hypertension, a family history or age above 60 every year with creatinine, eGFR and urine albumin.
8. **Follow the kidney diet if disease is present.** Limit fluid to urine output plus 500 mL, restrict potassium (banana, potato, oranges, coconut water), phosphate (milk, colas, nuts) and salt, and take enough but not extra protein. Protect the arm with the dialysis fistula: no BP, blood tests or tight clothing on it, and feel for the thrill daily.

## Formula and fact sheet

- CrCl = (140 − age) × weight ÷ (72 × creatinine) (× 0.85 for women): 55.6 mL/min in the example. GFR 125 mL/min = 180 L/day.
- TBW = 60% of weight (36 L at 60 kg): ICF 24 L, ECF 12 L, plasma 3 L. Maintenance by 4-2-1: 110 mL/h at 70 kg.
- Minimum urine output 0.5 mL/kg/h (35 mL/h at 70 kg). Winter's expected PaCO₂ = 1.5 × HCO₃ + 8.
- Free-water deficit in hypernatraemia = 0.6 × weight × (Na ÷ 140 − 1): for Na 160 and 60 kg it is **5.1 L**, corrected over 48 h.
- 3% saline holds 513 mmol/L: to raise sodium by 8 mmol/L in a 60-kg patient needs 0.6 × 60 × 8 = 288 mmol, about **561 mL**, ordered by the doctor.

## Chapter summary

- The nephron filters, reabsorbs and secretes; GFR of 125 mL/min means 99% of the filtrate is returned to the blood.
- ADH controls water, aldosterone controls sodium and potassium, and the RAAS links them to blood pressure.
- TBW is 60% of weight, two-thirds inside the cells; maintenance fluid follows the 4-2-1 rule.
- Potassium and sodium disorders are corrected slowly under monitoring; read the ABG by pH, then CO₂ and HCO₃.
- Prevention of kidney disease rests on control of BP and sugar, safe medicines, hydration and yearly screening.

## Practice

**MCQs (with reasons)**

1. Most glucose reabsorption occurs in the: (a) proximal tubule (b) loop of Henle (c) distal tubule (d) collecting duct.
2. The hormone that makes the collecting duct permeable to water is: (a) aldosterone (b) ADH (c) renin (d) ANP.
3. A 70 kg adult needs maintenance fluid by the 4-2-1 rule of: (a) 70 (b) 90 (c) 110 (d) 140 mL/h.
4. A peaked T wave and wide QRS suggest: (a) hypokalaemia (b) hyperkalaemia (c) hypocalcaemia (d) hypernatraemia.
5. pH 7.28, PaCO₂ 30 and HCO₃ 14 indicate: (a) respiratory acidosis (b) metabolic alkalosis (c) metabolic acidosis with respiratory compensation (d) normal.

::: note Answers and rationales
**1. (a).** The proximal tubule reabsorbs all filtered glucose through sodium-linked carriers; glucose appears in urine only when blood glucose passes about 180 mg/dL.
**2. (b).** ADH inserts aquaporin channels in the collecting duct. Aldosterone acts on sodium, renin is an enzyme and ANP promotes sodium loss.
**3. (c).** 40 + 20 + 50 = 110 mL/h. Option (d) would be 2 mL/kg/h for the whole weight.
**4. (b).** High potassium reduces the resting potential and gives tall peaked T waves, then wide QRS and arrest; low potassium gives flat T waves and U waves.
**5. (c).** A low pH with low bicarbonate is metabolic acidosis and a low CO₂ (expected 29 by Winter's formula) shows the lungs blowing off acid.
:::

**Short answer (3 marks): Urine output and the 4-2-1 rule.** The minimum urine output in an adult is 0.5 mL/kg/h, which is 35 mL/h for 70 kg, and below this the nurse reports possible acute kidney injury or hypovolaemia. Maintenance fluid is 4 mL/kg/h for the first 10 kg, 2 for the next 10 kg and 1 for each kg above 20. An 18-kg child needs 56 mL/h and a 70-kg adult 110 mL/h. Strict input-output charting and daily weight guide the plan.

**Medium answer (5 marks): Describe the control of water and sodium balance (Figure 3.2).** When blood volume or BP falls, or plasma osmolality rises, **osmoreceptors** and baroreceptors make the posterior pituitary release **ADH**, which opens water channels in the collecting duct so water is kept and urine is concentrated. The same fall in perfusion makes the juxtaglomerular cells release **renin**, which forms **angiotensin II**, a vasoconstrictor, and **aldosterone** from the adrenal cortex, which makes the distal tubule retain sodium (water follows) and lose potassium. Both pathways restore the volume. When the atria are stretched, **ANP** causes sodium and water loss. Nursing relevance: patients on ACE inhibitors or spironolactone need potassium checks, those on furosemide need daily weights, and fluid in heart failure is restricted.

**Long answer (10 marks): Mr Hari Prasad Dahal, 58, 60 kg, a diabetic and hypertensive patient, comes to the emergency department of a teaching hospital with breathlessness, vomiting and leg swelling. He passes 200 mL of urine a day. BP 170/100 mmHg, weight 4 kg above his dry weight, creatinine 6.5 mg/dL, potassium 6.8 mmol/L, ECG with peaked T waves. Discuss the condition and prepare a nursing care plan.**

*Introduction.* This is **chronic kidney disease stage 5 (end stage)** with fluid overload and life-threatening hyperkalaemia. His creatinine clearance is (140 − 58) × 60 ÷ (72 × 6.5) = **10.5 mL/min**, below 15. The kidneys can no longer excrete potassium, water or acid, causing oedema, hypertension, uraemic vomiting and a risk of cardiac arrest. Diabetic nephropathy and hypertension are the likely causes.

*Management.* (1) Protect the heart first: **10 mL of 10% calcium gluconate** IV over 10 minutes with ECG monitoring. (2) Move potassium into cells: 10 units of regular insulin with 25 g glucose, that is **50 mL of 50% dextrose**, and nebulised salbutamol; check glucose hourly for hypoglycaemia. (3) Remove potassium and fluid by **urgent haemodialysis**: with 4 kg excess, ultrafiltration of 3 L over 4 hours is 750 mL/h, or **12.5 mL/kg/h**, below the safe limit of 13. (4) Fluid allowance is the urine output plus 500 mL, so **700 mL/day**. (5) Treat BP, nausea and acidosis; the long-term plan is dialysis (the government supports it), transplant assessment, anaemia and bone care.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "my legs are swollen and I can't breathe lying flat." **O:** weight +4 kg, BP 170/100, oedema 3+, urine 200 mL/day. | **Excess fluid volume** related to compromised regulatory mechanism (renal failure), as evidenced by oedema, weight gain and hypertension. | **Fluid balance:** weight down to dry weight, oedema 1+ or less, BP below 140/90 in 1 week. | 1. Fluid limit 700 mL/day and salt below 2 g; *limits retention.* 2. Daily weight on the same scale and strict input-output; *shows fluid trend.* 3. Dialysis with UF at 750 mL/h; *removes fluid safely.* 4. Check BP before and after dialysis; *detects hypotension.* | Weight and oedema checked daily; target dry weight reached. |
| **O:** K 6.8 mmol/L, peaked T waves, weak pulse. | **Risk for electrolyte imbalance** (hyperkalaemia) related to kidney failure, as evidenced by raised potassium and ECG change. | **Electrolyte balance:** K 3.5-5.0, normal ECG within 12 h. | 1. Continuous ECG; *detects arrhythmia.* 2. Calcium gluconate, insulin with dextrose as ordered; *protects heart and lowers K.* 3. Hourly glucose; *prevents insulin hypoglycaemia.* 4. Low-potassium diet teaching and no potassium-sparing drugs; *prevents relapse.* | K rechecked at 2, 6 and 12 h; ECG normalised. |
| **S:** nausea, itching. **O:** vomiting, urea high, uraemic breath, albumin low. | **Imbalanced nutrition: less than body requirements** related to anorexia and uraemia, as evidenced by vomiting and weight pattern. | **Nutritional status:** keeps down 75% of meals, no vomiting in 3 days. | 1. Antiemetic before meals as ordered; *reduces nausea.* 2. Small frequent meals with controlled protein, potassium and phosphate; *lessens uraemic load.* 3. Oral care before meals; *improves taste.* 4. Dietitian referral; *tailors the plan.* | Meal intake chart and weekly weight. |
| **S:** "how will we pay for dialysis?" **O:** farmer, family anxious. | **Deficient knowledge and anxiety** related to new illness and costs, as evidenced by questions and tearfulness. | **Knowledge: illness care:** patient and family explain diet, fistula care and dialysis schedule in 1 week. | 1. Teach fistula protection and warning signs; *keeps access working.* 2. Link to social worker and the free dialysis programme and medicine support; *lowers cost burden.* 3. Allow questions and involve the family; *builds coping.* | Return explanation correct; attends dialysis. |

*Prevention and education.* Control BP and sugar, avoid NSAIDs, check urine albumin yearly. *Conclusion.* In kidney failure the nurse watches potassium, fluid and breathing, and protects the fistula arm.

::: tip Exam tip
For any kidney question quote the GFR formula and the staging, then link every symptom to retained water, potassium or acid. Always list hyperkalaemia treatment in the order calcium, insulin with glucose, then dialysis.
:::
