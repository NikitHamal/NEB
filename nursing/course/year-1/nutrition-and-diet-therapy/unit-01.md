---
subject: Nutrition and Diet Therapy
grade: BSc Nursing Year 1
unit: 1
title: Nutrition Science, Energy, Macronutrients and Nutritional Assessment
hours: 12
area: BSN 8 · Nutrition and Diet Therapy · Unit 1
---

Food is the first medicine a nurse gives. In Nepal about 25% of children under five are stunted, 8% are wasted and 19% are underweight (NDHS 2022), while overweight and diabetes rise in the towns. The Multi-Sector Nutrition Plan III (2023-2030) of the National Planning Commission puts nutrition into health, agriculture, education and local government together, and the Ministry of Health and Population (MoHP) delivers it through health posts, FCHVs and hospitals. A ward nurse must therefore be able to do three things well: **calculate what a person needs, assess what the person actually has, and teach the difference in simple words.** This unit builds those skills with energy arithmetic that is computed and checked by program.

::: key What this unit gives you
- Real photographs of a Nepali meal, a dal bowl, a skinfold caliper and a food label, with the energy sum on the label checked.
- Atwater factors, the macronutrients, energy balance, BMR (Harris-Benedict and Mifflin-St Jeor), total energy need, BMI, waist-hip ratio and ideal weight.
- Eight points on the nurse's role in nutritional assessment, and model answers with a full care plan.
:::

## 1.1 Nutrition, nutrients and energy

**Nutrition** is the science of how the body takes in, uses and gets rid of food. A **nutrient** is a substance in food that the body needs for energy, growth, repair or control. **Macronutrients** (carbohydrate, protein, fat and water) are needed in grams; **micronutrients** (vitamins and minerals) are needed in milligrams or micrograms. Food is the vehicle: a **balanced diet** gives all the nutrients in the right proportion from a variety of foods, which in Nepal means a cereal (rice, maize, wheat, millet), a pulse (dal, beans), vegetables and fruit (gundruk, saag, seasonal fruit), an animal food (milk, egg, fish, meat) and a little oil or ghee in each day. The MSNP-III plan promotes this diversity and the preparation of food-based dietary guidelines and Nepal-specific recommended allowances; until then campuses use ICMR-NIN and WHO values.

**Energy** is measured in kilocalories (kcal); 1 kcal = 4.184 kJ. The energy in food is found by the **Atwater factors**: **carbohydrate 4 kcal/g, protein 4 kcal/g, fat 9 kcal/g, alcohol 7 kcal/g**. A plate of rice, dal and gundruk curry with about 95 g carbohydrate, 22 g protein and 18 g fat gives 95 × 4 + 22 × 4 + 18 × 9 = **630 kcal**, of which carbohydrate supplies 60.3%, protein 14.0% and fat 25.7%. The recommended share for an adult is **carbohydrate 55-65%, protein 10-15% and fat 20-30%** of energy, so this meal is a little low in fat and fully acceptable in the others.

