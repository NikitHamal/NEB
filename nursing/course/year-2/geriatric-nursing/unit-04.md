---
subject: Geriatric Nursing
grade: BSc Nursing Year 2
unit: 4
title: Medicines in Older Adults: Pharmacokinetics, Polypharmacy, Beers Criteria and Deprescribing
hours: 8
area: BSN 11 · Geriatric Nursing · Unit 4
---

An older Nepali often arrives at the clinic with a plastic bag of tablets: some from the hospital, some from the corner pharmacy, some from an Ayurvedic *baidya*, and some borrowed from a neighbour. Sleeping tablets, painkillers, antacids and "vitamins" are bought without a prescription, and many drugs are taken long after the reason has gone. Older people take more drugs, handle them more slowly and react to them more strongly, so **adverse drug reactions are a leading cause of falls, confusion and hospital admission** in old age. The geriatric nurse is the last safety check between the prescription and the patient. All arithmetic in this unit is checked by program.

::: key What this unit gives you
- Real photographs of a weekly pill organiser, a medication-reminder blister card and hands opening a blister strip, plus four SVG figures.
- Pharmacokinetic and pharmacodynamic changes, Cockcroft-Gault dosing, half-life and steady state, anticholinergic burden, polypharmacy, the 2023 AGS Beers criteria, STOPP/START and the deprescribing cycle.
- Eight high-risk drug groups, eight points of safe medication nursing and adherence maths.
- Model answers and a NANDA-I care plan for an older man with hypoglycaemia and eleven medicines.
:::

## 4.1 How the older body handles a drug

Four processes decide a drug's effect: **absorption, distribution, metabolism and excretion (pharmacokinetics)**, and the body's response to the drug (**pharmacodynamics**). In old age:

- **Absorption** changes little; less stomach acid and slower gut movement matter mainly for iron, calcium and vitamin B12.
- **Distribution** shifts: body water and muscle fall and fat rises, and albumin is lower in illness. **Fat-soluble drugs (diazepam) spread widely and stay long; water-soluble drugs (digoxin, gentamicin, lithium) reach higher blood levels** from a standard dose; low albumin raises the free fraction of phenytoin and warfarin.
- **Metabolism** slows because liver blood flow and enzyme activity fall; first-pass drugs (propranolol, morphine) reach higher levels.
- **Excretion** is the largest change: the glomerular filtration rate falls with age, and **serum creatinine stays "normal" because muscle mass is lower**. Doses of renally cleared drugs must be set by the **Cockcroft-Gault creatinine clearance**.
- **Pharmacodynamics:** the brain is more sensitive to sedatives, opioids and anticholinergics, and the baroreflex is blunted, so drugs that lower BP cause falls.

The rule is **"start low, go slow"**: begin with half the adult dose, increase gradually and review often.

```svgfig label="4.1" caption="Four pharmacokinetic changes that make a standard adult dose too much for many older people. The result is higher or longer drug levels and a greater effect on a more sensitive brain and blood pressure control."
f = Fig(760, 220)
items = [("ABSORPTION", "little change;\nless acid, slower gut\n(iron, calcium, B12)", BLUE, NAVY), ("DISTRIBUTION", "less water, more fat,\nless albumin: diazepam\nstays, digoxin rises", SAND, AMBER),
         ("METABOLISM", "less liver flow\nand enzyme activity:\nlonger half-life", MINT, TEAL), ("EXCRETION", "GFR falls about\n1 mL/min a year:\nrenal drugs accumulate", ROSE, RED)]
for i, (h, t, fl, st) in enumerate(items):
    x = 10 + i * 187
    f.box(x, 14, 175, 34, h, fill=st, stroke=st, color="#ffffff", size=11, bold=True)
    f.box(x, 54, 175, 80, t, fill=fl, stroke=st, size=11, bold=True)
f.arrow([(380, 138), (380, 162)], color=SLATE, sw=2)
f.box(110, 164, 540, 46, "Higher or longer drug level + a more sensitive brain and BP = more falls, confusion and bleeding", fill=ROSE, stroke=RED, color=RED, size=11, bold=True)
```

