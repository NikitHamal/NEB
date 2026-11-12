---
subject: Software Project Management
grade: BCA Semester 7
unit: 3
title: Software Estimation Techniques
hours: 7
area: BCA 402 · Software Project Management · Unit 3
---

"How long will it take, and what will it cost?" is the first question every client asks and the one on which the whole project plan rests. Software cannot be weighed or measured with a ruler, so estimation is partly science and partly judgement. This unit teaches the main techniques (expert judgement, analogy, bottom-up, top-down and parametric models such as function points and COCOMO) and, equally important, why every estimate is a range rather than a single number.

::: key What this unit gives you
- Why over-estimation and under-estimation both hurt, and the basis on which software estimates are made.
- Expert judgement and the Delphi technique; estimating by analogy with a worked example.
- Bottom-up and top-down estimating, and when to prefer each.
- Size measures: lines of code and function points; parametric models: basic and intermediate COCOMO with worked numbers.
- How to present, track and improve estimates.
:::

## 3.1 Software effort estimation: the problem

**Effort** is the amount of work, measured in **person-days, person-months or person-hours**. **Duration** (elapsed time) depends on effort and on how many people can work in parallel. **Cost** is effort multiplied by the cost rate plus equipment, travel, licences and overheads. An **estimate** is a prediction; a **target** is what the customer wants; a **commitment** is a promise. Confusing these three causes most disputes.

### Problems with over- and under-estimation

| | Over-estimation | Under-estimation |
|---|---|---|
| Direct effect | budget and time are wasted; the bid may lose | the project overruns and costs more than quoted |
| Behaviour | **Parkinson's law**: work expands to fill the time available, so the extra time is consumed anyway | **Brooks' law**: adding people to a late project makes it later; the team cuts corners on design and testing |
| Quality | gold-plating, features nobody asked for | rushed code, skipped tests, more defects, technical debt |
| People | boredom, loss of urgency | overtime, burnout, staff leave |
| Business | resources unavailable for other projects | loss of customer trust; penalties |
| Psychology | padding is hidden in every task | optimistic bias, "everything will go right" |

The **cone of uncertainty** (Boehm; McConnell) shows that early in a project the actual result can be anywhere from about **0.25 to 4 times** the first estimate, narrowing to about 0.8 to 1.25 after detailed design. The lesson is to quote a range and to re-estimate at each milestone.

### Basis of software estimating

Estimates are built from four ingredients:

1. **Size of the product**, for example lines of code, function points, number of screens, use cases or user stories.
2. **Productivity** (size delivered per person-month), taken from *historical data* of similar past projects of the same organisation.
3. **Factors that adjust productivity:** experience of the team, tool support, complexity, reliability required, reuse, schedule pressure.
4. **Project data kept after completion**, which alone makes the next estimate better.

The basic relation: **effort = size ÷ productivity** (or, in parametric models, effort = a × size<sup>b</sup> × adjustment).

::: note Good estimating habits
Estimate by *several* methods and compare; involve the people who will do the work; write down assumptions; add an explicit contingency for risk; estimate *effort* first and derive duration; keep a log of estimated versus actual values and review it after every project.
:::

## 3.2 Software effort estimation techniques

```svgfig label="3.1" caption="A map of estimation techniques. Expert-based and analogy methods depend on judgement and history; algorithmic methods compute effort from a size measure."
f = Fig(620, 230)
f.box(230, 8, 160, 36, "Effort estimation", fill="#ccfbf1", stroke=TEAL, color=NAVY, size=12, bold=True)
cols = [(10, "Experience-based", ["Expert judgement", "Delphi technique", "Analogy"], BLUE, NAVY),
        (215, "Decomposition-based", ["Bottom-up (WBS)", "Top-down (% of total)"], "#bbf7d0", TEAL),
        (420, "Algorithmic / parametric", ["Function points", "COCOMO, COCOMO II", "Putnam / SLIM"], "#fde68a", AMBER)]
for x, t, items, fl, st in cols:
    f.box(x, 80, 190, 34, t, fill=fl, stroke=st, color=NAVY, size=11.5, bold=True)
    f.arrow([(310, 44), (310, 62), (x + 95, 62), (x + 95, 80)], color=SLATE, sw=1.3)
    for i, s in enumerate(items):
        f.box(x + 12, 130 + i * 32, 166, 26, s, fill="#ffffff", stroke=st, color=NAVY, size=10.5)
```

### Expert judgement and the Delphi technique

