---
subject: Midwifery I
grade: BSc Nursing Year 3
unit: 3
title: Antenatal Care: History, Examination, Leopold's Grips, Screening, Safe Motherhood and Aama, Danger Signs and Birth Preparedness
hours: 24
area: BSN 17-18 · Midwifery I · Unit 4
---

Maya Magar, 28, is a mother of two from a village in Kavre. At 34 weeks she walks 90 minutes to the birthing centre because "my head is splitting and the lights look strange". The auxiliary nurse midwife takes her blood pressure: **160/110 mmHg**; the urine strip turns orange-brown for protein. Four ANC visits at months 4, 6, 8 and 9 were meant to find exactly this sooner, but Maya attended only two. This unit covers the **antenatal assessment** that every midwife must perform: history, general and obstetric examination, **Leopold's grips**, fetal heart rate, screening tests, the **Nepal ANC protocol and the Aama programme**, **danger signs**, and **birth preparedness and complication readiness (BPCR)**.

::: key What this unit gives you
- Real images: the four **Leopold's grips** (Leopold and Spörlin's original 1894 plates), a **urine dipstick**, a **rapid HIV, hepatitis B and hepatitis C test** cassette and a **magnesium sulfate** infusion bag on a stand; with numbered marks.
- SVG figures: the **Nepal and WHO ANC schedules**, a **bar chart of NDHS maternal-care trends (1996-2022)** and the **pre-eclampsia decision algorithm**.
- **Eight danger signs** and **eight elements of BPCR**, each in 3-4 plain sentences, and the screening tests with the OGTT cut-offs.
- Verified maths: HMIS coverage and dropout, IFA stock, **MAP**, and the **magnesium sulfate loading and maintenance volumes**; MCQs, short, medium and long answers and a 5-column NANDA-I plan for severe pre-eclampsia.
:::

## 3.1 Aims of antenatal care and the Nepal context

**Antenatal care (ANC)** is the planned series of contacts between a pregnant woman and a skilled provider to keep her and the baby healthy, find problems early and prepare for birth. Its aims are to **promote health**, **screen and treat** (anaemia, infection, hypertension, diabetes), **prevent** (Td, iron, calcium, malaria nets), **prepare** for birth and the newborn, and **build a relationship** that brings her back for delivery and postnatal care.

**The Nepal protocol.** MoHP's Safe Motherhood programme counts a woman as having completed the protocol when she has **four ANC visits at months 4, 6, 8 and 9** (about 12-16, 24-28, 32 and 36 weeks), an institutional delivery and a postnatal check. WHO's 2016 model recommends **eight contacts** (first before 12 weeks, then 20, 26, 30, 34, 36, 38 and 40 weeks), which reduced perinatal deaths in modelling studies; Nepal's guidelines are moving toward more contacts, so always check the current MoHP circular. The **Aama (Safe Motherhood) Programme** gives free delivery care and a transport incentive for institutional birth, and an incentive for completing four ANC visits (amounts differ by ecological belt and over time, so confirm at the facility). The **NDHS 2022** shows how far Nepal has come: **94%** of women had skilled ANC, **81%** had four or more visits, **73%** made their first visit in the first trimester, **79%** delivered in a health facility and **80%** with a skilled provider (Figure 3.2).

```svgfig label="3.1" caption="The ANC schedules compared. Nepal's protocol uses four visits at months 4, 6, 8 and 9; WHO 2016 recommends eight contacts. Services marked with each visit are the minimum package: history and examination at every visit; iron-folic acid from the fourth month (180 tablets); albendazole after 12 weeks; Td two doses; calcium; urine, Hb and infection screening; ultrasound at 18-22 weeks where available; birth plan at the third visit."
f = Fig(760, 330)
f.line(40, 50, 720, 50, color=SLATE, sw=2)
for x, w in [(40, "0"), (150, "12"), (260, "20"), (340, "26"), (405, "30"), (470, "34"), (520, "36"), (580, "38"), (640, "40")]:
    f.line(x, 44, x, 56, color=SLATE, sw=2); f.text(x, 36, w, size=10, color=SLATE, bold=True)
f.text(700, 36, "weeks", size=10, color=SLATE, bold=True)
f.text(20, 80, "NEPAL (4 visits)", size=11, color=TEAL, bold=True, anchor="start")
for x, s in [(150, "1: month 4\n(12-16 wk)"), (320, "2: month 6\n(24-28 wk)"), (450, "3: month 8\n(32 wk)"), (540, "4: month 9\n(36 wk)")]:
    f.box(x - 42, 90, 88, 46, s, fill=MINT, stroke=TEAL, size=9.5, bold=True)
f.text(20, 170, "WHO 2016 (8 contacts)", size=11, color=NAVY, bold=True, anchor="start")
for x, s in [(110, "1\n<12"), (260, "2\n20"), (340, "3\n26"), (405, "4\n30"), (470, "5\n34"), (520, "6\n36"), (580, "7\n38"), (640, "8\n40")]:
    f.box(x - 22, 180, 44, 44, s, fill=BLUE, stroke=NAVY, size=10, bold=True)
f.box(40, 250, 330, 66, "EVERY VISIT: BP, weight, urine protein,\nfundal height, fetal heart, danger signs, counselling", fill=SAND, stroke=AMBER, size=10, bold=True)
f.box(390, 250, 340, 66, "PACKAGE: IFA 180 tablets from month 4, albendazole,\nTd x 2, calcium, malaria net (endemic areas), scan,\nHb, blood group and Rh, HIV, syphilis, HBsAg", fill=MINT, stroke=TEAL, size=10, bold=True)
```

