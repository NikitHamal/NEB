---
subject: Child Health Nursing
grade: BSc Nursing Year 3
unit: 2
title: The Newborn and Neonatal Disorders: Assessment, Respiratory Distress, Birth Injuries and Congenital Anomalies
hours: 22
area: BSN 21-22 · Child Health Nursing · Units 4-7
---

At a district hospital in Dolakha, baby **Anju** is born at term, weighing **2.9 kg**. The midwife sees a **gap in the upper lip and the roof of the mouth (bilateral cleft lip and palate)**. Anju cries well, but milk runs from her nose and she chokes when she sucks. Her mother is silent and ashamed. In the next bed, a preterm boy, **Sunil (30 weeks, 1.4 kg)**, is grunting and has chest retractions. Two babies, two different needs: one for **feeding and family support**, the other for **breathing support**. This unit teaches how to examine a newborn, manage respiratory distress and care for the common congenital anomalies.

::: key What this unit gives you
- Real images: **spina bifida** (a photograph with its cross-section), **cleft lip repair**, **clubfoot in Ponseti casts** and a **child with Down syndrome from Nepal**; each with numbered marks.
- SVG figures: the **respiratory distress syndrome pathway** and the **congenital heart disease map**, plus the **Silverman-Anderson scoring table**.
- **Eight points of nursing care of a baby with a congenital anomaly**, **seven points of prevention and parent education** and **eight points of care in neonatal respiratory distress**, each in 3-4 plain sentences, anchored in MoHP, NIP, Aama, NNC Code of Ethics and Nepal newborn care.
- Verified maths: **weight loss percentage, Silverman score, surfactant, caffeine and fluid doses, cleft feeding volumes, pulse-oximetry screening**; MCQs, short, medium and long answers and a 5-column NANDA-I plan.
:::

## 2.1 Assessment and routine care of the newborn

**Classification.** By gestation: **preterm** (below 37 weeks), **term** (37-42 weeks) and **post-term** (over 42 weeks). By weight: **low birth weight (LBW)** below 2,500 g, **very low (VLBW)** below 1,500 g and **extremely low (ELBW)** below 1,000 g. By growth: **small for gestational age (SGA)** below the 10th centile, appropriate (AGA) or large (LGA, above the 90th). The gestational age is found from the last menstrual period, early ultrasound or the **new Ballard score** (neuromuscular and physical signs).

**Normal values.** Respiratory rate **40-60/min**, heart rate **120-160/min**, axillary temperature **36.5-37.5 °C**, SpO₂ 95% or more. Birth weight **falls by 5-10% in the first 3-4 days** (fluid shift) and is **regained by 10-14 days**; weight loss over 10% needs a feeding check. Meconium passes within 24-48 hours and urine within 24 hours.

**Essential newborn care in Nepal** follows the MoHP newborn care package: **dry and wrap, skin-to-skin on the mother's chest, delayed cord clamping (1-3 minutes), a single application of 7.1% chlorhexidine to the cord stump as per the Nepal protocol, breastfeeding within the first hour, vitamin K 1 mg IM (0.5 mg if under 1.5 kg), weighing, eye care, and a head-to-toe examination**. Keep the baby warm (room 25-28 °C), delay the bath for 24 hours, and give no pre-lacteal feeds. Teach the mother the **danger signs**: not feeding, fits, fast breathing (60 or more), chest indrawing, fever or cold, yellow soles, and a red, discharging cord.

**Head-to-toe examination.** Look at the colour and cry; measure head circumference; feel the fontanelles and sutures; inspect the face and palate with a clean gloved finger; check the eyes (red reflex), ears, neck and clavicles; count the fingers and toes; listen to the heart and lungs; feel the abdomen and femoral pulses; look at the anus, genitals and spine; test the **Moro, rooting, sucking and grasp** reflexes; and check the hips (Barlow and Ortolani).

## 2.2 Neonatal respiratory distress

**Respiratory distress syndrome (RDS, hyaline membrane disease)** is the commonest breathing problem in a preterm baby. The lung of a baby below 34 weeks makes too little **surfactant**, the fatty film that lowers surface tension in the alveoli. Without it the alveoli collapse at the end of each breath, the lungs stiffen, oxygen exchange falls and the baby tires. The signs begin within hours: **fast breathing, grunting, nasal flaring, chest retractions and cyanosis**. The chest X-ray shows a **ground-glass appearance with air bronchograms**.

