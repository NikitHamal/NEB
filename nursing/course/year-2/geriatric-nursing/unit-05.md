---
subject: Geriatric Nursing
grade: BSc Nursing Year 2
unit: 5
title: Pressure Injury, Incontinence, Elder Abuse, Palliative Care and Senior Citizen Services in Nepal
hours: 10
area: BSN 11 · Geriatric Nursing · Unit 5
---

The last unit of geriatric nursing deals with what happens when an older person becomes bedbound, incontinent, dependent on others or close to death. These are the problems that decide whether old age is lived with dignity: **a pressure injury that begins on the heel or sacrum in a single night, a wet bed that no one changes, a pension collected by someone else, a grandmother labelled a *boksi* (witch), a death at home without pain relief**. WHO estimates that about **1 in 6 people aged 60 and above (15.7%)** experience abuse in the community each year; if this global figure applied to Nepal's 2.97 million older people, about **466,290** would be affected (an estimate, not a count). The **Senior Citizens Act 2063 (2006)**, the Senior Citizens Regulations 2065 (2008), the National Policy on Senior Citizens 2058 (2002) and the old-age allowance (started in 1995) give the legal frame. All arithmetic in this unit is checked by program.

::: key What this unit gives you
- Real photographs of a pressure injury, an absorbent pad for incontinence and a smiling older Nepali woman, plus four SVG figures: pressure injury stages, types of incontinence and the response to elder abuse.
- The Braden Scale, NPIAP staging, nutrition for healing, wound area change, nocturnal polyuria index, post-void residual, the pad test, opioid breakthrough dosing and the Nepal Senior Citizens Act.
- Eight points each on pressure injury prevention, incontinence care, elder abuse response and palliative care.
- Model answers and a NANDA-I care plan for a bedridden woman with a sacral pressure injury, incontinence and signs of neglect.
:::

## 5.1 Pressure injury

A **pressure injury** is localised damage to the skin and underlying tissue over a bony prominence (sacrum, heels, hips, elbows, back of the head) caused by **pressure, or pressure with shear**. The older person is at risk because the skin is thin and dry, fat padding is lost, sensation, mobility and nutrition fall and incontinence keeps the skin wet. Shear happens when the head of the bed is raised above 30 degrees and the person slides down. Damage can begin within 2 hours, and deep tissue injury shows only days later. The **NPIAP stages** (Figure 5.1) are: **Stage 1** non-blanchable redness with intact skin; **Stage 2** partial-thickness loss with a shallow open ulcer or blister; **Stage 3** full-thickness skin loss with visible fat; **Stage 4** full-thickness loss with exposed muscle, tendon or bone. **Unstageable** (covered by slough or eschar) and **deep tissue pressure injury** (persistent deep red, maroon or purple discolouration) are also reported.

```svgfig label="5.1" caption="The four stages of pressure injury shown on a cross-section of skin, fat, muscle and bone. The depth of damage increases from the surface (Stage 1, intact skin that does not blanch) to bone (Stage 4). Unstageable and deep tissue injury are reported separately. Never massage a red area over a bony point."
f = Fig(760, 250)
layers = [("Epidermis", 60, 12, "#fde68a"), ("Dermis", 72, 30, "#fcd9b6"), ("Fat", 102, 40, "#fef3c7"), ("Muscle", 142, 40, "#fecaca"), ("Bone", 182, 14, "#e2e8f0")]
for nm, y, h, col in layers:
    f.text(88, y + h / 2, nm, size=10, anchor="end", vmid=True, bold=True)
stages = [("STAGE 1", "non-blanchable\nredness, skin intact", 72), ("STAGE 2", "shallow ulcer or\nblister, dermis", 100), ("STAGE 3", "full-thickness loss,\nfat visible", 140), ("STAGE 4", "muscle, tendon or\nbone exposed", 192)]
for i, (h, t, dep) in enumerate(stages):
    x = 100 + i * 165
    for nm, y, hh, col in layers:
        f.box(x, y, 150, hh, "", fill=("#fca5a5" if (i == 0 and y == 60) else col), stroke="#94a3b8", r=0, sw=0.8)
    if i > 0:
        f.poly([(x + 45, 60), (x + 105, 60), (x + 75, dep)], fill="#b91c1c", stroke=RED, sw=1.2)
    f.box(x, 14, 150, 30, h, fill=RED if i > 1 else AMBER, stroke=RED if i > 1 else AMBER, color="#ffffff", size=11, bold=True)
    f.text(x + 75, 214, t, size=10.5, bold=True, color=SLATE)
```

