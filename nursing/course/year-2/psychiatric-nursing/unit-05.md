---
subject: Psychiatric Nursing
grade: BSc Nursing Year 2
unit: 5
title: Substance Use, Psychiatric Emergencies and Community Psychiatry: Alcohol, Opioids, Agitation and Rehabilitation
hours: 16
area: BSN 13-14 · Psychiatric Nursing · Unit 5
---

At 3 a.m. a truck driver is brought to the Pokhara hospital by his brother. He stopped drinking two days ago, his hands shake, he is drenched in sweat, his pulse is 118, his temperature is 38.2 °C and he is brushing "insects" off the bed. He is in **alcohol withdrawal delirium (delirium tremens)**, a **medical emergency with a real risk of death** if untreated. In Nepal alcohol, including home-brewed *raksi*, *jaand* and *tongba*, is woven into festivals and daily life, **tobacco** use is common, **cannabis** (*ganja*, *charas*) and **opioids** are used, and injecting drug use has driven HIV spread in several districts. This unit also covers **psychiatric emergencies** (agitation, violence) and **community mental health and rehabilitation**, which return patients to life after the ward. All calculations are checked by program.

::: key What this unit gives you
- Real images: **alcoholic liver histology** and **Mallory bodies**, an **MRI of Wernicke encephalopathy**, fermented millet *tongba*, an **opium poppy**, **cannabis** under a Himalayan peak and a **methadone dispensing window**, with four SVG figures (cycle of change, alcohol withdrawal timeline, agitation algorithm, rehabilitation pathway).
- Dependence criteria, the **stages of change**, **standard drinks**, AUDIT, **CIWA-Ar**, a diazepam withdrawal regimen, **thiamine**, naloxone, methadone and **rapid tranquillisation** doses, all with checked calculations.
- Eight points each on alcohol withdrawal care, opioid care, managing agitation and community rehabilitation.
- Model answers and a NANDA-I care plan for a truck driver in withdrawal delirium.
:::

## 5.1 Substance use disorders: concepts

A **psychoactive substance** changes mood, perception or behaviour. Use ranges from **experimental** to **hazardous** (raises risk), **harmful** (damage already present) and **dependence**. **Dependence** (ICD-10) is present when **three or more** of the following occurred together in the past year: strong **craving**; **loss of control** over use; **withdrawal** on stopping; **tolerance** (needing more); **neglect** of other interests; and **persistence despite harm**. **DSM-5-TR** counts 11 criteria for a **substance use disorder**: **2-3 mild, 4-5 moderate, 6 or more severe**. Addiction is a **chronic, relapsing brain disorder** involving the dopamine reward pathway, not a moral weakness, and relapse rates (40-60%) resemble those of diabetes and hypertension.

**Nepal's legal setting:** the **Narcotic Drugs (Control) Act 2033 (1976)** controls cannabis, opium and heroin; the **Tobacco Product (Control and Regulatory) Act 2068** restricts smoking in public places and requires pictorial warnings; alcohol is regulated by local government and licensing. Government and NGO services provide **opioid substitution therapy (methadone, buprenorphine)** and needle-syringe programmes, and the **mhGAP** module for substance use is part of primary care training.

```svgfig label="5.1" caption="The cycle (stages) of change (Prochaska and DiClemente). People move round the wheel and often relapse and re-enter; relapse is a learning step, not failure. The nurse matches her approach to the stage: information and non-judgement early, goal-setting and skills in the middle, and relapse-prevention planning at the end."
f = Fig(760, 280)
f.box(20, 100, 150, 60, "PRE-CONTEMPLATION\n\"I have no problem\"\nraise awareness", fill=SOFT, stroke=SLATE, size=10.5, bold=True)
f.box(200, 30, 150, 60, "CONTEMPLATION\n\"maybe I should\"\nweigh pros and cons", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(400, 30, 150, 60, "PREPARATION\n\"I will start soon\"\nset a date and plan", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(590, 100, 150, 60, "ACTION\nstops or cuts down\nskills, support, drugs", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(400, 200, 150, 60, "MAINTENANCE\nkeeps the change\nrelapse prevention", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(200, 200, 150, 60, "RELAPSE\nreturn to use:\nre-enter, no blame", fill=ROSE, stroke=RED, color=RED, size=10.5, bold=True)
f.arrow([(170, 120), (230, 90)]); f.arrow([(350, 60), (400, 60)]); f.arrow([(550, 70), (620, 100)]); f.arrow([(650, 160), (550, 220)]); f.arrow([(400, 230), (350, 230)])
f.arrow([(230, 200), (110, 160)], color=RED, dash=True)
```

## 5.2 Alcohol: use, harm and withdrawal