```svgfig label="2.1" caption="Respiratory distress syndrome. Prematurity (and maternal diabetes or caesarean birth without labour) reduces surfactant, so the alveoli collapse; the baby grunts to keep pressure in the lungs. Treatment breaks the chain at four points: antenatal steroids before birth, early CPAP, surfactant by thin tube and caffeine to prevent apnoea."
f = Fig(760, 320)
f.box(15, 15, 170, 62, "LOW SURFACTANT\npreterm below 34 wk,\ndiabetic mother", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(210, 15, 170, 62, "ALVEOLI COLLAPSE\nhigh surface tension,\nstiff lungs", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(405, 15, 170, 62, "HYPOXIA, CO2 RISE\ncyanosis, acidosis,\ntiring baby", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(600, 15, 145, 62, "SIGNS\ngrunt, flaring,\nretractions", fill=ROSE, stroke=RED, size=10.5, bold=True)
for x in (185, 380, 575): f.arrow([(x, 46), (x + 25, 46)], color=SLATE, sw=2)
f.box(15, 105, 730, 36, "TREATMENT: break the chain at four points", fill=BLUE, stroke=NAVY, size=11.5, bold=True)
tr = ["BEFORE BIRTH\nantenatal steroids\n24-34 weeks\n(dexamethasone 6 mg\nIM q12h x 4)", "EARLY CPAP\nbubble CPAP\n5-6 cm water,\nstart in the\nfirst hour", "SURFACTANT\nporactant 200 mg/kg\nfirst dose by\nthin tube or INSURE", "SUPPORT\nwarmth, glucose,\ncaffeine 20 mg/kg,\nSpO2 90-95%,\ngentle handling"]
for i, s in enumerate(tr):
    f.box(15 + i * 184, 160, 175, 120, s, fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(15, 290, 730, 24, "Avoid too much oxygen: SpO2 above 95% in a preterm baby risks retinopathy of prematurity", fill=SAND, stroke=AMBER, size=10.5, bold=True)
```

**Other causes.** **Transient tachypnoea of the newborn (TTN)** follows caesarean birth or late preterm birth, because fetal lung fluid clears slowly; the baby is fast breathing but improves within 24-72 hours. **Meconium aspiration syndrome** affects term and post-term babies who pass meconium before birth; the baby is covered in green liquor, has a barrel chest and may develop **persistent pulmonary hypertension**. **Birth asphyxia, pneumonia and sepsis, pneumothorax, diaphragmatic hernia and congenital heart disease** also cause distress. **Apnoea of prematurity** is a pause of over 20 seconds or a shorter pause with bradycardia (below 100) or cyanosis; it is treated with stimulation and **caffeine citrate**.

**Assessment by the Silverman-Anderson score.** The nurse scores five signs: **upper chest movement (synchronised, lag, see-saw), lower chest retraction, xiphoid retraction, nasal flaring and expiratory grunt**, each 0 (none), 1 (mild) or 2 (marked). **0 = no distress, 1-3 = mild, 4-6 = moderate, 7 or more = severe distress with impending respiratory failure**. The score is repeated every 1-2 hours so that trends are seen early. The **IMNCI** signs for referral are fast breathing of 60 or more, severe chest indrawing, grunting and central cyanosis.

| Sign | 0 | 1 | 2 |
|---|---|---|---|
| Upper chest | Rises with abdomen | Lags behind abdomen | See-saw breathing |
| Lower chest retraction | None | Just visible | Marked |
| Xiphoid retraction | None | Just visible | Marked |
| Nasal flaring | None | Minimal | Marked |
| Expiratory grunt | None | Heard with stethoscope | Heard with the naked ear |

### Eight points of nursing care in neonatal respiratory distress

1. **Recognise and score early.** Count the respiratory rate for a full minute, look for grunting, flaring and retractions, and use the Silverman-Anderson score every 1-2 hours. Call the doctor at once if the score rises. Early recognition prevents respiratory failure.
2. **Keep the airway open and give oxygen or CPAP.** Place the baby supine with a small shoulder roll so that the neck is slightly extended, and suction gently only if secretions are seen. Give oxygen or bubble CPAP as ordered, aiming for SpO₂ **90-95%** in preterm babies. Too much oxygen can cause blindness (retinopathy of prematurity).
3. **Keep the baby warm.** Use a radiant warmer, an incubator or kangaroo care, and check the temperature every 3 hours. A cold baby uses more oxygen and makes the distress worse. Aim for 36.5-37.5 °C.
4. **Give the ordered medicines on time.** These include surfactant, caffeine, antibiotics (ampicillin and gentamicin) and glucose. Check the dose by weight with another nurse. Calculation errors are the commonest drug error in newborns.
5. **Give fluids and nutrition carefully.** Start IV 10% dextrose at the ordered volume (for example 60-80 mL/kg/day on day 1-2) and begin small expressed breast milk feeds by tube when stable. Too much fluid worsens lung oedema. Record intake and output.
6. **Reduce handling and noise.** Cluster the care, speak softly and avoid heel pricks and suctioning that are not needed. Stress raises oxygen demand. Rest is treatment.
7. **Prevent infection.** Wash hands before and after touching the baby, use clean equipment for suction and CPAP prongs, and keep the baby away from visitors with cough. Infection is a major cause of late deaths in the neonatal unit.
8. **Support the parents.** Explain the machines in Nepali and let the mother touch and express milk for the baby. Parents of a baby in a NICU feel afraid and guilty. Their calm cooperation helps recovery and kangaroo care later.

