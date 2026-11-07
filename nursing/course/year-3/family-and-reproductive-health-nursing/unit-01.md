---
subject: Family and Reproductive Health Nursing
grade: BSc Nursing Year 3
unit: 1
title: Reproductive Health in Nepal, Adolescents, Gender-Based Violence and Safe Abortion
hours: 20
area: BSN 23-24 · Family and Reproductive Health Nursing · Units 1-5
---

Sabina Magar is **17 years old**, a Grade 12 student in Bhaktapur. Her last menstrual period (LMP) began on **12 January 2025**. On **16 March 2025** she comes to the health post with a friend, afraid and ashamed, with a positive urine pregnancy test. She says she does not want to continue the pregnancy and that nobody at home knows. The nurse must be kind, keep her secret, know the law, count the weeks, explain the choices and offer contraception before she leaves. This one visit uses everything in this unit.

::: key What this unit gives you
- Real images: **school students in Bhaktapur**, a **community health teaching session**, **Paropakar Maternity and Women's Hospital** and a **pregnancy test strip** sold in Nepal; each with numbered marks.
- SVG figures: the **reproductive health continuum across the life cycle**, the **Nepal policy timeline**, and the **abortion pathway under the Safe Motherhood and Reproductive Health Rights Act 2075**.
- **Eight points of adolescent-friendly nursing care**, **seven points of care for a survivor of violence** and **eight points of nursing responsibility in safe abortion**, each in 3-4 plain sentences anchored in MoHP, NNC, NDHS 2022 and the Nepal law.
- Verified maths: **total fertility rate, general fertility rate, demand satisfied, gestational age, expected date of delivery** and **medical abortion doses**; MCQs, short, medium and long answers and a 5-column NANDA-I plan.
:::

## 1.1 Reproductive health: meaning, components and rights

**Reproductive health (RH)** is a state of complete physical, mental and social well-being in all matters related to the reproductive system, not only the absence of disease. The **International Conference on Population and Development (ICPD, Cairo 1994)** gave this definition and said that people should be able to have a **satisfying and safe sex life**, the **capacity to reproduce**, and the **freedom to decide if, when and how often** to do so. **Sexual and reproductive health and rights (SRHR)** add that these choices are human rights. Article 38 of the **Constitution of Nepal (2015)** gives every woman the right to safe motherhood and reproductive health and forbids violence against her.

The **components of RH** (a favourite short note) are: **safe motherhood** (antenatal, delivery, postnatal and newborn care), **family planning**, **safe abortion**, **adolescent sexual and reproductive health**, **prevention and care of STIs including HIV**, **infertility care**, **gynaecological problems and cancers (cervix, breast)**, **menopause and elderly women's health**, **prevention of gender-based violence**, and **men's participation**. Nepal's package follows the same list. The nurse sees every component in daily work, so you should keep it in mind as one **continuum of care** from birth to old age.

**Key terms.** *Fertility* is actual childbearing; *fecundity* is the biological ability. The **crude birth rate** is births per 1,000 population; the **general fertility rate (GFR)** is births per 1,000 women aged 15-49; the **age-specific fertility rate (ASFR)** is births per 1,000 women of one age group; the **total fertility rate (TFR)** is the number of children a woman would have if she lived through the reproductive years at the current ASFRs, so **TFR = 5 × (sum of ASFR) ÷ 1,000** when 5-year groups are used. **Replacement level** is a TFR of about **2.1**.

