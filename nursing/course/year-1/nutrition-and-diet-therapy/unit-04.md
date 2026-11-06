---
subject: Nutrition and Diet Therapy
grade: BSc Nursing Year 1
unit: 4
title: Therapeutic Diets: Diabetes, Hypertension, Kidney, Liver, Burns and Fever
hours: 14
area: BSN 8 · Nutrition and Diet Therapy · Unit 4
---

A **therapeutic diet** is a normal diet changed in energy, nutrient content, texture or timing to treat a disease. In Nepal the burden of non-communicable disease is rising: the NDHS 2022 found raised blood pressure in 18% of women and 23% of men aged 15 and over (about half of them unaware), and the MoHP **Package of Essential Non-Communicable Disease (PEN)** programme asks every health post to screen for diabetes and hypertension and to give diet advice. The nurse serves, explains and monitors these diets and must be able to turn a prescription into plates of rice, dal and vegetables that a patient will really eat. This unit pairs each diet with its calculation, and every number is checked by program.

::: key What this unit gives you
- Real photographs of a glucometer reading, a dialysis machine, a blood-pressure check and a hospital soft-diet tray, with numbered marks.
- Routine hospital diets and the logic of changing a diet; diabetes with carbohydrate exchanges and glycaemic load.
- Sodium, salt and saturated fat for hypertension and heart disease; protein, fluid and potassium for kidney disease; liver, burns, fever and tuberculosis.
- Eight points on the nurse's role in diet therapy, with model answers and a full care plan for diabetes with hypertension.
:::

## 4.1 Principles of diet therapy and routine hospital diets

The diet is changed in one or more of six ways: **energy** (increase or decrease), **a nutrient** (protein, sodium, potassium, fat, carbohydrate), **consistency** (liquid, soft, mashed), **fibre** (low or high), **frequency** (small frequent meals) and **route** (oral, tube or vein). The **rules** are: the diet is prescribed by the doctor or dietitian, it follows the normal pattern as far as possible, it uses food the patient likes and can afford, and it is checked regularly. Foods are chosen from the patient's culture: rice, *roti*, *dhido*, dal, vegetable, curd, egg and fish, which can nearly always be adapted.

| Diet | Description | Used in |
|---|---|---|
| **Normal / full** | All foods, 2,000-2,400 kcal | Patients with no restriction |
| **Soft** | Cooked, mashed, low-fibre foods: *khichadi*, *jaulo*, mashed vegetable, egg, curd | Fever, after surgery, dental problems |
| **Liquid** (clear and full) | Clear: water, ORS, thin soup. Full: milk, juice, gruel | Acute illness, post-operative start |
| **Bland / low residue** | Little fibre and spice | Peptic ulcer, colitis, before bowel surgery |
| **High-energy, high-protein** | 3,000+ kcal, 1.5 g protein/kg | TB, burns, malnutrition |
| **Diabetic** | Controlled carbohydrate, regular timing | Diabetes mellitus |
| **Low sodium** | Under 2 g sodium (5 g salt) | Hypertension, heart failure, oedema |

## 4.2 Diabetes mellitus: diet is the first treatment

The aim is to keep blood glucose near normal, avoid hypoglycaemia, reach a healthy weight and lower the risk of heart disease. The usual plan has **carbohydrate 50-55%** of energy (chiefly complex and high-fibre), **protein 15-20%** (0.8-1.0 g/kg unless the kidney is damaged), **fat under 30%** with saturated fat under 10% and **fibre 25-40 g** a day. Rice, *roti* and potato are not forbidden; the **amount, timing and the company they keep** (dal, vegetables) matter. Meals must be regular, with 3 meals and 2-3 snacks so that the dose of insulin or tablet matches the glucose load. Alcohol is limited and never taken fasting.

A **carbohydrate exchange** is the portion containing about **15 g of carbohydrate**, for example half a cup of cooked rice, one *roti*, a small potato or a small fruit. The prescribed energy is converted into a number of exchanges. The **glycaemic index (GI)** ranks foods by their effect on blood glucose; the **glycaemic load (GL)** = GI × carbohydrate in the portion (g) ÷ 100 includes the quantity, so a small portion of a high-GI food can have a modest load.

