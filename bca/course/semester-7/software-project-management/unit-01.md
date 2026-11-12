---
subject: Software Project Management
grade: BCA Semester 7
unit: 1
title: Software Project Management Concepts
hours: 8
area: BCA 402 · Software Project Management · Unit 1
---

A college decides to replace its paper-based admission process with a web portal. The principal wants it live before the next intake, the budget is fixed, three teachers want three different features, and the only developers are four final-year students. Nobody doubts that the software can be written. The real questions are different: who decides what is built, how long each part takes, what happens if one developer leaves, and how the principal will know the project is on track. **Software project management (SPM)** is the discipline that answers those questions.

::: key What this unit gives you
- What a project and a software project are, and how software projects differ from bridges and buildings.
- Why software project management is important and why so many software projects still fail.
- The activities, the management cycle and the process of SPM, with the project life cycle.
- The characteristics of a good and of a successful software project manager.
- An overview of software project planning, including the Step Wise outline and the types of plan.
:::

## 1.1 Introduction: project, software project and project management

### What is a project?

A **project** is a temporary endeavour, with a definite beginning and end, undertaken to create a unique product, service or result. Four words in that definition matter.

- **Temporary.** It ends when its objectives are met or when it is cancelled. A project is not routine work such as running the college server every day.
- **Unique.** Even if similar systems exist, this one has a different customer, team, data and context.
- **Objectives.** A project exists to achieve something specific and measurable.
- **Constraints.** Every project is bound by scope, time, cost and quality, often drawn as the **project management triangle**: change one side and at least one other must move.

Jobs that are *not* projects: payroll processing every month, answering helpdesk calls, daily database backup. They are **operations**, repeated indefinitely.

### Characteristics of a project

| Characteristic | Meaning | Software example |
|---|---|---|
| Non-routine | tasks are not repetitive | each new app needs new analysis and design |
| Planned | work follows a plan towards a goal | schedule and budget approved by the sponsor |
| Aiming at a specific target | a defined deliverable | "online admission system, version 1.0" |
| Made for a customer | a sponsor or client pays | the college, a bank, a ministry |
| Predetermined time span | start and end dates | 24 weeks from kick-off to hand-over |
| Involves several specialisms | analysts, designers, testers | requirement analyst, UI designer, DBA |
| Phased | work proceeds in stages | analysis, design, build, test, deploy |
| Uses resources | people, money, equipment | team of five, laptops, cloud hosting |
| Risky | outcome is uncertain | a key developer resigns in week 10 |

### What is a software project?

A **software project** is a project whose deliverable is software (a program, a system, a mobile app, a website), together with the documentation, data and procedures needed to use and maintain it. A software project is more than coding. It includes eliciting requirements, designing, programming, testing, installing, training users, and often later maintenance. The same word *software* may mean a one-off bespoke system (a payroll for one bank), a product sold to many users (a word processor), or an embedded program inside a device.

### Software projects versus other projects

Software shares the general nature of all projects, but several of its properties make it harder to manage than, say, building a house.

| Aspect | Conventional project (e.g. a bridge) | Software project |
|---|---|---|
| Visibility | progress can be seen on site | the product is invisible; progress must be inferred from documents and tests |
| Complexity | complexity is bounded by physics and codes | very high per pound of cost; huge numbers of states and interactions |
| Conformity | follows physical laws and standard parts | must conform to arbitrary human and legacy-system interfaces |
| Flexibility | changes are expensive once poured | thought to be easy to change, so changes arrive constantly (requirements creep) |
| Estimation | decades of cost data and standard materials | little history, new technology each time, large variance in programmer productivity |
| Raw material | physical; wasted material is visible | intellectual effort; wasted effort is invisible |
| Life | stable for decades | continuous maintenance and evolution; obsolescence in years |
| Process | well-known sequences | many competing process models |

::: note Brooks' observation
Fred Brooks in *The Mythical Man-Month* (1975) argued that software has "essential difficulties": complexity, conformity, changeability and invisibility. Adding people to a late project often makes it later, because new members must be trained and communication paths multiply as n(n−1)/2.
:::

### Software engineering problem and software product