## 2.3 Birth injuries and other newborn problems

| Condition | Key facts | Nursing care |
|---|---|---|
| **Caput succedaneum** | Soft, pitting scalp swelling present **at birth**, **crosses suture lines**, gone in 2-3 days | Reassure; no treatment |
| **Cephalhaematoma** | Blood under the periosteum, appears **after 12-24 hours**, **does not cross sutures**, resolves in weeks; may cause jaundice | Do not aspirate; watch bilirubin; reassure |
| **Erb's palsy** | C5-C6 brachial plexus injury after shoulder dystocia; arm hangs, adducted and internally rotated ("waiter's tip") | Gentle positioning, physiotherapy after 7-10 days, refer if no recovery by 3 months |
| **Fractured clavicle** | Crepitus, absent Moro on one side; heals in 2-3 weeks | Handle gently, pin sleeve to chest, reassure |
| **Necrotising enterocolitis (NEC)** | Preterm; feed intolerance, **distended abdomen, bloody stool**, lethargy; X-ray shows gas in the bowel wall | Nil by mouth, NG decompression, IV fluids and antibiotics, refer to a surgeon |
| **Neonatal seizures** | Subtle (lip smacking, cycling, apnoea) or clonic; causes are hypoxic injury, hypoglycaemia, infection, low calcium | Protect airway, check glucose, give phenobarbital 20 mg/kg as ordered, find the cause |

## 2.4 Congenital anomalies

A **congenital anomaly** is a structural or functional defect present at birth. About **3% of babies** have a major anomaly, and in Nepal these are a growing cause of neonatal death as infections fall. Causes are **genetic (chromosome or single gene), infections (rubella, CMV, toxoplasma, syphilis), drugs (valproate, alcohol, thalidomide), maternal diabetes, folic acid lack, radiation, and consanguinity**.

**Neural tube defects (NTD).** Failure of the neural tube to close by day 28 gives **anencephaly** (fatal), **encephalocele** and **spina bifida**. In **myelomeningocele** the sac contains cord and nerves; legs are weak, the bladder and bowel are paralysed, and **80% develop hydrocephalus**. Cover the sac with sterile saline-soaked non-adherent gauze and clingfilm, nurse the baby **prone or on the side**, avoid pressure and latex, and refer for surgery within 48-72 hours. **Hydrocephalus** has a fast-growing head, a bulging fontanelle, **setting-sun eyes** and irritability; the treatment is a **ventriculoperitoneal shunt**.

**Cleft lip and palate** occur in about 1 in 700 births. They cause **feeding trouble, nasal regurgitation, ear infections, speech and dental problems**. Breastfeeding is possible with a cleft lip; for a cleft palate use a long soft teat, a squeezable bottle, a cup or spoon, feed **upright** and burp often. The **rule of 10** is a guide for lip repair: **age 10 weeks (about 3 months), weight 10 lb (4.5 kg), haemoglobin 10 g/dL**. Palate repair is done at **9-12 months**, before speech begins.

**Clubfoot (CTEV)** is a foot turned in and down (equinus, varus, adduction). The **Ponseti method** starts in the first 1-2 weeks: gentle manipulation and a long-leg cast changed **weekly for 5-6 weeks**, a small Achilles tenotomy, then **boots on an abduction bar for 23 hours a day for 3 months and then at night until 4-5 years**. Low-cost Ponseti services exist in Nepal (for example CURE Hospital, Banepa); ask the district hospital for the current referral list. **Developmental dysplasia of the hip (DDH)** is picked up by the **Barlow (dislocates) and Ortolani (relocates) tests**, and is treated in a **Pavlik harness**.

