---
subject: Geriatric Nursing
grade: BSc Nursing Year 2
unit: 3
title: Delirium, Dementia and Depression: The Three Ds of Old Age
hours: 10
area: BSN 11 · Geriatric Nursing · Unit 3
---

"*Buwa* has become forgetful, he wanders at night and does not know me." In Nepal this is often called *budesakal* (just old age) and nobody looks for a cause. Yet confusion in an older person is **never normal ageing**. It may be **delirium** (acute, dangerous and often curable), **dementia** (chronic and progressive) or **depression** (treatable), and the three often overlap. WHO estimates that **5-8% of people over 60 live with dementia**; applied to Nepal's 2.97 million older people that is about **148,500 to 237,600** persons (an estimate, not a count), and most are cared for at home by a daughter-in-law or wife with no training. The nurse's skill is to **recognise, screen, treat the cause, keep the person safe and support the family**. All arithmetic in this unit is checked by program.

::: key What this unit gives you
- Real photographs of Alzheimer histology (hippocampus, neurofibrillary tangle, amyloid plaque), an MRI comparison of Alzheimer disease, dementia with Lewy bodies and a normal brain, and Lewy pathology beside a plaque, plus three SVG figures.
- Delirium versus dementia versus depression, CAM and 4AT, the Mini-Cog, MMSE bands, GDS-15, test accuracy (sensitivity, specificity, predictive values) and low-dose drug maths.
- Eight points each on delirium care, dementia care and depression care.
- Model answers and a NANDA-I care plan for a man with moderate Alzheimer disease who wanders at night.
:::

## 3.1 The three Ds compared

| Feature | **Delirium** | **Dementia** | **Depression** |
|---|---|---|---|
| Onset | Hours to days (acute) | Months to years (insidious) | Weeks to months |
| Course | Fluctuates, worse at night | Slow, steady decline | Often worse in the morning |
| Attention | Always poor | Normal until late | May be poor from low interest |
| Consciousness | Altered (drowsy or agitated) | Clear | Clear |
| Orientation and memory | Disoriented, variable | Recent memory lost first | "I don't know" answers, effort is poor |
| Cause | Physical illness, drugs, pain | Brain disease (Alzheimer, vascular) | Loss, illness, isolation, brain chemistry |
| Reversible? | Usually yes, if the cause is found | Not reversible; symptoms can be eased | Yes, with treatment |

## 3.2 Delirium: the emergency of the confused old person

**Delirium** is an acute, fluctuating disturbance of attention and awareness caused by a medical condition. It occurs in about **one in five older hospital patients** and in up to half after hip surgery, and it raises the risk of falls, long stay, dementia and death. The **hypoactive** form (quiet, sleepy, not eating) is the commonest and the most missed. Causes are remembered as **DELIRIUMS**: Drugs (sedatives, anticholinergics, opioids), Electrolytes (sodium, calcium), Lack of drugs (alcohol or benzodiazepine withdrawal), Infection (urine, chest), Reduced sensory input (no glasses or hearing aid), Intracranial (stroke, subdural), Urinary retention and faecal impaction, Myocardial (MI, heart failure, hypoxia) and Sleep deprivation. The **Confusion Assessment Method (CAM)** is positive when there is **(1) acute onset with a fluctuating course and (2) inattention, plus either (3) disorganised thinking or (4) an altered level of consciousness**. The **4AT** (0-12) is faster: alertness, a 4-item orientation test (AMT4), months of the year backwards and acute change; **4 or more** suggests possible delirium.

```python
cam = {"acute onset and fluctuating course": True, "inattention": True, "disorganised thinking": False, "altered consciousness": True}
cam_pos = cam["acute onset and fluctuating course"] and cam["inattention"] and (cam["disorganised thinking"] or cam["altered consciousness"])
alert, amt4, months, acute = 0, 2, 1, 4          # 4AT items: alertness, AMT4, months backwards, acute change
at4 = alert + amt4 + months + acute
mg, strength = 0.5, 5.0                          # haloperidol 0.5 mg ordered, ampoule 5 mg/mL
vol = mg / strength
print(f"CAM positive: {cam_pos}")
print(f"4AT = {alert} + {amt4} + {months} + {acute} = {at4} ({'possible delirium' if at4 >= 4 else 'unlikely'}; 4 or more)")
print(f"Haloperidol {mg} mg from a {strength:.0f} mg/mL ampoule = {vol:.1f} mL (lowest dose, only for severe distress, as ordered)")
```