```python
kcal = 1600
carb_kcal = 0.55 * kcal
carb_g = carb_kcal / 4
print(f"Energy {kcal} kcal: carbohydrate 55% = {carb_kcal:.0f} kcal = {carb_g:.0f} g = {carb_g/15:.1f} exchanges of 15 g")
plan = {"breakfast": 3, "mid-morning": 1, "lunch": 4, "evening": 2, "dinner": 4, "bedtime": 1}
n = sum(plan.values())
print(f"Plan: {plan} -> {n} exchanges = {n*15} g = {n*15*4} kcal = {n*15*4/kcal*100:.1f}% of energy")
print(f"Glycaemic load: white rice (GI 73, 45 g carbohydrate) = {73*45/100:.1f}; dal (GI 30, 20 g) = {30*20/100:.1f}")
print(f"Ideal weight for 164 cm (Broca) = {164-100} kg; at 25 kcal/kg = {25*(164-100)} kcal")
```

```text
Energy 1600 kcal: carbohydrate 55% = 880 kcal = 220 g = 14.7 exchanges of 15 g
Plan: {'breakfast': 3, 'mid-morning': 1, 'lunch': 4, 'evening': 2, 'dinner': 4, 'bedtime': 1} -> 15 exchanges = 225 g = 900 kcal = 56.2% of energy
Glycaemic load: white rice (GI 73, 45 g carbohydrate) = 32.9; dal (GI 30, 20 g) = 6.0
Ideal weight for 164 cm (Broca) = 64 kg; at 25 kcal/kg = 1600 kcal
```

A prescription of 1,600 kcal with 55% carbohydrate gives **880 kcal or 220 g, which is 14.7 exchanges**; the plan of 15 exchanges spreads this over six eating times, giving **225 g or 56.2% of energy**. A cup of white rice (45 g carbohydrate, GI 73) has a glycaemic load of **32.9**, while a bowl of dal (GI 30, 20 g) has only **6.0**, which is why dal and vegetables are always served with rice. A person with a height of 164 cm has an ideal weight of 64 kg, and 25 kcal/kg gives the same 1,600 kcal.

```photogrid label="4.1" cols="4" ratio="1.0" caption="Diet therapy in practice. (a) A real glucometer reading 142 mg/dL with its strip vial and lancet: the nurse checks capillary glucose before meals and at bedtime. (b) A real haemodialysis machine: dialysis patients need protein 1.0-1.2 g/kg and a fluid limit. (c) A blood-pressure check by aneroid sphygmomanometer: salt and weight advice follows every high reading. (d) A hospital soft-diet tray with porridge, curd, scrambled egg and a dessert."
@ photo id="nur4/glucometer" cap="Glucometer"
fit 1.0
focus 0.4 0.6
mark 0.22 0.55 "1"
mark 0.78 0.58 "2"
key 1 (a) The display: capillary glucose in mg/dL
key 2 (a) Test-strip vial: strip must be in date and the vial closed
@ photo id="nur4/dialysis" cap="Dialysis machine"
fit 1.0
focus 0.5 0.62
mark 0.30 0.82 "3"
mark 0.50 0.45 "4"
key 3 (b) The display and controls: set the ultrafiltration (fluid removal)
key 4 (b) The dialyser and blood tubing: waste products and fluid are removed
@ photo id="nur4/bpaneroid" cap="BP measurement"
fit 1.0
focus 0.5 0.55
mark 0.55 0.48 "5"
key 5 (c) The cuff on the upper arm at heart level: repeat after 5 minutes' rest
@ photo id="nur4/meal" cap="Hospital soft diet tray"
fit 1.0
focus 0.5 0.5
mark 0.78 0.55 "6"
mark 0.88 0.82 "7"
key 6 (d) Scrambled egg: soft protein
key 7 (d) Creamy porridge: soft, easy-to-swallow energy
```

