---
subject: Midwifery II
grade: BSc Nursing Year 3
unit: 3
title: Hypertensive Disorders of Pregnancy, Eclampsia and HELLP; Anaemia, Gestational Diabetes and Heart Disease in Pregnancy
hours: 28
area: BSN 19-20 · Midwifery II · Units 7-9
---

At 6 p.m. a jeep brings Rukmini Chaudhary, 20, a primigravida at 37 weeks, from a village in Bardiya to the district hospital. Four hours earlier she had a headache and blurred vision; one hour ago she **had a fit at home**. Her blood pressure is **176/118**, her urine shows **3+ protein**, and her knee jerks are brisk. The midwife has seconds to decide: **protect the airway, give magnesium sulfate, lower the pressure carefully, and deliver the baby**. Hypertensive disorders cause **12% of maternal deaths in Nepal (NMMS 2021)** and, with haemorrhage, are the leading direct cause. This unit builds on the basic ANC screening in Midwifery I and covers **classification, pathophysiology, severe features, the full magnesium sulfate regimen, antihypertensives, eclampsia first aid, HELLP syndrome, delivery and postpartum care**, followed by the three commonest **medical disorders**: **anaemia, gestational diabetes and heart disease**.

::: key What this unit gives you
- Real images: a **magnesium sulfate 1 g/2 mL vial**, **pitting oedema** of the legs, a **urine dipstick strip**, an **iron-deficiency blood smear** and an **IV iron sucrose drip**; numbered marks on strips of 3 and 2.
- SVG figures: the **pathophysiology of pre-eclampsia**, the **magnesium sulfate regimen with its toxicity checks**, and the **eclampsia emergency algorithm**.
- **Seven clinical manifestations of severe pre-eclampsia** and **eight points of nursing care in eclampsia**, each in 3-4 plain sentences, anchored in WHO recommendations, MoHP and the NMMS 2021.
- Verified maths: **mean arterial pressure**, **magnesium sulfate volumes and vial counts**, **infusion rate**, **calcium gluconate volume**, **Ganzoni iron deficit**, **glucose unit conversion**; MCQs, short, medium and long answers and a 5-column NANDA-I plan.
:::

## 3.1 Classification and diagnosis

Hypertension in pregnancy is **blood pressure of 140/90 mmHg or more on two readings 4 hours apart** (or a systolic of 160 or a diastolic of 110 on a single reading for **severe hypertension**), measured seated with a correct cuff after 5 minutes of rest. **Pre-eclampsia** is **new hypertension after 20 weeks with proteinuria or with another organ sign**. Protein is no longer essential for diagnosis if there are severe features.

| Disorder | Definition | Key points |
|---|---|---|
| **Chronic hypertension** | BP of 140/90 or more **before pregnancy or before 20 weeks** | Methyldopa, labetalol or nifedipine; avoid ACE inhibitors and ARBs |
| **Gestational hypertension** | New hypertension **after 20 weeks**, no proteinuria or organ signs; settles within 12 weeks postpartum | May progress to pre-eclampsia: weekly review |
| **Pre-eclampsia** | New hypertension after 20 weeks **plus** proteinuria (dipstick 1+ or protein:creatinine ratio 0.3 or more, or 300 mg per 24 hours) **or** organ dysfunction | Affects 2-8% of pregnancies |
| **Pre-eclampsia with severe features** | Above plus: BP 160/110 or more, platelets under 100,000, liver enzymes twice normal, creatinine over 1.1 mg/dL, pulmonary oedema, new headache or visual disturbance | Needs magnesium sulfate and delivery planning |
| **Eclampsia** | **Generalised convulsions** in a woman with pre-eclampsia, not due to another cause | Can occur before, during or up to 6 weeks after birth |
| **HELLP syndrome** | **H**aemolysis, **E**levated **L**iver enzymes, **L**ow **P**latelets (under 100,000) | Variant of severe pre-eclampsia; DIC, liver haematoma |
| **Superimposed pre-eclampsia** | Chronic hypertension plus new proteinuria or severe features | Higher risk than either alone |

**Risk factors.** First pregnancy, age under 18 or over 35, previous pre-eclampsia, family history, **chronic hypertension, diabetes, kidney disease, lupus**, twins, hydatidiform mole, obesity, and a long gap since the last birth. **Prevention** for high-risk women is **low-dose aspirin (75-150 mg at night from 12-16 weeks until 36 weeks)** and, in places with low dietary calcium, **calcium 1.5-2 g elemental daily** (WHO), alongside early ANC and BP checks at every visit. Nepal's ANC protocol checks BP and urine protein at every visit, and the Aama programme pays for the four contacts and for delivery in a health facility.

