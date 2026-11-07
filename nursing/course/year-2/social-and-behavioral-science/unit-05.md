---
subject: Social and Behavioral Science
grade: BSc Nursing Year 2
unit: 5
title: Social Problems, Deviance and Social Control: Poverty, Unemployment, Migration, Substance Use, Trafficking and Delinquency
hours: 14
area: BSN 16 · Social and Behavioral Science · Unit 5
---

A nurse in a district hospital meets, in one week, a boy of 12 with a burned hand from a brick kiln, a mother whose husband has gone to Malaysia and stopped sending money, a young man vomiting after raksi, and a girl who was offered a "job in Delhi". None of these is only a medical problem. A **social problem** is a condition that a large number of people see as harmful to society and as needing collective action. This unit joins **sociological theory** (Merton, Becker, Sutherland, Durkheim) with the **Nepali facts** on poverty, unemployment, labour migration, substance use, trafficking, child labour and juvenile delinquency, and ends with **social control**, **social work** and **community assessment**.

::: key What this unit gives you
- Real images: **Robert K. Merton** and **Howard S. Becker**, a **Kathmandu riverbank settlement**, women carrying bricks, **children in a brick kiln**, a **foreign-employment agency**, **raksi** brewing and a village meeting; SVG figures on Merton's strain typology, poverty by province, STEPS 2019 bars, the trafficking response pathway, social control and the project cycle.
- **Social problems and deviance**: functionalist, conflict and interactionist views; Merton's five adaptations, labelling, differential association.
- **Poverty and unemployment** with **NLSS-IV 2022/23** figures; headcount, **poverty gap** and unemployment rate worked out step by step.
- **Migration, substance use, trafficking, child labour and delinquency** with Nepal's laws (Foreign Employment Act, Human Trafficking and Transportation (Control) Act 2064, Children's Act 2075).
- **Social control, social work and community assessment**; eight nursing responses to each major problem; a long case on a returned migrant with alcohol use.
:::

## 5.1 Social problems and theories of deviance

A condition becomes a social problem when it is **widespread**, **harmful**, **seen as a problem** and **open to change by group action**. Poverty has existed for centuries, but it is called a problem when society decides it should be reduced. Social problems are **interlinked** (poverty leads to migration, migration to family breakdown, loneliness to alcohol) and are often both **cause and result** of ill health. Three views explain them. The **functionalist** view (Durkheim, Merton) says problems come from **weak social integration or strain** and that society must repair itself. The **conflict** view (Marx) says problems come from **unequal power and resources**, so the poor, women and low-caste groups carry the largest burden. The **interactionist** view (Mead, Becker) says a behaviour becomes "a problem" through **labels and meanings** given by powerful groups.

```photogrid label="5.1" cols="3" ratio="1.0" caption="Theorists and a social problem. (a) Robert K. Merton (1910-2003) in academic dress at Leiden, 1965; his strain theory explains deviance as a gap between goals and means. (b) Howard S. Becker, author of Outsiders (1963) and the labelling approach. (c) A riverbank settlement in Kathmandu: crowded, informal housing with no secure tenure, water or sanitation, which is a daily picture of urban poverty. Wikimedia Commons (CC0, CC BY-SA)."
@ photo id="nur10/merton" cap="Robert K. Merton"
fit 1.0
focus 0.5 0.6
mark 0.50 0.84 "1"
key 1 (a) Merton: anomie and strain
@ photo id="nur10/becker" cap="Howard S. Becker"
fit 1.0
focus 0.5 0.7
mark 0.50 0.38 "2"
key 2 (b) Becker: deviance is a label, not only an act
@ photo id="nur10/slum" cap="Riverbank settlement, Kathmandu"
fit 1.0
focus 0.5 0.5
mark 0.30 0.38 "3"
mark 0.82 0.65 "4"
key 3 (c) Makeshift housing on the bank without services
key 4 (c) The polluted river: water and sanitation risk
```

**Deviance** is behaviour that breaks a group's norms. It is **relative** (it depends on time, place and group), so drinking tea is normal and drinking raksi at a funeral may be too, while the same drinking in a classroom is deviant. **Durkheim** said deviance is normal and even useful (it marks the boundary of morality) and that **anomie**, a state of weak or unclear norms during rapid change, raises suicide and crime. **Merton** (1938) said strain arises when a society sets **cultural goals** (wealth, success, a good job abroad) but gives unequal **legitimate means** (schooling, capital, networks). People adapt in five ways (Figure 5.2).

```svgfig label="5.2" caption="Merton's strain typology. A plus sign means the person accepts the goal or the means; a minus sign means rejects. Examples from Nepal: the student who studies for Loksewa (conformity), the fake recruiting agent (innovation), the clerk who follows every rule and forgets its purpose (ritualism), the person who drops out into alcohol or drugs (retreatism) and the group that tries to replace both goals and means (rebellion)."
f = Fig(760, 350)
f.box(10, 10, 160, 36, "ADAPTATION", fill=NAVY, stroke=NAVY, color="#ffffff", size=11, bold=True)
f.box(176, 10, 90, 36, "GOALS", fill=NAVY, stroke=NAVY, color="#ffffff", size=11, bold=True)
f.box(272, 10, 90, 36, "MEANS", fill=NAVY, stroke=NAVY, color="#ffffff", size=11, bold=True)
f.box(368, 10, 382, 36, "NEPALI EXAMPLE", fill=NAVY, stroke=NAVY, color="#ffffff", size=11, bold=True)
rows = [("CONFORMITY", "+", "+", "Studies hard, prepares for Loksewa", MINT, TEAL),
        ("INNOVATION", "+", "-", "Fake agent sells a 'job abroad'; smuggling", ROSE, RED),
        ("RITUALISM", "-", "+", "Clerk follows every form, forgets the patient", SAND, AMBER),
        ("RETREATISM", "-", "-", "Drops out of school and work into alcohol or drugs", ROSE, RED),
        ("REBELLION", "+/-", "+/-", "Group rejects both and builds new goals", BLUE, NAVY)]
for i, (a, g, m, ex, fl, sk) in enumerate(rows):
    y = 54 + i * 54
    f.box(10, y, 160, 46, a, fill=fl, stroke=sk, size=11, bold=True)
    f.box(176, y, 90, 46, g, fill=SOFT, stroke=sk, size=16, bold=True)
    f.box(272, y, 90, 46, m, fill=SOFT, stroke=sk, size=16, bold=True)
    f.box(368, y, 382, 46, ex, fill=SOFT, stroke=sk, size=10.5)
f.text(380, 337, "Strain = (cultural goals) minus (legitimate means). Most people conform; deviance is a response to blocked means.", size=10, color=NAVY)
```

