---
subject: Adult Nursing I
grade: BSc Nursing Year 2
unit: 5
title: Haematological Nursing: Anaemia, Haemoglobinopathies, Leukaemia, Bleeding Disorders and Blood Transfusion
hours: 22
area: BSN 9 · Adult Nursing I · Unit 5
---

Blood disease touches every ward. **Anaemia affects 34% of women aged 15-49 and 43% of children aged 6-59 months in Nepal** (NDHS 2022); thalassaemia and sickle cell disease are reported in the Terai and in Tharu communities; leukaemia fills the haematology and oncology wards at Bhaktapur Cancer Hospital, BP Koirala Memorial Cancer Hospital and the teaching hospitals; and the **Nepal Red Cross Society Blood Transfusion Service** supplies voluntary-donor blood that nurses give every day. The nurse reads the blood count, gives iron and blood safely, protects the neutropenic patient and recognises a transfusion reaction in minutes. All arithmetic is checked by program.

::: key What this unit gives you
- Real photographs of an iron-deficiency blood smear, sickle cells, leukaemic blasts, purpura and a unit of blood during transfusion, with three SVG figures.
- Red-cell indices, reticulocyte correction, iron deficit (Ganzoni), absolute neutrophil count, BSA and drug dose, factor VIII dose and transfusion rate.
- Anaemia (eight points of iron therapy and teaching), haemoglobinopathies, leukaemia (eight points of nursing care), bleeding disorders and transfusion (eight responsibilities and eight reactions).
- Model answers and a NANDA-I plan for a woman with severe iron-deficiency anaemia needing transfusion.
:::

## 5.1 Reading the blood count

Normal adult values: **haemoglobin 12-16 g/dL (women) and 13-17 g/dL (men)**, haematocrit 36-46% and 40-50%, **RBC 4.0-5.5 million/µL**, WBC 4,000-11,000/µL, platelets 150,000-400,000/µL, MCV 80-100 fL, MCH 27-32 pg, MCHC 32-36 g/dL. **Anaemia** is Hb below 12 g/dL in women and 13 g/dL in men (11 in pregnancy). The **indices** explain the type: **MCV = Hct × 10 ÷ RBC**, **MCH = Hb × 10 ÷ RBC**, **MCHC = Hb × 100 ÷ Hct**. The **corrected reticulocyte count** (reticulocyte % × Hct ÷ 45) shows whether the marrow is responding; the **absolute neutrophil count** (ANC = WBC × neutrophils % ÷ 100) shows the risk of infection.

```python
hb, hct, rbc = 7.0, 24, 3.6
mcv = hct * 10 / rbc; mch = hb * 10 / rbc; mchc = hb * 100 / hct
print(f"MCV = {hct} x 10 / {rbc} = {mcv:.1f} fL; MCH = {hb} x 10 / {rbc} = {mch:.1f} pg; MCHC = {hb} x 100 / {hct} = {mchc:.1f} g/dL: microcytic, hypochromic")
ret = 3 * hct / 45
print(f"Corrected reticulocyte count = 3 x {hct} / 45 = {ret:.1f}% (below 2%: marrow not responding)")
w = 55; deficit = w * (12 - hb) * 2.4 + 500
print(f"Iron deficit (Ganzoni) = {w} x (12 - {hb}) x 2.4 + 500 = {deficit:,.0f} mg")
anc = 2000 * 20 / 100
print(f"ANC = 2,000 x 20 / 100 = {anc:,.0f} per microlitre = {anc / 1000:.1f} x 10^9/L (below 500: severe neutropenia)")
print(f"Oral iron: ferrous sulphate 200 mg has 65 mg elemental; 3 tablets daily = {3 * 65} mg; IFA 180 tablets = {180 // 30} months")
```

```text
MCV = 24 x 10 / 3.6 = 66.7 fL; MCH = 7.0 x 10 / 3.6 = 19.4 pg; MCHC = 7.0 x 100 / 24 = 29.2 g/dL: microcytic, hypochromic
Corrected reticulocyte count = 3 x 24 / 45 = 1.6% (below 2%: marrow not responding)
Iron deficit (Ganzoni) = 55 x (12 - 7.0) x 2.4 + 500 = 1,160 mg
ANC = 2,000 x 20 / 100 = 400 per microlitre = 0.4 x 10^9/L (below 500: severe neutropenia)
Oral iron: ferrous sulphate 200 mg has 65 mg elemental; 3 tablets daily = 195 mg; IFA 180 tablets = 6 months
```

