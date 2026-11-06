---
subject: Adult Nursing II
grade: BSc Nursing Year 2
unit: 2
title: Endocrine Nursing: Diabetes Mellitus, Insulin, DKA, Diabetic Foot and Thyroid Disorders
hours: 20
area: BSN 10 · Adult Nursing II · Unit 2
---

Diabetes is now a ward disease and a village disease in Nepal. The **STEPS survey 2019 found raised blood sugar in about 6% of adults aged 15-69, and about 9-10% of those aged 45-69**, and many of them were never diagnosed. The Package of Essential Non-communicable Disease (**PEN**) programme of the **MoHP** trains health workers at the primary level to screen adults over 40 for blood sugar and blood pressure, and the nurse in a health post, a PHCC or a hospital teaches insulin technique, foot care and diet. Diabetes causes blindness, kidney failure, amputations and heart attacks, so good control and education prevent a great deal of suffering. All arithmetic in this unit is checked by program.

::: key What this unit gives you
- Real photographs of an insulin pen with its parts labelled, a patient giving a pen injection, a neuropathic heel ulcer and a patient with thyroid eye disease (Graves), plus four SVG figures.
- Diagnosis, HbA1c to average glucose, BMI, insulin total daily dose, correction factor, carbohydrate ratio, DKA numbers and the diabetic foot (ABI).
- Eight points each on insulin injection care, DKA/hypoglycaemia care, diabetic foot education and thyroidectomy care.
- Model answers and a NANDA-I care plan for a woman with type 2 diabetes and a foot ulcer.
:::

## 2.1 Diabetes mellitus: types, diagnosis and the numbers

**Diabetes mellitus** is a group of diseases with high blood glucose from a lack of insulin or its poor action. **Type 1** (autoimmune destruction of beta cells; children and young adults; needs insulin from the start), **type 2** (insulin resistance and a relative lack; adults, overweight, family history; most cases), **gestational diabetes** (first found in pregnancy) and secondary diabetes (pancreatitis, steroids). The classic symptoms are **polyuria, polydipsia, polyphagia and weight loss**, with tiredness, blurred vision, recurrent infections and slow healing wounds. The diagnosis needs one of: **fasting plasma glucose 126 mg/dL (7.0 mmol/L) or more**, a **2-hour glucose 200 mg/dL (11.1 mmol/L) or more** in an OGTT with 75 g of glucose, **HbA1c 6.5% or more**, or a random glucose of 200 mg/dL or more with symptoms. A fasting glucose of 100-125 or HbA1c of 5.7-6.4% is **prediabetes**. Most adults aim for an HbA1c below 7% and individual targets for older or frail people.

```python
a1c = 8.0                                        # HbA1c %
eag = 28.7 * a1c - 46.7                          # estimated average glucose mg/dL
wt, ht = 78, 1.65
bmi = wt / ht ** 2
tdd = 0.5 * 70                                   # total daily insulin, 0.5 unit/kg, 70 kg
basal = tdd / 2; bolus = (tdd - basal) / 3       # 50% basal, rest in three meals
cf = 1800 / tdd; corr = (250 - 120) / cf         # correction factor, glucose 250, target 120
icr = 500 / tdd; meal = 60 / icr                 # carbohydrate ratio, 60 g meal
print(f"HbA1c {a1c}% -> eAG = 28.7 x {a1c} - 46.7 = {eag:.0f} mg/dL = {eag/18:.1f} mmol/L")
print(f"BMI = {wt} / {ht}^2 = {bmi:.1f} kg/m2 (overweight; Asian cut-off 23, obese 27.5)")
print(f"Total daily dose = 0.5 x 70 = {tdd:.0f} units; basal {basal:.1f}, each meal {bolus:.1f}")
print(f"Correction factor = 1800 / {tdd:.0f} = {cf:.1f} mg/dL per unit; glucose 250 to target 120: {corr:.1f} units")
print(f"Carbohydrate ratio = 500 / {tdd:.0f} = {icr:.1f} g per unit; 60 g meal needs {meal:.1f} units")
```

```text
HbA1c 8.0% -> eAG = 28.7 x 8.0 - 46.7 = 183 mg/dL = 10.2 mmol/L
BMI = 78 / 1.65^2 = 28.7 kg/m2 (overweight; Asian cut-off 23, obese 27.5)
Total daily dose = 0.5 x 70 = 35 units; basal 17.5, each meal 5.8
Correction factor = 1800 / 35 = 51.4 mg/dL per unit; glucose 250 to target 120: 2.5 units
Carbohydrate ratio = 500 / 35 = 14.3 g per unit; 60 g meal needs 4.2 units
```