```svgfig label="4.1" caption="The plate method for a person with diabetes and hypertension: half non-starchy vegetables, a quarter cereal (rice, roti, dhido) and a quarter dal, egg, fish or lean meat, with one fruit and a little oil. Use little salt and no sweet drinks."
f = Fig(760, 220)
f.text(380, 16, "One plate, by proportion", size=12, color=NAVY, bold=True)
f.box(10, 28, 360, 66, "Non-starchy vegetables\n1/2 of the plate", fill=MINT, stroke=TEAL, size=12, bold=True)
f.box(370, 28, 180, 66, "Cereal\n1/4 of the plate", fill=SAND, stroke=AMBER, size=12, bold=True)
f.box(550, 28, 200, 66, "Dal, egg, fish\n1/4 of the plate", fill=ROSE, stroke=RED, size=12, bold=True)
f.box(10, 110, 240, 60, "Vegetables: green leaves,\ngourd, beans, cauliflower", fill=SOFT, stroke=TEAL, size=10.5)
f.box(260, 110, 240, 60, "Cereal: 1 roti or half cup of rice\n(1 exchange = 15 g carbohydrate)", fill=SOFT, stroke=AMBER, size=10.5)
f.box(510, 110, 240, 60, "Protein: 1 katori dal, egg,\nfish or low-fat curd", fill=SOFT, stroke=RED, size=10.5)
f.text(380, 200, "Oil 3-4 teaspoons a day; salt under 5 g; water to drink", size=11, color=NAVY, bold=True)
```

## 4.3 Hypertension, heart disease and raised cholesterol

Hypertension (140/90 mmHg or more) is the commonest NCD that a Nepali nurse meets. The **DASH diet** (Dietary Approaches to Stop Hypertension) lowers systolic pressure by 8-14 mmHg: plenty of vegetables, fruit, pulses, low-fat milk and whole grain, with less red meat, sweets and **salt**. The WHO limit is **under 5 g salt (2 g sodium) a day**. Sodium is 39.3% of salt, so 1 g of salt contains 393 mg of sodium. The hidden sources in Nepal are **pickles (*achar*), dried fish, instant noodles, chips, *papad*, ghee-fried snacks and added salt at the table**, and many families add salt three times in cooking. Potassium-rich foods (banana, orange, green leaves, potato with skin) help, except in kidney failure. Other advice is weight reduction (every kg lost lowers systolic BP by about 1 mmHg), stopping tobacco, limiting alcohol and 30 minutes of walking daily.

In **heart failure** the sodium limit is 2 g, fluid may be limited to 1.5-2 L, and small frequent meals avoid load on the heart. In **dyslipidaemia** keep **saturated fat below 10% of energy** (below 7% in high risk), trans fat below 1%, cholesterol under 300 mg, and add oats, pulses, nuts, fish and fruit; replace ghee and vanaspati with mustard or soybean oil in small quantity.

## 4.4 Kidney disease and liver disease

In **chronic kidney disease (CKD)** the nurse balances protein, sodium, potassium, phosphorus and fluid. **Before dialysis** protein is limited to **0.6-0.8 g/kg** to slow decline; **on haemodialysis** the need rises to **1.0-1.2 g/kg** (at least half high-quality protein: egg, fish, milk, lean meat) because dialysis removes amino acids; energy is 30-35 kcal/kg. **Sodium** is limited to 2 g, **potassium** to 2-3 g if the blood level is high (avoid banana, orange, coconut water, potato and tomato; leaching vegetables by soaking and boiling reduces it), **phosphorus** to 800-1,000 mg (milk, nuts, pulses and cola in limit; binders with food), and **fluid** = the previous day's urine output + 500 mL. In **nephrotic syndrome** protein is 0.8-1.0 g/kg, salt is restricted and fat is low.

In **liver disease** energy is 30-35 kcal/kg and protein is **1.2-1.5 g/kg**, not restricted, even in hepatic encephalopathy, since starvation worsens muscle loss. A **late-evening snack** shortens overnight fasting; sodium is limited to 2 g if ascites is present, and **alcohol is completely stopped**. Fat is allowed as tolerated; in acute hepatitis small frequent meals with a good breakfast are best when appetite is poor in the evening.

## 4.5 Burns, fever, tuberculosis and surgery

After a major burn the metabolic rate rises up to two times and large protein is lost in the exudate, so feeding starts early (within 24-48 hours, oral or NG), at high energy and protein. The **Curreri formula** for adults gives energy = **25 kcal × weight (kg) + 40 kcal × % TBSA burned**, and protein is 1.5-2 g/kg. In **fever**, the BMR rises by about **13% for every 1 °C above 37 °C**, so fluids and soft, high-energy feeds are needed. In **tuberculosis** the energy need is 35-40 kcal/kg and the protein 1.5 g/kg, and the Nepal National TB Programme gives a nutrition support food package for patients on treatment in selected districts. Before **surgery** correct malnutrition, fast for solids 6 hours (clear fluid 2 hours), and start oral feeding early after.

