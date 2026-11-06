---
subject: System Analysis and Design
grade: BCA Semester 3
unit: 2
title: Planning
hours: 7
area: BCA 204 · System Analysis and Design · Unit 2
---

Most systems projects fail not in coding but at the start: the wrong project, unclear scope, no business case. **Planning** answers *should we do this, and can we?* before money is committed.

::: key What this unit gives you
- Identifying and selecting projects; corporate and IS planning.
- Initiating and planning a project: scope, the baseline project plan.
- The five feasibility tests, with a worked cost–benefit analysis (NPV, ROI, payback).
- Reviewing the plan.
:::

## 2.1 Identifying and selecting systems development projects

**Sources of projects:** requests from management (strategic), from departments (operational problems), from IT staff (technology refresh), and from external forces (new law, competitors, partners). A **steering committee** of senior managers reviews proposals.

**Selection criteria.** Rate each candidate on: **value chain** analysis (does it improve a key activity such as ordering or service?), strategic alignment, potential benefits, resource availability, project size and duration, technical difficulty and risk. A **weighted scoring** table makes the choice explicit.

::: example Worked example: weighted scoring
Criteria weights: strategic fit 40%, benefit 30%, cost (lower is better, scored inversely) 20%, risk (lower better) 10%. Project X scores 8, 7, 5, 6; project Y scores 6, 9, 8, 8 (all out of 10).
X: 0.4·8 + 0.3·7 + 0.2·5 + 0.1·6 = 3.2 + 2.1 + 1.0 + 0.6 = **6.9**.
Y: 0.4·6 + 0.3·9 + 0.2·8 + 0.1·8 = 2.4 + 2.7 + 1.6 + 0.8 = **7.5**. Y is preferred despite lower strategic fit.
:::

## 2.2 Corporate and information systems planning

IS projects should support the organisation's strategy. Planning proceeds from **corporate strategic planning** (mission, objectives, competitive strategy) to **IS planning**: an inventory of existing systems, a statement of IS objectives, and an architecture and schedule of projects. Tools:

- **SWOT analysis:** strengths, weaknesses (internal); opportunities, threats (external).
- **Critical success factors (CSFs):** the few things that must go right (for a bank: customer trust, uptime), which tell the IS what information managers need.
- **Porter's value chain:** primary activities (inbound logistics, operations, outbound logistics, marketing/sales, service) and support activities (infrastructure, HR, technology, procurement); look for IS opportunities in each.
- **Business process reengineering (BPR)** and enterprise models that tie data, processes and organisation together.

## 2.3 Initiating and planning a project

**Process of initiating and planning:**

1. **Establish the project initiation team** (analyst, sponsor, business users).
2. **Establish a relationship with the customer** (a clear sponsor and contacts).
3. **Establish the project initiation plan**: a short description of the problem and the work to be done.
4. **Establish management procedures** (team roles, communication, reporting, change control).
5. **Establish the project management environment and project workbook** (a shared, current record of all project documents).
6. **Develop the project charter**: why the project exists, objectives, scope, deliverables, assumptions, constraints, sponsor and budget.

Then the **analyst defines the problem and scope** (what is in, what is out), identifies the **project's benefits**, estimates **resources** (people, time, money), considers **risks** and starts the **baseline project plan**.

## 2.4 Assessing project feasibility

A **feasibility study** asks whether the project is practical. Each of six tests can sink it:

| Feasibility | Question | Typical items |
|---|---|---|
| **Economic** (cost-benefit) | Do benefits exceed costs? | development and operating cost, tangible and intangible benefits |
| **Technical** | Can we build it with available technology and skills? | familiarity, size, compatibility, risk |
| **Operational** | Will it work in the organisation and will people use it? | user acceptance, fit with processes |
| **Schedule** | Can it be done in time? | deadlines, dependencies |
| **Legal and contractual** | Does it comply with law and contracts? | privacy, copyright, licence terms |
| **Political** | Will powerful stakeholders support it? | sponsorship, resistance |

