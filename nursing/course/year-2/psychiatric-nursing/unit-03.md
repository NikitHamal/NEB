---
subject: Psychiatric Nursing
grade: BSc Nursing Year 2
unit: 3
title: Mood Disorders and Suicide: Depression, Mania, Lithium, ECT and Suicide Prevention in Nepal
hours: 16
area: BSN 13-14 · Psychiatric Nursing · Unit 3
---

A 35-year-old mother in Dhading comes to the health post with headache, burning of the body, "tension" and weakness. She has not slept for weeks, has stopped cooking, and when asked gently says that her family would be better off without her. Her husband works in Qatar and the family owes money. This is **depression**, and the body complaints are how many Nepalis express it. Meanwhile, **Nepal Police recorded 7,221 suicidal deaths in FY 2080/81**, about **20 a day**, and the **National Mental Health Survey 2020** found current suicidal thoughts in **6.5% of adults**. Mood disorders are the commonest cause of suicide, and they are **treatable**. The nurse who asks, listens and acts may save a life. All numbers are checked by program.

::: key What this unit gives you
- Real images: Van Gogh's drawing of an old man in despair, **ECT machines** (1960s Siemens and a museum unit), a **fluoxetine** pack and **St John's wort**, with SVG figures on the monoamine synapse, PHQ-9 bands, the lithium range and the suicide response pathway.
- Depression, mania and bipolar disorder (criteria, causes, scales), **PHQ-9**, antidepressants, **lithium levels and toxicity**, ECT with its indications and nursing care.
- Nepal suicide data (FY 2080/81), **crude rate per 100,000**, Section 185 of the Criminal Code, means restriction and the **1166** national helpline.
- Eight points each on care in depression, mania, ECT and suicide prevention; model answers and a 5-column NANDA-I plan for a woman with severe depression and suicidal thoughts.
:::

## 3.1 Depression

**Major depressive disorder** needs **five or more of nine symptoms for at least two weeks**, present nearly every day, with at least one being **low mood or loss of interest and pleasure (anhedonia)**, and with distress or loss of function. The nine symptoms are low mood, loss of interest, low energy, changed sleep, changed appetite or weight, guilt or worthlessness, poor concentration, slowing or agitation, and thoughts of death or suicide. In **severe depression** there may also be **psychotic features** (delusions of guilt or poverty, voices) or refusal of food and drink. Depression differs from normal grief by pervasive low mood, worthlessness and loss of self-esteem; grief comes in waves with good memories. Other forms include **persistent depressive disorder** (dysthymia, two years or more), **postpartum depression** (roughly 1 in 10 to 1 in 5 mothers screen positive in several Nepali hospital and community studies) and **depression in older adults**, which looks like memory loss (see Geriatric Nursing, Unit 3).

**Causes.** The **monoamine hypothesis** says that low **serotonin, noradrenaline and dopamine** activity in the synapse produces depression (Figure 3.1), and the **HPA axis** is overactive with high cortisol. Genes carry about 40% of the risk. Triggers in Nepal include **foreign employment and separation, debt, domestic violence, early marriage, bereavement, the 2015 earthquake, chronic illness and alcohol**. People who are poor, female, widowed or very old are at higher risk, and stigma delays care.

```svgfig label="3.1" caption="The monoamine synapse and the antidepressant effect. In depression less serotonin (5-HT) or noradrenaline stays in the gap. SSRIs such as fluoxetine block the reuptake pump so more transmitter remains and receptors are stimulated; benefit appears after 2-4 weeks, as receptors and brain circuits adapt, which is why patients must be told to continue."
f = Fig(760, 240)
f.box(20, 30, 220, 70, "PRESYNAPTIC NEURON\nstores serotonin in vesicles\nand releases it", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(520, 130, 220, 70, "POSTSYNAPTIC NEURON\nreceptors: mood, sleep,\nappetite, energy", fill=MINT, stroke=TEAL, size=11, bold=True)
f.circle(300, 90, 7, fill=AMBER, stroke=AMBER); f.circle(340, 105, 7, fill=AMBER, stroke=AMBER); f.circle(380, 120, 7, fill=AMBER, stroke=AMBER); f.circle(420, 135, 7, fill=AMBER, stroke=AMBER)
f.arrow([(240, 70), (290, 85)], label="release", lpos=(262, 66)); f.arrow([(430, 140), (520, 160)], label="binds", lpos=(480, 140))
f.box(250, 175, 190, 52, "REUPTAKE PUMP (SERT)\nrecycles serotonin", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.arrow([(340, 175), (240, 100)], color=AMBER, dash=True)
f.box(560, 20, 190, 70, "SSRI (fluoxetine)\nBLOCKS the pump\n= more serotonin\nin the gap", fill=ROSE, stroke=RED, color=RED, size=10.5, bold=True)
f.arrow([(560, 70), (420, 190)], color=RED, dash=True)
```