```svgfig label="3.1" caption="Pathophysiology of pre-eclampsia. Poor remodelling of the uterine spiral arteries leaves narrow, high-resistance vessels, so the placenta becomes ischaemic. The placenta releases anti-angiogenic factors (soluble Flt-1) and less placental growth factor into the mother's blood, causing widespread endothelial dysfunction: vasospasm, leaky capillaries and platelet activation. The results are hypertension, proteinuria (glomerular endotheliosis), oedema, headache and seizures (cerebral oedema), liver damage and HELLP, and poor placental perfusion causing growth restriction and abruption."
f = Fig(760, 330)
f.box(15, 15, 220, 60, "ABNORMAL PLACENTATION\nspiral arteries stay narrow\n(trophoblast invasion is shallow)", fill=SAND, stroke=AMBER, size=10, bold=True)
f.box(270, 15, 220, 60, "PLACENTAL ISCHAEMIA\nrelease of sFlt-1,\nless PlGF in maternal blood", fill=SAND, stroke=AMBER, size=10, bold=True)
f.box(525, 15, 220, 60, "ENDOTHELIAL DYSFUNCTION\nvasospasm, leaky capillaries,\nplatelet activation", fill=ROSE, stroke=RED, size=10, bold=True)
f.arrow([(235, 45), (270, 45)]); f.arrow([(490, 45), (525, 45)])
eff = [("BRAIN", "headache, visual blurring,\nbrisk reflexes, seizures", ROSE, RED), ("KIDNEY", "proteinuria, oliguria,\nrising creatinine", BLUE, NAVY), ("LIVER AND BLOOD", "epigastric pain, HELLP,\nlow platelets, DIC", ROSE, RED), ("HEART AND LUNG", "hypertension, pulmonary\noedema, heart failure", BLUE, NAVY), ("PLACENTA AND FETUS", "growth restriction, abruption,\noligohydramnios, preterm birth", SAND, AMBER), ("WHOLE BODY", "oedema of face, hands and\nfeet; rapid weight gain", MINT, TEAL)]
for i, (a, b, fl, st) in enumerate(eff):
    x, y = 15 + (i % 3) * 248, 125 + (i // 3) * 90
    f.box(x, y, 235, 78, a + "\n" + b, fill=fl, stroke=st, size=10.5, bold=True)
f.arrow([(635, 75), (635, 100)], color=SLATE, sw=1.6)
f.line(132, 100, 635, 100, color=SLATE, sw=1.6)
for _x in (132, 380, 628): f.arrow([(_x, 100), (_x, 125)], color=SLATE, sw=1.6)
f.text(380, 318, "Delivery of the placenta is the cure; the signs fade over days after birth", size=10.5, color=NAVY, bold=True)
```

### Seven clinical manifestations of severe pre-eclampsia

1. **Severe headache.** A frontal or occipital headache that does not go with paracetamol means swelling of the brain and a coming fit. The woman may hold her head or vomit. Treat any new headache after 20 weeks as a warning.
2. **Visual disturbance.** Blurred vision, flashing lights or spots mean spasm of the blood vessels of the retina and visual cortex. Ask every woman about her eyes at each visit. Sudden blindness is a late sign.
3. **Epigastric or right upper abdominal pain.** The liver capsule is stretched by swelling and bleeding. The pain is under the right ribs and may feel like indigestion. It often comes before HELLP and liver rupture.
4. **Severe hypertension (160/110 or more).** A very high pressure threatens a brain haemorrhage, so it needs treatment within 30-60 minutes. Take two readings 15 minutes apart with the right cuff size. Always compare with her booking pressure.
5. **Oliguria and heavy proteinuria.** Urine under 30 mL per hour or 3+ protein shows kidney damage. Put in a catheter and measure hourly. A rising creatinine means danger to the kidneys.
6. **Pulmonary oedema and breathlessness.** Fluid leaks into the lungs, and she gets crackles, cough and low oxygen. Restrict fluids to 80 mL per hour or less in total and sit her upright. This is a common cause of death.
7. **Hyper-reflexia and clonus.** Brisk knee jerks and sustained ankle clonus show a very irritable nervous system. They warn of a fit and also guide magnesium monitoring, because the reflex disappears as magnesium reaches toxic levels.

```photogrid label="3.1" cols="3" ratio="1.0" caption="Bedside clues and drugs in pre-eclampsia. (a) A magnesium sulfate 50% vial (1 g in 2 mL): the anticonvulsant of choice for severe pre-eclampsia and eclampsia. (b) Pitting oedema: a thumb press leaves a pit in the swollen leg; sudden oedema of the face and hands with weight gain over 1 kg a week is more specific. (c) A urine dipstick: the protein pad is read after 60 seconds and compared with the colour chart; 1+ or more is positive."
@ photo id="nur12/mgso4" cap="Magnesium sulfate 1 g per 2 mL vial"
fit 1.0
focus 0.5 0.45
mark 0.50 0.42 "1"
key 1 (a) Magnesium sulfate 50% (1 g in 2 mL)
@ photo id="nur12/edema" cap="Pitting oedema of the legs"
fit 1.0
focus 0.5 0.5
mark 0.30 0.62 "2"
key 2 (b) Thumb pressing the swollen leg, leaving a pit
@ photo id="nur12/dip" cap="Urine dipstick strips"
fit 1.0
focus 0.5 0.5
mark 0.40 0.42 "3"
key 3 (c) Pad read at 60 s against the colour chart
```

