---
subject: System Analysis and Design
grade: BCA Semester 3
unit: 1
title: System Development Fundamentals
hours: 9
area: BCA 204 · System Analysis and Design · Unit 1
---

Organisations run on information systems: a bank's core system, a university's result portal, a shop's billing software. **Systems analysis and design (SAD)** is the disciplined way of building them so that they solve the right problem, on time and within budget.

::: key What this unit gives you
- Systems, information systems and their types.
- The systems development life cycle (SDLC) and its models: waterfall, prototyping, spiral, RAD, agile, XP.
- CASE tools, service-oriented architecture, object-oriented analysis and design.
- Acquiring software (build, buy, outsource, reuse) and managing the project: Gantt, PERT, critical path.
:::

## 1.1 The systems development environment

A **system** is a set of interrelated components working toward a goal, with inputs, processing, outputs, feedback and a boundary separating it from its **environment**. An **information system (IS)** collects, processes, stores and distributes information to support operations and decisions; it combines people, procedures, data, hardware and software. The **systems analyst** is the bridge between users and technologists: studies the business problem, defines requirements, designs the solution, and manages change. Skills: analytical thinking, communication, technical knowledge, business knowledge, and project management.

### Types of information systems

| Type | Purpose | Users | Example |
|---|---|---|---|
| **Transaction Processing System (TPS)** | records daily transactions accurately and fast | clerks, operators | billing, ATM, bus ticketing |
| **Management Information System (MIS)** | summary reports from TPS data for control | middle managers | monthly sales report |
| **Decision Support System (DSS)** | interactive "what-if" models for semi-structured decisions | managers, analysts | budget simulator |
| **Executive Support System (ESS)** | dashboards of key indicators and trends | senior executives | enterprise dashboard |
| **Expert system** | rule-based advice replacing a specialist | any | loan advisor |
| **Office automation / knowledge management** | documents, mail, collaboration | all staff | e-mail, shared drives |
| **ERP / CRM** | integrate processes across departments / manage customers | organisation | SAP, Salesforce |

## 1.2 Modern approaches to systems analysis and design

Two broad views of building a system: **structured** (process-oriented: data flow diagrams and flowcharts, data kept separate from processing; Units 3 and 4) and **object-oriented** (the system as interacting objects bundling data and behaviour; UML). Both exist inside a development *method*: a series of phases with deliverables. A **methodology** gives the steps, techniques and tools; the **life cycle** gives the order.

## 1.3 The systems development life cycle (SDLC)

| Phase | Question answered | Main output |
|---|---|---|
| **1. Planning** (identification and selection, feasibility) | Is this project worth doing? | baseline project plan |
| **2. Analysis** | What must the system do? | requirements, process and data models |
| **3. Design** | How will it do it? | logical then physical design specifications |
| **4. Implementation** | Build and deliver it | coded, tested, installed system; documentation, training |
| **5. Maintenance** (operation) | Keep it useful | fixes and enhancements |

At the end of each phase a **review** gate decides whether to proceed. The cost of finding an error rises steeply with the phase: a requirement mistake found during maintenance can cost 50–100 times what it would have cost during analysis, which is why analysis and design effort pays off.

### The traditional waterfall model

Phases run strictly in sequence, with documentation as the contract between them. **Strengths:** simple, clear milestones, good for stable and well-understood requirements, easy to manage. **Weaknesses:** no working software until late; changes are expensive; users see the product only at the end; assumes requirements can be frozen early.

### Approaches for improving development

| Model | Idea | Best when | Risk |
|---|---|---|---|
| **Prototyping** | build a quick working model, show users, refine | requirements are unclear | endless iteration; throw-away vs evolutionary confusion |
| **Spiral** | repeated cycles of plan → risk analysis → build → evaluate | large, risky projects | needs risk expertise; costly |
| **Incremental / iterative** | deliver working slices, each adding functions | early value, changing needs | architecture can degrade |
| **RAD (Rapid Application Development)** | timeboxed (60–90 day) builds with heavy user involvement, prototypes, reuse and CASE | well-bounded systems, strong users | needs skilled small team; poor for large scale |
| **Agile** | short iterations (1–4 weeks), working software, customer collaboration, response to change | volatile requirements | needs disciplined, co-located or well-coordinated team |

## 1.4 CASE tools

**Computer-Aided Software Engineering** tools automate parts of development. *Upper CASE* supports analysis and design (diagram editors for DFD/ERD/UML, a central **repository** of definitions, consistency checking); *lower CASE* supports implementation (code generation, testing, version control). Benefits: faster, consistent diagrams, enforced standards, easier changes, generated documentation. Costs: licences, training, and the risk of mistaking tool output for understanding. Examples: Visual Paradigm, Enterprise Architect, draw.io/Lucidchart, StarUML.

## 1.5 Service-oriented architecture

**SOA** builds applications from **services**: self-contained, reusable business functions (check stock, validate payment) with a published interface, called over a network (SOAP/WSDL or REST/JSON) and loosely coupled. Benefits: reuse, interoperability among platforms, replacing one service without touching others, incremental modernisation. Cost: network latency, governance, and the complexity of distributed transactions. Its modern descendant is **microservices**.

## 1.6 Agile methodologies and Extreme Programming

The **Agile Manifesto** (2001) values *individuals and interactions* over processes and tools, *working software* over comprehensive documentation, *customer collaboration* over contract negotiation, and *responding to change* over following a plan. **Scrum** organises work in **sprints** (usually 2 weeks) with roles *product owner*, *scrum master*, *team*; artefacts *product backlog*, *sprint backlog*, *increment*; events *sprint planning, daily stand-up, review, retrospective*. **Kanban** limits work in progress on a board.

**Extreme Programming (XP)** takes good engineering practices to the extreme: **pair programming**, **test-driven development** (write the test first), **continuous integration**, **small releases**, **refactoring** (improve structure without changing behaviour), **simple design**, **collective code ownership**, an **on-site customer**, a sustainable pace of 40 hours a week, and **user stories** as requirements.

| | Waterfall | Agile |
|---|---|---|
| Requirements | fixed up front | evolve every iteration |
| Delivery | once, at the end | every few weeks |
| Customer role | at start and end | continuous |
| Change | costly | expected |
| Documentation | heavy | just enough |

## 1.7 Object-oriented analysis and design

