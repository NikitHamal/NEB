---
subject: Software Project Management
grade: BCA Semester 7
unit: 5
title: Risk Management
hours: 5
area: BCA 402 · Software Project Management · Unit 5
---

Every plan is a bet on the future. The lead developer may resign, the payment gateway may change its API, the user may rewrite the requirements in week 12. A **risk** is an uncertain event that, if it happens, affects the project's objectives; a risk that has already happened is an **issue**. The aim of risk management is not to remove uncertainty (impossible) but to **think about it early, when options are many and cheap**, instead of being surprised late, when options are few and costly.

::: key What this unit gives you
- Risk, its categories and its relation to a project's objectives.
- A framework for dealing with risk: identification, assessment, planning, monitoring.
- Risk exposure, expected monetary value, risk reduction leverage and responses (avoid, mitigate, transfer, accept).
- Evaluating risks to the schedule with PERT and near-critical paths; contingency and buffers.
:::

## 5.1 Risk and its categories

**Risk** = an uncertain event or condition with a probability of occurring and an impact on at least one project objective (scope, time, cost, quality). Two properties describe every risk:

- **Probability (likelihood)** that the event occurs, from 0 to 1.
- **Impact (loss)**, the consequence if it occurs, in money, days or quality.

**Risk exposure (RE) = probability × impact**, also called the **expected loss** or **risk value**.

### Categories of risk

Risks can be classified by *where they come from* or *what they threaten*.

| Category | Examples in a software project |
|---|---|
| **Requirements** | incomplete or changing requirements; misunderstanding; gold-plating |
| **Estimation and schedule** | optimistic estimates; unrealistic deadline; dependencies on other teams |
| **Technology** | new or immature tools; performance targets not met; integration problems; poor tool support |
| **People** | key staff leave; skill gaps; conflicts; low morale |
| **Organisational and management** | changes in priorities; budget cuts; poor communication; weak sponsor |
| **External** | supplier failure; change in law (for example data-protection rules); market changes; power cuts and connectivity in Nepal |
| **Quality and security** | excessive defects; data breach; non-compliance |
| **Contractual / commercial** | unclear contract; penalty clauses; client insolvency |

Boehm's classic **top ten software risk items** list includes personnel shortfalls, unrealistic schedules and budgets, wrong software functions, wrong user interface, gold plating, continuing stream of requirements changes, shortfalls in externally furnished components, shortfalls in externally performed tasks, real-time performance shortfalls, and straining computer science capabilities.

Another useful split is by *type*: **project risks** (threaten the schedule or resources), **product (technical) risks** (threaten the quality or performance of the software) and **business risks** (threaten the viability of the product, for example a competitor releases first). A risk may also be a **positive risk (opportunity)**, such as a reusable component turning out better than expected.

## 5.2 A framework for dealing with risk

```svgfig label="5.1" caption="The risk management cycle. Risk identification and assessment feed planning; monitoring feeds new risks back into identification."
f = Fig(620, 240)
f.box(10, 24, 130, 54, "1. Risk\nidentification", fill=BLUE, color=NAVY, size=11.5, bold=True)
f.box(165, 24, 130, 54, "2. Risk analysis,\nprioritisation", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=11, bold=True)
f.box(320, 24, 130, 54, "3. Risk planning\n(responses)", fill="#fde68a", stroke=AMBER, color=NAVY, size=11.5, bold=True)
f.box(475, 24, 130, 54, "4. Monitoring\nand control", fill="#fecaca", stroke=RED, color=NAVY, size=11.5, bold=True)
for x in (140, 295, 450):
    f.arrow([(x, 51), (x + 25, 51)], color=NAVY, sw=1.8)
f.arrow([(540, 78), (540, 150), (75, 150), (75, 78)], color=SLATE, sw=1.6, dash=True)
f.text(310, 170, "New and changed risks are fed back every week or sprint", size=11, color=SLATE)
f.box(150, 190, 320, 36, "Risk register: the live record of every risk", fill="#ccfbf1", stroke=TEAL, color=NAVY, size=11.5, bold=True)
```

