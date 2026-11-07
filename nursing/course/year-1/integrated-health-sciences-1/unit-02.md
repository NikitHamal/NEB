---
subject: Integrated Health Sciences I
grade: BSc Nursing Year 1
unit: 2
title: Blood, Haemostasis and Immunity
hours: 30
area: BSN 1 · Integrated Health Sciences I · Unit 2
---

Blood is the tissue a nurse handles most: it is drawn, tested, transfused and watched for loss. This unit covers its composition, the red cell and haemoglobin, anaemia (the commonest nutritional problem among Nepali women and children), white cells, clotting, blood groups and the immune system, with the red-cell indices and iron deficit calculated by formula.

::: key What this unit gives you
- Composition and functions of blood, and haemopoiesis in a diagram.
- Real stained blood smears: normal, iron-deficiency and sickle cell, labelled.
- Red-cell indices (MCV, MCH, MCHC), corrected reticulocyte count, absolute neutrophil count and the Ganzoni iron deficit, all worked step by step.
- The coagulation cascade, ABO and Rh groups, innate and adaptive immunity.
- Eight points on nursing responsibilities in blood transfusion, and model answers with a full care plan for anaemia in pregnancy.
:::

## 2.1 Composition and functions of blood

Blood is a fluid connective tissue. An adult of 60 kg has about 70 mL/kg, that is **4200 mL** of blood, of which plasma (55%) is **2310 mL**. Plasma is 91% water and carries proteins (albumin, globulins, fibrinogen), electrolytes, nutrients and hormones. The formed elements are **red cells** (about 45% of the volume, the haematocrit), **white cells** and **platelets**. Functions: transport (oxygen, CO₂, nutrients, hormones), regulation (pH, temperature, fluid balance) and protection (clotting and immunity).

```svgfig label="2.1" caption="A centrifuged blood tube and the common cell counts. Packed red cells make the haematocrit; the thin buffy coat holds white cells and platelets."
f = Fig(760, 250)
f.box(60, 20, 70, 24, "", fill="#e5e7eb", stroke=SLATE, r=4)
f.box(60, 44, 70, 120, "", fill="#fef3c7", stroke=AMBER, r=0)
f.box(60, 164, 70, 8, "", fill="#f8fafc", stroke=SLATE, r=0)
f.box(60, 172, 70, 62, "", fill="#dc2626", stroke=RED, r=0)
f.arrow([(140, 100), (200, 100)], color=AMBER, sw=1.5); f.text(210, 100, "Plasma 55%: water, albumin, globulins, fibrinogen", size=11.5, color=AMBER, bold=True, anchor="start")
f.arrow([(140, 168), (200, 160)], color=SLATE, sw=1.5); f.text(210, 158, "Buffy coat <1%: white cells + platelets", size=11.5, color=SLATE, bold=True, anchor="start")
f.arrow([(140, 205), (200, 205)], color=RED, sw=1.5); f.text(210, 205, "Red cells 45% (haematocrit)", size=11.5, color=RED, bold=True, anchor="start")
```

| Test | Normal adult value |
|---|---|
| Haemoglobin | men 13-17 g/dL, women 12-15 g/dL (anaemia in pregnancy: below 11 g/dL) |
| Red cells / haematocrit | 4.5-5.5 million/µL; men 40-50%, women 36-46% |
| White cells | 4,000-11,000/µL (neutrophils 40-70%, lymphocytes 20-40%, monocytes 2-8%, eosinophils 1-4%, basophils below 1%) |
| Platelets | 150,000-400,000/µL |

## 2.2 Haemopoiesis and the red cell

All blood cells come from a pluripotent stem cell in red bone marrow (the flat bones, vertebrae and the ends of long bones in adults; the liver and spleen in the fetus). Erythropoietin from the kidney, released when oxygen is low, drives red-cell production. A red cell is a biconcave disc without a nucleus, lives about **120 days** and is removed by the spleen. Its haemoglobin has four haem units, each with one iron atom, and carries 1.34 mL of oxygen per gram. Production needs **iron, vitamin B12, folate, protein and vitamin C**. One gram of haemoglobin contains **3.47 mg** of iron, so a loss of 500 mL of blood (about 75 g Hb) costs roughly 260 mg of iron.