**Screening and rating.** The **PHQ-9** has nine items scored 0-3 (total 0-27): **0-4 minimal, 5-9 mild, 10-14 moderate, 15-19 moderately severe, 20-27 severe**. A score of **10 or more** has good sensitivity and specificity for major depression, and **any positive answer to item 9** (thoughts of being better off dead) needs a direct suicide assessment on the same day. Nepali-language PHQ-9 versions have been validated in community and hospital settings; the nurse reads the items aloud for patients who cannot read.

```python
items = [2, 2, 3, 2, 1, 2, 2, 1, 1]              # PHQ-9 items 1-9, each scored 0-3
total = sum(items)
bands = [(4, "minimal"), (9, "mild"), (14, "moderate"), (19, "moderately severe"), (27, "severe")]
band = next(name for top, name in bands if total <= top)
item9 = items[8]
change = (total - 8) / total * 100               # a follow-up PHQ-9 of 8 after treatment
print(f"PHQ-9 total = {total} ({band}); item 9 = {item9} -> {'ask about suicide today' if item9 > 0 else 'no suicide item'}")
print(f"Follow-up score 8: fall of {change:.0f}% (a fall of 50% or more is a treatment response)")
```

```text
PHQ-9 total = 16 (moderately severe); item 9 = 1 -> ask about suicide today
Follow-up score 8: fall of 50% (a fall of 50% or more is a treatment response)
```

The woman's items add up to **16**, which is **moderately severe**, and item 9 is **1**, so the nurse **asks directly about suicide today**. After treatment, a score of 8 is a fall of **50%**; a fall of **50% or more** counts as a **response**, and a score under 5 as **remission**.

```photogrid label="3.2" cols="2" ratio="1.0" caption="Depression in art and a scale. (a) Van Gogh's drawing Sorrowful Old Man (1890) shows a man bent over with his face in his hands, a classic posture of despair: slumped shoulders, hidden face, withdrawal. (b) PHQ-9 severity bands: the score of the woman in the case (16) lies in the moderately severe band, and a treatment response is a 50% fall."
@ photo id="nur8/oldman" cap="Van Gogh, Sorrowful Old Man"
fit 1.0
focus 0.5 0.5
mark 0.40 0.55 "1"
mark 0.62 0.35 "2"
key 1 (a) Face buried in the hands: withdrawal, low mood, shame
key 2 (a) Bent back and slumped shoulders: exhaustion and hopelessness
@ svg cap="PHQ-9 severity bands"
f = Fig(380, 300)
f.box(10, 20, 360, 34, "0-4 minimal: no treatment, watch", fill=MINT, stroke=TEAL, size=13, bold=True)
f.box(10, 64, 360, 34, "5-9 mild: support, repeat in 2 weeks", fill=BLUE, stroke=NAVY, size=13, bold=True)
f.box(10, 108, 360, 34, "10-14 moderate: counselling or drug", fill=SAND, stroke=AMBER, size=13, bold=True)
f.box(10, 152, 360, 34, "15-19 mod. severe: drug + therapy", fill=ROSE, stroke=RED, size=13, bold=True)
f.box(10, 196, 360, 34, "20-27 severe: urgent, refer", fill=ROSE, stroke=RED, color=RED, size=13, bold=True)
f.circle(355, 169, 12, fill="#ffffff", stroke=RED, sw=2.5, label="16", size=11, color=RED)
f.text(190, 262, "Item 9 above 0 = ask about suicide today", size=13, color=RED, bold=True)
```

### Depression: eight points of nursing care

