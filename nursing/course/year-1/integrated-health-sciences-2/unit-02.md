---
subject: Integrated Health Sciences II
grade: BSc Nursing Year 1
unit: 2
title: The Endocrine System and Diabetes
hours: 30
area: BSN 2-3 · Integrated Health Sciences II · Unit 2
---

Hormones are chemical messengers that run growth, metabolism, stress response, water balance and reproduction through the blood. A nurse meets them every day: the thyroid tablet at 6 am, the insulin before lunch, the steroid taper after asthma. This unit covers the glands and feedback loops, the thyroid and iodine, the adrenal stress axis, and the pancreas with diabetes mellitus, the largest endocrine problem in Nepal's PEN programme.

::: key What this unit gives you
- A feedback-loop diagram of the hypothalamus-pituitary-thyroid axis paired with a real thyroid micrograph.
- A real pancreatic micrograph, an illustrated glucometer sequence and an insulin-glucagon schematic in one three-up strip.
- The HPA stress axis as a flow diagram.
- HbA1c to average glucose, insulin total daily dose, correction factor, anion gap and corrected sodium, all worked step by step.
- Eight points of diabetes self-care education and model answers with a full care plan for diabetic ketoacidosis.
:::

## 2.1 Hormones, glands and feedback

An **endocrine gland** releases hormones directly into the blood; a hormone acts only on cells with the right receptor. **Peptide hormones** (insulin, ADH, growth hormone) are water-soluble, bind surface receptors and act in seconds. **Steroid hormones** (cortisol, oestrogen, testosterone, aldosterone) and **thyroid hormones** are fat-soluble, enter the cell and change gene expression over hours. Most control is by **negative feedback**: the product switches off its own release, as when high blood glucose raises insulin and insulin then lowers the glucose. The **hypothalamus** is the link between brain and glands: it sends releasing hormones to the **anterior pituitary** (TSH, ACTH, FSH, LH, GH, prolactin) and makes ADH and oxytocin that the **posterior pituitary** stores and releases.

| Gland | Main hormone | Main action | Typical disorder |
|---|---|---|---|
| Anterior pituitary | GH, TSH, ACTH, FSH, LH, prolactin | Growth, control of other glands | Gigantism, acromegaly, hypopituitarism |
| Posterior pituitary | ADH, oxytocin | Water retention, uterine contraction | Diabetes insipidus, SIADH |
| Thyroid | T3, T4, calcitonin | Metabolic rate, growth | Goitre, hypothyroidism, Graves' disease |
| Parathyroid | PTH | Raises blood calcium | Tetany after thyroidectomy |
| Adrenal cortex | Cortisol, aldosterone | Stress, sodium retention | Cushing's, Addison's disease |
| Adrenal medulla | Adrenaline | Fight or flight | Phaeochromocytoma |
| Pancreatic islets | Insulin, glucagon | Lower and raise glucose | Diabetes mellitus |

## 2.2 Thyroid, iodine and the thyroid axis

The thyroid lies in front of the trachea and is made of follicles filled with colloid, the store of thyroglobulin. The follicle cells trap **iodide**, join it to tyrosine and release **T4 (thyroxine)** and the more active **T3**, which raise the basal metabolic rate, heart rate and heat production and are essential for the growth of the brain in the foetus. The adult needs about **150 µg of iodine a day**; Nepal fights iodine deficiency by **iodised salt**, made with 30 parts per million (30 µg per g) iodine, so 5 g of salt supplies about 150 µg. Low iodine causes goitre in adults and cretinism (mental retardation) in children whose mothers were deficient, which is why the National Iodine Deficiency Disorders programme checks salt at the household with a test kit.

