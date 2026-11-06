---
subject: Midwifery I
grade: BSc Nursing Year 3
unit: 2
title: Well-Woman Care, Pre-conception Care, Diagnosis of Pregnancy, Dating, Physiological Changes and Minor Disorders
hours: 22
area: BSN 17-18 · Midwifery I · Units 2-3
---

Kalpana Rai, 24, walks into a municipal health post in Ilam with a missed period, a metallic taste in her mouth and a pregnancy test in her hand. She has one child of 3 years, her haemoglobin has never been checked, and she asks four questions: *Am I really pregnant? When is the baby due? Is it normal to feel sick all day? What should I eat?* A midwife answers all four with the same body of knowledge: **well-woman and pre-conception care**, the **signs that diagnose pregnancy**, the **calculation of the due date**, the **physiological changes of each system** and the **minor disorders** that can be managed at home. This unit covers these topics, linking them to the Nepal ANC protocol (Unit 3).

::: key What this unit gives you
- Real images: a **urine hCG test** with two lines, a **linea nigra** on a pregnant abdomen, a **Doppler fetal heart detector**, a midwife using a **Pinard horn** and a bottle of **prenatal tablets**; plus SVG figures on the signs of pregnancy, fundal height by week and the hormone-to-system map of pregnancy.
- **Eight points on pre-conception care** and **eight minor disorders** with remedies, each in 3-4 plain sentences.
- Dating maths verified by Python: **Naegele's rule and EDD**, gestational age, **McDonald's rule**, GTPAL, blood-volume change, BMI and weight-gain target.
- MCQs, short, medium and long answers and a 5-column NANDA-I plan for Kalpana (nausea, heartburn, backache, anaemia).
:::

## 2.1 Well-woman care and a healthy family

**Well-woman care** looks after a woman's reproductive health in every stage of life, not just when she is pregnant. It includes **puberty education** (menarche at about 12-13 years, menstrual hygiene), **safe sexual development** (consent, protection from STIs and unplanned pregnancy), cervical screening (VIA or Pap smear from 30 years), breast self-examination, nutrition and anaemia control, immunisation (**Td, MR, HPV** for girls under the National Immunisation Programme), family planning and menopause care. A **healthy family** is planned in size and timing, free of violence and with shared decisions; the **Healthy Timing and Spacing of Pregnancy (HTSP)** message is *first pregnancy after 20 years, at least 24 months between a birth and the next pregnancy and 6 months after a miscarriage*. Nepal's **Safe Motherhood and Reproductive Health Rights Act 2075 (2018)** gives every woman the right to safe motherhood, safe abortion services within the limits of the Act and respectful care, and the midwife must know it. **Culturally sensitive education** means using local languages, involving mothers-in-law and husbands, and respecting beliefs about food in pregnancy (for example "cooling" and "heating" foods) while correcting only what is harmful.

## 2.2 Eight points of pre-conception care

Pre-conception care prepares the body **before** the pregnancy begins, because organs form in the first 8 weeks, often before a woman knows she is pregnant.

1. **Folic acid.** A daily dose of **400 micrograms** from at least one month before conception until 12 weeks reduces neural tube defects such as spina bifida by about 70%. Women who have had an affected baby, who have diabetes or take anti-epileptic drugs need a higher dose (4-5 mg) on a doctor's order. Green leafy vegetables, lentils and fortified flour help but are not enough alone.
2. **Immunisation.** Check rubella (MR) status, tetanus-diphtheria (Td) and, where advised, hepatitis B. Rubella in early pregnancy causes deafness, cataract and heart defects. Live vaccines such as MR must be given at least 4 weeks before conception.
3. **Nutrition and anaemia.** Aim for a BMI of 18.5-24.9, a haemoglobin of 12 g/dL or more, and a balanced diet of dal, eggs, milk, vegetables and fruit. Treat anaemia and deworm. Underweight mothers have small babies; obese mothers risk diabetes and pre-eclampsia.
4. **Control of chronic illness.** Diabetes, hypertension, epilepsy, thyroid disease, heart disease, TB and HIV need a plan before conception. For example, a woman with diabetes should reach an HbA1c under 6.5% to cut the risk of malformation. HIV-positive women are linked to ART to prevent mother-to-child transmission.
5. **Avoid harmful substances.** Stop alcohol, tobacco, chewing tobacco (*khaini*), unprescribed drugs and, as far as possible, **indoor smoke from wood and dung fires**, which is common in Nepal's hills and Tarai. These cause miscarriage, low birth weight and fetal alcohol syndrome. Offer help to quit.
6. **Healthy timing and spacing.** The best age for pregnancy is 20-35 years. A pregnancy under 18 years carries higher risk of obstructed labour, pre-eclampsia and preterm birth, and an interval under 18 months raises the risk of preterm birth and low weight. Discuss family planning to make this possible.
7. **Genetic counselling.** Ask about family history, previous malformed or stillborn babies, consanguineous marriage, advanced age (35 years or more) and thalassaemia or sickle cell disease. Offer counselling and referral for testing. Respect the couple's decision and avoid blame.
8. **Mental health, violence and STIs.** Screen for depression, domestic violence and STIs including syphilis and HIV. Women who experience violence are at higher risk of miscarriage and preterm birth. Provide confidential care and link to One-Stop Crisis Management Centres (OCMC) in hospitals.