**Costs:** one-time (hardware, software, development, training, data conversion) and recurring (maintenance, support, licences, hosting). **Benefits:** *tangible* (reduced staff time, fewer errors, more revenue) and *intangible* (satisfaction, goodwill, better decisions), which are listed and, where possible, given estimated values.

### Cost-benefit measures

- **Present value:** money later is worth less; PV = FV/(1 + r)ᵗ for discount rate r and year t.
- **Net present value (NPV):** sum of discounted benefits minus costs; accept if **NPV > 0**.
- **Return on investment (ROI):** (total benefits − total costs)/total costs.
- **Payback period:** time until cumulative net benefit equals the investment (simple or discounted).
- **Benefit–cost ratio (BCR):** PV of benefits ÷ PV of costs; accept if > 1.
- **Internal rate of return (IRR):** the discount rate making NPV = 0.

::: example Worked example: should the college buy a new result system?
Development cost **NPR 500,000** now (year 0); operating cost 100,000 a year; benefits 350,000 a year (saved staff hours, fewer errors) for 5 years; discount rate 10%.
Net annual benefit = 350,000 − 100,000 = **250,000**. The 5-year annuity factor at 10% is Σ 1/1.1ᵗ = **3.7908**.
**NPV** = −500,000 + 250,000 × 3.7908 = −500,000 + 947,697 = **+447,697** → accept.
**ROI** = (5 × 250,000 − 500,000)/500,000 = 750,000/500,000 = **150%** (undiscounted).
**Simple payback** = 500,000/250,000 = **2.0 years**. **Discounted payback:** cumulative discounted net benefit is 227,273 after year 1; 433,884 after year 2; 621,713 after year 3, so payback falls in year 3 at 2 + (500,000 − 433,884)/187,829 = **2.35 years**.
**BCR** = PV(benefits)/PV(costs) = (350,000 × 3.7908)/(500,000 + 100,000 × 3.7908) = 1,326,775/879,079 = **1.51**. **IRR ≈ 41%**, far above the 10% rate. All measures say go; the real risks are whether the benefits materialise.
:::

**Sensitivity analysis** repeats the calculation with pessimistic numbers (benefits 25% lower, cost 25% higher) to see whether the decision survives.

```photogrid label="2.1" cols="2" ratio="1.2" caption="Cost and time estimates can be wrong by a factor of ten. (a) Sydney Opera House: approved in 1959 with an estimate of 7 million Australian dollars and a four-year build (finish 1963); it opened in 1973 at 102 million, which is 14.6 times the estimate (an overrun of 1,357 per cent) and 3.5 times the planned duration. (b) The college result system of Section 2.4 has development cost NPR 500,000 and a discounted net benefit of NPR 947,697 over five years, so its NPV stays positive until the cost has grown by 947,697 / 500,000 - 1 = 89.5 per cent. A feasibility study therefore asks two questions: is the NPV positive, and how large an overrun can it survive? Sensitivity analysis with a pessimistic case answers the second; the Opera House had no such margin."
@ photo id="bcasad/opera" cap="Sydney Opera House, finished 1973"
fit 1.2
focus 0.5 0.5
@ svg cap="Planned against actual, and the safety margin"
plan_c, act_c, plan_t, act_t = 7, 102, 1963 - 1959, 1973 - 1959
margin = 947697 / 500000 - 1
assert round(act_c / plan_c, 1) == 14.6 and round((act_c / plan_c - 1) * 100) == 1357
assert round(act_t / plan_t, 1) == 3.5 and round(margin * 100, 1) == 89.5
f = Fig(300, 240)
f.text(150, 14, "Sydney Opera House (1959 start)", size=10.5, color=NAVY, bold=True)
def pair(y, lab, a, b, unit_):
    f.text(8, y, lab, size=10.5, color=SLATE, anchor="start", bold=True)
    for k, (v, col, nm) in enumerate([(a, TEAL, "plan"), (b, RED, "actual")]):
        w = 150 * v / b
        f.box(60, y + 8 + k * 20, w, 15, "", fill=col, stroke=col, r=0)
        f.text(60 + w + 5, y + 16 + k * 20, f"{v} {unit_} ({nm})", size=10.5, color=NAVY, anchor="start", vmid=True)
pair(34, "Cost (AUD million)", plan_c, act_c, "M")
pair(98, "Years", plan_t, act_t, "yr")
f.box(10, 160, 280, 64, "", fill="#f1f5f9", stroke=SLATE, r=6, sw=1)
f.text(150, 178, "College result system: NPV > 0 until", size=10.5, color=NAVY, bold=True)
f.text(150, 196, "cost overrun reaches 89.5%", size=10.5, color=TEAL, bold=True)
f.text(150, 214, "Opera House overran 1,357%", size=10.5, color=RED, bold=True)
```