```photogrid label="2.1" cols="2" ratio="1.4" caption="The thyroid. (a) A real micrograph of human thyroid (H and E, 100x): round follicles filled with pink colloid, lined by one layer of cells. (b) The hypothalamus-pituitary-thyroid feedback loop: T4 and T3 switch off TRH and TSH."
@ photo id="nur2/thyroid" cap="Human thyroid follicles"
fit 1.4
focus 0.5 0.5
mark 0.30 0.62 "1"
mark 0.62 0.38 "2"
key 1 (a) A follicle: a ring of cells around pale colloid, the hormone store
key 2 (a) Interfollicular tissue with small vessels; active follicles are small with scalloped colloid
@ svg cap="Thyroid axis"
f = Fig(380, 270)
f.box(100, 10, 180, 44, "Hypothalamus\nreleases TRH", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(100, 90, 180, 44, "Anterior pituitary\nreleases TSH", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(100, 170, 180, 44, "Thyroid gland\nmakes T4 and T3 (iodine)", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.arrow([(190, 54), (190, 90)], color=SLATE, sw=2); f.arrow([(190, 134), (190, 170)], color=SLATE, sw=2)
f.arrow([(280, 192), (350, 192), (350, 112), (280, 112)], color=RED, sw=1.8, dash=True)
f.arrow([(350, 112), (350, 32), (280, 32)], color=RED, sw=1.8, dash=True)
f.text(335, 150, "negative", size=9.5, color=RED, bold=True); f.text(335, 163, "feedback", size=9.5, color=RED, bold=True)
f.text(190, 240, "Low T4: TSH high (primary hypothyroidism). High T4: TSH low (Graves').", size=10, color=SLATE, bold=True)
```

**Hypothyroidism** (low T4, high TSH) gives tiredness, cold intolerance, weight gain, constipation, dry skin and a slow pulse, and is treated with lifelong **levothyroxine** taken on an empty stomach 30 minutes before breakfast. **Hyperthyroidism** (Graves' disease) gives weight loss, heat intolerance, palpitations, tremor and bulging eyes; carbimazole, beta-blockers or surgery are used. After thyroidectomy the nurse watches for **airway swelling and hypocalcaemia** (tingling around the mouth, Chvostek's sign) because the parathyroids lie behind the thyroid.

## 2.3 The adrenal glands and the stress axis

The **adrenal cortex** makes cortisol, aldosterone and androgens; the **medulla** makes adrenaline. Stress triggers the **HPA axis**: the hypothalamus releases CRH, the pituitary releases ACTH, and the adrenal cortex releases **cortisol**, which raises blood glucose, suppresses inflammation and supports blood pressure. Cortisol then switches off CRH and ACTH. A patient on long-term prednisolone has a suppressed axis, so the steroid must **never be stopped suddenly** (adrenal crisis: low BP, vomiting, shock), and extra dose is needed in illness or surgery.

```svgfig label="2.2" caption="HPA axis. Stress raises CRH, ACTH and cortisol; cortisol feeds back to switch the axis off. Long-term steroid tablets act like cortisol, so the patient's own adrenal glands shrink."
f = Fig(760, 200)
st = [("Stress (illness,\nfear, surgery)", ROSE, RED), ("Hypothalamus\nCRH", SAND, AMBER), ("Pituitary\nACTH", BLUE, NAVY), ("Adrenal cortex\ncortisol", MINT, TEAL), ("Raised glucose,\nBP, less\ninflammation", MINT, TEAL)]
for i, (t_, fc, sc) in enumerate(st):
    x = 8 + i * 150; f.box(x, 40, 128, 66, t_, fill=fc, stroke=sc, size=10.5, bold=True)
    if i < 4: f.arrow([(x + 128, 73), (x + 150, 73)], color=SLATE, sw=2)
f.arrow([(514, 106), (514, 155), (214, 155)], color=RED, sw=1.8, dash=True)
f.arrow([(214, 155), (214, 106)], color=RED, sw=1.8, dash=True)
f.text(364, 175, "Negative feedback: cortisol switches off CRH and ACTH", size=10.5, color=RED, bold=True)
f.text(380, 20, "Hypothalamic-pituitary-adrenal axis", size=11, color=SLATE, bold=True)
```

## 2.4 The pancreas, insulin and diabetes mellitus

