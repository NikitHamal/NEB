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

## 5.5 Pictures of a sample survey

```svgfig label="5.1" caption="The life of a sample survey and where each error enters. The frame may miss units (frame error); only part of the population is drawn (sampling error, measurable); some chosen units do not answer or answer wrongly (non-response and response error); data entry adds processing error. Inference then goes back from sample to population."
f = Fig(580, 225)
f.box(8, 30, 118, 52, "Target\npopulation", fill=BLUE, bold=True)
f.box(160, 30, 118, 52, "Sampling\nframe", fill=BLUE, bold=True)
f.box(312, 30, 118, 52, "Sample\n(n units)", fill=MINT, stroke=TEAL, bold=True)
f.box(464, 30, 108, 52, "Collected\ndata", fill=SAND, stroke=AMBER, bold=True)
f.arrow([(126, 56), (160, 56)]); f.arrow([(278, 56), (312, 56)]); f.arrow([(430, 56), (464, 56)])
for x, t in [(143, "frame\nerror"), (295, "sampling\nerror"), (447, "non-response,\nresponse error")]:
    f.text(x, 108, t, size=10.5, color=RED, bold=True)
f.arrow([(518, 82), (518, 150)], label=None)
f.box(464, 150, 108, 44, "Tables and\nestimates", fill=SOFT, stroke=SLATE, bold=True)
f.text(518, 130, "processing error", size=10.5, color=RED, bold=True)
f.arrow([(464, 172), (68, 172), (68, 82)], color=TEAL, dash=True)
f.text(280, 164, "inference: generalise from the sample to the population", size=11, color=TEAL, bold=True)
f.text(280, 212, "Sampling error falls as n grows; the other errors do not.", size=10.5, color=SLATE, italic=True)
```

```svgfig label="5.2" caption="Sample size against margin of error for a proportion at 95% confidence (p = 0.5): n = 0.9604/e². Halving the margin quadruples the sample, so precision is expensive: ±5 points needs 385, ±3 needs 1,068 and ±1 needs 9,604 respondents."
f = Fig(580, 215)
ax = Axes(f, 70, 16, 350, 160, (0, 10), (0, 4000))
ax.grid(2, 1000, xfmt=lambda v: f"{v:g}%"); ax.axes("margin of error e", "n")
ax.curve(lambda e: 0.9604 / (e / 100) ** 2, 1.55, 10, color=NAVY, sw=2.6)
for e, n in [(5, 384.16), (3, 1067.1), (2, 2401)]:
    ax.pt(e, n, f"e = {e}%: n = {round(n + 0.5)}", dx=10, dy=-6, color=RED)
f.text(500, 60, "e = 1% needs", size=11, color=AMBER, bold=True); f.text(500, 78, "n = 9,604", size=11, color=AMBER, bold=True)
f.text(500, 110, "Finite population", size=10.5, color=SLATE); f.text(500, 126, "correction trims n", size=10.5, color=SLATE)
f.text(500, 142, "when N is small", size=10.5, color=SLATE)
```

```svgfig label="5.3" caption="Random error versus bias, shown as four targets (centre = true value). (a) Accurate and precise: small sampling error and no bias. (b) Precise but biased: a bad frame or a leading question moves every estimate the same way. (c) Unbiased but scattered: a small sample, large sampling error. (d) Both problems."
f = Fig(580, 205)
shots = [[(0, 0), (6, -4), (-5, 5), (3, 7), (-6, -3)], [(30, 22), (35, 26), (28, 28), (33, 20), (37, 24)],
         [(-26, 18), (28, -20), (-10, -32), (32, 14), (-30, -12)], [(-30, 24), (-20, 36), (-36, 14), (-24, 28), (-14, 20)]]
for k, (t, pts) in enumerate(zip(["(a) accurate, precise", "(b) biased, precise", "(c) scattered", "(d) biased + scattered"], shots)):
    cx = 72 + k * 145
    for r, c in [(52, "#dbeafe"), (36, "#93c5fd"), (20, "#3b82f6"), (7, "#1e3a8a")]:
        f.circle(cx, 98, r, fill=c, stroke="#ffffff", sw=1.2)
    for dx, dy in pts:
        f.circle(cx + dx, 98 + dy, 3.6, fill=RED, stroke="#ffffff", sw=1)
    f.text(cx, 172, t, size=10.5, color=NAVY, bold=True)
f.text(290, 194, "Larger n shrinks the scatter in (c); only better design removes the bias in (b).", size=10.5, color=SLATE, italic=True)
```

## 5.6 Eight rules of a good sample survey