**OOAD** models the problem as **objects** with attributes and operations, grouped into **classes**, related by association, aggregation and **inheritance**, communicating by messages; its principles are encapsulation, inheritance and polymorphism (as in OOP in Java, Semester II). The **Unified Modeling Language (UML)** notation includes: **use case diagrams** (actors and what they do with the system), **class diagrams** (classes, attributes, operations, relationships), **sequence diagrams** (messages over time), **activity diagrams** (workflow) and **state diagrams**. The **Unified Process** is an iterative, use-case-driven method with phases *inception, elaboration, construction, transition*. Analysis models what the business needs; design adds technology (classes become Java or Python code).

## 1.8 The origins of software and system acquisition

Software can come from several sources:

| Source | When suitable | Drawback |
|---|---|---|
| **In-house development** | unique needs, competitive advantage | slow, costly, needs skills |
| **Off-the-shelf (packaged) software** (e.g. Tally, MS Office) | common needs | needs adjusting to the package; vendor lock-in |
| **Customised package** (ERP) | standard process with local tweaks | expensive customisation; upgrades |
| **Outsourcing** (a software firm builds or runs it) | lack of staff or skills, focus on core business | dependence, confidentiality, contract management |
| **Open source** | low licence cost, flexibility | support and quality vary |
| **Cloud / SaaS** | quick start, no servers | subscription, data control |
| **End-user development** | small personal tools (spreadsheets) | no standards, hard to maintain |

**Choosing a supplier:** write a **request for proposal (RFP)** listing requirements; score vendors against weighted criteria (functionality, cost, support, reputation, flexibility, training); demonstrate and trial. **Reuse** means building from existing components, libraries, frameworks and patterns, and saves cost and defects but requires design for reuse and documentation.

## 1.9 Managing the information systems project

A **project** is a temporary effort with defined scope, schedule and budget, run by a **project manager** who plans, staffs, monitors and controls. Success depends on balancing **scope, time, cost and quality**. Activities: define scope, break work into tasks (**work breakdown structure**), estimate effort, sequence tasks, assign people, track progress, manage risks and changes, report.

### Representing and scheduling project plans

A **Gantt chart** shows tasks as bars along a calendar. A **network diagram** (PERT/CPM) shows task dependencies. **Critical Path Method (CPM)**: compute for each activity the earliest start/finish (forward pass) and latest start/finish (backward pass); **slack** = LS − ES; the **critical path** is the longest chain with zero slack, and it fixes the project duration. **PERT** uses three estimates per activity: optimistic *a*, most likely *m*, pessimistic *b*, with expected time **t = (a + 4m + b)/6** and standard deviation (b − a)/6.

::: example Worked example: critical path
Activities (duration in weeks, predecessors): A 3 (none); B 2 (A); C 4 (A); D 3 (B); E 2 (C); F 2 (D, E).
Forward pass: A 0→3; B 3→5; C 3→7; D 5→8; E 7→9; F starts at max(8, 9) = 9 → finishes **11**.
Backward pass (from 11): F 9–11; E 7–9; D 6–9; C 3–7; B 4–6; A 0–3.
Slack: A 0, C 0, E 0, F 0; **B = 4 − 3 = 1 and D = 6 − 5 = 1**. Critical path **A → C → E → F = 3 + 4 + 2 + 2 = 11 weeks**. Delaying B or D by up to a week does not delay the project; delaying any critical activity does.
**PERT estimate:** an activity with a = 2, m = 5, b = 14 has t = (2 + 20 + 14)/6 = **6**, standard deviation (14 − 2)/6 = 2.
:::

Project management software (MS Project, Jira, Trello, OpenProject) records tasks, dependencies, resources and baselines, draws Gantt charts, recalculates the critical path when dates change, tracks actual versus planned effort, and produces reports. Typical risks: unclear requirements, scope creep, unrealistic estimates, staff turnover, new technology; managed by identifying, rating (probability × impact), planning responses and monitoring.

## 1.10 The life cycle as a picture, and agile practice in the field

Figure 1.1 draws the five SDLC phases as the classic waterfall staircase. Each step has a **review gate**: the work is checked and the sponsor decides whether to go on, change course or stop. In practice a problem found in design often sends the team back to analysis, so the staircase is rarely followed without some rework. Plate 1.1 shows what the agile alternative looks like in a real team: a visible task board, short stand-up meetings and developers working in pairs. Notice that agile does not remove planning, analysis or testing; it repeats small amounts of each in every short iteration instead of doing each once.

```svgfig label="1.1" caption="SDLC waterfall. Each phase hands a document to the next and ends with a review gate. Red arrows show the hand-over of documents. The cost multiplier under each phase is the usual rule of thumb for fixing a requirement error found at that stage."
f = Fig(600, 250)
names = [("1 Planning", "baseline plan"), ("2 Analysis", "requirements"), ("3 Design", "design spec"), ("4 Implement", "tested system"), ("5 Maintain", "updates")]
cols = [BLUE, "#fde68a", "#bbf7d0", "#fbcfe8", "#e2e8f0"]
for i, (n, o) in enumerate(names):
    x, y = 10 + i * 116, 20 + i * 34
    f.box(x, y, 100, 40, n, fill=cols[i], color=NAVY, size=11, bold=True)
    f.text(x + 50, y + 54, o, size=9.5, color=SLATE)
    if i < 4:
        f.arrow([(x + 100, y + 20), (x + 108, y + 20), (x + 108, y + 54), (x + 116, y + 54)], color=RED, sw=1.8)
    f.text(x + 50, 232, ["1x", "5x", "10x", "50x", "100x"][i], size=11, color=RED, bold=True)
f.text(300, 246, "relative cost of fixing the same requirement error", size=10, color=RED, bold=True)
```

```photogrid label="1.1" cols="3" ratio="1.2" caption="Agile practice. (a) A task board of cards moving from To do to Done keeps the whole team's work visible. (b) A scrum-style board and short daily meeting. (c) Pair programming: two developers share one screen, so code is reviewed as it is written."
@ photo id="bca256/kanban" cap="Task board (To do / Doing / Done)"
fit 1.2
@ photo id="bca256/scrum" cap="Scrum board and stand-up"
fit 1.2
@ photo id="bca256/pair" cap="Pair programming"
fit 1.2
```

## 1.11 Eight reasons why a systematic life cycle matters

