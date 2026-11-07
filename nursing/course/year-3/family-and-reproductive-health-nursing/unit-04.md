---
subject: Family and Reproductive Health Nursing
grade: BSc Nursing Year 3
unit: 4
title: Gynaecological Disorders and Cancers: Cervical Screening, Breast, Prolapse and Hysterectomy
hours: 24
area: BSN 23-24 · Family and Reproductive Health Nursing · Units 1-5
---

Mina Gurung, **45 years old**, a mother of four from Gorkha, attends a **cervical cancer screening camp** organised by the municipality. She has had **white watery discharge for 6 months** and **bleeding after intercourse** twice. She has never been screened and was never vaccinated. The nurse at the camp performs **visual inspection with acetic acid (VIA)**: a white lesion touches the squamocolumnar junction, so the test is **positive**. This case shows the gap that Nepal's programme tries to close: a disease that can be **prevented by vaccine, found early by a simple test and cured when found early**, yet still kills many women.

::: key What this unit gives you
- Real images: a **historic speculum engraving**, a **normal Pap smear**, a **cervical cancer cytology smear**, a **Pap stain field**, a **mammogram being taken**, **fibroid specimens**, a **prolapse illustration** and a **ring pessary**; each with numbered marks.
- SVG figures: the **natural history of cervical cancer with prevention points**, the **screen-and-treat algorithm**, and the **pelvic organ prolapse ladder**.
- **Eight points of nursing responsibility in a pelvic examination and Pap or VIA test**, **seven points of cervical cancer prevention education** and **eight points of nursing care after hysterectomy**, each in 3-4 plain sentences anchored in MoHP and Nepal practice.
- Verified maths: **sensitivity, specificity, PPV and NPV of VIA and HPV tests, screening coverage, HPV vaccine doses, body surface area for cisplatin and IV drip rate**; MCQs, short, medium and long answers and a 5-column NANDA-I plan.
:::

## 4.1 Gynaecological assessment and the pelvic examination

The **gynaecological history** covers the **chief complaint** (discharge, bleeding, pain, lump, itching, urinary or bowel symptoms), the **menstrual history** (age at menarche, cycle, flow, LMP, post-coital and post-menopausal bleeding), the **obstetric history** (GTPAL), **contraception**, **sexual history**, **past infections and surgery**, **screening history** and **family history of breast, ovarian or colon cancer**. **Examination:** general (pallor, weight, blood pressure), **breast**, **abdomen** (mass, tenderness), then the **pelvic examination**: inspection of the vulva, **speculum examination** (cervix colour, ectropion, discharge, growth, bleeding; Cusco's bivalve or Sims' speculum), **Pap smear or VIA**, and **bimanual examination** (uterine size, position, mobility, adnexal mass, cervical motion tenderness, and prolapse by asking the woman to cough). Culture of the discharge is taken before the bimanual.

### Eight points of nursing responsibility in a pelvic examination and Pap or VIA test

1. **Explain and obtain consent.** Describe the steps in simple Nepali, show the speculum and say that it may feel uncomfortable but should not hurt. Ask for permission and tell her she can stop at any time. A woman who understands is relaxed and allows a better view.
2. **Ensure privacy and dignity.** Use a closed room and a screen, cover her with a sheet, and keep a female attendant if she wishes. Shame is the main reason women avoid screening in Nepal. Respectful care brings them back.
3. **Prepare the woman.** Ask her to empty the bladder, avoid douching, vaginal creams or sex for 24-48 hours before a Pap smear, and not to come during heavy menstrual bleeding. Correct preparation gives a readable sample and avoids repeating the test.
4. **Prepare the tray and light.** Check a sterile or high-level disinfected speculum, spatula and brush, glass slides with pencil labels, fixative, 3-5% acetic acid, cotton swabs, gloves and a good light. A ready tray shortens the time and avoids contamination.
5. **Position and support the woman.** Help her into the lithotomy position with the legs supported, talk to her during the test, and ask her to breathe slowly and relax the thighs. Distraction lowers fear and muscle spasm.
6. **Assist and label correctly.** Hand the instruments, apply acetic acid, record the VIA findings (white lesion, size, relation to the squamocolumnar junction) and fix the Pap slide at once with the woman's name and number written in pencil. Wrong labels cause the worst error in screening, a wrong result for the wrong woman.
7. **Infection prevention.** Wear gloves, wash hands, soak the instruments in 0.5% chlorine, then clean and sterilise or high-level disinfect them, and dispose of waste safely. This protects the next woman from HIV, HPV and other infection.
8. **Give the result and follow up.** Explain when the result comes, who will tell her, and what happens if it is abnormal. Record in the register and HMIS and trace women who do not return. Screening saves lives only when abnormal results are followed.

## 4.2 Cervical cancer: prevention, screening and treatment

