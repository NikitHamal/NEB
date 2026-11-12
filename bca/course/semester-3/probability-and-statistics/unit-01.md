---
subject: Probability and Statistics
grade: BCA Semester 3
unit: 1
title: Introduction to Statistics
hours: 3
area: BCA 205 · Probability and Statistics · Unit 1
---

**Statistics** is the science of collecting, organising, analysing and interpreting data to make decisions under uncertainty. A computer scientist uses it for performance measurement, A/B tests, machine learning, quality control and research.

::: key What this unit gives you
- The meaning, scope and limitations of statistics.
- Types of data and variables; levels of measurement.
- Primary and secondary sources; methods of collection and their problems.
:::

## 1.1 Meaning, scope and limitations

In the **singular** sense statistics is a subject (a method of studying data); in the **plural** sense it means numerical facts (the statistics of exam results). Two branches: **descriptive statistics** summarises the data you have (mean, charts); **inferential statistics** draws conclusions about a **population** from a **sample** (estimation and testing). **Population** is the complete set of units of interest; a **sample** is a part of it; a number describing a population is a **parameter** $(\mu ,\  \sigma)$, a number computed from a sample is a **statistic** $(\bar{x} ,\  s)$.

**Scope:** business and economics (demand forecasting), industry (quality control), government (census, planning), health (clinical trials), computing (benchmarking, network traffic modelling, data science), and research in every science.

**Limitations:** statistics deals with **aggregates**, not individuals; it studies **quantitative** facts (qualitative facts must be converted to numbers); results are true **on average**, not for every case; it can be **misused** (selective data, misleading graphs, wrong sampling); and its results are only as good as the data. "There are lies, damned lies, and statistics" is a warning about misuse, not about the method.

## 1.2 Types of data and variables

| Classification | Types | Examples |
|---|---|---|
| **Qualitative (categorical)** | **nominal** (no order), **ordinal** (ordered) | gender, district (nominal); grade A/B/C, satisfaction level (ordinal) |
| **Quantitative (numerical)** | **discrete** (countable, gaps) and **continuous** (any value in a range) | students in a class, errors in a program (discrete); height, response time (continuous) |

**Levels of measurement:** *nominal* (labels), *ordinal* (order but no meaningful differences), *interval* (equal differences, no true zero: temperature in $^{\circ} C$), *ratio* (true zero, ratios meaningful: income, weight). The level decides which statistics make sense: you can compute a mean of ratio data but only a mode for nominal data.