1. **Clear stages and responsibilities.** Every phase has a known purpose and a named output, so the team always knows what is finished and who owns what. A college project team can say, for example, that analysis ends when the requirements document is signed off.
2. **Cheaper error correction.** Mistakes found early cost far less than mistakes found after delivery. Spending an extra week checking the requirements can save months of rework after the system is live.
3. **Better user involvement.** Users take part in analysis, design reviews and acceptance tests. A system for a municipal office is more likely to be used if the ward staff helped to define its screens.
4. **Management control.** Review gates give the sponsor points to approve, change or stop the project. Money is released stage by stage instead of all at once, which limits the loss from a bad idea.
5. **Documentation.** Each phase leaves models and documents behind. When a new developer joins, or the original team leaves, the system can still be maintained and understood.
6. **Risk reduction.** Feasibility study and planning expose technical, financial and schedule risks before large sums are spent. Many failed projects skipped this step.
7. **Quality through testing.** Testing is planned from the requirements, so the delivered system can be checked against what was promised. Acceptance criteria are written before coding begins.
8. **Support for change.** Iterative and agile variants of the life cycle accept that requirements change. Working increments are shown to users every few weeks so a wrong turn is caught quickly.

## 1.12 Choosing a life-cycle model: waterfall, incremental, prototyping, spiral and RAD

The syllabus asks you to know the traditional waterfall life cycle and the approaches used to improve development. Every model below answers one question: *how do we find out what the user really wants before we spend the budget?* The models differ in when the user sees working software.

### The models in turn

- **Waterfall.** Phases run once, in order (planning, analysis, design, implementation, maintenance) and each phase is signed off before the next begins. It is predictable and easy to manage and document, but a mistake found in testing means going back through every earlier phase. It suits small, stable, well-understood systems and fixed-price government contracts, such as a payroll rule set that is fixed by law.
- **Incremental.** The system is cut into slices (for example login, then billing, then reports). Each slice goes through a short waterfall and is delivered to users. The first useful slice appears early, and later slices benefit from user feedback.
- **Prototyping.** A cheap, quick, partial model (paper sketch, clickable screens, or a small working program) is shown to users, who react, and the model is revised. A **throwaway prototype** is discarded after requirements are clear; an **evolutionary prototype** grows into the final system. Prototyping reduces requirement risk but can hide poor architecture and encourage users to expect the real thing in a week.
- **Spiral.** Each loop of the spiral passes through four steps: set objectives, assess and reduce risks, develop and test, and plan the next loop. It is risk driven and suits large, uncertain projects, but it needs skilled risk assessment and is expensive for small ones.
- **Rapid Application Development (RAD).** RAD compresses analysis, design and build into a few months using prototypes, **time-boxing** (a fixed deadline, features are dropped rather than the date moved), reusable components, CASE and **Joint Application Design (JAD)** workshops that put users and analysts in one room. It needs committed users, a modular design and a team that can build fast; it is a poor fit for safety-critical or very large systems.
- **Agile.** Short iterations of one to four weeks deliver working software each time and welcome changing requirements (see 1.6).

```svgfig label="1.2" caption="Where the models sit. Horizontal: how clear the requirements are at the start. Vertical: how soon the user needs working software. Waterfall lives at clear requirements with a relaxed delivery date; agile and RAD live where requirements are vague and speed matters."
f = Fig(600, 300)
f.line(60, 250, 580, 250, color=NAVY, sw=1.8)
f.line(60, 250, 60, 20, color=NAVY, sw=1.8)
f.text(320, 284, "Requirements clarity at the start  (vague  to  clear)", size=11, color=NAVY, bold=True)
f.text(34, 135, "Speed", size=11, color=NAVY, bold=True)
f.text(34, 150, "needed", size=11, color=NAVY, bold=True)
f.box(420, 190, 150, 44, "Waterfall", fill=BLUE, color=NAVY, size=12, bold=True)
f.box(300, 150, 150, 44, "Incremental", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=12, bold=True)
f.box(90, 40, 150, 44, "Agile", fill="#fde68a", stroke=AMBER, color=NAVY, size=12, bold=True)
f.box(250, 40, 150, 44, "RAD", fill="#fbcfe8", color=NAVY, size=12, bold=True)
f.box(90, 150, 150, 44, "Prototyping", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=12, bold=True)
f.box(90, 98, 150, 44, "Spiral (high risk)", fill=BLUE, color=NAVY, size=12, bold=True)
```

### Selection criteria

| Question about the project | Points towards |
|---|---|
| Requirements stable and well known | waterfall, incremental |
| Users cannot say what they want until they see something | prototyping, agile |
| High technical or business risk | spiral |
| Fixed, short deadline and active users | RAD, agile |
| Strict documentation or audit (banking, government) | waterfall, incremental with documentation gates |
| Large team spread over several sites | incremental with clear modules |

::: example Worked example: choosing a model
A municipality in Nepal wants a system to issue **birth and marriage certificates**. The legal fields are fixed by the Act, the forms are known, and the audit office wants a document at every stage. The team is small and users are available only for sign-off. The best fit is **incremental with waterfall-style gates**: deliver birth registration first, then marriage, then migration records. Contrast this with a **food-delivery start-up** that is not sure which features customers will pay for and must launch before a competitor does: **agile or RAD** with a clickable prototype in week one is the better choice.
:::

**Exam hint.** A 5-mark answer lists three or four models, one advantage and one disadvantage each, and ends with a sentence on how to choose. A 10-mark answer adds the comparison table and an example for the chosen model.

## 1.13 Information systems and their types, in depth

An **information system (IS)** is an organised set of people, data, processes, hardware and software that collects, stores, processes and distributes information to support operations, management and decision-making. The five organisational levels below each have their own kind of system, and the systems pass data upward.

```svgfig label="1.3" caption="The pyramid of information systems. Transaction processing systems at the base capture raw data; each higher layer summarises it for a more senior user and a less structured decision."
f = Fig(600, 280)
f.poly([(300, 14), (360, 64), (240, 64)], fill="#fbcfe8", label="ESS", lx=300, ly=48, size=12, color=NAVY)
f.poly([(240, 64), (360, 64), (420, 114), (180, 114)], fill="#fde68a", stroke=AMBER, label="DSS / Expert", lx=300, ly=92, size=12, color=NAVY)
f.poly([(180, 114), (420, 114), (480, 164), (120, 164)], fill="#bbf7d0", stroke=TEAL, label="MIS", lx=300, ly=142, size=12, color=NAVY)
f.poly([(120, 164), (480, 164), (540, 214), (60, 214)], fill=BLUE, label="TPS", lx=300, ly=192, size=12, color=NAVY)
f.text(560, 40, "Senior managers", size=10.5, color=NAVY, bold=True, anchor="end")
f.text(560, 92, "Analysts, managers", size=10.5, color=NAVY, bold=True, anchor="end")
f.text(560, 142, "Middle managers", size=10.5, color=NAVY, bold=True, anchor="end")
f.text(300, 240, "Operational staff: clerks, tellers, cashiers", size=11, color=NAVY, bold=True)
f.text(300, 262, "more data, more detail  (bottom)     more summary, more judgement  (top)", size=10, color=SLATE)
```