```svgfig label="3.2" caption="Maternal care in Nepal, NDHS 1996 compared with NDHS 2022 (percent of women with a recent birth). Skilled ANC rose from 25% to 94%, four or more ANC visits from 9% to 81%, and skilled birth attendance from 10% to 80%. The remaining gap is greatest in the Tarai, among less educated women and in remote hill districts; the postnatal check within 2 days (70% in 2022) and neonatal mortality (21 per 1,000, unchanged since 2016) are the next frontier."
f = Fig(760, 300)
rows = [("Skilled ANC provider", 25, 94), ("Four or more ANC visits", 9, 81), ("Skilled birth attendant", 10, 80)]
y = 30
for name, a, b in rows:
    f.text(20, y + 14, name, size=11, color=SLATE, bold=True, anchor="start")
    f.box(230, y, a * 4.6, 22, "", fill=SAND, stroke=AMBER); f.text(230 + a * 4.6 + 6, y + 15, f"1996: {a}%", size=10, color=AMBER, bold=True, anchor="start")
    f.box(230, y + 28, b * 4.6, 22, "", fill=MINT, stroke=TEAL); f.text(230 + b * 4.6 + 6, y + 43, f"2022: {b}%", size=10, color=TEAL, bold=True, anchor="start")
    y += 85
f.line(230, 18, 230, 285, color=SLATE, sw=1.4)
```

## 3.2 History and examination at the first visit

**History.** Record **personal data** (age, occupation, education, caste or ethnic group, distance from the facility), **menstrual history** (LMP, cycle, EDD), **obstetric history** (GTPAL, previous births: mode, place, birth weight, complications such as PPH, stillbirth, pre-eclampsia, caesarean), **medical and surgical history** (diabetes, hypertension, heart, TB, epilepsy, asthma, HIV, previous operations), **family history** (twins, diabetes, congenital problems), **drug and allergy history**, **personal habits** (smoking, alcohol, *khaini*), **nutrition**, **workload and rest**, and **social support and safety** at home. Ask about the present pregnancy: bleeding, discharge, fever, headache, swelling, fetal movement.

**General examination.** Weigh her and measure height (**under 145 cm** is a risk), take BP (rest 5 minutes, sitting, correct cuff), pulse, temperature and respiration, check for pallor (conjunctiva, palm), jaundice, oedema (face, hands, legs), goitre, breasts (nipples), teeth and legs (varicose veins). **Abdominal examination** has four steps: **inspect** (shape, scars, linea nigra, striae, fetal movement), **palpate** (fundal height, Leopold's grips), **auscultate** (fetal heart) and, if needed, **vaginal examination** (usually not at routine ANC).

**Leopold's grips** (Plate 3.1) are performed with the woman lying on her back, knees slightly bent, bladder empty, and the midwife's hands warm; the first three grips face the woman's head and the fourth faces her feet. **Grip 1 (fundal):** both hands at the top of the uterus find the **fundal height** and what lies in the fundus: a soft, broad, irregular **breech** or a hard, round, ballotable **head**. **Grip 2 (lateral or umbilical):** one hand steadies the uterus while the other feels the sides; the smooth, firm curve is the **back** and the knobby irregular part is the **limbs**, which gives the **position**. **Grip 3 (pelvic or Pawlik's):** the right hand grasps the lower pole above the symphysis to find the **presenting part** (head is firm and ballotable; breech is soft) and whether it is **engaged** (not movable). **Grip 4 (deep pelvic):** facing the feet, both hands press down on each side to measure **how many fifths of the head are palpable above the brim** and the **attitude** (flexion). A head that is **5/5 palpable at 38 weeks in a primigravida** is not engaged (Unit 1).