An HbA1c of 8.0% means that the average blood glucose over about 3 months was **183 mg/dL (10.2 mmol/L)**. A woman or man of 78 kg and 1.65 m has a **BMI of 28.7**, which is obese by the Asian cut-off of 27.5. For a 70 kg adult on a total dose of 0.5 unit/kg the **total daily dose is 35 units**; half (**17.5 units**) is basal and the rest is split into three meal doses of **5.8 units**. The correction factor (1800 rule) is **51.4 mg/dL per unit**, so a glucose of 250 mg/dL with a target of 120 needs **2.5 units**. The carbohydrate ratio (500 rule) is **14.3 g per unit**, so a 60 g meal needs **4.2 units**. These are teaching examples; the doctor prescribes the actual dose and the nurse checks it against the chart and the glucose before giving it.

## 2.2 Insulin and oral drugs

**Metformin** (first-line in type 2; stop when eGFR is below 30 or before contrast and in sepsis), **sulphonylureas** (gliclazide, glimepiride: risk of hypoglycaemia), **DPP-4 inhibitors**, **SGLT2 inhibitors** (empagliflozin, dapagliflozin: also protect heart and kidney; risk of genital infection and ketoacidosis) and **GLP-1 agonists** are the main non-insulin drugs. **Insulin** is needed in type 1, in gestational diabetes not controlled by diet, in DKA, in surgery and in type 2 when drugs fail. Nepal's hospitals use human insulin (regular and NPH vials, 40 or 100 units/mL) and insulin analogue pens in many private and referral centres. **Always check the strength: a 40 units/mL vial needs a U-40 syringe and a 100 units/mL vial a U-100 syringe.**

```svgfig label="2.1" caption="Insulin action profiles as bars: onset (light), peak (dark) and total duration (line), in hours after injection. Rapid-acting analogues start in 10-20 minutes and are given just before meals; regular insulin starts in 30-60 minutes and is given 30 minutes before a meal; NPH peaks at 4-10 hours (the risk time for night hypoglycaemia); long-acting glargine has almost no peak and lasts about 24 hours."
f = Fig(760, 250)
f.text(60, 18, "Hours after injection", size=11, color=NAVY, bold=True, anchor="start")
for h in range(0, 25, 4):
    x = 190 + h * 23
    f.line(x, 28, x, 200, color="#cbd5e1", sw=1); f.text(x, 214, str(h), size=10.5, color=SLATE)
rows = [("Rapid (aspart, lispro)", 0.3, 1, 3, 5, BLUE, NAVY), ("Regular (soluble)", 0.5, 2, 4, 8, SAND, AMBER), ("NPH (isophane)", 1.5, 4, 10, 16, MINT, TEAL), ("Glargine (long)", 1.5, 2, 3, 24, ROSE, RED)]
for i, (n, on, p0, p1, d, fl, st) in enumerate(rows):
    y = 36 + i * 40
    f.text(180, y + 12, n, size=11, color=st, bold=True, anchor="end")
    f.line(190 + on * 23, y + 12, 190 + d * 23, y + 12, color=st, sw=2.5)
    f.box(190 + p0 * 23, y + 2, (p1 - p0) * 23, 20, "peak" if i < 3 else "flat", fill=fl, stroke=st, size=10, bold=True)
f.text(380, 240, "Give rapid insulin with meals; never skip basal insulin, even when not eating", size=11, color=NAVY, bold=True)
```

```photogrid label="2.2" cols="4" ratio="1.0" caption="Endocrine nursing. (a) A real insulin pen (premixed NovoMix 30 FlexPen) with labels for its parts. (b) A real patient holding a pen injector against the skin to inject. (c) A real neuropathic ulcer on the heel of a diabetic patient, held in a gloved hand. (d) A real patient with Graves' disease: the eyelids are retracted and the eyes bulge (exophthalmos)."
@ photo id="nur6/pen" cap="Insulin pen"
fit 1.0
focus 0.5 0.5
mark 0.50 0.93 "1"
mark 0.50 0.17 "2"
key 1 (a) Needle end (tip): a fresh needle is attached for every injection
key 2 (a) Dose display and button: dial the units, then press and count to 10
@ photo id="nur6/inj" cap="Pen injection"
fit 1.0
focus 0.5 0.5
mark 0.42 0.82 "3"
mark 0.50 0.15 "4"
key 3 (b) Needle end: pinch the skin, insert at 90 degrees for a short needle
key 4 (b) Thumb on the button: hold for 10 seconds before withdrawing the needle
@ photo id="nur6/dfu" cap="Neuropathic heel ulcer"
fit 1.0
focus 0.55 0.5
mark 0.46 0.52 "5"
mark 0.82 0.85 "6"
key 5 (c) Ulcer on the pressure point of the heel: a painless wound in a numb foot
key 6 (c) Gauze: the wound is cleaned, debrided and offloaded; no weight-bearing on it
@ photo id="nur6/graves" cap="Graves' eye disease"
fit 1.0
focus 0.5 0.5
mark 0.27 0.60 "7"
mark 0.77 0.46 "8"
key 7 (d) Lid retraction: white sclera is visible above the iris
key 8 (d) Exophthalmos: forward bulging of the eyeball from tissue swelling behind it
```