| System | Input | Processing | Output | Nepali example |
|---|---|---|---|---|
| **TPS** | raw transactions | validate, record, update files, immediate | receipts, updated balances | eSewa payment, bank teller system, Sajha Yatayat ticketing |
| **MIS** | TPS data | summarise, compare with plan | periodic and exception reports | monthly loan-recovery report of a cooperative |
| **DSS** | TPS/MIS data plus models | what-if analysis, simulation | scenarios, charts | a bank's interest-rate simulator, load-shedding planner |
| **ESS / EIS** | internal and external data | filter, drill down | dashboards, trends | CEO dashboard of branches and NPLs |
| **Expert system** | rules from experts | inference over a knowledge base | advice, diagnosis | crop-disease advisor for farmers |
| **Office automation** | documents, messages | edit, share, schedule | letters, calendars | word processor, email, shared drive |

### Properties that separate them

1. **Structure of the decision.** TPS handles fully structured work; MIS supports structured and some semi-structured decisions; DSS and ESS support semi-structured and unstructured decisions.
2. **Time horizon.** TPS is real time or daily; MIS is weekly or monthly; ESS is yearly and strategic.
3. **Data.** TPS data is detailed and internal; ESS also uses external data (market, rivals, regulations).
4. **Users.** Many operational users for TPS; few executives for ESS.

::: example Worked example: one sale travelling up the pyramid
A customer pays Rs 1,200 at a supermarket. The **TPS** records the sale, reduces stock of three items and prints a bill. At month end the **MIS** adds all bills into a sales-by-category report and flags items below reorder level. The **DSS** lets the manager test "what happens to profit if we cut the price of rice by 3 percent and sales rise by 8 percent?". The **ESS** shows the chief executive the chain's sales trend against the national retail index. Same data, four views.
:::

### Why analysts must know the types

The type decides the design. A TPS must be fast, accurate and recoverable (data entry validation, locking, audit trail). An MIS must be flexible in reporting. A DSS needs models and friendly what-if screens. Choosing the wrong type is a common reason for failure: managers asked for a "dashboard" but the project delivered a data-entry system with no summary.

**Likely questions.** (a) Define information system and explain the five types with one example each (10 marks). (b) Differentiate TPS and MIS in five points (5 marks). (c) Draw and explain the pyramid of information systems.

## 1.14 Object-oriented analysis with UML: use cases, classes, sequences and states

Section 1.7 named the idea; this section shows how an analyst actually draws it. The **Unified Modeling Language (UML)** is a standard set of diagrams, not a method. Each diagram answers one question about the system, and the analyst picks only the diagrams that help. For a college project four are enough: the use case diagram (who uses the system and for what), the class diagram (what things the system must remember), the sequence diagram (how objects talk to finish one scenario) and the state diagram (the life of one object).

| Diagram | Question it answers | Drawn during | Structured-analysis cousin |
|---|---|---|---|
| **Use case** | Which actors want which goals from the system? | analysis | context diagram, list of processes |
| **Class** | Which classes, attributes, operations and relationships exist? | analysis, then design | entity-relationship diagram |
| **Sequence** | In what order do objects exchange messages in one scenario? | analysis and design | the logic of one DFD process |
| **State (state machine)** | Which states can one object be in and what moves it between them? | design | entity life history, decision logic |
| **Activity** | What is the flow of actions, with branches and parallel paths? | analysis | flowchart, process model |

### Use case diagrams

An **actor** is anything outside the system that interacts with it: a person in a role (Member, Librarian), another system (the SMS gateway) or a clock that triggers a job. An actor is a role, not a person; one librarian can also be a member, and the diagram then shows two actors. A **use case** is a goal of an actor that the system helps to reach, named with a verb phrase: *Borrow book*, not *Borrowing screen*. The **system boundary** is a rectangle; actors stand outside it, use cases inside. A line joins an actor to the use cases it takes part in.

Two relationships between use cases appear in almost every exam answer. **`<<include>>`** means the base use case always calls the other one (Borrow book always includes Verify membership), so shared steps are written once. **`<<extend>>`** means the other use case happens only sometimes and under a condition (Calculate fine extends Return book, but only when the book is late). Use **generalisation** when one actor or use case is a special kind of another (Student member is a kind of Member).

```svgfig label="1.4" caption="Use case diagram of the library system. Stick figures are actors outside the boundary; ovals are use cases. Borrow book always includes Verify membership (dashed arrow, include); Calculate fine extends Return book only when the book is late (dashed arrow, extend)."
f = Fig(640, 312)
f.box(120, 6, 400, 292, "", fill="#ffffff", stroke=SLATE, r=4, dash=True)
f.text(320, 22, "Library system", size=11.5, color=SLATE, bold=True)
def actor(x, y, name):
    f.circle(x, y, 9, fill="#ffffff", stroke=NAVY, sw=1.8)
    f.line(x, y + 9, x, y + 40, color=NAVY, sw=1.8)
    f.line(x - 16, y + 20, x + 16, y + 20, color=NAVY, sw=1.8)
    f.line(x, y + 40, x - 13, y + 62, color=NAVY, sw=1.8)
    f.line(x, y + 40, x + 13, y + 62, color=NAVY, sw=1.8)
    f.text(x, y + 78, name, size=11, color=NAVY, bold=True)
def uc(cx, cy, label):
    f.raw('<ellipse cx="%s" cy="%s" rx="72" ry="26" fill="#ecfdf5" stroke="#0f766e" stroke-width="1.6"/>' % (cx, cy))
    f.text(cx, cy, label, size=10.5, color=NAVY, bold=True, vmid=True)
actor(55, 140, "Member")
actor(585, 140, "Librarian")
uc(215, 75, "Search\ncatalogue")
uc(215, 160, "Borrow\nbook")
uc(215, 245, "Return\nbook")
uc(425, 75, "Add new\nbook")
uc(425, 160, "Verify\nmembership")
uc(425, 245, "Calculate\nfine")
for yy in (75, 160, 245):
    f.line(71, 170, 143, yy, color=NAVY, sw=1.3)
f.line(569, 170, 497, 75, color=NAVY, sw=1.3)
f.line(569, 170, 497, 245, color=NAVY, sw=1.3)
f.arrow([(287, 160), (353, 160)], color=RED, sw=1.5, dash=True, label="<<include>>", lpos=(320, 150), lsize=9.5, lcolor=RED)
f.arrow([(353, 245), (287, 245)], color=AMBER, sw=1.5, dash=True, label="<<extend>>", lpos=(320, 235), lsize=9.5, lcolor=AMBER)
```