The pancreatic **islets of Langerhans** hold **beta cells** (insulin, lowers glucose by moving it into muscle, fat and liver) and **alpha cells** (glucagon, raises glucose by liver glycogen breakdown). Normal fasting plasma glucose is 70-99 mg/dL. **Diabetes mellitus** is diagnosed by fasting glucose of 126 mg/dL or more (7.0 mmol/L), a 2-hour glucose of 200 mg/dL or more (11.1 mmol/L), or **HbA1c of 6.5% or more**. **Type 1** is autoimmune destruction of beta cells (insulin always needed); **Type 2** is insulin resistance with relative lack, linked to obesity and ageing. The glucose in a capillary drop is measured by a meter, and HbA1c reflects the last 2-3 months.

```photogrid label="2.2" cols="3" ratio="1.1" caption="The pancreas and glucose. (a) A real micrograph of pancreatic tissue (H and E). (b) The steps of a finger-prick glucose test in an illustration (not a photograph): lance, drop, strip, meter. (c) Glucose control by insulin and glucagon."
@ photo id="nur2/islet" cap="Pancreatic tissue"
fit 1.1
focus 0.5 0.5
mark 0.35 0.62 "1"
mark 0.72 0.30 "2"
key 1 (a) Pale pocket of islet cells among the darker purple digestive acini
key 2 (a) Acinar cells: pink-purple clusters that make digestive enzymes
@ photo id="nur2/glucose" cap="Glucometer test (illustration)"
fit 1.1
focus 0.5 0.5
mark 0.66 0.78 "3"
mark 0.42 0.73 "4"
mark 0.82 0.60 "5"
key 3 (b) Lancet device: use the side of the fingertip and a new lancet each time
key 4 (b) Blood drop applied to the strip (about 0.5-1 microlitre)
key 5 (b) Meter reading: 100 mg/dL is normal fasting
@ svg cap="Insulin and glucagon"
f = Fig(300, 270)
f.box(80, 90, 140, 48, "Blood glucose\n70-99 mg/dL", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(10, 10, 130, 48, "High: beta cells\nrelease insulin", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.box(160, 10, 130, 48, "Low: alpha cells\nrelease glucagon", fill=ROSE, stroke=RED, size=10, bold=True)
f.box(10, 190, 130, 56, "Insulin: glucose into\ncells, glycogen made", fill=MINT, stroke=TEAL, size=10, bold=True)
f.box(160, 190, 130, 56, "Glucagon: liver\nbreaks glycogen", fill=MINT, stroke=TEAL, size=10, bold=True)
f.arrow([(110, 90), (80, 58)], color=NAVY, sw=1.8); f.arrow([(190, 90), (220, 58)], color=RED, sw=1.8)
f.arrow([(80, 190), (110, 138)], color=TEAL, sw=1.8); f.arrow([(220, 190), (190, 138)], color=TEAL, sw=1.8)
```

```python
a1c = 7.0
eag = 28.7 * a1c - 46.7
tdd = 0.5 * 60
cf = 1800 / tdd
icr = 500 / tdd
corr = (250 - 110) / cf
print(f"eAG = {eag:.1f} mg/dL = {eag / 18.016:.1f} mmol/L")
print(f"TDD = {tdd:.1f} U, basal = {tdd / 2:.1f} U")
print(f"ICR = 1 U per {icr:.1f} g; CF = {cf:.1f} mg/dL per U")
print(f"Correction for 250 mg/dL = {corr:.1f} U")
```

```text
eAG = 154.2 mg/dL = 8.6 mmol/L
TDD = 30.0 U, basal = 15.0 U
ICR = 1 U per 16.7 g; CF = 60.0 mg/dL per U
Correction for 250 mg/dL = 2.3 U
```

The block shows the arithmetic behind a basal-bolus plan for a 60 kg adult with HbA1c 7.0%. The **estimated average glucose** is 154.2 mg/dL (8.6 mmol/L). A starting **total daily dose** of 0.5 U/kg gives 30 U, half as basal insulin (15 U). The **500 rule** gives 1 unit per 16.7 g of carbohydrate, the **1800 rule** gives a correction factor of 60.0 mg/dL per unit, and for a reading of 250 mg/dL with a target of 110 the correction dose is 2.3 units, rounded by the doctor's order. These are teaching figures; the nurse always follows the prescribed regimen and checks it with a second nurse before giving insulin.