### Insulin therapy: eight points of nursing responsibility

1. **Check the six rights and the glucose first.** Verify the patient, drug, dose, time, route and the written order, and check that the capillary glucose was taken just before. Two nurses should check high-risk insulin doses. A wrong unit scale or a missed decimal can kill.
2. **Use the right insulin and syringe.** Read the label for the type and the strength (40 or 100 units/mL) and use the matching syringe or pen. Never use a normal 1 mL syringe to measure units. Write "units" in full, never "U".
3. **Prepare it correctly.** Roll cloudy insulin (NPH) gently between the palms 10 times, because shaking makes bubbles and uneven doses. When mixing, draw up clear (regular) first and then cloudy (NPH). Never mix glargine with other insulins.
4. **Choose and rotate the site.** Use the abdomen (fastest absorption), thighs or upper arms, and keep 2-3 cm from the navel. Change the spot within the area every day. Using the same spot causes lumps (lipohypertrophy), which absorb insulin badly.
5. **Inject with the correct technique.** Clean the skin with spirit and let it dry. Use a 4-6 mm needle at 90 degrees; pinch the skin only for thin patients or longer needles. Press the button, count to 10 and then withdraw.
6. **Time the dose with food.** Give rapid insulin just before a meal and regular insulin 30 minutes before. Make sure the meal is on its way, because a dose without food causes hypoglycaemia. Hold and call the doctor if the patient is nil by mouth or vomiting.
7. **Store and dispose safely.** Keep unopened insulin in the refrigerator (2-8 °C, never frozen) and an opened vial or pen at room temperature for 28 days. In hot places use a clay pot or a cool bag. Put used needles into a sharps container or a cut plastic bottle.
8. **Teach and watch for hypoglycaemia.** Teach the patient and the family to give the injection, to measure sugar, to recognise sweating, shaking and hunger, and to act with 15 g of sugar. Keep a glucose log. Review technique at every visit.

## 2.3 Acute complications: DKA, HHS and hypoglycaemia

**Diabetic ketoacidosis (DKA)** occurs mostly in type 1 diabetes, when a missed insulin dose, infection or surgery leaves the body with too little insulin. Cells cannot use glucose, so fat is broken down into **ketones (acids)**, the blood glucose rises (usually above 250 mg/dL), the pH falls below 7.3 and the bicarbonate below 18. Glucose and ketones pull water and salts into the urine, causing dehydration with a potassium deficit. The patient has thirst, polyuria, abdominal pain, vomiting, **deep sighing (Kussmaul) breathing**, a fruity smell and drowsiness. **Hyperosmolar hyperglycaemic state (HHS)** occurs in older type 2 patients with a glucose above 600 mg/dL, severe dehydration and no ketones. **Hypoglycaemia** is a glucose below 70 mg/dL (below 54 is serious) and is the commonest emergency of treated diabetes.

```python
na, cl, hco3, glu = 130, 94, 8, 600              # mmol/L, mmol/L, mmol/L, mg/dL
ag = na - (cl + hco3)
cna = na + 1.6 * (glu - 100) / 100               # sodium corrected for glucose
osm = 2 * na + glu / 18
wt = 70; ins = 0.1 * wt                          # insulin 0.1 unit/kg/h
rate = ins / 50 * 50                             # 50 units in 50 mL syringe: mL/h
gtt = 1000 * 20 / (2 * 60)                       # 1 litre over 2 h, 20 gtt/mL set
d50 = 50 * 50 / 100; d10 = 150 * 10 / 100        # grams of glucose given
print(f"Anion gap = {na} - ({cl} + {hco3}) = {ag} (normal 8-12): high-gap acidosis")
print(f"Corrected sodium = {na} + 1.6 x ({glu} - 100)/100 = {cna:.0f} mmol/L")
print(f"Effective osmolality = 2 x {na} + {glu}/18 = {osm:.1f} mOsm/kg")
print(f"Insulin 0.1 x {wt} = {ins:.1f} units/h = {rate:.0f} mL/h from 50 units in 50 mL")
print(f"1 L saline over 2 h at 20 gtt/mL = {gtt:.0f} gtt/min ({round(gtt)})")
print(f"50 mL of 50% dextrose = {d50:.0f} g; 150 mL of 10% dextrose = {d10:.0f} g")
```