**Down syndrome (trisomy 21)** gives a flat face, **upward-slanting eyes**, epicanthic folds, a single palmar crease, low tone and a protruding tongue. The risk rises with age (about 1 in 1,000 at 30 and 1 in 100 at 40). Look for **heart disease (40-50%), duodenal atresia, hypothyroidism, hearing loss and later leukaemia**. Care is early stimulation, speech therapy, vaccines on time and a loving school place. The Nepal Act on Rights of Persons with Disabilities 2074 protects these children.

```photogrid label="2.2" cols="4" ratio="1.0" caption="Common congenital anomalies. (a) Spina bifida: the photograph with a cross-section that shows the cord and meninges in the open sac. (b) Repair of a cleft lip in an infant: the surgeon is closing the lip, with the tube and tape fixed to the face. (c) Bilateral clubfoot in Ponseti casts: the feet are held out in the corrected position. (d) A Nepali child with Down syndrome brushing his teeth in an oral health activity."
@ photo id="nur13/sb" cap="Spina bifida (open defect)"
fit 1.0
focus 0.5 0.5
mark 0.78 0.35 "1"
key 1 (a) Open sac on the lower back
@ photo id="nur13/cleft" cap="Cleft lip surgery on an infant"
fit 1.0
focus 0.4 0.5
mark 0.45 0.55 "2"
key 2 (b) Repair of the lip with fine sutures
@ photo id="nur13/ctev" cap="Clubfoot in Ponseti casts"
fit 1.0
focus 0.5 0.5
mark 0.4 0.5 "3"
key 3 (c) Casts hold the corrected foot position
@ photo id="nur13/downnp" cap="Child with Down syndrome, Nepal"
fit 1.0
focus 0.5 0.6
mark 0.5 0.62 "4"
key 4 (d) Flat face and upward-slanting eyes
```

**Congenital heart disease (CHD)** occurs in about 8 per 1,000 births. **Acyanotic** defects (left-to-right shunt) are the **ventricular septal defect (VSD, the most common)**, atrial septal defect, **patent ductus arteriosus (PDA, continuous machinery murmur)**, and coarctation. **Cyanotic** defects (right-to-left shunt) include **tetralogy of Fallot (TOF)**, the commonest cyanotic lesion beyond infancy (VSD, pulmonary stenosis, overriding aorta, right ventricular hypertrophy), and **transposition of the great arteries**, the commonest in the newborn. In a **"tet spell"** the child turns blue and cries: place in the **knee-chest position**, give oxygen, calm, and give morphine or propranolol as ordered. **Pulse-oximetry screening** at 24 hours measures the right hand and one foot: **pass if both are 95% or more and the difference is 3 points or less**. Prostaglandin E1 keeps the duct open in duct-dependent lesions.

```svgfig label="2.3" caption="Congenital heart disease map. Acyanotic defects send blood from left to right and cause breathlessness and failure to thrive; cyanotic defects send blue blood from right to left and cause cyanosis, clubbing and squatting. A pass in pulse-oximetry screening needs a right hand and foot SpO2 of 95% or more with a difference of 3 points or less."
f = Fig(760, 320)
f.box(15, 12, 360, 34, "ACYANOTIC (left to right shunt): pink, breathless", fill=MINT, stroke=TEAL, size=11, bold=True)
f.box(385, 12, 360, 34, "CYANOTIC (right to left shunt): blue, squats", fill=ROSE, stroke=RED, size=11, bold=True)
ac = ["VSD\nmost common\nharsh pansystolic\nmurmur", "ASD\nfixed split S2,\nflow murmur", "PDA\ncontinuous\nmachinery murmur", "COARCTATION\nweak femoral pulses,\narm BP above leg BP"]
cy = ["TETRALOGY OF FALLOT\nVSD + pulmonary stenosis\n+ overriding aorta + RVH\ntet spells, boot-shaped heart", "TRANSPOSITION\nof the great arteries\nblue at birth,\negg-on-side heart", "TRUNCUS, TAPVR,\ntricuspid atresia\nseverely blue,\nduct dependent"]
for i, s in enumerate(ac):
    f.box(15 + (i % 2) * 182, 58 + (i // 2) * 84, 176, 76, s, fill=BLUE, stroke=NAVY, size=10, bold=True)
for i, s in enumerate(cy):
    f.box(385, 58 + i * 56, 360, 52, s, fill=SAND, stroke=AMBER, size=10, bold=True)
f.box(15, 232, 360, 76, "NURSING: weigh and feed small, frequent meals; give digoxin and diuretic as ordered; count the pulse for 1 full minute; watch for heart failure (fast breathing, liver enlarged, sweating on feeding)", fill=BLUE, stroke=NAVY, size=9.5, bold=True)
f.box(385, 232, 360, 76, "TET SPELL: knee-chest position, oxygen, calm, IV fluids, morphine or propranolol as ordered. SCREEN: right hand and foot SpO2 at 24 hours", fill=ROSE, stroke=RED, size=10, bold=True)
```

