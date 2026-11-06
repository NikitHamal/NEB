---
subject: Adult Nursing II
grade: BSc Nursing Year 2
unit: 1
title: Renal and Urinary Nursing: AKI, CKD, Dialysis, Catheters, UTI and Stones
hours: 20
area: BSN 10 · Adult Nursing II · Unit 1
---

Kidney disease is a quiet and expensive problem in Nepal. **Diabetes and hypertension are the two commonest causes of chronic kidney disease (CKD)**, and both are rising. Many patients reach a hospital only when they are breathless, swollen and vomiting, because early CKD gives no pain. In Kathmandu the Shahid Dharmabhakta National Transplant Centre (Bhaktapur) and the dialysis units of TUTH, Bir, Patan, BPKIHS and the provincial hospitals carry a heavy load, and the government supports dialysis for registered patients at designated hospitals (check the current MoHP rules). Transplant and organ donation are governed by the **Human Body Organ Transplant (Regulation and Prohibition) Act 2055**. The nurse watches urine, weight, blood pressure and potassium, and every number below is checked by program.

::: key What this unit gives you
- Real photographs of a catheter bag with blood-stained urine, a haemodialysis machine and chair, two kidney stones beside a ruler and a kidney ultrasound with a dilated calyx, plus four SVG figures.
- Urine output, creatinine clearance (Cockcroft-Gault), KDIGO staging, fluid balance, URR and interdialytic weight gain.
- Eight points each on CKD complications, catheter-associated UTI prevention, stone prevention and haemodialysis care.
- Model answers and a NANDA-I care plan for a man with CKD stage 5 on haemodialysis.
:::

## 1.1 Renal assessment and the numbers that matter

Ask about urine amount and colour, burning, frequency, night passing of urine (nocturia), flank pain, swelling of the face and feet, appetite, itching and breathlessness. Examine the **blood pressure**, **weight**, **oedema**, **skin** and the lungs. A urine dipstick shows protein, blood, glucose, leucocytes and nitrite; the urine microscopy and culture follow. Blood tests are **creatinine**, **urea (BUN)**, **sodium**, **potassium**, bicarbonate, calcium and haemoglobin. **Normal urine output is about 0.5-1 mL/kg/h (800-2,000 mL a day)**; oliguria is below 0.5 mL/kg/h for 6 hours or 400 mL a day, and anuria is below 100 mL a day. The kidney function is estimated, in adults, by the **Cockcroft-Gault** formula.

```python
age, wt, scr = 64, 60, 3.6                       # years, kg, creatinine mg/dL (male)
crcl = (140 - age) * wt / (72 * scr)
fem = (70 - 0) * 50 / (72 * 1.4) * 0.85          # woman 70 y, 50 kg, creatinine 1.4
kg, passed, hours = 70, 150, 6                   # urine passed in 6 hours
need = 0.5 * kg; rate = passed / kg / hours
base, now = 1.0, 2.5                             # creatinine baseline and now (mg/dL)
u, v, p = 90, 1200, 1.5                          # urine creat mg/dL, volume mL/day, plasma creat
cl24 = u * (v / 1440) / p
print(f"Cockcroft-Gault (man) = (140 - {age}) x {wt} / (72 x {scr}) = {crcl:.1f} mL/min (CKD G4: 15-29)")
print(f"Cockcroft-Gault (woman) = (140 - 70) x 50 / (72 x 1.4) x 0.85 = {fem:.1f} mL/min")
print(f"Minimum urine = 0.5 x {kg} = {need:.0f} mL/h; in {hours} h {need*hours:.0f} mL; he passed {passed} mL = {rate:.2f} mL/kg/h: oliguria")
print(f"Creatinine ratio = {now}/{base} = {now/base:.1f} times baseline: KDIGO stage 2 (2.0-2.9 times)")
print(f"24 h creatinine clearance = {u} x ({v}/1440) / {p} = {cl24:.0f} mL/min")
```