**Labelling theory** (Lemert, Becker): **primary deviance** is the first rule-breaking act, often hidden and small; **secondary deviance** follows when society **labels** the person ("addict", "thief", "prostitute") and he accepts the label as his identity. A boy caught stealing once, expelled from school and shunned, may become a thief. This is why Nepal's **Children's Act 2075** stresses **diversion**, privacy and reintegration. **Differential association** (Sutherland): crime is **learned** in close groups, in proportion to the balance of favourable and unfavourable definitions of law-breaking. **Biological and psychological views** (Lombroso, XYY, impulsivity) are weak alone; modern models are **biopsychosocial**. Nurses use these ideas to **avoid blame**: they treat the patient, not the label.

## 5.2 Poverty and unemployment

**Absolute poverty** is a lack of the minimum needed for survival, set by a **poverty line**. **Relative poverty** compares a person with the average in the same society. **Multidimensional poverty** counts deprivation in health, education and living standards together. In Nepal, **NLSS-IV (2022/23, National Statistics Office)** put **20.27%** of people below the national line of **NPR 72,908 per person per year**, a fall from **25.16%** in 2010/11. Poverty was **24.66% in rural** and **18.34% in urban** areas, highest in **Sudurpaschim (34.16%)** and lowest in **Gandaki (11.88%)** (Figure 5.3). Nepal's official **Multidimensional Poverty Index** (2021 report, 2019 data) found **17.4%** multidimensionally poor, with children (0-17) at nearly 22%, and nutrition and years of schooling among the biggest deprivations.

```svgfig label="5.3" caption="Poverty headcount by province, NLSS-IV 2022/23 (percent of people below NPR 72,908 per person per year). The dashed line is the national rate of 20.27%. Sudurpaschim, Karnali, Lumbini and Madhesh are above it; Sudurpaschim has nearly three times the rate of Gandaki."
f = Fig(760, 300)
prov = [("Sudurpaschim", 34.16, ROSE, RED), ("Karnali", 26.69, ROSE, RED), ("Lumbini", 24.35, SAND, AMBER), ("Madhesh", 22.53, SAND, AMBER), ("Koshi", 17.19, MINT, TEAL), ("Bagmati", 12.59, MINT, TEAL), ("Gandaki", 11.88, MINT, TEAL)]
for i, (n, v, fl, sk) in enumerate(prov):
    y = 14 + i * 36
    f.text(138, y + 14, n, size=11, color=SLATE, bold=True, anchor="end", vmid=True)
    f.box(146, y, v * 15, 28, f"{v:.2f}%", fill=fl, stroke=sk, size=11, bold=True)
f.line(146 + 20.27 * 15, 6, 146 + 20.27 * 15, 270, color=NAVY, sw=1.8, dash=True)
f.text(146 + 20.27 * 15 + 6, 285, "National 20.27%", size=10.5, color=NAVY, bold=True, anchor="start")
f.line(146, 6, 146, 270, color=SLATE, sw=1.4)
```

**Poverty maths.** The headcount ratio counts the poor; the **poverty gap** measures **how far** they fall below the line (the depth); the squared gap weights the poorest more (the severity). A village of ten households has these annual per-person consumptions (NPR): 40,000; 58,000; 72,908; 90,000; 120,000; 65,000; 30,000; 150,000; 72,000; 100,000.

```python
z = 72908                                              # NLSS-IV national poverty line, NPR per person per year
y = [40000, 58000, 72908, 90000, 120000, 65000, 30000, 150000, 72000, 100000]
poor = [v for v in y if v < z]                         # strictly below the line
gaps = [(z - v) / z for v in poor]
print(f"Line per day = Rs {z / 365:.1f}; family of 5 per year = Rs {z * 5:,}")
print(f"Poor households = {len(poor)} of {len(y)}; headcount P0 = {len(poor) / len(y) * 100:.0f}%")
print(f"Poverty gap P1 = {sum(gaps) / len(y) * 100:.1f}%; mean gap among the poor = {sum(gaps) / len(poor) * 100:.1f}%")
print(f"Severity P2 = {sum(g * g for g in gaps) / len(y) * 100:.1f}%")
```

```text
Line per day = Rs 199.7; family of 5 per year = Rs 364,540
Poor households = 5 of 10; headcount P0 = 50%
Poverty gap P1 = 13.7%; mean gap among the poor = 27.3%
Severity P2 = 6.0%
```

The line is about **Rs 199.7 a day**. Five of ten households are poor (**P0 = 50%**); the poorest fall on average **27.3%** below the line, and the whole village's **gap is 13.7%**. A household at exactly Rs 72,908 is **not** poor, which is why only five are counted.

**Unemployment** is being without work, **available** and **looking** for work. The **unemployment rate = unemployed / labour force x 100**, where labour force = employed + unemployed. **Types:** frictional (between jobs), structural (skills do not match jobs), cyclical (economic slowdown), seasonal (farm and tourism) and **underemployment / disguised** (many people on a small farm, or a graduate working below his skill). **NLSS-IV** found a national rate of **12.6%** (11.4% in 2017/18), and **22.7%** for ages 15-24. If 8,000 people are employed and 1,150 are looking for work, the labour force is **9,150** and the rate is **1,150 / 9,150 = 12.6%**. Many Nepali jobs are informal and farm-based, without leave, insurance or safe conditions, so "employed" does not always mean "secure"; the **Prime Minister Employment Programme** and the **Contributory Social Security Scheme** try to close the gap.

**Eight ways poverty and unemployment harm health, and the nursing response.**