A patient with Hb 7.0, Hct 24 and RBC 3.6 has **MCV 66.7 fL, MCH 19.4 pg and MCHC 29.2 g/dL**: small, pale cells typical of iron deficiency (Figure 5.1a). A reticulocyte count of 3% corrects to **1.6%**, a poor marrow response. The **iron deficit is 1,160 mg** for a 55-kg patient. A WBC of 2,000 with 20% neutrophils gives an **ANC of 400 per µL**: severe neutropenia. Three tablets of ferrous sulphate (200 mg each) give **195 mg of elemental iron a day**.

```photogrid label="5.1" cols="4" ratio="1.0" caption="Blood and bleeding on the slide and on the skin. (a) A real peripheral smear in iron-deficiency anaemia: pale, small red cells with large central pallor and a normal lymphocyte for comparison. (b) A real smear in sickle cell anaemia: elongated, curved red cells. (c) A real smear in acute lymphoblastic leukaemia: large purple blasts crowd out the red cells. (d) Real purpura: red-purple spots in the skin from bleeding, in a patient with a low platelet count or vasculitis."
@ photo id="nur5/ida" cap="Iron-deficiency smear"
fit 1.0
focus 0.5 0.5
mark 0.62 0.59 "1"
mark 0.35 0.70 "2"
key 1 (a) Lymphocyte nucleus: a normal red cell is about the same size
key 2 (a) Hypochromic red cell: pale centre over one third of the cell
@ photo id="nur5/sickle" cap="Sickle cell smear"
fit 1.0
focus 0.5 0.5
mark 0.50 0.50 "3"
key 3 (b) Sickle cell: crescent-shaped, rigid, blocks small vessels and is destroyed early
@ photo id="nur5/all" cap="Acute leukaemia smear"
fit 1.0
focus 0.5 0.5
mark 0.38 0.68 "4"
key 4 (c) Lymphoblast: large nucleus, high nucleus-to-cytoplasm ratio, fine chromatin
@ photo id="nur5/purpura" cap="Purpura"
fit 1.0
focus 0.5 0.5
mark 0.50 0.50 "5"
key 5 (d) Purpuric spots: do not blanch on pressure; look for low platelets, clotting problem or vasculitis
```

```svgfig label="5.2" caption="Classifying anaemia by MCV. Small cells (MCV below 80 fL) point to iron deficiency, thalassaemia or chronic disease; normal-sized cells (80-100 fL) to acute blood loss, haemolysis, aplastic anaemia or kidney disease; large cells (over 100 fL) to vitamin B12 or folate deficiency, alcohol or hypothyroidism."
f = Fig(760, 210)
f.box(260, 8, 240, 44, "Anaemia: Hb low. Check MCV", fill=BLUE, stroke=NAVY, size=12, bold=True)
cols = [("MICROCYTIC\nMCV below 80", "Iron deficiency\nThalassaemia\nChronic disease", ROSE, RED, 10), ("NORMOCYTIC\nMCV 80-100", "Acute blood loss\nHaemolysis, aplastic\nKidney disease", SAND, AMBER, 265), ("MACROCYTIC\nMCV above 100", "B12 or folate lack\nAlcohol, liver disease\nHypothyroidism", MINT, TEAL, 520)]
for t, d, fl, st, x in cols:
    f.box(x, 78, 230, 46, t, fill=fl, stroke=st, size=11, bold=True)
    f.box(x, 138, 230, 62, d, fill=SOFT, stroke=st, size=10.5)
    f.arrow([(380, 52), (x + 115, 78)], sw=1.8)
```

## 5.2 Anaemia, with focus on iron deficiency