```text
Cockcroft-Gault (man) = (140 - 64) x 60 / (72 x 3.6) = 17.6 mL/min (CKD G4: 15-29)
Cockcroft-Gault (woman) = (140 - 70) x 50 / (72 x 1.4) x 0.85 = 29.5 mL/min
Minimum urine = 0.5 x 70 = 35 mL/h; in 6 h 210 mL; he passed 150 mL = 0.36 mL/kg/h: oliguria
Creatinine ratio = 2.5/1.0 = 2.5 times baseline: KDIGO stage 2 (2.0-2.9 times)
24 h creatinine clearance = 90 x (1200/1440) / 1.5 = 50 mL/min
```

A 64-year-old man with creatinine 3.6 mg/dL and weight 60 kg has a **clearance of 17.6 mL/min**, which is CKD **grade G4** (15-29); a 70-year-old woman of 50 kg with creatinine 1.4 has **29.5 mL/min** after the 0.85 correction. A 70 kg patient needs at least **35 mL/h** (210 mL in 6 hours); one who passes 150 mL has **0.36 mL/kg/h**, which is oliguria. A rise of creatinine from 1.0 to 2.5 is **2.5 times baseline**, which is **KDIGO stage 2** acute kidney injury. A 24-hour urine collection with creatinine 90 mg/dL in 1,200 mL, and a plasma creatinine of 1.5, gives a measured clearance of **50 mL/min**.

## 1.2 Acute kidney injury and chronic kidney disease

**Acute kidney injury (AKI)** is a sudden fall in kidney function over hours to days. **Pre-renal** causes (about half) are low blood flow: dehydration, diarrhoea, bleeding, sepsis and heart failure. **Intrinsic** causes are damage to the kidney itself: acute tubular necrosis from prolonged shock, drugs (gentamicin, NSAIDs, contrast), snakebite, and glomerulonephritis. **Post-renal** causes are blockage: stones, a big prostate and tumours. KDIGO stages AKI by creatinine rise (stage 1: 1.5-1.9 times baseline or 0.3 mg/dL rise; stage 2: 2.0-2.9 times; stage 3: 3 times or dialysis) and by urine output. AKI is often reversible if the cause is treated early: fluids for pre-renal, relief of the block for post-renal, and stopping nephrotoxic drugs.

**Chronic kidney disease (CKD)** is a reduced filtration rate (GFR below 60 mL/min) or kidney damage (such as albuminuria) for more than 3 months. It is staged G1 to G5 by GFR, and A1 to A3 by albumin in urine. In **G5 (GFR below 15)**, or **end-stage kidney disease (ESKD)**, life needs dialysis or a transplant.

```svgfig label="1.1" caption="KDIGO classification of CKD by GFR (mL/min) with the nurse's focus at each grade. G1-G2: find the cause and control blood pressure and glucose. G3: avoid nephrotoxic drugs, treat anaemia and bone disease. G4: prepare for dialysis (protect the arm veins, make a fistula). G5: start dialysis or transplant when symptoms or hyperkalaemia, acidosis or fluid overload cannot be controlled."
f = Fig(760, 250)
rows = [("G1  90 or more", "Normal or high; damage present", MINT, TEAL), ("G2  60-89", "Mildly reduced", MINT, TEAL), ("G3a  45-59", "Mild to moderate", SAND, AMBER), ("G3b  30-44", "Moderate to severe", SAND, AMBER), ("G4  15-29", "Severely reduced", ROSE, RED), ("G5  below 15", "Kidney failure (ESKD)", ROSE, RED)]
for i, (a, b, fl, st) in enumerate(rows):
    y = 12 + i * 36
    f.box(10, y, 170, 30, a, fill=fl, stroke=st, size=11.5, bold=True)
    f.box(185, y, 215, 30, b, fill=fl, stroke=st, size=11)
f.box(425, 12, 325, 66, "G1-G2: treat cause; BP below 130/80;\ncontrol glucose; stop smoking", fill=MINT, stroke=TEAL, size=11, bold=True)
f.box(425, 84, 325, 66, "G3: avoid NSAIDs and contrast;\ntreat anaemia, bone disease, acidosis", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(425, 156, 325, 66, "G4-G5: vascular access, diet, diuretics,\ndialysis or transplant planning", fill=ROSE, stroke=RED, size=11, bold=True)
f.text(380, 242, "Each grade also carries an albuminuria category A1 (under 30 mg/g), A2 (30-300), A3 (over 300)", size=10.5, color=NAVY, bold=True)
```

### Chronic kidney disease: eight complications the nurse must recognise

