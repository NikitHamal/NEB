---
subject: Psychiatric Nursing
grade: BSc Nursing Year 2
unit: 1
title: Foundations of Psychiatric Nursing: Mental Health, Nepal's System, the Therapeutic Relationship and the Mental Status Examination
hours: 14
area: BSN 13-14 · Psychiatric Nursing · Unit 1
---

"*Ke garne, pagal bhayo*" (what to do, he has gone mad) is the sentence many Nepali families say before they take a suffering relative to a *dhami* or *jhankri* and only later, if at all, to a health worker. The **National Mental Health Survey, Nepal 2020** (Nepal Health Research Council, NHRC) found that **10% of adults have had a mental disorder in their lifetime and 4.3% have one now**, yet only about **23% of those with a problem sought any treatment**. The psychiatric nurse stands in this gap: she must **notice, listen, assess, treat with safe medicines, protect, and bring the family along**. This unit gives the language and the skills on which every later unit rests. All arithmetic is computed and checked by program.

::: key What this unit gives you
- Real images: Pinel freeing patients at the Salpêtrière, Hogarth's Bedlam, a 19th-century asylum and a Rorschach blot, plus three SVG figures (the mental health continuum, Peplau's four phases, the Nepal service pyramid).
- Definitions, biopsychosocial causes, ICD-11 and DSM-5-TR, the **National Mental Health Survey 2020** numbers and the treatment gap, with checked prevalence and bed calculations.
- Eight points each on the principles of psychiatric nursing, therapeutic communication and patient rights, the full **Mental Status Examination** and defence mechanisms.
- Model answers and a 5-column NANDA-I care plan for a withdrawn, mistrustful young man admitted to the ward.
:::

## 1.1 Mental health, mental illness and the biopsychosocial model

The **World Health Organization** defines **mental health** as "a state of mental well-being that enables people to cope with the stresses of life, realise their abilities, learn well and work well, and contribute to their community". It is **more than the absence of illness**. A person can have a diagnosed illness and still be well supported and productive, and a person without a diagnosis can be in deep distress. Think of a **continuum** (Figure 1.1) that moves with life events, rather than two separate boxes.

```svgfig label="1.1" caption="The mental health continuum and the biopsychosocial model. A person moves along the line with life events, support and treatment (top). Biological, psychological and social factors interact to protect or to harm (bottom). Nurses act on every box: medicines, coping skills and family and community support."
f = Fig(760, 250)
f.box(10, 15, 150, 50, "THRIVING\ncoping, working,\nconnected", fill=MINT, stroke=TEAL, size=11, bold=True)
f.box(200, 15, 150, 50, "SURVIVING\nstressed, tired,\nsleeping badly", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(390, 15, 150, 50, "STRUGGLING\nsymptoms affect\nwork and family", fill=ROSE, stroke=RED, size=11, bold=True)
f.box(580, 15, 170, 50, "IN CRISIS\nrisk of harm,\nneeds admission", fill=ROSE, stroke=RED, color=RED, size=11, bold=True)
f.arrow([(160, 40), (200, 40)], both=True); f.arrow([(350, 40), (390, 40)], both=True); f.arrow([(540, 40), (580, 40)], both=True)
f.box(40, 120, 200, 56, "BIOLOGICAL\ngenes, brain chemistry,\nillness, drugs, sleep", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(280, 120, 200, 56, "PSYCHOLOGICAL\nthinking style, trauma,\ncoping, self-esteem", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(520, 120, 200, 56, "SOCIAL\nfamily, poverty, stigma,\nmigration, disaster", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.arrow([(240, 148), (280, 148)], both=True); f.arrow([(480, 148), (520, 148)], both=True)
f.box(240, 205, 280, 36, "MENTAL HEALTH or ILLNESS (interaction)", fill=SAND, stroke=AMBER, size=11, bold=True)
f.arrow([(140, 176), (260, 205)]); f.arrow([(380, 176), (380, 205)]); f.arrow([(620, 176), (500, 205)])
```

