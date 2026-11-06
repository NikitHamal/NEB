---
subject: Midwifery II
grade: BSc Nursing Year 3
unit: 5
title: Puerperal Complications and the High-Risk Newborn: Sepsis, Thromboembolism, Mastitis, Postpartum Mental Illness, Preterm and Low Birth Weight Care, Resuscitation, Neonatal Sepsis, Jaundice and Maternal and Perinatal Death Review
hours: 24
area: BSN 19-20 · Midwifery II · Units 14-17
---

Sarita Gurung, 22, gave birth on Monday at a district hospital in Dhading, at 34 weeks, after her waters had broken 20 hours earlier. The baby, Asha, weighed **1.8 kg**. On day 4 at home Sarita has a **temperature of 39.0 °C, a pulse of 118, a blood pressure of 98/60 and a respiratory rate of 24**. Her uterus is tender and her lochia smell foul. Asha is sleepy, feeds poorly and feels cool. This one family shows the two halves of this unit: a mother with **puerperal sepsis**, a leading preventable killer of women, and a **small, high-risk newborn** who needs warmth, feeding, infection control and perhaps resuscitation. In Nepal the neonatal mortality rate is still **21 per 1,000 live births (NDHS 2022)** and most of those deaths are due to prematurity, asphyxia and infection. A midwife who can recognise these early and act within minutes is the main reason a family returns home with both people alive.

::: key What this unit gives you
- Real images: **mastitis** with a wedge of redness, a **swollen leg in deep vein thrombosis**, **kangaroo mother care**, a **preterm baby in an incubator**, a **neonatal CPAP set**, a **jaundiced baby** and **phototherapy**; with numbered marks.
- SVG figures: the **puerperal sepsis pathway with the one-hour bundle**, the **Helping Babies Breathe golden-minute algorithm**, **Kramer's zones of jaundice** and the **MPDSR cycle** for Nepal.
- **Eight points of nursing care in puerperal sepsis**, **seven points of postnatal health education**, **eight points of care of the preterm baby** and **eight points of care in neonatal sepsis and jaundice**, each in 3-4 plain sentences, anchored in WHO, MoHP, Aama, IMNCI and the Nepal MPDSR guideline.
- Verified maths: **qSOFA, shock index, gentamicin, sepsis fluid and drip rate, enoxaparin, newborn fluids, newborn gentamicin and ampicillin, bilirubin units, weight gain**; MCQs, short, medium and long answers and a 5-column NANDA-I plan.
:::

## 5.1 Puerperal sepsis

The **puerperium** is the 6 weeks after birth. **Puerperal sepsis** (maternal sepsis) is an infection of the genital tract that starts during labour, abortion or the puerperium and spreads to cause organ dysfunction. WHO defines maternal sepsis as a life-threatening condition from infection during pregnancy, childbirth, post-abortion or the **42 days after birth**. The usual first site is the **placental bed**, a raw area the size of a plate, so the first disease is **endometritis**; it may then spread to the tubes, pelvis, peritoneum and blood.

**Causes and risk factors.** The organisms are usually mixed: **group A and group B streptococci, *Escherichia coli*, *Staphylococcus aureus*** and anaerobes such as *Bacteroides*. Risk rises with **prolonged rupture of membranes, long labour, many vaginal examinations, unclean birth practices, retained placenta or products, caesarean section, anaemia, malnutrition and trauma**. Group A streptococcus can kill within 24 hours, so a woman with high fever and a tender uterus is never watched for "just a day".

**Features.** Fever of **38 °C or more** (after the first 24 hours), chills, **fast pulse**, lower abdominal pain, a **tender, soft, larger-than-expected uterus (subinvolution)**, **foul or heavy lochia**, and later a high respiratory rate and low blood pressure. Danger signs of **sepsis** are respiratory rate of 22 or more, systolic pressure of 100 mm Hg or less, confusion, a shock index of 1.0 or more, and little urine.

```svgfig label="5.1" caption="Puerperal sepsis: pathway and the one-hour bundle. Risk factors (prolonged rupture of membranes, long labour, many vaginal examinations, retained products, caesarean) allow bacteria to enter the raw placental bed. Endometritis may spread to parametritis, pelvic abscess, peritonitis and septic shock. Recognise it early by fever, tender uterus, foul lochia, and a respiratory rate of 22 or more, systolic pressure of 100 or less or confusion (qSOFA 2 or more). Within one hour: oxygen, blood cultures, IV antibiotics, IV fluids (30 mL/kg if hypotensive), lactate or urine output, and removal of the source (retained products, abscess) by the doctor."
f = Fig(760, 330)
f.box(15, 15, 170, 60, "RISK\nPROM, long labour, many PVs,\nretained products, CS", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(210, 15, 170, 60, "ENDOMETRITIS\nfever, tender uterus,\nfoul lochia", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(405, 15, 170, 60, "SPREAD\nparametritis, pelvic abscess,\nperitonitis", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(600, 15, 145, 60, "SEPTIC SHOCK\nDIC, organ failure,\ndeath", fill=ROSE, stroke=RED, size=10.5, bold=True)
for x in (185, 380, 575): f.arrow([(x, 45), (x + 25, 45)], color=SLATE, sw=2)
f.box(15, 100, 730, 42, "SCREEN: qSOFA = respiratory rate 22 or more + systolic BP 100 or less + confusion. Score 2 or more = high risk; shock index 1.0 or more", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
names = ["O2\n(if SpO2\nbelow 94%)", "BLOOD\nCULTURES\n(before\nantibiotics)", "IV\nANTIBIOTICS\nwithin\n1 hour", "IV FLUIDS\n30 mL/kg\nif low BP", "LACTATE\nor urine\noutput\n(30 mL/h)", "SOURCE\ncontrol:\nevacuate,\ndrain"]
for i, n in enumerate(names):
    x = 15 + i * 123
    f.box(x, 165, 112, 100, n, fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(15, 282, 730, 36, "Antibiotics: ampicillin 2 g q6h + gentamicin 5 mg/kg daily + metronidazole 500 mg q8h (Nepal) or clindamycin + gentamicin (WHO)", fill=SAND, stroke=AMBER, size=10.5, bold=True)
```

**Management.** The aim is the **"sepsis bundle" within one hour**: oxygen if needed, **blood cultures** (and a high vaginal swab), **IV broad-spectrum antibiotics**, IV fluids, a measure of **lactate or hourly urine output**, and finding and treating the source. In Nepal the usual regimen is **ampicillin 2 g IV every 6 hours + gentamicin 5 mg/kg IV once daily + metronidazole 500 mg IV every 8 hours**; WHO also accepts **clindamycin 900 mg IV every 8 hours + gentamicin**. Continue until the woman is fever-free for 24-48 hours. Retained products are removed by the doctor (manual vacuum aspiration), abscesses are drained and a laparotomy is done for peritonitis. A woman with septic shock needs the high dependency or intensive care unit.

