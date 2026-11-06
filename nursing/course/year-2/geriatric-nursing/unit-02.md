---
subject: Geriatric Nursing
grade: BSc Nursing Year 2
unit: 2
title: Falls, Mobility and Musculoskeletal Care in Older Adults
hours: 8
area: BSN 11 · Geriatric Nursing · Unit 2
---

Falls are the commonest accident of old age. About **one in three people over 65, and about half of those over 80, fall at least once a year** (WHO and CDC figures). In Nepal the causes are close to home: steep stairs and terraces, a slippery bathroom or *chaarpi* (toilet) at night, a dark path, loose *dhoti* and *sari* hems, open stoves at floor level and poorly lit hospital corridors. One fall in ten leads to serious injury, the **hip fracture** is the most feared, and a fall also takes confidence, so the person moves less and becomes weaker. If WHO's 28-35% applied to Nepal's 2.97 million older people, about **831,600 to 1,039,500** would fall each year; this is an estimate, not a count. All arithmetic in this unit is checked by program.

::: key What this unit gives you
- Real photographs of a walking frame, walking aids, a bathroom grab bar, an older man with a cane, a hip fracture fixation X-ray and a knee with osteoarthritis, plus SVG figures on fall causes and the screening pathway.
- Intrinsic and extrinsic causes of falls, the Morse Fall Scale, timed up-and-go, orthostatic hypotension, fall rate per 1,000 bed-days and hip fracture timing.
- Eight points each on fall prevention, hip fracture nursing and teaching about walking aids.
- Model answers and a NANDA-I care plan for an older man with a hip fracture after a night-time fall.
:::

## 2.1 Why older people fall

A **fall** is an event in which a person comes to rest on the ground or a lower level unintentionally. Falls arise from the **meeting of a weak person and a risky place**. **Intrinsic factors** are inside the person: age-related change (slow reflexes, weak legs, poor balance, poor vision and hearing), diseases (stroke, Parkinson disease, arthritis, diabetic neuropathy, dementia, anaemia, arrhythmia, infection), **orthostatic hypotension**, nocturia, foot problems and **drugs** (sedatives, antihypertensives, diuretics, antipsychotics, sulfonylureas). **Extrinsic factors** are outside: wet or uneven floors, poor light, no handrails, high beds, long clothes, unsuitable footwear and tripping over mats, pets and cables. The more risk factors a person has, the higher the chance of a fall, and a person with four or more falls risk is very likely to fall in the next year.

```svgfig label="2.1" caption="How a fall happens. Intrinsic and extrinsic risk factors combine, usually at night, on the way to the toilet. The consequences go far beyond the injury: fear of falling leads to less walking, weaker muscles and more falls. Prevention works on every box, not only on the floor."
f = Fig(760, 250)
f.box(10, 12, 230, 100, "INTRINSIC (the person)\nweak legs, poor balance\nvision and hearing loss\nstroke, Parkinson, dementia\nlow BP on standing, nocturia", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(10, 138, 230, 100, "EXTRINSIC (the place)\nwet floor, dark path, stairs\nloose mat, high bed\nlong hem, slippery footwear\nno grab bar or handrail", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(290, 78, 160, 90, "FALL\n(usually at night,\nto the toilet)", fill=ROSE, stroke=RED, color=RED, size=12, bold=True)
f.arrow([(240, 62), (290, 110)], color=NAVY, sw=2); f.arrow([(240, 188), (290, 138)], color=AMBER, sw=2)
f.box(500, 12, 250, 62, "INJURY\nhip fracture, head injury, bruise", fill=ROSE, stroke=RED, size=11, bold=True)
f.box(500, 94, 250, 62, "LONG LIE\ndehydration, pressure injury, pneumonia", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(500, 176, 250, 62, "FEAR OF FALLING\nless walking, weaker, more falls", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.arrow([(450, 110), (500, 43)], color=RED, sw=2); f.arrow([(450, 123), (500, 125)], color=RED, sw=2); f.arrow([(450, 140), (500, 207)], color=RED, sw=2)
```