A **standard drink** in the WHO scale holds **10 g of pure ethanol**. The **grams of alcohol = volume (mL) × strength (fraction) × 0.789** (the density of ethanol). Counting drinks lets the nurse judge risk in any Nepali setting. The **AUDIT** (Alcohol Use Disorders Identification Test) has 10 items (total 0-40): **0-7 low risk, 8-15 hazardous, 16-19 harmful, 20 or more possible dependence**.

```python
vol, abv = 650, 0.05                             # one large bottle of beer, 5% alcohol
grams = vol * abv * 0.789
drinks = grams / 10
bottles = 3                                      # a man drinks 3 bottles a day
daily_g = grams * bottles
audit = [3, 3, 2, 2, 2, 1, 2, 1, 2, 0]           # AUDIT items 1-10
a_total = sum(audit)
a_band = "low risk" if a_total <= 7 else "hazardous" if a_total <= 15 else "harmful" if a_total <= 19 else "possible dependence"
print(f"One 650 mL bottle at 5% = {grams:.1f} g ethanol = {drinks:.1f} standard drinks")
print(f"{bottles} bottles a day = {daily_g:.1f} g = {daily_g / 10:.1f} standard drinks")
print(f"AUDIT total = {a_total} ({a_band})")
```

```text
One 650 mL bottle at 5% = 25.6 g ethanol = 2.6 standard drinks
3 bottles a day = 76.9 g = 7.7 standard drinks
AUDIT total = 18 (harmful)
```

One large bottle of beer holds **25.6 g** of ethanol, **2.6 standard drinks**; three bottles a day is **76.9 g** or **7.7 standard drinks**. An AUDIT total of **18** is in the **harmful** range (16-19) and needs brief advice, assessment of dependence and referral if withdrawal is likely.

**Effects and complications.** Alcohol depresses the brain, damages the liver (fatty liver, **alcoholic hepatitis with Mallory bodies**, cirrhosis), the stomach and pancreas (gastritis, bleeding, pancreatitis), the heart (cardiomyopathy, arrhythmia), nerves (neuropathy) and the brain (**Wernicke encephalopathy and Korsakoff syndrome** from thiamine deficiency), and it causes road accidents, violence, self-harm and family breakdown. It is a leading preventable risk for **tuberculosis, injury and suicide** in Nepal.

```photogrid label="5.2" cols="3" ratio="1.0" caption="Alcohol and the organs. (a) A real liver biopsy under the microscope (H&E): the cells contain large clear fat vacuoles (steatosis), the earliest stage of alcoholic liver disease. (b) High-power view of alcoholic hepatitis: Mallory bodies are the pink irregular clumps inside swollen liver cells. (c) A real MRI (FLAIR) of Wernicke encephalopathy: bright signal around the third ventricle and in the thalami, caused by thiamine deficiency."
@ photo id="nur8/cirr" cap="Fatty liver (steatosis)"
fit 1.0
focus 0.5 0.5
mark 0.30 0.55 "1"
mark 0.70 0.45 "2"
key 1 (a) Large clear vacuoles: fat displacing the cell contents
key 2 (a) Pink liver tissue between the fatty cells: early scarring risk
@ photo id="nur8/mallory" cap="Mallory bodies"
fit 1.0
focus 0.5 0.5
mark 0.50 0.45 "3"
key 3 (b) Mallory body: pink hyaline clump inside a swollen hepatocyte
@ photo id="nur8/wern" cap="Wernicke MRI"
fit 1.0
focus 0.5 0.5
mark 0.43 0.55 "4"
mark 0.60 0.55 "5"
key 4 (c) Bright signal beside the third ventricle: brain damage from thiamine lack
key 5 (c) Bright thalamus: involved in memory, linked with Korsakoff syndrome
```

**Alcohol withdrawal** begins **6-24 hours** after the last drink in a dependent person. **Minor withdrawal** (6-24 h): tremor, sweating, anxiety, nausea, insomnia, fast pulse. **Seizures** (12-48 h). **Alcoholic hallucinosis** (12-48 h): hallucinations with clear consciousness. **Delirium tremens (48-96 h)**: confusion, vivid hallucinations (insects, animals), agitation, fever, high pulse and BP; it is **fatal in a few percent** even with treatment and more without. The **CIWA-Ar** scale (10 items, maximum 67) guides treatment: **below 8-10 minimal, 8-15 mild to moderate, 16 or more severe (needs medication)**.

