---
subject: Social and Behavioral Science
grade: BSc Nursing Year 2
unit: 2
title: Family, Marriage, Social Institutions and Social Stratification in Nepal
hours: 14
area: BSN 16 · Social and Behavioral Science · Unit 2
---

Two women in the same district hospital, both 16, both in labour. One is a schoolgirl from a city family who married late; the other is a Dalit bride from a far village, married at 15, who walked for six hours. Their outcomes will differ before the first contraction because **family, marriage, caste, class and gender** decided how much schooling, food, rest and money each had. This unit covers the social institutions that organise life, and the **stratification** that sorts people into unequal positions, and links both to health in Nepal.

::: key What this unit gives you
- Real images: **school girls in Bhaktapur, children carrying bricks in a kiln, a woman carrying firewood, and a marriage rite**, in a 4-up plate with numbered marks; SVG figures on family types, the Lorenz curve and the layers of social determinants.
- **The family**: definition, types, eight functions, change in Nepal (household maths from census 2021), and the **law of marriage** in Nepal with child-marriage figures from NDHS 2022.
- **Social institutions** (family, economy, polity, religion, education, health) and **social change** with Nepal's migration and federalism.
- **Stratification**: caste, class, ethnicity, gender, region; open and closed systems; mobility; Muluki Ain to the 2015 Constitution; **Gini coefficient** computed from quintile shares.
- Eight points on how inequality harms health, eight nursing actions, and a long case on an adolescent Dalit primigravida with Naegele's date, BMI, anaemia and IFA maths.
:::

## 2.1 The family

The **family** is a group of people related by blood, marriage or adoption who usually share a home and responsibility for the care of children and the old. A **household** (the census unit) is the people who live and eat together, whether related or not. The 2021 census counted 6,666,937 households for 29,164,578 people.

```python
pop, households = 29_164_578, 6_666_937
avg = pop / households
print(f"Average household size = {avg:.2f} persons")
print(f"A ward of 250 households holds about {250 * avg:.0f} people")
```

```text
Average household size = 4.37 persons
A ward of 250 households holds about 1094 people
```

The average household has **4.37 persons**, so a ward of 250 households holds about **1094 people**; use this to estimate the number of mothers and children for a health post catchment when no list is at hand.

**Types of family.**