### Eight points of nursing care in puerperal sepsis

1. **Recognise early and call for help.** Take the temperature, pulse, respiratory rate and blood pressure of every postnatal woman who feels unwell. Work out the qSOFA and shock index in 1 minute. Tell the doctor at once, because the first hour decides survival.
2. **Start the sepsis bundle within one hour.** Take blood cultures before the first antibiotic dose if this does not delay it. Give the ordered IV antibiotics on time, every time. A missed dose of an antibiotic is a dangerous error in sepsis.
3. **Resuscitate with fluids and oxygen.** Put in two large IV lines and give crystalloid as ordered (for example 30 mL/kg over 3 hours if she is hypotensive). Give oxygen by mask if SpO₂ is below 94%. Record her intake and urine output every hour.
4. **Control the fever and give comfort.** Give paracetamol 1 g every 6 hours, tepid sponging and plenty of fluids. Change wet sheets and pads, and keep her warm if shivering. Pain and fever tire her, and she may be anxious about the baby.
5. **Observe the lochia and the uterus.** Describe the smell, colour and amount, and mark the fundal height daily. Foul lochia with a soft, large uterus points to endometritis or retained products. Report heavy bleeding because secondary PPH can follow.
6. **Prevent spread and protect others.** Use standard precautions, clean gloves and hand hygiene. Group A streptococcus can pass to other mothers and babies, so isolate her if possible, dispose of pads as infectious waste and keep the baby safe.
7. **Support breastfeeding and the mother-baby bond.** Most antibiotics are compatible with breastfeeding, and continuing feeds protects the baby. If the mother is too ill, help her to express milk and let the family hold the baby. Check the baby for signs of infection too.
8. **Document, report and educate.** Chart vital signs, antibiotics and fluid balance on the partograph or postnatal chart, and report to the Nepal MPDSR system if it becomes a near-miss or a death. Before discharge teach hand washing, perineal care and danger signs, and arrange a visit within 48 hours.

## 5.2 Other puerperal complications

**Venous thromboembolism (VTE).** The puerperium is the period of highest VTE risk because pregnancy raises clotting factors and slows venous flow. Risk rises after **caesarean section, immobility, obesity, age over 35, pre-eclampsia, infection, long labour, smoking and a past VTE**. **Deep vein thrombosis (DVT)** gives a **swollen, warm, painful calf on one side**, with a calf circumference at least 2-3 cm larger than the other leg. **Pulmonary embolism (PE)** gives sudden breathlessness, chest pain, fast pulse, cough, haemoptysis and collapse, and is a leading cause of maternal death in high-income countries. Management: refer, give **low molecular weight heparin** (for example enoxaparin 1 mg/kg subcutaneously every 12 hours), keep the leg raised, avoid massaging it, and arrange scan and anticoagulation for at least 3 months. Prevention: early mobilisation, good fluid intake, compression stockings and prophylactic LMWH (for example enoxaparin 40 mg once daily) for women at high risk.

**Mastitis and breast abscess.** *Staphylococcus aureus* from the baby's mouth or skin enters through a cracked nipple, usually with milk stasis. The woman has a **hot, red, wedge-shaped painful area**, flu-like fever and a hard lump. Treatment: **continue breastfeeding or expressing** (milk is safe for the baby), improve attachment, give **ibuprofen or paracetamol**, rest, and **cloxacillin 500 mg four times daily for 10-14 days** if there is fever or no improvement in 24 hours. If a **fluctuant lump** forms (abscess), the doctor drains it by needle or incision, and feeding continues from the other breast (and from the affected one if the pump is possible).

```photogrid label="5.2" cols="2" ratio="1.25" caption="Two puerperal complications. (a) Mastitis: a hot, red, wedge-shaped area on the breast with a tender hard lump; the mother keeps feeding or expressing and takes antibiotics if the fever persists. (b) Deep vein thrombosis of the right leg: the swollen, darker leg (blue arrow) is bigger than the left; a midwife measures both calves and refers at once, without massage."
@ photo id="nur12/mastitis" cap="Mastitis in a breast"
fit 1.25
focus 0.5 0.5
mark 0.72 0.15 "1"
mark 0.5 0.55 "2"
key 1 (a) Red wedge of inflamed skin
key 2 (a) Warm, stretched skin over a hard tender lump
@ photo id="nur12/dvt" cap="Deep vein thrombosis of the right leg"
fit 1.25
focus 0.5 0.62
mark 0.3 0.3 "3"
mark 0.78 0.3 "4"
key 3 (b) Swollen right calf with darkened skin (the blue arrow)
key 4 (b) Normal left leg for comparison
```

**Subinvolution and secondary PPH.** The uterus normally shrinks about **1 cm a day** and is not palpable above the pubis by about day 10-14. Subinvolution means it stays large, soft and tender with prolonged red lochia. It is usually caused by **retained placental tissue or endometritis**, sometimes a fibroid. Give uterotonics (oxytocin or oral ergometrine 0.2 mg three times daily for 2-3 days if there is no hypertension), antibiotics, and refer for ultrasound and evacuation of retained products. Secondary PPH (24 hours to 12 weeks) is explained in Unit 2.

## 5.3 Postpartum mental health and postnatal education

About half of all mothers feel tearful, anxious and irritable on days 3-5 (**baby blues**); it settles by itself within 2 weeks with rest and support. **Postpartum depression (PPD)** is different: low mood, loss of interest, poor sleep and appetite, guilt, no bond with the baby and sometimes thoughts of self-harm for more than 2 weeks. Studies in Nepal using the Edinburgh Postnatal Depression Scale (EPDS, cut-off 10 or more) report prevalence of about **17-34%**, higher with a poor family support, domestic violence, an unplanned pregnancy, a past illness, a complicated birth, baby loss and (in some studies) the birth of a girl. **Postpartum psychosis** is rare (1-2 per 1,000 births), starts within 2 weeks with confusion, hallucinations, delusions and wild mood, and is a **psychiatric emergency** because of the risk of suicide and harm to the baby; it often signals bipolar disorder.

| Condition | Onset and course | Features | Management |
|---|---|---|---|
| **Baby blues** | Day 3-5; under 2 weeks | Tearful, anxious, labile | Reassurance, sleep, support |
| **Postpartum depression** | Within weeks to a year; lasts weeks to months | Low mood, guilt, poor bonding, EPDS 10 or more | EPDS screen, counselling, mhGAP, SSRI (sertraline) if needed |
| **Postpartum psychosis** | Within 2 weeks; sudden | Delusions, hallucinations, confusion, risk to baby | Emergency referral, admission, supervise baby; psychiatrist treats |

**Screening and care.** The midwife asks two questions at every postnatal visit ("In the past 2 weeks, have you felt down or hopeless? Have you lost interest in things?") and uses the **10-item EPDS** (score 0-30). Any positive answer to **item 10 (thoughts of self-harm)** needs same-day review. Mild depression is managed with listening, problem solving and family support; moderate or severe depression with psychological therapy and an antidepressant such as **sertraline**, compatible with breastfeeding, under mhGAP. In Nepal the **TPO Nepal helpline 1166** and the district hospital psychiatric services are used; a mother who speaks of harming herself or the baby is never left alone.