**Mental illness** is a clinically significant disturbance in thinking, emotion or behaviour that causes **distress or disability** and is not a normal response to a culturally accepted event (a widow grieving for months is not ill; a person who stops eating and wants to die a year later may be). **Causes are multiple**: the *biological* (family history, neurotransmitter imbalance, infection, head injury, alcohol), the *psychological* (childhood abuse, loss, poor coping) and the *social* (poverty, debt, foreign labour migration, domestic violence, the 2015 earthquake). This is why treatment combines **medicine, talking therapy and social support**, and why the nurse never explains illness as only "weak mind" or only "witchcraft".

## 1.2 Burden of mental illness and the treatment gap in Nepal

The NHRC survey (2019-2020, all seven provinces; **9,200 adults and 5,888 adolescents**) is the first national mental health survey. It reported **lifetime mental disorder 10.0% and current 4.3% in adults**, **5.2% in adolescents**, current **suicidal thoughts 6.5%** in adults and **lifetime suicide attempt 1.1%**. Only about **23%** of people with a disorder sought treatment, most often from a non-specialist doctor (8.8%), a **faith healer (6.7%)** or a psychiatrist (6.5%). The national plan counts about **1.5 psychiatric beds per 100,000 people**. In **FY 2080/81 Nepal Police recorded 7,221 suicidal deaths**, about 85% by hanging.

```python
adults, teens = 9200, 5888
life, cur, teen = 0.10, 0.043, 0.052
life_n, cur_n, teen_n = round(adults * life), round(adults * cur), round(teens * teen)
seek = 0.23                                    # sought any treatment
per1000 = 1000
treated, untreated = round(per1000 * seek), round(per1000 * (1 - seek))
beds_per_100k, pop = 1.5, 2_000_000            # a province-sized catchment of 2 million
beds = round(pop / 100_000 * beds_per_100k)
print(f"Adults with a lifetime disorder in the sample: {life_n}; current: {cur_n}; adolescents: {teen_n}")
print(f"Of {per1000} people with a disorder: {treated} seek treatment, {untreated} do not (gap {100 - seek * 100:.0f}%)")
print(f"Beds for {pop:,} people at {beds_per_100k} per 100,000 = {beds}")
```

```text
Adults with a lifetime disorder in the sample: 920; current: 396; adolescents: 306
Of 1000 people with a disorder: 230 seek treatment, 770 do not (gap 77%)
Beds for 2,000,000 people at 1.5 per 100,000 = 30
```

Of 9,200 adults, **920** had a lifetime disorder and **396** a current one, and of 5,888 adolescents about **306** had a disorder. For every 1,000 people who need care, only **230** seek it and **770** go without, a **treatment gap of 77%**. A catchment of 2 million people would need only **30 beds** at the national figure, which is why care must move into **health posts and community units**, not wait for hospital beds. Reasons for not seeking help were wanting to solve the problem alone, belief that it would pass and fear of what the family would think.

### Eight principles of psychiatric nursing practice

1. **Accept the person, not the behaviour.** A patient who shouts or refuses food is ill, not rude. The nurse sets calm limits on dangerous acts and keeps respect for the person. Acceptance builds trust, and without trust no treatment works.
2. **Treat the whole person.** Check physical illness, pain, sleep, nutrition and drugs as carefully as thoughts and mood, because thyroid disease, infection, anaemia, drugs and alcohol can all look like a mental disorder. A person with schizophrenia has two to three times the risk of diabetes and heart disease. Weigh, measure the waist and check the blood pressure.
3. **Use the self therapeutically.** Your voice, face, calmness and consistency are tools. Be on time, do what you promise and keep a steady tone. Know your own reactions (fear, anger, pity) and discuss them in supervision.
4. **Keep safety first, with the least restriction.** Assess the risk of suicide, violence and absconding at every shift. Choose the least restrictive method that keeps people safe: talk first, then environment, then medicine, and restraint only last. Every restraint is recorded and reviewed.
5. **Respect confidentiality and consent.** Share information only with the team and with the family as the patient permits, except when life is at risk. Explain every treatment in simple words and ask for consent. Capacity is judged for each decision, not once for all.
6. **Involve the family and community.** In Nepal the family decides, pays and cares. Teach them the illness, medicines and warning signs, and listen to their burden. Link them with the Female Community Health Volunteer, the health post and self-help groups.
7. **Work as a team.** The psychiatrist, nurse, psychologist, social worker and occupational therapist share one plan. The nurse is with the patient 24 hours and observes what no one else sees. Report changes early and record them in clear, factual words.
8. **Hope and recovery.** Most people improve with treatment, and many return to work and family. Use the language of recovery: strengths, goals and small steps. Never tell a patient or family that the illness is "hopeless" or "a curse".