```svgfig label="2.2" caption="Haemopoiesis. The stem cell branches into the myeloid line (red cells, platelets, granulocytes, monocytes) and the lymphoid line (B, T and NK cells)."
f = Fig(760, 270)
f.box(300, 8, 160, 40, "Pluripotent stem cell\n(bone marrow)", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(110, 90, 190, 40, "Myeloid progenitor", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(470, 90, 190, 40, "Lymphoid progenitor", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.arrow([(340, 48), (230, 90)], color=SLATE, sw=1.6); f.arrow([(420, 48), (540, 90)], color=SLATE, sw=1.6)
for i, (t_, c) in enumerate([("Red cells\n(erythropoietin)", RED), ("Platelets\n(thrombopoietin)", AMBER), ("Neutrophil\nEosino / Baso", TEAL), ("Monocyte\nmacrophage", TEAL)]):
    x = 8 + i * 118
    f.box(x, 190, 108, 54, t_, fill="#ffffff", stroke=c, size=10.5, color=c, bold=True); f.arrow([(205, 130), (x + 54, 190)], color=SLATE, sw=1)
for i, (t_, c) in enumerate([("B cell\nplasma cell", NAVY), ("T cell\nhelper, cytotoxic", NAVY), ("NK cell", NAVY)]):
    x = 490 + i * 90 - 40 if i else 450
    x = [470, 570, 670][i]
    f.box(x, 190, 86, 54, t_, fill="#ffffff", stroke=c, size=10, color=c, bold=True); f.arrow([(565, 130), (x + 43, 190)], color=SLATE, sw=1)
```

### Red-cell indices

The indices describe the size and haemoglobin content of red cells. **MCV** = haematocrit (%) × 10 ÷ RBC (million/µL); **MCH** = Hb (g/dL) × 10 ÷ RBC; **MCHC** = Hb ÷ haematocrit × 100. For Hb 12.0, Hct 36 and RBC 4.0: MCV = **90 fL**, MCH = **30 pg**, MCHC = **33.3 g/dL**, all normal (MCV 80-100 fL, MCH 27-32 pg, MCHC 32-36). For an anaemic woman with Hb 8.0, Hct 27 and RBC 3.8: MCV = **71.1 fL** (microcytic), MCH = **21.1 pg** and MCHC = **29.6 g/dL** (hypochromic), the picture of iron deficiency.

The **corrected reticulocyte count** shows whether marrow is responding: retic 4% × (patient Hct 27 ÷ normal 45) = **2.4%**, below 2%-3% is an inadequate response. The **absolute neutrophil count** = WBC × neutrophil fraction = 8,000 × 0.60 = **4800/µL**; below 500 is severe neutropenia needing reverse isolation.

```photogrid label="2.1" cols="3" ratio="1.0" caption="Real stained blood smears. (a) Normal: biconcave red cells with a central pallor, one neutrophil (multilobed nucleus) and platelets. (b) Iron deficiency: small pale (hypochromic microcytic) red cells with a large central pallor, and one small lymphocyte. (c) Sickle cell disease: crescent-shaped red cells among target cells."
@ photo id="nur1/rbc-normal" cap="Normal smear (Wright)"
fit 1.0
focus 0.5 0.5
mark 0.50 0.52 "1"
key 1 (a) Neutrophil with a segmented nucleus
@ photo id="nur1/ida" cap="Iron-deficiency anaemia"
fit 1.0
focus 0.5 0.5
mark 0.58 0.45 "1"
key 1 (b) Lymphocyte, about one red cell wide, beside pale small red cells
@ photo id="nur1/sickle" cap="Sickle cell anaemia"
fit 1.0
focus 0.5 0.5
mark 0.50 0.50 "1"
key 1 (c) Crescent-shaped sickled red cells
```

## 2.3 Anaemia