```svgfig label="1.1" caption="The reproductive health continuum. Each life stage has its own needs, but the care is joined: a healthy girl becomes a healthy adolescent, a safe mother and a healthy older woman. The red band lists the cross-cutting rights that apply at every stage."
f = Fig(760, 330)
st = ["CHILDHOOD\n0-9 years", "ADOLESCENCE\n10-19 years", "REPRODUCTIVE AGE\n20-49 years", "MENOPAUSE\n45-55 years", "OLDER AGE\n60 years and over"]
need = ["Nutrition, HPV and\nroutine vaccines,\nbirth registration,\nprotection from abuse", "Puberty and menstrual\nhealth, life skills,\ncontraception, anaemia,\nprevention of early\nmarriage", "Family planning, ANC,\nsafe delivery, PNC,\nsafe abortion, STI and\nHIV care, infertility", "Hot flushes, bone and\nheart health, cervical\nand breast screening,\nprolapse care", "Prolapse, osteoporosis,\ncancers, dignity and\nsocial support"]
cols = [(MINT, TEAL), (BLUE, NAVY), (SAND, AMBER), (MINT, TEAL), (BLUE, NAVY)]
for i in range(5):
    x = 15 + i * 147
    f.box(x, 14, 140, 48, st[i], fill=NAVY, stroke=NAVY, color="#ffffff", size=10.5, bold=True)
    f.box(x, 74, 140, 150, need[i], fill=cols[i][0], stroke=cols[i][1], size=10.5)
    if i < 4: f.arrow([(x + 140, 38), (x + 147, 38)], color=SLATE, sw=2)
f.box(15, 238, 730, 34, "Services come through health posts, PHCCs, hospitals, FCHVs and school health programmes under MoHP", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(15, 284, 730, 36, "RIGHTS: information, choice, privacy, consent, no violence, respect | Article 38, Constitution 2015", fill=ROSE, stroke=RED, size=10.5, bold=True)
```

## 1.2 Reproductive health policy and indicators in Nepal

Nepal started the **National Safe Motherhood Programme in 1997** and a **National Reproductive Health Strategy in 1998**. **Abortion was legalised in 2002** (Eleventh Amendment of the Muluki Ain). The **Aama (Safe Motherhood) Programme of 2009** pays transport and delivery incentives and free care. The **Safe Motherhood and Reproductive Health Rights Act 2075 (2018)** turned the constitutional right into law: it covers safe motherhood, newborn care, family planning, safe abortion, infertility services, and punishes denial of service. The current **Nepal Health Sector Strategic Plan** sets the direction for MoHP, and the **Family Welfare Division** of the Department of Health Services runs the programme. Facility data flow into **HMIS/DHIS2**.

```svgfig label="1.2" caption="Nepal's reproductive health milestones from the 1994 Cairo conference to the 2022 survey. Every milestone widened the services a nurse can offer."
f = Fig(760, 210)
ev = [("1994", "ICPD Cairo\nRH and rights"), ("1997", "Safe Motherhood\nProgramme"), ("1998", "National RH\nStrategy"), ("2002", "Abortion\nlegalised"), ("2009", "Aama\nProgramme"), ("2015", "Constitution,\nArticle 38"), ("2018", "SMRHR Act\n2075"), ("2022", "NDHS 2022\nTFR 2.1")]
f.line(30, 70, 730, 70, color=NAVY, sw=3)
for i, (y_, t_) in enumerate(ev):
    x = 20 + i * 91
    f.circle(x + 45, 70, 9, fill=AMBER, stroke=NAVY)
    f.box(x, 14, 90, 30, y_, fill=NAVY, stroke=NAVY, color="#ffffff", size=11, bold=True)
    f.box(x, 100, 90, 54, t_, fill=BLUE if i % 2 == 0 else MINT, stroke=NAVY, size=10)
f.box(15, 168, 730, 32, "Each step added a right or a service: from safe delivery, to choice, to law and enforcement", fill=SAND, stroke=AMBER, size=10.5, bold=True)
```

**The numbers a nurse should know (NDHS 2022).** The **TFR is 2.1** children per woman (2.3 in 2016). **57%** of currently married women use a contraceptive method: **43% a modern method** (female sterilisation 13%, injectables 9%, implants 6%) and **15% a traditional method** (withdrawal 13%). The **total demand** for family planning is **78%** and **21%** of married women have an **unmet need**; only about **55%** of the demand is met by modern methods. **Physical violence since age 15 is reported by 23%** of women aged 15-49 and **sexual violence by 8%**. Skilled birth attendance is about **80%** and four ANC visits **81%** (see Midwifery I). Modern method use has stayed at about **43% since 2011**, so Nepal needs better choice and counselling more than more clinics.