In **expert judgement** one or more experienced people give an estimate from their knowledge of similar work. It is quick and often accurate, but it is subjective, hard to audit and affected by the expert's optimism or by group pressure.

The **Delphi technique** reduces these biases:

1. A coordinator gives each expert the specification and an estimation form.
2. Experts estimate **independently and anonymously** and may ask the coordinator questions.
3. The coordinator circulates a summary (range, median) without names.
4. Experts revise their estimates in the light of the summary; steps 3 and 4 repeat until the estimates converge.

The **wideband Delphi** variant adds a short group meeting between rounds to discuss reasons for the differences. Planning Poker in agile teams is a close relative.

### Estimating by analogy

Compare the new project with completed projects stored in a database and adjust the closest match.

1. Record attributes (for example screens, database tables, team skill) and actual effort for past projects.
2. Choose the same attributes for the new project.
3. Compute the **distance** between the new project and each past project: d = √((a<sub>new</sub> − a<sub>past</sub>)² + (b<sub>new</sub> − b<sub>past</sub>)²).
4. Take the nearest project (or the average of the nearest two or three) as the base.
5. Adjust for known differences, such as size ratio.

::: example Worked example: analogy with nearest neighbour
The new project has 20 screens and 5 database tables. The history holds:

| Past project | Screens | Tables | Actual effort (person-months) | Distance to the new project |
|---|---|---|---|---|
| P1 | 18 | 4 | 9 | √((20 − 18)² + (5 − 4)²) = √5 = **2.24** |
| P2 | 25 | 6 | 14 | √(25 + 1) = **5.10** |
| P3 | 10 | 2 | 5 | √(100 + 9) = **10.44** |

The nearest is **P1**, so the base estimate is 9 person-months. Adjusting by the size ratio 20/18 gives 9 × 20/18 = **10 person-months**.
:::

*Strengths:* based on real data, easy to explain. *Weaknesses:* needs a good, comparable history; "similar" is subjective; may miss a new technology.

### Bottom-up estimating

The project is decomposed into a WBS down to work packages; each package is estimated by the person who will do it, and the estimates are **added up** (then overheads for integration, management and testing are added).

| Module | Estimate (person-days) |
|---|---|
| Registration and login | 12 |
| Document upload | 8 |
| Payment gateway | 15 |
| Admin panel and reports | 20 |
| Data migration | 6 |
| **Subtotal (coding and unit test)** | **61** |
| Integration and system test (30%) | 18 |
| Project management and reviews (15%) | 9 |
| **Total** | **88 person-days** |

*Advantages:* detailed and accurate when the design is known; the team owns the numbers; tasks feed straight into the schedule. *Disadvantages:* it needs a complete WBS (so it is impossible very early); easy to forget system-level activities such as integration, documentation and meetings; it takes time.

### Top-down estimating

A total estimate for the whole project is made first (from analogy, a parametric model, or a given budget) and **divided** among the components or phases using historical percentages.

| Phase | Typical share of effort | For a 100 person-day project |
|---|---|---|
| Requirements and analysis | 10 to 15% | 12 |
| Design | 15 to 20% | 18 |
| Coding and unit testing | 30 to 40% | 35 |
| Integration and testing | 20 to 25% | 23 |
| Project management and deployment | 10 to 15% | 12 |

*Advantages:* usable at the start with little information; it takes the whole-system view; quick. *Disadvantages:* it can miss technical difficulties of individual parts, and low-level estimates inherit any error in the total. Use top-down for early budgets and bottom-up for detailed plans, then **reconcile** the two.

### Comparison

| Technique | Needs | Accuracy (when applied properly) | Best used |
|---|---|---|---|
| Expert judgement / Delphi | experienced people | medium | early stage; new kinds of work |
| Analogy | past project data | medium | similar projects |
| Bottom-up | WBS and design | high | detailed planning |
| Top-down | total or size estimate | low to medium | feasibility and budgeting |
| Parametric models | size and calibration data | medium to high | planning, what-if analysis |

## 3.3 Measuring size

### Lines of code (LOC and KLOC)

The simplest size measure is the number of source lines (**KLOC** = thousand lines of code). Productivity of a team is then LOC per person-month. LOC is easy to count after the project, but it has serious weaknesses: it is not known at the start; it depends on the language (a task needing 1,000 lines of C may need 300 in Python); it rewards verbose code; and it ignores design, documentation and testing effort.

### Function points (FP)

**Function point analysis** (Allan Albrecht at IBM, 1979; now maintained by IFPUG) measures the **functionality delivered to the user**, independent of language. It can be done from the requirements.