```photogrid label="1.1" cols="3" ratio="1.0" caption="Food, energy and the Atwater factors. (a) Gundruk with rice, a Nepali fermented-vegetable dish: cereal energy with a green-leaf food that supplies iron, fibre and vitamins. (b) A bowl of tempered dal: the pulse that adds protein to a cereal meal. (c) The energy per gram of each nutrient, drawn to scale: fat has more than twice the energy of carbohydrate or protein."
@ photo id="nur4/gundruk" cap="Gundruk with rice"
fit 1.0
focus 0.5 0.5
mark 0.30 0.35 "1"
mark 0.70 0.60 "2"
key 1 (a) Rice: the staple cereal, mainly starch (carbohydrate)
key 2 (a) Gundruk curry: fermented leaf, iron, fibre and vitamin K
@ photo id="nur4/daal" cap="Dal in a metal bowl"
fit 1.0
focus 0.45 0.5
mark 0.50 0.45 "3"
mark 0.35 0.65 "4"
key 3 (b) Yellow dal (lentil): protein and iron, plus lysine that cereals lack
key 4 (b) Oil-tempered spices (jimbu or cumin): fat adds energy and carries vitamin A
@ svg cap="Energy per gram"
f = Fig(300, 300)
f.text(150, 24, "kcal per gram (Atwater)", size=12, color=NAVY, bold=True)
for i, (n_, v_, fc, sc) in enumerate([("Carbohydrate", 4, BLUE, NAVY), ("Protein", 4, MINT, TEAL), ("Alcohol", 7, SAND, AMBER), ("Fat", 9, ROSE, RED)]):
    y = 50 + i * 62
    f.box(20, y, v_ * 28, 40, "", fill=fc, stroke=sc)
    f.text(20 + v_ * 28 + 8, y + 20, f"{v_}", size=14, color=sc, bold=True, anchor="start", vmid=True)
    f.text(24, y + 54, n_, size=10.5, color=SLATE, bold=True, anchor="start")
f.text(150, 292, "1 kcal = 4.184 kJ", size=10.5, color=SLATE, bold=True)
```

## 1.2 Carbohydrate, protein, fat, fibre and water

**Carbohydrates** supply 55-65% of energy. Starch from cereals and tubers is digested to glucose; the brain needs about **130 g of glucose a day**. Dietary **fibre** (25-30 g a day) is not digested, adds bulk, slows glucose absorption and lowers cholesterol; whole grain, pulses, vegetables and fruit supply it. **Free sugars** should be below 10% of energy. The **glycaemic index (GI)** ranks foods by how fast they raise blood glucose: white rice and sweets are high, pulses and millet are lower, which matters in diabetes.

**Proteins** (4 kcal/g) build and repair tissue and make enzymes, hormones and antibodies. They are chains of **amino acids**, nine of which are *essential* (histidine, isoleucine, leucine, lysine, methionine, phenylalanine, threonine, tryptophan, valine). Animal proteins are *complete*; cereals are low in lysine and pulses are low in methionine, so **rice with dal** completes the amino acid pattern, which is the logic of the Nepali *sarbottam pitho* (a flour of half cereal and half pulses). The adult allowance is **0.83 g/kg a day**, so a 52-kg woman needs about **43.2 g**; protein is 16% nitrogen, so protein = nitrogen × 6.25.

**Fats** (9 kcal/g) give concentrated energy, carry vitamins A, D, E and K, and build cell membranes. Saturated fat (ghee, butter, coconut) and trans fat (hydrogenated vanaspati) raise LDL cholesterol; unsaturated fat (mustard, soybean and sunflower oil, fish, nuts) protects. **Linoleic and alpha-linolenic acids** are essential. Keep saturated fat below 10% of energy and trans fat below 1%. **Water** is 55-60% of adult body weight; the need is about 30-35 mL/kg, which for 52 kg is **1,560 to 1,820 mL** a day, more in fever, heat or diarrhoea.

```svgfig label="1.1" caption="Energy balance. Energy in (food, by Atwater factors) is spent on basal metabolism, the thermic effect of food and physical activity. When intake exceeds expenditure the surplus is stored as fat; when it is less, the body uses its stores."
f = Fig(760, 210)
f.box(10, 60, 170, 90, "Energy IN\nCarbohydrate 4\nProtein 4  Fat 9 kcal/g", fill=MINT, stroke=TEAL, size=11, bold=True)
f.box(300, 14, 220, 52, "BMR 60-70%\nbreathing, heart, brain, liver", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(300, 78, 220, 52, "Thermic effect of food 10%\ndigestion and absorption", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(300, 142, 220, 52, "Physical activity 20-30%\nwalking, farm work, nursing", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(600, 60, 150, 90, "Energy OUT\n= TEE", fill=BLUE, stroke=NAVY, size=12, bold=True)
for yy in (40, 104, 168):
    f.arrow([(180, 105), (240, yy), (300, yy)], color=SLATE, sw=1.6)
    f.arrow([(520, yy), (560, yy), (600, 105)], color=SLATE, sw=1.6)
f.text(380, 205, "IN > OUT: weight gain.  IN < OUT: weight loss", size=11, color=RED, bold=True)
```