The **Braden Scale** scores six items: sensory perception (1-4), moisture (1-4), activity (1-4), mobility (1-4), nutrition (1-4) and friction and shear (1-3). The total is 6-23; **18 or less is at risk**: 15-18 mild, 13-14 moderate, 10-12 high and 9 or below very high risk. Healing needs **energy 30-35 kcal/kg, protein 1.25-1.5 g/kg and about 1 mL of fluid per kcal**, and healing is judged by the fall in wound area (length × width).

```python
braden = {"sensory perception": 3, "moisture": 2, "activity": 1, "mobility": 2, "nutrition": 2, "friction and shear": 1}
b = sum(braden.values())
turns = 24 // 2                                    # two-hourly repositioning
wt = 60
plo, phi = 1.25 * wt, 1.5 * wt
klo, khi = 30 * wt, 35 * wt
a0, a1 = 5 * 4, 4 * 3                              # wound area (cm2) at week 0 and week 4
red = (a0 - a1) / a0 * 100
print(f"Braden = {b} -> {'high risk (10-12)' if 10 <= b <= 12 else 'other band'}")
print(f"Repositioning every 2 h = {turns} turns in 24 h")
print(f"Protein {plo:.0f}-{phi:.0f} g; energy {klo:,}-{khi:,} kcal for {wt} kg")
print(f"Wound area {a0} cm2 -> {a1} cm2 = {red:.1f}% reduction in 4 weeks")
```

```text
Braden = 11 -> high risk (10-12)
Repositioning every 2 h = 12 turns in 24 h
Protein 75-90 g; energy 1,800-2,100 kcal for 60 kg
Wound area 20 cm2 -> 12 cm2 = 40.0% reduction in 4 weeks
```

A patient with Braden items of 3, 2, 1, 2, 2 and 1 scores **11**, **high risk**, and needs a pressure-redistributing mattress and **12 turns in 24 hours**. For a 60 kg patient, protein is **75-90 g** and energy **1,800-2,100 kcal** a day. A wound that shrinks from 5 × 4 = **20 cm²** to 4 × 3 = **12 cm²** has a **40.0%** reduction in 4 weeks; a healing wound should be smaller by about 30-40% in this time, otherwise the plan is reviewed.

### Pressure injury: eight points of prevention and care

1. **Assess risk at admission and daily.** Use the Braden Scale and examine the skin of the sacrum, heels, hips, elbows, ears and the back of the head, especially under devices. Note colour, warmth, firmness and pain. Press the red area: if it does not blanch, it is a Stage 1 injury.
2. **Reposition on a schedule.** Turn at least every 2 hours (the interval may be longer on a good mattress), use the 30-degree side-lying position and pillows between the knees and ankles. Keep the head of the bed at 30 degrees or lower unless eating, to reduce shear. A turning chart makes everyone responsible.
3. **Use the right surface.** Provide a pressure-redistributing foam or alternating-pressure mattress, a cushion in the chair and **float the heels** on a pillow under the calves. Do not use ring cushions or sheepskin lumps. In Nepal's rural homes a thick foam, folded blankets and regular turning are the low-cost options.
4. **Keep the skin clean and dry.** Clean quickly after each episode of incontinence with a pH-balanced cleanser, pat dry, apply a barrier cream and use soft absorbent pads, not plastic sheets. Moisturise dry skin. Never massage red areas or bony prominences.
5. **Reduce friction and shear.** Lift with a draw sheet and do not drag the patient across the bed, keep the sheets smooth and use a sliding sheet. Heel and elbow dressings can protect the skin of a restless patient.
6. **Feed for healing.** Give 30-35 kcal/kg, protein 1.25-1.5 g/kg (dal, eggs, milk, fish, soya, meat), fluids and vitamins and minerals if deficient. Weigh weekly and add supplements for a poor eater. Treat anaemia.
7. **Treat the wound with moist healing.** Clean with saline, remove dead tissue as ordered, keep the bed moist with a suitable dressing (hydrocolloid, foam or alginate) and protect with aseptic technique. Measure and record the size, depth, exudate, odour and surrounding skin weekly. Report spreading redness, pus, fever or odour.
8. **Teach the family.** Show how to turn, how to lift without dragging, how to check the skin twice a day and how to feed. Explain that the injury is preventable and is not caused by bad care alone. Link the household with the health post or a home-care nurse, since most injuries occur at home after discharge.