## 1.3 History: from chains to community care

Mental illness has been explained as **possession, sin or moral weakness** in most societies. Asylums were built to hide people, and visitors paid to watch them at **Bedlam (Bethlem Hospital)**, London, in the 1700s. In **1793 Philippe Pinel** at the Bicêtre and the Salpêtrière in Paris ordered the chains struck off and treated patients as sick people. **Kirkbride-plan hospitals** in the United States (1840s onward) offered fresh air and routine, but crowding turned them into long-stay institutions. **Chlorpromazine (1952)** and later drugs made care outside hospital possible, and **deinstitutionalisation** after the 1960s moved care to the community. In 1952 **Hildegard Peplau**, a nurse, published *Interpersonal Relations in Nursing*, describing the nurse-patient relationship as a therapeutic process, and founded modern psychiatric nursing. In Nepal organised services began in the mid-20th century with a psychiatric unit and later the **Mental Hospital at Lagankhel (Patan)**; today **TUTH, Patan, BPKIHS, Bir, PAHS and Koshi** hospitals offer psychiatric units, and the **Community Mental Health Care Package 2017** extends care to primary level.

```photogrid label="1.2" cols="4" ratio="1.0" caption="From chains to tests. (a) Pinel at the Salpêtrière in 1795 orders the chains removed (Tony Robert-Fleury, 1876). (b) Hogarth's engraving of Bedlam (1735): patients are crowded, chained and watched by fashionable visitors. (c) A 19th-century asylum of the Kirkbride type, a large hospital set in grounds. (d) A real Rorschach inkblot, an early projective test whose use today is limited."
@ photo id="nur8/pinel" cap="Pinel frees the insane"
fit 1.0
focus 0.5 0.5
mark 0.50 0.50 "1"
key 1 (a) Pinel: orders the chains removed, the start of humane care
@ photo id="nur8/bedlam" cap="Hogarth, Bedlam 1735"
fit 1.0
focus 0.5 0.5
mark 0.30 0.35 "2"
key 2 (b) Chained patients: restraint and public display were routine
@ photo id="nur8/kirkbride" cap="Asylum building"
fit 1.0
focus 0.5 0.5
mark 0.50 0.70 "3"
key 3 (c) Central block with wings: a large, isolated institution
@ photo id="nur8/rorschach" cap="Rorschach inkblot"
fit 1.0
focus 0.5 0.5
mark 0.50 0.50 "4"
key 4 (d) Inkblot no. 8: patients describe what they see; ambiguity is the test
```

## 1.4 Classification and Nepal's service pyramid

Doctors diagnose with the **ICD-11** (WHO, in force from 2022) or the **DSM-5-TR** (American Psychiatric Association, 2022). Both group disorders by cluster (psychotic, mood, anxiety, trauma, substance, neurodevelopmental, personality). A diagnosis needs a **pattern of symptoms for a minimum time with distress or impairment**, and the nurse supports it by accurate observation and recording. At primary level the **WHO mhGAP Intervention Guide 2.0** lists seven **priority conditions**: depression, psychoses (including bipolar disorder), epilepsy, child and adolescent disorders, dementia, substance use disorders and self-harm or suicide. Nepal trains medical officers, health assistants and nurses in mhGAP under the **National Mental Health Strategy and Action Plan 2020 (2021-2025)**, which promises **free primary mental health care** and stronger secondary care, though implementation is limited.