A **software product** has attributes the customer expects: *maintainability*, *dependability* (reliability, security, safety), *efficiency* and *acceptability* (usable and compatible). Different projects weigh these differently: a hospital system stresses dependability, a mobile game stresses efficiency and acceptability. Project management must trade these off against time and money, because the cost of a product rises steeply as each attribute is pushed higher.

### What is project management?

**Project management** is the application of knowledge, skills, tools and techniques to project activities to meet the project requirements. It involves planning the work, organising and staffing it, directing the team, and controlling progress against the plan. In a software context it also means managing *uncertainty*: about what the user really wants, about how long the code takes, and about the technology.

```svgfig label="1.1" caption="The project management triangle (scope, time, cost) with quality at the centre. Squeezing one side forces trade-offs on the others."
f = Fig(600, 250)
f.poly([(300, 22), (110, 210), (490, 210)], fill="#ccfbf1", stroke=TEAL, sw=2.2)
f.text(300, 14, "Scope (what is built)", size=12, color=NAVY, bold=True)
f.text(92, 232, "Time (schedule)", size=12, color=NAVY, bold=True)
f.text(508, 232, "Cost (budget)", size=12, color=NAVY, bold=True)
f.circle(300, 150, 42, fill="#fde68a", stroke=AMBER, sw=2, label="Quality", size=12, color=NAVY)
f.text(300, 100, "Customer value", size=10.5, color=SLATE)
```

## 1.2 Importance of and problems in software project management

### Why SPM matters

1. **Software is everywhere and expensive.** Banks, airlines, hospitals and governments depend on it; failure costs money and sometimes lives.
2. **Without a plan, work expands.** A team without a schedule discovers it is late only when it is too late to recover.
3. **Resources are limited.** A manager decides which features to build first and which people do what.
4. **Customers and developers think differently.** A project manager is the bridge: translating business needs into tasks, and technical limits into business language.
5. **Control and early warning.** Regular monitoring shows slippage in week 3 instead of week 30.
6. **Quality and risk.** Planned reviews, tests and risk lists find problems while they are cheap to fix.
7. **Better predictability for the customer.** Dates, costs and scope are agreed and tracked.

### Problems in software project management

| Problem | Why it happens | Typical remedy |
|---|---|---|
| Unclear or changing requirements | users cannot state needs in advance; business changes | prototyping, iterative delivery, change control |
| Poor estimation | little history, optimism, pressure from the customer | use several techniques, keep records, add contingency |
| Unrealistic deadlines | commitments made before analysis | negotiate scope; produce an estimate before agreeing a date |
| Scope creep | small additions accepted without checking cost | formal change control, product backlog |
| Inadequate risk management | risks are ignored until they become problems | risk register, regular risk review |
| Lack of skilled people; turnover | competition for developers | training, pairing, documentation, bus-factor reduction |
| Poor communication | many stakeholders, distributed teams | communication plan, regular meetings, shared tools |
| Technology change | new frameworks arrive during the project | prototype early, limit new technology on critical paths |
| Weak testing and quality control | testing is squeezed at the end | quality plan, reviews, automated tests |
| Poor visibility of progress | work is invisible | working increments, burn-down charts, earned value |