```photogrid label="5.2" cols="3" ratio="1.0" caption="Skin, continence and dignity. (a) A real pressure injury over a bony area: a red-purple, non-blanchable patch with a small area of broken skin; stage and depth need bedside assessment. (b) A real absorbent pad of the kind used for urinary incontinence. (c) A real older Nepali woman smiling in traditional dress: the aim of all geriatric care is comfort and dignity."
@ photo id="nur7/decub" cap="Pressure injury"
fit 1.0
focus 0.5 0.5
mark 0.42 0.55 "1"
mark 0.80 0.50 "2"
key 1 (a) Non-blanchable red-purple area over a bony point: stop pressure on it at once
key 2 (a) Surrounding skin: check warmth, firmness and moisture, and compare with the other side
@ photo id="nur7/pad" cap="Incontinence pad"
fit 1.0
focus 0.5 0.5
mark 0.45 0.45 "3"
mark 0.42 0.72 "4"
key 3 (b) Absorbent core: choose the size by the volume lost; change as soon as it is wet
key 4 (b) Soft top layer: keeps urine away from the skin and prevents dermatitis
@ photo id="nur7/nep3" cap="Older Nepali woman"
fit 1.0
focus 1.0 0.5
mark 0.61 0.66 "5"
mark 0.29 0.80 "6"
key 5 (c) Face: dignity and a smile are measures of good care
key 6 (c) Flower and traditional dress: respect religion, culture and personal choice
```

## 5.2 Urinary incontinence

**Urinary incontinence** is the involuntary loss of urine. It is **common but never normal**: it affects about one in three older women and many men, it is under-reported from embarrassment, and it leads to skin breakdown, urinary infection, falls on the way to the toilet, isolation and admission to care. **Types** (Figure 5.3): **stress** (leaks on cough, sneeze or lifting; weak pelvic floor after childbirth, and **uterine prolapse** is common among Nepali women), **urge** (sudden urgency; overactive bladder, infection, stroke), **overflow** (a full bladder dribbles; enlarged prostate, diabetic neuropathy, constipation and drugs), **functional** (a normal bladder but the person cannot reach or use the toilet because of dementia, poor mobility or a high bed) and **mixed**. Assessment includes a **3-day bladder diary**, urine dipstick, a **post-void residual (PVR)** by bladder scan or catheter (**100 mL or more** suggests retention), a drug review (diuretics, sedatives, anticholinergics) and a check for faecal impaction.