**Cervical cancer** is among the commonest cancers of Nepali women (with breast cancer). Nearly all cases are caused by **persistent infection with high-risk human papillomavirus (HPV)**, especially **types 16 and 18, which cause about 70% of cases**. Most HPV infections clear in 1-2 years; in a few women the virus persists and over **10-15 years** the cells pass through **CIN 1, CIN 2 and CIN 3** (cervical intraepithelial neoplasia) to invasive cancer. **Risk factors:** early first intercourse, many partners (or a partner with many), early and many pregnancies, **smoking**, **HIV infection**, long use of the pill, poor genital hygiene, and **no screening**. **Symptoms:** watery, foul or blood-stained discharge, **post-coital** and **intermenstrual bleeding**, postmenopausal bleeding and, late, back and leg pain, urinary or rectal symptoms.

```svgfig label="4.1" caption="The natural history of cervical cancer and the three levels of prevention. HPV infection takes 10-15 years to become cancer, so a vaccine given before exposure, a screening test after age 30 and treatment of precancer each break the chain."
f = Fig(760, 330)
st = [("HPV INFECTION", "sexual contact\nmost clear in 1-2 years"), ("PERSISTENT HPV", "types 16 and 18\nhigh-risk types"), ("PRECANCER", "CIN 1, CIN 2, CIN 3\n(5-15 years)"), ("INVASIVE CANCER", "stage I to IV\nspreads to nodes, bladder"), ("DEATH OR CURE", "early: cure over 90%\nlate: under 30%")]
cols = [(MINT, TEAL), (BLUE, NAVY), (SAND, AMBER), (ROSE, RED), (ROSE, RED)]
for i, (a_, b_) in enumerate(st):
    x = 15 + i * 147
    f.box(x, 12, 140, 34, a_, fill=NAVY, stroke=NAVY, color="#ffffff", size=10, bold=True)
    f.box(x, 56, 140, 56, b_, fill=cols[i][0], stroke=cols[i][1], size=10)
    if i < 4: f.arrow([(x + 140, 29), (x + 147, 29)], color=SLATE, sw=2)
f.box(15, 140, 280, 70, "PRIMARY PREVENTION\nHPV vaccine for girls 9-14 years\nsingle dose in Nepal from 2025\ncondoms, no tobacco, delay first sex", fill=MINT, stroke=TEAL, size=10, bold=True)
f.box(310, 140, 215, 70, "SECONDARY PREVENTION\nVIA or HPV test at 30-60 years\nevery 5 years (Nepal guideline)", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.box(540, 140, 205, 70, "TERTIARY CARE\nsurgery, chemoradiation,\nbrachytherapy, palliative care", fill=SAND, stroke=AMBER, size=10, bold=True)
f.box(15, 228, 730, 44, "Nepal screens only a small share of eligible women; the aim is 70% of women aged 30-60 years screened", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(15, 284, 730, 36, "Stage at diagnosis decides survival: nurses can move the stage to the left by screening and referral", fill=SAND, stroke=AMBER, size=10.5)
```

**Screening in Nepal.** The national guideline recommends **VIA** (3-5% acetic acid, naked-eye look after 1 minute, white lesion near the transformation zone is positive) for women **30-60 years, every 5 years**; **women living with HIV** are screened from diagnosis and every 3 years. **WHO prefers the HPV DNA test** (sensitivity about 90%) every 5-10 years, with self-sampling possible, and Nepal is moving towards it. The **Pap smear** (cytology, Bethesda reporting: ASC-US, LSIL, HSIL, cancer) is done every 3 years in hospitals. **Colposcopy and biopsy** confirm CIN. **HPV vaccination** is given free in the NIP; the 2025 revised schedule uses a **single dose** for adolescent girls (follow the current MoHP circular for the age group).

**Treatment.** *Precancer (CIN 2-3 or VIA positive with a lesion that covers less than three-quarters of the cervix and is not in the canal):* **thermal ablation** or **cryotherapy** in one visit at primary level; larger lesions need **LEEP** (loop excision) or cone biopsy at a referral centre. *Invasive cancer* by **FIGO stage**: **IA** microscopic, **IB** confined to cervix, **II** upper two-thirds of vagina or parametrium, **III** lower vagina, pelvic wall or hydronephrosis, **IV** bladder, rectum or distant spread. Stage **IB1-IIA** is treated with **radical hysterectomy and node dissection** or radiotherapy; stage **IIB-IVA** with **concurrent chemoradiation (external beam radiotherapy with weekly cisplatin 40 mg/m²) followed by brachytherapy**. Referral centres in Nepal include the **B.P. Koirala Memorial Cancer Hospital (Bharatpur)**, **Bhaktapur Cancer Hospital**, **Kathmandu Cancer Centre** and TUTH. Palliative care and morphine are given for advanced disease.