```svgfig label="5.3" caption="Timeline of alcohol withdrawal after the last drink. Tremor and sweating start within hours; seizures peak at 12-48 hours; delirium tremens appears at 48-96 hours. Give thiamine before or with glucose, give benzodiazepines in a reducing course, hydrate, and monitor temperature, pulse, BP and CIWA-Ar scores."
f = Fig(760, 240)
f.line(30, 110, 730, 110, color=SLATE, sw=2.5)
for x, s in [(60, "6-24 h"), (240, "12-48 h"), (440, "48-96 h"), (650, "Day 5+")]:
    f.circle(x, 110, 6, fill=NAVY, stroke=NAVY); f.text(x, 134, s, size=11, color=NAVY, bold=True)
f.box(10, 30, 170, 56, "TREMOR, SWEATING\nanxiety, nausea,\ninsomnia", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(190, 30, 190, 56, "SEIZURES and\nHALLUCINOSIS\n(clear consciousness)", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(390, 30, 200, 56, "DELIRIUM TREMENS\nconfusion, fever, tachycardia,\nvivid hallucinations", fill=ROSE, stroke=RED, color=RED, size=10.5, bold=True)
f.box(600, 30, 150, 56, "SETTLES in most;\nWernicke risk persists", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(30, 160, 700, 60, "TREAT: thiamine (before glucose), diazepam in a reducing course, IV fluids and electrolytes (magnesium, potassium),\nquiet room, CIWA-Ar every 1-4 hours, treat infection and glucose, never leave a delirious patient alone", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
```

```python
ciwa = [3, 4, 3, 4, 3, 2, 2, 2, 2, 2]            # ten CIWA-Ar items
c_total = sum(ciwa)
status = "severe, give medication" if c_total >= 16 else "mild to moderate" if c_total >= 8 else "minimal"
reg = [(4, 10), (3, 10), (2, 10), (1, 10)]       # diazepam 10 mg tablets per day, days 1 to 4
tabs = sum(t for t, _ in reg)
mg = tabs * 10
thiamine = 200 * 3 * 3                           # 200 mg IV three times a day for 3 days (suspected Wernicke)
print(f"CIWA-Ar = {c_total} of 67 ({status})")
print(f"Diazepam 10 mg tablets: day 1 to 4 = {', '.join(str(t) for t, _ in reg)}; total = {tabs} tablets = {mg} mg")
print(f"Thiamine 200 mg IV three times a day for 3 days = {thiamine:,} mg")
```

```text
CIWA-Ar = 27 of 67 (severe, give medication)
Diazepam 10 mg tablets: day 1 to 4 = 4, 3, 2, 1; total = 10 tablets = 100 mg
Thiamine 200 mg IV three times a day for 3 days = 1,800 mg
```

A CIWA-Ar of **27** is **severe** (16 or more) and needs medication. The reducing regimen diazepam 10 mg four, three, two and one times a day over four days uses **10 tablets**, a total of **100 mg**. Thiamine 200 mg three times daily for three days (suspected Wernicke encephalopathy) totals **1,800 mg**. Doses are for understanding: always follow the doctor's order and the hospital protocol.

### Alcohol withdrawal: eight points of nursing care

1. **Assess quickly and repeatedly.** Record the time of the last drink, the usual amount, past seizures or delirium, other drugs and illness. Use CIWA-Ar every 1-4 hours and check temperature, pulse, BP, RR and glucose. Rising scores mean rising risk.
2. **Give thiamine first.** Thiamine goes **before or together with glucose**, because glucose alone can precipitate Wernicke encephalopathy. Give it by IM or IV as ordered, especially if there is confusion, ataxia or eye signs. Give oral vitamins and folate later.
3. **Give benzodiazepines as ordered.** Diazepam in a fixed reducing course or symptom-triggered by CIWA-Ar prevents seizures and delirium. Check sedation and breathing before every dose. Do not give extra doses without an order, and avoid combining with other sedatives.
4. **Maintain fluids and electrolytes.** Sweating, vomiting and fever cause dehydration. Give oral or IV fluids, and monitor magnesium, potassium and sodium. Record intake and output.
5. **Protect from injury.** Seizure precautions: padded bed rails, low bed, suction and oxygen at hand. Never restrain by force unless unavoidable. Keep a constant observer, with a relative if possible.
6. **Orient and reduce stimulation.** Use a quiet, well-lit room (shadows cause illusions), a clock, a calendar and familiar faces. Explain care simply. Do not argue with hallucinations; say "I do not see them but I know you are frightened."
7. **Watch for complications.** Alcohol users may bleed from the stomach or varices, have pancreatitis, pneumonia, head injury or hypoglycaemia. Report vomiting of blood, black stools, severe abdominal pain, fever or neck stiffness. Check the airway after seizures.
8. **Plan for recovery.** After detox, motivational interviewing (FRAMES: feedback, responsibility, advice, menu, empathy, self-efficacy), relapse prevention, naltrexone or acamprosate as the doctor chooses (disulfiram only with strong support), self-help groups and family counselling. Detoxification alone is not treatment.

## 5.3 Opioids, cannabis, tobacco and other substances