```text
CAM positive: True
4AT = 0 + 2 + 1 + 4 = 7 (possible delirium; 4 or more)
Haloperidol 0.5 mg from a 5 mg/mL ampoule = 0.1 mL (lowest dose, only for severe distress, as ordered)
```

A patient with acute onset, inattention and drowsiness is **CAM positive**, and a 4AT of 0 + 2 + 1 + 4 = **7** also suggests delirium. If the doctor orders haloperidol 0.5 mg for severe distress that endangers the patient, the volume from a 5 mg/mL ampoule is **0.1 mL**. Drugs are the **last** choice: the first steps are to find and treat the cause and to use non-drug measures. Benzodiazepines make delirium worse, except in alcohol withdrawal.

```svgfig label="3.1" caption="The CAM decision rule for delirium. Features 1 and 2 are both needed, plus feature 3 or feature 4. A positive screen means a medical emergency to look for infection, drugs, pain, retention, low oxygen, sodium and glucose, not a psychiatric problem."
f = Fig(760, 230)
f.box(10, 80, 150, 70, "1. ACUTE ONSET\nand FLUCTUATING\ncourse?", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(200, 80, 150, 70, "2. INATTENTION?\n(cannot count\nbackwards)", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(400, 20, 170, 60, "3. DISORGANISED\nthinking, rambling?", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(400, 150, 170, 60, "4. ALTERED level of\nconsciousness?", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(610, 80, 140, 70, "DELIRIUM\nlook for the cause\nnow", fill=ROSE, stroke=RED, color=RED, size=12, bold=True)
f.arrow([(160, 115), (200, 115)], label="YES", lpos=(180, 104)); f.arrow([(350, 105), (400, 55)], label="YES", lpos=(365, 70)); f.arrow([(350, 125), (400, 175)], label="YES", lpos=(365, 160))
f.arrow([(570, 50), (610, 100)], color=RED, sw=2); f.arrow([(570, 180), (610, 130)], color=RED, sw=2)
f.text(180, 175, "If feature 1 or 2 is NO:\ndelirium is unlikely", size=10.5, color=SLATE)
```

### Delirium: eight points of prevention and nursing care

1. **Find the cause first.** Check temperature, SpO2, pulse, BP, blood glucose, hydration and urine output, and ask for urine and chest tests, sodium, calcium and kidney tests. Check for retention (a full bladder) and constipation by palpation and rectal examination. Treat the cause, because delirium cannot be sedated away.
2. **Review every drug.** Stop or reduce sedatives, anticholinergic drugs (diphenhydramine, amitriptyline, hyoscine), opioids and steroids when possible, as the **Beers criteria** advise. A new drug in the last week is the first suspect. Give the list to the doctor.
3. **Restore the senses.** Fit glasses and hearing aids, remove wax and keep the room lit by day. A person who cannot see or hear misreads the ward and becomes frightened.
4. **Orient and reassure.** Place a clock and a calendar in view, use the person's name, explain every procedure, repeat the day and place gently and bring familiar things from home. Do not argue with false beliefs; calm them.
5. **Encourage family presence.** A familiar face is the best medicine, so allow a relative to stay. Teach the family what delirium is, that it is not madness and that most patients recover.
6. **Protect sleep.** Keep the room dark and quiet at night, cluster care to avoid waking the patient, avoid the sleeping tablet, offer warm milk and reduce noise. Daytime light and walking set the body clock.
7. **Keep the body working.** Offer fluids, food and help with eating, walk three times a day, avoid urinary catheters and IV lines that are not needed, and start bowel care. Catheters and restraints are triggers.
8. **Keep the patient safe without restraint.** Use a low bed, floor mat, one-to-one observation or a family sitter; use physical restraint only as the last resort. Antipsychotic drugs are used only for severe distress or danger, at the lowest dose for the shortest time, and stopped as soon as possible.

## 3.3 Dementia