1. **Assess risk first.** Ask every depressed person, "Have you had thoughts of ending your life?" Asking does not plant the idea; it opens the door. Record the plan, means and intent, and arrange safety if risk is present.
2. **Build a warm, patient relationship.** Sit with the patient, speak slowly and accept silence. Do not say "cheer up" or "think of your children", which add guilt. Praise small steps and show that you expect recovery.
3. **Meet basic needs.** Encourage small, frequent meals, fluids and hygiene, and weigh weekly. Depressed people neglect themselves, especially older people and new mothers. Check bowel habit and sleep.
4. **Restore sleep and routine.** Keep regular times for waking, meals, light, walking and sleep, avoid daytime napping and caffeine late in the day. Morning sunlight and a short daily walk lift mood. Avoid sleeping tablets that are not ordered.
5. **Activate gently.** Agree one small pleasant or useful task a day (cooking tea, a short walk, a phone call). Activity scheduling is a proven therapy. Build up slowly and note achievements.
6. **Challenge negative thoughts kindly.** Help the patient spot thoughts such as "I am useless" and examine the evidence, a basic part of cognitive behaviour therapy. Avoid arguing. Teach problem-solving for debts or family conflict with social worker support.
7. **Give medicines and teach.** Explain that fluoxetine takes 2-4 weeks to work, that nausea and restlessness fade, that the drug is not addictive and must continue for **at least 9-12 months** after recovery. Warn that stopping suddenly causes discomfort, and watch young patients for new suicidal thoughts in the first weeks.
8. **Involve family and link with the community.** Teach the family that depression is an illness, not laziness or weakness, and give them a safety plan. Link the patient to the health post, FCHV, women's groups and counselling services. Address alcohol, violence and loneliness.

## 3.2 Mania and bipolar disorder

**Mania** is a distinct period of **abnormally elevated, expansive or irritable mood and increased energy lasting at least one week** (or any length if hospitalisation is needed), with **three or more** of the following (remembered as **DIGFAST**): **D**istractibility, **I**ndiscretion (reckless spending, sex, driving), **G**randiosity, **F**light of ideas, **A**ctivity increase, **S**leep need decreased and **T**alkativeness (pressured speech). **Hypomania** is the same but milder, lasts at least four days and does not cause hospital admission or psychosis. **Bipolar I disorder** includes at least one manic episode; **bipolar II** includes hypomania and depression. The lifetime risk is about 1% and the genetic component is strong (about 80% heritability). Mania can cause **exhaustion, injury, debt and broken relationships** within days, and depressive episodes bring a high suicide risk.

| Feature | **Depression** | **Mania** |
|---|---|---|
| Mood | Low, empty, hopeless | Elated, expansive, irritable |
| Energy and sleep | Tired; insomnia or oversleeping | Boundless energy; needs little sleep without tiredness |
| Speech and thought | Slow, few words | Fast, pressured, flight of ideas |
| Self-view | Worthless, guilty | Grand, special powers |
| Behaviour | Withdrawn, slowed | Overactive, reckless, intrusive |
| Insight | Often present | Usually absent |
| Main danger | Suicide, self-neglect | Exhaustion, violence, financial ruin |
| First drugs | SSRI (fluoxetine) | Lithium, valproate, antipsychotic |

## 3.3 Treatment: antidepressants, mood stabilisers and ECT

| Drug | Usual adult dose | Points for the nurse |
|---|---|---|
| **Fluoxetine** (SSRI) | 20 mg each morning (mhGAP first line) | Nausea, insomnia, restlessness, sexual problems; safe in overdose; weeks to act; serotonin syndrome with other serotonergic drugs |
| **Amitriptyline** (TCA) | 25 mg at night, raised to 75-150 mg | Dry mouth, constipation, sedation, hypotension; **dangerous in overdose** (heart rhythm, seizure); avoid in older people and in suicidal patients; limit the supply |
| **Lithium carbonate** | 300 mg tablets, 600-1,200 mg a day; target blood level **0.6-1.0 mmol/L** | Narrow safety range; blood level 12 hours after the last dose; fluids and normal salt |
| **Sodium valproate** | 500-1,500 mg a day in divided doses | Liver tests, weight gain, tremor; **dangerous in pregnancy** (neural tube defects) |
| **Antipsychotic** (olanzapine, haloperidol, risperidone) | See Unit 2 | For severe mania and psychotic depression |

**Lithium** is the classic mood stabiliser, and it is toxic just above its treatment range (Figure 3.3). Measure the level **12 hours after the last dose**, **5-7 days** after any dose change (steady state takes about five half-lives of roughly 24 hours) and every 3-6 months, with **kidney function, thyroid function and calcium** every 6 months. **Toxicity** begins above about **1.5 mmol/L** with coarse tremor, vomiting, diarrhoea, slurred speech, unsteady gait and confusion; above 2.0 there are seizures and coma. Dehydration, sweating in summer, vomiting, a low-salt diet, and drugs such as **NSAIDs (ibuprofen, diclofenac), thiazide diuretics, ACE inhibitors and metronidazole** raise the level.

