---
subject: Family and Reproductive Health Nursing
grade: BSc Nursing Year 3
unit: 5
title: STI, RTI, HIV and PMTCT: Syndromic Management and the Nepal National Protocols
hours: 24
area: BSN 23-24 · Family and Reproductive Health Nursing · Units 1-5
---

Rina Tamang, **24 years old**, is **16 weeks pregnant** and attends her second ANC visit at a district hospital in Sindhupalchok. Her husband returned from Qatar two months ago. She has a **thick yellow vaginal discharge with itching**, and the routine HIV test offered to every pregnant woman is **reactive** on the national rapid-test algorithm. She cries and says, "My husband will throw me out." The nurse must treat the discharge by the **syndromic chart**, confirm and counsel on HIV, start **antiretroviral therapy (ART) the same day**, protect the baby by the **PMTCT package**, and protect Rina from stigma and violence. This unit teaches that work.

::: key What this unit gives you
- Real images: a **gonorrhoea Gram stain**, **vaginal candidiasis**, **Trichomonas vaginalis**, a **primary syphilis chancre**, **HIV rapid test devices**, an **HIV ELISA plate** and a **once-daily antiretroviral tablet**; each with numbered marks.
- SVG figures: the **Nepal syndromic management chart**, the **HIV treatment cascade (95-95-95)**, and the **PMTCT four-prong package with the infant timeline**.
- **Seven points of STI and HIV prevention education** and **eight points of nursing responsibility in HIV care**, each in 3-4 plain sentences, anchored in the National Centre for AIDS and STD Control (NCASC), the national STI guideline, NNC ethics and HMIS.
- Verified maths: **the HIV treatment cascade, the 3-test algorithm and predictive value, mother-to-child transmission averted, nevirapine dose, RPR titre fall, adherence and the PEP time window**; MCQs, short, medium and long answers and a 5-column NANDA-I plan.
:::

## 5.1 Reproductive tract infections and sexually transmitted infections

**Reproductive tract infections (RTIs)** include **endogenous infections** (candidiasis, bacterial vaginosis), **sexually transmitted infections (STIs)** (gonorrhoea, chlamydia, trichomoniasis, syphilis, herpes, HPV, HIV, hepatitis B) and **iatrogenic infections** after IUCD insertion, abortion or delivery. They cause **PID, infertility, ectopic pregnancy, cervical cancer, adverse pregnancy outcomes and increased HIV risk**. In Nepal most health facilities have **no laboratory** for diagnosis, so the **national STI case management guideline (first issued in 1995 and updated in 2022)** uses the **syndromic approach**: the nurse treats the **group of signs and symptoms** for the commonest causes at the first visit. The **STI register** is kept at the clinic and reported monthly to **HMIS**. Nepal has set a target to **eliminate congenital syphilis (case rate 50 per 100,000 live births or less)** and to end STIs as a public health problem by 2030.