```python
age, wt, cr = 84, 45, 1.2                          # woman, creatinine 1.2 mg/dL
crcl = (140 - age) * wt / (72 * cr) * 0.85
enox = 1.0 * wt                                    # enoxaparin 1 mg/kg once daily when CrCl is below 30
t12_young = 20
t12_old = 20 + (80 - 20)                           # diazepam: about 20 h at age 20, rising about 1 h per year
ss_young, ss_old = 5 * t12_young / 24, 5 * t12_old / 24   # steady state after about 5 half-lives (days)
acb = {"amitriptyline": 3, "ranitidine": 1, "furosemide": 1, "metoprolol": 1}
print(f"Cockcroft-Gault CrCl = (140 - {age}) x {wt} / (72 x {cr}) x 0.85 = {crcl:.1f} mL/min (below 30)")
print(f"Enoxaparin for CrCl below 30 = 1 mg/kg x {wt} kg = {enox:.0f} mg once daily (as ordered)")
print(f"Diazepam half-life {t12_young} h at 20 years and {t12_old} h at 80 years; steady state {ss_young:.1f} days vs {ss_old:.1f} days")
print(f"Anticholinergic burden score = {sum(acb.values())} (3 or more is clinically relevant)")
```

```text
Cockcroft-Gault CrCl = (140 - 84) x 45 / (72 x 1.2) x 0.85 = 24.8 mL/min (below 30)
Enoxaparin for CrCl below 30 = 1 mg/kg x 45 kg = 45 mg once daily (as ordered)
Diazepam half-life 20 h at 20 years and 80 h at 80 years; steady state 4.2 days vs 16.7 days
Anticholinergic burden score = 6 (3 or more is clinically relevant)
```

An 84-year-old woman of 45 kg with a serum creatinine of 1.2 has a clearance of only **24.8 mL/min**, although 1.2 looks almost normal. Enoxaparin for a clearance below 30 is **45 mg once daily** (1 mg/kg), as the doctor orders. Diazepam's half-life lengthens from about 20 h at age 20 to about 80 h at age 80, so it takes **16.7 days** to reach steady state (and the same time to leave the body after stopping) instead of **4.2 days**; a nightly dose therefore builds up and causes day-time drowsiness and falls. The **anticholinergic burden** of amitriptyline (3), ranitidine (1), furosemide (1) and metoprolol (1) is **6**, well above the level of 3 linked to confusion and falls.

```svgfig label="4.2" caption="Why a long half-life matters. Using the 5-half-lives rule, a drug with a half-life of 20 h reaches steady state in about 4.2 days; the same drug with a half-life of 80 h in an 80-year-old takes about 16.7 days. The same dose builds up for two weeks, and the level falls just as slowly after the drug is stopped."
f = Fig(760, 250)
f.line(60, 20, 60, 210, color=SLATE, sw=1.4); f.line(60, 210, 730, 210, color=SLATE, sw=1.4)
def X(d): return 60 + d / 20 * 650
def Y(p): return 210 - p / 100 * 185
for p in (0, 25, 50, 75, 100):
    f.line(60, Y(p), 730, Y(p), color="#cbd5e1", sw=0.6); f.text(52, Y(p), str(p) + "%", size=10, anchor="end", vmid=True)
for d in (0, 4, 8, 12, 16, 20):
    f.text(X(d), 226, str(d), size=10); f.line(X(d), 210, X(d), 214)
f.text(395, 244, "Days of daily dosing", size=11, bold=True)
for t12, col, nm in ((20, TEAL, "half-life 20 h (young adult)"), (80, RED, "half-life 80 h (age 80)")):
    pts = [(X(d / 2), Y((1 - 0.5 ** ((d / 2) * 24 / t12)) * 100)) for d in range(0, 41)]
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]): f.line(x1, y1, x2, y2, color=col, sw=2.8)
f.line(X(4.2), Y(97), X(4.2), 210, color=TEAL, sw=1.2, dash=True); f.line(X(16.7), Y(97), X(16.7), 210, color=RED, sw=1.2, dash=True)
f.text(X(4.2) + 6, Y(38), "steady state\nday 4.2", size=10.5, color=TEAL, bold=True, anchor="start")
f.text(X(16.7) - 6, Y(60), "steady state\nday 16.7", size=10.5, color=RED, bold=True, anchor="end")
f.box(420, 150, 300, 36, "teal: half-life 20 h | red: half-life 80 h", fill=SAND, stroke=AMBER, size=11, bold=True)
```