**The Morse Fall Scale** is the most used ward tool. Score history of falling in the last 3 months (25), secondary diagnosis (15), walking aid (none or nurse assist 0, crutch, cane or walker 15, furniture 30), IV line or heparin lock (20), gait (normal 0, weak 10, impaired 20) and mental status (oriented 0, forgets limitations 15). **0-24 is no risk, 25-44 low risk and 45 or more high risk** (use the cut-off your hospital has adopted). The **timed up-and-go (TUG)** asks the patient to rise from a chair, walk 3 metres, turn, return and sit; **12 seconds or more** means fall risk. For **orthostatic hypotension**, the patient lies for 5 minutes, then BP is measured at 1 and 3 minutes after standing; a fall of **20 mmHg or more systolic or 10 mmHg or more diastolic** is positive. Hospitals count a **fall rate per 1,000 patient bed-days** to compare wards.

```python
morse = {"history of falling": 25, "secondary diagnosis": 15, "cane or walker": 15, "IV line": 0, "gait weak": 10, "mental status": 0}
m = sum(morse.values())
sys_l, dia_l, sys_s, dia_s = 140, 80, 108, 70       # BP lying and at 3 minutes standing (mmHg)
d_sys, d_dia = sys_l - sys_s, dia_l - dia_s
falls, bed_days = 6, 1500
rate = falls / bed_days * 1000
print(f"Morse score = {m} -> {'high risk (45 or more)' if m >= 45 else 'lower risk'}")
print(f"Orthostatic drop = {d_sys} / {d_dia} mmHg -> {'positive' if d_sys >= 20 or d_dia >= 10 else 'negative'}")
print(f"Fall rate = {falls} / {bed_days:,} x 1000 = {rate:.1f} per 1,000 bed-days")
print(f"Falls in Nepal if 28-35% of 2.97 million fall = {0.28 * 2.97e6:,.0f} to {0.35 * 2.97e6:,.0f}")
```

```text
Morse score = 65 -> high risk (45 or more)
Orthostatic drop = 32 / 10 mmHg -> positive
Fall rate = 6 / 1,500 x 1000 = 4.0 per 1,000 bed-days
Falls in Nepal if 28-35% of 2.97 million fall = 831,600 to 1,039,500
```

A patient with a history of falling (25), a secondary diagnosis (15), a walker (15) and weak gait (10) scores **65**, high risk. His BP falls from 140/80 lying to 108/70 standing, a drop of **32/10 mmHg**: orthostatic hypotension, so the nurse reviews fluids and drugs and teaches him to rise slowly. A ward with 6 falls in 1,500 bed-days has a rate of **4.0 per 1,000 bed-days**.

### Falls: eight points of prevention in hospital and at home

1. **Screen every older patient on admission.** Ask three questions: Have you fallen in the past year? Do you feel unsteady? Are you worried about falling? A yes to any one leads to a Morse score and TUG. Record the score and review it when the condition changes.
2. **Make the bed area safe.** Keep the bed low and locked, place the call bell, glasses, water and walking aid within reach, and put a light on. Avoid trailing cables. A bedside commode lets a night-time patient avoid the long walk.
3. **Plan toileting.** Offer the toilet every 2-3 hours and before sleep, and answer calls quickly. Most hospital falls happen when a patient goes alone to the toilet. Put a grab bar and a non-slip mat in the bathroom and a stool in the shower.
4. **Review medicines.** Look for sedatives, sleeping tablets, antipsychotics, diuretics and multiple BP drugs. Ask the doctor to stop or lower those that are not needed. Four or more drugs raise the risk.
5. **Correct vision, hearing and feet.** Clean glasses and hearing aids, treat cataract and wax, trim nails and give well-fitting closed shoes with a firm sole, not loose slippers.
6. **Strengthen and balance.** Chair stands, heel raises, tandem standing near a wall and **tai chi**-type exercise three times a week cut falls by about a quarter to a third. A physiotherapist can start the programme.
7. **Avoid physical restraints.** Rails, belts and ties cause injury and delirium and do not prevent falls; the **NNC Code of Ethics** and good practice favour the least restrictive way. Use a low bed, floor mats, a sitter or family member and close observation.
8. **After a fall, act in order.** Do not lift at once; check consciousness, breathing, pain and the neck, hip and wrist, then call help, record vital signs and neurological observations, tell the doctor and the family, write an incident report and find the cause. Teach how to get up or call for help.

