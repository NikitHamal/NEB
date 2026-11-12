---
subject: Software Project Management
grade: BCA Semester 7
unit: 4
title: Software Evaluation and Costing
hours: 8
area: BCA 402 · Software Project Management · Unit 4
---

An organisation has more project ideas than money. A bank may want a mobile app, a new loan system and a data warehouse in the same year, yet it can afford one or two. **Project evaluation** is the process of deciding, before heavy spending, whether a project is worth doing and which of several candidates to do first. This unit covers strategic, technical and economic assessment, the cost-benefit techniques (NPV, IRR, payback, ROI), the evaluation of risk, and the choice of an appropriate project approach.

::: key What this unit gives you
- Strategic and technical assessment, including a weighted scoring model.
- Cost-benefit analysis, cash flow forecasting and the four evaluation techniques with numerical examples.
- Risk evaluation: sensitivity analysis, expected value and risk-adjusted rates.
- Selecting an appropriate project report and project approach: choosing technologies, process models and structured methods.
:::

## 4.1 Project evaluation: strategic and technical assessment

Evaluation is done in three layers: **strategic** (does the project fit the organisation?), **technical** (can we build it?) and **economic** (is it worth the cost?). It happens at the start (the feasibility study) and again at stage gates during the project.

### Strategic assessment

Strategic assessment checks whether a project supports the organisation's objectives and its **information systems strategy**. The organisation compares candidate projects on:

- **Programme management.** Several projects form a *programme* with a common business goal; a project that supports it is preferred.
- **Strategic fit:** does it support the mission (for example more customers, lower cost, regulatory compliance)?
- **Portfolio management.** The portfolio balances risk and return, short-term and long-term, new and maintenance work.
- **Dependencies:** it may need infrastructure that another project is building.

### Technical assessment

Technical assessment asks whether the required functionality can be delivered with the available hardware and software, **and** whether the organisation has the skills. It compares the proposed solution with the technical constraints (performance, security, compatibility with legacy systems) and the cost of the hardware and software. It supplies the *cost side* for the economic analysis.

### Weighted scoring

When several options must be compared on non-money criteria, assign each criterion a **weight** (summing to 1) and each option a **score** (for example 0 to 10); the option with the highest weighted total wins.

::: example Worked example: choosing a payment platform
| Criterion | Weight | Option A score | Option B score |
|---|---|---|---|
| Fit with requirements | 0.40 | 8 | 6 |
| Security | 0.30 | 6 | 9 |
| Cost | 0.20 | 7 | 8 |
| Local vendor support | 0.10 | 9 | 7 |
| **Weighted total** | **1.00** | 0.4 × 8 + 0.3 × 6 + 0.2 × 7 + 0.1 × 9 = **7.3** | 0.4 × 6 + 0.3 × 9 + 0.2 × 8 + 0.1 × 7 = **7.4** |

B wins by only 0.1. The decision is **sensitive to the weights**: if "fit with requirements" is weighted 0.5 and "security" 0.2 (the other weights unchanged), A scores 7.5 and B only 7.1, so A wins. Always test how the ranking changes when weights are varied.
:::

## 4.2 Cost-benefit analysis

**Cost-benefit analysis (CBA)** compares the expected costs of a project with its expected benefits, over its useful life, to decide whether it is worthwhile. Two steps: (1) identify and estimate all costs and benefits, and (2) express them in the same unit (money) and compare.

### Costs

| Type | Examples |
|---|---|
| **Development costs** | salaries of analysts, programmers and testers; training |
| **Set-up costs** | hardware, licences, network, data conversion, site preparation |
| **Operating costs** | hosting, support staff, maintenance, upgrades, electricity |
| **Hidden costs** | disruption during the transition, lost productivity while users learn |

### Benefits

| Type | Meaning | Example |
|---|---|---|
| **Direct benefits** | accrue directly from use and are easily valued | savings from fewer clerks |
| **Assessable indirect benefits** | secondary but can be valued with some effort | fewer errors that would have needed rework |
| **Intangible benefits** | real but hard to quantify | better customer satisfaction, reputation, staff morale |

Intangible benefits should not be ignored; assign a conservative estimated value or describe them separately in the report.

## 4.3 Cash flow forecasting

A **cash flow forecast** shows the expected inflows and outflows of money over time. For software, most **costs come first** (development), and **benefits arrive later** (after delivery), so the early years show negative **net cash flow**.

::: example Worked example: cash flow forecast
A project costs Rs 100,000 now (year 0). Net benefits (savings less operating costs) are Rs 30,000, 40,000, 50,000 and 30,000 in years 1 to 4.