## 4.2 Polypharmacy and potentially inappropriate medicines

**Polypharmacy** is the regular use of **five or more drugs**, and **hyper-polypharmacy** is ten or more. It is sometimes needed (heart failure, diabetes), but it becomes harmful when drugs are given without a clear reason, in doubled doses, or to treat the side effects of other drugs (a **prescribing cascade**: an NSAID raises BP, then an antihypertensive is added, which causes dizziness and a fall). The risk of an adverse reaction rises sharply with every extra drug, and with more than one prescriber, no review and use of Ayurvedic or over-the-counter products. Tools to find the harm are the **AGS Beers Criteria (2023 update)**, which lists medicines to avoid or use with caution in those aged 65 and over, and **STOPP/START (version 3, 2023)**, which lists drugs to *stop* (STOPP) and useful drugs that are *missing* (START, for example a statin after stroke or calcium and vitamin D with osteoporosis). Both are guides: the final decision is the doctor's and the patient's.

```photogrid label="4.3" cols="3" ratio="1.0" caption="Medicines at home. (a) A real weekly pill organiser with seven compartments, filled once a week by the patient, nurse or relative. (b) A real medication-reminder card with the doses arranged by time of day (breakfast, lunch, supper, bedtime). (c) Real hands pressing a tablet out of a blister strip: the grip, finger strength and eyesight of the patient decide whether the pack can be used."
@ photo id="nur7/pillbox" cap="Weekly pill organiser"
fit 1.0
focus 0.5 0.55
mark 0.47 0.50 "1"
mark 0.33 0.35 "2"
key 1 (a) Lid and compartments: one for each day; a missed day is visible
key 2 (a) A single compartment: check the contents against the prescription list each week
@ photo id="nur7/blister" cap="Medication reminder card"
fit 1.0
focus 0.5 0.2
mark 0.50 0.76 "3"
mark 0.40 0.40 "4"
key 3 (b) Header row: the four times of day, each with its own column
key 4 (b) A column of identical capsules: a missing tablet in a row means a missed dose
@ photo id="nur7/pills" cap="Opening a blister strip"
fit 1.0
focus 0.5 0.5
mark 0.50 0.70 "5"
mark 0.20 0.33 "6"
key 5 (c) Blister strip: push the tablet through the foil; check the name and expiry
key 6 (c) Hand: weak grip or arthritis makes foil and child-proof caps difficult; ask for easy-open packs
```

### Eight high-risk drug groups in older adults (Beers 2023 and STOPP)