```photogrid label="3.1" cols="4" ratio="1.0" caption="Leopold's four grips in the original plates of Leopold and Spörlin (1894). (a) Grip 1: hands on the fundus find what lies at the top of the uterus. (b) Grip 2: hands on both sides find the back and the limbs. (c) Grip 3 (Pawlik): the right hand grasps the presenting part above the symphysis. (d) Grip 4: the examiner faces the feet and feels how much of the head is above the brim."
@ photo id="nur11/leo1" cap="Grip 1: fundal"
fit 1.0
focus 0.5 0.5
mark 0.47 0.70 "1"
key 1 (a) Both hands cup the fundus: breech (soft) or head (hard)?
@ photo id="nur11/leo2" cap="Grip 2: lateral"
fit 1.0
focus 0.5 0.5
mark 0.22 0.55 "2"
mark 0.70 0.55 "3"
key 2 (b) Left hand: feels the back or the limbs on the left side
key 3 (b) Right hand: the opposite side; smooth back, knobby limbs
@ photo id="nur11/leo3" cap="Grip 3: Pawlik's"
fit 1.0
focus 0.5 0.5
mark 0.55 0.42 "4"
key 4 (c) Right hand grasps the presenting part above the symphysis
@ photo id="nur11/leo4" cap="Grip 4: deep pelvic"
fit 1.0
focus 0.5 0.5
mark 0.30 0.38 "5"
mark 0.74 0.45 "6"
key 5 (d) Fingers press toward the pelvis: head above the brim?
key 6 (d) Other hand mirrors it: count the fifths of the head palpable
```

**Fetal heart rate (FHR)** is counted for a full minute with a **Pinard horn, Doppler or fetoscope**, placed over the fetal back (the anterior shoulder); normal is **110-160 beats per minute**; a rate below 110 or above 160 or irregular is referred. **Fetal movements:** the mother counts **10 movements in 12 hours** ("count-to-ten"); fewer movements signal possible fetal compromise. **Terms:** **lie** (long axis of fetus to mother: longitudinal, transverse, oblique), **presentation** (part at the pelvic brim: cephalic, breech, shoulder), **position** (relation of the denominator to the pelvis, e.g. left occipito-anterior, LOA), **attitude** (flexion) and **engagement** (the widest part of the head has passed the brim).

## 3.3 Screening and investigations

| Test | When | Abnormal result and action |
|---|---|---|
| **Haemoglobin** | First visit; 28-36 weeks | Below 11 g/dL = anaemia: iron treatment, search for hookworm and malaria; below 7 g/dL refer |
| **Urine protein** (dipstick) | Every visit | 1+ or more with BP of 140/90 or more: suspect pre-eclampsia; with burning, check for infection |
| **Urine sugar** and **OGTT** | OGTT at 24-28 weeks (75 g glucose) | Gestational diabetes if fasting 92 mg/dL or more, 1-hour 180 or more, or 2-hour 153 or more (IADPSG); diet, insulin, refer |
| **Blood group and Rh** | First visit | Rh-negative: repeat antibody screen, anti-D 300 micrograms at 28 weeks (per protocol) and within 72 hours after an Rh-positive birth |
| **HIV, syphilis (RPR/VDRL), hepatitis B** | First visit (opt-out, with consent) | Reactive HIV: start ART same day (PMTCT); syphilis: benzathine penicillin 2.4 MU IM; HBsAg: baby gets birth dose and HBIG |
| **Blood pressure** | Every visit | 140/90 or more on two readings 4 hours apart is hypertension; with proteinuria it is pre-eclampsia |
| **Ultrasound** | 18-22 weeks (anomaly scan) and for any danger sign | Placenta praevia, twins, growth restriction, malformation |
| **Malaria, TB screen** | Endemic districts; any cough over 2 weeks | Rapid test and treat; refer for TB workup |