1. **Fluid overload and hypertension.** Failing kidneys cannot remove salt and water, so the weight rises, the feet and face swell and the lungs may fill (pulmonary oedema). Blood pressure climbs. Weigh daily, count the fluid and limit salt.
2. **Hyperkalaemia.** Potassium above 5.5 mmol/L causes weakness, slow pulse and tall T waves on the ECG, and above 6.5 it may stop the heart. Watch the ECG and the blood results. Calcium gluconate, insulin with dextrose, salbutamol and dialysis are given by order.
3. **Metabolic acidosis.** The kidney cannot excrete acid, so the bicarbonate falls and the breathing becomes deep and fast (Kussmaul). Acidosis also causes bone loss and muscle wasting. Sodium bicarbonate tablets may be ordered.
4. **Anaemia.** Damaged kidneys make less erythropoietin, so the haemoglobin falls and the patient feels tired and pale. Give epoetin (about 50 IU/kg three times a week), iron and transfusion only when needed. Keep the haemoglobin near 10-11 g/dL.
5. **Mineral and bone disease.** High phosphate, low calcium and high parathyroid hormone weaken bones and calcify vessels. Give phosphate binders with meals, calcium and vitamin D by order and limit dairy, nuts and cola.
6. **Uraemia.** Waste products cause nausea, itching, a metallic taste, hiccups, confusion, a pericardial rub and, if untreated, convulsions and coma. These are indications to start dialysis. Give mouth care and skin care.
7. **Infection.** Uraemia weakens immunity and lines and fistulas break the skin. Use strict hand hygiene, vaccinate against hepatitis B, influenza and pneumococcus, and treat fever at once.
8. **Cardiovascular disease and depression.** Most CKD deaths come from heart attack and stroke, and the long illness brings fear, loss of work and money worries. Control BP, lipids and glucose, listen to the patient and involve the family and social worker.

## 1.3 Urinary tract infection and the urinary catheter

A **urinary tract infection (UTI)** is infection anywhere from the urethra to the kidney. **Cystitis** (bladder) causes burning, frequency, urgency and suprapubic pain; **pyelonephritis** (kidney) adds fever, rigors, flank pain and vomiting. **Escherichia coli** causes most infections, and women are at more risk because the urethra is short. The urine culture shows more than 100,000 colonies per mL, and treatment follows the culture and the local antibiogram: for example nitrofurantoin or cotrimoxazole for simple cystitis (3-5 days) and a parenteral cephalosporin or aminoglycoside for pyelonephritis.

A **catheter-associated UTI (CAUTI)** is the commonest hospital infection after a catheter has been in place for more than 2 days. The **infection rate** is expressed per 1,000 catheter-days: if there are 4 infections in 1,250 catheter-days the rate is 4 / 1,250 × 1,000 = **3.2 per 1,000 catheter-days**.

```photogrid label="1.2" cols="4" ratio="1.0" caption="Renal and urinary nursing. (a) A real drainage bag with blood-stained urine (haematuria), showing its scale and drain tap. (b) A real haemodialysis machine beside a dialysis chair. (c) Two real kidney stones passed by a patient, shown beside a centimetre ruler. (d) A real ultrasound (sagittal section) of a kidney with a dilated calyx: hydronephrosis from a blocked ureter."
@ photo id="nur6/hemat" cap="Haematuria in bag"
fit 1.0
focus 0.5 0.5
mark 0.30 0.78 "1"
mark 0.55 0.40 "2"
key 1 (a) Scale: measure and chart the volume at every shift
key 2 (a) Blood-stained urine: a sign of bleeding or clot; report it and watch the tube for blockage
@ photo id="nur6/dial" cap="Haemodialysis machine"
fit 1.0
focus 0.4 0.5
mark 0.42 0.72 "3"
mark 0.82 0.40 "4"
key 3 (b) Screen: shows blood flow, pressures, time and weight removed
key 4 (b) Chair: the patient sits here for 4 hours, three times a week
@ photo id="nur6/stone" cap="Kidney stones"
fit 1.0
focus 0.5 0.5
mark 0.35 0.62 "5"
mark 0.50 0.22 "6"
key 5 (c) Stones: rough, brown calculi of calcium salts; small ones pass in urine
key 6 (c) Ruler: stones larger than 10 mm seldom pass without treatment
@ photo id="nur6/hydro" cap="Hydronephrosis on ultrasound"
fit 1.0
focus 0.5 0.5
mark 0.43 0.55 "7"
mark 0.50 0.20 "8"
key 7 (d) Dilated calyx: urine is backing up behind a blockage
key 8 (d) Sagittal section: the label shows the plane through the kidney
```

