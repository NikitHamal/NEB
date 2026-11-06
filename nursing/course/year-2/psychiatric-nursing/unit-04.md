---
subject: Psychiatric Nursing
grade: BSc Nursing Year 2
unit: 4
title: Anxiety, OCD, Trauma and Dissociative Disorders: Fear, Rituals, Earthquake Stress and "Possession"
hours: 14
area: BSN 13-14 · Psychiatric Nursing · Unit 4
---

A nursing student in Dharan rushes into the emergency room: her heart is pounding at 118 a minute, she is breathing at 28, her hands are tingling and she believes she is dying. The ECG and thyroid tests are normal. This is a **panic attack**. Anxiety and stress-related disorders are the commonest mental disorders. The **National Mental Health Survey 2020** found current **neurotic and stress-related disorders in 3% of adults** (about **276** of the 9,200 surveyed) and **2.8% of adolescents** (about **165** of 5,888), the commonest group in young people. In Nepal the **2015 earthquake, the 1996-2006 conflict, foreign labour migration and domestic violence** add trauma to everyday worry, and distress often appears as **body complaints**, "tension" or spirit "possession". The nurse must separate normal fear from disorder, treat panic calmly, and know the first-line talking and drug treatments. All numbers are checked by program.

::: key What this unit gives you
- A real **amygdala** brain image, Munch's **The Scream**, a real **diazepam** tablet photograph and three SVG figures (the four levels of anxiety, GABA action, trauma timeline).
- Generalised anxiety, **panic disorder**, phobias, **OCD** with the **Y-BOCS** score, acute stress reaction, **PTSD** with the PCL-5, adjustment, conversion and dissociative disorders, and a table of personality and childhood disorders.
- **Psychological first aid**, relaxation and breathing, graded exposure, SSRIs and **benzodiazepines with dependence risks and equivalent doses**, with checked calculations.
- Eight points each on anxiety care, panic management, trauma response and conversion disorder; model answers and a NANDA-I plan for a student with panic disorder and avoidance.
:::

## 4.1 Anxiety and the anxiety disorders

**Anxiety** is a feeling of worry, tension and dread about a future threat, with body signs of **sympathetic activation**: fast pulse, sweating, tremor, dry mouth, chest tightness, overbreathing and "butterflies". **Fear** is the reaction to a present danger. Both are normal and useful. An **anxiety disorder** exists when the fear is **excessive, persistent (typically six months for GAD), out of proportion and causes distress or avoidance**. **Peplau** described four **levels of anxiety** (Figure 4.1), which guide how the nurse speaks and acts.

```svgfig label="4.1" caption="Peplau's four levels of anxiety. As anxiety rises, perception narrows and learning falls. At mild and moderate levels the nurse can teach and problem-solve; at severe level only short, calm commands work; in panic the person needs a safe place, a calm presence and brief instructions. Do not leave a panicking person alone."
f = Fig(760, 250)
f.box(10, 60, 170, 110, "MILD\nalert, curious, learns\nbest; restlessness\nNurse: teach, explore", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(200, 60, 170, 110, "MODERATE\nnarrowed attention,\nvoice shaky, tension\nNurse: guide, simple talk", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(390, 60, 170, 110, "SEVERE\nsees only the threat,\nheadache, tremor\nNurse: short commands", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(580, 60, 170, 110, "PANIC\nterror, loss of control,\nunreal feeling\nNurse: stay, safe place", fill=ROSE, stroke=RED, color=RED, size=10.5, bold=True)
f.arrow([(180, 115), (200, 115)]); f.arrow([(370, 115), (390, 115)]); f.arrow([(560, 115), (580, 115)])
f.arrow([(30, 205), (730, 205)], color=SLATE, sw=2, label="anxiety rises: perception narrows, learning falls", lpos=(380, 196))
f.text(380, 30, "Peplau: levels of anxiety", size=12, color=NAVY, bold=True)
```

| Disorder | Core features | Key points for care |
|---|---|---|
| **Generalised anxiety disorder (GAD)** | Excessive worry about many things on most days for 6 months, with restlessness, fatigue, poor concentration, irritability, muscle tension, poor sleep | **GAD-7**; CBT, relaxation; SSRI; avoid long-term benzodiazepines |
| **Panic disorder** | Recurrent unexpected **panic attacks** peaking within about 10 minutes (palpitations, sweating, tremor, breathlessness, chest pain, dizziness, fear of dying or going mad), then fear of another attack | Rule out heart, thyroid, asthma, caffeine, alcohol; breathing training; SSRI; CBT |
| **Agoraphobia** | Fear of places where escape is hard (buses, crowds, markets) | Graded exposure; avoid reinforcing avoidance |
| **Social anxiety disorder** | Fear of embarrassment in social or performance situations | CBT, SSRI; group practice |
| **Specific phobia** | Intense fear of an object or situation (dogs, heights, blood, injections) | Systematic desensitisation and exposure |