1. **State the objective in one sentence.** A vague aim such as "learn about students" gives useless data. A clear aim such as "the share of BCA students who use e-books weekly" fixes who, what and when. Every question afterwards must serve that sentence.
2. **Build a complete, up-to-date frame.** The frame is the list from which units are drawn, so a missing name can never be selected. An old voters' list or an outdated student register causes frame error. Updating the list is cheaper than correcting a biased result.
3. **Choose probability sampling.** Giving every unit a known chance of selection allows an honest margin of error. Convenience samples, such as asking friends, cannot do this. Simple random, stratified and cluster designs are covered in Unit 6.
4. **Work out the sample size, do not guess.** Use n₀ = z²p(1 − p)/e² and apply the finite-population correction for a small population. A college of 2,000 needs about 323 students for ±5 points at 95% confidence. Too small a sample wastes the survey; too large wastes money.
5. **Write simple, neutral questions.** Ask one thing at a time and avoid leading words such as "Don't you agree". Offer options that cover all answers without overlap. Translate carefully into Nepali, since a changed word changes the answer.
6. **Pilot-test first.** Try the form on 10 to 20 people and watch where they hesitate. Fix the confusing items and time the interview. A one-day pilot often saves weeks of bad fieldwork.
7. **Train enumerators and control non-response.** Interviewers must read questions exactly and record answers honestly. Callbacks, a convenient time and a short form raise the response rate. Large non-response is a bigger danger than a small sample.
8. **Check, enter and report with care.** Edit forms for gaps, use double entry or range checks, and keep a log of changes. Report the frame, the sample size, the response rate and the margin of error. Honest reporting lets readers judge how far to trust the numbers.

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

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). A municipality has 20,000 households. Find the sample size needed to estimate the proportion with home internet within ±2 percentage points at 99% confidence. How many households would be needed to estimate mean monthly data use if σ = 12 GB and the error allowed is ±2 GB at 95% confidence?**

*Introduction.* The sample size for a proportion is n₀ = z²p(1 − p)/e². With no prior estimate we take p = 0.5, which gives the largest possible p(1 − p) = 0.25 and so a safe size.

*Proportion.* For 99% confidence z = 2.576, and e = 0.02. n₀ = 2.576² × 0.25/0.02² = 1.6589/0.0004 = **4147.4**, rounded up to 4,148.

*Finite-population correction.* The population is small enough to matter, so n = n₀/[1 + (n₀ − 1)/N] = 4147.36/(1 + 4146.36/20000) = 4147.36/1.2073 = **3435.2**, rounded up to **3,436 households**.

*Mean.* For a mean, n₀ = z²σ²/e² = 1.96² × 12²/2² = 3.8416 × 144/4 = **138.3**, rounded up to **139 households**.

*Interpretation.* Estimating a proportion to a tight ±2 points costs many more interviews than estimating a mean to a reasonable precision. *Conclusion.* Always round up, apply the correction when n is a noticeable part of N, and remember that halving e multiplies n by four.

**Q2 (5 marks). Distinguish between a census and a sample survey. When is a sample survey preferred?**

*Introduction.* A **census** collects information from every unit of the population; a **sample survey** collects it from a selected part and generalises to the whole. Nepal's decennial population census is the standard example of the first; a college's satisfaction survey of 300 students is an example of the second.

*Comparison (Table).*

| Point | Census | Sample survey |
|---|---|---|
| Coverage | every unit | a selected part |
| Cost and time | very high, years of work | much lower, results in weeks |
| Sampling error | none | present but measurable |
| Non-sampling error | can be large (many enumerators) | easier to control with fewer, trained staff |
| Detail | small-area figures available | only for large groups |

*When a sample survey is preferred.* (1) The population is very large. (2) Testing destroys the unit, as with bulbs or crash tests. (3) Results are needed quickly. (4) The budget is limited. (5) Better-trained interviewers can improve quality.

*When a census is needed.* When every unit's record matters, such as the voter list or small-area planning data. *Conclusion.* A well-designed sample is often more accurate in practice than a rushed census.

**Q3 (10 marks). Explain the steps of organising a sample survey and discuss sampling and non-sampling errors with their remedies.**

*Introduction.* A **sample survey** studies a part of the population in order to infer about the whole. Its quality depends on planning, design and control of errors (Figure 5.1 shows the life of a survey).

*Steps of organising a survey.*

1. **Objectives:** state precisely what, who, where and when.
2. **Population and frame:** define the target population and prepare an up-to-date, complete list.
3. **Data and method:** decide the items to collect and the method (interview, mail, phone, web).
4. **Questionnaire:** short, clear, neutral, one idea per question, logically ordered.
5. **Sampling design and size:** choose a probability design and compute n = z²p(1 − p)/e².
6. **Pilot survey:** test the form and field procedure on a small group.
7. **Fieldwork:** train enumerators, supervise, follow up non-response.
8. **Editing, tabulation, analysis and report:** check, code, enter, estimate and report with margins of error.

*Sampling error.* It is the difference between the sample estimate and the true value because only a part is observed. It is **random**, **measurable** through the standard error, and falls roughly as 1/√n; a census has none. For example, with n = 385 the margin for a proportion is about ±5 points, and with n = 1,068 it is about ±3 (Figure 5.2).

*Non-sampling errors.* They arise at every stage, occur even in a census, and **do not shrink with larger n**.

| Source | Example | Remedy |
|---|---|---|
| Frame error | outdated list, missing hostels | update and check the frame |
| Non-response | nobody at home, refusals | callbacks, short form, weighting |
| Response error | memory lapse, sensitive question | clear wording, trained interviewers |
| Processing error | wrong code, typing mistake | double entry, range checks |
| Selection bias | asking friends only | probability sampling |

*Sampling versus non-sampling (Table).*

| Point | Sampling error | Non-sampling error |
|---|---|---|
| Cause | observing only a part | mistakes in design, collection, processing |
| Direction | random, averages out | often one-sided (bias) |
| Effect of larger n | decreases | may increase |
| Measurable? | yes, by standard error | difficult |
| In a census | absent | present |

*Conclusion.* Total survey error is sampling error plus non-sampling error. Increasing n helps only against the first, so a good survey invests in a sound frame, clear questions, trained staff and a high response rate, as Figure 5.3 shows with its targets of bias and scatter.