## 2.3 Diagnosis of pregnancy

The diagnosis rests on three groups of signs (Figure 2.1). **Presumptive** signs are what the woman feels and may have other causes. **Probable** signs are what the examiner finds and are strong but can be misleading. **Positive** (diagnostic) signs can only be caused by a fetus.

```svgfig label="2.1" caption="Signs of pregnancy on a timeline in completed weeks from the last menstrual period (LMP). Presumptive signs begin from week 4-6 (a missed period), probable signs from week 6 (Hegar's, Chadwick's) and positive signs from week 6 (cardiac activity on ultrasound) to 20 weeks (Pinard). The urine hCG test turns positive about 10-14 days after fertilisation, at or just after the missed period."
f = Fig(760, 330)
f.line(40, 40, 720, 40, color=SLATE, sw=2)
for x, w in [(40, "4"), (130, "6"), (220, "8"), (310, "10-12"), (400, "16"), (500, "18-20"), (600, "28"), (700, "36-40")]:
    f.line(x, 34, x, 46, color=SLATE, sw=2); f.text(x, 24, w + " wk", size=10, color=SLATE, bold=True)
f.box(40, 62, 330, 58, "PRESUMPTIVE (woman's story)\namenorrhoea, nausea and vomiting, breast tenderness,\nfrequency of micturition, fatigue, quickening (16-20 wk)", fill=SAND, stroke=AMBER, size=10, bold=True)
f.box(130, 130, 590, 70, "PROBABLE (examiner finds)\nHegar's sign 6-8 wk (soft isthmus), Chadwick's sign (blue vagina and cervix), Goodell's sign (soft cervix),\nuterine enlargement, Braxton Hicks, ballottement 16-28 wk, positive urine or serum hCG", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.box(130, 210, 590, 62, "POSITIVE (only a fetus can cause)\nultrasound: sac 5 wk, embryo with heartbeat 6 wk | Doppler heart sounds 10-12 wk | Pinard 18-20 wk\nfetal parts and movements felt by the examiner (after 20 wk) | X-ray or scan seeing a skeleton", fill=MINT, stroke=TEAL, size=10, bold=True)
f.box(40, 282, 680, 42, "Remember: positive hCG with an empty uterus on scan may be an ECTOPIC pregnancy;\npositive hCG with a large uterus and no fetus may be a MOLE", fill=ROSE, stroke=RED, size=10, bold=True)
```

**Urine pregnancy test (UPT).** Lateral-flow strips detect **hCG at 20-25 mIU/mL** in urine; the first morning sample is the most concentrated. Two lines (control and test) mean pregnant; one control line means not pregnant (Plate 2.1 a). **False negatives** occur if tested too early or the urine is dilute; **false positives** with molar pregnancy, some tumours and recent miscarriage. **Serum beta-hCG** doubles about every 48-72 hours in early normal pregnancy; a slower rise suggests ectopic or failing pregnancy. **Ultrasound** is the confirmatory test: the gestational sac is seen at about 5 weeks, the yolk sac at 5.5 weeks and a heartbeat at about 6 weeks.

**Skin signs.** The pigmentation of pregnancy is caused by MSH and oestrogen: the **linea nigra** (a dark line from the pubis to the umbilicus), darker nipples and areolae, and **chloasma** (the "mask of pregnancy") on the face. **Striae gravidarum** are pink or purple stretch lines on the abdomen, thighs and breasts, which fade to silvery-white after birth. None of these is harmful. Advise the woman that they are normal, avoid unproven creams and use sun protection for the face.