```svgfig label="3.3" caption="Lithium blood levels (mmol/L), measured 12 hours after the last dose. The safe maintenance range is narrow and toxic effects begin at 1.5. A level above 1.5 means: withhold the next dose, call the doctor, give fluids and recheck. Above 2.0 is an emergency with risk of seizures and permanent brain damage."
f = Fig(760, 190)
segs = [(30, 160, "0-0.4\nbelow range", SOFT, SLATE), (190, 140, "0.4-0.6\nlow", BLUE, NAVY), (330, 150, "0.6-1.0 MAINTENANCE\nthe target", MINT, TEAL), (480, 90, "1.0-1.2\nacute mania", SAND, AMBER), (570, 90, "1.2-1.5\nwatch", SAND, AMBER), (660, 80, ">1.5 TOXIC", ROSE, RED)]
for x, w, s, fl, st in segs:
    f.box(x, 40, w, 70, s, fill=fl, stroke=st, size=10.5, bold=True)
f.text(380, 140, "Toxic features: coarse tremor, vomiting, diarrhoea, slurred speech, ataxia, confusion", size=11, color=RED, bold=True)
f.text(380, 165, "Action: hold lithium, call doctor, IV fluids, recheck level, avoid NSAIDs and diuretics", size=11, color=SLATE)
```

```python
tab, daily = 300, 900                            # lithium carbonate 300 mg tablets, 900 mg a day
tabs_a_day = daily // tab
tabs14 = tabs_a_day * 14
level = 1.8
status = "TOXIC (above 1.5)" if level > 1.5 else ("in range" if 0.6 <= level <= 1.0 else "outside target")
sessions = 3 * 3                                 # ECT 3 times a week for 3 weeks
wt = 55                                          # kg, amitriptyline overdose risk
toxic_mg = 10 * wt
toxic_tabs = toxic_mg // 25
print(f"Lithium {daily} mg = {tabs_a_day} tablets a day; 14 days = {tabs14} tablets")
print(f"Level {level} mmol/L is {status}")
print(f"ECT course: {sessions} sessions; amitriptyline 10 mg/kg for {wt} kg = {toxic_mg} mg = {toxic_tabs} tablets of 25 mg")
```

```text
Lithium 900 mg = 3 tablets a day; 14 days = 42 tablets
Level 1.8 mmol/L is TOXIC (above 1.5)
ECT course: 9 sessions; amitriptyline 10 mg/kg for 55 kg = 550 mg = 22 tablets of 25 mg
```

A 900 mg daily dose of lithium is **3 tablets** of 300 mg and a 14-day supply is **42 tablets**. A blood level of **1.8 mmol/L is toxic**. An ECT course of three sessions a week for three weeks is **9 sessions**. For a 55 kg patient, amitriptyline at 10 mg/kg (a potentially life-threatening dose) is **550 mg, only 22 tablets of 25 mg**, which is why the nurse and prescriber **limit the supply** to a few days or one week for a suicidal patient and ask the family to hold the tablets.

### Mania: eight points of nursing care

1. **Reduce stimulation.** Place the patient in a quiet, low-light room away from crowds, televisions and visitors who excite. Speak slowly in a calm, low voice. A busy ward worsens mania.
2. **Set clear, kind limits.** Say "I will not allow you to hit others, but I will help you walk" and keep the same rule every shift. Do not argue or use sarcasm. Consistent limits make the patient feel safe.
3. **Ensure safety.** Watch for fights, falls, absconding and intrusive behaviour. Keep valuables, money and sharp items away and offer a quiet exit if tension rises. Escalate promptly if violence threatens (see Unit 5).
4. **Meet nutrition and fluid needs.** Overactive patients forget to eat and drink and lose weight rapidly. Offer finger foods that can be eaten while moving, high-energy drinks and 2-3 litres of water, and record intake. Lithium requires adequate salt and fluids.
5. **Promote sleep and rest.** Dim lights, avoid caffeine and stimulating talk, provide a warm drink and a regular bedtime. Give the ordered drug. Sleep loss deepens mania, so restoring 6-8 hours is a main goal.
6. **Support dignity and dress.** Help the patient to dress modestly, protect them from embarrassing behaviour and handle sexual remarks calmly. Redirect intrusive acts to harmless activity such as walking or drawing. Do not take offence at insults.
7. **Give medication and watch levels.** Give lithium, valproate or antipsychotics as ordered and check swallowing. Send lithium levels 12 hours after the last dose and record the time. Watch for toxicity, especially with sweating and diarrhoea.
8. **Teach and plan.** Teach the family early signs (little sleep, big plans, irritability) and the need for long-term mood stabiliser. Keep a mood and sleep diary, avoid alcohol and plan how to manage money during relapse. Offer family counselling.