### Catheter-associated UTI: eight points of prevention

1. **Insert only when needed.** Valid reasons are acute retention, strict hourly output in critical illness, major surgery, pressure ulcer healing of a patient who is incontinent, and end of life comfort. Convenience of staff is not a reason. Write the reason in the notes.
2. **Use strict aseptic technique at insertion.** Wash hands, use sterile gloves, drape, antiseptic solution and sterile lubricant jelly. Choose the smallest catheter that drains well (usually 14-16 Fr in adults). Breaking asepsis pushes bacteria into the bladder.
3. **Secure and keep the system closed.** Fix the tube to the thigh so it does not pull the urethra, and never disconnect the tube from the bag. A closed system stops bacteria entering. Sample from the sampling port with a sterile syringe.
4. **Keep the bag below the bladder and off the floor.** Urine must flow downhill, because backflow carries bacteria upward. Empty the bag when it is three-quarters full with a clean container for each patient. Do not let the tap touch the container.
5. **Give daily meatal care.** Clean the urethral opening and the tube with soap and water each day and after a bowel motion. Bacteria climb along the outside of the tube. Do not use antiseptic creams routinely.
6. **Keep urine flowing.** Check for kinks, clots and a full bag and keep fluid intake at 2 L a day unless restricted. Flow washes bacteria out. Bladder irrigation is needed only when there is clot retention.
7. **Review the need every day.** Ask each morning whether the catheter can be removed, and use a nurse-led stop order. Each extra day raises the risk of infection by 3-7%. Do a trial without catheter after surgery as early as possible.
8. **Watch for infection and teach.** Report fever, cloudy or foul urine, flank pain and new confusion in the elderly, and send a culture before antibiotics. Teach patient and family to keep the bag low, wash hands and report problems.

## 1.4 Renal calculi (urolithiasis)

A **kidney stone** is a hard crystal mass (calcium oxalate in 80%, also uric acid, struvite and cystine) that forms when urine is concentrated and low in citrate. Nepal lies in the Asian stone belt, and hill farmers, labourers in hot Terai plains and people who drink little water are commonly affected. **Renal colic** is a severe, wave-like pain from the loin to the groin with vomiting, restlessness and blood in the urine (Plate 1.2c). The diagnosis uses the history, urine dipstick, ultrasound (Plate 1.2d shows the dilated calyx behind a block) and a non-contrast CT or X-ray KUB. Treatment is analgesia (diclofenac IM or PR, with opioids as needed), fluids, an alpha blocker (tamsulosin) to help passage of stones under 10 mm, and for larger stones **ESWL (shock-wave lithotripsy)**, ureteroscopy or percutaneous nephrolithotomy. Infected, obstructed kidneys are an emergency.

### Kidney stones: eight points of health education

1. **Drink enough water.** Aim for 2.5-3 litres a day so that the urine is pale and the output above 2 litres. At **2,500 mL over 16 waking hours this is 156 mL every hour**. Dilute urine stops crystals forming.
2. **Eat less salt.** More sodium in food brings more calcium into the urine. Reduce pickles, instant noodles, salted fish and papad. Aim for under 5 g of salt a day.
3. **Do not cut calcium.** Normal dietary calcium (milk, curd) binds oxalate in the gut and lowers stones. Avoid calcium tablets unless ordered. Cutting dairy makes calcium-oxalate stones more likely.
4. **Limit oxalate-rich foods.** Spinach, rhubarb, nuts, tea in large amounts and chocolate raise urinary oxalate. Use them in small amounts and with a meal. Do not stop vegetables altogether.
5. **Moderate animal protein.** Too much meat, fish and eggs raises uric acid and lowers citrate. Keep portions to a palm size. Add lemon or citrus fruits for natural citrate.
6. **Strain the urine and keep the stones.** Use a clean cloth or a strainer at each passing of urine in an attack. A stone sent to the laboratory shows its type and guides prevention. Record the size and time.
7. **Manage pain and know the red flags.** Take medicine on time and walk and move; heat on the loin comforts. Go to hospital at once for fever, shaking chills, vomiting that stops drinking, or no urine. These suggest an infected, blocked kidney.
8. **Follow up and treat the cause.** Stones come back in half of patients within 10 years. Take medicines for gout, infection or high calcium as advised and repeat the ultrasound after treatment. A high-risk patient may need a metabolic work-up.