### Seven points of postnatal health education

1. **Know the danger signs and come back at once.** These are heavy bleeding (a pad soaked in under an hour), fever, foul lochia, severe headache or blurred vision, calf pain or swelling, chest pain or breathlessness, red hot breast, and fits. Tell the family too, because the mother may be too weak to ask. Go to the nearest health facility without waiting for the next visit.
2. **Keep clean to prevent infection.** Wash hands with soap before touching the baby and after the toilet. Wash the perineum with clean water from front to back, change pads 4-6 times a day, and dry the stitches. Do not put cloths, herbs or ash in the vagina.
3. **Eat well and rest.** Eat extra food (dal, green vegetables, eggs, milk, fish, meat, fruit) and drink plenty of water; no foods are "forbidden" after birth. Take **iron-folic acid** as per the Nepal protocol after birth and sleep when the baby sleeps. Anaemia delays healing and raises the risk of infection.
4. **Breastfeed and look after the breasts.** Feed within one hour of birth and exclusively for 6 months, 8-12 times a day. Good attachment prevents cracked nipples and mastitis. If a breast is red and hot, continue feeding and come for treatment.
5. **Plan the next pregnancy.** Wait at least **24 months** after a live birth. Lactational amenorrhoea works only if the baby is under 6 months, fully breastfed and she has no periods; implants, an IUCD (immediate postpartum IUCD) and injections are free in Nepal. Husbands should be counselled too.
6. **Look after emotional health.** Tell her that tears and worry are common, but that low mood for more than 2 weeks, no interest in the baby or thoughts of self-harm need help. Encourage the husband and mother-in-law to share the work. Give the helpline number 1166.
7. **Attend postnatal visits and immunise the baby.** The Safe Motherhood protocol gives postnatal visits at about 24 hours, day 3, day 7 and 6 weeks (check the latest MoHP circular). Give the baby BCG, polio and other vaccines on schedule. Take the vaccination card to every visit.

## 5.4 The preterm and low birth weight baby

A baby born before **37 completed weeks** is **preterm** (extremely preterm below 28 weeks, very preterm 28 to under 32, moderate to late 32 to under 37). A **low birth weight (LBW)** baby weighs **under 2,500 g** (very low under 1,500 g, extremely low under 1,000 g). A baby can be small because it is early (preterm) or because it did not grow well (small for gestational age). The commonest causes of preterm birth are infection, **premature rupture of membranes**, multiple pregnancy, pre-eclampsia, anaemia, short interval pregnancies and maternal malnutrition. Preterm birth, birth asphyxia and infection are the main causes of neonatal death in Nepal.

**Before birth.** If birth is likely within 7 days at 24-34 weeks, and good newborn care is available, WHO (2022) recommends **antenatal corticosteroids**: **dexamethasone 6 mg IM every 12 hours for 4 doses** (or betamethasone 12 mg IM every 24 hours for 2 doses), a total of 24 mg, to mature the baby's lungs. They are not given if there is clinical infection (chorioamnionitis). Magnesium sulfate may be given for neuroprotection before 32 weeks, and a woman with PPROM gets an antibiotic.

**At birth.** Delay cord clamping for 1-3 minutes if the baby does not need resuscitation, dry, wrap and put the baby on the mother's chest in **skin-to-skin contact** with a cap on the head.

**Kangaroo mother care (KMC)** is the foundation of care. WHO (2022) recommends it as routine care for **all preterm or LBW babies**, started **as soon as possible after birth**, for **8-24 hours a day** (as close to continuous as possible for babies of 2,000 g or less). The baby, wearing only a nappy and cap, is held upright, skin to skin between the mother's breasts and tied with a cloth binder so the airway is open. KMC reduces death, hypothermia and sepsis, helps breastfeeding and weight gain, and can be continued at home. The father or another family member can also give KMC.

```photogrid label="5.3" cols="3" ratio="1.0" caption="Care of the small baby. (a) Kangaroo mother care: a newborn on the mother's chest, skin to skin, and covered with a cloth. (b) A mother with her premature baby inside an incubator: when KMC is not yet possible, the incubator gives a thermoneutral space and the mother's hands stay in contact. (c) A newborn on nasal CPAP: a prong or mask delivers positive airway pressure, and a bubble system is used in many low-resource units for respiratory distress syndrome."
@ photo id="nur12/kmc" cap="Kangaroo mother care"
fit 1.0
focus 0.65 0.5
mark 0.58 0.55 "1"
mark 0.35 0.75 "2"
key 1 (a) Baby in skin-to-skin contact on the chest of the mother
key 2 (a) Baby wrapped in a cap and cloth, head turned to one side
@ photo id="nur12/premie" cap="Mother and preterm baby in an incubator"
fit 1.0
focus 0.5 0.35
mark 0.75 0.5 "3"
mark 0.5 0.75 "4"
key 3 (b) Transparent hood of the incubator
key 4 (b) Mother leaning over the incubator to touch her baby
@ photo id="nur12/cpap" cap="Newborn on nasal CPAP"
fit 1.0
focus 0.5 0.3
mark 0.55 0.3 "5"
mark 0.55 0.75 "6"
key 5 (c) Face of the baby with the nasal prongs and tube
key 6 (c) Humidifier chamber and tubing above the cot
```

### Eight points of care of the preterm baby

1. **Keep the baby warm (prevent hypothermia).** A small baby has a large surface area and little fat, so heat is lost fast. Start KMC at once, or use a radiant warmer or incubator at 34-36 °C, and keep the room above 25 °C. A temperature below 36.5 °C is a danger; check it every 3-4 hours.
2. **Support breathing.** Position the baby with the neck slightly extended, clear the nose, and watch for grunting, chest in-drawing, fast breathing over 60 per minute or apnoea. Give oxygen only when SpO₂ is below 90% and keep it at 90-95% to avoid retinopathy of prematurity. **CPAP** is used for respiratory distress syndrome and caffeine citrate for apnoea, as the doctor orders.
3. **Feed carefully.** The best feed is the mother's own milk. Babies below 32 weeks or 1,500 g get expressed milk by NG tube or cup, babies of 32-34 weeks by cup or spoon, and those over 34 weeks may suck. Start early, increase by 10-20 mL/kg a day, and watch for vomiting, abdominal distension (necrotising enterocolitis) and aspiration.
4. **Prevent infection.** Hand hygiene is the most important step. Clean cords with chlorhexidine as per Nepal policy, avoid unnecessary handling and IV lines, and use only clean feeding equipment. Preterm babies tire and show infection only as "not doing well".
5. **Check glucose and fluids.** Small babies drop their blood sugar quickly. Feed early (within 1 hour), check glucose in at-risk babies and treat a value below **2.6 mmol/L (47 mg/dL)**. If IV fluids are needed, calculate by weight and age and avoid overload.
6. **Give vitamin K, vaccines and watch for jaundice.** Give vitamin K at birth to prevent bleeding and BCG, polio as per the schedule. Preterm babies become jaundiced more easily; check the skin colour daily and start phototherapy by the chart for gestation and age.
7. **Support the family and bonding.** The mother is often afraid and tired. Teach KMC, expressing milk, cup feeding and danger signs. Let the father take part, because a confident family means earlier discharge and better survival.
8. **Plan discharge and follow-up.** Discharge when the baby is feeding well, gaining weight on 3 days in a row, keeps the temperature in KMC, and the mother is confident. Review at 2-3 days, weekly for the first month, then monthly; check growth, anaemia, eyes (ROP screening for babies under 32 weeks or 1,500 g), hearing and development. Record in the HMIS.

