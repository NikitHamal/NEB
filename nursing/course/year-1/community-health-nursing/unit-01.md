---
subject: Community Health Nursing
grade: BSc Nursing Year 1
unit: 1
title: Community Health, Primary Health Care and the Nepal Health System
hours: 20
area: BSN 6-7 · Community Health Nursing · Unit 1
---

A community health nurse works where people live: in the home, the ward office, the school, the health post and the mothers' group. The patient is not one person but a population, so the nurse counts, plans and prevents instead of only treating. In Nepal this work sits inside a federal health system that the 2015 Constitution made a right (basic health care free to every citizen), run by the Ministry of Health and Population (MoHP), the seven provinces and 753 local governments, and carried to the doorstep by about 51,000 Female Community Health Volunteers (FCHVs).

::: key What this unit gives you
- Real photographs of a Nepal health post, a blood-pressure check and an FCHV group session, with labelled marks.
- Community health, the levels of prevention, the Alma-Ata principles and the eight elements of Primary Health Care (PHC).
- The Nepal health system pyramid, HMIS and DHIS2, and community diagnosis with population estimates, a 30-cluster sample and coverage gaps, all worked step by step.
- Eight points on the elements of PHC as the nurse delivers them, and model answers with a full community care plan.
:::

## 1.1 Community health nursing and the levels of prevention

**Community health nursing** is the practice of nursing and public health to promote and protect the health of a population, with continuing (not episodic) care, the family as the unit of service and the community as the client. Its pillars are health promotion, disease prevention, care of the sick at home and referral. A **community** is a group of people who share a place, interests or a social structure (a ward, a Dalit settlement, a school); **health** is, by the WHO, complete physical, mental and social well-being and not merely absence of disease. The nurse works through the **determinants of health**: income, education, water and sanitation, food, housing, social inclusion, gender, and access to services.

Prevention is taught at four levels. **Primordial** prevention stops risk factors from arising at all (tobacco-control law, clean cooking fuel policy). **Primary** prevention stops disease in the healthy (immunisation, handwashing, iodised salt). **Secondary** prevention finds disease early and treats it (blood-pressure and diabetes screening under the Package of Essential Non-communicable Disease interventions, PEN; sputum testing of coughers). **Tertiary** prevention limits disability and rehabilitates (foot care in diabetes, physiotherapy after stroke).

```svgfig label="1.1" caption="Levels of prevention with a Nepal example at each level. The earlier the level, the more people it protects for each rupee spent."
f = Fig(760, 210)
L = [("Primordial", "No risk factor yet\nTobacco law,\nclean fuel policy", SAND, AMBER), ("Primary", "Healthy person\nVaccine, ORS,\nhandwashing, iodine", MINT, TEAL), ("Secondary", "Early disease\nBP and sugar screen,\nsputum test, Pap smear", BLUE, NAVY), ("Tertiary", "Established disease\nFoot care, stroke\nrehabilitation", ROSE, RED)]
for i, (t_, d_, fc, sc) in enumerate(L):
    x = 10 + i * 187
    f.box(x, 20, 165, 34, t_, fill=fc, stroke=sc, size=12, bold=True)
    f.box(x, 62, 165, 78, d_, fill=SOFT, stroke=sc, size=10.5)
    if i < 3: f.arrow([(x + 165, 37), (x + 187, 37)], color=SLATE, sw=2)
f.text(380, 168, "Stage of natural history:  no risk  >  risk  >  early disease  >  disability", size=10.5, color=SLATE, bold=True)
f.text(380, 192, "Health promotion runs across all four levels", size=10.5, color=TEAL, bold=True)
```

## 1.2 Primary Health Care: Alma-Ata to Astana