**Dementia** is a progressive loss of memory and at least one other thinking skill (language, planning, judgement, recognition) that is severe enough to interfere with daily life. **Alzheimer disease** causes 60-70% of cases; **vascular dementia** follows strokes and small vessel disease and steps down in stages; **dementia with Lewy bodies** brings visual hallucinations, fluctuating alertness and Parkinson-like stiffness; **frontotemporal dementia** changes personality and behaviour early. In Alzheimer disease **amyloid-beta plaques** build up between neurons and **tau neurofibrillary tangles** build up inside them, synapses and cholinergic neurons are lost and the hippocampus and cortex shrink (Figure 3.2, Plates 3.3 and 3.4). **Risk factors** include age, hypertension, diabetes, smoking, midlife obesity, hearing loss, depression, low education and head injury; about **40% of cases may be delayable** by controlling these. Alzheimer disease and Parkinson disease are among the illnesses named for government treatment support in Nepal (check the current list at the district hospital).

```svgfig label="3.2" caption="Alzheimer disease in one picture. Amyloid-beta clumps outside neurons and tau tangles inside them damage synapses; acetylcholine falls and the hippocampus and cortex shrink, which produce memory loss and then loss of daily skills. Cholinesterase inhibitors (donepezil) raise acetylcholine; memantine blocks excess glutamate."
f = Fig(760, 240)
f.box(10, 20, 170, 56, "AMYLOID-BETA\nplaques outside\nneurons", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(10, 100, 170, 56, "TAU TANGLES\ninside neurons", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(10, 176, 170, 56, "AGE, BP, DIABETES,\nHEARING LOSS,\nSMOKING", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(230, 60, 160, 70, "SYNAPSE AND\nNEURON LOSS\nacetylcholine falls", fill=ROSE, stroke=RED, color=RED, size=11, bold=True)
f.box(440, 60, 150, 70, "ATROPHY\nhippocampus,\ncortex", fill=ROSE, stroke=RED, color=RED, size=11, bold=True)
f.box(630, 20, 120, 56, "MEMORY LOSS\nlanguage, planning", fill=MINT, stroke=TEAL, size=11, bold=True)
f.box(630, 100, 120, 56, "ADL LOSS\nwandering, BPSD", fill=MINT, stroke=TEAL, size=11, bold=True)
f.arrow([(180, 48), (230, 85)]); f.arrow([(180, 128), (230, 110)]); f.arrow([(180, 204), (230, 120)], dash=True)
f.arrow([(390, 95), (440, 95)]); f.arrow([(590, 80), (630, 50)]); f.arrow([(590, 110), (630, 128)])
f.box(230, 170, 360, 56, "TREATMENT: donepezil (raise acetylcholine), memantine,\ncontrol BP and diabetes, exercise, hearing aids, company", fill=MINT, stroke=TEAL, size=11, bold=True)
```

```photogrid label="3.3" cols="2" ratio="1.0" caption="Alzheimer pathology under the microscope. (a) A real histology composite: the hippocampus at low power (top left), a neuron containing a neurofibrillary tangle (bottom left) and an amyloid plaque (right). (b) A real stained amyloid plaque: a pink, amorphous deposit between neurons marked by arrows."
@ photo id="nur7/histo" cap="Alzheimer histology"
fit 1.0
focus 0.0 0.5
mark 0.21 0.80 "1"
mark 0.17 0.24 "2"
key 1 (a) Hippocampus at low power: the memory centre, the first area to shrink
key 2 (a) Neuron with a neurofibrillary tangle: tau protein collects inside the cell
@ photo id="nur7/amyloid" cap="Amyloid plaque"
fit 1.0
focus 0.5 0.5
mark 0.45 0.52 "3"
mark 0.18 0.80 "4"
key 3 (b) Amyloid plaque: a pink, amorphous deposit of amyloid-beta between neurons
key 4 (b) Neighbouring cell nuclei: neurons around a plaque lose their synapses
```