```photogrid label="2.1" cols="4" ratio="1.0" caption="Diagnosing pregnancy in real images. (a) Two hCG cassette tests, each with a control line and a test line (both positive). (b) A linea nigra running from the umbilicus to the pubis, with a darkened areola above. (c) A hand-held fetal Doppler: a probe sends sound to the fetal heart and a screen shows the rate (normal 110-160 beats per minute). (d) A midwife listening for the fetal heart with a Pinard horn pressed on the mother's abdomen."
@ photo id="nur11/ptest" cap="hCG urine tests, positive"
fit 1.0
focus 0.5 0.5
mark 0.37 0.46 "1"
mark 0.64 0.46 "2"
key 1 (a) Control line and test line: two lines mean positive
key 2 (a) Second cassette: a faint test line is still positive
@ photo id="nur11/linea" cap="Linea nigra"
fit 1.0
focus 0.5 0.5
mark 0.22 0.57 "3"
mark 0.28 0.13 "4"
key 3 (b) Linea nigra, a dark midline streak (MSH and oestrogen)
key 4 (b) Darkened skin near the lower abdomen and areola
@ photo id="nur11/doppler" cap="Fetal Doppler"
fit 1.0
focus 0.5 0.5
mark 0.45 0.88 "5"
mark 0.82 0.72 "6"
key 5 (c) Display: shows fetal heart rate in beats per minute
key 6 (c) Probe: placed on the abdomen with gel
@ photo id="nur11/pinard" cap="Pinard horn auscultation"
fit 1.0
focus 0.5 0.5
```

## 2.4 Dating the pregnancy: EDD, gestational age and fundal height

**Naegele's rule** gives the **expected date of delivery (EDD)**: take the first day of the last normal menstrual period (LMP), **add 7 days and subtract 3 months** (or add 9 months). It assumes a 28-day cycle and 280 days (40 weeks) from LMP. Only about 4-5% of babies arrive on the EDD, and normal term is **37 to 41 completed weeks**. In Nepal women often remember the date by the Nepali calendar (BS), so convert carefully to the Gregorian date before counting. If the LMP is uncertain or the cycle is irregular, use **early ultrasound (crown-rump length before 13 weeks)**, which is accurate to within 5-7 days.

**Gestational age (GA)** is the time from LMP to today, in completed weeks and days. **Fundal height** (symphysis pubis to the top of the fundus, measured in cm with a tape, bladder empty) after 24 weeks equals the **weeks of gestation ± 2 cm**. **McDonald's rule:** GA (weeks) = fundal height (cm) × 8/7, and GA (months) = fundal height ÷ 3.5. The landmark method (Figure 2.2) works from the 12th week.

```svgfig label="2.2" caption="Fundal height by landmark. The uterus becomes an abdominal organ at 12 weeks (just above the symphysis), reaches the umbilicus at 20-22 weeks (fundal height about 20-22 cm) and the xiphisternum at 36 weeks (about 36 cm), and then sinks 2-3 cm in the last 2 weeks as the head engages (lightening). Fundal height 3 cm or more below or above the weeks suggests growth restriction, a wrong date, twins or polyhydramnios and needs an ultrasound."
f = Fig(760, 330)
f.raw('<path d="M110 40 Q160 20 210 40 L225 120 Q260 200 220 270 Q160 305 100 270 Q60 200 95 120 Z" fill="#fff7ed" stroke="#b45309" stroke-width="2"/>')
for y, lab, col in [(262, "12 wk: above symphysis", TEAL), (222, "16 wk: halfway to umbilicus", TEAL), (176, "20-22 wk: umbilicus (20 cm)", NAVY), (138, "28 wk: 3 fingers above (28 cm)", NAVY), (98, "32 wk: midway to xiphisternum", NAVY), (60, "36 wk: xiphisternum (36 cm)", RED)]:
    f.line(112, y, 232, y, color=col, sw=2, dash=True)
    f.text(248, y + 4, lab, size=10.5, color=col, bold=True, anchor="start")
f.circle(166, 176, 5, fill=SAND, stroke=AMBER)
f.box(500, 40, 245, 70, "McDonald's rule\nweeks = cm x 8 / 7\nmonths = cm / 3.5", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(500, 130, 245, 70, "After 24 weeks\nfundal height (cm) = weeks +/- 2\nmeasure with the bladder empty", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(500, 220, 245, 80, "Refer for scan if 3 cm or more\nbelow (growth restriction, wrong date)\nor above (twins, polyhydramnios,\nmacrosomia)", fill=ROSE, stroke=RED, size=10.5, bold=True)
```