1. **Hunger and undernutrition.** A poor family buys cheaper, less varied food, so children become stunted and anaemic. Nepal's NDHS 2022 still finds a substantial share of children under five stunted. The nurse measures MUAC and growth, teaches local low-cost foods (dal, eggs, green leaves, sattu) and links families to supplementary food and the Child Nutrition Grant where available.
2. **Delayed care-seeking.** The poor wait until illness is severe because of transport cost, lost wages and fear of bills. This turns simple diarrhoea or pneumonia into an emergency. The nurse explains **free essential services**, the **Basic Health Services** package and the Health Insurance Board scheme, and asks about cost barriers at every contact.
3. **Unsafe housing and WASH.** Crowded, damp, smoky homes with open drains cause TB, acute respiratory infection and diarrhoea (Plate 5.1c). The nurse teaches chimney or improved stoves, boiling or chlorinating water, handwashing and refers for housing or ward support.
4. **Mental distress.** Debt, job loss and shame raise depression, alcohol use and suicide. The nurse screens with PHQ-9, listens without judging and uses the **mhGAP** referral route and the national helpline 1166.
5. **Child labour and school drop-out.** Poor families send children to work, which harms growth and learning (Section 5.5). The nurse reports hazardous work, supports school return and links to the Ward Child Protection Committee.
6. **Early marriage and early pregnancy.** Economic pressure pushes girls into early marriage, raising adolescent pregnancy and maternal risk. The nurse gives adolescent-friendly counselling, family planning, and promotes the legal age of marriage (20 years).
7. **Gender and caste layers of poverty.** Women, Dalits, Muslims and remote ethnic groups carry a heavier load of deprivation. The nurse practises **equity**: she gives time, language and respect to the least served, and records caste and ethnicity in HMIS for equity analysis.
8. **Poor adherence to treatment.** Lost wages and transport cost cause missed TB, HIV and diabetes doses. The nurse links patients to DOTS and **treatment supporter** schemes, gives drug supplies for longer intervals when protocols allow, and follows up by phone.

## 5.3 Labour migration and its health effects

**Migration** is a lasting change of residence. **Push factors** (poverty, no jobs, conflict, disaster) and **pull factors** (wages, jobs, family, services) drive it, in the **push-pull** model. Types: **internal** (hills to Terai, village to Kathmandu), **international** (labour to Gulf, Malaysia, India), **seasonal** and **forced**. The **2021 Census** counted **2,190,592 absentees**, or **7.5%** of the population of 29,164,578, mostly men aged 15-44. **Remittances** were about **NPR 1,445 billion (about USD 11 billion) in 2023/24**, roughly a quarter of GDP, and in 2024/25 the state issued **839,266 labour permits**, of which **94,455 (11.3%)** went to women (Department of Foreign Employment). The **Foreign Employment Act 2064** requires a labour permit, an approved agency, **pre-departure orientation**, a medical check at an **authorised centre**, insurance and a **Foreign Employment Welfare Fund** claim for death or injury.

```photogrid label="5.4" cols="3" ratio="1.0" caption="Work, childhood and migration. (a) Women stacking and carrying hand-made bricks near Kathmandu: heavy, informal, low-wage work. (b) Two children carrying bricks on their heads at a brick kiln in Nepal: a worst form of child labour under ILO C182. (c) A visa centre in Kathmandu, one of the many offices where migrant workers register their biometric data before going abroad. Wikimedia Commons (CC BY-SA)."
@ photo id="nur10/bricklayer" cap="Women brick workers"
fit 1.0
focus 0.5 0.5
mark 0.45 0.48 "1"
key 1 (a) Bricks carried and stacked by hand
@ photo id="nur10/kilnchild" cap="Children in a brick kiln"
fit 1.0
focus 0.5 0.5
mark 0.44 0.62 "2"
mark 0.74 0.62 "3"
key 2 (b) Child with a load on the head
key 3 (b) Second child carrying a brick stack: spinal and growth risk
@ photo id="nur10/qvc" cap="Visa centre, Kathmandu"
fit 1.0
focus 0.5 0.5
mark 0.50 0.58 "4"
key 4 (c) Visa centre where migrants give biometric data before departure
```

**Health effects.** Migrant workers face **injury and death** (falls, heat stroke, road accidents, cardiac arrest in young men), **mental illness** (isolation, debt, abuse), **sexual and communicable risks** (HIV, TB, hepatitis), and **debts to recruiters**. **Left-behind families** face loneliness, child neglect, the **"mother alone"** load and sometimes unwise spending; **returnees** meet unemployment, injury, TB or alcohol dependence. A **remittance example**: a worker earning Rs 45,000 a month and sending 70% sends Rs 31,500 a month, or **Rs 378,000 a year**. This is **Rs 13,460** above the poverty line of a family of five (Rs 364,540), so a single migrant income can lift a household out of poverty, but only while the job lasts.

**Eight nursing actions for migrants and their families.**

1. **Ask about migration in every history.** "Does anyone in the family work abroad?" takes ten seconds and opens the door to a hidden problem. Record the country, job, duration and last return. Use this to plan screening and education.
2. **Check the pre-departure health card.** Only authorised medical centres may certify fitness. Teach the worker to keep the report, to ask for the result and to know which conditions (TB, HIV in some countries, hepatitis) can cause refusal and where to seek treatment and counselling.
3. **Teach occupational safety and heat illness.** Gulf workers face temperatures above 45 degrees C. Teach water, shade, rest, salt, and signs of heat stroke (hot dry skin, confusion). Insist on written contracts and on the right to protective equipment.
4. **Offer safe-sex and infection education.** Give condom, STI and HIV information, and TB symptom screening on return. Link to HIV testing and ART centres without stigma. Return visits for TB treatment must continue under DOTS.
5. **Screen for depression, alcohol use and suicide.** Isolation and debt are strong risks. Use PHQ-9 and AUDIT-C, listen, and refer. Teach families that calls and video chats protect mental health.
6. **Support left-behind spouses, children and elders.** Check that the child is attending school and growing; teach safe use of money; link elders to the Senior Citizen Allowance and the ward social security desk. Encourage women's savings groups.
7. **Plan reintegration of returnees.** Examine for injury, TB, hypertension and alcohol use; connect to skill training, the Prime Minister Employment Programme and Remittance-based microfinance. Unemployed returnees are at high risk of relapse.
8. **Know the rights channels.** Workers can complain to the Department of Foreign Employment, Nepali embassy labour desks, the Foreign Employment Board and the NHRC. A nurse who tells a family the correct channel can prevent exploitation and recover compensation.

## 5.4 Substance use: tobacco, alcohol and drugs

**Substance use** is taking a psychoactive substance; **misuse** is use that harms; **dependence** is a strong urge, loss of control, tolerance and withdrawal, continued despite harm. In Nepal the **Tobacco Product (Control and Regulation) Act 2068** controls tobacco (see Unit 4), the **Narcotic Drugs (Control) Act 2033** bans cannabis, opium and heroin, and alcohol is licensed and taxed but **home-brewed raksi, jaad and tongba** are made in many homes. The **STEPS survey 2019** (Nepal Health Research Council, ages 15-69) found **28.9%** current tobacco users (men **48.3%**, women **11.6%**) and **23.9%** current drinkers (men **38.6%**, women **10.8%**); **11.7% of men** drank daily or almost daily, **6.8%** of adults had heavy episodic drinking, and about **68.5%** of current drinkers had taken **unrecorded** (home-brewed or illicit) alcohol in the past week. NDHS 2022 likewise found that about **42% of men** and **11% of women** aged 15-49 had taken alcohol in the previous month.