```photogrid label="5.4" cols="4" ratio="1.0" caption="Substances in Nepal. (a) Tongba: fermented millet in a bowl, sipped through a pipe with warm water, a traditional hill drink that contains alcohol. (b) The opium poppy (Papaver somniferum): the seed capsule yields the latex from which morphine, codeine and heroin come. (c) Cannabis plants growing wild in front of the Himalayas; cannabis cultivation, sale and use are illegal in Nepal. (d) A real methadone dispensing window where each dose is taken under observation."
@ photo id="nur8/tongba" cap="Tongba, fermented millet"
fit 1.0
focus 0.5 0.6
mark 0.45 0.32 "1"
key 1 (a) Fermented millet in a bowl: sipped with a pipe; contains alcohol
@ photo id="nur8/poppy" cap="Opium poppy"
fit 1.0
focus 0.5 0.5
mark 0.52 0.52 "2"
key 2 (b) Seed capsule at the flower centre: the source of opium latex
@ photo id="nur8/cann" cap="Cannabis plants"
fit 1.0
focus 0.35 0.5
mark 0.30 0.55 "3"
key 3 (c) Cannabis plant: sold as ganja, charas and bhang; illegal under the 1976 Act
@ photo id="nur8/metha" cap="Methadone dispensing"
fit 1.0
focus 0.6 0.5
mark 0.52 0.45 "4"
key 4 (d) Dispensing hatch: a daily observed dose, with staff counselling
```

| Substance | Intoxication | Withdrawal | Key nursing points |
|---|---|---|---|
| **Opioids** (heroin or "brown sugar", morphine, tramadol, codeine syrup; misused pharmaceutical injections such as buprenorphine ampoules) | Euphoria, **pinpoint pupils, slow breathing, coma** | Yawning, runny nose, dilated pupils, goosebumps, cramps, diarrhoea, aches; **not life-threatening**, very uncomfortable (**COWS**) | **Naloxone** for overdose; methadone or buprenorphine maintenance; **never share needles**; test for HIV, hepatitis B and C |
| **Cannabis** | Red eyes, dry mouth, appetite, anxiety, slow reaction, may induce psychosis | Irritability, poor sleep, low appetite, restlessness for 1-2 weeks | No specific drug; counselling; early use raises schizophrenia risk |
| **Stimulants** (methamphetamine "yaba" tablets, cocaine) | Alertness, euphoria, **fast pulse, high BP, hyperthermia, paranoia** | Crash: fatigue, depression, craving, suicide risk | Cool, calm, benzodiazepines for agitation; check ECG and temperature |
| **Sedatives** (diazepam, nitrazepam) | Drowsiness, slurred speech, ataxia | Anxiety, tremor, **seizures** (can be fatal) | Slow taper over weeks; flumazenil for overdose only in specialist hands |
| **Tobacco and nicotine** | Alertness | Irritability, craving, poor concentration, weight gain | **5 As** (ask, advise, assess, assist, arrange); nicotine gum or lozenge, bupropion or varenicline by doctor |
| **Inhalants** (glue, solvents, "dendrite") | Dizziness, euphoria, slurred speech, sudden death | Mild | Common in street children; protect, feed, link with shelters |

**Opioid emergencies.** Overdose gives the triad of **pinpoint pupils, respiratory rate below 10 and reduced consciousness**. Open the airway, ventilate with a bag-valve-mask and give **naloxone 0.4 mg** (IV, IM, SC or intranasal), repeated every 2-3 minutes up to about 2 mg if there is no response. Naloxone is short acting (30-90 minutes), so **watch for return of sedation**, especially after long-acting opioids such as methadone. **Opioid withdrawal** is scored by **COWS** (11 items): **5-12 mild, 13-24 moderate, 25-36 moderately severe, above 36 severe**. **Methadone** is a long-acting full agonist and **buprenorphine** is a partial agonist; both **stabilise the patient, reduce injecting and HIV risk and allow normal life**.

```python
nal_mg, nal_strength = 0.4, 0.4                  # naloxone 0.4 mg/mL ampoule
nal_ml = nal_mg / nal_strength
nal_total_mg, nal_total_ml = 2.0, 2.0 / nal_strength
cows = [2, 2, 2, 1, 2, 1, 2, 1, 2, 2, 1]         # eleven COWS items
c_total = sum(cows)
band = "mild" if c_total <= 12 else "moderate" if c_total <= 24 else "moderately severe" if c_total <= 36 else "severe"
meth_mg, meth_strength, days = 80, 5.0, 28       # methadone 80 mg a day, 5 mg/mL syrup
meth_ml = meth_mg / meth_strength
meth_total = meth_mg * days
print(f"Naloxone {nal_mg} mg from {nal_strength} mg/mL = {nal_ml:.1f} mL; 2 mg in total = {nal_total_ml:.0f} mL")
print(f"COWS total = {c_total} ({band})")
print(f"Methadone {meth_mg} mg from {meth_strength:.0f} mg/mL = {meth_ml:.0f} mL a day; {days} days = {meth_total:,} mg")
```

```text
Naloxone 0.4 mg from 0.4 mg/mL = 1.0 mL; 2 mg in total = 5 mL
COWS total = 18 (moderate)
Methadone 80 mg from 5 mg/mL = 16 mL a day; 28 days = 2,240 mg
```