**Gravida and para.** **Gravida** is the number of pregnancies including the present one; **para** is the number of births after 28 weeks (Nepal and WHO count viable births after 28 weeks; some textbooks use 24 weeks). **GTPAL** records **G**ravida, **T**erm births, **P**reterm births, **A**bortions and **L**iving children. A woman who has had two term births and a miscarriage at 10 weeks and is now pregnant is **G4 T2 P0 A1 L2**.

```python
from datetime import date, timedelta
lmp = date(2025, 10, 12)
edd = lmp + timedelta(days=280)                      # same as Naegele: +7 days, -3 months
visit = date(2026, 2, 1)
days = (visit - lmp).days
weeks, extra = divmod(days, 7)
fh = 32                                              # fundal height in cm at another visit
mcd_weeks = fh * 8 / 7
mcd_months = fh / 3.5
g, t, p, a = 4, 2, 0, 1                              # two term births, one miscarriage, now pregnant
living = 2
print(f"LMP {lmp:%d %b %Y} -> EDD {edd:%d %b %Y}; on {visit:%d %b %Y} GA = {weeks} weeks {extra} days ({days} days)")
print(f"Fundal height {fh} cm -> {mcd_weeks:.1f} weeks ({mcd_months:.1f} months) by McDonald; GTPAL = G{g} T{t} P{p} A{a} L{living}")
```

```text
LMP 12 Oct 2025 -> EDD 19 Jul 2026; on 01 Feb 2026 GA = 16 weeks 0 days (112 days)
Fundal height 32 cm -> 36.6 weeks (9.1 months) by McDonald; GTPAL = G4 T2 P0 A1 L2
```

With the LMP on 12 October 2025 the EDD is **19 July 2026**; on 1 February 2026 she is **16 weeks 0 days** (112 days). A fundal height of 32 cm corresponds to **36.6 weeks** (9.1 months by the 3.5 rule), and the GTPAL is **G4 T2 P0 A1 L2**.

## 2.5 Physiological changes of pregnancy

Pregnancy changes every system, driven by **hCG** (first trimester), **progesterone** (relaxes smooth muscle), **oestrogen** (growth, blood flow), **relaxin** (softens ligaments), **hPL** (raises maternal glucose) and **prolactin** (prepares the breast). Figure 2.3 maps the hormones to the organs, and the table gives the numbers.

```svgfig label="2.3" caption="From hormone to organ. Progesterone relaxes smooth muscle (slow gut, reflux, constipation, ureter dilation, vein dilation), oestrogen increases blood flow and growth (uterus, breast, skin pigmentation, vaginal discharge), relaxin softens joints (backache), hPL makes the mother insulin-resistant to save glucose for the baby, and hCG in the first trimester supports the corpus luteum (nausea peaks when hCG peaks at 8-12 weeks)."
f = Fig(760, 330)
f.box(15, 100, 190, 130, "HORMONES\nhCG (weeks 1-12)\nprogesterone, oestrogen\nrelaxin, hPL, prolactin", fill=SAND, stroke=AMBER, size=10.5, bold=True)
spec = [(260, 15, "UTERUS: 50 g to 1,000 g\nlength 7.5 to 30 cm", BLUE, NAVY), (510, 15, "BLOOD: volume +40-50%\nHb falls (haemodilution)", ROSE, RED),
        (260, 125, "LUNGS: tidal volume +30-40%\nbreathless, PaCO2 30 mmHg", MINT, TEAL), (510, 125, "KIDNEY: GFR +50%\nfrequency, glucosuria", BLUE, NAVY),
        (260, 235, "GUT: slow transit\nnausea, reflux, constipation", SAND, AMBER), (510, 235, "SKIN, BREAST, JOINTS\nlinea nigra, striae, backache", MINT, TEAL)]
for x, y, s, fl, st in spec:
    f.box(x, y, 235, 75, s, fill=fl, stroke=st, size=10.5, bold=True)
    f.arrow([(205, 165), (x, y + 37)], color=SLATE, sw=1.4)
```