```photogrid label="2.2" cols="4" ratio="1.0" caption="Mobility aids and a safer home. (a) A real patient standing at a walking frame beside a hospital bed. (b) A real set of aids: a straight cane, a walker-cane hybrid and a standard folding walker. (c) A real bathroom with a horizontal grab bar beside the toilet and a tall tub edge. (d) A real older man walking with a cane on a cobbled street, the surface is itself a fall hazard."
@ photo id="nur7/walker" cap="Walking frame in ward"
fit 1.0
focus 0.4 0.5
mark 0.36 0.88 "1"
mark 0.30 0.12 "2"
key 1 (a) Handgrips: set at wrist-crease height with the elbows slightly bent
key 2 (a) Rubber feet: all four on the floor before each step; check that they are not worn
@ photo id="nur7/cane" cap="Cane, hybrid and walker"
fit 1.0
focus 0.6 0.5
mark 0.32 0.84 "3"
mark 0.87 0.74 "4"
key 3 (b) Hybrid frame: gives more support than a single cane
key 4 (b) Walker frame: lift, move forward, step in; it is for support, not for lifting the patient
@ photo id="nur7/grab" cap="Bathroom grab bar"
fit 1.0
focus 0.8 0.5
mark 0.72 0.46 "5"
mark 0.25 0.12 "6"
key 5 (c) Grab bar: fixed into the wall at the toilet, strong enough for the whole body weight
key 6 (c) Tub edge: a high step; add a bath seat, non-slip mat and handheld shower
@ photo id="nur7/cane2" cap="Older man with cane"
fit 1.0
focus 0.5 0.6
mark 0.62 0.50 "7"
mark 0.50 0.12 "8"
key 7 (d) Cane: held in the hand opposite the weak leg, top at the wrist crease
key 8 (d) Uneven stone paving: a real outdoor hazard, like the stone steps of many Nepali towns
```

```svgfig label="2.3" caption="A falls screening and action pathway for older adults, adapted from the CDC STEADI and the WHO world guidelines for falls prevention (2022). Screen, test the gait, then act on the risk level. A fall in the last year, unsteadiness or fear of falling is enough to start."
f = Fig(760, 250)
f.box(8, 90, 120, 70, "OLDER ADULT\n65+ or one fall\nin the last year", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(160, 90, 130, 70, "SCREEN\n3 questions\n(fall, unsteady,\nworried)", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(322, 90, 130, 70, "TEST\nTUG 12 s or more\n30-s chair stand\n4-m gait speed", fill=SAND, stroke=AMBER, size=11, bold=True)
f.arrow([(128, 125), (160, 125)]); f.arrow([(290, 125), (322, 125)])
f.box(500, 10, 250, 62, "LOW RISK\nexercise, vitamin D, safe home advice,\nyearly review", fill=MINT, stroke=TEAL, size=11, bold=True)
f.box(500, 94, 250, 62, "MODERATE RISK\nstrength and balance programme,\nmedicine and foot review", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(500, 178, 250, 66, "HIGH RISK\nmultifactorial assessment: drugs, lying and\nstanding BP, vision, feet, home, cognition", fill=ROSE, stroke=RED, size=11, bold=True)
f.arrow([(452, 110), (500, 41)], color=TEAL, sw=2); f.arrow([(452, 125), (500, 125)], color=AMBER, sw=2); f.arrow([(452, 140), (500, 211)], color=RED, sw=2)
```