1. **Benzodiazepines and Z-drugs (diazepam, alprazolam, zolpidem).** They cause confusion, falls, hip fracture, car crashes and dependence, and their half-life is long in older people. Avoid starting them for sleep or anxiety; if the patient has taken them for years, reduce by 10-25% every 1-2 weeks, never suddenly. Teach sleep hygiene instead.
2. **Anticholinergics and first-generation antihistamines (chlorpheniramine, promethazine, diphenhydramine, hyoscine, amitriptyline, oxybutynin).** They cause confusion, dry mouth, constipation, urinary retention, blurred vision and delirium, and add up in a "burden" score. They are common in Nepali cough and cold mixtures bought over the counter. Replace with safer options and teach families to read labels.
3. **NSAIDs (diclofenac, ibuprofen, ketorolac).** They cause stomach bleeding, kidney injury, raised BP and heart failure and interact with warfarin and ACE inhibitors. Use topical gel, paracetamol first and the shortest oral course with food and a stomach-protecting drug if unavoidable; avoid when CrCl is below 30.
4. **Sulfonylureas (glibenclamide, glimepiride).** The 2023 update widened the warning to all sulfonylureas because of severe, prolonged **hypoglycaemia**, which looks like confusion or a fall. Glibenclamide is widely used in Nepal. Prefer metformin (with kidney check) or safer agents; if one is used, a short-acting drug such as glipizide is better. Teach the signs of low sugar.
5. **Aspirin for primary prevention and some anticoagulants.** Starting aspirin to prevent a first heart attack is now to be avoided in older adults because bleeding outweighs the benefit; consider stopping it if there is no heart or stroke history. Avoid starting warfarin when a safer direct anticoagulant is available, and use rivaroxaban with caution for long-term use. Never stop an anticoagulant without the doctor.
6. **Proton pump inhibitors (omeprazole, pantoprazole) beyond 8 weeks.** Long use raises the risk of *C. difficile* infection, pneumonia, fractures and low B12 and magnesium. Review the reason; reduce to the lowest dose or on-demand use unless there is a clear indication such as a bleeding ulcer or Barrett oesophagus.
7. **Antipsychotics (haloperidol, risperidone, olanzapine).** In dementia they raise the risk of stroke, pneumonia and death. Use only for severe distress or danger after non-drug measures fail, at the lowest dose for the shortest time, and stop as soon as possible.
8. **Opioids, muscle relaxants and combinations of three or more CNS-active drugs.** Combining an opioid with a benzodiazepine, gabapentinoid or sedative multiplies the risk of falls, confusion and respiratory depression. Count the CNS-active drugs on the list: **three or more** is a signal for review. Give a bowel regimen with every opioid.

```svgfig label="4.4" caption="The deprescribing cycle. Medicines are reviewed on a schedule, not only when something goes wrong. Drugs without a current indication, with harm greater than benefit or duplicated are stopped one at a time with a monitoring plan, and the patient and the family take part in every decision."
f = Fig(760, 250)
steps = [("1. LIST", "every drug: tablets,\ninjections, Ayurvedic,\nshop-bought", BLUE, NAVY), ("2. REVIEW", "indication, dose, CrCl,\nBeers and STOPP,\nanticholinergic score", SAND, AMBER), ("3. PRIORITISE", "stop the highest-harm,\nlowest-benefit drug\nfirst", ROSE, RED),
         ("4. TAPER AND STOP", "one change at a time;\nslow taper for diazepam,\nsteroid, SSRI", MINT, TEAL), ("5. MONITOR", "symptoms, BP, glucose,\nfalls, mood; record and\nrepeat review", BLUE, NAVY)]
for i, (h, t, fl, st) in enumerate(steps):
    x = 8 + i * 150
    f.box(x, 40, 140, 30, h, fill=st, stroke=st, color="#ffffff", size=10.5, bold=True)
    f.box(x, 74, 140, 80, t, fill=fl, stroke=st, size=10.5, bold=True)
    if i < 4: f.arrow([(x + 140, 114), (x + 150, 114)], color=SLATE, sw=2)
f.arrow([(640, 156), (640, 190), (78, 190), (78, 158)], color=SLATE, dash=True)
f.text(380, 206, "Repeat the review every 6-12 months and after every admission", size=11, color=SLATE, bold=True)
f.box(180, 8, 400, 26, "Shared decision with the patient, family and prescriber", fill=MINT, stroke=TEAL, size=11, bold=True)
```

### Eight points of nursing responsibility for safe medicines in older people

1. **Take a complete medicine history.** Ask about prescribed, over-the-counter, Ayurvedic, herbal and borrowed medicines, and ask the patient or family to bring all packs ("brown bag review"). Note allergies, alcohol and tobacco. Keep one written list and give a copy to the patient.
2. **Check the dose against kidney function.** Do not trust a "normal" creatinine; look for the Cockcroft-Gault clearance and the doctor's dose adjustment, especially for gentamicin, enoxaparin, digoxin, metformin and antibiotics. Report a falling urine output.
3. **Give the right drug by the right route.** Check the six rights, watch for tablets that cannot be crushed, check swallowing, and give oral drugs upright with a full glass of water. Avoid IM injections in a frail, thin person where possible.
4. **Monitor for adverse effects.** Look for new confusion, dizziness, falls, constipation, bleeding, rash, low BP, slow pulse and low glucose after every new drug. In older people, a new symptom is a drug effect until proved otherwise.
5. **Check adherence.** Count tablets, ask what the patient actually takes and why they stop. Reasons are cost, fear of side effects, forgetfulness and not understanding. Use pill organisers, a reminder card and family help.
6. **Make the pack easy to use.** Choose large-print labels, easy-open containers, picture charts for those who cannot read and one daily time where possible. Tell the pharmacist which drugs are to be dispensed in organised blister packs.
7. **Teach in simple steps.** For each drug, say the name, what it is for, how to take it, the important side effect and when to call. Use teach-back. Warn against sharing drugs and against buying sleeping tablets or painkillers without a prescription.
8. **Report and review.** Record reactions in the pharmacovigilance form (the Department of Drug Administration receives reports) and ask for a medication review at every admission, discharge and transfer. Support deprescribing in the team.