| System | Change (numbers) | What the midwife does with it |
|---|---|---|
| Uterus | 50 g to about 1,000 g; length 7.5 to 30 cm; capacity 10 mL to 5 L; blood flow 500-700 mL/min at term | Measure fundal height; teach that sudden severe pain or bleeding is never normal |
| Cervix and vagina | Chadwick's blue colour, Goodell's softness, mucus plug, more discharge (pH 3.5-4.5) | Do not mistake white discharge for infection unless itchy or foul |
| Breast | Larger, tender, Montgomery's tubercles, colostrum from 16 weeks | Advise a supportive bra and nipple preparation by the mother's choice only |
| Blood and heart | Blood volume +40-50% (+1.2 to 1.8 L), cardiac output +30-50%, heart rate +10-15 per minute, BP lowest at 20-24 weeks, fibrinogen rises | Expect a flow murmur; avoid lying flat on the back (**supine hypotension**); anaemia is Hb below 11 g/dL (first and third trimester) |
| Lungs | Tidal volume +30-40%, subcostal angle widens, oxygen use +20% | Normal breathlessness is mild; severe breathlessness needs a check for anaemia, heart disease or pulmonary embolism |
| Kidney | GFR +50%, ureters dilate (right more), bladder pressed in first and third trimesters | Frequency is normal; burning or loin pain is a urinary infection; test urine for protein and sugar at every visit |
| Gut | Slowed motility, relaxed cardiac sphincter, gums bleed, gallstones more likely | Small frequent meals; fibre; fluids |
| Metabolism | Weight gain 11.5-16 kg (normal BMI), energy +340 kcal (2nd) and +450 kcal (3rd trimester), insulin resistance | Plot weight at each visit; screen for gestational diabetes at 24-28 weeks |
| Skin and joints | Linea nigra, chloasma, striae, ligament laxity | Reassure; teach posture |

**Anaemia is the commonest threat in Nepal.** Plasma volume rises by about 50% but red cells by only 20-30%, so haemoglobin falls even in a healthy woman ("physiological anaemia"). Below the WHO limit of **11 g/dL** (10.5 in the second trimester) the woman is anaemic: mild 10.0-10.9, moderate 7.0-9.9 and severe below 7.0 g/dL. The NDHS 2022 found 34% of women anaemic, and the national programme gives every pregnant woman **180 tablets of iron (60 mg) plus folic acid (400 micrograms)**, one daily from the fourth month, and albendazole after the first trimester.

```python
plasma0, rbc0 = 2.7, 1.8                       # litres, non-pregnant (total 4.5 L)
plasma1 = plasma0 * 1.50                       # plasma +50%
rbc1 = rbc0 * 1.25                             # red cells +25%
total0, total1 = plasma0 + rbc0, plasma1 + rbc1
hct0, hct1 = rbc0 / total0 * 100, rbc1 / total1 * 100
print(f"Blood volume {total0:.1f} L -> {total1:.1f} L (+{total1 - total0:.1f} L, +{(total1 / total0 - 1) * 100:.0f}%)")
print(f"Haematocrit falls from {hct0:.0f}% to {hct1:.1f}% (physiological haemodilution)")
```

```text
Blood volume 4.5 L -> 6.3 L (+1.8 L, +40%)
Haematocrit falls from 40% to 35.7% (physiological haemodilution)
```

The blood volume rises from 4.5 L to **6.3 L** (**+1.8 L, +40%**), and the haematocrit falls from 40% to **35.7%**: the "anaemia" of pregnancy is mostly dilution, but a true iron shortage must still be treated.

**Psychological changes.** In the **first trimester** the mother is often ambivalent, tired and moody; in the **second** she feels well and bonds as she feels the baby move; in the **third** she is anxious about labour and may "nest". Fathers may have anxiety too. Listen without judging and involve the family. A mother who is sad for more than two weeks needs screening for antenatal depression (Unit 5 and Psychiatric Nursing).

## 2.6 Eight minor disorders of pregnancy and their care

Minor disorders are common and not dangerous, but they can ruin a woman's life if no one listens. The midwife first rules out the dangerous cause, then offers non-drug measures.