## 2.2 Hip fracture, osteoarthritis and immobility

A **hip fracture** is a fracture of the upper femur. **Intracapsular (femoral neck)** fractures cut the blood supply of the head and are treated by **hemiarthroplasty or total hip replacement**; **extracapsular (intertrochanteric)** fractures are fixed with a **dynamic hip screw (DHS) or intramedullary nail** (Plate 2.4a). The leg is **shortened and externally rotated**, with groin pain and inability to bear weight. Surgery within **24-48 hours** lowers pain, complications and death; delay for investigation is justified only for urgent medical problems. The one-year death rate after hip fracture is high, so these patients need **orthogeriatric care**: surgeon, physician, anaesthetist, nurse, physiotherapist, nutritionist and social worker.

```python
from datetime import datetime
wt = 60
para = 15 * wt                                   # paracetamol 15 mg/kg per dose
prot = 1.5 * wt                                  # protein for fracture healing, 1.5 g/kg
kcal = 30 * wt
inj, op = datetime(2025, 3, 3, 20, 0), datetime(2025, 3, 5, 8, 0)
hrs = (op - inj).total_seconds() / 3600
print(f"Paracetamol 15 mg/kg x {wt} kg = {para} mg per dose (not above 3 g a day in the frail)")
print(f"Protein 1.5 g/kg x {wt} kg = {prot:.0f} g a day; energy 30 kcal/kg = {kcal:,} kcal")
print(f"Injury Monday 20:00 to surgery Wednesday 08:00 = {hrs:.0f} hours (target 24-48 h)")
```

```text
Paracetamol 15 mg/kg x 60 kg = 900 mg per dose (not above 3 g a day in the frail)
Protein 1.5 g/kg x 60 kg = 90 g a day; energy 30 kcal/kg = 1,800 kcal
Injury Monday 20:00 to surgery Wednesday 08:00 = 36 hours (target 24-48 h)
```

For a 60 kg patient the paracetamol dose is **900 mg** (about 1 g, not more than 3 g a day in a frail older person), protein need is **90 g** and energy **1,800 kcal** a day. A patient injured on Monday at 20:00 and operated on Wednesday at 08:00 waits **36 hours**, within the 24-48 hour target.

```photogrid label="2.4" cols="2" ratio="1.0" caption="The bones of old age. (a) A real pelvis X-ray of an 80-year-old woman after dynamic hip screw fixation of a femoral neck fracture on the right side (the film is marked R). (b) A real knee X-ray with osteoarthritis: the joint space is narrowed and the bone edges form spurs (osteophytes)."
@ photo id="nur7/dhs" cap="Dynamic hip screw, right hip"
fit 1.0
focus 0.5 0.5
mark 0.37 0.68 "1"
mark 0.24 0.42 "2"
key 1 (a) Lag screw: runs from the side plate up into the femoral head and slides to compress the fracture
key 2 (a) Side plate and cortical screws: fixed to the femoral shaft; mobilise with weight bearing as the surgeon allows
@ photo id="nur7/oa" cap="Knee osteoarthritis"
fit 1.0
focus 0.5 0.45
mark 0.50 0.45 "3"
mark 0.82 0.50 "4"
key 3 (b) Narrow joint space: cartilage has worn away, bone rubs on bone
key 4 (b) Osteophyte: a bony spur at the joint edge; causes stiffness and pain on movement
```

### Hip fracture: eight points of nursing responsibility