**Fear circuit.** A threat is registered by the **amygdala**, which triggers the **hypothalamus** and brainstem to release adrenaline and cortisol (fight-or-flight); the **prefrontal cortex** and **hippocampus** normally judge whether the threat is real. In anxiety disorders the amygdala is overactive and the prefrontal "brake" is weak, and **GABA**, the main inhibitory transmitter, is relatively low (Plate 4.4). A panic attack is a false alarm of this system; it is **not dangerous** and ends within about 20-30 minutes, which is the most important thing to tell the patient.

```photogrid label="4.2" cols="2" ratio="1.0" caption="Fear in art and in the brain. (a) The Scream by Edvard Munch (1893), an iconic image of panic and dread: wide eyes, open mouth, hands on the face and a swirling world. (b) A real brain illustration (coronal slice) with the two amygdalae in green, the almond-shaped structures that trigger the fear response, deep in the temporal lobes."
@ photo id="nur8/scream" cap="Munch, The Scream, 1893"
fit 1.0
focus 0.5 0.55
mark 0.50 0.40 "1"
mark 0.50 0.78 "2"
key 1 (a) Hands on the face, open mouth: acute panic and terror
key 2 (a) Swirling red sky: the surroundings feel unreal (derealisation)
@ photo id="nur8/amyg" cap="Amygdala in the brain"
fit 1.0
focus 0.5 0.0
mark 0.35 0.52 "3"
mark 0.67 0.52 "4"
key 3 (b) Left amygdala (green): registers threat and starts the fear response
key 4 (b) Right amygdala (green): overactive in anxiety and PTSD
```

```python
gad = [2, 2, 3, 2, 1, 1, 2]                     # GAD-7 items, each 0-3
total = sum(gad)
band = "minimal" if total <= 4 else "mild" if total <= 9 else "moderate" if total <= 14 else "severe"
lor_mg = 2.0                                     # lorazepam 2 mg a day
dz_per_lor = 10.0                                # lorazepam 1 mg is roughly diazepam 10 mg
dz_equiv = lor_mg * dz_per_lor
bd, days = 2, 10                                 # diazepam 5 mg twice a day for 10 days (short course)
tabs = bd * days
print(f"GAD-7 total = {total} ({band}); 10 or more means further assessment")
print(f"Lorazepam {lor_mg:.0f} mg = diazepam {dz_equiv:.0f} mg a day (approximate equivalence)")
print(f"Diazepam 5 mg twice a day for {days} days = {tabs} tablets")
```

```text
GAD-7 total = 13 (moderate); 10 or more means further assessment
Lorazepam 2 mg = diazepam 20 mg a day (approximate equivalence)
Diazepam 5 mg twice a day for 10 days = 20 tablets
```

The GAD-7 items add to **13**, which is **moderate** (10-14; 15-21 is severe), and a score of **10 or more** needs further assessment. Lorazepam 2 mg a day is about **20 mg** of diazepam (the equivalence used when switching to diazepam for withdrawal). A short course of diazepam 5 mg twice daily for 10 days is **20 tablets**; benzodiazepines are limited to **2-4 weeks** because of tolerance and dependence.

### Anxiety and panic: eight points of nursing care