```photogrid label="1.3" cols="4" ratio="1.0" caption="Reproductive health at work in Nepal. (a) School students in Bhaktapur, the age group that needs life-skills and adolescent-friendly services. (b) A community health teaching session in a Nepal village: group teaching is the main route for reproductive health messages. (c) Paropakar Maternity and Women's Hospital, Kathmandu, the national referral centre for women. (d) A pregnancy test strip sold in Nepal: a positive line begins the care pathway."
@ photo id="nur14/girls" cap="Students in Bhaktapur"
fit 1.0
focus 0.45 0.5
mark 0.45 0.55 "1"
key 1 (a) Adolescents in school uniform
@ photo id="nur14/teach" cap="Community health teaching"
fit 1.0
focus 0.5 0.5
mark 0.45 0.35 "2"
key 2 (b) Group sitting for a health talk
@ photo id="nur14/paropakar" cap="Paropakar Maternity and Women's Hospital"
fit 1.0
focus 0.5 0.5
mark 0.5 0.5 "3"
key 3 (c) Main building of the women's hospital
@ photo id="nur14/ptest" cap="Pregnancy test strips"
fit 1.0
focus 0.5 0.5
mark 0.5 0.55 "4"
key 4 (d) Strip pack for the urine hCG test
```

## 1.3 Adolescent sexual and reproductive health

**Adolescence** is the age of **10-19 years** (WHO); **youth** is 15-24 years. It is a time of **puberty** (breast budding at 9-11 years, menarche at about 12-13 years in Nepal), fast growth, and a search for identity. Nepal's problems are **child marriage** (the legal age of marriage is 20 for both sexes under the Criminal Code 2074), **early pregnancy**, **anaemia**, **poor menstrual hygiene**, **unsafe abortion**, **STIs and HIV**, **substance use** and **violence**. Many girls miss school during menstruation, and in far-western Nepal the **chhaupadi** custom (now a crime under the Criminal Code) has caused deaths. MoHP runs **adolescent-friendly health services (AFHS)** in selected health facilities, the school health and nutrition programme, and weekly iron-folic acid tablets for school girls.

### Eight points of adolescent-friendly nursing care

1. **Give privacy and confidentiality.** Talk in a closed room and promise that nothing will be told to parents, teachers or neighbours except where the law demands protection from harm. Adolescents stay away from clinics when they fear gossip. Trust is the first treatment.
2. **Use a respectful, non-judging attitude.** Sit at the same level, use simple Nepali, and never scold about sex. A blamed girl will hide the problem and delay care. Praise her for coming.
3. **Provide correct information.** Explain puberty, menstruation, pregnancy, contraception and STIs with models and pictures, and correct myths such as "periods make a girl impure". Wrong beliefs lead to harm. Correct facts give power.
4. **Teach menstrual hygiene.** Show how to use and dispose of pads or a clean cloth, change every 4-6 hours, wash and sun-dry cloth, and keep a calendar. Good hygiene lowers urinary and genital infections and school absence.
5. **Screen for anaemia and nutrition.** Check haemoglobin, give weekly iron-folic acid tablets, and advise green leaves, lentils, eggs and vitamin C foods. Girls need iron after menarche and are the mothers of the next generation.
6. **Counsel on contraception and dual protection.** Offer condoms, pills, injectables and implants as suited, and advise condoms against STI along with another method. Emergency contraception is explained as a back-up. Early choices prevent unsafe abortion.
7. **Screen for risk and violence.** Ask gently about coercion, early marriage pressure, tobacco, alcohol and low mood using the HEEADSSS prompts (Home, Education, Eating, Activities, Drugs, Sex, Suicide, Safety). Early detection prevents long harm. Refer to OCMC or mental health services when needed.
8. **Involve parents, teachers and peers.** Hold school talks, form peer educator groups and meet parents with consent. A supportive family and school protect the girl more than any clinic. Always put the adolescent's welfare first.

## 1.4 Gender-based violence (GBV)

**Gender-based violence** is any harm done to a person because of gender: physical, sexual, emotional, economic, or harmful practices such as **child marriage, dowry-related abuse, witch accusation (boksi), chhaupadi and trafficking**. In Nepal, **NDHS 2022** shows that **23%** of women aged 15-49 had physical violence after age 15, **8%** had sexual violence, and **28%** of women who ever had a partner faced partner violence (physical, sexual or emotional); the usual perpetrator is the current husband. Only a minority seek help. The main laws are the **Domestic Violence (Offence and Punishment) Act 2066**, the **Criminal Code 2074** (rape, child marriage, chhaupadi, human trafficking) and the **Act Relating to Children 2075**. Hospitals run **One-Stop Crisis Management Centres (OCMC)** where the survivor receives medical care, counselling, police and legal support, and temporary shelter in one place. Helplines include **Nepal Police 100**, **National Women Commission 1145** and **Childline 1098** (confirm numbers in the current directory).