## 1.5 Dialysis and renal replacement

**Haemodialysis (HD)** passes the patient's blood through a dialyser (an artificial kidney) against dialysate across a semipermeable membrane; waste and extra potassium leave by **diffusion**, and extra water by **ultrafiltration**. The usual schedule is 4 hours, three times a week, through an **arteriovenous (AV) fistula** (the best long-term access, made by joining an artery and a vein at the wrist or elbow), a graft or a central venous catheter for urgent starts. **Peritoneal dialysis (PD)** uses the abdominal lining as the membrane: dialysate is run into the peritoneal cavity through a catheter, left to dwell and drained; it is done at home (CAPD, 4 exchanges a day) and suits patients far from a unit, which helps in remote Nepal, but peritonitis is its danger. **Kidney transplantation** from a living or deceased donor gives the best survival and quality of life and is done at the national transplant centre in Bhaktapur and in several private hospitals.

```python
pre, post = 120, 36                              # urea (mg/dL) before and after dialysis
urr = (pre - post) / pre * 100
dry, arrive = 58, 61.5                           # dry weight and weight on arrival (kg)
gain = arrive - dry; pct = gain / dry * 100
urine = 300; allow = urine + 500                 # fluid allowance mL/day
iv, oral, uo, drain = 1000, 800, 700, 100        # 24 h intake and output (mL)
bal = iv + oral - (uo + drain)
epo = 50 * 60                                    # 50 IU/kg, weight 60 kg
print(f"URR = ({pre} - {post}) / {pre} x 100 = {urr:.0f}% (target 65% or more)")
print(f"Interdialytic gain = {arrive} - {dry} = {gain:.1f} kg = {pct:.1f}% of dry weight (aim under 4-5%)")
print(f"Fluid allowance = urine {urine} + 500 = {allow} mL/day")
print(f"Balance = ({iv} + {oral}) - ({uo} + {drain}) = +{bal:,} mL")
print(f"Epoetin 50 IU/kg x 60 kg = {epo:,} IU per dose, three times a week")
```

```text
URR = (120 - 36) / 120 x 100 = 70% (target 65% or more)
Interdialytic gain = 61.5 - 58 = 3.5 kg = 6.0% of dry weight (aim under 4-5%)
Fluid allowance = urine 300 + 500 = 800 mL/day
Balance = (1000 + 800) - (700 + 100) = +1,000 mL
Epoetin 50 IU/kg x 60 kg = 3,000 IU per dose, three times a week
```

A patient whose urea falls from 120 to 36 mg/dL has a **urea reduction ratio of 70%**, above the 65% target. One who arrives at 61.5 kg with a dry weight of 58 kg has gained **3.5 kg, or 6.0%**, which is too much and needs fluid teaching. The rule for a fluid allowance is the previous day's urine plus 500 mL for insensible loss, so **300 + 500 = 800 mL a day**. A chart showing 1,800 mL in and 800 mL out gives a **positive balance of +1,000 mL**, which is about 1 kg of retained water. Epoetin at 50 IU/kg for a 60 kg patient is **3,000 IU per dose**.