## 1.3 Energy needs: BMR, activity and total energy expenditure

The **basal metabolic rate (BMR)** is the energy used at complete rest, awake, fasting and in a warm room. The **revised Harris-Benedict equations** (Roza and Shizgal, 1984) are: **men** BMR = 88.362 + 13.397 W + 4.799 H + 5.677 A; **women** BMR = 447.593 + 9.247 W + 3.098 H + 4.330 A (W kg, H cm, A years). The **Mifflin-St Jeor** equation is: 10 W + 6.25 H − 5 A + 5 (men) or − 161 (women), and is usually closer to measured values in modern adults. **Total energy expenditure (TEE)** = BMR × **physical activity level (PAL)**: 1.2 bedrest or sedentary, 1.4 light, 1.55 moderate (teacher, nurse, farmer on easy days), 1.75 heavy, 2.0 very heavy (porter, hill farmer). A quick ward rule is 25-30 kcal/kg a day.

```python
def hb(sex, w, h, a):
    return 88.362 + 13.397*w + 4.799*h + 5.677*a if sex == "M" else 447.593 + 9.247*w + 3.098*h + 4.330*a
def mj(sex, w, h, a):
    return 10*w + 6.25*h - 5*a + (5 if sex == "M" else -161)
print(f"Woman 24 y, 52 kg, 155 cm: HB = {hb('F',52,155,24):.1f}, Mifflin = {mj('F',52,155,24):.1f} kcal/day")
print(f"TEE at PAL 1.55 (Harris-Benedict) = {hb('F',52,155,24)*1.55:.0f} kcal/day")
print(f"Man 30 y, 68 kg, 170 cm: HB = {hb('M',68,170,30):.1f}, Mifflin = {mj('M',68,170,30):.1f} kcal/day")
print(f"Protein 0.83 g/kg x 52 kg = {0.83*52:.1f} g; water 30-35 mL/kg = {30*52} to {35*52} mL")
print(f"Label check: 8 g fat x 9 + 37 g carbohydrate x 4 + 3 g protein x 4 = {8*9 + 37*4 + 3*4} kcal (printed 230)")
```

```text
Woman 24 y, 52 kg, 155 cm: HB = 1512.5, Mifflin = 1207.8 kcal/day
TEE at PAL 1.55 (Harris-Benedict) = 2344 kcal/day
Man 30 y, 68 kg, 170 cm: HB = 1985.5, Mifflin = 1597.5 kcal/day
Protein 0.83 g/kg x 52 kg = 43.2 g; water 30-35 mL/kg = 1560 to 1820 mL
Label check: 8 g fat x 9 + 37 g carbohydrate x 4 + 3 g protein x 4 = 232 kcal (printed 230)
```

The 52-kg woman has an HB BMR of **1512.5 kcal/day** (Mifflin-St Jeor **1207.8**) and, at PAL 1.55, a TEE of about **2,344 kcal/day**. The 30-year-old man's BMR is 1985.5 by Harris-Benedict and 1597.5 by Mifflin-St Jeor. The two formulas differ by 10-20%, so the nurse treats any figure as an estimate and **adjusts it by weight change** over 2-4 weeks. To lose 0.5 kg of fat a week a deficit of about 500 kcal a day (3,850 kcal a week; 1 kg of fat is about 7,700 kcal) is used.

## 1.4 Nutritional assessment: ABCD