**Hypoglycaemia** (glucose below 70 mg/dL, 3.9 mmol/L) causes sweating, shaking, hunger and confusion: give 15 g of fast sugar (3 teaspoons of sugar in water or 150 mL of juice), repeat the test in 15 minutes, and give IV 10% dextrose if unconscious. **Diabetic ketoacidosis (DKA)** is insulin lack with fat breakdown to ketones: glucose is high, pH is below 7.30, bicarbonate is below 18 mmol/L and the anion gap is raised.

## 2.5 Diabetes self-care education: eight points

Nepal's PEN programme now screens for diabetes at primary care level, and nurses at health posts, diabetes clinics (Bir, Patan, Kathmandu Diabetes and Thyroid Centre) and in the community teach these eight points at every visit.

1. **Eat in a planned, balanced way.** Fill half the plate with vegetables, a quarter with dal or egg, and a quarter with rice, roti or other grain, and limit sugar, sweets, juice and sweet milk tea. Eating at fixed times keeps the glucose steady. Choose brown rice, millet (kodo) and whole wheat instead of polished rice.
2. **Move daily.** Walk briskly for 30 minutes on five days a week or do equal household and farm work. Muscles use glucose without needing much insulin. Check glucose before exercise and carry sugar in case of a low.
3. **Take medicine on time.** Metformin goes with meals, glimepiride before breakfast, and insulin exactly as prescribed. Missing doses makes the glucose run high, and extra doses cause lows. Never stop insulin when ill, even if not eating.
4. **Check sugar and know the targets.** Fasting glucose should be 80-130 mg/dL and HbA1c near 7%. Keep a diary of home readings and bring it to the clinic. HbA1c is checked every 3 months until stable.
5. **Care for the feet every day.** Look at both feet, including between the toes, each evening, wash and dry them, and apply moisturiser except between toes. Never walk barefoot, even indoors, and wear soft shoes with socks. A small blister can become an ulcer and lead to amputation because nerve damage hides the pain.
6. **Inject insulin correctly.** Rotate sites in the abdomen, thigh and upper arm, keep 2-3 cm from the last site, and use each needle once. Store unopened insulin in the fridge (2-8 °C) and the opened vial in a cool place for 28 days; in Nepal's hot months a clay pot with water works. Never freeze it.
7. **Prevent and treat low sugar.** Know the signs of sweating, shaking and hunger, and carry sugar or glucose tablets. Treat with 15 g of fast sugar and recheck in 15 minutes. Tell family how to give sugar and when to call for help.
8. **Go for regular checks and avoid risks.** Have eyes examined yearly (retinopathy), urine albumin and kidney tests yearly, BP at every visit, and a foot check by a nurse. Stop tobacco and alcohol, which speed up damage. Report vomiting with abdominal pain, fast breathing or drowsiness at once, because this may be DKA.

## Formula and fact sheet

- eAG (mg/dL) = 28.7 × HbA1c − 46.7; HbA1c 7.0% gives 154.2 mg/dL. Divide mg/dL by 18.016 for mmol/L.
- TDD = 0.5 U/kg (type 1 start) = 30 U for 60 kg; basal about half. ICR = 500 ÷ TDD = 16.7 g/U; CF = 1800 ÷ TDD = 60.0 mg/dL per U.
- Anion gap = Na − (Cl + HCO₃); normal 8-12. Corrected Na = measured Na + 0.016 × (glucose − 100).
- Effective osmolality = 2 × Na + glucose ÷ 18.016. Hypoglycaemia: below 70 mg/dL, treat with 15 g sugar.
- Diagnosis: fasting 126 mg/dL (7.0 mmol/L), 2-hour 200 mg/dL (11.1 mmol/L), HbA1c 6.5%.

## Chapter summary