```photogrid label="5.5" cols="2" ratio="1.0" caption="Alcohol in everyday Nepal. (a) A woman at a traditional fireplace where raksi is distilled from millet or rice in a clay and metal still; the strength is unregulated and varies widely. (b) A village shop selling home-brewed raksi beside packaged goods: alcohol is easy to buy, cheap and near homes. Wikimedia Commons (CC BY-SA)."
@ photo id="nur10/raksibrew" cap="Home distillation of raksi"
fit 1.0
focus 0.5 0.5
mark 0.33 0.78 "1"
mark 0.72 0.30 "2"
key 1 (a) The brewer: production is a home and women's livelihood task
key 2 (a) The still: strength is not controlled or labelled
@ photo id="nur10/raksishop" cap="Village shop selling raksi"
fit 1.0
focus 0.5 0.4
mark 0.45 0.68 "3"
mark 0.82 0.27 "4"
key 3 (b) The seller: raksi is sold with daily goods
key 4 (b) Bottles of locally made spirit at the counter
```

```svgfig label="5.6" caption="Tobacco and alcohol use by sex, Nepal STEPS survey 2019 (adults 15-69 years). Men use both substances about four times as often as women for tobacco and alcohol; a quarter of adults drink and nearly three in ten use tobacco, so both are public-health priorities and common causes of liver disease, cancer, injury and violence."
f = Fig(760, 290)
groups = [("Tobacco (any form)", [("Men", 48.3, ROSE, RED), ("Women", 11.6, SAND, AMBER), ("All", 28.9, BLUE, NAVY)]),
          ("Alcohol (past 12 months)", [("Men", 38.6, ROSE, RED), ("Women", 10.8, SAND, AMBER), ("All", 23.9, BLUE, NAVY)])]
for g, (name, bars) in enumerate(groups):
    for i, (lab, v, fl, sk) in enumerate(bars):
        x = 40 + g * 370 + i * 105
        h = v * 4.2
        f.box(x, 235 - h, 85, h, f"{v:.1f}%", fill=fl, stroke=sk, size=12, bold=True)
        f.text(x + 42, 252, lab, size=11, color=SLATE, bold=True)
    f.text(40 + g * 370 + 150, 275, name, size=12, color=NAVY, bold=True)
f.line(30, 235, 740, 235, color=SLATE, sw=1.4)
f.text(380, 15, "Percent of adults aged 15-69 years", size=11, color=NAVY, bold=True)
```

**Alcohol arithmetic.** A **standard drink** holds **10 g of pure ethanol**. Grams of alcohol = **volume (mL) x strength x 0.789** (density of ethanol). A 60 mL glass of 40% raksi has 60 x 0.40 x 0.789 = **18.9 g**, about **1.9 standard drinks**, and **60 g** (the heavy-episode threshold) is about **190 mL** of such raksi, or three big glasses. Because home-brewed strength is unknown, real intake may be higher.

**Eight nursing actions for substance use.**

1. **Screen everyone, not only "suspects".** Ask about tobacco, alcohol and drugs at admission and at every health-post visit with AUDIT-C or ASSIST. Ask in a calm, private and non-judging way. Early screening finds risky use before dependence.
2. **Give a brief intervention (FRAMES).** Feedback on risk, Responsibility of the person, Advice to cut down or stop, a Menu of options, Empathy and Self-efficacy. Five minutes of advice reduces drinking in risky users. Record the advice and follow up.
3. **Watch for withdrawal and intoxication.** Alcohol withdrawal (tremor, sweating, anxiety, seizures, delirium tremens) begins 6 to 24 hours after the last drink and is dangerous. Monitor vital signs and CIWA-Ar, give thiamine before glucose and use benzodiazepines as ordered (see Psychiatric Nursing, Unit 5). Opioid overdose needs airway care and naloxone.
4. **Treat the whole person.** Check liver, nutrition, injuries, infections (HIV, hepatitis B and C, TB) and mental illness, which often co-occur. Many users have depression or trauma behind the use. A physical examination also builds trust.
5. **Use harm reduction where it exists.** Needle and syringe programmes, methadone or buprenorphine maintenance, and condom promotion reduce HIV and death. These are part of Nepal's national HIV programme and saved many lives. Harm reduction does not promote drugs; it keeps people alive until they are ready to change.
6. **Involve the family and teach them.** Teach that dependence is a health condition, not a moral weakness. Advise how to avoid enabling (covering for the person, giving money), how to stay safe and where help is. Support groups such as Alcoholics Anonymous help families.
7. **Prevent at three levels.** Primary: life-skills education, no sale to minors, taxes and advertising bans. Secondary: screening and brief advice. Tertiary: detoxification, rehabilitation, relapse prevention and vocational support. School health nurses and FCHVs carry primary prevention.
8. **Know the law and rights.** Treat patients with confidentiality and dignity. Know that possession of narcotics is an offence but treatment should be offered, and refer to licensed rehabilitation and the mhGAP route. Never shame or restrain a person without clinical need.

## 5.5 Trafficking, child labour and juvenile delinquency

**Trafficking in persons** has three parts: an **act** (recruiting, moving, harbouring), a **means** (force, deception, abuse of vulnerability) and a **purpose** (exploitation). Nepal's **Human Trafficking and Transportation (Control) Act 2064 (2007)**, section 4, lists **selling or buying a person for any purpose, using a person in prostitution, and removing a human organ** (except for lawful treatment) as trafficking; selling or buying carries **10 to 20 years** of imprisonment and the consent of a **child below 18** is no defence. In **FY 2020/21** the Nepal Police recorded **134 cases with 187 victims**, of whom **80 (42.8%) were under 18**, which is about **1.4 victims per case**. Girls and women, poor and low-caste families, school drop-outs, migrants and earthquake survivors are the most targeted; promises of a "good job in the Gulf" or marriage are common lures, and open borders with India and misuse of **orphanages** are known routes.