The 1978 **Alma-Ata Declaration** set the goal of "Health for All" through PHC: essential health care that is practical, scientifically sound, socially acceptable, universally accessible, at a cost the country can afford, and delivered close to where people live. Its principles are **equity** (distribution of care by need), **community participation**, **intersectoral coordination** (health, water, agriculture, education working together), **appropriate technology** and **emphasis on prevention and promotion**. The 2018 **Astana Declaration** renewed the promise with three parts: primary care and essential public health functions, multisectoral policy, and empowered people and communities. Nepal adopted PHC in the 1978 national plan, created the FCHV programme in 1988 and today delivers it as the **Basic Health Service (BHS) package**, free at the local level under the Public Health Service Act 2075 (2018).

```photogrid label="1.1" cols="3" ratio="1.0" caption="Primary health care in Nepal. (a) The drug distributor desk of a health post in Pokhara: the first point of contact. (b) A blood-pressure check of a mother with her child on her lap, by a health worker. (c) An FCHV with a flip chart teaching a mothers' group about regular antenatal check-ups (USAID Nepal)."
@ photo id="nur3/hpost" cap="Health post drug desk, Pokhara"
fit 1.0
focus 0.6 0.5
mark 0.62 0.72 "1"
mark 0.45 0.52 "2"
key 1 (a) Boxes of essential medicines kept at the health post (the essential drugs element of PHC)
key 2 (a) The free drug distributor desk: medicines are handed out with counselling
@ photo id="nur3/hpcheck" cap="Blood-pressure check at the health post"
fit 1.0
focus 0.5 0.5
mark 0.60 0.50 "3"
mark 0.42 0.25 "4"
key 3 (b) Cuff on the mother's arm: screening for hypertension is secondary prevention
key 4 (b) The child on her lap is seen at the same visit (family as the unit of care)
@ photo id="nur3/fchv" cap="FCHV with flip chart, Salyan"
fit 1.0
focus 0.6 0.5
mark 0.77 0.45 "5"
mark 0.25 0.28 "6"
key 5 (c) The FCHV holds the flip chart used in health education
key 6 (c) The mothers' group: community participation in practice
```

```svgfig label="1.2" caption="The Nepal health system as a pyramid. Care is delivered at the bottom, so most problems are solved close to home; each level refers upward and receives feedback."
f = Fig(760, 300)
f.box(250, 10, 260, 40, "Federal: MoHP, national and\nsuper-speciality hospitals", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(190, 62, 380, 40, "Province: Ministry of Social Development / Health,\nprovincial and teaching hospitals (Teku, Bir, TUTH, BPKIHS)", fill=SAND, stroke=AMBER, size=10, bold=True)
f.box(120, 114, 520, 40, "District / local level: hospitals, Primary Health Care Centres,\n753 local governments run the health service", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.box(50, 166, 660, 40, "Health posts and Urban Health Clinics (BHS package), outreach and immunisation clinics", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(10, 218, 740, 40, "Ward and community: about 51,000 FCHVs, mothers' groups, ward health committees, family", fill=SOFT, stroke=SLATE, size=10.5, bold=True)
f.text(380, 282, "Data flow: register > monthly HMIS report > DHIS2 > planning (reverse arrow: supervision, supplies, feedback)", size=10, color=TEAL, bold=True)
f.arrow([(745, 255), (745, 20)], color=RED, sw=2, label="referral", lpos=(722, 140))
```

## 1.3 HMIS, DHIS2 and community diagnosis

Every health post keeps registers (OPD, ANC, delivery, immunisation, FCHV) and sends a monthly report to the **Health Management Information System (HMIS)**, which is entered into **DHIS2** at the municipality. Indicators such as the percentage of pregnant women with four ANC visits, institutional delivery, DPT-HepB-Hib 3 coverage and the dropout rate guide the annual plan. A nurse who cannot read these numbers cannot find the gaps.

**Community diagnosis** (community needs assessment) is the process by which the nurse describes the community's health, finds its problems, ranks them and plans action. Its steps are: define the community, collect data (census, HMIS, survey, key informants, ward walk), analyse, **prioritise** (size of the problem, seriousness, preventability, community concern, resources), plan with the community, act and evaluate. Population-based targets are estimated from crude rates. In a municipality of 42,000 people and 9 wards with 27 FCHVs, the nurse works out:

```python
pop, wards, fchv = 42000, 9, 27
births = pop * 20 / 1000            # crude birth rate 20 per 1000
pregnancies = births * 1.1          # 10% added for abortions and stillbirths
under5 = pop * 0.10
wra = pop * 0.24                    # women 15-49 years
print(f"Expected births per year   = {births:.0f}")
print(f"Expected pregnancies       = {pregnancies:.0f}")
print(f"Children under 5 years     = {under5:,.0f}")
print(f"Women of reproductive age  = {wra:,.0f}")
print(f"Population per ward        = {pop / wards:.0f}")
print(f"Population per FCHV        = {pop / fchv:.0f}")
print(f"30-cluster sampling interval = {pop / 30:,.0f}; children surveyed = {30 * 7}")
```

```text
Expected births per year   = 840
Expected pregnancies       = 924
Children under 5 years     = 4,200
Women of reproductive age  = 10,080
Population per ward        = 4667
Population per FCHV        = 1556
30-cluster sampling interval = 1,400; children surveyed = 210
```

The estimate gives 840 births and 924 pregnancies a year, 4,200 children under five and 10,080 women aged 15-49. Each ward has about 4667 people and each FCHV serves about 1556. For a coverage survey such as the immunisation survey the nurse uses the WHO **30-cluster method**: list the wards with cumulative population, divide the total by 30 to get the **sampling interval of 1,400**, pick a random start, choose each cluster where the interval falls (probability proportional to size) and survey 7 children in each cluster, which is **210 children**. If the HMIS shows 616 women with four ANC visits out of 924 expected, the coverage is **66.7%**; if 588 of 840 births were attended by skilled staff, the coverage is **70.0%** and the gap is **252 births** a year. Gaps become the priorities.

## 1.4 The eight elements of Primary Health Care: eight points

The Alma-Ata declaration listed eight essential elements. The nurse delivers each of them in Nepal in the following ways.

1. **Health education.** Teaching people to prevent and control their own health problems is the base of PHC. The nurse uses flip charts, mothers' group meetings, school clubs and radio. A message works best when it is short, local and repeated, such as "wash hands with soap after the toilet".
2. **Food supply and proper nutrition.** This means balanced diet, exclusive breastfeeding for 6 months, growth monitoring and vitamin A and iron-folic acid supply. The nurse promotes local foods such as dal, green leafy vegetables, eggs and millet (kodo). Under-five children who are stunted or wasted are found with weight and MUAC checks and referred for treatment.
3. **Safe water and basic sanitation.** Clean water, toilets and waste disposal prevent diarrhoea, typhoid and worms. The nurse teaches household water treatment, safe storage and the use of toilets. Nepal declared itself open-defecation free in 2019, and the aim now is to keep every toilet in use.
4. **Maternal and child health including family planning.** Antenatal care, clean delivery, postnatal visits, newborn care, growth monitoring and spacing of births belong here. The Safe Motherhood programme gives incentives for ANC visits and institutional delivery. The nurse tracks every pregnant woman in the ward until 42 days after birth.
5. **Immunisation against the major infectious diseases.** The National Immunization Programme gives free vaccines at birth and in infancy. The nurse keeps the cold chain, runs clinics, traces defaulters and gives the mother the card. Fully immunised coverage in NDHS 2022 was 80% of children aged 12-23 months, so one child in five still needs to be reached.
6. **Prevention and control of locally endemic diseases.** In Nepal these are tuberculosis, malaria in the Terai, kala-azar, dengue, scrub typhus and leprosy. The nurse finds cases, ensures complete treatment (DOTS for TB) and teaches vector control. Reporting an unusual cluster to the district office quickly can stop an outbreak.
7. **Appropriate treatment of common diseases and injuries.** The health post treats cough, diarrhoea, fever, wounds, burns and minor injuries with standard protocols such as IMNCI. The nurse gives first aid, treats what she can, and refers danger signs without delay. Early referral of a bleeding mother or a child who cannot drink saves lives.
8. **Provision of essential drugs.** A short list of safe, effective and cheap medicines must be available at all times. The nurse manages stock with the logistics management information system, checks expiry dates and teaches the patient how to take the drug. Stock-outs of ORS, zinc or oxytocin are a failure of the system, not of the patient.