```svgfig label="4.2" caption="The screen-and-treat algorithm used at primary level. A negative test means rescreening in 5 years; a positive test leads to ablation if the lesion is eligible, to LEEP or referral if not, and to biopsy and referral if cancer is suspected. Every positive woman is traced until treated."
f = Fig(760, 330)
f.box(270, 8, 220, 36, "WOMAN 30-60 years\nVIA or HPV test", fill=NAVY, stroke=NAVY, color="#ffffff", size=10.5, bold=True)
f.box(15, 80, 200, 50, "NEGATIVE\nrescreen in 5 years\n(3 years if HIV positive)", fill=MINT, stroke=TEAL, size=10.5)
f.box(280, 80, 200, 50, "POSITIVE\ncheck lesion size and canal", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(545, 80, 200, 50, "SUSPICIOUS FOR CANCER\nirregular growth, bleeding", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.arrow([(380, 44), (115, 80)], color=SLATE, sw=1.8)
f.arrow([(380, 44), (380, 80)], color=SLATE, sw=1.8)
f.arrow([(380, 44), (645, 80)], color=SLATE, sw=1.8)
f.box(190, 165, 210, 56, "ELIGIBLE\nthermal ablation or\ncryotherapy at the same visit", fill=MINT, stroke=TEAL, size=10.5)
f.box(15, 165, 160, 56, "NOT ELIGIBLE\nLEEP or referral", fill=BLUE, stroke=NAVY, size=10.5)
f.box(545, 165, 200, 56, "BIOPSY and urgent referral\nto cancer centre", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.arrow([(380, 130), (295, 165)], color=SLATE, sw=1.8)
f.arrow([(380, 130), (95, 165)], color=SLATE, sw=1.8)
f.arrow([(645, 130), (645, 165)], color=SLATE, sw=1.8)
f.box(15, 245, 730, 36, "FOLLOW UP: review at 6 and 12 months after treatment; trace every positive woman by phone and FCHV", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(15, 292, 730, 30, "Record in the register and HMIS; counsel on HPV vaccination of daughters", fill=BLUE, stroke=NAVY, size=10)
```

```photogrid label="4.1" cols="4" ratio="1.0" caption="Cervical screening in real images. (a) An old engraving of bivalve and Sims-type vaginal specula; a modern speculum has the same two blades. (b) A normal Pap smear: flat superficial squamous cells with small nuclei. (c) A cytology smear from a cervical cancer, with clustered cells with large dark nuclei. (d) A Pap-stained field seen through the microscope."
@ photo id="nur14/speculum" cap="Engraving of vaginal specula"
fit 1.0
focus 0.5 0.6
mark 0.5 0.75 "1"
key 1 (a) Bivalve speculum with two blades
@ photo id="nur14/papwnl" cap="Normal Pap smear"
fit 1.0
focus 0.5 0.5
mark 0.55 0.5 "2"
key 2 (b) Flat squamous cells, small nuclei
@ photo id="nur14/cacx" cap="Cancer cytology smear"
fit 1.0
focus 0.5 0.5
mark 0.5 0.55 "3"
key 3 (c) Cell cluster with large dark nuclei
@ photo id="nur14/papsmear" cap="Pap-stained cervical smear"
fit 1.0
focus 0.5 0.5
mark 0.5 0.5 "4"
key 4 (d) Stained cells in the microscope field
```

### Seven points of cervical cancer prevention education

1. **Explain that the disease is caused by a virus and is preventable.** Tell women that HPV spreads by sexual contact, that most infections clear, and that cancer takes 10-15 years to grow. This removes blame and shows that there is time to act.
2. **Promote HPV vaccination of girls.** Explain that the free vaccine works best before the first sexual contact and that mothers should take their daughters to the school or health post session. A vaccinated girl is protected against about 70% of cervical cancers.
3. **Invite every woman of 30-60 years for screening.** Say it takes about 5 minutes, is painless, and the result is known at once with VIA. Use FCHVs, mothers' groups and camps. A woman screened once in 5 years is largely protected.
4. **Teach the warning signs.** Tell women to come at once for bleeding after sex, between periods or after menopause, and for foul or blood-stained discharge. Do not wait for a screening day. Early symptoms mean a curable stage.
5. **Advise safe sexual practice.** Teach condom use, one faithful partner and delaying the first sex until adulthood. Condoms lower HPV spread and also prevent HIV. Men need the message as well.
6. **Stop tobacco and treat infections.** Smoking doubles the risk and damages cervical immunity; advise cessation and treat vaginal infections early. Women living with HIV need screening more often. Simple steps reduce persistence of HPV.
7. **Follow up positives and counsel the family.** Trace every woman with a positive result until she is treated, explain that treatment is simple for precancer, and involve the husband. A woman who is lost after a positive test gains nothing from screening.