| Year | Net cash flow | Cumulative |
|---|---|---|
| 0 | −100,000 | −100,000 |
| 1 | +30,000 | −70,000 |
| 2 | +40,000 | −30,000 |
| 3 | +50,000 | +20,000 |
| 4 | +30,000 | +50,000 |

The cumulative cash flow crosses zero during year 3: the project **pays back** its cost and ends with a net surplus of Rs 50,000 (undiscounted).
:::

```svgfig label="4.1" caption="Cumulative cash flow (Rs thousand) for the worked example. The line crosses zero between years 2 and 3: the payback point."
f = Fig(600, 260)
x0, y0, sx, sy = 70, 150, 100, 1.1
f.line(40, y0, 560, y0, color=SLATE, sw=1.5)
f.line(x0, 20, x0, 240, color=SLATE, sw=1.5)
vals = [-100, -70, -30, 20, 50]
pts = [(x0 + i * sx, y0 - v * sy) for i, v in enumerate(vals)]
for i in range(len(pts) - 1):
    f.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], color=TEAL, sw=2.6)
for i, (x, y) in enumerate(pts):
    f.circle(x, y, 5, fill="#fde68a", stroke=AMBER, sw=1.6)
    f.text(x, y0 + 16 if vals[i] > 0 else y0 - 8, "Year " + str(i), size=10.5, color=SLATE)
    f.text(x + 4, y - 10 if vals[i] > 0 else y + 18, str(vals[i]), size=10.5, color=NAVY, bold=True)
f.text(x0 + 2.6 * sx, y0 + 30, "payback at about 2.6 years", size=11, color=RED, bold=True)
```

## 4.4 Cost-benefit evaluation techniques

### 1. Net profit

**Net profit** = total income − total costs over the life, undiscounted. In the example, 150,000 − 100,000 = **Rs 50,000**. It is simple but ignores the timing of money and the size of the investment.

### 2. Payback period

The **payback period** is the time taken for cumulative net cash flow to reach zero. Using the table: after year 2 the shortfall is 30,000, and year 3 brings 50,000, so payback = 2 + 30,000/50,000 = **2.6 years**. Simple and favoured by risk-averse managers (shorter means less exposure), but it ignores everything after payback and the time value of money.

### 3. Return on investment (ROI) or accounting rate of return

**ROI** = (average annual profit ÷ total investment) × 100. Average annual net profit = 50,000/4 = 12,500, so ROI = 12,500 / 100,000 = **12.5% per year** (50% over the four years in total). It is easy to compute, but it ignores timing and the choice of "average" can mislead.

### 4. Net present value (NPV)

Money received later is worth less than money today because it could be invested (and because of inflation and risk). The **discount rate** r reflects this. The **present value** of an amount C received in year t is PV = C / (1 + r)<sup>t</sup>; the **discount factor** is 1/(1 + r)<sup>t</sup>. **NPV** is the sum of the present values of all cash flows, including the initial investment:

**NPV = Σ C<sub>t</sub> / (1 + r)<sup>t</sup>** (t = 0 to n). **Accept** a project if NPV > 0 (and choose the highest NPV among alternatives of similar size).

::: example Worked example: NPV at 10%
| Year | Cash flow | Discount factor at 10% | Present value |
|---|---|---|---|
| 0 | −100,000 | 1.0000 | −100,000 |
| 1 | 30,000 | 0.9091 | 27,273 |
| 2 | 40,000 | 0.8264 | 33,058 |
| 3 | 50,000 | 0.7513 | 37,566 |
| 4 | 30,000 | 0.6830 | 20,490 |
| **NPV** | | | **+18,387** |

The present value of the benefits is 118,387 against a cost of 100,000. NPV is positive, so the project **earns more than the 10% required** and should be accepted on this test.
:::

### 5. Internal rate of return (IRR)

The **IRR** is the discount rate at which NPV = 0, found by trial and interpolation (or a spreadsheet function `=IRR()`). Accept a project if IRR is greater than the required rate (the **hurdle rate**). For the example NPV is +18,387 at 10%; at 20% it is about −3,800; interpolation puts the IRR close to **18%**, which exceeds 10%, so the project is acceptable.

| Technique | Considers time value of money? | Considers cash flows after payback? | Decision rule |
|---|---|---|---|
| Net profit | no | yes | positive and highest |
| Payback | no | no | shorter than the target period |
| ROI / ARR | no | yes (averaged) | higher than the target |
| NPV | yes | yes | NPV > 0, highest |
| IRR | yes | yes | IRR > hurdle rate |