**Gastrointestinal and other anomalies.** **Oesophageal atresia with tracheo-oesophageal fistula**: frothing, choking and cyanosis on first feed, and an NG tube that will not pass; keep the baby nil by mouth, head up, with continuous suction. **Imperforate anus**: no meconium in 24-48 hours; check the anus in every newborn. **Hirschsprung disease**: no meconium for over 48 hours and a distended abdomen. **Gastroschisis** (bowel outside, no sac) and **omphalocele** (sac present): cover with warm, saline-moist gauze and a plastic wrap or bowel bag, nil by mouth, NG tube, and urgent referral. **Hypospadias**: no circumcision, because the foreskin is needed for repair.

### Eight points of nursing care of a baby with a congenital anomaly

1. **Protect the baby first, then talk.** Make sure the airway, breathing, warmth and glucose are safe before anything else. For a sac or an abdominal defect, cover the defect with sterile moist saline gauze and plastic. The first hour decides infection and heat loss.
2. **Position safely.** Nurse the baby with spina bifida prone or on the side, a baby with TEF head-up, a baby with a cleft palate upright for feeds, and a baby with hydrocephalus with the head supported. Correct positioning prevents injury, aspiration and pressure on the defect.
3. **Feed in the right way.** Use a special teat, a cup or tube as advised, give small and frequent feeds, burp often and watch for choking. Weigh daily or every 3 days. Good feeding gives the weight needed for safe surgery.
4. **Prevent infection.** Use strict hand hygiene, sterile dressings, clean cord care and early antibiotics when ordered. A sac that is open or an infected skin close to a repair wound can cause meningitis or failure of repair.
5. **Monitor the right signs.** Measure head circumference daily in hydrocephalus, count limb movement and bladder function in spina bifida, check SpO₂ in CHD, and watch for distension in bowel anomalies. Early signs of worsening allow early rescue.
6. **Refer early and carry the baby safely.** Arrange transfer to the Kanti Children's Hospital, a central or provincial hospital, with warmth, oxygen, IV line and a written note. Early surgery gives the best result, and a long delay worsens outcome.
7. **Support the family through grief.** Parents may blame themselves or fear the community. Tell them that most anomalies are no one's fault, let them hold and name the baby, and arrange support from other parents. A mother's acceptance is the child's best protection.
8. **Plan long-term care and rights.** Teach home care, appointments, vaccines on time, early stimulation and school entry. Tell the family about the disability card and allowances under the Rights of Persons with Disabilities Act 2074. Good follow-up turns a defect into a full life.

### Seven points of prevention and health education

1. **Take folic acid before pregnancy.** Advise every woman who may become pregnant to take 400 µg of folic acid daily from at least 1 month before conception to the end of the 12th week; women with a previous NTD child need 4 mg. This prevents about 70% of neural tube defects. Eat green leaves, lentils and fortified flour too.
2. **Vaccinate before pregnancy.** Check the rubella (MR) status of girls and women, and give Td in pregnancy. Rubella in the first trimester causes heart disease, cataract and deafness in the baby.
3. **Control diabetes and other diseases.** Women with diabetes should achieve good sugar control before pregnancy, and women on valproate or other teratogens should talk to a doctor before conception. Uncontrolled diabetes multiplies the risk of anomalies.
4. **Avoid harmful substances.** Stop alcohol, tobacco and unprescribed drugs, and avoid X-rays and pesticides in pregnancy. Many rural Nepali women use pesticides without gloves; teach safer methods.
5. **Attend all four ANC visits.** Aama gives free ANC; the anomaly scan at 18-20 weeks (where available) finds major defects early. Early detection lets the family plan delivery in a hospital that can treat the baby.
6. **Avoid consanguineous marriage and late pregnancy.** Advise genetic counselling in a family with a known disorder, and explain that the Down syndrome risk rises after 35 years. Early and safe childbearing lowers risk.
7. **Screen every newborn.** Do a head-to-toe examination, check the palate, anus, spine and hips, and use pulse oximetry for heart defects at 24 hours. A defect found at birth can often be treated, but one found at 6 months may have caused damage.

## 2.5 Calculations

Newborn doses are **mg/kg × weight**, converted to mL by **dose ÷ concentration**. Weight loss is **(birth weight - current weight) ÷ birth weight × 100**. IV fluid is **mL/kg/day × weight ÷ 24 = mL/h**; with a microdrip set (60 drops/mL) the **drops per minute equal the mL per hour**. The Silverman score is the sum of five signs scored 0-2.