## 4.3 Breast and other gynaecological cancers

**Breast cancer** is the commonest cancer of women worldwide and among the two commonest in Nepal. **Risk factors:** age, family history or **BRCA1/2** mutation, early menarche and late menopause, no childbirth or late first birth, obesity, alcohol and past chest radiation. **Features:** a **painless, hard, irregular, fixed lump** (often upper outer quadrant), **skin dimpling or peau d'orange**, **nipple retraction or bloody discharge**, **enlarged axillary nodes**. **Triple assessment:** clinical examination, imaging (**mammography** from 40 years, ultrasound in younger women) and **core needle biopsy**. Staging is by **TNM**. Treatment combines **surgery** (breast-conserving or mastectomy with sentinel node), **radiotherapy**, **chemotherapy**, **tamoxifen 20 mg daily for 5-10 years** for hormone-receptor-positive disease and **trastuzumab** for HER2-positive disease. **Breast self-examination (BSE)** is taught to raise awareness: monthly, **5-7 days after the period** (or the same day each month after menopause): (1) look in a mirror with arms down and then raised for shape, dimpling and nipple change; (2) lie down with a pillow under the shoulder; (3) use the three middle finger pads in small circles with light, medium and firm pressure; (4) cover the whole breast and armpit in a **vertical strip pattern**; (5) squeeze each nipple gently. Any lump that persists for a cycle needs a clinic visit.

**Ovarian cancer** is often found late: persistent **bloating, early satiety, pelvic pain and urinary frequency**; **CA-125** (above 35 U/mL) and ultrasound; treated with surgery and **carboplatin and paclitaxel**. **Endometrial cancer** presents with **postmenopausal bleeding** (risk: obesity, diabetes, unopposed oestrogen, PCOS, tamoxifen); the test is an **endometrial biopsy** and the treatment is **hysterectomy with salpingo-oophorectomy**.

**Common benign conditions.** **Fibroids (leiomyomas)** are the commonest benign tumours (submucosal, intramural, subserosal): heavy periods and anaemia, pressure on the bladder and rectum, and sometimes infertility; managed by **observation, tranexamic acid, iron, GnRH analogues, myomectomy, uterine artery embolisation or hysterectomy**. **Endometriosis** (endometrial tissue outside the uterus) causes **severe dysmenorrhoea, deep dyspareunia, chronic pelvic pain and infertility**; diagnosed by laparoscopy and treated with **NSAIDs, hormonal suppression (COC, progestin, GnRH analogues)** and surgery. **Pelvic inflammatory disease (PID)** is explained with STIs in Unit 5.

```photogrid label="4.2" cols="4" ratio="1.0" caption="Breast and pelvic floor problems. (a) A woman having a mammogram: the breast is compressed between two plates for a low-dose X-ray. (b) A cut uterine fibroid: a round, well-defined, whorled mass in the muscle wall. (c) An illustration of uterine prolapse, with the uterus, bladder, rectum and vaginal wall labelled. (d) A ring-type pessary with a support disc, a device that holds a prolapsed uterus in place."
@ photo id="nur14/mammo" cap="Mammography"
fit 1.0
focus 0.45 0.5
mark 0.45 0.5 "1"
key 1 (a) Breast positioned between the plates
@ photo id="nur14/fibroid" cap="Cut uterine fibroid"
fit 1.0
focus 0.5 0.5
mark 0.5 0.5 "2"
key 2 (b) Rounded, whorled fibroid in the uterine wall
@ photo id="nur14/prolapse" cap="Uterine prolapse illustration"
fit 1.0
focus 0.5 0.55
mark 0.55 0.72 "3"
key 3 (c) Uterus descending into the vagina
@ photo id="nur14/pessary" cap="Support pessary"
fit 1.0
focus 0.5 0.5
mark 0.5 0.45 "4"
key 4 (d) Pessary frame with support disc
```

## 4.4 Pelvic organ prolapse and hysterectomy

**Pelvic organ prolapse (POP)** is the descent of the uterus, bladder (cystocele) or rectum (rectocele) into the vagina when the pelvic floor muscles and ligaments are weak. It is a **major hidden problem in Nepal**: studies report that **about 10% to over 30%** of women have some degree of uterine prolapse, because of **early, frequent and unattended childbirth, heavy lifting soon after birth, malnutrition, and menopause**. Symptoms are a **dragging sensation or lump at the vulva**, back pain, urinary frequency, leakage on coughing or difficulty in emptying, ulceration and discharge. **POP-Q stages:** **0** no prolapse; **I** the lowest point is more than 1 cm above the hymen; **II** within 1 cm above or below the hymen; **III** more than 1 cm below the hymen; **IV** complete eversion. Management: **pelvic floor (Kegel) exercises**, weight reduction, treating cough and constipation, **ring pessary** (fitted and changed every 3-6 months with vaginal oestrogen cream, checked for ulcers), and **surgery** (vaginal hysterectomy with repair, sacrospinous fixation, or colpocleisis in older women). MoHP and partners run **free prolapse surgery camps** in districts; the nurse identifies cases, counsels and refers. **Prevention:** four ANC visits and facility birth, no heavy loads for 6 weeks after delivery, birth spacing, and good nutrition.

