---
subject: Community Health Nursing
grade: BSc Nursing Year 1
unit: 4
title: Maternal, Newborn and Child Health, IMNCI and Nutrition
hours: 25
area: BSN 6-7 · Community Health Nursing · Unit 4
---

Nepal's greatest public health success is the fall in maternal and child deaths: the under-five mortality rate dropped from 118 in 1996 to 33 per 1000 live births in NDHS 2022, and skilled birth attendance reached 80%. The nurse in the community delivers this success through the Safe Motherhood Programme, the Aama programme, the Community-Based Integrated Management of Neonatal and Childhood Illness (CB-IMNCI) and nutrition services. This unit pairs these programmes with the dosing arithmetic the nurse must get right: ORS plans, zinc, IFA supply and the weight-for-age Z-score.

::: key What this unit gives you
- A real blood-pressure check at antenatal-type visit, a real MUAC tape in use, and a MUAC colour-band schematic.
- Safe Motherhood and the Aama programme, the ANC contacts, birth preparedness and the continuum of care.
- IMNCI classification by colour, the three ORS plans with calculations for an 8-kg infant, zinc, Z-score and IFA supply, all computed.
- Eight points on the nurse's role in Safe Motherhood and model answers with a child case and care plan.
:::

## 4.1 Safe Motherhood, the Aama programme and the continuum of care

The **Safe Motherhood Programme** aims to reduce maternal and newborn deaths through four pillars: antenatal care, clean and safe delivery by a skilled attendant, emergency obstetric care and postnatal care, with family planning running through all. Nepal's maternal mortality ratio fell from 539 in 1996 to **151 per 100,000 live births** in the 2021 national maternal mortality study; in a district with 8,400 live births this still means about **12.7 maternal deaths a year**. The **Aama Surakshya Programme** gives free institutional delivery and a transport incentive, and an incentive for completing the **four antenatal visits** (at months 4, 6, 8 and 9; the WHO model has 8 contacts) so that cost does not stop a woman from reaching a birthing centre. Free safe abortion services are provided under the Safe Motherhood and Reproductive Health Rights Act 2075 (2018). **Birth preparedness** means that each family has chosen the place of delivery and the skilled attendant, saved money, arranged transport, identified a blood donor and kept the health post phone number.

The **continuum of care** links time (adolescence, pregnancy, birth, the newborn period, childhood) with place (home, community, health post, hospital). Each visit is used to give what the next stage needs: iron-folic acid (**180 tablets** a woman), calcium, albendazole, Td, birth plan and breastfeeding advice. For the 924 expected pregnancies of a municipality the IFA need is 924 × 180 = **166,320 tablets** a year.

```photogrid label="4.1" cols="3" ratio="1.0" caption="Mother and child contacts. (a) Blood pressure is checked as part of every antenatal-type visit: a raised pressure in pregnancy is pre-eclampsia until shown otherwise. (b) A real mid-upper-arm circumference band in use on an infant: the coloured band gives the result in seconds. (c) MUAC colour zones for a child aged 6-59 months."
@ photo id="nur3/hpcheck" cap="Blood-pressure check, health post"
fit 1.0
focus 0.55 0.55
mark 0.62 0.50 "1"
mark 0.40 0.22 "2"
key 1 (a) The BP cuff: record in every visit, 140/90 mmHg or more needs referral in pregnancy
key 2 (a) A young child brought along: the same visit is used to ask about growth and immunisation
@ photo id="nur3/muac" cap="MUAC band on an infant"
fit 1.0
focus 0.6 0.5
mark 0.70 0.55 "3"
mark 0.35 0.65 "4"
key 3 (b) The band wraps the mid-upper arm: read where the arrow shows
key 4 (b) The child is held by the mother, so the arm is relaxed (not crying)
@ svg cap="MUAC colour zones"
f = Fig(300, 300)
f.box(30, 20, 240, 62, "Red: below 115 mm\nSevere acute malnutrition (SAM)\nRefer / start RUTF", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(30, 98, 240, 62, "Yellow: 115 to below 125 mm\nModerate acute malnutrition\nSupplementary food, counsel", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(30, 176, 240, 62, "Green: 125 mm or more\nWell nourished\nContinue growth monitoring", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.text(150, 268, "Age 6 to 59 months; also check oedema of both feet", size=10, color=SLATE, bold=True)
```

## 4.2 Antenatal, delivery and postnatal care in the community