**Anaemia** is a reduction of haemoglobin that lowers oxygen delivery. The commonest cause in Nepal is **iron deficiency**: low iron intake (a cereal-based diet, tea with meals), **blood loss** (heavy menstruation, childbirth, hookworm, bleeding piles and ulcers) and increased need (pregnancy, adolescence, infancy). Other types: **megaloblastic** (vitamin B12 or folate deficiency), **haemolytic** (sickle cell, thalassaemia, malaria, G6PD deficiency), **aplastic** (marrow failure) and **anaemia of chronic disease**. **Symptoms** are fatigue, pallor, breathlessness, palpitation, headache, dizziness and, in severe iron deficiency, **brittle spoon-shaped nails (koilonychia), sore tongue, angular cheilitis and pica**. Signs: pale conjunctivae and palms, tachycardia, flow murmur and, when severe, heart failure.

### Anaemia and iron therapy: eight points of nursing care and teaching

1. **Find the cause as well as treating the anaemia.** Ask about diet, periods, pregnancies, black stools, piles and worm infection. Send stool for ova and occult blood. Treating the cause (deworming with albendazole 400 mg once, treating the ulcer) prevents relapse.
2. **Give oral iron correctly.** Ferrous sulphate 200 mg (65 mg elemental iron) two or three times a day on an empty stomach, with vitamin C (citrus juice) improves absorption. If it upsets the stomach, give it with food or at night. Continue for 3 months after the Hb is normal to fill the stores.
3. **Warn about the side effects.** Iron turns the stool black and may cause constipation, nausea or a metallic taste. Black stool from iron is formed and not tarry or sticky, which tells it from melaena. Advise fluids, fibre and walking.
4. **Avoid what blocks iron.** Tea, coffee, milk, calcium and antacids reduce absorption, so keep them 2 hours apart from the iron tablets. Take tablets with water. Store the tablets away from children, since an overdose is dangerous.
5. **Use injectable iron safely.** Intravenous iron (iron sucrose) is given in a hospital when oral iron fails or is not tolerated, with a test for allergy and observation for 30 minutes. Deep intramuscular iron stains the skin and is painful. Calculate the dose with the Ganzoni formula.
6. **Improve diet.** Teach iron-rich food: green leafy vegetables (rayo saag, spinach), pulses, liver, meat, fish, egg yolk, jaggery, and vitamin C-rich fruit. For babies, add iron-rich foods from 6 months. Use iron cooking pots where possible.
7. **Support activity and safety.** Plan rest between activities, rise slowly from bed and check pulse and breathing during exercise. Severe anaemia strains the heart. Give oxygen and prepare for transfusion if there is breathlessness at rest.
8. **Know the national programmes.** Nepal gives **180 iron-folic acid tablets** to every pregnant woman, weekly iron-folic acid to adolescent girls, iron supplements (sprinkles) to children 6-23 months and deworming twice yearly. Teach the family to collect them free from the health post or FCHV. Check the Hb 4 weeks after starting.

## 5.3 Haemoglobinopathies: sickle cell disease and thalassaemia

**Sickle cell disease** is a genetic disorder in which abnormal haemoglobin S makes red cells sickle-shaped when oxygen is low (Figure 5.1b). The cells block small vessels, causing **painful crises**, and are destroyed early, causing haemolytic anaemia. It occurs in several Terai communities, with **sickle cell trait** reported in Tharu populations. A **crisis** is triggered by dehydration, infection, cold and hypoxia. Care: **hydration** (oral and IV), strong **pain relief** by the clock (paracetamol, NSAID, morphine), **oxygen** if SpO2 is low, warmth, antibiotics for infection, folic acid daily and penicillin prophylaxis in children, vaccines, and genetic counselling.

**Thalassaemia** is an inherited failure to make globin chains. **Beta-thalassaemia major** shows severe anaemia from 6 months of age, an enlarged spleen and liver, bone changes and growth failure, and needs **regular transfusion every 3-4 weeks** with **iron chelation** (deferasirox 20 mg/kg a day, which is 1,000 mg for a 50-kg patient) because transfusion causes iron overload. **Counselling and screening before marriage and early in pregnancy** are the way to prevent it; the Nepal Thalassaemia Society supports families.

## 5.4 Leukaemia and its nursing care