## 3.4 Electroconvulsive therapy (ECT)

**ECT** passes a brief electric current through the brain to produce a controlled generalised seizure of at least 20-25 seconds. It is **given under general anaesthesia with a muscle relaxant (modified ECT)**, so there is no visible convulsion and little risk of fracture. It is among the **most effective treatments for severe depression**, especially with **suicide risk, psychosis, refusal of food and fluid or catatonia**, and it is also used for **severe mania, catatonia and drug-resistant schizophrenia**. A course is usually **6-12 sessions, two or three times a week**. ECT is used at the larger government and teaching hospitals in Nepal and must follow written consent and hospital protocol.

```photogrid label="3.4" cols="4" ratio="1.0" caption="Treatments for mood disorders. (a) A real 1960s Siemens Konvulsator III ECT machine; modern devices are brief-pulse and are given under anaesthesia. (b) An ECT apparatus on museum display. (c) A fluoxetine 20 mg capsule pack, the first-line SSRI in mhGAP. (d) St John's wort (Hypericum perforatum), a herbal remedy that interacts with many drugs and is not a substitute for treatment."
@ photo id="nur8/ect1" cap="ECT machine, 1960s"
fit 1.0
focus 0.5 0.5
mark 0.50 0.58 "1"
mark 0.35 0.18 "2"
key 1 (a) Control dial and meter: sets the stimulus
key 2 (a) Cable and handle leading to the electrodes
@ photo id="nur8/ect2" cap="ECT apparatus, museum"
fit 1.0
focus 0.5 0.62
mark 0.50 0.35 "3"
key 3 (b) Control panel of an early apparatus
@ photo id="nur8/fluox" cap="Fluoxetine 20 mg"
fit 1.0
focus 0.5 0.5
mark 0.80 0.70 "4"
key 4 (c) Label: drug name and 20 mg capsule strength
@ photo id="nur8/hyper" cap="St John's wort"
fit 1.0
focus 0.5 0.6
mark 0.48 0.62 "5"
key 5 (d) Yellow flowers: contain hyperforin, which speeds up drug breakdown
```

### ECT: eight points of nursing care

1. **Consent and explanation.** The doctor obtains written informed consent, and the nurse checks that the patient and family understand the procedure, the number of sessions, memory effects and the alternatives. Use a guardian's consent only as the hospital protocol and law permit. A fearful patient needs time and honest answers.
2. **Pre-procedure checks.** Confirm fasting for 6-8 hours, an empty bladder, dentures, jewellery and nail polish removed, loose clothing and recent vital signs, ECG and blood tests. Withhold or time medicines as ordered (for example, hold the usual dose of anticonvulsants or benzodiazepines only if ordered). Record weight and baseline orientation.
3. **Prepare the room and the patient.** Have oxygen, suction, a bag-valve-mask, an anaesthetic team, a bite block and emergency drugs ready. Place the patient supine with the electrodes on clean skin. Provide a reassuring presence until induction.
4. **Monitor during the treatment.** Observe pulse, BP, oxygen saturation and the seizure (about 25-30 seconds on the EEG or limb cuff). Support the airway, give oxygen and note any problems. The anaesthetist gives the drug; the nurse assists and documents.
5. **Recover safely.** Place the patient on one side, watch breathing and pulse until awake (usually 15-30 minutes), then record vital signs. Expect brief confusion, headache or nausea and treat as ordered. Reorient with a clock, a calendar and a calm voice.
6. **Watch for complications.** Confusion, memory loss for recent events (usually recovers within weeks to months), headache, muscle ache, nausea, rarely prolonged seizure, fractures, dental injury or heart rhythm change. Report prolonged confusion at once. Keep a record of orientation before each session.
7. **Support the patient and family.** Explain that ECT does not cause brain damage when properly given and that the patient is asleep. Offer breakfast after recovery and encourage rest. Teach that relapse prevention needs medicines or maintenance ECT.
8. **Document and review.** Record consent, pre-checks, the treatment details, seizure time, recovery and mental state. Compare mood scores, for example the PHQ-9, after every few sessions and report change. Missed or unclear documentation is a serious nursing failure.

## 3.5 Suicide and self-harm