**Step 1: count five component types** and weight them by complexity (low, average, high):

| Component | Meaning | Low | Average | High |
|---|---|---|---|---|
| External inputs (EI) | data or control entering the system (forms, transactions) | 3 | 4 | 6 |
| External outputs (EO) | reports and screens produced from processed data | 4 | 5 | 7 |
| External inquiries (EQ) | input-output pairs that retrieve data without processing | 3 | 4 | 6 |
| Internal logical files (ILF) | user-identifiable data groups maintained by the system | 7 | 10 | 15 |
| External interface files (EIF) | data groups used by the system but maintained elsewhere | 5 | 7 | 10 |

The weighted total is the **unadjusted function point count (UFP)**.

**Step 2: value adjustment factor (VAF).** Rate 14 general system characteristics (data communications, distributed processing, performance, heavily used configuration, transaction rate, online data entry, end-user efficiency, online update, complex processing, reusability, installation ease, operational ease, multiple sites, ease of change) from 0 (no influence) to 5 (strong). With **TDI** the total degree of influence (0 to 70):

**VAF = 0.65 + 0.01 × TDI**, and **FP = UFP × VAF**.

**Step 3: effort** = FP ÷ productivity (FP per person-month from history).

::: example Worked example: function points
For the admission portal, all components are of average complexity: 10 EI, 8 EO, 6 EQ, 5 ILF and 3 EIF.

UFP = 10 × 4 + 8 × 5 + 6 × 4 + 5 × 10 + 3 × 7 = 40 + 40 + 24 + 50 + 21 = **175**.
The 14 characteristics total TDI = 42, so VAF = 0.65 + 0.01 × 42 = **1.07**.
FP = 175 × 1.07 = **187.25 function points**.
If the organisation delivers 12 FP per person-month, effort = 187.25 / 12 = **15.6 person-months**.
At about 53 lines of Java per FP, this is roughly 9,900 lines of code, which also gives a rough size for COCOMO.
:::

*Advantages:* language-independent; available early; relates to user value. *Disadvantages:* some subjectivity in judging complexity; needs training; less suited to algorithm-heavy or real-time systems (extensions such as feature points and COSMIC exist); counting takes effort.

## 3.4 Parametric (algorithmic) models

A **parametric model** computes effort from a size measure and a set of parameters, calibrated from many past projects: **effort = a × size<sup>b</sup>** (or a function of several drivers). The exponent b > 1 expresses **diseconomy of scale**: doubling the size more than doubles the effort because of communication and integration overhead.

### Basic COCOMO (Boehm, 1981)

The **COnstructive COst MOdel** estimates from size in KLOC. Projects are classed in three modes:

| Mode | Description | a | b | c | d |
|---|---|---|---|---|---|
| **Organic** | small team, familiar problem, flexible requirements, little innovation (e.g. a business application) | 2.4 | 1.05 | 2.5 | 0.38 |
| **Semi-detached** | medium team, mixed experience, mixture of rigid and flexible requirements (e.g. a DBMS or compiler) | 3.0 | 1.12 | 2.5 | 0.35 |
| **Embedded** | tight hardware, software and operational constraints (e.g. flight control, ATM switch) | 3.6 | 1.20 | 2.5 | 0.32 |

- **Effort (person-months)** E = a × (KLOC)<sup>b</sup>
- **Development time (months)** D = c × E<sup>d</sup>
- **Average staffing** = E / D people
- **Productivity** = KLOC / E (or LOC per person-month)

::: example Worked example: basic COCOMO for 32 KLOC
For a product of 32 KLOC, 32<sup>1.05</sup> = 38.05 and 32<sup>1.12</sup> = 48.5, 32<sup>1.20</sup> = 64.0.

| Mode | Effort E (person-months) | Time D (months) | Staff E / D | Productivity (LOC per person-month) |
|---|---|---|---|---|
| Organic | 2.4 × 38.05 = **91.3** | 2.5 × 91.3<sup>0.38</sup> = **13.9** | **6.6** | 350 |
| Semi-detached | 3.0 × 48.5 = **145.5** | 2.5 × 145.5<sup>0.35</sup> = **14.3** | **10.2** | 220 |
| Embedded | 3.6 × 64.0 = **230.4** | 2.5 × 230.4<sup>0.32</sup> = **14.3** | **16.2** | 139 |

If an organic-mode developer costs Rs 60,000 per month, the labour cost is 91.3 × 60,000 = **Rs 5.48 million**. Note how the same size costs 2.5 times more effort in embedded mode.
:::