**Leukaemia** is cancer of the blood-forming cells in the marrow. Abnormal white cells (blasts) multiply and crowd out normal red cells, white cells and platelets, so the patient has **anaemia (pallor, tiredness), infections (fever, mouth ulcers) and bleeding (bruises, gum bleeding, nosebleed)**, with bone pain and enlarged spleen, liver and lymph nodes. **Acute lymphoblastic leukaemia (ALL)** is commonest in children, **acute myeloid leukaemia (AML)** in adults, **chronic myeloid leukaemia (CML)** in middle age and **chronic lymphocytic leukaemia (CLL)** in the old. Diagnosis is by the blood film (Figure 5.1c), bone-marrow aspirate and flow cytometry. Treatment is **chemotherapy** in phases (induction, consolidation, maintenance), targeted drugs (imatinib for CML) and stem-cell transplant where available. Drug doses are calculated from **body surface area (BSA)**: Mosteller formula **BSA (m²) = √(height cm × weight kg ÷ 3600)**.

```svgfig label="5.3" caption="Where the four main leukaemias arise. The stem cell makes myeloid cells (red cells, platelets, neutrophils, monocytes) and lymphoid cells (B and T lymphocytes). Acute leukaemias arise from immature blasts and progress in weeks; chronic leukaemias arise from more mature cells and progress over years."
f = Fig(760, 210)
f.box(300, 8, 160, 44, "Blood stem cell", fill=BLUE, stroke=NAVY, size=12, bold=True)
f.box(80, 85, 220, 44, "Myeloid line", fill=SAND, stroke=AMBER, size=12, bold=True)
f.box(460, 85, 220, 44, "Lymphoid line", fill=MINT, stroke=TEAL, size=12, bold=True)
f.arrow([(340, 52), (200, 85)], sw=2); f.arrow([(420, 52), (560, 85)], sw=2)
for i, t in enumerate(["AML\nacute, adults", "CML\nchronic, middle age"]):
    f.box(60 + i * 130, 150, 120, 48, t, fill=ROSE, stroke=RED, size=10, bold=True); f.arrow([(140 + i * 60, 129), (120 + i * 130, 150)], sw=1.6)
for i, t in enumerate(["ALL\nacute, children", "CLL\nchronic, elderly"]):
    f.box(440 + i * 130, 150, 120, 48, t, fill=ROSE, stroke=RED, size=10, bold=True); f.arrow([(520 + i * 60, 129), (500 + i * 130, 150)], sw=1.6)
```

### Leukaemia and chemotherapy: eight points of nursing care

1. **Protect from infection (neutropenia).** When the ANC is below 500/µL, use hand hygiene, a single room, no fresh flowers, and cooked food only. Check the temperature every 4 hours; a fever of 38 °C or more is an emergency that needs blood cultures and antibiotics within 60 minutes. Do not give rectal drugs or temperatures.
2. **Prevent and manage bleeding.** Check platelets; below 20,000 /µL there is a risk of spontaneous bleeding. Use a soft toothbrush, an electric razor and avoid IM injections. Hold pressure for 5 minutes after any needle. Report headache, black stool or blood in urine.
3. **Give chemotherapy safely.** Check the order against the BSA, height and weight twice with another nurse, use gloves, gown and a closed system, and dispose of waste in cytotoxic bins. Pregnant staff must not handle cytotoxic drugs. Watch the IV site for leakage (extravasation) and stop the drug if the patient feels burning.
4. **Control nausea and vomiting.** Give the antiemetic (ondansetron, dexamethasone) before the drug and regularly after it. Offer small cool meals, ginger and mouth rinses. Record the vomit volume and watch for dehydration.
5. **Care for the mouth (mucositis).** Inspect the mouth daily and rinse with saline or soda-bicarbonate after meals. Use a soft brush, avoid spicy and acidic food and give analgesic gel. Treat thrush with antifungal drugs.
6. **Manage anaemia and fatigue.** Give red-cell transfusion when Hb is below 7-8 g/dL and platelets when the count is low, as ordered. Plan rest periods and allow the patient to do what they can. Teach that fatigue improves slowly.
7. **Support the child, the adult and the family.** Explain the diagnosis and treatment honestly; leukaemia in children has a good cure rate with full treatment. Involve the family in care, arrange play and schooling, and offer counselling and financial advice about free cancer-care schemes of the Nepal government. Hair loss is temporary; offer a cap or scarf.
8. **Watch for tumour lysis and monitor the labs.** After the first doses the rapid cell death raises potassium, uric acid and phosphate. Give allopurinol, hydrate with IV fluids and check urine output and electrolytes. Report cramps, an irregular pulse and low urine.