1. **Control pain from the first minute.** Give paracetamol regularly and a small dose of opioid or a nerve block as ordered, and avoid NSAIDs in kidney disease. Pain causes delirium, so assess it with a numbers or faces scale and, in dementia, with a behaviour scale such as PAINAD.
2. **Position and move with care.** Support the leg on pillows, log-roll with a pillow between the knees and never lift by the injured leg. After a hemiarthroplasty, follow the surgeon's **hip precautions**: do not bend the hip beyond 90 degrees, cross the legs or turn the leg inward.
3. **Prepare for early surgery.** Keep the patient nil by mouth, correct dehydration with IV fluids, take blood for Hb, group and cross-match, ECG and renal tests and obtain consent from the patient or the legally authorised family member. Delay for avoidable reasons is a nursing quality failure.
4. **Prevent clots.** Give enoxaparin or heparin as ordered, use compression stockings, teach ankle pumps every hour and start walking early. Report a swollen painful calf or sudden breathlessness, which can mean pulmonary embolism.
5. **Prevent delirium.** Give oxygen if SpO2 is low, treat pain, keep glasses and hearing aids in place, keep a clock and a calendar, allow sleep and avoid sedatives and a urinary catheter if possible. Delirium occurs in up to half of hip fracture patients.
6. **Protect the skin.** A patient lying on a hard trolley for hours can develop a pressure injury. Use a pressure-relieving mattress, turn 2-hourly as allowed and keep heels free. Inspect the heels and sacrum at every turn.
7. **Mobilise and give nutrition.** Help the patient stand on day 1 with the physiotherapist, increase walking daily and teach the use of a frame. Give protein 1.5 g/kg, extra calcium and vitamin D and fluids. A frail eater needs supplements.
8. **Prevent the next fracture.** Treat osteoporosis (calcium, vitamin D, bisphosphonate as ordered), review the drugs, fit a home safety plan and arrange follow-up with the orthopaedic clinic. A hip fracture is a sign that another one will follow unless the cause is treated.

### Walking aids and osteoarthritis: eight points of teaching

1. **Fit the aid.** The handle of a cane or walker should be at the wrist crease when the arm hangs, with the elbow bent about 20-30 degrees. A wrongly fitted aid causes shoulder pain and falls.
2. **Hold the cane on the strong side.** Hold the cane in the hand opposite the weak leg; move the cane and the weak leg together, then the strong leg.
3. **Use the walker properly.** Lift or slide it forward, step into it with the weak leg first and then the strong leg. Do not pull on it to stand up from a chair.
4. **Stairs: up with the good, down with the bad.** Step up with the good leg first and down with the weak leg first, holding the rail; the cane follows the weak leg.
5. **Check the tips.** Replace worn rubber tips and keep the aid dry. A smooth tip on a wet floor can slip.
6. **Manage osteoarthritis pain.** Use heat before activity, cold after a flare, paracetamol and a topical NSAID gel first; oral NSAIDs only briefly and with food, and never in kidney disease or ulcer. Lose weight, because each kilogram lost takes about four kilograms of load off the knee.
7. **Exercise the joint.** Quadriceps strengthening, cycling, swimming and walking on level ground reduce pain. Stairs and squatting on the floor for prayer and cooking may need a stool or a raised seat.
8. **Know when to ask for surgery.** Pain at night and at rest, a failing aid and loss of independence suggest referral for joint replacement, which is performed in Kathmandu, Pokhara and provincial centres.

## Formula and fact sheet

- Morse Fall Scale: history 25, secondary diagnosis 15, aid 0/15/30, IV 20, gait 0/10/20, mental 0/15; 45 or more = high risk.
- TUG 12 s or more = fall risk; orthostatic hypotension = fall of 20 mmHg systolic or 10 mmHg diastolic within 3 min of standing; fall rate = falls ÷ bed-days × 1,000.
- Hip fracture: shortened, externally rotated leg; surgery within 24-48 h; paracetamol 15 mg/kg; protein 1.5 g/kg; energy 30 kcal/kg.
- Cane at wrist crease; hold on the strong side; stairs up with the good, down with the bad.

## Chapter summary

- Falls come from weak people in risky places; screen, test gait, review drugs and fix the home.
- The Morse score, TUG and lying-standing BP identify risk; physical restraints are avoided.
- Hip fracture care is orthogeriatric: early surgery, pain control, clot and delirium prevention, early walking and bone treatment.
- Good teaching about aids, osteoarthritis and exercise keeps independence.

