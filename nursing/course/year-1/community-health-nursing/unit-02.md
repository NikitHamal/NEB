---
subject: Community Health Nursing
grade: BSc Nursing Year 1
unit: 2
title: Epidemiology and Biostatistics
hours: 25
area: BSN 6-7 · Community Health Nursing · Unit 2
---

Epidemiology is the basic science of public health: the study of how disease is distributed in populations and why. Every HMIS indicator, every outbreak report and every research paper that a nurse reads is built on its measures. In 1854 John Snow used a map of cholera deaths to trace an epidemic in London to one water pump, and the same logic is used today when Nepal's Epidemiology and Disease Control Division investigates dengue, cholera or measles clusters.

::: key What this unit gives you
- A real copy of John Snow's cholera map with marked clusters, paired with the epidemiological triad.
- Incidence, prevalence, IMR, NMR, MMR, relative risk, odds ratio, attributable risk, sensitivity, specificity, PPV and NPV, all computed in an executed block.
- Mean, SD, standard error, confidence interval, t-test, chi-square and sample size, with worked numbers.
- Eight steps of an outbreak investigation and model answers, including a screening-camp case with a care plan.
:::

## 2.1 Epidemiology: concepts, triad and natural history

**Epidemiology** is the study of the distribution and determinants of health-related states in specified populations and the application of that study to control health problems. It answers *who, where, when* (descriptive epidemiology: person, place, time) and *why, how* (analytical epidemiology). Its main uses are to describe the health of a community, to find causes, to plan and evaluate services, and to predict future needs.

The **epidemiological triad** says that disease results from an **agent** (germ, chemical, nutrient lack), a susceptible **host** (age, immunity, behaviour) and a favourable **environment** (water, crowding, climate), joined by a **vector or vehicle** for transmission. Breaking any side of the triangle prevents disease. Terms the nurse must know: **endemic** (usual level in a place, such as malaria in the Terai), **epidemic** (clearly above the usual level), **pandemic** (worldwide), **sporadic** (scattered cases), **outbreak** (small localised epidemic), **zoonosis** (animal to man, such as rabies) and **incubation period** (infection to first symptom).

```photogrid label="2.1" cols="2" ratio="1.0" caption="Descriptive epidemiology. (a) The original map by Dr John Snow (1854): each black bar is a household with deaths from cholera, and the cluster is centred on the Broad Street pump. (b) The epidemiological triad: the disease is prevented by changing agent, host or environment."
@ photo id="nur3/snow" cap="John Snow's cholera map, London 1854"
fit 1.0
focus 0.5 0.5
mark 0.42 0.48 "1"
mark 0.30 0.30 "2"
key 1 (a) The Broad Street pump: deaths cluster round it, so the water is the source
key 2 (a) Black bars are deaths per house; few bars far from the pump show the pattern in place
@ svg cap="Epidemiological triad"
f = Fig(300, 300)
f.poly([(150, 30), (40, 220), (260, 220)], fill=BLUE, stroke=NAVY, sw=2)
f.box(98, 22, 104, 30, "AGENT", fill=ROSE, stroke=RED, size=11, bold=True)
f.box(14, 215, 104, 30, "HOST", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(182, 215, 104, 30, "ENVIRONMENT", fill=MINT, stroke=TEAL, size=10, bold=True)
f.text(150, 140, "Disease", size=13, color=NAVY, bold=True)
f.text(150, 160, "(cholera)", size=10.5, color=SLATE)
f.text(150, 275, "Vibrio cholerae > unsafe water > susceptible child", size=9.5, color=SLATE, bold=True)
```

## 2.2 Measures of disease frequency and mortality

**Incidence** counts new cases in a period among those at risk; **prevalence** counts all existing cases at a point or period. Prevalence = incidence × mean duration, so a lifelong disease such as diabetes has a high prevalence even when the incidence is low. **Rates** have a denominator of the population at risk, **ratios** compare two unrelated numbers, and **proportions** have the numerator inside the denominator.

The vital indicators of Nepal are the **neonatal mortality rate** (NMR, deaths under 28 days per 1000 live births), the **infant mortality rate** (IMR, deaths under 1 year per 1000 live births), the **under-5 mortality rate** and the **maternal mortality ratio** (MMR, maternal deaths per 100,000 live births). NDHS 2022 gave NMR 21, IMR 28 and under-5 mortality 33 per 1000 live births, and the 2021 national maternal mortality study gave an MMR of 151 per 100,000. Neonatal deaths make three-quarters of infant deaths, so newborn care is the priority.