```photogrid label="3.2" cols="3" ratio="1.0" caption="Screening tools in real images. (a) A urine reagent strip held against its colour scale: each pad reacts to one substance (protein, glucose, blood, nitrite, leukocytes, ketones, pH). (b) A rapid test cassette for HIV, hepatitis B surface antigen and hepatitis C; a control line must appear for the test to be valid. (c) A magnesium sulfate infusion bag on an IV stand, the anticonvulsant used to prevent and treat eclampsia."
@ photo id="nur11/urine" cap="Urine dipstick and colour chart"
fit 1.0
focus 0.5 0.5
mark 0.22 0.55 "1"
key 1 (a) Reagent pads on the strip: compare colours with the chart on time
@ photo id="nur11/rapid" cap="HIV, HBsAg, HCV rapid tests"
fit 1.0
focus 0.5 0.5
mark 0.45 0.62 "2"
key 2 (b) Cassette: read at the stated minutes; no control line means invalid
@ photo id="nur11/mgso4" cap="Magnesium sulfate infusion"
fit 1.0
focus 0.5 0.5
mark 0.50 0.70 "3"
key 3 (c) Magnesium sulfate bag: check the label, dose and pump every time
```

**Immunisation and supplements.** **Td** (tetanus-diphtheria) two doses at least 4 weeks apart for unprotected women and a booster in later pregnancies (NIP Nepal); NDHS 2022 found **93%** of mothers protected against neonatal tetanus. **IFA** 60 mg iron with 400 mcg folic acid daily from the fourth month for 180 days (and 45 days after birth); **albendazole** 400 mg once after the first trimester; **calcium** as per the current national protocol (it reduces pre-eclampsia risk in low-intake settings). Offer **malaria nets** in endemic districts and teach **hygiene, rest (8 hours at night, 2 hours at midday), nutrition (one extra meal a day), avoiding heavy loads and smoke** and when to return.

```python
pop, cbr = 30000, 20                         # ward population; assumed crude birth rate per 1,000
expected = pop * cbr // 1000                 # expected births in a year
anc1, anc4, inst, sba = 540, 432, 450, 462   # women with first ANC, four ANC, institutional births, SBA births
cov1, cov4 = anc1 / expected * 100, anc4 / expected * 100
dropout = (anc1 - anc4) / anc1 * 100
inst_cov, sba_cov = inst / expected * 100, sba / expected * 100
ifa = expected * 180
stock = ifa * 1.10
print(f"Expected births {expected}; ANC1 {cov1:.0f}%; ANC4 {cov4:.0f}%; dropout ANC1 to ANC4 {dropout:.0f}%")
print(f"Institutional {inst_cov:.0f}%; SBA {sba_cov:.0f}%; IFA need {ifa:,} tablets; with 10% buffer {stock:,.0f}")
```

```text
Expected births 600; ANC1 90%; ANC4 72%; dropout ANC1 to ANC4 20%
Institutional 75%; SBA 77%; IFA need 108,000 tablets; with 10% buffer 118,800
```

In a ward of 30,000 people with a crude birth rate of 20 per 1,000 there are **600** expected births. The 540 women with a first ANC visit give **90%** coverage; the 432 with four visits give **72%**, so **20%** drop out between the first and fourth visit. Institutional births are **75%** and skilled attendance **77%**; the IFA need for the year is **108,000** tablets, or **118,800** with a 10% buffer. The health post manager uses exactly these indicators from **HMIS and DHIS2**.

## 3.4 Eight danger signs in pregnancy

Every woman, her husband and her mother-in-law must know these signs by heart, and the FCHV repeats them at the mothers' group. **Any one of them means: go to a hospital now, do not wait for morning.**

1. **Vaginal bleeding.** Any bleeding after 22 weeks is dangerous. Painless bright-red bleeding suggests placenta praevia; painful bleeding with a hard tender uterus suggests placental abruption. The midwife must **not do a vaginal examination**, must lay her down, start an IV line, and send her with an escort.
2. **Severe headache, blurred vision or epigastric pain.** These suggest severe pre-eclampsia, especially with high BP. The headache does not go away with paracetamol, and the epigastric pain can mean a swollen liver. Take the BP at once and begin the pre-eclampsia protocol (Figure 3.3).
3. **Convulsions or unconsciousness.** A fit in a pregnant woman is eclampsia until proved otherwise. Protect her airway and injuries, turn her to the left side, give magnesium sulfate and refer. Never leave her alone.
4. **Fever above 38 °C.** It can be malaria, urinary infection, pneumonia, typhoid or chorioamnionitis. High fever harms the fetus. Cool the woman, take a blood film or rapid test in endemic districts, give the first dose of an antibiotic and refer if the cause is unclear.
5. **Leaking of fluid before labour.** Gush or trickle of clear fluid before 37 weeks is preterm prelabour rupture of membranes, and after 37 weeks is PROM. The danger is infection and cord prolapse. Advise a clean pad, no vaginal examination, and send her to the hospital.
6. **Reduced or absent fetal movements.** Less than 10 movements in 12 hours, or a sudden change, may mean fetal hypoxia. Listen to the fetal heart. Absent heart sounds mean possible fetal death and need ultrasound and counselling with kindness.
7. **Severe abdominal pain.** Constant severe pain with a hard uterus suggests abruption; pain with shock suggests a ruptured ectopic pregnancy or a ruptured uterus in a scarred uterus. Intermittent tightening before 37 weeks is preterm labour. Lay her down and transfer.
8. **Severe pallor, breathlessness or swelling of face and hands.** Very pale palms with breathlessness mean severe anaemia (Hb below 7 g/dL) and risk of heart failure. Swelling of the face and hands with high BP means pre-eclampsia. Keep her at rest, give oxygen and refer.

