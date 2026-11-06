---
subject: Adult Nursing I
grade: BSc Nursing Year 2
unit: 3
title: Cardiovascular Nursing: Hypertension, Ischaemic Heart Disease, Heart Failure, Arrhythmias and Resuscitation
hours: 24
area: BSN 9 · Adult Nursing I · Unit 3
---

Heart and blood-vessel disease is the largest single killer in Nepal: **cardiovascular disease causes close to one in three deaths** and NCDs as a whole about 71% (WHO estimates), while **NDHS 2022 found raised blood pressure in 20% of adults aged 15 and over** and the 2019 STEPS survey found 24.5%, with more than half unaware. A nurse at the coronary care unit of a hospital in Kathmandu or at a health post doing PEN screening works with the same few conditions: hypertension, angina and heart attack, heart failure, rhythm disorders and cardiac arrest. Rheumatic heart disease still strikes young people in the hills. All arithmetic is checked by program.

::: key What this unit gives you
- Real photographs of a 12-lead ECG with ST elevation, an atrial fibrillation strip, a wall-mounted AED and a raised jugular venous pressure, with four SVG figures.
- BP categories (2025 AHA/ACC and Nepal PEN), MAP, pulse pressure, heart rate from the ECG, QTc, cardiac output and ejection fraction.
- Hypertension (eight education points), acute coronary syndrome (eight nursing points), heart failure (eight points), arrhythmia, BLS and defibrillation.
- Drug-dose, infusion and heparin calculations, model answers and a NANDA-I plan for a man with an acute anterior STEMI.
:::

## 3.1 Cardiovascular assessment and the numbers

Take the **pulse** (rate, rhythm, volume), **blood pressure** (sitting, arm at heart level, correct cuff, two readings), **jugular venous pressure**, **heart sounds and murmurs**, **peripheral oedema** (pitting), **capillary refill** (under 2 seconds) and **chest pain** (site, character, radiation, duration, relief, associated sweating or nausea). The **12-lead ECG** is the fastest test: it is done within **10 minutes** of arrival with chest pain. **Troponin**, chest X-ray and echocardiogram follow.

```svgfig label="3.1" caption="The normal ECG complex. The P wave is atrial depolarisation, the QRS complex is ventricular depolarisation (under 0.12 s), the ST segment is flat on the baseline and the T wave is ventricular repolarisation. On standard paper one small square is 0.04 s and one large square (5 small squares) is 0.20 s."
f = Fig(760, 210)
f.raw('<path d="M30,120 L130,120 Q150,90 170,120 L230,120 L245,135 L265,30 L285,150 L300,120 L380,120 Q415,70 450,120 L520,120 L535,135 L555,30 L575,150 L590,120 L650,120 Q680,90 710,120 L740,120" fill="none" stroke="#1E3A8A" stroke-width="3"/>')
f.text(150, 80, "P", size=13, color=NAVY, bold=True); f.text(265, 20, "R", size=13, color=NAVY, bold=True)
f.text(240, 152, "Q", size=12, color=NAVY, bold=True); f.text(286, 168, "S", size=12, color=NAVY, bold=True)
f.text(415, 60, "T", size=13, color=NAVY, bold=True)
f.line(245, 190, 300, 190, color=RED, sw=2); f.text(272, 205, "QRS under 0.12 s", size=10.5, color=RED, bold=True)
f.line(130, 190, 245, 190, color=TEAL, sw=2); f.text(188, 205, "PR 0.12-0.20 s", size=10.5, color=TEAL, bold=True)
f.line(330, 120, 380, 120, color=AMBER, sw=0); f.text(340, 108, "ST", size=11, color=AMBER, bold=True)
f.line(535, 190, 555, 190, color=NAVY, sw=0); f.text(620, 190, "R to R = 0.8 s = 75 per minute", size=11, color=NAVY, bold=True)
```