```svgfig label="1.3" caption="Nepal's mental health service pyramid. Most people should be first seen at the base (health post, FCHV, community) by a worker trained in mhGAP; harder cases move up. Referral flows up and the patient returns down for follow-up, so the nurse is the link between levels."
f = Fig(760, 270)
f.poly([(380, 15), (300, 60), (460, 60)], fill=ROSE, stroke=RED, label="TERTIARY", lx=380, ly=44, size=10, color=RED)
f.poly([(295, 66), (465, 66), (520, 112), (240, 112)], fill=SAND, stroke=AMBER, label="Provincial / teaching hospital psychiatry unit", lx=380, ly=92, size=10, color=SLATE)
f.poly([(235, 118), (525, 118), (590, 164), (170, 164)], fill=BLUE, stroke=NAVY, label="District / PHCC: psychiatric nurse, medical officer (mhGAP), drugs", lx=380, ly=144, size=10, color=SLATE)
f.poly([(165, 170), (595, 170), (670, 216), (90, 216)], fill=MINT, stroke=TEAL, label="Health post: mhGAP-trained health worker, basic drugs, follow-up", lx=380, ly=196, size=10, color=SLATE)
f.poly([(85, 222), (675, 222), (750, 262), (10, 262)], fill=SOFT, stroke=SLATE, label="Community: FCHV, family, schools, mothers' groups, NGOs (TPO Nepal, CMC-Nepal)", lx=380, ly=246, size=10, color=SLATE)
f.text(620, 40, "Refer UP when needed;\nreturn DOWN for follow-up", size=11, color=NAVY, bold=True)
```

## 1.5 The therapeutic nurse-patient relationship (Peplau)

A **therapeutic relationship** is a planned, goal-directed, time-limited relationship in which the nurse uses communication and self-awareness to help the patient. It differs from a social relationship: it is **for the patient's benefit**, the nurse carries the professional boundary, and it ends when the goals are met. **Peplau's four phases** describe how it grows (Figure 1.4), and her **nurse roles** (stranger, resource person, teacher, leader, surrogate, counsellor) show how the nurse's function changes with the patient's need.

```svgfig label="1.4" caption="Peplau's four phases of the nurse-patient relationship. Each phase has a task for the nurse. Termination begins to be discussed in the orientation phase so that the patient is never surprised, and a discharge plan with follow-up at the health post closes the work."
f = Fig(760, 230)
f.box(10, 70, 160, 90, "1. ORIENTATION\nstrangers meet; set\ncontract, time, place,\nconfidentiality", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(200, 70, 160, 90, "2. IDENTIFICATION\npatient responds;\nproblems named; trust\ngrows", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(390, 70, 160, 90, "3. EXPLOITATION\npatient uses help;\nskills practised;\ngoals pursued", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(580, 70, 170, 90, "4. RESOLUTION\n(termination) goals met;\nsummary, feelings of\nloss, follow-up plan", fill=ROSE, stroke=RED, color=RED, size=10.5, bold=True)
f.arrow([(170, 115), (200, 115)]); f.arrow([(360, 115), (390, 115)]); f.arrow([(550, 115), (580, 115)])
f.text(90, 30, "Nurse: stranger", size=11, color=NAVY, bold=True); f.text(280, 30, "Nurse: resource, teacher", size=11, color=TEAL, bold=True)
f.text(470, 30, "Nurse: leader, counsellor", size=11, color=AMBER, bold=True); f.text(665, 30, "Nurse: surrogate, guide", size=11, color=RED, bold=True)
f.text(380, 200, "Boundaries throughout: no gifts, no secrets, no personal contact outside care, supervision", size=11, color=SLATE)
```

### Therapeutic communication: eight techniques