## 3.5 Pre-eclampsia: recognise, treat, refer

**Pre-eclampsia** is **BP of 140/90 mmHg or more on two readings 4 hours apart after 20 weeks with proteinuria (1+ or more) or organ signs**; it is **severe** if the BP is 160/110 or more or if there are symptoms (headache, visual disturbance, epigastric pain, oliguria, convulsion). It affects about 5-8% of pregnancies and, with haemorrhage and sepsis, is a leading cause of maternal death in Nepal. Risk factors: primigravida, age under 18 or over 35, twins, diabetes, obesity, previous pre-eclampsia, chronic hypertension and kidney disease.

```svgfig label="3.3" caption="Pre-eclampsia decision algorithm for the birthing centre. Measure the BP correctly, test urine, ask about symptoms, then follow the right-hand branch. The severe branch needs magnesium sulfate loading before transfer (IV 4 g and IM 5 g in each buttock), an oral antihypertensive per protocol (for example nifedipine 10 mg), an escort with a referral note and a call ahead to the CEONC hospital. The mild branch needs weekly checks, calcium, rest and a plan for delivery at 37 weeks."
f = Fig(760, 340)
f.box(270, 8, 220, 44, "BP 140/90 or more after 20 wk\nRepeat after 4 hours", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.arrow([(380, 52), (380, 84)], color=SLATE, sw=2)
f.box(250, 84, 260, 52, "Test urine protein; ask: headache,\nblurred vision, epigastric pain, fits?", fill=SOFT, stroke=SLATE, size=10.5, bold=True)
f.arrow([(300, 136), (170, 170)], color=TEAL, sw=2, label="no", lpos=(215, 150))
f.arrow([(460, 136), (590, 170)], color=RED, sw=2, label="yes, or BP 160/110", lpos=(575, 150))
f.box(20, 170, 300, 70, "MILD / GESTATIONAL HYPERTENSION\nBP under 160/110, no symptoms\nweekly visit, calcium, rest, kick counts", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(20, 255, 300, 62, "Hospital assessment, scan, plan delivery\nat 37 weeks; teach danger signs", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.arrow([(170, 240), (170, 255)], color=TEAL, sw=2)
f.box(430, 170, 310, 70, "SEVERE PRE-ECLAMPSIA / ECLAMPSIA\nIV line, left lateral position, airway,\nMgSO4 loading dose, antihypertensive", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(430, 255, 310, 62, "REFER NOW with escort to CEONC;\nmonitor RR, reflexes, urine, BP, FHR", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.arrow([(585, 240), (585, 255)], color=RED, sw=2)
```

**Magnesium sulfate (MgSO4)** is the drug of choice to prevent and stop eclamptic fits (Pritchard or Zuspan regimens, WHO and MoHP protocol). The **loading dose** is **4 g IV** (8 mL of 50% solution diluted with saline to 20 mL, given slowly over at least 5 minutes) **plus 5 g IM into each buttock** (10 mL of 50% with 1 mL of 2% lignocaine in the same syringe). The **maintenance dose** is **5 g IM every 4 hours** into alternate buttocks, for 24 hours after birth or the last fit. Before each dose check that **respiratory rate is 16 or more, the knee (patellar) reflex is present and urine output is at least 30 mL/hour**; if not, **hold the dose** and give **calcium gluconate 1 g (10 mL of 10%) IV slowly** as the antidote.