## 5.5 Bleeding disorders

**Haemophilia A** is an X-linked inherited deficiency of factor VIII (haemophilia B: factor IX), seen in boys, with bleeding into joints (haemarthrosis) and muscles after minor injury. Treatment is **factor replacement**: **dose in IU = weight (kg) × desired rise (%) × 0.5** for factor VIII. **Immune thrombocytopenic purpura (ITP)** causes a low platelet count with purpura (Figure 5.1d) and is treated with prednisolone. **Disseminated intravascular coagulation (DIC)** is a dangerous complication of sepsis, obstetric emergencies and cancer, with bleeding and clotting together. In all, the nurse prevents injury (soft toothbrush, padded bed, no IM injections), applies pressure and ice to bleeding sites, rests an affected joint, avoids aspirin and NSAIDs, and teaches the family to recognise bleeding and to carry a medical card.

## 5.6 Blood transfusion

**Indications:** acute blood loss with shock, symptomatic anaemia with Hb below 7 g/dL (below 8 g/dL with heart disease), marrow failure, thalassaemia and sickle cell disease. **Components:** whole blood, packed red cells (about 300 mL), platelets, fresh frozen plasma and cryoprecipitate. The group (**ABO and Rh**) and a **cross-match** are done before every red-cell unit. **Each unit of red cells raises the Hb of a 70-kg adult by about 1 g/dL**, so the rise is 70 ÷ weight for a lighter patient. Current practice is to give **one unit and reassess** rather than prescribing two automatically.

```python
import math
h, w = 160, 55
bsa = math.sqrt(h * w / 3600)
print(f"BSA = sqrt({h} x {w} / 3600) = {bsa:.2f} m2; a drug at 100 mg/m2 = {100 * bsa:.0f} mg")
print(f"Factor VIII: 50 kg x 50% x 0.5 = {50 * 50 * 0.5:,.0f} IU")
print(f"Transfusion: 350 mL over 3.5 h = {350 / 3.5:.0f} mL/h; blood set 15 gtt/mL = {350 / 3.5 * 15 / 60:.0f} gtt/min")
print(f"First 15 minutes at 2 mL/min = {2 * 15} mL = {2 * 15} gtt/min on a 15 gtt/mL set")
hb, hct, rbc = 6.0, 20, 3.1
print(f"Case: MCV = {hct * 10 / rbc:.1f} fL; MCH = {hb * 10 / rbc:.1f} pg; MCHC = {hb * 100 / hct:.1f} g/dL; corrected reticulocytes = 1.5 x {hct} / 45 = {1.5 * hct / 45:.2f}%")
print(f"Case iron deficit = 50 x (12 - 6) x 2.4 + 500 = {50 * 6 * 2.4 + 500:,.0f} mg; Hb rise per unit = 70 / 50 = {70 / 50:.1f} g/dL")
```

```text
BSA = sqrt(160 x 55 / 3600) = 1.56 m2; a drug at 100 mg/m2 = 156 mg
Factor VIII: 50 kg x 50% x 0.5 = 1,250 IU
Transfusion: 350 mL over 3.5 h = 100 mL/h; blood set 15 gtt/mL = 25 gtt/min
First 15 minutes at 2 mL/min = 30 mL = 30 gtt/min on a 15 gtt/mL set
Case: MCV = 64.5 fL; MCH = 19.4 pg; MCHC = 30.0 g/dL; corrected reticulocytes = 1.5 x 20 / 45 = 0.67%
Case iron deficit = 50 x (12 - 6) x 2.4 + 500 = 1,220 mg; Hb rise per unit = 70 / 50 = 1.4 g/dL
```

A 160-cm, 55-kg patient has a **BSA of 1.56 m²**, so a drug ordered at 100 mg/m² is **156 mg**. A 50-kg patient with haemophilia A who needs a 50% rise in factor VIII needs **1,250 IU**. A 350-mL unit over 3.5 hours runs at **100 mL/h, which is 25 gtt/min** on a 15 gtt/mL blood set; for the first 15 minutes the rate is **30 mL** at 2 mL/min while the nurse stays beside the patient.