```python
# a district of 20,000 people in one year
pop = 20000
incidence = 150 / pop * 1000          # 150 new cases
prevalence = 300 / pop * 1000         # 300 existing cases at mid-year
live = 8400                           # live births in a larger district
imr = 235 / live * 1000
nmr = 168 / live * 1000
mmr = 13 / live * 100000
print(f"Incidence = {incidence:.1f} per 1000 per year")
print(f"Prevalence = {prevalence:.1f} per 1000")
print(f"IMR = {imr:.1f}, NMR = {nmr:.1f} per 1000 live births")
print(f"MMR = {mmr:.1f} per 100,000 live births")
# cohort: 150/1000 smokers vs 100/2000 non-smokers developed TB
risk_e, risk_u = 150 / 1000, 100 / 2000
print(f"RR = {risk_e / risk_u:.1f}")
print(f"Attributable risk = {risk_e - risk_u:.2f}")
print(f"Attributable risk % = {(risk_e - risk_u) / risk_e * 100:.1f}")
# case-control: exposed cases 60, unexposed cases 40, exposed controls 30, unexposed controls 70
print(f"OR = {(60 * 70) / (40 * 30):.1f}")
```

```text
Incidence = 7.5 per 1000 per year
Prevalence = 15.0 per 1000
IMR = 28.0, NMR = 20.0 per 1000 live births
MMR = 154.8 per 100,000 live births
RR = 3.0
Attributable risk = 0.10
Attributable risk % = 66.7
OR = 3.5
```

The district has an incidence of **7.5 per 1000 a year** and a prevalence of **15.0 per 1000**. From 8,400 live births and 235 infant deaths the IMR is **28.0**, from 168 neonatal deaths the NMR is **20.0**, and 13 maternal deaths give an MMR of **154.8** per 100,000.

## 2.3 Study designs, risk and screening tests

A **cohort study** follows exposed and unexposed people forward to compare disease; it gives **incidence** and the **relative risk (RR)** = risk in the exposed ÷ risk in the unexposed. A **case-control study** starts with cases and controls and looks back at exposure; it gives the **odds ratio (OR)** = (a × d) ÷ (b × c) and suits rare diseases. A **cross-sectional survey** gives prevalence at one time, and a **randomised controlled trial** is the strongest test of an intervention. In the block above, smokers had a TB risk of 15% against 5% in non-smokers, so **RR = 3.0**, the **attributable risk** is **0.10** (the excess due to smoking) and **66.7%** of the TB in smokers is due to smoking. The case-control table gives an **OR of 3.5**. RR or OR above 1 means a risk factor, below 1 means protection, and 1 means no association.

```svgfig label="2.1" caption="The 2 x 2 table for a screening test. Sensitivity and specificity belong to the test; the predictive values change with how common the disease is in the people tested."
f = Fig(760, 250)
f.box(190, 20, 130, 30, "Disease present", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(330, 20, 130, 30, "Disease absent", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(20, 60, 160, 60, "Test positive", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(20, 130, 160, 60, "Test negative", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(190, 60, 130, 60, "TP = 90\nTrue positive", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(330, 60, 130, 60, "FP = 180\nFalse positive", fill=SOFT, stroke=SLATE, size=11)
f.box(190, 130, 130, 60, "FN = 10\nFalse negative", fill=SOFT, stroke=SLATE, size=11)
f.box(330, 130, 130, 60, "TN = 720\nTrue negative", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.text(620, 70, "Sensitivity = TP / (TP + FN)", size=11, color=NAVY, bold=True)
f.text(620, 98, "Specificity = TN / (TN + FP)", size=11, color=NAVY, bold=True)
f.text(620, 126, "PPV = TP / (TP + FP)", size=11, color=TEAL, bold=True)
f.text(620, 154, "NPV = TN / (TN + FN)", size=11, color=TEAL, bold=True)
f.text(380, 226, "Example: 1000 people tested, 10% have the disease", size=10.5, color=SLATE, bold=True)
```