At every antenatal visit the nurse takes history, measures weight, BP, fundal height and foetal heart, tests urine for protein and haemoglobin, gives IFA, calcium and Td, and counsels. **Danger signs** that need immediate referral are vaginal bleeding, severe headache or blurred vision, fits, fever, water breaking before labour, reduced foetal movement and severe breathlessness. During delivery the skilled attendant uses the **partograph**, active management of the third stage (oxytocin 10 IU IM within one minute, controlled cord traction and uterine massage) and the **Essential Newborn Care** steps: dry and stimulate, delayed cord clamping, skin-to-skin contact and breastfeeding within one hour. Postnatal visits are made within 24 hours, on day 3 and day 7, and at 6 weeks.

```svgfig label="4.1" caption="The Safe Motherhood continuum with Nepal's key contacts. Each contact has a defined set of services, and danger signs at any point mean referral."
f = Fig(760, 200)
st = [("Pregnancy", "4 ANC visits\nIFA 180, Td,\ncalcium, albendazole", SAND, AMBER), ("Birth", "Skilled attendant,\npartograph, AMTSL,\nbirth centre", ROSE, RED), ("Postnatal", "Visits at 24 h,\nday 3, day 7, 6 weeks\nFP, vitamin A", BLUE, NAVY), ("Newborn", "Warmth, breastfeeding,\nBCG, cord care,\nCB-IMNCI", MINT, TEAL), ("Child", "Growth, vaccines,\nvitamin A, deworm,\nIMNCI", SAND, AMBER)]
for i, (t_, d_, fc, sc) in enumerate(st):
    x = 6 + i * 150
    f.box(x, 24, 134, 34, t_, fill=fc, stroke=sc, size=11, bold=True)
    f.box(x, 66, 134, 74, d_, fill=SOFT, stroke=sc, size=10)
    if i < 4: f.arrow([(x + 134, 41), (x + 150, 41)], color=SLATE, sw=2)
f.text(380, 168, "Danger sign at any point: stabilise, refer, accompany, and give feedback", size=11, color=RED, bold=True)
f.text(380, 190, "FCHV and mothers' group link every contact to the ward", size=10.5, color=TEAL, bold=True)
```

## 4.3 IMNCI: assess, classify, treat, counsel

**IMNCI** (Integrated Management of Neonatal and Childhood Illness) is the national protocol for children up to 5 years, delivered at health posts and, as **CB-IMNCI**, by FCHVs in the community. For every sick child aged 2 months to 5 years the health worker **assesses** the general danger signs (cannot drink or breastfeed, vomits everything, convulsions, lethargic or unconscious) and then asks about cough or difficult breathing, diarrhoea, fever, ear problem, malnutrition and anaemia, and immunisation. The sign is then **classified** by a colour: **pink** (urgent referral), **yellow** (treat at the post) or **green** (home care). **Fast breathing** is 60 or more breaths a minute under 2 months, **50 or more at 2-11 months**, and **40 or more at 12-59 months**; fast breathing with no danger sign is **pneumonia** (oral amoxicillin for 5 days), and chest indrawing or a danger sign is severe pneumonia (first dose, then refer).

The dehydration classification decides the **ORS plan**. A child with no signs is given **Plan A** (home care: more fluids, ORS 50-100 mL after each loose stool under 2 years, zinc and feeding). *Some dehydration* (restless or irritable, sunken eyes, drinks eagerly, skin pinch goes back slowly) needs **Plan B**: **ORS 75 mL/kg over 4 hours** at the post. *Severe dehydration* (lethargic, sunken eyes, drinks poorly, skin pinch very slow) needs **Plan C**: IV Ringer's lactate **100 mL/kg**: in an infant 30 mL/kg in the first hour and 70 mL/kg over the next 5 hours (older children 30 mL/kg in 30 minutes and 70 mL/kg in 2.5 hours). Every child with diarrhoea gets **zinc 20 mg daily for 10 days** (10 mg under 6 months). The low-osmolarity ORS packet makes 1 litre and contains glucose 13.5 g, sodium chloride 2.6 g, potassium chloride 1.5 g and trisodium citrate 2.9 g.