```python
sbp, dbp = 160, 110
map_ = (sbp + 2 * dbp) / 3                       # mean arterial pressure
conc = 0.5                                       # 50% solution = 0.5 g per mL
iv_ml = 4 / conc                                 # IV loading, diluted to 20 mL
im_ml_each = 5 / conc                            # IM each buttock
im_total_ml = 2 * im_ml_each
load_g = 4 + 2 * 5
maint_ml = 5 / conc
doses_24h = 24 // 4
maint_24h_g = 5 * doses_24h
urine_4h = 30 * 4                                # at least 30 mL/h
ca_ml = 1 / 0.10                                 # calcium gluconate 10%
print(f"MAP = {map_:.1f} mmHg; loading {load_g} g: IV {iv_ml:.0f} mL (made up to 20 mL) + IM {im_ml_each:.0f} mL in each buttock ({im_total_ml:.0f} mL)")
print(f"Maintenance {maint_ml:.0f} mL (5 g) every 4 h = {doses_24h} doses = {maint_24h_g} g per 24 h; urine at least {urine_4h} mL in 4 h; antidote {ca_ml:.0f} mL of 10% calcium gluconate")
```

```text
MAP = 126.7 mmHg; loading 14 g: IV 8 mL (made up to 20 mL) + IM 10 mL in each buttock (20 mL)
Maintenance 10 mL (5 g) every 4 h = 6 doses = 30 g per 24 h; urine at least 120 mL in 4 h; antidote 10 mL of 10% calcium gluconate
```

Maya's mean arterial pressure is **126.7 mmHg**. The loading dose of **14 g** is **8 mL** of 50% solution IV (made up to 20 mL) plus **10 mL** into each buttock (**20 mL** IM). Maintenance is **10 mL (5 g)** every 4 hours (**30 g** in 24 hours), the urine must be at least **120 mL in 4 hours** and the antidote is **10 mL** of 10% calcium gluconate.

## 3.6 Eight elements of birth preparedness and complication readiness (BPCR)

BPCR is a plan made **before** labour so that no time is lost when something goes wrong. The midwife completes the plan with the woman and her family by the third visit and keeps the card with her.

1. **Skilled provider.** Choose the nurse, midwife or doctor who will attend the birth, and know her phone number. A skilled attendant reduces maternal death by finding complications in time. Home birth with a non-skilled attendant is the biggest risk.
2. **Place of birth.** Decide on a health post with a birthing centre, a BEONC or a CEONC hospital, and a back-up hospital for complications. A woman with a danger sign, a previous caesarean, short stature or twins should plan for a CEONC hospital. The Aama programme makes delivery free.
3. **Transport.** Fix a vehicle, a driver or a stretcher (*doli*) in advance, and know the road in the monsoon. Many villages in the hills are hours from the road, so waiting for labour to start loses the chance. Some local governments run an ambulance fund.
4. **Money.** Start a savings fund, using the Aama transport incentive, the mothers' group fund or a community emergency fund. Complications and newborn care cost more than a normal birth. Do not let money delay the journey.
5. **Blood donor.** Name one or two compatible donors who will go to the hospital with her. Know her blood group early. Postpartum haemorrhage can kill in two hours, and the blood bank may need a replacement donor.
6. **Companion and home support.** Choose a birth companion and someone to care for the older children and the cattle. Women who have continuous support in labour have shorter labour and fewer interventions. The companion is also a decision maker if the woman cannot decide.
7. **Danger-sign knowledge.** Teach the eight danger signs to the woman, her husband and her mother-in-law, using the card and role play. They must know that "wait and see" is not safe. FCHVs reinforce this at mothers' group meetings.
8. **Supplies for mother and baby.** Prepare a clean cloth, soap, a blade and cord tie if birth is at home, warm clothes and a cap for the baby (the *Nyano Jhola* programme gives a newborn warming set), sanitary cloths, the ANC card and citizenship papers for the Aama claim. Warmth saves newborn lives.

## Formula and fact sheet

- **ANC schedule:** Nepal 4 visits (months 4, 6, 8, 9); WHO 8 contacts (12, 20, 26, 30, 34, 36, 38, 40 weeks). IFA 180 tablets from month 4; albendazole after 12 weeks; Td two doses; Hb below 11 g/dL = anaemia.
- **Leopold's grips:** 1 fundus, 2 sides (back and limbs), 3 Pawlik (presenting part), 4 deep pelvic (engagement in fifths). FHR 110-160; 10 movements in 12 hours.
- **OGTT 75 g (IADPSG):** fasting 92, 1 h 180, 2 h 153 mg/dL. Anti-D 300 micrograms within 72 hours.
- **Pre-eclampsia:** 140/90 twice, 4 h apart + proteinuria or organ signs; severe at 160/110 or symptoms. MAP = (SBP + 2 × DBP) ÷ 3.
- **MgSO4:** load 4 g IV (8 mL) + 5 g IM each buttock (10 mL each); maintain 5 g IM 4-hourly; RR 16 or more, reflex present, urine 30 mL/h or more; antidote calcium gluconate 1 g (10 mL of 10%).
- **HMIS:** coverage = women served ÷ expected births × 100; dropout = (ANC1 - ANC4) ÷ ANC1 × 100. NDHS 2022: 4+ ANC 81%, facility birth 79%, SBA 80%, PNC within 2 days 70%.