```python
salt = 5.0
print(f"Sodium in {salt:.0f} g salt = {salt*393.4:.0f} mg; 2,000 mg sodium = {2000/393.4:.2f} g salt; 160 mg sodium on a label = {160/393.4:.2f} g salt")
print(f"Saturated fat limit 10% of 2,000 kcal = {0.10*2000/9:.1f} g")
w = 60
print(f"Dialysis patient {w} kg: protein 1.2 g/kg = {1.2*w:.0f} g; energy 30-35 kcal/kg = {30*w} to {35*w} kcal; fluid = 600 mL + 500 = {600+500} mL")
print(f"Pre-dialysis protein 0.6-0.8 g/kg = {0.6*w:.0f} to {0.8*w:.0f} g")
print(f"Curreri: 25 x {w} + 40 x 30 = {25*w + 40*30} kcal; protein 2 g/kg = {2*w} g")
bmr = 1500
print(f"Fever 39 C: BMR {bmr} x (1 + 0.13 x 2) = {bmr*(1+0.13*2):.0f} kcal")
```

```text
Sodium in 5 g salt = 1967 mg; 2,000 mg sodium = 5.08 g salt; 160 mg sodium on a label = 0.41 g salt
Saturated fat limit 10% of 2,000 kcal = 22.2 g
Dialysis patient 60 kg: protein 1.2 g/kg = 72 g; energy 30-35 kcal/kg = 1800 to 2100 kcal; fluid = 600 mL + 500 = 1100 mL
Pre-dialysis protein 0.6-0.8 g/kg = 36 to 48 g
Curreri: 25 x 60 + 40 x 30 = 2700 kcal; protein 2 g/kg = 120 g
Fever 39 C: BMR 1500 x (1 + 0.13 x 2) = 1890 kcal
```

A diet limited to 2,000 mg sodium allows **5.08 g of salt**; a packet snack with 160 mg sodium contains **0.41 g** of it, a good reason to read labels, and 5 g of salt holds **1,967 mg** of sodium. The saturated fat limit is **22.2 g** on a 2,000-kcal diet. A 60-kg dialysis patient needs **72 g protein, 1,800 kcal and 1,100 mL of fluid** a day, while the same man before dialysis would take only 36-48 g of protein. A 60-kg adult with **30% burns** needs 25 × 60 + 40 × 30 = **2,700 kcal** and 120 g of protein; and a patient with a 39 °C fever whose BMR is 1,500 kcal needs about **1,890 kcal**.

```svgfig label="4.2" caption="Diet in kidney disease. Before dialysis protein is restricted to slow the loss of nephrons; once dialysis starts, protein is increased because the machine removes amino acids. Sodium, potassium, phosphorus and fluid are controlled in both stages."
f = Fig(760, 220)
f.box(10, 18, 340, 58, "BEFORE DIALYSIS (CKD 3-5)\nProtein 0.6-0.8 g/kg   Energy 30-35 kcal/kg", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(410, 18, 340, 58, "ON HAEMODIALYSIS\nProtein 1.0-1.2 g/kg   Energy 30-35 kcal/kg", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.arrow([(350, 47), (410, 47)], color=SLATE, sw=2.2)
items = [("Sodium\n2 g (5 g salt)", ROSE, RED), ("Potassium\n2-3 g if high", SAND, AMBER), ("Phosphorus\n800-1,000 mg", BLUE, NAVY), ("Fluid\nurine + 500 mL", MINT, TEAL)]
for i, (t_, fc, sc) in enumerate(items):
    f.box(10 + i * 188, 100, 172, 60, t_, fill=fc, stroke=sc, size=11, bold=True)
f.text(380, 188, "Weigh daily; gains of more than 2 kg between dialysis sessions suggest fluid overload", size=10.5, color=RED, bold=True)
f.text(380, 208, "High-quality protein: egg, fish, milk, lean meat; dal in measured amounts", size=10.5, color=TEAL, bold=True)
```

## 4.6 The nurse's role in diet therapy: eight points