1. **Stay calm and stay close.** Your calm voice and slow movements spread safety. Stay with a person who is panicking, as a person left alone feels more fear. Speak in short, clear sentences: "You are safe. I am here. This will pass."
2. **Rule out physical causes.** Check pulse, BP, temperature, oxygen saturation, glucose and ECG when chest pain or breathlessness occurs. Ask about caffeine, tobacco, alcohol, cannabis, thyroid symptoms and drugs such as salbutamol. Never dismiss chest pain without checking.
3. **Teach slow breathing.** Overbreathing lowers carbon dioxide and causes tingling and dizziness. Teach breathing in for 4 seconds and out for 6 seconds, through the nose, with a hand on the abdomen, for 5 minutes. A paper-bag rebreather is not advised.
4. **Use grounding.** Ask the patient to name 5 things seen, 4 touched, 3 heard, 2 smelled and 1 tasted, or to press the feet on the floor. Grounding pulls attention from the body alarm to the present and lowers derealisation.
5. **Explain the physiology.** Say plainly that panic is a false alarm of the fear system and cannot cause death, madness or a heart attack. Understanding removes the fear of fear that drives repeat attacks. Draw Figure 4.1 or the fear circuit for the patient.
6. **Teach relaxation and lifestyle.** Teach progressive muscle relaxation (tense each muscle group for 5 seconds, then release), regular sleep, exercise, less caffeine and tea, and no alcohol. Practise daily, as a skill that needs repetition. Yoga and meditation, familiar in Nepal, are acceptable adjuncts.
7. **Support exposure and stop avoidance.** Avoidance maintains anxiety. With a therapist, agree a graded list from easy to hard (sit near the lecture hall, enter for 5 minutes, take a short bus ride) and praise every step. Do not rescue the patient from every feared situation.
8. **Give medicine wisely and teach.** SSRIs (fluoxetine, sertraline) take 2-4 weeks, may cause jitteriness at first and are started at a low dose. Benzodiazepines are for short use only (a few days to 4 weeks) because of dependence. Never stop an SSRI suddenly.

## 4.2 Obsessive-compulsive disorder (OCD)

**OCD** has **obsessions** (unwanted, intrusive thoughts, images or urges that cause distress: contamination, doubt, harm, order, religious or sexual thoughts) and **compulsions** (repeated acts or mental rituals done to reduce the distress: washing, checking, counting, ordering, praying, reassurance). The person knows the thoughts are their own and often excessive (**insight present** in most). The disorder is diagnosed when rituals take **more than one hour a day** or cause distress or impairment. Lifetime prevalence is about **1-2%**, usually starting in adolescence or early adulthood. Compulsions give short relief, which reinforces the cycle (obsession, anxiety, compulsion, relief, and the obsession returns stronger). In Nepal, purity and religious concerns may be mistaken for piety or for "possession", so patients delay care for years.

The **Yale-Brown Obsessive Compulsive Scale (Y-BOCS)** has 10 items scored 0-4 (total 0-40): **0-7 subclinical, 8-15 mild, 16-23 moderate, 24-31 severe, 32-40 extreme**. Treatment is **exposure and response prevention (ERP)** (facing the feared trigger and not doing the ritual until the anxiety falls) plus an **SSRI at higher doses** (fluoxetine 40-60 mg), and clomipramine as second line; benefit takes **8-12 weeks**.

```python
ybocs = [3, 2, 3, 2, 3, 3, 2, 3, 2, 3]            # 10 items, each 0-4
y_total = sum(ybocs)
y_band = next(n for top, n in [(7, "subclinical"), (15, "mild"), (23, "moderate"), (31, "severe"), (40, "extreme")] if y_total <= top)
washes, minutes = 25, 4                          # hand-washing 25 times a day, 4 minutes each
daily_min = washes * minutes
weekly_h = daily_min * 7 / 60
waking = 16 * 60
share = daily_min / waking * 100
print(f"Y-BOCS total = {y_total} ({y_band})")
print(f"Washing = {washes} x {minutes} min = {daily_min} min a day = {weekly_h:.1f} h a week = {share:.1f}% of a 16-h day")
```

```text
Y-BOCS total = 26 (severe)
Washing = 25 x 4 min = 100 min a day = 11.7 h a week = 10.4% of a 16-h day
```

A Y-BOCS total of **26** is **severe**. A patient who washes 25 times a day for 4 minutes spends **100 minutes** (1.7 hours) daily, **11.7 hours a week** and **10.4%** of the waking day on the ritual, which is well over the one-hour diagnostic threshold.

### OCD: eight points of nursing care