- **By structure:** the **nuclear family** (parents and unmarried children); the **joint family** (several married brothers, their wives and children under one head and one kitchen, common in Nepal); and the **extended family** (nuclear families plus other relatives, such as grandparents, uncles and cousins, not necessarily under one roof).
- **By authority:** **patriarchal** (father/eldest male decides), **matriarchal** (mother decides) and egalitarian. Most Nepali communities are patriarchal and **patrilineal** (descent through the father); several groups (some Janajati, as in parts of Tharu and Newar traditions) give women more voice.
- **By residence:** **patrilocal** (couple lives with the groom's family, the usual pattern), matrilocal and neolocal (own home).
- **By marriage:** **monogamous** (one spouse) and **polygamous** (illegal in Nepal).

```svgfig label="2.1" caption="Family types. Nuclear: two generations in one home. Joint: three generations and several married couples sharing one kitchen and one head. Extended: related nuclear families living near each other and sharing support. Square = male, circle = female. In Nepal, labour migration is turning many joint families into 'nuclear with a distant earner' households."
f = Fig(760, 270)
def person(x, y, male):
    if male: f.box(x - 9, y - 9, 18, 18, "", fill=BLUE, stroke=NAVY, r=2)
    else: f.circle(x, y, 10, fill=ROSE, stroke=RED, label="")
f.box(10, 15, 235, 235, "", fill=SOFT, stroke=NAVY)
f.text(127, 35, "NUCLEAR", size=12, color=NAVY, bold=True)
person(95, 90, True); person(160, 90, False); f.line(105, 90, 150, 90, color=SLATE)
person(95, 170, True); person(160, 170, False); f.line(127, 90, 127, 135, color=SLATE)
f.text(127, 215, "2 generations\nOwn kitchen", size=10.5)
f.box(262, 15, 235, 235, "", fill=SOFT, stroke=TEAL)
f.text(380, 35, "JOINT", size=12, color=TEAL, bold=True)
person(320, 80, True); person(360, 80, False); person(415, 80, True); person(455, 80, False)
person(300, 150, True); person(340, 150, False); person(380, 150, False); person(420, 150, True); person(460, 150, False)
f.text(380, 205, "3 generations, brothers' families\nOne head, one kitchen", size=10.5)
f.box(514, 15, 235, 235, "", fill=SOFT, stroke=AMBER)
f.text(632, 35, "EXTENDED", size=12, color=AMBER, bold=True)
person(560, 100, True); person(595, 100, False); f.box(545, 70, 65, 60, "", fill="none", stroke=AMBER, dash=True)
person(660, 100, True); person(695, 100, False); f.box(645, 70, 65, 60, "", fill="none", stroke=AMBER, dash=True)
person(610, 180, False); f.arrow([(600, 130), (610, 165)], color=SLATE, sw=1.4); f.arrow([(670, 130), (620, 165)], color=SLATE, sw=1.4)
f.text(632, 215, "Related families nearby\nSeparate homes, shared support", size=10.5)
```

**Eight functions of the family** (each is a reason the nurse works with the family, not only the patient).

1. **Reproduction.** The family gives society its new members and sets the rules of marriage and childbirth. It is the unit in which pregnancy and birth are planned. Family planning counselling therefore must include the husband and often the mother-in-law.
2. **Care and protection.** The family feeds, clothes, shelters and nurses its members when they are sick or old. In Nepal most nursing care after discharge is done by relatives. Teaching them wound care, feeding and medicine is part of nursing.
3. **Socialization.** The family teaches language, manners, food habits, gender roles and religion. A child learns hand washing or smoking at home first. Health habits are therefore best changed through families.
4. **Economic function.** The family earns, saves and shares resources, and farms or runs a shop together. Illness of the earner pushes the whole household into debt. Out-of-pocket expenditure for health is a major cause of poverty.
5. **Emotional support.** The family gives love, belonging and security. Supportive families speed recovery and lower depression and suicide risk. Lonely patients, such as the old and the migrants' wives, need more nursing attention.
6. **Status and identity.** The family gives name, caste, ethnicity, religion and inheritance. This gives security but also fixes roles. A nurse should ask how the family sees the patient's role.
7. **Social control.** The family enforces norms by praise and blame. It can prevent risk behaviour, or force harm (child marriage, chhaupadi). Health educators win elders first.
8. **Recreation and religion.** Festivals, rituals and shared meals bind members. Fasting and ritual impurity affect hospital stay. Plan diet and visiting hours with these in mind.

**Change in the Nepali family.** Labour migration (millions abroad, mainly to the Gulf, Malaysia and India) leaves wives, children and elders at home and sends **remittances** that raise consumption and school fees. Urbanisation and education bring more nuclear families, later marriage and smaller size (NDHS 2022 total fertility rate 2.1). The elderly lose family care; women carry double work. These changes create **new needs**: single-parent homes, loneliness, adolescents who lack guidance and elders who need support.

## 2.2 Marriage

**Marriage** is a socially and legally recognised union between two persons that sets rights and duties for them and their children. Forms: **monogamy** (one spouse), **polygyny** (one husband, many wives) and **polyandry** (one wife, many husbands; both are illegal in Nepal today though polyandry persists in a few Himalayan communities); **endogamy** (marry within caste, ethnic or religious group, the norm in Nepal) and **exogamy** (marry outside the clan, required in many groups, such as the same clan or gotra). **Arranged**, **love** and **elopement/capture** marriages all exist, and inter-caste marriage is still a source of conflict and, at times, violence.

**Law in Nepal (as stated in the National Civil Code 2074 and Criminal Code 2074).** The legal minimum age for marriage is **20 years for both sexes**, with consent. Child marriage is a crime; polygamy is a crime; **dowry** is prohibited; marital rape is recognised as an offence; and domestic violence is punishable under the Domestic Violence (Offence and Punishment) Act 2066. Despite this, **NDHS 2022** reports about **34.9% of women aged 20-24 married before age 18** and **5.8% before age 15**, and an adolescent birth rate of **71 per 1,000 girls aged 15-19**. NDHS 2022 also reports that **23% of women aged 15-49** have had physical violence since age 15 and **8%** sexual violence.

```python
women_20_24, pct_before_18 = 250, 34.9        # women aged 20-24 in a catchment; NDHS 2022 share married before 18
girls_15_19, abr = 1_200, 71                   # girls aged 15-19; adolescent births per 1,000 girls
exp_child_brides = women_20_24 * pct_before_18 / 100
exp_births = girls_15_19 * abr / 1000
print(f"Expected child brides among {women_20_24} women aged 20-24: {exp_child_brides:.0f}")
print(f"Expected adolescent births a year among {girls_15_19:,} girls aged 15-19: {exp_births:.0f}")
```

```text
Expected child brides among 250 women aged 20-24: 87
Expected adolescent births a year among 1,200 girls aged 15-19: 85
```

In a catchment with 250 women aged 20-24 we would expect about **87** to have married before 18, and among **1,200** girls aged 15-19 about **85** adolescent births a year. A nurse can plan adolescent-friendly services with such numbers.

**Eight health effects of early marriage and nursing action.**

1. **Obstructed labour and fistula.** The pelvis of a girl under 18 is still growing, so head and pelvis may not fit. Obstructed labour can cause fistula, stillbirth or maternal death. Refer early, use the partograph and promote institutional birth.
2. **Anaemia and malnutrition.** Teens need iron for their own growth and the baby's. Low weight and anaemia raise the risk of preterm and low-birth-weight babies. Give 180 iron-folic acid tablets, deworm, and advise on food.
3. **Pre-eclampsia and eclampsia.** Teen first pregnancies carry more hypertensive disease. Check BP and urine protein at every visit. Teach danger signs: headache, blurred vision, swelling, fits.
4. **Low birth weight and neonatal death.** Babies of teen mothers are smaller and more often die in the first month. Promote early and exclusive breastfeeding, warmth and kangaroo care.
5. **Violence and sexual abuse.** Young brides have less power and are more at risk of partner violence. Provide private screening and link to the One-Stop Crisis Management Centre (OCMC) and police.
6. **Mental health.** Isolation, school drop-out and early motherhood lead to depression and suicide risk. Screen with PHQ-9 and give counselling and support.
7. **Loss of education and income.** The girl leaves school and has fewer chances to earn, which keeps the family poor for the next generation. Encourage school re-entry and skills.
8. **Short birth interval and repeated pregnancy.** Young brides are under pressure to have a child at once and again. Offer adolescent-friendly family planning (implant, pills, condoms, injectable) with privacy, as per the national guideline.

## 2.3 Social institutions and social change

A **social institution** is an organised set of norms and roles that meets a basic need of society. The five main ones: the **family** (reproduction and care), the **economy** (production and distribution; in Nepal many households depend partly on farming and on remittances), **politics and government** (law, power and services; federal, provincial and local governments share health duties after 2015), **religion** (meaning, ritual and moral rules) and **education** (knowledge, skills and social mobility). The **health system** is the institution that cares for illness and promotes health; its roles are doctor, nurse, patient and community.

**Social change** is the alteration of social structure, institutions and culture over time. **Factors:** technology (mobile phones), economy (remittances, markets), education, migration and urbanisation, politics (the 2006 movement, 2008 republic, 2015 federal constitution), ideas and social movements (Dalit, Janajati, women's and Madhesi movements) and war or disaster (the 2015 earthquake). **Theories:** evolutionary (societies pass through stages), cyclical (rise and fall) and conflict (change from struggle). **Cultural lag** (Ogburn): the material part changes first and the non-material part slowly follows.

```photogrid label="2.2" cols="4" ratio="1.0" caption="Family, work and inequality in Nepal. (a) School girls in Bhaktapur after class: education delays marriage. (b) Children carrying bricks in a kiln: poverty and child labour. (c) A woman carrying firewood in a doko: women's unpaid work. (d) The ring-and-henna rite of a marriage: the union that begins a new household. Wikimedia Commons (CC BY and CC BY-SA)."
@ photo id="nur10/schoolgirls" cap="School girls, Bhaktapur"
fit 1.0
focus 0.35 0.5
mark 0.35 0.70 "1"
key 1 (a) Schooling in uniform: each year of school lowers the risk of child marriage
@ photo id="nur10/brick" cap="Children in a brick kiln"
fit 1.0
focus 0.4 0.5
mark 0.23 0.55 "2"
mark 0.71 0.52 "3"
key 2 (b) Child carrying bricks on the head
key 3 (b) A second child: heavy loads damage growing spines and lungs
@ photo id="nur10/firewood" cap="Woman carrying firewood"
fit 1.0
focus 0.55 0.5
mark 0.37 0.50 "4"
key 4 (c) Load carried by head-strap; women's workload and back pain
@ photo id="nur10/marriage" cap="Marriage rite"
fit 1.0
focus 0.5 0.5
mark 0.50 0.40 "5"
key 5 (d) Ring and henna: legal age 20 for both partners
```

## 2.4 Social stratification: caste, class, ethnicity, gender and region

**Social stratification** is the ranking of people into layers, with unequal power, wealth and prestige, that continues across generations. It is **universal** (found in every society), **social** (made by society, not nature), **ancient**, **diverse** in form and **consequential** (it changes life chances, including health and length of life). A **closed system** (caste) fixes position by birth; an **open system** (class) allows movement by effort; **ascribed status** comes at birth, **achieved status** is earned. **Marx** stressed ownership of production (class); **Weber** added **status** (prestige) and **party** (power).

- **Caste.** The *Muluki Ain* of 1854 (Jung Bahadur Rana) wrote a hierarchy into law, with "touchable" and "untouchable" castes. The 1963 Code removed the legal basis; the **Caste-Based Discrimination and Untouchability (Offence and Punishment) Act 2068 (2011)** made discrimination a crime; the **Constitution 2015** (Article 24) bans untouchability. **Dalits** are about 13% of the population and still have the lowest literacy, income and access to services.
- **Class** is position in the economy (income, wealth, education, occupation). NDHS groups households in **wealth quintiles**, and health indicators rise steadily from the poorest to the richest.
- **Ethnicity.** Janajati (indigenous peoples), Madhesi, Muslims and Khas-Arya groups differ in language, land, voice and services. **Gender**: women have less property, schooling and decision power. **Region**: Karnali and Sudurpashchim and remote hills have fewer staff, roads and facilities than Bagmati. Disability and age add more layers.
- **Social mobility** is movement between strata: **vertical** (up or down), **horizontal** (same level), **intergenerational** (child compared with parent) and **intragenerational** (over one's own life). In Nepal, education, migration and remittances, and the nursing profession itself, are the main ladders.

**Measuring inequality: the Lorenz curve and Gini coefficient.** The **Lorenz curve** plots the cumulative share of income (y) against the cumulative share of households ranked poor to rich (x). The diagonal is perfect equality. The **Gini coefficient** is the area between the diagonal and the curve divided by the area under the diagonal (0 equality, 1 one person has all). The **quintile ratio** is the share of the richest 20% divided by that of the poorest 20%. The numbers below are **illustrative teaching data**, not an official Nepal figure.

```python
shares = [6, 10, 15, 22, 47]                 # % of income held by poorest to richest quintile (teaching data)
cum = [0]
for s in shares:
    cum.append(cum[-1] + s / 100)
area_under = sum(0.2 * (cum[i] + cum[i + 1]) / 2 for i in range(5))   # trapezoids
gini = 1 - 2 * area_under
ratio = shares[-1] / shares[0]
print("Cumulative shares:", [round(c, 2) for c in cum])
print(f"Gini coefficient = {gini:.3f}")
print(f"Quintile ratio (top 20% / bottom 20%) = {ratio:.2f}")
```

```text
Cumulative shares: [0, 0.06, 0.16, 0.31, 0.53, 1.0]
Gini coefficient = 0.376
Quintile ratio (top 20% / bottom 20%) = 7.83
```

```svgfig label="2.3" caption="Lorenz curve for the teaching data above. The dashed diagonal is perfect equality. The bowed curve shows that the poorest 60% of households hold only 31% of income. The shaded gap between the diagonal and the curve gives the Gini coefficient of 0.376."
f = Fig(760, 290)
ox, oy, W, H = 70, 250, 250, 220
f.line(ox, oy, ox + W, oy, color=SLATE, sw=1.6); f.line(ox, oy, ox, oy - H, color=SLATE, sw=1.6)
f.line(ox, oy, ox + W, oy - H, color=SLATE, sw=1.3, dash=True)
pts = [(0, 0), (0.2, 0.06), (0.4, 0.16), (0.6, 0.31), (0.8, 0.53), (1, 1)]
xy = [(ox + W * a, oy - H * b) for a, b in pts]
f.poly(xy + [(ox + W, oy - H)], fill="#fde68a", stroke=AMBER, sw=1.2)
for i in range(5):
    f.line(xy[i][0], xy[i][1], xy[i + 1][0], xy[i + 1][1], color=RED, sw=2.6)
for (x, y) in xy:
    f.circle(x, y, 3.5, fill=RED, stroke=RED)
f.text(ox + W / 2, oy + 28, "Cumulative share of households (poor to rich)", size=10.5, color=SLATE)
f.text(ox + 8, oy - H - 10, "Cumulative share of income", size=10.5, color=SLATE, anchor="start")
f.line(ox, oy, ox + W, oy - H, color=NAVY, sw=1.8, dash=True)
f.text(ox + 62, oy - 150, "Line of equality", size=10.5, color=NAVY, bold=True)
f.box(380, 30, 360, 60, "Poorest 60% of households hold\nonly 31% of income", fill=ROSE, stroke=RED, size=11, bold=True)
f.box(380, 105, 360, 60, "Richest 20% hold 47%, which is\n7.83 times the poorest 20%", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(380, 180, 360, 60, "Gini = 1 - 2 x area under curve\n= 0.376", fill=BLUE, stroke=NAVY, size=11, bold=True)
```

The Gini coefficient is **0.376** and the quintile ratio is **7.83**: the richest fifth holds nearly eight times the income of the poorest fifth. In health, the same method gives the **concentration index** of services: a positive value means services favour the rich.

## 2.5 Social determinants of health

The **social determinants of health** are the conditions in which people are born, grow, live, work and age, and the systems that shape them (WHO Commission, 2008). The **Dahlgren-Whitehead** model (Figure 2.4) shows layers from personal factors outward to the broad social, economic and cultural environment.

```svgfig label="2.4" caption="The Dahlgren-Whitehead rainbow as rings. The individual (age, sex, genes) sits at the core. Around it: lifestyle (smoking, diet, activity), social and community networks, living and working conditions (housing, water, education, jobs, health services), and the outer ring of general socioeconomic, cultural and environmental conditions, including caste, gender and policy."
f = Fig(760, 300)
f.circle(200, 150, 140, fill="#f1f5f9", stroke=SLATE, sw=1.6)
f.circle(200, 150, 112, fill=BLUE, stroke=NAVY, sw=1.6)
f.circle(200, 150, 84, fill=MINT, stroke=TEAL, sw=1.6)
f.circle(200, 150, 56, fill=SAND, stroke=AMBER, sw=1.6)
f.circle(200, 150, 28, fill=ROSE, stroke=RED, sw=1.6, label="Person", size=10, color=RED)
f.box(380, 15, 370, 50, "OUTER: socioeconomic, cultural and\nenvironmental conditions (caste, gender, policy)", fill="#f1f5f9", stroke=SLATE, size=10.5, bold=True)
f.box(380, 78, 370, 50, "Living and working conditions: housing,\nwater, education, jobs, health services", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(380, 141, 370, 50, "Social and community networks:\nfamily, FCHV, mothers' group", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(380, 204, 370, 50, "Individual lifestyle: tobacco, alcohol,\nfood, activity", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.text(560, 280, "Change the outer rings and the whole population gains", size=10.5, color=NAVY, bold=True)
```

**Eight ways social inequality harms health in Nepal.**

1. **Poverty.** Poor families cannot buy food, transport or medicines, so stunting, anaemia and TB are common. Out-of-pocket costs push households into debt. Free-care schemes and insurance exist, but the poorest still bear indirect costs.
2. **Low education.** People who cannot read miss instructions, danger signs and immunisation dates. Mothers' schooling is strongly tied to child survival and nutrition. Use pictures and teach-back.
3. **Caste discrimination.** Dalit patients may face rude treatment, late care or segregation in facilities. They may avoid facilities as a result. Equal care is both an ethical and legal duty.
4. **Gender inequality.** Girls eat last, marry early and cannot decide on their own treatment. Women have more anaemia and violence. Empowering women lowers maternal and child deaths.
5. **Geography.** Hill and mountain villages are hours from a hospital, and staff turnover is high. Women deliver at home and die of bleeding. Birthing centres, transport funds and FCHVs reduce this gap.
6. **Occupation and migration.** Brick kiln, construction and farm workers face injuries, pesticide exposure and lung disease; migrants face accidents, HIV and mental stress. Occupational health teaching is part of community nursing.
7. **Social exclusion and stigma.** People with disability, leprosy, HIV or mental illness are often hidden by families. Stigma delays diagnosis and treatment. Counselling and community education reduce it.
8. **Chronic stress.** Constant insecurity raises cortisol, blood pressure and depression, which add to heart disease. Support groups and counselling lower risk. Social support is a protective factor.

**Nursing actions for equity (summary).** Give care by need, not caste, class or gender; use a wealth and exclusion lens in community assessment; go to the unreached with outreach clinics; include women, Dalits, Janajati and disabled people in health committees; teach with pictures and local languages; refer to social protection schemes (senior and single-women allowances, free essential drugs, Aama programme); document exclusion; and advocate to the local government for water, roads and schools.

## Formula and fact sheet

- Family types: nuclear, joint, extended; patriarchal, patrilineal, patrilocal. Average household size = population / households = 29,164,578 / 6,666,937 = 4.37.
- Legal marriage age in Nepal = 20 years for both sexes; NDHS 2022: 34.9% of women 20-24 married before 18; ABR 71 per 1,000.
- Stratification: caste (closed, ascribed), class (open, achieved); mobility vertical, horizontal, inter- and intragenerational.
- Gini = 1 - 2 x area under the Lorenz curve; quintile ratio = top 20% share / bottom 20% share.
- Naegele's rule: EDD = LMP + 7 days - 3 months + 1 year (about LMP + 280 days).

## Chapter summary

- Family is the basic institution (care, socialization, economy); joint families are changing through migration and education.
- Nepal's law sets marriage at 20, yet child marriage persists and harms mother and baby.
- Caste, class, ethnicity, gender and region stratify Nepali society; the Constitution and the 2011 Act forbid discrimination.
- Gini and quintile ratio measure inequality; social determinants (Dahlgren-Whitehead) explain health gaps; nurses promote equity.

## Practice

```python
from datetime import date, timedelta
lmp, visit = date(2025, 3, 10), date(2025, 9, 22)
edd280 = lmp + timedelta(days=280)
n = lmp + timedelta(days=7)
m, y = n.month - 3, n.year + 1
if m <= 0:
    m, y = m + 12, y - 1
naegele = date(y, m, n.day)
days = (visit - lmp).days
w, d = divmod(days, 7)
bmi = 41 / 1.48 ** 2
hb = 9.8
grade = "mild" if hb >= 10 else ("moderate" if hb >= 7 else "severe")
ifa = (edd280 - visit).days
g = [6, 10, 15, 22, 47]
print(f"EDD (LMP + 280 days) = {edd280:%d %b %Y}; Naegele = {naegele:%d %b %Y}")
print(f"Gestation on {visit:%d %b %Y} = {days} days = {w} weeks {d} days")
print(f"BMI = {bmi:.1f}; Hb {hb} g/dL = {grade} anaemia; IFA tablets to term = {ifa}")
print(f"MCQ3 quintile ratio = {g[-1] / g[0]:.1f}; MCQ4 household size = {29_164_578 / 6_666_937:.2f}")
```

```text
EDD (LMP + 280 days) = 15 Dec 2025; Naegele = 17 Dec 2025
Gestation on 22 Sep 2025 = 196 days = 28 weeks 0 days
BMI = 18.7; Hb 9.8 g/dL = moderate anaemia; IFA tablets to term = 84
MCQ3 quintile ratio = 7.8; MCQ4 household size = 4.37
```

**MCQs (with reasons)**

1. A family in which several married brothers live with their wives and children under one head and one kitchen is: (a) nuclear (b) joint (c) extended only (d) matrilocal.
2. The legal minimum age of marriage in Nepal is: (a) 18 for girls, 21 for boys (b) 18 for both (c) 20 for both (d) 22 for both.
3. If the richest 20% hold 47% and the poorest 20% hold 6% of income, the quintile ratio is about: (a) 0.1 (b) 3.5 (c) 7.8 (d) 41.
4. Average household size from 29,164,578 people in 6,666,937 households is about: (a) 2.4 (b) 4.4 (c) 6.4 (d) 8.4.
5. Which statement about caste is correct? (a) It is an open system (b) Discrimination is a crime under the 2011 Act (c) It was created in 1990 (d) It has no health effect.

::: note Answers and rationales
**1. (b).** A joint family has several couples of related men under one authority and one kitchen. A nuclear family has only parents and children, and an extended family does not necessarily share one head or kitchen.
**2. (c).** The Civil Code sets 20 years for both sexes, with consent. Earlier rules of 18 and 16 are obsolete, so options (a), (b) and (d) are wrong.
**3. (c).** The ratio is 47 / 6 = 7.8; 0.1 is the inverse and 41 is the difference. A ratio of 1 would mean equality.
**4. (b).** 29,164,578 / 6,666,937 = 4.37. The options 2.4, 6.4 and 8.4 are not close to the census values.
**5. (b).** The Caste-Based Discrimination and Untouchability Act 2068 (2011) and Article 24 of the 2015 Constitution forbid it. Caste is a closed system, dates from the Muluki Ain of 1854 or earlier, and strongly affects health.
:::

**Short answer (3 marks): List the functions of the family.** The family reproduces society, protects and cares for members, socialises children, provides economic support, gives emotional security, confers status and identity, controls behaviour through norms and carries religion and recreation. In nursing, the family is the main caregiver after discharge, so teaching the family is part of care.

**Medium answer (5 marks): Describe social stratification in Nepal and its effect on health.** Social stratification is the ranking of people into unequal layers by caste, class, ethnicity, gender and region (Figure 2.4). Caste is closed and ascribed; class is open and achieved. The Muluki Ain of 1854 made caste a legal hierarchy; the Constitution 2015 and the 2011 Act forbid discrimination, yet Dalits remain poorest and least educated. Inequality is measured by the Lorenz curve and Gini coefficient (Figure 2.3). Health effects: poverty causes malnutrition and TB; low education means missed danger signs; discrimination delays care; gender inequality causes early marriage and anaemia; remote areas lack staff. Nurses reduce the effect by equal care, outreach, health education and advocacy.

**Long answer (10 marks): Kamala Bishwakarma, 16 years, a Dalit girl married at 15, comes to an antenatal clinic on 22 September 2025. LMP 10 March 2025. Weight 41 kg, height 148 cm, BP 120/76 mmHg, Hb 9.8 g/dL. She walked for six hours, eats last in the family, has no IFA tablets and her husband is in Malaysia. Calculate and write the nursing care plan.**

*Calculations.* EDD by LMP + 280 days is **15 Dec 2025** and by Naegele's rule **17 Dec 2025**. Gestation today is **196 days = 28 weeks 0 days**. BMI = 41 / (1.48 x 1.48) = **18.7 kg/m2** (normal range 18.5-24.9, but at the lower edge; a pregnant teenager who is still growing needs a higher weight gain). Hb 9.8 g/dL is **moderate anaemia** in pregnancy (WHO: mild 10-10.9, moderate 7-9.9, severe below 7). She needs about **84 IFA tablets** to reach term, so the 180-tablet course should be started at once.

*Social analysis.* Her risk comes from age (adolescent pregnancy), caste (Dalit exclusion), gender (eats last, low voice), poverty and distance (six hours' walk). Using the Dahlgren-Whitehead model, the nurse acts on individual factors (iron, food), networks (FCHV, mothers' group, mother-in-law) and the living conditions (transport, birthing centre).

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **O:** Hb 9.8 g/dL, BMI 18.7, "I eat last." | **Imbalanced nutrition: less than body requirements** related to poverty and household food rules, as evidenced by anaemia and low BMI. | **Nutritional status:** Hb 11 g/dL or more by 36 weeks; weight gain 0.4 kg/week. | Give 180 IFA tablets and teach daily use with food (corrects anaemia); deworm after the first trimester (reduces loss); teach dal, green leaves, egg, milk and a meal sequence with family (boosts intake); link with Aama and FCHV (follow-up). | Hb rising; gains weight. |
| **O:** 16 years, 28 weeks, primigravida. | **Risk for ineffective childbearing process** related to adolescent age and anaemia. | **Pregnancy outcome:** birth at a facility at 37-41 weeks with no complication. | Four ANC visits (28, 32, 36, 38 weeks) with BP, urine protein and fetal growth (early detection of pre-eclampsia); plan institutional birth with a birth preparedness card (reduces delay); teach danger signs. | All visits kept; plan made. |
| **S:** "I cannot decide; my mother-in-law does." **O:** quiet, husband abroad. | **Powerlessness** related to young age, low caste and gender status. | **Health beliefs: control:** states one decision she will make; mother-in-law attends teaching. | Private, respectful talk (builds trust); include mother-in-law and teach together (the decision-maker is on board); screen for violence and depression (PHQ-9); refer to OCMC if abuse (safety). | Voices choices; screens negative. |
| **S:** "It takes six hours to walk." | **Ineffective health management** related to distance and cost. | **Access:** has transport and funds ready by 36 weeks. | Explain the Aama transport and delivery incentive and free birthing services; identify the nearest birthing centre and ambulance contact; arrange a waiting stay at 38 weeks if needed (prevents home delivery). | Plan documented; transport ready. |
| **S:** "People say we are not allowed to sit with others." | **Social isolation** related to caste exclusion and migrant husband. | **Social support:** attends the mothers' group; names two support people. | Give equal care and use her name (respect); introduce FCHV and mothers' group (peer support); refer to school re-entry and social protection after birth (long-term change). | Attends group; reports feeling supported. |