NPV is preferred by finance experts because it is a money amount and **additive**; IRR is popular because it gives a percentage, but it can mislead when comparing projects of different sizes or when cash flows change sign several times.

## 4.5 Risk evaluation

All the figures above are *forecasts*; actual benefits may be lower or arrive later. Risk evaluation looks at what could go wrong with the numbers.

### Risk identification and ranking

List the risks (changing requirements, new technology, supplier failure, staff loss), assess **probability** and **impact**, and rank them by **risk exposure = probability × impact**. Unit 5 deals with managing them; here the aim is to adjust the project's value.

### Sensitivity analysis

Change one input at a time and see how the result moves. If the benefits are **20% lower** than forecast, the PV of benefits falls to 0.8 × 118,387 = 94,710 and NPV becomes **−5,290**: the decision flips. The project is therefore *sensitive* to its benefit forecast, so the manager should look hard at that figure.

### Expected value (decision tree) approach

Attach probabilities to scenarios and compute the **expected NPV**: with a 25% chance of a pessimistic outcome (NPV −20,000), 50% of the likely outcome (+18,387) and 25% optimistic (+50,000), expected NPV = −5,000 + 9,194 + 12,500 = **+16,694**.

### Risk-adjusted discount rate and certainty equivalents

A risky project is discounted at a **higher rate** (for example 10% plus a risk premium of 5% for a new technology = 15%), so uncertain future benefits count for less. Another method reduces each forecast to a **certainty equivalent** (the sure amount the company would accept instead).

### Risk profile and Monte Carlo simulation

A **risk profile** (probability distribution of NPV) is built by running a **Monte Carlo simulation**: each uncertain input is drawn from a distribution thousands of times, and the spread of NPV shows the probability of loss.

::: note Good practice in evaluation
Use more than one technique (payback for liquidity, NPV for value); state assumptions (discount rate, life, growth); show a sensitivity table; include intangible benefits separately; and re-evaluate at each stage gate.
:::

## 4.6 Selection of an appropriate project report

After the evaluation, the findings are written up in a **project report** (feasibility report or business case), which the sponsor reads to decide whether to proceed. The report is *selected and tailored* to its readers: an executive needs a short summary and the financial case; the technical board needs architecture and risks. A typical structure:

1. **Executive summary:** the problem, the recommended option and the headline figures.
2. **Background and objectives:** why the project is needed and how success will be measured.
3. **Options considered** (including "do nothing") with a short comparison.
4. **Technical assessment:** approach, technology, constraints.
5. **Cost-benefit analysis:** cost and benefit tables, cash flow, NPV, IRR, payback.
6. **Risk assessment** with sensitivity analysis.
7. **Implementation plan:** high-level schedule, resources, milestones.
8. **Recommendation** and the decision required, with appendices for detail.

Good reports are honest about assumptions and uncertainties; a report which shows only the favourable case is a sign of a project that will later be judged unfairly.

## 4.7 Project approach: choosing technologies and process models

The **project approach** answers *how* the software will be built. It is chosen in step 3 of the Step Wise framework after analysing the project's characteristics.

### Build or buy?

| Option | Advantage | Disadvantage |
|---|---|---|
| **Build** (bespoke) | exact fit; full control; competitive advantage | expensive, slow, risk of failure, maintenance burden |
| **Buy** (off-the-shelf or SaaS) | quick; cheaper; proven; vendor support | less fit; licences; dependency on the vendor; customisation limits |
| **Customise** an existing framework or ERP | compromise on cost and fit | complexity; upgrade problems |
| **Outsource** | skills and capacity; cost | communication and contract risk, loss of knowledge |
| **Open source** | no licence fee; community | support risk, integration effort |

### Choosing technologies

The choice of language, framework, database and platform follows from the **problem** (data-intensive, real-time, mobile), the **organisation** (existing skills, infrastructure, standards) and the **product** (performance, security, expected life). Questions to ask: Does a suitable **structured method** (for example SSADM, Yourdon) or an **object-oriented method** (UML) exist? Is there a CASE tool? Is the team trained? Is the technology mature and supported in Nepal? Is it new (high risk) or proven? Prototype any *new* technology on a small piece before committing the plan to it.

### Software processes and process models

A **software process** is the set of activities by which software is built; a **process model** is an abstract description of it. The main models, and the project characteristics that favour each:

| Model | Idea | Suits | Weakness |
|---|---|---|---|
| **Waterfall** | linear: requirements, design, code, test, deploy; each stage completed and signed off before the next | stable, well-understood requirements; regulated projects | late feedback; changes are costly; working software appears at the end |
| **V-model** | waterfall with a test level mapped to each development stage | safety-critical systems with clear verification | same rigidity as waterfall |
| **Prototyping** | build a quick model to clarify requirements, then discard or evolve it | unclear requirements; UI-heavy systems | users may demand to "just finish" the throw-away prototype |
| **Incremental delivery** | deliver the system in successive working increments | early value needed; a core system with later add-ons | needs a good architecture up front |
| **Spiral** (Boehm) | repeated cycles of planning, risk analysis, engineering and evaluation | large, high-risk projects | needs risk expertise; costly |
| **RAD / DSDM (Atern)** | time-boxed iterations, heavy user involvement, prototypes, fixed time with flexible scope | business systems that can be modularised | needs committed users |
| **Agile (Scrum, XP, Kanban)** | short sprints, working software each iteration, changing requirements welcomed, self-organising teams | uncertain or fast-changing requirements, small to medium teams | harder to fix price and scope; needs discipline |
| **Unified Process / iterative** | iterate through inception, elaboration, construction, transition | object-oriented medium to large systems | process overhead |

### Structure versus speed of delivery

Process models sit on a spectrum. **Structured** approaches (waterfall, V-model) give predictability, documentation and control, and suit large, safety-critical or contract-driven projects where rework is expensive. **Fast** approaches (RAD, agile) give early delivery and tolerance to change, and suit projects where speed to market and uncertain needs dominate. Projects with *high uncertainty about requirements* favour prototyping and iteration; projects with *high uncertainty about technology* favour a spiral approach or early prototypes of the risky part; stable requirements and a known technology favour a plan-driven model.

```svgfig label="4.2" caption="Choosing a process model by two uncertainties: of the requirements and of the technology. High-risk quadrants call for iteration and prototyping."
f = Fig(560, 270)
f.line(70, 20, 70, 230, color=SLATE, sw=1.6)
f.line(70, 230, 530, 230, color=SLATE, sw=1.6)
f.text(300, 255, "Technology uncertainty (low to high)", size=11, color=NAVY, bold=True)
f.text(20, 125, "Req.", size=11, color=NAVY, bold=True)
f.text(20, 140, "unc.", size=11, color=NAVY, bold=True)
f.box(80, 28, 200, 90, "Prototyping, then\nincremental delivery\n(clarify what to build)", fill=BLUE, color=NAVY, size=11, bold=True)
f.box(290, 28, 230, 90, "Spiral or agile with\nearly risk spikes\n(unknown what and how)", fill="#fecaca", stroke=RED, color=NAVY, size=11, bold=True)
f.box(80, 128, 200, 92, "Waterfall or V-model\n(plan-driven, predictable)", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=11, bold=True)
f.box(290, 128, 230, 92, "Incremental with a\ntechnical prototype\n(prove the technology first)", fill="#fde68a", stroke=AMBER, color=NAVY, size=11, bold=True)
```

### Agile in brief: Scrum and Extreme Programming

**Scrum** organises work in **sprints** of two to four weeks. Roles: Product Owner (priorities), Scrum Master (process coach), Development Team. Artefacts: product backlog, sprint backlog, increment. Events: sprint planning, daily stand-up, sprint review, retrospective. **Extreme Programming (XP)** adds engineering practices: pair programming, test-driven development, continuous integration, refactoring, small releases, collective code ownership. The **Agile Manifesto** (2001) values individuals and interactions, working software, customer collaboration and responding to change, over their counterparts.

### Structured methods

A **structured method** gives a standard set of techniques and notations for analysis and design: **data flow diagrams**, **entity-relationship models**, structure charts, decision tables and a defined sequence of steps. Examples are SSADM and Yourdon. *Benefits:* a common language, consistent documentation, easier maintenance, and a basis for estimation. *Costs:* training, overhead, rigidity. For object-oriented systems the counterpart is UML-based development.

## Formula and fact sheet

