---
subject: Midwifery II
grade: BSc Nursing Year 3
unit: 1
title: Bleeding in Pregnancy: Abortion, Ectopic Pregnancy, Molar Pregnancy and Antepartum Haemorrhage (Placenta Praevia, Abruption, Vasa Praevia, Uterine Rupture)
hours: 26
area: BSN 19-20 · Midwifery II · Units 1-3
---

At 2 a.m. a bus drops Sunita Rai, 28, G3P2 at 34 weeks, at a district hospital in Dolakha. She has bled **a bright red gush without any pain**. Her pulse is 118 and her blood pressure 86/54. Two hours earlier, the same hospital had admitted a woman who bled with a **hard, tender, woody uterus** and no fetal heartbeat. Both women are "bleeding in late pregnancy", yet one needs gentle hands off the abdomen and a theatre, and the other needs the uterus emptied while fluids run. The midwife who tells them apart in two minutes saves two lives. This unit covers **bleeding in early pregnancy** (abortion, ectopic, molar) and **antepartum haemorrhage (APH)**: causes, recognition, emergency care, drugs, calculations and the nursing process.

::: key What this unit gives you
- Real specimen photographs: a **placental abruption** with retroplacental clot, a **complete hydatidiform mole**, a **ruptured tubal ectopic** with the sac, and a **tubal pregnancy with embryo**; numbered marks, in a 4-up strip.
- SVG figures: the **first-trimester bleeding triage chart**, **placenta praevia grades beside the three types of abruption**, and the **APH decision algorithm**.
- **Seven points of post-abortion care** and **eight points of nursing care in APH**, each in 3-4 plain sentences, anchored in the Safe Motherhood and Reproductive Health Rights Act 2075, Aama, BEONC/CEONC and the NMMS 2021.
- Verified maths: **shock index**, **blood volume and percentage lost**, **hCG rise**, **methotrexate dose by body surface area**, **misoprostol tablets**; MCQs, short, medium and long answers and a 5-column NANDA-I plan.
:::

## 1.1 Why bleeding in pregnancy matters in Nepal

The **Nepal Maternal Mortality Study 2021** (MoHP and National Statistics Office) reports a national **MMR of 151 per 100,000 live births**. Of the deaths, **26% were due to obstetric haemorrhage** and 12% to hypertensive disorders; **about 57% of deaths happened in health facilities**, most because care was delayed or inadequate, and 26% at home. Bleeding is therefore a problem of **recognising early and acting fast**, not only of reaching a facility. Nepal's **Aama programme** pays for four ANC visits and facility delivery, and the **BEONC** (basic) and **CEONC** (comprehensive, with surgery and blood) signal functions are the ladder on which a bleeding woman climbs.