```photogrid label="5.4" cols="2" ratio="1.0" caption="Giving blood. (a) A real unit of red cells hanging on a drip stand during transfusion, with the administration set and a filter. (b) The nurse's response to a suspected transfusion reaction: stop the transfusion first, keep the line open with saline, and call the doctor."
@ photo id="nur5/transf" cap="Blood during transfusion"
fit 1.0
focus 0.5 0.62
mark 0.40 0.70 "1"
mark 0.60 0.90 "2"
key 1 (a) Unit of red cells: check the label, group, expiry and patient identity with a second nurse
key 2 (a) Drip chamber and administration set with filter: use a new set every unit or every 4 hours
@ svg cap="Reaction response"
f = Fig(300, 300)
f.box(10, 8, 280, 52, "1 STOP the blood\nKeep line with saline", fill=ROSE, stroke=RED, size=14, bold=True)
f.box(10, 70, 280, 52, "2 Check patient, ABC,\nvitals; call doctor", fill=SAND, stroke=AMBER, size=14, bold=True)
f.box(10, 132, 280, 52, "3 Recheck bag label\nand patient name", fill=BLUE, stroke=NAVY, size=14, bold=True)
f.box(10, 194, 280, 52, "4 Return bag, set, samples\nto the blood bank", fill=MINT, stroke=TEAL, size=14, bold=True)
f.text(150, 275, "Record and report every reaction", size=14, color=NAVY, bold=True)
```

### Blood transfusion: eight nursing responsibilities

1. **Confirm the need and the consent.** Check the doctor's order (component, volume, rate) and that the patient or guardian understands and has consented. Explain what to expect and to report chills, itching, back pain or breathlessness. Record the pre-transfusion Hb.
2. **Check identity twice.** At the bedside, two qualified persons compare the patient's name band, hospital number, the blood-group label, the unit number, the cross-match tag and the expiry date. A single identity mistake causes ABO incompatibility, the deadliest error. Never "pre-check" in the corridor.
3. **Collect and store correctly.** Take blood from the blood bank only when the patient is ready; start within 30 minutes and finish within 4 hours of leaving the fridge. Do not warm it in hot water or store it in the ward fridge. A unit out of the cold chain must be returned.
4. **Use the right equipment.** Use a new blood set with a 170-200 micron filter and a large cannula (18-20 G). Do not add drugs or any fluid except normal saline to the blood. Dextrose and Ringer's lactate cause clotting or haemolysis.
5. **Start slowly and observe.** Run the first 15 minutes at about 2 mL/min and stay with the patient, with a full set of vital signs at the start, at 15 minutes, hourly and at the end. Most severe reactions begin in the first 15 minutes. Increase the rate if all is well.
6. **Monitor the whole transfusion.** Record temperature, pulse, BP and respiration, look for rash and watch breathing, particularly in the old and those with heart or kidney disease. Each unit must run in under 4 hours. Document volume and times.
7. **Respond to reactions at once.** Stop the transfusion, keep the line open with saline, call the doctor, check vitals and send the bag and a new blood sample back to the blood bank. Give the drugs ordered. Never restart a stopped transfusion without a doctor's order.
8. **After the transfusion.** Flush the line with saline, record the end time, volume and vital signs, check the Hb as ordered and dispose of the used set as biohazard waste. Reassure the patient and teach to report a delayed reaction (fever, dark urine, yellow eyes) within days.

### Eight transfusion reactions: recognise and act