1. **Nausea and vomiting (morning sickness).** It affects about 70% of women between 6 and 14 weeks, linked to hCG. Advise dry biscuits before rising, small frequent meals, ginger or lemon drinks, and avoiding strong smells. Refer if she vomits more than 3 times a day, loses weight, or has ketones in the urine (hyperemesis gravidarum needs a drip and thiamine).
2. **Heartburn.** The relaxed gastro-oesophageal sphincter and the pressing uterus push acid upward, mostly after 28 weeks. Advise small meals, no lying down for 2 hours after eating, extra pillows, and avoiding spicy and fried food. The doctor may add an antacid. Severe epigastric pain with headache is pre-eclampsia, not heartburn.
3. **Constipation and haemorrhoids.** Progesterone slows the gut and iron tablets add to it. Advise 2-3 litres of fluid, fibre (vegetables, *saag*, fruit, whole grain) and daily walking, and never to strain. For piles use sitz baths and cold compresses. Bleeding that is heavy or painful needs a check.
4. **Backache and symphysis pain.** Relaxin loosens joints and the weight of the uterus shifts the centre of gravity. Teach good posture, flat low-heeled shoes, bending at the knees, a firm mattress, warm packs and pelvic rocking. A support belt may help. Fever with loin pain suggests infection.
5. **Leg cramps.** They occur at night in the second and third trimesters, linked to low calcium or tired muscles. Teach calf stretching before bed (toes pulled to the knee), warm massage and a calcium tablet of 500 mg daily as per national protocol. A painful swollen red calf is a possible deep vein thrombosis and needs urgent referral.
6. **Frequency of micturition.** The uterus presses on the bladder in the first and third trimesters. Reassure her, reduce fluids at night but not by day, and teach her to lean forward when passing urine to empty fully. Pain, burning or fever means urinary tract infection and needs a urine test.
7. **Vaginal discharge (leucorrhoea).** Increased oestrogen produces a thin, white, non-smelly discharge. Advise cotton underwear, washing with water, wiping front to back and no douching. If it is itchy, curdy, green or foul, suspect candida, trichomonas or bacterial vaginosis and treat after testing.
8. **Oedema of the feet and varicose veins.** The uterus presses on the pelvic veins and progesterone dilates them, so ankles swell by evening. Advise resting with the feet raised, lying on the left side, avoiding long standing and wearing support stockings. **Swelling of the face and hands with raised BP or headache is pre-eclampsia** and must be sent to hospital the same day.

## Formula and fact sheet

- **EDD** = LMP + 7 days - 3 months (+1 year) = LMP + 280 days; term 37-41 weeks. **GA** = days since LMP ÷ 7 (weeks) with remainder days.
- **McDonald:** weeks = fundal height (cm) × 8/7; months = cm ÷ 3.5; after 24 weeks cm = weeks ± 2.
- **GTPAL:** Gravida, Term, Preterm, Abortions, Living. Anaemia in pregnancy: Hb under 11 g/dL (mild 10-10.9, moderate 7-9.9, severe under 7).
- hCG test: 20-25 mIU/mL, positive 10-14 days after fertilisation; sac on scan 5 weeks, heartbeat 6 weeks, Doppler 10-12 weeks, Pinard 18-20 weeks.
- Blood volume +40-50%; GFR +50%; cardiac output +30-50%; weight gain 11.5-16 kg for BMI 18.5-24.9 (IOM 2009).
- National IFA: 180 tablets (60 mg iron + 400 mcg folic acid) from the 4th month; folic acid 400 mcg pre-conception.

## Chapter summary

- Well-woman and pre-conception care (folic acid, immunisation, nutrition, chronic disease, substances, spacing, genetics, mental health) prevent problems that begin in the first weeks.
- Diagnose pregnancy with presumptive, probable and positive signs; only ultrasound, fetal heart sounds and fetal parts are positive.
- Use Naegele's rule or early ultrasound for the EDD, record GTPAL, and check growth with fundal height and McDonald's rule.
- Hormones remodel every system; the blood volume rises more than the red cells, so haemoglobin falls; the midwife separates normal from dangerous.
- Minor disorders get non-drug care; red flags (vomiting with weight loss, calf pain, facial oedema, burning urine, foul discharge) need referral.

## Practice