```text
Anion gap = 130 - (94 + 8) = 28 (normal 8-12): high-gap acidosis
Corrected sodium = 130 + 1.6 x (600 - 100)/100 = 138 mmol/L
Effective osmolality = 2 x 130 + 600/18 = 293.3 mOsm/kg
Insulin 0.1 x 70 = 7.0 units/h = 7 mL/h from 50 units in 50 mL
1 L saline over 2 h at 20 gtt/mL = 167 gtt/min (167)
50 mL of 50% dextrose = 25 g; 150 mL of 10% dextrose = 15 g
```

The patient with sodium 130, chloride 94 and bicarbonate 8 has an **anion gap of 28**, a severe high-gap metabolic acidosis; the sodium corrected for a glucose of 600 is **138 mmol/L**, so the true sodium is normal. The effective osmolality is **293.3 mOsm/kg**. In a 70 kg patient the fixed-rate insulin infusion of 0.1 unit/kg/h is **7 units/h**, which equals **7 mL/h** when 50 units of regular insulin are made up to 50 mL. One litre of saline over 2 hours on a 20 gtt/mL set is **167 gtt/min**. For hypoglycaemia, 50 mL of 50% dextrose gives **25 g** of glucose and 150 mL of 10% dextrose gives **15 g**.

```svgfig label="2.3" caption="How insulin deficiency produces DKA, and where nursing care acts. No insulin leads to high glucose and fat breakdown to ketones; osmotic diuresis dehydrates and removes potassium; ketone acids lower the pH and cause Kussmaul breathing. Treatment: fluids first, then insulin, with potassium replacement, glucose and ketone monitoring every hour and finding the cause."
f = Fig(760, 270)
f.box(10, 100, 120, 60, "Insulin deficiency\n(missed dose, infection)", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(180, 30, 150, 56, "Glucose cannot enter\ncells: glucose above\n250 mg/dL", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(180, 175, 150, 56, "Fat breakdown:\nketones (acids)\nbicarbonate falls", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(385, 30, 160, 56, "Osmotic diuresis:\nwater, sodium and\npotassium lost", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(385, 175, 160, 56, "Acidosis: pH below 7.3,\nKussmaul breathing,\nvomiting", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(595, 100, 155, 60, "Dehydration, shock,\ncoma, arrhythmia", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.arrow([(130, 115), (180, 60)], sw=1.8); f.arrow([(130, 145), (180, 200)], sw=1.8)
f.arrow([(330, 58), (385, 58)], sw=1.8); f.arrow([(330, 203), (385, 203)], sw=1.8)
f.arrow([(545, 58), (595, 120)], sw=1.8); f.arrow([(545, 203), (595, 140)], sw=1.8)
f.text(380, 130, "Treat: 1 fluids, 2 insulin 0.1 unit/kg/h, 3 potassium, 4 find the cause", size=11, color=TEAL, bold=True)
```

### DKA and hypoglycaemia: eight points of nursing care

1. **Secure the airway and breathing.** Put the drowsy patient on the side, give oxygen if the SpO2 is low and monitor the breathing rate. Vomiting with a low level of consciousness risks aspiration. Place a nasogastric tube if needed.
2. **Start fluids at once.** Insert two large IV lines and give 0.9% sodium chloride as ordered (about 1 litre in the first 1-2 hours, then slower). Fluids lower the glucose and restore the circulation. Chart the intake and the hourly urine output.
3. **Give insulin by infusion.** A fixed rate of 0.1 unit/kg/h is given by a syringe pump after the first fluid and the potassium check. Use only regular insulin and label the syringe. Do not stop the insulin when the glucose falls; add glucose instead until the ketones clear.
4. **Replace potassium.** Insulin drives potassium into cells and can cause fatal hypokalaemia. Add potassium to the fluid once the level is below 5.5 mmol/L and urine is passing. Monitor the ECG for flat T waves and U waves.
5. **Monitor often.** Check the glucose and ketones hourly, the electrolytes and blood gas every 2-4 hours, and BP, pulse, temperature and the level of consciousness. Use a chart. A fall in glucose faster than 90 mg/dL per hour risks cerebral oedema.
6. **Find and treat the cause.** Look for infection, missed insulin, a heart attack or stress, and send cultures. Give antibiotics as ordered. Ask why the insulin was missed (cost, fear, illness).
7. **In hypoglycaemia: the 15-15 rule.** If the patient is awake, give 15 g of fast carbohydrate (3 teaspoons of sugar in water, half a glass of juice), recheck in 15 minutes and repeat. An unconscious patient receives IV dextrose or IM glucagon; follow with a meal.
8. **Teach sick-day rules.** Never stop insulin when ill, drink fluids, test glucose and ketones every 4 hours, and seek help for vomiting or sugar above 250 mg/dL. Teach the family the signs of hypoglycaemia. Carry sugar and an identity card.