**Vaginal discharge syndrome.** *Normal* discharge is clear or white, odourless and varies with the cycle. *Candidiasis*: thick, **curdy white**, itching, redness, pH under 4.5, pseudohyphae on a wet mount. *Bacterial vaginosis (BV)*: thin grey, **fishy smell**, pH above 4.5, **clue cells** (Amsel's criteria: 3 of 4). *Trichomoniasis*: **frothy yellow-green**, itching, "strawberry" cervix, motile flagellates. *Cervicitis* (gonorrhoea or chlamydia): mucopurulent cervical discharge, bleeding on touch, **lower abdominal pain** if it spreads. Rina's yellow, itchy discharge in pregnancy is treated for **trichomoniasis and BV (metronidazole 400 mg twice daily for 7 days, safe after the first trimester)** and for **candidiasis (clotrimazole 500 mg pessary once)** if curdy; if cervicitis signs or a high-risk partner exist, **cefixime or ceftriaxone** plus **azithromycin** is added (doxycycline is avoided in pregnancy).

**Other syndromes** (examples follow WHO 2021 and national charts; always use the current MoHP chart): **Urethral discharge** (men): ceftriaxone 1 g IM once **plus** doxycycline 100 mg twice daily for 7 days. **Genital ulcer:** **benzathine penicillin 2.4 million units IM once** for syphilis (3 weekly doses for late or unknown duration), plus **acyclovir 400 mg three times daily for 7 days** for herpes; penicillin allergy needs doxycycline (not in pregnancy) or referral. **Lower abdominal pain (PID):** ceftriaxone 500 mg IM once **plus** doxycycline 100 mg twice daily **plus** metronidazole 400 mg twice daily for 14 days; refer if pregnant, peritonitis or no response in 72 hours. **Inguinal bubo:** treat for chancroid and lymphogranuloma venereum (azithromycin or doxycycline) and aspirate, do not incise. **Every STI patient** receives **condoms, partner notification and treatment, abstinence until both are treated, and offers of HIV, syphilis and hepatitis B testing**.

```svgfig label="5.1" caption="The syndromic management chart. The nurse recognises the syndrome, treats the common causes together at the first visit, and always adds condoms, partner treatment, counselling and testing. Doses are examples; use the current MoHP chart."
f = Fig(760, 372)
sy = [("VAGINAL DISCHARGE", "metronidazole 400 mg bd x 7 d + clotrimazole 500 mg pessary or fluconazole 150 mg;\nadd cefixime or azithromycin if cervicitis signs", MINT, TEAL), ("URETHRAL DISCHARGE", "ceftriaxone 1 g IM once + doxycycline 100 mg bd x 7 days", BLUE, NAVY), ("GENITAL ULCER", "benzathine penicillin 2.4 MU IM once + acyclovir 400 mg tds x 7 days", SAND, AMBER), ("LOWER ABDOMINAL PAIN (PID)", "ceftriaxone 500 mg IM + doxycycline + metronidazole x 14 days; refer if severe", ROSE, RED), ("INGUINAL BUBO", "azithromycin or doxycycline; aspirate the node, do not incise", MINT, TEAL)]
for i, (a_, b_, fc, sc) in enumerate(sy):
    y = 10 + i * 50
    f.box(15, y, 225, 42, a_, fill=NAVY, stroke=NAVY, color="#ffffff", size=10.5, bold=True)
    f.box(250, y, 495, 42, b_, fill=fc, stroke=sc, size=10)
f.box(15, 266, 730, 34, "FOR EVERY PATIENT: condoms | partner notification and treatment | HIV and syphilis test | hepatitis B vaccine", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(15, 308, 730, 28, "PREGNANT WOMAN: avoid doxycycline; test every woman for syphilis and HIV at ANC", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(15, 342, 730, 26, "Record in the STI register; report to HMIS monthly; review in 7 days", fill=BLUE, stroke=NAVY, size=10.5)
```

**Syphilis** (*Treponema pallidum*) passes by sex and across the placenta. **Primary:** a painless hard **chancre** after 3 weeks with painless nodes; **secondary:** rash on palms and soles, condylomata lata, fever (6-8 weeks); **latent:** no symptoms; **tertiary:** gummas, aortitis, neurosyphilis. In pregnancy untreated syphilis causes **stillbirth, preterm birth and congenital syphilis** (rhinitis, rash, bone lesions, hepatosplenomegaly). Test with a **treponemal rapid test** and **RPR** (titre in doubling dilutions 1:1, 1:2, 1:4 ... ; a **four-fold fall (two dilutions) after treatment** means success). Treat the mother and partner with benzathine penicillin and the newborn as advised.

```photogrid label="5.1" cols="4" ratio="1.0" caption="STI diagnosis in real images. (a) A Gram stain showing Neisseria gonorrhoeae diplococci with pus cells. (b) A vaginal smear with Candida yeast cells and pseudohyphae. (c) A Gram stain showing Trichomonas vaginalis. (d) A primary syphilitic chancre on the tongue, a painless round ulcer with a firm base."
@ photo id="nur14/gono" cap="Gonorrhoea Gram stain"
fit 1.0
focus 0.5 0.5
mark 0.5 0.5 "1"
key 1 (a) Pus cells and Gram-negative diplococci
@ photo id="nur14/candida" cap="Vaginal candidiasis smear"
fit 1.0
focus 0.5 0.5
mark 0.5 0.5 "2"
key 2 (b) Yeast cells and pseudohyphae
@ photo id="nur14/trich" cap="Trichomonas on Gram stain"
fit 1.0
focus 0.5 0.5
mark 0.5 0.5 "3"
key 3 (c) Pear-shaped Trichomonas among pus cells
@ photo id="nur14/chancre" cap="Primary syphilis chancre"
fit 1.0
focus 0.5 0.5
mark 0.5 0.5 "4"
key 4 (d) Painless round chancre on the tongue
```

### Seven points of STI and HIV prevention education

1. **Teach the ABC and condom use.** Explain Abstain or delay sex, Be faithful to one tested partner, and use a Condom every time. Show correct condom use on a model. Condoms are the only method that protects against both pregnancy and STI.
2. **Explain how infections spread and which signs matter.** Tell people about discharge, ulcers, pain on passing urine, lower abdominal pain and genital warts, and that many STIs show no sign at all. Knowing the signs sends them early to the clinic.
3. **Advise early care and the full course.** Stress that treatment must start at the first sign, that all tablets are completed even when the symptoms stop, and that no sex is allowed until both partners are treated. Half treatment breeds resistance and re-infection.
4. **Promote partner notification and treatment.** Help the patient tell the partner (patient referral card), without violence or blame. Untreated partners re-infect the patient. Confidentiality is explained to both.
5. **Promote testing and vaccination.** Offer HIV, syphilis and hepatitis B tests at ANC, to couples, migrants and key populations, and give hepatitis B and HPV vaccines. Testing is the first step to treatment and prevention.
6. **Reach migrant workers and key populations.** Give returning migrants and their wives information at the border, in health posts and by FCHVs; reach female sex workers, men who have sex with men, transgender people and people who inject drugs with condoms, needle exchange and friendly services. These groups carry most new infections in Nepal.
7. **Fight stigma and protect rights.** Explain that HIV does not spread by touching, sharing food or mosquitoes, that Nepal's law of 2064 BS prohibits discrimination, and that the nurse keeps every result confidential. Stigma stops people from testing more than any other barrier.

## 5.2 HIV and AIDS in Nepal

**HIV** is a retrovirus that destroys **CD4 T-helper cells**; without treatment it leads to **AIDS** (CD4 below 200 or an AIDS-defining illness) in about 8-10 years. It spreads by **unprotected sex, infected blood and needles, and from mother to child** (pregnancy, birth, breastfeeding); it does **not** spread by touch, food, coughing or mosquitoes. **Nepal (NCASC, 2024 estimates):** about **34,337 people live with HIV**; about **26,372 (77%) are on ART**; there were about **614 new infections** in 2024 (89% fewer than in 2000) and **about 569 AIDS deaths**; adult prevalence is **0.13%**. Modelling shows that **migrant workers (about 25%) and men who have sex with men and transgender people (about 19%)** account for the largest shares of new infections, followed by female sex workers, clients and people who inject drugs. Only about **58% of HIV-positive pregnant women** received ARV for PMTCT in FY 2081/82, so PMTCT is a priority. The **National HIV Strategic Plan 2021-2026** aims for **95-95-95** and an end to vertical transmission; ART is given free at **ART sites** in district hospitals and the **Sukraraj Tropical and Infectious Disease Hospital (Teku)**.

**WHO clinical stages.** **1** asymptomatic or persistent lymphadenopathy; **2** mild weight loss under 10%, recurrent mouth ulcers, herpes zoster, recurrent chest infection; **3** weight loss over 10%, chronic diarrhoea over 1 month, unexplained fever, oral thrush, **pulmonary TB**, severe bacterial infection; **4** **HIV wasting, pneumocystis pneumonia, cerebral toxoplasmosis, cryptococcal meningitis, oesophageal candidiasis, Kaposi sarcoma, extrapulmonary TB**.

**Diagnosis.** Pre-test information and **informed consent**, then the **national rapid-test algorithm of three tests** (the first is a screening test; reactive samples are retested with two others of different kind; a result is positive only if the tests agree). Infants under 18 months are tested by **HIV DNA PCR** (antibody tests show maternal antibodies). **CD4 count** and **viral load (VL)** guide care: **VL under 1,000 copies/mL is "suppressed"**, and **under 200** (or undetectable) means the virus **cannot be sexually transmitted (U = U)**.

```svgfig label="5.2" caption="The Nepal treatment cascade against the 95-95-95 goal. The top bar is the estimated 34,337 people living with HIV in 2024. The middle bar shows the 26,372 (77%) on ART. The lower bar shows the 2026 target in which 95% of people are diagnosed, 95% of those are on ART and 95% of those are virally suppressed."
f = Fig(760, 250)
full = 700
f.box(30, 20, full, 40, "Estimated people living with HIV, 2024: 34,337 (100%)", fill=BLUE, stroke=NAVY, size=11, bold=True)
w1 = round(full * 26372 / 34337)
f.box(30, 80, w1, 40, "On ART, 2024: 26,372 (77%)", fill=MINT, stroke=TEAL, size=11, bold=True)
f.box(30 + w1, 80, full - w1, 40, "gap 23%", fill=ROSE, stroke=RED, size=10.5, bold=True)
w2 = round(full * 0.95 * 0.95)
f.box(30, 140, w2, 40, "Target: on ART 95% x 95% = 90.3%", fill=SAND, stroke=AMBER, size=11, bold=True)
w3 = round(full * 0.95 * 0.95 * 0.95)
f.box(30, 200, w3, 40, "Target: suppressed 95% x 95% x 95% = 85.7%", fill=MINT, stroke=TEAL, size=11, bold=True)
```

**Antiretroviral therapy.** Nepal follows **"treat all"**: ART for everyone with HIV, started **as early as possible (same day if ready)**, regardless of CD4. First-line is **TLD once daily: tenofovir 300 mg + lamivudine 300 mg + dolutegravir 50 mg**. Side effects: nausea, headache, insomnia, weight gain, rarely kidney injury. **Adherence of 95% or more** keeps the virus suppressed; adherence support (pill box, treatment buddy, mobile reminders) and **multi-month dispensing** for stable patients keep people in care. **Opportunistic infections:** screen at every visit for **TB** (cough, fever, night sweats, weight loss; Xpert test), give **TB preventive therapy**, **cotrimoxazole prophylaxis** (960 mg daily for stage 3 or 4 or CD4 below 350), vaccinate, and treat thrush, diarrhoea and cryptococcal disease. **Post-exposure prophylaxis (PEP):** TLD for **28 days**, started **as soon as possible and within 72 hours** after a needle-stick or sexual assault, with baseline and 3-month tests. **Pre-exposure prophylaxis (PrEP)** with daily tenofovir and emtricitabine is being introduced for key populations under the national guideline.

## 5.3 Preventing mother-to-child transmission (PMTCT)

Without any intervention, **15-25% of babies** are infected during pregnancy and delivery, and up to **35-45%** if breastfeeding goes on for 2 years. With the **full package** the risk falls **below 2%** (non-breastfeeding) or **below 5%** (breastfeeding populations). The **four prongs** are: (1) **prevent HIV in women of reproductive age** (education, condoms, testing); (2) **prevent unintended pregnancy in women with HIV** (family planning, dual protection); (3) **ART for pregnant and breastfeeding women** (lifelong, started the same day; **viral load at 3 months**, then every 6 months to 12 months and yearly); and (4) **care, treatment and support** for the mother, child and family. At delivery: normal delivery is safe if VL is suppressed (caesarean only for obstetric reasons or VL above 1,000), avoid artificial rupture of membranes, episiotomy and scalp electrodes unless needed. **Infant:** **nevirapine syrup once daily from birth for 6 weeks** (12 weeks if the mother started ART late or VL is high), weight-band doses (2.0-2.4 kg 10 mg, 2.5-3.9 kg 15 mg, 4 kg or more 20 mg); **cotrimoxazole from 6 weeks** until HIV is excluded; **HIV DNA PCR at 6 weeks**, antibody test at 18 months and at 6 weeks after weaning. **Feeding:** the mother on ART with suppressed VL **exclusively breastfeeds for 6 months** and continues with complementary food (WHO and national advice); replacement feeding only if safe, affordable and sustainable.

```svgfig label="5.3" caption="PMTCT in Nepal: four prongs on top, and the mother and baby timeline below. The mother starts TLD the day HIV is confirmed and continues for life; the baby receives nevirapine from birth, PCR at 6 weeks, exclusive breastfeeding for 6 months under maternal ART and a final antibody test at 18 months."
f = Fig(760, 330)
pr = ["PRONG 1\nprevent HIV in women", "PRONG 2\nprevent unintended\npregnancy in HIV+ women", "PRONG 3\nART for pregnant and\nbreastfeeding women", "PRONG 4\ncare and support for\nmother, baby, family"]
for i, p in enumerate(pr):
    f.box(15 + i * 185, 12, 175, 56, p, fill=[BLUE, MINT, SAND, ROSE][i], stroke=[NAVY, TEAL, AMBER, RED][i], size=10, bold=True)
tl = [("ANC\nHIV and syphilis\ntest, start TLD", MINT, TEAL), ("3 months\nviral load,\nadherence check", BLUE, NAVY), ("DELIVERY\nsafe birth,\nskilled attendant", SAND, AMBER), ("BIRTH\nnevirapine\nwithin 6-12 hours", ROSE, RED), ("6 WEEKS\nPCR test,\ncotrimoxazole", BLUE, NAVY), ("6 MONTHS\nexclusive\nbreastfeeding", MINT, TEAL), ("18 MONTHS\nantibody test,\nfinal status", SAND, AMBER)]
for i, (t_, fc, sc) in enumerate(tl):
    x = 15 + i * 105
    f.box(x, 110, 98, 80, t_, fill=fc, stroke=sc, size=9.5)
    if i < 6: f.arrow([(x + 98, 150), (x + 105, 150)], color=SLATE, sw=2)
f.box(15, 210, 730, 40, "Mother: TLD for life, 95% adherence, viral load below 200 copies/mL = no sexual transmission", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(15, 262, 730, 56, "Risk of infection in the baby: 15-45% with no action; under 2% (formula) or under 5% (breastfeeding)\nwith ART, infant prophylaxis and safe feeding | record every step in the PMTCT register", fill=SAND, stroke=AMBER, size=10.5)
```

```photogrid label="5.2" cols="3" ratio="1.0" caption="HIV testing and treatment in real images. (a) Rapid HIV test devices (cassettes and a sample well): a coloured control line and a test line are read after the waiting time. (b) An HIV ELISA plate with the colour reaction in the wells. (c) A single once-daily antiretroviral tablet, the fixed-dose combination that replaced multi-pill regimens."
@ photo id="nur14/hivrapid" cap="Rapid HIV test devices"
fit 1.0
focus 0.5 0.5
mark 0.5 0.5 "1"
key 1 (a) Cassette with window for control and test lines
@ photo id="nur14/elisa" cap="HIV ELISA plate"
fit 1.0
focus 0.5 0.7
mark 0.5 0.7 "2"
key 2 (b) Coloured wells show a reactive result
@ photo id="nur14/art" cap="Once-daily ART tablet"
fit 1.0
focus 0.5 0.5
mark 0.5 0.5 "3"
key 3 (c) Single fixed-dose antiretroviral tablet
```

### Eight points of nursing responsibility in HIV care

1. **Give pre- and post-test counselling and take consent.** Explain the test, the meaning of each result and the support available, and take the person's own consent in private. Give the result in person, never by phone or through a relative. Trust and consent are the base of HIV care.
2. **Protect confidentiality and fight stigma.** Keep records locked, share results only with the person's permission and on a need-to-know basis, and challenge discrimination by staff. The NNC Code of Ethics and the 2064 BS law protect this right. Fear of disclosure is the main reason people hide and delay treatment.
3. **Follow standard precautions.** Wash hands, use gloves, a new needle for every injection, safe sharps boxes and chlorine decontamination, and report any needle-stick for PEP within 72 hours. HIV is not spread by routine care when precautions are followed, and every patient is treated as potentially infected.
4. **Start ART and support adherence.** Help to begin TLD at once, explain the once-daily tablet, side effects and the need for 95% adherence, set up reminders and a treatment supporter, and arrange refills and multi-month dispensing. Missed doses allow the virus to become resistant.
5. **Screen for opportunistic infections.** At each visit ask about cough, fever, night sweats, weight loss, diarrhoea and mouth sores, weigh the patient, send sputum for Xpert, and give TB preventive therapy and cotrimoxazole as ordered. Early TB and OI treatment prevents most deaths.
6. **Promote nutrition, hygiene and vaccination.** Advise energy-rich foods (dal, eggs, milk, oil), safe water and hand washing, treat anaemia, and give hepatitis B and other vaccines. A well-fed patient responds better to ART.
7. **Provide family planning and PMTCT care.** Offer condoms and a hormonal or long-acting method (dual protection), test and treat pregnant women at ANC, arrange the infant prophylaxis, PCR at 6 weeks and infant feeding counselling. This prevents more than 95% of infant infections.
8. **Give psychosocial support, referral and records.** Look for depression and violence, link to peer groups and community care centres, refer to the ART site and TB centre, and complete the ART and PMTCT registers and HMIS. Support helps people to stay in treatment for life.

## 5.4 Calculations

The **treatment cascade** is each step as a percentage of the one before: **on ART = people on ART ÷ people living with HIV**; the **95-95-95 target** gives **0.95 × 0.95 × 0.95 = 85.7%** of all people suppressed. **Infections averted = births × (risk without - risk with intervention)**. **Positive predictive value (PPV) = TP ÷ (TP + FP)** and rises with each extra test in a series. **Infant nevirapine** is a weight-band dose; the **volume = dose ÷ concentration**. **Adherence = doses taken ÷ doses due × 100**. **The PEP window** is 72 hours.

```python
from datetime import date, datetime, timedelta
plhiv, art = 34337, 26372
print(f"On ART = 26,372 / 34,337 = {art / plhiv * 100:.1f}%; not on ART = {plhiv - art:,} people ({(plhiv - art) / plhiv * 100:.1f}%)")
d1 = plhiv * 0.95
d2 = d1 * 0.95
d3 = d2 * 0.95
print(f"95-95-95 target: diagnosed {d1:,.0f}, on ART {d2:,.0f}, suppressed {d3:,.0f} ({d3 / plhiv * 100:.1f}%); that is {d2 - art:,.0f} more people on ART than in 2024")
print(f"Of 1,000 pregnant women with HIV, infections without action at 25% = {1000 * 0.25:.0f}; with the full package at 2% = {1000 * 0.02:.0f}; averted = {1000 * (0.25 - 0.02):.0f}")
n, prev, se, sp = 10000, 0.001, 0.995, 0.99
tp = n * prev
fp = n * (1 - prev)
line = []
for k in (1, 2, 3):
    tp, fp = tp * se, fp * (1 - sp)
    line.append(f"after test {k} the PPV is {tp / (tp + fp) * 100:.1f}%")
print("Three-test algorithm in 10,000 women at 0.1% prevalence: " + "; ".join(line))
kg = 3.0
dose = 10 if kg < 2.5 else 15 if kg < 4 else 20
print(f"Baby weighing {kg} kg: nevirapine {dose} mg once daily = {dose / 10:.1f} mL of 10 mg/mL syrup; for 6 weeks = {dose / 10 * 42:.0f} mL")
print(f"RPR titre of 1:16 falls four-fold to 1:{16 // 4} after treatment, which is two dilutions")
print(f"Adherence: 27 of 30 doses = {27 / 30 * 100:.0f}%; 29 of 30 = {29 / 30 * 100:.1f}%; the target is 95% or more")
sex = datetime(2025, 3, 14, 23, 0)
print(f"Needle-stick on Friday {sex.strftime('%d %B %Y at %H:%M')}: PEP should start before {(sex + timedelta(hours=72)).strftime('%A %d %B at %H:%M')}; course = 28 days = 28 TLD tablets")
visit = date(2025, 5, 12)
lmp = visit - timedelta(weeks=16)
print(f"Rina at 16 weeks on 12 May 2025: LMP {lmp.strftime('%d %B %Y')}; expected delivery {(lmp + timedelta(days=280)).strftime('%d %B %Y')}; viral load due {date(2025, 8, 12).strftime('%d %B %Y')}; baby PCR at 6 weeks on {(lmp + timedelta(days=280 + 42)).strftime('%d %B %Y')}")
```

```text
On ART = 26,372 / 34,337 = 76.8%; not on ART = 7,965 people (23.2%)
95-95-95 target: diagnosed 32,620, on ART 30,989, suppressed 29,440 (85.7%); that is 4,617 more people on ART than in 2024
Of 1,000 pregnant women with HIV, infections without action at 25% = 250; with the full package at 2% = 20; averted = 230
Three-test algorithm in 10,000 women at 0.1% prevalence: after test 1 the PPV is 9.1%; after test 2 the PPV is 90.8%; after test 3 the PPV is 99.9%
Baby weighing 3.0 kg: nevirapine 15 mg once daily = 1.5 mL of 10 mg/mL syrup; for 6 weeks = 63 mL
RPR titre of 1:16 falls four-fold to 1:4 after treatment, which is two dilutions
Adherence: 27 of 30 doses = 90%; 29 of 30 = 96.7%; the target is 95% or more
Needle-stick on Friday 14 March 2025 at 23:00: PEP should start before Monday 17 March at 23:00; course = 28 days = 28 TLD tablets
Rina at 16 weeks on 12 May 2025: LMP 20 January 2025; expected delivery 27 October 2025; viral load due 12 August 2025; baby PCR at 6 weeks on 08 December 2025
```

## Formula and fact sheet

- **Nepal HIV 2024 (NCASC):** 34,337 people living with HIV; 26,372 on ART (77%); about 614 new infections; adult prevalence 0.13%; 95-95-95 target; PMTCT coverage 58% in FY 2081/82.
- **Syndromes:** vaginal discharge, urethral discharge, genital ulcer, lower abdominal pain, inguinal bubo. **Syphilis:** benzathine penicillin 2.4 MU IM once (early). **Gonorrhoea:** ceftriaxone 1 g IM. **Chlamydia:** doxycycline 100 mg bd x 7 d (azithromycin in pregnancy). **Trichomonas and BV:** metronidazole 400 mg bd x 7 d.
- **ART:** TLD (tenofovir 300 + lamivudine 300 + dolutegravir 50) once daily; adherence 95% or more; viral load under 1,000 suppressed, under 200 untransmittable. **PEP:** 28 days, within 72 hours.
- **PMTCT:** no action 15-45%; full package under 2% (formula) or under 5% (breastfeeding); infant nevirapine 6 weeks; PCR at 6 weeks; antibody test at 18 months; exclusive breastfeeding 6 months under maternal ART.

## Chapter summary

- RTIs and STIs are managed by the syndromic approach in Nepal; the five syndromes are treated together at the first visit with condoms, partner treatment, counselling and testing.
- Syphilis is screened in every pregnancy and treated with benzathine penicillin; a four-fold fall in RPR titre shows cure.
- HIV is diagnosed by the national three-test algorithm; ART (TLD) is started for all, adherence of 95% keeps the virus suppressed, and TB and opportunistic infections are screened at each visit.
- PMTCT has four prongs; with maternal ART, infant nevirapine, PCR at 6 weeks and safe feeding, infant infection falls below 2-5%.
- The nurse protects confidentiality, fights stigma, uses standard precautions and records every step in the registers and HMIS.

## Practice

```python
from datetime import datetime, timedelta
print(f"MCQ1 = {15000 / 20000 * 100:.0f}%; MCQ2 = {20000 * 0.95:,.0f}; MCQ3 = {20 / 10:.1f} mL; MCQ5 = {400 * (0.25 - 0.02):.0f}; MCQ6 = 1:{32 // 4}; MCQ7 = {28 / 30 * 100:.1f}%")
print(f"MCQ4 = {(datetime(2025, 3, 15, 10) + timedelta(hours=72)).strftime('%A %H:%M')}")
```

```text
MCQ1 = 75%; MCQ2 = 19,000; MCQ3 = 2.0 mL; MCQ5 = 92; MCQ6 = 1:8; MCQ7 = 93.3%
MCQ4 = Tuesday 10:00
```

**MCQs (with reasons)**

1. Of 20,000 people living with HIV, 15,000 are on ART. The percentage on ART is: (a) 25% (b) 66.7% (c) 75% (d) 95%.
2. The 95% target for people diagnosed among 20,000 people living with HIV is: (a) 1,900 (b) 15,000 (c) 19,000 (d) 20,000.
3. A baby weighing 4.2 kg needs nevirapine 20 mg once daily using a syrup of 10 mg/mL. The volume is: (a) 0.5 mL (b) 1 mL (c) 2 mL (d) 20 mL.
4. A woman had unprotected sex with an HIV-positive partner at 10:00 on Saturday 15 March 2025. The 72-hour PEP limit is: (a) Sunday 10:00 (b) Monday 10:00 (c) Tuesday 10:00 (d) Wednesday 10:00.
5. 400 HIV-exposed infants face a 25% risk without action and 2% with the full package. The infections averted are: (a) 8 (b) 23 (c) 92 (d) 100.
6. An RPR titre of 1:32 falls four-fold after treatment. The new titre is: (a) 1:4 (b) 1:8 (c) 1:16 (d) 1:64.
7. A patient took 28 of 30 TLD doses. The adherence is: (a) 85% (b) 90% (c) 93.3% (d) 98%.
8. Why does Nepal use three rapid tests in series in a low-prevalence setting? (a) To save cost (b) Because each test is slower (c) To raise the predictive value of a positive result (d) To lower the sensitivity.

::: note Answers and rationales
**1. (c).** 15,000 ÷ 20,000 = 75%. 25% is the share not on ART; 95% is the target, not the result.
**2. (c).** 0.95 × 20,000 = 19,000. 1,900 is 9.5%; 15,000 is the number on ART in question 1.
**3. (c).** A baby of 4 kg or more takes 20 mg, and 20 ÷ 10 = 2 mL. 20 mL is a tenfold overdose.
**4. (c).** 72 hours = 3 days, so Saturday 10:00 becomes Tuesday 10:00. Starting later is still better than not starting but is less effective.
**5. (c).** 400 × (0.25 - 0.02) = 92 infections averted. 100 would be the infections without action.
**6. (b).** A four-fold fall means two dilutions, 1:32 to 1:8. A two-fold fall (1:16) is not enough to call cure.
**7. (c).** 28 ÷ 30 = 93.3%, below the 95% target, so adherence counselling is needed. 98% is not what was taken.
**8. (c).** At low prevalence a single test gives many false positives (PPV about 9%), and two or three tests in series raise the PPV above 99%, so no one is wrongly told they have HIV.
:::

**Short answer (3 marks): Name the five STI syndromes of the Nepal guideline and the principles of syndromic management.** The syndromes are vaginal discharge, urethral discharge, genital ulcer, lower abdominal pain (PID) and inguinal bubo. The nurse treats the common causes of the syndrome at the first visit, because laboratory tests are often unavailable. Every patient gets condoms, partner notification and treatment, counselling and an offer of HIV and syphilis tests, and the case is entered in the STI register and HMIS.

**Short answer (3 marks): State the indications and the regimen for HIV post-exposure prophylaxis (PEP).** PEP is for occupational needle-stick or splash injuries, sexual assault and unprotected sex with a person with HIV or unknown status. The first-line regimen is TLD (tenofovir 300 mg, lamivudine 300 mg and dolutegravir 50 mg) once daily for 28 days, started as soon as possible and within 72 hours. The wound is washed with soap and water, baseline HIV, hepatitis B and C tests are done, adherence is supported and the HIV test is repeated at 3 months.

**Medium answer (5 marks): Describe the PMTCT programme in Nepal (Figure 5.3).** The four prongs are prevention of HIV in women, prevention of unintended pregnancy in women with HIV, ART for pregnant and breastfeeding women, and care for mother, child and family. Every pregnant woman is tested for HIV and syphilis at ANC; if she is positive she starts TLD the same day, regardless of CD4, and continues for life, with viral load at 3 months. Delivery is by a skilled attendant; caesarean is for obstetric reasons or when the viral load is above 1,000 copies/mL, and avoidable procedures are not done. The baby receives nevirapine syrup within 6-12 hours and daily for 6 weeks (12 weeks if the mother started late), cotrimoxazole from 6 weeks, an HIV DNA PCR at 6 weeks and an antibody test at 18 months. The mother breastfeeds exclusively for 6 months under ART and adds complementary food after that. With these steps, transmission falls from 15-45% to under 2-5%. The nurse keeps records in the PMTCT register and HMIS.

**Long answer (10 marks): Rina Tamang, 24, is 16 weeks pregnant, has a reactive HIV test and a thick yellow itching discharge. Her husband returned from Qatar two months ago. Calculate the dates and doses, plan the PMTCT, and write the nursing care plan.**

*Calculations and interpretation.* The reactive result must be confirmed by the **three-test algorithm** (in a woman with 0.1% prevalence, one test alone has a PPV of only about 9%; three tests in series raise it above 99%). If confirmed, Rina is **HIV positive, probably infected by her husband**. If her visit date is 12 May 2025 at 16 weeks, her **LMP was 20 January 2025** and her **expected delivery is 27 October 2025**. **Viral load is due on 12 August 2025** (3 months after starting ART). Her baby, expected to weigh about 3.0 kg, will receive **nevirapine 15 mg (1.5 mL of 10 mg/mL) daily for 6 weeks (63 mL in total)**, and the **PCR is due at 6 weeks, about 8 December 2025**. Without any action, about **25% of babies** are infected; with the full package the risk is **2%**, so 230 of 1,000 infections are averted.

*Management.* The nurse first gives post-test counselling in a private room, with Rina's consent for every step. She explains that HIV is a long-term condition that is treated with one daily tablet, that she can have a healthy baby and live a normal life, and that she is not to blame. **TLD** is started the same day. For the discharge she gives metronidazole 400 mg twice daily for 7 days and a clotrimazole 500 mg pessary, with partner treatment and condoms. Syphilis and hepatitis B tests are done, TB symptoms are screened, haemoglobin is checked, iron-folic acid is given and ANC continues with at least 4 visits. She supports disclosure to her husband in a safe way (with a counsellor, and a safety plan if there is a risk of violence), invites him for testing, and arranges family planning for the future. The nurse plans a facility birth, infant prophylaxis, PCR at 6 weeks, exclusive breastfeeding for 6 months under maternal ART, and tracing of mother and baby by the ART site and FCHV. Records go into the ART and PMTCT registers and HMIS under a code, not her name.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "My husband will throw me out." **O:** tearful, new reactive test | **Fear** related to HIV diagnosis and possible violence or abandonment | **Fear self-control:** names support persons and a safety plan | Private counselling, confirm the result, discuss safe disclosure with a counsellor, safety plan and OCMC contacts (reduces fear and risk of harm) | States 2 supports and agrees to the plan |
| **S:** "Will my baby have HIV?" **O:** 16 weeks pregnant, knowledge poor | **Deficient knowledge** (HIV, ART, PMTCT, infant feeding) related to a new diagnosis | **Knowledge: infection management:** explains ART, the 6-week PCR and feeding plan | Teach with pictures and teach-back; written schedule of visits (informed mothers adhere better and protect the baby) | Correct teach-back, dates on card |
| **O:** HIV positive, needs lifelong TLD, VL due 12 August | **Risk for ineffective health management** (adherence) related to stigma and fear | **Treatment behaviour: illness or injury:** adherence 95% or more | Same-day ART, pill reminders, treatment buddy, refill dates (missed doses cause drug resistance and infant risk) | 29 of 30 doses taken; VL under 200 at 3 months |
| **S:** "It itches and smells." **O:** yellow discharge and vulvar redness | **Impaired comfort** related to vaginal infection | **Symptom control:** itching absent in 7 days | Metronidazole 400 mg bd x 7 d, clotrimazole pessary, cotton underwear, no douching, partner treatment, condoms (treats the syndrome and prevents reinfection) | Discharge cleared at review |
| **O:** TB, syphilis and hepatitis B status unknown; pregnancy | **Risk for infection** (opportunistic, vertical) related to immunosuppression and pregnancy | **Infection status:** no TB or OI; baby HIV negative at 18 months | Screen for TB and syphilis, cotrimoxazole if indicated, vaccines, infant nevirapine 15 mg (1.5 mL) x 6 weeks, PCR at 6 weeks (early detection and prophylaxis protect mother and baby) | Screen negative; baby PCR negative at 6 weeks |