```svgfig label="5.3" caption="Five types of urinary incontinence with their commonest cause and the first nursing action. Treat reversible causes first: infection, constipation, drugs, delirium, poor mobility and a toilet that is far or dark."
f = Fig(760, 240)
t = [("STRESS", "leak on cough, lift;\nweak pelvic floor,\nprolapse", "pelvic floor\nexercise", BLUE, NAVY), ("URGE", "sudden urgency;\noveractive bladder,\ninfection, stroke", "bladder training,\ncut caffeine", SAND, AMBER), ("OVERFLOW", "dribbling; BPH,\nneuropathy, stool,\ndrugs", "measure PVR,\nrelieve outlet", ROSE, RED),
     ("FUNCTIONAL", "normal bladder; cannot\nreach toilet\n(dementia, mobility)", "prompted voiding,\ncommode", MINT, TEAL), ("MIXED", "stress + urge,\ncommon in older\nwomen", "treat the\nworse part first", BLUE, NAVY)]
for i, (h, c, a, fl, st) in enumerate(t):
    x = 8 + i * 150
    f.box(x, 14, 142, 30, h, fill=st, stroke=st, color="#ffffff", size=11, bold=True)
    f.box(x, 48, 142, 84, c, fill=fl, stroke=st, size=10.5, bold=True)
    f.arrow([(x + 71, 134), (x + 71, 152)], color=SLATE, sw=1.8)
    f.box(x, 154, 142, 48, a, fill="#ffffff", stroke=st, size=10.5, bold=True)
f.text(380, 224, "First: exclude infection, constipation, drugs, delirium and mobility problems", size=11, bold=True)
```

```python
day_ml, night_ml = 1800, 700
npi = night_ml / day_ml * 100                       # nocturnal polyuria index, above 33% is nocturnal polyuria
pvr = 180
wet, dry = 112, 25                                  # one-hour pad test: weights in grams
leak = wet - dry
dose, doses = 5, 6                                  # oral morphine 5 mg every 4 h for 24 h
daily = dose * doses
bt = daily / 6                                      # breakthrough dose is one-sixth of the daily dose
print(f"Nocturnal polyuria index = {night_ml} / {day_ml} x 100 = {npi:.1f}% (above 33%)")
print(f"Post-void residual {pvr} mL ({'retention suspected' if pvr >= 100 else 'low'}; 100 mL or more)")
print(f"One-hour pad test: {wet} - {dry} = {leak} g (over 50 g is severe)")
print(f"Oral morphine {dose} mg x {doses} = {daily} mg a day; breakthrough dose = {daily} / 6 = {bt:.0f} mg")
```

```text
Nocturnal polyuria index = 700 / 1800 x 100 = 38.9% (above 33%)
Post-void residual 180 mL (retention suspected; 100 mL or more)
One-hour pad test: 112 - 25 = 87 g (over 50 g is severe)
Oral morphine 5 mg x 6 = 30 mg a day; breakthrough dose = 30 / 6 = 5 mg
```

A patient who passes 1,800 mL in 24 hours, of which 700 mL at night, has a **nocturnal polyuria index of 38.9%** (above 33%), so evening fluids, diuretic timing, leg swelling and sleep apnoea are reviewed. A PVR of **180 mL** suggests retention. A one-hour pad test with a pad that rises from 25 g to 112 g shows a leak of **87 g**, severe incontinence.

### Incontinence: eight points of nursing care

1. **Assess and record.** Keep a 3-day diary of fluid intake, voids, leaks and urgency. Do a dipstick, check the PVR and ask about prolapse, prostate symptoms, constipation and drugs. The diary shows the pattern and the type.
2. **Treat reversible causes.** Treat urinary infection, constipation, delirium and drug effects (diuretics, sedatives, anticholinergics, alpha-blockers). Many patients become dry after these steps alone.
3. **Pelvic floor exercise.** Teach women (and men after prostate surgery) to squeeze the muscles used to stop urine for 6-8 seconds, 8-12 repeats, three times a day for at least 3 months. The squeeze should not involve the buttocks or breath-holding. Midwives and physiotherapists can assist.
4. **Bladder training and prompted voiding.** Lengthen the interval between voids by 15 minutes each week and use urge suppression (stand still, squeeze, relax, breathe). In dementia, offer the toilet every 2-3 hours and praise success.
5. **Adjust fluids and diet.** Drink 1.5-2 L in the day, less in the evening, cut tea, coffee and alcohol, treat constipation with fibre and fluids and reduce weight. Do not restrict fluid severely, since concentrated urine irritates the bladder.
6. **Make the toilet easy.** Provide a light, a short clear path, a raised seat, rails, a commode near the bed and clothes with simple fastenings. Respond to calls promptly. Functional incontinence is mostly an environmental problem.
7. **Protect the skin and use aids wisely.** Wash after leakage, apply barrier cream, use absorbent pads or pants sized to the volume and change them promptly. Avoid an indwelling catheter for convenience: it causes **CAUTI** in a few days. Use it only for retention, pressure injury healing or comfort at the end of life.
8. **Respect dignity and refer.** Speak in private, offer a same-sex nurse where wished, and explain that incontinence is treatable. Refer for prolapse repair, a ring pessary, prostate treatment or a urology opinion, and be careful with oxybutynin, which is on the Beers list.