```svgfig label="5.7" caption="A nurse's response pathway for a suspected trafficked person: recognise, protect, treat, document, refer and rehabilitate. Rescued persons should be seen privately, never be returned to a suspected trafficker, and be told of their right to confidentiality. National helplines: Nepal Police 100, Child Helpline 1098 and Women helpline 1145."
f = Fig(760, 250)
steps = [("1 RECOGNISE", "Red flags: no ID,\nfear, bruises,\ncontrolled by\nanother person", ROSE, RED), ("2 PROTECT", "Private room,\ninterpreter,\nconsent, safety;\nnot with escort", SAND, AMBER),
         ("3 TREAT", "Injury, STI, HIV\nPEP, pregnancy,\nmental distress,\nnutrition", MINT, TEAL), ("4 DOCUMENT", "Facts in own\nwords; body\nchart; preserve\nevidence", BLUE, NAVY),
         ("5 REFER", "OCMC, police,\nchild helpline,\nshelter, legal aid,\nNGOs", BLUE, NAVY), ("6 REHABILITATE", "Counselling, skills,\nschool, family or\nsafe reintegration", MINT, TEAL)]
for i, (a, b, fl, sk) in enumerate(steps):
    x = 6 + i * 126
    f.box(x, 12, 118, 40, a, fill=fl, stroke=sk, size=10.5, bold=True)
    f.box(x, 62, 118, 100, b, fill=SOFT, stroke=sk, size=10.5)
    if i < 5: f.arrow([(x + 118, 32), (x + 126, 32)], color=SLATE, sw=2)
f.box(6, 182, 748, 52, "NEVER: blame, photograph without consent, share her name,\nor send her home with a companion you suspect.", fill=ROSE, stroke=RED, size=11, bold=True)
```

**Child labour** is work that harms a child's health, schooling or development. The **Nepal Child Labour Report 2021** (ILO and the Central Bureau of Statistics, from NLFS 2017/18) found **1.1 million children, 15.3% of 7,074,756 children aged 5-17**, in child labour, a fall from 1.6 million in 2008; **222,493 (3.1% of all children)** did **hazardous** work, which is about **20.6% of all child labourers**. Child labour is highest among Dalit (19.4%) and Janajati (18.1%) children and in agriculture, brick kilns, carpets, domestic work and quarries. The **Labour Act 2074** sets 14 years as the minimum age of work and bans hazardous work below 18. Heavy loads hurt the spine, brick dust and clay cause lung disease, and long hours cause missed schooling (Plate 5.4b).

**Juvenile delinquency** is law-breaking by a person below 18. **Causes** are a broken or violent home, neglect, poor supervision, peer groups, school failure, poverty, substance use, media and trauma. The **Children's Act 2075** defines a child as under **18**, sets **10 years** as the minimum age of criminal responsibility, gives **reduced, graduated penalties**, uses **child-friendly closed hearings**, diversion and **child correction homes**, and protects the child's **identity**. A crime-rate example: **2,500 offences by children in a population of 1,200,000 children** is **208.3 per 100,000**. Prevention uses parenting support, school life-skills, sports and early help (see Merton and labelling).

**Eight nursing actions on trafficking, child labour and delinquency.**

1. **Know the red flags.** A person with no identity papers, a controlling companion, fear of authority, signs of abuse or an unexplained debt may be trafficked. Do not ask in front of the companion. Make time to see the patient alone, under a sound reason such as "routine examination".
2. **Make safety the first goal.** Offer a private space, an interpreter and reassurance. Explain confidentiality and its limits. Never promise what you cannot do and never send the person away with someone suspicious.
3. **Treat injuries, infections and mental harm.** Give wound care, STI and HIV post-exposure prophylaxis, emergency contraception, tetanus and hepatitis B vaccines, and trauma counselling. Use trauma-informed communication: choice, control and no repeated questioning. Follow OCMC protocol.
4. **Document and preserve evidence.** Record the person's own words, use a body chart and photographs only with consent, and keep clothing in paper bags. Your note may be used in court. Stick to facts, not opinions.
5. **Refer through the proper chain.** Contact the One-stop Crisis Management Centre (OCMC), the Nepal Police Women and Children Service Centre, Child Helpline 1098 and approved NGO shelters such as Maiti Nepal. Use the Ward Child Protection Committee for children. Follow up that the referral was completed.
6. **Find working children and act.** Ask every child about school and work. In hazardous work (kiln, quarry, mine, carrying, domestic work), report to the ward, child protection committee or MoLESS, and help return to school. A child's health card can record work-related injury.
7. **Treat young offenders with respect.** Do not label or shame. Ask about home, school, substances and abuse, and refer for counselling and diversion. Protect identity and give information to parents. Early support reduces secondary deviance.
8. **Prevent at community level.** Teach girls and families about safe migration, the labour permit, the Foreign Employment Board and the danger of "free tickets". Support schools, mothers' groups and FCHVs to spot risk, and join community watch groups.

## 5.6 Social control

**Social control** is the set of methods by which society **encourages conformity** and **discourages deviance**. **Informal control** works through family, peers, religion, caste and village opinion, with praise, gossip, shame and exclusion, and is strongest in small, close communities. **Formal control** works through law, police, courts, schools, professional councils and regulations, with written rules and **sanctions**. **Positive sanctions** reward (awards, promotion, respect), **negative sanctions** punish (fines, jail, loss of licence, expulsion). When change is fast (migration, urbanisation) informal control weakens and **anomie** can rise (Durkheim), so formal control must take over and **both** must fit local culture. In health, the **Nepal Nursing Council Act 2052** controls professional behaviour, the Tobacco Act controls tobacco, the **Public Health Service Act 2075** protects the right to basic health care, and **clinical audit** and **ward rules** are professional controls.