1. **Active listening.** Face the patient, keep an open posture, nod and give your full attention without looking at the clock. Listen to the feeling behind the words as well as the facts. Many patients improve simply because someone finally listened.
2. **Open-ended questions.** Ask "How have you been sleeping?" or "Tell me what has been worrying you" instead of questions that need only yes or no. This invites the patient to lead. Use closed questions only for facts and for suicide screening.
3. **Reflecting.** Return the patient's feeling in your own words: "You feel nobody understands you." This shows that you heard and invites more. Do not parrot every phrase.
4. **Clarifying.** Say "I am not sure I understood; do you mean you hear voices at night?" This avoids wrong assumptions and keeps the story accurate. It is especially important with a patient whose speech is vague or jumbled.
5. **Using silence.** A pause of a few seconds lets the patient think and cry. Stay present and calm and do not rush to fill the quiet. Silence is respectful when it is warm and short.
6. **Offering self.** "I will sit with you for ten minutes" gives presence without demands. It helps the withdrawn or frightened patient most. Keep the promise and keep to the time.
7. **Focusing and summarising.** Gently bring a wandering talker back to the main concern and end with a short summary: "So the main things are poor sleep, fear at night and no appetite." This gives structure and checks understanding.
8. **Giving information and showing empathy.** Say plainly what will happen, what the tablet is for and when the doctor will come. Empathy means "I can see how hard this is," not "I know exactly how you feel". Truthful, simple information lowers fear.

**Blocks to avoid:** false reassurance ("don't worry, everything will be fine"), giving advice before understanding, changing the subject, asking "why" questions that sound like blame, agreeing with a delusion, arguing with it, and judging ("that is wrong"). **Respond to a delusion** with "I understand this is very real for you; I do not see it myself, but I can see it frightens you."

## 1.6 The Mental Status Examination (MSE)

The **MSE** is the psychiatric equivalent of a physical examination: a structured description of the patient's mind **at the time of the interview**. It is observed, not guessed, and it is written in plain descriptive words. The nurse completes it on admission and repeats it every shift or day to detect change.