Suicide results from the interaction of **pain, hopelessness and access to means**. In **Nepal Police data for FY 2080/81, 7,221 people died by suicide; about 85% by hanging; 56% were men, 33% women, 8% girls and 4% boys** (rounded). The crude rate is **24.8 per 100,000** if the 2021 census population of 29.16 million is used (an approximation). **Pesticide and other poisoning** is the second common method and is **highly lethal in rural areas**. Suicide is the leading cause of death in women of reproductive age in some Nepali studies. **Section 185 of the Muluki Criminal Code 2074** punishes **abetting suicide** (as reported, up to five years' imprisonment and a fine); a person who attempts suicide needs health care, not punishment.

```python
deaths, pop = 7221, 29.16e6
rate = deaths / pop * 100_000
per_day = deaths / 365
hang = round(deaths * 0.85)
men = round(deaths * 0.56)
print(f"Crude rate = {deaths:,} / {pop / 1e6:.2f} million x 100,000 = {rate:.1f} per 100,000")
print(f"Per day = {per_day:.1f}; hanging 85% = {hang:,}; men 56% = {men:,}")
```

```text
Crude rate = 7,221 / 29.16 million x 100,000 = 24.8 per 100,000
Per day = 19.8; hanging 85% = 6,138; men 56% = 4,044
```

The crude rate is **24.8 per 100,000**, about **20 deaths each day**; 85% by hanging is **6,138** deaths and 56% in men is **4,044** deaths. Nepal's **national suicide prevention helpline is 1166** (toll-free; check the current number at the health post), **Police 100** and **ambulance 102**.

**Risk factors** are previous attempt, depression, psychosis, alcohol and drug use, chronic pain or illness, recent loss, debt, abuse, access to pesticide or a rope, isolation and a family history; **protective factors** are family and community connection, reasons for living, treatment and help-seeking. **Warning signs** include talk of death, giving away items, sudden calm after distress, farewell messages and stockpiling tablets.

```svgfig label="3.5" caption="Suicide risk response based on the mhGAP self-harm module. Ask directly, judge the level of risk, and act: never leave a high-risk person alone, remove the means, treat the cause, and arrange follow-up contact within a week. A written safety plan lists warning signs, coping steps, people to call and the 1166 helpline."
f = Fig(760, 270)
f.box(10, 100, 150, 70, "ASK directly:\n\"Are you having thoughts\nof ending your life?\"", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(200, 100, 150, 70, "ASSESS plan, means,\nintent, past attempts,\nprotective factors", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(390, 10, 365, 66, "LOW: thoughts only, no plan.\nListen, safety plan, treat depression,\nfollow-up in 1 week, involve family", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(390, 102, 365, 66, "MODERATE: plan or past attempt, no intent.\nSafety plan, remove means, family watch,\nurgent mental health review", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(390, 194, 365, 66, "HIGH: intent, plan and means, or attempt.\nNEVER leave alone; remove means;\nurgent referral, treat medical emergency", fill=ROSE, stroke=RED, color=RED, size=10.5, bold=True)
f.arrow([(160, 135), (200, 135)]); f.arrow([(350, 125), (390, 45)]); f.arrow([(350, 135), (390, 135)]); f.arrow([(350, 145), (390, 227)])
```

### Suicide prevention: eight points of nursing care

1. **Ask directly and calmly.** Use plain words: "Have you thought of ending your life? Do you have a plan?" Direct questions reduce risk and relieve the patient. Never promise to keep a plan secret.
2. **Listen without judgement.** Let the person speak, accept silence and say, "I am glad you told me." Do not argue, lecture or call it selfish. Feeling heard is the first protection.
3. **Assess the level of risk.** Record the plan, method, access to means, timing, intent, previous attempts and protective factors. Use a structured tool such as the mhGAP module or the Columbia scale. Reassess at every shift and after every change.
4. **Remove the means.** Lock up pesticide and medicines, hold ropes, belts and razors, and give limited tablet supplies (see the amitriptyline calculation). Means restriction saves more lives than any other measure because the crisis passes. Ask the family to store pesticide away from the home.
5. **Never leave a high-risk person alone.** Provide one-to-one observation within arm's length, including toilet and bath, and keep the room free of cords, glass and windows that open. Count and secure tablets after each dose. Record observations at set times.
6. **Make a safety plan.** Write with the patient the warning signs, three coping steps, people and places for distraction, a trusted person to call, the helpline and a step to make the place safe. Give a copy to the family. A safety plan roughly halves repeat attempts in some studies.
7. **Treat the cause.** Treat depression, psychosis, alcohol use and pain, and refer for psychological therapy. Give medicines as ordered and monitor, with a small supply in the first weeks. Contact within the first week after discharge, a period of high risk, with a call or visit.
8. **Support family and community.** Teach the family warning signs, not to blame, and to keep the plan. Offer them counselling, since the family is also in crisis. Support school, community and media safe-messaging (no method details, no glorification) and provide help for those bereaved by suicide.

## Formula and fact sheet

- PHQ-9: 0-4 minimal, 5-9 mild, 10-14 moderate, 15-19 moderately severe, 20-27 severe; response = 50% fall; item 9 above 0 = ask about suicide.
- Depression: 5 of 9 symptoms for 2 weeks; mania: 1 week and 3 or more DIGFAST features; hypomania: 4 days.
- Lithium: target 0.6-1.0 mmol/L, 12 h post-dose, toxic above 1.5; avoid NSAIDs, thiazides and ACE inhibitors; recheck 5-7 days after a change.
- Crude suicide rate = deaths ÷ population × 100,000 (7,221 ÷ 29.16 million = 24.8). Amitriptyline 10 mg/kg is a dangerous dose.

## Chapter summary

- Depression and bipolar disorder are common, treatable and the leading psychiatric causes of suicide; ask directly and use the PHQ-9.
- SSRIs (fluoxetine) take weeks to work and must continue for 9-12 months; lithium needs level checks and fluids; tricyclics are dangerous in overdose.
- ECT is a safe, effective treatment for severe illness when consent, anaesthesia and nursing care are correct.
- In Nepal 7,221 people died by suicide in FY 2080/81; means restriction, safety plans, follow-up and the 1166 helpline save lives.

## Practice

```python
m1 = 2 + 2 + 3 + 2 + 1 + 2 + 0 + 0 + 0           # MCQ1 PHQ-9 total of a patient
m2 = 900 // 300 * 14                             # MCQ2 lithium tablets for 14 days
m3 = 7221 / 29.16e6 * 100_000                    # MCQ3 crude suicide rate
w0, hang = 55, round(7221 * 0.85)
c_caps = 30                                      # Mrs Kamala Tamang: fluoxetine 20 mg daily for a month
c_270 = 30 * 9                                   # 9 months of treatment after recovery
c_tox = 10 * 55
c_tabs = c_tox // 25
c_resp = (16 - 7) / 16 * 100
print(f"MCQ1 = {m1}; MCQ2 = {m2}; MCQ3 = {m3:.1f}; hanging = {hang:,}")
print(f"Mrs Tamang: fluoxetine {c_caps} capsules a month, {c_270} for 9 months; amitriptyline danger dose {c_tox} mg = {c_tabs} tablets; PHQ-9 16 to 7 = fall of {c_resp:.0f}%")
```

```text
MCQ1 = 12; MCQ2 = 42; MCQ3 = 24.8; hanging = 6,138
Mrs Tamang: fluoxetine 30 capsules a month, 270 for 9 months; amitriptyline danger dose 550 mg = 22 tablets; PHQ-9 16 to 7 = fall of 56%
```

**MCQs (with reasons)**

1. A patient's PHQ-9 items are 2, 2, 3, 2, 1, 2, 0, 0, 0. The total and band are: (a) 12, moderate (b) 12, mild (c) 8, mild (d) 14, severe.
2. Lithium carbonate 900 mg/day is given as 300 mg tablets for 14 days. The tablets needed are: (a) 14 (b) 28 (c) 42 (d) 84.
3. 7,221 suicides in a population of 29.16 million is a crude rate per 100,000 of: (a) 2.5 (b) 24.8 (c) 72 (d) 248.
4. A lithium level of 1.8 mmol/L, 12 hours after the dose, means: (a) normal (b) sub-therapeutic (c) toxic, hold the dose and call the doctor (d) give an extra dose.
5. A woman screened with PHQ-9 gives item 9 a score of 1. The next step is: (a) ignore it (b) ask directly about suicide today and assess risk (c) tell her to be strong (d) repeat the test next year.

::: note Answers and rationales
**1. (a).** The sum is 12, which lies in the 10-14 moderate band; 5-9 is mild.
**2. (c).** 900 ÷ 300 = 3 tablets a day, 3 × 14 = 42; 28 would be only 2 tablets a day.
**3. (b).** 7,221 ÷ 29,160,000 × 100,000 = 24.8; 2.5 would be a decimal slip.
**4. (c).** Above 1.5 mmol/L is toxic, so hold the next dose, call the doctor, give fluids and recheck; extra doses are dangerous.
**5. (b).** Any positive item 9 needs a direct suicide enquiry the same day; asking does not raise risk.
:::

**Short answer (3 marks): Mention four features of mania.** Mania shows elevated or irritable mood for at least one week, increased energy and activity, decreased need for sleep, pressured speech and flight of ideas, grandiosity, distractibility and reckless behaviour such as overspending. Insight is usually lost. It needs a mood stabiliser, a quiet environment, nutrition and safety measures.

**Medium answer (5 marks): Describe the nursing care of a patient on lithium (Figure 3.3).** Before starting, check kidney, thyroid, pregnancy status and drugs. Give with food and keep the dose time constant. Take the blood level 12 hours after the last dose and 5-7 days after any change; keep it at 0.6-1.0 mmol/L. Teach fluids of 2-3 litres a day, normal salt and no NSAIDs or diuretics. Watch for fine tremor, thirst and passing much urine (early) and for coarse tremor, vomiting, diarrhoea, ataxia and confusion (toxicity), then hold the dose and report. Repeat kidney, thyroid and calcium tests every six months and counsel women about pregnancy.

**Long answer (10 marks): Mrs Kamala Tamang, 35 years, 55 kg, from Dhading, whose husband works in Qatar and who has a loan, is brought by her sister with 6 weeks of low mood, no sleep, poor appetite and headaches. She says her children would be better without her, and that she thought of drinking the pesticide kept in the house. Her PHQ-9 total is 16 with item 9 scored 1. Calculate and write the nursing care plan.**

*Calculations.* PHQ-9 of **16** is moderately severe and item 9 is positive. Fluoxetine 20 mg daily for a month is **30 capsules**, and for **9 months** after recovery **270 capsules**. Amitriptyline at 10 mg/kg is **550 mg** for her weight, only **22 tablets** of 25 mg, so a full pack is a danger. If after treatment the PHQ-9 falls from 16 to 7 the fall is **56%**, which is a **response**.

*Care.* Ask directly about plan, means and intent: she has a method (pesticide) but no immediate intent, so risk is **moderate to high** and a one-to-one watch is used on admission or her sister stays with her. **Remove the pesticide** from the house, give small supplies of any tablets, and write a safety plan with her sister, the 1166 helpline and the health post number. Start fluoxetine 20 mg each morning as ordered, explaining that it takes 2-4 weeks and must continue for 9-12 months. Restore sleep and food, encourage a daily walk and one small task, and review thoughts like "my children are better without me". Link her with the social worker about debt and with the women's group; follow up by phone in 3 days and visit in 1 week.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "My children are better without me." **O:** PHQ-9 16, item 9 = 1, plan: pesticide. | **Risk for suicide** related to depression, hopelessness and access to means. | **Suicide self-restraint:** no self-harm; states two reasons to live and uses the safety plan within 1 week. | Ask directly each shift (opens talk); one-to-one watch while risk is high (prevents act); remove pesticide, limit tablets (blocks means); written safety plan with the 1166 helpline (coping step). | No self-harm; names reasons; sister holds the plan. |
| **S:** "I cannot sleep." **O:** sleeps 3 h, poor appetite, 55 kg. | **Insomnia** and **imbalanced nutrition: less than body requirements** related to depression. | **Sleep and nutrition:** sleeps 6 h and eats 75% of meals in 2 weeks. | Fixed sleep schedule and morning light (resets body clock); warm drink, no caffeine (aids sleep); small frequent meals and weekly weight (restores intake); fluoxetine in the morning as ordered (reduces insomnia). | Sleeps 6 h; eats three-quarters of meals. |
| **S:** "I am a burden to everyone." **O:** tearful, avoids eye contact. | **Hopelessness** related to debt and separation, as evidenced by statements of being a burden. | **Hope:** names one future plan and takes part in daily activity within 3 weeks. | Active listening and small achievable tasks (build mastery); challenge negative thoughts (cognitive restructuring); link with the social worker for the loan and with the women's group (reduce stressors, add support). | Plans to restart her shop; joins the group. |
| **O:** sister fears she is "mad". | **Ineffective family coping** related to knowledge deficit and stigma. | **Family knowledge:** sister states warning signs and her role. | Teach that depression is treatable and not a weakness (corrects belief); teach warning signs and what to do (early action); give counselling and the follow-up date (support). | Sister repeats the plan; attends follow-up. |