## 5.5 Birth asphyxia and neonatal resuscitation

**Birth asphyxia** is failure to establish regular breathing at birth. About **1 in 10** newborns needs some help to breathe and about 1 in 20 needs ventilation, so every birth must be attended by someone able to resuscitate, with equipment ready: a clean warm towel, a **self-inflating bag with a neonatal mask (size 0 and 1)**, a suction device and a clock. The **Helping Babies Breathe (HBB)** programme, used in Nepal's skilled birth attendant training, builds on the **Golden Minute**: breathing must be started within **one minute** of birth because the brain is damaged by minutes of no oxygen. Apgar scoring at 1 and 5 minutes (heart rate, respiration, tone, reflex, colour; 0-2 each; 7-10 normal, 4-6 moderate, 0-3 severe asphyxia) describes the baby's state but **resuscitation must never wait for the Apgar score**.

```svgfig label="5.4" caption="The Helping Babies Breathe algorithm and the Golden Minute. At birth ask three questions: term? crying or breathing? good tone? If yes, give routine care: skin-to-skin, delay cord clamping, and start breastfeeding. If not, move to the warmer: dry thoroughly, remove the wet cloth and stimulate by rubbing the back; if still not breathing well, clear the airway only if it is blocked, then clamp and cut the cord, position the head and ventilate with the bag and mask at 40 breaths a minute within the Golden Minute. Check the heart rate and the chest rise; if the baby is not breathing or the heart rate is below 100, improve ventilation (reposition, reseal the mask, suction, open the mouth, squeeze harder) and call for help. If the heart rate is below 60, call for advanced help (compressions at 3:1 in an NRP-trained unit). After stable breathing give KMC and monitor."
f = Fig(760, 350)
f.box(15, 10, 730, 36, "BIRTH: term? crying or breathing? good tone?   YES = routine care (skin to skin, delay clamp, breastfeed)", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.arrow([(380, 46), (380, 60)], color=SLATE, sw=2)
st = [("DRY\nthoroughly,\nstimulate", BLUE, NAVY), ("CLEAR\nairway only\nif blocked", BLUE, NAVY), ("CLAMP and CUT\ncord; position\nhead", SAND, AMBER), ("VENTILATE\n40 breaths/min\nbag and mask", ROSE, RED), ("CHECK\nchest rise,\nheart rate", SAND, AMBER)]
for i, (t_, fc, sc) in enumerate(st):
    x = 15 + i * 148
    f.box(x, 62, 132, 74, t_, fill=fc, stroke=sc, size=10.5, bold=True)
    if i < 4: f.arrow([(x + 132, 99), (x + 148, 99)], color=SLATE, sw=2)
f.box(15, 150, 730, 30, "THE GOLDEN MINUTE: ventilation must start within 60 seconds of birth", fill=ROSE, stroke=RED, size=11, bold=True)
f.box(15, 196, 235, 70, "HEART RATE 100 OR MORE\nand breathing: stop bag,\nKMC and monitor", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(262, 196, 235, 70, "BELOW 100 or not breathing:\nimprove ventilation (MR SOP),\nand call for help", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(509, 196, 236, 70, "BELOW 60 after 30 s:\nadvanced care (compressions\n3:1, adrenaline) at a NICU", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(15, 282, 730, 56, "After resuscitation: skin to skin, glucose check, monitor temperature and breathing; record Apgar at 1 and 5 min; explain to the parents.\nIf no heart beat after 10 minutes of good ventilation, the doctor may stop and support the family", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
```

**Steps.** (1) Prepare before every birth: wash hands, check the bag and mask, warm the room and towel. (2) Dry the baby well and rub the back; this alone makes many babies cry. (3) If not breathing or gasping, **clamp and cut the cord** and move to the flat warm surface; position the head slightly extended with a roll under the shoulders. (4) **Ventilate at 40 breaths a minute** with the mask sealed over mouth and nose, watching the **chest rise**; oxygen is not routinely needed in term babies (air is started first). (5) After one minute of ventilation, check the heart rate by stethoscope or cord pulse (count for 6 s and multiply by 10). If breathing is regular and the heart rate is at least 100, stop; otherwise **improve ventilation** (mask seal, head position, suction, open the mouth, squeeze harder) and call for help.

**After resuscitation.** A baby who needed ventilation has a high risk of **hypoxic-ischaemic encephalopathy (HIE)**: poor tone, poor feeding, seizures. Keep the baby warm but not hot, start KMC when stable, check glucose every 3 hours (target above 2.6 mmol/L), watch for seizures (phenobarbital 20 mg/kg IV loading dose as prescribed), and refer to a neonatal unit. Counsel the parents honestly. Cooling therapy is limited to tertiary hospitals. In Nepal the HBB bag-and-mask skill is the single most useful newborn skill in the BEONC list, and the equipment is audited on every birthing centre inspection.

## 5.6 Neonatal sepsis, jaundice and hypoglycaemia

**Neonatal sepsis** is a bloodstream infection in the first 28 days. **Early-onset** sepsis (under 72 hours) comes from the mother's genital tract (group B streptococcus, *E. coli*, *Klebsiella*), after PPROM, maternal fever, foul liquor or a prolonged labour; **late-onset** sepsis comes from the hospital or community (unclean cord, hands, feeds, bottles). A sick newborn gives few clear signs, so IMNCI uses **Possible Serious Bacterial Infection (PSBI)**: not feeding well, convulsions, **fast breathing (60 or more a minute)**, severe chest in-drawing, **fever (37.5 °C or more)** or **low temperature (below 35.5 °C)**, movement only on stimulation, a red umbilicus with skin spread, or many pustules. A baby with any sign receives the **first dose of IM gentamicin and ampicillin (or amoxicillin) before referral** and is kept warm, with glucose, and sent with the mother. Nepal's **chlorhexidine gel (7.1% digluconate, delivering 4% chlorhexidine) for the cord**, applied once within one hour of birth under the national policy, lowers cord infection and death; avoid ash, oil, cow dung or turmeric on the stump (WHO says dry cord care is enough in clean settings).