## 2.5 Building and reviewing the baseline project plan

The **Baseline Project Plan (BPP)** is the major deliverable of planning: the best current estimate of scope, benefits, costs, risks and resources, which later phases are measured against. Typical contents:

- **Introduction:** project overview, recommendation.
- **System description:** the business problem and a high-level view of alternatives and the recommended approach.
- **Feasibility assessment** (the six tests) and the cost-benefit analysis.
- **Management issues:** team composition, communication plan, project schedule, standards and procedures, risks.

It is reviewed in a **structured walkthrough**: the author presents the plan to peers and users, who look for omissions and errors (not to judge the author). Roles: coordinator, presenter, user representative, secretary, standards bearer. The outcome is approve, approve with changes, or reject; the sponsor and steering committee give final go/no-go.

## 2.6 Seeing the payback, and planning the schedule

Numbers in a cost-benefit table are easier to trust when they are drawn. Figure 2.1 plots the cumulative discounted net benefit of the college result system from Section 2.4. The project starts at −NPR 500,000 (the development cost). Each year adds a smaller discounted benefit, so the curve rises more slowly than a straight line, and it crosses zero between years 2 and 3: that crossing is the **discounted payback period** of about 2.35 years. By year 5 the curve ends at +447,697, which is the NPV. Figure 2.2 shows the other half of the baseline project plan, the schedule, as a Gantt chart drawn to scale.

```svgfig label="2.1" caption="Cumulative discounted net benefit of the result system (thousand NPR, 10% discount rate). The curve crosses zero at about 2.35 years (discounted payback) and ends at +447.7 thousand (the NPV)."
f = Fig(600, 260)
ax = Axes(f, 60, 20, 500, 190, (0, 5), (-550, 500))
ax.grid(1, 100).axes("year", "thousand NPR")
vals = [-500, -273, -66, 122, 292, 448]
ax.curve(lambda x: -500 + 250 * sum(1 / 1.1 ** t for t in range(1, int(x) + 1)) + (250 / 1.1 ** (int(x) + 1)) * (x - int(x)) if x < 5 else 447.7, 0, 5, color=NAVY, n=400)
for t, v in enumerate(vals):
    ax.pt(t, v, str(v), color=TEAL if v >= 0 else RED, dy=-10 if v >= 0 else 14, anchor="middle")
ax.hline(0, color=SLATE, dash=False, sw=1)
ax.vline(2.35, color=AMBER)
ax.tag(ax.X(2.35) + 6, ax.Y(-420), "payback 2.35 yr", size=11, color=AMBER, bold=True, anchor="start")
```