```svgfig label="4.3" caption="The pelvic organ prolapse ladder (POP-Q). The hymen is the reference line. The cervix or lowest point sits above the hymen in stages I and II and passes beyond it in stages III and IV; the nurse's advice and the treatment step up with the stage."
f = Fig(760, 330)
f.line(300, 150, 460, 150, color=RED, sw=3)
f.text(335, 170, "HYMEN LINE", size=10.5, color=RED, bold=True)
levels = [("STAGE 0\nnormal support", 33), ("STAGE I\nmore than 1 cm above", 83), ("STAGE II\nwithin 1 cm of hymen", 150), ("STAGE III\nmore than 1 cm below", 183), ("STAGE IV\ncomplete eversion", 233)]
for i, (t_, y) in enumerate(levels):
    f.circle(380, y if i != 2 else 150, 10, fill=SAND if i < 2 else ROSE, stroke=AMBER if i < 2 else RED, label=str(i))
    f.box(480, 12 + i * 50, 265, 42, t_, fill=[MINT, MINT, SAND, ROSE, ROSE][i], stroke=[TEAL, TEAL, AMBER, RED, RED][i], size=10, bold=True)
f.box(15, 12, 250, 70, "STAGE 0-I\nKegel exercises, lifestyle,\nreassure and review", fill=MINT, stroke=TEAL, size=10)
f.box(15, 96, 250, 70, "STAGE II\npessary or surgery by symptoms;\nvaginal oestrogen", fill=SAND, stroke=AMBER, size=10)
f.box(15, 180, 250, 70, "STAGE III-IV\nsurgery or colpocleisis;\nskin and bladder care", fill=ROSE, stroke=RED, size=10)
f.box(15, 266, 730, 48, "Nepal: the commonest gynaecological complaint in far and mid-western districts; use camps, FCHVs and referral", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
```

**Hysterectomy** (removal of the uterus: **total**, **subtotal**, or **radical** with parametrium and nodes; **abdominal**, **vaginal** or **laparoscopic**) is done for fibroids, prolapse, heavy bleeding, endometriosis and cancer. Removal of both ovaries brings immediate surgical menopause.

### Eight points of nursing care after hysterectomy

1. **Monitor vital signs and bleeding.** Check pulse, blood pressure, temperature and respiration every 15 minutes at first, then hourly, and count the vaginal pads. A rising pulse and a falling pressure are early signs of internal haemorrhage. Report at once.
2. **Maintain airway and prevent chest problems.** Raise the head, teach deep breathing and coughing with a pillow splint every 2 hours, and mobilise early. This prevents atelectasis and pneumonia after general anaesthesia.
3. **Control pain.** Give analgesics as ordered (paracetamol, NSAID, or opioid for the first 24 hours), use a pain score, and teach her to ask early. Pain stops her from moving and breathing deeply. Good control speeds recovery.
4. **Care for the wound and drain.** Keep the dressing dry, watch for redness, discharge and swelling, empty and record any drain, and keep the area clean. Early wound care prevents infection, which is the commonest complication in low-resource wards.
5. **Care for the bladder and bowel.** Record the urine output (aim for 30 mL an hour or more), remove the catheter at 24-48 hours (earlier after vaginal surgery), watch for retention or ureteric injury (flank pain, haematuria), and give fluids and fibre. Bladder trouble is common after pelvic surgery.
6. **Prevent thrombosis.** Use early walking, leg exercises, stockings and low-molecular-weight heparin if ordered, and watch for calf pain and swelling. Deep vein thrombosis and pulmonary embolism are major causes of death after surgery.
7. **Give emotional and sexual counselling.** Explain that periods and pregnancy end, that desire and sex continue, and that a woman is not less feminine. Talk about surgical menopause if the ovaries were removed and about hormone options. Fear and grief are common and need time.
8. **Teach discharge care.** No heavy lifting or intercourse for 6 weeks, walk daily, take iron and a good diet, report fever, bleeding, foul discharge or leg pain, and attend the follow-up visit with the histology report. This prevents readmission and late complications.

## 4.5 Calculations