**Neonatal jaundice** is a yellow skin and sclera because of bilirubin. **Physiological jaundice** appears after 24 hours, peaks at day 3-5 in term babies (day 5-7 in preterm) and clears by 2 weeks (3 weeks in preterm); the baby is well. **Pathological jaundice** starts within 24 hours, rises quickly (more than 5 mg/dL, or 85 µmol/L, a day), lasts over 14 days (term) or comes with dark urine, pale stool, fever or poor feeding. Causes: **haemolysis (Rh and ABO incompatibility, G6PD deficiency)**, sepsis, cephalhaematoma, infection, hypothyroidism, **biliary atresia (pale stool; refer by 2 weeks; surgery before 8 weeks)**. High bilirubin enters the brain and causes **kernicterus** (lethargy, high-pitched cry, arching, deafness, athetoid cerebral palsy). **Kramer's zones** estimate the level by how far the yellow colour has spread from head to feet, but sight underestimates, especially in darker skin; measure the serum or transcutaneous bilirubin.

```photogrid label="5.5" cols="2" ratio="1.15" caption="Jaundice and its treatment. (a) A jaundiced infant: the yellow colour spreads from the face to the trunk (Kramer zones 1-3). (b) Phototherapy: the baby lies in a cot under blue light with the eyes covered; the light converts bilirubin to a water-soluble form that the baby passes in urine and stool."
@ photo id="nur12/jaund" cap="Jaundiced infant"
fit 1.15
focus 0.5 0.4
mark 0.5 0.7 "1"
mark 0.5 0.4 "2"
key 1 (a) Yellow face and sclera (zone 1)
key 2 (a) Yellow trunk down to the umbilicus (zones 2-3)
@ photo id="nur12/photo" cap="Phototherapy unit"
fit 1.15
focus 0.5 0.45
mark 0.5 0.75 "3"
mark 0.45 0.4 "4"
key 3 (b) Blue-light lamp above the cot
key 4 (b) Baby lying in the cot under the light
```

```svgfig label="5.6" caption="Kramer's zones of jaundice. Zone 1: head and neck (bilirubin about 6 mg/dL, 100 µmol/L); zone 2: to the umbilicus (about 9 mg/dL); zone 3: to the knees (about 12 mg/dL); zone 4: to the ankles and wrists (about 15 mg/dL); zone 5: palms and soles (over 15 mg/dL, over 260 µmol/L). Press the skin with a finger in natural light to see the colour. Yellow palms and soles, or any jaundice in the first 24 hours or after 14 days, is severe jaundice in IMNCI: refer. Phototherapy uses blue light of 430-490 nm and an irradiance of at least 30 µW per cm² per nm; the baby's eyes are covered; breastfeeding continues."
f = Fig(760, 300)
bands = [("ZONE 1: head, neck", "about 6 mg/dL", MINT, TEAL), ("ZONE 2: to umbilicus", "about 9 mg/dL", SAND, AMBER), ("ZONE 3: to knees", "about 12 mg/dL", SAND, AMBER), ("ZONE 4: to ankles, wrists", "about 15 mg/dL", ROSE, RED), ("ZONE 5: palms, soles", "over 15 mg/dL", ROSE, RED)]
for i, (a, b, fl, st) in enumerate(bands):
    y = 15 + i * 54
    f.box(15, y, 250, 46, a + "\n" + b, fill=fl, stroke=st, size=10.5, bold=True)
f.circle(380, 45, 22, fill=SAND, stroke=AMBER, sw=1.8)
f.line(380, 68, 380, 150, color=AMBER, sw=14)
f.line(380, 150, 365, 240, color=AMBER, sw=9); f.line(380, 150, 395, 240, color=AMBER, sw=9)
f.line(380, 85, 345, 130, color=AMBER, sw=7); f.line(380, 85, 415, 130, color=AMBER, sw=7)
for i in range(5):
    y = 15 + i * 54 + 23
    f.arrow([(265, y), (350, [45, 100, 160, 230, 265][i])], color=SLATE, sw=1.2)
f.box(470, 15, 275, 110, "CHECK\nin natural light, press the skin;\nzone 4-5 = urgent\nmeasure serum or skin bilirubin", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(470, 140, 275, 80, "REFER if jaundice:\nunder 24 h, after 14 days,\nyellow palms and soles", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(470, 235, 275, 55, "PHOTOTHERAPY: blue light, eyes covered,\nbreastfeed, check temperature", fill=MINT, stroke=TEAL, size=10.5, bold=True)
```

**Neonatal hypoglycaemia** is a blood glucose below **2.6 mmol/L (47 mg/dL)**. It occurs in preterm, SGA, asphyxiated, septic and cold babies and in babies of diabetic mothers. Signs are jitteriness, poor feeding, lethargy, apnoea and fits. Prevention: early breastfeeding, KMC. Treatment: if the baby can suck, feed immediately and recheck in 30 minutes; if symptomatic or unable to feed, give **2 mL/kg of 10% dextrose IV over 5-10 minutes**, followed by an infusion at a **glucose infusion rate of 6-8 mg/kg/min**.

### Eight points of nursing care in neonatal sepsis and jaundice

1. **Recognise the danger signs early.** Every newborn is checked for PSBI signs: fast breathing, chest in-drawing, poor feeding, fever or cold, convulsions, lethargy and yellow palms and soles. A mother who says "the baby is not feeding well" is always believed. Early reporting saves hours.
2. **Give the first dose of antibiotics without delay.** Give IM gentamicin and ampicillin as ordered before referral and do not wait for the culture. Use the weight-based dose (gentamicin 3 mg/kg once daily under 2 kg, 5 mg/kg at 2 kg or above in the first week). Write down the time and the dose in the referral note.
3. **Keep the baby warm and give glucose.** Use KMC or a warmer for transport, wrap the baby in a cap and blanket and check the temperature. Feed or give expressed milk during transport. Check blood glucose and treat below 2.6 mmol/L.
4. **Support breathing.** Position the baby with the neck slightly extended, clear the nose, give oxygen if SpO₂ is below 90% and watch apnoea. Keep a bag and mask beside the cot. Report grunting and chest in-drawing.
5. **Give correct phototherapy.** Expose the baby, cover the eyes with a soft cover, keep the lamp at the right distance, and turn the baby every 2-3 hours. Continue breastfeeding every 2-3 hours, check temperature and hydration, and remove the cover during feeds so mother and baby can see each other. Stop when the level has fallen below the chart limit.
6. **Maintain hydration, nutrition and elimination.** Encourage frequent feeds (8-12 a day), count wet nappies (six or more a day by day 5) and stools. Jaundiced babies who feed well clear bilirubin faster. Give extra fluids only as ordered.
7. **Care for the cord, eyes and skin; prevent spread.** Wash hands before and after handling, apply chlorhexidine to the cord as per policy, and keep the nappy below the stump. Clean the eyes with sterile water, and keep phototherapy lamps and cots clean. Isolate a baby with pustules or a discharging umbilicus from others.
8. **Counsel the family and follow up.** Explain why the baby is in hospital, teach danger signs and exclusive breastfeeding, and warn against sun-drying or herbal remedies for jaundice. Review the baby 48 hours after discharge. For Rh-negative mothers give anti-D 300 mcg IM within 72 hours of a Rh-positive baby's birth to protect later pregnancies.