**Screening** is the search for unrecognised disease in apparently healthy people with a quick test. Sensitivity is the ability to find the diseased (few false negatives) and specificity is the ability to clear the healthy (few false positives). For 1000 people with a 10% prevalence, a test with 90% sensitivity and 80% specificity gives 90 true positives, 10 false negatives, 720 true negatives and 180 false positives. The **PPV is 33.3%** (only one in three positives is truly ill), the **NPV is 98.6%** and the accuracy is **81%**. A positive screen is therefore always followed by a confirmatory test.

## 2.4 Biostatistics: describing, comparing and sampling

Data are described by the **mean** (average), **median** (middle value) and **mode** (most frequent), and the spread by the **standard deviation (SD)**: SD = √[Σ(x − mean)² ÷ (n − 1)]. In a normal distribution 68% of values lie within 1 SD, 95% within 2 SD and 99.7% within 3 SD of the mean. The **standard error** SE = SD ÷ √n shows how precisely a sample mean estimates the population mean, and the **95% confidence interval (CI)** is mean ± t × SE. A **p-value** below 0.05 means that a result this large would happen less than 1 time in 20 by chance alone.

Tests are chosen by the data. The **t-test** compares two means (small samples, numerical data); **ANOVA** compares three or more means; the **chi-square test** compares proportions in categories, with χ² = N(ad − bc)² ÷ [(a+b)(c+d)(a+c)(b+d)] for a 2 × 2 table (df = 1, critical value 3.84 at p = 0.05). The **sample size** for a survey of a proportion is n = Z²pq ÷ d²; with no prior estimate p = 0.5, Z = 1.96 and an error d of 5%.

```python
import math
hb = [10.2, 11.5, 9.8, 12.1, 10.9, 10.8, 9.5, 12.4]      # haemoglobin, g/dL, 8 women
n = len(hb); mean = sum(hb) / n
sd = math.sqrt(sum((x - mean) ** 2 for x in hb) / (n - 1))
se = sd / math.sqrt(n); t7 = 2.365                        # t for 7 df at 95%
print(f"Mean = {mean:.1f}, SD = {sd:.2f}, SE = {se:.2f}")
print(f"95% CI = {mean - t7 * se:.1f} to {mean + t7 * se:.1f} g/dL")
# chi-square: vaccinated 10 ill / 190 well; unvaccinated 40 ill / 160 well
a, b, c, d = 10, 190, 40, 160
chi = (a + b + c + d) * (a * d - b * c) ** 2 / ((a + b) * (c + d) * (a + c) * (b + d))
print(f"Chi-square = {chi:.2f} (critical 3.84, df 1)")
# two-sample t-test: group A 11.2 +/- 1.1, group B 9.9 +/- 1.3, n = 10 each
sp = math.sqrt((9 * 1.1 ** 2 + 9 * 1.3 ** 2) / 18)
t = (11.2 - 9.9) / (sp * math.sqrt(1 / 10 + 1 / 10))
print(f"Pooled SD = {sp:.3f}, t = {t:.2f} (critical 2.101, df 18)")
nss = 1.96 ** 2 * 0.5 * 0.5 / 0.05 ** 2
print(f"Sample size = {math.ceil(nss)}; with 10% non-response = {math.ceil(math.ceil(nss) / 0.9)}")
```

```text
Mean = 10.9, SD = 1.05, SE = 0.37
95% CI = 10.0 to 11.8 g/dL
Chi-square = 20.57 (critical 3.84, df 1)
Pooled SD = 1.204, t = 2.41 (critical 2.101, df 18)
Sample size = 385; with 10% non-response = 428
```

The eight women have a mean haemoglobin of **10.9 g/dL**, an SD of **1.05** and an SE of **0.37**, so the 95% CI is **10.0 to 11.8 g/dL**. The chi-square of **20.57** is far above 3.84, so ill-health and vaccination are associated (p < 0.05). The t-test with a pooled SD of **1.204** gives **t = 2.41**, above the critical 2.101 for 18 degrees of freedom, so the two groups differ significantly. The survey needs **385** people, or **428** after adding for 10% non-response.

## 2.5 Investigating an outbreak: eight steps

When two or more people from one place fall ill with the same illness, the nurse reports to the district public health office the same day, and then helps with these eight steps.