## Formula and fact sheet

- Levels of prevention: primordial (no risk yet), primary (healthy), secondary (early disease), tertiary (disability). Health promotion runs through all.
- PHC principles: equity, community participation, intersectoral coordination, appropriate technology, prevention first. Eight elements: education, nutrition, water and sanitation, MCH and FP, immunisation, endemic disease control, treatment of common illness, essential drugs.
- Expected births = population × CBR ÷ 1000; expected pregnancies = births × 1.1; coverage = achieved ÷ expected × 100.
- 30-cluster survey: interval = population ÷ 30; 7 children per cluster = 210 children.
- Nepal: 7 provinces, 753 local governments, about 51,000 FCHVs (programme since 1988), PHC adopted in 1978, Public Health Service Act 2075, HMIS reported through DHIS2.

## Chapter summary

- Community health nursing treats the community as the client and works through prevention at four levels.
- PHC (Alma-Ata 1978, Astana 2018) rests on equity, participation, intersectoral action, appropriate technology and prevention.
- Nepal delivers the BHS package through a federal pyramid from the ward and FCHV to the federal ministry, and reports through HMIS and DHIS2.
- Community diagnosis uses estimates, surveys and priority ranking; coverage gaps decide the plan.

## Practice

**MCQs (with reasons)**

1. Tobacco-control legislation is an example of: (a) primordial prevention (b) primary prevention (c) secondary prevention (d) tertiary prevention.
2. Which is NOT one of the eight elements of PHC? (a) Essential drugs (b) Health education (c) Organ transplantation (d) Safe water and sanitation.
3. In a municipality of 42,000 people with a crude birth rate of 20 per 1000, the expected number of births is: (a) 420 (b) 840 (c) 924 (d) 4,200.
4. In the 30-cluster survey, the sampling interval for a population of 42,000 is: (a) 210 (b) 840 (c) 1,400 (d) 4,200.
5. The Nepal FCHV programme began in: (a) 1978 (b) 1988 (c) 2008 (d) 2018.

::: note Answers and rationales
**1. (a).** The law acts before any risk factor takes hold in the population, which is primordial prevention; vaccination (primary) and screening (secondary) act later.
**2. (c).** Transplantation is tertiary hospital care; the other three are elements named at Alma-Ata.
**3. (b).** 42,000 × 20 ÷ 1000 = 840; option (c) is pregnancies (840 × 1.1) and (d) is children under five.
**4. (c).** 42,000 ÷ 30 = 1,400; 210 is the number of children surveyed (30 × 7).
**5. (b).** The programme started in 1988 after the 1978 PHC commitment; Astana was in 2018.
:::

**Short answer (3 marks): Levels of prevention.** Prevention has four levels. Primordial prevention prevents risk factors from appearing (tobacco law). Primary prevention protects the healthy (immunisation, handwashing, iodised salt). Secondary prevention detects disease early (BP and diabetes screening under PEN, sputum test for TB). Tertiary prevention limits disability and rehabilitates (foot care, stroke physiotherapy).

**Medium answer (5 marks): Describe the principles and eight elements of Primary Health Care with reference to Nepal (Figure 1.2).** PHC was declared at Alma-Ata in 1978 as essential, acceptable, accessible and affordable care close to the people. Its principles are **equity**, **community participation**, **intersectoral coordination**, **appropriate technology** and **emphasis on prevention**. The eight elements are health education; food and nutrition; safe water and sanitation; maternal and child health with family planning; immunisation; control of local endemic diseases; treatment of common diseases and injuries; and essential drugs. In Nepal the elements are delivered through the Basic Health Service package at about 51,000 FCHVs, health posts, primary health care centres and hospitals, which form the pyramid in Figure 1.2. Services are free at the local level, supplies and supervision flow down, referrals flow up, and HMIS with DHIS2 records the results for planning. The nurse's role is to deliver, supervise, teach and report.