### Seven points of nursing care for a survivor of violence

1. **Treat life-threatening injury first.** Check airway, breathing and circulation, stop bleeding and give pain relief. A survivor can be badly hurt and ashamed to say so. Safety of life comes before the story.
2. **Believe, listen and do not blame.** Say "It is not your fault" and let her tell the story in her own words once, with a female nurse if she prefers. Blame closes the door to care. Respect helps healing.
3. **Collect evidence with consent.** Keep clothes in paper bags, record injuries on a body chart in the survivor's own words, and take swabs only with written consent and by the trained doctor. Good records support the case without further trauma. Never ask repeated questions.
4. **Give post-rape medical care within 72 hours.** Offer emergency contraception (levonorgestrel 1.5 mg), HIV post-exposure prophylaxis for 28 days, tetanus and hepatitis B vaccine, and syndromic STI treatment. Early drugs prevent pregnancy and infection. Delay reduces benefit.
5. **Offer psychological first aid and screening.** Look, listen and link; assess for depression, panic and suicide risk, and refer to counselling and the mental health helpline 1166. Many survivors have shock and shame for weeks. Gentle support lowers long-term harm.
6. **Make a safety plan.** Ask who is safe at home, arrange shelter or a trusted relative, and note emergency contacts and the nearest OCMC. A plan can save a life in the next attack. The survivor decides what to do.
7. **Report, document and refer.** Explain the legal options, help to contact the police and legal aid if she chooses, and record everything in the confidential register. Follow the NNC Code of Ethics on confidentiality. Child survivors must be reported to child protection authorities.

## 1.5 Safe abortion in Nepal

An **abortion** is the end of a pregnancy before viability (before 28 weeks in Nepal). Unsafe abortion once caused a large share of maternal deaths in Nepal; after legalisation in 2002, the share fell sharply. The **SMRHR Act 2075, Section 15** says: abortion is allowed **on the woman's own decision up to 12 weeks**; **up to 28 weeks** when the pregnancy is from **rape or incest**, when the **woman's life, physical or mental health is at risk**, when there is a **serious fetal impairment**, or when the woman is **HIV positive or has an incurable disease**; and at any time to save life. **Only the woman's consent is needed** (no husband or parent consent), **sex-selective abortion is forbidden**, and only **government-approved trained providers** in **approved sites** may give the service, which is **free at public facilities**. (Readers will meet 18 weeks quoted for rape and incest in older notes and in the Criminal Code; the 2075 Act gives 28 weeks, and a nurse must follow the current MoHP circular.)

**Methods.** *Medical abortion (MA)*: **mifepristone 200 mg orally**, then **misoprostol 800 micrograms** (four 200 microgram tablets) **buccal or sublingual after 24-48 hours**; the Nepal CAC protocol approves it **up to 9 weeks (63 days)**. *Manual vacuum aspiration (MVA)*: a hand-held syringe, **up to 12 weeks**. *Dilatation and evacuation or induction* are used later by trained doctors. A nurse is part of the **comprehensive abortion care (CAC)** team: counselling, assessment, pain relief, post-abortion contraception.