```python
kg = 1.4
sil = 1 + 2 + 1 + 2 + 1
surf = 200 * kg
print(f"Sunil: Silverman {sil} (7 or more = severe); surfactant 200 mg/kg = {surf:.0f} mg = {surf / 80:.1f} mL of 80 mg/mL")
caf = 20 * kg
print(f"Caffeine citrate load 20 mg/kg = {caf:.0f} mg = {caf / 20:.1f} mL of 20 mg/mL; maintenance 5 mg/kg = {5 * kg:.0f} mg = {5 * kg / 20:.2f} mL daily")
fl = 80 * kg
print(f"Day 2 fluid 80 mL/kg/day = {fl:.0f} mL/day = {fl / 24:.1f} mL/h = {fl / 24:.1f} drops/min (microdrip); antenatal dexamethasone 6 mg x 4 = {6 * 4} mg")
anju, d3 = 2.9, 2.7
feed = 150 * anju
print(f"Anju: weight loss {(anju - d3) / anju * 100:.1f}%; feeds 150 mL/kg/day = {feed:.0f} mL/day = {feed / 8:.0f} mL per 3-hourly feed = {feed * 0.67:.0f} kcal/day")
print(f"Rule of 10: needs {4.5 - anju:.1f} kg more; at 30 g/day = {(4.5 - anju) * 1000 / 30:.0f} days. Pulse oximetry: hand 97, foot 93, difference {97 - 93} points (fail if above 3)")
```

```text
Sunil: Silverman 7 (7 or more = severe); surfactant 200 mg/kg = 280 mg = 3.5 mL of 80 mg/mL
Caffeine citrate load 20 mg/kg = 28 mg = 1.4 mL of 20 mg/mL; maintenance 5 mg/kg = 7 mg = 0.35 mL daily
Day 2 fluid 80 mL/kg/day = 112 mL/day = 4.7 mL/h = 4.7 drops/min (microdrip); antenatal dexamethasone 6 mg x 4 = 24 mg
Anju: weight loss 6.9%; feeds 150 mL/kg/day = 435 mL/day = 54 mL per 3-hourly feed = 291 kcal/day
Rule of 10: needs 1.6 kg more; at 30 g/day = 53 days. Pulse oximetry: hand 97, foot 93, difference 4 points (fail if above 3)
```

## Formula and fact sheet

- **Classes:** preterm below 37 weeks; LBW below 2,500 g, VLBW below 1,500 g. **Normal newborn:** RR 40-60, HR 120-160, temperature 36.5-37.5 °C; weight loss up to 10%, regained by 10-14 days.
- **RDS:** surfactant lack below 34 weeks; antenatal dexamethasone 6 mg IM q12h × 4; bubble CPAP 5-6 cm; **poractant 200 mg/kg** first dose; **caffeine citrate 20 mg/kg** load, 5-10 mg/kg/day; SpO₂ 90-95%.
- **Silverman-Anderson:** 0 none, 1-3 mild, 4-6 moderate, 7 or more severe.
- **Caput** crosses sutures; **cephalhaematoma** does not and appears after 12-24 hours. **Erb's palsy** C5-C6.
- **NTD:** folic acid 400 µg daily (4 mg if previous NTD); myelomeningocele covered, prone, surgery in 48-72 hours. **Cleft:** rule of 10 (10 weeks, 10 lb, Hb 10 g/dL); palate repair 9-12 months. **Ponseti:** weekly casts × 5-6, tenotomy, boots 23 hours/day × 3 months.
- **CHD screen:** right hand and foot SpO₂ at 24 hours; pass if both 95% or more and difference 3 or less.

## Chapter summary

- A newborn is classified by gestation, weight and growth, and examined from head to toe; Nepal's essential newborn care keeps the baby dry, warm, fed and protected.
- RDS is a surfactant problem of the preterm baby, treated with steroids before birth, CPAP, surfactant and caffeine; the Silverman score tracks distress.
- Birth injuries differ by whether the swelling crosses sutures; NEC, seizures and sepsis need urgent referral.
- Congenital anomalies (NTD, hydrocephalus, cleft, clubfoot, DDH, Down syndrome, CHD, bowel defects) need protection of the defect, feeding support, early referral and family support.
- Folic acid, rubella vaccination, diabetes control, ANC and newborn screening prevent or detect them early.

## Practice