::: example Worked example: reading a use case description
A diagram shows only names; the real analysis is the **use case description**. For *Borrow book*:

- **Actor:** Member (primary), Librarian (operates the counter). **Trigger:** the member presents a book and a card.
- **Precondition:** the member record exists and is not suspended. **Main flow:** (1) librarian scans the card; (2) system verifies membership (included use case); (3) librarian scans the book; (4) system checks that the copy is available and that the member has fewer than 3 loans; (5) system records the loan with a due date 14 days ahead; (6) system prints the slip.
- **Alternative flows:** 2a card expired, system refuses and the use case ends; 4a limit reached, system asks to return a book first; 4b book already issued, system shows the due date.
- **Postcondition:** one new LOAN row exists and the book is marked issued.
Each numbered step becomes a test case in unit 5, and each alternative flow becomes a rule in the requirements specification.
:::

### Class diagrams

```svgfig label="1.5" caption="Class diagram of the library system. Member, Loan and Book are classes with attributes and operations. One Member has zero or more Loans (1 to 0..*), each Loan is for exactly one Book (0..* to 1). Student and Teacher inherit from Member (hollow triangle)."
f = Fig(680, 292)
def cls(x, y, w, name, attrs, ops, fill=BLUE):
    ha = 20 + 15 * len(attrs) + 6
    ho = 15 * len(ops) + 8
    f.raw('<rect x="%s" y="%s" width="%s" height="%s" fill="#ffffff" stroke="#1e3a8a" stroke-width="1.5"/>' % (x, y, w, 24 + ha - 20 + ho))
    f.raw('<rect x="%s" y="%s" width="%s" height="24" fill="%s" stroke="#1e3a8a" stroke-width="1.5"/>' % (x, y, w, fill))
    f.text(x + w / 2, y + 12, name, size=11.5, color=NAVY, bold=True, vmid=True)
    for i, a in enumerate(attrs):
        f.text(x + 8, y + 24 + 12 + 15 * i, a, size=9.8, color=SLATE, anchor="start", vmid=True)
    ly = y + 24 + 6 + 15 * len(attrs)
    f.line(x, ly, x + w, ly, color=NAVY, sw=1.2)
    for i, o in enumerate(ops):
        f.text(x + 8, ly + 11 + 15 * i, o, size=9.8, color=SLATE, anchor="start", vmid=True)
cls(10, 15, 160, "Member", ["- memberId : int", "- name : String", "- phone : String"], ["+ borrow(book)", "+ giveBack(book)"])
cls(260, 15, 160, "Loan", ["- loanId : int", "- issueDate : Date", "- dueDate : Date"], ["+ calculateFine() : int", "+ isOverdue() : boolean"], fill="#fde68a")
cls(510, 15, 160, "Book", ["- bookId : int", "- title : String", "- author : String"], ["+ isAvailable() : boolean", "+ markIssued()"])
f.line(170, 80, 260, 80, color=NAVY, sw=1.6)
f.line(420, 80, 510, 80, color=NAVY, sw=1.6)
f.text(181, 70, "1", size=10.5, color=RED, bold=True)
f.text(243, 70, "0..*", size=10.5, color=RED, bold=True)
f.text(437, 70, "0..*", size=10.5, color=RED, bold=True)
f.text(499, 70, "1", size=10.5, color=RED, bold=True)
f.text(215, 96, "has", size=10, color=SLATE, italic=True)
f.text(465, 96, "is for", size=10, color=SLATE, italic=True)
f.poly([(90, 142), (78, 160), (102, 160)], fill="#ffffff", stroke=NAVY, sw=1.6)
f.line(90, 142, 90, 128, color=NAVY, sw=1.6)
f.line(90, 160, 90, 178, color=NAVY, sw=1.6)
f.line(52, 178, 157, 178, color=NAVY, sw=1.6)
f.line(52, 178, 52, 196, color=NAVY, sw=1.6)
f.line(157, 178, 157, 196, color=NAVY, sw=1.6)
cls(5, 196, 95, "Student", ["- program"], ["+ borrowLimit()"], fill=MINT)
cls(110, 196, 95, "Teacher", ["- department"], ["+ borrowLimit()"], fill=MINT)
f.text(470, 232, "Visibility: + public, - private.\nMultiplicity: 1 exactly one,\n0..* zero or more.\nSubclasses redefine borrowLimit()\n(polymorphism).", size=10, color=SLATE, anchor="start")
```

A **class** is drawn as a rectangle with three compartments: the name, the **attributes** (data) and the **operations** (behaviour). A **visibility mark** can precede each member: + public, - private, # protected. The lines between classes carry the design:

| Relationship | Meaning | Notation | Library example |
|---|---|---|---|
| **Association** | objects know each other; carries a **multiplicity** (1, 0..1, 0..*, 1..*) | plain line | one Member has 0..* Loans |
| **Aggregation** | whole and parts, parts can live alone | line with hollow diamond at the whole | a Shelf has Books |
| **Composition** | whole and parts, parts die with the whole | line with filled diamond | an Invoice has InvoiceLines |
| **Generalisation (inheritance)** | a subclass is a kind of the superclass | line with hollow triangle at the superclass | Student and Teacher are kinds of Member |
| **Dependency** | one class uses another briefly | dashed arrow | FineCalculator uses Loan |

### Sequence diagrams

A **sequence diagram** shows one scenario of a use case. Objects (or actors) stand along the top as boxes, each with a dashed vertical **lifeline**; time runs downward. A solid arrow is a call (message), a dashed arrow is the return. The order of the arrows is the order of events, so a sequence diagram is the quickest way to find a missing operation: every arrow that arrives at an object must correspond to an operation in that object's class. In Figure 1.6 the arrow *isAvailable(bookId)* tells us that class Book (or the BOOK table's data-access class) needs that operation, which is exactly what Figure 1.5 lists.