```python
from datetime import date, timedelta
m1 = date(2026, 1, 20) + timedelta(days=280)                  # MCQ1 EDD for LMP 20 Jan 2026
m3 = 4.5 * 0.40                                                # MCQ3 rise in blood volume, litres
lmp = date(2025, 9, 8)
edd = lmp + timedelta(days=280)
visit = date(2026, 1, 18)
days = (visit - lmp).days
w, d = divmod(days, 7)
weight, height = 52, 1.55
bmi = weight / height ** 2
lo, hi = weight + 11.5, weight + 16
hb = 9.8
band = "severe" if hb < 7 else "moderate" if hb < 10 else "mild" if hb < 11 else "normal"
tablets = 2 * 30                                               # two 60-mg tablets a day for 30 days
iron_mg = 2 * 60
print(f"MCQ1 = {m1:%d %b %Y}; MCQ3 = {m3:.1f} L")
print(f"Kalpana: LMP {lmp:%d %b %Y} -> EDD {edd:%d %B %Y}; on {visit:%d %b %Y} GA = {w} weeks {d} days; BMI {bmi:.1f}; target weight {lo:.1f}-{hi:.1f} kg")
print(f"Hb {hb} g/dL = {band} anaemia; treatment {iron_mg} mg iron a day = {tablets} tablets for 30 days")
```

```text
MCQ1 = 27 Oct 2026; MCQ3 = 1.8 L
Kalpana: LMP 08 Sep 2025 -> EDD 15 June 2026; on 18 Jan 2026 GA = 18 weeks 6 days; BMI 21.6; target weight 63.5-68.0 kg
Hb 9.8 g/dL = moderate anaemia; treatment 120 mg iron a day = 60 tablets for 30 days
```

**MCQs (with reasons)**

1. A woman's LMP was 20 January 2026. Her EDD by Naegele's rule is: (a) 20 October 2026 (b) 27 October 2026 (c) 27 November 2026 (d) 20 July 2026.
2. A woman in her third pregnancy has two living term children. Her GTPAL is: (a) G3 T2 P0 A0 L2 (b) G2 T2 P0 A0 L2 (c) G3 T3 P0 A0 L2 (d) G2 T1 P1 A0 L2.
3. The blood volume of a non-pregnant woman (4.5 L) rises by 40%. The increase is: (a) 0.9 L (b) 1.8 L (c) 2.7 L (d) 3.6 L.
4. Hegar's sign is: (a) bluish vagina (b) softening of the isthmus of the uterus (c) a fetal kick (d) a dark midline on the abdomen.
5. For heartburn in the third trimester the best advice is: (a) lie flat after meals (b) small frequent meals and raised head (c) stop iron tablets forever (d) drink only milk at night.

::: note Answers and rationales
**1. (b).** 20 January + 7 days = 27 January; minus 3 months gives October 2025, so the year moves on to **27 October 2026**; (a) forgets the 7 days and (d) subtracts 6 months.
**2. (a).** Gravida counts the present pregnancy (3), two were term (T2) and none preterm or aborted; (b) forgets the present one.
**3. (b).** 4.5 × 0.40 = 1.8 L; 0.9 L is a 20% rise.
**4. (b).** Hegar's sign is a soft compressible isthmus at 6-8 weeks (probable sign); (a) is Chadwick's, (c) is a positive sign and (d) a presumptive skin sign.
**5. (b).** Small meals and an upright position reduce reflux; lying flat worsens it, and iron should continue, with food, for anaemia.
:::

**Short answer (3 marks): Name the probable signs of pregnancy.** Probable signs are found by the examiner: enlargement of the uterus and abdomen, **Hegar's sign** (soft isthmus, 6-8 weeks), **Chadwick's sign** (bluish vagina and cervix), **Goodell's sign** (soft cervix), **Braxton Hicks** contractions, **ballottement** (16-28 weeks) and a positive urine or serum hCG test. They are strong evidence but can be caused by other conditions (for example a molar pregnancy), so only fetal heart sounds, fetal parts felt by the examiner and ultrasound are *positive* signs.

**Medium answer (5 marks): Describe the cardiovascular and haematological changes of pregnancy and their importance in nursing (Figure 2.3).** Blood volume rises by 40-50% (about 1.8 L, from 4.5 L to 6.3 L), beginning at 6 weeks and peaking at 32-34 weeks. Plasma rises about 50% and red cells 20-25%, so **haemoglobin and haematocrit fall** (physiological haemodilution); anaemia is Hb under 11 g/dL. Cardiac output rises 30-50% and heart rate by 10-15 beats per minute; blood pressure falls in the second trimester (lowest at 20-24 weeks) and returns to baseline at term. The enlarged uterus can compress the vena cava when she lies flat, causing **supine hypotension syndrome**, so she is advised to lie on her left side. Clotting factors and fibrinogen rise, which protects against bleeding but increases the risk of thrombosis. Nursing importance: check Hb at the first visit and at 28-36 weeks, give 180 iron-folic acid tablets, teach food sources, rest on the left side, avoid long standing and look for signs of heart failure in women with cardiac disease. A flow murmur is normal but a loud diastolic murmur is not.