A naloxone dose of 0.4 mg from a 0.4 mg/mL ampoule is **1.0 mL**, and 2 mg in all is **5 mL**. A COWS score of **18** is **moderate** (13-24). Methadone 80 mg from a 5 mg/mL syrup is **16 mL**, and 28 days total **2,240 mg**. (Strengths of syrups differ between suppliers: always read the label.)

### Opioid use disorder and overdose: eight points of nursing care

1. **Treat the overdose first.** Call for help, open the airway, give oxygen or bag-mask ventilation, then naloxone as ordered. Place the patient on the side and monitor breathing for at least 2 hours. Do not leave the patient alone, since the sedation may return.
2. **Assess without judging.** Ask about substances, route, last use, injecting sites, sharing of needles and overdose history. Use respectful words ("person who uses drugs", not "addict"). Stigma keeps people away from care.
3. **Score and treat withdrawal.** Use the COWS, give fluids, rest, antiemetic, antidiarrhoeal and analgesic as ordered, and start buprenorphine or methadone when the doctor decides. Explain that withdrawal is miserable but not dangerous. Treat the person, not only the symptom.
4. **Prevent infection.** Offer HIV, hepatitis B and C and TB screening, hepatitis B vaccine and counselling. Teach never to share needles, syringes or spoons, and to use needle-syringe programme services. Examine injection sites for abscess or thrombophlebitis.
5. **Give substitution therapy correctly.** Methadone is taken daily under observation; check identity, dose and the swallow. Watch for sedation, QT prolongation (ECG) and interactions with alcohol and benzodiazepines. Never stop abruptly; missed doses of more than 3 days need a new assessment.
6. **Teach overdose prevention.** Tolerance falls after detox or jail, so the old dose can kill. Teach family to call for help, recovery position and naloxone use where available. Never use alone.
7. **Address mental and physical health.** Screen for depression, PTSD, suicide risk and psychosis, and treat TB, wounds, malnutrition and dental disease. Pregnant women are offered treatment and antenatal care without judgement. Plan contraception.
8. **Support recovery and rights.** Link with rehabilitation centres, peer groups (NA), vocational training and family counselling. Teach the family about relapse as part of recovery. Protect confidentiality and the right to treatment.

## 5.4 Psychiatric emergencies: agitation and violence

An **agitated or violent patient** is the commonest psychiatric emergency. Causes include **psychosis, mania, delirium, intoxication or withdrawal, head injury, hypoglycaemia, epilepsy, pain and fear**. Always **exclude a medical cause**. The guiding rule is the **least restrictive measure that keeps everyone safe**: **verbal de-escalation first**, then medicine by mouth, then injection, and physical restraint only last.

```svgfig label="5.5" caption="Managing an agitated patient. Check safety and cause, de-escalate with calm talk and choices, offer oral medicine, and give rapid tranquillisation by injection only if danger continues. Physical restraint is the last step, is brief, done by a trained team and followed by monitoring and a debrief."
f = Fig(760, 250)
f.box(10, 90, 130, 70, "1. SAFETY and\nCAUSE: space, exit,\nteam, glucose, vitals", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(160, 90, 130, 70, "2. DE-ESCALATE:\ncalm voice, choices,\nlisten, no threats", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(310, 90, 130, 70, "3. ORAL medicine\nif accepted\n(lorazepam or\nolanzapine)", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(460, 90, 140, 70, "4. INJECTION (rapid\ntranquillisation):\nhaloperidol +\npromethazine IM", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(620, 90, 130, 70, "5. RESTRAINT last:\ntrained team, short,\nobserve, record", fill=ROSE, stroke=RED, color=RED, size=10.5, bold=True)
f.arrow([(140, 125), (160, 125)]); f.arrow([(290, 125), (310, 125)]); f.arrow([(440, 125), (460, 125)]); f.arrow([(600, 125), (620, 125)])
f.box(10, 190, 740, 50, "AFTER: observe every 15 minutes (RR, BP, SpO2, consciousness), treat the cause, debrief the patient and the staff, record and review", fill=SOFT, stroke=SLATE, size=10.5, bold=True)
f.text(380, 40, "Least restrictive first", size=12, color=NAVY, bold=True)
```

```python
halo_mg, halo_str = 5.0, 5.0                     # haloperidol 5 mg/mL
prom_mg, prom_str = 25.0, 25.0                   # promethazine 25 mg/mL
halo_ml, prom_ml = halo_mg / halo_str, prom_mg / prom_str
checks = 60 // 15                                # observations in the first hour at 15-minute intervals
print(f"Haloperidol {halo_mg:.0f} mg = {halo_ml:.1f} mL; promethazine {prom_mg:.0f} mg = {prom_ml:.1f} mL")
print(f"Observation checks in the first hour at 15-minute intervals = {checks}")
```