```svgfig label="5.8" caption="Social control. Informal agencies (family, peers, religion, custom) and formal agencies (law, police, courts, schools, councils) apply positive and negative sanctions that push people toward conformity. When both are weak, strain and anomie increase deviance (Merton, Durkheim). Good control combines persuasion and fair rules; harsh control alone can cause rebellion."
f = Fig(760, 290)
f.box(10, 10, 300, 40, "INFORMAL CONTROL (unwritten)", fill=SAND, stroke=AMBER, size=12, bold=True)
f.box(450, 10, 300, 40, "FORMAL CONTROL (written)", fill=BLUE, stroke=NAVY, size=12, bold=True)
f.box(10, 62, 300, 100, "Family, peers, religion, caste\nand village opinion, custom\n\nPraise, respect, gossip, shame,\nexclusion", fill=SOFT, stroke=AMBER, size=11)
f.box(450, 62, 300, 100, "Law, police, courts, schools,\nNursing Council, regulations\n\nAwards, licence, fines, jail,\nsuspension", fill=SOFT, stroke=NAVY, size=11)
f.box(250, 190, 260, 56, "CONFORMITY\n(order and safety)", fill=MINT, stroke=TEAL, size=12, bold=True)
f.arrow([(160, 162), (270, 190)], color=AMBER, sw=2.2); f.arrow([(600, 162), (490, 190)], color=NAVY, sw=2.2)
f.box(330, 70, 100, 80, "Positive and\nnegative\nsanctions", fill=SOFT, stroke=SLATE, size=10.5)
f.arrow([(310, 110), (330, 110)], color=SLATE, sw=1.6); f.arrow([(450, 110), (430, 110)], color=SLATE, sw=1.6)
f.text(380, 270, "Weak informal AND weak formal control = strain, anomie and more deviance", size=10.5, color=RED, bold=True)
```

## 5.7 Applied sociology, social work and community assessment

**Applied sociology** uses sociological knowledge, methods and theory to **solve practical problems** (a health survey, a programme evaluation, a community diagnosis), unlike **pure sociology**, which builds theory. **Social work** is a profession that promotes **social change, problem-solving, empowerment** and wellbeing (IFSW). **Primary methods:** **casework** (one person or family), **group work** and **community organisation**; **secondary methods:** **social action**, **social welfare administration** and **social work research**. **Principles:** acceptance, individualisation, **confidentiality**, **self-determination**, non-judgemental attitude and controlled emotional involvement. In Nepal, NGOs register with the **Social Welfare Council** under the **Social Welfare Act 2049**; hospitals have social service units and OCMCs, and the nurse works with social workers, FCHVs and ward committees. **Medical social work** links patients to money, shelter, legal and family support.

**Community assessment** finds needs before a project starts. Use **participatory rural appraisal (PRA)** tools: **social map** (who lives where), **transect walk**, **seasonal calendar** (food, disease, migration), **wealth ranking**, **Venn diagram** (which institutions matter), **focus groups** and a **household survey**. For a prevalence survey of an unknown proportion, **n = 1.96^2 x p x q / d^2 = 1.96^2 x 0.5 x 0.5 / 0.05^2 = 384.2**, rounded up to **385**; adding 10% for non-response gives 385 / 0.9 = **428 households**. The **project cycle** (Figure 5.9) runs from **needs assessment** to **planning (logical framework)**, **implementation**, **monitoring** (ongoing) and **evaluation** (at the end), and then feeds lessons into the next cycle.

```photogrid label="5.9" cols="2" ratio="1.0" caption="Community decision-making and the project cycle. (a) Two community members in a local meeting in Nepal; community consultation is the starting point of every needs assessment. (b) The project cycle: assess needs, plan, implement, monitor and evaluate, with lessons feeding back. Photo: USAID, public domain."
@ photo id="nur10/meeting" cap="Community meeting, Nepal"
fit 1.0
focus 0.5 0.5
mark 0.25 0.55 "1"
mark 0.72 0.52 "2"
key 1 (a) A community member speaking for the group
key 2 (a) A second participant: every voice and gender should be heard
@ svg cap="The project cycle"
f = Fig(380, 300)
f.box(110, 10, 160, 48, "1 ASSESS NEEDS\n(PRA, survey)", fill=ROSE, stroke=RED, size=12.5, bold=True)
f.box(230, 80, 140, 48, "2 PLAN\n(logframe)", fill=SAND, stroke=AMBER, size=12.5, bold=True)
f.box(230, 150, 140, 48, "3 IMPLEMENT", fill=MINT, stroke=TEAL, size=12.5, bold=True)
f.box(110, 232, 160, 48, "4 MONITOR\n5 EVALUATE", fill=BLUE, stroke=NAVY, size=12.5, bold=True)
f.box(10, 150, 90, 48, "Lessons", fill=SOFT, stroke=SLATE, size=12.5, bold=True)
f.arrow([(250, 58), (290, 80)], color=SLATE, sw=2); f.arrow([(300, 128), (300, 150)], color=SLATE, sw=2); f.arrow([(290, 198), (230, 232)], color=SLATE, sw=2)
f.arrow([(110, 256), (55, 198)], color=SLATE, sw=2); f.arrow([(55, 150), (130, 58)], color=SLATE, sw=2)
```

**Eight roles of the nurse in social problems and community work.**

1. **Look beyond the symptom.** Ask about income, work, housing, family and safety (the social history). A patient with repeated admissions for alcohol or injury needs a social plan as well as treatment. Record the findings in the care plan.
2. **Be a case manager.** Coordinate doctors, social workers, police, NGOs and the family for one patient. Write a clear referral list with names and phone numbers. Follow up so that nobody "falls between the services".
3. **Advocate for the patient.** Speak for those without a voice: the child worker, the trafficked girl, the migrant without papers. Advocacy is a duty in the NNC Code of Ethics. Use official channels and keep confidentiality.
4. **Do community diagnosis with the people.** Use PRA tools and listen to women, Dalits, youth and disabled persons. A needs assessment that hears only the loudest voices misses the poorest. Share the result back to the community.
5. **Build skills and groups.** Support mothers' groups, savings groups, youth clubs and FCHV networks. Group strength reduces isolation and gives peer control. Offer health education and livelihood links.
6. **Use the law and the system.** Know the Children's Act 2075, the Human Trafficking Act 2064, the Foreign Employment Act, the Public Health Service Act 2075 and the Tobacco and Narcotics Acts. Teach families their rights and the correct office. Document so that a case can be taken forward.
7. **Monitor and evaluate your own programme.** Set indicators before starting (for example, percent of working children back in school) and check them at fixed times. Use HMIS and local records. Use the findings to adjust the plan.
8. **Practise ethical and culturally safe care.** Accept without judging, avoid labels such as "addict" or "prostitute", and respect caste, gender and religion. Protect confidentiality and consent. Reflect on your own bias, since it is part of the social problem.

## Formula and fact sheet

