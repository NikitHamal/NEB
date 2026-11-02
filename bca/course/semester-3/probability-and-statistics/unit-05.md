---
subject: Probability and Statistics
grade: BCA Semester 3
unit: 5
title: Sample Survey
hours: 6
area: BCA 205 · Probability and Statistics · Unit 5
---

Measuring every unit of a population is usually too slow or too costly (or impossible: testing a battery to destruction). A **sample survey** studies a part and generalises to the whole. This unit covers the concepts and the practical organisation of a survey; Unit 6 covers the sampling designs and estimation.

::: key What this unit gives you
- Population, sample, sampling frame; census versus sample survey; the need for sampling.
- Organising a survey: planning, questionnaire design, pilot, field work.
- Selecting a sample and **determining the sample size** (with a worked formula).
- Sampling and non-sampling errors.
:::

## 5.1 Population and sample; census versus sample survey

The **target population** is all units about which we want information; the **sampling frame** is the list from which the sample is drawn (a voters' list, a student register), which should cover the population without omissions or duplicates; a **sampling unit** is the element or group selected; a **sample** is the selected part; **sample size** n and **population size** N give the **sampling fraction** f = n/N. A **census** (complete enumeration) studies every unit; a **sample survey** studies some.

| | Census | Sample survey |
|---|---|---|
| Cost and time | high | much lower |
| Coverage | all units | part |
| Accuracy | no sampling error; non-sampling errors may be large | has sampling error, but careful work can reduce others |
| Suitable when | small populations, or a complete list is needed | large populations, destructive testing, speed matters |

**Needs of sampling:** economy, speed, feasibility when testing destroys the unit (bulbs, crash tests), better quality of fieldwork with fewer, better-trained enumerators, and accuracy that is often high enough. **Limitations:** sampling error; needs expertise in design; not usable when every unit's information is needed (a census of voters for elections).

## 5.2 Organising a sample survey

1. **Define objectives** precisely: what, who, where, when. 2. **Define the population and frame.** 3. **Decide the data to collect** and the method (interview, mail, phone, web). 4. **Design the questionnaire** (below). 5. **Choose the sampling design and size.** 6. **Pilot survey** on a small group to test questions and procedure. 7. **Train the field staff and supervise.** 8. **Collect data and follow up non-response.** 9. **Edit, code, enter and check** the data. 10. **Analyse and report** with limitations stated.

### Questionnaire design

Keep it short and relevant; use **clear, simple, unambiguous** words; ask one thing per question (avoid "double-barrelled" questions); avoid **leading** questions ("Don't you agree that…") and sensitive questions early; provide exhaustive, mutually exclusive options; begin with easy questions and order logically; use **closed** questions (fixed options, easy to analyse) and some **open** ones (richer but hard to code); use Likert scales (strongly disagree … strongly agree) for opinions; add clear instructions and a thank-you; **pilot-test**.

## 5.3 Sample selection and determining the sample size

**Probability (random) sampling** gives every unit a known non-zero chance of selection, which allows valid error estimates: simple random, stratified, systematic, cluster, multistage (Unit 6). **Non-probability sampling** (convenience, judgement, quota, snowball) is cheaper but cannot give valid sampling-error estimates and may be biased.

**Sample size** depends on the **required precision** (margin of error e), the **confidence level** (z), the **variability** of the data, and the **population size**. To estimate a **proportion** within ±e: **n₀ = z² p(1 − p)/e²**, taking p = 0.5 (the worst case, which maximises p(1 − p) = 0.25) when unknown. For a **mean**: n₀ = z² σ²/e². For a finite population of size N apply the **finite population correction**: **n = n₀/(1 + (n₀ − 1)/N)**.

::: example Worked example
A college wants the percentage of students who use the library, within ±5 points at 95% confidence (z = 1.96), p unknown. n₀ = 1.96² × 0.25/0.05² = 0.9604/0.0025 = **384.16 → 385**. The college has N = 2,000 students: n = 384.16/(1 + 383.16/2000) = **322.4 → 323**. Tightening the margin to ±3 points needs 1.96² × 0.25/0.03² = **1,067.11 → 1,068** (before the correction): precision is expensive because n grows with 1/e², so halving the error quadruples the sample. Increasing the confidence to 99% (z = 2.576) enlarges n by (2.576/1.96)² = 1.73 times.
:::

## 5.4 Sampling and non-sampling errors

**Sampling error** is the difference between a sample estimate and the true population value that arises because only part of the population is observed. It is random, can be **measured** (standard error), and **decreases as n increases** (roughly ∝ 1/√n); a census has none.

**Non-sampling errors** can occur even in a census and do **not** decrease with larger samples; they are often the larger problem:

| Source | Examples | Remedy |
|---|---|---|
| **Frame errors** | out-of-date or incomplete list | update and check the frame |
| **Non-response** | people not at home or refuse | callbacks, incentives, weighting, substitute carefully |
| **Response/measurement errors** | misunderstanding, memory, lying, interviewer effect | clear questions, trained interviewers, validation |
| **Processing errors** | coding, data-entry, tabulation mistakes | double entry, range checks |
| **Selection bias** | non-random choice | use probability sampling |

**Bias** is a systematic error pushing estimates one way (a web survey about internet use over-represents internet users), whereas random sampling error averages out. **Total survey error = sampling error + non-sampling error.**

## Formula and fact sheet

- Sampling fraction f = n/N. Proportion: n₀ = z²p(1 − p)/e² (p = 0.5 worst case). Mean: n₀ = z²σ²/e².
- Finite population correction: n = n₀/(1 + (n₀ − 1)/N). Halving e quadruples n.
- z = 1.645 (90%), 1.96 (95%), 2.576 (99%).
- Sampling error falls with n; non-sampling error does not.

## Chapter summary

- A sample survey is faster and cheaper than a census; its quality depends on the frame, the design, the questionnaire, the sample size and the control of errors.
- Sample size for a proportion follows n₀ = z²p(1 − p)/e² with a finite-population correction.
- Sampling error is random and shrinks with n; non-sampling errors are systematic and need careful procedures.

## Practice

1. Differentiate census and sample survey with advantages of each.
2. Define sampling frame, sampling unit and sampling fraction.
3. Find the sample size to estimate a proportion within ±4% at 95% confidence (p unknown); apply the correction for N = 5,000.
4. List the guidelines for a good questionnaire; criticise "Do you agree that the poor service of the library should be improved?"
5. Differentiate sampling and non-sampling errors; give two examples of the latter.
6. Why is a larger sample not a cure for bias?
7. Why is p = 0.5 used when the proportion is unknown?

::: note Answers and worked solutions
**1.** Census: complete, no sampling error, costly. Sample survey: cheaper, faster, usable for destructive tests, but has sampling error.
**2.** Frame: list of units from which to sample; unit: element or group selected; fraction: n/N.
**3.** n₀ = 1.96² × 0.25/0.04² = 0.9604/0.0016 = **600.25 → 601**. With N = 5,000: 600.25/(1 + 599.25/5000) = **536.0 → 536**.
**4.** Guidelines in 5.2. The example is **leading** and loaded ("poor service") and double-barrelled; neutral: "How satisfied are you with the library service?" with a scale.
**5.** Sampling error comes from observing only a part (measurable, shrinks with n). Non-sampling: non-response, measurement error, frame error, processing error.
**6.** Bias is systematic: a larger sample from a biased procedure only gives a more precise wrong answer.
**7.** p(1 − p) is largest (0.25) at p = 0.5, so the resulting n is large enough for any true p.
:::