```python
mcq1 = 2 + 1 + 1 + 1 + 0                # MCQ1 Silverman score
mcq2 = (3.2 - 2.9) / 3.2 * 100          # MCQ2 weight loss percent
mcq3 = 20 * 1.2                         # MCQ3 caffeine load mg
mcq4 = 60 * 2.0 / 24                    # MCQ4 mL/h
mcq5 = 100 * 1.6 / 80                   # MCQ5 mL surfactant repeat dose
mcq6 = 96 - 94                          # MCQ6 SpO2 difference
print(f"MCQ1 = {mcq1}; MCQ2 = {mcq2:.1f}%; MCQ3 = {mcq3:.0f} mg; MCQ4 = {mcq4:.1f} mL/h; MCQ5 = {mcq5:.1f} mL; MCQ6 = {mcq6} points")
```

```text
MCQ1 = 5; MCQ2 = 9.4%; MCQ3 = 24 mg; MCQ4 = 5.0 mL/h; MCQ5 = 2.0 mL; MCQ6 = 2 points
```

**MCQs (with reasons)**

1. A baby has upper chest see-saw movement (2), mild lower chest retraction (1), mild xiphoid retraction (1), minimal flaring (1) and no grunt (0). The Silverman score and meaning is: (a) 3, mild (b) 5, moderate (c) 7, severe (d) 5, mild.
2. A baby weighed 3.2 kg at birth and 2.9 kg on day 3. The weight loss is: (a) 3% (b) 6% (c) 9.4% (d) 15%.
3. A 1.2 kg preterm baby needs caffeine citrate 20 mg/kg as a loading dose. The dose is: (a) 6 mg (b) 12 mg (c) 24 mg (d) 240 mg.
4. A 2.0 kg baby needs 60 mL/kg/day IV fluid. The rate is: (a) 2.5 mL/h (b) 5 mL/h (c) 7.5 mL/h (d) 120 mL/h.
5. A repeat surfactant dose of 100 mg/kg for a 1.6 kg baby, using 80 mg/mL, is: (a) 1.0 mL (b) 2.0 mL (c) 3.2 mL (d) 4.0 mL.
6. At 24 hours the right hand SpO₂ is 96% and the foot is 94%. The screen is: (a) fail, difference 2 (b) pass, difference 2 (c) fail, below 95% (d) invalid.
7. A scalp swelling that is not present at birth, appears on day 2 and does not cross the suture lines is: (a) caput succedaneum (b) cephalhaematoma (c) subgaleal haemorrhage (d) hydrocephalus.
8. A woman who has had a baby with spina bifida plans another pregnancy. The daily folic acid dose is: (a) 100 µg (b) 400 µg (c) 4 mg (d) 40 mg.

::: note Answers and rationales
**1. (b).** 2 + 1 + 1 + 1 + 0 = 5, which is moderate (4-6). A score of 7 or more is severe.
**2. (c).** (3.2 - 2.9) ÷ 3.2 = 9.4%. This is at the upper limit of the normal 5-10%; check feeding and watch for more loss. 3% and 6% are wrong calculations and 15% would be dangerous.
**3. (c).** 20 × 1.2 = 24 mg. 12 mg is 10 mg/kg and 240 mg is a ten-fold overdose.
**4. (b).** 60 × 2.0 = 120 mL/day ÷ 24 = 5 mL/h. 120 mL is the daily volume and 2.5 mL/h is half the required rate.
**5. (b).** 100 × 1.6 = 160 mg ÷ 80 mg/mL = 2.0 mL. 3.2 mL would be the 200 mg/kg first dose.
**6. (b).** Both readings are 95% or more and the difference (2 points) is not above 3, so the screen is passed. A fail needs a value below 95% or a difference above 3.
**7. (b).** A cephalhaematoma is bleeding under the periosteum and is limited by the suture lines. A caput is present at birth and crosses sutures.
**8. (c).** A woman with a previous child with a neural tube defect needs 4 mg daily before conception and to the 12th week. 400 µg is the standard dose for other women.
:::

**Short answer (3 marks): Differentiate caput succedaneum from cephalhaematoma.** Caput succedaneum is oedema of the scalp from the pressure of labour; it is present at birth, crosses the suture lines, pits on pressure and goes in 2-3 days. Cephalhaematoma is blood under the periosteum of one skull bone; it appears after 12-24 hours, does not cross the suture lines, feels firm and takes weeks to resolve. It may cause jaundice. Neither needs treatment; the nurse reassures the mother, does not aspirate the swelling and watches the bilirubin.

**Short answer (3 marks): Describe the feeding of a baby with a cleft lip and palate.** Feed in the upright or semi-upright position, because milk can flow into the nose. A baby with only a cleft lip can often breastfeed, as the breast fills the gap. With a cleft palate use a soft, long teat with a large hole, a squeezable bottle, a cup or spoon, or expressed milk. Feed small amounts, burp often, and stop if the baby chokes. Weigh the baby regularly, because lip repair needs 4.5 kg.