**Long answer (10 marks): Kalpana Rai, 24 years, G2 P1 L1, comes to the health post at 18 weeks 6 days (LMP 8 September 2025). She weighs 52 kg and is 155 cm tall; fundal height is 19 cm, Hb is 9.8 g/dL. She complains of nausea, heartburn, backache and constipation. Calculate her EDD, BMI and weight-gain target, classify her anaemia and write the care plan.**

*Calculations.* Naegele's rule gives an **EDD of 15 June 2026** (LMP + 280 days), and on 18 January 2026 she is **18 weeks 6 days**; the fundal height of 19 cm lies between the symphysis and the umbilicus, in line with the date. Her **BMI is 21.6** (52 ÷ 1.55²), which is normal, so the recommended gain is **11.5-16 kg** (target weight 63.5-68.0 kg). With Hb **9.8 g/dL** she has **moderate anaemia** (7.0-9.9), and the treatment dose is two 60-mg iron tablets daily (120 mg iron) which is 60 tablets for 30 days, with Hb repeated in 4 weeks and a rise of at least 1 g/dL expected in 2-3 weeks; the doctor or the national protocol decides the dose.

*Care.* The midwife first excludes danger signs (bleeding, fever, burning urine, severe vomiting, headache, blurred vision). She takes a dietary history and teaches iron-rich foods (*saag*, lentils, liver, eggs, jaggery) taken with vitamin C (citrus, tomato) and not with tea. She gives iron after food, at night, with water and warns about dark stools. Nausea is managed with dry biscuits, ginger and small meals; heartburn with small meals and an upright posture; constipation with fluids, fibre and walking; and backache with posture, flat shoes and a firm bed. She records weight, BP, urine, fundal height and fetal heart, gives albendazole, Td and calcium as per protocol, completes a birth preparedness plan, and schedules the next visit at 6 months.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "I feel sick all day." **O:** vomits twice a day, weight 52 kg, no ketones. | **Nausea** related to hormonal changes of early pregnancy. | **Nausea severity:** no vomiting and eats 5 small meals within 1 week. | Dry biscuit before rising, ginger tea, small meals (empty stomach worsens nausea); avoid strong smell; review weight (detects hyperemesis early). | Vomiting stops; eating well. |
| **O:** Hb 9.8 g/dL, pallor, diet low in iron and protein. | **Imbalanced nutrition: less than body requirements** related to inadequate iron intake, as evidenced by Hb 9.8. | **Nutritional status:** Hb 11 g/dL or more by 28 weeks. | Give iron 120 mg daily after food (corrects deficiency); teach saag, lentils, eggs, vitamin C (better absorption); avoid tea with meals (blocks iron); deworm; recheck Hb in 4 weeks (assesses response). | Hb 10.8 at 4 weeks; takes tablets. |
| **S:** "My back hurts at night." **O:** mild lumbar tenderness, no fever. | **Acute pain** related to ligament laxity and posture, as evidenced by backache. | **Pain level:** pain 2/10 or less within 1 week. | Teach posture, flat shoes, bending knees (reduce strain); warm pack, pelvic rocking (relax muscle); firm bed (supports spine). | Pain 1/10; sleeps well. |
| **S:** "I pass stool every 3 days, and I have heartburn." **O:** hard stool, belching. | **Constipation** related to progesterone and iron; heartburn from sphincter relaxation. | **Bowel elimination:** soft stool daily within 3 days. | Fluids 2-3 L, fibre, walking (stimulate gut); small meals, raised pillows (limit reflux); do not strain (avoids piles). | Soft stool daily; heartburn less. |
| **S:** "Is it safe?" **O:** first visit at 18 weeks, no birth plan, no knowledge of danger signs. | **Deficient knowledge** related to lack of exposure to antenatal information. | **Knowledge:** names 5 danger signs and the next visit date before leaving. | Teach danger signs, ANC schedule (months 4, 6, 8, 9), IFA and calcium use, nutrition (informed mothers attend more); give a card; involve husband. | Repeats 5 danger signs; booked. |