**Long answer (10 marks): Nurse Sunita Rai, posted to a health post of a hill rural municipality (population 42,000, 9 wards, 27 FCHVs), finds that 616 of 924 expected pregnant women had four ANC visits, only 588 of 840 expected births were attended by skilled staff, and nutritional problems are common. Plan a community diagnosis and a PHC response.**

*Estimate and gap.* The expected births are 42,000 × 20 ÷ 1000 = **840** and pregnancies **924**; four-visit ANC coverage is 616 ÷ 924 = **66.7%** and skilled birth coverage is 588 ÷ 840 = **70.0%**, leaving **252 births** a year without a skilled attendant. Each FCHV serves about 1556 people, so the load is heavy. A 30-cluster survey (interval 1,400, 210 children) will measure immunisation and nutrition.

*Steps.* (1) Define the community and make a ward map showing the health post, FCHVs, roads and hazards. (2) Collect HMIS data, interview ward leaders, mothers' groups and FCHVs, and do a household survey. (3) Analyse by ward to find the worst. (4) Rank the problems by size, seriousness, preventability and community concern; low skilled-birth coverage ranks first because it drives maternal and newborn deaths. (5) Plan with the ward health committee: a birthing centre with a skilled birth attendant, transport through a community fund, FCHV home visits to every pregnant woman, ANC reminder cards and the Aama programme incentives. (6) Implement: train FCHVs, hold mothers' group meetings, set up outreach clinics in distant wards. (7) Evaluate with HMIS each month: the target is four-visit ANC above 80% and skilled birth coverage above 85% in one year.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **O:** ANC 4 visits 66.7%, skilled births 70.0%, 252 births unattended a year; 2 wards more than 3 hours from the birthing centre. | **Deficient community health** (risk of maternal and newborn deaths) related to limited access to skilled birth care and transport, as evidenced by low ANC and delivery coverage. | **Community health status:** four-visit ANC 80% and skilled births 85% within 12 months. | 1. Community diagnosis and ward-wise HMIS analysis; *puts effort where the gap is largest.* 2. FCHV home visits and a pregnancy register in each ward; *every woman is traced.* 3. Community emergency transport fund and Aama incentives; *removes the cost and distance barrier.* 4. Mothers' group education with flip charts; *builds demand and trust.* | HMIS review each month; goal met when targets are reached for two quarters. |
| **S:** mothers say "the health post is far and delivery at home is our custom." **O:** home delivery common in 2 wards. | **Ineffective health self-management** (community) related to cultural preference and low knowledge of danger signs. | **Health beliefs:** 90% of women name three danger signs by 6 months. | 1. Teach danger signs (bleeding, fits, fever, no movement); *prompt referral saves lives.* 2. Involve mothers-in-law and husbands; *the decision makers are reached.* 3. Show a clean birthing centre; *builds acceptance.* | Spot-check knowledge in mothers' groups quarterly. |
| **O:** 27 FCHVs for 42,000 people; stock-outs of iron and zinc recorded. | **Ineffective community coping** related to overstretched volunteers and supply gaps. | **Resource availability:** no stock-out of iron, zinc or ORS for 3 months. | 1. Monthly FCHV meeting for refreshers and supplies; *keeps skills and stock current.* 2. Use the logistics system with a reorder level; *prevents stock-outs.* 3. Recognise FCHVs at ward events; *sustains motivation.* | Stock cards checked monthly. |

::: tip Exam tip
In a community-diagnosis question, always give the steps in order (define, collect, analyse, prioritise, plan, implement, evaluate), show one calculated coverage figure, and name the Nepal tools (HMIS, DHIS2, FCHV, BHS package).
:::