```svgfig label="2.2" caption="Gantt chart of the baseline project plan, drawn to scale (one column = one week, 10 weeks). Analysis cannot start until planning ends, but coding and test planning overlap; the critical path is planning, analysis, design, coding, testing."
f = Fig(600, 230)
tasks = [("Planning", 0, 1.5, BLUE), ("Analysis", 1.5, 3, "#fde68a"), ("Design", 3, 5, "#bbf7d0"), ("Coding", 5, 8, "#fbcfe8"), ("Test planning", 5, 7, "#e2e8f0"), ("Testing", 8, 9.5, "#fecaca"), ("Training", 8.5, 10, "#ddd6fe")]
x0, w = 120, 460
for k in range(11):
    f.line(x0 + k * w / 10, 22, x0 + k * w / 10, 205, color="#e2e8f0", sw=1)
    f.text(x0 + k * w / 10, 14, str(k), size=10, color=SLATE)
for i, (n, a, b, c) in enumerate(tasks):
    y = 28 + i * 25
    f.text(112, y + 9, n, size=10.5, color=NAVY, anchor="end", bold=True, vmid=True)
    f.box(x0 + a * w / 10, y, (b - a) * w / 10, 18, "", fill=c, stroke=NAVY)
f.text(350, 222, "weeks", size=10, color=SLATE)
```

```photogrid label="2.2" cols="2" ratio="1.0" caption="Critical path method (CPM) on a simplified plan. (a) Henry L. Gantt (1861-1919), the engineer who introduced the bar chart used for scheduling. (b) Seven tasks in whole weeks: Planning 2, Analysis 2 (after Planning), Design 2 (after Analysis), Coding 3 and Test planning 2 (both after Design), Testing 2 (after Coding and Test planning) and Training 1 (after Coding). A forward pass gives each task's earliest start and finish; a backward pass from the 11-week deadline gives the latest finish; the difference is slack. Planning, Analysis, Design, Coding and Testing have zero slack, so they form the critical path of 2 + 2 + 2 + 3 + 2 = 11 weeks, and a one-week delay to any of them delays the whole project. Test planning and Training each have one week of slack, so they can slip a week without harm."
@ photo id="bcasad/gantt" cap="Henry L. Gantt, scheduling pioneer"
fit 1.0
focus 0.5 0.3
@ svg cap="Forward and backward pass, slack in pale boxes"
T = [("Planning", 2, []), ("Analysis", 2, [0]), ("Design", 2, [1]), ("Coding", 3, [2]), ("Test plan", 2, [2]), ("Testing", 2, [3, 4]), ("Training", 1, [3])]
es, ef = [], []
for n, d, p in T:
    s = max([ef[i] for i in p], default=0); es.append(s); ef.append(s + d)
L = max(ef); lf = [L] * len(T)
for i in range(len(T) - 1, -1, -1):
    succ = [j for j, t in enumerate(T) if i in t[2]]
    lf[i] = min([lf[j] - T[j][1] for j in succ], default=L)
slack = [lf[i] - ef[i] for i in range(len(T))]
assert L == 11 and slack == [0, 0, 0, 0, 1, 0, 1] and es == [0, 2, 4, 6, 6, 9, 9]
f = Fig(300, 240)
x0, sc = 72, 20
f.text(150, 12, "weeks (red = critical, pale = slack)", size=10.5, color=SLATE)
for k in range(0, 12, 2):
    f.line(x0 + k * sc, 22, x0 + k * sc, 196, color="#e2e8f0", sw=1)
    f.text(x0 + k * sc, 208, str(k), size=10.5, color=SLATE)
for i, (n, d, p) in enumerate(T):
    y = 28 + i * 24
    f.text(66, y + 9, n, size=10.5, color=NAVY, anchor="end", bold=True, vmid=True)
    if slack[i]:
        f.box(x0 + ef[i] * sc, y, slack[i] * sc, 18, "", fill="#f1f5f9", stroke=SLATE, r=0, sw=1)
    crit = slack[i] == 0
    f.box(x0 + es[i] * sc, y, d * sc, 18, "", fill="#fecaca" if crit else "#bfdbfe", stroke=RED if crit else NAVY, r=0, sw=1.2)
f.text(150, 228, "critical path: 2 + 2 + 2 + 3 + 2 = 11 weeks", size=10.5, color=RED, bold=True)
```