1. **Acute haemolytic reaction (ABO mismatch).** Fever, chills, back and chest pain, red-brown urine and low BP within minutes. Stop, support the circulation with fluid, keep the urine flowing and inform the blood bank.
2. **Febrile non-haemolytic reaction.** A rise of 1 °C or more with chills but no other signs, from antibodies to donor white cells. Stop, give paracetamol and let the doctor decide on restart.
3. **Allergic (urticarial) reaction.** Itching and hives with no other signs. Pause, give an antihistamine, and restart slowly only if the doctor allows.
4. **Anaphylaxis.** Wheeze, swelling of the throat, hypotension and collapse. Stop, call for help and give IM adrenaline 0.5 mg (0.5 mL of 1:1000) and oxygen.
5. **Transfusion-associated circulatory overload (TACO).** Breathlessness, cough and crackles in a patient with a weak heart, with a high JVP and BP. Sit upright, give oxygen and furosemide, and slow the next unit.
6. **Transfusion-related acute lung injury (TRALI).** Sudden severe breathlessness and non-cardiac pulmonary oedema within 6 hours. Stop, give oxygen and call the ICU team.
7. **Bacterial contamination.** High fever, rigors and shock, especially with platelets. Stop, culture the bag and the patient, and start broad antibiotics.
8. **Metabolic effects of massive transfusion.** Citrate lowers calcium and cold blood lowers temperature and raises potassium. Warm the blood, monitor ECG and calcium, and give calcium as ordered.

## Formula and fact sheet

- MCV = Hct × 10 ÷ RBC; MCH = Hb × 10 ÷ RBC; MCHC = Hb × 100 ÷ Hct; corrected reticulocytes = retic % × Hct ÷ 45; ANC = WBC × neutrophil % ÷ 100.
- Ganzoni iron deficit (mg) = weight × (target Hb - actual Hb) × 2.4 + 500; ferrous sulphate 200 mg = 65 mg elemental iron.
- BSA (Mosteller) = √(height × weight ÷ 3600); factor VIII dose (IU) = weight × % rise × 0.5.
- One red-cell unit raises Hb by about 1 g/dL (70 kg); first 15 minutes 2 mL/min; finish each unit within 4 hours; stop the transfusion first in any reaction.

## Chapter summary

- The blood count and its indices classify anaemia; iron deficiency is the commonest type in Nepal and is treated with iron, vitamin C and removal of the cause.
- Sickle cell disease and thalassaemia are inherited; hydration, pain relief, transfusion with chelation and genetic counselling are key.
- Leukaemia care protects from infection and bleeding, and handles cytotoxic drugs safely by BSA and double check.
- Transfusion safety rests on two-person identity checks, a slow start, close observation and an immediate stop when a reaction occurs.

## Practice

**MCQs (with reasons)**

1. A patient has Hct 30% and RBC 4.0 million/µL. The MCV is: (a) 7.5 fL (b) 75 fL (c) 120 fL (d) 133 fL.
2. 300 mL of blood over 3 hours with a 15 gtt/mL set runs at: (a) 15 gtt/min (b) 25 gtt/min (c) 50 gtt/min (d) 100 gtt/min.
3. A 60-kg patient with haemophilia A needs a 40% rise in factor VIII: the dose is: (a) 600 IU (b) 1,200 IU (c) 2,400 IU (d) 4,800 IU.
4. A WBC of 3,000 with 10% neutrophils gives an ANC of: (a) 30 (b) 300 (c) 1,000 (d) 2,700.
5. The first action when a transfusion reaction is suspected is: (a) give paracetamol (b) stop the transfusion (c) increase the rate (d) call the relatives.

::: note Answers and rationales
**1. (b).** MCV = 30 × 10 ÷ 4.0 = 75 fL, a microcytic cell (below 80); (d) inverts the ratio.
**2. (b).** 300 ÷ 3 = 100 mL/h; 100 × 15 ÷ 60 = 25 gtt/min; (d) forgets the drop factor.
**3. (b).** 60 × 40 × 0.5 = 1,200 IU; (c) omits the 0.5 factor.
**4. (b).** 3,000 × 10 ÷ 100 = 300, which is severe neutropenia (below 500); (d) uses the lymphocyte percentage.
**5. (b).** Stopping the transfusion limits the dose of incompatible or contaminated blood; drugs and calls follow, and increasing the rate is dangerous.
:::

**Short answer (3 marks): Iron deficiency anaemia.** It is anaemia from lack of iron due to poor diet, blood loss, hookworm or increased need. The red cells are small and pale (low MCV and MCHC) with low ferritin. Treatment is ferrous sulphate with vitamin C for 3 months after the Hb is normal, treating the cause, and a diet with green leaves, pulses and meat.