1. **Accept the person and the distress.** Do not say "just stop" or ridicule the ritual; the patient already knows it is excessive. Show respect and curiosity. Shame hides symptoms for years.
2. **Assess the rituals fully.** Ask what the thoughts are, which rituals follow, how long they take and what the patient fears will happen. Record hours spent and avoided places, and use the Y-BOCS. Also screen for depression and suicide, which are common.
3. **Do not forcibly stop rituals.** Blocking a ritual suddenly raises anxiety and may cause aggression. Agree a plan with the patient and therapist, and delay the ritual in steps (wait 5 minutes, then 10).
4. **Avoid giving reassurance again and again.** Repeated reassurance feeds the compulsion. Reply kindly once and then say, "We agreed I would not answer that question again; let us breathe together."
5. **Support ERP.** Help the patient list triggers from least to most frightening, practise exposure and resist the ritual while the nurse stays. Record each success. Progress is gradual over weeks.
6. **Protect skin and health.** Excessive washing causes cracked, bleeding hands, and checking costs sleep and meals. Provide moisturiser and lukewarm water, treat dermatitis, and supervise nutrition and rest.
7. **Give SSRIs and teach.** Explain that doses are higher than for depression and the benefit takes 8-12 weeks, so patience is needed. Watch for nausea, sleep change, sexual side effects and serotonin syndrome. Do not stop suddenly.
8. **Educate and involve the family.** Teach the family not to join in rituals or give repeated reassurance, but to praise effort. Explain that OCD is an illness, not a lack of willpower or a spiritual failure. Offer family counselling.

## 4.3 Trauma and stressor-related disorders

A **trauma** is exposure to death, serious injury or sexual violence, directly, as a witness or through a close person. In Nepal, trauma includes the **2015 Gorkha earthquake** (about 9,000 deaths and large losses of homes), the decade of **armed conflict (1996-2006)**, road and workplace accidents, floods and landslides, **gender-based violence, trafficking and abuse of migrant workers**. Most people recover with time and support; some develop disorder (Figure 4.3).

```svgfig label="4.3" caption="Trauma timeline. In the first hours to days, psychological first aid and safety are the priority. An acute stress reaction lasts from 3 days to 1 month; if symptoms persist beyond 1 month and cause impairment, PTSD is diagnosed. Most people recover without a disorder when safe and supported; some need trauma-focused therapy and medicines."
f = Fig(760, 240)
f.line(30, 100, 730, 100, color=SLATE, sw=2.5)
for x, s in [(60, "Event"), (200, "Days"), (400, "1 month"), (600, "Months-years")]:
    f.circle(x, 100, 6, fill=NAVY, stroke=NAVY); f.text(x, 124, s, size=11, color=NAVY, bold=True)
f.box(100, 20, 200, 56, "ACUTE STRESS REACTION\nshock, numbness, fear\n(hours to 1 month)", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(420, 20, 300, 56, "PTSD: intrusion, avoidance, negative mood,\nhyperarousal, more than 1 month", fill=ROSE, stroke=RED, color=RED, size=10.5, bold=True)
f.box(30, 160, 220, 56, "PSYCHOLOGICAL FIRST AID\nsafety, comfort, Look-Listen-Link", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(300, 160, 440, 56, "TRAUMA-FOCUSED CBT or EMDR, SSRI (sertraline), sleep and nightmare care,\nfamily support, return to work and school", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
```

| PTSD cluster | Examples | Nursing note |
|---|---|---|
| **Intrusion (re-experiencing)** | Flashbacks, nightmares, distress at reminders | Ground with the 5-4-3-2-1 method; do not push for details |
| **Avoidance** | Avoids places, people, talk about the event | Respect pace; gentle graded return |
| **Negative mood and thinking** | Guilt ("why did I survive"), detachment, numbness, memory gaps | Normalise, challenge guilt gently |
| **Hyperarousal** | Startle, irritability, insomnia, poor concentration, hypervigilance | Sleep routine, relaxation, safe environment |

The **PCL-5** has 20 items scored 0-4 (total 0-80); a score of **about 33 or more** suggests probable PTSD and calls for assessment by a clinician. Other conditions are **adjustment disorder** (distress within 3 months of an ordinary stressor, such as job loss or migration failure, usually settling within 6 months) and **prolonged grief disorder** (intense yearning for more than 6-12 months after a loss).

```python
pcl = [3] * 8 + [2] * 8 + [1] * 4                # 20 PCL-5 items scored 0-4
pcl_total = sum(pcl)
cut = 33
probable = pcl_total >= cut
adult_n, teen_n = round(9200 * 0.03), round(5888 * 0.028)
print(f"PCL-5 total = {pcl_total} of 80 ({'probable PTSD, refer for assessment' if probable else 'below the cut-off'}; cut-off about {cut})")
print(f"NMHS 2020 current neurotic and stress-related disorders: adults {adult_n}, adolescents {teen_n}")
```