## 5.7 Maternal and perinatal death review, near-miss review and respectful care

A **maternal death** is the death of a woman while pregnant or within **42 days of the end of pregnancy** from any cause related to or aggravated by the pregnancy (not accidental or incidental). Nepal's **Maternal Mortality Ratio is 151 per 100,000 live births (NMMS 2021)**. A **perinatal death** is a stillbirth or an early neonatal death in the first 7 days. A **maternal near-miss** is a woman who nearly died of a complication but survived (for example eclampsia, severe PPH with hysterectomy or intensive care admission). The **Maternal and Perinatal Death Surveillance and Response (MPDSR)** system, carried out under the MoHP Family Welfare Division, treats every such event as a chance to learn without blame. Under the Nepal guideline, a facility **notifies a maternal death within 24 hours** and fills the **Maternal Death Review (MDR) form**, the **review committee meets within 72 hours** and the perinatal death review (PDR) form is submitted within 72 hours; the **FCHV** or health worker reports community deaths of women of reproductive age, and a **verbal autopsy** is done with the family.

```svgfig label="5.7" caption="The MPDSR cycle in Nepal. 1 Identify and notify: every maternal and perinatal death is reported (facility within 24 hours; the FCHV reports community deaths). 2 Review: the committee meets within 72 hours, fills the MDR or PDR form and, for a community death, does a verbal autopsy with the family. 3 Analyse: find the medical cause and the avoidable factors using the three delays (deciding to seek care, reaching the facility, receiving good care). 4 Act: recommendations are made, such as transport, blood supply, training, drugs, referral and respectful care. 5 Monitor and feed back: results go to the district and national level through DHIS2; progress is checked at the next review."
f = Fig(760, 320)
st = [("1 IDENTIFY\nand NOTIFY\n24 hours", BLUE, NAVY), ("2 REVIEW\nMDR / PDR form\nwithin 72 hours", SAND, AMBER), ("3 ANALYSE\ncause and the\nthree delays", ROSE, RED), ("4 ACT\nrecommend and\nfix the system", MINT, TEAL), ("5 MONITOR\nfeedback through\nDHIS2", BLUE, NAVY)]
for i, (t_, fc, sc) in enumerate(st):
    x = 15 + i * 148
    f.box(x, 20, 132, 80, t_, fill=fc, stroke=sc, size=10.5, bold=True)
    if i < 4: f.arrow([(x + 132, 60), (x + 148, 60)], color=SLATE, sw=2)
f.arrow([(670, 100), (670, 125), (85, 125), (85, 100)], color=SLATE, sw=1.8, dash=True)
f.box(15, 140, 235, 80, "DELAY 1\ndeciding to seek care\n(family, culture, cost)", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(262, 140, 235, 80, "DELAY 2\nreaching the facility\n(road, transport, distance)", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(509, 140, 236, 80, "DELAY 3\nreceiving good care\n(staff, blood, drugs)", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(15, 238, 730, 66, "No blame, confidential, action-oriented. The aim is to find avoidable factors and change the system.\nA near-miss review follows the same steps. The midwife supplies facts, charts and the partograph.", fill=MINT, stroke=TEAL, size=10.5, bold=True)
```

**Respectful maternity care (RMC).** Every woman has the right to give birth with dignity. The **Safe Motherhood and Reproductive Health Rights Act 2075** and the NNC Code of Ethics support seven rights: **freedom from harm and ill-treatment, information and informed consent, privacy and confidentiality, dignity and respect, equal care without discrimination, timely care without delay, and freedom to choose** (companion, position, pain relief). Disrespect and abuse in facilities keep women away and cause delay 1 for the next woman. The midwife also records near-miss events, counsels bereaved parents, and takes part in the review with an honest account.

## 5.8 Calculations

Sepsis fluid is **30 mL/kg** over 3 hours. A **qSOFA** score counts one point each for respiratory rate 22 or more, systolic BP 100 or less and altered mentation. The **shock index** is pulse ÷ systolic BP. Newborn fluids are **mL/kg/day × weight**, divided by the feeds (8 three-hourly feeds); a microdrip set gives 60 drops/mL, so mL/h equals drops/min. **Bilirubin**: mg/dL × 17.1 = µmol/L. The **glucose infusion rate** (GIR, mg/kg/min) with 10% dextrose (100 mg/mL) is mL/h × 100 ÷ (60 × weight). Sarita weighs 58 kg and Asha 1.8 kg.

```python
import math
kg, pulse, sbp, dbp, rr = 58, 118, 98, 60, 24
qsofa = (rr >= 22) + (sbp <= 100) + 0               # alert, so no point for mentation
si = pulse / sbp
mapv = (sbp + 2 * dbp) / 3
gent = 5 * kg
amp_day = 2 * (24 // 6)
metro_day = 500 * (24 // 8)
fluid = 30 * kg
ml_h = fluid / 3
gtt = ml_h / 60 * 15
enox = 1 * kg
print(f"Sarita: qSOFA {qsofa}; shock index {si:.2f}; MAP {mapv:.1f}; gentamicin {gent} mg; ampicillin {amp_day} g/day; metronidazole {metro_day} mg/day")
print(f"Sepsis fluid {fluid} mL over 3 h = {ml_h:.0f} mL/h = {gtt:.0f} gtt/min (15 gtt/mL); enoxaparin 1 mg/kg = {enox} mg every 12 h if VTE")
w = 1.8
fl_day = 120 * w
feed = fl_day / 8
iv_h = fl_day / 24
b_gent = 3 * w
b_amp = 50 * w
steroid = 6 * 4
print(f"Asha: day 4 fluid {fl_day:.0f} mL/day = {feed:.0f} mL per 3-hourly feed = {iv_h:.0f} mL/h IV ({iv_h:.0f} gtt/min microdrip)")
print(f"Asha: gentamicin 3 mg/kg = {b_gent:.1f} mg once daily; ampicillin 50 mg/kg = {b_amp:.0f} mg every 12 h ({2 * b_amp:.0f} mg/day); dexamethasone course = {steroid} mg")
gain = 15 * w
days = math.ceil(200 / gain)
bol = 2 * w
gir_ml = 6 * w * 60 / 100
print(f"Weight gain 15 g/kg/day = {gain:.0f} g/day; {days} days to gain 200 g (1.8 kg to 2.0 kg)")
print(f"Hypoglycaemia: 10% dextrose bolus 2 mL/kg = {bol:.1f} mL; GIR 6 mg/kg/min = {gir_ml:.1f} mL/h of 10% dextrose")
print(f"Bilirubin: 15 mg/dL = {15 * 17.1:.0f} umol/L; 260 umol/L = {260 / 17.1:.1f} mg/dL")
print(f"HBB: 40 breaths/min = one breath every {60 / 40:.1f} s; Apgar 1 min = {1 + 1 + 1 + 1 + 0}, 5 min = {2 + 2 + 1 + 1 + 1}")
```