```svgfig label="1.6" caption="Sequence diagram for the main flow of Borrow book. Time runs downward. Solid arrows are messages, dashed arrows are returns. Each message names an operation that some class in Figure 1.5 must provide."
f = Fig(640, 322)
xs = [80, 240, 400, 560]
names = [":Librarian", ":IssueScreen", ":LoanService", ":BookTable"]
for x, n in zip(xs, names):
    f.box(x - 58, 8, 116, 28, n, fill=BLUE, color=NAVY, size=11, bold=True)
    f.line(x, 36, x, 312, color=SLATE, sw=1.2, dash=True)
msgs = [(0, 1, 76, "1: issue(memberId, bookId)", False), (1, 2, 112, "2: createLoan()", False),
        (2, 3, 148, "3: isAvailable(bookId)", False), (3, 2, 184, "4: true", True),
        (2, 3, 220, "5: markIssued(bookId)", False), (2, 1, 256, "6: dueDate", True),
        (1, 0, 292, "7: slip printed", True)]
for a, b, y, lab, ret in msgs:
    f.arrow([(xs[a], y), (xs[b], y)], color=AMBER if ret else NAVY, sw=1.6, dash=ret)
    f.text((xs[a] + xs[b]) / 2, y - 8, lab, size=10, color=SLATE, bold=not ret)
```

### State diagrams

A **state diagram** (state machine) describes the life of one object whose behaviour depends on its history: a book is *Available*, then *Issued*, possibly *Overdue*, then back to *Available*. A black dot is the start; rounded boxes are **states**; arrows are **transitions** labelled *event [guard] / action*, where the guard in square brackets must be true for the transition to fire. State diagrams are the right tool for objects with a clear life cycle: orders, loans, exam papers, support tickets.

```svgfig label="1.7" caption="State diagram of one Book copy. The black dot is the start. A transition is labelled event [guard]. Returning a late book also needs the fine to be paid, so the Overdue to Available arrow carries a guard."
f = Fig(640, 232)
f.circle(18, 96, 7, fill=NAVY, stroke=NAVY)
f.box(55, 72, 120, 48, "Available", fill=MINT, stroke=TEAL, color=NAVY, size=12, bold=True, r=22)
f.box(260, 72, 120, 48, "Issued", fill=BLUE, color=NAVY, size=12, bold=True, r=22)
f.box(465, 72, 120, 48, "Overdue", fill=ROSE, stroke=RED, color=NAVY, size=12, bold=True, r=22)
f.arrow([(25, 96), (55, 96)], color=NAVY, sw=1.6)
f.arrow([(175, 90), (260, 90)], color=NAVY, sw=1.6, label="issue [member valid]", lpos=(217, 62), lsize=9.5)
f.arrow([(380, 90), (465, 90)], color=NAVY, sw=1.6, label="due date passes", lpos=(423, 62), lsize=9.5)
f.arrow([(320, 120), (320, 160), (115, 160), (115, 120)], color=TEAL, sw=1.6, label="return", lpos=(218, 176), lsize=10)
f.arrow([(525, 120), (525, 206), (140, 206), (140, 120)], color=RED, sw=1.6, label="return [fine paid]", lpos=(332, 222), lsize=10)
```

An **activity diagram** is the object-oriented flowchart: rounded actions, diamonds for decisions, thick bars for fork and join (parallel work), and **swimlanes** that show which actor performs each action. It is the usual way to show a business process before it is split into use cases.

### From the diagrams to code

The diagrams are a bridge to the programming units. Each class becomes a Java or Python class, each attribute a field, each operation a method, each association a field or collection reference (Member holds a list of Loan), and each generalisation an `extends`. A state diagram becomes an `enum` plus a `switch` in the methods that change state. A sequence diagram becomes the body of one method: the arrows leaving :LoanService are the calls made inside `createLoan()`.

::: note Structured versus object-oriented: say it in two lines
Structured analysis separates **processes** (DFD) from **data** (ER) and asks "what happens to the data?". Object-oriented analysis keeps data and behaviour together in **classes** and asks "which objects collaborate to do this?". Both are valid in an exam; a good answer names one diagram from each family and says what question it answers.
:::

## 1.15 Acquiring a system: build, buy, outsource or rent

The TU syllabus lists **system acquisition** and **reuse** under the origins of software. The decision is rarely "write everything ourselves". It is a comparison of fit, cost over several years, risk and speed.

### Total cost of ownership

The **licence or development price is only the first line** of the bill. The **total cost of ownership (TCO)** adds set-up, customisation, training, annual support, upgrades and the cost of leaving. A five-year view prevents a cheap start from hiding an expensive tail.

::: example Worked example: five-year TCO of three routes for a college fee system (Rs, invented figures)
- **Build in-house:** development 1,800,000 once; maintenance 270,000 a year. Five years: 1,800,000 + 5 x 270,000 = **3,150,000**.
- **Buy a package and customise it:** licence 600,000 + customisation 400,000 once; support 120,000 a year. Five years: 600,000 + 400,000 + 5 x 120,000 = **1,600,000**.
- **Rent software as a service:** set-up 100,000 once; subscription 15,000 a month = 180,000 a year. Five years: 100,000 + 5 x 180,000 = **1,000,000**.
The cheapest total is the rented service, but the subscription never ends and the college does not own the code; the in-house build costs three times as much but fits the college's rules exactly. TCO therefore **feeds** the decision; it does not make it.
:::

### Scoring vendors with a weighted matrix

After the RFP, the committee scores each proposal against criteria that were weighted **before** the proposals arrived (otherwise the weights drift toward the favourite). Each score runs from 1 (poor) to 5 (excellent); the weighted total is the sum of weight x score.

| Criterion | Weight | A: packaged | B: local firm, custom | C: SaaS |
|---|---|---|---|---|
| Functionality (fit to rules) | 30 | 4 | 5 | 3 |
| Total cost (TCO, higher score = cheaper) | 25 | 4 | 2 | 4 |
| Support and maintenance | 20 | 3 | 4 | 4 |
| Flexibility to change | 15 | 2 | 5 | 3 |
| Training and documentation | 10 | 4 | 4 | 3 |
| **Weighted total (out of 500)** | 100 | **350** | **395** | **345** |

Check, vendor B: 30 x 5 + 25 x 2 + 20 x 4 + 15 x 5 + 10 x 4 = 150 + 50 + 80 + 75 + 40 = **395**. Vendor B wins on fit and flexibility even though it is the dearest, because the committee gave functionality the biggest weight. Change the weights (cost 40, functionality 20) and the order changes: **always run a sensitivity check** and write the reason for the final choice in the project file.

### Reuse

**Reuse** means building the new system from parts that already exist. Levels, from small to large: copied code, **libraries and frameworks**, **components and services** (a payment API, an SMS gateway), **design patterns** and whole **product lines**. Benefits are lower cost, fewer defects and faster delivery. The costs are real: reusable parts must be documented and tested, their licences checked (MIT, Apache, GPL differ in what they require of your code), and their updates tracked, because a library with a security hole becomes your security hole.