```photogrid label="3.4" cols="2" ratio="1.0" caption="Imaging and pathology of dementia. (a) Real coronal MRI slices (left to right) of Alzheimer disease (AD), dementia with Lewy bodies (DLB) and a normal control (NC); the red boxes mark the medial temporal lobes. (b) A real immunostain of Lewy pathology (dark) beside an amyloid plaque (brown): the two diseases often overlap."
@ photo id="nur7/mri" cap="MRI: AD, DLB and normal"
fit 1.0
focus 0.5 0.5
mark 0.18 0.42 "5"
mark 0.83 0.42 "6"
key 5 (a) Alzheimer disease: the hippocampus is shrunken and the temporal horn wider
key 6 (a) Normal control: the hippocampus fills the space; compare the red boxes
@ photo id="nur7/lewy" cap="Lewy pathology beside a plaque"
fit 1.0
focus 0.5 0.5
mark 0.50 0.55 "7"
mark 0.59 0.35 "8"
key 7 (b) Amyloid plaque: the brown granular stain, the hallmark of Alzheimer disease
key 8 (b) Lewy neurite (arrow): alpha-synuclein pathology, seen in Lewy body dementia
```

**Screening and staging.** The **Mini-Cog** takes 3 minutes: register three words, draw a clock set to 11:10 and recall the words; score 1 point per word recalled (0-3) plus 2 for a normal clock (0 or 2), **a total below 3 is a positive screen** (0-5). The **MMSE** (30 points): **24-30 normal, 19-23 mild, 10-18 moderate, below 10 severe**; scores are affected by education, so use the **MoCA** (26 or more is normal) for those with higher education and a culture-fair tool for those who cannot read. Dementia goes through three stages (Figure 3.5): **early** (forgets recent events, misplaces things, needs reminders), **middle** (needs help with dressing and bathing, gets lost, sleeps badly and shows behaviour change) and **late** (cannot walk, speak or swallow safely, is bedbound and incontinent). Average survival is 8-10 years after diagnosis.

```python
tp, fn, fp, tn = 45, 5, 20, 130                  # Mini-Cog result against the specialist diagnosis, 200 persons
n = tp + fn + fp + tn
sens, spec = tp / (tp + fn) * 100, tn / (tn + fp) * 100
ppv, npv = tp / (tp + fp) * 100, tn / (tn + fn) * 100
prev = (tp + fn) / n * 100
recall1, clock1, recall2, clock2 = 2, 2, 1, 0
print(f"Prevalence = {tp + fn} / {n} = {prev:.1f}%")
print(f"Sensitivity = {sens:.1f}%; specificity = {spec:.1f}%")
print(f"PPV = {ppv:.1f}%; NPV = {npv:.1f}%")
print(f"Mini-Cog A = {recall1} + {clock1} = {recall1 + clock1} (negative); B = {recall2} + {clock2} = {recall2 + clock2} (positive, below 3)")
```

```text
Prevalence = 50 / 200 = 25.0%
Sensitivity = 90.0%; specificity = 86.7%
PPV = 69.2%; NPV = 96.3%
Mini-Cog A = 2 + 2 = 4 (negative); B = 1 + 0 = 1 (positive, below 3)
```

In a study of 200 persons, the Mini-Cog found 45 of 50 with dementia and wrongly flagged 20 of the 150 without. The **sensitivity is 90.0%, specificity 86.7%, positive predictive value 69.2% and negative predictive value 96.3%** at a prevalence of 25.0%. A negative result is therefore reassuring, but one positive in three is a false alarm, so a positive screen needs the full assessment and exclusion of delirium, depression, thyroid disease, vitamin B12 deficiency and drug effects. A patient who recalls two words and draws a normal clock scores **4** (negative); recalling one word with an abnormal clock scores **1** (positive).

```svgfig label="3.5" caption="The course of dementia over about 8-10 years from diagnosis. As the stages move on, independence and safety fall and the family's burden grows, so planning for care, money, legal matters and end-of-life wishes should begin in the early stage while the person can still take part."
f = Fig(760, 220)
cols = [("EARLY (years 1-3)", "forgets recent events,\nmisplaces things,\nstill manages ADL\nwith reminders", MINT, TEAL), ("MIDDLE (years 3-7)", "needs help to dress and bathe,\ngets lost, sleeps badly,\nBPSD: agitation, suspicion", SAND, AMBER), ("LATE (years 7-10)", "cannot walk, speak or\nswallow safely, bedbound,\nincontinent, pressure injury", ROSE, RED)]
for i, (h, t, fl, st) in enumerate(cols):
    x = 10 + i * 250
    f.box(x, 14, 240, 34, h, fill=st, stroke=st, color="#ffffff", size=11, bold=True)
    f.box(x, 54, 240, 88, t, fill=fl, stroke=st, size=11, bold=True)
f.arrow([(250, 98), (260, 98)]); f.arrow([(500, 98), (510, 98)])
f.box(10, 162, 740, 44, "Nursing focus: early = diagnosis, safety, planning; middle = routine, ADL help, wandering, caregiver support; late = comfort, feeding, skin care", fill=BLUE, stroke=NAVY, size=11, bold=True)
```