Anaemia is a haemoglobin below the reference for age and sex (below 11 g/dL in pregnancy and in children 6-59 months; below 12 in non-pregnant women). It is very common in Nepal: the Nepal Demographic and Health Survey 2022 reported about two in five children under five and about one in three women aged 15-49 as anaemic. The national programme gives **iron-folic acid tablets** to pregnant women (180 tablets), **albendazole** deworming, and **micronutrient powder** for children 6-23 months. *Classification by indices:* microcytic hypochromic (iron deficiency, thalassaemia), normocytic (acute blood loss, chronic disease) and macrocytic (B12 or folate deficiency).

**Parenteral iron.** The **Ganzoni** formula estimates the total iron deficit: weight (kg) × (target Hb − actual Hb) × 2.4 + 500 mg of stores. For a woman of 50 kg with Hb 8.0 and a target of 15: 50 × 7.0 × 2.4 + 500 = **1340 mg**. Iron sucrose is given in divided doses, never as a single large dose.

## 2.4 White cells and immunity

White cells defend the body. **Neutrophils** (first responders, phagocytosis) rise in bacterial infection, **lymphocytes** (B and T cells) in viral infection, **eosinophils** in worms and allergy (common with helminths in rural Nepal), **monocytes** become macrophages, and **basophils** release histamine. **Innate immunity** is immediate and non-specific: skin, mucus, stomach acid, phagocytes, complement, fever. **Adaptive immunity** is specific and has memory: B cells make antibodies (humoral) and T cells kill infected cells (cell-mediated).

- **Natural active:** infection itself. **Artificial active:** vaccine (BCG, OPV, pentavalent, PCV, rotavirus, MR, TD, HPV in the NIP Nepal schedule).
- **Natural passive:** maternal IgG across the placenta and IgA in colostrum. **Artificial passive:** ready-made antibody (tetanus immunoglobulin, rabies immunoglobulin, anti-D).
- **Antibody classes:** IgG (most abundant, crosses placenta), IgM (first response), IgA (secretions), IgE (allergy), IgD (B-cell receptor).

## 2.5 Haemostasis and coagulation

Haemostasis stops bleeding in three steps: **vascular spasm**, a **platelet plug** (adhesion by von Willebrand factor, aggregation) and **coagulation**, the conversion of soluble fibrinogen to a fibrin mesh. The *extrinsic pathway* (tissue factor, factor VII) is fast and measured by **PT/INR**; the *intrinsic pathway* (factors XII, XI, IX, VIII) is measured by **aPTT**; both meet at factor X, forming thrombin. Calcium (factor IV) and vitamin K (for factors II, VII, IX, X) are essential. Warfarin blocks vitamin K, so it is monitored by INR (target 2-3); heparin acts on antithrombin and is monitored by aPTT.

```svgfig label="2.3" caption="The coagulation cascade in simplified form. Prothrombin time tests the extrinsic limb, aPTT the intrinsic limb; both feed the common pathway that makes fibrin."
f = Fig(760, 300)
f.box(40, 10, 220, 34, "Intrinsic: XII → XI → IX (+VIIIa)", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(500, 10, 220, 34, "Extrinsic: tissue factor + VII", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.text(150, 62, "tested by aPTT; heparin", size=10.5, color=NAVY, bold=True); f.text(610, 62, "tested by PT / INR; warfarin", size=10.5, color=AMBER, bold=True)
f.box(290, 100, 180, 36, "Factor X → Xa", fill=SOFT, stroke=SLATE, size=11, bold=True)
f.arrow([(150, 44), (150, 78), (340, 78), (340, 100)], color=NAVY, sw=1.8); f.arrow([(610, 44), (610, 78), (420, 78), (420, 100)], color=AMBER, sw=1.8)
f.box(290, 170, 180, 36, "Prothrombin → Thrombin", fill=SOFT, stroke=SLATE, size=11, bold=True)
f.box(290, 240, 180, 36, "Fibrinogen → Fibrin clot", fill=ROSE, stroke=RED, size=11, bold=True)
f.arrow([(380, 136), (380, 170)], color=SLATE, sw=1.8); f.arrow([(380, 206), (380, 240)], color=SLATE, sw=1.8)
f.text(570, 188, "Ca²⁺ and platelet phospholipid needed", size=10.5, color=SLATE, bold=True, anchor="start")
f.text(570, 258, "stabilised by factor XIIIa", size=10.5, color=SLATE, bold=True, anchor="start")
```