Nutritional assessment finds who is malnourished, why, and how it changes. The four arms are remembered as **ABCD**: **A**nthropometry, **B**iochemical tests, **C**linical examination and **D**ietary history. **Anthropometry** measures weight, height, **BMI** = weight (kg) ÷ height (m)², mid-upper-arm circumference, skinfold thickness (triceps, biceps, subscapular, suprailiac, by a calibrated caliper), and waist and hip circumference. **Biochemical** tests include haemoglobin, serum albumin (half-life 20 days), prealbumin (2 days), transferrin, lymphocyte count and blood glucose. The **clinical** examination looks at hair, eyes, mouth, skin, nails, oedema and muscle. The **dietary** history uses a **24-hour recall**, a food-frequency list and a food diary.

The woman above (52 kg, 155 cm) has a BMI of 52 ÷ 1.55² = **21.6 kg/m²**, which is normal. The WHO classes are: below 18.5 underweight, 18.5-24.9 normal, 25-29.9 overweight, 30 or more obese; because South Asians carry more body fat at a given BMI, the **Asia-Pacific cut-offs** (overweight from 23, obese from 25) are used to judge risk. A waist of 88 cm with a hip of 98 cm gives a **waist-hip ratio of 0.90**; the WHO risk limit is above 0.85 in women and 0.90 in men, so this woman has central-fat risk even with a normal BMI. A quick **ideal body weight** is Broca's: height in cm minus 100, here **55 kg**.

```photogrid label="1.2" cols="3" ratio="1.0" caption="Tools of assessment. (a) A real skinfold caliper: fold of skin and fat is held between the jaws and the dial gives millimetres. (b) A real food label: the printed 230 kcal equals the Atwater sum of the fat, carbohydrate and protein shown (232 kcal, rounded). (c) BMI classes on a linear scale."
@ photo id="nur4/caliper" cap="Skinfold caliper"
fit 1.0
focus 0.5 0.45
mark 0.55 0.35 "1"
mark 0.40 0.78 "2"
key 1 (a) The dial: reads skinfold thickness in millimetres
key 2 (a) The jaws: pinch a fold of skin and fat at the triceps or subscapular site
@ photo id="nur4/label" cap="Nutrition facts label"
fit 1.0
focus 0.5 0.80
mark 0.17 0.60 "3"
mark 0.17 0.09 "4"
key 3 (b) Calories per serving: check against 4-4-9
key 4 (b) Sodium, fibre and added sugar: read them in diabetes and hypertension
@ svg cap="BMI classes"
f = Fig(300, 300)
f.text(150, 22, "BMI (kg/m2)", size=12, color=NAVY, bold=True)
for i, (a_, lab_, fc, sc) in enumerate([("below 18.5", "Underweight", SAND, AMBER), ("18.5 - 24.9", "Normal", MINT, TEAL), ("25 - 29.9", "Overweight", SAND, AMBER), ("30 or more", "Obese", ROSE, RED)]):
    f.box(30, 40 + i * 62, 240, 50, f"{a_}   {lab_}", fill=fc, stroke=sc, size=11, bold=True)
f.text(150, 292, "Asia-Pacific risk cut-offs: 23 and 25", size=10, color=SLATE, bold=True)
```

```svgfig label="1.2" caption="The ABCD of nutritional assessment. Each arm gives a different kind of evidence, and a diagnosis is made from the pattern, not from one test."
f = Fig(760, 220)
arms = [("A  Anthropometry", "Weight, height, BMI\nMUAC, skinfold\nwaist and hip", BLUE, NAVY), ("B  Biochemical", "Haemoglobin, albumin\nprealbumin, lymphocytes\nglucose, urea", MINT, TEAL), ("C  Clinical", "Hair, eyes, mouth\nskin, nails, oedema\nmuscle wasting", SAND, AMBER), ("D  Dietary", "24-hour recall\nfood frequency\ndiary, appetite", ROSE, RED)]
for i, (t_, d_, fc, sc) in enumerate(arms):
    x = 6 + i * 188
    f.box(x, 22, 172, 36, t_, fill=fc, stroke=sc, size=12, bold=True)
    f.box(x, 66, 172, 86, d_, fill=SOFT, stroke=sc, size=10.5)
    f.arrow([(x + 86, 152), (x + 86, 170), (380, 176)], color=sc, sw=1.4)
f.box(230, 176, 300, 38, "Nutritional diagnosis, plan and review", fill=BLUE, stroke=NAVY, size=12, bold=True)
```