## Chapter summary

- ANC finds and prevents problems; Nepal's protocol has four visits and WHO's eight; every visit includes BP, weight, urine, fundal height, fetal heart and counselling.
- Leopold's four grips give lie, presentation, position and engagement; FHR is 110-160 and movements are counted.
- Screen for anaemia, hypertension, proteinuria, diabetes, infections and Rh status; give IFA, Td, albendazole and calcium.
- The eight danger signs mean immediate referral; severe pre-eclampsia needs MgSO4 loading, an antihypertensive and escorted transfer.
- BPCR (provider, place, transport, money, blood donor, companion, danger-sign knowledge, supplies) turns knowledge into action; HMIS indicators show how well the system works.

## Practice

```python
exp_births, anc4 = 500, 350
m1 = anc4 / exp_births * 100                       # MCQ1 coverage
m2 = 4 / 0.5                                       # MCQ2 mL of 50% MgSO4 for 4 g
m3 = (150 + 2 * 100) / 3                           # MCQ3 MAP of 150/100
m4 = 5 * 6                                         # MCQ4 grams of maintenance MgSO4 in 24 h
map_c = (160 + 2 * 110) / 3                        # Maya
load_iv, load_im = 4 / 0.5, 2 * 5 / 0.5
urine = 30 * 4
rr_ok = 14 >= 16
print(f"MCQ1 = {m1:.0f}%; MCQ2 = {m2:.0f} mL; MCQ3 = {m3:.1f} mmHg; MCQ4 = {m4} g")
print(f"Maya: MAP {map_c:.1f}; IV {load_iv:.0f} mL; IM {load_im:.0f} mL in total; urine at least {urine} mL in 4 h; RR 14 passes check: {rr_ok}")
```

```text
MCQ1 = 70%; MCQ2 = 8 mL; MCQ3 = 116.7 mmHg; MCQ4 = 30 g
Maya: MAP 126.7; IV 8 mL; IM 20 mL in total; urine at least 120 mL in 4 h; RR 14 passes check: False
```

**MCQs (with reasons)**

1. In a ward with 500 expected births, 350 women completed four ANC visits. The coverage is: (a) 35% (b) 50% (c) 70% (d) 85%.
2. The volume of 50% magnesium sulfate for a 4 g IV loading dose is: (a) 2 mL (b) 4 mL (c) 8 mL (d) 16 mL.
3. The mean arterial pressure for 150/100 mmHg is: (a) 100.0 (b) 116.7 (c) 125.0 (d) 133.3.
4. Before each maintenance dose of magnesium sulfate the nurse must check all EXCEPT: (a) respiratory rate (b) knee reflex (c) urine output (d) blood sugar.
5. The grip that tells whether the head is engaged is: (a) first (b) second (c) third (d) fourth.

::: note Answers and rationales
**1. (c).** 350 ÷ 500 × 100 = 70%; 35% is 350 ÷ 1,000 and 85% has no basis.
**2. (c).** 4 g at 0.5 g/mL = 8 mL; 4 mL would be a 100% solution and 16 mL would be a 25% solution.
**3. (b).** (150 + 2 × 100) ÷ 3 = 116.7; adding without doubling the diastolic gives wrong answers.
**4. (d).** Magnesium toxicity shows as low respiratory rate, absent knee reflex and low urine; blood sugar is not part of the check.
**5. (d).** The deep pelvic grip, facing the feet, counts the fifths of head above the brim; the third grip finds the presenting part and its mobility only.
:::

**Short answer (3 marks): State the aims of antenatal care.** The aims are to keep the mother and fetus healthy and to find risk early: promote health and nutrition, **screen** for anaemia, hypertension, diabetes and infection, **prevent** disease with Td, iron-folic acid, calcium and albendazole, **prepare** the woman and family for birth and the newborn through a birth plan (BPCR), teach danger signs and **build trust** so that she returns for a skilled delivery and postnatal care.