- Hormones act by receptor; most loops are negative feedback through the hypothalamus and pituitary.
- Iodine is needed for T4 and T3; Nepal uses iodised salt to prevent goitre and cretinism.
- Long-term steroids suppress the HPA axis and must be tapered, never stopped suddenly.
- Insulin lowers glucose and glucagon raises it; diabetes is diagnosed by fasting glucose, 2-hour glucose or HbA1c.
- Foot care, insulin technique, treatment of lows and early reporting of DKA are the core of diabetes teaching.

## Practice

**MCQs (with reasons)**

1. In primary hypothyroidism the usual pattern is: (a) low T4, low TSH (b) low T4, high TSH (c) high T4, low TSH (d) high T4, high TSH.
2. The hormone that raises blood glucose is: (a) insulin (b) glucagon (c) ADH (d) calcitonin.
3. HbA1c of 7.0% corresponds to an average glucose of about: (a) 120 (b) 154 (c) 200 (d) 240 mg/dL.
4. Na 132, Cl 96 and HCO₃ 8 mmol/L give an anion gap of: (a) 28 (b) 36 (c) 12 (d) 20.
5. After thyroidectomy the nurse watches for tingling around the mouth because of: (a) hypoglycaemia (b) hypocalcaemia (c) hyperkalaemia (d) hypoxia.

::: note Answers and rationales
**1. (b).** When the thyroid fails, T4 is low, so feedback no longer holds TSH down and TSH is high. Low TSH with low T4 points to a pituitary cause.
**2. (b).** Glucagon from alpha cells breaks down liver glycogen. Insulin lowers glucose, and ADH and calcitonin act on water and calcium.
**3. (b).** 28.7 × 7.0 − 46.7 = 154.2 mg/dL. The value 200 matches an HbA1c of about 8.6%.
**4. (a).** 132 − (96 + 8) = 28, a high gap that shows unmeasured ketone acids; the normal gap is 8-12.
**5. (b).** The parathyroids may be damaged or removed, PTH falls and calcium drops; mouth tingling and a positive Chvostek's sign are early signs.
:::

**Short answer (3 marks): Insulin and glucagon.** Insulin is made by beta cells of the islets of Langerhans and lowers blood glucose by moving it into muscle and fat and by building glycogen in the liver. Glucagon from alpha cells does the opposite and raises glucose by breaking down glycogen. The two keep the fasting glucose at 70-99 mg/dL by negative feedback. Lack of insulin gives diabetes mellitus, and an overdose of insulin gives hypoglycaemia.

**Medium answer (5 marks): Describe the thyroid axis and the care of a patient on levothyroxine (Figure 2.1).** The hypothalamus releases **TRH**, which makes the anterior pituitary release **TSH**; TSH makes the thyroid follicles take up iodine and release **T4 and T3**, which raise the metabolic rate. Rising T3 and T4 switch off TRH and TSH by **negative feedback**. In hypothyroidism T4 is low and TSH high, and the patient has tiredness, cold intolerance, weight gain, constipation and a slow pulse. **Levothyroxine** is taken every morning on an empty stomach, 30 minutes before food, and not with iron or calcium. The nurse checks pulse and watches for overdose signs of palpitations, tremor and weight loss, arranges a TSH test 6-8 weeks after a dose change, teaches never to stop the drug, and promotes iodised salt (150 µg a day) in the family.

**Long answer (10 marks): Sita Rai, 45, known type 1 diabetic, 70 kg, is brought to the emergency department after 2 days of vomiting and missing insulin. She is drowsy, breathing deeply and fast (Kussmaul), with a dry tongue. Glucose 480 mg/dL, pH 7.10, HCO₃ 8 mmol/L, Na 132, Cl 96, K 4.6 mmol/L, ketones in urine. Discuss and prepare a nursing care plan.**

*Introduction.* This is **diabetic ketoacidosis (DKA)**: without insulin the body breaks down fat to ketones, causing acidosis, and high glucose causes an osmotic diuresis with dehydration. Her anion gap is 132 − (96 + 8) = **28**, markedly raised. The corrected sodium is 132 + 0.016 × (480 − 100) = **138.1 mmol/L** and her effective osmolality is 2 × 132 + 480 ÷ 18.016 = **290.6 mOsm/kg**. Her glucose is 26.6 mmol/L. Precipitating causes are missed insulin and infection.