```text
Sarita: qSOFA 2; shock index 1.20; MAP 72.7; gentamicin 290 mg; ampicillin 8 g/day; metronidazole 1500 mg/day
Sepsis fluid 1740 mL over 3 h = 580 mL/h = 145 gtt/min (15 gtt/mL); enoxaparin 1 mg/kg = 58 mg every 12 h if VTE
Asha: day 4 fluid 216 mL/day = 27 mL per 3-hourly feed = 9 mL/h IV (9 gtt/min microdrip)
Asha: gentamicin 3 mg/kg = 5.4 mg once daily; ampicillin 50 mg/kg = 90 mg every 12 h (180 mg/day); dexamethasone course = 24 mg
Weight gain 15 g/kg/day = 27 g/day; 8 days to gain 200 g (1.8 kg to 2.0 kg)
Hypoglycaemia: 10% dextrose bolus 2 mL/kg = 3.6 mL; GIR 6 mg/kg/min = 6.5 mL/h of 10% dextrose
Bilirubin: 15 mg/dL = 256 umol/L; 260 umol/L = 15.2 mg/dL
HBB: 40 breaths/min = one breath every 1.5 s; Apgar 1 min = 4, 5 min = 7
```

## Formula and fact sheet

- **Maternal sepsis:** within 1 hour, cultures, IV antibiotics (ampicillin 2 g q6h + gentamicin 5 mg/kg + metronidazole 500 mg q8h), fluids 30 mL/kg if hypotensive; qSOFA 2 or more; shock index 1.0 or more. **DVT:** unilateral swollen calf; LMWH; no massage. **Mastitis:** keep feeding; cloxacillin 500 mg QID for 10-14 days.
- **PPD:** EPDS 10 or more; item 10 positive = urgent. **Psychosis:** within 2 weeks; emergency. **Helpline 1166.** **Postnatal visits:** 24 h, day 3, day 7, 6 weeks (check the circular).
- **Preterm** under 37 weeks; **LBW** under 2,500 g. **Dexamethasone** 6 mg IM q12h × 4 at 24-34 weeks. **KMC** 8-24 h/day, as soon as possible after birth. Hypoglycaemia below 2.6 mmol/L; 2 mL/kg of 10% dextrose.
- **HBB:** dry, stimulate, clamp, ventilate **40 breaths/min** in the Golden Minute; heart rate below 100 improve ventilation. **Apgar** 7-10 normal; **never wait for it.**
- **Neonatal sepsis (PSBI):** fast breathing 60 or more, temperature 37.5 or more or below 35.5, convulsions; first dose gentamicin (3 mg/kg under 2 kg, 5 mg/kg at 2 kg or more) and ampicillin 50 mg/kg q12h, then refer. **Jaundice:** under 24 h, over 14 days, palms and soles; 1 mg/dL = 17.1 µmol/L.
- **MPDSR:** notify 24 h, review 72 h, three delays. **NMR 21** (NDHS 2022); **MMR 151** (NMMS 2021).

## Chapter summary

- Puerperal sepsis is found by fever, a tender uterus, foul lochia and the qSOFA; the one-hour bundle with antibiotics and fluids saves lives, and the other puerperal problems (DVT, mastitis, subinvolution, depression and psychosis) need early recognition and referral.
- Postnatal education covers danger signs, hygiene, food, breastfeeding, family planning, mental health and visits.
- The preterm or LBW baby needs warmth with KMC, breathing and feeding support, infection control, glucose, vitamin K and a careful discharge plan; antenatal steroids help at 24-34 weeks.
- The Golden Minute of HBB (dry, clamp, ventilate at 40 per minute) is the key newborn skill.
- Neonatal sepsis is found by IMNCI PSBI signs, jaundice by Kramer's zones and the danger rules, and both are treated early with first-dose antibiotics, phototherapy and feeding.
- The MPDSR cycle and respectful maternity care turn every death and near-miss into learning.

## Practice

```python
mcq1 = 30 * 52                                        # MCQ1 mL sepsis fluid, 52 kg
mcq2 = 3 * 1.6                                        # MCQ2 mg gentamicin, 1.6 kg, first week
mcq3 = 20 * 17.1                                      # MCQ3 umol/L for 20 mg/dL
mcq4 = 20 * 2.8                                       # MCQ4 mg phenobarbital loading dose
mcq5 = 100 * 2.4 / 8                                  # MCQ5 mL per feed, day 3, 2.4 kg
mcq6 = 60 / 40                                        # MCQ6 seconds per breath
print(f"MCQ1 = {mcq1} mL; MCQ2 = {mcq2:.1f} mg; MCQ3 = {mcq3:.0f} umol/L; MCQ4 = {mcq4:.0f} mg; MCQ5 = {mcq5:.0f} mL; MCQ6 = {mcq6:.1f} s")
```

```text
MCQ1 = 1560 mL; MCQ2 = 4.8 mg; MCQ3 = 342 umol/L; MCQ4 = 56 mg; MCQ5 = 30 mL; MCQ6 = 1.5 s
```

**MCQs (with reasons)**

1. A hypotensive woman with sepsis weighs 52 kg. Crystalloid 30 mL/kg is: (a) 1,040 mL (b) 1,560 mL (c) 1,820 mL (d) 2,600 mL.
2. A 1.6 kg baby in the first week has sepsis. Gentamicin 3 mg/kg once daily is: (a) 0.48 mg (b) 4.8 mg (c) 8.0 mg (d) 16 mg.
3. A baby's bilirubin is 20 mg/dL. In µmol/L this is about: (a) 117 (b) 200 (c) 342 (d) 400.
4. A 2.8 kg baby with seizures after asphyxia gets a phenobarbital loading dose of 20 mg/kg. The dose is: (a) 14 mg (b) 28 mg (c) 56 mg (d) 112 mg.
5. A 2.4 kg baby on day 3 needs 100 mL/kg/day in 8 feeds. Volume per feed: (a) 24 mL (b) 30 mL (c) 36 mL (d) 240 mL.
6. HBB ventilation at 40 breaths per minute means one breath every: (a) 0.67 s (b) 1.0 s (c) 1.5 s (d) 2.0 s.