1. **Confirm that an outbreak exists.** Compare the number of cases with the usual number for that place and season. Check the diagnosis with a laboratory test where possible. Many "outbreaks" are only better reporting.
2. **Verify the diagnosis.** Examine some patients and collect samples (stool, blood, throat swab) before antibiotics are given. Send them in the right medium and cold box to the laboratory. A case definition cannot be written without a firm diagnosis.
3. **Define a case and count cases.** Write a simple case definition by person, place and time, such as "any person in ward 4 with 3 or more loose stools in 24 hours since 1 Shrawan". Search houses, schools and health posts for more cases. Make a line list with name, age, sex, address, onset date and outcome.
4. **Describe by time, place and person.** Draw an epidemic curve (cases by day), a spot map of houses, and tables by age and sex. A single sharp peak suggests a common source; a series of peaks suggests person-to-person spread. This is exactly how Snow's map worked.
5. **Form a hypothesis.** Ask what the sick share that the well do not, such as the same tap, festival feast or school. State the likely agent, source and way of spread. Test it against the facts rather than assuming it.
6. **Test the hypothesis.** Use a cohort or case-control comparison and calculate the attack rate or odds ratio for each exposure. The exposure with the highest RR or OR and a significant chi-square is the suspect. Environmental samples confirm it.
7. **Control and prevent.** Act at once on the likely source: chlorinate the water, isolate cases, vaccinate contacts, give ORS and treat patients, and spread messages through FCHVs and radio. Do not wait for the final proof before acting. Protect health workers with proper precautions.
8. **Report and follow up.** Write a clear report with findings and recommendations for the district and DHIS2. Keep surveillance until two incubation periods pass with no new case. Share the lesson with the community so it can protect itself next time.

## Formula and fact sheet

- Incidence = new cases ÷ population at risk × 1000; prevalence = all cases ÷ population × 1000; prevalence ≈ incidence × duration.
- IMR = infant deaths ÷ live births × 1000; NMR (under 28 days) ÷ live births × 1000; MMR = maternal deaths ÷ live births × 100,000. NDHS 2022: NMR 21, IMR 28, under-5 33.
- RR = risk exposed ÷ risk unexposed; AR = risk exposed − risk unexposed; OR = ad ÷ bc. RR 3.0, AR 0.10, OR 3.5 in the examples.
- Sensitivity = TP ÷ (TP+FN); specificity = TN ÷ (TN+FP); PPV = TP ÷ (TP+FP); NPV = TN ÷ (TN+FN).
- SE = SD ÷ √n; 95% CI = mean ± t × SE; χ² critical 3.84 (df 1); n = 1.96² × pq ÷ d².

## Chapter summary

- Epidemiology describes (person, place, time) and explains (cohort, case-control, trial) the distribution of disease.
- Incidence counts new cases, prevalence all cases; NMR, IMR and MMR are the main Nepal indicators.
- RR, AR and OR measure the strength of an association; sensitivity and specificity measure a test; PPV depends on prevalence.
- Mean, SD, SE, CI, t-test, chi-square and sample size are the working tools of nursing research.
- An outbreak is handled in eight steps, from confirming it to reporting.

## Practice

**MCQs (with reasons)**

1. A study that starts with people who have the disease and looks back at exposure is: (a) cohort (b) case-control (c) cross-sectional (d) trial.
2. Of 1000 smokers 150 and of 2000 non-smokers 100 developed TB. The relative risk is: (a) 1.5 (b) 2.0 (c) 3.0 (d) 5.0.
3. A test has 90 true positives, 10 false negatives. Its sensitivity is: (a) 10% (b) 80% (c) 90% (d) 99%.
4. If the disease becomes rarer, the PPV of a screening test will: (a) rise (b) fall (c) stay the same (d) equal the specificity.
5. The minimum sample size for a proportion with p = 0.5 and error 5% is: (a) 96 (b) 196 (c) 385 (d) 1,000.

::: note Answers and rationales
**1. (b).** A case-control study works backwards from the outcome; a cohort starts from exposure and follows forward.
**2. (c).** Risk in smokers is 150 ÷ 1000 = 0.15 and in non-smokers 100 ÷ 2000 = 0.05, so RR = 0.15 ÷ 0.05 = 3.0.
**3. (c).** Sensitivity = 90 ÷ (90 + 10) = 90%; 10% is the false negative rate and 80% is the specificity in the example.
**4. (b).** With fewer diseased people, a larger share of positives are false positives, so the PPV falls while sensitivity and specificity stay fixed.
**5. (c).** n = 1.96² × 0.5 × 0.5 ÷ 0.05² = 384.2, rounded up to 385.
:::