1. **Check the diet order before serving.** Match the patient's name, bed and the written diet with the tray. A diabetic given sweet tea or a renal patient given a banana can be harmed in minutes. If an order is unclear, ask the doctor or dietitian before the tray is given.
2. **Explain the purpose of the diet in plain words.** Say why salt, sugar or protein is limited and what food can be eaten, not only what is forbidden. People follow a diet that they understand and that fits their culture. Use the plate model, pictures and real portion sizes.
3. **Make the diet acceptable.** Serve food warm, attractive and in the right texture, with spices that the patient likes within limits. Invite the family to bring permitted home food. Poor acceptance is the main reason therapeutic diets fail.
4. **Monitor intake and record it.** Note the percentage eaten at each meal, fluids drunk and the vomit and stool. Weigh regularly and report if the intake is below half for two days. Small shortfalls grow into malnutrition.
5. **Monitor the effect of the diet.** Check capillary glucose, BP, weight, oedema, urine output and lab values as ordered. Compare them with the target and report to the team. The diet is changed if the result is not reached.
6. **Coordinate meals with medicines.** Give insulin or glibenclamide so the meal follows on time, give iron and calcium apart, and give medicines that need food with the meal. A missed meal after insulin causes hypoglycaemia. Keep a quick sugar source at the bedside.
7. **Prepare the family for home.** Teach the diet in their language, with local food lists, label reading and a three-day sample menu. Involve the person who cooks. Link the patient to the health post PEN service for follow-up.
8. **Prevent complications and special risks.** Watch for hypoglycaemia, hyperkalaemia, fluid overload, aspiration, bed-sores and refeeding signs. Teach the danger signs and what to do. Record and report promptly so that the diet is changed on time.

## Formula and fact sheet

- Diabetes: carbohydrate 50-55%, 1 exchange = 15 g; GL = GI × carbohydrate (g) ÷ 100; 3 meals plus 2-3 snacks.
- Salt under 5 g (2 g sodium); 1 g salt = 393 mg sodium; saturated fat under 10% of energy.
- CKD before dialysis protein 0.6-0.8 g/kg; on dialysis 1.0-1.2 g/kg; fluid = urine + 500 mL; liver protein 1.2-1.5 g/kg.
- Curreri 25 kcal/kg + 40 kcal × %TBSA; fever +13% BMR per °C above 37; TB 35-40 kcal/kg and 1.5 g protein/kg.

## Chapter summary

- Diet therapy changes energy, one nutrient, texture, frequency or route, and keeps to the patient's own foods.
- Diabetes diet controls the amount and timing of carbohydrate; the plate method and exchanges make it practical.
- Hypertension needs under 5 g salt and the DASH pattern; kidney disease balances protein, sodium, potassium, phosphorus and fluid.
- Burns, fever and TB need high energy and protein; the nurse checks the order, serves, monitors and teaches.

## Practice

**MCQs (with reasons)**

1. The sodium in 5 g of common salt is about: (a) 500 mg (b) 1,000 mg (c) 1,967 mg (d) 5,000 mg.
2. A 70-kg adult has 40% TBSA burns; the Curreri energy requirement is: (a) 1,750 kcal (b) 2,800 kcal (c) 3,350 kcal (d) 4,200 kcal.
3. The glycaemic load of a portion with GI 73 and 30 g carbohydrate is: (a) 2.4 (b) 21.9 (c) 43.0 (d) 73.0.
4. A dialysis patient passed 400 mL of urine yesterday; today's fluid allowance is: (a) 400 mL (b) 500 mL (c) 900 mL (d) 1,500 mL.
5. A prescription of 3,000 mg sodium corresponds to salt of about: (a) 3 g (b) 4.5 g (c) 7.6 g (d) 11.8 g.

::: note Answers and rationales
**1. (c).** Salt is 39.3% sodium, so 5 g contains 1,967 mg; this is also the WHO daily limit.
**2. (c).** 25 × 70 + 40 × 40 = 1,750 + 1,600 = 3,350 kcal; the first answer forgets the burn term.
**3. (b).** GL = 73 × 30 ÷ 100 = 21.9; GL combines the quality (GI) and quantity of carbohydrate.
**4. (c).** Allowance = previous urine output + 500 mL = 900 mL, which limits interdialytic weight gain.
**5. (c).** 3,000 ÷ 393.4 = 7.6 g of salt; dividing by 1,000 only converts units and gives the wrong figure.
:::