::: example Why do software projects fail? A simple picture
Industry surveys (the Standish Group's CHAOS reports, for instance) have repeatedly found that only a minority of software projects are delivered on time, on budget and with full scope. The usual causes, in order of how often they appear: weak user involvement, incomplete requirements, changing requirements, lack of executive support, and unrealistic expectations. All of them are management problems, not coding problems. The exact percentages differ between reports and years, so quote the pattern rather than a number in an exam.
:::

## 1.3 Activities and the process of software project management

### Activities covered by SPM

Hughes and Cotterell, whose textbook *Software Project Management* the TU syllabus follows, list the activities covered by SPM as feasibility study, planning, and project execution (requirements analysis, design, coding, verification and validation, implementation, maintenance and support), and these are surrounded by control activities.

1. **Feasibility study.** Is the project worth doing? Costs and benefits are estimated to decide whether to go ahead.
2. **Planning.** If it is feasible, decide how, when and by whom the work will be done: scope, schedule, resources, quality, risk and communication.
3. **Execution.** Carry out the plan: requirements analysis, design, implementation, testing, installation, with sub-planning for each stage.
4. **Monitoring and control.** Compare actual progress with the plan and correct deviations.
5. **Closure.** Hand over, record lessons learned, release the team.

### The project management cycle

Management is cyclic: a manager sets *objectives*, makes a *plan*, *monitors* progress, and *replans* when reality departs from the plan. The classic loop is **plan, do, check, act**.

```svgfig label="1.2" caption="The project management cycle. Monitoring compares actual progress with the plan; deviations lead to corrective action or replanning."
f = Fig(620, 230)
f.box(10, 90, 100, 50, "Project\nobjectives", fill="#ccfbf1", stroke=TEAL, color=NAVY, size=11, bold=True)
f.box(160, 90, 90, 50, "Plan", fill=BLUE, color=NAVY, size=12, bold=True)
f.box(300, 90, 90, 50, "Execute", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=12, bold=True)
f.box(440, 90, 100, 50, "Monitor and\ncompare", fill="#fde68a", stroke=AMBER, color=NAVY, size=11, bold=True)
f.box(300, 8, 130, 46, "Replan or take\ncorrective action", fill=BLUE, color=NAVY, size=10.5, bold=True)
f.box(160, 180, 230, 40, "Project closure and lessons learned", fill="#ccfbf1", stroke=TEAL, color=NAVY, size=10, bold=True)
f.arrow([(110, 115), (160, 115)], color=NAVY, sw=1.8)
f.arrow([(250, 115), (300, 115)], color=NAVY, sw=1.8)
f.arrow([(390, 115), (440, 115)], color=NAVY, sw=1.8)
f.arrow([(490, 90), (490, 31), (430, 31)], color=NAVY, sw=1.8)
f.arrow([(300, 31), (205, 31), (205, 90)], color=NAVY, sw=1.8)
f.arrow([(345, 140), (345, 180)], color=SLATE, sw=1.5, dash=True)
```

### Project phases and the project life cycle

A project passes through phases: **initiation** (idea, feasibility, charter), **planning** (scope, schedule, budget, risks), **execution** (the technical work), **monitoring and control** (overlapping execution) and **closure**. Resources and spending are small at the start, peak during execution and fall at closure. The ability to change the project cheaply is greatest at the beginning and falls as work is done; this is why requirements and plan reviews early in the project are so valuable.

The **product life cycle** is longer than the project life cycle. It covers the whole life of the software: conception, development (the project), operation and maintenance, retirement. The project ends at hand-over, but the product continues and often costs more to maintain than to build.

### Project management knowledge areas

The Project Management Institute's PMBOK Guide groups the work into knowledge areas, all of which apply to software:

| Knowledge area | What it controls | Software example |
|---|---|---|
| Integration | coordinating all other areas, change control | approving a change request |
| Scope | what is and is not in the project | the product backlog or requirements document |
| Schedule | activities, durations, critical path | Gantt chart, network diagram |
| Cost | estimating and budgeting | COCOMO estimate, budget baseline |
| Quality | meeting acceptance criteria | test plan, code review |
| Resources | team and equipment | assigning developers to modules |
| Communication | information flow | weekly status report, stand-up |
| Risk | identifying and responding to uncertainty | risk register |
| Procurement | buying or outsourcing | contract with a hosting vendor |
| Stakeholders | those affected by the project | principal, teachers, students |

## 1.4 Characteristics of a good project manager

A project manager (PM) is accountable for delivering the project's objectives. The role differs from the technical lead: the PM manages people, time, money and risk, while the lead decides the technical approach.

### Responsibilities

- Define scope and objectives together with the sponsor; write the project plan.
- Estimate effort and cost; build the schedule; assign tasks.
- Select, motivate and organise the team; resolve conflict.
- Communicate with stakeholders and report progress honestly.
- Manage risks, issues and changes.
- Ensure quality; negotiate with the customer and with suppliers.

### Qualities of a good project manager

| Quality | Why it matters |
|---|---|
| Leadership and vision | the team needs direction and a reason to follow the plan |
| Communication (listening, writing, presenting) | most of a PM's day is communication |
| Technical understanding | to judge estimates and risks, though not necessarily to be the best coder |
| Organisation and planning | tracking dozens of tasks and dependencies |
| Decision-making | choosing quickly with incomplete information |
| Negotiation and conflict resolution | between customer and team, and within the team |
| Realism and honesty | bad news reported early can still be fixed |
| Ability to motivate | developers work best when they see purpose and recognition |
| Adaptability and calmness | changes and crises are normal |
| Integrity and ethics | honest reporting, protection of customer data |

### Successful software project manager

A **successful** manager delivers value, not only on-time delivery. Typical marks of success: the project meets its time, cost and quality targets; the customer is satisfied; the team is still intact and willing to work together again; lessons are recorded; and the product can be maintained. Skills that distinguish successful managers: they involve users from the start, insist on clear requirements, break the work into small verifiable pieces, protect the team from outside interruption, keep a visible risk list, and say no (or "yes, if we drop this") to scope changes.

## 1.5 Overview of software project planning

Planning answers: *what* will be built, *how*, *when*, *by whom*, *at what cost* and *what could go wrong*. Hughes and Cotterell's **Step Wise** framework is a convenient outline of ten steps.

| Step | Activity | Output |
|---|---|---|
| 0 | Select project | a candidate project |
| 1 | Identify project scope and objectives | objectives, stakeholders, authority |
| 2 | Identify project infrastructure | organisation, standards, tools |
| 3 | Analyse project characteristics | project type, risks, approach |
| 4 | Identify products and activities | product breakdown, activity list |
| 5 | Estimate effort for each activity | effort and cost estimates |
| 6 | Identify activity risks | risk register |
| 7 | Allocate resources | staff allocation |
| 8 | Review and publicise the plan | agreed plan |
| 9 and 10 | Execute plan and lower-level planning | detailed plans, monitoring |

### Types of project plan

| Plan | Contents |
|---|---|
| Project (software development) plan | scope, schedule, resources, deliverables, milestones |
| Quality plan | quality targets, reviews, test strategy |
| Risk management plan | identified risks, probability, impact, responses |
| Configuration management plan | version control, baselines, change procedure |
| Communication plan | who gets what information, how often |
| Staffing plan | roles, skills, timing of staff |
| Validation and verification plan | test levels, acceptance criteria |
| Maintenance plan | support after delivery |

### Feasibility study and project scope

Before heavy investment, a feasibility study tests whether the project is technically possible, economically worthwhile, and operationally acceptable. Scope is then fixed in a **scope statement**: objectives, deliverables, boundaries (what is *out* of scope), assumptions and constraints. A precise scope statement is the single best defence against scope creep.

::: example A scope statement for the college admission portal
**Objective:** allow applicants to register, upload documents and pay fees online before 15 Baisakh.
**Deliverables:** web application, admin panel, user manual, trained staff.
**In scope:** registration, document upload, payment through a wallet gateway, admission list publishing.
**Out of scope:** hostel allocation, library membership, native mobile app.
**Assumptions:** the college supplies hosting and a test list of 200 applicants.
**Constraints:** budget Rs 6 lakh; live date fixed; four developers.
:::

## Formula and fact sheet

- Project = temporary, unique, objective-driven, constrained by scope, time, cost and quality.
- Software differs from other projects in visibility, complexity, conformity, changeability and estimation difficulty.
- Communication channels in a team of n people = n(n − 1)/2 (n = 5 gives 10; n = 10 gives 45).
- Management cycle: objectives, plan, execute, monitor, replan.
- Step Wise has ten steps, from selecting the project to lower-level planning.

## Chapter summary

- A project is a temporary, unique effort with objectives and constraints; a software project delivers software and its supporting documentation.
- Software projects are harder to manage than conventional ones because the product is invisible, complex, constantly changing and difficult to estimate.
- SPM matters because it provides plans, control, early warning and quality assurance; typical problems are poor requirements, estimation, scope creep and weak risk management.
- SPM activities run from feasibility to closure, within a plan-do-monitor-replan cycle and the PMBOK knowledge areas.
- A good project manager combines leadership, communication, planning, negotiation and integrity; success is measured by value delivered and a team that remains intact.
- Planning follows the Step Wise outline and produces several plans, beginning with a clear scope statement.

## Practice

1. Define *project* and list five characteristics. Give two examples of work that is not a project.
2. Differentiate software projects from other types of projects, with five points.
3. Explain the importance of software project management.
4. List and explain six problems faced in software project management and a remedy for each.
5. What is the project management cycle? Draw and explain it.
6. Explain the activities covered by software project management.
7. Write the characteristics of a good project manager.
8. A team grows from 5 to 9 people. How many communication channels exist before and after? What does this say about adding people to a late project?
9. Write a scope statement for a hospital appointment app, with at least two items that are out of scope.
10. Explain the Step Wise approach to planning in brief.

::: note Answers and worked solutions
**1.** A project is a temporary endeavour with a start and end that creates a unique product, service or result. Characteristics: non-routine, planned, specific target, made for a customer, fixed time span, several specialisms, phased, uses resources, risky. Not projects: monthly payroll, daily backups.
**2.** Visibility (software is invisible), complexity, conformity to arbitrary interfaces, flexibility leading to constant change, estimation difficulty because of little history and variable productivity, and long maintenance life.
**3.** Planning, control, resource use, bridge between customer and developers, early warning of slippage, quality and risk management, predictability for the customer.
**4.** Changing requirements (prototyping, change control); poor estimates (several techniques, historical data); unrealistic deadlines (negotiate scope); scope creep (change control board); staff turnover (documentation, pairing); poor communication (communication plan).
**5.** Objectives lead to a plan; the plan is executed; progress is monitored against the plan; deviations trigger corrective action or replanning; the loop repeats until closure (figure 1.2).
**6.** Feasibility study, planning, execution (requirements, design, coding, verification and validation, implementation, maintenance), monitoring and control, closure.
**7.** Leadership, communication, technical understanding, planning, decision-making, negotiation, honesty, motivation, adaptability, ethics.
**8.** n = 5: 5 × 4 / 2 = **10**. n = 9: 9 × 8 / 2 = **36**. Channels rise 3.6 times for 1.8 times the people, so new staff add communication and training overhead; Brooks' law says adding people to a late project makes it later.
**9.** Objective: patients book, change and cancel appointments from a phone. In scope: registration, doctor schedule, booking, SMS reminder. Out of scope: billing, electronic medical records, pharmacy. Assumptions and constraints should also be stated.
**10.** Select the project; define scope and objectives; set infrastructure; analyse characteristics; identify products and activities; estimate effort; identify risks; allocate resources; review and publicise the plan; execute and plan in detail.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). How do software projects differ from other types of project?**