```text
Haloperidol 5 mg = 1.0 mL; promethazine 25 mg = 1.0 mL
Observation checks in the first hour at 15-minute intervals = 4
```

Rapid tranquillisation commonly uses **haloperidol 5 mg IM (1.0 mL of 5 mg/mL)** with **promethazine 25 mg IM (1.0 mL of 25 mg/mL)**, or a benzodiazepine, as the hospital protocol and doctor order; promethazine also lowers the risk of dystonia. After an injection the nurse records **4 observation checks in the first hour** (every 15 minutes) of breathing, BP, pulse, SpO2 and consciousness, and keeps the patient in view.

### Agitation and violence: eight points of nursing care

1. **Keep yourself and others safe.** Stay near the exit, keep an arm's length plus, remove sharp objects, call the team early and never be alone with a violent patient. Keep a calm face and open hands. Early help prevents injury.
2. **Respect personal space and speak calmly.** Stand at an angle, keep one person talking, use a low, slow voice, short sentences, and do not shout, point, stare or touch without warning. Respect lowers fear, which drives most violence.
3. **Listen and find what the patient wants.** Ask what is wrong, repeat back what you heard and agree where you can ("I understand you are angry that no one told you"). Offer choices: "Would you like water or to sit in the quiet room?" Never make promises you cannot keep.
4. **Set limits kindly and clearly.** "I cannot allow you to hit anyone. If you can calm down we can talk; if not, we will help you with medicine." State the consequence once, offer a way out, and keep the same message from all staff.
5. **Look for the cause.** Check glucose, temperature, oxygen, pain, full bladder, intoxication, withdrawal, head injury and drug effects. Treat what is treatable. Delirium and hypoglycaemia are missed when agitation is called "behaviour".
6. **Give medicine in the least restrictive way.** Offer oral medicine first. If danger persists, give injection as ordered, with enough staff and a clear plan, and explain afterwards. Check airway, BP, pulse, RR and SpO2 after every injection.
7. **Use restraint only as a last resort.** A trained team of at least four uses a hold with the head protected, never prone, never on the chest, and never to punish. A doctor orders it, it is brief, a nurse watches the airway and colour all the time, and it is recorded with the reason, time and end. Remove restraint as soon as safe.
8. **Debrief and prevent.** Afterwards, talk with the patient about what happened, and check injuries. Staff debrief learns which trigger or ward factor to change. Use advance plans and early warning signs to reduce repeat events.

## 5.5 Community psychiatry and rehabilitation

**Community mental health care** aims to treat people **where they live**, avoiding long admissions. In Nepal this follows the **mhGAP**, the **Community Mental Health Care Package 2017** and the **National Mental Health Strategy and Action Plan 2020**, with trained health workers at health posts, **free essential psychotropic medicines**, FCHVs who identify and refer, NGO counsellors (TPO Nepal, CMC-Nepal), community-based rehabilitation and self-help groups. **Rehabilitation** restores the skills, roles and rights lost to illness: self-care, social skills, education, work and housing.

```svgfig label="5.6" caption="The pathway of recovery in the community. After hospital the patient returns to the health post for medicine and follow-up, the FCHV and family give daily support, rehabilitation builds skills and work, and a relapse plan with early signs links back to treatment. Hospital is a short step in a long journey."
f = Fig(760, 240)
f.box(10, 90, 130, 70, "HOSPITAL\nstabilise, plan\ndischarge", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(170, 90, 140, 70, "HEALTH POST\nmedicine, follow-up,\nmhGAP worker", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(340, 90, 140, 70, "HOME and FCHV\nfamily support, daily\ntablets, early signs", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(510, 90, 120, 70, "REHAB\nskills, work,\nschool, groups", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(660, 90, 90, 70, "LIFE\nrole, income,\nrights", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.arrow([(140, 125), (170, 125)]); f.arrow([(310, 125), (340, 125)]); f.arrow([(480, 125), (510, 125)]); f.arrow([(630, 125), (660, 125)])
f.arrow([(400, 90), (400, 40), (240, 40), (240, 90)], color=RED, dash=True, label="early relapse signs: return for review", lpos=(320, 30))
f.text(380, 205, "Aim: recovery, independence and community acceptance", size=12, color=NAVY, bold=True)
```

### Community rehabilitation: eight points of nursing responsibility