**Medium answer (5 marks): Describe the nursing care of a patient receiving a blood transfusion (Figure 5.4).** Check the order and consent and record the baseline vitals and Hb. Two nurses verify the patient's name, number, group, unit number and expiry at the bedside. Use a fresh blood set with a filter and a large cannula and no drugs in the line. Start at 2 mL/min for 15 minutes beside the patient, then increase to finish in under 4 hours, with vitals at 15 minutes and hourly. If there is fever, rash, breathlessness or back pain, stop the blood, keep the line open with saline, call the doctor and send the bag and a sample to the blood bank. Document everything.

**Long answer (10 marks): Mrs Maya Devi Chaudhary, 35 years, 50 kg, from the Terai, has had tiredness, breathlessness on walking and palpitations for two months, heavy periods and a diet of rice and dal. She has pale conjunctivae, koilonychia, pulse 112, BP 100/60 and SpO2 96%. Hb 6.0 g/dL, Hct 20%, RBC 3.1 million/µL. Plan her care.**

*Calculations.* **MCV = 64.5 fL, MCH = 19.4 pg and MCHC = 30.0 g/dL**: microcytic hypochromic anaemia of iron deficiency. Her **iron deficit is 50 × (12 - 6) × 2.4 + 500 = 1,220 mg**. A unit of red cells raises her Hb by about 70 ÷ 50 = **1.4 g/dL**, so with a target of 8 g/dL one unit is given and she is reassessed. A 350-mL unit over 3.5 hours runs at 100 mL/h, which is 25 gtt/min on a 15 gtt/mL set, and the first 15 minutes are given at 2 mL/min (**30 mL**) beside her.

*Care.* Because she is symptomatic with a tachycardia, she is transfused with one unit of crossmatched red cells after consent and identity check by two nurses. Vital signs are taken before, at 15 minutes, hourly and at the end. She is started on ferrous sulphate 200 mg three times a day (**195 mg elemental iron**) with citrus juice, deworming with albendazole 400 mg, and the cause of her heavy periods is investigated by the gynaecologist. Teach her to avoid tea with meals and eat green leaves, pulses and egg, to expect black stools and to attend the health post for follow-up Hb at 4 weeks and monthly for 3 months. She is advised to rest and rise slowly. The family is taught to recognise delayed reactions.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "I get breathless walking." **O:** Hb 6.0, pulse 112, pallor. | **Ineffective peripheral tissue perfusion** related to decreased haemoglobin, as evidenced by pallor and tachycardia. | **Tissue perfusion:** pulse below 100 and no breathlessness at rest after transfusion. | 1. One unit of cross-matched blood with the correct check; *restores oxygen carriage.* 2. Vitals before, at 15 minutes, hourly; *detect reaction early.* 3. Oxygen if SpO2 below 94%; *supports tissues.* | Pulse 92, Hb 7.5 after the unit. |
| **S:** "I am tired all day." **O:** koilonychia, pale. | **Activity intolerance** related to imbalance of oxygen supply and demand. | **Energy conservation:** walks 50 m without breathlessness before discharge. | 1. Pace activity with rests; *saves oxygen.* 2. Assist when rising; *prevents falls.* 3. Increase activity step by step; *builds tolerance.* | Walks 50 m with SpO2 above 94%. |
| **O:** rice-dal diet, heavy menses, BMI 19. | **Imbalanced nutrition: less than body requirements** related to inadequate iron intake. | **Nutritional status: iron:** states 5 iron-rich foods and takes iron daily. | 1. Teach iron-rich foods, vitamin C and tea restriction; *improves absorption.* 2. Give iron and explain black stool; *supports compliance.* 3. Deworm; *removes blood loss.* | Names 5 foods; Hb 9.5 at 4 weeks. |
| **S:** "I have never had blood before." **O:** anxious. | **Risk for adverse reaction to transfusion** related to blood component exposure. | **Safe transfusion:** no reaction recorded. | 1. Double identity check; *prevents ABO error.* 2. Stay for the first 15 minutes; *most severe reactions start then.* 3. Stop and report symptoms at once; *limits harm.* | No reaction; unit completed in 3.5 hours. |

::: tip Exam tip
For an anaemia case write the indices, the iron deficit, the transfusion rate and the first 15 minutes, the two-nurse check, and four NANDA-I diagnoses beginning with ineffective tissue perfusion and activity intolerance.
:::