## 2.7 Eight reasons to do a feasibility study first

1. **Avoids wasted money.** A study can show that the cost is higher than the benefit before any money is committed. The result-system example is clearly worth building (NPV positive), but a similar study of another idea may say stop.
2. **Tests the technology.** Technical feasibility asks whether the team knows the tools and whether the hardware and network are adequate. A rural campus with weak internet may need an offline-first design.
3. **Checks that people will use it.** Operational feasibility looks at staff skills, habits and resistance. A system that nobody accepts has zero benefit, however good the code is.
4. **Sets a realistic schedule.** Schedule feasibility compares the work with the deadline, for example whether a results portal can be ready before the examination month. It prevents promises that cannot be kept.
5. **Finds legal problems early.** Privacy, copyright, licence terms and contracts are checked before building. Student data, for example, must be protected as required by Nepalese law and university rules.
6. **Wins or loses support.** Political feasibility identifies who sponsors the project and who might resist it. A project with no senior sponsor often dies halfway.
7. **Compares alternatives.** Several options, such as build, buy or outsource, are measured with the same criteria. Management then chooses with evidence instead of opinion.
8. **Creates the baseline plan.** The study ends with scope, budget, schedule and risks written down. Later, progress is measured against this baseline.

## Formula and fact sheet

- Feasibility: economic, technical, operational, schedule, legal, political.
- PV = FV/(1 + r)ᵗ; NPV = Σ PV(benefits) − Σ PV(costs); accept if NPV > 0.
- ROI = (benefits − costs)/costs; payback = investment / net annual benefit; BCR = PV(B)/PV(C).
- BPP = scope + feasibility + schedule + risks, reviewed in a walkthrough.

## Chapter summary

- Projects are identified from many sources and selected with explicit criteria aligned to corporate strategy.
- Initiation sets up the team, charter, scope and management procedures.
- Feasibility tests, especially cost-benefit measures (NPV, ROI, payback), decide whether to proceed.
- The baseline project plan is reviewed by walkthrough and becomes the standard for later phases.

## Practice

1. Name four sources of project requests and four selection criteria.
2. Explain SWOT and critical success factors.
3. Describe the steps of project initiation and what a project charter contains.
4. Explain the six feasibility tests with an example of each.
5. A project costs 200,000 now and returns 90,000 net per year for 4 years at a 10% discount rate. Compute NPV, simple payback and ROI. (Annuity factor 4 years at 10% = 3.1699.)
6. Distinguish tangible and intangible benefits with examples.
7. What is a baseline project plan and how is it reviewed?
8. Why is sensitivity analysis done?

::: note Answers and worked solutions
**1.** Sources: management, departments, IT staff, external requirements. Criteria: strategic alignment, benefits, cost, risk, resources, size.
**2.** SWOT lists internal strengths and weaknesses and external opportunities and threats. CSFs are the few areas that must perform well for the organisation to succeed; the IS should supply information about them.
**3.** Form team; establish customer relationship; initiation plan; management procedures; project workbook; charter (purpose, objectives, scope, deliverables, constraints, sponsor, budget).
**4.** Economic: benefits exceed costs. Technical: team can build with the technology. Operational: users will adopt it. Schedule: deadline achievable. Legal: complies with privacy law. Political: head of department supports it.
**5.** NPV = −200,000 + 90,000 × 3.1699 = −200,000 + 285,291 = **+85,291**. Payback = 200,000/90,000 = **2.22 years**. ROI = (4 × 90,000 − 200,000)/200,000 = **80%**.
**6.** Tangible: reduced staff hours, fewer errors, lower paper cost. Intangible: better student satisfaction, improved reputation, faster decisions.
**7.** The BPP is the first documented plan of scope, cost, schedule, risks and feasibility. It is reviewed in a structured walkthrough by peers and users, then approved by the sponsor.
**8.** To test whether the recommendation still holds if costs rise or benefits fall.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the types of feasibility that are assessed before a systems development project is approved.**