- Poverty headcount P0 = poor / population x 100; poverty gap P1 = mean of max(0, (z - y) / z) x 100; severity P2 = mean of squared gaps. Nepal NLSS-IV 2022/23: line NPR 72,908; P0 20.27%.
- Unemployment rate = unemployed / (employed + unemployed) x 100. NLSS-IV: 12.6%; ages 15-24: 22.7%.
- Absentee share = absentees / total population x 100 = 2,190,592 / 29,164,578 = 7.5%.
- Grams of alcohol = mL x strength x 0.789; standard drink = 10 g; heavy episodic drinking = 60 g or more.
- Crime rate = offences / population x 100,000. Sample size n = 1.96^2 x p x q / d^2; inflate by dividing by (1 - non-response).
- Merton: conformity (+,+), innovation (+,-), ritualism (-,+), retreatism (-,-), rebellion (+/-,+/-). Primary deviance (act) leads to secondary deviance (identity) after a label.
- Laws: Human Trafficking and Transportation (Control) Act 2064; Children's Act 2075 (child under 18; no liability under 10); Foreign Employment Act 2064; Labour Act 2074 (minimum age 14); Social Welfare Act 2049; Narcotic Drugs (Control) Act 2033.

## Chapter summary

- A social problem is a widespread, harmful condition that people think society should change; functionalist, conflict and interactionist views explain it differently.
- Merton's strain theory, labelling and differential association explain deviance; nurses avoid labels and treat the person.
- NLSS-IV shows poverty at 20.27% and unemployment at 12.6%; poverty gap and headcount measure breadth and depth.
- Migration (7.5% absent) and remittance bring income and risk; the nurse screens migrants, returnees and left-behind families.
- Alcohol and tobacco are common in Nepal (STEPS 2019); unrecorded alcohol is a major risk; use screening, brief advice and harm reduction.
- Trafficking, child labour and delinquency need recognition, safe care, documentation, referral and prevention under Nepal's laws.
- Social control is informal and formal; social work and community assessment (PRA, project cycle) turn knowledge into action.

## Practice

```python
import math
z = 72908
y = [40000, 58000, 72908, 90000, 120000, 65000, 30000, 150000, 72000, 100000]
poor = [v for v in y if v < z]
p0 = len(poor) / len(y) * 100
p1 = sum((z - v) / z for v in poor) / len(y) * 100
rate = 1150 / (8000 + 1150) * 100
absent = 2190592 / 29164578 * 100
glass = 60 * 0.40 * 0.789
cl = 0.153 * 7074756
hazard = 222493 / 7074756 * 100
traf = 80 / 187 * 100
crime = 2500 / 1200000 * 100000
n = 1.96 ** 2 * 0.5 * 0.5 / 0.05 ** 2
income = 700 * 20
per_person = income * 12 / 5
print(f"MCQ2 unemployment = {rate:.1f}%; MCQ3 P0 = {p0:.0f}%, P1 = {p1:.1f}%; MCQ4 glass = {glass:.1f} g")
print(f"Absent = {absent:.1f}%; child labour = {cl:,.0f}; hazardous = {hazard:.1f}%; minors among trafficked = {traf:.1f}%")
print(f"Crime rate = {crime:.1f} per 100,000; sample n = {n:.1f} -> {math.ceil(n)}; with 10% non-response = {math.ceil(math.ceil(n) / 0.9)}")
print(f"Case: income Rs {income:,} a month = Rs {income * 12:,} a year; per person Rs {per_person:,.0f} = {per_person / z * 100:.1f}% of the line")
print(f"Case: gap per person Rs {z - per_person:,.0f}; household gap Rs {(z - per_person) * 5:,.0f} a year")
grams = 3 * 60 * 0.40 * 0.789
spend = 300 * 30
print(f"Case: alcohol {grams:.1f} g = {grams / 10:.1f} standard drinks a day; spends Rs {spend:,} a month = {spend / income * 100:.1f}% of income; Rs {300 * 365:,} a year")
```

```text
MCQ2 unemployment = 12.6%; MCQ3 P0 = 50%, P1 = 13.7%; MCQ4 glass = 18.9 g
Absent = 7.5%; child labour = 1,082,438; hazardous = 3.1%; minors among trafficked = 42.8%
Crime rate = 208.3 per 100,000; sample n = 384.2 -> 385; with 10% non-response = 428
Case: income Rs 14,000 a month = Rs 168,000 a year; per person Rs 33,600 = 46.1% of the line
Case: gap per person Rs 39,308; household gap Rs 196,540 a year
Case: alcohol 56.8 g = 5.7 standard drinks a day; spends Rs 9,000 a month = 64.3% of income; Rs 109,500 a year
```

**MCQs (with reasons)**

1. A person who accepts the goal of wealth but uses illegal means, such as a fake recruiting agent, shows Merton's: (a) conformity (b) innovation (c) ritualism (d) retreatism.
2. If 8,000 people are employed and 1,150 are unemployed and seeking work, the unemployment rate is about: (a) 11.5% (b) 12.6% (c) 14.4% (d) 87.4%.
3. In a village of ten households, five fall below the poverty line with an average gap of 27.3% of the line. The poverty gap index (P1) for the village is: (a) 13.7% (b) 27.3% (c) 50% (d) 6.0%.
4. The alcohol in one 60 mL glass of 40% raksi is about: (a) 9.5 g (b) 12 g (c) 18.9 g (d) 24 g.
5. Under the Children's Act 2075 a child below which age has no criminal liability? (a) 8 years (b) 10 years (c) 14 years (d) 16 years.

::: note Answers and rationales
**1. (b).** Innovation keeps the cultural goal (money) but rejects legitimate means (honest work). Conformity accepts both, ritualism keeps the means but forgets the goal, and retreatism rejects both.
**2. (b).** Labour force = 8,000 + 1,150 = 9,150, so the rate is 1,150 / 9,150 x 100 = 12.6%. Dividing by the employed only (14.4%) or giving the employed share (87.4%) answers a different question.
**3. (a).** P1 is the average gap over all households: 27.3% x 5 / 10 = 13.7%. The value 27.3% is the mean gap among the poor only, and 50% is the headcount.
**4. (c).** 60 x 0.40 x 0.789 = 18.9 g, about 1.9 standard drinks of 10 g. The other values ignore the density factor or the strength.
**5. (b).** Children under 10 cannot be held criminally responsible; between 10 and 18 graduated, child-friendly justice applies. Ages 14 and 16 are band limits for penalties, not the minimum age.
:::

**Short answer (3 marks): Differentiate primary and secondary deviance.** Primary deviance is the first, often small rule-breaking act (a boy steals a pencil). It is usually hidden and does not change the person's identity. Secondary deviance follows when society labels the person (a "thief") and he accepts the label and acts accordingly, as in Becker's and Lemert's labelling theory. The nurse avoids labels and uses diversion and support to stop secondary deviance.