## 5.3 Elder abuse and the Senior Citizens Act

**Elder abuse** is a single or repeated act, or lack of action, within a relationship of trust that causes harm or distress to an older person. Types are **physical, emotional, financial (taking property, pension or allowance), sexual, neglect and abandonment**. In Nepal common forms are property disputes, neglect after children migrate, taking of the allowance, blaming a widow as a *boksi* and leaving an older person alone at a temple or a hospital. **Risk factors** are dependence, dementia, isolation, caregiver stress, alcohol or drug use and financial pressure. The **Senior Citizens Act 2063** places the duty of care on children and relatives, gives older people priority services, provides for care homes, social protection and allowances, and penalises abuse and abandonment; check the latest amendments (the Regulations were amended in 2024).

```svgfig label="5.4" caption="Response to suspected elder abuse. Safety comes first; the older person's wishes and capacity guide the response. Report to the facility lead, the ward office or the police service centre for women, children and senior citizens, and record only facts."
f = Fig(760, 230)
f.box(8, 80, 140, 70, "SUSPECT\nunexplained injury,\nfear, neglect, money", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(180, 80, 140, 70, "ENSURE SAFETY\nseparate and\ninterview in private", fill=ROSE, stroke=RED, size=11, bold=True)
f.box(352, 80, 140, 70, "ASSESS\ncapacity, injuries,\nmoney, caregiver", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(524, 14, 224, 50, "DOCUMENT in the patient's words;\nbody map and photographs with consent", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(524, 90, 224, 50, "REPORT to the senior nurse, doctor,\nward office, police service centre", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(524, 166, 224, 50, "FOLLOW UP: safe place, counselling,\nlegal and social support, caregiver aid", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.arrow([(148, 115), (180, 115)]); f.arrow([(320, 115), (352, 115)])
f.arrow([(492, 100), (524, 40)]); f.arrow([(492, 115), (524, 115)]); f.arrow([(492, 130), (524, 190)])
```

### Elder abuse: eight points of recognition and response

1. **Know the warning signs.** Unexplained bruises, burns or fractures, poor hygiene, weight loss, pressure injuries, fear of a caregiver, missing money or documents and delay in seeking care. A caregiver who answers for the patient or refuses privacy is a red flag.
2. **Ask privately and kindly.** Say, "Has anyone hurt you, taken your money or made you afraid?" Ask without the caregiver present and use an interpreter if needed. Do not promise secrecy but promise help.
3. **Assess capacity and wishes.** A capable adult may choose to stay in a risky home; a person with dementia needs protection. Involve the doctor and, where needed, the social worker.
4. **Ensure immediate safety.** Provide a safe bed, medical treatment and a protected conversation, and admit the patient if needed. Do not discharge an unsafe patient into the same situation without a plan.
5. **Document carefully.** Write the patient's words in quotes, record injuries with a body map and dated photographs (with consent), and note dates and witnesses. These records may be used by the police or a court.
6. **Report through the right channel.** Tell the senior nurse and doctor, the ward office or municipality and the police service centre for women, children and senior citizens. Know your hospital's policy and the **NNC Code of Ethics** duty to protect patients.
7. **Support the caregiver.** Much neglect comes from exhausted or poor caregivers. Offer training, respite, links to the senior citizens' group, the allowance and health insurance, and refer the caregiver for stress or alcohol problems.
8. **Prevent.** Encourage legal documents about property, a bank account in the older person's own name, regular visits by FCHVs and neighbours, and education in the community about the Act and the rights of senior citizens.