```python
w = 8                                   # infant, kg
print(f"ORS packet = {13.5 + 2.6 + 1.5 + 2.9:.1f} g per litre")
planb = 75 * w
print(f"Plan B: {planb} mL ORS over 4 h = {planb / 4:.0f} mL/h")
planc = 100 * w
print(f"Plan C total = {planc} mL: 30 mL/kg = {30 * w} mL in 1 h, then 70 mL/kg = {70 * w} mL over 5 h = {70 * w / 5:.0f} mL/h")
print(f"Zinc 20 mg x 10 days = {20 * 10} mg")
print(f"Amoxicillin DT 250 mg, 1 tablet twice daily x 5 days = {1 * 2 * 5} tablets (4 to under 10 kg band)")
z = (8.2 - 10.9) / 1.2                  # reference median 10.9 kg, SD 1.2 (rounded teaching values)
print(f"Weight-for-age Z-score = {z:.2f}")
```

```text
ORS packet = 20.5 g per litre
Plan B: 600 mL ORS over 4 h = 150 mL/h
Plan C total = 800 mL: 30 mL/kg = 240 mL in 1 h, then 70 mL/kg = 560 mL over 5 h = 112 mL/h
Zinc 20 mg x 10 days = 200 mg
Amoxicillin DT 250 mg, 1 tablet twice daily x 5 days = 10 tablets (4 to under 10 kg band)
Weight-for-age Z-score = -2.25
```

For an 8-kg infant Plan B gives **600 mL of ORS over 4 hours, which is 150 mL/h**, and Plan C gives **800 mL in all: 240 mL in the first hour and 560 mL over 5 hours (112 mL/h)**. The zinc course is **200 mg** and the amoxicillin course is **10 tablets**. The **Z-score** = (observed − reference median) ÷ reference SD; a child of 8.2 kg against a reference median of 10.9 kg and SD 1.2 (teaching values rounded from the WHO tables) has a Z-score of **-2.25**, below −2 and therefore **underweight** (below −3 is severe). Always use the actual WHO growth chart in practice.

```svgfig label="4.2" caption="IMNCI colour-coded classification for diarrhoea. The colour sets the place of treatment and the ORS plan."
f = Fig(760, 210)
f.box(10, 20, 235, 120, "PINK: severe dehydration\nLethargic, sunken eyes,\ndrinks poorly, skin pinch very slow\nPlan C: IV RL 100 mL/kg\nrefer, ORS on the way", fill=ROSE, stroke=RED, size=10, bold=True)
f.box(262, 20, 235, 120, "YELLOW: some dehydration\nRestless, sunken eyes,\ndrinks eagerly, pinch slow\nPlan B: ORS 75 mL/kg in 4 h\nzinc, review after 4 h", fill=SAND, stroke=AMBER, size=10, bold=True)
f.box(514, 20, 235, 120, "GREEN: no dehydration\nNo signs\nPlan A: fluids, ORS after\neach stool, zinc 10 days\nreturn if worse", fill=MINT, stroke=TEAL, size=10, bold=True)
f.text(380, 168, "Persistent diarrhoea (14 days or more): refer. Blood in stool: treat as dysentery.", size=10.5, color=SLATE, bold=True)
f.text(380, 192, "Continue breastfeeding and feeding in every plan", size=10.5, color=TEAL, bold=True)
```

## 4.4 Growth, breastfeeding and complementary feeding

Growth is monitored monthly under two years and every 3 months to 5 years by weight on the growth chart, because a flat or falling line is the earliest sign of trouble. NDHS 2022 found about 25% of under-five children stunted, 8% wasted and 19% underweight. **Exclusive breastfeeding** for 6 months, with breastfeeding for 2 years or more, gives the child protection against diarrhoea and pneumonia; start within one hour of birth and give colostrum. From **6 months** add soft **thick home-made foods**: *lito* or *jaulo* with oil, ghee, mashed dal, egg and vegetables, going from 2-3 meals a day at 6-8 months to 3-4 meals and snacks by 12 months. **Vitamin A** capsules are given twice a year from 6 to 59 months (100,000 IU at 6-11 months, 200,000 IU at 12-59 months) and deworming (albendazole) twice a year from 12 months. **Low birth weight** is below 2,500 g and these babies need kangaroo mother care.

## 4.5 The nurse's role in the Safe Motherhood Programme: eight points