## 2.6 Blood groups and transfusion safety

The **ABO** group depends on antigens on the red cell; the plasma carries the opposite antibody. **Rh** positive means the D antigen is present; Rh-negative blood has no D antigen and forms anti-D only after exposure.

| Group | Red-cell antigen | Plasma antibody | Can receive red cells from |
|---|---|---|---|
| A | A | anti-B | A, O |
| B | B | anti-A | B, O |
| AB | A and B | none | A, B, AB, O (universal recipient) |
| O | none | anti-A and anti-B | O only (universal donor) |

A parent of group A (AO) and a parent of group B (BO) can have children of all four groups, each with probability 1 in 4. An **Rh-negative mother** carrying an Rh-positive baby can be sensitised at delivery; **anti-D immunoglobulin 300 µg** within 72 hours neutralises 30 mL of fetal whole blood, so a 15 mL bleed needs **1** vial. In Nepal blood is collected and screened (HIV, hepatitis B and C, syphilis, malaria) by the **Nepal Red Cross Society blood transfusion service** and hospital blood banks; only voluntary non-remunerated donors are used.

```python
mcv = 36 * 10 / 4.0
mch = 12.0 * 10 / 4.0
mchc = 12.0 / 36 * 100
imcv = 27 * 10 / 3.8
retic = 4 * 27 / 45
ganzoni = 50 * (15 - 8.0) * 2.4 + 500
print("MCV", f"{mcv:.0f}")
print("MCH", f"{mch:.0f}")
print("MCHC", f"{mchc:.1f}")
print("Anaemic MCV", f"{imcv:.1f}")
print("Corrected retic", f"{retic:.1f}")
print("Ganzoni mg", f"{ganzoni:.0f}")
```

```text
MCV 90
MCH 30
MCHC 33.3
Anaemic MCV 71.1
Corrected retic 2.4
Ganzoni mg 1340
```

## 2.7 Nursing responsibilities in blood transfusion: eight points