## 5.4 Palliative care and the end of life

**Palliative care** improves the quality of life of patients and families facing life-limiting illness by preventing and relieving suffering through early identification and treatment of pain and physical, psychosocial and spiritual problems (WHO). Many older Nepalis die at home from cancer, COPD, heart, kidney or liver failure, stroke or dementia. Palliative services are few and are mainly in Kathmandu Valley and large hospitals, so nurses at the district hospital and health post must give basic palliative care. **Pain** is treated by the WHO analgesic ladder: paracetamol and NSAID, then weak opioid, then **oral morphine** started low in older people with a laxative; the breakthrough dose is **one-sixth of the 24-hour dose**. A patient who takes 5 mg every 4 hours receives **30 mg** in 24 hours, and the breakthrough dose is **5 mg**, as ordered.

### Palliative and end-of-life care: eight points of nursing care

1. **Control pain and symptoms.** Assess pain regularly with a simple scale, give analgesics by the clock and not only on demand, and add a laxative for every patient on opioids. Treat nausea, breathlessness (fan, positioning, small doses of morphine), cough and anxiety.
2. **Communicate honestly and gently.** Ask what the patient and family understand and wish to know, and respect the custom of telling the family first only if the patient agrees. Give information in small pieces and allow silence.
3. **Respect rituals and religion.** Many Hindu families wish for a dying person to be at home with tulsi leaves, Ganga water and chanting, Buddhist families for prayers and a quiet room. Arrange a priest or lama and privacy. Spiritual comfort is part of nursing care.
4. **Provide comfort care.** Give mouth care, turn for comfort, keep the skin clean and dry, use a light blanket, and keep the room calm. Stop unnecessary tests, intravenous fluids and routine observations when the patient is dying, if the plan agrees.
5. **Support eating and drinking sensibly.** Offer small sips and favourite foods; do not force feed. Reduced appetite in the last days is natural and the family needs help to understand it.
6. **Recognise the dying phase.** Signs are sleep, no appetite, cool and mottled limbs, irregular breathing and noisy secretions ("death rattle"). Explain them, keep the family present, reposition and use drugs as ordered for secretions and distress.
7. **Support the family.** Teach basic care, allow presence at the bedside, speak in their language and explain the next steps, including the death certificate and the registration of death at the ward office. Offer bereavement support.
8. **Care after death with dignity.** Wash and wrap the body respectfully, follow religious and family wishes, record the time and complete the documents. Allow family members to take part in the last offices if they wish and care for the nurse's own grief.

## Formula and fact sheet

- Braden total 6-23: 15-18 mild, 13-14 moderate, 10-12 high, 9 or less very high; turn every 2 h; protein 1.25-1.5 g/kg; energy 30-35 kcal/kg; wound area = length × width, and area reduction = (old − new) ÷ old × 100.
- NPIAP stages: 1 non-blanchable redness, 2 partial thickness, 3 full thickness (fat), 4 muscle or bone; plus unstageable and deep tissue injury.
- Nocturnal polyuria index = night urine ÷ 24-hour urine × 100 (above 33%); PVR 100 mL or more suggests retention; 1-hour pad test over 50 g is severe.
- Breakthrough morphine = one-sixth of the 24-hour dose; Nepal: Senior Citizens Act 2063, Regulations 2065, senior citizen from 60 years, allowance from 70 years (60 for Dalit and former Karnali districts); WHO: 15.7% of older people experience abuse each year.

## Chapter summary

- Pressure injury is preventable: assess with the Braden Scale, reposition, redistribute pressure, keep skin clean and dry, and feed for healing.
- Incontinence is common and treatable; find the type, treat reversible causes, use pelvic floor exercise and bladder training, and protect dignity and skin.
- Elder abuse and neglect are common and hidden; ask privately, ensure safety, document, report and support the caregiver; know the Senior Citizens Act.
- Palliative care gives symptom control, honest communication, cultural respect and family support through the last days.