```svgfig label="1.3" caption="The legal and clinical pathway for abortion in Nepal. The woman's decision and consent are the centre; the gestation decides the route and the legal ground. Post-abortion contraception is offered in every route."
f = Fig(760, 330)
f.box(270, 10, 220, 40, "Woman asks for abortion\nconsent from her alone", fill=NAVY, stroke=NAVY, color="#ffffff", size=10.5, bold=True)
f.box(270, 70, 220, 40, "Confirm pregnancy, LMP, scan if\nin doubt; count the weeks", fill=BLUE, stroke=NAVY, size=10.5)
f.arrow([(380, 50), (380, 70)], color=SLATE, sw=2)
f.box(15, 135, 220, 62, "Up to 12 weeks\non her own decision, no reason\nMA to 63 days or MVA to 12 weeks", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(270, 135, 220, 62, "12 to 28 weeks on grounds\nrape or incest, danger to health,\nfetal impairment, HIV or incurable illness", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(525, 135, 220, 62, "Any week\nto save the woman's life\n(licensed doctor decides)", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.arrow([(380, 110), (125, 135)], color=SLATE, sw=1.8)
f.arrow([(380, 110), (380, 135)], color=SLATE, sw=1.8)
f.arrow([(380, 110), (635, 135)], color=SLATE, sw=1.8)
f.box(15, 215, 730, 40, "Pain relief, infection control, Rh check, anti-D if Rh negative | follow up in 2 weeks | warning signs explained", fill=BLUE, stroke=NAVY, size=10.5)
f.box(15, 270, 730, 44, "POST-ABORTION CONTRACEPTION the same day: pill, injectable, implant, IUCD or condom | ovulation can return within 2 weeks", fill=SAND, stroke=AMBER, size=10.5, bold=True)
```

### Eight points of nursing responsibility in safe abortion

1. **Counsel without judgement.** Explain choices (continue, adoption, abortion) in neutral words and respect her decision. Pressure causes harm and delay. Counselling is the nurse's first duty in CAC.
2. **Confirm consent and confidentiality.** Record the woman's own consent (a guardian signs only if she is a minor under the facility rule and the law allows). No husband permission is needed. Keep the register locked.
3. **Count the gestation exactly.** Use LMP, uterine size and, where available, ultrasound. The route and the legal ground depend on weeks. A wrong count can mean a wrong method.
4. **Check health and Rh group.** Ask about allergy, bleeding disorders, anaemia, ectopic signs and the blood group. Give anti-D to Rh-negative women according to protocol. This avoids danger and later haemolytic disease in the baby.
5. **Give the drugs or assist the procedure correctly.** For MA, give mifepristone 200 mg, then misoprostol 800 micrograms as ordered; for MVA, prepare the sterile set, give a paracervical block and monitor. Correct dose and sterile technique prevent failure and sepsis.
6. **Control pain and bleeding.** Give ibuprofen, offer a hot water bottle, and tell her that cramps and bleeding like a heavy period for several days are normal. Check pad count and vital signs. Calm explanation lowers fear.
7. **Teach warning signs and follow-up.** Return at once for soaking 2 pads in an hour for 2 hours, fever above 38 °C, severe pain, foul discharge or no bleeding after the drugs. Follow up in 2 weeks. Early return prevents deaths.
8. **Offer contraception and record.** Start the chosen method before she leaves and enter data in HMIS (CAC register). Fertility returns within about 2 weeks. A protected woman avoids a repeat crisis.

## 1.6 Calculations

Fertility is measured by **ASFR**, **TFR = 5 × ΣASFR ÷ 1,000** and **GFR = births ÷ women aged 15-49 × 1,000**. Family planning is measured by the **contraceptive prevalence rate (CPR)**, **unmet need** and **total demand = CPR + unmet need**; the **demand satisfied by modern methods = modern CPR ÷ total demand × 100**. Pregnancy is dated from the **LMP**: **gestation in days ÷ 7 = weeks**, and **Naegele's rule** gives the **EDD = LMP + 7 days - 3 months + 1 year**.

```python
from datetime import date, timedelta
asfr = [65, 135, 120, 65, 28, 8, 1]
tfr = 5 * sum(asfr) / 1000
print(f"Total of the seven age-specific fertility rates = {sum(asfr)} per 1,000; total fertility rate = {tfr:.2f} children per woman")
gfr = 1200 / 25000 * 1000
print(f"General fertility rate = {gfr:.1f} births per 1,000 women aged 15-49")
cpr, unmet, modern = 57, 21, 43
demand = cpr + unmet
print(f"Total demand for family planning = {demand}%; demand satisfied by modern methods = {modern / demand * 100:.1f}%")
lmp, visit = date(2025, 1, 12), date(2025, 3, 16)
days = (visit - lmp).days
print(f"Sabina's gestation on 16 March 2025 = {days} days = {days // 7} weeks {days % 7} days")
def naegele(d0):
    d = d0 + timedelta(days=7)
    m, y = d.month - 3, d.year + 1
    if m <= 0:
        m, y = m + 12, y - 1
    return date(y, m, d.day)
edd = naegele(lmp)
print(f"Expected date of delivery by Naegele's rule = {edd.strftime('%d %B %Y')}")
limit12 = lmp + timedelta(days=84)
print(f"The 12-week limit for abortion on request falls on {limit12.strftime('%d %B %Y')}, which is {(limit12 - visit).days} days after the visit")
print(f"Medical abortion: mifepristone 200 mg, then misoprostol 800 micrograms = {800 // 200} tablets of 200 micrograms, due between 17 and 18 March")
print(f"Of 400 women in a clinic, 23% with physical violence since age 15 = {0.23 * 400:.0f} women")
```