## 3.2 Treating severe hypertension and preventing fits

The aims are **to prevent fits (magnesium sulfate), to bring severe hypertension down safely (not too fast), to deliver the baby at the right time and to prevent complications**. Delivery is the only cure. WHO recommends that a woman with severe hypertension (160/110 or more) receives an **antihypertensive** and that **magnesium sulfate** be given to every woman with **severe pre-eclampsia or eclampsia**, in preference to diazepam or phenytoin.

| Drug | Dose and route | Cautions |
|---|---|---|
| **Labetalol** | 20 mg IV over 2 min; then 40 mg and 80 mg at 10-min intervals if needed (maximum 300 mg); oral 100-400 mg 8-12 hourly | Not in asthma or heart block; watch pulse (keep above 60) |
| **Nifedipine (immediate-release)** | 10 mg orally; repeat in 20-30 minutes if BP is still 160/110 or more; then 10-20 mg 4-6 hourly | Do not use the sublingual route; headache, flushing, reflex tachycardia |
| **Hydralazine** | 5 mg IV slowly; repeat every 20 minutes up to 20 mg | More fetal heart-rate changes; second line |
| **Methyldopa** | 250-500 mg orally 8 hourly (long-term) | Slow onset; depression, sedation |

**Target:** bring BP below 160/110 within 30-60 minutes, then to about 140-150/90-100 mmHg. A fall of more than 25% of the mean arterial pressure (MAP) in the first hour can reduce placental blood flow and cause fetal distress. **Avoid** ACE inhibitors and ARBs in pregnancy (fetal kidney damage, oligohydramnios).

## 3.3 Magnesium sulfate: the full regimen and its safety checks

**Magnesium sulfate (MgSO4)** blocks NMDA receptors and calcium channels, calms cerebral vasospasm and reduces the risk of eclampsia by more than half. It does not lower BP. In Nepal's birthing centres and hospitals the **Pritchard (IV + IM) regimen** is used with 50% solution (500 mg/mL; a 1 g vial is 2 mL).

```svgfig label="3.2" caption="Magnesium sulfate regimen and toxicity monitoring. Loading dose: 4 g IV (8 mL of 50% mixed with 12 mL normal saline to make 20 mL of 20% solution) slowly over 5-10 minutes, plus 10 g IM as 5 g (10 mL of 50% with 1 mL of 2% lignocaine) deep into each buttock. Maintenance: 5 g IM every 4 hours alternating buttocks, continued for 24 hours after delivery or after the last seizure, whichever is later. Before every dose check three things: respiratory rate of 16 or more per minute, patellar reflexes present, and urine output of at least 30 mL per hour over the previous 4 hours. If any check fails, withhold the next dose. Toxicity: loss of the knee jerk first (blood level about 7-10 mEq/L), then respiratory depression (12-15 mEq/L) and cardiac arrest at higher levels. Antidote: calcium gluconate 1 g (10 mL of 10%) IV over 10 minutes."
f = Fig(760, 340)
f.box(15, 15, 355, 110, "LOADING DOSE (Pritchard)\n\nIV: 4 g = 8 mL of 50% + 12 mL saline\n(20 mL of 20%) over 5-10 min\n\nIM: 5 g = 10 mL of 50% + 1 mL lignocaine\ninto EACH buttock (total 10 g)", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(390, 15, 355, 110, "MAINTENANCE\n\n5 g IM (10 mL of 50%) every 4 hours,\nalternate buttocks\n\nFor 24 h after delivery or last fit,\nwhichever is later", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.arrow([(370, 70), (390, 70)])
f.text(380, 150, "BEFORE EVERY DOSE CHECK ALL THREE (otherwise WITHHOLD and call a doctor)", size=11, color=RED, bold=True)
for i, (a, b) in enumerate([("RESPIRATIONS", "16 or more per minute"), ("KNEE JERK", "patellar reflex present"), ("URINE OUTPUT", "30 mL/h or more in 4 h")]):
    f.box(15 + i * 248, 165, 235, 56, a + "\n" + b, fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(15, 240, 355, 80, "TOXICITY LADDER\n7-10 mEq/L: knee jerk lost\n12-15 mEq/L: breathing slows, stops\nover 30 mEq/L: cardiac arrest", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(390, 240, 355, 80, "ANTIDOTE: CALCIUM GLUCONATE\n1 g = 10 mL of 10% slowly IV over 10 min\nBag and mask, oxygen, stop MgSO4\nKeep it at the bedside", fill=MINT, stroke=TEAL, size=10.5, bold=True)
```

If a **second fit** occurs 15 minutes after the loading dose, give **2 g IV (4 mL of 50% in 6 mL saline)** over 5 minutes. When only a loading dose can be given at a health post (WHO recommendation), give the **full loading dose and transfer** at once with a nurse and a written note. Use a pump or a burette for IV infusions: the **Zuspan regimen** is 4 g IV then **1 g per hour by infusion**. In renal failure the dose is reduced because magnesium is excreted by the kidneys.