```svgfig label="1.3" caption="The haemodialysis circuit. Blood leaves the fistula, is pumped (200-400 mL/min) past a heparin syringe into the dialyser, where it flows against dialysate in the opposite direction (counter-current). Waste and potassium diffuse into the dialysate and water is removed by pressure. Blood returns through the air trap, which detects bubbles, to the patient. Pressure monitors and the air detector protect the patient."
f = Fig(760, 250)
f.box(10, 100, 110, 60, "AV fistula\n(patient's arm)", fill=ROSE, stroke=RED, size=11, bold=True)
f.box(160, 100, 100, 60, "Blood pump\n200-400 mL/min", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(160, 20, 100, 44, "Heparin\nsyringe", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(300, 85, 190, 90, "DIALYSER\nblood and dialysate\nflow in opposite directions", fill=MINT, stroke=TEAL, size=11, bold=True)
f.box(300, 200, 190, 40, "Dialysate in (Na, K, Ca, bicarbonate)", fill=BLUE, stroke=NAVY, size=10.5)
f.box(300, 14, 190, 44, "Used dialysate to drain:\nurea, K+, water removed", fill=SAND, stroke=AMBER, size=10.5)
f.box(540, 100, 110, 60, "Air trap and\nbubble detector", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(660, 100, 90, 60, "Blood back\nto patient", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.arrow([(120, 130), (160, 130)], sw=2); f.arrow([(260, 130), (300, 130)], sw=2); f.arrow([(490, 130), (540, 130)], sw=2); f.arrow([(650, 130), (660, 130)], sw=2)
f.arrow([(210, 64), (210, 100)], sw=1.6); f.arrow([(395, 200), (395, 175)], sw=1.6); f.arrow([(395, 85), (395, 58)], sw=1.6)
```

### Haemodialysis: eight points of nursing care

1. **Before dialysis: weigh and assess.** Record the weight, the BP lying and standing, the pulse, temperature and the leg and lung signs. Compare the weight with the dry weight to plan the fluid to remove. Check the last potassium and haemoglobin and any missed doses.
2. **Protect the vascular access.** Feel the **thrill** (buzz) and listen for the bruit in the fistula before each session. Never take BP, draw blood or start an IV in that arm. A lost thrill means clotting, and the doctor must be called at once.
3. **Use strict asepsis for cannulation and lines.** Clean the skin, wear a mask and sterile gloves and give catheter dressings with sterile technique. Dialysis patients share a unit, so hepatitis B, C and HIV control is essential. Use a separate machine for a positive patient according to the unit policy.
4. **Monitor during dialysis.** Record the BP, pulse, blood flow and pressures every 30-60 minutes. The commonest problem is **hypotension with cramps and nausea**: lower the head of the bed, stop or slow the ultrafiltration and give 100 mL of normal saline by order.
5. **Prevent and manage complications.** Watch for **air embolism** (clamp the line, lie the patient on the left side with the head down), **disequilibrium syndrome** (headache, confusion in the first sessions; reduce the speed), bleeding and **access bleeding** (apply gentle pressure). Keep the emergency drugs ready.
6. **After dialysis: care of the needle sites.** Apply light pressure until the bleeding stops (10-15 minutes) and avoid tight bandages. Take the weight again and record the fluid removed. Let the patient sit before standing and give a meal.
7. **Teach diet and fluid control.** Restrict potassium (banana, orange, potato, tomato, coconut water), phosphate and salt, and take enough protein (1.0-1.2 g/kg) from eggs, fish and pulses that have been soaked and boiled. Limit fluid to the urine volume plus 500 mL. Keep the weight gain under 4% of the dry weight.
8. **Support, drugs and follow-up.** Explain the medicines (phosphate binders with food, vitamin D, epoetin, iron, antihypertensives timed after dialysis). Counsel about work, sex and fear, and refer to the social worker for financial support and transplant counselling. Teach the patient to attend every session, because skipped sessions cause hyperkalaemia and death.

## Formula and fact sheet

- Cockcroft-Gault = (140 − age) × weight (kg) ÷ (72 × creatinine mg/dL), × 0.85 for women; CKD G4 is 15-29 and G5 below 15.
- Oliguria below 0.5 mL/kg/h for 6 h; KDIGO stage 1 = 1.5-1.9 × baseline, stage 2 = 2.0-2.9 ×, stage 3 = 3 × or dialysis.
- Clearance = U × V ÷ P; URR = (pre − post) ÷ pre × 100 (target 65% or more); CAUTI rate = infections ÷ catheter-days × 1,000.
- Fluid allowance = urine volume + 500 mL; interdialytic gain below 4-5% of dry weight; epoetin 50 IU/kg three times a week.

## Chapter summary