```text
Total of the seven age-specific fertility rates = 422 per 1,000; total fertility rate = 2.11 children per woman
General fertility rate = 48.0 births per 1,000 women aged 15-49
Total demand for family planning = 78%; demand satisfied by modern methods = 55.1%
Sabina's gestation on 16 March 2025 = 63 days = 9 weeks 0 days
Expected date of delivery by Naegele's rule = 19 October 2025
The 12-week limit for abortion on request falls on 06 April 2025, which is 21 days after the visit
Medical abortion: mifepristone 200 mg, then misoprostol 800 micrograms = 4 tablets of 200 micrograms, due between 17 and 18 March
Of 400 women in a clinic, 23% with physical violence since age 15 = 92 women
```

## Formula and fact sheet

- **TFR** = 5 × ΣASFR ÷ 1,000. **GFR** = births ÷ women 15-49 × 1,000. Replacement TFR is about 2.1. **Total demand** = CPR + unmet need; **demand satisfied** = modern CPR ÷ total demand.
- **NDHS 2022:** TFR 2.1; CPR 57%, modern 43%, traditional 15%; unmet need 21%; total demand 78%; physical violence 23%, sexual violence 8%, partner violence 28%.
- **Law:** abortion on request to 12 weeks; to 28 weeks on grounds; woman's consent only; sex selection forbidden; free in public facilities (SMRHR Act 2075, Section 15).
- **Medical abortion:** mifepristone 200 mg, then misoprostol 800 micrograms after 24-48 hours, up to 63 days in the Nepal protocol; **MVA** up to 12 weeks.
- **Post-rape:** emergency contraception within 72 hours (up to 120 hours with some methods), PEP for 28 days, tetanus, hepatitis B, STI cover, OCMC referral.

## Chapter summary

- Reproductive health covers safe motherhood, family planning, safe abortion, adolescent care, STI and HIV, infertility, gynaecological problems and cancers, menopause and violence prevention, as one continuum with rights at the centre.
- Nepal's policy moved from the 1997 Safe Motherhood Programme to the 2015 constitutional right and the 2018 Safe Motherhood and Reproductive Health Rights Act.
- NDHS 2022 shows a TFR of 2.1, modern method use stuck at 43% and an unmet need of 21%.
- Adolescent-friendly care rests on privacy, respect, correct information and early screening; survivors of violence need life-saving care, evidence with consent, post-rape drugs and a safety plan.
- Abortion is legal on request to 12 weeks and on grounds to 28 weeks with the woman's consent alone; the nurse counsels, dates the pregnancy, assists, teaches warning signs and gives contraception.

## Practice

```python
from datetime import date, timedelta
print(f"MCQ1 = {5 * 380 / 1000:.1f}; MCQ2 = {900 / 20000 * 1000:.0f}; MCQ3 = {40 / 80 * 100:.0f}%")
d1 = (date(2025, 4, 27) - date(2025, 2, 2)).days
print(f"MCQ4 = {d1} days = {d1 // 7} weeks; MCQ5 = {800 // 200} tablets; MCQ7 = {78 - 57}%")
def naegele(d0):
    d = d0 + timedelta(days=7)
    m, y = d.month - 3, d.year + 1
    if m <= 0:
        m, y = m + 12, y - 1
    return date(y, m, d.day)
print(f"MCQ6 = {naegele(date(2025, 5, 10)).strftime('%d %B %Y')}")
```