1. **Start discharge planning on admission.** Plan medicines, follow-up date, home setting, finance and supports with the patient and family from day one. Give a written plan and a 4-6 week supply of medicine where permitted. A planned discharge halves early readmission.
2. **Ensure continuity of medicine.** Link with the nearest health post and FCHV for supply and reminders; teach the family to supervise. Use depot injections when adherence is poor. Missed medicine is the commonest cause of relapse.
3. **Teach relapse signs and the action plan.** Write the patient's own early signs (poor sleep, withdrawal, suspicion, irritability, stopping tablets) and exactly what to do and whom to call. Review it at every visit. Early return prevents admission.
4. **Support the family.** Provide psychoeducation, practical skills to reduce criticism and over-involvement, and respite and counselling for carers. Link with family groups and the social worker. Carers who are supported provide better care.
5. **Build daily living and social skills.** Use occupational therapy, daily routines, hygiene, money handling, cooking, travel and communication practice. Praise each step and set small goals. Skills make independence possible.
6. **Promote work and education.** Link to vocational training, supported employment, farming, handicrafts, tailoring and returning to school. Work gives income, role and self-esteem. Employers and teachers may need education and reassurance.
7. **Fight stigma and protect rights.** Teach the community in plain language, using stories of recovery and local leaders, schools and mothers' groups. Support disability certification and social security allowances where eligible, and challenge abuse and chaining. Respect confidentiality.
8. **Monitor physical health and wellbeing.** Check weight, BP, glucose, smoking and alcohol, TB and dental health at follow-up, since people with severe mental illness die about 10-20 years earlier than others. Promote exercise, nutrition and sleep. Treat the whole person.

## Formula and fact sheet

- Alcohol (g) = volume (mL) × strength × 0.789; standard drink = 10 g. AUDIT: 0-7, 8-15, 16-19, 20 or more. CIWA-Ar 16 or more needs medicine.
- Withdrawal: tremor 6-24 h, seizures 12-48 h, delirium tremens 48-96 h. Thiamine before glucose.
- Naloxone 0.4 mg every 2-3 minutes (up to about 2 mg); COWS 5-12, 13-24, 25-36, above 36. Volume = dose ÷ strength.
- Agitation: de-escalate, oral, injection, restraint last; observe every 15 minutes; community care follows mhGAP.

## Chapter summary

- Substance dependence is a chronic relapsing brain disorder; match care to the stage of change and avoid blame.
- Alcohol withdrawal is dangerous: give thiamine, benzodiazepines, fluids and constant observation; use CIWA-Ar.
- Opioid overdose needs airway care and naloxone; methadone or buprenorphine and harm-reduction services reduce death and HIV.
- Manage agitation with the least restrictive measures; rehabilitation and community care in Nepal depend on mhGAP, family and FCHV support.

## Practice

```python
m1 = 60 * 0.40 * 0.789                           # MCQ1 grams in 60 mL of 40% spirit
m2 = 0.4 / 0.4                                   # MCQ2 naloxone volume
m3 = 80 / 5.0                                    # MCQ3 methadone volume
m4 = 60 // 15                                    # MCQ4 checks in the first hour
beer, raksi = 650 * 0.05 * 0.789, 100 * 0.40 * 0.789   # Mr Gurung: 3 bottles of beer and 100 mL spirit a day
c_g = beer * 3 + raksi
c_sd = c_g / 10
c_fl = 30 * 62
c_obs = 24                                       # hourly observations for 24 hours
c_ciwa = 3 + 4 + 3 + 4 + 3 + 2 + 2 + 2 + 2 + 2
c_dz = (4 + 3 + 2 + 1) * 10
c_thi = 200 * 3 * 3
print(f"MCQ1 = {m1:.1f} g; MCQ2 = {m2:.1f} mL; MCQ3 = {m3:.0f} mL; MCQ4 = {m4}")
print(f"Mr Gurung: alcohol = {c_g:.1f} g = {c_sd:.1f} drinks a day; fluid at 30 mL/kg = {c_fl:,} mL; observations = {c_obs}; CIWA = {c_ciwa}; diazepam = {c_dz} mg; thiamine = {c_thi:,} mg")
```

```text
MCQ1 = 18.9 g; MCQ2 = 1.0 mL; MCQ3 = 16 mL; MCQ4 = 4
Mr Gurung: alcohol = 108.5 g = 10.8 drinks a day; fluid at 30 mL/kg = 1,860 mL; observations = 24; CIWA = 27; diazepam = 100 mg; thiamine = 1,800 mg
```

**MCQs (with reasons)**

1. 60 mL of 40% spirit contains about: (a) 9.5 g (b) 18.9 g (c) 24 g (d) 40 g of ethanol.
2. Naloxone 0.4 mg is ordered from a 0.4 mg/mL ampoule. The volume is: (a) 0.4 mL (b) 1 mL (c) 4 mL (d) 0.1 mL.
3. Methadone 80 mg is ordered from a 5 mg/mL syrup. The volume is: (a) 4 mL (b) 8 mL (c) 16 mL (d) 80 mL.
4. After rapid tranquillisation, observations every 15 minutes in the first hour number: (a) 2 (b) 4 (c) 6 (d) 12.
5. In suspected Wernicke encephalopathy in an alcohol-dependent patient, the correct order is: (a) glucose then thiamine (b) thiamine before or with glucose (c) neither (d) only benzodiazepine.