1. **Verify the order and the consent.** Check the doctor's written order, the indication and the patient's informed consent. Confirm the blood group and cross-match result in the file. An undocumented transfusion is a legal and safety risk.
2. **Two-nurse identity check.** At the bedside, two nurses read aloud the patient's name, age, hospital number, ABO and Rh group on the wristband, the blood bag label and the cross-match form. Check the donation number and the expiry date. Most fatal reactions come from a wrong-patient error at this step.
3. **Inspect the bag.** Look for clots, discolouration, haemolysis (pink plasma), leaks or air bubbles, and never use a bag out of the blood bank for more than 30 minutes. Never warm blood in hot water or a microwave. Bad storage damages cells and causes reactions.
4. **Use the right line.** Use an 18-20 G cannula and a set with a 170-micron filter, primed only with normal saline (never dextrose or Ringer's lactate, which cause clotting or haemolysis). Do not add drugs to the blood. A separate line is needed for any other infusion.
5. **Baseline vitals, then start slowly.** Record temperature, pulse, BP and respiration before starting. Run at about 2 mL/min (15 drops/min) for the first 15 minutes and stay with the patient. Most severe reactions begin in this time.
6. **Watch for reactions.** Fever, chills, rash, itching, back pain, breathlessness, hypotension or dark urine mean stop the transfusion at once, keep the line open with saline, call the doctor, recheck the labels and send the bag, set and a fresh sample to the blood bank. Vitals are repeated at 15 minutes, hourly, and at the end.
7. **Complete within 4 hours.** One unit (about 350 mL) usually runs over 2-4 hours, faster only for active bleeding and slower (1 mL/kg/h) in heart failure or the elderly. Longer than 4 hours allows bacteria to grow. Give the diuretic if ordered to prevent circulatory overload.
8. **Document and teach.** Record the unit number, volume, start and stop time, vitals and any reaction. Tell the patient to report itching, shivering, chest tightness or pain at the site. Return the empty bag as per hospital policy and report adverse events in the hospital haemovigilance record.

## Formula and fact sheet

- Blood volume about 70 mL/kg (4200 mL at 60 kg); plasma 55%. Red cell life 120 days. 1 g Hb = 3.47 mg iron.
- MCV = Hct × 10 ÷ RBC; MCH = Hb × 10 ÷ RBC; MCHC = Hb ÷ Hct × 100. Anaemic example: 71.1 fL, 21.1 pg, 29.6 g/dL.
- Corrected reticulocyte % = retic % × (patient Hct ÷ 45) = 2.4%. ANC = WBC × neutrophil fraction = 4800/µL.
- Ganzoni deficit = weight × (target Hb − actual Hb) × 2.4 + 500 = 1340 mg (50 kg, Hb 8.0 to 15).
- PT/INR = extrinsic, aPTT = intrinsic. Anti-D 300 µg covers 30 mL fetal blood.

## Chapter summary

- Blood is plasma (55%) plus cells; all cells arise from marrow stem cells.
- Indices classify anaemia: low MCV and MCH mean iron deficiency, the commonest type in Nepal.
- Clotting runs through the intrinsic and extrinsic pathways to fibrin; INR monitors warfarin, aPTT monitors heparin.
- ABO and Rh matching with a two-nurse bedside check prevents fatal transfusion reactions.
- Immunity is innate (fast, non-specific) and adaptive (specific, memory); vaccines give artificial active immunity.

## Practice

**MCQs (with reasons)**

1. The universal red-cell donor group is: (a) A (b) B (c) AB (d) O.
2. Hb 8.0 g/dL, Hct 27% and RBC 3.8 million/µL give an MCV of: (a) 71 fL (b) 85 fL (c) 95 fL (d) 110 fL.
3. Warfarin therapy is monitored by: (a) aPTT (b) INR (c) bleeding time (d) platelet count.
4. A blood transfusion must be completed within: (a) 1 hour (b) 2 hours (c) 4 hours (d) 8 hours.
5. Tetanus immunoglobulin gives: (a) natural active (b) artificial active (c) natural passive (d) artificial passive immunity.

::: note Answers and rationales
**1. (d).** Group O red cells carry neither A nor B antigen, so recipient anti-A and anti-B cannot attack them. AB is the universal recipient, not donor.
**2. (a).** MCV = 27 × 10 ÷ 3.8 = 71.1 fL, microcytic. Values 85-95 are normal.
**3. (b).** Warfarin depresses vitamin K clotting factors, which the extrinsic pathway (PT/INR) reflects; aPTT monitors heparin.
**4. (c).** After 4 hours at room temperature bacteria multiply, so a bag must finish or be stopped within that time.
**5. (d).** It is ready-made antibody given from outside, so it is passive and artificial.
:::

**Short answer (3 marks): Red-cell indices.** Indices describe the average size and haemoglobin content of red cells. MCV = Hct × 10 ÷ RBC (normal 80-100 fL), MCH = Hb × 10 ÷ RBC (27-32 pg) and MCHC = Hb ÷ Hct × 100 (32-36 g/dL). A woman with Hb 8.0, Hct 27 and RBC 3.8 has MCV 71.1 fL, MCH 21.1 pg and MCHC 29.6 g/dL, which indicates microcytic hypochromic anaemia, usually iron deficiency.

**Medium answer (5 marks): Describe the mechanism of blood coagulation (Figure 2.3).** Clotting is a cascade in which each inactive factor activates the next. After vessel injury, platelets plug the gap and tissue factor starts the *extrinsic pathway* with factor VII, which is quick and tested by PT/INR. The *intrinsic pathway* (XII, XI, IX with VIII) starts in contact with exposed collagen and is tested by aPTT. Both activate **factor X**, and Xa with factor V and calcium converts prothrombin to **thrombin**. Thrombin changes soluble fibrinogen to insoluble **fibrin**, which factor XIIIa cross-links to form a stable clot that traps red cells. Vitamin K is needed for factors II, VII, IX and X, so deficiency (newborns, obstructive jaundice, warfarin) causes bleeding. Later, plasmin dissolves the clot (fibrinolysis). Haemophilia A is factor VIII deficiency and prolongs aPTT.

**Long answer (10 marks): Mrs Sunita Tamang, 24, is 28 weeks pregnant and attends the antenatal clinic with tiredness, breathlessness on climbing stairs and palpitations. She eats mostly rice and tea, pallor of conjunctiva and nail beds is noted, pulse 104/min, BP 100/64 mmHg. Hb 8.0 g/dL, Hct 27%, RBC 3.8 million/µL. Discuss the condition and prepare a nursing care plan.**

*Introduction.* Her Hb is below the 11 g/dL cut-off for pregnancy, so she has anaemia (moderate: 7.0-9.9 g/dL). The indices MCV 71.1 fL, MCH 21.1 pg and MCHC 29.6 g/dL show microcytic hypochromic anaemia: iron deficiency from a diet low in iron, tea that blocks absorption, hookworm and the higher demand of pregnancy (blood volume rises about 40%). Risks are preterm birth, low birth weight, postpartum haemorrhage and heart failure. Her estimated iron deficit by the Ganzoni formula (50 kg, target 15 g/dL) is **1340 mg**. Treatment is oral iron-folic acid (60 mg elemental iron and 400 µg folic acid daily, as in the Nepal safe motherhood programme), albendazole after the first trimester, and iron sucrose in divided IV doses if oral therapy fails or Hb is below 7 g/dL near term. A response is seen as a reticulocyte rise in 7-10 days and Hb rise of about 1 g/dL in 2-3 weeks.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "I get tired and breathless on stairs." **O:** pallor, P 104, BP 100/64, Hb 8.0. | **Activity intolerance** related to reduced oxygen-carrying capacity, as evidenced by fatigue, breathlessness and tachycardia. | **Energy conservation:** walks 100 m without dyspnoea and pulse below 100 in 2 weeks. | 1. Plan rest periods and left lateral lying; *reduces oxygen demand and improves venous return.* 2. Check pulse and RR before and after activity; *measures tolerance.* 3. Give iron-folic acid after food with vitamin C; *iron needs acid for absorption.* | Pulse and RR after walking each visit; goal met when within target. |
| **S:** "I eat rice, dal and tea." **O:** pale conjunctiva, MCV 71.1 fL. | **Imbalanced nutrition: less than body requirements** related to inadequate iron intake. | **Nutritional status:** Hb at least 10 g/dL in 8 weeks. | 1. Teach iron-rich foods (green leafy vegetables, liver, lentils, jaggery, eggs) and vitamin C fruit; *raises dietary iron.* 2. Advise no tea or coffee within 1 hour of meals or tablets; *tannins block iron.* 3. Counsel on black stools and constipation; *common, harmless side effects, so adherence improves.* | Hb repeated at 4 and 8 weeks; tablet count at each visit. |
| **S:** "I forgot some tablets." **O:** no deworming recorded. | **Deficient knowledge** about anaemia and its prevention. | **Knowledge: health behaviour:** states 3 causes and takes at least 90% of tablets. | 1. Explain anaemia, risks to baby and delivery; *motivates adherence.* 2. Give albendazole 400 mg once as ordered; *removes hookworm blood loss.* 3. Teach footwear use, hand washing and delivery at a health facility; *prevents reinfestation and haemorrhage.* | Teach-back at the next visit; return demonstration of tablet schedule. |

::: tip Exam tip
For anaemia questions give the cut-off, the indices with the arithmetic, the classification and the Nepal programme (IFA 180 tablets, albendazole), and end with health education. These earn the full marks.
:::