**Short answer (3 marks): Incidence and prevalence.** Incidence is the number of new cases in a defined population during a period, for example 150 new cases among 20,000 people in a year is 7.5 per 1000. Prevalence is all existing cases at a time, for example 300 per 20,000 is 15 per 1000. Prevalence depends on incidence and the duration of disease, so a chronic disease has high prevalence. Incidence measures risk, and prevalence measures burden.

**Medium answer (5 marks): Discuss the sensitivity, specificity and predictive values of a screening test (Figure 2.1).** A screening test separates people into positive and negative. **Sensitivity** (TP ÷ (TP + FN)) is the proportion of the diseased who test positive; a sensitive test is chosen to rule out disease. **Specificity** (TN ÷ (TN + FP)) is the proportion of the healthy who test negative; a specific test is chosen to confirm disease. In the table of 1000 people with 10% disease, 90 TP, 10 FN, 720 TN and 180 FP give sensitivity 90% and specificity 80%. The **PPV** (TP ÷ (TP + FP)) is 33.3% and the **NPV** is 98.6%; both depend on prevalence, so the PPV rises in high-risk groups. Every positive screen needs a confirmatory test, and the programme should be acceptable, cheap and followed by treatment.

**Long answer (10 marks): At a ward screening camp under the PEN programme, 1000 adults were tested with a finger-prick glucose strip, and 270 tested positive. Of the 100 people later found to have diabetes, 90 had tested positive. Evaluate the test and plan the nurse's response.**

*Evaluation.* The 270 positives contain 90 true positives, so there are **180 false positives**; the 10 diabetics who tested negative are the false negatives, leaving 730 negatives of whom 720 are truly healthy. **Sensitivity = 90 ÷ 100 = 90%**, **specificity = 720 ÷ 900 = 80%**, **PPV = 90 ÷ 270 = 33.3%**, **NPV = 720 ÷ 730 = 98.6%** and accuracy = 810 ÷ 1000 = **81%**. The test is good at excluding disease (NPV 98.6%) but two of three positives are false, so every positive needs a fasting plasma glucose before any label or drug. The 10 missed cases show that a negative result is not a lifelong guarantee, so repeat testing every 1-3 years is advised for those with risk factors.

*Response.* Give clear results with privacy, send all 270 for confirmation to the health post or PHCC, enrol confirmed cases in the PEN register with monthly follow-up, and teach diet, activity, foot care and stopping tobacco. For the 180 false positives teach healthy lifestyle and re-screen yearly. Report the numbers through HMIS.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "I feel fine, why do I need another test?" **O:** screen positive, random glucose high, BMI 29. | **Deficient knowledge** about diabetes and the confirmatory test related to unfamiliarity with screening, as evidenced by questions and reluctance. | **Knowledge: disease process:** the person explains why confirmation is needed and attends within 1 week. | 1. Explain a screen is not a diagnosis; *reduces fear and false belief.* 2. Arrange fasting glucose at the health post; *confirms the diagnosis.* 3. Give a written appointment and a follow-up call by the FCHV; *improves attendance.* | Attendance checked at 1 week; goal met when confirmation is done. |
| **O:** 90 confirmed cases, 40% with BMI above 25, tobacco use common. | **Risk-prone health behaviour** related to low awareness of risk, as evidenced by inactivity and diet high in rice and fat. | **Health promoting behaviour:** 50% of cases walk 30 minutes a day within 3 months. | 1. Teach plate model, less rice and oil, more saag and dal; *reduces glucose load.* 2. Group walking club in the ward; *social support helps habits.* 3. Brief tobacco cessation advice; *cuts cardiovascular risk.* | Review weight, BP and glucose monthly. |
| **O:** no PEN register in the ward. | **Ineffective health self-management** (community) related to lack of follow-up system. | **Treatment behaviour:** all 90 cases on the register with monthly visits for 6 months. | 1. Start a PEN register and recall list; *prevents loss to follow-up.* 2. Monthly BP, weight and glucose check by the nurse; *detects complications early.* | Register audit at 6 months. |

::: tip Exam tip
Always draw the 2 × 2 table before calculating, write the formula beside each answer, and state in one sentence what the value means (for example "two of three positives are false positives").
:::