## Practice

```python
m1 = 3 + 3 + 2 + 2 + 3 + 2                       # Braden items
m2 = 450 / 1200 * 100                            # night urine 450 of 1,200 mL
m3 = 60 / 6                                      # breakthrough morphine, 24-hour dose 60 mg
wt = 48                                          # Mrs Kamala
c_braden = 2 + 1 + 1 + 1 + 2 + 1
c_turns = 24 // 2
c_prot, c_kcal = 1.5 * wt, 35 * wt
c_fluid = 1 * c_kcal
c_a0, c_a1 = 4 * 3, 3 * 2
c_red = (c_a0 - c_a1) / c_a0 * 100
c_pad = 146 - 30
print(f"MCQ1 Braden = {m1}; MCQ2 NPi = {m2:.1f}%; MCQ3 breakthrough = {m3:.0f} mg")
print(f"Mrs Kamala: Braden = {c_braden}; turns = {c_turns}; protein = {c_prot:.0f} g; energy = {c_kcal:,} kcal; fluid = {c_fluid:,} mL")
print(f"Mrs Kamala: wound {c_a0} cm2 -> {c_a1} cm2 = {c_red:.1f}% reduction; pad test = {c_pad} g")
```

```text
MCQ1 Braden = 15; MCQ2 NPi = 37.5%; MCQ3 breakthrough = 10 mg
Mrs Kamala: Braden = 8; turns = 12; protein = 72 g; energy = 1,680 kcal; fluid = 1,680 mL
Mrs Kamala: wound 12 cm2 -> 6 cm2 = 50.0% reduction; pad test = 116 g
```

**MCQs (with reasons)**

1. A patient has Braden items 3, 3, 2, 2, 3 and 2. The total and risk level are: (a) 9, very high (b) 15, mild risk (c) 18, no risk (d) 20, none.
2. A patient passes 450 mL of urine at night and 1,200 mL in 24 hours. The nocturnal polyuria index is: (a) 27% (b) 37.5%, nocturnal polyuria (c) 2.7% (d) 75%.
3. The 24-hour oral morphine dose is 60 mg. The breakthrough dose is: (a) 5 mg (b) 10 mg (c) 20 mg (d) 30 mg.
4. When an older patient says her son takes her allowance and leaves her unwashed, the first nursing action is: (a) confront the son at once (b) ensure safety, interview privately, document and report (c) ignore it as a family matter (d) discharge her.
5. Persistent non-blanchable redness over the sacrum with intact skin is: (a) Stage 1 (b) Stage 2 (c) Stage 3 (d) Stage 4.

::: note Answers and rationales
**1. (b).** 3 + 3 + 2 + 2 + 3 + 2 = 15, which is in the mild risk band of 15-18; 9 would be very high risk and 18 is still at risk.
**2. (b).** 450 ÷ 1,200 × 100 = 37.5%, above the 33% limit; 27% and 2.7% are arithmetic errors and 75% is a different ratio.
**3. (b).** One-sixth of 60 mg is 10 mg; 5 mg is one-twelfth, 20 mg is one-third and 30 mg is half.
**4. (b).** Safety, a private interview, factual documentation and reporting protect the patient; confrontation can increase danger and silence continues the abuse.
**5. (a).** Intact skin with non-blanchable redness is Stage 1; Stage 2 has partial-thickness loss of skin, and Stage 3-4 involve fat, muscle or bone.
:::

**Short answer (3 marks): Pressure injury prevention.** Assess risk with the Braden Scale on admission and daily and inspect bony points. Reposition at least every 2 hours with the 30-degree tilt, use a pressure-redistributing mattress and float the heels. Keep skin clean and dry, avoid shear, give 30-35 kcal/kg and 1.25-1.5 g/kg protein, and teach the family.