### Intermediate COCOMO

Intermediate COCOMO multiplies the nominal effort by an **effort adjustment factor (EAF)**, the product of 15 **cost drivers**, each rated from very low to extra high:

| Group | Cost drivers |
|---|---|
| Product | required reliability (RELY), database size (DATA), product complexity (CPLX) |
| Computer | execution time constraint (TIME), storage constraint (STOR), virtual machine volatility (VIRT), turnaround time (TURN) |
| Personnel | analyst capability (ACAP), application experience (AEXP), programmer capability (PCAP), virtual machine experience (VEXP), language experience (LEXP) |
| Project | modern programming practices (MODP), software tools (TOOL), required schedule (SCED) |

E = a<sub>i</sub> × (KLOC)<sup>b</sup> × EAF, with a<sub>i</sub> = 3.2 (organic), 3.0 (semi-detached) and 2.8 (embedded); b is unchanged.

::: example Worked example: intermediate COCOMO
An organic 32 KLOC product has high complexity and tight timing (EAF = 1.15). E = 3.2 × 38.05 × 1.15 = **140.0 person-months**. D = 2.5 × 140<sup>0.38</sup> = **16.3 months**, and average staff = 140.0 / 16.3 = **8.6 people**. Compare with 121.8 person-months at EAF = 1.00: the drivers raise the effort by 15%.
:::

### COCOMO II (2000)

COCOMO II updates the model for modern development. It has three stages: **application composition** (prototyping, estimated with object points), **early design** (function points and 7 drivers) and **post-architecture** (source size and 17 drivers). The exponent is not fixed: **E = A × Size<sup>B</sup> × ΠEM**, where B = 1.01 + 0.01 × Σ(five **scale factors**: precedentedness, development flexibility, architecture and risk resolution, team cohesion, process maturity) and A = 2.94. It handles reuse, rapid application development and component-based software.

### Other models

The **Putnam model** (SLIM) relates size, effort and time through the Rayleigh curve, with effort proportional to 1/time<sup>4</sup> for a fixed size, showing that compressing the schedule is very expensive. **Use case points**, **story points** and **object points** serve object-oriented and agile projects.

### Limits of parametric models

- Garbage in, garbage out: the size estimate is itself uncertain (so give a range).
- The models need **calibration** to the organisation's own history.
- They assume a conventional process; they say little about requirements volatility or the effect of an individual star developer.
- Results are best treated as one input to be compared with bottom-up and expert estimates.

## Formula and fact sheet

- Effort = size ÷ productivity; duration depends on staffing.
- Delphi: independent anonymous estimates, summary feedback, repeat until convergence.
- FP = UFP × (0.65 + 0.01 × TDI); weights EI 4, EO 5, EQ 4, ILF 10, EIF 7 (average).
- Basic COCOMO: E = a × KLOC<sup>b</sup>; D = 2.5 × E<sup>d</sup>; staff = E/D. Organic (2.4, 1.05, 0.38), semi-detached (3.0, 1.12, 0.35), embedded (3.6, 1.20, 0.32).
- Intermediate COCOMO: E = a<sub>i</sub> × KLOC<sup>b</sup> × EAF with a<sub>i</sub> = 3.2, 3.0, 2.8.
- PERT t<sub>e</sub> = (O + 4M + P)/6 may also be used for each task estimate.

## Chapter summary

- Over-estimation wastes resources (Parkinson's law) and under-estimation harms quality and morale (Brooks' law); estimates are ranges that narrow over time (cone of uncertainty).
- Estimates are based on size, productivity from historical data, and adjustment factors.
- Experience-based methods are expert judgement, Delphi and analogy; decomposition methods are bottom-up and top-down; algorithmic methods are function points and COCOMO.
- Function points measure user functionality independent of language; COCOMO converts KLOC to effort, time and staffing with b > 1.
- Use several techniques, keep records and re-estimate at milestones.

## Practice

1. Distinguish estimate, target and commitment. Why does confusing them cause trouble?
2. Explain the problems with over-estimation and under-estimation.
3. Describe the Delphi technique with its steps.
4. Explain estimating by analogy. A new project has 12 screens and 3 tables; past projects are P1 (10, 3, 6 person-months) and P2 (16, 5, 11 person-months). Which is nearest and what is the estimate?
5. Compare bottom-up and top-down estimating, with advantages and disadvantages.
6. Compute the function points: 5 EI, 4 EO, 3 EQ, 2 ILF, 1 EIF, all average; TDI = 35.
7. Using basic COCOMO organic mode, find the effort, duration and average staff for a 20 KLOC system. (20<sup>1.05</sup> = 23.2, E<sup>0.38</sup> follows from your answer.)
8. Why is the exponent b greater than 1 in COCOMO?
9. List the three COCOMO modes with an example for each.
10. Give four limitations of parametric models.