```text
MCQ1 = 1.9; MCQ2 = 45; MCQ3 = 50%
MCQ4 = 84 days = 12 weeks; MCQ5 = 4 tablets; MCQ7 = 21%
MCQ6 = 17 February 2026
```

**MCQs (with reasons)**

1. The sum of age-specific fertility rates (5-year groups) is 380 per 1,000. The total fertility rate is: (a) 0.38 (b) 1.9 (c) 3.8 (d) 19.
2. There were 900 births among 20,000 women aged 15-49. The general fertility rate is: (a) 4.5 (b) 18 (c) 45 (d) 90.
3. The modern CPR is 40% and the total demand is 80%. The demand satisfied by modern methods is: (a) 32% (b) 40% (c) 50% (d) 80%.
4. LMP was 2 February 2025 and the visit is on 27 April 2025. The gestation is: (a) 10 weeks (b) 11 weeks (c) 12 weeks (d) 13 weeks.
5. How many 200 microgram tablets make a misoprostol dose of 800 micrograms? (a) 2 (b) 3 (c) 4 (d) 8.
6. LMP was 10 May 2025. The EDD by Naegele's rule is: (a) 17 February 2026 (b) 10 February 2026 (c) 17 March 2026 (d) 10 August 2026.
7. CPR is 57% and total demand is 78%. The unmet need is: (a) 15% (b) 21% (c) 43% (d) 55%.
8. Under the Safe Motherhood and Reproductive Health Rights Act 2075, whose consent is needed for abortion at 10 weeks? (a) Husband (b) Parents (c) The woman (d) A court.

::: note Answers and rationales
**1. (b).** 5 × 380 ÷ 1,000 = 1.9, just below replacement. 3.8 multiplies by 10 instead of 5, and 0.38 divides by 1,000 but forgets the 5-year width.
**2. (c).** 900 ÷ 20,000 × 1,000 = 45 per 1,000 women. 4.5 moves the decimal point; 90 doubles it.
**3. (c).** 40 ÷ 80 = 50%. 40% is the CPR itself and 80% is the demand, not the share met.
**4. (c).** 2 Feb to 27 Apr is 84 days, which is exactly 12 weeks, the last day of the on-request window. 11 and 13 weeks come from counting months as 4 weeks or adding a month.
**5. (c).** 800 ÷ 200 = 4 tablets. Two tablets give only 400 micrograms and would risk an incomplete abortion.
**6. (a).** 10 May + 7 days = 17 May; minus 3 months = 17 February 2026. Option (b) forgets the 7 days; (c) subtracts 2 months only.
**7. (b).** Total demand = CPR + unmet need, so 78 - 57 = 21%. 43% is the modern method use.
**8. (c).** The Act requires only the woman's own consent up to 12 weeks. Husband or parent consent is not needed, and a court order is not part of the process.
:::

**Short answer (3 marks): Define reproductive health and list its components.** Reproductive health is complete physical, mental and social well-being in all matters of the reproductive system, with the right to a safe sex life and to decide if, when and how often to have children (ICPD 1994). The components are safe motherhood, family planning, safe abortion, adolescent health, STI and HIV prevention and care, infertility care, gynaecological problems and cancers, menopause and elderly care, prevention of violence and men's participation. Nepal follows this package through the Family Welfare Division and the SMRHR Act 2075.

**Short answer (3 marks): State the legal provisions for abortion in Nepal.** Under Section 15 of the Safe Motherhood and Reproductive Health Rights Act 2075, a woman may have an abortion on her own decision up to 12 weeks. Up to 28 weeks it is allowed for pregnancy from rape or incest, danger to the woman's life, physical or mental health, serious fetal impairment, or HIV or another incurable disease. Only the woman's consent is needed, sex-selective abortion is forbidden, and only trained providers at approved sites may perform it, free of cost in public facilities.