```python
disp, left, days, per_day = 60, 12, 30, 2           # tablets dispensed, returned, days, tablets/day
adh = (disp - left) / (days * per_day) * 100
wt = 45
para = 15 * wt                                      # paracetamol 15 mg/kg per dose
para_max = 60 * wt                                  # at most 60 mg/kg/day in the frail under 50 kg
vol, drops, mins = 500, 20, 6 * 60                  # 500 mL over 6 h, 20 gtt/mL set (slow in heart failure)
gtt = vol * drops / mins
print(f"Adherence by pill count = ({disp} - {left}) / ({days} x {per_day}) x 100 = {adh:.1f}% (80% or more is good)")
print(f"Paracetamol 15 mg/kg x {wt} kg = {para} mg per dose; daily limit 60 mg/kg = {para_max:,} mg")
print(f"IV rate = {vol} mL x {drops} / {mins} min = {gtt:.1f} drops/min, about {round(gtt)} gtt/min")
```

```text
Adherence by pill count = (60 - 12) / (30 x 2) x 100 = 80.0% (80% or more is good)
Paracetamol 15 mg/kg x 45 kg = 675 mg per dose; daily limit 60 mg/kg = 2,700 mg
IV rate = 500 mL x 20 / 360 min = 27.8 drops/min, about 28 gtt/min
```

A patient given 60 tablets for 30 days of twice-daily dosing who returns 12 has taken 48, an adherence of **80.0%**, at the 80% threshold. For a frail patient weighing 45 kg, paracetamol 15 mg/kg is **675 mg** per dose with a daily limit of 60 mg/kg, **2,700 mg**. A slow infusion for a patient with heart failure, 500 mL over 6 hours with a 20 drops/mL set, runs at about **28 drops per minute**.

## Formula and fact sheet

- Cockcroft-Gault CrCl = (140 − age) × weight ÷ (72 × creatinine) (× 0.85 for women); steady state = about 5 half-lives; polypharmacy = 5 or more drugs, hyper-polypharmacy = 10 or more.
- Beers 2023 highlights: avoid starting aspirin for primary prevention; avoid all sulfonylureas as first or second-line; avoid warfarin as first choice and long-term rivaroxaban; avoid 3 or more CNS-active drugs; benzodiazepines, first-generation antihistamines and antipsychotics in dementia.
- Anticholinergic burden score of 3 or more is clinically relevant; paracetamol 15 mg/kg, not above 60 mg/kg/day in the frail under 50 kg; IV rate = volume × drop factor ÷ minutes.
- Deprescribing cycle: list, review, prioritise, taper and stop, monitor.

## Chapter summary

- Older people have less muscle and water, more fat, less liver and kidney clearance and a more sensitive brain, so "start low, go slow".
- Creatinine misleads: use Cockcroft-Gault clearance for renally cleared drugs.
- Beers and STOPP/START identify high-risk drugs; benzodiazepines, anticholinergics, sulfonylureas and NSAIDs cause most harm.
- Nurses take the full medicine history, check adherence, make packs easy to use, teach and report, and support deprescribing.

## Practice