::: note Answers and worked solutions
**1.** An estimate is a prediction, a target is a desired result, a commitment is a promise. If a target is passed off as an estimate, the plan is built on wishes and the team is blamed when it fails.
**2.** Over-estimation: wasted budget, Parkinson's law, lost bids, gold-plating. Under-estimation: overruns, rushed work and defects, Brooks' law, stress, loss of trust, penalties.
**3.** A coordinator gives the specification; experts estimate independently and anonymously; a summary is circulated; experts revise; the cycle repeats until the estimates converge. Wideband Delphi adds a discussion meeting.
**4.** Distance to P1 = √((12 − 10)² + 0) = **2.0**; to P2 = √(16 + 4) = **4.47**. P1 is nearest: 6 person-months, scaled by 12/10 gives **7.2 person-months**.
**5.** Bottom-up: detailed and owned by the team, but needs a full WBS and may omit system-level work. Top-down: fast and usable early, but may hide technical difficulty. Use both and reconcile.
**6.** UFP = 5 × 4 + 4 × 5 + 3 × 4 + 2 × 10 + 1 × 7 = 20 + 20 + 12 + 20 + 7 = **79**; VAF = 0.65 + 0.35 = **1.00**; FP = **79**.
**7.** E = 2.4 × 23.2 = **55.7 person-months**; D = 2.5 × 55.7<sup>0.38</sup> = 2.5 × 4.59 = **11.5 months**; staff = 55.7/11.5 = **4.8 people**.
**8.** Because productivity falls as projects grow: more communication paths and integration work mean a diseconomy of scale.
**9.** Organic (payroll or inventory system), semi-detached (database management system, compiler), embedded (flight control, ATM switch).
**10.** Uncertain size input, need for calibration, assumes a conventional process, ignores individual differences and requirement volatility.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the problems with over-estimation and under-estimation of a software project.**

*Introduction.* Estimation predicts the effort, time and cost of a project; errors in either direction harm the project.

*Over-estimation.* It leads to a plan with more time and money than needed. By **Parkinson's law** work expands to fill the available time, so the extra is wasted. A bid based on an inflated estimate may be lost, and resources are tied up that other projects need. Teams drift into gold-plating.

*Under-estimation.* The project overruns its budget and deadline. Under pressure, developers skip design, reviews and testing, so defects rise and quality falls. Management may add people late, which by **Brooks' law** makes things worse. Overtime causes fatigue and turnover, and the customer loses confidence.

*Conclusion.* Slight over-estimation is less harmful than under-estimation, but both are avoided by using several techniques, historical data, and ranges that are updated as knowledge grows.

**Q2 (10 marks). Explain COCOMO with its three modes. Estimate effort, time and staffing for a 32 KLOC organic project.**

*Introduction.* COCOMO is a parametric model proposed by Barry Boehm in 1981 that predicts effort from the size of the software in KLOC.

*Modes and equations.* Organic (a = 2.4, b = 1.05, d = 0.38), semi-detached (3.0, 1.12, 0.35) and embedded (3.6, 1.20, 0.32). E = a × KLOC<sup>b</sup> person-months; D = 2.5 × E<sup>d</sup> months; staff = E / D.

*Calculation (organic, 32 KLOC).* E = 2.4 × 32<sup>1.05</sup> = 2.4 × 38.05 = **91.3 person-months**. D = 2.5 × 91.3<sup>0.38</sup> = **13.9 months**. Staff = 91.3/13.9 = **6.6 people**. Productivity = 32,000/91.3 = 350 LOC per person-month.

| Quantity | Value |
|---|---|
| Effort | 91.3 person-months |
| Duration | 13.9 months |
| Average team | 6.6 persons |
| Labour cost at Rs 60,000 per month | Rs 5.48 million |

*Intermediate and COCOMO II.* Intermediate COCOMO multiplies the effort by the product of 15 cost drivers (EAF); COCOMO II uses scale factors for the exponent and handles reuse and modern processes.

*Limits.* The size must itself be estimated and the model needs local calibration.

*Conclusion.* COCOMO gives a defendable baseline that is combined with expert and bottom-up estimates.