A screening test is judged by **sensitivity = TP ÷ (TP + FN)**, **specificity = TN ÷ (TN + FP)**, **PPV = TP ÷ (TP + FP)** and **NPV = TN ÷ (TN + FN)**. **Coverage = women screened ÷ eligible women × 100**. **Vaccine wastage factor = 1 ÷ (1 - wastage rate)**. **BSA (Mosteller) = square root of (height cm × weight kg ÷ 3,600)** and **chemotherapy dose = mg/m² × BSA**. **IV drip rate (gtt/min) = volume × drop factor ÷ time in minutes**.

```python
import math
n, prev = 2000, 0.05
dis = n * prev
for name, se, sp in (("VIA", 0.70, 0.85), ("HPV DNA test", 0.90, 0.90)):
    tp, fn = dis * se, dis * (1 - se)
    tn, fp = (n - dis) * sp, (n - dis) * (1 - sp)
    print(f"{name}: of 2,000 women with 100 cases, true positives {tp:.0f}, false negatives {fn:.0f}, true negatives {tn:.0f}, false positives {fp:.0f}; PPV {tp / (tp + fp) * 100:.1f}%, NPV {tn / (tn + fn) * 100:.1f}%")
print(f"Screening coverage = 840 / 4,200 = {840 / 4200 * 100:.1f}%; to reach 70% the ward needs {0.7 * 4200:.0f} women screened, which is {0.7 * 4200 - 840:.0f} more")
print(f"HPV vaccine: 100,000 girls at 90% coverage need {100000 * 0.9:.0f} single doses (a two-dose schedule would need {100000 * 0.9 * 2:.0f}); with 20% wastage the order is {100000 * 0.9 / (1 - 0.2):.0f} doses")
bsa = math.sqrt(152 * 50 / 3600)
print(f"Mina's body surface area = square root of (152 x 50 / 3,600) = {bsa:.2f} m2; cisplatin 40 mg/m2 = {40 * bsa:.1f} mg each week")
print(f"Post-operative fluid 1,000 mL over 8 hours = {1000 / 8:.0f} mL per hour = {1000 * 20 / (8 * 60):.0f} drops per minute with a 20 drops per mL set")
print(f"Minimum urine output after surgery for a 60 kg woman at 0.5 mL per kg per hour = {0.5 * 60:.0f} mL per hour = {0.5 * 60 * 24:.0f} mL per day")
print(f"Tamoxifen 20 mg daily for 5 years = {365 * 5} tablets = {20 * 365 * 5:,} mg")
```

```text
VIA: of 2,000 women with 100 cases, true positives 70, false negatives 30, true negatives 1615, false positives 285; PPV 19.7%, NPV 98.2%
HPV DNA test: of 2,000 women with 100 cases, true positives 90, false negatives 10, true negatives 1710, false positives 190; PPV 32.1%, NPV 99.4%
Screening coverage = 840 / 4,200 = 20.0%; to reach 70% the ward needs 2940 women screened, which is 2100 more
HPV vaccine: 100,000 girls at 90% coverage need 90000 single doses (a two-dose schedule would need 180000); with 20% wastage the order is 112500 doses
Mina's body surface area = square root of (152 x 50 / 3,600) = 1.45 m2; cisplatin 40 mg/m2 = 58.1 mg each week
Post-operative fluid 1,000 mL over 8 hours = 125 mL per hour = 42 drops per minute with a 20 drops per mL set
Minimum urine output after surgery for a 60 kg woman at 0.5 mL per kg per hour = 30 mL per hour = 720 mL per day
Tamoxifen 20 mg daily for 5 years = 1825 tablets = 36,500 mg
```

## Formula and fact sheet

- **Sensitivity** = TP ÷ (TP + FN); **specificity** = TN ÷ (TN + FP); **PPV** = TP ÷ (TP + FP); **NPV** = TN ÷ (TN + FN). PPV rises and NPV falls when the disease is more common.
- **Cervical cancer:** HPV 16 and 18 cause about 70%; screen 30-60 years every 5 years (VIA in Nepal, HPV DNA preferred by WHO); thermal ablation for eligible lesions; chemoradiation (cisplatin 40 mg/m² weekly) and brachytherapy for stage IIB-IVA; HPV single dose for girls in the NIP.
- **FIGO:** I cervix only; II upper two-thirds vagina or parametrium; III lower vagina or pelvic wall; IV bladder, rectum or distant.
- **Breast:** BSE monthly 5-7 days after the period; mammography from 40; tamoxifen 20 mg daily for 5-10 years. **Ovarian:** CA-125 above 35 U/mL. **Endometrial:** postmenopausal bleeding needs biopsy.
- **POP-Q:** 0 normal; I more than 1 cm above hymen; II within 1 cm; III more than 1 cm below; IV complete eversion. **Pessary** changed every 3-6 months.

## Chapter summary