**Medium answer (5 marks): Explain the cause and management of respiratory distress syndrome (Figure 2.1).** RDS is caused by a **lack of surfactant** in the preterm lung (below 34 weeks), so the alveoli collapse at the end of each breath, the lungs become stiff and gas exchange falls. Signs are fast breathing, grunting, nasal flaring, chest retractions and cyanosis, starting within hours of birth; the X-ray shows ground-glass lungs with air bronchograms. **Prevention** is antenatal dexamethasone 6 mg IM every 12 hours for four doses at 24-34 weeks. **Treatment** includes warmth, IV glucose, early **bubble CPAP** at 5-6 cm of water, **surfactant 200 mg/kg** by thin tube, **caffeine** to prevent apnoea, antibiotics for possible sepsis, and oxygen to keep SpO₂ at 90-95%. **Nursing care** is the Silverman score every 1-2 hours, correct position, minimal handling, careful fluids, infection control and parent support. Complications are air leak, bronchopulmonary dysplasia, retinopathy of prematurity and intraventricular haemorrhage.

**Long answer (10 marks): Baby Anju, term girl, birth weight 2.9 kg, has a bilateral cleft lip and palate. On day 3 her weight is 2.7 kg, milk comes from her nose, and she chokes at the breast. Her mother is silent and asks, "What did I do wrong?" Calculate, describe the management and write the nursing care plan.**

*Calculations.* Anju's weight loss is (2.9 - 2.7) ÷ 2.9 = **6.9%**, within the normal range, but feeding must be corrected. At 150 mL/kg/day she needs **435 mL/day = 54 mL per 3-hourly feed (about 291 kcal/day)**. Lip repair is planned by the **rule of 10**; she needs **4.5 kg**, which is 1.6 kg more, or about **53 days** at 30 g per day. Pulse oximetry was hand 97% and foot 93%, a **difference of 4 points**, so she **fails the screen** and needs an echocardiogram (clefts can coexist with heart defects).

*Management.* The nurse first checks airway, breathing, temperature and glucose, and holds Anju upright for feeds. She uses a squeezable bottle with a long soft teat, or a cup, gives small amounts of expressed breast milk with frequent burping, and weighs the baby every 3 days. She cleans the mouth and nose after feeds and watches for aspiration and ear infection. The doctor refers for echocardiography, hearing tests, genetic review if other anomalies appear, and cleft team care at 3 months (lip) and 9-12 months (palate). The nurse sits with the mother, explains that clefts are rarely anyone's fault (folic acid and unknown causes), shows photographs of repaired children, and links her with a support group and the disability allowance office. She teaches danger signs, vaccines on time, ear care and, later, speech therapy.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "She chokes when she sucks." **O:** milk from nose, weight 2.7 kg (-6.9%) | **Ineffective infant feeding pattern** related to cleft palate | **Nutritional status:** takes 54 mL per feed; gains 30 g per day by day 14 | Upright position, long soft teat or cup, small feeds, burp often, weigh every 3 days (reduces aspiration and ensures calories) | Takes 50 mL feeds; weight 2.9 kg on day 10 |
| **O:** choking, SpO₂ 93% foot | **Risk for aspiration** related to nasal regurgitation | **Aspiration control:** no choking episodes, clear chest | Hold upright, feed slowly, suction ready, stop feed if coughing, check chest (prevents pneumonia) | No choking in 48 h, chest clear |
| **O:** open lip and palate, mouth debris | **Risk for infection** (ear, respiratory) related to open palate | **Infection status:** afebrile, no ear or chest signs | Clean mouth with sterile water after feeds, hand hygiene, vaccines on time, watch for ear discharge (limits bacteria entering the middle ear) | Afebrile, ear normal |
| **S:** "What did I do wrong?" **O:** silent, avoids holding baby | **Anxiety and grieving** related to the baby's appearance and guilt | **Coping:** mother holds, feeds and names the baby; states plan | Explain causes in Nepali, show repair photographs, encourage skin contact, refer to a support group (guilt falls when facts are given) | Mother feeds baby, asks about surgery |
| **O:** failed pulse-oximetry screen, repair planned | **Deficient knowledge** (surgery, follow-up) related to a new condition | **Knowledge: treatment:** mother states the repair plan and the danger signs | Teach rule of 10, appointments, danger signs, referral to the cleft team and echocardiogram (parents who understand the plan attend follow-up) | Mother repeats dates and 4 danger signs |