Screening tools find risk early: the **Malnutrition Universal Screening Tool (MUST)** scores BMI (above 20 = 0; 18.5-20 = 1; below 18.5 = 2), unplanned weight loss over 3-6 months (below 5% = 0; 5-10% = 1; above 10% = 2) and acute illness with no intake for 5 days (2). A total of 2 or more is high risk. Percentage weight loss = (usual − present) ÷ usual × 100; a loss of more than 10% in 6 months, or 5% in a month, is severe.

## 1.5 The nurse's role in nutritional assessment and care: eight points

1. **Screen every patient on admission.** Weigh, measure height and calculate BMI within 24 hours, and use MUST or the hospital tool. Record the weight on the chart in kilograms with the date. A patient screened early is fed early, and early feeding shortens the hospital stay.
2. **Take an accurate diet history.** Ask what the patient ate in the last 24 hours, usual meal times, fasting customs, allergies, dislikes and who cooks. Use household measures such as a *mana*, a cup and a spoon, and write what you were told, not what you expect. A good history reveals low protein, little oil or a monotonous cereal diet.
3. **Weigh and measure correctly.** Use a calibrated scale, remove shoes and heavy clothes, and measure height against a wall. For bedridden patients use MUAC or knee-height estimates. Wrong weights give wrong drug and feed doses.
4. **Examine for signs of deficiency.** Look at the eyes (Bitot's spots), mouth (cheilosis, glossitis, bleeding gums), skin (dermatitis), neck (goitre) and legs (oedema, bowing). A quick head-to-toe takes three minutes and often finds what laboratories miss.
5. **Interpret and report abnormal results.** BMI below 18.5, weight loss above 5%, haemoglobin below normal or albumin below 3.5 g/dL need the doctor and dietitian. State the number and the trend. A trend over weeks is more useful than one reading.
6. **Plan and serve food to the patient's needs.** Check that the diet on the tray matches the diet order, that it is warm, attractive, at the right texture and within reach. Sit the patient up and help with feeding. Record the percentage eaten at each meal.
7. **Teach patient and family.** Use local foods, small amounts of oil, dal with rice, a green vegetable daily and fruit in season, and avoid long fasts or unproven diets. Teach in simple Nepali with a plate model and pictures. The teaching succeeds if the family can say it back.
8. **Monitor, record and refer.** Weigh weekly (daily for some patients), keep an intake chart, and review the plan after 2-4 weeks. Refer to the dietitian, community nutrition programme or health post for follow-up. Record in the nursing notes so that the next shift continues the plan.

## Formula and fact sheet

- Atwater: carbohydrate 4, protein 4, fat 9, alcohol 7 kcal/g; 1 kcal = 4.184 kJ; shares 55-65 : 10-15 : 20-30%.
- Harris-Benedict (revised) men 88.362 + 13.397 W + 4.799 H + 5.677 A; women 447.593 + 9.247 W + 3.098 H + 4.330 A. Mifflin-St Jeor 10 W + 6.25 H − 5 A + 5 or − 161.
- TEE = BMR × PAL (1.2, 1.4, 1.55, 1.75, 2.0). Protein 0.83 g/kg; water 30-35 mL/kg; fibre 25-30 g; protein = N × 6.25.
- BMI = kg ÷ m². WHR limits 0.85 (women) and 0.90 (men). Broca's weight = height (cm) − 100. Weight loss % = (usual − present) ÷ usual × 100.
- Nepal (NDHS 2022): stunting 25%, wasting 8%, underweight 19%, anaemia in women 34% and in children 6-59 months 43%; MSNP-III 2023-2030.

## Chapter summary

- Energy comes from carbohydrate and protein at 4 kcal/g, fat at 9 and alcohol at 7; a balanced diet gives each in the right share from varied local foods.
- BMR plus activity gives total energy need; every formula result is an estimate to be adjusted by weight change.
- Assessment follows ABCD, uses BMI, WHR, MUAC and skinfolds, and screening with MUST finds risk early.
- The nurse screens, measures, examines, plans, teaches and records, and refers to the dietitian when needed.

## Practice

**MCQs (with reasons)**

1. A snack has 20 g carbohydrate, 10 g protein and 5 g fat. Its energy is: (a) 95 kcal (b) 165 kcal (c) 215 kcal (d) 335 kcal.
2. A man weighs 70 kg and is 1.75 m tall. His BMI is: (a) 20.0 (b) 22.9 (c) 25.7 (d) 40.0.
3. A patient excretes protein-equivalent nitrogen of 8 g in the day; the protein is: (a) 8 g (b) 32 g (c) 50 g (d) 72 g.
4. A woman who weighed 60 kg now weighs 54 kg; her weight loss is: (a) 6% (b) 10% (c) 11% (d) 15%.
5. The amino-acid pairing that makes rice and dal a complete protein is explained by: (a) both being low in lysine (b) cereals low in lysine and pulses low in methionine (c) both lacking essential fat (d) dal containing vitamin B12.

::: note Answers and rationales
**1. (b).** 20 × 4 + 10 × 4 + 5 × 9 = 80 + 40 + 45 = 165 kcal; (c) wrongly uses 9 kcal/g for carbohydrate and protein.
**2. (b).** 70 ÷ 1.75² = 22.9 kg/m², which is normal by WHO but at the upper normal for Asian risk (23 is the cut-off for overweight).
**3. (c).** Protein = nitrogen × 6.25 = 8 × 6.25 = 50 g, because protein is 16% nitrogen.
**4. (b).** (60 − 54) ÷ 60 × 100 = 10%; dividing by the present weight would give 11%, which is wrong.
**5. (b).** Each food is low in a different amino acid, so together they complete each other; this is why Nepali *dal bhat* and *sarbottam pitho* work.
:::

**Short answer (3 marks): Atwater factors.** The Atwater factors give the usable energy of the nutrients: carbohydrate 4, protein 4, fat 9 and alcohol 7 kcal per gram. They are used to find the energy of a food from its composition, for example 8 g fat, 37 g carbohydrate and 3 g protein = 72 + 148 + 12 = **232 kcal**, which matches a printed label of 230 kcal. They are also used to find the share of energy from each nutrient, which should be 55-65% carbohydrate, 10-15% protein and 20-30% fat.

**Medium answer (5 marks): Describe the ABCD of nutritional assessment (Figure 1.2).** Nutritional assessment finds malnutrition early and guides care. **A, Anthropometry:** weight, height, BMI, MUAC, skinfold thickness and waist-hip ratio, compared with standards and with the patient's own previous values. **B, Biochemical:** haemoglobin, serum albumin, prealbumin, transferrin, total lymphocyte count and glucose; albumin falls slowly and prealbumin quickly, so prealbumin shows recent change. **C, Clinical:** sparse hair, Bitot's spots, cheilosis, bleeding gums, goitre, dermatitis, oedema and wasted muscle. **D, Dietary:** a 24-hour recall, a food-frequency list and a diary give intake, habits and beliefs. A screening score such as MUST decides who needs a full assessment. The nurse records all findings and informs the dietitian.

**Long answer (10 marks): Mrs Sita Tamang, 62 years, is admitted to the medical ward with weakness and poor appetite. She weighed 47 kg three months ago and weighs 41 kg now; her height is 152 cm; haemoglobin is 9.1 g/dL and albumin 2.9 g/dL. She eats one small meal of rice and thin dal a day and lives alone. Assess her nutritional state, calculate her needs and write the nursing care plan.**

*Assessment.* **Anthropometry:** BMI = 41 ÷ 1.52² = **17.7 kg/m²** (underweight, below 18.5); weight loss = (47 − 41) ÷ 47 × 100 = **12.8%** in 3 months, which is severe (above 10%). **MUST score:** BMI below 18.5 = 2, weight loss above 10% = 2, total **4**, so she is at high risk. **Biochemical:** haemoglobin 9.1 g/dL shows anaemia, and albumin 2.9 g/dL (normal 3.5-5.0) shows poor protein status, though albumin also falls in inflammation. **Clinical:** examine for pallor, cheilosis, pitting oedema, muscle wasting and dentition. **Dietary:** one meal a day of rice with thin dal, no vegetable, egg, milk or oil, so energy, protein, iron and vitamins are all low.

*Requirements.* Energy about 30 kcal/kg = 30 × 41 = **1230 kcal a day** to start (increased by 5 kcal/kg later for catch-up), and protein 1.2 g/kg = **49.2 g a day**. Give 5-6 small meals using energy-dense local foods such as *jaulo* or *lito* with oil, dal, egg, milk, mashed vegetables and fruit, with iron-folic acid after meals as ordered and vitamin C food to help absorption. Feed slowly and watch for refeeding signs (weakness, palpitation, swelling) in the first week. Involve the dietitian and arrange community follow-up through the health post and the ward FCHV, and consider social support for a woman who lives alone.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "I have no appetite, I eat once a day." **O:** 41 kg, BMI 17.7, loss 12.8% in 3 months, albumin 2.9 g/dL, MUST 4. | **Imbalanced nutrition: less than body requirements** related to inadequate intake and poor appetite, as evidenced by 6-kg weight loss and BMI below 18.5. | **Nutritional status:** intake of 1230 kcal and 49.2 g protein a day within 3 days; weight gain 0.5 kg a week. | 1. Serve 5-6 small energy-dense meals with dal, egg, milk and oil; *raises energy and protein without overloading the stomach.* 2. Keep an intake chart and weigh weekly; *tracks response objectively.* 3. Give oral hygiene before meals and keep a pleasant setting; *improves appetite.* 4. Refer to the dietitian; *adjusts the plan to labs.* | Day 3: eats at least 75% of each meal; week 2: weight 42 kg or more; goal met. |
| **O:** Hb 9.1 g/dL, pale conjunctiva, tired. | **Fatigue** related to anaemia and undernutrition, as evidenced by weakness and haemoglobin 9.1 g/dL. | **Energy conservation:** carries out daily activity without breathlessness within 1 week. | 1. Give iron-folic acid as ordered after food; *treats iron deficiency.* 2. Offer green leaves, gundruk and citrus; *adds iron and vitamin C.* 3. Space activity with rest; *lowers energy cost.* | Haemoglobin rising at 4 weeks; walks to the toilet unaided. |
| **S:** lives alone, cooks only once. **O:** no family visitor, limited food stock. | **Deficient knowledge** related to lack of information about diet, as evidenced by a one-meal-a-day pattern. | **Knowledge: diet:** names four food groups and plans one day's menu before discharge. | 1. Teach with a plate model and pictures in Nepali; *visual teaching is remembered.* 2. Arrange follow-up with the health post and FCHV; *keeps support at home.* 3. Involve neighbours or relatives in meals; *secures daily feeding.* | Teach-back correct on day of discharge; the first home visit at 1 week. |

::: tip Exam tip
In every nutrition case write the calculation (BMI, percentage weight loss, energy and protein per kg) with its unit, state the category it falls in, and then give a food-based plan using local foods.
:::