## Practice

```python
m1 = 25 + 15 + 20 + 20                          # Morse: history, secondary dx, IV, impaired gait
m2 = 150 - 124                                  # systolic drop lying to standing
m3 = 15 * 40                                    # paracetamol for 40 kg
wt = 55                                         # Mr Dhan Bahadur
c_sys, c_dia = 150 - 118, 84 - 70
c_morse = 25 + 15 + 20 + 20 + 15
c_para, c_prot, c_kcal = 15 * wt, 1.5 * wt, 30 * wt
c_hr = 32                                       # Tuesday 02:00 to Wednesday 10:00
print(f"MCQ1 Morse = {m1}; MCQ2 systolic drop = {m2} mmHg; MCQ3 paracetamol = {m3} mg")
print(f"Mr Dhan: drop = {c_sys}/{c_dia} mmHg; Morse = {c_morse}; paracetamol = {c_para} mg")
print(f"Mr Dhan: protein = {c_prot:.1f} g; energy = {c_kcal:,} kcal; time to surgery = {c_hr} h")
```

```text
MCQ1 Morse = 80; MCQ2 systolic drop = 26 mmHg; MCQ3 paracetamol = 600 mg
Mr Dhan: drop = 32/14 mmHg; Morse = 95; paracetamol = 825 mg
Mr Dhan: protein = 82.5 g; energy = 1,650 kcal; time to surgery = 32 h
```

**MCQs (with reasons)**

1. A patient has a history of falling (25), a secondary diagnosis (15), an IV line (20) and impaired gait (20). His Morse score is: (a) 25 (b) 45 (c) 80 (d) 100.
2. A patient's BP is 150/80 lying and 124/76 standing at 3 minutes. The systolic drop is: (a) 4 mmHg, normal (b) 26 mmHg, orthostatic hypotension (c) 26 mmHg, normal (d) 74 mmHg, normal.
3. Paracetamol 15 mg/kg is ordered for a 40 kg patient. The dose is: (a) 60 mg (b) 375 mg (c) 600 mg (d) 1,000 mg.
4. You find an older patient on the ward floor. The first action is: (a) lift to bed at once (b) assess consciousness, breathing and injury before moving (c) give oral fluids (d) tie the patient to the bed.
5. The typical leg position in a displaced femoral neck fracture is: (a) lengthened and internally rotated (b) shortened and externally rotated (c) normal length (d) flexed and abducted.

::: note Answers and rationales
**1. (c).** 25 + 15 + 20 + 20 = 80, high risk (45 or more); 45 is only the cut-off and 100 adds an item not present.
**2. (b).** 150 − 124 = 26 mmHg, which is 20 or more; 4 mmHg is the diastolic difference misread, and options (c) and (d) are wrong arithmetic or interpretation.
**3. (c).** 15 × 40 = 600 mg; 60 mg is a tenfold error and 1,000 mg is the adult fixed dose, which would overdose a small patient.
**4. (b).** Moving a patient with a neck, hip or head injury can worsen it; assess first, then lift with help. Restraint is unsafe and unethical.
**5. (b).** The unopposed muscles pull the distal fragment up and rotate it outward, so the leg looks shorter and turned out.
:::

**Short answer (3 marks): Orthostatic hypotension.** It is a fall of 20 mmHg or more in systolic (or 10 mmHg in diastolic) BP within 3 minutes of standing, from slow baroreceptor response, dehydration, autonomic neuropathy or drugs (diuretics, antihypertensives, tamsulosin). It causes dizziness, falls and syncope. The nurse measures BP lying and standing, corrects dehydration, reviews drugs and teaches to rise slowly in stages.