1. **Register and trace every pregnant woman.** Make a pregnancy register for the ward with the FCHVs, noting the last menstrual period, the expected date and risk factors. Visit those who have missed an ANC contact. Early registration in the first three months is the base of all later care.
2. **Provide complete antenatal care.** Take history, weight, BP, fundal height, foetal heart and urine protein at each visit, and test haemoglobin. Give 180 IFA tablets, calcium and Td, and albendazole after the first trimester. Do not skip any step even on a busy day.
3. **Detect and refer the high-risk mother.** Age under 18 or over 35, height under 145 cm, anaemia, previous caesarean, twins, high BP and bleeding are risks. Write the risk on the card and refer early to a hospital with emergency obstetric care. Referral must include a note and, if possible, an escort.
4. **Teach danger signs and birth preparedness.** Teach the mother, husband and mother-in-law the signs: bleeding, fits, severe headache, fever and reduced movements. Help the family plan the place of birth, transport, funds and a blood donor. The "three delays" (in deciding, reaching and receiving care) are shortened by this planning.
5. **Ensure a clean and safe delivery.** Encourage delivery at a birthing centre or hospital with a skilled attendant, supplied under the Aama programme. Use the partograph, clean delivery kit, active management of the third stage and Essential Newborn Care. Clean hands, a clean surface and a clean cord cut are the three cleans.
6. **Give postnatal care to mother and baby.** Visit within 24 hours, on day 3 and day 7, and at 6 weeks. Check bleeding, temperature, uterus, breasts, perineum, the baby's feeding, cord and warmth. Give vitamin A to the mother within 42 days and counsel on family planning.
7. **Promote nutrition, rest and breastfeeding.** Advise an extra meal each day in pregnancy, with dal, green vegetables, egg, milk and fruit, and rest at least two hours in the day. Teach attaching the baby well and feeding on demand. Beliefs that deny colostrum or encourage heavy work in pregnancy are gently corrected.
8. **Record, report and review deaths.** Fill in the ANC and delivery registers, report through HMIS and notify every maternal and perinatal death within 24 hours. Take part in the maternal and perinatal death review, which is a no-blame learning process. The review finds the delay that caused the death and changes the system.

## Formula and fact sheet

- NDHS 2022: NMR 21, IMR 28, under-5 33 per 1000; skilled birth attendance 80%; MMR 151 per 100,000 (2021 study).
- ANC at months 4, 6, 8, 9; IFA 180 tablets; Td; postnatal visits at 24 h, day 3, day 7 and 6 weeks.
- IMNCI fast breathing: ≥50 (2-11 months), ≥40 (12-59 months). Plan A at home, Plan B ORS 75 mL/kg in 4 h, Plan C IV 100 mL/kg.
- Zinc 20 mg for 10 days (10 mg under 6 months). ORS packet 20.5 g per litre (13.5 + 2.6 + 1.5 + 2.9).
- MUAC: below 115 mm severe, 115 to below 125 mm moderate, 125 mm or more normal. Z-score = (observed − median) ÷ SD.

## Chapter summary

- Safe Motherhood and the Aama programme bring skilled care at four ANC contacts, delivery and postnatal visits.
- IMNCI classifies by colour and fixes the treatment, and CB-IMNCI extends it to the FCHV.
- Diarrhoea is treated by ORS plan A, B or C with zinc, and all plans continue feeding.
- Growth monitoring, MUAC and Z-score find undernutrition early; breastfeeding and thick home foods prevent it.

## Practice

**MCQs (with reasons)**

1. Fast breathing in a child aged 14 months is: (a) 30 or more (b) 40 or more (c) 50 or more (d) 60 or more.
2. For an 8-kg infant with some dehydration, Plan B gives: (a) 240 mL in 4 h (b) 400 mL in 4 h (c) 600 mL in 4 h (d) 800 mL in 4 h.
3. A MUAC of 112 mm in a child of 2 years means: (a) normal (b) moderate malnutrition (c) severe acute malnutrition (d) obesity.
4. The usual zinc course in diarrhoea of a 1-year-old is: (a) 10 mg for 5 days (b) 20 mg for 10 days (c) 20 mg for 3 days (d) 40 mg for 14 days.
5. IFA tablets given to a pregnant woman in Nepal total: (a) 30 (b) 90 (c) 180 (d) 360.

::: note Answers and rationales
**1. (b).** The cut-off for 12-59 months is 40 breaths a minute; 50 applies to 2-11 months and 60 to infants under 2 months.
**2. (c).** 75 mL × 8 kg = 600 mL over 4 hours (150 mL/h); 800 mL is the Plan C volume.
**3. (c).** Below 115 mm is severe acute malnutrition and needs RUTF or referral.
**4. (b).** Zinc 20 mg for 10 days shortens the illness and prevents the next attack; 10 mg is for infants under 6 months.
**5. (c).** The Safe Motherhood schedule is 180 IFA tablets, one daily from the fourth month, with a further 45 tablets after delivery.
:::