By time: **cross-sectional** data (many units at one time, e.g. today's marks of all students), **time-series** data (one unit over time, e.g. monthly rainfall), **panel** data (both).

## 1.3 Sources of data

|  | Primary data | Secondary data |
|---|---|---|
| Definition | collected first-hand for the present purpose | already collected by someone else |
| Examples | your own survey, experiment, observation | census reports, Nepal Rastra Bank bulletins, published research, company records |
| Advantages | exact fit to the need, known quality | cheap and fast |
| Disadvantages | costly and slow | may be out of date, differ in definitions, or be unreliable |

## 1.4 Methods of collecting primary data

- **Direct personal investigation (interview):** reliable and detailed; costly; interviewer bias.
- **Indirect oral investigation:** questioning people who know about the subject.
- **Questionnaire / schedule:** a questionnaire is filled by respondents (mailed or online), a **schedule** by an enumerator. Good questions are short, clear, neutral, in logical order; pilot-test them.
- **Observation** and **experiment**; **telephone and web surveys**; **local reports and correspondents**.

**Problems of collection:** non-response; **bias** from leading questions or unrepresentative samples; inaccurate answers (memory, sensitivity); cost and time; ambiguous definitions; enumerator errors. **Secondary data** should be checked for source reliability, the definitions used, the date, and the accuracy and units. **Editing** (checking completeness and consistency) comes before tabulation.

## 1.5 Seeing the structure of data

```svgfig label="1.1" caption="Classification of data. Qualitative data are labels (nominal) or ordered labels (ordinal); quantitative data are counts (discrete) or measurements (continuous). The scale of measurement, nominal to ratio, decides which averages make sense."
f = Fig(580, 215)
f.box(220, 8, 140, 32, "Data", fill=NAVY, color="#ffffff", bold=True, size=13)
f.box(70, 66, 170, 32, "Qualitative (categorical)", fill=MINT, stroke=TEAL, bold=True)
f.box(340, 66, 170, 32, "Quantitative (numerical)", fill=SAND, stroke=AMBER, bold=True)
f.arrow([(290, 40), (290, 52), (155, 52), (155, 66)]); f.arrow([(290, 40), (290, 52), (425, 52), (425, 66)])
for x, y, t, fl, st in [(8, 128, "Nominal\nblood group, district", MINT, TEAL), (150, 128, "Ordinal\ngrade A/B/C, rank", MINT, TEAL), (300, 128, "Discrete\nbugs, students", SAND, AMBER), (436, 128, "Continuous\nheight, response time", SAND, AMBER)]:
    f.box(x, y, 126, 44, t, fill=fl, stroke=st, size=10.5)
f.arrow([(155, 98), (155, 112), (71, 112), (71, 128)]); f.arrow([(155, 98), (155, 112), (213, 112), (213, 128)])
f.arrow([(425, 98), (425, 112), (363, 112), (363, 128)]); f.arrow([(425, 98), (425, 112), (499, 112), (499, 128)])
f.text(290, 196, "Scales: nominal (mode) → ordinal (median) → interval (mean, no true zero) → ratio (mean, ratios valid)", size=10.5, color=SLATE, italic=True)
```

```photogrid label="1.1" cols="2" ratio="1.0" caption="From punched card to survey pipeline. (a) The Hollerith tabulating machine, built for the 1890 US census, counted holes in punched cards: the first large automatic statistical processing. (b) Every modern survey, from Nepal's decennial census to a college feedback form, still follows the same five steps."
@ photo id="bca205/hollerith" cap="Hollerith census machine, replica at the Computer History Museum"
fit 1.0
focus 0.5 0.45
@ svg cap="The five steps of a statistical study"
f = Fig(300, 300)
for i, (t, d) in enumerate([("1 Plan", "aim, population,\nvariables"), ("2 Collect", "survey, sensor,\nrecords"), ("3 Edit", "check, clean,\ncode"), ("4 Tabulate", "tables, charts,\nsummaries"), ("5 Analyse", "estimate, test,\ndecide")]):
    y = 10 + i * 57
    f.box(14, y, 96, 40, t, fill=NAVY, color="#ffffff", bold=True, size=13)
    f.text(124, y + 20, d, size=12.5, color=SLATE, anchor="start", vmid=True)
    if i < 4: f.arrow([(62, y + 40), (62, y + 57)])
```

## 1.6 Eight reasons why every computing student needs statistics

1. **Measuring performance honestly.** One run of a program says little, because timings vary from run to run. The mean and standard deviation of many runs tell you the typical speed and how stable it is. A Nepali web team comparing two hosting plans would use exactly this before choosing one.
2. **Making decisions under uncertainty.** Inferential statistics lets you decide from a sample while admitting the chance of error. A bank such as Nabil or NIC Asia tests a new mobile-banking screen on 2,000 users before showing it to millions. The result carries a measured confidence instead of a guess.
3. **Machine learning and data science.** Regression, classification and clustering are statistical ideas in code. Without knowing variance, bias and sampling, a student cannot tell a good model from a lucky one. Nepal's Election Commission and NRB data sets are natural practice material.
4. **Quality control in industry.** Factories sample a few items from each batch and judge the whole batch from them. A Biratnagar noodle mill or a Bhaktapur brick kiln uses this to keep defects low at low cost. Software teams do the same with bug counts per release.
5. **Government planning and the census.** The National Statistics Office counts people, houses and farms to plan schools, hospitals and roads. The 2078 BS census used handheld digital collection, so statistics and computing met in one project. Policies such as the allocation of seats and budgets depend on these figures.
6. **A/B testing and product research.** Two versions of an $a p p$ screen are shown to two random groups, and a statistical test says whether the difference is real. Fonepay and eSewa-type wallets run such experiments on button text and offers. Only a test, not opinion, shows what actually works.
7. **Health, agriculture and environment.** Clinical trials, crop-yield trials and river-pollution monitoring all depend on sampling and comparison. A trial of a new paddy variety in the Terai compares yields on many plots, not one. The same logic protects patients and farmers from false claims.
8. **Reading the news critically.** Graphs with cut axes, tiny samples and selective percentages are common in advertisements and politics. A student who knows what the sample was, how it was chosen and what the margin of error is can spot a weak claim at once. This is the everyday use of the subject.

```photogrid label="1.2" cols="2" ratio="1.2" caption="Never trust a summary you have not drawn. (a) Florence Nightingale, a pioneer of statistical graphics: in 1858 she used a coloured diagram of deaths by month to convince the British government that most soldiers in the Crimean War died of disease, not wounds. (b) Anscombe's four data sets (Francis Anscombe, 1973) each have 11 points, and each has mean of *x* equal to 9, mean of *y* equal to 7.50, correlation $r = 0.82$ and the same regression line $y = 3$ + 0.5x. Yet the pictures are a straight scatter, a smooth curve, a line with one outlier and a vertical stack with one far point. The numbers are identical and the stories are completely different, so always plot the data first. All statistics are recomputed in the figure."
@ photo id="bcamath/nightingale" cap="Florence Nightingale (statistical graphics)"
fit 1.2
focus 0.5 0.35
@ svg cap="Anscombe's quartet: same numbers, four pictures"
import numpy as np
x = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]
ys = [[8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68], [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74], [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]]
x4 = [8] * 7 + [19] + [8] * 3; y4 = [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89]
sets = [(x, ys[0]), (x, ys[1]), (x, ys[2]), (x4, y4)]
for X, Y in sets:
    assert np.mean(X) == 9 and round(np.mean(Y), 2) == 7.5 and round(np.corrcoef(X, Y)[0, 1], 2) == 0.82
    assert np.allclose(np.polyfit(X, Y, 1), [0.5, 3.0], atol=0.005)
f = Fig(300, 240)
for k, (X, Y) in enumerate(sets):
    ox = 8 + (k % 2) * 146; oy = 8 + (k // 2) * 104
    f.box(ox, oy, 138, 96, "", fill=SOFT, stroke="#cbd5e1", r=2, sw=1)
    px = lambda v: ox + 8 + (v - 3) / 17 * 122
    py = lambda v: oy + 88 - (v - 2) / 12 * 78
    f.line(px(3.5), py(3 + .5 * 3.5), px(19.5), py(3 + .5 * 19.5), color=AMBER, sw=1.6)
    for a, b in zip(X, Y): f.circle(px(a), py(b), 3, fill=NAVY, stroke=NAVY, sw=1)
    f.text(ox + 10, oy + 11, ["I", "II", "III", "IV"][k], size=10.5, color=RED, bold=True, anchor="start")
f.text(150, 226, "all: mean x 9, mean y 7.50, r = 0.82, y = 3 + 0.5x", size=10.5, color=NAVY, bold=True)
```

```photogrid label="1.3" cols="2" ratio="1.2" caption="How many people must a poll $a s k$? (a) A ballot drop box: an election is a census of voters, but an opinion poll before it is a sample. (b) For a proportion with the worst case $p = 0.5$ and 95 percent confidence $(z = 1.96)$ the sample size is $n = \frac{z^{2} p (1 - p)}{e^{2}}$. A margin of error $e = 5$ percent needs 385 people, 3 percent needs 1,068, 2 percent needs 2,401 and 1 percent needs 9,604: to cut the error in half you must $a s k$ four times as many. These numbers hardly depend on the size of the country: for the whole of Nepal (about 29 million people) 1,068 are still enough for 3 percent, while for a college of N = 1,000 students the finite-population correction $\frac{n}{1 + \frac{n - 1}{N}}$ brings the 5 percent sample down from 385 to 278, and for $N = 500$ to 218."
@ photo id="bcamath/dropbox" cap="A ballot drop box"
fit 1.2
focus 0.5 0.55
@ svg cap="Sample size for 95 percent confidence, p = 0.5"
import math
def n0(e): return 1.96 ** 2 * 0.25 / e ** 2
def fpc(n, N): return n / (1 + (n - 1) / N)
vals = [(e, math.ceil(n0(e))) for e in (0.05, 0.03, 0.02, 0.01)]
assert [v for _, v in vals] == [385, 1068, 2401, 9604]
assert math.ceil(fpc(n0(0.05), 1000)) == 278 and math.ceil(fpc(n0(0.05), 500)) == 218
assert math.ceil(fpc(n0(0.03), 29_200_000)) == 1068
f = Fig(300, 240)
for i, (e, n) in enumerate(vals):
    y = 18 + i * 32
    f.text(10, y + 11, f"error {int(e * 100)}%", size=10.5, color=SLATE, bold=True, anchor="start", vmid=True)
    w = max(4, n / 9604 * 150)
    f.box(78, y, w, 22, "", fill=(MINT if i == 0 else BLUE), stroke=(TEAL if i == 0 else NAVY), r=2)
    f.text(78 + w + 6, y + 11, f"{n:,}", size=10.5, color=NAVY, bold=True, anchor="start", vmid=True)
f.text(150, 162, "half the error needs four times the sample", size=10.5, color=RED, bold=True)
f.text(150, 186, "college of N = 1,000 at 5%: 385 -> 278", size=10.5, color=TEAL, bold=True)
f.text(150, 206, "college of N = 500 at 5%: 385 -> 218", size=10.5, color=TEAL, bold=True)
f.text(150, 228, "Nepal (29 million) at 3%: still 1,068", size=10.5, color=SLATE)
```

## Formula and fact sheet

- Descriptive $v s$ inferential; population/parameter $v s$ sample/statistic.
- Qualitative: nominal, ordinal. Quantitative: discrete, continuous. Scales: nominal, ordinal, interval, ratio.
- Primary: first-hand. Secondary: existing sources.

## Chapter summary

- Statistics collects, organises, analyses and interprets data; it is powerful but limited to aggregates and can be misused.
- Data are qualitative or quantitative and measured on nominal, ordinal, interval or ratio scales.
- Primary data come from surveys, interviews, observation and experiments; secondary data from existing records; each has typical problems.

## Practice

1. Differentiate descriptive and inferential statistics; population and sample; parameter and statistic.
2. Classify: blood group, number of bugs, server response time, exam grade, temperature in $^{\circ} C$.
3. State four limitations of statistics.
4. Compare primary and secondary data.
5. What is the difference between a questionnaire and a schedule?
6. List four problems in data collection.

::: note Answers and worked solutions
**1.** Descriptive summarises observed data; inferential generalises from sample to population. Population: all units; sample: part of it. A parameter describes a population $(\mu)$; a statistic describes a sample $(\bar{x})$.

**2.** Blood group: nominal; number of bugs: discrete ratio; response time: continuous ratio; exam grade: ordinal; temperature in $^{\circ} C$: continuous interval.

**3.** Deals with groups not individuals; only quantitative; true on average; can be misused; depends on data quality.

**4.** See 1.3: primary is first-hand, exact but costly; secondary is existing, cheap but possibly unsuitable.

**5.** A questionnaire is completed by the respondents themselves; a schedule is filled in by an enumerator who asks the questions.

**6.** Non-response, biased questions, inaccurate answers, unrepresentative sample, cost/time.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Distinguish between primary and secondary data. Describe two methods of collecting primary data.**

*Introduction.* Every statistical study starts with data, and the first question is where the data came from. **Primary data** are collected first-hand by the investigator for the present purpose. **Secondary data** were collected earlier by someone else for another purpose and are reused.

*Comparison (Table).*

| Point | Primary data | Secondary data |
|---|---|---|
| Source | own survey, interview, experiment | census report, NRB bulletin, published paper |
| Fit to need | exact, questions are designed for the study | approximate, definitions may differ |
| Cost and time | high cost, slow | low cost, fast |
| Reliability | known, because the collector controls quality | must be checked for source, date and units |
| Example | a BCA college surveying 120 students about Wi-Fi use | using the NSO census table of literacy by district |

*Two collection methods.* (1) **Direct personal interview:** the enumerator asks each respondent a schedule of questions. It gives detailed and reliable answers and allows clarification, but it is costly and the interviewer may bias answers. (2) **Questionnaire (online or mailed):** respondents fill in the form themselves. It is cheap and reaches many people, as with a Google Form sent to alumni, but non-response is high and nobody can explain a confusing question.

*Conclusion.* Use primary data when no suitable record exists; use secondary data first when it does, and always check its definitions and date.

**Q2 (5 marks). Explain the four scales of measurement with one example each. Why does the scale matter?**

*Introduction.* The **scale of measurement** describes how much information a variable carries, and it decides which statistics are legal to compute.

*The four scales.*

1. **Nominal:** labels with no order, such as blood group or district. Only counting and the **mode** make sense.
2. **Ordinal:** labels with a meaningful order but unequal gaps, such as grade A, B, C or a satisfaction rating. The **median** and percentiles are allowed; averaging the codes is doubtful.
3. **Interval:** equal differences but no true zero, such as temperature in $^{\circ} C$. The **mean** and standard deviation are valid, but 40 $^{\circ} C$ is not "twice as hot" as 20 $^{\circ} C$.
4. **Ratio:** equal differences and a true zero, such as income, weight or response time. Every statistic and ratio is valid: 60 ms is twice as slow as 30 ms.

*Why it matters.* The scale picks the average (mode, median, mean), the chart (bar chart for nominal, histogram for ratio) and the test. Averaging student roll numbers is arithmetic but statistical nonsense, because roll numbers are only labels.

*Conclusion.* Identify the scale first; the right method follows from it.

**Q3 (10 marks). Define statistics. Explain its scope and limitations, and describe the sources and methods of collecting data.**

*Introduction.* In the **singular** sense, statistics is the science of collecting, organising, presenting, analysing and interpreting data to support decisions under uncertainty. In the **plural** sense it means the numerical facts themselves, such as exam results. Its two branches are **descriptive statistics**, which summarises the data in hand, and **inferential statistics**, which draws conclusions about a population from a sample (Figure 1.1 and Plate 1.1 show the data types and the five-step process).

*Scope (six areas).*

1. **Business and economics:** demand forecasting, price indices, risk.
2. **Industry:** sampling inspection and quality control.
3. **Government:** census, planning, budgets, election rolls.
4. **Health and agriculture:** clinical and crop trials.
5. **Computing:** benchmarking, network-traffic models, A/B tests, machine learning.
6. **Research:** every science tests ideas with data.

*Limitations (five points).*

1. Statistics deals with **aggregates**, not with the individual case.
2. It handles only **quantitative** facts; qualitative facts must first be coded.
3. Results are true **on average**, not in every instance.
4. It can be **misused** by selective data, truncated graphs or biased samples.
5. Conclusions are **only as good as the data** collected.

*Sources of data.* **Primary** data are collected first-hand (survey, experiment); **secondary** data come from existing records (census, NRB bulletins, company files). Primary data fit the need but cost more; secondary data are cheap but may be outdated.

*Methods of collecting primary data.* Direct personal interview, indirect oral investigation, questionnaire or schedule, observation, experiment, and telephone or web surveys. Good questions are short, clear, neutral and pilot-tested. Typical problems are non-response, leading questions, memory errors and enumerator bias; collected forms are **edited** for completeness and consistency before tabulation.

*Comparison (Table).*

| Branch | Purpose | Example |
|---|---|---|
| Descriptive | summarise known data | average marks of a class of 48 |
| Inferential | generalise from a sample | estimate the national mean from 1,000 sampled students |

*Conclusion.* Statistics turns raw numbers into evidence, but only when the data are collected carefully and the limits of the method are respected.