**Medium answer (5 marks): Explain Merton's strain theory with Nepali examples.** Merton (1938) said strain arises when society sets cultural goals, such as wealth and a good job, but gives unequal legitimate means, such as schooling, capital and contacts. People adapt in five ways (Figure 5.2). **Conformity** accepts goals and means (a student preparing for Loksewa). **Innovation** accepts the goal but uses illegal means (a fake agent selling "jobs abroad", smuggling). **Ritualism** follows the rules but forgets the goal (a clerk who follows every form and ignores the patient). **Retreatism** rejects both and withdraws into alcohol or drugs. **Rebellion** rejects both and builds new goals and means (a revolutionary group). Most people conform. The theory explains why deviance is high where opportunity is blocked: among poor, unemployed youth and migrants in debt. Prevention means widening legitimate means through education, jobs, credit and fair access, along with firm laws.

**Medium answer (5 marks): Describe the nurse's response to a suspected trafficked girl.** Follow the six steps of Figure 5.7. First **recognise** the red flags: no papers, a controlling companion, bruises, fear and a story that does not fit. Second **protect**: see her alone in a private room, with an interpreter, and explain confidentiality. Third **treat**: wounds, STI and HIV post-exposure prophylaxis, emergency contraception, tetanus and hepatitis B vaccines, and psychological first aid with trauma-informed communication. Fourth **document** her own words, a body chart and evidence with consent. Fifth **refer** to the OCMC, the Nepal Police (100), Child Helpline 1098 or Women helpline 1145, and an approved shelter such as Maiti Nepal. Sixth **support rehabilitation** with counselling, schooling, skills and safe family or community reintegration. The nurse never blames, never shares identity and never sends her home with a suspect companion. Under the Human Trafficking Act 2064 the consent of a child under 18 is no defence.

**Long answer (10 marks): Mr Ram Bahadur Tamang, 34 years, returned from Malaysia after a contract ended and has been unemployed for four months. He now works as a daily-wage labourer, earns Rs 700 a day for 20 days a month and supports a family of five. He drinks three 60 mL glasses of 40% raksi daily at Rs 100 a glass and was brought to the health post with tremor, anxiety and poor sleep after a day without drink. He says, "I came back with debt and no job. Drink is the only thing that calms me." Using the unit: (a) explain the sociology, (b) calculate his household position and alcohol intake, and (c) write the nursing care plan.**

*Sociological analysis.* Mr Tamang's problem is a chain: **push-pull migration** (poverty and unemployment pushed him out), **strain** (the goal of a good income for his family without secure means, so he took a foreign job and debt), a failed contract, and **retreatism** into alcohol after unemployment. Home-brewed raksi is cheap and easy to buy (Plate 5.5), and informal social control is weak after migration. He faces **secondary deviance** if the village labels him a "drunkard". Nepal's STEPS 2019 shows that 11.7% of men drink daily or almost daily, so he is not alone.

*Calculations.* Monthly income = 700 x 20 = **Rs 14,000**, or **Rs 168,000** a year. Per person = 168,000 / 5 = **Rs 33,600**, only **46.1%** of the poverty line of Rs 72,908, so the household is **poor**. The gap per person is **Rs 39,308** and for the household **Rs 196,540** a year. Alcohol per day = 3 x 60 x 0.40 x 0.789 = **56.8 g**, which is **5.7 standard drinks**, just under the 60 g heavy-episode mark but clearly hazardous when taken every day. Spending = 3 x 100 = Rs 300 a day = **Rs 9,000 a month, or 64.3%** of his income, and **Rs 109,500** a year. Cutting spending on drink would raise the family's per-person consumption more than any other single change.

*Nursing priorities.* Safety first: monitor vital signs, give **CIWA-Ar** scoring, thiamine before glucose, fluids and benzodiazepine as ordered, and watch for seizures and delirium tremens in the next 48 hours. Then assess depression and suicide risk (PHQ-9), screen for TB and HIV (as a returned migrant), and give brief advice (FRAMES). Link to counselling, to alcohol treatment, to a skills course and to the Prime Minister Employment Programme, and involve his wife through family teaching.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "Drink is the only thing that calms me." **O:** 56.8 g alcohol a day, tremor, anxiety, 1 day without drink. | **Risk for acute substance withdrawal syndrome** related to daily heavy alcohol use. | **Substance withdrawal severity:** CIWA-Ar below 8 and no seizure within 72 hours. | Monitor vital signs and CIWA-Ar every 4 hours (detects worsening early); give thiamine then glucose and benzodiazepine as ordered (prevents Wernicke damage and seizures); keep a quiet, safe room (reduces stimulation). | CIWA-Ar below 8; no seizure. |
| **S:** "I came back with debt and no job." **O:** unemployed 4 months, income Rs 14,000. | **Ineffective coping** related to unemployment, debt and migration failure. | **Coping:** names two non-alcohol coping methods and one support person within 2 weeks. | Use active listening and PHQ-9 (identifies depression and suicide risk); teach problem-solving, breathing and exercise (replaces drinking); refer to counselling and a peer group (social support). | Uses two methods; attends group. |
| **O:** per-person Rs 33,600 (46.1% of line); Rs 9,000 a month on alcohol. | **Ineffective health management / risk-prone health behaviour** related to alcohol dependence and low income. | **Health-seeking behaviour:** agrees to a treatment plan and reduces monthly spending on alcohol by half within 1 month. | Give brief intervention (FRAMES) and show his Rs 109,500 yearly cost (personal motivation); set a written goal (commitment); link to a de-addiction service (specialist care). | Treatment started; spending halved. |
| **S:** "My wife is afraid." **O:** family of five depends on him. | **Compromised family coping** related to a member's alcohol use and poverty. | **Family coping:** wife names two safe actions and one support service in 2 weeks. | Teach the family about dependence and about avoiding enabling (reduces conflict); link to the ward social security desk and women's group (income and peer support); offer family counselling. | Wife states actions; contact made. |
| **O:** returned migrant; chronic cough not yet assessed. | **Risk for infection** related to migration exposure and alcohol-related low immunity. | **Infection status:** TB and HIV screening done and results recorded within 1 week. | Screen for cough over 2 weeks, test sputum and offer HIV counselling (early detection); give nutrition advice (immunity); link to DOTS or ART if positive (treatment adherence). | Screening done; results recorded. |