- Pelvic examination needs consent, privacy, correct preparation, accurate labelling and infection prevention; the nurse's follow-up of abnormal results decides whether screening saves a life.
- Cervical cancer is caused by persistent high-risk HPV and takes 10-15 years to develop; vaccination, screening at 30-60 years every 5 years and treatment of precancer prevent it.
- The screen-and-treat algorithm uses ablation for eligible lesions, LEEP or referral for larger ones and biopsy for suspicious ones; invasive disease is treated by stage with surgery or chemoradiation and brachytherapy.
- Breast cancer is found by awareness, clinical examination, mammography and biopsy; ovarian and endometrial cancers are recognised by bloating and postmenopausal bleeding.
- Prolapse is a major burden in Nepal and is managed by Kegel exercises, pessary and surgery; hysterectomy care covers bleeding, wound, bladder, thrombosis, pain and counselling.

## Practice

```python
print(f"MCQ1 = {45 / (45 + 5) * 100:.0f}%; MCQ2 = {810 / (810 + 90) * 100:.0f}%; MCQ3 = {80 / (80 + 120) * 100:.0f}%; MCQ4 = {600 / 2000 * 100:.0f}%")
print(f"MCQ5 = {50000 * 0.9:.0f} doses; MCQ6 = {40 * 1.6:.0f} mg; MCQ7 = {500 * 15 / (4 * 60):.0f} drops per minute")
```

```text
MCQ1 = 90%; MCQ2 = 90%; MCQ3 = 40%; MCQ4 = 30%
MCQ5 = 45000 doses; MCQ6 = 64 mg; MCQ7 = 31 drops per minute
```

**MCQs (with reasons)**

1. A test finds 45 of 50 women with disease. Its sensitivity is: (a) 45% (b) 50% (c) 90% (d) 95%.
2. A test is negative in 810 of 900 healthy women. Its specificity is: (a) 10% (b) 81% (c) 90% (d) 99%.
3. A test gives 80 true and 120 false positives. The PPV is: (a) 40% (b) 60% (c) 67% (d) 80%.
4. A ward has 2,000 eligible women and 600 are screened. The coverage is: (a) 20% (b) 30% (c) 60% (d) 70%.
5. A district vaccinates 50,000 girls with single-dose HPV vaccine at 90% coverage. Doses needed: (a) 45,000 (b) 50,000 (c) 90,000 (d) 100,000.
6. Cisplatin 40 mg/m² for a woman with a BSA of 1.6 m² is: (a) 25 mg (b) 40 mg (c) 64 mg (d) 80 mg.
7. A 500 mL infusion is given over 4 hours with a 15 drops/mL set. The rate is: (a) 21 (b) 31 (c) 42 (d) 125 drops per minute.
8. In the Nepal guideline, VIA screening for women aged 30-60 years is repeated every: (a) 1 year (b) 3 years (c) 5 years (d) 10 years.

::: note Answers and rationales
**1. (c).** 45 ÷ 50 = 90%; sensitivity looks only at women who have the disease. 95% is wrongly 45 ÷ 47.
**2. (c).** 810 ÷ 900 = 90%; specificity looks only at healthy women. 10% is the false-positive rate.
**3. (a).** 80 ÷ (80 + 120) = 40%; two of every five positives are true. 67% divides by 120 only.
**4. (b).** 600 ÷ 2,000 = 30%. 60% divides by 1,000. The target in the national plan is 70%.
**5. (a).** 50,000 × 0.9 = 45,000 single doses. 90,000 would be the two-dose figure.
**6. (c).** 40 × 1.6 = 64 mg. 40 mg ignores the body size; 80 mg doubles it.
**7. (b).** 500 × 15 ÷ 240 = 31.25, so 31 drops per minute. 125 is the mL per hour.
**8. (c).** The national guideline recommends VIA every 5 years for 30-60 years; 3 years applies to women with HIV. Yearly screening is not needed and wastes resources.
:::

**Short answer (3 marks): List the risk factors of cervical cancer.** Persistent infection with high-risk HPV (types 16 and 18) is the cause. Other risk factors are early first intercourse, many partners, early and repeated childbirth, smoking, HIV infection or other immunosuppression, long use of oral contraceptives, poor genital hygiene and absence of screening. Prevention is by HPV vaccination, screening at 30-60 years and condom use.

**Short answer (3 marks): Describe breast self-examination.** The woman examines her breasts monthly, 5-7 days after the period starts (after menopause on a fixed date). She looks in a mirror for shape, dimpling, nipple change and skin change with arms down and up. Lying down with a pillow under the shoulder, she presses with the pads of three fingers in small circles, using light, medium and firm pressure, and covers the whole breast and armpit in a vertical strip pattern. She squeezes the nipple gently for discharge. A lump, discharge or skin change that persists needs a clinic visit.