- NPV = Σ C<sub>t</sub> / (1 + r)<sup>t</sup>; accept if NPV > 0. IRR is the r that makes NPV = 0; accept if IRR > hurdle rate.
- Payback = last negative year + (unrecovered amount ÷ next year's inflow). ROI = average annual profit ÷ investment.
- Risk exposure = probability × impact; expected NPV = Σ (probability × NPV).
- Weighted score = Σ (weight × score) for each option.
- Benefits: direct, assessable indirect, intangible. Costs: development, set-up, operating.

## Chapter summary

- Evaluation asks if a project is strategically aligned, technically feasible and economically worthwhile.
- CBA lists costs and benefits; a cash flow forecast shows when they occur; NPV and IRR use the time value of money, payback and ROI do not.
- Risk evaluation uses sensitivity analysis, expected values and risk-adjusted discount rates.
- The project report presents the findings to the sponsor in a structure suited to its readers.
- The project approach covers build-or-buy, technology choice and process model; the right model depends on requirement and technology uncertainty.

## Practice

1. Explain strategic and technical assessment of a project.
2. Differentiate direct, indirect and intangible benefits with examples.
3. A project costs Rs 200,000 and returns Rs 80,000, 90,000 and 100,000 in years 1 to 3. Find the payback period and net profit.
4. For the data in question 3 compute NPV at 12% (discount factors 0.8929, 0.7972, 0.7118).
5. Explain IRR. When is a project accepted on the IRR rule?
6. Why is NPV considered better than payback and ROI?
7. What is sensitivity analysis? Give an example of its use.
8. Explain Build vs Buy with advantages and disadvantages.
9. Compare waterfall, prototyping, spiral and agile models in a table.
10. What is a structured method? List its advantages.

::: note Answers and worked solutions
**1.** Strategic: fit with organisational goals and information strategy, programme and portfolio fit. Technical: whether the required functionality can be delivered with the hardware, software and skills available, and at what cost.
**2.** Direct: savings in staff time; indirect: fewer errors leading to less rework; intangible: customer satisfaction and brand image.
**3.** Cumulative: −200,000; −120,000; −30,000; +70,000. Payback = 2 + 30,000/100,000 = **2.3 years**. Net profit = 270,000 − 200,000 = **Rs 70,000**.
**4.** PV = 80,000 × 0.8929 + 90,000 × 0.7972 + 100,000 × 0.7118 = 71,432 + 71,748 + 71,180 = 214,360; NPV = **+14,360** (accept).
**5.** IRR is the discount rate at which NPV is zero. Accept if IRR exceeds the required (hurdle) rate.
**6.** NPV accounts for the time value of money and all cash flows over the project's life and gives the absolute value added, while payback ignores benefits after payback and ROI ignores timing.
**7.** Vary one input and see the effect on NPV: a 20% lower benefit changes NPV of the worked example from +18,387 to −5,290.
**8.** Build: exact fit and control but high cost and risk. Buy: fast and cheaper but less fit and dependence on the vendor.
**9.** See the process model table: waterfall linear, prototyping for unclear requirements, spiral risk-driven, agile iterative and adaptive.
**10.** A defined set of techniques and notations (DFD, ERD) and steps for analysis and design; advantages: common language, consistent documentation, easier maintenance and estimation.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain cost-benefit evaluation techniques.**

*Introduction.* Cost-benefit evaluation compares the expected costs and benefits of a project to decide whether it is worth doing.

*Techniques.*

1. **Net profit:** total income less total cost; simple but ignores timing.
2. **Payback period:** the time for cumulative cash flow to reach zero; quick but ignores later flows and the time value of money.
3. **ROI:** average annual profit divided by investment.
4. **NPV:** discounts every cash flow at the required rate, NPV = Σ C<sub>t</sub>/(1 + r)<sup>t</sup>; accept if positive.
5. **IRR:** the discount rate that makes NPV zero; accept if above the hurdle rate.

*Example.* For cash flows −100,000, 30,000, 40,000, 50,000, 30,000 the payback is 2.6 years, ROI is 12.5% per year, NPV at 10% is +18,387 and IRR is about 18%.

*Conclusion.* NPV and IRR are preferred because they include the time value of money; payback is often added as a measure of liquidity risk.

**Q2 (10 marks). Describe the process models from which a project manager can choose and explain how the choice is made.**

*Introduction.* The process model defines the order and rhythm of development activities; choosing the wrong one is a major source of failure.

*Models.* Waterfall (linear, plan-driven), V-model (testing mapped to each stage), prototyping (to clarify requirements), incremental delivery (core first, add-ons later), spiral (risk-driven cycles), RAD and DSDM (time-boxed with user involvement) and agile methods such as Scrum and XP (short sprints, adaptive).

| Situation | Suitable model |
|---|---|
| Stable requirements, known technology | waterfall or V-model |
| Unclear requirements | prototyping, agile |
| New technology, high risk | spiral, with early technical prototype |
| Early value needed | incremental, RAD |
| Fast-changing market | agile |

*Making the choice.* Analyse the **project characteristics**: uncertainty about requirements and technology, size, criticality, team experience, customer availability, contractual form (fixed price favours plan-driven). Use the matrix of requirement uncertainty against technology uncertainty; a hybrid is common (waterfall for the stable core, agile for the user-facing part).

*Conclusion.* No model is best for all projects: the manager matches structure and speed of delivery to the project's risks.