```text
PCL-5 total = 44 of 80 (probable PTSD, refer for assessment; cut-off about 33)
NMHS 2020 current neurotic and stress-related disorders: adults 276, adolescents 165
```

A PCL-5 total of **44** of 80 is above the cut-off of about 33, so this survivor needs assessment for PTSD.

### Trauma survivors: eight points of nursing care (psychological first aid)

1. **Ensure safety and basic needs.** Move the person to a safe, quiet place, give water, food, a blanket, a phone call to relatives and shelter. Basic needs come before talking. After disasters, use camps and health posts supported by the District Health Office.
2. **Look: check for urgent needs.** Look for injuries, danger and people in severe distress (confused, not speaking, wanting to hurt themselves). Protect children from being separated from their carers. Identify who needs a medical, social or mental health referral.
3. **Listen without pressure.** Stay near, offer presence, and listen if the person wants to talk. Do not force an account and do not do "debriefing" that makes people retell the event in detail. Say, "I am here. Take your time."
4. **Normalise reactions.** Explain that shaking, crying, poor sleep and nightmares are normal reactions to an abnormal event and usually ease in weeks. Do not say "be strong" or "it was God's will". Reassure honestly, without false promises.
5. **Link to help.** Connect people with family, information, services, the FCHV, the health post and psychosocial counsellors (for example TPO Nepal and CMC-Nepal). Help them to find missing relatives and to use relief supplies. Give clear information about where to return.
6. **Care for sleep and body.** Encourage regular meals, rest, light walking and routine, and avoid alcohol and sleeping tablets. For nightmares, teach a bedtime routine and the grounding technique. Treat injuries and pain quickly because pain keeps trauma alive.
7. **Treat disorder when it appears.** If symptoms last more than a month or are severe, refer for trauma-focused CBT or EMDR, and treat depression, panic and substance use. SSRIs (sertraline) may be ordered. Screen for suicide in every survivor.
8. **Protect vulnerable groups and care for yourself.** Pay special attention to children, women, older people, people with disability and survivors of gender-based violence. Handle disclosure with confidentiality and refer for legal and medical help. Rescue and health workers are also affected, so use supervision and rest.

## 4.4 Dissociative and conversion (functional) disorders

**Dissociative disorders** involve a break in the normal integration of memory, identity, perception and consciousness: **dissociative amnesia**, **dissociative fugue**, **depersonalisation or derealisation** and **possession or trance states**. **Conversion disorder (functional neurological symptom disorder)** is the loss or alteration of motor or sensory function (paralysis, blindness, mutism, **non-epileptic seizures**) that **cannot be explained by neurological disease** and arises, usually, after stress. The symptoms are **real and not faked**, and the person does not choose them. It is commoner in young women and in settings where distress cannot be voiced openly. In Nepal and South Asia, trance and possession states are often interpreted as the arrival of a god or spirit (*devi aaune*, *bhoot laagyo*) and families go first to a *dhami* or *jhankri*; **outbreaks of shared dissociative episodes among schoolgirls** have been reported. The nurse respects belief, rules out medical illness and offers a clear, kind explanation.

| Feature | **Non-epileptic (dissociative) seizure** | **Epileptic seizure** |
|---|---|---|
| Duration | Often long (more than 2 minutes), waxes and wanes | Usually 1-2 minutes |
| Eyes | Often **closed** and resist opening | Usually open |
| Movements | Thrashing, side-to-side head movement, out-of-phase | Rhythmic, synchronous jerks |
| Injury, tongue bite, incontinence | Uncommon | Common (lateral tongue bite) |
| After the episode | Quick recovery, may cry | Confusion and drowsiness |
| Trigger | Stress, emotion, being observed | Sleep loss, flicker, may be unprovoked |
| Test | Normal EEG during the event (video-EEG is definitive) | Epileptic discharge on EEG |