### Dementia: eight points of nursing care

1. **Keep a calm routine.** Wake, eat, wash, walk and sleep at the same times each day. Routine reduces fear and agitation because the person cannot plan the day.
2. **Communicate simply.** Approach from the front, call the person by name, use short sentences, one instruction at a time, a warm tone and gestures. Do not correct or quiz; join the person's reality gently ("Tell me about your village").
3. **Manage wandering safely.** Wandering is often a search for a toilet, food or home. Provide a safe walking path, an ID bracelet with a phone number, a door chime, a recent photo, and regular toilet and drink offers. Never lock the person alone in a room.
4. **Respond to behaviour with the ABC method.** Find the Antecedent (pain, hunger, toilet, noise), describe the Behaviour and change the Consequence. Check pain, constipation, infection, thirst and boredom before any drug. **Antipsychotics** raise stroke and death rates and are used only for severe distress or danger, briefly (Beers 2023).
5. **Protect nutrition and fluids.** Give finger foods, familiar dishes, small portions, a cup in view and help at the table. Weigh monthly; a weight loss of 5% is a warning. Check swallowing in late disease and avoid force-feeding.
6. **Preserve independence.** Let the person do what he or she can: washing the face, eating, folding cloth, shelling peas. Lay out clothes in order and use large labels. Small successes protect dignity.
7. **Make the home safe.** Remove sharp tools and stoves with open fire, lock medicines and chemicals, fit night lights and grab bars, use non-slip floors and keep a clear path. Supervise fire and water.
8. **Support the caregiver.** Caregivers have high rates of depression and physical illness. Teach them the disease, share care among family, use respite and local senior citizens' groups, and watch for burnout and abuse. Give the caregiver a number to call.

## 3.4 Depression and suicide risk in older people

Depression in old age is under-diagnosed because it shows as **tiredness, pain, poor appetite, poor sleep, anxiety or "memory problems"** more than as sadness. Triggers are bereavement, chronic disease, pain, loneliness (children abroad), loss of work and money worries. Screen with the **Geriatric Depression Scale GDS-15** (a score of **5 or more** suggests depression, 10 or more severe) or the PHQ-9, and always ask about **suicidal thoughts**, which are a major risk in older men and in people who feel a burden. First-line drugs are SSRIs such as sertraline or escitalopram, started at half the adult dose; watch for **hyponatraemia** and falls, and avoid amitriptyline (Beers). Psychological help, activity and company work as well in mild cases.

### Depression and suicide risk: eight points of nursing care

1. **Ask directly.** Ask "Do you sometimes feel life is not worth living?" Asking does not plant the idea; it opens the door. Record and report every positive answer.
2. **Look for hidden depression.** Poor sleep, appetite loss, weight loss, unexplained pain and refusal of food may be depression. Use the GDS-15 at each assessment.
3. **Rule out physical causes.** Check thyroid, anaemia, B12, sodium, pain and drugs (steroids, beta-blockers). Treating them often lifts the mood.
4. **Make a safety plan.** Remove pesticides, ropes, sharp tools and extra medicines at home; do not leave a high-risk patient alone. Many suicides in rural Nepal use organophosphate poison, so safe storage is protective.
5. **Give medicines carefully.** Give SSRIs in the morning, monitor sodium and falls, explain that effect takes 2-4 weeks and that the course lasts months, and do not stop suddenly. Keep the supply short for a high-risk patient.
6. **Encourage activity and company.** Daily walk, prayer or meditation, mothers' or senior citizens' groups, visits and phone calls. Behavioural activation is the simplest effective therapy.
7. **Listen and validate.** Allow tears, reflect feelings and do not say "cheer up". Reminiscence and grief counselling help after a bereavement.
8. **Refer and follow up.** Refer to the psychiatric unit or the trained mental-health worker (mhGAP) for severe depression, psychosis or suicidal intent, and follow up by phone or home visit within a week of discharge.

## Formula and fact sheet