## 3.4 Eclampsia: emergency care

```svgfig label="3.3" caption="Eclampsia emergency algorithm. At the first sign of a fit (loss of consciousness, tonic then clonic movements for 1-2 minutes) call for help and do not leave the woman. Airway and safety: left lateral position, clear the mouth, suction, oxygen 10 L/min once the fit ends, pad the bed sides. Circulation and drugs: IV line, MgSO4 loading dose, BP control with labetalol or nifedipine if 160/110 or more, catheter with hourly urine, fluid limited to 80 mL per hour. Assess the baby, the cervix and the blood tests. After the woman is stabilised (not during the fit), deliver: induction if the cervix is favourable and the baby is well, caesarean if not, within 12 hours of the first fit. Continue MgSO4 for 24 hours and monitor BP, reflexes, respiration and urine. Document and complete the MDR form if death occurs."
f = Fig(760, 340)
f.box(250, 10, 260, 40, "ECLAMPSIA: a fit in pre-eclampsia\nCALL FOR HELP, stay with her", fill=NAVY, stroke=NAVY, color="#ffffff", size=10.5, bold=True)
cols = [("AIRWAY AND SAFETY", "left lateral position\nclear mouth, suction\npad the bed sides\noxygen 10 L/min", MINT, TEAL), ("DRUGS AND CIRCULATION", "IV line, bloods\nMgSO4 loading dose\nlabetalol or nifedipine\nif BP 160/110 or more", BLUE, NAVY), ("MONITOR", "catheter, urine hourly\nfluids 80 mL/h at most\nBP, pulse, respiration,\nknee jerk every 15 min", SAND, AMBER), ("DELIVER", "after stabilisation\ninduce or caesarean\nwithin 12 hours;\nMgSO4 for 24 h after", ROSE, RED)]
for i, (a, b, fl, st) in enumerate(cols):
    x = 15 + i * 187
    f.box(x, 80, 175, 30, a, fill=st, stroke=st, color="#ffffff", size=10, bold=True)
    f.box(x, 114, 175, 106, b, fill=fl, stroke=st, size=10.5)
    f.arrow([(380, 50), (x + 87, 80)], color=SLATE, sw=1.2)
f.box(15, 240, 730, 36, "DO NOT: leave her alone, put anything between the teeth, give a rapid IV push of antihypertensive, or give oxytocin before her fit is controlled", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.text(380, 305, "Fits can recur up to 6 weeks postpartum: teach danger signs at discharge", size=10.5, color=NAVY, bold=True)
```

### Eight points of nursing care in eclampsia

1. **Protect the airway and prevent injury.** During the fit turn her to the left side, wipe the mouth, suction and keep the bed rails up. Put nothing between the teeth. Oxygen is given by mask once the fit has stopped.
2. **Call for help and never leave her.** A second fit can occur at any minute. Stay beside her, send another nurse for the doctor and the MgSO4 tray. Keep the room dark and quiet to reduce stimuli.
3. **Give magnesium sulfate exactly as ordered.** Check the strength (50%), the dose, the route and the time with a second nurse. Give IV over 5-10 minutes and the IM doses deep with lignocaine. Keep calcium gluconate and a bag-and-mask ready at the bedside.
4. **Monitor for magnesium toxicity before every dose.** Record respiratory rate (16 or more), patellar reflexes and hourly urine (30 mL/h or more). Stop if any check fails and call the doctor. Give calcium gluconate 10 mL of 10% IV over 10 minutes if breathing slows.
5. **Control blood pressure carefully.** Give labetalol or nifedipine as ordered and recheck in 15 minutes. Aim at 140-150/90-100, not lower. A rapid drop can cut blood flow to the baby and brain.
6. **Insert a catheter and limit fluids.** Record hourly urine output and give total fluids of 80 mL per hour or less (maintenance plus drugs) to avoid pulmonary oedema. Auscultate the lungs, and watch for cough and breathlessness.
7. **Watch the baby and prepare for birth.** Listen to the fetal heart or use CTG, give dexamethasone if under 34 weeks, and prepare for induction or caesarean after stabilisation. Have a newborn resuscitation team, warm cot and oxygen ready for a preterm or growth-restricted baby.
8. **Support the family and plan the follow-up.** Explain what is happening in Nepali, help the husband and mother stay calm, and respect privacy. After birth continue monitoring for 24-48 hours, check BP daily until it is normal and teach warning signs. Refer to a higher centre if she is in a health post, and complete the **MDR form within 24 hours** if she dies.