::: note Answers and rationales
**1. (b).** 30 × 52 = 1,560 mL over 3 hours. 1,040 mL is 20 mL/kg and 1,820 mL is 35 mL/kg.
**2. (b).** 3 × 1.6 = 4.8 mg. The 5 mg/kg dose (8.0 mg) is for babies of 2 kg or more, and 16 mg would be 10 mg/kg, a toxic overdose for a small baby.
**3. (c).** 20 × 17.1 = 342 µmol/L, a level at which exchange transfusion may be considered by the chart. 117 µmol/L is 6.8 mg/dL.
**4. (c).** 20 × 2.8 = 56 mg IV slowly as prescribed. 28 mg is 10 mg/kg and 112 mg is 40 mg/kg.
**5. (b).** 100 × 2.4 = 240 mL a day ÷ 8 = 30 mL. 240 mL is the whole day's volume.
**6. (c).** 60 ÷ 40 = 1.5 s per breath, so a breath about every second and a half. 1.0 s gives 60 breaths a minute, too fast for the newborn.
:::

**Short answer (3 marks): Define kangaroo mother care and list its benefits.** KMC is early, prolonged and continuous skin-to-skin contact between mother (or another family member) and a preterm or LBW baby, with exclusive breastfeeding and early discharge. The baby wears only a cap and nappy and is tied upright against the chest. WHO (2022) recommends it from birth for 8-24 hours a day. Benefits: it prevents hypothermia, improves breathing and heart rate, supports breastfeeding, reduces sepsis and death and builds bonding.

**Short answer (3 marks): Differentiate baby blues, postpartum depression and postpartum psychosis.** Baby blues starts on day 3-5, lasts under 2 weeks and needs only support. Postpartum depression lasts over 2 weeks with low mood, guilt and poor bonding (EPDS 10 or more) and needs counselling, mhGAP care and sometimes sertraline. Postpartum psychosis begins in the first 2 weeks with delusions, hallucinations and confusion and is an emergency needing psychiatric admission and supervision of the baby.

**Medium answer (5 marks): Describe the steps of newborn resuscitation by Helping Babies Breathe (Figure 5.4).** HBB works within the **Golden Minute**. Before birth wash hands, check the bag and mask, and warm the room. At birth ask: term, crying, good tone? If yes, give routine care (skin-to-skin, delayed cord clamping, breastfeeding). If not, **dry thoroughly and stimulate** by rubbing the back, and remove the wet cloth. If the baby is still not breathing, **clamp and cut the cord**, place the baby on a flat warm surface with the head slightly extended, and **ventilate with a bag and mask at 40 breaths a minute**, watching the chest rise. After about a minute check the heart rate (stethoscope or cord, count 6 seconds × 10). If it is 100 or more and the baby breathes, stop the bag. If not, **improve ventilation**: reposition the head, reseal the mask, suction, open the mouth and squeeze harder, then call for help. If the heart rate is below 60, advanced care is needed. After recovery, give skin-to-skin contact, check temperature and glucose, and record the Apgar at 1 and 5 minutes. Do not wait for the Apgar score to begin. Inform the parents. If there is no heartbeat after 10 minutes of good ventilation, the doctor may stop.

**Long answer (10 marks): Sarita Gurung, 22, gave birth at 34 weeks after 20 hours of ruptured membranes. On day 4 she has T 39.0 °C, pulse 118, BP 98/60, RR 24, a tender uterus and foul lochia; her 58 kg body needs fluids. Her baby Asha (1.8 kg, day 4) is sleepy, cool and feeding poorly. Calculate and write the nursing care plan.**

*Calculations.* Sarita's **qSOFA is 2** (respiratory rate 24 and systolic 98) and her **shock index is 1.20** (118 ÷ 98), so she has **puerperal sepsis with early shock**. Crystalloid 30 mL/kg is **1,740 mL over 3 hours = 580 mL/h = 145 drops/min** with a 15 drops/mL set. Gentamicin 5 mg/kg is **290 mg** once daily, with ampicillin 2 g every 6 hours (8 g a day) and metronidazole 500 mg every 8 hours. For Asha, the day 4 fluid of 120 mL/kg is **216 mL a day = 27 mL per three-hourly feed**; gentamicin 3 mg/kg is **5.4 mg** daily and ampicillin 50 mg/kg is **90 mg** every 12 hours.

*Management.* The midwife calls the doctor and opens the sepsis bundle: she gives oxygen if SpO₂ is below 94%, takes blood cultures and a high vaginal swab, starts the antibiotics within one hour and the fluids, inserts a urinary catheter for hourly output (aim for 30 mL/h or more), and gives paracetamol. The doctor examines for retained products (ultrasound, manual vacuum aspiration) and decides on referral to the CEONC if she is worse. The midwife observes the lochia and uterus, takes vital signs every 15 minutes and later hourly, prevents spread with hand hygiene and encourages expressed milk. Asha is a PSBI case (poor feeding, cold, sleepy): she receives the first dose of gentamicin and ampicillin, is placed in KMC to rewarm (target above 36.5 °C), has a glucose check (treat below 2.6 mmol/L), is fed with expressed milk by cup or tube, and is admitted to the newborn unit. The mother is counselled on danger signs, family planning and postnatal depression, and the event is reported in the MPDSR as a near-miss if she nearly dies.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "I am burning and shivering." **O:** T 39.0 °C, pulse 118, foul lochia | **Hyperthermia** related to endometritis | **Thermoregulation:** temperature below 37.5 °C in 24 h | Antibiotics within 1 h, paracetamol 1 g q6h, tepid sponging, fluids (treat cause, reduce heat) | T 37.2 °C on day 6 |
| **O:** BP 98/60, RR 24, SI 1.20, qSOFA 2 | **Risk for shock** related to sepsis | **Circulation status:** systolic BP above 100, urine at least 30 mL/h | Two IV lines, 1,740 mL crystalloid, oxygen, hourly output, vital signs every 15 min (restores perfusion) | BP 110/70, urine 45 mL/h |
| **S:** "My stomach hurts." **O:** tender uterus, grimacing | **Acute pain** related to inflammation of the uterus | **Pain level:** score 3 or less out of 10 | Paracetamol, comfortable position, explain, reassess in 1 h (pain raises pulse and anxiety) | Pain 2/10 |
| **O:** Asha 1.8 kg, T 35.9 °C, cool, sleepy | **Risk for hypothermia (neonatal)** related to prematurity | **Thermoregulation neonate:** 36.5-37.5 °C in 2 h | KMC or warmer, cap, dry wrap, temperature every 3 h (prevents cold stress and hypoglycaemia) | T 36.8 °C |
| **S:** "She will not suck." **O:** poor feeding, glucose borderline | **Ineffective breastfeeding** and **risk for unstable blood glucose** | **Breastfeeding establishment:** feeds 8 times a day; glucose above 2.6 mmol/L | Expressed milk by cup, 27 mL per feed, check glucose, KMC, teach expressing (small babies need milk and sugar) | Takes 27 mL; glucose 3.2 |
| **S:** "Will my baby die?" **O:** crying, family afraid | **Anxiety** related to sick mother and baby | **Anxiety self-control:** states plan, rests, has support | Explain in Nepali, involve husband, let her stay with baby, refer for PPD screen (fear lowers milk and bonding) | Calmer; EPDS arranged |