- CAM positive = (1) acute onset and fluctuating course AND (2) inattention AND [(3) disorganised thinking OR (4) altered consciousness]; 4AT 4 or more = possible delirium.
- Mini-Cog below 3 positive; MMSE 24-30 normal, 19-23 mild, 10-18 moderate, below 10 severe; GDS-15 5 or more = depression.
- Sensitivity = TP ÷ (TP + FN); specificity = TN ÷ (TN + FP); PPV = TP ÷ (TP + FP); NPV = TN ÷ (TN + FN); volume = dose ÷ strength.
- Donepezil 5 mg at night, raised to 10 mg after 4-6 weeks; antipsychotics only for severe distress, lowest dose and shortest time.

## Chapter summary

- Confusion in an older person is never normal ageing: look for delirium first, then dementia and depression.
- Delirium is an emergency: use CAM or 4AT, find the cause, review drugs, restore the senses and avoid restraints.
- Dementia care is routine, simple communication, safe wandering, nutrition, independence and caregiver support.
- Depression is common and treatable; ask about suicide, secure the means and follow up.

## Practice

```python
m1 = 36 / 40 * 100                              # test positive in 36 of 40 persons with dementia
m2 = 10 * 28 // 5                               # donepezil 10 mg a day for 28 days, 5 mg tablets
m3 = 0.5 / 5                                    # haloperidol 0.5 mg from 5 mg/mL
wt = 58                                         # Mr Narayan
c_kcal, c_fluid = 30 * wt, 30 * wt
c_tabs = 28 + 56                                # 4 weeks at 5 mg, then 4 weeks at 10 mg (two 5-mg tablets)
c_hrs = 14 * 7                                  # caregiver hours a week
print(f"MCQ1 sensitivity = {m1:.0f}%; MCQ2 tablets = {m2}; MCQ3 volume = {m3:.1f} mL")
print(f"Mr Narayan: energy = {c_kcal:,} kcal; fluid 30 mL/kg = {c_fluid:,} mL; donepezil tablets for 8 weeks = {c_tabs}; care = {c_hrs} h/week")
```

```text
MCQ1 sensitivity = 90%; MCQ2 tablets = 56; MCQ3 volume = 0.1 mL
Mr Narayan: energy = 1,740 kcal; fluid 30 mL/kg = 1,740 mL; donepezil tablets for 8 weeks = 84; care = 98 h/week
```

**MCQs (with reasons)**

1. A screening test is positive in 36 of 40 people who have dementia. Its sensitivity is: (a) 40% (b) 90% (c) 36% (d) 4%.
2. Donepezil 10 mg a day is given as 5 mg tablets for 28 days. The number of tablets is: (a) 28 (b) 56 (c) 112 (d) 14.
3. Haloperidol 0.5 mg is ordered from a 5 mg/mL ampoule. The volume is: (a) 0.01 mL (b) 0.1 mL (c) 1 mL (d) 5 mL.
4. An 80-year-old becomes drowsy and inattentive over one day. This is most consistent with: (a) dementia (b) delirium (c) normal ageing (d) depression.
5. The best management of agitation in an older person with dementia after a physical cause is excluded is: (a) a sedative injection (b) non-drug measures first, antipsychotic only for severe distress (c) physical restraint (d) discharge.

::: note Answers and rationales
**1. (b).** Sensitivity = true positives ÷ all diseased = 36 ÷ 40 = 90%; 36% is the count and 4% is the false-negative fraction.
**2. (b).** 10 mg needs two 5-mg tablets a day, so 2 × 28 = 56 tablets; 28 would give only 5 mg a day.
**3. (b).** 0.5 ÷ 5 = 0.1 mL; 1 mL would be 5 mg, a tenfold overdose in an older patient.
**4. (b).** Acute onset with inattention and altered awareness defines delirium, an emergency; dementia and depression do not start in a day.
**5. (b).** Antipsychotics raise the risk of stroke and death in dementia, so non-drug measures come first; restraint worsens agitation.
:::

**Short answer (3 marks): Differences between delirium and dementia.** Delirium starts in hours to days, fluctuates, impairs attention and consciousness from the start, is caused by an acute illness or drug and is usually reversible. Dementia starts over months to years, has a steady course, keeps attention and consciousness clear until late and is irreversible. Delirium can occur on top of dementia and is then easily missed.