### Step 1: Risk identification

Risks must be found before they can be managed. Techniques:

- **Checklists** based on past projects and on lists such as Boehm's top ten.
- **Brainstorming** with the whole team, users and sponsor.
- **Delphi technique** with anonymous expert opinion.
- **Interviews, SWOT analysis** and **assumption analysis** (every assumption is a possible risk).
- **Review of lessons learned** and of the WBS (look at each work package: what could go wrong?).
- **Prompt lists** (people, process, product, technology, external).

Write every risk clearly in the form **cause, event, effect**: "Because the team has never used the payment API (cause), integration may take longer than planned (event), delaying go-live by two weeks (effect)."

### Step 2: Risk assessment (analysis)

**Qualitative assessment** rates probability and impact on a scale (low, medium, high or 1 to 5) and plots them on a **probability-impact matrix**, which ranks the risks.

```svgfig label="5.2" caption="A probability-impact matrix. Red cells need an active response, amber cells need monitoring, green cells are accepted. R1, R2 and R3 are plotted risks."
f = Fig(520, 270)
cols = ["#bbf7d0", "#bbf7d0", "#fde68a", "#fde68a", "#fecaca"]
for i in range(3):
    for j in range(3):
        score = (i + 1) * (j + 1)
        c = "#bbf7d0" if score <= 2 else ("#fde68a" if score <= 4 else "#fecaca")
        f.box(110 + j * 120, 20 + (2 - i) * 70, 116, 66, "", fill=c, stroke=SLATE)
for k, t in enumerate(["Low", "Medium", "High"]):
    f.text(168 + k * 120, 244, t, size=11, color=NAVY, bold=True)
    f.text(98, 56 + (2 - k) * 70, t, size=11, color=NAVY, bold=True, anchor="end")
f.text(290, 262, "Impact", size=11, color=SLATE)
f.text(20, 20, "Probability", size=11, color=SLATE, anchor="start")
f.circle(405, 52, 15, fill="#ffffff", stroke=RED, sw=2, label="R1", size=11, color=NAVY)
f.circle(285, 122, 15, fill="#ffffff", stroke=AMBER, sw=2, label="R2", size=11, color=NAVY)
f.circle(160, 192, 15, fill="#ffffff", stroke=TEAL, sw=2, label="R3", size=11, color=NAVY)
```

**Quantitative assessment** uses numbers: risk exposure and expected monetary value.

::: example Worked example: risk exposure and ranking
| Risk | Probability | Impact (Rs) | Exposure = P × impact | Rank |
|---|---|---|---|---|
| R1 Lead developer leaves | 0.30 | 200,000 | **60,000** | 1 |
| R2 Gateway API changes late | 0.10 | 500,000 | **50,000** | 2 |
| R3 Requirements change by 10% | 0.50 | 40,000 | **20,000** | 3 |

Total exposure = 130,000. This is a good size for a **contingency reserve**. Note that R2, though rare, ranks second because its impact is large, while R3 is the most likely but the least costly.
:::

### Step 3: Risk planning (responses)

For every significant risk choose a strategy:

| Strategy | Meaning | Example |
|---|---|---|
| **Avoid (prevent)** | change the plan so that the risk cannot occur | use a proven library instead of a new one |
| **Mitigate (reduce)** | lower the probability or the impact | train a second developer; document code; prototype the API first |
| **Transfer (share)** | shift the impact to a third party | insurance; fixed-price contract; outsource the payment module |
| **Accept** | do nothing in advance, perhaps with a **contingency plan** | accept small delays; agree a fallback if it occurs |
| **Exploit** (for opportunities) | make sure the positive risk happens | assign the best developer to a task that can finish early |

A **contingency plan** (the "plan B") and a **trigger** (an early-warning sign such as three missed stand-ups) are defined in advance. **Contingency reserve** (for known risks) and **management reserve** (for unknown unknowns) are kept in time and budget.