**BP categories (2025 AHA/ACC):** normal below 120/80, elevated 120-129 and below 80, **stage 1 hypertension 130-139 or 80-89**, **stage 2 hypertension 140 or above, or 90 or above**, hypertensive crisis 180 and/or 120 or above. The 2025 guideline keeps these cut points, sets a treatment goal below 130/80 for most adults, and prefers a combination pill when treatment starts at stage 2. The Nepal **PEN protocol (MoHP)** diagnoses hypertension at **140/90 or above** on repeated visits and bases treatment on this and on total cardiovascular risk, so use the protocol of the facility where you work.

```python
sbp, dbp = 150, 94
pp = sbp - dbp; mapx = (sbp + 2 * dbp) / 3
print(f"BP {sbp}/{dbp}: pulse pressure = {pp} mmHg; MAP = ({sbp} + 2 x {dbp}) / 3 = {mapx:.1f} mmHg")
print(f"Regular rhythm, 4 large squares R-R: 300/4 = {300 / 4:.0f}; 20 small squares: 1500/20 = {1500 / 20:.0f} per minute")
print(f"Irregular rhythm, 12 QRS in 6 s: 12 x 10 = {12 * 10} per minute")
rr = 60 / 75; qtc = 400 / rr ** 0.5
print(f"QTc (Bazett) = QT / sqrt(RR) = 400 / sqrt({rr:.1f}) = {qtc:.0f} ms (normal under 450 men, 460 women)")
co = 75 * 70; ef = 70 / 120 * 100
print(f"Cardiac output = 75 x 70 mL = {co:,} mL/min = {co / 1000:.2f} L/min; EF = 70/120 = {ef:.0f}%")
print(f"Furosemide 40 mg from 10 mg/mL = {40 / 10:.0f} mL; heparin 25,000 units in 500 mL = {25000 / 500:.0f} units/mL; 1,000 units/h = {1000 / 50:.0f} mL/h")
```

```text
BP 150/94: pulse pressure = 56 mmHg; MAP = (150 + 2 x 94) / 3 = 112.7 mmHg
Regular rhythm, 4 large squares R-R: 300/4 = 75; 20 small squares: 1500/20 = 75 per minute
Irregular rhythm, 12 QRS in 6 s: 12 x 10 = 120 per minute
QTc (Bazett) = QT / sqrt(RR) = 400 / sqrt(0.8) = 447 ms (normal under 450 men, 460 women)
Cardiac output = 75 x 70 mL = 5,250 mL/min = 5.25 L/min; EF = 70/120 = 58%
Furosemide 40 mg from 10 mg/mL = 4 mL; heparin 25,000 units in 500 mL = 50 units/mL; 1,000 units/h = 20 mL/h
```

A reading of 150/94 has a **pulse pressure of 56 mmHg** and a **mean arterial pressure of 112.7 mmHg** (a MAP of at least 65 keeps the organs perfused). On the ECG a regular rhythm with 4 large squares between R waves is **75 per minute**, with 20 small squares it is **75**, and for an irregular rhythm, 12 QRS complexes in a 6-second strip give **120 per minute**. A QT of 400 ms at 75 per minute corrects to a **QTc of 447 ms** (normal). The **cardiac output** (heart rate × stroke volume) is **5,250 mL/min**, and the **ejection fraction** is **58%** (normal 55-70%). Furosemide 40 mg from 10 mg/mL is **4 mL**; a heparin bag of 25,000 units in 500 mL holds 50 units/mL, so 1,000 units an hour runs at **20 mL/h**.

## 3.2 Hypertension