**Medium answer (5 marks): Explain the prevention of falls in older people (Figures 2.1 and 2.3).** *Screen:* ask three questions on admission and do a Morse score and TUG. *Person:* review drugs (sedatives, diuretics, antihypertensives), correct vision, hearing and foot problems, treat orthostatic hypotension, manage nocturia and cognitive impairment. *Place:* a low locked bed, light, call bell and walking aid within reach, non-slip floor, grab bars, a clear path to the toilet and suitable footwear. *Exercise:* strength and balance training, tai chi. *Do not restrain.* *After a fall:* assess, record, report and find the cause.

**Long answer (10 marks): Mr Dhan Bahadur Thapa, 82 years, 55 kg, a retired farmer from Pokhara, fell in the dark going to the toilet at 02:00 on Tuesday. He has a right femoral neck fracture and is admitted to an orthopaedic ward; he takes amlodipine, a nightly diazepam tablet and has nocturia. Lying BP is 150/84 and standing BP 118/70 mmHg. He is operated on at 10:00 on Wednesday (hemiarthroplasty). Calculate and write the nursing care plan.**

*Calculations.* His orthostatic drop is **32/14 mmHg**, positive, so amlodipine and diazepam are reviewed. His Morse score on admission is 25 + 15 + 20 + 20 + 15 = **95** (very high). The wait for surgery is **32 hours**, within the 48-hour target. Paracetamol 15 mg/kg is **825 mg**, protein 1.5 g/kg is **82.5 g** and energy 30 kcal/kg is **1,650 kcal** a day.

*Care.* Before surgery give analgesia and fluids, keep him warm and nil by mouth, apply a pressure-relieving mattress and take blood for Hb and cross-match. After surgery follow the hip precautions (no bending beyond 90 degrees, no crossing the legs, pillow between the knees), give enoxaparin as ordered, check the wound and leg length, circulation and sensation, and get him on his feet on day 1 with a frame. Prevent delirium with glasses, a clock, family at the bedside, sleep and treatment of pain. Review the diazepam (stop gradually) and the BP drug, and teach him to sit for a minute before standing. Before discharge, arrange a toilet next to the bed, a night light, a grab bar, non-slip footwear and a stick, start calcium, vitamin D and an osteoporosis drug as ordered, and link him with the ward FCHV and the health post. Teach the family not to use bed rails or ties.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "My hip is on fire." **O:** pain 8/10, leg shortened and turned out. | **Acute pain** related to fracture and surgery, as evidenced by pain score 8/10 and guarding. | **Pain level:** pain 3 or less within 1 hour of analgesia; can turn in bed. | Scheduled paracetamol and opioid or nerve block as ordered (steady pain relief); pillows and log-roll (less movement of fracture); PAINAD if confused (detects pain in dementia). | Pain 3/10 at rest; sleeps. |
| **S:** "I cannot stand." **O:** non-weight bearing; post-hemiarthroplasty. | **Impaired physical mobility** related to hip fracture and surgery. | **Mobility:** stands on day 1 and walks 10 metres with a frame by day 4. | Physiotherapy from day 1 (prevents muscle loss); hip precautions (prevent dislocation); ankle pumps and enoxaparin (prevent clots); protein 82.5 g (heals tissue). | Walks 10 m with a frame on day 4. |
| **S:** "I got up in the dark." **O:** Morse 95, orthostatic drop 32/14 mmHg, diazepam. | **Risk for falls** related to orthostatic hypotension, sedative use, nocturia and unfamiliar ward. | **Fall prevention behaviour:** no falls in hospital and none in the first 3 months at home. | Low locked bed, night light, commode, call bell (reduce night-time risk); drug review (removes the cause); teach slow rising (counters low BP); no restraints (avoid delirium and injury). | No falls; drop under 20 mmHg. |
| **S:** "Will the wound smell?" **O:** surgical wound, age 82, 55 kg. | **Risk for infection** related to surgical wound and malnutrition risk. | **Wound healing:** wound clean and dry with no fever for 14 days. | Aseptic dressing and hand hygiene (blocks bacteria); antibiotic prophylaxis on time (protects the implant); temperature and wound checks (early detection); protein and fluids (healing). | Afebrile; wound dry; sutures removed day 14. |
