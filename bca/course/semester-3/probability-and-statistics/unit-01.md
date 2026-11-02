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

In the **singular** sense statistics is a subject (a method of studying data); in the **plural** sense it means numerical facts (the statistics of exam results). Two branches: **descriptive statistics** summarises the data you have (mean, charts); **inferential statistics** draws conclusions about a **population** from a **sample** (estimation and testing). **Population** is the complete set of units of interest; a **sample** is a part of it; a number describing a population is a **parameter** (μ, σ), a number computed from a sample is a **statistic** (x̄, s).

**Scope:** business and economics (demand forecasting), industry (quality control), government (census, planning), health (clinical trials), computing (benchmarking, network traffic modelling, data science), and research in every science.

**Limitations:** statistics deals with **aggregates**, not individuals; it studies **quantitative** facts (qualitative facts must be converted to numbers); results are true **on average**, not for every case; it can be **misused** (selective data, misleading graphs, wrong sampling); and its results are only as good as the data. "There are lies, damned lies, and statistics" is a warning about misuse, not about the method.

## 1.2 Types of data and variables

| Classification | Types | Examples |
|---|---|---|
| **Qualitative (categorical)** | **nominal** (no order), **ordinal** (ordered) | gender, district (nominal); grade A/B/C, satisfaction level (ordinal) |
| **Quantitative (numerical)** | **discrete** (countable, gaps) and **continuous** (any value in a range) | students in a class, errors in a program (discrete); height, response time (continuous) |

**Levels of measurement:** *nominal* (labels), *ordinal* (order but no meaningful differences), *interval* (equal differences, no true zero: temperature in °C), *ratio* (true zero, ratios meaningful: income, weight). The level decides which statistics make sense: you can compute a mean of ratio data but only a mode for nominal data.

By time: **cross-sectional** data (many units at one time, e.g. today's marks of all students), **time-series** data (one unit over time, e.g. monthly rainfall), **panel** data (both).

## 1.3 Sources of data

| | Primary data | Secondary data |
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

## Formula and fact sheet

- Descriptive vs inferential; population/parameter vs sample/statistic.
- Qualitative: nominal, ordinal. Quantitative: discrete, continuous. Scales: nominal, ordinal, interval, ratio.
- Primary: first-hand. Secondary: existing sources.

## Chapter summary

- Statistics collects, organises, analyses and interprets data; it is powerful but limited to aggregates and can be misused.
- Data are qualitative or quantitative and measured on nominal, ordinal, interval or ratio scales.
- Primary data come from surveys, interviews, observation and experiments; secondary data from existing records; each has typical problems.

## Practice

1. Differentiate descriptive and inferential statistics; population and sample; parameter and statistic.
2. Classify: blood group, number of bugs, server response time, exam grade, temperature in °C.
3. State four limitations of statistics.
4. Compare primary and secondary data.
5. What is the difference between a questionnaire and a schedule?
6. List four problems in data collection.

::: note Answers and worked solutions
**1.** Descriptive summarises observed data; inferential generalises from sample to population. Population: all units; sample: part of it. A parameter describes a population (μ); a statistic describes a sample (x̄).
**2.** Blood group: nominal; number of bugs: discrete ratio; response time: continuous ratio; exam grade: ordinal; temperature in °C: continuous interval.
**3.** Deals with groups not individuals; only quantitative; true on average; can be misused; depends on data quality.
**4.** See 1.3: primary is first-hand, exact but costly; secondary is existing, cheap but possibly unsuitable.
**5.** A questionnaire is completed by the respondents themselves; a schedule is filled in by an enumerator who asks the questions.
**6.** Non-response, biased questions, inaccurate answers, unrepresentative sample, cost/time.
:::