```python
m1 = (140 - 80) * 70 / 72                           # man, 80 y, 70 kg, creatinine 1.0
m2 = 5 * 80 / 24                                    # diazepam half-life 80 h
m3 = 250 * 20 / (4 * 60)                            # 250 mL over 4 h, 20 gtt/mL
wt, age, cr = 52, 81, 1.3                           # Mr Hari Prasad
c_crcl = (140 - age) * wt / (72 * cr)
c_n = 11
c_acb = 3 + 3 + 1                                   # amitriptyline, chlorpheniramine, furosemide
c_mg = 2.4 * 18                                     # glucose mmol/L to mg/dL
c_d10 = 15 / 10 * 100                               # 15 g glucose from 10% dextrose (mL)
c_taper = 4 * 2                                     # diazepam: four 25% steps, 2 weeks each
print(f"MCQ1 CrCl = {m1:.1f} mL/min; MCQ2 days = {m2:.1f}; MCQ3 rate = {m3:.0f} gtt/min")
print(f"Mr Hari: CrCl = {c_crcl:.1f} mL/min; drugs = {c_n}; ACB = {c_acb}; glucose 2.4 mmol/L = {c_mg:.0f} mg/dL")
print(f"Mr Hari: 15 g glucose = {c_d10:.0f} mL of 10% dextrose; diazepam taper = {c_taper} weeks")
```

```text
MCQ1 CrCl = 58.3 mL/min; MCQ2 days = 16.7; MCQ3 rate = 21 gtt/min
Mr Hari: CrCl = 32.8 mL/min; drugs = 11; ACB = 7; glucose 2.4 mmol/L = 43 mg/dL
Mr Hari: 15 g glucose = 150 mL of 10% dextrose; diazepam taper = 8 weeks
```

**MCQs (with reasons)**

1. An 80-year-old man weighs 70 kg and his creatinine is 1.0 mg/dL. His Cockcroft-Gault clearance is about: (a) 41.7 (b) 58.3 (c) 100 (d) 84 mL/min.
2. Diazepam has a half-life of 80 h in an 80-year-old. The days to steady state (5 half-lives) are: (a) 3.3 (b) 8.3 (c) 16.7 (d) 33.3.
3. 250 mL is ordered over 4 hours with a 20 drops/mL set. The rate is: (a) 10 (b) 15 (c) 21 (d) 42 gtt/min.
4. A patient takes amitriptyline, chlorpheniramine and furosemide. The main nursing concern is: (a) low anticholinergic load (b) high anticholinergic burden: confusion, retention, constipation and falls (c) vitamin deficiency (d) none.
5. Under the 2023 Beers criteria the recommendation for starting aspirin to prevent a first heart attack in a 75-year-old is to: (a) always start (b) avoid starting it (c) double the dose (d) give with an NSAID.

::: note Answers and rationales
**1. (b).** (140 − 80) × 70 ÷ (72 × 1.0) = 58.3 mL/min; 41.7 uses a weight of 50 kg and 100 ignores age.
**2. (c).** 5 × 80 ÷ 24 = 16.7 days; 3.3 days is for a half-life of 16 h and 33.3 multiplies by ten.
**3. (c).** 250 × 20 ÷ 240 = 21 gtt/min; 10 and 15 use the wrong drop factor or time, and 42 is the rate for 500 mL.
**4. (b).** Amitriptyline and chlorpheniramine carry a score of 3 each and furosemide 1, a total of 7, linked to delirium, retention, constipation and falls.
**5. (b).** Evidence shows more bleeding than benefit in older adults who have not had a heart or stroke event; those already taking it should be reviewed by the doctor.
:::

**Short answer (3 marks): Why are older people at risk of adverse drug reactions?** They take more drugs and often have several prescribers. Body water and muscle fall and fat rises, so the distribution of drugs changes; liver metabolism and renal clearance fall, so drugs last longer; the brain and the baroreflex are more sensitive; and memory, vision and cost affect adherence. Therefore doses are started low, renal function is calculated and drugs are reviewed regularly.

**Medium answer (5 marks): Explain the deprescribing process (Figure 4.4).** *List* all drugs, including Ayurvedic and over-the-counter ones. *Review* the indication, dose, kidney function, Beers and STOPP criteria and the anticholinergic score. *Prioritise* drugs with the highest harm and lowest benefit, such as long-term benzodiazepines, duplicate NSAIDs and aspirin for primary prevention. *Taper and stop* one drug at a time, slowly for benzodiazepines, steroids and SSRIs. *Monitor* symptoms, BP, glucose, falls and mood, record the outcome and repeat the review in 6-12 months. Include the patient and family and inform all prescribers.