::: note Answers and rationales
**1. (b).** 60 × 0.40 × 0.789 = 18.9 g, about 1.9 standard drinks; 24 g would ignore the density factor.
**2. (b).** 0.4 ÷ 0.4 = 1 mL; 0.4 mL would be one-third of the dose, a common slip.
**3. (c).** 80 ÷ 5 = 16 mL; 4 mL would give only 20 mg.
**4. (b).** 60 ÷ 15 = 4 checks of breathing, BP, pulse, SpO2 and consciousness.
**5. (b).** Glucose alone uses up the remaining thiamine and can precipitate or worsen Wernicke encephalopathy, so thiamine is given first or together.
:::

**Short answer (3 marks): Mention the features of delirium tremens.** Delirium tremens appears 48-96 hours after the last drink in a dependent person. It shows confusion and disorientation, vivid hallucinations (insects, animals), severe tremor, sweating, fever, fast pulse and high BP, with agitation and risk of seizures and collapse. It is an emergency treated with benzodiazepines, thiamine, fluids and constant observation.

**Medium answer (5 marks): Describe the nursing management of an agitated, violent patient (Figure 5.5).** *Safety:* team, space, exit, remove objects. *De-escalation:* calm voice, listening, choices, clear limits. *Cause:* glucose, temperature, oxygen, pain, intoxication, delirium. *Medicine:* oral first, then rapid tranquillisation by injection as ordered, monitoring every 15 minutes. *Restraint:* last resort, trained team, brief, airway watched, recorded. *After:* debrief, treat the cause, review care plan and staff learning.

**Long answer (10 marks): Mr Dhan Bahadur Gurung, 45 years, a truck driver weighing 62 kg, is brought by his brother with 15 years of heavy drinking (3 bottles of 650 mL beer at 5% and 100 mL of 40% spirit a day). He stopped drinking 2 days ago. He is sweating and trembling, sees insects, is disoriented, has pulse 118, temperature 38.2 °C and unsteady gait, and his CIWA-Ar is 27. Calculate and write the nursing care plan.**

*Calculations.* Alcohol is about **108.5 g** a day, **10.8 standard drinks**. CIWA-Ar **27** is severe. A reducing diazepam course (10 mg tablets, 4, 3, 2 and 1 a day) is **100 mg**. Thiamine 200 mg three times a day for 3 days is **1,800 mg**. Fluid at 30 mL/kg is **1,860 mL** a day (adjusted to fever and output), and hourly observations for 24 hours are **24 checks**.

*Care.* This is delirium tremens with possible Wernicke encephalopathy (ataxia and confusion). Move him to a quiet, well-lit room with a constant observer, seizure precautions and oxygen and suction available. Give thiamine first or together with any glucose, then diazepam as ordered after checking breathing and sedation. Give IV fluids and check glucose, magnesium and potassium. Record pulse, BP, temperature, SpO2 and CIWA-Ar every hour. Orient him with a clock, calendar and his brother, and do not argue with the hallucinations. Look for infection, injury, bleeding and liver disease. Before discharge give brief motivational counselling, an assessment of relapse risk and referral for naltrexone or acamprosate if the doctor decides, a family meeting, a relapse plan, and links with the health post and self-help group.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "Insects on the bed." **O:** disoriented, CIWA 27, pulse 118, T 38.2 °C. | **Acute confusion** related to alcohol withdrawal, as evidenced by hallucinations and disorientation. | **Cognitive orientation:** oriented and CIWA below 8 within 72 hours. | Diazepam course as ordered (prevents seizures and delirium); thiamine before glucose (prevents Wernicke); quiet lit room, clock, brother present (orientation); CIWA hourly (guides dose). | Oriented; CIWA 7 at day 3. |
| **O:** tremor, ataxia, high BP and pulse, drinks 108 g a day. | **Risk for injury** related to seizures, confusion and unsteady gait. | **Safe environment:** no fall, no seizure injury. | Constant observer (early help); padded rails, low bed (limits harm); suction and oxygen at hand (airway); avoid restraint (prevents exhaustion and injury). | No injury during admission. |
| **O:** sweating, fever 38.2 °C, 62 kg. | **Deficient fluid volume** related to sweating and fever. | **Hydration:** intake 1,860 mL a day, normal pulse and urine output. | IV fluids with electrolytes (replaces losses); strict intake and output (monitor balance); cool sponging and antipyretic as ordered (fever); check Mg and K (prevents arrhythmia and seizure). | Pulse under 100; urine adequate. |
| **S:** Brother: "He will not stop." **O:** 15 years of heavy use. | **Ineffective health management** related to dependence and limited knowledge. | **Treatment behaviour:** accepts relapse-prevention plan and follow-up. | Motivational interviewing, FRAMES (builds motivation); family education and support (shared plan); naltrexone or acamprosate as ordered (reduces craving); link with health post and self-help group (continuity). | Agrees to plan; attends first follow-up. |