**Hypertension** is a sustained BP of 140/90 or above (or 130/80 in a high-risk person by the American guideline). In 90-95% of cases the cause is not found (**primary or essential**); the rest are **secondary** to kidney disease, endocrine disease (Cushing's, phaeochromocytoma, hyperaldosteronism), pregnancy or drugs. Risk factors in Nepal: **high salt intake (dal, pickles, tea with salt, processed noodles), tobacco and alcohol, overweight, inactivity, stress and family history**. Hypertension is usually silent; severe cases give headache, dizziness, blurred vision and nosebleed. Complications are stroke, myocardial infarction, heart failure, kidney failure and retinopathy. First-line drugs are **ACE inhibitors or ARBs, calcium channel blockers and thiazide-like diuretics**, taken daily and for life.

### Hypertension: eight points of health education

1. **Measure and know your numbers.** Check BP at least once a year after age 30 at the health post or pharmacy, and at home if advised. Sit quietly for 5 minutes with the arm at heart level. Write each reading in a diary and carry it to every visit.
2. **Reduce salt to under 5 g a day.** That is about one level teaspoon, including salt in pickles, dried fish, noodles and snacks. Taste food before adding salt. Lower salt lowers BP within weeks.
3. **Eat the DASH way.** Take more vegetables, fruit, dal, low-fat curd and whole grains, and less fried food and red meat. Potassium-rich food helps unless kidney disease is present. Use mustard oil sparingly.
4. **Be active.** Walk briskly for 30 minutes on most days, climbing hills where you can. Exercise lowers BP by 5-8 mmHg. Start slowly if you have not exercised before.
5. **Keep a healthy weight and waist.** Each 1 kg lost lowers systolic BP by about 1 mmHg. Aim for a BMI of 18.5-22.9 and a waist under 90 cm in men and 80 cm in women. Cut sugary drinks.
6. **Stop tobacco and limit alcohol.** Smoking and chewing tobacco injure vessels and raise stroke risk at once. Ask for help to quit. Local home-brewed alcohol (raksi) adds to BP and liver harm.
7. **Take drugs regularly.** Do not stop when you feel well, and do not skip doses to save money. Report cough with an ACE inhibitor, ankle swelling with amlodipine or dizziness on standing. Get refills before the tablets run out.
8. **Know the danger signs.** Sudden severe headache, chest pain, weakness of the face or limb, difficulty speaking or breathlessness need hospital care at once. A reading of 180/120 or more with symptoms is an emergency. Teach the family to recognise stroke with FAST.

## 3.3 Ischaemic heart disease: angina and myocardial infarction

**Ischaemic heart disease** results from narrowing of the coronary arteries by atheroma (fatty plaque). **Stable angina** is chest pain on effort, lasting under 15 minutes and relieved by rest or glyceryl trinitrate (GTN) under the tongue. **Acute coronary syndrome (ACS)** covers unstable angina and myocardial infarction (MI), where a plaque ruptures and a clot blocks the artery. **STEMI** shows ST elevation on the ECG, **NSTEMI** does not but troponin is raised. The pain of MI is crushing central chest pain lasting over 20 minutes, spreading to the left arm, jaw or back, with sweating, nausea and fear; diabetics and women may have only breathlessness. Risk factors: tobacco, hypertension, diabetes, raised cholesterol, obesity, inactivity and family history.

**Emergency treatment of STEMI:** oxygen only if SpO2 is below 90%, **aspirin 300 mg chewed**, a second antiplatelet (clopidogrel or ticagrelor), an anticoagulant (heparin or enoxaparin), GTN and **morphine** for pain, and a statin. **Reperfusion** is the key: **primary PCI** (balloon and stent) within 90 minutes of first medical contact where a catheter laboratory exists (in Nepal mainly in Kathmandu, Pokhara, Bharatpur, Butwal and a few other cities), or **thrombolysis** (streptokinase or tenecteplase) with a **door-to-needle time under 30 minutes** if PCI cannot be reached in 120 minutes.

```photogrid label="3.2" cols="4" ratio="1.0" caption="Cardiac recognition and rescue. (a) A real 12-lead ECG with ST-segment elevation: the arched ST segments mean the heart muscle is injured. (b) A real ECG strip of atrial fibrillation: irregularly irregular R-R intervals with no clear P waves. (c) A real wall-mounted automated external defibrillator (AED) with its sign. (d) A real photograph of a raised jugular venous pressure: the distended neck vein is marked with an arrow."
@ photo id="nur5/stemi" cap="STEMI ECG"
fit 1.0
focus 0.7 0.5
mark 0.80 0.82 "1"
mark 0.18 0.50 "2"
key 1 (a) ST elevation: the segment is arched above the baseline in several leads
key 2 (a) ECG grid paper: one small square is 0.04 s and 0.1 mV
@ photo id="nur5/afib" cap="Atrial fibrillation"
fit 1.0
focus 0.5 0.5
mark 0.50 0.60 "3"
key 3 (b) Irregularly irregular R-R intervals; no organised P waves; pulse deficit possible
@ photo id="nur5/aed" cap="Wall-mounted AED"
fit 1.0
focus 0.5 0.62
mark 0.50 0.08 "4"
mark 0.50 0.88 "5"
key 4 (c) The AED cabinet: open it and the device speaks the steps aloud
key 5 (c) The AED sign: marks the location so a bystander can find it quickly
@ photo id="nur5/jvp" cap="Raised JVP"
fit 1.0
focus 0.5 0.5
mark 0.50 0.58 "6"
key 6 (d) Distended neck vein (arrow): sign of raised right atrial pressure, as in right heart failure
```

### Acute coronary syndrome: eight points of nursing care

1. **Act fast and call for help.** Place the patient at rest in a semi-sitting position and record the ECG within 10 minutes. Time lost is muscle lost. Start continuous monitoring and keep the defibrillator at the bedside.
2. **Give the first drugs on time.** Chewed aspirin 300 mg, the second antiplatelet, an anticoagulant, GTN and a statin follow the doctor's order. Check allergy, bleeding risk and BP before GTN (hold if systolic BP is below 90). Record the time of each dose.
3. **Relieve pain and anxiety.** Pain raises heart work. Give IV morphine in small doses (2-4 mg) as ordered and assess the pain score every 5-10 minutes. A calm explanation to the patient and family reduces fear and oxygen demand.
4. **Prepare for reperfusion.** Obtain consent, take blood (troponin, CBC, creatinine, group), set up two IV lines and shave the groin or wrist for PCI. For streptokinase run the infusion over 60 minutes and have the antidote and adrenaline ready. Streptokinase can cause hypotension and allergy; do not give it again within 12 months.
5. **Monitor for complications.** Watch for arrhythmia (VF is commonest in the first hours), heart failure, cardiogenic shock, bleeding and a new murmur. Report a new rhythm, a fall in BP, crackles or oliguria. Reperfusion arrhythmias are expected and brief.
6. **Rest, then mobilise.** Bed rest for the first 12-24 hours with a bedside commode, then gradual sitting and walking as the doctor allows. Avoid straining; give a stool softener. Check pulse and BP before and after each activity.
7. **Nutrition and fluids.** Give small light meals low in salt and saturated fat and restrict fluid only if there is heart failure. Avoid very hot or very cold drinks. Record intake and output.
8. **Teach and plan the discharge.** Teach the drugs (aspirin, statin, beta-blocker, ACE inhibitor), stopping tobacco, a heart-healthy diet, exercise and cardiac rehabilitation. Explain when to use GTN and when to call for help (pain unrelieved by 2 doses 5 minutes apart). Return to sexual activity and work as the doctor advises, usually in 4-6 weeks.

## 3.4 Heart failure

**Heart failure** is a syndrome in which the heart cannot pump enough blood for the body's needs, or does so only at high filling pressures. **Left heart failure** causes breathlessness on effort, orthopnoea (needing pillows), paroxysmal nocturnal dyspnoea, cough with frothy sputum and crackles; **right heart failure** causes raised JVP, hepatomegaly, ankle oedema and ascites. Causes in Nepal: hypertension, coronary disease, **rheumatic valve disease**, cardiomyopathy, COPD (cor pulmonale) and anaemia. **Treatment** uses diuretics for congestion, ACE inhibitors or ARNI, beta-blockers, mineralocorticoid antagonists and SGLT2 inhibitors for survival, with oxygen and sitting up in acute pulmonary oedema.

```svgfig label="3.3" caption="The vicious cycle of heart failure and where each drug acts. A weak pump lowers cardiac output; the body responds with sympathetic and RAAS activation, which retains salt and water and narrows vessels. The extra load worsens the failure. ACE inhibitors, beta-blockers, MRAs and diuretics break the cycle."
f = Fig(760, 220)
f.box(10, 80, 150, 60, "Weak pump\nlow cardiac output", fill=ROSE, stroke=RED, size=11, bold=True)
f.box(210, 80, 160, 60, "SNS and RAAS\nactivated", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(420, 15, 160, 56, "Salt and water\nretained: preload up", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(420, 150, 160, 56, "Vasoconstriction:\nafterload up", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(620, 80, 130, 60, "Congestion,\noedema, strain", fill=ROSE, stroke=RED, size=11, bold=True)
f.arrow([(160, 110), (210, 110)], sw=2); f.arrow([(370, 100), (420, 55)], sw=2); f.arrow([(370, 120), (420, 168)], sw=2)
f.arrow([(580, 50), (640, 80)], sw=2); f.arrow([(580, 178), (640, 140)], sw=2); f.arrow([(685, 80), (685, 40), (85, 40), (85, 80)], sw=1.6, dash=True)
f.text(380, 205, "Drugs: ACEi/ARNI, beta-blocker, MRA, SGLT2i, diuretic", size=10.5, color=TEAL, bold=True)
```

### Heart failure: eight points of nursing care

1. **Position for breathing.** Sit the patient upright with the legs down (Fowler's) or leaning forward on a table. This pools blood in the legs and eases the lungs. Give oxygen if SpO2 is below 94%.
2. **Weigh every day.** Use the same scale, same time (after voiding, before breakfast) and light clothes. A gain of over 2 kg in 3 days means fluid is collecting and the doctor must be told. Record it in a chart.
3. **Restrict salt and, if ordered, fluid.** Advise under 2 g of sodium (5 g of salt) and about 1.5 L of fluid a day in severe cases. Small sips, ice chips and sugar-free sweets ease thirst. Check labels of packed food.
4. **Give diuretics wisely.** Give furosemide in the morning (twice a day: morning and early afternoon) to avoid night-time toilet trips. Weigh, record urine, watch for low potassium, cramps and dizziness. Replace potassium as ordered.
5. **Monitor vital signs and rhythm.** Check pulse, BP, breathing and SpO2 every 4 hours and more often if acute. Hold the beta-blocker if pulse is below 50 or systolic BP below 90. Listen for crackles and a third heart sound.
6. **Prevent skin breakdown and clots.** Oedematous skin breaks easily; change position every 2 hours and raise the legs when seated. Use stockings or heparin as ordered. Keep the skin clean and dry.
7. **Conserve energy.** Plan rest between care, allow sitting for meals and baths, and increase activity step by step. Short walks improve strength. Stop if the patient becomes breathless or dizzy.
8. **Teach self-care.** Teach daily weight, salt and fluid limits, drug names and timing, vaccines (influenza and pneumococcal) and the early signs of worsening: breathlessness, more pillows, swelling, rapid weight gain. Give clear Nepali instructions and a follow-up date.

## 3.5 Arrhythmias, defibrillation and basic life support

**Atrial fibrillation (AF)** is the commonest sustained arrhythmia: the atria quiver, the ventricles respond irregularly (Figure 3.2b), the pulse is irregularly irregular and clots may form in the left atrium, causing stroke. It is treated with rate control (beta-blocker, diltiazem, digoxin), anticoagulation (warfarin or a DOAC) and, in selected patients, cardioversion. **Ventricular tachycardia (VT) without a pulse and ventricular fibrillation (VF)** are **shockable** rhythms; **asystole and pulseless electrical activity (PEA)** are **non-shockable** and treated with CPR and adrenaline.

```svgfig label="3.4" caption="Basic life support for an unresponsive adult (BLS). Check safety and response, shout for help and call for the AED, check breathing for no more than 10 seconds, begin 30 compressions and 2 breaths at 100-120 per minute and at least 5 cm depth, attach the AED as soon as it arrives and follow its voice."
f = Fig(760, 230)
steps = [("1 Safe? Shake\nand shout", BLUE, NAVY), ("2 Call help,\nsend for AED", BLUE, NAVY), ("3 Breathing and\npulse, 10 s", SAND, AMBER), ("4 CPR 30:2\n100-120/min, 5 cm", ROSE, RED)]
for i, (t, fl, st) in enumerate(steps):
    x = 10 + i * 188
    f.box(x, 20, 170, 70, t, fill=fl, stroke=st, size=11, bold=True)
    if i < 3: f.arrow([(x + 170, 55), (x + 188, 55)], sw=2)
f.box(10, 140, 230, 70, "5 AED on: pads on bare, dry chest,\nstand clear, analyse", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(270, 140, 220, 70, "Shock advised: shock, then\nCPR 2 min at once", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(520, 140, 230, 70, "No shock: CPR 2 min;\ncontinue until help arrives", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.arrow([(745, 90), (745, 118), (125, 118), (125, 140)], sw=1.6, dash=True)
f.arrow([(240, 175), (270, 175)], sw=1.8); f.arrow([(490, 175), (520, 175)], sw=1.8)
```

**CPR in an adult:** push hard (at least 5 cm, not over 6 cm) and fast (100-120 per minute) in the centre of the chest, allow full recoil, minimise pauses, give 30 compressions to 2 breaths (or continuous compressions with an advanced airway). A **biphasic defibrillator** shock of **120-200 J** (as the manufacturer says) is delivered for VF or pulseless VT, followed at once by 2 minutes of CPR; **adrenaline 1 mg IV** is given every 3-5 minutes. Check the 4 Hs (hypoxia, hypovolaemia, hypo/hyperkalaemia, hypothermia) and 4 Ts (tension pneumothorax, tamponade, toxins, thrombosis). **Rheumatic heart disease**, caused by an immune reaction after streptococcal throat infection, is prevented by treating sore throat and by **benzathine penicillin G 1.2 million units IM every 3-4 weeks** for secondary prophylaxis, often provided free in Nepal's government hospitals.

```python
sbp, dbp = 100, 60
print(f"MAP = ({sbp} + 2 x {dbp}) / 3 = {(sbp + 2 * dbp) / 3:.1f} mmHg")
rate = 100 / 60; gtt = rate * 20
print(f"Streptokinase 1.5 million units in 100 mL over 60 min: {100 / 60 * 60:.0f} mL/h; macro 20 gtt/mL = {gtt:.1f} = {round(gtt)} gtt/min; micro = {rate * 60:.0f} gtt/min")
print(f"Enoxaparin 1 mg/kg x 70 kg = {1 * 70} mg; aspirin 300 mg from 75 mg tablets = {300 // 75}; atorvastatin 80 mg from 40 mg tablets = {80 // 40}")
```

```text
MAP = (100 + 2 x 60) / 3 = 73.3 mmHg
Streptokinase 1.5 million units in 100 mL over 60 min: 100 mL/h; macro 20 gtt/mL = 33.3 = 33 gtt/min; micro = 100 gtt/min
Enoxaparin 1 mg/kg x 70 kg = 70 mg; aspirin 300 mg from 75 mg tablets = 4; atorvastatin 80 mg from 40 mg tablets = 2
```

For the case below the **MAP is 73.3 mmHg** (100/60), the streptokinase infusion of 100 mL over 60 minutes runs at **100 mL/h, or 33 gtt/min** on a 20 gtt/mL set, **enoxaparin 1 mg/kg is 70 mg**, aspirin 300 mg is **4 tablets of 75 mg** and atorvastatin 80 mg is **2 tablets of 40 mg**.

## Formula and fact sheet

- MAP = (SBP + 2 × DBP) ÷ 3; pulse pressure = SBP - DBP; HR = 300 ÷ large squares = 1500 ÷ small squares; irregular rhythm: QRS in 6 s × 10.
- Cardiac output = HR × stroke volume; EF = SV ÷ EDV (normal 55-70%); QTc = QT ÷ √RR (seconds).
- STEMI: ECG in 10 min, aspirin 300 mg, PCI within 90 min or thrombolysis within 30 min; heparin units/h ÷ units per mL = mL/h.
- BLS: 30:2, 100-120 per minute, at least 5 cm, AED early; adrenaline 1 mg every 3-5 min; HF weight gain over 2 kg in 3 days is a warning.

## Chapter summary

- Assessment uses pulse, BP, JVP, oedema, ECG and troponin; the numbers MAP, rate and EF guide care.
- Hypertension is silent and controlled by salt reduction, exercise, weight loss, no tobacco and regular drugs.
- STEMI is a race: ECG in 10 minutes, antiplatelets, reperfusion, monitoring for arrhythmia and teaching for secondary prevention.
- Heart failure care is position, daily weight, salt and fluid limits, diuretics and teaching; BLS and the AED save lives in arrest.

## Practice

**MCQs (with reasons)**

1. The MAP of a patient with BP 120/80 is: (a) 80 (b) 93.3 (c) 100 (d) 120.
2. The heart rate with 6 large squares between R waves is: (a) 30 (b) 50 (c) 75 (d) 100.
3. Furosemide 20 mg is ordered from a 10 mg/mL ampoule: (a) 0.5 mL (b) 1 mL (c) 2 mL (d) 20 mL.
4. A heparin bag of 25,000 units in 250 mL must give 1,000 units/h: the rate is: (a) 5 mL/h (b) 10 mL/h (c) 20 mL/h (d) 40 mL/h.
5. The first drug given by mouth to a patient with suspected MI is: (a) paracetamol (b) aspirin 300 mg chewed (c) ibuprofen (d) salbutamol.

::: note Answers and rationales
**1. (b).** (120 + 2 × 80) ÷ 3 = 93.3; (c) is the simple average of 120 and 80, which ignores the longer diastole.
**2. (b).** 300 ÷ 6 = 50 per minute; 75 would need 4 large squares.
**3. (c).** Desired ÷ have = 20 ÷ 10 = 2 mL; (a) gives 5 mg.
**4. (b).** 25,000 ÷ 250 = 100 units/mL, and 1,000 ÷ 100 = 10 mL/h; (c) is the answer for a 500 mL bag.
**5. (b).** Chewed aspirin 300 mg blocks platelets and lowers death in MI; ibuprofen and other NSAIDs raise clot risk and paracetamol does not act on platelets.
:::

**Short answer (3 marks): Atrial fibrillation.** It is a rhythm in which the atria quiver and the ventricles beat irregularly, giving an irregularly irregular pulse and no P waves on the ECG. It causes palpitations, breathlessness and stroke from atrial clots. Treatment is rate control, anticoagulation and sometimes cardioversion; the nurse checks the apical and radial pulse, gives drugs on time and teaches stroke signs.

**Medium answer (5 marks): Describe the nursing care of a patient with heart failure (Figure 3.3).** Sit the patient upright with legs down and give oxygen if SpO2 is below 94%. Weigh daily and report a gain over 2 kg in 3 days. Limit salt to under 5 g and fluid if ordered. Give diuretics in the morning and record urine; watch for low potassium and dizziness. Monitor pulse, BP, breathing and SpO2, and hold the beta-blocker for pulse below 50 or systolic BP below 90. Prevent bed-sores and clots, plan rest with activity and teach the patient and family self-care, drugs, vaccines and warning signs.

**Long answer (10 marks): Mr Hari Prasad Sharma, 58 years, a shopkeeper and smoker of 20 years, 70 kg, arrives at the emergency department of a district hospital with crushing central chest pain for 45 minutes and sweating. ECG shows ST elevation in V1 to V4. Pulse 96, BP 100/60, SpO2 95%. The nearest PCI centre is 5 hours away. Plan his care.**

*Calculations.* His **MAP is 73.3 mmHg**, adequate but low. The doctor orders aspirin 300 mg (**4 tablets of 75 mg**), clopidogrel, **enoxaparin 1 mg/kg = 70 mg**, atorvastatin 80 mg (**2 tablets of 40 mg**) and thrombolysis with streptokinase 1.5 million units in 100 mL over 60 minutes: **100 mL/h, which is 33 gtt/min** on a 20 gtt/mL set. The door-to-needle target is under 30 minutes.

*Care.* Sit him at 45°, start continuous ECG monitoring and keep the defibrillator beside the bed. Record the ECG within 10 minutes, take blood for troponin, group and creatinine and insert two IV lines. Give the drugs on time and record the clock times. Give small doses of IV morphine for pain and reassess the pain score. Run the streptokinase infusion with BP every 15 minutes, watch for hypotension, allergy, bleeding and reperfusion arrhythmias, and have adrenaline and a defibrillator ready. Keep him on bed rest with a commode and give soft diet. Arrange transfer to a PCI-capable hospital after thrombolysis. Teach him and his family the drugs, tobacco cessation, diet and when to call for help.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "Crushing pain in my chest." **O:** ST elevation V1-V4, sweating. | **Acute pain** related to myocardial ischaemia, as evidenced by chest pain and diaphoresis. | **Pain level:** pain 3 or less within 30 minutes of treatment. | 1. Aspirin, GTN, morphine as ordered; *relieve ischaemia and pain.* 2. Rest in semi-sitting position; *lowers oxygen demand.* 3. Reassess pain score every 5-10 minutes; *shows response.* | Pain 2 out of 10 at 60 minutes. |
| **O:** BP 100/60, MAP 73.3, pulse 96. | **Decreased cardiac output** related to altered contractility, as evidenced by low BP and tachycardia. | **Cardiac pump effectiveness:** MAP at least 65, no arrhythmia, urine at least 0.5 mL/kg/h. | 1. Continuous ECG and BP every 15 minutes; *early arrhythmia detection.* 2. Thrombolysis with the correct drip rate; *reopens the artery.* 3. Record urine hourly; *shows perfusion.* | MAP 80, regular rhythm, urine 40 mL/h. |
| **S:** "Am I going to die?" **O:** restless, rapid speech. | **Anxiety** related to threat to life. | **Anxiety level:** reports calm and sleeps. | 1. Explain each step simply; *reduces fear.* 2. Allow a family member to stay; *comfort.* 3. Reduce noise; *lowers sympathetic drive.* | Calm and cooperative. |
| **O:** thrombolysis plus heparin. | **Risk for bleeding** related to thrombolytic and anticoagulant therapy. | **Blood loss severity:** no bleeding by discharge. | 1. Avoid IM injections and watch gums, urine, stool; *early sign of bleeding.* 2. Pressure on puncture sites; *stops oozing.* 3. Observe for headache and altered consciousness; *signs of intracranial bleed.* | No bleeding recorded. |

::: tip Exam tip
For an MI case write the MAP, the drug calculation, the 10-minute ECG, the 90- and 30-minute targets and four NANDA-I diagnoses beginning with acute pain and decreased cardiac output.
:::