| Route | Best when | Main risk | Question to ask before choosing |
|---|---|---|---|
| Build | the process is unique and gives advantage | cost, delay, skills | can we maintain it for years? |
| Buy package | the process is standard (accounts, payroll) | forcing the business to fit the package | how many requirements are met without customising? |
| Outsource | skills or staff are missing | dependence, confidentiality | who owns the code and the data? |
| Rent (SaaS) | quick start, small IT team | lock-in, data location, price rises | can we export our data in a usable format? |
| Reuse components | common technical needs | licence and update burden | is the component maintained and licensed for our use? |

## 1.16 Project management software, the work breakdown structure and earned value

Section 1.9 introduced Gantt charts and the critical path. Real projects add three more habits: break the work down properly, record a **baseline**, and measure progress in money and time with the same yardstick.

### Work breakdown structure (WBS)

A **work breakdown structure** divides the project deliverables into smaller and smaller pieces until each piece is a **work package** that one person can estimate, assign and finish in a few days. The rule of thumb is the **100 per cent rule**: the children of a box add up to exactly the parent, nothing missing and nothing extra. A WBS is organised by deliverable (nouns: *Result database*, *Marks-entry screen*), not by activity, and it is the checklist from which the schedule and the budget are built. For the result system a first level could be: 1 Management, 2 Requirements, 3 Database, 4 Screens, 5 Reports, 6 Testing, 7 Deployment and training; the work package *3.2 Create tables and keys* then feeds the network diagram as an activity with a duration and a predecessor.

### What project management software does

Tools such as MS Project, OpenProject, Jira, Trello or a spreadsheet template keep the plan alive. Their useful features, in the order a student project meets them:

1. **Task list with dependencies.** Finish-to-start is the usual link; start-to-start (both begin together) and finish-to-finish also exist, and **lag** or **lead** time can be added.
2. **Automatic critical path.** Change one duration and the whole schedule is recalculated, including the slack of every task.
3. **Resources and calendars.** Assigning one person to two tasks at the same time shows **over-allocation**; a holiday such as Dashain removes working days from the calendar.
4. **Baseline.** A saved copy of the approved plan. The software then shows variance: planned versus actual dates and effort.
5. **Boards and backlogs** (Jira, Trello): cards move across *To do, In progress, Done*, which suits agile sprints better than a Gantt chart.
6. **Reports:** milestone list, burn-down chart, resource load, cost to date.

The software calculates; it does not manage. A beautiful plan built on wrong estimates is a precise error.

### Earned value in one page

**Earned value management (EVM)** answers "are we ahead or behind, and are we over or under budget?" with three quantities at the status date:

- **Planned value (PV)** = the budgeted cost of the work that **should** be finished by now.
- **Earned value (EV)** = the budgeted cost of the work **actually** finished.
- **Actual cost (AC)** = the money actually spent.

| Measure | Formula | Reading |
|---|---|---|
| Schedule variance | SV = EV - PV | negative: behind schedule |
| Cost variance | CV = EV - AC | negative: over budget |
| Schedule performance index | SPI = EV / PV | below 1: behind |
| Cost performance index | CPI = EV / AC | below 1: over budget |
| Estimate at completion | EAC = BAC / CPI | forecast final cost if the present efficiency continues |

::: example Worked example: a result system a third of the way through
Budget at completion BAC = Rs 1,000,000. At the status date, the plan says 50 per cent should be finished; the team has finished 40 per cent and spent Rs 520,000.
PV = 0.50 x 1,000,000 = **500,000**; EV = 0.40 x 1,000,000 = **400,000**; AC = **520,000**.
SV = 400,000 - 500,000 = **-100,000** and SPI = 400,000 / 500,000 = **0.80**: the project is 20 per cent behind schedule.
CV = 400,000 - 520,000 = **-120,000** and CPI = 400,000 / 520,000 = **0.77**: every rupee spent buys 77 paisa of planned work.
EAC = 1,000,000 / 0.769 = **1,300,000**: if nothing changes the project ends **Rs 300,000 over** budget. The manager must act now (reduce scope, add skilled help, or ask the sponsor) rather than at the end.
:::

::: note Why earned value beats "percent of budget spent"
Spending 52 per cent of the budget sounds like being close to the plan of 50 per cent. Only EV shows that the 52 per cent bought just 40 per cent of the work. Money spent is never a measure of progress on its own.
:::

## Formula and fact sheet

- SDLC: planning → analysis → design → implementation → maintenance.
- PERT expected time = (a + 4m + b)/6; σ = (b − a)/6. Slack = LS − ES = LF − EF.
- Critical path = longest path, zero slack, sets project duration.
- Waterfall: sequential, fixed requirements. Agile: iterations, change welcome. XP: pair programming, TDD, CI, refactoring.
- IS types: TPS, MIS, DSS, ESS, expert.
- UML: use case (actors, include, extend), class (association, aggregation, composition, generalisation), sequence (time downward), state (event [guard]).
- TCO = purchase or build + set-up + years x (support + maintenance). Weighted score = sum of weight x score.
- Earned value: SV = EV - PV, CV = EV - AC, SPI = EV/PV, CPI = EV/AC, EAC = BAC/CPI.

## Chapter summary

- Information systems come in several types and are built through an SDLC under a chosen model; each model trades predictability for flexibility.
- CASE tools, SOA and OOAD/UML are supporting technologies; agile methods and XP emphasise short iterations.
- Software may be built, bought, outsourced or reused; the project manager schedules with Gantt charts and the critical path method.

## Practice

1. Define system, information system and systems analyst.
2. Differentiate TPS, MIS and DSS with examples.
3. Describe the phases of the SDLC and the output of each.
4. Compare waterfall and agile; when is each suitable?
5. What is RAD? List its strengths and risks.
6. List the XP practices.
7. Compare building in-house, buying packaged software and outsourcing.
8. Activities: A 2 (none), B 4 (A), C 3 (A), D 2 (B, C). Find the project duration, critical path and slack of C.
9. Compute the PERT expected time for a = 4, m = 6, b = 14.
10. Draw a use case diagram for an online examination system with the actors Student, Teacher and Admin, and show one include and one extend relationship.
11. Distinguish the include and extend relationships between use cases with one example each.
12. For Student, Course and Enrolment, give the classes, two attributes each, and the multiplicities of the associations.
13. List the messages of a sequence diagram for withdrawing cash from an ATM.
14. List the states and transitions of an online order.
15. Build costs Rs 2,000,000 plus Rs 300,000 a year; a package costs Rs 900,000 plus Rs 150,000 a year. Compare the four-year TCO.
16. Weights: function 50, cost 30, support 20. Vendor X scores 4, 3, 5; vendor Y scores 5, 4, 2 (scale 1 to 5). Which wins?
17. BAC = Rs 600,000. The plan says 50 per cent should be done; 35 per cent is done and Rs 240,000 is spent. Find SV, CV, SPI, CPI and EAC.