*Introduction.* A feasibility study asks whether a proposed project is practical before large sums are spent. It tests six aspects, and failure in any one can stop the project.

*Types of feasibility.*

1. **Economic.** Do the benefits exceed the costs? It uses cost-benefit measures such as NPV, ROI and payback.
2. **Technical.** Can the system be built with available technology and skills? Familiarity with tools, project size and compatibility with existing systems matter.
3. **Operational.** Will the system fit the organisation, and will people use it? User acceptance and fit with existing work processes are tested.
4. **Schedule.** Can the project be finished in the time available, given dependencies and resources?
5. **Legal and contractual.** Does it comply with privacy law, copyright, licences and contracts?
6. **Political.** Will powerful stakeholders support it, and who might resist?

| Type | Key question | Example for a college result system |
|---|---|---|
| Economic | Benefit > cost? | NPV of +447,697 |
| Technical | Can we build it? | web stack the staff know |
| Operational | Will staff use it? | training for exam section |
| Schedule | In time? | ready before exam month |
| Legal | Allowed? | student data privacy |
| Political | Supported? | principal as sponsor |

*Conclusion.* The study ends with a recommendation to go, change or stop, and its figures become part of the baseline project plan.

**Q2 (10 marks). A college proposes a library system costing NPR 300,000 now. It saves NPR 180,000 a year, costs NPR 40,000 a year to run, and will be used for 4 years. The discount rate is 12%. Calculate NPV, ROI, simple and discounted payback and the benefit–cost ratio, and give a decision.**

*Introduction.* Cost-benefit analysis compares the money a system costs with the money it earns. Because money later is worth less than money now, future amounts are discounted: PV = FV/(1 + r)ᵗ (Figure 2.1 shows this for another project).

*Step 1: net annual benefit.* 180,000 − 40,000 = **NPR 140,000** a year.

*Step 2: discounted net benefits at 12%.*

| Year | Net benefit | Discount factor | Present value | Cumulative PV − 300,000 |
|---|---|---|---|---|
| 1 | 140,000 | 0.8929 | 125,000 | −175,000 |
| 2 | 140,000 | 0.7972 | 111,607 | −63,393 |
| 3 | 140,000 | 0.7118 | 99,649 | +36,256 |
| 4 | 140,000 | 0.6355 | 88,973 | +125,229 |

*Step 3: measures.*

1. **NPV** = 425,229 − 300,000 = **+NPR 125,229**. Positive, so the project adds value.
2. **ROI** = (4 × 140,000 − 300,000) ÷ 300,000 = 260,000 ÷ 300,000 = **86.7%** (undiscounted).
3. **Simple payback** = 300,000 ÷ 140,000 = **2.14 years**.
4. **Discounted payback.** The cumulative PV reaches 236,607 after year 2, so the remaining 63,393 is recovered in year 3: 2 + 63,393 ÷ 99,649 = **2.64 years**.
5. **BCR.** PV of benefits = 180,000 × 3.0373 = 546,723; PV of costs = 300,000 + 40,000 × 3.0373 = 421,494; BCR = **1.30**, above 1.
6. **IRR** is about **30.7%**, far above the 12% discount rate.

*Sensitivity.* If benefits fall by 25% to 135,000 a year, net benefit is 95,000 and NPV = 95,000 × 3.0373 − 300,000 = −11,452: the decision is marginal, so the benefits must be confirmed.

*Decision.* NPV > 0, BCR > 1 and IRR > discount rate all say **accept**. Payback inside the 4-year life supports this. Intangible benefits (better service to students) add to the case, but the sensitivity test shows a real risk.

*Conclusion.* A project is accepted when discounted benefits exceed discounted costs; several measures should agree, and a sensitivity test shows how fragile the answer is.