The value of a response is measured by **risk reduction leverage**: RRL = (RE<sub>before</sub> − RE<sub>after</sub>) / cost of the reduction. Responses with RRL above 1 are worth doing, and the highest values are done first.

::: example Worked example: risk reduction leverage
For R1 (lead developer leaves), RE before = 0.30 × 200,000 = Rs 60,000. Pair programming and documentation (cost Rs 10,000) cut the probability to 0.10, so RE after = 0.10 × 200,000 = Rs 20,000.
RRL = (60,000 − 20,000) / 10,000 = **4.0**. Each rupee spent removes four rupees of expected loss, so the response is clearly worthwhile.
:::

### Step 4: Risk monitoring and control

The **risk register** holds for each risk: ID, description (cause, event, effect), probability, impact, exposure, owner, response, trigger, status. It is reviewed at every weekly meeting or sprint review; risks are added, re-scored, closed or escalated. Lessons from risks that occurred are recorded for future projects.

## 5.3 Evaluating risks to the schedule

Schedule risk is the uncertainty in the completion date. Single-figure CPM durations hide it. Three approaches:

### Using PERT

With three-point estimates (Unit 2) the expected completion time T<sub>E</sub> and standard deviation σ<sub>T</sub> give the probability of meeting a target date. The PERT value is a lower bound: it counts only the critical path.

### Near-critical paths

When a second path is only slightly shorter than the critical path, either can determine the finish. The probability of finishing on time is roughly the **product** of the probabilities for each path (if they are independent).

::: example Worked example: two competing paths
Path 1 (critical): mean 18 weeks, σ = 2. Path 2 (near-critical): mean 17 weeks, σ = 4. Target = 20 weeks.
P(path 1 ≤ 20) = Φ((20 − 18)/2) = Φ(1.00) = **0.841**. P(path 2 ≤ 20) = Φ((20 − 17)/4) = Φ(0.75) = **0.773**.
P(project ≤ 20) ≈ 0.841 × 0.773 = **0.651**, not the 84.1% that the critical path alone suggests. Paths with little float add real schedule risk.
:::

### Monte Carlo simulation

Thousands of simulated runs of the network are made, each drawing random durations from the activity distributions; the proportion of runs finishing by a date gives the probability. It handles many paths, different distributions and correlations, and produces a **criticality index** (the percentage of runs in which an activity is on the critical path).

### Buffers and critical chain