## 2.4 Chronic complications and the diabetic foot

High glucose damages small vessels (**microvascular**: retinopathy, nephropathy, neuropathy) and large vessels (**macrovascular**: heart attack, stroke, peripheral arterial disease). Yearly eye examination, urine albumin, creatinine, foot examination, blood pressure and lipids are routine in Nepal's PEN and in hospital diabetes clinics. The **diabetic foot** is a main cause of non-traumatic amputation: neuropathy removes pain, so a blister or a nail goes unnoticed (Plate 2.2c); arterial disease slows healing; infection spreads. The **Wagner grade** describes depth: 0 skin intact but at risk, 1 superficial ulcer, 2 deep ulcer to tendon or joint, 3 abscess or osteomyelitis, 4 gangrene of the toes, 5 gangrene of the whole foot. The **ankle-brachial index (ABI)** is the ankle systolic pressure divided by the arm systolic pressure: with an ankle pressure of 90 and an arm pressure of 120 the ABI is 90 / 120 = **0.75**, which means mild-to-moderate arterial disease (normal 1.0-1.4; below 0.9 is abnormal; below 0.4 is critical).

### Diabetic foot: eight points of health education

1. **Look at both feet every day.** Use a mirror or ask a family member to check the soles, heels and between the toes for blisters, cracks, redness and cuts. Numb feet do not hurt, so the eye must do the work. Report any wound the same day.
2. **Wash and dry carefully.** Wash in lukewarm water, test the water with the elbow and dry between the toes. Apply moisturiser to the soles but not between the toes. Hot water bottles and hot water cause burns.
3. **Never walk barefoot.** Wear shoes or sandals with a closed toe and a soft sole, even inside the house and on the village path. A thorn or stone can start an ulcer. Shake out the shoes before wearing.
4. **Choose shoes and socks well.** Buy shoes in the afternoon when the feet are largest, and choose a broad toe box. Wear clean cotton socks without tight elastic. Avoid sandals with a strap between the toes.
5. **Cut the nails straight.** Trim straight across and file the edges; do not cut corns or calluses with a blade and do not use chemical corn cures. Ask the nurse or podiatrist to treat thick nails and calluses. Cutting causes ulcers.
6. **Keep the glucose in target.** High sugar slows healing and feeds infection. Take drugs and insulin regularly, eat the planned diet and keep the HbA1c under 7% if the doctor advises. Good control reduces the risk of ulcers.
7. **Stop smoking and exercise.** Tobacco narrows the arteries and doubles the risk of amputation. Walking 30 minutes daily improves circulation if the feet are protected. Raise the feet when sitting.
8. **Act quickly for a wound.** Cover with a clean dry dressing, rest the foot and see a doctor or nurse within 24 hours, since an infected ulcer can spread in days. Take off weight with a cast or special shoe as advised. Come for follow-up until healed.

## 2.5 Thyroid and adrenal disorders