**Long answer (10 marks): Mr Hari Prasad Adhikari, 81 years, 52 kg, a retired clerk from Dharan, is admitted to a teaching hospital after a fall at 3 am. His blood glucose is 2.4 mmol/L and creatinine 1.3 mg/dL. He takes 11 drugs: glibenclamide, metformin, amlodipine, enalapril, furosemide, aspirin 75 mg (no heart disease), diclofenac for knee pain, diazepam 5 mg at night, amitriptyline 25 mg at night, omeprazole (3 years) and chlorpheniramine for a cough. Calculate and write the nursing care plan.**

*Calculations.* His Cockcroft-Gault clearance is (140 − 81) × 52 ÷ (72 × 1.3) = **32.8 mL/min** (far lower than the creatinine suggests). He takes **11 drugs** (hyper-polypharmacy). The anticholinergic burden of amitriptyline (3), chlorpheniramine (3) and furosemide (1) is **7**. His glucose of 2.4 mmol/L is **43 mg/dL**, severe hypoglycaemia. Fifteen grams of glucose is **150 mL of 10% dextrose**. The diazepam taper by 25% every 2 weeks takes **8 weeks**.

*Care.* Treat the hypoglycaemia at once (glucose IV or oral as ordered, recheck in 15 minutes and then hourly) and monitor for recurrence because glibenclamide lasts long. Do a brown bag review. Ask the doctor to stop glibenclamide, reduce metformin for the kidney function, stop diclofenac, aspirin (primary prevention), chlorpheniramine and amitriptyline, and to review omeprazole, furosemide and BP drugs against his lying and standing BP. Taper diazepam slowly and teach sleep hygiene. Give a written list, a pill organiser and a large-print chart, teach the signs of low sugar, and arrange a follow-up with the medicine clinic and the ward FCHV. Teach the family not to buy sleeping or cough medicines without a prescription.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "I felt shaky and sweaty, then fell." **O:** glucose 2.4 mmol/L (43 mg/dL), on glibenclamide, CrCl 32.8. | **Unstable blood glucose level** (risk of hypoglycaemia) related to sulfonylurea in reduced renal clearance. | **Blood glucose level:** glucose 5-10 mmol/L; no hypoglycaemia for 4 weeks. | Treat with 150 mL 10% dextrose or oral glucose and recheck (restores brain glucose); hourly glucose for 12 h (long-acting drug); stop sulfonylurea as ordered (removes the cause); teach signs and snacks. | No glucose below 4 mmol/L at 4 weeks. |
| **S:** "I take many tablets; some from the pharmacy." **O:** 11 drugs, ACB 7, diclofenac with CrCl 32.8. | **Ineffective health self-management** related to complex regimen and over-the-counter use. | **Medication response:** takes only the reviewed list; adherence 80% or more. | Brown bag review (finds all drugs); written list, pill organiser, large print (support memory); teach-back (confirms understanding); coordinate deprescribing with the doctor (reduces harm). | Five drugs remain; adherence 90%. |
| **S:** "I cannot sleep without my tablet." **O:** diazepam and amitriptyline nightly; fall at 3 am. | **Risk for falls** related to sedatives, hypoglycaemia and nocturia. | **Fall prevention behaviour:** no falls in 3 months. | Taper diazepam by 25% every 2 weeks over 8 weeks (avoid withdrawal); sleep hygiene (warm drink, fixed time); night light and commode (safe toileting); lying and standing BP (finds orthostatic hypotension). | No falls; sleeps 6 hours. |
| **S:** "Why were my tablets stopped?" **O:** anxious, family worried. | **Deficient knowledge** about the new regimen. | **Knowledge: medication:** states the reason for each drug. | Plain-language teaching and picture chart; involve the family; give a contact number (reduces fear); schedule review at 6 months. | Explains each drug correctly. |