**Classification by time.** Bleeding **before 12-13 weeks** is usually abortion, ectopic or mole; **13 to 28 weeks** includes late abortion, cervical causes and early praevia; **after 28 weeks and before labour** is **APH**; after delivery it is **PPH** (Unit 2). (Some countries use 24 weeks for APH; Nepal's HMIS and teaching use 28 weeks, and the viable-fetus rule is applied clinically.)

| Gestation | Main causes | First question to ask |
|---|---|---|
| Under 12 weeks | Threatened, incomplete, missed or septic abortion; **ectopic**; **molar** pregnancy | Is there pain, shock or a positive pregnancy test with an empty uterus? |
| 13-28 weeks | Late abortion, cervical insufficiency, polyp, trauma, early praevia | Is the cervix open? Any fever or discharge? |
| After 28 weeks | **Placenta praevia**, **abruption**, **vasa praevia**, **uterine rupture**, show, local causes | **Painless** or **painful**? Is the uterus soft or hard? Is the fetus alive? |

```svgfig label="1.1" caption="First-trimester bleeding triage for a midwife at a health post or birthing centre. Step 1 check the airway, pulse, blood pressure and consciousness. Shock (pulse over 100, systolic under 90, cold skin) means starting two IV lines, giving fluids, and referring to a CEONC with a nurse escort. A tender lower abdomen with a positive pregnancy test needs an ultrasound and a surgeon: a ruptured ectopic is the first thought. A closed cervix with light bleeding is a threatened abortion; an open cervix with products is incomplete or inevitable; a large uterus for dates with vesicles points to a mole. Check the Rh group of every bleeding woman."
f = Fig(760, 330)
f.box(250, 12, 260, 40, "BLEEDING IN EARLY PREGNANCY\nABC, pulse, BP, pregnancy test, Rh group", fill=NAVY, stroke=NAVY, color="#ffffff", size=10, bold=True)
f.box(20, 90, 220, 70, "SHOCK or SEVERE PAIN?\nTwo IV lines, fluids,\nrefer to CEONC with escort", fill=ROSE, stroke=RED, size=10, bold=True)
f.box(270, 90, 220, 70, "PAIN + EMPTY UTERUS\nSUSPECT ECTOPIC\nultrasound, surgeon, no food", fill=SAND, stroke=AMBER, size=10, bold=True)
f.box(520, 90, 220, 70, "UTERUS LARGE FOR DATES\nvesicles, very high hCG\nSUSPECT MOLE", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.box(20, 200, 220, 70, "CERVIX CLOSED\nTHREATENED ABORTION\nrest, review, reassure", fill=MINT, stroke=TEAL, size=10, bold=True)
f.box(270, 200, 220, 70, "CERVIX OPEN, TISSUE SEEN\nINCOMPLETE / INEVITABLE\nMVA or misoprostol", fill=MINT, stroke=TEAL, size=10, bold=True)
f.box(520, 200, 220, 70, "NO HEARTBEAT, CLOSED CERVIX\nMISSED ABORTION\nmedical or MVA", fill=MINT, stroke=TEAL, size=10, bold=True)
for x in (130, 380, 630): f.arrow([(380, 52), (x, 90)], color=SLATE)
for x in (130, 380, 630): f.arrow([(x, 160), (x, 200)], color=SLATE)
f.text(380, 300, "Every bleeding woman: Rh group, anti-D if Rh negative, family planning before discharge", size=10, color=NAVY, bold=True)
f.text(380, 318, "Fever, foul discharge or tender uterus = SEPTIC abortion: antibiotics first, then evacuate", size=10, color=RED, bold=True)
```

## 1.2 Abortion

**Abortion** is the termination of pregnancy **before the fetus is viable** (WHO uses 22 weeks or 500 g; Nepal's HMIS reports abortion services up to 28 weeks). About one in five known pregnancies ends in miscarriage, most often from **fetal chromosomal abnormality**. **Spontaneous** abortion is by nature; **induced** abortion is deliberate. In Nepal the **Safe Motherhood and Reproductive Health Rights Act 2075 (2018)** allows abortion **on the woman's request up to 12 weeks** without a reason and with her consent alone, and **up to 28 weeks on specified grounds** (rape or incest, risk to her life or physical or mental health, serious fetal anomaly, HIV or another incurable disease). Sex-selective abortion is prohibited. Services at government facilities are free, and only an authorised provider may carry out the procedure. *(Legal details come from reliable secondary summaries of the Act; check the current rules in your campus manual.)*

| Type | Cervix | Bleeding and pain | Tissue passed | Management |
|---|---|---|---|---|
| **Threatened** | Closed | Light bleeding, mild or no pain | None | Rest as comfort, ultrasound, review; no drugs prevent loss |
| **Inevitable** | Open | Heavy bleeding, cramps | None yet | Evacuate: misoprostol or MVA |
| **Incomplete** | Open | Heavy bleeding, cramps | Part passed | Misoprostol 600 mcg orally (or 400 mcg sublingual) or MVA |
| **Complete** | Closed | Bleeding stops | All passed | Confirm by ultrasound, haemoglobin, counselling |
| **Missed** | Closed | Brown spotting, no growth | None; fetal death | Mifepristone then misoprostol, or MVA |
| **Septic** | Open | Fever, foul discharge, tender uterus | Infected products | IV antibiotics, then evacuate within hours |
| **Recurrent** | Varies | Three or more losses | - | Investigate: cervix, thyroid, antiphospholipid, chromosomes |

**Evacuation methods.** **Manual vacuum aspiration (MVA)** with a Karman cannula and a 60 mL syringe is the standard under 12 weeks and is safer than sharp curettage. For **medical abortion up to 12 weeks** WHO 2022 recommends **mifepristone 200 mg orally, then misoprostol 800 mcg** (buccal, sublingual or vaginal) 1-2 days later (Nepal's programme uses 24-48 hours); for **incomplete abortion under 13 weeks** misoprostol 600 mcg orally is one option. **Anti-D immunoglobulin** is given to Rh-negative women within 72 hours of any bleeding event.

### Seven points of post-abortion care (PAC)

1. **Treat the emergency first.** Shock, sepsis and haemorrhage kill before anything else does. Start IV fluids, take blood for the group and haemoglobin, and give antibiotics for suspected sepsis. Refer to a CEONC if surgery or blood is needed.
2. **Evacuate the uterus safely.** Choose MVA or misoprostol by gestation and condition, because retained tissue causes bleeding and infection. Use pain relief and a paracervical block. Check the tissue for completeness.
3. **Give pain relief and comfort.** Cramping is real and fear makes it worse. Explain every step, give paracetamol or ibuprofen, and let a female companion stay. Respect and privacy keep women from hiding future complications.
4. **Counsel and offer family planning.** Ovulation can return within two weeks. Offer a method **before she leaves**: pills, injection, implant or IUCD can start at once if there is no infection. Counselling lowers repeat unsafe abortion.
5. **Prevent infection.** Use hand hygiene, sterile instruments and clean pads. Teach her to watch for fever, foul discharge and lower abdominal pain. Give antibiotics if sepsis is suspected.
6. **Give Rh immunoglobulin when needed.** An Rh-negative mother can form antibodies that harm the next baby. Check her group and give anti-D within 72 hours. Record it on the card.
7. **Link to other care and follow up.** Check anaemia and give iron-folic acid, screen for violence, offer HIV and syphilis testing and tell her to return in 7-14 days. Warn her to come back at once for heavy bleeding, fever or severe pain.

## 1.3 Ectopic pregnancy

An **ectopic pregnancy** implants **outside the uterine cavity**: **95% in the fallopian tube** (ampulla about 70%, isthmus 12%, fimbria 11%, interstitial 2-3%), the rest in the ovary, cervix, abdomen or caesarean scar. **Risk factors:** previous ectopic, **pelvic inflammatory disease (chlamydia, gonorrhoea, post-septic abortion)**, tubal surgery or sterilisation failure, **IUCD in place**, assisted conception, smoking, and age over 35. **Classic triad:** **amenorrhoea of 6-8 weeks, lower abdominal pain, and vaginal spotting**. A **ruptured ectopic** causes sudden severe pain, **shoulder-tip pain** (blood under the diaphragm), faintness, shock and a rigid abdomen with cervical excitation. **Every woman of reproductive age with abdominal pain and a missed period has an ectopic until proved otherwise.**

```photogrid label="1.1" cols="4" ratio="1.0" caption="Real specimens of pregnancy bleeding. (a) A placental abruption: the dark retroplacental clot separates the placenta from the uterine wall. (b) A ruptured tubal ectopic pregnancy: the swollen tube with haemorrhagic wall lies beside the opened gestational sac with the small embryo. (c) A complete hydatidiform mole: the villi swell into translucent vesicles like a bunch of grapes. (d) A tubal pregnancy opened at operation: the embryo lies within the tube."
@ photo id="nur12/abrupt" cap="Placental abruption (specimen)"
fit 1.0
focus 0.45 0.5
mark 0.35 0.55 "1"
mark 0.60 0.62 "2"
key 1 (a) Dark retroplacental clot behind the placenta
key 2 (a) Placenta with membranes and cord
@ photo id="nur12/ectop" cap="Ruptured tubal ectopic with sac"
fit 1.0
focus 0.40 0.5
mark 0.25 0.45 "3"
mark 0.22 0.85 "4"
key 3 (b) Swollen, ruptured fallopian tube
key 4 (b) Dark clot and haemorrhage at the rupture
@ photo id="nur12/mole" cap="Complete hydatidiform mole"
fit 1.0
focus 0.5 0.5
mark 0.40 0.55 "5"
key 5 (c) Grape-like swollen vesicles
@ photo id="nur12/tubal" cap="Tubal pregnancy with embryo"
fit 1.0
focus 0.5 0.5
mark 0.35 0.45 "6"
key 6 (d) Embryo lying inside the opened tube
```

**Investigations.** A **urine pregnancy test** (positive), a **transvaginal ultrasound** (empty uterus, adnexal mass, free fluid in the pouch of Douglas; the "blob" or "bagel" sign), a serial **serum beta-hCG** (a normal early pregnancy raises hCG by at least 49-53% in 48 hours when the starting value is under 1,500 mIU/mL; a slower rise suggests ectopic or failing pregnancy), haemoglobin and the Rh group.

**Management.** *Unstable or ruptured:* resuscitate with two wide IV lines and fluids, cross-match blood, and do an **emergency laparotomy or laparoscopy and salpingectomy**. *Stable, unruptured, small:* **methotrexate 50 mg per m² of body surface area IM, single dose**, if hCG is low (under about 5,000 mIU/mL), the mass is under 3.5-4 cm, there is no fetal heartbeat and the woman can return for follow-up; hCG is checked on day 4 and day 7 (a fall of at least 15% is expected). Counsel her to avoid NSAIDs, alcohol, folic acid supplements and sun, and not to conceive for three months. *Nursing points:* keep her nil by mouth if surgery may follow, record vitals every 15 minutes, and give anti-D if Rh negative.

## 1.4 Gestational trophoblastic disease (molar pregnancy)

A **hydatidiform mole** is an abnormal placenta in which the villi swell into fluid-filled vesicles. A **complete mole** (46,XX, all paternal chromosomes, no fetus) is the classic one; a **partial mole** (triploid, 69 chromosomes, sometimes a fetus) is milder.

| Feature | Complete mole | Partial mole |
|---|---|---|
| Karyotype | 46,XX or XY, all paternal | Triploid 69,XXY |
| Fetus | None | Possible, abnormal |
| Uterus size | Often **larger than dates** | Small or equal to dates |
| hCG | **Very high** (often over 100,000 mIU/mL) | Mildly raised |
| Risk of choriocarcinoma or persistent disease | About 15-20% | About 1-5% |

**Features:** bleeding at 8-16 weeks (brown, "prune-juice"), **severe hyperemesis**, **early pre-eclampsia before 20 weeks**, **hyperthyroidism**, theca-lutein cysts and passage of vesicles. **Ultrasound** shows a "snowstorm" or "cluster of grapes". **Treatment** is **suction evacuation**, with oxytocin started after evacuation begins, and **hCG follow-up weekly until three normal values and then monthly for 6 months**; reliable **contraception (not an IUCD)** is advised for the whole follow-up. A rising hCG means **persistent trophoblastic disease**, treated with methotrexate or actinomycin-D, and cure rates exceed 95%.

## 1.5 Antepartum haemorrhage (APH)

**APH** is bleeding from the genital tract **after 28 weeks of pregnancy and before the birth of the baby**. It complicates 3-5% of pregnancies and is a leading cause of maternal death and **stillbirth and preterm birth**. The three questions that sort the causes are: **Is it painful? Is the uterus soft or hard? What is the fetal heart doing?** The midwife must **never do a vaginal examination** until a placenta praevia has been excluded by ultrasound or the woman is in theatre with a double set-up, because a finger can tear the placenta and cause a torrent of bleeding.

| Feature | **Placenta praevia** | **Placental abruption** |
|---|---|---|
| Pain | **Painless** | **Painful**, constant, may be severe |
| Blood | **Bright red**, fresh, often recurrent ("warning bleed") | **Dark**, may be small or **concealed**; out of proportion to the shock |
| Uterus | Soft, relaxed, non-tender | **Hard, woody, tender**; may rise in size |
| Fetal parts | Easily felt, malpresentation common | Hard to feel |
| Fetal heart | Usually normal until the mother is shocked | Distress or **absent** |
| Shock | In proportion to visible loss | **Out of proportion** to visible loss |
| Associations | Previous caesarean, multiparity, twin, age, smoking | **Hypertension and pre-eclampsia**, trauma, cocaine, smoking, previous abruption, PPROM, high parity |

```svgfig label="1.2" caption="Placenta praevia and placental abruption. Top row, praevia grades by how the placenta lies in relation to the internal os: grade I (low-lying) in the lower segment but not reaching the os; grade II (marginal) at the edge of the os; grade III (partial) partly covering the os; grade IV (complete or central) covering the os fully. Grades III and IV need caesarean birth. Bottom row, three types of abruption: revealed (blood escapes through the cervix), concealed (blood is trapped behind the placenta, so the uterus is hard and the shock is out of proportion) and mixed. The red area is the retroplacental clot and the dark line is the placenta."
f = Fig(760, 340)
f.text(20, 22, "PLACENTA PRAEVIA (position of placenta against the internal os)", size=11, color=NAVY, bold=True, anchor="start")
grades = [("I  LOW-LYING", "in lower segment,\nnot reaching os", (-30, 20, -12, 36)), ("II  MARGINAL", "reaches the\nedge of the os", (-30, 20, -4, 38)), ("III  PARTIAL", "covers part\nof the os", (-30, 20, 14, 36)), ("IV  COMPLETE", "covers the\nwhole os", (-30, 20, 30, 20))]
for i, (nm, d, (a, b, c, e)) in enumerate(grades):
    cx, cy = 95 + i * 190, 85
    f.circle(cx, cy, 40, fill="#ffffff", stroke=NAVY, sw=1.6)
    f.circle(cx, cy + 40, 5, fill=MINT, stroke=TEAL, sw=1.4)
    f.line(cx + a, cy + b, cx + c, cy + e + 6, color=RED, sw=7)
    f.text(cx, 150, nm, size=10.5, color=NAVY, bold=True)
    f.text(cx, 165, d.split("\n")[0], size=10, color=SLATE)
    f.text(cx, 178, d.split("\n")[1], size=10, color=SLATE)
f.text(20, 205, "PLACENTAL ABRUPTION (retroplacental clot)", size=11, color=RED, bold=True, anchor="start")
types = [("REVEALED", "blood escapes\nthrough the cervix", True), ("CONCEALED", "clot trapped:\nhard uterus, shock", False), ("MIXED", "both, with\nfetal death common", True)]
for i, (nm, d, out) in enumerate(types):
    cx, cy = 130 + i * 250, 255
    f.circle(cx, cy, 36, fill="#ffffff", stroke=NAVY, sw=1.6)
    f.line(cx - 30, cy - 14, cx - 30, cy + 14, color=SLATE, sw=6)
    f.circle(cx - 22, cy, 9, fill=RED, stroke=RED, sw=1)
    if out: f.arrow([(cx, cy + 36), (cx + 18, cy + 66)], color=RED, sw=2)
    f.text(cx + 78, cy - 6, nm, size=10.5, color=RED, bold=True, anchor="start")
    f.text(cx + 78, cy + 8, d.split("\n")[0], size=10, color=SLATE, anchor="start")
    f.text(cx + 78, cy + 21, d.split("\n")[1], size=10, color=SLATE, anchor="start")
f.text(380, 330, "Never do a vaginal examination in APH until praevia is excluded", size=10.5, color=RED, bold=True)
```

**Other causes of APH.** **Vasa praevia** is a fetal vessel running through the membranes across the cervix; when the membranes rupture the fetus bleeds, giving **fresh bleeding, fetal bradycardia and a sinusoidal trace within minutes**, with a very high fetal death rate unless an **emergency caesarean** follows. **Uterine rupture** causes sudden severe pain, loss of contractions, **bleeding, shock, fetal parts felt under the abdominal skin** and loss of the fetal heart; risk factors are a **previous caesarean scar**, obstructed labour, grand multiparity and oxytocin or misoprostol misuse. **Local causes** (cervical polyp, ectropion, vaginal trauma) and "show" are diagnoses of exclusion.

**Placenta accreta spectrum.** With a praevia over a caesarean scar the placenta may invade the muscle (**accreta**), the myometrium (**increta**) or beyond (**percreta**); the risk rises steeply with each previous caesarean. Plan delivery in a **CEONC** with blood, an experienced surgeon and, if needed, hysterectomy, at about 34-36 weeks for a suspected accreta and **36-37 weeks for a praevia without accreta**.

```svgfig label="1.3" caption="APH decision algorithm for a CEONC or BEONC. Step 1 call for help, check airway, breathing, pulse and blood pressure, put in two wide IV lines, send blood for group, cross-match, haemoglobin and clotting, and give fluids (Ringer's lactate or normal saline). Step 2 ask about pain, colour of blood, fetal movements and trauma; palpate the uterus; listen to the fetal heart. Step 3 ultrasound for placental site and retroplacental clot. Painless fresh bleeding with a soft uterus means praevia; painful bleeding with a hard tender uterus means abruption; sudden pain with shock and loss of contractions means rupture; bleeding with membrane rupture and fetal bradycardia means vasa praevia."
f = Fig(760, 330)
f.box(230, 10, 300, 44, "APH (bleeding after 28 weeks)\nCALL FOR HELP, 2 IV lines, fluids, blood", fill=NAVY, stroke=NAVY, color="#ffffff", size=10, bold=True)
f.box(20, 88, 340, 46, "ASSESS: pain? blood colour? uterus soft or hard?\nfetal heart and movements, pulse and BP, NO PV", fill=SAND, stroke=AMBER, size=10, bold=True)
f.box(400, 88, 340, 46, "INVESTIGATE: ultrasound (placenta site, clot),\nCBC, group and cross-match, clotting, CTG", fill=SAND, stroke=AMBER, size=10, bold=True)
f.arrow([(380, 54), (190, 88)]); f.arrow([(380, 54), (570, 88)])
dx = [("PAINLESS, FRESH, SOFT UTERUS", "PLACENTA PRAEVIA\nsteroids, anti-D, expectant if stable;\nCS if heavy bleeding or 37 wk", MINT, TEAL), ("PAINFUL, HARD, DARK BLOOD", "ABRUPTION\nresuscitate, deliver; ARM and\ninduce if alive or dead; watch DIC", ROSE, RED), ("SUDDEN PAIN, SHOCK, SCAR", "UTERINE RUPTURE\nresuscitate, laparotomy,\nrepair or hysterectomy", ROSE, RED), ("BLEED + ROM + BRADYCARDIA", "VASA PRAEVIA\nemergency caesarean,\nneonatal resuscitation team", BLUE, NAVY)]
for i, (a, b, fl, st) in enumerate(dx):
    x = 15 + i * 187
    f.box(x, 170, 175, 44, a, fill=fl, stroke=st, size=9.5, bold=True)
    f.box(x, 224, 175, 70, b, fill="#ffffff", stroke=st, size=9.5)
    f.arrow([(x + 87, 134), (x + 87, 170)])
f.text(380, 318, "After delivery: active third stage, uterotonics, watch for PPH, anti-D for Rh negative", size=10, color=NAVY, bold=True)
```

**Management by condition.**

- **Placenta praevia, stable, preterm:** admit, **two IV lines**, group and save or cross-match, **antenatal corticosteroids** (dexamethasone 6 mg IM every 12 hours for 4 doses between 24 and 34 weeks) for fetal lungs, **anti-D** if Rh negative, iron to correct anaemia, bed rest as comfort only and **no vaginal or rectal examination**. **Caesarean** at 36-37 weeks, or at once for heavy bleeding or fetal compromise.
- **Placental abruption:** resuscitate first; deliver. If the baby is alive and the mother stable, **caesarean** is chosen for fetal distress, and **vaginal birth after membrane rupture and oxytocin** is chosen when the baby is dead or birth is near. **Watch for DIC** (check the clotting time with a 2 mL clot test or a lab coagulation screen), **renal failure** (urine output at least 30 mL/h) and **PPH**.
- **Vasa praevia and rupture:** immediate surgery; call the neonatal resuscitation team.

### Eight points of nursing care in antepartum haemorrhage

1. **Call for help and start resuscitation (ABC).** Bleeding can change a stable woman into a shocked one in minutes. Position her on her left side or with a tilt, give oxygen at 8-10 L/min by mask, and put in two wide-bore cannulae. Take bloods and run Ringer's lactate or saline fast.
2. **Do not examine the vagina.** A finger may disturb a praevia and trigger torrential bleeding. Inspect the pad and perineum, never insert anything, and do a speculum or digital examination only in theatre after ultrasound by a doctor.
3. **Assess blood loss and shock.** Count and weigh the pads and soak-ups because visible loss under-estimates in abruption. Record pulse, BP, respiration, capillary refill and the shock index every 15 minutes. Take a 2 mL bedside clotting test.
4. **Monitor the fetus.** Listen to the fetal heart every 15 minutes or use continuous CTG. A heart rate below 110 or above 160, or loss of variability, means fetal compromise. Tell the doctor at once and prepare for caesarean.
5. **Examine the uterus gently and measure it.** Mark the fundal height with a pen and repeat every hour. A rising fundus with a hard tender uterus means concealed bleeding. Report any increase immediately.
6. **Give drugs and blood as ordered.** Prepare dexamethasone for fetal lungs, oxytocin after delivery, anti-D if Rh negative and tranexamic acid when ordered. Cross-match 2-4 units and give blood early with warmed fluids. Check the group on every bag with a second nurse.
7. **Prepare for theatre and the baby.** Take consent from the woman (or her family if she is too ill), pass a Foley catheter, give nil by mouth, shave only if needed and call the anaesthetist and newborn team. Keep a warm resuscitation corner ready for a preterm baby.
8. **Support, refer and record.** Explain every step to the woman and her family in simple Nepali, hold her hand and respect her privacy. If you work at a health post or BEONC, **refer** after stabilisation with a nurse, a letter, oxygen and IV fluids running. Record times and events, and complete the **maternal death review (MDR) form** if the worst happens.

### Seven complications of placental abruption

1. **Hypovolaemic shock** from a large concealed loss, with pallor, rapid pulse and low BP out of proportion to visible blood.
2. **Disseminated intravascular coagulation (DIC)**, because the clot uses up clotting factors and tissue thromboplastin enters the blood; the woman bleeds from cannula sites and the clot test fails.
3. **Acute kidney injury** from poor renal perfusion; the urine output drops below 30 mL/h and may need dialysis.
4. **Couvelaire uterus (uterine apoplexy)**, where blood infiltrates the muscle, making the uterus purple and atonic, so it causes PPH.
5. **Postpartum haemorrhage**, both from atony and from clotting failure, so uterotonics and TXA are ready.
6. **Fetal death or asphyxia**, preterm birth and growth restriction, because the placental surface for gas exchange is lost.
7. **Sheehan syndrome and Rh sensitisation**, from pituitary necrosis after severe shock and from fetomaternal bleeding in an Rh-negative woman (give anti-D).

## 1.6 Calculations in bleeding emergencies

The shock index (SI) is **pulse divided by systolic BP**: normal 0.5-0.7, and **0.9 or more** is abnormal in pregnancy, while **1.0 or more** signals major haemorrhage. Total blood volume at term is about **100 mL per kg** (non-pregnant adults about 65-70). Sunita (60 kg) has pulse 118 and BP 86/54. Methotrexate dosing uses the **Mosteller BSA** = square root of (height cm × weight kg ÷ 3600). The hCG rise in 48 hours is **(second − first) ÷ first × 100**.

```python
pulse, sbp, kg, loss = 118, 86, 60, 1200
si = pulse / sbp                                     # shock index
bv = 100 * kg                                        # blood volume at term, mL
pct = loss / bv * 100                                # percentage lost
h1, h2, h3 = 1200, 1500, 2100                        # beta-hCG at 0 h and 48 h (two cases)
rise_a, rise_b = (h2 - h1) / h1 * 100, (h3 - h1) / h1 * 100
bsa = (160 * 55 / 3600) ** 0.5                       # Mosteller BSA, 160 cm and 55 kg
mtx = 50 * bsa                                       # methotrexate 50 mg per m2
d4, d7 = 2900, 2400                                  # hCG day 4 and day 7 after methotrexate
fall = (d4 - d7) / d4 * 100
print(f"Sunita: shock index {si:.2f}; blood volume {bv} mL; {loss} mL is {pct:.1f}% of it")
print(f"hCG rise in 48 h: case A {rise_a:.0f}% (abnormal), case B {rise_b:.0f}% (expected 49% or more)")
print(f"BSA {bsa:.2f} m2; methotrexate {mtx:.0f} mg; misoprostol 800 mcg = {800 // 200} tablets of 200 mcg")
print(f"Dexamethasone 6 mg from 4 mg/mL = {6 / 4:.1f} mL per dose; 4 doses = {6 * 4} mg; day 4 to 7 hCG fall {fall:.1f}%")
```

```text
Sunita: shock index 1.37; blood volume 6000 mL; 1200 mL is 20.0% of it
hCG rise in 48 h: case A 25% (abnormal), case B 75% (expected 49% or more)
BSA 1.56 m2; methotrexate 78 mg; misoprostol 800 mcg = 4 tablets of 200 mcg
Dexamethasone 6 mg from 4 mg/mL = 1.5 mL per dose; 4 doses = 24 mg; day 4 to 7 hCG fall 17.2%
```

## Formula and fact sheet

- **Shock index** = pulse ÷ systolic BP: 0.5-0.7 normal; 0.9 or more abnormal; 1.0 or more major haemorrhage. **Blood volume at term** about 100 mL/kg.
- **APH** = bleeding after 28 weeks and before birth; praevia is painless, soft, bright red; abruption is painful, hard, dark with shock out of proportion; **no PV examination** until praevia is excluded.
- **Abortion** (Nepal Act 2075): on request to 12 weeks; to 28 weeks on grounds (rape, incest, risk to health, fetal anomaly, HIV). Medical: mifepristone 200 mg then misoprostol 800 mcg; incomplete: misoprostol 600 mcg oral. MVA under 12 weeks.
- **Ectopic:** 95% tubal; triad of amenorrhoea, pain and spotting; methotrexate 50 mg/m² if stable, hCG low, mass under 3.5-4 cm; hCG should rise at least 49% in 48 h in a normal pregnancy.
- **Molar:** hCG follow-up weekly to three normal values then monthly for 6 months; contraception (not IUCD); persistent disease treated with methotrexate or actinomycin-D.
- **Steroids:** dexamethasone 6 mg IM q12h × 4 doses (24-34 weeks). **Anti-D** within 72 hours for Rh-negative bleeding. **NMMS 2021:** MMR 151; haemorrhage 26%; hypertension 12%; 57% of deaths in facilities.

## Chapter summary

- Bleeding before 12 weeks is abortion, ectopic or mole until proved otherwise; a woman with pain, amenorrhoea and a positive test has an ectopic until the scan says no.
- Nepal's Act 2075 permits abortion on request to 12 weeks and to 28 weeks on specified grounds; MVA and medical abortion are safe, and post-abortion family planning is part of care.
- APH is bleeding after 28 weeks; painless fresh bleeding with a soft uterus is praevia; painful dark bleeding with a hard uterus is abruption; **never do a vaginal examination** before ultrasound.
- Resuscitate first (two IV lines, fluids, oxygen, blood), monitor the fetus, give steroids and anti-D when indicated and deliver in a CEONC.
- Abruption brings shock, DIC, renal failure, Couvelaire uterus and PPH; molar pregnancy needs 6 months of hCG follow-up.

## Practice

```python
mcq1 = 110 / 100                                       # MCQ1 shock index, pulse 110, SBP 100
mcq2 = 800 // 200                                      # MCQ2 tablets of misoprostol 200 mcg
mcq3 = 50 * 1.6                                        # MCQ3 methotrexate mg for BSA 1.6 m2
mcq4 = (1400 - 1000) / 1000 * 100                      # MCQ4 hCG rise in 48 h
mcq5 = 1000 / (100 * 50) * 100                         # MCQ5 percent of blood volume, 1,000 mL in 50 kg
case_si = 118 / 86
case_pct = 1200 / (100 * 60) * 100
dex = 6 * 4
print(f"MCQ1 = {mcq1:.1f}; MCQ2 = {mcq2} tablets; MCQ3 = {mcq3:.0f} mg; MCQ4 = {mcq4:.0f}%; MCQ5 = {mcq5:.0f}%")
print(f"Sunita: shock index {case_si:.2f}; loss {case_pct:.0f}% of blood volume; dexamethasone total {dex} mg")
```

```text
MCQ1 = 1.1; MCQ2 = 4 tablets; MCQ3 = 80 mg; MCQ4 = 40%; MCQ5 = 20%
Sunita: shock index 1.37; loss 20% of blood volume; dexamethasone total 24 mg
```

**MCQs (with reasons)**

1. A woman has pulse 110 and systolic BP 100 mmHg. Her shock index is: (a) 0.9 (b) 1.1 (c) 1.5 (d) 0.5.
2. The complete medical abortion regimen of misoprostol 800 mcg using 200 mcg tablets needs: (a) 2 tablets (b) 3 tablets (c) 4 tablets (d) 8 tablets.
3. Methotrexate 50 mg/m² for a woman with BSA 1.6 m² is: (a) 50 mg (b) 80 mg (c) 160 mg (d) 32 mg.
4. A woman's hCG rises from 1,000 to 1,400 mIU/mL in 48 hours (40%). This suggests: (a) a normal intrauterine pregnancy (b) a possible ectopic or failing pregnancy (c) twins (d) a molar pregnancy.
5. A woman of 34 weeks has painless fresh vaginal bleeding with a soft uterus. The first thing to avoid is: (a) IV fluids (b) ultrasound (c) vaginal examination (d) listening to the fetal heart.

::: note Answers and rationales
**1. (b).** SI = 110 ÷ 100 = 1.1, above 1.0 and so a sign of major haemorrhage. 0.9 would need a pulse of 90 at the same BP; 0.5 is normal.
**2. (c).** 800 ÷ 200 = 4 tablets. Three tablets give only 600 mcg (the incomplete-abortion oral dose), and eight would be 1,600 mcg.
**3. (b).** 50 × 1.6 = 80 mg. 50 mg ignores body surface area and 160 mg doubles the dose.
**4. (b).** A rise under about 49% for a starting hCG below 1,500 is subnormal, so ectopic or failing pregnancy must be excluded with ultrasound. A molar pregnancy has a very high hCG and a normal pregnancy rises faster.
**5. (c).** Painless fresh bleeding is praevia until proved otherwise and a finger can cause massive haemorrhage. Fluids, ultrasound and fetal heart assessment are all needed.
:::

**Short answer (3 marks): Define antepartum haemorrhage and list its causes.** APH is bleeding from the genital tract after 28 weeks and before birth of the baby (some countries use 24 weeks). The main causes are **placenta praevia**, **placental abruption**, **vasa praevia** and **uterine rupture**; **local causes** include cervical polyp, ectropion, trauma and show, and some bleeds have no cause. First care is two IV lines, fluids, blood tests and fetal monitoring, and **no vaginal examination** until praevia is excluded.

**Medium answer (5 marks): Differentiate placenta praevia from placental abruption (Figure 1.2).** **Placenta praevia** is a placenta implanted in the lower segment, partly or fully covering the internal os, and gives **painless, fresh, recurrent** bleeding with a **soft uterus**, a high or malpresenting fetus and a normal fetal heart. Bleeding is in proportion to shock. **Abruption** is premature separation of a normally sited placenta and gives **painful, dark or concealed** bleeding with a **hard, woody, tender uterus**, difficulty feeling fetal parts, fetal distress or death and **shock out of proportion** to the visible blood. Praevia is linked to previous caesarean and multiparity; abruption to **pre-eclampsia**, trauma, smoking and cocaine. Ultrasound shows the low placenta or the clot. Praevia needs steroids, anti-D and caesarean at 36-37 weeks (earlier if bleeding is heavy); abruption needs resuscitation and delivery with watch for DIC, renal failure and PPH. *Diagram:* four praevia grades from low-lying to complete; three abruption types (revealed, concealed, mixed).

**Long answer (10 marks): Sunita Rai, 28, G3P2 (two previous caesareans) at 34 weeks, arrives at a district hospital with painless, bright red vaginal bleeding of about 1,200 mL. Pulse 118, BP 86/54, respiratory rate 24, uterus soft and non-tender, fetal heart 150 per minute. She weighs 60 kg and is Rh positive. Write the assessment, calculations, management and a nursing care plan.**

*Assessment.* Painless fresh bleeding with a soft uterus and a normal fetal heart, after two caesareans, is **placenta praevia** until proved otherwise; a placenta accreta is possible. Her **shock index is 1.37**, a sign of major haemorrhage, and her estimated blood volume is 100 × 60 = 6,000 mL, so 1,200 mL is **20%** of her blood volume (class II-III haemorrhage). The bleeding is concealed neither by colour nor by pain, so an abruption is less likely, but the clot test is done to exclude DIC.

*Management.* **Call the obstetrician, anaesthetist and the newborn team.** Give oxygen 10 L/min by mask, lay her on her left side, insert **two 16-18 G cannulae**, send blood for group, cross-match (4 units), haemoglobin, platelets and clotting, and run **Ringer's lactate 1 L fast** followed by blood as soon as available. Catheterise, aim for urine of at least 30 mL/h, and **do no vaginal examination**. Give **dexamethasone 6 mg IM** (1.5 mL from a 4 mg/mL ampoule; four doses, 24 mg in total) if there is time, but **do not delay delivery**: with heavy bleeding and maternal shock she needs an **emergency caesarean** with an experienced surgeon, uterotonics ready, tranexamic acid 1 g IV and readiness for hysterectomy because of the accreta risk. After the birth: oxytocin infusion, measure blood loss, monitor for 24 hours in high dependency, give iron and counsel on family planning (a permanent method if she wishes, as a third caesarean raises risk). Record on HMIS and complete the MDR form if she dies. In Nepal she would be referred early, free under Aama, with a nurse escort; this is **delay 2** (reaching care) being solved.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "I feel dizzy and weak." **O:** pulse 118, BP 86/54, SI 1.37, loss 1,200 mL | **Deficient fluid volume** related to active vaginal haemorrhage | **Fluid balance:** pulse under 100, systolic BP over 100, urine at least 30 mL/h in 2 h | Two wide IV lines, Ringer's lactate 1 L fast, then blood (restore volume); oxygen 10 L/min; record vitals every 15 min; catheter and hourly urine | Pulse 96, BP 106/68, urine 40 mL/h |
| **O:** FHR 150, preterm 34 weeks, placental separation risk | **Risk for fetal injury** related to placental blood loss and preterm birth | **Fetal status:** FHR 110-160, baby born alive and breathing | Continuous CTG or FHR every 15 min (detect distress); left tilt; dexamethasone; newborn team ready | FHR stable until delivery; baby cried at birth |
| **S:** "Will I lose my baby? Will I die?" **O:** crying, clinging to husband | **Anxiety** related to threat to self and baby | **Anxiety level:** states fear is lower; cooperates with care | Stay with her, explain each step in Nepali, involve husband (reduces fear); consent; privacy | Calm; consents to caesarean |
| **O:** praevia, two previous scars, bleeding, invasive lines | **Risk for infection** related to surgery and blood loss | **Infection status:** temperature under 37.5 °C, clean wound | Hand hygiene, aseptic technique, prophylactic antibiotic before incision (cuts wound infection); monitor wound and temperature | Afebrile; wound dry on day 3 |
| **O:** low Hb expected, blood loss, new baby | **Risk for bleeding** related to praevia site atony and possible DIC | **Blood loss:** under 500 mL further; uterus firm; clot test normal | Oxytocin 10 IU, TXA 1 g, uterine massage, weigh pads; clot test; fundal check every 15 min | Uterus firm; stable Hb after 2 units |