The **hypothalamus** releases TRH, the **pituitary** releases TSH and the **thyroid** releases T4 and T3, which act on nearly every cell and feed back to switch off TRH and TSH. **Hyperthyroidism** (most often **Graves' disease**; also toxic nodular goitre) causes weight loss with a good appetite, heat intolerance, sweating, palpitations, tremor, diarrhoea, anxiety, a goitre and in Graves' disease eye signs (Plate 2.2d). TSH is low and free T4 is high. Treatment is carbimazole or propylthiouracil, propranolol for symptoms, radioiodine or surgery; **thyroid storm** (fever above 38.5 °C, heart rate above 140, agitation, delirium) is an emergency treated with cooling, fluids, propranolol, antithyroid drugs and steroids. **Hypothyroidism** (Hashimoto's thyroiditis, iodine deficiency, after surgery) causes tiredness, cold intolerance, weight gain, constipation, dry skin, slow pulse and a hoarse voice; TSH is high. It is treated by **levothyroxine**, usually about 1.6 µg/kg/day, so a 60 kg adult needs **96 µg** a day, given on an empty stomach, 30-60 minutes before breakfast. **Myxoedema coma** is the extreme state with hypothermia, bradycardia and coma; give IV levothyroxine and hydrocortisone and warm the patient slowly. Goitre is still seen in the hills of Nepal despite salt iodisation (30 ppm), and the nurse supports the National Iodine Deficiency Disorders programme and teaches the family to buy iodised salt in a sealed packet.

```svgfig label="2.4" caption="The hypothalamic-pituitary-thyroid axis. TRH from the hypothalamus drives TSH from the pituitary, which drives thyroid hormones T4 and T3. Rising T4 and T3 inhibit TRH and TSH (negative feedback). In Graves' disease antibodies mimic TSH, so thyroid hormone is high and TSH is low; in primary hypothyroidism the thyroid fails, so T4 is low and TSH is high."
f = Fig(760, 230)
f.box(20, 85, 150, 60, "Hypothalamus\nreleases TRH", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(230, 85, 150, 60, "Pituitary\nreleases TSH", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(440, 85, 150, 60, "Thyroid gland\nmakes T4 and T3", fill=MINT, stroke=TEAL, size=11, bold=True)
f.box(630, 85, 120, 60, "Body cells:\nmetabolic rate", fill=ROSE, stroke=RED, size=11, bold=True)
f.arrow([(170, 115), (230, 115)], sw=2); f.arrow([(380, 115), (440, 115)], sw=2); f.arrow([(590, 115), (630, 115)], sw=2)
f.arrow([(515, 85), (515, 30), (95, 30), (95, 85)], sw=1.8, dash=True, color=RED)
f.text(300, 20, "Negative feedback: high T4 switches off TRH and TSH", size=11, color=RED, bold=True)
f.box(20, 175, 350, 44, "Graves: T4 high, TSH low; weight loss, tremor, heat intolerance", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(395, 175, 355, 44, "Hypothyroid: T4 low, TSH high; weight gain, cold, slow pulse", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
```

### Thyroidectomy: eight points of post-operative nursing care

1. **Airway first.** Keep a tracheostomy set and suction at the bedside for the first 24 hours. Swelling or a haematoma can press on the trachea and cause stridor. Nurse the patient in a semi-Fowler position.
2. **Check the neck for bleeding.** Look at the dressing and behind the neck, since blood runs backward when the patient lies flat. Increasing swelling, tightness or difficulty in swallowing is an emergency. Keep clip or suture removers for the surgeon to open the wound.
3. **Support the head and neck.** Use pillows or sandbags on both sides, and teach the patient to hold the neck with the hands when moving or coughing. Avoid hyperextension, which strains the sutures. Early gentle movement of the neck follows the surgeon's advice.
4. **Observe the voice.** Ask the patient to speak at each visit; hoarseness or a weak voice suggests injury to the recurrent laryngeal nerve. Report it and encourage voice rest. Most changes recover over weeks.
5. **Watch for hypocalcaemia.** Damage or removal of the parathyroid glands lowers calcium within 24-72 hours, causing tingling around the mouth and in the fingers, muscle cramps and carpopedal spasm (Chvostek and Trousseau signs). Keep calcium gluconate 10 mL of 10% ready and report symptoms. Check the serum calcium as ordered.
6. **Watch for thyroid storm.** Before surgery for Graves' disease the patient is made euthyroid with drugs; a storm may still occur. Check temperature and pulse every 4 hours and report fever or tachycardia over 120. Give propranolol and cooling as ordered.
7. **Relieve pain and feed gradually.** Give analgesia, offer cool fluids when the swallowing is safe and add soft food afterwards. Cool drinks soothe the throat. Record the intake.
8. **Teach for home.** Teach lifelong levothyroxine after total thyroidectomy, regular blood tests, neck exercises, wound care, signs of low calcium and low thyroid hormone, and the need for follow-up. Counsel about the scar and its fading.

**Adrenal disorders.** **Cushing's syndrome** (excess cortisol, often from long-term steroid tablets) causes a moon face, central obesity, purple striae, high BP, high glucose, thin skin and weak bones; the nurse protects the skin, watches glucose and BP and teaches about infection. **Addison's disease** (cortisol deficiency) causes weight loss, fatigue, low BP, dark skin and low sodium; an **adrenal crisis** (shock, vomiting, confusion) is treated with hydrocortisone 100 mg IV at once, saline and glucose. **Never stop long-term steroid tablets suddenly**, and double the dose during fever or surgery on the doctor's advice.

## Formula and fact sheet

- Diagnosis: fasting glucose 126 mg/dL or more, 2 h OGTT 200 or more, HbA1c 6.5% or more; eAG = 28.7 × HbA1c − 46.7; BMI = kg ÷ m².
- Insulin: total daily dose about 0.5 unit/kg; correction factor = 1800 ÷ TDD; carbohydrate ratio = 500 ÷ TDD; a vial of 40 units/mL needs a U-40 syringe.
- DKA: anion gap = Na − (Cl + HCO3); corrected Na = Na + 1.6 × (glucose − 100) ÷ 100; insulin 0.1 unit/kg/h; hypoglycaemia below 70 mg/dL, 15 g of sugar, recheck in 15 minutes.
- ABI = ankle systolic ÷ arm systolic; below 0.9 abnormal; levothyroxine about 1.6 µg/kg/day.

## Chapter summary

- Diabetes is diagnosed by glucose or HbA1c and controlled by diet, exercise, drugs and insulin; the nurse checks the dose, the site and the food before every injection.
- DKA is treated in order: fluids, insulin, potassium, cause; hypoglycaemia is treated at once with 15 g of sugar or IV dextrose.
- The diabetic foot is prevented by daily inspection, proper shoes, nail care and good control; ABI and Wagner grade guide treatment.
- Thyroid disease is a feedback problem: high T4 with low TSH is Graves' disease, low T4 with high TSH is hypothyroidism; thyroidectomy care watches airway, bleeding, voice and calcium.

## Practice

**MCQs (with reasons)**

1. An HbA1c of 7.0% corresponds to an average glucose of about: (a) 100 mg/dL (b) 126 mg/dL (c) 154 mg/dL (d) 200 mg/dL.
2. A patient has sodium 140, chloride 104 and bicarbonate 24 mmol/L. The anion gap is: (a) 8 (b) 12 (c) 16 (d) 28.
3. A 60 kg patient in DKA is ordered insulin at 0.1 unit/kg/h. The rate is: (a) 0.6 units/h (b) 3 units/h (c) 6 units/h (d) 60 units/h.
4. Levothyroxine 1.6 µg/kg/day is ordered for a 50 kg woman. The dose is: (a) 32 µg (b) 50 µg (c) 80 µg (d) 160 µg.
5. In DKA the correct order of treatment is: (a) insulin, fluid, potassium (b) fluids, insulin with potassium monitoring, then find the cause (c) bicarbonate first (d) oral sugar and rest.

::: note Answers and rationales
**1. (c).** 28.7 × 7.0 − 46.7 = 154 mg/dL; 126 mg/dL is the fasting diagnostic value, not the average, and 200 mg/dL corresponds to an HbA1c near 8.6%.
**2. (b).** 140 − (104 + 24) = 12, which is normal (8-12); 28 would be the answer in DKA.
**3. (c).** 0.1 × 60 = 6 units/h; (b) uses 0.05 unit/kg/h and (d) forgets the factor of 0.1.
**4. (c).** 1.6 × 50 = 80 µg; (d) is a tenfold error and (a) uses 0.64 µg/kg.
**5. (b).** Dehydration is the first danger, so fluids start first; insulin goes on after the first fluid and a potassium check, and bicarbonate is rarely needed; oral sugar worsens ketoacidosis.
:::

**Short answer (3 marks): Hypoglycaemia and its treatment.** It is a blood glucose below 70 mg/dL, with sweating, shaking, hunger, palpitations, confusion and, if severe, fits and coma. A conscious patient receives 15 g of quick sugar (three teaspoons in water) and the glucose is rechecked in 15 minutes; an unconscious patient receives 50 mL of 50% dextrose (25 g) IV or IM glucagon, followed by a meal. Find the cause (extra insulin, missed meal, exercise).

**Medium answer (5 marks): Describe the nursing care of a patient with diabetic ketoacidosis (Figure 2.3).** *Airway and monitoring:* position on the side, give oxygen if the SpO2 is low and put on the cardiac monitor. *Fluids:* two IV lines, 0.9% saline about 1 litre in the first hour, then reduced; chart the hourly urine. *Insulin:* a fixed infusion of 0.1 unit/kg/h, regular insulin only, for example 7 units/h (7 mL/h from 50 units in 50 mL) for a 70 kg patient. *Potassium:* add as ordered when it is below 5.5 mmol/L and urine is passing. *Monitor:* glucose and ketones hourly, electrolytes and blood gas every 2-4 hours, and the level of consciousness. *Cause and teaching:* treat infection, ask why insulin was missed and teach sick-day rules and hypoglycaemia recognition.

**Long answer (10 marks): Mrs Sita Gurung, 55 years, a shopkeeper from Pokhara, has had type 2 diabetes for 12 years. She weighs 68 kg and is 1.55 m tall. Her HbA1c is 9.4% and blood glucose today is 340 mg/dL. She has had a painless ulcer on the right heel for 3 weeks that is deep to the tendon (Wagner grade 2), with an ankle systolic pressure of 95 and an arm systolic pressure of 125 mmHg. Calculate the values and write the nursing care plan.**

*Calculations.* Her estimated average glucose is 28.7 × 9.4 − 46.7 = **223 mg/dL**, so the control is poor. Her BMI is 68 ÷ 1.55² = **28.3 kg/m²** (obese for Asians). Her estimated insulin total daily dose is 0.5 × 68 = **34 units**, the correction factor is 1800 ÷ 34 = **52.9 mg/dL per unit** and a correction for a glucose of 340 mg/dL to a target of 140 is 200 ÷ 52.9 = **3.8 units**. Her ABI is 95 ÷ 125 = **0.76**, a mild-to-moderate arterial disease.

*Care.* Admit and take the history; check capillary glucose before meals and at bedtime and give the prescribed insulin after checking the dose and the six rights. Take a swab or tissue culture and give antibiotics as ordered. The wound is cleaned with normal saline, dead tissue is removed (debridement) by the doctor, a moist dressing is applied and the heel is **offloaded** with a bed cradle and a pillow under the calf so that the heel floats. Check the pulses, colour and temperature of both feet each shift. Arrange an X-ray of the foot to look for osteomyelitis and refer to the surgeon for vascular assessment. Give a diabetic diet of about 1,500 kcal with a dietitian, with small meals of dal, vegetables and a controlled amount of rice. Teach her and the daughter about the eight foot-care points, insulin injection with the pen, hypoglycaemia and follow-up in the diabetes clinic. Stop smoking of tobacco in the family and encourage walking after healing.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "I did not feel it; it just would not heal." **O:** heel ulcer Wagner 2, 3 weeks, glucose 340. | **Impaired tissue integrity** related to neuropathy, pressure and impaired circulation, as evidenced by a deep heel ulcer. | **Wound healing: secondary intention:** ulcer smaller by 50% in 4 weeks with no infection. | 1. Clean with saline and apply a moist dressing daily; *keeps the bed moist and clean.* 2. Offload the heel with a pillow under the calf; *removes pressure so that tissue can heal.* 3. Assist debridement; *dead tissue delays healing.* 4. Measure and photograph weekly; *tracks progress.* | Ulcer 40% smaller at 3 weeks, pink granulation tissue. |
| **O:** HbA1c 9.4%, glucose 340 mg/dL, BMI 28.3. | **Unstable blood glucose level** (risk) related to inadequate insulin action and diet. | **Blood glucose level:** fasting 100-140 mg/dL within 3 days, no hypoglycaemia. | 1. Check glucose before meals and at bedtime; *guides doses.* 2. Give insulin on time after the six rights; *prevents swings.* 3. Diet of 1,500 kcal with fixed carbohydrate portions; *steady intake.* 4. Teach hypoglycaemia action (15 g sugar); *safety.* | Fasting 128 mg/dL on day 3. |
| **O:** ABI 0.76, foot pulses weak, smoker in the family. | **Ineffective peripheral tissue perfusion** related to peripheral arterial disease. | **Tissue perfusion: peripheral:** warm foot, palpable pulse, capillary refill under 3 s. | 1. Check pulses, colour, warmth every shift; *early warning of ischaemia.* 2. Keep the legs level, avoid elevation and tight dressings; *protects flow.* 3. Teach smoke-free home and daily walking; *improves flow.* 4. Refer to the vascular surgeon; *may need revascularisation.* | Capillary refill 3 seconds, no new ulcer. |
| **S:** "I never knew I should look at my feet." | **Deficient knowledge** (foot care and insulin) related to lack of exposure to information. | **Knowledge: diabetes management:** states 6 of 8 foot-care points and injects correctly by discharge. | 1. Teach the eight foot-care points with a mirror; *a daily look prevents ulcers.* 2. Return demonstration of pen injection; *confirms skill.* 3. Involve the daughter; *support at home.* 4. Written plan in Nepali and a follow-up date; *continuity.* | Gave 7 of 8 points and injected correctly on return demonstration. |

::: tip Exam tip
For a diabetes case write the eAG from HbA1c, the BMI, the insulin calculation with the six rights, Wagner grade with ABI, and four NANDA-I diagnoses starting with impaired tissue integrity and unstable blood glucose level.
:::