**Medium answer (5 marks): Describe Leopold's grips with their purpose (Plate 3.1).** With the woman lying on her back, knees bent, bladder empty and hands warm, the midwife faces her head for the first three grips. **Grip 1 (fundal)** finds the fundal height and the part in the fundus (breech is soft and irregular, head is hard and round). **Grip 2 (lateral)** uses one hand to steady and the other to feel the sides: the back is smooth and firm, the limbs are knobby, which gives the position. **Grip 3 (Pawlik)** grasps the lower pole to identify the presenting part and whether it is movable or engaged. **Grip 4 (deep pelvic)**, facing the feet, presses down along both sides to find the fifths of head above the brim and the attitude (degree of flexion). Findings are recorded as lie, presentation, position and engagement, and then the fetal heart is counted over the back. Precautions: explain the procedure, gain consent, avoid pressure during a contraction, and do not repeat the grips often. A head that is not engaged at 38 weeks in a primigravida needs assessment of the pelvis and a scan.

**Long answer (10 marks): Maya Magar, 28, G3 P2, comes to the birthing centre at 34 weeks with severe headache and blurred vision. BP is 160/110 mmHg (repeated), urine protein 2+, pulse 98, respiratory rate 20, FHR 140, knee reflexes brisk. Calculate her MAP and the magnesium sulfate doses, and write the care plan.**

*Diagnosis and calculations.* She has **severe pre-eclampsia** (BP 160/110, proteinuria and symptoms). Her **MAP is 126.7 mmHg** ((160 + 2 × 110) ÷ 3). The **loading dose is 4 g IV (8 mL of 50% solution, diluted to 20 mL, given slowly over at least 5 minutes) plus 5 g IM into each buttock (10 mL each, with 1 mL of 2% lignocaine)**, totalling 14 g (28 mL). Maintenance is **5 g (10 mL) IM every 4 hours**, alternating buttocks. Before each dose she must have a respiratory rate of 16 or more, a present knee reflex and **at least 120 mL of urine in 4 hours**; calcium gluconate 10 mL of 10% is kept at the bedside.

*Care.* The midwife puts her on the left side in a quiet, dim room, secures an IV line, passes a urinary catheter with an hourly urine bag, pads the bed rails and keeps airway and suction ready. She gives the MgSO4 loading dose and an antihypertensive per protocol (for example oral nifedipine 10 mg), aiming at a diastolic of 90-100 mmHg and avoiding a sudden fall. She restricts IV fluids to about 80 mL an hour to avoid pulmonary oedema, records BP and FHR every 15-30 minutes, and respiratory rate, reflexes and urine hourly. She phones the CEONC hospital, writes a full referral note, sends the MgSO4 and calcium gluconate with a trained escort and informs the husband. After delivery she continues MgSO4 for 24 hours, watches for postpartum haemorrhage and fits, and counsels Maya on the risk of recurrence in a future pregnancy and on family planning.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "My head is splitting." **O:** BP 160/110, 2+ protein, brisk reflexes. | **Risk for injury (maternal)** related to seizure risk of severe pre-eclampsia. | **Seizure control:** no convulsion during transfer and labour. | Give MgSO4 4 g IV and 5 g IM each buttock (prevents seizures); quiet dim room, padded rails (lower stimuli, protect); suction ready (clears airway). | No seizure; reflexes normal. |
| **O:** MAP 126.7 mmHg, blurred vision. | **Risk for ineffective cerebral tissue perfusion** related to severe hypertension. | **Tissue perfusion:** BP 140-150 / 90-100 mmHg within 2 hours. | Antihypertensive per order, BP every 15 min (detects over-treatment); left-lateral position (improves uterine flow). | BP 148/98; headache eases. |
| **O:** RR 20, urine 40 mL/h, on MgSO4. | **Risk for ineffective breathing pattern** related to magnesium toxicity. | **Respiratory status:** RR 16 or more, reflex present, urine 30 mL/h or more. | Check RR, reflex and urine before each dose (early signs of toxicity); hold dose if abnormal; calcium gluconate 1 g IV ready (antidote). | RR 18; no toxicity. |
| **O:** FHR 140, 34 weeks, reduced placental perfusion likely. | **Risk for impaired fetal gas exchange** related to placental insufficiency. | **Fetal status:** FHR 110-160 throughout. | Count FHR every 15-30 min; refer for steroids and delivery planning (improves lung maturity and timing); left side (blood flow). | FHR normal. |
| **S:** "Will I die? Who will look after my children?" **O:** tearful, husband absent. | **Anxiety** related to threat to self and baby. | **Anxiety level:** states fears and cooperates with transfer. | Explain every step calmly (reduces fear); involve family; arrange child care (practical help); stay with her (reassures). | Calm; consents to referral. |