::: note Answers and worked solutions
**1.** System: interrelated components pursuing a goal. IS: people, procedures, data, hardware and software that process information. Analyst: the person who studies the business problem and defines and designs the solution.
**2.** TPS records transactions (a bus ticketing counter); MIS summarises them for managers (monthly sales report); DSS supports what-if decisions (a budget simulator).
**3.** See the table in 1.3: planning → plan; analysis → requirements and models; design → design specifications; implementation → tested installed system; maintenance → fixes and enhancements.
**4.** Waterfall suits stable, well-understood requirements and fixed-price contracts; agile suits changing requirements and where early feedback matters.
**5.** RAD builds in short timeboxes with prototypes, heavy user participation and CASE. Strengths: speed, user fit. Risks: needs a skilled small team, weak for very large or high-performance systems.
**6.** Pair programming, TDD, continuous integration, small releases, refactoring, simple design, collective ownership, on-site customer, sustainable pace, user stories.
**7.** In-house: tailored but slow and costly; packaged: quick and cheap but must adapt to the package; outsourcing: access to skills but dependence and contract management.
**8.** Paths: A-B-D = 2 + 4 + 2 = 8; A-C-D = 2 + 3 + 2 = 7. Duration **8**; critical path **A → B → D**; slack of C = 8 − 7 = **1**.
**9.** t = (4 + 24 + 14)/6 = **7**.
**10.** Actors outside the boundary; use cases: Log in, Take exam, Submit answers, View result (Student); Create question set, Mark answers (Teacher); Manage users (Admin). Take exam *includes* Log in; Show timeout warning *extends* Take exam (only when time is nearly over).
**11.** Include: always happens as a part of the base use case (Borrow book includes Verify membership). Extend: optional, conditional addition (Calculate fine extends Return book when the book is late).
**12.** Student (studentId, name), Course (courseCode, title), Enrolment (enrolDate, grade). Student 1 to 0..* Enrolment; Course 1 to 0..* Enrolment; Enrolment resolves the many-to-many link between Student and Course.
**13.** Customer inserts card; ATM sends verifyPin(); Bank returns ok; ATM sends withdraw(amount); Bank checks balance and returns approved; ATM dispenses cash; ATM prints receipt.
**14.** Placed, Paid, Packed, Shipped, Delivered; Cancelled (from Placed or Paid). Events: pay, pack, ship, deliver, cancel [before shipping].
**15.** Build: 2,000,000 + 4 x 300,000 = **3,200,000**. Package: 900,000 + 4 x 150,000 = **1,500,000**. The package is cheaper by **1,700,000** over four years.
**16.** X: 50 x 4 + 30 x 3 + 20 x 5 = 200 + 90 + 100 = **390**. Y: 50 x 5 + 30 x 4 + 20 x 2 = 250 + 120 + 40 = **410**. Y wins by 20 points.
**17.** PV = 300,000; EV = 210,000; SV = **-90,000**; SPI = **0.70**; CV = 210,000 - 240,000 = **-30,000**; CPI = **0.875**; EAC = 600,000 / 0.875 = **Rs 685,714**.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Describe the phases of the systems development life cycle (SDLC) and the main output of each.**

*Introduction.* The SDLC is a structured, phase-by-phase method for building an information system. Each phase answers one question and ends with a review gate before the next begins (Figure 1.1).

*Phases.*

1. **Planning.** Decides whether the project is worth doing. Activities: identify and select the project, study feasibility (economic, technical, operational, schedule, legal, political). Output: the baseline project plan.
2. **Analysis.** Decides what the system must do. Requirements are gathered by interviews, questionnaires and observation, and modelled with data flow diagrams and entity-relationship diagrams. Output: requirements specification and logical models.
3. **Design.** Decides how the system will do it. Logical design is turned into physical design: database tables, screens, reports and program structure. Output: design specification.
4. **Implementation.** Coding, testing, installation, data conversion, documentation and user training. Output: the working, accepted system.
5. **Maintenance.** The system is corrected, adapted and enhanced during its life. Output: change requests, patches and new versions.

| Phase | Question | Main output |
|---|---|---|
| Planning | Is it worth doing? | baseline plan |
| Analysis | What must it do? | requirements, models |
| Design | How will it do it? | design specification |
| Implementation | Build and deliver | tested system |
| Maintenance | Keep it useful | updates |

*Conclusion.* Errors cost much more to fix in later phases (Figure 1.1), so early phases deserve careful effort.

**Q2 (10 marks). Compare the waterfall, prototyping, spiral, RAD and agile approaches to system development, and recommend one for a college result-management system whose rules change every semester.**

*Introduction.* No single life-cycle model suits every project. The choice depends on how clear the requirements are, how risky the project is, and how involved the users can be.

*The models.*

1. **Waterfall.** Phases run strictly in sequence with documents as contracts. It is simple and easy to manage, but users see the product only at the end and change is costly.
2. **Prototyping.** A quick working model is shown to users and refined. It is excellent when requirements are unclear, but can drift into endless iteration.
3. **Spiral.** Repeated cycles of planning, risk analysis, building and evaluation. It suits large, risky systems but needs risk expertise and is expensive.
4. **Incremental.** Working slices are delivered one after another, giving early value.
5. **RAD.** Timeboxed builds of 60 to 90 days with heavy user involvement, reuse and CASE tools. It suits well-bounded systems.
6. **Agile.** One- to four-week iterations deliver working software, with continuous customer collaboration and welcome for change (Plate 1.1).

| Model | Requirements | User involvement | Risk handling | Best for |
|---|---|---|---|---|
| Waterfall | fixed, clear | low until end | weak | stable, well-known systems |
| Prototyping | unclear | high | moderate | new interfaces |
| Spiral | evolving | medium | strong | large, risky systems |
| RAD | bounded | very high | moderate | small, fast systems |
| Agile | changing | continuous | strong, by short cycles | volatile needs |

*Recommendation.* A result-management system whose rules change every semester has changing requirements and strong user involvement (examination staff). **Agile with short iterations** is the best fit: build the core mark entry and result calculation first, show it to staff after two weeks, and adjust the rules in the next iteration. A short initial feasibility study is still needed, because even agile projects must justify cost.

*Conclusion.* Waterfall suits fixed requirements; prototyping, RAD and agile suit uncertainty; spiral suits risk. Matching the model to the project is part of good analysis.