**HELLP syndrome** is haemolysis (schistocytes on smear, LDH 600 U/L or more), **elevated liver enzymes** (AST 70 U/L or more) and **low platelets** (under 100,000/mm³). Signs include epigastric pain, nausea and bleeding. Management is the same as severe pre-eclampsia with MgSO4 and prompt delivery; platelets under 50,000 need transfusion before caesarean, and dexamethasone is not routinely given to raise platelets. **Delivery timing:** pre-eclampsia without severe features at **37 weeks**; with severe features **after stabilisation at 34 weeks or more** (earlier for fits, HELLP, pulmonary oedema, abruption or fetal distress). **After birth** BP often peaks at days 3-6, so check it in the community; labetalol, nifedipine and enalapril are safe in breastfeeding. Women with pre-eclampsia have **2-4 times higher lifetime risk of hypertension and heart disease**.

## 3.5 Anaemia in pregnancy

**Anaemia in pregnancy** is haemoglobin **below 11 g/dL** in the first and third trimesters and **below 10.5 g/dL** in the second (WHO). **Mild** is 10.0-10.9, **moderate** 7.0-9.9 and **severe** below 7.0 g/dL. Plasma volume rises 40-50% but red cells only 20-30%, so a physiological dilution occurs; true anaemia is mostly **iron deficiency** (poor diet, hookworm, short birth intervals), sometimes **folate deficiency, malaria or thalassaemia**. NDHS 2022 found about **one in three women aged 15-49** anaemic. Anaemia raises the risk of **preterm birth, low birth weight, PPH, infection, heart failure and maternal death**.

**Features:** tiredness, pallor of the conjunctiva, palms and tongue, breathlessness, palpitation, oedema and a systolic flow murmur. **Investigations:** Hb, peripheral smear (microcytic hypochromic cells), ferritin, stool for ova, malaria test and sickle or thalassaemia screening where relevant.

```photogrid label="3.2" cols="2" ratio="1.3" caption="Anaemia in pregnancy. (a) A peripheral blood smear in iron-deficiency anaemia: pale, small red cells (microcytes and hypochromia) with increased central pallor and a few pencil-shaped cells, beside a normal-looking white cell. (b) An IV iron sucrose infusion: a dark brown iron solution diluted in a small bag of saline and given slowly through a drip set."
@ photo id="nur12/ida" cap="Iron-deficiency anaemia smear"
fit 1.3
focus 0.5 0.5
mark 0.30 0.70 "1"
mark 0.68 0.42 "2"
key 1 (a) Small pale red cells with wide central pallor
key 2 (a) White cell (lymphocyte) for size comparison
@ photo id="nur12/ironiv" cap="IV iron sucrose drip"
fit 1.3
focus 0.5 0.62
mark 0.45 0.62 "3"
mark 0.45 0.30 "4"
key 3 (b) Bag with dark iron sucrose solution
key 4 (b) Drip chamber and line to the patient
```