**Medium answer (5 marks): Describe the nursing care of a patient with Alzheimer disease (Figure 3.2).** *Assessment:* Mini-Cog or MMSE, ADL (Barthel), behaviour, nutrition and caregiver strain. *Communication:* simple, calm and respectful. *Safety:* a safe home, wandering plan, ID bracelet, locked medicines. *Routine and independence:* fixed daily timetable and encouragement of small tasks. *Nutrition and elimination:* finger foods, fluids and toilet prompts. *Behaviour:* ABC method; antipsychotics only if essential. *Caregiver:* education, respite, support groups and a contact number. *Medicines:* give donepezil at night and watch for slow pulse, nausea and vomiting.

**Long answer (10 marks): Mr Narayan Prasad Sharma, 79 years, a retired teacher weighing 58 kg from Kathmandu, is brought by his wife to the geriatric clinic. For 2 years he has forgotten recent events and misplaced objects; for 3 months he gets lost in the street, wanders at night and does not recognise his grandchildren. He scores MMSE 17/30 and Barthel 65/100. His wife provides care for 14 hours a day, is exhausted and weeps easily. Calculate and write the nursing care plan.**

*Calculations.* MMSE 17 is in the **moderate** range (10-18) and Barthel 65 is moderate dependence (61-90). Donepezil is started at 5 mg at night for 4 weeks (28 tablets) and then 10 mg (two tablets a day, 56 tablets), giving **84 tablets** for 8 weeks. His energy need is 30 kcal/kg, **1,740 kcal**, and fluid 30 mL/kg, **1,740 mL** a day. His wife gives **98 hours of care a week**, a heavy burden.

*Care.* Confirm that delirium, depression, B12 deficiency, thyroid disease and drug effects are excluded. Teach the wife the disease and the ABC approach. Set a daily routine, give simple instructions and use a clock and a calendar. For wandering, fit an ID bracelet and door chime, keep a recent photograph, offer toilet and drinks before sleep, keep the evening calm and use night lights; he must not be locked alone. Give donepezil at night with food and watch for nausea, a pulse below 50 and vomiting. Weigh him monthly. Review the home for stairs, the kitchen stove and medicines. Arrange respite care with a neighbour or a daughter, link the family with a senior citizens' group, and guide them about the ward office, the social security allowance and the Alzheimer and Parkinson treatment support. Discuss legal matters and his wishes about the future while he can still take part. Review monthly.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "He does not know the grandchildren." **O:** MMSE 17/30, disoriented to time and place. | **Chronic confusion** related to Alzheimer disease, as evidenced by memory loss and disorientation. | **Cognitive orientation:** stays calm and safe; orientation cues used daily. | Fixed routine and clock, calendar (reduce confusion); simple one-step instructions (match his ability); reminiscence (preserves identity); donepezil at night as ordered (raises acetylcholine). | Calmer; fewer distress episodes; MMSE stable at 3 months. |
| **S:** "He got up and left at 2 am." **O:** wanders at night, got lost in the street. | **Risk for injury** related to wandering and impaired judgement. | **Safety behaviour:** no injury or getting lost in 3 months. | ID bracelet, recent photograph, door chime (traceable); toilet and drink before sleep (meets the cause of wandering); night lights (visual safety); safe walking in the day (burns energy). | No lost episodes; no injury. |
| **S:** "He wakes me four times a night." **O:** wife tired, sleeping about 4 hours. | **Insomnia** related to day-night reversal; and **Caregiver role strain** related to 14 hours of daily care (98 hours a week). | **Caregiver wellbeing:** wife sleeps 6 hours; shares care with one other person. | Teach disease and ABC approach (confidence); respite and a sharing roster (rest); senior citizens' group and counselling (support); avoid sedatives for him (fall and delirium risk). | Wife sleeps 6 hours; respite arranged weekly. |
| **S:** "He leaves half his rice." **O:** 58 kg, weight loss 2 kg in 2 months. | **Imbalanced nutrition: less than body requirements** related to forgetting to eat. | **Nutritional status:** weight stable; intake of 1,740 kcal and 1,740 mL. | Finger foods, small frequent meals, a cup in view and assistance at the table (compensate for memory loss); monthly weight (early detection); dentures and swallowing check. | Weight steady at 58 kg at 3 months. |