**Short answer (3 marks): Aama programme.** The Aama Surakshya Programme is a Nepal government scheme to increase institutional deliveries. It provides free delivery care and a transport incentive, and an incentive for four antenatal visits, so that cost does not prevent women from reaching skilled care. It is run through health facilities and reimbursed through the local level. It has helped to raise skilled birth attendance to 80% (NDHS 2022).

**Medium answer (5 marks): Describe the IMNCI approach and the management of diarrhoea in a child (Figure 4.2).** IMNCI assesses a child aged 2 months to 5 years for general danger signs and for cough, diarrhoea, fever, ear problem and nutrition, classifies each by colour (pink, yellow, green) and gives matching treatment and counselling. In diarrhoea the dehydration is graded. With none, **Plan A** is home fluids, ORS after each stool, zinc and food. With some dehydration, **Plan B** gives ORS 75 mL/kg over 4 hours at the post and reassesses. With severe dehydration, **Plan C** gives IV Ringer's lactate 100 mL/kg (30 then 70 mL/kg) and refers. **Zinc 20 mg for 10 days** is given to all, and breastfeeding and feeding continue. The mother is taught to return for blood in the stool, repeated vomiting or not drinking.

**Long answer (10 marks): A mother brings her 14-month-old son to the health post with watery stools for 3 days and cough. He weighs 8.2 kg (reference median 10.9 kg, SD 1.2), is restless, has sunken eyes, drinks eagerly and the skin pinch goes back slowly. Respiratory rate 46/min, temperature 37.8 °C, no chest indrawing. Classify and manage him, and prepare the nursing care plan.**

*Classification.* He has **some dehydration** (restless, sunken eyes, drinks eagerly, slow pinch), **pneumonia** (46 breaths a minute is above the 40 cut-off for his age, with no danger sign or indrawing) and is **underweight** with a Z-score of (8.2 − 10.9) ÷ 1.2 = **-2.25**. He is yellow for diarrhoea and for pneumonia and can be treated at the post.

*Treatment.* **Plan B**: ORS 75 mL/kg × 8 kg (weight rounded to 8 kg) = **600 mL over 4 hours = 150 mL/h**, in small sips by cup and spoon, stopping and restarting after 10 minutes if he vomits; reassess after 4 hours and move to Plan A if hydrated or to Plan C if worse. Give **zinc 20 mg daily for 10 days (200 mg in all)**, **amoxicillin dispersible tablet 250 mg, 1 tablet twice a day for 5 days (10 tablets)**, and continue breastfeeding and feeding. Give vitamin A if due. Teach the mother Plan A at home, the danger signs and the return visit in 2 days for pneumonia. Enrol him in growth monitoring and counsel about thick foods with oil, egg and dal.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** mother: "he passes watery stool many times, he is thirsty." **O:** restless, sunken eyes, slow skin pinch, 8.2 kg. | **Deficient fluid volume** related to loss through diarrhoea, as evidenced by sunken eyes and slow skin pinch. | **Hydration:** skin pinch normal and no sunken eyes in 4 hours. | 1. ORS 600 mL over 4 h by cup and spoon; *replaces the loss orally and safely.* 2. Give small sips every 1-2 minutes; *prevents vomiting.* 3. Zinc 20 mg daily; *reduces the duration and the next attack.* 4. Reassess at 4 hours; *decides the next plan.* | At 4 hours, signs of dehydration absent; goal met. |
| **O:** RR 46/min, cough, temp 37.8 °C. | **Ineffective breathing pattern** related to lower respiratory infection, as evidenced by fast breathing. | **Respiratory status:** RR below 40/min in 3 days. | 1. Give amoxicillin DT 250 mg twice daily for 5 days; *treats bacterial pneumonia.* 2. Keep him warm and give fluids; *thins secretions.* 3. Teach danger signs (chest indrawing, not drinking); *early return.* | Review on day 2 and day 5. |
| **O:** Z-score -2.25, mother gives only thin rice water. | **Imbalanced nutrition: less than body requirements** related to inadequate complementary food, as evidenced by Z-score below −2. | **Nutritional status:** weight gain of 200 g in a month and 4 meals a day. | 1. Teach thick foods with oil, egg and dal, and 4 meals a day; *gives energy and protein.* 2. Continue breastfeeding; *protects from infection.* 3. Monthly growth monitoring with the FCHV; *tracks response.* | Weigh in 1 month; goal met at 8.4 kg or more. |

::: tip Exam tip
For any IMNCI case, state the classification of each problem with its colour, show the calculation for the dose or the ORS volume with the weight, and finish with home care and return signs.
:::