- Urine output (0.5 mL/kg/h), creatinine and weight are the three bedside measures; CKD is staged by GFR and treated by controlling BP, glucose, diet and drugs.
- AKI is reversible if the cause (pre-renal, intrinsic or post-renal) is treated early; stop nephrotoxic drugs.
- CAUTI is prevented by avoiding catheters, using asepsis, a closed system, daily review and early removal.
- Stones are prevented with water and less salt; haemodialysis care protects the fistula, controls fluid and potassium and watches for hypotension and air embolism.

## Practice

**MCQs (with reasons)**

1. The minimum acceptable hourly urine output of an 80 kg adult is: (a) 20 mL (b) 40 mL (c) 80 mL (d) 400 mL.
2. A dialysis patient with a dry weight of 50 kg arrives at 52 kg. The interdialytic gain is: (a) 2.0% (b) 4.0% (c) 5.0% (d) 40%.
3. Epoetin 50 IU/kg is ordered for a 70 kg patient. The dose is: (a) 350 IU (b) 1,750 IU (c) 3,500 IU (d) 35,000 IU.
4. Urea falls from 120 to 30 mg/dL in dialysis. The URR is: (a) 25% (b) 50% (c) 75% (d) 90%.
5. Before starting dialysis you cannot feel the thrill in the fistula. The first action is to: (a) start dialysis in the other arm (b) inform the doctor at once and do not use the access (c) massage the arm firmly (d) apply a warm pack and wait.

::: note Answers and rationales
**1. (b).** 0.5 mL/kg/h × 80 kg = 40 mL/h; 400 mL is the daily minimum, not hourly, and 80 mL/h would be 1 mL/kg/h.
**2. (b).** 2 ÷ 50 × 100 = 4.0%; this is at the upper limit of the usual 4-5% target, so fluid teaching is needed; 40% forgets to divide by the weight.
**3. (c).** 50 × 70 = 3,500 IU; (a) and (d) are errors of a factor of ten and (b) uses 25 IU/kg.
**4. (c).** (120 − 30) ÷ 120 × 100 = 75%; 90 is the difference in mg/dL, not a percentage, and 25% is the proportion left.
**5. (b).** A missing thrill means that the fistula has clotted; forcing a needle in or waiting wastes the access that took months to mature, so tell the doctor and arrange a catheter or an angioplasty.
:::

**Short answer (3 marks): Catheter-associated urinary tract infection (CAUTI).** It is a urinary infection that appears in a patient whose urinary catheter has been in place for more than 2 days. Bacteria enter along the catheter outer surface or through the drainage bag, and the risk rises by 3-7% for each day. It is prevented by inserting a catheter only for valid reasons, aseptic technique, a closed system, bag below the bladder and removal as soon as possible.

**Medium answer (5 marks): Describe the nursing care of a patient on haemodialysis (Figure 1.3).** *Before:* weigh the patient against the dry weight, record BP, pulse and temperature and check the thrill and bruit of the fistula. *During:* use aseptic technique for the needles, record BP, pulse and machine pressures every 30-60 minutes, and watch for hypotension (lie flat, slow ultrafiltration, 100 mL saline), cramps, air embolism (clamp, left side, head down) and bleeding. *After:* press on the needle sites for 10-15 minutes, weigh again and let the patient rest before standing. *Teaching:* the fluid allowance (urine plus 500 mL), low potassium and salt diet with enough protein, drugs, access protection (no BP or needles in the fistula arm) and regular attendance. Support the family and refer to the social worker. Record all in the dialysis chart.

**Long answer (10 marks): Mr Ram Bahadur Thapa, 58 years, a farmer from Gorkha with diabetes for 15 years and hypertension, is admitted to the medical ward of a provincial hospital with 4 days of vomiting, itching, breathlessness and swollen legs. Creatinine is 6.8 mg/dL, potassium 6.4 mmol/L, BP 170/100 mmHg and he passes about 100 mL of urine a day. His dry weight is 56 kg and he weighs 61.5 kg now. The diagnosis is CKD stage 5 and he will start haemodialysis. Calculate his clearance and write the nursing care plan.**