**Medium answer (5 marks): Describe the nurse's role in the care of a survivor of sexual violence (Figure 1.3 and Section 1.4).** The nurse first treats life-threatening injury and gives a private, safe room with a female nurse if wished. She believes the survivor, listens without blame and explains each step. With written consent, she documents injuries on a body chart, keeps clothes in paper bags and helps the doctor collect swabs. Within 72 hours she gives emergency contraception (levonorgestrel 1.5 mg), HIV post-exposure prophylaxis for 28 days, tetanus and hepatitis B vaccine and syndromic STI treatment. She offers psychological first aid, screens for suicide risk and refers to counselling (helpline 1166). She makes a safety plan, links the survivor to the One-Stop Crisis Management Centre, police and legal aid only as the survivor chooses, keeps all records confidential in line with the NNC Code of Ethics, and arranges follow-up at 2 weeks, 6 weeks, 3 months and 6 months for repeat HIV and STI tests.

**Long answer (10 marks): Sabina Magar, 17, has a positive pregnancy test and an LMP of 12 January 2025. She visits the health post on 16 March 2025 and wants to end the pregnancy. Calculate the gestation, state the law and the method, and write the nursing care plan.**

*Calculations.* From 12 January to 16 March is **63 days = 9 weeks 0 days**. Her **EDD by Naegele's rule is 19 October 2025**. The **12-week limit** for abortion on request falls on **6 April 2025**, 21 days away, so she has time to decide, but she should not wait. She is within the **63-day (9-week) limit for medical abortion**, so **mifepristone 200 mg** can be given today and **misoprostol 800 micrograms (four 200 microgram tablets) buccally on 17 or 18 March**.

*Legal position.* She is under 12 weeks, so under **Section 15 of the SMRHR Act 2075** she decides by herself; **no consent from parents or a husband is needed**, the service is **free** at a government site and the provider must be **trained and approved**. As a minor she must be asked who she trusts, and if the pregnancy came from rape, incest or coercion, the nurse follows the child protection and OCMC route and tells her that abortion remains available up to 28 weeks on that ground.

*Management.* The nurse gives private counselling about all options and records her own consent. She checks vital signs, haemoglobin, blood group (anti-D if Rh negative), allergy and signs of ectopic pregnancy (pain, bleeding, shoulder-tip pain). She assists with the drugs, gives ibuprofen for cramps and tells her that heavy bleeding for several days is expected. She teaches the **warning signs** (soaking two pads in an hour for two hours, fever above 38 °C, severe pain, foul discharge, no bleeding) and gives the health post number. A follow-up visit is booked at 2 weeks to confirm completion. Before she leaves, she is offered a **contraceptive of her choice** (condoms with pills, injectable or implant), because ovulation can return within 2 weeks. The nurse screens for pressure or violence, mood and school support, and records the case in the CAC register and HMIS without her name outside the clinic.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "Please do not tell my parents." **O:** 17 years, tearful, 9 weeks, positive urine test | **Anxiety** related to unplanned pregnancy and fear of disclosure | **Anxiety self-control:** states fear is lower within 30 minutes | Private room, active listening, explain confidentiality and the law (trust lowers fear and allows informed choice) | Calm, asks questions, signs consent |
| **S:** "I do not know what is allowed." **O:** no knowledge of the Act | **Deficient knowledge** (abortion law, procedure, warning signs) related to no prior information | **Knowledge: health resources:** names the legal limit, the 4 tablets and 3 warning signs | Teach with pictures; teach-back; give a written warning card (clear steps prevent late presentation) | Teach-back correct |
| **O:** drugs to be taken, bleeding expected, Rh group unknown | **Risk for bleeding** related to the abortion process | **Blood loss severity:** pad count under 2 per hour; Hb stable | Check blood group and give anti-D if Rh negative, monitor pads and vitals, ibuprofen not aspirin (early detection of haemorrhage) | Normal vital signs, bleeding settled by day 7 |
| **S:** "It hurts like a bad period." **O:** cramps 6/10 after misoprostol | **Acute pain** related to uterine contractions | **Pain level:** 3/10 or less in 1 hour | Ibuprofen 400 mg, warmth to abdomen, relaxed breathing (reduces prostaglandin pain and distress) | Pain 2/10 at 1 hour |
| **O:** sexually active, no method, ovulation returns in 2 weeks | **Ineffective health self-management** (contraception) related to lack of access | **Knowledge: family planning:** chooses and starts a method before leaving | Offer all methods, give condoms and the chosen method, plan follow-up at 2 weeks (prevents repeat unsafe abortion) | Method started; attends follow-up |