| Domain | What is observed | Example of a written finding |
|---|---|---|
| **Appearance and behaviour** | Grooming, dress, eye contact, posture, movements, rapport | Unkempt, wearing yesterday's clothes, avoids eye contact, sits at the edge of the bed |
| **Speech** | Rate, volume, amount, flow | Quiet, slow, answers in 2-3 words |
| **Mood** (patient's words) and **affect** (observed) | Sadness, elation, anxiety; range, match with content | Mood "fine"; affect flat and restricted |
| **Thought process (form)** | Logical, circumstantial, tangential, loosening of association, flight of ideas | Linear but sparse |
| **Thought content** | Delusions, obsessions, phobias, suicidal or violent ideas | Suspicion that neighbours speak about him; denies suicidal thoughts |
| **Perception** | Hallucinations (auditory, visual), illusions, depersonalisation | Denies hearing voices; seen looking at the wall |
| **Cognition** | Orientation (time, place, person), attention (serial 7s), memory, abstract thinking | Oriented; serial 7s 4 of 5 correct |
| **Insight** | Awareness of illness and need for treatment | Poor: "I am not ill; they are against me" |
| **Judgement** | Decisions in a practical situation | Impaired: refuses food because he thinks it is poisoned |

```python
start, step, tries = 100, 7, 5
expected = [start - step * i for i in range(1, tries + 1)]
said = [93, 86, 78, 71, 64]                      # patient's answers
prev, score = start, 0
for s in said:
    score += (s == prev - step)                  # MMSE style: each answer is judged from the previous answer
    prev = s
checks30, checks15 = 24 * 60 // 30, 24 * 60 // 15
print(f"Correct serial 7s: {expected}")
print(f"Patient said {said}: score {score} of {tries}")
print(f"Observation checks in 24 h: every 30 min = {checks30}, every 15 min = {checks15}")
```

```text
Correct serial 7s: [93, 86, 79, 72, 65]
Patient said [93, 86, 78, 71, 64]: score 4 of 5
Observation checks in 24 h: every 30 min = 48, every 15 min = 96
```

Serial sevens from 100 should give **93, 86, 79, 72, 65**; the patient said 93, 86, 78, 71, 64 and scores **4 of 5** (each answer judged against the previous one, the MMSE method). A patient on **intermittent observation every 30 minutes** is checked **48 times a day**; on **every 15 minutes**, **96 times**; a patient at high risk needs **continuous (1:1) observation**, with the nurse within arm's reach.

**Defence mechanisms** are unconscious ways in which the mind lowers anxiety (Freud, Anna Freud). The nurse uses them to *understand* behaviour, not to attack it.

| Mechanism | Meaning | Example |
|---|---|---|
| **Denial** | Refusing to accept a painful reality | "I do not have a problem with alcohol." |
| **Projection** | Attributing own unacceptable feelings to others | A man who is angry says "everyone is angry with me." |
| **Displacement** | Shifting feeling to a safer target | A father scolded at work beats his child |
| **Repression** | Pushing a painful memory out of awareness | A trauma survivor cannot recall the event |
| **Regression** | Returning to earlier behaviour | A hospitalised child wets the bed again |
| **Rationalisation** | Giving a logical excuse | "I drink only because my job is stressful." |
| **Reaction formation** | Acting the opposite of the true feeling | Over-kindness to a resented relative |
| **Sublimation** | Turning an impulse into a useful act | Aggression channelled into football or boxing |

## 1.7 Ethics, law and the rights of the patient in Nepal

Nepal has **no standalone Mental Health Act in force** (a draft has been discussed for years). Care therefore rests on several instruments: the **Constitution of Nepal 2072** (right to health), the **Act Relating to the Rights of Persons with Disabilities 2074 (2017)**, the **Muluki Civil and Criminal Codes 2074**, the **National Health Policy 2019**, the **National Mental Health Strategy and Action Plan 2020**, the **Community Mental Health Care Package 2017** and the **Nepal Nursing Council Act 2052 and Code of Ethics**. **Section 185 of the Criminal Code punishes abetting suicide** (up to five years' imprisonment and a fine of Rs 50,000, as reported); an attempt is treated as a health problem needing care. A hospital must not treat a patient against their will outside its own policy and the principles of necessity, so every unit should follow a written involuntary admission and restraint protocol.

### Eight rights of the psychiatric patient and the nurse's duty

1. **Right to dignity and humane care.** The patient must not be beaten, shouted at, shamed or locked in a room. Use the patient's name and respectful words, give privacy for toilet and bath and protect from teasing by other patients. Humane care is the first ethical duty of the nurse.
2. **Right to information and informed consent.** The patient is told, in simple language, the diagnosis, the treatment, its side effects and the alternatives. Consent is sought for each treatment, especially ECT. If the patient lacks capacity, the legal guardian consents and the patient is still told what is happening.
3. **Right to confidentiality.** Records and talk about the illness are shared only with those directly involved in care. Never discuss patients in corridors or on social media. Break confidentiality only to prevent serious harm, and tell the patient when you must.
4. **Right to the least restrictive treatment.** Hospital care is used only when community care cannot keep the person safe. Seclusion and restraint are last resorts, ordered by a doctor, time-limited, observed continuously and recorded. They are never punishment.
5. **Right to treatment and medicines.** The patient should receive the right drug in the right dose, with monitoring of side effects. Free essential medicines are available at government facilities under the basic health service package. Stopping medicine suddenly is dangerous, so teach adherence.
6. **Right to protection from abuse and exploitation.** Patients must be safe from physical, sexual and financial abuse by staff, other patients and family. Report any concern at once. Property is listed and kept safe on admission.
7. **Right to communication and contact.** Patients may talk to family and keep personal belongings in a reasonable way unless there is clinical reason to restrict, which is then recorded. Family visits help recovery. Allow religious practice and cultural food.
8. **Right to rehabilitation and community life.** Discharge planning starts on admission. The patient and family receive medicine supply, a follow-up date, the contact of the nearest health post and help with school, work or the disability card. The aim is a return to ordinary life.

## Formula and fact sheet

- Prevalence in a sample = cases ÷ sample × 100; treatment gap = 100 − % who sought treatment. NMHS 2020: lifetime 10.0%, current 4.3% (adults); adolescents 5.2%; 23% sought help.
- Observation checks per day = 1,440 ÷ interval in minutes (every 30 min = 48; every 15 min = 96).
- Peplau phases: orientation, identification, exploitation, resolution. MSE: appearance and behaviour, speech, mood and affect, thought form and content, perception, cognition, insight, judgement.
- mhGAP priority conditions: depression, psychoses, epilepsy, child and adolescent disorders, dementia, substance use, self-harm or suicide.

## Chapter summary

- Mental health is a continuum shaped by biological, psychological and social factors; in Nepal 4.3% of adults have a current disorder but about 77% receive no treatment.
- Psychiatric nursing grew from the freeing of patients by Pinel to Peplau's therapeutic relationship and community care.
- Therapeutic communication (listening, open questions, reflecting, silence) and the MSE are the nurse's core tools; defence mechanisms explain behaviour.
- Nepal has no standalone mental health act; the Disability Rights Act 2074, Criminal Code section 185, NNC code and the 2020 Strategy guide practice. Rights, consent and least restriction apply.

## Practice

```python
adults, cur = 9200, 0.043
m1 = round(adults * cur)                         # MCQ1
m4 = 24 * 60 // 15                               # MCQ4 checks a day at 15 min
wt, ht = 48, 1.68                                # Mr Ram Bahadur Thapa
bmi = wt / ht ** 2
fluid = 30 * wt
meals = 3 * 7                                    # three meals a day for a week
print(f"MCQ1 = {m1}; MCQ4 = {m4}")
print(f"Mr Thapa: BMI = {bmi:.1f} kg/m2; fluid at 30 mL/kg = {fluid:,} mL; meals observed in a week = {meals}")
```

```text
MCQ1 = 396; MCQ4 = 96
Mr Thapa: BMI = 17.0 kg/m2; fluid at 30 mL/kg = 1,440 mL; meals observed in a week = 21
```

**MCQs (with reasons)**

1. In a survey of 9,200 adults, 4.3% have a current mental disorder. The number of people is about: (a) 92 (b) 396 (c) 920 (d) 4,300.
2. The phase in which the patient actively uses the nurse's help to solve problems is: (a) orientation (b) identification (c) exploitation (d) resolution.
3. "You feel nobody cares about you?" is an example of: (a) false reassurance (b) reflecting (c) advising (d) changing the subject.
4. A patient on 15-minute observation is checked how many times in 24 hours: (a) 24 (b) 48 (c) 96 (d) 144.
5. Which statement about mental health law in Nepal is correct: (a) a Mental Health Act of 2052 governs all admissions (b) there is no standalone Mental Health Act; Section 185 of the Criminal Code punishes abetting suicide (c) suicide attempts are punished by prison (d) only psychiatrists may give care.

::: note Answers and rationales
**1. (b).** 9,200 × 0.043 = 395.6, about 396; 920 is the lifetime count (10%) and 92 is 1%.
**2. (c).** In exploitation the patient uses the services offered; orientation is the meeting, identification the naming of problems and resolution the ending.
**3. (b).** The nurse returns the feeling in other words to invite more; reassurance, advice and changing the subject close the conversation.
**4. (c).** 1,440 minutes ÷ 15 = 96 checks; 48 would be every 30 minutes.
**5. (b).** Nepal still has no standalone act; the Criminal Code 2074 section 185 targets abetment, and an attempt is treated as a health problem.
:::

**Short answer (3 marks): Differences between a therapeutic and a social relationship.** A therapeutic relationship is planned, goal-directed and for the patient's benefit; the nurse carries the professional boundary, communication is structured and confidential, and the relationship ends when goals are met. A social relationship is spontaneous, mutual, has no fixed goal and may continue for life. In therapy the nurse's own needs are not met through the patient.

**Medium answer (5 marks): Describe the phases of the nurse-patient relationship (Peplau) (Figure 1.4).** *Orientation:* the nurse and patient meet as strangers; the nurse explains her role, sets the contract (time, place, confidentiality) and assesses the problem. *Identification:* the patient responds to those who seem to help, the problems are named and trust grows. *Exploitation:* the patient uses the services fully, skills are practised and goals are pursued; the nurse acts as resource, teacher and counsellor. *Resolution (termination):* the goals are met, the nurse reviews progress, handles feelings of loss and links the patient to follow-up. Boundaries and supervision apply in every phase, and termination is discussed from the start.

**Long answer (10 marks): Mr Ram Bahadur Thapa, 22 years, a student from Sindhupalchok weighing 48 kg (height 1.68 m), is brought to the psychiatric ward by his brother. For three weeks he has stayed in his room, eaten little and said that neighbours talk about him. He is unkempt, avoids eye contact, answers in two or three words, says his mood is "fine", has a flat affect, believes his food may be poisoned, denies voices and suicidal thoughts, is oriented, scores 4 of 5 on serial 7s and has poor insight. Write the MSE, the calculations and the nursing care plan.**

*Calculations.* BMI = 48 ÷ 1.68² = **17.0 kg/m²**, which is underweight (below 18.5). Fluid at 30 mL/kg = **1,440 mL** a day. Meals are observed three times a day, **21 in a week**. Observation: he has suspicious ideas but denies suicide or violence, so intermittent observation every **30 minutes (48 checks a day)** is chosen, to be increased if risk rises.

*MSE.* Unkempt, poor eye contact; speech sparse and slow; mood "fine", affect flat; thought form linear but sparse; content of persecutory suspicion and fear of poisoning (a possible delusion); no hallucinations or suicidal ideas reported; oriented, attention intact, serial 7s 4 of 5; insight poor and judgement impaired by food refusal.

*Care.* Introduce yourself, orient him to the ward and agree a regular 15-minute daily talk. Use short, calm sentences and avoid arguing with the suspicion. Offer sealed packets and let him open them himself and eat with a trusted brother. Record intake and weight twice a week and refer for a dietitian. Help with bath, clean clothes and sleep routine. Give medicines as ordered and observe for side effects. Assess risk each shift. Teach the brother that the illness is treatable, not a curse, and that medicines must continue. Plan follow-up at the nearest health post and link him with the college for a return to study.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "They are all talking about me." **O:** stays in room 3 weeks, avoids eye contact, answers in 2-3 words. | **Social isolation** related to mistrust and persecutory ideas, as evidenced by withdrawal and few words. | **Social involvement:** talks with the nurse daily and joins one group activity within 2 weeks. | Daily 15-minute one-to-one talk (builds trust gradually); consistent staff (reduces fear); do not argue with the belief (avoids defence); invite to a short walk or carrom game (small step back to contact). | Talks 5 minutes with the nurse and joins one activity by day 14. |
| **S:** "The food may be poisoned." **O:** BMI 17.0, eats little. | **Imbalanced nutrition: less than body requirements** related to fear of poisoning, as evidenced by weight 48 kg and low intake. | **Nutritional status:** eats at least 75% of meals and gains 1 kg in 3 weeks. | Sealed packets he opens himself and brother present (reduces fear of tampering); small frequent meals; fluid 1,440 mL a day (hydration); weigh twice a week (monitor response); dietitian referral (energy plan). | Eats 75% of meals; weight up 1 kg at 3 weeks. |
| **O:** unkempt, same clothes for days. | **Self-care deficit: bathing and hygiene** related to withdrawal and low motivation. | **Self-care: hygiene:** bathes and changes clothes daily with prompts. | Prompt kindly and give a set time (routine); provide soap and clean clothes (remove barriers); praise each success (reinforce); privacy during care (dignity). | Bathes daily with one prompt by day 7. |
| **S:** Brother: "We took him to a dhami first." **O:** brother anxious, unsure how to help. | **Ineffective health management** (family) related to lack of knowledge and stigma. | **Knowledge: illness and medicines:** brother names the illness, three warning signs and the medicine plan. | Teach causes, treatment and the role of the health post in simple words (corrects the curse belief); written follow-up date (continuity); involve in discharge planning (shares the burden); give the contact number (safety net). | Brother repeats the plan and attends follow-up. |