Rather than padding every task (which Parkinson's law uses up), the **critical chain method** (Goldratt) removes padding from tasks and adds a single **project buffer** at the end, plus **feeding buffers** where non-critical chains join the critical chain. Buffer consumption is monitored as a signal of schedule health (green, amber, red).

## Formula and fact sheet

- Risk exposure RE = probability × impact; expected monetary value of a risk = P × loss.
- Total contingency reserve is about the sum of risk exposures of the accepted risks.
- RRL = (RE<sub>before</sub> − RE<sub>after</sub>) / cost of reduction; do responses with RRL greater than 1.
- Four responses to a threat: avoid, mitigate, transfer, accept (plus exploit for opportunities).
- Probability of meeting a date over several near-critical paths is about the product of the path probabilities.

## Chapter summary

- Risk is an uncertain event with probability and impact; exposure combines them. Categories include requirements, estimation, technology, people, organisation and external risks.
- The framework is identification, assessment, planning and monitoring, kept in a risk register and repeated throughout the project.
- Qualitative matrices and quantitative exposure rank risks; responses are avoid, mitigate, transfer or accept, supported by contingency plans and reserves.
- Schedule risk is assessed with PERT, near-critical paths, Monte Carlo simulation and buffers.

## Practice

1. Define risk. Distinguish a risk from an issue.
2. List and explain five categories of software project risks.
3. Explain the risk management framework with a diagram.
4. Describe four techniques of risk identification.
5. A risk has probability 0.2 and impact Rs 150,000. Find its exposure. A mitigation costing Rs 8,000 reduces the probability to 0.05. Compute the RRL.
6. Explain the four responses to risk with examples.
7. What is a risk register? List its contents.
8. Why does the critical-path PERT estimate usually overstate the chance of finishing on time?
9. Path 1: mean 30 days, σ = 3; path 2: mean 28 days, σ = 5. Target 33 days. Find the approximate probability of finishing in time. (Φ(1.00) = 0.8413, Φ(1.00) for path 2 is the same z.)
10. Write a risk statement in the form cause, event, effect for a team using a new framework.

::: note Answers and worked solutions
**1.** A risk is an uncertain event that, if it occurs, affects objectives; an issue is a risk that has already occurred and must be handled now.
**2.** Requirements (changes, ambiguity), estimation (optimism), technology (immature tools), people (turnover), external (supplier or law changes); each with an example.
**3.** Identify, assess, plan responses, monitor and control, with feedback and a risk register (figure 5.1).
**4.** Checklists, brainstorming, Delphi, SWOT and assumption analysis, review of lessons learned.
**5.** RE = 0.2 × 150,000 = **30,000**; after mitigation 0.05 × 150,000 = 7,500; RRL = (30,000 − 7,500)/8,000 = **2.81**, so worthwhile.
**6.** Avoid (use proven technology), mitigate (train backups), transfer (fixed-price contract or insurance), accept (small delay with a contingency plan).
**7.** A live log of risks: ID, description, probability, impact, exposure, owner, response, trigger, status.
**8.** It looks only at the critical path; other paths with small float can also delay completion, so the true probability is lower.
**9.** Path 1: z = (33 − 30)/3 = 1.00, P = 0.841. Path 2: z = (33 − 28)/5 = 1.00, P = 0.841. Combined ≈ 0.841 × 0.841 = **0.708**.
**10.** "Because the team has never used the framework (cause), the first module may take twice as long (event), which would delay the first release by three weeks (effect)."
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). What is risk management? Explain the framework for dealing with risk.**

*Introduction.* Risk management is the systematic process of identifying, assessing, planning for and monitoring uncertain events that could affect a project.

*Framework.*

1. **Identification:** find risks by checklists, brainstorming, Delphi, SWOT and lessons learned, and record each as cause, event, effect.
2. **Assessment:** estimate probability and impact; rank by exposure (P × impact) using a matrix.
3. **Planning:** select a response (avoid, mitigate, transfer, accept) and write contingency plans and triggers; set aside reserves.
4. **Monitoring and control:** review the risk register regularly, track triggers, close old risks and add new ones.

*Conclusion.* The cycle repeats throughout the project, so that surprises are fewer and the response is early.

**Q2 (10 marks). Explain the categories of software project risk and describe how risks are assessed and responded to, with a numerical example.**

*Introduction.* Software projects face uncertainty from many sources; classifying and quantifying risks lets the manager spend effort where it matters.

*Categories.* Requirements, estimation and schedule, technology, people, organisational, external, quality and security, and contractual risks.

*Assessment.* Qualitative: a probability-impact matrix. Quantitative: exposure = probability × impact. For example R1 (developer leaves, 0.3 × Rs 200,000 = Rs 60,000), R2 (API change, 0.1 × 500,000 = 50,000) and R3 (requirements change, 0.5 × 40,000 = 20,000); the total exposure of Rs 130,000 sets the contingency reserve.

*Response.* Avoid, mitigate, transfer or accept. Mitigating R1 by pair programming at Rs 10,000 reduces exposure from 60,000 to 20,000, an RRL of 4.0, so it is justified.

| Risk | Exposure | Response |
|---|---|---|
| R1 developer leaves | 60,000 | mitigate (pairing, documentation) |
| R2 API change | 50,000 | transfer or mitigate (adapter layer, vendor agreement) |
| R3 requirements change | 20,000 | accept with change control |

*Conclusion.* Risk management turns vague worries into ranked, owned and funded actions.