*Management.* (1) Airway, oxygen, two large IV lines and monitoring. (2) **Fluids first:** 0.9% saline 1000 mL in the first hour; with a 15 drops/mL set this is 1000 × 15 ÷ 60 = **250 drops/min**, then 250-500 mL/h guided by urine and BP. (3) **Potassium** is checked before insulin: with K 4.6 mmol/L, add 20-30 mmol KCl per litre once urine flows; if K is below 3.3 mmol/L, insulin is held until it is replaced. (4) **Insulin** 0.1 U/kg/h = **7 U/h**; with 50 units in 50 mL saline (1 U/mL) set the pump at 7 mL/h. (5) Hourly glucose; when it falls below 200 mg/dL (11.1 mmol/L) add 5% dextrose and continue insulin until ketones clear. (6) Find and treat infection, and change to subcutaneous insulin with a 1-2 hour overlap.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** thirst, nausea, abdominal pain. **O:** dry tongue, sunken eyes, BP 90/60, pulse 120, glucose 480. | **Deficient fluid volume** related to osmotic diuresis and vomiting, as evidenced by dry mucosa, tachycardia and hypotension. | **Hydration:** BP above 100 systolic, urine at least 0.5 mL/kg/h, moist mucosa in 6 h. | 1. IV 0.9% saline as ordered with a pump; *restores circulating volume.* 2. Hourly urine output with catheter; *shows renal perfusion.* 3. Strict input-output chart; *guides fluid rate.* 4. Check lung sounds; *detects overload.* | Vital signs and urine hourly; goal met when urine exceeds 35 mL/h. |
| **O:** glucose 480, ketones present, pH 7.10, Kussmaul breathing. | **Unstable blood glucose level** related to insulin deficiency, as evidenced by hyperglycaemia and ketosis. | **Blood glucose level:** fall of 50-75 mg/dL per hour to below 200 mg/dL, ketones negative in 24 h. | 1. Insulin infusion by pump, double-checked; *stops ketone production.* 2. Capillary glucose hourly and K 2-hourly; *avoids hypoglycaemia and hypokalaemia.* 3. Add dextrose when below 200 mg/dL; *allows insulin to continue.* | Hourly glucose chart; ABG every 2-4 h. |
| **O:** RR 30 and deep, pH 7.10, drowsy (GCS 12). | **Risk for electrolyte imbalance and impaired gas exchange** related to acidosis and insulin therapy. | **Acid-base balance:** pH above 7.30, HCO₃ above 18, K 4-5 mmol/L in 24 h. | 1. ECG monitor and K level; *insulin drives potassium into cells.* 2. Neuro checks hourly; *cerebral oedema is a risk.* 3. Side-lying position, nil by mouth while drowsy; *prevents aspiration.* | ABG and electrolytes reviewed 2-hourly. |
| **S:** "I ran out of insulin." **O:** no glucometer at home, lives 6 hours from the district hospital. | **Ineffective health self-management** related to limited access and knowledge, as evidenced by missed insulin and DKA. | **Knowledge: diabetes management:** states sick-day rules and injection steps before discharge. | 1. Teach sick-day rules: never stop insulin, drink fluid, test sugar and ketones; *prevents recurrence.* 2. Demonstrate injection and sites with return demonstration; *builds skill.* 3. Link to the nearest PEN site and diabetes association for insulin supply. | Return demonstration correct; follow-up in 1 week. |

*Prevention and education.* Never skip insulin, use sick-day rules, carry a diabetes card, and report vomiting with fast breathing. *Conclusion.* DKA is a nursing emergency in which fluids, potassium and insulin are given in that order and checked hourly.

::: tip Exam tip
For DKA write the anion gap and corrected sodium with the patient's own numbers, then the order fluids, potassium, insulin. Always say "check potassium before insulin".
:::