*Calculations.* At 58 years and 56 kg with a creatinine of 6.8 mg/dL, the Cockcroft-Gault clearance is (140 − 58) × 56 ÷ (72 × 6.8) = **9.4 mL/min**, so he is in stage G5 (below 15). He should pass at least 0.5 × 56 = **28 mL/h** and passes about 4 mL/h, which is oliguria. He has gained **5.5 kg, which is 9.8% of the dry weight**, so the fluid is overloaded. His fluid allowance is 100 mL urine + 500 = **600 mL a day**. Epoetin 50 IU/kg for his dry weight of 56 kg is **2,800 IU** three times a week.

*Care.* Admit him in a semi-upright position and give oxygen if the SpO2 is below 94%. Put him on the cardiac monitor because the potassium of 6.4 can cause arrhythmia, and be ready with calcium gluconate 10 mL of 10% IV over 10 minutes, insulin 10 units with 50 mL of 50% dextrose (25 g) and salbutamol by order. Weigh him daily, measure the BP and keep a strict intake-output chart. Limit fluid to 600 mL, salt and potassium. Protect the arm that will hold the fistula: no BP, no cannulas or blood sampling on it. Give mouth and skin care for the uraemia and itching, antihypertensives, a phosphate binder and the epoetin and iron as ordered, and check the blood sugar because insulin needs fall in kidney failure and hypoglycaemia is common. Assist with a temporary dialysis catheter, give catheter care by a sterile technique and watch for infection and bleeding. Explain every step, involve the family, discuss costs and the government dialysis support with the social worker and teach the diet and fluid plan before discharge.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "My legs are swollen and I cannot breathe lying down." **O:** weight 61.5 kg (dry 56), BP 170/100, urine 100 mL/day, crackles. | **Excess fluid volume** related to compromised regulatory mechanism (renal failure), as evidenced by weight gain of 5.5 kg, oedema and dyspnoea. | **Fluid balance:** weight within 1 kg of dry weight after dialysis; clear lungs; no oedema. | 1. Daily weight and strict intake-output chart; *shows the retained water.* 2. Fluid limit 600 mL and salt under 5 g; *stops further gain.* 3. Sit upright, give oxygen; *eases breathing.* 4. Prepare for dialysis and record the ultrafiltration; *removes the excess.* | Weight 57 kg after the first session, SpO2 97% on air, oedema reduced. |
| **O:** K 6.4 mmol/L, ECG with tall T waves, weakness. | **Risk for electrolyte imbalance** related to impaired renal regulation (hyperkalaemia). | **Electrolyte balance:** K 3.5-5.0 mmol/L, normal ECG, no arrhythmia. | 1. Continuous ECG monitoring; *early detection of arrhythmia.* 2. Calcium gluconate, insulin with dextrose and salbutamol by order; *protect the heart and shift K into cells.* 3. Low-potassium diet teaching (no banana, orange, potato); *prevents recurrence.* 4. Repeat K after dialysis; *confirms removal.* | K 4.6 mmol/L after dialysis; ECG normal. |
| **S:** "Nothing tastes good; I vomit and itch." **O:** urea high, loss of weight. | **Imbalanced nutrition: less than body requirements** related to anorexia and uraemic nausea, as evidenced by vomiting and weight loss. | **Nutritional status:** eats 75% of meals, no vomiting within 3 days. | 1. Give antiemetics before meals; *reduces nausea.* 2. Protein 1.0-1.2 g/kg on dialysis from eggs, fish, soaked pulses; *replaces losses.* 3. Small frequent meals and oral care; *better intake and taste.* 4. Dietitian referral; *tailored low-K, low-phosphate plan.* | Eating about 70-75% of meals, nausea controlled. |
| **O:** temporary dialysis catheter, diabetes. | **Risk for infection** related to invasive device and diabetes. | **Infection severity:** no fever, clean exit site for the whole stay. | 1. Sterile dressing, hand hygiene and mask for catheter care; *blocks entry of bacteria.* 2. Check the site and temperature each shift; *early detection.* 3. Keep glucose 140-180 mg/dL; *high sugar impairs defences.* 4. Teach the patient not to touch the dressing; *protects the line.* | Afebrile, site clean on day 7. |

::: tip Exam tip
For a CKD or dialysis case write the Cockcroft-Gault value, the 0.5 mL/kg/h urine target, the interdialytic gain as a percentage, the fluid allowance (urine + 500 mL), hyperkalaemia emergency drugs and four NANDA-I diagnoses beginning with excess fluid volume and risk for electrolyte imbalance.
:::