**Medium answer (5 marks): Describe the screen-and-treat approach to cervical cancer prevention (Figure 4.2).** Women of 30-60 years are tested with VIA (or an HPV DNA test) by a trained nurse; women with HIV are screened more often. A negative test means rescreening in 5 years. A positive test is followed by checking the lesion: if it is small, away from the canal and visible, thermal ablation or cryotherapy is done at the same visit; if it is larger, LEEP or referral is arranged. A lesion that looks like cancer is biopsied and the woman is referred urgently. The nurse explains each step, obtains consent, controls infection, gives pain advice, and teaches to avoid sex and tampons for 4 weeks after ablation and to return for fever, foul discharge or heavy bleeding. She records in the register and HMIS and traces every positive woman by FCHV and telephone until treatment is completed. Follow-up is at 6 and 12 months. She also promotes HPV vaccination of girls.

**Long answer (10 marks): Mina Gurung, 45, mother of four, has white discharge and post-coital bleeding. VIA at the camp is positive; biopsy shows squamous cell carcinoma, stage IIB, haemoglobin 9 g/dL, height 152 cm and weight 50 kg. Explain the diagnosis, calculate the cisplatin dose, and write the nursing care plan.**

*Explanation.* Mina's cancer is caused by persistent high-risk HPV, probably acquired many years ago; she was never vaccinated or screened. **Stage IIB** means spread into the parametrium but not to the pelvic wall, so the cancer is too wide for surgery and the treatment of choice is **concurrent chemoradiation followed by brachytherapy** at a cancer centre such as BP Koirala Memorial Cancer Hospital. Her **body surface area is the square root of (152 × 50 ÷ 3,600) = 1.45 m²**, so **weekly cisplatin 40 mg/m² = 58.1 mg**, given for 5-6 weeks with hydration, antiemetics and renal tests. She needs iron and possibly a blood transfusion for **haemoglobin 9 g/dL** before radiotherapy.

*Management.* The nurse first listens to Mina's fear and explains the diagnosis, the plan and the chance of cure (about 60-75% for stage IIB with modern chemoradiation) without false hope. She arranges referral with the biopsy slide and a letter, travel support through the cancer fund and a family companion. Before treatment: blood tests (CBC, creatinine), counselling on a **radiation schedule**, skin and bowel preparation. During treatment: IV hydration (for example 1,000 mL over 8 hours at 42 drops per minute with a 20 drops/mL set), antiemetics, monitoring of urine output (at least 30 mL per hour), watch for **radiation cystitis and proctitis** (burning urine, diarrhoea), skin reactions, vaginal stenosis (use dilators after treatment) and low blood counts (fever means urgent review). She teaches a high-protein diet, hygiene, no douching, and warning signs: heavy bleeding, fever above 38 °C, severe pain or leg swelling. She arranges counselling and social support, discusses sexual health, and organises follow-up at 1, 3, 6 and 12 months. She also invites Mina's daughters for HPV vaccination and her sisters for screening.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "Will I die? Who will care for my children?" **O:** tearful, new diagnosis of stage IIB cervical cancer | **Fear** related to the cancer diagnosis and treatment | **Fear self-control:** expresses fear and joins treatment plan | Honest information, involve husband and a counsellor, link to a cancer support group (open discussion reduces fear and treatment refusal) | Agrees to travel for treatment |
| **S:** "I do not know what radiotherapy is." **O:** referral planned, family unaware | **Deficient knowledge** (chemoradiation, side effects, warning signs) related to new diagnosis | **Knowledge: treatment regimen:** names 3 side effects and 3 warning signs | Teach with pictures and teach-back; give a written card with phone numbers (informed women report problems early) | Teach-back correct |
| **S:** "I feel weak and dizzy." **O:** Hb 9 g/dL, weight 50 kg, vaginal bleeding | **Risk for bleeding** and **Fatigue** related to tumour bleeding and anaemia | **Blood loss severity:** pad count falls; Hb 10 g/dL or more before radiotherapy | Iron-rich diet and iron tablets or transfusion as ordered, count pads, rest and pace activity (improves oxygen delivery and treatment tolerance) | Hb 10.2 g/dL at 2 weeks |
| **O:** cisplatin weekly, urine output to monitor | **Risk for deficient fluid volume** and **Nausea** related to chemotherapy and vomiting | **Hydration:** urine over 30 mL per hour, no weight loss over 2 kg | Pre-hydrate (IV fluid 1,000 mL over 8 hours), give antiemetics, small frequent meals, record intake and output (protects the kidneys from cisplatin) | Urine 45 mL per hour; weight stable |
| **S:** "Will I be able to be a wife again?" **O:** will have pelvic radiotherapy | **Ineffective sexuality pattern** related to cancer treatment and body-image change | **Sexual functioning:** states plan for intimacy and uses dilator | Private counselling with the husband, teach vaginal dilators and lubricant after therapy, reassure about no contagion (prevents vaginal stenosis and relationship strain) | Couple attends counselling; dilator taught |