(These features help but do not replace a doctor's assessment: some people have both conditions.)

### Conversion disorder: eight points of nursing care

1. **Believe the symptom.** Say, "I can see your legs are weak and that this is frightening." Never say "you are pretending" or "there is nothing wrong". The distress and the disability are genuine, and respect keeps the patient in treatment.
2. **Exclude physical illness first.** Support the doctor's examination and tests (neurological examination, glucose, electrolytes, EEG, imaging as needed). Do not rush to label the symptom psychological. Do not repeat unnecessary tests, which reinforce the idea of hidden disease.
3. **Stay with the patient during an episode.** Protect from injury, place pillows, loosen clothes, keep the airway clear and speak calmly. Do not hold the person down or shout. Avoid giving too much attention to the attack, but never leave the patient alone.
4. **Give a clear, positive explanation.** Explain that the nervous system is working but its signals are disturbed by stress, like a computer with a software fault and not a broken machine. Say that recovery is expected. Avoid "it is all in your mind".
5. **Find the stress.** Ask privately about exams, marriage, abuse, conflict and fear, and listen. Many patients are unable to say these things directly. Involve the counsellor or social worker and protect from abuse if present.
6. **Promote function.** Encourage normal activity and self-care step by step, with physiotherapy for weakness, without rewarding the symptom with extra attention or exemptions. Praise recovery. Set small daily goals.
7. **Work with traditional belief.** Do not mock the family's explanation. Say, "We will treat the body and the stress, and you may continue your prayers." This keeps families at the hospital instead of leaving for the healer.
8. **Teach the family and plan follow-up.** Explain the condition, the need to avoid fuss during attacks and the follow-up date. Link to school or work and to counselling. Warn that relapse during stress is possible, and that help is available.

## 4.5 Benzodiazepines, personality disorders and childhood disorders

**Benzodiazepines** (diazepam, lorazepam, clonazepam, alprazolam) enhance the effect of **GABA** at the GABA-A receptor and so reduce anxiety, cause sleep, relax muscles and stop seizures (Plate 4.4). They act within minutes but cause **tolerance, dependence, memory impairment, falls and dangerous breathing depression with alcohol or opioids**. Rules: lowest dose, shortest time (2-4 weeks), no sudden stopping, **flumazenil** is the antidote for overdose. Use SSRIs and psychological therapy as the main treatments for anxiety disorders.

```photogrid label="4.4" cols="2" ratio="1.0" caption="Benzodiazepines. (a) Real diazepam tablets: tablets of the same drug can differ in shape, colour and marking between makers, so always read the pack label and strength. (b) How benzodiazepines work: they increase the effect of GABA at the GABA-A receptor, opening the chloride channel more often, which calms the neuron."
@ photo id="nur8/diaz" cap="Diazepam tablets"
fit 1.0
focus 0.5 0.5
mark 0.20 0.50 "1"
mark 0.52 0.27 "2"
key 1 (a) Engraved code and break line on the tablet: the dose is read from the pack
key 2 (a) A tablet of another make: colour and shape differ between makers
@ svg cap="GABA-A receptor and benzodiazepine action"
f = Fig(380, 300)
f.box(10, 10, 360, 50, "GABA binds the GABA-A receptor\nchloride channel opens, neuron calmer", fill=BLUE, stroke=NAVY, size=13, bold=True)
f.box(10, 80, 360, 50, "BENZODIAZEPINE binds a separate site\nchannel opens MORE OFTEN", fill=ROSE, stroke=RED, color=RED, size=13, bold=True)
f.box(10, 150, 360, 50, "EFFECTS: calm, sleep, muscle relaxation,\nanticonvulsant", fill=MINT, stroke=TEAL, size=13, bold=True)
f.box(10, 220, 360, 62, "RISKS: dependence, falls, memory loss,\nbreathing depression with alcohol or opioids\nANTIDOTE: flumazenil", fill=SAND, stroke=AMBER, size=12.5, bold=True)
```

| Group | Features | Nursing approach |
|---|---|---|
| **Cluster A** (odd): paranoid, schizoid, schizotypal | Suspicion, detachment, eccentric beliefs | Be honest and consistent; respect distance |
| **Cluster B** (dramatic): antisocial, **borderline**, histrionic, narcissistic | Impulsivity, unstable mood and relationships, self-harm, rule-breaking | Firm, kind limits, same rules for all staff; avoid splitting; take self-harm seriously; DBT skills |
| **Cluster C** (anxious): avoidant, dependent, obsessive-compulsive | Fear of criticism, clinging, perfectionism | Build confidence, encourage independence |
| **ADHD** | Inattention, hyperactivity and impulsivity in at least two settings, onset before 12 years | Routine, school plan, parent training; drugs by specialist |
| **Autism spectrum** | Difficulty with social communication, repetitive behaviour | Predictable routine, visual cues, early intervention |
| **Intellectual disability** | IQ below about 70 with poor adaptive skills from childhood | Simple instruction, skill training, protect from abuse; family and community support |

## Formula and fact sheet

- GAD-7: 0-4 minimal, 5-9 mild, 10-14 moderate, 15-21 severe. Y-BOCS: 0-7, 8-15, 16-23, 24-31, 32-40. PCL-5 cut-off about 33 of 80.
- Lorazepam 1 mg ≈ diazepam 10 mg; benzodiazepines for 2-4 weeks only; SSRIs take 2-4 weeks (8-12 for OCD).
- Slow breathing: 4 s in and 6 s out = 10 s a cycle = 6 breaths a minute; time spent on rituals = number × minutes.
- Panic peaks within 10 minutes and passes in 20-30; acute stress reaction 3 days to 1 month; PTSD more than 1 month.

## Chapter summary

- Anxiety is a graded response: Peplau's four levels guide the nurse; panic is a false alarm of the amygdala and is not dangerous.
- Anxiety disorders and OCD respond to CBT, exposure and SSRIs; benzodiazepines are short-term only.
- After trauma give psychological first aid (Look, Listen, Link); refer if symptoms last beyond a month.
- Conversion and dissociative symptoms are real and stress-related; rule out illness, explain kindly and work with traditional belief.

## Practice

```python
m1 = 2 + 2 + 3 + 2 + 1 + 1 + 2                   # MCQ1 GAD-7 total
m2 = 2 * 10                                      # MCQ2 lorazepam 2 mg in diazepam mg
m3 = 60 // (4 + 6)                               # MCQ3 breaths a minute at 4 s in and 6 s out
m4 = 25 * 4 * 7 / 60                             # MCQ4 hours a week of washing
cyc = 4 + 6
bpm = 60 // cyc
in5 = bpm * 5
fall = (28 - bpm) / 28 * 100
gad = 3 + 2 + 3 + 2 + 1 + 2 + 2
sert = 7 * 1 + 21 * 2                            # sertraline 25 mg: 1 tablet x 7 days, then 2 tablets x 21 days
att = 3 * 8
goal = att // 2
print(f"MCQ1 = {m1}; MCQ2 = {m2} mg; MCQ3 = {m3}; MCQ4 = {m4:.1f} h")
print(f"Ms Rai: cycle = {cyc} s; {bpm} breaths a minute; {in5} breaths in 5 min; fall from 28 = {fall:.0f}%; GAD-7 = {gad}; sertraline 25 mg tablets for 4 weeks = {sert}; attacks in 8 weeks = {att}; goal = {goal}")
```

```text
MCQ1 = 13; MCQ2 = 20 mg; MCQ3 = 6; MCQ4 = 11.7 h
Ms Rai: cycle = 10 s; 6 breaths a minute; 30 breaths in 5 min; fall from 28 = 79%; GAD-7 = 15; sertraline 25 mg tablets for 4 weeks = 49; attacks in 8 weeks = 24; goal = 12
```

**MCQs (with reasons)**

1. A patient's GAD-7 items are 2, 2, 3, 2, 1, 1, 2. The total and band are: (a) 13, moderate (b) 13, severe (c) 9, mild (d) 15, severe.
2. A patient takes lorazepam 2 mg a day. The approximate diazepam equivalent is: (a) 2 mg (b) 5 mg (c) 10 mg (d) 20 mg.
3. Breathing in for 4 seconds and out for 6 seconds gives how many breaths a minute: (a) 4 (b) 6 (c) 10 (d) 12.
4. A patient washes her hands 25 times a day for 4 minutes. The weekly time is about: (a) 2 hours (b) 7 hours (c) 11.7 hours (d) 28 hours.
5. After an earthquake, the first step for a frightened survivor is: (a) detailed trauma debriefing (b) a safe place, basic needs and psychological first aid (c) sleeping tablets for all (d) telling them to forget.

::: note Answers and rationales
**1. (a).** The sum is 13, in the 10-14 moderate band; 15 or more would be severe.
**2. (d).** Lorazepam 1 mg ≈ diazepam 10 mg, so 2 mg ≈ 20 mg; 2 mg would be a tenfold underestimate.
**3. (b).** One cycle is 10 seconds, so 60 ÷ 10 = 6 breaths a minute; 12 would be a 5-second cycle.
**4. (c).** 25 × 4 = 100 minutes a day, × 7 = 700 minutes = 11.7 hours.
**5. (b).** Safety, basic needs and psychological first aid come first; forced debriefing and routine sedatives can harm and delay recovery.
:::

**Short answer (3 marks): Differentiate obsession from compulsion.** An obsession is an unwanted, repeated thought, image or urge that causes anxiety (for example fear of contamination). A compulsion is a repeated act or mental ritual (washing, checking, counting) done to reduce the anxiety or to prevent a feared event. Compulsions give brief relief that keeps the cycle going; treatment is exposure with response prevention and an SSRI.

**Medium answer (5 marks): Describe psychological first aid after a disaster.** *Prepare:* learn about the event and services. *Look:* check safety, urgent needs and people with serious distress. *Listen:* approach calmly, offer comfort, listen without forcing talk, no debriefing. *Link:* connect people with family, food, shelter, information and services; refer those with severe distress, suicidal thoughts or symptoms beyond one month. Protect children, women and other vulnerable groups, respect culture, keep confidentiality and care for yourself.

**Long answer (10 marks): Ms Anita Rai, 20 years, 54 kg, a nursing student at Dharan, has had 3 sudden attacks a week for 8 weeks, each with pounding heart, breathlessness (RR 28), tingling, fear of dying and a peak at about 10 minutes. She now avoids the lecture hall and buses. ECG and thyroid tests are normal. Her GAD-7 items are 3, 2, 3, 2, 1, 2, 2. She is started on sertraline 25 mg for 7 days and then 50 mg daily. Calculate and write the nursing care plan.**

*Calculations.* GAD-7 = **15**, severe (15-21). With breathing 4 seconds in and 6 seconds out, one cycle is **10 s**, giving **6 breaths a minute** and **30 breaths in 5 minutes**; this is a fall of **79%** from a rate of 28. Sertraline needs 7 tablets (25 mg) in week one and 2 tablets daily for 21 days, **49 tablets** over 4 weeks. She has had **24 attacks** in 8 weeks; a goal of a **50% reduction** is **12 attacks** over the next 8 weeks.

*Care.* During an attack stay with her, use short calm sentences, a quiet place, slow breathing and grounding. Check vital signs and exclude physical causes. Teach that panic is a false alarm that cannot kill and passes in 20-30 minutes. Teach progressive relaxation, regular sleep and less tea and coffee. With the psychologist plan graded exposure (sit near the lecture hall, then enter for 5 minutes, then a short bus ride) and praise each step. Explain that sertraline takes 2-4 weeks, may cause early jitteriness and must not be stopped suddenly; avoid benzodiazepines. Review mood and suicide risk, since depression often follows. Give the family a simple explanation and inform the college counsellor.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "I felt I was dying." **O:** pulse 118, RR 28, tingling, GAD-7 15. | **Anxiety (severe/panic)** related to fear of bodily sensations, as evidenced by palpitations, overbreathing and terror. | **Anxiety self-control:** uses slow breathing to end an attack within 20 minutes; attacks fall from 3 to 1.5 a week in 8 weeks. | Stay with the patient (reduces fear); breathing 4 s in, 6 s out for 5 minutes (restores carbon dioxide); grounding 5-4-3-2-1 (shifts attention); explain false alarm (breaks the fear cycle). | Aborts attacks in 20 minutes; 12 or fewer attacks in 8 weeks. |
| **S:** "I cannot go into class or take the bus." **O:** avoids lecture hall. | **Ineffective coping** related to avoidance of feared situations. | **Coping:** attends one full lecture and travels by bus in 6 weeks. | Graded exposure list with the therapist (extinguishes fear); praise each step (reinforces); no rescue from every situation (avoid maintaining avoidance). | Attends lectures; uses the bus. |
| **S:** "I am not sleeping." **O:** sleeps 4 hours, drinks 5 cups of tea. | **Insomnia** related to anxiety and caffeine. | **Sleep:** sleeps 6 hours with fewer than 2 cups of tea. | Sleep hygiene and relaxation practice (lowers arousal); cut tea and coffee after noon (removes stimulant); sertraline as ordered, avoid hypnotics (no dependence). | Sleeps 6 hours; tea reduced. |
| **S:** "I will fail my course." **O:** low confidence, asks for reassurance. | **Deficient knowledge** about panic disorder and drug treatment. | **Knowledge:** explains panic, sertraline timing and relapse plan. | Teach with Figure 4.1 and the fear circuit (understanding); tell her sertraline works in 2-4 weeks and must not be stopped (adherence); give contact for the counsellor and health service (support). | States the plan; attends follow-up. |