**Short answer (3 marks): Plate method for diabetes.** The plate method teaches portions without weighing. Half the plate is non-starchy vegetables, one quarter is a cereal such as rice or roti and one quarter is dal, egg, fish or lean meat, with a small fruit and little oil. It controls the carbohydrate load of each meal (about 3-4 exchanges of 15 g), is easily understood by a family that cooks Nepali meals and does not require a food scale. Sweetened drinks are replaced by water.

**Medium answer (5 marks): Describe the dietary management of hypertension.** The diet is the **DASH pattern**: plenty of vegetables, fruit, pulses, low-fat milk and whole grain with less red meat, ghee and sweets. **Salt is limited to under 5 g (2 g sodium) a day**: do not add salt at table, avoid *achar*, dried fish, noodles and packed snacks, and cook with spices and lemon. Potassium-rich foods help unless there is kidney disease. Weight is reduced if BMI is high, alcohol and tobacco are stopped and exercise of 30 minutes a day is added. The nurse measures BP regularly, teaches label-reading and refers to the PEN clinic of the health post for continued follow-up.

**Long answer (10 marks): Mr Hari Prasad Adhikari, 58 years, weighing 70 kg and 164 cm tall, is admitted with a fasting glucose of 212 mg/dL, HbA1c 8.4% and BP 156/96 mmHg. He eats three large plates of rice a day with pickle and extra salt, drinks four sweet teas and does little exercise. Plan his diet and the nursing care.**

*Assessment.* BMI = 70 ÷ 1.64² = **26.0 kg/m²**, overweight; ideal weight (Broca) 64 kg. He has type 2 diabetes and hypertension, both worsened by diet, weight and inactivity.

*Diet plan.* Energy **1,600 kcal a day** (25 kcal × 64 kg), which gives a deficit of about 500 kcal below his maintenance of about 2,100 kcal, or a loss of about **0.45 kg a week**; a target loss of 5-7% of body weight is **3.5 to 4.9 kg**. Carbohydrate 55% = 880 kcal = 220 g = **15 exchanges** of 15 g (three at breakfast, one mid-morning, four at lunch, two in the evening, four at dinner and one at bedtime), chiefly from whole grain, millet and pulses. Protein 0.8-1 g/kg, **saturated fat under 10% = 17.8 g**, fibre 30 g, **salt under 5 g**, no sweet tea (replace with unsweetened tea or lemon water), small portions of rice with a double portion of vegetable and a bowl of dal, and a fruit. Walking 30 minutes, 5 days a week; check capillary glucose before meals and at bedtime; teach foot care and hypoglycaemia recognition. Follow-up through the health post PEN clinic.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "I eat rice three times a day and I take sweet tea." **O:** glucose 212 mg/dL, HbA1c 8.4%, BMI 26.0. | **Unstable blood glucose level** (risk) related to excess carbohydrate intake and inactivity, as evidenced by glucose 212 mg/dL. | **Blood glucose level:** fasting glucose below 130 mg/dL in 4 weeks. | 1. Teach 15 exchanges and the plate method; *controls the carbohydrate load.* 2. Check glucose before meals and at bedtime; *guides therapy.* 3. Replace sweet tea with unsweetened drinks; *removes free sugar.* | Fasting glucose 118 mg/dL at 4 weeks; goal met. |
| **O:** BP 156/96 mmHg, adds salt and pickle. | **Ineffective health management** related to high salt use and lack of knowledge, as evidenced by BP 156/96 mmHg. | **Knowledge: hypertension management:** BP below 140/90 and salt below 5 g within 8 weeks. | 1. Teach DASH foods and hidden sources of salt; *salt restriction lowers BP.* 2. Measure BP on each visit; *monitors the effect.* 3. Teach walking and weight loss; *lowers BP and glucose.* | BP 134/84 at 8 weeks. |
| **O:** BMI 26.0, sedentary. | **Overweight** related to excess energy intake and low activity, as evidenced by BMI above 25. | **Weight control:** loss of 3.5 to 4.9 kg in 3 months. | 1. Set a plan of 1,600 kcal; *a deficit of 500 kcal a day loses about 0.45 kg a week.* 2. Weigh weekly; *objective feedback.* 3. Involve the family cook; *the diet is cooked at home.* | Weight 66 kg at 3 months; goal met. |

::: tip Exam tip
In every diet question give the energy prescription, convert the nutrient percentages into grams or exchanges, give the local food examples, and finish with monitoring and teaching.
:::
