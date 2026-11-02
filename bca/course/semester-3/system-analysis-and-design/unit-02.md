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

## 2.5 Building and reviewing the baseline project plan

The **Baseline Project Plan (BPP)** is the major deliverable of planning: the best current estimate of scope, benefits, costs, risks and resources, which later phases are measured against. Typical contents:

- **Introduction:** project overview, recommendation.
- **System description:** the business problem and a high-level view of alternatives and the recommended approach.
- **Feasibility assessment** (the six tests) and the cost-benefit analysis.
- **Management issues:** team composition, communication plan, project schedule, standards and procedures, risks.

It is reviewed in a **structured walkthrough**: the author presents the plan to peers and users, who look for omissions and errors (not to judge the author). Roles: coordinator, presenter, user representative, secretary, standards bearer. The outcome is approve, approve with changes, or reject; the sponsor and steering committee give final go/no-go.

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