**Medium answer (5 marks): Describe the nursing management of urinary incontinence (Figure 5.3).** *Assess:* a bladder diary, dipstick, post-void residual, drug and bowel review. *Treat causes:* infection, constipation, delirium, drugs. *Training:* pelvic floor exercises for stress type, bladder training for urge type, prompted voiding for functional type. *Environment:* an easy and lit toilet, a commode and simple clothing. *Skin:* wash, dry, barrier cream, absorbent pads and avoidance of long-term catheters. *Dignity:* privacy and encouragement, with referral for prolapse or prostate treatment.

**Long answer (10 marks): Mrs Kamala Devi Poudel, 84 years, 48 kg, a widow in Pokhara, is bedridden after a stroke and lives with her son and daughter-in-law. She is brought to the district hospital with a 4 × 3 cm Stage 3 sacral pressure injury, urine-soaked clothes, weight loss and a worried manner. She says, "My son collects my allowance and they leave me wet for hours." Her Braden score items are 2, 1, 1, 1, 2 and 1; a one-hour pad test shows 146 g (dry pad 30 g). Calculate and write the nursing care plan.**

*Calculations.* Her Braden score is **8**, very high risk (9 or less). She needs **12 turns** in 24 hours. Protein 1.5 g/kg is **72 g**, energy 35 kcal/kg **1,680 kcal** and fluid 1 mL/kcal **1,680 mL**. The pad test leak is 146 − 30 = **116 g**, severe. When a repeat measure after 4 weeks of care is 3 × 2 cm, the wound area falls from **12 cm²** to **6 cm²**, a **50.0%** reduction.

*Care.* Place her on a pressure-redistributing mattress, turn her every 2 hours at 30 degrees, float the heels and keep the head of the bed low. Clean the wound with saline, remove slough as ordered, apply a moist dressing and measure weekly. Treat the incontinence with a bladder diary, prompted toileting, a commode, absorbent pads changed quickly and barrier cream; avoid a catheter. Give the protein and energy plan and feed small meals; assess swallowing after the stroke. Interview her privately about neglect and the allowance, document her words, inform the senior nurse and doctor and report to the ward office or the police service centre; involve the social worker. Teach the daughter-in-law turning, lifting and skin checks, give her support, and explain the Senior Citizens Act and the family's duty of care. Arrange home-care follow-up through the health post and the FCHV.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "It burns at the back." **O:** Stage 3 sacral wound 12 cm², Braden 8. | **Impaired tissue integrity** related to pressure, shear, moisture and poor nutrition. | **Wound healing:** area reduced by 40% or more in 4 weeks; no infection. | Pressure-redistributing mattress and 2-hourly turns (12 turns) (remove pressure); moist dressing and saline cleaning (support healing); weekly measurement (tracks progress); protein 72 g. | Area 6 cm² at 4 weeks (50.0% reduction). |
| **S:** "I cannot reach the toilet." **O:** pad test 116 g; wet clothing. | **Functional urinary incontinence** related to immobility after stroke and no assistance. | **Urinary continence:** dry for most of the day; no skin breakdown from moisture. | Prompted toileting every 2-3 hours and commode (meets the cause); absorbent pad changed when wet (protects skin); barrier cream (prevents dermatitis); no catheter (avoids CAUTI). | Pad test under 50 g; skin intact. |
| **S:** "I leave half the food." **O:** 48 kg, weight loss; wound. | **Imbalanced nutrition: less than body requirements** related to stroke, dysphagia risk and neglect. | **Nutritional status:** weight stable; intake 1,680 kcal and 1,680 mL. | Swallow screen and speech therapy referral (safe feeding); small frequent protein-rich meals (healing); weekly weight; supplements (reach targets). | Weight 48-49 kg; eats 3 meals. |
| **S:** "They leave me wet; my son takes my allowance." **O:** soiled clothes, anxious, caregiver strained. | **Compromised family coping** related to caregiver burden and financial pressure, with suspected neglect and financial abuse. | **Family coping:** safe care plan agreed; allowance returned to her control. | Private interview and documentation (protect the patient); report to the senior nurse, ward office or police service centre (legal protection); teach and support the caregiver (reduces strain); link with allowance and insurance offices. | Safe plan agreed; patient reports feeling safe. |