**Management.** *Prevention:* **iron-folic acid** daily from the first contact (60 mg elemental iron with 400 mcg folic acid; 180 tablets in Nepal's programme), **albendazole 400 mg** once after the first trimester, iron-rich food (green leafy vegetables, lentils, meat, with citrus; tea after meals reduces absorption) and birth spacing. *Treatment:* mild to moderate anaemia needs **oral iron 120 mg elemental daily** with folic acid, a repeat Hb in 4 weeks (a rise of 1 g/dL in 2-3 weeks shows response) and deworming. If there is no response, intolerance or late pregnancy, give **IV iron sucrose 200 mg in 100 mL saline over 20-30 minutes** (alternate days) calculated by the **Ganzoni formula** (below). *Severe anaemia (Hb under 7) after 36 weeks or in heart failure:* admit, give **packed red cells slowly** with furosemide cover, deliver in a CEONC with an active third stage and watch for PPH.

## 3.6 Gestational diabetes

**Gestational diabetes mellitus (GDM)** is glucose intolerance first recognised in pregnancy, screened at 24-28 weeks with a **75 g oral glucose tolerance test (OGTT)**. WHO and IADPSG criteria: **fasting 5.1-6.9 mmol/L (92-125 mg/dL), 1 hour 10.0 mmol/L (180 mg/dL) or more, 2 hours 8.5-11.0 mmol/L (153-199 mg/dL)**; any one value is enough. **Overt diabetes** is fasting 7.0 or more or 2 hours 11.1 or more. *Risks:* macrosomia, shoulder dystocia, neonatal hypoglycaemia, pre-eclampsia, stillbirth and later type 2 diabetes. *Management:* **diet** (small frequent meals, complex carbohydrates), exercise, **self-monitoring** (fasting below 5.3 mmol/L; 1 hour after meals below 7.8; 2 hours below 6.7), and **insulin** (or metformin) if targets are not met in 1-2 weeks. Deliver at 38-40 weeks (earlier for complications); stop insulin after birth, and check an OGTT at **6-12 weeks postpartum** and then yearly. The newborn's glucose is checked within 1-2 hours and feeds are started early. (Glucose mmol/L × 18 = mg/dL.)

## 3.7 Heart disease in pregnancy

**Rheumatic heart disease (mitral stenosis)** is the commonest heart disease in Nepal, followed by congenital defects and peripartum cardiomyopathy. Cardiac output rises 30-50% in pregnancy, peaking at **28-34 weeks**, in **labour** and in the **first hour after birth** (the uterus returns about 500 mL of blood). These are the danger periods for **pulmonary oedema and heart failure**.

| NYHA class | Symptoms | Pregnancy outlook |
|---|---|---|
| **I** | No limitation | Usually safe; ANC at a hospital |
| **II** | Slight limitation; ordinary activity causes breathlessness | Monthly review, rest, iron |
| **III** | Marked limitation; less than ordinary activity causes symptoms | Admit from 28 weeks; high risk |
| **IV** | Symptoms at rest | Very high risk; consider termination or admission for life |

*Care:* a **multidisciplinary team**, rest and left lateral position, low-salt diet, **treat anaemia, infection and arrhythmia**, **penicillin prophylaxis** for rheumatic fever (benzathine penicillin 1.2 MU IM every 3-4 weeks), diuretics for failure, and **LMWH (not warfarin early in pregnancy)** for mechanical valves. *Labour:* semi-sitting position, oxygen, **short second stage (assisted delivery)**, careful fluids, **no ergometrine**, slow oxytocin, and **caesarean for obstetric indications only**. *After birth:* watch closely for 48 hours, as pulmonary oedema often appears then, and advise reliable contraception.

## 3.8 Calculations

```python
sbp, dbp = 176, 118
map_ = (sbp + 2 * dbp) / 3                          # mean arterial pressure
floor = 0.75 * map_                                 # do not drop MAP by more than 25% in the first hour
load_iv, load_im, maint, doses = 4, 10, 5, 5        # g; maintenance doses every 4 h for 20 h after loading
total_g = load_iv + load_im + maint * doses
vials = total_g / 1                                 # 1 g per 2 mL vial
zus = 20 / 500 * 1000                               # mg/mL, 20 g in 500 mL
zus_ml_h = 1000 / zus                               # mL/h for 1 g/h
ca_ml = 1 / 0.1                                     # mL of 10% calcium gluconate for 1 g
fluid24 = 80 * 24
urine4 = 30 * 4
kg, hb, tgt = 55, 7.0, 11.0
ganzoni = kg * (tgt - hb) * 2.4 + 500               # iron deficit, mg
n200 = -(-ganzoni // 200)                           # doses of 200 mg (rounded up)
print(f"Rukmini: MAP {map_:.1f}; lowest safe MAP in 1 h {floor:.0f}; MgSO4 in 24 h {total_g} g = {vials:.0f} vials ({vials * 2:.0f} mL)")
print(f"Zuspan 20 g/500 mL: {zus:.0f} mg/mL, 1 g/h = {zus_ml_h:.0f} mL/h; calcium gluconate 1 g = {ca_ml:.0f} mL; fluid {fluid24} mL/24 h; urine needed {urine4} mL in 4 h")
print(f"Ganzoni for {kg} kg, Hb {hb}: {ganzoni:.0f} mg = {n200:.0f} doses of 200 mg; OGTT 5.1/10.0/8.5 mmol/L = {5.1 * 18:.0f}/{10.0 * 18:.0f}/{8.5 * 18:.0f} mg/dL")
```

```text
Rukmini: MAP 137.3; lowest safe MAP in 1 h 103; MgSO4 in 24 h 39 g = 39 vials (78 mL)
Zuspan 20 g/500 mL: 40 mg/mL, 1 g/h = 25 mL/h; calcium gluconate 1 g = 10 mL; fluid 1920 mL/24 h; urine needed 120 mL in 4 h
Ganzoni for 55 kg, Hb 7.0: 1028 mg = 6 doses of 200 mg; OGTT 5.1/10.0/8.5 mmol/L = 92/180/153 mg/dL
```

## Formula and fact sheet

- **Pre-eclampsia:** BP 140/90 or more after 20 weeks plus proteinuria or organ dysfunction; **severe** 160/110 or more, platelets under 100,000, liver enzymes twice normal, creatinine over 1.1 mg/dL, pulmonary oedema, headache or visual signs. **Eclampsia** = fits. **HELLP** = haemolysis, elevated liver enzymes, low platelets.
- **MAP** = (SBP + 2 × DBP) ÷ 3. Aim at 140-150/90-100; avoid a MAP fall over 25% in the first hour.
- **MgSO4 (Pritchard):** 4 g IV over 5-10 min + 5 g IM each buttock; then 5 g IM every 4 h for 24 h after birth or last fit. **Zuspan:** 4 g IV then 1 g/h. **Checks:** RR 16 or more, reflex present, urine 30 mL/h or more. **Antidote:** calcium gluconate 1 g (10 mL of 10%).
- **Antihypertensives:** labetalol 20-40-80 mg IV; nifedipine 10 mg oral (not sublingual); hydralazine 5 mg IV. No ACE inhibitor or ARB. **Aspirin** 75-150 mg from 12-16 weeks; **calcium** 1.5-2 g/day in low-intake areas.
- **Anaemia:** Hb under 11 (first and third trimesters), mild 10-10.9, moderate 7-9.9, severe under 7. **Ganzoni:** weight × (target Hb - actual Hb) × 2.4 + 500 mg. **IFA:** 60 mg iron + 400 mcg folic acid; 180 tablets.
- **GDM (75 g OGTT):** fasting 5.1, 1 h 10.0, 2 h 8.5 mmol/L (92, 180, 153 mg/dL). **Heart disease:** peak risk at 28-34 weeks, in labour and for the first hour postpartum.

## Chapter summary

- Pre-eclampsia is new hypertension after 20 weeks with proteinuria or organ dysfunction; eclampsia is a fit; HELLP is haemolysis, raised liver enzymes and low platelets; aspirin and calcium prevent in high-risk women.
- Severe features (BP 160/110, headache, visual signs, epigastric pain, oliguria, pulmonary oedema) need magnesium sulfate, careful BP control and delivery.
- The Pritchard regimen is 4 g IV plus 10 g IM, then 5 g IM every 4 hours; check respiration, reflexes and urine before every dose; calcium gluconate 1 g is the antidote.
- In eclampsia protect the airway, give MgSO4, control BP, limit fluids to 80 mL/h and deliver after stabilisation; continue MgSO4 for 24 hours.
- Anaemia, GDM and heart disease are treated with IFA and IV iron by the Ganzoni formula, diet and insulin by glucose targets, and multidisciplinary care in the danger periods.

## Practice

```python
mcq1 = (160 + 2 * 110) / 3                               # MCQ1 MAP at 160/110
mcq2 = 5 * 1                                             # MCQ2 vials of 1 g/2 mL for a 5 g dose
mcq3 = 20 / 500 * 25                                     # MCQ3 g/h, 20 g in 500 mL at 25 mL/h
mcq4 = 50 * (11 - 8) * 2.4 + 500                         # MCQ4 Ganzoni, 50 kg, Hb 8
mcq5 = 5.1 * 18                                          # MCQ5 mg/dL for 5.1 mmol/L
case_map = (176 + 2 * 118) / 3
case_vials = 4 + 10 + 5 * 5
print(f"MCQ1 = {mcq1:.1f}; MCQ2 = {mcq2} vials; MCQ3 = {mcq3:.1f} g/h; MCQ4 = {mcq4:.0f} mg; MCQ5 = {mcq5:.0f} mg/dL")
print(f"Rukmini: MAP {case_map:.1f}; MgSO4 vials in 24 h {case_vials}; urine needed 4 h {30 * 4} mL")
```

```text
MCQ1 = 126.7; MCQ2 = 5 vials; MCQ3 = 1.0 g/h; MCQ4 = 860 mg; MCQ5 = 92 mg/dL
Rukmini: MAP 137.3; MgSO4 vials in 24 h 39; urine needed 4 h 120 mL
```

**MCQs (with reasons)**

1. The mean arterial pressure at 160/110 mmHg is: (a) 110 (b) 126.7 (c) 135 (d) 160.
2. A 5 g IM dose of MgSO4 from 1 g/2 mL vials needs: (a) 2 vials (b) 5 vials (c) 10 vials (d) 20 vials.
3. 20 g of MgSO4 in 500 mL at 25 mL/h delivers: (a) 0.5 g/h (b) 1 g/h (c) 2 g/h (d) 4 g/h.
4. A woman of 50 kg has Hb 8 g/dL (target 11). The Ganzoni total iron requirement is about: (a) 360 mg (b) 500 mg (c) 860 mg (d) 1,360 mg.
5. A fasting glucose of 5.1 mmol/L is in mg/dL: (a) 56 (b) 92 (c) 102 (d) 180.

::: note Answers and rationales
**1. (b).** MAP = (160 + 2 × 110) ÷ 3 = 126.7. Using 110 or 160 alone ignores that the diastolic pressure counts twice.
**2. (b).** 1 g vials, 5 g = 5 vials (10 mL of 50%). Ten vials would be 10 g, the total IM loading dose, and 20 vials is a mistake of volume (mL) for number.
**3. (b).** 20 g ÷ 500 mL = 0.04 g/mL; × 25 mL/h = 1 g/h, the Zuspan maintenance rate. 2 g/h would risk toxicity.
**4. (c).** 50 × (11 - 8) × 2.4 = 360 mg, plus 500 mg for stores = 860 mg. 360 mg forgets the stores.
**5. (b).** 5.1 × 18 = 91.8, about 92 mg/dL, the WHO fasting cut-off for GDM. 180 mg/dL is the 1-hour value.
:::

**Short answer (3 marks): State the signs of magnesium sulfate toxicity and its antidote.** Check before every dose. **Loss of the patellar reflex** is the first sign (blood level about 7-10 mEq/L), then **respiratory rate under 16 per minute**, **urine output under 30 mL/h** (reduced excretion), then respiratory paralysis and cardiac arrest. **Stop the drug**, give oxygen and support breathing with a bag and mask, and give **calcium gluconate 1 g (10 mL of 10%) IV slowly over 10 minutes**.

**Medium answer (5 marks): Describe the Pritchard regimen of magnesium sulfate (Figure 3.2).** For severe pre-eclampsia and eclampsia: **loading dose** 4 g IV (8 mL of 50% in 12 mL saline, 20 mL of 20%) over 5-10 minutes, plus **10 g IM** as 5 g (10 mL of 50% with 1 mL of 2% lignocaine) deep in each buttock. **Maintenance** is 5 g IM every 4 hours, alternating buttocks, for **24 hours after delivery or last convulsion**. Before each dose check **respiratory rate 16 or more, patellar reflex present and urine output 30 mL/h or more**; if any fails, withhold the dose. For a recurrent fit give 2 g IV. In a health post, give the loading dose and refer at once. The antidote is **calcium gluconate 1 g IV**. MgSO4 does not lower blood pressure, so labetalol or nifedipine is given separately. It halves the risk of eclampsia. *Diagram:* two boxes (loading, maintenance) over three check boxes and a toxicity ladder.

**Long answer (10 marks): Rukmini Chaudhary, 20, primigravida at 37 weeks, 55 kg, has had a fit at home. BP 176/118, urine protein 3+, headache and brisk reflexes, fetal heart 136, cervix closed. Calculate her MAP, write her management and a nursing care plan.**

*Calculations.* Her **MAP is 137.3 mmHg** ((176 + 236) ÷ 3), so the lowest safe level in the first hour is about 103 mmHg (a 25% fall). Her **24-hour magnesium sulfate** is 4 g IV + 10 g IM + five 5 g doses = **39 g, or 39 vials** (1 g per 2 mL; 78 mL). The urine output needed before each dose is **120 mL** over 4 hours (30 mL/h). Fluids are limited to 80 mL/h (1,920 mL per day).

*Management.* The diagnosis is **eclampsia** (fit plus severe hypertension and proteinuria). During the fit the midwife turns her to the left side, clears the airway and calls for help; afterwards she gives oxygen at 10 L/min, puts in an IV line and takes blood for Hb, platelets, creatinine, liver enzymes and group. She gives **MgSO4 4 g IV** over 10 minutes and **5 g IM into each buttock**, then **nifedipine 10 mg orally** (repeat in 30 minutes) or labetalol 20 mg IV to bring the BP towards 150/100. A catheter measures hourly urine and the lungs are checked for crackles. The fetus is monitored (136, normal). When the fits are controlled and BP lowered, **delivery** is planned within 12 hours; with a closed cervix and a well baby she may have induction with misoprostol or oxytocin, but if the cervix is unfavourable or the baby is distressed, a **caesarean** is done at a CEONC (transfer with a nurse, drugs and a written note if at a BEONC). She continues MgSO4 for 24 hours after delivery, with checks before each dose, receives calcium gluconate at the bedside, and is watched for HELLP, PPH, pulmonary oedema and stroke. At discharge she is taught danger signs (headache, fits up to 6 weeks postpartum), family planning (avoid oestrogen pills while hypertensive) and annual BP checks, because she now has a higher lifetime cardiovascular risk. Data go into HMIS, and if she dies the MDR form is completed within 24 hours.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "My head is splitting; I can't see well." **O:** fit, BP 176/118, brisk reflexes | **Risk for injury** related to seizures and cerebral irritability | **Seizure control:** no further fit; protected from injury | Left lateral, bed rails, suction, quiet dark room; MgSO4 4 g IV + 10 g IM, 5 g every 4 h (prevents fits); stay with her | No fit in 24 h |
| **O:** MAP 137.3, BP 176/118 | **Ineffective cerebral tissue perfusion** related to severe hypertension and vasospasm | **BP control:** 140-150/90-100 in 1 h; no fall over 25% of MAP | Nifedipine 10 mg orally or labetalol 20 mg IV, recheck at 15 min (prevents stroke without placental hypoperfusion) | BP 148/98 at 1 h |
| **O:** respiration 20, reflexes brisk, urine to be measured | **Risk for ineffective breathing pattern** related to magnesium toxicity | **Respiratory status:** RR 16 or more, reflex present, urine at least 30 mL/h | Check RR, reflexes and urine hourly and before each dose; calcium gluconate 1 g and bag-mask at the bedside (early detection and rescue) | RR 18; reflex present; urine 40 mL/h |
| **O:** 37 weeks, FHR 136, cervix closed | **Risk for disturbed fetal blood flow** related to maternal hypertension | **Fetal status:** FHR 110-160; baby born alive | CTG or FHR every 15 min; plan delivery within 12 h; newborn team ready (maternal stabilisation then delivery) | FHR 140; baby cried after caesarean |
| **S:** "Will I have another fit? Will my baby live?" **O:** frightened | **Anxiety** related to emergency and threat to baby | **Anxiety level:** calm, understands the plan | Explain every step in Nepali, involve husband, give updates, keep privacy (reduces fear and promotes cooperation) | Calm; asks about feeding |