*Introduction.* Every project is temporary, unique and constrained, but software has properties that make it harder to plan and control than most physical projects.

*Differences.*

1. **Invisibility.** A building grows before the eyes of the manager; software progress is seen only through documents, demonstrations and tests.
2. **Complexity.** Software contains a very large number of states and interactions for its cost; no two parts are alike.
3. **Conformity.** It must fit whatever hardware, laws, legacy systems and human habits exist.
4. **Changeability.** Because it seems easy to change, users keep asking for changes, so requirements creep.
5. **Estimation difficulty.** There are fewer standard components and little reliable history, and programmer productivity varies by a factor of ten or more.
6. **Maintenance.** Software is never finished; it evolves for years after delivery.

*Conclusion.* Because of these differences, software project managers rely on iterative delivery, prototypes, frequent reviews and strong change control.

**Q2 (10 marks). What is software project management? Explain its importance, activities and the characteristics of a good software project manager.**

*Introduction.* Software project management is the planning, organising, staffing, directing and controlling of software development so that the product is delivered within scope, time, cost and quality constraints.

*Importance.* It provides a plan and schedule, uses scarce people and money wisely, gives early warning of slippage, manages change and risk, and builds quality in through reviews and tests. It links the customer's business needs to the team's technical work.

*Activities.* Feasibility study, planning (scope, schedule, resources, quality, risk), execution (requirements, design, coding, testing, implementation), monitoring and control through the cycle of plan, execute, monitor and replan, and closure with lessons learned.

*The good project manager.* The manager leads and motivates, communicates clearly with team and customer, understands enough technology to judge estimates, organises work, decides under uncertainty, negotiates scope and resources, reports bad news early and acts ethically.

| Area | Key point |
|---|---|
| Purpose | deliver software within scope, time, cost, quality |
| Benefit | control, predictability, lower risk |
| Core cycle | plan, execute, monitor, replan |
| Manager's core skills | leadership, communication, planning, negotiation |

*Conclusion.* Good project management does not guarantee success, but its absence almost guarantees failure; most failed software projects fail for management reasons rather than technical ones.
